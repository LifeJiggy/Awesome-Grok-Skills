"""
Product Management Agent
Product strategy, roadmap planning, feature prioritization, user stories,
OKRs, product analytics, A/B testing, and go-to-market coordination.

Comprehensive implementation featuring:
- Product strategy and vision management
- Roadmap planning with multi-horizon support
- Feature prioritization frameworks (RICE, MoSCoW, Value vs Effort)
- User story creation and management
- OKR tracking and progress monitoring
- Product analytics and funnel analysis
- A/B testing framework
- Go-to-market planning
- Stakeholder communication
- Competitive analysis
- Customer feedback processing
- Sprint and release planning
"""

from __future__ import annotations

import abc
import csv
import hashlib
import json
import logging
import math
import sqlite3
import statistics
import time
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
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Priority(str, Enum):
    """Feature and task priority levels."""
    P0_CRITICAL = "p0_critical"
    P1_HIGH = "p1_high"
    P2_MEDIUM = "p2_medium"
    P3_LOW = "p3_low"
    P4_WISHLIST = "p4_wishlist"


class FeatureStatus(str, Enum):
    """Lifecycle states for a feature."""
    IDEA = "idea"
    BACKLOG = "backlog"
    PLANNED = "planned"
    IN_DESIGN = "in_design"
    IN_DEVELOPMENT = "in_development"
    TESTING = "testing"
    STAGING = "staging"
    LAUNCHED = "launched"
    MONITORING = "monitoring"
    MATURE = "mature"
    SUNSET = "sunset"


class RoadmapHorizon(str, Enum):
    """Planning horizons for roadmap items."""
    NOW = "now"
    NEXT = "next"
    LATER = "later"
    FUTURE = "future"


class StoryStatus(str, Enum):
    """User story workflow states."""
    DRAFT = "draft"
    REFINED = "refined"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class OKRStatus(str, Enum):
    """Objective and key result tracking states."""
    NOT_STARTED = "not_started"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BEHIND = "behind"
    ACHIEVED = "achieved"
    MISSED = "missed"


class ExperimentStatus(str, Enum):
    """A/B test lifecycle states."""
    HYPOTHESIS = "hypothesis"
    DESIGNED = "designed"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ANALYZING = "analyzing"
    DECIDED = "decided"


class GTMPhase(str, Enum):
    """Go-to-market phases."""
    DISCOVERY = "discovery"
    VALIDATION = "validation"
    PREPARE = "prepare"
    LAUNCH = "launch"
    POST_LAUNCH = "post_launch"


class FeedbackType(str, Enum):
    """Types of customer feedback."""
    FEATURE_REQUEST = "feature_request"
    BUG_REPORT = "bug_report"
    USABILITY = "usability"
    PRAISE = "praise"
    COMPLAINT = "complaint"
    QUESTION = "question"
    CHURN_SIGNAL = "churn_signal"


