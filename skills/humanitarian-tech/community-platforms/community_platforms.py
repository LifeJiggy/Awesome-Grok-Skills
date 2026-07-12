"""
Community Platforms Module
Part of the humanitarian-tech skill domain

Comprehensive community engagement platform system covering information sharing,
feedback mechanisms, digital services, and two-way communication.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum, IntEnum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import json
import random
import re
import uuid


# =============================================================================
# Enums
# =============================================================================

class ChannelType(Enum):
    """Communication channel types."""
    SMS = "sms"
    USSD = "ussd"
    IVR = "ivr"
    WEB = "web"
    MOBILE_APP = "mobile_app"
    RADIO = "radio"
    NOTICE_BOARD = "notice_board"
    COMMUNITY_MEETING = "community_meeting"
    HOTLINE = "hotline"
    WHATSAPP = "whatsapp"
    FACEBOOK = "facebook"
    TELEGRAM = "telegram"


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class MessageStatus(Enum):
    """Message delivery status."""
    DRAFT = "draft"
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FeedbackCategory(Enum):
    """Feedback categories."""
    SERVICE_QUALITY = "service_quality"
    COMPLAINT = "complaint"
    SUGGESTION = "suggestion"
    PRAISE = "praise"
    QUESTION = "question"
    REPORT_ABUSE = "report_abuse"
    REQUEST_INFO = "request_info"
    GENERAL = "general"


class FeedbackStatus(Enum):
    """Feedback processing status."""
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    IN_REVIEW = "in_review"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"


class ServiceType(Enum):
    """Digital service types."""
    INFORMATION = "information"
    UTILITY = "utility"
    TRANSACTION = "transaction"
    COMMUNICATION = "communication"
    SUPPORT = "support"
    EDUCATION = "education"
    HEALTH = "health"
    LIVELIHOOD = "livelihood"


class AccessMethod(Enum):
    """Service access methods."""
    WEB = "web"
    MOBILE_APP = "mobile_app"
    USSD = "ussd"
    IVR = "ivr"
    SMS = "sms"
    API = "api"
    BOT = "bot"


class ContentType(Enum):
    """Content types for information hub."""
    ALERT = "alert"
    UPDATE = "update"
    ADVISORY = "advisory"
    GUIDE = "guide"
    FAQ = "faq"
    NEWS = "news"
    ANNOUNCEMENT = "announcement"
    EDUCATIONAL = "educational"


class SentimentType(Enum):
    """Feedback sentiment analysis."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class AudienceType(Enum):
    """Target audience types."""
    ALL = "all"
    SPECIFIC_ZONE = "specific_zone"
    BENEFICIARY_GROUP = "beneficiary_group"
    STAFF = "staff"
    PARTNERS = "partners"
    CUSTOM = "custom"


class Language(Enum):
    """Supported languages."""
    ENGLISH = "en"
    ARABIC = "ar"
    FRENCH = "fr"
    SOMALI = "so"
    SWAHILI = "sw"
    SPANISH = "es"
    HINDI = "hi"
    URDU = "ur"
    TURKISH = "tr"
    AMHARIC = "am"


class ResponseTime(Enum):
    """Expected response time targets."""
    IMMEDIATE = "immediate"
    WITHIN_1_HOUR = "within_1_hour"
    WITHIN_24_HOURS = "within_24_hours"
    WITHIN_3_DAYS = "within_3_days"
    WITHIN_1_WEEK = "within_1_week"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class Channel:
    """Communication channel configuration."""
    channel_id: str
    channel_type: ChannelType
    name: str
    is_enabled: bool = True
    capacity_per_minute: int = 100
    cost_per_message: float = 0.01
    supported_languages: List[Language] = field(default_factory=lambda: [Language.ENGLISH])
    operating_hours: Optional[Tuple[int, int]] = None  # (start_hour, end_hour)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_available(self) -> bool:
        """Check if channel is currently available."""
        if not self.is_enabled:
            return False
        if self.operating_hours:
            current_hour = datetime.now().hour
            start, end = self.operating_hours
            if start <= end:
                return start <= current_hour < end
            else:
                return current_hour >= start or current_hour < end
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "channel_type": self.channel_type.value,
            "name": self.name,
            "is_enabled": self.is_enabled,
            "capacity_per_minute": self.capacity_per_minute,
            "supported_languages": [l.value for l in self.supported_languages]
        }


