# Ethics Agent — System Architecture

## Overview

The Ethics Agent is a comprehensive AI governance platform covering bias
detection, fairness metric calculation, compliance framework management,
transparency documentation, accountability tracking, audit trail management,
model risk assessment, and ethics guideline generation. It provides the tools
and processes needed to ensure AI systems are fair, transparent, and
accountable throughout their lifecycle.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        EthicsAgent                                       │
│                   (Top-level Orchestrator)                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────────────┐ │
│  │  Bias         │  │  Fairness      │  │  Compliance                   │ │
│  │  Detector     │  │  Metrics       │  │  Framework Manager            │ │
│  │              │  │                │  │                              │ │
│  │  - Statistical│ │  - Demographic │  │  - EU AI Act                 │ │
│  │  - Multi-attr │ │  - Equalized   │  │  - GDPR, CCPA                │ │
│  │  - History   │  │  - Equal Opp   │  │  - NIST, ISO                  │ │
│  └──────┬───────┘  └───────┬────────┘  └──────────────┬───────────────┘ │
│         │                  │                           │                  │
│  ┌──────┴───────┐  ┌──────┴────────┐  ┌──────────────┴───────────────┐ │
│  │  Transparency │  │  Account-    │  │  Audit                        │ │
│  │  Manager      │  │  ability     │  │  Trail                        │ │
│  │              │  │  Tracker     │  │                              │ │
│  │  - Model cards│ │  - Roles     │  │  - Event logging              │ │
│  │  - Impact     │ │  - Sign-offs │  │  - Audit records              │ │
│  │  - Documents  │ │  - Chain     │  │  - Reports                    │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  EthicsGuidelinesEngine │ ModelRiskManager │ Incident Store          │ │
│  │  - Principles │ Risk assessment │ Incident reporting & tracking     │ │
│  │  - Checklists │ Mitigation recs │ Severity & status management      │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dives

### 1. BiasDetector

**Purpose**: Detects bias across protected attributes using statistical
methods, with configurable thresholds and confidence intervals.

```
┌─────────────────────────────────────────┐
│          BiasDetector                    │
├─────────────────────────────────────────┤
│  _thresholds: Dict[str, float]          │
│  _analysis_history: List[BiasAnalysis]  │
├─────────────────────────────────────────┤
│  set_threshold()           → None       │
│  analyze_predictions()     → Dict       │
│  analyze_single_attribute() → Result    │
│  get_analysis_history()    → List       │
│  get_flagged_attributes()  → List       │
│  _calculate_confidence_interval()       │
│  _calculate_significance()              │
│  _generate_recommendations()            │
└─────────────────────────────────────────┘
```

**Analysis Pipeline**:
```
Predictions + Protected Attributes
  ↓
Group by attribute value
  ↓
Calculate positive outcome rate per group
  ↓
Compute disparity (max_rate - min_rate)
  ↓
Compare to threshold
  ↓
Calculate confidence interval (95%)
  ↓
Calculate statistical significance (p-value)
  ↓
Generate recommendations
  ↓
Return BiasAnalysisResult
```

### 2. FairnessMetrics

**Purpose**: Calculates formal fairness metrics across multiple definitions
(demographic parity, equalized odds, equal opportunity).

```
┌─────────────────────────────────────────┐
│         FairnessMetrics                  │
├─────────────────────────────────────────┤
│  _results: List[FairnessMetricResult]   │
├─────────────────────────────────────────┤
│  calculate_demographic_parity() → Result│
│  calculate_equalized_odds()     → Result│
│  calculate_equal_opportunity()  → Result│
│  calculate_all_metrics()        → Dict  │
│  get_all_results()              → List  │
│  get_unfair_metrics()           → List  │
└─────────────────────────────────────────┘
```

**Fairness Definitions**:
| Definition | Formula | Interpretation |
|-----------|---------|----------------|
| Demographic Parity | P(Ŷ=1\|A=a) = P(Ŷ=1\|A=b) | Equal positive prediction rates |
| Equalized Odds | TPR/FPR equal across groups | Equal error rates |
| Equal Opportunity | TPR equal across groups | Equal true positive rates |

### 3. ComplianceFrameworkManager

**Purpose**: Manages compliance frameworks (EU AI Act, GDPR, NIST, etc.)
and requirement tracking.

