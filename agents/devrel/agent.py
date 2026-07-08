"""
DevRel Agent - Developer relations, community building, documentation, API advocacy, developer experience, and content creation.

Provides comprehensive developer relations management including community analytics,
content strategy and creation, event management, documentation quality assessment,
developer experience measurement, feedback collection and analysis, SDK/API advocacy,
and developer journey mapping.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
import statistics
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
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

class Platform(Enum):
    """Developer community platforms."""
    DISCORD = "discord"
    SLACK = "slack"
    GITHUB = "github"
    STACK_OVERFLOW = "stackoverflow"
    DEV_TO = "dev_to"
    MEDIUM = "medium"
    TWITTER = "twitter"
    REDDIT = "reddit"
    YOUTUBE = "youtube"
    TWITCH = "twitch"
    HN = "hacker_news"
    FORUM = "forum"
    BLOG = "blog"
    DOCS = "docs"


class ContentType(Enum):
    """Types of developer content."""
    BLOG_POST = "blog_post"
    TUTORIAL = "tutorial"
    HOW_TO = "how_to"
    API_REFERENCE = "api_reference"
    QUICKSTART = "quickstart"
    VIDEO = "video"
    PODCAST = "podcast"
    WEBINAR = "webinar"
    CONFERENCE_TALK = "conference_talk"
    WORKSHOP = "workshop"
    CODE_SAMPLE = "code_sample"
    SAMPLE_APP = "sample_app"
    TEMPLATE = "template"
    CHEATSHEET = "cheatsheet"
    INTERVIEW = "interview"
    CASE_STUDY = "case_study"
    RELEASE_ANNOUNCEMENT = "release_announcement"
    THREAD = "thread"
    INFOGRAPHIC = "infographic"


class ContentStatus(Enum):
    """Status of content creation."""
    IDEA = "idea"
    OUTLINE = "outline"
    DRAFT = "draft"
    REVIEW = "review"
    EDITING = "editing"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    NEEDS_UPDATE = "needs_update"


class EventType(Enum):
    """Types of developer events."""
    MEETUP = "meetup"
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    HACKATHON = "hackathon"
    WEBINAR = "webinar"
    OFFICE_HOURS = "office_hours"
    AMA = "ama"
    LIVE_CODING = "live_coding"
    LAUNCH_EVENT = "launch_event"
    COMMUNITY_CALL = "community_call"


class EventStatus(Enum):
    """Status of an event."""
    PLANNING = "planning"
    PROMOTING = "promoting"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class FeedbackType(Enum):
    """Types of developer feedback."""
    FEATURE_REQUEST = "feature_request"
    BUG_REPORT = "bug_report"
    UX_FEEDBACK = "ux_feedback"
    DOCUMENTATION = "documentation"
    API_FEEDBACK = "api_feedback"
    SDK_FEEDBACK = "sdk_feedback"
    ONBOARDING = "onboarding"
    SUPPORT = "support"
    GENERAL = "general"
    SENTIMENT = "sentiment"


class Sentiment(Enum):
    """Sentiment analysis results."""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class JourneyStage(Enum):
    """Developer journey stages."""
    AWARENESS = "awareness"
    INTEREST = "interest"
    EVALUATION = "evaluation"
    ONBOARDING = "onboarding"
    FIRST_SUCCESS = "first_success"
    REGULAR_USAGE = "regular_usage"
    ADVOCACY = "advocacy"
    CONTRIBUTION = "contribution"
    CHURN_RISK = "churn_risk"


class MetricCategory(Enum):
    """Categories of developer relations metrics."""
    COMMUNITY_GROWTH = "community_growth"
    ENGAGEMENT = "engagement"
    CONTENT_PERFORMANCE = "content_performance"
    EVENT_IMPACT = "event_impact"
    DOCUMENTATION = "documentation"
    DEVELOPER_EXPERIENCE = "developer_experience"
    SUPPORT = "support"
    ADVOCACY = "advocacy"
    SENTIMENT = "sentiment"
    RETENTION = "retention"


class DocQuality(Enum):
    """Documentation quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ADEQUATE = "adequate"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CommunityMember:
    """A member of the developer community."""
    member_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    email: str = ""
    platform: Platform = Platform.DISCORD
    joined_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: Optional[datetime] = None
    posts_count: int = 0
    comments_count: int = 0
    reactions_count: int = 0
    helpful_answers: int = 0
    reputation_score: float = 0.0
    tags: List[str] = field(default_factory=list)
    journey_stage: JourneyStage = JourneyStage.AWARENESS
    nps_score: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "platform": self.platform.value,
            "joined_at": self.joined_at.isoformat(),
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "posts_count": self.posts_count,
            "comments_count": self.comments_count,
            "reactions_count": self.reactions_count,
            "helpful_answers": self.helpful_answers,
            "reputation_score": round(self.reputation_score, 2),
            "journey_stage": self.journey_stage.value,
            "nps_score": self.nps_score,
        }


@dataclass
class ContentItem:
    """A piece of developer content."""
    content_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    title: str = ""
    content_type: ContentType = ContentType.BLOG_POST
    status: ContentStatus = ContentStatus.IDEA
    author: str = ""
    platforms: List[Platform] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    url: Optional[str] = None
    word_count: int = 0
    reading_time_minutes: int = 0
    views: int = 0
    likes: int = 0
    shares: int = 0
    comments: int = 0
    bookmarks: int = 0
    ctr_percent: float = 0.0
    avg_time_on_page_seconds: float = 0.0
    bounce_rate_percent: float = 0.0
    conversions: int = 0
    sentiment_score: float = 0.0
    seo_score: float = 0.0
    quality_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_id": self.content_id,
            "title": self.title,
            "content_type": self.content_type.value,
            "status": self.status.value,
            "author": self.author,
            "platforms": [p.value for p in self.platforms],
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "url": self.url,
            "word_count": self.word_count,
            "reading_time_minutes": self.reading_time_minutes,
            "views": self.views,
            "likes": self.likes,
            "shares": self.shares,
            "comments": self.comments,
            "bookmarks": self.bookmarks,
            "ctr_percent": round(self.ctr_percent, 2),
            "avg_time_on_page_seconds": round(self.avg_time_on_page_seconds, 1),
            "bounce_rate_percent": round(self.bounce_rate_percent, 2),
            "conversions": self.conversions,
            "sentiment_score": round(self.sentiment_score, 2),
            "seo_score": round(self.seo_score, 2),
            "quality_score": round(self.quality_score, 2),
        }


