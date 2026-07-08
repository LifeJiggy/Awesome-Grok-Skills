"""
Finance Agent — Comprehensive financial analysis, portfolio management,
risk assessment, trading strategies, derivatives pricing, and quantitative modeling.

This module provides production-grade financial computations including:
- Portfolio construction and optimization (mean-variance, Black-Litterman)
- Risk metrics (VaR, CVaR, Sharpe, Sortino, maximum drawdown)
- Options pricing (Black-Scholes, binomial trees, Monte Carlo)
- Fixed income analytics (duration, convexity, yield curves)
- Technical indicators and signal generation
- Fundamental analysis scoring
- Backtesting framework for trading strategies
- Stress testing and scenario analysis
"""

from __future__ import annotations

import logging
import math
import statistics
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"
    SHORT = "short"
    COVER = "cover"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"
    ICEBERG = "iceberg"


class AssetClass(Enum):
    EQUITY = "equity"
    FIXED_INCOME = "fixed_income"
    COMMODITY = "commodity"
    CURRENCY = "currency"
    CRYPTO = "crypto"
    REAL_ESTATE = "real_estate"
    ALTERNATIVE = "alternative"


class RiskModel(Enum):
    HISTORICAL = "historical"
    PARAMETRIC = "parametric"
    MONTE_CARLO = "monte_carlo"
    EXPONENTIAL_WEIGHTED = "exponential_weighted"


class MarketRegime(Enum):
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"
    CRISIS = "crisis"


class OptionType(Enum):
    CALL = "call"
    PUT = "put"


class OptionStyle(Enum):
    AMERICAN = "american"
    EUROPEAN = "european"


class Greeks(NamedTuple):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


class SignalStrength(IntEnum):
    STRONG_SELL = -2
    SELL = -1
    NEUTRAL = 0
    BUY = 1
    STRONG_BUY = 2


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Trade:
    """Immutable trade record."""
    trade_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: datetime
    commission: float = 0.0
    slippage: float = 0.0

    @property
    def notional(self) -> float:
        return self.quantity * self.price

    @property
    def total_cost(self) -> float:
        multiplier = 1 if self.side in (OrderSide.BUY, OrderSide.SHORT) else -1
        return multiplier * self.notional + self.commission + self.slippage


@dataclass
class Position:
    """Tracks current holdings for a single instrument."""
    symbol: str
    asset_class: AssetClass
    quantity: float = 0.0
    avg_entry_price: float = 0.0
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0
    last_updated: datetime = field(default_factory=datetime.utcnow)

    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def cost_basis(self) -> float:
        return self.quantity * self.avg_entry_price

    def update_price(self, price: float) -> None:
        self.current_price = price
        self.unrealized_pnl = self.quantity * (price - self.avg_entry_price)
        self.last_updated = datetime.utcnow()


@dataclass
class MarketData:
    """OHLCV bar with optional derived fields."""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None

    @property
    def typical_price(self) -> float:
        return (self.high + self.low + self.close) / 3.0

    @property
    def mid_price(self) -> float:
        return (self.high + self.low) / 2.0

    @property
    def range_pct(self) -> float:
        if self.low == 0:
            return 0.0
        return (self.high - self.low) / self.low * 100.0


@dataclass
class FinancialStatement:
    """Simplified financial statement snapshot."""
    symbol: str
    period_end: datetime
    revenue: float = 0.0
    cost_of_goods_sold: float = 0.0
    operating_income: float = 0.0
    net_income: float = 0.0
    total_assets: float = 0.0
    total_liabilities: float = 0.0
    shareholders_equity: float = 0.0
    operating_cash_flow: float = 0.0
    free_cash_flow: float = 0.0
    current_assets: float = 0.0
    current_liabilities: float = 0.0
    long_term_debt: float = 0.0
    shares_outstanding: float = 0.0
    interest_expense: float = 0.0

    @property
    def gross_margin(self) -> float:
        if self.revenue == 0:
            return 0.0
        return (self.revenue - self.cost_of_goods_sold) / self.revenue

    @property
    def net_margin(self) -> float:
        if self.revenue == 0:
            return 0.0
        return self.net_income / self.revenue

    @property
    def roe(self) -> float:
        if self.shareholders_equity == 0:
            return 0.0
        return self.net_income / self.shareholders_equity

    @property
    def roa(self) -> float:
        if self.total_assets == 0:
            return 0.0
        return self.net_income / self.total_assets

    @property
    def debt_to_equity(self) -> float:
        if self.shareholders_equity == 0:
            return float('inf')
        return self.total_liabilities / self.shareholders_equity

    @property
    def current_ratio(self) -> float:
        if self.current_liabilities == 0:
            return float('inf')
        return self.current_assets / self.current_liabilities


@dataclass
class BacktestResult:
    """Container for backtest output metrics."""
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
    avg_trade_return: float
    avg_holding_days: float
    calmar_ratio: float = 0.0
    recovery_factor: float = 0.0


@dataclass
class RiskMetrics:
    """Aggregated risk metrics for a portfolio or position."""
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    volatility_annualized: float
    beta: float
    alpha: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    tracking_error: float
    information_ratio: float
    correlation_to_market: float


@dataclass
class YieldCurvePoint:
    """Single point on a yield curve."""
    tenor_years: float
    yield_pct: float
    instrument: str = "treasury"


@dataclass
class Bond:
    """Fixed income instrument representation."""
    symbol: str
    coupon_rate: float
    face_value: float
    maturity_date: datetime
    payment_frequency: int = 2  # semi-annual
    current_price: float = 0.0
    ytm: float = 0.0

    @property
    def years_to_maturity(self) -> float:
        delta = self.maturity_date - datetime.utcnow()
        return max(delta.days / 365.25, 0.0)

    @property
    def coupon_payment(self) -> float:
        return self.face_value * self.coupon_rate / self.payment_frequency


# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------

class DataSource(Protocol):
    """Protocol for market data providers."""
    def get_price(self, symbol: str) -> float: ...
    def get_history(self, symbol: str, days: int) -> List[MarketData]: ...


class Strategy(ABC):
    """Base class for all trading strategies."""

    @abstractmethod
    def generate_signals(
        self, data: List[MarketData], context: Dict[str, Any]
    ) -> Dict[str, SignalStrength]:
        ...

    @abstractmethod
    def name(self) -> str:
        ...


# ---------------------------------------------------------------------------
# Portfolio Management
# ---------------------------------------------------------------------------

