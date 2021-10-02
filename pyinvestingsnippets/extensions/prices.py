import pandas as pd
import matplotlib.pyplot as plt


@pd.api.extensions.register_series_accessor("prices")
class Prices:
    """Given a Prices Series, will attach useful attributes"""

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        assert isinstance(obj, pd.Series)
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def returns(self):
        return self._obj.returns

    @property
    def weekly_returns(self):
        return self._obj.weekly_returns

    @property
    def monthly_returns(self):
        return self._obj.monthly_returns

    @property
    def annual_returns(self):
        return self._obj.annual_returns

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        self._obj.plot(lw=2, alpha=0.7, x_compat=False, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha="center")

        ax.axhline(1.0, linestyle="--", color="black", lw=1)
        ax.set_ylabel("Price")
        ax.set_xlabel("Date")
        return ax
