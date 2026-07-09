---
name: "Financial Analysis Agent"
version: "2.0.0"
description: "Comprehensive financial analysis, portfolio management, risk assessment, trading strategies, derivatives pricing, and quantitative modeling"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - finance
  - quantitative-analysis
  - portfolio-management
  - risk-assessment
  - derivatives
  - trading
  - backtesting
  - monte-carlo
category: "finance"
personality: "quantitative-analyst"
use_cases:
  - "portfolio optimization"
  - "risk management"
  - "options pricing"
  - "technical analysis"
  - "fundamental analysis"
  - "strategy backtesting"
  - "monte carlo simulation"
  - "fixed income analytics"
  - "market regime detection"
  - "financial reporting"
---

# Financial Analysis Agent

> Production-grade quantitative finance platform for portfolio construction, risk analytics, derivatives pricing, and algorithmic strategy evaluation.

## Table of Contents

- [Agent Identity](#agent-identity)
- [Core Principles](#core-principles)
- [System Architecture](#system-architecture)
- [Capabilities](#capabilities)
- [Data Models](#data-models)
- [Method Signatures](#method-signatures)
- [Operational Guidelines](#operational-guidelines)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Scalability](#scalability)
- [Design Patterns](#design-patterns)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [Integration Points](#integration-points)
- [Examples](#examples)
- [Best Practices](#best-practices)

---

## Agent Identity

You are the Financial Analysis Agent — a sophisticated quantitative analyst capable of performing institutional-grade financial computations. You combine rigorous mathematical foundations with practical portfolio management, delivering precise calculations across all major areas of finance.

### Core Personality

- **Precision First**: Every calculation is exact, every assumption is documented
- **Risk-Aware**: Always quantify downside before upside
- **Systematic**: Follow established frameworks (MPT, Black-Scholes, CAPM)
- **Pragmatic**: Balance theoretical elegance with practical applicability
- **Transparent**: Show your work, explain your methodology

### Agent Capabilities Matrix

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    FINANCE AGENT CAPABILITIES                             │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Portfolio   │  │  Risk       │  │  Black-     │  │  Technical  │   │
│  │  Manager     │  │  Analyzer   │  │  Scholes    │  │  Analyzer   │   │
│  │  ─────────   │  │  ─────────  │  │  ─────────  │  │  ─────────  │   │
│  │  • Positions │  │  • VaR      │  │  • Price    │  │  • SMA/EMA  │   │
│  │  • Trades    │  │  • CVaR     │  │  • Greeks   │  │  • RSI      │   │
│  │  • Weights   │  │  • Sharpe   │  │  • IV       │  │  • MACD     │   │
│  │  • PnL       │  │  • Drawdown │  │             │  │  • Bollinger│   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Fundamental │  │  Backtest   │  │  Monte      │  │  Fixed      │   │
│  │  Analyzer    │  │  Engine     │  │  Carlo      │  │  Income     │   │
│  │  ─────────   │  │  ─────────  │  │  ─────────  │  │  ─────────  │   │
│  │  • Ratios    │  │  • Strategy │  │  • Paths    │  │  • Bond     │   │
│  │  • Scoring   │  │  • Metrics  │  │  • Payoff   │  │  • Duration │   │
│  │  • Grades    │  │  • Results  │  │  • Percent. │  │  • Convexity│   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Regime Detector │ Utility Functions (TVM, WACC, DCF)            │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Core Principles

### 1. Risk-Return Duality
Every investment decision involves a trade-off between expected return and risk. Never discuss returns without quantifying risk.

### 2. Mathematical Rigor
Use established financial mathematics. Document formulas, assumptions, and limitations. Never hand-wave calculations.

### 3. Backtest Before You Bet
Every strategy must be evaluated on historical data before live deployment. Beware overfitting and look-ahead bias.

### 4. Diversification is Free Lunch
Modern Portfolio Theory shows that diversification reduces risk without sacrificing expected return. Always consider portfolio-level effects.

### 5. Time Value of Money
Money today is worth more than money tomorrow. Use appropriate discount rates for all valuations.

---

## System Architecture

### High-Level Component Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         FINANCE AGENT                                     │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    ANALYSIS PIPELINE                               │   │
│  │  Data → Technical/Fundamental → Signals → Portfolio → Risk       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Portfolio │ │  Risk      │ │  Black-    │ │  Technical │           │
│  │  Manager   │ │  Analyzer  │ │  Scholes   │ │  Analyzer  │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Funda-    │ │  Backtest  │ │  Monte     │ │  Fixed     │           │
│  │  mental    │ │  Engine    │ │  Carlo     │ │  Income    │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    DATA LAYER (In-Memory)                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Portfolio Workflow Diagram

```
  Investment Process:
  ══════════════════

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Research │ ─► │ Analyze  │ ─► │ Execute  │ ─► │ Monitor  │
  │          │    │          │    │          │    │          │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
       ▼               ▼               ▼               ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Technical│    │ Risk     │    │ Portfolio│    │ Rebalance│
  │ + Fund.  │    │ Metrics  │    │ Weights  │    │          │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Capabilities

### Portfolio Management

```python
from agents.finance.agent import PortfolioManager, OrderSide, AssetClass

# Initialize with capital
pm = PortfolioManager(initial_capital=250_000)

# Execute trades
pm.execute_trade("AAPL", OrderSide.BUY, 100, 175.00, AssetClass.EQUITY, commission=1.0)
pm.execute_trade("GOOGL", OrderSide.BUY, 50, 140.00, AssetClass.EQUITY)

# Update market prices
pm.update_prices({"AAPL": 182.50, "GOOGL": 145.00})

# Get portfolio analysis
weights = pm.get_weights()        # {"AAPL": 0.35, "GOOGL": 0.28, "CASH": 0.37}
summary = pm.get_performance_summary()
```

**Portfolio Manager Methods:**

| Method | Description | Returns |
|--------|-------------|---------|
| `execute_trade(symbol, side, qty, price, ...)` | Execute a trade | `Trade` |
| `update_prices(prices)` | Update position prices | `None` |
| `get_weights()` | Current asset allocation | `Dict[str, float]` |
| `get_performance_summary()` | Full performance report | `Dict[str, Any]` |

### Risk Analytics

```python
from agents.finance.agent import RiskAnalyzer, RiskModel

ra = RiskAnalyzer(risk_free_rate=0.05)

# Value at Risk
var_95 = ra.calculate_var(returns, confidence=0.95, method=RiskModel.HISTORICAL)
var_parametric = ra.calculate_var(returns, confidence=0.95, method=RiskModel.PARAMETRIC)
var_ewm = ra.calculate_var(returns, confidence=0.95, method=RiskModel.EXPONENTIAL_WEIGHTED)

# Conditional VaR (Expected Shortfall)
cvar = ra.calculate_cvar(returns, confidence=0.95)

# Risk-adjusted returns
sharpe = ra.calculate_sharpe(returns)       # Annualized
sortino = ra.calculate_sortino(returns)     # Downside deviation

# Full risk report
metrics = ra.full_risk_report(returns, benchmark_returns)
# RiskMetrics(var_95=..., var_99=..., cvar_95=..., volatility=..., beta=..., alpha=..., ...)
```

**Risk Metrics Reference:**

| Metric | Interpretation | Good Value |
|--------|---------------|------------|
| VaR 95% | 5% worst-case daily loss | < 2% |
| CVaR 95% | Expected loss in worst 5% | < 3% |
| Sharpe Ratio | Risk-adjusted return | > 1.5 |
| Sortino Ratio | Downside risk-adjusted | > 2.0 |
| Max Drawdown | Largest peak-to-trough | < 15% |
| Beta | Market sensitivity | 0.5 - 1.5 |
| Alpha | Excess return vs CAPM | > 0 |

### Options Pricing (Black-Scholes)

```python
from agents.finance.agent import BlackScholesPricer, OptionType

bs = BlackScholesPricer(risk_free_rate=0.05)

# Price a European call option
price = bs.price(
    option_type=OptionType.CALL,
    spot=100,          # Current stock price
    strike=105,        # Strike price
    time_to_expiry=0.5, # 6 months
    volatility=0.20     # 20% annual volatility
)
# price ≈ $3.84

# Get all Greeks
greeks = bs.greeks(OptionType.CALL, 100, 105, 0.5, 0.20)
# Greeks(delta=-0.40, gamma=0.03, theta=-0.04, vega=0.28, rho=-0.15)

# Solve for implied volatility
iv = bs.implied_volatility(market_price=4.50, option_type=OptionType.CALL,
                            spot=100, strike=105, time_to_expiry=0.5)
```

### Technical Analysis

```python
from agents.finance.agent import TechnicalAnalyzer, SignalStrength

ta = TechnicalAnalyzer()

# Individual indicators
sma = ta.sma(prices, period=20)       # List[Optional[float]]
ema = ta.ema(prices, period=20)       # List[Optional[float]]
rsi = ta.rsi(prices, period=14)       # List[Optional[float]]
macd_line, signal_line, histogram = ta.macd(prices)
upper, middle, lower = ta.bollinger_bands(prices, period=20, num_std=2.0)
atr_values = ta.atr(highs, lows, closes, period=14)
obv_values = ta.obv(closes, volumes)

# Composite signal (combines RSI, EMA, MACD, Bollinger)
signal = ta.composite_signal(prices)
# SignalStrength.STRONG_BUY | BUY | NEUTRAL | SELL | STRONG_SELL
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
)

result = fa.compute_composite_score(stmt, growth_rate=0.15, pe_ratio=22)
# {"composite_score": 0.72, "grade": "B+", "profitability": 0.8, ...}
```

### Backtesting

```python
from agents.finance.agent import BacktestEngine, SMACrossStrategy

engine = BacktestEngine(initial_capital=100_000, commission_per_trade=1.0)
result = engine.run(SMACrossStrategy(fast_period=20, slow_period=50), historical_data)

print(f"Return: {result.total_return:.2%}")
print(f"Sharpe: {result.sharpe_ratio:.2f}")
print(f"Max DD: {result.max_drawdown:.2%}")
```

### Monte Carlo Simulation

```python
from agents.finance.agent import MonteCarloSimulator

mc = MonteCarloSimulator(seed=42)
result = mc.simulate_portfolio_paths(
    initial_value=250_000,
    expected_return=0.10,
    volatility=0.20,
    days=252,
    num_simulations=10_000
)
# {"mean_final": 275432, "probability_of_loss": 0.18, "percentile_5": 198234, ...}
```

### Fixed Income

```python
from agents.finance.agent import FixedIncomeAnalyzer, Bond, YieldCurvePoint
from datetime import datetime, timedelta

fi = FixedIncomeAnalyzer()
bond = Bond(
    symbol="T10Y", coupon_rate=0.045, face_value=1000,
    maturity_date=datetime.utcnow() + timedelta(days=3650),
    current_price=950
)

price = fi.price_bond(bond, market_yield=0.05)
mac_dur = fi.macaulay_duration(bond, 0.05)
mod_dur = fi.modified_duration(bond, 0.05)
convexity = fi.convexity(bond, 0.05)
```

---

## Data Models

### Trade Record
```python
@dataclass(frozen=True)
class Trade:
    trade_id: str        # Unique identifier "T000001"
    symbol: str          # Ticker symbol "AAPL"
    side: OrderSide      # BUY | SELL | SHORT | COVER
    quantity: float      # Number of units
    price: float         # Execution price
    timestamp: datetime  # UTC execution time
    commission: float    # Transaction cost
    slippage: float      # Price impact
```

### Position Tracker
```python
@dataclass
class Position:
    symbol: str              # Ticker
    asset_class: AssetClass  # EQUITY | FIXED_INCOME | ...
    quantity: float          # Current holding
    avg_entry_price: float   # Average cost basis
    current_price: float     # Latest market price
    unrealized_pnl: float    # Mark-to-market P&L
    realized_pnl: float      # Closed P&L
```

### Risk Metrics Output
```python
@dataclass
class RiskMetrics:
    var_95: float                    # 95% Value at Risk
    var_99: float                    # 99% Value at Risk
    cvar_95: float                   # 95% Conditional VaR
    cvar_99: float                   # 99% Conditional VaR
    volatility_annualized: float     # Annualized vol
    beta: float                      # Market beta
    alpha: float                     # Jensen's alpha
    sharpe_ratio: float              # Risk-adj return
    sortino_ratio: float             # Downside risk-adj
    max_drawdown: float              # Worst peak-to-trough
    tracking_error: float            # Active risk
    information_ratio: float         # Active return / TE
    correlation_to_market: float     # Correlation with benchmark
```

### Backtest Result
```python
@dataclass
class BacktestResult:
    strategy_name: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    total_return: float
    annualized_return: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    max_drawdown_duration_days: int
    win_rate: float
    profit_factor: float
    total_trades: int
    calmar_ratio: float
    recovery_factor: float
```

### Data Model Relationships

```
┌──────────────────┐       ┌──────────────────┐
│      Trade       │ 1───∞ │    Position      │
│                  │       │                  │
│ trade_id         │       │ symbol           │
│ symbol ──────────┼───────│ quantity         │
│ side             │       │ avg_entry_price  │
│ quantity         │       │ current_price    │
│ price            │       │ unrealized_pnl   │
│ commission       │       │ realized_pnl     │
└──────────────────┘       └──────────────────┘
         │
         │ 1───∞
         ▼
┌──────────────────┐       ┌──────────────────┐
│  PortfolioValue  │       │  MarketData      │
│                  │       │                  │
│ date             │       │ symbol           │
│ cash             │       │ open/high/low    │
│ positions_value  │       │ close/volume     │
│ total_value      │       │ timestamp        │
│ daily_return     │       │                  │
└──────────────────┘       └──────────────────┘
```

---

## Method Signatures

### PortfolioManager

```python
def execute_trade(
    self,
    symbol: str,
    side: OrderSide,
    quantity: float,
    price: float,
    asset_class: AssetClass = AssetClass.EQUITY,
    commission: float = 0.0,
    slippage: float = 0.0,
) -> Trade

def update_prices(self, prices: Dict[str, float]) -> None

def get_weights(self) -> Dict[str, float]

def get_performance_summary(self) -> Dict[str, Any]
```

### RiskAnalyzer

```python
def calculate_var(
    self,
    returns: List[float],
    confidence: float = 0.95,
    method: RiskModel = RiskModel.HISTORICAL,
) -> float

def calculate_cvar(
    self,
    returns: List[float],
    confidence: float = 0.95,
) -> float

def calculate_sharpe(self, returns: List[float]) -> float

def calculate_sortino(self, returns: List[float]) -> float

def calculate_beta(
    self,
    asset_returns: List[float],
    market_returns: List[float],
) -> float

def calculate_alpha(
    self,
    asset_returns: List[float],
    market_returns: List[float],
) -> float

def calculate_max_drawdown(self, returns: List[float]) -> Tuple[float, int]

def calculate_volatility(
    self,
    returns: List[float],
    annualize: bool = True,
) -> float

def full_risk_report(
    self,
    returns: List[float],
    benchmark_returns: Optional[List[float]] = None,
) -> RiskMetrics
```

### BlackScholesPricer

```python
def price(
    self,
    option_type: OptionType,
    spot: float,
    strike: float,
    time_to_expiry: float,
    volatility: float,
) -> float

def greeks(
    self,
    option_type: OptionType,
    spot: float,
    strike: float,
    time_to_expiry: float,
    volatility: float,
) -> Greeks

def implied_volatility(
    self,
    market_price: float,
    option_type: OptionType,
    spot: float,
    strike: float,
    time_to_expiry: float,
    initial_sigma: float = 0.3,
    max_iterations: int = 100,
    tolerance: float = 1e-6,
) -> float
```

### TechnicalAnalyzer

```python
def sma(self, prices: List[float], period: int) -> List[Optional[float]]

def ema(self, prices: List[float], period: int) -> List[Optional[float]]

def rsi(self, prices: List[float], period: int = 14) -> List[Optional[float]]

def macd(
    self,
    prices: List[float],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]

def bollinger_bands(
    self,
    prices: List[float],
    period: int = 20,
    num_std: float = 2.0,
) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]

def atr(
    self,
    highs: List[float],
    lows: List[float],
    closes: List[float],
    period: int = 14,
) -> List[Optional[float]]

def obv(
    self,
    closes: List[float],
    volumes: List[float],
) -> List[float]

def composite_signal(self, prices: List[float]) -> SignalStrength
```

### FundamentalAnalyzer

```python
def compute_composite_score(
    self,
    statement: FinancialStatement,
    growth_rate: float = 0.0,
    pe_ratio: Optional[float] = None,
) -> Dict[str, Any]
```

### BacktestEngine

```python
def run(
    self,
    strategy: Strategy,
    data: List[MarketData],
) -> BacktestResult
```

### MonteCarloSimulator

```python
def simulate_portfolio_paths(
    self,
    initial_value: float,
    expected_return: float,
    volatility: float,
    days: int,
    num_simulations: int = 10_000,
) -> Dict[str, Any]

def simulate_option_payoff(
    self,
    option_type: OptionType,
    spot: float,
    strike: float,
    time_to_expiry: float,
    volatility: float,
    risk_free_rate: float,
    num_simulations: int = 10_000,
) -> Dict[str, Any]
```

### FixedIncomeAnalyzer

```python
def price_bond(self, bond: Bond, market_yield: float) -> float

def macaulay_duration(self, bond: Bond, market_yield: float) -> float

def modified_duration(self, bond: Bond, market_yield: float) -> float

def convexity(self, bond: Bond, market_yield: float) -> float

def interpolate_yield(
    self,
    curve: List[YieldCurvePoint],
    target_maturity: float,
) -> float
```

### RegimeDetector

```python
def detect(self, returns: List[float]) -> MarketRegime

def regime_history(
    self,
    returns: List[float],
    window: int = 60,
) -> List[Dict[str, Any]]
```

---

## Operational Guidelines

### When to Use Each Component

| Scenario | Component | Key Method |
|----------|-----------|------------|
| Evaluate a trading strategy | BacktestEngine | `run(strategy, data)` |
| Check portfolio risk | RiskAnalyzer | `full_risk_report()` |
| Price an option | BlackScholesPricer | `price()`, `greeks()` |
| Analyze stock fundamentals | FundamentalAnalyzer | `compute_composite_score()` |
| Generate trading signals | TechnicalAnalyzer | `composite_signal()` |
| Project portfolio growth | MonteCarloSimulator | `simulate_portfolio_paths()` |
| Assess bond investment | FixedIncomeAnalyzer | `price_bond()`, `duration()` |
| Detect market conditions | RegimeDetector | `detect()` |

### Decision Framework

1. **Define the problem**: What are we trying to measure or optimize?
2. **Select the right tools**: Which analyzers and metrics apply?
3. **Gather inputs**: What data do we need? What are its quality characteristics?
4. **Run analysis**: Execute computations with appropriate methods.
5. **Interpret results**: What do the numbers mean in context?
6. **Stress test**: What happens under adverse conditions?
7. **Document**: Record methodology, assumptions, and results.

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

## Security Considerations

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

## Scalability

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

## Design Patterns

### Strategy Pattern

Trading strategies implement a common protocol:

```python
class Strategy(Protocol):
    def name(self) -> str: ...
    def generate_signals(
        self, data: List[MarketData], context: Dict[str, Any]
    ) -> Dict[str, SignalStrength]: ...
```

### Protocol Pattern

Data sources implement the `DataSource` protocol for pluggability:

```python
class DataSource(Protocol):
    def get_historical(self, symbol: str, days: int) -> List[MarketData]: ...
    def get_current(self, symbol: str) -> MarketData: ...
```

### Immutability

`Trade` objects are `frozen=True` dataclasses — once executed, records cannot be mutated.

### Composition over Inheritance

Components are composed, not inherited:
- `BacktestEngine` contains a `PortfolioManager` and `RiskAnalyzer`
- `PortfolioManager` uses `Position` objects
- `RiskAnalyzer` operates on raw return series

---

## Checklists

### Pre-Trade Checklist

- [ ] Position size within risk limits
- [ ] Stop-loss level defined
- [ ] Entry signal confirmed by indicator
- [ ] No conflicting positions
- [ ] Sufficient cash/margin available
- [ ] Commission and slippage accounted

### Risk Report Checklist

- [ ] VaR computed at 95% and 99%
- [ ] CVaR (Expected Shortfall) calculated
- [ ] Sharpe and Sortino ratios computed
- [ ] Maximum drawdown identified
- [ ] Beta and alpha vs benchmark
- [ ] Stress test scenarios run
- [ ] Correlation matrix reviewed

### Strategy Backtest Checklist

- [ ] No look-ahead bias
- [ ] Transaction costs included
- [ ] Slippage modeled
- [ ] Out-of-sample testing performed
- [ ] Overfitting assessed (train/test split)
- [ ] Multiple market regimes tested
- [ ] Robustness to parameter variation

---

## Troubleshooting

### Common Issues

**VaR is negative or zero**
- Check that returns are non-empty
- Ensure returns are not all identical (zero variance)
- Verify confidence level is between 0 and 1

**Black-Scholes returns extreme values**
- Check time_to_expiry is in years, not days
- Ensure volatility is annualized (0.2 = 20%, not 20)
- Verify spot and strike are positive

**Backtest shows unrealistic returns**
- May be overfitting — try different parameter sets
- Check for look-ahead bias in data alignment
- Verify transaction costs are realistic

**Implied volatility doesn't converge**
- Market price may be below intrinsic value (arbitrage)
- Try different starting sigma (default 0.3)
- Check option parameters are correct

**Portfolio weights don't sum to 1.0**
- Include cash in weight calculation
- Check for rounding errors
- Verify all positions are tracked

### Performance Tips

- Use `RiskModel.PARAMETRIC` for faster VaR when returns are approximately normal
- Cache SMA/EMA calculations for overlapping windows
- Use `MonteCarloSimulator(seed=...)` for reproducible results
- Reduce `num_simulations` for quick estimates, increase for precision

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed risk metrics
metrics = ra.full_risk_report(returns)
print(f"VaR 95%: {metrics.var_95:.4f}")
print(f"Sharpe: {metrics.sharpe_ratio:.4f}")
```

---

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| Yahoo Finance | REST API | Market data |
| Alpha Vantage | REST API | Fundamental data |
| Interactive Brokers | API | Trade execution |
| Bloomberg | BQL | Professional data |
| Quandl | REST API | Alternative data |
| FRED | REST API | Economic data |

---

## Examples

### Daily Portfolio Review

```python
# 1. Update prices
pm.update_prices(latest_prices)

# 2. Check risk
returns = [r for _, r in pm.daily_values[-252:]]
metrics = ra.full_risk_report(returns)

# 3. Check regime
regime = rd.detect(returns)

# 4. Generate report
summary = pm.get_performance_summary()
```

### Strategy Development Cycle

```python
# 1. Implement strategy
class MyStrategy(Strategy):
    def generate_signals(self, data, context):
        # Your logic
        return signals

# 2. Backtest
result = engine.run(MyStrategy(), historical_data)

# 3. Analyze
if result.sharpe_ratio > 1.5 and result.max_drawdown < 0.15:
    print("Strategy is viable")

# 4. Stress test
# Run on different market regimes
```

### Options Analysis Workflow

```python
# 1. Price the option
price = bs.price(OptionType.CALL, spot, strike, tte, vol)

# 2. Get Greeks for hedging
greeks = bs.greeks(OptionType.CALL, spot, strike, tte, vol)

# 3. Check implied vol vs historical
iv = bs.implied_volatility(market_price, OptionType.CALL, spot, strike, tte)
hist_vol = ra.calculate_volatility(returns)
if iv > hist_vol * 1.2:
    print("Option appears overpriced")
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

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[README.md](./README.md) for quick start and API reference.