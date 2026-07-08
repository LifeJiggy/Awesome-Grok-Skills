"""
Social Media Agent - Comprehensive Social Media Management and Analytics.

Capabilities include content scheduling, community management, engagement tracking,
audience analytics, influencer identification, reputation monitoring, and campaign
orchestration across multiple platforms.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import secrets
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Platform(Enum):
    """Supported social media platforms."""
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    GITHUB = "github"
    REDDIT = "reddit"
    DISCORD = "discord"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    THREADS = "threads"


class ContentType(Enum):
    """Types of social media content."""
    POST = "post"
    ARTICLE = "article"
    VIDEO = "video"
    IMAGE = "image"
    STORY = "story"
    THREAD = "thread"
    POLL = "poll"
    REEL = "reel"
    CAROUSEL = "carousel"
    LIVE = "live"


class EngagementType(Enum):
    """Types of user engagement."""
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    RETWEET = "retweet"
    FOLLOW = "follow"
    MENTION = "mention"
    DM = "dm"
    BOOKMARK = "bookmark"
    CLICK = "click"
    VIEW = "view"


class SentimentType(Enum):
    """Sentiment classification."""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class ContentStatus(Enum):
    """Content lifecycle status."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    FAILED = "failed"


class CampaignStatus(Enum):
    """Campaign lifecycle status."""
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InfluencerTier(Enum):
    """Influencer classification by follower count."""
    NANO = "nano"           # 1K-10K
    MICRO = "micro"         # 10K-100K
    MACRO = "macro"         # 100K-1M
    MEGA = "mega"           # 1M+


class ReputationAlertLevel(Enum):
    """Reputation monitoring alert levels."""
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SocialPost:
    """Social media post with full metadata."""
    id: str
    platform: Platform
    content: str
    content_type: ContentType
    created_at: datetime
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]
    metrics: Dict[str, int]
    hashtags: List[str]
    mentions: List[str]
    status: ContentStatus
    media_urls: List[str]
    author_id: str
    engagement_rate: float = 0.0
    reach: int = 0
    impressions: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "platform": self.platform.value,
            "content": self.content[:100],
            "type": self.content_type.value,
            "status": self.status.value,
            "metrics": self.metrics,
            "engagement_rate": self.engagement_rate,
        }


@dataclass
class Engagement:
    """User engagement record."""
    id: str
    post_id: str
    user_id: str
    username: str
    engagement_type: EngagementType
    timestamp: datetime
    content: str
    sentiment: SentimentType
    platform: Platform
    replied: bool = False


@dataclass
class AudienceInsight:
    """Audience demographics and behavior."""
    platform: Platform
    total_followers: int
    follower_growth_rate: float
    demographics: Dict[str, float]
    active_hours: List[int]
    top_locations: List[str]
    engagement_rate: float
    avg_reach_per_post: int
    audience_interests: List[str]
    last_updated: datetime


@dataclass
class Campaign:
    """Social media campaign."""
    id: str
    name: str
    description: str
    platforms: List[Platform]
    status: CampaignStatus
    start_date: datetime
    end_date: Optional[datetime]
    budget: float
    target_audience: Dict[str, Any]
    kpis: Dict[str, float]
    posts: List[str]
    metrics: Dict[str, Any]
    created_at: datetime


@dataclass
class InfluencerProfile:
    """Influencer collaboration profile."""
    id: str
    username: str
    platform: Platform
    tier: InfluencerTier
    followers: int
    engagement_rate: float
    niche: str
    collaboration_cost: float
    past_collaborations: int
    audience_overlap: float
    relevance_score: float


@dataclass
class ReputationEvent:
    """Reputation monitoring event."""
    id: str
    platform: Platform
    event_type: str
    sentiment: SentimentType
    content: str
    source: str
    timestamp: datetime
    alert_level: ReputationAlertLevel
    resolved: bool = False


@dataclass
class ContentCalendarEntry:
    """Calendar entry for content scheduling."""
    id: str
    post_id: str
    platform: Platform
    scheduled_time: datetime
    content_type: ContentType
    status: ContentStatus
    campaign_id: Optional[str]


# ---------------------------------------------------------------------------
# Content Manager
# ---------------------------------------------------------------------------

