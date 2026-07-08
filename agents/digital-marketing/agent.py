"""Digital Marketing Agent - Comprehensive Marketing Campaigns and Strategy.

This module provides a full-featured digital marketing platform covering
campaign management, channel strategy, paid advertising, email marketing,
social media, SEO/SEM, analytics, and multi-touch attribution modeling.
"""

import logging
import hashlib
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import (
    Any, Callable, Dict, List, Optional, Protocol, Tuple, Union,
)
from uuid import uuid4

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class CampaignStatus(Enum):
    """Lifecycle states of a marketing campaign."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"


class ChannelType(Enum):
    """Supported marketing channels."""
    PAID_SEARCH = "paid_search"
    PAID_SOCIAL = "paid_social"
    DISPLAY = "display"
    VIDEO = "video"
    EMAIL = "email"
    ORGANIC_SEARCH = "organic_search"
    SOCIAL_ORGANIC = "social_organic"
    AFFILIATE = "affiliate"
    INFLUENCER = "influencer"
    CONTENT = "content"
    SMS = "sms"
    PUSH_NOTIFICATION = "push_notification"
    PODCAST = "podcast"
    DIRECT_MAIL = "direct_mail"
    EVENT = "event"


class ObjectiveType(Enum):
    """Campaign objective categories."""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    CONVERSION = "conversion"
    RETENTION = "retention"
    ADVOCACY = "advocacy"
    LEAD_GENERATION = "lead_generation"
    TRAFFIC = "traffic"
    ENGAGEMENT = "engagement"
    APP_INSTALLS = "app_installs"
    STORE_VISITS = "store_visits"


class AttributionModel(Enum):
    """Supported attribution models."""
    FIRST_TOUCH = "first_touch"
    LAST_TOUCH = "last_touch"
    LINEAR = "linear"
    TIME_DECAY = "time_decay"
    POSITION_BASED = "position_based"
    DATA_DRIVEN = "data_driven"
    MARKOV_CHAIN = "markov_chain"
    SHAPLEY_VALUE = "shapley_value"


class AudienceSegment(Enum):
    """Standard audience segmentation buckets."""
    ALL = "all"
    NEW_VISITORS = "new_visitors"
    RETURNING = "returning"
    HIGH_VALUE = "high_value"
    AT_RISK = "at_risk"
    DORMANT = "dormant"
    ENGAGED = "engaged"
    CART_ABANDONERS = "cart_abandoners"
    WINDOW_SHOPPERS = "window_shoppers"
    LOYAL_CUSTOMERS = "loyal_customers"


class BidStrategy(Enum):
    """Automated bidding strategies."""
    MANUAL_CPC = "manual_cpc"
    TARGET CPA = "target_cpa"
    TARGET_ROAS = "target_roas"
    MAXIMIZE_CONVERSIONS = "maximize_conversions"
    MAXIMIZE_CLICKS = "maximize_clicks"
    ENHANCED_CPC = "enhanced_cpc"
    COST_PER_VIEW = "cost_per_view"
    PUBLISHER_OWNED = "publisher_owned"


class EmailEventType(Enum):
    """Email marketing event types."""
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    BOUNCED = "bounced"
    UNSUBSCRIBED = "unsubscribed"
    COMPLAINED = "complained"
    CONVERTED = "converted"


class SocialPlatform(Enum):
    """Social media platform identifiers."""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"
    REDDIT = "reddit"
    SNAPCHAT = "snapchat"
    THREADS = "threads"


class SEOSignal(Enum):
    """SEO performance signals."""
    ORGANIC_TRAFFIC = "organic_traffic"
    KEYWORD_RANKING = "keyword_ranking"
    BACKLINK_COUNT = "backlink_count"
    DOMAIN_AUTHORITY = "domain_authority"
    PAGE_SPEED = "page_speed"
    MOBILE_USABILITY = "mobile_usability"
    CORE_WEB_VITALS = "core_web_vitals"
    SCHEMA_MARKUP = "schema_markup"
    CLICK_THROUGH_RATE = "click_through_rate"
    BOUNCE_RATE = "bounce_rate"


class ReportFrequency(Enum):
    """Reporting cadence options."""
    REALTIME = "realtime"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class AdFormat(Enum):
    """Supported ad creative formats."""
    TEXT = "text"
    IMAGE = "image"
    CAROUSEL = "carousel"
    VIDEO = "video"
    STORY = "story"
    REEL = "reel"
    COLLECTION = "collection"
    SHOPPING = "shopping"
    NATIVE = "native"
    BANNER = "banner"
    INTERSTITIAL = "interstitial"
    PLAYABLE = "playable"


class MetricStatus(Enum):
    """Health status for a metric."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class BudgetAllocation:
    """Budget breakdown for a single channel."""
    channel: ChannelType
    daily_budget: float
    total_budget: float
    currency: str = "USD"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    pacing: str = "even"

    @property
    def remaining_budget(self) -> float:
        if not self.start_date or not self.end_date:
            return self.total_budget
        total_days = max((self.end_date - self.start_date).days, 1)
        elapsed = max((datetime.now() - self.start_date).days, 0)
        spent_ratio = min(elapsed / total_days, 1.0)
        return self.total_budget * (1 - spent_ratio)


@dataclass
class AudienceDefinition:
    """Target audience specification."""
    segment: AudienceSegment
    demographics: Dict[str, Any] = field(default_factory=dict)
    interests: List[str] = field(default_factory=list)
    behaviors: List[str] = field(default_factory=list)
    geo_targets: List[str] = field(default_factory=list)
    exclude_segments: List[AudienceSegment] = field(default_factory=list)
    lookalike_source: Optional[str] = None
    lookalike_percentage: float = 1.0

    def to_filter_dict(self) -> Dict[str, Any]:
        return {
            "segment": self.segment.value,
            "demographics": self.demographics,
            "interests": self.interests,
            "behaviors": self.behaviors,
            "geo_targets": self.geo_targets,
            "exclusions": [s.value for s in self.exclude_segments],
        }


@dataclass
class CreativeAsset:
    """Individual creative asset for an ad."""
    asset_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    format: AdFormat = AdFormat.IMAGE
    headline: str = ""
    body_text: str = ""
    call_to_action: str = "Learn More"
    url: str = ""
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    width: int = 1200
    height: int = 628
    duration_seconds: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height if self.height else 0

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.headline:
            errors.append("Headline is required")
        if self.format in (AdFormat.IMAGE, AdFormat.CAROUSEL) and not self.image_url:
            errors.append("Image URL required for image/carousel format")
        if self.format == AdFormat.VIDEO and not self.video_url:
            errors.append("Video URL required for video format")
        if len(self.headline) > 90:
            errors.append("Headline exceeds 90 characters")
        if len(self.body_text) > 400:
            errors.append("Body text exceeds 400 characters")
        return errors


@dataclass
class AdGroup:
    """A group of ads within a campaign."""
    ad_group_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    channel: ChannelType = ChannelType.PAID_SEARCH
    audience: Optional[AudienceDefinition] = None
    creatives: List[CreativeAsset] = field(default_factory=list)
    bid_strategy: BidStrategy = BidStrategy.MANUAL_CPC
    bid_amount: float = 0.0
    keywords: List[str] = field(default_factory=list)
    negative_keywords: List[str] = field(default_factory=list)
    status: CampaignStatus = CampaignStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    def active_creatives(self) -> List[CreativeAsset]:
        return self.creatives

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.name:
            errors.append("Ad group name is required")
        if not self.creatives:
            errors.append("At least one creative asset is required")
        if self.bid_amount < 0:
            errors.append("Bid amount cannot be negative")
        for creative in self.creatives:
            errors.extend(creative.validate())
        return errors


