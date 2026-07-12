"""
Traffic Analysis Module
Part of the networking skill domain.

Network traffic analysis: packet processing, flow collection, protocol
classification, anomaly detection, and bandwidth monitoring.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class Protocol(Enum):
    TCP = 6
    UDP = 17
    ICMP = 1
    IGMP = 2
    UNKNOWN = 0


KNOWN_PORTS: Dict[int, str] = {
    80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH", 25: "SMTP",
    110: "POP3", 143: "IMAP", 993: "IMAPS", 995: "POP3S",
    3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
    27017: "MongoDB", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt",
}


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
    vlan_id: int = 0

    @property
    def protocol_name(self) -> str:
        if self.dst_port in KNOWN_PORTS:
            return KNOWN_PORTS[self.dst_port]
        if self.src_port in KNOWN_PORTS:
            return KNOWN_PORTS[self.src_port]
        try:
            return Protocol(self.protocol).name
        except ValueError:
            return "OTHER"


@dataclass
class FlowRecord:
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: int
    packets: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    app_protocol: str = ""

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    @property
    def bytes_per_second(self) -> float:
        return self.bytes_sent / self.duration if self.duration > 0 else 0

    @property
    def total_bytes(self) -> int:
        return self.bytes_sent + self.bytes_received

    def to_dict(self) -> Dict[str, Any]:
        return {
            "src": f"{self.src_ip}:{self.src_port}",
            "dst": f"{self.dst_ip}:{self.dst_port}",
            "protocol": self.app_protocol or str(self.protocol),
            "packets": self.packets,
            "bytes": self.total_bytes,
            "duration_s": round(self.duration, 3),
            "bps": round(self.bytes_per_second, 1),
        }


@dataclass
class TrafficStats:
    total_packets: int = 0
    total_bytes: int = 0
    unique_src_ips: int = 0
    unique_dst_ips: int = 0
    protocol_distribution: Dict[str, int] = field(default_factory=dict)
    top_sources: List[Tuple[str, int]] = field(default_factory=list)
    top_destinations: List[Tuple[str, int]] = field(default_factory=list)
    top_protocols: List[Tuple[str, int]] = field(default_factory=list)
    avg_packet_size: float = 0.0
    duration: float = 0.0
    packets_per_second: float = 0.0


class PacketAnalyzer:
    def __init__(self, max_packets: int = 100000):
        self.max_packets = max_packets
        self._packets: List[Packet] = []

    def add_packet(self, packet: Packet):
        if len(self._packets) >= self.max_packets:
            self._packets.pop(0)
        self._packets.append(packet)

    def add_bulk(self, packets: List[Packet]):
        for p in packets:
            self.add_packet(p)

    def get_protocol_distribution(self) -> Dict[str, int]:
        dist: Dict[str, int] = defaultdict(int)
        for p in self._packets:
            dist[p.protocol_name] += 1
        return dict(sorted(dist.items(), key=lambda x: x[1], reverse=True))

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

    def get_top_ports(self, n: int = 10) -> List[Tuple[int, int]]:
        port_bytes: Dict[int, int] = defaultdict(int)
        for p in self._packets:
            port_bytes[p.dst_port] += p.size
        return sorted(port_bytes.items(), key=lambda x: x[1], reverse=True)[:n]

    def detect_anomalies(self, threshold: float = 3.0) -> List[Dict[str, Any]]:
        if len(self._packets) < 10:
            return []
        sizes = [p.size for p in self._packets]
        mean = sum(sizes) / len(sizes)
        std = (sum((s - mean) ** 2 for s in sizes) / len(sizes)) ** 0.5

        anomalies = []
        if std == 0:
            return anomalies
        for i, p in enumerate(self._packets):
            z_score = (p.size - mean) / std
            if abs(z_score) > threshold:
                anomalies.append({
                    "index": i, "src_ip": p.src_ip, "dst_ip": p.dst_ip,
                    "size": p.size, "z_score": round(z_score, 2),
                    "timestamp": p.timestamp,
                })
        return anomalies

    def detect_port_scan(self, threshold: int = 20) -> List[Dict[str, Any]]:
        connections_per_src: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for p in self._packets:
            if p.protocol == Protocol.TCP.value:
                connections_per_src[p.src_ip][p.dst_ip] += 1

        scans = []
        for src, dsts in connections_per_src.items():
            for dst, count in dsts.items():
                if count >= threshold:
                    scans.append({"src_ip": src, "dst_ip": dst, "port_count": count})
        return scans

    def get_statistics(self) -> TrafficStats:
        if not self._packets:
            return TrafficStats()

        src_ips = set(p.src_ip for p in self._packets)
        dst_ips = set(p.dst_ip for p in self._packets)
        total_bytes = sum(p.size for p in self._packets)
        duration = self._packets[-1].timestamp - self._packets[0].timestamp if len(self._packets) > 1 else 0

        return TrafficStats(
            total_packets=len(self._packets),
            total_bytes=total_bytes,
            unique_src_ips=len(src_ips),
            unique_dst_ips=len(dst_ips),
            protocol_distribution=self.get_protocol_distribution(),
            top_sources=self.get_top_talkers(5),
            top_destinations=self.get_top_destinations(5),
            top_protocols=list(self.get_protocol_distribution().items())[:5],
            avg_packet_size=total_bytes / len(self._packets),
            duration=duration,
            packets_per_second=len(self._packets) / duration if duration > 0 else 0,
        )

    def clear(self):
        self._packets.clear()


class FlowCollector:
    def __init__(self, active_timeout: float = 300.0, inactive_timeout: float = 15.0):
        self.active_timeout = active_timeout
        self.inactive_timeout = inactive_timeout
        self._flows: Dict[str, FlowRecord] = {}

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
                app_protocol=packet.protocol_name,
            )

    def get_flows(self) -> List[FlowRecord]:
        return list(self._flows.values())

    def get_top_flows(self, n: int = 10) -> List[FlowRecord]:
        return sorted(self._flows.values(), key=lambda f: f.total_bytes, reverse=True)[:n]

    def export_flows(self) -> List[Dict[str, Any]]:
        return [f.to_dict() for f in self.get_top_flows()]

    def get_summary(self) -> Dict[str, Any]:
        flows = list(self._flows.values())
        if not flows:
            return {"total_flows": 0}
        return {
            "total_flows": len(flows),
            "total_bytes": sum(f.total_bytes for f in flows),
            "avg_flow_duration": round(sum(f.duration for f in flows) / len(flows), 3),
            "avg_bytes_per_flow": round(sum(f.total_bytes for f in flows) / len(flows), 1),
        }

    def clear(self):
        self._flows.clear()


class TrafficClassifier:
    def classify_packet(self, packet: Packet) -> str:
        if packet.dst_port in KNOWN_PORTS:
            return KNOWN_PORTS[packet.dst_port]
        if packet.src_port in KNOWN_PORTS:
            return KNOWN_PORTS[packet.src_port]
        if packet.protocol == Protocol.ICMP.value:
            return "ICMP"
        return "Unknown"

    def classify_flows(self, flows: List[FlowRecord]) -> Dict[str, List[FlowRecord]]:
        classified: Dict[str, List[FlowRecord]] = defaultdict(list)
        for f in flows:
            app = f.app_protocol or self._classify_flow(f)
            classified[app].append(f)
        return dict(classified)

    def _classify_flow(self, flow: FlowRecord) -> str:
        if flow.dst_port in KNOWN_PORTS:
            return KNOWN_PORTS[flow.dst_port]
        if flow.src_port in KNOWN_PORTS:
            return KNOWN_PORTS[flow.src_port]
        if flow.protocol == Protocol.ICMP.value:
            return "ICMP"
        return "Unknown"

    def get_classification_summary(self, flows: List[FlowRecord]) -> Dict[str, Dict[str, Any]]:
        classified = self.classify_flows(flows)
        summary = {}
        for app, app_flows in classified.items():
            summary[app] = {
                "count": len(app_flows),
                "total_bytes": sum(f.total_bytes for f in app_flows),
                "avg_duration": round(sum(f.duration for f in app_flows) / len(app_flows), 3),
            }
        return summary


class BandwidthMonitor:
    def __init__(self, interface: str = "eth0"):
        self.interface = interface
        self._snapshots: List[Tuple[float, int, int]] = []

    def record(self, bytes_in: int, bytes_out: int):
        self._snapshots.append((time.time(), bytes_in, bytes_out))

    def get_utilization(self) -> Dict[str, Any]:
        if len(self._snapshots) < 2:
            return {"interface": self.interface, "samples": 0}
        first, last = self._snapshots[0], self._snapshots[-1]
        duration = last[0] - first[0]
        if duration <= 0:
            return {"interface": self.interface, "duration": 0}
        bytes_in_rate = (last[1] - first[1]) / duration
        bytes_out_rate = (last[2] - first[2]) / duration
        return {
            "interface": self.interface,
            "duration_s": round(duration, 2),
            "avg_in_mbps": round(bytes_in_rate * 8 / 1_000_000, 2),
            "avg_out_mbps": round(bytes_out_rate * 8 / 1_000_000, 2),
            "total_in_gb": round((last[1] - first[1]) / 1e9, 3),
            "total_out_gb": round((last[2] - first[2]) / 1e9, 3),
        }


def main():
    print("=== Traffic Analysis Module ===")

    import random
    analyzer = PacketAnalyzer(max_packets=5000)
    collector = FlowCollector()

    print("\n=== Generating Sample Traffic ===")
    src_ips = [f"192.168.1.{i}" for i in range(1, 20)]
    dst_ips = [f"10.0.{i}.{j}" for i in range(1, 5) for j in range(1, 10)]

    for i in range(500):
        src = random.choice(src_ips)
        dst = random.choice(dst_ips)
        proto = random.choice([Protocol.TCP.value, Protocol.UDP.value, Protocol.ICMP.value])
        dst_port = random.choice([80, 443, 53, 22, 3306, 8080, random.randint(10000, 60000)])
        size = random.randint(60, 1500)
        pkt = Packet(time.time(), src, dst, random.randint(1024, 65535), dst_port, proto, size)
        analyzer.add_packet(pkt)
        collector.process_packet(pkt)

    print("\n=== Protocol Distribution ===")
    for proto, count in analyzer.get_protocol_distribution().items():
        print(f"  {proto}: {count}")

    print("\n=== Top Talkers ===")
    for ip, bytes_sent in analyzer.get_top_talkers(5):
        print(f"  {ip}: {bytes_sent:,} bytes")

    print("\n=== Anomaly Detection ===")
    anomalies = analyzer.detect_anomalies(threshold=2.5)
    print(f"  Found {len(anomalies)} anomalies")

    print("\n=== Port Scan Detection ===")
    scans = analyzer.detect_port_scan(threshold=10)
    print(f"  Detected {len(scans)} potential scans")

    print("\n=== Flow Analysis ===")
    flow_summary = collector.get_summary()
    for k, v in flow_summary.items():
        print(f"  {k}: {v}")

    top_flows = collector.get_top_flows(3)
    for f in top_flows:
        print(f"  Flow: {f.src_ip}:{f.src_port} -> {f.dst_ip}:{f.dst_port} ({f.total_bytes} bytes)")

    print("\n=== Traffic Statistics ===")
    stats = analyzer.get_statistics()
    print(f"  Total packets: {stats.total_packets}")
    print(f"  Total bytes: {stats.total_bytes:,}")
    print(f"  Unique sources: {stats.unique_src_ips}")
    print(f"  Unique destinations: {stats.unique_dst_ips}")
    print(f"  Avg packet size: {stats.avg_packet_size:.0f} bytes")
    print(f"  Duration: {stats.duration:.1f}s")

    print("\n=== Bandwidth Monitor ===")
    bw = BandwidthMonitor("eth0")
    for i in range(10):
        bw.record(random.randint(100000, 500000), random.randint(50000, 200000))
    utilization = bw.get_utilization()
    for k, v in utilization.items():
        print(f"  {k}: {v}")

    print("\nDone.")


if __name__ == "__main__":
    main()
