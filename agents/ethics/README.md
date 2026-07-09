# Ethics Agent

Comprehensive AI ethics governance platform covering bias detection, fairness
metric calculation, compliance framework management, transparency documentation,
accountability tracking, audit trails, model risk assessment, and ethics
guideline generation.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Ethics Agent provides the governance infrastructure needed to build and
deploy responsible AI systems. It detects bias across 12+ protected attributes,
calculates fairness using formal definitions, manages compliance with major
frameworks (EU AI Act, GDPR, NIST, ISO), documents models for transparency,
tracks accountability chains, maintains audit trails, and assesses model risk.

Built with modular sub-engines, each component operates independently while
being orchestrated by a top-level agent for unified assessments and dashboards.

### Key Benefits

- **Zero Dependencies**: Pure Python stdlib, no external packages required
- **Statistical Rigor**: Bias claims backed by evidence, not intuition
- **Multi-Framework**: EU AI Act, GDPR, CCPA, NIST, ISO 42001 support
- **Modular Design**: Use only the components you need
- **Type-Safe**: Full type hints on all public methods
- **Extensible**: Easy to add custom bias rules, compliance frameworks

### Use Cases

| Use Case | Description |
|----------|-------------|
| Bias Detection | Analyze predictions across protected attributes |
| Fairness Metrics | Calculate DP, EO, EOpp metrics |
| Compliance | Track requirements across multiple frameworks |
| Transparency | Create model cards and impact assessments |
| Accountability | Assign roles and track sign-offs |
| Audit Trails | Log events and manage audits |
| Risk Assessment | Score and classify model risk |
| Incident Reporting | Track and resolve ethics incidents |

---

## Features

### Bias Detection
- Statistical bias analysis across 12+ protected attributes
- Configurable thresholds per attribute
- Confidence intervals and statistical significance
- Automatic recommendation generation
- Analysis history and trending
- Custom bias rule support
- Real-time monitoring capabilities

### Fairness Metrics
- Demographic Parity calculation
- Equalized Odds (TPR + FPR parity)
- Equal Opportunity (TPR parity)
- Multi-metric comparison
- Per-group fairness values
- Threshold customization
- Historical metric tracking

### Compliance Management
- 10+ frameworks (EU AI Act, GDPR, CCPA, NIST, ISO 42001, etc.)
- Requirement tracking with deadlines
- Compliance checking with evidence
- Overdue requirement alerts
- Compliance rate reporting
- Custom framework support
- Evidence attachment

### Transparency Documentation
- Model card generation
- Impact assessment creation
- Document approval workflow
- Public disclosure management
- Version tracking
- Template customization
- Bulk document generation

### Accountability
- Role-based responsibility assignment
- Sign-off tracking
- Accountability chain visualization
- Model ownership mapping
- Escalation procedures
- Deadline management
- Notification system

### Audit Trail
- Event logging with timestamps
- Audit lifecycle management (start → complete)
- Audit report generation
- History querying and filtering
- Immutable records
- Export capabilities
- Compliance evidence

### Risk Assessment
- Multi-factor risk scoring
- Risk level classification (Minimal to Critical)
- Automated recommendation generation
- High-risk model identification
- Risk trend analysis
- Mitigation tracking
- Executive summaries

### Ethics Guidelines
- 7 core AI ethics principles
- Domain-specific additions (healthcare, finance, criminal justice)
- Custom principle support
- Domain-specific checklists
- Best practice recommendations
- Training materials
- Regular updates

---

## Architecture

### Component Diagram

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
└──────────────────────────────────────────────────────────────────────────┘
```

### Governance Flow

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
```

### Bias Detection Pipeline

```
  Input Predictions → Group by Attribute → Calculate Rates →
  Compute Disparity → Apply Thresholds → Flag/Recommend
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed component diagrams,
data flows, and design patterns.

---

## Quick Start

```python
from agents.ethics.agent import (
    EthicsAgent, BiasType, ModelPrediction, ComplianceFramework,
)

