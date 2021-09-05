import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.ticker as mtick


@pd.api.extensions.register_series_accessor("WealthIndex")
class WealthIndex:
    """Given a Returns Series, will produce the Wealth Index on 1 unit, and other helper stats"""

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = ((pandas_obj + 1).cumprod()) * 1
        self._obj.rename('WealthIndex', inplace=True)

    @staticmethod
    def _validate(obj):
        assert pd.isnull(obj[0])
        assert isinstance(obj.index, pd.DatetimeIndex)

    @property
    def wealth_index(self):
        return self._obj

    @property
    def total_return(self):
        """Returns the total return"""
        return self._obj.iloc[-1]

    @property
    def cagr(self):
        """
        Returns compound_annual_growth_rate
        """
        no_of_years = len(np.unique(self._obj.index.year))
        return (self._obj.iloc[-1] ** (1 / no_of_years)) - 1

    @property
    def monthly_rets(self):
        return self._obj.resample('BM').apply(lambda x: x[-1]).pct_change()

    @property
    def positive_monthly_returns_percentage(self):
        return round(
            self.monthly_rets[self.monthly_rets > 0].shape[0] / self.monthly_rets.shape[0] * 100, 2
        )

    @property
    def get_annual_returns(self):
        return self._obj.resample('Y').apply(lambda x: x[-1]).pct_change()

    def plot(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()

        self._obj.plot(lw=2, color='green', alpha=0.7, x_compat=False, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=':')
        ax.xaxis.grid(linestyle=':')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')

        ax.axhline(1.0, linestyle='--', color='black', lw=1)
        ax.set_ylabel('Wealth Index')
        return ax

    # def plot_yearly_returns(self, ax=None, **kwargs):
    #     if ax is None:
    #         ax = plt.gca()

    #     self.get_annual_returns().plot(ax=ax, kind="bar")
    #     ax.yaxis.grid(linestyle=':')
    #     ax.xaxis.grid(linestyle=':')
    #     ax.set_ylabel('')
    #     ax.set_xlabel('')
    #     ax.xaxis.grid(False)
    #     plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')

    #     ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    #     yearly_dates = [i for i in self.get_annual_returns().index.strftime('%Y')]
    #     ax.set_xticklabels(yearly_dates, fontsize='small')
    #     ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    #     ax.set_title('Yearly Returns (%)', fontweight='bold')
    #     return ax

    # def plot_monthly_returns(self, ax=None, **kwargs):
    #     if ax is None:
    #         ax = plt.gca()

    #     self.get_monthly_returns().plot(ax=ax, kind="bar")
    #     ax.yaxis.grid(linestyle=':')
    #     ax.xaxis.grid(linestyle=':')
    #     ax.set_ylabel('')
    #     ax.set_xlabel('')
    #     ax.xaxis.grid(False)
    #     plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')

    #     ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    #     monthly_dates = [i for i in self.get_monthly_returns().index.strftime('%Y-%m')]
    #     ax.set_xticklabels(monthly_dates, fontsize='small')
    #     ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    #     ax.set_title('Monthly Returns (%)', fontweight='bold')
    #     return ax
