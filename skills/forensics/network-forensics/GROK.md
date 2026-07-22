---
name: "network-forensics"
category: "forensics"
version: "2.0.0"
tags: ["forensics", "network-forensics", "pcap-analysis", "traffic-analysis", "packet-inspection"]
difficulty: "advanced"
estimated_time: "40-55 minutes"
prerequisites: ["python", "networking-fundamentals", "tcpip"]
---

# Network Forensics

## Overview

Network forensics captures, records, and analyzes network traffic to investigate security incidents, detect intrusions, reconstruct data transfers, and attribute malicious activity. This module provides tools for PCAP analysis, protocol decoding, traffic reconstruction, IDS alert triage, NetFlow analysis, and encrypted traffic intelligence for forensic investigations.

## Core Capabilities

- **PCAP Analysis**: Deep packet inspection and protocol decoding for captured network traffic with session reconstruction
- **Traffic Reconstruction**: Reassemble TCP streams, extract files transferred over HTTP/FTP/SMB, and reconstruct email conversations
- **Protocol Analysis**: Decode and analyze HTTP, DNS, SMTP, SMB, RDP, SSH, TLS, and custom protocols
- **NetFlow Analysis**: IP flow data analysis for bandwidth usage, communication patterns, and anomaly detection
- **IDS/IPS Alert Triage**: Analyze Snort/Suricata alerts with full packet context for true positive validation
- **DNS Forensics**: DNS query/response analysis, DGA detection, DNS tunneling identification, and passive DNS reconstruction
- **TLS/SSL Analysis**: Certificate analysis, JA3/JA3S fingerprinting, encrypted traffic metadata analysis
- **Exfiltration Detection**: Identify data exfiltration patterns including DNS tunneling, ICMP tunneling, and covert channels
- **Wireless Forensics**: 802.11 packet capture analysis, deauth detection, and rogue AP identification
- **Network Timeline**: Build chronological timeline of all network activity from captures

## Usage Examples

### PCAP Analysis

```python
from forensics.network_forensics import PCAPAnalyzer, ProtocolFilter

analyzer = PCAPAnalyzer(
   pcap_path="evidence/capture.pcap",
    max_packets=1_000_000,
)

# Get summary statistics
summary = analyzer.get_summary()
print(f"Packets: {summary.total_packets:,}")
print(f"Duration: {summary.duration_seconds:.1f}s")
print(f"Protocols: {summary.protocol_distribution}")
print(f"Source IPs: {summary.unique_src_ips}")
print(f"Dest IPs: {summary.unique_dst_ips}")

# Filter and analyze specific traffic
http_sessions = analyzer.filter(
    protocol=ProtocolFilter.HTTP,
    src_ip="192.168.1.100",
)

for session in http_sessions[:5]:
    print(f"  {session.method} {session.url}")
    print(f"    Status: {session.status_code}, Size: {session.response_size} bytes")
```

### DNS Forensics

```python
from forensics.network_forensics import DNSAnalyzer

dns = DNSAnalyzer()

# Analyze DNS traffic
dns_analysis = dns.analyze(
    pcap_path="evidence/capture.pcap",
    detect_dga=True,
    detect_tunneling=True,
)

print(f"DNS Queries: {dns_analysis.total_queries}")
print(f"Unique Domains: {dns_analysis.unique_domains}")
print(f"DGA Suspects: {len(dns_analysis.dga_candidates)}")
for dga in dns_analysis.dga_candidates[:3]:
    print(f"  DGA: {dga.domain} (entropy={dga.entropy:.2f}, freq={dga.query_count})")

print(f"DNS Tunnel Suspects: {len(dns_analysis.tunnel_candidates)}")
for tunnel in dns_analysis.tunnel_candidates:
    print(f"  Tunnel: {tunnel.domain} ({tunnel.total_data_bytes} bytes)")
```

### File Extraction

