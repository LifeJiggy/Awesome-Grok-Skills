# Finance Agent — System Architecture

## 1. Executive Summary

The Finance Agent is a comprehensive quantitative finance platform providing portfolio management, risk analytics, derivatives pricing, technical/fundamental analysis, backtesting, and Monte Carlo simulation. It is designed as a modular, extensible system suitable for institutional-grade financial computations.

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          FINANCE AGENT                                   │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   Portfolio   │  │     Risk     │  │  Derivatives  │  │  Technical │  │
│  │   Manager     │  │   Analyzer   │  │   Pricer      │  │  Analysis  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
│         │                 │                  │                 │         │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  ┌─────┴──────┐  │
│  │   Backtest   │  │   Monte      │  │  Fixed       │  │ Fundamental │  │
│  │   Engine     │  │   Carlo      │  │  Income      │  │  Analysis   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Market Regime Detection                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Utility Functions (TVM, WACC, DCF)             │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Deep Dives

### 3.1 Portfolio Manager

The Portfolio Manager is the central hub for tracking positions, executing trades, and computing portfolio-level metrics.

**Responsibilities:**
- Position tracking with average entry price calculation
- Cash management and margin checking
- Trade execution with commission and slippage modeling
- Performance attribution (realized vs unrealized PnL)
- Weight computation for asset allocation analysis
- Daily value recording for drawdown and return analysis

**Key Data Structures:**
- `Position`: Per-symbol holding with entry price, quantity, current price, and PnL
- `Trade`: Immutable record of every transaction with cost breakdown
- `MarketData`: OHLCV bar with derived fields (typical price, range)

**Design Decisions:**
- Positions use `update_price()` to recalculate unrealized PnL lazily
- Cash is deducted on trade execution, not on settlement (T+0 modeling)
- Trade history is append-only for audit trail integrity
- Portfolio value snapshots stored for time-series analysis

```
  User/Strategy
       │
       ▼
  ┌─────────┐    execute_trade()    ┌──────────────┐
  │ Portfolio │ ──────────────────► │  Trade Log   │
  │ Manager   │                     │  (append)    │
  └─────┬────┘                     └──────────────┘
        │
        ├── update_prices() ──► Position Updates
        ├── get_weights() ────► Asset Allocation
        ├── get_performance_summary() ──► Metrics
        └── _daily_returns() ──► Return Series
```

### 3.2 Risk Analyzer

The Risk Analyzer computes risk metrics at position and portfolio levels.

**Computed Metrics:**
- **Value at Risk (VaR)**: Historical, Parametric, Exponential Weighted
- **Conditional VaR (CVaR)**: Expected shortfall beyond VaR threshold
- **Volatility**: Standard deviation with annualization option
- **Beta & Alpha**: Relative to market benchmark
- **Sharpe & Sortino Ratios**: Risk-adjusted return metrics
- **Max Drawdown**: Peak-to-trough decline with duration
- **Tracking Error & Information Ratio**: Active management metrics
- **Stress Testing**: Scenario-based PnL impact analysis

**VaR Methods Comparison:**

| Method | Pros | Cons |
|--------|------|------|
| Historical | Non-parametric, captures fat tails | Requires long history, stationary assumption |
| Parametric | Fast, analytical | Normality assumption, misses tail risk |
| Exponential Weighted | Recent-volatility sensitive | Parameter tuning required |

**Stress Testing Flow:**
```
  ┌──────────┐     ┌─────────────┐     ┌──────────────┐
  │ Position │ ──► │ Scenario    │ ──► │ PnL Impact   │
  │ List     │     │ Application │     │ Calculation  │
  └──────────┘     └─────────────┘     └──────────────┘
       │                                     │
       │         ┌─────────────┐             │
       └────────►│ Aggregate   │◄────────────┘
                 │ Portfolio   │
                 │ Impact      │
                 └─────────────┘
```

### 3.3 Black-Scholes Pricer

Options pricing engine with full Greeks computation and implied volatility solver.

**Capabilities:**
- European call/put pricing via Black-Scholes formula
- All five Greeks: Delta, Gamma, Theta, Vega, Rho
- Implied volatility via Newton-Raphson iteration
- Input validation for edge cases (zero time, zero volatility)

**Greeks Interpretation:**

| Greek | Measures | Typical Range |
|-------|----------|---------------|
| Delta | Price sensitivity to underlying | -1.0 to 1.0 |
| Gamma | Rate of delta change | 0 to ~0.5 |
| Theta | Time decay per day | Negative (long options) |
| Vega | Sensitivity to volatility | Positive (long options) |
| Rho | Sensitivity to interest rate | Small, positive/negative |

### 3.4 Technical Analyzer

Library of technical indicators with composite signal generation.

