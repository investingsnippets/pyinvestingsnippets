import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


@pd.api.extensions.register_series_accessor("monthly_returns")
class MonthlyReturns:
    """Given Prices it calculates the arithmentic Returns"""

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj.fillna(method="pad").resample("M").last().pct_change()

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def srri(self):
        return self._obj.srri

    @property
    def positive_monthly_returns_percentage(self):
        return round(self._obj[self._obj > 0].shape[0] / self._obj.shape[0] * 100, 2)

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        series_to_plot = self._obj * 100
        series_to_plot.plot(ax=ax, kind="bar", **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha="center")

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        monthly_dates = [i for i in self._obj.index.strftime("%Y-%m")]
        ax.set_xticklabels(monthly_dates, fontsize="small")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        ax.set_title("Monthly Returns", fontweight="bold")
        return ax