```python
from forensics.network_forensics import FileExtractor

extractor = FileExtractor(
    output_dir="extracted_files/",
    verify_hashes=True,
)

# Extract files from network capture
files = extractor.extract_from_pcap(
    pcap_path="evidence/capture.pcap",
    protocols=["http", "ftp", "smb", "tftp"],
    file_types=["executable", "document", "archive", "image"],
)

print(f"Files Extracted: {len(files)}")
for f in files:
    print(f"  {f.filename} ({f.file_type})")
    print(f"    Size: {f.size_bytes:,} bytes, MD5: {f.md5_hash[:16]}...")
    print(f"    Source: {f.source_ip}:{f.source_port} -> {f.dest_ip}:{f.dest_port}")
```

### NetFlow Analysis

```python
from forensics.network_forensics import NetFlowAnalyzer

netflow = NetFlowAnalyzer()

# Analyze flow data
analysis = netflow.analyze(
    flow_data="evidence/netflow.csv",
    time_window="2026-07-01 08:00:00/2026-07-01 18:00:00",
)

print(f"Top Talkers:")
for host in analysis.top_talkers[:5]:
    print(f"  {host.ip}: {host.bytes_sent / 1e6:.1f} MB sent, "
          f"{host.bytes_received / 1e6:.1f} MB received")

print(f"\nAnomalies Detected: {len(analysis.anomalies)}")
for anomaly in analysis.anomalies:
    print(f"  [{anomaly.severity}] {anomaly.description}")
```

## Best Practices

- Capture traffic at network boundaries (firewall, internet gateway) for maximum visibility
- Use ring buffers for continuous capture to avoid disk space exhaustion
- Preserve original PCAP files with hash verification; analyze working copies
- Correlate network timestamps with host-based artifacts for comprehensive timelines
- Analyze DNS traffic separately; it's often the best indicator of C2 and exfiltration
- Use JA3/JA3S fingerprints to identify malware TLS connections without decryption
- Extract and analyze TLS certificates for phishing and C2 infrastructure identification
- Monitor for DNS tunneling by tracking query length, entropy, and subdomain depth
- Document all filter criteria applied during analysis for reproducibility
- Preserve NetFlow data for at least 90 days for historical investigation support

## Related Modules

- `forensics/digital-investigation` - Overall investigation methodology
- `forensics/memory-forensics` - Memory analysis for network artifacts
- `forensics/disk-forensics` - Disk artifacts for correlated network evidence

## Advanced Configuration

### PCAP Capture Configuration

```yaml
pcap_capture:
  interfaces:
    - name: "eth0"
      description: "External facing interface"
      capture_filter: "not port 22"
      snaplen: 65535
      promiscuous: true
      
    - name: "eth1"
      description: "Internal network interface"
      capture_filter: ""
      snaplen: 65535
      promiscuous: true
      
  storage:
    output_dir: "/evidence/pcaps/"
    file_pattern: "{interface}_{timestamp}.pcap"
    max_file_size_mb: 1000
    rotation_strategy: "size"
    
  ring_buffer:
    enabled: true
    buffer_size_mb: 1024
    num_files: 10
    
  compression:
    enabled: true
    algorithm: "lz4"
    
  metadata:
    capture_interface: true
    capture_timestamp: true
    capture_filters: true
    hash_after_capture: true
    hash_algorithms: ["MD5", "SHA256"]
```

### Protocol Analysis Configuration

```yaml
protocol_analysis:
  protocols:
    http:
      enabled: true
      extract_bodies: true
      extract_files: true
      max_body_size_mb: 100
      
    dns:
      enabled: true
      detect_dga: true
      detect_tunneling: true
      entropy_threshold: 4.0
      query_length_threshold: 50
      
    smtp:
      enabled: true
      extract_attachments: true
      extract_bodies: true
      
    smb:
      enabled: true
      extract_files: true
      
    tls:
      enabled: true
      extract_certificates: true
      calculate_ja3: true
      calculate_ja3s: true
      
    ssh:
      enabled: true
      extract_commands: true
      
    rdp:
      enabled: true
      extractScreenshots: false
      
  analysis:
    session_reconstruction: true
    max_session_duration_minutes: 60
    max_session_bytes: 1000000000
    
  output:
    format: "json"
    include_raw_packets: false
    include_payloads: true
    max_payload_bytes: 1024
```

