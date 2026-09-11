# Statistical Arbitrage / Pairs Trading Model

A self-directed Python project implementing a statistical arbitrage / pairs trading strategy from scratch. The project covers the full pipeline from historical market data and statistical pair selection to signal generation, out-of-sample backtesting, transaction cost modeling, and performance evaluation.

## Project Overview

Pairs trading is a strategy that attempts to profit from the temporary divergence of two historically related assets.

The model:

1. Downloads historical daily price data.
2. Screens candidate pairs using correlation and cointegration.
3. Estimates a hedge ratio using OLS regression.
4. Constructs a mean-reverting spread.
5. Calculates a rolling z-score.
6. Generates trading signals using z-score thresholds.
7. Backtests both stateless and stateful strategies.
8. Applies a one-day signal shift to avoid lookahead bias.
9. Incorporates transaction costs.
10. Evaluates performance on an unseen test period.

## Project Structure
```
Statistical-Arbitrage-Model/

├── data/
│   ├── raw/                  # historical price data
│   └── results/              # Backtest and pair-selection results displaying the best pair and strategy found

├── src/
│   ├── config.py             # Ticker universe and model parameters
│   ├── load_data.py          # Historical data acquisition via yfinance
│   ├── pair_selection.py     # Correlation, cointegration, and hedge ratio
│   ├── spread.py             # Spread, rolling statistics, and z-score
│   ├── strategy.py           # Stateless and stateful signal generation
│   ├── backtester.py         # Returns, transaction costs, and cumulative returns
│   ├── metrics.py            # Performance metrics
│   └── __init__.py

├── main.py                   # Main project pipeline
├── requirements.txt
└── README.md
```

## Methodology

### 1. Data

Daily closing prices are downloaded using `yfinance`.

The model uses adjusted historical prices through yfinance's `auto_adjust=True` behavior, accounting for stock splits and dividends.

The current ticker universe contains stocks and ETFs across several sectors and market categories, including:

Technology
Financials
Energy
Consumer
Healthcare
International ETFs
Broad-market ETFs

### 2. Pair Selection

Candidate pairs are screened using the Pearson correlation coefficient.

Pairs must satisfy a minimum correlation threshold (>0.7) before proceeding to the cointegration test.

The second filter is the **Engle-Granger two-step cointegration test** using:

```python
statsmodels.tsa.stattools.coint
```

with:

```python
trend="c"
method="aeg"
```

The pair is retained only when both conditions are satisfied:

```text
Correlation ≥ threshold
Cointegration p-value ≤ threshold
```

Correlation measures whether two assets tend to move together, while cointegration tests whether a stable long-run relationship exists between their price series.

Therefore, high correlation alone is not sufficient for a pairs trading strategy.

### 3. Hedge Ratio

For pairs that pass the statistical tests, the hedge ratio is estimated using ordinary least squares (OLS):

$$
Price_B = \alpha + \beta Price_A + \epsilon
$$

The estimated coefficient \(\beta\) is used as the hedge ratio.

The spread is then defined as:

$$
Spread_t = Price_{B,t} - \beta Price_{A,t}
$$

An intercept is included when estimating the regression, but the trading spread uses the estimated hedge ratio.

### 4. Z-Score

The spread is standardized using a rolling 20-day mean and standard deviation:

$$
Z_t =
\frac{Spread_t-\mu_t}{\sigma_t}
$$

where:

* \(\mu_t\) = 20-day rolling mean of the spread
* \(\sigma_t\) = 20-day rolling standard deviation

The z-score measures how far the current spread is from its recent average.

### 5. Trading Strategies

Two signal-generation approaches are implemented.

#### Stateless Strategy

The stateless strategy generates signals based directly on the z-score:

```text
Z-score > +2  → Short spread
Z-score < -2  → Long spread
Otherwise     → No position
```

The signal is recalculated independently each day.

#### Stateful Strategy

The stateful strategy maintains a position after entering a trade.

```text
Z-score > +2  → Enter short spread
Z-score < -2  → Enter long spread

Short position → Exit when Z-score < +0.5
Long position  → Exit when Z-score > -0.5
```

