"""
Business Development Agent
A comprehensive B2B partnership, deal pipeline, revenue modeling,
market intelligence, and growth strategy engine.
"""

from __future__ import annotations

import logging
import math
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PartnershipType(Enum):
    STRATEGIC = "strategic"
    TECHNOLOGY = "technology"
    DISTRIBUTION = "distribution"
    RESELLER = "reseller"
    MARKETING = "marketing"
    JOINT_VENTURE = "joint_venture"
    LICENSING = "licensing"
    AFFILIATE = "affiliate"


class DealStage(Enum):
    IDENTIFICATION = "identification"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSING = "closing"
    POST_CLOSE = "post_close"
    MAINTENANCE = "maintenance"
    EXPANSION = "expansion"


class MarketSegment(Enum):
    ENTERPRISE = "enterprise"
    SMB = "smb"
    CONSUMER = "consumer"
    GOVERNMENT = "government"
    NON_PROFIT = "non_profit"


class RevenueModel(Enum):
    SUBSCRIPTION = "subscription"
    TRANSACTIONAL = "transactional"
    FREEMIUM = "freemium"
    LICENSING = "licensing"
    ADVERTISING = "advertising"
    MARKETPLACE = "marketplace"
    USAGE_BASED = "usage_based"


class CompetitorPositioning(Enum):
    LEADER = "leader"
    CHALLENGER = "challenger"
    NICHE = "niche"
    EMERGING = "emerging"


class GrowthStrategy(Enum):
    MARKET_PENETRATION = "market_penetration"
    MARKET_DEVELOPMENT = "market_development"
    PRODUCT_DEVELOPMENT = "product_development"
    DIVERSIFICATION = "diversification"


class PipelineHealth(Enum):
    HEALTHY = "healthy"
    AT_RISK = "at_risk"
    STAGNANT = "stagnant"
    DECLINING = "declining"


class NegotiationStyle(Enum):
    COMPETITIVE = "competitive"
    COLLABORATIVE = "collaborative"
    COMPROMISE = "compromise"
    ACCOMMODATING = "accommodating"
    AVOIDING = "avoiding"


class GeographyScope(Enum):
    LOCAL = "local"
    REGIONAL = "regional"
    NATIONAL = "national"
    INTERNATIONAL = "international"
    GLOBAL = "global"


class ValuePropositionType(Enum):
    COST = "cost"
    INNOVATION = "innovation"
    CUSTOMER_INTIMACY = "customer_intimacy"
    ECOSYSTEM = "ecosystem"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Partnership:
    partner_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    partnership_type: PartnershipType = PartnershipType.STRATEGIC
    stage: DealStage = DealStage.IDENTIFICATION
    market_segment: MarketSegment = MarketSegment.ENTERPRISE
    geography: GeographyScope = GeographyScope.NATIONAL
    annual_value: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    health_score: float = 0.5
    synergy_score: float = 0.0
    cultural_fit: float = 0.0
    strategic_alignment: float = 0.0
    contact_person: str = ""
    contact_email: str = ""
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)

    def composite_score(self) -> float:
        weights = {"synergy": 0.30, "cultural": 0.20, "strategic": 0.30, "health": 0.20}
        return (
            self.synergy_score * weights["synergy"]
            + self.cultural_fit * weights["cultural"]
            + self.strategic_alignment * weights["strategic"]
            + self.health_score * weights["health"]
        )

    def is_high_value(self, threshold: float = 0.7) -> bool:
        return self.composite_score() >= threshold and self.annual_value > 50_000

    def remaining_days(self) -> int:
        if self.end_date is None:
            return 365
        delta = self.end_date - datetime.now()
        return max(delta.days, 0)


@dataclass
class DealPipeline:
    pipeline_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    deals: list[Partnership] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    target_revenue: float = 0.0

    def deals_by_stage(self) -> dict[DealStage, list[Partnership]]:
        grouped: dict[DealStage, list[Partnership]] = defaultdict(list)
        for d in self.deals:
            grouped[d.stage].append(d)
        return dict(grouped)

    def weighted_value(self) -> float:
        stage_weights = {
            DealStage.IDENTIFICATION: 0.05,
            DealStage.QUALIFICATION: 0.15,
            DealStage.PROPOSAL: 0.35,
            DealStage.NEGOTIATION: 0.60,
            DealStage.CLOSING: 0.85,
            DealStage.POST_CLOSE: 1.0,
            DealStage.MAINTENANCE: 1.0,
            DealStage.EXPANSION: 1.0,
        }
        return sum(d.annual_value * stage_weights.get(d.stage, 0.0) for d in self.deals)

    def health(self) -> PipelineHealth:
        if not self.deals:
            return PipelineHealth.DECLINING
        avg_age_days = sum(
            (datetime.now() - d.start_date).days for d in self.deals if d.start_date
        ) / max(len(self.deals), 1)
        win_rate = sum(
            1 for d in self.deals
            if d.stage in (DealStage.POST_CLOSE, DealStage.MAINTENANCE, DealStage.EXPANSION)
        ) / max(len(self.deals), 1)
        if win_rate > 0.3 and avg_age_days < 90:
            return PipelineHealth.HEALTHY
        if win_rate < 0.1 and avg_age_days > 150:
            return PipelineHealth.DECLINING
        if avg_age_days > 120:
            return PipelineHealth.STAGNANT
        return PipelineHealth.AT_RISK


@dataclass
class MarketOpportunity:
    opportunity_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    segment: MarketSegment = MarketSegment.ENTERPRISE
    tam: float = 0.0
    sam: float = 0.0
    som: float = 0.0
    growth_rate: float = 0.0
    competition_intensity: float = 0.5
    entry_barriers: list[str] = field(default_factory=list)
    success_probability: float = 0.5
    estimated_cac: float = 0.0
    estimated_ltv: float = 0.0
    time_to_revenue_months: int = 6

    def ltv_cac_ratio(self) -> float:
        if self.estimated_cac == 0:
            return 0.0
        return self.estimated_ltv / self.estimated_cac

    def market_attractiveness_score(self) -> float:
        growth_score = min(self.growth_rate / 0.3, 1.0) * 0.25
        competition_score = (1 - self.competition_intensity) * 0.20
        barrier_score = (1 - min(len(self.entry_barriers) / 5, 1.0)) * 0.15
        ltv_cac = min(self.ltv_cac_ratio() / 3, 1.0) * 0.25
        prob_score = self.success_probability * 0.15
        return round(growth_score + competition_score + barrier_score + ltv_cac + prob_score, 3)


@dataclass
class RevenueForecast:
    model_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    monthly_revenue: list[float] = field(default_factory=list)
    assumptions: dict[str, Any] = field(default_factory=dict)
    discount_rate: float = 0.10
    projection_months: int = 36

    def npv(self) -> float:
        total = 0.0
        for i, rev in enumerate(self.monthly_revenue):
            total += rev / ((1 + self.discount_rate) ** (i / 12))
        return round(total, 2)

    def irr(self) -> float:
        if not self.monthly_revenue:
            return 0.0
        low, high = -0.5, 5.0
        for _ in range(200):
            mid = (low + high) / 2
            f = sum(r / ((1 + mid) ** (i / 12)) for i, r in enumerate(self.monthly_revenue))
            if f > 0:
                low = mid
            else:
                high = mid
        return round(mid, 4)

    def payback_months(self, initial_investment: float) -> Optional[int]:
        cumulative = 0.0
        for i, rev in enumerate(self.monthly_revenue):
            cumulative += rev
            if cumulative >= initial_investment:
                return i + 1
        return None


@dataclass
class CompetitorProfile:
    name: str = ""
    positioning: CompetitorPositioning = CompetitorPositioning.CHALLENGER
    market_share: float = 0.0
    pricing: dict[str, float] = field(default_factory=dict)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    recent_moves: list[str] = field(default_factory=list)
    threat_score: float = 0.5

    def competitive_threat(self) -> str:
        if self.threat_score >= 0.8:
            return "CRITICAL"
        if self.threat_score >= 0.6:
            return "HIGH"
        if self.threat_score >= 0.3:
            return "MODERATE"
        return "LOW"


@dataclass
class ValueProposition:
    prop_type: ValuePropositionType = ValuePropositionType.INNOVATION
    headline: str = ""
    customer_jobs: list[str] = field(default_factory=list)
    pains: list[str] = field(default_factory=list)
    gains: list[str] = field(default_factory=list)
    pain_relievers: list[str] = field(default_factory=list)
    gain_creators: list[str] = field(default_factory=list)
    score: float = 0.0

    def fit_score(self) -> float:
        jobs = max(len(self.customer_jobs), 1)
        pain_coverage = len(self.pain_relievers) / max(len(self.pains), 1)
        gain_coverage = len(self.gain_creators) / max(len(self.gains), 1)
        return round((pain_coverage + gain_coverage) / 2, 3)


