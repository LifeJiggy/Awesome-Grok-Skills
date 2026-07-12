"""
Citizen Services Module — Digital Government and Community Engagement Platform

Provides comprehensive digital government capabilities including 311 service
request management, permit applications, public records processing, community
engagement, multilingual service delivery, and equity analytics.

Domain: Smart Cities > Citizen Services
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EngineStatus(Enum):
    """Operational state of the citizen services engine."""
    UNINITIALIZED = auto()
    CONFIGURING = auto()
    READY = auto()
    RUNNING = auto()
    ERROR = auto()
    SHUTDOWN = auto()


class RequestType(Enum):
    """Types of 311 service requests."""
    POTHOLE = "pothole"
    STREETLIGHT = "streetlight_outage"
    GRAFFITI = "graffiti_removal"
    NOISE_COMPLAINT = "noise_complaint"
    TRASH_COLLECTION = "trash_collection"
    CODE_VIOLATION = "code_violation"
    TREE_MAINTENANCE = "tree_maintenance"
    SIDEWALK_REPAIR = "sidewalk_repair"
    ABANDONED_VEHICLE = "abandoned_vehicle"
    WATER_LEAK = "water_leak"


class RequestStatus(Enum):
    """Service request lifecycle status."""
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"
    CLOSED = "closed"
    REJECTED = "rejected"


class Priority(Enum):
    """Service request priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class PermitType(Enum):
    """Types of permits and licenses."""
    BUILDING_RESIDENTIAL = "building_residential"
    BUILDING_COMMERCIAL = "building_commercial"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    DEMOLITION = "demolition"
    BUSINESS_LICENSE = "business_license"
    EVENT_PERMIT = "event_permit"
    FOOD_SERVICE = "food_service"
    SIGN_PERMIT = "sign_permit"


class PermitStatus(Enum):
    """Permit application status."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ADDITIONAL_INFO_NEEDED = "additional_info_needed"
    APPROVED = "approved"
    CONDITIONALLY_APPROVED = "conditionally_approved"
    DENIED = "denied"
    EXPIRED = "expired"


class EngagementType(Enum):
    """Community engagement formats."""
    SURVEY = "survey"
    TOWN_HALL = "town_hall"
    WORKSHOP = "workshop"
    ONLINE_FORUM = "online_forum"
    PARTICIPATORY_BUDGETING = "participatory_budgeting"


class NotificationChannel(Enum):
    """Notification delivery channels."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    PHONE = "phone"
    POSTAL = "postal"


class ServiceMetric(Enum):
    """Service delivery performance metrics."""
    RESPONSE_TIME = "response_time"
    RESOLUTION_TIME = "resolution_time"
    SATISFACTION_SCORE = "satisfaction_score"
    FIRST_CONTACT_RESOLUTION = "first_contact_resolution"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ServiceConfig:
    """Configuration for citizen services operations."""
    request_types: int = 0
    departments: int = 0
    avg_daily_requests: int = 0
    sla_targets: Dict[str, int] = field(default_factory=dict)
    supported_languages: int = 1
    accessibility_level: str = "wcag_2.1_aa"


@dataclass
class ChannelConfig:
    """Available service delivery channels."""
    web_portal: bool = True
    mobile_app: bool = True
    phone_311: bool = True
    sms: bool = True
    email: bool = True
    walk_in_kiosks: int = 0
    chatbot: bool = False


@dataclass
class ServiceRequest:
    """A 311 service request."""
    request_id: str
    request_type: RequestType
    description: str
    address: str
    latitude: float
    longitude: float
    priority: Priority
    status: RequestStatus = RequestStatus.SUBMITTED
    reporter_phone: Optional[str] = None
    anonymous: bool = False
    department: str = ""
    work_order_id: Optional[str] = None
    sla_deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    photos: List[str] = field(default_factory=list)


@dataclass
class ServiceStatus:
    """Current status of a service request."""
    request_id: str
    current_status: RequestStatus
    last_update: str
    work_order_id: Optional[str] = None
    assigned_to: Optional[str] = None


@dataclass
class PermitApplication:
    """A permit or license application."""
    application_id: str
    permit_type: PermitType
    project_description: str
    property_address: str
    parcel_id: str
    applicant_name: str
    applicant_email: str
    contractor_name: Optional[str] = None
    contractor_license: Optional[str] = None
    estimated_value: float = 0.0
    total_fees: float = 0.0
    estimated_review_days: int = 30
    status: PermitStatus = PermitStatus.SUBMITTED
    submitted_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ReviewStatus:
    """Current review status of a permit application."""
    application_id: str
    current_stage: str
    assigned_reviewer: Optional[str] = None
    conditions: Optional[str] = None
    comments: List[str] = field(default_factory=list)