This prevents the strategy from repeatedly generating the same entry signal while the spread remains beyond an entry threshold.

### 6. Out-of-Sample Backtesting

To reduce lookahead bias and distinguish model formation from strategy evaluation, the historical data is split into:

```text
70% → Training / formation period
30% → Test period
```

Pair selection and hedge ratio estimation are performed **only using the training data**.

The selected pairs and their training-period hedge ratios are then applied to the unseen test data.

This prevents the test period from influencing which pairs are selected.

### 7. Lookahead Bias

The trading signal is shifted forward by one trading day before being applied to returns.

In other words:

```text
Today's signal
      ↓
Applied to
      ↓
Tomorrow's price movement
```

This prevents the model from using information from the same day's price movement to generate a trade that supposedly occurred before that movement.

### 8. Transaction Costs

A transaction cost assumption is incorporated whenever the trading position changes.

The model detects changes in the signal using:

```python
signals.diff().abs()
```

and subtracts the corresponding transaction cost from the daily strategy return.

This provides a more realistic performance estimate than a frictionless backtest.

The current implementation uses a simplified transaction-cost model rather than a full execution-level model for each leg.

## Performance Metrics

The model evaluates each pair and strategy using:

### Total Return

The cumulative return over the test period:

$$
R_{total} = \prod_{t=1}^{T}(1+R_t)-1
$$

### Sharpe Ratio

The annualized Sharpe ratio is calculated using a 0% risk-free rate:

$$
Sharpe =
\frac{\bar{R}}{\sigma_R}\sqrt{252}
$$

where 252 represents the approximate number of trading days per year.

### Active-Day Sharpe Ratio

An additional Sharpe ratio is calculated using only days on which the strategy has an active position.

This helps distinguish the performance of the strategy while trading from the diluted full-period performance caused by long periods with no position.

### Maximum Drawdown

Maximum drawdown measures the largest peak-to-trough decline in cumulative strategy returns.

## Out-of-Sample Results

The current out-of-sample test produced the following results:

| Pair         | Strategy     | Total Return |   Sharpe | Active Sharpe | Max Drawdown |
| ------------ | ------------ | -----------: | -------: | ------------: | -----------: |
| **NVDA/SPY** | **Stateful** |   **13.82%** | **1.73** |      **3.53** |   **-2.42%** |
| NVDA/COST    | Stateful     |       24.93% |     1.52 |          2.79 |       -5.80% |
| JPM/SPY      | Stateless    |        5.44% |     1.18 |          3.45 |       -1.64% |
| NVDA/SPY     | Stateless    |        5.18% |     1.06 |          3.19 |       -2.83% |
| GS/WMT       | Stateful     |       16.56% |     0.96 |          1.62 |      -12.96% |
| COP/MRK      | Stateful     |        9.74% |     0.63 |          1.14 |      -12.65% |
| JPM/SPY      | Stateful     |        4.06% |     0.51 |          0.84 |       -8.41% |
| META/JPM     | Stateful     |        5.61% |     0.39 |          0.68 |       -9.43% |
| MS/WMT       | Stateful     |        4.99% |     0.37 |          0.60 |       -7.55% |
| META/JPM     | Stateless    |        2.07% |     0.30 |          0.77 |       -3.66% |
| NVDA/COST    | Stateless    |        1.75% |     0.23 |          0.69 |       -5.12% |
| GS/WMT       | Stateless    |        1.15% |     0.14 |          0.35 |      -11.28% |
| MS/WMT       | Stateless    |        0.80% |     0.11 |          0.26 |       -8.93% |
| META/SPY     | Stateless    |       -0.27% |    -0.03 |         -0.07 |       -3.73% |
| META/SPY     | Stateful     |       -2.20% |    -0.17 |         -0.27 |       -9.30% |
| META/QQQ     | Stateful     |       -4.06% |    -0.25 |         -0.38 |      -14.52% |
| GOOGL/QQQ    | Stateful     |       -6.37% |    -0.44 |         -0.67 |      -20.59% |
| COP/MRK      | Stateless    |       -5.16% |    -0.57 |         -1.62 |      -12.31% |
| GOOGL/QQQ    | Stateless    |       -8.00% |    -0.94 |         -2.45 |      -12.44% |
| META/QQQ     | Stateless    |       -7.02% |    -1.04 |         -2.56 |      -10.02% |

