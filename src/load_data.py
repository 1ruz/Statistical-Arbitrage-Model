import yfinance as yf
from datetime import datetime, timedelta

""" picking correlated tickers that may be interesting to take a lot at to begin with 
    1) SPY vs QQQ 
    2) Apple (AAPL) vs Microsoft (MSFT)
    3) Google (GOOGL) vs Facebook (META)

    but first we will start with 
    SPY vs QQQ 

"""

# we will use the last 2 years of daily data for our experiments
ticker_symbol1  = "SPY"
ticker_symbol2 = "QQQ"
end_date = datetime.today().strftime("%Y-%m-%d")
start_date = datetime.today() - timedelta(days=(365*2))

df1 = yf.download(ticker_symbol1, start=start_date, end=end_date)
print(df1.head())

df2 = yf.download(ticker_symbol2, start=start_date,end=end_date)
print(df2.head())