@dataclass
class SalesForecast:
    product_line: str = ""
    period_months: int = 12
    scenarios: dict[str, list[float]] = field(default_factory=dict)
    baseline_growth_rate: float = 0.05
    seasonal_factors: list[float] = field(default_factory=list)

    def generate_scenario(
        self, name: str, growth_multiplier: float = 1.0
    ) -> list[float]:
        base = 10_000.0
        result = []
        for m in range(self.period_months):
            seasonal = (
                self.seasonal_factors[m % len(self.seasonal_factors)]
                if self.seasonal_factors
                else 1.0
            )
            base *= 1 + self.baseline_growth_rate * growth_multiplier
            result.append(round(base * seasonal, 2))
        self.scenarios[name] = result
        return result

    def expected_value(self) -> float:
        if not self.scenarios:
            self.generate_scenario("base")
        weights = {"pessimistic": 0.25, "base": 0.50, "optimistic": 0.25}
        total = 0.0
        for name, values in self.scenarios.items():
            w = weights.get(name, 1.0 / max(len(self.scenarios), 1))
            total += sum(values) * w
        return round(total, 2)


@dataclass
class PartnerScorecard:
    partner: Optional[Partnership] = None
    financial_stability: float = 0.0
    market_reach: float = 0.0
    technical_capability: float = 0.0
    cultural_alignment: float = 0.0
    innovation_potential: float = 0.0
    risk_level: float = 0.0
    overall_score: float = 0.0

    def compute_overall(self) -> float:
        weights = [0.20, 0.18, 0.22, 0.15, 0.15, 0.10]
        scores = [
            self.financial_stability,
            self.market_reach,
            self.technical_capability,
            self.cultural_alignment,
            self.innovation_potential,
            1 - self.risk_level,
        ]
        self.overall_score = round(sum(w * s for w, s in zip(weights, scores)), 3)
        return self.overall_score

    def recommendation(self) -> str:
        s = self.overall_score
        if s >= 0.8:
            return "PURSUE AGGRESSIVELY"
        if s >= 0.6:
            return "PURSUE WITH MODERATE INVESTMENT"
        if s >= 0.4:
            return "CONDITIONAL PURSUIT - ADDRESS GAPS"
        return "DO NOT PURSUE"


@dataclass
class MarketAnalysis:
    industry: str = ""
    market_size: float = 0.0
    cagr: float = 0.0
    key_trends: list[str] = field(default_factory=list)
    swot: dict[str, list[str]] = field(default_factory=dict)
    porter_forces: dict[str, float] = field(default_factory=dict)
    regulatory_factors: list[str] = field(default_factory=list)

    def industry_attractiveness(self) -> float:
        forces_avg = sum(self.porter_forces.values()) / max(
            len(self.porter_forces), 1
        )
        trend_score = min(len(self.key_trends) / 5, 1.0) * 0.3
        cagr_score = min(self.cagr / 0.2, 1.0) * 0.35
        force_score = (1 - forces_avg) * 0.25
        reg_penalty = min(len(self.regulatory_factors) * 0.05, 0.20)
        return round(trend_score + cagr_score + force_score - reg_penalty, 3)


@dataclass
class GrowthPlan:
    company_name: str = ""
    strategy: GrowthStrategy = GrowthStrategy.MARKET_PENETRATION
    objectives: list[str] = field(default_factory=list)
    initiatives: list[str] = field(default_factory=list)
    timeline_months: int = 12
    budget: float = 0.0
    kpis: dict[str, str] = field(default_factory=dict)
    risks: list[str] = field(default_factory=list)
    milestones: dict[str, str] = field(default_factory=dict)

    def progress_score(self) -> float:
        if not self.milestones:
            return 0.0
        total_months = self.timeline_months
        now_months = min(total_months, 6)
        achieved = sum(
            1 for m in self.milestones.values() if m.lower() in ("done", "complete")
        )
        return round(achieved / max(len(self.milestones), 1), 3)


@dataclass
class NegotiationStrategy:
    style: NegotiationStyle = NegotiationStyle.COLLABORATIVE
    walk_away_point: float = 0.0
    target_point: float = 0.0
    anchor_point: float = 0.0
    concessions: list[str] = field(default_factory=list)
    leverage_points: list[str] = field(default_factory=list)
    zone_of_possible_agreement: tuple[float, float] = (0.0, 0.0)

    def zopa_width(self) -> float:
        return max(self.zone_of_possible_agreement[1] - self.zone_of_possible_agreement[0], 0)

    def probability_of_acceptance(self, offer: float) -> float:
        low, high = self.zone_of_possible_agreement
        if low <= offer <= high:
            mid = (low + high) / 2
            dist = abs(offer - mid) / max((high - low) / 2, 0.01)
            return round(1 - dist * 0.3, 3)
        return 0.05


@dataclass
class LeadQualification:
    lead_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    company_name: str = ""
    contact: str = ""
    budget_score: float = 0.0
    authority_score: float = 0.0
    need_score: float = 0.0
    timeline_score: float = 0.0
    fit_score: float = 0.0

    def bant_score(self) -> float:
        return round(
            (self.budget_score + self.authority_score + self.need_score + self.timeline_score) / 4,
            3,
        )

    def qualification_status(self) -> str:
        bant = self.bant_score()
        if bant >= 0.75 and self.fit_score >= 0.7:
            return "HOT_LEAD"
        if bant >= 0.5:
            return "WARM_LEAD"
        return "COLD_LEAD"


@dataclass
class ChannelStrategy:
    product: str = ""
    market: MarketSegment = MarketSegment.ENTERPRISE
    channels: list[str] = field(default_factory=list)
    partner_types: list[PartnershipType] = field(default_factory=list)
    investment: float = 0.0
    expected_reach: int = 0
    conversion_rate: float = 0.02

    def estimated_deals(self) -> int:
        return int(self.expected_reach * self.conversion_rate)

    def cost_per_acquisition(self) -> float:
        deals = self.estimated_deals()
        if deals == 0:
            return float("inf")
        return round(self.investment / deals, 2)


@dataclass
class PricingModel:
    base_price: float = 0.0
    tier_multipliers: dict[str, float] = field(default_factory=dict)
    discount_tiers: dict[str, float] = field(default_factory=dict)
    volume_breaks: dict[int, float] = field(default_factory=dict)

    def price_for_tier(self, tier: str, volume: int = 1) -> float:
        mult = self.tier_multipliers.get(tier, 1.0)
        vol_discount = 1.0
        for break_qty, disc in sorted(self.volume_breaks.items()):
            if volume >= break_qty:
                vol_discount = disc
        return round(self.base_price * mult * vol_discount * volume, 2)

    def competitive_price(self, competitor_price: float, undercut_pct: float = 0.10) -> float:
        return round(competitor_price * (1 - undercut_pct), 2)


@dataclass
class ExpansionRoadmap:
    current_markets: list[str] = field(default_factory=list)
    target_markets: list[str] = field(default_factory=list)
    phases: list[dict[str, Any]] = field(default_factory=list)
    total_budget: float = 0.0
    timeline_months: int = 18

    def phase_count(self) -> int:
        return len(self.phases)

    def budget_per_phase(self) -> float:
        phases = max(len(self.phases), 1)
        return round(self.total_budget / phases, 2)


@dataclass
class PartnershipAgreement:
    agreement_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    partnership: Optional[Partnership] = None
    terms: dict[str, Any] = field(default_factory=dict)
    revenue_share: float = 0.0
    exclusivity: bool = False
    termination_clause: str = ""
    renewal_terms: str = ""
    compliance_requirements: list[str] = field(default_factory=list)

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.agreement_id,
            "revenue_share": f"{self.revenue_share:.1%}",
            "exclusivity": self.exclusivity,
            "term": self.terms.get("duration", "unspecified"),
            "compliance_items": len(self.compliance_requirements),
        }


@dataclass
class BusinessMetric:
    name: str = ""
    value: float = 0.0
    target: float = 0.0
    unit: str = ""
    trend: str = "stable"

    def attainment(self) -> float:
        if self.target == 0:
            return 0.0
        return round(self.value / self.target, 3)

    def status(self) -> str:
        att = self.attainment()
        if att >= 1.0:
            return "EXCEEDED"
        if att >= 0.9:
            return "ON_TRACK"
        if att >= 0.7:
            return "AT_RISK"
        return "BEHIND"


