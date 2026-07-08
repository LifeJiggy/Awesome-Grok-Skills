"""
Compliance Audit Agent - Regulatory Compliance Management.

Provides comprehensive compliance assessment, audit management, policy enforcement,
risk assessment, remediation tracking, and regulatory adherence capabilities.
Supports SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001, CCPA, and custom compliance
frameworks with full audit lifecycle management.
"""

from __future__ import annotations

import logging
import uuid
import json
import hashlib
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Set
from collections import defaultdict

logger = logging.getLogger(__name__)


# =============================================================================
# Enumerations
# =============================================================================

class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    SOC2 = "SOC2"
    SOC2_TYPE1 = "SOC2_Type1"
    SOC2_TYPE2 = "SOC2_Type2"
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    PCI_DSS = "PCI_DSS"
    ISO27001 = "ISO27001"
    CCPA = "CCPA"
    NIST_CSF = "NIST_CSF"
    SOX = "SOX"
    FedRAMP = "FedRAMP"
    HITRUST = "HITRUST"
    CSA_CCM = "CSA_CCM"
    CIS = "CIS"
    COBIT = "COBIT"
    PCI_4 = "PCI_DSS_v4"


class ComplianceStatus(Enum):
    """Compliance assessment status."""
    NOT_ASSESSED = "not_assessed"
    IN_PROGRESS = "in_progress"
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    EXCEPTION = "exception"
    REMEDIATION_IN_PROGRESS = "remediation_in_progress"


class Severity(Enum):
    """Finding severity levels."""
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditStatus(Enum):
    """Audit lifecycle status."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    FIELDWORK_COMPLETE = "fieldwork_complete"
    REPORTING = "reporting"
    COMPLETE = "complete"
    FOLLOW_UP = "follow_up"
    CANCELLED = "cancelled"


class AuditType(Enum):
    """Types of audits."""
    INTERNAL = "internal"
    EXTERNAL = "external"
    SELF_ASSESSMENT = "self_assessment"
    PENETRATION_TEST = "penetration_test"
    VULNERABILITY_ASSESSMENT = "vulnerability_assessment"
    CODE_REVIEW = "code_review"
    CONFIGURATION_AUDIT = "configuration_audit"
    VENDOR_AUDIT = "vendor_audit"
    REGULATORY = "regulatory"
    SURPRISE = "surprise"


class PolicyStatus(Enum):
    """Policy lifecycle status."""
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ACTIVE = "active"
    UNDER_REVISION = "under_revision"
    RETIRED = "retired"


class RemediationStatus(Enum):
    """Remediation tracking status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    CLOSED = "closed"
    ACCEPTED_RISK = "accepted_risk"


class RiskLevel(Enum):
    """Risk assessment levels."""
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EvidenceType(Enum):
    """Types of audit evidence."""
    DOCUMENT = "document"
    SCREENSHOT = "screenshot"
    LOG = "log"
    CONFIGURATION = "configuration"
    POLICY = "policy"
    TRAINING_RECORD = "training_record"
    ACCESS_REPORT = "access_report"
    VULNERABILITY_REPORT = "vulnerability_report"
    TEST_RESULT = "test_result"
    SCREENCAST = "screencast"
    ATTESTATION = "attestation"
    INTERVIEW_NOTES = "interview_notes"


class ControlCategory(Enum):
    """Categories of security controls."""
    ACCESS_CONTROL = "access_control"
    DATA_PROTECTION = "data_protection"
    NETWORK_SECURITY = "network_security"
    PHYSICAL_SECURITY = "physical_security"
    OPERATIONS = "operations"
    CHANGE_MANAGEMENT = "change_management"
    RISK_MANAGEMENT = "risk_management"
    COMPLIANCE = "compliance"
    INCIDENT_RESPONSE = "incident_response"
    BUSINESS_CONTINUITY = "business_continuity"
    VENDOR_MANAGEMENT = "vendor_management"
    HUMAN_RESOURCES = "human_resources"
    ASSET_MANAGEMENT = "asset_management"
    CRYPTOGRAPHY = "cryptography"
    MONITORING = "monitoring"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Control:
    """A compliance control."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    framework: ComplianceFramework = ComplianceFramework.SOC2
    control_id: str = ""
    name: str = ""
    description: str = ""
    category: ControlCategory = ControlCategory.ACCESS_CONTROL
    requirements: List[str] = field(default_factory=list)
    implementation_guidance: str = ""
    test_procedure: str = ""
    evidence_requirements: List[str] = field(default_factory=list)
    status: ComplianceStatus = ComplianceStatus.NOT_ASSESSED
    owner: str = ""
    frequency: str = "annual"
    automated: bool = False
    related_controls: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "framework": self.framework.value,
            "control_id": self.control_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "requirements": self.requirements,
            "implementation_guidance": self.implementation_guidance,
            "test_procedure": self.test_procedure,
            "evidence_requirements": self.evidence_requirements,
            "status": self.status.value,
            "owner": self.owner,
            "frequency": self.frequency,
            "automated": self.automated,
            "related_controls": self.related_controls,
        }


@dataclass
class Finding:
    """An audit finding."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    severity: Severity = Severity.MEDIUM
    control_id: str = ""
    framework: ComplianceFramework = ComplianceFramework.SOC2
    category: str = ""
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    recommendation: str = ""
    remediation_plan: str = ""
    remediation_status: RemediationStatus = RemediationStatus.OPEN
    remediation_owner: str = ""
    remediation_deadline: Optional[datetime] = None
    risk_level: RiskLevel = RiskLevel.MEDIUM
    affected_assets: List[str] = field(default_factory=list)
    cve_ids: List[str] = field(default_factory=list)
    cvss_score: Optional[float] = None
    identified_date: datetime = field(default_factory=datetime.utcnow)
    verified_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "control_id": self.control_id,
            "framework": self.framework.value,
            "category": self.category,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "remediation_plan": self.remediation_plan,
            "remediation_status": self.remediation_status.value,
            "remediation_owner": self.remediation_owner,
            "remediation_deadline": self.remediation_deadline.isoformat() if self.remediation_deadline else None,
            "risk_level": self.risk_level.value,
            "affected_assets": self.affected_assets,
            "cve_ids": self.cve_ids,
            "cvss_score": self.cvss_score,
            "identified_date": self.identified_date.isoformat(),
            "verified_date": self.verified_date.isoformat() if self.verified_date else None,
            "closed_date": self.closed_date.isoformat() if self.closed_date else None,
        }


