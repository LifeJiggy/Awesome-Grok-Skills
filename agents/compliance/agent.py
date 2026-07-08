"""
Compliance Agent - Regulatory Compliance and Audit Automation.

Provides comprehensive regulatory compliance management, policy tracking,
audit trail generation, risk assessment, privacy management, and remediation
planning across multiple compliance frameworks including GDPR, HIPAA, SOC 2,
PCI DSS, and ISO 27001.
"""

from __future__ import annotations

import logging
import uuid
import json
import hashlib
import re
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Set, Union
from collections import defaultdict

logger = logging.getLogger(__name__)


# =============================================================================
# Enumerations
# =============================================================================

class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    GDPR = "gdpr"
    SOC2 = "soc2"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    ISO27001 = "iso27001"
    CCPA = "ccpa"
    SOX = "sox"
    NIST_800_53 = "nist_800_53"
    FISMA = "fisma"
    FedRAMP = "fedramp"


class RiskSeverity(Enum):
    """Risk severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceStatus(Enum):
    """Status of compliance requirements."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"


class AuditAction(Enum):
    """Types of audit actions."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    ACCESS = "access"
    EXPORT = "export"
    APPROVE = "approve"
    DENY = "deny"


class DataType(Enum):
    """Types of personal data for privacy management."""
    PERSONAL = "personal"
    SENSITIVE = "sensitive"
    HEALTH = "health"
    FINANCIAL = "financial"
    BIOMETRIC = "biometric"
    CHILDREN = "children"
    LOCATION = "location"
    BEHAVIORAL = "behavioral"


class RequestType(Enum):
    """GDPR data subject request types."""
    ACCESS = "access"
    DELETION = "deletion"
    RECTIFICATION = "rectification"
    PORTABILITY = "portability"
    RESTRICTION = "restriction"
    OBJECTION = "objection"


class FindingStatus(Enum):
    """Security finding statuses."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REMEDIATED = "remediated"
    ACCEPTED = "accepted"
    FALSE_POSITIVE = "false_positive"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ComplianceRequirement:
    """A single compliance requirement."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    framework: str = ""
    control_id: str = ""
    requirement: str = ""
    description: str = ""
    severity: RiskSeverity = RiskSeverity.HIGH
    status: ComplianceStatus = ComplianceStatus.NOT_STARTED
    evidence: List[str] = field(default_factory=list)
    owner: str = ""
    due_date: Optional[str] = None
    verified: bool = False
    last_checked: Optional[str] = None
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "framework": self.framework,
            "control_id": self.control_id,
            "requirement": self.requirement,
            "description": self.description,
            "severity": self.severity.value,
            "status": self.status.value,
            "evidence": self.evidence,
            "owner": self.owner,
            "due_date": self.due_date,
            "verified": self.verified,
            "last_checked": self.last_checked,
            "notes": self.notes,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class AuditLogEntry:
    """An audit trail log entry."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    action: str = ""
    actor: str = ""
    resource: str = ""
    resource_type: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: str = ""
    user_agent: str = ""
    session_id: str = ""
    outcome: str = "success"
    severity: str = "info"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "action": self.action,
            "actor": self.actor,
            "resource": self.resource,
            "resource_type": self.resource_type,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
            "outcome": self.outcome,
            "severity": self.severity,
        }