@dataclass
class OutreachCampaign:
    campaign_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    channel: str = "email"
    total_sent: int = 0
    responses: int = 0
    meetings: int = 0
    deals_generated: int = 0
    spend: float = 0.0

    def response_rate(self) -> float:
        return round(self.responses / max(self.total_sent, 1), 4)

    def meeting_rate(self) -> float:
        return round(self.meetings / max(self.responses, 1), 4)

    def deal_rate(self) -> float:
        return round(self.deals_generated / max(self.total_sent, 1), 4)

    def cost_per_meeting(self) -> float:
        return round(self.spend / max(self.meetings, 1), 2)


@dataclass
class ConversionFunnel:
    stage_names: list[str] = field(default_factory=list)
    stage_counts: list[int] = field(default_factory=list)

    def conversion_rates(self) -> list[float]:
        rates = []
        for i in range(1, len(self.stage_counts)):
            prev = self.stage_counts[i - 1]
            rates.append(round(self.stage_counts[i] / max(prev, 1), 4))
        return rates

    def overall_conversion(self) -> float:
        if len(self.stage_counts) < 2:
            return 0.0
        return round(self.stage_counts[-1] / max(self.stage_counts[0], 1), 4)

    def bottleneck_stage(self) -> str:
        rates = self.conversion_rates()
        if not rates:
            return "N/A"
        min_idx = rates.index(min(rates))
        return self.stage_names[min_idx + 1]


@dataclass
class QuarterlyReview:
    quarter: str = ""
    year: int = 2026
    metrics: list[BusinessMetric] = field(default_factory=list)
    deals_closed: int = 0
    revenue_generated: float = 0.0
    pipeline_value: float = 0.0
    highlights: list[str] = field(default_factory=list)
    challenges: list[str] = field(default_factory=list)
    next_quarter_focus: list[str] = field(default_factory=list)

    def overall_health(self) -> str:
        statuses = [m.status() for m in self.metrics]
        on_track = sum(1 for s in statuses if s in ("EXCEEDED", "ON_TRACK"))
        ratio = on_track / max(len(statuses), 1)
        if ratio >= 0.8:
            return "STRONG"
        if ratio >= 0.5:
            return "MODERATE"
        return "WEAK"

    def summary(self) -> dict[str, Any]:
        return {
            "quarter": f"{self.quarter} {self.year}",
            "health": self.overall_health(),
            "revenue": self.revenue_generated,
            "pipeline": self.pipeline_value,
            "deals": self.deals_closed,
            "metrics_on_track": sum(
                1 for m in self.metrics if m.status() in ("EXCEEDED", "ON_TRACK")
            ),
            "total_metrics": len(self.metrics),
        }


# ---------------------------------------------------------------------------
# BusinessDevelopmentAgent
# ---------------------------------------------------------------------------

