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

## Advanced Configuration

### NetFlow v9 Template Configuration

NetFlow v9 uses templates to define the structure of flow records, allowing flexible field definitions.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import struct
import time

@dataclass
class NetFlowTemplate:
    template_id: int
    fields: List[Dict[str, int]]
    count: int = 0
    timeout: int = 1800

    def to_bytes(self) -> bytes:
        header = struct.pack("!HHI", self.template_id, self.count, self.timeout)
        field_bytes = b""
        for field_def in self.fields:
            for field_type, field_length in field_def.items():
                field_bytes += struct.pack("!HH", field_type, field_length)
        return header + field_bytes

    @classmethod
    def from_bytes(cls, data: bytes, template_id: int) -> "NetFlowTemplate":
        count = struct.unpack("!H", data[2:4])[0]
        timeout = struct.unpack("!I", data[4:8])[0]
        fields = []
        offset = 8
        for _ in range(count):
            field_type = struct.unpack("!H", data[offset:offset+2])[0]
            field_length = struct.unpack("!H", data[offset+2:offset+4])[0]
            fields.append({field_type: field_length})
            offset += 4
        return cls(template_id=template_id, fields=fields, count=count, timeout=timeout)


class NetFlowV9Collector:
    TEMPLATE_FIELD_TYPES = {
        1: ("src_ipv4", 4),
        2: ("src_port", 2),
        3: ("proto", 1),
        4: ("tos", 1),
        5: ("tcp_flags", 1),
        6: ("src_as", 2),
        7: ("src_mask", 1),
        8: ("input_snmp", 2),
        10: ("packets", 4),
        11: ("octets", 4),
        14: ("src_vlan", 2),
        21: ("dst_ipv4", 4),
        22: ("dst_port", 2),
        29: ("dst_as", 2),
        30: ("dst_mask", 1),
        31: ("output_snmp", 2),
        54: ("dst_vlan", 2),
        56: ("src_mac", 6),
        57: ("dst_mac", 6),
        59: ("engine_type", 1),
        60: ("engine_id", 1),
        61: ("sampling_interval", 2),
        136: ("flow_sampler_id", 1),
        148: ("flow_id", 4),
        150: ("engine_type_ext", 1),
        152: ("flow_start_seconds", 4),
        153: ("flow_end_seconds", 4),
        154: ("flow_start_milliseconds", 4),
        155: ("flow_end_milliseconds", 4),
    }

    def __init__(self, buffer_size: int = 65535):
        self.buffer_size = buffer_size
        self.templates: Dict[int, NetFlowTemplate] = {}
        self._flow_buffer: List[Dict] = []
        self._packet_count: int = 0
        self._sequence: int = 0

    def process_template(self, template_id: int, data: bytes):
        template = NetFlowTemplate.from_bytes(data, template_id)
        self.templates[template_id] = template

    def parse_flow_set(self, template_id: int, data: bytes) -> List[Dict]:
        template = self.templates.get(template_id)
        if not template:
            return []
        flows = []
        offset = 0
        record_size = sum(list(f.values())[0] for f in template.fields)
        while offset + record_size <= len(data):
            flow = {}
            for field_def in template.fields:
                for field_type, field_length in field_def.items():
                    if field_type in self.TEMPLATE_FIELD_TYPES:
                        name, expected_len = self.TEMPLATE_FIELD_TYPES[field_type]
                        if field_length == 4:
                            value = struct.unpack("!I", data[offset:offset+4])[0]
                        elif field_length == 2:
                            value = struct.unpack("!H", data[offset:offset+2])[0]
                        elif field_length == 1:
                            value = data[offset]
                        else:
                            value = data[offset:offset+field_length].hex()
                        flow[name] = value
                    offset += field_length
            flows.append(flow)
        return flows

    def get_statistics(self) -> Dict:
        return {
            "packet_count": self._packet_count,
            "template_count": len(self.templates),
            "flow_buffer_size": len(self._flow_buffer),
            "active_templates": list(self.templates.keys()),
        }
```

### sFlow Configuration

```python
@dataclass
class SFlowSample:
    sequence: int
    source_id: int
    rate: int
    drop_events: int
    input_interface: int
    output_interface: int
    samples: List[Dict] = field(default_factory=list)

class SFlowCollector:
    def __init__(self, port: int = 6343):
        self.port = port
        self._samples: List[SFlowSample] = []
        self._enterprise_map: Dict[int, str] = {
            0: "Packet Header",
            1: "Extended Switch",
            2: "Extended Router",
            3: "Extended Gateway",
            4: "Extended Host",
            5: "Extended LAN/TAG",
        }

    def parse_datagram(self, data: bytes) -> Dict:
        version = struct.unpack("!I", data[0:4])[0]
        ip_version = struct.unpack("!I", data[4:8])[0]
        agent_ip = struct.unpack("!I", data[8:12])[0]
        sub_agent_id = struct.unpack("!I", data[12:16])[0]
        sequence = struct.unpack("!I", data[16:20])[0]
        uptime = struct.unpack("!I", data[20:24])[0]
        num_samples = struct.unpack("!I", data[24:28])[0]

        sample = SFlowSample(
            sequence=sequence,
            source_id=sub_agent_id,
            rate=0,
            drop_events=0,
            input_interface=0,
            output_interface=0,
        )

        offset = 28
        for _ in range(num_samples):
            if offset + 8 > len(data):
                break
            sample_type = struct.unpack("!I", data[offset:offset+4])[0]
            sample_length = struct.unpack("!I", data[offset+4:offset+8])[0]
            enterprise = sample_type >> 12
            format_type = sample_type & 0xFFF
            sample_info = self._parse_sample(data[offset+8:offset+8+sample_length], enterprise, format_type)
            sample.samples.append(sample_info)
            offset += 8 + sample_length

        self._samples.append(sample)
        return {
            "version": version,
            "agent_ip": f"{(agent_ip >> 24) & 0xFF}.{(agent_ip >> 16) & 0xFF}.{(agent_ip >> 8) & 0xFF}.{agent_ip & 0xFF}",
            "sequence": sequence,
            "num_samples": num_samples,
        }

    def _parse_sample(self, data: bytes, enterprise: int, format_type: int) -> Dict:
        if enterprise == 0 and format_type == 1:
            protocol = struct.unpack("!I", data[0:4])[0]
            length = struct.unpack("!I", data[4:8])[0]
            header = data[8:8+min(length, len(data)-8)]
            return {"type": "packet_header", "protocol": protocol, "header_length": len(header)}
        elif enterprise == 0 and format_type == 3:
            seq = struct.unpack("!I", data[0:4])[0]
            rate = struct.unpack("!I", data[4:8])[0]
            drops = struct.unpack("!I", data[8:12])[0]
            return {"type": "flow_sample", "sequence": seq, "rate": rate, "drops": drops}
        return {"type": "unknown", "enterprise": enterprise, "format": format_type}

    def get_summary(self) -> Dict:
        total_samples = sum(len(s.samples) for s in self._samples)
        return {
            "datagrams_received": len(self._samples),
            "total_samples": total_samples,
            "unique_sources": len(set(s.source_id for s in self._samples)),
        }
```

### Deep Packet Inspection Engine

```python
import re
from typing import Dict, List, Tuple, Optional

