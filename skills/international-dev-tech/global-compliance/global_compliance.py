"""
Global Compliance Module
Regulatory compliance management for international operations
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"

class ImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RegulationCategory(Enum):
    DATA_PRIVACY = "data_privacy"
    FINANCIAL = "financial"
    CONSUMER_PROTECTION = "consumer_protection"
    SECURITY = "security"
    INDUSTRY_SPECIFIC = "industry_specific"

@dataclass
class AssessmentRequest:
    company_region: str = ""
    target_markets: List[str] = field(default_factory=list)
    data_types: List[str] = field(default_factory=list)
    processing_activities: List[str] = field(default_factory=list)

@dataclass
class JurisdictionAssessment:
    name: str = ""
    compliance_score: float = 0.0
    status: ComplianceStatus = ComplianceStatus.UNKNOWN
    requirements: List[str] = field(default_factory=list)
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class ComplianceAssessmentResult:
    overall_score: float = 0.0
    jurisdictions: List[JurisdictionAssessment] = field(default_factory=list)
    assessed_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class DataProcessingActivity:
    activity_id: str = ""
    purpose: str = ""
    data_categories: List[str] = field(default_factory=list)
    legal_basis: str = "consent"
    retention_period_months: int = 12
    cross_border_transfers: bool = False
    transfer_countries: List[str] = field(default_factory=list)

@dataclass
class PrivacyCheckResult:
    is_compliant: bool = True
    requirements_met: int = 0
    missing_requirements: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class RegulatoryChange:
    change_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    title: str = ""
    jurisdiction: str = ""
    category: RegulationCategory = RegulationCategory.DATA_PRIVACY
    effective_date: str = ""
    impact_level: ImpactLevel = ImpactLevel.LOW
    action_required: str = ""
    description: str = ""
    published_date: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ConsentRecord:
    user_id: str = ""
    purpose: str = ""
    jurisdiction: str = ""
    consent_given: bool = False
    consent_method: str = ""
    recorded_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

@dataclass
class ConsentSummary:
    jurisdiction: str = ""
    total_users: int = 0
    consented: int = 0
    denied: int = 0
    pending: int = 0

REGULATION_REQUIREMENTS = {
    "EU": {
        "data_privacy": ["gdpr_compliance", "data_protection_officer", "privacy_policy", "consent_management", "data_breach_notification", "right_to_erasure"],
        "financial": ["psd2_compliance", "aml_kyc"],
    },
    "UK": {
        "data_privacy": ["uk_gdpr", "ico_registration", "privacy_policy"],
    },
    "BR": {
        "data_privacy": ["lgpd_compliance", "dpo_appointment", "consent_management"],
    },
    "US": {
        "data_privacy": ["ccpa_compliance", "state_privacy_laws"],
        "financial": ["sox_compliance", "glba"],
    },
}

class ComplianceEngine:
    def __init__(self) -> None:
        self._assessments: List[ComplianceAssessmentResult] = []

    def assess_compliance(self, request: AssessmentRequest) -> ComplianceAssessmentResult:
        jurisdictions = []
        for market in request.target_markets:
            market_reqs = REGULATION_REQUIREMENTS.get(market, {})
            all_reqs = []
            gaps = []
            for category in request.processing_activities:
                reqs = market_reqs.get("data_privacy", []) + market_reqs.get("financial", [])
                all_reqs.extend(reqs)
                gaps.extend(reqs[:2])  # Simulate some gaps

            score = max(0, 1.0 - len(gaps) / max(len(all_reqs), 1))
            status = ComplianceStatus.COMPLIANT if score > 0.9 else ComplianceStatus.PARTIALLY_COMPLIANT if score > 0.5 else ComplianceStatus.NON_COMPLIANT
            jurisdictions.append(JurisdictionAssessment(name=market, compliance_score=score, status=status, requirements=all_reqs, gaps=gaps))

        overall = sum(j.compliance_score for j in jurisdictions) / len(jurisdictions) if jurisdictions else 0
        result = ComplianceAssessmentResult(overall_score=overall, jurisdictions=jurisdictions)
        self._assessments.append(result)
        return result

class PrivacyManager:
    def __init__(self) -> None:
        self._activities: Dict[str, DataProcessingActivity] = {}

    def register_activity(self, activity: DataProcessingActivity) -> None:
        self._activities[activity.activity_id] = activity

    def check_gdpr_compliance(self, activity: DataProcessingActivity) -> PrivacyCheckResult:
        missing = []
        if activity.legal_basis not in ("consent", "legitimate_interest", "contract", "legal_obligation"):
            missing.append("valid_legal_basis")
        if not activity.data_categories:
            missing.append("data_categories_defined")
        if activity.retention_period_months > 60:
            missing.append("excessive_retention")
        return PrivacyCheckResult(is_compliant=len(missing) == 0, requirements_met=6 - len(missing), missing_requirements=missing)

class RegulatoryTracker:
    def __init__(self) -> None:
        self._changes: List[RegulatoryChange] = [
            RegulatoryChange(title="EU AI Act Implementation", jurisdiction="EU", category=RegulationCategory.DATA_PRIVACY, effective_date="2024-08-01", impact_level=ImpactLevel.HIGH, action_required="Conduct AI risk assessment"),
            RegulatoryChange(title="CCPA Amendments", jurisdiction="US-CA", category=RegulationCategory.DATA_PRIVACY, effective_date="2024-01-01", impact_level=ImpactLevel.MEDIUM, action_required="Update privacy policy"),
        ]

    def get_recent_changes(self, jurisdictions: List[str], days: int = 90, categories: Optional[List[str]] = None) -> List[RegulatoryChange]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [c for c in self._changes if c.published_date >= cutoff]

class ConsentManager:
    def __init__(self) -> None:
        self._records: List[ConsentRecord] = []

    def record_consent(self, user_id: str, purpose: str, jurisdiction: str, consent_given: bool, consent_method: str = "") -> None:
        self._records.append(ConsentRecord(user_id=user_id, purpose=purpose, jurisdiction=jurisdiction, consent_given=consent_given, consent_method=consent_method))

    def check_consent(self, user_id: str, purpose: str) -> bool:
        for record in reversed(self._records):
            if record.user_id == user_id and record.purpose == purpose:
                return record.consent_given
        return False

    def get_consent_summary(self, jurisdiction: str) -> ConsentSummary:
        records = [r for r in self._records if r.jurisdiction == jurisdiction]
        users = set(r.user_id for r in records)
        consented = sum(1 for uid in users if self.check_consent(uid, records[0].purpose if records else ""))
        return ConsentSummary(jurisdiction=jurisdiction, total_users=len(users), consented=consented, denied=len(users) - consented)

def main() -> None:
    print("=" * 60)
    print("  Global Compliance Module — Demo")
    print("=" * 60)

    engine = ComplianceEngine()
    assessment = engine.assess_compliance(AssessmentRequest(company_region="US", target_markets=["EU", "UK", "BR"], data_types=["personal_data"], processing_activities=["marketing", "analytics"]))
    print(f"\n[+] Compliance Assessment:")
    print(f"    Overall Score: {assessment.overall_score:.1%}")
    for jur in assessment.jurisdictions:
        print(f"    {jur.name}: {jur.compliance_score:.1%} ({jur.status.value})")

    privacy = PrivacyManager()
    activity = DataProcessingActivity(activity_id="marketing", purpose="Email marketing", data_categories=["name", "email"], legal_basis="consent")
    gdpr_check = privacy.check_gdpr_compliance(activity)
    print(f"\n[+] GDPR Check: {'Compliant' if gdpr_check.is_compliant else 'Non-Compliant'}")

    tracker = RegulatoryTracker()
    changes = tracker.get_recent_changes(["EU"], days=365)
    print(f"\n[+] Regulatory Changes: {len(changes)}")
    for c in changes:
        print(f"    {c.title} ({c.jurisdiction}): {c.impact_level.value}")

    consent_mgr = ConsentManager()
    consent_mgr.record_consent("user-1", "marketing", "EU", True)
    consent_mgr.record_consent("user-2", "marketing", "EU", False)
    print(f"\n[+] Consent Check: {consent_mgr.check_consent('user-1', 'marketing')}")
    print(f"    Summary: {consent_mgr.get_consent_summary('EU')}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
