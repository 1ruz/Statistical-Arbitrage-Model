import pandas as pd 
from spread import calculate_spread,calculate_zscore

""" 
Generally for pairs trading if the z-score is above 2 std, 
this would mean that the spread is too high, which meants 
that it will eventually come back down prompting a short of the spread. 
Conversely if the z-score is below 2 std, the spread is lower than usual, 
and there is an expectation for price to go back up which prompts 
a long of the spread. When z-score cross back toward 0, this would be 
a signal that it is time to exit the trade as the reversion would have happened.

Signal = -1 for a short 
Signal = 1 for a long  
"""

def strategy(z_score): 
    signal = pd.Series(0, index=z_score.index)
    signal[z_score > 2] = -1 
    signal[z_score < -2] = 1 

    return signal 


if __name__ == "__main__": 
    spread = calculate_spread("EWA", "EWC")
    z_score = calculate_zscore(spread)
    print(strategy(z_score))


