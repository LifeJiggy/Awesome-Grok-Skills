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