class DeepPacketInspector:
    PROTOCOL_SIGNATURES = {
        "HTTP": [b"GET ", b"POST ", b"PUT ", b"DELETE ", b"HTTP/1.", b"Host:"],
        "HTTPS": [b"\x16\x03"],  # TLS ClientHello
        "DNS": [],  # Port-based detection
        "SSH": [b"SSH-2.0", b"SSH-1."],
        "SMTP": [b"220 ", b"EHLO", b"MAIL FROM:"],
        "FTP": [b"220 FTP", b"USER ", b"PASS "],
        "IRC": [b"NICK ", b"JOIN #", b"PRIVMSG"],
        "BitTorrent": [b"\x13BitTorrent protocol"],
        "Tor": [b"\x15\x00\x00\x00\x00\x00\x02"],
        "OpenVPN": [b"\x00\x0e\x38"],
    }

    def __init__(self):
        self._detected_protocols: Dict[str, int] = {}
        self._inspection_results: List[Dict] = []

    def inspect_payload(self, payload: bytes, src_port: int = 0, dst_port: int = 0) -> Dict:
        result = {
            "detected_protocol": "Unknown",
            "confidence": 0.0,
            "signatures_matched": [],
            "metadata": {},
        }

        port_protocol_map = {
            80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH", 25: "SMTP",
            21: "FTP", 110: "POP3", 143: "IMAP", 993: "IMAPS", 995: "POP3S",
            3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt", 6667: "IRC",
        }

        if dst_port in port_protocol_map:
            result["detected_protocol"] = port_protocol_map[dst_port]
            result["confidence"] = 0.7

        for proto, signatures in self.PROTOCOL_SIGNATURES.items():
            for sig in signatures:
                if payload[:len(sig)] == sig:
                    result["detected_protocol"] = proto
                    result["confidence"] = 0.95
                    result["signatures_matched"].append(sig.hex())
                    break

        if result["detected_protocol"] == "HTTP" and len(payload) > 0:
            try:
                header_end = payload.find(b"\r\n\r\n")
                if header_end > 0:
                    headers = payload[:header_end].decode("utf-8", errors="ignore")
                    result["metadata"]["headers"] = headers.split("\r\n")[:10]
            except Exception:
                pass

        if result["detected_protocol"] == "Unknown" and len(payload) > 0:
            entropy = self._calculate_entropy(payload)
            result["metadata"]["entropy"] = entropy
            if entropy > 7.5:
                result["metadata"]["note"] = "High entropy - possible encrypted or compressed data"

        self._detected_protocols[result["detected_protocol"]] = \
            self._detected_protocols.get(result["detected_protocol"], 0) + 1
        self._inspection_results.append(result)
        return result

    def _calculate_entropy(self, data: bytes) -> float:
        import math
        if not data:
            return 0.0
        freq = [0] * 256
        for byte in data:
            freq[byte] += 1
        entropy = 0.0
        for count in freq:
            if count > 0:
                p = count / len(data)
                entropy -= p * math.log2(p)
        return entropy

    def get_protocol_stats(self) -> Dict[str, int]:
        return dict(self._detected_protocols)

    def detect_application(self, payload: bytes) -> Dict:
        result = self.inspect_payload(payload)
        app_hints = {
            "HTTP": self._extract_http_info(payload),
            "DNS": self._extract_dns_info(payload),
            "TLS": self._extract_tls_info(payload),
        }
        if result["detected_protocol"] in app_hints:
            result["metadata"].update(app_hints[result["detected_protocol"]])
        return result

    def _extract_http_info(self, payload: bytes) -> Dict:
        try:
            text = payload.decode("utf-8", errors="ignore")
            lines = text.split("\r\n")
            if lines:
                first_line = lines[0].split(" ")
                return {"method": first_line[0], "path": first_line[1] if len(first_line) > 1 else ""}
        except Exception:
            pass
        return {}

    def _extract_dns_info(self, payload: bytes) -> Dict:
        if len(payload) < 12:
            return {}
        return {"query_id": struct.unpack("!H", payload[0:2])[0]}

    def _extract_tls_info(self, payload: bytes) -> Dict:
        if len(payload) < 5:
            return {}
        content_type = payload[0]
        version = struct.unpack("!H", payload[1:3])[0]
        version_map = {0x0301: "TLS 1.0", 0x0302: "TLS 1.1", 0x0303: "TLS 1.2/1.3"}
        return {"content_type": content_type, "version": version_map.get(version, f"0x{version:04x}")}
```

## Architecture Patterns

### Distributed Traffic Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    Traffic Analysis Architecture                 │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Probe   │───▶│  Kafka   │───▶│  Flink   │───▶│  Redis   │ │
│  │  (Mirror)│    │  (Buffer)│    │  (Stream)│    │  (Cache) │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │                               │                │        │
│       │                               ▼                ▼        │
│       │                         ┌──────────┐    ┌──────────┐  │
│       │                         │  Click   │    │  Grafana │  │
│       │                         │  House   │    │  (Dash)  │  │
│       │                         └──────────┘    └──────────┘  │
│       │                                                        │
│  ┌──────────┐                                                  │
│  │  pcap    │───▶ File-based batch analysis                    │
│  │  storage │                                                  │
│  └──────────┘                                                  │
└─────────────────────────────────────────────────────────────────┘
```

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from collections import defaultdict
from enum import Enum
import time
import threading

class ProcessingMode(Enum):
    REALTIME = "realtime"
    BATCH = "batch"
    HYBRID = "hybrid"

@dataclass
class AnalysisPipeline:
    name: str
    mode: ProcessingMode = ProcessingMode.REALTIME
    stages: List[Dict] = field(default_factory=list)
    buffer_size: int = 10000
    flush_interval: int = 60

class TrafficAnalysisOrchestrator:
    def __init__(self):
        self.pipelines: Dict[str, AnalysisPipeline] = {}
        self._processors: Dict[str, Callable] = {}
        self._buffer: Dict[str, List] = defaultdict(list)
        self._lock = threading.Lock()
        self._running = False

    def register_pipeline(self, pipeline: AnalysisPipeline):
        self.pipelines[pipeline.name] = pipeline

    def register_processor(self, stage_name: str, processor: Callable):
        self._processors[stage_name] = processor

    def process_packet(self, pipeline_name: str, packet: Dict):
        pipeline = self.pipelines.get(pipeline_name)
        if not pipeline:
            return
        with self._lock:
            self._buffer[pipeline_name].append(packet)
            if len(self._buffer[pipeline_name]) >= pipeline.buffer_size:
                self._flush_pipeline(pipeline_name)

    def _flush_pipeline(self, pipeline_name: str):
        pipeline = self.pipelines[pipeline_name]
        data = self._buffer[pipeline_name][:]
        self._buffer[pipeline_name] = []
        result = data
        for stage in pipeline.stages:
            processor = self._processors.get(stage["name"])
            if processor:
                result = processor(result)
        return result

    def get_stats(self) -> Dict:
        stats = {}
        for name, pipeline in self.pipelines.items():
            stats[name] = {
                "mode": pipeline.mode.value,
                "buffered": len(self._buffer[name]),
                "stages": len(pipeline.stages),
            }
        return stats
```

### Multi-Layer Analysis Framework

```python
class MultiLayerAnalyzer:
    def __init__(self):
        self.layers = {
            "l2_data_link": {"name": "Data Link", "analyzers": []},
            "l3_network": {"name": "Network", "analyzers": []},
            "l4_transport": {"name": "Transport", "analyzers": []},
            "l7_application": {"name": "Application", "analyzers": []},
        }

    def add_analyzer(self, layer: str, analyzer: Callable):
        if layer in self.layers:
            self.layers[layer]["analyzers"].append(analyzer)

    def analyze_packet(self, packet: Dict) -> Dict:
        results = {}
        for layer_name, layer_config in self.layers.items():
            layer_results = []
            for analyzer in layer_config["analyzers"]:
                try:
                    result = analyzer(packet)
                    layer_results.append(result)
                except Exception as e:
                    layer_results.append({"error": str(e)})
            results[layer_name] = layer_results
        return results

    def get_layer_summary(self) -> Dict:
        return {
            name: {"name": config["name"], "analyzer_count": len(config["analyzers"])}
            for name, config in self.layers.items()
        }


