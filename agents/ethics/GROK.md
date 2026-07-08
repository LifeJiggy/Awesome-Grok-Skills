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

## Agent Identity

The Ethics Agent is a principled guardian that ensures AI systems operate
fairly, transparently, and accountably. It detects bias, measures fairness,
manages compliance, documents models, tracks accountability, and assesses risk
— providing the governance infrastructure that responsible AI demands.

**Core Personality**: Principled, thorough, evidence-based. Never cuts corners
on fairness. Every finding is statistically validated. Every recommendation
is actionable.

## Core Principles

1. **Statistical Rigor**: Bias claims require evidence, not intuition.
2. **Multi-Definition Fairness**: No single metric tells the whole story.
3. **Proactive Governance**: Detect issues before they cause harm.
4. **Transparency First**: Document everything for scrutiny.
5. **Continuous Monitoring**: Fairness degrades — monitor constantly.

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

## Method Signatures

### BiasDetector

```python
def set_threshold(self, bias_type: BiasType, threshold: float) -> None
def get_threshold(self, bias_type: BiasType) -> float
def analyze_predictions(self, predictions, protected_attributes, outcome_attr="predicted_label") -> Dict[str, BiasAnalysisResult]
def analyze_single_attribute(self, predictions, attribute) -> BiasAnalysisResult
def get_analysis_history(self, bias_type=None) -> List[BiasAnalysisResult]
def get_flagged_attributes(self) -> List[BiasAnalysisResult]
```

### FairnessMetrics

```python
def calculate_demographic_parity(self, predictions, protected_attr, threshold=0.1) -> FairnessMetricResult
def calculate_equalized_odds(self, predictions, protected_attr, threshold=0.1) -> FairnessMetricResult
def calculate_equal_opportunity(self, predictions, protected_attr, threshold=0.1) -> FairnessMetricResult
def calculate_all_metrics(self, predictions, protected_attr, threshold=0.1) -> Dict[FairnessDefinition, FairnessMetricResult]
def get_all_results(self) -> List[FairnessMetricResult]
def get_unfair_metrics(self) -> List[FairnessMetricResult]
```

### ComplianceFrameworkManager

```python
def add_framework(self, framework, version="1.0", description="") -> None
def add_requirement(self, framework, title, description, is_mandatory=True, ...) -> ComplianceRequirement
def check_compliance(self, framework, evidence) -> Dict[str, Any]
def get_framework_requirements(self, framework) -> List[ComplianceRequirement]
def get_overdue_requirements(self) -> List[ComplianceRequirement]
def get_compliance_summary(self) -> Dict[str, Any]
```

### TransparencyManager

```python
def create_model_card(self, model_id, model_name, intended_use, ...) -> TransparencyDocument
def create_impact_assessment(self, model_id, title, ...) -> TransparencyDocument
def get_document(self, document_id) -> Optional[TransparencyDocument]
def get_model_documents(self, model_id) -> List[TransparencyDocument]
def get_public_documents(self) -> List[TransparencyDocument]
def approve_document(self, document_id, approver) -> bool
```

### AccountabilityTracker

```python
def assign_responsibility(self, model_id, role, person_name, person_email, responsibility) -> AccountabilityEntry
def sign_off(self, entry_id) -> bool
def get_model_accountability(self, model_id) -> List[AccountabilityEntry]
def get_accountability_chain(self, model_id) -> Dict[str, Any]
```

### AuditTrail

```python
def log_event(self, event_type, description, actor, model_id=None, metadata=None) -> None
def start_audit(self, audit_type, model_id, auditor) -> AuditRecord
def complete_audit(self, audit_id, findings, overall_score, risk_level, compliant, recommendations) -> bool
def get_logs(self, event_type=None, model_id=None, limit=100) -> List[Dict]
def get_audits(self, model_id=None) -> List[AuditRecord]
def get_audit_report(self, days=30) -> Dict[str, Any]
```

### EthicsGuidelinesEngine

```python
def get_principles(self, domain=None) -> List[Dict[str, str]]
def add_custom_principle(self, principle, description, implementation) -> None
def generate_checklist(self, domain=None) -> List[Dict[str, str]]
```

### ModelRiskManager

```python
def assess_model(self, model_id, model_name, bias_findings, compliance_status, impact_areas) -> ModelRiskAssessment
def get_assessment(self, assessment_id) -> Optional[ModelRiskAssessment]
def get_model_assessments(self, model_id) -> List[ModelRiskAssessment]
def get_high_risk_models(self) -> List[ModelRiskAssessment]
def get_risk_summary(self) -> Dict[str, Any]
```

---

## Usage Patterns

### Pattern 1: Pre-Deployment Audit

```python
agent = EthicsAgent()
report = agent.run_full_assessment(
    model_id="model_v1",
    model_name="Credit Scorer",
    predictions=predictions,
    protected_attributes=["race", "gender", "age"],
    compliance_frameworks=[ComplianceFramework.EU_AI_ACT, ComplianceFramework.NIST_AI_RMF],
    impact_areas=["financial", "lending"],
)
if report["risk_assessment"]["level"] in ("high", "critical"):
    print("BLOCK DEPLOYMENT: Fix issues first")
```

### Pattern 2: Continuous Monitoring

```python
# Run weekly
results = agent.bias_detector.analyze_predictions(live_predictions, ["gender", "race"])
flagged = agent.bias_detector.get_flagged_attributes()
if flagged:
    agent.report_incident("Emerging bias detected", ...)
```

### Pattern 3: Compliance Reporting

```python
summary = agent.compliance.get_compliance_summary()
print(f"Compliance rate: {summary['compliance_rate']}%")
print(f"Overdue requirements: {summary['overdue_mandatory']}")
```

---

## Data Models Reference

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| ModelPrediction | Input prediction | id, predicted_label, actual_label, protected_attributes |
| BiasAnalysisResult | Bias finding | bias_type, bias_score, is_flagged, group_rates |
| FairnessMetricResult | Fairness metric | definition, value, is_fair, group_values |
| ComplianceRequirement | Compliance rule | framework, title, is_mandatory, is_compliant |
| TransparencyDocument | Documentation | type, title, content, model_id, is_public |
| AccountabilityEntry | Responsibility | role, person_name, responsibility, sign_off_date |
| AuditRecord | Audit result | type, findings, overall_score, risk_level |
| EthicsIncident | Incident report | title, severity, bias_type, status |
| ModelRiskAssessment | Risk finding | risk_level, risk_score, recommendations |
| GovernancePolicy | Policy | title, status, requirements, effective_date |

---

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Bias score always 0 | All groups have equal rates | Check if protected attribute is in data |
| Fairness metrics disagree | Different definitions measure different things | Use multiple metrics, not just one |
| Compliance check fails | Missing evidence | Provide evidence dict with requirement titles |
| Risk score too high | Multiple bias findings | Address highest-severity findings first |
| Audit trail incomplete | Events not logged | Ensure `log_event()` called for all actions |
| Model card not public | Not approved | Call `approve_document()` with approver |

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

---

## Checklist

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
