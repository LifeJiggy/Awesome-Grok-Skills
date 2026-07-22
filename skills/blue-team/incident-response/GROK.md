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

## Advanced Configuration

### Incident Response Platform Configuration

```yaml
# Incident management platform
platform:
  name: "PagerDuty"
  api_key: "${PAGERDUTY_API_KEY}"
  escalation_policies:
    critical:
      policy_id: "P1CRITICAL"
      notify_method: ["phone", "sms", "email"]
      escalation_delay: 0
    high:
      policy_id: "P2HIGH"
      notify_method: ["sms", "email"]
      escalation_delay: 300
    medium:
      policy_id: "P3MEDIUM"
      notify_method: ["email"]
      escalation_delay: 1800
```

### Evidence Collection Configuration

```yaml
evidence_collection:
  forensic_workstation:
    ip: "10.0.0.100"
    credentials_vault: "hashicorp_vault"
    storage_location: "/evidence/cases"
  imaging:
    tool: "ftk_imager"
    hash_algorithm: "sha256"
    compression: "lz4"
    verification: true
  volatile_data:
    timeout_seconds: 300
    network_capture: true
    memory_dump: true
    process_list: true
```

### Communication Templates

```yaml
templates:
  executive_briefing:
    subject: "Security Incident {incident_id} - Executive Update"
    recipients: ["ciso", "cto", "legal", "pr"]
    classification: "confidential"
    sections:
      - summary
      - impact
      - containment_status
      - business_impact
      - next_steps
  regulatory_notification:
    subject: "Regulatory Notification - {incident_id}"
    recipients: ["legal", "compliance"]
    classification: "restricted"
    sections:
      - incident_summary
      - data_types_affected
      - affected_records
      - remediation_actions
      - notification_timeline
```

## Architecture Patterns

### NIST Incident Response Lifecycle

```
1. Preparation
   ├── IR plan documentation
   ├── Team roles and responsibilities
   ├── Tool deployment and testing
   ├── Communication channels
   └── Training and exercises

2. Detection & Analysis
   ├── Alert triage
   ├── Initial assessment
   ├── Scope determination
   ├── Evidence collection
   └── Documentation

3. Containment, Eradication, Recovery
   ├── Short-term containment
   ├── Long-term containment
   ├── Evidence preservation
   ├── Eradication
   └── Recovery

4. Post-Incident Activity
   ├── Lessons learned
   ├── Playbook updates
   ├── Detection improvements
   ├── Control gap analysis
   └── Report generation
```

### Incident Classification

| Severity | Criteria | Response Time | Team |
|----------|----------|---------------|------|
| Critical | Active data breach, ransomware, APT | Immediate | Full IR team |
| High | Confirmed compromise, lateral movement | 15 min | IR team + management |
| Medium | Suspicious activity, potential compromise | 1 hour | SOC + IR support |
| Low | Policy violation, minor incident | 4 hours | SOC |

### Chain of Custody Process

```
Evidence Collection
├── Document collector identity
├── Record collection timestamp
├── Calculate hash (SHA-256)
├── Label evidence bag
└── Store in secure location

Evidence Transfer
├── Record transfer date/time
├── Record receiver identity
├── Verify hash integrity
├── Update chain of custody log
└── Store transfer receipt

Evidence Storage
├── Climate-controlled environment
├── Tamper-evident packaging
├── Access logging
├── Periodic integrity checks
└── Retention policy compliance
```

## Integration Guide

### Forensic Tool Integration

```python
from incident_response import ForensicToolIntegration

# Volatility memory analysis
volatility = ForensicToolIntegration(
    tool="volatility3",
    evidence_path="/evidence/cases/CASE-001/memory.raw",
)

# Extract processes
processes = volatility.run_plugin("windows.pslist")
print(f"Processes found: {len(processes)}")

# Extract network connections
connections = volatility.run_plugin("windows.netscan")
print(f"Network connections: {len(connections)}")

# Extract injected code
injected = volatility.run_plugin("windows.malfind")
print(f"Injected code regions: {len(injected)}")
```

### Network Forensics Integration

```python
from incident_response import NetworkForensics

tcpdump = NetworkForensics(
    tool="tcpdump",
    interface="eth0",
    bpf_filter="host 192.168.1.100",
)

# Capture traffic
capture = tcpdump.capture(
    duration_seconds=300,
    output_file="/evidence/cases/CASE-001/capture.pcap",
)
print(f"Captured {capture.packet_count} packets")
print(f"Duration: {capture.duration_seconds}s")
```

### SIEM Integration

```python
from incident_response import SIEMIntegration

siem = SIEMIntegration(
    platform="splunk",
    url="https://splunk.internal:8089",
    token="${SPLUNK_TOKEN}",
)

# Pull related events
events = siem.query(
    f'index=security src_ip="{compromised_ip}" earliest=-24h',
    max_results=1000,
)
print(f"Related events: {len(events)}")
```

## Performance Optimization

### Incident Response Time Optimization

