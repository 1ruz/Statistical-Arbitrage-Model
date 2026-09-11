from itertools import combinations 
from src.config import TICKERS
from src.load_data import load_data 
from src.pair_selection import pair_selection_results
from src.spread import calculate_zscore, calculate_spread
from src.strategy import get_signal, get_stateful_signal
from src.backtester import shift_signal, calculate_return, cumulative_returns
from src.metrics import total_returns, sharpe_ratio, sharpe_ratio_active, max_drawdown
from src.plots import plot_equity_curve, plot_zscore
import pandas as pd 


def select_pairs(prices): 
    # Generate all possible pairs from ticker universe 
    tickers = [ticker for group in TICKERS.values() for ticker in group]
    pairs = list(combinations(tickers,2))
    
    passing_pairs = []
    
    for t1, t2 in pairs:
    
        corr, p_val, hedge_ratio, passing = pair_selection_results(prices[t1], prices[t2])
    
        if passing: 
            passing_pairs.append((t1,t2, hedge_ratio))

    return passing_pairs 
        

def backtest_pair(price1, price2, hedge_ratio, t1, t2): 
    spread = calculate_spread(price1, price2, hedge_ratio)
    z_score = calculate_zscore(spread)
    
    signal = get_signal(z_score)
    stateful_signal = get_stateful_signal(z_score)
    
    strategies = [("Stateless Strategy", signal), ("Stateful Strategy", stateful_signal)]

    results = [] 

    for strategy_name, sig in strategies: 
    
        shift_sig = shift_signal(sig)
        returns = calculate_return(shift_sig, price1, price2, hedge_ratio)
        cum_returns = cumulative_returns(returns)
    
        results.append({
                        "pair": f"{t1}/{t2}", 
                        "strategy_name": strategy_name, 
                        "total_returns" : total_returns(cum_returns), 
                        "sharpe_ratio": sharpe_ratio(returns), 
                        "sharpe_ratio_active": sharpe_ratio_active(returns), 
                        "max_drawdown" : max_drawdown(cum_returns)
                        })
    return results 

def best_strategy(results_df, test_prices, passing_pairs):
    # Get the best strategy
    best_result = results_df.iloc[0]

    print("\nBest out-of-sample strategy:")
    print(best_result)


    # Get the pair
    t1, t2 = best_result["pair"].split("/")

    # Find the training hedge ratio 
    for pair_t1, pair_t2, hedge_ratio in passing_pairs:
        if pair_t1 == t1 and pair_t2 == t2:
            break

    pair_df = test_prices[[t1, t2]].dropna()

    # Calculate spread and z-score
    spread = calculate_spread(
        pair_df[t1],
        pair_df[t2],
        hedge_ratio
    )

    z_score = calculate_zscore(spread)

    # Select the strategy
    if best_result["strategy_name"] == "Stateless Strategy":
        signal = get_signal(z_score)
    else:
        signal = get_stateful_signal(z_score)


    # Backtest
    shift_sig = shift_signal(signal)

    returns = calculate_return(
        shift_sig,
        pair_df[t1],
        pair_df[t2],
        hedge_ratio
    )

    cumulative = cumulative_returns(returns)

    return cumulative, z_score, best_result, t1, t2


def main(): 

    prices = load_data(TICKERS)

    split_index = int(len(prices) * 0.7)

    train_prices = prices.iloc[:split_index]
    test_prices = prices.iloc[split_index:]

    passing_pairs = select_pairs(train_prices)

    results = []

    for t1, t2, hedge_ratio in passing_pairs: 

        pair_df = test_prices[[t1,t2]].dropna()
        pair_results = backtest_pair(pair_df[t1], pair_df[t2], hedge_ratio, t1, t2)

        results.extend(pair_results)

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("sharpe_ratio", ascending=False)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", None)
    print(results_df)

    cumulative, z_score, best_result, s1, s2 = best_strategy(results_df,test_prices,passing_pairs)

    plot_equity_curve(cumulative, s1, s2, best_result)
    plot_zscore(z_score, s1, s2)


if __name__ == "__main__": 
    main()


            





