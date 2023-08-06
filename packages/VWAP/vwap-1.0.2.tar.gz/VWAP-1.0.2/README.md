Welcome to the VWAP package. This package takes as input an Alpha Vantage free API key, which can be found here: https://www.alphavantage.co/support/#api-key,
a stock ticker (eg. AAPL, AMZN, TSLA...), and a time interval (1min, 5min, 15min...). The package returns 4 figures:

(1) buy and sell signals figure with stock price and VWAP line
(2) Portfolio flow over time (holding, cash, total)
(3) ROI for VWAP strategy vs buy and hold
(4) Sharpe Ratio for VWAP strategy vs buy and hold

Please note that there is a call limit using a free API (5 calls per minute and 500 calls per day)
To run the code, you will first need to install AlphaVantage using the following pip call:
pip install alpha_vantage
Then, you can run the following lines to get the figures:

from portfolio import run
test = run(API_key='YOUR_API_KEY', ticker='TICKER_NAME', interval='5min')
full = test.complete()