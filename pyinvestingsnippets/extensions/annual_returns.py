import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


@pd.api.extensions.register_series_accessor("annual_returns")
class AnnualReturns:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj.fillna(method="pad").resample("Y").last().pct_change()
        self._obj.index = self._obj.index.year

    @staticmethod
    def _validate(obj):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self):
        return self._obj

    @property
    def annualized(self):
        """Returns the annualized return."""
        comp_growth = (1 + self._obj).prod()
        return comp_growth ** (1 / self._obj.shape[0]) - 1

    @property
    def volatility_annualized(self):
        """Returns the annualized volatility."""
        return self._obj.std() * (1 ** 0.5)

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        series_to_plot = self._obj * 100
        series_to_plot.plot(lw=2, alpha=0.7, ax=ax, kind="bar", **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        yearly_dates = [i for i in self._obj.index]
        ax.set_xticklabels(yearly_dates, fontsize="small")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.tick_params(axis='x', labelrotation=45)

        ax.set_title("Annual Returns", fontweight="bold")
        return ax
