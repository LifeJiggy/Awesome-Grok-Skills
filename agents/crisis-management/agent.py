"""Crisis Management Agent - Crisis Response Planning, Communication, Stakeholder Management, Recovery.

A comprehensive crisis management system that handles crisis response planning,
communication strategy development, stakeholder management, recovery protocol design,
and post-crisis analysis. Built for communications teams, risk managers, and executives
who need a structured, auditable approach to crisis management.

Architecture: Event-driven crisis lifecycle with detection → assessment → response →
recovery → analysis stages. Each stage produces validated artifacts that feed downstream
operations. All actions are logged for audit and compliance purposes.

Author: Awesome Grok Skills Team
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
    cast,
)

# ---------------------------------------------------------------------------
# Module-level setup
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

__all__ = [
    "CrisisManagementAgent",
    "Config",
    "CrisisPlan",
    "CrisisEvent",
    "CommunicationPlan",
    "StakeholderRegistry",
    "RecoveryPlan",
    "PostMortem",
    "CrisisSeverity",
    "CrisisType",
    "CrisisPhase",
    "CommunicationChannel",
    "StakeholderPriority",
    "MessageType",
    "RecoveryPhase",
    "IncidentStatus",
    "EscalationLevel",
    "ComplianceRequirement",
]

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class CrisisType(Enum):
    """Types of crises the agent can manage."""
    OPERATIONAL = "operational"
    SECURITY = "security"
    REPUTATIONAL = "reputational"
    FINANCIAL = "financial"
    REGULATORY = "regulatory"
    NATURAL = "natural"
    PANDEMIC = "pandemic"
    TECHNICAL = "technical"
    HUMAN = "human"
    SUPPLY_CHAIN = "supply_chain"
    LEGAL = "legal"
    MARKET = "market"
    CYBER = "cyber"
    DATA_BREACH = "data_breach"
    PR_SCANDAL = "pr_scandal"
    PRODUCT_RECALL = "product_recall"
    INSIDER_THREAT = "insider_threat"
    PARTNER_FAILURE = "partner_failure"
    INFRASTRUCTURE = "infrastructure"
    REGULATORY_ACTION = "regulatory_action"


class CrisisSeverity(Enum):
    """Severity levels for crises."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class CrisisPhase(Enum):
    """Phases of the crisis lifecycle."""
    DETECTION = "detection"
    ASSESSMENT = "assessment"
    ACTIVATION = "activation"
    CONTAINMENT = "containment"
    COMMUNICATION = "communication"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    POST_MORTEM = "post_mortem"
    IMPROVEMENT = "improvement"
    MONITORING = "monitoring"
    STAND_DOWN = "stand_down"


class CommunicationChannel(Enum):
    """Channels for crisis communication."""
    EMAIL = "email"
    SLACK = "slack"
    SMS = "sms"
    PHONE = "phone"
    VIDEO_CALL = "video_call"
    PRESS_RELEASE = "press_release"
    SOCIAL_MEDIA = "social_media"
    INTERNAL_WIKI = "internal_wiki"
    ALL_HANDS = "all_hands"
    BOARD_CALL = "board_call"
    CUSTOMER_PORTAL = "customer_portal"
    WEBSITE_BANNER = "website_banner"
    MEDIA_BRIEFING = "media_briefing"
    INVESTOR_RELATIONS = "investor_relations"
    REGULATORY_FILING = "regulatory_filing"
    EMPLOYEE_TOWN_HALL = "employee_town_hall"
    PARTNER_NOTIFICATION = "partner_notification"
    VENDOR_ALERT = "vendor_alert"


class StakeholderPriority(Enum):
    """Priority levels for stakeholder communication."""
    P1_IMMEDIATE = 1      # Board, CEO, Legal — immediate notification
    P2_URGENT = 2         # C-Suite, Legal, PR — within 1 hour
    P3_HIGH = 3           # VP-level, Department Heads — within 4 hours
    P4_MEDIUM = 4         # Managers, Team Leads — within 8 hours
    P5_STANDARD = 5       # Individual Contributors — within 24 hours
    P6_EXTERNAL = 6       # Customers, Partners, Media — as needed


class MessageType(Enum):
    """Types of crisis communications."""
    INITIAL_ALERT = "initial_alert"
    SITUATION_UPDATE = "situation_update"
    ACTION_REQUIRED = "action_required"
    RESOLUTION_NOTICE = "resolution_notice"
    PREVENTIVE_MEASURES = "preventive_measures"
    STAKEHOLDER_UPDATE = "stakeholder_update"
    MEDIA_STATEMENT = "media_statement"
    CUSTOMER_ADVISORY = "customer_advisory"
    REGULATORY_NOTICE = "regulatory_notice"
    EMPLOYEE_COMMUNICATION = "employee_communication"
    INVESTOR_UPDATE = "investor_update"
    POST_MORTEM_SUMMARY = "post_mortem_summary"
    LESSONS_LEARNED = "lessons_learned"
    APPRECIATION = "appreciation"


class RecoveryPhase(Enum):
    """Phases of the recovery process."""
    IMMEDIATE = "immediate"          # 0-24 hours
    SHORT_TERM = "short_term"        # 1-7 days
    MEDIUM_TERM = "medium_term"      # 1-4 weeks
    LONG_TERM = "long_term"          # 1-3 months
    SUSTAINED = "sustained"          # 3+ months


class IncidentStatus(Enum):
    """Status of an incident/crisis."""
    DETECTED = "detected"
    ACKNOWLEDGED = "acknowledged"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    ERADICATING = "eradicating"
    RECOVERING = "recovering"
    RESOLVED = "resolved"
    POST_MORTEM = "post_mortem"
    CLOSED = "closed"
    REOPENED = "reopened"


class EscalationLevel(Enum):
    """Escalation levels for crisis response."""
    L1_OPS = "l1_ops"
    L2_MANAGEMENT = "l2_management"
    L3_SENIOR_LEADERSHIP = "l3_senior_leadership"
    L4_C_SUITE = "l4_c_suite"
    L5_BOARD = "l5_board"
    L6_EXTERNAL = "l6_external"


class ComplianceRequirement(Enum):
    """Compliance requirements for crisis response."""
    GDPR_72HR = "gdpr_72hr"
    HIPAA_NOTIFICATION = "hipaa_notification"
    SEC_FILING = "sec_filing"
    PCI_REPORT = "pci_report"
    SOC2_INCIDENT = "soc2_incident"
    ISO27001_INCIDENT = "iso27001_incident"
    STATE_BREACH = "state_breach"
    CUSTOMER_NOTIFICATION = "customer_notification"
    REGULATORY_REPORT = "regulatory_report"
    LAW_ENFORCEMENT = "law_enforcement"
    INSURANCE_NOTIFICATION = "insurance_notification"
    AUDIT_DOCUMENTATION = "audit_documentation"


class CommunicationTone(Enum):
    """Tone options for crisis communications."""
    EMPATHETIC = "empathetic"
    PROFESSIONAL = "professional"
    AUTHORITATIVE = "authoritative"
    TRANSPARENT = "transparent"
    REASSURING = "reassuring"
    FORMAL = "formal"
    CONCISE = "concise"
    DETAILED = "detailed"
    APOLOGETIC = "apologetic"
    FACTUAL = "factual"


class AudienceType(Enum):
    """Types of audiences for crisis communication."""
    INTERNAL_EXECUTIVE = "internal_executive"
    INTERNAL_LEGAL = "internal_legal"
    INTERNAL_ENGINEERING = "internal_engineering"
    INTERNAL_ALL_EMPLOYEES = "internal_all_employees"
    EXTERNAL_CUSTOMERS = "external_customers"
    EXTERNAL_PARTNERS = "external_partners"
    EXTERNAL_MEDIA = "external_media"
    EXTERNAL_REGULATORS = "external_regulators"
    EXTERNAL_INVESTORS = "external_investors"
    EXTERNAL_PUBLIC = "external_public"