class L2Analyzer:
    def analyze(self, packet: Dict) -> Dict:
        src_mac = packet.get("src_mac", "")
        dst_mac = packet.get("dst_mac", "")
        vlan_id = packet.get("vlan_id", 0)
        return {
            "layer": "L2",
            "src_mac": src_mac,
            "dst_mac": dst_mac,
            "vlan_id": vlan_id,
            "broadcast": dst_mac == "ff:ff:ff:ff:ff:ff",
            "multicast": dst_mac.startswith("01:00:5e"),
        }


class L3Analyzer:
    def analyze(self, packet: Dict) -> Dict:
        src_ip = packet.get("src_ip", "")
        dst_ip = packet.get("dst_ip", "")
        protocol = packet.get("protocol", 0)
        tos = packet.get("tos", 0)
        return {
            "layer": "L3",
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol,
            "dscp": (tos >> 2) & 0x3F,
            "ecn": tos & 0x03,
            "fragmented": packet.get("flags", 0) & 0x2000 != 0,
        }


class L4Analyzer:
    def analyze(self, packet: Dict) -> Dict:
        src_port = packet.get("src_port", 0)
        dst_port = packet.get("dst_port", 0)
        protocol = packet.get("protocol", 0)
        tcp_flags = packet.get("tcp_flags", 0)
        return {
            "layer": "L4",
            "src_port": src_port,
            "dst_port": dst_port,
            "is_syn": bool(tcp_flags & 0x02),
            "is_ack": bool(tcp_flags & 0x10),
            "is_fin": bool(tcp_flags & 0x01),
            "is_rst": bool(tcp_flags & 0x04),
            "connection_start": bool(tcp_flags & 0x02) and not bool(tcp_flags & 0x10),
        }


class L7Analyzer:
    WELL_KNOWN_PORTS = {
        80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH", 25: "SMTP",
        110: "POP3", 143: "IMAP", 3306: "MySQL", 5432: "PostgreSQL",
        6379: "Redis", 27017: "MongoDB", 8080: "HTTP-Proxy",
    }

    def analyze(self, packet: Dict) -> Dict:
        dst_port = packet.get("dst_port", 0)
        src_port = packet.get("src_port", 0)
        application = self.WELL_KNOWN_PORTS.get(dst_port,
                    self.WELL_KNOWN_PORTS.get(src_port, "Unknown"))
        return {
            "layer": "L7",
            "application": application,
            "dst_port": dst_port,
            "src_port": src_port,
            "is_database": application in ["MySQL", "PostgreSQL", "Redis", "MongoDB"],
            "is_web": application in ["HTTP", "HTTPS", "HTTP-Proxy"],
        }
```

### Network Segmentation Analyzer

```python
@dataclass
class NetworkSegment:
    name: str
    cidr: str
    vlan_id: int
    zone: str  # internal, dmz, external
    allowed_protocols: List[str] = field(default_factory=list)

class SegmentationAnalyzer:
    def __init__(self):
        self.segments: List[NetworkSegment] = []
        self.violations: List[Dict] = []

    def add_segment(self, segment: NetworkSegment):
        self.segments.append(segment)

    def check_flow(self, flow: Dict) -> Dict:
        src_ip = flow.get("src_ip", "")
        dst_ip = flow.get("dst_ip", "")
        protocol = flow.get("protocol", "unknown")
        src_segment = self._find_segment(src_ip)
        dst_segment = self._find_segment(dst_ip)

        result = {
            "src_segment": src_segment.name if src_segment else "unknown",
            "dst_segment": dst_segment.name if dst_segment else "unknown",
            "cross_segment": src_segment != dst_segment and src_segment and dst_segment,
            "allowed": True,
        }

        if result["cross_segment"] and dst_segment:
            if dst_segment.allowed_protocols and protocol not in dst_segment.allowed_protocols:
                result["allowed"] = False
                self.violations.append({
                    "src_ip": src_ip, "dst_ip": dst_ip,
                    "protocol": protocol,
                    "src_segment": src_segment.name if src_segment else "unknown",
                    "dst_segment": dst_segment.name,
                })

        return result

    def _find_segment(self, ip: str) -> Optional[NetworkSegment]:
        from ipaddress import ip_address, ip_network
        try:
            addr = ip_address(ip)
            for segment in self.segments:
                if addr in ip_network(segment.cidr):
                    return segment
        except ValueError:
            pass
        return None

    def get_violation_report(self) -> Dict:
        return {
            "total_violations": len(self.violations),
            "unique_sources": len(set(v["src_ip"] for v in self.violations)),
            "unique_destinations": len(set(v["dst_ip"] for v in self.violations)),
            "violations": self.violations[-100:],
        }
```

## Integration Guide

### Elasticsearch Integration

```python
from typing import Dict, List
import json

class ElasticsearchTrafficIndexer:
    def __init__(self, index_name: str = "traffic-"):
        self.index_name = index_name
        self._buffer: List[Dict] = []
        self._batch_size: int = 1000

    def index_flow(self, flow: Dict):
        doc = {
            "src_ip": flow.get("src_ip"),
            "dst_ip": flow.get("dst_ip"),
            "src_port": flow.get("src_port"),
            "dst_port": flow.get("dst_port"),
            "protocol": flow.get("protocol"),
            "bytes": flow.get("bytes_sent", 0),
            "packets": flow.get("packets", 0),
            "duration": flow.get("duration", 0),
            "timestamp": flow.get("timestamp", time.time()),
        }
        self._buffer.append(doc)
        if len(self._buffer) >= self._batch_size:
            self._flush()

    def _flush(self):
        if not self._buffer:
            return
        bulk_body = ""
        for doc in self._buffer:
            bulk_body += json.dumps({"index": {"_index": self.index_name}}) + "\n"
            bulk_body += json.dumps(doc) + "\n"
        self._buffer = []

    def get_aggregation_query(self, field: str, size: int = 10) -> Dict:
        return {
            "size": 0,
            "aggs": {
                f"top_{field}": {
                    "terms": {
                        "field": field,
                        "size": size,
                    }
                }
            }
        }

    def get_time_series_query(self, interval: str = "1h") -> Dict:
        return {
            "size": 0,
            "aggs": {
                "traffic_over_time": {
                    "date_histogram": {
                        "field": "timestamp",
                        "fixed_interval": interval,
                    },
                    "aggs": {
                        "total_bytes": {"sum": {"field": "bytes"}},
                        "unique_sources": {"cardinality": {"field": "src_ip"}},
                    }
                }
            }
        }
```

### Prometheus Metrics Exporter

```python
class PrometheusTrafficExporter:
    def __init__(self):
        self.metrics: Dict[str, float] = {}
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = {}

    def inc_counter(self, name: str, value: float = 1.0, labels: Dict[str, str] = None):
        key = self._make_key(name, labels)
        self._counters[key] = self._counters.get(key, 0) + value

    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        key = self._make_key(name, labels)
        self._gauges[key] = value

    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        key = self._make_key(name, labels)
        if key not in self._histograms:
            self._histograms[key] = []
        self._histograms[key].append(value)

    def _make_key(self, name: str, labels: Dict[str, str] = None) -> str:
        if labels:
            label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
            return f"{name}{{{label_str}}}"
        return name

    def render(self) -> str:
        lines = []
        for key, value in self._counters.items():
            lines.append(f"# TYPE {key.split('{')[0]} counter")
            lines.append(f"{key} {value}")
        for key, value in self._gauges.items():
            lines.append(f"# TYPE {key.split('{')[0]} gauge")
            lines.append(f"{key} {value}")
        for key, values in self._histograms.items():
            base = key.split("{")[0]
            lines.append(f"# TYPE {base} histogram")
            sorted_vals = sorted(values)
            for i, v in enumerate(sorted_vals):
                lines.append(f'{key}{{le="{v}"}} {i + 1}')
            lines.append(f'{key}{{le="+Inf"}} {len(values)}')
            lines.append(f"{base}_sum {sum(values)}")
            lines.append(f"{base}_count {len(values)}")
        return "\n".join(lines)
