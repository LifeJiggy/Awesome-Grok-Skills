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

## Advanced Configuration

### Evidence Collection Configuration

```yaml
evidence_collection:
  imaging:
    tools:
      - name: "FTK Imager"
        version: "4.7"
        nist_cftt_approved: true
        supported_formats: ["E01", "RAW", "AFF4"]
        
      - name: "dd"
        version: "coreutils"
        nist_cftt_approved: true
        supported_formats: ["RAW"]
        
      - name: "Guymager"
        version: "0.8"
        nist_cftt_approved: true
        supported_formats: ["E01", "AFF4"]
        
    hash_algorithms:
      - "MD5"
      - "SHA1"
      - "SHA256"
      
    verification:
      verify_after_imaging: true
      verify_before_analysis: true
      hash_comparison_threshold: 0
      
  write_blockers:
    hardware:
      - name: "Tableau T356789iu"
        type: "USB 3.0"
        supported_interfaces: ["SATA", "IDE"]
        
      - name: "Tableau T8-R2"
        type: "PCIe"
        supported_interfaces: ["NVMe", "SATA"]
        
    software:
      - name: "Linux write blocker"
        method: "block_device_readonly"
        command: "blockdev --setro /dev/sdX"
        
  volatile_data:
    capture_order:
      - "network_connections"
      - "running_processes"
      - "logged_on_users"
      - "open_files"
      - "memory_dump"
      - "registry_hives"
      
    memory_dump:
      tools:
        - "FTK Imager Lite"
        - "Magnet RAM Capture"
        - "Belkasoft RAM Capturer"
      compression: true
      hash_after_capture: true
```

### Chain of Custody Configuration

```yaml
chain_of_custody:
  tracking:
    method: "blockchain"
    blockchain_network: "private"
    block_confirmation_required: 3
    
  evidence_labels:
    format: "CASE-{case_number}-EVD-{sequence}"
    barcode_enabled: true
    rfid_enabled: false
    
  transfer_procedure:
    required_fields:
      - "evidence_id"
      - "from_custodian"
      - "to_custodian"
      - "purpose"
      - "condition"
      - "location"
      - "timestamp"
      - "hash_verification"
      
    hash_verification:
      algorithms: ["MD5", "SHA256"]
      verify_on_transfer: true
      tolerance: 0
      
  storage:
    temperature_controlled: true
    humidity_controlled: true
    fire_suppression: true
    access_logging: true
    video_surveillance: true
```

### Timeline Analysis Configuration

```yaml
timeline_analysis:
  timezone_handling:
    default_timezone: "UTC"
    skew_tolerance_seconds: 30
    dst_aware: true
    
  sources:
    file_system:
      enabled: true
      parse_metadata: true
      parse_extended_attributes: true
      
    windows_event_logs:
      enabled: true
      log_channels:
        - "Security"
        - "System"
        - "Application"
        - "PowerShell"
        - "Sysmon"
        
    registry:
      enabled: true
      hives:
        - "SYSTEM"
        - "SOFTWARE"
        - "NTUSER.DAT"
        - "UsrClass.dat"
        
    browser_history:
      enabled: true
      browsers:
        - "Chrome"
        - "Firefox"
        - "Edge"
        - "Safari"
        
    prefetch:
      enabled: true
      parse_execution_count: true
      parse_last_run_time: true
      
  correlation:
    method: "event_based"
    time_window_seconds: 5
    entity_resolution: true
    
  filters:
    date_range: true
    keywords: true
    file_paths: true
    process_names: true
    network_addresses: true
```

## Architecture Patterns

### Evidence Processing Pipeline

