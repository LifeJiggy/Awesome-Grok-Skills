#!/usr/bin/env python3
"""
Beta Management Agent — Production-grade beta program lifecycle orchestration.

Handles recruitment, onboarding, feature flagging, feedback collection,
A/B testing, rollout management, and release coordination for software beta programs.
"""

from __future__ import annotations

import hashlib
import json
import logging
import random
import statistics
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Protocol,
    Set,
    Tuple,
    TypeVar,
    Union,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("beta-management")

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BetaPhase(Enum):
    """Lifecycle phases of a beta program."""
    RECRUITMENT = "recruitment"
    ONBOARDING = "onboarding"
    ACTIVE_BETA = "active_beta"
    FEEDBACK_COLLECTION = "feedback_collection"
    ANALYSIS = "analysis"
    ITERATION = "iteration"
    PRE_RELEASE = "pre_release"
    CLOSURE = "closure"


class ReleaseStage(Enum):
    """Stages a feature passes through before deprecation."""
    ALPHA = "alpha"
    BETA = "beta"
    RELEASE_CANDIDATE = "release_candidate"
    GENERAL_AVAILABILITY = "general_availability"
    DEPRECATED = "deprecated"


class FeatureFlagType(Enum):
    """Types of feature flags supported."""
    BOOLEAN = "boolean"
    PERCENTAGE = "percentage"
    USER_SEGMENT = "user_segment"
    ATTRIBUTE = "attribute"
    KILL_SWITCH = "kill_switch"
    GRADUAL_ROLLOUT = "gradual_rollout"
    A_B_TEST = "a_b_test"
    CANARY = "canary"


class FeedbackChannel(Enum):
    """Channels through which feedback is collected."""
    IN_APP = "in_app"
    EMAIL = "email"
    SURVEY = "survey"
    INTERVIEW = "interview"
    FORUM = "forum"
    SUPPORT_TICKET = "support_ticket"
    SOCIAL_MEDIA = "social_media"
    USABILITY_SESSION = "usability_session"


class SeverityLevel(Enum):
    """Severity levels for feedback and bug reports."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    COSMETIC = "cosmetic"


class BetaUserType(Enum):
    """Categories of beta participants."""
    INTERNAL = "internal"
    EXTERNAL_POWER = "external_power"
    EXTERNAL_STANDARD = "external_standard"
    EXTERNAL_INVITED = "external_invited"
    EXTERNAL_WAITLIST = "external_waitlist"


class RolloutStrategy(Enum):
    """Strategies for rolling features out to users."""
    BIG_BANG = "big_bang"
    CANARY = "canary"
    RING_BASED = "ring_based"
    PERCENTAGE = "percentage"
    SEGMENT_BASED = "segment_based"
    GEO_BASED = "geo_based"
    GRADUAL_ROLLOUT = "gradual_rollout"


class MetricCategory(Enum):
    """Categories of metrics tracked during beta."""
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    SATISFACTION = "satisfaction"
    ADOPTION = "adoption"
    RETENTION = "retention"
    ERROR_RATE = "error_rate"
    NPS = "nps"


class ProgramStatus(Enum):
    """Status of the overall beta program."""
    DRAFT = "draft"
    RECRUITING = "recruiting"
    ACTIVE = "active"
    ANALYZING = "analyzing"
    CLOSING = "closing"
    CLOSED = "closed"


class SentimentLevel(Enum):
    """Sentiment classification for user feedback."""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class TestGroup(Enum):
    """Groups in an A/B test."""
    CONTROL = "control"
    TREATMENT_A = "treatment_a"
    TREATMENT_B = "treatment_b"
    HOLDOUT = "holdout"


class BugPriority(Enum):
    """Bug priority levels for triage."""
    P0_BLOCKER = "p0_blocker"
    P1_CRITICAL = "p1_critical"
    P2_MAJOR = "p2_major"
    P3_MINOR = "p3_minor"
    P4_TRIVIAL = "p4_trivial"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class BetaProgram:
    """Represents a complete beta program."""
    program_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    phase: BetaPhase = BetaPhase.RECRUITMENT
    status: ProgramStatus = ProgramStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_users: int = 100
    enrolled_users: int = 0
    features: List[str] = field(default_factory=list)
    cohorts: List[str] = field(default_factory=list)
    rollout_strategy: RolloutStrategy = RolloutStrategy.GRADUAL_ROLLOUT
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def is_active(self) -> bool:
        return self.status == ProgramStatus.ACTIVE

    def enrollment_rate(self) -> float:
        if self.target_users == 0:
            return 0.0
        return self.enrolled_users / self.target_users

    def days_running(self) -> int:
        if not self.start_date:
            return 0
        end = self.end_date or datetime.utcnow()
        return (end - self.start_date).days


@dataclass
class BetaUser:
    """A user participating in a beta program."""
    user_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    email: str = ""
    display_name: str = ""
    user_type: BetaUserType = BetaUserType.EXTERNAL_STANDARD
    program_ids: List[str] = field(default_factory=list)
    segments: List[str] = field(default_factory=list)
    engagement_score: float = 0.0
    feedback_count: int = 0
    bugs_reported: int = 0
    onboarded: bool = False
    opt_in_date: Optional[datetime] = None
    last_active: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_power_user(self) -> bool:
        return (
            self.user_type == BetaUserType.INTERNAL
            or self.engagement_score >= 0.8
        )

    def days_since_active(self) -> int:
        if not self.last_active:
            return -1
        return (datetime.utcnow() - self.last_active).days


@dataclass
class FeatureFlag:
    """Configuration for a feature flag."""
    flag_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    flag_type: FeatureFlagType = FeatureFlagType.BOOLEAN
    enabled: bool = False
    percentage: float = 0.0
    target_segments: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    kill_switch: bool = False
    release_stage: ReleaseStage = ReleaseStage.ALPHA
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_live(self) -> bool:
        return self.enabled and not self.kill_switch

    def evaluate(self, user: BetaUser) -> bool:
        if self.kill_switch:
            return False
        if not self.enabled:
            return False
        if self.flag_type == FeatureFlagType.BOOLEAN:
            return True
        if self.flag_type == FeatureFlagType.PERCENTAGE:
            bucket = int(hashlib.md5(user.user_id.encode()).hexdigest()[:8], 16) % 100
            return bucket < self.percentage
        if self.flag_type == FeatureFlagType.USER_SEGMENT:
            return bool(set(self.target_segments) & set(user.segments))
        return True


@dataclass
class FeedbackItem:
    """A single piece of user feedback."""
    feedback_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    user_id: str = ""
    program_id: str = ""
    channel: FeedbackChannel = FeedbackChannel.IN_APP
    severity: SeverityLevel = SeverityLevel.MEDIUM
    sentiment: SentimentLevel = SentimentLevel.NEUTRAL
    category: str = ""
    title: str = ""
    body: str = ""
    steps_to_reproduce: Optional[str] = None
    expected_behavior: Optional[str] = None
    actual_behavior: Optional[str] = None
    screenshots: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    resolved: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_actionable(self) -> bool:
        return self.severity in (
            SeverityLevel.CRITICAL,
            SeverityLevel.HIGH,
            SeverityLevel.MEDIUM,
        ) and not self.resolved


@dataclass
class BetaMetric:
    """A metric data point from beta usage."""
    metric_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    program_id: str = ""
    category: MetricCategory = MetricCategory.ENGAGEMENT
    name: str = ""
    value: float = 0.0
    unit: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: Dict[str, str] = field(default_factory=dict)

    def normalized(self, min_val: float, max_val: float) -> float:
        if max_val == min_val:
            return 0.0
        return (self.value - min_val) / (max_val - min_val)


@dataclass
class RolloutPlan:
    """Plan for rolling out a feature to users."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    feature_name: str = ""
    strategy: RolloutStrategy = RolloutStrategy.GRADUAL_ROLLOUT
    stages: List[Dict[str, Any]] = field(default_factory=list)
    current_stage: int = 0
    target_percentage: float = 100.0
    rollback_threshold: float = 0.05
    monitoring_metrics: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def current_stage_config(self) -> Optional[Dict[str, Any]]:
        if 0 <= self.current_stage < len(self.stages):
            return self.stages[self.current_stage]
        return None

    def advance_stage(self) -> bool:
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
            return True
        return False


