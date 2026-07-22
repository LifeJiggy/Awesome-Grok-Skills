---
name: "Network Debugging"
version: "2.0.0"
description: "Comprehensive network debugging toolkit with packet capture, protocol analysis, latency measurement, DNS debugging, and connection diagnostics for production network troubleshooting"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["debugger", "network", "packet-capture", "protocol-analysis", "latency", "DNS"]
category: "debugger"
personality: "network-engineer"
use_cases: ["packet capture", "protocol analysis", "latency measurement", "DNS debugging", "connection diagnostics"]
---

# Network Debugging

> Production-grade network debugging framework providing packet capture, protocol analysis, latency measurement, DNS debugging, and connection diagnostics for troubleshooting network issues in production environments.

## Overview

The Network Debugging module provides tools for diagnosing network-level issues in distributed systems. It implements packet capture with filter expressions, protocol analysis for HTTP/HTTPS, gRPC, and database connections, latency measurement with percentile breakdowns, DNS resolution debugging, connection pool analysis, and automated network health checks. Every analysis produces actionable reports with root cause identification and remediation steps.

## Core Capabilities

### 1. Packet Capture and Analysis
- Live packet capture with BPF filters
- PCAP file reading and analysis
- Protocol dissection (TCP, UDP, HTTP, TLS)
- Conversation tracking
- Flow analysis

### 2. Protocol Analysis
- HTTP request/response inspection
- TLS handshake analysis
- gRPC message inspection
- Database protocol analysis (MySQL, PostgreSQL, Redis)
- WebSocket frame analysis

### 3. Latency Measurement
- End-to-end latency tracking
- Percentile breakdown (p50, p95, p99)
- Latency distribution analysis
- Jitter measurement
- Correlation with application metrics

### 4. DNS Debugging
- DNS resolution tracing
- DNS cache analysis
- DNSSEC validation
- DNS latency measurement
- DNS failure diagnosis

### 5. Connection Diagnostics
- TCP connection state tracking
- Connection pool utilization
- Connection leak detection
- Keep-alive analysis
- Timeout diagnosis

### 6. Network Health Checks
- Port connectivity testing
- Service discovery verification
- Certificate expiration monitoring
- Bandwidth testing
- MTU path discovery

## Usage Examples

### Packet Capture

```python
from network_debugging import PacketCapture, CaptureFilter

capture = PacketCapture(interface="eth0")

# Start capture with filter
capture.start(
    filter=CaptureFilter(host="192.168.1.100", port=443),
    max_packets=1000,
    duration_seconds=30,
)

# Get results
packets = capture.get_packets()
print(f"Captured {len(packets)} packets")
for pkt in packets[:5]:
    print(f"  {pkt.src_ip}:{pkt.src_port} → {pkt.dst_ip}:{pkt.dst_port} "
          f"({pkt.protocol}, {pkt.size_bytes} bytes, {pkt.timestamp})")
```

### Protocol Analysis

```python
from network_debugging import ProtocolAnalyzer

analyzer = ProtocolAnalyzer()

# Analyze HTTP traffic
http_analysis = analyzer.analyze_http(packets)
print(f"HTTP requests: {http_analysis.request_count}")
print(f"HTTP errors: {http_analysis.error_count}")
print(f"Avg response time: {http_analysis.avg_response_ms:.1f}ms")

print("Top endpoints:")
for endpoint in http_analysis.top_endpoints[:5]:
    print(f"  {endpoint.method} {endpoint.path}: {endpoint.count} requests, "
          f"{endpoint.avg_ms:.1f}ms avg")
```

### Latency Measurement

```python
from network_debugging import LatencyMeasurer

measurer = LatencyMeasurer()

# Measure latency to multiple targets
targets = ["api.example.com:443", "db.example.com:5432", "cache.example.com:6379"]
for target in targets:
    result = measurer.measure(target, count=100)
    print(f"  {target}:")
    print(f"    p50={result.p50_ms:.1f}ms, p95={result.p95_ms:.1f}ms, p99={result.p99_ms:.1f}ms")
    print(f"    Loss: {result.packet_loss_pct:.1f}%, Jitter: {result.jitter_ms:.2f}ms")
```

