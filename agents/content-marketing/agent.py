"""Content Marketing Agent - Content Strategy, Editorial Calendars, SEO, Distribution, Analytics.

A comprehensive content marketing management system that handles the full content lifecycle
from strategy development through performance analysis, including editorial calendar planning,
SEO content optimization, multi-channel distribution, and detailed content analytics.

This agent is designed for marketing teams, content strategists, and digital marketing
professionals who need a structured, data-driven approach to content marketing.

Architecture: Pipeline-based content operations with strategy → calendar → creation →
optimization → distribution → analytics stages. Each stage produces validated artifacts
that feed downstream stages.

Author: Awesome Grok Skills Team
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    Generator,
    Iterator,
    List,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

# ---------------------------------------------------------------------------
# Module-level setup
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

__all__ = [
    "ContentMarketingAgent",
    "ContentStrategy",
    "EditorialCalendar",
    "SEOOptimizer",
    "DistributionManager",
    "ContentAnalytics",
    "Config",
    "ContentType",
    "ContentStatus",
    "DistributionChannel",
    "SEOPriority",
    "ContentMetric",
    "AnalyticsTimeframe",
    "CalendarEntry",
    "ContentPiece",
    "SEOReport",
    "DistributionResult",
    "PerformanceSnapshot",
]

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ContentType(Enum):
    """Primary content types supported by the system."""
    BLOG_POST = "blog_post"
    VIDEO = "video"
    PODCAST = "podcast"
    INFOGRAPHIC = "infographic"
    WHITEPAPER = "whitepaper"
    CASE_STUDY = "case_study"
    EBOOK = "ebook"
    SOCIAL_POST = "social_post"
    EMAIL_NEWSLETTER = "email_newsletter"
    WEBINAR = "webinar"
    LANDING_PAGE = "landing_page"
    PRESS_RELEASE = "press_release"
    TUTORIAL = "tutorial"
    PRODUCT_REVIEW = "product_review"
    INTERVIEW = "interview"
    NEWSLETTER = "newsletter"
    MICRO_CONTENT = "micro_content"
    USER_GENERATED = "user_generated"
    GUEST_POST = "guest_post"
    SYNDICATED = "syndicated"


class ContentStatus(Enum):
    """Lifecycle status of a content piece."""
    IDEATION = "ideation"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    PROMOTING = "promoting"
    ARCHIVED = "archived"
    REPURPOSED = "repurposed"
    DECLINED = "declined"


class DistributionChannel(Enum):
    """Channels through which content can be distributed."""
    ORGANIC_SEARCH = "organic_search"
    SOCIAL_MEDIA_FACEBOOK = "social_media_facebook"
    SOCIAL_MEDIA_TWITTER = "social_media_twitter"
    SOCIAL_MEDIA_LINKEDIN = "social_media_linkedin"
    SOCIAL_MEDIA_INSTAGRAM = "social_media_instagram"
    SOCIAL_MEDIA_TIKTOK = "social_media_tiktok"
    SOCIAL_MEDIA_PINTEREST = "social_media_pinterest"
    EMAIL_MARKETING = "email_marketing"
    PAID_SEARCH = "paid_search"
    PAID_SOCIAL = "paid_social"
    CONTENT_SYNDICATION = "content_syndication"
    PARTNER_NETWORK = "partner_network"
    INFLUENCER_OUTREACH = "influencer_outreach"
    COMMUNITY_FORUMS = "community_forums"
    SLIDE_SHARE = "slide_share"
    MEDIUM = "medium"
    GITHUB = "github"
    YOUTUBE = "youtube"
    PODCAST_DIRECTORIES = "podcast_directories"
    RSS_FEED = "rss_feed"
    PRESS_WIRE = "press_wire"
    MICROSOFT_START = "microsoft_start"
    NEWS_GOOGLE = "news_google"
    AMP_CACHE = "amp_cache"
    AGGREGATORS = "aggregators"


class SEOPriority(IntEnum):
    """Priority levels for SEO optimization tasks."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKLOG = 5


class ContentMetric(Enum):
    """Metrics tracked for content performance."""
    PAGEVIEWS = "pageviews"
    UNIQUE_VISITORS = "unique_visitors"
    SESSIONS = "sessions"
    BOUNCE_RATE = "bounce_rate"
    TIME_ON_PAGE = "time_on_page"
    AVG_READ_TIME = "avg_read_time"
    SCROLL_DEPTH = "scroll_depth"
    CLICK_THROUGH_RATE = "click_through_rate"
    CONVERSION_RATE = "conversion_rate"
    SOCIAL_SHARES = "social_shares"
    BACKLINKS = "backlinks"
    KEYWORD_RANKINGS = "keyword_rankings"
    DOMAIN_AUTHORITY = "domain_authority"
    ORGANIC_TRAFFIC = "organic_traffic"
    REFERRAL_TRAFFIC = "referral_traffic"
    EMAIL_OPEN_RATE = "email_open_rate"
    EMAIL_CLICK_RATE = "email_click_rate"
    SUBSCRIBER_GROWTH = "subscriber_growth"
    ENGAGEMENT_SCORE = "engagement_score"
    REVENUE_ATTRIBUTION = "revenue_attribution"


class AnalyticsTimeframe(Enum):
    """Timeframes for analytics reporting."""
    REALTIME = "realtime"
    TODAY = "today"
    YESTERDAY = "yesterday"
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"
    LAST_12_MONTHS = "last_12_months"
    CUSTOM = "custom"
    WEEK_TO_DATE = "week_to_date"
    MONTH_TO_DATE = "month_to_date"
    QUARTER_TO_DATE = "quarter_to_date"
    YEAR_TO_DATE = "year_to_date"


class AudienceSegment(Enum):
    """Target audience segments for content targeting."""
    ALL = "all"
    NEW_VISITORS = "new_visitors"
    RETURNING_VISITORS = "returning_visitors"
    SUBSCRIBERS = "subscribers"
    CUSTOMERS = "customers"
    LEADS = "leads"
    ENTERPRISE = "enterprise"
    SMB = "smb"
    TECHNICAL = "technical"
    EXECUTIVE = "executive"
    MANAGER = "manager"
    DEVELOPER = "developer"
    DESIGNER = "designer"
    MARKETER = "marketer"
    STUDENT = "student"
    AGENCY = "agency"


class ContentGoal(Enum):
    """Strategic goals for content pieces."""
    AWARENESS = "awareness"
    EDUCATION = "education"
    CONSIDERATION = "consideration"
    CONVERSION = "conversion"
    RETENTION = "retention"
    ADVOCACY = "advocacy"
    BRAND_BUILDING = "brand_building"
    THOUGHT_LEADERSHIP = "thought_leadership"
    LEAD_GENERATION = "lead_generation"
    CUSTOMER_SUCCESS = "customer_success"
    COMMUNITY_BUILDING = "community_building"
    SEO_AUTHORITY = "seo_authority"


class ContentFormat(Enum):
    """Detailed content format specifications."""
    LONG_FORM_ARTICLE = "long_form_article"
    SHORT_FORM_ARTICLE = "short_form_article"
    LISTICLE = "listicle"
    HOW_TO_GUIDE = "how_to_guide"
    COMPARISON = "comparison"
    ROUNDUP = "roundup"
    CASE_STUDY_NARRATIVE = "case_study_narrative"
    TUTORIAL_STEP_BY_STEP = "tutorial_step_by_step"
    VIDEO_TUTORIAL = "video_tutorial"
    VIDEO_INTERVIEW = "video_interview"
    VIDEO_DEMO = "video_demo"
    PODCAST_EPISODE = "podcast_episode"
    PODCAST_INTERVIEW = "podcast_episode_interview"
    INFOGRAPHIC_DATA = "infographic_data"
    INFOGRAPHIC_PROCESS = "infographic_process"
    WHITEPAPER_TECHNICAL = "whitepaper_technical"
    WHITEPAPER_BUSINESS = "whitepaper_business"
    EBOOK_GUIDE = "ebook_guide"
    TEMPLATE = "template"
    CHECKLIST = "checklist"
    CHEAT_SHEET = "cheat_sheet"
    WEBINAR_LIVE = "webinar_live"
    WEBINAR_ON_DEMAND = "webinar_on_demand"
    EMAIL序列 = "email_sequence"
    SOCIAL_THREAD = "social_thread"
    SOCIAL_CAROUSEL = "social_carousel"
    SOCIAL_STORY = "social_story"
    LANDING_PAGE_HERO = "landing_page_hero"
    LANDING_PAGE_SQUEEZE = "landing_page_squeeze"
    PRESS_RELEASE_STANDARD = "press_release_standard"
    PRESS_RELEASE_PRODUCT = "press_release_product"
    GUEST_POST_STANDARD = "guest_post_standard"
    SYNDICATED_ARTICLE = "syndicated_article"
    MICRO_CONTENT_SNIPPET = "micro_content_snippet"


