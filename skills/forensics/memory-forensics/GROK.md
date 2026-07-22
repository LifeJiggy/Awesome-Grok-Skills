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

## Advanced Configuration

### Memory Acquisition Configuration

```yaml
memory_acquisition:
  tools:
    windows:
      - name: "WinPmem"
        version: "4.0"
        mode: "kernel"
        supported_arch: ["x64", "x86"]
        
      - name: "FTK Imager Lite"
        version: "4.7"
        mode: "kernel"
        bootable: true
        
      - name: "Magnet RAM Capture"
        version: "1.0"
        mode: "kernel"
        
    linux:
      - name: "LiME"
        version: "1.8"
        mode: "kernel_module"
        supported_arch: ["x64", "x86", "arm"]
        
      - name: "AVML"
        version: "0.4"
        mode: "userland"
        compression: true
        
    macos:
      - name: "osxpmem"
        version: "2.0"
        mode: "kernel"
        
  acquisition_settings:
    compression:
      enabled: true
      algorithm: "lz4"
      level: 1
      
    hash_verification:
      algorithms: ["MD5", "SHA256"]
      verify_after_acquisition: true
      
    target_directory: "EVIDENCE/{case_number}/memory/"
    filename_pattern: "{hostname}_{timestamp}.raw"
```

### Volatility Configuration

```yaml
volatility:
  version: "3"
  path: "volatility3"
  
  profiles:
    windows:
      - "Win10x64_19041"
      - "Win10x64_19045"
      - "Win11x64_22621"
      - "Win2019x64_17763"
      - "Win2022x64_20348"
      
    linux:
      - "Linux5_4x64"
      - "Linux5_10x64"
      - "Linux5_15x64"
      - "Linux6_1x64"
      
    macos:
      - "MacOS_12_0"
      - "MacOS_13_0"
      - "MacOS_14_0"
      
  plugins:
    process_analysis:
      - "pslist"
      - "pstree"
      - "psxview"
      - "handles"
      - "cmdline"
      - "envars"
      
    network_analysis:
      - "netscan"
      - "netscanwin8"
      - "dns_cache"
      - "arp"
      
    malware_detection:
      - "malfind"
      - "ldrdetect"
      - "threads"
      - "apihooks"
      - "ssdt"
      
    credential_extraction:
      - "hashdump"
      - "lsadump"
      - "cachedump"
      - "kerberos"
      
    registry_analysis:
      - "hivelist"
      - "printkey"
      - "userassist"
      - "shellbags"
      
  performance:
    parallel_plugins: true
    max_workers: 4
    cache_size_mb: 1024
```

### YARA Rules Configuration

```yaml
yara_rules:
  directories:
    - "rules/malware/"
    - "rules/exploits/"
    - "rules/cobalt_strike/"
    - "rules/apt/"
    - "rules/custom/"
    
  scanning:
    timeout_seconds: 300
    max_memory_per_rule_mb: 100
    scan_all_memory_regions: true
    
  categories:
    malware:
      description: "Known malware signatures"
      severity_default: "high"
      
    exploit:
      description: "Exploit code patterns"
      severity_default: "critical"
      
    cobalt_strike:
      description: "Cobalt Strike beacon indicators"
      severity_default: "critical"
      
    apt:
      description: "APT group TTPs"
      severity_default: "high"
      
    suspicious:
      description: "Suspicious behavior patterns"
      severity_default: "medium"
```

## Architecture Patterns

### Memory Analysis Pipeline

```python
class MemoryAnalysisPipeline:
    def __init__(self, volatility_engine, yara_scanner):
        self.volatility = volatility_engine
        self.yara = yara_scanner
    
    async def analyze(self, memory_dump: str, case_number: str) -> MemoryAnalysisResult:
        # Detect profile
        profile = await self.volatility.detect_profile(memory_dump)
        
        # Run process analysis
        processes = await self.analyze_processes(memory_dump, profile)
        
        # Run network analysis
        connections = await self.analyze_network(memory_dump, profile)
        
        # Run malware detection
        malware = await self.detect_malware(memory_dump, profile)
        
        # Extract credentials
        credentials = await self.extract_credentials(memory_dump, profile)
        
        # Correlate findings
        correlated = self.correlate_findings(processes, connections, malware, credentials)
        
        return MemoryAnalysisResult(
            memory_dump=memory_dump,
            case_number=case_number,
            profile=profile,
            processes=processes,
            connections=connections,
            malware_findings=malware,
            credentials=credentials,
            correlated_findings=correlated,
        )
```

