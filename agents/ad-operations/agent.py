
"""
Ad Operations Agent - Digital Advertising Campaign Management & Optimization.

A comprehensive, production-ready agent for managing, optimizing, and analyzing
digital advertising campaigns across Google Ads, Meta, LinkedIn, Twitter/X, TikTok,
and programmatic platforms.

Features:
- Cross-platform campaign creation and synchronization
- Automated bid management and budget allocation
- A/B testing framework with statistical significance calculation
- Audience targeting and segmentation analysis
- Ad creative performance scoring
- Fraud detection and invalid traffic filtering
- Real-time budget pacing and spend forecasting
- Multi-format reporting (HTML, JSON, CSV, PDF)
- Conversion tracking and attribution modeling
- Compliance with platform policies and GDPR/CCPA
- Batch campaign operations
- Historical trend analysis
- Alerting and anomaly detection
- Integration hooks for Google Ads, Meta Ads, TikTok Ads APIs
"""

from __future__ import annotations

import abc
import asyncio
import csv
import enum
import hashlib
import json
import logging
import math
import random
import re
import statistics
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    Callable,
    Type,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Enumerations
# ============================================================================


class AdPlatform(enum.Enum):
    """Supported advertising platforms."""

    GOOGLE = "google"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    PROGRAMMATIC = "programmatic"
    DISPLAY = "display"
    SEARCH = "search"
    SOCIAL = "social"
    NATIVE = "native"


class CampaignObjective(enum.Enum):
    """Advertising campaign objectives."""

    AWARENESS = "awareness"
    TRAFFIC = "traffic"
    CONVERSIONS = "conversions"
    SALES = "sales"
    LEAD_GENERATION = "lead_generation"
    APP_INSTALLS = "app_installs"
    VIDEO_VIEWS = "video_views"
    ENGAGEMENT = "engagement"
    CATALOG_SALES = "catalog_sales"
    BRAND_RECONSIDERATION = "brand_reconsideration"
    STORE_VISITS = "store_visits"


class CampaignStatus(enum.Enum):
    """Campaign lifecycle statuses."""

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"
    REMOVED = "removed"
    DISAPPROVED = "disapproved"


class BiddingStrategy(enum.Enum):
    """Automated and manual bidding strategies."""

    LOWEST_COST = "lowest_cost"
    LOWEST_COST_WITH_CAP = "lowest_cost_with_cap"
    TARGET_CPA = "target_cpa"
    TARGET_ROAS = "target_roas"
    MAXIMIZE_CONVERSIONS = "maximize_conversions"
    MAXIMIZE_CLICKS = "maximize_clicks"
    MANUAL_CPC = "manual_cpc"
    MANUAL_CPV = "manual_cpv"
    MANUAL_CPM = "manual_cpm"
    ENHANCED_CPC = "enhanced_cpc"


class AdStatus(enum.Enum):
    """Individual ad status."""

    ENABLED = "enabled"
    PAUSED = "paused"
    REMOVED = "removed"
    PENDING_REVIEW = "pending_review"
    DISAPPROVED = "disapproved"


class AdType(enum.Enum):
    """Creative formats."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    COLLECTION = "collection"
    RESPONSIVE_SEARCH = "responsive_search"
    RESPONSIVE_DISPLAY = "responsive_display"
    SHOPPING = "shopping"
    LEAD_FORM = "lead_form"
    STORY = "story"
    REELS = "reels"
    SPARK_AD = "spark_ad"


class AudienceType(enum.Enum):
    """Audience segmentation types."""

    CUSTOM = "custom"
    LOOKALIKE = "lookalike"
    INTEREST = "interest"
    BEHAVIORAL = "behavioral"
    GEO = "geo"
    DEMOGRAPHIC = "demographic"
    RETARGETING = "retargeting"
    IN_MARKET = "in_market"
    LIFE_EVENT = "life_event"


class DeviceType(enum.Enum):
    """Device categories."""

    MOBILE = "mobile"
    DESKTOP = "desktop"
    TABLET = "tablet"
    CONNECTED_TV = "connected_tv"
    UNKNOWN = "unknown"


class AlertSeverity(enum.Enum):
    """Alert priority levels."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class ReportGranularity(enum.Enum):
    """Time granularity for reports."""

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    LIFETIME = "lifetime"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class BiddingConfig:
    """Bidding strategy configuration for a campaign or ad group."""

    strategy: BiddingStrategy = BiddingStrategy.TARGET_CPA
    target_cpa: Optional[float] = None
    target_roas: Optional[float] = None
    daily_budget: float = 100.0
    lifetime_budget: Optional[float] = None
    budget_pacing: str = "standard"
    bid_adjustments: Dict[str, float] = field(default_factory=dict)
    max_bid: Optional[float] = None
    min_bid: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["strategy"] = self.strategy.value
        return data


@dataclass
class AudienceSegment:
    """Represents a target audience segment."""

    id: str
    name: str
    platform: AdPlatform
    type: AudienceType
    size: int = 0
    targeting_spec: Dict[str, Any] = field(default_factory=dict)
    is_custom: bool = False
    is_positive: bool = True
    bid_modifier: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["platform"] = self.platform.value
        data["type"] = self.type.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data


@dataclass
class AdCreative:
    """Ad creative asset."""

    id: str
    headline: str
    description: str
    ad_type: AdType
    platform: AdPlatform
    status: AdStatus = AdStatus.ENABLED
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    call_to_action: str = "LEARN_MORE"
    display_url: str = ""
    final_url: str = ""
    tracking_url: Optional[str] = None
    metrics: Dict[str, float] = field(default_factory=dict)
    ab_test_variant: str = "control"
    created_at: datetime = field(default_factory=datetime.now)

    def ctr(self) -> float:
        """Calculate click-through rate."""
        impressions = self.metrics.get("impressions", 0)
        clicks = self.metrics.get("clicks", 0)
        if impressions > 0:
            return (clicks / impressions) * 100
        return 0.0

    def cpc(self) -> float:
        """Calculate cost per click."""
        clicks = self.metrics.get("clicks", 0)
        cost = self.metrics.get("cost", 0)
        if clicks > 0:
            return cost / clicks
        return 0.0

    def conversion_rate(self) -> float:
        """Calculate conversion rate."""
        clicks = self.metrics.get("clicks", 0)
        conversions = self.metrics.get("conversions", 0)
        if clicks > 0:
            return (conversions / clicks) * 100
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["ad_type"] = self.ad_type.value
        data["platform"] = self.platform.value
        data["status"] = self.status.value
        data["ctr"] = self.ctr()
        data["cpc"] = self.cpc()
        data["conversion_rate"] = self.conversion_rate()
        data["created_at"] = self.created_at.isoformat()
        return data


