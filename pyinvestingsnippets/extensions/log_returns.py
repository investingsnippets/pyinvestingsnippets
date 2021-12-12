import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


@pd.api.extensions.register_series_accessor("log_returns")
class Returns:
    """Given a Prices Series, will build the logarithmic returns and
    attach several properties
    """

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = np.log(pandas_obj.fillna(method="pad")).diff()

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def srri(self):
        return self._obj.srri

    def plot(self):  # pragma: no cover
        gridkw = dict(height_ratios=[5, 1])
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw=gridkw)
        fig.suptitle("Log Returns", weight="bold")
        sns.histplot(data=self._obj, ax=ax1)  # array, top subplot
        sns.boxplot(data=self._obj, ax=ax2, width=0.4)  # bottom subplot
        return fig