### NetFlow Analysis Configuration

```yaml
netflow_analysis:
  data_sources:
    - name: "router_netflow"
      type: "netflow_v9"
      endpoint: "router.internal"
      poll_interval_seconds: 60
      
    - name: "firewall_ipfix"
      type: "ipfix"
      endpoint: "firewall.internal"
      poll_interval_seconds: 30
      
  storage:
    database: "timescaledb"
    retention_days: 90
    compression: true
    
  analysis:
    top_n_talkers: 20
    anomaly_detection:
      enabled: true
      method: "isolation_forest"
      sensitivity: 0.1
      
  alerting:
    bandwidth_threshold_mbps: 100
    connection_threshold: 10000
    unique_dst_threshold: 100
```

### IDS/IPS Integration Configuration

```yaml
ids_integration:
  engines:
    - name: "suricata"
      version: "7.0"
      rules_path: "/etc/suricata/rules/"
      log_path: "/var/log/suricata/"
      
    - name: "snort"
      version: "3.1"
      rules_path: "/etc/snort/rules/"
      log_path: "/var/log/snort/"
      
  alert_processing:
    auto_triage: true
    correlation_window_seconds: 300
    severity_mapping:
      critical: 1
      high: 2
      medium: 3
      low: 4
      informational: 5
      
  enrichment:
    threat_intel: true
    geo_ip: true
    whois: true
    reputation_lookup: true
```

## Architecture Patterns

### Network Traffic Analysis Pipeline

```python
class NetworkTrafficAnalyzer:
    def __init__(self, pcap_parser, protocol_decoders):
        self.pcap_parser = pcap_parser
        self.decoders = protocol_decoders
    
    async def analyze_pcap(self, pcap_path: str) -> PCAPAnalysisResult:
        # Parse PCAP
        packets = await self.pcap_parser.parse(pcap_path)
        
        # Reconstruct sessions
        sessions = await self.reconstruct_sessions(packets)
        
        # Decode protocols
        decoded = await self.decode_protocols(sessions)
        
        # Extract files
        files = await self.extract_files(decoded)
        
        # Analyze DNS
        dns_analysis = await self.analyze_dns(decoded)
        
        # Analyze TLS
        tls_analysis = await self.analyze_tls(decoded)
        
        return PCAPAnalysisResult(
            pcap_path=pcap_path,
            total_packets=len(packets),
            sessions=sessions,
            decoded_protocols=decoded,
            extracted_files=files,
            dns_analysis=dns_analysis,
            tls_analysis=tls_analysis,
        )
```

### Session Reconstruction Engine

```python
class SessionReconstructionEngine:
    def __init__(self, packet_reassembler):
        self.reassembler = packet_reassembler
    
    async def reconstruct_sessions(self, packets: List[Packet]) -> List[Session]:
        # Group packets by flow
        flows = self.group_by_flow(packets)
        
        # Reassemble TCP streams
        sessions = []
        for flow_key, flow_packets in flows.items():
            if flow_key.protocol == "TCP":
                stream = await self.reassembler.reassemble_tcp(flow_packets)
                session = Session(
                    flow_key=flow_key,
                    packets=flow_packets,
                    stream_data=stream,
                    start_time=flow_packets[0].timestamp,
                    end_time=flow_packets[-1].timestamp,
                )
            else:
                session = Session(
                    flow_key=flow_key,
                    packets=flow_packets,
                    stream_data=None,
                    start_time=flow_packets[0].timestamp,
                    end_time=flow_packets[-1].timestamp,
                )
            
            sessions.append(session)
        
        return sessions
    
    def group_by_flow(self, packets: List[Packet]) -> Dict[FlowKey, List[Packet]]:
        flows = {}
        for packet in packets:
            flow_key = FlowKey(
                src_ip=packet.src_ip,
                dst_ip=packet.dst_ip,
                src_port=packet.src_port,
                dst_port=packet.dst_port,
                protocol=packet.protocol,
            )
            
            if flow_key not in flows:
                flows[flow_key] = []
            flows[flow_key].append(packet)
        
        return flows
```

