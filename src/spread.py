from src.config import WINDOW 
""" 
Functions for constructing the price spread and 
calculating rolling statistics and z-scores. 
"""
def calculate_spread(price1, price2, hedge_ratio): 
    """ 
    Calculates the spread between two assets using the hedge ratio. 
    """
    spread = price2 - (hedge_ratio * price1) 
    return spread 


def calculate_mean(spread): 
    """ 
    A rolling mean or in other words the moving average smooths data 
    by averaging subsets of a fixed window size 
    """
    return spread.rolling(WINDOW).mean()


def calculate_std(spread): 
    """ 
    Calculates the rolling standard deviation or in other words 
    the moving standard deviation by averaging subsets 
    of a fixed window size 
    """
    return spread.rolling(WINDOW).std()

def calculate_zscore(spread): 
    """ 
    Calculates the rolling z_score of the spread
    """

    rolling_mean = calculate_mean(spread)
    rolling_std = calculate_std(spread)

    z_score = (spread - rolling_mean) / rolling_std
    return z_score 





