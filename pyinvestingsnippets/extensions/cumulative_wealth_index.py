import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from pandas.api.extensions import register_series_accessor, register_dataframe_accessor


@register_series_accessor("wealth_index")
@register_dataframe_accessor("wealth_index")
class CumulativeWealthIndex:
    """Given Arithmetic Returns Series, will produce the
    Cumulative Wealth Index on 1$.
    """

    def __init__(self, pandas_obj: pd.Series):
        self._validate(pandas_obj)
        self._obj = ((pandas_obj + 1).cumprod()) * 1
        self._obj.iloc[0] = 1

    @staticmethod
    def _validate(obj: pd.Series):
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def data(self) -> pd.Series:
        return self._obj

    def __call__(self):
        return self._obj

    def __getitem__(self, idx):
        return self._obj.loc[idx]

    @property
    def drawdown(self):
        return self._obj.drawdown

    @property
    def total_return(self):
        """Returns the total return"""
        return self._obj.iloc[-1] - 1

    @property
    def cagr(self):
        """Returns compound_annual_growth_rate"""
        no_of_years = len(np.unique(self._obj.index.year))
        return (self._obj.iloc[-1] ** (1 / no_of_years)) - 1

    @property
    def monthly_returns(self):
        return self._obj.monthly_returns

    @property
    def weekly_returns(self):
        return self._obj.weekly_returns

    @property
    def annual_returns(self):
        return self._obj.annual_returns

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        if ax is None:
            ax = plt.gca()

        self._obj.plot(lw=2, alpha=0.7, x_compat=True, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=":")
        ax.xaxis.grid(linestyle=":")
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.xaxis.grid(False)
        if 'label' in kwargs:
            ax.legend(loc="best")

        ax.axhline(1.0, linestyle="--", color="black", lw=1)
        ax.set_ylabel("Wealth Index")
        return ax

    def plotly(self, **kwargs):  # pragma: no cover
        fig = px.line(self._obj, **kwargs)
        fig.update_layout(
            title="Performance on 1$",
            legend_title="Symbol",
        )
        return fig
