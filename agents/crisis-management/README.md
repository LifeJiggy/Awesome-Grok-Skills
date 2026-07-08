# Crisis Management Agent

> Comprehensive crisis response — planning, communication, stakeholder management, recovery, and post-mortem.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)](CHANGELOG.md)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Crisis Plan Creation](#crisis-plan-creation)
  - [Crisis Activation](#crisis-activation)
  - [Status Management](#status-management)
  - [Communication Management](#communication-management)
  - [Stakeholder Management](#stakeholder-management)
  - [Recovery Planning](#recovery-planning)
  - [Post-Mortem Analysis](#post-mortem-analysis)
  - [Plan Testing](#plan-testing)
  - [Dashboard](#dashboard)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Crisis Management Agent is a comprehensive system for managing the full crisis lifecycle. It handles crisis response planning, communication strategy development, stakeholder management, recovery protocol design, and post-crisis analysis.

Built for communications teams, risk managers, executives, and incident response teams who need a structured, auditable approach to crisis management.

### What Makes This Agent Different

- **Full Lifecycle Coverage**: From plan creation through post-mortem
- **18 Communication Channels**: Comprehensive multi-channel support
- **Compliance Tracking**: GDPR, SOC2, HIPAA, PCI, SEC requirements
- **Stakeholder Priority Matrix**: Right message to right people at right time
- **Recovery Milestones**: RTO/RPO targets with phased recovery
- **Audit Trail**: Every action logged for compliance and forensics
- **Plan Testing**: Identify gaps before a real crisis hits

---

## Features

| Feature | Description |
|---------|-------------|
| Crisis Plans | Scenario-based plans with steps, contacts, and compliance |
| Crisis Events | Full lifecycle tracking with timeline and status |
| Communications | 18 channels with templates, tone, and approval workflow |
| Stakeholders | Priority-based registry with notification rules |
| Recovery Plans | Milestones with RTO/RPO targets and phases |
| Post-Mortem | Structured analysis with lessons and action items |
| Escalation | Auto-escalation with configurable rules |
| Compliance | GDPR, SOC2, HIPAA, PCI, SEC tracking |
| Dashboard | Real-time crisis status overview |
| Plan Testing | Gap analysis and recommendations |
| Export | JSON, CSV, Markdown, PDF formats |
| Audit Trail | Immutable operation logging |

---

## Quick Start

```python
from agents.crisis_management.agent import CrisisManagementAgent, CrisisType, CrisisSeverity

# Initialize agent
agent = CrisisManagementAgent()

# Create crisis plan
plan = agent.create_crisis_plan(
    name="Data Breach Response",
    scenario="Customer PII exposed",
    crisis_type=CrisisType.DATA_BREACH,
    severity=CrisisSeverity.CRITICAL,
)

# Activate crisis
crisis = agent.activate_crisis(
    plan_id=plan.plan_id,
    title="S3 Bucket Data Breach",
    severity=CrisisSeverity.CRITICAL,
)

# Manage and resolve
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.RESOLVED)
post_mortem = agent.generate_post_mortem(crisis.crisis_id)

# Get status
print(agent.get_status())
```

### Run the Demo

```bash
python agents/crisis-management/agent.py
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# No external dependencies required
# Python 3.10+ with standard library only
```

---

## Usage

### Crisis Plan Creation

```python
from agents.crisis_management.agent import CrisisManagementAgent, CrisisType, CrisisSeverity, ComplianceRequirement

agent = CrisisManagementAgent()

plan = agent.create_crisis_plan(
    name="Data Breach Response Plan",
    scenario="Customer PII exposed due to misconfigured S3 bucket",
    crisis_type=CrisisType.DATA_BREACH,
    severity=CrisisSeverity.CRITICAL,
    contacts=[
        {"name": "Jane Smith", "role": "CEO", "priority": 1},
        {"name": "Legal Team", "role": "Legal Counsel", "priority": 2},
        {"name": "CTO", "role": "Technical Lead", "priority": 2},
    ],
    compliance=[
        ComplianceRequirement.GDPR_72HR,
        ComplianceRequirement.STATE_BREACH,
        ComplianceRequirement.CUSTOMER_NOTIFICATION,
    ],
)

print(f"Plan: {plan.name} ({plan.plan_id})")
print(f"Steps: {len(plan.steps)}")
print(f"Contacts: {len(plan.contacts)}")
```

### Crisis Activation

```python
crisis = agent.activate_crisis(
    plan_id=plan.plan_id,
    title="Customer Data Breach - S3 Bucket Exposure",
    description="Security team discovered misconfigured S3 bucket",
    severity=CrisisSeverity.CRITICAL,
    trigger=CrisisTrigger.SECURITY_SCAN,
    incident_commander="CTO",
)

print(f"Crisis: {crisis.title} ({crisis.crisis_id})")
print(f"Status: {crisis.status.value}")
```

### Status Management

```python
# Update through lifecycle
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.ACKNOWLEDGED)
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.INVESTIGATING)
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.CONTAINED)
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.RESOLVED)

# Escalate if needed
agent.escalate_crisis(crisis.crisis_id, EscalationLevel.L4_C_SUITE, "Critical breach")
```

### Communication Management

```python
# Develop communication plan
comm_plan = agent.develop_communication_plan(
    crisis_id=crisis.crisis_id,
    strategy="Transparent, empathetic communication",
    key_messages=[
        "We have identified unauthorized access to customer data",
        "We are taking immediate steps to secure affected systems",
        "Affected customers will be notified directly",
    ],
    spokesperson="Jane Smith, CEO",
)

# Send communications
agent.send_communication(
    crisis_id=crisis.crisis_id,
    message_type=MessageType.INITIAL_ALERT,
    channel=CommunicationChannel.SLACK,
    audience=AudienceType.INTERNAL_ALL_EMPLOYEES,
    subject="URGENT: Data Breach Detected",
    body="We have detected a data breach. Team is investigating.",
)

# Draft using templates
draft = agent.draft_communication(
    crisis_id=crisis.crisis_id,
    message_type=MessageType.CUSTOMER_ADVISORY,
    audience=AudienceType.EXTERNAL_CUSTOMERS,
)
```

### Stakeholder Management

```python
# Add stakeholders
agent.add_stakeholder(name="Jane Smith", role="CEO", priority=StakeholderPriority.P1_IMMEDIATE)
agent.add_stakeholder(name="Legal Team", role="Legal", priority=StakeholderPriority.P2_URGENT)

# Get notification list
notify_list = agent.get_notification_list(severity=CrisisSeverity.CRITICAL)
```

### Recovery Planning

```python
recovery = agent.develop_recovery(
    crisis_id=crisis.crisis_id,
    rto_hours=4,
    rpo_hours=1,
    mttr_hours=24,
)

print(f"Milestones: {len(recovery.milestones)}")
print(f"RTO: {recovery.rto_hours}h")
print(f"Progress: {recovery.get_completion_percentage():.0f}%")
```

### Post-Mortem Analysis

```python
post_mortem = agent.generate_post_mortem(
    crisis_id=crisis.crisis_id,
    title="Post-Mortem: Customer Data Breach",
    participants=["CTO", "Security Lead", "Legal Counsel"],
)

print(f"Lessons: {len(post_mortem.lessons)}")
print(f"What went well: {post_mortem.what_went_well}")
print(f"What went wrong: {post_mortem.what_went_wrong}")
```

### Plan Testing

```python
test_result = agent.test_crisis_plan(plan.plan_id)
print(f"Gaps: {test_result['gaps']}")
print(f"Recommendations: {test_result['recommendations']}")
```

### Dashboard

```python
dashboard = agent.get_crisis_dashboard()
print(f"Active crises: {dashboard['active_crises']}")
print(f"By severity: {dashboard['by_severity']}")
```

---

## API Reference

### CrisisManagementAgent

| Method | Description | Returns |
|--------|-------------|---------|
| `create_crisis_plan()` | Create crisis plan | `CrisisPlan` |
| `update_crisis_plan()` | Update plan | `CrisisPlan` |
| `get_crisis_plan()` | Get plan by ID | `CrisisPlan` |
| `list_plans()` | List all plans | `List[CrisisPlan]` |
| `test_crisis_plan()` | Test plan for gaps | `Dict` |
| `activate_crisis()` | Activate crisis | `CrisisEvent` |
| `update_crisis_status()` | Update status | `CrisisEvent` |
| `escalate_crisis()` | Escalate crisis | `CrisisEvent` |
| `get_crisis()` | Get crisis by ID | `CrisisEvent` |
| `list_crises()` | List all crises | `List[CrisisEvent]` |
| `get_active_crises()` | Get active crises | `List[CrisisEvent]` |
| `get_crisis_dashboard()` | Get dashboard | `Dict` |
| `develop_communication_plan()` | Create comm plan | `CommunicationPlan` |
| `send_communication()` | Send communication | `CommunicationRecord` |
| `draft_communication()` | Draft communication | `CommunicationRecord` |
| `add_stakeholder()` | Add stakeholder | `Stakeholder` |
| `get_stakeholder()` | Get stakeholder | `Optional[Stakeholder]` |
| `list_stakeholders()` | List stakeholders | `List[Stakeholder]` |
| `get_notification_list()` | Get notification list | `List[Stakeholder]` |
| `develop_recovery()` | Create recovery plan | `RecoveryPlan` |
| `get_recovery()` | Get recovery plan | `RecoveryPlan` |
| `list_recovery_plans()` | List recovery plans | `List[RecoveryPlan]` |
| `generate_post_mortem()` | Create post-mortem | `PostMortem` |
| `get_post_mortem()` | Get post-mortem | `PostMortem` |
| `list_post_mortems()` | List post-mortems | `List[PostMortem]` |
| `get_status()` | Get agent status | `Dict` |
| `get_operation_log()` | Get operation log | `List[Dict]` |
| `clear_cache()` | Clear cache | `int` |
| `export_data()` | Export all data | `str` |

---

## Examples

### Example 1: Full Crisis Response

```python
agent = CrisisManagementAgent()

# Plan
plan = agent.create_crisis_plan(
    name="Data Breach Response",
    scenario="Customer data exposed",
    crisis_type=CrisisType.DATA_BREACH,
    severity=CrisisSeverity.CRITICAL,
)

# Activate
crisis = agent.activate_crisis(plan.plan_id, "S3 Bucket Breach", severity=CrisisSeverity.CRITICAL)

# Respond
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.ACKNOWLEDGED)
agent.develop_communication_plan(crisis.crisis_id)
agent.send_communication(crisis.crisis_id, MessageType.INITIAL_ALERT, CommunicationChannel.SLACK, AudienceType.INTERNAL_ALL_EMPLOYEES)

# Resolve
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.RESOLVED)

# Learn
post_mortem = agent.generate_post_mortem(crisis.crisis_id)
```

### Example 2: Communication Cascade

```python
# Notify by priority
stakeholders = agent.get_notification_list(severity=CrisisSeverity.CRITICAL)
for s in stakeholders:
    agent.send_communication(
        crisis_id=crisis.crisis_id,
        message_type=MessageType.STAKEHOLDER_UPDATE,
        channel=s.communication_preference,
        audience=AudienceType.INTERNAL_EXECUTIVE,
    )
```

### Example 3: Recovery Tracking

```python
recovery = agent.develop_recovery(crisis.crisis_id)
for milestone in recovery.milestones:
    print(f"{milestone.name}: {milestone.status}")
```

---

## Configuration

```python
from agents.crisis_management.agent import Config, CommunicationConfig, RecoveryConfig

config = Config(
    agent_name="MyCrisisAgent",
    response_time_target_minutes=15,
    post_mortem_required=True,
    communication=CommunicationConfig(
        update_frequency_hours={CrisisSeverity.CRITICAL: 1},
        approval_required_for_external=True,
    ),
    recovery=RecoveryConfig(
        rto_target_hours=4,
        rpo_target_hours=1,
    ),
)

agent = CrisisManagementAgent(config=config)
```

---

## Best Practices

### Planning

1. **Create plans for all scenario types** — don't wait for a crisis
2. **Include compliance requirements** — GDPR, SOC2, HIPAA deadlines
3. **Test plans regularly** — quarterly at minimum
4. **Keep contacts updated** — people change roles
5. **Document escalation paths** — who calls whom

### Communication

1. **Lead with empathy** — acknowledge impact first
2. **No speculation** — only confirmed facts
3. **Regular updates** — even without new information
4. **Multi-channel** — appropriate channel for each audience
5. **Approval for external** — legal/executive review required

### Recovery

1. **Set RTO/RPO targets** — know your recovery goals
2. **Track milestones** — measure progress
3. **Verify before declaring** — test all systems
4. **Monitor post-recovery** — watch for recurrence
5. **Communicate resolution** — notify all stakeholders

### Post-Mortem

1. **Schedule within 72 hours** — before memories fade
2. **Blameless culture** — focus on systems, not people
3. **Document lessons** — track to completion
4. **Share widely** — organization-wide learning
5. **Update plans** — incorporate findings

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Plan has no steps | Crisis type not set | Set `crisis_type` when creating plan |
| Stakeholders not notified | Priority mismatch | Check stakeholder priorities vs severity |
| Communication stuck in draft | External requires approval | Approve before sending |
| Recovery progress at 0% | Milestones not completed | Mark milestones as complete |
| Post-mortem has no lessons | Not generated after crisis | Generate after crisis is resolved |

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

*Crisis Management Agent v3.0.0 — Part of the Awesome Grok Skills collection.*

*Last updated: 2026-07-06*