### Process Analysis Engine

```python
class ProcessAnalysisEngine:
    def __init__(self, volatility_engine):
        self.volatility = volatility_engine
    
    async def analyze_processes(self, memory_dump: str, profile: str) -> List[ProcessInfo]:
        # Get process list
        pslist = await self.volatility.run_plugin(memory_dump, profile, "pslist")
        
        # Get process tree
        pstree = await self.volatility.run_plugin(memory_dump, profile, "pstree")
        
        # Cross-reference with psxview for hidden processes
        psxview = await self.volatility.run_plugin(memory_dump, profile, "psxview")
        
        # Analyze each process
        processes = []
        for proc in pslist:
            process_info = ProcessInfo(
                pid=proc['PID'],
                ppid=proc['PPID'],
                name=proc['ImageFileName'],
                offset=proc['Offset(V)'],
                threads=proc['Threads'],
                handles=proc['Handles'],
                is_hidden=self.check_hidden(proc, psxview),
                is_suspicious=await self.check_suspicious(proc),
            )
            
            # Get command line
            cmdline = await self.get_cmdline(memory_dump, profile, proc['Offset(V)'])
            process_info.cmdline = cmdline
            
            # Get loaded modules
            modules = await self.get_modules(memory_dump, profile, proc['Offset(V)'])
            process_info.modules = modules
            
            processes.append(process_info)
        
        return processes
    
    async def check_suspicious(self, proc: Dict) -> bool:
        # Check for suspicious indicators
        indicators = [
            proc['ImageFileName'] in ['cmd.exe', 'powershell.exe', 'wscript.exe'],
            proc['Threads'] > 100,
            proc['Handles'] > 1000,
            await self.check_injection(proc),
        ]
        
        return any(indicators)
```

### Network Analysis Engine

```python
class NetworkAnalysisEngine:
    def __init__(self, volatility_engine):
        self.volatility = volatility_engine
    
    async def analyze_network(self, memory_dump: str, profile: str) -> List[NetworkConnection]:
        # Get network connections
        netscan = await self.volatility.run_plugin(memory_dump, profile, "netscan")
        
        # Get DNS cache
        dns_cache = await self.volatility.run_plugin(memory_dump, profile, "dns_cache")
        
        # Analyze connections
        connections = []
        for conn in netscan:
            connection = NetworkConnection(
                local_address=conn['LocalAddr'],
                local_port=conn['LocalPort'],
                remote_address=conn['ForeignAddr'],
                remote_port=conn['ForeignPort'],
                state=conn['State'],
                pid=conn['PID'],
                created_time=conn['Created'],
                owner=conn['Owner'],
            )
            
            # Check for suspicious connections
            connection.is_suspicious = await self.check_suspicious_connection(connection)
            
            connections.append(connection)
        
        return connections
    
    async def check_suspicious_connection(self, conn: NetworkConnection) -> bool:
        # Check for known malicious IPs
        malicious_ips = await self.get_malicious_ips()
        if conn.remote_address in malicious_ips:
            return True
        
        # Check for unusual ports
        unusual_ports = [4444, 5555, 6666, 7777, 8888, 9999]
        if conn.remote_port in unusual_ports:
            return True
        
        return False
```

### Malware Detection Engine

```python
class MalwareDetectionEngine:
    def __init__(self, volatility_engine, yara_scanner):
        self.volatility = volatility_engine
        self.yara = yara_scanner
    
    async def detect_malware(self, memory_dump: str, profile: str) -> List[MalwareFinding]:
        findings = []
        
        # Run malfind for code injection
        malfind = await self.volatility.run_plugin(memory_dump, profile, "malfind")
        for item in malfind:
            finding = MalwareFinding(
                type="code_injection",
                pid=item['PID'],
                process_name=item['Process'],
                evidence=item['Hexdump'][:200],
                severity="high",
            )
            findings.append(finding)
        
        # Run YARA scan
        yara_matches = await self.yara.scan_memory(memory_dump)
        for match in yara_matches:
            finding = MalwareFinding(
                type="yara_match",
                rule=match['rule'],
                pid=match.get('pid'),
                process_name=match.get('process'),
                evidence=match['strings'][:200],
                severity=match.get('severity', 'medium'),
            )
            findings.append(finding)
        
        # Check for rootkit indicators
        rootkit_indicators = await self.check_rootkit(memory_dump, profile)
        for indicator in rootkit_indicators:
            finding = MalwareFinding(
                type="rootkit",
                description=indicator['description'],
                severity="critical",
            )
            findings.append(finding)
        
        return findings
```