@dataclass
class DeveloperEvent:
    """A developer relations event."""
    event_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    event_type: EventType = EventType.MEETUP
    status: EventStatus = EventStatus.PLANNING
    description: str = ""
    date: Optional[datetime] = None
    duration_minutes: int = 60
    location: str = ""
    is_virtual: bool = True
    max_attendees: int = 100
    registered_count: int = 0
    attended_count: int = 0
    speakers: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    satisfaction_score: float = 0.0
    nps_score: Optional[int] = None
    recordings_url: Optional[str] = None
    materials_url: Optional[str] = None
    feedback_count: int = 0
    follow_up_actions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "name": self.name,
            "event_type": self.event_type.value,
            "status": self.status.value,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "duration_minutes": self.duration_minutes,
            "location": self.location,
            "is_virtual": self.is_virtual,
            "max_attendees": self.max_attendees,
            "registered_count": self.registered_count,
            "attended_count": self.attended_count,
            "speakers": self.speakers,
            "topics": self.topics,
            "satisfaction_score": round(self.satisfaction_score, 2),
            "nps_score": self.nps_score,
            "feedback_count": self.feedback_count,
        }


@dataclass
class FeedbackItem:
    """A developer feedback entry."""
    feedback_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    feedback_type: FeedbackType = FeedbackType.GENERAL
    source: Platform = Platform.GITHUB
    author: str = ""
    message: str = ""
    sentiment: Sentiment = Sentiment.NEUTRAL
    sentiment_score: float = 0.0
    tags: List[str] = field(default_factory=list)
    priority: str = "medium"
    status: str = "open"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    response_time_hours: Optional[float] = None
    upvotes: int = 0
    related_content: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feedback_id": self.feedback_id,
            "feedback_type": self.feedback_type.value,
            "source": self.source.value,
            "author": self.author,
            "message": self.message[:500],
            "sentiment": self.sentiment.value,
            "sentiment_score": round(self.sentiment_score, 2),
            "tags": self.tags,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "response_time_hours": round(self.response_time_hours, 1) if self.response_time_hours else None,
            "upvotes": self.upvotes,
        }


@dataclass
class DocumentationPage:
    """A documentation page assessment."""
    page_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    title: str = ""
    url: str = ""
    section: str = ""
    last_updated: Optional[datetime] = None
    word_count: int = 0
    has_code_examples: bool = False
    has_api_reference: bool = False
    has_tutorial: bool = False
    has_troubleshooting: bool = False
    has_changelog: bool = False
    quality: DocQuality = DocQuality.ADEQUATE
    issues: List[str] = field(default_factory=list)
    page_views: int = 0
    avg_time_on_page: float = 0.0
    bounce_rate: float = 0.0
    search_terms: List[str] = field(default_factory=list)
    feedback_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_id": self.page_id,
            "title": self.title,
            "url": self.url,
            "section": self.section,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "word_count": self.word_count,
            "has_code_examples": self.has_code_examples,
            "has_api_reference": self.has_api_reference,
            "has_tutorial": self.has_tutorial,
            "has_troubleshooting": self.has_troubleshooting,
            "has_changelog": self.has_changelog,
            "quality": self.quality.value,
            "issues": self.issues,
            "page_views": self.page_views,
            "bounce_rate": round(self.bounce_rate, 2),
            "feedback_score": round(self.feedback_score, 2),
        }


@dataclass
class DXMetric:
    """Developer Experience metric."""
    metric_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    category: MetricCategory = MetricCategory.DEVELOPER_EXPERIENCE
    value: float = 0.0
    unit: str = ""
    target: Optional[float] = None
    trend: str = "stable"  # improving, stable, declining
    period: str = "monthly"
    measured_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    breakdown: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_id": self.metric_id,
            "name": self.name,
            "category": self.category.value,
            "value": round(self.value, 2),
            "unit": self.unit,
            "target": round(self.target, 2) if self.target else None,
            "trend": self.trend,
            "period": self.period,
            "measured_at": self.measured_at.isoformat(),
            "breakdown": {k: round(v, 2) for k, v in self.breakdown.items()},
        }


@dataclass
class DeveloperJourney:
    """A developer's journey through the product."""
    journey_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    developer_id: str = ""
    current_stage: JourneyStage = JourneyStage.AWARENESS
    stages_completed: List[JourneyStage] = field(default_factory=list)
    time_in_stage_days: Dict[str, float] = field(default_factory=dict)
    first_contact: Optional[datetime] = None
    first_success: Optional[datetime] = None
    last_active: Optional[datetime] = None
    total_contributions: int = 0
    support_tickets: int = 0
    nps_score: Optional[int] = None
    churn_risk: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "journey_id": self.journey_id,
            "developer_id": self.developer_id,
            "current_stage": self.current_stage.value,
            "stages_completed": [s.value for s in self.stages_completed],
            "time_in_stage_days": {k: round(v, 1) for k, v in self.time_in_stage_days.items()},
            "first_contact": self.first_contact.isoformat() if self.first_contact else None,
            "first_success": self.first_success.isoformat() if self.first_success else None,
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "total_contributions": self.total_contributions,
            "nps_score": self.nps_score,
            "churn_risk": round(self.churn_risk, 2),
        }