```
┌─────────────────────────────────────────┐
│     ComplianceFrameworkManager          │
├─────────────────────────────────────────┤
│  _frameworks: Dict[Framework, Dict]     │
│  _requirements: Dict[str, Requirement]  │
│  _compliance_results: List[Dict]        │
├─────────────────────────────────────────┤
│  add_framework()            → None      │
│  add_requirement()          → Requirement│
│  check_compliance()         → Dict      │
│  get_framework_requirements() → List    │
│  get_overdue_requirements() → List      │
│  get_compliance_summary()   → Dict      │
└─────────────────────────────────────────┘
```

### 4. TransparencyManager

**Purpose**: Creates and manages model cards, impact assessments, and
transparency documentation.

```
┌─────────────────────────────────────────┐
│        TransparencyManager              │
├─────────────────────────────────────────┤
│  _documents: Dict[str, Document]        │
│  _model_cards: Dict[str, Dict]          │
├─────────────────────────────────────────┤
│  create_model_card()        → Document  │
│  create_impact_assessment() → Document  │
│  get_document()             → Document  │
│  get_model_documents()      → List      │
│  get_public_documents()     → List      │
│  approve_document()         → bool      │
└─────────────────────────────────────────┘
```

### 5. AccountabilityTracker

**Purpose**: Tracks responsibility assignments and sign-offs in the
AI accountability chain.

```
┌─────────────────────────────────────────┐
│       AccountabilityTracker             │
├─────────────────────────────────────────┤
│  _entries: Dict[str, Entry]             │
│  _model_ownership: Dict[str, List[str]] │
├─────────────────────────────────────────┤
│  assign_responsibility()    → Entry     │
│  sign_off()                 → bool      │
│  get_model_accountability() → List      │
│  get_accountability_chain() → Dict      │
└─────────────────────────────────────────┘
```

### 6. AuditTrail

**Purpose**: Comprehensive logging of ethics-related decisions and
audit record management.

```
┌─────────────────────────────────────────┐
│            AuditTrail                   │
├─────────────────────────────────────────┤
│  _logs: List[Dict]                      │
│  _audits: List[AuditRecord]             │
├─────────────────────────────────────────┤
│  log_event()                → None      │
│  start_audit()              → AuditRec  │
│  complete_audit()           → bool      │
│  get_logs()                 → List      │
│  get_audits()               → List      │
│  get_audit_report()         → Dict      │
└─────────────────────────────────────────┘
```

### 7. EthicsGuidelinesEngine

**Purpose**: Generates ethics principles and checklists for specific
domains (healthcare, finance, criminal justice, education).

```
┌─────────────────────────────────────────┐
│      EthicsGuidelinesEngine             │
├─────────────────────────────────────────┤
│  BASE_PRINCIPLES: List[Dict]            │
│  DOMAIN_ADDITIONS: Dict[str, List]      │
│  _custom_principles: List[Dict]         │
├─────────────────────────────────────────┤
│  get_principles()          → List[Dict] │
│  add_custom_principle()    → None       │
│  generate_checklist()      → List[Dict] │
└─────────────────────────────────────────┘
```

### 8. ModelRiskManager

**Purpose**: Comprehensive model risk assessment combining bias findings,
compliance status, and impact areas.

```
┌─────────────────────────────────────────┐
│         ModelRiskManager                │
├─────────────────────────────────────────┤
│  _assessments: Dict[str, Assessment]    │
│  _risk_policies: List[Dict]             │
├─────────────────────────────────────────┤
│  assess_model()             → Assessment│
│  get_assessment()           → Assessment│
│  get_model_assessments()    → List      │
│  get_high_risk_models()     → List      │
│  get_risk_summary()         → Dict      │
└─────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Bias Analysis Flow

```
Model Predictions + Protected Attributes
     │
     ▼
┌──────────────────────────────────┐
│  BiasDetector                    │
│  .analyze_predictions()          │
└────────────┬─────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  Group   Calculate   Compare to
  by Attr  Rates      Threshold
     │       │           │
     └───────┼───────────┘
             ▼
      Confidence Interval
             │
             ▼
      Statistical Significance
             │
             ▼
      Generate Recommendations
             │
             ▼
     BiasAnalysisResult
```

### Compliance Check Flow

```
Framework + Evidence
     │
     ▼
┌──────────────────────────────────┐
│  ComplianceFrameworkManager      │
│  .check_compliance()             │
└────────────┬─────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  Load    Check each   Count
  Reqs    Requirement  Results
     │       │           │
     └───────┼───────────┘
             ▼
      Mandatory Failed?
             │
     ┌───────┴───────┐
     ▼               ▼
    YES             NO
     │               │
  Non-Compliant   Compliant