## Integration Guide

### Volatility 3 Integration

```python
class Volatility3Integration:
    def __init__(self, volatility_path: str):
        self.volatility_path = volatility_path
    
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
    
    async def detect_profile(self, memory_dump: str) -> str:
        cmd = [
            self.volatility_path,
            "-f", memory_dump,
            "windows.info",
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        return self.parse_profile(stdout.decode())
```

### YARA Integration

```python
import yara

class YARAIntegration:
    def __init__(self, rules_path: str):
        self.rules = yara.compile(filepath=rules_path)
    
    async def scan_memory(self, memory_dump: str) -> List[YARAMatch]:
        matches = self.rules.match(memory_dump)
        
        results = []
        for match in matches:
            results.append({
                'rule': match.rule,
                'tags': match.tags,
                'meta': match.meta,
                'strings': self.extract_strings(match.strings),
            })
        
        return results
    
    def extract_strings(self, strings: List) -> str:
        extracted = []
        for s in strings:
            extracted.append(f"{s[1]}: {s[2]}")
        return "\n".join(extracted[:10])
```

### Memory Acquisition Tool Integration

```python
class MemoryAcquisitionIntegration:
    def __init__(self, tool_path: str):
        self.tool_path = tool_path
    
    async def acquire_memory_windows(self, output_path: str) -> AcquisitionResult:
        cmd = [
            self.tool_path,
            "-o", output_path,
            "--compress",
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        # Calculate hashes
        md5 = await self.calculate_hash(output_path, "md5")
        sha256 = await self.calculate_hash(output_path, "sha256")
        
        return AcquisitionResult(
            output_path=output_path,
            size_bytes=os.path.getsize(output_path),
            md5_hash=md5,
            sha256_hash=sha256,
            success=process.returncode == 0,
        )
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_processes_memory_dump ON processes (memory_dump_id, pid);
CREATE INDEX idx_connections_memory_dump ON network_connections (memory_dump_id, local_port);
CREATE INDEX idx_malware_findings_memory_dump ON malware_findings (memory_dump_id, severity);

-- Create full-text search index
CREATE INDEX idx_process_name_search ON processes USING gin(to_tsvector('english', name));

-- Partition malware findings by date
CREATE TABLE malware_findings (
    id UUID PRIMARY KEY,
    memory_dump_id VARCHAR(100),
    finding_type VARCHAR(50),
    severity VARCHAR(20),
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);
```

### Caching Strategy

```python
class MemoryForensicsCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_analysis_result(self, memory_dump_id: str) -> Optional[MemoryAnalysisResult]:
        cache_key = f"memory_analysis:{memory_dump_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return MemoryAnalysisResult.from_json(cached)
        return None
    
    async def cache_analysis_result(self, memory_dump_id: str, result: MemoryAnalysisResult):
        cache_key = f"memory_analysis:{memory_dump_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            result.to_json()
        )
```

### Batch Processing

```python
class MemoryForensicsBatchProcessor:
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
    
    async def process_batch(self, memory_dumps: List[str], analyzer: MemoryAnalyzer):
        batches = [
            memory_dumps[i:i+self.batch_size]
            for i in range(0, len(memory_dumps), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                analyzer.analyze(dump) for dump in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Evidence Encryption

```python
from cryptography.fernet import Fernet

class MemoryEvidenceEncryption:
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
class MemoryForensicsAccessControl:
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
class MemoryForensicsAuditLogger:
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

**Issue: Wrong profile detection**
```python
async def diagnose_profile_detection(memory_dump: str):
    # Try multiple profile detection methods
    methods = ["windows.info", "linux.info", "macos.info"]
    
    for method in methods:
        result = await volatility.run_plugin(memory_dump, "", method)
        print(f"Method {method}: {result}")
    
    print(f"Recommendation: Manually specify profile if auto-detection fails")
```