### DNS Forensics Engine

```python
class DNSForensicsEngine:
    def __init__(self, dga_detector, tunnel_detector):
        self.dga_detector = dga_detector
        self.tunnel_detector = tunnel_detector
    
    async def analyze_dns(self, packets: List[Packet]) -> DNSAnalysisResult:
        # Extract DNS queries and responses
        dns_queries = self.extract_dns_queries(packets)
        dns_responses = self.extract_dns_responses(packets)
        
        # Detect DGA domains
        dga_candidates = await self.dga_detector.detect(dns_queries)
        
        # Detect DNS tunneling
        tunnel_candidates = await self.tunnel_detector.detect(dns_queries, dns_responses)
        
        # Build domain inventory
        domain_inventory = self.build_domain_inventory(dns_queries, dns_responses)
        
        return DNSAnalysisResult(
            total_queries=len(dns_queries),
            total_responses=len(dns_responses),
            unique_domains=len(domain_inventory),
            dga_candidates=dga_candidates,
            tunnel_candidates=tunnel_candidates,
            domain_inventory=domain_inventory,
        )
    
    async def detect_dga(self, domains: List[str]) -> List[DGACandidate]:
        candidates = []
        
        for domain in domains:
            # Calculate entropy
            entropy = self.calculate_entropy(domain)
            
            # Check character distribution
            char_dist = self.calculate_char_distribution(domain)
            
            # Check for dictionary words
            has_dict_words = self.check_dictionary_words(domain)
            
            # Apply DGA heuristics
            if entropy > 4.0 and not has_dict_words:
                candidates.append(DGACandidate(
                    domain=domain,
                    entropy=entropy,
                    char_distribution=char_dist,
                    confidence=min(entropy / 5.0, 1.0),
                ))
        
        return candidates
```

### File Extraction Engine

```python
class FileExtractionEngine:
    def __init__(self, protocol_decoders, file_carver):
        self.decoders = protocol_decoders
        self.carver = file_carver
    
    async def extract_files(self, sessions: List[Session]) -> List[ExtractedFile]:
        extracted_files = []
        
        for session in sessions:
            # Extract from HTTP
            if session.flow_key.dst_port == 80 or session.flow_key.dst_port == 443:
                http_files = await self.decoders.http.extract_files(session)
                extracted_files.extend(http_files)
            
            # Extract from FTP
            elif session.flow_key.dst_port == 21:
                ftp_files = await self.decoders.ftp.extract_files(session)
                extracted_files.extend(ftp_files)
            
            # Extract from SMB
            elif session.flow_key.dst_port == 445:
                smb_files = await self.decoders.smb.extract_files(session)
                extracted_files.extend(smb_files)
        
        # Calculate hashes
        for file in extracted_files:
            file.md5_hash = await self.calculate_md5(file.data)
            file.sha256_hash = await self.calculate_sha256(file.data)
        
        return extracted_files
```

## Integration Guide

### Scapy Integration

```python
from scapy.all import rdpcap, TCP, UDP, IP

class ScapyIntegration:
    def __init__(self):
        pass
    
    async def parse_pcap(self, pcap_path: str) -> List[Packet]:
        # Read PCAP with Scapy
        packets = rdpcap(pcap_path)
        
        # Convert to our Packet format
        parsed_packets = []
        for pkt in packets:
            if IP in pkt:
                packet = Packet(
                    timestamp=float(pkt.time),
                    src_ip=pkt[IP].src,
                    dst_ip=pkt[IP].dst,
                    protocol=pkt[IP].proto,
                    length=len(pkt),
                )
                
                if TCP in pkt:
                    packet.src_port = pkt[TCP].sport
                    packet.dst_port = pkt[TCP].dport
                    packet.flags = str(pkt[TCP].flags)
                    packet.payload = bytes(pkt[TCP].payload)
                elif UDP in pkt:
                    packet.src_port = pkt[UDP].sport
                    packet.dst_port = pkt[UDP].dport
                    packet.payload = bytes(pkt[UDP].payload)
                
                parsed_packets.append(packet)
        
        return parsed_packets
```