agent = EthicsAgent()

# Analyze bias
predictions = [
    ModelPrediction(predicted_label=1, actual_label=1, protected_attributes={"gender": "male"}),
    ModelPrediction(predicted_label=0, actual_label=0, protected_attributes={"gender": "female"}),
]
results = agent.bias_detector.analyze_predictions(predictions, ["gender"])

# Check compliance
agent.compliance.add_framework(ComplianceFramework.EU_AI_ACT)
result = agent.compliance.check_compliance(ComplianceFramework.EU_AI_ACT, {})

print(f"Bias flagged: {any(r.is_flagged for r in results.values())}")
print(f"Compliant: {result['compliant']}")
```

---

## Installation

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -r requirements.txt
python agents/ethics/agent.py
```

### Requirements

- Python 3.10+
- No external dependencies (stdlib only)

### Platform Support

- Windows 10+
- macOS 10.15+
- Linux (Ubuntu 18.04+, Debian 9+)

---

## Usage

### Running the Demo

```bash
python agents/ethics/agent.py
```

Demonstrates bias analysis, fairness metrics, compliance checking, model
card creation, incident reporting, and risk assessment.

### Programmatic Usage

```python
from agents.ethics.agent import EthicsAgent

agent = EthicsAgent()

# Check agent status
print(agent.get_status())

# Get ethics dashboard
dashboard = agent.get_ethics_dashboard()
print(f"Bias analyses: {dashboard['bias']['total_analyses']}")
print(f"Compliance rate: {dashboard['compliance']['compliance_rate']}%")
```

### Using Individual Components

```python
from agents.ethics.agent import BiasDetector, FairnessMetrics

# Use bias detector independently
detector = BiasDetector()
results = detector.analyze_predictions(predictions, ["gender"])

# Use fairness metrics independently
fairness = FairnessMetrics()
dp = fairness.calculate_demographic_parity(predictions, "gender")
```

---

## API Reference

### EthicsAgent (Top-Level)

| Method | Description | Returns |
|--------|-------------|---------|
| `run_full_assessment(...)` | Complete assessment | `Dict` |
| `report_incident(...)` | Report incident | `EthicsIncident` |
| `create_governance_policy(...)` | Create policy | `GovernancePolicy` |
| `get_ethics_dashboard()` | Dashboard | `Dict` |
| `get_status()` | Agent status | `Dict` |

### BiasDetector

| Method | Description | Returns |
|--------|-------------|---------|
| `set_threshold(type, threshold)` | Set threshold | `None` |
| `analyze_predictions(preds, attrs)` | Analyze bias | `Dict[str, Result]` |
| `analyze_single_attribute(preds, attr)` | Single attribute | `BiasAnalysisResult` |
| `get_analysis_history(type)` | History | `List[BiasAnalysisResult]` |
| `get_flagged_attributes()` | Flagged | `List[BiasAnalysisResult]` |

### FairnessMetrics

| Method | Description | Returns |
|--------|-------------|---------|
| `calculate_demographic_parity(preds, attr)` | Demographic parity | `FairnessMetricResult` |
| `calculate_equalized_odds(preds, attr)` | Equalized odds | `FairnessMetricResult` |
| `calculate_equal_opportunity(preds, attr)` | Equal opportunity | `FairnessMetricResult` |
| `calculate_all_metrics(preds, attr)` | All metrics | `Dict[Definition, Result]` |
| `get_unfair_metrics()` | Unfair | `List[FairnessMetricResult]` |

### ComplianceFrameworkManager

| Method | Description | Returns |
|--------|-------------|---------|
| `add_framework(framework, version)` | Add framework | `None` |
| `add_requirement(framework, title, desc, ...)` | Add requirement | `Requirement` |
| `check_compliance(framework, evidence)` | Check | `Dict` |
| `get_overdue_requirements()` | Overdue | `List[Requirement]` |
| `get_compliance_summary()` | Summary | `Dict` |

