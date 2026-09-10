import yfinance as yf
import numpy as np 
from datetime import datetime, timedelta
from src.config import TICKERS 



# we will use the last 5 years of daily data for our experiments

def load_data(TICKERS): 

    """ 
    Downloads the last five years of daily price data for the specified 
    ticker universe and saves the closing prices to CSV. 

    The ticker universe is provided as a dictionary grouped by sector or
    asset type.
    """

    tickers = [ ticker for group in TICKERS.values() for ticker in group]
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = datetime.today() - timedelta(days=(365*5))

    data = yf.download(tickers, start=start_date, end=end_date)

    prices = data["Close"]
    prices.to_csv("data/raw/prices.csv")

    return prices 
