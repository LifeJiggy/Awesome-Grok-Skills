"""
DeFi Module
AMM operations, liquidity management, yield farming, flash loans, and lending protocol integration.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProtocolType(Enum):
    AMM = "amm"
    LENDING = "lending"
    YIELD = "yield"
    STABLECOIN = "stablecoin"
    DERIVATIVES = "derivatives"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SwapQuote:
    """Result of an AMM swap quote."""
    token_in: str
    token_out: str
    amount_in: float
    amount_out: float
    minimum_out: float
    price_impact: float
    fee: float
    route: List[str] = field(default_factory=list)
    gas_estimate: int = 0
    slippage_tolerance: float = 0.005


@dataclass
class LiquidityPosition:
    """LP token position."""
    pool_address: str
    token0: str
    token1: str
    amount0: float
    amount1: float
    lp_tokens: float
    entry_value_usd: float = 0.0
    current_value_usd: float = 0.0
    fees_earned_usd: float = 0.0


@dataclass
class PoolInfo:
    """AMM pool information."""
    address: str
    token0_symbol: str
    token1_symbol: str
    reserve0: float
    reserve1: float
    lp_supply: float
    fee_tier: float = 0.003
    protocol: str = "uniswap_v2"
    total_value_locked: float = 0.0


@dataclass
class ImpermanentLossResult:
    """Impermanent loss calculation result."""
    entry_price_ratio: float
    current_price_ratio: float
    il_pct: float
    fees_earned: float
    net_return: float
    holding_return: float


@dataclass
class YieldStrategy:
    """Yield farming strategy."""
    name: str
    protocol: str
    apr: float
    tvl: float
    risk_level: RiskLevel
    compound_freq: int = 365
    min_deposit: float = 0.0
    lock_period_days: int = 0

    @property
    def apy(self) -> float:
        if self.compound_freq == 0:
            return self.apr
        return (1 + self.apr / self.compound_freq) ** self.compound_freq - 1


@dataclass
class FlashLoanPlan:
    """Flash loan execution plan."""
    asset: str
    amount: float
    provider: str
    fee_rate: float
    fee: float
    actions: List[Dict[str, Any]] = field(default_factory=list)
    gas_cost: float = 0.0
    projected_profit: float = 0.0


@dataclass
class HealthFactor:
    """Lending protocol health factor."""
    health_factor: float
    collateral_value: float
    borrow_value: float
    liquidation_threshold: float
    max_borrow: float
    current_ltv: float = 0.0


@dataclass
class PriceOracle:
    """Price oracle data point."""
    asset: str
    price: float
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: float = 0.95
    stale: bool = False

    @property
    def age_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self.timestamp).total_seconds()


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

UNISWAP_V2_FEE = 0.003
UNISWAP_V3_FEES = [0.0001, 0.0005, 0.003, 0.01]
AAVE_FLASH_LOAN_FEE = 0.0009
AAVE_LIQUIDATION_THRESHOLD = 0.825
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"


# ---------------------------------------------------------------------------
# AMM Router
# ---------------------------------------------------------------------------

class AMMRouter:
    """Automated Market Maker router for token swaps."""

    def __init__(
        self,
        protocol: str = "uniswap_v2",
        fee_tier: float = UNISWAP_V2_FEE,
    ):
        self.protocol = protocol
        self.fee_tier = fee_tier
        self._pools: Dict[str, PoolInfo] = {}
        self._prices: Dict[str, float] = {
            "WETH": 3000.0,
            "USDC": 1.0,
            "DAI": 1.0,
            "WBTC": 60000.0,
            "USDT": 1.0,
            "UNI": 10.0,
            "LINK": 15.0,
        }

    def get_swap_quote(
        self,
        token_in: str,
        token_out: str,
        amount_in: float,
        fee_tier: Optional[float] = None,
        slippage: float = 0.005,
    ) -> SwapQuote:
        """Calculate swap output with fees and slippage."""
        fee = fee_tier or self.fee_tier
        amount_after_fee = amount_in * (1 - fee)
        price_in = self._prices.get(token_in, 1.0)
        price_out = self._prices.get(token_out, 1.0)
        amount_out = amount_after_fee * price_in / price_out
        price_impact = self._estimate_price_impact(amount_in, token_in, token_out)
        minimum_out = amount_out * (1 - slippage)
        route = [token_in, token_out]
        return SwapQuote(
            token_in=token_in,
            token_out=token_out,
            amount_in=amount_in,
            amount_out=round(amount_out, 6),
            minimum_out=round(minimum_out, 6),
            price_impact=price_impact,
            fee=round(amount_in * fee, 6),
            route=route,
            gas_estimate=150_000,
            slippage_tolerance=slippage,
        )

    def find_best_route(
        self,
        token_in: str,
        token_out: str,
        amount_in: float,
        max_hops: int = 3,
    ) -> SwapQuote:
        """Find optimal multi-hop route."""
        best_quote = self.get_swap_quote(token_in, token_out, amount_in)
        intermediates = [
            t for t in self._prices
            if t not in (token_in, token_out)
        ]
        for mid in intermediates:
            quote1 = self.get_swap_quote(token_in, mid, amount_in)
            quote2 = self.get_swap_quote(mid, token_out, quote1.amount_out)
            total_amount_out = quote2.amount_out
            total_fee = quote1.fee + quote2.fee
            if total_amount_out > best_quote.amount_out:
                best_quote = SwapQuote(
                    token_in=token_in,
                    token_out=token_out,
                    amount_in=amount_in,
                    amount_out=round(total_amount_out, 6),
                    minimum_out=round(total_amount_out * 0.995, 6),
                    price_impact=quote1.price_impact + quote2.price_impact,
                    fee=round(total_fee, 6),
                    route=[token_in, mid, token_out],
                    gas_estimate=300_000,
                )
        return best_quote

    def calculate_price(
        self, reserve_in: float, reserve_out: float, amount_in: float
    ) -> float:
        """Constant product formula: x * y = k."""
        amount_in_with_fee = amount_in * (1 - self.fee_tier)
        return (amount_in_with_fee * reserve_out) / (reserve_in + amount_in_with_fee)

    def _estimate_price_impact(
        self, amount_in: float, token_in: str, token_out: str
    ) -> float:
        price_in = self._prices.get(token_in, 1.0)
        value = amount_in * price_in
        base_liquidity = 1_000_000
        return min(value / base_liquidity, 0.5)


# ---------------------------------------------------------------------------
# Liquidity Pool
# ---------------------------------------------------------------------------

class LiquidityPool:
    """Manage AMM liquidity pool interactions."""

    def __init__(self, address: str, protocol: str = "uniswap_v2"):
        self.address = address
        self.protocol = protocol
        self._pool_info: Optional[PoolInfo] = None

    def get_pool_info(self) -> PoolInfo:
        """Fetch pool information."""
        if self._pool_info:
            return self._pool_info
        self._pool_info = PoolInfo(
            address=self.address,
            token0_symbol="WETH",
            token1_symbol="USDC",
            reserve0=5000.0,
            reserve1=15_000_000.0,
            lp_supply=8_660_000.0,
            fee_tier=UNISWAP_V2_FEE,
            protocol=self.protocol,
            total_value_locked=30_000_000.0,
        )
        return self._pool_info

    def calculate_add_liquidity(
        self,
        amount0_desired: float,
        amount1_desired: float,
        slippage: float = 0.005,
    ) -> Dict[str, Any]:
        """Calculate LP tokens received for adding liquidity."""
        info = self.get_pool_info()
        ratio = info.reserve1 / max(info.reserve0, 1)
        amount0_optimal = amount1_desired / ratio
        amount1_optimal = amount0_optimal * ratio
        if amount0_optimal <= amount0_desired:
            amount1 = amount1_desired
        else:
            amount0_optimal = amount0_desired
            amount1 = amount0_optimal * ratio
        total_supply = info.lp_supply
        liquidity = math.sqrt(amount0_optimal * amount1_optimal)
        lp_tokens = liquidity * total_supply / math.sqrt(info.reserve0 * info.reserve1)
        return {
            "amount0": round(amount0_optimal, 6),
            "amount1": round(amount1, 6),
            "lp_tokens": round(lp_tokens, 6),
            "pool_share": lp_tokens / max(total_supply, 1) * 100,
            "price": ratio,
        }

    def calculate_remove_liquidity(
        self, lp_tokens: float
    ) -> Dict[str, float]:
        """Calculate token amounts received for removing liquidity."""
        info = self.get_pool_info()
        share = lp_tokens / max(info.lp_supply, 1)
        amount0 = share * info.reserve0
        amount1 = share * info.reserve1
        return {
            "amount0": round(amount0, 6),
            "amount1": round(amount1, 6),
            "share_pct": round(share * 100, 4),
        }

    def calculate_pool_apy(self, fee_volume_24h: float) -> float:
        """Calculate LP provider APR from daily fee volume."""
        info = self.get_pool_info()
        annual_fees = fee_volume_24h * 365
        return annual_fees / max(info.total_value_locked, 1)


# ---------------------------------------------------------------------------
# Impermanent Loss Calculator
# ---------------------------------------------------------------------------

class ImpermanentLossCalc:
    """Calculate impermanent loss for liquidity positions."""

    def calculate(
        self,
        entry_price_ratio: float,
        current_price_ratio: float,
        fee_apy: float = 0.0,
        days_in_pool: int = 0,
    ) -> ImpermanentLossResult:
        """Calculate IL with fee offset."""
        if entry_price_ratio <= 0 or current_price_ratio <= 0:
            return ImpermanentLossResult(
                entry_price_ratio=entry_price_ratio,
                current_price_ratio=current_price_ratio,
                il_pct=0.0,
                fees_earned=0.0,
                net_return=0.0,
                holding_return=0.0,
            )
        price_change = current_price_ratio / entry_price_ratio
        il = (
            2 * math.sqrt(price_change) / (1 + price_change) - 1
        )
        il_pct = abs(il)
        sqrt_r = math.sqrt(price_change)
        holding_return = price_change - 1
        lp_return = (2 * sqrt_r) / (1 + price_change) - 1
        daily_fee_rate = fee_apy / 365
        fees_earned = daily_fee_rate * days_in_pool
        net_return = lp_return + fees_earned
        return ImpermanentLossResult(
            entry_price_ratio=entry_price_ratio,
            current_price_ratio=current_price_ratio,
            il_pct=round(il_pct, 6),
            fees_earned=round(fees_earned, 6),
            net_return=round(net_return, 6),
            holding_return=round(holding_return, 6),
        )

    def breakeven_apr(
        self,
        price_change: float,
        days: int = 365,
    ) -> float:
        """Minimum APR needed to offset IL."""
        result = self.calculate(1.0, price_change, 0.0, 0)
        return abs(result.il_pct) / (days / 365)


# ---------------------------------------------------------------------------
# Yield Calculator
# ---------------------------------------------------------------------------

class YieldCalculator:
    """Calculate and compare yield farming strategies."""

    def compound_apy(self, apr: float, compound_freq: int = 365) -> float:
        """Convert APR to APY with compounding."""
        if compound_freq == 0:
            return apr
        return (1 + apr / compound_freq) ** compound_freq - 1

    def risk_adjusted_return(
        self, apy: float, risk_level: str
    ) -> float:
        """Risk-adjusted return based on protocol risk."""
        factors = {"low": 0.95, "medium": 0.85, "high": 0.70, "critical": 0.50}
        factor = factors.get(risk_level, 0.85)
        return apy * factor

    def compare_strategies(
        self, strategies: List[YieldStrategy]
    ) -> List[YieldStrategy]:
        """Rank strategies by risk-adjusted APY."""
        return sorted(
            strategies,
            key=lambda s: self.risk_adjusted_return(s.apy, s.risk_level.value),
            reverse=True,
        )

    def optimal_compound_frequency(
        self, apr: float, gas_cost_usd: float, position_value: float
    ) -> int:
        """Find optimal compounding frequency given gas costs."""
        best_freq = 365
        best_net = 0.0
        for freq in [1, 7, 14, 30, 90, 180, 365]:
            apy = self.compound_apy(apr, freq)
            net_apy = apy - (gas_cost_usd * freq / position_value)
            if net_apy > best_net:
                best_net = net_apy
                best_freq = freq
        return best_freq

    def calculate_rewards(
        self,
        staked_amount: float,
        reward_rate_per_day: float,
        token_price: float,
        days: int,
    ) -> Dict[str, float]:
        total_rewards = reward_rate_per_day * days
        value = total_rewards * token_price
        apr = (total_rewards / max(staked_amount, 1)) * (365 / days)
        return {
            "total_rewards": round(total_rewards, 4),
            "value_usd": round(value, 2),
            "apr": round(apr, 4),
            "apy": round(self.compound_apy(apr, 365), 4),
        }


# ---------------------------------------------------------------------------
# Flash Loan Executor
# ---------------------------------------------------------------------------

class FlashLoanExecutor:
    """Design and simulate flash loan transactions."""

    def __init__(self, provider: str = "aave_v3"):
        self.provider = provider
        self.fee_rate = AAVE_FLASH_LOAN_FEE if provider == "aave_v3" else 0.0

    def create_flash_loan(
        self,
        asset: str,
        amount: float,
        actions: List[Dict[str, Any]],
        gas_price_gwei: float = 30.0,
    ) -> FlashLoanPlan:
        fee = amount * self.fee_rate
        gas_cost_eth = 0.003 * gas_price_gwei / 1e9 * 1e18 / 1e18
        gas_cost_usd = gas_cost_eth * 3000
        return FlashLoanPlan(
            asset=asset,
            amount=amount,
            provider=self.provider,
            fee_rate=self.fee_rate,
            fee=round(fee, 2),
            actions=actions,
            gas_cost=round(gas_cost_usd, 2),
            projected_profit=0.0,
        )

    def simulate_arbitrage(
        self,
        asset: str,
        amount: float,
        buy_price: float,
        sell_price: float,
        gas_cost_usd: float = 10.0,
    ) -> Dict[str, float]:
        fee = amount * self.fee_rate
        buy_tokens = amount / buy_price
        sell_revenue = buy_tokens * sell_price
        profit = sell_revenue - amount - fee - gas_cost_usd
        return {
            "amount": amount,
            "tokens_bought": round(buy_tokens, 6),
            "revenue": round(sell_revenue, 2),
            "fee": round(fee, 2),
            "gas_cost": round(gas_cost_usd, 2),
            "profit": round(profit, 2),
            "roi": round(profit / amount * 100, 2),
        }


# ---------------------------------------------------------------------------
# Lending Protocol
# ---------------------------------------------------------------------------

class LendingProtocol:
    """Lending/borrowing protocol integration (Aave V3 style)."""

    def __init__(self, protocol: str = "aave_v3"):
        self.protocol = protocol
        self.collateral_factors = {
            "WETH": 0.825, "WBTC": 0.70, "LINK": 0.70,
            "UNI": 0.65, "AAVE": 0.60, "USDC": 0.80,
        }
        self.liquidation_thresholds = {
            "WETH": 0.825, "WBTC": 0.75, "LINK": 0.70,
            "UNI": 0.65, "AAVE": 0.60, "USDC": 0.85,
        }
        self.prices = {"WETH": 3000, "WBTC": 60000, "USDC": 1, "DAI": 1, "LINK": 15, "UNI": 10}

    def calculate_health_factor(
        self,
        collateral: List[Dict[str, Any]],
        borrow: List[Dict[str, Any]],
    ) -> HealthFactor:
        collateral_value = sum(
            c["amount"] * self.prices.get(c["asset"], 0) for c in collateral
        )
        borrow_value = sum(
            b["amount"] * self.prices.get(b["asset"], 0) for b in borrow
        )
        weighted_threshold = 0.0
        for c in collateral:
            asset_value = c["amount"] * self.prices.get(c["asset"], 0)
            threshold = self.liquidation_thresholds.get(c["asset"], 0.5)
            weighted_threshold += asset_value * threshold
        health = weighted_threshold / max(borrow_value, 1)
        ltv = borrow_value / max(collateral_value, 1) * 100
        max_borrow = weighted_threshold
        return HealthFactor(
            health_factor=round(health, 4),
            collateral_value=round(collateral_value, 2),
            borrow_value=round(borrow_value, 2),
            liquidation_threshold=round(weighted_threshold, 2),
            max_borrow=round(max_borrow, 2),
            current_ltv=round(ltv, 2),
        )

    def calculate_borrow_capacity(
        self, collateral: List[Dict[str, Any]]
    ) -> float:
        total = 0.0
        for c in collateral:
            value = c["amount"] * self.prices.get(c["asset"], 0)
            factor = self.collateral_factors.get(c["asset"], 0.5)
            total += value * factor
        return total

    def estimate_liquidation_price(
        self,
        collateral_asset: str,
        collateral_amount: float,
        borrow_asset: str,
        borrow_amount: float,
    ) -> float:
        threshold = self.liquidation_thresholds.get(collateral_asset, 0.5)
        borrow_value = borrow_amount * self.prices.get(borrow_asset, 1)
        liq_value = borrow_value / threshold
        return liq_value / max(collateral_amount, 1)


# ---------------------------------------------------------------------------
# Price Oracle
# ---------------------------------------------------------------------------

class PriceOracleManager:
    """Multi-oracle aggregation and staleness detection."""

    def __init__(self):
        self._oracles: Dict[str, List[PriceOracle]] = {}

    def add_oracle(self, asset: str, oracle: PriceOracle) -> None:
        if asset not in self._oracles:
            self._oracles[asset] = []
        self._oracles[asset].append(oracle)

    def get_price(
        self, asset: str, max_age_seconds: float = 3600
    ) -> Optional[float]:
        oracles = self._oracles.get(asset, [])
        valid = [
            o for o in oracles
            if o.age_seconds <= max_age_seconds and not o.stale
        ]
        if not valid:
            return None
        prices = [o.price for o in valid]
        if len(prices) >= 3:
            prices.sort()
            prices = prices[1:-1]
        return sum(prices) / len(prices)

    def detect_manipulation(
        self, asset: str, threshold: float = 0.05
    ) -> bool:
        oracles = self._oracles.get(asset, [])
        if len(oracles) < 2:
            return False
        prices = [o.price for o in oracles]
        mean_price = sum(prices) / len(prices)
        return any(
            abs(p - mean_price) / mean_price > threshold for p in prices
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  DeFi Module Demo")
    print("=" * 60)

    print("\n[1] AMM Swap Quote")
    router = AMMRouter()
    quote = router.get_swap_quote("WETH", "USDC", 1.0)
    print(f"  1 WETH -> {quote.amount_out:.2f} USDC")
    print(f"  Price impact: {quote.price_impact:.2%}")
    print(f"  Fee: {quote.fee:.4f} WETH")

    print("\n[2] Multi-hop Route")
    route = router.find_best_route("DAI", "WBTC", 10000)
    print(f"  Route: {' -> '.join(route.route)}")
    print(f"  Output: {route.amount_out:.6f} WBTC")

    print("\n[3] Liquidity Pool")
    pool = LiquidityPool("0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc")
    info = pool.get_pool_info()
    print(f"  {info.token0_symbol}/{info.token1_symbol}")
    print(f"  TVL: ${info.total_value_locked:,.0f}")
    add_liq = pool.calculate_add_liquidity(5.0, 15000.0)
    print(f"  LP tokens: {add_liq['lp_tokens']:.4f}")

    print("\n[4] Impermanent Loss")
    il_calc = ImpermanentLossCalc()
    il = il_calc.calculate(1.0, 2.0, fee_apy=0.25, days_in_pool=365)
    print(f"  IL: {il.il_pct:.2%}  Fees: {il.fees_earned:.2%}")
    print(f"  Net: {il.net_return:.2%} vs Hold: {il.holding_return:.2%}")

    print("\n[5] Yield Strategies")
    calc = YieldCalculator()
    apy = calc.compound_apy(0.15, compound_freq=365)
    print(f"  15% APR compounded daily: {apy:.2%} APY")

    print("\n[6] Flash Loan")
    executor = FlashLoanExecutor()
    sim = executor.simulate_arbitrage("USDC", 1_000_000, 0.999, 1.001)
    print(f"  Profit: ${sim['profit']:.2f} ({sim['roi']:.2f}% ROI)")

    print("\n[7] Lending Health Factor")
    lending = LendingProtocol()
    health = lending.calculate_health_factor(
        collateral=[{"asset": "WETH", "amount": 10}],
        borrow=[{"asset": "USDC", "amount": 15000}],
    )
    print(f"  Health factor: {health.health_factor:.2f}")
    print(f"  LTV: {health.current_ltv:.1f}%")

    print("\n" + "=" * 60)
    print("  DeFi module demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
