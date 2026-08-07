
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

if __name__ == "__main__": 
    print(calculate_spread("EWA", "EWC"))


