
def shift_signal(signal): 

    """ 
    Shifts the signal series one day ahead to avoids look-ahead bias 

    Look-ahead bias is the idea that you should not make decisions based on 
    information that you do not yet have at the time of the decision. 
    Calculating returns on the same day of receiving a signal can or
    would cause an optimistic result that would be profitable in the backtest 
    but would fail in real life live execution. 

    """
    return signal.shift(periods = 1, freq = None)


def calculate_return(signals, price1, price2, hedge_ratio): 

    """ 
    Calculates the daily percentage return of the pairs-trading portfolio 

    The P&L is determined by the signal and the price changes of both assets and is 
    adjusted by the hedge ratio
    """
    price1_change = price1.diff()
    price2_change = price2.diff()

    pnl = signals * (price2_change - hedge_ratio * price1_change)

    capital = price2 + abs(hedge_ratio) * price1

    return pnl / capital 

def cumulative_returns(returns): 
    """ 
    Calculates the cumulative returns 
    """
    return returns.cumsum()