```

### Syslog Integration

```python
class TrafficSyslogForwarder:
    SEVERITY_MAP = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4,
        "info": 6,
    }

    def __init__(self, facility: int = 16):
        self.facility = facility
        self._buffer: List[str] = []

    def format_event(self, event: Dict, severity: str = "info") -> str:
        sev = self.SEVERITY_MAP.get(severity, 6)
        priority = self.facility * 8 + sev
        timestamp = time.strftime("%b %d %H:%M:%S", time.localtime())
        hostname = event.get("hostname", "traffic-analyzer")
        app = event.get("app", "netflow")
        msg = event.get("message", "")
        return f"<{priority}>{timestamp} {hostname} {app}: {msg}"

    def forward_event(self, event: Dict, severity: str = "info"):
        formatted = self.format_event(event, severity)
        self._buffer.append(formatted)

    def flush(self) -> List[str]:
        events = self._buffer[:]
        self._buffer = []
        return events
```

## Performance Optimization

### High-Performance Packet Processing

```python
class HighPerformancePacketProcessor:
    def __init__(self, buffer_size: int = 65536):
        self.buffer_size = buffer_size
        self._ring_buffer: List[Optional[Dict]] = [None] * buffer_size
        self._head: int = 0
        self._tail: int = 0
        self._batch_size: int = 256
        self._processed_count: int = 0
        self._dropped_count: int = 0

    def enqueue(self, packet: Dict) -> bool:
        next_head = (self._head + 1) % self.buffer_size
        if next_head == self._tail:
            self._dropped_count += 1
            return False
        self._ring_buffer[self._head] = packet
        self._head = next_head
        return True

    def dequeue_batch(self) -> List[Dict]:
        batch = []
        while self._tail != self._head and len(batch) < self._batch_size:
            packet = self._ring_buffer[self._tail]
            if packet:
                batch.append(packet)
            self._ring_buffer[self._tail] = None
            self._tail = (self._tail + 1) % self.buffer_size
        self._processed_count += len(batch)
        return batch

    def get_stats(self) -> Dict:
        used = (self._head - self._tail) % self.buffer_size
        return {
            "buffer_used": used,
            "buffer_size": self.buffer_size,
            "utilization": used / self.buffer_size,
            "processed": self._processed_count,
            "dropped": self._dropped_count,
            "drop_rate": self._dropped_count / (self._processed_count + self._dropped_count)
                         if (self._processed_count + self._dropped_count) > 0 else 0,
        }


class FlowHashOptimizer:
    def __init__(self, table_size: int = 1048576):
        self.table_size = table_size
        self._flow_table: Dict[int, Dict] = {}
        self._active_count: int = 0

    def compute_flow_key(self, src_ip: str, dst_ip: str, src_port: int, dst_port: int, proto: int) -> int:
        h = 0
        for c in src_ip:
            h = (h * 31 + ord(c)) & 0xFFFFFFFF
        for c in dst_ip:
            h = (h * 31 + ord(c)) & 0xFFFFFFFF
        h = (h * 31 + src_port) & 0xFFFFFFFF
        h = (h * 31 + dst_port) & 0xFFFFFFFF
        h = (h * 31 + proto) & 0xFFFFFFFF
        return h % self.table_size

    def update_flow(self, flow_key: int, packet: Dict):
        if flow_key in self._flow_table:
            flow = self._flow_table[flow_key]
            flow["packets"] += 1
            flow["bytes"] += packet.get("size", 0)
            flow["end_time"] = packet.get("timestamp", time.time())
        else:
            self._flow_table[flow_key] = {
                "src_ip": packet.get("src_ip"),
                "dst_ip": packet.get("dst_ip"),
                "src_port": packet.get("src_port"),
                "dst_port": packet.get("dst_port"),
                "protocol": packet.get("protocol"),
                "packets": 1,
                "bytes": packet.get("size", 0),
                "start_time": packet.get("timestamp", time.time()),
                "end_time": packet.get("timestamp", time.time()),
            }
            self._active_count += 1

    def expire_flows(self, timeout: int = 300) -> int:
        now = time.time()
        expired = []
        for key, flow in self._flow_table.items():
            if now - flow["end_time"] > timeout:
                expired.append(key)
        for key in expired:
            del self._flow_table[key]
            self._active_count -= 1
        return len(expired)

    def get_top_flows(self, n: int = 10) -> List[Dict]:
        return sorted(
            self._flow_table.values(),
            key=lambda f: f["bytes"],
            reverse=True,
        )[:n]

    def get_utilization(self) -> float:
        return self._active_count / self.table_size
```

### BPF Filter Optimization

```python
class BpfFilterOptimizer:
    COMMON_FILTERS = {
        "web_traffic": "tcp port 80 or tcp port 443",
        "dns_traffic": "udp port 53 or tcp port 53",
        "ssh_traffic": "tcp port 22",
        "email_traffic": "tcp port 25 or tcp port 110 or tcp port 143",
        "database_traffic": "tcp port 3306 or tcp port 5432 or tcp port 6379",
        "all_traffic": "",
        "internal_only": "net 10.0.0.0/8 or net 172.16.0.0/12 or net 192.168.0.0/16",
        "external_only": "not net 10.0.0.0/8 and not net 172.16.0.0/12 and not net 192.168.0.0/16",
    }

    def __init__(self):
        self._compiled_filters: Dict[str, str] = {}
        self._filter_stats: Dict[str, Dict] = {}

    def build_filter(self, ports: List[int] = None, protocols: List[str] = None,
                     source_subnets: List[str] = None, exclude_ports: List[int] = None) -> str:
        parts = []
        if ports:
            port_filter = " or ".join(f"tcp port {p}" for p in ports)
            parts.append(f"({port_filter})")
        if protocols:
            proto_filter = " or ".join(protocols)
            parts.append(f"({proto_filter})")
        if source_subnets:
            net_filter = " or ".join(f"net {n}" for n in source_subnets)
            parts.append(f"({net_filter})")
        if exclude_ports:
            exclude_filter = " and ".join(f"not port {p}" for p in exclude_ports)
            parts.append(exclude_filter)
        return " and ".join(parts) if parts else ""

    def estimate_performance(self, filter_expr: str) -> Dict:
        complexity = 0
        if "or" in filter_expr.lower():
            complexity += filter_expr.lower().count("or") * 2
        if "and" in filter_expr.lower():
            complexity += filter_expr.lower().count("and") * 1
        if "not" in filter_expr.lower():
            complexity += 1
        return {
            "filter": filter_expr,
            "complexity_score": complexity,
            "estimated_cpu_overhead": "low" if complexity < 3 else "medium" if complexity < 7 else "high",
        }

    def get_recommended_filter(self, use_case: str) -> str:
        return self.COMMON_FILTERS.get(use_case, "")
