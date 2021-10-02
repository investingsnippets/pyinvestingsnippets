import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@pd.api.extensions.register_series_accessor("returns")
class Returns:
    """Given a Prices Series, will build the arithmetic returns and
    attach several properties
    """

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj.fillna(method="pad").pct_change()

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def wealth_index(self):
        return self._obj.wealth_index

    def wealth_index_since(self, since=None):
        return self._obj[since:].wealth_index

    @property
    def rolling_returns(self):
        return self._obj.rolling_returns

    @property
    def rolling_volatility(self):
        return self._obj.rolling_volatility

    def plot(self):  # pragma: no cover
        gridkw = dict(height_ratios=[5, 1])
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw=gridkw)
        fig.suptitle("Returns", weight="bold")
        sns.histplot(data=self._obj, ax=ax1)  # array, top subplot
        sns.boxplot(data=self._obj, ax=ax2, width=0.4)  # bottom subplot
        return fig
