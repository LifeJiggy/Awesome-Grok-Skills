---
name: "incident-response"
category: "blue-team"
version: "2.0.0"
tags: ["blue-team", "incident-response", "DFIR", "containment", "recovery"]
---

# Incident Response

## Overview

The Incident Response module provides structured tools and workflows for handling security incidents from initial detection through containment, eradication, recovery, and post-incident analysis. It follows NIST SP 800-61 and SANS Incident Response lifecycle frameworks. The module includes evidence collection procedures, chain of custody management, communication templates, and lessons-learned documentation.

This skill is essential for incident responders, DFIR analysts, SOC teams, and security managers responsible for managing security breaches and minimizing organizational impact.

## Core Capabilities

- **Incident Classification**: Severity scoring, impact assessment, scope determination, and incident categorization
- **Containment Procedures**: Network isolation, account lockdown, endpoint quarantine, and DNS sinkholing
- **Evidence Collection**: Forensic imaging, volatile data collection, memory dumps, and log preservation
- **Chain of Custody**: Evidence tracking, hash verification, and legal admissibility procedures
- **Eradication**: Malware removal, IOC cleanup, credential rotation, and vulnerability patching
- **Recovery**: System restoration, validation testing, monitoring enhancement, and service restoration
- **Communication**: Stakeholder notifications, executive briefings, regulatory reporting (GDPR 72hr, HIPAA)
- **Post-Incident**: Lessons learned documentation, playbook updates, and control gap analysis

## Usage Examples

```python
from incident_response import (
    IncidentManager,
    ContainmentEngine,
    EvidenceCollector,
    ChainOfCustody,
    RecoveryManager,
    CommunicationManager,
)

# --- Incident Creation ---
manager = IncidentManager()
incident = manager.create_incident(
    title="Ransomware infection on finance workstation",
    severity="critical",
    category="malware",
    affected_systems=["FIN-WS-001", "FIN-SRV-001"],
    initial_indicators=["Encrypted files", "Ransom note present"],
)
print(f"Incident: {incident.incident_id}")
print(f"Severity: {incident.severity}")
print(f"Phase: {incident.current_phase}")

# --- Containment ---
containment = ContainmentEngine()
actions = containment.execute_containment(
    incident_id=incident.incident_id,
    systems=["FIN-WS-001"],
    actions=["isolate_network", "disable_account", "block_iocs"],
)
for action in actions:
    print(f"  {action.action}: {action.status}")

# --- Evidence Collection ---
collector = EvidenceCollector()
evidence = collector.collect_volatile_data(
    system="FIN-WS-001",
    items=["memory_dump", "running_processes", "network_connections", "browser_history"],
)
for item in evidence:
    print(f"  {item.item_type}: hash={item.sha256[:16]}...")

# --- Chain of Custody ---
coc = ChainOfCustody()
coc.register_evidence(
    evidence_id=evidence[0].evidence_id,
    collector="analyst1",
    description="Memory dump from FIN-WS-001",
)
coc.transfer(
    evidence_id=evidence[0].evidence_id,
    from_person="analyst1",
    to_person="forensics_team",
    reason="Deep analysis required",
)

# --- Recovery ---
recovery = RecoveryManager()
plan = recovery.create_recovery_plan(
    incident_id=incident.incident_id,
    systems=["FIN-WS-001", "FIN-SRV-001"],
    steps=["restore_from_backup", "patch_vulnerability", "reset_credentials", "validate_integrity"],
)
print(f"Recovery steps: {len(plan.steps)}")
print(f"Estimated time: {plan.estimated_hours}h")

# --- Communication ---
comms = CommunicationManager()
comms.send_notification(
    recipients=["ciso@company.com", "legal@company.com"],
    subject=f"Incident {incident.incident_id} - Critical",
    message="Ransomware incident detected. Containment in progress.",
    classification="confidential",
)
print(f"Notifications sent")

# --- Post-Incident Report ---
report = manager.generate_post_incident_report(incident.incident_id)
print(f"Report sections: {len(report.sections)}")
print(f"Recommendations: {len(report.recommendations)}")
```

## Best Practices

- Activate the incident response plan BEFORE an incident occurs — don't build the plane while flying it
- Establish clear severity levels with defined response time SLAs (Critical: 15min, High: 1hr)
- Collect volatile evidence first (memory, network connections) before disk imaging
- Always calculate and record cryptographic hashes (SHA-256) for all collected evidence
- Maintain chain of custody documentation from the moment evidence is collected
- Separate containment from eradication — contain first, then plan eradication carefully
- Test recovery procedures before you need them; untested backups are not backups
- Conduct lessons-learned meetings within 1 week of incident closure
- Update detection rules and playbooks based on lessons learned from every incident
- Establish relationships with legal, PR, and executive teams before incidents occur

## Related Modules

- **digital-forensics**: Deep forensic analysis tools for post-incident investigation
- **security-monitoring**: Alert detection that triggers incident response
- **threat-hunting**: Proactive search for indicators found during incidents
- **soc-operations**: Day-to-day operations that support incident response