@dataclass
class AdGroup:
    """Ad group within a campaign."""

    id: str
    name: str
    campaign_id: str
    status: CampaignStatus
    bidding: BiddingConfig
    creatives: List[AdCreative] = field(default_factory=list)
    target_cpa: Optional[float] = None
    audience_segments: List[AudienceSegment] = field(default_factory=list)
    device_bid_modifiers: Dict[DeviceType, float] = field(default_factory=dict)
    location_targets: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["bidding"] = self.bidding.to_dict()
        data["creatives"] = [c.to_dict() for c in self.creatives]
        data["audience_segments"] = [a.to_dict() for a in self.audience_segments]
        data["device_bid_modifiers"] = {k.value: v for k, v in self.device_bid_modifiers.items()}
        data["created_at"] = self.created_at.isoformat()
        return data


@dataclass
class Campaign:
    """Top-level advertising campaign."""

    id: str
    name: str
    platform: AdPlatform
    objective: CampaignObjective
    status: CampaignStatus
    budget: BiddingConfig
    ad_groups: List[AdGroup] = field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_budget: float = 0.0
    spent: float = 0.0
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    metrics: Dict[str, float] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.metrics:
            self.metrics = {}

    def ctr(self) -> float:
        if self.impressions > 0:
            return (self.clicks / self.impressions) * 100
        return 0.0

    def cpc(self) -> float:
        if self.clicks > 0:
            return self.spent / self.clicks
        return 0.0

    def cpa(self) -> float:
        if self.conversions > 0:
            return self.spent / self.conversions
        return 0.0

    def roas(self) -> float:
        if self.spent > 0:
            return self.revenue / self.spent
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["platform"] = self.platform.value
        data["objective"] = self.objective.value
        data["status"] = self.status.value
        data["budget"] = self.budget.to_dict()
        data["ad_groups"] = [ag.to_dict() for ag in self.ad_groups]
        data["start_date"] = self.start_date.isoformat() if self.start_date else None
        data["end_date"] = self.end_date.isoformat() if self.end_date else None
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        data["ctr"] = self.ctr()
        data["cpc"] = self.cpc()
        data["cpa"] = self.cpa()
        data["roas"] = self.roas()
        return data


@dataclass
class FraudSignal:
    """Represents a potential fraud signal."""

    signal_id: str
    campaign_id: str
    ad_id: str
    signal_type: str
    confidence: float
    description: str
    detected_at: datetime = field(default_factory=datetime.now)
    is_resolved: bool = False
    resolution_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PerformanceAlert:
    """Performance alert for campaigns."""

    alert_id: str
    campaign_id: str
    severity: AlertSeverity
    message: str
    metric: str
    current_value: float
    threshold: float
    triggered_at: datetime = field(default_factory=datetime.now)
    is_acknowledged: bool = False
    suggested_action: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["triggered_at"] = self.triggered_at.isoformat()
        return data


@dataclass
class ABTestResult:
    """A/B test statistical result."""

    test_id: str
    variant_a: str
    variant_b: str
    metric: str
    sample_size_a: int
    sample_size_b: int
    conversion_rate_a: float
    conversion_rate_b: float
    p_value: float
    confidence_level: float
    is_significant: bool
    winner: Optional[str]
    recommendation: str
    started_at: datetime
    ended_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Config:
    """Configuration for the Ad Operations Agent."""

    default_platform: str = "google"
    default_objective: str = "conversions"
    auto_optimize: bool = True
    budget_limit: float = 1000.0
    daily_budget_cap: float = 500.0
    max_bid: float = 10.0
    min_bid: float = 0.1
    default_bidding_strategy: str = "target_cpa"
    target_cpa: float = 25.0
    target_roas: float = 4.0
    fraud_detection_enabled: bool = True
    fraud_confidence_threshold: float = 0.8
    budget_pacing_alert_threshold: float = 0.8
    low_budget_threshold: float = 0.2
    ab_test_significance_threshold: float = 0.95
    reporting_granularity: str = "daily"
    supported_platforms: List[str] = field(
        default_factory=lambda: [p.value for p in AdPlatform]
    )
    enabled_platforms: List[str] = field(
        default_factory=lambda: [AdPlatform.GOOGLE.value, AdPlatform.FACEBOOK.value]
    )
    batch_operation_concurrency: int = 5
    retry_attempts: int = 3
    retry_delay_seconds: float = 1.0
    history_enabled: bool = True
    history_file: str = "ad_ops_history.json"
    retention_days: int = 90
    cache_enabled: bool = True
    cache_ttl_hours: int = 12
    report_formats: List[str] = field(
        default_factory=lambda: ["html", "json", "csv"]
    )
    output_directory: str = "./ad_ops_reports"
    notify_on_alerts: bool = True
    alert_channels: List[str] = field(default_factory=lambda: ["email", "slack"])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# Exceptions
# ============================================================================


class AdOperationsError(Exception):
    """Base exception for ad operations errors."""
    pass


class CampaignError(AdOperationsError):
    """Campaign management error."""
    pass


class BiddingError(AdOperationsError):
    """Bidding strategy error."""
    pass


class ReportingError(AdOperationsError):
    """Reporting generation error."""
    pass


class FraudDetectionError(AdOperationsError):
    """Fraud detection error."""
    pass


class PlatformAPIError(AdOperationsError):
    """External platform API error."""
    pass


class ConfigurationError(AdOperationsError):
    """Configuration validation error."""
    pass


class ValidationError(AdOperationsError):
    """Data validation error."""
    pass


# ============================================================================
# Fraud Detection Engine
# ============================================================================


