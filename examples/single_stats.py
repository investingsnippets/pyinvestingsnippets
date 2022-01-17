import datetime

import pandas_datareader as web

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import pyinvestingsnippets 


end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5 * 365)
end_date_frmt = end_date.strftime("%Y-%m-%d")
start_date_frmt = start_date.strftime("%Y-%m-%d")

spy_index_prices = web.DataReader("SPY", data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']

print(spy_index_prices.prices.weekly_returns.srri.value)
print(spy_index_prices.prices.weekly_returns.srri.risk_class)

print(spy_index_prices.prices.monthly_returns.srri.value)
print(spy_index_prices.prices.monthly_returns.srri.risk_class)