class RiskLevel(Enum):
    """Risk assessment levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class CrisisTrigger(Enum):
    """Triggers that can activate a crisis response."""
    MONITORING_ALERT = "monitoring_alert"
    USER_REPORT = "user_report"
    EMPLOYEE_REPORT = "employee_report"
    MEDIA_INQUIRY = "media_inquiry"
    REGULATORY_INQUIRY = "regulatory_inquiry"
    CUSTOMER_COMPLAINT = "customer_complaint"
    SECURITY_SCAN = "security_scan"
    AUDIT_FINDING = "audit_finding"
    THREAT_INTELLIGENCE = "threat_intelligence"
    PARTNER_NOTIFICATION = "partner_notification"
    AUTOMATED_DETECTION = "automated_detection"
    MANUAL_ESCALATION = "manual_escalation"


class LessonCategory(Enum):
    """Categories for post-crisis lessons."""
    PROCESS = "process"
    COMMUNICATION = "communication"
    TECHNICAL = "technical"
    ORGANIZATIONAL = "organizational"
    TRAINING = "training"
    TOOLING = "tooling"
    VENDOR = "vendor"
    COMPLIANCE = "compliance"
    CULTURE = "culture"
    RESILIENCE = "resilience"


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class CommunicationConfig:
    """Configuration for crisis communications."""
    default_channels: List[CommunicationChannel] = field(
        default_factory=lambda: [
            CommunicationChannel.EMAIL,
            CommunicationChannel.SLACK,
            CommunicationChannel.PHONE,
        ]
    )
    escalation_channels: List[CommunicationChannel] = field(
        default_factory=lambda: [
            CommunicationChannel.PHONE,
            CommunicationChannel.VIDEO_CALL,
            CommunicationChannel.SMS,
        ]
    )
    external_channels: List[CommunicationChannel] = field(
        default_factory=lambda: [
            CommunicationChannel.PRESS_RELEASE,
            CommunicationChannel.WEBSITE_BANNER,
            CommunicationChannel.CUSTOMER_PORTAL,
        ]
    )
    update_frequency_hours: Dict[CrisisSeverity, int] = field(
        default_factory=lambda: {
            CrisisSeverity.CRITICAL: 1,
            CrisisSeverity.HIGH: 2,
            CrisisSeverity.MEDIUM: 4,
            CrisisSeverity.LOW: 8,
        }
    )
    auto_escalation_enabled: bool = True
    escalation_timeout_minutes: int = 30
    max_updates_per_hour: int = 4
    template_enabled: bool = True
    approval_required_for_external: bool = True


@dataclass
class RecoveryConfig:
    """Configuration for recovery planning."""
    rto_target_hours: int = 4
    rpo_target_hours: int = 1
    mttr_target_hours: int = 24
    service_availability_target: float = 0.999
    customer_impact_threshold: float = 0.05
    automated_recovery_enabled: bool = False
    backup_verification_required: bool = True
    post_recovery_testing_required: bool = True
    stakeholder_notification_on_recovery: bool = True


@dataclass
class AuditConfig:
    """Configuration for audit and compliance."""
    audit_trail_enabled: bool = True
    retention_days: int = 2555  # 7 years
    immutable_logging: bool = True
    compliance_frameworks: List[ComplianceRequirement] = field(
        default_factory=lambda: [
            ComplianceRequirement.GDPR_72HR,
            ComplianceRequirement.SOC2_INCIDENT,
        ]
    )
    auto_documentation: bool = True
    export_formats: List[str] = field(
        default_factory=lambda: ["json", "markdown", "pdf"]
    )


@dataclass
class Config:
    """Main configuration for the Crisis Management Agent."""
    agent_name: str = "CrisisManagementAgent"
    version: str = "3.0.0"
    log_level: str = "INFO"
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    timezone: str = "UTC"
    response_time_target_minutes: int = 15
    post_mortem_required: bool = True
    notification_threshold: CrisisSeverity = CrisisSeverity.HIGH
    communication: CommunicationConfig = field(default_factory=CommunicationConfig)
    recovery: RecoveryConfig = field(default_factory=RecoveryConfig)
    audit: AuditConfig = field(default_factory=AuditConfig)
    escalation_timeout_minutes: int = 30
    auto_escalation_enabled: bool = True
    crisis_team_roles: List[str] = field(
        default_factory=lambda: [
            "Incident Commander",
            "Communications Lead",
            "Technical Lead",
            "Legal Advisor",
            "HR Representative",
            "Executive Sponsor",
        ]
    )
    notification_channels: List[str] = field(default_factory=lambda: ["email", "slack"])
    webhook_urls: Dict[str, str] = field(default_factory=dict)
    api_keys: Dict[str, str] = field(default_factory=dict)
    export_directory: str = "./exports"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------


@dataclass
class Stakeholder:
    """Represents a stakeholder in crisis communication."""
    stakeholder_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    role: str = ""
    department: str = ""
    priority: StakeholderPriority = StakeholderPriority.P5_STANDARD
    communication_preference: CommunicationChannel = CommunicationChannel.EMAIL
    contact_info: Dict[str, str] = field(default_factory=dict)
    notification_history: List[Dict[str, Any]] = field(default_factory=list)
    acknowledged: bool = False
    acknowledged_at: Optional[datetime] = None
    requires_acknowledgment: bool = False
    escalation_path: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stakeholder_id": self.stakeholder_id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "priority": self.priority.value,
            "communication_preference": self.communication_preference.value,
            "acknowledged": self.acknowledged,
            "requires_acknowledgment": self.requires_acknowledgment,
        }


@dataclass
class CrisisStep:
    """A single step in a crisis response plan."""
    step_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    responsible_role: str = ""
    responsible_person: str = ""
    deadline_minutes: int = 0
    status: str = "pending"
    completed_at: Optional[datetime] = None
    notes: str = ""
    dependencies: List[str] = field(default_factory=list)
    checklist: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def complete(self) -> None:
        self.status = "completed"
        self.completed_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "name": self.name,
            "description": self.description,
            "responsible_role": self.responsible_role,
            "responsible_person": self.responsible_person,
            "deadline_minutes": self.deadline_minutes,
            "status": self.status,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class CrisisPlan:
    """A crisis response plan for a specific scenario."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = ""
    scenario: str = ""
    crisis_type: CrisisType = CrisisType.OPERATIONAL
    severity: CrisisSeverity = CrisisSeverity.MEDIUM
    steps: List[CrisisStep] = field(default_factory=list)
    contacts: List[Stakeholder] = field(default_factory=list)
    communication_templates: Dict[str, str] = field(default_factory=dict)
    escalation_matrix: Dict[str, List[str]] = field(default_factory=dict)
    compliance_requirements: List[ComplianceRequirement] = field(default_factory=list)
    recovery_targets: Dict[str, Any] = field(default_factory=dict)
    resources_required: List[str] = field(default_factory=list)
    estimated_duration_hours: int = 24
    last_tested: Optional[datetime] = None
    version: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    approved_by: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_step(self, step: CrisisStep) -> None:
        self.steps.append(step)
        self.updated_at = datetime.utcnow()

    def add_contact(self, stakeholder: Stakeholder) -> None:
        if not any(s.stakeholder_id == stakeholder.stakeholder_id for s in self.contacts):
            self.contacts.append(stakeholder)
            self.updated_at = datetime.utcnow()

    def get_steps_by_status(self, status: str) -> List[CrisisStep]:
        return [s for s in self.steps if s.status == status]

    def get_completion_percentage(self) -> float:
        if not self.steps:
            return 0.0
        completed = sum(1 for s in self.steps if s.status == "completed")
        return (completed / len(self.steps)) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "scenario": self.scenario,
            "crisis_type": self.crisis_type.value,
            "severity": self.severity.value,
            "steps": [s.to_dict() for s in self.steps],
            "contacts": [c.to_dict() for c in self.contacts],
            "compliance_requirements": [c.value for c in self.compliance_requirements],
            "completion_percentage": self.get_completion_percentage(),
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class CommunicationRecord:
    """Record of a crisis communication."""
    record_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    crisis_id: str = ""
    message_type: MessageType = MessageType.INITIAL_ALERT
    channel: CommunicationChannel = CommunicationChannel.EMAIL
    audience: AudienceType = AudienceType.INTERNAL_ALL_EMPLOYEES
    tone: CommunicationTone = CommunicationTone.PROFESSIONAL
    subject: str = ""
    body: str = ""
    sender: str = ""
    recipients: List[str] = field(default_factory=list)
    sent_at: Optional[datetime] = None
    status: str = "draft"
    approved_by: str = ""
    approved_at: Optional[datetime] = None
    acknowledgment_required: bool = False
    acknowledgments: List[Dict[str, Any]] = field(default_factory=list)
    feedback: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def approve(self, approver: str) -> None:
        self.approved_by = approver
        self.approved_at = datetime.utcnow()
        self.status = "approved"

    def send(self) -> None:
        self.sent_at = datetime.utcnow()
        self.status = "sent"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "crisis_id": self.crisis_id,
            "message_type": self.message_type.value,
            "channel": self.channel.value,
            "audience": self.audience.value,
            "tone": self.tone.value,
            "subject": self.subject,
            "status": self.status,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "approved_by": self.approved_by,
        }