```python
class EvidenceProcessingPipeline:
    def __init__(self, hash_verifier, parser_registry):
        self.hash_verifier = hash_verifier
        self.parsers = parser_registry
    
    async def process_evidence(self, evidence: Evidence) -> ProcessingResult:
        # Verify hash integrity
        hash_result = await self.hash_verifier.verify(evidence)
        if not hash_result.valid:
            raise IntegrityError(f"Hash mismatch: {evidence.evidence_id}")
        
        # Process with appropriate parser
        parser = self.parsers.get_parser(evidence.evidence_type)
        parsed_data = await parser.parse(evidence)
        
        # Index for search
        await self.index_data(parsed_data)
        
        return ProcessingResult(
            evidence_id=evidence.evidence_id,
            hash_verified=True,
            records_extracted=len(parsed_data.records),
            processing_time=parsed_data.processing_time,
        )
```

### Chain of Custody Manager

```python
class ChainOfCustodyManager:
    def __init__(self, blockchain_client, evidence_store):
        self.blockchain = blockchain_client
        self.evidence_store = evidence_store
    
    async def create_custody_record(self, evidence: Evidence) -> CustodyRecord:
        # Create initial custody record
        record = CustodyRecord(
            evidence_id=evidence.evidence_id,
            case_number=evidence.case_number,
            created_by=evidence.examiner,
            created_at=datetime.utcnow(),
            hash_md5=evidence.md5_hash,
            hash_sha256=evidence.sha256_hash,
        )
        
        # Store locally
        await self.evidence_store.store_record(record)
        
        # Anchor to blockchain
        tx_hash = await self.blockchain.anchor_record(record)
        record.blockchain_tx = tx_hash
        
        return record
    
    async def transfer_custody(
        self,
        evidence_id: str,
        from_custodian: str,
        to_custodian: str,
        purpose: str,
        condition: str,
    ) -> TransferRecord:
        # Verify current custody
        current = await self.evidence_store.get_current_custody(evidence_id)
        if current.custodian != from_custodian:
            raise CustodyError("Transferor is not current custodian")
        
        # Create transfer record
        transfer = TransferRecord(
            transfer_id=str(uuid.uuid4()),
            evidence_id=evidence_id,
            from_custodian=from_custodian,
            to_custodian=to_custodian,
            purpose=purpose,
            condition=condition,
            timestamp=datetime.utcnow(),
            hash_verified=True,
        )
        
        # Update custody
        await self.evidence_store.update_custody(evidence_id, to_custodian)
        
        # Anchor transfer
        tx_hash = await self.blockchain.anchor_transfer(transfer)
        transfer.blockchain_tx = tx_hash
        
        return transfer
```

### Timeline Correlation Engine

```python
class TimelineCorrelationEngine:
    def __init__(self, event_store, entity_resolver):
        self.event_store = event_store
        self.entity_resolver = entity_resolver
    
    async def correlate_events(
        self,
        case_number: str,
        time_range: Tuple[datetime, datetime],
        sources: List[str],
    ) -> CorrelatedTimeline:
        # Collect events from all sources
        all_events = []
        for source in sources:
            events = await self.event_store.get_events(
                case_number=case_number,
                source=source,
                time_range=time_range,
            )
            all_events.extend(events)
        
        # Resolve entities
        entities = await self.entity_resolver.resolve(all_events)
        
        # Correlate events
        correlated = self.correlate(all_events, entities)
        
        # Build timeline
        timeline = self.build_timeline(correlated)
        
        return CorrelatedTimeline(
            case_number=case_number,
            total_events=len(all_events),
            correlated_events=len(correlated),
            entities=entities,
            timeline=timeline,
        )
```

### Report Generation Engine

```python
class ForensicReportGenerator:
    def __init__(self, template_engine, evidence_catalog):
        self.templates = template_engine
        self.catalog = evidence_catalog
    
    async def generate_report(self, case_number: str) -> ForensicReport:
        # Get case data
        case_data = await self.get_case_data(case_number)
        
        # Get evidence catalog
        evidence = await self.catalog.get_evidence(case_number)
        
        # Generate sections
        sections = {
            "executive_summary": await self.generate_executive_summary(case_data),
            "methodology": await self.generate_methodology(case_data),
            "findings": await self.generate_findings(case_data, evidence),
            "evidence_catalog": await self.generate_evidence_catalog(evidence),
            "conclusions": await self.generate_conclusions(case_data),
            "examiner_qualifications": await self.generate_qualifications(case_data),
        }
        
        # Assemble report
        report = await self.templates.assemble(sections)
        
        return ForensicReport(
            case_number=case_number,
            report_id=str(uuid.uuid4()),
            sections=sections,
            generated_at=datetime.utcnow(),
            examiner=case_data.examiner,
        )
```

