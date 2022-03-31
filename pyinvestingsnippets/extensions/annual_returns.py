import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor


@register_series_accessor("annual_returns")
@register_dataframe_accessor("annual_returns")
class AnnualReturns:
    """Given a pandas object of daily prices, will resampe them
    on yearly basis and get the last price of the year. Will then
    build the Arithmentic Returns and attach several properties
    """

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj.fillna(method="pad").resample("Y").last().pct_change()
        self._obj.index = self._obj.index.year

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    def __call__(self):
        return self._obj

    def __sub__(self, other):
        return self._obj - other.data

    def __getitem__(self, idx):
        return self._obj.loc[idx]

    def tail(self, number):
        return self._obj.tail(number)

    def head(self, number):
        return self._obj.head(number)

    @property
    def cwi(self):
        return self._obj.cwi

    @property
    def annualized(self):
        """Returns the annualized return."""
        comp = (1 + self._obj).prod()
        return comp ** (1 / self._obj.shape[0]) - 1

    @property
    def volatility_annualized(self):
        """Returns the annualized volatility."""
        return self._obj.std() * (1 ** 0.5)

    def var(self, percentile=5):
        """Returns the historic Value at Risk (VaR) at a specified level

        Parameters
        ----------
        percentile: percentile or sequence of percentiles to compute,
                    which must be between 0 and 100 inclusive.

        Returns
        -------
        float
        """
        return -np.percentile(self._obj[1:], percentile)

    def cvar(self, percentile=5):
        """Returns the Conditional VaR at a specified level

        Parameters
        ----------
        percentile: percentile or sequence of percentiles to compute,
                    which must be between 0 and 100 inclusive.

        Returns
        -------
        float
        """
        is_beyond = self._obj <= -self.var(percentile=percentile)
        return -self._obj[is_beyond].mean()

    def sharpe(self, risk_free_rate):
        """The Sharpe ratio is the average return earned in excess
        of the risk-free rate per unit of volatility.

        Parameters
        ----------
        risk_free_rate: The Risk Free Rate

        Returns
        -------
        float
        """
        periods = 1
        rf_per_period = (1 + risk_free_rate) ** (1 / periods) - 1
        excess_ret = self.data - rf_per_period
        comp = (1 + excess_ret).prod()
        ann_ex_ret = comp ** (periods / excess_ret.shape[0]) - 1
        ann_vol = self.data.std() * (periods ** 0.5)
        return ann_ex_ret / ann_vol

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        series_to_plot = self._obj * 100
        series_to_plot.plot(lw=2, alpha=0.7, ax=ax, kind="bar", **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        yearly_dates = [i for i in self._obj.index]
        ax.set_xticklabels(yearly_dates, fontsize="small")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.tick_params(axis='x', labelrotation=45)

        ax.set_title("Annual Returns", fontweight="bold")
        return ax
