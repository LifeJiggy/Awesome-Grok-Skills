---
name: "soc-operations"
category: "blue-team"
version: "2.0.0"
tags: ["blue-team", "SOC", "operations", "workflows", "playbooks"]
---

# SOC Operations

## Overview

The SOC Operations module provides comprehensive tools for Security Operations Center (SOC) workflow management, shift handover procedures, ticket management, playbook execution, and team performance tracking. It covers tier-based escalation procedures, SLA management, runbook automation, and KPI reporting for SOC teams.

This skill is essential for SOC managers, tier 1/2/3 analysts, and security operations engineers responsible for day-to-day security monitoring and response operations.

## Core Capabilities

- **Alert Triage Workflows**: Structured triage procedures for different alert types with decision trees
- **Escalation Management**: Tier-based escalation paths with SLA tracking and automated notifications
- **Playbook Execution**: Step-by-step incident response playbooks with checklists and evidence collection
- **Shift Handover**: Automated shift handover reports with open items, ongoing investigations, and status
- **Ticket Management**: Security ticket lifecycle, assignment, priority scoring, and SLA tracking
- **KPI Tracking**: Mean time to detect (MTTD), mean time to respond (MTTR), false positive rate, and analyst productivity
- **Shift Scheduling**: Coverage planning, on-call rotation, and workload balancing
- **Quality Assurance**: Analyst review scoring, calibration exercises, and continuous improvement tracking

## Usage Examples

```python
from soc_operations import (
    TriageEngine,
    EscalationManager,
    PlaybookRunner,
    ShiftHandover,
    KPITracker,
    TicketManager,
)

# --- Alert Triage ---
triage = TriageEngine()
decision = triage.triage_alert(
    alert_type="ssh_brute_force",
    severity="high",
    source_ip="192.168.1.100",
    context={"attempts": 15, "target_user": "root", "geo": "RU"},
)
print(f"Action: {decision.action}")
print(f"Playbook: {decision.playbook}")
print(f"Escalate: {decision.escalate}")
print(f"Priority: {decision.priority}")

# --- Escalation ---
esc_mgr = EscalationManager()
ticket = esc_mgr.create_ticket(
    title="SSH Brute Force from 192.168.1.100",
    severity="high",
    analyst="analyst1",
    alert_ids=["alert_001"],
)
print(f"Ticket: {ticket.ticket_id}")
print(f"SLA deadline: {ticket.sla_deadline}")

# --- Playbook Execution ---
runner = PlaybookRunner()
playbook = runner.load_playbook("brute_force_response")
result = runner.execute(playbook, context={
    "source_ip": "192.168.1.100",
    "target_user": "root",
})
print(f"Steps completed: {result.steps_completed}/{result.total_steps}")
print(f"Evidence collected: {len(result.evidence)}")

# --- Shift Handover ---
handover = ShiftHandover()
report = handover.generate(
    outgoing_shift="day",
    incoming_shift="night",
    open_tickets=[ticket],
    ongoing_investigations=["APT-28 tracking"],
)
print(f"Open items: {report.open_items}")
print(f"Critical alerts: {report.critical_alerts}")

# --- KPI Tracking ---
kpi = KPITracker()
kpi.record_detection("alert_001", detect_time=120, respond_time=300)
kpi.record_detection("alert_002", detect_time=60, respond_time=180)
metrics = kpi.get_metrics(period="daily")
print(f"MTTD: {metrics.mttd_minutes:.0f} min")
print(f"MTTR: {metrics.mttr_minutes:.0f} min")
print(f"Alerts handled: {metrics.alerts_handled}")

# --- Ticket Management ---
tickets = TicketManager()
t = tickets.create(title="Suspicious activity", priority="P2")
tickets.assign(t.ticket_id, "analyst2")
tickets.add_note(t.ticket_id, "IP blocked at firewall")
tickets.resolve(t.ticket_id, "False positive - legitimate scan")
```

## Best Practices