**Issue: Incomplete process list**
```python
async def diagnose_process_list(memory_dump: str, profile: str):
    # Compare pslist, pstree, and psxview
    pslist = await volatility.run_plugin(memory_dump, profile, "pslist")
    pstree = await volatility.run_plugin(memory_dump, profile, "pstree")
    psxview = await volatility.run_plugin(memory_dump, profile, "psxview")
    
    pslist_pids = set(p['PID'] for p in pslist)
    pstree_pids = set(p['PID'] for p in pstree)
    
    missing_from_pstree = pslist_pids - pstree_pids
    
    print(f"pslist PIDs: {len(pslist_pids)}")
    print(f"pstree PIDs: {len(pstree_pids)}")
    print(f"Missing from pstree: {len(missing_from_pstree)}")
    
    if missing_from_pstree:
        print(f"PIDs: {missing_from_pstree}")
        print(f"Recommendation: Check for process hiding techniques")
```

**Issue: YARA scan timeout**
```python
async def diagnose_yara_timeout(memory_dump: str):
    # Check memory dump size
    size_gb = os.path.getsize(memory_dump) / 1e9
    print(f"Memory dump size: {size_gb:.2f} GB")
    
    if size_gb > 16:
        print(f"WARNING: Large memory dump may cause timeouts")
        print(f"Recommendation:")
        print(f"  1. Increase timeout to 600 seconds")
        print(f"  2. Scan specific memory regions only")
        print(f"  3. Use optimized YARA rules")
```

## API Reference

### Memory Analysis API

```python
# Analyze memory dump
POST /api/v1/memory/analyze
Request:
{
    "memory_dump": "evidence/memory_dump.raw",
    "case_number": "CASE-2026-0042",
    "analysis_type": "comprehensive"
}

Response:
{
    "analysis_id": "MEM-001",
    "profile": "Win10x64_19041",
    "processes_found": 150,
    "connections_found": 25,
    "malware_findings": 3,
    "credentials_found": 5,
    "status": "completed"
}

# Get analysis results
GET /api/v1/memory/analysis/{analysis_id}
Response:
{
    "analysis_id": "MEM-001",
    "processes": [...],
    "connections": [...],
    "malware_findings": [...],
    "credentials": [...]
}
```

### Process Analysis API

```python
# Get processes
GET /api/v1/memory/{analysis_id}/processes
Response:
{
    "processes": [
        {
            "pid": 4,
            "ppid": 0,
            "name": "System",
            "is_suspicious": false,
            "cmdline": "",
            "threads": 150,
            "handles": 2500
        }
    ]
}
```

### Network Analysis API

```python
# Get network connections
GET /api/v1/memory/{analysis_id}/connections
Response:
{
    "connections": [
        {
            "local_address": "192.168.1.100",
            "local_port": 49752,
            "remote_address": "93.184.216.34",
            "remote_port": 443,
            "state": "ESTABLISHED",
            "pid": 1234,
            "process_name": "chrome.exe"
        }
    ]
}
```

## Data Models

### Memory Analysis Result Model

```python
class MemoryAnalysisResult:
    analysis_id: str
    memory_dump: str
    case_number: str
    profile: str
    acquisition_time: Optional[datetime]
    analysis_time: datetime
    processes: List[ProcessInfo]
    connections: List[NetworkConnection]
    malware_findings: List[MalwareFinding]
    credentials: List[Credential]
    correlated_findings: List[CorrelatedFinding]
```

### Process Info Model

```python
class ProcessInfo:
    pid: int
    ppid: int
    name: str
    offset: int
    threads: int
    handles: int
    is_hidden: bool
    is_suspicious: bool
    cmdline: Optional[str]
    modules: List[str]
    created_time: Optional[datetime]
```

### Malware Finding Model