## Integration Guide

### Autopsy Integration

```python
class AutopsyIntegration:
    def __init__(self, autopsy_api_url: str):
        self.api_url = autopsy_api_url
    
    async def create_case(self, case_data: CaseData) -> AutopsyCase:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "case_name": case_data.case_number,
            "case_number": case_data.case_number,
            "examiner": case_data.examiner,
            "lab_name": case_data.lab,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/cases",
                headers=headers,
                json=payload,
            )
        
        return self.parse_case(response.json())
    
    async def add_evidence(self, case_id: str, evidence: Evidence) -> AutopsyEvidence:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "case_id": case_id,
            "name": evidence.evidence_id,
            "path": evidence.file_path,
            "type": evidence.evidence_type,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/cases/{case_id}/evidence",
                headers=headers,
                json=payload,
            )
        
        return self.parse_evidence(response.json())
```

### Volatility Integration

```python
class VolatilityIntegration:
    def __init__(self, volatility_path: str):
        self.volatility_path = volatility_path
    
    async def analyze_memory(self, memory_dump: str, profile: str) -> MemoryAnalysis:
        # Run Volatility plugins
        plugins = [
            "pslist",
            "pstree",
            "netscan",
            "filescan",
            "hashdump",
            "malfind",
        ]
        
        results = {}
        for plugin in plugins:
            result = await self.run_plugin(memory_dump, profile, plugin)
            results[plugin] = result
        
        return MemoryAnalysis(
            memory_dump=memory_dump,
            profile=profile,
            processes=results.get("pslist", []),
            network_connections=results.get("netscan", []),
            files=results.get("filescan", []),
            suspicious_processes=results.get("malfind", []),
        )
    
    async def run_plugin(self, memory_dump: str, profile: str, plugin: str) -> List[Dict]:
        cmd = [
            self.volatility_path,
            "-f", memory_dump,
            "--profile", profile,
            plugin,
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        return self.parse_output(stdout.decode())
```

### YARA Integration

```python
class YARAIntegration:
    def __init__(self, rules_path: str):
        self.rules_path = rules_path
        self.rules = self.load_rules()
    
    async def scan_file(self, file_path: str) -> YARAResult:
        matches = []
        
        for rule in self.rules:
            match = rule.match(file_path)
            if match:
                matches.append({
                    "rule": rule.identifier,
                    "meta": rule.meta,
                    "strings": match.strings,
                })
        
        return YARAResult(
            file_path=file_path,
            matches=matches,
            is_malicious=len(matches) > 0,
        )
    
    async def scan_directory(self, dir_path: str) -> List[YARAResult]:
        results = []
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                result = await self.scan_file(file_path)
                if result.is_malicious:
                    results.append(result)
        
        return results
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_evidence_case ON evidence (case_number, evidence_id);
CREATE INDEX idx_custody_evidence ON chain_of_custody (evidence_id, transfer_timestamp);
CREATE INDEX idx_timeline_case_source ON timeline_events (case_number, source, event_timestamp);

-- Create full-text search index
CREATE INDEX idx_evidence_description_search ON evidence USING gin(to_tsvector('english', description));

-- Partition timeline events by date
CREATE TABLE timeline_events (
    id UUID PRIMARY KEY,
    case_number VARCHAR(50),
    source VARCHAR(100),
    event_timestamp TIMESTAMP,
    event_data JSONB
) PARTITION BY RANGE (event_timestamp);
```

### Caching Strategy

