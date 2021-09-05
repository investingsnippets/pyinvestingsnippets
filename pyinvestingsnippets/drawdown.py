import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates


class Drawdown:
    """Given a Wealth Index DataFrame, will produce usefull drawdown metrics"""

    def __init__(self, wealth_index_series: pd.Series):
        self.wealth_index_series = wealth_index_series
        peaks = self.wealth_index_series.cummax()
        self.drawdown_series = (self.wealth_index_series - peaks) / peaks
        self.drawdown_series.rename('Drawdown', inplace=True)

    def get_drawdown(self):
        """
        Returns the pandas Series with Drawdown calculated.

        Returns
        -------
        pd.Series
            The Drawdown series
        """

        return self.drawdown_series

    def get_max_drawdown(self):
        """Returns the maximum drawdown"""
        return self.drawdown_series.min()

    def compute_drawdown_lagoons_durations(self):
        """
        Returns a pd.Series where the index is the last day of the recovery of a lagoon
        and the value the total days since the previous max value for this lagoon
        """
        # find all the locations where the drawdown == 0
        zero_locations = np.unique(
            np.r_[(self.drawdown_series == 0).values.nonzero()[0], len(self.drawdown_series) - 1]
        )
        # also assign the dates so we know when things were not sinking
        zero_loc_s = pd.Series(zero_locations, index=self.drawdown_series.index[zero_locations])
        # do a shift to show what is the last and previous non zero dates
        df = zero_loc_s.to_frame('zero_loc')
        df['prev_zloc'] = zero_loc_s.shift()
        # keep only the dates where the difference is more than 1
        # that denotes the lagoons
        df = df[df['zero_loc'] - df['prev_zloc'] > 1].astype(int)
        item = self.drawdown_series.index.__getitem__
        df['Durations'] = df['zero_loc'].map(item) - df['prev_zloc'].map(item)
        df = df.reindex(self.drawdown_series.index)
        df = df.dropna()
        return df['Durations']

    def plot_drawdown(self, ax=None, **kwargs):
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

        series_to_plot = self.drawdown_series * 100
        series_to_plot.plot(ax=ax, lw=2, kind='area', color='red', alpha=0.3, **kwargs)
        ax.yaxis.grid(linestyle=':')
        ax.xaxis.grid(linestyle=':')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.xaxis.set_tick_params(reset=True)
        ax.xaxis.set_major_locator(mdates.YearLocator(1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        ax.set_title('Drawdown (%)', fontweight='bold')
        return ax
