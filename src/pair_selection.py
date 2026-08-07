import pandas as pd
from statsmodels.tsa.stattools import coint
import numpy as np 
import statsmodels.api as sm 


def get_df(ticker1, ticker2): 
    df = pd.read_csv("data/processed/{s1}_{s2}_data.csv".format(s1=ticker1, s2=ticker2))
    return df 

# calculate correlation (corrrelation check)
""" 
Correlation measures how two assets move in relation to each other. 
The statistical metric is typically between -1.0 and 1.0. 
A correlation above 0.7 is considered highly correlated by industry standards 

"""
def correlation_test(ticker1, ticker2): 
    df = get_df(ticker1, ticker2)
    corr = df[ticker1+"_close"].corr(df[ticker2+"_close"])
    return corr 

""" 
    Cointegration is a property that indicates whether two or more non-stationary time series share an equilibrium long-term. 
    This equilibrium is determined by whether or not after a certain period of time the residuals of these two assests are 
    stationary when observed over a period of time. 

"""
# cointegration test 
def cointegration_test(ticker1, ticker2): 
    df = get_df(ticker1, ticker2)

    y0 = df[ticker1+"_close"]
    y1 = df[ticker2+"_close"]

    test_stat, p_val, crit_val = coint(y0, y1, trend = "c", method = "aeg")

    return test_stat, p_val, crit_val 


""" Hedge Ratio Formula : 
    Regressing one stock on the other using OLS (Ordinary Least Squares) 
    yt = alpha + beta * xt + Et 
    QQQ = intercept + (hedge ratio) * SPY + residual 
 """ 

def compute_hedge_ratio(ticker1, ticker2): 
    df = get_df(ticker1, ticker2)

    x = np.array(df[ticker1+"_close"])
    x_intercept = sm.add_constant(x)
    y = np.array(df[ticker2+"_close"])

    model = sm.OLS(y, x_intercept)
    coefficients = model.fit() 

    slope = coefficients.params[1]

    return slope 
    

def pair_selection_results(ticker1, ticker2): 
    corr = correlation_test(ticker1, ticker2)
    p_val = cointegration_test(ticker1, ticker2)[1]

    print(corr)
    print(p_val)
    
    if corr < 0.7 or p_val > 0.05 : 
        with open("data/results/results.csv", "a") as file: 
            file.write("{symbol1},{symbol2} - Failure\n".format(symbol1=ticker1, symbol2=ticker2)) 
    else: 
        with open("data/results/results.csv", "a") as file:
            file.write("{symbol1},{symbol2} - Success\n".format(symbol1=ticker1, symbol2=ticker2))

if __name__ == "__main__":
    pair_selection_results("EWA", "EWC")