import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor


@register_series_accessor("returns")
@register_dataframe_accessor("returns")
class Returns:
    """Given a pandas object, will build the Arithmentic Returns and
    attach several properties
    """

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj.fillna(method="pad").pct_change()[1:]

    @staticmethod
    def _validate(obj):
        # assert isinstance(obj, pd.Series)
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
    def total(self):
        """Returns the total return on an investment.
        It is the aggregate amount that the investment has gained
        or lost over time, independent of the amount of time involved.

        This is the same as self._obj.cwi.total_return
        """
        return (1 + self._obj).prod() - 1

    @property
    def average(self):
        """Returns the Average Return over a period. This is the
        Geometric Mean
        """
        comp = (1 + self._obj).prod()
        return comp ** (1 / self._obj.shape[0]) - 1

    def cwi_since(self, since=None):
        return self._obj[since:].cwi

    def annualized(self, ppy=252):
        """Returns the annualized return (Compound Annual Growth Rate)
        based on the days provided. This is not a property
        because the incoming prices are of undefined periodicity.
        """
        comp = (1 + self._obj).prod()
        return comp ** (ppy / self._obj.shape[0]) - 1

    def volatility_annualized(self, ppy=252):
        """Returns the annualized volatility based on the days provided.
        This is not a property because the incoming prices are of
        undefined periodicity.
        """
        return self._obj.std() * (ppy ** 0.5)

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
        return -np.percentile(self._obj, percentile)

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

    def sharpe(self, risk_free_rate, periods=252):
        """The Sharpe ratio is the average return earned in excess
        of the risk-free rate per unit of volatility.

        Parameters
        ----------
        risk_free_rate: The Risk Free Rate

        Returns
        -------
        float
        """
        rf_per_period = (1 + risk_free_rate) ** (1 / periods) - 1
        excess_ret = self.data - rf_per_period
        comp = (1 + excess_ret).prod()
        ann_ex_ret = comp ** (periods / excess_ret.shape[0]) - 1
        ann_vol = self.data.std() * (periods ** 0.5)
        return ann_ex_ret / ann_vol

    @property
    def srri(self):
        return self._obj.srri

    def plot(self, ax=None):  # pragma: no cover
        if ax is None:
            fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw=dict(height_ratios=[5, 1]))
            fig.suptitle("Returns", weight="bold")
            sns.histplot(data=self._obj, ax=ax1)
            sns.boxplot(data=self._obj, ax=ax2, width=0.4)
            return fig
        return sns.histplot(data=self._obj, ax=ax)