@dataclass
class Survey:
    """Community survey."""
    survey_id: str
    title: str
    description: str
    engagement_type: EngagementType
    questions: List[Dict[str, Any]]
    target_audience: str
    duration_days: int
    languages: List[str] = field(default_factory=lambda: ["en"])
    response_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SurveyResults:
    """Survey results summary."""
    survey_id: str
    total_responses: int
    response_rate: float
    questions: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class FOIARequest:
    """Freedom of Information Act request."""
    request_id: str
    requester_name: str
    requester_email: str
    description: str
    department: str
    format_preferred: str = "electronic"
    estimated_completion_date: Optional[str] = None
    estimated_fees: float = 0.0
    status: str = "submitted"
    pages_identified: int = 0
    exemptions: List[str] = field(default_factory=list)


@dataclass
class NotificationPreference:
    """Citizen notification preferences."""
    citizen_id: str
    preferences: Dict[str, List[NotificationChannel]] = field(default_factory=dict)
    quiet_hours: Optional[Dict[str, str]] = None
    language: str = "en"


@dataclass
class BulkNotification:
    """Result of a bulk notification send."""
    notification_id: str
    template: str
    recipient_count: int
    channels_used: List[NotificationChannel]
    sent_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DimensionBreakdown:
    """Equity analysis breakdown by dimension."""
    dimension: str
    group_name: str
    avg_value: float
    disparity_ratio: float
    sample_size: int = 0


@dataclass
class EquityReport:
    """Equity analysis report for a service type."""
    service_type: str
    metric: ServiceMetric
    overall_avg: float
    dimension_breakdown: List[DimensionBreakdown] = field(default_factory=list)
    time_period_days: int = 90


@dataclass
class EquityRecommendation:
    """Equity improvement recommendation."""
    description: str
    expected_impact: str
    priority: Priority = Priority.HIGH


# ---------------------------------------------------------------------------
# Helper Classes
# ---------------------------------------------------------------------------

class ServiceRequestManager:
    """Manages 311 service request lifecycle."""

    def __init__(self, engine: "CitizenServicesEngine") -> None:
        self._engine = engine

    def create_request(
        self,
        request_type: RequestType,
        description: str,
        location: Dict[str, Any],
        photos: Optional[List[str]] = None,
        reporter_contact: Optional[Dict[str, str]] = None,
        anonymous: bool = False,
        priority: Priority = Priority.MEDIUM,
    ) -> ServiceRequest:
        request = ServiceRequest(
            request_id=f"sr-{uuid.uuid4().hex[:8]}",
            request_type=request_type,
            description=description,
            address=location.get("address", ""),
            latitude=location.get("lat", 0.0),
            longitude=location.get("lon", 0.0),
            priority=priority,
            reporter_phone=reporter_contact.get("phone") if reporter_contact else None,
            anonymous=anonymous,
            photos=photos or [],
            department=self._assign_department(request_type),
        )

        sla_hours = self._engine._service_config.sla_targets.get(request_type.value, 72)
        request.sla_deadline = datetime.utcnow() + timedelta(hours=sla_hours)

        self._engine._requests[request.request_id] = request
        logger.info("Service request %s created: %s", request.request_id, request_type.value)
        return request

    def get_status(self, request_id: str) -> ServiceStatus:
        request = self._engine._requests.get(request_id)
        if request is None:
            raise KeyError(f"Request not found: {request_id}")

        return ServiceStatus(
            request_id=request_id,
            current_status=request.status,
            last_update=request.updated_at.isoformat(),
            work_order_id=request.work_order_id,
        )

    def _assign_department(self, request_type: RequestType) -> str:
        mapping = {
            RequestType.POTHOLE: "public_works",
            RequestType.STREETLIGHT: "public_works",
            RequestType.GRAFFITI: "public_works",
            RequestType.NOISE_COMPLAINT: "code_enforcement",
            RequestType.TRASH_COLLECTION: "sanitation",
            RequestType.CODE_VIOLATION: "code_enforcement",
            RequestType.TREE_MAINTENANCE: "parks",
            RequestType.SIDEWALK_REPAIR: "public_works",
            RequestType.ABANDONED_VEHICLE: "police",
            RequestType.WATER_LEAK: "water_utility",
        }
        return mapping.get(request_type, "general")


