from collections import Sequence
from typing import Optional, Union, List, Dict

import numpy as np
import pandas as pd
import torch
from pytorch_forecasting.data import timeseries
from pytorch_forecasting.data.encoders import (
    NaNLabelEncoder,
    EncoderNormalizer,
    TorchNormalizer
)


from sklearn.preprocessing import RobustScaler, StandardScaler


class TimeseriesDataset(timeseries.TimeSeriesDataSet):
    """Dataset for time series models.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe with time series data. Each row can be identified with
        ``date`` and the ``group_ids``.

    group_ids : list of str
        List of column names identifying a time series. This means that the
        ``group_ids`` identify a sample together with ``date``. If you
        have only one times series, set this to the name of column that is
        constant.

    time_idx : str
        Time index column.

    target : str
        Target column.

    max_prediction_length : int
        Maximum prediction/decoder length. Usually this is defined by the
        difference between forecasting dates.

    max_encoder_length : int, default=None
        Maximum length to encode (also known as `input sequence length`). This
        is the maximum history length used by the time series dataset.

    time_varying_known_reals : list of str
        List of continuous variables that change over time and are known in the
        future (e.g. price of a product, but not demand of a product).

    time_varying_unknown_reals : list of str
        List of continuous variables that change over time and are not known in
        the future. You might want to include your ``target`` here.

    static_categoricals : list of str
        List of categorical variables that do not change over time (also known
        as `time independent variables`). You might want to include your
        ``group_ids`` here for the learning algorithm to distinguish between
        different time series.

    scalers : dict, default=None
        Dictionary of scalers or `None` for using no normalizer.

    categorical_encoders : dict, default=None
        Dictionary of label transformers or `None` for using
        :class:`encoders.NanLabelEncoder`.

    target_normalizer : TorchNormalizer,
    default=TorchNormalizer(method='identity')
        Transformer that take group_ids, target and time_idx to normalize
        targets or `None` for using no normalizer / normalizer with `center=0`
        and `scale=1` (`method="identity"`).
    """

    def __init__(
            self,
            data: pd.DataFrame,
            group_ids: List[str],
            time_idx: str,
            target: str,
            max_prediction_length: int,
            max_encoder_length: int,
            time_varying_known_reals: List[str],
            time_varying_unknown_reals: List[str],
            static_categoricals: List[str],
            scalers: Optional[Dict[str, Union[
                StandardScaler, RobustScaler, TorchNormalizer,
                EncoderNormalizer]]] = None,
            categorical_encoders: Optional[Dict[str, NaNLabelEncoder]] = None,
            target_normalizer: Optional[TorchNormalizer] =
            TorchNormalizer(method='identity'),
            predict_mode=False
    ):
        if scalers is None:
            reals = time_varying_known_reals + time_varying_unknown_reals
            scalers = {name: None for name in reals if name != target}

        if categorical_encoders is None:
            categorical_encoders = {
                name: NaNLabelEncoder()
                for name in static_categoricals
            }

        super().__init__(
            data=data, time_idx=time_idx, target=target, group_ids=group_ids,
            max_encoder_length=max_encoder_length,
            max_prediction_length=max_prediction_length,
            time_varying_known_reals=time_varying_known_reals,
            time_varying_unknown_reals=time_varying_unknown_reals,
            static_categoricals=static_categoricals, scalers=scalers,
            categorical_encoders=categorical_encoders,
            target_normalizer=target_normalizer, predict_mode=predict_mode)

    def _construct_index(
            self,
            data: pd.DataFrame,
            predict_mode: bool
    ) -> pd.DataFrame:

        df_index = super()._construct_index(data, predict_mode=False)

        if predict_mode:
            # Get the rows containing the max sequence length of their group.
            # Note that if a group has multiple max values, all will be
            # returned.
            max_on_each_row = df_index.groupby('sequence_id')[
                'sequence_length'].transform(max)
            idx = (max_on_each_row == df_index['sequence_length'])
            return df_index.loc[idx].reset_index(drop=True)

        return df_index


class SliceDataset(Sequence, torch.utils.data.Dataset):
    """Makes Dataset sliceable.

    Helper class that wraps a torch dataset to make it work with
    sklearn. That is, sometime sklearn will touch the input data, e.g. when
    splitting the data for a grid search. This will fail when the input data is
    a torch dataset. To prevent this, use this wrapper class for your
    dataset.

    ``dataset`` attributes are also available from :class:`SliceDataset`
    object (see Examples section).

    Parameters
    ----------
    dataset : torch.utils.data.Dataset
      A valid torch dataset.

    indices : list, np.ndarray, or None (default=None)
      If you only want to return a subset of the dataset, indicate
      which subset that is by passing this argument. Typically, this
      can be left to be None, which returns all the data.

    Examples
    --------
    >>> X = MyCustomDataset()
    >>> search = GridSearchCV(net, params, ...)
    >>> search.fit(X, y)  # raises error
    >>> ds = SliceDataset(X)
    >>> search.fit(ds, y)  # works
    >>> ds.a  # returns 1 since ``X`` attributes are also available from ``ds``

    Notes
    -----
    This class will only return the X value by default (i.e. the
    first value returned by indexing the original dataset). Sklearn,
    and hence skorch, always require 2 values, X and y. Therefore, you
    still need to provide the y data separately.

    This class behaves similarly to a PyTorch
    :class:`~torch.utils.data.Subset` when it is indexed by a slice or
    numpy array: It will return another ``SliceDataset`` that
    references the subset instead of the actual values. Only when it
    is indexed by an int does it return the actual values. The reason
    for this is to avoid loading all data into memory when sklearn,
    for instance, creates a train/validation split on the
    dataset. Data will only be loaded in batches during the fit loop.
    """

    def __init__(
            self,
            dataset: torch.utils.data.Dataset,
            indices: Optional[Union[List[int], np.array]] = None
    ):
        self.dataset = dataset
        self.indices = indices
        self.indices_ = (
            self.indices if self.indices is not None
            else np.arange(len(self.dataset))
        )
        self.ndim = 1

    @property
    def shape(self):
        return len(self)

    def transform(self, data):
        """Additional transformations on ``data``.

        Notes
        -----
        If you use this in conjunction with PyTorch
        :class:`~torch.utils.data.DataLoader`, the latter will call
        the dataset for each row separately, which means that the
        incoming ``data`` is a single rows.

        """
        return data

    def __getattr__(self, attr):
        """If attr is not in self, look in self.dataset.

        Notes
        -----
        Issues with serialization were solved with the following discussion:
        https://stackoverflow.com/questions/49380224/how-to-make-classes-with-getattr-pickable
        """
        if 'dataset' not in vars(self):
            raise AttributeError
        return getattr(self.dataset, attr)

    def __len__(self):
        return len(self.indices_)

    def __getitem__(self, i):
        if isinstance(i, (int, np.integer)):
            Xn = self.dataset[self.indices_[i]]
            return self.transform(Xn)
        if isinstance(i, slice):
            return SliceDataset(self.dataset, indices=self.indices_[i])
        if isinstance(i, np.ndarray):
            if i.ndim != 1:
                raise IndexError(
                    "SliceDataset only supports slicing with 1 "
                    "dimensional arrays, got {} dimensions "
                    "instead".format(i.ndim)
                )
            if i.dtype == np.bool:
                i = np.flatnonzero(i)
        return SliceDataset(self.dataset, indices=self.indices_[i])
