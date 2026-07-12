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