class ContentManager:
    """Manages content creation, scheduling, and publishing."""

    def __init__(self) -> None:
        self.posts: Dict[str, SocialPost] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.calendar: Dict[str, List[ContentCalendarEntry]] = defaultdict(list)
        self._content_rules: Dict[Platform, Dict[str, Any]] = self._init_platform_rules()
        logger.info("ContentManager initialized")

    def _init_platform_rules(self) -> Dict[Platform, Dict[str, Any]]:
        """Platform-specific content rules."""
        return {
            Platform.TWITTER: {"max_length": 280, "max_hashtags": 5, "supports_threads": True},
            Platform.LINKEDIN: {"max_length": 3000, "max_hashtags": 5, "supports_articles": True},
            Platform.INSTAGRAM: {"max_length": 2200, "max_hashtags": 30, "supports_reels": True},
            Platform.FACEBOOK: {"max_length": 63206, "max_hashtags": 10, "supports_groups": True},
            Platform.GITHUB: {"max_length": 65536, "max_hashtags": 0, "supports_wiki": True},
            Platform.YOUTUBE: {"max_length": 5000, "max_hashtags": 15, "supports_shorts": True},
            Platform.TIKTOK: {"max_length": 2200, "max_hashtags": 10, "supports_duet": True},
        }

    def create_post(self, platform: Platform, content: str,
                    content_type: ContentType = ContentType.POST,
                    scheduled_at: Optional[datetime] = None,
                    hashtags: Optional[List[str]] = None,
                    mentions: Optional[List[str]] = None,
                    media_urls: Optional[List[str]] = None,
                    author_id: str = "system") -> SocialPost:
        """Create a new social media post."""
        rules = self._content_rules.get(platform, {})
        max_len = rules.get("max_length", 2000)

        if len(content) > max_len:
            logger.warning("Content truncated from %d to %d chars for %s",
                           len(content), max_len, platform.value)
            content = content[:max_len]

        post = SocialPost(
            id=f"post_{uuid.uuid4().hex[:8]}",
            platform=platform,
            content=content,
            content_type=content_type,
            created_at=datetime.now(),
            scheduled_at=scheduled_at,
            published_at=None,
            metrics={"likes": 0, "comments": 0, "shares": 0, "views": 0},
            hashtags=hashtags or [],
            mentions=mentions or [],
            status=ContentStatus.SCHEDULED if scheduled_at else ContentStatus.DRAFT,
            media_urls=media_urls or [],
            author_id=author_id,
        )
        self.posts[post.id] = post

        if scheduled_at:
            cal_entry = ContentCalendarEntry(
                id=f"cal_{uuid.uuid4().hex[:8]}",
                post_id=post.id,
                platform=platform,
                scheduled_time=scheduled_at,
                content_type=content_type,
                status=post.status,
                campaign_id=None,
            )
            date_key = scheduled_at.strftime("%Y-%m-%d")
            self.calendar[date_key].append(cal_entry)

        logger.info("Post %s created for %s", post.id, platform.value)
        return post

    def create_thread(self, platform: Platform, messages: List[str],
                      hashtags: Optional[List[str]] = None) -> List[SocialPost]:
        """Create a thread (series of connected posts)."""
        posts: List[SocialPost] = []
        for idx, msg in enumerate(messages):
            numbering = f"({idx + 1}/{len(messages)}) "
            post = self.create_post(
                platform=platform,
                content=numbering + msg,
                content_type=ContentType.THREAD,
                hashtags=hashtags,
            )
            posts.append(post)
        return posts

    def add_template(self, name: str, template: str,
                     platform: Optional[Platform] = None,
                     variables: Optional[List[str]] = None) -> None:
        """Register a reusable content template."""
        self.templates[name] = {
            "template": template,
            "platform": platform,
            "variables": variables or self._extract_variables(template),
            "created_at": datetime.now(),
        }

    def _extract_variables(self, template: str) -> List[str]:
        """Extract template variables from {{var}} syntax."""
        return list(set(re.findall(r"\{\{(\w+)\}\}", template)))

    def render_template(self, template_name: str,
                        variables: Dict[str, str]) -> Optional[str]:
        """Render a template with provided variables."""
        tmpl = self.templates.get(template_name)
        if not tmpl:
            logger.warning("Template %s not found", template_name)
            return None
        content = tmpl["template"]
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", value)
        return content

    def get_calendar(self, start: datetime, end: datetime,
                     platform: Optional[Platform] = None) -> Dict[str, List[ContentCalendarEntry]]:
        """Get content calendar for a date range."""
        result: Dict[str, List[ContentCalendarEntry]] = defaultdict(list)
        for date_key, entries in self.calendar.items():
            dt = datetime.strptime(date_key, "%Y-%m-%d")
            if start.date() <= dt.date() <= end.date():
                for entry in entries:
                    if platform is None or entry.platform == platform:
                        result[date_key].append(entry)
        return dict(result)

    def get_posts_by_status(self, status: ContentStatus) -> List[SocialPost]:
        """Filter posts by status."""
        return [p for p in self.posts.values() if p.status == status]

    def publish_post(self, post_id: str) -> Dict[str, Any]:
        """Mark a post as published."""
        post = self.posts.get(post_id)
        if not post:
            return {"error": f"Post {post_id} not found"}
        post.status = ContentStatus.PUBLISHED
        post.published_at = datetime.now()
        return {"post_id": post_id, "status": "published", "platform": post.platform.value}


