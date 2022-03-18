import pandas as pd
import numpy as np
from pandas.api.extensions import register_series_accessor


@register_series_accessor("drawdown_durations")
class DrawdownDurations:
    """Given a Drawdown pandas Series,
    calculates the durations of the different drawdowns
    and attaches properties"""

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        # find all the locations where the drawdown == 0
        zero_locations = np.unique(
            np.r_[(pandas_obj == 0).values.nonzero()[0], len(pandas_obj) - 1]
        )
        # also assign the dates so we know when things were not sinking
        zero_loc_s = pd.Series(zero_locations, index=pandas_obj.index[zero_locations])
        # do a shift to show what is the last and previous non zero dates
        df = zero_loc_s.to_frame("zero_loc")
        df["prev_zloc"] = zero_loc_s.shift()
        # keep only the dates where the difference is more than 1
        # that denotes the lagoons
        df = df[df["zero_loc"] - df["prev_zloc"] > 1].astype(int)
        item = pandas_obj.index.__getitem__
        df["Durations"] = df["zero_loc"].map(item) - df["prev_zloc"].map(item)
        df = df.reindex(pandas_obj.index)
        df = df.dropna()
        self._obj = df["Durations"]

    @staticmethod
    def _validate(obj):
        assert isinstance(obj, pd.Series)
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    def __getitem__(self, idx):
        return self._obj.loc[idx]

    @property
    def mean(self) -> pd.Timedelta:
        return self._obj.mean() if self._obj.shape[0] > 0 else pd.Timedelta("0 days")

    @property
    def max(self) -> pd.Timedelta:
        return self._obj.max() if self._obj.shape[0] > 0 else pd.Timedelta("0 days")