### Zeek Integration

```python
class ZeekIntegration:
    def __init__(self, zeek_path: str):
        self.zeek_path = zeek_path
    
    async def analyze_pcap(self, pcap_path: str) -> ZeekResult:
        # Run Zeek on PCAP
        cmd = [
            self.zeek_path,
            "-r", pcap_path,
            "/opt/zeek/share/zeek/site/",
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        # Parse Zeek logs
        logs = await self.parse_zeek_logs(os.path.dirname(pcap_path))
        
        return ZeekResult(
            pcap_path=pcap_path,
            logs=logs,
            success=process.returncode == 0,
        )
```

### Suricata Integration

```python
class SuricataIntegration:
    def __init__(self, suricata_path: str):
        self.suricata_path = suricata_path
    
    async def analyze_pcap(self, pcap_path: str) -> SuricataResult:
        # Run Suricata on PCAP
        cmd = [
            self.suricata_path,
            "-r", pcap_path,
            "-l", "/tmp/suricata_output/",
            "-q", "0",
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        # Parse EVE JSON log
        alerts = await self.parse_eve_json("/tmp/suricata_output/eve.json")
        
        return SuricataResult(
            pcap_path=pcap_path,
            alerts=alerts,
            success=process.returncode == 0,
        )
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_pcap_sessions_source ON pcap_sessions (src_ip, src_port);
CREATE INDEX idx_dns_queries_domain ON dns_queries (query_name, query_type);
CREATE INDEX idx_extracted_files_hash ON extracted_files (md5_hash, sha256_hash);

-- Create full-text search index
CREATE INDEX idx_domain_search ON dns_queries USING gin(to_tsvector('english', query_name));

-- Partition packets by timestamp
CREATE TABLE packets (
    id UUID PRIMARY KEY,
    pcap_id VARCHAR(100),
    timestamp TIMESTAMP,
    src_ip INET,
    dst_ip INET,
    src_port INTEGER,
    dst_port INTEGER,
    protocol INTEGER,
    length INTEGER
) PARTITION BY RANGE (timestamp);
```

### Caching Strategy

```python
class NetworkForensicsCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_pcap_summary(self, pcap_id: str) -> Optional[PCAPSummary]:
        cache_key = f"pcap_summary:{pcap_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return PCAPSummary.from_json(cached)
        return None
    
    async def cache_pcap_summary(self, pcap_id: str, summary: PCAPSummary):
        cache_key = f"pcap_summary:{pcap_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            summary.to_json()
        )
```

### Batch Processing

```python
class NetworkForensicsBatchProcessor:
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

class NetworkEvidenceEncryption:
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
class NetworkForensicsAccessControl:
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
class NetworkForensicsAuditLogger:
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

**Issue: Large PCAP file handling**
```python
async def handle_large_pcap(pcap_path: str):
    # Check file size
    size_gb = os.path.getsize(pcap_path) / 1e9
    print(f"PCAP file size: {size_gb:.2f} GB")
    
    if size_gb > 10:
        print(f"WARNING: Large PCAP file")
        print(f"Recommendations:")
        print(f"  1. Use tcpdump for initial filtering")
        print(f"  2. Split into smaller files")
        print(f"  3. Use memory-mapped files")
        print(f"  4. Increase timeout to 3600 seconds")
```

**Issue: Protocol decoding errors**
```python
async def diagnose_protocol_errors(pcap_path: str):
    # Try to parse with different decoders
    decoders = ["scapy", "dpkt", "pyshark"]
    
    for decoder in decoders:
        try:
            result = await decode_with(pcap_path, decoder)
            print(f"Decoder {decoder}: Success ({len(result.packets)} packets)")
        except Exception as e:
            print(f"Decoder {decoder}: Failed ({e})")
    
    print(f"Recommendation: Use the most compatible decoder")
```

**Issue: DNS analysis timeouts**
```python
async def diagnose_dns_timeout(pcap_path: str):
    # Count DNS packets
    dns_count = await count_dns_packets(pcap_path)
    print(f"DNS packets: {dns_count}")
    
    if dns_count > 1000000:
        print(f"WARNING: High DNS packet count")
        print(f"Recommendations:")
        print(f"  1. Filter to specific domains first")
        print(f"  2. Use batch processing")
        print(f"  3. Increase timeout to 1800 seconds")
