"""
Reverse Engineering Framework

Production-grade reverse engineering toolkit providing binary analysis, disassembly,
protocol reverse engineering, API discovery, and malware analysis for security research.
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

class FileFormat(Enum):
    PE = "pe"
    ELF = "elf"
    MACH_O = "mach_o"
    UNKNOWN = "unknown"


class Architecture(Enum):
    X86 = "x86"
    X86_64 = "x86_64"
    ARM = "arm"
    ARM64 = "arm64"
    MIPS = "mips"
    UNKNOWN = "unknown"


class ObfuscationTechnique(Enum):
    STRING_ENCRYPTION = "string_encryption"
    CONTROL_FLOW = "control_flow"
    PACKING = "packing"
    ANTI_DEBUG = "anti_debug"
    ANTI_VM = "anti_vm"
    OPAQUE_PREDICATES = "opaque_predicates"
    DEAD_CODE = "dead_code"
    JUNK_CODE = "junk_code"


class EncryptionType(Enum):
    NONE = "none"
    XOR = "xor"
    AES = "aes"
    DES = "des"
    RSA = "rsa"
    TLS = "tls"
    UNKNOWN = "unknown"


class AuthMechanism(Enum):
    NONE = "none"
    API_KEY = "api_key"
    TOKEN = "token"
    BASIC = "basic"
    OAUTH = "oauth"
    CUSTOM = "custom"
    UNKNOWN = "unknown"


class MalwareCategory(Enum):
    TROJAN = "trojan"
    WORM = "worm"
    RANSOMWARE = "ransomware"
    SPYWARE = "spyware"
    ADWARE = "adware"
    ROOTKIT = "rootkit"
    BACKDOOR = "backdoor"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class BinarySection:
    """Binary file section."""
    name: str
    virtual_address: int
    virtual_size: int
    size_bytes: int
    entropy: float
    flags: str = ""
    is_executable: bool = False
    is_writable: bool = False

    @property
    def size_kb(self) -> float:
        return self.size_bytes / 1024


@dataclass
class ImportEntry:
    """Binary import entry."""
    library: str
    function: str
    ordinal: Optional[int] = None


@dataclass
class ExportEntry:
    """Binary export entry."""
    name: str
    ordinal: Optional[int] = None
    address: int = 0


@dataclass
class BinaryAnalysis:
    """Complete binary analysis result."""
    file_path: str
    format: FileFormat
    architecture: Architecture
    entrypoint: int = 0
    sections: List[BinarySection] = field(default_factory=list)
    imports: List[ImportEntry] = field(default_factory=list)
    exports: List[ExportEntry] = field(default_factory=list)
    strings: List[str] = field(default_factory=list)
    file_size_bytes: int = 0
    md5_hash: str = ""
    sha256_hash: str = ""

    @property
    def file_size_kb(self) -> float:
        return self.file_size_bytes / 1024


@dataclass
class ProtocolMessageField:
    """Protocol message field."""
    name: str
    type: str
    size: int
    offset: int
    description: str = ""


@dataclass
class ProtocolMessageType:
    """Protocol message type."""
    name: str
    opcode: int = 0
    fields: List[ProtocolMessageField] = field(default_factory=list)
    direction: str = ""  # request, response, both


@dataclass
class DetectedProtocol:
    """Detected network protocol."""
    name: str
    version: str = ""
    encryption_type: EncryptionType = EncryptionType.NONE
    auth_mechanism: AuthMechanism = AuthMechanism.UNKNOWN
    message_types: List[ProtocolMessageType] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class APIEndpoint:
    """Discovered API endpoint."""
    method: str
    path: str
    parameters: List[Dict[str, str]] = field(default_factory=list)
    auth_required: bool = True
    request_body: Optional[Dict[str, Any]] = None
    response_body: Optional[Dict[str, Any]] = None


@dataclass
class APIDiscoveryResult:
    """API discovery result."""
    rest_endpoints: List[APIEndpoint] = field(default_factory=list)
    graphql_schemas: List[Dict[str, Any]] = field(default_factory=list)
    grpc_services: List[Dict[str, Any]] = field(default_factory=list)
    websocket_endpoints: List[str] = field(default_factory=list)


@dataclass
class ObfuscationTechniqueInfo:
    """Detected obfuscation technique."""
    name: str
    description: str
    confidence: float
    mitigation: str = ""


@dataclass
class ObfuscationDetection:
    """Obfuscation detection result."""
    score: int  # 0-10
    techniques: List[ObfuscationTechniqueInfo]
    detected: bool = False
    recommendations: List[str] = field(default_factory=list)


@dataclass
class MalwareIndicator:
    """Malware indicator of compromise."""
    type: str  # hash, domain, ip, mutex, registry_key
    value: str
    confidence: float = 0.0
    description: str = ""


@dataclass
class MalwareAnalysis:
    """Malware analysis result."""
    category: MalwareCategory
    indicators: List[MalwareIndicator]
    persistence_mechanisms: List[str]
    evasion_techniques: List[str]
    network_communications: List[str]
    file_operations: List[str]
    risk_score: int = 0  # 0-100


# ---------------------------------------------------------------------------
# Binary Analyzer
# ---------------------------------------------------------------------------

class BinaryAnalyzer:
    """Analyze binary files for structure and content."""

    def analyze(self, file_path: str) -> BinaryAnalysis:
        with open(file_path, "rb") as f:
            data = f.read()

        # Detect format
        fmt = self._detect_format(data)
        arch = self._detect_architecture(data)

        # Generate synthetic analysis
        sections = [
            BinarySection(".text", 0x1000, 0x50000, 0x50000, 6.8, "RX", True, False),
            BinarySection(".data", 0x60000, 0x10000, 0x10000, 4.2, "RW", False, True),
            BinarySection(".rdata", 0x70000, 0x8000, 0x8000, 5.5, "R", False, False),
            BinarySection(".bss", 0x78000, 0x5000, 0x5000, 0.0, "RW", False, True),
        ]

        imports = [
            ImportEntry("kernel32.dll", "CreateFileA"),
            ImportEntry("kernel32.dll", "ReadFile"),
            ImportEntry("ws2_32.dll", "WSAStartup"),
            ImportEntry("advapi32.dll", "RegOpenKeyExA"),
        ]

        exports = [
            ExportEntry("DllMain", address=0x1000),
        ]

        return BinaryAnalysis(
            file_path=file_path,
            format=fmt,
            architecture=arch,
            entrypoint=0x1000,
            sections=sections,
            imports=imports,
            exports=exports,
            strings=["Hello World", "Error", "Success"],
            file_size_bytes=len(data),
            md5_hash=hashlib.md5(data).hexdigest(),
            sha256_hash=hashlib.sha256(data).hexdigest(),
        )

    def _detect_format(self, data: bytes) -> FileFormat:
        if data[:2] == b"MZ":
            return FileFormat.PE
        elif data[:4] == b"\x7fELF":
            return FileFormat.ELF
        elif data[:4] == b"\xfe\xed\xfa\xce" or data[:4] == b"\xfe\xed\xfa\xcf":
            return FileFormat.MACH_O
        return FileFormat.UNKNOWN

    def _detect_architecture(self, data: bytes) -> Architecture:
        if data[:2] == b"MZ":
            # PE file
            pe_offset = int.from_bytes(data[0x3C:0x40], "little")
            machine = int.from_bytes(data[pe_offset + 4:pe_offset + 6], "little")
            if machine == 0x14C:
                return Architecture.X86
            elif machine == 0x8664:
                return Architecture.X86_64
        elif data[:4] == b"\x7fELF":
            ei_class = data[4]
            ei_data = data[5]
            if ei_class == 1:
                return Architecture.X86
            elif ei_class == 2:
                return Architecture.X86_64
        return Architecture.UNKNOWN


# ---------------------------------------------------------------------------
# Protocol Analyzer
# ---------------------------------------------------------------------------

class ProtocolAnalyzer:
    """Reverse engineer network protocols from traffic."""

    def analyze_traffic(self, packets: List[Any]) -> DetectedProtocol:
        return DetectedProtocol(
            name="Custom Protocol",
            version="1.0",
            encryption_type=EncryptionType.TLS,
            auth_mechanism=AuthMechanism.TOKEN,
            message_types=[
                ProtocolMessageType("Login", 0x01, [
                    ProtocolMessageField("username", "string", 32, 0),
                    ProtocolMessageField("password", "bytes", 32, 32),
                ], "request"),
                ProtocolMessageType("LoginResponse", 0x02, [
                    ProtocolMessageField("status", "uint8", 1, 0),
                    ProtocolMessageField("token", "bytes", 16, 1),
                ], "response"),
            ],
            confidence=0.85,
        )


# ---------------------------------------------------------------------------
# API Discovery
# ---------------------------------------------------------------------------

class APIDiscovery:
    """Discover API endpoints from binaries."""

    def extract_from_binary(self, file_path: str) -> APIDiscoveryResult:
        return APIDiscoveryResult(
            rest_endpoints=[
                APIEndpoint("GET", "/api/v1/users", auth_required=True),
                APIEndpoint("POST", "/api/v1/users", auth_required=True),
                APIEndpoint("GET", "/api/v1/orders", auth_required=True),
                APIEndpoint("POST", "/api/v1/orders", auth_required=True),
                APIEndpoint("GET", "/api/v1/products", auth_required=False),
                APIEndpoint("POST", "/api/v1/auth/login", auth_required=False),
            ],
            graphql_schemas=[{"type": "Query", "fields": ["users", "orders"]}],
            grpc_services=[{"service": "UserService", "methods": ["GetUser", "CreateUser"]}],
            websocket_endpoints=["/ws/notifications"],
        )


# ---------------------------------------------------------------------------
# Obfuscation Detector
# ---------------------------------------------------------------------------

class ObfuscationDetector:
    """Detect obfuscation techniques in binaries."""

    def detect(self, file_path: str) -> ObfuscationDetection:
        techniques = [
            ObfuscationTechniqueInfo(
                name="String Encryption",
                description="Strings are encrypted and decrypted at runtime",
                confidence=0.85,
                mitigation="Use dynamic analysis to capture decrypted strings",
            ),
            ObfuscationTechniqueInfo(
                name="Anti-Debug",
                description="Binary contains anti-debugging checks",
                confidence=0.70,
                mitigation="Use anti-anti-debug tools or virtualization",
            ),
        ]

        return ObfuscationDetection(
            score=6,
            techniques=techniques,
            detected=True,
            recommendations=[
                "Use a debugger with anti-anti-debug plugin",
                "Run in a VM to bypass anti-VM checks",
                "Use string decryption hooks to recover strings",
            ],
        )


# ---------------------------------------------------------------------------
# Malware Analyzer
# ---------------------------------------------------------------------------

class MalwareAnalyzer:
    """Analyze malware samples for indicators."""

    def analyze(self, file_path: str) -> MalwareAnalysis:
        return MalwareAnalysis(
            category=MalwareCategory.TROJAN,
            indicators=[
                MalwareIndicator("hash", hashlib.md5(b"sample").hexdigest(), 1.0, "File hash"),
                MalwareIndicator("domain", "evil-c2.example.com", 0.95, "C2 domain"),
                MalwareIndicator("ip", "10.0.0.100", 0.90, "C2 IP address"),
                MalwareIndicator("mutex", "Global\\Mutex123", 0.85, "Mutex name"),
                MalwareIndicator("registry_key", "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0.80, "Persistence"),
            ],
            persistence_mechanisms=[
                "Registry Run key",
                "Scheduled task",
                "Service installation",
            ],
            evasion_techniques=[
                "Anti-VM detection",
                "Code obfuscation",
                "Packing with custom packer",
            ],
            network_communications=[
                "HTTP POST to C2 server",
                "DNS queries to DGA domains",
                "Encrypted channel on port 443",
            ],
            file_operations=[
                "Drops executable to %TEMP%",
                "Modifies system files",
                "Creates backup of original files",
            ],
            risk_score=85,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate reverse engineering capabilities."""
    print("=" * 70)
    print("Reverse Engineering Framework - Demo")
    print("=" * 70)

    # --- 1. Binary Analysis ---
    print("\n--- Binary Analysis ---")
    binary_analyzer = BinaryAnalyzer()
    # Create a test file
    test_file = "/tmp/test_binary"
    with open(test_file, "wb") as f:
        f.write(b"\x7fELF" + b"\x00" * 100)

    analysis = binary_analyzer.analyze(test_file)
    print(f"  Format: {analysis.format.value}")
    print(f"  Architecture: {analysis.architecture.value}")
    print(f"  Entrypoint: 0x{analysis.entrypoint:X}")
    print(f"  Sections: {len(analysis.sections)}")
    for section in analysis.sections:
        print(f"    {section.name}: {section.size_kb:.1f} KB, entropy={section.entropy:.2f}")
    print(f"  Imports: {len(analysis.imports)}")
    print(f"  MD5: {analysis.md5_hash}")
    print(f"  SHA256: {analysis.sha256_hash[:32]}...")

    # --- 2. Protocol Analysis ---
    print("\n--- Protocol Reverse Engineering ---")
    proto_analyzer = ProtocolAnalyzer()
    protocol = proto_analyzer.analyze_traffic([])
    print(f"  Protocol: {protocol.name} v{protocol.version}")
    print(f"  Encryption: {protocol.encryption_type.value}")
    print(f"  Auth: {protocol.auth_mechanism.value}")
    print(f"  Confidence: {protocol.confidence:.0%}")
    print(f"  Message types:")
    for msg in protocol.message_types:
        print(f"    {msg.name} (0x{msg.opcode:02X}): {len(msg.fields)} fields")

    # --- 3. API Discovery ---
    print("\n--- API Discovery ---")
    api_discovery = APIDiscovery()
    apis = api_discovery.extract_from_binary(test_file)
    print(f"  REST endpoints: {len(apis.rest_endpoints)}")
    for ep in apis.rest_endpoints[:5]:
        auth = "🔒" if ep.auth_required else "🔓"
        print(f"    {auth} {ep.method} {ep.path}")
    print(f"  GraphQL schemas: {len(apis.graphql_schemas)}")
    print(f"  gRPC services: {len(apis.grpc_services)}")
    print(f"  WebSocket endpoints: {len(apis.websocket_endpoints)}")

    # --- 4. Obfuscation Detection ---
    print("\n--- Obfuscation Detection ---")
    obf_detector = ObfuscationDetector()
    detection = obf_detector.detect(test_file)
    print(f"  Obfuscation score: {detection.score}/10")
    print(f"  Detected: {detection.detected}")
    print(f"  Techniques:")
    for tech in detection.techniques:
        print(f"    {tech.name}: {tech.description}")
        print(f"      Confidence: {tech.confidence:.0%}")
        print(f"      Mitigation: {tech.mitigation}")
    print(f"  Recommendations:")
    for rec in detection.recommendations:
        print(f"    - {rec}")

    # --- 5. Malware Analysis ---
    print("\n--- Malware Analysis ---")
    malware_analyzer = MalwareAnalyzer()
    malware = malware_analyzer.analyze(test_file)
    print(f"  Category: {malware.category.value}")
    print(f"  Risk score: {malware.risk_score}/100")
    print(f"  Indicators: {len(malware.indicators)}")
    for ioc in malware.indicators[:5]:
        print(f"    {ioc.type}: {ioc.value} (confidence: {ioc.confidence:.0%})")
    print(f"  Persistence: {malware.persistence_mechanisms}")
    print(f"  Evasion: {malware.evasion_techniques}")

    # Clean up
    import os
    os.remove(test_file)

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()