class CalendarView(Enum):
    """Calendar view modes."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CONTENT_TYPE = "content_type"
    CHANNEL = "channel"
    AUTHOR = "author"
    TOPIC = "topic"


class KeywordIntent(Enum):
    """Search intent classification for keywords."""
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    TRANSACTIONAL = "transactional"
    COMMERCIAL = "commercial"
    LOCAL = "local"
    MIXED = "mixed"


class CompetitionLevel(Enum):
    """Keyword competition difficulty levels."""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ContentTone(Enum):
    """Tone and voice settings for content."""
    PROFESSIONAL = "professional"
    CONVERSATIONAL = "conversational"
    AUTHORITATIVE = "authoritative"
    FRIENDLY = "friendly"
    TECHNICAL = "technical"
    CASUAL = "casual"
    FORMAL = "formal"
    INSPIRATIONAL = "inspirational"
    HUMOROUS = "humorous"
    EDUCATIONAL = "educational"
    EMPATHETIC = "empathetic"
    URGENT = "urgent"


class DistributionTiming(Enum):
    """Optimal timing strategies for distribution."""
    REAL_TIME = "real_time"
    SCHEDULED_OPTIMAL = "scheduled_optimal"
    BURST = "burst"
    DRIP = "drip"
    EVERGREEN_ROTATION = "evergreen_rotation"
    EVENT_DRIVEN = "event_driven"
    TRENDING = "trending"


class ContentStage(Enum):
    """Content funnel stage alignment."""
    TOP_OF_FUNNEL = "top_of_funnel"
    MIDDLE_OF_FUNNEL = "middle_of_funnel"
    BOTTOM_OF_FUNNEL = "bottom_of_funnel"
    POST_PURCHASE = "post_purchase"
    CUSTOMER_SUCCESS = "customer_success"
    ADVOCACY = "advocacy"
    BRAND_AWARENESS = "brand_awareness"


class TopicClusterType(Enum):
    """Types within a topic cluster strategy."""
    PILLAR = "pillar"
    CLUSTER = "cluster"
    SUPPORTING = "supporting"
    SATELLITE = "satellite"
    CORNERSTONE = "cornerstone"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class SEOConfig:
    """SEO-specific configuration settings."""
    target_keyword_density: float = 0.02
    max_keyword_density: float = 0.04
    min_word_count: int = 300
    max_word_count: int = 5000
    ideal_word_count: int = 1500
    target_readability_score: float = 70.0
    min_readability_score: float = 50.0
    max_title_length: int = 60
    max_meta_description_length: int = 160
    max_h1_count: int = 1
    max_internal_links: int = 10
    min_internal_links: int = 3
    target_images_per_1000_words: float = 1.5
    max_alt_tag_length: int = 125
    enable_schema_markup: bool = True
    enable_open_graph: bool = True
    enable_twitter_cards: bool = True
    canonical_url_enforcement: bool = True
    mobile_first_optimization: bool = True
    core_web_vitals_target: Dict[str, float] = field(
        default_factory=lambda: {
            "lcp": 2.5,
            "fid": 100,
            "cls": 0.1,
            "inp": 200,
        }
    )


@dataclass
class DistributionConfig:
    """Configuration for content distribution channels."""
    primary_channels: List[DistributionChannel] = field(
        default_factory=lambda: [
            DistributionChannel.ORGANIC_SEARCH,
            DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
            DistributionChannel.EMAIL_MARKETING,
        ]
    )
    secondary_channels: List[DistributionChannel] = field(
        default_factory=lambda: [
            DistributionChannel.SOCIAL_MEDIA_TWITTER,
            DistributionChannel.SOCIAL_MEDIA_FACEBOOK,
            DistributionChannel.CONTENT_SYNDICATION,
        ]
    )
    posting_schedule: Dict[str, List[str]] = field(default_factory=dict)
    cross_post_enabled: bool = True
    auto_share_enabled: bool = False
    hashtag_limit: int = 5
    utm_parameter_template: str = "utm_source={source}&utm_medium={medium}&utm_campaign={campaign}"
    content_repurpose_threshold_days: int = 90
    syndication_delay_days: int = 7
    influencer_outreach_enabled: bool = False
    paid_amplification_budget: float = 0.0
    amplification_roi_threshold: float = 2.0


@dataclass
class AnalyticsConfig:
    """Configuration for analytics and reporting."""
    default_timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS
    realtime_refresh_interval_seconds: int = 30
    report_generation_timeout_seconds: int = 300
    data_retention_days: int = 730
    comparison_enabled: bool = True
    comparison_periods: int = 2
    goal_tracking_enabled: bool = True
    attribution_model: str = "last_touch"
    custom_dimensions_enabled: bool = False
    export_formats: List[str] = field(
        default_factory=lambda: ["json", "csv", "markdown", "pdf"]
    )
    alert_thresholds: Dict[str, float] = field(
        default_factory=lambda: {
            "bounce_rate_high": 0.70,
            "conversion_rate_low": 0.01,
            "traffic_drop_percent": 0.20,
            "engagement_drop_percent": 0.15,
        }
    )
    benchmark_enabled: bool = True
    cohort_analysis_enabled: bool = False
    funnel_visualization_enabled: bool = True


@dataclass
class Config:
    """Main configuration for the Content Marketing Agent."""
    agent_name: str = "ContentMarketingAgent"
    version: str = "3.0.0"
    log_level: str = "INFO"
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    max_concurrent_operations: int = 10
    seo: SEOConfig = field(default_factory=SEOConfig)
    distribution: DistributionConfig = field(default_factory=DistributionConfig)
    analytics: AnalyticsConfig = field(default_factory=AnalyticsConfig)
    timezone: str = "UTC"
    default_author: str = "content-team"
    brand_voice: ContentTone = ContentTone.PROFESSIONAL
    content_review_required: bool = True
    auto_optimize_enabled: bool = True
    topic_cluster_enabled: bool = True
    content_scoring_enabled: bool = True
    competitor_analysis_enabled: bool = False
    api_keys: Dict[str, str] = field(default_factory=dict)
    webhook_urls: Dict[str, str] = field(default_factory=dict)
    notification_channels: List[str] = field(default_factory=lambda: ["email"])
    export_directory: str = "./exports"
    template_directory: str = "./templates"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------


@dataclass
class Keyword:
    """Represents a target keyword with SEO metadata."""
    keyword: str
    search_volume: int = 0
    keyword_difficulty: float = 0.0
    cost_per_click: float = 0.0
    intent: KeywordIntent = KeywordIntent.INFORMATIONAL
    competition: CompetitionLevel = CompetitionLevel.MEDIUM
    current_rank: Optional[int] = None
    target_rank: int = 10
    related_keywords: List[str] = field(default_factory=list)
    long_tail_variations: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    clusters: List[str] = field(default_factory=list)
    last_checked: Optional[datetime] = None
    trend_direction: str = "stable"

    @property
    def opportunity_score(self) -> float:
        """Calculate keyword opportunity score based on volume and difficulty."""
        if self.keyword_difficulty == 0:
            return float(self.search_volume)
        volume_weight = min(self.search_volume / 1000, 10)
        difficulty_weight = max(10 - self.keyword_difficulty, 0)
        intent_bonus = {
            KeywordIntent.TRANSACTIONAL: 1.5,
            KeywordIntent.COMMERCIAL: 1.3,
            KeywordIntent.INFORMATIONAL: 1.0,
            KeywordIntent.NAVIGATIONAL: 0.8,
            KeywordIntent.LOCAL: 1.2,
            KeywordIntent.MIXED: 1.0,
        }
        return volume_weight * difficulty_weight * intent_bonus.get(self.intent, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyword": self.keyword,
            "search_volume": self.search_volume,
            "keyword_difficulty": self.keyword_difficulty,
            "cost_per_click": self.cost_per_click,
            "intent": self.intent.value,
            "competition": self.competition.value,
            "current_rank": self.current_rank,
            "target_rank": self.target_rank,
            "related_keywords": self.related_keywords,
            "long_tail_variations": self.long_tail_variations,
            "questions": self.questions,
            "clusters": self.clusters,
            "opportunity_score": round(self.opportunity_score, 2),
            "last_checked": self.last_checked.isoformat() if self.last_checked else None,
            "trend_direction": self.trend_direction,
        }


@dataclass
class ContentPiece:
    """Represents a single piece of content throughout its lifecycle."""
    content_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    title: str = ""
    slug: str = ""
    content_type: ContentType = ContentType.BLOG_POST
    status: ContentStatus = ContentStatus.IDEATION
    stage: ContentStage = ContentStage.TOP_OF_FUNNEL
    format: ContentFormat = ContentFormat.LONG_FORM_ARTICLE
    author: str = ""
    team: str = ""
    topic: str = ""
    cluster_id: Optional[str] = None
    keywords: List[Keyword] = field(default_factory=list)
    target_audience: List[AudienceSegment] = field(default_factory=list)
    goals: List[ContentGoal] = field(default_factory=list)
    tone: ContentTone = ContentTone.PROFESSIONAL
    word_count: int = 0
    reading_time_minutes: int = 0
    channels: List[DistributionChannel] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    brief: str = ""
    outline: List[str] = field(default_factory=list)
    body_markdown: str = ""
    meta_title: str = ""
    meta_description: str = ""
    canonical_url: str = ""
    og_image: str = ""
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    internal_links: List[str] = field(default_factory=list)
    external_links: List[str] = field(default_factory=list)
    images: List[Dict[str, str]] = field(default_factory=list)
    schema_markup: Dict[str, Any] = field(default_factory=dict)
    utm_parameters: Dict[str, str] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    seo_score: float = 0.0
    content_score: float = 0.0
    engagement_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    review_notes: List[Dict[str, Any]] = field(default_factory=list)
    version_history: List[Dict[str, Any]] = field(default_factory=list)
    repurposed_from: Optional[str] = None
    repurposed_into: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    assets: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.slug and self.title:
            self.slug = self._generate_slug(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.reading_time_minutes and self.word_count:
            self.reading_time_minutes = max(1, self.word_count // 238)

    @staticmethod
    def _generate_slug(title: str) -> str:
        slug = title.lower().strip()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug[:80].rstrip("-")

    def add_keyword(self, keyword: Keyword) -> None:
        if not any(k.keyword == keyword.keyword for k in self.keywords):
            self.keywords.append(keyword)
            self.updated_at = datetime.utcnow()

    def update_status(self, new_status: ContentStatus) -> None:
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()
        self.version_history.append({
            "from": old_status.value,
            "to": new_status.value,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def add_review_note(self, reviewer: str, note: str, category: str = "general") -> None:
        self.review_notes.append({
            "reviewer": reviewer,
            "note": note,
            "category": category,
            "timestamp": datetime.utcnow().isoformat(),
        })
        self.updated_at = datetime.utcnow()

    def calculate_seo_score(self, config: SEOConfig) -> float:
        score = 0.0
        if self.meta_title and len(self.meta_title) <= config.max_title_length:
            score += 15
        if self.meta_description and len(self.meta_description) <= config.max_meta_description_length:
            score += 15
        if config.min_word_count <= self.word_count <= config.max_word_count:
            score += 20
        elif self.word_count > 0:
            score += 10
        if self.keywords:
            primary_keyword = self.keywords[0].keyword.lower()
            if primary_keyword in self.title.lower():
                score += 15
            if primary_keyword in self.meta_description.lower():
                score += 10
            if primary_keyword in self.body_markdown.lower():
                keyword_count = self.body_markdown.lower().count(primary_keyword)
                density = keyword_count / max(self.word_count, 1)
                if config.target_keyword_density <= density <= config.max_keyword_density:
                    score += 15
        if self.images:
            score += 5
        if len(self.internal_links) >= config.min_internal_links:
            score += 5
        self.seo_score = min(100.0, score)
        return self.seo_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_id": self.content_id,
            "title": self.title,
            "slug": self.slug,
            "content_type": self.content_type.value,
            "status": self.status.value,
            "stage": self.stage.value,
            "format": self.format.value,
            "author": self.author,
            "team": self.team,
            "topic": self.topic,
            "cluster_id": self.cluster_id,
            "keywords": [k.to_dict() for k in self.keywords],
            "target_audience": [a.value for a in self.target_audience],
            "goals": [g.value for g in self.goals],
            "tone": self.tone.value,
            "word_count": self.word_count,
            "reading_time_minutes": self.reading_time_minutes,
            "channels": [c.value for c in self.channels],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "canonical_url": self.canonical_url,
            "tags": self.tags,
            "categories": self.categories,
            "internal_links": self.internal_links,
            "external_links": self.external_links,
            "seo_score": self.seo_score,
            "content_score": self.content_score,
            "engagement_score": self.engagement_score,
            "performance": self.performance,
            "metadata": self.metadata,
        }


@dataclass
class CalendarEntry:
    """Represents a single entry in the editorial calendar."""
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    date: datetime = field(default_factory=datetime.utcnow)
    content_piece: Optional[ContentPiece] = None
    content_type: ContentType = ContentType.BLOG_POST
    channel: DistributionChannel = DistributionChannel.ORGANIC_SEARCH
    author: str = ""
    topic: str = ""
    status: ContentStatus = ContentStatus.PLANNED
    priority: int = 3
    notes: str = ""
    dependencies: List[str] = field(default_factory=list)
    is_locked: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "date": self.date.isoformat(),
            "content_type": self.content_type.value,
            "channel": self.channel.value,
            "author": self.author,
            "topic": self.topic,
            "status": self.status.value,
            "priority": self.priority,
            "notes": self.notes,
            "is_locked": self.is_locked,
        }


@dataclass
class TopicCluster:
    """Represents a topic cluster for content strategy."""
    cluster_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    pillar_topic: str = ""
    pillar_content: Optional[str] = None
    cluster_type: TopicClusterType = TopicClusterType.PILLAR
    supporting_topics: List[str] = field(default_factory=list)
    supporting_content: List[str] = field(default_factory=list)
    keywords: List[Keyword] = field(default_factory=list)
    total_content_count: int = 0
    total_traffic: int = 0
    total_backlinks: int = 0
    authority_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_supporting_content(self, content_id: str, topic: str) -> None:
        if content_id not in self.supporting_content:
            self.supporting_content.append(content_id)
            if topic not in self.supporting_topics:
                self.supporting_topics.append(topic)
            self.total_content_count = len(self.supporting_content)
            self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "pillar_topic": self.pillar_topic,
            "pillar_content": self.pillar_content,
            "cluster_type": self.cluster_type.value,
            "supporting_topics": self.supporting_topics,
            "supporting_content": self.supporting_content,
            "keywords": [k.to_dict() for k in self.keywords],
            "total_content_count": self.total_content_count,
            "total_traffic": self.total_traffic,
            "total_backlinks": self.total_backlinks,
            "authority_score": self.authority_score,
        }


@dataclass
class ContentBrief:
    """Detailed content brief for writers."""
    brief_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    target_word_count: int = 1500
    primary_keyword: str = ""
    secondary_keywords: List[str] = field(default_factory=list)
    target_audience: str = ""
    search_intent: KeywordIntent = KeywordIntent.INFORMATIONAL
    content_type: ContentType = ContentType.BLOG_POST
    tone: ContentTone = ContentTone.PROFESSIONAL
    goals: List[ContentGoal] = field(default_factory=list)
    outline: List[str] = field(default_factory=list)
    required_sections: List[str] = field(default_factory=list)
    reference_urls: List[str] = field(default_factory=list)
    competitor_urls: List[str] = field(default_factory=list)
    internal_link_opportunities: List[str] = field(default_factory=list)
    call_to_action: str = ""
    deadline: Optional[datetime] = None
    special_instructions: str = ""
    persona_notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "brief_id": self.brief_id,
            "title": self.title,
            "target_word_count": self.target_word_count,
            "primary_keyword": self.primary_keyword,
            "secondary_keywords": self.secondary_keywords,
            "target_audience": self.target_audience,
            "search_intent": self.search_intent.value,
            "content_type": self.content_type.value,
            "tone": self.tone.value,
            "goals": [g.value for g in self.goals],
            "outline": self.outline,
            "required_sections": self.required_sections,
            "reference_urls": self.reference_urls,
            "competitor_urls": self.competitor_urls,
            "internal_link_opportunities": self.internal_link_opportunities,
            "call_to_action": self.call_to_action,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "special_instructions": self.special_instructions,
        }


@dataclass
class SEOReport:
    """SEO analysis report for content."""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content_id: str = ""
    overall_score: float = 0.0
    technical_score: float = 0.0
    content_score: float = 0.0
    on_page_score: float = 0.0
    off_page_score: float = 0.0
    issues: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    keyword_analysis: Dict[str, Any] = field(default_factory=dict)
    readability_analysis: Dict[str, Any] = field(default_factory=dict)
    competitor_comparison: Dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def add_issue(self, severity: str, category: str, message: str, fix: str = "") -> None:
        self.issues.append({
            "severity": severity,
            "category": category,
            "message": message,
            "fix": fix,
        })

    def add_recommendation(self, recommendation: str) -> None:
        self.recommendations.append(recommendation)

    def calculate_overall_score(self) -> float:
        weights = {"technical": 0.25, "content": 0.35, "on_page": 0.30, "off_page": 0.10}
        self.overall_score = (
            self.technical_score * weights["technical"]
            + self.content_score * weights["content"]
            + self.on_page_score * weights["on_page"]
            + self.off_page_score * weights["off_page"]
        )
        return self.overall_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "content_id": self.content_id,
            "overall_score": round(self.overall_score, 2),
            "technical_score": round(self.technical_score, 2),
            "content_score": round(self.content_score, 2),
            "on_page_score": round(self.on_page_score, 2),
            "off_page_score": round(self.off_page_score, 2),
            "issues": self.issues,
            "recommendations": self.recommendations,
            "keyword_analysis": self.keyword_analysis,
            "readability_analysis": self.readability_analysis,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class DistributionResult:
    """Result of a content distribution operation."""
    result_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content_id: str = ""
    channel: DistributionChannel = DistributionChannel.ORGANIC_SEARCH
    status: str = "pending"
    scheduled_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    url: str = ""
    reach: int = 0
    impressions: int = 0
    clicks: int = 0
    shares: int = 0
    engagement_rate: float = 0.0
    cost: float = 0.0
    roi: float = 0.0
    utm_parameters: Dict[str, str] = field(default_factory=dict)
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_successful(self) -> bool:
        return self.status == "published" and not self.error_message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "content_id": self.content_id,
            "channel": self.channel.value,
            "status": self.status,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "url": self.url,
            "reach": self.reach,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "shares": self.shares,
            "engagement_rate": self.engagement_rate,
            "cost": self.cost,
            "roi": self.roi,
            "utm_parameters": self.utm_parameters,
            "error_message": self.error_message,
        }


@dataclass
class PerformanceSnapshot:
    """Snapshot of content performance metrics at a point in time."""
    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content_id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS
    metrics: Dict[str, float] = field(default_factory=dict)
    channel_breakdown: Dict[str, Dict[str, float]] = field(default_factory=dict)
    audience_breakdown: Dict[str, Dict[str, float]] = field(default_factory=dict)
    device_breakdown: Dict[str, Dict[str, float]] = field(default_factory=dict)
    geographic_breakdown: Dict[str, Dict[str, float]] = field(default_factory=dict)
    conversion_events: List[Dict[str, Any]] = field(default_factory=list)
    revenue_attributed: float = 0.0
    cost_per_acquisition: float = 0.0
    lifetime_value_impact: float = 0.0
    comparison_data: Optional[Dict[str, Any]] = None
    anomalies: List[Dict[str, Any]] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)

    def get_metric(self, metric: ContentMetric, default: float = 0.0) -> float:
        return self.metrics.get(metric.value, default)

    def set_metric(self, metric: ContentMetric, value: float) -> None:
        self.metrics[metric.value] = value

    def compare_with(self, other: "PerformanceSnapshot") -> Dict[str, float]:
        changes: Dict[str, float] = {}
        all_keys = set(self.metrics.keys()) | set(other.metrics.keys())
        for key in all_keys:
            current = self.metrics.get(key, 0.0)
            previous = other.metrics.get(key, 0.0)
            if previous > 0:
                changes[key] = ((current - previous) / previous) * 100
            else:
                changes[key] = 100.0 if current > 0 else 0.0
        return changes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "content_id": self.content_id,
            "timestamp": self.timestamp.isoformat(),
            "timeframe": self.timeframe.value,
            "metrics": self.metrics,
            "channel_breakdown": self.channel_breakdown,
            "audience_breakdown": self.audience_breakdown,
            "revenue_attributed": self.revenue_attributed,
            "anomalies": self.anomalies,
            "insights": self.insights,
        }


@dataclass
class ContentStrategy:
    """Complete content strategy definition."""
    strategy_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    target_market: str = ""
    mission_statement: str = ""
    brand_voice: ContentTone = ContentTone.PROFESSIONAL
    target_audiences: List[AudienceSegment] = field(default_factory=list)
    primary_goals: List[ContentGoal] = field(default_factory=list)
    content_pillars: List[str] = field(default_factory=list)
    topic_clusters: List[TopicCluster] = field(default_factory=list)
    competitor_landscape: List[Dict[str, Any]] = field(default_factory=list)
    swot_analysis: Dict[str, List[str]] = field(default_factory=dict)
    budget: float = 0.0
    team_roles: Dict[str, List[str]] = field(default_factory=dict)
    kpis: List[Dict[str, Any]] = field(default_factory=list)
    content_mix: Dict[ContentType, float] = field(default_factory=dict)
    channel_mix: Dict[DistributionChannel, float] = field(default_factory=dict)
    publishing_frequency: Dict[ContentType, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    review_cycle_days: int = 90
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_pillar(self, pillar: str) -> None:
        if pillar not in self.content_pillars:
            self.content_pillars.append(pillar)
            self.updated_at = datetime.utcnow()

    def add_topic_cluster(self, cluster: TopicCluster) -> None:
        existing_ids = {c.cluster_id for c in self.topic_clusters}
        if cluster.cluster_id not in existing_ids:
            self.topic_clusters.append(cluster)
            self.updated_at = datetime.utcnow()

    def get_content_mix_summary(self) -> Dict[str, Any]:
        total = sum(self.content_mix.values()) or 1.0
        return {ct.value: round((pct / total) * 100, 1) for ct, pct in self.content_mix.items()}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "name": self.name,
            "description": self.description,
            "target_market": self.target_market,
            "mission_statement": self.mission_statement,
            "brand_voice": self.brand_voice.value,
            "target_audiences": [a.value for a in self.target_audiences],
            "primary_goals": [g.value for g in self.primary_goals],
            "content_pillars": self.content_pillars,
            "topic_clusters": [c.to_dict() for c in self.topic_clusters],
            "budget": self.budget,
            "content_mix": {k.value: v for k, v in self.content_mix.items()},
            "channel_mix": {k.value: v for k, v in self.channel_mix.items()},
            "publishing_frequency": {k.value: v for k, v in self.publishing_frequency.items()},
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
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
        raise ValidationError(
            field_name,
            f"Value {value} is out of range [{min_val}, {max_val}].",
        )


def _validate_list_not_empty(items: List[Any], field_name: str) -> None:
    if not items:
        raise ValidationError(field_name, "This list must contain at least one item.")


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------


class ContentMarketingAgent:
    """Comprehensive content marketing management agent.

    Orchestrates the full content marketing lifecycle:
    - Strategy development and management
    - Editorial calendar planning and scheduling
    - Content brief creation and management
    - SEO content optimization and auditing
    - Multi-channel content distribution
    - Performance analytics and reporting

    Example::

        agent = ContentMarketingAgent()
        strategy = agent.create_content_strategy(
            name="Q3 Growth Strategy",
            target_market="SaaS startups",
            pillars=["thought leadership", "product education", "customer stories"],
        )
        calendar = agent.create_editorial_calendar(strategy_id=strategy.strategy_id, months=3)
        brief = agent.create_content_brief(title="Ultimate Guide to CRO", primary_keyword="conversion rate optimization")
        seo_report = agent.analyze_seo(content_id=brief.brief_id)
        distribution = agent.distribute_content(content_id=brief.brief_id)
        analytics = agent.get_content_analytics(timeframe=AnalyticsTimeframe.LAST_30_DAYS)
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self._config = config or Config()
        self._cache = _Cache(ttl_seconds=self._config.cache_ttl_seconds) if self._config.enable_caching else None
        self._strategies: Dict[str, ContentStrategy] = {}
        self._calendars: Dict[str, EditorialCalendar] = {}
        self._content_pieces: Dict[str, ContentPiece] = {}
        self._briefs: Dict[str, ContentBrief] = {}
        self._seo_reports: Dict[str, SEOReport] = {}
        self._distribution_results: Dict[str, DistributionResult] = {}
        self._performance_snapshots: Dict[str, List[PerformanceSnapshot]] = defaultdict(list)
        self._topic_clusters: Dict[str, TopicCluster] = {}
        self._operation_log: List[Dict[str, Any]] = []
        self._error_count: int = 0
        self._success_count: int = 0
        logger.info(
            "ContentMarketingAgent initialized (version=%s, caching=%s)",
            self._config.version,
            self._config.enable_caching,
        )

    # ----- Strategy -----

    def create_content_strategy(
        self,
        name: str,
        target_market: str,
        pillars: List[str],
        goals: Optional[List[ContentGoal]] = None,
        audiences: Optional[List[AudienceSegment]] = None,
        voice: ContentTone = ContentTone.PROFESSIONAL,
        budget: float = 0.0,
    ) -> ContentStrategy:
        """Create a new content strategy with pillars, goals, and audience targeting.

        Args:
            name: Strategy name.
            target_market: Description of target market.
            pillars: Core content pillars (3-7 recommended).
            goals: Strategic content goals.
            audiences: Target audience segments.
            voice: Brand voice and tone.
            budget: Annual content marketing budget.

        Returns:
            ContentStrategy: The created strategy object.

        Raises:
            ValidationError: If required fields are missing or invalid.
        """
        _validate_required(name, "name")
        _validate_required(target_market, "target_market")
        _validate_list_not_empty(pillars, "pillars")

        strategy = ContentStrategy(
            name=name,
            description=f"Content strategy for {target_market}",
            target_market=target_market,
            mission_statement=f"To provide valuable, relevant content for {target_market}",
            brand_voice=voice,
            target_audiences=audiences or [AudienceSegment.ALL],
            primary_goals=goals or [ContentGoal.AWARENESS, ContentGoal.EDUCATION],
            content_pillars=pillars,
            budget=budget,
            content_mix={
                ContentType.BLOG_POST: 0.35,
                ContentType.VIDEO: 0.20,
                ContentType.SOCIAL_POST: 0.15,
                ContentType.EMAIL_NEWSLETTER: 0.10,
                ContentType.WHITEPAPER: 0.10,
                ContentType.CASE_STUDY: 0.10,
            },
            channel_mix={
                DistributionChannel.ORGANIC_SEARCH: 0.35,
                DistributionChannel.SOCIAL_MEDIA_LINKEDIN: 0.20,
                DistributionChannel.EMAIL_MARKETING: 0.20,
                DistributionChannel.SOCIAL_MEDIA_TWITTER: 0.10,
                DistributionChannel.CONTENT_SYNDICATION: 0.10,
                DistributionChannel.PAID_SOCIAL: 0.05,
            },
        )
        self._strategies[strategy.strategy_id] = strategy
        self._log_operation("create_strategy", {"strategy_id": strategy.strategy_id, "name": name})
        logger.info("Content strategy created: %s (%s)", name, strategy.strategy_id)
        return strategy

    def update_content_strategy(
        self,
        strategy_id: str,
        **kwargs: Any,
    ) -> ContentStrategy:
        """Update an existing content strategy."""
        strategy = self._get_strategy(strategy_id)
        for key, value in kwargs.items():
            if hasattr(strategy, key) and value is not None:
                setattr(strategy, key, value)
        strategy.updated_at = datetime.utcnow()
        self._log_operation("update_strategy", {"strategy_id": strategy_id, "fields": list(kwargs.keys())})
        return strategy

    def get_content_strategy(self, strategy_id: str) -> ContentStrategy:
        """Retrieve a content strategy by ID."""
        return self._get_strategy(strategy_id)

    def list_strategies(self) -> List[ContentStrategy]:
        """List all content strategies."""
        return list(self._strategies.values())

    def delete_content_strategy(self, strategy_id: str) -> bool:
        """Delete a content strategy."""
        if strategy_id in self._strategies:
            del self._strategies[strategy_id]
            self._log_operation("delete_strategy", {"strategy_id": strategy_id})
            return True
        return False

    # ----- Editorial Calendar -----

    def create_editorial_calendar(
        self,
        strategy_id: str,
        months: int = 3,
        start_date: Optional[datetime] = None,
    ) -> "EditorialCalendar":
        """Create an editorial calendar aligned with the given strategy.

        Generates planned content entries based on the strategy's content mix
        and publishing frequency over the specified time period.

        Args:
            strategy_id: ID of the strategy to base the calendar on.
            months: Number of months to plan.
            start_date: Calendar start date (defaults to today).

        Returns:
            EditorialCalendar: The created calendar with planned entries.
        """
        strategy = self._get_strategy(strategy_id)
        start = start_date or datetime.utcnow()
        calendar = EditorialCalendar(
            name=f"Calendar for {strategy.name}",
            strategy_id=strategy_id,
            start_date=start,
            end_date=start + timedelta(days=months * 30),
        )
        self._generate_calendar_entries(calendar, strategy, months)
        self._calendars[calendar.calendar_id] = calendar
        self._log_operation(
            "create_calendar",
            {"calendar_id": calendar.calendar_id, "months": months, "entries": len(calendar.entries)},
        )
        logger.info(
            "Editorial calendar created: %d entries over %d months",
            len(calendar.entries),
            months,
        )
        return calendar

    def update_calendar_entry(
        self,
        calendar_id: str,
        entry_id: str,
        **kwargs: Any,
    ) -> CalendarEntry:
        """Update a specific calendar entry."""
        calendar = self._get_calendar(calendar_id)
        entry = calendar.get_entry(entry_id)
        if entry is None:
            raise ValidationError("entry_id", f"Entry {entry_id} not found in calendar.")
        for key, value in kwargs.items():
            if hasattr(entry, key) and value is not None:
                setattr(entry, key, value)
        return entry

    def get_calendar(self, calendar_id: str) -> "EditorialCalendar":
        """Retrieve a calendar by ID."""
        return self._get_calendar(calendar_id)

    def list_calendars(self) -> List["EditorialCalendar"]:
        """List all editorial calendars."""
        return list(self._calendars.values())

    def get_calendar_view(
        self,
        calendar_id: str,
        view: CalendarView = CalendarView.MONTHLY,
        date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get a calendar in the specified view format."""
        calendar = self._get_calendar(calendar_id)
        return calendar.get_view(view, date)

    # ----- Content Briefs -----

    def create_content_brief(
        self,
        title: str,
        primary_keyword: str,
        target_word_count: int = 1500,
        secondary_keywords: Optional[List[str]] = None,
        audience: str = "",
        intent: KeywordIntent = KeywordIntent.INFORMATIONAL,
        tone: ContentTone = ContentTone.PROFESSIONAL,
        goals: Optional[List[ContentGoal]] = None,
        outline: Optional[List[str]] = None,
        deadline: Optional[datetime] = None,
    ) -> ContentBrief:
        """Create a detailed content brief for writers.

        Generates a structured brief with keyword targeting, audience information,
        outline, and required sections to guide content creation.

        Args:
            title: Working title for the content piece.
            primary_keyword: Main target keyword.
            target_word_count: Target word count for the piece.
            secondary_keywords: Supporting keywords to include.
            audience: Target audience description.
            intent: Search intent for the primary keyword.
            tone: Desired content tone.
            goals: Content goals.
            outline: Suggested outline/headings.
            deadline: Content completion deadline.

        Returns:
            ContentBrief: The created content brief.
        """
        _validate_required(title, "title")
        _validate_required(primary_keyword, "primary_keyword")
        _validate_range(target_word_count, 100, 50000, "target_word_count")

        suggested_outline = outline or self._generate_outline(title, primary_keyword, intent)
        required_sections = self._determine_required_sections(content_type=ContentType.BLOG_POST, intent=intent)

        brief = ContentBrief(
            title=title,
            target_word_count=target_word_count,
            primary_keyword=primary_keyword,
            secondary_keywords=secondary_keywords or [],
            target_audience=audience,
            search_intent=intent,
            tone=tone,
            goals=goals or [ContentGoal.EDUCATION],
            outline=suggested_outline,
            required_sections=required_sections,
            deadline=deadline,
        )
        self._briefs[brief.brief_id] = brief
        self._log_operation("create_brief", {"brief_id": brief.brief_id, "title": title})
        logger.info("Content brief created: %s (%s)", title, brief.brief_id)
        return brief

    def update_content_brief(
        self,
        brief_id: str,
        **kwargs: Any,
    ) -> ContentBrief:
        """Update an existing content brief."""
        brief = self._get_brief(brief_id)
        for key, value in kwargs.items():
            if hasattr(brief, key) and value is not None:
                setattr(brief, key, value)
        return brief

    def get_content_brief(self, brief_id: str) -> ContentBrief:
        """Retrieve a content brief by ID."""
        return self._get_brief(brief_id)

    def list_briefs(self) -> List[ContentBrief]:
        """List all content briefs."""
        return list(self._briefs.values())

    def generate_content_from_brief(self, brief_id: str) -> ContentPiece:
        """Generate a content piece from a content brief.

        Creates a ContentPiece pre-populated with data from the brief,
        ready for content creation.
        """
        brief = self._get_brief(brief_id)
        primary_kw = Keyword(
            keyword=brief.primary_keyword,
            intent=brief.search_intent,
        )
        secondary_kws = [
            Keyword(keyword=kw, intent=KeywordIntent.INFORMATIONAL)
            for kw in brief.secondary_keywords
        ]
        content = ContentPiece(
            title=brief.title,
            content_type=brief.content_type,
            status=ContentStatus.PLANNED,
            stage=ContentStage.TOP_OF_FUNNEL,
            tone=brief.tone,
            word_count=brief.target_word_count,
            brief=brief.special_instructions,
            outline=brief.outline,
            keywords=[primary_kw] + secondary_kws,
            goals=brief.goals,
        )
        self._content_pieces[content.content_id] = content
        self._log_operation("generate_content_from_brief", {
            "brief_id": brief_id,
            "content_id": content.content_id,
        })
        return content

    # ----- SEO Optimization -----

    def analyze_seo(
        self,
        content_id: str,
        check_competitors: bool = False,
    ) -> SEOReport:
        """Perform comprehensive SEO analysis on a content piece.

        Analyzes technical SEO, on-page optimization, content quality,
        readability, and keyword usage. Returns a detailed report with
        scores, issues, and actionable recommendations.

        Args:
            content_id: ID of the content piece to analyze.
            check_competitors: Whether to include competitor comparison.

        Returns:
            SEOReport: Detailed SEO analysis report.
        """
        content = self._get_content(content_id)
        report = SEOReport(content_id=content_id)
        report.content_score = self._analyze_content_seo(content, report)
        report.on_page_score = self._analyze_on_page_seo(content, report)
        report.technical_score = self._analyze_technical_seo(content, report)
        report.off_page_score = self._analyze_off_page_seo(content, report)
        if check_competitors:
            report.competitor_comparison = self._analyze_competitor_seo(content)
        report.calculate_overall_score()
        content.seo_score = report.overall_score
        self._seo_reports[report.report_id] = report
        self._log_operation("analyze_seo", {
            "content_id": content_id,
            "overall_score": report.overall_score,
            "issues": len(report.issues),
        })
        logger.info(
            "SEO analysis complete for %s: score=%.1f, issues=%d",
            content_id,
            report.overall_score,
            len(report.issues),
        )
        return report

    def optimize_seo_content(
        self,
        content_id: str,
        target_keyword: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate SEO optimization recommendations for content.

        Returns a structured set of recommendations for improving
        the SEO performance of the content piece.

        Args:
            content_id: ID of the content piece to optimize.
            target_keyword: Primary keyword to optimize for.

        Returns:
            Dict containing optimization recommendations and scores.
        """
        content = self._get_content(content_id)
        recommendations: List[Dict[str, Any]] = []
        if target_keyword:
            kw_lower = target_keyword.lower()
            if kw_lower not in content.title.lower():
                recommendations.append({
                    "type": "title",
                    "priority": "high",
                    "message": f"Include '{target_keyword}' in the title.",
                })
            if kw_lower not in content.meta_description.lower():
                recommendations.append({
                    "type": "meta_description",
                    "priority": "high",
                    "message": f"Include '{target_keyword}' in the meta description.",
                })
            body_lower = content.body_markdown.lower()
            kw_count = body_lower.count(kw_lower)
            word_count = max(content.word_count, 1)
            density = kw_count / word_count
            if density < self._config.seo.target_keyword_density:
                recommendations.append({
                    "type": "keyword_density",
                    "priority": "medium",
                    "message": f"Keyword density is {density:.3%}, target is {self._config.seo.target_keyword_density:.1%}. "
                               f"Add ~{int((self._config.seo.target_keyword_density - density) * word_count)} more occurrences.",
                })
        if content.word_count < self._config.seo.min_word_count:
            recommendations.append({
                "type": "word_count",
                "priority": "high",
                "message": f"Content is {content.word_count} words. Minimum is {self._config.seo.min_word_count}.",
            })
        if not content.meta_title:
            recommendations.append({
                "type": "meta_title",
                "priority": "high",
                "message": "Add a meta title (H1 tag).",
            })
        if not content.meta_description:
            recommendations.append({
                "type": "meta_description",
                "priority": "high",
                "message": "Add a meta description.",
            })
        if len(content.images) < max(1, content.word_count // 1000):
            recommendations.append({
                "type": "images",
                "priority": "medium",
                "message": f"Add more images. Target: ~{max(1, content.word_count // 1000)} for this word count.",
            })
        if len(content.internal_links) < self._config.seo.min_internal_links:
            recommendations.append({
                "type": "internal_links",
                "priority": "medium",
                "message": f"Add more internal links. Current: {len(content.internal_links)}, "
                           f"minimum: {self._config.seo.min_internal_links}.",
            })
        if not content.canonical_url:
            recommendations.append({
                "type": "canonical_url",
                "priority": "medium",
                "message": "Add a canonical URL to prevent duplicate content issues.",
            })
        existing_report = self.analyze_seo(content_id)
        return {
            "content_id": content_id,
            "current_seo_score": existing_report.overall_score,
            "recommendations": recommendations,
            "issues": existing_report.issues,
            "estimated_improvement": self._estimate_seo_improvement(recommendations),
        }

    def generate_keyword_research(
        self,
        seed_keyword: str,
        topic: str = "",
        count: int = 20,
    ) -> List[Keyword]:
        """Generate keyword research from a seed keyword.

        Produces a list of related keywords with estimated metrics
        for content planning purposes.

        Args:
            seed_keyword: Starting keyword for research.
            topic: Optional topic context.
            count: Number of keywords to generate.

        Returns:
            List[Keyword]: List of researched keywords.
        """
        _validate_required(seed_keyword, "seed_keyword")
        _validate_range(count, 1, 200, "count")
        keywords: List[Keyword] = []
        intents = list(KeywordIntent)
        competitions = list(CompetitionLevel)
        modifiers = ["best", "top", "guide", "how to", "what is", "vs", "review", "tutorial"]
        long_tail_patterns = ["for beginners", "in 2026", "step by step", "examples", "tips"]
        base_keyword = Keyword(
            keyword=seed_keyword,
            search_volume=10000,
            keyword_difficulty=40.0,
            cost_per_click=2.50,
            intent=KeywordIntent.COMMERCIAL,
            competition=CompetitionLevel.MEDIUM,
        )
        keywords.append(base_keyword)
        for i in range(1, count):
            if i <= count // 3:
                modifier = modifiers[i % len(modifiers)]
                kw_text = f"{modifier} {seed_keyword}"
                intent = KeywordIntent.COMMERCIAL
            elif i <= 2 * count // 3:
                lt = long_tail_patterns[i % len(long_tail_patterns)]
                kw_text = f"{seed_keyword} {lt}"
                intent = KeywordIntent.INFORMATIONAL
            else:
                suffix = chr(ord("a") + (i % 26))
                kw_text = f"{seed_keyword} {suffix}"
                intent = intents[i % len(intents)]
            volume = max(100, 10000 - (i * 300) + (i % 5) * 100)
            difficulty = min(95, 20 + (i * 2) + (i % 3) * 5)
            kw = Keyword(
                keyword=kw_text,
                search_volume=volume,
                keyword_difficulty=float(difficulty),
                cost_per_click=round(0.5 + (i % 10) * 0.3, 2),
                intent=intent,
                competition=competitions[min(i % len(competitions), len(competitions) - 1)],
                target_rank=10 + (i % 20),
            )
            keywords.append(kw)
        logger.info("Generated %d keywords from seed '%s'", len(keywords), seed_keyword)
        return keywords

    def create_topic_cluster(
        self,
        pillar_topic: str,
        supporting_topics: List[str],
        keywords: Optional[List[Keyword]] = None,
    ) -> TopicCluster:
        """Create a topic cluster for content architecture.

        Args:
            pillar_topic: The main pillar topic.
            supporting_topics: Related subtopics for cluster content.
            keywords: Keywords associated with the cluster.

        Returns:
            TopicCluster: The created topic cluster.
        """
        _validate_required(pillar_topic, "pillar_topic")
        _validate_list_not_empty(supporting_topics, "supporting_topics")
        cluster = TopicCluster(
            pillar_topic=pillar_topic,
            supporting_topics=supporting_topics,
            keywords=keywords or [],
            cluster_type=TopicClusterType.PILLAR,
            total_content_count=len(supporting_topics) + 1,
        )
        self._topic_clusters[cluster.cluster_id] = cluster
        self._log_operation("create_topic_cluster", {
            "cluster_id": cluster.cluster_id,
            "pillar": pillar_topic,
            "supporting_count": len(supporting_topics),
        })
        return cluster

    # ----- Content Distribution -----

    def distribute_content(
        self,
        content_id: str,
        channels: Optional[List[DistributionChannel]] = None,
        schedule: Optional[Dict[DistributionChannel, datetime]] = None,
    ) -> List[DistributionResult]:
        """Distribute content across specified channels.

        Schedules or publishes content to the given distribution channels
        with appropriate UTM parameters and timing.

        Args:
            content_id: ID of the content to distribute.
            channels: Target distribution channels (defaults to strategy primary channels).
            schedule: Optional schedule for each channel.

        Returns:
            List[DistributionResult]: Results for each channel distribution.
        """
        content = self._get_content(content_id)
        target_channels = channels or self._config.distribution.primary_channels
        results: List[DistributionResult] = []
        for channel in target_channels:
            scheduled_time = schedule.get(channel) if schedule else datetime.utcnow()
            utm = self._build_utm_parameters(content, channel)
            result = DistributionResult(
                content_id=content_id,
                channel=channel,
                status="scheduled" if scheduled_time > datetime.utcnow() else "published",
                scheduled_at=scheduled_time,
                published_at=datetime.utcnow() if scheduled_time <= datetime.utcnow() else None,
                url=content.canonical_url or f"/content/{content.slug}",
                utm_parameters=utm,
            )
            self._distribution_results[result.result_id] = result
            results.append(result)
            if content.status == ContentStatus.IDEATION:
                content.update_status(ContentStatus.SCHEDULED)
            if channel not in content.channels:
                content.channels.append(channel)
        self._log_operation("distribute_content", {
            "content_id": content_id,
            "channels": [c.value for c in target_channels],
            "results_count": len(results),
        })
        logger.info(
            "Content %s distributed to %d channels",
            content_id,
            len(results),
        )
        return results

    def get_distribution_status(self, content_id: str) -> Dict[str, Any]:
        """Get distribution status for a content piece."""
        results = [
            r for r in self._distribution_results.values()
            if r.content_id == content_id
        ]
        return {
            "content_id": content_id,
            "total_distributions": len(results),
            "successful": sum(1 for r in results if r.is_successful),
            "failed": sum(1 for r in results if r.error_message),
            "channels": [r.to_dict() for r in results],
        }

    def get_optimal_posting_times(
        self,
        channel: DistributionChannel,
        audience: AudienceSegment = AudienceSegment.ALL,
    ) -> Dict[str, Any]:
        """Get optimal posting times for a channel and audience combination.

        Returns recommended posting schedule based on channel-specific
        best practices and audience behavior patterns.
        """
        defaults: Dict[DistributionChannel, Dict[str, Any]] = {
            DistributionChannel.SOCIAL_MEDIA_LINKEDIN: {
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "best_times": ["08:00", "10:00", "12:00", "17:00"],
                "timezone_recommendation": "audience_local",
                "frequency": "3-5 posts per week",
                "content_types": ["text", "image", "document", "video"],
            },
            DistributionChannel.SOCIAL_MEDIA_TWITTER: {
                "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "best_times": ["09:00", "12:00", "15:00", "18:00"],
                "timezone_recommendation": "audience_local",
                "frequency": "3-5 tweets per day",
                "content_types": ["text", "thread", "image", "link"],
            },
            DistributionChannel.SOCIAL_MEDIA_FACEBOOK: {
                "best_days": ["Wednesday", "Thursday", "Friday"],
                "best_times": ["09:00", "13:00", "15:00"],
                "timezone_recommendation": "audience_local",
                "frequency": "3-5 posts per week",
                "content_types": ["text", "image", "video", "link", "event"],
            },
            DistributionChannel.EMAIL_MARKETING: {
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "best_times": ["10:00", "14:00"],
                "timezone_recommendation": "audience_local",
                "frequency": "1-2 per week",
                "content_types": ["newsletter", "promotion", "transactional"],
            },
            DistributionChannel.ORGANIC_SEARCH: {
                "best_days": ["always"],
                "best_times": ["always"],
                "timezone_recommendation": "UTC",
                "frequency": "continuous",
                "content_types": ["blog", "landing_page", "resource"],
            },
        }
        schedule = defaults.get(channel, {
            "best_days": ["Monday", "Wednesday", "Friday"],
            "best_times": ["10:00", "14:00"],
            "timezone_recommendation": "audience_local",
            "frequency": "2-3 per week",
            "content_types": ["mixed"],
        })
        return {
            "channel": channel.value,
            "audience": audience.value,
            "schedule": schedule,
        }

    def repurpose_content(
        self,
        content_id: str,
        target_formats: List[ContentFormat],
    ) -> List[ContentBrief]:
        """Create content briefs for repurposing existing content into new formats.

        Takes an existing content piece and generates briefs for transforming
        it into different formats (e.g., blog post → video script, infographic).

        Args:
            content_id: ID of the source content.
            target_formats: Desired output formats.

        Returns:
            List[ContentBrief]: Briefs for each repurposed format.
        """
        source = self._get_content(content_id)
        briefs: List[ContentBrief] = []
        format_titles: Dict[ContentFormat, str] = {
            ContentFormat.VIDEO_TUTORIAL: f"Video Tutorial: {source.title}",
            ContentFormat.VIDEO_INTERVIEW: f"Interview Discussion: {source.title}",
            ContentFormat.INFOGRAPHIC_DATA: f"Infographic: {source.title}",
            ContentFormat.SOCIAL_CAROUSEL: f"Social Carousel: {source.title}",
            ContentFormat.PODCAST_EPISODE: f"Podcast Episode: {source.title}",
            ContentFormat.EBOOK_GUIDE: f"Comprehensive Guide: {source.title}",
            ContentFormat.CHECKLIST: f"Checklist: {source.title}",
            ContentFormat.CHEAT_SHEET: f"Cheat Sheet: {source.title}",
            ContentFormat.WEBINAR_LIVE: f"Webinar: {source.title}",
            ContentFormat.EMAIL序列: f"Email Sequence: {source.title}",
        }
        for fmt in target_formats:
            title = format_titles.get(fmt, f"Repurposed: {source.title}")
            brief = ContentBrief(
                title=title,
                primary_keyword=source.keywords[0].keyword if source.keywords else "",
                secondary_keywords=[k.keyword for k in source.keywords[1:]],
                content_type=source.content_type,
                tone=source.tone,
                goals=source.goals,
                special_instructions=f"Repurposed from content {content_id}. "
                                     f"Original title: {source.title}. Adapt for {fmt.value} format.",
            )
            self._briefs[brief.brief_id] = brief
            briefs.append(brief)
        source.repurposed_into.extend([b.brief_id for b in briefs])
        self._log_operation("repurpose_content", {
            "source_id": content_id,
            "target_formats": [f.value for f in target_formats],
            "briefs_created": len(briefs),
        })
        return briefs

    # ----- Content Management -----

    def create_content_piece(
        self,
        title: str,
        content_type: ContentType = ContentType.BLOG_POST,
        author: str = "",
        topic: str = "",
        keywords: Optional[List[Keyword]] = None,
        channels: Optional[List[DistributionChannel]] = None,
    ) -> ContentPiece:
        """Create a new content piece."""
        _validate_required(title, "title")
        content = ContentPiece(
            title=title,
            content_type=content_type,
            author=author or self._config.default_author,
            topic=topic,
            keywords=keywords or [],
            channels=channels or [],
            tone=self._config.brand_voice,
        )
        self._content_pieces[content.content_id] = content
        self._log_operation("create_content", {"content_id": content.content_id, "title": title})
        return content

    def update_content_status(
        self,
        content_id: str,
        new_status: ContentStatus,
    ) -> ContentPiece:
        """Update the status of a content piece."""
        content = self._get_content(content_id)
        content.update_status(new_status)
        self._log_operation("update_content_status", {
            "content_id": content_id,
            "new_status": new_status.value,
        })
        return content

    def get_content(self, content_id: str) -> ContentPiece:
        """Retrieve a content piece by ID."""
        return self._get_content(content_id)

    def list_content(
        self,
        status: Optional[ContentStatus] = None,
        content_type: Optional[ContentType] = None,
        author: Optional[str] = None,
    ) -> List[ContentPiece]:
        """List content pieces with optional filters."""
        results = list(self._content_pieces.values())
        if status:
            results = [c for c in results if c.status == status]
        if content_type:
            results = [c for c in results if c.content_type == content_type]
        if author:
            results = [c for c in results if c.author == author]
        return results

    def delete_content(self, content_id: str) -> bool:
        """Delete a content piece."""
        if content_id in self._content_pieces:
            del self._content_pieces[content_id]
            self._log_operation("delete_content", {"content_id": content_id})
            return True
        return False

    def get_content_pipeline(self) -> Dict[str, int]:
        """Get a count of content pieces by status (pipeline view)."""
        pipeline: Dict[str, int] = defaultdict(int)
        for content in self._content_pieces.values():
            pipeline[content.status.value] += 1
        return dict(pipeline)

    # ----- Analytics -----

    def record_performance(
        self,
        content_id: str,
        metrics: Dict[str, float],
        timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS,
        channel_breakdown: Optional[Dict[str, Dict[str, float]]] = None,
        audience_breakdown: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> PerformanceSnapshot:
        """Record performance metrics for a content piece.

        Creates a performance snapshot with the given metrics and optional
        breakdowns by channel, audience, device, and geography.

        Args:
            content_id: ID of the content piece.
            metrics: Dictionary of metric names to values.
            timeframe: The timeframe these metrics cover.
            channel_breakdown: Metrics broken down by channel.
            audience_breakdown: Metrics broken down by audience segment.

        Returns:
            PerformanceSnapshot: The recorded performance snapshot.
        """
        content = self._get_content(content_id)
        snapshot = PerformanceSnapshot(
            content_id=content_id,
            timeframe=timeframe,
            metrics=metrics,
            channel_breakdown=channel_breakdown or {},
            audience_breakdown=audience_breakdown or {},
        )
        content.performance.update(metrics)
        self._performance_snapshots[content_id].append(snapshot)
        self._log_operation("record_performance", {
            "content_id": content_id,
            "metric_count": len(metrics),
        })
        return snapshot

    def get_content_analytics(
        self,
        content_id: Optional[str] = None,
        timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS,
        metrics: Optional[List[ContentMetric]] = None,
    ) -> Dict[str, Any]:
        """Get content analytics with optional filtering.

        Aggregates performance data across content pieces for the specified
        timeframe and metrics.

        Args:
            content_id: Specific content piece (None for all).
            timeframe: Analytics timeframe.
            metrics: Specific metrics to include (None for all).

        Returns:
            Dict containing aggregated analytics data.
        """
        target_content = (
            [self._get_content(content_id)] if content_id
            else list(self._content_pieces.values())
        )
        aggregated: Dict[str, float] = defaultdict(float)
        count = 0
        for content in target_content:
            for key, value in content.performance.items():
                if metrics is None or key in [m.value for m in metrics]:
                    aggregated[key] += value
            count += 1
        averages = {k: round(v / max(count, 1), 2) for k, v in aggregated.items()}
        channel_totals: Dict[str, float] = defaultdict(float)
        for content in target_content:
            for ch in content.channels:
                channel_totals[ch.value] += 1
        pipeline = self.get_content_pipeline()
        return {
            "timeframe": timeframe.value,
            "content_count": count,
            "total_metrics": dict(aggregated),
            "average_metrics": averages,
            "channel_distribution": dict(channel_totals),
            "pipeline_status": pipeline,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_performance_comparison(
        self,
        content_id: str,
        current_timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS,
        previous_timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS,
    ) -> Dict[str, Any]:
        """Compare performance between two timeframes."""
        snapshots = self._performance_snapshots.get(content_id, [])
        if len(snapshots) < 2:
            return {
                "content_id": content_id,
                "comparison": {},
                "message": "Insufficient data for comparison.",
            }
        current = snapshots[-1]
        previous = snapshots[-2]
        changes = current.compare_with(previous)
        return {
            "content_id": content_id,
            "current_timeframe": current_timeframe.value,
            "previous_timeframe": previous_timeframe.value,
            "changes": changes,
            "current_metrics": current.metrics,
            "previous_metrics": previous.metrics,
        }

    def generate_performance_report(
        self,
        content_ids: Optional[List[str]] = None,
        timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS,
    ) -> Dict[str, Any]:
        """Generate a comprehensive performance report.

        Creates a detailed report covering all tracked metrics, trends,
        top performers, and actionable insights.
        """
        target_ids = content_ids or list(self._content_pieces.keys())
        all_metrics: Dict[str, List[float]] = defaultdict(list)
        content_scores: List[Dict[str, Any]] = []
        for cid in target_ids:
            content = self._content_pieces.get(cid)
            if not content:
                continue
            for key, value in content.performance.items():
                all_metrics[key].append(value)
            content_scores.append({
                "content_id": cid,
                "title": content.title,
                "seo_score": content.seo_score,
                "engagement_score": content.engagement_score,
                "total_performance": sum(content.performance.values()),
            })
        content_scores.sort(key=lambda x: x["total_performance"], reverse=True)
        summary_metrics: Dict[str, Dict[str, float]] = {}
        for key, values in all_metrics.items():
            summary_metrics[key] = {
                "total": round(sum(values), 2),
                "average": round(sum(values) / max(len(values), 1), 2),
                "min": round(min(values), 2) if values else 0,
                "max": round(max(values), 2) if values else 0,
            }
        return {
            "timeframe": timeframe.value,
            "total_content": len(target_ids),
            "summary_metrics": summary_metrics,
            "top_performers": content_scores[:10],
            "pipeline": self.get_content_pipeline(),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_content_gaps(
        self,
        strategy_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Identify content gaps based on strategy pillars and existing content.

        Analyzes the content library against strategy pillars and topic clusters
        to find missing or underrepresented content areas.
        """
        strategy = self._get_strategy(strategy_id) if strategy_id else None
        pillar_coverage: Dict[str, int] = defaultdict(int)
        existing_topics = {c.topic.lower() for c in self._content_pieces.values() if c.topic}
        gaps: List[Dict[str, Any]] = []
        if strategy:
            for pillar in strategy.content_pillars:
                pillar_lower = pillar.lower()
                matching = sum(1 for t in existing_topics if pillar_lower in t)
                pillar_coverage[pillar] = matching
                if matching < 3:
                    gaps.append({
                        "type": "pillar_underrepresented",
                        "pillar": pillar,
                        "existing_count": matching,
                        "recommendation": f"Create more content around '{pillar}' pillar.",
                        "priority": "high" if matching == 0 else "medium",
                    })
        all_clusters = list(self._topic_clusters.values())
        for cluster in all_clusters:
            covered = sum(
                1 for t in existing_topics
                if cluster.pillar_topic.lower() in t
            )
            total_needed = len(cluster.supporting_topics) + 1
            if covered < total_needed:
                gaps.append({
                    "type": "cluster_gap",
                    "cluster_id": cluster.cluster_id,
                    "pillar_topic": cluster.pillar_topic,
                    "covered": covered,
                    "needed": total_needed,
                    "missing_topics": [
                        t for t in cluster.supporting_topics
                        if t.lower() not in existing_topics
                    ],
                    "priority": "medium",
                })
        funnel_stages = [s.value for s in ContentStage]
        stage_coverage: Dict[str, int] = defaultdict(int)
        for content in self._content_pieces.values():
            stage_coverage[content.stage.value] += 1
        for stage in funnel_stages:
            if stage_coverage[stage] == 0:
                gaps.append({
                    "type": "funnel_gap",
                    "stage": stage,
                    "recommendation": f"No content targeting the {stage} stage.",
                    "priority": "high",
                })
        gaps.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 3))
        return gaps

    # ----- Internal Helpers -----

    def _get_strategy(self, strategy_id: str) -> ContentStrategy:
        strategy = self._strategies.get(strategy_id)
        if strategy is None:
            raise ValidationError("strategy_id", f"Strategy {strategy_id} not found.")
        return strategy

    def _get_calendar(self, calendar_id: str) -> "EditorialCalendar":
        calendar = self._calendars.get(calendar_id)
        if calendar is None:
            raise ValidationError("calendar_id", f"Calendar {calendar_id} not found.")
        return calendar

    def _get_content(self, content_id: str) -> ContentPiece:
        content = self._content_pieces.get(content_id)
        if content is None:
            raise ValidationError("content_id", f"Content piece {content_id} not found.")
        return content

    def _get_brief(self, brief_id: str) -> ContentBrief:
        brief = self._briefs.get(brief_id)
        if brief is None:
            raise ValidationError("brief_id", f"Brief {brief_id} not found.")
        return brief

    def _log_operation(self, operation: str, details: Dict[str, Any]) -> None:
        self._operation_log.append({
            "operation": operation,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def _generate_calendar_entries(
        self,
        calendar: "EditorialCalendar",
        strategy: ContentStrategy,
        months: int,
    ) -> None:
        current_date = calendar.start_date
        end_date = calendar.end_date
        author_pool = ["content-writer-1", "content-writer-2", "content-writer-3", "content-writer-4"]
        topic_index = 0
        while current_date < end_date:
            if current_date.weekday() < 5:
                blog_entry = CalendarEntry(
                    date=current_date,
                    content_type=ContentType.BLOG_POST,
                    channel=DistributionChannel.ORGANIC_SEARCH,
                    author=author_pool[topic_index % len(author_pool)],
                    topic=strategy.content_pillars[topic_index % len(strategy.content_pillars)] if strategy.content_pillars else "General",
                    status=ContentStatus.PLANNED,
                    priority=2,
                )
                calendar.entries.append(blog_entry)
            if current_date.weekday() in (1, 3):
                social_entry = CalendarEntry(
                    date=current_date,
                    content_type=ContentType.SOCIAL_POST,
                    channel=DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
                    author=author_pool[(topic_index + 1) % len(author_pool)],
                    topic=strategy.content_pillars[topic_index % len(strategy.content_pillars)] if strategy.content_pillars else "General",
                    status=ContentStatus.PLANNED,
                    priority=3,
                )
                calendar.entries.append(social_entry)
            if current_date.weekday() == 2:
                email_entry = CalendarEntry(
                    date=current_date,
                    content_type=ContentType.EMAIL_NEWSLETTER,
                    channel=DistributionChannel.EMAIL_MARKETING,
                    author=author_pool[0],
                    topic="Weekly Newsletter",
                    status=ContentStatus.PLANNED,
                    priority=2,
                )
                calendar.entries.append(email_entry)
            current_date += timedelta(days=1)
            topic_index += 1

    def _generate_outline(
        self,
        title: str,
        keyword: str,
        intent: KeywordIntent,
    ) -> List[str]:
        base_outline = [
            f"Introduction: Understanding {keyword}",
        ]
        if intent == KeywordIntent.INFORMATIONAL:
            base_outline.extend([
                f"What is {keyword}?",
                f"Why {keyword} matters",
                f"Key benefits of {keyword}",
                f"How to implement {keyword}",
                f"Best practices for {keyword}",
                f"Common mistakes to avoid",
                f"Tools and resources",
                f"Case studies and examples",
                f"Measuring success with {keyword}",
                f"Conclusion and next steps",
            ])
        elif intent == KeywordIntent.TRANSACTIONAL:
            base_outline.extend([
                f"Top {keyword} solutions compared",
                f"Key features to look for",
                f"Pricing and plans",
                f"Implementation guide",
                f"Customer testimonials",
                f"Getting started",
            ])
        elif intent == KeywordIntent.COMMERCIAL:
            base_outline.extend([
                f"What is {keyword}?",
                f"Top {keyword} options for 2026",
                f"Feature comparison",
                f"Pros and cons",
                f"Pricing comparison",
                f"Which is best for your needs",
                f"Frequently asked questions",
            ])
        else:
            base_outline.extend([
                f"Overview of {keyword}",
                f"Detailed analysis",
                f"Key insights",
                f"Conclusion",
            ])
        return base_outline

    def _determine_required_sections(
        self,
        content_type: ContentType,
        intent: KeywordIntent,
    ) -> List[str]:
        sections = [
            "Compelling headline",
            "Clear introduction with hook",
            "Structured body with subheadings",
            "Conclusion with CTA",
        ]
        if intent == KeywordIntent.INFORMATIONAL:
            sections.extend([
                "Definition/explanation section",
                "Step-by-step instructions",
                "Examples and use cases",
            ])
        elif intent == KeywordIntent.TRANSACTIONAL:
            sections.extend([
                "Product comparison table",
                "Pricing information",
                "Sign up / purchase CTA",
            ])
        if content_type == ContentType.BLOG_POST:
            sections.extend([
                "Meta title and description",
                "Internal links (minimum 3)",
                "Featured image with alt text",
            ])
        return sections

    def _analyze_content_seo(self, content: ContentPiece, report: SEOReport) -> float:
        score = 0.0
        if content.body_markdown:
            word_count = content.word_count
            if word_count >= self._config.seo.ideal_word_count:
                score += 20
            elif word_count >= self._config.seo.min_word_count:
                score += 12
            else:
                report.add_issue("high", "content", f"Word count too low: {word_count}")
        if content.keywords:
            primary = content.keywords[0].keyword.lower()
            title_present = primary in content.title.lower()
            meta_present = primary in content.meta_description.lower()
            body_present = primary in content.body_markdown.lower()
            if title_present:
                score += 10
            else:
                report.add_issue("high", "keyword", f"Primary keyword missing from title.")
            if meta_present:
                score += 8
            else:
                report.add_issue("medium", "keyword", f"Primary keyword missing from meta description.")
            if body_present:
                score += 10
                kw_count = content.body_markdown.lower().count(primary)
                density = kw_count / max(content.word_count, 1)
                if density > self._config.seo.max_keyword_density:
                    report.add_issue("medium", "keyword", f"Keyword density too high: {density:.3%}")
            else:
                report.add_issue("high", "keyword", f"Primary keyword missing from body.")
        if content.images:
            score += 5
        else:
            report.add_issue("medium", "content", "No images found in content.")
        if content.internal_links:
            if len(content.internal_links) >= self._config.seo.min_internal_links:
                score += 5
            else:
                report.add_issue("low", "links", f"Only {len(content.internal_links)} internal links.")
        else:
            report.add_issue("medium", "links", "No internal links found.")
        return min(40.0, score)

    def _analyze_on_page_seo(self, content: ContentPiece, report: SEOReport) -> float:
        score = 0.0
        if content.meta_title:
            if len(content.meta_title) <= self._config.seo.max_title_length:
                score += 12
            else:
                report.add_issue("medium", "on_page", f"Meta title too long: {len(content.meta_title)} chars")
        else:
            report.add_issue("high", "on_page", "Missing meta title.")
        if content.meta_description:
            if len(content.meta_description) <= self._config.seo.max_meta_description_length:
                score += 12
            else:
                report.add_issue("medium", "on_page", f"Meta description too long: {len(content.meta_description)} chars")
        else:
            report.add_issue("high", "on_page", "Missing meta description.")
        if content.canonical_url:
            score += 5
        else:
            report.add_issue("low", "on_page", "Missing canonical URL.")
        if content.slug:
            score += 3
        else:
            report.add_issue("low", "on_page", "Missing URL slug.")
        if content.schema_markup:
            score += 8
        else:
            report.add_issue("low", "on_page", "No schema markup found.")
        return min(40.0, score)

    def _analyze_technical_seo(self, content: ContentPiece, report: SEOReport) -> float:
        score = 20.0
        if content.og_image:
            score += 3
        else:
            report.add_issue("low", "technical", "Missing Open Graph image.")
        if not content.slug:
            report.add_issue("medium", "technical", "URL slug not set.")
            score -= 5
        if content.reading_time_minutes > 0:
            score += 2
        return min(30.0, max(0.0, score))

    def _analyze_off_page_seo(self, content: ContentPiece, report: SEOReport) -> float:
        score = 0.0
        if content.performance.get("backlinks", 0) > 0:
            score += 10
        if content.performance.get("domain_authority", 0) > 30:
            score += 5
        if content.channels:
            score += 5
        return min(20.0, score)

    def _analyze_competitor_seo(self, content: ContentPiece) -> Dict[str, Any]:
        return {
            "competitor_count": 0,
            "average_word_count": 0,
            "average_backlinks": 0,
            "common_keywords": [],
            "content_gaps": [],
        }

    def _build_utm_parameters(
        self,
        content: ContentPiece,
        channel: DistributionChannel,
    ) -> Dict[str, str]:
        return {
            "utm_source": channel.value,
            "utm_medium": self._get_channel_medium(channel),
            "utm_campaign": content.slug or content.content_id,
            "utm_content": content.content_id,
        }

    @staticmethod
    def _get_channel_medium(channel: DistributionChannel) -> str:
        if channel.value.startswith("social_media"):
            return "social"
        elif channel == DistributionChannel.EMAIL_MARKETING:
            return "email"
        elif channel.value.startswith("paid"):
            return "paid"
        elif channel == DistributionChannel.ORGANIC_SEARCH:
            return "organic"
        elif channel == DistributionChannel.CONTENT_SYNDICATION:
            return "syndication"
        return "referral"

    def _estimate_seo_improvement(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        priority_impact = {"high": 8, "medium": 4, "low": 2}
        total_impact = sum(
            priority_impact.get(r.get("priority", "low"), 0)
            for r in recommendations
        )
        return {
            "estimated_score_increase": min(30.0, total_impact),
            "high_priority_count": sum(1 for r in recommendations if r.get("priority") == "high"),
            "medium_priority_count": sum(1 for r in recommendations if r.get("priority") == "medium"),
            "low_priority_count": sum(1 for r in recommendations if r.get("priority") == "low"),
        }

    # ----- Status & Diagnostics -----

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status."""
        return {
            "agent": self._config.agent_name,
            "version": self._config.version,
            "strategies": len(self._strategies),
            "calendars": len(self._calendars),
            "content_pieces": len(self._content_pieces),
            "briefs": len(self._briefs),
            "seo_reports": len(self._seo_reports),
            "distribution_results": len(self._distribution_results),
            "topic_clusters": len(self._topic_clusters),
            "performance_snapshots": sum(len(v) for v in self._performance_snapshots.values()),
            "operations_logged": len(self._operation_log),
            "cache_size": self._cache.size() if self._cache else 0,
            "uptime": "active",
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
            "strategies": [s.to_dict() for s in self._strategies.values()],
            "content_pieces": [c.to_dict() for c in self._content_pieces.values()],
            "briefs": [b.to_dict() for b in self._briefs.values()],
            "seo_reports": [r.to_dict() for r in self._seo_reports.values()],
            "topic_clusters": [c.to_dict() for c in self._topic_clusters.values()],
            "status": self.get_status(),
        }
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        return str(data)


# ---------------------------------------------------------------------------
# Editorial Calendar (companion class)
# ---------------------------------------------------------------------------


class EditorialCalendar:
    """Editorial calendar for content planning and scheduling.

    Manages a collection of calendar entries organized by date,
    supporting multiple view modes and entry management.
    """

    def __init__(
        self,
        name: str = "",
        strategy_id: str = "",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> None:
        self.calendar_id: str = str(uuid.uuid4())[:8]
        self.name: str = name
        self.strategy_id: str = strategy_id
        self.start_date: datetime = start_date or datetime.utcnow()
        self.end_date: datetime = end_date or (self.start_date + timedelta(days=90))
        self.entries: List[CalendarEntry] = []
        self.created_at: datetime = datetime.utcnow()
        self.metadata: Dict[str, Any] = {}

    def add_entry(self, entry: CalendarEntry) -> None:
        """Add an entry to the calendar."""
        self.entries.append(entry)

    def get_entry(self, entry_id: str) -> Optional[CalendarEntry]:
        """Get an entry by ID."""
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return entry
        return None

    def remove_entry(self, entry_id: str) -> bool:
        """Remove an entry by ID."""
        for i, entry in enumerate(self.entries):
            if entry.entry_id == entry_id:
                self.entries.pop(i)
                return True
        return False

    def get_entries_by_date(self, date: datetime) -> List[CalendarEntry]:
        """Get all entries for a specific date."""
        return [
            e for e in self.entries
            if e.date.date() == date.date()
        ]

    def get_entries_by_status(self, status: ContentStatus) -> List[CalendarEntry]:
        """Get all entries with a specific status."""
        return [e for e in self.entries if e.status == status]

    def get_entries_by_type(self, content_type: ContentType) -> List[CalendarEntry]:
        """Get all entries of a specific content type."""
        return [e for e in self.entries if e.content_type == content_type]

    def get_entries_by_channel(self, channel: DistributionChannel) -> List[CalendarEntry]:
        """Get all entries for a specific channel."""
        return [e for e in self.entries if e.channel == channel]

    def get_entries_by_author(self, author: str) -> List[CalendarEntry]:
        """Get all entries by a specific author."""
        return [e for e in self.entries if e.author == author]

    def get_view(
        self,
        view: CalendarView,
        date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get calendar entries in the specified view format."""
        if view == CalendarView.DAILY:
            target_date = date or datetime.utcnow()
            entries = self.get_entries_by_date(target_date)
            return {
                "view": "daily",
                "date": target_date.date().isoformat(),
                "entries": [e.to_dict() for e in entries],
                "total": len(entries),
            }
        elif view == CalendarView.WEEKLY:
            target = date or datetime.utcnow()
            week_start = target - timedelta(days=target.weekday())
            week_end = week_start + timedelta(days=6)
            entries = [
                e for e in self.entries
                if week_start.date() <= e.date.date() <= week_end.date()
            ]
            return {
                "view": "weekly",
                "week_start": week_start.date().isoformat(),
                "week_end": week_end.date().isoformat(),
                "entries": [e.to_dict() for e in entries],
                "total": len(entries),
            }
        elif view == CalendarView.MONTHLY:
            target = date or datetime.utcnow()
            entries = [
                e for e in self.entries
                if e.date.month == target.month and e.date.year == target.year
            ]
            return {
                "view": "monthly",
                "month": target.strftime("%Y-%m"),
                "entries": [e.to_dict() for e in entries],
                "total": len(entries),
            }
        elif view == CalendarView.CONTENT_TYPE:
            grouped: Dict[str, List[CalendarEntry]] = defaultdict(list)
            for entry in self.entries:
                grouped[entry.content_type.value].append(entry)
            return {
                "view": "content_type",
                "groups": {
                    k: {"entries": [e.to_dict() for e in v], "count": len(v)}
                    for k, v in grouped.items()
                },
                "total": len(self.entries),
            }
        elif view == CalendarView.CHANNEL:
            grouped: Dict[str, List[CalendarEntry]] = defaultdict(list)
            for entry in self.entries:
                grouped[entry.channel.value].append(entry)
            return {
                "view": "channel",
                "groups": {
                    k: {"entries": [e.to_dict() for e in v], "count": len(v)}
                    for k, v in grouped.items()
                },
                "total": len(self.entries),
            }
        elif view == CalendarView.AUTHOR:
            grouped: Dict[str, List[CalendarEntry]] = defaultdict(list)
            for entry in self.entries:
                grouped[entry.author].append(entry)
            return {
                "view": "author",
                "groups": {
                    k: {"entries": [e.to_dict() for e in v], "count": len(v)}
                    for k, v in grouped.items()
                },
                "total": len(self.entries),
            }
        return {
            "view": view.value,
            "entries": [e.to_dict() for e in self.entries],
            "total": len(self.entries),
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the calendar."""
        type_counts: Dict[str, int] = defaultdict(int)
        status_counts: Dict[str, int] = defaultdict(int)
        channel_counts: Dict[str, int] = defaultdict(int)
        for entry in self.entries:
            type_counts[entry.content_type.value] += 1
            status_counts[entry.status.value] += 1
            channel_counts[entry.channel.value] += 1
        return {
            "calendar_id": self.calendar_id,
            "name": self.name,
            "strategy_id": self.strategy_id,
            "period": f"{self.start_date.date()} to {self.end_date.date()}",
            "total_entries": len(self.entries),
            "by_type": dict(type_counts),
            "by_status": dict(status_counts),
            "by_channel": dict(channel_counts),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "calendar_id": self.calendar_id,
            "name": self.name,
            "strategy_id": self.strategy_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "entries": [e.to_dict() for e in self.entries],
            "total_entries": len(self.entries),
            "created_at": self.created_at.isoformat(),
        }


# ---------------------------------------------------------------------------
# CLI Demo
# ---------------------------------------------------------------------------


def main() -> None:
    """Demonstrate Content Marketing Agent capabilities."""
    print("=" * 70)
    print("Content Marketing Agent v3.0.0 - Comprehensive Demo")
    print("=" * 70)
    config = Config()
    agent = ContentMarketingAgent(config=config)
    print("\n--- Creating Content Strategy ---")
    strategy = agent.create_content_strategy(
        name="SaaS Growth Strategy 2026",
        target_market="B2B SaaS startups",
        pillars=[
            "product-led growth",
            "developer experience",
            "customer success stories",
            "industry thought leadership",
        ],
        goals=[ContentGoal.AWARENESS, ContentGoal.LEAD_GENERATION, ContentGoal.THOUGHT_LEADERSHIP],
        audiences=[AudienceSegment.DEVELOPER, AudienceSegment.MANAGER, AudienceSegment.ENTERPRISE],
        voice=ContentTone.AUTHORITATIVE,
        budget=120000.0,
    )
    print(f"Strategy created: {strategy.name} ({strategy.strategy_id})")
    print(f"Content pillars: {strategy.content_pillars}")
    print(f"Content mix: {strategy.get_content_mix_summary()}")
    print("\n--- Creating Editorial Calendar ---")
    calendar = agent.create_editorial_calendar(
        strategy_id=strategy.strategy_id,
        months=3,
    )
    print(f"Calendar created: {calendar.name} ({calendar.calendar_id})")
    print(f"Total entries: {len(calendar.entries)}")
    summary = calendar.get_summary()
    print(f"By type: {summary['by_type']}")
    print("\n--- Keyword Research ---")
    keywords = agent.generate_keyword_research(seed_keyword="conversion rate optimization", count=10)
    print(f"Generated {len(keywords)} keywords")
    for kw in keywords[:5]:
        print(f"  - {kw.keyword} (vol: {kw.search_volume}, diff: {kw.keyword_difficulty}, intent: {kw.intent.value})")
    print("\n--- Creating Content Brief ---")
    brief = agent.create_content_brief(
        title="The Complete Guide to Conversion Rate Optimization in 2026",
        primary_keyword="conversion rate optimization",
        secondary_keywords=["CRO", "conversion optimization", "landing page optimization"],
        target_word_count=2500,
        audience="Marketing managers at B2B SaaS companies",
        intent=KeywordIntent.INFORMATIONAL,
        goals=[ContentGoal.EDUCATION, ContentGoal.LEAD_GENERATION],
        outline=[
            "What is CRO?",
            "Why CRO matters for SaaS",
            "The CRO process step by step",
            "Key metrics to track",
            "Tools and frameworks",
            "Case studies",
            "Getting started",
        ],
    )
    print(f"Brief created: {brief.title} ({brief.brief_id})")
    print(f"Outline sections: {len(brief.outline)}")
    print("\n--- Topic Cluster ---")
    cluster = agent.create_topic_cluster(
        pillar_topic="Conversion Rate Optimization",
        supporting_topics=[
            "A/B testing best practices",
            "Landing page design",
            "Call-to-action optimization",
            "User behavior analytics",
            "Heatmap analysis",
            "Form optimization",
            "Checkout flow optimization",
        ],
        keywords=keywords[:5],
    )
    print(f"Cluster created: {cluster.pillar_topic} ({cluster.cluster_id})")
    print(f"Supporting topics: {len(cluster.supporting_topics)}")
    print("\n--- Creating Content Piece ---")
    content = agent.create_content_piece(
        title="The Complete Guide to Conversion Rate Optimization in 2026",
        content_type=ContentType.BLOG_POST,
        author="content-writer-1",
        topic="CRO",
        keywords=keywords[:3],
    )
    print(f"Content created: {content.title} ({content.content_id})")
    print(f"Slug: {content.slug}")
    print(f"Status: {content.status.value}")
    print("\n--- SEO Analysis ---")
    seo_report = agent.analyze_seo(content.content_id)
    print(f"SEO Report: overall={seo_report.overall_score:.1f}, issues={len(seo_report.issues)}")
    for issue in seo_report.issues[:3]:
        print(f"  [{issue['severity']}] {issue['category']}: {issue['message']}")
    print("\n--- SEO Optimization ---")
    optimization = agent.optimize_seo_content(
        content_id=content.content_id,
        target_keyword="conversion rate optimization",
    )
    print(f"Estimated improvement: +{optimization['estimated_improvement']['estimated_score_increase']:.1f} points")
    print(f"Recommendations: {len(optimization['recommendations'])}")
    print("\n--- Distributing Content ---")
    dist_results = agent.distribute_content(
        content_id=content.content_id,
        channels=[
            DistributionChannel.ORGANIC_SEARCH,
            DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
            DistributionChannel.EMAIL_MARKETING,
        ],
    )
    for result in dist_results:
        print(f"  {result.channel.value}: {result.status}")
    print("\n--- Recording Performance ---")
    agent.record_performance(
        content_id=content.content_id,
        metrics={
            "pageviews": 1250,
            "unique_visitors": 980,
            "bounce_rate": 0.42,
            "time_on_page": 345,
            "social_shares": 67,
            "backlinks": 12,
            "conversion_rate": 0.035,
        },
        channel_breakdown={
            "organic_search": {"pageviews": 800, "conversions": 35},
            "social_media": {"pageviews": 300, "conversions": 8},
            "email": {"pageviews": 150, "conversions": 12},
        },
    )
    print("Performance recorded successfully")
    print("\n--- Content Analytics ---")
    analytics = agent.get_content_analytics(timeframe=AnalyticsTimeframe.LAST_30_DAYS)
    print(f"Content count: {analytics['content_count']}")
    print(f"Pipeline: {analytics['pipeline_status']}")
    print("\n--- Content Gaps ---")
    gaps = agent.get_content_gaps(strategy_id=strategy.strategy_id)
    print(f"Found {len(gaps)} content gaps")
    for gap in gaps[:3]:
        print(f"  [{gap['priority']}] {gap['type']}: {gap.get('recommendation', 'N/A')}")
    print("\n--- Posting Times ---")
    times = agent.get_optimal_posting_times(
        channel=DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
        audience=AudienceSegment.MANAGER,
    )
    print(f"LinkedIn best days: {times['schedule']['best_days']}")
    print(f"LinkedIn best times: {times['schedule']['best_times']}")
    print("\n--- Content Pipeline ---")
    pipeline = agent.get_content_pipeline()
    print(f"Pipeline: {pipeline}")
    print("\n--- Repurposing ---")
    repurposed = agent.repurpose_content(
        content_id=content.content_id,
        target_formats=[
            ContentFormat.VIDEO_TUTORIAL,
            ContentFormat.INFOGRAPHIC_DATA,
            ContentFormat.SOCIAL_CAROUSEL,
        ],
    )
    print(f"Created {len(repurposed)} repurposed content briefs")
    for brief in repurposed:
        print(f"  - {brief.title}")
    print("\n--- Agent Status ---")
    status = agent.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
