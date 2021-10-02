import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates


class RollingVolatility:
    """Given a Returns Series, will build the rolling volatility.

    Depending on the input Returns Series:
    - Daily, Weekly, Monthly

    rolling_window: The periods to roll. If for example we have daily returns
    and we would like monthly rolling then it will be 30. If weekly returns and
    we still want monthly rolling then it will be 4. If we want 3 months rolling
    then it will be 4 * 3 = 12.

    window: will be used in square root. If daily returns and we want
    annualized volatility then window = 252, if we have weekly returns
    and want annualized vol then window = 52.
    if monthly returns then window = 12 for annualization
    """

    def __init__(self, pandas_obj, rolling_window, window=252):
        self._validate(pandas_obj)
        self.window = window
        self._obj = (
            pandas_obj.fillna(method="pad")
            .rolling(window=rolling_window)
            .std()
            .apply(lambda x: x * window ** 0.5)
        )

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        to_plot = self._obj * 100
        to_plot.plot(lw=2, x_compat=False, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha="center")

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.xaxis.set_tick_params(reset=True)
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

        ax.set_title(f"Rolling Volatility - {self.window}", fontweight="bold")
        return ax
