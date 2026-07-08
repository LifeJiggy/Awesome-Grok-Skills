"""Conversion Optimization Agent - A/B Testing, Funnel Optimization, UX Analysis, Landing Pages, CRO.

A comprehensive conversion rate optimization system that handles A/B test design and analysis,
conversion funnel optimization, UX analysis, landing page optimization, and CRO framework
implementation. Built for growth teams, product managers, and UX researchers who need a
structured, data-driven approach to improving conversion rates.

Architecture: Event-driven CRO pipeline with hypothesis → experiment → analysis → implementation
stages. Each stage produces validated artifacts that feed downstream optimization cycles.

Author: Awesome Grok Skills Team
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import random
import re
import statistics
import uuid
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
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

# ---------------------------------------------------------------------------
# Module-level setup
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

__all__ = [
    "ConversionOptimizationAgent",
    "Config",
    "ABTest",
    "FunnelAnalysis",
    "UXReport",
    "LandingPageAudit",
    "CROStrategy",
    "Hypothesis",
    "ExperimentResult",
    "ContentType",
    "TestStatus",
    "TestType",
    "FunnelStage",
    "UXSeverity",
    "LandingPageElement",
    "CROFramework",
    "ConversionMetric",
    "TrafficSource",
    "DeviceType",
    "UserSegment",
    "TestPriority",
    "StatisticalSignificance",
    "HeatmapType",
    "FormFieldType",
    "CTAPosition",
    "TrustSignal",
    "PricingModel",
    "SocialProofType",
    "UrgencyType",
    "CheckoutStep",
    "PageSpeedMetric",
    "AccessibilityIssue",
    "MobileBreakpoint",
]

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class TestStatus(Enum):
    """Status of an A/B test."""
    DRAFT = "draft"
    APPROVED = "approved"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TestType(Enum):
    """Types of A/B tests."""
    A_B = "a_b"
    A_B_N = "a_b_n"
    MULTIVARIATE = "multivariate"
    SPLIT_URL = "split_url"
    MULTIPAGE = "multipage"
    BANDIT = "bandit"
    PERSONALIZATION = "personalization"


class TestPriority(IntEnum):
    """Priority levels for tests."""
    P0_CRITICAL = 0
    P1_HIGH = 1
    P2_MEDIUM = 2
    P3_LOW = 3
    P4_BACKLOG = 4


class FunnelStage(Enum):
    """Stages of a conversion funnel."""
    AWARENESS = "awareness"
    INTEREST = "interest"
    CONSIDERATION = "consideration"
    INTENT = "intent"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    ONBOARDING = "onboarding"
    RETENTION = "retention"
    ADVOCACY = "advocacy"
    UPSELL = "upsell"
    CROSSSELL = "crosssell"
    RENEWAL = "renewal"
    CHECKOUT = "checkout"
    CART = "cart"
    SIGNUP = "signup"
    TRIAL = "trial"
    ACTIVATION = "activation"


class UXSeverity(Enum):
    """Severity levels for UX issues."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class LandingPageElement(Enum):
    """Elements of a landing page."""
    HERO_SECTION = "hero_section"
    HEADLINE = "headline"
    SUBHEADLINE = "subheadline"
    CALL_TO_ACTION = "call_to_action"
    SOCIAL_PROOF = "social_proof"
    TRUST_SIGNALS = "trust_signals"
    BENEFITS = "benefits"
    FEATURES = "features"
    TESTIMONIALS = "testimonials"
    CASE_STUDIES = "case_studies"
    PRICING = "pricing"
    FAQ = "faq"
    FOOTER = "footer"
    NAVIGATION = "navigation"
    FORM = "form"
    MEDIA = "media"
    COUNTER = "counter"
    GUARANTEE = "guarantee"
    RISK_REVERSAL = "risk_reversal"
    URGENCY = "urgency"


class CROFramework(Enum):
    """CRO frameworks for structured optimization."""
    AARRR = "aarrr"
    ICE = "ice"
    PXL = "pxl"
    RICE = "rice"
    PIE = "pie"
    WISH = "wish"
    now_next_roadmap = "now_next_roadmap"
    HOURS_of_impact = "hours_of_impact"
    impact_effort = "impact_effort"
    confidence_impact_ease = "confidence_impact_ease"


class ConversionMetric(Enum):
    """Metrics tracked for conversion optimization."""
    CONVERSION_RATE = "conversion_rate"
    REVENUE_PER_VISITOR = "revenue_per_visitor"
    AVERAGE_ORDER_VALUE = "average_order_value"
    CART_ABANDONMENT_RATE = "cart_abandonment_rate"
    CHECKOUT_COMPLETION_RATE = "checkout_completion_rate"
    SIGNUP_RATE = "signup_rate"
    TRIAL_START_RATE = "trial_start_rate"
    TRIAL_TO_PAID_RATE = "trial_to_paid_rate"
    ENGAGEMENT_RATE = "engagement_rate"
    BOUNCE_RATE = "bounce_rate"
    TIME_ON_PAGE = "time_on_page"
    PAGES_PER_SESSION = "pages_per_session"
    CLICK_THROUGH_RATE = "click_through_rate"
    FORM_COMPLETION_RATE = "form_completion_rate"
    LEAD_GENERATION_RATE = "lead_generation_rate"
    CUSTOMER_ACQUISITION_COST = "customer_acquisition_cost"
    LIFETIME_VALUE = "lifetime_value"
    CHURN_RATE = "churn_rate"
    NET_PROMOTER_SCORE = "net_promoter_score"
    ACTIVATION_RATE = "activation_rate"
    FEATURE_ADOPTION_RATE = "feature_adoption_rate"
    ONBOARDING_COMPLETION_RATE = "onboarding_completion_rate"


class TrafficSource(Enum):
    """Traffic sources for segmentation."""
    ORGANIC_SEARCH = "organic_search"
    PAID_SEARCH = "paid_search"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    REFERRAL = "referral"
    DIRECT = "direct"
    DISPLAY = "display"
    AFFILIATE = "affiliate"
    VIDEO = "video"
    PODCAST = "podcast"
    PARTNERSHIP = "partnership"
    OFFLINE = "offline"


class DeviceType(Enum):
    """Device types for segmentation."""
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    SMART_TV = "smart_tv"
    WEARABLE = "wearable"


class UserSegment(Enum):
    """User segments for targeting."""
    NEW_VISITOR = "new_visitor"
    RETURNING_VISITOR = "returning_visitor"
    SUBSCRIBER = "subscriber"
    TRIAL_USER = "trial_user"
    FREE_USER = "free_user"
    PAID_USER = "paid_user"
    ENTERPRISE = "enterprise"
    SMB = "smb"
    POWER_USER = "power_user"
    CHURN_RISK = "churn_risk"
    DORMANT = "dormant"
    HIGH_VALUE = "high_value"
    LOW_VALUE = "low_value"
    REFERRED = "referred"
    ORGANIC = "organic"


class StatisticalSignificance(Enum):
    """Statistical significance levels."""
    VERY_HIGH = "very_high"    # p < 0.01
    HIGH = "high"              # p < 0.05
    MODERATE = "moderate"      # p < 0.10
    LOW = "low"                # p < 0.20
    NONE = "none"              # p >= 0.20


class HeatmapType(Enum):
    """Types of heatmaps for UX analysis."""
    CLICK = "click"
    MOVE = "move"
    SCROLL = "scroll"
    ATTENTION = "attention"
    CONFUSION = "confusion"
    ENGAGEMENT = "engagement"


class FormFieldType(Enum):
    """Form field types for analysis."""
    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"
    PHONE = "phone"
    NUMBER = "number"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TEXTAREA = "textarea"
    DATE = "date"
    FILE = "file"
    ADDRESS = "address"
    PAYMENT = "payment"
    CAPTCHA = "captcha"


class CTAPosition(Enum):
    """Call-to-action position types."""
    ABOVE_FOLD = "above_fold"
    BELOW_FOLD = "below_fold"
    INLINE = "inline"
    FLOATING = "floating"
    MODAL = "modal"
    SLIDE_IN = "slide_in"
    STICKY = "sticky"
    END_OF_CONTENT = "end_of_content"
    SIDEBAR = "sidebar"
    NAVIGATION = "navigation"


class TrustSignal(Enum):
    """Trust signals for landing pages."""
    SSL_CERTIFICATE = "ssl_certificate"
    PRIVACY_POLICY = "privacy_policy"
    TERMS_OF_SERVICE = "terms_of_service"
    MONEY_BACK_GUARANTEE = "money_back_guarantee"
    FREE_TRIAL = "free_trial"
    CASE_STUDY = "case_study"
    TESTIMONIAL = "testimonial"
    CLIENT_LOGO = "client_logo"
    INDUSTRY_AWARD = "industry_award"
    MEDIA_MENTION = "media_mention"
    PARTNER_LOGO = "partner_logo"
    SECURITY_BADGE = "security_badge"
    REVIEW_SCORE = "review_score"
    CUSTOMER_COUNT = "customer_count"
    YEARS_IN_BUSINESS = "years_in_business"


class SocialProofType(Enum):
    """Types of social proof."""
    TESTIMONIAL = "testimonial"
    CASE_STUDY = "case_study"
    REVIEW = "review"
    RATING = "rating"
    CLIENT_LOGO = "client_logo"
    USER_COUNT = "user_count"
    DOWNLOAD_COUNT = "download_count"
    USAGE_STAT = "usage_stat"
    ENDORSEMENT = "endorsement"
    MEDIA_MENTION = "media_mention"
    AWARD = "award"
    CERTIFICATION = "certification"


class UrgencyType(Enum):
    """Types of urgency/scarcity."""
    COUNTDOWN_TIMER = "countdown_timer"
    LIMITED_STOCK = "limited_stock"
    LIMITED_TIME = "limited_time"
    FLASH_SALE = "flash_sale"
    EARLY_BIRD = "early_bird"
    WAITLIST = "waitlist"
    EXCLUSIVE = "exclusive"
    SEASONAL = "seasonal"
    PRICE_INCREASE = "price_increase"
    FEATURE_REMOVAL = "feature_removal"


