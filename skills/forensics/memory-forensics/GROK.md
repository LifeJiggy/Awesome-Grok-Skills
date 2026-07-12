---
name: "memory-forensics"
category: "forensics"
version: "2.0.0"
tags: ["forensics", "memory-forensics", "volatility", "ram-analysis", "malware-detection"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["python", "operating-systems", "forensics-fundamentals"]
---

# Memory Forensics

## Overview

Memory forensics (RAM forensics) analyzes volatile memory dumps to extract artifacts that disk forensics cannot capture: running processes, network connections, encryption keys, injected code, rootkits, and anti-forensic activity. This module provides tools for analyzing memory images using frameworks like Volatility, extracting malware artifacts, recovering credentials, and reconstructing attacker activity from RAM captures.

## Core Capabilities

- **Process Analysis**: Extract running processes, parent-child relationships, command-line arguments, loaded DLLs, and process memory regions
- **Network Connections**: Recover active and historical network connections, socket states, associated PIDs, and DNS cache entries
- **Malware Detection**: Identify code injection (DLL injection, process hollowing), rootkit hooks, hidden processes, and suspicious API calls
- **Credential Recovery**: Extract plaintext passwords, NTLM hashes, Kerberos tickets, and browser-stored credentials from memory
- **Registry Analysis**: Reconstruct Windows registry hives from memory, extract recently accessed files, USB device history, and user activity
- **DLL and Handle Analysis**: Map loaded libraries, detect suspicious module loads, analyze open handles and file objects
- **Kernel Analysis**: Detect kernel-level rootkits, SSDT hooks, IDT modifications, and DKOM (Direct Kernel Object Manipulation)
- **Timeline from Memory**: Build activity timeline from memory-resident artifacts including timestamps, event logs, and clipboard content
- **YARA Scanning**: Scan memory regions with YARA rules for known malware signatures and behavioral patterns
- **Memory Dump Acquisition**: Live memory acquisition tools for Windows, Linux, and macOS systems

## Usage Examples

### Process Analysis

```python
from forensics.memory_forensics import MemoryAnalyzer, AnalysisProfile

analyzer = MemoryAnalyzer(
    profile=AnalysisProfile.WIN10_X64,
    volatility_path="volatility3",
)

# Analyze processes in memory dump
processes = analyzer.analyze_processes(
    memory_image="evidence/memory_dump.raw",
)

print(f"Processes Found: {len(processes)}")
for proc in processes[:10]:
    suspicious = " *** SUSPICIOUS" if proc.is_suspicious else ""
    print(f"  PID {proc.pid}: {proc.name} (PPID {proc.ppid}) {suspicious}")
    if proc.cmdline:
        print(f"    CMD: {proc.cmdline[:80]}")
    print(f"    Threads: {proc.thread_count}, Handles: {proc.handle_count}")
```

### Network Connection Analysis

```python
from forensics.memory_forensics import NetworkAnalyzer

net_analyzer = NetworkAnalyzer()

# Extract network connections
connections = net_analyzer.extract_connections(
    memory_image="evidence/memory_dump.raw",
    include_closed=True,
)

print(f"Network Connections: {len(connections)}")
for conn in connections[:10]:
    print(f"  {conn.local_address}:{conn.local_port} -> "
          f"{conn.remote_address}:{conn.remote_port} [{conn.state}]")
    print(f"    PID: {conn.pid}, Process: {conn.process_name}")
```

### Malware Detection

```python
from forensics.memory_forensics import MalwareDetector

detector = MalwareDetector(
    yara_rules_dir="rules/",
    heuristics_enabled=True,
)

# Scan for malware
findings = detector.scan(
    memory_image="evidence/memory_dump.raw",
    scan_type="comprehensive",
)

print(f"Malware Findings: {len(findings)}")
for finding in findings:
    print(f"  [{finding.severity}] {finding.rule_name}")
    print(f"    Process: {finding.process_name} (PID {finding.pid})")
    print(f"    Evidence: {finding.evidence_description}")
    print(f"    YARA Match: {finding.yara_match}")
```

### Credential Extraction

```python
from forensics.memory_forensics import CredentialExtractor

extractor = CredentialExtractor(
    decrypt_browser_creds=True,
    extract_ntlm=True,
)

# Extract credentials
creds = extractor.extract(
    memory_image="evidence/memory_dump.raw",
    target_processes=["lsass.exe", "chrome.exe", "firefox.exe"],
)

print(f"Credentials Found: {len(creds)}")
for cred in creds:
    print(f"  Type: {cred.credential_type}")
    print(f"    User: {cred.username}")
    print(f"    Source: {cred.source_process}")
    if cred.domain:
        print(f"    Domain: {cred.domain}")
```

## Architecture

```
Memory Image (.raw, .vmem, .lime)
         │
         ▼
┌─────────────────────┐
│  Memory Parser       │──→ Page table walking, structure recovery
│  (Volatility Core)   │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│Process │ │Network │──→ Connections, sockets, DNS
│Analysis│ │Analysis│
└────┬───┘ └────┬───┘
     │          │
     ▼          ▼
┌─────────────────────┐
│  Malware Detection   │──→ YARA, heuristics, injection detection
│  + Credential Ext.   │
└─────────────────────┘
```

## Best Practices

- Acquire memory before disk imaging; RAM contents are lost on power-off
- Use dedicated memory acquisition tools (WinPmem, LiME, AVML) that operate in kernel mode
- Verify memory image integrity with hash before and after analysis
- Analyze memory with the correct OS profile; wrong profiles produce false results
- Cross-reference memory artifacts with disk forensics for correlated findings
- Use YARA rules specific to the investigation target for efficient malware scanning
- Document all Volatility commands and their output for examination reports
- Check for anti-forensic memory wiping tools that zero out sensitive memory regions
- Extract encryption keys from memory before attempting disk decryption
- Analyze kernel structures to detect rootkits that hide from user-mode tools

## Related Modules

- `forensics/digital-investigation` - Overall investigation methodology
- `forensics/disk-forensics` - File system analysis for correlated evidence
- `forensics/network-forensics` - Network traffic analysis
- `forensics/mobile-forensics` - Mobile device memory analysis