class PermitManager:
    """Manages permit and license applications."""

    def __init__(self, engine: "CitizenServicesEngine") -> None:
        self._engine = engine

    def submit_application(
        self,
        permit_type: PermitType,
        project_description: str,
        property_address: str,
        parcel_id: str,
        applicant: Dict[str, str],
        contractor: Optional[Dict[str, str]] = None,
        estimated_value: float = 0.0,
        documents: Optional[List[str]] = None,
    ) -> PermitApplication:
        fee_schedule = {
            PermitType.BUILDING_RESIDENTIAL: 0.02,
            PermitType.BUILDING_COMMERCIAL: 0.025,
            PermitType.ELECTRICAL: 150.0,
            PermitType.PLUMBING: 125.0,
            PermitType.DEMOLITION: 500.0,
            PermitType.BUSINESS_LICENSE: 250.0,
            PermitType.EVENT_PERMIT: 100.0,
            PermitType.FOOD_SERVICE: 300.0,
            PermitType.SIGN_PERMIT: 200.0,
        }
        rate = fee_schedule.get(permit_type, 100.0)
        total_fees = rate * estimated_value if rate < 1.0 else rate

        application = PermitApplication(
            application_id=f"perm-{uuid.uuid4().hex[:8]}",
            permit_type=permit_type,
            project_description=project_description,
            property_address=property_address,
            parcel_id=parcel_id,
            applicant_name=applicant.get("name", ""),
            applicant_email=applicant.get("email", ""),
            contractor_name=contractor.get("name") if contractor else None,
            contractor_license=contractor.get("license_number") if contractor else None,
            estimated_value=estimated_value,
            total_fees=round(total_fees, 2),
            estimated_review_days=self._get_review_days(permit_type),
        )

        self._engine._permits[application.application_id] = application
        return application

    def get_review_status(self, application_id: str) -> ReviewStatus:
        permit = self._engine._permits.get(application_id)
        if permit is None:
            raise KeyError(f"Permit not found: {application_id}")

        return ReviewStatus(
            application_id=application_id,
            current_stage=permit.status.value,
            assigned_reviewer=f"reviewer-{uuid.uuid4().hex[:4]}",
        )

    def _get_review_days(self, permit_type: PermitType) -> int:
        review_days = {
            PermitType.BUILDING_RESIDENTIAL: 14,
            PermitType.BUILDING_COMMERCIAL: 30,
            PermitType.ELECTRICAL: 10,
            PermitType.PLUMBING: 10,
            PermitType.DEMOLITION: 21,
            PermitType.BUSINESS_LICENSE: 7,
            PermitType.EVENT_PERMIT: 14,
            PermitType.FOOD_SERVICE: 21,
            PermitType.SIGN_PERMIT: 14,
        }
        return review_days.get(permit_type, 14)


class EngagementPlatform:
    """Community engagement and participatory tools."""

    def __init__(self, engine: "CitizenServicesEngine") -> None:
        self._engine = engine

    def create_survey(
        self,
        title: str,
        description: str,
        engagement_type: EngagementType,
        questions: List[Dict[str, Any]],
        target_audience: str,
        duration_days: int = 30,
        languages: Optional[List[str]] = None,
    ) -> Survey:
        survey = Survey(
            survey_id=f"srv-{uuid.uuid4().hex[:8]}",
            title=title,
            description=description,
            engagement_type=engagement_type,
            questions=questions,
            target_audience=target_audience,
            duration_days=duration_days,
            languages=languages or ["en"],
        )
        self._engine._surveys[survey.survey_id] = survey
        return survey

    def get_survey_results(self, survey_id: str) -> SurveyResults:
        survey = self._engine._surveys.get(survey_id)
        if survey is None:
            raise KeyError(f"Survey not found: {survey_id}")

        import random
        random.seed(hash(survey_id) % 2**31)

        question_results = []
        for q in survey.questions:
            question_results.append({
                "text": q.get("question", ""),
                "response_rate": round(random.uniform(0.5, 0.9), 2),
                "top_answer": q.get("options", ["N/A"])[0] if q.get("options") else "N/A",
            })

        return SurveyResults(
            survey_id=survey_id,
            total_responses=random.randint(50, 500),
            response_rate=round(random.uniform(0.15, 0.45), 2),
            questions=question_results,
        )


