import numpy as np
from src.backtester import cumulative_returns, shift_signal, calculate_spread_change, calculate_return
from src.spread import calculate_spread, calculate_zscore
from src.strategy import get_signal


def total_returns(cum_returns): 
    """ 
    Generates the total final cumulative returns from a pandas Series or 
    Dataframe of cumulative returns
    """
    return cum_returns.iloc[-1]


def sharpe_ratio(returns): 
    """ 
    Returns the annualized sharpe ratio of a series of returns.
    """
    return (returns.mean() / returns.std()) * np.sqrt(252)


def sharpe_ratio_active(returns): 
    """ 
    Returns the sharpe ratio of returns from which a signal or trade was generated. 
    """
    non_zero_returns = returns[returns != 0]
    return (non_zero_returns.mean() / non_zero_returns.std()) * np.sqrt(252)


def max_drawdown(cum_returns): 
    """ 
    Calculates the largest drawdown in absolute cumulative-return 
    you would encounter using the strategy.
    """
    peaks = cum_returns.cummax()
    drawdown = (cum_returns - peaks)
    return drawdown.min()
    