@dataclass
class Policy:
    """An organizational policy."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    version: str = "1.0"
    status: PolicyStatus = PolicyStatus.DRAFT
    category: str = ""
    owner: str = ""
    approved_by: str = ""
    effective_date: Optional[datetime] = None
    review_date: Optional[datetime] = None
    next_review: Optional[datetime] = None
    frameworks: List[ComplianceFramework] = field(default_factory=list)
    content: str = ""
    attachments: List[str] = field(default_factory=list)
    review_history: List[Dict[str, Any]] = field(default_factory=list)
    training_required: bool = False
    acknowledgment_required: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "version": self.version,
            "status": self.status.value,
            "category": self.category,
            "owner": self.owner,
            "approved_by": self.approved_by,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "review_date": self.review_date.isoformat() if self.review_date else None,
            "next_review": self.next_review.isoformat() if self.next_review else None,
            "frameworks": [f.value for f in self.frameworks],
            "training_required": self.training_required,
            "acknowledgment_required": self.acknowledgment_required,
        }


@dataclass
class AuditScope:
    """Defines the scope of an audit."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    frameworks: List[ComplianceFramework] = field(default_factory=list)
    systems: List[str] = field(default_factory=list)
    departments: List[str] = field(default_factory=list)
    excluded_systems: List[str] = field(default_factory=list)
    time_period_start: Optional[datetime] = None
    time_period_end: Optional[datetime] = None
    key_personnel: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "frameworks": [f.value for f in self.frameworks],
            "systems": self.systems,
            "departments": self.departments,
            "excluded_systems": self.excluded_systems,
            "time_period_start": self.time_period_start.isoformat() if self.time_period_start else None,
            "time_period_end": self.time_period_end.isoformat() if self.time_period_end else None,
            "key_personnel": self.key_personnel,
        }


@dataclass
class Audit:
    """A compliance audit."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    audit_type: AuditType = AuditType.INTERNAL
    status: AuditStatus = AuditStatus.PLANNED
    framework: ComplianceFramework = ComplianceFramework.SOC2
    scope: Optional[AuditScope] = None
    lead_auditor: str = ""
    audit_team: List[str] = field(default_factory=list)
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    findings: List[Finding] = field(default_factory=list)
    controls_tested: List[str] = field(default_factory=list)
    evidence_collected: List[Dict[str, Any]] = field(default_factory=list)
    overall_score: float = 0.0
    compliance_rate: float = 0.0
    report_url: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "audit_type": self.audit_type.value,
            "status": self.status.value,
            "framework": self.framework.value,
            "scope": self.scope.to_dict() if self.scope else None,
            "lead_auditor": self.lead_auditor,
            "audit_team": self.audit_team,
            "planned_start": self.planned_start.isoformat() if self.planned_start else None,
            "planned_end": self.planned_end.isoformat() if self.planned_end else None,
            "actual_start": self.actual_start.isoformat() if self.actual_start else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "findings_count": len(self.findings),
            "controls_tested": len(self.controls_tested),
            "evidence_collected": len(self.evidence_collected),
            "overall_score": self.overall_score,
            "compliance_rate": self.compliance_rate,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class RiskAssessment:
    """A risk assessment entry."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    asset: str = ""
    threat: str = ""
    vulnerability: str = ""
    risk_level: RiskLevel = RiskLevel.MEDIUM
    likelihood: float = 0.5
    impact: float = 0.5
    risk_score: float = 0.25
    existing_controls: List[str] = field(default_factory=list)
    residual_risk: RiskLevel = RiskLevel.MEDIUM
    mitigation_plan: str = ""
    risk_owner: str = ""
    assessment_date: datetime = field(default_factory=datetime.utcnow)
    review_date: Optional[datetime] = None
    status: str = "open"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "asset": self.asset,
            "threat": self.threat,
            "vulnerability": self.vulnerability,
            "risk_level": self.risk_level.value,
            "likelihood": self.likelihood,
            "impact": self.impact,
            "risk_score": self.risk_score,
            "existing_controls": self.existing_controls,
            "residual_risk": self.residual_risk.value,
            "mitigation_plan": self.mitigation_plan,
            "risk_owner": self.risk_owner,
            "assessment_date": self.assessment_date.isoformat(),
            "review_date": self.review_date.isoformat() if self.review_date else None,
            "status": self.status,
        }