@dataclass
class CommunityMetrics:
    """Aggregated community metrics."""
    period: str = "monthly"
    total_members: int = 0
    new_members: int = 0
    active_members: int = 0
    retention_rate: float = 0.0
    posts_count: int = 0
    comments_count: int = 0
    questions_answered: int = 0
    avg_response_time_hours: float = 0.0
    satisfaction_score: float = 0.0
    nps_score: float = 0.0
    top_contributors: List[Dict[str, Any]] = field(default_factory=list)
    platform_breakdown: Dict[str, int] = field(default_factory=dict)
    sentiment_distribution: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "period": self.period,
            "total_members": self.total_members,
            "new_members": self.new_members,
            "active_members": self.active_members,
            "retention_rate": round(self.retention_rate, 2),
            "posts_count": self.posts_count,
            "comments_count": self.comments_count,
            "questions_answered": self.questions_answered,
            "avg_response_time_hours": round(self.avg_response_time_hours, 1),
            "satisfaction_score": round(self.satisfaction_score, 2),
            "nps_score": round(self.nps_score, 1),
            "top_contributors": self.top_contributors[:10],
            "platform_breakdown": self.platform_breakdown,
            "sentiment_distribution": self.sentiment_distribution,
        }


@dataclass
class DevRelReport:
    """Comprehensive DevRel performance report."""
    report_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    period: str = "monthly"
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    community_metrics: Optional[CommunityMetrics] = None
    content_summary: Dict[str, Any] = field(default_factory=dict)
    event_summary: Dict[str, Any] = field(default_factory=dict)
    feedback_summary: Dict[str, Any] = field(default_factory=dict)
    documentation_summary: Dict[str, Any] = field(default_factory=dict)
    dx_metrics: List[DXMetric] = field(default_factory=list)
    highlights: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "period": self.period,
            "generated_at": self.generated_at.isoformat(),
            "community_metrics": self.community_metrics.to_dict() if self.community_metrics else None,
            "content_summary": self.content_summary,
            "event_summary": self.event_summary,
            "feedback_summary": self.feedback_summary,
            "documentation_summary": self.documentation_summary,
            "dx_metrics": [m.to_dict() for m in self.dx_metrics],
            "highlights": self.highlights,
            "concerns": self.concerns,
            "recommendations": self.recommendations,
        }


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class DevRelConfig:
    """Configuration for the DevRel Agent."""
    # Community
    min_response_time_hours: float = 4.0
    target_retention_rate: float = 0.70
    target_nps: float = 50.0
    inactive_days_threshold: int = 30
    top_contributor_min_posts: int = 10

    # Content
    target_posts_per_week: int = 3
    target_reading_time_minutes: int = 8
    min_word_count: int = 500
    quality_score_threshold: float = 0.7
    seo_optimization_enabled: bool = True

    # Events
    target_satisfaction_score: float = 4.0
    target_attendance_rate: float = 0.70
    max_event_size: int = 500
    follow_up_window_days: int = 7

    # Feedback
    response_sla_hours: float = 24.0
    sentiment_analysis_enabled: bool = True
    auto_categorize: bool = True
    priority_keywords: Dict[str, str] = field(default_factory=lambda: {
        "critical": "high",
        "urgent": "high",
        "broken": "high",
        "security": "critical",
        "crash": "critical",
        "feature request": "medium",
        "suggestion": "low",
        "typo": "low",
    })

    # Documentation
    freshness_days: int = 90
    min_code_examples: int = 1
    target_doc_quality: DocQuality = DocQuality.GOOD
    require_troubleshooting: bool = True

    # DX Metrics
    target_time_to_first_hello_world: float = 5.0  # minutes
    target_api_adoption_rate: float = 0.30
    target_community_growth_rate: float = 0.10  # monthly

    # Sentiment
    positive_keywords: List[str] = field(default_factory=lambda: [
        "great", "awesome", "love", "excellent", "helpful", "easy",
        "fast", "clean", "intuitive", "powerful", "well-documented",
        "amazing", "perfect", "brilliant", "fantastic", "smooth",
    ])
    negative_keywords: List[str] = field(default_factory=lambda: [
        "broken", "terrible", "hate", "confusing", "slow", "buggy",
        "frustrating", "difficult", "outdated", "missing", "broken",
        "terrible", "awful", "disappointing", "useless", "nightmare",
    ])


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _analyze_sentiment(text: str, config: DevRelConfig) -> Tuple[Sentiment, float]:
    """Analyze sentiment of text using keyword matching."""
    text_lower = text.lower()
    pos_count = sum(1 for kw in config.positive_keywords if kw in text_lower)
    neg_count = sum(1 for kw in config.negative_keywords if kw in text_lower)
    total = pos_count + neg_count
    if total == 0:
        return Sentiment.NEUTRAL, 0.0
    score = (pos_count - neg_count) / total
    if score > 0.5:
        return Sentiment.VERY_POSITIVE, score
    elif score > 0.1:
        return Sentiment.POSITIVE, score
    elif score < -0.5:
        return Sentiment.VERY_NEGATIVE, score
    elif score < -0.1:
        return Sentiment.NEGATIVE, score
    return Sentiment.NEUTRAL, score


def _categorize_feedback(text: str, config: DevRelConfig) -> FeedbackType:
    """Auto-categorize feedback based on content."""
    text_lower = text.lower()
    if any(kw in text_lower for kw in ["feature", "add", "support for", "would be nice", "request"]):
        return FeedbackType.FEATURE_REQUEST
    if any(kw in text_lower for kw in ["bug", "error", "crash", "broken", "doesn't work"]):
        return FeedbackType.BUG_REPORT
    if any(kw in text_lower for kw in ["doc", "documentation", "example", "tutorial", "guide"]):
        return FeedbackType.DOCUMENTATION
    if any(kw in text_lower for kw in ["api", "endpoint", "sdk", "library", "method"]):
        return FeedbackType.API_FEEDBACK
    if any(kw in text_lower for kw in ["setup", "install", "getting started", "onboarding", "hello world"]):
        return FeedbackType.ONBOARDING
    if any(kw in text_lower for kw in ["ux", "ui", "interface", "design", "layout"]):
        return FeedbackType.UX_FEEDBACK
    return FeedbackType.GENERAL