```

## Security Considerations

### Traffic Anomaly Detection

```python
class TrafficAnomalyDetector:
    def __init__(self, baseline_window: int = 3600):
        self.baseline_window = baseline_window
        self._baseline: Dict[str, List[float]] = {}
        self._current_window: Dict[str, List[float]] = {}
        self._alerts: List[Dict] = []

    def update_baseline(self, metric_name: str, value: float):
        if metric_name not in self._baseline:
            self._baseline[metric_name] = []
        self._baseline[metric_name].append(value)
        if len(self._baseline[metric_name]) > 1000:
            self._baseline[metric_name] = self._baseline[metric_name][-1000:]

    def detect_spike(self, metric_name: str, current_value: float, threshold: float = 3.0) -> bool:
        baseline = self._baseline.get(metric_name, [])
        if len(baseline) < 10:
            return False
        mean = sum(baseline) / len(baseline)
        std = (sum((x - mean) ** 2 for x in baseline) / len(baseline)) ** 0.5
        if std == 0:
            return False
        z_score = (current_value - mean) / std
        if abs(z_score) > threshold:
            self._alerts.append({
                "metric": metric_name,
                "value": current_value,
                "baseline_mean": mean,
                "z_score": z_score,
                "timestamp": time.time(),
            })
            return True
        return False

    def detect_port_scan(self, src_ip: str, dst_ports: List[int], threshold: int = 20) -> bool:
        unique_ports = set(dst_ports)
        if len(unique_ports) > threshold:
            self._alerts.append({
                "type": "port_scan",
                "src_ip": src_ip,
                "unique_ports": len(unique_ports),
                "timestamp": time.time(),
            })
            return True
        return False

    def detect_ddos(self, dst_ip: str, src_ips: List[str], pps_threshold: int = 10000) -> bool:
        unique_sources = set(src_ips)
        if len(src_ips) > pps_threshold and len(unique_sources) > 100:
            self._alerts.append({
                "type": "ddos",
                "dst_ip": dst_ip,
                "pps": len(src_ips),
                "unique_sources": len(unique_sources),
                "timestamp": time.time(),
            })
            return True
        return False

    def get_alerts(self, severity: str = None) -> List[Dict]:
        if severity:
            return [a for a in self._alerts if a.get("severity") == severity]
        return self._alerts
```

### Encrypted Traffic Analysis

```python
class EncryptedTrafficAnalyzer:
    def __init__(self):
        self._tls_sessions: Dict[str, Dict] = {}

    def analyze_tls_handshake(self, src_ip: str, dst_ip: str, payload: bytes) -> Dict:
        if len(payload) < 5:
            return {"valid": False, "reason": "payload_too_short"}
        content_type = payload[0]
        version = struct.unpack("!H", payload[1:3])[0]
        length = struct.unpack("!H", payload[3:5])[0]
        session_key = f"{src_ip}:{dst_ip}"
        self._tls_sessions[session_key] = {
            "version": version,
            "content_type": content_type,
            "length": length,
            "timestamp": time.time(),
        }
        return {
            "valid": True,
            "content_type": content_type,
            "tls_version": f"0x{version:04x}",
            "length": length,
        }

    def estimate_encryption_strength(self, tls_version: int) -> Dict:
        strength_map = {
            0x0301: {"version": "TLS 1.0", "strength": "weak", "recommendation": "upgrade"},
            0x0302: {"version": "TLS 1.1", "strength": "weak", "recommendation": "upgrade"},
            0x0303: {"version": "TLS 1.2", "strength": "strong", "recommendation": "acceptable"},
            0x0304: {"version": "TLS 1.3", "strength": "strongest", "recommendation": "preferred"},
        }
        return strength_map.get(tls_version, {"version": "unknown", "strength": "unknown"})

    def detect_certificate_anomalies(self, cert_data: bytes) -> List[Dict]:
        anomalies = []
        if len(cert_data) < 20:
            anomalies.append({"type": "short_certificate", "severity": "high"})
        return anomalies
```

### DDoS Mitigation Integration

```python
class DdosMitigationEngine:
    def __init__(self):
        self._rate_limits: Dict[str, List[float]] = {}
        self._blacklist: set = set()
        self._whitelist: set = set()
        self._threshold_pps: int = 10000
        self._threshold_bps: int = 1000000000

    def check_rate(self, src_ip: str, current_pps: float) -> Dict:
        if src_ip in self._blacklist:
            return {"action": "drop", "reason": "blacklisted"}
        if src_ip in self._whitelist:
            return {"action": "pass", "reason": "whitelisted"}
        if current_pps > self._threshold_pps:
            self._blacklist.add(src_ip)
            return {"action": "drop", "reason": "rate_exceeded", "pps": current_pps}
        return {"action": "pass"}

    def add_to_blacklist(self, ip: str):
        self._blacklist.add(ip)

    def add_to_whitelist(self, ip: str):
        self._whitelist.add(ip)
        self._blacklist.discard(ip)

    def get_mitigation_stats(self) -> Dict:
        return {
            "blacklisted_count": len(self._blacklist),
            "whitelisted_count": len(self._whitelist),
            "threshold_pps": self._threshold_pps,
            "threshold_bps": self._threshold_bps,
        }

    def generate_mitigation_rules(self) -> List[Dict]:
        rules = []
        for ip in self._blacklist:
            rules.append({
                "action": "drop",
                "source": ip,
                "description": f"Auto-blacklisted IP: {ip}",
            })
        return rules
```

## Troubleshooting Guide

### Common Traffic Analysis Issues

| Issue | Symptom | Root Cause | Solution |
|-------|---------|------------|----------|
| High packet loss | Missing flows in analysis | Buffer overflow or CPU saturation | Increase buffer size, optimize filters |
| Incomplete flows | Only one-directional data | Asymmetric routing or probe placement | Deploy probes on both paths |
| High CPU usage | Analysis delays | Too many active flows | Enable flow aggregation, reduce capture rate |
| Timestamp skew | Correlation failures | NTP drift on probes | Sync all probes to NTP source |
| Memory exhaustion | OOM kills | Unbounded flow tables | Set flow expiration timers |
| Duplicate packets | Inflated statistics | Multiple probe captures | Deduplicate by flow key |

```python
class TrafficDiagnostics:
    def __init__(self):
        self._diagnostics: List[Dict] = []

    def check_capture_health(self, packet_count: int, dropped_count: int, buffer_util: float) -> Dict:
        issues = []
        if dropped_count > 0:
            loss_rate = dropped_count / (packet_count + dropped_count)
            issues.append({
                "severity": "high" if loss_rate > 0.01 else "medium",
                "issue": "packet_loss",
                "loss_rate": f"{loss_rate * 100:.2f}%",
                "recommendation": "Increase capture buffer or use BPF filters to reduce load",
            })
        if buffer_util > 0.8:
            issues.append({
                "severity": "high",
                "issue": "buffer_nearing_full",
                "utilization": f"{buffer_util * 100:.1f}%",
                "recommendation": "Increase buffer size or flush more frequently",
            })
        return {"status": "healthy" if not issues else "degraded", "issues": issues}

    def check_flow_table_health(self, active_flows: int, max_flows: int, expired_count: int) -> Dict:
        utilization = active_flows / max_flows if max_flows > 0 else 0
        return {
            "active_flows": active_flows,
            "utilization": f"{utilization * 100:.1f}%",
            "expired": expired_count,
            "status": "healthy" if utilization < 0.7 else "warning" if utilization < 0.9 else "critical",
        }

    def check_timestamp_consistency(self, timestamps: List[float]) -> Dict:
        if len(timestamps) < 2:
            return {"consistent": True}
        diffs = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        max_diff = max(diffs)
        min_diff = min(diffs)
        skew = max_diff - min_diff
        return {
            "consistent": skew < 1.0,
            "max_skew_seconds": skew,
            "recommendation": "Sync probes to NTP" if skew >= 1.0 else "None",
        }
```

### Performance Troubleshooting

```python
class PerformanceTroubleshooter:
    def __init__(self):
        self._baseline_metrics: Dict[str, float] = {}
        self._current_metrics: Dict[str, float] = {}

    def set_baseline(self, metrics: Dict[str, float]):
        self._baseline_metrics = metrics.copy()

    def update_current(self, metrics: Dict[str, float]):
        self._current_metrics = metrics.copy()

    def analyze_degradation(self) -> List[Dict]:
        issues = []
        for metric, current_val in self._current_metrics.items():
            baseline_val = self._baseline_metrics.get(metric)
            if baseline_val and baseline_val > 0:
                degradation = (current_val - baseline_val) / baseline_val
                if degradation > 0.2:
                    issues.append({
                        "metric": metric,
                        "baseline": baseline_val,
                        "current": current_val,
                        "degradation_pct": f"{degradation * 100:.1f}%",
                        "severity": "high" if degradation > 0.5 else "medium",
                    })
        return issues

    def get_recommendations(self, issues: List[Dict]) -> List[str]:
        recommendations = []
        for issue in issues:
            if "cpu" in issue["metric"].lower():
                recommendations.append("Consider upgrading CPU or reducing capture rate")
            elif "memory" in issue["metric"].lower():
                recommendations.append("Increase available memory or optimize flow table size")
            elif "latency" in issue["metric"].lower():
                recommendations.append("Check network congestion and probe placement")
        return recommendations