class PortfolioManager:
    """
    Manages multi-asset portfolios with position tracking, rebalancing,
    and performance attribution.
    """

    def __init__(self, initial_capital: float = 100_000.0) -> None:
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.trade_history: List[Trade] = []
        self.daily_values: List[Tuple[datetime, float]] = []
        self.benchmark_values: List[float] = []
        self._trade_counter = 0
        logger.info("PortfolioManager initialized with capital %.2f", initial_capital)

    @property
    def total_value(self) -> float:
        return self.cash + sum(p.market_value for p in self.positions.values())

    @property
    def total_unrealized_pnl(self) -> float:
        return sum(p.unrealized_pnl for p in self.positions.values())

    @property
    def total_realized_pnl(self) -> float:
        return sum(p.realized_pnl for p in self.positions.values())

    @property
    def invested_value(self) -> float:
        return sum(p.market_value for p in self.positions.values())

    @property
    def cash_weight(self) -> float:
        tv = self.total_value
        return self.cash / tv if tv > 0 else 1.0

    def execute_trade(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        price: float,
        asset_class: AssetClass = AssetClass.EQUITY,
        commission: float = 0.0,
        slippage: float = 0.0,
    ) -> Trade:
        self._trade_counter += 1
        trade = Trade(
            trade_id=f"T{self._trade_counter:06d}",
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            timestamp=datetime.utcnow(),
            commission=commission,
            slippage=slippage,
        )
        cost = trade.total_cost
        if cost > self.cash and side == OrderSide.BUY:
            raise ValueError(
                f"Insufficient cash: need {cost:.2f}, have {self.cash:.2f}"
            )

        self.cash -= cost

        if symbol not in self.positions:
            self.positions[symbol] = Position(
                symbol=symbol, asset_class=asset_class
            )

        pos = self.positions[symbol]
        if side == OrderSide.BUY:
            total_cost = pos.avg_entry_price * pos.quantity + price * quantity
            pos.quantity += quantity
            pos.avg_entry_price = total_cost / pos.quantity if pos.quantity else 0
        elif side == OrderSide.SELL:
            realized = quantity * (price - pos.avg_entry_price)
            pos.realized_pnl += realized
            pos.quantity -= quantity
            if pos.quantity <= 0:
                pos.quantity = 0
                pos.avg_entry_price = 0.0

        pos.update_price(price)
        self.trade_history.append(trade)
        self.daily_values.append((trade.timestamp, self.total_value))
        logger.info("Trade executed: %s %s %.4f @ %.2f", side.value, symbol, quantity, price)
        return trade

    def update_prices(self, prices: Dict[str, float]) -> None:
        for symbol, price in prices.items():
            if symbol in self.positions:
                self.positions[symbol].update_price(price)

    def get_weights(self) -> Dict[str, float]:
        tv = self.total_value
        if tv == 0:
            return {}
        weights = {"CASH": self.cash / tv}
        for sym, pos in self.positions.items():
            if pos.quantity > 0:
                weights[sym] = pos.market_value / tv
        return weights

    def get_performance_summary(self) -> Dict[str, Any]:
        total_ret = (self.total_value - self.initial_capital) / self.initial_capital
        returns = self._daily_returns()
        ann_ret = 0.0
        ann_vol = 0.0
        sharpe = 0.0
        sortino = 0.0
        max_dd = 0.0

        if len(returns) >= 2:
            ann_ret = statistics.mean(returns) * 252
            ann_vol = statistics.stdev(returns) * math.sqrt(252)
            if ann_vol > 0:
                sharpe = ann_ret / ann_vol
            downside = [r for r in returns if r < 0]
            if len(downside) >= 2:
                downside_vol = statistics.stdev(downside) * math.sqrt(252)
                sortino = ann_ret / downside_vol if downside_vol > 0 else 0.0
            max_dd = self._max_drawdown()

        return {
            "total_value": self.total_value,
            "total_return_pct": total_ret * 100,
            "annualized_return_pct": ann_ret * 100,
            "annualized_volatility_pct": ann_vol * 100,
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "max_drawdown_pct": max_dd * 100,
            "total_trades": len(self.trade_history),
            "cash": self.cash,
            "invested": self.invested_value,
            "unrealized_pnl": self.total_unrealized_pnl,
            "realized_pnl": self.total_realized_pnl,
        }

    def _daily_returns(self) -> List[float]:
        if len(self.daily_values) < 2:
            return []
        vals = [v for _, v in self.daily_values]
        return [(vals[i] - vals[i - 1]) / vals[i - 1] for i in range(1, len(vals)) if vals[i - 1] != 0]

    def _max_drawdown(self) -> float:
        vals = [v for _, v in self.daily_values]
        if not vals:
            return 0.0
        peak = vals[0]
        max_dd = 0.0
        for v in vals:
            if v > peak:
                peak = v
            dd = (peak - v) / peak if peak > 0 else 0
            max_dd = max(max_dd, dd)
        return max_dd


# ---------------------------------------------------------------------------
# Risk Analytics
# ---------------------------------------------------------------------------

