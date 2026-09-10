import matplotlib.pyplot as plt 
from config import ticker1, ticker2, window
from load_data import load_data 
from preprocess import process_data
from pair_selection import pair_selection_results
from spread import calculate_zscore, calculate_spread
from strategy import get_signal 
from backtester import calculate_spread_change, shift_signal, calculate_return, cumulative_returns
from metrics import total_returns, sharpe_ratio, sharpe_ratio_active, max_drawdown


if __name__ == "__main__": 
    t1 = ticker1 
    t2 = ticker2 

    load_data(t1, t2)
    process_data(t1, t2)

    corr, p_val, passing = pair_selection_results

    if passing == False: 
        print("This pair does not meet the necessary requirements for correlation or cointegration")
    else: 
        spread = calculate_spread(t1, t2)
        z_score = calculate_zscore(window, spread)

        signal = get_signal(z_score)
        shift_sig = shift_signal(signal)
        spread_diff = calculate_spread_change(spread)
        returns = calculate_return(shift_sig, spread_diff)
        cum_returns = cumulative_returns(returns)

        cum_returns.plot()
        plt.show()

        print("Total returns: " + str(total_returns(cum_returns)))
        print("--------")
        print("Sharpe ratio: " + str(sharpe_ratio(returns)))
        print("---------")
        print("Sharpe ratio active: " + sharpe_ratio_active(returns))
        print("---------")
        print("Max Drawdown: " + max_drawdown(cum_returns))