**Indicators Implemented:**
- **SMA** (Simple Moving Average): Trend identification
- **EMA** (Exponential Moving Average): Responsive trend
- **RSI** (Relative Strength Index): Momentum oscillator
- **MACD**: Trend-following momentum
- **Bollinger Bands**: Volatility envelope
- **ATR** (Average True Range): Volatility measurement
- **OBV** (On-Balance Volume): Volume-price confirmation

**Composite Signal Logic:**
```
  Input: Price series
         │
         ├── RSI < 30 ──────────► +1 (oversold)
         ├── RSI > 70 ──────────► -1 (overbought)
         ├── Price > EMA(20) ───► +1 (uptrend)
         ├── Price < EMA(20) ───► -1 (downtrend)
         ├── MACD crossover ────► ±1 (momentum shift)
         ├── BB lower breach ───► +1 (mean reversion buy)
         ├── BB upper breach ───► -1 (mean reversion sell)
         │
         ▼
  Score >= 2  → STRONG_BUY
  Score == 1  → BUY
  Score == 0  → NEUTRAL
  Score == -1 → SELL
  Score <= -2 → STRONG_SELL
```

### 3.5 Fundamental Analyzer

Multi-factor scoring engine based on financial statement analysis.

**Scoring Categories and Weights:**

| Category | Weight | Key Ratios |
|----------|--------|------------|
| Profitability | 25% | Gross margin, Net margin, ROE |
| Growth | 20% | Revenue growth rate |
| Valuation | 20% | P/E ratio inverse |
| Financial Health | 20% | Current ratio, Debt/Equity |
| Efficiency | 15% | Asset turnover |

**Grading Scale:**
- A+ (≥0.85), A (≥0.75), B+ (≥0.65), B (≥0.55)
- C+ (≥0.45), C (≥0.35), D (<0.35)

### 3.6 Fixed Income Analyzer

Bond pricing, duration, convexity, and yield curve interpolation.

**Key Formulas:**
- **Bond Price**: PV of coupon payments + PV of face value
- **Macaulay Duration**: Weighted average time to cash flows
- **Modified Duration**: Price sensitivity to yield changes
- **Convexity**: Second-order price sensitivity (curvature)

**Price Change Approximation:**
```
ΔP ≈ -Modified_Duration × ΔY + ½ × Convexity × (ΔY)²
```

### 3.7 Backtest Engine

Event-driven strategy evaluation framework.

**Architecture:**
```
  ┌──────────────┐
  │ Historical   │
  │ Data Feed    │
  └──────┬───────┘
         │ for each bar:
         ▼
  ┌──────────────┐     ┌──────────────┐
  │ Strategy     │ ──► │  Signal      │
  │ .generate()  │     │  Generation  │
  └──────────────┘     └──────┬───────┘
                              │
                              ▼
                      ┌──────────────┐
                      │  Position    │
                      │  Sizing      │
                      └──────┬───────┘
                              │
                              ▼
                      ┌──────────────┐
                      │  Portfolio   │
                      │  Execution   │
                      └──────┬───────┘
                              │
                              ▼
                      ┌──────────────┐
                      │  Backtest    │
                      │  Results     │
                      └──────────────┘
```

**Metrics Computed:**
- Total return, Annualized return
- Sharpe ratio, Sortino ratio, Calmar ratio
- Max drawdown and duration
- Win rate, Profit factor
- Trade count and average holding period
- Recovery factor

### 3.8 Monte Carlo Simulator

Random-path simulation for portfolio projections and option pricing.

**Portfolio Path Simulation:**
- Geometric Brownian Motion (GBM) model
- Configurable expected return, volatility, time horizon
- Outputs: mean, percentiles (1/5/95/99), probability of loss, Expected Shortfall

**Option Payoff Simulation:**
- Simulates terminal asset prices under GBM
- Computes average discounted payoff
- Reports probability of finishing in-the-money

### 3.9 Regime Detector

Market regime classification from return series.

**Regimes:**
- Bull: Annualized return > 10%
- Bear: Annualized return < -10%
- High Volatility: Annualized vol > 1.5× threshold
- Low Volatility: Annualized vol < 0.5× threshold
- Sideways: Default for moderate conditions

---

## 4. Data Flow Architecture

```
  ┌──────────────────────────────────────────────────────────────┐
  │                     DATA INGESTION                           │
  │  Market Data │ Financial Statements │ User Portfolio State    │
  └──────┬───────┴──────────┬──────────┴──────────┬─────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
  │  Technical   │  │ Fundamental  │  │  Portfolio           │
  │  Analysis    │  │ Analysis     │  │  Management          │
  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘
         │                  │                     │
         ▼                  ▼                     ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
  │  Signal      │  │  Score       │  │  Position            │
  │  Generation  │  │  Computation │  │  Tracking            │
  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘
         │                  │                     │
         └──────────────────┼─────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Strategy        │
                  │  Execution       │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  Risk Analysis   │
                  │  & Reporting     │
                  └──────────────────┘
```