@dataclass
class Campaign:
    """A marketing campaign."""
    campaign_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    objective: ObjectiveType = ObjectiveType.AWARENESS
    status: CampaignStatus = CampaignStatus.DRAFT
    channels: List[ChannelType] = field(default_factory=list)
    budget: Optional[BudgetAllocation] = None
    ad_groups: List[AdGroup] = field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    kpis: Dict[str, float] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def total_budget(self) -> float:
        if self.budget:
            return self.budget.total_budget
        return sum(ag.bid_amount for ag in self.ad_groups)

    @property
    def is_active(self) -> bool:
        return self.status == CampaignStatus.ACTIVE

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.name:
            errors.append("Campaign name is required")
        if not self.channels:
            errors.append("At least one channel must be selected")
        if self.total_budget <= 0:
            errors.append("Campaign budget must be positive")
        for ag in self.ad_groups:
            for err in ag.validate():
                errors.append(f"Ad group '{ag.name}': {err}")
        return errors


@dataclass
class Touchpoint:
    """A single touchpoint in a customer journey."""
    touchpoint_id: str = field(default_factory=lambda: str(uuid4()))
    channel: ChannelType = ChannelType.PAID_SEARCH
    campaign_id: Optional[str] = None
    ad_group_id: Optional[str] = None
    creative_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    cost: float = 0.0
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    visitor_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttributionResult:
    """Result of an attribution analysis."""
    model: AttributionModel = AttributionModel.LINEAR
    channel_credits: Dict[str, float] = field(default_factory=dict)
    total_conversions: int = 0
    total_revenue: float = 0.0
    total_cost: float = 0.0
    roas: float = 0.0
    cost_per_conversion: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EmailCampaign:
    """Email marketing campaign specification."""
    email_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    subject_line: str = ""
    preview_text: str = ""
    from_name: str = ""
    from_email: str = ""
    reply_to: str = ""
    html_content: str = ""
    plain_text_content: str = ""
    audience: Optional[AudienceDefinition] = None
    send_time: Optional[datetime] = None
    timezone: str = "UTC"
    ab_test_variants: List[Dict[str, str]] = field(default_factory=list)
    suppression_lists: List[str] = field(default_factory=list)
    status: CampaignStatus = CampaignStatus.DRAFT

    @property
    def has_ab_test(self) -> bool:
        return len(self.ab_test_variants) > 0


@dataclass
class EmailMetrics:
    """Email performance metrics."""
    email_id: str = ""
    sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    bounced: int = 0
    unsubscribed: int = 0
    complained: int = 0
    converted: int = 0

    @property
    def delivery_rate(self) -> float:
        return self.delivered / self.sent if self.sent else 0

    @property
    def open_rate(self) -> float:
        return self.opened / self.delivered if self.delivered else 0

    @property
    def click_rate(self) -> float:
        return self.clicked / self.delivered if self.delivered else 0

    @property
    def conversion_rate(self) -> float:
        return self.converted / self.delivered if self.delivered else 0

    @property
    def unsubscribe_rate(self) -> float:
        return self.unsubscribed / self.delivered if self.delivered else 0

    @property
    def bounce_rate(self) -> float:
        return self.bounced / self.sent if self.sent else 0

    @property
    def spam_complaint_rate(self) -> float:
        return self.complained / self.delivered if self.delivered else 0


@dataclass
class SocialPost:
    """Social media post specification."""
    post_id: str = field(default_factory=lambda: str(uuid4()))
    platform: SocialPlatform = SocialPlatform.FACEBOOK
    content: str = ""
    media_urls: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)
    scheduled_time: Optional[datetime] = None
    link_url: Optional[str] = None
    audience: Optional[AudienceDefinition] = None
    status: CampaignStatus = CampaignStatus.DRAFT

    @property
    def has_media(self) -> bool:
        return len(self.media_urls) > 0


@dataclass
class SocialMetrics:
    """Social media performance metrics."""
    post_id: str = ""
    platform: SocialPlatform = SocialPlatform.FACEBOOK
    impressions: int = 0
    reach: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    clicks: int = 0
    link_clicks: int = 0
    video_views: int = 0
    engagement_rate: float = 0.0
    cost_per_click: float = 0.0
    cost_per_mille: float = 0.0
    conversions: int = 0

    @property
    def total_engagement(self) -> int:
        return self.likes + self.comments + self.shares + self.saves

    @property
    def computed_engagement_rate(self) -> float:
        return self.total_engagement / self.reach if self.reach else 0


@dataclass
class SEOKeyword:
    """A tracked SEO keyword."""
    keyword_id: str = field(default_factory=lambda: str(uuid4()))
    keyword: str = ""
    url: str = ""
    position: int = 0
    previous_position: int = 0
    search_volume: int = 0
    keyword_difficulty: float = 0.0
    click_through_rate: float = 0.0
    impressions: int = 0
    clicks: int = 0
    is_tracked: bool = True
    last_checked: Optional[datetime] = None

    @property
    def position_change(self) -> int:
        return self.previous_position - self.position

    @property
    def is_top_10(self) -> bool:
        return 1 <= self.position <= 10

    @property
    def is_top_3(self) -> bool:
        return 1 <= self.position <= 3


@dataclass
class SEOAuditResult:
    """SEO site audit findings."""
    audit_id: str = field(default_factory=lambda: str(uuid4()))
    domain: str = ""
    audit_date: datetime = field(default_factory=datetime.now)
    overall_score: float = 0.0
    page_speed_score: float = 0.0
    mobile_score: float = 0.0
    seo_score: float = 0.0
    accessibility_score: float = 0.0
    issues_critical: int = 0
    issues_warning: int = 0
    issues_info: int = 0
    pages_crawled: int = 0
    issues: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class ConversionGoal:
    """A tracked conversion goal."""
    goal_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    url_pattern: str = ""
    value: float = 0.0
    type: str = "destination"
    is_primary: bool = False
    count: int = 0
    total_value: float = 0.0

    def record_conversion(self, revenue: float = 0.0) -> None:
        self.count += 1
        self.total_value += revenue or self.value


@dataclass
class ChannelPerformance:
    """Aggregated performance data for a single channel."""
    channel: ChannelType = ChannelType.PAID_SEARCH
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    cost: float = 0.0
    revenue: float = 0.0
    ctr: float = 0.0
    cpc: float = 0.0
    cpa: float = 0.0
    roas: float = 0.0

    def compute_derived(self) -> None:
        self.ctr = self.clicks / self.impressions if self.impressions else 0
        self.cpc = self.cost / self.clicks if self.clicks else 0
        self.cpa = self.cost / self.conversions if self.conversions else 0
        self.roas = self.revenue / self.cost if self.cost else 0


