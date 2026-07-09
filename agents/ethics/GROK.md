---
name: "Ethics Agent"
version: "2.0.0"
description: "Comprehensive AI ethics governance platform covering bias detection, fairness metrics, compliance frameworks, transparency documentation, accountability tracking, audit trails, model risk assessment, and ethics guideline generation"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["ethics", "ai-governance", "bias-detection", "fairness", "compliance", "transparency", "accountability", "audit", "risk-assessment", "responsible-ai"]
category: "governance"
personality: "principled-guardian"
use_cases:
  - "bias detection and analysis"
  - "fairness metric calculation"
  - "compliance framework management"
  - "model transparency documentation"
  - "accountability chain tracking"
  - "ethics audit management"
  - "model risk assessment"
  - "ethics incident reporting"
  - "governance policy management"
---

# Ethics Agent

> Principled guardian of AI fairness, transparency, and accountability.

## Table of Contents

- [Agent Identity](#agent-identity)
- [Core Principles](#core-principles)
- [System Architecture](#system-architecture)
- [Capabilities](#capabilities)
- [Data Models](#data-models)
- [Method Signatures](#method-signatures)
- [Operational Guidelines](#operational-guidelines)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Scalability](#scalability)
- [Design Patterns](#design-patterns)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [Integration Points](#integration-points)
- [Examples](#examples)
- [Best Practices](#best-practices)

---

## Agent Identity

The Ethics Agent is a principled guardian that ensures AI systems operate
fairly, transparently, and accountably. It detects bias, measures fairness,
manages compliance, documents models, tracks accountability, and assesses risk
— providing the governance infrastructure that responsible AI demands.

**Core Personality**: Principled, thorough, evidence-based. Never cuts corners
on fairness. Every finding is statistically validated. Every recommendation
is actionable.

### Agent Capabilities Matrix

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ETHICS AGENT CAPABILITIES                         │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Bias       │  │  Fairness   │  │  Compliance │  │  Trans-     │   │
│  │  Detector   │  │  Metrics    │  │  Manager    │  │  parency    │   │
│  │  ─────────  │  │  ─────────  │  │  ─────────  │  │  ─────────  │   │
│  │  • Analyze  │  │  • DP       │  │  • EU AI    │  │  • Cards    │   │
│  │  • Flag     │  │  • EO       │  │  • NIST     │  │  • Impact   │   │
│  │  • Recommend│  │  • EOpp     │  │  • GDPR     │  │  • Approve  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Account-   │  │  Audit      │  │  Risk       │  │  Guidelines │   │
│  │  ability    │  │  Trail      │  │  Manager    │  │  Engine     │   │
│  │  ─────────  │  │  ─────────  │  │  ─────────  │  │  ─────────  │   │
│  │  • Roles    │  │  • Log      │  │  • Assess   │  │  • Principles│  │
│  │  • Sign-off │  │  • Audit    │  │  • Score    │  │  • Checklist│   │
│  │  • Chain    │  │  • Report   │  │  • Recommend│  │  • Domain   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Core Principles

1. **Statistical Rigor**: Bias claims require evidence, not intuition.
2. **Multi-Definition Fairness**: No single metric tells the whole story.
3. **Proactive Governance**: Detect issues before they cause harm.
4. **Transparency First**: Document everything for scrutiny.
5. **Continuous Monitoring**: Fairness degrades — monitor constantly.

---

## System Architecture

### High-Level Component Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ETHICS AGENT                                      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    GOVERNANCE WORKFLOW                             │   │
│  │  Detect → Assess → Document → Approve → Monitor → Audit          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Bias      │ │  Fairness  │ │  Compliance│ │  Trans-    │           │
│  │  Detector  │ │  Metrics   │ │  Manager   │ │  parency   │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Account-  │ │  Audit     │ │  Risk      │ │  Guidelines│           │
│  │  ability   │ │  Trail     │ │  Manager   │ │  Engine    │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    DATA LAYER (In-Memory + Optional DB)           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Governance Workflow Diagram

```
  Pre-Deployment Assessment:
  ═════════════════════════

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Collect  │ ─► │ Analyze  │ ─► │ Assess   │ ─► │ Document │
  │ Predict- │    │ Bias     │    │ Risk     │    │ Findings │
  │ ions     │    │          │    │          │    │          │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
       ▼               ▼               ▼               ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Protected│    │ Fairness │    │ Compliance│   │ Model    │
  │ Attrs    │    │ Metrics  │    │ Check    │    │ Card     │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                              │
                                              ▼
                                       ┌──────────┐    ┌──────────┐
                                       │ Approve  │ ─► │ Monitor  │
                                       │ / Block  │    │ Ongoing  │
                                       └──────────┘    └──────────┘
```

### Bias Detection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    BIAS DETECTION PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Input Predictions                                             │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ predictions = [                                      │     │
│     │   {label: 1, actual: 1, attrs: {gender: "male"}},   │     │
│     │   {label: 0, actual: 1, attrs: {gender: "female"}}, │     │
│     │   ...                                                │     │
│     │ ]                                                    │     │
│     └─────────────────────────────────────────────────────┘     │
│                          │                                        │
│                          ▼                                        │
│  2. Group by Protected Attribute                                  │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ Male:   [TP=80, FP=20, FN=10, TN=90]                │     │
│     │ Female: [TP=60, FP=30, FN=20, TN=90]                │     │
│     └─────────────────────────────────────────────────────┘     │
│                          │                                        │
│                          ▼                                        │
│  3. Calculate Group Rates                                         │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ Male:   TPR=0.89, FPR=0.18, Selection=0.50          │     │
│     │ Female: TPR=0.75, FPR=0.25, Selection=0.45          │     │
│     └─────────────────────────────────────────────────────┘     │
│                          │                                        │
│                          ▼                                        │
│  4. Compute Disparity Metrics                                     │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ Demographic Parity: |0.50 - 0.45| = 0.05            │     │
│     │ Equalized Odds: max(|0.89-0.75|, |0.18-0.25|) = 0.14│    │
│     │ Equal Opportunity: |0.89 - 0.75| = 0.14             │     │
│     └─────────────────────────────────────────────────────┘     │
│                          │                                        │
│                          ▼                                        │
│  5. Apply Thresholds                                              │
│     ┌─────────────────────────────────────────────────────┐     │
│     │ DP  > 0.10 → FLAGGED                                │     │
│     │ EO  > 0.10 → FLAGGED                                │     │
│     │ EOpp > 0.10 → FLAGGED                                │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Capabilities

### 1. Bias Detection

```python
from agents.ethics.agent import (
    EthicsAgent, BiasType, ModelPrediction, IncidentSeverity
)

agent = EthicsAgent()

predictions = [
    ModelPrediction(predicted_label=1, actual_label=1, protected_attributes={"gender": "male"}),
    ModelPrediction(predicted_label=1, actual_label=0, protected_attributes={"gender": "male"}),
    ModelPrediction(predicted_label=0, actual_label=1, protected_attributes={"gender": "female"}),
    ModelPrediction(predicted_label=0, actual_label=0, protected_attributes={"gender": "female"}),
]

# Analyze bias across protected attributes
results = agent.bias_detector.analyze_predictions(
    predictions, protected_attributes=["gender"]
)

for attr, result in results.items():
    print(f"{attr}: score={result.bias_score:.3f}, flagged={result.is_flagged}")
    print(f"  Rates: {result.group_rates}")
    print(f"  Recommendations: {result.recommendations}")
```

**Supported Bias Types**: Gender, Race, Age, Socioeconomic, Religious,
Disability, Geographic, Ethnicity, National Origin, Sexual Orientation,
Marital Status, Veteran Status.

### 2. Fairness Metrics

```python
# Demographic Parity
dp = agent.fairness.calculate_demographic_parity(predictions, "gender")
print(f"Demographic parity: {dp.value:.3f}, fair={dp.is_fair}")

# Equalized Odds
eo = agent.fairness.calculate_equalized_odds(predictions, "gender")
print(f"Equalized odds: {eo.value:.3f}")

# Equal Opportunity
eop = agent.fairness.calculate_equal_opportunity(predictions, "gender")
print(f"Equal opportunity: {eop.value:.3f}")

# All metrics at once
all_metrics = agent.fairness.calculate_all_metrics(predictions, "gender")
```

### 3. Compliance Framework Management

```python
from agents.ethics.agent import ComplianceFramework, AccountabilityRole

# Add frameworks
agent.compliance.add_framework(ComplianceFramework.EU_AI_ACT, "2024")
agent.compliance.add_framework(ComplianceFramework.NIST_AI_RMF, "2023")

# Add requirements
agent.compliance.add_requirement(
    ComplianceFramework.EU_AI_ACT,
    title="Transparency",
    description="High-risk AI must be transparent about capabilities and limitations",
    is_mandatory=True,
    responsible_role=AccountabilityRole.MODEL_OWNER,
)

# Check compliance
result = agent.compliance.check_compliance(
    ComplianceFramework.EU_AI_ACT,
    {"Transparency": True}
)
print(f"Compliant: {result['compliant']}")
print(f"Score: {result['compliant_count']}/{result['total_requirements']}")

# Get overdue requirements
overdue = agent.compliance.get_overdue_requirements()
```

### 4. Transparency Documentation

```python
# Create model card
model_card = agent.transparency.create_model_card(
    model_id="hiring_model_v2",
    model_name="Hiring Resume Screener",
    intended_use="Screen job applications for engineering roles",
    training_data_description="100K historical applications from 2018-2023",
    performance_metrics={"accuracy": 0.87, "precision": 0.84, "recall": 0.89},
    limitations=["May not generalize to non-engineering roles", "Limited to English-language resumes"],
    ethical_considerations=["Historical gender imbalance in training data", "Potential for proxy discrimination"],
)
print(f"Model card: {model_card.title}")

# Create impact assessment
impact = agent.transparency.create_impact_assessment(
    model_id="hiring_model_v2",
    title="Hiring Model Impact Assessment",
    affected_populations=["job applicants", "underrepresented groups"],
    potential_harms=["employment discrimination", "reinforcement of historical bias"],
    mitigation_measures=["regular bias audits", "human review of flagged cases", "diverse training data"],
)
```

### 5. Accountability Tracking

```python
from agents.ethics.agent import AccountabilityRole

# Assign responsibilities
entry = agent.accountability.assign_responsibility(
    model_id="hiring_model_v2",
    role=AccountabilityRole.MODEL_OWNER,
    person_name="Jane Smith",
    person_email="jane@company.com",
    responsibility="Overall model governance and fairness",
)

# Sign off
agent.accountability.sign_off(entry.entry_id)

# Get accountability chain
chain = agent.accountability.get_accountability_chain("hiring_model_v2")
print(f"All signed off: {chain['all_signed_off']}")
```

### 6. Audit Trail

```python
from agents.ethics.agent import AuditType, RiskLevel

# Start audit
audit = agent.audit_trail.start_audit(
    AuditType.PRE_DEPLOYMENT,
    "hiring_model_v2",
    "External Auditor Inc.",
)

# Complete audit
agent.audit_trail.complete_audit(
    audit.audit_id,
    findings=[{"type": "bias", "detail": "Gender disparity detected", "severity": "high"}],
    overall_score=65.0,
    risk_level=RiskLevel.HIGH,
    compliant=False,
    recommendations=["Re-balance training data", "Implement fairness constraints"],
)

# Get audit report
report = agent.audit_trail.get_audit_report(days=30)
```

### 7. Ethics Guidelines

```python
# Get principles for domain
principles = agent.guidelines.get_principles("healthcare")
for p in principles:
    print(f"{p['principle']}: {p['description']}")

# Generate checklist
checklist = agent.guidelines.generate_checklist("finance")
for item in checklist:
    print(f"[{item['priority']}] {item['item']}")
```

### 8. Model Risk Assessment

```python
risk = agent.risk_manager.assess_model(
    model_id="hiring_model_v2",
    model_name="Hiring Resume Screener",
    bias_findings=list(results.values()),
    compliance_status={"eu_ai_act": True, "gdpr": True},
    impact_areas=["employment", "financial"],
)
print(f"Risk level: {risk.risk_level.value}")
print(f"Risk score: {risk.risk_score:.1f}")
print(f"Recommendations:")
for rec in risk.recommendations:
    print(f"  - {rec}")
```

### 9. Incident Reporting

```python
incident = agent.report_incident(
    title="Bias detected in loan approval model",
    description="African American applicants receiving 30% fewer approvals",
    severity=IncidentSeverity.HIGH,
    reported_by="Ethics Review Board",
    bias_type=BiasType.RACE,
    affected_groups=["african_american"],
    model_id="loan_model_v1",
)
print(f"Incident: {incident.incident_id}")
```

### 10. Full Assessment (All-in-One)

```python
report = agent.run_full_assessment(
    model_id="hiring_model_v2",
    model_name="Hiring Resume Screener",
    predictions=predictions,
    protected_attributes=["gender"],
    compliance_frameworks=[ComplianceFramework.EU_AI_ACT],
    impact_areas=["employment"],
)
# Returns comprehensive report with bias, fairness, compliance, and risk
```

---

## Data Models

### ModelPrediction Model

```python
@dataclass
class ModelPrediction:
    prediction_id: str           # Unique identifier
    predicted_label: int         # Model's prediction
    actual_label: int            # Ground truth
    protected_attributes: Dict[str, str]  # {gender: "male", race: "white"}
    confidence: float            # Prediction confidence (0-1)
    timestamp: datetime
```

### BiasAnalysisResult Model

```python
@dataclass
class BiasAnalysisResult:
    analysis_id: str             # Unique identifier
    bias_type: BiasType          # Protected attribute analyzed
    bias_score: float            # 0-1, higher = more biased
    is_flagged: bool             # Exceeds threshold
    threshold: float             # Configured threshold
    group_rates: Dict[str, float]  # Rates per group
    recommendations: List[str]   # Action items
    created_at: datetime
```

### FairnessMetricResult Model

```python
@dataclass
class FairnessMetricResult:
    metric_id: str               # Unique identifier
    definition: FairnessDefinition  # DP, EO, EOpp
    value: float                 # Metric value (0-1)
    is_fair: bool                # Within threshold
    threshold: float             # Configured threshold
    group_values: Dict[str, float]  # Per-group values
    created_at: datetime
```

### ComplianceRequirement Model

```python
@dataclass
class ComplianceRequirement:
    requirement_id: str          # Unique identifier
    framework: ComplianceFramework  # EU_AI_ACT, NIST, etc.
    title: str                   # Requirement title
    description: str             # Requirement description
    is_mandatory: bool           # Required or recommended
    is_compliant: bool           # Current compliance status
    responsible_role: AccountabilityRole  # Who is responsible
    deadline: Optional[datetime]  # Compliance deadline
    evidence: List[str]          # Supporting evidence
```

### TransparencyDocument Model

```python
@dataclass
class TransparencyDocument:
    document_id: str             # Unique identifier
    document_type: str           # model_card, impact_assessment
    title: str                   # Document title
    content: Dict[str, Any]      # Document content
    model_id: str                # Associated model
    is_public: bool              # Public disclosure
    version: str                 # Document version
    created_at: datetime
    approved_at: Optional[datetime]
    approver: Optional[str]
```

### AccountabilityEntry Model

```python
@dataclass
class AccountabilityEntry:
    entry_id: str                # Unique identifier
    model_id: str                # Associated model
    role: AccountabilityRole     # Role type
    person_name: str             # Responsible person
    person_email: str            # Contact email
    responsibility: str          # Specific responsibility
    assigned_at: datetime        # Assignment date
    sign_off_date: Optional[datetime]  # Sign-off date
```

### AuditRecord Model

```python
@dataclass
class AuditRecord:
    audit_id: str                # Unique identifier
    audit_type: AuditType        # PRE_DEPLOYMENT, PERIODIC, etc.
    model_id: str                # Associated model
    auditor: str                 # Auditor name/organization
    status: str                  # IN_PROGRESS, COMPLETED
    findings: List[Dict[str, Any]]  # Audit findings
    overall_score: float         # 0-100 score
    risk_level: RiskLevel        # MINIMAL to CRITICAL
    compliant: bool              # Overall compliance
    recommendations: List[str]   # Improvement items
    started_at: datetime
    completed_at: Optional[datetime]
```

### EthicsIncident Model

```python
@dataclass
class EthicsIncident:
    incident_id: str             # Unique identifier
    title: str                   # Incident title
    description: str             # Detailed description
    severity: IncidentSeverity   # LOW to CRITICAL
    status: str                  # OPEN, INVESTIGATING, RESOLVED
    reported_by: str             # Reporter
    bias_type: Optional[BiasType]  # Associated bias type
    affected_groups: List[str]   # Affected populations
    model_id: Optional[str]      # Associated model
    created_at: datetime
    resolved_at: Optional[datetime]
```

### ModelRiskAssessment Model

```python
@dataclass
class ModelRiskAssessment:
    assessment_id: str           # Unique identifier
    model_id: str                # Associated model
    model_name: str              # Model name
    risk_level: RiskLevel        # MINIMAL to CRITICAL
    risk_score: float            # 0-100
    bias_findings: List[BiasAnalysisResult]  # Bias issues
    compliance_status: Dict[str, bool]  # Framework compliance
    impact_areas: List[str]      # Areas of impact
    recommendations: List[str]   # Mitigation recommendations
    assessed_at: datetime
```

### Data Model Relationships

```
┌──────────────────┐       ┌──────────────────┐
│  ModelPrediction │ 1───∞ │ BiasAnalysisResult│
│                  │       │                  │
│ prediction_id    │       │ analysis_id      │
│ protected_attrs ─┼──────►│ bias_type        │
│ predicted_label  │       │ bias_score       │
│ actual_label     │       │ is_flagged       │
└──────────────────┘       └──────────────────┘
         │
         │ 1───∞
         ▼
┌──────────────────┐       ┌──────────────────┐
│ FairnessMetric   │       │ ComplianceReq    │
│                  │       │                  │
│ metric_id        │       │ requirement_id   │
│ definition       │       │ framework        │
│ value            │       │ is_mandatory     │
│ is_fair          │       │ is_compliant     │
└──────────────────┘       └──────────────────┘
         │                         │
         │ 1───∞                   │ 1───∞
         ▼                         ▼
┌──────────────────┐       ┌──────────────────┐
│ TransparencyDoc  │       │ AccountabilityEntry│
│                  │       │                  │
│ document_id      │       │ entry_id         │
│ model_id         │       │ model_id         │
│ is_public        │       │ role             │
└──────────────────┘       │ sign_off_date    │
                           └──────────────────┘
                                  │
                                  │ 1───∞
                                  ▼
                           ┌──────────────────┐
                           │   AuditRecord    │
                           │                  │
                           │ audit_id         │
                           │ findings         │
                           │ risk_level       │
                           │ compliant        │
                           └──────────────────┘
```

---

## Method Signatures

### EthicsAgent (Top-Level)

```python
def run_full_assessment(
    self,
    model_id: str,
    model_name: str,
    predictions: List[ModelPrediction],
    protected_attributes: List[str],
    compliance_frameworks: Optional[List[ComplianceFramework]] = None,
    impact_areas: Optional[List[str]] = None,
) -> Dict[str, Any]

def report_incident(
    self,
    title: str,
    description: str,
    severity: IncidentSeverity,
    reported_by: str,
    bias_type: Optional[BiasType] = None,
    affected_groups: Optional[List[str]] = None,
    model_id: Optional[str] = None,
) -> EthicsIncident

def create_governance_policy(
    self,
    title: str,
    description: str,
    requirements: List[str],
    effective_date: datetime,
) -> GovernancePolicy

def get_ethics_dashboard(self) -> Dict[str, Any]

def get_status(self) -> Dict[str, Any]
```

### BiasDetector

```python
def set_threshold(self, bias_type: BiasType, threshold: float) -> None

def get_threshold(self, bias_type: BiasType) -> float

def analyze_predictions(
    self,
    predictions: List[ModelPrediction],
    protected_attributes: List[str],
    outcome_attr: str = "predicted_label",
) -> Dict[str, BiasAnalysisResult]

def analyze_single_attribute(
    self,
    predictions: List[ModelPrediction],
    attribute: str,
) -> BiasAnalysisResult

def get_analysis_history(
    self,
    bias_type: Optional[BiasType] = None,
) -> List[BiasAnalysisResult]

def get_flagged_attributes(self) -> List[BiasAnalysisResult]
```

### FairnessMetrics

```python
def calculate_demographic_parity(
    self,
    predictions: List[ModelPrediction],
    protected_attr: str,
    threshold: float = 0.1,
) -> FairnessMetricResult

def calculate_equalized_odds(
    self,
    predictions: List[ModelPrediction],
    protected_attr: str,
    threshold: float = 0.1,
) -> FairnessMetricResult

def calculate_equal_opportunity(
    self,
    predictions: List[ModelPrediction],
    protected_attr: str,
    threshold: float = 0.1,
) -> FairnessMetricResult

def calculate_all_metrics(
    self,
    predictions: List[ModelPrediction],
    protected_attr: str,
    threshold: float = 0.1,
) -> Dict[FairnessDefinition, FairnessMetricResult]

def get_all_results(self) -> List[FairnessMetricResult]

def get_unfair_metrics(self) -> List[FairnessMetricResult]
```

### ComplianceFrameworkManager

```python
def add_framework(
    self,
    framework: ComplianceFramework,
    version: str = "1.0",
    description: str = "",
) -> None

def add_requirement(
    self,
    framework: ComplianceFramework,
    title: str,
    description: str,
    is_mandatory: bool = True,
    responsible_role: AccountabilityRole = AccountabilityRole.MODEL_OWNER,
    deadline: Optional[datetime] = None,
) -> ComplianceRequirement

def check_compliance(
    self,
    framework: ComplianceFramework,
    evidence: Dict[str, bool],
) -> Dict[str, Any]

def get_framework_requirements(
    self,
    framework: ComplianceFramework,
) -> List[ComplianceRequirement]

def get_overdue_requirements(self) -> List[ComplianceRequirement]

def get_compliance_summary(self) -> Dict[str, Any]
```

### TransparencyManager

```python
def create_model_card(
    self,
    model_id: str,
    model_name: str,
    intended_use: str,
    training_data_description: str = "",
    performance_metrics: Optional[Dict[str, float]] = None,
    limitations: Optional[List[str]] = None,
    ethical_considerations: Optional[List[str]] = None,
) -> TransparencyDocument

def create_impact_assessment(
    self,
    model_id: str,
    title: str,
    affected_populations: Optional[List[str]] = None,
    potential_harms: Optional[List[str]] = None,
    mitigation_measures: Optional[List[str]] = None,
) -> TransparencyDocument

def get_document(self, document_id: str) -> Optional[TransparencyDocument]

def get_model_documents(self, model_id: str) -> List[TransparencyDocument]

def get_public_documents(self) -> List[TransparencyDocument]

def approve_document(self, document_id: str, approver: str) -> bool
```

### AccountabilityTracker

```python
def assign_responsibility(
    self,
    model_id: str,
    role: AccountabilityRole,
    person_name: str,
    person_email: str,
    responsibility: str,
) -> AccountabilityEntry

def sign_off(self, entry_id: str) -> bool

def get_model_accountability(self, model_id: str) -> List[AccountabilityEntry]

def get_accountability_chain(self, model_id: str) -> Dict[str, Any]
```

### AuditTrail

```python
def log_event(
    self,
    event_type: str,
    description: str,
    actor: str,
    model_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None

def start_audit(
    self,
    audit_type: AuditType,
    model_id: str,
    auditor: str,
) -> AuditRecord

def complete_audit(
    self,
    audit_id: str,
    findings: List[Dict[str, Any]],
    overall_score: float,
    risk_level: RiskLevel,
    compliant: bool,
    recommendations: Optional[List[str]] = None,
) -> bool

def get_logs(
    self,
    event_type: Optional[str] = None,
    model_id: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]

def get_audits(self, model_id: Optional[str] = None) -> List[AuditRecord]

def get_audit_report(self, days: int = 30) -> Dict[str, Any]
```

### EthicsGuidelinesEngine

```python
def get_principles(self, domain: Optional[str] = None) -> List[Dict[str, str]]

def add_custom_principle(
    self,
    principle: str,
    description: str,
    implementation: str,
) -> None

def generate_checklist(self, domain: Optional[str] = None) -> List[Dict[str, str]]
```

### ModelRiskManager

```python
def assess_model(
    self,
    model_id: str,
    model_name: str,
    bias_findings: List[BiasAnalysisResult],
    compliance_status: Dict[str, bool],
    impact_areas: List[str],
) -> ModelRiskAssessment

def get_assessment(self, assessment_id: str) -> Optional[ModelRiskAssessment]

def get_model_assessments(self, model_id: str) -> List[ModelRiskAssessment]

def get_high_risk_models(self) -> List[ModelRiskAssessment]

def get_risk_summary(self) -> Dict[str, Any]
```

---

## Operational Guidelines

### Pre-Deployment Checklist

1. Run bias analysis on all protected attributes
2. Calculate fairness metrics (demographic parity, equalized odds, equal opportunity)
3. Check compliance with applicable frameworks
4. Create/update model card
5. Complete impact assessment
6. Assign accountability roles
7. Get sign-offs from all responsible parties
8. Conduct pre-deployment audit
9. Document risk assessment findings
10. Set up monitoring for drift and emerging bias

### Bias Investigation Workflow

1. Detect bias via `analyze_predictions()`
2. Validate findings with additional data
3. Report incident via `report_incident()`
4. Assess risk via `assess_model()`
5. Create mitigation plan
6. Implement fixes
7. Re-run bias analysis to verify
8. Document lessons learned

### Compliance Maintenance

- Review requirements quarterly
- Update evidence when models change
- Track overdue mandatory requirements
- Generate compliance summary for leadership
- Maintain audit trail for all compliance checks

---

## Configuration

### Agent Configuration

```yaml
ethics_agent:
  bias_detector:
    default_threshold: 0.1
    significance_level: 0.05
    min_sample_size: 30

  fairness:
    default_threshold: 0.1
    metrics_to_compute:
      - demographic_parity
      - equalized_odds
      - equal_opportunity

  compliance:
    frameworks:
      - eu_ai_act
      - gdpr
      - nist_ai_rmf
    auto_check_interval_days: 30

  transparency:
    require_model_cards: true
    require_impact_assessment: true

  accountability:
    required_roles:
      - model_owner
      - data_scientist
      - ethics_committee
    sign_off_required: true

  audit:
    retention_days: 2555
    auto_audit_frequency: quarterly

  risk:
    high_risk_threshold: 35
    critical_risk_threshold: 50
    reassessment_interval_days: 90
```

---

## Security Considerations

### Data Protection

- Bias analysis data contains sensitive protected attributes
- Implement access controls on audit trails
- Encrypt model cards and impact assessments at rest
- Use audit logging for all governance operations
- Protect incident reports from unauthorized access

### Access Control

- Role-based access for compliance management
- Separate permissions for audit trail access
- Approval workflows for transparency documents
- Immutable audit records (append-only)

### Integrity

- Audit trail entries are timestamped and immutable
- Model cards require approval before publication
- Compliance checks are logged with evidence
- Risk assessments are versioned

---

## Scalability

### Current Design Limits

| Component | Limit | Notes |
|-----------|-------|-------|
| Predictions | ~100,000 | Per analysis batch |
| Models tracked | ~1,000 | In-memory storage |
| Audit records | ~10,000 | Per session |
| Compliance frameworks | ~20 | Per instance |

### Scaling Strategies

```
┌─────────────────────────────────────────────────────────────┐
│                    SCALING PATHWAY                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Phase 1: In-Memory (Current)                                │
│  ├── Single process, stdlib only                             │
│  └── Suitable for < 100 models                               │
│                                                               │
│  Phase 2: Database Backend                                   │
│  ├── PostgreSQL for predictions and audit trails             │
│  ├── Redis for caching fairness metrics                      │
│  └── Suitable for < 1000 models                              │
│                                                               │
│  Phase 3: Distributed                                        │
│  ├── Microservices per component                             │
│  ├── Batch processing for large prediction sets              │
│  ├── Message queues for async assessments                    │
│  └── Suitable for 1000+ models                               │
│                                                               │
│  Phase 4: Enterprise Scale                                   │
│  ├── Multi-tenant deployment                                 │
│  ├── Real-time monitoring pipelines                          │
│  ├── Federated bias detection                                │
│  └── Suitable for 10K+ models                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Performance Benchmarks

| Operation | Current | With DB | With Cache |
|-----------|---------|---------|------------|
| Bias analysis (1K predictions) | ~20ms | ~50ms | ~15ms |
| Fairness metrics (3 definitions) | ~30ms | ~80ms | ~25ms |
| Compliance check | ~5ms | ~15ms | ~5ms |
| Risk assessment | ~10ms | ~30ms | ~10ms |
| Audit report generation | ~50ms | ~100ms | ~40ms |

---

## Design Patterns

### Strategy Pattern

Different fairness definitions are interchangeable:

```python
class FairnessStrategy(ABC):
    @abstractmethod
    def calculate(self, predictions: List[ModelPrediction], attr: str) -> float:
        pass

class DemographicParity(FairnessStrategy):
    def calculate(self, predictions, attr):
        # Calculate selection rate parity
        pass

class EqualizedOdds(FairnessStrategy):
    def calculate(self, predictions, attr):
        # Calculate TPR and FPR parity
        pass
```

### Observer Pattern

Bias findings trigger notifications:

```python
class BiasObserver(ABC):
    @abstractmethod
    def on_bias_detected(self, finding: BiasAnalysisResult):
        pass

class IncidentCreator(BiasObserver):
    def on_bias_detected(self, finding):
        if finding.is_flagged:
            self.create_incident(finding)

class AlertSender(BiasObserver):
    def on_bias_detected(self, finding):
        if finding.bias_score > 0.3:
            self.send_alert(finding)
```

### Template Method Pattern

Compliance checking follows a common template:

```python
class ComplianceChecker(ABC):
    def check(self, framework, evidence):
        requirements = self.get_requirements(framework)
        results = [self.check_requirement(r, evidence) for r in requirements]
        return self.compile_results(results)

    @abstractmethod
    def get_requirements(self, framework):
        pass

    @abstractmethod
    def check_requirement(self, requirement, evidence):
        pass
```

### State Pattern

Incident lifecycle:

```python
class IncidentState(ABC):
    @abstractmethod
    def next(self, incident: EthicsIncident) -> 'IncidentState':
        pass

class OpenState(IncidentState):
    def next(self, incident):
        return InvestigatingState()

class InvestigatingState(IncidentState):
    def next(self, incident):
        if incident.resolved_at:
            return ResolvedState()
        return self
```

---

## Checklists

### Pre-Deployment Checklist

- [ ] Protected attributes identified and documented
- [ ] Bias analysis run on all protected attributes
- [ ] Fairness metrics calculated (all applicable definitions)
- [ ] Compliance frameworks identified
- [ ] Requirements documented and tracked
- [ ] Model card created and approved
- [ ] Impact assessment completed
- [ ] Accountability roles assigned and signed off
- [ ] Pre-deployment audit conducted
- [ ] Risk assessment documented
- [ ] Monitoring plan established
- [ ] Incident response procedure documented

### Bias Investigation Checklist

- [ ] Bias detected via `analyze_predictions()`
- [ ] Findings validated with additional data
- [ ] Incident reported via `report_incident()`
- [ ] Risk assessed via `assess_model()`
- [ ] Mitigation plan created
- [ ] Fixes implemented
- [ ] Re-analysis confirms fix
- [ ] Lessons learned documented

### Compliance Review Checklist

- [ ] All frameworks reviewed quarterly
- [ ] Evidence updated for changed models
- [ ] Overdue requirements tracked
- [ ] Compliance summary generated
- [ ] Audit trail maintained
- [ ] Leadership notified of gaps

---

## Troubleshooting

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Bias score always 0 | All groups have equal rates | Check if protected attribute is in data |
| Fairness metrics disagree | Different definitions measure different things | Use multiple metrics, not just one |
| Compliance check fails | Missing evidence | Provide evidence dict with requirement titles |
| Risk score too high | Multiple bias findings | Address highest-severity findings first |
| Audit trail incomplete | Events not logged | Ensure `log_event()` called for all actions |
| Model card not public | Not approved | Call `approve_document()` with approver |
| At-risk list empty | No high-risk models | Lower risk threshold |
| Incident not resolving | Missing resolution | Set `resolved_at` timestamp |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed bias analysis
results = agent.bias_detector.analyze_predictions(predictions, ["gender"])
for attr, result in results.items():
    print(f"{attr}: {result.group_rates}")
```

---

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| MLflow | REST API | Model registry integration |
| Weights & Biases | REST API | Experiment tracking |
| Great Expectations | Python API | Data quality validation |
| Alibi Detect | Python API | Advanced bias detection |
| AI Fairness 360 | Python API | Extended fairness metrics |
| LIME/SHAP | Python API | Model explainability |
| Slack | Webhook | Incident notifications |
| Jira | REST API | Issue tracking |

---

## Examples

### Example 1: Complete Pre-Deployment Assessment

```python
agent = EthicsAgent()

# Full assessment
report = agent.run_full_assessment(
    model_id="credit_scorer_v3",
    model_name="Credit Scoring Model",
    predictions=live_predictions,
    protected_attributes=["race", "gender", "age"],
    compliance_frameworks=[
        ComplianceFramework.EU_AI_ACT,
        ComplianceFramework.NIST_AI_RMF,
    ],
    impact_areas=["financial", "lending", "housing"],
)

if report["risk_assessment"]["level"] in ("high", "critical"):
    print("BLOCK: Resolve issues before deployment")
else:
    print("APPROVED: Ready for deployment")
```

### Example 2: Continuous Monitoring Dashboard

```python
agent = EthicsAgent()

# Run weekly
results = agent.bias_detector.analyze_predictions(
    weekly_predictions, ["gender", "race", "age"]
)

flagged = agent.bias_detector.get_flagged_attributes()
for finding in flagged:
    agent.report_incident(
        title=f"Emerging bias in {finding.bias_type.value}",
        description=f"Disparity of {finding.bias_score:.3f}",
        severity=IncidentSeverity.HIGH,
        reported_by="Monitoring System",
    )

dashboard = agent.get_ethics_dashboard()
```

### Example 3: Compliance Reporting

```python
agent = EthicsAgent()
agent.compliance.add_framework(ComplianceFramework.EU_AI_ACT)
# ... add requirements ...

summary = agent.compliance.get_compliance_summary()
print(f"Compliance rate: {summary['compliance_rate']}%")
print(f"Overdue mandatory: {summary['overdue_mandatory']}")

overdue = agent.compliance.get_overdue_requirements()
for req in overdue:
    print(f"OVERDUE: {req.title} (responsible: {req.responsible_role.value})")
```

### Example 4: Accountability Chain

```python
agent = EthicsAgent()

# Assign roles
agent.accountability.assign_responsibility(
    "model_001", AccountabilityRole.MODEL_OWNER,
    "Alice", "alice@co.com", "Overall governance"
)
agent.accountability.assign_responsibility(
    "model_001", AccountabilityRole.DATA_SCIENTIST,
    "Bob", "bob@co.com", "Model development"
)
agent.accountability.assign_responsibility(
    "model_001", AccountabilityRole.ETHICS_COMMITTEE,
    "Ethics Board", "ethics@co.com", "Review and approval"
)

chain = agent.accountability.get_accountability_chain("model_001")
print(f"All signed off: {chain['all_signed_off']}")
```

---

## Best Practices

1. **Run bias analysis before every deployment** — not just once.
2. **Use multiple fairness metrics** — no single metric captures all bias.
3. **Set thresholds based on domain** — healthcare needs stricter than entertainment.
4. **Document everything** — model cards, impact assessments, decisions.
5. **Assign clear accountability** — every model needs an owner.
6. **Conduct regular audits** — quarterly minimum, monthly for high-risk.
7. **Report incidents immediately** — don't wait for the next audit cycle.
8. **Monitor continuously** — bias can emerge over time as data drifts.
9. **Engage diverse stakeholders** — include affected communities in review.
10. **Stay current** — regulations evolve; update compliance frameworks.

---

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[README.md](./README.md) for quick start and API reference.