class RiskAnalyzer:
    """
    Computes portfolio and position-level risk metrics including VaR,
    CVaR, volatility, drawdown, factor exposure, and stress scenarios.
    """

    def __init__(
        self,
        risk_free_rate: float = 0.05,
        confidence_levels: Tuple[float, ...] = (0.95, 0.99),
    ) -> None:
        self.risk_free_rate = risk_free_rate
        self.confidence_levels = confidence_levels
        logger.info("RiskAnalyzer initialized (rf=%.4f)", risk_free_rate)

    def calculate_var(
        self,
        returns: List[float],
        confidence: float = 0.95,
        method: RiskModel = RiskModel.HISTORICAL,
        **kwargs: Any,
    ) -> float:
        if not returns:
            return 0.0

        if method == RiskModel.HISTORICAL:
            sorted_ret = sorted(returns)
            idx = int((1 - confidence) * len(sorted_ret))
            idx = max(0, min(idx, len(sorted_ret) - 1))
            return -sorted_ret[idx]

        elif method == RiskModel.PARAMETRIC:
            mu = statistics.mean(returns)
            sigma = statistics.stdev(returns) if len(returns) > 1 else 0
            z = self._norm_ppf(1 - confidence)
            return -(mu + z * sigma)

        elif method == RiskModel.EXPONENTIAL_WEIGHTED:
            decay = kwargs.get("decay", 0.94)
            weights = [decay ** i for i in range(len(returns))]
            weights.reverse()
            total_w = sum(weights)
            weights = [w / total_w for w in weights]
            mu = sum(w * r for w, r in zip(weights, returns))
            var_w = sum(w * (r - mu) ** 2 for w, r in zip(weights, returns))
            sigma = math.sqrt(var_w)
            z = self._norm_ppf(1 - confidence)
            return -(mu + z * sigma)

        else:
            return self.calculate_var(
                returns, confidence, RiskModel.HISTORICAL
            )

    def calculate_cvar(
        self, returns: List[float], confidence: float = 0.95
    ) -> float:
        if not returns:
            return 0.0
        sorted_ret = sorted(returns)
        cutoff = int((1 - confidence) * len(sorted_ret))
        cutoff = max(1, cutoff)
        tail = sorted_ret[:cutoff]
        return -statistics.mean(tail) if tail else 0.0

    def calculate_volatility(
        self,
        returns: List[float],
        annualize: bool = True,
        window: Optional[int] = None,
    ) -> float:
        if window:
            returns = returns[-window:]
        if len(returns) < 2:
            return 0.0
        vol = statistics.stdev(returns)
        if annualize:
            vol *= math.sqrt(252)
        return vol

    def calculate_beta(
        self,
        asset_returns: List[float],
        market_returns: List[float],
    ) -> float:
        if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
            return 0.0
        cov = self._covariance(asset_returns, market_returns)
        var_m = self._variance(market_returns)
        return cov / var_m if var_m != 0 else 0.0

    def calculate_alpha(
        self,
        asset_returns: List[float],
        market_returns: List[float],
    ) -> float:
        beta = self.calculate_beta(asset_returns, market_returns)
        ann_asset = statistics.mean(asset_returns) * 252
        ann_market = statistics.mean(market_returns) * 252
        return ann_asset - (self.risk_free_rate + beta * (ann_market - self.risk_free_rate))

    def calculate_sharpe(self, returns: List[float]) -> float:
        if not returns:
            return 0.0
        ann_ret = statistics.mean(returns) * 252
        ann_vol = self.calculate_volatility(returns, annualize=True)
        if ann_vol == 0:
            return 0.0
        return (ann_ret - self.risk_free_rate) / ann_vol

    def calculate_sortino(self, returns: List[float]) -> float:
        if not returns:
            return 0.0
        ann_ret = statistics.mean(returns) * 252
        downside = [r for r in returns if r < 0]
        if len(downside) < 2:
            return 0.0
        downside_vol = statistics.stdev(downside) * math.sqrt(252)
        if downside_vol == 0:
            return 0.0
        return (ann_ret - self.risk_free_rate) / downside_vol

    def calculate_max_drawdown(
        self, equity_curve: List[float]
    ) -> Tuple[float, int]:
        if not equity_curve:
            return 0.0, 0
        peak = equity_curve[0]
        max_dd = 0.0
        dd_start = 0
        max_dd_duration = 0
        current_dd_start = 0

        for i, val in enumerate(equity_curve):
            if val >= peak:
                peak = val
                duration = i - current_dd_start
                max_dd_duration = max(max_dd_duration, duration)
                current_dd_start = i
            else:
                dd = (peak - val) / peak if peak > 0 else 0
                if dd > max_dd:
                    max_dd = dd
                    dd_start = current_dd_start

        return max_dd, max_dd_duration

    def calculate_tracking_error(
        self,
        portfolio_returns: List[float],
        benchmark_returns: List[float],
    ) -> float:
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) < 2:
            return 0.0
        active = [p - b for p, b in zip(portfolio_returns, benchmark_returns)]
        return statistics.stdev(active) * math.sqrt(252)

    def calculate_information_ratio(
        self,
        portfolio_returns: List[float],
        benchmark_returns: List[float],
    ) -> float:
        te = self.calculate_tracking_error(portfolio_returns, benchmark_returns)
        if te == 0:
            return 0.0
        active_return = (
            statistics.mean(portfolio_returns) - statistics.mean(benchmark_returns)
        ) * 252
        return active_return / te

    def stress_test(
        self,
        positions: Dict[str, Position],
        scenarios: List[Dict[str, float]],
    ) -> List[Dict[str, Any]]:
        results = []
        for scenario in scenarios:
            scenario_pnl = 0.0
            details = {}
            for sym, pos in positions.items():
                shock = scenario.get(sym, scenario.get("default", 0.0))
                pnl = pos.quantity * pos.current_price * shock
                scenario_pnl += pnl
                details[sym] = {"shock_pct": shock * 100, "pnl": pnl}
            results.append({
                "scenario_pnl": scenario_pnl,
                "details": details,
            })
        return results

    def full_risk_report(
        self,
        returns: List[float],
        benchmark_returns: Optional[List[float]] = None,
        equity_curve: Optional[List[float]] = None,
    ) -> RiskMetrics:
        if equity_curve is None:
            equity_curve = list(returns)
        max_dd, _ = self.calculate_max_drawdown(equity_curve)
        beta = 0.0
        alpha = 0.0
        te = 0.0
        ir = 0.0
        corr = 0.0
        if benchmark_returns and len(benchmark_returns) == len(returns):
            beta = self.calculate_beta(returns, benchmark_returns)
            alpha = self.calculate_alpha(returns, benchmark_returns)
            te = self.calculate_tracking_error(returns, benchmark_returns)
            ir = self.calculate_information_ratio(returns, benchmark_returns)
            corr = self._correlation(returns, benchmark_returns)

        return RiskMetrics(
            var_95=self.calculate_var(returns, 0.95),
            var_99=self.calculate_var(returns, 0.99),
            cvar_95=self.calculate_cvar(returns, 0.95),
            cvar_99=self.calculate_cvar(returns, 0.99),
            volatility_annualized=self.calculate_volatility(returns),
            beta=beta,
            alpha=alpha,
            sharpe_ratio=self.calculate_sharpe(returns),
            sortino_ratio=self.calculate_sortino(returns),
            max_drawdown=max_dd,
            tracking_error=te,
            information_ratio=ir,
            correlation_to_market=corr,
        )

    @staticmethod
    def _norm_ppf(p: float) -> float:
        if p <= 0:
            return -4.0
        if p >= 1:
            return 4.0
        if p == 0.5:
            return 0.0
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308
        t = math.sqrt(-2 * math.log(1 - p)) if p < 0.5 else math.sqrt(-2 * math.log(p))
        x = t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)
        return x if p >= 0.5 else -x

    @staticmethod
    def _variance(data: List[float]) -> float:
        n = len(data)
        if n < 2:
            return 0.0
        mean = statistics.mean(data)
        return sum((x - mean) ** 2 for x in data) / (n - 1)

    @staticmethod
    def _covariance(x: List[float], y: List[float]) -> float:
        n = len(x)
        if n < 2:
            return 0.0
        mx, my = statistics.mean(x), statistics.mean(y)
        return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - 1)

    @staticmethod
    def _correlation(x: List[float], y: List[float]) -> float:
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        sx = statistics.stdev(x)
        sy = statistics.stdev(y)
        if sx == 0 or sy == 0:
            return 0.0
        n = len(x)
        mx, my = statistics.mean(x), statistics.mean(y)
        cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - 1)
        return cov / (sx * sy)


# ---------------------------------------------------------------------------
# Derivatives Pricing
# ---------------------------------------------------------------------------