@dataclass
class DashboardSnapshot:
    """Point-in-time dashboard data."""
    snapshot_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    total_spend: float = 0.0
    total_revenue: float = 0.0
    total_conversions: int = 0
    total_impressions: int = 0
    total_clicks: int = 0
    overall_ctr: float = 0.0
    overall_roas: float = 0.0
    channel_data: Dict[str, ChannelPerformance] = field(default_factory=dict)
    top_campaigns: List[Dict[str, Any]] = field(default_factory=list)
    alerts: List[Dict[str, Any]] = field(default_factory=list)

    def compute_derived(self) -> None:
        self.overall_ctr = (
            self.total_clicks / self.total_impressions
            if self.total_impressions else 0
        )
        self.overall_roas = (
            self.total_revenue / self.total_spend
            if self.total_spend else 0
        )


# ---------------------------------------------------------------------------
# Protocol / Interface Definitions
# ---------------------------------------------------------------------------

class Reportable(Protocol):
    """Anything that can produce a report dict."""
    def to_report(self) -> Dict[str, Any]: ...


class Auditable(Protocol):
    """Anything that can be audited for compliance."""
    def audit(self) -> Dict[str, Any]: ...


# ---------------------------------------------------------------------------
# Core Agent Classes
# ---------------------------------------------------------------------------

class CampaignManager:
    """Full lifecycle management for marketing campaigns."""

    def __init__(self) -> None:
        self._campaigns: Dict[str, Campaign] = {}
        self._audit_log: List[Dict[str, Any]] = []
        logger.info("CampaignManager initialized")

    def create_campaign(
        self,
        name: str,
        objective: ObjectiveType,
        channels: List[ChannelType],
        budget_total: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> Campaign:
        campaign = Campaign(
            name=name,
            objective=objective,
            channels=channels,
            start_date=start_date or datetime.now(),
            end_date=end_date or (datetime.now() + timedelta(days=30)),
            tags=tags or [],
        )
        campaign.budget = BudgetAllocation(
            channel=ChannelType.PAID_SEARCH,
            daily_budget=budget_total / 30,
            total_budget=budget_total,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
        )
        self._campaigns[campaign.campaign_id] = campaign
        self._log_event("campaign_created", campaign.campaign_id, {"name": name})
        logger.info("Campaign created: %s (%s)", name, campaign.campaign_id)
        return campaign

    def update_campaign(
        self, campaign_id: str, updates: Dict[str, Any]
    ) -> Campaign:
        if campaign_id not in self._campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        campaign = self._campaigns[campaign_id]
        for key, value in updates.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)
        campaign.updated_at = datetime.now()
        self._log_event("campaign_updated", campaign_id, updates)
        return campaign

    def delete_campaign(self, campaign_id: str) -> bool:
        if campaign_id not in self._campaigns:
            return False
        del self._campaigns[campaign_id]
        self._log_event("campaign_deleted", campaign_id, {})
        return True

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        return self._campaigns.get(campaign_id)

    def list_campaigns(
        self,
        status: Optional[CampaignStatus] = None,
        channel: Optional[ChannelType] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Campaign]:
        results = list(self._campaigns.values())
        if status:
            results = [c for c in results if c.status == status]
        if channel:
            results = [c for c in results if channel in c.channels]
        if tags:
            results = [
                c for c in results if any(t in c.tags for t in tags)
            ]
        return results

    def activate_campaign(self, campaign_id: str) -> bool:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return False
        errors = campaign.validate()
        if errors:
            logger.warning("Campaign validation failed: %s", errors)
            return False
        campaign.status = CampaignStatus.ACTIVE
        campaign.updated_at = datetime.now()
        self._log_event("campaign_activated", campaign_id, {})
        return True

    def pause_campaign(self, campaign_id: str) -> bool:
        campaign = self.get_campaign(campaign_id)
        if not campaign or campaign.status != CampaignStatus.ACTIVE:
            return False
        campaign.status = CampaignStatus.PAUSED
        campaign.updated_at = datetime.now()
        self._log_event("campaign_paused", campaign_id, {})
        return True

    def complete_campaign(self, campaign_id: str) -> bool:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return False
        campaign.status = CampaignStatus.COMPLETED
        campaign.updated_at = datetime.now()
        self._log_event("campaign_completed", campaign_id, {})
        return True

    def duplicate_campaign(
        self, campaign_id: str, new_name: str
    ) -> Optional[Campaign]:
        original = self.get_campaign(campaign_id)
        if not original:
            return None
        new_campaign = Campaign(
            name=new_name,
            objective=original.objective,
            channels=list(original.channels),
            start_date=datetime.now(),
            end_date=original.end_date,
            tags=list(original.tags),
            kpis=dict(original.kpis),
        )
        new_campaign.budget = BudgetAllocation(
            channel=ChannelType.PAID_SEARCH,
            daily_budget=original.total_budget / 30,
            total_budget=original.total_budget,
        )
        self._campaigns[new_campaign.campaign_id] = new_campaign
        self._log_event(
            "campaign_duplicated",
            new_campaign.campaign_id,
            {"source": campaign_id},
        )
        return new_campaign

    def add_ad_group(self, campaign_id: str, ad_group: AdGroup) -> bool:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return False
        campaign.ad_groups.append(ad_group)
        campaign.updated_at = datetime.now()
        return True

    def get_campaign_health(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            return {"status": "not_found"}
        return {
            "campaign_id": campaign_id,
            "status": campaign.status.value,
            "validation_errors": campaign.validate(),
            "ad_groups": len(campaign.ad_groups),
            "total_creatives": sum(
                len(ag.creatives) for ag in campaign.ad_groups
            ),
            "budget_remaining": (
                campaign.budget.remaining_budget if campaign.budget else 0
            ),
        }

    def _log_event(
        self, event_type: str, campaign_id: str, details: Dict[str, Any]
    ) -> None:
        self._audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "campaign_id": campaign_id,
            "details": details,
        })


