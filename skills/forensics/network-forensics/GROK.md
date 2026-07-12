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