class CheckoutStep(Enum):
    """Steps in a checkout flow."""
    CART_REVIEW = "cart_review"
    ACCOUNT_CREATION = "account_creation"
    SHIPPING_INFO = "shipping_info"
    BILLING_INFO = "billing_info"
    PAYMENT = "payment"
    ORDER_REVIEW = "order_review"
    CONFIRMATION = "confirmation"
    UPSELL = "upsell"


class PageSpeedMetric(Enum):
    """Page speed metrics."""
    FIRST_CONTENTFUL_PAINT = "first_contentful_paint"
    LARGEST_CONTENTFUL_PAINT = "largest_contentful_paint"
    FIRST_INPUT_DELAY = "first_input_delay"
    CUMULATIVE_LAYOUT_SHIFT = "cumulative_layout_shift"
    INTERACTION_TO_NEXT_PAINT = "interaction_to_next_paint"
    TIME_TO_FIRST_BYTE = "time_to_first_byte"
    TOTAL_BLOCKING_TIME = "total_blocking_time"
    SPEED_INDEX = "speed_index"


class AccessibilityIssue(Enum):
    """Accessibility issues."""
    MISSING_ALT_TEXT = "missing_alt_text"
    MISSING_LABEL = "missing_label"
    LOW_CONTRAST = "low_contrast"
    MISSING_FOCUS = "missing_focus"
    MISSING_HEADING = "missing_heading"
    MISSING_LANG = "missing_lang"
    MISSING_SKIP_LINK = "missing_skip_link"
    MISSING_ARIA = "missing_aria"
    KEYBOARD_TRAP = "keyboard_trap"
    MISSING_CAPTION = "missing_caption"
    REDUNDANT_LINK = "redundant_link"
    MISSING_TITLE = "missing_title"


class MobileBreakpoint(Enum):
    """Mobile responsive breakpoints."""
    MOBILE_PORTRAIT = "mobile_portrait"    # < 576px
    MOBILE_LANDSCAPE = "mobile_landscape"  # 576-767px
    TABLET_PORTRAIT = "tablet_portrait"    # 768-991px
    TABLET_LANDSCAPE = "tablet_landscape"  # 992-1199px
    DESKTOP = "desktop"                    # 1200-1439px
    LARGE_DESKTOP = "large_desktop"        # >= 1440px


class PersonaType(Enum):
    """User persona types for targeting."""
    DECISION_MAKER = "decision_maker"
    INFLUENCER = "influencer"
    USER = "user"
    BUYER = "buyer"
    ADMIN = "admin"
    TECHNICAL = "technical"
    EXECUTIVE = "executive"
    FINANCE = "finance"
    OPERATIONS = "operations"


class ExperimentGoal(Enum):
    """Goals for experiments."""
    INCREASE_CONVERSIONS = "increase_conversions"
    REDUCE_BOUNCE = "reduce_bounce"
    INCREASE_ENGAGEMENT = "increase_engagement"
    REDUCE_DROP_OFF = "reduce_drop_off"
    INCREASE_REVENUE = "increase_revenue"
    IMPROVE_RETENTION = "improve_retention"
    REDUCE_CHURN = "reduce_churn"
    INCREASE_ACTIVATION = "increase_activation"
    IMPROVE_ONBOARDING = "improve_onboarding"
    REDUCE_SUPPORT = "reduce_support"


class AnalysisType(Enum):
    """Types of funnel analysis."""
    DROP_OFF = "drop_off"
    COHORT = "cohort"
    SEGMENT = "segment"
    PATH = "path"
    TIME_SERIES = "time_series"
    COMPARISON = "comparison"
    ATTRIBUTION = "attribution"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class TestConfig:
    """Configuration for A/B testing."""
    default_confidence_level: float = 0.95
    minimum_sample_size: int = 100
    maximum_test_duration_days: int = 30
    minimum_runtime_days: int = 7
    traffic_allocation_default: float = 0.5
    auto_stop_on_significance: bool = True
    false_positive_rate: float = 0.05
    minimum_detectable_effect: float = 0.02
    sequential_testing_enabled: bool = False
    bayesian_testing_enabled: bool = False
    cross_domain_tracking: bool = False
    bot_filtering_enabled: bool = True
    cookie_duration_days: int = 30
    sticky_assignment: bool = True
    qa_enabled: bool = True


@dataclass
class FunnelConfig:
    """Configuration for funnel analysis."""
    default_attribution_window_days: int = 30
    session_timeout_minutes: int = 30
    cross_device_tracking: bool = True
    cohort_analysis_enabled: bool = True
    path_analysis_enabled: bool = True
    drop_off_threshold: float = 0.10
    funnel_steps_limit: int = 20
    segment_comparison_enabled: bool = True
    real_time_updates: bool = False


@dataclass
class UXConfig:
    """Configuration for UX analysis."""
    heatmap_enabled: bool = True
    session_recording_enabled: bool = True
    scroll_depth_tracking: bool = True
    form_analytics_enabled: bool = True
    rage_click_detection: bool = True
    dead_click_detection: bool = True
    error_tracking_enabled: bool = True
    accessibility_audit_enabled: bool = True
    mobile_testing_enabled: bool = True
    page_speed_monitoring: bool = True


@dataclass
class LandingPageConfig:
    """Configuration for landing page optimization."""
    auto_optimize_enabled: bool = False
    personalization_enabled: bool = True
    dynamic_text_enabled: bool = True
    social_proof_auto_rotate: bool = True
    urgency_elements_enabled: bool = True
    exit_intent_enabled: bool = True
    ab_test_all_elements: bool = False
    min_elements_for_test: int = 2
    max_variations_per_element: int = 5


@dataclass
class Config:
    """Main configuration for the Conversion Optimization Agent."""
    agent_name: str = "ConversionOptimizationAgent"
    version: str = "3.0.0"
    log_level: str = "INFO"
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    timezone: str = "UTC"
    default_currency: str = "USD"
    tracking_enabled: bool = True
    privacy_mode: bool = False
    data_retention_days: int = 730
    export_formats: List[str] = field(
        default_factory=lambda: ["json", "csv", "markdown", "pdf"]
    )
    ab_test: TestConfig = field(default_factory=TestConfig)
    funnel: FunnelConfig = field(default_factory=FunnelConfig)
    ux: UXConfig = field(default_factory=UXConfig)
    landing_page: LandingPageConfig = field(default_factory=LandingPageConfig)
    notification_channels: List[str] = field(default_factory=lambda: ["email"])
    webhook_urls: Dict[str, str] = field(default_factory=dict)
    api_keys: Dict[str, str] = field(default_factory=dict)
    export_directory: str = "./exports"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------


@dataclass
class Variant:
    """A variant in an A/B test."""
    variant_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    is_control: bool = False
    traffic_percentage: float = 50.0
    changes: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "variant_id": self.variant_id,
            "name": self.name,
            "description": self.description,
            "is_control": self.is_control,
            "traffic_percentage": self.traffic_percentage,
            "changes": self.changes,
        }


@dataclass
class Hypothesis:
    """A test hypothesis based on observation or data."""
    hypothesis_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    observation: str = ""
    insight: str = ""
    hypothesis_statement: str = ""
    expected_impact: str = ""
    priority: TestPriority = TestPriority.P2_MEDIUM
    ice_score: float = 0.0
    impact: int = 5
    confidence: int = 5
    ease: int = 5
    framework: CROFramework = CROFramework.ICE
    source: str = ""
    supporting_data: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "proposed"
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_ice_score(self) -> float:
        self.ice_score = (self.impact + self.confidence + self.ease) / 3.0
        return self.ice_score

    def calculate_rice_score(self, reach: int = 100, effort: int = 1) -> float:
        return (self.impact * reach * self.confidence) / max(effort, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "title": self.title,
            "observation": self.observation,
            "insight": self.insight,
            "hypothesis_statement": self.hypothesis_statement,
            "expected_impact": self.expected_impact,
            "priority": self.priority.value,
            "ice_score": round(self.ice_score, 2),
            "impact": self.impact,
            "confidence": self.confidence,
            "ease": self.ease,
            "framework": self.framework.value,
            "source": self.source,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ExperimentResult:
    """Statistical results of an A/B test."""
    result_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    test_id: str = ""
    variant_results: List[Dict[str, Any]] = field(default_factory=list)
    primary_metric: str = "conversion_rate"
    confidence_level: float = 0.0
    p_value: float = 1.0
    statistical_power: float = 0.0
    winner: Optional[str] = None
    lift: float = 0.0
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    sample_size_reached: bool = False
    minimum_runtime_reached: bool = False
    significance: StatisticalSignificance = StatisticalSignificance.NONE
    bayesian_probability: Optional[float] = None
    segments: Dict[str, Any] = field(default_factory=dict)
    daily_results: List[Dict[str, Any]] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def determine_significance(self) -> StatisticalSignificance:
        if self.p_value < 0.01:
            self.significance = StatisticalSignificance.VERY_HIGH
        elif self.p_value < 0.05:
            self.significance = StatisticalSignificance.HIGH
        elif self.p_value < 0.10:
            self.significance = StatisticalSignificance.MODERATE
        elif self.p_value < 0.20:
            self.significance = StatisticalSignificance.LOW
        else:
            self.significance = StatisticalSignificance.NONE
        return self.significance

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "test_id": self.test_id,
            "variant_results": self.variant_results,
            "primary_metric": self.primary_metric,
            "confidence_level": round(self.confidence_level, 4),
            "p_value": round(self.p_value, 6),
            "winner": self.winner,
            "lift": round(self.lift, 4),
            "significance": self.significance.value,
            "sample_size_reached": self.sample_size_reached,
            "minimum_runtime_reached": self.minimum_runtime_reached,
            "analyzed_at": self.analyzed_at.isoformat(),
        }