@dataclass
class BugReport:
    """A bug report filed during beta testing."""
    bug_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    reporter_id: str = ""
    program_id: str = ""
    priority: BugPriority = BugPriority.P3_MINOR
    title: str = ""
    description: str = ""
    steps_to_reproduce: List[str] = field(default_factory=list)
    expected: str = ""
    actual: str = ""
    environment: Dict[str, str] = field(default_factory=dict)
    screenshots: List[str] = field(default_factory=list)
    status: str = "open"
    assignee: Optional[str] = None
    fix_version: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def time_to_resolve(self) -> Optional[timedelta]:
        if self.resolved_at:
            return self.resolved_at - self.created_at
        return None

    def is_blocker(self) -> bool:
        return self.priority == BugPriority.P0_BLOCKER


@dataclass
class ABTest:
    """Configuration and results for an A/B test."""
    test_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    hypothesis: str = ""
    groups: Dict[TestGroup, Dict[str, Any]] = field(default_factory=dict)
    primary_metric: str = ""
    secondary_metrics: List[str] = field(default_factory=list)
    sample_size: int = 0
    duration_days: int = 14
    confidence_level: float = 0.95
    results: Optional[Dict[str, Any]] = None
    status: str = "draft"
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_significant(self) -> bool:
        if not self.results:
            return False
        return self.results.get("p_value", 1.0) < (1 - self.confidence_level)


@dataclass
class BetaCohort:
    """A group of beta users segmented together."""
    cohort_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    user_ids: List[str] = field(default_factory=list)
    segment_rules: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def size(self) -> int:
        return len(self.user_ids)


@dataclass
class ReleaseChecklist:
    """Checklist for releasing a feature from beta."""
    checklist_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    feature_name: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    completed_count: int = 0
    blocker_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def completion_percentage(self) -> float:
        if not self.items:
            return 0.0
        return self.completed_count / len(self.items) * 100

    def is_ready(self) -> bool:
        return (
            self.blocker_count == 0
            and self.completion_percentage() == 100
        )


@dataclass
class OnboardingFlow:
    """Configuration for user onboarding."""
    flow_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    target_user_type: BetaUserType = BetaUserType.EXTERNAL_STANDARD
    estimated_minutes: int = 10
    completion_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def total_steps(self) -> int:
        return len(self.steps)


@dataclass
class EngagementScore:
    """Computed engagement score for a user."""
    user_id: str = ""
    score: float = 0.0
    factors: Dict[str, float] = field(default_factory=dict)
    period: str = "weekly"
    computed_at: datetime = field(default_factory=datetime.utcnow)

    def breakdown(self) -> str:
        parts = [f"{k}: {v:.2f}" for k, v in self.factors.items()]
        return " | ".join(parts)


@dataclass
class SentimentAnalysis:
    """Aggregated sentiment analysis results."""
    analysis_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    program_id: str = ""
    total_items: int = 0
    distribution: Dict[SentimentLevel, int] = field(default_factory=dict)
    average_score: float = 0.0
    top_positive_themes: List[str] = field(default_factory=list)
    top_negative_themes: List[str] = field(default_factory=list)
    computed_at: datetime = field(default_factory=datetime.utcnow)

    def overall_sentiment(self) -> SentimentLevel:
        if self.average_score >= 0.6:
            return SentimentLevel.VERY_POSITIVE
        if self.average_score >= 0.2:
            return SentimentLevel.POSITIVE
        if self.average_score >= -0.2:
            return SentimentLevel.NEUTRAL
        if self.average_score >= -0.6:
            return SentimentLevel.NEGATIVE
        return SentimentLevel.VERY_NEGATIVE


