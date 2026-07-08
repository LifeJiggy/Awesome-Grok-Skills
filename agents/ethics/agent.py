"""Ethics Agent — Ethical AI governance, bias detection, and fairness frameworks.

Covers bias detection across multiple protected attributes, fairness metric
calculation, compliance framework management, transparency documentation,
accountability tracking, audit trail management, model risk assessment,
explainability, and governance policy enforcement.
"""

import logging
import hashlib
import uuid
import statistics
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, Tuple, Union
from uuid import uuid4

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class BiasType(Enum):
    """Protected attributes for bias detection."""
    GENDER = "gender"
    RACE = "race"
    AGE = "age"
    SOCIOECONOMIC = "socioeconomic"
    RELIGIOUS = "religious"
    DISABILITY = "disability"
    GEOGRAPHIC = "geographic"
    ETHNICITY = "ethnicity"
    NATIONAL_ORIGIN = "national_origin"
    SEXUAL_ORIENTATION = "sexual_orientation"
    MARITAL_STATUS = "marital_status"
    VETERAN_STATUS = "veteran_status"


class FairnessDefinition(Enum):
    """Formal fairness definitions."""
    DEMOGRAPHIC_PARITY = "demographic_parity"
    EQUALIZED_ODDS = "equalized_odds"
    EQUAL_OPPORTUNITY = "equal_opportunity"
    PREDICTIVE_PARITY = "predictive_parity"
    CALIBRATION = "calibration"
    INDIVIDUAL_FAIRNESS = "individual_fairness"
    COUNTERFACTUAL_FAIRNESS = "counterfactual_fairness"
    PROCEDURAL_FAIRNESS = "procedural_fairness"


class RiskLevel(Enum):
    """Ethical risk classification."""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    EU_AI_ACT = "eu_ai_act"
    GDPR = "gdpr"
    CCPA = "ccpa"
    NIST_AI_RMF = "nist_ai_rmf"
    ISO_42001 = "iso_42001"
    IEEE_ETHICALLY_ALIGNED = "ieee_ethically_aligned"
    OECD_AI_PRINCIPLES = "oecd_ai_principles"
    AI_RISK_MANAGEMENT = "ai_risk_management"
    SECTION_230 = "section_230"
    HIPAA = "hipaa"
    SOX = "sox"
    CUSTOM = "custom"


class TransparencyLevel(Enum):
    """Levels of model transparency."""
    BLACK_BOX = "black_box"
    LIMITED = "limited"
    PARTIAL = "partial"
    FULL = "full"
    EXPLAINABLE = "explainable"


class AccountabilityRole(Enum):
    """Roles in AI accountability chain."""
    MODEL_OWNER = "model_owner"
    DATA_SCIENTIST = "data_scientist"
    PRODUCT_MANAGER = "product_manager"
    ETHICS_COMMITTEE = "ethics_committee"
    END_USER = "end_user"
    EXTERNAL_AUDITOR = "external_auditor"
    REGULATOR = "regulator"


class AuditType(Enum):
    """Types of ethical audits."""
    PRE_DEPLOYMENT = "pre_deployment"
    POST_DEPLOYMENT = "post_deployment"
    PERIODIC = "periodic"
    INCIDENT_RESPONSE = "incident_response"
    AD_HOC = "ad_hoc"
    CONTINUOUS = "continuous"


