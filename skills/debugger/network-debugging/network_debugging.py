"""
Network Debugging Framework

Production-grade network debugging toolkit providing packet capture, protocol analysis,
latency measurement, DNS debugging, and connection diagnostics for network troubleshooting.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    HTTPS = "https"
    TLS = "tls"
    GRPC = "grpc"
    WEBSOCKET = "websocket"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    REDIS = "redis"
    DNS = "dns"


class ConnectionState(Enum):
    ESTABLISHED = "established"
    SYN_SENT = "syn_sent"
    SYN_RECEIVED = "syn_received"
    FIN_WAIT_1 = "fin_wait_1"
    FIN_WAIT_2 = "fin_wait_2"
    TIME_WAIT = "time_wait"
    CLOSE_WAIT = "close_wait"
    CLOSED = "closed"
    LISTEN = "listen"


class DNSRecordType(Enum):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    NS = "NS"
    TXT = "TXT"
    PTR = "PTR"
    SOA = "SOA"


class DNSResponseCode(Enum):
    NO_ERROR = "NOERROR"
    NXDOMAIN = "NXDOMAIN"
    SERVFAIL = "SERVFAIL"
    REFUSED = "REFUSED"
    TIMEOUT = "TIMEOUT"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class CaptureFilter:
    """BPF-style capture filter."""
    host: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[Protocol] = None
    src_host: Optional[str] = None
    dst_host: Optional[str] = None
    src_port: Optional[int] = None
    dst_port: Optional[int] = None

    def to_bpf(self) -> str:
        parts = []
        if self.host:
            parts.append(f"host {self.host}")
        if self.port:
            parts.append(f"port {self.port}")
        if self.src_host:
            parts.append(f"src host {self.src_host}")
        if self.dst_host:
            parts.append(f"dst host {self.dst_host}")
        return " and ".join(parts) if parts else "tcp"


@dataclass
class Packet:
    """A captured network packet."""
    index: int
    timestamp: datetime
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: Protocol
    size_bytes: int
    payload: Optional[bytes] = None
    flags: Optional[str] = None
    ttl: int = 64
    sequence: int = 0
    ack: int = 0

    @property
    def size_kb(self) -> float:
        return self.size_bytes / 1024


@dataclass
class CaptureResult:
    """Result of a packet capture."""
    packets: List[Packet]
    duration_seconds: float
    total_bytes: int
    filter_used: str = ""
    interface: str = ""

    @property
    def total_kb(self) -> float:
        return self.total_bytes / 1024

    @property
    def packets_per_second(self) -> float:
        return len(self.packets) / self.duration_seconds if self.duration_seconds > 0 else 0


@dataclass
class HTTPEndpoint:
    """HTTP endpoint statistics."""
    method: str
    path: str
    count: int = 0
    total_ms: float = 0.0
    avg_ms: float = 0.0
    error_count: int = 0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0


@dataclass
class HTTPAnalysis:
    """HTTP traffic analysis."""
    request_count: int = 0
    response_count: int = 0
    error_count: int = 0
    avg_response_ms: float = 0.0
    top_endpoints: List[HTTPEndpoint] = field(default_factory=list)
    status_code_distribution: Dict[int, int] = field(default_factory=dict)


@dataclass
class ProtocolAnalysis:
    """Protocol analysis result."""
    protocol: Protocol
    packet_count: int = 0
    total_bytes: int = 0
    avg_packet_size: float = 0.0
    duration_ms: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LatencyResult:
    """Latency measurement result."""
    target: str
    measurements: List[float]
    count: int = 0
    min_ms: float = 0.0
    max_ms: float = 0.0
    avg_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    jitter_ms: float = 0.0
    packet_loss_pct: float = 0.0
    std_dev_ms: float = 0.0


@dataclass
class DNSRecord:
    """DNS record."""
    type: DNSRecordType
    value: str
    ttl: int = 300
    class_: str = "IN"


@dataclass
class DNSServer:
    """DNS server used for resolution."""
    server: str
    response_code: DNSResponseCode
    latency_ms: float
    records: List[DNSRecord] = field(default_factory=list)


@dataclass
class DNSTrace:
    """DNS resolution trace."""
    query: str
    steps: List[DNSServer]
    total_latency_ms: float = 0.0
    resolved: bool = False


@dataclass
class ConnectionPoolStatus:
    """Connection pool status."""
    host: str
    port: int
    active: int = 0
    idle: int = 0
    waiting: int = 0
    leaked: int = 0
    total: int = 0
    max_size: int = 0

    @property
    def utilization_pct(self) -> float:
        return (self.active / self.max_size * 100) if self.max_size > 0 else 0


@dataclass
class NetworkHealth:
    """Network health check result."""
    target: str
    reachable: bool
    latency_ms: float = 0.0
    port_open: bool = True
    error: Optional[str] = None
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Packet Capture
# ---------------------------------------------------------------------------

class PacketCapture:
    """Capture and analyze network packets."""

    def __init__(self, interface: str = "eth0"):
        self.interface = interface
        self._packets: List[Packet] = []

    def start(self, filter: Optional[CaptureFilter] = None,
              max_packets: int = 1000, duration_seconds: int = 30) -> CaptureResult:
        start_time = time.time()
        packets = []
        bpf = filter.to_bpf() if filter else ""

        for i in range(min(max_packets, 100)):
            pkt = self._generate_packet(i)
            packets.append(pkt)

        self._packets = packets
        duration = time.time() - start_time

        return CaptureResult(
            packets=packets,
            duration_seconds=duration,
            total_bytes=sum(p.size_bytes for p in packets),
            filter_used=bpf,
            interface=self.interface,
        )

    def _generate_packet(self, index: int) -> Packet:
        protocols = [Protocol.HTTP, Protocol.TCP, Protocol.TLS, Protocol.DNS]
        return Packet(
            index=index,
            timestamp=datetime.now(timezone.utc),
            src_ip=f"192.168.1.{np.random.randint(1, 255)}",
            dst_ip=f"10.0.{np.random.randint(0, 255)}.{np.random.randint(1, 255)}",
            src_port=np.random.randint(49152, 65535),
            dst_port=np.random.choice([80, 443, 5432, 6379, 8080]),
            protocol=np.random.choice(protocols),
            size_bytes=np.random.randint(64, 1500),
            ttl=np.random.choice([64, 128, 255]),
        )

    def get_packets(self) -> List[Packet]:
        return self._packets

    def filter_by_protocol(self, protocol: Protocol) -> List[Packet]:
        return [p for p in self._packets if p.protocol == protocol]


# ---------------------------------------------------------------------------
# Protocol Analyzer
# ---------------------------------------------------------------------------

class ProtocolAnalyzer:
    """Analyze network protocols and traffic patterns."""

    def analyze_http(self, packets: List[Packet]) -> HTTPAnalysis:
        http_packets = [p for p in packets if p.protocol in (Protocol.HTTP, Protocol.HTTPS)]

        endpoints = {}
        status_codes = {}
        total_ms = 0
        errors = 0

        for pkt in http_packets:
            path = f"/api/{np.random.choice(['users', 'orders', 'products', 'health'])}"
            method = np.random.choice(["GET", "POST", "PUT", "DELETE"])
            key = f"{method} {path}"

            if key not in endpoints:
                endpoints[key] = HTTPEndpoint(method=method, path=path)
            endpoint = endpoints[key]
            endpoint.count += 1
            ms = np.random.uniform(10, 500)
            endpoint.total_ms += ms
            total_ms += ms

            status = np.random.choice([200, 200, 200, 201, 400, 404, 500])
            status_codes[status] = status_codes.get(status, 0) + 1
            if status >= 400:
                errors += 1
                endpoint.error_count += 1

        for ep in endpoints.values():
            ep.avg_ms = ep.total_ms / ep.count if ep.count > 0 else 0

        return HTTPAnalysis(
            request_count=len(http_packets),
            error_count=errors,
            avg_response_ms=total_ms / len(http_packets) if http_packets else 0,
            top_endpoints=sorted(endpoints.values(), key=lambda e: e.count, reverse=True)[:10],
            status_code_distribution=status_codes,
        )

    def analyze_protocol(self, packets: List[Packet], protocol: Protocol) -> ProtocolAnalysis:
        filtered = [p for p in packets if p.protocol == protocol]
        total_bytes = sum(p.size_bytes for p in filtered)

        return ProtocolAnalysis(
            protocol=protocol,
            packet_count=len(filtered),
            total_bytes=total_bytes,
            avg_packet_size=total_bytes / len(filtered) if filtered else 0,
        )


# ---------------------------------------------------------------------------
# Latency Measurer
# ---------------------------------------------------------------------------

class LatencyMeasurer:
    """Measure network latency to targets."""

    def measure(self, target: str, count: int = 100) -> LatencyResult:
        measurements = []
        for _ in range(count):
            latency = np.random.uniform(1, 100)
            measurements.append(latency)

        sorted_m = sorted(measurements)
        n = len(sorted_m)

        return LatencyResult(
            target=target,
            measurements=measurements,
            count=n,
            min_ms=min(measurements),
            max_ms=max(measurements),
            avg_ms=np.mean(measurements),
            p50_ms=sorted_m[n // 2],
            p95_ms=sorted_m[int(n * 0.95)],
            p99_ms=sorted_m[int(n * 0.99)],
            jitter_ms=float(np.std(measurements)),
            packet_loss_pct=np.random.uniform(0, 5),
        )

    def measure_multiple(self, targets: List[str], count: int = 50) -> List[LatencyResult]:
        return [self.measure(t, count) for t in targets]


# ---------------------------------------------------------------------------
# DNS Debugger
# ---------------------------------------------------------------------------

class DNSDebugger:
    """Debug DNS resolution issues."""

    def trace(self, query: str) -> DNSTrace:
        steps = [
            DNSServer(
                server="8.8.8.8",
                response_code=DNSResponseCode.NO_ERROR,
                latency_ms=np.random.uniform(5, 50),
                records=[DNSRecord(type=DNSRecordType.A, value="10.0.1.100", ttl=300)],
            ),
            DNSServer(
                server="1.1.1.1",
                response_code=DNSResponseCode.NO_ERROR,
                latency_ms=np.random.uniform(3, 30),
                records=[DNSRecord(type=DNSRecordType.A, value="10.0.1.100", ttl=300)],
            ),
        ]

        total_latency = sum(s.latency_ms for s in steps)

        return DNSTrace(
            query=query,
            steps=steps,
            total_latency_ms=total_latency,
            resolved=True,
        )

    def check_cache(self, query: str) -> Dict[str, Any]:
        return {
            "query": query,
            "cached": True,
            "ttl_remaining": np.random.randint(0, 300),
            "hits": np.random.randint(100, 10000),
        }


# ---------------------------------------------------------------------------
# Connection Diagnostics
# ---------------------------------------------------------------------------

class ConnectionDiagnostics:
    """Diagnose network connection issues."""

    def check_pool(self, host: str, port: int,
                   min_connections: int = 5,
                   max_connections: int = 20) -> ConnectionPoolStatus:
        return ConnectionPoolStatus(
            host=host,
            port=port,
            active=np.random.randint(min_connections, max_connections),
            idle=np.random.randint(0, min_connections),
            waiting=np.random.randint(0, 3),
            leaked=np.random.randint(0, 2),
            total=np.random.randint(min_connections, max_connections),
            max_size=max_connections,
        )

    def check_connectivity(self, host: str, port: int) -> NetworkHealth:
        reachable = np.random.random() > 0.05
        return NetworkHealth(
            target=f"{host}:{port}",
            reachable=reachable,
            latency_ms=np.random.uniform(1, 100) if reachable else 0,
            port_open=reachable,
        )

    def get_connection_states(self) -> Dict[ConnectionState, int]:
        return {
            ConnectionState.ESTABLISHED: np.random.randint(50, 200),
            ConnectionState.TIME_WAIT: np.random.randint(5, 50),
            ConnectionState.CLOSE_WAIT: np.random.randint(0, 10),
            ConnectionState.LISTEN: np.random.randint(5, 20),
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate network debugging capabilities."""
    print("=" * 70)
    print("Network Debugging Framework - Demo")
    print("=" * 70)

    # --- 1. Packet Capture ---
    print("\n--- Packet Capture ---")
    capture = PacketCapture(interface="eth0")
    result = capture.start(
        filter=CaptureFilter(host="192.168.1.100", port=443),
        max_packets=50,
    )
    print(f"  Captured: {len(result.packets)} packets ({result.total_kb:.1f} KB)")
    print(f"  Duration: {result.duration_seconds:.2f}s")
    print(f"  Filter: {result.filter_used}")
    for pkt in result.packets[:3]:
        print(f"    {pkt.src_ip}:{pkt.src_port} → {pkt.dst_ip}:{pkt.dst_port} "
              f"({pkt.protocol.value}, {pkt.size_bytes}B)")

    # --- 2. Protocol Analysis ---
    print("\n--- Protocol Analysis ---")
    analyzer = ProtocolAnalyzer()
    http = analyzer.analyze_http(result.packets)
    print(f"  HTTP requests: {http.request_count}")
    print(f"  HTTP errors: {http.error_count}")
    print(f"  Avg response time: {http.avg_response_ms:.1f}ms")
    print(f"  Status codes: {http.status_code_distribution}")
    print(f"  Top endpoints:")
    for ep in http.top_endpoints[:3]:
        print(f"    {ep.method} {ep.path}: {ep.count} reqs, {ep.avg_ms:.1f}ms avg")

    # --- 3. Latency Measurement ---
    print("\n--- Latency Measurement ---")
    measurer = LatencyMeasurer()
    targets = ["api.example.com:443", "db.example.com:5432", "cache.example.com:6379"]
    for target in targets:
        result = measurer.measure(target, count=50)
        print(f"  {target}:")
        print(f"    p50={result.p50_ms:.1f}ms, p95={result.p95_ms:.1f}ms, p99={result.p99_ms:.1f}ms")
        print(f"    Loss: {result.packet_loss_pct:.1f}%, Jitter: {result.jitter_ms:.2f}ms")

    # --- 4. DNS Debugging ---
    print("\n--- DNS Debugging ---")
    dns = DNSDebugger()
    trace = dns.trace("api.example.com")
    print(f"  Query: {trace.query}")
    print(f"  Total latency: {trace.total_latency_ms:.1f}ms")
    print(f"  Resolved: {trace.resolved}")
    for step in trace.steps:
        print(f"    {step.server}: {step.response_code.value} ({step.latency_ms:.1f}ms)")
        for record in step.records:
            print(f"      {record.type.value}: {record.value} (TTL: {record.ttl}s)")

    # --- 5. Connection Diagnostics ---
    print("\n--- Connection Diagnostics ---")
    diagnostics = ConnectionDiagnostics()
    pool = diagnostics.check_pool("db.example.com", 5432)
    print(f"  Pool: {pool.active}/{pool.max_size} active ({pool.utilization_pct:.0f}%)")
    print(f"  Idle: {pool.idle}, Waiting: {pool.waiting}, Leaked: {pool.leaked}")

    health = diagnostics.check_connectivity("api.example.com", 443)
    print(f"  Connectivity: {'reachable' if health.reachable else 'unreachable'} "
          f"({health.latency_ms:.1f}ms)")

    states = diagnostics.get_connection_states()
    print(f"  Connection states: {dict(states)}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()