class ChannelStrategyEngine:
    """Develops and optimizes multi-channel marketing strategies."""

    CHANNEL_COST_BENCHMARKS: Dict[ChannelType, Dict[str, float]] = {
        ChannelType.PAID_SEARCH: {"avg_cpc": 2.69, "avg_cpm": 12.0},
        ChannelType.PAID_SOCIAL: {"avg_cpc": 1.72, "avg_cpm": 8.0},
        ChannelType.DISPLAY: {"avg_cpc": 0.63, "avg_cpm": 3.12},
        ChannelType.EMAIL: {"avg_cpc": 0.10, "avg_cpm": 1.50},
        ChannelType.VIDEO: {"avg_cpc": 0.10, "avg_cpm": 5.0},
        ChannelType.AFFILIATE: {"avg_cpc": 1.20, "avg_cpm": 6.0},
        ChannelType.INFLUENCER: {"avg_cpc": 3.00, "avg_cpm": 15.0},
    }

    def __init__(self) -> None:
        self._strategies: Dict[str, Dict[str, Any]] = {}
        logger.info("ChannelStrategyEngine initialized")

    def develop_strategy(
        self,
        objective: ObjectiveType,
        total_budget: float,
        target_audience: AudienceDefinition,
        preferred_channels: Optional[List[ChannelType]] = None,
    ) -> Dict[str, Any]:
        channels = preferred_channels or self._recommend_channels(
            objective, target_audience
        )
        allocation = self._allocate_budget(
            channels, total_budget, objective
        )
        strategy = {
            "objective": objective.value,
            "total_budget": total_budget,
            "channels": [ch.value for ch in channels],
            "budget_allocation": {
                ch.value: alloc for ch, alloc in allocation.items()
            },
            "audience": target_audience.to_filter_dict(),
            "recommended_bid_strategy": self._recommend_bid_strategy(
                objective
            ),
            "estimated_metrics": self._estimate_metrics(
                channels, allocation, objective
            ),
            "created_at": datetime.now().isoformat(),
        }
        strategy_id = hashlib.md5(
            f"{objective.value}_{total_budget}".encode()
        ).hexdigest()[:12]
        self._strategies[strategy_id] = strategy
        return strategy

    def optimize_allocation(
        self,
        strategy_id: str,
        performance_data: Dict[str, ChannelPerformance],
    ) -> Dict[str, Any]:
        if strategy_id not in self._strategies:
            raise ValueError(f"Strategy {strategy_id} not found")
        strategy = self._strategies[strategy_id]
        current_alloc = strategy["budget_allocation"]
        new_alloc: Dict[str, float] = {}
        total_roas = sum(
            p.roas for p in performance_data.values() if p.roas > 0
        )
        for channel_name, current_amount in current_alloc.items():
            ch = ChannelType(channel_name)
            if ch in performance_data:
                perf = performance_data[ch]
                if total_roas > 0:
                    weight = perf.roas / total_roas
                else:
                    weight = 1.0 / len(current_alloc)
                new_alloc[channel_name] = strategy["total_budget"] * weight
            else:
                new_alloc[channel_name] = current_amount
        strategy["budget_allocation"] = new_alloc
        strategy["last_optimized"] = datetime.now().isoformat()
        return strategy

    def get_channel_recommendations(
        self,
        objective: ObjectiveType,
        audience: AudienceDefinition,
        budget: float,
    ) -> List[Dict[str, Any]]:
        recommendations: List[Dict[str, Any]] = []
        channels = self._recommend_channels(objective, audience)
        for ch in channels:
            bench = self.CHANNEL_COST_BENCHMARKS.get(ch, {})
            recommendations.append({
                "channel": ch.value,
                "estimated_cpc": bench.get("avg_cpc", 0),
                "estimated_cpm": bench.get("avg_cpm", 0),
                "estimated_daily_clicks": (
                    budget / 30 / bench.get("avg_cpc", 1)
                    if bench.get("avg_cpc", 0) > 0 else 0
                ),
                "fit_score": self._score_channel_fit(ch, objective, audience),
            })
        recommendations.sort(key=lambda r: r["fit_score"], reverse=True)
        return recommendations

    def _recommend_channels(
        self,
        objective: ObjectiveType,
        audience: AudienceDefinition,
    ) -> List[ChannelType]:
        objective_channel_map: Dict[ObjectiveType, List[ChannelType]] = {
            ObjectiveType.AWARENESS: [
                ChannelType.PAID_SOCIAL,
                ChannelType.DISPLAY,
                ChannelType.VIDEO,
            ],
            ObjectiveType.CONSIDERATION: [
                ChannelType.PAID_SEARCH,
                ChannelType.CONTENT,
                ChannelType.SOCIAL_ORGANIC,
            ],
            ObjectiveType.CONVERSION: [
                ChannelType.PAID_SEARCH,
                ChannelType.EMAIL,
                ChannelType.DISPLAY,
            ],
            ObjectiveType.RETENTION: [
                ChannelType.EMAIL,
                ChannelType.PUSH_NOTIFICATION,
                ChannelType.SMS,
            ],
            ObjectiveType.LEAD_GENERATION: [
                ChannelType.PAID_SEARCH,
                ChannelType.PAID_SOCIAL,
                ChannelType.CONTENT,
            ],
            ObjectiveType.TRAFFIC: [
                ChannelType.PAID_SEARCH,
                ChannelType.SOCIAL_ORGANIC,
                ChannelType.CONTENT,
                ChannelType.AFFILIATE,
            ],
        }
        return objective_channel_map.get(
            objective,
            [ChannelType.PAID_SEARCH, ChannelType.PAID_SOCIAL],
        )

    def _allocate_budget(
        self,
        channels: List[ChannelType],
        total_budget: float,
        objective: ObjectiveType,
    ) -> Dict[ChannelType, float]:
        weights: Dict[ChannelType, float] = {}
        for ch in channels:
            weights[ch] = 1.0
        if objective == ObjectiveType.AWARENESS:
            for ch in channels:
                if ch == ChannelType.VIDEO:
                    weights[ch] = 2.0
                elif ch == ChannelType.DISPLAY:
                    weights[ch] = 1.5
        elif objective == ObjectiveType.CONVERSION:
            for ch in channels:
                if ch == ChannelType.PAID_SEARCH:
                    weights[ch] = 2.5
                elif ch == ChannelType.EMAIL:
                    weights[ch] = 1.8
        total_weight = sum(weights.values())
        return {
            ch: total_budget * (weights[ch] / total_weight)
            for ch in channels
        }

    def _recommend_bid_strategy(
        self, objective: ObjectiveType
    ) -> BidStrategy:
        strategy_map: Dict[ObjectiveType, BidStrategy] = {
            ObjectiveType.AWARENESS: BidStrategy.MAXIMIZE_CLICKS,
            ObjectiveType.CONSIDERATION: BidStrategy.ENHANCED_CPC,
            ObjectiveType.CONVERSION: BidStrategy.TARGET CPA,
            ObjectiveType.RETENTION: BidStrategy.TARGET_ROAS,
            ObjectiveType.LEAD_GENERATION: BidStrategy.TARGET CPA,
            ObjectiveType.TRAFFIC: BidStrategy.MAXIMIZE_CLICKS,
        }
        return strategy_map.get(objective, BidStrategy.MANUAL_CPC)

    def _estimate_metrics(
        self,
        channels: List[ChannelType],
        allocation: Dict[ChannelType, float],
        objective: ObjectiveType,
    ) -> Dict[str, Dict[str, float]]:
        estimates: Dict[str, Dict[str, float]] = {}
        for ch in channels:
            budget = allocation.get(ch, 0)
            bench = self.CHANNEL_COST_BENCHMARKS.get(ch, {})
            cpc = bench.get("avg_cpc", 1.0)
            clicks = budget / cpc if cpc > 0 else 0
            conversion_rate = 0.02 if objective == ObjectiveType.CONVERSION else 0.01
            estimates[ch.value] = {
                "estimated_clicks": round(clicks, 0),
                "estimated_impressions": round(clicks * 20, 0),
                "estimated_conversions": round(clicks * conversion_rate, 0),
            }
        return estimates

    def _score_channel_fit(
        self,
        channel: ChannelType,
        objective: ObjectiveType,
        audience: AudienceDefinition,
    ) -> float:
        score = 50.0
        channel_obj_fit = self._recommend_channels(objective, audience)
        if channel in channel_obj_fit:
            idx = channel_obj_fit.index(channel)
            score += (len(channel_obj_fit) - idx) * 10
        if audience.segment in (
            AudienceSegment.ENGAGED,
            AudienceSegment.HIGH_VALUE,
        ):
            if channel in (ChannelType.EMAIL, ChannelType.PUSH_NOTIFICATION):
                score += 15
        if audience.segment == AudienceSegment.NEW_VISITORS:
            if channel in (
                ChannelType.PAID_SEARCH,
                ChannelType.DISPLAY,
                ChannelType.VIDEO,
            ):
                score += 10
        return min(score, 100.0)