```

### Full Assessment Flow

```
Model + Predictions + Frameworks
     │
     ▼
┌──────────────────────────────────┐
│  EthicsAgent.run_full_assessment()│
└────────────┬─────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  Bias    Fairness    Compliance
  Analysis Metrics    Check
     │       │           │
     └───────┼───────────┘
             ▼
      Risk Assessment
             │
             ▼
      Log to Audit Trail
             │
             ▼
     Return Full Report
```

---

## Design Patterns

### Strategy Pattern
Different fairness definitions (demographic parity, equalized odds, equal
opportunity) implement the same calculation interface, allowing the
FairnessMetrics engine to compute any definition without branching.

### Chain of Responsibility
Risk assessment chains bias findings, compliance failures, and impact
areas into a cumulative risk score, with each factor contributing
independently.

### Observer Pattern
The AuditTrail observes all significant events across sub-engines,
maintaining a comprehensive log without coupling sub-engines to logging.

### Template Method
Model card generation follows a fixed template (intended use, training data,
metrics, limitations, ethical considerations) with domain-specific additions.

---

## Data Model Relationships

```
EthicsAgent ─────────────────────────┐
  │                                   │
  ├── BiasDetector                    │
  │     └── BiasAnalysisResult (1:N)  │
  │                                   │
  ├── FairnessMetrics                 │
  │     └── FairnessMetricResult (1:N)│
  │                                   │
  ├── ComplianceFrameworkManager      │
  │     ├── Framework (1:N)           │
  │     └── Requirement (1:N)         │
  │                                   │
  ├── TransparencyManager             │
  │     └── Document (1:N)            │
  │                                   │
  ├── AccountabilityTracker           │
  │     └── Entry (1:N)               │
  │                                   │
  ├── AuditTrail                      │
  │     ├── Log (1:N)                 │
  │     └── AuditRecord (1:N)         │
  │                                   │
  ├── EthicsGuidelinesEngine          │
  │     └── Principle/Checklist       │
  │                                   │
  ├── ModelRiskManager                │
  │     └── Assessment (1:N)          │
  │                                   │
  ├── Incident Store (1:N)            │
  └── Policy Store (1:N)              │
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | dataclasses + Enum |
| Statistics | scipy.stats (optional) |
| Logging | stdlib logging |
| Storage | In-memory dicts (pluggable) |
| Serialization | dataclass → dict (JSON-serializable) |
| Testing | pytest + hypothesis |
| Visualization | matplotlib/plotly (optional) |

---

## Security Considerations

1. **Audit Trail Integrity**: Audit logs must be append-only and tamper-evident.
   Use cryptographic hashing for log integrity.
2. **Access Control**: Ethics assessments and compliance reports contain
   sensitive information. Restrict access to authorized personnel.
3. **Data Privacy**: Protected attribute data must be handled in compliance
   with GDPR/CCPA. Minimize data collection.
4. **Incident Confidentiality**: Ethics incidents may involve legal
   sensitivity. Ensure proper access controls and confidentiality.
5. **Model Risk Data**: Risk assessments inform business decisions. Ensure
   accuracy and prevent manipulation.

---

## Scalability Considerations

| Dimension | Current | Target |
|-----------|---------|--------|
| Predictions analyzed | 10K | 100M+ |
| Protected attributes | 12 | 30+ |
| Compliance frameworks | 10 | 50+ |
| Models assessed | 100 | 10,000+ |
| Audit records | 1K | 10,000,000+ |

**Scaling Strategy**:
- Use Apache Spark for large-scale bias analysis.
- Implement streaming bias detection for real-time monitoring.
- Shard audit trails by model_id for horizontal scaling.
- Use PostgreSQL for persistent compliance and audit data.
- Implement caching for repeated fairness metric calculations.

---

## Extension Points

1. **New Fairness Definitions**: Add to `FairnessDefinition` enum and
   implement calculation in `FairnessMetrics`.
2. **New Compliance Frameworks**: Add to `ComplianceFramework` enum and
   populate requirements.
3. **New Bias Types**: Add to `BiasType` enum and update group analysis.
4. **Custom Mitigation Strategies**: Extend `MitigationStrategy` enum
   and implement in bias correction pipeline.
5. **External Audit Integration**: Connect to third-party audit platforms
   via API adapters.

---

