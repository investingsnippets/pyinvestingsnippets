import datetime
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import pandas_datareader as web

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import pyinvestingsnippets

from utils import gbm

TICKER = 'MSFT'

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5 * 365)
end_date_frmt = end_date.strftime("%Y-%m-%d")
start_date_frmt = start_date.strftime("%Y-%m-%d")

# prices = web.DataReader(TICKER, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
prices = gbm(10, 1, steps_per_year=252).iloc[:, 0]  # gets first column
prices.name = f"{TICKER}-gbm"

fig = plt.figure(figsize=(14, 8), constrained_layout=True)
fig.suptitle("Report", weight='bold')
gs = gridspec.GridSpec(3, 1, figure=fig)
ax_equity = plt.subplot(gs[0, :])
ax_drawdown = plt.subplot(gs[1, :])
ax_histogram = plt.subplot(gs[2, :])

rets = prices.returns

wi = rets.wealth_index
dd = wi.drawdown

wi.plot(ax=ax_equity, color='blue')
dd.plot(ax=ax_drawdown, color='blue')
rets.plot(ax=ax_histogram)

ax_histogram.axvline(-rets.var(), color ='red', lw = 2, alpha = 0.75,label='VaR: {:.3f}'.format(-rets.var()))
ax_histogram.axvline(-rets.cvar(), color ='green', lw = 2, alpha = 0.75,label='CVaR: {:.3f}'.format(-rets.cvar()))

plt.legend(loc=0)
plt.show()