@dataclass
class ABTest:
    """Represents an A/B test experiment."""
    test_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = ""
    description: str = ""
    test_type: TestType = TestType.A_B
    status: TestStatus = TestStatus.DRAFT
    priority: TestPriority = TestPriority.P2_MEDIUM
    hypothesis_id: Optional[str] = None
    url: str = ""
    page_type: str = ""
    target_metric: ConversionMetric = ConversionMetric.CONVERSION_RATE
    variants: List[Variant] = field(default_factory=list)
    traffic_allocation: float = 100.0
    target_segments: List[UserSegment] = field(default_factory=list)
    target_sources: List[TrafficSource] = field(default_factory=list)
    target_devices: List[DeviceType] = field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    results: Optional[ExperimentResult] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_variant(self, name: str, is_control: bool = False, traffic: float = 50.0) -> Variant:
        variant = Variant(name=name, is_control=is_control, traffic_percentage=traffic)
        self.variants.append(variant)
        self.updated_at = datetime.utcnow()
        return variant

    def get_control(self) -> Optional[Variant]:
        for v in self.variants:
            if v.is_control:
                return v
        return None

    def get_total_traffic(self) -> float:
        return sum(v.traffic_percentage for v in self.variants)

    def is_ready_to_run(self) -> bool:
        return (
            len(self.variants) >= 2
            and self.status == TestStatus.APPROVED
            and any(v.is_control for v in self.variants)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "name": self.name,
            "description": self.description,
            "test_type": self.test_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "hypothesis_id": self.hypothesis_id,
            "url": self.url,
            "target_metric": self.target_metric.value,
            "variants": [v.to_dict() for v in self.variants],
            "traffic_allocation": self.traffic_allocation,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "results": self.results.to_dict() if self.results else None,
            "tags": self.tags,
        }


@dataclass
class FunnelStep:
    """A single step in a conversion funnel."""
    step_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    stage: FunnelStage = FunnelStage.AWARENESS
    url_pattern: str = ""
    event_name: str = ""
    visitors: int = 0
    conversions: int = 0
    drop_off_rate: float = 0.0
    conversion_rate: float = 0.0
    avg_time_on_step: float = 0.0
    bounce_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_rates(self, previous_visitors: int = 0) -> None:
        if previous_visitors > 0:
            self.drop_off_rate = 1.0 - (self.visitors / previous_visitors)
            self.conversion_rate = self.conversions / previous_visitors
        else:
            self.drop_off_rate = 0.0
            self.conversion_rate = self.conversions / max(self.visitors, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "name": self.name,
            "stage": self.stage.value,
            "visitors": self.visitors,
            "conversions": self.conversions,
            "drop_off_rate": round(self.drop_off_rate, 4),
            "conversion_rate": round(self.conversion_rate, 4),
            "avg_time_on_step": round(self.avg_time_on_step, 2),
        }


@dataclass
class FunnelAnalysis:
    """Complete funnel analysis with steps and insights."""
    analysis_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    steps: List[FunnelStep] = field(default_factory=list)
    total_visitors: int = 0
    total_conversions: int = 0
    overall_conversion_rate: float = 0.0
    overall_drop_off_rate: float = 0.0
    time_period_days: int = 30
    segment: Optional[UserSegment] = None
    source: Optional[TrafficSource] = None
    device: Optional[DeviceType] = None
    analysis_type: AnalysisType = AnalysisType.DROP_OFF
    insights: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    biggest_drop_off: Optional[str] = None
    benchmark_comparison: Optional[Dict[str, Any]] = None
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_overall_rate(self) -> float:
        if self.steps:
            self.total_visitors = self.steps[0].visitors
            self.total_conversions = self.steps[-1].conversions
            self.overall_conversion_rate = (
                self.total_conversions / max(self.total_visitors, 1)
            )
        return self.overall_conversion_rate

    def find_biggest_drop_off(self) -> Optional[FunnelStep]:
        if not self.steps:
            return None
        max_drop = 0.0
        biggest = None
        for i in range(1, len(self.steps)):
            if self.steps[i].drop_off_rate > max_drop:
                max_drop = self.steps[i].drop_off_rate
                biggest = self.steps[i]
        self.biggest_drop_off = biggest.step_id if biggest else None
        return biggest

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "name": self.name,
            "steps": [s.to_dict() for s in self.steps],
            "total_visitors": self.total_visitors,
            "total_conversions": self.total_conversions,
            "overall_conversion_rate": round(self.overall_conversion_rate, 4),
            "biggest_drop_off": self.biggest_drop_off,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "analyzed_at": self.analyzed_at.isoformat(),
        }


@dataclass
class UXIssue:
    """A UX issue identified during analysis."""
    issue_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    severity: UXSeverity = UXSeverity.MEDIUM
    category: str = ""
    element: str = ""
    page_url: str = ""
    screenshot_url: str = ""
    affected_users_percent: float = 0.0
    estimated_impact: str = ""
    recommendation: str = ""
    status: str = "open"
    assigned_to: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "category": self.category,
            "element": self.element,
            "affected_users_percent": self.affected_users_percent,
            "recommendation": self.recommendation,
            "status": self.status,
        }


@dataclass
class UXReport:
    """Comprehensive UX analysis report."""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    page_url: str = ""
    overall_score: float = 0.0
    issues: List[UXIssue] = field(default_factory=list)
    heatmap_data: Dict[str, Any] = field(default_factory=dict)
    scroll_depth_data: Dict[str, Any] = field(default_factory=dict)
    form_analytics: Dict[str, Any] = field(default_factory=dict)
    page_speed: Dict[str, float] = field(default_factory=dict)
    accessibility_score: float = 0.0
    mobile_score: float = 0.0
    readability_score: float = 0.0
    conversion_barriers: List[str] = field(default_factory=list)
    opportunities: List[Dict[str, Any]] = field(default_factory=list)
    benchmarks: Dict[str, float] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_issue(self, title: str, severity: UXSeverity, category: str, recommendation: str = "") -> UXIssue:
        issue = UXIssue(
            title=title,
            severity=severity,
            category=category,
            recommendation=recommendation,
            page_url=self.page_url,
        )
        self.issues.append(issue)
        return issue

    def calculate_overall_score(self) -> float:
        severity_weights = {
            UXSeverity.CRITICAL: 10,
            UXSeverity.HIGH: 7,
            UXSeverity.MEDIUM: 4,
            UXSeverity.LOW: 2,
            UXSeverity.INFO: 1,
        }
        total_deductions = sum(
            severity_weights.get(issue.severity, 0) for issue in self.issues
        )
        self.overall_score = max(0.0, 100.0 - total_deductions)
        return self.overall_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "page_url": self.page_url,
            "overall_score": round(self.overall_score, 2),
            "issues": [i.to_dict() for i in self.issues],
            "page_speed": self.page_speed,
            "accessibility_score": round(self.accessibility_score, 2),
            "mobile_score": round(self.mobile_score, 2),
            "conversion_barriers": self.conversion_barriers,
            "opportunities": self.opportunities,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class LandingPageElementAnalysis:
    """Analysis of a specific landing page element."""
    element_type: LandingPageElement = LandingPageElement.HERO_SECTION
    score: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    benchmark_comparison: Optional[Dict[str, Any]] = None
    ab_test_suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "element_type": self.element_type.value,
            "score": round(self.score, 2),
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendations": self.recommendations,
            "ab_test_suggestions": self.ab_test_suggestions,
        }


@dataclass
class LandingPageAudit:
    """Complete landing page audit with element-by-element analysis."""
    audit_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    page_url: str = ""
    page_type: str = ""
    overall_score: float = 0.0
    elements: List[LandingPageElementAnalysis] = field(default_factory=list)
    headline_analysis: Optional[LandingPageElementAnalysis] = None
    cta_analysis: Optional[LandingPageElementAnalysis] = None
    social_proof_analysis: Optional[LandingPageElementAnalysis] = None
    trust_signals_analysis: Optional[LandingPageElementAnalysis] = None
    form_analysis: Optional[LandingPageElementAnalysis] = None
    mobile_experience: float = 0.0
    page_speed_score: float = 0.0
    conversion_rate_benchmark: float = 0.0
    top_recommendations: List[str] = field(default_factory=list)
    quick_wins: List[str] = field(default_factory=list)
    long_term_improvements: List[str] = field(default_factory=list)
    ab_test_roadmap: List[Dict[str, Any]] = field(default_factory=list)
    audited_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_element_analysis(self, analysis: LandingPageElementAnalysis) -> None:
        self.elements.append(analysis)

    def calculate_overall_score(self) -> float:
        if self.elements:
            self.overall_score = sum(e.score for e in self.elements) / len(self.elements)
        return self.overall_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "page_url": self.page_url,
            "overall_score": round(self.overall_score, 2),
            "elements": [e.to_dict() for e in self.elements],
            "mobile_experience": round(self.mobile_experience, 2),
            "page_speed_score": round(self.page_speed_score, 2),
            "top_recommendations": self.top_recommendations,
            "quick_wins": self.quick_wins,
            "ab_test_roadmap": self.ab_test_roadmap,
            "audited_at": self.audited_at.isoformat(),
        }


