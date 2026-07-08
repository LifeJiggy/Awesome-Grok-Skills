# Finance Agent

> Production-grade quantitative finance platform for portfolio management, risk analytics, derivatives pricing, technical/fundamental analysis, and algorithmic strategy backtesting.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
  - [Portfolio Management](#portfolio-management)
  - [Risk Analytics](#risk-analytics)
  - [Options Pricing](#options-pricing)
  - [Technical Analysis](#technical-analysis)
  - [Fundamental Analysis](#fundamental-analysis)
  - [Backtesting](#backtesting)
  - [Monte Carlo Simulation](#monte-carlo-simulation)
  - [Fixed Income](#fixed-income)
  - [Market Regime Detection](#market-regime-detection)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Finance Agent provides a comprehensive suite of financial computation tools built entirely in Python with zero external dependencies. It covers the full spectrum of quantitative finance:

- **Portfolio Management**: Position tracking, trade execution, performance attribution
- **Risk Analytics**: VaR, CVaR, Sharpe/Sortino ratios, drawdown analysis, stress testing
- **Derivatives Pricing**: Black-Scholes with full Greeks, implied volatility solver
- **Technical Analysis**: SMA, EMA, RSI, MACD, Bollinger Bands, ATR, OBV, composite signals
- **Fundamental Analysis**: Multi-factor scoring from financial statements
- **Backtesting**: Event-driven strategy evaluation with realistic cost modeling
- **Monte Carlo Simulation**: Portfolio projections and option pricing via random paths
- **Fixed Income**: Bond pricing, duration, convexity, yield curve interpolation
- **Market Regime Detection**: Bull/bear/volatility classification from return series

---

## Features

| Category | Capabilities |
|----------|-------------|
| Portfolio | Multi-asset tracking, weight analysis, daily snapshots |
| Risk | VaR (3 methods), CVaR, beta, alpha, tracking error, stress tests |
| Options | Black-Scholes pricing, 5 Greeks, implied volatility |
| Technical | 7 indicators, composite signal scoring (5 levels) |
| Fundamental | 5-category weighted scoring, letter grades |
| Backtest | Strategy evaluation, Sharpe, Sortino, Calmar, drawdown |
| Monte Carlo | Portfolio paths, option payoffs, percentile analysis |
| Fixed Income | Price, duration, convexity, yield interpolation |
| Regime | 5 market regimes from historical returns |

---

## Quick Start

```python
from agents.finance.agent import (
    PortfolioManager, RiskAnalyzer, OrderSide, AssetClass,
    BlackScholesPricer, OptionType,
    TechnicalAnalyzer, FundamentalAnalyzer, FinancialStatement,
    BacktestEngine, SMACrossStrategy,
    MonteCarloSimulator, FixedIncomeAnalyzer, Bond,
)
from datetime import datetime, timedelta

# 1. Create a portfolio
pm = PortfolioManager(initial_capital=100_000)
pm.execute_trade("AAPL", OrderSide.BUY, 50, 175.0)
pm.execute_trade("GOOGL", OrderSide.BUY, 30, 140.0)
pm.update_prices({"AAPL": 182.0, "GOOGL": 145.0})

print(pm.get_performance_summary())

# 2. Analyze risk
import random
rng = random.Random(42)
returns = [rng.gauss(0.0005, 0.015) for _ in range(252)]
ra = RiskAnalyzer()
print(ra.full_risk_report(returns))

# 3. Price an option
bs = BlackScholesPricer()
print(bs.price(OptionType.CALL, 100, 105, 0.5, 0.2))
```

### Run the Agent

```bash
python agents/finance/agent.py
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Finance Agent                           │
├─────────────────────────────────────────────────────────────┤
│  Portfolio Manager │ Risk Analyzer │ Black-Scholes Pricer    │
│  Technical Analyzer│ Fundamental   │ Fixed Income Analyzer   │
│  Backtest Engine   │ Monte Carlo   │ Regime Detector         │
├─────────────────────────────────────────────────────────────┤
│              Utility Functions (TVM, WACC, DCF)              │
├─────────────────────────────────────────────────────────────┤
│        Data Models (Trade, Position, MarketData, Bond)       │
└─────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

---

## Usage

### Portfolio Management

```python
from agents.finance.agent import PortfolioManager, OrderSide, AssetClass

pm = PortfolioManager(initial_capital=250_000)

# Execute trades with commission and slippage
pm.execute_trade("AAPL", OrderSide.BUY, 100, 175.00, AssetClass.EQUITY, commission=1.0)
pm.execute_trade("MSFT", OrderSide.BUY, 80, 330.00, AssetClass.EQUITY, commission=1.0)
pm.execute_trade("NVDA", OrderSide.BUY, 60, 450.00, AssetClass.EQUITY, commission=1.0)

# Update market prices
pm.update_prices({"AAPL": 182.50, "MSFT": 345.00, "NVDA": 480.00})

# Analyze
print(pm.get_weights())          # {"AAPL": 0.35, "MSFT": 0.53, "NVDA": 0.12}
print(pm.get_performance_summary())  # Full metrics dict
```

### Risk Analytics

```python
from agents.finance.agent import RiskAnalyzer, RiskModel

ra = RiskAnalyzer(risk_free_rate=0.05)

# Value at Risk — three methods
var_hist = ra.calculate_var(returns, 0.95, RiskModel.HISTORICAL)
var_param = ra.calculate_var(returns, 0.95, RiskModel.PARAMETRIC)
var_ewm = ra.calculate_var(returns, 0.95, RiskModel.EXPONENTIAL_WEIGHTED)

# Conditional VaR (Expected Shortfall)
cvar = ra.calculate_cvar(returns, 0.95)

# Risk-adjusted metrics
sharpe = ra.calculate_sharpe(returns)
sortino = ra.calculate_sortino(returns)

# Beta and Alpha
beta = ra.calculate_beta(asset_returns, market_returns)
alpha = ra.calculate_alpha(asset_returns, market_returns)

# Full report
metrics = ra.full_risk_report(returns, benchmark_returns)
```

### Options Pricing

```python
from agents.finance.agent import BlackScholesPricer, OptionType

bs = BlackScholesPricer(risk_free_rate=0.05)

# European Call
price = bs.price(OptionType.CALL, spot=100, strike=105, time_to_expiry=0.5, volatility=0.2)
greeks = bs.greeks(OptionType.CALL, 100, 105, 0.5, 0.2)

# European Put
put_price = bs.price(OptionType.PUT, spot=100, strike=95, time_to_expiry=0.5, volatility=0.2)

# Implied Volatility from market price
iv = bs.implied_volatility(4.50, OptionType.CALL, 100, 105, 0.5)
```

### Technical Analysis

```python
from agents.finance.agent import TechnicalAnalyzer

ta = TechnicalAnalyzer()

# Individual indicators
sma = ta.sma(prices, period=20)
ema = ta.ema(prices, period=20)
rsi = ta.rsi(prices, period=14)
macd_line, signal_line, histogram = ta.macd(prices)
upper, middle, lower = ta.bollinger_bands(prices)
atr_values = ta.atr(highs, lows, closes)
obv_values = ta.obv(closes, volumes)

# Composite signal (combines all indicators)
signal = ta.composite_signal(prices)
# Returns: STRONG_BUY, BUY, NEUTRAL, SELL, or STRONG_SELL
```

### Fundamental Analysis

```python
from agents.finance.agent import FundamentalAnalyzer, FinancialStatement
from datetime import datetime

fa = FundamentalAnalyzer()

stmt = FinancialStatement(
    symbol="DEMO",
    period_end=datetime.utcnow(),
    revenue=10_000_000,
    cost_of_goods_sold=6_000_000,
    operating_income=3_000_000,
    net_income=2_000_000,
    total_assets=15_000_000,
    total_liabilities=5_000_000,
    shareholders_equity=10_000_000,
    current_assets=6_000_000,
    current_liabilities=3_000_000,
    shares_outstanding=1_000_000,
)

result = fa.compute_composite_score(stmt, growth_rate=0.15, pe_ratio=22)
print(f"Score: {result['composite_score']:.3f}, Grade: {result['grade']}")
```

### Backtesting

```python
from agents.finance.agent import BacktestEngine, SMACrossStrategy, RSIMeanReversionStrategy

engine = BacktestEngine(initial_capital=100_000, commission_per_trade=1.0)

# SMA crossover
result = engine.run(SMACrossStrategy(fast_period=20, slow_period=50), data)
print(f"Return: {result.total_return:.2%}, Sharpe: {result.sharpe_ratio:.2f}")

# RSI mean reversion
result = engine.run(RSIMeanReversionStrategy(period=14), data)
```

### Monte Carlo Simulation

```python
from agents.finance.agent import MonteCarloSimulator

mc = MonteCarloSimulator(seed=42)

# Portfolio projection
result = mc.simulate_portfolio_paths(
    initial_value=250_000,
    expected_return=0.10,
    volatility=0.20,
    days=252,
    num_simulations=10_000
)
print(f"Mean final: ${result['mean_final']:,.0f}")
print(f"Prob of loss: {result['probability_of_loss']:.1%}")

# Option payoff simulation
option_result = mc.simulate_option_payoff(
    OptionType.CALL, spot=100, strike=105, time_to_expiry=0.5,
    volatility=0.2, risk_free_rate=0.05
)
```

### Fixed Income

```python
from agents.finance.agent import FixedIncomeAnalyzer, Bond, YieldCurvePoint
from datetime import datetime, timedelta

fi = FixedIncomeAnalyzer()

bond = Bond(
    symbol="T10Y", coupon_rate=0.045, face_value=1000,
    maturity_date=datetime.utcnow() + timedelta(days=3650)
)

price = fi.price_bond(bond, market_yield=0.05)
mac_dur = fi.macaulay_duration(bond, 0.05)
mod_dur = fi.modified_duration(bond, 0.05)
conv = fi.convexity(bond, 0.05)

# Yield curve interpolation
curve = [
    YieldCurvePoint(0.25, 4.5), YieldCurvePoint(0.5, 4.6),
    YieldCurvePoint(1.0, 4.7), YieldCurvePoint(2.0, 4.8),
    YieldCurvePoint(5.0, 4.9), YieldCurvePoint(10.0, 5.0),
]
y_3yr = fi.interpolate_yield(curve, 3.0)  # Interpolated 3-year yield
```

### Market Regime Detection

```python
from agents.finance.agent import RegimeDetector

rd = RegimeDetector(lookback=60, vol_threshold=0.25)
regime = rd.detect(daily_returns)
# Returns: BULL, BEAR, SIDEWAYS, HIGH_VOLATILITY, LOW_VOLATILITY

history = rd.regime_history(daily_returns, window=60)
```

---

## API Reference

### Core Classes

| Class | Description |
|-------|-------------|
| `PortfolioManager` | Portfolio tracking and trade execution |
| `RiskAnalyzer` | Risk metric computation |
| `BlackScholesPricer` | European option pricing with Greeks |
| `TechnicalAnalyzer` | Technical indicator library |
| `FundamentalAnalyzer` | Financial statement scoring |
| `BacktestEngine` | Strategy backtesting framework |
| `MonteCarloSimulator` | Random path simulation |
| `FixedIncomeAnalyzer` | Bond analytics |
| `RegimeDetector` | Market regime classification |

### Data Classes

| Class | Description |
|-------|-------------|
| `Trade` | Immutable trade record |
| `Position` | Current holding tracker |
| `MarketData` | OHLCV bar with derived fields |
| `FinancialStatement` | Company financials snapshot |
| `BacktestResult` | Backtest output metrics |
| `RiskMetrics` | Aggregated risk metrics |
| `Bond` | Fixed income instrument |
| `YieldCurvePoint` | Yield curve data point |

### Enums

| Enum | Values |
|------|--------|
| `OrderSide` | BUY, SELL, SHORT, COVER |
| `OrderType` | MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP, ICEBERG |
| `AssetClass` | EQUITY, FIXED_INCOME, COMMODITY, CURRENCY, CRYPTO, REAL_ESTATE, ALTERNATIVE |
| `RiskModel` | HISTORICAL, PARAMETRIC, MONTE_CARLO, EXPONENTIAL_WEIGHTED |
| `MarketRegime` | BULL, BEAR, SIDEWAYS, HIGH_VOLATILITY, LOW_VOLATILITY, CRISIS |
| `OptionType` | CALL, PUT |
| `OptionStyle` | AMERICAN, EUROPEAN |
| `SignalStrength` | STRONG_SELL(-2), SELL(-1), NEUTRAL(0), BUY(1), STRONG_BUY(2) |

---

## Examples

### Complete Portfolio Workflow

```python
from agents.finance.agent import *

# Initialize
pm = PortfolioManager(500_000)
ra = RiskAnalyzer(risk_free_rate=0.05)

# Build portfolio
pm.execute_trade("AAPL", OrderSide.BUY, 200, 175.0, commission=2.0)
pm.execute_trade("GOOGL", OrderSide.BUY, 100, 140.0, commission=2.0)
pm.execute_trade("MSFT", OrderSide.BUY, 150, 330.0, commission=2.0)
pm.execute_trade("BND", OrderSide.BUY, 300, 95.0, AssetClass.FIXED_INCOME, commission=1.0)

# Update and analyze
pm.update_prices({"AAPL": 182.0, "GOOGL": 145.0, "MSFT": 345.0, "BND": 96.0})

summary = pm.get_performance_summary()
weights = pm.get_weights()

# Risk analysis on daily returns
returns = [r for _, r in pm.daily_values[-252:]]
if len(returns) > 1:
    metrics = ra.full_risk_report(returns)
    print(f"VaR 95%: {metrics.var_95:.2%}")
    print(f"Sharpe: {metrics.sharpe_ratio:.2f}")
```

### Strategy Comparison

```python
from agents.finance.agent import *

strategies = [
    SMACrossStrategy(10, 30),
    SMACrossStrategy(20, 50),
    RSIMeanReversionStrategy(14),
    RSIMeanReversionStrategy(7),
]

results = []
for strat in strategies:
    result = engine.run(strat, historical_data)
    results.append(result)
    print(f"{result.strategy_name}: Return={result.total_return:.2%}, "
          f"Sharpe={result.sharpe_ratio:.2f}, MaxDD={result.max_drawdown:.2%}")
```

---

## Configuration

### Risk Analyzer Settings

```python
# Custom risk-free rate and confidence levels
ra = RiskAnalyzer(risk_free_rate=0.045, confidence_levels=(0.90, 0.95, 0.99))
```

### Backtest Engine Settings

```python
# Custom cost model
engine = BacktestEngine(
    initial_capital=100_000,
    commission_per_trade=2.0,      # $2 per trade
    slippage_pct=0.001             # 0.1% slippage
)
```

### Fundamental Analyzer Weights

```python
# Custom scoring weights
fa = FundamentalAnalyzer(weights={
    "profitability": 0.30,
    "growth": 0.25,
    "valuation": 0.15,
    "financial_health": 0.20,
    "efficiency": 0.10,
})
```

### Monte Carlo Settings

```python
# Reproducible simulation with custom seed
mc = MonteCarloSimulator(seed=12345)
```

---

## Best Practices

1. **Always include transaction costs** in backtests — realistic commission and slippage
2. **Use multiple VaR methods** — historical for non-normal, parametric for speed
3. **Validate implied volatility** — check for convergence and reasonable values
4. **Test strategies across regimes** — bull, bear, sideways, high-volatility
5. **Beware overfitting** — use out-of-sample data and parameter sensitivity analysis
6. **Monitor portfolio weights** — avoid concentration risk
7. **Use stop-losses** — limit maximum drawdown per position
8. **Document assumptions** — every model has limitations
9. **Stress test regularly** — run scenario analysis on adverse conditions
10. **Keep trade logs** — append-only for audit trail integrity

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| VaR is zero or negative | Check returns are non-empty and not all identical |
| Black-Scholes extreme values | Verify time_to_expiry is in years, volatility is annualized |
| Backtest unrealistic returns | Check for look-ahead bias, add transaction costs |
| Implied vol doesn't converge | Market price may be below intrinsic; try different starting sigma |
| Weights don't sum to 1.0 | Include cash position in weight calculation |
| NaN in results | Check for zero division in ratio calculations |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/add-new-indicator`)
3. Add tests for new functionality
4. Ensure all existing tests pass
5. Update documentation (GROK.md, README.md)
6. Submit a pull request

### Code Standards
- Full type hints on all public methods
- Docstrings for all classes and public methods
- Follow existing naming conventions
- Zero external dependencies (stdlib only)

---

## License

MIT License. See [LICENSE](../../LICENSE) for details.

---

## Files

- `agent.py` — Full implementation with all financial computation modules
- `ARCHITECTURE.md` — Detailed system architecture and design decisions
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

*Built with mathematical precision for quantitative finance.*
