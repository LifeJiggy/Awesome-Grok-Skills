---
name: "forensic-analysis"
category: "hunting"
version: "2.0.0"
tags: ["hunting", "forensics", "digital-forensics", "incident-response", "evidence"]
description: "Digital forensic analysis for incident investigation and evidence collection"
---

# Forensic Analysis

## Overview

The Forensic Analysis module provides comprehensive digital forensic capabilities for incident investigation, evidence collection, and analysis. It supports the collection, preservation, examination, and presentation of digital evidence following forensic best practices. The module covers disk forensics, memory forensics, network forensics, and log analysis, enabling investigators to reconstruct attack timelines and establish chains of custody for legal proceedings.

## Core Capabilities

- **Evidence Collection**: Forensic acquisition of disk images, memory dumps, and network captures
- **Chain of Custody**: Maintain detailed evidence handling records for legal admissibility
- **Timeline Analysis**: Reconstruct event timelines from multiple data sources
- **Memory Forensics**: Analyze process memory, network connections, and injected code
- **Disk Forensics**: Examine file systems, recover deleted files, and analyze artifacts
- **Log Correlation**: Correlate logs across multiple systems for comprehensive investigation
- **Hash Verification**: Validate evidence integrity using cryptographic hashes
- **Report Generation**: Create detailed forensic reports for stakeholders

## Usage Examples

### Evidence Collection and Preservation

```python
from forensic_analysis import EvidenceCollector, EvidenceItem, ChainOfCustody

collector = EvidenceCollector(investigator="jsmith", case_id="IR-2024-042")

# Collect disk image
disk_evidence = collector.collect_disk_image(
    source="/dev/sda1",
    destination="/evidence/case-042/disk_image.E01",
    format="ewf",
    compression=True,
)

# Verify integrity
print(f"Disk Image Hash: {disk_evidence.sha256_hash}")
print(f"Collection Time: {disk_evidence.collected_at}")
print(f"Chain of Custody: {disk_evidence.chain_of_custody.current_custodian}")

# Collect memory dump
memory_evidence = collector.collect_memory_dump(
    target="10.0.1.100",
    output="/evidence/case-042/memory.dmp",
)

print(f"Memory Dump Size: {memory_evidence.size_bytes / 1024 / 1024:.1f} MB")
print(f"Memory Hash: {memory_evidence.md5_hash}")
```

### Timeline Analysis

```python
from forensic_analysis import TimelineAnalyzer, TimelineEvent

analyzer = TimelineAnalyzer()

# Add events from different sources
events = [
    TimelineEvent(timestamp="2024-01-15T08:30:00Z", source="auth_log",
                  description="Failed login attempt from 198.51.100.42", severity="medium"),
    TimelineEvent(timestamp="2024-01-15T08:31:00Z", source="auth_log",
                  description="Successful login from 198.51.100.42", severity="high"),
    TimelineEvent(timestamp="2024-01-15T08:45:00Z", source="process_log",
                  description="powershell.exe launched with encoded command", severity="high"),
    TimelineEvent(timestamp="2024-01-15T09:00:00Z", source="network_log",
                  description="Outbound connection to 203.0.113.50:443", severity="medium"),
]

for event in events:
    analyzer.add_event(event)

# Generate timeline
timeline = analyzer.generate_timeline()
print("Attack Timeline:")
for event in timeline:
    print(f"  [{event.timestamp}] {event.source}: {event.description}")
```

### Memory Analysis

```python
from forensic_analysis import MemoryAnalyzer, ProcessInfo

analyzer = MemoryAnalyzer()

# Analyze memory dump
results = analyzer.analyze("memory.dmp")

print("Memory Analysis Results:")
print(f"  Total Processes: {results.total_processes}")
print(f"  Suspicious Processes: {len(results.suspicious_processes)}")

for proc in results.suspicious_processes:
    print(f"\n  Suspicious Process: {proc.name} (PID {proc.pid})")
    print(f"    Parent: {proc.parent_name} (PID {proc.parent_pid})")
    print(f"    Risk Score: {proc.risk_score}")
    print(f"    Indicators: {proc.indicators}")

# Check for injected code
injections = analyzer.detect_code_injection(results)
print(f"\n  Code Injections Detected: {len(injections)}")
for inj in injections:
    print(f"    {inj.process_name}: {inj.injection_type} at {inj.address}")
```

### Log Correlation

```python
from forensic_analysis import LogCorrelator, LogSource

correlator = LogCorrelator()

# Add log sources
correlator.add_source(LogSource(
    name="auth_log",
    path="/var/log/auth.log",
    parser="syslog",
))

correlator.add_source(LogSource(
    name="web_log",
    path="/var/log/apache2/access.log",
    parser="apache",
))

# Correlate by time window
correlations = correlate(
    time_window_seconds=300,
    filters={"src_ip": "198.51.100.42"}
)

print(f"Correlated Events: {len(correlations)}")
for corr in correlations:
    print(f"  [{corr.timestamp}] {corr.source}: {corr.message}")
```

## Best Practices

- **Maintain Chain of Custody**: Document every person who handles evidence
- **Use Write Blockers**: Prevent accidental modification during acquisition
- **Verify Hashes**: Always verify evidence integrity before and after analysis
- **Work on Copies**: Never analyze original evidence; work on forensic copies
- **Document Everything**: Record all actions taken during the investigation
- **Use Forensic Tools**: Employ validated forensic tools with known good practices
- **Preserve Volatile Data**: Collect memory and network data before disk imaging
- **Follow Legal Requirements**: Ensure evidence collection meets jurisdictional requirements

## Advanced Forensic Workflows

### Automated Evidence Acquisition Pipeline