- Follow the NIST SOC Capability Model: Monitor → Detect → Analyze → Respond → Recover
- Maintain a maximum 15-minute triage SLA for critical alerts, 1 hour for high, 4 hours for medium
- Document every investigation step — if it isn't documented, it didn't happen
- Conduct weekly calibration sessions to align analyst severity scoring
- Use MITRE ATT&CK mapping for every alert to ensure technique coverage
- Implement automated enrichment (GeoIP, WHOIS, threat intel) to reduce triage time
- Track false positive rates per rule; retire rules with >90% FP rate after tuning
- Shift handover must cover: open tickets, ongoing investigations, notable events, and equipment issues
- Cross-train analysts across alert categories to prevent knowledge silos
- Review and update playbooks quarterly or after every significant incident

## Related Modules

- **security-monitoring**: Alert generation and SIEM integration
- **incident-response**: Detailed incident handling procedures
- **threat-hunting**: Proactive threat detection activities
- **digital-forensics**: Post-incident investigation tools

## Advanced Configuration

### Escalation Configuration

```yaml
escalation_paths:
  low:
    initial: "tier1_analyst"
    timeout_minutes: 60
    escalation: "tier2_analyst"
    notification: "email"
  medium:
    initial: "tier1_analyst"
    timeout_minutes: 30
    escalation: "tier2_analyst"
    notification: "slack,email"
  high:
    initial: "tier2_analyst"
    timeout_minutes: 15
    escalation: "tier3_analyst,manager"
    notification: "slack,phone"
  critical:
    initial: "tier3_analyst"
    timeout_minutes: 5
    escalation: "ciso,ir_team"
    notification: "phone,page"
```

### SLA Configuration

```yaml
sla_targets:
  critical:
    acknowledge_minutes: 5
    contain_minutes: 15
    remediate_hours: 4
    report_hours: 24
  high:
    acknowledge_minutes: 15
    contain_minutes: 60
    remediate_hours: 8
    report_hours: 48
  medium:
    acknowledge_minutes: 60
    contain_hours: 4
    remediate_days: 7
    report_days: 14
  low:
    acknowledge_hours: 4
    contain_days: 7
    remediate_days: 30
    report_days: 60
```

### Shift Configuration

```yaml
shifts:
  day:
    start: "06:00"
    end: "14:00"
    min_analysts: 2
    max_analysts: 5
  evening:
    start: "14:00"
    end: "22:00"
    min_analysts: 2
    max_analysts: 4
  night:
    start: "22:00"
    end: "06:00"
    min_analysts: 1
    max_analysts: 3
  oncall:
    type: "rotation"
    rotation_days: 7
    backup: true
```

## Architecture Patterns

### SOC Operating Model

```
Tier 1 — Alert Triage:
├── Monitor alert queue
├── Perform initial triage
├── Escalate true positives
├── Close false positives
├── Document investigation steps
└── Time SLA: 15min critical, 1hr high

Tier 2 — Investigation:
├── Deep-dive investigation
├── Threat hunting (ad-hoc)
├── Malware analysis basics
├── Network forensics basics
├── Containment actions
└── Time SLA: 1hr critical, 4hr high

Tier 3 — Advanced Analysis:
├── Complex incident handling
├── Reverse engineering
├── Advanced forensics
├── Threat intelligence
├── Root cause analysis
└── Time SLA: Immediate critical, 24hr high

Management:
├── Shift leads
├── SOC manager
├── Security director
└── CISO
```

### Playbook Architecture

```
Playbook Types:
├── Alert-Based Playbooks
│   ├── SSH Brute Force
│   ├── Malware Detected
│   ├── Phishing Report
│   └── Data Exfiltration
├── Incident-Based Playbooks
│   ├── Ransomware Response
│   ├── Account Compromise
│   ├── Data Breach
│   └── Insider Threat
└── Procedural Playbooks
    ├── Shift Handover
    ├── Escalation
    ├── Communication
    └── Reporting
```

### Ticket Lifecycle

```
Created → Assigned → In Progress → Investigating → Resolved → Closed
  │          │           │              │              │          │
  └── Auto   └── Manual  └── Analyst    └── Deep dive  └── Fix    └── Verified
      or          or         working         or verify       applied     confirmed
      triage      auto-
                  assign
```

