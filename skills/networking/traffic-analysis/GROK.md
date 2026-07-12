---
name: traffic-analysis
category: networking
version: 2.0.0
tags: [networking, traffic-analysis, packet-capture, flow-monitoring, netflow]
---

# Traffic Analysis

## Overview

Network traffic analysis toolkit covering packet capture processing, flow analysis (NetFlow/IPFIX/sFlow), bandwidth monitoring, protocol identification, anomaly detection, and traffic classification. This skill provides tools for deep packet inspection, traffic pattern analysis, and network forensics for understanding and optimizing network usage.

## Core Capabilities

- **Packet Analysis**: PCAP parsing, protocol dissection, header extraction
- **Flow Analysis**: NetFlow v5/v9, IPFIX, and sFlow record processing
- **Bandwidth Monitoring**: Interface utilization, per-host bandwidth, protocol breakdown
- **Protocol Detection**: Deep packet inspection, application-layer protocol identification
- **Anomaly Detection**: Unusual traffic patterns, spike detection, DDoS identification
- **Traffic Classification**: QoS tagging, application identification, user-agent analysis
- **Geolocation**: IP-to-location mapping for traffic origin analysis
- **Reporting**: Traffic summaries, top talkers, protocol distribution charts

## Usage Examples

```python
import struct
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from enum import Enum

class Protocol(Enum):
    TCP = 6
    UDP = 17
    ICMP = 1
    HTTP = 80
    HTTPS = 443
    DNS = 53
    SSH = 22
    SMTP = 25
    UNKNOWN = 0

@dataclass
class Packet:
    timestamp: float
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: int
    size: int
    flags: str = ""
    payload_preview: str = ""

    @property
    def protocol_name(self) -> str:
        port_map = {80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH", 25: "SMTP"}
        return port_map.get(self.dst_port, Protocol(self.protocol).name if self.protocol in [p.value for p in Protocol] else "OTHER")

@dataclass
class FlowRecord:
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: int
    packets: int = 0
    bytes_sent: int = 0
    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    @property
    def bytes_per_second(self) -> float:
        return self.bytes_sent / self.duration if self.duration > 0 else 0

@dataclass
class TrafficStats:
    total_packets: int = 0
    total_bytes: int = 0
    unique_src_ips: int = 0
    unique_dst_ips: int = 0
    protocol_distribution: Dict[str, int] = field(default_factory=dict)
    top_sources: List[Tuple[str, int]] = field(default_factory=list)
    top_destinations: List[Tuple[str, int]] = field(default_factory=list)
    avg_packet_size: float = 0.0
    duration: float = 0.0

class PacketAnalyzer:
    def __init__(self):
        self._packets: List[Packet] = []

    def add_packet(self, packet: Packet):
        self._packets.append(packet)

    def get_protocol_distribution(self) -> Dict[str, int]:
        dist: Dict[str, int] = defaultdict(int)
        for p in self._packets:
            dist[p.protocol_name] += 1
        return dict(dist)

    def get_top_talkers(self, n: int = 10) -> List[Tuple[str, int]]:
        src_bytes: Dict[str, int] = defaultdict(int)
        for p in self._packets:
            src_bytes[p.src_ip] += p.size
        return sorted(src_bytes.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_top_destinations(self, n: int = 10) -> List[Tuple[str, int]]:
        dst_bytes: Dict[str, int] = defaultdict(int)
        for p in self._packets:
            dst_bytes[p.dst_ip] += p.size
        return sorted(dst_bytes.items(), key=lambda x: x[1], reverse=True)[:n]

    def detect_anomalies(self, threshold: float = 3.0) -> List[Dict]:
        anomalies = []
        if len(self._packets) < 10:
            return anomalies
        sizes = [p.size for p in self._packets]
        mean_size = sum(sizes) / len(sizes)
        std_size = (sum((s - mean_size) ** 2 for s in sizes) / len(sizes)) ** 0.5

        for i, p in enumerate(self._packets):
            if std_size > 0 and abs(p.size - mean_size) > threshold * std_size:
                anomalies.append({
                    "index": i, "src_ip": p.src_ip, "dst_ip": p.dst_ip,
                    "size": p.size, "deviation": (p.size - mean_size) / std_size,
                })
        return anomalies

    def get_statistics(self) -> TrafficStats:
        if not self._packets:
            return TrafficStats()
        src_ips = set(p.src_ip for p in self._packets)
        dst_ips = set(p.dst_ip for p in self._packets)
        protocol_dist = self.get_protocol_distribution()
        total_bytes = sum(p.size for p in self._packets)
        return TrafficStats(
            total_packets=len(self._packets),
            total_bytes=total_bytes,
            unique_src_ips=len(src_ips),
            unique_dst_ips=len(dst_ips),
            protocol_distribution=protocol_dist,
            top_sources=self.get_top_talkers(5),
            top_destinations=self.get_top_destinations(5),
            avg_packet_size=total_bytes / len(self._packets),
            duration=self._packets[-1].timestamp - self._packets[0].timestamp if len(self._packets) > 1 else 0,
        )

class FlowCollector:
    def __init__(self):
        self._flows: Dict[str, FlowRecord] = {}
        self._active_timeout: float = 300
        self._inactive_timeout: float = 15

    def _flow_key(self, src_ip: str, dst_ip: str, src_port: int, dst_port: int, proto: int) -> str:
        return f"{src_ip}:{src_port}-{dst_ip}:{dst_port}-{proto}"

    def process_packet(self, packet: Packet):
        key = self._flow_key(packet.src_ip, packet.dst_ip, packet.src_port, packet.dst_port, packet.protocol)
        if key in self._flows:
            flow = self._flows[key]
            flow.packets += 1
            flow.bytes_sent += packet.size
            flow.end_time = packet.timestamp
        else:
            self._flows[key] = FlowRecord(
                src_ip=packet.src_ip, dst_ip=packet.dst_ip,
                src_port=packet.src_port, dst_port=packet.dst_port,
                protocol=packet.protocol, packets=1, bytes_sent=packet.size,
                start_time=packet.timestamp, end_time=packet.timestamp,
            )

    def get_flows(self) -> List[FlowRecord]:
        return list(self._flows.values())

    def get_top_flows(self, n: int = 10) -> List[FlowRecord]:
        return sorted(self._flows.values(), key=lambda f: f.bytes_sent, reverse=True)[:n]

    def get_summary(self) -> Dict:
        flows = list(self._flows.values())
        return {
            "total_flows": len(flows),
            "total_bytes": sum(f.bytes_sent for f in flows),
            "avg_flow_duration": sum(f.duration for f in flows) / len(flows) if flows else 0,
        }

class TrafficClassifier:
    KNOWN_PORTS = {80: "Web", 443: "Web-Secure", 53: "DNS", 22: "SSH", 25: "SMTP",
                   110: "POP3", 143: "IMAP", 993: "IMAPS", 995: "POP3S",
                   3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB"}

    def classify(self, packet: Packet) -> str:
        if packet.dst_port in self.KNOWN_PORTS:
            return self.KNOWN_PORTS[packet.dst_port]
        if packet.src_port in self.KNOWN_PORTS:
            return self.KNOWN_PORTS[packet.src_port]
        if packet.protocol == Protocol.ICMP.value:
            return "ICMP"
        return "Other"

    def classify_flow(self, flow: FlowRecord) -> str:
        return self.classify(Packet(0, flow.src_ip, flow.dst_ip, flow.src_port, flow.dst_port, flow.protocol, 0))
```

## Best Practices

- Use flow-based analysis (NetFlow/IPFIX) for large networks instead of full packet capture
- Set appropriate capture filters to reduce storage requirements
- Implement rolling capture buffers to prevent disk exhaustion
- Use protocol dissectors for accurate application identification
- Monitor baseline traffic patterns to detect anomalies effectively
- Aggregate similar flows to reduce analysis complexity
- Implement geographic IP mapping for international traffic analysis
- Use time-bucketed analysis for traffic trending and capacity planning
- Correlate DNS queries with subsequent connections for attribution
- Retain packet captures according to compliance requirements

## Related Modules

- `network-engineering` - Network infrastructure management
- `load-balancing` - Traffic distribution
- `sdn` - Software-defined networking
- `dns-management` - DNS infrastructure