The strongest out-of-sample result was the **NVDA/SPY Stateful Strategy**, which produced a 13.82% total return, a 1.73 annualized Sharpe ratio, and a maximum drawdown of approximately 2.42%.

The NVDA/COST Stateful Strategy produced the highest total return at 24.93%, but with a lower Sharpe ratio of 1.52 and a larger maximum drawdown of 5.80%.

## Visualizations

The project generates:

### Equity Curve

The equity curve shows the cumulative performance of the best-performing out-of-sample strategy over the test period.

### Spread Z-Score

The z-score visualization shows the movement of the normalized spread relative to the trading thresholds:

```text
+2  → Short-entry threshold
 0  → Spread mean
-2  → Long-entry threshold
```

These visualizations help assess whether the strategy's trades correspond to periods of significant spread divergence and subsequent mean reversion.

## Findings

Several observations emerged from the analysis.

### Cointegration is more informative than correlation alone

Highly correlated assets do not necessarily form a suitable pairs-trading relationship.

For example, SPY/QQQ displayed extremely high correlation but failed the cointegration test. Similarly, AAPL/MSFT showed periods of reasonably high correlation without statistically significant cointegration.

This demonstrates the distinction between correlation and cointegration: correlation measures short-term co-movement, while cointegration is concerned with a stable long-run relationship.

### Cointegration does not guarantee profitability

Passing the cointegration test does not automatically imply that a profitable trading strategy exists.

A statistically valid long-run relationship can still produce weak or negative trading performance after considering entry thresholds, exit rules, transaction costs, and the specific testing period.

### Stateful signals generally performed better

The stateful strategy outperformed the stateless strategy for most of the strongest pairs.

This suggests that allowing positions to remain open until the spread partially reverts can be more effective than independently generating signals whenever the z-score crosses an entry threshold.

### Out-of-sample performance is important

The results demonstrate why pair selection should not be performed using the same data on which strategy performance is evaluated.

Using a formation period for pair selection and a separate unseen test period provides a more meaningful assessment of whether the strategy's historical relationship generalizes beyond the data used to construct it.

## Limitations

This project is intended as a statistical modeling and learning exercise rather than a production trading system.

Key limitations include:

* The test period represents only a portion of the available historical data.
* Pair relationships can change over time.
* The hedge ratio is estimated once during the formation period rather than dynamically updated.
* Transaction costs are modeled using a simplified assumption.
* Slippage, bid-ask spreads, market impact, and execution latency are not modeled.
* Capital allocation across multiple simultaneous pairs is not implemented.
* The current backtest does not simulate actual order execution.
* A single train/test split does not provide the same robustness as walk-forward testing.

Therefore, strong historical results should not be interpreted as evidence of guaranteed future profitability.

## Future Work

Potential extensions include:

* Walk-forward / rolling out-of-sample testing
* Dynamic hedge-ratio estimation
* More detailed two-leg transaction cost and slippage modeling
* Per-trade statistics such as win rate, average trade return, and holding period
* Capital allocation across multiple pairs
* Additional candidate pairs and asset classes
* Parameter sensitivity analysis for entry and exit thresholds
* Paper trading and live execution after extensive validation

## Conclusion

This project demonstrates a complete statistical arbitrage workflow, from identifying statistically related asset pairs to evaluating a trading strategy on unseen data.

The results show that statistical validation alone is not enough to establish a trading edge. Pair selection, signal design, transaction costs, and out-of-sample validation all materially affect strategy performance.

The strongest current result is the NVDA/SPY stateful strategy, but the out-of-sample results also demonstrate substantial variation across pairs, highlighting the importance of robust validation rather than relying on a single successful backtest.