```

## API Reference

### TrafficAnalyzer API

```python
class TrafficAnalyzerApi:
    """RESTful API wrapper for traffic analysis operations."""

    def __init__(self, analyzer: PacketAnalyzer):
        self.analyzer = analyzer

    def get_protocol_distribution(self) -> Dict[str, int]:
        return self.analyzer.get_protocol_distribution()

    def get_top_talkers(self, limit: int = 10) -> List[Dict]:
        talkers = self.analyzer.get_top_talkers(limit)
        return [{"ip": ip, "bytes": b} for ip, b in talkers]

    def get_anomalies(self, threshold: float = 3.0) -> List[Dict]:
        return self.analyzer.detect_anomalies(threshold)

    def get_statistics(self) -> Dict:
        stats = self.analyzer.get_statistics()
        return {
            "total_packets": stats.total_packets,
            "total_bytes": stats.total_bytes,
            "unique_src_ips": stats.unique_src_ips,
            "unique_dst_ips": stats.unique_dst_ips,
            "avg_packet_size": stats.avg_packet_size,
            "duration": stats.duration,
        }
```

### FlowCollector API

```python
class FlowCollectorApi:
    def __init__(self, collector: FlowCollector):
        self.collector = collector

    def ingest_packet(self, packet: Dict):
        pkt = Packet(
            timestamp=packet.get("timestamp", time.time()),
            src_ip=packet.get("src_ip", ""),
            dst_ip=packet.get("dst_ip", ""),
            src_port=packet.get("src_port", 0),
            dst_port=packet.get("dst_port", 0),
            protocol=packet.get("protocol", 0),
            size=packet.get("size", 0),
        )
        self.collector.process_packet(pkt)

    def get_top_flows(self, limit: int = 10) -> List[Dict]:
        flows = self.collector.get_top_flows(limit)
        return [
            {
                "src_ip": f.src_ip, "dst_ip": f.dst_ip,
                "src_port": f.src_port, "dst_port": f.dst_port,
                "bytes": f.bytes_sent, "packets": f.packets,
                "duration": f.duration,
            }
            for f in flows
        ]

    def get_summary(self) -> Dict:
        return self.collector.get_summary()
```

## Data Models

### Traffic Record Schema

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class TrafficRecordType(Enum):
    PACKET = "packet"
    FLOW = "flow"
    ALERT = "alert"
    STATISTICS = "statistics"

@dataclass
class TrafficRecordSchema:
    record_type: str
    timestamp: float
    src_ip: str
    dst_ip: str
    src_port: int = 0
    dst_port: int = 0
    protocol: int = 0
    bytes_sent: int = 0
    packets: int = 0
    duration: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "record_type": self.record_type,
            "timestamp": self.timestamp,
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
            "src_port": self.src_port,
            "dst_port": self.dst_port,
            "protocol": self.protocol,
            "bytes_sent": self.bytes_sent,
            "packets": self.packets,
            "duration": self.duration,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TrafficRecordSchema":
        return cls(
            record_type=data["record_type"],
            timestamp=data["timestamp"],
            src_ip=data["src_ip"],
            dst_ip=data["dst_ip"],
            src_port=data.get("src_port", 0),
            dst_port=data.get("dst_port", 0),
            protocol=data.get("protocol", 0),
            bytes_sent=data.get("bytes_sent", 0),
            packets=data.get("packets", 0),
            duration=data.get("duration", 0.0),
            metadata=data.get("metadata", {}),
        )

@dataclass
class TrafficAlertSchema:
    alert_type: str
    severity: str
    src_ip: str
    dst_ip: str
    message: str
    timestamp: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "alert_type": self.alert_type,
            "severity": self.severity,
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
            "message": self.message,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
```

### Network Baseline Schema

```python
@dataclass
class NetworkBaseline:
    interface: str
    avg_bps: float = 0.0
    peak_bps: float = 0.0
    avg_pps: float = 0.0
    peak_pps: float = 0.0
    avg_packet_size: float = 0.0
    protocol_distribution: Dict[str, float] = field(default_factory=dict)
    top_talkers: List[Dict] = field(default_factory=list)
    measurement_window: int = 3600
    last_updated: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "interface": self.interface,
            "avg_bps": self.avg_bps,
            "peak_bps": self.peak_bps,
            "avg_pps": self.avg_pps,
            "peak_pps": self.peak_pps,
            "avg_packet_size": self.avg_packet_size,
            "protocol_distribution": self.protocol_distribution,
            "top_talkers": self.top_talkers,
            "measurement_window": self.measurement_window,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "NetworkBaseline":
        return cls(
            interface=data["interface"],
            avg_bps=data.get("avg_bps", 0.0),
            peak_bps=data.get("peak_bps", 0.0),
            avg_pps=data.get("avg_pps", 0.0),
            peak_pps=data.get("peak_pps", 0.0),
            avg_packet_size=data.get("avg_packet_size", 0.0),
            protocol_distribution=data.get("protocol_distribution", {}),
            top_talkers=data.get("top_talkers", []),
            measurement_window=data.get("measurement_window", 3600),
            last_updated=data.get("last_updated", 0.0),
        )
```

## Deployment Guide

### Probe Deployment Architecture

```python
class ProbeDeploymentManager:
    def __init__(self):
        self.probes: List[Dict] = []
        self._deployment_configs: Dict[str, Dict] = {}

    def add_probe(self, name: str, interface: str, ip: str, role: str = "passive"):
        self.probes.append({
            "name": name,
            "interface": interface,
            "ip": ip,
            "role": role,
            "status": "pending",
        })

    def configure_probe(self, name: str, config: Dict):
        self._deployment_configs[name] = config

    def generate_deployment_script(self, probe_name: str) -> str:
        probe = next((p for p in self.probes if p["name"] == probe_name), None)
        if not probe:
            return ""
        config = self._deployment_configs.get(probe_name, {})
        script_lines = [
            "#!/bin/bash",
            f"# Deployment script for probe: {probe_name}",
            f"INTERFACE={probe['interface']}",
            f"ROLE={probe['role']}",
            "",
            "# Setup capture interface",
            f"ip link set $INTERFACE up",
            "",
            "# Configure BPF filter",
            f"tcpdump -i $INTERFACE -w /var/capture/{probe_name}.pcap -G 3600 &",
            "",
            "# Start NetFlow collector",
            f"nfcapd -p 9995 -d /var/netflow/{probe_name} &",
            "",
            f"echo 'Probe {probe_name} deployed successfully'",
        ]
        return "\n".join(script_lines)

    def get_deployment_status(self) -> Dict:
        statuses = {}
        for probe in self.probes:
            statuses[probe["name"]] = probe["status"]
        return statuses
```

### Distributed Capture Configuration

```python
class DistributedCaptureConfig:
    def __init__(self):
        self.capture_nodes: List[Dict] = []
        self._aggregation_server: Optional[str] = None

    def add_node(self, name: str, ip: str, interface: str, bpf_filter: str = ""):
        self.capture_nodes.append({
            "name": name,
            "ip": ip,
            "interface": interface,
            "bpf_filter": bpf_filter,
            "status": "configured",
        })

    def set_aggregation_server(self, ip: str):
        self._aggregation_server = ip

    def generate_config_file(self) -> str:
        config = {
            "capture_nodes": self.capture_nodes,
            "aggregation_server": self._aggregation_server,
            "global_settings": {
                "buffer_size": 65536,
                "snap_length": 96,
                "promiscuous": True,
                "timestamp_precision": "micro",
            },
        }
        import json
        return json.dumps(config, indent=2)

    def generate_docker_compose(self) -> str:
        services = []
        for node in self.capture_nodes:
            services.append(f"""
  {node['name']}:
    image: tcpdump:latest
    network_mode: host
    command: tcpdump -i {node['interface']} -w /data/{node['name']}.pcap
    volumes:
      - ./captures:/data""")
        compose = "version: '3'\nservices:" + "\n".join(services)
        return compose
```

