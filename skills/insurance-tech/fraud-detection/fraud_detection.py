"""
Fraud Detection Module
Insurance fraud detection, prevention, and investigation
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FraudRiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ClaimType(Enum):
    AUTO_COLLISION = "auto_collision"
    AUTO_COMPREHENSIVE = "auto_comprehensive"
    PROPERTY_DAMAGE = "property_damage"
    PROPERTY_THEFT = "property_theft"
    HEALTH_MEDICAL = "health_medical"
    LIABILITY_GENERAL = "liability_general"


class CaseStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    PENDING_REVIEW = "pending_review"
    REFERRED = "referred"
    CLOSED_GENUINE = "closed_genuine"
    CLOSED_FRAUDULENT = "closed_fraudulent"


class ServiceProviderType(Enum):
    AUTO_REPAIR = "auto_repair"
    MEDICAL_PROVIDER = "medical_provider"
    LEGAL_SERVICES = "legal_services"
    CONTRACTOR = "contractor"


class OperatorType(Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    CONTAINS = "contains"
    IN_LIST = "in_list"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ClaimScoreRequest:
    """Request for claim fraud scoring."""
    claim_number: str = ""
    policy_number: str = ""
    claim_type: str = ""
    reported_amount: float = 0.0
    loss_date: str = ""
    claimant_name: str = ""
    loss_description: str = ""
    claimant_age: Optional[int] = None
    policy_age_days: Optional[int] = None
    prior_claims: int = 0
    loss_location: str = ""


@dataclass
class FraudScore:
    """Result of fraud scoring."""
    claim_number: str = ""
    risk_score: float = 0.0  # 0.0 to 1.0
    risk_level: FraudRiskLevel = FraudRiskLevel.LOW
    confidence: float = 0.85
    red_flags: List[str] = field(default_factory=list)
    model_version: str = "v1.0"
    scored_at: datetime = field(default_factory=datetime.utcnow)
    recommendation: str = ""


@dataclass
class RuleCondition:
    """Condition for a fraud detection rule."""
    field: str = ""
    operator: OperatorType = OperatorType.EQUALS
    value: Any = None

    def evaluate(self, data: Dict[str, Any]) -> bool:
        field_value = data.get(self.field)
        if field_value is None:
            return False

        if self.operator == OperatorType.EQUALS:
            return field_value == self.value
        elif self.operator == OperatorType.NOT_EQUALS:
            return field_value != self.value
        elif self.operator == OperatorType.GREATER_THAN:
            return float(field_value) > float(self.value)
        elif self.operator == OperatorType.LESS_THAN:
            return float(field_value) < float(self.value)
        elif self.operator == OperatorType.CONTAINS:
            return str(self.value).lower() in str(field_value).lower()
        elif self.operator == OperatorType.IN_LIST:
            return field_value in self.value if isinstance(self.value, list) else False
        return False


@dataclass
class FraudRule:
    """Fraud detection rule."""
    name: str = ""
    description: str = ""
    conditions: List[RuleCondition] = field(default_factory=list)
    score_weight: int = 10
    enabled: bool = True
    category: str = "general"

    def evaluate(self, data: Dict[str, Any]) -> Tuple[bool, int]:
        if not self.enabled:
            return False, 0

        all_match = all(cond.evaluate(data) for cond in self.conditions)
        return all_match, self.score_weight if all_match else 0


@dataclass
class ServiceProvider:
    """Service provider for analysis."""
    provider_id: str = ""
    provider_type: ServiceProviderType = ServiceProviderType.AUTO_REPAIR
    name: str = ""
    location: str = ""
    claim_count: int = 0
    total_billed: float = 0.0
    avg_claim_amount: float = 0.0
    unique_claimants: int = 0

    @property
    def claims_per_claimant(self) -> float:
        if self.unique_claimants == 0:
            return 0.0
        return self.claim_count / self.unique_claimants


@dataclass
class ProviderAnalysis:
    """Result of provider fraud analysis."""
    provider_id: str = ""
    provider_name: str = ""
    anomaly_score: float = 0.0
    red_flags: List[str] = field(default_factory=list)
    referral_recommended: bool = False
    analysis_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class InvestigationCase:
    """Fraud investigation case."""
    case_id: str = field(default_factory=lambda: f"SIU-{str(uuid.uuid4())[:8].upper()}")
    claim_number: str = ""
    fraud_score: float = 0.0
    red_flags: List[str] = field(default_factory=list)
    status: CaseStatus = CaseStatus.OPEN
    assigned_investigator: str = ""
    priority: str = "medium"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    notes: List[str] = field(default_factory=list)
    resolution: str = ""


@dataclass
class CaseUpdate:
    """Update to an investigation case."""
    status: Optional[CaseStatus] = None
    notes: str = ""
    assigned_investigator: Optional[str] = None
    priority: Optional[str] = None


# ---------------------------------------------------------------------------
# Fraud Engine
# ---------------------------------------------------------------------------

class FraudEngine:
    """Main fraud detection engine."""

    def __init__(self, model_version: str = "v1.0") -> None:
        self.model_version = model_version
        self._rules: List[FraudRule] = []
        self._scoring_history: List[FraudScore] = []

    def add_rule(self, rule: FraudRule) -> None:
        self._rules.append(rule)

    def score_claim(self, request: ClaimScoreRequest) -> FraudScore:
        score = 0.0
        red_flags = []

        # Evaluate rules
        data = {
            "claim_amount": request.reported_amount,
            "policy_age_days": request.policy_age_days or 999,
            "prior_claims": request.prior_claims,
            "claim_type": request.claim_type,
        }

        for rule in self._rules:
            matches, rule_score = rule.evaluate(data)
            if matches:
                score += rule_score
                red_flags.append(rule.name)

        # Built-in checks
        if request.reported_amount > 25000:
            score += 15
            red_flags.append("high_amount")

        if request.policy_age_days is not None and request.policy_age_days < 30:
            score += 20
            red_flags.append("recent_policy_inception")

        if request.prior_claims > 3:
            score += 10
            red_flags.append("frequent_claims")

        # Normalize score to 0-1
        normalized_score = min(1.0, score / 100.0)

        # Determine risk level
        if normalized_score >= 0.7:
            risk_level = FraudRiskLevel.VERY_HIGH
            recommendation = "Refer to SIU immediately"
        elif normalized_score >= 0.5:
            risk_level = FraudRiskLevel.HIGH
            recommendation = "Enhanced investigation recommended"
        elif normalized_score >= 0.3:
            risk_level = FraudRiskLevel.MEDIUM
            recommendation = "Additional documentation required"
        else:
            risk_level = FraudRiskLevel.LOW
            recommendation = "Standard processing"

        result = FraudScore(
            claim_number=request.claim_number,
            risk_score=normalized_score,
            risk_level=risk_level,
            red_flags=red_flags,
            model_version=self.model_version,
            recommendation=recommendation,
        )

        self._scoring_history.append(result)
        return result

    def batch_score(self, requests: List[ClaimScoreRequest]) -> List[FraudScore]:
        return [self.score_claim(r) for r in requests]

    def get_high_risk_claims(self, threshold: float = 0.5) -> List[FraudScore]:
        return [s for s in self._scoring_history if s.risk_score >= threshold]


# ---------------------------------------------------------------------------
# Rule Engine
# ---------------------------------------------------------------------------

class RuleEngine:
    """Manages fraud detection rules."""

    def __init__(self) -> None:
        self._rules: List[FraudRule] = []

    def add_rule(self, rule: FraudRule) -> None:
        self._rules.append(rule)

    def remove_rule(self, name: str) -> bool:
        for i, rule in enumerate(self._rules):
            if rule.name == name:
                self._rules.pop(i)
                return True
        return False

    def evaluate(self, data: Dict[str, Any]) -> List[Tuple[FraudRule, int]]:
        results = []
        for rule in self._rules:
            matches, score = rule.evaluate(data)
            if matches:
                results.append((rule, score))
        return results

    def get_rules(self) -> List[FraudRule]:
        return self._rules.copy()


# ---------------------------------------------------------------------------
# Provider Analyzer
# ---------------------------------------------------------------------------

class ProviderAnalyzer:
    """Analyzes service providers for fraud patterns."""

    def __init__(self, avg_claim_threshold: float = 5000, claims_per_claimant_threshold: float = 3.0) -> None:
        self.avg_claim_threshold = avg_claim_threshold
        self.claims_per_claimant_threshold = claims_per_claimant_threshold

    def analyze_provider(self, provider: ServiceProvider) -> ProviderAnalysis:
        red_flags = []
        anomaly_score = 0.0

        # Check average claim amount
        avg_amount = provider.total_billed / max(provider.claim_count, 1)
        if avg_amount > self.avg_claim_threshold:
            red_flags.append("high_avg_claim_amount")
            anomaly_score += 0.3

        # Check claims per claimant
        if provider.claim_count > 0 and provider.unique_claimants > 0:
            ratio = provider.claim_count / provider.unique_claimants
            if ratio > self.claims_per_claimant_threshold:
                red_flags.append("high_claims_per_claimant")
                anomaly_score += 0.3

        # Check for unusual patterns
        if provider.claim_count > 100 and provider.unique_claimants < 20:
            red_flags.append("concentrated_claimants")
            anomaly_score += 0.2

        return ProviderAnalysis(
            provider_id=provider.provider_id,
            provider_name=provider.name,
            anomaly_score=min(1.0, anomaly_score),
            red_flags=red_flags,
            referral_recommended=anomaly_score > 0.5,
        )


# ---------------------------------------------------------------------------
# Case Manager
# ---------------------------------------------------------------------------

class CaseManager:
    """Manages fraud investigation cases."""

    def __init__(self) -> None:
        self._cases: Dict[str, InvestigationCase] = {}

    def create_case(self, case: InvestigationCase) -> str:
        self._cases[case.case_id] = case
        return case.case_id

    def get_case(self, case_id: str) -> Optional[InvestigationCase]:
        return self._cases.get(case_id)

    def update_status(self, case_id: str, status: Optional[CaseStatus] = None, notes: str = "", assigned_investigator: Optional[str] = None) -> bool:
        case = self._cases.get(case_id)
        if case is None:
            return False

        if status:
            case.status = status
        if notes:
            case.notes.append(f"[{datetime.utcnow().isoformat()}] {notes}")
        if assigned_investigator:
            case.assigned_investigator = assigned_investigator
        case.updated_at = datetime.utcnow()
        return True

    def add_note(self, case_id: str, note: str) -> bool:
        case = self._cases.get(case_id)
        if case is None:
            return False
        case.notes.append(f"[{datetime.utcnow().isoformat()}] {note}")
        case.updated_at = datetime.utcnow()
        return True

    def get_open_cases(self) -> List[InvestigationCase]:
        return [c for c in self._cases.values() if c.status in (CaseStatus.OPEN, CaseStatus.INVESTIGATING)]

    def close_case(self, case_id: str, resolution: str, fraudulent: bool) -> bool:
        case = self._cases.get(case_id)
        if case is None:
            return False
        case.status = CaseStatus.CLOSED_FRAUDULENT if fraudulent else CaseStatus.CLOSED_GENUINE
        case.resolution = resolution
        case.updated_at = datetime.utcnow()
        return True


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Fraud Detection module."""
    print("=" * 60)
    print("  Fraud Detection Module — Demo")
    print("=" * 60)

    # Fraud engine
    engine = FraudEngine(model_version="v3.0")
    engine.add_rule(FraudRule(
        name="high_amount_first_claim",
        conditions=[
            RuleCondition(field="prior_claims", operator=OperatorType.EQUALS, value=0),
            RuleCondition(field="claim_amount", operator=OperatorType.GREATER_THAN, value=10000),
        ],
        score_weight=30,
    ))

    # Score claims
    request = ClaimScoreRequest(
        claim_number="CLM-2024-0001",
        claim_type="auto_collision",
        reported_amount=15000.00,
        loss_date="2024-01-15",
        claimant_name="John Smith",
        policy_age_days=15,
        prior_claims=0,
    )
    score = engine.score_claim(request)
    print(f"\n[+] Fraud Score:")
    print(f"    Claim: {score.claim_number}")
    print(f"    Risk Score: {score.risk_score:.3f}")
    print(f"    Risk Level: {score.risk_level.value}")
    print(f"    Red Flags: {score.red_flags}")
    print(f"    Recommendation: {score.recommendation}")

    # Provider analysis
    analyzer = ProviderAnalyzer()
    provider = ServiceProvider(
        provider_id="PROV-001",
        name="Quick Fix Auto Body",
        claim_count=150,
        total_billed=2500000,
        unique_claimants=15,
    )
    analysis = analyzer.analyze_provider(provider)
    print(f"\n[+] Provider Analysis:")
    print(f"    Provider: {analysis.provider_name}")
    print(f"    Anomaly Score: {analysis.anomaly_score:.2f}")
    print(f"    Red Flags: {analysis.red_flags}")
    print(f"    Referral Recommended: {analysis.referral_recommended}")

    # Case management
    case_manager = CaseManager()
    case = InvestigationCase(
        claim_number="CLM-2024-0001",
        fraud_score=score.risk_score,
        red_flags=score.red_flags,
        assigned_investigator="siu-001",
    )
    case_id = case_manager.create_case(case)
    print(f"\n[+] Investigation Case Created: {case_id}")

    case_manager.update_status(case_id, status=CaseStatus.INVESTIGATING, notes="Starting investigation")
    case_manager.add_note(case_id, "Claimant provided inconsistent statements")

    open_cases = case_manager.get_open_cases()
    print(f"    Open Cases: {len(open_cases)}")

    # Close case
    case_manager.close_case(case_id, resolution="Confirmed fraud - staged accident", fraudulent=True)
    print(f"    Case Closed as Fraudulent")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