```python
from forensic_analysis import AcquisitionPipeline, AcquisitionTarget, EvidenceLocker

pipeline = AcquisitionPipeline(
    case_id="IR-2024-102",
    investigator="analyst-01",
    evidence_locker=EvidenceLocker(base_path="/evidence/IR-2024-102")
)

# Define targets for simultaneous acquisition
targets = [
    AcquisitionTarget(
        host="dc-01.corp.local",
        type="memory_dump",
        tool="winpmem",
        output_name="dc01_memory.dmp"
    ),
    AcquisitionTarget(
        host="dc-01.corp.local",
        type="disk_image",
        tool="ftkimager",
        source="C:",
        output_name="dc01_c_drive.E01"
    ),
    AcquisitionTarget(
        host="web-srv-01.corp.local",
        type="memory_dump",
        tool="linux_getram",
        output_name="websrv01_memory.lime"
    ),
    AcquisitionTarget(
        host="web-srv-01.corp.local",
        type="disk_image",
        tool="dc3dd",
        source="/dev/sda",
        output_name="websrv01_sda.E01"
    ),
    AcquisitionTarget(
        host="10.0.1.100",
        type="network_capture",
        tool="tcpdump",
        interface="eth0",
        duration_seconds=300,
        output_name="network_capture.pcap"
    ),
]

# Execute acquisitions in parallel with timeout
results = pipeline.acquire(
    targets=targets,
    max_parallel=3,
    timeout_per_target=600,
    verify_hash=True
)

print("Acquisition Results:")
for result in results:
    status = "SUCCESS" if result.success else "FAILED"
    print(f"  [{status}] {result.target.host} - {result.target.type}")
    if result.success:
        print(f"    Path: {result.output_path}")
        print(f"    Size: {result.size_bytes / (1024*1024):.1f} MB")
        print(f"    SHA256: {result.sha256}")
        print(f"    Duration: {result.duration_seconds:.1f}s")
    else:
        print(f"    Error: {result.error_message}")
```

### Volatile Data Collection Script

```python
from forensic_analysis import VolatileDataCollector, CollectionOrder

collector = VolatileDataCollector(
    target="10.0.1.100",
    target_os="windows",
    credentials=("admin", "password_hash")
)

# Follow proper volatile data collection order
collection_order = CollectionOrder(
    steps=[
        {"order": 1, "data_type": "process_list", "command": "tasklist /v /fo csv"},
        {"order": 2, "data_type": "network_connections", "command": "netstat -anob"},
        {"order": 3, "data_type": "open_files", "command": "openfiles /query /fo csv"},
        {"order": 4, "data_type": "loaded_modules", "command": "driverquery /v /fo csv"},
        {"order": 5, "data_type": "logged_on_users", "command": "query user"},
        {"order": 6, "data_type": "system_info", "command": "systeminfo /fo csv"},
        {"order": 7, "data_type": "arp_cache", "command": "arp -a"},
        {"order": 8, "data_type": "dns_cache", "command": "ipconfig /displaydns"},
        {"order": 9, "data_type": "route_table", "command": "route print"},
        {"order": 10, "data_type": "clipboard", "command": "powershell Get-Clipboard"},
        {"order": 11, "data_type": "environment_vars", "command": "set"},
        {"order": 12, "data_type": "scheduled_tasks", "command": "schtasks /query /fo csv /v"},
        {"order": 13, "data_type": "services", "command": "sc query type= all state= all"},
        {"order": 14, "data_type": "event_logs", "command": "wevtutil epl Security /q:'*[System[(EventID=4624 or EventID=4625)]]'"},
    ]
)

results = collector.collect_all(collection_order)

print("Volatile Data Collection Report:")
for result in results:
    print(f"  [{result.order}] {result.data_type}: {result.status}")
    print(f"    Output: {result.output_path}")
    print(f"    Size: {result.output_size_bytes} bytes")
    print(f"    Hash: {result.md5}")

# Package volatile evidence
volatile_evidence = collector.package(
    output_dir="/evidence/IR-2024-102/volatile/",
    include_metadata=True
)
print(f"\nVolatile evidence package: {volatile_evidence.package_path}")
```

## Memory Forensics Deep Dive

### Advanced Volatility Analysis

```python
from forensic_analysis import MemoryForensics, VolatilityProfile, AnalysisModule

mem = MemoryForensics(
    dump_path="/evidence/IR-2024-102/memory.dmp",
    profile=VolatilityProfile.WIN10X64_19041
)

# Run comprehensive analysis modules
modules = [
    AnalysisModule.PROCESS_LIST,          # pslist, psscan, pstree
    AnalysisModule.HANDLE_TABLE,          # handles
    AnalysisModule.NETWORK_CONNECTIONS,   # netscan, connections
    AnalysisModule.INJECTED_CODE,         # malfind
    AnalysisModule.DLL_LIST,              # ldrmodules, dlldlist
    AnalysisModule.REGISTRY_HIVES,        # hivelist, userassist
    AnalysisModule.MUTANT_SCANS,          # mutantscan
    AnalysisModule.DRIVERS,               # driverscan, modules
    AnalysisModule.FILE_SCAN,             # filescan, dumpfiles
    AnalysisModule.EVENT_LOGS,            # evtx
]

results = {}
for module in modules:
    print(f"Running {module.value}...")
    result = mem.run_module(module)
    results[module.value] = result
    print(f"  Found {result.item_count} items")

# Analyze suspicious process injection
print("\n--- Code Injection Analysis ---")
injections = results["injected_code"].items
for inj in injections:
    print(f"\n  Process: {inj.process_name} (PID {inj.pid})")
    print(f"    Address: 0x{inj.address:016x}")
    print(f"    Size: {inj.size_bytes} bytes")
    print(f"    Protection: {inj.protection}")
    print(f"    Entropy: {inj.entropy:.4f}")
    print(f"    Suspicious: {inj.is_suspicious}")
    if inj.is_suspicious:
        print(f"    Indicators: {inj.indicators}")
        # Dump the injected region for further analysis
        dump_path = mem.dump_region(inj.address, inj.size_bytes,
                                     output=f"/evidence/IR-2024-102/injected_{inj.pid}_{inj.address:x}.bin")
        print(f"    Dumped to: {dump_path}")
```

### Process Hollowing Detection