@dataclass
class CrisisEvent:
    """An active crisis event being managed."""
    crisis_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    title: str = ""
    description: str = ""
    crisis_type: CrisisType = CrisisType.OPERATIONAL
    severity: CrisisSeverity = CrisisSeverity.MEDIUM
    status: IncidentStatus = IncidentStatus.DETECTED
    phase: CrisisPhase = CrisisPhase.DETECTION
    plan_id: Optional[str] = None
    trigger: CrisisTrigger = CrisisTrigger.MONITORING_ALERT
    detected_at: datetime = field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None
    contained_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    incident_commander: str = ""
    affected_systems: List[str] = field(default_factory=list)
    affected_users_count: int = 0
    impact_description: str = ""
    root_cause: str = ""
    communications: List[CommunicationRecord] = field(default_factory=list)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    actions_taken: List[Dict[str, Any]] = field(default_factory=list)
    open_issues: List[Dict[str, Any]] = field(default_factory=list)
    linked_crises: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_timeline_entry(self, event: str, details: str = "", actor: str = "") -> None:
        self.timeline.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "details": details,
            "actor": actor,
        })

    def update_status(self, new_status: IncidentStatus) -> None:
        old_status = self.status
        self.status = new_status
        self.add_timeline_entry(
            event="status_change",
            details=f"Status changed from {old_status.value} to {new_status.value}",
        )

    def get_duration_hours(self) -> float:
        end = self.resolved_at or datetime.utcnow()
        return (end - self.detected_at).total_seconds() / 3600

    def to_dict(self) -> Dict[str, Any]:
        return {
            "crisis_id": self.crisis_id,
            "title": self.title,
            "description": self.description,
            "crisis_type": self.crisis_type.value,
            "severity": self.severity.value,
            "status": self.status.value,
            "phase": self.phase.value,
            "detected_at": self.detected_at.isoformat(),
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "duration_hours": round(self.get_duration_hours(), 2),
            "incident_commander": self.incident_commander,
            "affected_users_count": self.affected_users_count,
            "timeline": self.timeline,
            "communications_count": len(self.communications),
        }


@dataclass
class CommunicationPlan:
    """A structured communication plan for a crisis."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    crisis_id: str = ""
    strategy: str = ""
    key_messages: List[str] = field(default_factory=list)
    audience_matrix: Dict[AudienceType, Dict[str, Any]] = field(default_factory=dict)
    channel_strategy: Dict[CommunicationChannel, Dict[str, Any]] = field(default_factory=dict)
    approval_workflow: List[str] = field(default_factory=list)
    update_schedule: Dict[CrisisSeverity, str] = field(default_factory=dict)
    tone_guidelines: Dict[AudienceType, CommunicationTone] = field(default_factory=dict)
    prohibited_content: List[str] = field(default_factory=list)
    spokesperson: str = ""
    media_contacts: List[Dict[str, str]] = field(default_factory=list)
    social_media_guidelines: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "crisis_id": self.crisis_id,
            "strategy": self.strategy,
            "key_messages": self.key_messages,
            "spokesperson": self.spokesperson,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class StakeholderRegistry:
    """Registry of all stakeholders for crisis communication."""
    registry_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    stakeholders: List[Stakeholder] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_stakeholder(self, stakeholder: Stakeholder) -> None:
        if not any(s.stakeholder_id == stakeholder.stakeholder_id for s in self.stakeholders):
            self.stakeholders.append(stakeholder)
            self.updated_at = datetime.utcnow()

    def get_by_priority(self, priority: StakeholderPriority) -> List[Stakeholder]:
        return [s for s in self.stakeholders if s.priority == priority]

    def get_by_department(self, department: str) -> List[Stakeholder]:
        return [s for s in self.stakeholders if s.department.lower() == department.lower()]

    def get_unacknowledged(self) -> List[Stakeholder]:
        return [s for s in self.stakeholders if s.requires_acknowledgment and not s.acknowledged]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry_id": self.registry_id,
            "stakeholders": [s.to_dict() for s in self.stakeholders],
            "total": len(self.stakeholders),
        }


@dataclass
class RecoveryMilestone:
    """A milestone in the recovery process."""
    milestone_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    phase: RecoveryPhase = RecoveryPhase.IMMEDIATE
    target_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    status: str = "pending"
    responsible: str = ""
    dependencies: List[str] = field(default_factory=list)
    verification_steps: List[str] = field(default_factory=list)
    verified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def complete(self) -> None:
        self.status = "completed"
        self.completed_date = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "milestone_id": self.milestone_id,
            "name": self.name,
            "phase": self.phase.value,
            "status": self.status,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
        }


@dataclass
class RecoveryPlan:
    """A structured recovery plan with milestones and targets."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    crisis_id: str = ""
    name: str = ""
    rto_hours: int = 4
    rpo_hours: int = 1
    mttr_hours: int = 24
    milestones: List[RecoveryMilestone] = field(default_factory=list)
    resource_requirements: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    communication_checkpoints: List[Dict[str, Any]] = field(default_factory=list)
    verification_steps: List[str] = field(default_factory=list)
    rollback_plan: str = ""
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_milestone(self, milestone: RecoveryMilestone) -> None:
        self.milestones.append(milestone)
        self.updated_at = datetime.utcnow()

    def get_completion_percentage(self) -> float:
        if not self.milestones:
            return 0.0
        completed = sum(1 for m in self.milestones if m.status == "completed")
        return (completed / len(self.milestones)) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "crisis_id": self.crisis_id,
            "rto_hours": self.rto_hours,
            "rpo_hours": self.rpo_hours,
            "mttr_hours": self.mttr_hours,
            "milestones": [m.to_dict() for m in self.milestones],
            "completion_percentage": self.get_completion_percentage(),
            "status": self.status,
        }


@dataclass
class Lesson:
    """A lesson learned from a crisis."""
    lesson_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    category: LessonCategory = LessonCategory.PROCESS
    severity: CrisisSeverity = CrisisSeverity.MEDIUM
    recommendation: str = ""
    owner: str = ""
    status: str = "open"
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lesson_id": self.lesson_id,
            "title": self.title,
            "category": self.category.value,
            "severity": self.severity.value,
            "recommendation": self.recommendation,
            "status": self.status,
        }


@dataclass
class PostMortem:
    """Post-crisis analysis and lessons learned."""
    post_mortem_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    crisis_id: str = ""
    title: str = ""
    summary: str = ""
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    root_cause: str = ""
    impact_assessment: Dict[str, Any] = field(default_factory=dict)
    response_evaluation: Dict[str, Any] = field(default_factory=dict)
    lessons: List[Lesson] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    what_went_well: List[str] = field(default_factory=list)
    what_went_wrong: List[str] = field(default_factory=list)
    what_could_improve: List[str] = field(default_factory=list)
    follow_up_date: Optional[datetime] = None
    participants: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    approved_by: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_lesson(self, lesson: Lesson) -> None:
        self.lessons.append(lesson)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "post_mortem_id": self.post_mortem_id,
            "crisis_id": self.crisis_id,
            "title": self.title,
            "summary": self.summary,
            "root_cause": self.root_cause,
            "lessons": [l.to_dict() for l in self.lessons],
            "what_went_well": self.what_went_well,
            "what_went_wrong": self.what_went_wrong,
            "created_at": self.created_at.isoformat(),
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
        raise ValidationError(field_name, f"Value {value} is out of range [{min_val}, {max_val}].")


