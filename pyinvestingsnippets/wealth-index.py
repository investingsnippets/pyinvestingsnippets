import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


class WealthIndex:
    """Given a Returns Series, will produce the Wealth Index on 1 unit, and other helper stats"""

    def __init__(self, returns_series: pd.Series):
        assert not returns_series.isnull().values.any()
        self.returns_series = returns_series
        self.wealth_index = ((returns_series + 1).cumprod()) * 1
        self.wealth_index.rename('WealthIndex', inplace=True)

    def get_wealth_index(self):
        """
        Returns the pandas Series with Wealth Index calculated.

        Returns
        -------
        pd.Series
            The Wealth Index series
        """

        return self.wealth_index

    def get_total_return(self):
        """Returns the total return"""
        if self.total_return:
            return self.total_return

        self.total_return = (self.wealth_index[-1] - self.wealth_index[1]) / self.wealth_index[1]
        return self.total_return

    def get_compound_annual_growth_rate(self):
        """
        Returns compound_annual_growth_rate
        """
        if self.cagr:
            return self.cagr

        no_of_years = len(np.unique(self.wealth_index.index.year))
        self.cagr = ((self.wealth_index[-1] - self.wealth_index[1]) ** (1 / no_of_years)) - 1
        return self.cagr

    def get_monthly_returns(self):
        if self.monthly_returns:
            return self.get_monthly_returns

        self.monthly_returns = self.wealth_index.resample('BM').apply(lambda x: x[-1]).pct_change()
        return self.monthly_returns

    def return_positive_monthly_returns_percentage(self):
        if self.positive_monthly_pct:
            return self.positive_monthly_pct

        monthly_rets = self.get_monthly_returns()
        self.positive_monthly_pct = round(
            monthly_rets[monthly_rets > 0].shape[0] / monthly_rets.shape[0] * 100, 2
        )
        return self.positive_monthly_pct

    def get_annual_returns(self):
        if self.annual_returns:
            return self.annual_returns

        self.annual_returns = self.wealth_index.resample('Y').apply(lambda x: x[-1]).pct_change()
        return self.annual_returns

    def plot_wealth_index(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()

        self.wealth_index.plot(lw=2, color='green', alpha=0.7, x_compat=False, ax=ax, **kwargs)
        ax.yaxis.grid(linestyle=':')
        ax.xaxis.grid(linestyle=':')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')

        ax.axhline(1.0, linestyle='--', color='black', lw=1)
        ax.set_ylabel('Wealth Index')
        return ax

    def plot_yearly_returns(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()

        self.get_annual_returns().plot(ax=ax, kind="bar")
        ax.yaxis.grid(linestyle=':')
        ax.xaxis.grid(linestyle=':')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        yearly_dates = [i for i in self.get_annual_returns().index.strftime('%Y')]
        ax.set_xticklabels(yearly_dates, fontsize='small')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        ax.set_title('Yearly Returns (%)', fontweight='bold')
        return ax

    def plot_monthly_returns(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()

        self.get_monthly_returns().plot(ax=ax, kind="bar")
        ax.yaxis.grid(linestyle=':')
        ax.xaxis.grid(linestyle=':')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.xaxis.grid(False)
        plt.setp(ax.get_xticklabels(), visible=True, rotation=0, ha='center')

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        monthly_dates = [i for i in self.get_monthly_returns().index.strftime('%Y-%m')]
        ax.set_xticklabels(monthly_dates, fontsize='small')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        ax.set_title('Monthly Returns (%)', fontweight='bold')
        return ax