```python
from forensic_analysis import ProcessHollowingDetector, MemoryRegion

detector = ProcessHollowingDetector(mem)

# Check for process hollowing indicators
hollowed_procs = detector.scan(
    checks=[
        "header_mismatch",      # PE header on disk vs memory
        "unmapped_sections",    # Sections in memory not on disk
        "suspended_threads",    # Threads in START_SUSPENDED state
        "section_permissions",  # RWX sections in non-image memory
        "parent_anomaly",       # Parent process doesn't match expected
    ]
)

print(f"Process Hollowing Scan Results:")
print(f"  Processes scanned: {detector.process_count}")
print(f"  Potential hollowing detected: {len(hollowed_procs)}")

for proc in hollowed_procs:
    print(f"\n  SUSPECT: {proc.process_name} (PID {proc.pid})")
    print(f"    Image on disk: {proc.image_path}")
    print(f"    Image base (memory): 0x{proc.memory_base:016x}")
    print(f"    Image size (disk): {proc.disk_image_size} bytes")
    print(f"    Image size (memory): {proc.memory_image_size} bytes")
    print(f"    Size mismatch: {proc.size_mismatch}")
    print(f"    Suspended threads: {proc.suspended_thread_count}")
    print(f"    Section anomalies: {proc.section_anomalies}")
    print(f"    Risk Score: {proc.risk_score:.2f}")

    # Extract and analyze the hollowed process
    proc_dump = detector.extract_process(proc.pid)
    print(f"    Process dump: {proc_dump.output_path}")
    print(f"    Dump SHA256: {proc_dump.sha256}")
```

### Rootkit Detection in Memory

```python
from forensic_analysis import RootkitDetector, DetectionTechnique

detector = RootkitDetector(mem)

# Multi-technique rootkit detection
techniques = [
    DetectionTechnique.IDT_HOOK,           # Interrupt Descriptor Table hooks
    DetectionTechnique.SSDT_HOOK,          # System Service Descriptor Table hooks
    DetectionTechnique.IAT_HOOK,           # Import Address Table hooks
    DetectionTechnique.DIRECT_KERNEL,      # Direct kernel object manipulation
    DetectionTechnique.HIDDEN_PROCESSES,   # Processes hidden from API
    DetectionTechnique.HIDDEN_FILES,       # Files hidden from API
    DetectionTechnique.HIDDEN_REGISTRY,    # Registry keys hidden from API
    DetectionTechnique.KMOD_ANALYSIS,      # Kernel module integrity
    DetectionTechnique.DPC_TIMERS,         # Deferred Procedure Call analysis
    DetectionTechnique.ETW_PATCHING,       # Event Tracing for Windows patching
]

results = detector.scan(techniques=techniques)

print("Rootkit Detection Results:")
for technique, result in results.items():
    status = "CLEAN" if not result.detected else "DETECTED"
    print(f"\n  {technique.value}: {status}")
    if result.detected:
        print(f"    Confidence: {result.confidence:.1%}")
        print(f"    Details: {result.details}")
        print(f"    Affected items: {result.affected_count}")
        for item in result.affected_items[:5]:
            print(f"      - {item}")
```

## Disk Forensics Deep Dive

### File System Timeline Reconstruction

```python
from forensic_analysis import FileSystemForensics, TimelineBuilder, TimestampSource

forensics = FileSystemForensics(
    image_path="/evidence/IR-2024-102/disk_image.E01",
    file_system_type="NTFS"
)

# Build comprehensive timeline from multiple timestamp sources
builder = TimelineBuilder(forensics)

timeline = builder.build(
    timestamp_sources=[
        TimestampSource.MFT,              # Master File Table timestamps
        TimestampSource.UsnJrnl,          # USN Change Journal
        TimestampSource.$LogFile,         # NTFS Log File
        TimestampSource.ShortcutFiles,    # .lnk files
        TimestampSource.JumpLists,        # Jump list entries
        TimestampSource.Amcache,          # Amcache.hve
        TimestampSource.SRUM,             # System Resource Usage Monitor
        TimestampSource.BrowserHistory,   # Web browser history
        TimestampSource.RecycleBin,       # $Recycle.Bin
        TimestampSource.Shellbags,        # Shellbag artifacts
    ],
    time_range=("2024-01-10T00:00:00Z", "2024-01-20T23:59:59Z")
)

print(f"Timeline Analysis Results:")
print(f"  Total events: {len(timeline.events):,}")
print(f"  Unique timestamps: {len(timeline.unique_timestamps):,}")
print(f"  Time range: {timeline.start_time} to {timeline.end_time}")

# Filter for suspicious activity
suspicious = timeline.filter(
    criteria={
        "exclude_known_good": True,
        "file_extensions": [".exe", ".dll", ".bat", ".ps1", ".vbs", ".js"],
        "min_timestamp_entropy": 0.7,  # Unusual timestamp patterns
    }
)

print(f"\n  Suspicious events: {len(suspicious.events):,}")
for event in suspicious.events[:20]:
    print(f"    [{event.timestamp}] {event.action}: {event.path}")
    print(f"      Source: {event.source}, MFT Entry: {event.mft_entry}")
```

### Deleted File Recovery

```python
from forensic_analysis import DeletedFileRecovery, RecoveryTechnique

recovery = DeletedFileRecovery(forensics)

# Multi-technique deleted file recovery
techniques = [
    RecoveryTechnique.MFT_ANALYSIS,       # Scan MFT for deleted entries
    RecoveryTechnique.USRNJOURNAL,        # Parse USN Journal for deletions
    RecoveryTechnique.UNALLOCATED_SPACE,  # Carve unallocated space
    RecoveryTechnique.$LOGFILE,           # Parse NTFS log for deleted file refs
    RecoveryTechnique.SHADOW_COPIES,      # Access Volume Shadow Copies
]

results = recovery.recover(techniques=techniques)

print("Deleted File Recovery Results:")
print(f"  Total deleted files found: {results.total_deleted}")
print(f"  Recoverable files: {results.recoverable_count}")
print(f"  Recovery techniques used: {len(results.technique_results)}")

for technique_result in results.technique_results:
    print(f"\n  {technique_result.technique.value}:")
    print(f"    Files found: {technique_result.files_found}")
    print(f"    Successfully recovered: {technique_result.recovered}")

# List recoverable files with details
for file in results.recoverable_files[:30]:
    recover_status = "FULL" if file.full_recovery_possible else "PARTIAL"
    print(f"\n    {file.original_path}")
    print(f"      Deleted: {file.deletion_timestamp}")
    print(f"      Size: {file.size_bytes} bytes")
    print(f"      Recovery: {recover_status}")
    print(f"      Confidence: {file.recovery_confidence:.1%}")

    if file.full_recovery_possible:
        output_path = recovery.extract_file(
            file,
            output=f"/evidence/IR-2024-102/recovered/{file.safe_filename}"
        )
        print(f"      Extracted to: {output_path}")
```