def _validate_list_not_empty(items: List[Any], field_name: str) -> None:
    if not items:
        raise ValidationError(field_name, "This list must contain at least one item.")


# ---------------------------------------------------------------------------
# Template Generator
# ---------------------------------------------------------------------------


class _TemplateGenerator:
    """Generates communication templates for crisis scenarios."""

    TEMPLATES: Dict[str, Dict[str, str]] = {
        "initial_alert": {
            "internal": "URGENT: {crisis_type} incident detected. Severity: {severity}. "
                        "Incident Commander: {commander}. Next update: {next_update}.",
            "external": "We are aware of an issue affecting our {affected_area}. "
                        "Our team is actively investigating and we will provide updates shortly.",
        },
        "situation_update": {
            "internal": "UPDATE [{severity}]: {crisis_type} incident update. "
                        "Current status: {status}. {details} Next update: {next_update}.",
            "external": "Update on the current situation: {details}. "
                        "We are working to resolve this and will share more information soon.",
        },
        "resolution": {
            "internal": "RESOLVED: The {crisis_type} incident has been resolved. "
                        "Root cause: {root_cause}. Duration: {duration}. "
                        "Post-mortem scheduled for {post_mortem_date}.",
            "external": "The issue has been resolved. {resolution_details}. "
                        "We apologize for any inconvenience and have implemented measures to prevent recurrence.",
        },
        "preventive": {
            "internal": "POST-CRISIS: Following the {crisis_type} incident, we have implemented: "
                        "{preventive_measures}. Please review and acknowledge.",
            "external": "We have taken steps to prevent similar issues in the future, including: "
                        "{preventive_measures}.",
        },
    }

    @classmethod
    def generate(cls, template_type: str, audience: str, **kwargs: Any) -> Dict[str, str]:
        templates = cls.TEMPLATES.get(template_type, {})
        template = templates.get(audience, templates.get("internal", ""))
        try:
            body = template.format(**kwargs)
        except KeyError:
            body = template
        return {
            "subject": f"Crisis Update: {kwargs.get('crisis_type', 'Incident')}",
            "body": body,
        }


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------