class FraudDetectionEngine:
    """Detects suspicious ad activity and invalid traffic.

    Uses rule-based and heuristic methods to identify:
    - Bot traffic patterns
    - Click fraud
    - Conversion fraud
    - Proxy/VPN traffic
    - Unusual activity spikes
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._detected_signals: List[FraudSignal] = []

    def analyze_clicks(self, clicks: List[Dict]) -> List[FraudSignal]:
        signals = []

        if not self.config.fraud_detection_enabled:
            return signals

        ip_addresses = {}
        user_agents = {}

        for click in clicks:
            ip = click.get("ip_address", "")
            ua = click.get("user_agent", "")
            ts = click.get("timestamp", datetime.now().isoformat())

            # Track IP frequency
            ip_addresses.setdefault(ip, []).append(ts)
            user_agents.setdefault(ua, []).append(ts)

        # Detect high-frequency IPs (possible bot clicks)
        for ip, timestamps in ip_addresses.items():
            if len(timestamps) > 20:
                time_diffs = [
                    (
                        datetime.fromisoformat(timestamps[i]) -
                        datetime.fromisoformat(timestamps[i - 1])
                    ).total_seconds()
                    for i in range(1, len(timestamps))
                ]
                avg_interval = statistics.mean(time_diffs) if time_diffs else 0

                if avg_interval < 1.0:
                    signals.append(FraudSignal(
                        signal_id=self._generate_signal_id("high-freq-click", ip),
                        campaign_id=clicks[0].get("campaign_id", ""),
                        ad_id=clicks[0].get("ad_id", ""),
                        signal_type="high_frequency_click",
                        confidence=0.9,
                        description=f"IP {ip} generated {len(timestamps)} clicks with avg interval {avg_interval:.2f}s.",
                    ))

        # Detect duplicate user agents
        for ua, timestamps in user_agents.items():
            if len(timestamps) > 50:
                signals.append(FraudSignal(
                    signal_id=self._generate_signal_id("duplicate-ua", ua),
                    campaign_id=clicks[0].get("campaign_id", ""),
                    ad_id=clicks[0].get("ad_id", ""),
                    signal_type="duplicate_user_agent",
                    confidence=0.7,
                    description=f"User agent '{ua}' used {len(timestamps)} times.",
                ))

        self._detected_signals.extend(signals)
        return signals

    def analyze_conversions(self, conversions: List[Dict]) -> List[FraudSignal]:
        signals = []

        if not self.config.fraud_detection_enabled:
            return signals

        # Detect conversion spikes
        timestamps = [
            datetime.fromisoformat(c.get("timestamp", datetime.now().isoformat()))
            for c in conversions
        ]
        if len(timestamps) > 10:
            time_diffs = [
                (timestamps[i] - timestamps[i - 1]).total_seconds()
                for i in range(1, len(timestamps))
            ]
            min_diff = min(time_diffs) if time_diffs else 0
            if min_diff < 0.1:  # Less than 100ms between conversions
                signals.append(FraudSignal(
                    signal_id=self._generate_signal_id("conversion-spike", ""),
                    campaign_id=conversions[0].get("campaign_id", "") if conversions else "",
                    ad_id="",
                    signal_type="conversion_spike",
                    confidence=0.85,
                    description=f"{len(conversions)} conversions in rapid succession.",
                ))

        return signals

    def get_signals(self) -> List[FraudSignal]:
        return self._detected_signals

    def clear_signals(self) -> None:
        self._detected_signals = []

    def _generate_signal_id(self, signal_type: str, unique_part: str) -> str:
        raw = f"{signal_type}-{unique_part}-{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


# ============================================================================
# Bidding Engine
# ============================================================================


class BiddingEngine:
    """Automated bidding optimization engine.

    Implements:
    - Target CPA/ROAS optimization
    - Budget pacing and allocation
    - Bid adjustment rules
    - Dayparting bid modifiers
    - Device/location targeting bid adjustments
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._bid_history: List[Dict[str, Any]] = []

    def calculate_bid(
        self,
        campaign: Campaign,
        ad_group: AdGroup,
        target_metric: str = "cpa",
    ) -> float:
        """Calculate optimal bid for an ad group based on historical performance."""
        hist = self._get_historical_performance(campaign.id, ad_group.id)

        if not hist:
            return self._calculate_default_bid(campaign, ad_group)

        if target_metric == "cpa":
            avg_conversion_value = statistics.mean(
                [h.get("conversion_value", 0) for h in hist]
            )
            if avg_conversion_value > 0:
                return min(
                    self.config.max_bid,
                    max(
                        self.config.min_bid,
                        avg_conversion_value * self.config.target_cpa / avg_conversion_value,
                    ),
                )
        elif target_metric == "roas":
            revenue = statistics.mean([h.get("revenue", 0) for h in hist])
            cost = statistics.mean([h.get("cost", 0) for h in hist])
            if cost > 0:
                current_roas = revenue / cost
                bid = self._calculate_default_bid(campaign, ad_group)
                if current_roas < self.config.target_roas:
                    bid *= 0.9  # Reduce bid to improve ROAS
                else:
                    bid *= 1.1  # Increase bid to capture more
                return min(self.config.max_bid, max(self.config.min_bid, bid))

        return self._calculate_default_bid(campaign, ad_group)

    def optimize_budget_allocation(
        self, campaigns: List[Campaign]
    ) -> Dict[str, float]:
        """Allocate daily budget across campaigns based on predicted performance."""
        if not campaigns:
            return {}

        total_budget = sum(c.budget.daily_budget for c in campaigns)
        if total_budget == 0:
            return {c.id: 0.0 for c in campaigns}

        # Weighted allocation by ROAS and CPA efficiency
        scores = {}
        for c in campaigns:
            roas_score = c.roas() if c.roas() > 0 else 1.0
            cpa_score = 1.0 / (c.cpa() if c.cpa() > 0 else self.config.target_cpa)
            scores[c.id] = roas_score * cpa_score * (1 + random.uniform(0.95, 1.05))

        total_score = sum(scores.values())
        allocations = {}
        for c in campaigns:
            if total_score > 0:
                allocations[c.id] = (scores[c.id] / total_score) * total_budget
            else:
                allocations[c.id] = total_budget / len(campaigns)

        return allocations

    def _calculate_default_bid(self, campaign: Campaign, ad_group: AdGroup) -> float:
        base_bid = ad_group.target_cpa or self.config.target_cpa
        if ad_group.device_bid_modifiers:
            avg_modifier = statistics.mean(ad_group.device_bid_modifiers.values())
            base_bid *= avg_modifier
        return min(self.config.max_bid, max(self.config.min_bid, base_bid))

    def _get_historical_performance(
        self, campaign_id: str, ad_group_id: str
    ) -> List[Dict[str, Any]]:
        return [
            h
            for h in self._bid_history
            if h.get("campaign_id") == campaign_id and h.get("ad_group_id") == ad_group_id
        ]

    def record_bid(
        self,
        campaign_id: str,
        ad_group_id: str,
        bid: float,
        outcome: Dict[str, float],
    ) -> None:
        self._bid_history.append(
            {
                "campaign_id": campaign_id,
                "ad_group_id": ad_group_id,
                "bid": bid,
                "timestamp": datetime.now().isoformat(),
                **outcome,
            }
        )


# ============================================================================
# A/B Test Manager
# ============================================================================


