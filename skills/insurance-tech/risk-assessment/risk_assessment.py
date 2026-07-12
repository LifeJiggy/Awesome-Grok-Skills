"""
Risk Assessment Module
Insurance risk scoring, modeling, and portfolio analysis
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class InsuranceLine(Enum):
    AUTO = "auto"
    PROPERTY = "property"
    HEALTH = "health"
    LIABILITY = "liability"
    LIFE = "life"
    UMBRELLA = "umbrella"
    WORKERS_COMP = "workers_comp"


class RiskTier(Enum):
    PREFERRED_PLUS = "preferred_plus"
    PREFERRED = "preferred"
    STANDARD_PLUS = "standard_plus"
    STANDARD = "standard"
    SUBSTANDARD = "substandard"
    DECLINED = "declined"


class CatastropheType(Enum):
    HURRICANE = "hurricane"
    EARTHQUAKE = "earthquake"
    FLOOD = "flood"
    WILDFIRE = "wildfire"
    TORNADO = "tornado"
    HAIL = "hail"


class RiskFactorCategory(Enum):
    DEMOGRAPHIC = "demographic"
    BEHAVIORAL = "behavioral"
    ENVIRONMENTAL = "environmental"
    FINANCIAL = "financial"
    VEHICLE = "vehicle"
    PROPERTY = "property"
    HEALTH = "health"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class RiskFactor:
    """Individual risk factor."""
    name: str
    value: Any
    weight: float = 1.0
    category: RiskFactorCategory = RiskFactorCategory.DEMOGRAPHIC
    impact: float = 0.0  # -1.0 to 1.0, negative = lower risk

    @property
    def weighted_impact(self) -> float:
        return self.impact * self.weight


@dataclass
class RiskProfile:
    """Risk profile for an applicant."""
    applicant_id: str = ""
    insurance_line: InsuranceLine = InsuranceLine.AUTO
    factors: List[RiskFactor] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskResult:
    """Result of risk assessment."""
    applicant_id: str = ""
    score: float = 0.0  # 0.0 (low risk) to 1.0 (high risk)
    tier: RiskTier = RiskTier.STANDARD
    confidence: float = 0.85
    top_factors: List[Tuple[str, float]] = field(default_factory=list)
    calculated_at: datetime = field(default_factory=datetime.utcnow)
    model_version: str = "v1.0"

    @property
    def risk_percentage(self) -> float:
        return self.score * 100


@dataclass
class Policy:
    """Policy for portfolio analysis."""
    policy_id: str = ""
    line: str = "auto"
    premium: float = 0.0
    risk_score: float = 0.0
    exposure: float = 0.0
    effective_date: str = ""
    expiration_date: str = ""


@dataclass
class PortfolioAnalysis:
    """Portfolio risk analysis result."""
    total_policies: int = 0
    total_premium: float = 0.0
    total_exposure: float = 0.0
    avg_risk_score: float = 0.0
    max_risk_score: float = 0.0
    concentration_risk: str = "low"
    diversification_score: float = 0.0
    line_distribution: Dict[str, int] = field(default_factory=dict)
    risk_distribution: Dict[str, int] = field(default_factory=dict)


@dataclass
class PropertyRisk:
    """Property risk details."""
    property_id: str = ""
    location: str = ""
    property_type: str = "residential"
    construction_type: str = "frame"
    year_built: int = 2000
    replacement_value: float = 0.0
    features: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CatastropheRisk:
    """Catastrophe risk assessment."""
    property_id: str = ""
    hurricane_risk: str = "low"
    flood_risk: str = "low"
    earthquake_risk: str = "low"
    wildfire_risk: str = "low"
    tornado_risk: str = "low"
    expected_annual_loss: float = 0.0
    probability_of_loss: float = 0.0
    maximum_loss: float = 0.0


@dataclass
class RiskThreshold:
    """Threshold for risk tier assignment."""
    tier: RiskTier
    min_score: float
    max_score: float


# ---------------------------------------------------------------------------
# Risk Engine
# ---------------------------------------------------------------------------

class RiskEngine:
    """Main risk assessment engine."""

    TIER_THRESHOLDS = [
        RiskThreshold(RiskTier.PREFERRED_PLUS, 0.0, 0.15),
        RiskThreshold(RiskTier.PREFERRED, 0.15, 0.30),
        RiskThreshold(RiskTier.STANDARD_PLUS, 0.30, 0.45),
        RiskThreshold(RiskTier.STANDARD, 0.45, 0.65),
        RiskThreshold(RiskTier.SUBSTANDARD, 0.65, 0.85),
        RiskThreshold(RiskTier.DECLINED, 0.85, 1.01),
    ]

    def __init__(self, model_version: str = "v1.0") -> None:
        self.model_version = model_version
        self._factor_weights: Dict[str, float] = {}

    def calculate_risk(self, profile: RiskProfile) -> RiskResult:
        if not profile.factors:
            return RiskResult(
                applicant_id=profile.applicant_id,
                score=0.5,
                tier=RiskTier.STANDARD,
                confidence=0.5,
            )

        # Calculate weighted risk score
        total_weight = sum(f.weight for f in profile.factors)
        if total_weight == 0:
            total_weight = 1.0

        weighted_sum = sum(f.weighted_impact for f in profile.factors)
        normalized_score = (weighted_sum / total_weight + 1.0) / 2.0  # Normalize to 0-1
        score = max(0.0, min(1.0, normalized_score))

        # Determine tier
        tier = self._score_to_tier(score)

        # Calculate confidence
        confidence = min(1.0, 0.7 + len(profile.factors) * 0.03)

        # Get top factors
        top_factors = sorted(
            [(f.name, f.weighted_impact) for f in profile.factors],
            key=lambda x: abs(x[1]),
            reverse=True,
        )[:5]

        return RiskResult(
            applicant_id=profile.applicant_id,
            score=score,
            tier=tier,
            confidence=confidence,
            top_factors=top_factors,
            model_version=self.model_version,
        )

    def _score_to_tier(self, score: float) -> RiskTier:
        for threshold in self.TIER_THRESHOLDS:
            if threshold.min_score <= score < threshold.max_score:
                return threshold.tier
        return RiskTier.SUBSTANDARD

    def batch_assess(self, profiles: List[RiskProfile]) -> List[RiskResult]:
        return [self.calculate_risk(p) for p in profiles]


# ---------------------------------------------------------------------------
# Portfolio Analyzer
# ---------------------------------------------------------------------------

class PortfolioAnalyzer:
    """Analyzes insurance portfolio risk."""

    def __init__(self) -> None:
        self._policies: List[Policy] = []

    def add_policy(self, policy: Policy) -> None:
        self._policies.append(policy)

    def analyze_portfolio(self) -> PortfolioAnalysis:
        if not self._policies:
            return PortfolioAnalysis()

        total_premium = sum(p.premium for p in self._policies)
        total_exposure = sum(p.exposure for p in self._policies)
        risk_scores = [p.risk_score for p in self._policies]
        avg_risk = sum(risk_scores) / len(risk_scores)

        # Line distribution
        line_dist: Dict[str, int] = {}
        for p in self._policies:
            line_dist[p.line] = line_dist.get(p.line, 0) + 1

        # Risk distribution
        risk_dist: Dict[str, int] = {"low": 0, "medium": 0, "high": 0}
        for score in risk_scores:
            if score < 0.3:
                risk_dist["low"] += 1
            elif score < 0.6:
                risk_dist["medium"] += 1
            else:
                risk_dist["high"] += 1

        # Concentration risk
        concentration = "low"
        if len(self._policies) > 0:
            max_line_pct = max(line_dist.values()) / len(self._policies)
            if max_line_pct > 0.7:
                concentration = "high"
            elif max_line_pct > 0.5:
                concentration = "medium"

        # Diversification score (0-1)
        num_lines = len(line_dist)
        diversification = min(1.0, num_lines / 5.0)

        return PortfolioAnalysis(
            total_policies=len(self._policies),
            total_premium=total_premium,
            total_exposure=total_exposure,
            avg_risk_score=avg_risk,
            max_risk_score=max(risk_scores),
            concentration_risk=concentration,
            diversification_score=diversification,
            line_distribution=line_dist,
            risk_distribution=risk_dist,
        )


# ---------------------------------------------------------------------------
# Catastrophe Assessor
# ---------------------------------------------------------------------------

class CatastropheAssessor:
    """Assesses catastrophe risk for properties."""

    LOCATION_RISK = {
        "miami, fl": {"hurricane": "high", "flood": "high", "earthquake": "low", "wildfire": "low"},
        "san francisco, ca": {"hurricane": "low", "flood": "low", "earthquake": "high", "wildfire": "medium"},
        "denver, co": {"hurricane": "low", "flood": "low", "earthquake": "low", "wildfire": "medium"},
        "los angeles, ca": {"hurricane": "low", "flood": "low", "earthquake": "high", "wildfire": "high"},
        "houston, tx": {"hurricane": "high", "flood": "high", "earthquake": "low", "wildfire": "low"},
        "seattle, wa": {"hurricane": "low", "flood": "medium", "earthquake": "medium", "wildfire": "low"},
    }

    def assess(self, property_risk: PropertyRisk) -> CatastropheRisk:
        location_key = property_risk.location.lower()
        risk_data = self.LOCATION_RISK.get(location_key, {
            "hurricane": "low", "flood": "low", "earthquake": "low", "wildfire": "low",
        })

        # Calculate expected annual loss
        base_loss_pct = {"low": 0.001, "medium": 0.01, "high": 0.05}
        expected_loss_pct = sum(base_loss_pct.get(r, 0.001) for r in risk_data.values()) / len(risk_data)
        expected_loss = property_risk.replacement_value * expected_loss_pct

        # Age factor
        age_factor = max(1.0, (2024 - property_risk.year_built) / 100)

        return CatastropheRisk(
            property_id=property_risk.property_id,
            hurricane_risk=risk_data.get("hurricane", "low"),
            flood_risk=risk_data.get("flood", "low"),
            earthquake_risk=risk_data.get("earthquake", "low"),
            wildfire_risk=risk_data.get("wildfire", "low"),
            expected_annual_loss=expected_loss * age_factor,
            probability_of_loss=expected_loss_pct,
            maximum_loss=property_risk.replacement_value,
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Risk Assessment module."""
    print("=" * 60)
    print("  Risk Assessment Module — Demo")
    print("=" * 60)

    # Risk scoring
    engine = RiskEngine(model_version="v2.1")
    profile = RiskProfile(
        applicant_id="APP-001",
        insurance_line=InsuranceLine.AUTO,
        factors=[
            RiskFactor(name="age", value=35, weight=0.15, impact=0.2),
            RiskFactor(name="driving_history", value="clean", weight=0.25, impact=0.4),
            RiskFactor(name="vehicle_type", value="sedan", weight=0.20, impact=0.1),
            RiskFactor(name="annual_mileage", value=12000, weight=0.15, impact=-0.1),
            RiskFactor(name="credit_score", value=750, weight=0.15, impact=0.3),
        ],
    )
    result = engine.calculate_risk(profile)
    print(f"\n[+] Individual Risk Assessment:")
    print(f"    Applicant: {result.applicant_id}")
    print(f"    Risk Score: {result.score:.3f} ({result.risk_percentage:.1f}%)")
    print(f"    Tier: {result.tier.value}")
    print(f"    Confidence: {result.confidence:.1%}")
    print(f"    Top Factors: {result.top_factors}")

    # Portfolio analysis
    analyzer = PortfolioAnalyzer()
    policies = [
        Policy(policy_id="POL-001", line="auto", premium=1200, risk_score=0.35, exposure=50000),
        Policy(policy_id="POL-002", line="property", premium=2400, risk_score=0.60, exposure=250000),
        Policy(policy_id="POL-003", line="auto", premium=800, risk_score=0.25, exposure=30000),
        Policy(policy_id="POL-004", line="liability", premium=1500, risk_score=0.45, exposure=100000),
    ]
    for p in policies:
        analyzer.add_policy(p)

    analysis = analyzer.analyze_portfolio()
    print(f"\n[+] Portfolio Analysis:")
    print(f"    Total Policies: {analysis.total_policies}")
    print(f"    Total Premium: ${analysis.total_premium:,.2f}")
    print(f"    Avg Risk Score: {analysis.avg_risk_score:.3f}")
    print(f"    Concentration: {analysis.concentration_risk}")
    print(f"    Diversification: {analysis.diversification_score:.2f}")
    print(f"    Line Distribution: {analysis.line_distribution}")
    print(f"    Risk Distribution: {analysis.risk_distribution}")

    # Catastrophe assessment
    cat_assessor = CatastropheAssessor()
    property_risk = PropertyRisk(
        property_id="PROP-001",
        location="Miami, FL",
        property_type="residential",
        year_built=2005,
        replacement_value=350000,
    )
    cat_risk = cat_assessor.assess(property_risk)
    print(f"\n[+] Catastrophe Risk (Miami, FL):")
    print(f"    Hurricane: {cat_risk.hurricane_risk}")
    print(f"    Flood: {cat_risk.flood_risk}")
    print(f"    Earthquake: {cat_risk.earthquake_risk}")
    print(f"    Wildfire: {cat_risk.wildfire_risk}")
    print(f"    Expected Annual Loss: ${cat_risk.expected_annual_loss:,.2f}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