def _assess_doc_quality(page: DocumentationPage, config: DevRelConfig) -> DocQuality:
    """Assess documentation page quality based on multiple factors."""
    score = 0
    issues = []

    if page.word_count < config.min_word_count:
        issues.append(f"Content too short ({page.word_count} words, minimum {config.min_word_count})")
    else:
        score += 20

    if page.has_code_examples:
        score += 20
    else:
        issues.append("No code examples")

    if page.has_api_reference:
        score += 15
    else:
        issues.append("No API reference section")

    if page.has_tutorial:
        score += 15
    else:
        issues.append("No tutorial walkthrough")

    if page.has_troubleshooting:
        score += 10
    else:
        issues.append("No troubleshooting section")

    if page.has_changelog:
        score += 5
    else:
        issues.append("No changelog")

    if page.last_updated:
        age_days = (datetime.now(timezone.utc) - page.last_updated).days
        if age_days > config.freshness_days:
            issues.append(f"Content is {age_days} days old (threshold: {config.freshness_days})")
            score -= 10
        else:
            score += 10

    if page.page_views > 0:
        if page.bounce_rate > 70:
            issues.append(f"High bounce rate: {page.bounce_rate:.0f}%")
            score -= 5
        elif page.bounce_rate < 40:
            score += 5

    score = max(0, min(100, score))

    if score >= 80:
        quality = DocQuality.EXCELLENT
    elif score >= 65:
        quality = DocQuality.GOOD
    elif score >= 50:
        quality = DocQuality.ADEQUATE
    elif score >= 30:
        quality = DocQuality.NEEDS_IMPROVEMENT
    else:
        quality = DocQuality.POOR

    page.quality = quality
    page.issues = issues
    return quality


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------

