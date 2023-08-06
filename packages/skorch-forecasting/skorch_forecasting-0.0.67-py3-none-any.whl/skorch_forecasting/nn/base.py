import inspect
from abc import ABCMeta, abstractmethod
from typing import Dict, Union, Type, Any, List, Callable, Literal

import numpy as np
import pandas as pd
import sklearn
import skorch
import torch
from pytorch_forecasting import metrics

from . import datasets
from ..utils import validation


class Transformer(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    """Transformer generic type.

    Must implement `fit`/`transform` methods.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        pass


class BaseOutputDecoder:
    """Base class for output transformers.

    .. note::
        This class should not be used directly. Use derived classes instead.
    """

    def __init__(self, dataset: datasets.TimeseriesDataset):
        self.dataset = dataset

    def decode(self, X: np.ndarray, out: pd.DataFrame = None):
        pass


class BaseModule(torch.nn.Module, metaclass=ABCMeta):
    """Base class for pytorch neural network modules.

    .. note::
        This class should not be used directly. Use derived classes instead.
    """

    @classmethod
    @abstractmethod
    def from_dataset(cls, dataset, **kwargs):
        """Create model from dataset

        Parameters
        ----------
        dataset : timeseries dataset

        Returns
        -------
        BaseModule: Model that can be trained
        """
        pass


class NeuralNetEstimator(sklearn.base.BaseEstimator):
    """Base class for all neural net estimators in skorch-forecasting.
    """

    def _get_param_names(self):
        return (k for k in self.__dict__ if not k.endswith('_'))

    def get_params(self, deep: bool = True) -> Dict:
        params = super().get_params(deep=deep)

        # Don't include the following attributes.
        to_exclude = {'module', 'dataset'}
        return {key: val for key, val in params.items() if
                key not in to_exclude}

    def get_init_signature(self, cls: Type[Any]) -> inspect.Signature:
        """Retrieves __init__ signature from ``cls``.

        Parameters
        ----------
        cls : class

        Returns
        -------
        Signature
        """
        init = getattr(cls.__init__, "deprecated_original", cls.__init__)
        return inspect.signature(init)

    def get_kwargs_for(self, name: str, add_prefix: bool = False) -> Dict:
        """Collects __init__ kwargs for an attribute.

        Attributes must be type class and could be, for instance, pytorch
        modules, criteria or data loaders.

        The returned kwargs are obtained by inspecting the __init__ method
        from the passed attribute (e.g., module.__init__()) and from prefixed
        kwargs (double underscore notation, e.g., 'module__something') passed
        at __init__.

        Parameters
        ----------
        name : str
            The name of the attribute whose arguments should be
            returned. E.g. for the module, it should be ``'module'``.

        add_prefix : bool
            If True, keys will contain ``name`` with double underscore as
            prefix.

        Returns
        -------
        kwargs : dict
        """
        cls = getattr(self, name)

        # Consider the constructor parameters.
        init_signature = self.get_init_signature(cls)
        kwargs = self._get_init_kwargs(init_signature)

        # Consider kwargs with prefix "name".
        kwargs.update(
            skorch.utils.params_for(prefix=name, kwargs=self.__dict__))

        if add_prefix:
            kwargs = {name + '__' + k: v for k, v in kwargs.items()}
        return kwargs

    def _get_init_kwargs(self, init_signature):
        return {
            k: v
            for k, v in self.__dict__.items()
            if k in init_signature.parameters
        }


class TimeseriesNeuralNet(NeuralNetEstimator):
    """Base class for time series neural nets.

    In addition to the parameters listed below, there are parameters
    with specific prefixes that are handled separately. To illustrate
    this, here is an example:

    >>> net = TimeseriesNeuralNet(
    ...    [...],
    ...    optimizer=torch.optim.SGD,
    ...    optimizer__momentum=0.95,
    ...)

    This way, when ``optimizer`` is initialized, :class:`.NeuralNet`
    will take care of setting the ``momentum`` parameter to 0.95.
    (Note that the double underscore notation in
    ``optimizer__momentum`` means that the parameter ``momentum``
    should be set on the object ``optimizer``. This is the same
    semantic as used by sklearn.). Supported prefixes include:
    ['module',
    'iterator_train',
    'iterator_valid',
    'optimizer',
    'criterion',
    'callbacks',
    'dataset']

    .. note::
        This class should not be used directly. Use derived classes instead.
    
    Parameters
    ----------
    module : class
        Neural network class that inherits from :class:`BaseModule`

    group_ids : list of str
        List of column names identifying a time series. This means that the
        group_ids identify a sample together with the time_idx. If you have
        only one time series, set this to the name of column that is constant.

    time_idx : str
        Time index column. This column is used to determine the sequence of
        samples.

    target : str
        Target column. Column containing the values to be predicted.

    max_prediction_length : int
        Maximum prediction/decoder length (choose this not too short as it can
        help convergence)

    max_encoder_length : int
        Maximum length to encode. This is the maximum history length used by
        the time series dataset.

    time_varying_known_reals : list of str
        List of continuous variables that change over time and are known in the
        future (e.g. price of a product, but not demand of a product). If None,
        every numeric column excluding ``target`` is used.

    time_varying_unknown_reals : list of str
        List of continuous variables that change over time and are not known in
        the future. You might want to include your ``target`` here. If None,
        only ``target`` is used.

    static_categoricals : list of str
        List of categorical variables that do not change over time (also known
        as `time independent variables`). You might want to include your
        ``group_ids`` here for the learning algorithm to distinguish between
        different time series. If None, only ``group_ids`` is used.
      
    dataset : class
        The dataset is necessary for the incoming data to work with
        pytorch :class:`DataLoader`. Must inherit from
        :class:`pytorch.utils.data.Dataset`.

    min_encoder_length : int, default=None
        Minimum allowed length to encode. If None, defaults to
        ``max_encoder_length``.

    criterion : class, default=None
        The uninitialized criterion (loss) used to optimize the
        module. If None, the root mean squared error (:class:`RMSE`) is used.

    optimizer : class, default=None
        The uninitialized optimizer (update rule) used to optimize the
        module. If None, :class:`Adam` optimizer is used.

    lr : float, default=1e-5
        Learning rate passed to the optimizer.

    max_epochs : int, default=10
        The number of epochs to train for each :meth:`fit` call. Note that you
        may keyboard-interrupt training at any time.

    batch_size : int, default=64
        Mini-batch size. If ``batch_size`` is -1, a single batch with all the
        data will be used during training and validation.

    callbacks: None, “disable”, or list of Callback instances, default=None
        Which callbacks to enable.

        - If callbacks=None, only use default callbacks which include:
            - `epoch_timer`: measures the duration of each epoch
            - `train_loss`: computes average of train batch losses
            - `valid_loss`: computes average of valid batch losses
            - `print_log`:  prints all of the above in nice format

        - If callbacks="disable":
            disable all callbacks, i.e. do not run any of the callbacks.

        - If callbacks is a list of callbacks:
            use those callbacks in addition to the default ones. Each
            callback should be an instance of skorch :class:`.Callback`.

        Alternatively, a tuple ``(name, callback)`` can be passed, where
        ``name`` should be unique. Callbacks may or may not be instantiated.
        The callback name can be used to set parameters on specific
        callbacks (e.g., for the callback with name ``'print_log'``, use
        ``net.set_params(callbacks__print_log__keys_ignored=['epoch',
        'train_loss'])``).

    warm_start: bool, default=False
        Whether each fit call should lead to a re-initialization of the module
        (cold start) or whether the module should be trained further
        (warm start).

    verbose : int, default=1
        This parameter controls how much print output is generated by
        the net and its callbacks. By setting this value to 0, e.g. the
        summary scores at the end of each epoch are no longer printed.
        This can be useful when running a hyperparameters search. The
        summary scores are always logged in the history attribute,
        regardless of the verbose setting.

    device : str, torch.device, default='cpu'
        The compute device to be used. If set to 'cuda', data in torch
        tensors will be pushed to cuda tensors before being sent to the
        module. If set to None, then all compute devices will be left
        unmodified.

    kwargs : dict
       Extra prefixed parameters (see list of supported prefixes above).

    Attributes
    ----------
    dataset_params_ : dict
        Training dataset parameters.

    nn_ : skorch.NeuralNet
        Fitted skorch neural network.
    """

    prefixes = [
        'module',
        'iterator_train',
        'iterator_valid',
        'optimizer',
        'criterion',
        'callbacks',
        'dataset'
    ]

    def __init__(
            self,
            module: Type[BaseModule], dataset: Type[datasets.TimeseriesDataset],
            group_ids: List[str], time_idx: str, target: str,
            max_prediction_length: int, max_encoder_length: int,
            time_varying_known_reals: List[str],
            time_varying_unknown_reals: List[str],
            static_categoricals: List[str],
            criterion: metrics.MultiHorizonMetric,
            optimizer: torch.optim.Optimizer,
            train_split: Callable = None, lr: float = 1e-5,
            max_epochs: int = 10, batch_size: int = 64,
            min_encoder_length: int = None, callbacks: List = None,
            warm_start: bool = False, collate_fn: Callable = None,
            output_decoder: Type[BaseOutputDecoder] = None,
            verbose: int = 1, device: Literal["cpu", "cuda"] = 'cpu',
            **kwargs
    ):
        self.module = module
        self.dataset = dataset
        self.group_ids = group_ids
        self.time_idx = time_idx
        self.target = target
        self.max_prediction_length = max_prediction_length
        self.max_encoder_length = max_encoder_length
        self.time_varying_known_reals = time_varying_known_reals
        self.time_varying_unknown_reals = time_varying_unknown_reals
        self.static_categoricals = static_categoricals
        self.min_encoder_length = min_encoder_length
        self.criterion = criterion
        self.optimizer = optimizer
        self.train_split = train_split
        self.lr = lr
        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.callbacks = callbacks
        self.warm_start = warm_start
        self.verbose = verbose
        self.device = device
        self.collate_fn = collate_fn
        self.output_decoder = output_decoder
        vars(self).update(kwargs)

    def fit(
            self,
            X: Union[pd.DataFrame, torch.utils.data.Dataset],
            y=None
    ) -> NeuralNetEstimator:
        """Initialize and fit the neural net estimator.

        If the module was already initialized, by calling fit, the module
        will be re-initialized (unless warm_start is True).

        Parameters
        ----------
        X : pd.DataFrame
            The input data

        y : None
            This parameter only exists for sklearn compatibility and must
            be left in None.

        Returns
        -------
        self : NeuralNetEstimator
        """
        X = self.get_dataset(X)

        if validation.bool_check_is_fitted(self):
            self.nn_.fit(X)
        else:
            skorch_nn = self._initialize_skorch_nn(X)
            skorch_nn.fit(X)
            self.nn_ = skorch_nn
            self.dataset_params_ = X.get_parameters()

        return self

    def predict(
            self,
            X: Union[pd.DataFrame, torch.utils.data.Dataset],
            return_dataset: bool = False
    ) -> Union[np.array, pd.DataFrame]:
        """Predicts input data X.

        Parameters
        ----------
        X : pd.DataFrame
            Input values.

        return_dataset : bool, default=False
            If True, predict dataset is also returned.

        Returns
        -------
        output : np.array.
            Predicted values.
        """
        validation.check_is_fitted(self)
        dataset = self.get_predict_dataset(X)
        output = self.nn_.predict(dataset)
        if return_dataset:
            return output, dataset
        return output

    def pretty_predict(self, X: pd.DataFrame):
        output, dataset = self.predict(X, return_dataset=True)
        return self.output_decoder(dataset).decode(output, out=X)

    def get_predict_dataset(self, X: pd.DataFrame) -> torch.utils.data.Dataset:
        """Returns dataset in prediction mode.

        Parameters
        ----------
        X : pd.DataFrame
            Input values.

        Returns
        -------
        dataset : torch.utils.data.Dataset
        """
        validation.check_is_fitted(self)
        return self.get_dataset(X, self.dataset_params_, predict_mode=True)

    def get_dataset(
            self,
            X: pd.DataFrame,
            params: Union[Dict, None] = None,
            sliceable: bool = False,
            **kwargs
    ) -> torch.utils.data.Dataset:
        """Constructs torch dataset using the input data ``X``

        Parameters
        ----------
        X : pd.DataFrame
            Input data

        params : dict, default=None
            If given, generates torch dataset using this parameters. Otherwise,
            the parameters are obtained from the object (self) attributes.

        sliceable : bool, default=False
            If True, the sliceable version of the dataset is returned.

        **kwargs : key-word arguments
            Additional parameters passed to dataset class. If given,
            kwargs will override values given to ``params``.

        Returns
        -------
        dataset: torch dataset
            The initialized dataset.
        """
        # Return ``X`` if already is a dataset
        if isinstance(X, torch.utils.data.Dataset):
            return X

        if params is not None:
            dataset = self.dataset.from_parameters(params, X, **kwargs)
        else:
            dataset_params = self.get_kwargs_for('dataset')
            dataset_params.update(kwargs)
            dataset = self.dataset(X, **dataset_params)
        if sliceable:
            return datasets.SliceDataset(dataset)
        return dataset

    def get_history(
            self,
            name: str,
            step_every: Literal["batch", "epoch"] = 'epoch'
    ) -> List:
        """Obtains history.

        Parameters
        ----------
        name : str
            Name of history.

        step_every : str {'batch', 'epoch'}, default='epoch'

        Returns
        -------
        history : list
        """
        validation.check_is_fitted(self)
        if step_every == 'epoch':
            history = self.nn_.history_[:, name]

        elif step_every == 'batch':
            history = []
            for epoch in self.nn_.history_:
                for batch in epoch['batches']:
                    if batch:
                        val = batch[name]
                        history.append(val)

        else:
            raise ValueError('`step_every` can be either "epoch" or "batch".')

        return history

    def _initialize_skorch_nn(self, X):
        """Initializes :class:`NeuralNet`.

        Parameters
        ----------
        X : torch dataset
            Training dataset

        Returns
        -------
        skorch NeuralNet fitted
        """
        return skorch.NeuralNet(
            module=self._initialize_module(X), criterion=self.criterion,
            optimizer=self.optimizer, lr=self.lr, max_epochs=self.max_epochs,
            batch_size=self.batch_size, callbacks=self.callbacks,
            verbose=self.verbose, device=self.device,
            warm_start=self.warm_start, train_split=self.train_split,
            iterator_train__shuffle=True,
            iterator_train__collate_fn=self.collate_fn,
            iterator_valid__collate_fn=self.collate_fn)

    def _initialize_module(self, X):
        """Instantiates pytorch module using object (self) attributes and
        training dataset.

        Parameters
        ----------
        X : torch dataset
            Training dataset. Used as input in ``from_dataset`` factory.

        Returns
        -------
        module : torch neural net object
            Instantiated neural net
        """
        module_kwargs = self.get_kwargs_for('module')
        module = self.module.from_dataset(X, **module_kwargs)
        return module.to(self.device)