class IncidentSeverity(Enum):
    """Severity of ethical incidents."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MitigationStrategy(Enum):
    """Bias mitigation approaches."""
    PRE_PROCESSING = "pre_processing"
    IN_PROCESSING = "in_processing"
    POST_PROCESSING = "post_processing"
    DATA_REWEIGHTING = "data_reweighting"
    FEATURE_TRANSFORMATION = "feature_transformation"
    ADVERSarial_DEBIASING = "adversarial_debiasing"
    THRESHOLD_ADJUSTMENT = "threshold_adjustment"
    ENSEMBLE = "ensemble"


class DocumentType(Enum):
    """Types of transparency documentation."""
    MODEL_CARD = "model_card"
    DATASHEET = "datasheet"
    IMPACT_ASSESSMENT = "impact_assessment"
    AUDIT_REPORT = "audit_report"
    INCIDENT_REPORT = "incident_report"
    POLICY_DOCUMENT = "policy_document"
    TRAINING_MATERIAL = "training_material"
    PUBLIC_DISCLOSURE = "public_disclosure"


class GovernanceStatus(Enum):
    """Status of governance actions."""
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    MONITORING = "monitoring"
    RETIRED = "retired"
    REJECTED = "rejected"


class ProtectedAttribute:
    """Represents a protected attribute with allowed values."""

    STANDARD_ATTRIBUTES: Dict[BiasType, List[str]] = {
        BiasType.GENDER: ["male", "female", "non_binary", "unknown"],
        BiasType.RACE: ["white", "black", "hispanic", "asian", "other", "unknown"],
        BiasType.AGE: ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        BiasType.DISABILITY: ["none", "visual", "hearing", "motor", "cognitive", "unknown"],
        BiasType.GEOGRAPHIC: ["urban", "suburban", "rural", "unknown"],
    }


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ModelPrediction:
    """A single model prediction with protected attributes."""
    prediction_id: str = field(default_factory=lambda: str(uuid4()))
    input_id: str = ""
    predicted_label: int = 0
    actual_label: Optional[int] = None
    confidence: float = 0.0
    protected_attributes: Dict[str, str] = field(default_factory=dict)
    features: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    model_version: str = ""

    @property
    def is_correct(self) -> Optional[bool]:
        if self.actual_label is None:
            return None
        return self.predicted_label == self.actual_label

    @property
    def is_positive_prediction(self) -> bool:
        return self.predicted_label == 1

    @property
    def is_positive_actual(self) -> Optional[bool]:
        if self.actual_label is None:
            return None
        return self.actual_label == 1


@dataclass
class BiasAnalysisResult:
    """Result of a bias analysis on a set of predictions."""
    analysis_id: str = field(default_factory=lambda: str(uuid4()))
    bias_type: BiasType = BiasType.GENDER
    bias_score: float = 0.0
    threshold: float = 0.1
    is_flagged: bool = False
    group_rates: Dict[str, float] = field(default_factory=dict)
    sample_sizes: Dict[str, int] = field(default_factory=dict)
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    statistical_significance: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.now)

    @property
    def max_group_rate(self) -> float:
        return max(self.group_rates.values()) if self.group_rates else 0

    @property
    def min_group_rate(self) -> float:
        return min(self.group_rates.values()) if self.group_rates else 0

    @property
    def rate_disparity(self) -> float:
        return self.max_group_rate - self.min_group_rate


@dataclass
class FairnessMetricResult:
    """Result of a fairness metric calculation."""
    metric_id: str = field(default_factory=lambda: str(uuid4()))
    definition: FairnessDefinition = FairnessDefinition.DEMOGRAPHIC_PARITY
    value: float = 0.0
    is_fair: bool = True
    threshold: float = 0.1
    group_values: Dict[str, float] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)
    calculated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ComplianceRequirement:
    """A single compliance requirement."""
    requirement_id: str = field(default_factory=lambda: str(uuid4()))
    framework: ComplianceFramework = ComplianceFramework.EU_AI_ACT
    title: str = ""
    description: str = ""
    is_mandatory: bool = True
    status: GovernanceStatus = GovernanceStatus.PROPOSED
    evidence: List[str] = field(default_factory=list)
    responsible_role: AccountabilityRole = AccountabilityRole.MODEL_OWNER
    deadline: Optional[datetime] = None
    last_verified: Optional[datetime] = None
    is_compliant: Optional[bool] = None

    @property
    def is_overdue(self) -> bool:
        if not self.deadline:
            return False
        return datetime.now() > self.deadline


@dataclass
class EthicsIncident:
    """A recorded ethics incident."""
    incident_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    severity: IncidentSeverity = IncidentSeverity.LOW
    bias_type: Optional[BiasType] = None
    affected_groups: List[str] = field(default_factory=list)
    model_id: Optional[str] = None
    detected_at: datetime = field(default_factory=datetime.now)
    reported_by: str = ""
    status: str = "open"
    root_cause: str = ""
    mitigation_actions: List[str] = field(default_factory=list)
    resolved_at: Optional[datetime] = None
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class ModelRiskAssessment:
    """Risk assessment for an AI model."""
    assessment_id: str = field(default_factory=lambda: str(uuid4()))
    model_id: str = ""
    model_name: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    risk_score: float = 0.0
    risk_factors: List[Dict[str, Any]] = field(default_factory=list)
    impact_areas: List[str] = field(default_factory=list)
    bias_findings: List[BiasAnalysisResult] = field(default_factory=list)
    compliance_status: Dict[str, bool] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    assessed_at: datetime = field(default_factory=datetime.now)
    next_assessment: Optional[datetime] = None


@dataclass
class TransparencyDocument:
    """A transparency or documentation artifact."""
    document_id: str = field(default_factory=lambda: str(uuid4()))
    document_type: DocumentType = DocumentType.MODEL_CARD
    title: str = ""
    content: str = ""
    model_id: Optional[str] = None
    version: str = "1.0"
    author: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    is_public: bool = False
    approved_by: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    @property
    def is_approved(self) -> bool:
        return self.approved_by is not None


@dataclass
class AccountabilityEntry:
    """An entry in the accountability chain."""
    entry_id: str = field(default_factory=lambda: str(uuid4()))
    model_id: str = ""
    role: AccountabilityRole = AccountabilityRole.MODEL_OWNER
    person_name: str = ""
    person_email: str = ""
    responsibility: str = ""
    assigned_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    sign_off_date: Optional[datetime] = None


@dataclass
class GovernancePolicy:
    """A governance policy or guideline."""
    policy_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    category: str = ""
    status: GovernanceStatus = GovernanceStatus.PROPOSED
    version: str = "1.0"
    effective_date: Optional[datetime] = None
    review_date: Optional[datetime] = None
    owner: str = ""
    applicable_frameworks: List[ComplianceFramework] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def is_effective(self) -> bool:
        if not self.effective_date:
            return False
        return datetime.now() >= self.effective_date and self.status == GovernanceStatus.IMPLEMENTED


@dataclass
class AuditRecord:
    """A completed audit record."""
    audit_id: str = field(default_factory=lambda: str(uuid4()))
    audit_type: AuditType = AuditType.PRE_DEPLOYMENT
    model_id: str = ""
    auditor: str = ""
    findings: List[Dict[str, Any]] = field(default_factory=list)
    overall_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    compliant: bool = True
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    next_audit_date: Optional[datetime] = None
    recommendations: List[str] = field(default_factory=list)
    status: str = "in_progress"


@dataclass
class ExplainabilityResult:
    """Model explainability analysis."""
    result_id: str = field(default_factory=lambda: str(uuid4()))
    model_id: str = ""
    prediction_id: str = ""
    method: str = "shap"
    feature_importance: Dict[str, float] = field(default_factory=dict)
    top_features: List[Tuple[str, float]] = field(default_factory=list)
    explanation_text: str = ""
    confidence: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)


# ---------------------------------------------------------------------------
# Core Engine Classes
# ---------------------------------------------------------------------------

class BiasDetector:
    """Detects bias across protected attributes using statistical methods."""

    def __init__(self) -> None:
        self._thresholds: Dict[str, float] = {
            bt.value: 0.1 for bt in BiasType
        }
        self._analysis_history: List[BiasAnalysisResult] = []
        logger.info("BiasDetector initialized")

    def set_threshold(self, bias_type: BiasType, threshold: float) -> None:
        self._thresholds[bias_type.value] = threshold

    def get_threshold(self, bias_type: BiasType) -> float:
        return self._thresholds.get(bias_type.value, 0.1)

    def analyze_predictions(
        self,
        predictions: List[ModelPrediction],
        protected_attributes: List[str],
        outcome_attr: str = "predicted_label",
    ) -> Dict[str, BiasAnalysisResult]:
        results: Dict[str, BiasAnalysisResult] = {}
        for attr_name in protected_attributes:
            group_data: Dict[str, Dict[str, int]] = {}
            for pred in predictions:
                group = pred.protected_attributes.get(attr_name, "unknown")
                if group not in group_data:
                    group_data[group] = {"positive": 0, "total": 0}
                group_data[group]["total"] += 1
                if pred.is_positive_prediction:
                    group_data[group]["positive"] += 1
            rates = {
                g: d["positive"] / d["total"] if d["total"] > 0 else 0
                for g, d in group_data.items()
            }
            sample_sizes = {g: d["total"] for g, d in group_data.items()}
            max_rate = max(rates.values()) if rates else 0
            min_rate = min(rates.values()) if rates else 0
            bias_score = max_rate - min_rate
            threshold = self._thresholds.get(attr_name, 0.1)
            is_flagged = bias_score > threshold
            ci = self._calculate_confidence_interval(predictions, attr_name)
            p_value = self._calculate_significance(predictions, attr_name)
            recommendations = self._generate_recommendations(
                attr_name, bias_score, is_flagged, rates
            )
            result = BiasAnalysisResult(
                bias_type=BiasType(attr_name) if attr_name in [bt.value for bt in BiasType] else BiasType.GENDER,
                bias_score=round(bias_score, 4),
                threshold=threshold,
                is_flagged=is_flagged,
                group_rates={g: round(r, 4) for g, r in rates.items()},
                sample_sizes=sample_sizes,
                confidence_interval=ci,
                statistical_significance=p_value,
                recommendations=recommendations,
            )
            results[attr_name] = result
            self._analysis_history.append(result)
        return results

    def analyze_single_attribute(
        self,
        predictions: List[ModelPrediction],
        attribute: str,
    ) -> BiasAnalysisResult:
        results = self.analyze_predictions(predictions, [attribute])
        return results.get(attribute, BiasAnalysisResult())

    def get_analysis_history(
        self, bias_type: Optional[BiasType] = None
    ) -> List[BiasAnalysisResult]:
        if bias_type:
            return [r for r in self._analysis_history if r.bias_type == bias_type]
        return list(self._analysis_history)

    def get_flagged_attributes(self) -> List[BiasAnalysisResult]:
        return [r for r in self._analysis_history if r.is_flagged]

    def _calculate_confidence_interval(
        self,
        predictions: List[ModelPrediction],
        attribute: str,
        confidence: float = 0.95,
    ) -> Tuple[float, float]:
        rates = []
        group_data: Dict[str, List[int]] = {}
        for pred in predictions:
            group = pred.protected_attributes.get(attribute, "unknown")
            if group not in group_data:
                group_data[group] = []
            group_data[group].append(1 if pred.is_positive_prediction else 0)
        for group, outcomes in group_data.items():
            if outcomes:
                rates.append(sum(outcomes) / len(outcomes))
        if not rates:
            return (0.0, 0.0)
        mean_rate = statistics.mean(rates)
        if len(rates) < 2:
            return (mean_rate, mean_rate)
        std_err = statistics.stdev(rates) / math.sqrt(len(rates))
        margin = 1.96 * std_err
        return (max(0, mean_rate - margin), min(1, mean_rate + margin))

    def _calculate_significance(
        self,
        predictions: List[ModelPrediction],
        attribute: str,
    ) -> float:
        group_outcomes: Dict[str, List[int]] = {}
        for pred in predictions:
            group = pred.protected_attributes.get(attribute, "unknown")
            if group not in group_outcomes:
                group_outcomes[group] = []
            group_outcomes[group].append(1 if pred.is_positive_prediction else 0)
        groups = list(group_outcomes.values())
        if len(groups) < 2 or not all(g for g in groups):
            return 1.0
        try:
            import scipy.stats as stats
            f_stat, p_value = stats.f_oneway(*groups)
            return p_value
        except ImportError:
            return 1.0

    def _generate_recommendations(
        self,
        attribute: str,
        bias_score: float,
        is_flagged: bool,
        rates: Dict[str, float],
    ) -> List[str]:
        recs: List[str] = []
        if is_flagged:
            recs.append(f"Bias detected in {attribute}: disparity of {bias_score:.3f}")
            recs.append(f"Review {attribute} representation in training data")
            recs.append(f"Consider re-sampling to balance {attribute} groups")
            recs.append("Apply fairness constraints during training")
            min_group = min(rates, key=rates.get)
            max_group = max(rates, key=rates.get)
            recs.append(
                f"Group '{min_group}' has {rates[min_group]:.1%} positive rate "
                f"vs '{max_group}' at {rates[max_group]:.1%}"
            )
        else:
            recs.append(f"No significant bias detected in {attribute}")
        return recs


import math


class FairnessMetrics:
    """Calculates formal fairness metrics across multiple definitions."""

    def __init__(self) -> None:
        self._results: List[FairnessMetricResult] = []
        logger.info("FairnessMetrics initialized")

    def calculate_demographic_parity(
        self,
        predictions: List[ModelPrediction],
        protected_attr: str,
        threshold: float = 0.1,
    ) -> FairnessMetricResult:
        group_positive: Dict[str, int] = {}
        group_total: Dict[str, int] = {}
        for pred in predictions:
            group = pred.protected_attributes.get(protected_attr, "unknown")
            group_total[group] = group_total.get(group, 0) + 1
            if pred.is_positive_prediction:
                group_positive[group] = group_positive.get(group, 0) + 1
        rates = {
            g: group_positive.get(g, 0) / group_total[g]
            for g in group_total
            if group_total[g] > 0
        }
        overall_rate = (
            sum(group_positive.values()) / max(sum(group_total.values()), 1)
        )
        disparities = {
            g: abs(rate - overall_rate) / max(overall_rate, 0.001)
            for g, rate in rates.items()
        }
        max_disparity = max(disparities.values()) if disparities else 0
        result = FairnessMetricResult(
            definition=FairnessDefinition.DEMOGRAPHIC_PARITY,
            value=round(max_disparity, 4),
            is_fair=max_disparity <= threshold,
            threshold=threshold,
            group_values={g: round(r, 4) for g, r in rates.items()},
            details={"overall_rate": round(overall_rate, 4), "disparities": disparities},
        )
        self._results.append(result)
        return result

    def calculate_equalized_odds(
        self,
        predictions: List[ModelPrediction],
        protected_attr: str,
        threshold: float = 0.1,
    ) -> FairnessMetricResult:
        group_tpr: Dict[str, float] = {}
        group_fpr: Dict[str, float] = {}
        for group in set(p.protected_attributes.get(protected_attr, "unknown") for p in predictions):
            group_preds = [p for p in predictions if p.protected_attributes.get(protected_attr) == group]
            tp = sum(1 for p in group_preds if p.is_positive_prediction and p.is_positive_actual)
            fn = sum(1 for p in predictions if not p.is_positive_prediction and p.is_positive_actual)
            fp = sum(1 for p in group_preds if p.is_positive_prediction and not p.is_positive_actual)
            tn = sum(1 for p in group_preds if not p.is_positive_prediction and not p.is_positive_actual)
            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            group_tpr[group] = tpr
            group_fpr[group] = fpr
        tpr_disparity = max(group_tpr.values()) - min(group_tpr.values()) if group_tpr else 0
        fpr_disparity = max(group_fpr.values()) - min(group_fpr.values()) if group_fpr else 0
        max_disparity = max(tpr_disparity, fpr_disparity)
        result = FairnessMetricResult(
            definition=FairnessDefinition.EQUALIZED_ODDS,
            value=round(max_disparity, 4),
            is_fair=max_disparity <= threshold,
            threshold=threshold,
            group_values={f"tpr_{g}": round(v, 4) for g, v in group_tpr.items()},
            details={
                "tpr_disparity": round(tpr_disparity, 4),
                "fpr_disparity": round(fpr_disparity, 4),
                "group_tpr": {g: round(v, 4) for g, v in group_tpr.items()},
                "group_fpr": {g: round(v, 4) for g, v in group_fpr.items()},
            },
        )
        self._results.append(result)
        return result

    def calculate_equal_opportunity(
        self,
        predictions: List[ModelPrediction],
        protected_attr: str,
        threshold: float = 0.1,
    ) -> FairnessMetricResult:
        group_tpr: Dict[str, float] = {}
        for group in set(p.protected_attributes.get(protected_attr, "unknown") for p in predictions):
            positives = [p for p in predictions if p.protected_attributes.get(protected_attr) == group and p.is_positive_actual]
            if positives:
                tp = sum(1 for p in positives if p.is_positive_prediction)
                group_tpr[group] = tp / len(positives)
            else:
                group_tpr[group] = 0
        disparity = max(group_tpr.values()) - min(group_tpr.values()) if group_tpr else 0
        result = FairnessMetricResult(
            definition=FairnessDefinition.EQUAL_OPPORTUNITY,
            value=round(disparity, 4),
            is_fair=disparity <= threshold,
            threshold=threshold,
            group_values={g: round(v, 4) for g, v in group_tpr.items()},
        )
        self._results.append(result)
        return result

    def calculate_all_metrics(
        self,
        predictions: List[ModelPrediction],
        protected_attr: str,
        threshold: float = 0.1,
    ) -> Dict[FairnessDefinition, FairnessMetricResult]:
        results: Dict[FairnessDefinition, FairnessMetricResult] = {}
        results[FairnessDefinition.DEMOGRAPHIC_PARITY] = self.calculate_demographic_parity(
            predictions, protected_attr, threshold
        )
        results[FairnessDefinition.EQUALIZED_ODDS] = self.calculate_equalized_odds(
            predictions, protected_attr, threshold
        )
        results[FairnessDefinition.EQUAL_OPPORTUNITY] = self.calculate_equal_opportunity(
            predictions, protected_attr, threshold
        )
        return results

    def get_all_results(self) -> List[FairnessMetricResult]:
        return list(self._results)

    def get_unfair_metrics(self) -> List[FairnessMetricResult]:
        return [r for r in self._results if not r.is_fair]


class ComplianceFrameworkManager:
    """Manages compliance frameworks and requirement checking."""

    def __init__(self) -> None:
        self._frameworks: Dict[ComplianceFramework, Dict[str, Any]] = {}
        self._requirements: Dict[str, ComplianceRequirement] = {}
        self._compliance_results: List[Dict[str, Any]] = []
        logger.info("ComplianceFrameworkManager initialized")

    def add_framework(
        self,
        framework: ComplianceFramework,
        version: str = "1.0",
        description: str = "",
    ) -> None:
        self._frameworks[framework] = {
            "version": version,
            "description": description,
            "added_at": datetime.now(),
        }

    def add_requirement(
        self,
        framework: ComplianceFramework,
        title: str,
        description: str,
        is_mandatory: bool = True,
        responsible_role: AccountabilityRole = AccountabilityRole.MODEL_OWNER,
        deadline: Optional[datetime] = None,
    ) -> ComplianceRequirement:
        req = ComplianceRequirement(
            framework=framework,
            title=title,
            description=description,
            is_mandatory=is_mandatory,
            responsible_role=responsible_role,
            deadline=deadline,
        )
        self._requirements[req.requirement_id] = req
        return req

    def check_compliance(
        self,
        framework: ComplianceFramework,
        evidence: Dict[str, bool],
    ) -> Dict[str, Any]:
        framework_reqs = [
            r for r in self._requirements.values()
            if r.framework == framework
        ]
        results: List[Dict[str, Any]] = []
        for req in framework_reqs:
            compliant = evidence.get(req.title, False)
            req.is_compliant = compliant
            req.last_verified = datetime.now()
            req.status = GovernanceStatus.IMPLEMENTED if compliant else GovernanceStatus.PROPOSED
            results.append({
                "requirement_id": req.requirement_id,
                "title": req.title,
                "mandatory": req.is_mandatory,
                "compliant": compliant,
                "responsible": req.responsible_role.value,
            })
        mandatory_failed = [r for r in results if r["mandatory"] and not r["compliant"]]
        compliance_result = {
            "framework": framework.value,
            "total_requirements": len(results),
            "compliant_count": len([r for r in results if r["compliant"]]),
            "mandatory_failed": len(mandatory_failed),
            "compliant": len(mandatory_failed) == 0,
            "results": results,
            "checked_at": datetime.now().isoformat(),
        }
        self._compliance_results.append(compliance_result)
        return compliance_result

    def get_framework_requirements(
        self, framework: ComplianceFramework
    ) -> List[ComplianceRequirement]:
        return [
            r for r in self._requirements.values()
            if r.framework == framework
        ]

    def get_overdue_requirements(self) -> List[ComplianceRequirement]:
        return [
            r for r in self._requirements.values()
            if r.is_overdue and r.is_mandatory
        ]

    def get_compliance_summary(self) -> Dict[str, Any]:
        total = len(self._requirements)
        compliant = len([r for r in self._requirements.values() if r.is_compliant])
        overdue = len(self.get_overdue_requirements())
        return {
            "total_requirements": total,
            "compliant": compliant,
            "non_compliant": total - compliant,
            "overdue_mandatory": overdue,
            "compliance_rate": round(compliant / max(total, 1) * 100, 1),
        }


class TransparencyManager:
    """Manages model transparency and documentation."""

    def __init__(self) -> None:
        self._documents: Dict[str, TransparencyDocument] = {}
        self._model_cards: Dict[str, Dict[str, Any]] = {}
        logger.info("TransparencyManager initialized")

    def create_model_card(
        self,
        model_id: str,
        model_name: str,
        intended_use: str,
        training_data_description: str,
        performance_metrics: Dict[str, float],
        limitations: List[str],
        ethical_considerations: List[str],
    ) -> TransparencyDocument:
        content = f"""# Model Card: {model_name}

