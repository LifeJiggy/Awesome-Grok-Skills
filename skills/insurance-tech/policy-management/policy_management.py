"""
Policy Management Module
Insurance policy lifecycle management and endorsements
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class InsuranceLine(Enum):
    AUTO = "auto"
    HOMEOWNERS = "homeowners"
    COMMERCIAL_PROPERTY = "commercial_property"
    GENERAL_LIABILITY = "general_liability"
    PROFESSIONAL_LIABILITY = "professional_liability"
    HEALTH = "health"
    LIFE = "life"
    WORKERS_COMP = "workers_comp"


class PolicyStatus(Enum):
    QUOTE = "quote"
    APPLICATION = "application"
    BOUND = "bound"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    NON_RENEWED = "non_renewed"
    PENDING_RENEWAL = "pending_renewal"


class EndorsementType(Enum):
    ADD_COVERAGE = "add_coverage"
    REMOVE_COVERAGE = "remove_coverage"
    INCREASE_LIMIT = "increase_limit"
    DECREASE_LIMIT = "decrease_limit"
    CHANGE_DEDUCTIBLE = "change_deductible"
    ADD_INTEREST = "add_interest"
    REMOVE_INTEREST = "remove_interest"
    NAME_CHANGE = "name_change"


class RenewalStatus(Enum):
    PENDING = "pending"
    QUOTED = "quoted"
    OFFER_SENT = "offer_sent"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


class BillingStatus(Enum):
    CURRENT = "current"
    PAST_DUE = "past_due"
    DELINQUENT = "delinquent"
    CANCELLED = "cancelled"
    PAID = "paid"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class CoverageOption:
    """Insurance coverage option."""
    name: str
    limit: float = 0.0
    deductible: float = 0.0
    premium: float = 0.0
    description: str = ""
    is_included: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "limit": self.limit,
            "deductible": self.deductible,
            "premium": self.premium,
        }


@dataclass
class PolicyApplication:
    """Policy application."""
    applicant_name: str = ""
    insurance_line: InsuranceLine = InsuranceLine.AUTO
    effective_date: str = ""
    coverages: List[CoverageOption] = field(default_factory=list)
    additional_interests: List[str] = field(default_factory=list)
    applicant_info: Dict[str, Any] = field(default_factory=dict)
    submission_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Policy:
    """Insurance policy record."""
    policy_number: str = ""
    insured_name: str = ""
    insurance_line: InsuranceLine = InsuranceLine.AUTO
    status: PolicyStatus = PolicyStatus.QUOTE
    effective_date: str = ""
    expiration_date: str = ""
    premium: float = 0.0
    coverages: List[CoverageOption] = field(default_factory=list)
    additional_interests: List[str] = field(default_factory=list)
    agent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    renewal_policy_number: Optional[str] = None
    endorsements: List[str] = field(default_factory=list)

    @property
    def is_active(self) -> bool:
        return self.status == PolicyStatus.ACTIVE

    @property
    def days_until_expiry(self) -> Optional[int]:
        if not self.expiration_date:
            return None
        try:
            exp = datetime.strptime(self.expiration_date, "%Y-%m-%d")
            return (exp - datetime.now()).days
        except ValueError:
            return None


@dataclass
class PolicyIssueResult:
    """Result of policy issuance."""
    policy_number: str = ""
    status: PolicyStatus = PolicyStatus.ACTIVE
    effective_date: str = ""
    expiration_date: str = ""
    premium: float = 0.0
    bind_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CoverageChange:
    """Change to a coverage."""
    coverage_name: str = ""
    action: str = ""  # increase_limit, decrease_limit, add, remove
    new_limit: Optional[float] = None
    new_deductible: Optional[float] = None
    reason: str = ""


@dataclass
class EndorsementRequest:
    """Endorsement request."""
    policy_number: str = ""
    effective_date: str = ""
    changes: List[CoverageChange] = field(default_factory=list)
    requested_by: str = ""
    request_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EndorsementResult:
    """Result of endorsement processing."""
    endorsement_number: str = ""
    policy_number: str = ""
    effective_date: str = ""
    premium_change: float = 0.0
    new_premium: float = 0.0
    status: str = "processed"
    processed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RenewalOffer:
    """Renewal offer."""
    policy_number: str = ""
    new_effective_date: str = ""
    new_expiration_date: str = ""
    renewal_premium: float = 0.0
    retention_discount: float = 0.0
    status: RenewalStatus = RenewalStatus.PENDING
    offer_date: datetime = field(default_factory=datetime.utcnow)
    response_date: Optional[datetime] = None


@dataclass
class PolicyTransaction:
    """Policy transaction record."""
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=datetime.utcnow)
    description: str = ""
    transaction_type: str = ""
    premium_change: float = 0.0
    agent_id: Optional[str] = None


@dataclass
class PolicyInquiryResult:
    """Policy inquiry result."""
    policy_number: str = ""
    insured_name: str = ""
    insurance_line: str = ""
    status: str = ""
    effective_date: str = ""
    expiration_date: str = ""
    premium: float = 0.0
    coverages: List[Dict[str, Any]] = field(default_factory=list)
    additional_interests: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Policy Engine
# ---------------------------------------------------------------------------

class PolicyEngine:
    """Main engine for policy management."""

    def __init__(self) -> None:
        self._policies: Dict[str, Policy] = {}
        self._transactions: Dict[str, List[PolicyTransaction]] = {}

    def issue_policy(self, application: PolicyApplication) -> PolicyIssueResult:
        policy_number = f"{application.insurance_line.value[:2].upper()}-{datetime.utcnow().year}-{str(uuid.uuid4())[:8].upper()}"

        # Calculate premium (simplified)
        premium = sum(c.limit * 0.001 for c in application.coverages)

        # Set dates
        effective = application.effective_date or datetime.utcnow().strftime("%Y-%m-%d")
        try:
            eff_date = datetime.strptime(effective, "%Y-%m-%d")
            exp_date = eff_date + timedelta(days=365)
        except ValueError:
            eff_date = datetime.now()
            exp_date = eff_date + timedelta(days=365)

        policy = Policy(
            policy_number=policy_number,
            insured_name=application.applicant_name,
            insurance_line=application.insurance_line,
            status=PolicyStatus.ACTIVE,
            effective_date=eff_date.strftime("%Y-%m-%d"),
            expiration_date=exp_date.strftime("%Y-%m-%d"),
            premium=premium,
            coverages=application.coverages,
            additional_interests=application.additional_interests,
        )
        self._policies[policy_number] = policy
        self._transactions[policy_number] = []

        self._add_transaction(policy_number, "Policy Issued", "issue", premium)

        return PolicyIssueResult(
            policy_number=policy_number,
            status=PolicyStatus.ACTIVE,
            effective_date=policy.effective_date,
            expiration_date=policy.expiration_date,
            premium=premium,
        )

    def process_endorsement(self, endorsement: EndorsementRequest) -> EndorsementResult:
        policy = self._policies.get(endorsement.policy_number)
        if policy is None:
            return EndorsementResult(status="error")

        premium_change = 0.0
        for change in endorsement.changes:
            if change.action == "increase_limit" and change.new_limit:
                # Find coverage and calculate premium change
                for coverage in policy.coverages:
                    if coverage.name == change.coverage_name:
                        old_premium = coverage.premium
                        coverage.limit = change.new_limit
                        coverage.premium = change.new_limit * 0.001
                        premium_change += coverage.premium - old_premium

        policy.premium += premium_change
        policy.updated_at = datetime.utcnow()

        endorsement_number = f"END-{str(uuid.uuid4())[:8].upper()}"
        policy.endorsements.append(endorsement_number)

        self._add_transaction(
            endorsement.policy_number,
            f"Endorsement {endorsement_number}",
            "endorsement",
            premium_change,
        )

        return EndorsementResult(
            endorsement_number=endorsement_number,
            policy_number=endorsement.policy_number,
            effective_date=endorsement.effective_date,
            premium_change=premium_change,
            new_premium=policy.premium,
        )

    def _add_transaction(self, policy_number: str, description: str, tx_type: str, premium_change: float) -> None:
        if policy_number not in self._transactions:
            self._transactions[policy_number] = []
        self._transactions[policy_number].append(PolicyTransaction(
            description=description,
            transaction_type=tx_type,
            premium_change=premium_change,
        ))

    def get_policy(self, policy_number: str) -> Optional[Policy]:
        return self._policies.get(policy_number)

    def get_transactions(self, policy_number: str) -> List[PolicyTransaction]:
        return self._transactions.get(policy_number, [])


# ---------------------------------------------------------------------------
# Renewal Processor
# ---------------------------------------------------------------------------

class RenewalProcessor:
    """Handles policy renewal processing."""

    def __init__(self, retention_discount_rate: float = 0.05) -> None:
        self.retention_discount_rate = retention_discount_rate

    def process_renewal(
        self,
        policy_number: str,
        renewal_term: str = "annual",
        retention_offer: bool = True,
    ) -> RenewalOffer:
        # Simulate renewal processing
        retention_discount = self.retention_discount_rate if retention_offer else 0.0

        return RenewalOffer(
            policy_number=policy_number,
            new_effective_date="2025-02-01",
            new_expiration_date="2026-02-01",
            renewal_premium=10000.00 * (1 - retention_discount),
            retention_discount=retention_discount,
            status=RenewalStatus.QUOTED,
        )


# ---------------------------------------------------------------------------
# Policy Inquiry
# ---------------------------------------------------------------------------

class PolicyInquiry:
    """Provides policy lookup and inquiry."""

    def __init__(self, policy_engine: Optional[PolicyEngine] = None) -> None:
        self._engine = policy_engine or PolicyEngine()

    def get_policy(self, policy_number: str) -> Optional[PolicyInquiryResult]:
        policy = self._engine.get_policy(policy_number)
        if policy is None:
            return None

        return PolicyInquiryResult(
            policy_number=policy.policy_number,
            insured_name=policy.insured_name,
            insurance_line=policy.insurance_line.value,
            status=policy.status.value,
            effective_date=policy.effective_date,
            expiration_date=policy.expiration_date,
            premium=policy.premium,
            coverages=[c.to_dict() for c in policy.coverages],
            additional_interests=policy.additional_interests,
        )

    def get_policy_history(self, policy_number: str) -> List[PolicyTransaction]:
        return self._engine.get_transactions(policy_number)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Policy Management module."""
    print("=" * 60)
    print("  Policy Management Module — Demo")
    print("=" * 60)

    engine = PolicyEngine()

    # Issue policy
    application = PolicyApplication(
        applicant_name="Acme Corporation",
        insurance_line=InsuranceLine.COMMERCIAL_PROPERTY,
        effective_date="2024-02-01",
        coverages=[
            CoverageOption(name="building", limit=1000000, deductible=5000),
            CoverageOption(name="contents", limit=250000, deductible=2500),
        ],
        additional_interests=["Mortgage Company Inc."],
    )
    result = engine.issue_policy(application)
    print(f"\n[+] Policy Issued:")
    print(f"    Number: {result.policy_number}")
    print(f"    Status: {result.status.value}")
    print(f"    Effective: {result.effective_date}")
    print(f"    Premium: ${result.premium:,.2f}")

    # Endorsement
    endorsement = EndorsementRequest(
        policy_number=result.policy_number,
        effective_date="2024-06-01",
        changes=[
            CoverageChange(coverage_name="building", action="increase_limit", new_limit=1500000),
        ],
        requested_by="agent-001",
    )
    end_result = engine.process_endorsement(endorsement)
    print(f"\n[+] Endorsement Processed:")
    print(f"    Number: {end_result.endorsement_number}")
    print(f"    Premium Change: ${end_result.premium_change:,.2f}")
    print(f"    New Premium: ${end_result.new_premium:,.2f}")

    # Renewal
    renewal_processor = RenewalProcessor()
    renewal = renewal_processor.process_renewal(result.policy_number, retention_offer=True)
    print(f"\n[+] Renewal Offer:")
    print(f"    Policy: {renewal.policy_number}")
    print(f"    Renewal Premium: ${renewal.renewal_premium:,.2f}")
    print(f"    Retention Discount: {renewal.retention_discount:.1%}")

    # Inquiry
    inquiry = PolicyInquiry(engine)
    details = inquiry.get_policy(result.policy_number)
    if details:
        print(f"\n[+] Policy Inquiry:")
        print(f"    Number: {details.policy_number}")
        print(f"    Insured: {details.insured_name}")
        print(f"    Line: {details.insurance_line}")
        print(f"    Status: {details.status}")
        print(f"    Coverages: {len(details.coverages)}")

    history = inquiry.get_policy_history(result.policy_number)
    print(f"\n[+] Policy History: {len(history)} transactions")
    for tx in history:
        print(f"    - {tx.description}: ${tx.premium_change:,.2f}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
