import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

import datetime


from yahoofinancials import YahooFinancials
import pandas as pd
import matplotlib.pyplot as plt
import dateutil.parser

import pyinvestingsnippets

def retrieve_stock_data(ticker, start, end):
    json = YahooFinancials(ticker).get_historical_price_data(start, end, "daily")
    columns=["adjclose"]  # ["open","close","adjclose"]
    df = pd.DataFrame(columns=columns)
    for row in json[ticker]["prices"]:
        d = dateutil.parser.isoparse(row["formatted_date"])
        df.loc[d] = [row["adjclose"]] # [row["open"], row["close"], row["adjclose"]]
    df.index.name = "date"
    df.columns = [ticker]
    return df


end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5 * 365)
end_date_frmt = end_date.strftime("%Y-%m-%d")
start_date_frmt = start_date.strftime("%Y-%m-%d")

ASSET_1 = 'AAPL'
ASSET_2 = 'SPY'

asset1_prices = retrieve_stock_data(ASSET_1, start_date_frmt, end_date_frmt)
asset2_prices = retrieve_stock_data(ASSET_2, start_date_frmt, end_date_frmt)

# rc = {
#     'lines.linewidth': 1.0,
#     'axes.facecolor': '0.995',
#     'figure.facecolor': '0.97',
#     'font.family': 'sans-serif',
#     'font.sans-serif': 'Times New Roman',
#     'font.monospace': 'Courier',
#     'font.size': 10,
#     'axes.labelsize': 10,
#     'axes.labelweight': 'bold',
#     'axes.titlesize': 10,
#     'xtick.labelsize': 8,
#     'ytick.labelsize': 8,
#     'legend.fontsize': 10,
#     'figure.titlesize': 12
# }

# sns.set(style='whitegrid', context=rc, palette='deep')

rows = 6
cols = 6

fig = plt.figure(figsize=(14, 16), constrained_layout=True)
fig.suptitle("Report", weight='bold')
gs = gridspec.GridSpec(rows, cols, figure=fig)

ax_equity = plt.subplot(gs[0, :])
ax_drawdown = plt.subplot(gs[1, :])
ax_rolling_sharpe = plt.subplot(gs[2, :])
ax_monthly_returns = plt.subplot(gs[3, :3])
ax_yearly_returns = plt.subplot(gs[3, 3:])
ax_rolling_returns = plt.subplot(gs[4, :2])
ax_rolling_vol = plt.subplot(gs[4, 2:4])
ax_downside_risk = plt.subplot(gs[4, 4:])
ax_stats = plt.subplot(gs[5, :2])
ax_beta = plt.subplot(gs[5, 2:4])

asset1_rets = asset1_prices[ASSET_1].prices.returns
asset2_rets = asset2_prices[ASSET_2].prices.returns

asset1_wi = asset1_rets.wealth_index
asset1_dd = asset1_wi.drawdown
asset1_dd_dur = asset1_dd.durations

asset2_wi = asset2_rets.wealth_index
asset2_dd = asset2_wi.drawdown
asset2_dd_dur = asset2_dd.durations

asset1_wi.plot(ax=ax_equity, color='green', label=ASSET_1)
asset2_wi.plot(ax=ax_equity, color='grey', label=ASSET_2)

asset1_dd.plot(ax=ax_drawdown, color='green')
asset2_dd.plot(ax=ax_drawdown, color='grey')

asset1_wi.monthly_returns.plot(ax=ax_monthly_returns, color='green')
asset1_wi.annual_returns.plot(ax=ax_yearly_returns, color='green')

rolling_rets = pyinvestingsnippets.RollingReturns(asset1_rets.data, rolling_window=252)

# 3 month rolling annualized vol
rolling_vol = pyinvestingsnippets.RollingVolatility(asset1_rets.data, rolling_window=90, window=252)

# get the monthly rolling beta
# rolling_beta = pyinvestingsnippets.RollingBetaRegression(asset2_rets.data, asset1_rets.data, 30)
# rolling_beta.plot(ax=ax_beta, color='red', label='regr')
rolling_beta = pyinvestingsnippets.RollingBetaCovariance(asset2_rets.data, asset1_rets.data, 30)
rolling_beta.plot(ax=ax_beta, color='green', label='cov')

# get the total beta
beta = pyinvestingsnippets.BetaCovariance(asset2_wi.monthly_returns.data, asset1_wi.monthly_returns.data)

rolling_rets.plot(ax=ax_rolling_returns)
rolling_vol.plot(ax=ax_rolling_vol)

downside_risk = pyinvestingsnippets.DownsideRisk(asset1_rets.data)
downside_risk.plot(ax=ax_downside_risk)

def _plot_stats(ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    data = [
        ['Total Return', '{:.0%}'.format(asset1_wi.total_return), '{:.0%}'.format(asset2_wi.total_return)],
        ['CAGR', '{:.2%}'.format(asset1_wi.cagr), '{:.2%}'.format(asset2_wi.cagr)],
        ['Max Drawdown', '{:.2%}'.format(asset1_dd.max_drawdown), '{:.2%}'.format(asset2_dd.max_drawdown)],
        ['Avg Drawdown Duration', asset1_dd_dur.mean(), asset2_dd_dur.mean()],
        ['Max Drawdown Duration', asset1_dd_dur.max(), asset2_dd_dur.max()],
        ['SRRI', '{}/7 ({:.2%})'.format(asset1_prices[ASSET_1].prices.monthly_returns.srri.risk_class,
                    asset1_prices[ASSET_1].prices.monthly_returns.srri.value),
                '{}/7 ({:.2%})'.format(asset2_prices[ASSET_2].prices.monthly_returns.srri.risk_class,
                    asset2_prices[ASSET_2].prices.monthly_returns.srri.value)],
        ['Beta', '{:.2}'.format(beta.beta), '1']
    ]
    column_labels=["Metric", f"{ASSET_1}", f"{ASSET_2}"]
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=data, colLabels=column_labels, loc="center", edges='open')

    ax.grid(False)
    ax.spines['top'].set_linewidth(2.0)
    ax.spines['bottom'].set_linewidth(2.0)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel('')
    ax.set_xlabel('')

    ax.axis([0, 10, 0, 10])

    return ax

_plot_stats(ax=ax_stats)

plt.show()