## Intended Use
{intended_use}

## Training Data
{training_data_description}

## Performance Metrics
{chr(10).join(f'- {k}: {v}' for k, v in performance_metrics.items())}

## Limitations
{chr(10).join(f'- {l}' for l in limitations)}

## Ethical Considerations
{chr(10).join(f'- {e}' for e in ethical_considerations)}
"""
        doc = TransparencyDocument(
            document_type=DocumentType.MODEL_CARD,
            title=f"Model Card: {model_name}",
            content=content,
            model_id=model_id,
            is_public=True,
            tags=["model_card", model_id],
        )
        self._documents[doc.document_id] = doc
        self._model_cards[model_id] = {
            "name": model_name,
            "intended_use": intended_use,
            "limitations": limitations,
            "created_at": datetime.now().isoformat(),
        }
        return doc

    def create_impact_assessment(
        self,
        model_id: str,
        title: str,
        affected_populations: List[str],
        potential_harms: List[str],
        mitigation_measures: List[str],
    ) -> TransparencyDocument:
        content = f"""# Impact Assessment: {title}

## Affected Populations
{chr(10).join(f'- {p}' for p in affected_populations)}

## Potential Harms
{chr(10).join(f'- {h}' for h in potential_harms)}

## Mitigation Measures
{chr(10).join(f'- {m}' for m in mitigation_measures)}
"""
        doc = TransparencyDocument(
            document_type=DocumentType.IMPACT_ASSESSMENT,
            title=title,
            content=content,
            model_id=model_id,
            tags=["impact_assessment", model_id],
        )
        self._documents[doc.document_id] = doc
        return doc

    def get_document(self, document_id: str) -> Optional[TransparencyDocument]:
        return self._documents.get(document_id)

    def get_model_documents(self, model_id: str) -> List[TransparencyDocument]:
        return [
            d for d in self._documents.values()
            if d.model_id == model_id
        ]

    def get_public_documents(self) -> List[TransparencyDocument]:
        return [d for d in self._documents.values() if d.is_public]

    def approve_document(self, document_id: str, approver: str) -> bool:
        doc = self._documents.get(document_id)
        if not doc:
            return False
        doc.approved_by = approver
        doc.last_updated = datetime.now()
        return True


class AccountabilityTracker:
    """Tracks accountability assignments and sign-offs."""

    def __init__(self) -> None:
        self._entries: Dict[str, AccountabilityEntry] = {}
        self._model_ownership: Dict[str, List[str]] = {}
        logger.info("AccountabilityTracker initialized")

    def assign_responsibility(
        self,
        model_id: str,
        role: AccountabilityRole,
        person_name: str,
        person_email: str,
        responsibility: str,
    ) -> AccountabilityEntry:
        entry = AccountabilityEntry(
            model_id=model_id,
            role=role,
            person_name=person_name,
            person_email=person_email,
            responsibility=responsibility,
        )
        self._entries[entry.entry_id] = entry
        self._model_ownership.setdefault(model_id, []).append(entry.entry_id)
        return entry

    def sign_off(self, entry_id: str) -> bool:
        entry = self._entries.get(entry_id)
        if not entry:
            return False
        entry.sign_off_date = datetime.now()
        return True

    def get_model_accountability(self, model_id: str) -> List[AccountabilityEntry]:
        entry_ids = self._model_ownership.get(model_id, [])
        return [
            self._entries[eid]
            for eid in entry_ids
            if eid in self._entries and self._entries[eid].is_active
        ]

    def get_accountability_chain(self, model_id: str) -> Dict[str, Any]:
        entries = self.get_model_accountability(model_id)
        return {
            "model_id": model_id,
            "roles": [
                {
                    "role": e.role.value,
                    "person": e.person_name,
                    "responsibility": e.responsibility,
                    "signed_off": e.sign_off_date is not None,
                }
                for e in entries
            ],
            "all_signed_off": all(e.sign_off_date for e in entries),
        }


class AuditTrail:
    """Comprehensive audit trail for ethics-related decisions."""

    def __init__(self) -> None:
        self._logs: List[Dict[str, Any]] = []
        self._audits: List[AuditRecord] = []
        logger.info("AuditTrail initialized")

    def log_event(
        self,
        event_type: str,
        description: str,
        actor: str,
        model_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        entry = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "description": description,
            "actor": actor,
            "model_id": model_id,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }
        self._logs.append(entry)
        logger.info("Audit event: %s by %s", event_type, actor)

    def start_audit(
        self,
        audit_type: AuditType,
        model_id: str,
        auditor: str,
    ) -> AuditRecord:
        audit = AuditRecord(
            audit_type=audit_type,
            model_id=model_id,
            auditor=auditor,
        )
        self._audits.append(audit)
        self.log_event(
            "audit_started",
            f"Started {audit_type.value} audit for model {model_id}",
            auditor,
            model_id,
        )
        return audit

    def complete_audit(
        self,
        audit_id: str,
        findings: List[Dict[str, Any]],
        overall_score: float,
        risk_level: RiskLevel,
        compliant: bool,
        recommendations: List[str],
    ) -> bool:
        audit = next((a for a in self._audits if a.audit_id == audit_id), None)
        if not audit:
            return False
        audit.findings = findings
        audit.overall_score = overall_score
        audit.risk_level = risk_level
        audit.compliant = compliant
        audit.recommendations = recommendations
        audit.completed_at = datetime.now()
        audit.status = "completed"
        self.log_event(
            "audit_completed",
            f"Completed audit {audit_id}: score={overall_score}, compliant={compliant}",
            audit.auditor,
            audit.model_id,
        )
        return True

    def get_logs(
        self,
        event_type: Optional[str] = None,
        model_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        logs = self._logs
        if event_type:
            logs = [l for l in logs if l["event_type"] == event_type]
        if model_id:
            logs = [l for l in logs if l.get("model_id") == model_id]
        return logs[-limit:]

    def get_audits(
        self, model_id: Optional[str] = None
    ) -> List[AuditRecord]:
        if model_id:
            return [a for a in self._audits if a.model_id == model_id]
        return list(self._audits)

    def get_audit_report(self, days: int = 30) -> Dict[str, Any]:
        cutoff = datetime.now() - timedelta(days=days)
        recent_logs = [
            l for l in self._logs
            if datetime.fromisoformat(l["timestamp"]) >= cutoff
        ]
        event_counts: Dict[str, int] = {}
        for log in recent_logs:
            event_counts[log["event_type"]] = event_counts.get(log["event_type"], 0) + 1
        return {
            "period_days": days,
            "total_events": len(recent_logs),
            "event_breakdown": event_counts,
            "total_audits": len(self._audits),
            "completed_audits": len([a for a in self._audits if a.status == "completed"]),
        }


class EthicsGuidelinesEngine:
    """Generates ethics principles and checklists for specific domains."""

    BASE_PRINCIPLES: List[Dict[str, str]] = [
        {
            "principle": "Transparency",
            "description": "AI systems should be transparent and explainable to users and stakeholders.",
            "implementation": "Provide model cards, documentation, and clear explanations of AI decisions.",
        },
        {
            "principle": "Fairness",
            "description": "AI systems should not discriminate against any group.",
            "implementation": "Conduct regular bias audits and fairness testing across protected attributes.",
        },
        {
            "principle": "Accountability",
            "description": "Clear accountability structures for AI decisions.",
            "implementation": "Assign responsible roles, maintain audit trails, enable human oversight.",
        },
        {
            "principle": "Privacy",
            "description": "Protect user data and privacy throughout the AI lifecycle.",
            "implementation": "Data minimization, encryption, consent management, right to deletion.",
        },
        {
            "principle": "Safety",
            "description": "AI systems should be safe, secure, and robust.",
            "implementation": "Robust testing, adversarial testing, monitoring, incident response.",
        },
        {
            "principle": "Beneficence",
            "description": "AI should benefit humanity and minimize harm.",
            "implementation": "Impact assessments, stakeholder consultation, harm monitoring.",
        },
        {
            "principle": "Autonomy",
            "description": "Respect human autonomy and decision-making.",
            "implementation": "Human-in-the-loop for critical decisions, opt-out mechanisms.",
        },
    ]

    DOMAIN_ADDITIONS: Dict[str, List[Dict[str, str]]] = {
        "healthcare": [
            {
                "principle": "Clinical Oversight",
                "description": "AI should support, not replace, clinical judgment.",
                "implementation": "Human-in-the-loop for all diagnostic and treatment decisions.",
            },
            {
                "principle": "Patient Safety",
                "description": "Patient safety must be the top priority.",
                "implementation": "Rigorous clinical validation, adverse event monitoring.",
            },
        ],
        "finance": [
            {
                "principle": "Consumer Protection",
                "description": "Protect consumers from algorithmic discrimination.",
                "implementation": "Regular fairness testing on lending and insurance decisions.",
            },
            {
                "principle": "Financial Stability",
                "description": "AI should not threaten financial system stability.",
                "implementation": "Stress testing, risk limits, regulatory compliance.",
            },
        ],
        "criminal_justice": [
            {
                "principle": "Due Process",
                "description": "Defendants have the right to understand and challenge AI decisions.",
                "implementation": "Explainable decisions, appeal processes, human review.",
            },
            {
                "principle": "Proportionality",
                "description": "AI-assisted decisions must be proportionate.",
                "implementation": "Proportionality review, impact assessment for each deployment.",
            },
        ],
        "education": [
            {
                "principle": "Student Welfare",
                "description": "AI in education must prioritize student well-being.",
                "implementation": "Student data protection, age-appropriate AI, parental consent.",
            },
        ],
    }

    def __init__(self) -> None:
        self._custom_principles: List[Dict[str, str]] = []
        logger.info("EthicsGuidelinesEngine initialized")

    def get_principles(self, domain: Optional[str] = None) -> List[Dict[str, str]]:
        principles = list(self.BASE_PRINCIPLES)
        if domain and domain in self.DOMAIN_ADDITIONS:
            principles.extend(self.DOMAIN_ADDITIONS[domain])
        principles.extend(self._custom_principles)
        return principles

    def add_custom_principle(
        self, principle: str, description: str, implementation: str
    ) -> None:
        self._custom_principles.append({
            "principle": principle,
            "description": description,
            "implementation": implementation,
        })

    def generate_checklist(self, domain: Optional[str] = None) -> List[Dict[str, str]]:
        checklist = [
            {"item": "Document model purpose, intended use, and limitations", "priority": "high"},
            {"item": "Conduct bias testing on all protected attributes", "priority": "high"},
            {"item": "Provide model explanations to end users", "priority": "high"},
            {"item": "Implement human oversight for critical decisions", "priority": "high"},
            {"item": "Establish data governance and privacy policies", "priority": "high"},
            {"item": "Create incident response procedures", "priority": "medium"},
            {"item": "Train team on AI ethics principles", "priority": "medium"},
            {"item": "Set up continuous monitoring for drift and bias", "priority": "medium"},
            {"item": "Conduct regular third-party audits", "priority": "medium"},
            {"item": "Document decision-making processes", "priority": "medium"},
        ]
        if domain == "healthcare":
            checklist.extend([
                {"item": "Ensure FDA/regulatory compliance", "priority": "high"},
                {"item": "Validate on diverse patient populations", "priority": "high"},
                {"item": "Implement clinical decision support warnings", "priority": "high"},
                {"item": "Establish adverse event reporting", "priority": "high"},
            ])
        elif domain == "finance":
            checklist.extend([
                {"item": "Fair lending compliance testing", "priority": "high"},
                {"item": "Model risk management (SR 11-7)", "priority": "high"},
                {"item": "Consumer adverse action notices", "priority": "high"},
            ])
        elif domain == "criminal_justice":
            checklist.extend([
                {"item": "Due process procedures", "priority": "high"},
                {"item": "Defense access to algorithm details", "priority": "high"},
                {"item": "Regular accuracy and bias audits", "priority": "high"},
            ])
        return checklist


class ModelRiskManager:
    """Comprehensive model risk assessment and management."""

    def __init__(self) -> None:
        self._assessments: Dict[str, ModelRiskAssessment] = {}
        self._risk_policies: List[Dict[str, Any]] = []
        logger.info("ModelRiskManager initialized")

    def assess_model(
        self,
        model_id: str,
        model_name: str,
        bias_findings: List[BiasAnalysisResult],
        compliance_status: Dict[str, bool],
        impact_areas: List[str],
    ) -> ModelRiskAssessment:
        risk_score = 0.0
        risk_factors: List[Dict[str, Any]] = []
        for finding in bias_findings:
            if finding.is_flagged:
                risk_score += finding.bias_score * 30
                risk_factors.append({
                    "factor": f"Bias in {finding.bias_type.value}",
                    "score": finding.bias_score,
                    "threshold": finding.threshold,
                })
        for framework, compliant in compliance_status.items():
            if not compliant:
                risk_score += 15
                risk_factors.append({
                    "factor": f"Non-compliance with {framework}",
                    "score": 15,
                })
        high_impact_areas = {"criminal_justice", "healthcare", "finance", "education"}
        for area in impact_areas:
            if area in high_impact_areas:
                risk_score += 10
                risk_factors.append({
                    "factor": f"High-impact domain: {area}",
                    "score": 10,
                })
        if risk_score >= 50:
            level = RiskLevel.CRITICAL
        elif risk_score >= 35:
            level = RiskLevel.HIGH
        elif risk_score >= 20:
            level = RiskLevel.MEDIUM
        elif risk_score >= 10:
            level = RiskLevel.LOW
        else:
            level = RiskLevel.MINIMAL
        recommendations = self._generate_risk_recommendations(level, risk_factors)
        assessment = ModelRiskAssessment(
            model_id=model_id,
            model_name=model_name,
            risk_level=level,
            risk_score=min(risk_score, 100),
            risk_factors=risk_factors,
            impact_areas=impact_areas,
            bias_findings=bias_findings,
            compliance_status=compliance_status,
            recommendations=recommendations,
            next_assessment=datetime.now() + timedelta(days=90),
        )
        self._assessments[assessment.assessment_id] = assessment
        return assessment

    def get_assessment(self, assessment_id: str) -> Optional[ModelRiskAssessment]:
        return self._assessments.get(assessment_id)

    def get_model_assessments(self, model_id: str) -> List[ModelRiskAssessment]:
        return [a for a in self._assessments.values() if a.model_id == model_id]

    def get_high_risk_models(self) -> List[ModelRiskAssessment]:
        return [
            a for a in self._assessments.values()
            if a.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
        ]

    def get_risk_summary(self) -> Dict[str, Any]:
        assessments = list(self._assessments.values())
        return {
            "total_assessments": len(assessments),
            "by_risk_level": {
                level.value: len([a for a in assessments if a.risk_level == level])
                for level in RiskLevel
            },
            "high_risk_count": len(self.get_high_risk_models()),
            "average_risk_score": (
                sum(a.risk_score for a in assessments) / len(assessments)
                if assessments else 0
            ),
        }

    def _generate_risk_recommendations(
        self,
        level: RiskLevel,
        risk_factors: List[Dict[str, Any]],
    ) -> List[str]:
        recs: List[str] = []
        if level in (RiskLevel.CRITICAL, RiskLevel.HIGH):
            recs.append("URGENT: Halt deployment until issues are resolved")
            recs.append("Conduct comprehensive bias audit with diverse test data")
            recs.append("Engage external ethics review board")
        if level in (RiskLevel.HIGH, RiskLevel.MEDIUM):
            recs.append("Implement fairness constraints in model training")
            recs.append("Increase human oversight and review frequency")
            recs.append("Add monitoring for drift and emerging bias")
        if level in (RiskLevel.MEDIUM, RiskLevel.LOW):
            recs.append("Schedule regular bias audits (quarterly)")
            recs.append("Update model documentation and transparency materials")
        if level == RiskLevel.MINIMAL:
            recs.append("Continue monitoring with standard review cycle")
        return recs


# ---------------------------------------------------------------------------
# Main Agent Orchestrator
# ---------------------------------------------------------------------------

class EthicsAgent:
    """Top-level orchestrator for all ethics and governance operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._bias_detector = BiasDetector()
        self._fairness = FairnessMetrics()
        self._compliance = ComplianceFrameworkManager()
        self._transparency = TransparencyManager()
        self._accountability = AccountabilityTracker()
        self._audit_trail = AuditTrail()
        self._guidelines = EthicsGuidelinesEngine()
        self._risk_manager = ModelRiskManager()
        self._incidents: Dict[str, EthicsIncident] = {}
        self._policies: Dict[str, GovernancePolicy] = {}
        logger.info("EthicsAgent initialized")

    @property
    def bias_detector(self) -> BiasDetector:
        return self._bias_detector

    @property
    def fairness(self) -> FairnessMetrics:
        return self._fairness

    @property
    def compliance(self) -> ComplianceFrameworkManager:
        return self._compliance

    @property
    def transparency(self) -> TransparencyManager:
        return self._transparency

    @property
    def accountability(self) -> AccountabilityTracker:
        return self._accountability

    @property
    def audit_trail(self) -> AuditTrail:
        return self._audit_trail

    @property
    def guidelines(self) -> EthicsGuidelinesEngine:
        return self._guidelines

    @property
    def risk_manager(self) -> ModelRiskManager:
        return self._risk_manager

    def report_incident(
        self,
        title: str,
        description: str,
        severity: IncidentSeverity,
        reported_by: str,
        bias_type: Optional[BiasType] = None,
        affected_groups: Optional[List[str]] = None,
        model_id: Optional[str] = None,
    ) -> EthicsIncident:
        incident = EthicsIncident(
            title=title,
            description=description,
            severity=severity,
            bias_type=bias_type,
            affected_groups=affected_groups or [],
            model_id=model_id,
            reported_by=reported_by,
        )
        self._incidents[incident.incident_id] = incident
        self._audit_trail.log_event(
            "incident_reported",
            f"Incident: {title} (severity: {severity.value})",
            reported_by,
            model_id,
        )
        return incident

    def create_governance_policy(
        self,
        title: str,
        description: str,
        category: str,
        owner: str,
        applicable_frameworks: Optional[List[ComplianceFramework]] = None,
        requirements: Optional[List[str]] = None,
    ) -> GovernancePolicy:
        policy = GovernancePolicy(
            title=title,
            description=description,
            category=category,
            owner=owner,
            applicable_frameworks=applicable_frameworks or [],
            requirements=requirements or [],
        )
        self._policies[policy.policy_id] = policy
        self._audit_trail.log_event(
            "policy_created",
            f"Policy created: {title}",
            owner,
        )
        return policy

    def run_full_assessment(
        self,
        model_id: str,
        model_name: str,
        predictions: List[ModelPrediction],
        protected_attributes: List[str],
        compliance_frameworks: List[ComplianceFramework],
        impact_areas: List[str],
    ) -> Dict[str, Any]:
        bias_results = self._bias_detector.analyze_predictions(
            predictions, protected_attributes
        )
        fairness_results: Dict[str, FairnessMetricResult] = {}
        for attr in protected_attributes:
            fairness_results[attr] = self._fairness.calculate_demographic_parity(
                predictions, attr
            )
        compliance_status: Dict[str, bool] = {}
        for framework in compliance_frameworks:
            result = self._compliance.check_compliance(framework, {})
            compliance_status[framework.value] = result["compliant"]
        risk_assessment = self._risk_manager.assess_model(
            model_id=model_id,
            model_name=model_name,
            bias_findings=list(bias_results.values()),
            compliance_status=compliance_status,
            impact_areas=impact_areas,
        )
        self._audit_trail.log_event(
            "full_assessment_completed",
            f"Full assessment for {model_name}: risk={risk_assessment.risk_level.value}",
            "system",
            model_id,
        )
        return {
            "model_id": model_id,
            "model_name": model_name,
            "bias_analysis": {
                attr: {
                    "score": r.bias_score,
                    "flagged": r.is_flagged,
                    "rates": r.group_rates,
                }
                for attr, r in bias_results.items()
            },
            "fairness_metrics": {
                attr: {
                    "value": r.value,
                    "fair": r.is_fair,
                }
                for attr, r in fairness_results.items()
            },
            "compliance": compliance_status,
            "risk_assessment": {
                "level": risk_assessment.risk_level.value,
                "score": risk_assessment.risk_score,
                "recommendations": risk_assessment.recommendations,
            },
        }

    def get_ethics_dashboard(self) -> Dict[str, Any]:
        bias_flagged = self._bias_detector.get_flagged_attributes()
        fairness_unfair = self._fairness.get_unfair_metrics()
        compliance_summary = self._compliance.get_compliance_summary()
        risk_summary = self._risk_manager.get_risk_summary()
        return {
            "bias": {
                "total_analyses": len(self._bias_detector._analysis_history),
                "flagged_attributes": len(bias_flagged),
            },
            "fairness": {
                "total_metrics": len(self._fairness._results),
                "unfair_metrics": len(fairness_unfair),
            },
            "compliance": compliance_summary,
            "risk": risk_summary,
            "incidents": {
                "total": len(self._incidents),
                "open": len([i for i in self._incidents.values() if i.status == "open"]),
            },
            "policies": {
                "total": len(self._policies),
                "effective": len([p for p in self._policies.values() if p.is_effective]),
            },
            "generated_at": datetime.now().isoformat(),
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "EthicsAgent",
            "analyses_run": len(self._bias_detector._analysis_history),
            "fairness_metrics": len(self._fairness._results),
            "requirements_tracked": len(self._compliance._requirements),
            "documents": len(self._transparency._documents),
            "audits": len(self._audit_trail._audits),
            "incidents": len(self._incidents),
            "policies": len(self._policies),
            "risk_assessments": len(self._risk_manager._assessments),
        }


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    print("=== Ethics Agent Demo ===")
    agent = EthicsAgent()

    predictions = [
        ModelPrediction(predicted_label=1, actual_label=1, protected_attributes={"gender": "male"}),
        ModelPrediction(predicted_label=1, actual_label=1, protected_attributes={"gender": "male"}),
        ModelPrediction(predicted_label=1, actual_label=0, protected_attributes={"gender": "male"}),
        ModelPrediction(predicted_label=0, actual_label=0, protected_attributes={"gender": "female"}),
        ModelPrediction(predicted_label=0, actual_label=1, protected_attributes={"gender": "female"}),
        ModelPrediction(predicted_label=1, actual_label=1, protected_attributes={"gender": "female"}),
    ]

    bias_results = agent.bias_detector.analyze_predictions(predictions, ["gender"])
    for attr, result in bias_results.items():
        print(f"Bias {attr}: score={result.bias_score:.3f}, flagged={result.is_flagged}")

    fairness_result = agent.fairness.calculate_demographic_parity(predictions, "gender")
    print(f"Demographic parity: {fairness_result.value:.3f}, fair={fairness_result.is_fair}")

    agent.compliance.add_framework(ComplianceFramework.EU_AI_ACT, "2024")
    agent.compliance.add_requirement(
        ComplianceFramework.EU_AI_ACT, "Transparency", "Models must be transparent", True
    )
    compliance_result = agent.compliance.check_compliance(
        ComplianceFramework.EU_AI_ACT, {"Transparency": True}
    )
    print(f"Compliance: {compliance_result['compliant']}")

    model_card = agent.transparency.create_model_card(
        "model_001", "Hiring Algorithm",
        "Screen job applications",
        "Historical hiring data",
        {"accuracy": 0.85, "f1": 0.82},
        ["May not generalize to new roles"],
        ["Potential gender bias in historical data"],
    )
    print(f"Model card created: {model_card.title}")

    agent.accountability.assign_responsibility(
        "model_001", AccountabilityRole.MODEL_OWNER, "Jane Doe", "jane@company.com",
        "Overall model governance"
    )

    incident = agent.report_incident(
        "Bias detected in hiring model",
        "Gender bias found in resume screening",
        IncidentSeverity.HIGH,
        "Ethics Team",
        bias_type=BiasType.GENDER,
        model_id="model_001",
    )
    print(f"Incident reported: {incident.incident_id}")

    guidelines = agent.guidelines.get_principles("healthcare")
    checklist = agent.guidelines.generate_checklist("finance")
    print(f"Principles: {len(guidelines)}, Checklist items: {len(checklist)}")

    risk = agent.risk_manager.assess_model(
        "model_001", "Hiring Algorithm",
        list(bias_results.values()),
        {"eu_ai_act": True},
        ["employment", "financial"],
    )
    print(f"Risk level: {risk.risk_level.value}, score: {risk.risk_score:.1f}")

    dashboard = agent.get_ethics_dashboard()
    print(f"Dashboard: {dashboard['compliance']['compliance_rate']}% compliant")

    status = agent.get_status()
    print(f"Agent status: {status}")


if __name__ == "__main__":
    main()
