import yfinance as yf
import numpy as np 
from datetime import datetime, timedelta

""" Picking correlated tickers that may be interesting to take a lot at to begin with 
    1) SPY vs QQQ 
    2) Apple (AAPL) vs Microsoft (MSFT)
    3) Google (GOOGL) vs Facebook (META)
    4) EWA (Australia) vs EWC (Canada)
    5) GLD (Gold Trust) vs GDX (Gold Miners)
    6) XLE (Energy Select Sector) vs OIH (Oil Services) 
    7) SPY vs IVV 
    
"""

# we will use the last 5 years of daily data for our experiments

def load_data(ticker1, ticker2): 
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = datetime.today() - timedelta(days=(365*5))

    df1 = yf.download(ticker1, start=start_date, end=end_date)
    #print(df1.head())
    df1.to_csv("data/raw/{symbol}_raw.csv".format(symbol=ticker1))

    df2 = yf.download(ticker2, start=start_date,end=end_date)
    #print(df2.head())
    df2.to_csv("data/raw/{symbol}_raw.csv".format(symbol=ticker2))

load_data("EWA", "EWC")