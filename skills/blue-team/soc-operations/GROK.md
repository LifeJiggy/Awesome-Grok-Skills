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
