.. title:: pyinvestingsnippets

pyinvestingsnippets
=====================

PyInvestingSnippets is a python library which implements `pandas <https://pandas.pydata.org/>`_ extensions
for stock and investment portfolio analysis. Several utilities are also provided.

Quick links
-----------

* Current version: |version| (`download from PyPI <https://pypi.python.org/pypi/pyinvestingsnippets>`_)
* `Source (GitHub) <https://github.com/investingsnippets/pyinvestingsnippets>`_

Features
--------

* WealthIndex
* Drawdown
* `SRRI <https://www.esma.europa.eu/sites/default/files/library/2015/11/10_673.pdf>`_
* Weekly/Monthly/Annual Returns
* Rolling Returns
* Rolling Volatility
* Beta (regression/covariance)
* Rolling Beta (regression/covariance)
* Exponentially Weighted Downside Risk

Example
-------

Here is a simple example ::

   from yahoofinancials import YahooFinancials
   import datetime
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

   if __name__ == "__main__":
      end_date = datetime.datetime.now()
      start_date = end_date - datetime.timedelta(days=5 * 365)
      end_date_frmt = end_date.strftime("%Y-%m-%d")
      start_date_frmt = start_date.strftime("%Y-%m-%d")

      aapl_prices = retrieve_stock_data('AAPL', start_date_frmt, end_date_frmt)
      aapl_rets = aapl_prices['AAPL'].prices.returns

      aapl_wi = aapl_rets.wealth_index
      aapl_dd = aapl_wi.drawdown
      aapl_dd_dur = aapl_dd.durations

      print('Total return: {:.0%}'.format(aapl_wi.total_return))
      print('Max drawdown: {:.2%}'.format(aapl_dd.max_drawdown))
      print('Average drawdown duration: {}'.format(aapl_dd_dur.mean()))
   
Complete examples can be found `here <https://github.com/investingsnippets/pyinvestingsnippets/tree/master/examples>`_.


Installation
------------

::

    pip install pyinvestingsnippets

Pyinvestingsnippets is listed in `PyPI <https://pypi.org/project/pyinvestingsnippets/>`_ and
can be installed with ``pip``.

**Prerequisites**: pyinvestingsnippets requires Python 3.7 or newer

.. toctree::
   :titlesonly:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
