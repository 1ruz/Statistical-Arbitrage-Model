import pandas as pd 

"""""
Data constitutes of : | Price | Close | High | Low | Open | Volume 
                       Ticker | SYMBOL --------------------------- 
                       Date   | 
""" 
ticker_symbol1  = "SPY"
ticker_symbol2 = "QQQ"

df1 = pd.read_csv("{}_raw.csv".format(ticker_symbol1), index_col="Date", parse_dates=["Date"])
df2 = pd.read_csv("{}_raw.csv".format(ticker_symbol2), index_col="Date", parse_dates=["Date"])

merged_df = pd.merge(df1["Close"].rename("{symbol}_close".format(symbol = ticker_symbol1)), df2["Close"].rename("{symbol}_close".format(symbol = ticker_symbol2)), left_index=True, right_index=True, how="inner")
merged_df.to_csv("data/processed/{symbol1}_{symbol2}_data.csv".format(symbol1=ticker_symbol1, symbol2=ticker_symbol2))