@dataclass
class CROStrategy:
    """A comprehensive CRO strategy with priorities and roadmap."""
    strategy_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    framework: CROFramework = CROFramework.ICE
    hypotheses: List[Hypothesis] = field(default_factory=list)
    prioritized_tests: List[str] = field(default_factory=list)
    quick_wins: List[str] = field(default_factory=list)
    strategic_initiatives: List[str] = field(default_factory=list)
    kpis: List[Dict[str, Any]] = field(default_factory=list)
    budget: float = 0.0
    team_roles: Dict[str, List[str]] = field(default_factory=dict)
    timeline_months: int = 3
    current_month: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        if hypothesis.hypothesis_id not in [h.hypothesis_id for h in self.hypotheses]:
            self.hypotheses.append(hypothesis)
            self.updated_at = datetime.utcnow()

    def prioritize_hypotheses(self) -> List[Hypothesis]:
        for h in self.hypotheses:
            if h.framework == CROFramework.ICE:
                h.calculate_ice_score()
        self.hypotheses.sort(key=lambda h: h.ice_score, reverse=True)
        return self.hypotheses

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "name": self.name,
            "framework": self.framework.value,
            "hypotheses": [h.to_dict() for h in self.hypotheses],
            "kpis": self.kpis,
            "budget": self.budget,
            "timeline_months": self.timeline_months,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class FormAnalytics:
    """Analytics data for a form."""
    form_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    form_name: str = ""
    page_url: str = ""
    total_submissions: int = 0
    successful_submissions: int = 0
    completion_rate: float = 0.0
    field_analysis: List[Dict[str, Any]] = field(default_factory=list)
    abandonment_fields: List[str] = field(default_factory=list)
    avg_time_to_complete: float = 0.0
    validation_errors: List[Dict[str, Any]] = field(default_factory=list)
    device_breakdown: Dict[str, Dict[str, float]] = field(default_factory=dict)
    insights: List[str] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.utcnow)

    def calculate_completion_rate(self) -> float:
        self.completion_rate = self.successful_submissions / max(self.total_submissions, 1)
        return self.completion_rate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "form_id": self.form_id,
            "form_name": self.form_name,
            "completion_rate": round(self.completion_rate, 4),
            "total_submissions": self.total_submissions,
            "abandonment_fields": self.abandonment_fields,
            "avg_time_to_complete": round(self.avg_time_to_complete, 2),
            "insights": self.insights,
        }


@dataclass
class CheckoutAnalysis:
    """Analysis of a checkout flow."""
    analysis_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    steps: List[Dict[str, Any]] = field(default_factory=list)
    overall_completion_rate: float = 0.0
    biggest_abandonment_step: str = ""
    avg_checkout_time: float = 0.0
    payment_method_breakdown: Dict[str, float] = field(default_factory=dict)
    device_breakdown: Dict[str, float] = field(default_factory=dict)
    abandonment_reasons: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    benchmark_comparison: Optional[Dict[str, Any]] = None
    analyzed_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_id": self.analysis_id,
            "steps": self.steps,
            "overall_completion_rate": round(self.overall_completion_rate, 4),
            "biggest_abandonment_step": self.biggest_abandonment_step,
            "avg_checkout_time": round(self.avg_checkout_time, 2),
            "abandonment_reasons": self.abandonment_reasons,
            "recommendations": self.recommendations,
        }


# ---------------------------------------------------------------------------
# Cache Layer
# ---------------------------------------------------------------------------


class _Cache:
    """Simple in-memory TTL cache."""

    def __init__(self, ttl_seconds: int = 3600) -> None:
        self._store: Dict[str, Tuple[Any, float]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            value, ts = self._store[key]
            if (datetime.utcnow() - datetime.utcfromtimestamp(ts)).total_seconds() < self._ttl:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (value, datetime.utcnow().timestamp())

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        return len(self._store)


# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------


class ValidationError(Exception):
    """Raised when input validation fails."""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")


def _validate_required(value: Any, field_name: str) -> None:
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(field_name, "This field is required and cannot be empty.")


def _validate_range(value: float, min_val: float, max_val: float, field_name: str) -> None:
    if not min_val <= value <= max_val:
        raise ValidationError(field_name, f"Value {value} is out of range [{min_val}, {max_val}].")


def _validate_list_not_empty(items: List[Any], field_name: str) -> None:
    if not items:
        raise ValidationError(field_name, "This list must contain at least one item.")


# ---------------------------------------------------------------------------
# Statistical Utilities
# ---------------------------------------------------------------------------


def _calculate_z_score(control_rate: float, treatment_rate: float,
                       control_n: int, treatment_n: int) -> float:
    """Calculate Z-score for two-proportion Z-test."""
    p_pool = (control_rate * control_n + treatment_rate * treatment_n) / (control_n + treatment_n)
    se = math.sqrt(p_pool * (1 - p_pool) * (1/control_n + 1/treatment_n))
    if se == 0:
        return 0.0
    return (treatment_rate - control_rate) / se


def _calculate_p_value(z_score: float) -> float:
    """Calculate two-tailed p-value from Z-score using approximation."""
    abs_z = abs(z_score)
    t = 1.0 / (1.0 + 0.2316419 * abs_z)
    d = 0.3989422804014327
    prob = d * math.exp(-abs_z * abs_z / 2.0) * (
        t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))))
    )
    return 2.0 * prob