### DNS Debugging

```python
from network_debugging import DNSDebugger

dns = DNSDebugger()

# Trace DNS resolution
trace = dns.trace("api.example.com")
print(f"DNS trace for {trace.query}:")
for step in trace.steps:
    print(f"  {step.server}: {step.response_code} ({step.latency_ms:.1f}ms)")
    if step.records:
        for record in step.records:
            print(f"    {record.type}: {record.value} (TTL: {record.ttl}s)")
```

### Connection Diagnostics

```python
from network_debugging import ConnectionDiagnostics

diagnostics = ConnectionDiagnostics()

# Check connection pool
pool_status = diagnostics.check_pool(
    host="db.example.com",
    port=5432,
    min_connections=5,
    max_connections=20,
)

print(f"Connection pool:")
print(f"  Active: {pool_status.active}")
print(f"  Idle: {pool_status.idle}")
print(f"  Waiting: {pool_status.waiting}")
print(f"  Leaked: {pool_status.leaked}")
```

## Best Practices

### Packet Capture
- Use specific BPF filters to reduce capture volume
- Limit capture duration in production
- Store captures securely (may contain sensitive data)
- Use ring buffers for continuous capture

### Protocol Analysis
- Decode TLS traffic only when you have the keys
- Focus on error responses and slow requests
- Correlate protocol metrics with application logs
- Monitor for protocol violations

### Latency Measurement
- Measure from multiple vantage points
- Include network and application latency separately
- Track latency percentiles, not just averages
- Correlate latency spikes with system events

### DNS Debugging
- Monitor DNS resolution times as a key metric
- Check DNS cache hit rates
- Verify DNSSEC configuration
- Test from multiple DNS resolvers

## Related Modules

- **dynamic-analysis**: Application-level tracing
- **crash-analysis**: Network-related crash analysis
- **performance-tuning**: Network performance optimization
- **monitoring**: Network monitoring and alerting

---

## Advanced Configuration

### Advanced Packet Capture

```python
from network_debugging import PacketCapture, CaptureFilter, CaptureConfig

capture = PacketCapture(
    interface="eth0",
    config=CaptureConfig(
        buffer_size_mb=64,
        max_packets=100000,
        timeout_seconds=300,
        promiscuous_mode=True,
        snapshot_length=65535,
        ring_buffer_packets=1000000,
    ),
)

# Advanced BPF filter
capture.start(
    filter=CaptureFilter(
        host="192.168.1.0/24",
        port_range=(80, 443),
        protocol="tcp",
        flags=["syn", "ack"],
    ),
    output_file="capture.pcap",
)

# Capture with analysis
capture.start_analysis(
    filter="tcp port 443",
    protocols=["http", "tls", "dns"],
    extract_payloads=True,
    reassemble_tcp=True,
)
```

### Advanced Protocol Analysis

```python
from network_debugging import ProtocolAnalyzer, ProtocolConfig

analyzer = ProtocolAnalyzer(
    config=ProtocolConfig(
        decode_tls=True,
        tls_keylog_file="/path/to/keylog.txt",
        reassemble_http=True,
        parse_json=True,
        extract_headers=True,
        follow_streams=True,
    ),
)

# Analyze HTTP traffic
http_analysis = analyzer.analyze_http(
    packets,
    include_request_body=True,
    include_response_body=True,
    max_body_size=10240,
)

print(f"HTTP requests: {http_analysis.request_count}")
print(f"HTTP errors: {http_analysis.error_count}")
print(f"Avg response time: {http_analysis.avg_response_ms:.1f}ms")

# Analyze TLS handshakes
tls_analysis = analyzer.analyze_tls(packets)
print(f"TLS handshakes: {tls_analysis.handshake_count}")
print(f"Protocol versions: {tls_analysis.protocol_versions}")
print(f"Cipher suites: {tls_analysis.cipher_suites}")
```