class BlackScholesPricer:
    """
    Black-Scholes option pricing with Greeks computation.
    Supports European calls and puts.
    """

    def __init__(self, risk_free_rate: float = 0.05) -> None:
        self.risk_free_rate = risk_free_rate

    def price(
        self,
        option_type: OptionType,
        spot: float,
        strike: float,
        time_to_expiry: float,
        volatility: float,
    ) -> float:
        d1, d2 = self._d1_d2(spot, strike, time_to_expiry, volatility)
        if option_type == OptionType.CALL:
            return spot * self._norm_cdf(d1) - strike * math.exp(
                -self.risk_free_rate * time_to_expiry
            ) * self._norm_cdf(d2)
        else:
            return strike * math.exp(
                -self.risk_free_rate * time_to_expiry
            ) * self._norm_cdf(-d2) - spot * self._norm_cdf(-d1)

    def greeks(
        self,
        option_type: OptionType,
        spot: float,
        strike: float,
        time_to_expiry: float,
        volatility: float,
    ) -> Greeks:
        d1, d2 = self._d1_d2(spot, strike, time_to_expiry, volatility)
        exp_neg_rt = math.exp(-self.risk_free_rate * time_to_expiry)
        sqrt_t = math.sqrt(time_to_expiry)
        pdf_d1 = self._norm_pdf(d1)

        delta = self._norm_cdf(d1) if option_type == OptionType.CALL else self._norm_cdf(d1) - 1
        gamma = pdf_d1 / (spot * volatility * sqrt_t) if (spot * volatility * sqrt_t) != 0 else 0
        vega = spot * pdf_d1 * sqrt_t / 100.0

        if option_type == OptionType.CALL:
            theta = (
                -spot * pdf_d1 * volatility / (2 * sqrt_t)
                - self.risk_free_rate * strike * exp_neg_rt * self._norm_cdf(d2)
            ) / 365.0
        else:
            theta = (
                -spot * pdf_d1 * volatility / (2 * sqrt_t)
                + self.risk_free_rate * strike * exp_neg_rt * self._norm_cdf(-d2)
            ) / 365.0

        if option_type == OptionType.CALL:
            rho = strike * time_to_expiry * exp_neg_rt * self._norm_cdf(d2) / 100.0
        else:
            rho = -strike * time_to_expiry * exp_neg_rt * self._norm_cdf(-d2) / 100.0

        return Greeks(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)

    def implied_volatility(
        self,
        market_price: float,
        option_type: OptionType,
        spot: float,
        strike: float,
        time_to_expiry: float,
        tol: float = 1e-6,
        max_iter: int = 100,
    ) -> float:
        sigma = 0.3
        for _ in range(max_iter):
            price = self.price(option_type, spot, strike, time_to_expiry, sigma)
            diff = price - market_price
            if abs(diff) < tol:
                return sigma
            d1, _ = self._d1_d2(spot, strike, time_to_expiry, sigma)
            vega = spot * self._norm_pdf(d1) * math.sqrt(time_to_expiry)
            if vega == 0:
                break
            sigma -= diff / vega
            sigma = max(sigma, 0.001)
        return sigma

    def _d1_d2(
        self, spot: float, strike: float, t: float, sigma: float
    ) -> Tuple[float, float]:
        if sigma <= 0 or t <= 0 or spot <= 0 or strike <= 0:
            return 0.0, 0.0
        d1 = (math.log(spot / strike) + (self.risk_free_rate + 0.5 * sigma ** 2) * t) / (
            sigma * math.sqrt(t)
        )
        d2 = d1 - sigma * math.sqrt(t)
        return d1, d2

    @staticmethod
    def _norm_cdf(x: float) -> float:
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    @staticmethod
    def _norm_pdf(x: float) -> float:
        return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


# ---------------------------------------------------------------------------
# Technical Analysis
# ---------------------------------------------------------------------------

class TechnicalAnalyzer:
    """
    Technical indicator library for market data analysis.
    Provides SMA, EMA, RSI, MACD, Bollinger Bands, ATR, OBV, and composite scoring.
    """

    @staticmethod
    def sma(prices: List[float], period: int) -> List[Optional[float]]:
        result: List[Optional[float]] = []
        for i in range(len(prices)):
            if i < period - 1:
                result.append(None)
            else:
                window = prices[i - period + 1 : i + 1]
                result.append(sum(window) / period)
        return result

    @staticmethod
    def ema(prices: List[float], period: int) -> List[Optional[float]]:
        if not prices:
            return []
        k = 2 / (period + 1)
        result: List[Optional[float]] = [prices[0]]
        for i in range(1, len(prices)):
            val = prices[i] * k + result[-1] * (1 - k)  # type: ignore
            result.append(val)
        return result

    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> List[Optional[float]]:
        if len(prices) < period + 1:
            return [None] * len(prices)
        result: List[Optional[float]] = [None] * period
        gains = []
        losses = []
        for i in range(1, period + 1):
            change = prices[i] - prices[i - 1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        result.append(100 - 100 / (1 + rs))

        for i in range(period + 1, len(prices)):
            change = prices[i] - prices[i - 1]
            gain = max(change, 0)
            loss = max(-change, 0)
            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period
            rs = avg_gain / avg_loss if avg_loss != 0 else 100
            result.append(100 - 100 / (1 + rs))
        return result

    @staticmethod
    def macd(
        prices: List[float],
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ) -> Tuple[List[float], List[float], List[float]]:
        def _ema(data: List[float], period: int) -> List[float]:
            if not data:
                return []
            k = 2 / (period + 1)
            result = [data[0]]
            for i in range(1, len(data)):
                result.append(data[i] * k + result[-1] * (1 - k))
            return result

        ema_fast = _ema(prices, fast)
        ema_slow = _ema(prices, slow)
        macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
        signal_line = _ema(macd_line, signal)
        histogram = [m - s for m, s in zip(macd_line, signal_line)]
        return macd_line, signal_line, histogram

    @staticmethod
    def bollinger_bands(
        prices: List[float], period: int = 20, num_std: float = 2.0
    ) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
        upper: List[Optional[float]] = []
        middle: List[Optional[float]] = []
        lower: List[Optional[float]] = []
        for i in range(len(prices)):
            if i < period - 1:
                upper.append(None)
                middle.append(None)
                lower.append(None)
            else:
                window = prices[i - period + 1 : i + 1]
                avg = sum(window) / period
                std = statistics.stdev(window) if len(window) > 1 else 0
                middle.append(avg)
                upper.append(avg + num_std * std)
                lower.append(avg - num_std * std)
        return upper, middle, lower

    @staticmethod
    def atr(
        highs: List[float], lows: List[float], closes: List[float], period: int = 14
    ) -> List[Optional[float]]:
        if len(highs) < 2:
            return [None] * len(highs)
        tr_list: List[float] = [highs[0] - lows[0]]
        for i in range(1, len(highs)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i - 1]),
                abs(lows[i] - closes[i - 1]),
            )
            tr_list.append(tr)
        result: List[Optional[float]] = [None] * (period - 1)
        atr_val = sum(tr_list[:period]) / period
        result.append(atr_val)
        for i in range(period, len(tr_list)):
            atr_val = (atr_val * (period - 1) + tr_list[i]) / period
            result.append(atr_val)
        return result

    @staticmethod
    def obv(closes: List[float], volumes: List[int]) -> List[float]:
        if not closes:
            return []
        result = [0.0]
        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                result.append(result[-1] + volumes[i])
            elif closes[i] < closes[i - 1]:
                result.append(result[-1] - volumes[i])
            else:
                result.append(result[-1])
        return result

    def composite_signal(
        self, prices: List[float], volumes: Optional[List[int]] = None
    ) -> SignalStrength:
        if len(prices) < 50:
            return SignalStrength.NEUTRAL

        score = 0
        rsi_vals = self.rsi(prices, 14)
        rsi_val = rsi_vals[-1] if rsi_vals[-1] is not None else 50
        if rsi_val < 30:
            score += 1
        elif rsi_val > 70:
            score -= 1

        ema_vals = self.ema(prices, 20)
        if ema_vals[-1] is not None and ema_vals[-2] is not None:
            if prices[-1] > ema_vals[-1]:
                score += 1
            else:
                score -= 1

        _, _, hist = self.macd(prices)
        if len(hist) >= 2:
            if hist[-1] > 0 and hist[-2] <= 0:
                score += 1
            elif hist[-1] < 0 and hist[-2] >= 0:
                score -= 1

        upper, middle, lower = self.bollinger_bands(prices)
        if lower[-1] is not None and upper[-1] is not None:
            if prices[-1] < lower[-1]:
                score += 1
            elif prices[-1] > upper[-1]:
                score -= 1

        if score >= 2:
            return SignalStrength.STRONG_BUY
        elif score == 1:
            return SignalStrength.BUY
        elif score <= -2:
            return SignalStrength.STRONG_SELL
        elif score == -1:
            return SignalStrength.SELL
        return SignalStrength.NEUTRAL


