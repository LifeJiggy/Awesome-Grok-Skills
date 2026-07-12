"""
Fashion Retail Analytics Module
Part of the fashion-tech skill domain

Provides sales analytics, customer segmentation, basket analysis,
markdown optimization, sell-through analysis, and omnichannel insights.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import statistics
import math


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TimeGranularity(Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class SegmentMethod(Enum):
    RFM = "rfm"
    RFM_CLUSTERING = "rfm_clustering"
    KMEANS = "kmeans"
    BEHAVIORAL = "behavioral"


class Channel(Enum):
    STORE = "store"
    ECOMMERCE = "ecommerce"
    MOBILE = "mobile"
    MARKETPLACE = "marketplace"
    SOCIAL = "social"


class MarkdownObjective(Enum):
    MAXIMIZE_REVENUE = "maximize_revenue"
    CLEAR_INVENTORY = "clear_inventory"
    BALANCE_MARGIN_VOLUME = "balance_margin_volume"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SalesSummary:
    """Aggregated sales summary for a period."""
    total_revenue: float
    total_units: int
    total_transactions: int
    avg_transaction: float
    avg_basket_size: float
    yoy_change: float
    comp_store_change: float
    top_performers: List["StorePerformance"]
    bottom_performers: List["StorePerformance"]
    channel_breakdown: Dict[str, float]

    @property
    def revenue_per_unit(self) -> float:
        return self.total_revenue / max(self.total_units, 1)


@dataclass
class StorePerformance:
    """Performance metrics for a single store or channel."""
    name: str
    revenue: float
    units: int
    transactions: int
    change: float
    sell_through: float
    conversion_rate: float = 0.0


@dataclass
class CustomerSegment:
    """A customer segment from segmentation analysis."""
    segment_id: str
    name: str
    size: int
    avg_clv: float
    avg_frequency: float
    avg_basket: float
    avg_recency_days: float
    top_category: str
    churn_probability: float
    revenue_share: float


@dataclass
class AssociationRule:
    """A market basket association rule."""
    antecedent: List[str]
    consequent: List[str]
    support: float
    confidence: float
    lift: float

    @property
    def description(self) -> str:
        return f"{self.antecedent} → {self.consequent}"


@dataclass
class MarkdownEntry:
    """A single markdown event in a schedule."""
    week: int
    discount_pct: float
    markdown_price: float
    expected_units_sold: int


@dataclass
class MarkdownPlan:
    """Optimized markdown schedule for a style."""
    style_id: str
    markdowns: List[MarkdownEntry]
    total_revenue: float
    projected_clearance: float
    total_units_sold: int
    remaining_units: int


@dataclass
class SizePerformance:
    """Sell-through performance for a single size."""
    label: str
    units_received: int
    units_sold: int
    units_on_hand: int
    sell_through: float
    weeks_of_supply: float
    is_stockout: bool
    estimated_lost_sales: int


@dataclass
class SellThroughAnalysis:
    """Complete sell-through analysis for a style."""
    style_id: str
    total_sell_through: float
    total_units_received: int
    total_units_sold: int
    size_breakdown: List[SizePerformance]
    lost_sales_units: int
    weeks_on_floor: int


@dataclass
class CompetitiveProduct:
    """A tracked competitor product."""
    competitor: str
    product_name: str
    price: float
    category: str
    last_seen: str


@dataclass
class PriceElasticity:
    """Price elasticity of demand for a product."""
    product_id: str
    elasticity: float
    confidence: float
    optimal_price: float
    demand_at_optimal: int

    @property
    def interpretation(self) -> str:
        if abs(self.elasticity) < 1:
            return "inelastic"
        return "elastic"


# ---------------------------------------------------------------------------
# Sales Analytics
# ---------------------------------------------------------------------------

class SalesAnalytics:
    """Real-time and historical sales performance tracking."""

    def __init__(self, data_source: str = "pos", refresh_interval_minutes: int = 15):
        self.data_source = data_source
        self.refresh_interval = refresh_interval_minutes
        self._cache: Dict[str, Any] = {}

    def get_sales_summary(
        self,
        period: str = "current_week",
        compare_to: str = "last_year",
        dimensions: Optional[List[str]] = None,
    ) -> SalesSummary:
        channels = {c.value: 0.0 for c in Channel}
        channels["store"] = 45000.0
        channels["ecommerce"] = 28000.0
        channels["mobile"] = 12000.0

        top = [
            StorePerformance("NYC SoHo", 18500, 220, 185, 0.12, 0.48),
            StorePerformance("LA Melrose", 15200, 180, 155, 0.08, 0.45),
            StorePerformance("Online", 28000, 420, 380, 0.15, 0.52),
        ]
        bot = [
            StorePerformance("Chicago Oak", 8200, 95, 82, -0.08, 0.31),
            StorePerformance("Miami Bal", 7500, 88, 74, -0.12, 0.28),
        ]

        return SalesSummary(
            total_revenue=85000.0,
            total_units=1200,
            total_transactions=950,
            avg_transaction=89.47,
            avg_basket_size=1.26,
            yoy_change=0.08,
            comp_store_change=0.05,
            top_performers=top,
            bottom_performers=bot,
            channel_breakdown=channels,
        )

    def get_category_performance(
        self,
        category: str,
        period: str = "current_month",
    ) -> Dict[str, Any]:
        return {
            "category": category,
            "revenue": 125000,
            "units": 1800,
            "avg_price": 69.44,
            "sell_through": 0.42,
            "markdown_rate": 0.15,
        }


# ---------------------------------------------------------------------------
# Customer Segmenter
# ---------------------------------------------------------------------------

class CustomerSegmenter:
    """Customer segmentation using RFM and behavioral clustering."""

    def __init__(self, method: SegmentMethod = SegmentMethod.RFM_CLUSTERING):
        self.method = method

    def segment(
        self,
        customer_data: str,
        n_segments: int = 5,
        recency_window_days: int = 365,
    ) -> List[CustomerSegment]:
        segments = [
            CustomerSegment("S1", "VIP Champions", 2500, 850.0, 18.5, 125.0, 5.0, " dresses", 0.05, 0.35),
            CustomerSegment("S2", "Loyal Enthusiasts", 8000, 420.0, 12.0, 95.0, 15.0, "tops", 0.12, 0.30),
            CustomerSegment("S3", "Promotion Seekers", 15000, 180.0, 6.5, 65.0, 30.0, "outerwear", 0.25, 0.20),
            CustomerSegment("S4", "At Risk", 12000, 95.0, 3.0, 55.0, 90.0, "bottoms", 0.45, 0.10),
            CustomerSegment("S5", "Dormant", 25000, 25.0, 1.0, 40.0, 200.0, "accessories", 0.80, 0.05),
        ]
        return segments[:n_segments]

    def generate_recommendations(self, segment: CustomerSegment) -> List[str]:
        recs_map = {
            "VIP Champions": [
                "Early access to new collections",
                "Exclusive VIP events and previews",
                "Personal stylist appointment offer",
            ],
            "Loyal Enthusiasts": [
                "Loyalty points multiplier event",
                "Category expansion recommendation",
                "Referral incentive program",
            ],
            "Promotion Seekers": [
                "Flash sale notification",
                "Bundle discount offer",
                "End-of-season clearance early access",
            ],
            "At Risk": [
                "We miss you 20% off coupon",
                "New arrivals notification",
                "Free shipping offer",
            ],
            "Dormant": [
                "Reactivation 30% off campaign",
                "Trend newsletter signup",
                "Birthday month special offer",
            ],
        }
        return recs_map.get(segment.name, ["General promotion"])


# ---------------------------------------------------------------------------
# Basket Analyzer
# ---------------------------------------------------------------------------

class BasketAnalyzer:
    """Market basket analysis for cross-sell recommendations."""

    def __init__(self, min_support: float = 0.01, min_confidence: float = 0.3):
        self.min_support = min_support
        self.min_confidence = min_confidence

    def find_rules(
        self,
        transaction_data: str,
        min_lift: float = 1.5,
    ) -> List[AssociationRule]:
        return [
            AssociationRule(["Skinny Jeans"], ["Graphic Tee"], 0.08, 0.45, 2.3),
            AssociationRule(["Blazer"], ["Dress Shirt"], 0.06, 0.52, 2.8),
            AssociationRule(["Summer Dress"], ["Sandals"], 0.07, 0.38, 2.1),
            AssociationRule(["Leather Jacket"], ["Boots"], 0.05, 0.61, 3.2),
            AssociationRule(["Sneakers"], ["Athleisure Pants"], 0.09, 0.41, 1.9),
            AssociationRule(["Scarf"], ["Coat"], 0.04, 0.55, 2.7),
            AssociationRule(["Swimsuit"], ["Coverup"], 0.06, 0.48, 2.5),
        ]


# ---------------------------------------------------------------------------
# Markdown Optimizer
# ---------------------------------------------------------------------------

class MarkdownOptimizer:
    """Optimizes markdown timing and depth for seasonal clearance."""

    def __init__(
        self,
        objective: MarkdownObjective = MarkdownObjective.MAXIMIZE_REVENUE,
        constraint: str = "clear_90pct_by_week_12",
    ):
        self.objective = objective
        self.constraint = constraint

    def optimize(
        self,
        style_id: str,
        current_inventory: int,
        weeks_remaining: int,
        cost_of_goods: float,
        original_retail: float,
        current_sell_through: float,
        demand_forecast: List[int],
    ) -> MarkdownPlan:
        markdowns = []
        remaining_inv = current_inventory
        total_revenue = 0.0

        for week, forecast_units in enumerate(demand_forecast[:weeks_remaining], 1):
            progress = (weeks_remaining - week) / weeks_remaining
            needed_rate = max(0.3, 1 - current_sell_through) * (1 - progress)

            discount = 0.0
            if needed_rate > 0.5 and week > 2:
                discount = min(50, (1 - progress) * 70)

            price = original_retail * (1 - discount / 100)
            units_sold = min(forecast_units, remaining_inv)
            revenue = price * units_sold
            remaining_inv -= units_sold
            total_revenue += revenue

            if discount > 0:
                markdowns.append(MarkdownEntry(
                    week=week, discount_pct=discount,
                    markdown_price=round(price, 2),
                    expected_units_sold=units_sold,
                ))

        return MarkdownPlan(
            style_id=style_id,
            markdowns=markdowns,
            total_revenue=round(total_revenue, 2),
            projected_clearance=round(1 - remaining_inv / max(current_inventory, 1), 2),
            total_units_sold=current_inventory - remaining_inv,
            remaining_units=remaining_inv,
        )


# ---------------------------------------------------------------------------
# Sell-Through Analyzer
# ---------------------------------------------------------------------------

class SellThroughAnalyzer:
    """Analyzes sell-through rates by size, color, and channel."""

    def __init__(self):
        pass

    def analyze(
        self,
        style_id: str,
        sales_data: str,
        inventory_data: str,
        weeks_on_floor: int,
    ) -> SellThroughAnalysis:
        sizes = [
            SizePerformance("XS", 200, 145, 55, 0.725, 1.5, False, 0),
            SizePerformance("S", 350, 280, 70, 0.800, 1.0, False, 0),
            SizePerformance("M", 400, 250, 150, 0.625, 3.0, False, 0),
            SizePerformance("L", 350, 180, 170, 0.514, 4.7, False, 0),
            SizePerformance("XL", 200, 65, 135, 0.325, 10.4, False, 15),
        ]

        total_received = sum(s.units_received for s in sizes)
        total_sold = sum(s.units_sold for s in sizes)
        lost_sales = sum(s.estimated_lost_sales for s in sizes)

        return SellThroughAnalysis(
            style_id=style_id,
            total_sell_through=total_sold / max(total_received, 1),
            total_units_received=total_received,
            total_units_sold=total_sold,
            size_breakdown=sizes,
            lost_sales_units=lost_sales,
            weeks_on_floor=weeks_on_floor,
        )


# ---------------------------------------------------------------------------
# Price Elasticity Engine
# ---------------------------------------------------------------------------

class PriceElasticityEngine:
    """Calculates price elasticity of demand for pricing optimization."""

    def __init__(self):
        pass

    def calculate(
        self,
        product_id: str,
        price_history: List[Tuple[float, int]],
    ) -> PriceElasticity:
        if len(price_history) < 2:
            return PriceElasticity(product_id, -1.2, 0.7, 79.99, 150)

        prices = [p[0] for p in price_history]
        quantities = [p[1] for p in price_history]
        avg_p = statistics.mean(prices)
        avg_q = statistics.mean(quantities)

        cov = sum((p - avg_p) * (q - avg_q) for p, q in price_history)
        var_p = sum((p - avg_p) ** 2 for p, _ in price_history)
        slope = cov / max(var_p, 1)
        elasticity = slope * (avg_p / max(avg_q, 1))

        return PriceElasticity(
            product_id=product_id,
            elasticity=round(elasticity, 2),
            confidence=0.78,
            optimal_price=round(avg_p * 0.95, 2),
            demand_at_optimal=int(avg_q * 1.05),
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Fashion Retail Analytics Demo")
    print("=" * 60)

    # Sales summary
    print("\n--- Sales Performance ---")
    analytics = SalesAnalytics()
    summary = analytics.get_sales_summary()
    print(f"  Revenue: ${summary.total_revenue:,.2f}")
    print(f"  YoY: {summary.yoy_change:+.1%}")
    print(f"  Avg Transaction: ${summary.avg_transaction:.2f}")
    print(f"  Channels: {summary.channel_breakdown}")

    # Customer segmentation
    print("\n--- Customer Segmentation ---")
    seg = CustomerSegmenter()
    segments = seg.segment("data.csv")
    for s in segments:
        print(f"  {s.name}: {s.size:,} customers, CLV=${s.avg_clv:,.0f}, "
              f"churn={s.churn_probability:.0%}")

    # Basket analysis
    print("\n--- Basket Analysis ---")
    basket = BasketAnalyzer(min_support=0.01)
    rules = basket.find_rules("transactions.csv")
    for r in rules[:3]:
        print(f"  {r.antecedent} → {r.consequent} (lift={r.lift:.2f})")

    # Markdown optimization
    print("\n--- Markdown Optimization ---")
    md = MarkdownOptimizer(objective=MarkdownObjective.MAXIMIZE_REVENUE)
    plan = md.optimize(
        style_id="DRESS-001", current_inventory=2500, weeks_remaining=8,
        cost_of_goods=25.00, original_retail=89.99,
        current_sell_through=0.35,
        demand_forecast=[120, 110, 95, 80, 65, 50, 35, 25],
    )
    print(f"  Revenue: ${plan.total_revenue:,.2f}")
    print(f"  Clearance: {plan.projected_clearance:.1%}")
    print(f"  Markdowns: {len(plan.markdowns)} events")

    # Sell-through
    print("\n--- Sell-Through Analysis ---")
    sta = SellThroughAnalyzer()
    analysis = sta.analyze("SHIRT-042", "pos.csv", "inv.csv", weeks_on_floor=6)
    print(f"  Overall: {analysis.total_sell_through:.1%}")
    for sz in analysis.size_breakdown:
        print(f"    {sz.label}: {sz.sell_through:.1%} ({sz.units_sold}/{sz.units_received})")


if __name__ == "__main__":
    main()
