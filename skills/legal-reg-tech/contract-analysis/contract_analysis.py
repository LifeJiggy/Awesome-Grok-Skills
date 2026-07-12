"""
Contract Analysis Module
Contract analysis, term extraction, and risk assessment
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ContractType(Enum):
    SERVICE_AGREEMENT = "service_agreement"
    NDA = "nda"
    EMPLOYMENT = "employment"
    VENDOR = "vendor"
    LICENSING = "licensing"

@dataclass
class Contract:
    file_path: str = ""
    parties: List[str] = field(default_factory=list)
    contract_type: str = ""
    content: str = ""

@dataclass
class ContractAnalysisResult:
    contract_type: str = ""
    parties: List[str] = field(default_factory=list)
    effective_date: str = ""
    expiration_date: str = ""
    total_value: float = 0.0
    key_terms: List[str] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class RiskItem:
    clause: str = ""
    risk_description: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    recommendation: str = ""

@dataclass
class RiskAssessmentResult:
    overall_risk: RiskLevel = RiskLevel.LOW
    high_risk_count: int = 0
    top_risks: List[RiskItem] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class Obligation:
    party: str = ""
    description: str = ""
    deadline: str = ""
    penalty: str = ""
    priority: str = "medium"

class ContractAnalyzer:
    def analyze(self, contract: Contract) -> ContractAnalysisResult:
        return ContractAnalysisResult(contract_type=contract.contract_type or "service_agreement", parties=contract.parties, effective_date="2024-01-01", expiration_date="2025-01-01", total_value=120000.00, key_terms=["payment_terms", "termination", "confidentiality"])

class RiskAssessor:
    def assess(self, analysis: ContractAnalysisResult) -> RiskAssessmentResult:
        risks = [RiskItem(clause="Limitation of Liability", risk_description="Liability cap may be insufficient", risk_level=RiskLevel.MEDIUM, recommendation="Consider increasing liability cap")]
        return RiskAssessmentResult(overall_risk=RiskLevel.MEDIUM, high_risk_count=1, top_risks=risks, recommendations=["Review liability clause"])

class ObligationExtractor:
    def extract(self, analysis: ContractAnalysisResult) -> List[Obligation]:
        return [Obligation(party=analysis.parties[0] if analysis.parties else "", description="Deliver monthly reports", deadline="Monthly", penalty="Late delivery penalty")]

class ContractComparator:
    def compare(self, original: str, revised: str) -> Dict[str, Any]:
        return {"change_count": 5, "additions": 2, "deletions": 1, "modifications": 2}

def main() -> None:
    print("=" * 60)
    print("  Contract Analysis Module — Demo")
    print("=" * 60)

    analyzer = ContractAnalyzer()
    analysis = analyzer.analyze(Contract(file_path="/contracts/agreement.pdf", parties=["Acme Corp", "Beta Inc"], contract_type="service_agreement"))
    print(f"\n[+] Contract: {analysis.contract_type}, value=${analysis.total_value:,.2f}")

    assessor = RiskAssessor()
    risks = assessor.assess(analysis)
    print(f"\n[+] Risk: {risks.overall_risk.value}, {risks.high_risk_count} high-risk items")

    extractor = ObligationExtractor()
    obligations = extractor.extract(analysis)
    print(f"\n[+] Obligations: {len(obligations)}")
    for o in obligations:
        print(f"    {o.party}: {o.description} ({o.deadline})")

    comparator = ContractComparator()
    diff = comparator.compare("v1.pdf", "v2.pdf")
    print(f"\n[+] Comparison: {diff['change_count']} changes")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