# ---------------------------------------------------------------------------
# Fundamental Analysis
# ---------------------------------------------------------------------------

class FundamentalAnalyzer:
    """
    Fundamental analysis scoring based on financial statement ratios
    and valuation metrics.
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None) -> None:
        self.weights = weights or {
            "profitability": 0.25,
            "growth": 0.20,
            "valuation": 0.20,
            "financial_health": 0.20,
            "efficiency": 0.15,
        }

    def score_profitability(self, stmt: FinancialStatement) -> float:
        scores = []
        gm = stmt.gross_margin
        scores.append(min(max((gm - 0.2) / 0.5, 0), 1))
        nm = stmt.net_margin
        scores.append(min(max((nm - 0.05) / 0.25, 0), 1))
        roe = stmt.roe
        scores.append(min(max(roe / 0.3, 0), 1))
        return statistics.mean(scores) if scores else 0

    def score_financial_health(self, stmt: FinancialStatement) -> float:
        scores = []
        cr = stmt.current_ratio
        scores.append(min(max(cr / 3.0, 0), 1))
        de = stmt.debt_to_equity
        scores.append(min(max(1 - de / 3.0, 0), 1))
        return statistics.mean(scores) if scores else 0

    def score_efficiency(self, stmt: FinancialStatement) -> float:
        if stmt.total_assets == 0:
            return 0
        asset_turnover = stmt.revenue / stmt.total_assets
        return min(max(asset_turnover / 2.0, 0), 1)

    def compute_composite_score(
        self, stmt: FinancialStatement, growth_rate: float = 0.0, pe_ratio: float = 0.0
    ) -> Dict[str, Any]:
        profitability = self.score_profitability(stmt)
        health = self.score_financial_health(stmt)
        efficiency = self.score_efficiency(stmt)
        growth_score = min(max(growth_rate / 0.3, 0), 1)
        valuation_score = 0.5
        if pe_ratio > 0:
            valuation_score = min(max(1 - pe_ratio / 50, 0), 1)

        composite = (
            self.weights["profitability"] * profitability
            + self.weights["growth"] * growth_score
            + self.weights["valuation"] * valuation_score
            + self.weights["financial_health"] * health
            + self.weights["efficiency"] * efficiency
        )

        return {
            "composite_score": composite,
            "profitability": profitability,
            "growth": growth_score,
            "valuation": valuation_score,
            "financial_health": health,
            "efficiency": efficiency,
            "grade": self._score_to_grade(composite),
        }

    @staticmethod
    def _score_to_grade(score: float) -> str:
        if score >= 0.85:
            return "A+"
        elif score >= 0.75:
            return "A"
        elif score >= 0.65:
            return "B+"
        elif score >= 0.55:
            return "B"
        elif score >= 0.45:
            return "C+"
        elif score >= 0.35:
            return "C"
        else:
            return "D"


# ---------------------------------------------------------------------------
# Fixed Income Analytics
# ---------------------------------------------------------------------------

class FixedIncomeAnalyzer:
    """
    Bond analytics: pricing, duration, convexity, yield-to-maturity,
    and yield curve interpolation.
    """

    def price_bond(self, bond: Bond, market_yield: float) -> float:
        y = market_yield / bond.payment_frequency
        n = int(bond.years_to_maturity * bond.payment_frequency)
        if n <= 0:
            return bond.face_value
        coupon_pv = sum(
            bond.coupon_payment / (1 + y) ** t for t in range(1, n + 1)
        )
        face_pv = bond.face_value / (1 + y) ** n
        return coupon_pv + face_pv

    def macaulay_duration(self, bond: Bond, market_yield: float) -> float:
        y = market_yield / bond.payment_frequency
        n = int(bond.years_to_maturity * bond.payment_frequency)
        if n <= 0:
            return 0.0
        price = self.price_bond(bond, market_yield)
        if price == 0:
            return 0.0
        weighted = sum(
            t * bond.coupon_payment / (1 + y) ** t for t in range(1, n + 1)
        )
        weighted += n * bond.face_value / (1 + y) ** n
        return weighted / price / bond.payment_frequency

    def modified_duration(self, bond: Bond, market_yield: float) -> float:
        mac_dur = self.macaulay_duration(bond, market_yield)
        y = market_yield / bond.payment_frequency
        return mac_dur / (1 + y)

    def convexity(self, bond: Bond, market_yield: float) -> float:
        y = market_yield / bond.payment_frequency
        n = int(bond.years_to_maturity * bond.payment_frequency)
        if n <= 0:
            return 0.0
        price = self.price_bond(bond, market_yield)
        if price == 0:
            return 0.0
        conv = sum(
            t * (t + 1) * bond.coupon_payment / (1 + y) ** (t + 2)
            for t in range(1, n + 1)
        )
        conv += n * (n + 1) * bond.face_value / (1 + y) ** (n + 2)
        return conv / price / (bond.payment_frequency ** 2)

    def price_change_approx(
        self, bond: Bond, market_yield: float, yield_change: float
    ) -> float:
        mod_dur = self.modified_duration(bond, market_yield)
        conv = self.convexity(bond, market_yield)
        price = self.price_bond(bond, market_yield)
        return price * (-mod_dur * yield_change + 0.5 * conv * yield_change ** 2)

    def interpolate_yield(
        self,
        curve: List[YieldCurvePoint],
        target_tenor: float,
    ) -> float:
        if not curve:
            return 0.0
        sorted_curve = sorted(curve, key=lambda p: p.tenor_years)
        if target_tenor <= sorted_curve[0].tenor_years:
            return sorted_curve[0].yield_pct
        if target_tenor >= sorted_curve[-1].tenor_years:
            return sorted_curve[-1].yield_pct
        for i in range(len(sorted_curve) - 1):
            t1 = sorted_curve[i].tenor_years
            t2 = sorted_curve[i + 1].tenor_years
            if t1 <= target_tenor <= t2:
                frac = (target_tenor - t1) / (t2 - t1) if t2 != t1 else 0
                return sorted_curve[i].yield_pct + frac * (
                    sorted_curve[i + 1].yield_pct - sorted_curve[i].yield_pct
                )
        return sorted_curve[-1].yield_pct


# ---------------------------------------------------------------------------
# Backtesting Engine
# ---------------------------------------------------------------------------

class BacktestEngine:
    """
    Event-driven backtesting engine for evaluating trading strategies
    on historical data.
    """

    def __init__(
        self,
        initial_capital: float = 100_000.0,
        commission_per_trade: float = 1.0,
        slippage_pct: float = 0.001,
    ) -> None:
        self.initial_capital = initial_capital
        self.commission_per_trade = commission_per_trade
        self.slippage_pct = slippage_pct

    def run(
        self,
        strategy: Strategy,
        data: List[MarketData],
        position_size_pct: float = 0.1,
    ) -> BacktestResult:
        portfolio = PortfolioManager(self.initial_capital)
        risk_analyzer = RiskAnalyzer()

        for i, bar in enumerate(data):
            window = data[max(0, i - 100) : i + 1]
            context = {"bar_index": i, "portfolio_value": portfolio.total_value}
            signals = strategy.generate_signals(window, context)

            for sym, signal in signals.items():
                price = bar.close
                if signal in (SignalStrength.BUY, SignalStrength.STRONG_BUY):
                    alloc = portfolio.cash * position_size_pct
                    if alloc > 0 and price > 0:
                        qty = alloc / price
                        slippage = price * self.slippage_pct
                        portfolio.execute_trade(
                            sym, OrderSide.BUY, qty, price + slippage,
                            commission=self.commission_per_trade,
                        )
                elif signal in (SignalStrength.SELL, SignalStrength.STRONG_SELL):
                    if sym in portfolio.positions and portfolio.positions[sym].quantity > 0:
                        qty = portfolio.positions[sym].quantity
                        slippage = price * self.slippage_pct
                        portfolio.execute_trade(
                            sym, OrderSide.SELL, qty, price - slippage,
                            commission=self.commission_per_trade,
                        )

        returns = portfolio._daily_returns()
        equity = [v for _, v in portfolio.daily_values]
        max_dd, dd_dur = risk_analyzer.calculate_max_drawdown(equity)
        win_trades = [
            t for t in portfolio.trade_history if t.side == OrderSide.SELL
        ]
        win_count = sum(
            1 for t in win_trades
            if any(
                prev.side == OrderSide.BUY and prev.symbol == t.symbol
                for prev in portfolio.trade_history
                if prev.timestamp < t.timestamp
            )
        )
        win_rate = win_count / len(win_trades) if win_trades else 0
        ann_ret = statistics.mean(returns) * 252 if returns else 0
        ann_vol = statistics.stdev(returns) * math.sqrt(252) if len(returns) > 1 else 1
        final_val = portfolio.total_value

        return BacktestResult(
            strategy_name=strategy.name(),
            start_date=data[0].timestamp if data else datetime.utcnow(),
            end_date=data[-1].timestamp if data else datetime.utcnow(),
            initial_capital=self.initial_capital,
            final_capital=final_val,
            total_return=(final_val - self.initial_capital) / self.initial_capital,
            annualized_return=ann_ret,
            sharpe_ratio=risk_analyzer.calculate_sharpe(returns),
            sortino_ratio=risk_analyzer.calculate_sortino(returns),
            max_drawdown=max_dd,
            max_drawdown_duration_days=dd_dur,
            win_rate=win_rate,
            profit_factor=0.0,
            total_trades=len(portfolio.trade_history),
            avg_trade_return=0.0,
            avg_holding_days=0.0,
            calmar_ratio=ann_ret / max_dd if max_dd > 0 else 0,
            recovery_factor=(
                (final_val - self.initial_capital) / self.initial_capital / max_dd
                if max_dd > 0
                else 0
            ),
        )


# ---------------------------------------------------------------------------
# Example Strategy Implementations
# ---------------------------------------------------------------------------

class SMACrossStrategy(Strategy):
    """Simple moving average crossover strategy."""

    def __init__(self, fast_period: int = 20, slow_period: int = 50) -> None:
        self.fast_period = fast_period
        self.slow_period = slow_period
        self._ta = TechnicalAnalyzer()

    def name(self) -> str:
        return f"SMA_Cross_{self.fast_period}_{self.slow_period}"

    def generate_signals(
        self, data: List[MarketData], context: Dict[str, Any]
    ) -> Dict[str, SignalStrength]:
        if len(data) < self.slow_period:
            return {}
        closes = [bar.close for bar in data]
        fast = self._ta.sma(closes, self.fast_period)
        slow = self._ta.sma(closes, self.slow_period)
        if fast[-1] is None or slow[-1] is None or fast[-2] is None or slow[-2] is None:
            return {}
        symbol = data[-1].symbol
        if fast[-1] > slow[-1] and fast[-2] <= slow[-2]:
            return {symbol: SignalStrength.STRONG_BUY}
        elif fast[-1] < slow[-1] and fast[-2] >= slow[-2]:
            return {symbol: SignalStrength.STRONG_SELL}
        return {}


class RSIMeanReversionStrategy(Strategy):
    """RSI-based mean reversion strategy."""

    def __init__(self, period: int = 14, oversold: float = 30, overbought: float = 70) -> None:
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        self._ta = TechnicalAnalyzer()

    def name(self) -> str:
        return f"RSI_MeanRev_{self.period}"

    def generate_signals(
        self, data: List[MarketData], context: Dict[str, Any]
    ) -> Dict[str, SignalStrength]:
        if len(data) < self.period + 1:
            return {}
        closes = [bar.close for bar in data]
        rsi_vals = self._ta.rsi(closes, self.period)
        rsi = rsi_vals[-1]
        if rsi is None:
            return {}
        symbol = data[-1].symbol
        if rsi < self.oversold:
            return {symbol: SignalStrength.BUY}
        elif rsi > self.overbought:
            return {symbol: SignalStrength.SELL}
        return {}


# ---------------------------------------------------------------------------
# Monte Carlo Simulation
# ---------------------------------------------------------------------------

class MonteCarloSimulator:
    """Monte Carlo simulation for portfolio projections and risk analysis."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self._seed = seed

    def simulate_portfolio_paths(
        self,
        initial_value: float,
        expected_return: float,
        volatility: float,
        days: int = 252,
        num_simulations: int = 10_000,
    ) -> Dict[str, Any]:
        import random
        rng = random.Random(self._seed)
        final_values: List[float] = []
        all_paths: List[List[float]] = []

        for _ in range(num_simulations):
            path = [initial_value]
            value = initial_value
            for _ in range(days):
                z = rng.gauss(0, 1)
                daily_return = expected_return / 252 + volatility / math.sqrt(252) * z
                value *= 1 + daily_return
                path.append(value)
            final_values.append(value)
            all_paths.append(path)

        final_values.sort()
        n = num_simulations
        return {
            "mean_final": statistics.mean(final_values),
            "median_final": final_values[n // 2],
            "percentile_5": final_values[int(n * 0.05)],
            "percentile_95": final_values[int(n * 0.95)],
            "percentile_1": final_values[int(n * 0.01)],
            "percentile_99": final_values[int(n * 0.99)],
            "probability_of_loss": sum(1 for v in final_values if v < initial_value) / n,
            "expected_shortfall_5": statistics.mean(final_values[:int(n * 0.05)]),
            "paths_sample": [all_paths[i] for i in range(0, n, n // 10)],
        }

    def simulate_option_payoff(
        self,
        option_type: OptionType,
        spot: float,
        strike: float,
        time_to_expiry: float,
        volatility: float,
        risk_free_rate: float,
        num_simulations: int = 10_000,
        seed: Optional[int] = None,
    ) -> Dict[str, float]:
        import random
        rng = random.Random(seed or self._seed)
        payoffs: List[float] = []

        for _ in range(num_simulations):
            z = rng.gauss(0, 1)
            st = spot * math.exp(
                (risk_free_rate - 0.5 * volatility ** 2) * time_to_expiry
                + volatility * math.sqrt(time_to_expiry) * z
            )
            if option_type == OptionType.CALL:
                payoffs.append(max(st - strike, 0))
            else:
                payoffs.append(max(strike - st, 0))

        discount = math.exp(-risk_free_rate * time_to_expiry)
        avg_payoff = statistics.mean(payoffs)
        return {
            "price": avg_payoff * discount,
            "avg_payoff": avg_payoff,
            "probability_itm": sum(1 for p in payoffs if p > 0) / num_simulations,
            "max_payoff": max(payoffs),
            "min_payoff": min(payoffs),
        }


# ---------------------------------------------------------------------------
# Market Regime Detection
# ---------------------------------------------------------------------------

class RegimeDetector:
    """Detects market regimes from historical return series."""

    def __init__(self, lookback: int = 60, vol_threshold: float = 0.25) -> None:
        self.lookback = lookback
        self.vol_threshold = vol_threshold

    def detect(self, returns: List[float]) -> MarketRegime:
        if len(returns) < self.lookback:
            return MarketRegime.SIDEWAYS
        window = returns[-self.lookback :]
        ann_ret = statistics.mean(window) * 252
        ann_vol = statistics.stdev(window) * math.sqrt(252) if len(window) > 1 else 0

        if ann_vol > self.vol_threshold * 1.5:
            return MarketRegime.HIGH_VOLATILITY
        elif ann_vol < self.vol_threshold * 0.5:
            return MarketRegime.LOW_VOLATILITY

        if ann_ret > 0.10:
            return MarketRegime.BULL
        elif ann_ret < -0.10:
            return MarketRegime.BEAR
        return MarketRegime.SIDEWAYS

    def regime_history(
        self, returns: List[float], window: int = 60
    ) -> List[MarketRegime]:
        history: List[MarketRegime] = []
        for i in range(window, len(returns) + 1):
            regime = self.detect(returns[:i])
            history.append(regime)
        return history


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def calculate_compound_annual_growth_rate(
    beginning_value: float, ending_value: float, years: float
) -> float:
    if beginning_value <= 0 or ending_value <= 0 or years <= 0:
        return 0.0
    return (ending_value / beginning_value) ** (1 / years) - 1


def calculate_weighted_average_cost_of_capital(
    equity_value: float,
    debt_value: float,
    cost_of_equity: float,
    cost_of_debt: float,
    tax_rate: float,
) -> float:
    total = equity_value + debt_value
    if total == 0:
        return 0.0
    we = equity_value / total
    wd = debt_value / total
    return we * cost_of_equity + wd * cost_of_debt * (1 - tax_rate)


def discount_cash_flows(
    cash_flows: List[float], discount_rate: float, periods: Optional[List[float]] = None
) -> float:
    if periods is None:
        periods = [float(i + 1) for i in range(len(cash_flows))]
    total = 0.0
    for cf, t in zip(cash_flows, periods):
        if discount_rate >= -1:
            total += cf / (1 + discount_rate) ** t
    return total


def future_value(
    present_value: float, rate: float, periods: float, compounding: int = 1
) -> float:
    return present_value * (1 + rate / compounding) ** (compounding * periods)


def present_value(
    future_value_amount: float, rate: float, periods: float, compounding: int = 1
) -> float:
    return future_value_amount / (1 + rate / compounding) ** (compounding * periods)


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("Finance Agent — Comprehensive Demo")
    print("=" * 60)

    pm = PortfolioManager(initial_capital=250_000)
    pm.execute_trade("AAPL", OrderSide.BUY, 100, 175.0)
    pm.execute_trade("GOOGL", OrderSide.BUY, 50, 140.0)
    pm.execute_trade("MSFT", OrderSide.BUY, 80, 330.0)
    pm.execute_trade("AMZN", OrderSide.BUY, 40, 180.0)
    pm.execute_trade("TSLA", OrderSide.BUY, 30, 250.0)
    pm.execute_trade("NVDA", OrderSide.BUY, 60, 450.0)

    pm.update_prices({
        "AAPL": 182.5, "GOOGL": 145.0, "MSFT": 345.0,
        "AMZN": 188.0, "TSLA": 240.0, "NVDA": 480.0,
    })

    perf = pm.get_performance_summary()
    print(f"\nPortfolio Summary:")
    print(f"  Total Value:     ${perf['total_value']:,.2f}")
    print(f"  Cash:            ${perf['cash']:,.2f}")
    print(f"  Invested:        ${perf['invested']:,.2f}")
    print(f"  Unrealized PnL:  ${perf['unrealized_pnl']:,.2f}")
    print(f"  Total Trades:    {perf['total_trades']}")
    print(f"  Weights: {pm.get_weights()}")

    print("\n--- Risk Analysis ---")
    ra = RiskAnalyzer(risk_free_rate=0.05)
    import random
    rng = random.Random(42)
    daily_returns = [rng.gauss(0.0005, 0.015) for _ in range(252)]
    metrics = ra.full_risk_report(daily_returns)
    print(f"  VaR 95%:         {metrics.var_95:.4f}")
    print(f"  VaR 99%:         {metrics.var_99:.4f}")
    print(f"  CVaR 95%:        {metrics.cvar_95:.4f}")
    print(f"  Volatility:      {metrics.volatility_annualized:.4f}")
    print(f"  Sharpe Ratio:    {metrics.sharpe_ratio:.4f}")
    print(f"  Sortino Ratio:   {metrics.sortino_ratio:.4f}")
    print(f"  Max Drawdown:    {metrics.max_drawdown:.4f}")

    print("\n--- Black-Scholes Pricing ---")
    bs = BlackScholesPricer(risk_free_rate=0.05)
    call_price = bs.price(OptionType.CALL, 100, 105, 0.5, 0.2)
    call_greeks = bs.greeks(OptionType.CALL, 100, 105, 0.5, 0.2)
    print(f"  Call Price:  ${call_price:.4f}")
    print(f"  Delta:       {call_greeks.delta:.4f}")
    print(f"  Gamma:       {call_greeks.gamma:.4f}")
    print(f"  Theta:       {call_greeks.theta:.4f}")
    print(f"  Vega:        {call_greeks.vega:.4f}")
    print(f"  Rho:         {call_greeks.rho:.4f}")

    print("\n--- Technical Analysis ---")
    ta = TechnicalAnalyzer()
    sample_prices = [100 + i * 0.5 + rng.gauss(0, 2) for i in range(100)]
    sma20 = ta.sma(sample_prices, 20)
    rsi14 = ta.rsi(sample_prices, 14)
    signal = ta.composite_signal(sample_prices)
    print(f"  SMA(20) last: {sma20[-1]:.2f}")
    print(f"  RSI(14) last: {rsi14[-1]:.2f}")
    print(f"  Composite Signal: {signal.name}")

    print("\n--- Fundamental Analysis ---")
    fa = FundamentalAnalyzer()
    stmt = FinancialStatement(
        symbol="DEMO", period_end=datetime.utcnow(),
        revenue=10_000_000, cost_of_goods_sold=6_000_000,
        operating_income=3_000_000, net_income=2_000_000,
        total_assets=15_000_000, total_liabilities=5_000_000,
        shareholders_equity=10_000_000, current_assets=6_000_000,
        current_liabilities=3_000_000, shares_outstanding=1_000_000,
    )
    score_result = fa.compute_composite_score(stmt, growth_rate=0.15, pe_ratio=22)
    print(f"  Composite Score: {score_result['composite_score']:.3f}")
    print(f"  Grade: {score_result['grade']}")

    print("\n--- Fixed Income ---")
    fi = FixedIncomeAnalyzer()
    bond = Bond(
        symbol="T10Y", coupon_rate=0.045, face_value=1000,
        maturity_date=datetime.utcnow() + timedelta(days=365 * 10),
        current_price=950,
    )
    bond_price = fi.price_bond(bond, 0.05)
    mac_d = fi.macaulay_duration(bond, 0.05)
    mod_d = fi.modified_duration(bond, 0.05)
    conv = fi.convexity(bond, 0.05)
    print(f"  Bond Price:      ${bond_price:.2f}")
    print(f"  Macaulay Dur:    {mac_d:.4f}")
    print(f"  Modified Dur:    {mod_d:.4f}")
    print(f"  Convexity:       {conv:.4f}")

    print("\n--- Monte Carlo ---")
    mc = MonteCarloSimulator(seed=42)
    mc_result = mc.simulate_portfolio_paths(250_000, 0.10, 0.20, days=252)
    print(f"  Mean Final:      ${mc_result['mean_final']:,.2f}")
    print(f"  5th Percentile:  ${mc_result['percentile_5']:,.2f}")
    print(f"  95th Percentile: ${mc_result['percentile_95']:,.2f}")
    print(f"  Prob of Loss:    {mc_result['probability_of_loss']:.2%}")

    print("\n--- Backtest ---")
    engine = BacktestEngine(initial_capital=100_000)
    mock_data = [
        MarketData(
            symbol="TEST", timestamp=datetime.utcnow() - timedelta(days=100 - i),
            open=100 + i * 0.3, high=102 + i * 0.3, low=99 + i * 0.3,
            close=100 + i * 0.3 + rng.gauss(0, 1), volume=1_000_000,
        )
        for i in range(100)
    ]
    bt_result = engine.run(SMACrossStrategy(10, 30), mock_data)
    print(f"  Strategy:        {bt_result.strategy_name}")
    print(f"  Total Return:    {bt_result.total_return:.2%}")
    print(f"  Sharpe:          {bt_result.sharpe_ratio:.4f}")
    print(f"  Max Drawdown:    {bt_result.max_drawdown:.2%}")
    print(f"  Total Trades:    {bt_result.total_trades}")

    print("\n--- Regime Detection ---")
    rd = RegimeDetector()
    regime = rd.detect(daily_returns)
    print(f"  Current Regime:  {regime.value}")

    print("\n--- Utility Functions ---")
    cagr = calculate_compound_annual_growth_rate(100_000, 250_000, 5)
    print(f"  CAGR (5yr):      {cagr:.2%}")
    dcf = discount_cash_flows([1000, 1200, 1500, 1800, 2000], 0.08)
    print(f"  DCF Value:       ${dcf:,.2f}")
    fv = future_value(100_000, 0.07, 10)
    print(f"  Future Value:    ${fv:,.2f}")

    print("\n" + "=" * 60)
    print("Finance Agent demo complete.")
    print("=" * 60)