## Monitoring & Observability

### Traffic Monitoring Dashboard

```python
class TrafficMonitoringDashboard:
    def __init__(self):
        self._metrics: Dict[str, List[Dict]] = {
            "bandwidth": [],
            "packets_per_second": [],
            "active_flows": [],
            "anomaly_score": [],
        }
        self._alerts: List[Dict] = []

    def record_metric(self, metric_name: str, value: float):
        if metric_name in self._metrics:
            self._metrics[metric_name].append({
                "value": value,
                "timestamp": time.time(),
            })
            if len(self._metrics[metric_name]) > 10000:
                self._metrics[metric_name] = self._metrics[metric_name][-10000:]

    def get_bandwidth_utilization(self, interface: str, capacity_bps: float) -> float:
        recent = self._metrics.get("bandwidth", [])[-100:]
        if not recent:
            return 0.0
        avg_bps = sum(m["value"] for m in recent) / len(recent)
        return (avg_bps / capacity_bps) * 100

    def get_dashboard_data(self) -> Dict:
        return {
            "current_bandwidth": self._get_latest("bandwidth"),
            "current_pps": self._get_latest("packets_per_second"),
            "active_flows": self._get_latest("active_flows"),
            "anomaly_score": self._get_latest("anomaly_score"),
            "alerts": len(self._alerts),
        }

    def _get_latest(self, metric_name: str) -> float:
        values = self._metrics.get(metric_name, [])
        return values[-1]["value"] if values else 0.0

    def check_thresholds(self, thresholds: Dict[str, Dict]) -> List[Dict]:
        alerts = []
        for metric, config in thresholds.items():
            current = self._get_latest(metric)
            if current > config.get("critical", float("inf")):
                alerts.append({"metric": metric, "severity": "critical", "value": current})
            elif current > config.get("warning", float("inf")):
                alerts.append({"metric": metric, "severity": "warning", "value": current})
        return alerts
```

### Flow Analytics Reporter

```python
class FlowAnalyticsReporter:
    def __init__(self):
        self._flows: List[Dict] = []
        self._reports: List[Dict] = []

    def add_flow(self, flow: Dict):
        self._flows.append(flow)

    def generate_summary_report(self, window_seconds: int = 3600) -> Dict:
        now = time.time()
        recent = [f for f in self._flows if now - f.get("timestamp", 0) < window_seconds]
        if not recent:
            return {"total_flows": 0}
        total_bytes = sum(f.get("bytes", 0) for f in recent)
        total_packets = sum(f.get("packets", 0) for f in recent)
        src_ips = set(f.get("src_ip") for f in recent)
        dst_ips = set(f.get("dst_ip") for f in recent)
        return {
            "total_flows": len(recent),
            "total_bytes": total_bytes,
            "total_packets": total_packets,
            "unique_sources": len(src_ips),
            "unique_destinations": len(dst_ips),
            "avg_flow_duration": sum(f.get("duration", 0) for f in recent) / len(recent),
            "avg_bytes_per_flow": total_bytes / len(recent),
        }

    def generate_protocol_report(self) -> Dict:
        protocol_stats: Dict[str, Dict] = {}
        for flow in self._flows:
            proto = str(flow.get("protocol", "unknown"))
            if proto not in protocol_stats:
                protocol_stats[proto] = {"bytes": 0, "packets": 0, "flows": 0}
            protocol_stats[proto]["bytes"] += flow.get("bytes", 0)
            protocol_stats[proto]["packets"] += flow.get("packets", 0)
            protocol_stats[proto]["flows"] += 1
        return protocol_stats
```

## Testing Strategy

### Unit Tests

```python
import unittest

class TestPacketAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PacketAnalyzer()

    def test_protocol_distribution(self):
        self.analyzer.add_packet(Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 100))
        self.analyzer.add_packet(Packet(0, "10.0.0.1", "10.0.0.2", 12346, 443, 6, 200))
        dist = self.analyzer.get_protocol_distribution()
        self.assertEqual(dist.get("HTTP", 0), 1)
        self.assertEqual(dist.get("HTTPS", 0), 1)

    def test_top_talkers(self):
        for _ in range(5):
            self.analyzer.add_packet(Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 100))
        self.analyzer.add_packet(Packet(0, "10.0.0.3", "10.0.0.2", 12345, 80, 6, 50))
        talkers = self.analyzer.get_top_talkers(1)
        self.assertEqual(talkers[0][0], "10.0.0.1")
        self.assertEqual(talkers[0][1], 500)

    def test_anomaly_detection(self):
        for _ in range(20):
            self.analyzer.add_packet(Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 100))
        self.analyzer.add_packet(Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 10000))
        anomalies = self.analyzer.detect_anomalies()
        self.assertTrue(len(anomalies) > 0)

    def test_statistics(self):
        self.analyzer.add_packet(Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 100))
        self.analyzer.add_packet(Packet(0, "10.0.0.3", "10.0.0.4", 12345, 443, 6, 200))
        stats = self.analyzer.get_statistics()
        self.assertEqual(stats.total_packets, 2)
        self.assertEqual(stats.total_bytes, 300)
        self.assertEqual(stats.unique_src_ips, 2)


class TestFlowCollector(unittest.TestCase):
    def setUp(self):
        self.collector = FlowCollector()

    def test_flow_creation(self):
        pkt = Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 100)
        self.collector.process_packet(pkt)
        flows = self.collector.get_flows()
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].packets, 1)

    def test_flow_aggregation(self):
        pkt = Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 100)
        self.collector.process_packet(pkt)
        self.collector.process_packet(pkt)
        flows = self.collector.get_flows()
        self.assertEqual(flows[0].packets, 2)
        self.assertEqual(flows[0].bytes_sent, 200)

    def test_top_flows(self):
        for i in range(10):
            pkt = Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, i * 100)
            self.collector.process_packet(pkt)
        top = self.collector.get_top_flows(1)
        self.assertEqual(top[0].bytes_sent, 900)


class TestTrafficClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = TrafficClassifier()

    def test_classify_web(self):
        pkt = Packet(0, "10.0.0.1", "10.0.0.2", 12345, 80, 6, 100)
        result = self.classifier.classify(pkt)
        self.assertEqual(result, "Web")

    def test_classify_database(self):
        pkt = Packet(0, "10.0.0.1", "10.0.0.2", 12345, 3306, 6, 100)
        result = self.classifier.classify(pkt)
        self.assertEqual(result, "MySQL")

    def test_classify_unknown(self):
        pkt = Packet(0, "10.0.0.1", "10.0.0.2", 12345, 9999, 6, 100)
        result = self.classifier.classify(pkt)
        self.assertEqual(result, "Other")


if __name__ == "__main__":
    unittest.main()
```

### Integration Tests

