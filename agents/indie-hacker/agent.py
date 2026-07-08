"""
Indie Hacker Agent - Comprehensive Startup Building and Business Growth Platform.

This agent provides end-to-end capabilities for solo entrepreneurs and indie hackers
to build, launch, grow, and monetize their software products. Includes MVP development,
marketing automation, analytics, revenue optimization, customer acquisition, and
operational tools for sustainable business growth.

Key Capabilities:
- MVP Development: Rapid prototyping, technical decisions, development workflows
- Marketing Automation: Campaign management, email sequences, social media automation
- Product Analytics: User behavior tracking, conversion funnels, retention analysis
- Revenue Optimization: Pricing strategies, subscription management, churn reduction
- Customer Acquisition: SEO, content marketing, growth experiments, funnel optimization
- Business Operations: Project management, task tracking, team coordination
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union, Callable
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib
import random
import uuid
import re
from abc import ABC, abstractmethod
import math


class ProjectStatus(Enum):
    """Status of a startup project."""
    IDEA = "idea"
    VALIDATION = "validation"
    MVP = "mvp"
    LAUNCH = "launch"
    GROWTH = "growth"
    SCALE = "scale"
    MAINTENANCE = "maintenance"


class RevenueModel(Enum):
    """Revenue models for indie businesses."""
    SUBSCRIPTION_MONTHLY = "subscription_monthly"
    SUBSCRIPTION_YEARLY = "subscription_yearly"
    ONE_TIME = "one_time"
    FREEMIUM = "freemium"
    MARKETPLACE = "marketplace"
    ADVERTISING = "advertising"
    LICENSING = "licensing"
    CONSULTING = "consulting"
    HYBRID = "hybrid"


class ChurnType(Enum):
    """Types of customer churn."""
    VOLUNTARY = "voluntary"
    INVOLUNTARY = "involuntary"
    ECONOMIC = "economic"
    PRODUCT = "product"
    COMPETITOR = "competitor"


class MarketingChannel(Enum):
    """Marketing channels for customer acquisition."""
    SEO = "seo"
    CONTENT_MARKETING = "content_marketing"
    EMAIL_MARKETING = "email_marketing"
    SOCIAL_MEDIA = "social_media"
    PAID_ADS = "paid_ads"
    REFERRAL = "referral"
    PARTNERSHIPS = "partnerships"
    DIRECT = "direct"
    ORGANIC = "organic"


class TaskPriority(Enum):
    """Priority levels for tasks."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskStatus(Enum):
    """Status of a task."""
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"


@dataclass
class Feature:
    """Product feature definition."""
    name: str
    description: str
    priority: int
    status: str = "planned"
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    user_stories: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class UserPersona:
    """Customer persona for product development."""
    name: str
    demographics: Dict[str, str] = field(default_factory=dict)
    goals: List[str] = field(default_factory=list)
    pain_points: List[str] = field(default_factory=list)
    behaviors: List[str] = field(default_factory=list)
    motivations: List[str] = field(default_factory=list)
    tier: str = "standard"


@dataclass
class MVPComponent:
    """Component of an MVP."""
    name: str
    description: str
    technology: str
    priority: int
    complexity: str = "medium"
    is_essential: bool = True
    dependencies: List[str] = field(default_factory=list)
    estimated_dev_time: str = "1 week"


@dataclass
class GrowthExperiment:
    """A growth experiment to run."""
    name: str
    hypothesis: str
    metric: str
    status: str = "draft"
    sample_size: int = 100
    duration_days: int = 14
    control_conversion: float = 0.0
    variant_conversion: float = 0.0
    confidence_level: float = 0.95
    results: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class EmailCampaign:
    """Email marketing campaign."""
    name: str
    subject: str
    segment: str
    status: str = "draft"
    template: str = ""
    send_time: Optional[datetime] = None
    sent_count: int = 0
    open_rate: float = 0.0
    click_rate: float = 0.0
    conversion_rate: float = 0.0
    sequence_order: int = 0
    automation_triggers: List[str] = field(default_factory=list)


@dataclass
class ContentPiece:
    """Content for marketing."""
    title: str
    type: str
    topic: str
    status: str = "draft"
    keywords: List[str] = field(default_factory=list)
    word_count: int = 0
    seo_score: int = 0
    publish_date: Optional[datetime] = None
    traffic: int = 0
    conversions: int = 0


@dataclass
class PricingTier:
    """Pricing tier configuration."""
    name: str
    price: float
    interval: str = "monthly"
    features: List[str] = field(default_factory=list)
    limits: Dict[str, int] = field(default_factory=dict)
    is_popular: bool = False
    stripe_price_id: str = ""


@dataclass
class Customer:
    """Customer record."""
    email: str
    name: str
    company: str = ""
    plan: str = "free"
    acquired_from: str = ""
    ltv: float = 0.0
    health_score: int = 100
    engagement_score: int = 50
    signup_date: datetime = field(default_factory=datetime.now)
    last_active: Optional[datetime] = None
    churned_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FunnelStage:
    """Conversion funnel stage."""
    name: str
    order: int
    visitors: int = 0
    conversion_rate: float = 0.0
    dropoff_rate: float = 0.0
    avg_time_spent: int = 0


@dataclass
class ProjectConfig:
    """Configuration for an indie hacker project."""
    name: str
    description: str = ""
    status: ProjectStatus = ProjectStatus.IDEA
    revenue_model: RevenueModel = RevenueModel.SUBSCRIPTION_MONTHLY
    target_market: str = ""
    initial_budget: float = 0.0
    monthly_burn: float = 0.0
    runway_months: float = 0.0
    launch_date: Optional[datetime] = None


@dataclass
class Task:
    """Task for project management."""
    id: str
    title: str
    priority: TaskPriority
    status: TaskStatus = TaskStatus.TODO
    project: str = ""
    assignee: str = ""
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class TimeEntry:
    """Time tracking entry."""
    id: str
    task_id: str
    description: str
    hours: float
    date: datetime = field(default_factory=datetime.now)
    billable: bool = True


class MVPTemplate(Enum):
    """MVP development templates."""
    SAAS_APP = "saas_app"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    CONTENT_SITE = "content_site"
    MARKETPLACE = "marketplace"
    ECOMMERCE = "ecommerce"
    TOOL = "tool"
    API_KEY = "api_key"