## Integration Guide

### SOAR Integration

```python
from soc_operations import SOARConnector

soar = SOARConnector(
    platform="splunk_soar",
    url="https://soar.internal:8443",
    token="${SOAR_TOKEN}",
)

# Trigger playbook
playbook_id = soar.trigger_playbook(
    playbook="phishing_response",
    context={
        "alert_id": "alert_001",
        "source_email": "phishing@suspicious.com",
        "target_users": ["user1@company.com"],
    },
)
print(f"Playbook triggered: {playbook_id}")

# Get playbook status
status = soar.get_playbook_status(playbook_id)
print(f"Status: {status.state}")
print(f"Steps completed: {status.completed_steps}/{status.total_steps}")
```

### Ticketing System Integration

```python
from soc_operations import TicketingSystem

jira = TicketingSystem(
    platform="jira",
    url="https://jira.company.com",
    project="SEC",
    token="${JIRA_TOKEN}",
)

# Create security ticket
ticket = jira.create_ticket(
    title="SSH Brute Force from 198.51.100.1",
    description="Multiple failed SSH attempts detected",
    severity="High",
    assignee="soc-analyst-2",
    labels=["security", "brute-force"],
    custom_fields={
        "source_ip": "198.51.100.1",
        "target_system": "web-server-01",
        "alert_ids": ["alert_001", "alert_002"],
    },
)
print(f"Ticket: {ticket.key}")
print(f"URL: {ticket.url}")
```

### ChatOps Integration

```python
from soc_operations import ChatOps

slack = ChatOps(platform="slack", channel="#soc-alerts")

# Send alert notification
slack.send_alert(
    severity="high",
    title="Potential Data Exfiltration",
    details="Large outbound transfer detected to unknown IP",
    actions=[
        {"text": "Investigate", "value": "investigate"},
        {"text": "Block IP", "value": "block_ip"},
        {"text": "False Positive", "value": "close_fp"},
    ],
)
```

## Performance Optimization

### Alert Triage Efficiency

| Technique | Description | Impact |
|-----------|-------------|--------|
| Auto-enrichment | Pre-populate context | 50% faster triage |
| Auto-close FP | ML-based false positive detection | 30% fewer manual closes |
| Priority scoring | Dynamic severity adjustment | Better resource allocation |
| Batch processing | Group related alerts | 40% faster handling |
| Runbook automation | Auto-execute common responses | 60% faster MTTR |

### Shift Handover Optimization

```python
from soc_operations import HandoverOptimizer

optimizer = HandoverOptimizer()
report = optimizer.generate_handover(
    shift="day",
    include_metrics=True,
    include_open_tickets=True,
    include_ongoing_investigations=True,
    include_notable_events=True,
    include_equipment_issues=True,
)
print(f"Handover report: {len(report.sections)} sections")
print(f"Critical items: {report.critical_count}")
```

### Workload Balancing

```python
from soc_operations import WorkloadBalancer

balancer = WorkloadBalancer()
assignment = balancer.assign_ticket(
    ticket_severity="high",
    available_analysts=["analyst1", "analyst2", "analyst3"],
    criteria=["expertise", "current_load", "shift_hours"],
)
print(f"Assigned to: {assignment.analyst}")
print(f"Reason: {assignment.reason}")
```

## Security Considerations

### SOC Security Controls

| Control | Description | Implementation |
|---------|-------------|----------------|
| Access Control | Role-based access to tools | RBAC with least privilege |
| Audit Logging | Track all analyst actions | SIEM integration |
| Credential Management | Secure storage of credentials | Vault/KMS |
| Network Isolation | SOC tools on dedicated VLAN | Network segmentation |
| Data Protection | Sensitive data handling | Encryption, masking |

### Analyst Accountability

```
Required logging for all SOC actions:
├── Ticket updates and status changes
├── Evidence access and collection
├── Containment actions (IP blocks, account locks)
├── Tool usage (forensic tools, SIEM queries)
├── Escalation decisions
└── Communication with stakeholders
```

### Sensitive Data Handling

