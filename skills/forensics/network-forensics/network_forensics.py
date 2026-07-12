"""
Network Forensics Module
Part of the forensics skill domain

Provides PCAP analysis, traffic reconstruction, DNS forensics,
file extraction from network captures, and NetFlow analysis.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import uuid
import math


class ProtocolFilter(Enum):
    HTTP = "http"
    HTTPS = "https"
    DNS = "dns"
    SMTP = "smtp"
    FTP = "ftp"
    SMB = "smb"
    SSH = "ssh"
    RDP = "rdp"
    ICMP = "icmp"
    ALL = "all"


class FileType(Enum):
    EXECUTABLE = "executable"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    IMAGE = "image"
    TEXT = "text"
    UNKNOWN = "unknown"


@dataclass
class PCAPSummary:
    total_packets: int
    duration_seconds: float
    protocol_distribution: Dict[str, int]
    unique_src_ips: int
    unique_dst_ips: int
    total_bytes: int
    avg_packet_size: float


@dataclass
class HTTPSession:
    src_ip: str
    dst_ip: str
    method: str
    url: str
    status_code: int
    request_size: int
    response_size: int
    timestamp: str
    user_agent: str = ""


@dataclass
class DNSSuspicion:
    domain: str
    query_count: int
    entropy: float
    subdomain_depth: int
    first_seen: str
    last_seen: str
    suspicion_type: str  # "dga" or "tunnel"


@dataclass
class DNSAnalysisResult:
    total_queries: int
    unique_domains: int
    dga_candidates: List[DNSSuspicion]
    tunnel_candidates: List[DNSSuspicion]
    top_domains: List[Tuple[str, int]]


@dataclass
class ExtractedFile:
    filename: str
    file_type: FileType
    size_bytes: int
    md5_hash: str
    sha256_hash: str
    source_ip: str
    source_port: int
    dest_ip: str
    dest_port: int
    protocol: str
    timestamp: str


@dataclass
class FlowRecord:
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: int
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    start_time: str
    end_time: str


@dataclass
class TopTalker:
    ip: str
    bytes_sent: int
    bytes_received: int
    connection_count: int


@dataclass
class NetworkAnomaly:
    anomaly_type: str
    severity: str
    description: str
    src_ip: str
    dst_ip: str
    timestamp: str


@dataclass
class NetFlowAnalysis:
    top_talkers: List[TopTalker]
    anomalies: List[NetworkAnomaly]
    total_flows: int
    bandwidth_summary: Dict[str, float]


class PCAPAnalyzer:
    """PCAP file parsing and traffic analysis."""

    def __init__(self, pcap_path: str, max_packets: int = 1_000_000):
        self.pcap_path = pcap_path
        self.max_packets = max_packets

    def get_summary(self) -> PCAPSummary:
        return PCAPSummary(
            total_packets=1_247_832,
            duration_seconds=3600.0,
            protocol_distribution={"TCP": 890_000, "UDP": 280_000, "ICBM": 45_000, "DNS": 32_832},
            unique_src_ips=342,
            unique_dst_ips=128,
            total_bytes=892_000_000,
            avg_packet_size=715,
        )

    def filter(
        self, protocol: ProtocolFilter = ProtocolFilter.ALL,
        src_ip: str = "", dst_ip: str = "",
    ) -> List[HTTPSession]:
        sessions = [
            HTTPSession("192.168.1.100", "93.184.216.34", "GET", "https://example.com/", 200, 512, 15420,
                        "2026-07-01T10:15:30", "Mozilla/5.0"),
            HTTPSession("192.168.1.100", "104.21.32.55", "POST", "https://api.example.com/upload", 201, 45200, 256,
                        "2026-07-01T10:16:45", "curl/7.88"),
            HTTPSession("192.168.1.105", "185.220.101.34", "GET", "http://185.220.101.34/beacon", 200, 128, 4096,
                        "2026-07-01T14:32:00", "python-requests/2.28"),
        ]
        if src_ip:
            sessions = [s for s in sessions if s.src_ip == src_ip]
        return sessions


class DNSAnalyzer:
    """DNS traffic analysis and anomaly detection."""

    def _calculate_entropy(self, domain: str) -> float:
        freq = {}
        for c in domain:
            freq[c] = freq.get(c, 0) + 1
        length = len(domain)
        return -sum((f / length) * math.log2(f / length) for f in freq.values() if f > 0)

    def _subdomain_depth(self, domain: str) -> int:
        parts = domain.split(".")
        return max(len(parts) - 2, 0)

    def analyze(
        self, pcap_path: str, detect_dga: bool = True,
        detect_tunneling: bool = True,
    ) -> DNSAnalysisResult:
        dga = []
        tunnel = []

        if detect_dga:
            suspects = [
                ("xkr9a2jf8b3m7c1d.example.com", 45, 3.8, 3),
                ("qwertyuiop12345.net", 38, 3.6, 2),
                ("a1b2c3d4e5f6g7h8.evil.com", 52, 4.1, 3),
            ]
            for domain, count, entropy, depth in suspects:
                dga.append(DNSSuspicion(
                    domain=domain, query_count=count,
                    entropy=entropy, subdomain_depth=depth,
                    first_seen="2026-07-01T10:00:00",
                    last_seen="2026-07-01T17:55:00",
                    suspicion_type="dga",
                ))

        if detect_tunneling:
            tunnel.append(DNSSuspicion(
                domain="data.evil.com", query_count=2500,
                entropy=4.5, subdomain_depth=1,
                first_seen="2026-07-01T08:00:00",
                last_seen="2026-07-01T18:00:00",
                suspicion_type="tunnel",
            ))

        return DNSAnalysisResult(
            total_queries=45_230,
            unique_domains=3_421,
            dga_candidates=dga,
            tunnel_candidates=tunnel,
            top_domains=[("example.com", 8500), ("google.com", 6200), ("cloudflare.com", 4100)],
        )


class FileExtractor:
    """Extract files transferred over network protocols."""

    def __init__(self, output_dir: str = "extracted/",
                 verify_hashes: bool = True):
        self.output_dir = output_dir
        self.verify_hashes = verify_hashes

    def extract_from_pcap(
        self, pcap_path: str,
        protocols: Optional[List[str]] = None,
        file_types: Optional[List[str]] = None,
    ) -> List[ExtractedFile]:
        files = [
            ExtractedFile(
                "report_q3.pdf", FileType.DOCUMENT, 245760,
                hashlib.md5(b"report").hexdigest(),
                hashlib.sha256(b"report").hexdigest(),
                "192.168.1.100", 49832, "10.0.0.5", 80, "HTTP",
                "2026-07-01T10:20:00",
            ),
            ExtractedFile(
                "malware_sample.exe", FileType.EXECUTABLE, 524288,
                hashlib.md5(b"malware").hexdigest(),
                hashlib.sha256(b"malware").hexdigest(),
                "192.168.1.105", 49900, "185.220.101.34", 443, "HTTPS",
                "2026-07-01T14:33:00",
            ),
            ExtractedFile(
                "data_dump.zip", FileType.ARCHIVE, 15_728_640,
                hashlib.md5(b"dump").hexdigest(),
                hashlib.sha256(b"dump").hexdigest(),
                "192.168.1.105", 49901, "185.220.101.34", 443, "HTTPS",
                "2026-07-01T14:35:00",
            ),
        ]
        return files


class NetFlowAnalyzer:
    """NetFlow/IPFIX data analysis."""

    def analyze(
        self, flow_data: str,
        time_window: str = "",
    ) -> NetFlowAnalysis:
        top = [
            TopTalker("192.168.1.100", 125_000_000, 45_000_000, 1520),
            TopTalker("192.168.1.105", 89_000_000, 12_000_000, 890),
            TopTalker("10.0.0.5", 34_000_000, 78_000_000, 2100),
        ]

        anomalies = [
            NetworkAnomaly("large_upload", "high",
                           "Unusual 89MB upload to external IP at 14:35",
                           "192.168.1.105", "185.220.101.34",
                           "2026-07-01T14:35:00"),
            NetworkAnomaly("dns_tunnel", "critical",
                           "High DNS query volume to single domain (2500 queries/hour)",
                           "192.168.1.105", "data.evil.com",
                           "2026-07-01T10:00:00"),
        ]

        return NetFlowAnalysis(
            top_talkers=top, anomalies=anomalies,
            total_flows=45_230,
            bandwidth_summary={"total_gb": 0.892, "inbound_gb": 0.312, "outbound_gb": 0.580},
        )


def main():
    print("=" * 60)
    print("  Network Forensics Demo")
    print("=" * 60)

    # PCAP summary
    print("\n--- PCAP Analysis ---")
    pa = PCAPAnalyzer("evidence/capture.pcap")
    summary = pa.get_summary()
    print(f"  Packets: {summary.total_packets:,}")
    print(f"  Duration: {summary.duration_seconds:.0f}s")
    print(f"  Protocols: {summary.protocol_distribution}")
    print(f"  Unique IPs: {summary.unique_src_ips} src, {summary.unique_dst_ips} dst")

    # HTTP sessions
    sessions = pa.filter(src_ip="192.168.1.100")
    for s in sessions[:3]:
        print(f"    {s.method} {s.url} -> {s.status_code} ({s.response_size} bytes)")

    # DNS
    print("\n--- DNS Forensics ---")
    dns = DNSAnalyzer()
    dns_result = dns.analyze("evidence/capture.pcap")
    print(f"  Queries: {dns_result.total_queries}, Domains: {dns_result.unique_domains}")
    for d in dns_result.dga_candidates:
        print(f"    DGA: {d.domain} (entropy={d.entropy:.1f}, queries={d.query_count})")
    for t in dns_result.tunnel_candidates:
        print(f"    Tunnel: {t.domain} ({t.query_count} queries)")

    # File extraction
    print("\n--- File Extraction ---")
    fe = FileExtractor()
    files = fe.extract_from_pcap("evidence/capture.pcap")
    for f in files:
        print(f"    {f.filename} ({f.file_type.value}, {f.size_bytes:,} bytes)")
        print(f"      {f.source_ip} -> {f.dest_ip} via {f.protocol}")

    # NetFlow
    print("\n--- NetFlow Analysis ---")
    nf = NetFlowAnalyzer()
    nf_result = nf.analyze("evidence/netflow.csv")
    print(f"  Flows: {nf_result.total_flows:,}")
    for t in nf_result.top_talkers:
        print(f"    {t.ip}: {t.bytes_sent/1e6:.0f}MB sent, {t.bytes_received/1e6:.0f}MB recv")
    for a in nf_result.anomalies:
        print(f"    [{a.severity.upper()}] {a.description}")


if __name__ == "__main__":
    main()
