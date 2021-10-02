import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@pd.api.extensions.register_series_accessor("wealth_index")
class WealthIndex:
    """Given a Returns Series, will produce the Wealth Index
    on 1 unit, and other helper stats
    """

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = ((pandas_obj + 1).cumprod()) * 1
        self._obj.iloc[0] = 1

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def drawdown(self):
        return self._obj.drawdown

    @property
    def total_return(self):
        """Returns the total return"""
        return self._obj.iloc[-1] - 1

    @property
    def cagr(self):
        """Returns compound_annual_growth_rate"""
        no_of_years = len(np.unique(self._obj.index.year))
        return (self._obj.iloc[-1] ** (1 / no_of_years)) - 1

    @property
    def monthly_returns(self):
        return self._obj.monthly_returns

    @property
    def weekly_returns(self):
        return self._obj.weekly_returns

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
        ax.legend(loc="best")

        ax.axhline(1.0, linestyle="--", color="black", lw=1)
        ax.set_ylabel("Wealth Index")
        return ax
