"""
DeFi Patterns Module
AMM, lending, yield, flash loans, and stablecoin mechanics.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AMMType(Enum):
    CONSTANT_PRODUCT = "constant_product"
    CONSTANT_SUM = "constant_sum"
    STABLE_SWAP = "stable_swap"
    CONCENTRATED = "concentrated"


class CollateralType(Enum):
    ETH = "eth"
    BTC = "btc"
    STABLECOIN = "stablecoin"
    LP_TOKEN = "lp_token"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SwapResult:
    """AMM swap result."""
    input_amount: float
    output_amount: float
    price_impact: float
    fee: float
    price_before: float = 0.0
    price_after: float = 0.0


@dataclass
class StableSwapResult:
    """Stable swap result."""
    input_index: int
    output_index: int
    input_amount: float
    output_amount: float
    fee: float = 0.0


@dataclass
class LendingPosition:
    """Lending position."""
    collateral_amount: float
    collateral_price: float
    borrow_amount: float
    borrow_asset: str = "USDC"
    collateral_asset: str = "ETH"
    liquidation_threshold: float = 0.80
    interest_rate: float = 0.05

    @property
    def collateral_value(self) -> float:
        return self.collateral_amount * self.collateral_price

    @property
    def ltv(self) -> float:
        return self.borrow_amount / max(self.collateral_value, 1)

    def health_factor(self) -> float:
        return (self.collateral_value * self.liquidation_threshold) / max(self.borrow_amount, 1)

    def liquidation_price(self) -> float:
        return self.borrow_amount / (self.collateral_amount * self.liquidation_threshold)

    def max_borrow(self) -> float:
        return self.collateral_value * self.liquidation_threshold


@dataclass
class YieldResult:
    """Yield calculation result."""
    apy: float
    apr: float
    daily_reward: float
    annual_reward: float
    compounding_factor: float = 1.0


@dataclass
class FlashLoanResult:
    """Flash loan simulation result."""
    flash_amount: float
    fee: float
    gas_cost: float
    profit: float
    roi: float = 0.0


@dataclass
class InterestRateModel:
    """Interest rate model."""
    name: str
    base_rate: float
    slope1: float
    slope2: float
    optimal_utilization: float

    def get_rate(self, utilization: float) -> float:
        if utilization <= self.optimal_utilization:
            return self.base_rate + (utilization / self.optimal_utilization) * self.slope1
        else:
            excess = utilization - self.optimal_utilization
            return self.base_rate + self.slope1 + (excess / (1 - self.optimal_utilization)) * self.slope2


# ---------------------------------------------------------------------------
# AMM Calculator
# ---------------------------------------------------------------------------

class AMMCalculator:
    """Automated Market Maker calculations."""

    def __init__(
        self,
        reserve_a: float = 1000,
        reserve_b: float = 2000,
        fee: float = 0.003,
    ):
        self.reserve_a = reserve_a
        self.reserve_b = reserve_b
        self.fee = fee

    @property
    def price_a_in_b(self) -> float:
        return self.reserve_b / max(self.reserve_a, 1)

    @property
    def price_b_in_a(self) -> float:
        return self.reserve_a / max(self.reserve_b, 1)

    @property
    def k(self) -> float:
        return self.reserve_a * self.reserve_b

    def calculate_swap(
        self, input_amount: float, input_token: str = "A"
    ) -> SwapResult:
        price_before = self.price_a_in_b if input_token == "A" else self.price_b_in_a
        fee_amount = input_amount * self.fee
        amount_in_after_fee = input_amount - fee_amount
        if input_token == "A":
            new_reserve_a = self.reserve_a + amount_in_after_fee
            new_reserve_b = self.k / new_reserve_a
            output = self.reserve_b - new_reserve_b
            price_after = new_reserve_b / new_reserve_a
        else:
            new_reserve_b = self.reserve_b + amount_in_after_fee
            new_reserve_a = self.k / new_reserve_b
            output = self.reserve_a - new_reserve_a
            price_after = new_reserve_b / new_reserve_a
        price_impact = abs(price_after - price_before) / max(price_before, 1)
        return SwapResult(
            input_amount=input_amount,
            output_amount=round(output, 6),
            price_impact=round(price_impact, 6),
            fee=round(fee_amount, 6),
            price_before=round(price_before, 6),
            price_after=round(price_after, 6),
        )

    def add_liquidity(
        self, amount_a: float, amount_b: Optional[float] = None
    ) -> Dict[str, float]:
        if amount_b is None:
            amount_b = amount_a * self.price_a_in_b
        share = math.sqrt(amount_a * amount_b) / math.sqrt(self.k)
        return {
            "amount_a": amount_a,
            "amount_b": round(amount_b, 6),
            "lp_tokens": round(share * 1000, 6),
            "pool_share": round(share * 100, 2),
        }


# ---------------------------------------------------------------------------
# Stable Swap Calculator
# ---------------------------------------------------------------------------

class StableSwapCalculator:
    """Curve-style stable swap calculations."""

    def __init__(
        self,
        balances: Optional[List[float]] = None,
        amplification: float = 100,
        fee: float = 0.0004,
    ):
        self.balances = balances or [1_000_000, 1_000_000, 1_000_000]
        self.amplification = amplification
        self.fee = fee

    def swap(
        self, input_index: int, output_index: int, amount: float
    ) -> StableSwapResult:
        fee_amount = amount * self.fee
        amount_after_fee = amount - fee_amount
        D = self._get_D()
        new_balance = self.balances[input_index] + amount_after_fee
        output_amount = self.balances[output_index] - self._compute_y(
            input_index, output_index, new_balance, D
        )
        return StableSwapResult(
            input_index=input_index,
            output_index=output_index,
            input_amount=amount,
            output_amount=round(max(output_amount, 0), 6),
            fee=round(fee_amount, 6),
        )

    def _get_D(self) -> float:
        S = sum(self.balances)
        D = S
        for _ in range(256):
            D_prev = D
            n = len(self.balances)
            f = D
            for balance in self.balances:
                f = f * D / (balance * n + 1e-18)
            D = (self.amplification * S + f) * D / (
                (self.amplification - 1) * D + (n + 1) * f
            )
            if abs(D - D_prev) <= 1:
                break
        return D

    def _compute_y(
        self, input_index: int, output_index: int, new_x: float, D: float
    ) -> float:
        n = len(self.balances)
        c = D
        for i, b in enumerate(self.balances):
            if i != output_index:
                if i == input_index:
                    c = c * D / (new_x * n + 1e-18)
                else:
                    c = c * D / (b * n + 1e-18)
        c = c * D / (self.amplification * n + 1e-18)
        y = D
        for _ in range(256):
            y_prev = y
            y = (y * y + c) / (2 * y + self.amplification * D / (n + 1e-18) - D)
            if abs(y - y_prev) <= 1:
                break
        return y


# ---------------------------------------------------------------------------
# Lending Model
# ---------------------------------------------------------------------------

class LendingModel:
    """Lending protocol model."""

    def __init__(
        self,
        collateral: float = 10,
        collateral_price: float = 3000,
        borrow_amount: float = 15000,
        liquidation_threshold: float = 0.80,
        interest_rate: float = 0.05,
    ):
        self.position = LendingPosition(
            collateral_amount=collateral,
            collateral_price=collateral_price,
            borrow_amount=borrow_amount,
            liquidation_threshold=liquidation_threshold,
            interest_rate=interest_rate,
        )

    def health_factor(self) -> float:
        return self.position.health_factor()

    def liquidation_price(self) -> float:
        return self.position.liquidation_price()

    def max_borrow(self) -> float:
        return self.position.max_borrow()

    def interest_model(self) -> InterestRateModel:
        return InterestRateModel(
            name="kink_model",
            base_rate=0.02,
            slope1=0.08,
            slope2=0.30,
            optimal_utilization=0.80,
        )


# ---------------------------------------------------------------------------
# Yield Calculator
# ---------------------------------------------------------------------------

class YieldCalculator:
    """Calculate yield and staking returns."""

    def calculate_apy(
        self,
        reward_per_day: float,
        token_price: float,
        staked_value: float,
        compound_freq: int = 365,
    ) -> float:
        daily_rate = (reward_per_day * token_price) / max(staked_value, 1)
        apr = daily_rate * 365
        apy = (1 + daily_rate) ** 365 - 1
        return apy

    def calculate_il(
        self, entry_price: float, current_price: float
    ) -> float:
        ratio = current_price / max(entry_price, 1)
        il = 2 * math.sqrt(ratio) / (1 + ratio) - 1
        return abs(il)

    def calculate_vault_returns(
        self,
        total_assets: float,
        share_price: float,
        performance_fee: float = 0.2,
        management_fee: float = 0.02,
    ) -> Dict[str, float]:
        shares = total_assets / max(share_price, 1)
        management = total_assets * management_fee / 365
        return {
            "shares": shares,
            "daily_management_fee": round(management, 2),
            "annual_management_fee": round(management * 365, 2),
        }


# ---------------------------------------------------------------------------
# Flash Loan Simulator
# ---------------------------------------------------------------------------

class FlashLoanSimulator:
    """Simulate flash loan transactions."""

    FLASH_LOAN_FEE = 0.0009

    def simulate_arbitrage(
        self,
        flash_amount: float,
        buy_price: float,
        sell_price: float,
        gas_cost_usd: float = 10,
    ) -> float:
        fee = flash_amount * self.FLASH_LOAN_FEE
        tokens_bought = flash_amount / max(buy_price, 0.001)
        revenue = tokens_bought * sell_price
        profit = revenue - flash_amount - fee - gas_cost_usd
        return round(profit, 2)

    def simulate_liquidation(
        self,
        flash_amount: float,
        collateral_amount: float,
        collateral_price: float,
        discount: float = 0.05,
        gas_cost_usd: float = 15,
    ) -> float:
        collateral_value = collateral_amount * collateral_price
        discounted_value = collateral_value * (1 - discount)
        fee = flash_amount * self.FLASH_LOAN_FEE
        profit = discounted_value - flash_amount - fee - gas_cost_usd
        return round(profit, 2)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  DeFi Patterns Demo")
    print("=" * 60)

    print("\n[1] AMM Swap")
    amm = AMMCalculator(1000, 2_000_000)
    result = amm.calculate_swap(10, "A")
    print(f"  Swap: 10 A -> {result.output_amount:.2f} B")
    print(f"  Impact: {result.price_impact:.4%}")

    print("\n[2] Stable Swap")
    stable = StableSwapCalculator([1_000_000, 1_000_000, 1_000_000], 100)
    result = stable.swap(0, 1, 10_000)
    print(f"  Swap: 10000 -> {result.output_amount:.2f}")

    print("\n[3] Lending Position")
    lending = LendingModel(10, 3000, 15000)
    print(f"  Health factor: {lending.health_factor():.2f}")
    print(f"  Liquidation price: ${lending.liquidation_price():.0f}")
    print(f"  Max borrow: ${lending.max_borrow():.0f}")

    print("\n[4] Yield Calculation")
    yc = YieldCalculator()
    apy = yc.calculate_apy(100, 5, 100_000)
    print(f"  APY: {apy:.1%}")
    il = yc.calculate_il(1.0, 2.0)
    print(f"  Impermanent loss: {il:.2%}")

    print("\n[5] Flash Loan")
    flash = FlashLoanSimulator()
    profit = flash.simulate_arbitrage(1_000_000, 0.999, 1.001, 10)
    print(f"  Profit: ${profit:.2f}")

    print("\n[6] Interest Rate Model")
    model = InterestRateModel("kink", 0.02, 0.08, 0.30, 0.80)
    for util in [0.4, 0.6, 0.8, 0.9, 0.95]:
        rate = model.get_rate(util)
        print(f"  Utilization {util:.0%}: Rate {rate:.1%}")

    print("\n" + "=" * 60)
    print("  DeFi patterns demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