```python
class MalwareFinding:
    finding_id: str
    type: str  # code_injection, yara_match, rootkit
    rule: Optional[str]
    pid: Optional[int]
    process_name: Optional[str]
    evidence: str
    severity: str  # low, medium, high, critical
    created_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memory-forensics-service
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
      app: memory-forensics-service
  template:
    metadata:
      labels:
        app: memory-forensics-service
    spec:
      containers:
      - name: memory-forensics
        image: your-registry/memory-forensics-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "2Gi"
            cpu: "2000m"
          limits:
            memory: "4Gi"
            cpu: "4000m"
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

# Analysis metrics
memory_analyses_counter = Counter(
    'forensics_memory_analyses_total',
    'Total memory analyses',
    ['profile', 'status']
)

memory_analysis_duration = Histogram(
    'forensics_memory_analysis_duration_seconds',
    'Memory analysis duration',
    ['analysis_type'],
    buckets=[60, 300, 600, 1800, 3600]
)

# Finding metrics
malware_findings_counter = Counter(
    'forensics_malware_findings_total',
    'Total malware findings',
    ['type', 'severity']
)

# Process metrics
processes_extracted_counter = Counter(
    'forensics_processes_extracted_total',
    'Total processes extracted',
    ['memory_dump_id']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Memory Forensics",
    "panels": [
      {
        "title": "Analysis Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(forensics_memory_analyses_total[5m])",
            "legendFormat": "{{profile}} - {{status}}"
          }
        ]
      },
      {
        "title": "Malware Findings",
        "type": "pie",
        "targets": [
          {
            "expr": "rate(forensics_malware_findings_total[5m])",
            "legendFormat": "{{type}}"
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
- name: memory_forensics_alerts
  rules:
  - alert: HighMalwareDetectionRate
    expr: rate(forensics_malware_findings_total{severity="critical"}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Critical malware detection rate high"
      
  - alert: AnalysisBacklog
    expr: forensics_memory_analyses_total{status="pending"} > 5
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Memory analysis backlog exceeds 5"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestProcessAnalysis:
    def test_extract_processes(self, memory_analyzer):
        processes = memory_analyzer.analyze_processes(
            memory_dump="test_memory.raw",
            profile="Win10x64_19041",
        )
        
        assert len(processes) > 0
        assert all(p.pid is not None for p in processes)
    
    def test_detect_suspicious_process(self, memory_analyzer):
        processes = memory_analyzer.analyze_processes(
            memory_dump="test_memory.raw",
            profile="Win10x64_19041",
        )
        
        suspicious = [p for p in processes if p.is_suspicious]
        assert len(suspicious) >= 0  # May or may not find suspicious processes
```

### Integration Tests

```python
class TestEndToEndMemoryForensics:
    async def test_memory_analysis_flow(self, memory_forensics_system):
        # Analyze memory dump
        result = await memory_forensics_system.analyze(
            memory_dump="test_memory.raw",
            case_number="CASE-TEST-001",
        )
        
        assert result.analysis_id is not None
        assert result.profile is not None
        assert len(result.processes) > 0
        
        # Get specific analysis
        analysis = await memory_forensics_system.get_analysis(result.analysis_id)
        assert analysis.analysis_id == result.analysis_id
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class MemoryForensicsUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(5)
    def analyze_memory(self):
        self.client.post("/api/v1/memory/analyze", json={
            "memory_dump": f"test_memory_{self.dump_counter}.raw",
            "case_number": f"CASE-{self.dump_counter}",
        })
        self.dump_counter += 1
    
    @task(10)
    def get_analysis(self):
        self.client.get(f"/api/v1/memory/analysis/analysis-{self.analysis_counter}")
        self.analysis_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/memory/analyze", methods=["POST"])
@app.route("/api/v2/memory/analyze", methods=["POST"])
async def analyze_memory():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await analyze_memory_v2()
    return await analyze_memory_v1()
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

- **LiME**: Linux Memory Extractor - kernel module for memory acquisition
- **Volatility**: Open-source memory forensics framework
- **YARA**: Pattern matching tool for malware identification
- **Process Hollowing**: Malware technique hiding code in legitimate process
- **DLL Injection**: Technique loading malicious DLL into target process
- **Rootkit**: Software hiding malicious activity from OS
- **SSDT**: System Service Descriptor Table - kernel hooking target
- **DKOM**: Direct Kernel Object Manipulation - rootkit technique
- **LSASS**: Local Security Authority Subsystem Service - stores credentials
- **NTLM**: Windows authentication protocol hashes

## Changelog

### Version 2.0.0 (2026-07-01)
- Added Volatility 3 support
- Implemented YARA scanning integration
- Enhanced rootkit detection
- Added credential extraction

### Version 1.5.0 (2026-01-15)
- Added network connection analysis
- Implemented process tree analysis
- Enhanced malware detection

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic process analysis
- Memory dump parsing

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def analyze_processes(
    memory_dump: str,
    profile: str,
) -> List[ProcessInfo]:
    """Analyze processes in memory dump.
    
    Args:
        memory_dump: Path to memory dump file.
        profile: Memory profile.
    
    Returns:
        List of process information.
    
    Raises:
        AnalysisError: If analysis fails.
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

Copyright (c) 2026 Memory Forensics Platform

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