class SaaSMetricsCalculator:
    """Calculates and projects SaaS business metrics."""

    def __init__(self):
        self.metrics_history: List[Dict] = []

    def calculate_mrr(
        self,
        customers_by_tier: Dict[str, int],
        pricing: Dict[str, float]
    ) -> float:
        """Calculate Monthly Recurring Revenue."""
        mrr = 0.0
        for tier, count in customers_by_tier.items():
            if tier in pricing:
                price = pricing[tier]
                if price > 0:
                    mrr += count * price
        return mrr

    def calculate_arr(self, mrr: float) -> float:
        """Calculate Annual Recurring Revenue."""
        return mrr * 12

    def calculate_ltv(
        self,
        mrr: float,
        churn_rate: float,
        gross_margin: float = 0.80,
        cac: float = 0.0,
        discount_rate: float = 0.10
    ) -> float:
        """Calculate Customer Lifetime Value.

        LTV = (ARPU × Gross Margin) × (1 / Churn Rate) - CAC
        With discounting: LTV = Σ (ARPU × Margin × (1-churn)^t) / (1+discount)^t
        """
        if churn_rate <= 0:
            return float('inf')

        arpu = mrr / max(1, sum(c for c in [100, 50, 25] if c > 0))
        margin = mrr * gross_margin

        ltv_simple = (arpu * margin) / (churn_rate / 100)

        return ltv_simple - cac

    def calculate_churn_rate(
        self,
        customers_start: int,
        customers_end: int,
        new_customers: int
    ) -> float:
        """Calculate monthly churn rate."""
        churned = customers_start + new_customers - customers_end
        if customers_start <= 0:
            return 0.0
        return (churned / customers_start) * 100

    def calculate_net_revenue_churn(
        self,
        mrr_start: float,
        mrr_end: float,
        expansion_mrr: float,
        contraction_mrr: float
    ) -> float:
        """Calculate Net Revenue Churn."""
        if mrr_start <= 0:
            return 0.0
        churned_mrr = mrr_start + expansion_mrr - mrr_end - contraction_mrr
        return (churned_mrr / mrr_start) * 100

    def calculate_quick_ratio(
        self,
        new_mrr: float,
        expansion_mrr: float,
        contraction_mrr: float,
        churned_mrr: float
    ) -> float:
        """Calculate Quick Ratio (efficiency metric)."""
        denominator = contraction_mrr + churned_mrr
        if denominator <= 0:
            return float('inf')
        return (new_mrr + expansion_mrr) / denominator

    def calculate_burn_rate(
        self,
        cash_balance: float,
        months_of_runway: int
    ) -> float:
        """Calculate monthly burn rate."""
        return cash_balance / max(1, months_of_runway)

    def calculate_runway(
        self,
        cash_balance: float,
        monthly_burn: float,
        monthly_revenue: float = 0.0
    ) -> Dict[str, Any]:
        """Calculate runway and burn metrics."""
        net_burn = monthly_burn - monthly_revenue

        if net_burn <= 0:
            return {
                "runway_months": float('inf'),
                "net_burn": 0.0,
                "gross_burn": monthly_burn,
                "is_profitable": True,
                "days_saved": 0
            }

        runway_months = cash_balance / net_burn
        runway_days = int(runway_months * 30)

        return {
            "runway_months": round(runway_months, 1),
            "net_burn": round(net_burn, 2),
            "gross_burn": monthly_burn,
            "is_profitable": False,
            "days_saved": runway_days,
            "burn_rate_percent": round((net_burn / max(1, monthly_burn)) * 100, 1)
        }

    def calculate_unit_economics(
        self,
        mrr: float,
        total_customers: int,
        monthly_cac: float,
        gross_margin: float = 0.80
    ) -> Dict[str, Any]:
        """Calculate unit economics metrics."""
        if total_customers <= 0:
            return {}

        arpu = mrr / total_customers
        ltv = self.calculate_ltv(mrr, 5.0, gross_margin, monthly_cac)
        ltv_cac_ratio = ltv / monthly_cac if monthly_cac > 0 else float('inf')
        payback_months = monthly_cac / (arpu * gross_margin) if arpu > 0 else float('inf')

        return {
            "arpu": round(arpu, 2),
            "ltv": round(ltv, 2),
            "cac": round(monthly_cac, 2),
            "ltv_cac_ratio": round(ltv_cac_ratio, 2),
            "payback_months": round(payback_months, 1),
            "gross_margin_percent": round(gross_margin * 100, 1),
            "margin_dollars": round(arpu * gross_margin, 2)
        }

    def project_growth(
        self,
        current_mrr: float,
        growth_rate_percent: float,
        churn_rate_percent: float,
        months: int
    ) -> List[Dict[str, Any]]:
        """Project MRR growth over time."""
        projections = []
        mrr = current_mrr

        for month in range(1, months + 1):
            new_mrr = mrr * (growth_rate_percent / 100)
            churned_mrr = mrr * (churn_rate_percent / 100)
            mrr = mrr + new_mrr - churned_mrr

            projections.append({
                "month": month,
                "mrr": round(mrr, 2),
                "new_mrr": round(new_mrr, 2),
                "churned_mrr": round(churned_mrr, 2),
                "net_change": round(new_mrr - churned_mrr, 2),
                "arr": round(mrr * 12, 2)
            })

        return projections