@dataclass
class Evidence:
    """Audit evidence."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    evidence_type: EvidenceType = EvidenceType.DOCUMENT
    description: str = ""
    file_path: str = ""
    hash_sha256: str = ""
    collected_by: str = ""
    collected_date: datetime = field(default_factory=datetime.utcnow)
    control_ids: List[str] = field(default_factory=list)
    finding_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    verified: bool = False
    verified_by: str = ""
    verification_date: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "evidence_type": self.evidence_type.value,
            "description": self.description,
            "file_path": self.file_path,
            "hash_sha256": self.hash_sha256,
            "collected_by": self.collected_by,
            "collected_date": self.collected_date.isoformat(),
            "control_ids": self.control_ids,
            "finding_ids": self.finding_ids,
            "tags": self.tags,
            "verified": self.verified,
            "verified_by": self.verified_by,
        }


# =============================================================================
# Compliance Framework Manager
# =============================================================================

class ComplianceFrameworkManager:
    """
    Manages compliance frameworks, controls, and requirements.

    Provides framework-specific control libraries, mapping between
    frameworks, and compliance status tracking.
    """

    CONTROL_LIBRARIES: Dict[str, List[Dict[str, Any]]] = {
        "SOC2": [
            {"control_id": "CC1.1", "name": "COSO Principle 1", "description": "The entity demonstrates a commitment to integrity and ethical values", "category": "control_environment"},
            {"control_id": "CC1.2", "name": "Board Oversight", "description": "The board of directors demonstrates independence from management and exercises oversight", "category": "control_environment"},
            {"control_id": "CC2.1", "name": "Internal Communication", "description": "The entity generates and uses quality information to support functioning of internal control", "category": "information"},
            {"control_id": "CC3.1", "name": "Risk Assessment", "description": "The entity specifies objectives with sufficient clarity to identify and assess risks", "category": "risk_assessment"},
            {"control_id": "CC4.1", "name": "Monitoring Activities", "description": "The entity selects, develops, and performs ongoing evaluations", "category": "monitoring"},
            {"control_id": "CC5.1", "name": "Control Activities", "description": "The entity selects and develops control activities that contribute to mitigation of risks", "category": "control_activities"},
            {"control_id": "CC6.1", "name": "Logical Access", "description": "The entity implements logical access security measures", "category": "logical_access"},
            {"control_id": "CC6.2", "name": "User Registration", "description": "Prior to issuing system credentials, the entity registers and authorizes new users", "category": "logical_access"},
            {"control_id": "CC6.3", "name": "Access Removal", "description": "The entity authorizes, modifies, or removes access to data, software, and systems", "category": "logical_access"},
            {"control_id": "CC7.1", "name": "Vulnerability Management", "description": "To meet its objectives, the entity uses detection and monitoring procedures", "category": "system_operations"},
            {"control_id": "CC7.2", "name": "Incident Response", "description": "The entity monitors system components and the operation of those components", "category": "system_operations"},
            {"control_id": "CC8.1", "name": "Change Management", "description": "The entity authorizes, designs, develops or acquires, configures, documents, tests, approves changes", "category": "change_management"},
            {"control_id": "CC9.1", "name": "Risk Mitigation", "description": "The entity identifies, selects, and develops risk mitigation activities", "category": "risk_mitigation"},
            {"control_id": "A1.1", "name": "Capacity Management", "description": "The entity authorizes, designs, develops or acquires, implements, operates, approves, maintains infrastructure", "category": "availability"},
            {"control_id": "PI1.1", "name": "Data Classification", "description": "The entity identifies and maintains confidential information", "category": "processing_integrity"},
            {"control_id": "PR1.1", "name": "Data Protection", "description": "The entity implements policies and procedures to protect against unauthorized access", "category": "privacy"},
        ],
        "GDPR": [
            {"control_id": "Art.5", "name": "Principles of Processing", "description": "Personal data shall be processed lawfully, fairly, and transparently", "category": "data_protection"},
            {"control_id": "Art.6", "name": "Lawful Basis", "description": "Processing shall be lawful only if at least one lawful basis applies", "category": "lawful_processing"},
            {"control_id": "Art.12", "name": "Transparent Communication", "description": "Information shall be provided in a concise, transparent, intelligible form", "category": "data_subject_rights"},
            {"control_id": "Art.15", "name": "Right of Access", "description": "The data subject shall have the right to obtain confirmation and access", "category": "data_subject_rights"},
            {"control_id": "Art.17", "name": "Right to Erasure", "description": "The data subject shall have the right to obtain erasure of personal data", "category": "data_subject_rights"},
            {"control_id": "Art.25", "name": "Data Protection by Design", "description": "Data protection by design and by default measures shall be implemented", "category": "privacy_by_design"},
            {"control_id": "Art.30", "name": "Records of Processing", "description": "The controller shall maintain a record of processing activities", "category": "accountability"},
            {"control_id": "Art.32", "name": "Security of Processing", "description": "Appropriate technical and organizational measures shall be implemented", "category": "security"},
            {"control_id": "Art.33", "name": "Breach Notification", "description": "The controller shall notify the supervisory authority within 72 hours", "category": "incident_response"},
            {"control_id": "Art.35", "name": "DPIA", "description": "A data protection impact assessment shall be carried out", "category": "risk_assessment"},
            {"control_id": "Art.37", "name": "DPO", "description": "The controller and processor shall designate a data protection officer", "category": "governance"},
            {"control_id": "Art.44-49", "name": "International Transfers", "description": "Transfer of personal data to third countries shall meet specific conditions", "category": "data_transfers"},
        ],
        "HIPAA": [
            {"control_id": "164.308(a)(1)", "name": "Security Management Process", "description": "Implement policies and procedures to prevent, detect, contain, and correct security violations", "category": "administrative"},
            {"control_id": "164.308(a)(3)", "name": "Workforce Security", "description": "Implement policies and procedures to ensure workforce members have appropriate access", "category": "administrative"},
            {"control_id": "164.308(a)(4)", "name": "Information Access Management", "description": "Implement policies and procedures for authorizing access to ePHI", "category": "administrative"},
            {"control_id": "164.308(a)(5)", "name": "Security Awareness Training", "description": "Implement a security awareness and training program", "category": "administrative"},
            {"control_id": "164.308(a)(6)", "name": "Security Incident Procedures", "description": "Implement policies and procedures to address security incidents", "category": "administrative"},
            {"control_id": "164.310(a)(1)", "name": "Facility Access Controls", "description": "Implement policies and procedures to limit physical access to facilities", "category": "physical"},
            {"control_id": "164.312(a)(1)", "name": "Access Control", "description": "Implement technical policies and procedures for electronic information systems", "category": "technical"},
            {"control_id": "164.312(b)", "name": "Audit Controls", "description": "Implement hardware, software, and/or procedural mechanisms to record and examine activity", "category": "technical"},
            {"control_id": "164.312(c)(1)", "name": "Integrity Controls", "description": "Implement policies and procedures to protect ePHI from improper alteration or destruction", "category": "technical"},
            {"control_id": "164.312(d)", "name": "Authentication", "description": "Implement procedures to verify identity of person or entity seeking access to ePHI", "category": "technical"},
            {"control_id": "164.312(e)(1)", "name": "Transmission Security", "description": "Implement technical security measures to guard against unauthorized access during transmission", "category": "technical"},
        ],
        "PCI_DSS": [
            {"control_id": "1.1", "name": "Firewall Configuration", "description": "Install and maintain a firewall configuration to protect cardholder data", "category": "network_security"},
            {"control_id": "2.1", "name": "Default Passwords", "description": "Do not use vendor-supplied defaults for system passwords and security parameters", "category": "secure_configuration"},
            {"control_id": "3.1", "name": "Data Retention", "description": "Keep cardholder data storage to a minimum", "category": "data_protection"},
            {"control_id": "4.1", "name": "Encryption in Transit", "description": "Encrypt transmission of cardholder data across open, public networks", "category": "encryption"},
            {"control_id": "5.1", "name": "Anti-Virus", "description": "Use and regularly update anti-virus software on all systems", "category": "malware_protection"},
            {"control_id": "6.1", "name": "Secure Development", "description": "Establish a process to identify security vulnerabilities", "category": "secure_development"},
            {"control_id": "7.1", "name": "Need-to-Know Access", "description": "Limit access to system components and cardholder data to only authorized individuals", "category": "access_control"},
            {"control_id": "8.1", "name": "Unique IDs", "description": "Assign a unique ID to each person with computer access", "category": "authentication"},
            {"control_id": "9.1", "name": "Physical Access", "description": "Implement physical measures to protect cardholder data", "category": "physical_security"},
            {"control_id": "10.1", "name": "Audit Logs", "description": "Implement audit trails to link all access to system components", "category": "logging"},
            {"control_id": "11.1", "name": "Vulnerability Scanning", "description": "Test security of systems and networks regularly", "category": "testing"},
            {"control_id": "12.1", "name": "Security Policy", "description": "Establish an information security policy", "category": "policy"},
        ],
    }

    FRAMEWORK_CROSS_MAP: Dict[str, Dict[str, List[str]]] = {
        "SOC2_to_ISO27001": {
            "CC6.1": ["A.9.1", "A.9.2"],
            "CC7.1": ["A.12.6", "A.12.2"],
            "CC8.1": ["A.12.1"],
        },
    }

    def __init__(self) -> None:
        self._frameworks: Dict[str, List[Control]] = {}
        self._initialize_frameworks()

    def _initialize_frameworks(self) -> None:
        for fw_name, controls_data in self.CONTROL_LIBRARIES.items():
            controls: List[Control] = []
            for cd in controls_data:
                control = Control(
                    framework=ComplianceFramework(fw_name) if fw_name in [e.value for e in ComplianceFramework] else ComplianceFramework.SOC2,
                    control_id=cd["control_id"],
                    name=cd["name"],
                    description=cd["description"],
                    category=ControlCategory(cd["category"]) if cd["category"] in [e.value for e in ControlCategory] else ControlCategory.COMPLIANCE,
                )
                controls.append(control)
            self._frameworks[fw_name] = controls

    def get_controls(self, framework: str) -> List[Dict[str, Any]]:
        controls = self._frameworks.get(framework, [])
        return [c.to_dict() for c in controls]

    def get_control(self, framework: str, control_id: str) -> Optional[Dict[str, Any]]:
        controls = self._frameworks.get(framework, [])
        for c in controls:
            if c.control_id == control_id:
                return c.to_dict()
        return None

    def map_controls(
        self, source_framework: str, target_framework: str
    ) -> Dict[str, Any]:
        """Map controls between two frameworks."""
        map_key = f"{source_framework}_to_{target_framework}"
        mapping = self.FRAMEWORK_CROSS_MAP.get(map_key, {})

        source_controls = self._frameworks.get(source_framework, [])
        target_controls = self._frameworks.get(target_framework, [])

        return {
            "source_framework": source_framework,
            "target_framework": target_framework,
            "mapping": mapping,
            "source_controls_count": len(source_controls),
            "target_controls_count": len(target_controls),
        }

    def get_frameworks_summary(self) -> Dict[str, Any]:
        return {
            fw: {
                "controls_count": len(controls),
                "categories": list(set(c.category.value for c in controls)),
            }
            for fw, controls in self._frameworks.items()
        }


# =============================================================================
# Risk Assessment Engine
# =============================================================================

class RiskAssessmentEngine:
    """
    Performs and manages organizational risk assessments.

    Identifies risks, evaluates likelihood and impact,
    and tracks mitigation strategies.
    """

    def __init__(self) -> None:
        self._assessments: Dict[str, RiskAssessment] = {}
        self._risk_register: List[RiskAssessment] = []

    def assess_risk(
        self,
        asset: str,
        threat: str,
        vulnerability: str,
        likelihood: float,
        impact: float,
        existing_controls: Optional[List[str]] = None,
        mitigation_plan: str = "",
        risk_owner: str = "",
    ) -> RiskAssessment:
        """Create a new risk assessment."""
        likelihood = max(0.0, min(1.0, likelihood))
        impact = max(0.0, min(1.0, impact))
        risk_score = round(likelihood * impact, 3)

        if risk_score >= 0.7:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 0.5:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 0.3:
            risk_level = RiskLevel.MEDIUM
        elif risk_score >= 0.1:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.NEGLIGIBLE

        assessment = RiskAssessment(
            asset=asset,
            threat=threat,
            vulnerability=vulnerability,
            likelihood=likelihood,
            impact=impact,
            risk_score=risk_score,
            risk_level=risk_level,
            existing_controls=existing_controls or [],
            mitigation_plan=mitigation_plan,
            risk_owner=risk_owner,
            residual_risk=risk_level,
        )

        self._assessments[assessment.id] = assessment
        self._risk_register.append(assessment)

        return assessment

    def update_residual_risk(
        self, risk_id: str, new_residual: str, mitigation_notes: str = ""
    ) -> Dict[str, Any]:
        """Update residual risk after mitigation."""
        assessment = self._assessments.get(risk_id)
        if not assessment:
            return {"error": f"Risk {risk_id} not found"}

        rr = RiskLevel(new_residual) if new_residual in [e.value for e in RiskLevel] else RiskLevel.MEDIUM
        assessment.residual_risk = rr
        if mitigation_notes:
            assessment.mitigation_plan += f"\nUpdated: {mitigation_notes}"

        return assessment.to_dict()

    def get_risk_register(
        self, level_filter: Optional[RiskLevel] = None
    ) -> List[Dict[str, Any]]:
        """Get the risk register with optional filtering."""
        risks = self._risk_register
        if level_filter:
            risks = [r for r in risks if r.risk_level == level_filter]
        risks.sort(key=lambda r: r.risk_score, reverse=True)
        return [r.to_dict() for r in risks]

    def risk_summary(self) -> Dict[str, Any]:
        """Summarize the risk register."""
        if not self._risk_register:
            return {"total_risks": 0, "by_level": {}, "average_score": 0.0}

        by_level: Dict[str, int] = defaultdict(int)
        for r in self._risk_register:
            by_level[r.risk_level.value] += 1

        avg_score = sum(r.risk_score for r in self._risk_register) / len(self._risk_register)

        return {
            "total_risks": len(self._risk_register),
            "by_level": dict(by_level),
            "average_score": round(avg_score, 3),
            "highest_risk": self._risk_register[0].to_dict() if self._risk_register else None,
            "critical_count": by_level.get("critical", 0),
            "high_count": by_level.get("high", 0),
        }

    def calculate_risk_trend(self) -> Dict[str, Any]:
        """Calculate risk trend over time."""
        if len(self._risk_register) < 2:
            return {"trend": "insufficient_data"}

        sorted_risks = sorted(self._risk_register, key=lambda r: r.assessment_date)
        first_half = sorted_risks[:len(sorted_risks)//2]
        second_half = sorted_risks[len(sorted_risks)//2:]

        avg_first = sum(r.risk_score for r in first_half) / len(first_half)
        avg_second = sum(r.risk_score for r in second_half) / len(second_half)

        return {
            "earlier_average": round(avg_first, 3),
            "recent_average": round(avg_second, 3),
            "trend": "increasing" if avg_second > avg_first * 1.1 else "decreasing" if avg_second < avg_first * 0.9 else "stable",
        }


# =============================================================================
# Remediation Tracker
# =============================================================================

class RemediationTracker:
    """
    Tracks remediation of compliance findings and risks.

    Manages remediation plans, deadlines, verification,
    and progress reporting.
    """

    def __init__(self) -> None:
        self._items: Dict[str, Finding] = {}
        self._history: List[Dict[str, Any]] = []

    def add_finding(self, finding: Finding) -> str:
        """Add a finding to track for remediation."""
        self._items[finding.id] = finding
        self._log_event(finding.id, "created", finding.title)
        return finding.id

    def update_status(
        self,
        finding_id: str,
        new_status: str,
        notes: str = "",
        updated_by: str = "",
    ) -> Dict[str, Any]:
        """Update the remediation status of a finding."""
        finding = self._items.get(finding_id)
        if not finding:
            return {"error": f"Finding {finding_id} not found"}

        old_status = finding.remediation_status.value
        finding.remediation_status = RemediationStatus(new_status) if new_status in [e.value for e in RemediationStatus] else RemediationStatus.OPEN

        if notes:
            finding.notes += f"\n[{datetime.utcnow().isoformat()}] {notes}"

        if finding.remediation_status == RemediationStatus.VERIFIED:
            finding.verified_date = datetime.utcnow()
        elif finding.remediation_status == RemediationStatus.CLOSED:
            finding.closed_date = datetime.utcnow()

        self._log_event(finding_id, "status_change", f"{old_status} -> {new_status}", updated_by)

        return finding.to_dict()

    def assign_remediation(
        self,
        finding_id: str,
        owner: str,
        deadline_days: int = 30,
        plan: str = "",
    ) -> Dict[str, Any]:
        """Assign remediation to an owner with a deadline."""
        finding = self._items.get(finding_id)
        if not finding:
            return {"error": f"Finding {finding_id} not found"}

        finding.remediation_owner = owner
        finding.remediation_deadline = datetime.utcnow() + timedelta(days=deadline_days)
        finding.remediation_plan = plan or finding.remediation_plan
        finding.remediation_status = RemediationStatus.IN_PROGRESS

        self._log_event(finding_id, "assigned", f"Assigned to {owner}")

        return finding.to_dict()

    def get_overdue(self) -> List[Dict[str, Any]]:
        """Get all findings past their remediation deadline."""
        now = datetime.utcnow()
        overdue = []
        for f in self._items.values():
            if (
                f.remediation_deadline
                and f.remediation_deadline < now
                and f.remediation_status
                not in (RemediationStatus.CLOSED, RemediationStatus.VERIFIED, RemediationStatus.ACCEPTED_RISK)
            ):
                overdue.append(f.to_dict())
        overdue.sort(key=lambda x: x.get("remediation_deadline", ""))
        return overdue

    def get_progress_report(self) -> Dict[str, Any]:
        """Generate a remediation progress report."""
        if not self._items:
            return {"total": 0, "by_status": {}}

        by_status: Dict[str, int] = defaultdict(int)
        by_severity: Dict[str, int] = defaultdict(int)
        for f in self._items.values():
            by_status[f.remediation_status.value] += 1
            by_severity[f.severity.value] += 1

        total = len(self._items)
        closed = by_status.get("closed", 0) + by_status.get("verified", 0)

        return {
            "total": total,
            "by_status": dict(by_status),
            "by_severity": dict(by_severity),
            "completion_rate": round(closed / total, 3) if total > 0 else 0.0,
            "overdue_count": len(self.get_overdue()),
        }

    def _log_event(
        self, finding_id: str, event_type: str, details: str, actor: str = ""
    ) -> None:
        self._history.append({
            "finding_id": finding_id,
            "event_type": event_type,
            "details": details,
            "actor": actor,
            "timestamp": datetime.utcnow().isoformat(),
        })


# =============================================================================
# Evidence Manager
# =============================================================================

class EvidenceManager:
    """
    Manages audit evidence collection, verification, and retention.

    Tracks evidence items, their association with controls and findings,
    and ensures proper chain of custody.
    """

    def __init__(self) -> None:
        self._evidence: Dict[str, Evidence] = {}
        self._by_control: Dict[str, List[str]] = defaultdict(list)
        self._by_finding: Dict[str, List[str]] = defaultdict(list)

    def collect(
        self,
        name: str,
        evidence_type: str,
        description: str = "",
        file_path: str = "",
        control_ids: Optional[List[str]] = None,
        finding_ids: Optional[List[str]] = None,
        collected_by: str = "",
        tags: Optional[List[str]] = None,
    ) -> Evidence:
        """Collect a new piece of evidence."""
        et = EvidenceType(evidence_type) if evidence_type in [e.value for e in EvidenceType] else EvidenceType.DOCUMENT

        evidence = Evidence(
            name=name,
            evidence_type=et,
            description=description,
            file_path=file_path,
            collected_by=collected_by,
            control_ids=control_ids or [],
            finding_ids=finding_ids or [],
            tags=tags or [],
        )

        if file_path:
            evidence.hash_sha256 = hashlib.sha256(file_path.encode()).hexdigest()

        self._evidence[evidence.id] = evidence
        for cid in evidence.control_ids:
            self._by_control[cid].append(evidence.id)
        for fid in evidence.finding_ids:
            self._by_finding[fid].append(evidence.id)

        return evidence

    def verify(self, evidence_id: str, verified_by: str) -> Dict[str, Any]:
        """Verify an evidence item."""
        evidence = self._evidence.get(evidence_id)
        if not evidence:
            return {"error": f"Evidence {evidence_id} not found"}

        evidence.verified = True
        evidence.verified_by = verified_by
        evidence.verification_date = datetime.utcnow()

        return evidence.to_dict()

    def get_for_control(self, control_id: str) -> List[Dict[str, Any]]:
        evidence_ids = self._by_control.get(control_id, [])
        return [self._evidence[eid].to_dict() for eid in evidence_ids if eid in self._evidence]

    def get_for_finding(self, finding_id: str) -> List[Dict[str, Any]]:
        evidence_ids = self._by_finding.get(finding_id, [])
        return [self._evidence[eid].to_dict() for eid in evidence_ids if eid in self._evidence]

    def get_stats(self) -> Dict[str, Any]:
        total = len(self._evidence)
        verified = sum(1 for e in self._evidence.values() if e.verified)
        return {
            "total": total,
            "verified": verified,
            "verification_rate": round(verified / total, 3) if total > 0 else 0.0,
            "by_type": {
                et.value: sum(1 for e in self._evidence.values() if e.evidence_type == et)
                for et in EvidenceType
            },
        }


# =============================================================================
# Policy Manager
# =============================================================================

class PolicyManager:
    """
    Manages organizational policies and their lifecycle.

    Tracks policy creation, review, approval, and compliance
    mapping to frameworks.
    """

    def __init__(self) -> None:
        self._policies: Dict[str, Policy] = {}
        self._templates: Dict[str, str] = {
            "information_security": "This policy establishes the framework for protecting information assets...",
            "access_control": "Access to organizational systems and data shall be granted based on the principle of least privilege...",
            "data_protection": "All personal and sensitive data shall be protected throughout its lifecycle...",
            "incident_response": "The organization shall maintain an incident response plan to detect, respond to, and recover from security incidents...",
            "acceptable_use": "All users of organizational systems shall adhere to acceptable use standards...",
            "change_management": "All changes to production systems shall follow a formal change management process...",
            "business_continuity": "The organization shall maintain plans to ensure continuity of critical business operations...",
        }

    def create_policy(
        self,
        title: str,
        description: str = "",
        category: str = "",
        content: str = "",
        owner: str = "",
        frameworks: Optional[List[str]] = None,
        training_required: bool = False,
    ) -> Policy:
        """Create a new policy."""
        fws = []
        for fw in (frameworks or []):
            try:
                fws.append(ComplianceFramework(fw))
            except ValueError:
                pass

        policy = Policy(
            title=title,
            description=description,
            category=category,
            content=content or self._templates.get(category, ""),
            owner=owner,
            frameworks=fws,
            training_required=training_required,
            status=PolicyStatus.DRAFT,
        )

        self._policies[policy.id] = policy
        return policy

    def approve_policy(self, policy_id: str, approved_by: str) -> Dict[str, Any]:
        """Approve a policy."""
        policy = self._policies.get(policy_id)
        if not policy:
            return {"error": f"Policy {policy_id} not found"}

        policy.status = PolicyStatus.APPROVED
        policy.approved_by = approved_by
        policy.effective_date = datetime.utcnow()
        policy.next_review = datetime.utcnow() + timedelta(days=365)

        policy.review_history.append({
            "action": "approved",
            "by": approved_by,
            "date": datetime.utcnow().isoformat(),
        })

        return policy.to_dict()

    def get_policies_due_for_review(self) -> List[Dict[str, Any]]:
        """Get policies that need review."""
        now = datetime.utcnow()
        due = []
        for p in self._policies.values():
            if p.next_review and p.next_review <= now:
                due.append(p.to_dict())
        return due

    def get_policy_stats(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        for p in self._policies.values():
            by_status[p.status.value] += 1
        return {
            "total": len(self._policies),
            "by_status": dict(by_status),
            "categories": list(set(p.category for p in self._policies.values() if p.category)),
        }


# =============================================================================
# Main Compliance Audit Agent
# =============================================================================

class ComplianceAuditAgent:
    """
    Primary orchestrator for compliance and audit management.

    Coordinates framework management, compliance assessment, audit execution,
    risk assessment, evidence collection, policy management, and remediation
    tracking into a unified compliance workflow.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._framework_manager = ComplianceFrameworkManager()
        self._risk_engine = RiskAssessmentEngine()
        self._remediation_tracker = RemediationTracker()
        self._evidence_manager = EvidenceManager()
        self._policy_manager = PolicyManager()
        self._audits: Dict[str, Audit] = {}
        self._assessments: Dict[str, Dict[str, Any]] = {}
        self._created_at = datetime.utcnow()

        logger.info("ComplianceAuditAgent initialized")

    def assess_compliance(
        self,
        framework: str,
        control_scores: Optional[Dict[str, float]] = None,
        organization: str = "",
    ) -> Dict[str, Any]:
        """
        Assess compliance against a specific framework.

        Evaluates controls and produces a compliance score with gaps.
        """
        controls = self._framework_manager.get_controls(framework)
        if not controls:
            return {"error": f"Framework {framework} not found"}

        if control_scores is None:
            control_scores = {c["control_id"]: 0.5 for c in controls}

        compliant = 0
        partial = 0
        non_compliant = 0
        gaps: List[Dict[str, Any]] = []

        for control in controls:
            score = control_scores.get(control["control_id"], 0.5)
            if score >= 0.8:
                compliant += 1
            elif score >= 0.5:
                partial += 1
            else:
                non_compliant += 1
                gaps.append({
                    "control_id": control["control_id"],
                    "control_name": control["name"],
                    "score": score,
                    "description": control["description"],
                    "severity": "critical" if score < 0.3 else "significant",
                })

        total = len(controls)
        compliance_rate = round(compliant / total, 3) if total > 0 else 0.0
        partial_rate = round(partial / total, 3) if total > 0 else 0.0

        if compliance_rate >= 0.9:
            overall_status = ComplianceStatus.COMPLIANT
        elif compliance_rate >= 0.7:
            overall_status = ComplianceStatus.PARTIALLY_COMPLIANT
        else:
            overall_status = ComplianceStatus.NON_COMPLIANT

        assessment = {
            "framework": framework,
            "organization": organization,
            "overall_status": overall_status.value,
            "compliance_rate": compliance_rate,
            "partial_rate": partial_rate,
            "total_controls": total,
            "compliant": compliant,
            "partially_compliant": partial,
            "non_compliant": non_compliant,
            "gaps": sorted(gaps, key=lambda g: g["score"]),
            "assessed_at": datetime.utcnow().isoformat(),
        }

        self._assessments[framework] = assessment
        return assessment

    def review_policy(
        self,
        policy_title: str,
        category: str = "",
        content: str = "",
        owner: str = "",
        frameworks: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create or review a policy."""
        existing = None
        for p in self._policy_manager._policies.values():
            if p.title == policy_title:
                existing = p
                break

        if existing:
            existing.status = PolicyStatus.UNDER_REVISION
            existing.content = content or existing.content
            existing.review_history.append({
                "action": "revision_started",
                "date": datetime.utcnow().isoformat(),
            })
            return {
                "policy_id": existing.id,
                "status": "under_revision",
                "title": policy_title,
            }

        policy = self._policy_manager.create_policy(
            title=policy_title,
            category=category,
            content=content,
            owner=owner,
            frameworks=frameworks,
        )
        return {
            "policy_id": policy.id,
            "status": policy.status.value,
            "title": policy_title,
            "created": True,
        }

    def prepare_audit(
        self,
        title: str,
        framework: str = "SOC2",
        audit_type: str = "internal",
        lead_auditor: str = "",
        systems: Optional[List[str]] = None,
        departments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Prepare for an upcoming audit."""
        fw = ComplianceFramework(framework) if framework in [e.value for e in ComplianceFramework] else ComplianceFramework.SOC2
        at = AuditType(audit_type) if audit_type in [e.value for e in AuditType] else AuditType.INTERNAL

        scope = AuditScope(
            name=f"{title} Scope",
            frameworks=[fw],
            systems=systems or [],
            departments=departments or [],
        )

        audit = Audit(
            title=title,
            audit_type=at,
            status=AuditStatus.PLANNED,
            framework=fw,
            scope=scope,
            lead_auditor=lead_auditor,
            planned_start=datetime.utcnow() + timedelta(days=7),
            planned_end=datetime.utcnow() + timedelta(days=30),
        )

        self._audits[audit.id] = audit

        controls = self._framework_manager.get_controls(framework)
        return {
            "audit_id": audit.id,
            "title": title,
            "framework": framework,
            "type": audit_type,
            "scope": scope.to_dict(),
            "controls_in_scope": len(controls),
            "planned_start": audit.planned_start.isoformat(),
            "planned_end": audit.planned_end.isoformat(),
            "status": audit.status.value,
        }

    def plan_remediation(
        self,
        finding_id: str,
        owner: str = "",
        deadline_days: int = 30,
        plan: str = "",
    ) -> Dict[str, Any]:
        """Plan remediation for a finding."""
        finding = self._remediation_tracker._items.get(finding_id)
        if not finding:
            finding = Finding(
                title=f"Finding {finding_id}",
                remediation_status=RemediationStatus.OPEN,
            )
            self._remediation_tracker.add_finding(finding)

        return self._remediation_tracker.assign_remediation(
            finding_id=finding.id,
            owner=owner or "security_team",
            deadline_days=deadline_days,
            plan=plan,
        )

    def record_risk(
        self,
        asset: str,
        threat: str,
        vulnerability: str,
        likelihood: float = 0.5,
        impact: float = 0.5,
        mitigation: str = "",
        owner: str = "",
    ) -> Dict[str, Any]:
        """Record a risk assessment."""
        risk = self._risk_engine.assess_risk(
            asset=asset,
            threat=threat,
            vulnerability=vulnerability,
            likelihood=likelihood,
            impact=impact,
            mitigation_plan=mitigation,
            risk_owner=owner,
        )
        return risk.to_dict()

    def collect_evidence(
        self,
        name: str,
        evidence_type: str = "document",
        description: str = "",
        control_ids: Optional[List[str]] = None,
        finding_ids: Optional[List[str]] = None,
        collected_by: str = "",
    ) -> Dict[str, Any]:
        """Collect audit evidence."""
        evidence = self._evidence_manager.collect(
            name=name,
            evidence_type=evidence_type,
            description=description,
            control_ids=control_ids,
            finding_ids=finding_ids,
            collected_by=collected_by,
        )
        return evidence.to_dict()

    def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Get a comprehensive compliance dashboard."""
        latest_assessment = None
        if self._assessments:
            latest_key = list(self._assessments.keys())[-1]
            latest_assessment = self._assessments[latest_key]

        return {
            "frameworks_available": list(self._framework_manager._frameworks.keys()),
            "latest_assessment": latest_assessment,
            "audits": {
                "total": len(self._audits),
                "by_status": {
                    status.value: sum(1 for a in self._audits.values() if a.status == status)
                    for status in AuditStatus
                },
            },
            "risks": self._risk_engine.risk_summary(),
            "remediation": self._remediation_tracker.get_progress_report(),
            "evidence": self._evidence_manager.get_stats(),
            "policies": self._policy_manager.get_policy_stats(),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def list_frameworks(self) -> Dict[str, Any]:
        """List available compliance frameworks."""
        return self._framework_manager.get_frameworks_summary()

    def list_audits(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self._audits.values()]

    def get_audit(self, audit_id: str) -> Optional[Dict[str, Any]]:
        audit = self._audits.get(audit_id)
        return audit.to_dict() if audit else None

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "ComplianceAuditAgent",
            "version": "2.0.0",
            "frameworks_supported": len(self._framework_manager._frameworks),
            "active_audits": len(self._audits),
            "total_findings": len(self._remediation_tracker._items),
            "total_evidence": len(self._evidence_manager._evidence),
            "total_policies": len(self._policy_manager._policies),
            "risk_register_size": len(self._risk_engine._risk_register),
            "uptime": str(datetime.utcnow() - self._created_at),
        }


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Demonstrate the Compliance Audit Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    print("=" * 70)
    print("  Compliance Audit Agent v2.0 - Demonstration")
    print("=" * 70)

    agent = ComplianceAuditAgent({"user": "demo_user"})

    # List frameworks
    print("\n--- Available Frameworks ---")
    frameworks = agent.list_frameworks()
    for fw, info in frameworks.items():
        print(f"  {fw}: {info['controls_count']} controls")

    # Compliance assessment
    print("\n--- Compliance Assessment (SOC2) ---")
    assessment = agent.assess_compliance("SOC2", organization="Acme Corp")
    print(f"Status: {assessment['overall_status']}")
    print(f"Compliance rate: {assessment['compliance_rate']}")
    print(f"Gaps: {len(assessment['gaps'])}")

    # Policy management
    print("\n--- Policy Management ---")
    policy_result = agent.review_policy(
        policy_title="Information Security Policy",
        category="information_security",
        owner="CISO",
        frameworks=["SOC2", "ISO27001"],
    )
    print(f"Policy: {policy_result.get('title', 'N/A')}")
    print(f"Status: {policy_result.get('status', 'N/A')}")

    # Audit preparation
    print("\n--- Audit Preparation ---")
    audit = agent.prepare_audit(
        title="Annual SOC2 Type 2 Audit",
        framework="SOC2",
        audit_type="external",
        lead_auditor="Jane Smith",
        systems=["Production", "Staging", "Development"],
        departments=["Engineering", "Security", "Operations"],
    )
    print(f"Audit ID: {audit['audit_id']}")
    print(f"Controls in scope: {audit['controls_in_scope']}")
    print(f"Status: {audit['status']}")

    # Risk assessment
    print("\n--- Risk Assessment ---")
    risk1 = agent.record_risk(
        asset="Customer Database",
        threat="Data Breach",
        vulnerability="SQL Injection",
        likelihood=0.4,
        impact=0.9,
        mitigation="WAF + Parameterized Queries",
        owner="Security Team",
    )
    risk2 = agent.record_risk(
        asset="Internal Network",
        threat="Ransomware",
        vulnerability="Outdated Patches",
        likelihood=0.3,
        impact=0.8,
        owner="IT Operations",
    )
    print(f"Risk 1: {risk1['risk_level']} (score: {risk1['risk_score']})")
    print(f"Risk 2: {risk2['risk_level']} (score: {risk2['risk_score']})")

    # Risk summary
    risk_summary = agent._risk_engine.risk_summary()
    print(f"Total risks: {risk_summary['total_risks']}")
    print(f"By level: {risk_summary['by_level']}")

    # Evidence collection
    print("\n--- Evidence Collection ---")
    ev1 = agent.collect_evidence(
        name="Access Control Policy v2",
        evidence_type="policy",
        description="Current access control policy",
        control_ids=["CC6.1", "CC6.2"],
        collected_by="Auditor",
    )
    ev2 = agent.collect_evidence(
        name="Vulnerability Scan Report",
        evidence_type="vulnerability_report",
        description="Latest quarterly vulnerability scan",
        control_ids=["CC7.1"],
        collected_by="Security Team",
    )
    evidence_stats = agent._evidence_manager.get_stats()
    print(f"Total evidence: {evidence_stats['total']}")
    print(f"Verified: {evidence_stats['verified']}")

    # Remediation tracking
    print("\n--- Remediation Tracking ---")
    finding = Finding(
        title="Unencrypted data at rest",
        description="Customer data not encrypted in backup storage",
        severity=Severity.HIGH,
        framework=ComplianceFramework.SOC2,
        remediation_status=RemediationStatus.OPEN,
    )
    finding_id = agent._remediation_tracker.add_finding(finding)
    agent._remediation_tracker.assign_remediation(
        finding_id=finding_id,
        owner="Infrastructure Team",
        deadline_days=14,
        plan="Enable encryption at rest for all backup volumes",
    )
    progress = agent._remediation_tracker.get_progress_report()
    print(f"Total findings: {progress['total']}")
    print(f"Completion rate: {progress['completion_rate']}")
    print(f"Overdue: {progress['overdue_count']}")

    # Compliance dashboard
    print("\n--- Compliance Dashboard ---")
    dashboard = agent.get_compliance_dashboard()
    print(f"Frameworks: {dashboard['frameworks_available']}")
    print(f"Audits: {dashboard['audits']['total']}")
    print(f"Risks: {dashboard['risks']['total_risks']}")
    print(f"Remediation items: {dashboard['remediation']['total']}")
    print(f"Evidence items: {dashboard['evidence']['total']}")
    print(f"Policies: {dashboard['policies']['total']}")

    # Agent status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 70)
    print("  Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
