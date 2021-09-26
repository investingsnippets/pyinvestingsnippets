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

spy_index_prices = retrieve_stock_data("SPY", start_date_frmt, end_date_frmt)

print(spy_index_prices['SPY'].prices.weekly_returns.srri.value)
print(spy_index_prices['SPY'].prices.weekly_returns.srri.risk_class)

print(spy_index_prices['SPY'].prices.monthly_returns.srri.value)
print(spy_index_prices['SPY'].prices.monthly_returns.srri.risk_class)