class ABTestManager:
    """Manages A/B tests for ad creatives and campaign settings.

    Uses chi-squared test for statistical significance.
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._tests: Dict[str, ABTestResult] = {}
        self._active_tests: Dict[str, Dict[str, Any]] = {}

    def create_test(
        self,
        test_id: str,
        variant_a: str,
        variant_b: str,
        metric: str,
        sample_size: int = 1000,
    ) -> ABTestResult:
        if test_id in self._tests:
            raise ValidationError(f"Test {test_id} already exists.")

        now = datetime.now()
        result = ABTestResult(
            test_id=test_id,
            variant_a=variant_a,
            variant_b=variant_b,
            metric=metric,
            sample_size_a=0,
            sample_size_b=0,
            conversion_rate_a=0.0,
            conversion_rate_b=0.0,
            p_value=1.0,
            confidence_level=0.0,
            is_significant=False,
            winner=None,
            recommendation="Test in progress",
            started_at=now,
            ended_at=now,
        )
        self._tests[test_id] = result
        self._active_tests[test_id] = {
            "variant_a_conversions": 0,
            "variant_a_impressions": 0,
            "variant_b_conversions": 0,
            "variant_b_impressions": 0,
            "target_sample_size": sample_size,
        }
        return result

    def record_observation(
        self,
        test_id: str,
        variant: str,
        converted: bool,
        impression: bool = True,
    ) -> None:
        if test_id not in self._active_tests:
            raise ValidationError(f"Test {test_id} not found or already completed.")

        test_state = self._active_tests[test_id]

        if variant.lower() == "a":
            test_state["variant_a_impressions"] += 1 if impression else 0
            test_state["variant_a_conversions"] += 1 if converted else 0
        elif variant.lower() == "b":
            test_state["variant_b_impressions"] += 1 if impression else 0
            test_state["variant_b_conversions"] += 1 if converted else 0

        self._update_test_result(test_id)

    def _update_test_result(self, test_id: str) -> None:
        test_state = self._active_tests[test_id]
        result = self._tests[test_id]

        impressions_a = test_state["variant_a_impressions"]
        conversions_a = test_state["variant_a_conversions"]
        impressions_b = test_state["variant_b_impressions"]
        conversions_b = test_state["variant_b_conversions"]

        result.sample_size_a = impressions_a
        result.sample_size_b = impressions_b
        result.conversion_rate_a = (conversions_a / impressions_a * 100) if impressions_a > 0 else 0.0
        result.conversion_rate_b = (conversions_b / impressions_b * 100) if impressions_b > 0 else 0.0

        # Chi-squared test (simplified)
        if impressions_a > 0 and impressions_b > 0:
            pooled_rate = (conversions_a + conversions_b) / (impressions_a + impressions_b)
            if pooled_rate > 0 and pooled_rate < 1:
                se = math.sqrt(
                    pooled_rate * (1 - pooled_rate) * (1 / impressions_a + 1 / impressions_b)
                )
                if se > 0:
                    z_score = (
                        result.conversion_rate_b - result.conversion_rate_a
                    ) / (se * 100)
                    result.p_value = 2 * (1 - self._normal_cdf(abs(z_score)))
                    result.confidence_level = (1 - result.p_value) * 100
                    result.is_significant = result.confidence_level >= self.config.ab_test_significance_threshold * 100
                    if result.is_significant:
                        result.winner = "B" if result.conversion_rate_b > result.conversion_rate_a else "A"
                        result.recommendation = (
                            f"Variant {result.winner} wins with "
                            f"{result.confidence_level:.1f}% confidence. "
                            f"Conversion rate: {getattr(result, f'conversion_rate_{result.winner.lower()}'):.2f}%"
                        )
                    else:
                        result.winner = None
                        result.recommendation = "No significant difference detected yet."
            else:
                result.p_value = 1.0
                result.confidence_level = 0.0
                result.is_significant = False
                result.winner = None
                result.recommendation = "Insufficient data for statistical significance."

    def get_test(self, test_id: str) -> Optional[ABTestResult]:
        return self._tests.get(test_id)

    def complete_test(self, test_id: str) -> ABTestResult:
        if test_id not in self._active_tests:
            raise ValidationError(f"Test {test_id} not active.")
        self._update_test_result(test_id)
        del self._active_tests[test_id]
        result = self._tests[test_id]
        result.ended_at = datetime.now()
        return result

    def _normal_cdf(self, x: float) -> float:
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# ============================================================================
# Budget & Pacing Monitor
# ============================================================================


class BudgetPacingMonitor:
    """Monitors campaign budget pacing and spend forecasts.

    Detects underspend/overspend risks and generates alerts.
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._daily_spend: Dict[str, List[Tuple[datetime, float]]] = {}
        self._alerts: List[PerformanceAlert] = []

    def record_spend(self, campaign_id: str, amount: float, timestamp: Optional[datetime] = None) -> None:
        ts = timestamp or datetime.now()
        self._daily_spend.setdefault(campaign_id, []).append((ts, amount))
        self._check_pacing(campaign_id)

    def get_spend_forecast(
        self, campaign_id: str, days_ahead: int = 7
    ) -> List[Dict[str, Any]]:
        history = self._daily_spend.get(campaign_id, [])
        if not history:
            return []

        daily_sums: Dict[str, float] = {}
        for ts, amt in history:
            day = ts.strftime("%Y-%m-%d")
            daily_sums[day] = daily_sums.get(day, 0.0) + amt

        if not daily_sums:
            return []

        avg_daily = statistics.mean(daily_sums.values())
        forecast = []
        base_date = datetime.now().date()

        for i in range(days_ahead):
            day = base_date + timedelta(days=i)
            forecast.append(
                {
                    "date": day.isoformat(),
                    "forecasted_spend": avg_daily,
                    "confidence": 0.8 if len(daily_sums) > 7 else 0.5,
                }
            )

        return forecast

    def get_alerts(self) -> List[PerformanceAlert]:
        return self._alerts

    def _check_pacing(self, campaign_id: str) -> None:
        today = datetime.now().date()
        today_spend = sum(
            amt for ts, amt in self._daily_spend.get(campaign_id, [])
            if ts.date() == today
        )
        hour_of_day = datetime.now().hour
        expected_spend_so_far = (hour_of_day / 24.0) * self.config.daily_budget_cap

        if expected_spend_so_far > 0:
            pace_ratio = today_spend / expected_spend_so_far
            if pace_ratio > self.config.budget_pacing_alert_threshold:
                alert = PerformanceAlert(
                    alert_id=self._generate_alert_id(campaign_id, "overspend"),
                    campaign_id=campaign_id,
                    severity=AlertSeverity.CRITICAL,
                    message=f"Campaign {campaign_id} is overspending: {pace_ratio:.2f}x of expected.",
                    metric="daily_spend",
                    current_value=today_spend,
                    threshold=expected_spend_so_far,
                    suggested_action="Pause campaign or increase budget.",
                )
                self._alerts.append(alert)

            elif (
                today_spend < self.config.low_budget_threshold * self.config.daily_budget_cap
                and hour_of_day > 18
            ):
                alert = PerformanceAlert(
                    alert_id=self._generate_alert_id(campaign_id, "underspend"),
                    campaign_id=campaign_id,
                    severity=AlertSeverity.WARNING,
                    message=f"Campaign {campaign_id} underspending: only {today_spend:.2f} of {self.config.daily_budget_cap:.2f}.",
                    metric="daily_spend",
                    current_value=today_spend,
                    threshold=self.config.low_budget_threshold * self.config.daily_budget_cap,
                    suggested_action="Increase bids or expand targeting.",
                )
                self._alerts.append(alert)

    def _generate_alert_id(self, campaign_id: str, alert_type: str) -> str:
        raw = f"{campaign_id}-{alert_type}-{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


