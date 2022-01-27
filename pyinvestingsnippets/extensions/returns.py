import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


@pd.api.extensions.register_series_accessor("returns")
class Returns:
    """Given a Prices Series, will build the Arithmentic Returns and
    attach several properties
    """

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj.fillna(method="pad").pct_change().dropna()

    @staticmethod
    def _validate(obj):
        assert isinstance(obj, pd.Series)
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def wealth_index(self):
        return self._obj.wealth_index

    def wealth_index_since(self, since=None):
        return self._obj[since:].wealth_index

    def annualized(self, ppy=252):
        """Returns the annualized return based on the days provided.
        This is not a property because the incoming prices are of
        undefined periodicity.
        """
        comp_growth = (1 + self._obj).prod()
        return comp_growth ** (ppy / self._obj.shape[0]) - 1

    def volatility_annualized(self, ppy):
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