class PublicRecordsManager:
    """Public records and FOIA request management."""

    def __init__(self, engine: "CitizenServicesEngine") -> None:
        self._engine = engine

    def submit_request(
        self,
        requester: Dict[str, str],
        description: str,
        department: str,
        format_preferred: str = "electronic",
    ) -> FOIARequest:
        request = FOIARequest(
            request_id=f"foia-{uuid.uuid4().hex[:8]}",
            requester_name=requester.get("name", ""),
            requester_email=requester.get("email", ""),
            description=description,
            department=department,
            format_preferred=format_preferred,
            estimated_completion_date=(
                datetime.utcnow() + timedelta(days=15)
            ).strftime("%Y-%m-%d"),
            estimated_fees=0.0,
        )
        self._engine._foia_requests[request.request_id] = request
        return request

    def track_request(self, request_id: str) -> FOIARequest:
        request = self._engine._foia_requests.get(request_id)
        if request is None:
            raise KeyError(f"FOIA request not found: {request_id}")
        return request


class NotificationHub:
    """Multi-channel notification delivery."""

    def __init__(self, engine: "CitizenServicesEngine") -> None:
        self._engine = engine
        self._preferences: Dict[str, NotificationPreference] = {}

    def set_preferences(
        self,
        citizen_id: str,
        preferences: Dict[str, List[NotificationChannel]],
        quiet_hours: Optional[Dict[str, str]] = None,
        language: str = "en",
    ) -> NotificationPreference:
        pref = NotificationPreference(
            citizen_id=citizen_id,
            preferences=preferences,
            quiet_hours=quiet_hours,
            language=language,
        )
        self._preferences[citizen_id] = pref
        return pref

    def send_bulk(
        self,
        template: str,
        recipient_filter: Dict[str, Any],
        data: Dict[str, str],
        channels: Optional[List[NotificationChannel]] = None,
    ) -> BulkNotification:
        import random
        random.seed(hash(template) % 2**31)
        recipient_count = random.randint(500, 10000)

        return BulkNotification(
            notification_id=f"notif-{uuid.uuid4().hex[:8]}",
            template=template,
            recipient_count=recipient_count,
            channels_used=channels or [NotificationChannel.EMAIL],
        )


class EquityAnalyzer:
    """Service delivery equity analysis."""

    def __init__(self, engine: "CitizenServicesEngine") -> None:
        self._engine = engine

    def analyze_service_equity(
        self,
        service_type: str,
        metric: ServiceMetric,
        dimensions: List[str],
        time_period_days: int = 90,
    ) -> EquityReport:
        import random
        random.seed(hash(service_type) % 2**31)

        breakdown: List[DimensionBreakdown] = []
        for dim in dimensions:
            groups = self._get_dimension_groups(dim)
            for group in groups:
                avg = random.uniform(2.0, 48.0)
                disparity = random.uniform(0.6, 2.5)
                breakdown.append(DimensionBreakdown(
                    dimension=dim,
                    group_name=group,
                    avg_value=round(avg, 1),
                    disparity_ratio=round(disparity, 2),
                    sample_size=random.randint(50, 500),
                ))

        overall = sum(b.avg_value for b in breakdown) / max(len(breakdown), 1)

        return EquityReport(
            service_type=service_type,
            metric=metric,
            overall_avg=round(overall, 1),
            dimension_breakdown=breakdown,
            time_period_days=time_period_days,
        )

    def generate_recommendations(
        self,
        service_type: str,
        target_disparity_ratio: float = 1.2,
    ) -> List[EquityRecommendation]:
        return [
            EquityRecommendation(
                description=f"Increase staffing for {service_type} in high-disparity areas",
                expected_impact=f"Reduce disparity ratio to {target_disparity_ratio:.1f}x",
                priority=Priority.HIGH,
            ),
            EquityRecommendation(
                description=f"Deploy mobile {service_type} units to underserved neighborhoods",
                expected_impact="Improve access within 30 days",
                priority=Priority.MEDIUM,
            ),
            EquityRecommendation(
                description="Implement proactive outreach to under-reporting communities",
                expected_impact="Increase request volume from underserved areas by 20%",
                priority=Priority.MEDIUM,
            ),
        ]

    def _get_dimension_groups(self, dimension: str) -> List[str]:
        groups_map = {
            "income_quartile": ["Q1_lowest", "Q2", "Q3", "Q4_highest"],
            "neighborhood": ["north", "south", "east", "west", "central"],
            "race_ethnicity": ["white", "black", "hispanic", "asian", "other"],
        }
        return groups_map.get(dimension, ["group_a", "group_b"])


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