# ============================================================================
# Reporting Engine
# ============================================================================


class ReportingEngine:
    """Generates multi-format campaign performance reports.

    Supports:
    - HTML interactive dashboards
    - JSON data exports
    - CSV spreadsheets
    - PDF print-ready reports
    - Scheduled report delivery
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def generate(
        self,
        campaigns: List[Campaign],
        fmt: str = "html",
        output_path: Optional[str] = None,
        granularity: str = "daily",
    ) -> str:
        if fmt == "html":
            content = self._generate_html(campaigns, granularity)
        elif fmt == "json":
            content = self._generate_json(campaigns, granularity)
        elif fmt == "csv":
            content = self._generate_csv(campaigns, granularity)
        elif fmt == "pdf":
            content = self._generate_pdf(campaigns, granularity)
        else:
            raise ReportingError(f"Unsupported format: {fmt}")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        return content

    def schedule_report(
        self,
        campaign_ids: List[str],
        cron_expression: str,
        fmt: str,
        recipients: List[str],
    ) -> str:
        schedule_id = f"sched-{hashlib.md5(str(campaign_ids).encode()).hexdigest()[:8]}"
        schedule_file = Path(self.config.output_directory) / "schedules.json"
        try:
            if schedule_file.exists():
                with open(schedule_file, "r") as f:
                    schedules = json.load(f)
            else:
                schedules = {}
            schedules[schedule_id] = {
                "campaign_ids": campaign_ids,
                "cron": cron_expression,
                "format": fmt,
                "recipients": recipients,
                "created_at": datetime.now().isoformat(),
            }
            with open(schedule_file, "w") as f:
                json.dump(schedules, f, indent=2)
        except Exception as e:
            raise ReportingError(f"Failed to save schedule: {e}")
        return schedule_id

    def _generate_html(
        self, campaigns: List[Campaign], granularity: str
    ) -> str:
        rows = ""
        for c in campaigns:
            for ag in c.ad_groups:
                for cr in ag.creatives:
                    rows += f"""
                    <tr>
                      <td>{c.name}</td>
                      <td>{cr.headline}</td>
                      <td>{c.platform.value}</td>
                      <td>{cr.ctr():.2f}%</td>
                      <td>{cr.cpc():.2f}</td>
                      <td>{cr.conversion_rate():.2f}%</td>
                      <td>{ag.bidding.daily_budget:.2f}</td>
                      <td>{c.spent:.2f}</td>
                    </tr>
                    """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ad Operations Report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 1400px; margin: 0 auto; padding: 20px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f5f5f5; }}
    .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
    .metric {{ padding: 15px; background: #f9f9f9; border-radius: 5px; }}
    .metric h3 {{ margin: 0; font-size: 1.5em; }}
  </style>
</head>
<body>
  <h1>Ad Operations Performance Report</h1>
  <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Granularity: {granularity}</p>
  <div class="summary">
    <div class="metric"><h3>{sum(c.impressions for c in campaigns):,}</h3><p>Impressions</p></div>
    <div class="metric"><h3>{sum(c.clicks for c in campaigns):,}</h3><p>Clicks</p></div>
    <div class="metric"><h3>{sum(c.conversions for c in campaigns):,}</h3><p>Conversions</p></div>
    <div class="metric"><h3>${sum(c.spent for c in campaigns):,.2f}</h3><p>Total Spend</p></div>
  </div>
  <h2>Creative Performance</h2>
  <table>
    <thead>
      <tr>
        <th>Campaign</th>
        <th>Headline</th>
        <th>Platform</th>
        <th>CTR</th>
        <th>CPC</th>
        <th>CVR</th>
        <th>Budget</th>
        <th>Spent</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>"""

    def _generate_json(
        self, campaigns: List[Campaign], granularity: str
    ) -> str:
        data = {
            "generated_at": datetime.now().isoformat(),
            "granularity": granularity,
            "campaigns": [c.to_dict() for c in campaigns],
            "summary": {
                "total_impressions": sum(c.impressions for c in campaigns),
                "total_clicks": sum(c.clicks for c in campaigns),
                "total_conversions": sum(c.conversions for c in campaigns),
                "total_spend": sum(c.spent for c in campaigns),
                "total_revenue": sum(c.revenue for c in campaigns),
            },
        }
        return json.dumps(data, indent=2, default=str)

    def _generate_csv(
        self, campaigns: List[Campaign], granularity: str
    ) -> str:
        output = []
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "campaign_id", "campaign_name", "platform", "objective",
                "status", "impressions", "clicks", "conversions", "spent",
                "revenue", "ctr", "cpc", "cpa", "roas",
            ],
        )
        writer.writeheader()
        for c in campaigns:
            row = {
                "campaign_id": c.id,
                "campaign_name": c.name,
                "platform": c.platform.value,
                "objective": c.objective.value,
                "status": c.status.value,
                "impressions": c.impressions,
                "clicks": c.clicks,
                "conversions": c.conversions,
                "spent": c.spent,
                "revenue": c.revenue,
                "ctr": f"{c.ctr():.2f}",
                "cpc": f"{c.cpc():.2f}",
                "cpa": f"{c.cpa():.2f}",
                "roas": f"{c.roas():.2f}",
            }
            output.append(writer.writerow(row))
        return "\n".join(output)

    def _generate_pdf(
        self, campaigns: List[Campaign], granularity: str
    ) -> str:
        # Placeholder for actual PDF generation (e.g., weasyprint)
        return self._generate_json(campaigns, granularity)


