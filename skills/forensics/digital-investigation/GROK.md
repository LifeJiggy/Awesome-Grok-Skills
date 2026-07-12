---
name: "digital-investigation"
category: "forensics"
version: "2.0.0"
tags: ["forensics", "digital-investigation", "incident-response", "evidence-collection", "chain-of-custody"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["python", "forensics-fundamentals", "operating-systems"]
---

# Digital Investigation

## Overview

Digital investigation provides the methodology and tools for conducting forensic examinations of digital evidence across computers, networks, mobile devices, and cloud environments. This module covers incident response procedures, evidence collection and preservation, chain of custody management, timeline analysis, artifact recovery, and expert testimony preparation. It addresses the critical need for legally admissible digital evidence handling in criminal, civil, and regulatory investigations.

## Core Capabilities

- **Incident Response**: Structured IR lifecycle (preparation, identification, containment, eradication, recovery, lessons learned) with playbooks for common incident types
- **Evidence Collection**: Forensic imaging (dd, FTK Imager), live acquisition, volatile data capture, and remote evidence collection from cloud/SaaS
- **Chain of Custody**: Digital chain of custody tracking with cryptographic hashing, tamper-evident logs, and court-admissible documentation
- **Timeline Analysis**: Cross-source timeline reconstruction correlating file system, registry, event logs, browser history, and network activity
- **Artifact Recovery**: Deleted file recovery, file system metadata analysis, file carving, and slack space analysis
- **Memory Analysis**: RAM dump analysis for process extraction, network connections, encryption keys, and malware artifacts
- **Log Analysis**: Centralized log analysis across Windows Event Logs, syslog, application logs, and cloud audit trails
- **Report Generation**: Professional forensic examination reports with findings, evidence catalog, and expert opinion sections
- **Legal Compliance**: Evidence handling procedures meeting Federal Rules of Evidence, Daubert standard, and international equivalents
- **Tool Integration**: Orchestration of Autopsy, Volatility, Wireshark, YARA, and custom Python analysis scripts

## Usage Examples

### Incident Response Playbook

```python
from forensics.digital_investigation import IncidentResponder, IncidentType, Severity

responder = IncidentResponder(
    organization="Acme Corp",
    ir_team="CERT",
    playbooks_dir="playbooks/",
)

# Initiate incident response
incident = responder.create_incident(
    incident_type=IncidentType.MALWARE,
    severity=Severity.HIGH,
    description="Ransomware detected on Finance workstation FS-001",
    reported_by="EDR Alert",
    affected_systems=["FS-001", "FS-002", "FIN-SERVER-01"],
)

print(f"Incident: {incident.incident_id}")
print(f"Severity: {incident.severity.value}")
print(f"Phase: {incident.current_phase}")
print(f"Playbook: {incident.playbook_name}")

# Execute containment
responder.execute_phase(incident.incident_id, "containment", {
    "actions": ["isolate_network", "disable_account", "snapshot_disk"],
    "timestamp": "2026-07-01T14:30:00Z",
})
```

### Evidence Collection

```python
from forensics.digital_investigation import EvidenceCollector, EvidenceType

collector = EvidenceCollector(
    case_number="CASE-2026-0042",
    examiner="Dr. Sarah Chen",
    lab="Digital Forensics Lab",
)

# Create forensic image
evidence = collector.image_disk(
    source="\\\\FS-001\\PhysicalDrive0",
    destination="EVIDENCE/CASE-2026-0042/FS001_E01.E01",
    evidence_type=EvidenceType.DISK_IMAGE,
    write_blocker=True,
    compression=True,
    description="Full disk image of ransomware-affected workstation",
)

print(f"Evidence ID: {evidence.evidence_id}")
print(f"Source Hash (MD5): {evidence.md5_hash}")
print(f"Source Hash (SHA256): {evidence.sha256_hash}")
print(f"Image Size: {evidence.size_bytes / 1e9:.2f} GB")
print(f"Write Status: {'Protected' if evidence.write_blocker_used else 'UNPROTECTED'}")
```

### Chain of Custody

```python
from forensics.digital_investigation import ChainOfCustody

coc = ChainOfCustody(case_number="CASE-2026-0042")

# Record evidence transfer
transfer = coc.transfer(
    evidence_id="EVD-001",
    from_custodian="Crime Scene Team",
    to_custodian="Forensic Lab",
    purpose="Forensic Examination",
    condition="Sealed, tamper-evident bag intact",
    location="Evidence Room B",
)

print(f"Transfer: {transfer.transfer_id}")
print(f"Timestamp: {transfer.timestamp}")
print(f"Hash Verified: {transfer.hash_verified}")

# Generate custody report
report = coc.generate_report(case_number="CASE-2026-0042")
print(f"\nChain of Custody Report:")
print(f"  Total Transfers: {report.total_transfers}")
print(f"  Evidence Items: {report.evidence_count}")
print(f"  Integrity Status: {report.integrity_status}")
```

### Timeline Analysis

```python
from forensics.digital_investigation import TimelineAnalyzer

analyzer = TimelineAnalyzer(
    timezone="UTC",
    time_skew_tolerance_seconds=30,
)

# Build timeline from multiple sources
timeline = analyzer.build_timeline(
    case_number="CASE-2026-0042",
    sources=[
        {"type": "file_system", "path": "EVIDENCE/FS001_E01.E01"},
        {"type": "windows_event_log", "path": "EVIDENCE/FS001_EventLogs/"},
        {"type": "browser_history", "path": "EVIDENCE/FS001_Browser/"},
        {"type": "prefetch", "path": "EVIDENCE/FS001_Prefetch/"},
    ],
    filters={
        "start_date": "2026-06-28",
        "end_date": "2026-07-02",
        "keywords": ["encrypt", "ransom", "payment", ".onion"],
    },
)

print(f"Timeline Events: {timeline.total_events}")
print(f"Time Range: {timeline.start_time} to {timeline.end_time}")
for event in timeline.key_events[:10]:
    print(f"  [{event.timestamp}] {event.source}: {event.description}")
```

## Architecture

```
Evidence Sources
├── Disk Images (E01, RAW, VHD)
├── Memory Dumps
├── Network Captures
├── Cloud Audit Logs
├── Mobile Device Extractions
└── Physical Media
         │
         ▼
┌─────────────────────┐
│  Processing Layer    │──→ Parsing, indexing, hash verification
│  (Autopsy / Custom)  │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│Timeline│ │Artifact│──→ File system, registry, logs
│Engine  │ │Analysis│
└────┬───┘ └────┬───┘
     │          │
     ▼          ▼
┌─────────────────────┐
│  Case Management     │──→ Evidence catalog, chain of custody
│  (Reporting)         │
└─────────────────────┘
```

## Best Practices

- Always use write blockers for physical disk acquisitions to maintain evidence integrity
- Document every evidence handling action with timestamp, personnel, and purpose for chain of custody
- Verify cryptographic hashes (MD5 + SHA256) at acquisition, before analysis, and before presentation
- Capture volatile data (memory, network connections, logged-on users) before powering down systems
- Maintain separate work copies of evidence; never analyze original forensic images directly
- Use tool validation (NIST CFTT) approved tools for forensic imaging and analysis
- Document examiner qualifications and methodology for Daubert/Frye admissibility challenges
- Preserve raw evidence with minimal processing; apply analysis techniques to working copies
- Correlate artifacts across multiple sources to build a comprehensive timeline of events
- Prepare examination reports contemporaneously with analysis, not weeks afterward

## Related Modules

- `forensics/memory-forensics` - RAM dump analysis for volatile artifacts
- `forensics/network-forensics` - Network traffic capture and analysis
- `forensics/disk-forensics` - File system and disk-level analysis
- `forensics/mobile-forensics` - Mobile device evidence extraction