---

## 5. Design Patterns

### Strategy Pattern
Trading strategies implement the `Strategy` protocol with `generate_signals()` and `name()`. This enables:
- Runtime strategy selection
- Strategy composition (signal combination)
- Backtest engine compatibility

### Protocol Pattern
The `DataSource` protocol defines the interface for market data providers, enabling:
- Mock data for testing
- Pluggable real data feeds
- API abstraction

### Immutability
`Trade` objects are `frozen=True` dataclasses — once executed, records cannot be mutated. This ensures audit trail integrity.

### Composition over Inheritance
Components are composed, not inherited:
- `BacktestEngine` contains a `PortfolioManager` and `RiskAnalyzer`
- `PortfolioManager` uses `Position` objects
- `RiskAnalyzer` operates on raw return series

---

## 6. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | Type hints + dataclasses |
| Numerics | math, statistics (stdlib) |
| Random | random (with seed for reproducibility) |
| Logging | Python logging module |
| Patterns | ABC, Protocol, Enum, NamedTuple |
| Testing | pytest (recommended) |
| Distribution | Pure Python, no external dependencies |

---

## 7. Security Considerations

### Data Sensitivity
- Financial data is processed in-memory only; no persistent storage by default
- No external network calls in the core library
- All computations are deterministic given the same inputs

### Input Validation
- Division-by-zero guards on all ratio calculations
- Bounds checking on confidence levels and probabilities
- Negative value guards on prices and quantities

### Audit Trail
- Every trade is logged with unique ID, timestamp, and cost breakdown
- Portfolio value snapshots are recorded for historical analysis
- Trade history is append-only

### Reproducibility
- Monte Carlo simulations accept seed parameter
- Backtest results are deterministic for the same data and strategy
- Random number generation uses module-level Random instances

---

## 8. Scalability Considerations

### Current Design
- Single-threaded, in-memory computation
- Suitable for portfolio sizes up to ~10,000 positions
- Backtest engine processes one bar at a time (streaming)

### Scaling Strategies
1. **Vectorization**: Replace loops with numpy arrays for 10-100× speedup
2. **Parallelism**: Monte Carlo paths can be distributed across cores
3. **Caching**: Memoize indicator calculations for overlapping windows
4. **Streaming**: Process market data in real-time via generator pattern
5. **Persistence**: Add database backend for trade history and analytics

### Performance Benchmarks (Estimated)

| Operation | Current | With NumPy |
|-----------|---------|-----------|
| SMA(252) on 10K bars | ~2ms | ~0.1ms |
| VaR (10K simulations) | ~50ms | ~5ms |
| Monte Carlo (10K paths) | ~200ms | ~20ms |
| Backtest (252 bars) | ~100ms | ~15ms |

---

## 9. Extension Points

### Adding a New Strategy
```python
class MyStrategy(Strategy):
    def name(self) -> str:
        return "MyStrategy"

    def generate_signals(
        self, data: List[MarketData], context: Dict[str, Any]
    ) -> Dict[str, SignalStrength]:
        # Your signal logic here
        return {"AAPL": SignalStrength.BUY}
```

### Adding a New Risk Model
Extend `RiskAnalyzer.calculate_var()` with a new `RiskModel` enum variant.

### Adding a New Indicator
Add a static method to `TechnicalAnalyzer` following the pattern:
```python
@staticmethod
def my_indicator(prices: List[float], period: int) -> List[Optional[float]]:
    ...
```

### Custom Financial Statements
Create `FinancialStatement` objects with any subset of fields — all derived ratios handle zero/missing values gracefully.

---

## 10. Testing Strategy

### Unit Tests
- Each indicator has known-input/known-output test cases
- VaR calculations validated against industry benchmarks
- Black-Scholes prices validated against published tables
- Edge cases: empty inputs, zero values, negative prices

### Integration Tests
- Backtest engine with known strategy and synthetic data
- Portfolio execution with multi-trade sequences
- Risk report computation on real return series

### Property-Based Tests
- VaR always non-negative
- Portfolio value = cash + Σ(position market values)
- Sum of weights = 1.0
- Greeks satisfy put-call parity relationships

---

## 11. Dependencies and Constraints

### External Dependencies
None — the agent uses only Python standard library modules. This ensures:
- Zero-install deployment
- No version conflicts
- Full portability across platforms

### Python Version
Requires Python 3.10+ for:
- `match` statements (if used)
- Modern type hint syntax
- Performance improvements in CPython

### Memory Profile
- ~1KB per position object
- ~100 bytes per trade record
- ~8KB per 10K-bar time series
- Typical portfolio (100 positions): < 1MB total