@dataclass
class DataSubject:
    """A data subject for privacy management."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    email: str = ""
    name: str = ""
    data_categories: List[str] = field(default_factory=list)
    consent_given: bool = False
    consent_purposes: List[str] = field(default_factory=list)
    consent_date: Optional[str] = None
    last_activity: Optional[str] = None
    data_retention_date: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "data_categories": self.data_categories,
            "consent_given": self.consent_given,
            "consent_purposes": self.consent_purposes,
            "consent_date": self.consent_date,
            "last_activity": self.last_activity,
            "data_retention_date": self.data_retention_date,
            "created_at": self.created_at,
        }


@dataclass
class SecurityFinding:
    """A security finding from an audit or scan."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    severity: RiskSeverity = RiskSeverity.MEDIUM
    status: FindingStatus = FindingStatus.OPEN
    category: str = ""
    cvss_score: float = 0.0
    cve_id: str = ""
    affected_resource: str = ""
    remediation: str = ""
    remediation_timeline: str = ""
    evidence: List[str] = field(default_factory=list)
    reported_by: str = ""
    scan_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "status": self.status.value,
            "category": self.category,
            "cvss_score": self.cvss_score,
            "cve_id": self.cve_id,
            "affected_resource": self.affected_resource,
            "remediation": self.remediation,
            "remediation_timeline": self.remediation_timeline,
            "evidence": self.evidence,
            "reported_by": self.reported_by,
            "scan_id": self.scan_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class RiskAssessment:
    """A risk assessment entry."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    asset: str = ""
    threat: str = ""
    vulnerability: str = ""
    likelihood: RiskSeverity = RiskSeverity.MEDIUM
    impact: RiskSeverity = RiskSeverity.MEDIUM
    risk_level: RiskSeverity = RiskSeverity.MEDIUM
    mitigation: str = ""
    owner: str = ""
    status: str = "open"
    review_date: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "asset": self.asset,
            "threat": self.threat,
            "vulnerability": self.vulnerability,
            "likelihood": self.likelihood.value,
            "impact": self.impact.value,
            "risk_level": self.risk_level.value,
            "mitigation": self.mitigation,
            "owner": self.owner,
            "status": self.status,
            "review_date": self.review_date,
            "created_at": self.created_at,
        }


@dataclass
class CompliancePolicy:
    """A compliance policy document."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    framework: str = ""
    version: str = "1.0"
    content: str = ""
    status: str = "draft"
    owner: str = ""
    approved_by: str = ""
    effective_date: Optional[str] = None"
    review_date: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "framework": self.framework,
            "version": self.version,
            "content": self.content,
            "status": self.status,
            "owner": self.owner,
            "approved_by": self.approved_by,
            "effective_date": self.effective_date,
            "review_date": self.review_date,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# =============================================================================
# Compliance Checker
# =============================================================================