| Technique | Description | Impact |
|-----------|-------------|--------|
| Pre-built playbooks | Ready-to-execute procedures | 50% faster response |
| Automated containment | Auto-isolate compromised hosts | 80% faster containment |
| Evidence pre-staging | Forensic tools ready to deploy | 30% faster collection |
| Communication templates | Pre-approved messaging | 40% faster notification |
| Runbook automation | Auto-execute common steps | 60% faster MTTR |

### Evidence Collection Speed

```
Optimization Strategy:
├── Prioritize volatile evidence (memory, network)
├── Use streaming collection (not stop-the-world)
├── Parallel collection of independent evidence
├── Pre-configured collection scripts
└── Automated hash calculation and logging
```

### Recovery Acceleration

```python
from incident_response import RecoveryOptimizer

optimizer = RecoveryOptimizer()
plan = optimizer.optimize_recovery(
    systems=["FIN-WS-001", "FIN-SRV-001"],
    backup_location="s3://backups/",
    verification_required=True,
    parallel_restore=True,
)
print(f"Estimated recovery time: {plan.estimated_hours}h")
print(f"Parallel restores: {plan.parallel_count}")
```

## Security Considerations

### Evidence Security

| Control | Description | Implementation |
|---------|-------------|----------------|
| Tamper Detection | Verify evidence integrity | SHA-256 hash verification |
| Access Control | Restrict evidence access | RBAC + MFA |
| Encryption | Protect evidence at rest | AES-256 encryption |
| Audit Logging | Track all evidence access | SIEM integration |
| Retention | Comply with legal requirements | Automated retention policies |

### Legal Considerations

```
Evidence Admissibility Requirements:
├── Chain of custody documentation
├── Hash verification at collection and transfer
├── Proper handling procedures
├── Qualified examiner credentials
├── Methodology documentation
└── Tool validation records
```

### Privacy Compliance

```
Data Protection During IR:
├── Minimize collection of PII
├── Redact unnecessary personal data
├── Secure storage of collected data
├── Retention limits aligned with policy
├── Right to deletion considerations
└── Cross-border data transfer rules
```

## Troubleshooting Guide

### Common IR Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Evidence Tampering | Hash mismatch | Re-collect with verification |
| Chain of Custody Gap | Missing transfer record | Document gap, add explanation |
| Slow Containment | Lateral movement continues | Increase containment aggressiveness |
| Communication Failure | Stakeholders uninformed | Establish backup channels |
| Recovery Failure | Systems won't restore | Use alternative backup source |

### Evidence Integrity Issues

```python
from incident_response import EvidenceValidator

validator = EvidenceValidator()
result = validator.verify_evidence(
    evidence_id="EVD-001",
    expected_hash="abc123...",
    expected_algorithm="sha256",
)
if result.valid:
    print("Evidence integrity verified")
else:
    print(f"Integrity failure: {result.error}")
    print(f"Expected: {result.expected_hash}")
    print(f"Actual: {result.actual_hash}")
```

### Communication Debugging

```
Issue: Executives not informed
1. Verify distribution list is current
2. Check email delivery (spam, delays)
3. Use backup channel (phone, SMS)
4. Escalate to CISO directly

Issue: Regulatory notification delayed
1. Verify legal review timeline
2. Check notification template readiness
3. Confirm affected data scope
4. Document delay reason
```

## API Reference

### IncidentManager

```python
class IncidentManager:
    def create_incident(
        title: str,
        severity: str,
        category: str,
        affected_systems: list[str],
        initial_indicators: list[str],
    ) -> Incident:
        """Create new security incident."""
    
    def update_incident(
        incident_id: str,
        status: str,
        notes: str,
    ) -> Incident:
        """Update incident status and notes."""
    
    def close_incident(
        incident_id: str,
        resolution: str,
        lessons_learned: str,
    ) -> Incident:
        """Close incident with resolution."""

class Incident:
    incident_id: str
    title: str
    severity: str
    category: str
    status: str
    current_phase: str
    affected_systems: list[str]
    created_at: datetime
    updated_at: datetime
    assigned_to: str
    evidence: list[Evidence]
```

### ContainmentEngine

```python
class ContainmentEngine:
    def execute_containment(
        incident_id: str,
        systems: list[str],
        actions: list[str],
    ) -> list[ContainmentAction]:
        """Execute containment actions."""
    
    def isolate_network(host: str) -> ActionResult:
        """Isolate host from network."""
    
    def block_ip(ip: str, duration_hours: int = 24) -> ActionResult:
        """Block IP at firewall."""

class ContainmentAction:
    action: str
    target: str
    status: str
    timestamp: datetime
    executed_by: str
```

### EvidenceCollector

```python
class EvidenceCollector:
    def collect_volatile_data(
        system: str,
        items: list[str],
    ) -> list[Evidence]:
        """Collect volatile evidence from system."""
    
    def image_disk(
        system: str,
        output_path: str,
        compression: str = "lz4",
    ) -> DiskImage:
        """Create forensic disk image."""
    
    def capture_network(
        interface: str,
        duration_seconds: int,
        bpf_filter: str = None,
    ) -> CaptureResult:
        """Capture network traffic."""

class Evidence:
    evidence_id: str
    item_type: str
    source_system: str
    collected_at: datetime
    collected_by: str
    sha256: str
    size_bytes: int
    storage_path: str
```

