import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.express as px
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor


@register_series_accessor("drawdown")
@register_dataframe_accessor("drawdown")
class Drawdown:
    """Given a Wealth Index pandas object,
    will produce usefull drawdown metrics"""

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        peaks = pandas_obj.cummax()
        self._obj = (pandas_obj - peaks) / peaks

    @staticmethod
    def _validate(obj):
        # assert not pd.isnull(obj[0])
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    def __call__(self):
        return self._obj

    def __getitem__(self, idx):
        return self._obj.loc[idx]

    @property
    def max_drawdown(self):
        """Returns the maximum drawdown"""
        return self._obj.min(axis=0)

    @property
    def durations(self):
        """Returns the drawdown_durations ONLY if Series"""
        assert isinstance(
            self._obj, pd.Series
        ), "Drawdown must be a Series to use this property"
        return self._obj.drawdown_durations

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
        series_to_plot.plot(ax=ax, lw=2, kind="area", alpha=0.3, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.xaxis.set_tick_params(reset=True)
        ax.tick_params(axis='x', labelrotation=45)

        ax.set_title("Drawdown", fontweight="bold")
        return ax

    def plotly(self, **kwargs):  # pragma: no cover
        fig = px.line(self._obj, **kwargs)
        fig.layout.yaxis.tickformat = '.1%'
        fig.update_layout(
            title="Drawdown",
            legend_title="Symbol",
        )
        return fig
