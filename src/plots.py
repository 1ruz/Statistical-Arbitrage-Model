import matplotlib.pyplot as plt 
from src.backtester import cumulative_returns

def plot_equity_curve(returns, t1, t2, best_result): 
    cumulative = cumulative_returns(returns)

    plt.figure(figsize=(10, 5))
    plt.plot(cumulative)
    plt.title(f"{t1}/{t2} - {best_result['strategy_name']} Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.show()
    plt.savefig("data/results/equity_curve.png")

def plot_zscore(z_score, t1, t2): 
    plt.figure(figsize=(10, 5))
    plt.plot(z_score)

    plt.axhline(2, linestyle="--")
    plt.axhline(-2, linestyle="--")
    plt.axhline(0, linestyle="-")

    plt.title(f"{t1}/{t2} Spread Z-Score")

    plt.xlabel("Date")
    plt.ylabel("Z-Score")

    plt.grid(True)
    plt.show()
    plt.savefig("data/results/z_score.png")
