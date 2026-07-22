---
name: "incident-response"
category: "cybersecurity"
version: "2.0.0"
tags: ["cybersecurity", "incident-response", "IR", "forensics", "recovery"]
---

# Incident Response

## Overview

The Incident Response module provides comprehensive tools and methodologies for responding to cybersecurity incidents. It covers the full incident lifecycle from detection through containment, eradication, recovery, and post-incident lessons learned. The module follows NIST SP 800-61 and SANS incident response frameworks.

This skill is essential for incident responders, SOC analysts, DFIR specialists, and security operations teams managing security incidents.

## Core Capabilities

- **Incident Classification**: Severity scoring, impact assessment, and incident categorization
- **Containment**: Short-term and long-term containment strategy development
- **Eradication**: Malware removal, vulnerability patching, and IOC cleanup
- **Recovery**: System restoration, validation testing, and service restoration
- **Evidence Collection**: Forensic evidence preservation, chain of custody, and evidence handling
- **Communication**: Stakeholder notification, executive briefing, and regulatory reporting
- **Post-Incident**: Lessons learned, playbook updates, and control improvements
- **Incident Tracking**: Ticket management, SLA tracking, and status reporting

## Usage Examples

```python
from incident_response import (
    IncidentManager,
    ContainmentPlanner,
    EvidenceCollector,
    RecoveryManager,
    IRReportGenerator,
)

# --- Incident Management ---
manager = IncidentManager()
incident = manager.create_incident(
    title="Ransomware on finance workstation",
    severity="critical",
    category="ransomware",
    affected_systems=["FIN-WS-001", "FIN-SRV-001"],
)
print(f"Incident: {incident.incident_id}")
print(f"Severity: {incident.severity}")
print(f"Phase: {incident.current_phase}")

# --- Containment ---
containment = ContainmentPlanner()
plan = containment.create_plan(
    incident_id=incident.incident_id,
    short_term=["isolate_network", "disable_accounts"],
    long_term=["patch_vulnerability", "reset_credentials"],
)
print(f"Containment steps: {len(plan.steps)}")

# --- Evidence Collection ---
evidence = EvidenceCollector()
items = evidence.collect(
    system="FIN-WS-001",
    evidence_types=["memory_dump", "disk_image", "logs"],
)
for item in items:
    print(f"  {item.evidence_type}: hash={item.sha256[:16]}...")

# --- Recovery ---
recovery = RecoveryManager()
plan = recovery.create_plan(
    incident_id=incident.incident_id,
    steps=["restore_backup", "validate_systems", "monitoring"],
)
print(f"Recovery steps: {len(plan.steps)}")

# --- IR Report ---
reporter = IRReportGenerator()
report = reporter.generate(
    incident=incident,
    timeline=manager.get_timeline(incident.incident_id),
    findings=["Malware detected and contained", "Backup integrity verified"],
)
print(f"Report: {report.title}")
print(f"Recommendations: {len(report.recommendations)}")
```

## Best Practices

- Activate incident response plan immediately upon detection — don't delay
- Preserve volatile evidence first (memory, network connections) before disk imaging
- Isolate affected systems from the network but keep them powered on for forensics
- Document every action with timestamps — this is your audit trail
- Communicate early and often with stakeholders — silence breeds rumors
- Use the incident as a learning opportunity — update playbooks based on lessons
- Practice incident response regularly through tabletop exercises and simulations
- Maintain up-to-date contact lists for incident response team and stakeholders
- Implement automated containment for high-confidence detections
- Track all incidents to closure with documented root cause and remediation

## Related Modules

- **penetration-testing**: Understanding attacker techniques for better response
- **security-audit**: Post-incident compliance assessment
- **threat-intelligence**: Intelligence-driven incident response
- **digital-forensics**: Deep forensic analysis during incident investigation

---

## Advanced Configuration

### Incident Severity Configuration

Configure incident severity levels.

```python
severity_config = SeverityConfig(
    levels={
        "critical": {
            "description": "Critical business impact",
            "response_time_minutes": 15,
            "escalation": "ciso",
            "communication": "executive_team",
        },
        "high": {
            "description": "Significant impact",
            "response_time_minutes": 30,
            "escalation": "security_manager",
            "communication": "it_leadership",
        },
        "medium": {
            "description": "Moderate impact",
            "response_time_minutes": 60,
            "escalation": "soc_lead",
            "communication": "security_team",
        },
        "low": {
            "description": "Minimal impact",
            "response_time_minutes": 240,
            "escalation": "analyst",
            "communication": "security_team",
        },
    },
)
```