```
Data Classification:
├── Public: Alert summaries, non-sensitive metrics
├── Internal: Investigation details, IOCs
├── Confidential: Evidence, PII, credentials
└── Restricted: Legal hold, executive communications
```

## Troubleshooting Guide

### Common SOC Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Alert Fatigue | Too many low-quality alerts | Tune thresholds, retire bad rules |
| Knowledge Silos | Only one analyst knows system | Cross-training, documentation |
| Tool Fragmentation | Multiple tools, no integration | SOAR platform, API integration |
| SLA Breach | Tickets not closed on time | Escalation automation, staffing |
| Shift Gaps | Issues missed between shifts | Better handover process |

### Alert Fatigue Mitigation

```python
from soc_operations import FatigueAnalyzer

analyzer = FatigueAnalyzer()
analysis = analyzer.analyze(
    period="30d",
    alerts_by_rule=True,
    false_positive_rates=True,
)
print(f"Total alerts: {analysis.total_alerts}")
print(f"False positive rate: {analysis.fp_rate:.1%}")
print(f"Top FP rules: {analysis.top_fp_rules}")
print(f"Recommended retirements: {analysis.retirement_candidates}")
```

### Playbook Debugging

```python
from soc_operations import PlaybookDebugger

debugger = PlaybookDebugger()
trace = debugger.trace_playbook(
    playbook_id="phishing_response_001",
    include_inputs=True,
    include_outputs=True,
    include_timing=True,
)
for step in trace.steps:
    print(f"[{step.status}] {step.name}: {step.duration_ms}ms")
```

## API Reference

### TriageEngine

```python
class TriageEngine:
    def triage_alert(
        alert_type: str,
        severity: str,
        source_ip: str,
        context: dict,
    ) -> TriageDecision:
        """Triage alert and determine next action."""
    
    def get_triage_stats(period: str) -> TriageStats:
        """Get triage performance statistics."""

class TriageDecision:
    action: str           # investigate, escalate, close
    playbook: str         # recommended playbook
    escalate: bool
    priority: str
    sla_minutes: int
```

### EscalationManager

```python
class EscalationManager:
    def create_ticket(
        title: str,
        severity: str,
        analyst: str,
        alert_ids: list[str],
    ) -> Ticket:
        """Create and track security ticket."""
    
    def escalate_ticket(
        ticket_id: str,
        reason: str,
        escalate_to: str,
    ) -> EscalationResult:
        """Escalate ticket to higher tier."""

class Ticket:
    ticket_id: str
    title: str
    severity: str
    status: str
    analyst: str
    created_at: datetime
    sla_deadline: datetime
    escalation_count: int
```

### PlaybookRunner

```python
class PlaybookRunner:
    def load_playbook(name: str) -> Playbook:
        """Load playbook definition."""
    
    def execute(
        playbook: Playbook,
        context: dict,
    ) -> PlaybookResult:
        """Execute playbook steps."""
    
    def get_execution_history(
        playbook_id: str,
    ) -> list[StepResult]:
        """Get step-by-step execution history."""

class PlaybookResult:
    steps_completed: int
    total_steps: int
    evidence: list[Evidence]
    duration_seconds: float
    status: str
```

## Data Models

### Alert

```
Alert:
  alert_id: str
  rule_name: str
  severity: str
  status: str           # new, triaged, investigating, resolved, closed
  source_ip: str
  target_system: str
  created_at: datetime
  triaged_at: datetime
  resolved_at: datetime
  analyst: str
  ticket_id: str
  mitre_technique: str
  iocs: list[str]
```

### Ticket

```
Ticket:
  ticket_id: str
  title: str
  description: str
  severity: str
  status: str
  priority: str
  analyst: str
  created_at: datetime
  sla_deadline: datetime
  updated_at: datetime
  escalation_count: int
  linked_alerts: list[str]
  evidence: list[Evidence]
  resolution: str
```

### ShiftReport

```
ShiftReport:
  shift_name: str
  start_time: datetime
  end_time: datetime
  analyst_count: int
  alerts_received: int
  alerts_triaged: int
  tickets_created: int
  tickets_resolved: int
  open_items: list[str]
  ongoing_investigations: list[str]
  notable_events: list[str]
  equipment_issues: list[str]
```

