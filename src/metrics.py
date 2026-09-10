import numpy as np
from backtester import cumulative_returns, shift_signal, calculate_spread_change, calculate_return
from spread import calculate_spread, calculate_zscore
from strategy import get_signal

""" 
Generates the total final cumulative returns from a pandas Series or 
Dataframe of cumulative returns
"""
def total_returns(cum_returns): 
    return cum_returns.iloc[-1]

""" 
Returns the annualized sharpe ratio of a series of returns.

"""
def sharpe_ratio(returns): 
    return (returns.mean() / returns.std()) * np.sqrt(252)

""" 
Returns the sharpe ratio of returns from which a signal or trade was generated. 
"""

def sharpe_ratio_active(returns): 
    non_zero_returns = returns[returns != 0]
    return (non_zero_returns.mean() / non_zero_returns.std()) * np.sqrt(252)

""" 
Calculates the largest drawdown in absolute cumulative-return 
you would encounter using the strategy.
"""

def max_drawdown(cum_returns): 
    peaks = cum_returns.cummax()
    drawdown = (cum_returns - peaks)
    return drawdown.min()
    
