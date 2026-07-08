# Change Management Agent

Comprehensive organizational change management with ADKAR modeling, stakeholder analysis, resistance management, communication planning, training development, and readiness assessment.

## Table of Contents

- [Overview](#overview)
- [Use Cases](#use-cases)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites and Requirements](#prerequisites-and-requirements)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Creating a Change Plan](#creating-a-change-plan)
  - [Stakeholder Analysis](#stakeholder-analysis)
  - [ADKAR Evaluation](#adkar-evaluation)
  - [Communication Planning](#communication-planning)
  - [Training Development](#training-development)
  - [Readiness Assessment](#readiness-assessment)
  - [Resistance Management](#resistance-management)
  - [Risk Management](#risk-management)
  - [Milestone Tracking](#milestone-tracking)
- [API Reference](#api-reference)
  - [ChangeManagementAgent](#changemanagementagent)
  - [ADKARModel](#adkarmodel)
  - [StakeholderAnalyzer](#stakeholderanalyzer)
  - [ResistanceManager](#resistancemanager)
  - [CommunicationPlanner](#communicationplanner)
  - [TrainingDeveloper](#trainingdeveloper)
  - [ReadinessAssessor](#readinessassessor)
  - [RiskManager](#riskmanager)
  - [MilestoneTracker](#milestonetracker)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Examples](#examples)
  - [Enterprise Cloud Migration](#example-1-enterprise-cloud-migration)
  - [Organizational Restructuring](#example-2-organizational-restructuring)
  - [Process Automation Rollout](#example-3-process-automation-rollout)
  - [Mergers and Acquisitions](#example-4-mergers-and-acquisitions)
  - [Compliance and Regulatory Change](#example-5-compliance-and-regulatory-change)
  - [Remote Work Transition](#example-6-remote-work-transition)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Deployment Options](#deployment-options)
- [Extending the Agent](#extending-the-agent)
- [FAQ](#faq)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Change Management Agent is a Python-based system for managing enterprise-scale organizational transformations. It implements the ADKAR individual change model alongside structured stakeholder analysis to provide a comprehensive approach to change readiness and resistance management.

### Key Capabilities

- Change plan creation with auto-generated phases and milestones
- Stakeholder mapping on power/interest grid
- ADKAR readiness evaluation with bottleneck identification
- Communication plan generation across multiple channels
- Training program development aligned to ADKAR phases
- Organizational readiness assessment across 8 dimensions
- Resistance tracking with intervention planning
- Risk identification and mitigation tracking
- Milestone progress monitoring with status updates
- Dashboard generation for executive reporting

### When to Use This Agent

1. Planning organizational restructuring or transformations
2. Implementing new technology systems (ERP, CRM, cloud migrations)
3. Merging with or acquiring other organizations
4. Rolling out new processes or compliance requirements
5. Transitioning to new work models (remote, hybrid, agile)
6. Needing to understand stakeholder readiness before a major change
7. Tracking resistance patterns across organizational units
8. Generating structured communication plans for change initiatives
9. Developing training programs for new skills or processes
10. Assessing organizational readiness for transformation

---

## Use Cases

| Use Case | Description |
|----------|-------------|
| Technology Adoption | Cloud platforms, AI tools, automation systems |
| Process Improvement | Six Sigma, ISO certifications, workflow redesigns |
| Mergers and Acquisitions | Integration of acquired companies |
| Compliance Changes | GDPR, SOX, HIPAA regulatory compliance |
| Remote Work Transitions | Shifting to remote or hybrid models |
| Digital Transformation | Large-scale digital transformation programs |

---

## Features

| Feature | Description |
|---------|-------------|
| Change Planning | Create comprehensive change plans with phases, milestones, and objectives |
| Stakeholder Analysis | Map stakeholders by influence, interest, impact, and resistance |
| ADKAR Model | Evaluate individual readiness across 5 dimensions |
| Communication Planning | Generate structured communication schedules across channels |
| Training Development | Create ADKAR-aligned training modules with enrollment tracking |
| Resistance Management | Track resistance levels and generate intervention plans |
| Readiness Assessment | Evaluate organizational readiness across 8 dimensions |
| Risk Management | Identify, assess, and track mitigation strategies |
| Milestone Tracking | Monitor progress against planned milestones with status updates |
| Dashboard | Unified view of all change initiative metrics |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Change Management Agent                          │
├─────────────────────────────────────────────────────────────────────┤
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐          │
│  │   Change   │ │Stakeholder │ │   ADKAR   │ │Communica- │          │
│  │   Plan     │ │ Analyzer   │ │ Evaluator │ │tion Plan  │          │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘          │
│        │              │              │              │                │
│  ┌─────┴─────┐ ┌──────┴─────┐ ┌──────┴─────┐ ┌─────┴─────┐        │
│  │Resistanc. │ │  Training  │ │ Readiness  │ │   Risk    │        │
│  │  Manager  │ │Developer   │ │  Assessor  │ │  Manager  │        │
│  └───────────┘ └────────────┘ └────────────┘ └───────────┘        │
│        │              │              │              │                │
│  ┌─────┴──────────────┴──────────────┴──────────────┴─────┐        │
│  │                    Milestone Tracker                    │        │
│  └────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites and Requirements

### System Requirements

- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 512MB RAM (2GB+ recommended for large initiatives)
- **Disk Space**: 100MB for agent + storage for initiative data

### Python Dependencies

```txt
python-dateutil>=2.8.0
dataclasses>=0.6;python_version<"3.7"
typing-extensions>=3.7.4;python_version<"3.8"
pandas>=1.3.0          # Optional - for data analysis
matplotlib>=3.4.0      # Optional - for visualization
openpyxl>=3.0.0        # Optional - for Excel export
```

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python -c "from agents.change_management.agent import ChangeManagementAgent; print('OK')"
```

### Environment Variables (Optional)

```bash
CHANGE_MGMT_STORAGE_PATH=/path/to/data
CHANGE_MGMT_LOG_LEVEL=INFO
CHANGE_MGMT_SLACK_WEBHOOK=https://hooks.slack.com/...
```

---

## Quick Start

### Basic Initialization

```python
from agents.change_management.agent import ChangeManagementAgent

# Initialize with default configuration
agent = ChangeManagementAgent({"user": "change_manager"})

# Initialize with custom configuration
agent = ChangeManagementAgent({
    "user": "change_manager",
    "default_timeline_weeks": 52,
    "adkar_ready_threshold": 0.75,
    "communication_channels": ["email", "town_hall", "one_on_one", "slack"],
})

# Check agent status
status = agent.get_status()
print(f"Agent initialized: {status['status']}")
```

### Creating Your First Change Plan

```python
plan = agent.create_change_plan(
    initiative_name="Cloud Migration 2024",
    change_type="technological",
    description="Migrating on-premise infrastructure to AWS cloud platform",
    objectives=[
        "Migrate 100% of production workloads to AWS",
        "Reduce infrastructure costs by 35%",
        "Improve deployment frequency from monthly to weekly",
    ],
    timeline_weeks=26,
    budget=1500000.0,
)

print(f"Plan created: {plan['plan_id']}")
print(f"Phases: {len(plan['phases'])}")
```

### Full Workflow Example

```python
# 1. Create change plan
plan = agent.create_change_plan(
    initiative_name="ERP Implementation",
    change_type="digital_transformation",
    objectives=["Replace legacy ERP with modern cloud ERP"],
    timeline_weeks=52,
)

# 2. Add stakeholders
agent.add_stakeholder(
    plan_id=plan["plan_id"],
    name="Sarah Chen",
    role="CTO",
    department="IT",
    impact_level="critical",
    resistance_level="champion",
    influence_score=0.9,
)

# 3. Evaluate ADKAR readiness
for stakeholder in agent._stakeholders.list_stakeholders():
    agent.evaluate_adkar(
        plan_id=plan["plan_id"],
        stakeholder_id=stakeholder.id,
        scores={"awareness": 0.8, "desire": 0.6, "knowledge": 0.4,
                "ability": 0.3, "reinforcement": 0.5},
    )

# 4. Generate plans and assess readiness
comm_plan = agent.develop_communication_plan(plan["plan_id"])
training = agent.develop_training_program(plan["plan_id"])
readiness = agent.assess_readiness(plan["plan_id"])

print(f"Readiness: {readiness['readiness_level']}")
```

---

## Usage

### Creating a Change Plan

```python
plan = agent.create_change_plan(
    initiative_name="Digital Transformation",
    change_type="digital_transformation",
    description="Moving from legacy systems to modern cloud-native architecture",
    objectives=[
        "Migrate 80% of workloads to cloud within 12 months",
        "Reduce infrastructure costs by 40%",
        "Improve deployment frequency from monthly to daily",
    ],
    timeline_weeks=52,
    budget=2000000.0,
)

# Auto-generates 5 phases, 6 milestones, stakeholder framework
for phase in plan["phases"]:
    print(f"  {phase['name']}: {phase['start_date']} to {phase['end_date']}")
```

#### Plan Types

| Type | Description | Typical Duration |
|------|-------------|-----------------|
| `technological` | Technology adoption or migration | 12-52 weeks |
| `process` | Process improvement or redesign | 8-26 weeks |
| `organizational` | Restructuring or reorganization | 12-52 weeks |
| `cultural` | Culture change initiatives | 26-104 weeks |
| `compliance` | Regulatory compliance changes | 8-52 weeks |
| `digital_transformation` | Broad digital transformation | 26-104 weeks |
| `merger_acquisition` | M&A integration | 26-104 weeks |

### Stakeholder Analysis

```python
stakeholders = [
    {"name": "CTO", "role": "Executive Sponsor", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 0.9, "engagement_score": 0.95},
    {"name": "VP Engineering", "role": "Implementation Lead", "impact_level": "high",
     "resistance_level": "supporter", "influence_score": 0.7, "engagement_score": 0.8},
    {"name": "Senior Developer", "role": "Technical Lead", "impact_level": "medium",
     "resistance_level": "neutral", "influence_score": 0.5,
     "concerns": ["learning curve", "tool changes"]},
]

for s in stakeholders:
    agent.add_stakeholder(plan_id=plan["plan_id"], **s)

# Get engagement strategies
for s in agent._stakeholders.list_stakeholders():
    strategy = agent._stakeholders.engagement_strategy(s.id)
    print(f"{s.name}: {strategy['strategy']['approach']}")

# Classify by power/interest grid
grid = agent._stakeholders.classify_by_influence_interest()
for quadrant, stakeholders in grid.items():
    print(f"  {quadrant}: {[s.name for s in stakeholders]}")

# Identify champions and risks
champions = agent._stakeholders.identify_champions()
risks = agent._stakeholders.identify_risks()
```

### ADKAR Evaluation

```python
adkar = agent.evaluate_adkar(
    plan_id=plan["plan_id"],
    stakeholder_id="stakeholder_id",
    scores={
        "awareness": 0.8,
        "desire": 0.6,
        "knowledge": 0.4,
        "ability": 0.3,
        "reinforcement": 0.5,
    },
)

# Check bottleneck
bottleneck = agent._adkar.get_bottleneck("stakeholder_id")
if bottleneck:
    print(f"Bottleneck: {bottleneck['phase']} ({bottleneck['score']})")
    print(f"Recommendation: {bottleneck['recommendation']}")

# Compare readiness across stakeholders
comparison = agent._adkar.compare_readiness([s.id for s in agent._stakeholders.list_stakeholders()])

# Organizational readiness
org_readiness = agent._adkar.overall_organizational_readiness([s.id for s in agent._stakeholders.list_stakeholders()])
```

### Communication Planning

```python
comm_plan = agent.develop_communication_plan(plan_id=plan["plan_id"])

for comm in comm_plan["communication_schedule"][:5]:
    print(f"{comm['title']}: {comm['channel']} on {comm['scheduled_date']}")
```

### Training Development

```python
training = agent.develop_training_program(plan_id=plan["plan_id"])

for module in training["modules"]:
    print(f"{module['title']}: {module['duration_hours']}h ({module['adkar_phase']})")

# Enroll participants
agent._training.enroll_participant(
    module_id=training["modules"][0]["id"],
    participant_id="emp_001",
    participant_name="John Smith",
)
```

### Readiness Assessment

```python
readiness = agent.assess_readiness(plan["plan_id"], scores={
    "leadership_commitment": 0.8,
    "employee_engagement": 0.6,
    "organizational_culture": 0.5,
    "technical_capability": 0.7,
    "resource_availability": 0.6,
    "change_history": 0.4,
    "communication_infrastructure": 0.7,
    "training_capacity": 0.5,
})

print(f"Level: {readiness['readiness_level']}")
for gap in readiness["gaps"]:
    print(f"  - {gap['dimension']}: {gap['severity']}")
```

### Resistance Management

```python
agent._resistance.add_resistance(
    plan_id=plan["plan_id"],
    stakeholder_id="stakeholder_id",
    level="high",
    root_cause="fear of job loss",
    description="Strong resistance due to perceived threat to job security",
    affected_area="technology_adoption",
)

summary = agent.get_resistance_summary()
interventions = agent._resistance.generate_intervention_plan("stakeholder_id")
```

### Risk Management

```python
agent._risk.add_risk(
    plan_id=plan["plan_id"],
    title="Key person departure",
    description="Risk of critical team members leaving during transition",
    likelihood=0.3,
    impact=0.8,
    risk_level="high",
    mitigation_strategy="Cross-training and knowledge documentation",
    owner="HR Director",
)

risks = agent._risk.get_risks_by_level(plan["plan_id"])
```

### Milestone Tracking

```python
agent._milestone.update_milestone_status(
    plan_id=plan["plan_id"],
    milestone_id="milestone_id",
    status="in_progress",
    progress=0.45,
    notes="On track, slight delay in vendor selection",
)

progress = agent._milestone.get_progress_summary(plan["plan_id"])
print(f"Overall Progress: {progress['overall_progress']}%")
```

---

## API Reference

### ChangeManagementAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_change_plan()` | initiative_name: str, change_type: str, description: str, objectives: list[str], timeline_weeks: int, budget: float | Plan dict |
| `add_stakeholder()` | plan_id: str, name: str, role: str, department: str, impact_level: str, resistance_level: str, influence_score: float, engagement_score: float, concerns: list[str] | Stakeholder dict |
| `evaluate_adkar()` | plan_id: str, stakeholder_id: str, scores: dict[str, float] | Evaluation dict |
| `develop_communication_plan()` | plan_id: str | Communication plan dict |
| `develop_training_program()` | plan_id: str | Training program dict |
| `assess_readiness()` | plan_id: str, scores: dict[str, float] | Readiness dict |
| `get_resistance_summary()` | plan_id: str | Summary dict |
| `get_plan_status()` | plan_id: str | Status dict |
| `list_plans()` | — | List of plan dicts |
| `get_status()` | — | Agent status dict |

### ADKARModel

| Method | Parameters | Returns |
|--------|-----------|---------|
| `evaluate_stakeholder()` | stakeholder_id: str, scores: dict | Evaluation with bottlenecks |
| `get_bottleneck()` | stakeholder_id: str | Bottleneck dict or None |
| `compare_readiness()` | stakeholder_ids: list[str] | Comparison matrix |
| `overall_organizational_readiness()` | stakeholder_ids: list[str] | Aggregate readiness |

### StakeholderAnalyzer

| Method | Parameters | Returns |
|--------|-----------|---------|
| `register_stakeholder()` | stakeholder: Stakeholder | Stakeholder ID |
| `classify_by_influence_interest()` | — | Power/interest grid |
| `identify_champions()` | — | List of champions |
| `identify_risks()` | — | Risk-ranked stakeholders |
| `engagement_strategy()` | stakeholder_id: str | Strategy dict |
| `list_stakeholders()` | — | List of Stakeholder objects |
| `get_stakeholder()` | stakeholder_id: str | Stakeholder or None |

### ResistanceManager

| Method | Parameters | Returns |
|--------|-----------|---------|
| `add_resistance()` | plan_id: str, stakeholder_id: str, level: str, root_cause: str, description: str, affected_area: str | Resistance ID |
| `generate_intervention_plan()` | stakeholder_id: str | List of interventions |
| `get_resistance_by_level()` | plan_id: str | Grouped by level |
| `update_resistance()` | resistance_id: str, level: str, status: str | bool |

### CommunicationPlanner

| Method | Parameters | Returns |
|--------|-----------|---------|
| `generate_schedule()` | plan_id: str, phases: list, stakeholders: list | Communication schedule |
| `create_message()` | title: str, channel: str, audience: str, content: str, scheduled_date: str, sender: str | Message dict |
| `get_channel_matrix()` | plan_id: str | Channel-audience mapping |

### TrainingDeveloper

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_program()` | plan_id: str, modules: list | Training program |
| `create_module()` | title: str, adkar_phase: str, duration_hours: float, format: str, objectives: list, prerequisites: list | Module dict |
| `enroll_participant()` | module_id: str, participant_id: str, participant_name: str | bool |
| `get_enrolled()` | module_id: str | List of participants |
| `update_progress()` | module_id: str, participant_id: str, progress: float, status: str | bool |

### ReadinessAssessor

| Method | Parameters | Returns |
|--------|-----------|---------|
| `assess()` | plan_id: str, scores: dict | Assessment dict |
| `get_dimensions()` | — | List of dimension names |
| `calculate_overall()` | scores: dict | Weighted score |
| `identify_gaps()` | scores: dict, threshold: float | List of gaps |

### RiskManager

| Method | Parameters | Returns |
|--------|-----------|---------|
| `add_risk()` | plan_id: str, title: str, description: str, likelihood: float, impact: float, risk_level: str, mitigation_strategy: str, owner: str | Risk ID |
| `get_risks_by_level()` | plan_id: str | Grouped by level |
| `update_risk()` | risk_id: str, status: str, mitigation_progress: float | bool |
| `calculate_risk_score()` | likelihood: float, impact: float | float |

### MilestoneTracker

| Method | Parameters | Returns |
|--------|-----------|---------|
| `update_milestone_status()` | plan_id: str, milestone_id: str, status: str, progress: float, notes: str | bool |
| `get_progress_summary()` | plan_id: str | Progress summary |
| `get_milestones_by_status()` | plan_id: str, status: str | List of milestones |
| `calculate_phase_progress()` | plan_id: str, phase: str | float |

---

## Data Models

### ChangePlan

```python
@dataclass
class ChangePlan:
    plan_id: str
    initiative_name: str
    change_type: str
    description: str
    objectives: list[str]
    timeline_weeks: int
    budget: float
    status: str          # "active", "completed", "paused", "cancelled"
    phases: list[dict]
    milestones: list[dict]
    created_date: str
    updated_date: str
```

### Stakeholder

```python
@dataclass
class Stakeholder:
    id: str
    name: str
    role: str
    department: str
    impact_level: str    # "low", "medium", "high", "critical"
    resistance_level: str # "champion", "supporter", "neutral", "passive", "blocker"
    influence_score: float  # 0.0-1.0
    engagement_score: float # 0.0-1.0
    concerns: list[str]
    adkar_scores: dict
```

### CommunicationMessage

```python
@dataclass
class CommunicationMessage:
    id: str
    title: str
    channel: str
    audience: str
    sender: str
    content: str
    scheduled_date: str
    status: str          # "scheduled", "sent", "failed"
```

### TrainingModule

```python
@dataclass
class TrainingModule:
    id: str
    title: str
    adkar_phase: str
    duration_hours: float
    format: str          # "in_person", "virtual", "self_paced", "workshop"
    objectives: list[str]
    prerequisites: list[str]
    enrolled: list[dict]
```

### ResistanceEntry

```python
@dataclass
class ResistanceEntry:
    id: str
    plan_id: str
    stakeholder_id: str
    level: str           # "none", "low", "moderate", "high", "blocking"
    root_cause: str
    description: str
    affected_area: str
    status: str          # "active", "resolved", "escalated"
```

### RiskEntry

```python
@dataclass
class RiskEntry:
    id: str
    plan_id: str
    title: str
    description: str
    likelihood: float    # 0.0-1.0
    impact: float        # 0.0-1.0
    risk_level: str      # "low", "medium", "high", "critical"
    mitigation_strategy: str
    owner: str
    status: str          # "open", "mitigating", "closed", "realized"
```

### Milestone

```python
@dataclass
class Milestone:
    id: str
    plan_id: str
    name: str
    phase: str
    target_date: str
    status: str          # "not_started", "in_progress", "completed", "delayed"
    progress: float      # 0.0-1.0
```

---

## Configuration

### Default Configuration

```python
config = {
    "user": "change_manager",
    "default_timeline_weeks": 26,
    "adkar_ready_threshold": 0.7,
    "adkar_partial_threshold": 0.4,
    "communication_channels": ["email", "town_hall", "one_on_one", "workshop", "newsletter", "slack"],
    "resistance_intervention_threshold": "moderate",
    "storage_backend": "memory",
    "storage_path": None,
    "log_level": "INFO",
    "enable_notifications": False,
    "budget_currency": "USD",
    "adkar_phase_weights": {
        "awareness": 0.15,
        "desire": 0.20,
        "knowledge": 0.25,
        "ability": 0.25,
        "reinforcement": 0.15,
    },
    "dimension_weights": {
        "leadership_commitment": 0.20,
        "employee_engagement": 0.15,
        "organizational_culture": 0.15,
        "technical_capability": 0.15,
        "resource_availability": 0.10,
        "change_history": 0.10,
        "communication_infrastructure": 0.05,
        "training_capacity": 0.10,
    },
}
agent = ChangeManagementAgent(config)
```

### Advanced Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `user` | str | `"change_manager"` | User identifier for audit logging |
| `default_timeline_weeks` | int | `26` | Default plan duration |
| `adkar_ready_threshold` | float | `0.7` | Score above which stakeholder is "ready" |
| `adkar_partial_threshold` | float | `0.4` | Score below which stakeholder is "not_ready" |
| `communication_channels` | list | 6 channels | Available communication channels |
| `resistance_intervention_threshold` | str | `"moderate"` | Resistance level triggering intervention |
| `storage_backend` | str | `"memory"` | `"memory"` or `"file"` |
| `storage_path` | str | `None` | File path for persistence |
| `log_level` | str | `"INFO"` | Logging level |
| `enable_notifications` | bool | `False` | Enable external notifications |
| `budget_currency` | str | `"USD"` | Currency for budget tracking |
| `adkar_phase_weights` | dict | See defaults | Weights for ADKAR scoring |
| `dimension_weights` | dict | See defaults | Weights for readiness calculation |

### Environment-Specific Configuration

```python
# Development
DEV_CONFIG = {
    "storage_backend": "memory",
    "log_level": "DEBUG",
    "default_timeline_weeks": 4,
}

# Production
PROD_CONFIG = {
    "storage_backend": "file",
    "storage_path": "/var/data/change_management",
    "log_level": "WARNING",
    "enable_notifications": True,
    "notification_channels": ["slack", "email"],
}

# Enterprise
ENTERPRISE_CONFIG = {
    "storage_backend": "file",
    "storage_path": "/enterprise/data/change_mgmt",
    "enable_audit_log": True,
    "max_stakeholders": 5000,
    "adkar_ready_threshold": 0.75,
}
```

---

## Examples

### Example 1: Enterprise Cloud Migration

```python
agent = ChangeManagementAgent({
    "user": "cloud_migration_lead",
    "default_timeline_weeks": 52,
})

plan = agent.create_change_plan(
    initiative_name="AWS Cloud Migration 2024",
    change_type="technological",
    description="Migrating all on-premise workloads to AWS cloud platform",
    objectives=["Migrate 100% of production workloads", "Reduce costs by 35%"],
    timeline_weeks=52,
    budget=5000000.0,
)

# Add executive sponsors
for exec in [
    {"name": "CEO", "role": "Executive Sponsor", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 1.0},
    {"name": "CTO", "role": "Technical Sponsor", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 0.9},
    {"name": "CFO", "role": "Financial Sponsor", "impact_level": "high",
     "resistance_level": "supporter", "influence_score": 0.8,
     "concerns": ["budget overrun", "ROI timeline"]},
]:
    agent.add_stakeholder(plan_id=plan["plan_id"], **exec)

# Generate all plans
comm_plan = agent.develop_communication_plan(plan["plan_id"])
training = agent.develop_training_program(plan["plan_id"])
readiness = agent.assess_readiness(plan["plan_id"])

print(f"Cloud Migration Ready: {readiness['readiness_level']}")
```

### Example 2: Organizational Restructuring

```python
agent = ChangeManagementAgent({"user": "org_design_lead"})

plan = agent.create_change_plan(
    initiative_name="Product Team Restructuring",
    change_type="organizational",
    description="Reorganizing from functional departments to cross-functional product teams",
    objectives=["Create 6 product teams by Q2", "Improve time-to-market by 40%"],
    timeline_weeks=26,
    budget=500000.0,
)

# Add stakeholders with varying resistance
for s in [
    {"name": "VP Engineering", "role": "Restructuring Lead", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 0.9},
    {"name": "Engineering Manager", "role": "Manager", "impact_level": "high",
     "resistance_level": "blocker", "influence_score": 0.7,
     "concerns": ["loss of domain expertise", "team instability"]},
]:
    agent.add_stakeholder(plan_id=plan["plan_id"], **s)

readiness = agent.assess_readiness(plan["plan_id"])
print(f"Restructuring Readiness: {readiness['readiness_level']}")
```

### Example 3: Process Automation Rollout

```python
agent = ChangeManagementAgent({"user": "process_automation_lead", "default_timeline_weeks": 16})

plan = agent.create_change_plan(
    initiative_name="Finance Process Automation",
    change_type="process",
    objectives=["Automate 80% of manual invoice processing", "Reduce processing time by 60%"],
    timeline_weeks=16,
    budget=750000.0,
)

for s in [
    {"name": "CFO", "role": "Executive Sponsor", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 0.9},
    {"name": "AP Clerk", "role": "End User", "impact_level": "high",
     "resistance_level": "blocker", "influence_score": 0.2,
     "concerns": ["job displacement", "learning new systems"]},
]:
    agent.add_stakeholder(plan_id=plan["plan_id"], **s)

training = agent.develop_training_program(plan["plan_id"])
print(f"Training modules: {len(training['modules'])}")
```

### Example 4: Mergers and Acquisitions

```python
agent = ChangeManagementAgent({"user": "ma_integration_lead", "default_timeline_weeks": 78})

plan = agent.create_change_plan(
    initiative_name="Acme Corp Integration",
    change_type="merger_acquisition",
    objectives=["Complete technology integration within 12 months", "Retain 90% of key talent"],
    timeline_weeks=78,
    budget=10000000.0,
)

for s in [
    {"name": "Acme CEO", "role": "Integration Partner", "impact_level": "critical",
     "resistance_level": "supporter", "influence_score": 0.8,
     "concerns": ["autonomy loss", "cultural changes"]},
    {"name": "Our CEO", "role": "Acquisition Sponsor", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 1.0},
]:
    agent.add_stakeholder(plan_id=plan["plan_id"], **s)

readiness = agent.assess_readiness(plan["plan_id"])
print(f"M&A Integration Readiness: {readiness['readiness_level']}")
```

### Example 5: Compliance and Regulatory Change

```python
agent = ChangeManagementAgent({"user": "compliance_lead"})

plan = agent.create_change_plan(
    initiative_name="GDPR Compliance Implementation",
    change_type="compliance",
    objectives=["Complete DPIAs for all systems", "Train 100% of data-handling staff"],
    timeline_weeks=26,
    budget=1200000.0,
)

for s in [
    {"name": "Legal Counsel", "role": "Compliance Sponsor", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 0.9},
    {"name": "Marketing Director", "role": "Business Process Owner", "impact_level": "high",
     "resistance_level": "blocker", "influence_score": 0.6,
     "concerns": ["campaign impact", "consent requirements"]},
]:
    agent.add_stakeholder(plan_id=plan["plan_id"], **s)

readiness = agent.assess_readiness(plan["plan_id"])
print(f"GDPR Compliance Readiness: {readiness['readiness_level']}")
```

### Example 6: Remote Work Transition

```python
agent = ChangeManagementAgent({"user": "workplace_transformation_lead"})

plan = agent.create_change_plan(
    initiative_name="Hybrid Work Model Transition",
    change_type="cultural",
    objectives=["Enable 80% of roles for hybrid work", "Achieve 75%+ employee satisfaction"],
    timeline_weeks=16,
    budget=300000.0,
)

for s in [
    {"name": "CHRO", "role": "Workplace Transformation Lead", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 0.9},
    {"name": "Office Manager", "role": "Facilities Lead", "impact_level": "high",
     "resistance_level": "blocker", "influence_score": 0.5,
     "concerns": ["office utilization", "team cohesion"]},
]:
    agent.add_stakeholder(plan_id=plan["plan_id"], **s)

readiness = agent.assess_readiness(plan["plan_id"])
print(f"Hybrid Work Readiness: {readiness['readiness_level']}")
```

---

## Best Practices

1. **Start with Stakeholder Analysis** — Before planning anything, understand who is affected and how. Map stakeholders on the power/interest grid.

2. **Evaluate ADKAR Early** — Individual readiness determines organizational readiness. Conduct assessments early to identify bottlenecks.

3. **Communicate Consistently** — Use the generated communication plan as your baseline. Consistent, multi-channel communication builds awareness.

4. **Address Resistance Proactively** — Don't wait for resistance to escalate. Identify early warning signs and intervene with appropriate strategies.

5. **Measure Readiness Regularly** — Re-assess before major milestones. Readiness levels change over time as stakeholders progress.

6. **Reinforce Change** — Without reinforcement, organizations regress to old behaviors. Build reinforcement activities into the plan from the beginning.

7. **Customize Training Programs** — One-size-fits-all training doesn't work. Use ADKAR bottleneck analysis to create targeted programs.

8. **Engage Champions Early** — Change champions are your most valuable asset. Identify them early, equip them with information, and leverage their influence.

9. **Track Metrics Continuously** — Monitor leading indicators (engagement, readiness scores) not just lagging indicators (adoption rates).

10. **Adapt to Feedback** — Change plans are living documents. Regularly review feedback and adjust communication, training, and intervention strategies.

11. **Document Lessons Learned** — Capture what works and what doesn't for future initiatives. Build a knowledge base of successful change patterns.

12. **Secure Executive Sponsorship** — Visible, active executive sponsorship is the single strongest predictor of change success.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Plan phases don't match timeline | Adjust `timeline_weeks` parameter; phases auto-calculate from total duration |
| Stakeholder not found | Verify ID from `add_stakeholder` return value; IDs are case-sensitive |
| ADKAR bottleneck unclear | Ensure all 5 phases have scores; bottleneck is the lowest-scoring phase |
| Communication plan empty | Add stakeholders with departments first; communications target specific audiences |
| Training modules missing | Verify plan has stakeholders for module targeting; add more stakeholders if needed |
| Resistance not tracking | Ensure `resistance_level` is one of: champion, supporter, neutral, passive, blocker |
| Readiness assessment returns "not_ready" | Scores below `adkar_partial_threshold` indicate not ready; improve dimension scores |
| Budget not calculating | Ensure `budget` parameter is a float (e.g., `1000000.0` not `1000000`) |
| Milestones not updating | Verify `milestone_id` from plan data; use `get_plan_status` to check IDs |
| Interventions not generating | Ensure stakeholder has resistance entries; check `get_resistance_summary` |
| Dashboard showing stale data | Call `get_status()` to refresh; in-memory backend updates immediately |
| Phase dates incorrect | Check `timeline_weeks` parameter; dates auto-calculate from plan creation |
| Stakeholder grid empty | Ensure `influence_score` and `engagement_score` are set (0.0-1.0 range) |
| Training enrollment failing | Verify `module_id` and `participant_id` are valid; check for duplicates |
| Organization readiness skewed | Check `dimension_weights` configuration; ensure scores are balanced |

---

## Deployment Options

### Local Development

```bash
python agents/change-management/agent.py
```

### As a Library

```python
from agents.change_management.agent import ChangeManagementAgent
agent = ChangeManagementAgent(config)
```

### As a Microservice (FastAPI)

```python
from fastapi import FastAPI
from agents.change_management.agent import ChangeManagementAgent

app = FastAPI()
agent = ChangeManagementAgent({"user": "api_user"})

@app.post("/plans")
def create_plan(plan_data: dict):
    return agent.create_change_plan(**plan_data)

@app.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    return agent.get_plan_status(plan_id)
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "agents/change-management/agent.py"]
```

### Persistent Storage

```python
agent = ChangeManagementAgent({
    "storage_backend": "file",
    "storage_path": "/var/data/change_management",
})
```

---

## Extending the Agent

### Custom ADKAR Phases

```python
config = {
    "adkar_phases": ["awareness", "desire", "knowledge", "ability", "reinforcement", "sustainability"],
}
agent = ChangeManagementAgent(config)
```

### Custom Stakeholder Classification

```python
config = {
    "stakeholder_impact_levels": {
        "minimal": {"description": "Almost no impact", "engagement": "monitor"},
        "low": {"description": "Minor impact", "engagement": "monitor"},
        "medium": {"description": "Moderate impact", "engagement": "keep_informed"},
        "high": {"description": "Significant impact", "engagement": "keep_satisfied"},
        "critical": {"description": "Major impact", "engagement": "manage_closely"},
        "transformative": {"description": "Complete role change", "engagement": "champion"},
    },
}
agent = ChangeManagementAgent(config)
```

### Custom Communication Channels

```python
config = {
    "communication_channels": [
        "email", "town_hall", "one_on_one", "workshop",
        "slack", "teams", "intranet", "newsletter",
        "manager_cascade", "skip_level",
    ],
}
agent = ChangeManagementAgent(config)
```

### Plugin Architecture

```python
class CustomPlugin:
    def __init__(self, agent):
        self.agent = agent
    
    def custom_analysis(self, plan_id):
        # Custom analysis logic
        pass

agent = ChangeManagementAgent(config)
plugin = CustomPlugin(agent)
agent.register_plugin("custom", plugin)
```

### Integration with External Systems

```python
class JiraIntegration:
    def __init__(self, agent, jira_client):
        self.agent = agent
        self.jira = jira_client
    
    def sync_milestones(self, plan_id):
        milestones = agent._milestone.get_milestones_by_status(plan_id, "in_progress")
        for milestone in milestones:
            self.jira.create_epic(milestone['name'], milestone['target_date'])
```

---

## FAQ

**Q: How many stakeholders can the agent manage?**
A: The agent can manage thousands of stakeholders per plan. For very large organizations (10,000+), consider using file-based storage and partitioning by department.

**Q: Can I use the agent for multiple concurrent initiatives?**
A: Yes. Each plan has a unique `plan_id`, and all operations are scoped to specific plans.

**Q: What if I don't have all ADKAR scores?**
A: You can provide partial scores. The agent calculates readiness based on available data and identifies which phases need assessment.

**Q: Can I customize the ADKAR thresholds?**
A: Yes. Set `adkar_ready_threshold` and `adkar_partial_threshold` in the configuration.

**Q: How do I export data from the agent?**
A: Use `get_plan_status()` and `list_plans()` to retrieve data. For file-based storage, data is persisted as JSON files.

**Q: Can the agent generate PowerPoint or PDF reports?**
A: The agent provides structured data that can be rendered into any format using external tools.

**Q: What happens if I lose the in-memory data?**
A: In-memory storage (default) does not persist across restarts. Configure `storage_backend: "file"` for persistent storage.

**Q: Can I integrate with Microsoft Project or Jira?**
A: Yes. The agent exposes structured data that can be mapped to external tools. See "Extending the Agent" for examples.

**Q: How accurate are the readiness assessments?**
A: Readiness assessments are based on the scores you provide. The agent calculates weighted averages and identifies gaps.

**Q: Can I run the agent without providing scores?**
A: Yes. The agent works with default scores (0.5) if you don't provide custom scores. Custom scores provide more accurate assessments.

**Q: Is there a GUI available?**
A: The agent is API-based. You can build a GUI using the API methods, or use the optional dashboard output.

**Q: How do I handle resistance from senior leadership?**
A: Senior leadership resistance requires executive-level engagement strategies. Use the `engagement_strategy()` method and escalate through proper channels.

**Q: Can I track resistance over time?**
A: Yes. Resistance entries include timestamps and status updates. Track changes by calling `get_resistance_summary()` at regular intervals.

**Q: What if my change initiative is delayed?**
A: Use `update_milestone_status()` to mark milestones as delayed. The agent recalculates progress and identifies schedule impacts.

---

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Follow the existing code style with type hints and dataclasses
2. Add tests for new functionality
3. Update documentation for API changes
4. Keep changes focused and well-described
5. Add examples for new features
6. Ensure backward compatibility

## License

Part of the Awesome Grok Skills collection. See project root for license details.
