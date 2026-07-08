"""
Legal Agent - Legal Operations, Contract Management, and Compliance Platform.

End-to-end legal operations covering contract lifecycle management, compliance
monitoring, intellectual property protection, regulatory analysis, risk
assessment, and legal document automation. Built for corporate legal departments,
startups building legal infrastructure, and organizations navigating complex
regulatory environments across GDPR, CCPA, SOC2, HIPAA, and industry-specific
regulations.

Key Capabilities:
- Contract Lifecycle: Drafting, negotiation tracking, execution, renewal management
- Compliance Monitoring: Regulation tracking, audit preparation, gap analysis
- IP Protection: Trademark monitoring, patent portfolio, copyright management
- Risk Assessment: Legal risk scoring, regulatory impact analysis, exposure mapping
- Document Automation: Template generation, clause libraries, version control
- Regulatory Analysis: Multi-jurisdiction tracking, policy change monitoring
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib
import uuid
import re
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ContractStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    NEGOTIATION = "negotiation"
    APPROVED = "approved"
    EXECUTED = "executed"
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    RENEWED = "renewed"
    DISPUTED = "disputed"


class ContractType(Enum):
    NDA = "nda"
    SOW = "sow"
    EMPLOYMENT = "employment"
    VENDOR = "vendor"
    LICENSE = "license"
    LEASE = "lease"
    PARTNERSHIP = "partnership"
    SALES = "sales"
    SERVICE_LEVEL = "service_level"
    DATA_PROCESSING = "data_processing"
    CONSULTING = "consulting"
    NON_COMPETE = "non_compete"


class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"
    EXEMPT = "exempt"
    NOT_APPLICABLE = "not_applicable"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DocumentStatus(Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class TrademarkStatus(Enum):
    APPLICATION = "application"
    PENDING = "pending"
    REGISTERED = "registered"
    OPPOSED = "opposed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class RegulationCategory(Enum):
    DATA_PRIVACY = "data_privacy"
    FINANCIAL = "financial"
    ENVIRONMENTAL = "environmental"
    LABOR = "labor"
    HEALTH = "health"
    SECURITY = "security"
    CONSUMER = "consumer"
    ANTI_TRUST = "anti_trust"
    EXPORT_CONTROL = "export_control"
    INDUSTRY_SPECIFIC = "industry_specific"


class AuditStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    FINDINGS = "findings"
    REMEDIATION = "remediation"
    CLOSED = "closed"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Contract:
    """A legal contract."""
    contract_id: str
    title: str
    contract_type: ContractType
    parties: List[str]
    status: ContractStatus = ContractStatus.DRAFT
    effective_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    renewal_date: Optional[datetime] = None
    auto_renew: bool = True
    notice_period_days: int = 30
    value: float = 0.0
    currency: str = "USD"
    terms: Dict[str, Any] = field(default_factory=dict)
    clauses: List[Dict[str, Any]] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)
    signers: List[Dict[str, Any]] = field(default_factory=list)
    renewal_terms: Dict[str, Any] = field(default_factory=dict)
    governing_law: str = ""
    dispute_resolution: str = ""
    confidentiality_level: str = "confidential"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceRegulation:
    """A compliance regulation or standard."""
    regulation_id: str
    name: str
    category: RegulationCategory
    jurisdiction: str
    description: str = ""
    status: ComplianceStatus = ComplianceStatus.UNDER_REVIEW
    requirements: List[Dict[str, Any]] = field(default_factory=list)
    effective_date: Optional[datetime] = None
    last_audit_date: Optional[datetime] = None
    next_audit_date: Optional[datetime] = None
    compliance_score: float = 0.0
    gaps: List[Dict[str, Any]] = field(default_factory=list)
    remediation_plan: List[Dict[str, Any]] = field(default_factory=list)
    responsible_party: str = ""
    documentation_url: str = ""
    penalties: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceRequirement:
    """A specific requirement within a regulation."""
    requirement_id: str
    regulation_id: str
    title: str
    description: str
    is_mandatory: bool = True
    status: ComplianceStatus = ComplianceStatus.UNDER_REVIEW
    evidence_required: List[str] = field(default_factory=list)
    evidence_collected: List[str] = field(default_factory=list)
    responsible_party: str = ""
    due_date: Optional[datetime] = None
    priority: RiskLevel = RiskLevel.MEDIUM
    controls: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Trademark:
    """A trademark registration."""
    trademark_id: str
    name: str
    owner: str
    jurisdiction: str
    status: TrademarkStatus = TrademarkStatus.APPLICATION
    registration_number: str = ""
    filing_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    nice_classes: List[int] = field(default_factory=list)
    goods_services: List[str] = field(default_factory=list)
    opposition_deadline: Optional[datetime] = None
    renewal_dates: List[datetime] = field(default_factory=list)
    monitoring_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LegalRisk:
    """A legal risk assessment."""
    risk_id: str
    title: str
    description: str
    category: str
    risk_level: RiskLevel
    probability: float = 0.0
    impact_score: float = 0.0
    risk_score: float = 0.0
    affected_contracts: List[str] = field(default_factory=list)
    affected_regulations: List[str] = field(default_factory=list)
    mitigation_strategies: List[str] = field(default_factory=list)
    owner: str = ""
    identified_date: datetime = field(default_factory=datetime.now)
    last_reviewed: Optional[datetime] = None
    status: str = "open"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LegalDocument:
    """A legal document or template."""
    document_id: str
    title: str
    document_type: str
    status: DocumentStatus = DocumentStatus.DRAFT
    version: str = "1.0"
    content_hash: str = ""
    author: str = ""
    reviewers: List[str] = field(default_factory=list)
    approvers: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    template_id: str = ""
    parent_document: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditRecord:
    """A compliance audit record."""
    audit_id: str
    regulation_id: str
    audit_type: str
    status: AuditStatus = AuditStatus.PLANNED
    auditor: str = ""
    scope: str = ""
    findings: List[Dict[str, Any]] = field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    overall_score: float = 0.0
    next_audit_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ClauseLibrary:
    """A library of standard contract clauses."""
    clause_id: str
    title: str
    category: str
    content: str
    risk_level: RiskLevel = RiskLevel.LOW
    jurisdiction: str = "global"
    version: str = "1.0"
    is_default: bool = False
    alternative_clauses: List[str] = field(default_factory=list)
    legal_notes: str = ""
    last_reviewed: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Contract Manager
# ---------------------------------------------------------------------------

class ContractManager:
    """Manages the full contract lifecycle."""

    def __init__(self) -> None:
        self.contracts: Dict[str, Contract] = {}
        self.clause_library: Dict[str, ClauseLibrary] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}

    def create_contract(self, title: str, contract_type: ContractType,
                        parties: List[str], **kwargs: Any) -> Contract:
        contract_id = f"CON-{hashlib.md5(title.encode()).hexdigest()[:8].upper()}"
        contract = Contract(
            contract_id=contract_id,
            title=title,
            contract_type=contract_type,
            parties=parties,
            value=kwargs.get("value", 0),
            currency=kwargs.get("currency", "USD"),
            governing_law=kwargs.get("governing_law", ""),
            dispute_resolution=kwargs.get("dispute_resolution", ""),
            confidentiality_level=kwargs.get("confidentiality", "confidential"),
            terms=kwargs.get("terms", {}),
        )
        self.contracts[contract_id] = contract
        logger.info("Created contract: %s (%s)", title, contract_id)
        return contract

    def generate_nda(self, party_a: str, party_b: str, duration_years: int = 2,
                     jurisdiction: str = "US") -> Contract:
        nda = self.create_contract(
            title=f"NDA - {party_a} & {party_b}",
            contract_type=ContractType.NDA,
            parties=[party_a, party_b],
            governing_law=jurisdiction,
        )
        nda.terms = {
            "duration_years": duration_years,
            "confidential_scope": "all business information",
            "exceptions": "publicly available information",
            "survival_period": f"{duration_years} years post-termination",
            "remedies": "injunctive relief",
        }
        nda.clauses = [
            {"clause": "Definition of Confidential Information", "order": 1},
            {"clause": "Obligations of Receiving Party", "order": 2},
            {"clause": "Exclusions from Confidential Information", "order": 3},
            {"clause": "Term and Termination", "order": 4},
            {"clause": "Remedies", "order": 5},
            {"clause": "Governing Law", "order": 6},
        ]
        nda.status = ContractStatus.APPROVED
        return nda

    def advance_contract(self, contract_id: str) -> Dict[str, Any]:
        contract = self.contracts.get(contract_id)
        if not contract:
            return {"error": f"Contract {contract_id} not found"}

        transitions = {
            ContractStatus.DRAFT: ContractStatus.UNDER_REVIEW,
            ContractStatus.UNDER_REVIEW: ContractStatus.NEGOTIATION,
            ContractStatus.NEGOTIATION: ContractStatus.APPROVED,
            ContractStatus.APPROVED: ContractStatus.EXECUTED,
            ContractStatus.EXECUTED: ContractStatus.ACTIVE,
            ContractStatus.ACTIVE: ContractStatus.EXPIRED,
        }
        new_status = transitions.get(contract.status)
        if new_status:
            old = contract.status
            contract.status = new_status
            contract.updated_at = datetime.now()
            return {"contract_id": contract_id, "old_status": old.value, "new_status": new_status.value}
        return {"contract_id": contract_id, "status": contract.status.value, "no_transition": True}

    def check_renewals(self, within_days: int = 90) -> List[Dict[str, Any]]:
        cutoff = datetime.now() + timedelta(days=within_days)
        renewals = []
        for contract in self.contracts.values():
            if contract.status != ContractStatus.ACTIVE:
                continue
            renew_date = contract.renewal_date or contract.expiration_date
            if renew_date and renew_date <= cutoff:
                renewals.append({
                    "contract_id": contract.contract_id,
                    "title": contract.title,
                    "renewal_date": renew_date.isoformat(),
                    "auto_renew": contract.auto_renew,
                    "value": contract.value,
                    "notice_required": contract.notice_period_days,
                    "action_needed": not contract.auto_renew,
                })
        return sorted(renewals, key=lambda x: x["renewal_date"])

    def contract_summary(self, contract_id: str) -> Dict[str, Any]:
        contract = self.contracts.get(contract_id)
        if not contract:
            return {"error": f"Contract {contract_id} not found"}
        days_to_expiry = None
        if contract.expiration_date:
            days_to_expiry = (contract.expiration_date - datetime.now()).days
        return {
            "contract_id": contract.contract_id,
            "title": contract.title,
            "type": contract.contract_type.value,
            "status": contract.status.value,
            "parties": contract.parties,
            "value": contract.value,
            "currency": contract.currency,
            "effective_date": contract.effective_date.isoformat() if contract.effective_date else None,
            "expiration_date": contract.expiration_date.isoformat() if contract.expiration_date else None,
            "days_to_expiry": days_to_expiry,
            "auto_renew": contract.auto_renew,
            "governing_law": contract.governing_law,
            "clauses_count": len(contract.clauses),
        }

    def get_portfolio(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        by_type: Dict[str, int] = defaultdict(int)
        total_value = 0.0
        expiring_30 = 0
        expiring_90 = 0
        now = datetime.now()
        for contract in self.contracts.values():
            by_status[contract.status.value] += 1
            by_type[contract.contract_type.value] += 1
            total_value += contract.value
            if contract.expiration_date:
                days = (contract.expiration_date - now).days
                if 0 < days <= 30:
                    expiring_30 += 1
                elif 0 < days <= 90:
                    expiring_90 += 1
        return {
            "total_contracts": len(self.contracts),
            "by_status": dict(by_status),
            "by_type": dict(by_type),
            "total_value": total_value,
            "expiring_30_days": expiring_30,
            "expiring_90_days": expiring_90,
            "auto_renew_count": sum(1 for c in self.contracts.values() if c.auto_renew),
        }

    def add_clause(self, title: str, category: str, content: str,
                   risk_level: RiskLevel = RiskLevel.LOW,
                   jurisdiction: str = "global") -> ClauseLibrary:
        clause_id = f"CLA-{hashlib.md5(title.encode()).hexdigest()[:8].upper()}"
        clause = ClauseLibrary(
            clause_id=clause_id,
            title=title,
            category=category,
            content=content,
            risk_level=risk_level,
            jurisdiction=jurisdiction,
        )
        self.clause_library[clause_id] = clause
        return clause

    def search_clauses(self, category: str = "", jurisdiction: str = "",
                       max_risk: RiskLevel = RiskLevel.HIGH) -> List[Dict[str, Any]]:
        risk_order = {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2, RiskLevel.CRITICAL: 3}
        results = []
        for clause in self.clause_library.values():
            if category and clause.category != category:
                continue
            if jurisdiction and clause.jurisdiction not in (jurisdiction, "global"):
                continue
            if risk_order.get(clause.risk_level, 0) > risk_order.get(max_risk, 2):
                continue
            results.append({
                "clause_id": clause.clause_id,
                "title": clause.title,
                "category": clause.category,
                "risk_level": clause.risk_level.value,
                "jurisdiction": clause.jurisdiction,
                "is_default": clause.is_default,
            })
        return results


# ---------------------------------------------------------------------------
# Compliance Manager
# ---------------------------------------------------------------------------

class ComplianceManager:
    """Manages regulatory compliance tracking and audit workflows."""

    def __init__(self) -> None:
        self.regulations: Dict[str, ComplianceRegulation] = {}
        self.requirements: Dict[str, ComplianceRequirement] = {}
        self.audits: Dict[str, AuditRecord] = {}
        self.policy_documents: Dict[str, LegalDocument] = {}

    def register_regulation(self, name: str, category: RegulationCategory,
                            jurisdiction: str, **kwargs: Any) -> ComplianceRegulation:
        reg_id = f"REG-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        regulation = ComplianceRegulation(
            regulation_id=reg_id,
            name=name,
            category=category,
            jurisdiction=jurisdiction,
            description=kwargs.get("description", ""),
            effective_date=kwargs.get("effective_date"),
            responsible_party=kwargs.get("responsible_party", ""),
            penalties=kwargs.get("penalties", {}),
        )
        self.regulations[reg_id] = regulation
        return regulation

    def add_requirement(self, regulation_id: str, title: str, description: str,
                        is_mandatory: bool = True, **kwargs: Any) -> ComplianceRequirement:
        reg = self.regulations.get(regulation_id)
        if not reg:
            return ComplianceRequirement(requirement_id="error", regulation_id=regulation_id, title=title, description=description)
        req_id = f"REQ-{hashlib.md5(title.encode()).hexdigest()[:8].upper()}"
        requirement = ComplianceRequirement(
            requirement_id=req_id,
            regulation_id=regulation_id,
            title=title,
            description=description,
            is_mandatory=is_mandatory,
            evidence_required=kwargs.get("evidence", []),
            responsible_party=kwargs.get("responsible_party", ""),
            due_date=kwargs.get("due_date"),
            priority=kwargs.get("priority", RiskLevel.MEDIUM),
        )
        self.requirements[req_id] = requirement
        reg.requirements.append({"requirement_id": req_id, "title": title})
        return requirement

    def assess_compliance(self, regulation_id: str) -> Dict[str, Any]:
        reg = self.regulations.get(regulation_id)
        if not reg:
            return {"error": f"Regulation {regulation_id} not found"}
        reqs = [r for r in self.requirements.values() if r.regulation_id == regulation_id]
        total = len(reqs)
        compliant = sum(1 for r in reqs if r.status == ComplianceStatus.COMPLIANT)
        partial = sum(1 for r in reqs if r.status == ComplianceStatus.PARTIALLY_COMPLIANT)
        non_compliant = sum(1 for r in reqs if r.status == ComplianceStatus.NON_COMPLIANT)
        under_review = sum(1 for r in reqs if r.status == ComplianceStatus.UNDER_REVIEW)
        score = (compliant * 100 + partial * 50) / max(1, total)
        reg.compliance_score = round(score, 1)
        return {
            "regulation_id": regulation_id,
            "name": reg.name,
            "jurisdiction": reg.jurisdiction,
            "total_requirements": total,
            "compliant": compliant,
            "partially_compliant": partial,
            "non_compliant": non_compliant,
            "under_review": under_review,
            "compliance_score": round(score, 1),
            "status": reg.status.value,
        }

    def run_audit(self, regulation_id: str, auditor: str,
                  scope: str = "full") -> AuditRecord:
        audit_id = f"AUD-{uuid.uuid4().hex[:8].upper()}"
        audit = AuditRecord(
            audit_id=audit_id,
            regulation_id=regulation_id,
            audit_type=scope,
            auditor=auditor,
            status=AuditStatus.IN_PROGRESS,
            start_date=datetime.now(),
        )
        self.audits[audit_id] = audit
        return audit

    def close_audit(self, audit_id: str, findings: List[Dict[str, Any]],
                    score: float) -> Dict[str, Any]:
        audit = self.audits.get(audit_id)
        if not audit:
            return {"error": f"Audit {audit_id} not found"}
        audit.findings = findings
        audit.overall_score = score
        audit.status = AuditStatus.FINDINGS
        audit.end_date = datetime.now()
        critical = sum(1 for f in findings if f.get("severity") == "critical")
        high = sum(1 for f in findings if f.get("severity") == "high")
        return {
            "audit_id": audit_id,
            "findings_count": len(findings),
            "critical_findings": critical,
            "high_findings": high,
            "overall_score": score,
            "status": audit.status.value,
        }

    def gap_analysis(self, regulation_id: str) -> Dict[str, Any]:
        reg = self.regulations.get(regulation_id)
        if not reg:
            return {"error": f"Regulation {regulation_id} not found"}
        reqs = [r for r in self.requirements.values() if r.regulation_id == regulation_id]
        gaps = []
        for req in reqs:
            if req.status in (ComplianceStatus.NON_COMPLIANT, ComplianceStatus.PARTIALLY_COMPLIANT):
                missing_evidence = [
                    e for e in req.evidence_required
                    if e not in req.evidence_collected
                ]
                gaps.append({
                    "requirement_id": req.requirement_id,
                    "title": req.title,
                    "status": req.status.value,
                    "missing_evidence": missing_evidence,
                    "priority": req.priority.value,
                    "due_date": req.due_date.isoformat() if req.due_date else None,
                })
        return {
            "regulation_id": regulation_id,
            "name": reg.name,
            "total_gaps": len(gaps),
            "gaps": gaps,
            "remediation_priority": sorted(gaps, key=lambda x: x["priority"], reverse=True),
        }

    def get_compliance_overview(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        for reg in self.regulations.values():
            by_status[reg.status.value] += 1
        avg_score = (
            sum(r.compliance_score for r in self.regulations.values())
            / max(1, len(self.regulations))
        )
        upcoming_audits = [
            {
                "regulation": reg.name,
                "next_audit": reg.next_audit_date.isoformat() if reg.next_audit_date else None,
            }
            for reg in self.regulations.values()
            if reg.next_audit_date and reg.next_audit_date > datetime.now()
        ]
        return {
            "total_regulations": len(self.regulations),
            "by_status": dict(by_status),
            "avg_compliance_score": round(avg_score, 1),
            "total_requirements": len(self.requirements),
            "total_audits": len(self.audits),
            "upcoming_audits": upcoming_audits,
        }


# ---------------------------------------------------------------------------
# IP Protection Manager
# ---------------------------------------------------------------------------

class IPProtectionManager:
    """Manages trademarks, copyrights, and IP portfolio protection."""

    def __init__(self) -> None:
        self.trademarks: Dict[str, Trademark] = {}
        self.monitoring_alerts: List[Dict[str, Any]] = []

    def register_trademark(self, name: str, owner: str, jurisdiction: str,
                           **kwargs: Any) -> Trademark:
        tm_id = f"TM-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        trademark = Trademark(
            trademark_id=tm_id,
            name=name,
            owner=owner,
            jurisdiction=jurisdiction,
            nice_classes=kwargs.get("nice_classes", []),
            goods_services=kwargs.get("goods_services", []),
        )
        self.trademarks[tm_id] = trademark
        return trademark

    def update_trademark_status(self, trademark_id: str,
                                 new_status: TrademarkStatus,
                                 **kwargs: Any) -> Dict[str, Any]:
        tm = self.trademarks.get(trademark_id)
        if not tm:
            return {"error": f"Trademark {trademark_id} not found"}
        old = tm.status
        tm.status = new_status
        if new_status == TrademarkStatus.REGISTERED:
            tm.registration_date = datetime.now()
            tm.expiration_date = datetime.now() + timedelta(days=365 * 10)
        if kwargs.get("registration_number"):
            tm.registration_number = kwargs["registration_number"]
        return {"trademark_id": trademark_id, "old_status": old.value, "new_status": new_status.value}

    def check_expirations(self, within_days: int = 180) -> List[Dict[str, Any]]:
        cutoff = datetime.now() + timedelta(days=within_days)
        expiring = []
        for tm in self.trademarks.values():
            if tm.expiration_date and tm.expiration_date <= cutoff:
                expiring.append({
                    "trademark_id": tm.trademark_id,
                    "name": tm.name,
                    "jurisdiction": tm.jurisdiction,
                    "expiration_date": tm.expiration_date.isoformat(),
                    "days_remaining": (tm.expiration_date - datetime.now()).days,
                })
        return sorted(expiring, key=lambda x: x["days_remaining"])

    def get_ip_portfolio(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        by_jurisdiction: Dict[str, int] = defaultdict(int)
        for tm in self.trademarks.values():
            by_status[tm.status.value] += 1
            by_jurisdiction[tm.jurisdiction] += 1
        return {
            "total_trademarks": len(self.trademarks),
            "by_status": dict(by_status),
            "by_jurisdiction": dict(by_jurisdiction),
            "expiring_6_months": len(self.check_expirations(180)),
            "monitoring_alerts": len(self.monitoring_alerts),
        }


# ---------------------------------------------------------------------------
# Risk Assessment Engine
# ---------------------------------------------------------------------------

class LegalRiskEngine:
    """Assesses and tracks legal risks."""

    def __init__(self) -> None:
        self.risks: Dict[str, LegalRisk] = {}

    def identify_risk(self, title: str, description: str, category: str,
                      risk_level: RiskLevel, probability: float = 0.5,
                      impact: float = 5.0, **kwargs: Any) -> LegalRisk:
        risk_id = f"RSK-{hashlib.md5(title.encode()).hexdigest()[:8].upper()}"
        risk_score = probability * impact
        risk = LegalRisk(
            risk_id=risk_id,
            title=title,
            description=description,
            category=category,
            risk_level=risk_level,
            probability=probability,
            impact_score=impact,
            risk_score=round(risk_score, 2),
            affected_contracts=kwargs.get("contracts", []),
            affected_regulations=kwargs.get("regulations", []),
            mitigation_strategies=kwargs.get("mitigations", []),
            owner=kwargs.get("owner", ""),
        )
        self.risks[risk_id] = risk
        return risk

    def update_risk(self, risk_id: str, **kwargs: Any) -> Dict[str, Any]:
        risk = self.risks.get(risk_id)
        if not risk:
            return {"error": f"Risk {risk_id} not found"}
        if "risk_level" in kwargs:
            risk.risk_level = kwargs["risk_level"]
        if "status" in kwargs:
            risk.status = kwargs["status"]
        if "probability" in kwargs:
            risk.probability = kwargs["probability"]
            risk.risk_score = round(risk.probability * risk.impact_score, 2)
        if "mitigations" in kwargs:
            risk.mitigation_strategies = kwargs["mitigations"]
        risk.last_reviewed = datetime.now()
        return {"risk_id": risk_id, "updated_fields": list(kwargs.keys())}

    def get_risk_register(self) -> Dict[str, Any]:
        by_level: Dict[str, List[Dict]] = defaultdict(list)
        for risk in self.risks.values():
            by_level[risk.risk_level.value].append({
                "risk_id": risk.risk_id,
                "title": risk.title,
                "score": risk.risk_score,
                "status": risk.status,
            })
        return {
            "total_risks": len(self.risks),
            "by_level": {k: len(v) for k, v in by_level.items()},
            "critical_risks": by_level.get("critical", []),
            "high_risks": by_level.get("high", []),
            "average_score": round(
                sum(r.risk_score for r in self.risks.values()) / max(1, len(self.risks)), 2
            ),
        }


# ---------------------------------------------------------------------------
# Document Automation Engine
# ---------------------------------------------------------------------------

class DocumentAutomationEngine:
    """Automates legal document generation and template management."""

    def __init__(self) -> None:
        self.documents: Dict[str, LegalDocument] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}

    def register_template(self, name: str, template_type: str,
                          content_template: str, variables: List[str]) -> Dict[str, Any]:
        template_id = f"TPL-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        self.templates[template_id] = {
            "template_id": template_id,
            "name": name,
            "type": template_type,
            "content": content_template,
            "variables": variables,
            "version": "1.0",
        }
        return self.templates[template_id]

    def generate_document(self, template_id: str, variables: Dict[str, str],
                          author: str = "") -> LegalDocument:
        template = self.templates.get(template_id)
        if not template:
            return LegalDocument(document_id="error", title="Not Found", document_type="unknown")

        content = template["content"]
        for var_name, var_value in variables.items():
            content = content.replace(f"{{{var_name}}}", var_value)

        doc_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
        doc = LegalDocument(
            document_id=doc_id,
            title=template["name"],
            document_type=template["type"],
            status=DocumentStatus.DRAFT,
            author=author,
            content_hash=hashlib.md5(content.encode()).hexdigest(),
            template_id=template_id,
        )
        self.documents[doc_id] = doc
        return doc

    def approve_document(self, document_id: str, approver: str) -> Dict[str, Any]:
        doc = self.documents.get(document_id)
        if not doc:
            return {"error": f"Document {document_id} not found"}
        doc.approvers.append(approver)
        if len(doc.approvers) >= 1:
            doc.status = DocumentStatus.APPROVED
        return {"document_id": document_id, "status": doc.status.value, "approver": approver}

    def get_document_inventory(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        by_type: Dict[str, int] = defaultdict(int)
        for doc in self.documents.values():
            by_status[doc.status.value] += 1
            by_type[doc.document_type] += 1
        return {
            "total_documents": len(self.documents),
            "total_templates": len(self.templates),
            "by_status": dict(by_status),
            "by_type": dict(by_type),
        }


# ---------------------------------------------------------------------------
# Legal Agent (Orchestrator)
# ---------------------------------------------------------------------------

class LegalAgent:
    """Orchestrates all legal operations components."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.contract_manager = ContractManager()
        self.compliance_manager = ComplianceManager()
        self.ip_manager = IPProtectionManager()
        self.risk_engine = LegalRiskEngine()
        self.doc_engine = DocumentAutomationEngine()
        self._initialized_at = datetime.now()
        logger.info("LegalAgent initialized")

    def get_dashboard(self) -> Dict[str, Any]:
        return {
            "contracts": self.contract_manager.get_portfolio(),
            "compliance": self.compliance_manager.get_compliance_overview(),
            "ip_portfolio": self.ip_manager.get_ip_portfolio(),
            "risks": self.risk_engine.get_risk_register(),
            "documents": self.doc_engine.get_document_inventory(),
            "uptime": str(datetime.now() - self._initialized_at),
        }


def _demo() -> None:
    agent = LegalAgent()

    nda = agent.contract_manager.generate_nda("Acme Corp", "Beta Inc", duration_years=2)
    print(f"NDA created: {nda.contract_id} -> {nda.status.value}")

    adv = agent.contract_manager.advance_contract(nda.contract_id)
    print(f"Advanced: {adv.get('new_status', adv.get('status'))}")

    reg = agent.compliance_manager.register_regulation(
        name="GDPR",
        category=RegulationCategory.DATA_PRIVACY,
        jurisdiction="EU",
        description="General Data Protection Regulation",
    )
    req = agent.compliance_manager.add_requirement(
        regulation_id=reg.regulation_id,
        title="Data Processing Agreement",
        description="Must have DPA with all data processors",
        evidence=["signed_dpa.pdf", "processor_list.xlsx"],
    )
    req.status = ComplianceStatus.COMPLIANT
    req.evidence_collected = ["signed_dpa.pdf", "processor_list.xlsx"]
    assessment = agent.compliance_manager.assess_compliance(reg.regulation_id)
    print(f"GDPR compliance: {assessment['compliance_score']}%")

    tm = agent.ip_manager.register_trademark("MyBrand", "Acme Corp", "US", nice_classes=[9, 42])
    agent.ip_manager.update_trademark_status(tm.trademark_id, TrademarkStatus.REGISTERED, registration_number="12345678")
    portfolio = agent.ip_manager.get_ip_portfolio()
    print(f"IP Portfolio: {portfolio['total_trademarks']} trademarks")

    risk = agent.risk_engine.identify_risk(
        title="Data Breach Liability",
        description="Potential liability from customer data breach",
        category="data_privacy",
        risk_level=RiskLevel.HIGH,
        probability=0.3,
        impact=8.0,
        mitigations=["Encryption at rest", "Incident response plan", "Cyber insurance"],
    )
    print(f"Risk identified: {risk.risk_id} (score: {risk.risk_score})")

    tpl = agent.doc_engine.register_template(
        name="Privacy Policy",
        template_type="policy",
        content_template="This Privacy Policy describes how {company} collects and uses personal data.",
        variables=["company"],
    )
    doc = agent.doc_engine.generate_document(tpl["template_id"], {"company": "Acme Corp"}, author="legal-team")
    agent.doc_engine.approve_document(doc.document_id, "legal-director")
    print(f"Document: {doc.document_id} -> {doc.status.value}")

    dashboard = agent.get_dashboard()
    print(f"\nDashboard: {json.dumps(dashboard, indent=2, default=str)}")


if __name__ == "__main__":
    _demo()