```

## API Reference

### PCAP Analysis API

```python
# Analyze PCAP
POST /api/v1/pcap/analyze
Request:
{
    "pcap_path": "evidence/capture.pcap",
    "case_number": "CASE-2026-0042",
    "analysis_type": "comprehensive"
}

Response:
{
    "analysis_id": "PCAP-001",
    "total_packets": 1500000,
    "duration_seconds": 3600,
    "unique_src_ips": 250,
    "unique_dst_ips": 500,
    "protocols": {"TCP": 1200000, "UDP": 300000},
    "status": "completed"
}

# Get PCAP summary
GET /api/v1/pcap/analysis/{analysis_id}
Response:
{
    "analysis_id": "PCAP-001",
    "sessions": [...],
    "dns_analysis": {...},
    "tls_analysis": {...},
    "extracted_files": [...]
}
```

### DNS Analysis API

```python
# Analyze DNS traffic
POST /api/v1/dns/analyze
Request:
{
    "pcap_path": "evidence/capture.pcap",
    "detect_dga": true,
    "detect_tunneling": true
}

Response:
{
    "analysis_id": "DNS-001",
    "total_queries": 50000,
    "unique_domains": 2500,
    "dga_candidates": [
        {"domain": "xkr4j2m9.com", "entropy": 4.2, "confidence": 0.85}
    ],
    "tunnel_candidates": [
        {"domain": "data.evil.com", "total_bytes": 15000}
    ]
}
```

### File Extraction API

```python
# Extract files from PCAP
POST /api/v1/files/extract
Request:
{
    "pcap_path": "evidence/capture.pcap",
    "protocols": ["http", "ftp", "smb"],
    "file_types": ["executable", "document"]
}

Response:
{
    "extraction_id": "FILE-001",
    "files_extracted": 25,
    "files": [
        {
            "filename": "malware.exe",
            "file_type": "executable",
            "size_bytes": 250000,
            "md5_hash": "abc123...",
            "sha256_hash": "def456..."
        }
    ]
}
```

## Data Models

### PCAP Analysis Result Model

```python
class PCAPAnalysisResult:
    analysis_id: str
    pcap_path: str
    case_number: str
    total_packets: int
    duration_seconds: float
    unique_src_ips: int
    unique_dst_ips: int
    protocols: Dict[str, int]
    sessions: List[Session]
    dns_analysis: Optional[DNSAnalysisResult]
    tls_analysis: Optional[TLSAnalysisResult]
    extracted_files: List[ExtractedFile]
    created_at: datetime
```

### DNS Analysis Result Model

```python
class DNSAnalysisResult:
    analysis_id: str
    total_queries: int
    total_responses: int
    unique_domains: int
    dga_candidates: List[DGACandidate]
    tunnel_candidates: List[TunnelCandidate]
    domain_inventory: Dict[str, DomainInfo]
    created_at: datetime
```

### Extracted File Model

```python
class ExtractedFile:
    file_id: str
    filename: str
    file_type: str
    size_bytes: int
    md5_hash: str
    sha256_hash: str
    source_ip: str
    source_port: int
    dest_ip: str
    dest_port: int
    protocol: str
    extracted_at: datetime
    data: Optional[bytes]
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: network-forensics-service
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
      app: network-forensics-service
  template:
    metadata:
      labels:
        app: network-forensics-service
    spec:
      containers:
      - name: network-forensics
        image: your-registry/network-forensics-service:2.0.0
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

# PCAP analysis metrics
pcap_analyses_counter = Counter(
    'forensics_pcap_analyses_total',
    'Total PCAP analyses',
    ['status']
)

pcap_analysis_duration = Histogram(
    'forensics_pcap_analysis_duration_seconds',
    'PCAP analysis duration',
    buckets=[60, 300, 600, 1800, 3600]
)