class BusinessDevelopmentAgent:
    """Core business development agent with partner discovery, deal pipeline
    management, revenue modeling, market intelligence, and growth strategy."""

    def __init__(self, company_name: str = "Acme Corp", industry: str = "SaaS"):
        self.company_name = company_name
        self.industry = industry
        self.partnerships: dict[str, Partnership] = {}
        self.pipeline = DealPipeline(name=f"{company_name} BD Pipeline")
        self.competitors: list[CompetitorProfile] = []
        self.market_analyses: dict[str, MarketAnalysis] = {}
        self.growth_plans: list[GrowthPlan] = []
        self.outreach_campaigns: list[OutreachCampaign] = []
        self._event_log: list[dict[str, Any]] = []
        logger.info("BusinessDevelopmentAgent initialized for %s (%s)", company_name, industry)

    # ---- internal helpers ----

    def _log_event(self, event_type: str, detail: str) -> None:
        self._event_log.append(
            {"time": datetime.now().isoformat(), "type": event_type, "detail": detail}
        )

    def _generate_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def _score_weighted(self, scores: dict[str, float], weights: dict[str, float]) -> float:
        return round(sum(scores[k] * weights.get(k, 0) for k in scores), 3)

    # ---- Partner Discovery ----

    def find_partners(
        self, criteria: dict[str, Any], market: MarketSegment = MarketSegment.ENTERPRISE
    ) -> list[dict[str, Any]]:
        """Discover and score potential partners matching criteria.

        Args:
            criteria: Dict with keys like 'industry', 'min_revenue',
                      'geography', 'capabilities', 'synergy_focus'.
            market: Target market segment filter.

        Returns:
            Ranked list of partner candidates with scores.
        """
        logger.info("Finding partners: criteria=%s market=%s", criteria, market.value)
        candidates: list[dict[str, Any]] = []
        target_industry = criteria.get("industry", self.industry)
        min_revenue = criteria.get("min_revenue", 0)
        capabilities = criteria.get("capabilities", [])
        synergy_focus = criteria.get("synergy_focus", "revenue")

        import random
        random.seed(hash(str(criteria)))
        for i in range(criteria.get("max_results", 10)):
            revenue_sim = random.uniform(50_000, 5_000_000)
            if revenue_sim < min_revenue:
                continue
            synergy = random.uniform(0.3, 0.95)
            strategic = random.uniform(0.4, 0.95)
            cultural = random.uniform(0.3, 0.9)
            reach = random.uniform(0.2, 0.95)
            capability_match = random.uniform(0.4, 0.95)

            composite = (
                synergy * 0.30
                + strategic * 0.25
                + cultural * 0.15
                + reach * 0.15
                + capability_match * 0.15
            )
            candidates.append(
                {
                    "candidate_id": self._generate_id(),
                    "name": f"{target_industry}-Partner-{i+1}",
                    "industry": target_industry,
                    "estimated_revenue": round(revenue_sim, 2),
                    "market_segment": market.value,
                    "scores": {
                        "synergy": round(synergy, 3),
                        "strategic_alignment": round(strategic, 3),
                        "cultural_fit": round(cultural, 3),
                        "market_reach": round(reach, 3),
                        "capability_match": round(capability_match, 3),
                    },
                    "composite_score": round(composite, 3),
                    "recommendation": (
                        "PURSUE" if composite >= 0.7
                        else "EVALUATE" if composite >= 0.5
                        else "MONITOR"
                    ),
                    "capability_coverage": round(
                        capability_match * len(capabilities) / max(len(capabilities), 1), 2
                    ),
                }
            )

        candidates.sort(key=lambda c: c["composite_score"], reverse=True)
        self._log_event(
            "partner_discovery",
            f"Found {len(candidates)} candidates for {target_industry} in {market.value}",
        )
        logger.info("Found %d partner candidates", len(candidates))
        return candidates

    def evaluate_partner(self, partner_data: dict[str, Any]) -> PartnerScorecard:
        """Multi-dimensional partner evaluation producing a scorecard.

        Args:
            partner_data: Dict containing partner details — financials,
                          market position, tech stack, culture info.

        Returns:
            PartnerScorecard with recommendation.
        """
        logger.info("Evaluating partner: %s", partner_data.get("name", "unknown"))
        scorecard = PartnerScorecard()
        scorecard.financial_stability = partner_data.get("financial_health", 0.5)
        scorecard.market_reach = partner_data.get("market_reach", 0.5)
        scorecard.technical_capability = partner_data.get("tech_capability", 0.5)
        scorecard.cultural_alignment = partner_data.get("cultural_fit", 0.5)
        scorecard.innovation_potential = partner_data.get("innovation", 0.5)
        scorecard.risk_level = partner_data.get("risk", 0.3)
        scorecard.compute_overall()
        self._log_event(
            "partner_evaluation",
            f"Scored {partner_data.get('name', 'unknown')}: {scorecard.overall_score}",
        )
        logger.info(
            "Partner %s -> %.3f (%s)",
            partner_data.get("name"),
            scorecard.overall_score,
            scorecard.recommendation(),
        )
        return scorecard

    # ---- Deal Pipeline ----

    def structure_deal(
        self,
        partner_name: str,
        partnership_type: PartnershipType,
        deal_value: float,
        **kwargs: Any,
    ) -> Partnership:
        """Structure a new deal and add it to the pipeline.

        Args:
            partner_name: Name of the partner organization.
            partnership_type: Type of partnership being structured.
            deal_value: Estimated annual deal value.
            **kwargs: Additional partnership fields.

        Returns:
            The created Partnership object.
        """
        deal = Partnership(
            name=partner_name,
            partnership_type=partnership_type,
            stage=DealStage.IDENTIFICATION,
            annual_value=deal_value,
            start_date=datetime.now(),
            end_date=kwargs.get("end_date", datetime.now() + timedelta(days=365)),
            **{k: v for k, v in kwargs.items() if k != "end_date"},
        )
        self.partnerships[deal.partner_id] = deal
        self.pipeline.deals.append(deal)
        self._log_event("deal_structured", f"Deal {deal.partner_id} with {partner_name}")
        logger.info(
            "Structured deal %s: %s (%s) value=$%.0f",
            deal.partner_id, partner_name, partnership_type.value, deal_value,
        )
        return deal

    def manage_pipeline(
        self, stage_filter: Optional[DealStage] = None
    ) -> dict[str, Any]:
        """Analyze and manage the deal pipeline.

        Args:
            stage_filter: Optional filter to show only a specific stage.

        Returns:
            Pipeline analysis with stage breakdown, weighted forecast, health.
        """
        deals_by_stage = self.pipeline.deals_by_stage()
        if stage_filter:
            deals_by_stage = {stage_filter: deals_by_stage.get(stage_filter, [])}

        analysis: dict[str, Any] = {
            "pipeline_id": self.pipeline.pipeline_id,
            "total_deals": len(self.pipeline.deals),
            "weighted_value": round(self.pipeline.weighted_value(), 2),
            "health": self.pipeline.health().value,
            "stages": {},
        }
        for stage, deals in deals_by_stage.items():
            analysis["stages"][stage.value] = {
                "count": len(deals),
                "total_value": round(sum(d.annual_value for d in deals), 2),
                "weighted_value": round(
                    sum(
                        d.annual_value
                        * {
                            DealStage.IDENTIFICATION: 0.05,
                            DealStage.QUALIFICATION: 0.15,
                            DealStage.PROPOSAL: 0.35,
                            DealStage.NEGOTIATION: 0.60,
                            DealStage.CLOSING: 0.85,
                            DealStage.POST_CLOSE: 1.0,
                            DealStage.MAINTENANCE: 1.0,
                            DealStage.EXPANSION: 1.0,
                        }.get(d.stage, 0)
                        for d in deals
                    ),
                    2,
                ),
                "avg_score": round(
                    sum(d.composite_score() for d in deals) / max(len(deals), 1), 3
                ),
            }
        analysis["target_coverage"] = (
            round(analysis["weighted_value"] / max(self.pipeline.target_revenue, 1), 3)
        )
        self._log_event("pipeline_analysis", f"Deals: {analysis['total_deals']}")
        return analysis

    # ---- Revenue Modeling ----

    def model_revenue(
        self,
        scenario: str = "base",
        timeline_months: int = 36,
        initial_mrr: float = 50_000,
        assumptions: Optional[dict[str, Any]] = None,
    ) -> RevenueForecast:
        """Build a revenue model with NPV and IRR.

        Args:
            scenario: Scenario name (base, aggressive, conservative).
            timeline_months: Projection horizon.
            initial_mrr: Starting monthly recurring revenue.
            assumptions: Growth rate, churn, expansion overrides.

        Returns:
            RevenueForecast with monthly projections, NPV, IRR.
        """
        assumptions = assumptions or {}
        growth_rates = {"conservative": 0.03, "base": 0.06, "aggressive": 0.10}
        churn_rates = {"conservative": 0.03, "base": 0.02, "aggressive": 0.015}
        growth = assumptions.get("growth_rate", growth_rates.get(scenario, 0.06))
        churn = assumptions.get("churn_rate", churn_rates.get(scenario, 0.02))
        expansion = assumptions.get("expansion_rate", 0.01)
        discount = assumptions.get("discount_rate", 0.10)

        monthly_rev: list[float] = []
        mrr = initial_mrr
        for m in range(timeline_months):
            seasonal = 1.0 + 0.05 * math.sin(2 * math.pi * m / 12)
            mrr = mrr * (1 + growth - churn + expansion) * seasonal
            monthly_rev.append(round(mrr, 2))

        forecast = RevenueForecast(
            name=f"{scenario}_scenario",
            monthly_revenue=monthly_rev,
            assumptions={
                "growth_rate": growth,
                "churn_rate": churn,
                "expansion_rate": expansion,
                "discount_rate": discount,
                "initial_mrr": initial_mrr,
            },
            discount_rate=discount,
            projection_months=timeline_months,
        )
        self._log_event(
            "revenue_model",
            f"Scenario={scenario} months={timeline_months} NPV={forecast.npv():.0f}",
        )
        logger.info(
            "Revenue model (%s): NPV=$%.0f, IRR=%.2f%%",
            scenario, forecast.npv(), forecast.irr() * 100,
        )
        return forecast

    # ---- Market Analysis ----

    def analyze_market(self, opportunity: dict[str, Any]) -> MarketAnalysis:
        """Deep market analysis with TAM/SAM/SOM sizing.

        Args:
            opportunity: Dict with industry, market_size, growth_rate,
                         trends, competition info.

        Returns:
            MarketAnalysis with SWOT, Porter's forces, attractiveness.
        """
        industry = opportunity.get("industry", self.industry)
        market_size = opportunity.get("market_size", 1_000_000_000)
        cagr = opportunity.get("cagr", 0.12)
        trends = opportunity.get("trends", [
            "Cloud migration accelerating",
            "AI/ML integration becoming standard",
            "Remote-first workflows permanent",
        ])

        analysis = MarketAnalysis(
            industry=industry,
            market_size=market_size,
            cagr=cagr,
            key_trends=trends,
            swot={
                "strengths": opportunity.get("strengths", ["Strong brand", "Technical moat"]),
                "weaknesses": opportunity.get("weaknesses", ["Limited geographic reach"]),
                "opportunities": opportunity.get(
                    "opportunities", ["Underserved SMB segment", "API platform play"]
                ),
                "threats": opportunity.get(
                    "threats", ["Big tech entry", "Regulation tightening"]
                ),
            },
            porter_forces={
                "supplier_power": opportunity.get("supplier_power", 0.3),
                "buyer_power": opportunity.get("buyer_power", 0.6),
                "competitive_rivalry": opportunity.get("rivalry", 0.7),
                "threat_of_substitutes": opportunity.get("substitutes", 0.4),
                "threat_of_new_entrants": opportunity.get("new_entrants", 0.5),
            },
            regulatory_factors=opportunity.get("regulations", [
                "GDPR compliance required",
                "SOC 2 Type II expected",
            ]),
        )
        self.market_analyses[industry] = analysis
        self._log_event(
            "market_analysis",
            f"{industry}: size=${market_size:,.0f}, CAGR={cagr:.1%}, "
            f"attractiveness={analysis.industry_attractiveness():.3f}",
        )
        logger.info(
            "Market analysis (%s): $%.1fB TAM, CAGR %.1f%%, attractiveness %.3f",
            industry, market_size / 1e9, cagr * 100,
            analysis.industry_attractiveness(),
        )
        return analysis

    # ---- Growth Strategy ----

    def develop_growth_strategy(
        self,
        company_profile: Optional[dict[str, Any]] = None,
    ) -> GrowthPlan:
        """Develop growth strategy based on Ansoff matrix.

        Args:
            company_profile: Dict with current_revenue, products, markets,
                             capabilities, risk_tolerance.

        Returns:
            GrowthPlan with strategy, objectives, initiatives, KPIs.
        """
        profile = company_profile or {}
        revenue = profile.get("current_revenue", 1_000_000)
        risk_tolerance = profile.get("risk_tolerance", "moderate")
        products = profile.get("products", 1)
        markets = profile.get("markets", 1)

        if products <= 1 and markets <= 1:
            strategy = GrowthStrategy.MARKET_PENETRATION
        elif products <= 1 and markets > 1:
            strategy = GrowthStrategy.MARKET_DEVELOPMENT
        elif products > 1 and markets <= 1:
            strategy = GrowthStrategy.PRODUCT_DEVELOPMENT
        else:
            strategy = GrowthStrategy.DIVERSIFICATION

        strategy_details = {
            GrowthStrategy.MARKET_PENETRATION: {
                "objectives": [
                    "Increase market share by 15% in current segments",
                    "Reduce customer acquisition cost by 20%",
                    "Improve net retention rate to 120%",
                ],
                "initiatives": [
                    "Launch referral program with incentive structure",
                    "Implement Account-Based Marketing for top 100 prospects",
                    "Optimize pricing tiers based on usage data",
                    "Strengthen customer success team for upsell motions",
                ],
                "kpis": {"market_share": "15%", "cac_reduction": "20%", "nrr": "120%"},
            },
            GrowthStrategy.MARKET_DEVELOPMENT: {
                "objectives": [
                    "Enter 2 new geographic markets within 12 months",
                    "Establish 5 channel partnerships in target regions",
                    "Achieve $500K ARR from new markets",
                ],
                "initiatives": [
                    "Hire regional sales leads for EMEA and APAC",
                    "Localize product for top 3 international markets",
                    "Partner with local system integrators",
                    "Attend 4 international industry conferences",
                ],
                "kpis": {"new_markets": "2", "partnerships": "5", "new_arr": "$500K"},
            },
            GrowthStrategy.PRODUCT_DEVELOPMENT: {
                "objectives": [
                    "Launch 2 new product lines in adjacent categories",
                    "Achieve 30% cross-sell rate among existing customers",
                    "Generate $750K from new products",
                ],
                "initiatives": [
                    "Conduct customer research for adjacent pain points",
                    "Build API platform for developer ecosystem",
                    "Acquire or build analytics module",
                    "Create integration marketplace",
                ],
                "kpis": {"new_products": "2", "cross_sell": "30%", "new_product_arr": "$750K"},
            },
            GrowthStrategy.DIVERSIFICATION: {
                "objectives": [
                    "Diversify revenue streams across 3+ product lines",
                    "Enter government segment with FedRAMP offering",
                    "Build strategic ecosystem of 10+ integration partners",
                ],
                "initiatives": [
                    "Establish government sales division",
                    "Build platform-as-a-service layer",
                    "Create partner certification program",
                    "Explore vertical-specific solutions",
                ],
                "kpis": {
                    "product_lines": "3",
                    "gov_segment": "launched",
                    "certified_partners": "10",
                },
            },
        }
        details = strategy_details[strategy]
        budget = revenue * (0.15 if risk_tolerance == "aggressive" else 0.10)
        plan = GrowthPlan(
            company_name=self.company_name,
            strategy=strategy,
            objectives=details["objectives"],
            initiatives=details["initiatives"],
            timeline_months=profile.get("timeline_months", 12),
            budget=round(budget, 2),
            kpis=details["kpis"],
            risks=[
                "Market timing risk",
                "Execution capability constraints",
                "Competitive response",
                "Resource allocation pressure",
            ],
            milestones={
                "Q1": "in_progress",
                "Q2": "planned",
                "Q3": "planned",
                "Q4": "planned",
            },
        )
        self.growth_plans.append(plan)
        self._log_event(
            "growth_strategy",
            f"Strategy: {strategy.value}, budget: ${budget:,.0f}",
        )
        logger.info("Growth strategy: %s (budget $%.0fK)", strategy.value, budget / 1000)
        return plan

    # ---- Negotiation ----

    def negotiate_deal(
        self,
        deal_value: float,
        style: NegotiationStyle = NegotiationStyle.COLLABORATIVE,
        walk_away: Optional[float] = None,
        target: Optional[float] = None,
    ) -> NegotiationStrategy:
        """Develop an optimized negotiation strategy.

        Args:
            deal_value: Expected deal value.
            style: Preferred negotiation style.
            walk_away: Walk-away point (default: 60% of deal_value).
            target: Target point (default: 90% of deal_value).

        Returns:
            NegotiationStrategy with ZOPA, anchor, concessions, leverage.
        """
        walk_away = walk_away or deal_value * 0.60
        target = target or deal_value * 0.90
        anchor = deal_value * 1.15

        strategy_map = {
            NegotiationStyle.COMPETITIVE: {
                "concessions": [
                    "Limited volume discount (max 5%)",
                    "Standard SLA only",
                    "Net-30 payment terms",
                ],
                "leverage": [
                    "Market-leading position",
                    "Proprietary technology",
                    "Strong brand reputation",
                ],
            },
            NegotiationStyle.COLLABORATIVE: {
                "concessions": [
                    "Flexible pricing tiers",
                    "Custom SLA options",
                    "Co-marketing investment",
                    "Extended payment terms (Net-45)",
                ],
                "leverage": [
                    "Mutual customer base overlap",
                    "Technology integration synergy",
                    "Shared market expansion opportunity",
                ],
            },
            NegotiationStyle.COMPROMISE: {
                "concessions": [
                    "Balanced pricing (mid-range)",
                    "Shared go-to-market costs",
                    "Joint customer success ownership",
                ],
                "leverage": [
                    "Market need for integrated solution",
                    "Competitive pressure on both sides",
                ],
            },
        }
        config = strategy_map.get(style, strategy_map[NegotiationStyle.COLLABORATIVE])
        zopa_low = walk_away
        zopa_high = deal_value * 1.05
        strategy = NegotiationStrategy(
            style=style,
            walk_away_point=walk_away,
            target_point=target,
            anchor_point=anchor,
            concessions=config["concessions"],
            leverage_points=config["leverage"],
            zone_of_possible_agreement=(zopa_low, zopa_high),
        )
        self._log_event(
            "negotiation_strategy",
            f"Style={style.value} ZOPA=[${zopa_low:,.0f}-${zopa_high:,.0f}]",
        )
        logger.info(
            "Negotiation strategy: %s, ZOPA [$%.0f-$%.0f], anchor $%.0f",
            style.value, zopa_low, zopa_high, anchor,
        )
        return strategy

    # ---- Value Proposition ----

    def create_value_proposition(
        self,
        target_market: MarketSegment = MarketSegment.ENTERPRISE,
        product_name: str = "Platform",
    ) -> ValueProposition:
        """Build a value proposition canvas for the target market.

        Args:
            target_market: Target segment.
            product_name: Product or platform name.

        Returns:
            ValueProposition with jobs, pains, gains, and fit score.
        """
        segment_profiles = {
            MarketSegment.ENTERPRISE: {
                "jobs": [
                    "Reduce total cost of ownership",
                    "Improve operational efficiency at scale",
                    "Ensure compliance and security",
                    "Integrate with existing enterprise stack",
                    "Demonstrate ROI to board",
                ],
                "pains": [
                    "Complex procurement processes",
                    "Integration with legacy systems",
                    "Vendor lock-in risk",
                    "Long implementation timelines",
                    "Change management resistance",
                ],
                "gains": [
                    "Unified analytics dashboard",
                    "99.99% uptime SLA",
                    "SOC 2 and ISO 27001 compliance",
                    "Dedicated success manager",
                    "Custom integrations",
                ],
                "pain_relievers": [
                    "Pre-built connectors for top 20 enterprise tools",
                    "90-day implementation guarantee",
                    "Flexible contract terms",
                    "White-glove onboarding",
                ],
                "gain_creators": [
                    "Real-time ROI calculator",
                    "Executive business reviews",
                    "Industry benchmarking data",
                    "Dedicated API engineering support",
                ],
            },
            MarketSegment.SMB: {
                "jobs": [
                    "Grow revenue without adding headcount",
                    "Compete with larger competitors",
                    "Simplify day-to-day operations",
                ],
                "pains": [
                    "Limited budget",
                    "No dedicated IT staff",
                    "Time-poor decision making",
                ],
                "gains": [
                    "Self-serve onboarding",
                    "Transparent pricing",
                    "Quick time-to-value",
                ],
                "pain_relievers": [
                    "No-code setup wizard",
                    "Free tier for getting started",
                    "In-app chat support",
                ],
                "gain_creators": [
                    "Growth playbooks",
                    "Community forum",
                    "Template library",
                ],
            },
        }
        profile = segment_profiles.get(target_market, segment_profiles[MarketSegment.ENTERPRISE])
        vp = ValueProposition(
            prop_type=ValuePropositionType.INNOVATION,
            headline=f"{product_name}: Unleash growth through intelligent automation",
            customer_jobs=profile["jobs"],
            pains=profile["pains"],
            gains=profile["gains"],
            pain_relievers=profile["pain_relievers"],
            gain_creators=profile["gain_creators"],
        )
        vp.score = vp.fit_score()
        self._log_event(
            "value_proposition",
            f"Created VP for {target_market.value}, fit={vp.score:.3f}",
        )
        logger.info(
            "Value proposition created: fit_score=%.3f (%s)",
            vp.score, target_market.value,
        )
        return vp

    # ---- Sales Forecasting ----

    def forecast_sales(
        self,
        product_line: str = "Core Platform",
        period_months: int = 12,
        base_mrr: float = 100_000,
    ) -> SalesForecast:
        """Generate sales forecast with multiple scenarios.

        Args:
            product_line: Product or service line.
            period_months: Forecast horizon.
            base_mrr: Starting MRR for the product line.

        Returns:
            SalesForecast with pessimistic/base/optimistic scenarios.
        """
        forecast = SalesForecast(
            product_line=product_line,
            period_months=period_months,
            baseline_growth_rate=0.05,
            seasonal_factors=[0.85, 0.90, 1.00, 1.05, 1.10, 1.15,
                              1.10, 1.05, 1.00, 0.95, 0.90, 0.85],
        )
        forecast.generate_scenario("pessimistic", growth_multiplier=0.6)
        forecast.generate_scenario("base", growth_multiplier=1.0)
        forecast.generate_scenario("optimistic", growth_multiplier=1.5)
        ev = forecast.expected_value()
        self._log_event(
            "sales_forecast",
            f"{product_line}: expected_value=${ev:,.0f}",
        )
        logger.info(
            "Sales forecast (%s, %dm): expected=$%.0f",
            product_line, period_months, ev,
        )
        return forecast

    # ---- Competitive Analysis ----

    def evaluate_competitive_landscape(
        self, industry: Optional[str] = None
    ) -> dict[str, Any]:
        """Analyze competitive landscape with positioning and threat assessment.

        Args:
            industry: Industry to analyze (defaults to self.industry).

        Returns:
            Competitive analysis with positioning map and recommendations.
        """
        industry = industry or self.industry
        sample_competitors = [
            CompetitorProfile(
                name="Market Leader Inc.",
                positioning=CompetitorPositioning.LEADER,
                market_share=0.35,
                pricing={"enterprise": 500, "smb": 99},
                strengths=["Brand", "Scale", "Ecosystem"],
                weaknesses=["Slow innovation", "Complex pricing"],
                recent_moves=["Acquired AI startup", "Launched marketplace"],
                threat_score=0.85,
            ),
            CompetitorProfile(
                name="FastGrow Tech",
                positioning=CompetitorPositioning.CHALLENGER,
                market_share=0.15,
                pricing={"enterprise": 400, "smb": 79},
                strengths=["Speed", "UX", "Pricing"],
                weaknesses=["Limited enterprise features", "Small team"],
                recent_moves=["Series C funding", "Opened London office"],
                threat_score=0.70,
            ),
            CompetitorProfile(
                name="Niche Solutions Co.",
                positioning=CompetitorPositioning.NICHE,
                market_share=0.05,
                pricing={"enterprise": 300, "smb": 49},
                strengths=["Domain expertise", "Customer loyalty"],
                weaknesses=["Narrow feature set", "No API"],
                recent_moves=["Launched vertical solution"],
                threat_score=0.35,
            ),
            CompetitorProfile(
                name="AI-First Startup",
                positioning=CompetitorPositioning.EMERGING,
                market_share=0.02,
                pricing={"enterprise": 200, "smb": 0},
                strengths=["AI-native", "Developer experience"],
                weaknesses=["No enterprise sales", "Unproven at scale"],
                recent_moves=["Open-sourced core engine", "Hired VP Sales"],
                threat_score=0.55,
            ),
        ]
        self.competitors = sample_competitors
        analysis = {
            "industry": industry,
            "competitor_count": len(sample_competitors),
            "market_concentration": round(
                sum(c.market_share for c in sample_competitors), 3
            ),
            "positioning_map": [
                {
                    "name": c.name,
                    "positioning": c.positioning.value,
                    "market_share": c.market_share,
                    "threat": c.competitive_threat(),
                    "threat_score": c.threat_score,
                }
                for c in sample_competitors
            ],
            "strategic_implications": [
                "Differentiate on AI capabilities vs. incumbent's legacy approach",
                "Target mid-market gap between enterprise leader and SMB niche player",
                "Accelerate go-to-market before AI-First Startup achieves scale",
                "Build integration ecosystem to counter Niche's domain lock-in",
            ],
            "competitive_moat_assessment": {
                "our_strengths": [
                    "AI-native architecture",
                    "Flexible pricing model",
                    "Developer-first approach",
                ],
                "vulnerabilities": [
                    "Brand awareness gap vs. market leader",
                    "Enterprise sales team still scaling",
                ],
            },
        }
        self._log_event(
            "competitive_analysis",
            f"Analyzed {len(sample_competitors)} competitors in {industry}",
        )
        logger.info("Competitive analysis: %d competitors mapped", len(sample_competitors))
        return analysis

    # ---- Market Entry ----

    def plan_market_entry(
        self,
        target_market: dict[str, Any],
    ) -> dict[str, Any]:
        """Plan market entry strategy for a new market.

        Args:
            target_market: Dict with name, segment, size, competitors,
                           regulations, timeline.

        Returns:
            Market entry plan with phases, budget, risk mitigation.
        """
        market_name = target_market.get("name", "New Market")
        segment = target_market.get("segment", "enterprise")
        timeline = target_market.get("timeline_months", 12)
        budget = target_market.get("budget", 500_000)

        plan = {
            "target_market": market_name,
            "segment": segment,
            "entry_mode": target_market.get("entry_mode", "direct"),
            "timeline_months": timeline,
            "total_budget": budget,
            "phases": [
                {
                    "phase": "Research & Validation (Months 1-3)",
                    "budget_allocation": budget * 0.15,
                    "activities": [
                        "Market sizing and customer interviews",
                        "Competitive landscape deep dive",
                        "Regulatory and compliance assessment",
                        "Local partner identification",
                    ],
                    "milestones": ["Market validation report", "Partner shortlist"],
                },
                {
                    "phase": "Foundation (Months 4-6)",
                    "budget_allocation": budget * 0.30,
                    "activities": [
                        "Hire local sales lead and SE",
                        "Localize product (language, compliance)",
                        "Establish legal entity or partnership",
                        "Build initial marketing collateral",
                    ],
                    "milestones": ["Legal setup complete", "Localized product beta"],
                },
                {
                    "phase": "Launch (Months 7-9)",
                    "budget_allocation": budget * 0.35,
                    "activities": [
                        "Execute go-to-market campaign",
                        "Onboard first 10 design partners",
                        "Launch at local industry event",
                        "Begin channel partner recruitment",
                    ],
                    "milestones": ["First 5 paying customers", "Event presence"],
                },
                {
                    "phase": "Scale (Months 10-12)",
                    "budget_allocation": budget * 0.20,
                    "activities": [
                        "Expand sales team based on pipeline",
                        "Optimize conversion funnel",
                        "Build customer reference base",
                        "Plan year-two expansion",
                    ],
                    "milestones": ["$100K ARR run rate", "Reference customers"],
                },
            ],
            "risk_mitigation": [
                "Start with design partners to validate product-market fit",
                "Hire local talent to navigate cultural nuances",
                "Build regulatory compliance into product from day one",
                "Maintain flexibility to pivot based on early learnings",
            ],
            "success_metrics": {
                "year_1_arr": "$100K",
                "customers": "10+",
                "nps": ">40",
                "payback_period": "<18 months",
            },
        }
        self._log_event(
            "market_entry",
            f"Planned entry into {market_name} ({timeline}mo, ${budget:,.0f})",
        )
        logger.info("Market entry plan: %s (%d months, $%.0fK)", market_name, timeline, budget / 1000)
        return plan

    # ---- Channel Strategy ----

    def design_channel_strategy(
        self,
        product: str = "Core Platform",
        target_market: MarketSegment = MarketSegment.ENTERPRISE,
    ) -> ChannelStrategy:
        """Design channel partner strategy.

        Args:
            product: Product to be distributed.
            target_market: Target segment.

        Returns:
            ChannelStrategy with channel mix, partner types, projections.
        """
        channel_configs = {
            MarketSegment.ENTERPRISE: {
                "channels": [
                    "Direct sales team",
                    "Strategic alliance partners",
                    "System integrators",
                    "Industry-specific consultancies",
                ],
                "partner_types": [
                    PartnershipType.STRATEGIC,
                    PartnershipType.TECHNOLOGY,
                    PartnershipType.DISTRIBUTION,
                ],
                "investment": 800_000,
                "expected_reach": 5_000,
                "conversion_rate": 0.04,
            },
            MarketSegment.SMB: {
                "channels": [
                    "Online self-serve",
                    "Reseller network",
                    "Digital marketing",
                    "Product-led growth",
                ],
                "partner_types": [
                    PartnershipType.RESELLER,
                    PartnershipType.AFFILIATE,
                    PartnershipType.MARKETING,
                ],
                "investment": 300_000,
                "expected_reach": 50_000,
                "conversion_rate": 0.02,
            },
        }
        config = channel_configs.get(target_market, channel_configs[MarketSegment.ENTERPRISE])
        strategy = ChannelStrategy(
            product=product,
            market=target_market,
            channels=config["channels"],
            partner_types=config["partner_types"],
            investment=config["investment"],
            expected_reach=config["expected_reach"],
            conversion_rate=config["conversion_rate"],
        )
        self._log_event(
            "channel_strategy",
            f"Designed for {product} ({target_market.value}): "
            f"{strategy.estimated_deals()} deals, CPA=${strategy.cost_per_acquisition():.0f}",
        )
        logger.info(
            "Channel strategy: %s -> %d est. deals, CPA $%.0f",
            target_market.value, strategy.estimated_deals(), strategy.cost_per_acquisition(),
        )
        return strategy

    # ---- Due Diligence ----

    def conduct_due_diligence(
        self, target: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute comprehensive due diligence checklist.

        Args:
            target: Dict with name, type (partner/acquisition/investment),
                    and relevant data.

        Returns:
            Due diligence report with checklist, risk assessment, decision.
        """
        target_name = target.get("name", "Unknown")
        target_type = target.get("type", "partner")
        checklist = {
            "financial_review": {
                "items": [
                    "Audited financial statements (3 years)",
                    "Revenue composition and growth trajectory",
                    "Burn rate and runway analysis",
                    "Outstanding liabilities and debt structure",
                    "Customer concentration risk",
                ],
                "status": "pending",
                "risk_level": target.get("financial_risk", "medium"),
            },
            "legal_review": {
                "items": [
                    "Corporate structure and ownership",
                    "Existing contracts and obligations",
                    "IP ownership and patent portfolio",
                    "Litigation history and pending matters",
                    "Regulatory compliance status",
                ],
                "status": "pending",
                "risk_level": target.get("legal_risk", "medium"),
            },
            "technical_review": {
                "items": [
                    "Technology stack assessment",
                    "Security audit and penetration test results",
                    "Scalability and architecture review",
                    "Technical debt evaluation",
                    "Integration compatibility",
                ],
                "status": "pending",
                "risk_level": target.get("technical_risk", "medium"),
            },
            "market_review": {
                "items": [
                    "Market position and competitive analysis",
                    "Customer satisfaction and NPS data",
                    "Product roadmap alignment",
                    "Go-to-market capability assessment",
                    "Brand reputation analysis",
                ],
                "status": "pending",
                "risk_level": target.get("market_risk", "low"),
            },
            "team_review": {
                "items": [
                    "Key person dependency analysis",
                    "Organizational structure assessment",
                    "Culture and values alignment",
                    "Employee retention and satisfaction",
                    "Leadership capability evaluation",
                ],
                "status": "pending",
                "risk_level": target.get("team_risk", "medium"),
            },
            "operational_review": {
                "items": [
                    "Business continuity plans",
                    "Vendor and supplier dependencies",
                    "Quality assurance processes",
                    "Support and SLA capabilities",
                    "Operational metrics and KPIs",
                ],
                "status": "pending",
                "risk_level": target.get("operational_risk", "low"),
            },
        }
        total_items = sum(len(v["items"]) for v in checklist.values())
        high_risk_areas = [
            area for area, v in checklist.items() if v["risk_level"] == "high"
        ]
        report = {
            "target": target_name,
            "type": target_type,
            "checklist": checklist,
            "total_items": total_items,
            "areas_completed": 0,
            "high_risk_areas": high_risk_areas,
            "overall_risk": "high" if high_risk_areas else "medium",
            "recommendation": (
                "PROCEED WITH CAUTION" if high_risk_areas else "PROCEED"
            ),
            "next_steps": [
                "Assign due diligence workstream owners",
                "Schedule data room access",
                "Set 2-week review cadence",
                "Engage external advisors for high-risk areas",
            ],
        }
        self._log_event(
            "due_diligence",
            f"Initiated for {target_name} ({target_type}): {total_items} items, "
            f"high-risk areas: {len(high_risk_areas)}",
        )
        logger.info(
            "Due diligence initiated: %s, %d items, %d high-risk areas",
            target_name, total_items, len(high_risk_areas),
        )
        return report

    # ---- Quarterly Review ----

    def generate_quarterly_review(
        self, quarter: str = "Q1", year: int = 2026
    ) -> QuarterlyReview:
        """Generate BD performance dashboard for a quarter.

        Args:
            quarter: Quarter identifier (Q1-Q4).
            year: Year.

        Returns:
            QuarterlyReview with metrics, highlights, challenges.
        """
        import random
        random.seed(hash(f"{quarter}{year}"))

        metrics = [
            BusinessMetric(
                name="Pipeline Generated",
                value=round(random.uniform(800_000, 2_000_000), 2),
                target=1_500_000,
                unit="USD",
                trend="up",
            ),
            BusinessMetric(
                name="Deals Closed",
                value=random.randint(5, 15),
                target=10,
                unit="count",
                trend="up",
            ),
            BusinessMetric(
                name="Average Deal Size",
                value=round(random.uniform(50_000, 150_000), 2),
                target=100_000,
                unit="USD",
                trend="stable",
            ),
            BusinessMetric(
                name="Sales Cycle Length",
                value=round(random.uniform(45, 90), 1),
                target=60,
                unit="days",
                trend="down",
            ),
            BusinessMetric(
                name="Partner Revenue Contribution",
                value=round(random.uniform(100_000, 400_000), 2),
                target=300_000,
                unit="USD",
                trend="up",
            ),
            BusinessMetric(
                name="Win Rate",
                value=round(random.uniform(0.20, 0.40), 3),
                target=0.30,
                unit="ratio",
                trend="stable",
            ),
        ]

        review = QuarterlyReview(
            quarter=quarter,
            year=year,
            metrics=metrics,
            deals_closed=random.randint(5, 15),
            revenue_generated=round(random.uniform(500_000, 1_500_000), 2),
            pipeline_value=round(random.uniform(2_000_000, 5_000_000), 2),
            highlights=[
                "Closed 3 strategic partnerships exceeding target value",
                "Entered new healthcare vertical with 2 design partners",
                "Reduced average sales cycle by 15% through improved qualification",
                "Launched partner portal with 15 active resellers",
            ],
            challenges=[
                "Enterprise deals taking longer due to procurement complexity",
                "Competitive pressure from AI-first entrant on pricing",
                "Partner onboarding slower than planned due to certification requirements",
            ],
            next_quarter_focus=[
                "Accelerate pipeline velocity with improved lead scoring",
                "Launch channel partner program 2.0",
                "Close 2 strategic technology partnerships",
                "Begin international expansion planning",
            ],
        )
        self._log_event(
            "quarterly_review",
            f"Generated {quarter} {year} review: {review.overall_health()}",
        )
        logger.info(
            "Quarterly review (%s %d): health=%s, revenue=$%.0fK, deals=%d",
            quarter, year, review.overall_health(),
            review.revenue_generated / 1000, review.deals_closed,
        )
        return review

    # ---- Outreach ----

    def create_outreach_campaign(
        self,
        name: str = "Q1 Partner Outreach",
        channel: str = "email",
        audience_size: int = 500,
    ) -> OutreachCampaign:
        """Create and analyze an outreach campaign.

        Args:
            name: Campaign name.
            channel: Outreach channel (email, linkedin, events).
            audience_size: Total target audience size.

        Returns:
            OutreachCampaign with projected funnel metrics.
        """
        import random
        random.seed(hash(name))

        sent = audience_size
        response_rates = {"email": 0.08, "linkedin": 0.12, "events": 0.25}
        meeting_rates = {"email": 0.15, "linkedin": 0.20, "events": 0.40}
        deal_rates = {"email": 0.03, "linkedin": 0.05, "events": 0.08}

        rr = response_rates.get(channel, 0.10)
        mr = meeting_rates.get(channel, 0.20)
        dr = deal_rates.get(channel, 0.04)
        spend_per = {"email": 5, "linkedin": 15, "events": 100}

        responses = int(sent * rr)
        meetings = int(responses * mr)
        deals = int(sent * dr)
        spend = sent * spend_per.get(channel, 10)

        campaign = OutreachCampaign(
            name=name,
            channel=channel,
            total_sent=sent,
            responses=responses,
            meetings=meetings,
            deals_generated=deals,
            spend=float(spend),
        )
        self.outreach_campaigns.append(campaign)
        self._log_event(
            "outreach_campaign",
            f"{name}: {sent} sent, {meetings} meetings, {deals} deals, "
            f"CPM=${campaign.cost_per_meeting():.0f}",
        )
        logger.info(
            "Outreach campaign '%s': %d/%d/%d (sent/meet/deal), CPA=$%.0f",
            name, sent, meetings, deals, campaign.cost_per_meeting(),
        )
        return campaign

    # ---- Funnel Analysis ----

    def analyze_conversion_funnel(
        self, funnel_data: Optional[dict[str, list[int]]] = None
    ) -> ConversionFunnel:
        """Analyze a conversion funnel and identify bottlenecks.

        Args:
            funnel_data: Dict with 'stages' (names) and 'counts' (numbers).

        Returns:
            ConversionFunnel with rates and bottleneck identification.
        """
        if funnel_data is None:
            funnel_data = {
                "stages": [
                    "Prospects", "Contacted", "Responded", "Meeting",
                    "Qualified", "Proposal", "Negotiation", "Closed Won",
                ],
                "counts": [1000, 800, 320, 160, 80, 45, 25, 12],
            }
        funnel = ConversionFunnel(
            stage_names=funnel_data.get("stages", []),
            stage_counts=funnel_data.get("counts", []),
        )
        self._log_event(
            "funnel_analysis",
            f"Overall: {funnel.overall_conversion():.2%}, "
            f"Bottleneck: {funnel.bottleneck_stage()}",
        )
        logger.info(
            "Funnel analysis: overall=%.2f%%, bottleneck=%s",
            funnel.overall_conversion() * 100, funnel.bottleneck_stage(),
        )
        return funnel


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def _demo() -> None:
    """Run a comprehensive B2B SaaS business development scenario."""
    print("=" * 72)
    print("  BUSINESS DEVELOPMENT AGENT — B2B SaaS DEMO")
    print("=" * 72)

    agent = BusinessDevelopmentAgent(
        company_name="CloudScale AI", industry="Enterprise AI Platform"
    )

    # 1. Partner Discovery
    print("\n--- 1. Partner Discovery ---")
    candidates = agent.find_partners(
        criteria={
            "industry": "Cloud Infrastructure",
            "min_revenue": 100_000,
            "capabilities": ["cloud hosting", "security", "analytics"],
            "synergy_focus": "revenue",
            "max_results": 8,
        },
        market=MarketSegment.ENTERPRISE,
    )
    for c in candidates[:3]:
        print(
            f"  {c['name']}: score={c['composite_score']:.3f} "
            f"({c['recommendation']})"
        )

    # 2. Partner Evaluation
    print("\n--- 2. Partner Evaluation ---")
    scorecard = agent.evaluate_partner({
        "name": "CloudScale Partner-1",
        "financial_health": 0.85,
        "market_reach": 0.72,
        "tech_capability": 0.90,
        "cultural_fit": 0.78,
        "innovation": 0.82,
        "risk": 0.15,
    })
    print(f"  Overall: {scorecard.overall_score:.3f} -> {scorecard.recommendation()}")

    # 3. Deal Structuring
    print("\n--- 3. Deal Structuring ---")
    deal = agent.structure_deal(
        partner_name="CloudScale Partner-1",
        partnership_type=PartnershipType.TECHNOLOGY,
        deal_value=250_000,
    )
    print(f"  Deal {deal.partner_id}: ${deal.annual_value:,.0f} ({deal.partnership_type.value})")

    # 4. Revenue Modeling
    print("\n--- 4. Revenue Modeling ---")
    for scenario in ["conservative", "base", "aggressive"]:
        rev = agent.model_revenue(scenario=scenario, timeline_months=24, initial_mrr=75_000)
        print(
            f"  {scenario:>14s}: NPV=${rev.npv():>12,.0f}  IRR={rev.irr():.2%}  "
            f"Payback={rev.payback_months(500_000) or 'N/A'} months"
        )

    # 5. Market Analysis
    print("\n--- 5. Market Analysis ---")
    market = agent.analyze_market({
        "industry": "Enterprise AI Platform",
        "market_size": 45_000_000_000,
        "cagr": 0.22,
        "trends": [
            "Generative AI adoption accelerating enterprise-wide",
            "MLOps becoming table stakes",
            "Data sovereignty regulations increasing",
        ],
        "rivalry": 0.65,
        "new_entrants": 0.55,
    })
    print(f"  TAM: ${market.market_size / 1e9:.1f}B  CAGR: {market.cagr:.0%}")
    print(f"  Attractiveness: {market.industry_attractiveness():.3f}")
    print(f"  SWOT strengths: {', '.join(market.swot['strengths'][:2])}")

    # 6. Growth Strategy
    print("\n--- 6. Growth Strategy ---")
    growth = agent.develop_growth_strategy({
        "current_revenue": 3_000_000,
        "products": 1,
        "markets": 1,
        "risk_tolerance": "moderate",
    })
    print(f"  Strategy: {growth.strategy.value}")
    print(f"  Budget: ${growth.budget:,.0f}")
    for obj in growth.objectives[:2]:
        print(f"    - {obj}")

    # 7. Negotiation Strategy
    print("\n--- 7. Negotiation Strategy ---")
    neg = agent.negotiate_deal(
        deal_value=250_000,
        style=NegotiationStyle.COLLABORATIVE,
    )
    print(f"  ZOPA: ${neg.zone_of_possible_agreement[0]:,.0f} - ${neg.zone_of_possible_agreement[1]:,.0f}")
    print(f"  Anchor: ${neg.anchor_point:,.0f}")
    print(f"  Concessions: {len(neg.concessions)}")

    # 8. Value Proposition
    print("\n--- 8. Value Proposition ---")
    vp = agent.create_value_proposition(MarketSegment.ENTERPRISE, "CloudScale Platform")
    print(f"  Headline: {vp.headline}")
    print(f"  Fit score: {vp.score:.3f}")
    print(f"  Jobs: {len(vp.customer_jobs)}, Pains: {len(vp.pains)}, Gains: {len(vp.gains)}")

    # 9. Sales Forecast
    print("\n--- 9. Sales Forecast ---")
    forecast = agent.forecast_sales("Core Platform", period_months=12, base_mrr=120_000)
    print(f"  Expected value: ${forecast.expected_value():,.0f}")
    for name, values in forecast.scenarios.items():
        print(f"    {name}: ${sum(values):>12,.0f} total over 12 months")

    # 10. Competitive Analysis
    print("\n--- 10. Competitive Analysis ---")
    comp = agent.evaluate_competitive_landscape()
    print(f"  Competitors mapped: {comp['competitor_count']}")
    for c in comp["positioning_map"][:3]:
        print(f"    {c['name']}: {c['positioning']} ({c['threat']})")

    # 11. Market Entry
    print("\n--- 11. Market Entry Plan ---")
    entry = agent.plan_market_entry({
        "name": "EMEA Market",
        "segment": "enterprise",
        "timeline_months": 12,
        "budget": 750_000,
    })
    print(f"  Target: {entry['target_market']} ({entry['timeline_months']} months)")
    print(f"  Phases: {len(entry['phases'])}")
    for phase in entry["phases"][:2]:
        print(f"    {phase['phase']}: ${phase['budget_allocation']:,.0f}")

    # 12. Channel Strategy
    print("\n--- 12. Channel Strategy ---")
    channel = agent.design_channel_strategy("CloudScale Platform", MarketSegment.ENTERPRISE)
    print(f"  Channels: {', '.join(channel.channels)}")
    print(f"  Est. deals: {channel.estimated_deals()}, CPA: ${channel.cost_per_acquisition():,.0f}")

    # 13. Due Diligence
    print("\n--- 13. Due Diligence ---")
    dd = agent.conduct_due_diligence({
        "name": "CloudScale Partner-1",
        "type": "strategic_partner",
    })
    print(f"  Items: {dd['total_items']}, High-risk areas: {len(dd['high_risk_areas'])}")
    print(f"  Recommendation: {dd['recommendation']}")

    # 14. Outreach Campaign
    print("\n--- 14. Outreach Campaign ---")
    campaign = agent.create_outreach_campaign("Q1 Strategic Partner Outreach", "linkedin", 300)
    print(f"  {campaign.total_sent} sent, {campaign.meetings} meetings, "
          f"{campaign.deals_generated} deals")
    print(f"  Cost per meeting: ${campaign.cost_per_meeting():,.0f}")

    # 15. Funnel Analysis
    print("\n--- 15. Funnel Analysis ---")
    funnel = agent.analyze_conversion_funnel()
    print(f"  Overall conversion: {funnel.overall_conversion():.2%}")
    print(f"  Bottleneck: {funnel.bottleneck_stage()}")
    for i, rate in enumerate(funnel.conversion_rates()):
        print(f"    {funnel.stage_names[i]} -> {funnel.stage_names[i+1]}: {rate:.1%}")

    # 16. Quarterly Review
    print("\n--- 16. Quarterly Review ---")
    review = agent.generate_quarterly_review("Q1", 2026)
    summary = review.summary()
    print(f"  {summary['quarter']}: health={summary['health']}")
    print(f"  Revenue: ${summary['revenue']:,.0f}, Pipeline: ${summary['pipeline']:,.0f}")
    print(f"  Metrics on track: {summary['metrics_on_track']}/{summary['total_metrics']}")

    print("\n" + "=" * 72)
    print("  DEMO COMPLETE")
    print(f"  Total events logged: {len(agent._event_log)}")
    print("=" * 72)


if __name__ == "__main__":
    _demo()
