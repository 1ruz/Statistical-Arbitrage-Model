from itertools import combinations 
from src.config import TICKERS
from src.load_data import load_data 
from src.pair_selection import pair_selection_results
from src.spread import calculate_zscore, calculate_spread
from src.strategy import get_signal, get_stateful_signal
from src.backtester import shift_signal, calculate_return, cumulative_returns
from src.metrics import total_returns, sharpe_ratio, sharpe_ratio_active, max_drawdown
import pandas as pd 


if __name__ == "__main__": 

    prices = load_data(TICKERS)

    # Generate all possible pairs from ticker universe 
    tickers = [ticker for group in TICKERS.values() for ticker in group]
    pairs = list(combinations(tickers,2))

    passing_pairs = []

    for t1, t2 in pairs:

        corr, p_val, hedge_ratio, passing = pair_selection_results(prices[t1], prices[t2])

        if passing: 
            passing_pairs.append((t1,t2, hedge_ratio))

    results = []

    for t1, t2, hedge_ratio in passing_pairs: 

        pair_df = prices[[t1,t2]].dropna()

        price1 = pair_df[t1]
        price2 = pair_df[t2]

        spread = calculate_spread(price1, price2, hedge_ratio)
        z_score = calculate_zscore(spread)

        signal = get_signal(z_score)
        stateful_signal = get_stateful_signal(z_score)

        strategies = [("Stateless Strategy", signal), ("Stateful Strategy", stateful_signal)]

        for strategy_name, sig in strategies: 

            shift_sig = shift_signal(sig)
            returns = calculate_return(shift_sig, price1, price2, hedge_ratio)
            cum_returns = cumulative_returns(returns)

            results.append({
                            "pair": f"{t1}/{t2}", 
                            "strategy_name": strategy_name, 
                            "total_returns" : total_returns(cum_returns), 
                            "sharpe_ratio": sharpe_ratio(returns), 
                            "sharpe_ratio_active ": sharpe_ratio_active(returns), 
                            "max_drawdown" : max_drawdown(cum_returns)
                            })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("sharpe_ratio", ascending=False)
    print(results_df)
            

            





