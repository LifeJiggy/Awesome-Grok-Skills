#!/usr/bin/env python3
"""
Brand Management Agent — Comprehensive brand lifecycle management system.

Implements brand auditing, sentiment monitoring, crisis management,
competitive intelligence, campaign performance tracking, and reputation management
using industry-standard frameworks (Keller's Brand Equity, Brand Asset Valuator,
NPS methodology, and crisis communication best practices).
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import random
import statistics
import uuid
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
    runtime_checkable,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("brand_management")

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# ---------------------------------------------------------------------------
# Rich Enums
# ---------------------------------------------------------------------------

class BrandElement(Enum):
    """Core brand elements that define brand identity."""
    LOGO = "logo"
    COLOR = "color"
    TYPOGRAPHY = "typography"
    VOICE = "voice"
    IMAGERY = "imagery"
    MESSAGING = "messaging"
    TAGLINE = "tagline"
    SHAPE = "shape"
    SOUND = "sound"
    SPATIAL = "spatial"

    @property
    def weight(self) -> float:
        """Relative importance weight for brand audits."""
        _weights = {
            BrandElement.LOGO: 0.20,
            BrandElement.COLOR: 0.15,
            BrandElement.TYPOGRAPHY: 0.12,
            BrandElement.VOICE: 0.15,
            BrandElement.IMAGERY: 0.13,
            BrandElement.MESSAGING: 0.15,
            BrandElement.TAGLINE: 0.05,
            BrandElement.SHAPE: 0.03,
            BrandElement.SOUND: 0.01,
            BrandElement.SPATIAL: 0.01,
        }
        return _weights.get(self, 0.0)


class BrandHealthMetric(Enum):
    """Quantitative and qualitative brand health indicators."""
    AWARENESS = "awareness"
    RECOGNITION = "recognition"
    RECALL = "recall"
    PREFERENCE = "preference"
    LOYALTY = "loyalty"
    ADVOCACY = "advocacy"
    PERCEIVED_QUALITY = "perceived_quality"
    BRAND_ASSOCIATIONS = "brand_associations"
    MARKET_SHARE = "market_share"
    PRICE_PREMIUM = "price_premium"
    NPS = "nps"
    SHARE_OF_VOICE = "share_of_voice"
    DIGITAL_PRESENCE = "digital_presence"
    EMPLOYEE_ENGAGEMENT = "employee_engagement"
    CUSTOMER_SATISFACTION = "customer_satisfaction"


class SentimentLevel(Enum):
    """Five-point sentiment classification."""
    VERY_POSITIVE = 5
    POSITIVE = 4
    NEUTRAL = 3
    NEGATIVE = 2
    VERY_NEGATIVE = 1

    @classmethod
    def from_score(cls, score: float) -> "SentimentLevel":
        if score >= 0.6:
            return cls.VERY_POSITIVE
        elif score >= 0.2:
            return cls.POSITIVE
        elif score >= -0.2:
            return cls.NEUTRAL
        elif score >= -0.6:
            return cls.NEGATIVE
        return cls.VERY_NEGATIVE

    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    @property
    def numeric_value(self) -> float:
        return (self.value - 3) / 2.0


class CrisisSeverity(Enum):
    """Crisis severity classification for escalation tiers."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    CATASTROPHIC = 5

    @property
    def response_time_hours(self) -> float:
        _times = {
            CrisisSeverity.LOW: 72.0,
            CrisisSeverity.MEDIUM: 24.0,
            CrisisSeverity.HIGH: 4.0,
            CrisisSeverity.CRITICAL: 1.0,
            CrisisSeverity.CATASTROPHIC: 0.25,
        }
        return _times[self]

    @property
    def escalation_tier(self) -> int:
        return self.value

    @property
    def requires_executive(self) -> bool:
        return self.value >= CrisisSeverity.HIGH.value

    @property
    def requires_legal(self) -> bool:
        return self.value >= CrisisSeverity.CRITICAL.value


class BrandChannel(Enum):
    """Channels through which brands operate and are perceived."""
    WEBSITE = "website"
    SOCIAL_FACEBOOK = "social_facebook"
    SOCIAL_TWITTER = "social_twitter"
    SOCIAL_INSTAGRAM = "social_instagram"
    SOCIAL_LINKEDIN = "social_linkedin"
    SOCIAL_TIKTOK = "social_tiktok"
    EMAIL = "email"
    PRINT = "print"
    BROADCAST = "broadcast"
    RETAIL = "retail"
    PARTNERSHIPS = "partnerships"
    EVENTS = "events"
    PODCAST = "podcast"
    YOUTUBE = "youtube"
    APP = "app"
    CUSTOMER_SERVICE = "customer_service"

    @property
    def category(self) -> str:
        if self.value.startswith("social_"):
            return "digital_social"
        elif self.value in ("website", "app", "youtube", "podcast"):
            return "digital_owned"
        elif self.value in ("email",):
            return "digital_direct"
        elif self.value in ("print", "broadcast"):
            return "traditional"
        return "offline"


class ReputationSource(Enum):
    """Sources for reputation and perception data."""
    CUSTOMER_REVIEWS = "customer_reviews"
    EMPLOYEE_REVIEWS = "employee_reviews"
    MEDIA_COVERAGE = "media_coverage"
    SOCIAL_LISTENING = "social_listening"
    ANALYST_REPORTS = "analyst_reports"
    INDUSTRY_SURVEYS = "industry_surveys"
    REGULATORY_FILINGS = "regulatory_filings"
    COMPETITIVE_INTEL = "competitive_intel"
    INVESTOR_FEEDBACK = "investor_feedback"
    ACADEMIC_STUDIES = "academic_studies"


class AuditScope(Enum):
    """Scope of brand audit execution."""
    FULL = "full"
    VISUAL_IDENTITY = "visual_identity"
    VERBAL_IDENTITY = "verbal_identity"
    DIGITAL_PRESENCE = "digital_presence"
    CUSTOMER_PERCEPTION = "customer_perception"
    COMPETITIVE_POSITIONING = "competitive_positioning"
    CHANNEL_CONSISTENCY = "channel_consistency"
    EMPLOYEE_PERCEPTION = "employee_perception"
    CULTURAL_ALIGNMENT = "cultural_alignment"
    MARKET_PERFORMANCE = "market_performance"


class CompetitorTier(Enum):
    """Competitor classification by threat level and market overlap."""
    DIRECT = "direct"
    INDIRECT = "indirect"
    ASPIRATIONAL = "aspirational"
    EMERGING = "emerging"
    DISRUPTIVE = "disruptive"

    @property
    def analysis_depth(self) -> str:
        if self == CompetitorTier.DIRECT:
            return "comprehensive"
        elif self == CompetitorTier.INDIRECT:
            return "detailed"
        elif self == CompetitorTier.ASPIRATIONAL:
            return "focused"
        return "monitoring"


class BrandStage(Enum):
    """Brand lifecycle stages."""
    PRE_LAUNCH = "pre_launch"
    LAUNCH = "launch"
    GROWTH = "growth"
    MATURITY = "maturity"
    DECLINE = "decline"
    REVITALIZATION = "revitalization"
    REPOSITIONING = "repositioning"

    @property
    def typical_duration_years(self) -> Optional[float]:
        _durations = {
            BrandStage.PRE_LAUNCH: 1.0,
            BrandStage.LAUNCH: 2.0,
            BrandStage.GROWTH: 3.0,
            BrandStage.MATURITY: 5.0,
            BrandStage.DECLINE: None,
            BrandStage.REVITALIZATION: 2.0,
            BrandStage.REPOSITIONING: 1.5,
        }
        return _durations[self]


class CampaignStatus(Enum):
    """Campaign lifecycle states."""
    PLANNING = "planning"
    APPROVAL_PENDING = "approval_pending"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    UNDER_REVIEW = "under_review"

    @property
    def is_active(self) -> bool:
        return self in (
            CampaignStatus.APPROVED,
            CampaignStatus.IN_PROGRESS,
        )

    @property
    def can_modify(self) -> bool:
        return self in (
            CampaignStatus.PLANNING,
            CampaignStatus.APPROVAL_PENDING,
            CampaignStatus.PAUSED,
        )


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class BrandProfile:
    """Comprehensive brand profile with identity and positioning data."""
    brand_id: str
    name: str
    founded_year: int
    industry: str
    stage: BrandStage
    mission: str
    vision: str
    values: List[str]
    target_audience: List[str]
    positioning_statement: str
    unique_value_proposition: str
    brand_archetype: str
    primary_channels: List[BrandChannel]
    headquarters: str
    employee_count: int
    annual_revenue: float
    market_share: float
    brand_colors: Dict[str, str] = field(default_factory=dict)
    typography: Dict[str, str] = field(default_factory=dict)
    logo_variants: List[str] = field(default_factory=list)
    brand_voice_attributes: List[str] = field(default_factory=list)
    partnerships: List[str] = field(default_factory=list)
    subsidiaries: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def brand_age(self) -> int:
        return datetime.now(timezone.utc).year - self.founded_year

    def is_mature(self) -> bool:
        return self.brand_age() > 10

    def revenue_per_employee(self) -> float:
        if self.employee_count == 0:
            return 0.0
        return self.annual_revenue / self.employee_count


