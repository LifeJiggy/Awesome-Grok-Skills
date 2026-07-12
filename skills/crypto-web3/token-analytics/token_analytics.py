"""
Token Analytics Module
Tokenomics, holder distribution, liquidity, market metrics, and whale tracking.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TokenomicsAnalysis:
    """Tokenomics analysis result."""
    total_supply: float
    circulating_supply: float
    circulating_pct: float
    inflation_rate: float
    years_to_full_dilution: float
    burn_rate: float
    emission_schedule: List[Dict[str, float]] = field(default_factory=list)


@dataclass
class HolderMetrics:
    """Holder distribution metrics."""
    gini_coefficient: float
    top1_pct: float
    top5_pct: float
    top10_pct: float
    top20_pct: float
    total_holders: int = 0
    median_holding: float = 0.0


@dataclass
class LiquidityDepth:
    """Liquidity depth analysis."""
    bid_depth_usd: float
    ask_depth_usd: float
    spread_pct: float
    mid_price: float
    slippage_1pct: float = 0.0
    depth_levels: int = 0


@dataclass
class MarketCapMetrics:
    """Market cap metrics."""
    price: float
    market_cap: float
    fully_diluted_valuation: float
    mcap_fdv_ratio: float
    circulating_supply: float
    total_supply: float


@dataclass
class OnChainMetrics:
    """On-chain analysis metrics."""
    active_addresses_24h: int = 0
    transaction_count_24h: int = 0
    avg_transaction_value: float = 0.0
    nvt_ratio: float = 0.0
    nvt_signal: float = 0.0
    network_growth: float = 0.0


@dataclass
class WhaleAlert:
    """Whale transaction alert."""
    amount: float
    token: str
    from_address: str
    to_address: str
    value_usd: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------------------------------------------------------------------------
# Tokenomics Analyzer
# ---------------------------------------------------------------------------

class TokenomicsAnalyzer:
    """Analyze token economics."""

    def analyze(
        self,
        total_supply: float = 1_000_000_000,
        circulating_supply: float = 500_000_000,
        annual_emission: float = 50_000_000,
        burn_rate: float = 0.02,
    ) -> TokenomicsAnalysis:
        circulating_pct = circulating_supply / max(total_supply, 1)
        net_emission = annual_emission - (circulating_supply * burn_rate)
        inflation_rate = net_emission / max(circulating_supply, 1)
        remaining_to_mint = total_supply - circulating_supply
        years_to_dilute = remaining_to_mint / max(annual_emission, 1) if annual_emission > 0 else float('inf')
        schedule = []
        supply = circulating_supply
        for year in range(1, min(int(years_to_dilute) + 2, 11)):
            emission = annual_emission * (0.85 ** (year - 1))
            supply = min(supply + emission, total_supply)
            schedule.append({"year": year, "supply": round(supply, 0), "emission": round(emission, 0)})
        return TokenomicsAnalysis(
            total_supply=total_supply,
            circulating_supply=circulating_supply,
            circulating_pct=round(circulating_pct, 4),
            inflation_rate=round(inflation_rate, 4),
            years_to_full_dilution=round(years_to_dilute, 1),
            burn_rate=burn_rate,
            emission_schedule=schedule,
        )


# ---------------------------------------------------------------------------
# Holder Distribution
# ---------------------------------------------------------------------------

class HolderDistribution:
    """Analyze token holder distribution."""

    def gini_coefficient(self, holdings: List[float]) -> float:
        if not holdings:
            return 0.0
        sorted_h = sorted(holdings)
        n = len(sorted_h)
        total = sum(sorted_h)
        if total == 0:
            return 0.0
        cumulative = 0.0
        gini_sum = 0.0
        for i, h in enumerate(sorted_h):
            cumulative += h
            gini_sum += (2 * (i + 1) - n - 1) * h
        return max(0, min(1, gini_sum / (n * total)))

    def concentration_metrics(self, holdings: List[float]) -> HolderMetrics:
        sorted_h = sorted(holdings, reverse=True)
        total = sum(sorted_h)
        if total == 0:
            return HolderMetrics(0, 0, 0, 0, 0)
        cumsum = 0.0
        metrics = {"top1": 0, "top5": 0, "top10": 0, "top20": 0}
        for i, h in enumerate(sorted_h):
            cumsum += h
            pct = cumsum / total
            if i == 0:
                metrics["top1"] = pct
            if i == 4:
                metrics["top5"] = pct
            if i == 9:
                metrics["top10"] = pct
            if i == 19:
                metrics["top20"] = pct
        return HolderMetrics(
            gini_coefficient=self.gini_coefficient(holdings),
            top1_pct=round(metrics["top1"], 4),
            top5_pct=round(metrics["top5"], 4),
            top10_pct=round(metrics["top10"], 4),
            top20_pct=round(metrics["top20"], 4),
            total_holders=len(holdings),
            median_holding=sorted_h[len(sorted_h) // 2],
        )


# ---------------------------------------------------------------------------
# Liquidity Analyzer
# ---------------------------------------------------------------------------

class LiquidityAnalyzer:
    """Analyze market liquidity."""

    def analyze_depth(
        self,
        bids: Optional[List[tuple]] = None,
        asks: Optional[List[tuple]] = None,
    ) -> LiquidityDepth:
        bids = bids or [(1.0, 10000)]
        asks = asks or [(1.01, 8000)]
        bid_depth = sum(price * qty for price, qty in bids)
        ask_depth = sum(price * qty for price, qty in asks)
        best_bid = max(p for p, _ in bids)
        best_ask = min(p for p, _ in asks)
        spread = (best_ask - best_bid) / max(best_bid, 1)
        mid = (best_bid + best_ask) / 2
        slippage = ask_depth * 0.01 / max(mid, 1) if ask_depth > 0 else 0
        return LiquidityDepth(
            bid_depth_usd=round(bid_depth, 2),
            ask_depth_usd=round(ask_depth, 2),
            spread_pct=round(spread, 6),
            mid_price=round(mid, 6),
            slippage_1pct=round(slippage, 6),
            depth_levels=len(bids) + len(asks),
        )

    def estimate_slippage(
        self, order_size_usd: float, depth: LiquidityDepth
    ) -> float:
        return order_size_usd / max(depth.ask_depth_usd, 1) * 0.5


# ---------------------------------------------------------------------------
# Market Metrics
# ---------------------------------------------------------------------------

class MarketMetrics:
    """Calculate market metrics."""

    def calculate_mcap(
        self,
        price: float,
        circulating_supply: float,
        total_supply: float,
    ) -> MarketCapMetrics:
        mcap = price * circulating_supply
        fdv = price * total_supply
        ratio = mcap / max(fdv, 1)
        return MarketCapMetrics(
            price=price,
            market_cap=round(mcap, 0),
            fully_diluted_valuation=round(fdv, 0),
            mcap_fdv_ratio=round(ratio, 4),
            circulating_supply=circulating_supply,
            total_supply=total_supply,
        )

    def calculate_nvt(
        self,
        market_cap: float,
        daily_transactions_usd: float,
        smoothing: int = 14,
    ) -> float:
        return market_cap / max(daily_transactions_usd * smoothing, 1)

    def volatility(self, prices: List[float], window: int = 30) -> float:
        if len(prices) < 2:
            return 0.0
        returns = [(prices[i] - prices[i-1]) / max(prices[i-1], 1) for i in range(1, len(prices))]
        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / max(len(returns) - 1, 1)
        return math.sqrt(variance)


# ---------------------------------------------------------------------------
# Whale Tracker
# ---------------------------------------------------------------------------

class WhaleTracker:
    """Track whale transactions."""

    def __init__(self, threshold: float = 1000000):
        self.threshold = threshold
        self._alerts: List[WhaleAlert] = []

    def detect_large_transfers(
        self,
        transactions: List[Dict[str, Any]],
        threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        threshold = threshold or self.threshold
        alerts: List[Dict[str, Any]] = []
        for tx in transactions:
            if tx.get("amount", 0) >= threshold:
                alerts.append({
                    "amount": tx["amount"],
                    "token": tx.get("token", "unknown"),
                    "from": tx.get("from", ""),
                    "to": tx.get("to", ""),
                })
        return alerts

    def detect_accumulation(
        self, holder_changes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        accumulations: List[Dict[str, Any]] = []
        for change in holder_changes:
            if change.get("change", 0) > 0:
                accumulations.append(change)
        return accumulations


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Token Analytics Demo")
    print("=" * 60)

    print("\n[1] Tokenomics Analysis")
    analyzer = TokenomicsAnalyzer()
    analysis = analyzer.analyze(1_000_000_000, 500_000_000, 50_000_000, 0.02)
    print(f"  Circulating: {analysis.circulating_pct:.1%}")
    print(f"  Inflation: {analysis.inflation_rate:.2%}")
    print(f"  Years to dilute: {analysis.years_to_full_dilution:.1f}")

    print("\n[2] Holder Distribution")
    holders = HolderDistribution()
    metrics = holders.concentration_metrics([1000, 500, 200, 100, 50, 30, 20, 10, 5, 3])
    print(f"  Gini: {metrics.gini_coefficient:.3f}")
    print(f"  Top 1: {metrics.top1_pct:.1%}")
    print(f"  Top 10: {metrics.top10_pct:.1%}")

    print("\n[3] Liquidity Analysis")
    liquidity = LiquidityAnalyzer()
    depth = liquidity.analyze_depth(
        [(1.0, 10000), (0.99, 15000)],
        [(1.01, 8000), (1.02, 12000)],
    )
    print(f"  Bid depth: ${depth.bid_depth_usd:,.0f}")
    print(f"  Spread: {depth.spread_pct:.4%}")

    print("\n[4] Market Metrics")
    metrics_calc = MarketMetrics()
    mcap = metrics_calc.calculate_mcap(2.5, 500_000_000, 1_000_000_000)
    print(f"  Market cap: ${mcap.market_cap:,.0f}")
    print(f"  FDV: ${mcap.fully_diluted_valuation:,.0f}")
    print(f"  Mcap/FDV: {mcap.mcap_fdv_ratio:.2%}")

    print("\n[5] Whale Tracking")
    tracker = WhaleTracker(1000000)
    alerts = tracker.detect_large_transfers([
        {"amount": 5000000, "token": "USDC", "from": "0x1234", "to": "0xABCD"},
        {"amount": 500000, "token": "USDC", "from": "0x5678", "to": "0xEFGH"},
    ])
    for a in alerts:
        print(f"  Whale: {a['amount']:,} {a['token']}")

    print("\n[6] Volatility")
    vol = metrics_calc.volatility([1.0, 1.1, 0.95, 1.05, 1.02, 0.98, 1.03])
    print(f"  Volatility: {vol:.4f}")

    print("\n" + "=" * 60)
    print("  Token analytics demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