### Playbook Configuration

Configure incident response playbooks.

```python
playbook_config = PlaybookConfig(
    playbooks={
        "ransomware": {
            "phases": ["containment", "eradication", "recovery", "lessons_learned"],
            "team": ["incident_responder", "forensics", "legal", "pr"],
            "external_notifications": ["fbi", "cyber_insurance"],
        },
        "data_breach": {
            "phases": ["containment", "assessment", "notification", "remediation"],
            "team": ["incident_responder", "legal", "privacy_officer"],
            "external_notifications": ["affected_individuals", "regulators"],
        },
        "insider_threat": {
            "phases": ["detection", "investigation", "containment", "remediation"],
            "team": ["incident_responder", "hr", "legal"],
            "external_notifications": [],
        },
    },
)
```

### Evidence Collection Configuration

Configure forensic evidence collection.

```python
evidence_config = ForensicEvidenceConfig(
    collection_order=[
        "volatile_memory",
        "network_connections",
        "process_list",
        "disk_image",
        "log_files",
    ],
    preservation={
        "hash_algorithm": "sha256",
        "chain_of_custody": True,
        "encryption": "AES-256",
        "storage_location": "secure_forensics_server",
    },
)
```

---

## Architecture Patterns

### NIST IR Lifecycle Pattern

```python
class NISTIRLifecycle:
    phases = [
        "preparation",
        "detection_analysis",
        "containment",
        "eradication",
        "recovery",
        "post_incident_activity",
    ]

    def execute(self, incident):
        context = {"incident": incident, "evidence": [], "actions": []}
        for phase in self.phases:
            handler = self.get_phase_handler(phase)
            context = handler.execute(context)
        return context
```

### Containment Strategy Pattern

```python
class ContainmentStrategy:
    def __init__(self):
        self.short_term = ShortTermContainment()
        self.long_term = LongTermContainment()

    def execute(self, incident):
        # Short-term: immediate containment
        self.short_term.isolate_systems(incident.affected_systems)
        self.short_term.block_malicious_ips(incident.indicators)

        # Long-term: root cause remediation
        self.long_term.patch_vulnerabilities(incident.root_cause)
        self.long_term.reset_credentials(incident.compromised_accounts)
```

### Communication Plan Pattern

```python
class CommunicationPlan:
    def __init__(self):
        self.stakeholders = {
            "executive": {"template": "executive_brief", "frequency": "daily"},
            "technical": {"template": "technical_detail", "frequency": "real_time"},
            "legal": {"template": "legal_brief", "frequency": "as_needed"},
            "public": {"template": "public_statement", "frequency": "as_needed"},
        }

    def notify(self, incident, audience):
        template = self.stakeholders[audience]["template"]
        message = self.render_template(template, incident)
        self.send(audience, message)
```

---

## Integration Guide

### SIEM Integration

```python
# Query SIEM for incident context
siem = SIEMIntegration(
    platform="splunk",
    host="splunk.internal",
    api_key="...",
)

# Search for related events
results = siem.search(
    query=f"index=security src_ip={incident.source_ip} | last 24h",
    max_results=1000,
)
```

### Ticketing Integration

```python
# Create incident ticket
ticketing = TicketingIntegration(
    platform="jira",
    project="SECURITY",
    api_key="...",
)

ticket = ticketing.create_ticket(
    title=f"Incident: {incident.title}",
    description=incident.description,
    severity=incident.severity,
    assignee=incident.assignee,
)
```

### Communication Platform Integration

```python
# Notify via Slack
slack = SlackIntegration(webhook_url="...")

slack.send_incident_notification(
    channel="#security-incidents",
    incident=incident,
    severity=incident.severity,
)
```

---

## Performance Optimization

### Evidence Processing

```python
# Parallel evidence collection
def collect_evidence_parallel(systems, evidence_types):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for system in systems:
            for evidence_type in evidence_types:
                futures.append(executor.submit(collect_evidence, system, evidence_type))
        return [f.result() for f in futures]
```