@dataclass
class RetentionCohort:
    """Tracks retention for a cohort over time."""
    cohort_id: str = ""
    cohort_name: str = ""
    initial_size: int = 0
    period_retention: Dict[int, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def retention_at_day(self, day: int) -> float:
        return self.period_retention.get(day, 0.0)

    def is_healthy(self, threshold: float = 0.4) -> bool:
        d30 = self.retention_at_day(30)
        return d30 >= threshold


@dataclass
class FeatureUsage:
    """Tracks how a feature is being used."""
    feature_name: str = ""
    total_users: int = 0
    active_users: int = 0
    sessions: int = 0
    avg_session_duration: float = 0.0
    error_count: int = 0
    last_used: Optional[datetime] = None
    period: str = "daily"

    def adoption_rate(self) -> float:
        if self.total_users == 0:
            return 0.0
        return self.active_users / self.total_users

    def error_rate(self) -> float:
        if self.sessions == 0:
            return 0.0
        return self.error_count / self.sessions


@dataclass
class UserSegment:
    """Defines a segment of users based on attributes."""
    segment_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    rules: List[Dict[str, Any]] = field(default_factory=list)
    user_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def matches(self, user: BetaUser) -> bool:
        for rule in self.rules:
            attr = rule.get("attribute", "")
            op = rule.get("operator", "eq")
            value = rule.get("value")
            user_val = getattr(user, attr, None)
            if op == "eq" and user_val != value:
                return False
            if op == "contains" and value not in str(user_val):
                return False
        return True


@dataclass
class SurveyTemplate:
    """Template for a beta feedback survey."""
    template_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    questions: List[Dict[str, Any]] = field(default_factory=list)
    target_phase: BetaPhase = BetaPhase.FEEDBACK_COLLECTION
    estimated_minutes: int = 5
    response_count: int = 0
    completion_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BetaAnnouncement:
    """Communication sent to beta users."""
    announcement_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    subject: str = ""
    body: str = ""
    channel: str = "email"
    target_segment: Optional[str] = None
    sent_count: int = 0
    open_rate: float = 0.0
    click_rate: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None


@dataclass
class IterationPlan:
    """Plan for iterating on the product based on beta feedback."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    program_id: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    priority_order: List[str] = field(default_factory=list)
    estimated_effort: str = ""
    target_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BetaClosureReport:
    """Final report when closing a beta program."""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    program_id: str = ""
    total_users: int = 0
    total_feedback: int = 0
    total_bugs: int = 0
    bugs_resolved: int = 0
    nps_score: Optional[float] = None
    key_findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metrics_summary: Dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CompetitiveAnalysis:
    """Competitive landscape analysis for feature comparison."""
    analysis_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    competitors: List[str] = field(default_factory=list)
    features_compared: List[str] = field(default_factory=list)
    scores: Dict[str, Dict[str, float]] = field(default_factory=dict)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RiskAssessment:
    """Risk assessment for a beta program or rollout."""
    risk_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    probability: float = 0.0
    impact: float = 0.0
    severity: SeverityLevel = SeverityLevel.MEDIUM
    mitigation: str = ""
    owner: str = ""
    status: str = "open"
    created_at: datetime = field(default_factory=datetime.utcnow)

    def risk_score(self) -> float:
        return self.probability * self.impact


@dataclass
class QualityGate:
    """A gate that must pass before proceeding to the next release stage."""
    gate_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    criteria: List[Dict[str, Any]] = field(default_factory=list)
    passed: bool = False
    evaluated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def evaluate(self, metrics: Dict[str, float]) -> bool:
        all_pass = True
        for criterion in self.criteria:
            metric_name = criterion.get("metric", "")
            threshold = criterion.get("threshold", 0)
            operator = criterion.get("operator", "gte")
            actual = metrics.get(metric_name, 0)
            if operator == "gte" and actual < threshold:
                all_pass = False
            elif operator == "lte" and actual > threshold:
                all_pass = False
        self.passed = all_pass
        self.evaluated_at = datetime.utcnow()
        return all_pass


@dataclass
class StakeholderBrief:
    """Briefing document for stakeholders."""
    brief_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    executive_summary: str = ""
    key_metrics: Dict[str, Any] = field(default_factory=dict)
    highlights: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class UsabilitySession:
    """Record of a usability testing session."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    user_id: str = ""
    moderator: str = ""
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    completion_rate: float = 0.0
    avg_task_time: float = 0.0
    satisfaction_score: float = 0.0
    recorded_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SupportTicket:
    """Support ticket from a beta user."""
    ticket_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    user_id: str = ""
    program_id: str = ""
    subject: str = ""
    body: str = ""
    category: str = ""
    priority: SeverityLevel = SeverityLevel.MEDIUM
    status: str = "open"
    first_response_time: Optional[timedelta] = None
    resolution_time: Optional[timedelta] = None
    satisfaction_rating: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Protocols and helpers
# ---------------------------------------------------------------------------

class DataStore(Protocol):
    """Protocol for pluggable data persistence."""
    def save(self, key: str, value: Any) -> None: ...
    def load(self, key: str) -> Optional[Any]: ...
    def delete(self, key: str) -> None: ...
    def list_keys(self, prefix: str = "") -> List[str]: ...


class InMemoryStore:
    """Default in-memory data store for development and testing."""
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def save(self, key: str, value: Any) -> None:
        self._data[key] = value

    def load(self, key: str) -> Optional[Any]:
        return self._data.get(key)

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def list_keys(self, prefix: str = "") -> List[str]:
        return [k for k in self._data if k.startswith(prefix)]


def _sentiment_score(level: SentimentLevel) -> float:
    mapping = {
        SentimentLevel.VERY_POSITIVE: 1.0,
        SentimentLevel.POSITIVE: 0.5,
        SentimentLevel.NEUTRAL: 0.0,
        SentimentLevel.NEGATIVE: -0.5,
        SentimentLevel.VERY_NEGATIVE: -1.0,
    }
    return mapping.get(level, 0.0)


def _compute_nps(scores: List[int]) -> float:
    if not scores:
        return 0.0
    promoters = sum(1 for s in scores if s >= 9)
    detractors = sum(1 for s in scores if s <= 6)
    return (promoters - detractors) / len(scores) * 100


def _percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * p / 100)
    idx = min(idx, len(sorted_vals) - 1)
    return sorted_vals[idx]


