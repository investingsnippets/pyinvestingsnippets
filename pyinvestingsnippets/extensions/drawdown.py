import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates


@pd.api.extensions.register_series_accessor("drawdown")
class Drawdown:
    """Given a Wealth Index DataFrame, will produce usefull drawdown metrics"""

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        peaks = pandas_obj.cummax()
        self._obj = (pandas_obj - peaks) / peaks
        self._obj.rename("Drawdown", inplace=True)

    @staticmethod
    def _validate(obj):
        assert not pd.isnull(obj[0])
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        """
        Returns the pandas Series with Drawdown calculated.

        Returns
        -------
        pd.Series
            The Drawdown series
        """

        return self._obj

    @property
    def max_drawdown(self):
        """Returns the maximum drawdown"""
        return self._obj.min()

    @property
    def durations(self):
        """
        Returns a pd.Series where the index is the last day of the recovery of a lagoon
        and the value the total days since the previous max value for this lagoon
        """
        # find all the locations where the drawdown == 0
        zero_locations = np.unique(
            np.r_[(self._obj == 0).values.nonzero()[0], len(self._obj) - 1]
        )
        # also assign the dates so we know when things were not sinking
        zero_loc_s = pd.Series(zero_locations, index=self._obj.index[zero_locations])
        # do a shift to show what is the last and previous non zero dates
        df = zero_loc_s.to_frame("zero_loc")
        df["prev_zloc"] = zero_loc_s.shift()
        # keep only the dates where the difference is more than 1
        # that denotes the lagoons
        df = df[df["zero_loc"] - df["prev_zloc"] > 1].astype(int)
        item = self._obj.index.__getitem__
        df["Durations"] = df["zero_loc"].map(item) - df["prev_zloc"].map(item)
        df = df.reindex(self._obj.index)
        df = df.dropna()
        return df["Durations"]

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        """
        Plots the Drawdown

        Parameters
        ----------
        ax : matlibplot axis
        kwargs : Arguments to pass to the plot

        Returns
        -------
        matlibplot axis
        """
        if ax is None:
            ax = plt.gca()

        series_to_plot = self._obj * 100
        if "color" not in kwargs:
            kwargs["color"] = "red"
        series_to_plot.plot(ax=ax, lw=2, kind="area", alpha=0.3, **kwargs)
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

        ax.set_title("Drawdown", fontweight="bold")
        return ax