class PerformanceAnalytics:
    """Track and analyze campaign performance metrics."""

    def __init__(self) -> None:
        self._touchpoints: List[Touchpoint] = []
        self._channel_performance: Dict[ChannelType, ChannelPerformance] = {}
        self._conversion_goals: Dict[str, ConversionGoal] = {}
        logger.info("PerformanceAnalytics initialized")

    def record_touchpoint(self, touchpoint: Touchpoint) -> None:
        self._touchpoints.append(touchpoint)
        ch = touchpoint.channel
        if ch not in self._channel_performance:
            self._channel_performance[ch] = ChannelPerformance(channel=ch)
        perf = self._channel_performance[ch]
        perf.impressions += touchpoint.impressions
        perf.clicks += touchpoint.clicks
        perf.conversions += touchpoint.conversions
        perf.cost += touchpoint.cost
        perf.revenue += touchpoint.revenue
        perf.compute_derived()

    def get_channel_performance(
        self, channel: Optional[ChannelType] = None
    ) -> Union[ChannelPerformance, Dict[str, ChannelPerformance]]:
        if channel:
            return self._channel_performance.get(
                channel, ChannelPerformance(channel=channel)
            )
        return dict(self._channel_performance)

    def get_total_metrics(self) -> Dict[str, float]:
        totals = {
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "cost": 0.0,
            "revenue": 0.0,
        }
        for perf in self._channel_performance.values():
            totals["impressions"] += perf.impressions
            totals["clicks"] += perf.clicks
            totals["conversions"] += perf.conversions
            totals["cost"] += perf.cost
            totals["revenue"] += perf.revenue
        totals["ctr"] = (
            totals["clicks"] / totals["impressions"]
            if totals["impressions"] else 0
        )
        totals["cpc"] = (
            totals["cost"] / totals["clicks"] if totals["clicks"] else 0
        )
        totals["cpa"] = (
            totals["cost"] / totals["conversions"]
            if totals["conversions"] else 0
        )
        totals["roas"] = (
            totals["revenue"] / totals["cost"] if totals["cost"] else 0
        )
        return totals

    def create_dashboard(self) -> DashboardSnapshot:
        totals = self.get_total_metrics()
        snapshot = DashboardSnapshot(
            total_spend=totals["cost"],
            total_revenue=totals["revenue"],
            total_conversions=int(totals["conversions"]),
            total_impressions=int(totals["impressions"]),
            total_clicks=int(totals["clicks"]),
            overall_ctr=totals["ctr"],
            overall_roas=totals["roas"],
            channel_data=dict(self._channel_performance),
        )
        snapshot.alerts = self._generate_alerts()
        return snapshot

    def get_performance_trend(
        self, days: int = 30
    ) -> List[Dict[str, Any]]:
        cutoff = datetime.now() - timedelta(days=days)
        daily_data: Dict[str, Dict[str, float]] = {}
        for tp in self._touchpoints:
            if tp.timestamp < cutoff:
                continue
            day_key = tp.timestamp.strftime("%Y-%m-%d")
            if day_key not in daily_data:
                daily_data[day_key] = {
                    "impressions": 0,
                    "clicks": 0,
                    "conversions": 0,
                    "cost": 0.0,
                    "revenue": 0.0,
                }
            daily_data[day_key]["impressions"] += tp.impressions
            daily_data[day_key]["clicks"] += tp.clicks
            daily_data[day_key]["conversions"] += tp.conversions
            daily_data[day_key]["cost"] += tp.cost
            daily_data[day_key]["revenue"] += tp.revenue
        trend: List[Dict[str, Any]] = []
        for day, data in sorted(daily_data.items()):
            ctr = data["clicks"] / data["impressions"] if data["impressions"] else 0
            cpc = data["cost"] / data["clicks"] if data["clicks"] else 0
            roas = data["revenue"] / data["cost"] if data["cost"] else 0
            trend.append({
                "date": day,
                "impressions": int(data["impressions"]),
                "clicks": int(data["clicks"]),
                "conversions": int(data["conversions"]),
                "cost": round(data["cost"], 2),
                "revenue": round(data["revenue"], 2),
                "ctr": round(ctr, 4),
                "cpc": round(cpc, 2),
                "roas": round(roas, 2),
            })
        return trend

    def register_conversion_goal(self, goal: ConversionGoal) -> None:
        self._conversion_goals[goal.goal_id] = goal

    def get_conversion_summary(self) -> Dict[str, Any]:
        return {
            "goals": [
                {
                    "name": g.name,
                    "count": g.count,
                    "total_value": g.total_value,
                    "is_primary": g.is_primary,
                }
                for g in self._conversion_goals.values()
            ],
            "total_conversions": sum(g.count for g in self._conversion_goals.values()),
            "total_value": sum(g.total_value for g in self._conversion_goals.values()),
        }

    def _generate_alerts(self) -> List[Dict[str, Any]]:
        alerts: List[Dict[str, Any]] = []
        for ch, perf in self._channel_performance.items():
            if perf.cost > 0 and perf.roas < 1.0:
                alerts.append({
                    "severity": "critical",
                    "channel": ch.value,
                    "message": f"ROAS below 1.0 for {ch.value} ({perf.roas:.2f})",
                })
            if perf.clicks > 0 and perf.cpc > 5.0:
                alerts.append({
                    "severity": "warning",
                    "channel": ch.value,
                    "message": f"High CPC for {ch.value} (${perf.cpc:.2f})",
                })
            if perf.impressions > 10000 and perf.ctr < 0.005:
                alerts.append({
                    "severity": "warning",
                    "channel": ch.value,
                    "message": f"Low CTR for {ch.value} ({perf.ctr:.3%})",
                })
        return alerts


