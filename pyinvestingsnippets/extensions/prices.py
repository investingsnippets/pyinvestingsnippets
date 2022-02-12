import pandas as pd
import matplotlib.pyplot as plt
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor


@register_series_accessor("prices")
@register_dataframe_accessor("prices")
class Prices:
    """Given a pandas object, will attach useful attributes"""

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    def __call__(self):
        return self._obj

    def __getitem__(self, idx):
        return self._obj.loc[idx]

    @property
    def cumulative_return(self):
        """Returns the cumulative return on an investment.
        It is the aggregate amount that the investment has gained
        or lost over time, independent of the amount of time involved."""
        return (self._obj.iloc[-1] - self._obj.iloc[0]) / self._obj.iloc[0]

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        self._obj.plot(lw=2, alpha=0.7, x_compat=True, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.axhline(1.0, linestyle="--", color="black", lw=1)
        ax.tick_params(axis='x', labelrotation=45)
        ax.set_ylabel("Price")
        ax.set_xlabel("Date")
        return ax