class MetricType(str, Enum):
    """Types of product metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    RATE = "rate"
    PERCENTAGE = "percentage"
    CURRENCY = "currency"


class StakeholderRole(str, Enum):
    """Roles of product stakeholders."""
    EXECUTIVE = "executive"
    ENGINEERING = "engineering"
    DESIGN = "design"
    MARKETING = "marketing"
    SALES = "sales"
    SUPPORT = "support"
    CUSTOMER = "customer"
    PARTNER = "partner"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ProductVision:
    """High-level product vision and mission."""
    vision_id: str
    statement: str
    mission: str
    target_users: List[str]
    value_proposition: str
    key_differentiators: List[str]
    success_metrics: List[str]
    created_at: datetime
    updated_at: datetime
    version: int = 1


@dataclass
class Feature:
    """A product feature with full metadata."""
    feature_id: str
    name: str
    description: str
    priority: Priority
    status: FeatureStatus
    horizon: RoadmapHorizon
    effort: int
    value: int
    impact: float
    confidence: float
    owner: str
    tags: List[str]
    dependencies: List[str]
    success_criteria: List[str]
    created_at: datetime
    updated_at: datetime
    launched_at: Optional[datetime] = None
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserStory:
    """A user story following INVEST criteria."""
    story_id: str
    title: str
    user_role: str
    action: str
    benefit: str
    acceptance_criteria: List[str]
    priority: Priority
    status: StoryStatus
    estimate: float
    tags: List[str]
    feature_id: Optional[str]
    sprint_id: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class Objective:
    """An OKR objective."""
    objective_id: str
    statement: str
    owner: str
    status: OKRStatus
    confidence: float
    key_results: List[KeyResult]
    quarter: str
    created_at: datetime
    updated_at: datetime


@dataclass
class KeyResult:
    """A measurable key result for an objective."""
    kr_id: str
    statement: str
    metric: str
    start_value: float
    target_value: float
    current_value: float
    unit: str
    owner: str
    status: OKRStatus
    check_in_date: Optional[datetime] = None


@dataclass
class ABTest:
    """An A/B test experiment."""
    experiment_id: str
    name: str
    hypothesis: str
    metric: str
    control_variant: Variant
    treatment_variants: List[Variant]
    status: ExperimentStatus
    sample_size: int
    confidence_level: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    results: Optional[ExperimentResults] = None


@dataclass
class Variant:
    """A variant in an A/B test."""
    variant_id: str
    name: str
    description: str
    traffic_percentage: float
    is_control: bool
    config: Dict[str, Any]


@dataclass
class ExperimentResults:
    """Results from an A/B test."""
    control_mean: float
    treatment_means: Dict[str, float]
    p_values: Dict[str, float]
    confidence_intervals: Dict[str, Tuple[float, float]]
    statistical_power: float
    winner: Optional[str]
    recommendation: str


@dataclass
class Feedback:
    """Customer feedback item."""
    feedback_id: str
    source: str
    feedback_type: FeedbackType
    title: str
    body: str
    customer_id: str
    sentiment: float
    tags: List[str]
    votes: int
    created_at: datetime
    processed: bool = False
    feature_id: Optional[str] = None


@dataclass
class ProductMetric:
    """A tracked product metric."""
    metric_id: str
    name: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    dimensions: Dict[str, str]
    metadata: Dict[str, Any]


@dataclass
class Release:
    """A product release."""
    release_id: str
    version: str
    name: str
    features: List[str]
    status: str
    release_date: Optional[datetime]
    changelog: List[str]
    owner: str


@dataclass
class Stakeholder:
    """A product stakeholder."""
    stakeholder_id: str
    name: str
    role: StakeholderRole
    email: str
    influence: float
    interest: float
    communication_preference: str
    last_contact: Optional[datetime]


@dataclass
class Sprint:
    """An agile sprint."""
    sprint_id: str
    name: str
    start_date: datetime
    end_date: datetime
    goal: str
    stories: List[str]
    capacity: float
    velocity: Optional[float]


@dataclass
class GTMPlan:
    """Go-to-market plan."""
    plan_id: str
    feature_id: str
    phase: GTMPhase
    activities: List[GTMActivity]
    timeline: Dict[str, datetime]
    budget: float
    owner: str
    success_metrics: List[str]


@dataclass
class GTMActivity:
    """An activity within a GTM plan."""
    activity_id: str
    name: str
    description: str
    phase: GTMPhase
    owner: str
    due_date: datetime
    status: str
    dependencies: List[str]


@dataclass
class CompetitiveProfile:
    """Competitive intelligence profile."""
    competitor_id: str
    name: str
    positioning: str
    strengths: List[str]
    weaknesses: List[str]
    pricing: Dict[str, Any]
    features: List[str]
    market_share: float
    last_updated: datetime


@dataclass
class ProductConfig:
    """Configuration for the product agent."""
    default_currency: str = "USD"
    roadmap_horizons: int = 3
    okr_quarter: str = "Q1 2024"
    confidence_threshold: float = 0.7
    min_sample_size: int = 1000
    significance_level: float = 0.05
    max_sprint_stories: int = 10
    feedback_vote_threshold: int = 10
    metric_retention_days: int = 90


# ---------------------------------------------------------------------------
# Abstract Base
# ---------------------------------------------------------------------------

class BaseAnalyzer(abc.ABC):
    """Base class for analysis components."""

    @abc.abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        ...


# ---------------------------------------------------------------------------
# Product Strategy Manager
# ---------------------------------------------------------------------------

class ProductStrategyManager:
    """Manages product vision, strategy, and competitive positioning."""

    def __init__(self) -> None:
        self.vision: Optional[ProductVision] = None
        self.strategies: Dict[str, Dict[str, Any]] = {}
        self.competitors: Dict[str, CompetitiveProfile] = {}
        self._history: List[Dict[str, Any]] = []

    def define_vision(
        self,
        statement: str,
        mission: str,
        target_users: List[str],
        value_proposition: str,
        differentiators: List[str],
        success_metrics: List[str],
    ) -> ProductVision:
        if not statement:
            raise ValueError("vision statement must not be empty")
        if not target_users:
            raise ValueError("at least one target user segment required")
        now = datetime.utcnow()
        self.vision = ProductVision(
            vision_id=str(uuid.uuid4())[:12],
            statement=statement,
            mission=mission,
            target_users=target_users,
            value_proposition=value_proposition,
            key_differentiators=differentiators,
            success_metrics=success_metrics,
            created_at=now,
            updated_at=now,
        )
        self._log_change("vision_defined", {"statement": statement[:100]})
        logger.info("Product vision defined: %s", self.vision.vision_id)
        return self.vision

    def update_vision(self, **kwargs: Any) -> ProductVision:
        if not self.vision:
            raise RuntimeError("vision not yet defined")
        for key, value in kwargs.items():
            if hasattr(self.vision, key) and key not in ("vision_id", "created_at"):
                setattr(self.vision, key, value)
        self.vision.updated_at = datetime.utcnow()
        self.vision.version += 1
        self._log_change("vision_updated", kwargs)
        return self.vision

    def define_strategy(
        self,
        name: str,
        goals: List[str],
        time_horizon: str,
        assumptions: List[str],
        risks: List[str],
    ) -> Dict[str, Any]:
        if not name:
            raise ValueError("strategy name required")
        strategy = {
            "strategy_id": str(uuid.uuid4())[:12],
            "name": name,
            "goals": goals,
            "time_horizon": time_horizon,
            "assumptions": assumptions,
            "risks": risks,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "progress": 0.0,
            "milestones": [],
        }
        self.strategies[strategy["strategy_id"]] = strategy
        logger.info("Strategy defined: %s", name)
        return strategy

    def add_competitor(
        self,
        name: str,
        positioning: str,
        strengths: List[str],
        weaknesses: List[str],
        pricing: Dict[str, Any],
        features: List[str],
        market_share: float,
    ) -> CompetitiveProfile:
        profile = CompetitiveProfile(
            competitor_id=str(uuid.uuid4())[:12],
            name=name,
            positioning=positioning,
            strengths=strengths,
            weaknesses=weaknesses,
            pricing=pricing,
            features=features,
            market_share=market_share,
            last_updated=datetime.utcnow(),
        )
        self.competitors[profile.competitor_id] = profile
        logger.info("Competitor added: %s", name)
        return profile

    def competitive_analysis(self) -> Dict[str, Any]:
        if not self.competitors:
            return {"analysis": "no competitors tracked"}
        total_share = sum(c.market_share for c in self.competitors.values())
        all_strengths: List[str] = []
        all_weaknesses: List[str] = []
        for c in self.competitors.values():
            all_strengths.extend(c.strengths)
            all_weaknesses.extend(c.weaknesses)
        return {
            "competitor_count": len(self.competitors),
            "total_market_share": total_share,
            "our_remaining_share": max(0, 1.0 - total_share),
            "top_competitors": sorted(
                self.competitors.values(),
                key=lambda c: c.market_share,
                reverse=True,
            )[:5],
            "common_strengths": self._most_common(all_strengths),
            "common_weaknesses": self._most_common(all_weaknesses),
            "gaps_in_market": self._identify_gaps(),
        }

    def swot_analysis(self) -> Dict[str, List[str]]:
        return {
            "strengths": self._infer_strengths(),
            "weaknesses": self._infer_weaknesses(),
            "opportunities": self._identify_market_opportunities(),
            "threats": self._identify_threats(),
        }

    def market_sizing(self, market_data: Dict[str, float]) -> Dict[str, Any]:
        tam = market_data.get("total_addressable_market", 0)
        sam = market_data.get("serviceable_addressable_market", 0)
        som = market_data.get("serviceable_obtainable_market", 0)
        return {
            "tam": tam,
            "sam": sam,
            "som": som,
            "sam_to_tam_ratio": sam / tam if tam else 0,
            "som_to_sam_ratio": som / sam if sam else 0,
            "capture_rate": som / tam if tam else 0,
        }

    def _log_change(self, action: str, details: Dict[str, Any]) -> None:
        self._history.append({
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def _most_common(self, items: List[str]) -> List[Tuple[str, int]]:
        counts: Dict[str, int] = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

    def _identify_gaps(self) -> List[str]:
        return [
            "advanced analytics",
            "enterprise SSO",
            "mobile offline mode",
            "API marketplace",
            "real-time collaboration",
        ]

    def _infer_strengths(self) -> List[str]:
        if self.vision:
            return list(self.vision.key_differentiators)
        return ["innovation", "customer focus", "agile development"]

    def _infer_weaknesses(self) -> List[str]:
        return ["brand awareness", "enterprise features", "global reach"]

    def _identify_market_opportunities(self) -> List[str]:
        return [
            "AI/ML integration",
            "emerging markets",
            "vertical expansion",
            "platform ecosystem",
        ]

    def _identify_threats(self) -> List[str]:
        threats = []
        for c in self.competitors.values():
            if c.market_share > 0.2:
                threats.append(f"dominant competitor: {c.name}")
        threats.extend([
            "regulatory changes",
            "economic downturn",
            "technology disruption",
        ])
        return threats


# ---------------------------------------------------------------------------
# Roadmap Planner
# ---------------------------------------------------------------------------

class RoadmapPlanner:
    """Manages product roadmap with horizon-based planning."""

    def __init__(self) -> None:
        self.features: Dict[str, Feature] = {}
        self.releases: Dict[str, Release] = {}
        self._allocation: Dict[RoadmapHorizon, List[str]] = {
            h: [] for h in RoadmapHorizon
        }

    def add_feature(self, feature: Feature) -> None:
        self.features[feature.feature_id] = feature
        self._allocation[feature.horizon].append(feature.feature_id)
        logger.info("Feature added to roadmap: %s [%s]", feature.name, feature.horizon.value)

    def remove_feature(self, feature_id: str) -> None:
        if feature_id not in self.features:
            raise ValueError(f"feature {feature_id} not found")
        feature = self.features.pop(feature_id)
        self._allocation[feature.horizon].remove(feature_id)

    def reprioritize(
        self,
        feature_id: str,
        new_priority: Priority,
        new_horizon: Optional[RoadmapHorizon] = None,
    ) -> Feature:
        if feature_id not in self.features:
            raise ValueError(f"feature {feature_id} not found")
        feature = self.features[feature_id]
        old_horizon = feature.horizon
        feature.priority = new_priority
        feature.updated_at = datetime.utcnow()
        if new_horizon and new_horizon != old_horizon:
            self._allocation[old_horizon].remove(feature_id)
            self._allocation[new_horizon].append(feature_id)
            feature.horizon = new_horizon
        return feature

    def get_roadmap(self) -> Dict[str, List[Feature]]:
        roadmap: Dict[str, List[Feature]] = {}
        for horizon, feature_ids in self._allocation.items():
            roadmap[horizon.value] = [
                self.features[fid]
                for fid in feature_ids
                if fid in self.features
            ]
            roadmap[horizon.value].sort(
                key=lambda f: (list(Priority).index(f.priority), -f.value)
            )
        return roadmap

    def roadmap_summary(self) -> Dict[str, Any]:
        roadmap = self.get_roadmap()
        summary = {}
        for horizon, features in roadmap.items():
            summary[horizon] = {
                "count": len(features),
                "total_effort": sum(f.effort for f in features),
                "avg_value": (
                    statistics.mean(f.value for f in features) if features else 0
                ),
                "priorities": {
                    p.value: sum(1 for f in features if f.priority == p)
                    for p in Priority
                },
            }
        return summary

    def create_release(
        self,
        version: str,
        name: str,
        feature_ids: List[str],
        release_date: Optional[datetime] = None,
        owner: str = "",
    ) -> Release:
        missing = [fid for fid in feature_ids if fid not in self.features]
        if missing:
            raise ValueError(f"features not found: {missing}")
        release = Release(
            release_id=str(uuid.uuid4())[:12],
            version=version,
            name=name,
            features=feature_ids,
            status="planned",
            release_date=release_date,
            changelog=[self.features[fid].name for fid in feature_ids],
            owner=owner,
        )
        self.releases[release.release_id] = release
        logger.info("Release created: %s (%s)", name, version)
        return release

    def capacity_check(self, horizon: RoadmapHorizon, max_effort: int) -> Dict[str, Any]:
        features = self._allocation.get(horizon, [])
        total_effort = sum(
            self.features[fid].effort
            for fid in features
            if fid in self.features
        )
        return {
            "horizon": horizon.value,
            "total_effort": total_effort,
            "max_effort": max_effort,
            "utilization": total_effort / max_effort if max_effort else 0,
            "is_overloaded": total_effort > max_effort,
            "feature_count": len(features),
        }

    def transition_features(
        self,
        from_horizon: RoadmapHorizon,
        to_horizon: RoadmapHorizon,
        feature_ids: List[str],
    ) -> List[Feature]:
        moved: List[Feature] = []
        for fid in feature_ids:
            if fid in self.features:
                feature = self.features[fid]
                if fid in self._allocation[from_horizon]:
                    self._allocation[from_horizon].remove(fid)
                    self._allocation[to_horizon].append(fid)
                    feature.horizon = to_horizon
                    feature.updated_at = datetime.utcnow()
                    moved.append(feature)
        return moved

    def dependencies_graph(self) -> Dict[str, List[str]]:
        graph: Dict[str, List[str]] = {}
        for fid, feature in self.features.items():
            graph[fid] = feature.dependencies
        return graph

    def blocked_features(self) -> List[Feature]:
        blocked: List[Feature] = []
        for fid, feature in self.features.items():
            for dep_id in feature.dependencies:
                dep = self.features.get(dep_id)
                if dep and dep.status not in (FeatureStatus.LAUNCHED, FeatureStatus.MATURE):
                    blocked.append(feature)
                    break
        return blocked


# ---------------------------------------------------------------------------
# Feature Prioritizer
# ---------------------------------------------------------------------------

class FeaturePrioritizer:
    """Prioritizes features using multiple frameworks."""

    def __init__(self) -> None:
        self.weights: Dict[str, float] = {
            "value": 0.35,
            "effort": 0.25,
            "impact": 0.20,
            "confidence": 0.10,
            "strategic_alignment": 0.10,
        }

    def rice_score(self, feature: Feature, reach: int, impact: float, confidence: float) -> float:
        """Calculate RICE score: (Reach * Impact * Confidence) / Effort."""
        if feature.effort <= 0:
            raise ValueError("effort must be positive for RICE")
        return (reach * impact * confidence) / feature.effort

    def moscow_classification(
        self, features: List[Feature], must_haves: List[str]
    ) -> Dict[str, List[Feature]]:
        """Classify features using MoSCoW method."""
        result: Dict[str, List[Feature]] = {
            "must_have": [],
            "should_have": [],
            "could_have": [],
            "wont_have": [],
        }
        for f in features:
            if f.feature_id in must_haves or f.priority == Priority.P0_CRITICAL:
                result["must_have"].append(f)
            elif f.priority == Priority.P1_HIGH:
                result["should_have"].append(f)
            elif f.priority == Priority.P2_MEDIUM:
                result["could_have"].append(f)
            else:
                result["wont_have"].append(f)
        return result

    def value_vs_effort_matrix(self, features: List[Feature]) -> Dict[str, List[Feature]]:
        """Categorize features into a 2x2 value vs effort matrix."""
        if not features:
            return {"quick_wins": [], "big_bets": [], "fill_ins": [], "money_pits": []}
        values = [f.value for f in features]
        efforts = [f.effort for f in features]
        median_value = statistics.median(values)
        median_effort = statistics.median(efforts)
        matrix: Dict[str, List[Feature]] = {
            "quick_wins": [],
            "big_bets": [],
            "fill_ins": [],
            "money_pits": [],
        }
        for f in features:
            high_value = f.value >= median_value
            low_effort = f.effort <= median_effort
            if high_value and low_effort:
                matrix["quick_wins"].append(f)
            elif high_value and not low_effort:
                matrix["big_bets"].append(f)
            elif not high_value and low_effort:
                matrix["fill_ins"].append(f)
            else:
                matrix["money_pits"].append(f)
        return matrix

    def weighted_scoring(self, features: List[Feature]) -> List[Tuple[Feature, float]]:
        """Calculate weighted priority score for each feature."""
        scored: List[Tuple[Feature, float]] = []
        for f in features:
            score = (
                f.value * self.weights["value"]
                + (10 - min(f.effort, 10)) * self.weights["effort"]
                + f.impact * 10 * self.weights["impact"]
                + f.confidence * 10 * self.weights["confidence"]
            )
            scored.append((f, round(score, 2)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def stack_ranking(self, features: List[Feature]) -> List[Feature]:
        """Stack rank features by composite score."""
        scored = self.weighted_scoring(features)
        return [f for f, _ in scored]

    def set_weights(self, weights: Dict[str, float]) -> None:
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"weights must sum to 1.0, got {total}")
        self.weights.update(weights)


# ---------------------------------------------------------------------------
# User Story Manager
# ---------------------------------------------------------------------------

class UserStoryManager:
    """Creates and manages user stories with INVEST validation."""

    VALID_TRANSITIONS: Dict[StoryStatus, Set[StoryStatus]] = {
        StoryStatus.DRAFT: {StoryStatus.REFINED},
        StoryStatus.REFINED: {StoryStatus.READY, StoryStatus.DRAFT},
        StoryStatus.READY: {StoryStatus.IN_PROGRESS},
        StoryStatus.IN_PROGRESS: {StoryStatus.IN_REVIEW},
        StoryStatus.IN_REVIEW: {StoryStatus.DONE, StoryStatus.IN_PROGRESS},
        StoryStatus.DONE: set(),
    }

    def __init__(self) -> None:
        self.stories: Dict[str, UserStory] = {}
        self._templates: Dict[str, Dict[str, str]] = {}

    def create_story(
        self,
        user_role: str,
        action: str,
        benefit: str,
        acceptance_criteria: List[str],
        priority: Priority = Priority.P2_MEDIUM,
        estimate: float = 1.0,
        tags: Optional[List[str]] = None,
        feature_id: Optional[str] = None,
    ) -> UserStory:
        title = f"As a {user_role}, I want to {action}, so that {benefit}"
        story = UserStory(
            story_id=str(uuid.uuid4())[:12],
            title=title,
            user_role=user_role,
            action=action,
            benefit=benefit,
            acceptance_criteria=acceptance_criteria,
            priority=priority,
            status=StoryStatus.DRAFT,
            estimate=estimate,
            tags=tags or [],
            feature_id=feature_id,
            sprint_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.stories[story.story_id] = story
        logger.info("User story created: %s", story.story_id)
        return story

    def validate_invest(self, story: UserStory) -> Dict[str, bool]:
        """Validate story against INVEST criteria."""
        return {
            "independent": len(story.dependencies) == 0 if hasattr(story, "dependencies") else True,
            "negotiable": story.status in (StoryStatus.DRAFT, StoryStatus.REFINED),
            "valuable": bool(story.benefit),
            "estimable": story.estimate > 0,
            "small": story.estimate <= 8,
            "testable": len(story.acceptance_criteria) > 0,
        }

    def transition(self, story_id: str, new_status: StoryStatus) -> UserStory:
        if story_id not in self.stories:
            raise ValueError(f"story {story_id} not found")
        story = self.stories[story_id]
        allowed = self.VALID_TRANSITIONS.get(story.status, set())
        if new_status not in allowed:
            raise ValueError(
                f"cannot transition from {story.status.value} to {new_status.value}"
            )
        story.status = new_status
        story.updated_at = datetime.utcnow()
        return story

    def ready_stories(self) -> List[UserStory]:
        return [s for s in self.stories.values() if s.status == StoryStatus.READY]

    def stories_by_priority(self) -> List[UserStory]:
        return sorted(self.stories.values(), key=lambda s: list(Priority).index(s.priority))

    def story_points_total(self, status: Optional[StoryStatus] = None) -> float:
        stories = self.stories.values()
        if status:
            stories = [s for s in stories if s.status == status]
        return sum(s.estimate for s in stories)

    def create_from_template(self, template_name: str, **overrides: Any) -> UserStory:
        if template_name not in self._templates:
            raise ValueError(f"template {template_name} not found")
        tmpl = self._templates[template_name]
        return self.create_story(
            user_role=overrides.get("user_role", tmpl.get("user_role", "user")),
            action=overrides.get("action", tmpl.get("action", "")),
            benefit=overrides.get("benefit", tmpl.get("benefit", "")),
            acceptance_criteria=overrides.get(
                "acceptance_criteria",
                json.loads(tmpl.get("acceptance_criteria", "[]")),
            ),
            priority=overrides.get("priority", Priority.P2_MEDIUM),
            estimate=overrides.get("estimate", 1.0),
            tags=overrides.get("tags", []),
            feature_id=overrides.get("feature_id"),
        )

    def add_template(self, name: str, template: Dict[str, str]) -> None:
        self._templates[name] = template


# ---------------------------------------------------------------------------
# OKR Manager
# ---------------------------------------------------------------------------

class OKRManager:
    """Tracks Objectives and Key Results."""

    def __init__(self) -> None:
        self.objectives: Dict[str, Objective] = {}
        self._check_ins: List[Dict[str, Any]] = []

    def create_objective(
        self,
        statement: str,
        owner: str,
        quarter: str,
        key_results: List[Dict[str, Any]],
    ) -> Objective:
        krs: List[KeyResult] = []
        for kr_data in key_results:
            kr = KeyResult(
                kr_id=str(uuid.uuid4())[:12],
                statement=kr_data["statement"],
                metric=kr_data["metric"],
                start_value=kr_data.get("start_value", 0),
                target_value=kr_data["target_value"],
                current_value=kr_data.get("start_value", 0),
                unit=kr_data.get("unit", ""),
                owner=kr_data.get("owner", owner),
                status=OKRStatus.NOT_STARTED,
            )
            krs.append(kr)
        objective = Objective(
            objective_id=str(uuid.uuid4())[:12],
            statement=statement,
            owner=owner,
            status=OKRStatus.NOT_STARTED,
            confidence=0.5,
            key_results=krs,
            quarter=quarter,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.objectives[objective.objective_id] = objective
        logger.info("Objective created: %s", statement[:60])
        return objective

    def check_in(
        self,
        objective_id: str,
        kr_updates: Dict[str, float],
        confidence: float,
        notes: str = "",
    ) -> Objective:
        if objective_id not in self.objectives:
            raise ValueError(f"objective {objective_id} not found")
        obj = self.objectives[objective_id]
        obj.confidence = confidence
        for kr in obj.key_results:
            if kr.kr_id in kr_updates:
                kr.current_value = kr_updates[kr.kr_id]
                kr.check_in_date = datetime.utcnow()
                kr.status = self._compute_kr_status(kr)
        obj.status = self._compute_objective_status(obj)
        obj.updated_at = datetime.utcnow()
        self._check_ins.append({
            "objective_id": objective_id,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": confidence,
            "notes": notes,
        })
        return obj

    def progress(self, objective_id: str) -> Dict[str, Any]:
        if objective_id not in self.objectives:
            raise ValueError(f"objective {objective_id} not found")
        obj = self.objectives[objective_id]
        kr_progress: List[Dict[str, Any]] = []
        for kr in obj.key_results:
            range_size = kr.target_value - kr.start_value
            if range_size == 0:
                pct = 100.0 if kr.current_value >= kr.target_value else 0.0
            else:
                pct = ((kr.current_value - kr.start_value) / range_size) * 100
            kr_progress.append({
                "kr_id": kr.kr_id,
                "statement": kr.statement,
                "progress_pct": round(min(pct, 100), 1),
                "status": kr.status.value,
            })
        overall = (
            statistics.mean(kp["progress_pct"] for kp in kr_progress)
            if kr_progress else 0
        )
        return {
            "objective": obj.statement,
            "quarter": obj.quarter,
            "overall_progress": round(overall, 1),
            "confidence": obj.confidence,
            "status": obj.status.value,
            "key_results": kr_progress,
        }

    def dashboard(self) -> Dict[str, Any]:
        objectives = list(self.objectives.values())
        if not objectives:
            return {"objectives": [], "overall_health": "no_data"}
        statuses = [o.status.value for o in objectives]
        on_track = statuses.count(OKRStatus.ON_TRACK.value)
        health = "green" if on_track > len(objectives) * 0.6 else "yellow"
        if statuses.count(OKRStatus.BEHIND.value) > len(objectives) * 0.3:
            health = "red"
        return {
            "total_objectives": len(objectives),
            "status_distribution": {
                s.value: statuses.count(s.value) for s in OKRStatus
            },
            "overall_health": health,
            "avg_confidence": round(
                statistics.mean(o.confidence for o in objectives), 2
            ),
        }

    def _compute_kr_status(self, kr: KeyResult) -> OKRStatus:
        rng = kr.target_value - kr.start_value
        if rng == 0:
            return OKRStatus.ACHIEVED if kr.current_value >= kr.target_value else OKRStatus.MISSED
        pct = (kr.current_value - kr.start_value) / rng
        if pct >= 1.0:
            return OKRStatus.ACHIEVED
        if pct >= 0.7:
            return OKRStatus.ON_TRACK
        if pct >= 0.4:
            return OKRStatus.AT_RISK
        return OKRStatus.BEHIND

    def _compute_objective_status(self, obj: Objective) -> OKRStatus:
        kr_statuses = [kr.status for kr in obj.key_results]
        if all(s == OKRStatus.ACHIEVED for s in kr_statuses):
            return OKRStatus.ACHIEVED
        if any(s == OKRStatus.BEHIND for s in kr_statuses):
            return OKRStatus.BEHIND
        if obj.confidence >= 0.7:
            return OKRStatus.ON_TRACK
        return OKRStatus.AT_RISK


# ---------------------------------------------------------------------------
# Product Analytics
# ---------------------------------------------------------------------------

class ProductAnalytics:
    """Tracks and analyzes product metrics, funnels, and cohorts."""

    def __init__(self, config: Optional[ProductConfig] = None) -> None:
        self.config = config or ProductConfig()
        self.metrics: List[ProductMetric] = []
        self._funnels: Dict[str, List[str]] = {}
        self._events: List[Dict[str, Any]] = []

    def track_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        dimensions: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ProductMetric:
        metric = ProductMetric(
            metric_id=str(uuid.uuid4())[:12],
            name=name,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.utcnow(),
            dimensions=dimensions or {},
            metadata=metadata or {},
        )
        self.metrics.append(metric)
        return metric

    def record_event(self, event: Dict[str, Any]) -> None:
        event.setdefault("timestamp", datetime.utcnow().isoformat())
        event.setdefault("event_id", str(uuid.uuid4())[:12])
        self._events.append(event)

    def define_funnel(self, name: str, steps: List[str]) -> None:
        self._funnels[name] = steps

    def analyze_funnel(self, funnel_name: str) -> Dict[str, Any]:
        if funnel_name not in self._funnels:
            raise ValueError(f"funnel {funnel_name} not found")
        steps = self._funnels[funnel_name]
        step_counts: Dict[str, int] = {}
        for step in steps:
            step_counts[step] = sum(
                1 for e in self._events if e.get("event_type") == step
            )
        analysis: List[Dict[str, Any]] = []
        prev_count = None
        for step in steps:
            count = step_counts.get(step, 0)
            drop_off = 0.0
            if prev_count and prev_count > 0:
                drop_off = ((prev_count - count) / prev_count) * 100
            analysis.append({
                "step": step,
                "count": count,
                "drop_off_pct": round(drop_off, 1),
            })
            prev_count = count
        first = step_counts.get(steps[0], 0) if steps else 0
        last = step_counts.get(steps[-1], 0) if steps else 0
        overall_conversion = (last / first * 100) if first > 0 else 0
        return {
            "funnel": funnel_name,
            "steps": analysis,
            "overall_conversion": round(overall_conversion, 1),
        }

    def cohort_analysis(
        self, cohort_field: str, period_days: int = 30
    ) -> Dict[str, List[Dict[str, Any]]]:
        cohorts: Dict[str, List[Dict[str, Any]]] = {}
        for event in self._events:
            cohort_key = event.get(cohort_field, "unknown")
            cohorts.setdefault(cohort_key, []).append(event)
        result: Dict[str, List[Dict[str, Any]]] = {}
        for cohort_key, events in cohorts.items():
            period_counts: Dict[int, int] = {}
            for event in events:
                ts = event.get("timestamp", "")
                if isinstance(ts, str):
                    try:
                        dt = datetime.fromisoformat(ts)
                        period = int((dt.timestamp() // (period_days * 86400)))
                        period_counts[period] = period_counts.get(period, 0) + 1
                    except ValueError:
                        pass
            result[cohort_key] = [
                {"period": p, "count": c} for p, c in sorted(period_counts.items())
            ]
        return result

    def metric_summary(self, name: str, hours: int = 24) -> Dict[str, Any]:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        relevant = [
            m for m in self.metrics
            if m.name == name and m.timestamp >= cutoff
        ]
        if not relevant:
            return {"name": name, "count": 0, "summary": "no data"}
        values = [m.value for m in relevant]
        return {
            "name": name,
            "count": len(values),
            "mean": round(statistics.mean(values), 2),
            "median": round(statistics.median(values), 2),
            "min": min(values),
            "max": max(values),
            "stddev": round(statistics.stdev(values), 2) if len(values) > 1 else 0,
        }

    def retention_rate(
        self, users_field: str = "user_id", days: int = 7
    ) -> Dict[str, Any]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        active_users: Set[str] = set()
        returning_users: Set[str] = set()
        for event in self._events:
            uid = event.get(users_field, "")
            ts_str = event.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(ts_str) if isinstance(ts_str, str) else None
            except ValueError:
                dt = None
            if dt and dt >= cutoff:
                active_users.add(uid)
            elif dt and dt < cutoff:
                returning_users.add(uid)
        retained = active_users & returning_users
        total = active_users | returning_users
        return {
            "active_users": len(active_users),
            "retained_users": len(retained),
            "retention_rate": round(len(retained) / len(total) * 100, 1) if total else 0,
        }


# ---------------------------------------------------------------------------
# A/B Testing Framework
# ---------------------------------------------------------------------------

class ABTestManager:
    """Manages A/B test experiments with statistical analysis."""

    def __init__(self, config: Optional[ProductConfig] = None) -> None:
        self.config = config or ProductConfig()
        self.experiments: Dict[str, ABTest] = {}

    def create_experiment(
        self,
        name: str,
        hypothesis: str,
        metric: str,
        control: Dict[str, Any],
        treatments: List[Dict[str, Any]],
        sample_size: int = 1000,
        confidence_level: float = 0.95,
    ) -> ABTest:
        control_variant = Variant(
            variant_id=str(uuid.uuid4())[:12],
            name="control",
            description=control.get("description", "Original"),
            traffic_percentage=control.get("traffic", 50),
            is_control=True,
            config=control.get("config", {}),
        )
        treatment_variants = []
        for t in treatments:
            tv = Variant(
                variant_id=str(uuid.uuid4())[:12],
                name=t.get("name", "treatment"),
                description=t.get("description", ""),
                traffic_percentage=t.get("traffic", 50 / len(treatments)),
                is_control=False,
                config=t.get("config", {}),
            )
            treatment_variants.append(tv)
        experiment = ABTest(
            experiment_id=str(uuid.uuid4())[:12],
            name=name,
            hypothesis=hypothesis,
            metric=metric,
            control_variant=control_variant,
            treatment_variants=treatment_variants,
            status=ExperimentStatus.DESIGNED,
            sample_size=sample_size,
            confidence_level=confidence_level,
        )
        self.experiments[experiment.experiment_id] = experiment
        logger.info("A/B test created: %s", name)
        return experiment

    def start_experiment(self, experiment_id: str) -> ABTest:
        exp = self._get_experiment(experiment_id)
        if exp.status != ExperimentStatus.DESIGNED:
            raise ValueError(f"cannot start experiment in status {exp.status.value}")
        exp.status = ExperimentStatus.RUNNING
        exp.start_date = datetime.utcnow()
        return exp

    def stop_experiment(self, experiment_id: str) -> ABTest:
        exp = self._get_experiment(experiment_id)
        if exp.status != ExperimentStatus.RUNNING:
            raise ValueError(f"cannot stop experiment in status {exp.status.value}")
        exp.status = ExperimentStatus.COMPLETED
        exp.end_date = datetime.utcnow()
        return exp

    def analyze_results(
        self,
        experiment_id: str,
        control_data: List[float],
        treatment_data: Dict[str, List[float]],
    ) -> ExperimentResults:
        exp = self._get_experiment(experiment_id)
        control_mean = statistics.mean(control_data) if control_data else 0
        treatment_means: Dict[str, float] = {}
        p_values: Dict[str, float] = {}
        ci: Dict[str, Tuple[float, float]] = {}
        for name, data in treatment_data.items():
            t_mean = statistics.mean(data) if data else 0
            treatment_means[name] = t_mean
            p_val = self._welch_t_test(control_data, data)
            p_values[name] = p_val
            se = self._standard_error(data)
            ci[name] = (t_mean - 1.96 * se, t_mean + 1.96 * se)
        winner = None
        for name, p_val in p_values.items():
            if p_val < (1 - exp.confidence_level):
                if treatment_means[name] > control_mean:
                    winner = name
                break
        recommendation = (
            f"Deploy winner: {winner}" if winner
            else "No statistically significant winner. Continue testing."
        )
        power = self._statistical_power(control_data, list(treatment_data.values())[0] if treatment_data else [])
        results = ExperimentResults(
            control_mean=control_mean,
            treatment_means=treatment_means,
            p_values=p_values,
            confidence_intervals=ci,
            statistical_power=power,
            winner=winner,
            recommendation=recommendation,
        )
        exp.results = results
        exp.status = ExperimentStatus.DECIDED
        return results

    def _welch_t_test(self, sample_a: List[float], sample_b: List[float]) -> float:
        if len(sample_a) < 2 or len(sample_b) < 2:
            return 1.0
        mean_a = statistics.mean(sample_a)
        mean_b = statistics.mean(sample_b)
        var_a = statistics.variance(sample_a)
        var_b = statistics.variance(sample_b)
        n_a = len(sample_a)
        n_b = len(sample_b)
        se = math.sqrt(var_a / n_a + var_b / n_b)
        if se == 0:
            return 1.0
        t_stat = abs(mean_a - mean_b) / se
        df = (var_a / n_a + var_b / n_b) ** 2 / (
            (var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1)
        )
        p_value = 2 * (1 - self._t_cdf(t_stat, df))
        return round(p_value, 4)

    def _t_cdf(self, t: float, df: float) -> float:
        x = df / (df + t ** 2)
        return 1 - 0.5 * self._beta_incomplete(df / 2, 0.5, x)

    def _beta_incomplete(self, a: float, b: float, x: float) -> float:
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        bt = math.exp(
            math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
            + a * math.log(x) + b * math.log(1 - x)
        )
        if x < (a + 1) / (a + b + 2):
            return bt * self._beta_cf(a, b, x) / a
        return 1 - bt * self._beta_cf(b, a, 1 - x) / b

    def _beta_cf(self, a: float, b: float, x: float) -> float:
        max_iter = 200
        eps = 1e-10
        qab = a + b
        qap = a + 1
        qam = a - 1
        c = 1.0
        d = 1.0 - qab * x / qap
        if abs(d) < eps:
            d = eps
        d = 1.0 / d
        h = d
        for m in range(1, max_iter + 1):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1.0 + aa * d
            if abs(d) < eps:
                d = eps
            c = 1.0 + aa / c
            if abs(c) < eps:
                c = eps
            d = 1.0 / d
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1.0 + aa * d
            if abs(d) < eps:
                d = eps
            c = 1.0 + aa / c
            if abs(c) < eps:
                c = eps
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < eps:
                break
        return h

    def _standard_error(self, data: List[float]) -> float:
        if len(data) < 2:
            return 0.0
        return statistics.stdev(data) / math.sqrt(len(data))

    def _statistical_power(self, sample_a: List[float], sample_b: List[float]) -> float:
        if len(sample_a) < 2 or len(sample_b) < 2:
            return 0.0
        effect_size = abs(statistics.mean(sample_a) - statistics.mean(sample_b))
        pooled_std = math.sqrt(
            (statistics.variance(sample_a) + statistics.variance(sample_b)) / 2
        )
        if pooled_std == 0:
            return 1.0
        cohens_d = effect_size / pooled_std
        n = min(len(sample_a), len(sample_b))
        non_centrality = cohens_d * math.sqrt(n / 2)
        return round(min(self._normal_cdf(non_centrality - 1.96), 1.0), 3)

    def _normal_cdf(self, x: float) -> float:
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def _get_experiment(self, experiment_id: str) -> ABTest:
        if experiment_id not in self.experiments:
            raise ValueError(f"experiment {experiment_id} not found")
        return self.experiments[experiment_id]


# ---------------------------------------------------------------------------
# Feedback Processor
# ---------------------------------------------------------------------------

class FeedbackProcessor:
    """Processes and categorizes customer feedback."""

    def __init__(self) -> None:
        self.feedback: List[Feedback] = []
        self._votes: Dict[str, int] = {}

    def submit_feedback(
        self,
        source: str,
        feedback_type: FeedbackType,
        title: str,
        body: str,
        customer_id: str,
        tags: Optional[List[str]] = None,
    ) -> Feedback:
        fb = Feedback(
            feedback_id=str(uuid.uuid4())[:12],
            source=source,
            feedback_type=feedback_type,
            title=title,
            body=body,
            customer_id=customer_id,
            sentiment=self._analyze_sentiment(body),
            tags=tags or [],
            votes=0,
            created_at=datetime.utcnow(),
        )
        self.feedback.append(fb)
        logger.info("Feedback submitted: %s [%s]", title, feedback_type.value)
        return fb

    def vote(self, feedback_id: str) -> Feedback:
        fb = self._get_feedback(feedback_id)
        fb.votes += 1
        return fb

    def get_top_feedback(
        self, feedback_type: Optional[FeedbackType] = None, limit: int = 10
    ) -> List[Feedback]:
        items = self.feedback
        if feedback_type:
            items = [f for f in items if f.feedback_type == feedback_type]
        return sorted(items, key=lambda f: f.votes, reverse=True)[:limit]

    def categorize(self, feedback_id: str, feature_id: str) -> Feedback:
        fb = self._get_feedback(feedback_id)
        fb.feature_id = feature_id
        fb.processed = True
        return fb

    def sentiment_summary(self) -> Dict[str, Any]:
        if not self.feedback:
            return {"average": 0, "distribution": {}}
        sentiments = [f.sentiment for f in self.feedback]
        distribution = {"positive": 0, "neutral": 0, "negative": 0}
        for s in sentiments:
            if s > 0.3:
                distribution["positive"] += 1
            elif s < -0.3:
                distribution["negative"] += 1
            else:
                distribution["neutral"] += 1
        return {
            "average": round(statistics.mean(sentiments), 3),
            "distribution": distribution,
            "total": len(sentiments),
        }

    def _analyze_sentiment(self, text: str) -> float:
        positive_words = {
            "great", "love", "excellent", "amazing", "perfect", "best",
            "fantastic", "awesome", "wonderful", "helpful", "easy", "fast",
            "reliable", "intuitive", "powerful", "beautiful",
        }
        negative_words = {
            "bad", "terrible", "awful", "hate", "worst", "broken", "slow",
            "confusing", "ugly", "buggy", "crash", "error", "fail", "difficult",
            "frustrating", "annoying", "missing", "poor",
        }
        words = set(text.lower().split())
        pos = len(words & positive_words)
        neg = len(words & negative_words)
        total = pos + neg
        if total == 0:
            return 0.0
        return round((pos - neg) / total, 2)

    def _get_feedback(self, feedback_id: str) -> Feedback:
        for fb in self.feedback:
            if fb.feedback_id == feedback_id:
                return fb
        raise ValueError(f"feedback {feedback_id} not found")


# ---------------------------------------------------------------------------
# Go-to-Market Manager
# ---------------------------------------------------------------------------

class GTMManager:
    """Manages go-to-market plans and activities."""

    def __init__(self) -> None:
        self.plans: Dict[str, GTMPlan] = {}
        self._activity_log: List[Dict[str, Any]] = []

    def create_plan(
        self,
        feature_id: str,
        phase: GTMPhase,
        activities: List[Dict[str, Any]],
        timeline: Dict[str, datetime],
        budget: float,
        owner: str,
        success_metrics: List[str],
    ) -> GTMPlan:
        gtm_activities = []
        for act in activities:
            gtm_act = GTMActivity(
                activity_id=str(uuid.uuid4())[:12],
                name=act["name"],
                description=act.get("description", ""),
                phase=phase,
                owner=act.get("owner", owner),
                due_date=act.get("due_date", datetime.utcnow()),
                status="pending",
                dependencies=act.get("dependencies", []),
            )
            gtm_activities.append(gtm_act)
        plan = GTMPlan(
            plan_id=str(uuid.uuid4())[:12],
            feature_id=feature_id,
            phase=phase,
            activities=gtm_activities,
            timeline=timeline,
            budget=budget,
            owner=owner,
            success_metrics=success_metrics,
        )
        self.plans[plan.plan_id] = plan
        logger.info("GTM plan created for feature: %s", feature_id)
        return plan

    def advance_phase(self, plan_id: str) -> GTMPlan:
        plan = self._get_plan(plan_id)
        phases = list(GTMPhase)
        idx = phases.index(plan.phase)
        if idx < len(phases) - 1:
            plan.phase = phases[idx + 1]
        return plan

    def activity_status(self, plan_id: str) -> Dict[str, Any]:
        plan = self._get_plan(plan_id)
        statuses: Dict[str, int] = {}
        for act in plan.activities:
            statuses[act.status] = statuses.get(act.status, 0) + 1
        total = len(plan.activities)
        completed = statuses.get("completed", 0)
        return {
            "plan_id": plan_id,
            "current_phase": plan.phase.value,
            "total_activities": total,
            "completed": completed,
            "progress_pct": round(completed / total * 100, 1) if total else 0,
            "status_breakdown": statuses,
        }

    def budget_utilization(self, plan_id: str) -> Dict[str, Any]:
        plan = self._get_plan(plan_id)
        spent = sum(
            act.activity_id != "" for act in plan.activities
            if act.status == "completed"
        ) * (plan.budget / max(len(plan.activities), 1))
        return {
            "plan_id": plan_id,
            "total_budget": plan.budget,
            "estimated_spent": round(spent, 2),
            "remaining": round(plan.budget - spent, 2),
            "utilization_pct": round(spent / plan.budget * 100, 1) if plan.budget else 0,
        }

    def _get_plan(self, plan_id: str) -> GTMPlan:
        if plan_id not in self.plans:
            raise ValueError(f"GTM plan {plan_id} not found")
        return self.plans[plan_id]


# ---------------------------------------------------------------------------
# Stakeholder Manager
# ---------------------------------------------------------------------------

class StakeholderManager:
    """Manages product stakeholder communication and engagement."""

    def __init__(self) -> None:
        self.stakeholders: Dict[str, Stakeholder] = {}
        self._communications: List[Dict[str, Any]] = []

    def add_stakeholder(
        self,
        name: str,
        role: StakeholderRole,
        email: str,
        influence: float,
        interest: float,
        communication_preference: str = "email",
    ) -> Stakeholder:
        sh = Stakeholder(
            stakeholder_id=str(uuid.uuid4())[:12],
            name=name,
            role=role,
            email=email,
            influence=influence,
            interest=interest,
            communication_preference=communication_preference,
            last_contact=None,
        )
        self.stakeholders[sh.stakeholder_id] = sh
        logger.info("Stakeholder added: %s [%s]", name, role.value)
        return sh

    def engagement_matrix(self) -> Dict[str, List[Dict[str, Any]]]:
        matrix: Dict[str, List[Dict[str, Any]]] = {
            "manage_closely": [],
            "keep_satisfied": [],
            "keep_informed": [],
            "monitor": [],
        }
        for sh in self.stakeholders.values():
            entry = {"id": sh.stakeholder_id, "name": sh.name, "role": sh.role.value}
            if sh.influence >= 0.7 and sh.interest >= 0.7:
                matrix["manage_closely"].append(entry)
            elif sh.influence >= 0.7 and sh.interest < 0.7:
                matrix["keep_satisfied"].append(entry)
            elif sh.influence < 0.7 and sh.interest >= 0.7:
                matrix["keep_informed"].append(entry)
            else:
                matrix["monitor"].append(entry)
        return matrix

    def record_communication(
        self,
        stakeholder_id: str,
        channel: str,
        subject: str,
        summary: str,
    ) -> None:
        sh = self._get_stakeholder(stakeholder_id)
        sh.last_contact = datetime.utcnow()
        self._communications.append({
            "stakeholder_id": stakeholder_id,
            "channel": channel,
            "subject": subject,
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def communication_due(self, days: int = 7) -> List[Stakeholder]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [
            sh for sh in self.stakeholders.values()
            if sh.last_contact is None or sh.last_contact < cutoff
        ]

    def _get_stakeholder(self, stakeholder_id: str) -> Stakeholder:
        if stakeholder_id not in self.stakeholders:
            raise ValueError(f"stakeholder {stakeholder_id} not found")
        return self.stakeholders[stakeholder_id]


# ---------------------------------------------------------------------------
# Sprint Manager
# ---------------------------------------------------------------------------

class SprintManager:
    """Manages agile sprints and sprint planning."""

    def __init__(self) -> None:
        self.sprints: Dict[str, Sprint] = {}
        self._velocity_history: List[float] = []

    def create_sprint(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        goal: str,
        capacity: float,
        story_ids: Optional[List[str]] = None,
    ) -> Sprint:
        sprint = Sprint(
            sprint_id=str(uuid.uuid4())[:12],
            name=name,
            start_date=start_date,
            end_date=end_date,
            goal=goal,
            stories=story_ids or [],
            capacity=capacity,
            velocity=None,
        )
        self.sprints[sprint.sprint_id] = sprint
        logger.info("Sprint created: %s", name)
        return sprint

    def complete_sprint(self, sprint_id: str, completed_stories: int) -> Sprint:
        sprint = self._get_sprint(sprint_id)
        sprint.velocity = float(completed_stories)
        self._velocity_history.append(completed_stories)
        return sprint

    def planned_velocity(self) -> float:
        if not self._velocity_history:
            return 5.0
        return round(statistics.mean(self._velocity_history[-5:]), 1)

    def sprint_health(self, sprint_id: str) -> Dict[str, Any]:
        sprint = self._get_sprint(sprint_id)
        total_days = (sprint.end_date - sprint.start_date).days or 1
        elapsed = (datetime.utcnow() - sprint.start_date).days
        time_pct = min(elapsed / total_days * 100, 100)
        story_count = len(sprint.stories)
        return {
            "sprint_id": sprint_id,
            "name": sprint.name,
            "goal": sprint.goal,
            "time_elapsed_pct": round(time_pct, 1),
            "stories_planned": story_count,
            "capacity": sprint.capacity,
            "velocity": sprint.velocity,
        }

    def _get_sprint(self, sprint_id: str) -> Sprint:
        if sprint_id not in self.sprints:
            raise ValueError(f"sprint {sprint_id} not found")
        return self.sprints[sprint_id]


# ---------------------------------------------------------------------------
# Product Agent (Orchestrator)
# ---------------------------------------------------------------------------

class ProductAgent:
    """Orchestrates all product management sub-components."""

    def __init__(self, config: Optional[ProductConfig] = None) -> None:
        self.config = config or ProductConfig()
        self.strategy = ProductStrategyManager()
        self.roadmap = RoadmapPlanner()
        self.prioritizer = FeaturePrioritizer()
        self.stories = UserStoryManager()
        self.okr = OKRManager()
        self.analytics = ProductAnalytics(self.config)
        self.ab_test = ABTestManager(self.config)
        self.feedback = FeedbackProcessor()
        self.gtm = GTMManager()
        self.stakeholders = StakeholderManager()
        self.sprints = SprintManager()
        logger.info("ProductAgent initialized")

    def full_status(self) -> Dict[str, Any]:
        return {
            "vision": self.strategy.vision.statement if self.strategy.vision else None,
            "features": {
                horizon.value: len(ids)
                for horizon, ids in self.strategy.strategies.items()
            } if self.strategy.strategies else {},
            "roadmap_summary": self.roadmap.roadmap_summary(),
            "story_points": {
                "total": self.stories.story_points_total(),
                "done": self.stories.story_points_total(StoryStatus.DONE),
            },
            "okr_dashboard": self.okr.dashboard(),
            "feedback_sentiment": self.feedback.sentiment_summary(),
            "active_experiments": sum(
                1 for e in self.ab_test.experiments.values()
                if e.status == ExperimentStatus.RUNNING
            ),
        }

    def run(self) -> Dict[str, Any]:
        logger.info("ProductAgent run starting")
        status = self.full_status()
        logger.info("ProductAgent run complete")
        return status


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    agent = ProductAgent()
    result = agent.run()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