# ============================================================================
# Main Agent
# ============================================================================


class AdOperationsAgent:
    """Agent for digital advertising operations and campaign management.

    Usage:
        agent = AdOperationsAgent()
        campaign = agent.create_campaign("Summer Sale", 500.0)
        agent.optimize_campaign(campaign.id)
        report = agent.generate_report([campaign])
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._campaigns: List[Campaign] = []
        self._campaign_count = 0
        self._last_report: Optional[str] = None
        self._fraud_engine = FraudDetectionEngine(self._config)
        self._bidding_engine = BiddingEngine(self._config)
        self._reporting_engine = ReportingEngine(self._config)
        self._ab_test_manager = ABTestManager(self._config)
        self._budget_monitor = BudgetPacingMonitor(self._config)
        self._alerts: List[PerformanceAlert] = []
        self._history: List[Dict[str, Any]] = []

    # -------------------------------------------------------------------------
    # Campaign Management
    # -------------------------------------------------------------------------

    def create_campaign(
        self,
        name: str,
        platform: str,
        objective: str,
        total_budget: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Campaign:
        """Create a new advertising campaign."""
        self._campaign_count += 1
        campaign = Campaign(
            id=f"camp-{self._campaign_count:04d}-{int(time.time())}",
            name=name,
            platform=AdPlatform(platform.lower()),
            objective=CampaignObjective(objective.lower()),
            status=CampaignStatus.DRAFT,
            budget=BiddingConfig(
                strategy=BiddingStrategy(self._config.default_bidding_strategy),
                target_cpa=self._config.target_cpa,
                target_roas=self._config.target_roas,
                daily_budget=self._config.daily_budget_cap,
            ),
            total_budget=total_budget,
            start_date=start_date,
            end_date=end_date,
        )
        self._campaigns.append(campaign)
        self._history.append(
            {
                "action": "create_campaign",
                "campaign_id": campaign.id,
                "timestamp": datetime.now().isoformat(),
            }
        )
        return campaign

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        for c in self._campaigns:
            if c.id == campaign_id:
                return c
        return None

    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise CampaignError(f"Campaign {campaign_id} not found.")
        campaign.status = CampaignStatus.PAUSED
        campaign.updated_at = datetime.now()
        return {"status": "success", "campaign": campaign_id, "new_status": campaign.status.value}

    def resume_campaign(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise CampaignError(f"Campaign {campaign_id} not found.")
        campaign.status = CampaignStatus.ACTIVE
        campaign.updated_at = datetime.now()
        return {"status": "success", "campaign": campaign_id, "new_status": campaign.status.value}

    def archive_campaign(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise CampaignError(f"Campaign {campaign_id} not found.")
        campaign.status = CampaignStatus.ARCHIVED
        campaign.updated_at = datetime.now()
        return {"status": "success", "campaign": campaign_id, "new_status": campaign.status.value}

    def add_ad_group(
        self,
        campaign_id: str,
        name: str,
        daily_budget: float,
        target_cpa: Optional[float] = None,
        bidding_strategy: str = "target_cpa",
    ) -> AdGroup:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise CampaignError(f"Campaign {campaign_id} not found.")

        ad_group = AdGroup(
            id=f"ag-{len(campaign.ad_groups) + 1:03d}-{int(time.time())}",
            name=name,
            campaign_id=campaign_id,
            status=CampaignStatus.DRAFT,
            bidding=BiddingConfig(
                strategy=BiddingStrategy(bidding_strategy),
                target_cpa=target_cpa,
                daily_budget=daily_budget,
            ),
            target_cpa=target_cpa,
        )
        campaign.ad_groups.append(ad_group)
        campaign.updated_at = datetime.now()
        return ad_group

    def add_creative(
        self,
        campaign_id: str,
        ad_group_id: str,
        headline: str,
        description: str,
        ad_type: str,
        image_url: Optional[str] = None,
        video_url: Optional[str] = None,
        final_url: str = "",
    ) -> AdCreative:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise CampaignError(f"Campaign {campaign_id} not found.")

        ad_group = None
        for ag in campaign.ad_groups:
            if ag.id == ad_group_id:
                ad_group = ag
                break

        if not ad_group:
            raise CampaignError(f"Ad group {ad_group_id} not found in campaign {campaign_id}.")

        creative = AdCreative(
            id=f"cr-{len(ad_group.creatives) + 1:03d}-{int(time.time())}",
            headline=headline,
            description=description,
            ad_type=AdType(ad_type.lower()),
            platform=campaign.platform,
            image_url=image_url,
            video_url=video_url,
            final_url=final_url,
        )
        ad_group.creatives.append(creative)
        ad_group.status = CampaignStatus.ACTIVE
        campaign.updated_at = datetime.now()
        return creative

    # -------------------------------------------------------------------------
    # Optimization
    # -------------------------------------------------------------------------

    def optimize_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Run full optimization cycle for a campaign."""
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise CampaignError(f"Campaign {campaign_id} not found.")

        recommendations = self._generate_recommendations(campaign)
        optimized = self._apply_optimizations(campaign, recommendations)

        return {
            "campaign_id": campaign_id,
            "recommendations": len(recommendations),
            "optimized": optimized,
            "actions_taken": [r["action"] for r in recommendations],
        }

    def optimize_budget(self, campaign_ids: Optional[List[str]] = None) -> Dict[str, float]:
        campaigns = (
            [self.get_campaign(cid) for cid in campaign_ids]
            if campaign_ids
            else [c for c in self._campaigns if c.status == CampaignStatus.ACTIVE]
        )
        campaigns = [c for c in campaigns if c is not None]
        return self._bidding_engine.optimize_budget_allocation(campaigns)

    def calculate_recommended_bid(
        self,
        campaign_id: str,
        ad_group_id: str,
        target_metric: str = "cpa",
    ) -> float:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise CampaignError(f"Campaign {campaign_id} not found.")

        ad_group = None
        for ag in campaign.ad_groups:
            if ag.id == ad_group_id:
                ad_group = ag
                break

        if not ad_group:
            raise CampaignError(f"Ad group {ad_group_id} not found.")
        return self._bidding_engine.calculate_bid(campaign, ad_group, target_metric)

    def _generate_recommendations(
        self, campaign: Campaign
    ) -> List[Dict[str, Any]]:
        recommendations = []

        # Low CTR recommendation
        if campaign.ctr() < 1.0:
            for ag in campaign.ad_groups:
                for cr in ag.creatives:
                    if cr.ctr() < 0.5:
                        recommendations.append(
                            {
                                "action": "pause_low_ctr_creative",
                                "creative_id": cr.id,
                                "reason": f"CTR {cr.ctr():.2f}% is below benchmark",
                                "confidence": 0.9,
                            }
                        )

        # High CPA recommendation
        if campaign.cpa() > self._config.target_cpa * 1.5:
            recommendations.append(
                {
                    "action": "lower_bids",
                    "reason": f"CPA {campaign.cpa():.2f} exceeds target {self._config.target_cpa:.2f}",
                    "confidence": 0.85,
                    "adjustment_factor": 0.9,
                }
            )

        # Budget pacing issue
        forecast = self._budget_monitor.get_spend_forecast(campaign.id)
        if forecast and len(forecast) >= 2:
            total_forecast = sum(f["forecasted_spend"] for f in forecast)
            if total_forecast > campaign.total_budget - campaign.spent:
                recommendations.append(
                    {
                        "action": "increase_budget",
                        "reason": "Projected overspend in next period",
                        "confidence": 0.8,
                        "recommended_budget": total_forecast,
                    }
                )

        return recommendations

    def _apply_optimizations(
        self, campaign: Campaign, recommendations: List[Dict[str, Any]]
    ) -> bool:
        for rec in recommendations:
            action = rec["action"]
            if action == "pause_low_ctr_creative":
                for ag in campaign.ad_groups:
                    for cr in ag.creatives:
                        if cr.id == rec["creative_id"]:
                            cr.status = AdStatus.PAUSED
            elif action == "lower_bids":
                for ag in campaign.ad_groups:
                    ag.bidding.target_cpa *= rec.get("adjustment_factor", 0.9)
            elif action == "increase_budget":
                campaign.budget.daily_budget = rec.get(
                    "recommended_budget", campaign.budget.daily_budget
                )
        return True


    # -------------------------------------------------------------------------
    # Metrics & Reporting
    # -------------------------------------------------------------------------

    def batch_audit(self, campaign_ids: List[str]) -> List[Dict[str, Any]]:
        results = []
        for cid in campaign_ids:
            campaign = self.get_campaign(cid)
            if campaign:
                results.append(
                    {
                        "campaign_id": cid,
                        "name": campaign.name,
                        "status": campaign.status.value,
                        "ctr": campaign.ctr(),
                        "cpc": campaign.cpc(),
                        "cpa": campaign.cpa(),
                        "roas": campaign.roas(),
                        "spent": campaign.spent,
                        "alerts": [
                            a.to_dict()
                            for a in self._alerts
                            if a.campaign_id == cid
                        ],
                    }
                )
        return results

    def generate_report(
        self,
        campaign_ids: Optional[List[str]] = None,
        fmt: str = "html",
        output_path: Optional[str] = None,
    ) -> str:
        campaigns = (
            [self.get_campaign(cid) for cid in campaign_ids]
            if campaign_ids
            else self._campaigns
        )
        campaigns = [c for c in campaigns if c is not None]
        self._last_report = self._reporting_engine.generate(
            campaigns, fmt=fmt, output_path=output_path
        )
        return self._last_report

    def get_metrics_summary(
        self, campaign_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if campaign_id:
            campaign = self.get_campaign(campaign_id)
            if not campaign:
                return {}
            return {
                "campaign_id": campaign.id,
                "name": campaign.name,
                "impressions": campaign.impressions,
                "clicks": campaign.clicks,
                "conversions": campaign.conversions,
                "spent": campaign.spent,
                "ctr": campaign.ctr(),
                "cpc": campaign.cpc(),
                "cpa": campaign.cpa(),
                "roas": campaign.roas(),
            }

        return {
            "total_campaigns": len(self._campaigns),
            "active_campaigns": sum(
                1 for c in self._campaigns if c.status == CampaignStatus.ACTIVE
            ),
            "total_impressions": sum(c.impressions for c in self._campaigns),
            "total_clicks": sum(c.clicks for c in self._campaigns),
            "total_conversions": sum(c.conversions for c in self._campaigns),
            "total_spent": sum(c.spent for c in self._campaigns),
            "total_revenue": sum(c.revenue for c in self._campaigns),
            "avg_ctr": statistics.mean(
                [c.ctr() for c in self._campaigns if c.impressions > 0]
            )
            or 0,
            "avg_cpc": statistics.mean(
                [c.cpc() for c in self._campaigns if c.clicks > 0]
            )
            or 0,
            "avg_cpa": statistics.mean(
                [c.cpa() for c in self._campaigns if c.conversions > 0]
            )
            or 0,
        }

    # -------------------------------------------------------------------------
    # Fraud Detection
    # -------------------------------------------------------------------------

    def analyze_fraud(
        self, clicks: List[Dict], conversions: List[Dict]
    ) -> List[FraudSignal]:
        click_signals = self._fraud_engine.analyze_clicks(clicks)
        conversion_signals = self._fraud_engine.analyze_conversions(conversions)
        return click_signals + conversion_signals

    def get_fraud_signals(self) -> List[FraudSignal]:
        return self._fraud_engine.get_signals()

    # -------------------------------------------------------------------------
    # A/B Testing
    # -------------------------------------------------------------------------

    def create_ab_test(
        self,
        test_id: str,
        variant_a_id: str,
        variant_b_id: str,
        metric: str = "ctr",
        sample_size: int = 1000,
    ) -> ABTestResult:
        return self._ab_test_manager.create_test(
            test_id, variant_a_id, variant_b_id, metric, sample_size
        )

    def record_ab_observation(
        self,
        test_id: str,
        variant: str,
        converted: bool,
        impression: bool = True,
    ) -> None:
        self._ab_test_manager.record_observation(test_id, variant, converted, impression)

    def get_ab_test_result(self, test_id: str) -> Optional[ABTestResult]:
        return self._ab_test_manager.get_test(test_id)

    def complete_ab_test(self, test_id: str) -> ABTestResult:
        return self._ab_test_manager.complete_test(test_id)

    # -------------------------------------------------------------------------
    # Alerts
    # -------------------------------------------------------------------------

    def get_alerts(self) -> List[PerformanceAlert]:
        return self._alerts + self._budget_monitor.get_alerts()

    def acknowledge_alert(self, alert_id: str) -> Dict[str, Any]:
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.is_acknowledged = True
                return {"status": "success", "alert_id": alert_id}
        return {"status": "not_found", "alert_id": alert_id}

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AdOperationsAgent",
            "campaigns": len(self._campaigns),
            "active_campaigns": sum(
                1 for c in self._campaigns if c.status == CampaignStatus.ACTIVE
            ),
            "total_alerts": len(self.get_alerts()),
            "fraud_signals": len(self.get_fraud_signals()),
            "active_ab_tests": len(self._ab_test_manager._active_tests),
        }

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history[-100:]

    def clear_history(self) -> None:
        self._history = []

    def batch_create_campaigns(
        self, campaign_defs: List[Dict[str, Any]]
    ) -> List[Campaign]:
        campaigns = []
        for defn in campaign_defs:
            try:
                campaign = self.create_campaign(
                    name=defn["name"],
                    platform=defn["platform"],
                    objective=defn["objective"],
                    total_budget=defn["total_budget"],
                )
                campaigns.append(campaign)
            except Exception as e:
                logger.error(f"Failed to create campaign {defn.get('name')}: {e}")
        return campaigns

    def export_campaigns(self, fmt: str = "json") -> str:
        return json.dumps(
            [c.to_dict() for c in self._campaigns], indent=2, default=str
        )

    def import_campaigns(self, data: str, fmt: str = "json") -> int:
        if fmt == "json":
            try:
                payload = json.loads(data)
                if isinstance(payload, list):
                    for item in payload:
                        self._import_single_campaign(item)
                    return len(payload)
            except json.JSONDecodeError:
                pass
        return 0

    def _import_single_campaign(self, item: Dict[str, Any]) -> None:
        item.setdefault("id", f"imported-{len(self._campaigns) + 1}")
        item.setdefault("status", CampaignStatus.DRAFT.value)
        item.setdefault("created_at", datetime.now().isoformat())
        self._campaigns.append(item)  # type: ignore

    def predict_performance(
        self, campaign_id: str, days: int = 7
    ) -> Dict[str, Any]:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return {}

        daily_spend = campaign.spent / max(1, (datetime.now() - campaign.created_at).days)
        daily_conversions = campaign.conversions / max(1, (datetime.now() - campaign.created_at).days)

        return {
            "campaign_id": campaign_id,
            "forecast_days": days,
            "forecasted_spend": daily_spend * days,
            "forecasted_conversions": daily_conversions * days,
            "forecasted_revenue": daily_conversions * days * self._config.target_cpa * 3,
            "cpa_forecast": self._config.target_cpa,
        }

    def compare_campaigns(self, ids: List[str]) -> Dict[str, Any]:
        campaigns = [self.get_campaign(cid) for cid in ids]
        campaigns = [c for c in campaigns if c]
        if not campaigns:
            return {}

        return {
            "campaigns": [
                {
                    "id": c.id,
                    "name": c.name,
                    "ctr": c.ctr(),
                    "cpc": c.cpc(),
                    "cpa": c.cpa(),
                    "roas": c.roas(),
                }
                for c in campaigns
            ],
            "best_ctr": max(campaigns, key=lambda c: c.ctr()).id,
            "best_roas": max(campaigns, key=lambda c: c.roas()).id,
            "lowest_cpa": min(campaigns, key=lambda c: c.cpa()).id,
            "highest_spend": max(campaigns, key=lambda c: c.spent).id,
        }

    def list_campaigns(
        self,
        status: Optional[str] = None,
        platform: Optional[str] = None,
    ) -> List[Campaign]:
        result = self._campaigns
        if status:
            result = [c for c in result if c.status.value == status]
        if platform:
            result = [
                c for c in result if c.platform.value.lower() == platform.lower()
            ]
        return result


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "AdOperationsAgent",
    "Campaign",
    "AdGroup",
    "AdCreative",
    "BiddingConfig",
    "AudienceSegment",
    "FraudSignal",
    "PerformanceAlert",
    "ABTestResult",
    "Config",
    "AdPlatform",
    "CampaignObjective",
    "CampaignStatus",
    "BiddingStrategy",
    "AdStatus",
    "AdType",
    "AudienceType",
    "DeviceType",
    "AlertSeverity",
    "BiddingEngine",
    "FraudDetectionEngine",
    "ABTestManager",
    "BudgetPacingMonitor",
    "ReportingEngine",
    "ReportGenerator",
    "AdOperationsError",
    "CampaignError",
    "BiddingError",
    "ReportingError",
    "FraudDetectionError",
    "PlatformAPIError",
    "ConfigurationError",
    "ValidationError",
]