### Registry Forensics

```python
from forensic_analysis import RegistryForensics, RegistryHive, AnalysisTarget

reg = RegistryForensics(
    image_path="/evidence/IR-2024-102/disk_image.E01"
)

# Analyze multiple registry hives
hives = [
    RegistryHive(path="Windows/System32/config/SYSTEM", name="SYSTEM"),
    RegistryHive(path="Windows/System32/config/SOFTWARE", name="SOFTWARE"),
    RegistryHive(path="Windows/System32/config/SECURITY", name="SECURITY"),
    RegistryHive(path="Windows/System32/config/SAM", name="SAM"),
    RegistryHive(path="Users/jsmith/NTUSER.DAT", name="NTUSER-jsmith"),
    RegistryHive(path="Users/jsmith/AppData/Local/Microsoft/Windows/UsrClass.dat", name="USRCLASS-jsmith"),
]

analysis_targets = [
    AnalysisTarget.RUN_KEYS,              # Autostart locations
    AnalysisTarget.SERVICES,              # Service configurations
    AnalysisTarget.NETWORK_PROFILES,      # Wi-Fi and network history
    AnalysisTarget.USERASSIST,            # UserAssist execution records
    AnalysisTarget.MRU_LISTS,             # Most Recently Used lists
    AnalysisTarget.SHELLBAGS,             # Shell folder access
    AnalysisTarget.SHIMCACHE,             # Application compatibility cache
    AnalysisTarget.AMCACHE,              # Amcache execution records
    AnalysisTarget.BAM,                   # Background Activity Moderator
    AnalysisTarget.LEAKED_CREDENTIALS,    # Credential artifacts
    AnalysisTarget.PERSISTENCE,           # Persistence mechanisms
    AnalysisTarget.INSTALLATION_HISTORY,  # Software installation records
]

results = {}
for hive in hives:
    print(f"\nAnalyzing {hive.name}...")
    hive_results = reg.analyze_hive(hive, targets=analysis_targets)
    results[hive.name] = hive_results

    for target, data in hive_results.items():
        if data.items:
            print(f"  {target.value}: {len(data.items)} entries")

# Focus on persistence mechanisms
print("\n=== Persistence Mechanisms Found ===")
for hive_name, hive_results in results.items():
    persistence = hive_results.get(AnalysisTarget.PERSISTENCE)
    if persistence and persistence.items:
        print(f"\n  In {hive_name}:")
        for item in persistence.items:
            print(f"    Type: {item.persistence_type}")
            print(f"    Key: {item.registry_key}")
            print(f"    Value: {item.value_name}")
            print(f"    Data: {item.value_data[:100]}")
            print(f"    Risk: {item.risk_assessment}")

# Analyze UserAssist for execution evidence
print("\n=== UserAssist Execution Records ===")
for hive_name, hive_results in results.items():
    userassist = hive_results.get(AnalysisTarget.USERASSIST)
    if userassist and userassist.items:
        print(f"\n  {hive_name}:")
        for record in userassist.items[:20]:
            print(f"    Path: {record.decoded_path}")
            print(f"    Runs: {record.run_count}")
            print(f"    Focus Time: {record.focus_time}")
            print(f"    Last Run: {record.last_run}")
```

## Network Forensics

### PCAP Analysis and Protocol Extraction

```python
from forensic_analysis import NetworkForensics, ProtocolAnalyzer, ExtractionTarget

netforensics = NetworkForensics(
    pcap_path="/evidence/IR-2024-102/network_capture.pcap"
)

# Protocol-level analysis
analyzer = ProtocolAnalyzer(netforensics)

protocols_detected = analyzer.identify_protocols()
print("Protocols Detected:")
for proto, count in protocols_detected.items():
    print(f"  {proto}: {count} packets")

# Extract specific data from network capture
extractions = [
    ExtractionTarget(type="dns_queries", output="dns_queries.json"),
    ExtractionTarget(type="http_requests", output="http_requests.json"),
    ExtractionTarget(type="http_responses", output="http_responses.json"),
    ExtractionTarget(type="tls_handshakes", output="tls_handshakes.json"),
    ExtractionTarget(type="smtp_messages", output="smtp_messages.json"),
    ExtractionTarget(type="ftp_commands", output="ftp_commands.json"),
    ExtractionTarget(type="smb_files", output="smb_transfers.json"),
    ExtractionTarget(type="dns_tunneling", output="dns_tunnel_suspects.json"),
    ExtractionTarget(type="beaconing", output="beaconing_analysis.json"),
]

results = analyzer.extract(extractions)

print("\nNetwork Data Extraction Results:")
for result in results:
    print(f"  {result.type}: {result.item_count} items -> {result.output_path}")

# Analyze DNS for C2 beaconing
dns_results = results[4]  # dns_tunnel_suspects
print(f"\n--- DNS Tunneling / Beaconing Analysis ---")
for suspect in dns_results.items:
    print(f"\n  Domain: {suspect.domain}")
    print(f"    Query count: {suspect.query_count}")
    print(f"    Avg query length: {suspect.avg_query_length:.1f} chars")
    print(f"    Entropy: {suspect.entropy:.4f}")
    print(f"    Regularity: {suspect.regularity_score:.4f}")
    print(f"    Suspicion: {suspect.suspicion_level}")
```

### Network Flow Reconstruction

