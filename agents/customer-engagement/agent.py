"""Customer Engagement Agent - Omnichannel Customer Engagement Platform.

Comprehensive framework for customer engagement strategies including
omnichannel communication, personalization, lifecycle marketing,
campaign management, and retention optimization.

Features:
- Omnichannel message orchestration (email, SMS, push, in-app, social)
- Customer segmentation and micro-segmentation
- Behavioral tracking and event processing
- Campaign creation and A/B testing
- Personalization engine with recommendation logic
- Journey mapping and automation
- Engagement scoring and analytics
- Multi-touch attribution
- Content personalization
- Real-time trigger processing
- Webhook integration for external systems
- Feedback collection and sentiment analysis
- Channel performance analytics
- Dynamic audience building
"""

import asyncio
import hashlib
import json
import logging
import os
import random
import statistics
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import (
    Any, Callable, Coroutine, Dict, List, Optional, Set, Tuple, Union,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("customer_engagement_agent")

# =============================================================================
# ENUMS
# =============================================================================

class ChannelType(Enum):
    EMAIL = auto()
    SMS = auto()
    PUSH_NOTIFICATION = auto()
    IN_APP = auto()
    SOCIAL_FACEBOOK = auto()
    SOCIAL_TWITTER = auto()
    SOCIAL_INSTAGRAM = auto()
    WEBHOOK = auto()
    DIRECT_MAIL = auto()
    chat = auto()


class MessageType(Enum):
    TRANSACTIONAL = auto()
    MARKETING = auto()
    LIFECYCLE = auto()
    ALERT = auto()
    SURVEY = auto()
    NEWSLETTER = auto()
    PROMOTIONAL = auto()
    ONBOARDING = auto()
    REENGAGEMENT = auto()


class CustomerStatus(Enum):
    PROSPECT = auto()
    ACTIVE = auto()
    AT_RISK = auto()
    CHURNED = auto()
    RECOVERED = auto()
    VIP = auto()
    DORMANT = auto()


class CampaignStatus(Enum):
    DRAFT = auto()
    SCHEDULED = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class SegmentType(Enum):
    BEHAVIORAL = auto()
    DEMOGRAPHIC = auto()
    PSYCHOGRAPHIC = auto()
    TRANSACTIONAL = auto()
    ENGAGEMENT = auto()
    LIFECYCLE = auto()
    CUSTOM = auto()


class EventPriority(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()


class PersonalizationLevel(Enum):
    NONE = auto()
    BASIC = auto()
    ADVANCED = auto()
    DYNAMIC = auto()
    AI_POWERED = auto()


class JourneyStage(Enum):
    AWARENESS = auto()
    CONSIDERATION = auto()
    CONVERSION = auto()
    ONBOARDING = auto()
    ENGAGEMENT = auto()
    RETENTION = auto()
    ADVOCACY = auto()
    WINBACK = auto()


class AttributionModel(Enum):
    FIRST_TOUCH = auto()
    LAST_TOUCH = auto()
    LINEAR = auto()
    TIME_DECAY = auto()
    POSITION_BASED = auto()
    DATA_DRIVEN = auto()


class ABTestStatus(Enum):
    SETUP = auto()
    RUNNING = auto()
    ANALYZING = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class ContentFormat(Enum):
    PLAIN_TEXT = auto()
    HTML = auto()
    MARKDOWN = auto()
    JSON = auto()
    TEMPLATE = auto()


class TriggerType(Enum):
    EVENT = auto()
    SCHEDULE = auto()
    THRESHOLD = auto()
    LIFECYCLE = auto()
    COMPOSITE = auto()


class FeedbackType(Enum):
    CSAT = auto()
    NPS = auto()
    CES = auto()
    SURVEY = auto()
    REVIEW = auto()
    RATING = auto()


class WebhookStatus(Enum):
    ACTIVE = auto()
    PAUSED = auto()
    FAILED = auto()
    RETRYING = auto()
    DISABLED = auto()


# =============================================================================
# CONSTANTS
# =============================================================================

DEFAULT_CHANNEL_CONFIG: Dict[ChannelType, Dict[str, Any]] = {
    ChannelType.EMAIL: {"daily_limit": 10, "cooldown_hours": 24, "enabled": True},
    ChannelType.SMS: {"daily_limit": 3, "cooldown_hours": 48, "enabled": True},
    ChannelType.PUSH_NOTIFICATION: {"daily_limit": 5, "cooldown_hours": 6, "enabled": True},
    ChannelType.IN_APP: {"daily_limit": 20, "cooldown_hours": 1, "enabled": True},
    ChannelType.SOCIAL_FACEBOOK: {"daily_limit": 2, "cooldown_hours": 12, "enabled": True},
    ChannelType.SOCIAL_TWITTER: {"daily_limit": 5, "cooldown_hours": 4, "enabled": True},
    ChannelType.WEBHOOK: {"daily_limit": 100, "cooldown_hours": 0, "enabled": True},
    ChannelType.DIRECT_MAIL: {"daily_limit": 1, "cooldown_hours": 168, "enabled": True},
    ChannelType.chat: {"daily_limit": 50, "cooldown_hours": 0, "enabled": True},
}

ENGAGEMENT_WEIGHTS: Dict[ChannelType, float] = {
    ChannelType.EMAIL: 1.0, ChannelType.SMS: 1.5,
    ChannelType.PUSH_NOTIFICATION: 1.2, ChannelType.IN_APP: 0.8,
    ChannelType.SOCIAL_FACEBOOK: 0.6, ChannelType.SOCIAL_TWITTER: 0.6,
    ChannelType.WEBHOOK: 0.3, ChannelType.DIRECT_MAIL: 2.0,
    ChannelType.chat: 0.5,
}

LIFECYCLE_STAGE_ORDER = [
    JourneyStage.AWARENESS, JourneyStage.CONSIDERATION,
    JourneyStage.CONVERSION, JourneyStage.ONBOARDING,
    JourneyStage.ENGAGEMENT, JourneyStage.RETENTION,
    JourneyStage.ADVOCACY, JourneyStage.WINBACK,
]

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Customer:
    customer_id: str
    email: str = ""
    phone: str = ""
    name: str = ""
    status: CustomerStatus = CustomerStatus.PROSPECT
    segment_ids: List[str] = field(default_factory=list)
    engagement_score: float = 0.0
    lifetime_value: float = 0.0
    last_active: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    channel_preferences: List[ChannelType] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    lifecycle_stage: JourneyStage = JourneyStage.AWARENESS
    acquisition_channel: ChannelType = ChannelType.EMAIL
    total_purchases: int = 0
    average_order_value: float = 0.0
    preferred_language: str = "en"
    timezone: str = "UTC"
    opt_out_channels: List[ChannelType] = field(default_factory=list)


@dataclass
class Event:
    event_id: str
    customer_id: str
    event_type: str
    channel: ChannelType = ChannelType.IN_APP
    properties: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    session_id: Optional[str] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    attributed_campaign: Optional[str] = None


@dataclass
class Message:
    message_id: str
    customer_id: str
    channel: ChannelType
    message_type: MessageType
    subject: str = ""
    body: str = ""
    template_id: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    converted: bool = False
    campaign_id: Optional[str] = None
    ab_test_id: Optional[str] = None
    variant: Optional[str] = None


@dataclass
class Campaign:
    campaign_id: str
    name: str
    campaign_type: MessageType
    status: CampaignStatus = CampaignStatus.DRAFT
    channels: List[ChannelType] = field(default_factory=list)
    segment_ids: List[str] = field(default_factory=list)
    template_id: Optional[str] = None
    subject: str = ""
    body: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    total_sent: int = 0
    total_delivered: int = 0
    total_opened: int = 0
    total_clicked: int = 0
    total_converted: int = 0
    total_unsubscribed: int = 0
    budget: float = 0.0
    spent: float = 0.0


@dataclass
class Segment:
    segment_id: str
    name: str
    segment_type: SegmentType
    description: str = ""
    rules: List[Dict[str, Any]] = field(default_factory=list)
    customer_ids: Set[str] = field(default_factory=set)
    size: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_dynamic: bool = True
    refresh_interval_hours: int = 24


@dataclass
class Template:
    template_id: str
    name: str
    channel: ChannelType
    message_type: MessageType
    subject: str = ""
    body: str = ""
    variables: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    version: int = 1
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JourneyStep:
    step_id: str
    name: str
    channel: ChannelType
    message_type: MessageType
    delay_hours: float = 0.0
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    template_id: Optional[str] = None
    next_step_on_action: Optional[str] = None
    next_step_on_inaction: Optional[str] = None
    timeout_hours: float = 24.0


@dataclass
class Journey:
    journey_id: str
    name: str
    trigger_event: str
    steps: List[JourneyStep] = field(default_factory=list)
    entry_segment_id: Optional[str] = None
    is_active: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    total_entries: int = 0
    total_completions: int = 0
    current_enrollments: int = 0


@dataclass
class ABTest:
    test_id: str
    name: str
    campaign_id: str
    variants: List[Dict[str, Any]] = field(default_factory=list)
    status: ABTestStatus = ABTestStatus.SETUP
    traffic_split: Dict[str, float] = field(default_factory=dict)
    primary_metric: str = "open_rate"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    winner: Optional[str] = None
    confidence_level: float = 0.95
    results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EngagementScore:
    customer_id: str
    score: float
    factors: Dict[str, float] = field(default_factory=dict)
    trend: str = "stable"
    calculated_at: datetime = field(default_factory=datetime.now)
    channel_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class AttributionEntry:
    customer_id: str
    campaign_id: str
    channel: ChannelType
    touchpoint_time: datetime
    credit: float = 0.0
    conversion_value: float = 0.0


@dataclass
class KPI:
    name: str
    value: float
    target: float
    unit: str = ""
    trend: str = "stable"
    period: str = "30d"


@dataclass
class ContentBlock:
    block_id: str
    name: str
    format: ContentFormat
    content: str = ""
    variables: List[str] = field(default_factory=list)
    channel: Optional[ChannelType] = None
    is_active: bool = True
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TriggerRule:
    rule_id: str
    name: str
    trigger_type: TriggerType
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    is_active: bool = True
    cooldown_minutes: int = 60
    last_fired: Optional[datetime] = None
    fire_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class FeedbackEntry:
    feedback_id: str
    customer_id: str
    feedback_type: FeedbackType
    score: float = 0.0
    comment: str = ""
    channel: ChannelType = ChannelType.EMAIL
    campaign_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    sentiment: str = "neutral"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WebhookConfig:
    webhook_id: str
    url: str
    events: List[str] = field(default_factory=list)
    status: WebhookStatus = WebhookStatus.ACTIVE
    secret: str = ""
    retry_count: int = 3
    timeout_seconds: int = 30
    headers: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_triggered: Optional[datetime] = None
    failure_count: int = 0


@dataclass
class ChannelPerformance:
    channel: ChannelType
    total_sent: int = 0
    total_delivered: int = 0
    total_opened: int = 0
    total_clicked: int = 0
    total_converted: int = 0
    total_bounced: int = 0
    total_complained: int = 0
    delivery_rate: float = 0.0
    open_rate: float = 0.0
    click_rate: float = 0.0
    conversion_rate: float = 0.0
    bounce_rate: float = 0.0
    complaint_rate: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


# =============================================================================
# EXCEPTIONS
# =============================================================================

class EngagementError(Exception):
    pass

class ChannelError(EngagementError):
    pass

class CampaignError(EngagementError):
    pass

class SegmentError(EngagementError):
    pass

class TemplateError(EngagementError):
    pass

class JourneyError(EngagementError):
    pass

class RateLimitError(EngagementError):
    pass

class PersonalizationError(EngagementError):
    pass

class ContentError(EngagementError):
    pass

class WebhookError(EngagementError):
    pass

class FeedbackError(EngagementError):
    pass

class TriggerError(EngagementError):
    pass


# =============================================================================
# CUSTOMER MANAGER
# =============================================================================

class CustomerManager:
    def __init__(self) -> None:
        self._customers: Dict[str, Customer] = {}
        self._events: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self._lock = threading.Lock()

    def create_customer(self, customer_id: str, email: str = "", phone: str = "",
                        name: str = "", **kwargs: Any) -> Customer:
        customer = Customer(
            customer_id=customer_id, email=email, phone=phone, name=name,
            channel_preferences=kwargs.get("channel_preferences", []),
            tags=kwargs.get("tags", []),
            acquisition_channel=kwargs.get("acquisition_channel", ChannelType.EMAIL),
        )
        with self._lock:
            self._customers[customer_id] = customer
        logger.info("Created customer %s", customer_id)
        return customer

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        with self._lock:
            return self._customers.get(customer_id)

    def update_customer(self, customer_id: str, **updates: Any) -> Optional[Customer]:
        with self._lock:
            customer = self._customers.get(customer_id)
            if not customer:
                return None
            for key, value in updates.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
        return customer

    def update_status(self, customer_id: str, status: CustomerStatus) -> bool:
        with self._lock:
            customer = self._customers.get(customer_id)
            if customer:
                customer.status = status
                return True
        return False

    def update_engagement_score(self, customer_id: str, score: float) -> None:
        with self._lock:
            customer = self._customers.get(customer_id)
            if customer:
                customer.engagement_score = score
                customer.last_active = datetime.now()

    def record_event(self, event: Event) -> None:
        with self._lock:
            self._events[event.customer_id].append(event)
            customer = self._customers.get(event.customer_id)
            if customer:
                customer.last_active = event.timestamp

    def get_events(self, customer_id: str, event_type: Optional[str] = None,
                   limit: int = 100) -> List[Event]:
        with self._lock:
            events = list(self._events.get(customer_id, []))
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events[-limit:]

    def get_customers_by_status(self, status: CustomerStatus) -> List[Customer]:
        with self._lock:
            return [c for c in self._customers.values() if c.status == status]

    def get_customers_by_segment(self, segment_id: str) -> List[Customer]:
        with self._lock:
            return [c for c in self._customers.values() if segment_id in c.segment_ids]

    def get_active_customers(self, days: int = 30) -> List[Customer]:
        cutoff = datetime.now() - timedelta(days=days)
        with self._lock:
            return [c for c in self._customers.values() if c.last_active >= cutoff]

    def search_customers(self, query: str) -> List[Customer]:
        query_lower = query.lower()
        with self._lock:
            return [c for c in self._customers.values()
                    if query_lower in c.email.lower() or query_lower in c.name.lower()
                    or query_lower in c.customer_id.lower()]

    def get_customer_count(self) -> int:
        with self._lock:
            return len(self._customers)

    def get_all_customers(self) -> List[Customer]:
        with self._lock:
            return list(self._customers.values())

    def bulk_update_status(self, customer_ids: List[str], status: CustomerStatus) -> int:
        updated = 0
        with self._lock:
            for cid in customer_ids:
                if cid in self._customers:
                    self._customers[cid].status = status
                    updated += 1
        return updated

    def bulk_create_customers(self, customers_data: List[Dict[str, Any]]) -> int:
        created = 0
        for data in customers_data:
            cid = data.get("customer_id", str(uuid.uuid4()))
            self.create_customer(
                cid, email=data.get("email", ""), phone=data.get("phone", ""),
                name=data.get("name", ""),
            )
            created += 1
        return created

    def get_customers_by_tag(self, tag: str) -> List[Customer]:
        with self._lock:
            return [c for c in self._customers.values() if tag in c.tags]

    def add_tag(self, customer_id: str, tag: str) -> bool:
        with self._lock:
            customer = self._customers.get(customer_id)
            if customer and tag not in customer.tags:
                customer.tags.append(tag)
                return True
        return False

    def remove_tag(self, customer_id: str, tag: str) -> bool:
        with self._lock:
            customer = self._customers.get(customer_id)
            if customer and tag in customer.tags:
                customer.tags.remove(tag)
                return True
        return False

    def opt_out_channel(self, customer_id: str, channel: ChannelType) -> bool:
        with self._lock:
            customer = self._customers.get(customer_id)
            if customer and channel not in customer.opt_out_channels:
                customer.opt_out_channels.append(channel)
                return True
        return False

    def delete_customer(self, customer_id: str) -> bool:
        with self._lock:
            if customer_id in self._customers:
                del self._customers[customer_id]
                self._events.pop(customer_id, None)
                return True
        return False


# =============================================================================
# SEGMENT MANAGER
# =============================================================================

class SegmentManager:
    def __init__(self, customer_manager: CustomerManager) -> None:
        self._customer_manager = customer_manager
        self._segments: Dict[str, Segment] = {}
        self._lock = threading.Lock()

    def create_segment(self, segment_id: str, name: str, segment_type: SegmentType,
                       rules: Optional[List[Dict[str, Any]]] = None,
                       description: str = "") -> Segment:
        segment = Segment(
            segment_id=segment_id, name=name, segment_type=segment_type,
            rules=rules or [], description=description,
        )
        with self._lock:
            self._segments[segment_id] = segment
        self._evaluate_segment(segment_id)
        logger.info("Created segment %s: %s (%d customers)", segment_id, name, segment.size)
        return segment

    def get_segment(self, segment_id: str) -> Optional[Segment]:
        with self._lock:
            return self._segments.get(segment_id)

    def _evaluate_segment(self, segment_id: str) -> None:
        segment = self._segments.get(segment_id)
        if not segment:
            return
        customers = self._customer_manager.get_all_customers()
        matched = set()
        for customer in customers:
            if self._matches_rules(customer, segment.rules):
                matched.add(customer.customer_id)
        with self._lock:
            segment.customer_ids = matched
            segment.size = len(matched)
            segment.updated_at = datetime.now()

    def _matches_rules(self, customer: Customer, rules: List[Dict[str, Any]]) -> bool:
        if not rules:
            return True
        for rule in rules:
            field_name = rule.get("field", "")
            operator = rule.get("operator", "eq")
            value = rule.get("value")
            customer_value = getattr(customer, field_name, None)
            if customer_value is None:
                return False
            if operator == "eq" and customer_value != value:
                return False
            if operator == "neq" and customer_value == value:
                return False
            if operator == "gt" and customer_value <= value:
                return False
            if operator == "lt" and customer_value >= value:
                return False
            if operator == "gte" and customer_value < value:
                return False
            if operator == "lte" and customer_value > value:
                return False
            if operator == "in" and customer_value not in value:
                return False
            if operator == "contains" and value not in str(customer_value):
                return False
        return True

    def refresh_segment(self, segment_id: str) -> int:
        self._evaluate_segment(segment_id)
        segment = self._segments.get(segment_id)
        return segment.size if segment else 0

    def refresh_all_segments(self) -> Dict[str, int]:
        results = {}
        with self._lock:
            segment_ids = list(self._segments.keys())
        for sid in segment_ids:
            results[sid] = self.refresh_segment(sid)
        return results

    def combine_segments(self, segment_ids: List[str], operator: str = "union") -> Set[str]:
        with self._lock:
            sets = [self._segments[sid].customer_ids for sid in segment_ids if sid in self._segments]
        if not sets:
            return set()
        if operator == "union":
            return set.union(*sets)
        elif operator == "intersection":
            return set.intersection(*sets)
        elif operator == "difference":
            return sets[0] - set.union(*sets[1:]) if len(sets) > 1 else sets[0]
        return set()

    def get_segment_size(self, segment_id: str) -> int:
        segment = self._segments.get(segment_id)
        return segment.size if segment else 0

    def get_all_segments(self) -> List[Segment]:
        with self._lock:
            return list(self._segments.values())

    def delete_segment(self, segment_id: str) -> bool:
        with self._lock:
            if segment_id in self._segments:
                del self._segments[segment_id]
                return True
        return False

    def clone_segment(self, segment_id: str, new_id: str, new_name: str) -> Optional[Segment]:
        original = self._segments.get(segment_id)
        if not original:
            return None
        return self.create_segment(new_id, new_name, original.segment_type,
                                   rules=list(original.rules),
                                   description=original.description)

    def get_segment_overlap(self, seg_a_id: str, seg_b_id: str) -> Dict[str, Any]:
        a = self._segments.get(seg_a_id)
        b = self._segments.get(seg_b_id)
        if not a or not b:
            return {"error": "Segment not found"}
        overlap = a.customer_ids & b.customer_ids
        return {
            "segment_a": seg_a_id, "segment_b": seg_b_id,
            "overlap_count": len(overlap),
            "overlap_pct_a": len(overlap) / a.size if a.size > 0 else 0,
            "overlap_pct_b": len(overlap) / b.size if b.size > 0 else 0,
        }


# =============================================================================
# MESSAGE ORCHESTRATOR
# =============================================================================

class MessageOrchestrator:
    def __init__(self, customer_manager: CustomerManager) -> None:
        self._customer_manager = customer_manager
        self._messages: List[Message] = []
        self._templates: Dict[str, Template] = {}
        self._channel_config: Dict[ChannelType, Dict[str, Any]] = dict(DEFAULT_CHANNEL_CONFIG)
        self._send_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._lock = threading.Lock()

    def register_template(self, template: Template) -> None:
        with self._lock:
            self._templates[template.template_id] = template
        logger.info("Registered template %s: %s", template.template_id, template.name)

    def get_template(self, template_id: str) -> Optional[Template]:
        with self._lock:
            return self._templates.get(template_id)

    def configure_channel(self, channel: ChannelType, config: Dict[str, Any]) -> None:
        with self._lock:
            self._channel_config[channel].update(config)

    def check_rate_limit(self, customer_id: str, channel: ChannelType) -> bool:
        config = self._channel_config.get(channel, {})
        daily_limit = config.get("daily_limit", 10)
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{customer_id}_{channel.name}"
        count = self._send_counts.get(today, {}).get(key, 0)
        return count < daily_limit

    def send_message(self, customer_id: str, channel: ChannelType,
                     message_type: MessageType, subject: str = "", body: str = "",
                     template_id: Optional[str] = None,
                     variables: Optional[Dict[str, Any]] = None,
                     campaign_id: Optional[str] = None) -> Optional[Message]:
        customer = self._customer_manager.get_customer(customer_id)
        if not customer:
            logger.error("Customer %s not found", customer_id)
            return None
        if channel in customer.opt_out_channels:
            logger.warning("Customer %s opted out of %s", customer_id, channel.name)
            return None
        if not self.check_rate_limit(customer_id, channel):
            raise RateLimitError(f"Rate limit exceeded for {customer_id} on {channel.name}")
        if template_id:
            template = self.get_template(template_id)
            if template:
                subject = template.subject
                body = template.body
                for var_name, var_value in (variables or {}).items():
                    subject = subject.replace(f"{{{{{var_name}}}}}", str(var_value))
                    body = body.replace(f"{{{{{var_name}}}}}", str(var_value))
        message = Message(
            message_id=str(uuid.uuid4()), customer_id=customer_id,
            channel=channel, message_type=message_type, subject=subject,
            body=body, template_id=template_id, variables=variables or {},
            campaign_id=campaign_id, status="sent", sent_at=datetime.now(),
        )
        with self._lock:
            self._messages.append(message)
            today = datetime.now().strftime("%Y-%m-%d")
            key = f"{customer_id}_{channel.name}"
            self._send_counts[today][key] += 1
        logger.info("Sent %s message to %s via %s", message_type.name, customer_id, channel.name)
        return message

    def send_bulk(self, customer_ids: List[str], channel: ChannelType,
                  message_type: MessageType, subject: str = "", body: str = "",
                  campaign_id: Optional[str] = None) -> Dict[str, Any]:
        sent = 0
        failed = 0
        rate_limited = 0
        for cid in customer_ids:
            try:
                msg = self.send_message(cid, channel, message_type, subject, body,
                                        campaign_id=campaign_id)
                if msg:
                    sent += 1
                else:
                    failed += 1
            except RateLimitError:
                rate_limited += 1
            except Exception as e:
                logger.error("Failed to send to %s: %s", cid, e)
                failed += 1
        return {
            "sent": sent, "failed": failed,
            "rate_limited": rate_limited, "total": len(customer_ids),
        }

    def get_message_history(self, customer_id: Optional[str] = None,
                            channel: Optional[ChannelType] = None,
                            limit: int = 100) -> List[Message]:
        with self._lock:
            messages = list(self._messages)
        if customer_id:
            messages = [m for m in messages if m.customer_id == customer_id]
        if channel:
            messages = [m for m in messages if m.channel == channel]
        return messages[-limit:]

    def get_send_stats(self, date: Optional[str] = None) -> Dict[str, int]:
        date = date or datetime.now().strftime("%Y-%m-%d")
        with self._lock:
            return dict(self._send_counts.get(date, {}))

    def update_message_status(self, message_id: str, status: str,
                              timestamp: Optional[datetime] = None) -> bool:
        with self._lock:
            for msg in self._messages:
                if msg.message_id == message_id:
                    msg.status = status
                    ts = timestamp or datetime.now()
                    if status == "delivered":
                        msg.delivered_at = ts
                    elif status == "opened":
                        msg.opened_at = ts
                    elif status == "clicked":
                        msg.clicked_at = ts
                    return True
        return False

    def get_channel_stats(self, channel: ChannelType) -> Dict[str, Any]:
        with self._lock:
            messages = [m for m in self._messages if m.channel == channel]
        total = len(messages)
        delivered = sum(1 for m in messages if m.delivered_at)
        opened = sum(1 for m in messages if m.opened_at)
        clicked = sum(1 for m in messages if m.clicked_at)
        return {
            "channel": channel.name, "total": total, "delivered": delivered,
            "opened": opened, "clicked": clicked,
            "delivery_rate": delivered / total if total > 0 else 0,
            "open_rate": opened / delivered if delivered > 0 else 0,
            "click_rate": clicked / opened if opened > 0 else 0,
        }

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        with self._lock:
            for msg in self._messages:
                if msg.message_id == message_id:
                    return msg
        return None

    def get_daily_volume(self, days: int = 7) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            with self._lock:
                day_counts = self._send_counts.get(date, {})
            result[date] = sum(day_counts.values())
        return result


# =============================================================================
# CAMPAIGN MANAGER
# =============================================================================

class CampaignManager:
    def __init__(self, customer_manager: CustomerManager,
                 message_orchestrator: MessageOrchestrator) -> None:
        self._customer_manager = customer_manager
        self._message_orchestrator = message_orchestrator
        self._campaigns: Dict[str, Campaign] = {}
        self._ab_tests: Dict[str, ABTest] = {}
        self._lock = threading.Lock()

    def create_campaign(self, campaign_id: str, name: str, campaign_type: MessageType,
                        channels: List[ChannelType], segment_ids: List[str],
                        subject: str = "", body: str = "", **kwargs: Any) -> Campaign:
        campaign = Campaign(
            campaign_id=campaign_id, name=name, campaign_type=campaign_type,
            channels=channels, segment_ids=segment_ids, subject=subject,
            body=body, created_by=kwargs.get("created_by", ""),
            budget=kwargs.get("budget", 0.0),
        )
        with self._lock:
            self._campaigns[campaign_id] = campaign
        logger.info("Created campaign %s: %s", campaign_id, name)
        return campaign

    def start_campaign(self, campaign_id: str) -> bool:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            if not campaign:
                return False
            campaign.status = CampaignStatus.RUNNING
            campaign.start_time = datetime.now()
        self._execute_campaign(campaign_id)
        return True

    def _execute_campaign(self, campaign_id: str) -> None:
        campaign = self._campaigns.get(campaign_id)
        if not campaign:
            return
        customer_ids: Set[str] = set()
        for seg_id in campaign.segment_ids:
            segment_customers = self._customer_manager.get_customers_by_segment(seg_id)
            customer_ids.update(c.customer_id for c in segment_customers)
        for channel in campaign.channels:
            result = self._message_orchestrator.send_bulk(
                list(customer_ids), channel, campaign.campaign_type,
                campaign.subject, campaign.body, campaign_id,
            )
            with self._lock:
                campaign.total_sent += result["total"]
                campaign.total_delivered += result["sent"]
        logger.info("Executed campaign %s: sent to %d customers", campaign_id, len(customer_ids))

    def pause_campaign(self, campaign_id: str) -> bool:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            if campaign and campaign.status == CampaignStatus.RUNNING:
                campaign.status = CampaignStatus.PAUSED
                return True
        return False

    def complete_campaign(self, campaign_id: str) -> bool:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            if campaign:
                campaign.status = CampaignStatus.COMPLETED
                campaign.end_time = datetime.now()
                return True
        return False

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        with self._lock:
            return self._campaigns.get(campaign_id)

    def get_all_campaigns(self, status: Optional[CampaignStatus] = None) -> List[Campaign]:
        with self._lock:
            campaigns = list(self._campaigns.values())
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        return campaigns

    def get_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self._campaigns.get(campaign_id)
        if not campaign:
            return {"error": "Campaign not found"}
        return {
            "campaign_id": campaign_id, "name": campaign.name,
            "status": campaign.status.name, "total_sent": campaign.total_sent,
            "total_delivered": campaign.total_delivered, "total_opened": campaign.total_opened,
            "total_clicked": campaign.total_clicked, "total_converted": campaign.total_converted,
            "delivery_rate": campaign.total_delivered / campaign.total_sent if campaign.total_sent > 0 else 0,
            "open_rate": campaign.total_opened / campaign.total_delivered if campaign.total_delivered > 0 else 0,
            "click_rate": campaign.total_clicked / campaign.total_opened if campaign.total_opened > 0 else 0,
            "conversion_rate": campaign.total_converted / campaign.total_clicked if campaign.total_clicked > 0 else 0,
            "unsubscribe_rate": campaign.total_unsubscribed / campaign.total_sent if campaign.total_sent > 0 else 0,
        }

    def create_ab_test(self, test_id: str, name: str, campaign_id: str,
                       variants: List[Dict[str, Any]],
                       primary_metric: str = "open_rate") -> ABTest:
        test = ABTest(
            test_id=test_id, name=name, campaign_id=campaign_id,
            variants=variants, primary_metric=primary_metric,
            traffic_split={v["name"]: 1.0 / len(variants) for v in variants},
        )
        with self._lock:
            self._ab_tests[test_id] = test
        logger.info("Created AB test %s: %s", test_id, name)
        return test

    def start_ab_test(self, test_id: str) -> bool:
        with self._lock:
            test = self._ab_tests.get(test_id)
            if test:
                test.status = ABTestStatus.RUNNING
                test.start_time = datetime.now()
                return True
        return False

    def record_ab_result(self, test_id: str, variant: str, metric_value: float) -> None:
        with self._lock:
            test = self._ab_tests.get(test_id)
            if test:
                if variant not in test.results:
                    test.results[variant] = {"values": [], "count": 0}
                test.results[variant]["values"].append(metric_value)
                test.results[variant]["count"] += 1

    def analyze_ab_test(self, test_id: str) -> Dict[str, Any]:
        with self._lock:
            test = self._ab_tests.get(test_id)
        if not test:
            return {"error": "Test not found"}
        analysis: Dict[str, Any] = {
            "test_id": test_id, "variants": {}, "winner": None, "confidence": 0,
        }
        variant_stats: Dict[str, Dict[str, float]] = {}
        for variant, data in test.results.items():
            values = data["values"]
            if values:
                mean = statistics.mean(values)
                std = statistics.stdev(values) if len(values) > 1 else 0
                variant_stats[variant] = {"mean": mean, "std": std, "count": len(values)}
                analysis["variants"][variant] = variant_stats[variant]
        if len(variant_stats) >= 2:
            best = max(variant_stats.items(), key=lambda x: x[1]["mean"])
            analysis["winner"] = best[0]
            analysis["confidence"] = min(0.99, 0.5 + (best[1]["count"] / 100))
        return analysis

    def get_all_ab_tests(self) -> List[ABTest]:
        with self._lock:
            return list(self._ab_tests.values())


# =============================================================================
# JOURNEY MANAGER
# =============================================================================

class JourneyManager:
    def __init__(self, customer_manager: CustomerManager,
                 message_orchestrator: MessageOrchestrator) -> None:
        self._customer_manager = customer_manager
        self._message_orchestrator = message_orchestrator
        self._journeys: Dict[str, Journey] = {}
        self._enrollments: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create_journey(self, journey_id: str, name: str, trigger_event: str,
                       steps: Optional[List[JourneyStep]] = None,
                       entry_segment_id: Optional[str] = None) -> Journey:
        journey = Journey(
            journey_id=journey_id, name=name, trigger_event=trigger_event,
            steps=steps or [], entry_segment_id=entry_segment_id,
        )
        with self._lock:
            self._journeys[journey_id] = journey
        logger.info("Created journey %s: %s", journey_id, name)
        return journey

    def activate_journey(self, journey_id: str) -> bool:
        with self._lock:
            journey = self._journeys.get(journey_id)
            if journey:
                journey.is_active = True
                return True
        return False

    def deactivate_journey(self, journey_id: str) -> bool:
        with self._lock:
            journey = self._journeys.get(journey_id)
            if journey:
                journey.is_active = False
                return True
        return False

    def enroll_customer(self, journey_id: str, customer_id: str) -> bool:
        with self._lock:
            journey = self._journeys.get(journey_id)
            if not journey or not journey.is_active:
                return False
            enrollment_id = f"{journey_id}_{customer_id}"
            self._enrollments[enrollment_id] = {
                "journey_id": journey_id, "customer_id": customer_id,
                "current_step": 0, "enrolled_at": datetime.now(),
                "status": "active", "history": [],
            }
            journey.total_entries += 1
            journey.current_enrollments += 1
        logger.info("Enrolled %s in journey %s", customer_id, journey_id)
        return True

    def process_enrollment(self, enrollment_id: str) -> bool:
        with self._lock:
            enrollment = self._enrollments.get(enrollment_id)
            if not enrollment or enrollment["status"] != "active":
                return False
            journey = self._journeys.get(enrollment["journey_id"])
            if not journey:
                return False
            step_index = enrollment["current_step"]
            if step_index >= len(journey.steps):
                enrollment["status"] = "completed"
                journey.total_completions += 1
                journey.current_enrollments -= 1
                return True
            step = journey.steps[step_index]
            customer = self._customer_manager.get_customer(enrollment["customer_id"])
            if customer:
                self._message_orchestrator.send_message(
                    customer.customer_id, step.channel, step.message_type,
                    template_id=step.template_id,
                )
            enrollment["current_step"] = step_index + 1
            enrollment["history"].append({
                "step": step.name, "channel": step.channel.name,
                "timestamp": datetime.now().isoformat(),
            })
        return True

    def advance_enrollment(self, enrollment_id: str, action: str = "next") -> bool:
        with self._lock:
            enrollment = self._enrollments.get(enrollment_id)
            if not enrollment:
                return False
            journey = self._journeys.get(enrollment["journey_id"])
            if not journey:
                return False
            step_index = enrollment["current_step"]
            if step_index < len(journey.steps):
                step = journey.steps[step_index]
                if action == "next":
                    next_step_id = step.next_step_on_action
                else:
                    next_step_id = step.next_step_on_inaction
                if next_step_id:
                    for i, s in enumerate(journey.steps):
                        if s.step_id == next_step_id:
                            enrollment["current_step"] = i
                            return True
            enrollment["current_step"] = step_index + 1
        return True

    def get_journey(self, journey_id: str) -> Optional[Journey]:
        with self._lock:
            return self._journeys.get(journey_id)

    def get_all_journeys(self) -> List[Journey]:
        with self._lock:
            return list(self._journeys.values())

    def get_enrollment_stats(self, journey_id: str) -> Dict[str, Any]:
        with self._lock:
            enrollments = [e for e in self._enrollments.values()
                           if e["journey_id"] == journey_id]
        total = len(enrollments)
        active = sum(1 for e in enrollments if e["status"] == "active")
        completed = sum(1 for e in enrollments if e["status"] == "completed")
        return {
            "journey_id": journey_id, "total_enrollments": total,
            "active": active, "completed": completed,
            "completion_rate": completed / total if total > 0 else 0,
        }

    def get_customer_journey_progress(self, customer_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            enrollments = [e for e in self._enrollments.values()
                           if e["customer_id"] == customer_id]
        return [{
            "journey_id": e["journey_id"], "current_step": e["current_step"],
            "status": e["status"], "history": e["history"],
        } for e in enrollments]


# =============================================================================
# ENGAGEMENT SCORER
# =============================================================================

class EngagementScorer:
    def __init__(self, customer_manager: CustomerManager) -> None:
        self._customer_manager = customer_manager
        self._scores: Dict[str, EngagementScore] = {}
        self._scoring_rules: Dict[str, float] = {
            "email_open": 2.0, "email_click": 5.0,
            "sms_click": 7.0, "purchase": 20.0,
            "app_open": 1.0, "page_view": 0.5,
            "signup": 10.0, "referral": 15.0,
            "review": 8.0, "social_share": 3.0,
        }
        self._decay_rate = 0.95
        self._lock = threading.Lock()

    def set_scoring_rule(self, event_type: str, points: float) -> None:
        self._scoring_rules[event_type] = points

    def calculate_score(self, customer_id: str) -> EngagementScore:
        events = self._customer_manager.get_events(customer_id, limit=1000)
        factors: Dict[str, float] = defaultdict(float)
        channel_scores: Dict[str, float] = defaultdict(float)
        for event in events:
            weight = self._scoring_rules.get(event.event_type, 0.1)
            recency_days = (datetime.now() - event.timestamp).days
            decay = self._decay_rate ** recency_days
            adjusted_weight = weight * decay
            factors[event.event_type] += adjusted_weight
            channel_scores[event.channel.name] += adjusted_weight
        total_score = sum(factors.values())
        normalized = min(100.0, total_score)
        previous = self._scores.get(customer_id)
        trend = "stable"
        if previous:
            if normalized > previous.score * 1.1:
                trend = "increasing"
            elif normalized < previous.score * 0.9:
                trend = "decreasing"
        score = EngagementScore(
            customer_id=customer_id, score=normalized,
            factors=dict(factors), trend=trend,
            channel_scores=dict(channel_scores),
        )
        with self._lock:
            self._scores[customer_id] = score
        self._customer_manager.update_engagement_score(customer_id, normalized)
        return score

    def get_score(self, customer_id: str) -> Optional[EngagementScore]:
        with self._lock:
            return self._scores.get(customer_id)

    def calculate_all_scores(self) -> Dict[str, float]:
        customers = self._customer_manager.get_all_customers()
        results: Dict[str, float] = {}
        for customer in customers:
            score = self.calculate_score(customer.customer_id)
            results[customer.customer_id] = score.score
        return results

    def get_top_engaged(self, limit: int = 20) -> List[EngagementScore]:
        with self._lock:
            scores = list(self._scores.values())
        scores.sort(key=lambda s: s.score, reverse=True)
        return scores[:limit]

    def get_low_engaged(self, threshold: float = 20.0) -> List[EngagementScore]:
        with self._lock:
            return [s for s in self._scores.values() if s.score < threshold]

    def get_score_distribution(self) -> Dict[str, int]:
        distribution: Dict[str, int] = {"0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0}
        with self._lock:
            for score in self._scores.values():
                if score.score < 20:
                    distribution["0-20"] += 1
                elif score.score < 40:
                    distribution["20-40"] += 1
                elif score.score < 60:
                    distribution["40-60"] += 1
                elif score.score < 80:
                    distribution["60-80"] += 1
                else:
                    distribution["80-100"] += 1
        return distribution

    def get_trend_summary(self) -> Dict[str, int]:
        trends: Dict[str, int] = {"increasing": 0, "stable": 0, "decreasing": 0}
        with self._lock:
            for score in self._scores.values():
                trends[score.trend] += 1
        return trends

    def get_score_percentiles(self) -> Dict[str, float]:
        with self._lock:
            scores = [s.score for s in self._scores.values()]
        if not scores:
            return {}
        scores.sort()
        n = len(scores)
        return {
            "p25": scores[int(n * 0.25)],
            "p50": scores[int(n * 0.50)],
            "p75": scores[int(n * 0.75)],
            "p90": scores[int(n * 0.90)],
            "p99": scores[int(n * 0.99)],
        }


# =============================================================================
# ATTRIBUTION MANAGER
# =============================================================================

class AttributionManager:
    def __init__(self) -> None:
        self._entries: List[AttributionEntry] = []
        self._model: AttributionModel = AttributionModel.LAST_TOUCH
        self._lock = threading.Lock()

    def set_model(self, model: AttributionModel) -> None:
        self._model = model

    def record_touchpoint(self, customer_id: str, campaign_id: str,
                          channel: ChannelType, touchpoint_time: datetime,
                          conversion_value: float = 0.0) -> None:
        entry = AttributionEntry(
            customer_id=customer_id, campaign_id=campaign_id,
            channel=channel, touchpoint_time=touchpoint_time,
            conversion_value=conversion_value,
        )
        with self._lock:
            self._entries.append(entry)

    def calculate_attribution(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            entries = [e for e in self._entries if e.customer_id == customer_id]
        if not entries:
            return {"customer_id": customer_id, "attributions": {}}
        entries.sort(key=lambda e: e.touchpoint_time)
        campaign_credits: Dict[str, float] = defaultdict(float)
        channel_credits: Dict[str, float] = defaultdict(float)
        if self._model == AttributionModel.FIRST_TOUCH:
            campaign_credits[entries[0].campaign_id] = 1.0
            channel_credits[entries[0].channel.name] = 1.0
        elif self._model == AttributionModel.LAST_TOUCH:
            campaign_credits[entries[-1].campaign_id] = 1.0
            channel_credits[entries[-1].channel.name] = 1.0
        elif self._model == AttributionModel.LINEAR:
            credit = 1.0 / len(entries)
            for entry in entries:
                campaign_credits[entry.campaign_id] += credit
                channel_credits[entry.channel.name] += credit
        elif self._model == AttributionModel.TIME_DECAY:
            total_weight = sum(1.0 / (i + 1) for i in range(len(entries)))
            for i, entry in enumerate(entries):
                weight = (1.0 / (i + 1)) / total_weight
                campaign_credits[entry.campaign_id] += weight
                channel_credits[entry.channel.name] += weight
        elif self._model == AttributionModel.POSITION_BASED:
            if len(entries) == 1:
                campaign_credits[entries[0].campaign_id] = 1.0
                channel_credits[entries[0].channel.name] = 1.0
            else:
                campaign_credits[entries[0].campaign_id] += 0.4
                campaign_credits[entries[-1].campaign_id] += 0.4
                channel_credits[entries[0].channel.name] += 0.4
                channel_credits[entries[-1].channel.name] += 0.4
                middle_credit = 0.2 / max(1, len(entries) - 2)
                for entry in entries[1:-1]:
                    campaign_credits[entry.campaign_id] += middle_credit
                    channel_credits[entry.channel.name] += middle_credit
        return {
            "customer_id": customer_id, "model": self._model.name,
            "campaign_attributions": dict(campaign_credits),
            "channel_attributions": dict(channel_credits),
            "touchpoints": len(entries),
        }

    def get_campaign_attribution_summary(self) -> Dict[str, Dict[str, float]]:
        with self._lock:
            entries = list(self._entries)
        campaign_summary: Dict[str, Dict[str, float]] = defaultdict(
            lambda: {"credit": 0, "value": 0},
        )
        for entry in entries:
            campaign_summary[entry.campaign_id]["credit"] += entry.credit
            campaign_summary[entry.campaign_id]["value"] += entry.conversion_value
        return dict(campaign_summary)

    def get_channel_attribution_summary(self) -> Dict[str, float]:
        with self._lock:
            entries = list(self._entries)
        channel_summary: Dict[str, float] = defaultdict(float)
        for entry in entries:
            channel_summary[entry.channel.name] += entry.credit
        return dict(channel_summary)


# =============================================================================
# PERSONALIZATION ENGINE
# =============================================================================

class PersonalizationEngine:
    def __init__(self, customer_manager: CustomerManager) -> None:
        self._customer_manager = customer_manager
        self._content_rules: Dict[str, List[Dict[str, Any]]] = {}
        self._recommendations: Dict[str, List[str]] = {}
        self._lock = threading.Lock()

    def add_content_rule(self, rule_id: str, conditions: List[Dict[str, Any]],
                         content: Dict[str, Any]) -> None:
        with self._lock:
            self._content_rules[rule_id] = {"conditions": conditions, "content": content}

    def personalize_content(self, customer_id: str, content_type: str,
                            base_content: Dict[str, Any]) -> Dict[str, Any]:
        customer = self._customer_manager.get_customer(customer_id)
        if not customer:
            return base_content
        personalized = dict(base_content)
        personalized["greeting"] = f"Hi {customer.name}" if customer.name else "Hi there"
        personalized["language"] = customer.preferred_language
        if customer.status == CustomerStatus.VIP:
            personalized["tier"] = "VIP"
            personalized["exclusive_offer"] = True
        elif customer.lifetime_value > 1000:
            personalized["tier"] = "Premium"
        if customer.lifecycle_stage == JourneyStage.ONBOARDING:
            personalized["onboarding_flow"] = True
        return personalized

    def get_recommendations(self, customer_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        customer = self._customer_manager.get_customer(customer_id)
        if not customer:
            return []
        events = self._customer_manager.get_events(customer_id, limit=50)
        recent_types = [e.event_type for e in events[-20:]]
        recommendations: List[Dict[str, Any]] = []
        if "product_view" in recent_types:
            recommendations.append({"type": "product", "reason": "Based on recent views"})
        if "cart_abandon" in recent_types:
            recommendations.append({"type": "cart_reminder", "reason": "Incomplete purchase"})
        if customer.status == CustomerStatus.AT_RISK:
            recommendations.append({"type": "winback_offer", "reason": "At-risk customer"})
        if customer.engagement_score > 80:
            recommendations.append({"type": "referral", "reason": "Highly engaged"})
        return recommendations[:limit]

    def get_optimal_send_time(self, customer_id: str) -> Dict[str, Any]:
        events = self._customer_manager.get_events(customer_id, limit=200)
        if not events:
            return {"hour": 10, "day": "Tuesday", "confidence": "low"}
        hourly_activity: Dict[int, int] = defaultdict(int)
        for event in events:
            hourly_activity[event.timestamp.hour] += 1
        if hourly_activity:
            best_hour = max(hourly_activity, key=hourly_activity.get)
        else:
            best_hour = 10
        return {"hour": best_hour, "day": "optimal", "confidence": "medium"}

    def get_personalization_level(self, customer_id: str) -> PersonalizationLevel:
        customer = self._customer_manager.get_customer(customer_id)
        if not customer:
            return PersonalizationLevel.NONE
        if customer.engagement_score > 80 and customer.total_purchases > 10:
            return PersonalizationLevel.AI_POWERED
        if customer.engagement_score > 50:
            return PersonalizationLevel.ADVANCED
        if customer.total_purchases > 0:
            return PersonalizationLevel.BASIC
        return PersonalizationLevel.NONE


# =============================================================================
# CONTENT MANAGER
# =============================================================================

class ContentManager:
    def __init__(self) -> None:
        self._blocks: Dict[str, ContentBlock] = {}
        self._lock = threading.Lock()

    def create_block(self, block_id: str, name: str, content: str,
                     format: ContentFormat = ContentFormat.PLAIN_TEXT,
                     channel: Optional[ChannelType] = None,
                     variables: Optional[List[str]] = None) -> ContentBlock:
        block = ContentBlock(
            block_id=block_id, name=name, format=format,
            content=content, channel=channel,
            variables=variables or [],
        )
        with self._lock:
            self._blocks[block_id] = block
        logger.info("Created content block %s: %s", block_id, name)
        return block

    def get_block(self, block_id: str) -> Optional[ContentBlock]:
        with self._lock:
            return self._blocks.get(block_id)

    def update_block(self, block_id: str, content: str) -> bool:
        with self._lock:
            block = self._blocks.get(block_id)
            if block:
                block.content = content
                block.version += 1
                return True
        return False

    def render_block(self, block_id: str, variables: Dict[str, Any]) -> str:
        block = self._blocks.get(block_id)
        if not block:
            return ""
        rendered = block.content
        for var_name, var_value in variables.items():
            rendered = rendered.replace(f"{{{{{var_name}}}}}", str(var_value))
        return rendered

    def get_blocks_by_channel(self, channel: ChannelType) -> List[ContentBlock]:
        with self._lock:
            return [b for b in self._blocks.values() if b.channel == channel]

    def delete_block(self, block_id: str) -> bool:
        with self._lock:
            if block_id in self._blocks:
                del self._blocks[block_id]
                return True
        return False

    def list_blocks(self) -> List[ContentBlock]:
        with self._lock:
            return list(self._blocks.values())

    def clone_block(self, block_id: str, new_id: str, new_name: str) -> Optional[ContentBlock]:
        original = self._blocks.get(block_id)
        if not original:
            return None
        return self.create_block(
            new_id, new_name, original.content,
            format=original.format, channel=original.channel,
            variables=list(original.variables),
        )


# =============================================================================
# WEBHOOK MANAGER
# =============================================================================

class WebhookManager:
    def __init__(self) -> None:
        self._webhooks: Dict[str, WebhookConfig] = {}
        self._delivery_log: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def register_webhook(self, webhook_id: str, url: str,
                         events: Optional[List[str]] = None,
                         secret: str = "",
                         headers: Optional[Dict[str, str]] = None) -> WebhookConfig:
        config = WebhookConfig(
            webhook_id=webhook_id, url=url,
            events=events or [], secret=secret,
            headers=headers or {},
        )
        with self._lock:
            self._webhooks[webhook_id] = config
        logger.info("Registered webhook %s -> %s", webhook_id, url)
        return config

    def get_webhook(self, webhook_id: str) -> Optional[WebhookConfig]:
        with self._lock:
            return self._webhooks.get(webhook_id)

    def update_webhook_status(self, webhook_id: str, status: WebhookStatus) -> bool:
        with self._lock:
            webhook = self._webhooks.get(webhook_id)
            if webhook:
                webhook.status = status
                return True
        return False

    def trigger_webhooks(self, event_type: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        with self._lock:
            webhooks = [w for w in self._webhooks.values()
                        if w.status == WebhookStatus.ACTIVE
                        and (not w.events or event_type in w.events)]
        for webhook in webhooks:
            delivery = {
                "webhook_id": webhook.webhook_id, "url": webhook.url,
                "event_type": event_type, "status": "delivered",
                "timestamp": datetime.now().isoformat(),
            }
            with self._lock:
                webhook.last_triggered = datetime.now()
                self._delivery_log.append(delivery)
            results.append(delivery)
        return results

    def get_delivery_log(self, webhook_id: Optional[str] = None,
                         limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            log = list(self._delivery_log)
        if webhook_id:
            log = [d for d in log if d.get("webhook_id") == webhook_id]
        return log[-limit:]

    def list_webhooks(self) -> List[WebhookConfig]:
        with self._lock:
            return list(self._webhooks.values())

    def delete_webhook(self, webhook_id: str) -> bool:
        with self._lock:
            if webhook_id in self._webhooks:
                del self._webhooks[webhook_id]
                return True
        return False

    def get_webhook_stats(self, webhook_id: str) -> Dict[str, Any]:
        with self._lock:
            log = [d for d in self._delivery_log if d.get("webhook_id") == webhook_id]
        total = len(log)
        delivered = sum(1 for d in log if d.get("status") == "delivered")
        failed = total - delivered
        return {
            "webhook_id": webhook_id, "total_triggers": total,
            "delivered": delivered, "failed": failed,
            "delivery_rate": delivered / total if total > 0 else 0,
        }


# =============================================================================
# FEEDBACK COLLECTOR
# =============================================================================

class FeedbackCollector:
    def __init__(self) -> None:
        self._entries: List[FeedbackEntry] = []
        self._lock = threading.Lock()

    def collect_feedback(self, customer_id: str, feedback_type: FeedbackType,
                         score: float = 0.0, comment: str = "",
                         channel: ChannelType = ChannelType.EMAIL,
                         campaign_id: Optional[str] = None) -> FeedbackEntry:
        entry = FeedbackEntry(
            feedback_id=str(uuid.uuid4()), customer_id=customer_id,
            feedback_type=feedback_type, score=score, comment=comment,
            channel=channel, campaign_id=campaign_id,
            sentiment=self._analyze_sentiment(score, comment),
        )
        with self._lock:
            self._entries.append(entry)
        logger.info("Collected %s feedback from %s (score=%.1f)",
                     feedback_type.name, customer_id, score)
        return entry

    def _analyze_sentiment(self, score: float, comment: str) -> str:
        if score >= 8.0:
            return "positive"
        elif score <= 4.0:
            return "negative"
        return "neutral"

    def get_feedback_by_customer(self, customer_id: str) -> List[FeedbackEntry]:
        with self._lock:
            return [e for e in self._entries if e.customer_id == customer_id]

    def get_feedback_by_type(self, feedback_type: FeedbackType) -> List[FeedbackEntry]:
        with self._lock:
            return [e for e in self._entries if e.feedback_type == feedback_type]

    def get_average_score(self, feedback_type: Optional[FeedbackType] = None) -> float:
        with self._lock:
            entries = self._entries
        if feedback_type:
            entries = [e for e in entries if e.feedback_type == feedback_type]
        if not entries:
            return 0.0
        return statistics.mean(e.score for e in entries)

    def get_sentiment_distribution(self) -> Dict[str, int]:
        dist: Dict[str, int] = {"positive": 0, "neutral": 0, "negative": 0}
        with self._lock:
            for entry in self._entries:
                dist[entry.sentiment] = dist.get(entry.sentiment, 0) + 1
        return dist

    def get_nps_score(self) -> Dict[str, Any]:
        nps_entries = [e for e in self._entries if e.feedback_type == FeedbackType.NPS]
        if not nps_entries:
            return {"nps": 0, "promoters": 0, "passives": 0, "detractors": 0}
        promoters = sum(1 for e in nps_entries if e.score >= 9)
        passives = sum(1 for e in nps_entries if 7 <= e.score <= 8)
        detractors = sum(1 for e in nps_entries if e.score <= 6)
        total = len(nps_entries)
        nps = ((promoters - detractors) / total * 100) if total > 0 else 0
        return {
            "nps": round(nps, 1), "promoters": promoters,
            "passives": passives, "detractors": detractors,
            "total_responses": total,
        }

    def get_feedback_summary(self) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._entries)
        total = len(entries)
        by_type: Dict[str, int] = defaultdict(int)
        for e in entries:
            by_type[e.feedback_type.name] += 1
        return {
            "total_feedback": total,
            "by_type": dict(by_type),
            "average_score": self.get_average_score() if entries else 0,
            "sentiment_distribution": self.get_sentiment_distribution(),
        }


# =============================================================================
# CHANNEL ANALYTICS
# =============================================================================

class ChannelAnalytics:
    def __init__(self, message_orchestrator: MessageOrchestrator) -> None:
        self._orchestrator = message_orchestrator
        self._performance: Dict[ChannelType, ChannelPerformance] = {}
        self._lock = threading.Lock()

    def calculate_performance(self, channel: ChannelType) -> ChannelPerformance:
        stats = self._orchestrator.get_channel_stats(channel)
        perf = ChannelPerformance(
            channel=channel,
            total_sent=stats.get("total", 0),
            total_delivered=stats.get("delivered", 0),
            total_opened=stats.get("opened", 0),
            total_clicked=stats.get("clicked", 0),
            delivery_rate=stats.get("delivery_rate", 0),
            open_rate=stats.get("open_rate", 0),
            click_rate=stats.get("click_rate", 0),
            last_updated=datetime.now(),
        )
        with self._lock:
            self._performance[channel] = perf
        return perf

    def calculate_all_performance(self) -> Dict[ChannelType, ChannelPerformance]:
        results: Dict[ChannelType, ChannelPerformance] = {}
        for channel in ChannelType:
            results[channel] = self.calculate_performance(channel)
        return results

    def get_performance(self, channel: ChannelType) -> Optional[ChannelPerformance]:
        with self._lock:
            return self._performance.get(channel)

    def get_comparison(self, channels: Optional[List[ChannelType]] = None) -> List[Dict[str, Any]]:
        if channels is None:
            channels = list(ChannelType)
        results: List[Dict[str, Any]] = []
        for ch in channels:
            perf = self.calculate_performance(ch)
            results.append({
                "channel": ch.name, "total_sent": perf.total_sent,
                "delivery_rate": perf.delivery_rate, "open_rate": perf.open_rate,
                "click_rate": perf.click_rate,
            })
        results.sort(key=lambda x: x["click_rate"], reverse=True)
        return results

    def get_channel_efficiency(self, channel: ChannelType) -> Dict[str, Any]:
        perf = self._performance.get(channel)
        if not perf:
            perf = self.calculate_performance(channel)
        cost_per_open = perf.total_sent / perf.total_opened if perf.total_opened > 0 else float("inf")
        cost_per_click = perf.total_sent / perf.total_clicked if perf.total_clicked > 0 else float("inf")
        return {
            "channel": channel.name,
            "efficiency_score": perf.click_rate * 1000 if perf.click_rate > 0 else 0,
            "cost_per_open": cost_per_open,
            "cost_per_click": cost_per_click,
            "total_sent": perf.total_sent,
        }


# =============================================================================
# TRIGGER ENGINE
# =============================================================================

class TriggerEngine:
    def __init__(self, customer_manager: CustomerManager,
                 message_orchestrator: MessageOrchestrator) -> None:
        self._customer_manager = customer_manager
        self._message_orchestrator = message_orchestrator
        self._rules: Dict[str, TriggerRule] = {}
        self._event_buffer: List[Event] = []
        self._lock = threading.Lock()

    def register_rule(self, rule_id: str, name: str, trigger_type: TriggerType,
                      conditions: Optional[List[Dict[str, Any]]] = None,
                      actions: Optional[List[Dict[str, Any]]] = None,
                      cooldown_minutes: int = 60) -> TriggerRule:
        rule = TriggerRule(
            rule_id=rule_id, name=name, trigger_type=trigger_type,
            conditions=conditions or [], actions=actions or [],
            cooldown_minutes=cooldown_minutes,
        )
        with self._lock:
            self._rules[rule_id] = rule
        logger.info("Registered trigger rule %s: %s", rule_id, name)
        return rule

    def get_rule(self, rule_id: str) -> Optional[TriggerRule]:
        with self._lock:
            return self._rules.get(rule_id)

    def process_event(self, event: Event) -> List[Dict[str, Any]]:
        fired: List[Dict[str, Any]] = []
        with self._lock:
            rules = list(self._rules.values())
        for rule in rules:
            if not rule.is_active:
                continue
            if rule.last_fired:
                elapsed = (datetime.now() - rule.last_fired).total_seconds() / 60
                if elapsed < rule.cooldown_minutes:
                    continue
            if self._check_conditions(rule, event):
                result = self._execute_actions(rule, event)
                with self._lock:
                    rule.last_fired = datetime.now()
                    rule.fire_count += 1
                fired.append({"rule_id": rule.rule_id, "result": result})
        return fired

    def _check_conditions(self, rule: TriggerRule, event: Event) -> bool:
        if not rule.conditions:
            return True
        for condition in rule.conditions:
            cond_type = condition.get("type", "event_type")
            if cond_type == "event_type" and event.event_type != condition.get("value"):
                return False
            if cond_type == "channel" and event.channel.name != condition.get("value"):
                return False
            if cond_type == "priority":
                priorities = {"LOW": 1, "NORMAL": 2, "HIGH": 3, "CRITICAL": 4}
                if priorities.get(event.priority.name, 0) < priorities.get(condition.get("value", "LOW"), 0):
                    return False
        return True

    def _execute_actions(self, rule: TriggerRule, event: Event) -> Dict[str, Any]:
        results: List[str] = []
        for action in rule.actions:
            action_type = action.get("type", "")
            if action_type == "send_message":
                channel = ChannelType[action.get("channel", "EMAIL")]
                self._message_orchestrator.send_message(
                    event.customer_id, channel,
                    MessageType[action.get("message_type", "ALERT")],
                    subject=action.get("subject", ""),
                    body=action.get("body", ""),
                )
                results.append(f"sent_{channel.name}")
            elif action_type == "update_status":
                status = CustomerStatus[action.get("status", "ACTIVE")]
                self._customer_manager.update_status(event.customer_id, status)
                results.append(f"status_{status.name}")
        return {"actions_executed": results, "rule_id": rule.rule_id}

    def list_rules(self) -> List[TriggerRule]:
        with self._lock:
            return list(self._rules.values())

    def get_fire_stats(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {r.rule_id: {"fire_count": r.fire_count} for r in self._rules.values()}

    def disable_rule(self, rule_id: str) -> bool:
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule:
                rule.is_active = False
                return True
        return False

    def enable_rule(self, rule_id: str) -> bool:
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule:
                rule.is_active = True
                return True
        return False


# =============================================================================
# AUDIENCE BUILDER
# =============================================================================

class AudienceBuilder:
    def __init__(self, customer_manager: CustomerManager,
                 segment_manager: SegmentManager) -> None:
        self._customer_manager = customer_manager
        self._segment_manager = segment_manager
        self._audiences: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def build_audience(self, audience_id: str, name: str,
                       segment_ids: List[str],
                       operator: str = "union") -> Dict[str, Any]:
        customer_ids = self._segment_manager.combine_segments(segment_ids, operator)
        audience = {
            "audience_id": audience_id, "name": name,
            "segment_ids": segment_ids, "operator": operator,
            "size": len(customer_ids), "customer_ids": list(customer_ids),
            "created_at": datetime.now().isoformat(),
        }
        with self._lock:
            self._audiences[audience_id] = audience
        logger.info("Built audience %s: %s (%d customers)", audience_id, name, len(customer_ids))
        return audience

    def get_audience(self, audience_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._audiences.get(audience_id)

    def exclude_audience(self, base_id: str, exclude_id: str) -> Set[str]:
        base = self._audiences.get(base_id)
        exclude = self._audiences.get(exclude_id)
        if not base or not exclude:
            return set()
        return set(base.get("customer_ids", [])) - set(exclude.get("customer_ids", []))

    def intersect_audiences(self, ids: List[str]) -> Set[str]:
        sets = []
        with self._lock:
            for aid in ids:
                aud = self._audiences.get(aid)
                if aud:
                    sets.append(set(aud.get("customer_ids", [])))
        if not sets:
            return set()
        return set.intersection(*sets)

    def list_audiences(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._audiences.values())

    def delete_audience(self, audience_id: str) -> bool:
        with self._lock:
            if audience_id in self._audiences:
                del self._audiences[audience_id]
                return True
        return False

    def refresh_audience(self, audience_id: str) -> Optional[int]:
        with self._lock:
            audience = self._audiences.get(audience_id)
        if not audience:
            return None
        updated = self.build_audience(
            audience_id, audience["name"],
            audience["segment_ids"], audience["operator"],
        )
        return updated.get("size", 0)


# =============================================================================
# CONFIG
# =============================================================================

class Config:
    def __init__(self, default_channel: ChannelType = ChannelType.EMAIL,
                 max_daily_sends: int = 10000, enable_ab_testing: bool = True,
                 enable_journeys: bool = True, scoring_decay_rate: float = 0.95,
                 attribution_model: AttributionModel = AttributionModel.LAST_TOUCH) -> None:
        self.default_channel = default_channel
        self.max_daily_sends = max_daily_sends
        self.enable_ab_testing = enable_ab_testing
        self.enable_journeys = enable_journeys
        self.scoring_decay_rate = scoring_decay_rate
        self.attribution_model = attribution_model


# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class CustomerEngagementAgent:
    def __init__(self, config: Optional[Config] = None) -> None:
        self._config = config or Config()
        self._customer_manager = CustomerManager()
        self._segment_manager = SegmentManager(self._customer_manager)
        self._message_orchestrator = MessageOrchestrator(self._customer_manager)
        self._campaign_manager = CampaignManager(
            self._customer_manager, self._message_orchestrator,
        )
        self._journey_manager = JourneyManager(
            self._customer_manager, self._message_orchestrator,
        )
        self._engagement_scorer = EngagementScorer(self._customer_manager)
        self._attribution_manager = AttributionManager()
        self._personalization_engine = PersonalizationEngine(self._customer_manager)
        self._content_manager = ContentManager()
        self._webhook_manager = WebhookManager()
        self._feedback_collector = FeedbackCollector()
        self._channel_analytics = ChannelAnalytics(self._message_orchestrator)
        self._trigger_engine = TriggerEngine(self._customer_manager, self._message_orchestrator)
        self._audience_builder = AudienceBuilder(self._customer_manager, self._segment_manager)
        self._running = False
        self._lock = threading.Lock()

    def initialize(self) -> Dict[str, Any]:
        logger.info("Initializing CustomerEngagementAgent")
        self._running = True
        self._attribution_manager.set_model(self._config.attribution_model)
        return {
            "status": "initialized",
            "default_channel": self._config.default_channel.name,
            "attribution_model": self._config.attribution_model.name,
        }

    def shutdown(self) -> Dict[str, Any]:
        self._running = False
        logger.info("CustomerEngagementAgent shutdown complete")
        return {"status": "shutdown"}

    def create_customer(self, customer_id: str, email: str = "", phone: str = "",
                        name: str = "", **kwargs: Any) -> Dict[str, Any]:
        customer = self._customer_manager.create_customer(customer_id, email, phone, name, **kwargs)
        return {"customer_id": customer.customer_id, "status": customer.status.name}

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        customer = self._customer_manager.get_customer(customer_id)
        if not customer:
            return {"error": "Customer not found"}
        return {
            "customer_id": customer.customer_id, "name": customer.name,
            "email": customer.email, "status": customer.status.name,
            "engagement_score": customer.engagement_score,
            "lifetime_value": customer.lifetime_value,
            "lifecycle_stage": customer.lifecycle_stage.name,
            "total_purchases": customer.total_purchases,
        }

    def update_customer(self, customer_id: str, **updates: Any) -> Dict[str, Any]:
        customer = self._customer_manager.update_customer(customer_id, **updates)
        if not customer:
            return {"error": "Customer not found"}
        return {"customer_id": customer_id, "updated": list(updates.keys())}

    def record_event(self, customer_id: str, event_type: str,
                     channel: ChannelType = ChannelType.IN_APP,
                     properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        event = Event(
            event_id=str(uuid.uuid4()), customer_id=customer_id,
            event_type=event_type, channel=channel, properties=properties or {},
        )
        self._customer_manager.record_event(event)
        self._engagement_scorer.calculate_score(customer_id)
        self._trigger_engine.process_event(event)
        return {"event_id": event.event_id, "customer_id": customer_id, "event_type": event_type}

    def create_segment(self, segment_id: str, name: str, segment_type: SegmentType,
                       rules: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        segment = self._segment_manager.create_segment(segment_id, name, segment_type, rules)
        return {"segment_id": segment.segment_id, "name": segment.name, "size": segment.size}

    def get_segment_size(self, segment_id: str) -> int:
        return self._segment_manager.get_segment_size(segment_id)

    def send_message(self, customer_id: str, channel: ChannelType, message_type: MessageType,
                     subject: str = "", body: str = "", **kwargs: Any) -> Dict[str, Any]:
        try:
            msg = self._message_orchestrator.send_message(
                customer_id, channel, message_type, subject, body, **kwargs,
            )
            if msg:
                return {"message_id": msg.message_id, "status": "sent"}
            return {"error": "Failed to send"}
        except RateLimitError as e:
            return {"error": str(e)}

    def create_campaign(self, campaign_id: str, name: str, campaign_type: MessageType,
                        channels: List[ChannelType], segment_ids: List[str],
                        subject: str = "", body: str = "") -> Dict[str, Any]:
        campaign = self._campaign_manager.create_campaign(
            campaign_id, name, campaign_type, channels, segment_ids, subject, body,
        )
        return {
            "campaign_id": campaign.campaign_id,
            "name": campaign.name, "status": campaign.status.name,
        }

    def start_campaign(self, campaign_id: str) -> Dict[str, Any]:
        success = self._campaign_manager.start_campaign(campaign_id)
        return {"campaign_id": campaign_id, "started": success}

    def get_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        return self._campaign_manager.get_campaign_performance(campaign_id)

    def create_journey(self, journey_id: str, name: str, trigger_event: str,
                       steps: Optional[List[JourneyStep]] = None) -> Dict[str, Any]:
        journey = self._journey_manager.create_journey(journey_id, name, trigger_event, steps)
        return {"journey_id": journey.journey_id, "name": journey.name}

    def enroll_in_journey(self, journey_id: str, customer_id: str) -> Dict[str, Any]:
        success = self._journey_manager.enroll_customer(journey_id, customer_id)
        return {"enrolled": success, "journey_id": journey_id, "customer_id": customer_id}

    def calculate_engagement_score(self, customer_id: str) -> Dict[str, Any]:
        score = self._engagement_scorer.calculate_score(customer_id)
        return {
            "customer_id": customer_id, "score": score.score,
            "trend": score.trend, "factors": score.factors,
        }

    def get_top_engaged_customers(self, limit: int = 20) -> List[Dict[str, Any]]:
        scores = self._engagement_scorer.get_top_engaged(limit)
        return [
            {"customer_id": s.customer_id, "score": s.score, "trend": s.trend}
            for s in scores
        ]

    def get_attribution(self, customer_id: str) -> Dict[str, Any]:
        return self._attribution_manager.calculate_attribution(customer_id)

    def personalize_content(self, customer_id: str, content: Dict[str, Any]) -> Dict[str, Any]:
        return self._personalization_engine.personalize_content(customer_id, "email", content)

    def get_recommendations(self, customer_id: str) -> List[Dict[str, Any]]:
        return self._personalization_engine.get_recommendations(customer_id)

    def get_send_time(self, customer_id: str) -> Dict[str, Any]:
        return self._personalization_engine.get_optimal_send_time(customer_id)

    def get_channel_stats(self, channel: ChannelType) -> Dict[str, Any]:
        return self._message_orchestrator.get_channel_stats(channel)

    def get_engagement_distribution(self) -> Dict[str, int]:
        return self._engagement_scorer.get_score_distribution()

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "CustomerEngagementAgent", "running": self._running,
            "customers": self._customer_manager.get_customer_count(),
            "segments": len(self._segment_manager.get_all_segments()),
            "campaigns": len(self._campaign_manager.get_all_campaigns()),
            "journeys": len(self._journey_manager.get_all_journeys()),
            "webhooks": len(self._webhook_manager.list_webhooks()),
            "triggers": len(self._trigger_engine.list_rules()),
        }

    def get_full_report(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": self.get_status(),
            "engagement_distribution": self.get_engagement_distribution(),
            "top_engaged": self.get_top_engaged_customers(10),
            "channel_comparison": self._channel_analytics.get_comparison(),
            "feedback_summary": self._feedback_collector.get_feedback_summary(),
            "trigger_stats": self._trigger_engine.get_fire_stats(),
        }


# =============================================================================
# ASYNC WRAPPER
# =============================================================================

class AsyncCustomerEngagementAgent:
    def __init__(self, config: Optional[Config] = None) -> None:
        self._agent = CustomerEngagementAgent(config)

    async def initialize(self) -> Dict[str, Any]:
        return self._agent.initialize()

    async def shutdown(self) -> Dict[str, Any]:
        return self._agent.shutdown()

    async def create_customer(self, customer_id: str, email: str = "",
                              phone: str = "", name: str = "",
                              **kwargs: Any) -> Dict[str, Any]:
        return self._agent.create_customer(customer_id, email, phone, name, **kwargs)

    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self._agent.get_customer(customer_id)

    async def record_event(self, customer_id: str, event_type: str,
                           channel: ChannelType = ChannelType.IN_APP,
                           properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._agent.record_event(customer_id, event_type, channel, properties)

    async def send_message(self, customer_id: str, channel: ChannelType,
                           message_type: MessageType, subject: str = "",
                           body: str = "", **kwargs: Any) -> Dict[str, Any]:
        return self._agent.send_message(customer_id, channel, message_type, subject, body, **kwargs)

    async def create_campaign(self, campaign_id: str, name: str,
                              campaign_type: MessageType, channels: List[ChannelType],
                              segment_ids: List[str], subject: str = "",
                              body: str = "") -> Dict[str, Any]:
        return self._agent.create_campaign(
            campaign_id, name, campaign_type, channels, segment_ids, subject, body,
        )

    async def calculate_engagement_score(self, customer_id: str) -> Dict[str, Any]:
        return self._agent.calculate_engagement_score(customer_id)

    async def get_full_report(self) -> Dict[str, Any]:
        return self._agent.get_full_report()


# =============================================================================
# ENTRY POINT
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("  Customer Engagement Agent - Comprehensive Demo")
    print("=" * 60)
    agent = CustomerEngagementAgent(Config())
    agent.initialize()

    for i in range(10):
        agent.create_customer(
            f"cust_{i:03d}", email=f"user{i}@example.com",
            name=f"User {i}", status=random.choice(list(CustomerStatus)),
        )
    print(f"Created {agent.get_status()['customers']} customers")

    for cid in ["cust_001", "cust_002", "cust_003"]:
        agent.record_event(cid, "page_view", ChannelType.IN_APP)
        agent.record_event(cid, "product_view", ChannelType.IN_APP)
        agent.record_event(cid, "email_open", ChannelType.EMAIL)

    agent.create_segment(
        "seg_active", "Active Customers", SegmentType.BEHAVIORAL,
        [{"field": "status", "operator": "eq", "value": CustomerStatus.ACTIVE}],
    )
    print(f"Segment 'seg_active' size: {agent.get_segment_size('seg_active')}")

    agent.create_campaign(
        "camp_001", "Welcome Campaign", MessageType.ONBOARDING,
        [ChannelType.EMAIL], ["seg_active"], "Welcome!", "Thanks for joining!",
    )
    perf = agent.get_campaign_performance("camp_001")
    print(f"Campaign: {perf.get('name', 'N/A')} | Status: {perf.get('status', 'N/A')}")

    score = agent.calculate_engagement_score("cust_001")
    print(f"Customer cust_001 engagement score: {score.get('score', 0):.1f}")

    dist = agent.get_engagement_distribution()
    print(f"Score distribution: {dist}")

    agent._webhook_manager.register_webhook("wh_001", "https://example.com/hook", ["purchase"])
    agent._feedback_collector.collect_feedback("cust_001", FeedbackType.NPS, 9.0)
    agent._trigger_engine.register_rule(
        "tr_001", "High Value Trigger", TriggerType.THRESHOLD,
        conditions=[{"type": "event_type", "value": "purchase"}],
    )
    agent._content_manager.create_block("cb_001", "Welcome Header", "Hello {{name}}!")
    agent._audience_builder.build_audience("aud_001", "All Active", ["seg_active"])

    report = agent.get_full_report()
    print(f"\nReport: {report['status']}")
    agent.shutdown()
    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