class DevRelAgent:
    """
    Enterprise-grade Developer Relations Agent providing community management,
    content strategy, event management, documentation assessment, developer
    experience measurement, feedback analysis, and comprehensive reporting.
    """

    def __init__(self, config: Optional[DevRelConfig] = None):
        self._config = config or DevRelConfig()
        self._members: Dict[str, CommunityMember] = {}
        self._content: Dict[str, ContentItem] = {}
        self._events: Dict[str, DeveloperEvent] = {}
        self._feedback: List[FeedbackItem] = []
        self._documentation: Dict[str, DocumentationPage] = {}
        self._dx_metrics: List[DXMetric] = []
        self._journeys: Dict[str, DeveloperJourney] = {}
        logger.info("DevRelAgent initialized")

    # -----------------------------------------------------------------------
    # Community Management
    # -----------------------------------------------------------------------

    def add_member(
        self,
        name: str,
        platform: Platform = Platform.DISCORD,
        email: str = "",
        **kwargs: Any,
    ) -> CommunityMember:
        """Add a developer community member."""
        member = CommunityMember(
            name=name,
            email=email,
            platform=platform,
            tags=kwargs.get("tags", []),
            journey_stage=kwargs.get("journey_stage", JourneyStage.AWARENESS),
        )
        self._members[member.member_id] = member
        logger.info("Added community member '%s' on %s", name, platform.value)
        return member

    def get_member(self, member_id: str) -> CommunityMember:
        """Get a community member by ID."""
        if member_id not in self._members:
            raise KeyError(f"Member '{member_id}' not found")
        return self._members[member_id]

    def list_members(
        self,
        platform: Optional[Platform] = None,
        stage: Optional[JourneyStage] = None,
        limit: int = 50,
    ) -> List[CommunityMember]:
        """List community members with optional filters."""
        members = list(self._members.values())
        if platform:
            members = [m for m in members if m.platform == platform]
        if stage:
            members = [m for m in members if m.journey_stage == stage]
        return members[:limit]

    def compute_community_metrics(self, period: str = "monthly") -> CommunityMetrics:
        """Compute aggregated community metrics."""
        members = list(self._members.values())
        now = datetime.now(timezone.utc)
        if period == "monthly":
            cutoff = now - timedelta(days=30)
        elif period == "weekly":
            cutoff = now - timedelta(days=7)
        else:
            cutoff = now - timedelta(days=365)

        new_members = sum(1 for m in members if m.joined_at >= cutoff)
        active = [m for m in members if m.last_active and m.last_active >= cutoff]
        retention = len(active) / len(members) if members else 0.0

        platform_counts = Counter(m.platform.value for m in members)
        top_contributors = sorted(
            members, key=lambda m: m.posts_count + m.comments_count, reverse=True
        )[:10]

        nps_scores = [m.nps_score for m in members if m.nps_score is not None]
        avg_nps = statistics.mean(nps_scores) if nps_scores else 0.0

        total_posts = sum(m.posts_count for m in members)
        total_comments = sum(m.comments_count for m in members)

        return CommunityMetrics(
            period=period,
            total_members=len(members),
            new_members=new_members,
            active_members=len(active),
            retention_rate=retention,
            posts_count=total_posts,
            comments_count=total_comments,
            nps_score=avg_nps,
            top_contributors=[
                {"name": m.name, "score": m.posts_count + m.comments_count}
                for m in top_contributors
            ],
            platform_breakdown=dict(platform_counts),
        )

    # -----------------------------------------------------------------------
    # Content Management
    # -----------------------------------------------------------------------

    def create_content(
        self,
        title: str,
        content_type: ContentType = ContentType.BLOG_POST,
        author: str = "",
        platforms: Optional[List[Platform]] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ContentItem:
        """Create a new content item."""
        item = ContentItem(
            title=title,
            content_type=content_type,
            author=author,
            platforms=platforms or [],
            tags=tags or [],
            word_count=kwargs.get("word_count", 0),
            url=kwargs.get("url"),
        )
        item.reading_time_minutes = max(1, item.word_count // 250) if item.word_count else 0
        self._content[item.content_id] = item
        logger.info("Created content '%s' (%s)", title, content_type.value)
        return item

    def get_content(self, content_id: str) -> ContentItem:
        """Get a content item by ID."""
        if content_id not in self._content:
            raise KeyError(f"Content '{content_id}' not found")
        return self._content[content_id]

    def update_content_status(self, content_id: str, status: ContentStatus) -> ContentItem:
        """Update content status."""
        item = self.get_content(content_id)
        item.status = status
        if status == ContentStatus.PUBLISHED:
            item.published_at = datetime.now(timezone.utc)
        return item

    def record_content_engagement(
        self,
        content_id: str,
        views: int = 0,
        likes: int = 0,
        shares: int = 0,
        comments: int = 0,
        bookmarks: int = 0,
    ) -> ContentItem:
        """Record engagement metrics for content."""
        item = self.get_content(content_id)
        item.views += views
        item.likes += likes
        item.shares += shares
        item.comments += comments
        item.bookmarks += bookmarks
        return item

    def list_content(
        self,
        content_type: Optional[ContentType] = None,
        status: Optional[ContentStatus] = None,
        platform: Optional[Platform] = None,
        limit: int = 50,
    ) -> List[ContentItem]:
        """List content items with filters."""
        items = list(self._content.values())
        if content_type:
            items = [i for i in items if i.content_type == content_type]
        if status:
            items = [i for i in items if i.status == status]
        if platform:
            items = [i for i in items if platform in i.platforms]
        return items[:limit]

    def compute_content_analytics(self) -> Dict[str, Any]:
        """Compute content performance analytics."""
        items = list(self._content.values())
        published = [i for i in items if i.status == ContentStatus.PUBLISHED]
        if not published:
            return {"message": "No published content"}

        total_views = sum(i.views for i in published)
        total_likes = sum(i.likes for i in published)
        total_shares = sum(i.shares for i in published)
        total_comments = sum(i.comments for i in published)

        by_type = defaultdict(list)
        for i in published:
            by_type[i.content_type.value].append(i)

        type_performance = {}
        for ctype, type_items in by_type.items():
            type_performance[ctype] = {
                "count": len(type_items),
                "total_views": sum(i.views for i in type_items),
                "avg_views": statistics.mean([i.views for i in type_items]),
                "total_engagement": sum(i.likes + i.shares + i.comments for i in type_items),
            }

        return {
            "total_content": len(items),
            "published": len(published),
            "total_views": total_views,
            "total_likes": total_likes,
            "total_shares": total_shares,
            "total_comments": total_comments,
            "avg_views_per_post": total_views / len(published) if published else 0,
            "engagement_rate": (total_likes + total_shares + total_comments) / total_views if total_views > 0 else 0,
            "by_type": type_performance,
            "top_performers": sorted(published, key=lambda i: i.views, reverse=True)[:5],
        }

    # -----------------------------------------------------------------------
    # Event Management
    # -----------------------------------------------------------------------

    def create_event(
        self,
        name: str,
        event_type: EventType = EventType.MEETUP,
        date: Optional[datetime] = None,
        is_virtual: bool = True,
        **kwargs: Any,
    ) -> DeveloperEvent:
        """Create a developer event."""
        event = DeveloperEvent(
            name=name,
            event_type=event_type,
            date=date,
            is_virtual=is_virtual,
            description=kwargs.get("description", ""),
            duration_minutes=kwargs.get("duration_minutes", 60),
            location=kwargs.get("location", ""),
            max_attendees=kwargs.get("max_attendees", 100),
            speakers=kwargs.get("speakers", []),
            topics=kwargs.get("topics", []),
        )
        self._events[event.event_id] = event
        logger.info("Created event '%s' (%s)", name, event_type.value)
        return event

    def get_event(self, event_id: str) -> DeveloperEvent:
        """Get an event by ID."""
        if event_id not in self._events:
            raise KeyError(f"Event '{event_id}' not found")
        return self._events[event_id]

    def update_event_status(self, event_id: str, status: EventStatus) -> DeveloperEvent:
        """Update event status."""
        event = self.get_event(event_id)
        event.status = status
        return event

    def record_event_feedback(
        self,
        event_id: str,
        attended_count: int,
        satisfaction_score: float,
        nps_score: Optional[int] = None,
    ) -> DeveloperEvent:
        """Record post-event feedback."""
        event = self.get_event(event_id)
        event.attended_count = attended_count
        event.satisfaction_score = satisfaction_score
        event.nps_score = nps_score
        event.feedback_count += 1
        return event

    def list_events(
        self,
        event_type: Optional[EventType] = None,
        status: Optional[EventStatus] = None,
        limit: int = 20,
    ) -> List[DeveloperEvent]:
        """List events with filters."""
        events = list(self._events.values())
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if status:
            events = [e for e in events if e.status == status]
        return events[:limit]

    def compute_event_analytics(self) -> Dict[str, Any]:
        """Compute event performance analytics."""
        events = list(self._events.values())
        completed = [e for e in events if e.status == EventStatus.COMPLETED]
        if not completed:
            return {"message": "No completed events"}

        total_registered = sum(e.registered_count for e in completed)
        total_attended = sum(e.attended_count for e in completed)
        attendance_rate = total_attended / total_registered if total_registered > 0 else 0.0
        avg_satisfaction = statistics.mean([e.satisfaction_score for e in completed if e.satisfaction_score > 0])
        nps_scores = [e.nps_score for e in completed if e.nps_score is not None]
        avg_nps = statistics.mean(nps_scores) if nps_scores else 0.0

        by_type = defaultdict(list)
        for e in completed:
            by_type[e.event_type.value].append(e)

        return {
            "total_events": len(events),
            "completed": len(completed),
            "total_registered": total_registered,
            "total_attended": total_attended,
            "attendance_rate": round(attendance_rate, 2),
            "avg_satisfaction": round(avg_satisfaction, 2),
            "avg_nps": round(avg_nps, 1),
            "by_type": {
                k: {"count": len(v), "avg_satisfaction": statistics.mean([e.satisfaction_score for e in v if e.satisfaction_score > 0])}
                for k, v in by_type.items()
            },
        }

    # -----------------------------------------------------------------------
    # Feedback Management
    # -----------------------------------------------------------------------

    def add_feedback(
        self,
        message: str,
        source: Platform = Platform.GITHUB,
        author: str = "",
        feedback_type: Optional[FeedbackType] = None,
        **kwargs: Any,
    ) -> FeedbackItem:
        """Add developer feedback."""
        if feedback_type is None and self._config.auto_categorize:
            feedback_type = _categorize_feedback(message, self._config)
        else:
            feedback_type = feedback_type or FeedbackType.GENERAL

        sentiment, sentiment_score = _analyze_sentiment(message, self._config)
        priority = "medium"
        for kw, prio in self._config.priority_keywords.items():
            if kw in message.lower():
                priority = prio
                break

        item = FeedbackItem(
            feedback_type=feedback_type,
            source=source,
            author=author,
            message=message,
            sentiment=sentiment,
            sentiment_score=sentiment_score,
            tags=kwargs.get("tags", []),
            priority=priority,
        )
        self._feedback.append(item)
        logger.info("Feedback added: [%s] %s (sentiment=%s)", feedback_type.value, message[:50], sentiment.value)
        return item

    def list_feedback(
        self,
        feedback_type: Optional[FeedbackType] = None,
        sentiment: Optional[Sentiment] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[FeedbackItem]:
        """List feedback items with filters."""
        items = self._feedback
        if feedback_type:
            items = [f for f in items if f.feedback_type == feedback_type]
        if sentiment:
            items = [f for f in items if f.sentiment == sentiment]
        if priority:
            items = [f for f in items if f.priority == priority]
        if status:
            items = [f for f in items if f.status == status]
        return items[:limit]

    def resolve_feedback(self, feedback_id: str) -> FeedbackItem:
        """Mark feedback as resolved."""
        for item in self._feedback:
            if item.feedback_id == feedback_id:
                item.status = "resolved"
                item.resolved_at = datetime.now(timezone.utc)
                if item.created_at:
                    delta = item.resolved_at - item.created_at
                    item.response_time_hours = delta.total_seconds() / 3600
                return item
        raise KeyError(f"Feedback '{feedback_id}' not found")

    def compute_feedback_analytics(self) -> Dict[str, Any]:
        """Compute feedback analytics."""
        items = self._feedback
        if not items:
            return {"message": "No feedback collected"}

        by_type = Counter(f.feedback_type.value for f in items)
        by_sentiment = Counter(f.sentiment.value for f in items)
        by_source = Counter(f.source.value for f in items)
        by_priority = Counter(f.priority for f in items)
        by_status = Counter(f.status for f in items)

        resolved = [f for f in items if f.status == "resolved"]
        response_times = [f.response_time_hours for f in resolved if f.response_time_hours is not None]
        avg_response_time = statistics.mean(response_times) if response_times else None

        return {
            "total_feedback": len(items),
            "by_type": dict(by_type),
            "by_sentiment": dict(by_sentiment),
            "by_source": dict(by_source),
            "by_priority": dict(by_priority),
            "by_status": dict(by_status),
            "resolution_rate": len(resolved) / len(items) if items else 0,
            "avg_response_time_hours": round(avg_response_time, 1) if avg_response_time else None,
            "positive_ratio": (by_sentiment.get("very_positive", 0) + by_sentiment.get("positive", 0)) / len(items),
        }

    # -----------------------------------------------------------------------
    # Documentation Assessment
    # -----------------------------------------------------------------------

    def add_documentation_page(
        self,
        title: str,
        url: str = "",
        section: str = "",
        **kwargs: Any,
    ) -> DocumentationPage:
        """Add a documentation page for assessment."""
        page = DocumentationPage(
            title=title,
            url=url,
            section=section,
            word_count=kwargs.get("word_count", 0),
            has_code_examples=kwargs.get("has_code_examples", False),
            has_api_reference=kwargs.get("has_api_reference", False),
            has_tutorial=kwargs.get("has_tutorial", False),
            has_troubleshooting=kwargs.get("has_troubleshooting", False),
            has_changelog=kwargs.get("has_changelog", False),
            last_updated=kwargs.get("last_updated"),
            page_views=kwargs.get("page_views", 0),
            bounce_rate=kwargs.get("bounce_rate", 0.0),
        )
        _assess_doc_quality(page, self._config)
        self._documentation[page.page_id] = page
        logger.info("Documentation page '%s' assessed: %s", title, page.quality.value)
        return page

    def assess_documentation(self) -> Dict[str, Any]:
        """Assess all documentation pages and compute summary."""
        pages = list(self._documentation.values())
        if not pages:
            return {"message": "No documentation pages"}

        quality_dist = Counter(p.quality.value for p in pages)
        issues_count = sum(len(p.issues) for p in pages)
        pages_with_examples = sum(1 for p in pages if p.has_code_examples)
        pages_with_troubleshooting = sum(1 for p in pages if p.has_troubleshooting)

        return {
            "total_pages": len(pages),
            "quality_distribution": dict(quality_dist),
            "pages_with_code_examples": pages_with_examples,
            "pages_with_troubleshooting": pages_with_troubleshooting,
            "total_issues": issues_count,
            "avg_issues_per_page": issues_count / len(pages) if pages else 0,
            "pages_needing_update": sum(1 for p in pages if p.quality in (DocQuality.NEEDS_IMPROVEMENT, DocQuality.POOR)),
            "worst_pages": sorted(pages, key=lambda p: list(DocQuality).index(p.quality), reverse=True)[:5],
        }

    # -----------------------------------------------------------------------
    # Developer Experience Metrics
    # -----------------------------------------------------------------------

    def record_dx_metric(
        self,
        name: str,
        value: float,
        unit: str = "",
        category: MetricCategory = MetricCategory.DEVELOPER_EXPERIENCE,
        target: Optional[float] = None,
        **kwargs: Any,
    ) -> DXMetric:
        """Record a developer experience metric."""
        metric = DXMetric(
            name=name,
            value=value,
            unit=unit,
            category=category,
            target=target,
            trend=kwargs.get("trend", "stable"),
            period=kwargs.get("period", "monthly"),
            breakdown=kwargs.get("breakdown", {}),
        )
        self._dx_metrics.append(metric)
        return metric

    def compute_dx_score(self) -> Dict[str, Any]:
        """Compute an overall developer experience score."""
        if not self._dx_metrics:
            return {"score": 0, "message": "No DX metrics recorded"}

        scores: List[float] = []
        for metric in self._dx_metrics:
            if metric.target and metric.target > 0:
                if metric.name in ["time_to_first_hello_world", "avg_response_time_hours"]:
                    # Lower is better
                    ratio = metric.target / max(metric.value, 0.01)
                    scores.append(min(1.0, ratio))
                else:
                    # Higher is better
                    ratio = metric.value / metric.target
                    scores.append(min(1.0, ratio))
            else:
                scores.append(0.5)

        overall = statistics.mean(scores) if scores else 0.0

        return {
            "overall_score": round(overall, 2),
            "metrics_count": len(self._dx_metrics),
            "on_target": sum(1 for m in self._dx_metrics if m.target and (
                (m.name in ["time_to_first_hello_world"] and m.value <= m.target) or
                (m.name not in ["time_to_first_hello_world"] and m.value >= m.target)
            )),
            "metrics": [m.to_dict() for m in self._dx_metrics],
        }

    # -----------------------------------------------------------------------
    # Developer Journey
    # -----------------------------------------------------------------------

    def track_journey(
        self,
        developer_id: str,
        stage: JourneyStage,
        **kwargs: Any,
    ) -> DeveloperJourney:
        """Track a developer's journey progression."""
        if developer_id not in self._journeys:
            self._journeys[developer_id] = DeveloperJourney(
                developer_id=developer_id,
                first_contact=datetime.now(timezone.utc),
            )

        journey = self._journeys[developer_id]
        if journey.current_stage != stage:
            if journey.current_stage not in journey.stages_completed:
                journey.stages_completed.append(journey.current_stage)
            journey.current_stage = stage
            if stage == JourneyStage.FIRST_SUCCESS:
                journey.first_success = datetime.now(timezone.utc)
            journey.last_active = datetime.now(timezone.utc)

        return journey

    def get_journey(self, developer_id: str) -> Optional[DeveloperJourney]:
        """Get a developer's journey."""
        return self._journeys.get(developer_id)

    def compute_journey_analytics(self) -> Dict[str, Any]:
        """Compute journey analytics across all developers."""
        journeys = list(self._journeys.values())
        if not journeys:
            return {"message": "No journey data"}

        stage_dist = Counter(j.current_stage.value for j in journeys)
        churn_risks = [j for j in journeys if j.churn_risk > 0.5]

        first_success_times = []
        for j in journeys:
            if j.first_contact and j.first_success:
                delta = j.first_success - j.first_contact
                first_success_times.append(delta.total_seconds() / 3600)

        return {
            "total_developers": len(journeys),
            "stage_distribution": dict(stage_dist),
            "churn_risk_count": len(churn_risks),
            "avg_time_to_first_success_hours": round(statistics.mean(first_success_times), 1) if first_success_times else None,
            "at_advocacy": sum(1 for j in journeys if j.current_stage == JourneyStage.ADVOCACY),
            "at_contribution": sum(1 for j in journeys if j.current_stage == JourneyStage.CONTRIBUTION),
        }

    # -----------------------------------------------------------------------
    # Comprehensive Reporting
    # -----------------------------------------------------------------------

    def generate_report(self, period: str = "monthly") -> DevRelReport:
        """Generate a comprehensive DevRel performance report."""
        report = DevRelReport(period=period)

        # Community
        report.community_metrics = self.compute_community_metrics(period)

        # Content
        content_data = self.compute_content_analytics()
        report.content_summary = {
            "total_content": content_data.get("total_content", 0),
            "published": content_data.get("published", 0),
            "total_views": content_data.get("total_views", 0),
            "engagement_rate": content_data.get("engagement_rate", 0),
        }

        # Events
        event_data = self.compute_event_analytics()
        report.event_summary = {
            "total_events": event_data.get("total_events", 0),
            "completed": event_data.get("completed", 0),
            "attendance_rate": event_data.get("attendance_rate", 0),
            "avg_satisfaction": event_data.get("avg_satisfaction", 0),
        }

        # Feedback
        feedback_data = self.compute_feedback_analytics()
        report.feedback_summary = {
            "total_feedback": feedback_data.get("total_feedback", 0),
            "resolution_rate": feedback_data.get("resolution_rate", 0),
            "positive_ratio": feedback_data.get("positive_ratio", 0),
        }

        # Documentation
        report.documentation_summary = self.assess_documentation()

        # DX Metrics
        dx = self.compute_dx_score()
        report.dx_metrics = self._dx_metrics[-20:]
        report.dx_metrics_summary = dx

        # Generate highlights and concerns
        if report.community_metrics and report.community_metrics.new_members > 0:
            report.highlights.append(f"Grew community by {report.community_metrics.new_members} new members")
        if content_data.get("total_views", 0) > 0:
            report.highlights.append(f"Content reached {content_data['total_views']} total views")
        if feedback_data.get("positive_ratio", 0) > 0.7:
            report.highlights.append(f"Positive sentiment at {feedback_data['positive_ratio']:.0%}")

        if report.community_metrics and report.community_metrics.retention_rate < self._config.target_retention_rate:
            report.concerns.append(f"Retention rate ({report.community_metrics.retention_rate:.0%}) below target ({self._config.target_retention_rate:.0%})")
        if feedback_data.get("resolution_rate", 1) < 0.8:
            report.concerns.append(f"Feedback resolution rate ({feedback_data.get('resolution_rate', 0):.0%}) below 80%")

        report.recommendations = self._generate_recommendations(report)
        return report

    def _generate_recommendations(self, report: DevRelReport) -> List[str]:
        """Generate recommendations based on report data."""
        recs = []
        if report.community_metrics:
            if report.community_metrics.active_members < report.community_metrics.total_members * 0.3:
                recs.append("Low active member ratio — consider re-engagement campaigns")
            if report.community_metrics.avg_response_time_hours > self._config.min_response_time_hours:
                recs.append(f"Response time ({report.community_metrics.avg_response_time_hours:.1f}h) exceeds SLA — add more moderators")
        if report.feedback_summary.get("positive_ratio", 0) < 0.5:
            recs.append("Negative sentiment trending — investigate top complaints")
        if report.documentation_summary.get("pages_needing_update", 0) > 0:
            recs.append(f"{report.documentation_summary['pages_needing_update']} doc pages need updating")
        if not recs:
            recs.append("All metrics within targets — continue current strategy")
        return recs

    # -----------------------------------------------------------------------
    # Status
    # -----------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": "DevRelAgent",
            "community_members": len(self._members),
            "content_items": len(self._content),
            "events": len(self._events),
            "feedback_items": len(self._feedback),
            "documentation_pages": len(self._documentation),
            "dx_metrics": len(self._dx_metrics),
            "journeys_tracked": len(self._journeys),
        }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the DevRel Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("=" * 60)
    print("DevRel Agent - Comprehensive Demo")
    print("=" * 60)

    agent = DevRelAgent()

    # Community
    print("\n--- Community Management ---")
    m1 = agent.add_member("Alice", Platform.DISCORD, tags=["python", "api"])
    m2 = agent.add_member("Bob", Platform.GITHUB, tags=["go", "cli"])
    m3 = agent.add_member("Charlie", Platform.SLACK, tags=["rust", "wasm"])
    agent.track_journey(m1.member_id, JourneyStage.REGULAR_USAGE)
    agent.track_journey(m2.member_id, JourneyStage.ADVOCACY)
    metrics = agent.compute_community_metrics()
    print(f"Members: {metrics.total_members}, Active: {metrics.active_members}")

    # Content
    print("\n--- Content Management ---")
    c1 = agent.create_content("Getting Started with Our API", ContentType.QUICKSTART,
                              author="Alice", word_count=1500,
                              platforms=[Platform.BLOG, Platform.DEV_TO])
    c2 = agent.create_content("Advanced API Patterns", ContentType.TUTORIAL,
                              author="Bob", word_count=2500,
                              platforms=[Platform.BLOG])
    agent.record_content_engagement(c1.content_id, views=5000, likes=200, shares=50)
    agent.record_content_engagement(c2.content_id, views=3000, likes=150, shares=30)
    agent.update_content_status(c1.content_id, ContentStatus.PUBLISHED)
    agent.update_content_status(c2.content_id, ContentStatus.PUBLISHED)
    content_analytics = agent.compute_content_analytics()
    print(f"Content: {content_analytics['published']} published, {content_analytics['total_views']} views")

    # Events
    print("\n--- Event Management ---")
    e1 = agent.create_event("API Workshop", EventType.WORKSHOP,
                            speakers=["Alice"], topics=["API", "REST"])
    agent.update_event_status(e1.event_id, EventStatus.COMPLETED)
    agent.record_event_feedback(e1.event_id, attended_count=45, satisfaction_score=4.5, nps_score=70)
    event_analytics = agent.compute_event_analytics()
    print(f"Events: {event_analytics['completed']} completed, satisfaction: {event_analytics['avg_satisfaction']}")

    # Feedback
    print("\n--- Feedback Management ---")
    f1 = agent.add_feedback("Love the new API docs! Very helpful.", author="Alice")
    f2 = agent.add_feedback("The SDK is broken, crashes on import", author="Bob")
    f3 = agent.add_feedback("Feature request: support for GraphQL", author="Charlie")
    feedback_analytics = agent.compute_feedback_analytics()
    print(f"Feedback: {feedback_analytics['total_feedback']} items, positive: {feedback_analytics['positive_ratio']:.0%}")

    # Documentation
    print("\n--- Documentation Assessment ---")
    d1 = agent.add_documentation_page("Quickstart Guide", section="getting-started",
                                       word_count=1200, has_code_examples=True,
                                       has_tutorial=True, has_troubleshooting=True)
    d2 = agent.add_documentation_page("API Reference", section="api",
                                       word_count=3000, has_code_examples=True,
                                       has_api_reference=True)
    doc_assessment = agent.assess_documentation()
    print(f"Docs: {doc_assessment['total_pages']} pages, quality: {doc_assessment['quality_distribution']}")

    # DX Metrics
    print("\n--- DX Metrics ---")
    agent.record_dx_metric("time_to_first_hello_world", 4.5, "minutes", target=5.0)
    agent.record_dx_metric("api_adoption_rate", 0.28, "ratio", target=0.30)
    agent.record_dx_metric("community_growth_rate", 0.12, "ratio", target=0.10)
    dx_score = agent.compute_dx_score()
    print(f"DX Score: {dx_score['overall_score']}, on target: {dx_score['on_target']}/{dx_score['metrics_count']}")

    # Report
    print("\n--- Comprehensive Report ---")
    report = agent.generate_report()
    print(f"Report: {report.report_id}")
    print(f"Highlights: {report.highlights}")
    print(f"Concerns: {report.concerns}")
    print(f"Recommendations: {report.recommendations}")

    # Status
    print(f"\nAgent Status: {json.dumps(agent.get_status(), indent=2)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
