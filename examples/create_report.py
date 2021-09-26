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

apple_stock_prices = retrieve_stock_data("AAPL", start_date_frmt, end_date_frmt)
msft_stock_prices = retrieve_stock_data("MSFT", start_date_frmt, end_date_frmt)
spy_index_prices = retrieve_stock_data("SPY", start_date_frmt, end_date_frmt)

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


aapl_rets = apple_stock_prices['AAPL'].prices.returns
msft_rets = msft_stock_prices['MSFT'].prices.returns
spy_rets = spy_index_prices['SPY'].prices.returns

aapl_wi = aapl_rets.wealth_index
aapl_dd = aapl_wi.drawdown
aapl_dd_dur = aapl_dd.durations

msft_wi = msft_rets.wealth_index

spy_wi = spy_rets.wealth_index
spy_dd = spy_wi.drawdown
spy_dd_dur = spy_dd.durations

aapl_wi.plot(ax=ax_equity, color='green', label='APPL')
msft_wi.plot(ax=ax_equity, color='blue', label='MSFT')
spy_wi.plot(ax=ax_equity, color='grey', label='SPY')

aapl_dd.plot(ax=ax_drawdown, color='green')
spy_dd.plot(ax=ax_drawdown, color='grey')

aapl_wi.monthly_returns.plot(ax=ax_monthly_returns)
aapl_wi.annual_returns.plot(ax=ax_yearly_returns)

rolling_rets = pyinvestingsnippets.RollingReturns(aapl_rets.data, rolling_window=252)

# 3 month rolling annualized vol
rolling_vol = pyinvestingsnippets.RollingVolatility(aapl_rets.data, rolling_window=90, window=252)

# get the monthly rolling beta
rolling_beta = pyinvestingsnippets.RollingBetaRegression(spy_rets.data, aapl_rets.data, 30)
rolling_beta.plot(ax=ax_beta, color='red', label='regr')
rolling_beta = pyinvestingsnippets.RollingBetaCovariance(spy_rets.data, aapl_rets.data, 30)
rolling_beta.plot(ax=ax_beta, color='green', label='cov')

# get the total beta
beta = pyinvestingsnippets.BetaCovariance(spy_wi.monthly_returns.data, aapl_wi.monthly_returns.data)

rolling_rets.plot(ax=ax_rolling_returns)
rolling_vol.plot(ax=ax_rolling_vol)

downside_risk = pyinvestingsnippets.DownsideRisk(aapl_rets.data)
downside_risk.plot(ax=ax_downside_risk)

print(apple_stock_prices['AAPL'].prices.weekly_returns.data.shape)
print(apple_stock_prices['AAPL'].prices.weekly_returns.srri.data)

def _plot_stats(ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()

    data = [
        ['Total Return', '{:.0%}'.format(aapl_wi.total_return), '{:.0%}'.format(spy_wi.total_return)],
        ['CAGR', '{:.2%}'.format(aapl_wi.cagr), '{:.2%}'.format(spy_wi.cagr)],
        ['Max Drawdown', '{:.2%}'.format(aapl_dd.max_drawdown), '{:.2%}'.format(spy_dd.max_drawdown)],
        ['Avg Drawdown Duration', aapl_dd_dur.mean(), spy_dd_dur.mean()],
        ['Max Drawdown Duration', aapl_dd_dur.max(), spy_dd_dur.max()],
        ['Beta', '{:.2}'.format(beta.beta), '1']
    ]
    column_labels=["Metric", "Asset", "Benchmark"]
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