@dataclass
class Message:
    """Message record for information dissemination."""
    message_id: str
    channel_id: str
    content: str
    priority: MessagePriority
    status: MessageStatus
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    recipient_count: int = 0
    delivered_count: int = 0
    read_count: int = 0
    failed_count: int = 0
    target_audience: AudienceType = AudienceType.ALL
    target_groups: List[str] = field(default_factory=list)
    language: Language = Language.ENGLISH
    expiration_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def delivery_rate(self) -> float:
        if self.recipient_count == 0:
            return 0.0
        return self.delivered_count / self.recipient_count

    @property
    def read_rate(self) -> float:
        if self.delivered_count == 0:
            return 0.0
        return self.read_count / self.delivered_count

    def is_expired(self) -> bool:
        if self.expiration_date is None:
            return False
        return datetime.now() > self.expiration_date

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "channel_id": self.channel_id,
            "content": self.content[:100] + "..." if len(self.content) > 100 else self.content,
            "priority": self.priority.value,
            "status": self.status.value,
            "recipient_count": self.recipient_count,
            "delivery_rate": self.delivery_rate,
            "read_rate": self.read_rate,
            "language": self.language.value,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class InformationItem:
    """Information content item."""
    item_id: str
    title: str
    content: str
    content_type: ContentType
    created_at: datetime
    created_by: str
    is_published: bool = False
    published_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    languages: List[Language] = field(default_factory=lambda: [Language.ENGLISH])
    target_audience: AudienceType = AudienceType.ALL
    tags: List[str] = field(default_factory=list)
    view_count: int = 0
    share_count: int = 0
    verification_status: str = "pending"
    source: str = ""
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_active(self) -> bool:
        if not self.is_published:
            return False
        if self.expires_at and datetime.now() > self.expires_at:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "content_type": self.content_type.value,
            "is_published": self.is_published,
            "languages": [l.value for l in self.languages],
            "view_count": self.view_count,
            "share_count": self.share_count,
            "verification_status": self.verification_status,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class Feedback:
    """Beneficiary feedback record."""
    feedback_id: str
    channel: ChannelType
    beneficiary_id: Optional[str]
    category: FeedbackCategory
    content: str
    submitted_at: datetime
    status: FeedbackStatus = FeedbackStatus.SUBMITTED
    sentiment: SentimentType = SentimentType.NEUTRAL
    response_time_target: ResponseTime = ResponseTime.WITHIN_24_HOURS
    assigned_to: Optional[str] = None
    response: Optional[str] = None
    responded_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    satisfaction_rating: Optional[int] = None
    language: Language = Language.ENGLISH
    is_anonymous: bool = False
    tags: List[str] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)
    escalation_level: int = 0

    @property
    def is_closed(self) -> bool:
        return self.status in (FeedbackStatus.RESOLVED, FeedbackStatus.CLOSED)

    @property
    def response_time_hours(self) -> Optional[float]:
        if self.responded_at:
            return (self.responded_at - self.submitted_at).total_seconds() / 3600
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feedback_id": self.feedback_id,
            "channel": self.channel.value,
            "category": self.category.value,
            "status": self.status.value,
            "sentiment": self.sentiment.value,
            "submitted_at": self.submitted_at.isoformat(),
            "response_time_hours": self.response_time_hours,
            "satisfaction_rating": self.satisfaction_rating,
            "is_anonymous": self.is_anonymous
        }


@dataclass
class DigitalService:
    """Digital service record."""
    service_id: str
    name: str
    service_type: ServiceType
    description: str
    access_methods: List[AccessMethod]
    is_active: bool = True
    availability: str = "24/7"
    languages: List[Language] = field(default_factory=lambda: [Language.ENGLISH])
    total_users: int = 0
    active_users_today: int = 0
    average_rating: float = 0.0
    total_ratings: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: Optional[datetime] = None
    contact_info: str = ""
    url: Optional[str] = None
    ussd_code: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def record_usage(self) -> None:
        """Record a service usage."""
        self.total_users += 1
        self.active_users_today += 1

    def add_rating(self, rating: int) -> None:
        """Add a user rating (1-5)."""
        if 1 <= rating <= 5:
            total = self.average_rating * self.total_ratings
            self.total_ratings += 1
            self.average_rating = (total + rating) / self.total_ratings

    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "name": self.name,
            "service_type": self.service_type.value,
            "description": self.description,
            "access_methods": [a.value for a in self.access_methods],
            "is_active": self.is_active,
            "total_users": self.total_users,
            "average_rating": self.average_rating,
            "languages": [l.value for l in self.languages]
        }


@dataclass
class Dialogue:
    """Community dialogue record."""
    dialogue_id: str
    title: str
    description: str
    facilitator_id: str
    scheduled_at: datetime
    location: str
    target_participants: int
    actual_participants: int = 0
    status: str = "scheduled"
    topics: List[str] = field(default_factory=list)
    outcomes: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    follow_up_actions: List[Dict[str, Any]] = field(default_factory=list)
    feedback_collected: List[Dict[str, Any]] = field(default_factory=list)
    languages_used: List[Language] = field(default_factory=lambda: [Language.ENGLISH])
    notes: str = ""

    @property
    def participation_rate(self) -> float:
        if self.target_participants == 0:
            return 0.0
        return self.actual_participants / self.target_participants

    def record_decision(self, decision: str, responsible: str, deadline: Optional[date] = None) -> None:
        """Record a community decision."""
        self.decisions.append(decision)
        self.follow_up_actions.append({
            "decision": decision,
            "responsible": responsible,
            "deadline": deadline.isoformat() if deadline else None,
            "status": "pending"
        })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dialogue_id": self.dialogue_id,
            "title": self.title,
            "scheduled_at": self.scheduled_at.isoformat(),
            "location": self.location,
            "status": self.status,
            "participation_rate": self.participation_rate,
            "topics": self.topics,
            "decisions_count": len(self.decisions),
            "follow_up_actions": len(self.follow_up_actions)
        }