class CrisisManagementAgent:
    """Comprehensive crisis management agent.

    Orchestrates the full crisis lifecycle:
    - Crisis plan creation and management
    - Crisis event tracking and status management
    - Communication plan development and execution
    - Stakeholder management and notification
    - Recovery planning with milestones and targets
    - Post-crisis analysis and lessons learned
    - Compliance tracking and audit trail

    Example::

        agent = CrisisManagementAgent()

        # Create crisis plan
        plan = agent.create_crisis_plan(
            name="Data Breach Response",
            scenario="Customer data exposed",
            crisis_type=CrisisType.DATA_BREACH,
            severity=CrisisSeverity.CRITICAL,
        )

        # Activate crisis
        crisis = agent.activate_crisis(plan_id=plan.plan_id, title="Customer Data Breach")

        # Manage communications
        agent.send_communication(crisis_id=crisis.crisis_id, message_type=MessageType.INITIAL_ALERT)

        # Develop recovery
        recovery = agent.develop_recovery(crisis_id=crisis.crisis_id)
    """

    def __init__(self, config: Optional[Config] = None) -> None:
        self._config = config or Config()
        self._cache = _Cache(ttl_seconds=self._config.cache_ttl_seconds) if self._config.enable_caching else None
        self._plans: Dict[str, CrisisPlan] = {}
        self._crises: Dict[str, CrisisEvent] = {}
        self._communication_plans: Dict[str, CommunicationPlan] = {}
        self._stakeholder_registry = StakeholderRegistry()
        self._recovery_plans: Dict[str, RecoveryPlan] = {}
        self._post_mortems: Dict[str, PostMortem] = {}
        self._operation_log: List[Dict[str, Any]] = []
        self._error_count: int = 0
        self._success_count: int = 0
        logger.info(
            "CrisisManagementAgent initialized (version=%s, caching=%s)",
            self._config.version,
            self._config.enable_caching,
        )

    # ----- Crisis Plan Management -----

    def create_crisis_plan(
        self,
        name: str,
        scenario: str,
        crisis_type: CrisisType = CrisisType.OPERATIONAL,
        severity: CrisisSeverity = CrisisSeverity.MEDIUM,
        contacts: Optional[List[Dict[str, Any]]] = None,
        compliance: Optional[List[ComplianceRequirement]] = None,
    ) -> CrisisPlan:
        """Create a crisis response plan.

        Args:
            name: Plan name.
            scenario: Description of the crisis scenario.
            crisis_type: Type of crisis.
            severity: Expected severity level.
            contacts: List of stakeholder dicts with name, role, priority.
            compliance: Compliance requirements to track.

        Returns:
            CrisisPlan: The created crisis plan.
        """
        _validate_required(name, "name")
        _validate_required(scenario, "scenario")

        plan = CrisisPlan(
            name=name,
            scenario=scenario,
            crisis_type=crisis_type,
            severity=severity,
            compliance_requirements=compliance or [],
        )

        # Generate default steps based on crisis type
        default_steps = self._generate_default_steps(crisis_type, severity)
        for step_data in default_steps:
            step = CrisisStep(**step_data)
            plan.add_step(step)

        # Add contacts
        if contacts:
            for contact_data in contacts:
                stakeholder = Stakeholder(
                    name=contact_data.get("name", ""),
                    role=contact_data.get("role", ""),
                    priority=StakeholderPriority(contact_data.get("priority", 5)),
                )
                plan.add_contact(stakeholder)
                self._stakeholder_registry.add_stakeholder(stakeholder)

        # Generate communication templates
        plan.communication_templates = self._generate_templates(crisis_type, severity)

        self._plans[plan.plan_id] = plan
        self._log_operation("create_crisis_plan", {"plan_id": plan.plan_id, "name": name})
        logger.info("Crisis plan created: %s (%s)", name, plan.plan_id)
        return plan

    def update_crisis_plan(self, plan_id: str, **kwargs: Any) -> CrisisPlan:
        """Update an existing crisis plan."""
        plan = self._get_plan(plan_id)
        for key, value in kwargs.items():
            if hasattr(plan, key) and value is not None:
                setattr(plan, key, value)
        plan.updated_at = datetime.utcnow()
        plan.version += 1
        return plan

    def get_crisis_plan(self, plan_id: str) -> CrisisPlan:
        """Retrieve a crisis plan by ID."""
        return self._get_plan(plan_id)

    def list_plans(self) -> List[CrisisPlan]:
        """List all crisis plans."""
        return list(self._plans.values())

    def test_crisis_plan(self, plan_id: str) -> Dict[str, Any]:
        """Simulate testing a crisis plan.

        Identifies gaps and generates a test report.
        """
        plan = self._get_plan(plan_id)
        gaps: List[str] = []
        recommendations: List[str] = []
        if not plan.contacts:
            gaps.append("No contacts defined in the plan.")
            recommendations.append("Add stakeholder contacts with roles and priorities.")
        if not plan.communication_templates:
            gaps.append("No communication templates defined.")
            recommendations.append("Generate communication templates for each audience.")
        if not plan.compliance_requirements:
            gaps.append("No compliance requirements tracked.")
            recommendations.append("Identify applicable compliance requirements (GDPR, SOC2, etc.).")
        incomplete_steps = plan.get_steps_by_status("pending")
        if incomplete_steps:
            gaps.append(f"{len(incomplete_steps)} steps are still pending.")
        plan.last_tested = datetime.utcnow()
        self._log_operation("test_crisis_plan", {"plan_id": plan_id, "gaps": len(gaps)})
        return {
            "plan_id": plan_id,
            "plan_name": plan.name,
            "gaps": gaps,
            "recommendations": recommendations,
            "completion": plan.get_completion_percentage(),
            "tested_at": datetime.utcnow().isoformat(),
        }

    # ----- Crisis Event Management -----

    def activate_crisis(
        self,
        plan_id: str,
        title: str,
        description: str = "",
        severity: CrisisSeverity = CrisisSeverity.HIGH,
        trigger: CrisisTrigger = CrisisTrigger.MONITORING_ALERT,
        incident_commander: str = "",
    ) -> CrisisEvent:
        """Activate a crisis response using an existing plan.

        Creates a new crisis event, links it to the plan, and begins
        the crisis lifecycle.

        Args:
            plan_id: ID of the crisis plan to activate.
            title: Crisis title.
            description: Crisis description.
            severity: Actual severity level.
            trigger: What triggered the crisis.
            incident_commander: Assigned incident commander.

        Returns:
            CrisisEvent: The activated crisis event.
        """
        _validate_required(title, "title")
        plan = self._get_plan(plan_id)

        crisis = CrisisEvent(
            title=title,
            description=description,
            crisis_type=plan.crisis_type,
            severity=severity,
            status=IncidentStatus.DETECTED,
            phase=CrisisPhase.DETECTION,
            plan_id=plan_id,
            trigger=trigger,
            incident_commander=incident_commander or "TBD",
        )
        crisis.add_timeline_entry(
            event="crisis_activated",
            details=f"Crisis activated from plan: {plan.name}",
            actor=incident_commander,
        )

        self._crises[crisis.crisis_id] = crisis
        self._log_operation("activate_crisis", {
            "crisis_id": crisis.crisis_id,
            "plan_id": plan_id,
            "severity": severity.value,
        })
        logger.warning("CRISIS ACTIVATED: %s (%s) - Severity: %s", title, crisis.crisis_id, severity.value)
        return crisis

    def update_crisis_status(
        self,
        crisis_id: str,
        new_status: IncidentStatus,
        notes: str = "",
    ) -> CrisisEvent:
        """Update the status of an active crisis."""
        crisis = self._get_crisis(crisis_id)
        crisis.update_status(new_status)
        if notes:
            crisis.add_timeline_entry(event="note", details=notes)
        if new_status == IncidentStatus.ACKNOWLEDGED:
            crisis.acknowledged_at = datetime.utcnow()
        elif new_status == IncidentStatus.CONTAINED:
            crisis.contained_at = datetime.utcnow()
        elif new_status == IncidentStatus.RESOLVED:
            crisis.resolved_at = datetime.utcnow()
        self._log_operation("update_crisis_status", {
            "crisis_id": crisis_id,
            "new_status": new_status.value,
        })
        return crisis

    def escalate_crisis(
        self,
        crisis_id: str,
        to_level: EscalationLevel,
        reason: str = "",
    ) -> CrisisEvent:
        """Escalate a crisis to a higher level."""
        crisis = self._get_crisis(crisis_id)
        crisis.add_timeline_entry(
            event="escalation",
            details=f"Escalated to {to_level.value}: {reason}",
        )
        crisis.metadata["escalation_level"] = to_level.value
        self._log_operation("escalate_crisis", {
            "crisis_id": crisis_id,
            "to_level": to_level.value,
        })
        return crisis

    def get_crisis(self, crisis_id: str) -> CrisisEvent:
        """Retrieve a crisis event by ID."""
        return self._get_crisis(crisis_id)

    def list_crises(self, status: Optional[IncidentStatus] = None) -> List[CrisisEvent]:
        """List all crisis events with optional status filter."""
        crises = list(self._crises.values())
        if status:
            crises = [c for c in crises if c.status == status]
        return crises

    def get_active_crises(self) -> List[CrisisEvent]:
        """Get all currently active (unresolved) crises."""
        return [
            c for c in self._crises.values()
            if c.status not in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]
        ]

    def get_crisis_dashboard(self) -> Dict[str, Any]:
        """Get a dashboard view of all crises."""
        status_counts: Dict[str, int] = defaultdict(int)
        severity_counts: Dict[str, int] = defaultdict(int)
        for crisis in self._crises.values():
            status_counts[crisis.status.value] += 1
            severity_counts[crisis.severity.value] += 1
        active = self.get_active_crises()
        return {
            "total_crises": len(self._crises),
            "active_crises": len(active),
            "by_status": dict(status_counts),
            "by_severity": dict(severity_counts),
            "plans": len(self._plans),
            "recovery_plans": len(self._recovery_plans),
            "post_mortems": len(self._post_mortems),
        }

    # ----- Communication Management -----

    def develop_communication_plan(
        self,
        crisis_id: str,
        strategy: str = "",
        key_messages: Optional[List[str]] = None,
        spokesperson: str = "",
    ) -> CommunicationPlan:
        """Develop a communication plan for a crisis.

        Args:
            crisis_id: ID of the crisis.
            strategy: Communication strategy description.
            key_messages: Key messages to communicate.
            spokesperson: Designated spokesperson.

        Returns:
            CommunicationPlan: The communication plan.
        """
        crisis = self._get_crisis(crisis_id)

        plan = CommunicationPlan(
            crisis_id=crisis_id,
            strategy=strategy or f"Transparent communication about {crisis.title}",
            key_messages=key_messages or [
                f"We are aware of the {crisis.crisis_type.value} incident",
                "Our team is actively working to resolve the issue",
                "We will provide regular updates as the situation develops",
                "We are committed to transparency and will share findings",
            ],
            spokesperson=spokesperson,
            update_schedule={
                CrisisSeverity.CRITICAL: "Every 1 hour",
                CrisisSeverity.HIGH: "Every 2 hours",
                CrisisSeverity.MEDIUM: "Every 4 hours",
                CrisisSeverity.LOW: "Every 8 hours",
            },
            tone_guidelines={
                AudienceType.INTERNAL_EXECUTIVE: CommunicationTone.FACTUAL,
                AudienceType.INTERNAL_ALL_EMPLOYEES: CommunicationTone.TRANSPARENT,
                AudienceType.EXTERNAL_CUSTOMERS: CommunicationTone.EMPATHETIC,
                AudienceType.EXTERNAL_MEDIA: CommunicationTone.PROFESSIONAL,
                AudienceType.EXTERNAL_REGULATORS: CommunicationTone.FORMAL,
            },
            prohibited_content=[
                "Speculation about root cause before confirmed",
                "Blaming individuals or third parties",
                "Promising specific resolution timelines before confirmed",
                "Sharing sensitive security details publicly",
            ],
        )

        # Build audience matrix
        for audience in AudienceType:
            plan.audience_matrix[audience] = {
                "channel": self._get_preferred_channel(audience),
                "frequency": plan.update_schedule.get(crisis.severity, "Every 4 hours"),
                "tone": plan.tone_guidelines.get(audience, CommunicationTone.PROFESSIONAL),
                "approval_required": audience in [
                    AudienceType.EXTERNAL_MEDIA,
                    AudienceType.EXTERNAL_REGULATORS,
                    AudienceType.EXTERNAL_INVESTORS,
                ],
            }

        self._communication_plans[plan.plan_id] = plan
        self._log_operation("develop_communication_plan", {
            "crisis_id": crisis_id,
            "plan_id": plan.plan_id,
        })
        return plan

    def send_communication(
        self,
        crisis_id: str,
        message_type: MessageType,
        channel: CommunicationChannel = CommunicationChannel.EMAIL,
        audience: AudienceType = AudienceType.INTERNAL_ALL_EMPLOYEES,
        subject: str = "",
        body: str = "",
        tone: CommunicationTone = CommunicationTone.PROFESSIONAL,
    ) -> CommunicationRecord:
        """Send a crisis communication.

        Creates a communication record and sends it through the specified channel.

        Args:
            crisis_id: ID of the crisis.
            message_type: Type of message.
            channel: Communication channel.
            audience: Target audience.
            subject: Message subject.
            body: Message body.
            tone: Communication tone.

        Returns:
            CommunicationRecord: The sent communication record.
        """
        crisis = self._get_crisis(crisis_id)

        record = CommunicationRecord(
            crisis_id=crisis_id,
            message_type=message_type,
            channel=channel,
            audience=audience,
            tone=tone,
            subject=subject or f"Crisis Update: {crisis.title}",
            body=body,
            status="sent",
            sent_at=datetime.utcnow(),
        )

        crisis.communications.append(record)
        crisis.add_timeline_entry(
            event="communication_sent",
            details=f"{message_type.value} sent via {channel.value} to {audience.value}",
        )

        self._log_operation("send_communication", {
            "crisis_id": crisis_id,
            "message_type": message_type.value,
            "channel": channel.value,
        })
        return record

    def draft_communication(
        self,
        crisis_id: str,
        message_type: MessageType,
        audience: AudienceType,
        **kwargs: Any,
    ) -> CommunicationRecord:
        """Draft a communication using templates.

        Generates a draft communication based on the crisis details
        and audience-specific templates.

        Args:
            crisis_id: ID of the crisis.
            message_type: Type of message.
            audience: Target audience.
            **kwargs: Additional template variables.

        Returns:
            CommunicationRecord: The drafted communication.
        """
        crisis = self._get_crisis(crisis_id)
        template_key = message_type.value
        audience_key = "internal" if "INTERNAL" in audience.value else "external"

        template_data = {
            "crisis_type": crisis.crisis_type.value,
            "severity": crisis.severity.value,
            "commander": crisis.incident_commander,
            "status": crisis.status.value,
            "next_update": "2 hours",
            "affected_area": "systems",
            "details": crisis.description or "Under investigation",
            "root_cause": crisis.root_cause or "Under investigation",
            "duration": f"{crisis.get_duration_hours():.1f} hours",
        }
        template_data.update(kwargs)

        generated = _TemplateGenerator.generate(template_key, audience_key, **template_data)

        record = CommunicationRecord(
            crisis_id=crisis_id,
            message_type=message_type,
            audience=audience,
            subject=generated["subject"],
            body=generated["body"],
            status="draft",
        )

        return record

    # ----- Stakeholder Management -----

    def add_stakeholder(
        self,
        name: str,
        role: str,
        department: str = "",
        priority: StakeholderPriority = StakeholderPriority.P5_STANDARD,
        communication_preference: CommunicationChannel = CommunicationChannel.EMAIL,
        contact_info: Optional[Dict[str, str]] = None,
    ) -> Stakeholder:
        """Add a stakeholder to the registry.

        Args:
            name: Stakeholder name.
            role: Stakeholder role.
            department: Department.
            priority: Communication priority level.
            communication_preference: Preferred communication channel.
            contact_info: Contact information.

        Returns:
            Stakeholder: The created stakeholder.
        """
        _validate_required(name, "name")
        _validate_required(role, "role")

        stakeholder = Stakeholder(
            name=name,
            role=role,
            department=department,
            priority=priority,
            communication_preference=communication_preference,
            contact_info=contact_info or {},
        )
        self._stakeholder_registry.add_stakeholder(stakeholder)
        self._log_operation("add_stakeholder", {"stakeholder_id": stakeholder.stakeholder_id, "name": name})
        return stakeholder

    def get_stakeholder(self, stakeholder_id: str) -> Optional[Stakeholder]:
        """Retrieve a stakeholder by ID."""
        for s in self._stakeholder_registry.stakeholders:
            if s.stakeholder_id == stakeholder_id:
                return s
        return None

    def list_stakeholders(self, priority: Optional[StakeholderPriority] = None) -> List[Stakeholder]:
        """List stakeholders with optional priority filter."""
        stakeholders = self._stakeholder_registry.stakeholders
        if priority:
            stakeholders = [s for s in stakeholders if s.priority == priority]
        return stakeholders

    def get_notification_list(
        self,
        severity: CrisisSeverity,
    ) -> List[Stakeholder]:
        """Get the list of stakeholders to notify based on severity."""
        priority_map = {
            CrisisSeverity.CRITICAL: [StakeholderPriority.P1_IMMEDIATE, StakeholderPriority.P2_URGENT, StakeholderPriority.P3_HIGH],
            CrisisSeverity.HIGH: [StakeholderPriority.P2_URGENT, StakeholderPriority.P3_HIGH, StakeholderPriority.P4_MEDIUM],
            CrisisSeverity.MEDIUM: [StakeholderPriority.P3_HIGH, StakeholderPriority.P4_MEDIUM, StakeholderPriority.P5_STANDARD],
            CrisisSeverity.LOW: [StakeholderPriority.P5_STANDARD, StakeholderPriority.P6_EXTERNAL],
        }
        target_priorities = priority_map.get(severity, [StakeholderPriority.P5_STANDARD])
        return [
            s for s in self._stakeholder_registry.stakeholders
            if s.priority in target_priorities
        ]

    # ----- Recovery Planning -----

    def develop_recovery(
        self,
        crisis_id: str,
        rto_hours: int = 4,
        rpo_hours: int = 1,
        mttr_hours: int = 24,
    ) -> RecoveryPlan:
        """Develop a recovery plan for a crisis.

        Creates a structured recovery plan with milestones for each phase
        of the recovery process.

        Args:
            crisis_id: ID of the crisis.
            rto_hours: Recovery Time Objective in hours.
            rpo_hours: Recovery Point Objective in hours.
            mttr_hours: Mean Time to Recovery target in hours.

        Returns:
            RecoveryPlan: The recovery plan with milestones.
        """
        crisis = self._get_crisis(crisis_id)

        recovery = RecoveryPlan(
            crisis_id=crisis_id,
            name=f"Recovery Plan: {crisis.title}",
            rto_hours=rto_hours,
            rpo_hours=rpo_hours,
            mttr_hours=mttr_hours,
        )

        # Generate milestones for each phase
        milestone_templates = [
            (RecoveryPhase.IMMEDIATE, "Immediate Containment", "Contain the damage and prevent further impact", 1),
            (RecoveryPhase.IMMEDIATE, "Root Cause Identification", "Identify the root cause of the crisis", 4),
            (RecoveryPhase.SHORT_TERM, "Critical Service Restoration", "Restore critical services and functionality", 24),
            (RecoveryPhase.SHORT_TERM, "Data Integrity Verification", "Verify data integrity and restore from backup if needed", 48),
            (RecoveryPhase.MEDIUM_TERM, "Full Service Restoration", "Restore all services to normal operation", 168),
            (RecoveryPhase.MEDIUM_TERM, "Stakeholder Communication Complete", "Complete all stakeholder notifications", 168),
            (RecoveryPhase.LONG_TERM, "Process Improvements Implemented", "Implement process improvements identified", 720),
            (RecoveryPhase.LONG_TERM, "Monitoring Enhanced", "Enhance monitoring and alerting", 720),
            (RecoveryPhase.SUSTAINED, "Post-Mortem Complete", "Complete post-mortem and lessons learned", 2160),
            (RecoveryPhase.SUSTAINED, "Prevention Measures Verified", "Verify all prevention measures are effective", 2160),
        ]

        now = datetime.utcnow()
        for phase, name, description, hours in milestone_templates:
            milestone = RecoveryMilestone(
                name=name,
                description=description,
                phase=phase,
                target_date=now + timedelta(hours=hours),
            )
            recovery.add_milestone(milestone)

        self._recovery_plans[recovery.plan_id] = recovery
        self._log_operation("develop_recovery", {
            "crisis_id": crisis_id,
            "recovery_id": recovery.plan_id,
            "milestones": len(recovery.milestones),
        })
        return recovery

    def get_recovery(self, plan_id: str) -> RecoveryPlan:
        """Retrieve a recovery plan by ID."""
        plan = self._recovery_plans.get(plan_id)
        if plan is None:
            raise ValidationError("plan_id", f"Recovery plan {plan_id} not found.")
        return plan

    def list_recovery_plans(self) -> List[RecoveryPlan]:
        """List all recovery plans."""
        return list(self._recovery_plans.values())

    # ----- Post-Mortem -----

    def generate_post_mortem(
        self,
        crisis_id: str,
        title: str = "",
        participants: Optional[List[str]] = None,
    ) -> PostMortem:
        """Generate a post-crisis analysis report.

        Creates a structured post-mortem document with timeline,
        root cause analysis, impact assessment, and lessons learned.

        Args:
            crisis_id: ID of the crisis.
            title: Post-mortem title.
            participants: List of participants.

        Returns:
            PostMortem: The post-mortem report.
        """
        crisis = self._get_crisis(crisis_id)

        post_mortem = PostMortem(
            crisis_id=crisis_id,
            title=title or f"Post-Mortem: {crisis.title}",
            summary=f"Analysis of {crisis.crisis_type.value} crisis: {crisis.title}",
            timeline=crisis.timeline,
            root_cause=crisis.root_cause or "To be determined during post-mortem analysis",
            participants=participants or [],
        )

        # Add default lessons based on crisis type
        default_lessons = self._generate_default_lessons(crisis.crisis_type)
        for lesson_data in default_lessons:
            lesson = Lesson(**lesson_data)
            post_mortem.add_lesson(lesson)

        # Generate what went well/wrong/what could improve
        post_mortem.what_went_well = [
            "Crisis was detected and escalated promptly",
            "Communication plan was executed effectively",
            "Recovery was completed within target RTO",
        ]
        post_mortem.what_went_wrong = [
            "Root cause was not immediately clear",
            "Some stakeholders were not notified promptly",
            "Monitoring gaps allowed the crisis to escalate",
        ]
        post_mortem.what_could_improve = [
            "Improve automated detection and alerting",
            "Enhance crisis communication templates",
            "Conduct regular crisis simulation exercises",
        ]

        self._post_mortems[post_mortem.post_mortem_id] = post_mortem
        crisis.phase = CrisisPhase.POST_MORTEM
        self._log_operation("generate_post_mortem", {
            "crisis_id": crisis_id,
            "post_mortem_id": post_mortem.post_mortem_id,
        })
        return post_mortem

    def get_post_mortem(self, post_mortem_id: str) -> PostMortem:
        """Retrieve a post-mortem by ID."""
        pm = self._post_mortems.get(post_mortem_id)
        if pm is None:
            raise ValidationError("post_mortem_id", f"Post-mortem {post_mortem_id} not found.")
        return pm

    def list_post_mortems(self) -> List[PostMortem]:
        """List all post-mortems."""
        return list(self._post_mortems.values())

    # ----- Internal Helpers -----

    def _get_plan(self, plan_id: str) -> CrisisPlan:
        plan = self._plans.get(plan_id)
        if plan is None:
            raise ValidationError("plan_id", f"Crisis plan {plan_id} not found.")
        return plan

    def _get_crisis(self, crisis_id: str) -> CrisisEvent:
        crisis = self._crises.get(crisis_id)
        if crisis is None:
            raise ValidationError("crisis_id", f"Crisis {crisis_id} not found.")
        return crisis

    def _log_operation(self, operation: str, details: Dict[str, Any]) -> None:
        self._operation_log.append({
            "operation": operation,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def _generate_default_steps(
        self,
        crisis_type: CrisisType,
        severity: CrisisSeverity,
    ) -> List[Dict[str, Any]]:
        steps = [
            {"name": "Acknowledge Incident", "description": "Acknowledge the crisis and assign incident commander", "responsible_role": "Incident Commander", "deadline_minutes": 15},
            {"name": "Assess Impact", "description": "Assess the scope and impact of the crisis", "responsible_role": "Technical Lead", "deadline_minutes": 30},
            {"name": "Notify Leadership", "description": "Notify executive leadership and legal", "responsible_role": "Communications Lead", "deadline_minutes": 30},
            {"name": "Activate Crisis Team", "description": "Assemble the crisis response team", "responsible_role": "Incident Commander", "deadline_minutes": 60},
            {"name": "Contain the Issue", "description": "Take immediate actions to contain the crisis", "responsible_role": "Technical Lead", "deadline_minutes": 120},
            {"name": "Initial Communication", "description": "Send initial stakeholder communications", "responsible_role": "Communications Lead", "deadline_minutes": 60},
            {"name": "Root Cause Analysis", "description": "Investigate and identify root cause", "responsible_role": "Technical Lead", "deadline_minutes": 240},
            {"name": "Implement Fix", "description": "Deploy fix or mitigation", "responsible_role": "Technical Lead", "deadline_minutes": 480},
            {"name": "Verify Resolution", "description": "Verify the crisis is resolved", "responsible_role": "Technical Lead", "deadline_minutes": 600},
            {"name": "Stakeholder Update", "description": "Send resolution communication to all stakeholders", "responsible_role": "Communications Lead", "deadline_minutes": 660},
            {"name": "Stand Down", "description": "Stand down crisis team and return to normal operations", "responsible_role": "Incident Commander", "deadline_minutes": 720},
        ]
        if severity in [CrisisSeverity.CRITICAL, CrisisSeverity.HIGH]:
            steps.insert(3, {"name": "Legal Review", "description": "Conduct legal review of the situation", "responsible_role": "Legal Advisor", "deadline_minutes": 60})
        if crisis_type in [CrisisType.DATA_BREACH, CrisisType.SECURITY, CrisisType.CYBER]:
            steps.insert(5, {"name": "Regulatory Notification", "description": "Assess and execute regulatory notification requirements", "responsible_role": "Legal Advisor", "deadline_minutes": 120})
        return steps

    def _generate_templates(
        self,
        crisis_type: CrisisType,
        severity: CrisisSeverity,
    ) -> Dict[str, str]:
        return {
            "initial_alert": f"URGENT: {crisis_type.value} incident detected. Severity: {severity.value}. Team is investigating.",
            "situation_update": f"UPDATE: {crisis_type.value} incident update. Status: Investigating. More details to follow.",
            "resolution": f"RESOLVED: The {crisis_type.value} incident has been resolved. Root cause identified and addressed.",
            "preventive": f"FOLLOW-UP: Measures implemented to prevent recurrence of {crisis_type.value} incidents.",
        }

    def _get_preferred_channel(self, audience: AudienceType) -> CommunicationChannel:
        channel_map = {
            AudienceType.INTERNAL_EXECUTIVE: CommunicationChannel.PHONE,
            AudienceType.INTERNAL_LEGAL: CommunicationChannel.EMAIL,
            AudienceType.INTERNAL_ENGINEERING: CommunicationChannel.SLACK,
            AudienceType.INTERNAL_ALL_EMPLOYEES: CommunicationChannel.EMAIL,
            AudienceType.EXTERNAL_CUSTOMERS: CommunicationChannel.CUSTOMER_PORTAL,
            AudienceType.EXTERNAL_MEDIA: CommunicationChannel.PRESS_RELEASE,
            AudienceType.EXTERNAL_REGULATORS: CommunicationChannel.REGULATORY_FILING,
            AudienceType.EXTERNAL_INVESTORS: CommunicationChannel.INVESTOR_RELATIONS,
            AudienceType.EXTERNAL_PARTNERS: CommunicationChannel.PARTNER_NOTIFICATION,
            AudienceType.EXTERNAL_PUBLIC: CommunicationChannel.WEBSITE_BANNER,
        }
        return channel_map.get(audience, CommunicationChannel.EMAIL)

    def _generate_default_lessons(self, crisis_type: CrisisType) -> List[Dict[str, Any]]:
        return [
            {"title": "Improve Detection", "description": f"Enhance monitoring for {crisis_type.value} scenarios", "category": LessonCategory.PROCESS, "severity": CrisisSeverity.HIGH, "recommendation": "Implement additional monitoring and alerting rules"},
            {"title": "Communication Speed", "description": "Improve speed of stakeholder notifications", "category": LessonCategory.COMMUNICATION, "severity": CrisisSeverity.MEDIUM, "recommendation": "Automate initial notification workflows"},
            {"title": "Runbook Completeness", "description": "Ensure crisis runbooks cover all scenarios", "category": LessonCategory.PROCESS, "severity": CrisisSeverity.MEDIUM, "recommendation": "Review and update crisis playbooks quarterly"},
            {"title": "Training Gaps", "description": "Identify training gaps in crisis response", "category": LessonCategory.TRAINING, "severity": CrisisSeverity.LOW, "recommendation": "Conduct quarterly crisis simulation exercises"},
        ]

    # ----- Status & Diagnostics -----

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status."""
        return {
            "agent": self._config.agent_name,
            "version": self._config.version,
            "plans": len(self._plans),
            "active_crises": len(self.get_active_crises()),
            "total_crises": len(self._crises),
            "communication_plans": len(self._communication_plans),
            "stakeholders": len(self._stakeholder_registry.stakeholders),
            "recovery_plans": len(self._recovery_plans),
            "post_mortems": len(self._post_mortems),
            "operations_logged": len(self._operation_log),
            "cache_size": self._cache.size() if self._cache else 0,
        }

    def get_operation_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent operation log entries."""
        return self._operation_log[-limit:]

    def clear_cache(self) -> int:
        """Clear the cache."""
        if self._cache:
            size = self._cache.size()
            self._cache.clear()
            return size
        return 0

    def export_data(self, format: str = "json") -> str:
        """Export all agent data."""
        data = {
            "plans": [p.to_dict() for p in self._plans.values()],
            "crises": [c.to_dict() for c in self._crises.values()],
            "communication_plans": [p.to_dict() for p in self._communication_plans.values()],
            "stakeholder_registry": self._stakeholder_registry.to_dict(),
            "recovery_plans": [r.to_dict() for r in self._recovery_plans.values()],
            "post_mortems": [p.to_dict() for p in self._post_mortems.values()],
            "status": self.get_status(),
        }
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        return str(data)


# ---------------------------------------------------------------------------
# CLI Demo
# ---------------------------------------------------------------------------


def main() -> None:
    """Demonstrate Crisis Management Agent capabilities."""
    print("=" * 70)
    print("Crisis Management Agent v3.0.0 - Comprehensive Demo")
    print("=" * 70)

    agent = CrisisManagementAgent()

    print("\n--- Adding Stakeholders ---")
    stakeholders = [
        ("Jane Smith", "CEO", "Executive", StakeholderPriority.P1_IMMEDIATE),
        ("Legal Team", "Legal Counsel", "Legal", StakeholderPriority.P2_URGENT),
        ("CTO", "Chief Technology Officer", "Engineering", StakeholderPriority.P2_URGENT),
        ("VP Marketing", "VP of Marketing", "Marketing", StakeholderPriority.P3_HIGH),
        ("Engineering Team", "Engineering Staff", "Engineering", StakeholderPriority.P4_MEDIUM),
        ("All Employees", "全体员工", "HR", StakeholderPriority.P5_STANDARD),
    ]
    for name, role, dept, priority in stakeholders:
        agent.add_stakeholder(name=name, role=role, department=dept, priority=priority)
    print(f"Added {len(stakeholders)} stakeholders")

    print("\n--- Creating Crisis Plan ---")
    plan = agent.create_crisis_plan(
        name="Data Breach Response Plan",
        scenario="Customer PII exposed due to misconfigured S3 bucket",
        crisis_type=CrisisType.DATA_BREACH,
        severity=CrisisSeverity.CRITICAL,
        contacts=[
            {"name": "Jane Smith", "role": "CEO", "priority": 1},
            {"name": "Legal Team", "role": "Legal", "priority": 2},
            {"name": "CTO", "role": "Technical", "priority": 2},
        ],
        compliance=[
            ComplianceRequirement.GDPR_72HR,
            ComplianceRequirement.STATE_BREACH,
            ComplianceRequirement.CUSTOMER_NOTIFICATION,
        ],
    )
    print(f"Plan created: {plan.name} ({plan.plan_id})")
    print(f"Steps: {len(plan.steps)}")
    print(f"Contacts: {len(plan.contacts)}")

    print("\n--- Testing Crisis Plan ---")
    test_result = agent.test_crisis_plan(plan.plan_id)
    print(f"Gaps found: {len(test_result['gaps'])}")
    for gap in test_result["gaps"]:
        print(f"  - {gap}")

    print("\n--- Activating Crisis ---")
    crisis = agent.activate_crisis(
        plan_id=plan.plan_id,
        title="Customer Data Breach - S3 Bucket Exposure",
        description="Security team discovered misconfigured S3 bucket exposing customer PII",
        severity=CrisisSeverity.CRITICAL,
        trigger=CrisisTrigger.SECURITY_SCAN,
        incident_commander="CTO",
    )
    print(f"Crisis activated: {crisis.title} ({crisis.crisis_id})")
    print(f"Severity: {crisis.severity.value}")

    print("\n--- Updating Crisis Status ---")
    agent.update_crisis_status(crisis.crisis_id, IncidentStatus.ACKNOWLEDGED, "Incident acknowledged by CTO")
    agent.update_crisis_status(crisis.crisis_id, IncidentStatus.INVESTIGATING, "Security team investigating")
    agent.escalate_crisis(crisis.crisis_id, EscalationLevel.L4_C_SUITE, "Critical data breach requires C-suite attention")
    print(f"Status: {crisis.status.value}")
    print(f"Timeline entries: {len(crisis.timeline)}")

    print("\n--- Developing Communication Plan ---")
    comm_plan = agent.develop_communication_plan(
        crisis_id=crisis.crisis_id,
        strategy="Transparent, empathetic communication focusing on customer protection",
        key_messages=[
            "We have identified unauthorized access to customer data",
            "We are taking immediate steps to secure the affected systems",
            "Affected customers will be notified directly",
            "We are working with law enforcement and regulators",
        ],
        spokesperson="Jane Smith, CEO",
    )
    print(f"Communication plan: {comm_plan.plan_id}")
    print(f"Audiences: {len(comm_plan.audience_matrix)}")

    print("\n--- Sending Communications ---")
    initial = agent.send_communication(
        crisis_id=crisis.crisis_id,
        message_type=MessageType.INITIAL_ALERT,
        channel=CommunicationChannel.SLACK,
        audience=AudienceType.INTERNAL_ALL_EMPLOYEES,
        subject="URGENT: Data Breach Detected",
        body="We have detected a data breach affecting customer data. The security team is actively investigating. More updates to follow.",
    )
    print(f"Communication sent: {initial.message_type.value} via {initial.channel.value}")

    customer_comm = agent.send_communication(
        crisis_id=crisis.crisis_id,
        message_type=MessageType.CUSTOMER_ADVISORY,
        channel=CommunicationChannel.EMAIL,
        audience=AudienceType.EXTERNAL_CUSTOMERS,
        subject="Important Security Notice",
        body="We are writing to inform you of a security incident that may have affected your personal information.",
    )
    print(f"Customer advisory sent: {customer_comm.status}")

    print("\n--- Developing Recovery Plan ---")
    recovery = agent.develop_recovery(
        crisis_id=crisis.crisis_id,
        rto_hours=4,
        rpo_hours=1,
        mttr_hours=24,
    )
    print(f"Recovery plan: {recovery.plan_id}")
    print(f"Milestones: {len(recovery.milestones)}")
    print(f"RTO: {recovery.rto_hours}h, RPO: {recovery.rpo_hours}h, MTTR: {recovery.mttr_hours}h")

    print("\n--- Resolving Crisis ---")
    agent.update_crisis_status(crisis.crisis_id, IncidentStatus.CONTAINED, "Breach contained, affected bucket secured")
    agent.update_crisis_status(crisis.crisis_id, IncidentStatus.RECOVERING, "Restoring from clean backup")
    agent.update_crisis_status(crisis.crisis_id, IncidentStatus.RESOLVED, "All systems restored, monitoring in place")
    print(f"Final status: {crisis.status.value}")
    print(f"Duration: {crisis.get_duration_hours():.2f} hours")

    print("\n--- Generating Post-Mortem ---")
    post_mortem = agent.generate_post_mortem(
        crisis_id=crisis.crisis_id,
        title="Post-Mortem: Customer Data Breach - S3 Bucket Exposure",
        participants=["CTO", "Security Lead", "Legal Counsel", "Communications Lead"],
    )
    print(f"Post-mortem: {post_mortem.title}")
    print(f"Lessons: {len(post_mortem.lessons)}")
    print(f"What went well: {len(post_mortem.what_went_well)}")
    print(f"What went wrong: {len(post_mortem.what_went_wrong)}")

    print("\n--- Crisis Dashboard ---")
    dashboard = agent.get_crisis_dashboard()
    for key, value in dashboard.items():
        print(f"  {key}: {value}")

    print("\n--- Agent Status ---")
    status = agent.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
