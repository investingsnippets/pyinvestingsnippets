import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.express as px


class RollingReturns:
    """Given a Returns Series, will build the rolling returns using window"""

    def __init__(self, pandas_obj, rolling_window: int = 252):
        self._validate(pandas_obj, rolling_window)
        self.window = rolling_window
        self._obj = (1 + pandas_obj).rolling(window=rolling_window).apply(
            np.prod, raw=True
        ) - 1

    @staticmethod
    def _validate(obj, rolling_window: int):
        assert isinstance(obj.index, pd.DatetimeIndex)
        assert rolling_window > 0 and isinstance(
            rolling_window, int
        ), "rolling_window must be possitive integer"

    @property
    def data(self):
        return self._obj

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        to_plot = self._obj * 100
        to_plot.plot(lw=2, x_compat=True, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.xaxis.set_tick_params(reset=True)
        ax.tick_params(axis='x', labelrotation=45)

        # ax.axhline(
        #     y=(to_plot.mean()),
        #     color="red",
        #     ls="--",
        #     lw=0.5,
        #     label=f"Avg ({to_plot.mean():0.2f}%)",
        # )
        # ax.axhline(y=0, color="black", lw=0.5)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.set_title(f"Rolling Returns - {self.window}", fontweight="bold")
        return ax

    def plotly(self, **kwargs):  # pragma: no cover
        return px.line(self._obj, **kwargs)