```python
class TestAnomalyDetector(unittest.TestCase):
    def setUp(self):
        self.detector = TrafficAnomalyDetector()

    def test_spike_detection(self):
        for _ in range(100):
            self.detector.update_baseline("bandwidth", 1000)
        result = self.detector.detect_spike("bandwidth", 5000)
        self.assertTrue(result)

    def test_no_spike_within_normal(self):
        for _ in range(100):
            self.detector.update_baseline("bandwidth", 1000)
        result = self.detector.detect_spike("bandwidth", 1050)
        self.assertFalse(result)

    def test_port_scan_detection(self):
        ports = list(range(100))
        result = self.detector.detect_port_scan("10.0.0.1", ports)
        self.assertTrue(result)

    def test_ddos_detection(self):
        src_ips = [f"10.0.{i // 256}.{i % 256}" for i in range(20000)]
        result = self.detector.detect_ddos("10.0.0.1", src_ips)
        self.assertTrue(result)


class TestHighPerformanceProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = HighPerformancePacketProcessor(buffer_size=1024)

    def test_enqueue_dequeue(self):
        pkt = {"src_ip": "10.0.0.1", "dst_ip": "10.0.0.2", "size": 100}
        self.assertTrue(self.processor.enqueue(pkt))
        batch = self.processor.dequeue_batch()
        self.assertEqual(len(batch), 1)

    def test_buffer_overflow(self):
        for _ in range(1025):
            self.processor.enqueue({"src_ip": "10.0.0.1"})
        stats = self.processor.get_stats()
        self.assertTrue(stats["dropped"] > 0)


class TestDdosMitigation(unittest.TestCase):
    def setUp(self):
        self.engine = DdosMitigationEngine()

    def test_normal_traffic_passes(self):
        result = self.engine.check_rate("10.0.0.1", 100)
        self.assertEqual(result["action"], "pass")

    def test_high_rate_gets_blocked(self):
        result = self.engine.check_rate("10.0.0.1", 50000)
        self.assertEqual(result["action"], "drop")

    def test_whitelist_bypasses(self):
        self.engine.add_to_whitelist("10.0.0.1")
        result = self.engine.check_rate("10.0.0.1", 50000)
        self.assertEqual(result["action"], "pass")


if __name__ == "__main__":
    unittest.main()
```

## Versioning & Migration

### Flow Record Version Control

```python
class FlowRecordVersionControl:
    def __init__(self):
        self.versions: List[Dict] = []
        self.current_version: int = 0

    def commit(self, flows: List[Dict], message: str, author: str = "system"):
        version = {
            "id": self.current_version,
            "flow_count": len(flows),
            "flows": flows[:1000],  # Store first 1000 for reference
            "message": message,
            "author": author,
            "timestamp": time.time(),
        }
        self.versions.append(version)
        self.current_version += 1
        return version["id"]

    def rollback(self, version_id: int) -> Optional[List[Dict]]:
        for version in self.versions:
            if version["id"] == version_id:
                return version["flows"]
        return None

    def get_history(self) -> List[Dict]:
        return [
            {"id": v["id"], "flow_count": v["flow_count"], "message": v["message"]}
            for v in self.versions
        ]
```

### Schema Migration Runner

```python
class SchemaMigrationRunner:
    def __init__(self):
        self.migrations: List[Dict] = []
        self.applied: List[Dict] = []

    def add_migration(self, name: str, up_fn, down_fn):
        self.migrations.append({
            "name": name,
            "up": up_fn,
            "down": down_fn,
            "applied": False,
        })

    def migrate_up(self) -> List[str]:
        results = []
        for migration in self.migrations:
            if not migration["applied"]:
                migration["up"]()
                migration["applied"] = True
                self.applied.append(migration)
                results.append(migration["name"])
        return results

    def migrate_down(self, steps: int = 1) -> List[str]:
        results = []
        for migration in reversed(self.applied[-steps:]):
            migration["down"]()
            migration["applied"] = False
            self.applied.remove(migration)
            results.append(migration["name"])
        return results
```

## Glossary

| Term | Definition |
|------|-----------|
| **PCAP** | Packet Capture - file format for storing captured network packets |
| **NetFlow** | Cisco's protocol for collecting IP traffic information |
| **IPFIX** | IP Flow Information Export - IETF standard for flow data |
| **sFlow** | Sampled Flow - packet sampling technology for network monitoring |
| **BPF** | Berkeley Packet Filter - kernel-level packet filtering |
| **DPI** | Deep Packet Inspection - analyzing packet payload content |
| **Top Talkers** | Devices generating the most network traffic |
| **Flow** | A sequence of packets sharing common 5-tuple attributes |
| **5-tuple** | Source IP, Destination IP, Source Port, Destination Port, Protocol |
| **Packet Loss** | Packets that fail to reach their destination |
| **Jitter** | Variation in packet delay (inter-packet delay variation) |
| **Bandwidth** | Maximum data transfer rate of a network link |
| **Throughput** | Actual data transfer rate achieved |
| **Latency** | Time delay for a packet to travel from source to destination |
| **Anycast** | Routing method where multiple servers share one IP address |
| **SNMP** | Simple Network Management Protocol |
| **MIB** | Management Information Base - SNMP database schema |
| **OID** | Object Identifier - SNMP resource identifier |
| **Syslog** | System logging protocol for event reporting |
| **QoS** | Quality of Service - traffic prioritization mechanisms |
| **DSCP** | Differentiated Services Code Point - QoS marking field |
| **ECN** | Explicit Congestion Notification - TCP congestion signal |
| **MTU** | Maximum Transmission Unit - largest packet size |
| **VLAN** | Virtual Local Area Network - logical network segmentation |
| **Trunk** | Link carrying multiple VLAN traffic |
| **SPAN** | Switched Port Analyzer - port mirroring |
| **ERSPAN** | Encapsulated Remote SPAN - tunnel-based mirroring |
| **Capture Buffer** | Memory area storing packets before processing |
| **Ring Buffer** | Circular buffer for continuous packet capture |
| **Flow Export** | Process of sending flow records to a collector |
| **Active Timeout** | Duration before an active flow is exported |
| **Inactive Timeout** | Duration of inactivity before a flow is exported |
| **Template** | NetFlow v9/IPFIX record structure definition |
| **Observability** | Ability to understand internal system state from outputs |
| **Telemetry** | Automated collection and transmission of monitoring data |
| **Baseline** | Reference measurement for normal network behavior |
| **Anomaly** | Deviation from expected network behavior patterns |
| **Histogram** | Statistical distribution of metric values |
| **Percentile** | Value below which a given percentage of data falls |

## Changelog

### Version 2.1.0 (Latest)
- Added NetFlow v9 template configuration and parsing
- Added sFlow datagram parsing with enterprise extension support
- Added Deep Packet Inspection engine with protocol signatures
- Added distributed traffic analysis pipeline architecture
- Added multi-layer analysis framework (L2-L7)
- Added Elasticsearch and Prometheus integration
- Added high-performance ring buffer processor
- Added BPF filter optimization and performance estimation
- Added traffic anomaly detection with baseline learning
- Added encrypted traffic analysis for TLS sessions
- Added DDoS mitigation engine
- Added comprehensive monitoring dashboard
- Added flow analytics reporter
- Added distributed capture configuration
- Added probe deployment management
- Added unit and integration test suites

### Version 2.0.0
- Complete rewrite with class-based architecture
- Added flow collection with active/inactive timeouts
- Added traffic classification and protocol detection
- Added anomaly detection with statistical analysis
- Added comprehensive statistics generation

### Version 1.0.0
- Initial release with basic packet analysis
- Protocol distribution and top talkers
- Simple anomaly detection

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/org/traffic-analysis-skill.git
cd traffic-analysis-skill

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Run linter
flake8 src/
mypy src/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Write docstrings for public classes and methods
- Keep functions under 50 lines
- Use dataclasses for data structures
- Prefer composition over inheritance

### Pull Request Process

1. Fork the repository and create a feature branch
2. Write tests for new functionality
3. Ensure all existing tests pass
4. Update documentation if adding new features
5. Submit PR with descriptive title and detailed description
6. Request review from at least one maintainer

### Issue Reporting

- Use GitHub Issues for bug reports
- Include reproduction steps and expected vs actual behavior
- Tag issues with appropriate labels (bug, enhancement, documentation)
- Check existing issues before creating new ones

## License

MIT License

Copyright (c) 2024 Traffic Analysis Skill Contributors

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
