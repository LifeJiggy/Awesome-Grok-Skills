"""
Real Estate Agent
Property valuation, market analysis, investment analysis,
portfolio management, and due diligence.

Comprehensive implementation featuring:
- Property valuation (comparable sales, income, cost approaches)
- Market analysis and trend detection
- Investment ROI and cash flow analysis
- Mortgage calculation and amortization
- Portfolio management and rebalancing
- Due diligence checklist automation
- Rental yield optimization
- Tax impact analysis
- Neighborhood scoring
- Property comparison
- Market cycle analysis
- Risk assessment
"""

from __future__ import annotations

import abc
import collections
import json
import logging
import math
import statistics
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PropertyType(Enum):
    """Types of real estate properties."""
    SINGLE_FAMILY = "single_family"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    MULTI_FAMILY = "multi_family"
    APARTMENT = "apartment"
    LAND = "land"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MIXED_USE = "mixed_use"


class ListingStatus(Enum):
    """Property listing statuses."""
    ACTIVE = "active"
    PENDING = "pending"
    SOLD = "sold"
    OFF_MARKET = "off_market"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"


class PropertyCondition(Enum):
    """Physical condition of a property."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    NEEDS_RENOVATION = "needs_renovation"


class MarketCycle(Enum):
    """Real estate market cycles."""
    RECOVERY = "recovery"
    EXPANSION = "expansion"
    HYPER_SUPPLY = "hyper_supply"
    RECESSION = "recession"


class InvestmentStrategy(Enum):
    """Real estate investment strategies."""
    BUY_AND_HOLD = "buy_and_hold"
    FLIPPING = "flipping"
    RENTAL_INCOME = "rental_income"
    BRRRR = "brrrr"
    WHOLESALE = "wholesale"
    SHORT_TERM_RENTAL = "short_term_rental"
    COMMERCIAL_LEASE = "commercial_lease"
    DEVELOPMENT = "development"


class DueDiligencePhase(Enum):
    """Due diligence phases."""
    INITIAL = "initial"
    UNDER_CONTRACT = "under_contract"
    INSPECTION = "inspection"
    APPRAISAL = "appraisal"
    FINANCING = "financing"
    CLOSING = "closing"
    POST_CLOSING = "post_closing"


class RiskCategory(Enum):
    """Investment risk categories."""
    MARKET = "market"
    LIQUIDITY = "liquidity"
    CREDIT = "credit"
    OPERATIONAL = "operational"
    LEGAL = "legal"
    ENVIRONMENTAL = "environmental"
    NATURAL_DISASTER = "natural_disaster"
    REGULATORY = "regulatory"


class TaxType(Enum):
    """Property tax types."""
    PROPERTY_TAX = "property_tax"
    INCOME_TAX = "income_tax"
    CAPITAL_GAINS = "capital_gains"
    DEPRECIATION = "depreciation"
    SALES_TAX = "sales_tax"
    TRANSFER_TAX = "transfer_tax"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Property:
    """A real estate property."""
    property_id: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: PropertyType
    listing_status: ListingStatus
    condition: PropertyCondition
    price: float
    bedrooms: int
    bathrooms: float
    sqft: int
    lot_size_sqft: int
    year_built: int
    garage_spaces: int
    stories: int
    hoa_monthly: float
    features: List[str]
    photos: List[str]
    mls_number: Optional[str]
    listing_date: Optional[datetime]
    sold_date: Optional[datetime]
    sold_price: Optional[float]
    latitude: float = 0.0
    longitude: float = 0.0
    property_taxes_annual: float = 0.0


@dataclass
class ComparableSale:
    """A comparable property sale."""
    comp_id: str
    address: str
    property_type: PropertyType
    sold_price: float
    sold_date: datetime
    sqft: int
    bedrooms: int
    bathrooms: float
    lot_size_sqft: int
    year_built: int
    condition: PropertyCondition
    distance_miles: float
    adjustments: Dict[str, float]


@dataclass
class ValuationResult:
    """Property valuation result."""
    valuation_id: str
    property_id: str
    method: str
    estimated_value: float
    confidence: float
    comparables_used: int
    adjustments_total: float
    price_per_sqft: float
    value_range: Tuple[float, float]
    calculated_at: datetime


@dataclass
class MarketData:
    """Market-level data."""
    market_id: str
    name: str
    median_price: float
    avg_price_per_sqft: float
    median_rent: float
    vacancy_rate: float
    cap_rate: float
    days_on_market: int
    inventory_months: float
    price_change_yoy: float
    rent_change_yoy: float
    population_growth: float
    employment_growth: float
    median_household_income: float
    market_cycle: MarketCycle
    last_updated: datetime


@dataclass
class NeighborhoodScore:
    """Neighborhood quality score."""
    neighborhood_id: str
    name: str
    walkability: float
    transit_score: float
    bike_score: float
    school_rating: float
    crime_index: float
    median_income: float
    appreciation_rate: float
    overall_score: float
    amenities: List[str]


@dataclass
class InvestmentAnalysis:
    """Investment analysis result."""
    analysis_id: str
    property_id: str
    strategy: InvestmentStrategy
    purchase_price: float
    down_payment: float
    loan_amount: float
    interest_rate: float
    loan_term_years: int
    monthly_rental_income: float
    monthly_expenses: float
    cash_flow_monthly: float
    cap_rate: float
    cash_on_cash_return: float
    roi_5yr: float
    roi_10yr: float
    break_even_years: float
    total_cash_needed: float


@dataclass
class MortgageCalculation:
    """Mortgage calculation result."""
    mortgage_id: str
    home_price: float
    down_payment: float
    down_payment_pct: float
    loan_amount: float
    interest_rate: float
    loan_term_years: int
    monthly_payment: float
    principal_interest: float
    property_tax_monthly: float
    insurance_monthly: float
    pmi_monthly: float
    total_monthly: float
    total_interest: float
    total_cost: float
    payoff_date: datetime
    amortization_schedule: List[Dict[str, Any]]


@dataclass
class RentalAnalysis:
    """Rental income analysis."""
    analysis_id: str
    property_id: str
    monthly_rent: float
    annual_rent: float
    vacancy_loss: float
    effective_gross_income: float
    operating_expenses: Dict[str, float]
    net_operating_income: float
    gross_yield: float
    net_yield: float
    rent_per_sqft: float
    market_rent_comparison: float


@dataclass
class PortfolioProperty:
    """A property in an investment portfolio."""
    portfolio_property_id: str
    property_id: str
    acquisition_price: float
    acquisition_date: datetime
    current_value: float
    monthly_income: float
    monthly_expenses: float
    equity: float
    strategy: InvestmentStrategy


@dataclass
class DueDiligenceChecklist:
    """A due diligence checklist."""
    checklist_id: str
    property_id: str
    phase: DueDiligencePhase
    items: List[DueDiligenceItem]
    completed_count: int
    total_count: int


@dataclass
class DueDiligenceItem:
    """A single due diligence item."""
    item_id: str
    name: str
    description: str
    required: bool
    completed: bool
    notes: str
    completed_at: Optional[datetime] = None


@dataclass
class TaxAnalysis:
    """Tax impact analysis."""
    analysis_id: str
    property_id: str
    annual_property_tax: float
    annual_income_tax_benefit: float
    depreciation_deduction: float
    net_tax_impact: float
    effective_tax_rate: float
    tax_strategies: List[str]


@dataclass
class PropertyRisk:
    """A property risk assessment."""
    risk_id: str
    property_id: str
    category: RiskCategory
    description: str
    probability: float
    impact: float
    risk_score: float
    mitigation: str


@dataclass
class MarketTrend:
    """A market trend observation."""
    trend_id: str
    market_id: str
    indicator: str
    direction: str
    magnitude: float
    period_months: int
    confidence: float
    data_points: List[Dict[str, Any]]


@dataclass
class RealEstateConfig:
    """Configuration for the real estate agent."""
    default_currency: str = "USD"
    default_mortgage_rate: float = 6.5
    default_loan_term: int = 30
    default_down_payment_pct: float = 20.0
    default_vacancy_rate: float = 0.05
    default_maintenance_rate: float = 0.01
    default_management_fee_rate: float = 0.08
    default_insurance_rate: float = 0.005
    comparable_search_radius_miles: float = 5.0
    max_comparables: int = 10
    min_comparables: int = 3
    appreciation_rate_default: float = 0.03
    discount_rate_default: float = 0.08
    holding_cost_monthly_rate: float = 0.005


# ---------------------------------------------------------------------------
# Property Valuation Engine
# ---------------------------------------------------------------------------

class PropertyValuationEngine:
    """Values properties using comparable sales, income, and cost approaches."""

    def __init__(self, config: Optional[RealEstateConfig] = None) -> None:
        self.config = config or RealEstateConfig()
        self.properties: Dict[str, Property] = {}
        self.comparables: Dict[str, List[ComparableSale]] = {}
        self-valuations: Dict[str, List[ValuationResult]] = {}

    def register_property(self, property_obj: Property) -> None:
        self.properties[property_obj.property_id] = property_obj
        logger.info("Property registered: %s", property_obj.address)

    def add_comparable(self, property_id: str, comp: ComparableSale) -> None:
        self.comparables.setdefault(property_id, []).append(comp)

    def comparable_sales_valuation(
        self,
        property_id: str,
        comps: Optional[List[ComparableSale]] = None,
    ) -> ValuationResult:
        prop = self._get_property(property_id)
        comp_list = comps or self.comparables.get(property_id, [])
        if len(comp_list) < self.config.min_comparables:
            raise ValueError(
                f"need at least {self.config.min_comparables} comparables, got {len(comp_list)}"
            )
        adjusted_prices: List[float] = []
        total_adjustments = 0.0
        for comp in comp_list:
            adjustment = self._calculate_adjustments(prop, comp)
            adjusted_price = comp.sold_price + adjustment
            adjusted_prices.append(adjusted_price)
            total_adjustments += abs(adjustment)
        estimated = statistics.mean(adjusted_prices)
        std_dev = statistics.stdev(adjusted_prices) if len(adjusted_prices) > 1 else estimated * 0.05
        confidence = max(0.5, min(1.0 - (std_dev / estimated), 1.0))
        result = ValuationResult(
            valuation_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            method="comparable_sales",
            estimated_value=round(estimated, 2),
            confidence=round(confidence, 3),
            comparables_used=len(comp_list),
            adjustments_total=round(total_adjustments, 2),
            price_per_sqft=round(estimated / prop.sqft, 2) if prop.sqft else 0,
            value_range=(round(estimated - 1.96 * std_dev, 2), round(estimated + 1.96 * std_dev, 2)),
            calculated_at=datetime.utcnow(),
        )
        self._valuations.setdefault(property_id, []).append(result)
        return result

    def income_approach_valuation(
        self,
        property_id: str,
        annual_rental_income: float,
        cap_rate: float,
        vacancy_rate: float = 0.05,
    ) -> ValuationResult:
        prop = self._get_property(property_id)
        egi = annual_rental_income * (1 - vacancy_rate)
        value = egi / cap_rate if cap_rate > 0 else 0
        confidence = 0.7 if 0.03 <= cap_rate <= 0.12 else 0.5
        result = ValuationResult(
            valuation_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            method="income_approach",
            estimated_value=round(value, 2),
            confidence=round(confidence, 3),
            comparables_used=0,
            adjustments_total=0.0,
            price_per_sqft=round(value / prop.sqft, 2) if prop.sqft else 0,
            value_range=(round(value * 0.85, 2), round(value * 1.15, 2)),
            calculated_at=datetime.utcnow(),
        )
        self._valuations.setdefault(property_id, []).append(result)
        return result

    def cost_approach_valuation(
        self,
        property_id: str,
        land_value: float,
        replacement_cost_per_sqft: float,
        depreciation_pct: float,
    ) -> ValuationResult:
        prop = self._get_property(property_id)
        replacement_cost = prop.sqft * replacement_cost_per_sqft
        depreciation = replacement_cost * depreciation_pct
        value = land_value + replacement_cost - depreciation
        result = ValuationResult(
            valuation_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            method="cost_approach",
            estimated_value=round(value, 2),
            confidence=0.65,
            comparables_used=0,
            adjustments_total=0.0,
            price_per_sqft=round(value / prop.sqft, 2) if prop.sqft else 0,
            value_range=(round(value * 0.9, 2), round(value * 1.1, 2)),
            calculated_at=datetime.utcnow(),
        )
        self._valuations.setdefault(property_id, []).append(result)
        return result

    def auto_valuation(self, property_id: str) -> ValuationResult:
        results: List[ValuationResult] = []
        try:
            if self.comparables.get(property_id):
                results.append(self.comparable_sales_valuation(property_id))
        except ValueError:
            pass
        if not results:
            prop = self._get_property(property_id)
            fallback_value = prop.sqft * 300
            result = ValuationResult(
                valuation_id=str(uuid.uuid4())[:12],
                property_id=property_id,
                method="estimated",
                estimated_value=fallback_value,
                confidence=0.4,
                comparables_used=0,
                adjustments_total=0.0,
                price_per_sqft=300.0,
                value_range=(fallback_value * 0.8, fallback_value * 1.2),
                calculated_at=datetime.utcnow(),
            )
            return result
        return min(results, key=lambda r: abs(r.confidence - 0.9))

    def price_analysis(self, property_id: str) -> Dict[str, Any]:
        prop = self._get_property(property_id)
        valuations = self._valuations.get(property_id, [])
        comps = self.comparables.get(property_id, [])
        return {
            "property": prop.address,
            "list_price": prop.price,
            "price_per_sqft": round(prop.price / prop.sqft, 2) if prop.sqft else 0,
            "valuations": [
                {"method": v.method, "value": v.estimated_value, "confidence": v.confidence}
                for v in valuations
            ],
            "comparable_count": len(comps),
            "assessment": self._price_assessment(prop, valuations),
        }

    def _calculate_adjustments(self, prop: Property, comp: ComparableSale) -> float:
        adjustment = 0.0
        sqft_diff = prop.sqft - comp.sqft
        adjustment += sqft_diff * 150
        bed_diff = prop.bedrooms - comp.bedrooms
        adjustment += bed_diff * 10000
        bath_diff = prop.bathrooms - comp.bathrooms
        adjustment += bath_diff * 7500
        year_diff = prop.year_built - comp.year_built
        adjustment += year_diff * 500
        return adjustment

    def _price_assessment(
        self, prop: Property, valuations: List[ValuationResult]
    ) -> str:
        if not valuations:
            return "no_valuations"
        avg_val = statistics.mean(v.estimated_value for v in valuations)
        ratio = prop.price / avg_val if avg_val else 1
        if ratio < 0.95:
            return "undervalued"
        elif ratio > 1.05:
            return "overvalued"
        return "fairly_priced"

    def _get_property(self, property_id: str) -> Property:
        if property_id not in self.properties:
            raise ValueError(f"property {property_id} not found")
        return self.properties[property_id]


# ---------------------------------------------------------------------------
# Market Analyzer
# ---------------------------------------------------------------------------

class MarketAnalyzer:
    """Analyzes real estate market conditions and trends."""

    def __init__(self) -> None:
        self.markets: Dict[str, MarketData] = {}
        self.neighborhoods: Dict[str, NeighborhoodScore] = {}
        self._trends: List[MarketTrend] = []

    def register_market(self, market: MarketData) -> None:
        self.markets[market.market_id] = market
        logger.info("Market registered: %s", market.name)

    def register_neighborhood(self, neighborhood: NeighborhoodScore) -> None:
        self.neighborhoods[neighborhood.neighborhood_id] = neighborhood

    def market_health(self, market_id: str) -> Dict[str, Any]:
        market = self._get_market(market_id)
        indicators: Dict[str, str] = {}
        indicators["price_trend"] = "up" if market.price_change_yoy > 0 else "down"
        indicators["rent_trend"] = "up" if market.rent_change_yoy > 0 else "down"
        indicators["supply"] = "low" if market.inventory_months < 3 else "balanced" if market.inventory_months < 6 else "high"
        indicators["demand"] = "strong" if market.days_on_market < 30 else "moderate" if market.days_on_market < 60 else "weak"
        health_score = self._calculate_health_score(market)
        return {
            "market": market.name,
            "health_score": health_score,
            "indicators": indicators,
            "market_cycle": market.market_cycle.value,
            "recommendation": self._market_recommendation(market),
        }

    def compare_markets(self, market_ids: List[str]) -> Dict[str, Any]:
        markets = [self._get_market(mid) for mid in market_ids]
        comparison: List[Dict[str, Any]] = []
        for m in markets:
            comparison.append({
                "market": m.name,
                "median_price": m.median_price,
                "cap_rate": m.cap_rate,
                "appreciation": m.price_change_yoy,
                "vacancy": m.vacancy_rate,
                "dom": m.days_on_market,
                "population_growth": m.population_growth,
            })
        best_appreciation = max(comparison, key=lambda x: x["appreciation"])
        best_yield = max(comparison, key=lambda x: x["cap_rate"])
        return {
            "markets": comparison,
            "best_for_appreciation": best_appreciation["market"],
            "best_for_yield": best_yield["market"],
        }

    def neighborhood_ranking(
        self, neighborhood_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        nh_list = list(self.neighborhoods.values())
        if neighborhood_ids:
            nh_list = [n for n in nh_list if n.neighborhood_id in neighborhood_ids]
        ranked = sorted(nh_list, key=lambda n: n.overall_score, reverse=True)
        return [
            {
                "rank": i + 1,
                "name": n.name,
                "overall_score": n.overall_score,
                "walkability": n.walkability,
                "school_rating": n.school_rating,
                "crime_index": n.crime_index,
                "appreciation": n.appreciation_rate,
            }
            for i, n in enumerate(ranked)
        ]

    def trend_analysis(self, market_id: str, months: int = 12) -> Dict[str, Any]:
        market = self._get_market(market_id)
        return {
            "market": market.name,
            "period_months": months,
            "price_change_yoy": market.price_change_yoy,
            "rent_change_yoy": market.rent_change_yoy,
            "population_growth": market.population_growth,
            "employment_growth": market.employment_growth,
            "market_cycle": market.market_cycle.value,
            "forecast": self._generate_forecast(market),
        }

    def investment_hotspots(self) -> List[Dict[str, Any]]:
        hotspots: List[Dict[str, Any]] = []
        for market in self.markets.values():
            score = (
                market.price_change_yoy * 30
                + market.population_growth * 25
                + market.employment_growth * 20
                + market.cap_rate * 100 * 15
                + (1 - market.vacancy_rate) * 10
            )
            hotspots.append({
                "market": market.name,
                "score": round(score, 2),
                "median_price": market.median_price,
                "cap_rate": market.cap_rate,
                "appreciation": market.price_change_yoy,
            })
        return sorted(hotspots, key=lambda x: x["score"], reverse=True)

    def _calculate_health_score(self, market: MarketData) -> float:
        score = 50.0
        if market.price_change_yoy > 0:
            score += min(market.price_change_yoy * 5, 15)
        else:
            score += max(market.price_change_yoy * 5, -15)
        if market.vacancy_rate < 0.05:
            score += 10
        elif market.vacancy_rate > 0.1:
            score -= 10
        if market.days_on_market < 30:
            score += 10
        elif market.days_on_market > 90:
            score -= 10
        if market.population_growth > 0.02:
            score += 10
        elif market.population_growth < 0:
            score -= 10
        return round(max(min(score, 100), 0), 1)

    def _market_recommendation(self, market: MarketData) -> str:
        cycle = market.market_cycle
        if cycle == MarketCycle.RECOVERY:
            return "Buy — prices at bottom, strong upside potential"
        if cycle == MarketCycle.EXPANSION:
            return "Buy cautiously — good fundamentals but prices rising"
        if cycle == MarketCycle.HYPER_SUPPLY:
            return "Wait — oversupply may push prices down"
        return "Sell/hold — declining market, limit exposure"

    def _generate_forecast(self, market: MarketData) -> Dict[str, Any]:
        return {
            "6_month": {
                "price_change_pct": round(market.price_change_yoy / 2, 2),
                "outlook": "stable" if abs(market.price_change_yoy) < 5 else "volatile",
            },
            "12_month": {
                "price_change_pct": market.price_change_yoy,
                "outlook": market.market_cycle.value,
            },
            "24_month": {
                "price_change_pct": round(market.price_change_yoy * 1.5, 2),
                "outlook": "growth" if market.price_change_yoy > 0 else "decline",
            },
        }

    def _get_market(self, market_id: str) -> MarketData:
        if market_id not in self.markets:
            raise ValueError(f"market {market_id} not found")
        return self.markets[market_id]


# ---------------------------------------------------------------------------
# Investment Analyzer
# ---------------------------------------------------------------------------

class InvestmentAnalyzer:
    """Analyzes real estate investment opportunities."""

    def __init__(self, config: Optional[RealEstateConfig] = None) -> None:
        self.config = config or RealEstateConfig()
        self._analyses: Dict[str, InvestmentAnalysis] = {}

    def analyze_property(
        self,
        property_id: str,
        purchase_price: float,
        down_payment_pct: float,
        interest_rate: float,
        loan_term_years: int,
        monthly_rental_income: float,
        monthly_expenses: float,
        strategy: InvestmentStrategy = InvestmentStrategy.BUY_AND_HOLD,
    ) -> InvestmentAnalysis:
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        monthly_rate = interest_rate / 100 / 12
        num_payments = loan_term_years * 12
        if monthly_rate > 0:
            monthly_pi = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** num_payments
            ) / ((1 + monthly_rate) ** num_payments - 1)
        else:
            monthly_pi = loan_amount / num_payments
        cash_flow = monthly_rental_income - monthly_expenses - monthly_pi
        annual_noi = (monthly_rental_income - monthly_expenses) * 12
        cap_rate = (annual_noi / purchase_price * 100) if purchase_price else 0
        total_cash = down_payment + purchase_price * 0.03
        cash_on_cash = (cash_flow * 12 / total_cash * 100) if total_cash else 0
        appreciation = self.config.appreciation_rate_default
        equity_5yr = purchase_price * ((1 + appreciation) ** 5 - 1) + (cash_flow * 12 * 5)
        roi_5yr = (equity_5yr / total_cash * 100) if total_cash else 0
        equity_10yr = purchase_price * ((1 + appreciation) ** 10 - 1) + (cash_flow * 12 * 10)
        roi_10yr = (equity_10yr / total_cash * 100) if total_cash else 0
        break_even = (total_cash / (cash_flow * 12)) if cash_flow > 0 else float("inf")
        analysis = InvestmentAnalysis(
            analysis_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            strategy=strategy,
            purchase_price=purchase_price,
            down_payment=down_payment,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            loan_term_years=loan_term_years,
            monthly_rental_income=monthly_rental_income,
            monthly_expenses=monthly_expenses,
            cash_flow_monthly=round(cash_flow, 2),
            cap_rate=round(cap_rate, 2),
            cash_on_cash_return=round(cash_on_cash, 2),
            roi_5yr=round(roi_5yr, 2),
            roi_10yr=round(roi_10yr, 2),
            break_even_years=round(break_even, 1),
            total_cash_needed=round(total_cash, 2),
        )
        self._analyses[property_id] = analysis
        logger.info("Investment analysis completed for property: %s", property_id)
        return analysis

    def flip_analysis(
        self,
        purchase_price: float,
        renovation_cost: float,
        holding_months: int,
        after_repair_value: float,
        closing_cost_buy_pct: float = 0.03,
        closing_cost_sell_pct: float = 0.06,
        holding_cost_monthly_pct: float = 0.005,
    ) -> Dict[str, Any]:
        closing_buy = purchase_price * closing_cost_buy_pct
        closing_sell = after_repair_value * closing_cost_sell_pct
        holding_costs = purchase_price * holding_cost_monthly_pct * holding_months
        total_investment = purchase_price + renovation_cost + closing_buy + holding_costs
        profit = after_repair_value - total_investment - closing_sell
        roi = (profit / total_investment * 100) if total_investment else 0
        monthly_profit = profit / holding_months if holding_months else 0
        return {
            "purchase_price": purchase_price,
            "renovation_cost": renovation_cost,
            "holding_costs": round(holding_costs, 2),
            "closing_costs_total": round(closing_buy + closing_sell, 2),
            "total_investment": round(total_investment, 2),
            "after_repair_value": after_repair_value,
            "profit": round(profit, 2),
            "roi_pct": round(roi, 2),
            "monthly_profit": round(monthly_profit, 2),
            "holding_months": holding_months,
        }

    def cash_flow_projection(
        self,
        monthly_rental: float,
        monthly_expenses: float,
        mortgage_payment: float,
        years: int = 10,
        rent_growth_pct: float = 0.03,
        expense_growth_pct: float = 0.02,
    ) -> List[Dict[str, Any]]:
        projections: List[Dict[str, Any]] = []
        for year in range(1, years + 1):
            rent = monthly_rental * (1 + rent_growth_pct) ** year
            expenses = monthly_expenses * (1 + expense_growth_pct) ** year
            net = rent - expenses - mortgage_payment
            projections.append({
                "year": year,
                "monthly_rental": round(rent, 2),
                "monthly_expenses": round(expenses, 2),
                "net_cash_flow": round(net, 2),
                "annual_cash_flow": round(net * 12, 2),
            })
        return projections

    def _get_analysis(self, property_id: str) -> InvestmentAnalysis:
        if property_id not in self._analyses:
            raise ValueError(f"analysis not found for property {property_id}")
        return self._analyses[property_id]


# ---------------------------------------------------------------------------
# Mortgage Calculator
# ---------------------------------------------------------------------------

class MortgageCalculator:
    """Calculates mortgage payments and amortization schedules."""

    def __init__(self, config: Optional[RealEstateConfig] = None) -> None:
        self.config = config or RealEstateConfig()

    def calculate(
        self,
        home_price: float,
        down_payment_pct: float,
        interest_rate: float,
        loan_term_years: int,
        property_tax_annual: float = 0,
        insurance_annual: float = 0,
        pmi_rate: float = 0,
    ) -> MortgageCalculation:
        down_payment = home_price * (down_payment_pct / 100)
        loan_amount = home_price - down_payment
        monthly_rate = interest_rate / 100 / 12
        num_payments = loan_term_years * 12
        if monthly_rate > 0:
            pi = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** num_payments
            ) / ((1 + monthly_rate) ** num_payments - 1)
        else:
            pi = loan_amount / num_payments
        tax_monthly = property_tax_annual / 12
        ins_monthly = insurance_annual / 12
        pmi_monthly = loan_amount * pmi_rate / 12 if pmi_rate > 0 and down_payment_pct < 20 else 0
        total_monthly = pi + tax_monthly + ins_monthly + pmi_monthly
        total_interest = pi * num_payments - loan_amount
        total_cost = down_payment + pi * num_payments + tax_monthly * num_payments + ins_monthly * num_payments
        payoff_date = datetime.utcnow() + timedelta(days=loan_term_years * 365)
        schedule = self._amortization_schedule(loan_amount, monthly_rate, pi, num_payments)
        return MortgageCalculation(
            mortgage_id=str(uuid.uuid4())[:12],
            home_price=home_price,
            down_payment=round(down_payment, 2),
            down_payment_pct=down_payment_pct,
            loan_amount=round(loan_amount, 2),
            interest_rate=interest_rate,
            loan_term_years=loan_term_years,
            monthly_payment=round(total_monthly, 2),
            principal_interest=round(pi, 2),
            property_tax_monthly=round(tax_monthly, 2),
            insurance_monthly=round(ins_monthly, 2),
            pmi_monthly=round(pmi_monthly, 2),
            total_monthly=round(total_monthly, 2),
            total_interest=round(total_interest, 2),
            total_cost=round(total_cost, 2),
            payoff_date=payoff_date,
            amortization_schedule=schedule,
        )

    def compare_rates(
        self,
        loan_amount: float,
        rates: List[float],
        term_years: int = 30,
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for rate in rates:
            calc = self.calculate(
                home_price=loan_amount / 0.8,
                down_payment_pct=20,
                interest_rate=rate,
                loan_term_years=term_years,
            )
            results.append({
                "rate": rate,
                "monthly_payment": calc.principal_interest,
                "total_interest": calc.total_interest,
            })
        return results

    def _amortization_schedule(
        self,
        loan_amount: float,
        monthly_rate: float,
        monthly_payment: float,
        num_payments: int,
    ) -> List[Dict[str, Any]]:
        schedule: List[Dict[str, Any]] = []
        balance = loan_amount
        for month in range(1, min(num_payments + 1, 361)):
            interest = balance * monthly_rate
            principal = monthly_payment - interest
            balance -= principal
            if balance < 0:
                balance = 0
            schedule.append({
                "month": month,
                "payment": round(monthly_payment, 2),
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "balance": round(balance, 2),
            })
            if balance <= 0:
                break
        return schedule


# ---------------------------------------------------------------------------
# Rental Analyzer
# ---------------------------------------------------------------------------

class RentalAnalyzer:
    """Analyzes rental income potential and optimization."""

    def __init__(self, config: Optional[RealEstateConfig] = None) -> None:
        self.config = config or RealEstateConfig()

    def analyze_rental(
        self,
        property_id: str,
        monthly_rent: float,
        property_tax_annual: float,
        insurance_annual: float,
        hoa_monthly: float,
        maintenance_annual: float,
        management_fee_pct: float = 0.08,
    ) -> RentalAnalysis:
        annual_rent = monthly_rent * 12
        vacancy_loss = annual_rent * self.config.default_vacancy_rate
        egi = annual_rent - vacancy_loss
        expenses = {
            "property_tax": property_tax_annual,
            "insurance": insurance_annual,
            "hoa": hoa_monthly * 12,
            "maintenance": maintenance_annual,
            "management": egi * management_fee_pct,
            "vacancy_loss": vacancy_loss,
        }
        total_expenses = sum(expenses.values())
        noi = egi - total_expenses
        gross_yield = (annual_rent / (annual_rent + 100000) * 100) if annual_rent else 0
        net_yield = (noi / (annual_rent + 100000) * 100) if noi else 0
        return RentalAnalysis(
            analysis_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            monthly_rent=monthly_rent,
            annual_rent=annual_rent,
            vacancy_loss=round(vacancy_loss, 2),
            effective_gross_income=round(egi, 2),
            operating_expenses=expenses,
            net_operating_income=round(noi, 2),
            gross_yield=round(gross_yield, 2),
            net_yield=round(net_yield, 2),
            rent_per_sqft=0,
            market_rent_comparison=0,
        )

    def rent_optimization(
        self, current_rent: float, market_avg: float, occupancy_rate: float
    ) -> Dict[str, Any]:
        revenue = current_rent * occupancy_rate
        scenarios: List[Dict[str, Any]] = []
        for pct in [-10, -5, 0, 5, 10, 15]:
            new_rent = current_rent * (1 + pct / 100)
            new_occupancy = max(0.5, occupancy_rate - pct * 0.02)
            new_revenue = new_rent * new_occupancy
            scenarios.append({
                "rent_change_pct": pct,
                "new_rent": round(new_rent, 2),
                "estimated_occupancy": round(new_occupancy, 3),
                "monthly_revenue": round(new_revenue, 2),
            })
        best = max(scenarios, key=lambda s: s["monthly_revenue"])
        return {
            "current": {"rent": current_rent, "occupancy": occupancy_rate, "revenue": round(revenue, 2)},
            "scenarios": scenarios,
            "recommended": best,
            "market_average": market_avg,
        }


# ---------------------------------------------------------------------------
# Portfolio Manager
# ---------------------------------------------------------------------------

class PortfolioManager:
    """Manages real estate investment portfolios."""

    def __init__(self, config: Optional[RealEstateConfig] = None) -> None:
        self.config = config or RealEstateConfig()
        self.properties: Dict[str, PortfolioProperty] = {}

    def add_property(self, portfolio_property: PortfolioProperty) -> None:
        self.properties[portfolio_property.portfolio_property_id] = portfolio_property
        logger.info("Portfolio property added: %s", portfolio_property.property_id)

    def remove_property(self, portfolio_property_id: str) -> None:
        if portfolio_property_id not in self.properties:
            raise ValueError(f"portfolio property {portfolio_property_id} not found")
        del self.properties[portfolio_property_id]

    def portfolio_summary(self) -> Dict[str, Any]:
        props = list(self.properties.values())
        if not props:
            return {"total_properties": 0}
        total_value = sum(p.current_value for p in props)
        total_equity = sum(p.equity for p in props)
        total_monthly_income = sum(p.monthly_income for p in props)
        total_monthly_expenses = sum(p.monthly_expenses for p in props)
        total_investment = sum(p.acquisition_price for p in props)
        return {
            "total_properties": len(props),
            "total_value": round(total_value, 2),
            "total_equity": round(total_equity, 2),
            "total_investment": round(total_investment, 2),
            "total_monthly_income": round(total_monthly_income, 2),
            "total_monthly_expenses": round(total_monthly_expenses, 2),
            "net_monthly_cash_flow": round(total_monthly_income - total_monthly_expenses, 2),
            "portfolio_roi": round((total_equity / total_investment * 100) if total_investment else 0, 2),
            "avg_cap_rate": round(
                statistics.mean(
                    ((p.monthly_income - p.monthly_expenses) * 12 / p.current_value * 100)
                    for p in props if p.current_value > 0
                ), 2
            ) if props else 0,
        }

    def allocation_by_type(self) -> Dict[str, float]:
        total_value = sum(p.current_value for p in self.properties.values())
        if total_value == 0:
            return {}
        by_strategy: Dict[str, float] = {}
        for p in self.properties.values():
            key = p.strategy.value
            by_strategy[key] = by_strategy.get(key, 0) + p.current_value
        return {k: round(v / total_value * 100, 1) for k, v in by_strategy.items()}

    def rebalance_suggestions(self) -> List[Dict[str, Any]]:
        allocation = self.allocation_by_type()
        suggestions: List[Dict[str, Any]] = []
        for strategy, pct in allocation.items():
            if pct > 40:
                suggestions.append({
                    "strategy": strategy,
                    "current_pct": pct,
                    "suggestion": "over-allocated — consider diversifying",
                })
            elif pct < 10:
                suggestions.append({
                    "strategy": strategy,
                    "current_pct": pct,
                    "suggestion": "under-allocated — consider adding properties",
                })
        return suggestions

    def performance_history(self) -> List[Dict[str, Any]]:
        return sorted(
            [
                {
                    "property_id": p.property_id,
                    "acquisition_price": p.acquisition_price,
                    "current_value": p.current_value,
                    "appreciation_pct": round(
                        (p.current_value - p.acquisition_price) / p.acquisition_price * 100, 1
                    ) if p.acquisition_price else 0,
                }
                for p in self.properties.values()
            ],
            key=lambda x: x["appreciation_pct"],
            reverse=True,
        )


# ---------------------------------------------------------------------------
# Due Diligence Manager
# ---------------------------------------------------------------------------

class DueDiligenceManager:
    """Manages property due diligence checklists."""

    STANDARD_ITEMS: Dict[DueDiligencePhase, List[Dict[str, Any]]] = {
        DueDiligencePhase.INITIAL: [
            {"name": "Property disclosure review", "required": True},
            {"name": "Preliminary title search", "required": True},
            {"name": "Zoning verification", "required": True},
            {"name": "HOA document review", "required": False},
        ],
        DueDiligencePhase.UNDER_CONTRACT: [
            {"name": "Purchase agreement review", "required": True},
            {"name": "Earnest money deposit", "required": True},
            {"name": "Inspection contingency", "required": True},
            {"name": "Financing contingency", "required": True},
        ],
        DueDiligencePhase.INSPECTION: [
            {"name": "General home inspection", "required": True},
            {"name": "Termite/pest inspection", "required": True},
            {"name": "Roof inspection", "required": True},
            {"name": "HVAC inspection", "required": True},
            {"name": "Plumbing inspection", "required": True},
            {"name": "Electrical inspection", "required": True},
            {"name": "Foundation inspection", "required": True},
            {"name": "Sewer/septic inspection", "required": False},
        ],
        DueDiligencePhase.APPRAISAL: [
            {"name": "Ordered appraisal", "required": True},
            {"name": "Appraisal review", "required": True},
        ],
        DueDiligencePhase.FINANCING: [
            {"name": "Loan application", "required": True},
            {"name": "Income verification", "required": True},
            {"name": "Credit check", "required": True},
            {"name": "Insurance binding", "required": True},
        ],
        DueDiligencePhase.CLOSING: [
            {"name": "Final walkthrough", "required": True},
            {"name": "Title insurance", "required": True},
            {"name": "Closing disclosure review", "required": True},
            {"name": "Wire transfer", "required": True},
        ],
        DueDiligencePhase.POST_CLOSING: [
            {"name": "Record deed", "required": True},
            {"name": "Transfer utilities", "required": True},
            {"name": "Update insurance", "required": True},
            {"name": "Property management setup", "required": False},
        ],
    }

    def create_checklist(
        self, property_id: str, phase: DueDiligencePhase
    ) -> DueDiligenceChecklist:
        items_data = self.STANDARD_ITEMS.get(phase, [])
        items = [
            DueDiligenceItem(
                item_id=str(uuid.uuid4())[:12],
                name=item["name"],
                description=item["name"],
                required=item["required"],
                completed=False,
                notes="",
            )
            for item in items_data
        ]
        checklist = DueDiligenceChecklist(
            checklist_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            phase=phase,
            items=items,
            completed_count=0,
            total_count=len(items),
        )
        return checklist

    def complete_item(
        self, checklist: DueDiligenceChecklist, item_id: str, notes: str = ""
    ) -> DueDiligenceChecklist:
        for item in checklist.items:
            if item.item_id == item_id:
                item.completed = True
                item.completed_at = datetime.utcnow()
                item.notes = notes
                break
        checklist.completed_count = sum(1 for i in checklist.items if i.completed)
        return checklist

    def checklist_progress(self, checklist: DueDiligenceChecklist) -> Dict[str, Any]:
        return {
            "phase": checklist.phase.value,
            "total_items": checklist.total_count,
            "completed": checklist.completed_count,
            "progress_pct": round(
                checklist.completed_count / checklist.total_count * 100, 1
            ) if checklist.total_count else 0,
            "remaining": [
                {"name": i.name, "required": i.required}
                for i in checklist.items if not i.completed
            ],
        }


# ---------------------------------------------------------------------------
# Tax Analyzer
# ---------------------------------------------------------------------------

class TaxAnalyzer:
    """Analyzes tax implications of real estate transactions."""

    def analyze_tax_impact(
        self,
        property_id: str,
        purchase_price: float,
        annual_rental_income: float,
        annual_expenses: float,
        depreciation_years: int = 27,
    ) -> TaxAnalysis:
        property_tax = purchase_price * 0.012
        annual_noi = annual_rental_income - annual_expenses
        depreciation = purchase_price * 0.8 / depreciation_years
        taxable_income = annual_noi - depreciation
        tax_benefit = max(0, -taxable_income) * 0.24
        net_impact = -property_tax + tax_benefit
        strategies = []
        if depreciation > 0:
            strategies.append("Maximize depreciation deductions")
        if annual_noi < 0:
            strategies.append("Loss can offset other income (up to limits)")
        strategies.extend([
            "1031 exchange for deferred capital gains",
            "Opportunity Zone investment for tax benefits",
            "Cost segregation for accelerated depreciation",
        ])
        return TaxAnalysis(
            analysis_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            annual_property_tax=round(property_tax, 2),
            annual_income_tax_benefit=round(tax_benefit, 2),
            depreciation_deduction=round(depreciation, 2),
            net_tax_impact=round(net_impact, 2),
            effective_tax_rate=round(property_tax / purchase_price * 100, 2) if purchase_price else 0,
            tax_strategies=strategies,
        )


# ---------------------------------------------------------------------------
# Risk Assessor
# ---------------------------------------------------------------------------

class RiskAssessor:
    """Assesses risks for real estate investments."""

    def assess_property_risks(
        self,
        property_id: str,
        property_type: PropertyType,
        year_built: int,
        location_risk_factors: Optional[List[str]] = None,
    ) -> List[PropertyRisk]:
        risks: List[PropertyRisk] = []
        age = datetime.utcnow().year - year_built
        if age > 40:
            risks.append(PropertyRisk(
                risk_id=str(uuid.uuid4())[:12],
                property_id=property_id,
                category=RiskCategory.OPERATIONAL,
                description="Aging property may require major systems replacement",
                probability=0.6,
                impact=0.7,
                risk_score=0.42,
                mitigation="Budget for capital improvements; get thorough inspection",
            ))
        risks.append(PropertyRisk(
            risk_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            category=RiskCategory.MARKET,
            description="Market downturn could reduce property value",
            probability=0.3,
            impact=0.8,
            risk_score=0.24,
            mitigation="Long holding period; focus on cash flow over appreciation",
        ))
        risks.append(PropertyRisk(
            risk_id=str(uuid.uuid4())[:12],
            property_id=property_id,
            category=RiskCategory.LIQUIDITY,
            description="Property may take longer to sell than expected",
            probability=0.4,
            impact=0.5,
            risk_score=0.20,
            mitigation="Maintain reserves; price competitively",
        ))
        if property_type in (PropertyType.SINGLE_FAMILY, PropertyType.CONDO):
            risks.append(PropertyRisk(
                risk_id=str(uuid.uuid4())[:12],
                property_id=property_id,
                category=RiskCategory.CREDIT,
                description="Tenant default risk",
                probability=0.2,
                impact=0.6,
                risk_score=0.12,
                mitigation="Thorough tenant screening; security deposit",
            ))
        for factor in (location_risk_factors or []):
            if "flood" in factor.lower():
                risks.append(PropertyRisk(
                    risk_id=str(uuid.uuid4())[:12],
                    property_id=property_id,
                    category=RiskCategory.NATURAL_DISASTER,
                    description="Flood zone location",
                    probability=0.3,
                    impact=0.9,
                    risk_score=0.27,
                    mitigation="Flood insurance required; review FEMA maps",
                ))
        return risks

    def risk_summary(self, risks: List[PropertyRisk]) -> Dict[str, Any]:
        if not risks:
            return {"total_risks": 0}
        avg_score = statistics.mean(r.risk_score for r in risks)
        by_category = collections.Counter(r.category.value for r in risks)
        return {
            "total_risks": len(risks),
            "avg_risk_score": round(avg_score, 3),
            "highest_risk": max(risks, key=lambda r: r.risk_score).description,
            "by_category": dict(by_category),
            "overall_rating": "low" if avg_score < 0.2 else "medium" if avg_score < 0.4 else "high",
        }


# ---------------------------------------------------------------------------
# Property Comparison Engine
# ---------------------------------------------------------------------------

class PropertyComparisonEngine:
    """Compares multiple properties side-by-side."""

    def __init__(self, config: Optional[RealEstateConfig] = None) -> None:
        self.config = config or RealEstateConfig()

    def compare(
        self,
        properties: List[Property],
        weights: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        if len(properties) < 2:
            raise ValueError("need at least 2 properties to compare")
        default_weights = {
            "price": 0.25,
            "sqft": 0.15,
            "condition": 0.15,
            "location": 0.20,
            "value_per_sqft": 0.15,
            "features": 0.10,
        }
        w = weights or default_weights
        comparison: List[Dict[str, Any]] = []
        for prop in properties:
            score = 0.0
            score += (1 - min(prop.price / 1_000_000, 1)) * w.get("price", 0) * 100
            score += min(prop.sqft / 3000, 1) * w.get("sqft", 0) * 100
            condition_score = {
                PropertyCondition.EXCELLENT: 100,
                PropertyCondition.GOOD: 75,
                PropertyCondition.FAIR: 50,
                PropertyCondition.POOR: 25,
                PropertyCondition.NEEDS_RENOVATION: 15,
            }.get(prop.condition, 50)
            score += (condition_score / 100) * w.get("condition", 0) * 100
            score += (prop.price / prop.sqft) * 0.01 if prop.sqft else 0
            comparison.append({
                "property_id": prop.property_id,
                "address": prop.address,
                "price": prop.price,
                "sqft": prop.sqft,
                "bedrooms": prop.bedrooms,
                "bathrooms": prop.bathrooms,
                "year_built": prop.year_built,
                "price_per_sqft": round(prop.price / prop.sqft, 2) if prop.sqft else 0,
                "score": round(score, 2),
            })
        ranked = sorted(comparison, key=lambda x: x["score"], reverse=True)
        return {
            "properties": ranked,
            "winner": ranked[0]["address"] if ranked else None,
            "weights_used": w,
        }


# ---------------------------------------------------------------------------
# Real Estate Agent (Orchestrator)
# ---------------------------------------------------------------------------

class RealEstateAgent:
    """Orchestrates all real estate sub-components."""

    def __init__(self, config: Optional[RealEstateConfig] = None) -> None:
        self.config = config or RealEstateConfig()
        self.valuation = PropertyValuationEngine(self.config)
        self.market = MarketAnalyzer()
        self.investment = InvestmentAnalyzer(self.config)
        self.mortgage = MortgageCalculator(self.config)
        self.rental = RentalAnalyzer(self.config)
        self.portfolio = PortfolioManager(self.config)
        self.due_diligence = DueDiligenceManager()
        self.tax = TaxAnalyzer()
        self.risk = RiskAssessor()
        self.comparison = PropertyComparisonEngine(self.config)
        logger.info("RealEstateAgent initialized")

    def full_status(self) -> Dict[str, Any]:
        return {
            "properties_registered": len(self.valuation.properties),
            "markets_tracked": len(self.market.markets),
            "portfolio": self.portfolio.portfolio_summary(),
            "neighborhoods": len(self.market.neighborhoods),
        }

    def run(self) -> Dict[str, Any]:
        logger.info("RealEstateAgent run starting")
        status = self.full_status()
        logger.info("RealEstateAgent run complete")
        return status


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    agent = RealEstateAgent()
    result = agent.run()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