### Log Analysis Optimization

```python
# Efficient log analysis
log_analyzer = LogAnalyzer(
    batch_size=10000,
    parallel_processing=True,
    index_optimization=True,
)
```

---

## Security Considerations

### Chain of Custody

```python
class ChainOfCustody:
    def __init__(self):
        self.evidence_log = []

    def add_entry(self, evidence_id, handler, action, timestamp):
        entry = {
            "evidence_id": evidence_id,
            "handler": handler,
            "action": action,
            "timestamp": timestamp,
            "hash": self.calculate_hash(evidence_id),
        }
        self.evidence_log.append(entry)

    def verify_integrity(self, evidence_id):
        # Verify hash chain
        entries = [e for e in self.evidence_log if e["evidence_id"] == evidence_id]
        return all(self.verify_hash_chain(entries))
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Evidence corrupted | Improper handling | Re-collect with proper procedures |
| Communication delayed | Unclear escalation | Follow communication plan |
| Recovery incomplete | Root cause not addressed | Complete eradication phase |

---

## API Reference

### IncidentManager

```python
class IncidentManager:
    def create_incident(title, severity, category, affected_systems) -> Incident
    def update_incident(incident_id, updates) -> Incident
    def get_timeline(incident_id) -> List[TimelineEntry]
    def close_incident(incident_id, root_cause, remediation) -> None
```

### ContainmentPlanner

```python
class ContainmentPlanner:
    def create_plan(incident_id, short_term, long_term) -> ContainmentPlan
    def execute_plan(plan) -> ContainmentResult
    def validate_containment(incident_id) -> ValidationResult
```

### EvidenceCollector

```python
class EvidenceCollector:
    def collect(system, evidence_types) -> List[EvidenceItem]
    def preserve(evidence_item) -> PreservedEvidence
    def verify_chain_of_custody(evidence_id) -> bool
```

---

## Data Models

### Incident

```python
@dataclass
class Incident:
    incident_id: str
    title: str
    severity: str
    category: str
    status: str
    affected_systems: List[str]
    timeline: List[TimelineEntry]
    evidence: List[EvidenceItem]
    created_at: datetime
    updated_at: datetime
```

### EvidenceItem

```python
@dataclass
class EvidenceItem:
    evidence_id: str
    evidence_type: str
    source_system: str
    sha256_hash: str
    collected_at: datetime
    collected_by: str
    description: str
```

---

## Deployment Guide

### IR Platform Deployment

```yaml
services:
  ir-platform:
    image: incident-response:latest
    environment:
      - DATABASE_URL=postgresql://...
      - SIEM_URL=https://splunk.internal
      - TICKETING_URL=https://jira.internal
    volumes:
      - ./playbooks:/playbooks
      - ./evidence:/evidence
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `ir.incident.count` | Active incidents | Spike |
| `ir.response.time` | Response time | > SLA |
| `ir.evidence.collected` | Evidence collected | Track |
| `ir.remediation.time` | Time to remediate | > SLA |

---

## Testing Strategy

### IR Tests

```python
def test_incident_lifecycle():
    manager = IncidentManager()
    incident = manager.create_incident("Test Incident", "medium", "malware", ["ws-001"])
    assert incident.status == "open"

    manager.update_incident(incident.incident_id, {"status": "contained"})
    assert incident.status == "contained"
```

### Tabletop Exercises

```python
# Run tabletop exercise
exercise = TabletopExercise(
    scenario="ransomware_attack",
    participants=["security_team", "it_ops", "management"],
    duration_hours=2,
)
exercise.execute()
```

---

## Versioning & Migration

### Playbook Versioning

Track playbook versions for continuous improvement.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Incident** | Security event requiring response |
| **Containment** | Limiting incident damage |
| **Eradication** | Removing threat from environment |
| **Chain of Custody** | Evidence handling documentation |
| **Tabletop Exercise** | Simulated incident response drill |

---

## Changelog

### v2.0.0
- Added playbook automation
- Evidence chain of custody
- Communication templates

### v1.0.0
- Initial release with basic incident tracking

---

## Contributing Guidelines

- Document all procedures
- Practice incident response regularly
- Update playbooks based on lessons learned

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