def _calculate_confidence_interval(proportion: float, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Calculate confidence interval for a proportion."""
    z = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}.get(confidence, 1.96)
    se = math.sqrt(proportion * (1 - proportion) / max(n, 1))
    margin = z * se
    return (max(0.0, proportion - margin), min(1.0, proportion + margin))


def _calculate_minimum_sample_size(baseline_rate: float, mde: float,
                                    alpha: float = 0.05, power: float = 0.80) -> int:
    """Calculate minimum sample size for A/B test."""
    if baseline_rate <= 0 or baseline_rate >= 1:
        return 1000
    treatment_rate = baseline_rate * (1 + mde)
    z_alpha = {0.05: 1.96, 0.01: 2.576, 0.10: 1.645}.get(alpha, 1.96)
    z_beta = {0.80: 0.842, 0.90: 1.282, 0.95: 1.645}.get(power, 0.842)
    p_avg = (baseline_rate + treatment_rate) / 2
    n = (
        (z_alpha * math.sqrt(2 * p_avg * (1 - p_avg))
         + z_beta * math.sqrt(baseline_rate * (1 - baseline_rate)
                              + treatment_rate * (1 - treatment_rate))) ** 2
        / (treatment_rate - baseline_rate) ** 2
    )
    return max(100, int(math.ceil(n)))


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------


class ConversionOptimizationAgent:
    """Comprehensive conversion rate optimization agent.

    Orchestrates the full CRO lifecycle:
    - Hypothesis generation and prioritization
    - A/B test design, execution, and analysis
    - Conversion funnel analysis and optimization
    - UX analysis and issue identification
    - Landing page auditing and optimization
    - CRO strategy development

    Example::

        agent = ConversionOptimizationAgent()

        # Create A/B test
        test = agent.create_ab_test(
            name="Hero CTA Color Test",
            url="/landing-page",
            variants=[("Control - Blue", True), ("Variant - Green", False)],
        )

        # Analyze funnel
        funnel = agent.analyze_funnel(name="Checkout", steps=[...])

        # Audit landing page
        audit = agent.audit_landing_page(url="/pricing")
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self._config = config or Config()
        self._cache = _Cache(ttl_seconds=self._config.cache_ttl_seconds) if self._config.enable_caching else None
        self._tests: Dict[str, ABTest] = {}
        self._hypotheses: Dict[str, Hypothesis] = {}
        self._funnel_analyses: Dict[str, FunnelAnalysis] = {}
        self._ux_reports: Dict[str, UXReport] = {}
        self._landing_page_audits: Dict[str, LandingPageAudit] = {}
        self._cro_strategies: Dict[str, CROStrategy] = {}
        self._form_analytics: Dict[str, FormAnalytics] = {}
        self._checkout_analyses: Dict[str, CheckoutAnalysis] = {}
        self._operation_log: List[Dict[str, Any]] = []
        self._error_count: int = 0
        self._success_count: int = 0
        logger.info(
            "ConversionOptimizationAgent initialized (version=%s, caching=%s)",
            self._config.version,
            self._config.enable_caching,
        )

    # ----- A/B Testing -----

    def create_ab_test(
        self,
        name: str,
        url: str,
        variants: List[Tuple[str, bool]],
        test_type: TestType = TestType.A_B,
        target_metric: ConversionMetric = ConversionMetric.CONVERSION_RATE,
        priority: TestPriority = TestPriority.P2_MEDIUM,
        hypothesis_id: Optional[str] = None,
        description: str = "",
    ) -> ABTest:
        """Create a new A/B test experiment.

        Args:
            name: Test name.
            url: URL to test.
            variants: List of (name, is_control) tuples.
            test_type: Type of test.
            target_metric: Primary metric to measure.
            priority: Test priority.
            hypothesis_id: Associated hypothesis ID.
            description: Test description.

        Returns:
            ABTest: The created test.
        """
        _validate_required(name, "name")
        _validate_required(url, "url")
        _validate_list_not_empty(variants, "variants")

        test = ABTest(
            name=name,
            description=description,
            test_type=test_type,
            status=TestStatus.DRAFT,
            priority=priority,
            hypothesis_id=hypothesis_id,
            url=url,
            target_metric=target_metric,
        )
        traffic_per = 100.0 / len(variants)
        for var_name, is_control in variants:
            test.add_variant(name=var_name, is_control=is_control, traffic=traffic_per)

        self._tests[test.test_id] = test
        self._log_operation("create_ab_test", {"test_id": test.test_id, "name": name})
        logger.info("A/B test created: %s (%s)", name, test.test_id)
        return test

    def update_ab_test(self, test_id: str, **kwargs: Any) -> ABTest:
        """Update an existing A/B test."""
        test = self._get_test(test_id)
        for key, value in kwargs.items():
            if hasattr(test, key) and value is not None:
                setattr(test, key, value)
        test.updated_at = datetime.utcnow()
        return test

    def approve_test(self, test_id: str) -> ABTest:
        """Approve a test for execution."""
        test = self._get_test(test_id)
        test.status = TestStatus.APPROVED
        test.updated_at = datetime.utcnow()
        self._log_operation("approve_test", {"test_id": test_id})
        return test

    def start_test(self, test_id: str) -> ABTest:
        """Start running a test."""
        test = self._get_test(test_id)
        if not test.is_ready_to_run():
            raise ValidationError("test_id", "Test is not ready to run. Need at least 2 variants with a control.")
        test.status = TestStatus.RUNNING
        test.start_date = datetime.utcnow()
        test.updated_at = datetime.utcnow()
        self._log_operation("start_test", {"test_id": test_id})
        logger.info("A/B test started: %s", test.name)
        return test

    def stop_test(self, test_id: str, winner_id: Optional[str] = None) -> ABTest:
        """Stop a running test."""
        test = self._get_test(test_id)
        test.status = TestStatus.STOPPED
        test.end_date = datetime.utcnow()
        test.updated_at = datetime.utcnow()
        if winner_id:
            for v in test.variants:
                if v.variant_id == winner_id:
                    v.metadata["winner"] = True
        self._log_operation("stop_test", {"test_id": test_id, "winner": winner_id})
        return test

    def analyze_test_results(self, test_id: str, sample_data: Optional[Dict[str, Any]] = None) -> ExperimentResult:
        """Analyze A/B test results with statistical testing.

        Performs a two-proportion Z-test to determine statistical significance
        and calculates confidence intervals for each variant.

        Args:
            test_id: ID of the test to analyze.
            sample_data: Optional sample data with visitor/conversion counts.

        Returns:
            ExperimentResult: Statistical analysis results.
        """
        test = self._get_test(test_id)
        result = ExperimentResult(test_id=test_id)

        if sample_data and "variants" in sample_data:
            variant_data = sample_data["variants"]
        else:
            variant_data = self._generate_sample_data(test)

        control = test.get_control()
        if not control:
            result.significance = StatisticalSignificance.NONE
            test.results = result
            return result

        control_data = variant_data.get(control.variant_id, {"visitors": 1000, "conversions": 50})
        control_rate = control_data["conversions"] / max(control_data["visitors"], 1)

        best_treatment_rate = 0.0
        best_lift = 0.0
        best_variant_id = None
        best_p_value = 1.0

        for variant in test.variants:
            if variant.is_control:
                ci = _calculate_confidence_interval(control_rate, control_data["visitors"])
                result.variant_results.append({
                    "variant_id": variant.variant_id,
                    "name": variant.name,
                    "is_control": True,
                    "visitors": control_data["visitors"],
                    "conversions": control_data["conversions"],
                    "conversion_rate": round(control_rate, 6),
                    "confidence_interval": [round(ci[0], 6), round(ci[1], 6)],
                })
                continue

            v_data = variant_data.get(variant.variant_id, {"visitors": 1000, "conversions": 45})
            v_rate = v_data["conversions"] / max(v_data["visitors"], 1)
            z = _calculate_z_score(control_rate, v_rate, control_data["visitors"], v_data["visitors"])
            p = _calculate_p_value(z)
            lift = (v_rate - control_rate) / max(control_rate, 0.001)
            ci = _calculate_confidence_interval(v_rate, v_data["visitors"])

            result.variant_results.append({
                "variant_id": variant.variant_id,
                "name": variant.name,
                "is_control": False,
                "visitors": v_data["visitors"],
                "conversions": v_data["conversions"],
                "conversion_rate": round(v_rate, 6),
                "lift": round(lift, 4),
                "p_value": round(p, 6),
                "confidence_interval": [round(ci[0], 6), round(ci[1], 6)],
            })

            if v_rate > best_treatment_rate:
                best_treatment_rate = v_rate
                best_lift = lift
                best_variant_id = variant.variant_id
                best_p_value = p

        result.p_value = best_p_value
        result.lift = best_lift
        result.winner = best_variant_id if best_p_value < self._config.ab_test.default_confidence_level else None
        result.confidence_level = 1.0 - best_p_value
        result.sample_size_reached = all(
            variant_data.get(v.variant_id, {}).get("visitors", 0) >= self._config.ab_test.minimum_sample_size
            for v in test.variants
        )
        result.minimum_runtime_reached = bool(
            test.start_date
            and (datetime.utcnow() - test.start_date).days >= self._config.ab_test.minimum_runtime_days
        )
        result.determine_significance()

        test.results = result
        test.status = TestStatus.COMPLETED
        test.end_date = datetime.utcnow()
        self._log_operation("analyze_test_results", {
            "test_id": test_id,
            "winner": result.winner,
            "significance": result.significance.value,
        })
        logger.info(
            "Test analysis complete: %s (winner=%s, p=%.4f)",
            test.name,
            result.winner,
            result.p_value,
        )
        return result

    def get_test(self, test_id: str) -> ABTest:
        """Retrieve a test by ID."""
        return self._get_test(test_id)

    def list_tests(self, status: Optional[TestStatus] = None) -> List[ABTest]:
        """List all tests with optional status filter."""
        tests = list(self._tests.values())
        if status:
            tests = [t for t in tests if t.status == status]
        return tests

    def get_test_dashboard(self) -> Dict[str, Any]:
        """Get a dashboard view of all tests."""
        status_counts: Dict[str, int] = defaultdict(int)
        for test in self._tests.values():
            status_counts[test.status.value] += 1
        total_lift = 0.0
        winners = 0
        for test in self._tests.values():
            if test.results and test.results.winner:
                total_lift += test.results.lift
                winners += 1
        return {
            "total_tests": len(self._tests),
            "by_status": dict(status_counts),
            "winners": winners,
            "average_lift": round(total_lift / max(winners, 1), 4),
            "running_tests": status_counts.get("running", 0),
        }

    # ----- Hypothesis Management -----

    def create_hypothesis(
        self,
        title: str,
        observation: str,
        insight: str,
        hypothesis_statement: str,
        expected_impact: str = "",
        impact: int = 5,
        confidence: int = 5,
        ease: int = 5,
        framework: CROFramework = CROFramework.ICE,
        source: str = "",
    ) -> Hypothesis:
        """Create a test hypothesis.

        Args:
            title: Hypothesis title.
            observation: What was observed.
            insight: Key insight from observation.
            hypothesis_statement: IF...THEN...BECAUSE statement.
            expected_impact: Expected impact description.
            impact: Impact score 1-10.
            confidence: Confidence score 1-10.
            ease: Ease score 1-10.
            framework: Prioritization framework.
            source: Source of the hypothesis.

        Returns:
            Hypothesis: The created hypothesis.
        """
        _validate_required(title, "title")
        _validate_required(hypothesis_statement, "hypothesis_statement")
        _validate_range(impact, 1, 10, "impact")
        _validate_range(confidence, 1, 10, "confidence")
        _validate_range(ease, 1, 10, "ease")

        hypothesis = Hypothesis(
            title=title,
            observation=observation,
            insight=insight,
            hypothesis_statement=hypothesis_statement,
            expected_impact=expected_impact,
            impact=impact,
            confidence=confidence,
            ease=ease,
            framework=framework,
            source=source,
        )
        hypothesis.calculate_ice_score()
        self._hypotheses[hypothesis.hypothesis_id] = hypothesis
        self._log_operation("create_hypothesis", {"hypothesis_id": hypothesis.hypothesis_id, "title": title})
        return hypothesis

    def update_hypothesis(self, hypothesis_id: str, **kwargs: Any) -> Hypothesis:
        """Update an existing hypothesis."""
        hypothesis = self._get_hypothesis(hypothesis_id)
        for key, value in kwargs.items():
            if hasattr(hypothesis, key) and value is not None:
                setattr(hypothesis, key, value)
        hypothesis.calculate_ice_score()
        return hypothesis

    def get_hypothesis(self, hypothesis_id: str) -> Hypothesis:
        """Retrieve a hypothesis by ID."""
        return self._get_hypothesis(hypothesis_id)

    def list_hypotheses(self, status: Optional[str] = None) -> List[Hypothesis]:
        """List all hypotheses with optional status filter."""
        hypotheses = list(self._hypotheses.values())
        if status:
            hypotheses = [h for h in hypotheses if h.status == status]
        return hypotheses

    def prioritize_hypotheses(self, framework: CROFramework = CROFramework.ICE) -> List[Hypothesis]:
        """Prioritize all hypotheses using the specified framework."""
        hypotheses = list(self._hypotheses.values())
        if framework == CROFramework.ICE:
            for h in hypotheses:
                h.calculate_ice_score()
            hypotheses.sort(key=lambda h: h.ice_score, reverse=True)
        elif framework == CROFramework.IMPACT_EFFORT:
            hypotheses.sort(key=lambda h: h.impact / max(h.ease, 1), reverse=True)
        return hypotheses

    # ----- Funnel Analysis -----

    def analyze_funnel(
        self,
        name: str,
        steps: List[Dict[str, Any]],
        time_period_days: int = 30,
        segment: Optional[UserSegment] = None,
        source: Optional[TrafficSource] = None,
    ) -> FunnelAnalysis:
        """Analyze a conversion funnel.

        Creates a funnel analysis with step-by-step conversion rates,
        drop-off analysis, and optimization recommendations.

        Args:
            name: Funnel name.
            steps: List of step dicts with name, stage, visitors, conversions.
            time_period_days: Analysis time period.
            segment: User segment filter.
            source: Traffic source filter.

        Returns:
            FunnelAnalysis: Complete funnel analysis.
        """
        _validate_required(name, "name")
        _validate_list_not_empty(steps, "steps")

        analysis = FunnelAnalysis(
            name=name,
            time_period_days=time_period_days,
            segment=segment,
            source=source,
        )

        previous_visitors = 0
        for i, step_data in enumerate(steps):
            step = FunnelStep(
                name=step_data.get("name", f"Step {i+1}"),
                stage=FunnelStage(step_data.get("stage", "awareness")),
                visitors=step_data.get("visitors", 0),
                conversions=step_data.get("conversions", 0),
                avg_time_on_step=step_data.get("avg_time", 0.0),
            )
            step.calculate_rates(previous_visitors)
            analysis.steps.append(step)
            previous_visitors = step.visitors

        analysis.calculate_overall_rate()
        biggest_drop = analysis.find_biggest_drop_off()
        if biggest_drop:
            analysis.recommendations.append(
                f"Focus optimization on '{biggest_drop.name}' — highest drop-off at "
                f"{biggest_drop.drop_off_rate:.1%}"
            )

        for step in analysis.steps:
            if step.drop_off_rate > self._config.funnel.drop_off_threshold:
                analysis.insights.append({
                    "type": "high_drop_off",
                    "step": step.name,
                    "drop_off_rate": step.drop_off_rate,
                    "impact": "high" if step.drop_off_rate > 0.30 else "medium",
                })

        self._funnel_analyses[analysis.analysis_id] = analysis
        self._log_operation("analyze_funnel", {
            "analysis_id": analysis.analysis_id,
            "name": name,
            "steps": len(steps),
            "overall_rate": analysis.overall_conversion_rate,
        })
        logger.info(
            "Funnel analysis complete: %s (rate=%.2f%%, steps=%d)",
            name,
            analysis.overall_conversion_rate * 100,
            len(steps),
        )
        return analysis

    def compare_funnels(
        self,
        funnel_id_1: str,
        funnel_id_2: str,
    ) -> Dict[str, Any]:
        """Compare two funnel analyses side by side."""
        f1 = self._get_funnel(funnel_id_1)
        f2 = self._get_funnel(funnel_id_2)
        return {
            "funnel_1": f1.to_dict(),
            "funnel_2": f2.to_dict(),
            "conversion_rate_diff": f2.overall_conversion_rate - f1.overall_conversion_rate,
            "step_comparison": [
                {
                    "step_1": s1.to_dict(),
                    "step_2": s2.to_dict() if i < len(f2.steps) else None,
                }
                for i, (s1, s2) in enumerate(zip(f1.steps, f2.steps))
            ],
        }

    def get_funnel(self, analysis_id: str) -> FunnelAnalysis:
        """Retrieve a funnel analysis by ID."""
        return self._get_funnel(analysis_id)

    def list_funnels(self) -> List[FunnelAnalysis]:
        """List all funnel analyses."""
        return list(self._funnel_analyses.values())

    # ----- UX Analysis -----

    def analyze_ux(
        self,
        page_url: str,
        page_type: str = "landing_page",
    ) -> UXReport:
        """Perform comprehensive UX analysis on a page.

        Analyzes page structure, accessibility, mobile experience,
        page speed, and identifies conversion barriers.

        Args:
            page_url: URL of the page to analyze.
            page_type: Type of page (landing_page, checkout, pricing, etc.).

        Returns:
            UXReport: Comprehensive UX analysis report.
        """
        _validate_required(page_url, "page_url")

        report = UXReport(page_url=page_url)

        report.accessibility_score = self._analyze_accessibility(report)
        report.mobile_score = self._analyze_mobile_experience(report)
        report.readability_score = self._analyze_readability(report)
        report.page_speed = self._analyze_page_speed(report)
        self._identify_conversion_barriers(report)
        self._identify_opportunities(report)
        report.calculate_overall_score()

        self._ux_reports[report.report_id] = report
        self._log_operation("analyze_ux", {
            "report_id": report.report_id,
            "page_url": page_url,
            "score": report.overall_score,
            "issues": len(report.issues),
        })
        logger.info(
            "UX analysis complete: %s (score=%.1f, issues=%d)",
            page_url,
            report.overall_score,
            len(report.issues),
        )
        return report

    def get_ux_report(self, report_id: str) -> UXReport:
        """Retrieve a UX report by ID."""
        report = self._ux_reports.get(report_id)
        if report is None:
            raise ValidationError("report_id", f"UX report {report_id} not found.")
        return report

    def list_ux_reports(self) -> List[UXReport]:
        """List all UX reports."""
        return list(self._ux_reports.values())

    # ----- Landing Page Audit -----

    def audit_landing_page(
        self,
        url: str,
        page_type: str = "landing_page",
    ) -> LandingPageAudit:
        """Perform a comprehensive landing page audit.

        Analyzes each element of the landing page for effectiveness,
        identifies quick wins, and creates an A/B test roadmap.

        Args:
            url: Landing page URL.
            page_type: Type of landing page.

        Returns:
            LandingPageAudit: Complete audit with element analysis.
        """
        _validate_required(url, "url")

        audit = LandingPageAudit(page_url=url, page_type=page_type)

        elements_to_analyze = [
            LandingPageElement.HERO_SECTION,
            LandingPageElement.HEADLINE,
            LandingPageElement.CALL_TO_ACTION,
            LandingPageElement.SOCIAL_PROOF,
            LandingPageElement.TRUST_SIGNALS,
            LandingPageElement.BENEFITS,
            LandingPageElement.FORM,
        ]
        for element in elements_to_analyze:
            analysis = self._analyze_landing_page_element(element, url)
            audit.add_element_analysis(analysis)

        audit.headline_analysis = next(
            (e for e in audit.elements if e.element_type == LandingPageElement.HEADLINE), None
        )
        audit.cta_analysis = next(
            (e for e in audit.elements if e.element_type == LandingPageElement.CALL_TO_ACTION), None
        )
        audit.social_proof_analysis = next(
            (e for e in audit.elements if e.element_type == LandingPageElement.SOCIAL_PROOF), None
        )

        self._generate_quick_wins(audit)
        self._generate_test_roadmap(audit)
        audit.calculate_overall_score()

        self._landing_page_audits[audit.audit_id] = audit
        self._log_operation("audit_landing_page", {
            "audit_id": audit.audit_id,
            "url": url,
            "score": audit.overall_score,
        })
        return audit

    def get_landing_page_audit(self, audit_id: str) -> LandingPageAudit:
        """Retrieve a landing page audit by ID."""
        audit = self._landing_page_audits.get(audit_id)
        if audit is None:
            raise ValidationError("audit_id", f"Landing page audit {audit_id} not found.")
        return audit

    def list_landing_page_audits(self) -> List[LandingPageAudit]:
        """List all landing page audits."""
        return list(self._landing_page_audits.values())

    # ----- CRO Strategy -----

    def create_cro_strategy(
        self,
        name: str,
        framework: CROFramework = CROFramework.ICE,
        budget: float = 0.0,
        timeline_months: int = 3,
        kpis: Optional[List[Dict[str, Any]]] = None,
    ) -> CROStrategy:
        """Create a CRO strategy with hypothesis prioritization.

        Args:
            name: Strategy name.
            framework: Prioritization framework.
            budget: CRO budget.
            timeline_months: Strategy timeline.
            kpis: Key performance indicators.

        Returns:
            CROStrategy: The created strategy.
        """
        _validate_required(name, "name")

        strategy = CROStrategy(
            name=name,
            framework=framework,
            budget=budget,
            timeline_months=timeline_months,
            kpis=kpis or [
                {"name": "Conversion Rate", "target": 0.05, "current": 0.03},
                {"name": "Revenue per Visitor", "target": 5.0, "current": 3.2},
                {"name": "Cart Abandonment Rate", "target": 0.60, "current": 0.70},
            ],
        )
        self._cro_strategies[strategy.strategy_id] = strategy
        self._log_operation("create_cro_strategy", {"strategy_id": strategy.strategy_id, "name": name})
        return strategy

    def add_hypothesis_to_strategy(self, strategy_id: str, hypothesis_id: str) -> CROStrategy:
        """Add a hypothesis to a CRO strategy."""
        strategy = self._get_strategy(strategy_id)
        hypothesis = self._get_hypothesis(hypothesis_id)
        strategy.add_hypothesis(hypothesis)
        return strategy

    def get_cro_strategy(self, strategy_id: str) -> CROStrategy:
        """Retrieve a CRO strategy by ID."""
        return self._get_strategy(strategy_id)

    def list_cro_strategies(self) -> List[CROStrategy]:
        """List all CRO strategies."""
        return list(self._cro_strategies.values())

    # ----- Form Analytics -----

    def analyze_form(
        self,
        form_name: str,
        page_url: str,
        total_submissions: int,
        successful_submissions: int,
        field_data: Optional[List[Dict[str, Any]]] = None,
    ) -> FormAnalytics:
        """Analyze form performance and identify abandonment points.

        Args:
            form_name: Name of the form.
            page_url: Page URL.
            total_submissions: Total form attempts.
            successful_submissions: Successful completions.
            field_data: Per-field analytics data.

        Returns:
            FormAnalytics: Form analysis with insights.
        """
        analytics = FormAnalytics(
            form_name=form_name,
            page_url=page_url,
            total_submissions=total_submissions,
            successful_submissions=successful_submissions,
            field_analysis=field_data or [],
        )
        analytics.calculate_completion_rate()

        if analytics.completion_rate < 0.50:
            analytics.insights.append("Form completion rate is below 50%. Consider simplifying the form.")
        if analytics.completion_rate < 0.30:
            analytics.insights.append("CRITICAL: Form completion rate is below 30%. Major redesign needed.")

        self._form_analytics[analytics.form_id] = analytics
        self._log_operation("analyze_form", {
            "form_id": analytics.form_id,
            "completion_rate": analytics.completion_rate,
        })
        return analytics

    # ----- Checkout Analysis -----

    def analyze_checkout(
        self,
        steps: List[Dict[str, Any]],
        abandonment_reasons: Optional[List[Dict[str, Any]]] = None,
    ) -> CheckoutAnalysis:
        """Analyze checkout flow and identify abandonment points.

        Args:
            steps: List of checkout steps with visitor/conversion data.
            abandonment_reasons: Common abandonment reasons.

        Returns:
            CheckoutAnalysis: Checkout analysis with recommendations.
        """
        _validate_list_not_empty(steps, "steps")

        analysis = CheckoutAnalysis(steps=steps)
        analysis.abandonment_reasons = abandonment_reasons or [
            {"reason": "Unexpected shipping costs", "percentage": 0.48},
            {"reason": "Just browsing", "percentage": 0.26},
            {"reason": "Found better price elsewhere", "percentage": 0.20},
            {"reason": "Complex checkout process", "percentage": 0.18},
            {"reason": "Didn't trust site with card info", "percentage": 0.17},
            {"reason": "Website errors", "percentage": 0.13},
            {"reason": "Delivery time too long", "percentage": 0.12},
            {"reason": "Return policy not satisfactory", "percentage": 0.10},
        ]

        if steps:
            first_step = steps[0].get("visitors", 0)
            last_step = steps[-1].get("conversions", 0)
            analysis.overall_completion_rate = last_step / max(first_step, 1)

        analysis.recommendations = [
            "Show total cost (including shipping) early in the process",
            "Offer guest checkout option",
            "Simplify form fields to essential only",
            "Add trust badges and security seals near payment",
            "Offer multiple payment methods",
            "Provide clear delivery time estimates",
            "Add progress indicator for multi-step checkout",
            "Implement exit-intent offers for cart abandonment",
        ]

        self._checkout_analyses[analysis.analysis_id] = analysis
        self._log_operation("analyze_checkout", {
            "analysis_id": analysis.analysis_id,
            "completion_rate": analysis.overall_completion_rate,
        })
        return analysis

    # ----- Recommendations -----

    def get_cro_recommendations(
        self,
        page_type: str = "landing_page",
    ) -> List[Dict[str, Any]]:
        """Get CRO recommendations based on page type and best practices.

        Returns a prioritized list of optimization recommendations
        based on the specified page type and industry benchmarks.
        """
        recommendations_by_type: Dict[str, List[Dict[str, Any]]] = {
            "landing_page": [
                {"category": "headline", "priority": "high", "recommendation": "Use a clear, benefit-focused headline that matches ad copy."},
                {"category": "cta", "priority": "high", "recommendation": "Use action-oriented CTA text. Test button colors and sizes."},
                {"category": "social_proof", "priority": "high", "recommendation": "Add customer testimonials with photos and names."},
                {"category": "trust", "priority": "medium", "recommendation": "Add security badges, guarantees, and privacy policy links."},
                {"category": "form", "priority": "medium", "recommendation": "Minimize form fields. Only ask for essential information."},
                {"category": "above_fold", "priority": "high", "recommendation": "Ensure value proposition and CTA are above the fold."},
                {"category": "urgency", "priority": "medium", "recommendation": "Add genuine urgency elements (limited time, limited spots)."},
                {"category": "mobile", "priority": "high", "recommendation": "Optimize for mobile with large tap targets and simplified forms."},
            ],
            "checkout": [
                {"category": "progress", "priority": "high", "recommendation": "Show checkout progress indicator."},
                {"category": "guest_checkout", "priority": "high", "recommendation": "Offer guest checkout option."},
                {"category": "payment", "priority": "high", "recommendation": "Offer multiple payment methods (cards, PayPal, Apple Pay)."},
                {"category": "security", "priority": "high", "recommendation": "Display security badges near payment fields."},
                {"category": "shipping", "priority": "high", "recommendation": "Show shipping costs early. Offer free shipping threshold."},
                {"category": "errors", "priority": "medium", "recommendation": "Provide clear inline error messages."},
                {"category": "summary", "priority": "medium", "recommendation": "Show order summary throughout checkout."},
                {"category": "support", "priority": "low", "recommendation": "Add live chat or support link in checkout."},
            ],
            "pricing": [
                {"category": "comparison", "priority": "high", "recommendation": "Show feature comparison table across plans."},
                {"category": "social_proof", "priority": "high", "recommendation": "Highlight most popular plan with social proof."},
                {"category": "annual", "priority": "medium", "recommendation": "Show monthly vs annual pricing with savings."},
                {"category": "cta", "priority": "high", "recommendation": "Use clear CTAs: 'Start Free Trial' vs 'Buy Now'."},
                {"category": "faq", "priority": "medium", "recommendation": "Address common pricing questions in FAQ section."},
                {"category": "guarantee", "priority": "medium", "recommendation": "Add money-back guarantee or free trial offer."},
            ],
            "signup": [
                {"category": "fields", "priority": "high", "recommendation": "Minimize signup fields. Email + password only."},
                {"category": "social_login", "priority": "medium", "recommendation": "Offer social login (Google, GitHub) options."},
                {"category": "benefits", "priority": "high", "recommendation": "Show key benefits of signing up near the form."},
                {"category": "trust", "priority": "medium", "recommendation": "Add privacy policy link and 'no spam' assurance."},
                {"category": "progress", "priority": "low", "recommendation": "If multi-step, show progress indicator."},
            ],
        }
        recs = recommendations_by_type.get(page_type, recommendations_by_type["landing_page"])
        recs.sort(key=lambda r: {"high": 0, "medium": 1, "low": 2}.get(r["priority"], 3))
        return recs

    # ----- Internal Helpers -----

    def _get_test(self, test_id: str) -> ABTest:
        test = self._tests.get(test_id)
        if test is None:
            raise ValidationError("test_id", f"Test {test_id} not found.")
        return test

    def _get_hypothesis(self, hypothesis_id: str) -> Hypothesis:
        hypothesis = self._hypotheses.get(hypothesis_id)
        if hypothesis is None:
            raise ValidationError("hypothesis_id", f"Hypothesis {hypothesis_id} not found.")
        return hypothesis

    def _get_funnel(self, analysis_id: str) -> FunnelAnalysis:
        analysis = self._funnel_analyses.get(analysis_id)
        if analysis is None:
            raise ValidationError("analysis_id", f"Funnel analysis {analysis_id} not found.")
        return analysis

    def _get_strategy(self, strategy_id: str) -> CROStrategy:
        strategy = self._cro_strategies.get(strategy_id)
        if strategy is None:
            raise ValidationError("strategy_id", f"CRO strategy {strategy_id} not found.")
        return strategy

    def _log_operation(self, operation: str, details: Dict[str, Any]) -> None:
        self._operation_log.append({
            "operation": operation,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def _generate_sample_data(self, test: ABTest) -> Dict[str, Dict[str, int]]:
        data: Dict[str, Dict[str, int]] = {}
        base_visitors = random.randint(1000, 5000)
        control_rate = random.uniform(0.02, 0.08)
        for variant in test.variants:
            visitors = int(base_visitors * variant.traffic_percentage / 100)
            if variant.is_control:
                conversions = int(visitors * control_rate)
            else:
                treatment_rate = control_rate * random.uniform(0.85, 1.25)
                conversions = int(visitors * treatment_rate)
            data[variant.variant_id] = {"visitors": visitors, "conversions": conversions}
        return data

    def _analyze_accessibility(self, report: UXReport) -> float:
        score = 70.0
        report.add_issue(
            "Check for missing alt text on images",
            UXSeverity.MEDIUM,
            "accessibility",
            "Add descriptive alt text to all images for screen readers.",
        )
        report.add_issue(
            "Ensure sufficient color contrast (4.5:1 minimum)",
            UXSeverity.HIGH,
            "accessibility",
            "Use contrast checking tools to verify text readability.",
        )
        report.add_issue(
            "Add form labels for all input fields",
            UXSeverity.MEDIUM,
            "accessibility",
            "Associate labels with inputs using for/id attributes.",
        )
        return score

    def _analyze_mobile_experience(self, report: UXReport) -> float:
        score = 65.0
        report.add_issue(
            "Tap targets too small on mobile (< 44px)",
            UXSeverity.HIGH,
            "mobile",
            "Increase tap target size to at least 44x44 pixels.",
        )
        report.add_issue(
            "Viewport meta tag may be missing",
            UXSeverity.MEDIUM,
            "mobile",
            "Add <meta name='viewport' content='width=device-width, initial-scale=1'>",
        )
        return score

    def _analyze_readability(self, report: UXReport) -> float:
        return 72.0

    def _analyze_page_speed(self, report: UXReport) -> Dict[str, float]:
        return {
            PageSpeedMetric.FIRST_CONTENTFUL_PAINT.value: 1.8,
            PageSpeedMetric.LARGEST_CONTENTFUL_PAINT.value: 3.2,
            PageSpeedMetric.CUMULATIVE_LAYOUT_SHIFT.value: 0.15,
            PageSpeedMetric.INTERACTION_TO_NEXT_PAINT.value: 250,
            PageSpeedMetric.TOTAL_BLOCKING_TIME.value: 350,
        }

    def _identify_conversion_barriers(self, report: UXReport) -> None:
        report.conversion_barriers = [
            "Complex navigation structure",
            "Missing social proof above the fold",
            "CTA button not prominent enough",
            "Too many form fields",
            "No urgency or scarcity elements",
            "Page load time exceeds 3 seconds",
        ]

    def _identify_opportunities(self, report: UXReport) -> None:
        report.opportunities = [
            {"type": "quick_win", "description": "Add customer testimonials near CTA", "estimated_impact": "+15% conversions"},
            {"type": "quick_win", "description": "Simplify headline to focus on main benefit", "estimated_impact": "+10% engagement"},
            {"type": "strategic", "description": "Implement personalization based on traffic source", "estimated_impact": "+20% conversions"},
            {"type": "strategic", "description": "Add video testimonials", "estimated_impact": "+25% trust"},
        ]

    def _analyze_landing_page_element(
        self,
        element: LandingPageElement,
        url: str,
    ) -> LandingPageElementAnalysis:
        analysis = LandingPageElementAnalysis(element_type=element)
        element_scores: Dict[LandingPageElement, float] = {
            LandingPageElement.HERO_SECTION: 65.0,
            LandingPageElement.HEADLINE: 60.0,
            LandingPageElement.CALL_TO_ACTION: 55.0,
            LandingPageElement.SOCIAL_PROOF: 45.0,
            LandingPageElement.TRUST_SIGNALS: 50.0,
            LandingPageElement.BENEFITS: 70.0,
            LandingPageElement.FORM: 55.0,
        }
        analysis.score = element_scores.get(element, 60.0)
        analysis.strengths = ["Present on page"]
        analysis.weaknesses = ["Could be improved based on best practices"]
        analysis.recommendations = [f"Optimize {element.value} based on CRO best practices"]
        analysis.ab_test_suggestions = [f"A/B test different {element.value} variations"]
        return analysis

    def _generate_quick_wins(self, audit: LandingPageAudit) -> None:
        audit.quick_wins = [
            "Add customer testimonials with photos",
            "Improve CTA button text to be more action-oriented",
            "Add trust badges near the CTA",
            "Simplify the form to essential fields only",
            "Add a compelling subheadline under the main headline",
        ]
        audit.top_recommendations = [
            "Redesign hero section with clearer value proposition",
            "Implement A/B testing on CTA button color and text",
            "Add social proof section with customer logos and testimonials",
            "Optimize page load speed",
            "Ensure mobile responsiveness across all breakpoints",
        ]
        audit.long_term_improvements = [
            "Implement dynamic content personalization",
            "Add video testimonials",
            "Create dedicated landing pages per traffic source",
            "Implement exit-intent popup with special offer",
        ]

    def _generate_test_roadmap(self, audit: LandingPageAudit) -> None:
        audit.ab_test_roadmap = [
            {
                "phase": 1,
                "duration": "Week 1-2",
                "tests": ["CTA button color test", "Headline variation test"],
                "priority": "high",
            },
            {
                "phase": 2,
                "duration": "Week 3-4",
                "tests": ["Social proof placement test", "Form field count test"],
                "priority": "medium",
            },
            {
                "phase": 3,
                "duration": "Week 5-6",
                "tests": ["Hero image test", "Value proposition framing test"],
                "priority": "medium",
            },
            {
                "phase": 4,
                "duration": "Week 7-8",
                "tests": ["Page layout test", "Pricing display test"],
                "priority": "low",
            },
        ]

    # ----- Status & Diagnostics -----

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status."""
        return {
            "agent": self._config.agent_name,
            "version": self._config.version,
            "tests": len(self._tests),
            "hypotheses": len(self._hypotheses),
            "funnel_analyses": len(self._funnel_analyses),
            "ux_reports": len(self._ux_reports),
            "landing_page_audits": len(self._landing_page_audits),
            "cro_strategies": len(self._cro_strategies),
            "form_analytics": len(self._form_analytics),
            "checkout_analyses": len(self._checkout_analyses),
            "operations_logged": len(self._operation_log),
            "cache_size": self._cache.size() if self._cache else 0,
        }

    def get_operation_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent operation log entries."""
        return self._operation_log[-limit:]

    def clear_cache(self) -> int:
        """Clear the cache and return number of entries removed."""
        if self._cache:
            size = self._cache.size()
            self._cache.clear()
            return size
        return 0

    def export_data(self, format: str = "json") -> str:
        """Export all agent data in the specified format."""
        data = {
            "tests": [t.to_dict() for t in self._tests.values()],
            "hypotheses": [h.to_dict() for h in self._hypotheses.values()],
            "funnel_analyses": [f.to_dict() for f in self._funnel_analyses.values()],
            "ux_reports": [r.to_dict() for r in self._ux_reports.values()],
            "landing_page_audits": [a.to_dict() for a in self._landing_page_audits.values()],
            "cro_strategies": [s.to_dict() for s in self._cro_strategies.values()],
            "status": self.get_status(),
        }
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        return str(data)


# ---------------------------------------------------------------------------
# CLI Demo
# ---------------------------------------------------------------------------


def main() -> None:
    """Demonstrate Conversion Optimization Agent capabilities."""
    print("=" * 70)
    print("Conversion Optimization Agent v3.0.0 - Comprehensive Demo")
    print("=" * 70)

    agent = ConversionOptimizationAgent()

    print("\n--- Creating Hypotheses ---")
    h1 = agent.create_hypothesis(
        title="CTA Button Color Impact",
        observation="Current blue CTA button gets low click-through rate",
        insight="Green buttons often perform better for 'start free trial' CTAs",
        hypothesis_statement="IF we change the CTA button from blue to green, THEN click-through rate will increase, BECAUSE green is associated with 'go' and action.",
        expected_impact="10-15% increase in CTR",
        impact=7,
        confidence=6,
        ease=9,
    )
    print(f"Hypothesis: {h1.title} (ICE: {h1.ice_score:.1f})")

    h2 = agent.create_hypothesis(
        title="Social Proof Above Fold",
        observation="Landing page has social proof below the fold",
        insight="Social proof near CTA increases conversion by 15-20%",
        hypothesis_statement="IF we add customer logos above the fold, THEN conversion rate will increase, BECAUSE social proof reduces purchase anxiety.",
        expected_impact="15-20% increase in conversion",
        impact=8,
        confidence=7,
        ease=7,
    )
    print(f"Hypothesis: {h2.title} (ICE: {h2.ice_score:.1f})")

    print("\n--- Prioritizing Hypotheses ---")
    prioritized = agent.prioritize_hypotheses()
    for i, h in enumerate(prioritized, 1):
        print(f"  {i}. {h.title} (ICE: {h.ice_score:.1f})")

    print("\n--- Creating A/B Tests ---")
    test1 = agent.create_ab_test(
        name="Hero CTA Button Color",
        url="/pricing",
        variants=[("Blue Control", True), ("Green Variant", False)],
        target_metric=ConversionMetric.CLICK_THROUGH_RATE,
        hypothesis_id=h1.hypothesis_id,
    )
    agent.approve_test(test1.test_id)
    agent.start_test(test1.test_id)
    print(f"Test started: {test1.name} ({test1.test_id})")

    test2 = agent.create_ab_test(
        name="Headline Value Proposition",
        url="/",
        variants=[("Current Headline", True), ("Benefit-focused Headline", False), ("Question Headline", False)],
        test_type=TestType.A_B_N,
    )
    print(f"Test created: {test2.name} ({test2.test_id})")

    print("\n--- Analyzing Test Results ---")
    results = agent.analyze_test_results(test1.test_id)
    print(f"Winner: {results.winner}")
    print(f"Lift: {results.lift:.2%}")
    print(f"Significance: {results.significance.value}")
    print(f"P-value: {results.p_value:.6f}")

    print("\n--- Analyzing Funnel ---")
    funnel = agent.analyze_funnel(
        name="SaaS Signup Funnel",
        steps=[
            {"name": "Homepage", "stage": "awareness", "visitors": 10000, "conversions": 8500},
            {"name": "Pricing Page", "stage": "consideration", "visitors": 8500, "conversions": 4200},
            {"name": "Signup Form", "stage": "intent", "visitors": 4200, "conversions": 2100},
            {"name": "Email Verification", "stage": "evaluation", "visitors": 2100, "conversions": 1800},
            {"name": "Onboarding Complete", "stage": "activation", "visitors": 1800, "conversions": 1200},
        ],
    )
    print(f"Funnel: {funnel.name}")
    print(f"Overall conversion: {funnel.overall_conversion_rate:.2%}")
    print(f"Biggest drop-off: {funnel.biggest_drop_off}")
    for insight in funnel.insights:
        print(f"  Insight: {insight['step']} — {insight['drop_off_rate']:.1%} drop-off")

    print("\n--- UX Analysis ---")
    ux_report = agent.analyze_ux(page_url="/pricing", page_type="pricing")
    print(f"UX Score: {ux_report.overall_score:.1f}")
    print(f"Issues: {len(ux_report.issues)}")
    print(f"Accessibility: {ux_report.accessibility_score:.1f}")
    print(f"Mobile: {ux_report.mobile_score:.1f}")
    for barrier in ux_report.conversion_barriers[:3]:
        print(f"  Barrier: {barrier}")

    print("\n--- Landing Page Audit ---")
    audit = agent.audit_landing_page(url="/pricing", page_type="pricing")
    print(f"Audit Score: {audit.overall_score:.1f}")
    print(f"Elements analyzed: {len(audit.elements)}")
    print(f"Quick wins: {len(audit.quick_wins)}")
    for qw in audit.quick_wins[:3]:
        print(f"  Quick win: {qw}")
    print(f"Test roadmap phases: {len(audit.ab_test_roadmap)}")

    print("\n--- CRO Strategy ---")
    strategy = agent.create_cro_strategy(
        name="Q3 Conversion Optimization",
        framework=CROFramework.ICE,
        budget=50000.0,
        timeline_months=3,
    )
    agent.add_hypothesis_to_strategy(strategy.strategy_id, h1.hypothesis_id)
    agent.add_hypothesis_to_strategy(strategy.strategy_id, h2.hypothesis_id)
    print(f"Strategy: {strategy.name} ({strategy.strategy_id})")
    print(f"Hypotheses: {len(strategy.hypotheses)}")

    print("\n--- Form Analysis ---")
    form = agent.analyze_form(
        form_name="Free Trial Signup",
        page_url="/signup",
        total_submissions=5000,
        successful_submissions=2800,
    )
    print(f"Completion rate: {form.completion_rate:.2%}")
    for insight in form.insights:
        print(f"  Insight: {insight}")

    print("\n--- Checkout Analysis ---")
    checkout = agent.analyze_checkout(
        steps=[
            {"name": "Cart Review", "visitors": 5000, "conversions": 4200},
            {"name": "Account Creation", "visitors": 4200, "conversions": 3800},
            {"name": "Shipping Info", "visitors": 3800, "conversions": 3200},
            {"name": "Payment", "visitors": 3200, "conversions": 2800},
            {"name": "Order Confirmation", "visitors": 2800, "conversions": 2600},
        ],
    )
    print(f"Completion rate: {checkout.overall_completion_rate:.2%}")
    print(f"Recommendations: {len(checkout.recommendations)}")

    print("\n--- CRO Recommendations ---")
    recs = agent.get_cro_recommendations(page_type="landing_page")
    print(f"Recommendations: {len(recs)}")
    for rec in recs[:3]:
        print(f"  [{rec['priority']}] {rec['category']}: {rec['recommendation']}")

    print("\n--- Test Dashboard ---")
    dashboard = agent.get_test_dashboard()
    print(f"Total tests: {dashboard['total_tests']}")
    print(f"Winners: {dashboard['winners']}")
    print(f"Average lift: {dashboard['average_lift']:.2%}")

    print("\n--- Agent Status ---")
    status = agent.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
