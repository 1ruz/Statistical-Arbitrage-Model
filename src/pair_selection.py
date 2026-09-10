import pandas as pd
from statsmodels.tsa.stattools import coint
import numpy as np 
import statsmodels.api as sm 
from src.config import COINTEGRATION_THRESHOLD, CORRELATION_THRESHOLD


# calculate correlation (corrrelation check)

def correlation_test(price1, price2): 
    """ 
    Correlation measures how two assets move in relation to each other. 
    The statistical metric is typically between -1.0 and 1.0. 
    A correlation above 0.7 is considered highly correlated by industry standards 
    """
    corr = price1.corr(price2)
    return corr 

# cointegration test 
def cointegration_test(price1, price2): 
    """ 
    Cointegration is a property that indicates whether two or more non-stationary time series share an equilibrium long-term. 
    This equilibrium is determined by whether or not after a certain period of time the residuals of these two assests are 
    stationary when observed over a period of time. 
    """
 
    test_stat, p_val, crit_val = coint(price1, price2, trend = "c", method = "aeg")

    return test_stat, p_val, crit_val 


def compute_hedge_ratio(price1, price2): 
    """ Hedge Ratio Formula : 
    Regressing one stock on the other using OLS (Ordinary Least Squares) 
    yt = alpha + beta * xt + Et 
    QQQ = intercept + (hedge ratio) * SPY + residual 
    """ 

    x = np.array(price1)
    x_intercept = sm.add_constant(x)
    y = np.array(price2)

    model = sm.OLS(y, x_intercept)
    coefficients = model.fit() 

    slope = coefficients.params[1]

    return slope 


def pair_selection_results(price1, price2): 
    """ 
    Calculates whether two tickers satisfy the correlation and cointegration test 
    requirements and records either "Sucess" or "Failure" in a CSV file
    """

    corr = correlation_test(price1, price2)
    p_val = cointegration_test(price1, price2)[1]
    hedge_ratio = compute_hedge_ratio(price1, price2)
    
    passing = (corr > CORRELATION_THRESHOLD and p_val <= COINTEGRATION_THRESHOLD)

    return corr, p_val, hedge_ratio, passing 

if __name__ == "__main__":
    pair_selection_results("EWA", "EWC")