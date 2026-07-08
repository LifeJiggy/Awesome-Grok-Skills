---
name: crisis-management
version: 3.0.0
description: Comprehensive crisis management agent — crisis response planning, communication strategy, stakeholder management, recovery protocols, post-mortem analysis, and compliance tracking for enterprise incident response.
author: Awesome Grok Skills Team
tags:
  - crisis-management
  - incident-response
  - communication
  - stakeholder-management
  - recovery
  - post-mortem
  - compliance
  - business-continuity
  - risk-management
  - disaster-recovery
category: Risk & Compliance
personality: Calm under pressure, methodical, empathetic yet decisive, focused on clear communication and measurable recovery, audit-minded
use_cases:
  - Creating crisis response plans
  - Managing active crisis events
  - Developing communication strategies
  - Notifying stakeholders
  - Planning and executing recovery
  - Generating post-mortem reports
  - Tracking compliance requirements
  - Coordinating crisis teams
  - Managing media communications
  - Documenting lessons learned
---

# Crisis Management Agent

> THE definitive agent for crisis planning, response orchestration, communication management,
> stakeholder handling, recovery strategies, and post-crisis analysis.
> Enterprise-ready, auditable, and deeply structured.

---

## Table of Contents

1. [Agent Identity](#agent-identity)
2. [Core Principles](#core-principles)
3. [Capabilities](#capabilities)
4. [Operational Guidelines](#operational-guidelines)
5. [Method Signatures](#method-signatures)
6. [Usage Patterns](#usage-patterns)
7. [Data Models](#data-models)
8. [Checklists](#checklists)
9. [Troubleshooting](#troubleshooting)

---

## Agent Identity

The Crisis Management Agent orchestrates end-to-end crisis response and recovery. It creates crisis plans, manages communications, handles stakeholder outreach, develops recovery strategies, and analyzes post-crisis effectiveness.

### What It Does

- Creates scenario-based crisis plans with step-by-step runbooks and contact lists
- Manages crisis communications across 18 channels with tone-appropriate messaging
- Handles stakeholder identification, prioritization, and tracking
- Develops recovery timelines with milestones and RTO/RPO targets
- Analyzes crisis response effectiveness with lessons learned
- Tracks crisis status and metrics throughout the lifecycle
- Exports structured crisis documentation for audits and compliance

### What It Does NOT Do

- Does not directly send external communications (manages drafting and tracking)
- Does not replace incident management tools (provides orchestration layer)
- Does not handle technical incident resolution (focuses on management and communication)
- Does not replace legal counsel (provides compliance tracking and documentation)

---

## Core Principles

### 1. Speed of Response
Every minute counts in a crisis. The agent enforces response time targets and automatic escalation to ensure no crisis goes unaddressed.

### 2. Clear Communication
Crisis communications must be clear, accurate, and appropriate for each audience. No jargon, no speculation, no blame.

### 3. Stakeholder-Centric
Different stakeholders need different information at different times. The agent ensures the right message reaches the right people through the right channel.

### 4. Documentation First
Every action, decision, and communication is logged. In a crisis, if it wasn't documented, it didn't happen.

### 5. Continuous Improvement
Every crisis is a learning opportunity. Post-mortems are mandatory, and lessons are tracked to prevent recurrence.

### 6. Compliance Awareness
Regulatory deadlines don't stop for crises. The agent tracks compliance requirements and ensures deadlines are met.

### 7. Empathy in Communication
Behind every incident are affected people. Communications lead with empathy and transparency.

---

## Capabilities

### 1. Crisis Plan Creation

Create comprehensive crisis response plans for different scenarios.

```python
from agents.crisis_management.agent import CrisisManagementAgent, CrisisType, CrisisSeverity, ComplianceRequirement

agent = CrisisManagementAgent()

# Create crisis plan
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

print(f"Plan created: {plan.name}")
print(f"Steps: {len(plan.steps)}")
print(f"Contacts: {len(plan.contacts)}")
```

**Plan Features:**
- Scenario-based step generation
- Contact list with priority levels
- Communication templates
- Compliance requirement tracking
- Escalation matrix
- Recovery targets

### 2. Crisis Event Activation

Activate crisis response using an existing plan.

```python
# Activate crisis
crisis = agent.activate_crisis(
    plan_id=plan.plan_id,
    title="Customer Data Breach - S3 Bucket Exposure",
    description="Security team discovered misconfigured S3 bucket exposing customer PII",
    severity=CrisisSeverity.CRITICAL,
    trigger=CrisisTrigger.SECURITY_SCAN,
    incident_commander="CTO",
)

print(f"Crisis activated: {crisis.title}")
print(f"Severity: {crisis.severity.value}")
print(f"Status: {crisis.status.value}")
```

### 3. Crisis Status Management

Track and update crisis status throughout the lifecycle.

```python
# Update status
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.ACKNOWLEDGED, "Incident acknowledged by CTO")
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.INVESTIGATING, "Security team investigating")
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.CONTAINED, "Breach contained")
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.RESOLVED, "All systems restored")

# Escalate if needed
agent.escalate_crisis(crisis.crisis_id, EscalationLevel.L4_C_SUITE, "Critical breach requires C-suite attention")
```

**Status Lifecycle:**
```
DETECTED → ACKNOWLEDGED → INVESTIGATING → CONTAINED → RECOVERING → RESOLVED → POST_MORTEM → CLOSED
```

### 4. Communication Management

Develop communication plans and send crisis communications.

```python
# Develop communication plan
comm_plan = agent.develop_communication_plan(
    crisis_id=crisis.crisis_id,
    strategy="Transparent, empathetic communication focusing on customer protection",
    key_messages=[
        "We have identified unauthorized access to customer data",
        "We are taking immediate steps to secure the affected systems",
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
    body="We have detected a data breach. The security team is investigating.",
)

# Draft communication using templates
draft = agent.draft_communication(
    crisis_id=crisis.crisis_id,
    message_type=MessageType.CUSTOMER_ADVISORY,
    audience=AudienceType.EXTERNAL_CUSTOMERS,
)
```

**Communication Channels (18):**
- Internal: Email, Slack, SMS, Phone, Video Call, Wiki, All-Hands
- External: Press Release, Social Media, Website Banner, Customer Portal
- Executive: Board Call, Investor Relations, Media Briefing
- Compliance: Regulatory Filing, Employee Town Hall

### 5. Stakeholder Management

Manage stakeholders with priority-based notification rules.

```python
# Add stakeholders
agent.add_stakeholder(name="Jane Smith", role="CEO", priority=StakeholderPriority.P1_IMMEDIATE)
agent.add_stakeholder(name="Legal Team", role="Legal", priority=StakeholderPriority.P2_URGENT)
agent.add_stakeholder(name="Engineering", role="CTO", priority=StakeholderPriority.P2_URGENT)

# Get notification list by severity
notify_list = agent.get_notification_list(severity=CrisisSeverity.CRITICAL)
print(f"Notify {len(notify_list)} stakeholders for critical crisis")
```

**Priority Levels:**

| Level | Role | Communication | Frequency |
|-------|------|---------------|-----------|
| P1 | Board, CEO | Direct call | Immediate |
| P2 | Legal, C-Suite | Email + call | Every 2 hours |
| P3 | VP, Dept Heads | Email update | Every 4 hours |
| P4 | Managers | Slack update | Every 8 hours |
| P5 | Individual Contributors | Slack update | Every 12 hours |
| P6 | External (PR, Media) | Press release | As needed |

### 6. Recovery Planning

Develop structured recovery plans with milestones and targets.

```python
# Develop recovery plan
recovery = agent.develop_recovery(
    crisis_id=crisis.crisis_id,
    rto_hours=4,
    rpo_hours=1,
    mttr_hours=24,
)

print(f"Recovery plan: {recovery.plan_id}")
print(f"Milestones: {len(recovery.milestones)}")
print(f"RTO: {recovery.rto_hours}h, RPO: {recovery.rpo_hours}h")
```

**Recovery Phases:**

| Phase | Duration | Focus |
|-------|----------|-------|
| Immediate | 0-24 hours | Contain damage, assess impact |
| Short-term | 1-7 days | Restore critical services |
| Medium-term | 1-4 weeks | Full service restoration |
| Long-term | 1-3 months | Process improvement |
| Sustained | 3+ months | Prevention and hardening |

### 7. Post-Mortem Analysis

Generate comprehensive post-crisis analysis reports.

```python
# Generate post-mortem
post_mortem = agent.generate_post_mortem(
    crisis_id=crisis.crisis_id,
    title="Post-Mortem: Customer Data Breach",
    participants=["CTO", "Security Lead", "Legal Counsel"],
)

print(f"Post-mortem: {post_mortem.title}")
print(f"Lessons: {len(post_mortem.lessons)}")
print(f"What went well: {len(post_mortem.what_went_well)}")
print(f"What went wrong: {len(post_mortem.what_went_wrong)}")
```

### 8. Plan Testing

Test crisis plans to identify gaps.

```python
test_result = agent.test_crisis_plan(plan.plan_id)
print(f"Gaps found: {len(test_result['gaps'])}")
for gap in test_result["gaps"]:
    print(f"  - {gap}")
for rec in test_result["recommendations"]:
    print(f"  Recommendation: {rec}")
```

### 9. Dashboard & Status

Get real-time views of crisis status.

```python
dashboard = agent.get_crisis_dashboard()
print(f"Active crises: {dashboard['active_crises']}")
print(f"By severity: {dashboard['by_severity']}")

status = agent.get_status()
for key, value in status.items():
    print(f"  {key}: {value}")
```

---

## Operational Guidelines

### Crisis Response Timeline

| Time | Action | Owner |
|------|--------|-------|
| T+0 | Detect and acknowledge | Monitoring/On-call |
| T+15min | Assign incident commander | Leadership |
| T+30min | Assess impact and severity | Technical Lead |
| T+30min | Notify executive leadership | Comms Lead |
| T+60min | Activate crisis team | Incident Commander |
| T+60min | Send initial communication | Comms Lead |
| T+2hrs | Contain the issue | Technical Lead |
| T+4hrs | Root cause identified | Technical Lead |
| T+24hrs | Resolution communicated | Comms Lead |
| T+72hrs | Post-mortem scheduled | Incident Commander |

### Communication Rules

1. **Lead with empathy** — acknowledge impact before explaining cause
2. **No speculation** — only state confirmed facts
3. **No blame** — focus on systems, not individuals
4. **Regular updates** — even if there's no new information
5. **Multi-channel** — use appropriate channels for each audience
6. **Approval required** — external communications need approval
7. **Document everything** — log all communications

### Escalation Rules

1. **No acknowledgment in 30 minutes** → Escalate to next level
2. **Severity increases** → Escalate immediately
3. **Compliance deadline approaching** → Escalate to legal/compliance
4. **Customer impact significant** → Escalate to executive leadership
5. **Media inquiry received** → Escalate to communications and legal

### Recovery Best Practices

1. **RTO < 4 hours** — for critical services
2. **RPO < 1 hour** — for data recovery point
3. **Verify before declaring resolved** — test all systems
4. **Monitor post-recovery** — watch for recurrence
5. **Communicate resolution** — notify all stakeholders
6. **Schedule post-mortem** — within 72 hours of resolution

---

## Method Signatures

### Crisis Plan Methods

```python
def create_crisis_plan(
    self,
    name: str,
    scenario: str,
    crisis_type: CrisisType = CrisisType.OPERATIONAL,
    severity: CrisisSeverity = CrisisSeverity.MEDIUM,
    contacts: Optional[List[Dict[str, Any]]] = None,
    compliance: Optional[List[ComplianceRequirement]] = None,
) -> CrisisPlan

def update_crisis_plan(self, plan_id: str, **kwargs: Any) -> CrisisPlan
def get_crisis_plan(self, plan_id: str) -> CrisisPlan
def list_plans(self) -> List[CrisisPlan]
def test_crisis_plan(self, plan_id: str) -> Dict[str, Any]
```

### Crisis Event Methods

```python
def activate_crisis(
    self,
    plan_id: str,
    title: str,
    description: str = "",
    severity: CrisisSeverity = CrisisSeverity.HIGH,
    trigger: CrisisTrigger = CrisisTrigger.MONITORING_ALERT,
    incident_commander: str = "",
) -> CrisisEvent

def update_crisis_status(self, crisis_id: str, new_status: IncidentStatus, notes: str = "") -> CrisisEvent
def escalate_crisis(self, crisis_id: str, to_level: EscalationLevel, reason: str = "") -> CrisisEvent
def get_crisis(self, crisis_id: str) -> CrisisEvent
def list_crises(self, status: Optional[IncidentStatus] = None) -> List[CrisisEvent]
def get_active_crises(self) -> List[CrisisEvent]
def get_crisis_dashboard(self) -> Dict[str, Any]
```

### Communication Methods

```python
def develop_communication_plan(
    self,
    crisis_id: str,
    strategy: str = "",
    key_messages: Optional[List[str]] = None,
    spokesperson: str = "",
) -> CommunicationPlan

def send_communication(
    self,
    crisis_id: str,
    message_type: MessageType,
    channel: CommunicationChannel = CommunicationChannel.EMAIL,
    audience: AudienceType = AudienceType.INTERNAL_ALL_EMPLOYEES,
    subject: str = "",
    body: str = "",
    tone: CommunicationTone = CommunicationTone.PROFESSIONAL,
) -> CommunicationRecord

def draft_communication(
    self,
    crisis_id: str,
    message_type: MessageType,
    audience: AudienceType,
    **kwargs: Any,
) -> CommunicationRecord
```

### Stakeholder Methods

```python
def add_stakeholder(
    self,
    name: str,
    role: str,
    department: str = "",
    priority: StakeholderPriority = StakeholderPriority.P5_STANDARD,
    communication_preference: CommunicationChannel = CommunicationChannel.EMAIL,
    contact_info: Optional[Dict[str, str]] = None,
) -> Stakeholder

def get_stakeholder(self, stakeholder_id: str) -> Optional[Stakeholder]
def list_stakeholders(self, priority: Optional[StakeholderPriority] = None) -> List[Stakeholder]
def get_notification_list(self, severity: CrisisSeverity) -> List[Stakeholder]
```

### Recovery Methods

```python
def develop_recovery(
    self,
    crisis_id: str,
    rto_hours: int = 4,
    rpo_hours: int = 1,
    mttr_hours: int = 24,
) -> RecoveryPlan

def get_recovery(self, plan_id: str) -> RecoveryPlan
def list_recovery_plans(self) -> List[RecoveryPlan]
```

### Post-Mortem Methods

```python
def generate_post_mortem(
    self,
    crisis_id: str,
    title: str = "",
    participants: Optional[List[str]] = None,
) -> PostMortem

def get_post_mortem(self, post_mortem_id: str) -> PostMortem
def list_post_mortems(self) -> List[PostMortem]
```

### Status & Export

```python
def get_status(self) -> Dict[str, Any]
def get_operation_log(self, limit: int = 50) -> List[Dict[str, Any]]
def clear_cache(self) -> int
def export_data(self, format: str = "json") -> str
```

---

## Usage Patterns

### Pattern 1: Full Crisis Response

```python
agent = CrisisManagementAgent()

# 1. Create plan
plan = agent.create_crisis_plan(
    name="Data Breach Response",
    scenario="Customer data exposed",
    crisis_type=CrisisType.DATA_BREACH,
    severity=CrisisSeverity.CRITICAL,
)

# 2. Activate crisis
crisis = agent.activate_crisis(
    plan_id=plan.plan_id,
    title="S3 Bucket Data Breach",
    severity=CrisisSeverity.CRITICAL,
)

# 3. Update status
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.ACKNOWLEDGED)
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.INVESTIGATING)

# 4. Develop communications
agent.develop_communication_plan(crisis_id=crisis.crisis_id)
agent.send_communication(crisis.crisis_id, MessageType.INITIAL_ALERT, CommunicationChannel.SLACK, AudienceType.INTERNAL_ALL_EMPLOYEES)

# 5. Resolve
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.CONTAINED)
agent.update_crisis_status(crisis.crisis_id, IncidentStatus.RESOLVED)

# 6. Post-mortem
post_mortem = agent.generate_post_mortem(crisis.crisis_id)
```

### Pattern 2: Communication Cascade

```python
# Develop plan
comm_plan = agent.develop_communication_plan(
    crisis_id=crisis.crisis_id,
    key_messages=["Issue identified", "Fix in progress", "Resolution expected soon"],
)

# Notify by priority
for priority in [StakeholderPriority.P1_IMMEDIATE, StakeholderPriority.P2_URGENT, StakeholderPriority.P3_HIGH]:
    stakeholders = agent.get_notification_list(severity=crisis.severity)
    for s in stakeholders:
        if s.priority == priority:
            agent.send_communication(
                crisis_id=crisis.crisis_id,
                message_type=MessageType.STAKEHOLDER_UPDATE,
                channel=s.communication_preference,
                audience=AudienceType.INTERNAL_EXECUTIVE,
                subject=f"Crisis Update: {crisis.title}",
                body=f"Status: {crisis.status.value}. Next update in 2 hours.",
            )
```

### Pattern 3: Recovery Execution

```python
# Develop recovery plan
recovery = agent.develop_recovery(crisis_id=crisis.crisis_id, rto_hours=4)

# Track milestones
for milestone in recovery.milestones:
    print(f"Milestone: {milestone.name} (Target: {milestone.target_date})")

# Monitor progress
print(f"Recovery progress: {recovery.get_completion_percentage():.0f}%")
```

---

## Data Models

### CrisisPlan

| Field | Type | Description |
|-------|------|-------------|
| plan_id | str | Unique 12-char ID |
| name | str | Plan name |
| scenario | str | Crisis scenario |
| crisis_type | CrisisType | Type of crisis |
| severity | CrisisSeverity | Severity level |
| steps | List[CrisisStep] | Response steps |
| contacts | List[Stakeholder] | Contact list |
| compliance | List[ComplianceRequirement] | Compliance tracking |
| version | int | Plan version |

### CrisisEvent

| Field | Type | Description |
|-------|------|-------------|
| crisis_id | str | Unique 12-char ID |
| title | str | Crisis title |
| status | IncidentStatus | Current status |
| severity | CrisisSeverity | Severity level |
| phase | CrisisPhase | Current phase |
| timeline | List[Dict] | Event timeline |
| communications | List[CommunicationRecord] | Sent communications |

### CommunicationRecord

| Field | Type | Description |
|-------|------|-------------|
| record_id | str | Unique ID |
| message_type | MessageType | Type of message |
| channel | CommunicationChannel | Delivery channel |
| audience | AudienceType | Target audience |
| tone | CommunicationTone | Message tone |
| status | str | draft/approved/sent |

### RecoveryPlan

| Field | Type | Description |
|-------|------|-------------|
| plan_id | str | Unique ID |
| rto_hours | int | Recovery Time Objective |
| rpo_hours | int | Recovery Point Objective |
| milestones | List[RecoveryMilestone] | Recovery milestones |
| completion | float | Completion percentage |

---

## Checklists

### Crisis Response Checklist

- [ ] Crisis detected and acknowledged
- [ ] Incident commander assigned
- [ ] Severity assessed
- [ ] Crisis team activated
- [ ] Stakeholders notified (by priority)
- [ ] Communication plan developed
- [ ] Initial communication sent
- [ ] Issue contained
- [ ] Root cause identified
- [ ] Fix deployed
- [ ] Resolution verified
- [ ] Resolution communicated
- [ ] Crisis stand-down
- [ ] Post-mortem scheduled

### Communication Checklist

- [ ] Key messages defined
- [ ] Spokesperson designated
- [ ] Audience matrix built
- [ ] Channel strategy defined
- [ ] Tone guidelines set
- [ ] Approval workflow established
- [ ] Templates generated
- [ ] Prohibited content listed
- [ ] Update schedule defined
- [ ] Feedback mechanism set

### Recovery Checklist

- [ ] RTO/RPO targets set
- [ ] Milestones defined
- [ ] Resources allocated
- [ ] Dependencies identified
- [ ] Communication checkpoints scheduled
- [ ] Verification steps defined
- [ ] Rollback plan documented
- [ ] Post-recovery testing planned
- [ ] Stakeholder notification on recovery
- [ ] Monitoring enhanced

### Post-Mortem Checklist

- [ ] Timeline reconstructed
- [ ] Root cause identified
- [ ] Impact assessed
- [ ] Response evaluated
- [ ] Lessons documented
- [ ] What went well identified
- [ ] What went wrong identified
- [ ] Improvements recommended
- [ ] Action items assigned
- [ ] Follow-up date set

---

## Troubleshooting

### Problem: Crisis plan has no steps

**Symptoms:** `len(plan.steps) == 0`

**Diagnosis:**
```python
plan = agent.get_crisis_plan(plan_id)
print(f"Crisis type: {plan.crisis_type.value}")
print(f"Steps: {len(plan.steps)}")
```

**Solution:** Ensure `crisis_type` is set when creating the plan. Steps are auto-generated based on crisis type.

### Problem: Stakeholders not notified

**Symptoms:** Communication not reaching stakeholders

**Diagnosis:**
```python
stakeholders = agent.get_notification_list(severity=CrisisSeverity.CRITICAL)
print(f"Stakeholders to notify: {len(stakeholders)}")
for s in stakeholders:
    print(f"  {s.name} ({s.priority.value}): {s.communication_preference.value}")
```

**Solution:** Check stakeholder priorities and ensure they match the crisis severity notification rules.

### Problem: Communication not sent

**Symptoms:** Communication status remains "draft"

**Solution:** External communications require approval. Use `approve()` before `send()`. Internal communications can be sent directly.

### Problem: Recovery plan not tracking progress

**Symptoms:** Completion percentage always 0%

**Solution:** Manually mark milestones as complete using `milestone.complete()`. Progress is calculated from completed milestones.

### Problem: Post-mortem missing lessons

**Symptoms:** Empty lessons list

**Solution:** Call `generate_post_mortem()` after the crisis is resolved. Default lessons are auto-generated based on crisis type.

---

*Crisis Management Agent v3.0.0 — Part of the Awesome Grok Skills collection.*
*Last updated: 2026-07-06*