### Advanced Latency Measurement

```python
from network_debugging import LatencyMeasurer, LatencyConfig

measurer = LatencyMeasurer(
    config=LatencyConfig(
        probe_count=1000,
        probe_interval_ms=10,
        timeout_ms=5000,
        include_jitter=True,
        include_path_mtu=True,
        include_dns_latency=True,
    ),
)

# Measure latency with detailed analysis
result = measurer.measure_detailed(
    target="api.example.com:443",
    protocol="tcp",
    include_handshake=True,
    include_tls=True,
)

print(f"Connection time: {result.connect_ms:.1f}ms")
print(f"TLS handshake: {result.tls_handshake_ms:.1f}ms")
print(f"First byte: {result.time_to_first_byte_ms:.1f}ms")
print(f"Latency p50: {result.latency_p50_ms:.1f}ms")
print(f"Latency p95: {result.latency_p95_ms:.1f}ms")
print(f"Latency p99: {result.latency_p99_ms:.1f}ms")
print(f"Packet loss: {result.packet_loss_pct:.1f}%")
print(f"Jitter: {result.jitter_ms:.2f}ms")
```

### Advanced DNS Debugging

```python
from network_debugging import DNSDebugger, DNSConfig

dns = DNSDebugger(
    config=DNSConfig(
        resolvers=["8.8.8.8", "1.1.1.1", "9.9.9.9"],
        timeout_seconds=10,
        retry_count=3,
        include_cname=True,
        include_mx=True,
        include_soa=True,
    ),
)

# Comprehensive DNS analysis
analysis = dns.analyze("api.example.com")
print(f"DNS resolution time: {analysis.resolution_ms:.1f}ms")
print(f"Records:")
for record in analysis.records:
    print(f"  {record.type}: {record.value} (TTL: {record.ttl}s)")
print(f"DNSSEC: {analysis.dnssec_valid}")
print(f"Cache status: {analysis.cache_status}")
```

## Architecture Patterns

### Network Debugging Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Network Debugging Architecture                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Capture Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Packet     │  │  Flow       │  │  Stream      │ │   │
│  │  │  Capture    │  │  Capture    │  │  Reassembly  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Protocol Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  HTTP/HTTPS │  │  TLS/SSL    │  │  Database   │ │   │
│  │  │  Parser     │  │  Analyzer   │  │  Protocols  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Analysis Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Latency    │  │  Throughput │  │  Error      │ │   │
│  │  │  Analysis   │  │  Analysis   │  │  Analysis   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Connection State Machine

```
┌─────────────────────────────────────────────────────────────┐
│                  TCP Connection States                      │
├─────────────────────────────────────────────────────────────┤
│  CLOSED ──► LISTEN ──► SYN_SENT ──► SYN_RECEIVED           │
│    │                                             │          │
│    │                                             ▼          │
│    └─────────────────────────────────────► ESTABLISHED      │
│                                              │    │         │
│                                              ▼    ▼         │
│                                    FIN_WAIT_1  CLOSE_WAIT  │
│                                        │          │         │
│                                        ▼          │         │
│                                    FIN_WAIT_2     │         │
│                                        │          │         │
│                                        ▼          ▼         │
│                                    TIME_WAIT   LAST_ACK    │
│                                        │          │         │
│                                        ▼          ▼         │
│                                      CLOSED     CLOSED     │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with FastAPI
from fastapi import FastAPI, Request
from network_debugging import LatencyMeasurer, ConnectionDiagnostics

app = FastAPI()
measurer = LatencyMeasurer()
diagnostics = ConnectionDiagnostics()

@app.middleware("http")
async def network_middleware(request: Request, call_next):
    import time
    
    # Measure network latency
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    # Record metrics
    measurer.record_latency(
        endpoint=request.url.path,
        duration_ms=duration * 1000,
    )
    
    return response

@app.get("/admin/network/diagnostics")
async def get_diagnostics():
    return {
        "dns": diagnostics.check_dns(),
        "connectivity": diagnostics.check_connectivity(),
        "latency": diagnostics.check_latency(),
    }
```