```python
from forensic_analysis import FlowReconstruction, Conversation, DataDirection

reconstructor = FlowReconstruction(netforensics)

# Reconstruct full conversations
conversations = reconstructor.reconstruct(
    filter_criteria={
        "min_bytes": 10240,
        "include_dns": True,
        "include_http": True,
        "include_tls": True,
    }
)

print(f"Reconstructed Conversations: {len(conversations)}")

for conv in conversations[:15]:
    print(f"\n  Conversation: {conv.src_ip}:{conv.src_port} <-> "
          f"{conv.dst_ip}:{conv.dst_port}")
    print(f"    Protocol: {conv.protocol}")
    print(f"    Duration: {conv.duration_seconds:.1f}s")
    print(f"    Bytes sent: {conv.bytes_out}")
    print(f"    Bytes received: {conv.bytes_in}")
    print(f"    Packets: {conv.packet_count}")

    # Extract data payloads
    for direction in [DataDirection.OUTBOUND, DataDirection.INBOUND]:
        payload = conv.get_payload(direction, max_bytes=4096)
        if payload:
            print(f"    {direction.value} payload ({len(payload)} bytes):")
            print(f"      Hex preview: {payload[:64].hex()}")
            print(f"      ASCII preview: {payload[:64].decode('ascii', errors='replace')}")
```

## Timeline Analysis

### Super Timeline Creation

```python
from forensic_analysis import SuperTimeline, TimelineSource, EventFilter

timeline = SuperTimeline(case_id="IR-2024-102")

# Add evidence sources
timeline.add_source(TimelineSource(
    type="memory_dump",
    path="/evidence/IR-2024-102/memory.dmp",
    parser="volatility",
    modules=["pslist", "netscan", "malfind", "hivelist"]
))

timeline.add_source(TimelineSource(
    type="disk_image",
    path="/evidence/IR-2024-102/disk_image.E01",
    parser="plaso",
    parsers=["filestat", "mft", "usnjrnl", "lnk", "shellbags",
             "amcache", "userassist", "prefetch", "evtx"]
))

timeline.add_source(TimelineSource(
    type="event_logs",
    path="/evidence/IR-2024-102/event_logs/",
    parser="evtx",
    log_names=["Security", "System", "Application", "Microsoft-Windows-Sysmon"]
))

timeline.add_source(TimelineSource(
    type="network_capture",
    path="/evidence/IR-2024-102/network_capture.pcap",
    parser="parsing",
    protocols=["dns", "http", "tls"]
))

# Build the super timeline
print("Building super timeline...")
result = timeline.build(
    time_range=("2024-01-14T00:00:00Z", "2024-01-16T23:59:59Z"),
    output_format="csv",
    output_path="/evidence/IR-2024-102/super_timeline.csv"
)

print(f"Super Timeline Results:")
print(f"  Total events: {result.total_events:,}")
print(f"  Sources processed: {result.sources_processed}")
print(f"  Time range: {result.start_time} to {result.end_time}")
print(f"  Output: {result.output_path}")

# Apply filters for analysis
filters = [
    EventFilter(field="source_type", operator="in",
                value=["process_creation", "network_connection", "file_modification"]),
    EventFilter(field="timestamp", operator="between",
                value=["2024-01-15T00:00:00Z", "2024-01-15T12:00:00Z"]),
    EventFilter(field="hostname", operator="equals", value="dc-01"),
]

filtered = timeline.query(filters)
print(f"\nFiltered events: {len(filtered):,}")

# Group by activity type
from collections import Counter
activity_counts = Counter(e.event_type for e in filtered)
print("\nActivity Distribution:")
for activity, count in activity_counts.most_common(20):
    print(f"  {activity}: {count:,}")
```

### Cuckoo Timeline Correlation

```python
from forensic_analysis import CuckooTimelineCorrelation, CorrelationKey

correlator = CuckooTimelineCorrelation()

# Define correlation keys across evidence sources
correlation_keys = [
    CorrelationKey(name="user_activity", fields=["username", "hostname"]),
    CorrelationKey(name="network_activity", fields=["src_ip", "dst_ip"]),
    CorrelationKey(name="process_activity", fields=["process_name", "pid"]),
    CorrelationKey(name="file_activity", fields=["file_path"]),
]

# Load timeline data from different sources
correlator.load_timeline("auth_logs", auth_timeline, correlation_keys)
correlator.load_timeline("process_logs", process_timeline, correlation_keys)
correlator.load_timeline("network_logs", network_timeline, correlation_keys)
correlator.load_timeline("file_logs", file_timeline, correlation_keys)

# Perform correlation
correlations = correlator.correlate(
    time_window_seconds=300,
    min_correlation_score=0.6
)

print(f"Correlation Results:")
print(f"  Total correlated events: {len(correlations)}")
print(f"  Unique correlation chains: {len(set(c.chain_id for c in correlations))}")

# Reconstruct attack chains
chains = correlator.reconstruct_chains(correlations)
for chain in chains:
    print(f"\n  Attack Chain: {chain.chain_id}")
    print(f"    Duration: {chain.duration_seconds:.0f}s")
    print(f"    Stages: {chain.stage_count}")
    print(f"    Confidence: {chain.confidence:.1%}")
    print(f"    MITRE Mapping: {[t.technique_id for t in chain.mitre_techniques]}")
    print(f"    Steps:")
    for step in chain.steps:
        print(f"      [{step.timestamp}] {step.source}: {step.description}")
```

## Database Schema for Forensic Evidence

```sql
-- Cases table
CREATE TABLE forensic_cases (
    case_id         VARCHAR(64) PRIMARY KEY,
    title           VARCHAR(512) NOT NULL,
    severity        ENUM('info', 'low', 'medium', 'high', 'critical') NOT NULL,
    status          ENUM('open', 'investigating', 'resolved', 'closed') DEFAULT 'open',
    lead_investigator VARCHAR(128),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    description     TEXT,
    INDEX idx_status (status),
    INDEX idx_severity (severity)
);

-- Evidence items
CREATE TABLE evidence_items (
    evidence_id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    case_id             VARCHAR(64) NOT NULL,
    evidence_type       ENUM('disk_image', 'memory_dump', 'network_capture',
                             'log_archive', 'volatile_data', 'screenshot',
                             'document', 'other') NOT NULL,
    source_host         VARCHAR(256),
    source_path         VARCHAR(1024),
    output_path         VARCHAR(1024) NOT NULL,
    file_format         VARCHAR(32),
    size_bytes          BIGINT,
    md5_hash            VARCHAR(32),
    sha256_hash         VARCHAR(64),
    collected_by        VARCHAR(128) NOT NULL,
    collected_at        TIMESTAMP NOT NULL,
    acquisition_tool    VARCHAR(128),
    write_blocker_used  BOOLEAN DEFAULT FALSE,
    notes               TEXT,
    FOREIGN KEY (case_id) REFERENCES forensic_cases(case_id),
    INDEX idx_case (case_id),
    INDEX idx_type (evidence_type),
    INDEX idx_host (source_host)
);

-- Chain of custody
CREATE TABLE chain_of_custody (
    custody_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    evidence_id     BIGINT NOT NULL,
    custodian       VARCHAR(128) NOT NULL,
    action          ENUM('acquired', 'transferred', 'analyzed', 'copied',
                         'exported', 'archived', 'destroyed') NOT NULL,
    action_timestamp TIMESTAMP NOT NULL,
    location        VARCHAR(256),
    notes           TEXT,
    witness         VARCHAR(128),
    FOREIGN KEY (evidence_id) REFERENCES evidence_items(evidence_id),
    INDEX idx_evidence (evidence_id),
    INDEX idx_timestamp (action_timestamp)
);

-- Timeline events
CREATE TABLE timeline_events (
    event_id        BIGINT AUTO_INCREMENT PRIMARY KEY,
    case_id         VARCHAR(64) NOT NULL,
    event_timestamp TIMESTAMP(6) NOT NULL,
    event_type      VARCHAR(128) NOT NULL,
    source          VARCHAR(128) NOT NULL,
    description     TEXT,
    hostname        VARCHAR(256),
    username        VARCHAR(128),
    source_path     VARCHAR(1024),
    evidence_id     BIGINT,
    data_json       JSON,
    FOREIGN KEY (case_id) REFERENCES forensic_cases(case_id),
    FOREIGN KEY (evidence_id) REFERENCES evidence_items(evidence_id),
    INDEX idx_case (case_id),
    INDEX idx_timestamp (event_timestamp),
    INDEX idx_type (event_type),
    INDEX idx_host (hostname),
    INDEX idx_user (username),
    FULLTEXT INDEX idx_description (description)
);

-- Analysis results
CREATE TABLE analysis_results (
    result_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    case_id         VARCHAR(64) NOT NULL,
    evidence_id     BIGINT,
    analysis_type   VARCHAR(128) NOT NULL,
    tool_name       VARCHAR(128),
    tool_version    VARCHAR(64),
    findings        JSON NOT NULL,
    risk_score      DOUBLE,
    analyst_notes   TEXT,
    completed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES forensic_cases(case_id),
    FOREIGN KEY (evidence_id) REFERENCES evidence_items(evidence_id),
    INDEX idx_case (case_id),
    INDEX idx_analysis_type (analysis_type)
);

-- IOCs extracted during forensics
CREATE TABLE forensic_iocs (
    ioc_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    case_id         VARCHAR(64) NOT NULL,
    ioc_type        ENUM('ip', 'domain', 'url', 'hash_md5', 'hash_sha1',
                         'hash_sha256', 'email', 'file_name', 'mutex',
                         'registry_key', 'cron_job', 'certificate') NOT NULL,
    ioc_value       VARCHAR(2048) NOT NULL,
    confidence      DOUBLE,
    context         TEXT,
    extracted_from  VARCHAR(128),
    evidence_id     BIGINT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES forensic_cases(case_id),
    FOREIGN KEY (evidence_id) REFERENCES evidence_items(evidence_id),
    INDEX idx_case (case_id),
    INDEX idx_type_value (ioc_type, ioc_value(255)),
    INDEX idx_confidence (confidence DESC)
);

-- Reports generated
CREATE TABLE forensic_reports (
    report_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    case_id         VARCHAR(64) NOT NULL,
    report_type     ENUM('preliminary', 'interim', 'final', 'ioc_share',
                         'executive_summary', 'technical_detail') NOT NULL,
    format          ENUM('markdown', 'html', 'pdf', 'docx') NOT NULL,
    output_path     VARCHAR(1024) NOT NULL,
    generated_by    VARCHAR(128),
    generated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    classification  ENUM('TLP:WHITE', 'TLP:GREEN', 'TLP:AMBER', 'TLP:RED') DEFAULT 'TLP:WHITE',
    FOREIGN KEY (case_id) REFERENCES forensic_cases(case_id),
    INDEX idx_case (case_id)
);
```

## Integration Patterns

### Forensic Tool Integration (Autopsy, SIFT, KAPE)

```python
from forensic_analysis import ToolIntegration, ForensicSuite, ToolConfig

# Autopsy integration
autopsy = ToolIntegration(
    suite=ForensicSuite.AUTOPSY,
    config=ToolConfig(
        install_path="/opt/autopsy",
        python_api="autopsy-api",
        case_database="/cases/IR-2024-102/autopsy.db"
    )
)

# Import evidence into Autopsy case
autopsy.import_evidence(
    case_name="IR-2024-102",
    evidence_items=[
        {"path": "/evidence/IR-2024-102/disk_image.E01", "type": "disk_image"},
        {"path": "/evidence/IR-2024-102/memory.dmp", "type": "memory_dump"},
    ]
)

# Run ingest modules
ingest_modules = [
    "hash_lookup",           # Known file hash lookup (NSRL, custom)
    "file_type_identifier",  # File type identification
    "keyword_search",        # Keyword searching
    "email_parser",          # Email artifact extraction
    "web_artifact_extractor",# Browser artifact extraction
    "recent_activity",       # Recent activity extraction
    "registry_analyzer",     # Registry analysis
    "picture_analyzer",      # Picture analysis
    "video_analyzer",        # Video analysis
    "extension_mismatch",    # Extension mismatch detection
]

results = autopsy.run_ingest_modules(ingest_modules)
print("Autopsy Ingest Module Results:")
for module, result in results.items():
    print(f"  {module}: {result.artifacts_found} artifacts found")

# Export results
export = autopsy.export_results(
    output_path="/evidence/IR-2024-102/autopsy_export/",
    export_format="csv"
)
print(f"Exported {export.total_artifacts} artifacts")
```

### Volatility Workbench Integration

```python
from forensic_analysis import VolatilityWorkbench, WorkbenchSession

workbench = VolatilityWorkbench(
    server_url="http://localhost:8000",
    api_key="your-api-key"
)

session = workbench.create_session(
    case_id="IR-2024-102",
    memory_dump="/evidence/IR-2024-102/memory.dmp",
    profile="Win10x64_19041"
)

# Run automated analysis
analysis = session.run_full_analysis(
    modules=[
        "windows.pslist", "windows.pstree", "windows.psscan",
        "windows.netscan", "windows.netstat",
        "windows.malfind", "windows.dlllist",
        "windows.handles", "windows.cmdline",
        "windows.filescan", "windows.dumpfiles",
        "windows.registry.hivelist", "windows.registry.userassist",
        "windows.registry.samdump", "windows.mutantscan",
    ],
    parallel=True,
    timeout_per_module=300
)

print("Volatility Workbench Analysis Complete:")
for module, results in analysis.items():
    print(f"  {module}: {results.item_count} results")
    if results.suspicious_count > 0:
        print(f"    Suspicious: {results.suspicious_count}")
```

## Performance Tuning Guide

### Evidence Processing Optimization

```python
from forensic_analysis import ProcessingConfig, PerformanceTuner

config = ProcessingConfig(
    # Parallelism
    max_workers=8,
    io_threads=4,
    analysis_threads=8,

    # Memory management
    max_memory_mb=8192,
    chunk_size_mb=256,
    streaming_mode=True,

    # Disk I/O
    read_ahead_mb=64,
    write_buffer_mb=32,
    use_direct_io=True,

    # Hashing
    hash_algorithm="sha256",
    hash_threads=4,
    use_gpu_hashing=True,

    # Compression
    compression_level=6,
    compression_algorithm="lz4"
)

tuner = PerformanceTuner(config)

# Benchmark evidence processing
benchmark = tuner.benchmark(
    test_image="/test_data/sample.E01",
    test_memory="/test_data/sample.dmp"
)

print("Processing Performance Benchmark:")
print(f"  Disk image read speed: {benchmark.disk_read_mbps:.1f} MB/s")
print(f"  Memory dump parse speed: {benchmark.memory_parse_mbps:.1f} MB/s")
print(f"  Hash computation speed: {benchmark.hash_speed_mbps:.1f} MB/s")
print(f"  Timeline generation: {benchmark.timeline_events_per_second:.0f} events/s")
print(f"  Peak memory usage: {benchmark.peak_memory_mb:.1f} MB")
print(f"  Total processing time: {benchmark.total_seconds:.1f}s")
```

### Scalable Evidence Storage

```python
from forensic_analysis import EvidenceStorage, StorageTier, RetentionPolicy

storage = EvidenceStorage(
    base_path="/evidence",
    tiers=[
        StorageTier(
            name="hot",
            path="/evidence/hot",
            max_size_gb=1000,
            retention_days=90,
            description="Active investigation evidence"
        ),
        StorageTier(
            name="warm",
            path="/evidence/warm",
            max_size_gb=5000,
            retention_days=365,
            description="Recently closed cases"
        ),
        StorageTier(
            name="cold",
            path="/evidence/cold",
            max_size_gb=50000,
            retention_days=2555,  # 7 years
            description="Archived cases for legal compliance"
        ),
    ],
    retention_policy=RetentionPolicy(
        auto_move_after_days=90,
        auto_archive_after_days=365,
        auto_delete_after_days=2555,
        legal_hold_exempt=True,
        encrypt_at_rest=True
    )
)

# Storage status
status = storage.get_status()
print("Evidence Storage Status:")
for tier in status.tiers:
    print(f"  {tier.name}: {tier.used_gb:.1f} / {tier.max_gb:.1f} GB "
          f"({tier.usage_percent:.1f}%)")
    print(f"    Items: {tier.item_count}")
    print(f"    Oldest: {tier.oldest_item}")
    print(f"    Newest: {tier.newest_item}")
```

## Reporting Templates

### Forensic Investigation Report

```python
from forensic_analysis import ForensicReport, ReportSection, FindingSeverity

report = ForensicReport(
    case_id="IR-2024-102",
    title="Forensic Investigation Report - Compromised Domain Controller",
    classification="TLP:AMBER",
    lead_investigator="analyst-01",
    date_range=("2024-01-15", "2024-01-20")
)

report.add_section(ReportSection(
    heading="Executive Summary",
    content="""
        This report presents findings from the forensic investigation of a compromised
        domain controller (dc-01.corp.local) following initial detection on 2024-01-15.
        Evidence collection included memory acquisition, disk imaging, and network
        capture. The investigation determined that an attacker gained initial access
        via compromised VPN credentials, established persistence through a scheduled
        task, and performed lateral movement to the domain controller using Pass-the-Hash.
    """
))

report.add_section(ReportSection(
    heading="Evidence Collected",
    template="evidence_table",
    evidence=[
        {"type": "Memory Dump", "host": "dc-01", "hash": "a1b2c3...", "size": "8 GB"},
        {"type": "Disk Image", "host": "dc-01", "hash": "d4e5f6...", "size": "200 GB"},
        {"type": "Network Capture", "host": "tap-01", "hash": "g7h8i9...", "size": "2 GB"},
        {"type": "Event Logs", "host": "dc-01", "hash": "j0k1l2...", "size": "500 MB"},
    ]
))

report.add_section(ReportSection(
    heading="Key Findings",
    template="findings_table",
    findings=[
        {"severity": "critical", "finding": "Attacker established Golden Ticket using krbtgt hash"},
        {"severity": "high", "finding": "Scheduled task created for persistence (every 6 hours)"},
        {"severity": "high", "finding": "Mimikatz artifacts found in process memory"},
        {"severity": "medium", "finding": "Suspicious PowerShell scripts in temp directory"},
        {"severity": "medium", "finding": "Anomalous LDAP queries for sensitive group enumeration"},
    ]
))

report.add_section(ReportSection(
    heading="Timeline of Compromise",
    template="timeline",
    events=[
        {"time": "2024-01-12 22:00", "event": "VPN login from unusual IP"},
        {"time": "2024-01-13 03:15", "event": "Credential harvesting via Mimikatz"},
        {"time": "2024-01-14 14:00", "event": "Lateral movement to dc-01"},
        {"time": "2024-01-14 14:30", "event": "krbtgt hash extraction"},
        {"time": "2024-01-14 15:00", "event": "Golden Ticket creation"},
        {"time": "2024-01-15 02:00", "event": "Data exfiltration begins"},
        {"time": "2024-01-15 08:00", "event": "Anomaly detected by SOC"},
    ]
))

report.add_section(ReportSection(
    heading="Recommendations",
    content="""
        1. Reset krbtgt password (twice, 12 hours apart)
        2. Reset all domain admin credentials
        3. Implement Privileged Access Workstations (PAW)
        4. Deploy Credential Guard on all domain controllers
        5. Enable Windows Advanced Audit Policy for credential validation
        6. Implement network segmentation for domain controllers
        7. Deploy Endpoint Detection and Response (EDR) on DCs
        8. Review and harden VPN authentication (certificate-based MFA)
    """
))

report.export(
    output_path="/evidence/IR-2024-102/reports/",
    formats=["pdf", "html", "markdown"]
)
print(f"Report exported: {report.output_path}")
```