class CustomerSegmenter:
    """Segments customers for targeted marketing."""

    def __init__(self):
        self.segments: Dict[str, Dict] = {}

    def create_segment(
        self,
        name: str,
        criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new customer segment."""
        self.segments[name] = {
            "criteria": criteria,
            "customer_ids": [],
            "total_value": 0.0,
            "avg_ltv": 0.0
        }
        return self.segments[name]

    def segment_by_behavior(
        self,
        customers: List[Customer],
        behavior: str,
        threshold: int = 5
    ) -> List[Customer]:
        """Filter customers by behavior."""
        if behavior == "active":
            return [c for c in customers if c.health_score >= 70]
        elif behavior == "engaged":
            return [c for c in customers if c.engagement_score >= 60]
        elif behavior == "at_risk":
            return [c for c in customers if 30 <= c.health_score < 70]
        elif behavior == "churned":
            return [c for c in customers if c.churned_at is not None]
        elif behavior == "power_user":
            return [c for c in customers if c.engagement_score >= 80]
        else:
            return []

    def segment_by_tier(
        self,
        customers: List[Customer],
        tier: str
    ) -> List[Customer]:
        """Filter customers by subscription tier."""
        return [c for c in customers if c.plan == tier]

    def segment_by_recency(
        self,
        customers: List[Customer],
        days: int
    ) -> List[Customer]:
        """Filter customers by last active date."""
        cutoff = datetime.now() - timedelta(days=days)
        return [c for c in customers if c.last_active and c.last_active >= cutoff]

    def calculate_segment_metrics(
        self,
        customers: List[Customer]
    ) -> Dict[str, Any]:
        """Calculate metrics for a customer segment."""
        if not customers:
            return {}

        total_ltv = sum(c.ltv for c in customers)
        avg_health = sum(c.health_score for c in customers) / len(customers)
        avg_engagement = sum(c.engagement_score for c in customers) / len(customers)

        tier_distribution = defaultdict(int)
        for c in customers:
            tier_distribution[c.plan] += 1

        return {
            "count": len(customers),
            "total_ltv": round(total_ltv, 2),
            "avg_ltv": round(total_ltv / len(customers), 2),
            "avg_health_score": round(avg_health, 1),
            "avg_engagement": round(avg_engagement, 1),
            "tier_distribution": dict(tier_distribution)
        }


class ChurnPredictor:
    """Predicts and analyzes customer churn."""

    def __init__(self):
        self.churn_factors: Dict[str, float] = {}
        self.thresholds: Dict[str, int] = {}

    def set_churn_factors(
        self,
        factors: Dict[str, float]
    ) -> None:
        """Set weights for churn prediction factors."""
        self.churn_factors = factors

    def set_thresholds(
        self,
        thresholds: Dict[str, int]
    ) -> None:
        """Set thresholds for churn indicators."""
        self.thresholds = thresholds

    def predict_churn_risk(
        self,
        customer: Customer,
        recent_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Predict churn risk for a customer."""
        risk_score = 0

        if customer.health_score < self.thresholds.get("health_critical", 30):
            risk_score += self.churn_factors.get("health", 30)

        if customer.engagement_score < self.thresholds.get("engagement_low", 40):
            risk_score += self.churn_factors.get("engagement", 20)

        days_inactive = 0
        if customer.last_active:
            days_inactive = (datetime.now() - customer.last_active).days

        if days_inactive > self.thresholds.get("inactivity", 14):
            risk_score += self.churn_factors.get("inactivity", 25)

        risk_level = "low"
        if risk_score >= 70:
            risk_level = "critical"
        elif risk_score >= 50:
            risk_level = "high"
        elif risk_score >= 30:
            risk_level = "medium"

        return {
            "customer_id": customer.email,
            "risk_score": min(100, risk_score),
            "risk_level": risk_level,
            "factors": {
                "health_score": customer.health_score,
                "engagement_score": customer.engagement_score,
                "days_inactive": days_inactive
            },
            "recommendations": self._get_recommendations(risk_level)
        }

    def _get_recommendations(self, risk_level: str) -> List[str]:
        """Get churn prevention recommendations."""
        recommendations = {
            "critical": [
                "Immediate outreach from founder",
                "Schedule personal call within 24 hours",
                "Offer emergency discount or extended trial",
                "Identify and resolve urgent issues"
            ],
            "high": [
                "Personal email from customer success",
                "Send case study of similar success",
                "Offer product training session",
                "Check if they're using key features"
            ],
            "medium": [
                "Automated email with tips and tricks",
                "Highlight new features they haven't used",
                "Send community spotlight or success story",
                "Invite to webinar or event"
            ],
            "low": [
                "Regular newsletter and updates",
                "Feature announcement emails",
                "Community engagement prompts",
                "Referral program invitation"
            ]
        }
        return recommendations.get(risk_level, [])

    def analyze_churn_reasons(
        self,
        churned_customers: List[Customer]
    ) -> Dict[str, Any]:
        """Analyze reasons for customer churn."""
        churn_by_type: Dict[ChurnType, int] = defaultdict(int)

        for customer in churned_customers:
            if customer.churned_at:
                reason = customer.metadata.get("churn_reason", "unknown")
                if "price" in reason.lower():
                    churn_by_type[ChurnType.ECONOMIC] += 1
                elif "competitor" in reason.lower():
                    churn_by_type[ChurnType.COMPETITOR] += 1
                elif "product" in reason.lower():
                    churn_by_type[ChurnType.PRODUCT] += 1
                elif "payment" in reason.lower():
                    churn_by_type[ChurnType.INVOLUNTARY] += 1
                else:
                    churn_by_type[ChurnType.VOLUNTARY] += 1

        total_churned = len(churned_customers)
        distribution = {
            ctype.value: round((count / total_churned) * 100, 1)
            for ctype, count in churn_by_type.items()
        }

        return {
            "total_churned": total_churned,
            "by_type": distribution,
            "top_reasons": sorted(
                distribution.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }


class MarketingAutomationEngine:
    """Automates marketing campaigns and workflows."""

    def __init__(self):
        self.campaigns: Dict[str, EmailCampaign] = {}
        self.sequences: Dict[str, List[EmailCampaign]] = {}
        self.triggers: Dict[str, List[Callable]] = {}
        self.automations: List[Dict] = []

    def create_campaign(
        self,
        name: str,
        subject: str,
        segment: str
    ) -> EmailCampaign:
        """Create a new email campaign."""
        campaign = EmailCampaign(
            name=name,
            subject=subject,
            segment=segment
        )
        self.campaigns[name] = campaign
        return campaign

    def create_sequence(
        self,
        name: str,
        campaigns: List[EmailCampaign]
    ) -> Dict[str, Any]:
        """Create an email automation sequence."""
        for i, campaign in enumerate(campaigns):
            campaign.sequence_order = i + 1

        self.sequences[name] = campaigns
        return {
            "sequence": name,
            "emails": len(campaigns),
            "total_duration_days": sum(c.duration_days for c in campaigns)
        }

    def add_trigger(
        self,
        trigger_name: str,
        action: Callable
    ) -> None:
        """Add an automation trigger."""
        if trigger_name not in self.triggers:
            self.triggers[trigger_name] = []
        self.triggers[trigger_name].append(action)

    def create_automation(
        self,
        name: str,
        trigger: str,
        actions: List[str]
    ) -> Dict[str, Any]:
        """Create a marketing automation workflow."""
        automation = {
            "id": str(uuid.uuid4()),
            "name": name,
            "trigger": trigger,
            "actions": actions,
            "enabled": True,
            "triggered_count": 0,
            "created_at": datetime.now().isoformat()
        }
        self.automations.append(automation)
        return automation

    def launch_campaign(
        self,
        campaign_name: str,
        recipients: List[str]
    ) -> Dict[str, Any]:
        """Launch an email campaign."""
        if campaign_name not in self.campaigns:
            return {"error": "Campaign not found"}

        campaign = self.campaigns[campaign_name]
        campaign.status = "sent"
        campaign.sent_count = len(recipients)
        campaign.send_time = datetime.now()

        estimated_opens = int(campaign.sent_count * campaign.open_rate)
        estimated_clicks = int(estimated_opens * campaign.click_rate)
        estimated_conversions = int(estimated_clicks * campaign.conversion_rate)

        return {
            "campaign": campaign_name,
            "sent": campaign.sent_count,
            "estimated_opens": estimated_opens,
            "estimated_clicks": estimated_clicks,
            "estimated_conversions": estimated_conversions,
            "send_time": campaign.send_time.isoformat()
        }

    def get_campaign_report(
        self,
        campaign_name: str
    ) -> Dict[str, Any]:
        """Get performance report for a campaign."""
        if campaign_name not in self.campaigns:
            return {"error": "Campaign not found"}

        campaign = self.campaigns[campaign_name]

        return {
            "name": campaign.name,
            "status": campaign.status,
            "sent": campaign.sent_count,
            "open_rate": campaign.open_rate,
            "click_rate": campaign.click_rate,
            "conversion_rate": campaign.conversion_rate,
            "revenue_generated": round(campaign.sent_count * campaign.open_rate *
                                     campaign.click_rate * campaign.conversion_rate * 100, 2)
        }


class ContentManager:
    """Manages content marketing and SEO."""

    def __init__(self):
        self.content_pieces: Dict[str, ContentPiece] = {}
        self.keywords: Dict[str, Dict] = {}
        self.editorial_calendar: List[Dict] = []

    def create_content(
        self,
        title: str,
        content_type: str,
        topic: str
    ) -> ContentPiece:
        """Create a new content piece."""
        piece = ContentPiece(
            title=title,
            type=content_type,
            topic=topic
        )
        self.content_pieces[title] = piece
        return piece

    def add_keyword(
        self,
        keyword: str,
        volume: int,
        difficulty: int,
        intent: str = "informational"
    ) -> Dict[str, Any]:
        """Add a keyword to track."""
        self.keywords[keyword] = {
            "volume": volume,
            "difficulty": difficulty,
            "intent": intent,
            "current_rank": 0,
            "best_rank": 0,
            "last_updated": datetime.now().isoformat()
        }
        return self.keywords[keyword]

    def plan_content(
        self,
        topics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Plan content for the editorial calendar."""
        for i, topic in enumerate(topics):
            self.editorial_calendar.append({
                "order": i + 1,
                "title": topic.get("title", ""),
                "type": topic.get("type", "blog"),
                "target_date": topic.get("date", ""),
                "keywords": topic.get("keywords", []),
                "status": "planned",
                "assigned_writer": topic.get("writer", "")
            })

        return {
            "planned": len(topics),
            "calendar": self.editorial_calendar
        }

    def calculate_seo_score(
        self,
        content: ContentPiece
    ) -> Dict[str, Any]:
        """Calculate SEO score for content."""
        score = 0
        max_score = 100

        keyword_bonus = min(30, len(content.keywords) * 10)
        score += keyword_bonus

        word_count_bonus = min(20, content.word_count // 100)
        score += word_count_bonus

        if content.publish_date:
            score += 10

        if content.traffic > 0:
            traffic_bonus = min(20, content.traffic // 100)
            score += traffic_bonus

        if content.conversions > 0:
            score += min(20, content.conversions * 2)

        content.seo_score = score

        return {
            "title": content.title,
            "seo_score": score,
            "breakdown": {
                "keywords": keyword_bonus,
                "word_count": word_count_bonus,
                "published": 10 if content.publish_date else 0,
                "traffic": traffic_bonus if content.traffic > 0 else 0,
                "conversions": min(20, content.conversions * 2) if content.conversions > 0 else 0
            }
        }

    def get_content_performance(
        self,
        content_type: str = ""
    ) -> Dict[str, Any]:
        """Get content performance metrics."""
        pieces = list(self.content_pieces.values())
        if content_type:
            pieces = [p for p in pieces if p.type == content_type]

        total_traffic = sum(p.traffic for p in pieces)
        total_conversions = sum(p.conversions for p in pieces)
        avg_seo_score = sum(p.seo_score for p in pieces) / max(1, len(pieces))

        by_type = defaultdict(list)
        for p in pieces:
            by_type[p.type].append(p.title)

        return {
            "total_pieces": len(pieces),
            "total_traffic": total_traffic,
            "total_conversions": total_conversions,
            "conversion_rate": round(total_conversions / max(1, total_traffic) * 100, 2),
            "avg_seo_score": round(avg_seo_score, 1),
            "by_type": dict(by_type)
        }


class PricingOptimizer:
    """Optimizes pricing strategy for indie products."""

    def __init__(self):
        self.tiers: Dict[str, PricingTier] = {}
        self.price_history: List[Dict] = []

    def add_tier(
        self,
        name: str,
        price: float,
        interval: str = "monthly",
        features: List[str] = None,
        limits: Dict[str, int] = None
    ) -> PricingTier:
        """Add a pricing tier."""
        tier = PricingTier(
            name=name,
            price=price,
            interval=interval,
            features=features or [],
            limits=limits or {}
        )
        self.tiers[name] = tier
        return tier

    def set_popular_tier(self, tier_name: str) -> Dict[str, Any]:
        """Set a tier as the popular option."""
        if tier_name not in self.tiers:
            return {"error": "Tier not found"}

        for name, tier in self.tiers.items():
            tier.is_popular = (name == tier_name)

        return {"tier": tier_name, "is_popular": True}

    def calculate_price_elasticity(
        self,
        current_price: float,
        new_price: float,
        current_demand: int
    ) -> Dict[str, Any]:
        """Estimate demand change with new price."""
        percent_change = (new_price - current_price) / current_price
        elasticity = -1.2
        demand_change = percent_change * elasticity * current_demand
        new_demand = int(current_demand + demand_change)

        revenue_current = current_price * current_demand
        revenue_new = new_price * new_demand

        return {
            "current_price": current_price,
            "new_price": new_price,
            "current_demand": current_demand,
            "estimated_demand": max(0, new_demand),
            "revenue_current": round(revenue_current, 2),
            "revenue_new": round(revenue_new, 2),
            "revenue_change": round(revenue_new - revenue_current, 2),
            "recommendation": "increase" if revenue_new > revenue_current else "keep current"
        }

    def calculate_psychological_price(
        self,
        base_price: float
    ) -> Dict[str, Any]:
        """Calculate psychological pricing points."""
        return {
            "charm_price": round(base_price * 0.95, 2),
            "premium_price": round(base_price * 1.25, 2),
            "enterprise_price": round(base_price * 5, 2),
            "anchor_full": base_price,
            "anchor_discount": round(base_price * 0.80, 2),
            "round_number": round(base_price, 0)
        }

    def compare_competitor_pricing(
        self,
        competitors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare pricing with competitors."""
        if not competitors:
            return {"error": "No competitor data"}

        avg_price = sum(c.get("price", 0) for c in competitors) / len(competitors)
        price_ranges = {
            "lowest": min(c.get("price", 0) for c in competitors),
            "highest": max(c.get("price", 0) for c in competitors),
            "average": round(avg_price, 2)
        }

        position = "mid"
        my_price = avg_price
        for tier in self.tiers.values():
            if tier.price > 0:
                my_price = tier.price
                break

        if my_price < price_ranges["lowest"] * 0.8:
            position = "budget"
        elif my_price > price_ranges["highest"] * 1.2:
            position = "premium"

        return {
            "competitor_count": len(competitors),
            "price_ranges": price_ranges,
            "market_position": position,
            "recommendation": self._get_pricing_recommendation(position, price_ranges)
        }

    def _get_pricing_recommendation(
        self,
        position: str,
        ranges: Dict[str, float]
    ) -> str:
        """Get pricing recommendations based on position."""
        recommendations = {
            "budget": "Your pricing is competitive. Consider adding premium features to justify higher prices.",
            "mid": "You're priced at market rate. Differentiate through features and support.",
            "premium": "You're positioned as premium. Ensure quality and support justify the price."
        }
        return recommendations.get(position, "Review your pricing strategy.")


class GrowthExperimentManager:
    """Manages growth experiments and A/B testing."""

    def __init__(self):
        self.experiments: Dict[str, GrowthExperiment] = {}
        self.results: Dict[str, Dict] = {}

    def create_experiment(
        self,
        name: str,
        hypothesis: str,
        metric: str,
        sample_size: int = 100,
        duration_days: int = 14
    ) -> GrowthExperiment:
        """Create a new growth experiment."""
        experiment = GrowthExperiment(
            name=name,
            hypothesis=hypothesis,
            metric=metric,
            sample_size=sample_size,
            duration_days=duration_days
        )
        self.experiments[name] = experiment
        return experiment

    def start_experiment(self, name: str) -> Dict[str, Any]:
        """Start an experiment."""
        if name not in self.experiments:
            return {"error": "Experiment not found"}

        experiment = self.experiments[name]
        experiment.status = "running"
        experiment.started_at = datetime.now()

        return {
            "experiment": name,
            "status": "started",
            "started_at": experiment.started_at.isoformat(),
            "expected_completion": (
                experiment.started_at + timedelta(days=experiment.duration_days)
            ).isoformat()
        }

    def record_result(
        self,
        experiment_name: str,
        variant: str,
        conversion_rate: float
    ) -> Dict[str, Any]:
        """Record results for an experiment variant."""
        if experiment_name not in self.experiments:
            return {"error": "Experiment not found"}

        experiment = self.experiments[experiment_name]

        if variant == "control":
            experiment.control_conversion = conversion_rate
        elif variant == "variant":
            experiment.variant_conversion = conversion_rate

        return {
            "experiment": experiment_name,
            "variant": variant,
            "conversion_rate": conversion_rate
        }

    def complete_experiment(self, name: str) -> Dict[str, Any]:
        """Complete an experiment and analyze results."""
        if name not in self.experiments:
            return {"error": "Experiment not found"}

        experiment = self.experiments[name]
        experiment.status = "completed"
        experiment.completed_at = datetime.now()

        lift = 0.0
        if experiment.control_conversion > 0:
            lift = ((experiment.variant_conversion - experiment.control_conversion)
                   / experiment.control_conversion) * 100

        winner = "variant" if experiment.variant_conversion > experiment.control_conversion else "control"
        significant = self._is_statistically_significant(
            experiment.control_conversion,
            experiment.variant_conversion,
            experiment.sample_size,
            experiment.confidence_level
        )

        experiment.results = {
            "winner": winner,
            "lift_percent": round(lift, 2),
            "is_significant": significant,
            "confidence_level": experiment.confidence_level,
            "control_rate": experiment.control_conversion,
            "variant_rate": experiment.variant_conversion
        }

        return {
            "experiment": name,
            "winner": winner,
            "lift": f"{lift:+.1f}%",
            "significant": significant,
            "results": experiment.results
        }

    def _is_statistically_significant(
        self,
        control_rate: float,
        variant_rate: float,
        sample_size: int,
        confidence: float
    ) -> bool:
        """Check if results are statistically significant."""
        if control_rate == 0 or variant_rate == 0:
            return False

        pooled_rate = (control_rate + variant_rate) / 2
        se = math.sqrt(pooled_rate * (1 - pooled_rate) * 2 / sample_size)

        if se == 0:
            return False

        z_score = abs(variant_rate - control_rate) / se

        z_thresholds = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        threshold = z_thresholds.get(confidence, 1.96)

        return z_score > threshold

    def get_experiment_summary(self) -> Dict[str, Any]:
        """Get summary of all experiments."""
        running = [e for e in self.experiments.values() if e.status == "running"]
        completed = [e for e in self.experiments.values() if e.status == "completed"]
        draft = [e for e in self.experiments.values() if e.status == "draft"]

        avg_lift = 0.0
        if completed:
            lifts = [e.results.get("lift_percent", 0) for e in completed]
            avg_lift = sum(lifts) / len(lifts)

        return {
            "total": len(self.experiments),
            "running": len(running),
            "completed": len(completed),
            "draft": len(draft),
            "avg_lift_percent": round(avg_lift, 2)
        }


class FunnelAnalyzer:
    """Analyzes conversion funnels."""

    def __init__(self):
        self.funnels: Dict[str, List[FunnelStage]] = {}
        self.attribution_models: Dict[str, Dict] = {}

    def create_funnel(
        self,
        name: str,
        stages: List[Dict[str, Any]]
    ) -> List[FunnelStage]:
        """Create a conversion funnel."""
        funnel = []
        for i, stage_data in enumerate(stages):
            stage = FunnelStage(
                name=stage_data["name"],
                order=stage_data.get("order", i + 1),
                visitors=stage_data.get("visitors", 0)
            )
            funnel.append(stage)

        self.funnels[name] = funnel
        self._calculate_conversion_rates(funnel)

        return funnel

    def _calculate_conversion_rates(self, funnel: List[FunnelStage]) -> None:
        """Calculate conversion and dropoff rates for funnel stages."""
        if not funnel:
            return

        funnel[0].conversion_rate = 100.0

        for i in range(1, len(funnel)):
            if funnel[i - 1].visitors > 0:
                funnel[i].conversion_rate = round(
                    (funnel[i].visitors / funnel[i - 1].visitors) * 100, 2
                )
                funnel[i].dropoff_rate = round(
                    100 - funnel[i].conversion_rate, 2
                )

    def add_funnel_data(
        self,
        funnel_name: str,
        stage_name: str,
        visitors: int
    ) -> Dict[str, Any]:
        """Add data to a funnel stage."""
        if funnel_name not in self.funnels:
            return {"error": "Funnel not found"}

        for stage in self.funnels[funnel_name]:
            if stage.name == stage_name:
                stage.visitors = visitors
                self._calculate_conversion_rates(self.funnels[funnel_name])
                return {"stage": stage_name, "visitors": visitors}

        return {"error": "Stage not found"}

    def analyze_funnel(self, funnel_name: str) -> Dict[str, Any]:
        """Get detailed funnel analysis."""
        if funnel_name not in self.funnels:
            return {"error": "Funnel not found"}

        funnel = self.funnels[funnel_name]

        if not funnel:
            return {"error": "Funnel is empty"}

        first_stage_visitors = funnel[0].visitors
        last_stage_visitors = funnel[-1].visitors

        overall_conversion = 0.0
        if first_stage_visitors > 0:
            overall_conversion = round(
                (last_stage_visitors / first_stage_visitors) * 100, 2
            )

        biggest_dropoff = max(funnel[1:], key=lambda s: s.dropoff_rate)
        best_conversion = max(funnel[1:], key=lambda s: s.conversion_rate)

        return {
            "funnel": funnel_name,
            "stages": len(funnel),
            "first_stage_visitors": first_stage_visitors,
            "last_stage_visitors": last_stage_visitors,
            "overall_conversion_rate": overall_conversion,
            "biggest_dropoff": {
                "stage": biggest_dropoff.name,
                "rate": biggest_dropoff.dropoff_rate
            },
            "best_conversion": {
                "stage": best_conversion.name,
                "rate": best_conversion.conversion_rate
            },
            "stage_details": [
                {
                    "name": s.name,
                    "visitors": s.visitors,
                    "conversion_rate": s.conversion_rate,
                    "dropoff_rate": s.dropoff_rate
                }
                for s in funnel
            ]
        }

    def calculate_attribution(
        self,
        channel: str,
        conversions: int,
        total_conversions: int,
        model: str = "first_touch"
    ) -> Dict[str, Any]:
        """Calculate channel attribution."""
        if model == "first_touch":
            attribution = conversions
        elif model == "last_touch":
            attribution = conversions
        elif model == "linear":
            attribution = conversions / max(1, len(self.attribution_models))
        elif model == "time_decay":
            attribution = conversions * 0.5
        else:
            attribution = conversions

        revenue_attributed = attribution * 100

        return {
            "channel": channel,
            "conversions": conversions,
            "total_conversions": total_conversions,
            "conversion_share": round(conversions / max(1, total_conversions) * 100, 2),
            "model": model,
            "attributed_conversions": attribution,
            "attributed_revenue": round(revenue_attributed, 2)
        }


class ProjectManager:
    """Manages indie hacker projects and tasks."""

    def __init__(self):
        self.projects: Dict[str, Dict] = {}
        self.tasks: Dict[str, Task] = {}
        self.time_entries: List[TimeEntry] = []
        self.current_project: Optional[str] = None

    def create_project(
        self,
        name: str,
        description: str = "",
        status: ProjectStatus = ProjectStatus.IDEA
    ) -> Dict[str, Any]:
        """Create a new project."""
        project = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "status": status,
            "features": [],
            "tasks": [],
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None
        }
        self.projects[name] = project
        return project

    def set_current_project(self, project_name: str) -> Dict[str, Any]:
        """Set the current active project."""
        if project_name not in self.projects:
            return {"error": "Project not found"}

        self.current_project = project_name
        if self.projects[project_name]["started_at"] is None:
            self.projects[project_name]["started_at"] = datetime.now().isoformat()

        return {"project": project_name, "status": "active"}

    def add_task(
        self,
        title: str,
        priority: TaskPriority,
        project: str = "",
        estimated_hours: float = 0.0,
        due_date: Optional[datetime] = None,
        tags: List[str] = None
    ) -> Task:
        """Add a new task."""
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            priority=priority,
            project=project or self.current_project,
            estimated_hours=estimated_hours,
            due_date=due_date,
            tags=tags or []
        )
        self.tasks[task.id] = task
        return task

    def update_task(
        self,
        task_id: str,
        status: TaskStatus = None,
        actual_hours: float = None
    ) -> Dict[str, Any]:
        """Update a task."""
        if task_id not in self.tasks:
            return {"error": "Task not found"}

        task = self.tasks[task_id]

        if status:
            task.status = status
            if status == TaskStatus.DONE:
                task.completed_at = datetime.now()

        if actual_hours is not None:
            task.actual_hours = actual_hours

        return {
            "task_id": task_id,
            "status": task.status.value,
            "completed": task.completed_at is not None
        }

    def log_time(
        self,
        task_id: str,
        description: str,
        hours: float,
        billable: bool = True
    ) -> TimeEntry:
        """Log time for a task."""
        entry = TimeEntry(
            id=str(uuid.uuid4()),
            task_id=task_id,
            description=description,
            hours=hours,
            billable=billable
        )
        self.time_entries.append(entry)
        return entry

    def get_project_report(self, project_name: str) -> Dict[str, Any]:
        """Get project status report."""
        if project_name not in self.projects:
            return {"error": "Project not found"}

        project = self.projects[project_name]
        project_tasks = [t for t in self.tasks.values() if t.project == project_name]

        status_counts = defaultdict(int)
        for task in project_tasks:
            status_counts[task.status.value] += 1

        total_hours_estimated = sum(t.estimated_hours for t in project_tasks)
        total_hours_actual = sum(
            e.hours for e in self.time_entries
            if e.task_id in [t.id for t in project_tasks]
        )

        return {
            "project": project_name,
            "status": project["status"].value if isinstance(project["status"], ProjectStatus) else project["status"],
            "tasks": {
                "total": len(project_tasks),
                "by_status": dict(status_counts)
            },
            "time": {
                "estimated_hours": total_hours_estimated,
                "actual_hours": round(total_hours_actual, 1),
                "efficiency": round(total_hours_actual / max(1, total_hours_estimated) * 100, 1)
            },
            "completion_percent": round(
                status_counts.get("done", 0) / max(1, len(project_tasks)) * 100, 1
            )
        }

    def get_tasks_due_soon(self, days: int = 7) -> List[Task]:
        """Get tasks due within specified days."""
        cutoff = datetime.now() + timedelta(days=days)
        return [
            t for t in self.tasks.values()
            if t.due_date and t.due_date <= cutoff
            and t.status not in [TaskStatus.DONE, TaskStatus.BLOCKED]
        ]


class MVPTemplateEngine:
    """Generates MVP templates and development plans."""

    def __init__(self):
        self.templates: Dict[str, Dict] = {}

    def generate_saas_template(
        self,
        product_name: str,
        core_features: List[str],
        tech_stack: str = "modern"
    ) -> Dict[str, Any]:
        """Generate a SaaS MVP template."""
        essential_features = [
            MVPTemplateComponent(
                name="User Authentication",
                description="Login, signup, password reset",
                priority=1,
                tech_suggestion="Auth0, Firebase, or NextAuth"
            ),
            MVPTemplateComponent(
                name="Dashboard",
                description="Main user dashboard with key metrics",
                priority=2,
                tech_suggestion="React + Recharts"
            ),
            MVPTemplateComponent(
                name="Core Feature 1",
                description=core_features[0] if core_features else "Main value proposition",
                priority=3,
                tech_suggestion="Custom implementation"
            ),
            MVPTemplateComponent(
                name="Settings & Profile",
                description="User settings and profile management",
                priority=4,
                tech_suggestion="React Forms"
            )
        ]

        tech_recommendations = {
            "modern": {
                "frontend": "Next.js + Tailwind CSS",
                "backend": "Node.js + Prisma",
                "database": "PostgreSQL",
                "hosting": "Vercel + Railway",
                "monitoring": "Sentry"
            },
            "minimal": {
                "frontend": "React + Vite",
                "backend": "Supabase",
                "database": "PostgreSQL",
                "hosting": "Vercel",
                "monitoring": "LogRocket"
            },
            "python": {
                "frontend": "React",
                "backend": "FastAPI",
                "database": "PostgreSQL",
                "hosting": "Railway",
                "monitoring": "Sentry"
            }
        }

        timeline_phases = [
            {"phase": "Week 1-2", "goals": ["Setup project", "Authentication", "Database design"]},
            {"phase": "Week 3-4", "goals": ["Core feature", "Dashboard", "API endpoints"]},
            {"phase": "Week 5-6", "goals": ["UI/UX polish", "Testing", "Documentation"]},
            {"phase": "Week 7-8", "goals": ["Launch prep", "Deployment", "Analytics setup"]}
        ]

        return {
            "product": product_name,
            "type": "saas",
            "essential_features": [
                {"name": f.name, "priority": f.priority, "suggestion": f.tech_suggestion}
                for f in essential_features
            ],
            "tech_stack": tech_recommendations.get(tech_stack, tech_recommendations["modern"]),
            "timeline_weeks": 8,
            "timeline_phases": timeline_phases,
            "estimated_budget": {
                "development": "$5000-15000",
                "infrastructure": "$100-500/month",
                "tools": "$50-200/month"
            },
            "launch_checklist": [
                "Domain configured",
                "SSL certificate installed",
                "Error monitoring active",
                "Analytics configured",
                "Terms of service ready",
                "Privacy policy ready",
                "Support process defined"
            ]
        }

    def generate_api_product_template(
        self,
        product_name: str,
        endpoints: List[str]
    ) -> Dict[str, Any]:
        """Generate an API product template."""
        return {
            "product": product_name,
            "type": "api_service",
            "features": {
                "authentication": ["API keys", "OAuth 2.0", "JWT tokens"],
                "rate_limiting": ["Tier-based limits", "Burst protection"],
                "monitoring": ["Usage analytics", "Latency tracking"],
                "documentation": ["OpenAPI spec", "Interactive docs"]
            },
            "endpoints": endpoints,
            "suggested_stack": {
                "framework": "FastAPI or Express",
                "documentation": "Swagger UI + Redoc",
                "testing": "Pytest + Postman",
                "deployment": "AWS Lambda + API Gateway"
            },
            "monetization": {
                "free_tier": "1000 calls/day",
                "basic": "$29/month - 10000 calls/day",
                "pro": "$99/month - 100000 calls/day",
                "enterprise": "Custom pricing"
            },
            "launch_timeline_weeks": 6
        }


@dataclass
class MVPTemplateComponent:
    """MVP template component."""
    name: str
    description: str
    priority: int
    tech_suggestion: str = ""


class IndieHackerAgent:
    """
    Comprehensive Indie Hacker Agent for building and growing software businesses.

    This agent provides end-to-end capabilities for solo entrepreneurs:
    - MVP Development: Templates, tech stack decisions, development workflows
    - Business Metrics: MRR, ARR, LTV, churn, runway calculations
    - Marketing Automation: Campaigns, sequences, growth experiments
    - Content Management: SEO, content planning, performance tracking
    - Customer Management: Segmentation, churn prediction, retention
    - Project Management: Tasks, time tracking, sprint planning
    """

    def __init__(self, config: Optional[ProjectConfig] = None):
        self._config = config
        self._initialized = False

        self.saas_metrics = SaaSMetricsCalculator()
        self.customer_segmenter = CustomerSegmenter()
        self.churn_predictor = ChurnPredictor()
        self.marketing_engine = MarketingAutomationEngine()
        self.content_manager = ContentManager()
        self.pricing_optimizer = PricingOptimizer()
        self.growth_manager = GrowthExperimentManager()
        self.funnel_analyzer = FunnelAnalyzer()
        self.project_manager = ProjectManager()
        self.mvp_engine = MVPTemplateEngine()

        self._setup_defaults()

    def _setup_defaults(self) -> None:
        """Set up default configurations."""
        self.churn_predictor.set_churn_factors({
            "health": 30,
            "engagement": 20,
            "inactivity": 25,
            "support_tickets": 15,
            "payment_failures": 10
        })

        self.churn_predictor.set_thresholds({
            "health_critical": 30,
            "engagement_low": 40,
            "inactivity": 14
        })

        self.pricing_optimizer.add_tier(
            "Free",
            0,
            "monthly",
            ["Basic features", "Limited usage"],
            {"api_calls": 1000}
        )

        self.pricing_optimizer.add_tier(
            "Pro",
            29,
            "monthly",
            ["All features", "Priority support", "Higher limits"],
            {"api_calls": 50000},
            True
        )

        self.pricing_optimizer.add_tier(
            "Business",
            99,
            "monthly",
            ["All Pro features", "Custom integrations", "Dedicated support"],
            {"api_calls": 500000}
        )

    def initialize_project(
        self,
        name: str,
        description: str = "",
        revenue_model: str = "subscription_monthly"
    ) -> Dict[str, Any]:
        """Initialize a new indie hacker project."""
        project = self.project_manager.create_project(
            name=name,
            description=description,
            status=ProjectStatus.IDEA
        )

        self._config = ProjectConfig(
            name=name,
            description=description,
            revenue_model=RevenueModel(revenue_model)
        )

        self._initialized = True

        return {
            "project": name,
            "status": "initialized",
            "revenue_model": revenue_model,
            "next_steps": [
                "Define target market and customer personas",
                "Create MVP feature list",
                "Set up development environment",
                "Plan launch timeline"
            ]
        }

    def calculate_financials(
        self,
        mrr: float,
        churn_rate: float,
        customers: int,
        monthly_cac: float,
        cash_balance: float
    ) -> Dict[str, Any]:
        """Calculate comprehensive business financials."""
        unit_econ = self.saas_metrics.calculate_unit_economics(
            mrr, customers, monthly_cac
        )

        runway = self.saas_metrics.calculate_runway(
            cash_balance, 0, mrr
        )

        projections = self.saas_metrics.project_growth(
            current_mrr=mrr,
            growth_rate_percent=20,
            churn_rate_percent=churn_rate,
            months=12
        )

        return {
            "current": {
                "mrr": mrr,
                "arr": self.saas_metrics.calculate_arr(mrr),
                "churn_rate": churn_rate,
                "customers": customers
            },
            "unit_economics": unit_econ,
            "runway": runway,
            "projections": projections
        }

    def create_mvp_plan(
        self,
        product_name: str,
        product_type: str,
        core_features: List[str]
    ) -> Dict[str, Any]:
        """Create a comprehensive MVP development plan."""
        if product_type == "saas":
            return self.mvp_engine.generate_saas_template(
                product_name=product_name,
                core_features=core_features,
                tech_stack="modern"
            )
        elif product_type == "api":
            return self.mvp_engine.generate_api_product_template(
                product_name=product_name,
                endpoints=core_features
            )
        else:
            return {
                "product": product_name,
                "type": product_type,
                "features": core_features,
                "timeline_weeks": 6,
                "note": "Generic template - consider SaaS or API templates for better results"
            }

    def add_task(
        self,
        title: str,
        priority: str,
        estimated_hours: float = 0.0,
        due_days: int = 0
    ) -> Dict[str, Any]:
        """Add a task to the current project."""
        priority_map = {
            "critical": TaskPriority.CRITICAL,
            "high": TaskPriority.HIGH,
            "medium": TaskPriority.MEDIUM,
            "low": TaskPriority.LOW
        }

        due_date = None
        if due_days > 0:
            due_date = datetime.now() + timedelta(days=due_days)

        task = self.project_manager.add_task(
            title=title,
            priority=priority_map.get(priority.lower(), TaskPriority.MEDIUM),
            estimated_hours=estimated_hours,
            due_date=due_date
        )

        return {
            "task_id": task.id,
            "title": task.title,
            "status": task.status.value,
            "priority": task.priority.name
        }

    def start_growth_experiment(
        self,
        name: str,
        hypothesis: str,
        metric: str,
        sample_size: int = 100
    ) -> Dict[str, Any]:
        """Start a new growth experiment."""
        experiment = self.growth_manager.create_experiment(
            name=name,
            hypothesis=hypothesis,
            metric=metric,
            sample_size=sample_size
        )

        return self.growth_manager.start_experiment(experiment.name)

    def create_email_campaign(
        self,
        name: str,
        subject: str,
        segment: str,
        open_rate: float = 0.2,
        click_rate: float = 0.05
    ) -> Dict[str, Any]:
        """Create an email marketing campaign."""
        campaign = self.marketing_engine.create_campaign(
            name=name,
            subject=subject,
            segment=segment
        )
        campaign.open_rate = open_rate
        campaign.click_rate = click_rate

        return {
            "campaign": name,
            "subject": subject,
            "segment": segment,
            "status": campaign.status
        }

    def get_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive business dashboard."""
        experiments_summary = self.growth_manager.get_experiment_summary()

        return {
            "agent": "IndieHackerAgent",
            "version": "2.0.0",
            "status": "active",
            "initialized": self._initialized,
            "pricing_tiers": len(self.pricing_optimizer.tiers),
            "active_experiments": experiments_summary.get("running", 0),
            "completed_experiments": experiments_summary.get("completed", 0),
            "campaigns": len(self.marketing_engine.campaigns),
            "content_pieces": len(self.content_manager.content_pieces),
            "projects": len(self.project_manager.projects),
            "tasks": len(self.project_manager.tasks),
            "quick_actions": [
                "calculate_financials",
                "create_mvp_plan",
                "add_task",
                "start_growth_experiment",
                "create_email_campaign"
            ]
        }


def main():
    """Main entry point for the Indie Hacker Agent."""
    print("\n" + "="*60)
    print("  Indie Hacker Agent")
    print("  Build, Launch & Grow Your SaaS")
    print("="*60 + "\n")

    agent = IndieHackerAgent()

    init_result = agent.initialize_project(
        name="SaaS Starter",
        description="A minimal viable SaaS product",
        revenue_model="subscription_monthly"
    )
    print("Project Initialization:")
    print(f"  Project: {init_result['project']}")
    print(f"  Status: {init_result['status']}\n")

    mvp_plan = agent.create_mvp_plan(
        product_name="Analytics Dashboard",
        product_type="saas",
        core_features=["Data visualization", "User reports", "Export"]
    )
    print("MVP Plan:")
    print(f"  Product: {mvp_plan['product']}")
    print(f"  Type: {mvp_plan['type']}")
    print(f"  Timeline: {mvp_plan['timeline_weeks']} weeks")
    print(f"  Frontend: {mvp_plan['tech_stack']['frontend']}")
    print(f"  Backend: {mvp_plan['tech_stack']['backend']}\n")

    financials = agent.calculate_financials(
        mrr=5000,
        churn_rate=5.0,
        customers=100,
        monthly_cac=200,
        cash_balance=24000
    )
    print("Financial Summary:")
    print(f"  MRR: ${financials['current']['mrr']:,.2f}")
    print(f"  ARR: ${financials['current']['arr']:,.2f}")
    print(f"  LTV: ${financials['unit_economics']['ltv']:,.2f}")
    print(f"  CAC: ${financials['unit_economics']['cac']:,.2f}")
    print(f"  LTV:CAC Ratio: {financials['unit_economics']['ltv_cac_ratio']:.1f}x")
    print(f"  Runway: {financials['runway']['runway_months']} months\n")

    agent.project_manager.set_current_project("SaaS Starter")
    task1 = agent.add_task("Set up development environment", "high", 4)
    task2 = agent.add_task("Implement user authentication", "critical", 8)
    task3 = agent.add_task("Create database schema", "high", 4)
    task4 = agent.add_task("Build dashboard UI", "medium", 12)
    print("Tasks Created:")
    print(f"  1. {task1['title']} [{task1['priority']}]")
    print(f"  2. {task2['title']} [{task2['priority']}]")
    print(f"  3. {task3['title']} [{task3['priority']}]")
    print(f"  4. {task4['title']} [{task4['priority']}]\n")

    experiment = agent.start_growth_experiment(
        name="CTA Button Color Test",
        hypothesis="Changing the CTA button from blue to green will increase click-through rate by 20%",
        metric="click_through_rate",
        sample_size=500
    )
    print("Growth Experiment Started:")
    print(f"  Name: {experiment['experiment']}")
    print(f"  Status: {experiment['status']}\n")

    dashboard = agent.get_dashboard()
    print("Agent Dashboard:")
    print(f"  Status: {dashboard['status']}")
    print(f"  Pricing Tiers: {dashboard['pricing_tiers']}")
    print(f"  Active Experiments: {dashboard['active_experiments']}")
    print(f"  Campaigns: {dashboard['campaigns']}")
    print(f"  Projects: {dashboard['projects']}")
    print(f"  Tasks: {dashboard['tasks']}\n")


if __name__ == "__main__":
    main()
