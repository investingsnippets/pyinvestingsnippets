import urllib.parse
import pandas as pd

# https://fred.stlouisfed.org/
url = "https://fred.stlouisfed.org/graph/fredgraph.csv"

syms = {
    "TWEXBMTH" : "usd", 
    "T10Y2YM" : "term_spread", 
    "GOLDAMGBD228NLBM" : "gold",
}

params = {
    "fq": "Monthly,Monthly,Monthly",
    "id": ",".join(syms.keys()),
    "cosd": "2000-01-01",
    "coed": "2019-02-01",
}

data = pd.read_csv(
    url + "?" + urllib.parse.urlencode(params, safe=","),
    na_values={"."},
    parse_dates=["DATE"],
    index_col=0
).pct_change().dropna().rename(columns=syms)
print(data.head())