## Architecture

```
+================================================================+
|                  FORENSIC ANALYSIS ARCHITECTURE                  |
+================================================================+

+---------------------+     +---------------------+     +---------------------+
|   ACQUISITION LAYER |     |   ANALYSIS LAYER    |     |   PRESENTATION      |
|                     |     |                     |     |   LAYER             |
|  +--------------+   |     |  +--------------+   |     |  +--------------+   |
|  | Memory       |---+--+  |  | Volatility  |---+--+  |  | Timeline    |---+--+
|  | Acquisition  |   |  |  |  | Framework   |   |  |  |  | Viewer      |   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  | Disk Imaging |---+  |  |  | Plaso/Super |---+  |  |  | Report      |---+  |
|  | (FTK/dd)     |   |  |  |  | Timeline    |   |  |  |  | Generator   |   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  | Network      |---+  |  |  | Network     |---+  |  |  | IOC         |---+  |
|  | Capture      |   |  |  |  | Forensics   |   |  |  |  | Export      |   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  |  +--------------+   |  |  +---------------------+  |
|  | Volatile     |---+  |  |  | Registry    |---+  |                           |
|  | Data Collect |   |  |  |  | Analysis    |   |  |                           |
|  +--------------+   |  |  |  +--------------+   |  |                           |
+---------------------+  |  +---------------------+  |
                          |                           |
                          v                           v
              +----------------------------------------------+
              |           EVIDENCE MANAGEMENT                 |
              |  +----------------------------------------+  |
              |  | Chain of Custody | Hash Verification  |  |
              |  | Evidence Locker  | Write Protection   |  |
              |  +----------------------------------------+  |
              +----------------------------------------------+
                                    |
                    +---------------+---------------+
                    |               |               |
                    v               v               v
            +-----------+  +-------------+  +------------+
            | Hot Store |  | Warm Store  |  | Cold Store |
            | (Active)  |  | (Closed)    |  | (Archive)  |
            +-----------+  +-------------+  +------------+
```

## Testing and Validation

### Forensic Tool Validation Tests

```python
import pytest
from forensic_analysis import EvidenceCollector, MemoryForensics, TimelineBuilder

class TestEvidenceIntegrity:
    def test_hash_verification(self, sample_image):
        """Verify evidence hash matches after acquisition."""
        collector = EvidenceCollector(investigator="test", case_id="TEST-001")
        result = collector.collect_disk_image(
            source=sample_image.source,
            destination="/tmp/test_image.E01",
            format="ewf"
        )
        assert result.sha256 == sample_image.expected_hash

    def test_chain_of_custody_completeness(self, evidence_item):
        """Verify chain of custody records are complete."""
        coc = evidence_item.chain_of_custody
        assert coc.entries[0].action == "acquired"
        assert coc.entries[0].custodian is not None
        assert coc.entries[0].timestamp is not None
        assert coc.verify_integrity() is True

    def test_write_blocker(self, source_device):
        """Verify write blocker was used during acquisition."""
        collector = EvidenceCollector(
            investigator="test",
            case_id="TEST-001",
            use_write_blocker=True
        )
        result = collector.collect_disk_image(source=source_device, destination="/tmp/test.E01")
        assert result.write_blocker_used is True

class TestMemoryForensics:
    def test_process_list_accuracy(self, memory_dump, expected_processes):
        """Verify process list matches expected."""
        mem = MemoryForensics(dump_path=memory_dump)
        result = mem.run_module("pslist")
        found_pids = {p.pid for p in result.items}
        for pid, name in expected_processes.items():
            assert pid in found_pids, f"Process {name} (PID {pid}) not found"

    def test_network_connection_detection(self, memory_dump):
        """Verify network connections are correctly extracted."""
        mem = MemoryForensics(dump_path=memory_dump)
        result = mem.run_module("netscan")
        assert len(result.items) > 0
        for conn in result.items:
            assert conn.src_ip is not None
            assert conn.dst_ip is not None

class TestTimelineBuilder:
    def test_timeline_completeness(self, disk_image):
        """Verify timeline contains events from all sources."""
        forensics = FileSystemForensics(image_path=disk_image)
        builder = TimelineBuilder(forensics)
        timeline = builder.build(timestamp_sources=["mft", "usnjrnl", "evtx"])
        assert len(timeline.events) > 1000
        sources = set(e.source for e in timeline.events)
        assert len(sources) >= 3

    def test_timeline_chronological_order(self, timeline):
        """Verify timeline events are in chronological order."""
        timestamps = [e.timestamp for e in timeline.events]
        assert timestamps == sorted(timestamps)
```

## Related Modules

- **threat-intelligence**: Intelligence for context during investigation
- **ioc-analysis**: Indicator analysis for evidence correlation
- **behavioral-analysis**: Behavioral patterns for timeline reconstruction