class AttributionEngine:
    """Multi-touch attribution modeling."""

    def __init__(self) -> None:
        self._touchpoint_store: List[Touchpoint] = []
        self._results_cache: Dict[AttributionModel, AttributionResult] = {}
        logger.info("AttributionEngine initialized")

    def add_touchpoints(self, touchpoints: List[Touchpoint]) -> None:
        self._touchpoint_store.extend(touchpoints)
        self._results_cache.clear()

    def compute_attribution(
        self, model: AttributionModel = AttributionModel.LINEAR
    ) -> AttributionResult:
        if model in self._results_cache:
            return self._results_cache[model]
        journeys = self._group_journeys()
        channel_credits: Dict[str, float] = {}
        total_conversions = 0
        total_revenue = 0.0
        total_cost = 0.0
        for visitor_id, touchpoints in journeys.items():
            sorted_tps = sorted(touchpoints, key=lambda t: t.timestamp)
            has_conversion = any(tp.conversions > 0 for tp in sorted_tps)
            journey_revenue = sum(tp.revenue for tp in sorted_tps)
            journey_cost = sum(tp.cost for tp in sorted_tps)
            if has_conversion:
                total_conversions += sum(tp.conversions for tp in sorted_tps)
                total_revenue += journey_revenue
            total_cost += journey_cost
            credits = self._compute_journey_credits(sorted_tps, model)
            for ch, credit in credits.items():
                channel_credits[ch] = channel_credits.get(ch, 0) + credit
        total_credit = sum(channel_credits.values()) or 1.0
        normalized = {
            ch: credit / total_credit for ch, credit in channel_credits.items()
        }
        result = AttributionResult(
            model=model,
            channel_credits=normalized,
            total_conversions=total_conversions,
            total_revenue=total_revenue,
            total_cost=total_cost,
            roas=total_revenue / total_cost if total_cost else 0,
            cost_per_conversion=(
                total_cost / total_conversions if total_conversions else 0
            ),
        )
        self._results_cache[model] = result
        return result

    def compare_models(self) -> Dict[str, AttributionResult]:
        results: Dict[str, AttributionResult] = {}
        for model in AttributionModel:
            results[model.value] = self.compute_attribution(model)
        return results

    def get_channel_attribution(
        self, model: AttributionModel = AttributionModel.LINEAR
    ) -> Dict[str, Dict[str, float]]:
        result = self.compute_attribution(model)
        channel_details: Dict[str, Dict[str, float]] = {}
        for ch, credit_share in result.channel_credits.items():
            channel_details[ch] = {
                "credit_share": credit_share,
                "estimated_revenue": result.total_revenue * credit_share,
                "estimated_conversions": (
                    result.total_conversions * credit_share
                ),
            }
        return channel_details

    def _group_journeys(self) -> Dict[str, List[Touchpoint]]:
        journeys: Dict[str, List[Touchpoint]] = {}
        for tp in self._touchpoint_store:
            vid = tp.visitor_id or "anonymous"
            if vid not in journeys:
                journeys[vid] = []
            journeys[vid].append(tp)
        return journeys

    def _compute_journey_credits(
        self,
        touchpoints: List[Touchpoint],
        model: AttributionModel,
    ) -> Dict[str, float]:
        credits: Dict[str, float] = {}
        n = len(touchpoints)
        if n == 0:
            return credits
        if model == AttributionModel.FIRST_TOUCH:
            ch = touchpoints[0].channel.value
            credits[ch] = 1.0
        elif model == AttributionModel.LAST_TOUCH:
            ch = touchpoints[-1].channel.value
            credits[ch] = 1.0
        elif model == AttributionModel.LINEAR:
            for tp in touchpoints:
                ch = tp.channel.value
                credits[ch] = credits.get(ch, 0) + 1.0 / n
        elif model == AttributionModel.TIME_DECAY:
            half_life_days = 7.0
            total_weight = 0.0
            weights: List[Tuple[str, float]] = []
            for tp in touchpoints:
                age = (
                    touchpoints[-1].timestamp - tp.timestamp
                ).total_seconds() / 86400
                w = 2 ** (-age / half_life_days)
                weights.append((tp.channel.value, w))
                total_weight += w
            for ch, w in weights:
                credits[ch] = credits.get(ch, 0) + w / total_weight
        elif model == AttributionModel.POSITION_BASED:
            for i, tp in enumerate(touchpoints):
                ch = tp.channel.value
                if i == 0:
                    credits[ch] = credits.get(ch, 0) + 0.4
                elif i == n - 1:
                    credits[ch] = credits.get(ch, 0) + 0.4
                else:
                    credits[ch] = credits.get(ch, 0) + 0.2 / max(n - 2, 1)
        return credits


class EmailMarketingEngine:
    """Email campaign creation, sending, and analytics."""

    def __init__(self) -> None:
        self._campaigns: Dict[str, EmailCampaign] = {}
        self._metrics: Dict[str, EmailMetrics] = {}
        self._event_log: List[Dict[str, Any]] = []
        logger.info("EmailMarketingEngine initialized")

    def create_campaign(
        self,
        name: str,
        subject_line: str,
        from_email: str,
        html_content: str,
        audience: Optional[AudienceDefinition] = None,
    ) -> EmailCampaign:
        campaign = EmailCampaign(
            name=name,
            subject_line=subject_line,
            from_email=from_email,
            html_content=html_content,
            audience=audience,
        )
        self._campaigns[campaign.email_id] = campaign
        self._metrics[campaign.email_id] = EmailMetrics(email_id=campaign.email_id)
        return campaign

    def send_campaign(
        self, email_id: str, recipient_count: int
    ) -> Dict[str, Any]:
        campaign = self._campaigns.get(email_id)
        if not campaign:
            raise ValueError(f"Campaign {email_id} not found")
        campaign.status = CampaignStatus.ACTIVE
        metrics = self._metrics.get(email_id, EmailMetrics(email_id=email_id))
        metrics.sent = recipient_count
        metrics.delivered = int(recipient_count * 0.97)
        metrics.bounced = recipient_count - metrics.delivered
        self._metrics[email_id] = metrics
        self._event_log.append({
            "timestamp": datetime.now().isoformat(),
            "event": "campaign_sent",
            "email_id": email_id,
            "recipients": recipient_count,
        })
        return {
            "status": "sent",
            "email_id": email_id,
            "recipients": recipient_count,
        }

    def record_event(
        self,
        email_id: str,
        event_type: EmailEventType,
        count: int = 1,
    ) -> None:
        metrics = self._metrics.get(email_id)
        if not metrics:
            return
        if event_type == EmailEventType.OPENED:
            metrics.opened += count
        elif event_type == EmailEventType.CLICKED:
            metrics.clicked += count
        elif event_type == EmailEventType.UNSUBSCRIBED:
            metrics.unsubscribed += count
        elif event_type == EmailEventType.COMPLAINED:
            metrics.complained += count
        elif event_type == EmailEventType.CONVERTED:
            metrics.converted += count

    def get_campaign_metrics(self, email_id: str) -> Optional[EmailMetrics]:
        return self._metrics.get(email_id)

    def get_all_metrics(self) -> Dict[str, EmailMetrics]:
        return dict(self._metrics)

    def calculate_roi(
        self, email_id: str, revenue_per_conversion: float = 50.0
    ) -> Dict[str, float]:
        metrics = self._metrics.get(email_id)
        if not metrics:
            return {"roi": 0, "revenue": 0, "cost": 0}
        revenue = metrics.converted * revenue_per_conversion
        cost = metrics.sent * 0.001
        roi = ((revenue - cost) / cost * 100) if cost > 0 else 0
        return {
            "roi": round(roi, 2),
            "revenue": round(revenue, 2),
            "cost": round(cost, 2),
        }

    def get_segment_performance(
        self,
    ) -> Dict[str, Dict[str, float]]:
        segment_data: Dict[str, Dict[str, float]] = {}
        for email_id, metrics in self._metrics.items():
            campaign = self._campaigns.get(email_id)
            if not campaign or not campaign.audience:
                continue
            segment = campaign.audience.segment.value
            if segment not in segment_data:
                segment_data[segment] = {
                    "total_sent": 0,
                    "total_opened": 0,
                    "total_clicked": 0,
                    "total_converted": 0,
                }
            segment_data[segment]["total_sent"] += metrics.sent
            segment_data[segment]["total_opened"] += metrics.opened
            segment_data[segment]["total_clicked"] += metrics.clicked
            segment_data[segment]["total_converted"] += metrics.converted
        for seg, data in segment_data.items():
            data["open_rate"] = (
                data["total_opened"] / data["total_sent"]
                if data["total_sent"] else 0
            )
            data["click_rate"] = (
                data["total_clicked"] / data["total_sent"]
                if data["total_sent"] else 0
            )
        return segment_data