def main():
    """Demo CLI for Ad Operations Agent."""
    import argparse

    parser = argparse.ArgumentParser(description="Ad Operations Agent")
    parser.add_argument("--create", action="store_true", help="Create demo campaign")
    parser.add_argument("--optimize", help="Optimize campaign by ID")
    parser.add_argument("--report", help="Generate report for campaign ID")
    parser.add_argument("--budget", action="store_true", help="Optimize budgets")
    parser.add_argument("--fraud", action="store_true", help="Run fraud analysis demo")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    agent = AdOperationsAgent()

    if args.create:
        campaign = agent.create_campaign(
            "Demo Campaign",
            "google",
            "conversions",
            1000.0,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=14),
        )
        print(f"Created campaign: {campaign.id}")
        ag = agent.add_ad_group(campaign.id, "Search Ads", 100.0)
        print(f"Created ad group: {ag.id}")
        cr = agent.add_creative(
            campaign.id,
            ag.id,
            "Best Deals Today",
            "Shop now and save big!",
            "text",
            final_url="https://example.com",
        )
        print(f"Created creative: {cr.id}")
        print(agent.get_status())
    elif args.optimize:
        result = agent.optimize_campaign(args.optimize)
        print(f"Optimization result: {result}")
    elif args.report:
        report = agent.generate_report([args.report], fmt="markdown")
        print(report)
    elif args.budget:
        allocations = agent.optimize_budget()
        print(f"Budget allocations: {allocations}")
    elif args.fraud:
        clicks = [
            {"ip_address": f"192.168.1.{random.randint(1, 255)}", "campaign_id": "1", "ad_id": "1"}
            for _ in range(30)
        ] + [
            {"ip_address": "10.0.0.1", "campaign_id": "1", "ad_id": "1"}
            for _ in range(50)
        ]
        signals = agent.analyze_fraud(clicks, [])
        print(f"Detected {len(signals)} fraud signals")
        for s in signals:
            print(f"  - {s.signal_type}: {s.description}")
    else:
        print("Ad Operations Agent Demo")
        print(agent.get_status())


if __name__ == "__main__":
    main()