# ---------------------------------------------------------------------------
# Engagement Manager
# ---------------------------------------------------------------------------

class EngagementManager:
    """Tracks and manages audience engagement."""

    def __init__(self) -> None:
        self.engagements: List[Engagement] = []
        self.responses: Dict[str, str] = {}
        self.automations: List[Dict[str, Any]] = []
        self._sentiment_lexicon = self._build_lexicon()
        logger.info("EngagementManager initialized")

    def _build_lexicon(self) -> Dict[str, List[str]]:
        """Build sentiment analysis lexicon."""
        return {
            "positive": ["great", "amazing", "love", "awesome", "thanks", "helpful",
                         "excellent", "fantastic", "brilliant", "perfect", "best",
                         "wonderful", "outstanding", "superb", "impressive"],
            "negative": ["bad", "hate", "terrible", "awful", "worst", "disappointed",
                         "horrible", "poor", "broken", "useless", "frustrating",
                         "annoying", "slow", "crash", "bug"],
        }

    def track_engagement(self, post_id: str, user_id: str, username: str,
                         engagement_type: EngagementType,
                         content: str = "",
                         platform: Platform = Platform.TWITTER) -> Engagement:
        """Record a user engagement event."""
        engagement = Engagement(
            id=f"eng_{uuid.uuid4().hex[:8]}",
            post_id=post_id,
            user_id=user_id,
            username=username,
            engagement_type=engagement_type,
            timestamp=datetime.now(),
            content=content,
            sentiment=self._analyze_sentiment(content),
            platform=platform,
        )
        self.engagements.append(engagement)
        return engagement

    def _analyze_sentiment(self, text: str) -> SentimentType:
        """Classify text sentiment using lexicon-based approach."""
        if not text:
            return SentimentType.NEUTRAL

        text_lower = text.lower()
        pos = sum(1 for w in self._sentiment_lexicon["positive"] if w in text_lower)
        neg = sum(1 for w in self._sentiment_lexicon["negative"] if w in text_lower)

        if pos >= 3:
            return SentimentType.VERY_POSITIVE
        elif pos > neg:
            return SentimentType.POSITIVE
        elif neg >= 3:
            return SentimentType.VERY_NEGATIVE
        elif neg > pos:
            return SentimentType.NEGATIVE
        return SentimentType.NEUTRAL

    def respond_to_engagement(self, engagement_id: str, response: str) -> Dict[str, Any]:
        """Record a response to an engagement."""
        for eng in self.engagements:
            if eng.id == engagement_id:
                eng.replied = True
                self.responses[engagement_id] = response
                return {"engagement_id": engagement_id, "responded": True}
        return {"error": f"Engagement {engagement_id} not found"}

    def create_automation(self, trigger: str, action: str,
                          conditions: Optional[Dict[str, Any]] = None,
                          name: str = "") -> Dict[str, Any]:
        """Create an engagement automation rule."""
        automation = {
            "id": f"auto_{uuid.uuid4().hex[:8]}",
            "name": name or f"Auto: {trigger} -> {action}",
            "trigger": trigger,
            "action": action,
            "conditions": conditions or {},
            "enabled": True,
            "created_at": datetime.now().isoformat(),
        }
        self.automations.append(automation)
        return automation

    def get_engagement_metrics(self, post_id: str) -> Dict[str, Any]:
        """Calculate engagement metrics for a specific post."""
        post_engs = [e for e in self.engagements if e.post_id == post_id]
        by_type = defaultdict(int)
        by_sentiment = defaultdict(int)
        for eng in post_engs:
            by_type[eng.engagement_type.value] += 1
            by_sentiment[eng.sentiment.value] += 1

        total = len(post_engs)
        return {
            "total_engagements": total,
            "by_type": dict(by_type),
            "by_sentiment": dict(by_sentiment),
            "response_rate": sum(1 for e in post_engs if e.replied) / max(total, 1),
        }

    def get_top_engagers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Identify most active engagers."""
        user_counts: Dict[str, int] = defaultdict(int)
        for eng in self.engagements:
            user_counts[eng.username] += 1

        sorted_users = sorted(user_counts.items(), key=lambda x: -x[1])[:limit]
        return [{"username": u, "engagements": c} for u, c in sorted_users]

    def get_sentiment_trend(self, days: int = 30) -> List[Dict[str, Any]]:
        """Calculate daily sentiment trend."""
        cutoff = datetime.now() - timedelta(days=days)
        daily: Dict[str, Dict[str, int]] = defaultdict(lambda: {"positive": 0, "negative": 0, "neutral": 0})

        for eng in self.engagements:
            if eng.timestamp >= cutoff:
                date_key = eng.timestamp.strftime("%Y-%m-%d")
                if eng.sentiment in (SentimentType.POSITIVE, SentimentType.VERY_POSITIVE):
                    daily[date_key]["positive"] += 1
                elif eng.sentiment in (SentimentType.NEGATIVE, SentimentType.VERY_NEGATIVE):
                    daily[date_key]["negative"] += 1
                else:
                    daily[date_key]["neutral"] += 1

        return [{"date": k, **v} for k, v in sorted(daily.items())]


# ---------------------------------------------------------------------------
# Audience Analyzer
# ---------------------------------------------------------------------------

class AudienceAnalyzer:
    """Audience demographics, behavior, and growth analysis."""

    def __init__(self) -> None:
        self.audiences: Dict[Platform, AudienceInsight] = {}
        self.follower_history: List[Dict[str, Any]] = []

    def add_audience_data(self, platform: Platform, data: Dict[str, Any]) -> AudienceInsight:
        """Ingest audience analytics data."""
        insight = AudienceInsight(
            platform=platform,
            total_followers=data.get("followers", 0),
            follower_growth_rate=data.get("growth_rate", 0.0),
            demographics=data.get("demographics", {}),
            active_hours=data.get("active_hours", []),
            top_locations=data.get("locations", []),
            engagement_rate=data.get("engagement_rate", 0.0),
            avg_reach_per_post=data.get("avg_reach", 0),
            audience_interests=data.get("interests", []),
            last_updated=datetime.now(),
        )
        self.audiences[platform] = insight
        self.follower_history.append({
            "platform": platform.value,
            "followers": insight.total_followers,
            "timestamp": datetime.now().isoformat(),
        })
        return insight

    def get_optimal_posting_times(self, platform: Platform, count: int = 3) -> List[Dict[str, Any]]:
        """Recommend best posting times based on audience activity."""
        insight = self.audiences.get(platform)
        if not insight or not insight.active_hours:
            return [{"hour": h, "score": 0} for h in [9, 12, 18]]

        hour_scores: Dict[int, int] = defaultdict(int)
        for h in insight.active_hours:
            hour_scores[h] += 1

        sorted_hours = sorted(hour_scores.items(), key=lambda x: -x[1])[:count]
        return [{"hour": h, "score": s} for h, s in sorted_hours]

    def analyze_cross_platform_overlap(self) -> Dict[str, float]:
        """Estimate audience overlap between platforms."""
        platforms = list(self.audiences.keys())
        overlap: Dict[str, float] = {}
        for i, p1 in enumerate(platforms):
            for p2 in platforms[i + 1:]:
                key = f"{p1.value}_{p2.value}"
                overlap[key] = 0.25
        return overlap

    def calculate_total_reach(self) -> Dict[str, Any]:
        """Calculate aggregate reach across all platforms."""
        total_followers = sum(a.total_followers for a in self.audiences.values())
        avg_engagement = (
            sum(a.engagement_rate for a in self.audiences.values())
            / max(len(self.audiences), 1)
        )
        return {
            "total_followers": total_followers,
            "platforms": len(self.audiences),
            "avg_engagement_rate": round(avg_engagement, 4),
            "by_platform": {
                p.value: {"followers": a.total_followers, "engagement": a.engagement_rate}
                for p, a in self.audiences.items()
            },
        }

    def get_growth_recommendations(self) -> List[str]:
        """Generate audience growth recommendations."""
        recs: List[str] = []
        for platform, insight in self.audiences.items():
            if insight.engagement_rate < 0.02:
                recs.append(f"{platform.value}: Engagement rate below 2% - focus on interactive content")
            if insight.follower_growth_rate < 0.01:
                recs.append(f"{platform.value}: Slow growth - increase posting frequency")
        recs.extend([
            "Cross-promote content across all active platforms",
            "Collaborate with creators in adjacent niches",
            "Leverage trending topics for organic discovery",
            "Run targeted follower acquisition campaigns",
        ])
        return recs


# ---------------------------------------------------------------------------
# Social Analytics
# ---------------------------------------------------------------------------

class SocialAnalytics:
    """Performance analytics across all social channels."""

    def __init__(self, content: ContentManager, engagement: EngagementManager,
                 audience: AudienceAnalyzer) -> None:
        self.content = content
        self.engagement = engagement
        self.audience = audience

    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate key performance indicators."""
        total_posts = len(self.content.posts)
        total_engagements = len(self.engagement.engagements)
        total_reach = sum(p.metrics.get("views", 0) for p in self.content.posts.values())
        total_followers = sum(a.total_followers for a in self.audience.audiences.values())

        published = [p for p in self.content.posts.values() if p.status == ContentStatus.PUBLISHED]
        avg_engagement_rate = (
            sum(p.engagement_rate for p in published) / max(len(published), 1)
        )

        return {
            "total_posts": total_posts,
            "published_posts": len(published),
            "total_engagements": total_engagements,
            "total_reach": total_reach,
            "total_followers": total_followers,
            "avg_engagement_rate": round(avg_engagement_rate, 4),
            "engagement_per_post": round(total_engagements / max(total_posts, 1), 2),
        }

    def get_top_performing_posts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Identify top performing posts by engagement."""
        ranked = sorted(
            self.content.posts.values(),
            key=lambda p: sum(p.metrics.values()),
            reverse=True,
        )[:limit]
        return [
            {
                "id": p.id,
                "platform": p.platform.value,
                "content_preview": p.content[:80],
                "total_engagement": sum(p.metrics.values()),
                "metrics": p.metrics,
            }
            for p in ranked
        ]

    def get_platform_breakdown(self) -> Dict[str, Dict[str, Any]]:
        """Performance breakdown by platform."""
        breakdown: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"posts": 0, "engagement": 0, "reach": 0})
        for post in self.content.posts.values():
            key = post.platform.value
            breakdown[key]["posts"] += 1
            breakdown[key]["engagement"] += sum(post.metrics.values())
            breakdown[key]["reach"] += post.metrics.get("views", 0)
        return dict(breakdown)

    def generate_report(self, start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        kpis = self.calculate_kpis()
        top_posts = self.get_top_performing_posts()
        platform_data = self.get_platform_breakdown()

        return {
            "period": {
                "start": (start_date or datetime.now() - timedelta(days=30)).isoformat(),
                "end": (end_date or datetime.now()).isoformat(),
            },
            "kpis": kpis,
            "top_posts": top_posts,
            "platform_breakdown": platform_data,
            "recommendations": self._generate_recommendations(kpis),
        }

    def _generate_recommendations(self, kpis: Dict[str, Any]) -> List[str]:
        """Generate data-driven optimization recommendations."""
        recs: List[str] = []
        if kpis.get("avg_engagement_rate", 0) < 0.03:
            recs.append("Engagement rate is low - test more interactive content formats")
        if kpis.get("total_reach", 0) < 10000:
            recs.append("Reach is limited - consider paid amplification or influencer partnerships")
        if kpis.get("engagement_per_post", 0) < 5:
            recs.append("Per-post engagement is low - review content quality and timing")
        recs.extend([
            "Analyze top-performing posts for replicable patterns",
            "A/B test content formats and posting times",
            "Invest in video content for higher engagement",
        ])
        return recs


# ---------------------------------------------------------------------------
# Influencer Manager
# ---------------------------------------------------------------------------

class InfluencerManager:
    """Manages influencer discovery, outreach, and collaboration tracking."""

    def __init__(self) -> None:
        self.profiles: Dict[str, InfluencerProfile] = {}
        self.collaborations: List[Dict[str, Any]] = []

    def add_influencer(self, username: str, platform: Platform,
                       followers: int, engagement_rate: float,
                       niche: str, cost: float = 0.0) -> InfluencerProfile:
        """Register an influencer profile."""
        tier = self._classify_tier(followers)
        profile = InfluencerProfile(
            id=f"inf_{uuid.uuid4().hex[:8]}",
            username=username,
            platform=platform,
            tier=tier,
            followers=followers,
            engagement_rate=engagement_rate,
            niche=niche,
            collaboration_cost=cost,
            past_collaborations=0,
            audience_overlap=0.0,
            relevance_score=self._calc_relevance(followers, engagement_rate),
        )
        self.profiles[profile.id] = profile
        return profile

    def _classify_tier(self, followers: int) -> InfluencerTier:
        """Classify influencer by follower count."""
        if followers >= 1_000_000:
            return InfluencerTier.MEGA
        elif followers >= 100_000:
            return InfluencerTier.MACRO
        elif followers >= 10_000:
            return InfluencerTier.MICRO
        return InfluencerTier.NANO

    def _calc_relevance(self, followers: int, engagement: float) -> float:
        """Calculate relevance score (engagement matters more than size)."""
        eng_score = min(engagement * 10, 5.0)
        size_score = min(followers / 1_000_000, 5.0)
        return round((eng_score * 0.6 + size_score * 0.4), 2)

    def find_top_influencers(self, niche: str, limit: int = 5) -> List[InfluencerProfile]:
        """Find top influencers by niche and relevance."""
        matching = [p for p in self.profiles.values() if niche.lower() in p.niche.lower()]
        ranked = sorted(matching, key=lambda p: -p.relevance_score)[:limit]
        return ranked

    def record_collaboration(self, influencer_id: str, campaign_id: str,
                             content_posts: int, total_reach: int,
                             cost: float) -> Dict[str, Any]:
        """Record a completed collaboration."""
        collab = {
            "id": f"collab_{uuid.uuid4().hex[:8]}",
            "influencer_id": influencer_id,
            "campaign_id": campaign_id,
            "content_posts": content_posts,
            "total_reach": total_reach,
            "cost": cost,
            "roi": round(total_reach / max(cost, 1), 2),
            "date": datetime.now().isoformat(),
        }
        self.collaborations.append(collab)
        if influencer_id in self.profiles:
            self.profiles[influencer_id].past_collaborations += 1
        return collab

    def get_influencer_summary(self) -> Dict[str, Any]:
        """Summarize influencer portfolio."""
        by_tier = defaultdict(int)
        for p in self.profiles.values():
            by_tier[p.tier.value] += 1
        return {
            "total_influencers": len(self.profiles),
            "by_tier": dict(by_tier),
            "total_collaborations": len(self.collaborations),
            "total_spend": sum(c["cost"] for c in self.collaborations),
            "avg_roi": round(
                sum(c["roi"] for c in self.collaborations) / max(len(self.collaborations), 1), 2
            ),
        }


# ---------------------------------------------------------------------------
# Reputation Monitor
# ---------------------------------------------------------------------------

class ReputationMonitor:
    """Monitors brand reputation and sentiment across platforms."""

    def __init__(self) -> None:
        self.events: List[ReputationEvent] = []
        self.alerts: List[Dict[str, Any]] = []
        self.keywords: List[str] = []

    def add_keywords(self, keywords: List[str]) -> None:
        """Add brand keywords to monitor."""
        self.keywords.extend(keywords)

    def record_event(self, platform: Platform, event_type: str,
                     content: str, source: str,
                     sentiment: SentimentType) -> ReputationEvent:
        """Record a reputation event."""
        alert_level = self._assess_alert_level(sentiment, content)
        event = ReputationEvent(
            id=f"rep_{uuid.uuid4().hex[:8]}",
            platform=platform,
            event_type=event_type,
            sentiment=sentiment,
            content=content,
            source=source,
            timestamp=datetime.now(),
            alert_level=alert_level,
        )
        self.events.append(event)

        if alert_level in (ReputationAlertLevel.ORANGE, ReputationAlertLevel.RED):
            self.alerts.append({
                "event_id": event.id,
                "level": alert_level.value,
                "content": content[:100],
                "timestamp": datetime.now().isoformat(),
            })

        return event

    def _assess_alert_level(self, sentiment: SentimentType,
                            content: str) -> ReputationAlertLevel:
        """Determine alert level from sentiment and content."""
        content_lower = content.lower()
        crisis_words = ["scam", "fraud", "lawsuit", "ban", "hack", "breach", "boycott"]

        if any(w in content_lower for w in crisis_words):
            return ReputationAlertLevel.RED
        if sentiment == SentimentType.VERY_NEGATIVE:
            return ReputationAlertLevel.ORANGE
        if sentiment == SentimentType.NEGATIVE:
            return ReputationAlertLevel.YELLOW
        return ReputationAlertLevel.GREEN

    def get_reputation_score(self) -> Dict[str, Any]:
        """Calculate overall reputation score."""
        if not self.events:
            return {"score": 50, "level": "neutral", "total_events": 0}

        sentiment_weights = {
            SentimentType.VERY_POSITIVE: 2,
            SentimentType.POSITIVE: 1,
            SentimentType.NEUTRAL: 0,
            SentimentType.NEGATIVE: -1,
            SentimentType.VERY_NEGATIVE: -2,
        }
        total = sum(sentiment_weights.get(e.sentiment, 0) for e in self.events)
        normalized = max(0, min(100, 50 + total * 5))

        if normalized >= 75:
            level = "excellent"
        elif normalized >= 50:
            level = "good"
        elif normalized >= 25:
            level = "concerning"
        else:
            level = "critical"

        return {
            "score": round(normalized, 1),
            "level": level,
            "total_events": len(self.events),
            "unresolved_alerts": sum(1 for a in self.alerts if not any(
                e.id == a["event_id"] and e.resolved for e in self.events
            )),
        }

    def get_recent_events(self, days: int = 7) -> List[ReputationEvent]:
        """Get recent reputation events."""
        cutoff = datetime.now() - timedelta(days=days)
        return [e for e in self.events if e.timestamp >= cutoff]


# ---------------------------------------------------------------------------
# Social Agent (Orchestrator)
# ---------------------------------------------------------------------------

class SocialAgent:
    """Top-level social media management agent."""

    def __init__(self) -> None:
        self.content = ContentManager()
        self.engagement = EngagementManager()
        self.audience = AudienceAnalyzer()
        self.analytics = SocialAnalytics(self.content, self.engagement, self.audience)
        self.influencer = InfluencerManager()
        self.reputation = ReputationMonitor()
        logger.info("SocialAgent initialized")

    def create_campaign(self, name: str, description: str,
                        platforms: List[Platform],
                        start_date: datetime,
                        end_date: Optional[datetime] = None,
                        budget: float = 0.0) -> Campaign:
        """Create and register a social media campaign."""
        campaign = Campaign(
            id=f"camp_{uuid.uuid4().hex[:8]}",
            name=name,
            description=description,
            platforms=platforms,
            status=CampaignStatus.PLANNING,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            target_audience={},
            kpis={},
            posts=[],
            metrics={"reach": 0, "engagement": 0, "conversions": 0},
            created_at=datetime.now(),
        )
        logger.info("Campaign %s created: %s", campaign.id, name)
        return campaign

    def schedule_content_batch(self, posts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Schedule multiple posts at once."""
        scheduled = []
        for data in posts_data:
            post = self.content.create_post(
                platform=Platform[data["platform"].upper()],
                content=data["content"],
                content_type=ContentType[data.get("type", "POST").upper()],
                scheduled_at=datetime.fromisoformat(data["scheduled_at"]),
                hashtags=data.get("hashtags", []),
            )
            scheduled.append(post.id)
        return {"scheduled_count": len(scheduled), "post_ids": scheduled}

    def respond_to_mentions(self, keyword: str) -> List[Dict[str, Any]]:
        """Find and draft responses for mentions containing keyword."""
        relevant = [
            e for e in self.engagement.engagements
            if keyword.lower() in e.content.lower()
        ]
        responses = []
        for eng in relevant:
            action = "respond" if eng.sentiment not in (
                SentimentType.NEGATIVE, SentimentType.VERY_NEGATIVE
            ) else "escalate"
            responses.append({
                "engagement_id": eng.id,
                "username": eng.username,
                "sentiment": eng.sentiment.value,
                "action": action,
            })
        return responses

    def get_social_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive social media dashboard."""
        kpis = self.analytics.calculate_kpis()
        reputation = self.reputation.get_reputation_score()
        influencer_summary = self.influencer.get_influencer_summary()
        audience_reach = self.audience.calculate_total_reach()

        return {
            "timestamp": datetime.now().isoformat(),
            "kpis": kpis,
            "audience": audience_reach,
            "reputation": reputation,
            "influencers": influencer_summary,
            "top_posts": self.analytics.get_top_performing_posts(3),
            "platform_breakdown": self.analytics.get_platform_breakdown(),
            "recommendations": self.analytics._generate_recommendations(kpis),
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate SocialAgent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    print("\n" + "=" * 60)
    print("  Social Media Agent - Content & Engagement Platform")
    print("=" * 60 + "\n")

    agent = SocialAgent()

    # Create content
    post = agent.content.create_post(
        platform=Platform.TWITTER,
        content="Excited to announce our new security features! Protecting your data is our priority.",
        content_type=ContentType.POST,
        hashtags=["#security", "#privacy", "#tech"],
    )
    print(f"Post created: {post.id}")

    # Schedule content
    batch = agent.schedule_content_batch([
        {"platform": "linkedin", "content": "Enterprise security webinar this Friday", "scheduled_at": "2025-02-01T10:00:00", "type": "POST"},
        {"platform": "twitter", "content": "Thread: 5 tips for better security", "scheduled_at": "2025-02-01T14:00:00", "type": "THREAD"},
    ])
    print(f"Batch scheduled: {batch['scheduled_count']} posts")

    # Track engagement
    eng = agent.engagement.track_engagement(
        post_id=post.id,
        user_id="user_001",
        username="securityfan",
        engagement_type=EngagementType.COMMENT,
        content="This is amazing! Great work on the new features.",
    )
    print(f"Engagement tracked: {eng.id} ({eng.sentiment.value})")

    # Add audience data
    agent.audience.add_audience_data(Platform.TWITTER, {
        "followers": 25000,
        "growth_rate": 0.03,
        "engagement_rate": 0.045,
        "active_hours": [9, 12, 14, 18, 20],
        "demographics": {"18-24": 0.15, "25-34": 0.40, "35-44": 0.30, "45+": 0.15},
    })

    # Record reputation event
    agent.reputation.record_event(
        platform=Platform.TWITTER,
        event_type="mention",
        content="Love the new update from @company",
        source="user_tweet",
        sentiment=SentimentType.POSITIVE,
    )

    # Dashboard
    dashboard = agent.get_social_dashboard()
    print(f"\nDashboard KPIs:")
    print(f"  Total posts: {dashboard['kpis']['total_posts']}")
    print(f"  Total followers: {dashboard['audience']['total_followers']}")
    print(f"  Reputation score: {dashboard['reputation']['score']}/100")
    print()


if __name__ == "__main__":
    main()
