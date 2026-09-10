Statistical Arbitrage / Pairs Trading Model

A self-directed learning project implementing a full pairs trading pipeline from scratch. This pipeline involves data acquisition, statistical pair validation, spread construction, signal generation, backtesting, and performance evaluation.

Project structure

Statistical-Arbitrage-Model/
├── data/
│   ├── raw/            # untouched and unprocessed price data per ticker, directly from yfinance
│   ├── processed/       # merged, date-aligned Close price series per pair data
│   └── results/         # pair selection test results (pass/fail log)
├── src/
│   ├── load_data.py     # Downloads historical price data via yfinance
│   ├── preprocess.py    # Merges/aligns two tickers' raw data into one series
│   ├── pair_selection.py # Correlation check, Engle-Granger cointegration test, hedge ratio
│   ├── spread.py        # Spread construction, rolling mean/std, z-score
│   ├── strategy.py       # Z-score threshold signal generation
│   ├── backtester.py     # Lookahead-bias-safe backtest, cumulative returns
│   └── metrics.py        # Total return, Sharpe ratio, max drawdown
├── requirements.txt
└── README.md

Methodology

Data: daily close prices pulled via yfinance, adjusted for splits/dividends (yfinance's default auto_adjust=True behavior).

Pair validation: candidate pairs are screened first by correlation (>0.7 threshold), then by the Engle-Granger two-step cointegration test (statsmodels.tsa.stattools.coint, trend="c", method="aeg"). Correlation alone is not sufficient — cointegration is the property that actually supports a mean-reversion strategy.

Hedge ratio: derived via OLS regression of one asset's close price on the other's, with an intercept. The spread is calculated as spread = price_B - hedge_ratio * price_A, matching the regression's dependent/independent variable setup.

Signal generation: a rolling mean and rolling standard deviation (20-day window) of the spread are used to compute a z-score. A stateless threshold rule flags a short signal when z-score > 2, a long signal when z-score < -2, and no signal otherwise.

Backtesting: the signal is shifted forward one day before being applied to returns, to avoid lookahead bias. Daily strategy returns are calculated as the shifted signal multiplied by the day-over-day spread change, then accumulated into a cumulative returns series.

Metrics: total return, annualized Sharpe ratio (0% risk-free rate, √252 annualization), and maximum drawdown (peak-to-trough decline of the cumulative returns series).

Pairs tested
Pair	   Correlation	 Cointegration p-value	 Result
SPY / QQQ	   0.99	                    0.14	Failed
AAPL / MSFT (2yr)	-0.08	0.89	Failed
AAPL / MSFT (5yr)	0.77	0.87	Failed
EWA / EWC (5yr)	>0.7	< 0.05	Passed

SPY/QQQ and AAPL/MSFT are a useful negative result: both had periods of reasonably high correlation without showing statistically significant cointegration, illustrating that correlation and cointegration are testing different properties. EWA/EWC (Australia and Canada equity ETFs, both commodity-driven economies) passed both tests, with plausible underlying economic rationale rather than a purely coincidental statistical result.


Backtest results — EWA/EWC (2021–2026, full 5-year window)
Total return: cumulative spread-point return of roughly 1.3 over the period.
Sharpe ratio (full period): ~0.10
Sharpe ratio (active days only): ~0.30
Max drawdown: roughly -6.6 spread points


My findings 

Cointegration is a real, necessary filter. The most intuitively "similar" pairs (SPY/QQQ, AAPL/MSFT) failed the cointegration test despite reasonable correlation. However, passing cointegration does not automatically mean a strong trading edge. EWA/EWC is statistically validated as a genuine long-run relationship, but the simple stateless ±2 z-score strategy tested here shows only a modest Sharpe ratio, not a strongly exploitable one.

A large share of the diluted full-period Sharpe ratio comes from the strategy not generating any trading signal on the majority of trading days, which is a known characteristic of a stateless, threshold-only signal design. These results have not yet been validated out-of-sample (formation vs. backtest split) or adjusted for transaction costs, so they should be read as an initial first assesment rather than a final verdict on tradeability.

Possible future work

Formation/backtest split: re-derive cointegration and hedge ratio on a formation subset only, and evaluate performance on a genuinely unseen backtest period.
Stateful signal logic: hold a position from entry to exit rather than re-flagging every day past threshold, enabling real win-rate and per-trade statistics.
Incorporate transaction cost modeling.
Screening additional candidate pairs (other resource-economy or currency-linked ETF pairs).
Live/paper execution, once a strategy shows a validated, out-of-sample edge.