```python
class ForensicsCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        cache_key = f"evidence:{evidence_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return Evidence.from_json(cached)
        return None
    
    async def cache_evidence(self, evidence_id: str, evidence: Evidence):
        cache_key = f"evidence:{evidence_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            evidence.to_json()
        )
```

### Batch Processing

```python
class ForensicsBatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
    
    async def process_batch(self, items: List, processor: Callable):
        batches = [
            items[i:i+self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                processor(item) for item in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Evidence Encryption

```python
from cryptography.fernet import Fernet

class EvidenceEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_evidence_metadata(self, data: str) -> str:
        """Encrypt sensitive evidence metadata"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_evidence_metadata(self, encrypted: str) -> str:
        """Decrypt sensitive evidence metadata"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class ForensicsAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            role_permissions = self.permissions.get(role, [])
            if action in role_permissions:
                return True
        return False
    
    def grant_role(self, user_id: str, role: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        self.roles[user_id].append(role)
```

### Audit Logging

```python
class ForensicsAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'action': event.action,
            'resource_id': event.resource_id,
            'details': event.details,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: Hash verification failure**
```python
async def diagnose_hash_failure(evidence_id: str):
    evidence = await get_evidence(evidence_id)
    current_hash = await calculate_hash(evidence.file_path)
    
    print(f"Evidence {evidence_id}:")
    print(f"  Original MD5: {evidence.md5_hash}")
    print(f"  Current MD5: {current_hash.md5}")
    print(f"  Original SHA256: {evidence.sha256_hash}")
    print(f"  Current SHA256: {current_hash.sha256}")
    
    if current_hash.md5 != evidence.md5_hash:
        print(f"  WARNING: Hash mismatch detected")
        print(f"  Possible causes:")
        print(f"    1. Evidence tampering")
        print(f"    2. File corruption")
        print(f"    3. Wrong file accessed")
        print(f"  Recommendation: Verify chain of custody")
```

**Issue: Timeline correlation gaps**
```python
async def diagnose_timeline_gaps(case_number: str):
    events = await get_timeline_events(case_number)
    
    # Sort by timestamp
    events.sort(key=lambda e: e.timestamp)
    
    # Find gaps
    gaps = []
    for i in range(1, len(events)):
        gap = (events[i].timestamp - events[i-1].timestamp).total_seconds()
        if gap > 3600:  # Gap > 1 hour
            gaps.append({
                'start': events[i-1].timestamp,
                'end': events[i].timestamp,
                'duration_hours': gap / 3600,
            })
    
    print(f"Timeline gaps for case {case_number}:")
    for gap in gaps:
        print(f"  {gap['start']} to {gap['end']}: {gap['duration_hours']:.1f} hours")
    
    if gaps:
        print(f"  Recommendation: Check for missing data sources")
```

**Issue: Memory analysis errors**
```python
async def diagnose_memory_analysis(memory_dump: str):
    # Check memory dump integrity
    file_size = os.path.getsize(memory_dump)
    print(f"Memory dump: {memory_dump}")
    print(f"  File size: {file_size / 1e9:.2f} GB")
    
    # Check profile compatibility
    profile = await detect_profile(memory_dump)
    print(f"  Detected profile: {profile}")
    
    if not profile:
        print(f"  WARNING: Could not detect profile")
        print(f"  Possible causes:")
        print(f"    1. Corrupted memory dump")
        print(f"    2. Unsupported OS version")
        print(f"  Recommendation: Try manual profile selection")
```

## API Reference

### Evidence Management API

```python
# Create evidence
POST /api/v1/evidence
Request:
{
    "case_number": "CASE-2026-0042",
    "evidence_type": "disk_image",
    "source": "\\\\FS-001\\PhysicalDrive0",
    "destination": "EVIDENCE/CASE-2026-0042/FS001.E01",
    "description": "Full disk image of affected workstation",
    "examiner": "Dr. Sarah Chen"
}

Response:
{
    "evidence_id": "EVD-001",
    "md5_hash": "abc123...",
    "sha256_hash": "def456...",
    "size_bytes": 500000000000,
    "status": "acquired"
}

# Get evidence
GET /api/v1/evidence/{evidence_id}
Response:
{
    "evidence_id": "EVD-001",
    "case_number": "CASE-2026-0042",
    "evidence_type": "disk_image",
    "md5_hash": "abc123...",
    "sha256_hash": "def456...",
    "custodian": "Forensic Lab",
    "status": "in_analysis"
}
```

### Chain of Custody API

```python
# Transfer custody
POST /api/v1/custody/transfer
Request:
{
    "evidence_id": "EVD-001",
    "from_custodian": "Crime Scene Team",
    "to_custodian": "Forensic Lab",
    "purpose": "Forensic Examination",
    "condition": "Sealed, tamper-evident bag intact"
}

Response:
{
    "transfer_id": "TRF-001",
    "timestamp": "2026-07-01T14:30:00Z",
    "hash_verified": true,
    "blockchain_tx": "0xabc123..."
}

# Get custody history
GET /api/v1/custody/{evidence_id}/history
Response:
{
    "evidence_id": "EVD-001",
    "transfers": [
        {
            "transfer_id": "TRF-001",
            "from_custodian": "Crime Scene Team",
            "to_custodian": "Forensic Lab",
            "timestamp": "2026-07-01T14:30:00Z"
        }
    ]
}
```

### Timeline Analysis API

```python
# Build timeline
POST /api/v1/timeline/build
Request:
{
    "case_number": "CASE-2026-0042",
    "sources": [
        {"type": "file_system", "path": "EVIDENCE/FS001.E01"},
        {"type": "windows_event_log", "path": "EVIDENCE/FS001_EventLogs/"}
    ],
    "time_range": {
        "start": "2026-06-28T00:00:00Z",
        "end": "2026-07-02T23:59:59Z"
    }
}

Response:
{
    "timeline_id": "TL-001",
    "total_events": 15000,
    "time_range": {
        "start": "2026-06-28T00:00:00Z",
        "end": "2026-07-02T23:59:59Z"
    }
}
```

## Data Models

### Evidence Model

```python
class Evidence:
    evidence_id: str
    case_number: str
    evidence_type: str
    source: str
    destination: str
    description: str
    examiner: str
    md5_hash: str
    sha256_hash: str
    size_bytes: int
    acquisition_date: datetime
    status: str  # acquired, in_analysis, archived
    write_blocker_used: bool
    metadata: Dict[str, Any]
```

### Chain of Custody Model

```python
class CustodyRecord:
    evidence_id: str
    case_number: str
    custodian: str
    created_by: str
    created_at: datetime
    hash_md5: str
    hash_sha256: str
    blockchain_tx: Optional[str]
    status: str  # active, transferred, archived
```

### Timeline Event Model

```python
class TimelineEvent:
    event_id: str
    case_number: str
    source: str
    event_timestamp: datetime
    event_type: str
    description: str
    details: Dict[str, Any]
    entities: List[str]
    created_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: digital-investigation-service
  namespace: forensics-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: digital-investigation-service
  template:
    metadata:
      labels:
        app: digital-investigation-service
    spec:
      containers:
      - name: digital-investigation
        image: your-registry/digital-investigation-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "1Gi"
            cpu: "1000m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Evidence metrics
evidence_counter = Counter(
    'forensics_evidence_total',
    'Total evidence items',
    ['case_number', 'evidence_type', 'status']
)

evidence_processing_duration = Histogram(
    'forensics_evidence_processing_duration_seconds',
    'Evidence processing duration',
    ['evidence_type'],
    buckets=[60, 300, 600, 1800, 3600]
)

# Chain of custody metrics
custody_transfers_counter = Counter(
    'forensics_custody_transfers_total',
    'Total custody transfers',
    ['case_number']
)

# Timeline metrics
timeline_events_counter = Counter(
    'forensics_timeline_events_total',
    'Total timeline events',
    ['case_number', 'source']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Digital Investigation",
    "panels": [
      {
        "title": "Evidence Processing",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(forensics_evidence_total[5m])",
            "legendFormat": "{{evidence_type}} - {{status}}"
          }
        ]
      },
      {
        "title": "Chain of Custody Transfers",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(forensics_custody_transfers_total[5m])",
            "legendFormat": "{{case_number}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: forensics_alerts
  rules:
  - alert: EvidenceProcessingBacklog
    expr: forensics_evidence_total{status="pending"} > 10
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Evidence processing backlog exceeds 10 items"
      
  - alert: HashVerificationFailure
    expr: rate(forensics_hash_verification_failures_total[5m]) > 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Hash verification failure detected"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestEvidenceCollection:
    def test_create_evidence(self, evidence_collector):
        evidence = evidence_collector.create_evidence(
            case_number="CASE-2026-0042",
            evidence_type="disk_image",
            source="/dev/sda1",
        )
        
        assert evidence.evidence_id is not None
        assert evidence.case_number == "CASE-2026-0042"
        assert evidence.md5_hash is not None
        assert evidence.sha256_hash is not None
    
    def test_verify_hash(self, hash_verifier):
        result = hash_verifier.verify(
            file_path="/path/to/evidence.E01",
            expected_md5="abc123...",
            expected_sha256="def456...",
        )
        
        assert result.valid == True
```

### Integration Tests

```python
class TestEndToEndInvestigation:
    async def test_investigation_flow(self, investigation_system):
        # Create case
        case = await investigation_system.create_case(
            case_number="CASE-2026-0042",
            description="Ransomware investigation",
        )
        
        assert case.case_number == "CASE-2026-0042"
        
        # Add evidence
        evidence = await investigation_system.add_evidence(
            case_number="CASE-2026-0042",
            evidence_type="disk_image",
            source="/dev/sda1",
        )
        
        assert evidence.evidence_id is not None
        
        # Transfer custody
        transfer = await investigation_system.transfer_custody(
            evidence_id=evidence.evidence_id,
            from_custodian="Crime Scene Team",
            to_custodian="Forensic Lab",
        )
        
        assert transfer.hash_verified == True
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class ForensicsUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def get_evidence(self):
        self.client.get(f"/api/v1/evidence/evidence-{self.evidence_counter}")
        self.evidence_counter += 1
    
    @task(5)
    def create_evidence(self):
        self.client.post("/api/v1/evidence", json={
            "case_number": "CASE-2026-0042",
            "evidence_type": "disk_image",
            "source": "/dev/sda1",
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/evidence", methods=["POST"])
@app.route("/api/v2/evidence", methods=["POST"])
async def create_evidence():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await create_evidence_v2()
    return await create_evidence_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **Chain of Custody**: Documentation of evidence handling from collection to presentation
- **Daubert Standard**: Legal standard for admissibility of expert testimony
- **E01**: Expert Witness Format - forensic image format
- **FTK**: Forensic Toolkit - forensic analysis software
- **Write Blocker**: Hardware/software preventing write operations to evidence
- **Volatility**: Memory forensics framework
- **YARA**: Pattern matching tool for malware identification
- **Timeline Analysis**: Correlation of events across multiple data sources
- **Forensic Imaging**: Bit-for-bit copy of digital media

## Changelog

### Version 2.0.0 (2026-07-01)
- Added blockchain-based chain of custody
- Implemented automated timeline correlation
- Enhanced YARA integration
- Added cloud evidence collection

### Version 1.5.0 (2026-01-15)
- Added memory analysis integration
- Implemented report generation
- Enhanced evidence management

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic evidence collection
- Chain of custody tracking

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def collect_evidence(
    case_number: str,
    evidence_type: str,
    source: str,
) -> Evidence:
    """Collect digital evidence.
    
    Args:
        case_number: Case identifier.
        evidence_type: Type of evidence.
        source: Evidence source.
    
    Returns:
        Collected evidence.
    
    Raises:
        CollectionError: If collection fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Digital Investigation Platform

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
