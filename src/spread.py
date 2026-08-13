from pair_selection import compute_hedge_ratio, get_df

""" 
A spread is 
Spread can be calculated using the following formula 
spread = ticker2 - hedge_ratio * ticker1
"""
def calculate_spread(ticker1, ticker2): 
    df = get_df(ticker1, ticker2)
    spread = df[ticker2+"_close"] - (compute_hedge_ratio(ticker1, ticker2) * df[ticker1+"_close"]) 
    return spread 

""" 
A rolling mean or in other words the moving average smooths data 
by averaging subsets of a fixed window size 
"""
def calculate_mean(window, spread): 
    return spread.rolling(window).mean()

def calculate_std(window, spread): 
    return spread.rolling(window).std()

def calculate_zscore(window, spread): 
    rolling_mean = calculate_mean(window,spread)
    rolling_std = calculate_std(window,spread)

    z_score = (spread - rolling_mean) / rolling_std
    return z_score 


if __name__ == "__main__": 
    spread = calculate_spread("EWA", "EWC")
    print(calculate_zscore(20, spread)) 