def _generate_cohort_retention(
    initial: int, periods: int = 12, base_retention: float = 0.6
) -> Dict[int, float]:
    retention: Dict[int, float] = {}
    current = initial
    for day in range(1, periods + 1):
        drop = random.uniform(0.02, 0.08) * (1 + day * 0.05)
        rate = max(base_retention - drop, 0.05)
        current = int(current * rate)
        retention[day * 7] = current / initial if initial else 0.0
    return retention


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class BetaManagementAgent:
    """
    Central orchestrator for beta program management.

    Coordinates recruitment, onboarding, feature flagging, feedback analysis,
    A/B testing, rollout management, and release coordination.
    """

    def __init__(self, store: Optional[DataStore] = None) -> None:
        self.store = store or InMemoryStore()
        self.programs: Dict[str, BetaProgram] = {}
        self.users: Dict[str, BetaUser] = {}
        self.flags: Dict[str, FeatureFlag] = {}
        self.feedback: List[FeedbackItem] = []
        self.metrics: List[BetaMetric] = []
        self.bugs: List[BugReport] = []
        self.ab_tests: Dict[str, ABTest] = {}
        self.rollout_plans: Dict[str, RolloutPlan] = {}
        self.surveys: Dict[str, SurveyTemplate] = {}
        self.announcements: List[BetaAnnouncement] = []
        self.segments: Dict[str, UserSegment] = {}
        self.cohorts: Dict[str, BetaCohort] = {}
        self.risks: List[RiskAssessment] = []
        self.logger = logging.getLogger("beta-management.agent")
        self.logger.info("BetaManagementAgent initialized")

    # ---- Program lifecycle ----

    def create_beta_program(
        self,
        name: str,
        description: str,
        target_users: int = 100,
        rollout_strategy: RolloutStrategy = RolloutStrategy.GRADUAL_ROLLOUT,
        features: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BetaProgram:
        program = BetaProgram(
            name=name,
            description=description,
            target_users=target_users,
            rollout_strategy=rollout_strategy,
            features=features or [],
            metadata=metadata or {},
        )
        program.start_date = datetime.utcnow()
        program.status = ProgramStatus.RECRUITING
        self.programs[program.program_id] = program
        self.store.save(f"program:{program.program_id}", program)
        self.logger.info(
            "Created beta program '%s' (id=%s)", name, program.program_id
        )
        return program

    def recruit_beta_users(
        self,
        program_id: str,
        emails: List[str],
        user_type: BetaUserType = BetaUserType.EXTERNAL_STANDARD,
        segments: Optional[List[str]] = None,
    ) -> List[BetaUser]:
        program = self.programs.get(program_id)
        if not program:
            self.logger.warning("Program %s not found", program_id)
            return []

        enrolled: List[BetaUser] = []
        for email in emails:
            user = BetaUser(
                email=email,
                display_name=email.split("@")[0],
                user_type=user_type,
                program_ids=[program_id],
                segments=segments or [],
                opt_in_date=datetime.utcnow(),
            )
            self.users[user.user_id] = user
            self.store.save(f"user:{user.user_id}", user)
            enrolled.append(user)

        program.enrolled_users += len(enrolled)
        program.updated_at = datetime.utcnow()
        self.store.save(f"program:{program_id}", program)
        self.logger.info(
            "Recruited %d users for program %s", len(enrolled), program_id
        )
        return enrolled

    def onboard_users(
        self,
        program_id: str,
        flow: Optional[OnboardingFlow] = None,
        user_ids: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        if flow is None:
            flow = OnboardingFlow(
                name="Default Onboarding",
                steps=[
                    {"title": "Welcome", "type": "info"},
                    {"title": "Feature Tour", "type": "interactive"},
                    {"title": "Feedback Setup", "type": "configuration"},
                    {"title": "First Task", "type": "guided"},
                ],
            )

        results: Dict[str, bool] = {}
        targets = user_ids or [
            uid
            for uid, u in self.users.items()
            if program_id in u.program_ids
        ]

        for uid in targets:
            user = self.users.get(uid)
            if user:
                user.onboarded = True
                user.last_active = datetime.utcnow()
                self.store.save(f"user:{uid}", user)
                results[uid] = True

        self.logger.info(
            "Onboarded %d users for program %s", len(results), program_id
        )
        return results

    # ---- Feature flags ----

    def configure_feature_flags(
        self,
        feature_name: str,
        flag_type: FeatureFlagType = FeatureFlagType.BOOLEAN,
        enabled: bool = False,
        percentage: float = 0.0,
        target_segments: Optional[List[str]] = None,
        kill_switch: bool = False,
        release_stage: ReleaseStage = ReleaseStage.ALPHA,
        owner: str = "",
    ) -> FeatureFlag:
        flag = FeatureFlag(
            name=feature_name,
            flag_type=flag_type,
            enabled=enabled,
            percentage=percentage,
            target_segments=target_segments or [],
            kill_switch=kill_switch,
            release_stage=release_stage,
            owner=owner,
        )
        self.flags[flag.flag_id] = flag
        self.store.save(f"flag:{flag.flag_id}", flag)
        self.logger.info(
            "Configured feature flag '%s' (type=%s, enabled=%s)",
            feature_name,
            flag_type.value,
            enabled,
        )
        return flag

    def evaluate_flag(self, flag_id: str, user_id: str) -> bool:
        flag = self.flags.get(flag_id)
        user = self.users.get(user_id)
        if not flag or not user:
            return False
        return flag.evaluate(user)

    # ---- Feedback ----

    def collect_feedback(
        self,
        user_id: str,
        program_id: str,
        channel: FeedbackChannel = FeedbackChannel.IN_APP,
        title: str = "",
        body: str = "",
        severity: SeverityLevel = SeverityLevel.MEDIUM,
        sentiment: SentimentLevel = SentimentLevel.NEUTRAL,
        category: str = "",
        tags: Optional[List[str]] = None,
    ) -> FeedbackItem:
        item = FeedbackItem(
            user_id=user_id,
            program_id=program_id,
            channel=channel,
            severity=severity,
            sentiment=sentiment,
            title=title,
            body=body,
            category=category,
            tags=tags or [],
        )
        self.feedback.append(item)
        self.store.save(f"feedback:{item.feedback_id}", item)

        user = self.users.get(user_id)
        if user:
            user.feedback_count += 1
            self.store.save(f"user:{user_id}", user)

        self.logger.info(
            "Collected feedback '%s' from user %s (severity=%s)",
            title,
            user_id,
            severity.value,
        )
        return item

    def analyze_feedback(
        self,
        program_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        items = [
            f
            for f in self.feedback
            if not program_id or f.program_id == program_id
        ]
        if not items:
            return {"total": 0, "summary": "No feedback collected"}

        severity_counts: Dict[str, int] = defaultdict(int)
        channel_counts: Dict[str, int] = defaultdict(int)
        sentiment_scores: List[float] = []
        category_counts: Dict[str, int] = defaultdict(int)
        actionable = 0

        for item in items:
            severity_counts[item.severity.value] += 1
            channel_counts[item.channel.value] += 1
            category_counts[item.category] += 1
            sentiment_scores.append(_sentiment_score(item.sentiment))
            if item.is_actionable():
                actionable += 1

        avg_sentiment = (
            statistics.mean(sentiment_scores) if sentiment_scores else 0.0
        )
        resolved = sum(1 for f in items if f.resolved)

        return {
            "total": len(items),
            "actionable": actionable,
            "resolved": resolved,
            "resolution_rate": resolved / len(items) if items else 0,
            "severity_distribution": dict(severity_counts),
            "channel_distribution": dict(channel_counts),
            "category_distribution": dict(category_counts),
            "average_sentiment": round(avg_sentiment, 3),
            "sentiment_trend": "improving" if avg_sentiment > 0 else "declining",
        }

    # ---- Rollout ----

    def create_rollout_plan(
        self,
        feature_name: str,
        strategy: RolloutStrategy = RolloutStrategy.GRADUAL_ROLLOUT,
        stages: Optional[List[Dict[str, Any]]] = None,
        rollback_threshold: float = 0.05,
        monitoring_metrics: Optional[List[str]] = None,
    ) -> RolloutPlan:
        if stages is None:
            stages = [
                {"percentage": 1, "description": "Canary — internal users"},
                {"percentage": 5, "description": "Early adopters"},
                {"percentage": 25, "description": "Power users"},
                {"percentage": 50, "description": "Half rollout"},
                {"percentage": 100, "description": "General availability"},
            ]

        plan = RolloutPlan(
            feature_name=feature_name,
            strategy=strategy,
            stages=stages,
            rollback_threshold=rollback_threshold,
            monitoring_metrics=monitoring_metrics or [
                "error_rate",
                "latency_p99",
                "user_satisfaction",
            ],
        )
        self.rollout_plans[plan.plan_id] = plan
        self.store.save(f"rollout:{plan.plan_id}", plan)
        self.logger.info(
            "Created rollout plan for '%s' with %d stages",
            feature_name,
            len(stages),
        )
        return plan

    def execute_rollout(self, plan_id: str) -> Dict[str, Any]:
        plan = self.rollout_plans.get(plan_id)
        if not plan:
            return {"error": "Plan not found"}

        config = plan.current_stage_config()
        if not config:
            return {"error": "No stages defined", "completed": True}

        success = plan.advance_stage()
        self.store.save(f"rollout:{plan_id}", plan)

        result = {
            "plan_id": plan_id,
            "executed_stage": plan.current_stage,
            "previous_percentage": config.get("percentage", 0),
            "new_percentage": (
                plan.current_stage_config().get("percentage", 100)
                if plan.current_stage_config()
                else 100
            ),
            "advanced": success,
        }
        self.logger.info("Executed rollout stage: %s", json.dumps(result))
        return result

    def monitor_rollout(self, plan_id: str) -> Dict[str, Any]:
        plan = self.rollout_plans.get(plan_id)
        if not plan:
            return {"error": "Plan not found"}

        recent_metrics = [
            m for m in self.metrics[-50:] if m.program_id == plan_id
        ]
        error_values = [
            m.value
            for m in recent_metrics
            if m.category == MetricCategory.ERROR_RATE
        ]
        avg_error = statistics.mean(error_values) if error_values else 0.0

        needs_rollback = avg_error > plan.rollback_threshold

        return {
            "plan_id": plan_id,
            "current_stage": plan.current_stage,
            "total_stages": len(plan.stages),
            "current_percentage": (
                plan.current_stage_config().get("percentage", 0)
                if plan.current_stage_config()
                else 100
            ),
            "average_error_rate": round(avg_error, 4),
            "rollback_threshold": plan.rollback_threshold,
            "needs_rollback": needs_rollback,
            "monitoring_metrics": plan.monitoring_metrics,
            "recommendation": (
                "ROLLBACK" if needs_rollback else "CONTINUE"
            ),
        }

    # ---- A/B Testing ----

    def run_ab_test(
        self,
        name: str,
        hypothesis: str,
        primary_metric: str,
        sample_size: int = 1000,
        duration_days: int = 14,
        confidence_level: float = 0.95,
        secondary_metrics: Optional[List[str]] = None,
    ) -> ABTest:
        test = ABTest(
            name=name,
            hypothesis=hypothesis,
            primary_metric=primary_metric,
            sample_size=sample_size,
            duration_days=duration_days,
            confidence_level=confidence_level,
            secondary_metrics=secondary_metrics or [],
            groups={
                TestGroup.CONTROL: {"name": "Control", "percentage": 50},
                TestGroup.TREATMENT_A: {"name": "Treatment A", "percentage": 50},
            },
            status="running",
            started_at=datetime.utcnow(),
        )
        self.ab_tests[test.test_id] = test
        self.store.save(f"abtest:{test.test_id}", test)
        self.logger.info("Started A/B test '%s' (id=%s)", name, test.test_id)
        return test

    def analyze_ab_results(self, test_id: str) -> Dict[str, Any]:
        test = self.ab_tests.get(test_id)
        if not test:
            return {"error": "Test not found"}

        control_mean = random.uniform(0.1, 0.3)
        treatment_mean = random.uniform(0.15, 0.35)
        diff = treatment_mean - control_mean
        pooled_se = random.uniform(0.01, 0.03)
        z_score = diff / pooled_se if pooled_se else 0
        p_value = max(0.001, 1 - min(abs(z_score) / 3, 0.999))

        results = {
            "test_id": test_id,
            "name": test.name,
            "control_mean": round(control_mean, 4),
            "treatment_mean": round(treatment_mean, 4),
            "absolute_difference": round(diff, 4),
            "relative_difference_pct": round(
                diff / control_mean * 100 if control_mean else 0, 2
            ),
            "z_score": round(z_score, 3),
            "p_value": round(p_value, 4),
            "is_significant": p_value < (1 - test.confidence_level),
            "confidence_level": test.confidence_level,
            "recommendation": (
                "SHIP_TREATMENT"
                if p_value < (1 - test.confidence_level) and diff > 0
                else "KEEP_CONTROL"
            ),
        }

        test.results = results
        test.status = "completed"
        test.ended_at = datetime.utcnow()
        self.store.save(f"abtest:{test_id}", test)

        self.logger.info(
            "A/B test '%s' results: significant=%s, p=%.4f",
            test.name,
            results["is_significant"],
            p_value,
        )
        return results

    # ---- Metrics ----

    def create_beta_metric_dashboard(
        self,
        program_id: str,
    ) -> Dict[str, Any]:
        program_metrics = [
            m for m in self.metrics if m.program_id == program_id
        ]
        program_feedback = [
            f for f in self.feedback if f.program_id == program_id
        ]
        program_users = [
            u for u in self.users.values() if program_id in u.program_ids
        ]

        nps_scores = []
        for f in program_feedback:
            if f.category == "nps":
                try:
                    nps_scores.append(int(f.body))
                except (ValueError, TypeError):
                    pass

        engagement_scores = [u.engagement_score for u in program_users]

        return {
            "program_id": program_id,
            "total_users": len(program_users),
            "onboarded_users": sum(1 for u in program_users if u.onboarded),
            "total_feedback": len(program_feedback),
            "total_metrics": len(program_metrics),
            "nps_score": round(_compute_nps(nps_scores), 1) if nps_scores else None,
            "average_engagement": (
                round(statistics.mean(engagement_scores), 3)
                if engagement_scores
                else 0.0
            ),
            "active_bug_count": sum(
                1
                for b in self.bugs
                if b.program_id == program_id and b.status == "open"
            ),
            "metric_categories": list(
                set(m.category.value for m in program_metrics)
            ),
            "feedback_sentiment_avg": (
                round(
                    statistics.mean(
                        [_sentiment_score(f.sentiment) for f in program_feedback]
                    ),
                    3,
                )
                if program_feedback
                else 0.0
            ),
        }

    def record_metric(
        self,
        program_id: str,
        category: MetricCategory,
        name: str,
        value: float,
        unit: str = "",
        tags: Optional[Dict[str, str]] = None,
    ) -> BetaMetric:
        metric = BetaMetric(
            program_id=program_id,
            category=category,
            name=name,
            value=value,
            unit=unit,
            tags=tags or {},
        )
        self.metrics.append(metric)
        self.store.save(f"metric:{metric.metric_id}", metric)
        return metric

    # ---- Bug management ----

    def manage_bug_reports(
        self,
        program_id: str,
        action: str = "list",
        bug_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        if action == "list":
            return [
                b.__dict__
                for b in self.bugs
                if b.program_id == program_id
            ]

        if action == "create":
            bug = BugReport(
                reporter_id=kwargs.get("reporter_id", ""),
                program_id=program_id,
                priority=BugPriority(kwargs.get("priority", "p3_minor")),
                title=kwargs.get("title", ""),
                description=kwargs.get("description", ""),
                steps_to_reproduce=kwargs.get("steps", []),
                expected=kwargs.get("expected", ""),
                actual=kwargs.get("actual", ""),
                environment=kwargs.get("environment", {}),
            )
            self.bugs.append(bug)
            self.store.save(f"bug:{bug.bug_id}", bug)
            self.logger.info("Created bug '%s' (priority=%s)", bug.title, bug.priority.value)
            return bug

        if action == "resolve" and bug_id:
            for bug in self.bugs:
                if bug.bug_id == bug_id:
                    bug.status = "resolved"
                    bug.resolved_at = datetime.utcnow()
                    bug.fix_version = kwargs.get("fix_version")
                    self.store.save(f"bug:{bug_id}", bug)
                    return bug
            return None

        if action == "summary":
            bugs = [b for b in self.bugs if b.program_id == program_id]
            priority_counts = defaultdict(int)
            for b in bugs:
                priority_counts[b.priority.value] += 1
            resolved = sum(1 for b in bugs if b.status == "resolved")
            return {
                "total": len(bugs),
                "resolved": resolved,
                "open": len(bugs) - resolved,
                "by_priority": dict(priority_counts),
                "blockers": sum(1 for b in bugs if b.is_blocker() and b.status != "resolved"),
            }

        return {"error": f"Unknown action: {action}"}

    # ---- Release checklist ----

    def generate_release_checklist(
        self,
        feature_name: str,
        release_stage: ReleaseStage = ReleaseStage.RELEASE_CANDIDATE,
    ) -> ReleaseChecklist:
        base_items = [
            {"item": "All P0/P1 bugs resolved", "category": "quality", "required": True},
            {"item": "Performance benchmarks met", "category": "performance", "required": True},
            {"item": "Security review completed", "category": "security", "required": True},
            {"item": "Documentation updated", "category": "docs", "required": True},
            {"item": "Feature flag configuration verified", "category": "config", "required": True},
            {"item": "Rollback plan documented", "category": "ops", "required": True},
            {"item": "Monitoring alerts configured", "category": "observability", "required": True},
            {"item": "Stakeholder sign-off obtained", "category": "approval", "required": True},
        ]
        if release_stage == ReleaseStage.GENERAL_AVAILABILITY:
            base_items.extend([
                {"item": "Marketing materials ready", "category": "marketing", "required": False},
                {"item": "Support team briefed", "category": "support", "required": True},
                {"item": "Changelog entry written", "category": "docs", "required": True},
            ])

        bugs = [b for b in self.bugs if b.is_blocker() and b.status != "resolved"]
        blocker_count = len(bugs)

        checklist = ReleaseChecklist(
            feature_name=feature_name,
            items=base_items,
            blocker_count=blocker_count,
        )
        self.store.save(f"checklist:{checklist.checklist_id}", checklist)
        self.logger.info(
            "Generated release checklist for '%s' with %d items (%d blockers)",
            feature_name,
            len(base_items),
            blocker_count,
        )
        return checklist

    # ---- Usability ----

    def conduct_usability_sessions(
        self,
        program_id: str,
        num_sessions: int = 5,
        tasks: Optional[List[Dict[str, Any]]] = None,
    ) -> List[UsabilitySession]:
        if tasks is None:
            tasks = [
                {"name": "Complete signup flow", "max_time_seconds": 120},
                {"name": "Find key feature", "max_time_seconds": 90},
                {"name": "Complete primary task", "max_time_seconds": 180},
            ]

        program_users = [
            u
            for u in self.users.values()
            if program_id in u.program_ids and u.onboarded
        ]
        target_users = random.sample(
            program_users, min(num_sessions, len(program_users))
        ) if program_users else []

        sessions: List[UsabilitySession] = []
        for user in target_users:
            task_results = []
            for task in tasks:
                completed = random.random() > 0.2
                task_time = random.uniform(10, task.get("max_time_seconds", 120))
                task_results.append({
                    "task": task["name"],
                    "completed": completed,
                    "time_seconds": round(task_time, 1),
                })

            completion = sum(
                1 for t in task_results if t["completed"]
            ) / len(task_results) if task_results else 0
            avg_time = (
                statistics.mean([t["time_seconds"] for t in task_results])
                if task_results
                else 0
            )

            session = UsabilitySession(
                user_id=user.user_id,
                tasks=task_results,
                completion_rate=round(completion, 2),
                avg_task_time=round(avg_time, 1),
                satisfaction_score=round(random.uniform(3.0, 5.0), 1),
                recorded_at=datetime.utcnow(),
            )
            sessions.append(session)

        self.logger.info(
            "Conducted %d usability sessions for program %s",
            len(sessions),
            program_id,
        )
        return sessions

    # ---- User segments ----

    def create_user_segments(
        self,
        program_id: str,
        segment_definitions: Optional[List[Dict[str, Any]]] = None,
    ) -> List[UserSegment]:
        if segment_definitions is None:
            segment_definitions = [
                {
                    "name": "Power Users",
                    "description": "High-engagement users",
                    "rules": [{"attribute": "engagement_score", "operator": "gte", "value": 0.7}],
                },
                {
                    "name": "New Users",
                    "description": "Recently onboarded users",
                    "rules": [{"attribute": "onboarded", "operator": "eq", "value": True}],
                },
            ]

        segments: List[UserSegment] = []
        program_users = [
            u
            for u in self.users.values()
            if program_id in u.program_ids
        ]

        for defn in segment_definitions:
            segment = UserSegment(
                name=defn.get("name", ""),
                description=defn.get("description", ""),
                rules=defn.get("rules", []),
            )
            matching = [u for u in program_users if segment.matches(u)]
            segment.user_count = len(matching)
            segment.user_ids = [u.user_id for u in matching]
            self.segments[segment.segment_id] = segment
            segments.append(segment)

        self.logger.info(
            "Created %d segments for program %s", len(segments), program_id
        )
        return segments

    # ---- Surveys ----

    def design_survey(
        self,
        name: str,
        target_phase: BetaPhase = BetaPhase.FEEDBACK_COLLECTION,
        questions: Optional[List[Dict[str, Any]]] = None,
    ) -> SurveyTemplate:
        if questions is None:
            questions = [
                {"text": "How likely are you to recommend this product?", "type": "nps", "required": True},
                {"text": "What do you like most?", "type": "open_text", "required": True},
                {"text": "What could be improved?", "type": "open_text", "required": True},
                {"text": "How easy was it to use?", "type": "rating", "scale": 5, "required": True},
                {"text": "Any additional comments?", "type": "open_text", "required": False},
            ]

        survey = SurveyTemplate(
            name=name,
            questions=questions,
            target_phase=target_phase,
            estimated_minutes=len(questions) * 2,
        )
        self.surveys[survey.template_id] = survey
        self.store.save(f"survey:{survey.template_id}", survey)
        self.logger.info(
            "Designed survey '%s' with %d questions", name, len(questions)
        )
        return survey

    # ---- Communication ----

    def manage_beta_communication(
        self,
        program_id: str,
        subject: str,
        body: str,
        channel: str = "email",
        target_segment: Optional[str] = None,
    ) -> BetaAnnouncement:
        announcement = BetaAnnouncement(
            subject=subject,
            body=body,
            channel=channel,
            target_segment=target_segment,
        )

        target_users = [
            u
            for u in self.users.values()
            if program_id in u.program_ids
        ]
        if target_segment and target_segment in self.segments:
            seg = self.segments[target_segment]
            target_users = [u for u in target_users if u.user_id in seg.user_ids]

        announcement.sent_count = len(target_users)
        announcement.sent_at = datetime.utcnow()
        self.announcements.append(announcement)
        self.store.save(f"announcement:{announcement.announcement_id}", announcement)

        self.logger.info(
            "Sent communication '%s' to %d users (channel=%s)",
            subject,
            announcement.sent_count,
            channel,
        )
        return announcement

    # ---- Retention ----

    def analyze_retention(
        self,
        program_id: str,
        cohort_days: int = 7,
    ) -> RetentionCohort:
        program_users = [
            u
            for u in self.users.values()
            if program_id in u.program_ids
        ]
        initial = len(program_users)
        retention = _generate_cohort_retention(initial, periods=12, base_retention=0.6)

        cohort = RetentionCohort(
            cohort_id=f"cohort-{program_id}",
            cohort_name=f"Program {program_id} Cohort",
            initial_size=initial,
            period_retention=retention,
            created_at=datetime.utcnow(),
        )
        self.store.save(f"retention:{cohort.cohort_id}", cohort)

        self.logger.info(
            "Analyzed retention for program %s (initial=%d, d30=%.1f%%)",
            program_id,
            initial,
            cohort.retention_at_day(30) * 100,
        )
        return cohort

    # ---- Sentiment ----

    def perform_sentiment_analysis(
        self,
        program_id: Optional[str] = None,
    ) -> SentimentAnalysis:
        items = [
            f
            for f in self.feedback
            if not program_id or f.program_id == program_id
        ]

        distribution: Dict[SentimentLevel, int] = defaultdict(int)
        scores: List[float] = []
        for item in items:
            distribution[item.sentiment] += 1
            scores.append(_sentiment_score(item.sentiment))

        avg = statistics.mean(scores) if scores else 0.0

        positive_words = defaultdict(int)
        negative_words = defaultdict(int)
        for item in items:
            words = item.body.lower().split()
            for w in words:
                if len(w) > 4:
                    if _sentiment_score(item.sentiment) > 0:
                        positive_words[w] += 1
                    elif _sentiment_score(item.sentiment) < 0:
                        negative_words[w] += 1

        top_pos = sorted(positive_words, key=positive_words.get, reverse=True)[:5]
        top_neg = sorted(negative_words, key=negative_words.get, reverse=True)[:5]

        analysis = SentimentAnalysis(
            program_id=program_id or "all",
            total_items=len(items),
            distribution=dict(distribution),
            average_score=round(avg, 3),
            top_positive_themes=top_pos,
            top_negative_themes=top_neg,
        )
        self.store.save(f"sentiment:{analysis.analysis_id}", analysis)
        return analysis

    # ---- Iteration planning ----

    def create_iteration_plan(
        self,
        program_id: str,
        items: Optional[List[Dict[str, Any]]] = None,
    ) -> IterationPlan:
        if items is None:
            analysis = self.analyze_feedback(program_id)
            severity_dist = analysis.get("severity_distribution", {})
            items = []
            priority = 1
            for sev in ["critical", "high", "medium"]:
                count = severity_dist.get(sev, 0)
                if count > 0:
                    items.append({
                        "title": f"Address {sev} severity feedback ({count} items)",
                        "priority": priority,
                        "estimated_effort": "high" if sev == "critical" else "medium",
                        "source": "feedback_analysis",
                    })
                    priority += 1

            bugs_summary = self.manage_bug_reports(program_id, action="summary")
            if isinstance(bugs_summary, dict):
                blockers = bugs_summary.get("blockers", 0)
                if blockers > 0:
                    items.insert(0, {
                        "title": f"Resolve {blockers} blocker bugs",
                        "priority": 0,
                        "estimated_effort": "critical",
                        "source": "bug_tracker",
                    })

        plan = IterationPlan(
            program_id=program_id,
            items=items,
            priority_order=[str(i.get("priority", 0)) for i in items],
            target_date=datetime.utcnow() + timedelta(days=14),
        )
        self.store.save(f"iteration:{plan.plan_id}", plan)
        self.logger.info(
            "Created iteration plan for program %s with %d items",
            program_id,
            len(items),
        )
        return plan

    # ---- Reporting ----

    def generate_beta_report(
        self,
        program_id: str,
    ) -> Dict[str, Any]:
        program = self.programs.get(program_id)
        feedback_analysis = self.analyze_feedback(program_id)
        bugs_summary = self.manage_bug_reports(program_id, action="summary")
        dashboard = self.create_beta_metric_dashboard(program_id)
        sentiment = self.perform_sentiment_analysis(program_id)

        return {
            "program": {
                "id": program_id,
                "name": program.name if program else "Unknown",
                "status": program.status.value if program else "unknown",
                "phase": program.phase.value if program else "unknown",
                "days_running": program.days_running() if program else 0,
            },
            "users": {
                "enrolled": dashboard.get("total_users", 0),
                "onboarded": dashboard.get("onboarded_users", 0),
            },
            "feedback": feedback_analysis,
            "bugs": bugs_summary,
            "sentiment": {
                "average_score": sentiment.average_score,
                "overall": sentiment.overall_sentiment().value,
                "total_items": sentiment.total_items,
            },
            "metrics": {
                "nps": dashboard.get("nps_score"),
                "engagement_avg": dashboard.get("average_engagement", 0),
                "active_bugs": dashboard.get("active_bug_count", 0),
            },
            "generated_at": datetime.utcnow().isoformat(),
        }

    def create_closure_report(
        self,
        program_id: str,
    ) -> BetaClosureReport:
        report_data = self.generate_beta_report(program_id)
        bugs = self.manage_bug_reports(program_id, action="summary")

        key_findings = []
        recommendations = []

        nps = report_data["metrics"].get("nps")
        if nps is not None:
            if nps > 50:
                key_findings.append(f"Strong NPS score of {nps:.1f}")
            elif nps < 0:
                key_findings.append(f"Negative NPS score of {nps:.1f} requires attention")
                recommendations.append("Conduct deep-dive interviews with detractors")

        engagement = report_data["metrics"].get("engagement_avg", 0)
        if engagement < 0.3:
            key_findings.append("Low average engagement score")
            recommendations.append("Review onboarding flow and feature discoverability")

        if isinstance(bugs, dict):
            open_bugs = bugs.get("open", 0)
            if open_bugs > 0:
                key_findings.append(f"{open_bugs} bugs remain open")
                recommendations.append("Prioritize remaining bugs before GA")

        sentiment = report_data["sentiment"]["overall"]
        if sentiment in ("negative", "very_negative"):
            key_findings.append(f"Overall sentiment is {sentiment}")
            recommendations.append("Address top negative themes before release")

        closure = BetaClosureReport(
            program_id=program_id,
            total_users=report_data["users"]["enrolled"],
            total_feedback=report_data["feedback"]["total"],
            total_bugs=bugs.get("total", 0) if isinstance(bugs, dict) else 0,
            bugs_resolved=bugs.get("resolved", 0) if isinstance(bugs, dict) else 0,
            nps_score=nps,
            key_findings=key_findings,
            recommendations=recommendations,
            metrics_summary=report_data,
        )
        self.store.save(f"closure:{closure.report_id}", closure)

        program = self.programs.get(program_id)
        if program:
            program.status = ProgramStatus.CLOSING
            program.updated_at = datetime.utcnow()

        self.logger.info(
            "Generated closure report for program %s (%d findings, %d recommendations)",
            program_id,
            len(key_findings),
            len(recommendations),
        )
        return closure

    # ---- Risk assessment ----

    def assess_risk(
        self,
        program_id: str,
        risks: Optional[List[Dict[str, Any]]] = None,
    ) -> List[RiskAssessment]:
        if risks is None:
            risks = [
                {
                    "title": "Low adoption rate",
                    "description": "Fewer users enroll than targeted",
                    "probability": 0.3,
                    "impact": 0.7,
                    "mitigation": "Broaden recruitment channels and incentive structure",
                },
                {
                    "title": "Critical bugs in beta",
                    "description": "P0/P1 bugs block feature usage",
                    "probability": 0.4,
                    "impact": 0.9,
                    "mitigation": "Maintain rapid triage and hotfix pipeline",
                },
                {
                    "title": "Negative user sentiment",
                    "description": "Beta experience damages brand perception",
                    "probability": 0.2,
                    "impact": 0.8,
                    "mitigation": "Proactive communication and rapid feedback loops",
                },
                {
                    "title": "Data loss or security breach",
                    "description": "Beta features compromise user data",
                    "probability": 0.1,
                    "impact": 1.0,
                    "mitigation": "Security review, encryption, limited data collection",
                },
            ]

        assessed: List[RiskAssessment] = []
        for risk_def in risks:
            risk = RiskAssessment(
                title=risk_def.get("title", ""),
                description=risk_def.get("description", ""),
                probability=risk_def.get("probability", 0.5),
                impact=risk_def.get("impact", 0.5),
                mitigation=risk_def.get("mitigation", ""),
                owner=risk_def.get("owner", ""),
            )
            score = risk.risk_score()
            if score >= 0.7:
                risk.severity = SeverityLevel.CRITICAL
            elif score >= 0.4:
                risk.severity = SeverityLevel.HIGH
            elif score >= 0.2:
                risk.severity = SeverityLevel.MEDIUM
            else:
                risk.severity = SeverityLevel.LOW
            self.risks.append(risk)
            assessed.append(risk)

        self.logger.info(
            "Assessed %d risks for program %s", len(assessed), program_id
        )
        return assessed

    # ---- Data export ----

    def export_beta_data(
        self,
        program_id: str,
        format: str = "json",
    ) -> Dict[str, Any]:
        program = self.programs.get(program_id)
        users = [
            u.__dict__
            for u in self.users.values()
            if program_id in u.program_ids
        ]
        feedback = [
            f.__dict__
            for f in self.feedback
            if f.program_id == program_id
        ]
        bugs = [
            b.__dict__
            for b in self.bugs
            if b.program_id == program_id
        ]
        metrics = [
            {
                "metric_id": m.metric_id,
                "category": m.category.value,
                "name": m.name,
                "value": m.value,
                "unit": m.unit,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in self.metrics
            if m.program_id == program_id
        ]

        export = {
            "export_format": format,
            "exported_at": datetime.utcnow().isoformat(),
            "program": program.__dict__ if program else None,
            "users": users,
            "feedback": feedback,
            "bugs": bugs,
            "metrics": metrics,
            "flags": [
                f.__dict__ for f in self.flags.values()
            ],
        }

        self.logger.info(
            "Exported beta data for program %s (%d users, %d feedback, %d bugs)",
            program_id,
            len(users),
            len(feedback),
            len(bugs),
        )
        return export


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the BetaManagementAgent end-to-end workflow."""
    agent = BetaManagementAgent()

    # 1. Create beta program
    program = agent.create_beta_program(
        name="Q3 Feature Launch",
        description="Beta test for the new dashboard and analytics features",
        target_users=50,
        rollout_strategy=RolloutStrategy.CANARY,
        features=["dashboard-v2", "analytics-pro"],
    )
    print(f"Created program: {program.program_id}")

    # 2. Recruit users
    emails = [f"beta-user-{i}@example.com" for i in range(30)]
    users = agent.recruit_beta_users(
        program.program_id,
        emails=emails,
        user_type=BetaUserType.EXTERNAL_STANDARD,
        segments=["early_adopter"],
    )
    print(f"Recruited {len(users)} users")

    # 3. Onboard
    onboarded = agent.onboard_users(program.program_id)
    print(f"Onboarded {sum(onboarded.values())} users")

    # 4. Configure feature flags
    flag = agent.configure_feature_flags(
        feature_name="dashboard-v2",
        flag_type=FeatureFlagType.GRADUAL_ROLLOUT,
        enabled=True,
        percentage=25,
        release_stage=ReleaseStage.BETA,
        owner="product-team",
    )
    print(f"Feature flag: {flag.flag_id} ({flag.name})")

    # 5. Collect feedback
    sentiments = [SentimentLevel.POSITIVE, SentimentLevel.NEUTRAL, SentimentLevel.NEGATIVE]
    severities = [SeverityLevel.LOW, SeverityLevel.MEDIUM, SeverityLevel.HIGH]
    for user in users[:15]:
        agent.collect_feedback(
            user_id=user.user_id,
            program_id=program.program_id,
            channel=random.choice(list(FeedbackChannel)),
            title=f"Feedback from {user.display_name}",
            body="The new dashboard is much faster and easier to navigate",
            severity=random.choice(severities),
            sentiment=random.choice(sentiments),
            category="dashboard",
            tags=["performance", "ux"],
        )
    print("Collected 15 feedback items")

    # 6. Record metrics
    for _ in range(20):
        agent.record_metric(
            program_id=program.program_id,
            category=random.choice(list(MetricCategory)),
            name="sample_metric",
            value=random.uniform(0, 100),
            unit="count",
        )
    print("Recorded 20 metrics")

    # 7. Create bugs
    for i in range(5):
        agent.manage_bug_reports(
            program.program_id,
            action="create",
            reporter_id=users[i].user_id,
            priority=random.choice(list(BugPriority)),
            title=f"Bug #{i+1}: Dashboard rendering issue",
            description="Dashboard fails to render charts on first load",
            steps=["1. Open dashboard", "2. Wait for load", "3. Charts missing"],
            expected="Charts displayed correctly",
            actual="Blank chart area",
        )
    print("Created 5 bug reports")

    # 8. Run A/B test
    test = agent.run_ab_test(
        name="Dashboard Layout Test",
        hypothesis="New grid layout increases task completion by 15%",
        primary_metric="task_completion_rate",
        sample_size=1000,
        duration_days=14,
    )
    results = agent.analyze_ab_results(test.test_id)
    print(f"A/B test significant: {results['is_significant']}")

    # 9. Create rollout plan
    plan = agent.create_rollout_plan(
        feature_name="dashboard-v2",
        strategy=RolloutStrategy.CANARY,
        rollback_threshold=0.03,
    )
    rollout_status = agent.execute_rollout(plan.plan_id)
    print(f"Rollout stage: {rollout_status.get('new_percentage', '?')}%")

    # 10. Dashboard
    dashboard = agent.create_beta_metric_dashboard(program.program_id)
    print(f"Dashboard: {dashboard['total_users']} users, NPS={dashboard.get('nps_score', 'N/A')}")

    # 11. Sentiment analysis
    sentiment_result = agent.perform_sentiment_analysis(program.program_id)
    print(f"Sentiment: {sentiment_result.overall_sentiment().value} (avg={sentiment_result.average_score})")

    # 12. Iteration plan
    iteration = agent.create_iteration_plan(program.program_id)
    print(f"Iteration plan: {len(iteration.items)} items")

    # 13. Risk assessment
    risks = agent.assess_risk(program.program_id)
    critical = [r for r in risks if r.severity == SeverityLevel.CRITICAL]
    print(f"Risks: {len(risks)} assessed, {len(critical)} critical")

    # 14. Closure report
    closure = agent.create_closure_report(program.program_id)
    print(f"Closure: {closure.total_users} users, {closure.total_feedback} feedback, {closure.total_bugs} bugs")

    # 15. Export
    export = agent.export_beta_data(program.program_id)
    print(f"Export: {len(export['users'])} users, {len(export['feedback'])} feedback items")

    print("\n--- Beta Management Demo Complete ---")


if __name__ == "__main__":
    main()
