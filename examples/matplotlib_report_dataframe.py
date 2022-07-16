import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import datetime

import pandas_datareader as web

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import pyinvestingsnippets 

from utils import gbm

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5 * 365)
end_date_frmt = end_date.strftime("%Y-%m-%d")
start_date_frmt = start_date.strftime("%Y-%m-%d")

ROLLING_WINDOW = 90  # days

# asset_prices = web.DataReader(['MSFT', 'SPY'], data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
asset_prices = gbm(10, 2, steps_per_year=252)

FIG_ROWS = 6
FIG_COLS = 6

fig = plt.figure(figsize=(14, 16), constrained_layout=True)
fig.suptitle("Report", weight='bold')
gs = gridspec.GridSpec(FIG_ROWS, FIG_COLS, figure=fig)

ax_prices = plt.subplot(gs[0, :])
ax_equity = plt.subplot(gs[1, :])
ax_drawdown = plt.subplot(gs[2, :])
ax_monthly_returns = plt.subplot(gs[3, :3])
ax_yearly_returns = plt.subplot(gs[3, 3:])
ax_rolling_returns = plt.subplot(gs[4, :2])
ax_rolling_vol = plt.subplot(gs[4, 2:4])
ax_downside_risk = plt.subplot(gs[4, 4:])
ax_stats = plt.subplot(gs[5, :3])
ax_beta = plt.subplot(gs[5, 3:])

prices = asset_prices.prices
prices.plot(ax=ax_prices)

wi = asset_prices.returns.cwi
wi.plot(ax=ax_equity)
wi.monthly_returns.plot(ax=ax_monthly_returns)
wi.annual_returns.plot(ax=ax_yearly_returns)

dd = wi.drawdown
dd.plot(ax=ax_drawdown)

returns = asset_prices.returns
rolling_rets = pyinvestingsnippets.RollingReturns(returns.data, rolling_window=ROLLING_WINDOW)
rolling_rets.plot(ax=ax_rolling_returns)

rolling_vol = pyinvestingsnippets.RollingVolatility(returns.data, rolling_window=ROLLING_WINDOW, window=252)
rolling_vol.plot(ax=ax_rolling_vol)

downside_risk = pyinvestingsnippets.ExponantiallyWeightedDownsideRisk(returns.data)
downside_risk.plot(ax=ax_downside_risk)

# we need two to dance here
rolling_beta = pyinvestingsnippets.RollingBetaCovariance(returns.data.iloc[:, 0], 
                            returns.data.iloc[:, -1], ROLLING_WINDOW)
rolling_beta.plot(ax=ax_beta, color='magenta', label='Cov')

def _plot_stats(ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    data = [
        ['Total Return'] + [f'{i:.0%}' for i in wi.total_return.values],
        ['CAGR'] + [f'{i:.2%}' for i in wi.annualized(252)],
        ['Max Drawdown'] + [f'{i:.2%}' for i in dd.max_drawdown],
        ['Avg Drawdown Duration'] + [f'{dd.data.iloc[:, i].drawdown_durations.mean}' for i in range(dd.data.shape[1])],
        ['Max Drawdown Duration'] + [f'{dd.data.iloc[:, i].drawdown_durations.max}' for i in range(dd.data.shape[1])],
        ['Beta'] + [f'{pyinvestingsnippets.BetaCovariance(returns.data.iloc[:, i], returns.data.iloc[:, -1]).beta:.2f}' for i in range(returns().shape[1])],
    ]

    monthly_returns = asset_prices.fillna(method="pad").resample('M').last().pct_change()
    if monthly_returns.shape[0] >= 60:
        data.append(['SRRI'] + [f'{monthly_returns.iloc[-60:, i].srri.risk_class}/7 ({monthly_returns.iloc[-60:, i].srri.value:.2%})' for i in range(dd.data.shape[1])])
    
    column_labels=["Metric"] + [f'{i}' for i in asset_prices.columns.values]
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=column_labels, loc="center", edges='open', **kwargs)
    # table.set_fontsize(10)
    # table.scale(1.5, 1.5)

    ax.grid(False)
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel("Stats")
    ax.set_xlabel('')

    ax.axis([0, 10, 0, 10])

    return ax

_plot_stats(ax=ax_stats)

plt.show()