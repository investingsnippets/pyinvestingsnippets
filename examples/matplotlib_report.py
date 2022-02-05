import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import datetime

import pandas_datareader as web

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import pyinvestingsnippets 

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5 * 365)
end_date_frmt = end_date.strftime("%Y-%m-%d")
start_date_frmt = start_date.strftime("%Y-%m-%d")

ASSET_1 = 'MSFT'
ASSET_2 = 'SPY'

asset1_prices = web.DataReader(ASSET_1, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
asset2_prices = web.DataReader(ASSET_2, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']

rows = 6
cols = 6

fig = plt.figure(figsize=(14, 16), constrained_layout=True)
fig.suptitle("Report", weight='bold')
gs = gridspec.GridSpec(rows, cols, figure=fig)

ax_equity = plt.subplot(gs[0, :])
ax_drawdown = plt.subplot(gs[1, :])
ax_monthly_returns = plt.subplot(gs[2, :3])
ax_yearly_returns = plt.subplot(gs[2, 3:])
ax_rolling_returns = plt.subplot(gs[3, :2])
ax_rolling_vol = plt.subplot(gs[3, 2:4])
ax_downside_risk = plt.subplot(gs[3, 4:])
ax_stats = plt.subplot(gs[4, :3])
ax_beta = plt.subplot(gs[4, 3:])

asset1_rets = asset1_prices.returns
asset2_rets = asset2_prices.returns

asset1_wi = asset1_rets.wealth_index
asset1_dd = asset1_wi.drawdown
asset1_dd_dur = asset1_dd.durations

asset2_wi = asset2_rets.wealth_index
asset2_dd = asset2_wi.drawdown
asset2_dd_dur = asset2_dd.durations

asset1_wi.plot(ax=ax_equity, color='blue', label=ASSET_1)
asset2_wi.plot(ax=ax_equity, color='grey', label=ASSET_2)

asset1_dd.plot(ax=ax_drawdown, color='blue')
asset2_dd.plot(ax=ax_drawdown, color='grey')

asset1_wi.monthly_returns.plot(ax=ax_monthly_returns, color='blue')
asset1_wi.annual_returns.plot(ax=ax_yearly_returns, color='blue')

rolling_rets = pyinvestingsnippets.RollingReturns(asset1_rets.data, rolling_window=252)

# 3 month rolling annualized vol
rolling_vol = pyinvestingsnippets.RollingVolatility(asset1_rets.data, rolling_window=90, window=252)

# get the monthly rolling beta
# rolling_beta = pyinvestingsnippets.RollingBetaRegression(asset2_rets.data, asset1_rets.data, 30)
# rolling_beta.plot(ax=ax_beta, color='red', label='regr')
rolling_beta = pyinvestingsnippets.RollingBetaCovariance(asset2_rets.data, asset1_rets.data, 30)
rolling_beta.plot(ax=ax_beta, color='blue', label='cov')

# get the total beta
beta = pyinvestingsnippets.BetaCovariance(asset2_wi.monthly_returns.data, asset1_wi.monthly_returns.data)

rolling_rets.plot(ax=ax_rolling_returns, color='blue')
rolling_vol.plot(ax=ax_rolling_vol, color='blue')

downside_risk = pyinvestingsnippets.ExponantiallyWeightedDownsideRisk(asset1_rets.data)
downside_risk.plot(ax=ax_downside_risk, color='blue')

def _plot_stats(ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    data = [
        ['Total Return', '{:.0%}'.format(asset1_wi.total_return), '{:.0%}'.format(asset2_wi.total_return)],
        ['CAGR', '{:.2%}'.format(asset1_wi.cagr), '{:.2%}'.format(asset2_wi.cagr)],
        ['Max Drawdown', '{:.2%}'.format(asset1_dd.max_drawdown), '{:.2%}'.format(asset2_dd.max_drawdown)],
        ['Avg Drawdown Duration', asset1_dd_dur.mean(), asset2_dd_dur.mean()],
        ['Max Drawdown Duration', asset1_dd_dur.max(), asset2_dd_dur.max()],
        ['SRRI', '{}/7 ({:.2%})'.format(asset1_prices.monthly_returns.srri.risk_class,
                    asset1_prices.monthly_returns.srri.value),
                '{}/7 ({:.2%})'.format(asset2_prices.monthly_returns.srri.risk_class,
                    asset2_prices.monthly_returns.srri.value)],
        ['Beta', '{:.2}'.format(beta.beta), '1']
    ]
    column_labels=["Metric", f"{ASSET_1}", f"{ASSET_2}"]
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=column_labels, loc="center", edges='open')
    table.set_fontsize(10)
    table.scale(1.5, 1.5)

    ax.grid(False)
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel("Stats")
    ax.set_xlabel('')

    ax.axis([0, 10, 0, 10])

    return ax

_plot_stats(ax=ax_stats)

plt.show()