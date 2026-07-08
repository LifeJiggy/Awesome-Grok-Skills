"""
Marketing Agent
Marketing strategy, campaign management, audience targeting, budget allocation, attribution, and ROI optimization.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class CampaignStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Channel(Enum):
    EMAIL = "email"
    SOCIAL = "social"
    SEARCH = "search"
    DISPLAY = "display"
    VIDEO = "video"
    SMS = "sms"
    PUSH = "push"
    AFFILIATE = "affiliate"
    CONTENT = "content"
    INFLUENCER = "influencer"


class AttributionModel(Enum):
    FIRST_TOUCH = "first_touch"
    LAST_TOUCH = "last_touch"
    LINEAR = "linear"
    TIME_DECAY = "time_decay"
    POSITION_BASED = "position_based"
    DATA_DRIVEN = "data_driven"


class AudienceType(Enum):
    BEHAVIORAL = "behavioral"
    DEMOGRAPHIC = "demographic"
    GEOGRAPHIC = "geographic"
    PSYCHOGRAPHIC = "psychographic"
    TECHOGRAPHIC = "techographic"
    PREDICTIVE = "predictive"


class FunnelStage(Enum):
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    CONVERSION = "conversion"
    RETENTION = "retention"
    ADVOCACY = "advocacy"


class BudgetStrategy(Enum):
    EQUAL_SPLIT = "equal_split"
    PERFORMANCE_BASED = "performance_based"
    AUDIENCE_SIZE = "audience_size"
    SEASONAL_ADJUST = "seasonal_adjust"
    CUSTOM = "custom"


# ──────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────

@dataclass
class AudienceSegment:
    segment_id: str = field(default_factory=lambda: str(uuid4())[:8])
    name: str = ""
    audience_type: AudienceType = AudienceType.BEHAVIORAL
    criteria: Dict[str, Any] = field(default_factory=dict)
    estimated_size: int = 0
    growth_rate: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)


@dataclass
class Campaign:
    campaign_id: str = field(default_factory=lambda: f"camp_{str(uuid4())[:8]}")
    name: str = ""
    channel: Channel = Channel.EMAIL
    status: CampaignStatus = CampaignStatus.DRAFT
    audience_segments: List[str] = field(default_factory=list)
    content: Dict[str, Any] = field(default_factory=dict)
    budget: float = 0.0
    spend: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)


@dataclass
class ConversionEvent:
    event_id: str = field(default_factory=lambda: str(uuid4())[:8])
    campaign_id: str = ""
    user_id: str = ""
    touchpoint: str = ""
    value: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    channel: Channel = Channel.EMAIL
    funnel_stage: FunnelStage = FunnelStage.AWARENESS


@dataclass
class AttributionResult:
    model: AttributionModel = AttributionModel.LINEAR
    channel_scores: Dict[str, float] = field(default_factory=dict)
    total_conversions: int = 0
    total_revenue: float = 0.0
    confidence: float = 0.0


@dataclass
class BudgetAllocation:
    allocation_id: str = field(default_factory=lambda: str(uuid4())[:8])
    total_budget: float = 0.0
    allocations: Dict[str, float] = field(default_factory=dict)
    strategy: BudgetStrategy = BudgetStrategy.EQUAL_SPLIT
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ROIMetric:
    channel: str = ""
    revenue: float = 0.0
    cost: float = 0.0
    roi: float = 0.0
    roas: float = 0.0
    cpa: float = 0.0
    ltv: float = 0.0
    period: str = ""


@dataclass
class ABTest:
    test_id: str = field(default_factory=lambda: f"test_{str(uuid4())[:8]}")
    name: str = ""
    variants: Dict[str, Any] = field(default_factory=dict)
    status: str = "draft"
    winning_variant: Optional[str] = None
    confidence: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# ──────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────

class MarketingError(Exception):
    """Base marketing agent error."""


class CampaignNotFoundError(MarketingError):
    """Raised when a campaign ID does not exist."""


class InvalidBudgetError(MarketingError):
    """Raised when budget values are invalid."""


class SegmentNotFoundError(MarketingError):
    """Raised when an audience segment does not exist."""


# ──────────────────────────────────────────────
# Audience Manager
# ──────────────────────────────────────────────

class AudienceManager:
    """Create, manage, and evaluate audience segments."""

    def __init__(self) -> None:
        self._segments: Dict[str, AudienceSegment] = {}
        self._segment_combinations: Dict[str, List[str]] = {}

    def create_segment(
        self,
        name: str,
        audience_type: AudienceType,
        criteria: Dict[str, Any],
        estimated_size: int = 0,
        tags: Optional[List[str]] = None,
    ) -> AudienceSegment:
        segment = AudienceSegment(
            name=name,
            audience_type=audience_type,
            criteria=criteria,
            estimated_size=estimated_size,
            tags=tags or [],
        )
        self._segments[segment.segment_id] = segment
        logger.info("Created segment %s (%s)", segment.segment_id, name)
        return segment

    def get_segment(self, segment_id: str) -> AudienceSegment:
        if segment_id not in self._segments:
            raise SegmentNotFoundError(f"Segment {segment_id} not found")
        return self._segments[segment_id]

    def update_segment(self, segment_id: str, **kwargs: Any) -> AudienceSegment:
        segment = self.get_segment(segment_id)
        for key, value in kwargs.items():
            if hasattr(segment, key):
                setattr(segment, key, value)
        logger.info("Updated segment %s", segment_id)
        return segment

    def delete_segment(self, segment_id: str) -> bool:
        if segment_id in self._segments:
            del self._segments[segment_id]
            logger.info("Deleted segment %s", segment_id)
            return True
        return False

    def combine_segments(
        self, name: str, segment_ids: List[str], operation: str = "intersect"
    ) -> AudienceSegment:
        if not all(sid in self._segments for sid in segment_ids):
            raise SegmentNotFoundError("One or more segment IDs not found")
        combined = self.create_segment(
            name=name,
            audience_type=AudienceType.BEHAVIORAL,
            criteria={"operation": operation, "source_segments": segment_ids},
            estimated_size=self._estimate_combined_size(segment_ids, operation),
        )
        self._segment_combinations[combined.segment_id] = segment_ids
        return combined

    def _estimate_combined_size(self, segment_ids: List[str], operation: str) -> int:
        sizes = [self._segments[sid].estimated_size for sid in segment_ids]
        if operation == "intersect":
            return max(1, min(sizes)) if sizes else 0
        elif operation == "union":
            return sum(sizes)
        elif operation == "exclude":
            return max(0, sizes[0] - sum(sizes[1:])) if sizes else 0
        return 0

    def score_segment(self, segment_id: str) -> Dict[str, float]:
        segment = self.get_segment(segment_id)
        size_score = min(1.0, segment.estimated_size / 100_000)
        growth_score = min(1.0, max(0, segment.growth_rate / 50))
        criteria_depth = min(1.0, len(segment.criteria) / 5)
        return {
            "size_score": round(size_score, 3),
            "growth_score": round(growth_score, 3),
            "criteria_depth": round(criteria_depth, 3),
            "overall": round((size_score + growth_score + criteria_depth) / 3, 3),
        }

    def list_segments(self) -> List[AudienceSegment]:
        return list(self._segments.values())


# ──────────────────────────────────────────────
# Campaign Manager
# ──────────────────────────────────────────────

class CampaignManager:
    """Create, launch, pause, and manage marketing campaigns."""

    def __init__(self) -> None:
        self._campaigns: Dict[str, Campaign] = {}
        self._events: List[ConversionEvent] = []
        self._hooks: Dict[str, List[Callable]] = {
            "on_launch": [],
            "on_pause": [],
            "on_complete": [],
        }

    def create_campaign(
        self,
        name: str,
        channel: Channel,
        audience_segments: List[str],
        content: Dict[str, Any],
        budget: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> Campaign:
        if budget < 0:
            raise InvalidBudgetError("Budget must be non-negative")
        campaign = Campaign(
            name=name,
            channel=channel,
            audience_segments=audience_segments,
            content=content,
            budget=budget,
            start_date=start_date,
            end_date=end_date,
            tags=tags or [],
        )
        self._campaigns[campaign.campaign_id] = campaign
        logger.info("Created campaign %s (%s)", campaign.campaign_id, name)
        return campaign

    def get_campaign(self, campaign_id: str) -> Campaign:
        if campaign_id not in self._campaigns:
            raise CampaignNotFoundError(f"Campaign {campaign_id} not found")
        return self._campaigns[campaign_id]

    def update_campaign(self, campaign_id: str, **kwargs: Any) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        for key, value in kwargs.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)
        logger.info("Updated campaign %s", campaign_id)
        return campaign

    def launch_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if campaign.status not in (CampaignStatus.DRAFT, CampaignStatus.SCHEDULED):
            raise MarketingError(f"Cannot launch campaign in {campaign.status.value} state")
        campaign.status = CampaignStatus.ACTIVE
        campaign.start_date = datetime.now()
        self._fire_hooks("on_launch", campaign)
        logger.info("Launched campaign %s", campaign_id)
        return campaign

    def pause_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if campaign.status != CampaignStatus.ACTIVE:
            raise MarketingError(f"Cannot pause campaign in {campaign.status.value} state")
        campaign.status = CampaignStatus.PAUSED
        self._fire_hooks("on_pause", campaign)
        logger.info("Paused campaign %s", campaign_id)
        return campaign

    def resume_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if campaign.status != CampaignStatus.PAUSED:
            raise MarketingError("Campaign is not paused")
        campaign.status = CampaignStatus.ACTIVE
        logger.info("Resumed campaign %s", campaign_id)
        return campaign

    def complete_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        campaign.status = CampaignStatus.COMPLETED
        campaign.end_date = datetime.now()
        self._fire_hooks("on_complete", campaign)
        logger.info("Completed campaign %s", campaign_id)
        return campaign

    def record_conversion(self, event: ConversionEvent) -> None:
        self._events.append(event)
        logger.debug("Recorded conversion %s for campaign %s", event.event_id, event.campaign_id)

    def get_conversions(self, campaign_id: str) -> List[ConversionEvent]:
        return [e for e in self._events if e.campaign_id == campaign_id]

    def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self.get_campaign(campaign_id)
        conversions = self.get_conversions(campaign_id)
        total_value = sum(c.value for c in conversions)
        return {
            "campaign_id": campaign_id,
            "name": campaign.name,
            "status": campaign.status.value,
            "budget": campaign.budget,
            "spend": campaign.spend,
            "conversions": len(conversions),
            "revenue": total_value,
            "roi": ((total_value - campaign.spend) / campaign.spend * 100) if campaign.spend > 0 else 0,
            "roas": (total_value / campaign.spend) if campaign.spend > 0 else 0,
            "cpa": (campaign.spend / len(conversions)) if conversions else 0,
        }

    def list_campaigns(self, status: Optional[CampaignStatus] = None) -> List[Campaign]:
        campaigns = list(self._campaigns.values())
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        return campaigns

    def register_hook(self, event: str, callback: Callable) -> None:
        if event in self._hooks:
            self._hooks[event].append(callback)

    def _fire_hooks(self, event: str, campaign: Campaign) -> None:
        for cb in self._hooks.get(event, []):
            try:
                cb(campaign)
            except Exception:
                logger.exception("Hook %s failed for campaign %s", event, campaign.campaign_id)


# ──────────────────────────────────────────────
# Budget Allocator
# ──────────────────────────────────────────────

class BudgetAllocator:
    """Allocate and optimize marketing budgets across channels."""

    def __init__(self) -> None:
        self._allocations: Dict[str, BudgetAllocation] = {}
        self._performance_history: Dict[str, List[ROIMetric]] = {}

    def create_allocation(
        self,
        total_budget: float,
        channel_budgets: Dict[str, float],
        strategy: BudgetStrategy = BudgetStrategy.EQUAL_SPLIT,
    ) -> BudgetAllocation:
        if total_budget < 0:
            raise InvalidBudgetError("Total budget must be non-negative")
        total_allocated = sum(channel_budgets.values())
        if total_allocated > total_budget:
            raise InvalidBudgetError(f"Allocated {total_allocated} exceeds budget {total_budget}")
        allocation = BudgetAllocation(
            total_budget=total_budget,
            allocations=channel_budgets,
            strategy=strategy,
        )
        self._allocations[allocation.allocation_id] = allocation
        logger.info("Created budget allocation %s", allocation.allocation_id)
        return allocation

    def equal_split(self, total_budget: float, channels: List[str]) -> Dict[str, float]:
        if not channels:
            return {}
        per_channel = total_budget / len(channels)
        return {ch: round(per_channel, 2) for ch in channels}

    def performance_based_split(
        self, total_budget: float, channel_rois: Dict[str, float]
    ) -> Dict[str, float]:
        total_roi = sum(max(0, v) for v in channel_rois.values())
        if total_roi == 0:
            return self.equal_split(total_budget, list(channel_rois.keys()))
        return {
            ch: round(total_budget * (max(0, roi) / total_roi), 2)
            for ch, roi in channel_rois.items()
        }

    def record_performance(self, channel: str, metric: ROIMetric) -> None:
        self._performance_history.setdefault(channel, []).append(metric)

    def get_channel_roi(self, channel: str) -> Dict[str, float]:
        metrics = self._performance_history.get(channel, [])
        if not metrics:
            return {"roi": 0.0, "roas": 0.0, "cpa": 0.0}
        total_revenue = sum(m.revenue for m in metrics)
        total_cost = sum(m.cost for m in metrics)
        return {
            "roi": ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            "roas": (total_revenue / total_cost) if total_cost > 0 else 0,
            "cpa": (total_cost / len(metrics)) if metrics else 0,
        }

    def recommend_reallocation(self) -> Dict[str, Any]:
        recommendations: List[Dict[str, Any]] = []
        for channel, metrics in self._performance_history.items():
            if not metrics:
                continue
            latest = metrics[-1]
            if latest.roi < 50:
                recommendations.append({
                    "channel": channel,
                    "action": "reduce",
                    "reason": f"ROI of {latest.roi:.1f}% is below threshold",
                })
            elif latest.roi > 200:
                recommendations.append({
                    "channel": channel,
                    "action": "increase",
                    "reason": f"ROI of {latest.roi:.1f}% exceeds target",
                })
        return {"recommendations": recommendations}

    def list_allocations(self) -> List[BudgetAllocation]:
        return list(self._allocations.values())


# ──────────────────────────────────────────────
# Attribution Engine
# ──────────────────────────────────────────────

class AttributionEngine:
    """Calculate channel attribution using various models."""

    def __init__(self, model: AttributionModel = AttributionModel.LINEAR) -> None:
        self.model = model
        self._touchpoints: Dict[str, List[Dict[str, Any]]] = {}

    def add_touchpoint(
        self,
        user_id: str,
        channel: str,
        timestamp: datetime,
        value: float = 0.0,
        position: int = 0,
    ) -> None:
        self._touchpoints.setdefault(user_id, []).append({
            "channel": channel,
            "timestamp": timestamp,
            "value": value,
            "position": position,
        })

    def calculate_attribution(self, user_id: str) -> AttributionResult:
        touchpoints = sorted(
            self._touchpoints.get(user_id, []), key=lambda t: t["timestamp"]
        )
        if not touchpoints:
            return AttributionResult(model=self.model)
        if self.model == AttributionModel.FIRST_TOUCH:
            scores = self._first_touch(touchpoints)
        elif self.model == AttributionModel.LAST_TOUCH:
            scores = self._last_touch(touchpoints)
        elif self.model == AttributionModel.LINEAR:
            scores = self._linear(touchpoints)
        elif self.model == AttributionModel.TIME_DECAY:
            scores = self._time_decay(touchpoints)
        elif self.model == AttributionModel.POSITION_BASED:
            scores = self._position_based(touchpoints)
        else:
            scores = self._linear(touchpoints)
        total_revenue = touchpoints[-1]["value"] if touchpoints else 0
        return AttributionResult(
            model=self.model,
            channel_scores=scores,
            total_conversions=len(touchpoints),
            total_revenue=total_revenue,
            confidence=self._compute_confidence(touchpoints),
        )

    def _first_touch(self, touchpoints: List[Dict]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        if touchpoints:
            ch = touchpoints[0]["channel"]
            scores[ch] = 1.0
        return scores

    def _last_touch(self, touchpoints: List[Dict]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        if touchpoints:
            ch = touchpoints[-1]["channel"]
            scores[ch] = 1.0
        return scores

    def _linear(self, touchpoints: List[Dict]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        weight = 1.0 / len(touchpoints) if touchpoints else 0
        for tp in touchpoints:
            scores[tp["channel"]] = scores.get(tp["channel"], 0) + weight
        return scores

    def _time_decay(self, touchpoints: List[Dict]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        if not touchpoints:
            return scores
        decay_factor = 0.7
        latest = touchpoints[-1]["timestamp"]
        for i, tp in enumerate(touchpoints):
            time_diff = (latest - tp["timestamp"]).total_seconds() / 86400
            weight = decay_factor ** time_diff
            scores[tp["channel"]] = scores.get(tp["channel"], 0) + weight
        total = sum(scores.values()) or 1
        return {k: v / total for k, v in scores.items()}

    def _position_based(self, touchpoints: List[Dict]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        if not touchpoints:
            return scores
        n = len(touchpoints)
        if n == 1:
            scores[touchpoints[0]["channel"]] = 1.0
            return scores
        first_weight = 0.4
        last_weight = 0.4
        middle_weight = 0.2
        scores[touchpoints[0]["channel"]] = first_weight
        scores[touchpoints[-1]["channel"]] = scores.get(touchpoints[-1]["channel"], 0) + last_weight
        mid = middle_weight / max(1, n - 2)
        for tp in touchpoints[1:-1]:
            scores[tp["channel"]] = scores.get(tp["channel"], 0) + mid
        return scores

    def _compute_confidence(self, touchpoints: List[Dict]) -> float:
        if len(touchpoints) < 2:
            return 0.5
        channels = [tp["channel"] for tp in touchpoints]
        unique = len(set(channels))
        return round(min(1.0, unique / len(touchpoints)), 3)

    def get_aggregated_attribution(self) -> Dict[str, float]:
        aggregated: Dict[str, float] = {}
        count = 0
        for user_id in self._touchpoints:
            result = self.calculate_attribution(user_id)
            for ch, score in result.channel_scores.items():
                aggregated[ch] = aggregated.get(ch, 0) + score
            count += 1
        if count > 0:
            aggregated = {k: v / count for k, v in aggregated.items()}
        return aggregated


# ──────────────────────────────────────────────
# Content Generator
# ──────────────────────────────────────────────

class ContentGenerator:
    """Generate marketing content using templates and brand voice."""

    def __init__(self) -> None:
        self._templates: Dict[str, str] = {}
        self._brand_voice: Dict[str, Any] = {"tone": "professional", "keywords": []}

    def set_brand_voice(self, tone: str, keywords: Optional[List[str]] = None) -> None:
        self._brand_voice = {"tone": tone, "keywords": keywords or []}

    def add_template(self, template_id: str, template: str) -> None:
        self._templates[template_id] = template

    def render(self, template_id: str, variables: Dict[str, str]) -> str:
        if template_id not in self._templates:
            raise ValueError(f"Template {template_id} not found")
        result = self._templates[template_id]
        for key, value in variables.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result

    def generate_email(self, subject: str, body: str, variables: Dict[str, str]) -> Dict[str, str]:
        return {
            "subject": self.render(subject, variables),
            "body": self.render(body, variables),
            "preview": variables.get("preview", subject[:50]),
        }

    def generate_social_post(self, platform: str, message: str, include_cta: bool = True) -> str:
        post = message
        if include_cta:
            ctas = {"twitter": "Learn more", "linkedin": "Read more", "instagram": "Link in bio"}
            post += f"\n\n{ctas.get(platform, 'Learn more')}"
        limits = {"twitter": 280, "linkedin": 3000, "instagram": 2200}
        max_len = limits.get(platform, 280)
        if len(post) > max_len:
            post = post[: max_len - 3] + "..."
        return post

    def ab_variants(self, base_content: str, variations: int = 2) -> List[Dict[str, str]]:
        variants = []
        for i in range(variations):
            variants.append({"variant_id": f"variant_{chr(65 + i)}", "content": base_content})
        return variants


# ──────────────────────────────────────────────
# Analytics Dashboard
# ──────────────────────────────────────────────

class AnalyticsDashboard:
    """Track events, manage goals, and generate reports."""

    def __init__(self) -> None:
        self._events: List[Dict[str, Any]] = []
        self._goals: Dict[str, Dict[str, Any]] = {}

    def track_event(self, event_type: str, properties: Dict[str, Any]) -> None:
        self._events.append({
            "type": event_type,
            "properties": properties,
            "timestamp": datetime.now(),
        })

    def set_goal(self, goal_id: str, metric: str, target: float, period: str = "monthly") -> None:
        self._goals[goal_id] = {
            "metric": metric,
            "target": target,
            "current": 0,
            "period": period,
        }

    def update_goal(self, goal_id: str, value: float) -> None:
        if goal_id in self._goals:
            self._goals[goal_id]["current"] = value

    def get_goal_status(self) -> List[Dict[str, Any]]:
        return [
            {
                "goal_id": gid,
                "metric": g["metric"],
                "target": g["target"],
                "current": g["current"],
                "progress": (g["current"] / g["target"] * 100) if g["target"] > 0 else 0,
            }
            for gid, g in self._goals.items()
        ]

    def generate_report(self, days: int = 30) -> Dict[str, Any]:
        since = datetime.now() - timedelta(days=days)
        recent = [e for e in self._events if e["timestamp"] >= since]
        by_type: Dict[str, int] = {}
        for e in recent:
            by_type[e["type"]] = by_type.get(e["type"], 0) + 1
        return {
            "period_days": days,
            "total_events": len(recent),
            "events_by_type": by_type,
            "goals": self.get_goal_status(),
        }

    def get_funnel(self, stages: List[str]) -> Dict[str, Any]:
        counts: Dict[str, int] = {}
        for e in self._events:
            stage = e["properties"].get("stage", "")
            if stage in stages:
                counts[stage] = counts.get(stage, 0) + 1
        funnel = []
        for i, stage in enumerate(stages):
            current = counts.get(stage, 0)
            prev = counts.get(stages[i - 1], current) if i > 0 else current
            conversion = (current / prev * 100) if prev > 0 else 0
            funnel.append({"stage": stage, "count": current, "conversion_rate": round(conversion, 2)})
        return {"funnel": funnel}


# ──────────────────────────────────────────────
# SEO Analyzer
# ──────────────────────────────────────────────

class SEOAnalyzer:
    """Analyze content for search engine optimization."""

    def __init__(self) -> None:
        self._keyword_data: Dict[str, Dict[str, Any]] = {}

    def analyze_keyword(self, keyword: str, content: str) -> Dict[str, Any]:
        content_lower = content.lower()
        kw_lower = keyword.lower()
        occurrences = content_lower.count(kw_lower)
        words = content_lower.split()
        density = (occurrences * len(kw_lower.split()) / len(words) * 100) if words else 0
        suggestions = []
        if occurrences == 0:
            suggestions.append("Add keyword to content")
        if density < 0.5:
            suggestions.append("Increase keyword density")
        elif density > 3.0:
            suggestions.append("Reduce keyword density to avoid over-optimization")
        return {
            "keyword": keyword,
            "occurrences": occurrences,
            "density": round(density, 2),
            "suggestions": suggestions,
        }

    def serp_preview(self, title: str, meta_description: str, url: str, keyword: str) -> Dict[str, Any]:
        return {
            "title": title[:60] + "..." if len(title) > 60 else title,
            "url": url,
            "description": meta_description[:160] + "..." if len(meta_description) > 160 else meta_description,
            "keyword_in_title": keyword.lower() in title.lower(),
            "keyword_in_description": keyword.lower() in meta_description.lower(),
            "title_length": len(title),
            "description_length": len(meta_description),
        }

    def content_score(self, title: str, body: str, keyword: str) -> Dict[str, Any]:
        title_analysis = self.analyze_keyword(keyword, title)
        body_analysis = self.analyze_keyword(keyword, body)
        title_ok = 30 <= len(title) <= 60
        desc_score = 1.0 if title_ok else 0.5
        kw_score = min(1.0, body_analysis["density"] / 2.0)
        overall = round((desc_score + kw_score) / 2, 3)
        return {
            "title_score": title_analysis,
            "body_score": body_analysis,
            "title_length_ok": title_ok,
            "overall_score": overall,
        }


# ──────────────────────────────────────────────
# Marketing Agent (orchestrator)
# ──────────────────────────────────────────────

class MarketingAgent:
    """Top-level orchestrator that exposes all marketing capabilities."""

    def __init__(self) -> None:
        self.audience = AudienceManager()
        self.campaigns = CampaignManager()
        self.budget = BudgetAllocator()
        self.attribution = AttributionEngine()
        self.content = ContentGenerator()
        self.analytics = AnalyticsDashboard()
        self.seo = SEOAnalyzer()
        logger.info("MarketingAgent initialized")

    def full_campaign_lifecycle(
        self,
        name: str,
        channel: Channel,
        segment_ids: List[str],
        budget: float,
        content: Dict[str, str],
    ) -> Dict[str, Any]:
        campaign = self.campaigns.create_campaign(
            name=name,
            channel=channel,
            audience_segments=segment_ids,
            content=content,
            budget=budget,
        )
        self.campaigns.launch_campaign(campaign.campaign_id)
        metrics = self.campaigns.get_campaign_metrics(campaign.campaign_id)
        self.campaigns.complete_campaign(campaign.campaign_id)
        return {"campaign_id": campaign.campaign_id, "metrics": metrics}

    def run_attribution_analysis(self) -> Dict[str, float]:
        return self.attribution.get_aggregated_attribution()

    def optimize_budget(self) -> Dict[str, Any]:
        return self.budget.recommend_reallocation()

    def generate_dashboard_report(self) -> Dict[str, Any]:
        return self.analytics.generate_report()


# ──────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = MarketingAgent()

    seg = agent.audience.create_segment(
        name="Young Professionals",
        audience_type=AudienceType.DEMOGRAPHIC,
        criteria={"age_range": "25-35", "location": "urban"},
        estimated_size=50000,
    )
    print(f"Segment: {seg.segment_id}, Size: {seg.estimated_size}")

    campaign = agent.campaigns.create_campaign(
        name="Summer Sale 2025",
        channel=Channel.EMAIL,
        audience_segments=[seg.segment_id],
        content={"subject": "Summer Sale - 50% Off!", "body": "Shop now"},
        budget=5000,
    )
    agent.campaigns.launch_campaign(campaign.campaign_id)
    print(f"Campaign: {campaign.campaign_id}, Status: {campaign.status.value}")

    allocation = agent.budget.create_allocation(
        total_budget=10000,
        channel_budgets={"email": 3000, "social": 3000, "search": 4000},
        strategy=Strategy.PERFORMANCE_BASED,
    )
    print(f"Allocation: {allocation.allocation_id}")

    agent.content.set_brand_voice("friendly", ["summer", "sale"])
    email = agent.content.generate_email(
        "Hi {{NAME}}", "Check out our {{PRODUCT}}!", {"NAME": "John", "PRODUCT": "Summer Collection"}
    )
    print(f"Email subject: {email['subject']}")

    seo = agent.seo.analyze_keyword("marketing", "Marketing is essential for growth.")
    print(f"Keyword density: {seo['density']}%")

    report = agent.analytics.generate_report()
    print(f"Report events: {report['total_events']}")