# File extraction metrics
files_extracted_counter = Counter(
    'forensics_files_extracted_total',
    'Total files extracted',
    ['protocol', 'file_type']
)

# DNS analysis metrics
dns_queries_analyzed_counter = Counter(
    'forensics_dns_queries_analyzed_total',
    'Total DNS queries analyzed'
)

dga_candidates_counter = Counter(
    'forensics_dga_candidates_total',
    'Total DGA candidates detected'
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Network Forensics",
    "panels": [
      {
        "title": "PCAP Analysis Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(forensics_pcap_analyses_total[5m])",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "title": "Files Extracted",
        "type": "pie",
        "targets": [
          {
            "expr": "rate(forensics_files_extracted_total[5m])",
            "legendFormat": "{{protocol}} - {{file_type}}"
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
- name: network_forensics_alerts
  rules:
  - alert: HighDGADetectionRate
    expr: rate(forensics_dga_candidates_total[5m]) > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High DGA detection rate"
      
  - alert: AnalysisBacklog
    expr: forensics_pcap_analyses_total{status="pending"} > 5
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "PCAP analysis backlog exceeds 5"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestPCAPAnalysis:
    def test_parse_pcap(self, pcap_analyzer):
        result = pcap_analyzer.parse_pcap("test.pcap")
        
        assert result.total_packets > 0
        assert result.duration_seconds > 0
    
    def test_extract_http_sessions(self, pcap_analyzer):
        sessions = pcap_analyzer.extract_http_sessions("test.pcap")
        
        assert len(sessions) >= 0  # May or may not have HTTP sessions
```

### Integration Tests

```python
class TestEndToEndNetworkForensics:
    async def test_pcap_analysis_flow(self, network_forensics_system):
        # Analyze PCAP
        result = await network_forensics_system.analyze_pcap(
            pcap_path="test.pcap",
            case_number="CASE-TEST-001",
        )
        
        assert result.analysis_id is not None
        assert result.total_packets > 0
        
        # Get analysis
        analysis = await network_forensics_system.get_analysis(result.analysis_id)
        assert analysis.analysis_id == result.analysis_id
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class NetworkForensicsUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(5)
    def analyze_pcap(self):
        self.client.post("/api/v1/pcap/analyze", json={
            "pcap_path": f"test_pcap_{self.pcap_counter}.pcap",
            "case_number": f"CASE-{self.pcap_counter}",
        })
        self.pcap_counter += 1
    
    @task(10)
    def get_analysis(self):
        self.client.get(f"/api/v1/pcap/analysis/analysis-{self.analysis_counter}")
        self.analysis_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/pcap/analyze", methods=["POST"])
@app.route("/api/v2/pcap/analyze", methods=["POST"])
async def analyze_pcap():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await analyze_pcap_v2()
    return await analyze_pcap_v1()
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

- **PCAP**: Packet Capture - file format for network traffic
- **NetFlow**: Cisco protocol for IP flow data collection
- **JA3/JA3S**: TLS fingerprinting methods
- **DGA**: Domain Generation Algorithm - malware technique
- **DNS Tunneling**: Covert channel using DNS queries
- **Zeek**: Network security monitor (formerly Bro)
- **Suricata**: Open-source IDS/IPS
- **TCPdump**: Command-line packet analyzer
- **Wireshark**: GUI network protocol analyzer
- **Full Packet Capture**: Complete network traffic recording

## Changelog

### Version 2.0.0 (2026-07-01)
- Added TLS/JA3 fingerprinting
- Implemented DNS tunneling detection
- Enhanced file extraction capabilities
- Added NetFlow analysis

### Version 1.5.0 (2026-01-15)
- Added DGA detection
- Implemented session reconstruction
- Enhanced protocol decoding

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic PCAP analysis
- Protocol decoding

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def analyze_pcap(
    pcap_path: str,
    case_number: str,
) -> PCAPAnalysisResult:
    """Analyze PCAP file.
    
    Args:
        pcap_path: Path to PCAP file.
        case_number: Case identifier.
    
    Returns:
        Analysis result.
    
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

Copyright (c) 2026 Network Forensics Platform

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