## Deployment Guide

### SOC Setup Steps

```
1. Planning
   ├── Define operating hours (24/7, business hours)
   ├── Staff requirements (T1/T2/T3 ratios)
   ├── Tool selection and procurement
   └── Communication channels

2. Infrastructure
   ├── Deploy SIEM platform
   ├── Set up ticketing system
   ├── Configure chat/communication tools
   └── Set up forensic workstation

3. Process
   ├── Define escalation procedures
   ├── Create playbooks for top alert types
   ├── Document SLA requirements
   └── Establish shift handover process

4. Training
   ├── Analyst onboarding
   ├── Playbook walkthroughs
   ├── Tool training
   └── Tabletop exercises

5. Go-Live
   ├── Start with business hours coverage
   ├── Expand to 24/7 as team matures
   ├── Continuously tune and improve
   └── Regular performance reviews
```

## Monitoring & Observability

### SOC KPIs

| KPI | Target | Description |
|-----|--------|-------------|
| MTTD | <15 min | Mean Time to Detect |
| MTTR | <1 hr | Mean Time to Respond |
| FP Rate | <10% | False Positive Rate |
| Alert-to-Ticket | <20% | Alerts requiring tickets |
| SLA Compliance | >95% | Tickets closed within SLA |
| Analyst Utilization | 70-80% | Productive time ratio |

### Performance Dashboards

```
SOC Performance Dashboard:
├── Alert volume trend (daily, weekly)
├── Mean time to detect/respond
├── Tickets by severity and status
├── Analyst workload distribution
├── Playbook execution metrics
├── SLA compliance rate
└── False positive rate trend
```

## Testing Strategy

### SOC Testing

```
1. Playbook Testing
   ├── Tabletop exercises (quarterly)
   ├── Simulated incidents (monthly)
   ├── Red team coordination (quarterly)
   └── Communication drills (monthly)

2. Process Testing
   ├── Shift handover drills
   ├── Escalation path verification
   ├── SLA compliance testing
   └── Tool integration testing

3. Performance Testing
   ├── Alert volume stress testing
   ├── Peak load simulation
   ├── After-hours coverage testing
   └── Incident response timing
```

## Versioning & Migration

### Process Versioning

```
v2.0: Major process overhaul
├── New escalation paths
├── New tool integrations
└── New SLA targets

v1.x: Process improvements
├── Playbook updates
├── Rule tuning
└── Training updates

v1.0.x: Bug fixes
├── Documentation corrections
├── Tool configuration fixes
└── Minor process adjustments
```

## Glossary

| Term | Definition |
|------|-----------|
| SOC | Security Operations Center |
| MTTD | Mean Time to Detect |
| MTTR | Mean Time to Respond |
| SLA | Service Level Agreement |
| FP | False Positive |
| TP | True Positive |
| Playbook | Step-by-step response procedure |
| Runbook | Automated execution procedure |
| Tier | Analyst skill level (1=entry, 3=expert) |
| SOAR | Security Orchestration, Automation, and Response |

## Changelog

### 2.0.0 (2024-12-01)
- Added SOAR integration
- Added ChatOps alerts
- Improved playbook engine
- Added workload balancing

### 1.2.0 (2024-08-15)
- Added shift handover automation
- Added SLA tracking
- Improved escalation paths

### 1.1.0 (2024-05-20)
- Added ticket management
- Added KPI tracking
- Added quality assurance scoring

### 1.0.0 (2024-02-01)
- Initial release with basic triage
- Simple escalation paths
- Basic playbooks

## Contributing Guidelines

### Adding New Playbooks

1. Define trigger conditions
2. Document step-by-step actions
3. Include evidence collection points
4. Add escalation criteria
5. Test with tabletop exercise
6. Submit PR with test results

### Code Quality

- Type hints on all functions
- Unit tests for triage logic
- Integration tests with SOAR
- Documentation for new playbooks

## License

MIT License

Copyright (c) 2024 SOC Operations Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
