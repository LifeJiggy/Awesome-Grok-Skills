# Change Management Agent

Comprehensive organizational change management with ADKAR modeling, stakeholder analysis, resistance management, communication planning, training development, and readiness assessment.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Creating a Change Plan](#creating-a-change-plan)
  - [Stakeholder Analysis](#stakeholder-analysis)
  - [ADKAR Evaluation](#adkar-evaluation)
  - [Communication Planning](#communication-planning)
  - [Training Development](#training-development)
  - [Readiness Assessment](#readiness-assessment)
- [API Reference](#api-reference)
  - [ChangeManagementAgent](#changemanagementagent)
  - [ADKARModel](#adkarmodel)
  - [StakeholderAnalyzer](#stakeholderanalyzer)
  - [ResistanceManager](#resistancemanager)
  - [CommunicationPlanner](#communicationplanner)
  - [TrainingDeveloper](#trainingdeveloper)
  - [ReadinessAssessor](#readinessassessor)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Change Management Agent is a Python-based system for managing enterprise-scale organizational transformations. It implements the ADKAR individual change model alongside structured stakeholder analysis to provide a comprehensive approach to change readiness and resistance management.

**Key Capabilities:**
- Change plan creation with auto-generated phases and milestones
- Stakeholder mapping on power/interest grid
- ADKAR readiness evaluation with bottleneck identification
- Communication plan generation across multiple channels
- Training program development aligned to ADKAR phases
- Organizational readiness assessment across 8 dimensions
- Resistance tracking with intervention planning

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
| Dashboard | Unified view of all change initiative metrics |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Change Management Agent                    │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │  Change  │ │Stakeholder│ │  ADKAR   │ │Communica-│     │
│  │  Plan    │ │ Analyzer  │ │ Evaluator│ │tion Plan │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │Resistanc.│ │ Training │ │ Readiness│ │  Risk    │     │
│  │ Manager  │ │Developer │ │ Assessor │ │ Manager  │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.change_management.agent import ChangeManagementAgent

# Initialize the agent
agent = ChangeManagementAgent({"user": "your_name"})

# Create a change plan
plan = agent.create_change_plan(
    initiative_name="Cloud Migration",
    change_type="technological",
    objectives=["Reduce costs by 30%", "Improve reliability"],
    timeline_weeks=26,
)

# Add a stakeholder
result = agent.add_stakeholder(
    plan_id=plan["plan_id"],
    name="Sarah Chen",
    role="CTO",
    impact_level="critical",
    resistance_level="champion",
)

# Assess readiness
readiness = agent.assess_readiness(plan["plan_id"])
print(f"Readiness: {readiness['readiness_level']}")
```

```bash
python agents/change-management/agent.py
```

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

# Auto-generates:
# - 5 phases (Preparation → Reinforcement)
# - 6 milestones with target dates
# - Stakeholder framework
```

### Stakeholder Analysis

```python
# Add multiple stakeholders
stakeholders = [
    {"name": "CTO", "role": "Executive Sponsor", "impact_level": "critical",
     "resistance_level": "champion", "influence_score": 0.9},
    {"name": "VP Engineering", "role": "Implementation Lead", "impact_level": "high",
     "resistance_level": "supporter", "influence_score": 0.7},
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
```

### ADKAR Evaluation

```python
# Evaluate individual readiness
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
```

### Communication Planning

```python
comm_plan = agent.develop_communication_plan(plan_id=plan["plan_id"])

# Result includes scheduled communications by channel and audience
for comm in comm_plan["communication_schedule"][:5]:
    print(f"{comm['title']}: {comm['channel']} on {comm['scheduled_date']}")
```

### Training Development

```python
training = agent.develop_training_program(plan_id=plan["plan_id"])

# 5 modules aligned to ADKAR phases
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
print(f"Gaps: {len(readiness['gaps'])}")
for gap in readiness["gaps"]:
    print(f"  - {gap['dimension']}: {gap['severity']}")
```

## API Reference

### ChangeManagementAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_change_plan()` | initiative_name, change_type, description, objectives, timeline_weeks, budget | Plan dict |
| `add_stakeholder()` | plan_id, name, role, department, impact_level, resistance_level, influence_score, engagement_score, concerns | Stakeholder dict |
| `evaluate_adkar()` | plan_id, stakeholder_id, scores | Evaluation dict |
| `develop_communication_plan()` | plan_id | Communication plan dict |
| `develop_training_program()` | plan_id | Training program dict |
| `assess_readiness()` | plan_id, scores | Readiness dict |
| `get_resistance_summary()` | — | Summary dict |
| `get_plan_status()` | plan_id | Status dict |
| `list_plans()` | — | List of plan dicts |
| `get_status()` | — | Agent status dict |

### ADKARModel

| Method | Parameters | Returns |
|--------|-----------|---------|
| `evaluate_stakeholder()` | stakeholder_id, scores | Evaluation with bottlenecks |
| `get_bottleneck()` | stakeholder_id | Bottleneck dict or None |
| `compare_readiness()` | stakeholder_ids | Comparison matrix |
| `overall_organizational_readiness()` | stakeholder_ids | Aggregate readiness |

### StakeholderAnalyzer

| Method | Parameters | Returns |
|--------|-----------|---------|
| `register_stakeholder()` | stakeholder | Stakeholder ID |
| `classify_by_influence_interest()` | — | Power/interest grid |
| `identify_champions()` | — | List of champions |
| `identify_risks()` | — | Risk-ranked stakeholders |
| `engagement_strategy()` | stakeholder_id | Strategy dict |

## Data Models

### ChangePlan
Core data structure for change initiatives with phases, stakeholders, communications, training, risks, and milestones.

### Stakeholder
Individual stakeholder profile with influence, engagement, resistance level, and ADKAR scores.

### ADKAR Evaluation
Results from ADKAR assessment including scores, bottleneck, readiness level, and recommendations.

### CommunicationMessage
Scheduled communication with channel, audience, sender, and timing.

### TrainingModule
ADKAR-aligned training unit with format, objectives, and assessment criteria.

## Configuration

```python
config = {
    "user": "change_manager",
    "default_timeline_weeks": 26,
    "adkar_ready_threshold": 0.7,
    "adkar_partial_threshold": 0.4,
    "communication_channels": ["email", "town_hall", "one_on_one", "workshop"],
}
agent = ChangeManagementAgent(config)
```

## Best Practices

1. **Start with Stakeholder Analysis** — Before planning anything, understand who is affected and how.
2. **Evaluate ADKAR Early** — Individual readiness determines organizational readiness.
3. **Communicate Consistently** — Use the generated communication plan as your baseline.
4. **Address Resistance Proactively** — Don't wait for resistance to escalate.
5. **Measure Readiness Regularly** — Re-assess before major milestones.
6. **Reinforce Change** — Without reinforcement, organizations regress to old behaviors.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Plan phases don't match timeline | Adjust `timeline_weeks` parameter |
| Stakeholder not found | Verify ID from `add_stakeholder` return value |
| ADKAR bottleneck unclear | Ensure all 5 phases have scores |
| Communication plan empty | Add stakeholders with departments first |
| Training modules missing | Verify plan has stakeholders for module targeting |

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

## License

Part of the Awesome Grok Skills collection. See project root for license details.