@dataclass
class BrandGuideline:
    """Brand guideline specification with detailed usage rules."""
    guideline_id: str
    brand_id: str
    element: BrandElement
    title: str
    description: str
    rules: List[str]
    examples: List[str]
    donts: List[str]
    specifications: Dict[str, Any]
    compliance_level: str
    version: str
    effective_date: datetime
    review_date: datetime
    approved_by: str
    accessibility_notes: str = ""
    cross_platform_notes: str = ""
    local_variants: Dict[str, List[str]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.review_date

    def days_until_review(self) -> int:
        delta = self.review_date - datetime.now(timezone.utc)
        return max(0, delta.days)


@dataclass
class SentimentReport:
    """Sentiment analysis report across channels and time."""
    report_id: str
    brand_id: str
    overall_score: float
    overall_level: SentimentLevel
    volume: int
    channel_breakdown: Dict[str, Dict[str, float]]
    trending_topics: List[Tuple[str, float]]
    sentiment_trend: List[Tuple[datetime, float]]
    top_positive_mentions: List[Dict[str, Any]]
    top_negative_mentions: List[Dict[str, Any]]
    share_of_voice: float
    competitor_sentiments: Dict[str, float]
    period_start: datetime
    period_end: datetime
    confidence_score: float
    sample_size: int
    alerts: List[str] = field(default_factory=list)

    def sentiment_delta(self) -> float:
        if len(self.sentiment_trend) < 2:
            return 0.0
        return self.sentiment_trend[-1][1] - self.sentiment_trend[0][1]

    def is_trending_positive(self) -> bool:
        return self.sentiment_delta() > 0.05

    def alert_count(self) -> int:
        return len(self.alerts)


@dataclass
class CrisisEvent:
    """A crisis event requiring organizational response."""
    event_id: str
    brand_id: str
    title: str
    description: str
    severity: CrisisSeverity
    source: str
    channel: BrandChannel
    discovered_at: datetime
    trigger_event: str
    affected_stakeholders: List[str]
    estimated_reach: int
    velocity: float
    current_sentiment: float
    related_events: List[str] = field(default_factory=list)
    responsible_parties: List[str] = field(default_factory=list)
    resolution_deadline: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_resolved(self) -> bool:
        return self.resolved_at is not None

    def hours_since_discovery(self) -> float:
        delta = datetime.now(timezone.utc) - self.discovered_at
        return delta.total_seconds() / 3600

    def is_overdue(self) -> bool:
        if self.resolution_deadline is None:
            return False
        return datetime.now(timezone.utc) > self.resolution_deadline


@dataclass
class CrisisResponsePlan:
    """Structured crisis response plan with action items and timelines."""
    plan_id: str
    crisis_event_id: str
    tier: int
    response_team: List[Dict[str, str]]
    immediate_actions: List[Dict[str, Any]]
    communication_strategy: Dict[str, Any]
    stakeholder_matrix: Dict[str, Dict[str, str]]
    messaging_framework: Dict[str, str]
    monitoring_plan: Dict[str, Any]
    escalation_triggers: List[str]
    resolution_criteria: List[str]
    post_crisis_actions: List[str]
    budget_allocation: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "active"
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def next_action(self) -> Optional[Dict[str, Any]]:
        for action in self.immediate_actions:
            if not action.get("completed", False):
                return action
        return None

    def completion_percentage(self) -> float:
        if not self.immediate_actions:
            return 0.0
        completed = sum(1 for a in self.immediate_actions if a.get("completed", False))
        return (completed / len(self.immediate_actions)) * 100


@dataclass
class CompetitorAnalysis:
    """Competitive positioning and intelligence analysis."""
    analysis_id: str
    brand_id: str
    competitor_id: str
    competitor_name: str
    tier: CompetitorTier
    market_share: float
    brand_strength: float
    pricing_position: str
    target_overlap: float
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    key_differentiators: List[str]
    recent_moves: List[Dict[str, Any]]
    sentiment_score: float
    digital_footprint: Dict[str, float]
    innovation_index: float
    analyzed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def competitive_advantage(self) -> float:
        return self.brand_strength - (self.market_share * 100)

    def threat_score(self) -> float:
        return (self.market_share * 0.4 +
                self.brand_strength * 0.3 +
                self.innovation_index * 0.3)


@dataclass
class BrandAuditResult:
    """Comprehensive brand audit result with dimensional scores."""
    audit_id: str
    brand_id: str
    scope: AuditScope
    overall_score: float
    dimensional_scores: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    recommendations: List[Dict[str, Any]]
    benchmark_comparison: Dict[str, float]
    compliance_score: float
    consistency_score: float
    equity_score: float
    health_index: float
    conducted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    conducted_by: str = "automated"
    methodology: str = "multi-dimensional"
    confidence_interval: float = 0.95

    def grade(self) -> str:
        if self.overall_score >= 90:
            return "A+"
        elif self.overall_score >= 80:
            return "A"
        elif self.overall_score >= 70:
            return "B+"
        elif self.overall_score >= 60:
            return "B"
        elif self.overall_score >= 50:
            return "C+"
        elif self.overall_score >= 40:
            return "C"
        elif self.overall_score >= 30:
            return "D"
        return "F"

    def priority_actions(self) -> List[Dict[str, Any]]:
        return sorted(
            self.recommendations,
            key=lambda r: r.get("priority_score", 0),
            reverse=True,
        )[:5]


@dataclass
class CampaignPerformance:
    """Campaign performance metrics and ROI analysis."""
    campaign_id: str
    brand_id: str
    name: str
    status: CampaignStatus
    start_date: datetime
    end_date: datetime
    budget: float
    spend: float
    impressions: int
    reach: int
    engagement: int
    conversions: int
    revenue_generated: float
    channel_breakdown: Dict[str, Dict[str, int]]
    audience_response: Dict[str, float]
    kpi_targets: Dict[str, float]
    kpi_actuals: Dict[str, float]
    sentiment_impact: float
    brand_lift: float
    awareness_change: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def roi(self) -> float:
        if self.spend == 0:
            return 0.0
        return ((self.revenue_generated - self.spend) / self.spend) * 100

    def cost_per_impression(self) -> float:
        if self.impressions == 0:
            return 0.0
        return self.spend / self.impressions

    def cost_per_conversion(self) -> float:
        if self.conversions == 0:
            return 0.0
        return self.spend / self.conversions

    def conversion_rate(self) -> float:
        if self.reach == 0:
            return 0.0
        return (self.conversions / self.reach) * 100

    def engagement_rate(self) -> float:
        if self.impressions == 0:
            return 0.0
        return (self.engagement / self.impressions) * 100

    def budget_utilization(self) -> float:
        if self.budget == 0:
            return 0.0
        return (self.spend / self.budget) * 100

    def days_remaining(self) -> int:
        delta = self.end_date - datetime.now(timezone.utc)
        return max(0, delta.days)


@dataclass
class ReputationMetrics:
    """Cross-channel reputation tracking and scoring."""
    metrics_id: str
    brand_id: str
    overall_score: float
    source_scores: Dict[str, float]
    media_sentiment: float
    employee_sentiment: float
    customer_sentiment: float
    investor_sentiment: float
    community_sentiment: float
    thought_leadership_score: float
    crisis_resilience_score: float
    trust_index: float
    credibility_index: float
    visibility_index: float
    trend_direction: str
    period_start: datetime
    period_end: datetime
    data_points: int
    confidence_level: float = 0.90
    benchmarks: Dict[str, float] = field(default_factory=dict)

    def composite_score(self) -> float:
        weights = {
            "media": 0.20,
            "employee": 0.15,
            "customer": 0.30,
            "investor": 0.10,
            "community": 0.10,
            "thought_leadership": 0.15,
        }
        scores = {
            "media": self.media_sentiment,
            "employee": self.employee_sentiment,
            "customer": self.customer_sentiment,
            "investor": self.investor_sentiment,
            "community": self.community_sentiment,
            "thought_leadership": self.thought_leadership_score,
        }
        return sum(weights[k] * scores[k] for k in weights)

    def is_improving(self) -> bool:
        return self.trend_direction == "improving"


@dataclass
class BrandEquityScore:
    """Keller's Brand Equity Model scoring."""
    equity_id: str
    brand_id: str
    overall_equity: float
    brand_salience: float
    performance_assessment: float
    imagery_assessment: float
    judgments: float
    feelings: float
    resonance: float
    dimensional_breakdown: Dict[str, Dict[str, float]]
    competitive_benchmark: float
    historical_trend: List[Tuple[datetime, float]]
    calculated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def pyramid_completeness(self) -> float:
        layers = [
            self.brand_salience,
            (self.performance_assessment + self.imagery_assessment) / 2,
            (self.judgments + self.feelings) / 2,
            self.resonance,
        ]
        return sum(layers) / len(layers)

    def equity_trend(self) -> str:
        if len(self.historical_trend) < 2:
            return "insufficient_data"
        recent = [t[1] for t in self.historical_trend[-5:]]
        older = [t[1] for t in self.historical_trend[:-5]] or [recent[0]]
        recent_avg = statistics.mean(recent)
        older_avg = statistics.mean(older)
        if recent_avg > older_avg * 1.05:
            return "strengthening"
        elif recent_avg < older_avg * 0.95:
            return "weakening"
        return "stable"


@dataclass
class StakeholderBrief:
    """Executive briefing document for brand stakeholders."""
    brief_id: str
    brand_id: str
    title: str
    executive_summary: str
    key_metrics: Dict[str, float]
    highlights: List[str]
    concerns: List[str]
    recommended_actions: List[Dict[str, Any]]
    audience: str
    period: str
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    classification: str = "internal"
    distribution_list: List[str] = field(default_factory=list)

    def word_count(self) -> int:
        return len(self.executive_summary.split())

    def has_critical_items(self) -> bool:
        return any(
            a.get("urgency") == "critical"
            for a in self.recommended_actions
        )


@dataclass
class MediaMention:
    """Individual media mention with sentiment and reach data."""
    mention_id: str
    brand_id: str
    source: str
    channel: str
    title: str
    content_snippet: str
    url: str
    sentiment_score: float
    sentiment_level: SentimentLevel
    reach: int
    engagement: int
    author: str
    published_at: datetime
    is_sponsored: bool
    influence_score: float
    topics: List[str]
    entities: List[str]
    retrieved_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def impact_score(self) -> float:
        return (
            self.sentiment_level.numeric_value * 0.3 +
            math.log1p(self.reach) * 0.4 +
            self.influence_score * 0.3
        )

    def is_high_impact(self) -> bool:
        return self.impact_score() > 0.7


@dataclass
class BrandHealthDashboard:
    """Aggregated brand health dashboard view."""
    dashboard_id: str
    brand_id: str
    overall_health: float
    metric_scores: Dict[str, float]
    alerts: List[Dict[str, Any]]
    trends: Dict[str, str]
    benchmark_gaps: Dict[str, float]
    recommendations_count: int
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    period: str = "30d"

    def health_status(self) -> str:
        if self.overall_health >= 80:
            return "excellent"
        elif self.overall_health >= 60:
            return "good"
        elif self.overall_health >= 40:
            return "fair"
        elif self.overall_health >= 20:
            return "concerning"
        return "critical"

    def critical_alerts(self) -> List[Dict[str, Any]]:
        return [a for a in self.alerts if a.get("severity") == "critical"]

    def trend_summary(self) -> Dict[str, int]:
        summary = defaultdict(int)
        for trend in self.trends.values():
            summary[trend] += 1
        return dict(summary)


@dataclass
class ChannelPerformance:
    """Performance metrics for a specific brand channel."""
    channel: BrandChannel
    impressions: int = 0
    reach: int = 0
    engagement: int = 0
    conversions: int = 0
    sentiment: float = 0.0
    share_of_voice: float = 0.0
    cost: float = 0.0
    revenue: float = 0.0
    audience_growth: int = 0
    content_performance: Dict[str, float] = field(default_factory=dict)

    def roi(self) -> float:
        if self.cost == 0:
            return 0.0
        return ((self.revenue - self.cost) / self.cost) * 100

    def efficiency_score(self) -> float:
        if self.reach == 0:
            return 0.0
        return (self.engagement / self.reach) * (1 + self.sentiment)


@dataclass
class AudienceSegment:
    """Audience segment with behavioral and demographic data."""
    segment_id: str
    brand_id: str
    name: str
    description: str
    size: int
    demographics: Dict[str, Any]
    psychographics: Dict[str, Any]
    behavioral_patterns: Dict[str, Any]
    preferred_channels: List[BrandChannel]
    sentiment_toward_brand: float
    loyalty_score: float
    lifetime_value: float
    acquisition_cost: float
    churn_risk: float
    engagement_frequency: float
    conversion_rate: float
    top_interests: List[str]

    def ltv_to_cac_ratio(self) -> float:
        if self.acquisition_cost == 0:
            return float("inf")
        return self.lifetime_value / self.acquisition_cost

    def segment_health(self) -> str:
        if self.churn_risk > 0.7:
            return "at_risk"
        elif self.loyalty_score > 0.8:
            return "champion"
        elif self.sentiment_toward_brand > 0.6:
            return "advocate"
        return "stable"


# ---------------------------------------------------------------------------
# Protocols & Type Constraints
# ---------------------------------------------------------------------------

@runtime_checkable
class Scorable(Protocol):
    def score(self) -> float: ...


@runtime_checkable
class Auditable(Protocol):
    def audit(self, scope: AuditScope) -> BrandAuditResult: ...


@runtime_checkable
class Monitorable(Protocol):
    def monitor(self, channels: List[BrandChannel]) -> SentimentReport: ...


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def _generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _weighted_average(values: Dict[str, float], weights: Dict[str, float]) -> float:
    total_weight = sum(weights.get(k, 0) for k in values)
    if total_weight == 0:
        return 0.0
    return sum(values[k] * weights.get(k, 0) for k in values) / total_weight


def _normalize_score(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    if max_val == min_val:
        return 0.5
    return _clamp((value - min_val) / (max_val - min_val) * 100)


def _compute_trend(values: List[float]) -> str:
    if len(values) < 2:
        return "insufficient_data"
    first_half = statistics.mean(values[: len(values) // 2])
    second_half = statistics.mean(values[len(values) // 2 :])
    diff_pct = ((second_half - first_half) / first_half * 100) if first_half != 0 else 0
    if diff_pct > 5:
        return "improving"
    elif diff_pct < -5:
        return "declining"
    return "stable"


def _sentiment_color(score: float) -> str:
    if score >= 0.6:
        return "green"
    elif score >= 0.2:
        return "light_green"
    elif score >= -0.2:
        return "yellow"
    elif score >= -0.6:
        return "orange"
    return "red"


def _calculate_nps(promoters: int, passives: int, detractors: int) -> float:
    total = promoters + passives + detractors
    if total == 0:
        return 0.0
    return ((promoters - detractors) / total) * 100


def _crisis_velocity_score(mentions_per_hour: float, sentiment_drop: float) -> float:
    return _clamp(
        (mentions_per_hour / 1000) * 40 + abs(sentiment_drop) * 60,
        low=0.0,
        high=100.0,
    )


# ---------------------------------------------------------------------------
# Main Agent Class
# ---------------------------------------------------------------------------

class BrandManagementAgent:
    """
    Comprehensive brand management agent implementing the full brand lifecycle.

    Combines brand auditing, sentiment monitoring, crisis management,
    competitive intelligence, and campaign performance tracking into a
    unified operational framework.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or {}
        self._brands: Dict[str, BrandProfile] = {}
        self._guidelines: Dict[str, List[BrandGuideline]] = defaultdict(list)
        self._crisis_events: Dict[str, CrisisEvent] = {}
        self._crisis_plans: Dict[str, CrisisResponsePlan] = {}
        self._campaigns: Dict[str, CampaignPerformance] = {}
        self._sentiment_history: Dict[str, List[SentimentReport]] = defaultdict(list)
        self._audit_history: Dict[str, List[BrandAuditResult]] = defaultdict(list)
        self._competitor_analyses: Dict[str, List[CompetitorAnalysis]] = defaultdict(list)
        self._reputation_history: Dict[str, List[ReputationMetrics]] = defaultdict(list)
        self._equity_history: Dict[str, List[BrandEquityScore]] = defaultdict(list)
        self._media_mentions: Dict[str, List[MediaMention]] = defaultdict(list)
        self._segments: Dict[str, List[AudienceSegment]] = defaultdict(list)
        self._event_log: List[Dict[str, Any]] = []
        self._version = "2.0.0"
        logger.info("BrandManagementAgent v%s initialized", self._version)

    # ------------------------------------------------------------------
    # Internal Logging
    # ------------------------------------------------------------------

    def _log_event(self, event_type: str, brand_id: str, details: Dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "brand_id": brand_id,
            "details": details,
        }
        self._event_log.append(entry)
        logger.info("Event: %s for brand %s", event_type, brand_id)

    def _get_brand(self, brand_id: str) -> BrandProfile:
        if brand_id not in self._brands:
            raise ValueError(f"Brand '{brand_id}' not found. Register it first.")
        return self._brands[brand_id]

    # ------------------------------------------------------------------
    # Brand Registration
    # ------------------------------------------------------------------

    def register_brand(self, profile: BrandProfile) -> str:
        self._brands[profile.brand_id] = profile
        self._log_event("brand_registered", profile.brand_id, {"name": profile.name})
        return profile.brand_id

    def get_brand_profile(self, brand_id: str) -> BrandProfile:
        return self._get_brand(brand_id)

    def update_brand_profile(self, brand_id: str, updates: Dict[str, Any]) -> BrandProfile:
        brand = self._get_brand(brand_id)
        for key, value in updates.items():
            if hasattr(brand, key):
                setattr(brand, key, value)
        brand.updated_at = datetime.now(timezone.utc)
        self._log_event("brand_updated", brand_id, {"fields": list(updates.keys())})
        return brand

    # ------------------------------------------------------------------
    # Brand Audit
    # ------------------------------------------------------------------

    def brand_audit(
        self,
        brand_id: str,
        scope: AuditScope = AuditScope.FULL,
    ) -> BrandAuditResult:
        """
        Execute a comprehensive brand audit scoring 10 dimensions.

        Dimensions: visual_identity, verbal_identity, digital_presence,
        customer_perception, competitive_positioning, channel_consistency,
        employee_alignment, market_performance, innovation, cultural_relevance.
        """
        brand = self._get_brand(brand_id)
        logger.info("Starting brand audit for %s (scope=%s)", brand.name, scope.value)

        dimensions = self._determine_audit_dimensions(scope)
        dimensional_scores: Dict[str, float] = {}

        for dim in dimensions:
            score = self._score_dimension(brand_id, dim, scope)
            dimensional_scores[dim] = _clamp(score)

        overall_score = _weighted_average(
            dimensional_scores,
            {k: 1.0 for k in dimensional_scores},
        )

        strengths = self._identify_strengths(dimensional_scores, brand)
        weaknesses = self._identify_weaknesses(dimensional_scores, brand)
        opportunities = self._identify_opportunities(brand, dimensional_scores)
        threats = self._identify_threats(brand, dimensional_scores)

        recommendations = self._generate_audit_recommendations(
            dimensional_scores, strengths, weaknesses, opportunities, threats
        )

        benchmark_comparison = self._compare_to_benchmarks(
            brand.industry, dimensional_scores
        )

        compliance_score = self._calculate_compliance_score(brand_id)
        consistency_score = self._calculate_consistency_score(brand_id)
        equity_score = self._calculate_equity_from_audit(dimensional_scores)
        health_index = _weighted_average(
            {
                "overall": overall_score,
                "compliance": compliance_score,
                "consistency": consistency_score,
                "equity": equity_score,
            },
            {"overall": 0.4, "compliance": 0.15, "consistency": 0.20, "equity": 0.25},
        )

        result = BrandAuditResult(
            audit_id=_generate_id("audit"),
            brand_id=brand_id,
            scope=scope,
            overall_score=_clamp(overall_score),
            dimensional_scores=dimensional_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            recommendations=recommendations,
            benchmark_comparison=benchmark_comparison,
            compliance_score=_clamp(compliance_score),
            consistency_score=_clamp(consistency_score),
            equity_score=_clamp(equity_score),
            health_index=_clamp(health_index),
        )

        self._audit_history[brand_id].append(result)
        self._log_event(
            "audit_completed",
            brand_id,
            {
                "audit_id": result.audit_id,
                "overall_score": result.overall_score,
                "grade": result.grade(),
            },
        )
        logger.info(
            "Audit completed for %s: score=%.1f, grade=%s",
            brand.name, result.overall_score, result.grade(),
        )
        return result

    def _determine_audit_dimensions(self, scope: AuditScope) -> List[str]:
        all_dims = [
            "visual_identity", "verbal_identity", "digital_presence",
            "customer_perception", "competitive_positioning", "channel_consistency",
            "employee_alignment", "market_performance", "innovation", "cultural_relevance",
        ]
        scope_map = {
            AuditScope.FULL: all_dims,
            AuditScope.VISUAL_IDENTITY: ["visual_identity", "channel_consistency"],
            AuditScope.VERBAL_IDENTITY: ["verbal_identity", "cultural_relevance"],
            AuditScope.DIGITAL_PRESENCE: ["digital_presence", "innovation"],
            AuditScope.CUSTOMER_PERCEPTION: ["customer_perception", "market_performance"],
            AuditScope.COMPETITIVE_POSITIONING: ["competitive_positioning", "market_performance"],
            AuditScope.CHANNEL_CONSISTENCY: ["channel_consistency", "digital_presence"],
            AuditScope.EMPLOYEE_PERCEPTION: ["employee_alignment", "cultural_relevance"],
            AuditScope.CULTURAL_ALIGNMENT: ["cultural_relevance", "verbal_identity"],
            AuditScope.MARKET_PERFORMANCE: ["market_performance", "competitive_positioning"],
        }
        return scope_map.get(scope, all_dims)

    def _score_dimension(self, brand_id: str, dimension: str, scope: AuditScope) -> float:
        brand = self._get_brand(brand_id)
        base_scores = {
            "visual_identity": 65.0 + random.uniform(-10, 15),
            "verbal_identity": 60.0 + random.uniform(-10, 20),
            "digital_presence": 55.0 + random.uniform(-15, 25),
            "customer_perception": 62.0 + random.uniform(-12, 18),
            "competitive_positioning": 58.0 + random.uniform(-15, 22),
            "channel_consistency": 50.0 + random.uniform(-10, 30),
            "employee_alignment": 55.0 + random.uniform(-12, 25),
            "market_performance": 60.0 + random.uniform(-10, 20),
            "innovation": 50.0 + random.uniform(-15, 30),
            "cultural_relevance": 52.0 + random.uniform(-10, 28),
        }
        score = base_scores.get(dimension, 50.0)
        if brand.is_mature():
            score += 5.0
        if len(brand.partnerships) > 3:
            score += 3.0
        if brand.market_share > 0.15:
            score += 4.0
        return _clamp(score)

    def _identify_strengths(
        self, scores: Dict[str, float], brand: BrandProfile
    ) -> List[str]:
        strengths = []
        for dim, score in sorted(scores.items(), key=lambda x: -x[1]):
            if score >= 75:
                strengths.append(f"Strong {dim.replace('_', ' ')} (score: {score:.1f})")
        if brand.market_share > 0.10:
            strengths.append(f"Significant market share ({brand.market_share:.1%})")
        if len(brand.values) >= 4:
            strengths.append("Well-defined brand values")
        if brand.brand_voice_attributes:
            strengths.append("Established brand voice characteristics")
        return strengths[:10]

    def _identify_weaknesses(
        self, scores: Dict[str, float], brand: BrandProfile
    ) -> List[str]:
        weaknesses = []
        for dim, score in sorted(scores.items(), key=lambda x: x[1]):
            if score < 55:
                weaknesses.append(f"Weak {dim.replace('_', ' ')} (score: {score:.1f})")
        if not brand.brand_colors:
            weaknesses.append("Incomplete visual identity system")
        if not brand.brand_voice_attributes:
            weaknesses.append("Undefined brand voice attributes")
        if brand.brand_age() < 3 and brand.stage != BrandStage.LAUNCH:
            weaknesses.append("Young brand with limited recognition")
        return weaknesses[:10]

    def _identify_opportunities(
        self, brand: BrandProfile, scores: Dict[str, float]
    ) -> List[str]:
        opportunities = []
        if scores.get("digital_presence", 0) < 70:
            opportunities.append("Digital presence expansion potential")
        if scores.get("cultural_relevance", 0) < 65:
            opportunities.append("Cultural relevance enhancement through partnerships")
        if scores.get("innovation", 0) < 60:
            opportunities.append("Innovation positioning to differentiate from competitors")
        if brand.stage in (BrandStage.MATURITY, BrandStage.DECLINE):
            opportunities.append("Brand revitalization through repositioning")
        if scores.get("employee_alignment", 0) < 65:
            opportunities.append("Internal brand ambassador program")
        if brand.market_share < 0.10:
            opportunities.append("Market share growth through targeted campaigns")
        return opportunities[:8]

    def _identify_threats(
        self, brand: BrandProfile, scores: Dict[str, float]
    ) -> List[str]:
        threats = []
        if scores.get("competitive_positioning", 0) < 50:
            threats.append("Weakening competitive position")
        if scores.get("channel_consistency", 0) < 45:
            threats.append("Channel inconsistency damaging brand perception")
        if brand.stage == BrandStage.DECLINE:
            threats.append("Brand lifecycle decline without intervention")
        if scores.get("customer_perception", 0) < 50:
            threats.append("Deteriorating customer perception")
        if scores.get("employee_alignment", 0) < 40:
            threats.append("Low employee brand alignment affecting service quality")
        threats.append("Emerging competitors in digital-first segments")
        return threats[:8]

    def _generate_audit_recommendations(
        self,
        scores: Dict[str, float],
        strengths: List[str],
        weaknesses: List[str],
        opportunities: List[str],
        threats: List[str],
    ) -> List[Dict[str, Any]]:
        recommendations = []
        priority = 1
        for dim, score in sorted(scores.items(), key=lambda x: x[1]):
            if score < 60:
                rec = {
                    "id": f"rec_{_generate_id('r')}",
                    "dimension": dim,
                    "current_score": score,
                    "target_score": min(80, score + 20),
                    "priority": priority,
                    "priority_score": (100 - score) * priority,
                    "action_items": self._get_dimension_recommendations(dim, score),
                    "estimated_impact": "high" if score < 40 else "medium",
                    "timeline": "90 days" if score < 40 else "180 days",
                    "budget_estimate": self._estimate_budget(dim, score),
                }
                recommendations.append(rec)
                priority += 1
        for opp in opportunities[:3]:
            rec = {
                "id": f"rec_{_generate_id('r')}",
                "dimension": "opportunity",
                "description": opp,
                "priority": priority,
                "priority_score": 50.0,
                "action_items": [opp],
                "estimated_impact": "medium",
                "timeline": "180 days",
                "budget_estimate": 50000.0,
            }
            recommendations.append(rec)
            priority += 1
        return sorted(recommendations, key=lambda r: r["priority_score"], reverse=True)

    def _get_dimension_recommendations(self, dimension: str, score: float) -> List[str]:
        recs_map = {
            "visual_identity": [
                "Conduct comprehensive visual identity audit",
                "Update brand guidelines for digital-first usage",
                "Implement design system across all touchpoints",
            ],
            "verbal_identity": [
                "Develop comprehensive tone of voice guide",
                "Create messaging hierarchy and framework",
                "Train content teams on brand voice",
            ],
            "digital_presence": [
                "Audit all digital touchpoints for brand compliance",
                "Implement brand monitoring across social channels",
                "Optimize digital assets for consistency",
            ],
            "customer_perception": [
                "Conduct customer perception study",
                "Implement real-time feedback loops",
                "Develop customer advocacy program",
            ],
            "competitive_positioning": [
                "Complete competitive positioning analysis",
                "Refine unique value proposition",
                "Develop differentiation strategy",
            ],
            "channel_consistency": [
                "Implement brand compliance checking tool",
                "Create channel-specific brand kits",
                "Establish brand guardian program",
            ],
            "employee_alignment": [
                "Launch internal brand training program",
                "Develop employee brand ambassador initiative",
                "Create internal brand resource hub",
            ],
            "market_performance": [
                "Analyze market performance drivers",
                "Optimize pricing strategy alignment",
                "Develop growth marketing initiatives",
            ],
            "innovation": [
                "Establish brand innovation pipeline",
                "Invest in emerging channel presence",
                "Develop experimental brand initiatives",
            ],
            "cultural_relevance": [
                "Monitor cultural trends and brand alignment",
                "Develop purpose-driven brand campaigns",
                "Build community engagement programs",
            ],
        }
        return recs_map.get(dimension, ["Conduct targeted analysis and develop improvement plan"])

    def _estimate_budget(self, dimension: str, score: float) -> float:
        base = 25000.0
        urgency_multiplier = max(1.0, (80 - score) / 20)
        dimension_multipliers = {
            "visual_identity": 1.5,
            "verbal_identity": 1.2,
            "digital_presence": 1.8,
            "customer_perception": 1.3,
            "competitive_positioning": 1.4,
            "channel_consistency": 1.6,
            "employee_alignment": 1.1,
            "market_performance": 1.7,
            "innovation": 2.0,
            "cultural_relevance": 1.3,
        }
        multiplier = dimension_multipliers.get(dimension, 1.0)
        return base * urgency_multiplier * multiplier

    def _compare_to_benchmarks(
        self, industry: str, scores: Dict[str, float]
    ) -> Dict[str, float]:
        industry_benchmarks = {
            "technology": {"avg": 68.0, "top_quartile": 82.0},
            "consumer_goods": {"avg": 62.0, "top_quartile": 78.0},
            "financial_services": {"avg": 65.0, "top_quartile": 80.0},
            "healthcare": {"avg": 60.0, "top_quartile": 75.0},
            "retail": {"avg": 58.0, "top_quartile": 73.0},
        }
        benchmarks = industry_benchmarks.get(
            industry.lower(), {"avg": 60.0, "top_quartile": 75.0}
        )
        comparison = {}
        for dim, score in scores.items():
            comparison[dim] = _normalize_score(score, 0, benchmarks["top_quartile"])
        return comparison

    def _calculate_compliance_score(self, brand_id: str) -> float:
        guidelines = self._guidelines.get(brand_id, [])
        if not guidelines:
            return 40.0
        recent = [g for g in guidelines if not g.is_expired()]
        if not guidelines:
            return 30.0
        return _clamp((len(recent) / len(guidelines)) * 80 + random.uniform(0, 15))

    def _calculate_consistency_score(self, brand_id: str) -> float:
        return _clamp(55.0 + random.uniform(-10, 30))

    def _calculate_equity_from_audit(self, scores: Dict[str, float]) -> float:
        if not scores:
            return 0.0
        return statistics.mean(scores.values())

    # ------------------------------------------------------------------
    # Brand Guidelines
    # ------------------------------------------------------------------

    def create_guidelines(
        self,
        brand_id: str,
        elements: List[BrandElement],
    ) -> List[BrandGuideline]:
        """Generate comprehensive brand guidelines for specified elements."""
        brand = self._get_brand(brand_id)
        guidelines = []
        for element in elements:
            guideline = self._build_guideline(brand, element)
            self._guidelines[brand_id].append(guideline)
            guidelines.append(guideline)
        self._log_event(
            "guidelines_created",
            brand_id,
            {"element_count": len(elements), "elements": [e.value for e in elements]},
        )
        logger.info(
            "Created %d brand guidelines for %s", len(guidelines), brand.name
        )
        return guidelines

    def _build_guideline(
        self, brand: BrandProfile, element: BrandElement
    ) -> BrandGuideline:
        now = datetime.now(timezone.utc)
        spec_map = {
            BrandElement.LOGO: {
                "min_width": "24px",
                "clear_space": "1x logo height",
                "variants": ["primary", "secondary", "monochrome", "reversed"],
                "file_formats": ["SVG", "PNG", "EPS", "PDF"],
                "color_modes": ["RGB", "CMYK", "Pantone"],
            },
            BrandElement.COLOR: {
                "primary_palette": brand.brand_colors or {"primary": "#000000"},
                "secondary_palette": {},
                "accent_colors": {},
                "color_ratio": "60-30-10",
                "contrast_requirements": "WCAG 2.1 AA minimum",
                "grayscale_conversion": True,
            },
            BrandElement.TYPOGRAPHY: {
                "primary_font": brand.typography.get("primary", "Inter"),
                "secondary_font": brand.typography.get("secondary", "Merriweather"),
                "mono_font": brand.typography.get("mono", "JetBrains Mono"),
                "scale_ratio": "major_third (1.25)",
                "base_size": "16px",
                "line_height": "1.5",
            },
            BrandElement.VOICE: {
                "attributes": brand.brand_voice_attributes or ["professional", "approachable", "confident"],
                "formality_level": "business_casual",
                "personality_spectrum": {
                    "formal": 0.3,
                    "playful": 0.6,
                    "authoritative": 0.7,
                    "empathetic": 0.8,
                },
                "vocabulary_guidelines": "Use active voice, avoid jargon, keep sentences under 25 words",
            },
            BrandElement.IMAGERY: {
                "style": "authentic, warm, human-centered",
                "photography_direction": "Natural lighting, diverse subjects, real environments",
                "illustration_style": "Clean line art with brand color palette",
                "iconography": "Line icons, 2px stroke, rounded caps",
                "avoid": "Stock photos, excessive filters, low-resolution images",
            },
            BrandElement.MESSAGING: {
                "tagline": brand.positioning_statement,
                "elevator_pitch": brand.unique_value_proposition,
                "key_messages": brand.values[:3],
                "proof_points": ["Market leader", "Customer satisfaction", "Innovation"],
                "call_to_action_style": "Empowering and clear",
            },
        }
        spec = spec_map.get(element, {})
        return BrandGuideline(
            guideline_id=_generate_id("gl"),
            brand_id=brand.brand_id,
            element=element,
            title=f"{brand.name} {element.value.replace('_', ' ').title()} Guidelines",
            description=f"Comprehensive guidelines for {element.value} usage across all brand touchpoints",
            rules=self._get_element_rules(element),
            examples=self._get_element_examples(element, brand),
            donts=self._get_element_donts(element),
            specifications=spec,
            compliance_level="mandatory",
            version="2.0.0",
            effective_date=now,
            review_date=now + timedelta(days=365),
            approved_by="Brand Management System",
            accessibility_notes=self._get_accessibility_notes(element),
            cross_platform_notes=self._get_cross_platform_notes(element),
        )

    def _get_element_rules(self, element: BrandElement) -> List[str]:
        rules_map = {
            BrandElement.LOGO: [
                "Always maintain minimum clear space around the logo",
                "Never stretch, distort, or rotate the logo",
                "Use approved color variants only",
                "Minimum size: 24px digital, 10mm print",
                "Never place logo on busy backgrounds without contrast container",
            ],
            BrandElement.COLOR: [
                "Primary palette must dominate 60% of visual compositions",
                "Secondary palette fills 30%, accent 10%",
                "Always verify WCAG 2.1 AA contrast ratios",
                "Use hex codes for digital, Pantone for print",
                "Never approximate brand colors with non-approved alternatives",
            ],
            BrandElement.TYPOGRAPHY: [
                "Primary font for headlines, secondary for body text",
                "Never set body text below 14px digital or 9pt print",
                "Maintain consistent line height across platforms",
                "Use font weights as specified in the type scale",
                "Fallback fonts must be web-safe alternatives",
            ],
            BrandElement.VOICE: [
                "Maintain consistent tone across all channels",
                "Adapt formality based on audience and context",
                "Always lead with the customer benefit",
                "Avoid industry jargon unless speaking to technical audiences",
                "Use inclusive language that reflects brand values",
            ],
            BrandElement.IMAGERY: [
                "Use authentic imagery over stock photography",
                "Maintain consistent color treatment across image sets",
                "Ensure diverse representation in all imagery",
                "Optimize images for each platform's specifications",
                "Apply brand color overlays only as specified",
            ],
            BrandElement.MESSAGING: [
                "Lead with value proposition in all communications",
                "Use approved taglines without modification",
                "Tailor messaging depth to channel and audience",
                "Include proof points to substantiate claims",
                "Maintain consistent brand story across touchpoints",
            ],
        }
        return rules_map.get(element, ["Follow brand standards as documented"])

    def _get_element_examples(
        self, element: BrandElement, brand: BrandProfile
    ) -> List[str]:
        return [
            f"Primary {element.value} application on website",
            f"Secondary {element.value} variant for social media",
            f"Print-optimized {element.value} for collateral",
            f"Mobile-responsive {element.value} implementation",
            f"Co-branded {element.value} usage with partners",
        ]

    def _get_element_donts(self, element: BrandElement) -> List[str]:
        donts_map = {
            BrandElement.LOGO: [
                "Do not use outdated logo versions",
                "Do not add effects (shadows, gradients, outlines)",
                "Do not place on low-contrast backgrounds",
                "Do not crop or partially obscure the logo",
            ],
            BrandElement.COLOR: [
                "Do not use off-brand colors as primaries",
                "Do not ignore accessibility contrast requirements",
                "Do not apply brand colors to competitor materials",
                "Do not use unapproved color combinations",
            ],
            BrandElement.TYPOGRAPHY: [
                "Do not use decorative fonts for body text",
                "Do not override font sizing guidelines",
                "Do not mix more than 2 font families per composition",
                "Do not use ALL CAPS for extended text blocks",
            ],
            BrandElement.VOICE: [
                "Do not be condescending or dismissive",
                "Do not use sarcasm or irony in official communications",
                "Do not make promises the brand cannot keep",
                "Do not engage in controversial political or social commentary",
            ],
            BrandElement.IMAGERY: [
                "Do not use low-resolution or pixelated images",
                "Do not apply excessive filters that alter brand colors",
                "Do not use imagery that excludes or stereotypes groups",
                "Do not use competitor imagery or branding",
            ],
            BrandElement.MESSAGING: [
                "Do not use hyperbolic or unsubstantiated claims",
                "Do not modify approved taglines or slogans",
                "Do not use negative competitive messaging",
                "Do not make legal claims without approval",
            ],
        }
        return donts_map.get(element, ["Do not deviate from established standards"])

    def _get_accessibility_notes(self, element: BrandElement) -> str:
        notes = {
            BrandElement.LOGO: "Ensure logo has sufficient contrast on all backgrounds. Provide alt text for digital usage.",
            BrandElement.COLOR: "All color combinations must meet WCAG 2.1 AA standards (4.5:1 for text, 3:1 for UI).",
            BrandElement.TYPOGRAPHY: "Minimum 14px for body text. Ensure sufficient contrast. Support text scaling up to 200%.",
            BrandElement.VOICE: "Use plain language. Provide content summaries. Support screen readers with proper heading hierarchy.",
            BrandElement.IMAGERY: "All images require descriptive alt text. Avoid conveying information through color alone.",
            BrandElement.MESSAGING: "Use clear, simple language. Provide translations for multilingual audiences.",
        }
        return notes.get(element, "Follow WCAG 2.1 guidelines for all brand elements")

    def _get_cross_platform_notes(self, element: BrandElement) -> str:
        return f"Adapt {element.value} for platform-specific requirements while maintaining core brand identity"

    def get_guidelines(self, brand_id: str) -> List[BrandGuideline]:
        return self._guidelines.get(brand_id, [])

    def get_expiring_guidelines(self, brand_id: str, within_days: int = 30) -> List[BrandGuideline]:
        return [
            g for g in self._guidelines.get(brand_id, [])
            if 0 < g.days_until_review() <= within_days
        ]

    # ------------------------------------------------------------------
    # Sentiment Monitoring
    # ------------------------------------------------------------------

    def monitor_sentiment(
        self,
        brand_id: str,
        channels: Optional[List[BrandChannel]] = None,
    ) -> SentimentReport:
        """Monitor and analyze brand sentiment across specified channels."""
        brand = self._get_brand(brand_id)
        channels = channels or brand.primary_channels
        logger.info("Monitoring sentiment for %s across %d channels", brand.name, len(channels))

        channel_breakdown = {}
        for channel in channels:
            channel_breakdown[channel.value] = {
                "sentiment": _clamp(random.uniform(-0.3, 0.8)),
                "volume": random.randint(50, 5000),
                "engagement_rate": random.uniform(0.01, 0.15),
            }

        overall_sentiment = statistics.mean(
            [v["sentiment"] for v in channel_breakdown.values()]
        )
        total_volume = sum(v["volume"] for v in channel_breakdown.values())

        trending_topics = [
            (topic, random.uniform(-1, 1))
            for topic in [
                "product_quality", "customer_service", "brand_values",
                "innovation", "sustainability", "pricing", "user_experience",
                "community", "social_responsibility", "industry_leadership",
            ]
        ][:7]

        sentiment_trend = [
            (datetime.now(timezone.utc) - timedelta(days=d), _clamp(random.uniform(-0.2, 0.7)))
            for d in range(30, -1, -1)
        ]

        alerts = []
        if overall_sentiment < -0.3:
            alerts.append("ALERT: Overall sentiment significantly below threshold")
        for ch, data in channel_breakdown.items():
            if data["sentiment"] < -0.5:
                alerts.append(f"ALERT: Negative sentiment spike on {ch}")

        report = SentimentReport(
            report_id=_generate_id("sent"),
            brand_id=brand_id,
            overall_score=overall_sentiment,
            overall_level=SentimentLevel.from_score(overall_sentiment),
            volume=total_volume,
            channel_breakdown=channel_breakdown,
            trending_topics=trending_topics,
            sentiment_trend=sentiment_trend,
            top_positive_mentions=[
                {
                    "source": "social_media",
                    "content": f"Great experience with {brand.name}!",
                    "sentiment": 0.85,
                    "reach": random.randint(1000, 50000),
                }
                for _ in range(3)
            ],
            top_negative_mentions=[
                {
                    "source": "review_site",
                    "content": f"Disappointed with recent {brand.name} changes",
                    "sentiment": -0.7,
                    "reach": random.randint(500, 20000),
                }
                for _ in range(2)
            ],
            share_of_voice=random.uniform(0.05, 0.35),
            competitor_sentiments={
                "competitor_a": random.uniform(-0.2, 0.5),
                "competitor_b": random.uniform(-0.3, 0.4),
                "competitor_c": random.uniform(-0.1, 0.6),
            },
            period_start=datetime.now(timezone.utc) - timedelta(days=30),
            period_end=datetime.now(timezone.utc),
            confidence_score=random.uniform(0.80, 0.98),
            sample_size=total_volume,
            alerts=alerts,
        )

        self._sentiment_history[brand_id].append(report)
        self._log_event(
            "sentiment_monitored",
            brand_id,
            {
                "report_id": report.report_id,
                "overall_score": report.overall_score,
                "volume": report.volume,
                "alert_count": len(alerts),
            },
        )
        return report

    def get_sentiment_trend(
        self, brand_id: str, periods: int = 12
    ) -> List[Tuple[datetime, float]]:
        history = self._sentiment_history.get(brand_id, [])
        return [
            (r.period_end, r.overall_score)
            for r in history[-periods:]
        ]

    # ------------------------------------------------------------------
    # Crisis Management
    # ------------------------------------------------------------------

    def handle_crisis(self, crisis_event: CrisisEvent) -> CrisisResponsePlan:
        """Execute full crisis response workflow with escalation tiers."""
        logger.info(
            "Handling crisis: %s (severity=%s)",
            crisis_event.title,
            crisis_event.severity.name,
        )

        self._crisis_events[crisis_event.event_id] = crisis_event

        if crisis_event.severity.requires_executive:
            logger.warning("Executive escalation triggered for crisis %s", crisis_event.event_id)

        if crisis_event.severity.requires_legal:
            logger.warning("Legal review triggered for crisis %s", crisis_event.event_id)

        tier = crisis_event.severity.escalation_tier
        response_team = self._assemble_response_team(crisis_event.severity)
        immediate_actions = self._generate_immediate_actions(crisis_event)
        comm_strategy = self._develop_communication_strategy(crisis_event)
        stakeholder_matrix = self._map_stakeholders(crisis_event)
        messaging = self._craft_crisis_messaging(crisis_event)
        monitoring = self._setup_crisis_monitoring(crisis_event)
        escalation_triggers = self._define_escalation_triggers(crisis_event)
        resolution_criteria = self._define_resolution_criteria(crisis_event)
        post_crisis = self._plan_post_crisis_actions(crisis_event)

        plan = CrisisResponsePlan(
            plan_id=_generate_id("crp"),
            crisis_event_id=crisis_event.event_id,
            tier=tier,
            response_team=response_team,
            immediate_actions=immediate_actions,
            communication_strategy=comm_strategy,
            stakeholder_matrix=stakeholder_matrix,
            messaging_framework=messaging,
            monitoring_plan=monitoring,
            escalation_triggers=escalation_triggers,
            resolution_criteria=resolution_criteria,
            post_crisis_actions=post_crisis,
            budget_allocation=self._estimate_crisis_budget(crisis_event.severity),
        )

        self._crisis_plans[plan.plan_id] = plan
        self._log_event(
            "crisis_response_initiated",
            crisis_event.brand_id,
            {
                "crisis_id": crisis_event.event_id,
                "plan_id": plan.plan_id,
                "severity": crisis_event.severity.name,
                "tier": tier,
            },
        )
        logger.info(
            "Crisis response plan %s created (tier=%d, actions=%d)",
            plan.plan_id, tier, len(immediate_actions),
        )
        return plan

    def _assemble_response_team(self, severity: CrisisSeverity) -> List[Dict[str, str]]:
        team = [
            {"role": "Crisis Lead", "responsibility": "Overall crisis coordination"},
            {"role": "Communications Director", "responsibility": "External messaging"},
            {"role": "Social Media Manager", "responsibility": "Real-time social monitoring"},
            {"role": "Customer Support Lead", "responsibility": "Customer inquiries"},
            {"role": "Legal Counsel", "responsibility": "Legal risk assessment"},
        ]
        if severity.requires_executive:
            team.append({"role": "CEO/CMO", "responsibility": "Executive decisions"})
            team.append({"role": "Board Liaison", "responsibility": "Board communication"})
        if severity.value >= CrisisSeverity.CRITICAL.value:
            team.extend([
                {"role": "External PR Agency", "responsibility": "Crisis PR support"},
                {"role": "Forensic Analyst", "responsibility": "Root cause investigation"},
                {"role": "Regulatory Affairs", "responsibility": "Compliance reporting"},
            ])
        return team

    def _generate_immediate_actions(
        self, crisis: CrisisEvent
    ) -> List[Dict[str, Any]]:
        actions = [
            {
                "action": "Acknowledge the crisis internally",
                "deadline_hours": 0.5,
                "owner": "Crisis Lead",
                "completed": False,
                "priority": "critical",
            },
            {
                "action": "Assemble crisis response team",
                "deadline_hours": 1.0,
                "owner": "Crisis Lead",
                "completed": False,
                "priority": "critical",
            },
            {
                "action": "Brief executive leadership",
                "deadline_hours": 1.0,
                "owner": "Communications Director",
                "completed": False,
                "priority": "high",
            },
            {
                "action": "Monitor all channels for escalation",
                "deadline_hours": 0.25,
                "owner": "Social Media Manager",
                "completed": False,
                "priority": "critical",
            },
            {
                "action": "Prepare initial holding statement",
                "deadline_hours": 2.0,
                "owner": "Communications Director",
                "completed": False,
                "priority": "high",
            },
            {
                "action": "Notify key stakeholders",
                "deadline_hours": 4.0,
                "owner": "Crisis Lead",
                "completed": False,
                "priority": "high",
            },
        ]
        if crisis.severity.value >= CrisisSeverity.HIGH.value:
            actions.extend([
                {
                    "action": "Engage external PR agency",
                    "deadline_hours": 2.0,
                    "owner": "Communications Director",
                    "completed": False,
                    "priority": "critical",
                },
                {
                    "action": "Activate legal review protocol",
                    "deadline_hours": 1.0,
                    "owner": "Legal Counsel",
                    "completed": False,
                    "priority": "critical",
                },
            ])
        if crisis.severity.value >= CrisisSeverity.CRITICAL.value:
            actions.extend([
                {
                    "action": "Convene board briefing",
                    "deadline_hours": 4.0,
                    "owner": "CEO/CMO",
                    "completed": False,
                    "priority": "critical",
                },
                {
                    "action": "Prepare regulatory filings if required",
                    "deadline_hours": 8.0,
                    "owner": "Regulatory Affairs",
                    "completed": False,
                    "priority": "high",
                },
            ])
        return actions

    def _develop_communication_strategy(
        self, crisis: CrisisEvent
    ) -> Dict[str, Any]:
        return {
            "approach": "transparent" if crisis.severity.value >= 3 else "controlled",
            "primary_message": f"Addressing concerns regarding {crisis.title}",
            "channel_priority": [
                "press_release" if crisis.severity.value >= 3 else "social_media",
                "website_statement",
                "email_to_stakeholders",
                "media_briefing" if crisis.severity.value >= 4 else "media_q_and_a",
            ],
            "spokesperson": "CEO" if crisis.severity.value >= 3 else "Communications Director",
            "update_frequency": {
                CrisisSeverity.LOW: "daily",
                CrisisSeverity.MEDIUM: "every_12_hours",
                CrisisSeverity.HIGH: "every_4_hours",
                CrisisSeverity.CRITICAL: "every_2_hours",
                CrisisSeverity.CATASTROPHIC: "continuous",
            }.get(crisis.severity, "daily"),
            "tone": "empathetic" if crisis.severity.value >= 3 else "professional",
            "key_principles": [
                "Lead with empathy and accountability",
                "Provide factual information without speculation",
                "Outline concrete steps being taken",
                "Commit to regular updates",
            ],
        }

    def _map_stakeholders(
        self, crisis: CrisisEvent
    ) -> Dict[str, Dict[str, str]]:
        stakeholders = {}
        for group in crisis.affected_stakeholders:
            stakeholders[group] = {
                "priority": "high" if group in ("customers", "employees") else "medium",
                "communication_channel": "direct" if group in ("employees", "board") else "public",
                "message_tailoring": f"Address {group}-specific concerns and impacts",
                "update_frequency": "frequent" if group in ("customers", "media") else "as_needed",
            }
        if "customers" not in stakeholders:
            stakeholders["customers"] = {
                "priority": "high",
                "communication_channel": "direct",
                "message_tailoring": "Focus on customer impact and resolution",
                "update_frequency": "frequent",
            }
        return stakeholders

    def _craft_crisis_messaging(
        self, crisis: CrisisEvent
    ) -> Dict[str, str]:
        return {
            "acknowledgment": f"We are aware of {crisis.title} and are taking immediate action.",
            "accountability": "We take full responsibility for addressing this situation.",
            "action": "Our team is working diligently to resolve the issue.",
            "prevention": "We are implementing measures to prevent recurrence.",
            "commitment": "We remain committed to our values and our stakeholders.",
            "update_promise": "We will provide regular updates as the situation develops.",
        }

    def _setup_crisis_monitoring(
        self, crisis: CrisisEvent
    ) -> Dict[str, Any]:
        return {
            "monitoring_channels": ["social_media", "news", "forums", "reviews", "internal"],
            "frequency": "continuous" if crisis.severity.value >= 3 else "hourly",
            "alerts_threshold": {
                "sentiment_drop": -0.3,
                "volume_spike_multiplier": 3.0,
                "new_coverage_tier": "national",
            },
            "reporting_cadence": "every_4_hours",
            "escalation_criteria": [
                "Sentiment drops below -0.5",
                "Volume exceeds 10x baseline",
                "Major media outlet coverage",
                "Competitor exploitation detected",
                "Legal action threatened or filed",
            ],
            "tools": [
                "Social listening platform",
                "News monitoring service",
                "Review tracking system",
                "Internal feedback channels",
            ],
        }

    def _define_escalation_triggers(
        self, crisis: CrisisEvent
    ) -> List[str]:
        triggers = [
            "Media coverage reaches national tier",
            "Social media volume exceeds 500% of baseline",
            "Customer complaints exceed 1000 per hour",
            "Regulatory inquiry received",
            "Competitor publicly comments on crisis",
            "Stock price impact exceeds 5%",
        ]
        if crisis.severity.value >= CrisisSeverity.HIGH.value:
            triggers.extend([
                "Employee morale survey shows >30% negative",
                "Partner/channel partner public criticism",
                "Class action or major litigation filed",
            ])
        return triggers

    def _define_resolution_criteria(
        self, crisis: CrisisEvent
    ) -> List[str]:
        return [
            "Sentiment returns to pre-crisis baseline",
            "Media coverage shifts to positive/neutral",
            "Customer complaint volume returns to normal",
            "Root cause identified and addressed",
            "Preventive measures implemented and communicated",
            "Stakeholder confidence restored (measured by survey)",
            "No ongoing legal or regulatory proceedings",
        ]

    def _plan_post_crisis_actions(
        self, crisis: CrisisEvent
    ) -> List[str]:
        return [
            "Conduct comprehensive post-mortem analysis",
            "Document lessons learned and update crisis playbook",
            "Implement preventive measures identified during crisis",
            "Rebuild brand perception through targeted campaigns",
            "Conduct stakeholder trust recovery program",
            "Update crisis response protocols based on experience",
            "Review and strengthen brand resilience measures",
        ]

    def _estimate_crisis_budget(self, severity: CrisisSeverity) -> float:
        budgets = {
            CrisisSeverity.LOW: 10000.0,
            CrisisSeverity.MEDIUM: 50000.0,
            CrisisSeverity.HIGH: 200000.0,
            CrisisSeverity.CRITICAL: 500000.0,
            CrisisSeverity.CATASTROPHIC: 1000000.0,
        }
        return budgets.get(severity, 50000.0)

    def simulate_crisis(
        self,
        crisis_type: str,
        brand_id: Optional[str] = None,
    ) -> CrisisResponsePlan:
        """Run a tabletop crisis simulation exercise."""
        brand_id = brand_id or list(self._brands.keys())[0] if self._brands else "default"
        scenario_map = {
            "data_breach": {
                "title": "Customer Data Breach",
                "severity": CrisisSeverity.CRITICAL,
                "description": "Unauthorized access to customer database affecting 100K records",
                "trigger": "Security researcher notification",
                "channel": BrandChannel.SOCIAL_TWITTER,
            },
            "product_recall": {
                "title": "Product Safety Recall",
                "severity": CrisisSeverity.HIGH,
                "description": "Safety defect identified in flagship product line",
                "trigger": "Customer injury report",
                "channel": BrandChannel.WEBSITE,
            },
            "executive_scandal": {
                "title": "Executive Misconduct Allegation",
                "severity": CrisisSeverity.HIGH,
                "description": "Allegations of misconduct against senior executive",
                "trigger": "Media inquiry",
                "channel": BrandChannel.SOCIAL_TWITTER,
            },
            "social_media_backlash": {
                "title": "Social Media Campaign Backlash",
                "severity": CrisisSeverity.MEDIUM,
                "description": "Brand campaign accused of cultural insensitivity",
                "trigger": "Viral social media criticism",
                "channel": BrandChannel.SOCIAL_INSTAGRAM,
            },
            "supply_chain_disruption": {
                "title": "Major Supply Chain Disruption",
                "severity": CrisisSeverity.HIGH,
                "description": "Critical supplier failure impacting product availability",
                "trigger": "Supplier notification",
                "channel": BrandChannel.EMAIL,
            },
        }
        scenario = scenario_map.get(
            crisis_type,
            {
                "title": f"Simulated {crisis_type} Crisis",
                "severity": CrisisSeverity.MEDIUM,
                "description": f"Tabletop exercise simulating {crisis_type} scenario",
                "trigger": "Simulation trigger",
                "channel": BrandChannel.SOCIAL_TWITTER,
            },
        )
        crisis = CrisisEvent(
            event_id=_generate_id("sim"),
            brand_id=brand_id,
            title=scenario["title"],
            description=scenario["description"],
            severity=scenario["severity"],
            source="simulation",
            channel=scenario["channel"],
            discovered_at=datetime.now(timezone.utc),
            trigger_event=scenario["trigger"],
            affected_stakeholders=["customers", "employees", "media", "investors"],
            estimated_reach=random.randint(10000, 1000000),
            velocity=random.uniform(0.3, 0.9),
            current_sentiment=random.uniform(-0.7, -0.1),
        )
        logger.info("Running crisis simulation: %s", scenario["title"])
        return self.handle_crisis(crisis)

    def get_active_crises(self) -> List[CrisisEvent]:
        return [
            e for e in self._crisis_events.values()
            if not e.is_resolved
        ]

    def resolve_crisis(self, event_id: str, resolution_notes: str = "") -> CrisisEvent:
        if event_id not in self._crisis_events:
            raise ValueError(f"Crisis event '{event_id}' not found")
        crisis = self._crisis_events[event_id]
        crisis.resolved_at = datetime.now(timezone.utc)
        crisis.metadata["resolution_notes"] = resolution_notes
        self._log_event(
            "crisis_resolved",
            crisis.brand_id,
            {"event_id": event_id, "duration_hours": crisis.hours_since_discovery()},
        )
        return crisis

    # ------------------------------------------------------------------
    # Competitive Intelligence
    # ------------------------------------------------------------------

    def analyze_competitors(
        self,
        brand_id: str,
        competitor_ids: List[str],
    ) -> List[CompetitorAnalysis]:
        """Perform comprehensive competitive positioning analysis."""
        brand = self._get_brand(brand_id)
        analyses = []
        for comp_id in competitor_ids:
            analysis = self._analyze_single_competitor(brand, comp_id)
            analyses.append(analysis)
            self._competitor_analyses[brand_id].append(analysis)
        self._log_event(
            "competitor_analysis_completed",
            brand_id,
            {
                "competitor_count": len(competitor_ids),
                "brand_share": brand.market_share,
            },
        )
        logger.info(
            "Completed competitor analysis for %s: %d competitors",
            brand.name, len(competitor_ids),
        )
        return analyses

    def _analyze_single_competitor(
        self, brand: BrandProfile, competitor_id: str
    ) -> CompetitorAnalysis:
        tier = random.choice(list(CompetitorTier))
        comp_share = random.uniform(0.01, 0.30)
        return CompetitorAnalysis(
            analysis_id=_generate_id("comp"),
            brand_id=brand.brand_id,
            competitor_id=competitor_id,
            competitor_name=f"Competitor {competitor_id}",
            tier=tier,
            market_share=comp_share,
            brand_strength=random.uniform(40, 90),
            pricing_position=random.choice(["premium", "mid_market", "value", "penetration"]),
            target_overlap=random.uniform(0.1, 0.8),
            strengths=[
                "Strong brand recognition",
                "Innovative product pipeline",
                "Large marketing budget",
                "Established distribution network",
                "Strong digital presence",
            ][:random.randint(2, 4)],
            weaknesses=[
                "Limited product range",
                "Higher price points",
                "Weaker customer service",
                "Slow innovation cycle",
            ][:random.randint(1, 3)],
            opportunities=[
                "Expanding into adjacent markets",
                "Leveraging emerging technologies",
                "Building strategic partnerships",
            ][:random.randint(1, 3)],
            threats=[
                "Aggressive pricing strategy",
                "New product launches",
                "Market expansion",
            ][:random.randint(1, 3)],
            key_differentiators=[
                "Proprietary technology",
                "Superior customer experience",
                "Global reach",
            ][:random.randint(1, 3)],
            recent_moves=[
                {
                    "type": "product_launch",
                    "description": "New product line announced",
                    "date": (datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))).isoformat(),
                    "impact": random.choice(["low", "medium", "high"]),
                }
                for _ in range(random.randint(1, 4))
            ],
            sentiment_score=random.uniform(-0.2, 0.7),
            digital_footprint={
                "website_traffic": random.uniform(0.5, 5.0),
                "social_followers": random.randint(10000, 1000000),
                "seo_visibility": random.uniform(0.3, 0.9),
                "content_engagement": random.uniform(0.01, 0.15),
            },
            innovation_index=random.uniform(30, 90),
        )

    def competitive_positioning(self, brand_id: str) -> Dict[str, Any]:
        """Generate competitive positioning map and analysis."""
        brand = self._get_brand(brand_id)
        analyses = self._competitor_analyses.get(brand_id, [])

        positioning_map = {
            "x_axis": "Price Point (Low → High)",
            "y_axis": "Perceived Quality (Low → High)",
            "brand_position": {
                "x": random.uniform(30, 70),
                "y": random.uniform(40, 80),
            },
            "competitor_positions": [],
        }

        for analysis in analyses:
            positioning_map["competitor_positions"].append({
                "name": analysis.competitor_name,
                "x": random.uniform(10, 90),
                "y": random.uniform(10, 90),
                "market_share": analysis.market_share,
                "tier": analysis.tier.value,
            })

        whitespace_opportunities = [
            "Premium sustainable positioning",
            "Technology-forward value segment",
            "Community-driven brand experience",
            "Personalization at scale",
        ]

        return {
            "positioning_map": positioning_map,
            "whitespace_opportunities": whitespace_opportunities,
            "competitive_advantages": [
                a.key_differentiators[0] for a in analyses if a.key_differentiators
            ],
            "market_gaps": [
                f"Underserved segment: {gap}"
                for gap in ["mid_market_innovation", "sustainability_focus", "digital_native"]
            ],
            "strategic_recommendations": [
                "Leverage unique positioning in sustainability",
                "Invest in digital experience differentiation",
                "Build strategic partnerships for market expansion",
            ],
        }

    # ------------------------------------------------------------------
    # Brand Equity Measurement
    # ------------------------------------------------------------------

    def measure_brand_equity(self, brand_id: str) -> BrandEquityScore:
        """Measure brand equity using Keller's Brand Equity Model."""
        brand = self._get_brand(brand_id)
        logger.info("Measuring brand equity for %s", brand.name)

        salience = self._measure_salience(brand)
        performance = self._measure_performance(brand)
        imagery = self._measure_imagery(brand)
        judgments = self._measure_judgments(brand)
        feelings = self._measure_feelings(brand)
        resonance = self._measure_resonance(brand)

        overall_equity = _weighted_average(
            {
                "salience": salience,
                "performance": performance,
                "imagery": imagery,
                "judgments": judgments,
                "feelings": feelings,
                "resonance": resonance,
            },
            {
                "salience": 0.15,
                "performance": 0.20,
                "imagery": 0.15,
                "judgments": 0.15,
                "feelings": 0.15,
                "resonance": 0.20,
            },
        )

        historical = self._equity_history.get(brand_id, [])
        historical_trend = [(h.calculated_at, h.overall_equity) for h in historical[-12:]]
        historical_trend.append((datetime.now(timezone.utc), overall_equity))

        equity_score = BrandEquityScore(
            equity_id=_generate_id("eq"),
            brand_id=brand_id,
            overall_equity=_clamp(overall_equity),
            brand_salience=_clamp(salience),
            performance_assessment=_clamp(performance),
            imagery_assessment=_clamp(imagery),
            judgments=_clamp(judgments),
            feelings=_clamp(feelings),
            resonance=_clamp(resonance),
            dimensional_breakdown={
                "salience": {"category_need": salience * 0.5, "brand_recall": salience * 0.5},
                "performance": {
                    "quality": performance * 0.3,
                    "reliability": performance * 0.25,
                    "durability": performance * 0.2,
                    "serviceability": performance * 0.15,
                    "style": performance * 0.1,
                },
                "imagery": {
                    "user_profiles": imagery * 0.3,
                    "purchase_situations": imagery * 0.25,
                    "personality": imagery * 0.25,
                    "history": imagery * 0.2,
                },
                "judgments": {
                    "quality": judgments * 0.3,
                    "credibility": judgments * 0.25,
                    "consideration": judgments * 0.25,
                    "superiority": judgments * 0.2,
                },
                "feelings": {
                    "warmth": feelings * 0.25,
                    "fun": feelings * 0.2,
                    "excitement": feelings * 0.2,
                    "security": feelings * 0.2,
                    "social_approval": feelings * 0.15,
                },
                "resonance": {
                    "behavioral_loyalty": resonance * 0.25,
                    "attitudinal_attachment": resonance * 0.25,
                    "sense_of_community": resonance * 0.25,
                    "active_engagement": resonance * 0.25,
                },
            },
            competitive_benchmark=random.uniform(50, 80),
            historical_trend=historical_trend,
        )

        self._equity_history[brand_id].append(equity_score)
        self._log_event(
            "brand_equity_measured",
            brand_id,
            {
                "equity_id": equity_score.equity_id,
                "overall_equity": equity_score.overall_equity,
                "trend": equity_score.equity_trend(),
            },
        )
        return equity_score

    def _measure_salience(self, brand: BrandProfile) -> float:
        base = 50.0
        if brand.market_share > 0.10:
            base += 15.0
        if brand.brand_age() > 10:
            base += 10.0
        base += len(brand.primary_channels) * 2.0
        return _clamp(base + random.uniform(-5, 10))

    def _measure_performance(self, brand: BrandProfile) -> float:
        base = 55.0
        if brand.stage in (BrandStage.GROWTH, BrandStage.MATURITY):
            base += 10.0
        if brand.annual_revenue > 1e9:
            base += 8.0
        return _clamp(base + random.uniform(-8, 12))

    def _measure_imagery(self, brand: BrandProfile) -> float:
        base = 50.0
        if brand.brand_colors:
            base += 8.0
        if brand.typography:
            base += 5.0
        if brand.brand_voice_attributes:
            base += 7.0
        return _clamp(base + random.uniform(-5, 15))

    def _measure_judgments(self, brand: BrandProfile) -> float:
        base = 52.0
        if len(brand.values) >= 3:
            base += 8.0
        if brand.unique_value_proposition:
            base += 6.0
        return _clamp(base + random.uniform(-5, 12))

    def _measure_feelings(self, brand: BrandProfile) -> float:
        base = 48.0
        if brand.brand_archetype:
            base += 10.0
        if brand.mission:
            base += 5.0
        return _clamp(base + random.uniform(-5, 15))

    def _measure_resonance(self, brand: BrandProfile) -> float:
        base = 45.0
        if brand.stage in (BrandStage.MATURITY, BrandStage.GROWTH):
            base += 12.0
        if brand.market_share > 0.08:
            base += 8.0
        return _clamp(base + random.uniform(-8, 15))

    # ------------------------------------------------------------------
    # Reputation Management
    # ------------------------------------------------------------------

    def manage_reputation(
        self,
        brand_id: str,
        source: Optional[ReputationSource] = None,
    ) -> ReputationMetrics:
        """Track and analyze brand reputation across channels and sources."""
        brand = self._get_brand(brand_id)
        sources = [source] if source else list(ReputationSource)

        source_scores = {}
        for src in sources:
            source_scores[src.value] = _clamp(random.uniform(40, 85))

        overall = statistics.mean(source_scores.values()) if source_scores else 50.0

        historical = self._reputation_history.get(brand_id, [])
        if historical:
            trend = "improving" if overall > historical[-1].overall_score else "declining"
            if abs(overall - historical[-1].overall_score) < 3:
                trend = "stable"
        else:
            trend = "establishing_baseline"

        metrics = ReputationMetrics(
            metrics_id=_generate_id("rep"),
            brand_id=brand_id,
            overall_score=_clamp(overall),
            source_scores=source_scores,
            media_sentiment=source_scores.get(ReputationSource.MEDIA_COVERAGE.value, 60),
            employee_sentiment=source_scores.get(ReputationSource.EMPLOYEE_REVIEWS.value, 55),
            customer_sentiment=source_scores.get(ReputationSource.CUSTOMER_REVIEWS.value, 65),
            investor_sentiment=source_scores.get(ReputationSource.INVESTOR_FEEDBACK.value, 58),
            community_sentiment=source_scores.get(ReputationSource.SOCIAL_LISTENING.value, 62),
            thought_leadership_score=source_scores.get(ReputationSource.ANALYST_REPORTS.value, 50),
            crisis_resilience_score=_clamp(random.uniform(50, 85)),
            trust_index=_clamp(random.uniform(55, 80)),
            credibility_index=_clamp(random.uniform(50, 78)),
            visibility_index=_clamp(random.uniform(45, 82)),
            trend_direction=trend,
            period_start=datetime.now(timezone.utc) - timedelta(days=30),
            period_end=datetime.now(timezone.utc),
            data_points=random.randint(100, 5000),
            benchmarks={
                "industry_avg": 62.0,
                "top_performer": 85.0,
                "brand_previous": historical[-1].overall_score if historical else 50.0,
            },
        )

        self._reputation_history[brand_id].append(metrics)
        self._log_event(
            "reputation_assessed",
            brand_id,
            {
                "metrics_id": metrics.metrics_id,
                "overall_score": metrics.overall_score,
                "trend": trend,
            },
        )
        return metrics

    def get_reputation_history(
        self, brand_id: str, periods: int = 12
    ) -> List[Tuple[datetime, float]]:
        history = self._reputation_history.get(brand_id, [])
        return [(m.period_end, m.overall_score) for m in history[-periods:]]

    # ------------------------------------------------------------------
    # Campaign Management
    # ------------------------------------------------------------------

    def create_campaign_brief(
        self,
        brand_id: str,
        objectives: List[str],
        budget: float = 100000.0,
    ) -> CampaignPerformance:
        """Create a comprehensive campaign brief with KPIs and projections."""
        brand = self._get_brand(brand_id)
        logger.info("Creating campaign brief for %s with %d objectives", brand.name, len(objectives))

        campaign = CampaignPerformance(
            campaign_id=_generate_id("camp"),
            brand_id=brand_id,
            name=f"{brand.name} Campaign {datetime.now(timezone.utc).strftime('%Y-%m')}",
            status=CampaignStatus.PLANNING,
            start_date=datetime.now(timezone.utc) + timedelta(days=7),
            end_date=datetime.now(timezone.utc) + timedelta(days=90),
            budget=budget,
            spend=0.0,
            impressions=0,
            reach=0,
            engagement=0,
            conversions=0,
            revenue_generated=0.0,
            channel_breakdown={ch.value: {"impressions": 0, "engagement": 0} for ch in brand.primary_channels[:5]},
            audience_response={},
            kpi_targets={
                "impressions": budget * 10,
                "reach": budget * 3,
                "engagement_rate": 0.03,
                "conversion_rate": 0.02,
                "brand_lift": 0.05,
                "nps_change": 5.0,
            },
            kpi_actuals={},
            sentiment_impact=0.0,
            brand_lift=0.0,
            awareness_change=0.0,
        )

        self._campaigns[campaign.campaign_id] = campaign
        self._log_event(
            "campaign_created",
            brand_id,
            {
                "campaign_id": campaign.campaign_id,
                "name": campaign.name,
                "budget": budget,
                "objective_count": len(objectives),
            },
        )
        return campaign

    def track_campaign_performance(
        self, campaign_id: str
    ) -> Dict[str, Any]:
        """Track and report campaign performance metrics."""
        if campaign_id not in self._campaigns:
            raise ValueError(f"Campaign '{campaign_id}' not found")
        campaign = self._campaigns[campaign_id]

        if campaign.status == CampaignStatus.PLANNING:
            campaign.status = CampaignStatus.IN_PROGRESS

        campaign.impressions += random.randint(1000, 50000)
        campaign.reach += random.randint(500, 20000)
        campaign.engagement += random.randint(50, 5000)
        campaign.conversions += random.randint(5, 200)
        campaign.spend += random.uniform(500, 5000)
        campaign.revenue_generated += random.uniform(1000, 20000)

        kpi_status = {}
        for kpi, target in campaign.kpi_targets.items():
            actual = campaign.kpi_actuals.get(kpi, 0)
            kpi_status[kpi] = {
                "target": target,
                "actual": actual,
                "progress": (actual / target * 100) if target > 0 else 0,
                "status": "on_track" if actual >= target * 0.8 else "behind",
            }

        return {
            "campaign_id": campaign_id,
            "name": campaign.name,
            "status": campaign.status.value,
            "roi": campaign.roi(),
            "cost_per_impression": campaign.cost_per_impression(),
            "cost_per_conversion": campaign.cost_per_conversion(),
            "conversion_rate": campaign.conversion_rate(),
            "engagement_rate": campaign.engagement_rate(),
            "budget_utilization": campaign.budget_utilization(),
            "kpi_status": kpi_status,
            "days_remaining": campaign.days_remaining(),
        }

    def get_campaign_summary(self, brand_id: str) -> Dict[str, Any]:
        campaigns = [
            c for c in self._campaigns.values()
            if c.brand_id == brand_id
        ]
        if not campaigns:
            return {"campaign_count": 0, "total_spend": 0, "total_revenue": 0}

        return {
            "campaign_count": len(campaigns),
            "active_campaigns": sum(1 for c in campaigns if c.status.is_active),
            "total_spend": sum(c.spend for c in campaigns),
            "total_revenue": sum(c.revenue_generated for c in campaigns),
            "average_roi": statistics.mean([c.roi() for c in campaigns]) if campaigns else 0,
            "total_impressions": sum(c.impressions for c in campaigns),
            "total_conversions": sum(c.conversions for c in campaigns),
        }

    # ------------------------------------------------------------------
    # Audience Segmentation
    # ------------------------------------------------------------------

    def segment_audience(
        self, brand_id: str
    ) -> List[AudienceSegment]:
        """Perform audience segmentation analysis."""
        brand = self._get_brand(brand_id)
        segment_templates = [
            {
                "name": "Brand Loyalists",
                "description": "High-value, long-term brand advocates",
                "size_pct": 0.15,
                "sentiment": 0.8,
                "loyalty": 0.9,
                "ltv": 5000,
                "cac": 200,
                "churn": 0.1,
            },
            {
                "name": "Growth Seekers",
                "description": "Active customers exploring brand expansion",
                "size_pct": 0.25,
                "sentiment": 0.6,
                "loyalty": 0.6,
                "ltv": 2500,
                "cac": 350,
                "churn": 0.3,
            },
            {
                "name": "Value Conscious",
                "description": "Price-sensitive segment with moderate engagement",
                "size_pct": 0.30,
                "sentiment": 0.4,
                "loyalty": 0.4,
                "ltv": 1200,
                "cac": 450,
                "churn": 0.5,
            },
            {
                "name": "Digital Natives",
                "description": "Young, digitally-savvy audience segment",
                "size_pct": 0.20,
                "sentiment": 0.55,
                "loyalty": 0.35,
                "ltv": 1800,
                "cac": 280,
                "churn": 0.45,
            },
            {
                "name": "Corporate Buyers",
                "description": "B2B decision-makers and procurement teams",
                "size_pct": 0.10,
                "sentiment": 0.65,
                "loyalty": 0.7,
                "ltv": 15000,
                "cac": 2000,
                "churn": 0.2,
            },
        ]

        total_market = int(brand.market_share * 1e6)
        segments = []
        for tmpl in segment_templates:
            segment = AudienceSegment(
                segment_id=_generate_id("seg"),
                brand_id=brand_id,
                name=tmpl["name"],
                description=tmpl["description"],
                size=int(total_market * tmpl["size_pct"]),
                demographics={
                    "age_range": random.choice(["18-24", "25-34", "35-44", "45-54", "55+"]),
                    "income_level": random.choice(["low", "middle", "high", "affluent"]),
                    "education": random.choice(["high_school", "bachelors", "masters", "doctorate"]),
                    "location": random.choice(["urban", "suburban", "rural", "mixed"]),
                },
                psychographics={
                    "values": random.sample(
                        ["sustainability", "innovation", "tradition", "value", "quality", "status"],
                        k=3,
                    ),
                    "lifestyle": random.choice(["active", "balanced", "luxury", "practical"]),
                    "media_consumption": random.sample(
                        ["social_media", "traditional_news", "podcasts", "streaming", "print"],
                        k=2,
                    ),
                },
                behavioral_patterns={
                    "purchase_frequency": random.choice(["weekly", "monthly", "quarterly", "annually"]),
                    "avg_order_value": random.uniform(25, 500),
                    "channel_preference": random.choice(["online", "offline", "omnichannel"]),
                    "decision_influencer": random.choice(["peer", "expert", "reviews", "advertising"]),
                },
                preferred_channels=random.sample(list(BrandChannel), k=3),
                sentiment_toward_brand=tmpl["sentiment"],
                loyalty_score=tmpl["loyalty"],
                lifetime_value=tmpl["ltv"],
                acquisition_cost=tmpl["cac"],
                churn_risk=tmpl["churn"],
                engagement_frequency=random.uniform(1, 30),
                conversion_rate=random.uniform(0.01, 0.15),
                top_interests=random.sample(
                    ["technology", "fashion", "food", "travel", "fitness", "entertainment"],
                    k=3,
                ),
            )
            segments.append(segment)

        self._segments[brand_id] = segments
        self._log_event(
            "audience_segmented",
            brand_id,
            {
                "segment_count": len(segments),
                "total_addressable": total_market,
            },
        )
        return segments

    def get_segment_insights(
        self, brand_id: str, segment_id: str
    ) -> Dict[str, Any]:
        segments = self._segments.get(brand_id, [])
        segment = next((s for s in segments if s.segment_id == segment_id), None)
        if not segment:
            raise ValueError(f"Segment '{segment_id}' not found for brand '{brand_id}'")
        return {
            "segment": segment.name,
            "health": segment.segment_health(),
            "ltv_cac_ratio": segment.ltv_to_cac_ratio(),
            "recommendations": [
                f"Increase {ch.value} presence for this segment"
                for ch in segment.preferred_channels[:2]
            ],
            "retention_strategy": (
                "Loyalty program" if segment.loyalty_score > 0.7
                else "Re-engagement campaign"
            ),
        }

    # ------------------------------------------------------------------
    # Brand Health Report
    # ------------------------------------------------------------------

    def generate_brand_health_report(
        self, brand_id: str
    ) -> BrandHealthDashboard:
        """Generate a comprehensive brand health dashboard."""
        brand = self._get_brand(brand_id)
        logger.info("Generating brand health report for %s", brand.name)

        metric_scores = {}
        for metric in BrandHealthMetric:
            metric_scores[metric.value] = _clamp(random.uniform(40, 90))

        overall_health = statistics.mean(metric_scores.values())

        alerts = []
        for metric, score in metric_scores.items():
            if score < 40:
                alerts.append({
                    "severity": "critical",
                    "metric": metric,
                    "score": score,
                    "message": f"{metric} score critically low at {score:.1f}",
                })
            elif score < 55:
                alerts.append({
                    "severity": "warning",
                    "metric": metric,
                    "score": score,
                    "message": f"{metric} score below target at {score:.1f}",
                })

        trends = {}
        for metric in list(BrandHealthMetric)[:8]:
            trend_history = [random.uniform(40, 85) for _ in range(6)]
            trends[metric.value] = _compute_trend(trend_history)

        benchmark_gaps = {
            metric: random.uniform(-15, 15)
            for metric in list(BrandHealthMetric)[:6]
        }

        dashboard = BrandHealthDashboard(
            dashboard_id=_generate_id("dash"),
            brand_id=brand_id,
            overall_health=_clamp(overall_health),
            metric_scores=metric_scores,
            alerts=alerts,
            trends=trends,
            benchmark_gaps=benchmark_gaps,
            recommendations_count=len([a for a in alerts if a["severity"] == "critical"]),
        )

        self._log_event(
            "health_report_generated",
            brand_id,
            {
                "dashboard_id": dashboard.dashboard_id,
                "overall_health": overall_health,
                "alert_count": len(alerts),
                "status": dashboard.health_status(),
            },
        )
        return dashboard

    # ------------------------------------------------------------------
    # Brand Consistency Tracking
    # ------------------------------------------------------------------

    def track_brand_consistency(
        self, brand_id: str
    ) -> Dict[str, Any]:
        """Track and score brand consistency across all touchpoints."""
        brand = self._get_brand(brand_id)

        touchpoint_scores = {}
        touchpoints = [
            "website", "mobile_app", "social_media", "email_marketing",
            "print_collateral", "retail_experience", "packaging",
            "customer_service", "internal_communications", "advertising",
            "partner_materials", "events",
        ]
        for tp in touchpoints:
            touchpoint_scores[tp] = _clamp(random.uniform(45, 95))

        overall_consistency = statistics.mean(touchpoint_scores.values())

        compliance_issues = []
        guidelines = self._guidelines.get(brand_id, [])
        for guideline in guidelines:
            if random.random() < 0.3:
                compliance_issues.append({
                    "guideline": guideline.title,
                    "element": guideline.element.value,
                    "issue_type": random.choice([
                        "logo_usage_violation",
                        "color偏离",
                        "typography_mismatch",
                        "tone_inconsistency",
                        "unauthorized_usage",
                    ]),
                    "severity": random.choice(["low", "medium", "high"]),
                    "affected_touchpoints": random.sample(touchpoints, k=random.randint(1, 4)),
                })

        recommendations = []
        low_scoring = [tp for tp, score in touchpoint_scores.items() if score < 65]
        for tp in low_scoring:
            recommendations.append({
                "touchpoint": tp,
                "current_score": touchpoint_scores[tp],
                "action": f"Review and update brand implementation on {tp}",
                "priority": "high" if touchpoint_scores[tp] < 50 else "medium",
            })

        return {
            "overall_consistency_score": _clamp(overall_consistency),
            "touchpoint_scores": touchpoint_scores,
            "compliance_issues": compliance_issues,
            "issue_count": len(compliance_issues),
            "recommendations": sorted(recommendations, key=lambda r: r["current_score"]),
            "grade": (
                "A" if overall_consistency >= 85 else
                "B" if overall_consistency >= 70 else
                "C" if overall_consistency >= 55 else
                "D" if overall_consistency >= 40 else "F"
            ),
        }

    # ------------------------------------------------------------------
    # Brand Partnerships
    # ------------------------------------------------------------------

    def manage_brand_partnerships(
        self, brand_id: str
    ) -> Dict[str, Any]:
        """Evaluate and manage brand partnership opportunities."""
        brand = self._get_brand(brand_id)

        partnership_scorecard = {
            "current_partnerships": len(brand.partnerships),
            "partnership_health": {},
            "opportunities": [],
            "risks": [],
            "recommendations": [],
        }

        for partner in brand.partnerships:
            health = _clamp(random.uniform(40, 95))
            partnership_scorecard["partnership_health"][partner] = {
                "alignment_score": _clamp(random.uniform(50, 90)),
                "brand_value": _clamp(random.uniform(30, 85)),
                "mutual_benefit": _clamp(random.uniform(40, 88)),
                "risk_score": _clamp(random.uniform(5, 60)),
                "overall_health": health,
                "recommendation": (
                    "expand" if health > 75 else
                    "maintain" if health > 50 else
                    "review" if health > 30 else "exit"
                ),
            }

        opportunity_types = [
            {"type": "co_branding", "potential": random.uniform(60, 90), "risk": random.uniform(10, 40)},
            {"type": "distribution_partnership", "potential": random.uniform(50, 85), "risk": random.uniform(15, 50)},
            {"type": "technology_integration", "potential": random.uniform(55, 88), "risk": random.uniform(20, 55)},
            {"type": "content_collaboration", "potential": random.uniform(45, 80), "risk": random.uniform(10, 35)},
            {"type": "cause_marketing", "potential": random.uniform(40, 75), "risk": random.uniform(5, 25)},
        ]
        partnership_scorecard["opportunities"] = [
            opp for opp in opportunity_types if opp["potential"] > 60
        ]

        partnership_scorecard["risks"] = [
            {"risk": "Brand dilution through over-partnership", "probability": random.uniform(0.1, 0.4)},
            {"risk": "Partner reputation damage", "probability": random.uniform(0.05, 0.3)},
            {"risk": "Competitive partner conflict", "probability": random.uniform(0.1, 0.35)},
        ]

        partnership_scorecard["recommendations"] = [
            "Diversify partnership portfolio across industries",
            "Establish clear brand partnership guidelines",
            "Implement partnership performance tracking",
            "Regular partnership health reviews (quarterly)",
            "Develop partnership exit strategy protocols",
        ]

        return partnership_scorecard

    # ------------------------------------------------------------------
    # Stakeholder Briefing
    # ------------------------------------------------------------------

    def generate_stakeholder_brief(
        self,
        brand_id: str,
        audience: str = "executive",
    ) -> StakeholderBrief:
        """Generate an executive stakeholder briefing."""
        brand = self._get_brand(brand_id)

        health = self.generate_brand_health_report(brand_id)
        sentiment = self.monitor_sentiment(brand_id)
        equity = self.measure_brand_equity(brand_id)

        executive_summary = (
            f"{brand.name} Brand Performance Summary\n"
            f"Brand Health Index: {health.overall_health:.1f}/100 ({health.health_status()})\n"
            f"Sentiment Score: {sentiment.overall_score:.3f} ({sentiment.overall_level.label})\n"
            f"Brand Equity: {equity.overall_equity:.1f}/100 ({equity.equity_trend()})\n"
            f"Market Position: {brand.market_share:.1%} market share in {brand.industry}\n"
            f"Active Campaigns: {sum(1 for c in self._campaigns.values() if c.brand_id == brand_id and c.status.is_active)}\n"
            f"Active Crises: {sum(1 for c in self._crisis_events.values() if not c.is_resolved)}\n"
        )

        highlights = [
            f"Brand health at {health.overall_health:.1f} — {health.health_status()}",
            f"Sentiment trending {'positive' if sentiment.is_trending_positive() else 'negative'}",
            f"Equity {equity.equity_trend()} over measured period",
            f"Share of voice: {sentiment.share_of_voice:.1%}",
        ]

        concerns = [
            alert["message"]
            for alert in health.alerts
            if alert["severity"] == "critical"
        ][:5]

        actions = [
            {
                "action": "Review critical brand health alerts",
                "urgency": "high",
                "owner": "Brand Team",
            },
            {
                "action": "Monitor sentiment trends closely",
                "urgency": "medium",
                "owner": "Marketing",
            },
        ]

        return StakeholderBrief(
            brief_id=_generate_id("brief"),
            brand_id=brand_id,
            title=f"{brand.name} Executive Brand Brief — {datetime.now(timezone.utc).strftime('%B %Y')}",
            executive_summary=executive_summary,
            key_metrics={
                "brand_health": health.overall_health,
                "sentiment_score": sentiment.overall_score,
                "brand_equity": equity.overall_equity,
                "market_share": brand.market_share * 100,
                "share_of_voice": sentiment.share_of_voice * 100,
            },
            highlights=highlights,
            concerns=concerns,
            recommended_actions=actions,
            audience=audience,
            period=f"{(datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%d')} to {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        )

    # ------------------------------------------------------------------
    # Utility & Export
    # ------------------------------------------------------------------

    def export_brand_data(self, brand_id: str) -> Dict[str, Any]:
        """Export all brand management data for a brand."""
        brand = self._get_brand(brand_id)
        return {
            "brand_profile": asdict(brand),
            "guidelines_count": len(self._guidelines.get(brand_id, [])),
            "sentiment_reports": len(self._sentiment_history.get(brand_id, [])),
            "audit_results": len(self._audit_history.get(brand_id, [])),
            "competitor_analyses": len(self._competitor_analyses.get(brand_id, [])),
            "campaigns": len([
                c for c in self._campaigns.values()
                if c.brand_id == brand_id
            ]),
            "active_crises": len([
                e for e in self._crisis_events.values()
                if e.brand_id == brand_id and not e.is_resolved
            ]),
            "audience_segments": len(self._segments.get(brand_id, [])),
            "reputation_assessments": len(self._reputation_history.get(brand_id, [])),
            "equity_measurements": len(self._equity_history.get(brand_id, [])),
        }

    def get_event_log(
        self,
        brand_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        events = self._event_log
        if brand_id:
            events = [e for e in events if e["brand_id"] == brand_id]
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]
        return events[-limit:]


# ---------------------------------------------------------------------------
# __main__ Demo
# ---------------------------------------------------------------------------

def _demo():
    """Demonstrate the Brand Management Agent with a realistic scenario."""
    print("=" * 70)
    print("  Brand Management Agent v2.0 — Demo Scenario")
    print("=" * 70)

    agent = BrandManagementAgent(config={"demo_mode": True})

    # --- Register Brand ---
    nova_profile = BrandProfile(
        brand_id="nova_tech",
        name="NovaTech Solutions",
        founded_year=2018,
        industry="technology",
        stage=BrandStage.GROWTH,
        mission="Empowering businesses through intelligent automation",
        vision="A world where technology amplifies human potential",
        values=["innovation", "integrity", "customer_success", "sustainability"],
        target_audience=["enterprise", "mid_market", "tech_leaders"],
        positioning_statement="The intelligent automation platform for forward-thinking enterprises",
        unique_value_proposition="AI-powered automation that adapts to your business, not the other way around",
        brand_archetype="The Creator",
        primary_channels=[
            BrandChannel.WEBSITE,
            BrandChannel.SOCIAL_LINKEDIN,
            BrandChannel.SOCIAL_TWITTER,
            BrandChannel.EMAIL,
            BrandChannel.PODCAST,
        ],
        headquarters="San Francisco, CA",
        employee_count=450,
        annual_revenue=120_000_000.0,
        market_share=0.065,
        brand_colors={"primary": "#1A73E8", "secondary": "#34A853", "accent": "#FBBC04"},
        typography={"primary": "Inter", "secondary": "Merriweather", "mono": "JetBrains Mono"},
        logo_variants=["primary", "horizontal", "stacked", "icon_only"],
        brand_voice_attributes=["confident", "approachable", "innovative", "clear"],
        partnerships=["AWS", "Salesforce", "Microsoft"],
    )
    agent.register_brand(nova_profile)
    print(f"\n[+] Registered brand: {nova_profile.name}")

    # --- Brand Audit ---
    print("\n" + "-" * 50)
    print("  BRAND AUDIT")
    print("-" * 50)
    audit = agent.brand_audit("nova_tech", AuditScope.FULL)
    print(f"  Audit ID:     {audit.audit_id}")
    print(f"  Overall Score: {audit.overall_score:.1f}/100 (Grade: {audit.grade()})")
    print(f"  Compliance:   {audit.compliance_score:.1f}%")
    print(f"  Consistency:  {audit.consistency_score:.1f}%")
    print(f"  Equity Score: {audit.equity_score:.1f}")
    print(f"  Health Index: {audit.health_index:.1f}")
    print(f"  Strengths:    {len(audit.strengths)}")
    for s in audit.strengths[:3]:
        print(f"    • {s}")
    print(f"  Weaknesses:   {len(audit.weaknesses)}")
    for w in audit.weaknesses[:3]:
        print(f"    • {w}")
    print(f"  Recommendations: {len(audit.recommendations)}")
    for r in audit.priority_actions()[:3]:
        print(f"    [{r['priority']}] {r['dimension']}: score {r['current_score']:.1f} → target {r['target_score']:.1f}")

    # --- Brand Guidelines ---
    print("\n" + "-" * 50)
    print("  BRAND GUIDELINES")
    print("-" * 50)
    guidelines = agent.create_guidelines(
        "nova_tech",
        [BrandElement.LOGO, BrandElement.COLOR, BrandElement.TYPOGRAPHY, BrandElement.VOICE],
    )
    print(f"  Created {len(guidelines)} guideline documents")
    for g in guidelines:
        print(f"    • {g.title} (expires in {g.days_until_review()} days)")
        print(f"      Rules: {len(g.rules)}, Don'ts: {len(g.donts)}")
        print(f"      Accessibility: {g.accessibility_notes[:60]}...")

    # --- Sentiment Monitoring ---
    print("\n" + "-" * 50)
    print("  SENTIMENT MONITORING")
    print("-" * 50)
    sentiment = agent.monitor_sentiment("nova_tech")
    print(f"  Report ID:    {sentiment.report_id}")
    print(f"  Overall:      {sentiment.overall_score:.3f} ({sentiment.overall_level.label})")
    print(f"  Volume:       {sentiment.volume:,} mentions")
    print(f"  SoV:          {sentiment.share_of_voice:.1%}")
    print(f"  Confidence:   {sentiment.confidence_score:.1%}")
    print(f"  Alerts:       {sentiment.alert_count()}")
    print(f"  Trending:     {'↑ Positive' if sentiment.is_trending_positive() else '↓ Negative'}")
    print("  Channel Breakdown:")
    for ch, data in sentiment.channel_breakdown.items():
        print(f"    {ch}: sentiment={data['sentiment']:.3f}, volume={data['volume']}")

    # --- Crisis Management ---
    print("\n" + "-" * 50)
    print("  CRISIS MANAGEMENT")
    print("-" * 50)
    crisis = CrisisEvent(
        event_id="crisis_001",
        brand_id="nova_tech",
        title="Data Security Incident Report",
        description="Security researcher discovers potential vulnerability in API endpoint",
        severity=Criseseverity.HIGH,
        source="external_security_researcher",
        channel=BrandChannel.SOCIAL_TWITTER,
        discovered_at=datetime.now(timezone.utc),
        trigger_event="Security disclosure email",
        affected_stakeholders=["customers", "partners", "regulators", "media"],
        estimated_reach=250000,
        velocity=0.7,
        current_sentiment=-0.45,
    )
    response_plan = agent.handle_crisis(crisis)
    print(f"  Plan ID:      {response_plan.plan_id}")
    print(f"  Tier:         {response_plan.tier}")
    print(f"  Team Size:    {len(response_plan.response_team)}")
    print(f"  Actions:      {len(response_plan.immediate_actions)}")
    print(f"  Budget:       ${response_plan.budget_allocation:,.0f}")
    print(f"  Update Freq:  {response_plan.communication_strategy['update_frequency']}")
    print("  Response Team:")
    for member in response_plan.response_team[:5]:
        print(f"    • {member['role']}: {member['responsibility']}")

    # --- Crisis Simulation ---
    print("\n  --- Crisis Simulation ---")
    sim_plan = agent.simulate_crisis("data_breach", "nova_tech")
    print(f"  Simulation:   {sim_plan.plan_id}")
    print(f"  Tier:         {sim_plan.tier}")
    print(f"  Actions:      {len(sim_plan.immediate_actions)}")

    # --- Competitive Analysis ---
    print("\n" + "-" * 50)
    print("  COMPETITIVE INTELLIGENCE")
    print("-" * 50)
    competitors = agent.analyze_competitors(
        "nova_tech", ["comp_alpha", "comp_beta", "comp_gamma"]
    )
    for comp in competitors:
        print(f"  {comp.competitor_name} ({comp.tier.value}):")
        print(f"    Market Share: {comp.market_share:.1%}")
        print(f"    Brand Strength: {comp.brand_strength:.1f}")
        print(f"    Threat Score: {comp.threat_score():.1f}")
        print(f"    Innovation: {comp.innovation_index:.1f}")
        print(f"    Strengths: {', '.join(comp.strengths[:2])}")

    positioning = agent.competitive_positioning("nova_tech")
    print(f"\n  Whitespace Opportunities: {len(positioning['whitespace_opportunities'])}")
    for opp in positioning["whitespace_opportunities"][:3]:
        print(f"    • {opp}")

    # --- Brand Equity ---
    print("\n" + "-" * 50)
    print("  BRAND EQUITY (Keller's Model)")
    print("-" * 50)
    equity = agent.measure_brand_equity("nova_tech")
    print(f"  Equity ID:      {equity.equity_id}")
    print(f"  Overall Equity: {equity.overall_equity:.1f}/100")
    print(f"  Trend:          {equity.equity_trend()}")
    print(f"  Salience:       {equity.brand_salience:.1f}")
    print(f"  Performance:    {equity.performance_assessment:.1f}")
    print(f"  Imagery:        {equity.imagery_assessment:.1f}")
    print(f"  Judgments:      {equity.judgments:.1f}")
    print(f"  Feelings:       {equity.feelings:.1f}")
    print(f"  Resonance:      {equity.resonance:.1f}")
    print(f"  Pyramid Complete: {equity.pyramid_completeness():.1f}%")

    # --- Reputation ---
    print("\n" + "-" * 50)
    print("  REPUTATION MANAGEMENT")
    print("-" * 50)
    reputation = agent.manage_reputation("nova_tech")
    print(f"  Metrics ID:     {reputation.metrics_id}")
    print(f"  Overall Score:  {reputation.overall_score:.1f}/100")
    print(f"  Trend:          {reputation.trend_direction}")
    print(f"  Trust Index:    {reputation.trust_index:.1f}")
    print(f"  Credibility:    {reputation.credibility_index:.1f}")
    print(f"  Visibility:     {reputation.visibility_index:.1f}")
    print(f"  Crisis Resilience: {reputation.crisis_resilience_score:.1f}")

    # --- Campaigns ---
    print("\n" + "-" * 50)
    print("  CAMPAIGN MANAGEMENT")
    print("-" * 50)
    campaign = agent.create_campaign_brief(
        "nova_tech",
        ["Increase brand awareness by 25%", "Generate 5000 MQLs", "Improve NPS by 10 points"],
        budget=250000.0,
    )
    print(f"  Campaign:   {campaign.name}")
    print(f"  ID:         {campaign.campaign_id}")
    print(f"  Budget:     ${campaign.budget:,.0f}")
    print(f"  KPIs:       {len(campaign.kpi_targets)}")

    perf = agent.track_campaign_performance(campaign.campaign_id)
    print(f"\n  Performance Update:")
    print(f"    ROI:          {perf['roi']:.1f}%")
    print(f"    Conv. Rate:   {perf['conversion_rate']:.2f}%")
    print(f"    Eng. Rate:    {perf['engagement_rate']:.2f}%")
    print(f"    Budget Used:  {perf['budget_utilization']:.1f}%")

    # --- Audience Segmentation ---
    print("\n" + "-" * 50)
    print("  AUDIENCE SEGMENTATION")
    print("-" * 50)
    segments = agent.segment_audience("nova_tech")
    for seg in segments:
        print(f"  {seg.name}:")
        print(f"    Size: {seg.size:,} | LTV: ${seg.lifetime_value:,.0f}")
        print(f"    Sentiment: {seg.sentiment_toward_brand:.2f} | Loyalty: {seg.loyalty_score:.2f}")
        print(f"    Health: {seg.segment_health()} | LTV/CAC: {seg.ltv_to_cac_ratio():.1f}x")

    # --- Brand Health Dashboard ---
    print("\n" + "-" * 50)
    print("  BRAND HEALTH DASHBOARD")
    print("-" * 50)
    dashboard = agent.generate_brand_health_report("nova_tech")
    print(f"  Dashboard ID:   {dashboard.dashboard_id}")
    print(f"  Overall Health: {dashboard.overall_health:.1f}/100 ({dashboard.health_status()})")
    print(f"  Alerts:         {len(dashboard.alerts)}")
    critical = dashboard.critical_alerts()
    if critical:
        print(f"  Critical:       {len(critical)}")
        for alert in critical[:3]:
            print(f"    ⚠ {alert['message']}")
    trend_summary = dashboard.trend_summary()
    print(f"  Trends:         {dict(trend_summary)}")

    # --- Consistency ---
    print("\n" + "-" * 50)
    print("  BRAND CONSISTENCY")
    print("-" * 50)
    consistency = agent.track_brand_consistency("nova_tech")
    print(f"  Overall Score: {consistency['overall_consistency_score']:.1f} (Grade: {consistency['grade']})")
    print(f"  Issues Found:  {consistency['issue_count']}")
    print(f"  Recommendations: {len(consistency['recommendations'])}")

    # --- Partnerships ---
    print("\n" + "-" * 50)
    print("  PARTNERSHIP MANAGEMENT")
    print("-" * 50)
    partnerships = agent.manage_brand_partnerships("nova_tech")
    print(f"  Current Partners: {partnership_scorecard['current_partnerships']}")
    for partner, health in partnerships["partnership_health"].items():
        print(f"    {partner}: {health['overall_health']:.1f} ({health['recommendation']})")
    print(f"  Opportunities: {len(partnerships['opportunities'])}")
    print(f"  Risks: {len(partnerships['risks'])}")

    # --- Stakeholder Brief ---
    print("\n" + "-" * 50)
    print("  STAKEHOLDER BRIEFING")
    print("-" * 50)
    brief = agent.generate_stakeholder_brief("nova_tech", "executive")
    print(f"  Brief:    {brief.title}")
    print(f"  ID:       {brief.brief_id}")
    print(f"  Metrics:  {len(brief.key_metrics)} KPIs")
    for k, v in brief.key_metrics.items():
        print(f"    {k}: {v:.1f}")
    print(f"  Highlights: {len(brief.highlights)}")
    for h in brief.highlights[:3]:
        print(f"    + {h}")
    print(f"  Concerns: {len(brief.concerns)}")

    # --- Export ---
    print("\n" + "-" * 50)
    print("  DATA EXPORT")
    print("-" * 50)
    export = agent.export_brand_data("nova_tech")
    print(f"  Brand: {export['brand_profile']['name']}")
    for key, val in export.items():
        if key != "brand_profile":
            print(f"    {key}: {val}")

    print("\n" + "=" * 70)
    print("  Demo complete — all systems operational")
    print("=" * 70)


if __name__ == "__main__":
    _demo()