## Data Models

### Incident

```
Incident:
  incident_id: str
  title: str
  severity: str
  category: str
  status: str
  current_phase: str
  affected_systems: list[str]
  initial_indicators: list[str]
  timeline: list[TimelineEntry]
  evidence: list[Evidence]
  communications: list[Communication]
  assigned_to: str
  created_at: datetime
  updated_at: datetime
  closed_at: datetime
```

### Evidence

```
Evidence:
  evidence_id: str
  incident_id: str
  item_type: str
  description: str
  source_system: str
  collected_at: datetime
  collected_by: str
  hash_algorithm: str
  hash_value: str
  size_bytes: int
  storage_path: str
  chain_of_custody: list[CustodyEntry]
```

### ChainOfCustodyEntry

```
ChainOfCustodyEntry:
  entry_id: str
  evidence_id: str
  action: str          # collected, transferred, accessed
  timestamp: datetime
  person: str
  reason: str
  hash_verified: bool
  location: str
```

## Deployment Guide

### IR Team Setup

```
1. Team Structure
   ├── IR Lead
   ├── Technical Lead
   ├── Forensic Analysts
   ├── Communication Lead
   ├── Legal Liaison
   └── Management Sponsor

2. Tool Deployment
   ├── Forensic workstation setup
   ├── Evidence storage infrastructure
   ├── Communication platform
   ├── Ticketing system
   └── SIEM access

3. Documentation
   ├── IR plan
   ├── Playbooks for common incidents
   ├── Contact lists
   ├── Legal requirements
   └── Vendor contacts

4. Training
   ├── Tabletop exercises (quarterly)
   ├── Technical training
   ├── Legal and compliance training
   └── Communication training
```

### Evidence Infrastructure

```
Requirements:
├── Forensic workstation (isolated network)
├── Evidence storage (encrypted, RAID)
├── Write blockers (hardware)
├── Network tap (for live capture)
├── Secure transfer mechanism
└── Backup and redundancy
```

## Monitoring & Observability

### IR Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| MTTD | <15 min | Mean Time to Detect |
| MTTC | <30 min | Mean Time to Contain |
| MTTR | <4 hrs | Mean Time to Recover |
| Evidence Integrity | 100% | Hash verification pass rate |
| Communication Time | <1 hr | Stakeholder notification time |
| Lessons Learned | 100% | Incidents with post-mortem |

### Incident Dashboard

```
Incident Dashboard:
├── Active incidents by severity
├── Incidents by category
├── Mean time to detect/respond
├── Evidence collection status
├── Communication timeline
├── Recovery progress
└── Trend analysis (30d, 90d)
```

## Testing Strategy

### IR Testing

```
1. Tabletop Exercises
   ├── Scenario walkthrough (quarterly)
   ├── Decision point analysis
   ├── Communication drill
   └── Documentation review

2. Technical Exercises
   ├── Evidence collection drill
   ├── Forensic analysis exercise
   ├── Recovery procedure test
   └── Tool proficiency test

3. Full-Scale Exercises
   ├── Simulated incident (annual)
   ├── Red team coordination
   ├── Legal involvement
   └── Executive notification
```

## Versioning & Migration

### IR Plan Versioning

```
v3.0: Major plan overhaul
├── New incident categories
├── Updated escalation paths
├── New tool integrations
└── Regulatory changes

v2.x: Plan updates
├── Playbook additions
├── Contact list updates
└── Tool configuration changes

v2.0.x: Minor updates
├── Documentation corrections
└── Template updates
```

## Glossary

| Term | Definition |
|------|-----------|
| Chain of Custody | Documented evidence handling history |
| Containment | Limiting incident spread and damage |
| DFIR | Digital Forensics and Incident Response |
| Eradication | Removing threat actor from environment |
| IoC | Indicator of Compromise |
| Playbook | Step-by-step incident response procedure |
| Recovery | Restoring systems to normal operation |
| Root Cause | Underlying reason for the incident |
| Triage | Initial assessment and prioritization |
| Volatile Evidence | Data that changes quickly (memory, connections) |

## Changelog

### 2.0.0 (2024-12-01)
- Added automated containment
- Added evidence chain of custody tracking
- Improved communication templates
- Added regulatory notification support

### 1.2.0 (2024-08-15)
- Added memory forensics integration
- Added network forensics integration
- Improved recovery planning

### 1.1.0 (2024-05-20)
- Added evidence collection procedures
- Added incident classification matrix
- Improved post-incident reporting

### 1.0.0 (2024-02-01)
- Initial release with basic incident management
- Simple containment procedures
- Basic evidence collection

## Contributing Guidelines

### Adding New Playbooks

1. Define trigger conditions and scope
2. Document step-by-step procedures
3. Include evidence collection points
4. Add escalation criteria
5. Test with tabletop exercise
6. Submit PR with exercise results

### Code Quality

- Type hints on all functions
- Unit tests for IR logic
- Integration tests with forensic tools
- Documentation for new procedures

## License

MIT License

Copyright (c) 2024 Incident Response Contributors

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