class CitizenServicesEngine:
    """Main engine for citizen services operations."""

    def __init__(
        self,
        city_id: str,
        service_config: Optional[ServiceConfig] = None,
        channel_config: Optional[ChannelConfig] = None,
    ) -> None:
        self.city_id = city_id
        self._service_config = service_config or ServiceConfig()
        self._channel_config = channel_config or ChannelConfig()
        self._status = EngineStatus.UNINITIALIZED
        self._requests: Dict[str, ServiceRequest] = {}
        self._permits: Dict[str, PermitApplication] = {}
        self._surveys: Dict[str, Survey] = {}
        self._foia_requests: Dict[str, FOIARequest] = {}
        self._active_channels: int = 0
        self._created_at = datetime.utcnow()
        self._last_run: Optional[datetime] = None

    def configure(self) -> CitizenServicesEngine:
        """Validate configuration and initialize service channels."""
        self._status = EngineStatus.CONFIGURING

        channels = [
            self._channel_config.web_portal,
            self._channel_config.mobile_app,
            self._channel_config.phone_311,
            self._channel_config.sms,
            self._channel_config.email,
            self._channel_config.chatbot,
        ]
        self._active_channels = sum(1 for c in channels if c) + self._channel_config.walk_in_kiosks

        logger.info(
            "Citizen services engine configured for %s: %d channels, %d languages",
            self.city_id, self._active_channels, self._service_config.supported_languages,
        )
        self._status = EngineStatus.READY
        return self

    def run(self) -> Dict[str, Any]:
        """Execute a full citizen services cycle."""
        if self._status != EngineStatus.READY:
            raise RuntimeError(f"Engine not ready: {self._status.name}")

        self._status = EngineStatus.RUNNING
        self._last_run = datetime.utcnow()

        result = {
            "city_id": self.city_id,
            "status": self._status.value,
            "timestamp": self._last_run.isoformat(),
            "open_requests": len(self._requests),
            "pending_permits": len(self._permits),
            "active_surveys": len(self._surveys),
            "active_channels": self._active_channels,
        }

        self._status = EngineStatus.READY
        return result

    def validate(self) -> bool:
        """Validate engine configuration."""
        if self._status == EngineStatus.UNINITIALIZED:
            return False
        if not self.city_id:
            return False
        return True

    def get_status(self) -> Dict[str, Any]:
        """Get current engine status and metrics."""
        return {
            "engine": "CitizenServices",
            "city_id": self.city_id,
            "status": self._status.name,
            "request_types": self._service_config.request_types,
            "departments": self._service_config.departments,
            "active_channels": self._active_channels,
            "languages": self._service_config.supported_languages,
            "open_requests": len(self._requests),
            "pending_permits": len(self._permits),
            "uptime_seconds": (datetime.utcnow() - self._created_at).total_seconds(),
            "last_run": self._last_run.isoformat() if self._last_run else None,
        }

    def shutdown(self) -> None:
        """Gracefully shut down the engine."""
        self._status = EngineStatus.SHUTDOWN
        logger.info("Citizen services engine shut down for %s", self.city_id)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate citizen services engine capabilities."""
    print("=" * 70)
    print("  Citizen Services — Digital Government Platform Demo")
    print("=" * 70)

    engine = CitizenServicesEngine(
        city_id="metro-seattle-001",
        service_config=ServiceConfig(
            request_types=320, departments=45, avg_daily_requests=2_500,
            sla_targets={"pothole": 72, "streetlight_outage": 48, "graffiti": 24},
            supported_languages=52, accessibility_level="wcag_2.1_aa",
        ),
        channel_config=ChannelConfig(
            web_portal=True, mobile_app=True, phone_311=True,
            sms=True, email=True, walk_in_kiosks=12, chatbot=True,
        ),
    )

    engine.configure()
    status = engine.get_status()
    print(f"\n[1] Engine Status: {status['status']}")
    print(f"    Service types: {status['request_types']}")
    print(f"    Active channels: {status['active_channels']}")
    print(f"    Languages: {status['languages']}")

    srm = ServiceRequestManager(engine)
    request = srm.create_request(
        request_type=RequestType.POTHOLE,
        description="Large pothole on 5th Ave near Main St intersection",
        location={"lat": 47.6062, "lon": -122.3321, "address": "500 5th Ave"},
        photos=["pothole_photo.jpg"],
        reporter_contact={"phone": "206-555-0100"},
        priority=Priority.HIGH,
    )
    print(f"\n[2] Service Request Created: {request.request_id}")
    print(f"    Type: {request.request_type.value}, Department: {request.department}")
    print(f"    SLA deadline: {request.sla_deadline}")

    svc_status = srm.get_status(request.request_id)
    print(f"    Current status: {svc_status.current_status.value}")

    permits = PermitManager(engine)
    application = permits.submit_application(
        permit_type=PermitType.BUILDING_RESIDENTIAL,
        project_description="Kitchen and bathroom renovation, 1,200 sq ft",
        property_address="456 Oak Street",
        parcel_id="APN-4567-890",
        applicant={"name": "Jane Smith", "email": "jane@example.com"},
        contractor={"name": "ABC Construction", "license_number": "LIC-12345"},
        estimated_value=85_000,
    )
    print(f"\n[3] Permit Application: {application.application_id}")
    print(f"    Type: {application.permit_type.value}")
    print(f"    Fees: ${application.total_fees:.2f}")
    print(f"    Review timeline: {application.estimated_review_days} days")

    review = permits.get_review_status(application.application_id)
    print(f"    Current stage: {review.current_stage}")

    platform = EngagementPlatform(engine)
    survey = platform.create_survey(
        title="Downtown Parks Improvement Survey",
        description="Help us prioritize improvements for downtown parks",
        engagement_type=EngagementType.SURVEY,
        questions=[
            {"type": "multiple_choice", "question": "Which park needs improvement?"},
            {"type": "rating", "question": "Rate park cleanliness (1-5)"},
            {"type": "text", "question": "What improvements would you like to see?"},
        ],
        target_audience="district_downtown",
        duration_days=30,
        languages=["en", "es", "zh", "vi"],
    )
    print(f"\n[4] Survey Created: {survey.survey_id}")
    print(f"    Title: {survey.title}")
    print(f"    Questions: {len(survey.questions)}")
    print(f"    Languages: {survey.languages}")

    results = platform.get_survey_results(survey.survey_id)
    print(f"    Responses: {results.total_responses}")
    print(f"    Response rate: {results.response_rate:.1%}")

    records = PublicRecordsManager(engine)
    foia = records.submit_request(
        requester={"name": "John Doe", "email": "john@example.com"},
        description="All email correspondence regarding the waterfront development project",
        department="mayors_office",
    )
    print(f"\n[5] FOIA Request: {foia.request_id}")
    print(f"    Department: {foia.department}")
    print(f"    Estimated completion: {foia.estimated_completion_date}")

    hub = NotificationHub(engine)
    hub.set_preferences(
        citizen_id="citizen-78901",
        preferences={
            "service_updates": [NotificationChannel.EMAIL, NotificationChannel.SMS],
            "emergency_alerts": [NotificationChannel.PUSH, NotificationChannel.PHONE],
        },
        quiet_hours={"start": "22:00", "end": "07:00"},
        language="es",
    )
    notification = hub.send_bulk(
        template="service_update",
        recipient_filter={"district": "north"},
        data={"park_name": "Riverside Park", "update": "Construction starts Monday"},
        channels=[NotificationChannel.EMAIL, NotificationChannel.PUSH],
    )
    print(f"\n[6] Bulk Notification: {notification.notification_id}")
    print(f"    Recipients: {notification.recipient_count:,}")
    print(f"    Channels: {[c.value for c in notification.channels_used]}")

    equity = EquityAnalyzer(engine)
    report = equity.analyze_service_equity(
        service_type="pothole_repair",
        metric=ServiceMetric.RESPONSE_TIME,
        dimensions=["income_quartile", "neighborhood"],
    )
    print(f"\n[7] Equity Report: {report.service_type}")
    print(f"    Overall avg: {report.overall_avg:.1f} hours")
    for dim in report.dimension_breakdown[:4]:
        print(f"    {dim.dimension}/{dim.group_name}: avg={dim.avg_value:.1f}, "
              f"disparity={dim.disparity_ratio:.2f}x")

    recommendations = equity.generate_recommendations("pothole_repair")
    print(f"\n    Recommendations:")
    for rec in recommendations:
        print(f"      - {rec.description} (priority: {rec.priority.value})")

    result = engine.run()
    print(f"\n[8] Pipeline Run: {result['open_requests']} requests, "
          f"{result['pending_permits']} permits")

    engine.shutdown()
    print(f"\n[9] Engine Shutdown: {engine.get_status()['status']}")


if __name__ == "__main__":
    main()