### Prometheus Integration

```python
from prometheus_client import Counter, Histogram, Gauge

NETWORK_LATENCY = Histogram('network_latency_seconds', 'Network latency', ['endpoint'])
NETWORK_ERRORS = Counter('network_errors_total', 'Network errors', ['type'])
CONNECTION_POOL = Gauge('network_connection_pool', 'Connection pool', ['state'])

class NetworkMetrics:
    def __init__(self, measurer: LatencyMeasurer):
        self.measurer = measurer
    
    def record_latency(self, endpoint: str, latency: float):
        NETWORK_LATENCY.labels(endpoint=endpoint).observe(latency)
    
    def record_error(self, error_type: str):
        NETWORK_ERRORS.labels(type=error_type).inc()
```

## Performance Optimization

### Network Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Latency p95 | < 100ms | 100-500ms | > 500ms |
| Packet loss | < 0.1% | 0.1-1% | > 1% |
| DNS resolution | < 50ms | 50-200ms | > 200ms |
| Connection time | < 50ms | 50-200ms | > 200ms |
| TLS handshake | < 100ms | 100-300ms | > 300ms |

### Optimized Packet Capture

```python
from network_debugging import OptimizedCapture

capture = OptimizedCapture()

# Configure for minimal overhead
capture.configure(
    ring_buffer_size=100000,
    snapshot_length=96,  # Headers only
    bpf_filter="tcp port 443",
    zero_copy=True,
    timestamp_type="adapter_unsynced",
)

# Capture with filtering
capture.start(
    protocols=["http", "tls"],
    exclude_broadcast=True,
    max_payload_size=256,
)
```

## Security Considerations

### Sensitive Data in Captures

```python
from network_debugging import CaptureSanitizer

sanitizer = CaptureSanitizer()

# Configure sanitization
sanitizer.configure(
    # Redact sensitive headers
    redact_headers=["Authorization", "Cookie", "X-Api-Key"],
    
    # Redact sensitive query params
    redact_params=["password", "token", "secret"],
    
    # Redact request/response bodies
    redact_body_patterns=[
        r'"password":\s*"[^"]*"',
        r'"token":\s*"[^"]*"',
        r'"secret":\s*"[^"]*"',
    ],
    
    # Mask IP addresses
    mask_ips=True,
    mask_ip_octets=2,  # 192.168.x.x
)

# Sanitize capture
sanitized = sanitizer.sanitize(capture)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| High latency | Slow responses | Check network path, DNS, TLS |
| Connection refused | Cannot connect | Check firewall, service status |
| DNS resolution slow | Delayed connections | Use local resolver, check DNS cache |
| TLS handshake slow | Slow HTTPS | Check certificate, cipher suite |
| Packet loss | Retransmissions | Check network quality, MTU |

### Diagnostic Commands

```bash
# Check network connectivity
ping -c 10 api.example.com

# Check DNS resolution
dig api.example.com +trace

# Check TLS certificate
openssl s_client -connect api.example.com:443

# Check route
traceroute api.example.com

# Check ports
nc -zv api.example.com 443
```

## API Reference

### PacketCapture

```python
class PacketCapture:
    def __init__(self, interface: str, config: CaptureConfig = None)
    def start(self, filter: str = None, duration_seconds: int = None)
    def stop(self) -> CaptureResult
    def get_packets(self) -> list[Packet]
    def export_pcap(self, filename: str)
    def get_statistics(self) -> CaptureStats