@dataclass
class UserProfile:
    """User/beneficiary profile for community platform."""
    user_id: str
    name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    preferred_language: Language = Language.ENGLISH
    preferred_channels: List[ChannelType] = field(default_factory=lambda: [ChannelType.SMS])
    location: str = ""
    registration_date: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    consent_given: bool = False
    consent_date: Optional[datetime] = None
    communication_history: List[str] = field(default_factory=list)
    feedback_count: int = 0
    services_used: List[str] = field(default_factory=list)
    accessibility_needs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "preferred_language": self.preferred_language.value,
            "preferred_channels": [c.value for c in self.preferred_channels],
            "location": self.location,
            "is_active": self.is_active,
            "consent_given": self.consent_given,
            "feedback_count": self.feedback_count,
            "services_used": len(self.services_used)
        }


# =============================================================================
# Core Systems
# =============================================================================

class InformationHub:
    """Multi-channel information dissemination system."""

    def __init__(self, languages: Optional[List[str]] = None):
        self.languages = [Language(lang) for lang in (languages or ["en"])]
        self.items: Dict[str, InformationItem] = {}
        self.messages: Dict[str, Message] = {}
        self.channels: Dict[str, Channel] = {}
        self.distribution_log: List[Dict[str, Any]] = []

    def register_channel(self, channel_type: ChannelType, name: str,
                         **kwargs) -> Channel:
        """Register a communication channel."""
        channel_id = f"CH-{uuid.uuid4().hex[:8].upper()}"
        channel = Channel(
            channel_id=channel_id,
            channel_type=channel_type,
            name=name,
            capacity_per_minute=kwargs.get("capacity", 100),
            cost_per_message=kwargs.get("cost", 0.01),
            supported_languages=kwargs.get("languages", self.languages[:1]),
            operating_hours=kwargs.get("operating_hours")
        )
        self.channels[channel_id] = channel
        return channel

    def create_information_item(self, title: str, content: str,
                                content_type: ContentType, created_by: str,
                                languages: Optional[List[Language]] = None,
                                **kwargs) -> InformationItem:
        """Create a new information item."""
        item_id = f"INFO-{uuid.uuid4().hex[:8].upper()}"
        item = InformationItem(
            item_id=item_id,
            title=title,
            content=content,
            content_type=content_type,
            created_at=datetime.now(),
            created_by=created_by,
            languages=languages or self.languages[:1],
            target_audience=kwargs.get("target_audience", AudienceType.ALL),
            tags=kwargs.get("tags", []),
            source=kwargs.get("source", ""),
            expires_at=kwargs.get("expires_at")
        )
        self.items[item_id] = item
        return item

    def publish_item(self, item_id: str) -> bool:
        """Publish an information item."""
        if item_id in self.items:
            self.items[item_id].is_published = True
            self.items[item_id].published_at = datetime.now()
            return True
        return False

    def distribute_update(self, title: str, content: str,
                          channels: List[str], priority: MessagePriority,
                          target_audience: AudienceType = AudienceType.ALL,
                          language: Language = Language.ENGLISH) -> List[Message]:
        """Distribute an update through specified channels."""
        messages = []
        for channel_id in channels:
            if channel_id not in self.channels:
                continue
            channel = self.channels[channel_id]
            if not channel.is_available():
                continue

            message_id = f"MSG-{uuid.uuid4().hex[:8].upper()}"
            message = Message(
                message_id=message_id,
                channel_id=channel_id,
                content=content,
                priority=priority,
                status=MessageStatus.QUEUED,
                created_at=datetime.now(),
                target_audience=target_audience,
                language=language
            )
            self.messages[message_id] = message
            messages.append(message)

            self.distribution_log.append({
                "message_id": message_id,
                "channel_id": channel_id,
                "channel_type": channel.channel_type.value,
                "distributed_at": datetime.now().isoformat()
            })

        return messages

    def get_published_items(self, content_type: Optional[ContentType] = None) -> List[InformationItem]:
        """Get all published information items."""
        items = [i for i in self.items.values() if i.is_active()]
        if content_type:
            items = [i for i in items if i.content_type == content_type]
        return sorted(items, key=lambda i: i.created_at, reverse=True)

    def search_items(self, query: str) -> List[InformationItem]:
        """Search information items by query."""
        query_lower = query.lower()
        return [i for i in self.items.values()
                if query_lower in i.title.lower() or query_lower in i.content.lower()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get information hub statistics."""
        by_type = {}
        by_status = {"draft": 0, "published": 0, "expired": 0}
        total_views = 0
        total_shares = 0

        for item in self.items.values():
            by_type[item.content_type.value] = by_type.get(item.content_type.value, 0) + 1
            if item.is_published:
                by_status["published"] += 1
            else:
                by_status["draft"] += 1
            total_views += item.view_count
            total_shares += item.share_count

        return {
            "total_items": len(self.items),
            "by_type": by_type,
            "by_status": by_status,
            "total_views": total_views,
            "total_shares": total_shares,
            "active_channels": sum(1 for c in self.channels.values() if c.is_enabled),
            "messages_sent": len(self.messages)
        }


class FeedbackManagementSystem:
    """Beneficiary feedback collection and management system."""

    def __init__(self, channels: Optional[List[str]] = None):
        self.channels = channels or ["sms", "web", "hotline"]
        self.feedbacks: Dict[str, Feedback] = {}
        self.categories: Dict[FeedbackCategory, int] = {cat: 0 for cat in FeedbackCategory}
        self.satisfaction_scores: List[int] = []
        self.response_templates: Dict[str, str] = {}
        self.feedback_counter = 0

    def submit_feedback(self, channel: ChannelType, category: FeedbackCategory,
                        content: str, language: Language = Language.ENGLISH,
                        beneficiary_id: Optional[str] = None,
                        is_anonymous: bool = False,
                        **kwargs) -> Feedback:
        """Submit new feedback."""
        self.feedback_counter += 1
        feedback_id = f"FB-{datetime.now().strftime('%Y%m')}-{self.feedback_counter:04d}"

        feedback = Feedback(
            feedback_id=feedback_id,
            channel=channel,
            beneficiary_id=beneficiary_id,
            category=category,
            content=content,
            submitted_at=datetime.now(),
            language=language,
            is_anonymous=is_anonymous,
            tags=kwargs.get("tags", []),
            attachments=kwargs.get("attachments", [])
        )

        self.feedbacks[feedback_id] = feedback
        self.categories[category] += 1
        return feedback

    def acknowledge_feedback(self, feedback_id: str) -> bool:
        """Acknowledge receipt of feedback."""
        if feedback_id in self.feedbacks:
            self.feedbacks[feedback_id].status = FeedbackStatus.ACKNOWLEDGED
            return True
        return False

    def assign_feedback(self, feedback_id: str, staff_id: str) -> bool:
        """Assign feedback to a staff member."""
        if feedback_id in self.feedbacks:
            self.feedbacks[feedback_id].assigned_to = staff_id
            self.feedbacks[feedback_id].status = FeedbackStatus.IN_REVIEW
            return True
        return False

    def respond_to_feedback(self, feedback_id: str, response: str) -> bool:
        """Respond to feedback."""
        if feedback_id in self.feedbacks:
            feedback = self.feedbacks[feedback_id]
            feedback.response = response
            feedback.responded_at = datetime.now()
            feedback.status = FeedbackStatus.IN_PROGRESS
            return True
        return False

    def resolve_feedback(self, feedback_id: str, satisfaction_rating: Optional[int] = None) -> bool:
        """Mark feedback as resolved."""
        if feedback_id in self.feedbacks:
            feedback = self.feedbacks[feedback_id]
            feedback.status = FeedbackStatus.RESOLVED
            feedback.resolved_at = datetime.now()
            if satisfaction_rating:
                feedback.satisfaction_rating = satisfaction_rating
                self.satisfaction_scores.append(satisfaction_rating)
            return True
        return False

    def escalate_feedback(self, feedback_id: str, reason: str) -> bool:
        """Escalate feedback to higher level."""
        if feedback_id in self.feedbacks:
            feedback = self.feedbacks[feedback_id]
            feedback.escalation_level += 1
            feedback.status = FeedbackStatus.ESCALATED
            feedback.tags.append(f"escalated: {reason}")
            return True
        return False

    def analyze_sentiment(self, text: str) -> SentimentType:
        """Simple sentiment analysis based on keywords."""
        positive_words = {"good", "great", "excellent", "thank", "helpful", "satisfied", "happy"}
        negative_words = {"bad", "poor", "terrible", "problem", "issue", "complaint", "unhappy", "slow"}

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return SentimentType.POSITIVE
        elif negative_count > positive_count:
            return SentimentType.NEGATIVE
        return SentimentType.NEUTRAL

    def get_feedback_by_category(self, category: FeedbackCategory,
                                 status: Optional[FeedbackStatus] = None) -> List[Feedback]:
        """Get feedback filtered by category and status."""
        results = []
        for fb in self.feedbacks.values():
            if fb.category == category:
                if status is None or fb.status == status:
                    results.append(fb)
        return sorted(results, key=lambda f: f.submitted_at, reverse=True)

    def get_pending_feedback(self) -> List[Feedback]:
        """Get all unresolved feedback."""
        return [fb for fb in self.feedbacks.values()
                if fb.status not in (FeedbackStatus.RESOLVED, FeedbackStatus.CLOSED)]

    def get_statistics(self) -> Dict[str, Any]:
        """Get feedback system statistics."""
        by_status = {}
        by_channel = {}
        by_sentiment = {}

        for fb in self.feedbacks.values():
            by_status[fb.status.value] = by_status.get(fb.status.value, 0) + 1
            by_channel[fb.channel.value] = by_channel.get(fb.channel.value, 0) + 1
            by_sentiment[fb.sentiment.value] = by_sentiment.get(fb.sentiment.value, 0) + 1

        avg_satisfaction = 0.0
        if self.satisfaction_scores:
            avg_satisfaction = sum(self.satisfaction_scores) / len(self.satisfaction_scores)

        response_times = [fb.response_time_hours for fb in self.feedbacks.values() if fb.response_time_hours]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return {
            "total_feedback": len(self.feedbacks),
            "by_category": {k.value: v for k, v in self.categories.items() if v > 0},
            "by_status": by_status,
            "by_channel": by_channel,
            "by_sentiment": by_sentiment,
            "average_satisfaction": avg_satisfaction,
            "average_response_time_hours": avg_response_time,
            "response_rate": sum(1 for fb in self.feedbacks.values() if fb.responded_at) / max(len(self.feedbacks), 1)
        }


class DigitalServicePortal:
    """Digital services directory and management system."""

    def __init__(self, mobile_enabled: bool = True):
        self.mobile_enabled = mobile_enabled
        self.services: Dict[str, DigitalService] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self.usage_log: List[Dict[str, Any]] = []

    def register_service(self, name: str, service_type: ServiceType,
                         description: str, access_methods: List[AccessMethod],
                         languages: Optional[List[Language]] = None,
                         **kwargs) -> DigitalService:
        """Register a new digital service."""
        service_id = f"SVC-{uuid.uuid4().hex[:8].upper()}"
        service = DigitalService(
            service_id=service_id,
            name=name,
            service_type=service_type,
            description=description,
            access_methods=access_methods,
            languages=languages or [Language.ENGLISH],
            availability=kwargs.get("availability", "24/7"),
            contact_info=kwargs.get("contact_info", ""),
            url=kwargs.get("url"),
            ussd_code=kwargs.get("ussd_code")
        )
        self.services[service_id] = service
        return service

    def record_service_usage(self, service_id: str, user_id: str,
                             access_method: AccessMethod) -> Dict[str, Any]:
        """Record service usage."""
        service = self.services.get(service_id)
        if not service:
            return {"success": False, "error": "Service not found"}

        service.record_usage()
        usage_record = {
            "service_id": service_id,
            "user_id": user_id,
            "access_method": access_method.value,
            "timestamp": datetime.now().isoformat()
        }
        self.usage_log.append(usage_record)
        return {"success": True, "record": usage_record}

    def rate_service(self, service_id: str, rating: int) -> bool:
        """Rate a service."""
        service = self.services.get(service_id)
        if service and 1 <= rating <= 5:
            service.add_rating(rating)
            return True
        return False

    def get_services_by_type(self, service_type: ServiceType) -> List[DigitalService]:
        """Get services filtered by type."""
        return [s for s in self.services.values()
                if s.service_type == service_type and s.is_active]

    def get_services_by_access(self, access_method: AccessMethod) -> List[DigitalService]:
        """Get services available via specific access method."""
        return [s for s in self.services.values()
                if access_method in s.access_methods and s.is_active]

    def search_services(self, query: str) -> List[DigitalService]:
        """Search services by query."""
        query_lower = query.lower()
        return [s for s in self.services.values()
                if query_lower in s.name.lower() or query_lower in s.description.lower()]

    def get_popular_services(self, limit: int = 10) -> List[DigitalService]:
        """Get most popular services by usage."""
        return sorted(self.services.values(), key=lambda s: s.total_users, reverse=True)[:limit]

    def get_statistics(self) -> Dict[str, Any]:
        """Get digital service statistics."""
        by_type = {}
        by_access = {}
        total_users = 0
        total_ratings = 0

        for service in self.services.values():
            by_type[service.service_type.value] = by_type.get(service.service_type.value, 0) + 1
            for method in service.access_methods:
                by_access[method.value] = by_access.get(method.value, 0) + 1
            total_users += service.total_users
            total_ratings += service.total_ratings

        return {
            "total_services": len(self.services),
            "active_services": sum(1 for s in self.services.values() if s.is_active),
            "by_type": by_type,
            "by_access_method": by_access,
            "total_users": total_users,
            "total_ratings": total_ratings
        }


class CommunityCommunicationManager:
    """Two-way communication and community dialogue management."""

    def __init__(self, consent_manager: bool = True):
        self.consent_manager = consent_manager
        self.users: Dict[str, UserProfile] = {}
        self.dialogues: Dict[str, Dialogue] = {}
        self.consent_registry: Dict[str, bool] = {}
        self.communication_log: List[Dict[str, Any]] = []
        self.dialogue_counter = 0

    def register_user(self, name: str, preferred_language: Language = Language.ENGLISH,
                      phone_number: Optional[str] = None,
                      preferred_channels: Optional[List[ChannelType]] = None,
                      **kwargs) -> UserProfile:
        """Register a new user."""
        user_id = f"USR-{uuid.uuid4().hex[:8].upper()}"
        user = UserProfile(
            user_id=user_id,
            name=name,
            phone_number=phone_number,
            preferred_language=preferred_language,
            preferred_channels=preferred_channels or [ChannelType.SMS],
            location=kwargs.get("location", ""),
            consent_given=kwargs.get("consent_given", False),
            consent_date=datetime.now() if kwargs.get("consent_given") else None,
            accessibility_needs=kwargs.get("accessibility_needs", [])
        )
        self.users[user_id] = user
        if self.consent_manager:
            self.consent_registry[user_id] = user.consent_given
        return user

    def update_consent(self, user_id: str, consent_given: bool) -> bool:
        """Update user consent status."""
        if user_id in self.users:
            self.users[user_id].consent_given = consent_given
            self.users[user_id].consent_date = datetime.now() if consent_given else None
            self.consent_registry[user_id] = consent_given
            return True
        return False

    def schedule_dialogue(self, title: str, description: str, facilitator_id: str,
                          scheduled_at: datetime, location: str,
                          target_participants: int,
                          topics: Optional[List[str]] = None) -> Dialogue:
        """Schedule a community dialogue."""
        self.dialogue_counter += 1
        dialogue_id = f"DLG-{self.dialogue_counter:04d}"

        dialogue = Dialogue(
            dialogue_id=dialogue_id,
            title=title,
            description=description,
            facilitator_id=facilitator_id,
            scheduled_at=scheduled_at,
            location=location,
            target_participants=target_participants,
            topics=topics or []
        )
        self.dialogues[dialogue_id] = dialogue
        return dialogue

    def conduct_dialogue(self, dialogue_id: str, actual_participants: int,
                         outcomes: List[str], decisions: List[str]) -> bool:
        """Record dialogue conduct."""
        if dialogue_id in self.dialogues:
            dialogue = self.dialogues[dialogue_id]
            dialogue.actual_participants = actual_participants
            dialogue.outcomes = outcomes
            dialogue.decisions = decisions
            dialogue.status = "completed"
            return True
        return False

    def record_follow_up(self, dialogue_id: str, action: str,
                         responsible: str, deadline: Optional[date] = None) -> bool:
        """Record follow-up action from dialogue."""
        if dialogue_id in self.dialogues:
            self.dialogues[dialogue_id].record_decision(action, responsible, deadline)
            return True
        return False

    def send_direct_message(self, sender_id: str, recipient_id: str,
                            content: str, channel: ChannelType) -> Dict[str, Any]:
        """Send a direct message between users."""
        if recipient_id not in self.users:
            return {"success": False, "error": "Recipient not found"}

        recipient = self.users[recipient_id]
        if self.consent_manager and not recipient.consent_given:
            return {"success": False, "error": "Recipient has not consented to communications"}

        message_record = {
            "message_id": f"DM-{uuid.uuid4().hex[:8].upper()}",
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "channel": channel.value,
            "content": content[:100] + "..." if len(content) > 100 else content,
            "sent_at": datetime.now().isoformat()
        }
        self.communication_log.append(message_record)
        return {"success": True, "record": message_record}

    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile."""
        return self.users.get(user_id)

    def get_users_by_location(self, location: str) -> List[UserProfile]:
        """Get users by location."""
        return [u for u in self.users.values() if u.location == location]

    def get_users_by_language(self, language: Language) -> List[UserProfile]:
        """Get users by preferred language."""
        return [u for u in self.users.values() if u.preferred_language == language]

    def get_active_dialogues(self) -> List[Dialogue]:
        """Get all scheduled or in-progress dialogues."""
        return [d for d in self.dialogues.values() if d.status in ("scheduled", "in_progress")]

    def get_dialogue_history(self) -> List[Dialogue]:
        """Get completed dialogues."""
        return [d for d in self.dialogues.values() if d.status == "completed"]

    def get_statistics(self) -> Dict[str, Any]:
        """Get communication manager statistics."""
        by_language = {}
        consent_count = 0

        for user in self.users.values():
            by_language[user.preferred_language.value] = by_language.get(user.preferred_language.value, 0) + 1
            if user.consent_given:
                consent_count += 1

        return {
            "total_users": len(self.users),
            "by_language": by_language,
            "consent_rate": consent_count / max(len(self.users), 1),
            "total_dialogues": len(self.dialogues),
            "completed_dialogues": sum(1 for d in self.dialogues.values() if d.status == "completed"),
            "total_messages": len(self.communication_log)
        }


# =============================================================================
# Main Demo Function
# =============================================================================

def main() -> None:
    """Demonstrate the community platforms system capabilities."""
    print("=" * 70)
    print("  COMMUNITY PLATFORMS SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # --- Information Hub ---
    print("\n[1] INFORMATION HUB")
    print("-" * 40)
    info_hub = InformationHub(languages=["en", "ar", "fr", "so"])

    # Register channels
    channels = [
        (ChannelType.SMS, "SMS Gateway", 500, 0.02),
        (ChannelType.RADIO, "Community Radio", 1000, 0.0),
        (ChannelType.NOTICE_BOARD, "Camp Notice Boards", 200, 0.0),
        (ChannelType.WHATSAPP, "WhatsApp Broadcast", 300, 0.01),
    ]
    for ctype, name, capacity, cost in channels:
        channel = info_hub.register_channel(ctype, name, capacity=capacity, cost=cost)
        print(f"  Registered channel: {name} ({ctype.value})")

    # Create information items
    items_data = [
        ("Water Distribution Schedule", "Water distribution at Zone A will occur daily from 6-8 AM. "
         "Please bring your water cards. Queue management tokens available at registration desk.",
         ContentType.UPDATE, ["water", "distribution"]),
        ("Health Clinic Hours", "The health clinic in Zone B operates from 8 AM to 4 PM, Monday to Saturday. "
         "Emergency services available 24/7. Bring your health card.",
         ContentType.GUIDE, ["health", "clinic"]),
        ("Vaccination Campaign", "A measles vaccination campaign will start next week for all children under 5. "
         "More details to follow.",
         ContentType.ANNOUNCEMENT, ["health", "vaccination", "children"]),
    ]

    for title, content, ctype, tags in items_data:
        item = info_hub.create_information_item(
            title=title,
            content=content,
            content_type=ctype,
            created_by="OCHA Communication Team",
            tags=tags
        )
        info_hub.publish_item(item.item_id)
        print(f"\n  Published: {item.title}")
        print(f"    Type: {item.content_type.value}, Tags: {', '.join(item.tags)}")

    # Distribute updates
    print("\n  Distributing emergency update...")
    messages = info_hub.distribute_update(
        title="Flash Flood Warning",
        content="Flash flood warning for Zone C. Residents in low-lying areas should move to higher ground immediately.",
        channels=["CH-" + ch for ch in list(info_hub.channels.keys())[:2]],
        priority=MessagePriority.URGENT,
        target_audience=AudienceType.SPECIFIC_ZONE
    )
    print(f"    Sent to {len(messages)} channels")

    print(f"\n  Information Hub Statistics:")
    stats = info_hub.get_statistics()
    print(f"    Total items: {stats['total_items']}")
    print(f"    Active channels: {stats['active_channels']}")
    print(f"    Messages sent: {stats['messages_sent']}")

    # --- Feedback System ---
    print("\n\n[2] FEEDBACK MANAGEMENT SYSTEM")
    print("-" * 40)
    feedback_system = FeedbackManagementSystem()

    # Submit feedback
    feedback_data = [
        (ChannelType.SMS, FeedbackCategory.COMPLAINT, "The water queue was too long today. Waited for 2 hours.",
         "so", True),
        (ChannelType.WEB, FeedbackCategory.SUGGESTION, "Could we have more distribution points in Zone B?",
         "en", False),
        (ChannelType.HOTLINE, FeedbackCategory.PRAISE, "The health clinic staff were very helpful and professional.",
         "en", False),
        (ChannelType.SMS, FeedbackCategory.SERVICE_QUALITY, "The new digital service for finding water points is excellent.",
         "en", True),
        (ChannelType.WEB, FeedbackCategory.COMPLAINT, "I was unable to access the education center due to overcrowding.",
         "fr", False),
    ]

    feedbacks = []
    for channel, category, content, lang, anon in feedback_data:
        fb = feedback_system.submit_feedback(
            channel=channel,
            category=category,
            content=content,
            language=Language(lang),
            is_anonymous=anon
        )
        feedbacks.append(fb)
        sentiment = feedback_system.analyze_sentiment(content)
        fb.sentiment = sentiment
        print(f"  Feedback {fb.feedback_id}: {category.value} ({sentiment.value})")

    # Process feedback
    print("\n  Processing feedback...")
    for fb in feedbacks[:3]:
        feedback_system.acknowledge_feedback(fb.feedback_id)
        feedback_system.assign_feedback(fb.feedback_id, "STAFF-001")
        feedback_system.respond_to_feedback(fb.feedback_id, f"Thank you for your feedback regarding {fb.category.value}. We are looking into this matter.")
        feedback_system.resolve_feedback(fb.feedback_id, satisfaction_rating=random.randint(3, 5))
        print(f"    Processed: {fb.feedback_id}")

    fb_stats = feedback_system.get_statistics()
    print(f"\n  Feedback Statistics:")
    print(f"    Total feedback: {fb_stats['total_feedback']}")
    print(f"    By category: {fb_stats['by_category']}")
    print(f"    Average satisfaction: {fb_stats['average_satisfaction']:.1f}/5")
    print(f"    Response rate: {fb_stats['response_rate']:.1%}")

    # --- Digital Services ---
    print("\n\n[3] DIGITAL SERVICE PORTAL")
    print("-" * 40)
    service_portal = DigitalServicePortal(mobile_enabled=True)

    # Register services
    services_data = [
        ("Water Point Locator", ServiceType.UTILITY, "Find nearest water points and queue status",
         [AccessMethod.USSD, AccessMethod.MOBILE_APP], "#123"),
        ("Health Information", ServiceType.HEALTH, "Access health advisories and clinic schedules",
         [AccessMethod.WEB, AccessMethod.SMS], "https://health.example.org"),
        ("Aid Distribution Schedule", ServiceType.INFORMATION, "View upcoming distribution events",
         [AccessMethod.USSD, AccessMethod.IVR, AccessMethod.WEB], "#456"),
        ("Feedback Portal", ServiceType.COMMUNICATION, "Submit feedback and complaints",
         [AccessMethod.WEB, AccessMethod.MOBILE_APP, AccessMethod.SMS], "https://feedback.example.org"),
        ("Education Resources", ServiceType.EDUCATION, "Access learning materials and class schedules",
         [AccessMethod.WEB, AccessMethod.MOBILE_APP], "https://edu.example.org"),
    ]

    for name, stype, desc, methods, code in services_data:
        service = service_portal.register_service(
            name=name,
            service_type=stype,
            description=desc,
            access_methods=methods,
            ussd_code=code if code.startswith("#") else None,
            url=code if code.startswith("http") else None
        )
        print(f"  Registered service: {name} ({stype.value})")
        print(f"    Access: {', '.join([m.value for m in methods])}")

    # Record usage
    print("\n  Recording service usage...")
    for service in list(service_portal.services.values())[:3]:
        for _ in range(random.randint(10, 50)):
            service_portal.record_service_usage(service.service_id, f"USR-{random.randint(1000, 9999)}",
                                                random.choice(service.access_methods))
        service_portal.rate_service(service.service_id, random.randint(3, 5))
        print(f"    {service.name}: {service.total_users} users, rating: {service.average_rating:.1f}")

    svc_stats = service_portal.get_statistics()
    print(f"\n  Digital Service Statistics:")
    print(f"    Total services: {svc_stats['total_services']}")
    print(f"    Active services: {svc_stats['active_services']}")
    print(f"    Total users: {svc_stats['total_users']}")
    print(f"    By type: {svc_stats['by_type']}")

    # --- Communication Manager ---
    print("\n\n[4] COMMUNICATION MANAGER")
    print("-" * 40)
    comm_manager = CommunityCommunicationManager(consent_manager=True)

    # Register users
    users_data = [
        ("Amina Hassan", Language.SOMALI, "+254-700-123456", [ChannelType.SMS, ChannelType.WHATSAPP], "Zone_A"),
        ("Jean Baptiste", Language.FRENCH, "+254-700-234567", [ChannelType.SMS, ChannelType.WEB], "Zone_A"),
        ("Fatima Al-Said", Language.ARABIC, "+254-700-345678", [ChannelType.SMS, ChannelType.IVR], "Zone_B"),
        ("Li Wei", Language.ENGLISH, None, [ChannelType.WEB, ChannelType.MOBILE_APP], "Zone_B"),
        ("Maria Santos", Language.SPANISH, "+254-700-456789", [ChannelType.SMS], "Zone_C"),
    ]

    for name, lang, phone, channels, loc in users_data:
        user = comm_manager.register_user(
            name=name,
            preferred_language=lang,
            phone_number=phone,
            preferred_channels=channels,
            location=loc,
            consent_given=True
        )
        print(f"  Registered user: {user.name} ({user.preferred_language.value}, {loc})")

    # Schedule dialogues
    dialogues = [
        ("Community Feedback Session", "Monthly feedback session on water and sanitation services",
         "USR-001", datetime.now() + timedelta(days=3), "Community Center", 50,
         ["water_access", "sanitation", "maintenance"]),
        ("Youth Education Forum", "Discussion on education needs and opportunities for youth",
         "USR-002", datetime.now() + timedelta(days=5), "School Compound", 30,
         ["education", "youth", "skills_training"]),
    ]

    for title, desc, facilitator, scheduled, location, participants, topics in dialogues:
        dialogue = comm_manager.schedule_dialogue(
            title=title,
            description=desc,
            facilitator_id=facilitator,
            scheduled_at=scheduled,
            location=location,
            target_participants=participants,
            topics=topics
        )
        print(f"\n  Scheduled dialogue: {dialogue.title}")
        print(f"    Date: {dialogue.scheduled_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"    Location: {dialogue.location}")
        print(f"    Topics: {', '.join(dialogue.topics)}")

    # Conduct a dialogue
    first_dialogue = list(comm_manager.dialogues.values())[0]
    comm_manager.conduct_dialogue(
        first_dialogue.dialogue_id,
        actual_participants=45,
        outcomes=["High demand for additional water points", "Request for extended clinic hours"],
        decisions=["Install 2 new water points in Zone A", "Extend clinic hours by 1 hour on weekdays"]
    )
    comm_manager.record_follow_up(
        first_dialogue.dialogue_id,
        "Install new water points",
        "WASH Team",
        date.today() + timedelta(days=14)
    )
    print(f"\n  Conducted dialogue: {first_dialogue.title}")
    print(f"    Participants: {first_dialogue.actual_participants} ({first_dialogue.participation_rate:.0%})")
    print(f"    Decisions: {len(first_dialogue.decisions)}")

    # Send direct messages
    users = list(comm_manager.users.values())
    if len(users) >= 2:
        result = comm_manager.send_direct_message(
            users[0].user_id,
            users[1].user_id,
            "Thank you for attending the community dialogue. Your input was valuable.",
            ChannelType.SMS
        )
        print(f"\n  Direct message sent: {result['success']}")

    comm_stats = comm_manager.get_statistics()
    print(f"\n  Communication Statistics:")
    print(f"    Total users: {comm_stats['total_users']}")
    print(f"    By language: {comm_stats['by_language']}")
    print(f"    Consent rate: {comm_stats['consent_rate']:.0%}")
    print(f"    Completed dialogues: {comm_stats['completed_dialogues']}")

    # --- Summary ---
    print("\n\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n  Components demonstrated:")
    print("    1. Information Hub - multi-channel publishing and distribution")
    print("    2. Feedback System - collection, processing, and sentiment analysis")
    print("    3. Digital Services - service directory and usage tracking")
    print("    4. Communication Manager - user registration, dialogues, messaging")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()