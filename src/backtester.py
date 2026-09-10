import pandas as pd 
from spread import calculate_spread, calculate_zscore
from strategy import get_signal

""" 
Shifts the signal series one day ahead to avoids look-ahead bias 

Look-ahead bias is the idea that you should not make decisions based on 
information that you do not yet have at the time of the decision. 
Calculating returns on the same day of receiving a signal can or
would cause an optimistic result that would be profitable in the backtest 
but would fail in real life live execution. 

"""

def shift_signal(signal): 
    return signal.shift(periods = 1, freq = None)

""" 
Calculates the difference between the spread of two adjacent dates and returns the series 
"""
def calculate_spread_change(spread): 
    return spread.diff()

""" 
Calculates the return by multiplying the signal by the spread_change 

A bullish day would be + 
+1 * spread_change = +return 

A bearish day would be - 
-1 * spread_change = - return 
"""
def calculate_return(signals, spread_change): 
    returns = signals * spread_change 
    return returns 

""" 
Calculates the cumulative returns 
"""
def cumulative_returns(returns): 
    return returns.cumsum()