class ComplianceChecker:
    """
    Checks compliance requirements against evidence and generates reports.

    Supports multiple frameworks and tracks compliance status per requirement.
    """

    def __init__(self) -> None:
        self._requirements: Dict[str, ComplianceRequirement] = {}
        self._by_framework: Dict[str, List[str]] = defaultdict(list)
        self._violations: List[str] = []
        self._checks_performed: int = 0

    def add_requirement(
        self,
        framework: str,
        control_id: str,
        requirement: str,
        description: str = "",
        severity: str = "high",
        owner: str = "",
    ) -> ComplianceRequirement:
        """Add a compliance requirement to track."""
        sev = RiskSeverity(severity) if severity in [e.value for e in RiskSeverity] else RiskSeverity.HIGH
        req = ComplianceRequirement(
            framework=framework,
            control_id=control_id,
            requirement=requirement,
            description=description,
            severity=sev,
            owner=owner,
        )
        self._requirements[req.id] = req
        self._by_framework[framework].append(req.id)
        logger.info("Compliance requirement added: %s/%s", framework, control_id)
        return req

    def check_requirement(
        self,
        requirement_id: str,
        evidence: Dict[str, Any],
        passed: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Check a single compliance requirement against evidence."""
        req = self._requirements.get(requirement_id)
        if not req:
            return {"error": f"Requirement {requirement_id} not found"}

        self._checks_performed += 1
        req.last_checked = datetime.utcnow().isoformat()
        req.evidence.append(json.dumps(evidence))

        if passed is not None:
            req.verified = passed
        else:
            req.verified = self._evaluate_evidence(req, evidence)

        if req.verified:
            req.status = ComplianceStatus.COMPLIANT
        else:
            req.status = ComplianceStatus.NON_COMPLIANT
            self._violations.append(requirement_id)

        req.updated_at = datetime.utcnow().isoformat()
        return {
            "requirement_id": requirement_id,
            "framework": req.framework,
            "control_id": req.control_id,
            "status": req.status.value,
            "verified": req.verified,
        }

    def bulk_check(
        self,
        framework: str,
        evidence_map: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Check multiple requirements for a framework."""
        results = []
        for req_id, evidence in evidence_map.items():
            result = self.check_requirement(req_id, evidence)
            results.append(result)

        passed = sum(1 for r in results if r.get("verified"))
        return {
            "framework": framework,
            "total_checked": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "results": results,
        }

    def generate_report(
        self,
        framework: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a compliance report."""
        if framework:
            req_ids = self._by_framework.get(framework, [])
            relevant = {rid: self._requirements[rid] for rid in req_ids if rid in self._requirements}
        else:
            relevant = dict(self._requirements)

        total = len(relevant)
        compliant = sum(1 for r in relevant.values() if r.status == ComplianceStatus.COMPLIANT)
        non_compliant = sum(1 for r in relevant.values() if r.status == ComplianceStatus.NON_COMPLIANT)
        in_progress = sum(1 for r in relevant.values() if r.status == ComplianceStatus.IN_PROGRESS)
        not_started = sum(1 for r in relevant.values() if r.status == ComplianceStatus.NOT_STARTED)

        score = (compliant / max(total, 1)) * 100

        by_severity: Dict[str, int] = defaultdict(int)
        for r in relevant.values():
            by_severity[r.severity.value] += 1

        return {
            "framework": framework or "all",
            "total_requirements": total,
            "compliant": compliant,
            "non_compliant": non_compliant,
            "in_progress": in_progress,
            "not_started": not_started,
            "compliance_score": round(score, 2),
            "violations": self._violations,
            "by_severity": dict(by_severity),
            "checks_performed": self._checks_performed,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_requirements(
        self,
        framework: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get requirements with optional filters."""
        reqs = list(self._requirements.values())
        if framework:
            reqs = [r for r in reqs if r.framework == framework]
        if status:
            reqs = [r for r in reqs if r.status.value == status]
        return [r.to_dict() for r in reqs]

    def _evaluate_evidence(
        self, req: ComplianceRequirement, evidence: Dict[str, Any]
    ) -> bool:
        """Evaluate whether evidence satisfies a requirement."""
        if req.framework == "gdpr":
            return evidence.get("data_consent", False)
        elif req.framework == "soc2":
            return len(evidence.get("audit_log", [])) > 0
        elif req.framework == "hipaa":
            return evidence.get("access_control", False)
        else:
            return evidence.get("compliant", True)


# =============================================================================
# Audit Logger
# =============================================================================

class AuditLogger:
    """
    Manages audit trail logs for compliance tracking.

    Provides logging, querying, and export capabilities for all
    system actions with full context tracking.
    """

    def __init__(self) -> None:
        self._logs: List[AuditLogEntry] = []
        self._by_actor: Dict[str, List[str]] = defaultdict(list)
        self._by_action: Dict[str, List[str]] = defaultdict(list)
        self._by_resource: Dict[str, List[str]] = defaultdict(list)

    def log(
        self,
        action: str,
        actor: str,
        resource: str,
        details: Optional[Dict[str, Any]] = None,
        resource_type: str = "",
        ip_address: str = "",
        user_agent: str = "",
        session_id: str = "",
        outcome: str = "success",
    ) -> AuditLogEntry:
        """Create an audit log entry."""
        entry = AuditLogEntry(
            action=action,
            actor=actor,
            resource=resource,
            resource_type=resource_type,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            outcome=outcome,
        )

        self._logs.append(entry)
        self._by_actor[actor].append(entry.id)
        self._by_action[action].append(entry.id)
        self._by_resource[resource].append(entry.id)

        return entry

    def query(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query audit logs with filters."""
        results = list(self._logs)

        if actor:
            results = [l for l in results if l.actor == actor]
        if action:
            results = [l for l in results if l.action == action]
        if resource:
            results = [l for l in results if resource in l.resource]
        if start_date:
            results = [l for l in results if l.timestamp >= start_date]
        if end_date:
            results = [l for l in results if l.timestamp <= end_date]

        results.sort(key=lambda l: l.timestamp, reverse=True)
        return [l.to_dict() for l in results[:limit]]

    def export_for_compliance(
        self,
        start_date: str,
        end_date: str,
        framework: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Export logs for compliance audit."""
        filtered = [
            l for l in self._logs
            if start_date <= l.timestamp <= end_date
        ]
        return [l.to_dict() for l in filtered]

    def get_statistics(self) -> Dict[str, Any]:
        """Get audit log statistics."""
        by_action = {k: len(v) for k, v in self._by_action.items()}
        by_actor = {k: len(v) for k, v in self._by_actor.items()}
        return {
            "total_entries": len(self._logs),
            "by_action": by_action,
            "by_actor": by_actor,
            "unique_actors": len(self._by_actor),
            "unique_resources": len(self._by_resource),
        }


# =============================================================================
# Privacy Manager
# =============================================================================

class PrivacyManager:
    """
    Manages data subject privacy requests and consent tracking.

    Handles GDPR data subject requests (access, deletion, portability,
    rectification) and maintains consent records.
    """

    def __init__(self) -> None:
        self._data_subjects: Dict[str, DataSubject] = {}
        self._consent_records: List[Dict[str, Any]] = []
        self._data_requests: List[Dict[str, Any]] = []

    def register_data_subject(
        self,
        email: str,
        name: str,
        data_categories: Optional[List[str]] = None,
    ) -> DataSubject:
        """Register a new data subject."""
        subject = DataSubject(
            email=email,
            name=name,
            data_categories=data_categories or [],
        )
        self._data_subjects[subject.id] = subject
        logger.info("Data subject registered: %s", email)
        return subject

    def record_consent(
        self,
        subject_id: str,
        purpose: str,
        granted: bool,
    ) -> Dict[str, Any]:
        """Record a consent decision."""
        subject = self._data_subjects.get(subject_id)
        if not subject:
            return {"error": "Data subject not found"}

        record = {
            "subject_id": subject_id,
            "purpose": purpose,
            "granted": granted,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._consent_records.append(record)

        if granted and purpose not in subject.consent_purposes:
            subject.consent_purposes.append(purpose)
        elif not granted and purpose in subject.consent_purposes:
            subject.consent_purposes.remove(purpose)

        subject.consent_given = len(subject.consent_purposes) > 0
        return record

    def handle_data_request(
        self,
        subject_id: str,
        request_type: str,
    ) -> Dict[str, Any]:
        """Handle a GDPR data subject request."""
        subject = self._data_subjects.get(subject_id)
        if not subject:
            return {"error": "Data subject not found"}

        req = RequestType(request_type) if request_type in [e.value for e in RequestType] else RequestType.ACCESS

        request_record = {
            "subject_id": subject_id,
            "request_type": req.value,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "processed",
        }
        self._data_requests.append(request_record)

        if req == RequestType.ACCESS:
            return {"data": subject.to_dict(), "format": "json"}
        elif req == RequestType.DELETION:
            del self._data_subjects[subject_id]
            return {"status": "deleted", "subject_id": subject_id}
        elif req == RequestType.PORTABILITY:
            return {"data": subject.to_dict(), "format": "json", "machine_readable": True}
        elif req == RequestType.RECTIFICATION:
            return {"status": "ready_for_update", "subject_id": subject_id}
        elif req == RequestType.RESTRICTION:
            return {"status": "processing_restricted", "subject_id": subject_id}
        elif req == RequestType.OBJECTION:
            return {"status": "processing_objection_noted", "subject_id": subject_id}

        return {"error": "Unknown request type"}

    def get_privacy_report(self) -> Dict[str, Any]:
        """Generate privacy management report."""
        total = len(self._data_subjects)
        consented = sum(1 for s in self._data_subjects.values() if s.consent_given)
        all_categories = set()
        for s in self._data_subjects.values():
            all_categories.update(s.data_categories)

        return {
            "total_data_subjects": total,
            "with_consent": consented,
            "consent_rate": round(consented / max(total, 1) * 100, 2),
            "data_categories": list(all_categories),
            "total_requests": len(self._data_requests),
            "consent_records": len(self._consent_records),
        }

    def get_data_subjects(self) -> List[Dict[str, Any]]:
        """Get all registered data subjects."""
        return [s.to_dict() for s in self._data_subjects.values()]


# =============================================================================
# Security Auditor
# =============================================================================

class SecurityAuditor:
    """
    Manages security scans, findings, and remediation tracking.

    Tracks vulnerabilities, their severity, status, and remediation progress.
    """

    def __init__(self) -> None:
        self._findings: List[SecurityFinding] = []
        self._scans: List[Dict[str, Any]] = []

    def run_scan(
        self,
        target: str,
        scan_type: str = "vulnerability",
    ) -> str:
        """Run a security scan."""
        scan_id = f"scan-{hashlib.md5((target + datetime.utcnow().isoformat()).encode()).hexdigest()[:8]}"
        self._scans.append({
            "id": scan_id,
            "target": target,
            "type": scan_type,
            "started_at": datetime.utcnow().isoformat(),
            "status": "completed",
        })
        return scan_id

    def add_finding(
        self,
        scan_id: str,
        title: str,
        severity: str = "medium",
        description: str = "",
        affected_resource: str = "",
        remediation: str = "",
        cvss_score: float = 0.0,
        cve_id: str = "",
    ) -> SecurityFinding:
        """Add a security finding."""
        sev = RiskSeverity(severity) if severity in [e.value for e in RiskSeverity] else RiskSeverity.MEDIUM

        finding = SecurityFinding(
            title=title,
            description=description,
            severity=sev,
            affected_resource=affected_resource,
            remediation=remediation,
            cvss_score=cvss_score,
            cve_id=cve_id,
            scan_id=scan_id,
        )
        self._findings.append(finding)
        return finding

    def update_finding_status(
        self,
        finding_id: str,
        status: str,
    ) -> Dict[str, Any]:
        """Update the status of a security finding."""
        finding = next((f for f in self._findings if f.id == finding_id), None)
        if not finding:
            return {"error": f"Finding {finding_id} not found"}

        new_status = FindingStatus(status) if status in [e.value for e in FindingStatus] else FindingStatus.OPEN
        finding.status = new_status
        finding.updated_at = datetime.utcnow().isoformat()
        return {"finding_id": finding_id, "status": new_status.value}

    def generate_security_report(
        self,
        days: int = 30,
    ) -> Dict[str, Any]:
        """Generate a security audit report."""
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        recent = [f for f in self._findings if f.created_at >= cutoff]

        by_severity: Dict[str, int] = defaultdict(int)
        by_status: Dict[str, int] = defaultdict(int)
        for f in recent:
            by_severity[f.severity.value] += 1
            by_status[f.status.value] += 1

        return {
            "period_days": days,
            "total_findings": len(recent),
            "by_severity": dict(by_severity),
            "by_status": dict(by_status),
            "critical_findings": [f.to_dict() for f in recent if f.severity == RiskSeverity.CRITICAL],
            "open_findings": by_status.get("open", 0),
            "remediated_findings": by_status.get("remediated", 0),
            "total_scans": len(self._scans),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_findings(
        self,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get findings with optional filters."""
        findings = list(self._findings)
        if severity:
            findings = [f for f in findings if f.severity.value == severity]
        if status:
            findings = [f for f in findings if f.status.value == status]
        return [f.to_dict() for f in findings]


# =============================================================================
# Risk Assessor
# =============================================================================

class RiskAssessor:
    """
    Conducts and manages risk assessments.

    Evaluates likelihood and impact to calculate risk levels
    and tracks mitigation progress.
    """

    SEVERITY_SCORES = {
        RiskSeverity.LOW: 1,
        RiskSeverity.MEDIUM: 2,
        RiskSeverity.HIGH: 3,
        RiskSeverity.CRITICAL: 4,
    }

    def __init__(self) -> None:
        self._assessments: Dict[str, RiskAssessment] = {}

    def create_assessment(
        self,
        asset: str,
        threat: str,
        vulnerability: str,
        likelihood: str = "medium",
        impact: str = "medium",
        mitigation: str = "",
        owner: str = "",
    ) -> RiskAssessment:
        """Create a new risk assessment."""
        lik = RiskSeverity(likelihood) if likelihood in [e.value for e in RiskSeverity] else RiskSeverity.MEDIUM
        imp = RiskSeverity(impact) if impact in [e.value for e in RiskSeverity] else RiskSeverity.MEDIUM

        risk_score = self.SEVERITY_SCORES[lik] * self.SEVERITY_SCORES[imp]
        if risk_score >= 12:
            risk_level = RiskSeverity.CRITICAL
        elif risk_score >= 8:
            risk_level = RiskSeverity.HIGH
        elif risk_score >= 4:
            risk_level = RiskSeverity.MEDIUM
        else:
            risk_level = RiskSeverity.LOW

        assessment = RiskAssessment(
            asset=asset,
            threat=threat,
            vulnerability=vulnerability,
            likelihood=lik,
            impact=imp,
            risk_level=risk_level,
            mitigation=mitigation,
            owner=owner,
        )

        self._assessments[assessment.id] = assessment
        return assessment

    def get_risk_summary(self) -> Dict[str, Any]:
        """Get summary of all risk assessments."""
        by_level: Dict[str, int] = defaultdict(int)
        for a in self._assessments.values():
            by_level[a.risk_level.value] += 1

        return {
            "total_assessments": len(self._assessments),
            "by_risk_level": dict(by_level),
            "critical_risks": by_level.get("critical", 0),
            "high_risks": by_level.get("high", 0),
        }

    def get_assessments(
        self,
        risk_level: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get assessments with optional risk level filter."""
        assessments = list(self._assessments.values())
        if risk_level:
            assessments = [a for a in assessments if a.risk_level.value == risk_level]
        return [a.to_dict() for a in assessments]


# =============================================================================
# Policy Manager
# =============================================================================

class PolicyManager:
    """
    Manages compliance policies and documentation.

    Tracks policy versions, approval status, and review schedules.
    """

    def __init__(self) -> None:
        self._policies: Dict[str, CompliancePolicy] = {}

    def create_policy(
        self,
        title: str,
        framework: str,
        content: str = "",
        owner: str = "",
    ) -> CompliancePolicy:
        """Create a new compliance policy."""
        policy = CompliancePolicy(
            title=title,
            framework=framework,
            content=content,
            owner=owner,
        )
        self._policies[policy.id] = policy
        return policy

    def approve_policy(
        self,
        policy_id: str,
        approved_by: str,
    ) -> Dict[str, Any]:
        """Approve a policy."""
        policy = self._policies.get(policy_id)
        if not policy:
            return {"error": f"Policy {policy_id} not found"}

        policy.status = "approved"
        policy.approved_by = approved_by
        policy.effective_date = datetime.utcnow().isoformat()
        policy.updated_at = datetime.utcnow().isoformat()
        return {"policy_id": policy_id, "status": "approved"}

    def get_policies(
        self,
        framework: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get policies with optional framework filter."""
        policies = list(self._policies.values())
        if framework:
            policies = [p for p in policies if p.framework == framework]
        return [p.to_dict() for p in policies]

    def get_policy_summary(self) -> Dict[str, Any]:
        """Get policy management summary."""
        by_status: Dict[str, int] = defaultdict(int)
        by_framework: Dict[str, int] = defaultdict(int)
        for p in self._policies.values():
            by_status[p.status] += 1
            by_framework[p.framework] += 1

        return {
            "total_policies": len(self._policies),
            "by_status": dict(by_status),
            "by_framework": dict(by_framework),
        }


# =============================================================================
# Main Compliance Agent
# =============================================================================

class ComplianceAgent:
    """
    Primary orchestrator for regulatory compliance and audit automation.

    Coordinates compliance checking, audit logging, privacy management,
    security auditing, risk assessment, and policy management into a
    unified compliance workflow.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._checker = ComplianceChecker()
        self._audit_logger = AuditLogger()
        self._privacy_manager = PrivacyManager()
        self._security_auditor = SecurityAuditor()
        self._risk_assessor = RiskAssessor()
        self._policy_manager = PolicyManager()
        self._created_at = datetime.utcnow()

        logger.info("ComplianceAgent initialized")

    def add_requirement(
        self,
        framework: str,
        control_id: str,
        requirement: str,
        description: str = "",
        severity: str = "high",
        owner: str = "",
    ) -> Dict[str, Any]:
        """Add a compliance requirement."""
        req = self._checker.add_requirement(
            framework=framework,
            control_id=control_id,
            requirement=requirement,
            description=description,
            severity=severity,
            owner=owner,
        )
        self._audit_logger.log(
            action="create_requirement",
            actor="system",
            resource=f"requirement:{req.id}",
            details={"framework": framework, "control_id": control_id},
        )
        return req.to_dict()

    def check_compliance(
        self,
        requirement_id: str,
        evidence: Dict[str, Any],
        passed: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Check a compliance requirement."""
        result = self._checker.check_requirement(requirement_id, evidence, passed)
        self._audit_logger.log(
            action="check_compliance",
            actor="system",
            resource=f"requirement:{requirement_id}",
            details=result,
        )
        return result

    def generate_compliance_report(
        self,
        framework: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a compliance report."""
        return self._checker.generate_report(framework)

    def log_audit_event(
        self,
        action: str,
        actor: str,
        resource: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Log an audit event."""
        entry = self._audit_logger.log(
            action=action,
            actor=actor,
            resource=resource,
            details=details,
        )
        return entry.to_dict()

    def query_audit_logs(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Query audit logs."""
        return self._audit_logger.query(actor=actor, action=action, resource=resource)

    def register_data_subject(
        self,
        email: str,
        name: str,
        data_categories: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Register a data subject."""
        subject = self._privacy_manager.register_data_subject(email, name, data_categories)
        return subject.to_dict()

    def record_consent(
        self,
        subject_id: str,
        purpose: str,
        granted: bool,
    ) -> Dict[str, Any]:
        """Record consent for a data subject."""
        return self._privacy_manager.record_consent(subject_id, purpose, granted)

    def handle_data_request(
        self,
        subject_id: str,
        request_type: str,
    ) -> Dict[str, Any]:
        """Handle a GDPR data subject request."""
        result = self._privacy_manager.handle_data_request(subject_id, request_type)
        self._audit_logger.log(
            action=f"data_request_{request_type}",
            actor="data_subject",
            resource=f"subject:{subject_id}",
            details=result,
        )
        return result

    def get_privacy_report(self) -> Dict[str, Any]:
        """Get privacy management report."""
        return self._privacy_manager.get_privacy_report()

    def run_security_scan(
        self,
        target: str,
        scan_type: str = "vulnerability",
    ) -> Dict[str, Any]:
        """Run a security scan."""
        scan_id = self._security_auditor.run_scan(target, scan_type)
        return {"scan_id": scan_id, "target": target, "status": "completed"}

    def add_security_finding(
        self,
        scan_id: str,
        title: str,
        severity: str = "medium",
        description: str = "",
    ) -> Dict[str, Any]:
        """Add a security finding."""
        finding = self._security_auditor.add_finding(
            scan_id=scan_id,
            title=title,
            severity=severity,
            description=description,
        )
        return finding.to_dict()

    def get_security_report(self, days: int = 30) -> Dict[str, Any]:
        """Get security audit report."""
        return self._security_auditor.generate_security_report(days)

    def create_risk_assessment(
        self,
        asset: str,
        threat: str,
        vulnerability: str,
        likelihood: str = "medium",
        impact: str = "medium",
        mitigation: str = "",
    ) -> Dict[str, Any]:
        """Create a risk assessment."""
        assessment = self._risk_assessor.create_assessment(
            asset=asset,
            threat=threat,
            vulnerability=vulnerability,
            likelihood=likelihood,
            impact=impact,
            mitigation=mitigation,
        )
        return assessment.to_dict()

    def get_risk_summary(self) -> Dict[str, Any]:
        """Get risk assessment summary."""
        return self._risk_assessor.get_risk_summary()

    def create_policy(
        self,
        title: str,
        framework: str,
        content: str = "",
        owner: str = "",
    ) -> Dict[str, Any]:
        """Create a compliance policy."""
        policy = self._policy_manager.create_policy(title, framework, content, owner)
        return policy.to_dict()

    def approve_policy(self, policy_id: str, approved_by: str) -> Dict[str, Any]:
        """Approve a policy."""
        return self._policy_manager.approve_policy(policy_id, approved_by)

    def get_policy_summary(self) -> Dict[str, Any]:
        """Get policy management summary."""
        return self._policy_manager.get_policy_summary()

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": "ComplianceAgent",
            "version": "2.0.0",
            "frameworks_tracked": len(set(
                r.framework for r in self._checker._requirements.values()
            )),
            "total_requirements": len(self._checker._requirements),
            "audit_logs": len(self._audit_logger._logs),
            "data_subjects": len(self._privacy_manager._data_subjects),
            "security_findings": len(self._security_auditor._findings),
            "risk_assessments": len(self._risk_assessor._assessments),
            "policies": len(self._policy_manager._policies),
            "uptime": str(datetime.utcnow() - self._created_at),
        }


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Demonstrate the Compliance Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    print("=" * 70)
    print("  Compliance Agent v2.0 - Demonstration")
    print("=" * 70)

    agent = ComplianceAgent()

    # Add GDPR requirements
    print("\n--- Adding GDPR Requirements ---")
    req1 = agent.add_requirement(
        framework="gdpr",
        control_id="GDPR-001",
        requirement="Data Consent",
        description="Ensure explicit consent for data processing",
        severity="high",
    )
    print(f"Added: {req1['control_id']} - {req1['requirement']}")

    req2 = agent.add_requirement(
        framework="gdpr",
        control_id="GDPR-002",
        requirement="Data Retention",
        description="Define and enforce data retention periods",
        severity="medium",
    )

    # Check compliance
    print("\n--- Checking Compliance ---")
    result1 = agent.check_compliance(req1["id"], {"data_consent": True})
    print(f"GDPR-001: {result1['status']}")

    result2 = agent.check_compliance(req2["id"], {"retention_policy": True})
    print(f"GDPR-002: {result2['status']}")

    # Generate compliance report
    print("\n--- Compliance Report ---")
    report = agent.generate_compliance_report("gdpr")
    print(f"Score: {report['compliance_score']}%")
    print(f"Compliant: {report['compliant']}, Non-compliant: {report['non_compliant']}")

    # Audit logging
    print("\n--- Audit Logging ---")
    agent.log_audit_event("CREATE", "admin@company.com", "user:123", {"action": "Created user"})
    agent.log_audit_event("ACCESS", "user@company.com", "document:456", {"action": "Read document"})
    logs = agent.query_audit_logs(action="CREATE")
    print(f"Audit logs: {len(logs)} entries")

    # Privacy management
    print("\n--- Privacy Management ---")
    subject = agent.register_data_subject("john@example.com", "John Doe", ["personal", "behavioral"])
    agent.record_consent(subject["id"], "marketing", True)
    agent.record_consent(subject["id"], "analytics", True)
    privacy_report = agent.get_privacy_report()
    print(f"Data subjects: {privacy_report['total_data_subjects']}")
    print(f"Consent rate: {privacy_report['consent_rate']}%")

    # Security audit
    print("\n--- Security Audit ---")
    scan = agent.run_security_scan("api.example.com", "vulnerability")
    agent.add_security_finding(scan["scan_id"], "SQL Injection", "critical", "Unparameterized query")
    agent.add_security_finding(scan["scan_id"], "XSS Vulnerability", "high", "Reflected XSS in search")
    security_report = agent.get_security_report()
    print(f"Findings: {security_report['total_findings']}")
    print(f"Critical: {security_report['by_severity'].get('critical', 0)}")

    # Risk assessment
    print("\n--- Risk Assessment ---")
    risk = agent.create_risk_assessment(
        asset="Customer Database",
        threat="Data Breach",
        vulnerability="Weak access controls",
        likelihood="medium",
        impact="critical",
        mitigation="Implement RBAC and encryption",
    )
    risk_summary = agent.get_risk_summary()
    print(f"Risk assessments: {risk_summary['total_assessments']}")
    print(f"Critical risks: {risk_summary['critical_risks']}")

    # Policy management
    print("\n--- Policy Management ---")
    policy = agent.create_policy(
        title="Data Protection Policy",
        framework="gdpr",
        content="All personal data must be processed lawfully...",
        owner="DPO",
    )
    agent.approve_policy(policy["id"], "CISO")
    policy_summary = agent.get_policy_summary()
    print(f"Policies: {policy_summary['total_policies']}")

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