## Configuration

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
    public_disclosure_required: false

  accountability:
    required_roles:
      - model_owner
      - data_scientist
      - ethics_committee
    sign_off_required: true

  audit:
    retention_days: 2555  # 7 years
    auto_audit_frequency: quarterly

  risk:
    high_risk_threshold: 35
    critical_risk_threshold: 50
    reassessment_interval_days: 90
```

---

## Performance Benchmarks

| Operation | Latency (p99) | Throughput |
|-----------|---------------|------------|
| Bias analysis (10K predictions) | < 2s | 100/s |
| Fairness metric calculation | < 1s | 200/s |
| Compliance check | < 100ms | 1K/s |
| Audit log write | < 5ms | 50K/s |
| Risk assessment | < 500ms | 20/s |
| Dashboard generation | < 2s | 50/s |

---

## Testing Strategy

| Test Type | Coverage Target | Tools |
|-----------|----------------|-------|
| Unit tests | 90%+ | pytest |
| Statistical tests | Metric accuracy | scipy |
| Integration tests | Full assessment | pytest + fixtures |
| Property tests | Fairness axioms | hypothesis |
| Regression tests | Known bias cases | pytest |

### Unit Test Examples

```python
# Bias Detector Tests
def test_bias_detection():
    detector = BiasDetector()
    predictions = [
        ModelPrediction(1, 1, {"gender": "male"}),
        ModelPrediction(0, 1, {"gender": "female"}),
    ]
    results = detector.analyze_predictions(predictions, ["gender"])
    assert "gender" in results
    assert results["gender"].bias_score > 0

# Fairness Metrics Tests
def test_demographic_parity():
    fairness = FairnessMetrics()
    predictions = [
        ModelPrediction(1, 1, {"gender": "male"}),
        ModelPrediction(1, 0, {"gender": "female"}),
    ]
    result = fairness.calculate_demographic_parity(predictions, "gender")
    assert result.value >= 0
    assert result.value <= 1

# Compliance Tests
def test_compliance_check():
    manager = ComplianceFrameworkManager()
    manager.add_framework(ComplianceFramework.EU_AI_ACT)
    manager.add_requirement(ComplianceFramework.EU_AI_ACT, "Transparency", "Must be transparent")
    result = manager.check_compliance(ComplianceFramework.EU_AI_ACT, {"Transparency": True})
    assert result["compliant"]
```

### Statistical Test Examples

```python
def test_bias_statistical_significance():
    """Test that bias detection uses proper statistical tests."""
    detector = BiasDetector()
    
    # Create predictions with known bias
    predictions = create_biased_predictions(bias_rate=0.2, n=1000)
    results = detector.analyze_predictions(predictions, ["gender"])
    
    # Verify statistical significance
    assert results["gender"].is_flagged
    assert results["gender"].p_value < 0.05

def test_fairness_metric_bounds():
    """Test that fairness metrics are bounded [0, 1]."""
    fairness = FairnessMetrics()
    
    for _ in range(100):
        predictions = create_random_predictions(n=500)
        dp = fairness.calculate_demographic_parity(predictions, "gender")
        assert 0 <= dp.value <= 1
```

### Integration Test Examples

```python
def test_full_assessment():
    agent = EthicsAgent()
    
    # Create predictions
    predictions = [
        ModelPrediction(1, 1, {"gender": "male", "race": "white"}),
        ModelPrediction(0, 1, {"gender": "female", "race": "black"}),
    ]
    
    # Run full assessment
    report = agent.run_full_assessment(
        model_id="test_model",
        model_name="Test Model",
        predictions=predictions,
        protected_attributes=["gender", "race"],
        compliance_frameworks=[ComplianceFramework.EU_AI_ACT],
    )
    
    assert "bias_analysis" in report
    assert "fairness_metrics" in report
    assert "compliance" in report
    assert "risk_assessment" in report
```

### Property Test Examples

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers(0, 1), min_size=100))
def test_demographic_parity_symmetry(labels):
    """Demographic parity should be symmetric."""
    fairness = FairnessMetrics()
    predictions = create_predictions(labels)
    dp = fairness.calculate_demographic_parity(predictions, "gender")
    assert dp.value == fairness.calculate_demographic_parity(predictions, "gender")

@given(st.floats(0.0, 1.0))
def test_bias_score_bounds(bias_rate):
    """Bias score should be bounded [0, 1]."""
    detector = BiasDetector()
    predictions = create_biased_predictions(bias_rate, n=1000)
    results = detector.analyze_predictions(predictions, ["gender"])
    assert 0 <= results["gender"].bias_score <= 1
```