```

### ProtocolAnalyzer

```python
class ProtocolAnalyzer:
    def __init__(self, config: ProtocolConfig = None)
    def analyze_http(self, packets: list[Packet], **kwargs) -> HTTPAnalysis
    def analyze_tls(self, packets: list[Packet]) -> TLSAnalysis
    def analyze_dns(self, packets: list[Packet]) -> DNSAnalysis
    def analyze_database(self, packets: list[Packet], protocol: str) -> DatabaseAnalysis
    def get_conversations(self) -> list[Conversation]
```

### LatencyMeasurer

```python
class LatencyMeasurer:
    def __init__(self, config: LatencyConfig = None)
    def measure(self, target: str, count: int = 100) -> LatencyResult
    def measure_detailed(self, target: str, **kwargs) -> DetailedLatency
    def measure_path(self, target: str) -> PathAnalysis
    def record_latency(self, endpoint: str, duration_ms: float)
    def get_statistics(self, endpoint: str = None) -> LatencyStats
```

### DNSDebugger

```python
class DNSDebugger:
    def __init__(self, config: DNSConfig = None)
    def trace(self, hostname: str) -> DNSTrace
    def analyze(self, hostname: str) -> DNSAnalysis
    def check_cache(self, hostname: str) -> CacheStatus
    def measure_latency(self, hostname: str, resolver: str = None) -> float
    def validate_dnssec(self, hostname: str) -> DNSSECResult
```

### ConnectionDiagnostics

```python
class ConnectionDiagnostics:
    def __init__(self)
    def check_pool(self, host: str, port: int, **kwargs) -> PoolStatus
    def check_connectivity(self, host: str, port: int) -> ConnectivityResult
    def check_tls(self, host: str, port: int) -> TLSResult
    def check_dns(self, hostname: str = None) -> DNSResult
    def get_connection_states(self) -> dict[str, int]
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    HTTP = "http"
    HTTPS = "https"
    DNS = "dns"

@dataclass
class Packet:
    timestamp: datetime
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: Protocol
    size_bytes: int
    payload: Optional[bytes]
    flags: List[str]

@dataclass
class LatencyResult:
    target: str
    p50_ms: float
    p95_ms: float
    p99_ms: float
    min_ms: float
    max_ms: float
    avg_ms: float
    packet_loss_pct: float
    jitter_ms: float

@dataclass
class Connection:
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    state: str
    bytes_sent: int
    bytes_received: int
    duration_ms: float
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  network-debugger:
    image: network-debugger:latest
    cap_add:
      - NET_ADMIN
      - NET_RAW
    network_mode: host
    environment:
      INTERFACE: eth0
      CAPTURE_FILTER: "tcp port 443"
    volumes:
      - ./captures:/captures
```

## Monitoring & Observability

### Metrics Collection

```python
from network_debugging import MetricsCollector

collector = MetricsCollector()

# Collect network metrics
collector.histogram("network.latency.seconds", latency, tags={"endpoint": endpoint})
collector.counter("network.packets.captured", count, tags={"protocol": protocol})
collector.counter("network.errors.total", count, tags={"type": error_type})
collector.gauge("network.connections.active", count)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from network_debugging import LatencyMeasurer, DNSDebugger

@pytest.fixture
def measurer():
    return LatencyMeasurer()

def test_latency_measurement(measurer):
    result = measurer.measure("localhost:80", count=10)
    assert result.p50_ms > 0

def test_dns_trace():
    dns = DNSDebugger()
    trace = dns.trace("example.com")
    assert len(trace.steps) > 0
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |
| libpcap | 1.0 | 1.10+ |

## Glossary

| Term | Definition |
|------|------------|
| **BPF** | Berkeley Packet Filter |
| **RTT** | Round-Trip Time |
| **TTL** | Time To Live |
| **MTU** | Maximum Transmission Unit |
| **SYN** | Synchronize (TCP flag) |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added TLS analysis
- New DNS debugging
- Improved latency measurement
- Added connection diagnostics

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/network-debugging.git
cd network-debugging
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills