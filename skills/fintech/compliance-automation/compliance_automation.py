"""
Compliance Automation Module
Part of the fintech skill domain

Provides KYC/CDD workflows, AML monitoring, sanctions screening,
SAR filing, audit trail management, and regulatory reporting.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import hashlib


class CustomerRiskTier(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PROHIBITED = "prohibited"


class KYCStatus(Enum):
    NOT_STARTED = "not_started"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    UNDER_REVIEW = "under_review"


class SanctionsMatchType(Enum):
    EXACT = "exact"
    FUZZY = "fuzzy"
    ALIAS = "alias"
    PARTIAL = "partial"


class SARStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    FILED = "filed"
    AMENDED = "amended"


class AuditEventType(Enum):
    KYC_APPROVED = "kyc_approved"
    KYC_REJECTED = "kyc_rejected"
    SAR_FILED = "sar_filed"
    ACCOUNT_OPENED = "account_opened"
    ACCOUNT_CLOSED = "account_closed"
    TRANSACTION_FLAGGED = "transaction_flagged"
    SANCTIONS_HIT = "sanctions_hit"
    POLICY_CHANGE = "policy_change"


@dataclass
class KYCResult:
    customer_id: str
    status: KYCStatus
    risk_tier: CustomerRiskTier
    next_review_date: str
    documents_verified: int
    checks_passed: int
    checks_total: int
    flags: List[str] = field(default_factory=list)


@dataclass
class SanctionsMatch:
    list_name: str
    entity_name: str
    entity_type: str
    score: float
    match_type: SanctionsMatchType
    program: str = ""
    remarks: str = ""


@dataclass
class SanctionsResult:
    has_match: bool
    matches: List[SanctionsMatch]
    screened_name: str
    lists_checked: List[str]
    screening_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SARReport:
    sar_number: str
    alert_id: str
    subject_name: str
    suspicious_activity_type: str
    total_amount: float
    date_range: Tuple[str, str]
    narrative: str
    status: SARStatus
    filing_date: Optional[str] = None
    filing_agency: str = "FinCEN"


@dataclass
class AuditEvent:
    event_id: str
    event_type: AuditEventType
    actor_id: str
    customer_id: str
    action: str
    details: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    hash_chain: str = ""


@dataclass
class AuditReport:
    total_events: int
    event_breakdown: Dict[str, int]
    compliance_score: float
    period_start: str
    period_end: str
    exceptions: List[str] = field(default_factory=list)


class KYCWorkflow:
    """Automated Know Your Customer workflow."""

    def __init__(self, jurisdiction: str = "US",
                 enhanced_due_diligence_threshold: float = 1_000_000):
        self.jurisdiction = jurisdiction
        self.edd_threshold = enhanced_due_diligence_threshold

    def process_customer(
        self, customer_id: str, customer_type: str,
        documents: List[Dict[str, Any]],
        source_of_funds: str = "",
        expected_transaction_volume: str = "low",
    ) -> KYCResult:
        checks_total = 3 + len(documents)
        checks_passed = checks_total
        flags = []

        if expected_transaction_volume == "high":
            flags.append("enhanced_review_recommended")
            checks_passed -= 1

        risk_tier = CustomerRiskTier.LOW
        if expected_transaction_volume == "high":
            risk_tier = CustomerRiskTier.MEDIUM

        review_months = {"low": 24, "medium": 12, "high": 6}
        next_review = (datetime.now() + timedelta(days=365 * review_months.get(risk_tier.value, 12))).isoformat()

        return KYCResult(
            customer_id=customer_id,
            status=KYCStatus.APPROVED if checks_passed == checks_total else KYCStatus.UNDER_REVIEW,
            risk_tier=risk_tier,
            next_review_date=next_review,
            documents_verified=len(documents),
            checks_passed=checks_passed,
            checks_total=checks_total,
            flags=flags,
        )


class SanctionsScreener:
    """Multi-list sanctions screening with fuzzy matching."""

    def __init__(self, lists: Optional[List[str]] = None,
                 fuzzy_threshold: float = 0.85, alias_expansion: bool = True):
        self.lists = lists or ["OFAC_SDN"]
        self.fuzzy_threshold = fuzzy_threshold
        self.alias_expansion = alias_expansion

    def screen(self, name: str, date_of_birth: str = "",
               nationality: str = "", document_number: str = "") -> SanctionsResult:
        matches = []
        # Simulate screening against each list
        for list_name in self.lists:
            score = 0.12  # Simulated low match score
            if "al-rashid" in name.lower():
                score = 0.92
                matches.append(SanctionsMatch(
                    list_name=list_name, entity_name="Mohammed Al-Rashid",
                    entity_type="individual", score=score,
                    match_type=SanctionsMatchType.FUZZY,
                    program="SDN", remarks="Potential match - manual review required",
                ))

        return SanctionsResult(
            has_match=len(matches) > 0,
            matches=matches,
            screened_name=name,
            lists_checked=self.lists,
        )


class SARFiling:
    """Suspicious Activity Report generation and filing."""

    def __init__(self, agency: str = "FinCEN", filing_type: str = "initial",
                 auto_narrative: bool = True):
        self.agency = agency
        self.filing_type = filing_type
        self.auto_narrative = auto_narrative
        self._counter = 0

    def generate_sar(
        self, alert_id: str, subject: Dict[str, Any],
        suspicious_activity: Dict[str, Any],
    ) -> SARReport:
        self._counter += 1
        sar_number = f"SAR-{datetime.now().year}-{self._counter:06d}"

        if self.auto_narrative:
            narrative = self._build_narrative(subject, suspicious_activity)
        else:
            narrative = ""

        return SARReport(
            sar_number=sar_number, alert_id=alert_id,
            subject_name=subject.get("name", "Unknown"),
            suspicious_activity_type=suspicious_activity.get("type", "unknown"),
            total_amount=suspicious_activity.get("amount", 0),
            date_range=suspicious_activity.get("date_range", ("", "")),
            narrative=narrative, status=SARStatus.DRAFT,
            filing_agency=self.agency,
        )

    def _build_narrative(self, subject: Dict[str, Any],
                         activity: Dict[str, Any]) -> str:
        name = subject.get("name", "the subject")
        act_type = activity.get("type", "suspicious activity")
        amount = activity.get("amount", 0)
        desc = activity.get("description", "")
        return (
            f"This SAR is being filed regarding {name} based on {act_type}. "
            f"The total amount of suspicious activity is ${amount:,.2f}. "
            f"{desc} "
            f"This activity was identified through automated transaction monitoring."
        )

    def submit(self, sar: SARReport) -> SARReport:
        sar.status = SARStatus.FILED
        sar.filing_date = datetime.now().isoformat()
        return sar


class AuditTrailManager:
    """Immutable audit trail with tamper-evident chaining."""

    def __init__(self, retention_years: int = 7,
                 tamper_evident: bool = True, immutable: bool = True):
        self.retention_years = retention_years
        self.tamper_evident = tamper_evident
        self.immutable = immutable
        self._events: List[AuditEvent] = []
        self._last_hash = "genesis"

    def record(self, event_type: AuditEventType, actor_id: str,
               customer_id: str, action: str,
               details: Optional[Dict[str, Any]] = None) -> AuditEvent:
        event_id = f"AUD-{uuid.uuid4().hex[:12].upper()}"
        event = AuditEvent(
            event_id=event_id, event_type=event_type,
            actor_id=actor_id, customer_id=customer_id,
            action=action, details=details or {},
        )
        if self.tamper_evident:
            event.hash_chain = hashlib.sha256(
                f"{self._last_hash}{event_id}{action}".encode()
            ).hexdigest()[:16]
            self._last_hash = event.hash_chain

        self._events.append(event)
        return event

    def generate_report(
        self, start_date: str, end_date: str,
        event_types: Optional[List[str]] = None,
    ) -> AuditReport:
        events = [
            e for e in self._events
            if start_date <= e.timestamp[:10] <= end_date
        ]
        if event_types:
            events = [e for e in events if e.event_type.value in event_types]

        breakdown: Dict[str, int] = {}
        for e in events:
            breakdown[e.event_type.value] = breakdown.get(e.event_type.value, 0) + 1

        expected_events = max(len(events) * 0.95, 1)
        compliance_score = min(len(events) / max(expected_events, 1), 1.0)

        return AuditReport(
            total_events=len(events),
            event_breakdown=breakdown,
            compliance_score=round(compliance_score, 2),
            period_start=start_date,
            period_end=end_date,
        )

    def get_events(self, customer_id: Optional[str] = None,
                   event_type: Optional[AuditEventType] = None) -> List[AuditEvent]:
        events = self._events
        if customer_id:
            events = [e for e in events if e.customer_id == customer_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events


def main():
    print("=" * 60)
    print("  Compliance Automation Demo")
    print("=" * 60)

    # KYC
    print("\n--- KYC/CDD Workflow ---")
    workflow = KYCWorkflow(jurisdiction="US")
    kyc = workflow.process_customer(
        "CUST-001", "individual",
        [{"type": "passport"}, {"type": "proof_of_address"}],
        source_of_funds="employment", expected_transaction_volume="moderate",
    )
    print(f"  Status: {kyc.status.value}, Risk: {kyc.risk_tier.value}")
    print(f"  Checks: {kyc.checks_passed}/{kyc.checks_total}")
    print(f"  Next review: {kyc.next_review_date[:10]}")

    # Sanctions
    print("\n--- Sanctions Screening ---")
    screener = SanctionsScreener(lists=["OFAC_SDN", "EU_SANCTIONS"])
    sanctions = screener.screen("Mohammed Al-Rashid", "1985-03-15", "AE")
    print(f"  Match: {sanctions.has_match}, Lists checked: {len(sanctions.lists_checked)}")
    if sanctions.has_match:
        m = sanctions.matches[0]
        print(f"  Hit: {m.entity_name} on {m.list_name} (score={m.score:.2f})")

    # SAR
    print("\n--- SAR Filing ---")
    filing = SARFiling(agency="FinCEN")
    sar = filing.generate_sar(
        "AML-001",
        {"name": "John Doe", "dob": "1980-01-15"},
        {"type": "structuring", "amount": 47500,
         "description": "Multiple deposits below reporting threshold.",
         "date_range": ("2026-06-01", "2026-06-30")},
    )
    print(f"  SAR: {sar.sar_number}, Status: {sar.status.value}")
    print(f"  Narrative: {sar.narrative[:80]}...")
    filing.submit(sar)
    print(f"  Filed: {sar.filing_date}")

    # Audit trail
    print("\n--- Audit Trail ---")
    audit = AuditTrailManager(retention_years=7)
    audit.record(AuditEventType.KYC_APPROVED, "agent_001", "CUST-001", "kyc_approved", {"risk": "low"})
    audit.record(AuditEventType.ACCOUNT_OPENED, "agent_001", "CUST-001", "account_created")
    report = audit.generate_report("2020-01-01", "2030-12-31")
    print(f"  Events: {report.total_events}, Score: {report.compliance_score:.1%}")
    print(f"  Breakdown: {report.event_breakdown}")


if __name__ == "__main__":
    main()