### TransparencyManager

| Method | Description | Returns |
|--------|-------------|---------|
| `create_model_card(model_id, name, ...)` | Model card | `Document` |
| `create_impact_assessment(model_id, ...)` | Impact assessment | `Document` |
| `get_model_documents(model_id)` | Documents | `List[Document]` |
| `get_public_documents()` | Public docs | `List[Document]` |
| `approve_document(id, approver)` | Approve | `bool` |

### AccountabilityTracker

| Method | Description | Returns |
|--------|-------------|---------|
| `assign_responsibility(model_id, role, ...)` | Assign | `Entry` |
| `sign_off(entry_id)` | Sign off | `bool` |
| `get_model_accountability(model_id)` | Model chain | `List[Entry]` |
| `get_accountability_chain(model_id)` | Chain | `Dict` |

### AuditTrail

| Method | Description | Returns |
|--------|-------------|---------|
| `log_event(type, desc, actor, ...)` | Log event | `None` |
| `start_audit(type, model_id, auditor)` | Start audit | `AuditRecord` |
| `complete_audit(id, findings, ...)` | Complete | `bool` |
| `get_logs(type, model_id, limit)` | Get logs | `List[Dict]` |
| `get_audit_report(days)` | Report | `Dict` |

### EthicsGuidelinesEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `get_principles(domain)` | Principles | `List[Dict]` |
| `add_custom_principle(principle, ...)` | Add principle | `None` |
| `generate_checklist(domain)` | Checklist | `List[Dict]` |

### ModelRiskManager

| Method | Description | Returns |
|--------|-------------|---------|
| `assess_model(model_id, name, findings, ...)` | Assess | `RiskAssessment` |
| `get_high_risk_models()` | High risk | `List[RiskAssessment]` |
| `get_risk_summary()` | Summary | `Dict` |

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
agent.accountability.assign_responsibility("model_001", AccountabilityRole.MODEL_OWNER, "Alice", "alice@co.com", "Overall governance")
agent.accountability.assign_responsibility("model_001", AccountabilityRole.DATA_SCIENTIST, "Bob", "bob@co.com", "Model development")
agent.accountability.assign_responsibility("model_001", AccountabilityRole.ETHICS_COMMITTEE, "Ethics Board", "ethics@co.com", "Review and approval")

chain = agent.accountability.get_accountability_chain("model_001")
print(f"All signed off: {chain['all_signed_off']}")
```

---

## Configuration

### Agent Configuration (YAML)

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

### Environment Variables

```bash
# Model Registry
MLFLOW_TRACKING_URI=...

# Notification
SLACK_WEBHOOK_URL=...
EMAIL_SMTP_HOST=...

# Storage
AUDIT_STORAGE_PATH=/var/audit
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

### Governance Best Practices

- Establish an AI ethics board
- Create clear escalation procedures
- Maintain audit trails for all decisions
- Provide regular training on responsible AI
- Document all model changes

### Compliance Best Practices

- Map requirements to specific model components
- Maintain evidence of compliance
- Track deadline adherence
- Conduct regular compliance reviews
- Prepare for external audits

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Bias score always 0 | All groups have equal outcomes | Check if attribute data is present |
| Metrics disagree | Different definitions measure different things | Use multiple metrics |
| Compliance check fails | Missing evidence dict | Provide evidence for each requirement |
| Risk score too high | Multiple issues found | Address highest-severity first |
| Audit trail gaps | Events not logged | Ensure log_event() called |
| Model card missing | Not created | Call create_model_card() |
| At-risk list empty | No high-risk models | Lower risk threshold |
| Incident not resolving | Missing resolution | Set resolved_at timestamp |

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Full type hints on all public methods
- Docstrings for all classes and public methods
- Zero external dependencies (stdlib only)
- Follow existing naming conventions
- Write tests for new functionality
- Update documentation for API changes

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[GROK.md](./GROK.md) for agent identity and operational guidelines.