---

## Deployment Architecture

### Single-Instance Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVER                         │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  EthicsAgent                           │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │ │
│  │  │  Bias   │ │Fairness │ │Compliance│ │Trans-   │    │ │
│  │  │Detector │ │ Metrics │ │ Manager │ │parency  │    │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │ │
│  │  │Account- │ │  Audit  │ │  Risk   │ │Guide-   │    │ │
│  │  │ability  │ │  Trail  │ │ Manager │ │lines    │    │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  DATA LAYER                            │ │
│  │  In-Memory │ Optional DB │ Audit Storage              │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Integration with ML Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    ML PIPELINE INTEGRATION                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │  Train  │ ─► │Validate │ ─► │  Ethics │ ─► │ Deploy  │  │
│  │  Model  │    │ Model   │    │  Check  │    │ Model   │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                       │               │                      │
│                       │               ▼                      │
│                       │         ┌─────────┐                 │
│                       │         │  Block  │                 │
│                       │         │ Deploy  │                 │
│                       │         └─────────┘                 │
│                       │                                      │
│                       ▼                                      │
│                 ┌─────────┐                                  │
│                 │  Pass   │                                  │
│                 └─────────┘                                  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### Data Protection

| Data Type | Protection | Storage |
|-----------|------------|---------|
| Predictions | Encrypted | Database |
| Bias findings | Access-controlled | Audit trail |
| Model cards | Version-controlled | Document store |
| Audit logs | Immutable | Append-only log |
| Incident reports | Access-controlled | Database |

### Access Control

| Role | Permissions |
|------|-------------|
| Data Scientist | Run bias analysis, view results |
| Model Owner | Create model cards, assign accountability |
| Ethics Committee | Approve documents, conduct audits |
| Auditor | View audit trail, generate reports |
| Admin | Full access |

### Audit Trail Integrity

- All entries are timestamped and immutable
- Cryptographic hashing for tamper detection
- Append-only storage
- Regular integrity checks

---

## Monitoring and Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Bias detection rate | Flagged attributes / total | > 20% |
| Fairness compliance | Fair metrics / total | < 80% |
| Compliance rate | Compliant requirements / total | < 90% |
| Incident count | Open incidents | > 5 |
| Audit completion | Completed / started | < 80% |
| Risk score average | Mean risk score | > 35 |

### Ethics Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                    ETHICS DASHBOARD                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Bias        │  │ Fairness    │  │ Compliance  │         │
│  │ Analyses    │  │ Metrics     │  │ Rate        │         │
│  │    150      │  │   85%       │  │    92%      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Incidents   │  │ High Risk   │  │ Audits      │         │
│  │    3        │  │   Models    │  │  Completed  │         │
│  │   Open      │  │     2       │  │    12       │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Retention Policy

| Data Type | Retention | Archive After |
|-----------|-----------|---------------|
| Bias analyses | 5 years | 2 years |
| Fairness metrics | 5 years | 2 years |
| Compliance records | 7 years | 3 years |
| Model cards | Indefinite | Never |
| Audit logs | 7 years | 3 years |
| Incident reports | 5 years | 2 years |

---

## Disaster Recovery

### Backup Strategy

| Data | Frequency | Method | Recovery Time |
|------|-----------|--------|---------------|
| Bias analyses | Daily | Full dump | < 1 hour |
| Audit trail | Real-time | Replication | < 5 minutes |
| Model cards | On change | Version control | < 15 minutes |
| Compliance data | Daily | Encrypted backup | < 2 hours |

### Recovery Procedures

1. **Data corruption**: Restore from last backup
2. **Service failure**: Restart and verify state
3. **Audit trail breach**: Activate integrity verification
4. **Full outage**: Deploy to backup region

---

## Regulatory Compliance

### EU AI Act Requirements

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Risk classification | Supported | Model risk assessment |
| Transparency | Supported | Model cards |
| Human oversight | Supported | Accountability tracking |
| Robustness | Supported | Bias detection |
| Record keeping | Supported | Audit trail |

### NIST AI RMF Functions

| Function | Coverage |
|----------|----------|
| Govern | Accountability, policies |
| Map | Risk assessment, impact analysis |
| Measure | Bias detection, fairness metrics |
| Manage | Incident response, mitigation |

---

**See Also**: [GROK.md](./GROK.md) for agent identity and capabilities,
[README.md](./README.md) for quick start and API reference.
