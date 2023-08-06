"""
The :mod:`skorch_forecasting.preprocessing` module includes tools for
performing a variety of transformations (not only for time series)
to pandas DataFrames. It also includes a group wise column transformer, i.e.,
:class:`GroupWiseColumnTransformer`, that makes it possible to fit and
transform each DataFrame group individually.
"""

from ._column_selector import make_column_selector
from ._data import SlidingWindowTransformer
from ._data import UnitCircleProjector
from ._data import inverse_transform_sliding_sequences
from ._encoders import CyclicalDatesEncoder
from ._encoders import MultiColumnLabelEncoder
from ._encoders import TimeIndexEncoder
from ._pandas_column_transformer import GroupWiseColumnTransformer
from ._pandas_column_transformer import PandasColumnTransformer

__all__ = [
    'GroupWiseColumnTransformer',
    'PandasColumnTransformer',
    'SlidingWindowTransformer',
    'MultiColumnLabelEncoder',
    'CyclicalDatesEncoder',
    'TimeIndexEncoder',
    'make_column_selector',
    'inverse_transform_sliding_sequences'
]