class SocialMediaManager:
    """Social media post management and analytics."""

    def __init__(self) -> None:
        self._posts: Dict[str, SocialPost] = {}
        self._metrics: Dict[str, SocialMetrics] = {}
        self._scheduling_queue: List[str] = []
        logger.info("SocialMediaManager initialized")

    def create_post(
        self,
        platform: SocialPlatform,
        content: str,
        media_urls: Optional[List[str]] = None,
        hashtags: Optional[List[str]] = None,
        scheduled_time: Optional[datetime] = None,
    ) -> SocialPost:
        post = SocialPost(
            platform=platform,
            content=content,
            media_urls=media_urls or [],
            hashtags=hashtags or [],
            scheduled_time=scheduled_time,
        )
        if scheduled_time:
            post.status = CampaignStatus.SCHEDULED
            self._scheduling_queue.append(post.post_id)
        self._posts[post.post_id] = post
        self._metrics[post.post_id] = SocialMetrics(
            post_id=post.post_id, platform=platform
        )
        return post

    def publish_post(self, post_id: str) -> bool:
        post = self._posts.get(post_id)
        if not post:
            return False
        post.status = CampaignStatus.ACTIVE
        if post_id in self._scheduling_queue:
            self._scheduling_queue.remove(post_id)
        return True

    def record_engagement(
        self, post_id: str, engagement_type: str, count: int = 1
    ) -> None:
        metrics = self._metrics.get(post_id)
        if not metrics:
            return
        if engagement_type == "like":
            metrics.likes += count
        elif engagement_type == "comment":
            metrics.comments += count
        elif engagement_type == "share":
            metrics.shares += count
        elif engagement_type == "save":
            metrics.saves += count
        elif engagement_type == "click":
            metrics.clicks += count
        elif engagement_type == "video_view":
            metrics.video_views += count

    def get_post_metrics(self, post_id: str) -> Optional[SocialMetrics]:
        return self._metrics.get(post_id)

    def get_platform_summary(
        self, platform: Optional[SocialPlatform] = None
    ) -> Dict[str, Any]:
        summaries: Dict[str, Dict[str, Any]] = {}
        for post_id, metrics in self._metrics.items():
            if platform and metrics.platform != platform:
                continue
            plat = metrics.platform.value
            if plat not in summaries:
                summaries[plat] = {
                    "total_posts": 0,
                    "total_impressions": 0,
                    "total_engagement": 0,
                    "total_reach": 0,
                }
            summaries[plat]["total_posts"] += 1
            summaries[plat]["total_impressions"] += metrics.impressions
            summaries[plat]["total_engagement"] += metrics.total_engagement
            summaries[plat]["total_reach"] += metrics.reach
        for plat, data in summaries.items():
            data["avg_engagement_rate"] = (
                data["total_engagement"] / data["total_reach"]
                if data["total_reach"] else 0
            )
        return summaries

    def get_top_posts(self, metric: str = "engagement", limit: int = 5) -> List[Dict[str, Any]]:
        scored: List[Tuple[str, float]] = []
        for post_id, m in self._metrics.items():
            if metric == "engagement":
                score = float(m.total_engagement)
            elif metric == "impressions":
                score = float(m.impressions)
            elif metric == "clicks":
                score = float(m.clicks)
            elif metric == "reach":
                score = float(m.reach)
            else:
                score = 0.0
            scored.append((post_id, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        results: List[Dict[str, Any]] = []
        for post_id, score in scored[:limit]:
            post = self._posts.get(post_id)
            m = self._metrics.get(post_id)
            results.append({
                "post_id": post_id,
                "platform": m.platform.value if m else "",
                "score": score,
                "content_preview": post.content[:100] if post else "",
            })
        return results


class SEOManager:
    """SEO tracking, auditing, and optimization."""

    def __init__(self) -> None:
        self._keywords: Dict[str, SEOKeyword] = {}
        self._audit_history: List[SEOAuditResult] = []
        self._site_urls: List[str] = []
        logger.info("SEOManager initialized")

    def add_keyword(
        self,
        keyword: str,
        url: str,
        position: int = 0,
        search_volume: int = 0,
    ) -> SEOKeyword:
        kw = SEOKeyword(
            keyword=keyword,
            url=url,
            position=position,
            search_volume=search_volume,
            last_checked=datetime.now(),
        )
        self._keywords[kw.keyword_id] = kw
        return kw

    def update_keyword_position(
        self, keyword_id: str, new_position: int
    ) -> Optional[SEOKeyword]:
        kw = self._keywords.get(keyword_id)
        if not kw:
            return None
        kw.previous_position = kw.position
        kw.position = new_position
        kw.last_checked = datetime.now()
        return kw

    def get_keyword_rankings(
        self, top_n: Optional[int] = None
    ) -> List[SEOKeyword]:
        sorted_kws = sorted(
            self._keywords.values(), key=lambda k: k.position
        )
        return sorted_kws[:top_n] if top_n else sorted_kws

    def get_ranking_changes(self) -> List[Dict[str, Any]]:
        changes: List[Dict[str, Any]] = []
        for kw in self._keywords.values():
            delta = kw.position_change
            if delta != 0:
                changes.append({
                    "keyword": kw.keyword,
                    "previous": kw.previous_position,
                    "current": kw.position,
                    "change": delta,
                    "direction": "improved" if delta > 0 else "declined",
                })
        changes.sort(key=lambda c: abs(c["change"]), reverse=True)
        return changes

    def run_site_audit(self, domain: str) -> SEOAuditResult:
        pages_crawled = len(self._site_urls) or 50
        import random
        audit = SEOAuditResult(
            domain=domain,
            pages_crawled=pages_crawled,
            overall_score=round(random.uniform(60, 95), 1),
            page_speed_score=round(random.uniform(50, 100), 1),
            mobile_score=round(random.uniform(60, 100), 1),
            seo_score=round(random.uniform(55, 95), 1),
            accessibility_score=round(random.uniform(65, 100), 1),
            issues_critical=random.randint(0, 5),
            issues_warning=random.randint(3, 15),
            issues_info=random.randint(5, 25),
        )
        audit.recommendations = [
            "Optimize meta descriptions for pages with missing content",
            "Compress images to improve page speed scores",
            "Add structured data markup to product pages",
            "Fix broken internal links",
            "Improve mobile touch target sizes",
        ]
        self._audit_history.append(audit)
        return audit

    def get_seo_scorecard(self) -> Dict[str, Any]:
        total_kws = len(self._keywords)
        top_10 = sum(1 for kw in self._keywords.values() if kw.is_top_10)
        top_3 = sum(1 for kw in self._keywords.values() if kw.is_top_3)
        total_impressions = sum(kw.impressions for kw in self._keywords.values())
        total_clicks = sum(kw.clicks for kw in self._keywords.values())
        avg_ctr = total_clicks / total_impressions if total_impressions else 0
        return {
            "total_keywords_tracked": total_kws,
            "keywords_in_top_10": top_10,
            "keywords_in_top_3": top_3,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "average_ctr": round(avg_ctr, 4),
            "last_audit_score": (
                self._audit_history[-1].overall_score
                if self._audit_history else 0
            ),
        }


# ---------------------------------------------------------------------------
# Main Agent Orchestrator
# ---------------------------------------------------------------------------

class DigitalMarketingAgent:
    """Top-level orchestrator for all digital marketing operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._campaign_manager = CampaignManager()
        self._channel_strategy = ChannelStrategyEngine()
        self._analytics = PerformanceAnalytics()
        self._attribution = AttributionEngine()
        self._email_engine = EmailMarketingEngine()
        self._social_manager = SocialMediaManager()
        self._seo_manager = SEOManager()
        logger.info("DigitalMarketingAgent initialized")

    @property
    def campaign_manager(self) -> CampaignManager:
        return self._campaign_manager

    @property
    def channel_strategy(self) -> ChannelStrategyEngine:
        return self._channel_strategy

    @property
    def analytics(self) -> PerformanceAnalytics:
        return self._analytics

    @property
    def attribution_engine(self) -> AttributionEngine:
        return self._attribution

    @property
    def email_engine(self) -> EmailMarketingEngine:
        return self._email_engine

    @property
    def social_manager(self) -> SocialMediaManager:
        return self._social_manager

    @property
    def seo_manager(self) -> SEOManager:
        return self._seo_manager

    def create_full_campaign(
        self,
        name: str,
        objective: ObjectiveType,
        channels: List[ChannelType],
        budget: float,
        audience: AudienceDefinition,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        campaign = self._campaign_manager.create_campaign(
            name=name,
            objective=objective,
            channels=channels,
            budget_total=budget,
            start_date=start_date,
            end_date=end_date,
        )
        strategy = self._channel_strategy.develop_strategy(
            objective=objective,
            total_budget=budget,
            target_audience=audience,
            preferred_channels=channels,
        )
        return {
            "campaign": {
                "id": campaign.campaign_id,
                "name": campaign.name,
                "status": campaign.status.value,
            },
            "strategy": strategy,
        }

    def get_marketing_dashboard(self) -> Dict[str, Any]:
        dashboard = self._analytics.create_dashboard()
        email_summary = {
            "total_campaigns": len(self._email_engine._campaigns),
            "total_sent": sum(
                m.sent for m in self._email_engine._metrics.values()
            ),
        }
        social_summary = self._social_manager.get_platform_summary()
        seo_scorecard = self._seo_manager.get_seo_scorecard()
        return {
            "campaigns": {
                "total": len(self._campaign_manager._campaigns),
                "active": len(self._campaign_manager.list_campaigns(CampaignStatus.ACTIVE)),
            },
            "performance": {
                "total_spend": dashboard.total_spend,
                "total_revenue": dashboard.total_revenue,
                "overall_roas": dashboard.overall_roas,
                "total_conversions": dashboard.total_conversions,
            },
            "email": email_summary,
            "social": social_summary,
            "seo": seo_scorecard,
            "alerts": dashboard.alerts,
            "generated_at": datetime.now().isoformat(),
        }

    def run_attribution_analysis(
        self, model: AttributionModel = AttributionModel.LINEAR
    ) -> Dict[str, Any]:
        result = self._attribution.compute_attribution(model)
        comparison = self._attribution.compare_models()
        return {
            "primary_model": result.model.value,
            "channel_credits": result.channel_credits,
            "total_conversions": result.total_conversions,
            "total_revenue": round(result.total_revenue, 2),
            "roas": round(result.roas, 2),
            "model_comparison": {
                m: {"roas": round(r.roas, 2), "credits": r.channel_credits}
                for m, r in comparison.items()
            },
        }

    def generate_monthly_report(self) -> Dict[str, Any]:
        dashboard = self._analytics.create_dashboard()
        seo = self._seo_manager.get_seo_scorecard()
        return {
            "report_type": "monthly_marketing",
            "period": datetime.now().strftime("%Y-%m"),
            "executive_summary": {
                "total_spend": dashboard.total_spend,
                "total_revenue": dashboard.total_revenue,
                "roas": dashboard.overall_roas,
                "conversions": dashboard.total_conversions,
            },
            "channel_breakdown": {
                ch.value: {
                    "impressions": p.impressions,
                    "clicks": p.clicks,
                    "conversions": p.conversions,
                    "cost": round(p.cost, 2),
                    "revenue": round(p.revenue, 2),
                    "roas": round(p.roas, 2),
                }
                for ch, p in dashboard.channel_data.items()
            },
            "seo_highlights": seo,
            "recommendations": self._generate_recommendations(dashboard),
        }

    def _generate_recommendations(
        self, dashboard: DashboardSnapshot
    ) -> List[str]:
        recs: List[str] = []
        if dashboard.overall_roas < 2.0:
            recs.append("Overall ROAS is below 2.0x; consider reallocating budget to higher-performing channels.")
        if dashboard.overall_ctr < 0.01:
            recs.append("CTR is below 1%; review ad creatives and targeting.")
        for ch, perf in dashboard.channel_data.items():
            if perf.roas < 1.0 and perf.cost > 100:
                recs.append(
                    f"{ch.value} is spending ${perf.cost:.0f} with ROAS {perf.roas:.2f}x; "
                    "pause or reduce spend on this channel."
                )
        if not recs:
            recs.append("Performance is within healthy ranges. Continue monitoring.")
        return recs

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "DigitalMarketingAgent",
            "campaigns": len(self._campaign_manager._campaigns),
            "email_campaigns": len(self._email_engine._campaigns),
            "social_posts": len(self._social_manager._posts),
            "seo_keywords": len(self._seo_manager._keywords),
            "touchpoints_tracked": len(self._analytics._touchpoints),
        }


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    print("=== Digital Marketing Agent Demo ===")
    agent = DigitalMarketingAgent()

    campaign = agent.campaign_manager.create_campaign(
        name="Summer Sale 2025",
        objective=ObjectiveType.CONVERSION,
        channels=[ChannelType.PAID_SEARCH, ChannelType.EMAIL, ChannelType.PAID_SOCIAL],
        budget_total=50000,
    )
    print(f"Campaign created: {campaign.name} ({campaign.campaign_id})")

    audience = AudienceDefinition(
        segment=AudienceSegment.HIGH_VALUE,
        demographics={"age_range": "25-45", "income": "high"},
        interests=["technology", "fashion"],
        geo_targets=["US", "CA", "UK"],
    )
    strategy = agent.channel_strategy.develop_strategy(
        objective=ObjectiveType.CONVERSION,
        total_budget=50000,
        target_audience=audience,
    )
    print(f"Strategy channels: {strategy['channels']}")

    for ch, alloc in strategy["budget_allocation"].items():
        print(f"  {ch}: ${alloc:,.2f}")

    tp = Touchpoint(
        channel=ChannelType.PAID_SEARCH,
        campaign_id=campaign.campaign_id,
        impressions=50000,
        clicks=2500,
        conversions=125,
        cost=5000,
        revenue=25000,
        visitor_id="v_001",
    )
    agent.analytics.record_touchpoint(tp)

    dashboard = agent.analytics.create_dashboard()
    print(f"ROAS: {dashboard.overall_roas:.2f}x")
    print(f"Conversions: {dashboard.total_conversions}")

    report = agent.generate_monthly_report()
    print(f"Monthly report recommendations: {len(report['recommendations'])}")

    status = agent.get_status()
    print(f"Agent status: {status}")


if __name__ == "__main__":
    main()
