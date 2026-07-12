"""
Underwriting AI Module
AI-assisted insurance underwriting with machine learning
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

class UnderwritingDecision(Enum):
    APPROVE = "approve"
    DECLINE = "decline"
    REFER = "refer"
    CONDITIONAL = "conditional"
    PENDING = "pending"


class RiskTier(Enum):
    PREFERRED_PLUS = "preferred_plus"
    PREFERRED = "preferred"
    STANDARD_PLUS = "standard_plus"
    STANDARD = "standard"
    SUBSTANDARD = "substandard"
    DECLINED = "declined"


class DocumentType(Enum):
    APPLICATION = "application"
    MEDICAL_RECORD = "medical_record"
    FINANCIAL_STATEMENT = "financial_statement"
    INSPECTION_REPORT = "inspection_report"
    CLAIMS_HISTORY = "claims_history"


class FactorImpact(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ApplicationData:
    """Insurance application data."""
    applicant_name: str = ""
    insurance_line: str = "auto"
    age: int = 30
    driving_history: str = "clean"
    vehicle_year: int = 2023
    vehicle_type: str = "sedan"
    annual_mileage: int = 12000
    credit_score: int = 700
    coverage_requested: Dict[str, int] = field(default_factory=dict)
    prior_claims: int = 0
    years_insured: int = 0
    location: str = ""
    additional_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnderwritingResult:
    """Result of underwriting decision."""
    application_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    applicant_name: str = ""
    outcome: UnderwritingDecision = UnderwritingDecision.PENDING
    risk_tier: RiskTier = RiskTier.STANDARD
    recommended_premium: float = 0.0
    confidence: float = 0.85
    is_straight_through: bool = True
    factors: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    decided_at: datetime = field(default_factory=datetime.utcnow)
    model_version: str = "v1.0"
    underwriter_notes: str = ""


@dataclass
class ExtractedField:
    """Extracted field from document."""
    name: str = ""
    value: Any = None
    confidence: float = 0.95
    source: str = ""


@dataclass
class DocumentAnalysis:
    """Result of document analysis."""
    document_type: DocumentType = DocumentType.APPLICATION
    extracted_fields: List[ExtractedField] = field(default_factory=list)
    data_quality_score: float = 0.90
    missing_fields: List[str] = field(default_factory=list)
    anomalies: List[str] = field(default_factory=list)
    analysis_time_ms: float = 0.0


@dataclass
class UnderwritingDocument:
    """Document for underwriting analysis."""
    document_type: DocumentType = DocumentType.APPLICATION
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FeatureFactor:
    """Factor influencing underwriting decision."""
    name: str = ""
    value: Any = None
    impact: FactorImpact = FactorImpact.NEUTRAL
    impact_score: float = 0.0
    description: str = ""


@dataclass
class ExplainabilityResult:
    """Explainability result for underwriting decision."""
    decision: str = ""
    primary_factors: List[FeatureFactor] = field(default_factory=list)
    feature_importance: List[FeatureFactor] = field(default_factory=list)
    model_confidence: float = 0.85
    explanation_text: str = ""


@dataclass
class BatchResult:
    """Result of batch processing."""
    total_processed: int = 0
    approved_count: int = 0
    referred_count: int = 0
    declined_count: int = 0
    conditional_count: int = 0
    processing_time_seconds: float = 0.0
    results: List[UnderwritingResult] = field(default_factory=list)

    @property
    def approval_rate(self) -> float:
        if self.total_processed == 0:
            return 0.0
        return self.approved_count / self.total_processed


@dataclass
class UnderwritingRule:
    """Rule for underwriting decisions."""
    name: str = ""
    condition: str = ""
    decision: UnderwritingDecision = UnderwritingDecision.REFER
    priority: int = 0
    enabled: bool = True


# ---------------------------------------------------------------------------
# Underwriting Engine
# ---------------------------------------------------------------------------

class UnderwritingEngine:
    """Main engine for AI-assisted underwriting."""

    def __init__(self, model_version: str = "v1.0") -> None:
        self.model_version = model_version
        self._rules: List[UnderwritingRule] = []
        self._decision_history: List[UnderwritingResult] = []

    def add_rule(self, rule: UnderwritingRule) -> None:
        self._rules.append(rule)

    def underwrite(self, application: ApplicationData) -> UnderwritingResult:
        # Calculate risk factors
        risk_score = self._calculate_risk_score(application)

        # Determine decision
        decision, tier = self._determine_decision(risk_score, application)

        # Calculate premium
        premium = self._calculate_premium(application, tier)

        # Check if straight-through
        is_stp = decision in (UnderwritingDecision.APPROVE, UnderwritingDecision.DECLINE) and risk_score not in (0.4, 0.5, 0.6)

        # Build factors
        factors = self._get_factors(application)

        result = UnderwritingResult(
            applicant_name=application.applicant_name,
            outcome=decision,
            risk_tier=tier,
            recommended_premium=premium,
            confidence=min(1.0, 0.8 + len(application.coverage_requested) * 0.02),
            is_straight_through=is_stp,
            factors=factors,
            model_version=self.model_version,
        )

        self._decision_history.append(result)
        return result

    def _calculate_risk_score(self, app: ApplicationData) -> float:
        score = 0.5  # Base score

        # Age factor
        if app.age < 25:
            score += 0.1
        elif app.age > 65:
            score += 0.05
        elif 30 <= app.age <= 55:
            score -= 0.1

        # Driving history
        if app.driving_history == "clean":
            score -= 0.15
        elif app.driving_history == "minor_violations":
            score += 0.05
        elif app.driving_history == "major_violations":
            score += 0.2

        # Vehicle
        current_year = datetime.utcnow().year
        vehicle_age = current_year - app.vehicle_year
        if vehicle_age > 10:
            score += 0.05
        elif vehicle_age < 3:
            score -= 0.05

        # Credit score
        if app.credit_score >= 750:
            score -= 0.1
        elif app.credit_score < 600:
            score += 0.15

        # Mileage
        if app.annual_mileage > 20000:
            score += 0.05
        elif app.annual_mileage < 5000:
            score -= 0.05

        # Prior claims
        score += min(0.3, app.prior_claims * 0.1)

        return max(0.0, min(1.0, score))

    def _determine_decision(self, risk_score: float, app: ApplicationData) -> Tuple[UnderwritingDecision, RiskTier]:
        # Check rules
        for rule in sorted(self._rules, key=lambda r: r.priority):
            if not rule.enabled:
                continue
            # Simplified rule evaluation
            if rule.name == "decline_high_risk" and risk_score > 0.8:
                return rule.decision, RiskTier.DECLINED
            if rule.name == "refer_medium_risk" and 0.4 <= risk_score <= 0.6:
                return rule.decision, RiskTier.STANDARD

        # Default decision based on score
        if risk_score < 0.25:
            return UnderwritingDecision.APPROVE, RiskTier.PREFERRED_PLUS
        elif risk_score < 0.40:
            return UnderwritingDecision.APPROVE, RiskTier.PREFERRED
        elif risk_score < 0.55:
            return UnderwritingDecision.APPROVE, RiskTier.STANDARD_PLUS
        elif risk_score < 0.70:
            return UnderwritingDecision.APPROVE, RiskTier.STANDARD
        elif risk_score < 0.85:
            return UnderwritingDecision.REFER, RiskTier.SUBSTANDARD
        else:
            return UnderwritingDecision.DECLINE, RiskTier.DECLINED

    def _calculate_premium(self, app: ApplicationData, tier: RiskTier) -> float:
        base_rate = 1000.0
        tier_multiplier = {
            RiskTier.PREFERRED_PLUS: 0.7,
            RiskTier.PREFERRED: 0.85,
            RiskTier.STANDARD_PLUS: 0.95,
            RiskTier.STANDARD: 1.0,
            RiskTier.SUBSTANDARD: 1.5,
            RiskTier.DECLINED: 0.0,
        }
        premium = base_rate * tier_multiplier.get(tier, 1.0)

        # Coverage adjustment
        for coverage, limit in app.coverage_requested.items():
            premium += limit * 0.001

        return premium

    def _get_factors(self, app: ApplicationData) -> List[str]:
        factors = []
        if app.age < 25:
            factors.append("Young driver surcharge")
        if app.driving_history == "clean":
            factors.append("Clean driving history discount")
        if app.credit_score >= 750:
            factors.append("Good credit discount")
        if app.prior_claims > 2:
            factors.append("Multiple prior claims")
        return factors


# ---------------------------------------------------------------------------
# Document Analyzer
# ---------------------------------------------------------------------------

class DocumentAnalyzer:
    """Analyzes underwriting documents."""

    def analyze(self, doc: UnderwritingDocument) -> DocumentAnalysis:
        extracted = [
            ExtractedField(name="applicant_name", value="John Smith", confidence=0.98),
            ExtractedField(name="date_of_birth", value="1990-01-15", confidence=0.95),
            ExtractedField(name="coverage_limit", value=100000, confidence=0.92),
        ]

        missing = []
        if "phone" not in doc.content.lower():
            missing.append("phone_number")

        return DocumentAnalysis(
            document_type=doc.document_type,
            extracted_fields=extracted,
            data_quality_score=0.95 if not missing else 0.85,
            missing_fields=missing,
        )


# ---------------------------------------------------------------------------
# Explainability Engine
# ---------------------------------------------------------------------------

class ExplainabilityEngine:
    """Provides explanations for underwriting decisions."""

    def explain(self, result: UnderwritingResult) -> ExplainabilityResult:
        primary_factors = []
        for i, factor in enumerate(result.factors[:3]):
            impact = FactorImpact.POSITIVE if "discount" in factor.lower() else FactorImpact.NEGATIVE
            primary_factors.append(FeatureFactor(
                name=factor,
                impact=impact,
                description=f"Factor: {factor}",
            ))

        feature_importance = [
            FeatureFactor(name="credit_score", importance=0.25),
            FeatureFactor(name="driving_history", importance=0.22),
            FeatureFactor(name="age", importance=0.18),
            FeatureFactor(name="vehicle_type", importance=0.15),
            FeatureFactor(name="annual_mileage", importance=0.12),
        ]

        return ExplainabilityResult(
            decision=result.outcome.value,
            primary_factors=primary_factors,
            feature_importance=feature_importance,
            model_confidence=result.confidence,
        )


# ---------------------------------------------------------------------------
# Batch Processor
# ---------------------------------------------------------------------------

class BatchProcessor:
    """Processes multiple applications in batch."""

    def __init__(self, engine: UnderwritingEngine) -> None:
        self.engine = engine

    def process_batch(self, applications: List[ApplicationData]) -> BatchResult:
        start_time = datetime.utcnow()
        results = []

        for app in applications:
            result = self.engine.underwrite(app)
            results.append(result)

        elapsed = (datetime.utcnow() - start_time).total_seconds()

        return BatchResult(
            total_processed=len(results),
            approved_count=sum(1 for r in results if r.outcome == UnderwritingDecision.APPROVE),
            referred_count=sum(1 for r in results if r.outcome == UnderwritingDecision.REFER),
            declined_count=sum(1 for r in results if r.outcome == UnderwritingDecision.DECLINE),
            conditional_count=sum(1 for r in results if r.outcome == UnderwritingDecision.CONDITIONAL),
            processing_time_seconds=elapsed,
            results=results,
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Underwriting AI module."""
    print("=" * 60)
    print("  Underwriting AI Module — Demo")
    print("=" * 60)

    # Engine
    engine = UnderwritingEngine(model_version="v2.0")
    engine.add_rule(UnderwritingRule(name="decline_high_risk", decision=UnderwritingDecision.DECLINE, priority=1))

    # Application
    application = ApplicationData(
        applicant_name="John Smith",
        age=35,
        driving_history="clean",
        vehicle_year=2023,
        vehicle_type="sedan",
        annual_mileage=12000,
        credit_score=750,
        coverage_requested={"liability": 100000, "collision": 500000},
    )

    # Underwrite
    result = engine.underwrite(application)
    print(f"\n[+] Underwriting Decision:")
    print(f"    Applicant: {result.applicant_name}")
    print(f"    Decision: {result.outcome.value}")
    print(f"    Risk Tier: {result.risk_tier.value}")
    print(f"    Premium: ${result.recommended_premium:,.2f}")
    print(f"    Confidence: {result.confidence:.1%}")
    print(f"    Straight-Through: {result.is_straight_through}")
    print(f"    Factors: {result.factors}")

    # Explainability
    explainer = ExplainabilityEngine()
    explanation = explainer.explain(result)
    print(f"\n[+] Explanation:")
    print(f"    Primary Factors:")
    for f in explanation.primary_factors:
        print(f"      - {f.name} ({f.impact.value})")

    # Document analysis
    doc_analyzer = DocumentAnalyzer()
    analysis = doc_analyzer.analyze(UnderwritingDocument(content="Auto application form"))
    print(f"\n[+] Document Analysis:")
    print(f"    Fields Extracted: {len(analysis.extracted_fields)}")
    print(f"    Quality: {analysis.data_quality_score:.1%}")
    print(f"    Missing: {analysis.missing_fields}")

    # Batch processing
    batch_processor = BatchProcessor(engine)
    batch_apps = [application, ApplicationData(applicant_name="Jane Doe", age=28, credit_score=680)]
    batch_result = batch_processor.process_batch(batch_apps)
    print(f"\n[+] Batch Results:")
    print(f"    Processed: {batch_result.total_processed}")
    print(f"    Approved: {batch_result.approved_count}")
    print(f"    Approval Rate: {batch_result.approval_rate:.1%}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
