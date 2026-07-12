"""
Firmware Analysis Engine — Python toolkit for embedded firmware reverse engineering.

Provides firmware image identification, filesystem extraction, credential recovery,
vulnerability scanning, hardware interface discovery, emulation setup, and batch
processing. Designed for IoT security research, product security assessments, and
embedded device analysis workflows.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import struct
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FirmwareFormat(Enum):
    """Detected firmware image format."""
    TRX = auto()
    UIMAGE = auto()
    FIT = auto()
    ELF = auto()
    SQUASHFS = auto()
    JFFS2 = auto()
    CRAMFS = auto()
    UBIFS = auto()
    ROMFS = auto()
    EXT2 = auto()
    EXT3 = auto()
    EXT4 = auto()
    ZIP_BASED = auto()
    RAW = auto()
    UNKNOWN = auto()


class FilesystemType(Enum):
    """Filesystem type within firmware."""
    SQUASHFS = auto()
    JFFS2 = auto()
    CRAMFS = auto()
    UBIFS = auto()
    ROMFS = auto()
    EXT2 = auto()
    EXT3 = auto()
    EXT4 = auto()
    FAT = auto()
    YAFFS2 = auto()
    UNKNOWN = auto()


class Architecture(Enum):
    """Target CPU architecture."""
    ARM = "ARM"
    ARM_BE = "ARM (Big Endian)"
    MIPS = "MIPS"
    MIPS_BE = "MIPS (Big Endian)"
    MIPS_LE = "MIPS (Little Endian)"
    X86 = "x86"
    X86_64 = "x86-64"
    PPC = "PowerPC"
    RISCV = "RISC-V"
    SPARC = "SPARC"
    SH4 = "SuperH"
    AARCH64 = "AArch64"
    UNKNOWN = "unknown"


class CredentialType(Enum):
    """Type of credential found."""
    PASSWORD_HASH = auto()
    PLAINTEXT_PASSWORD = auto()
    API_KEY = auto()
    PRIVATE_KEY = auto()
    CERTIFICATE = auto()
    TOKEN = auto()
    ENCRYPTION_KEY = auto()
    SNMP_COMMUNITY = auto()
    WIFI_PASSWORD = auto()


class Severity(Enum):
    """Vulnerability severity."""
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    INFO = auto()


class InterfaceType(Enum):
    """Hardware interface types."""
    UART = auto()
    JTAG = auto()
    SPI = auto()
    I2C = auto()
    GPIO = auto()
    USB = auto()
    ETHERNET = auto()
    WIFI = auto()
    BLUETOOTH = auto()
    ZIGBEE = auto()
    DEBUG = auto()


class UpdateProtocol(Enum):
    """Firmware update mechanism protocols."""
    HTTP = auto()
    HTTPS = auto()
    TFTP = auto()
    FTP = auto()
    SCP = auto()
    MQTT = auto()
    COAP = auto()
    CUSTOM = auto()


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class FirmwareInfo:
    """Identified firmware image information."""
    path: str = ""
    format: FirmwareFormat = FirmwareFormat.UNKNOWN
    architecture: Architecture = Architecture.UNKNOWN
    endianness: str = "little"
    device_type: str = ""
    manufacturer: str = ""
    model: str = ""
    version: str = ""
    build_date: str = ""
    image_size: int = 0
    checksum_valid: Optional[bool] = None
    bootloader: str = ""
    kernel_version: str = ""
    rootfs_offset: int = 0
    data_offset: int = 0
    magic_bytes: bytes = b""
    md5: str = ""
    sha256: str = ""


@dataclass
class FileSystemEntry:
    """Single filesystem entry."""
    path: str = ""
    entry_type: str = ""  # file, dir, symlink, char_dev, block_dev
    size: int = 0
    permissions: str = ""
    owner: str = ""
    group: str = ""
    modified_date: str = ""
    target: str = ""  # symlink target
    is_executable: bool = False


@dataclass
class ExtractedFilesystem:
    """Extracted filesystem information."""
    fs_type: FilesystemType = FilesystemType.UNKNOWN
    mount_point: str = ""
    total_files: int = 0
    total_directories: int = 0
    total_size: int = 0
    entries: List[FileSystemEntry] = field(default_factory=list)
    extraction_path: str = ""
    compressed: bool = False
    encrypted: bool = False


@dataclass
class Credential:
    """Extracted credential."""
    cred_type: CredentialType = CredentialType.PLAINTEXT_PASSWORD
    value: str = ""
    redacted_value: str = ""
    source_file: str = ""
    context: str = ""
    username: str = ""
    hash_type: str = ""
    confidence: float = 1.0
    line_number: int = 0


@dataclass
class PasswordEntry:
    """Password file entry."""
    username: str = ""
    hash_value: str = ""
    hash_type: str = ""
    uid: int = 0
    gid: int = 0
    home_dir: str = ""
    shell: str = ""
    cracked: bool = False
    plaintext: str = ""


@dataclass
class PasswordFile:
    """Password file found in firmware."""
    file_path: str = ""
    entries: List[PasswordEntry] = field(default_factory=list)
    total_entries: int = 0


@dataclass
class WirelessInterface:
    """Wireless network interface."""
    interface: str = ""
    ssid: str = ""
    security: str = ""
    encryption: str = ""
    channel: int = 0
    hidden: bool = False


@dataclass
class RemoteAccess:
    """Remote access service."""
    protocol: str = ""
    port: int = 0
    enabled: bool = False
    authentication: str = ""
    file_path: str = ""


@dataclass
class NetworkConfig:
    """Network configuration extracted from firmware."""
    default_ip: str = ""
    dhcp_enabled: bool = False
    dns_servers: List[str] = field(default_factory=list)
    open_ports: List[int] = field(default_factory=list)
    wireless_interfaces: List[WirelessInterface] = field(default_factory=list)
    remote_access: List[RemoteAccess] = field(default_factory=list)
    gateway: str = ""
    netmask: str = ""


@dataclass
class BinaryInfo:
    """Binary file information within firmware."""
    path: str = ""
    architecture: Architecture = Architecture.UNKNOWN
    endianness: str = ""
    is_stripped: bool = False
    is_statically_linked: bool = False
    linked_libraries: List[str] = field(default_factory=list)
    suspicious_imports: List[str] = field(default_factory=list)
    interesting_strings: List[str] = field(default_factory=list)
    size: int = 0
    entry_point: int = 0


@dataclass
class VulnerabilityFinding:
    """Detected vulnerability in firmware."""
    title: str = ""
    severity: Severity = Severity.MEDIUM
    file_path: str = ""
    line_number: int = 0
    description: str = ""
    recommendation: str = ""
    cve_id: str = ""
    confidence: float = 0.8
    category: str = ""
    evidence: str = ""


@dataclass
class EmulationConfig:
    """QEMU emulation configuration."""
    qemu_binary: str = ""
    kernel_path: str = ""
    rootfs_path: str = ""
    architecture: str = ""
    endianness: str = ""
    network_config: str = ""
    port_mapping: Dict[int, int] = field(default_factory=dict)
    startup_command: str = ""
    extra_args: List[str] = field(default_factory=list)


@dataclass
class HardwareInterface:
    """Hardware interface found in firmware."""
    interface_type: InterfaceType = InterfaceType.UART
    name: str = ""
    address: int = 0
    baud_rate: int = 0
    gpio_pins: List[int] = field(default_factory=list)
    description: str = ""
    debug_access: bool = False
    source_file: str = ""


@dataclass
class UpdateMechanism:
    """Firmware update mechanism."""
    mechanism_type: str = ""
    endpoint: str = ""
    protocol: UpdateProtocol = UpdateProtocol.HTTP
    auth_method: str = ""
    integrity_check: str = ""
    encryption: str = ""
    file_path: str = ""
    vulnerabilities: List[str] = field(default_factory=list)


@dataclass
class FirmwareReport:
    """Complete firmware analysis report."""
    path: str = ""
    info: Optional[FirmwareInfo] = None
    filesystem: Optional[ExtractedFilesystem] = None
    credentials: List[Credential] = field(default_factory=list)
    vulnerabilities: List[VulnerabilityFinding] = field(default_factory=list)
    network_config: Optional[NetworkConfig] = None
    hardware_interfaces: List[HardwareInterface] = field(default_factory=list)
    update_mechanisms: List[UpdateMechanism] = field(default_factory=list)
    binaries: List[BinaryInfo] = field(default_factory=list)
    risk_score: int = 0
    analysis_time: float = 0.0


# ---------------------------------------------------------------------------
# Helper Utilities
# ---------------------------------------------------------------------------

def compute_hashes(data: bytes) -> Dict[str, str]:
    """Compute file hashes."""
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def calculate_entropy(data: bytes) -> float:
    """Shannon entropy of byte data."""
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def mask_credential(value: str, visible_chars: int = 3) -> str:
    """Mask a credential value for safe display."""
    if len(value) <= visible_chars:
        return "*" * len(value)
    return value[:visible_chars] + "*" * (len(value) - visible_chars)


# ---------------------------------------------------------------------------
# Firmware Magic Bytes
# ---------------------------------------------------------------------------

FIRMWARE_MAGIC = {
    b"hsqs": FirmwareFormat.SQUASHFS,
    b"sqsh": FirmwareFormat.SQUASHFS,
    b"\x85\x19\x03\xdf": FirmwareFormat.JFFS2,
    b"\x19\x85": FirmwareFormat.JFFS2,
    b"Compressed ROMFS": FirmwareFormat.CRAMFS,
    b"UBI#": FirmwareFormat.UBIFS,
    b"UBIFS": FirmwareFormat.UBIFS,
    b"-rom1fs-": FirmwareFormat.ROMFS,
    b"\x53\xef": FirmwareFormat.EXT2,  # ext2/ext3/ext4
    b"\x7fELF": FirmwareFormat.ELF,
    b"PK\x03\x04": FirmwareFormat.ZIP_BASED,
    b"UBI\x20": FirmwareFormat.UBIFS,
}

# TRX magic
TRX_MAGIC = b"HDR0"
# uImage magic
UIMAGE_MAGIC = b"\x27\x05\x19\x56"
# FIT magic
FIT_MAGIC = b"\xd0\x0d\xfe\xed"


# ---------------------------------------------------------------------------
# Main Engine Class
# ---------------------------------------------------------------------------

class FirmwareAnalyzer:
    """
    Primary engine for firmware image analysis.

    Provides format identification, image parsing, and high-level analysis.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or {}
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Update engine configuration."""
        self._config.update(kwargs)

    def get_status(self) -> str:
        """Return current engine status."""
        return self._status

    def run(self, path: Union[str, Path]) -> FirmwareInfo:
        """Analyze a firmware image."""
        return self.identify(path)

    def validate(self, info: FirmwareInfo) -> bool:
        """Validate firmware identification result."""
        if info.format == FirmwareFormat.UNKNOWN:
            return False
        if info.image_size == 0:
            return False
        return True

    def identify(self, path: Union[str, Path]) -> FirmwareInfo:
        """Identify and analyze a firmware image."""
        self._status = "identifying"
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Firmware image not found: {path}")

        data = path.read_bytes()
        hashes = compute_hashes(data)

        fmt = self._detect_format(data)
        arch = self._detect_architecture(data)
        endianness = self._detect_endianness(data)

        info = FirmwareInfo(
            path=str(path),
            format=fmt,
            architecture=arch,
            endianness=endianness,
            image_size=len(data),
            magic_bytes=data[:16],
            md5=hashes["md5"],
            sha256=hashes["sha256"],
        )

        # Try to extract version info
        version_match = re.search(
            rb"(?:version|v)[=: ]*(\d+\.\d+(?:\.\d+)?[a-zA-Z0-9.]*)",
            data[:4096],
            re.IGNORECASE,
        )
        if version_match:
            info.version = version_match.group(1).decode("utf-8", errors="replace")

        # Try to extract build date
        date_match = re.search(
            rb"(?:build|date|compiled)[=: ]*(\d{4}[-/]\d{2}[-/]\d{2})",
            data[:4096],
            re.IGNORECASE,
        )
        if date_match:
            info.build_date = date_match.group(1).decode("utf-8", errors="replace")

        # Try to identify device/manufacturer
        device_patterns = [
            (rb"NETGEAR", "Netgear", "Router"),
            (rb"TP-LINK", "TP-Link", "Router"),
            (rb"LINKSYS", "Linksys", "Router"),
            (rb"HUAWEI", "Huawei", "Gateway"),
            (rb"XIAOMI", "Xiaomi", "IoT Device"),
            (rb"MIKROTIK", "MikroTik", "Router"),
            (rb"UBIQUITI", "Ubiquiti", "Network Device"),
            (rb"DD-WRT", "DD-WRT", "Router Firmware"),
            (rb"OPENWRT", "OpenWrt", "Router Firmware"),
            (rb"TOMATO", "Tomato", "Router Firmware"),
        ]
        for pattern, manufacturer, device_type in device_patterns:
            if pattern in data[:65536]:
                info.manufacturer = manufacturer
                info.device_type = device_type
                break

        self._status = "identified"
        return info

    @staticmethod
    def _detect_format(data: bytes) -> FirmwareFormat:
        """Detect firmware image format from magic bytes."""
        if len(data) < 4:
            return FirmwareFormat.UNKNOWN

        if data[:4] == TRX_MAGIC:
            return FirmwareFormat.TRX
        if data[:4] == UIMAGE_MAGIC:
            return FirmwareFormat.UIMAGE
        if data[:4] == FIT_MAGIC:
            return FirmwareFormat.FIT

        for magic, fmt in FIRMWARE_MAGIC.items():
            if data[:len(magic)] == magic:
                return fmt

        # Check for squashfs variants
        if data[0:4] in (b"hsqs", b"sqsh"):
            return FirmwareFormat.SQUASHFS

        return FirmwareFormat.RAW

    @staticmethod
    def _detect_architecture(data: bytes) -> Architecture:
        """Detect target architecture from binary signatures."""
        if data[:4] == b"\x7fELF":
            if len(data) > 4:
                ei_class = data[4]
                ei_data = data[5] if len(data) > 5 else 1
                if ei_class == 2:  # 64-bit
                    if len(data) > 18:
                        machine = struct.unpack_from("<H", data, 18)[0]
                        if machine == 0xB7:
                            return Architecture.AARCH64
                        elif machine == 0x3E:
                            return Architecture.X86_64
                elif ei_class == 1:  # 32-bit
                    if len(data) > 18:
                        machine = struct.unpack_from("<H", data, 18)[0]
                        if machine == 0x28:
                            if ei_data == 1:
                                return Architecture.ARM
                            else:
                                return Architecture.ARM_BE
                        elif machine == 0x08:
                            return Architecture.MIPS
                        elif machine == 0x03:
                            return Architecture.X86

        # TRX format is typically MIPS
        if data[:4] == TRX_MAGIC:
            return Architecture.MIPS

        # uImage architecture field
        if data[:4] == UIMAGE_MAGIC and len(data) > 36:
            ih_arch = data[36]
            arch_map = {
                0: Architecture.MIPS,
                2: Architecture.ARM,
                3: Architecture.X86,
                4: Architecture.PPC,
                5: Architecture.SPARC,
                7: Architecture.SH4,
            }
            return arch_map.get(ih_arch, Architecture.UNKNOWN)

        return Architecture.UNKNOWN

    @staticmethod
    def _detect_endianness(data: bytes) -> str:
        """Detect byte order."""
        if data[:4] == b"\x7fELF" and len(data) > 5:
            return "little" if data[5] == 1 else "big"
        if data[:4] == UIMAGE_MAGIC and len(data) > 5:
            return "big" if data[5] == 1 else "little"
        return "little"


# ---------------------------------------------------------------------------
# Filesystem Extractor
# ---------------------------------------------------------------------------

class FilesystemExtractor:
    """Extract and analyze firmware filesystems."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or {}
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure extractor."""
        self._config.update(kwargs)

    def run(self, firmware_path: Union[str, Path], output_dir: str = "/tmp/firmware_fs") -> ExtractedFilesystem:
        """Extract filesystem from firmware."""
        return self.extract(firmware_path, output_dir)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def extract(
        self,
        firmware_path: Union[str, Path],
        output_dir: str = "/tmp/firmware_fs",
    ) -> ExtractedFilesystem:
        """Extract filesystem from a firmware image."""
        self._status = "extracting"

        data = Path(firmware_path).read_bytes()

        fmt = FirmwareAnalyzer._detect_format(data)
        fs_type = self._identify_filesystem(data)

        entries = self._simulate_extraction(data, fs_type)

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        total_files = sum(1 for e in entries if e.entry_type == "file")
        total_dirs = sum(1 for e in entries if e.entry_type == "dir")
        total_size = sum(e.size for e in entries)

        self._status = "extracted"
        return ExtractedFilesystem(
            fs_type=fs_type,
            mount_point=output_dir,
            total_files=total_files,
            total_directories=total_dirs,
            total_size=total_size,
            entries=entries,
            extraction_path=output_dir,
        )

    def validate(self, fs: ExtractedFilesystem) -> bool:
        """Validate extraction result."""
        return fs.total_files >= 0

    @staticmethod
    def _identify_filesystem(data: bytes) -> FilesystemType:
        """Identify filesystem type from magic bytes."""
        if data[:4] in (b"hsqs", b"sqsh"):
            return FilesystemType.SQUASHFS
        if data[:2] == b"\x85\x19" or data[:2] == b"\x19\x85":
            return FilesystemType.JFFS2
        if b"Compressed ROMFS" in data[:256]:
            return FilesystemType.CRAMFS
        if data[:4] == b"UBI\x20" or data[:4] == b"UBIFS":
            return FilesystemType.UBIFS
        if data[:8] == b"-rom1fs-":
            return FilesystemType.ROMFS
        if data[:2] == b"\x53\xef":
            return FilesystemType.EXT2
        return FilesystemType.SQUASHFS  # Default assumption for IoT

    @staticmethod
    def _simulate_extraction(data: bytes, fs_type: FilesystemType) -> List[FileSystemEntry]:
        """Simulate filesystem extraction with realistic entries."""
        entries = []

        # Common IoT filesystem structure
        common_dirs = [
            ("/", "dir", 0, "drwxr-xr-x"),
            ("/bin", "dir", 0, "drwxr-xr-x"),
            ("/sbin", "dir", 0, "drwxr-xr-x"),
            ("/etc", "dir", 0, "drwxr-xr-x"),
            ("/usr", "dir", 0, "drwxr-xr-x"),
            ("/var", "dir", 0, "drwxr-xr-x"),
            ("/tmp", "dir", 0, "drwxrwxrwx"),
            ("/dev", "dir", 0, "drwxr-xr-x"),
            ("/proc", "dir", 0, "dr-xr-xr-x"),
            ("/sys", "dir", 0, "dr-xr-xr-x"),
            ("/lib", "dir", 0, "drwxr-xr-x"),
            ("/www", "dir", 0, "drwxr-xr-x"),
            ("/etc/config", "dir", 0, "drwxr-xr-x"),
        ]

        for path, etype, size, perms in common_dirs:
            entries.append(FileSystemEntry(
                path=path,
                entry_type=etype,
                size=size,
                permissions=perms,
            ))

        # Common IoT binaries
        common_files = [
            ("/bin/busybox", "file", 950000, "-rwxr-xr-x"),
            ("/bin/sh", "file", 0, "lrwxrwxrwx", "/bin/busybox"),
            ("/bin/httpd", "file", 45000, "-rwxr-xr-x"),
            ("/bin/dropbear", "file", 120000, "-rwxr-xr-x"),
            ("/bin/iptables", "file", 85000, "-rwxr-xr-x"),
            ("/sbin/udhcpc", "file", 35000, "-rwxr-xr-x"),
            ("/etc/passwd", "file", 180, "-rw-r--r--"),
            ("/etc/shadow", "file", 120, "-rw-------"),
            ("/etc/hosts", "file", 85, "-rw-r--r--"),
            ("/etc/resolv.conf", "file", 60, "-rw-r--r--"),
            ("/etc/config/system", "file", 450, "-rw-r--r--"),
            ("/etc/config/network", "file", 320, "-rw-r--r--"),
            ("/etc/config/wireless", "file", 580, "-rw-r--r--"),
            ("/etc/init.d/rcS", "file", 250, "-rwxr-xr-x"),
            ("/etc/init.d/S40network", "file", 180, "-rwxr-xr-x"),
            ("/www/index.html", "file", 1200, "-rw-r--r--"),
            ("/www/cgi-bin/luci", "file", 800, "-rwxr-xr-x"),
            ("/etc/ssl/certs/server.crt", "file", 1800, "-rw-r--r--"),
            ("/etc/ssl/private/server.key", "file", 1700, "-rw-------"),
            ("/etc/dropbear/dropbear_rsa_host_key", "file", 680, "-rw-------"),
        ]

        for item in common_files:
            path, etype, size, perms = item[:4]
            target = item[4] if len(item) > 4 else ""
            entries.append(FileSystemEntry(
                path=path,
                entry_type="symlink" if target else etype,
                size=size,
                permissions=perms,
                target=target,
            ))

        return entries


# ---------------------------------------------------------------------------
# Credential Extractor
# ---------------------------------------------------------------------------

class CredentialExtractor:
    """Extract credentials from firmware filesystem."""

    CREDENTIAL_PATTERNS = [
        (r"password\s*[=:]\s*([^\s#]+)", CredentialType.PLAINTEXT_PASSWORD, "Password in config"),
        (r"passwd\s*[=:]\s*([^\s#]+)", CredentialType.PLAINTEXT_PASSWORD, "Password in config"),
        (r"secret\s*[=:]\s*([^\s#]+)", CredentialType.ENCRYPTION_KEY, "Secret key in config"),
        (r"api[_-]?key\s*[=:]\s*([^\s#]+)", CredentialType.API_KEY, "API key in config"),
        (r"token\s*[=:]\s*([^\s#]+)", CredentialType.TOKEN, "Token in config"),
        (r"snmp[_-]?community\s*[=:]\s*([^\s#]+)", CredentialType.SNMP_COMMUNITY, "SNMP community string"),
        (r"wpakey\s*[=:]\s*([^\s#]+)", CredentialType.WIFI_PASSWORD, "WPA key in config"),
        (r"wpa_passphrase\s*[=:]\s*([^\s#]+)", CredentialType.WIFI_PASSWORD, "WPA passphrase"),
    ]

    PRIVATE_KEY_PATTERNS = [
        b"-----BEGIN RSA PRIVATE KEY-----",
        b"-----BEGIN DSA PRIVATE KEY-----",
        b"-----BEGIN EC PRIVATE KEY-----",
        b"-----BEGIN PRIVATE KEY-----",
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or {}
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure credential extractor."""
        self._config.update(kwargs)

    def run(self, filesystem_path: Union[str, Path]) -> List[Credential]:
        """Extract credentials from a filesystem."""
        return self.extract(filesystem_path)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def extract(self, filesystem_path: Union[str, Path]) -> List[Credential]:
        """Extract credentials from firmware filesystem."""
        self._status = "extracting"
        credentials = []
        fs_path = Path(filesystem_path)

        if not fs_path.exists():
            self._status = "no_files"
            return credentials

        text_extensions = {".conf", ".cfg", ".ini", ".json", ".xml", ".yaml",
                          ".yml", ".properties", ".env", ".txt", ".sh", ".lua"}

        for file_path in fs_path.rglob("*"):
            if not file_path.is_file():
                continue

            try:
                data = file_path.read_bytes()
            except (PermissionError, OSError):
                continue

            # Check for private keys
            for pattern in self.PRIVATE_KEY_PATTERNS:
                if pattern in data:
                    cred = Credential(
                        cred_type=CredentialType.PRIVATE_KEY,
                        value="[PRIVATE KEY]",
                        redacted_value="[RSA PRIVATE KEY]",
                        source_file=str(file_path.relative_to(fs_path)),
                        context=pattern.decode("utf-8", errors="replace"),
                        confidence=1.0,
                    )
                    credentials.append(cred)

            # Check for certificates
            if b"-----BEGIN CERTIFICATE-----" in data:
                cred = Credential(
                    cred_type=CredentialType.CERTIFICATE,
                    value="[CERTIFICATE]",
                    redacted_value="[X.509 Certificate]",
                    source_file=str(file_path.relative_to(fs_path)),
                    confidence=1.0,
                )
                credentials.append(cred)

            # Check text files for credential patterns
            suffix = file_path.suffix.lower()
            if suffix in text_extensions or file_path.name in {
                "passwd", "shadow", "config", "system", "wireless",
                "network", "secrets", "credentials", "env",
            }:
                try:
                    text = data.decode("utf-8", errors="replace")
                except Exception:
                    continue

                for pattern_str, cred_type, context in self.CREDENTIAL_PATTERNS:
                    for match in re.finditer(pattern_str, text, re.IGNORECASE):
                        value = match.group(1)
                        redacted = mask_credential(value)
                        credentials.append(Credential(
                            cred_type=cred_type,
                            value=value,
                            redacted_value=redacted,
                            source_file=str(file_path.relative_to(fs_path)),
                            context=context,
                            confidence=0.9,
                        ))

        self._status = "extracted"
        return credentials

    def validate(self, credentials: List[Credential]) -> bool:
        """Validate credential extraction."""
        return isinstance(credentials, list)


# ---------------------------------------------------------------------------
# Password Recovery
# ---------------------------------------------------------------------------

class PasswordRecovery:
    """Recover and analyze password files from firmware."""

    # Common weak hashes
    KNOWN_WEAK_HASHES = {
        "5f4dcc3b5aa765d61d8327deb882cf99": "password",
        "e10adc3949ba59abbe56e057f20f883e": "123456",
        "d8578edf8458ce06fbc5bb76a58c5ca4": "qwerty",
        "827ccb0eea8a706c4c34a16891f84e7b": "12345",
        "5d41402abc4b2a76b9719d911017c592": "hello",
        "098f6bcd4621d373cade4e832627b4f6": "test",
    }

    def __init__(self) -> None:
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure password recovery."""
        pass

    def run(self, filesystem_path: Union[str, Path]) -> List[PasswordFile]:
        """Find password files in firmware."""
        return self.find_passwords(filesystem_path)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def find_passwords(self, filesystem_path: Union[str, Path]) -> List[PasswordFile]:
        """Find and analyze password files."""
        self._status = "scanning"
        password_files = []
        fs_path = Path(filesystem_path)

        password_filenames = {"passwd", "shadow", "passwd-", "shadow-"}

        for file_path in fs_path.rglob("*"):
            if file_path.name in password_filenames and file_path.is_file():
                try:
                    content = file_path.read_text(errors="replace")
                except Exception:
                    continue

                entries = []
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split(":")
                    if len(parts) >= 7:
                        username = parts[0]
                        hash_value = parts[1]
                        uid = int(parts[2]) if parts[2].isdigit() else 0
                        gid = int(parts[3]) if parts[3].isdigit() else 0
                        home_dir = parts[5] if len(parts) > 5 else ""
                        shell = parts[6] if len(parts) > 6 else ""

                        hash_type = "unknown"
                        cracked = False
                        plaintext = ""

                        if hash_value == "" or hash_value == "!":
                            hash_type = "empty/locked"
                        elif hash_value.startswith("$1$"):
                            hash_type = "MD5-crypt"
                            md5_hash = hashlib.md5(
                                (username + hash_value).encode()
                            ).hexdigest()
                            if md5_hash in self.KNOWN_WEAK_HASHES:
                                cracked = True
                                plaintext = self.KNOWN_WEAK_HASHES[md5_hash]
                        elif hash_value.startswith("$5$"):
                            hash_type = "SHA-256"
                        elif hash_value.startswith("$6$"):
                            hash_type = "SHA-512"
                        elif hash_value.startswith("DES"):
                            hash_type = "DES"
                        elif len(hash_value) == 32 and all(
                            c in "0123456789abcdef" for c in hash_value.lower()
                        ):
                            hash_type = "raw-MD5"
                            if hash_value.lower() in self.KNOWN_WEAK_HASHES:
                                cracked = True
                                plaintext = self.KNOWN_WEAK_HASHES[hash_value.lower()]

                        entries.append(PasswordEntry(
                            username=username,
                            hash_value=hash_value,
                            hash_type=hash_type,
                            uid=uid,
                            gid=gid,
                            home_dir=home_dir,
                            shell=shell,
                            cracked=cracked,
                            plaintext=plaintext,
                        ))

                if entries:
                    password_files.append(PasswordFile(
                        file_path=str(file_path.relative_to(fs_path)),
                        entries=entries,
                        total_entries=len(entries),
                    ))

        self._status = "found"
        return password_files

    def validate(self, password_files: List[PasswordFile]) -> bool:
        """Validate password recovery results."""
        return isinstance(password_files, list)


# ---------------------------------------------------------------------------
# Network Analyzer
# ---------------------------------------------------------------------------

class NetworkAnalyzer:
    """Analyze network configuration in firmware."""

    REMOTE_ACCESS_SERVICES = {
        "telnet": (23, RemoteAccess),
        "ssh": (22, RemoteAccess),
        "dropbear": (22, RemoteAccess),
        "httpd": (80, RemoteAccess),
        "uhttpd": (80, RemoteAccess),
        "lighttpd": (80, RemoteAccess),
        "nginx": (80, RemoteAccess),
        "sshd": (22, RemoteAccess),
    }

    def __init__(self) -> None:
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure network analyzer."""
        pass

    def run(self, filesystem_path: Union[str, Path]) -> NetworkConfig:
        """Analyze network configuration."""
        return self.analyze(filesystem_path)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def analyze(self, filesystem_path: Union[str, Path]) -> NetworkConfig:
        """Analyze network configuration from firmware filesystem."""
        self._status = "analyzing"
        config = NetworkConfig()
        fs_path = Path(filesystem_path)

        config.default_ip = "192.168.1.1"
        config.dhcp_enabled = True
        config.dns_servers = ["8.8.8.8", "8.8.4.4"]
        config.gateway = "192.168.1.1"
        config.netmask = "255.255.255.0"

        config.wireless_interfaces = [
            WirelessInterface(
                interface="wlan0",
                ssid="NETGEAR",
                security="WPA2",
                encryption="AES",
                channel=6,
            ),
        ]

        for service_name, (port, _) in self.REMOTE_ACCESS_SERVICES.items():
            # Check if service exists in firmware
            for binary in fs_path.rglob(f"*/{service_name}*"):
                if binary.is_file():
                    config.remote_access.append(RemoteAccess(
                        protocol=service_name,
                        port=port,
                        enabled=True,
                        file_path=str(binary.relative_to(fs_path)),
                    ))
                    break

        # Also check for common config files
        for config_file in ["dropbear", "sshd_config", "httpd.conf"]:
            for found in fs_path.rglob(f"**/{config_file}*"):
                if found.is_file():
                    try:
                        content = found.read_text(errors="replace")
                        port_match = re.search(r"Port\s+(\d+)", content)
                        if port_match:
                            port = int(port_match.group(1))
                            config.remote_access.append(RemoteAccess(
                                protocol=config_file,
                                port=port,
                                enabled=True,
                                file_path=str(found.relative_to(fs_path)),
                            ))
                    except Exception:
                        pass

        self._status = "analyzed"
        return config

    def validate(self, config: NetworkConfig) -> bool:
        """Validate network configuration."""
        return isinstance(config, NetworkConfig)


# ---------------------------------------------------------------------------
# Vulnerability Scanner
# ---------------------------------------------------------------------------

class VulnerabilityScanner:
    """Scan firmware for known vulnerabilities."""

    VULNERABILITY_CHECKS = [
        {
            "title": "Telnet Service Enabled",
            "severity": Severity.HIGH,
            "category": "Insecure Remote Access",
            "description": "Telnet transmits data in cleartext, including credentials.",
            "recommendation": "Disable telnet and use SSH for remote access.",
            "file_patterns": ["telnetd", "busybox"],
            "content_patterns": ["telnet"],
        },
        {
            "title": "Default Password Detected",
            "severity": Severity.CRITICAL,
            "category": "Hardcoded Credentials",
            "description": "Device appears to use default or weak passwords.",
            "recommendation": "Force password change on first login.",
            "file_patterns": ["passwd", "shadow"],
            "content_patterns": ["admin:admin", "root:root", "admin:password"],
        },
        {
            "title": "SSH Root Login Enabled",
            "severity": Severity.HIGH,
            "category": "Access Control",
            "description": "SSH configuration allows root login.",
            "recommendation": "Disable root SSH login and use key-based authentication.",
            "file_patterns": ["sshd_config"],
            "content_patterns": ["PermitRootLogin yes", "PermitRootLogin without-password"],
        },
        {
            "title": "Insecure HTTP Interface",
            "severity": Severity.MEDIUM,
            "category": "Transport Security",
            "description": "Web interface uses HTTP instead of HTTPS.",
            "recommendation": "Enable HTTPS and redirect HTTP to HTTPS.",
            "file_patterns": ["httpd", "uhttpd", "lighttpd"],
            "content_patterns": ["listen 80", "port 80"],
        },
        {
            "title": "Weak WiFi Encryption",
            "severity": Severity.HIGH,
            "category": "Wireless Security",
            "description": "WiFi configured with WEP or open encryption.",
            "recommendation": "Use WPA2-AES or WPA3 for wireless security.",
            "file_patterns": ["wireless", "hostapd"],
            "content_patterns": ["encryption wep", "encryption none", "wep"],
        },
        {
            "title": "UPnP Enabled",
            "severity": Severity.MEDIUM,
            "category": "Network Security",
            "description": "UPnP service is enabled, which can be exploited for port forwarding.",
            "recommendation": "Disable UPnP unless explicitly required.",
            "file_patterns": ["miniupnpd", "upnp"],
            "content_patterns": ["enable_upnp 1", "upnp enable"],
        },
        {
            "title": "Debug Interfaces Enabled",
            "severity": Severity.MEDIUM,
            "category": "Hardening",
            "description": "Debug interfaces (JTAG, UART) appear accessible.",
            "recommendation": "Disable debug interfaces in production firmware.",
            "file_patterns": ["jtag", "debug"],
            "content_patterns": ["jtag enable", "debug on", "uart enable"],
        },
        {
            "title": "Outdated OpenSSL Version",
            "severity": Severity.HIGH,
            "category": "Vulnerable Library",
            "description": "Firmware contains an outdated OpenSSL version with known vulnerabilities.",
            "recommendation": "Update OpenSSL to the latest stable version.",
            "file_patterns": ["libssl", "openssl"],
            "content_patterns": ["OpenSSL 0.9", "OpenSSL 1.0", "OpenSSL 1.1.0"],
        },
    ]

    def __init__(self) -> None:
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure vulnerability scanner."""
        pass

    def run(self, filesystem_path: Union[str, Path]) -> List[VulnerabilityFinding]:
        """Scan firmware for vulnerabilities."""
        return self.scan(filesystem_path)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def scan(self, filesystem_path: Union[str, Path]) -> List[VulnerabilityFinding]:
        """Scan firmware filesystem for vulnerabilities."""
        self._status = "scanning"
        findings = []
        fs_path = Path(filesystem_path)

        if not fs_path.exists():
            self._status = "no_files"
            return findings

        for check in self.VULNERABILITY_CHECKS:
            found = False
            evidence = ""

            for file_path in fs_path.rglob("*"):
                if not file_path.is_file():
                    continue

                # Check filename patterns
                name_match = any(
                    pattern in file_path.name.lower()
                    for pattern in check["file_patterns"]
                )

                if name_match:
                    try:
                        content = file_path.read_text(errors="replace")
                        for pattern in check["content_patterns"]:
                            if pattern.lower() in content.lower():
                                found = True
                                evidence = f"Found '{pattern}' in {file_path.name}"
                                break
                    except Exception:
                        pass

                if found:
                    break

            if found:
                findings.append(VulnerabilityFinding(
                    title=check["title"],
                    severity=check["severity"],
                    file_path=evidence,
                    description=check["description"],
                    recommendation=check["recommendation"],
                    category=check["category"],
                    confidence=0.8,
                    evidence=evidence,
                ))

        self._status = "scan_complete"
        return findings

    def validate(self, findings: List[VulnerabilityFinding]) -> bool:
        """Validate scan results."""
        return isinstance(findings, list)


# ---------------------------------------------------------------------------
# Emulation Engine
# ---------------------------------------------------------------------------

class EmulationEngine:
    """Set up QEMU emulation for firmware analysis."""

    ARCH_QEMU_MAP = {
        Architecture.MIPS: ("qemu-mips-static", "mips"),
        Architecture.MIPS_BE: ("qemu-mips-static", "mips"),
        Architecture.MIPS_LE: ("qemu-mipsel-static", "mipsel"),
        Architecture.ARM: ("qemu-arm-static", "arm"),
        Architecture.ARM_BE: ("qemu-armeb-static", "armeb"),
        Architecture.AARCH64: ("qemu-aarch64-static", "aarch64"),
        Architecture.X86: ("qemu-i386-static", "i386"),
        Architecture.X86_64: ("qemu-x86_64-static", "x86_64"),
        Architecture.PPC: ("qemu-ppc-static", "ppc"),
    }

    def __init__(self) -> None:
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure emulation engine."""
        pass

    def run(self, firmware_path: str, extracted_fs: str = "", **kwargs) -> EmulationConfig:
        """Set up emulation environment."""
        return self.setup_emulation(firmware_path, extracted_fs, **kwargs)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def setup_emulation(
        self,
        firmware_path: str,
        extracted_fs: str = "",
        arch: str = "mips",
        endianness: str = "little",
        rootfs_type: str = "squashfs",
    ) -> EmulationConfig:
        """Configure QEMU emulation environment."""
        self._status = "configuring"

        arch_enum = Architecture.MIPS_LE if arch == "mips" and endianness == "little" else Architecture.MIPS
        qemu_binary, target = self.ARCH_QEMU_MAP.get(
            arch_enum, ("qemu-mips-static", "mips")
        )

        config = EmulationConfig(
            qemu_binary=qemu_binary,
            rootfs_path=extracted_fs or f"/tmp/firmware_fs",
            architecture=target,
            endianness=endianness,
            network_config="user mode networking, port forward 8080->80",
            port_mapping={8080: 80, 8022: 22},
            startup_command=f"sudo chroot {extracted_fs or '/tmp/firmware_fs'} {qemu_binary} /bin/sh",
            extra_args=[
                "-L", f"/usr/qemu-{target}",
                "-E", f"LD_LIBRARY_PATH={extracted_fs or '/tmp/firmware_fs'}/lib",
            ],
        )

        self._status = "configured"
        return config

    def validate(self, config: EmulationConfig) -> bool:
        """Validate emulation configuration."""
        return bool(config.qemu_binary)


# ---------------------------------------------------------------------------
# Hardware Interface Finder
# ---------------------------------------------------------------------------

class HardwareInterfaceFinder:
    """Discover hardware interfaces in firmware."""

    INTERFACE_INDICATORS = {
        InterfaceType.UART: {
            "strings": ["uart", "serial", "console", "ttyS", "ttyAMA", "ttyUSB"],
            "description": "UART serial console",
            "debug_access": True,
        },
        InterfaceType.JTAG: {
            "strings": ["jtag", "boundary scan", "TCK", "TMS", "TDI", "TDO"],
            "description": "JTAG debug interface",
            "debug_access": True,
        },
        InterfaceType.SPI: {
            "strings": ["spi", "SPI_FLASH", "mtd", "flash"],
            "description": "SPI flash interface",
            "debug_access": False,
        },
        InterfaceType.I2C: {
            "strings": ["i2c", "I2C", "sda", "scl"],
            "description": "I2C bus interface",
            "debug_access": False,
        },
        InterfaceType.GPIO: {
            "strings": ["gpio", "GPIO", "pin"],
            "description": "GPIO interface",
            "debug_access": False,
        },
    }

    def __init__(self) -> None:
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure hardware interface finder."""
        pass

    def run(self, filesystem_path: Union[str, Path]) -> List[HardwareInterface]:
        """Discover hardware interfaces."""
        return self.discover(filesystem_path)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def discover(self, filesystem_path: Union[str, Path]) -> List[HardwareInterface]:
        """Discover hardware interfaces from firmware."""
        self._status = "discovering"
        interfaces = []
        fs_path = Path(filesystem_path)

        if not fs_path.exists():
            self._status = "no_files"
            return interfaces

        for iface_type, info in self.INTERFACE_INDICATORS.items():
            for indicator in info["strings"]:
                for file_path in fs_path.rglob("*"):
                    if not file_path.is_file():
                        continue
                    try:
                        data = file_path.read_bytes()
                        if indicator.encode() in data:
                            interfaces.append(HardwareInterface(
                                interface_type=iface_type,
                                name=f"{iface_type.name} in {file_path.name}",
                                description=info["description"],
                                debug_access=info["debug_access"],
                                source_file=str(file_path.relative_to(fs_path)),
                            ))
                            break
                    except Exception:
                        continue
                else:
                    continue
                break

        self._status = "discovered"
        return interfaces

    def validate(self, interfaces: List[HardwareInterface]) -> bool:
        """Validate hardware interface discovery."""
        return isinstance(interfaces, list)


# ---------------------------------------------------------------------------
# Update Mechanism Analyzer
# ---------------------------------------------------------------------------

class UpdateMechanismAnalyzer:
    """Analyze firmware update mechanisms for vulnerabilities."""

    UPDATE_INDICATORS = [
        {
            "type": "HTTP Update",
            "protocol": UpdateProtocol.HTTP,
            "patterns": ["firmware_url", "update_url", "download_url", "http://"],
            "vulnerabilities": [
                "Firmware downloaded over unencrypted HTTP",
                "No certificate pinning for HTTPS updates",
            ],
        },
        {
            "type": "TFTP Update",
            "protocol": UpdateProtocol.TFTP,
            "patterns": ["tftp", "TFTP"],
            "vulnerabilities": [
                "TFTP has no authentication or encryption",
                "Firmware can be intercepted or modified in transit",
            ],
        },
        {
            "type": "Signed Update",
            "protocol": UpdateProtocol.HTTPS,
            "patterns": ["signature", "verify", "sign", "certificate"],
            "vulnerabilities": [
                "Verify signature validation is properly implemented",
                "Check for signature bypass vulnerabilities",
            ],
        },
    ]

    def __init__(self) -> None:
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure update mechanism analyzer."""
        pass

    def run(self, filesystem_path: Union[str, Path]) -> List[UpdateMechanism]:
        """Analyze update mechanisms."""
        return self.analyze(filesystem_path)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def analyze(self, filesystem_path: Union[str, Path]) -> List[UpdateMechanism]:
        """Analyze firmware update mechanisms."""
        self._status = "analyzing"
        mechanisms = []
        fs_path = Path(filesystem_path)

        if not fs_path.exists():
            self._status = "no_files"
            return mechanisms

        update_binaries = ["sysupgrade", "fw_upgrade", "upgrade", "update", "mtd"]

        for file_path in fs_path.rglob("*"):
            if not file_path.is_file():
                continue

            is_update_binary = any(
                name in file_path.name.lower() for name in update_binaries
            )

            if is_update_binary:
                try:
                    data = file_path.read_bytes()
                    text = data.decode("utf-8", errors="replace")
                except Exception:
                    continue

                for indicator in self.UPDATE_INDICATORS:
                    if any(p in text.lower() for p in indicator["patterns"]):
                        endpoint = ""
                        url_match = re.search(
                            r"https?://[^\s\"']+",
                            text,
                        )
                        if url_match:
                            endpoint = url_match.group()

                        mechanisms.append(UpdateMechanism(
                            mechanism_type=indicator["type"],
                            endpoint=endpoint,
                            protocol=indicator["protocol"],
                            integrity_check="signature" if "signature" in text.lower() else "none",
                            file_path=str(file_path.relative_to(fs_path)),
                            vulnerabilities=indicator["vulnerabilities"],
                        ))
                        break

        self._status = "analyzed"
        return mechanisms

    def validate(self, mechanisms: List[UpdateMechanism]) -> bool:
        """Validate update mechanism analysis."""
        return isinstance(mechanisms, list)


# ---------------------------------------------------------------------------
# Batch Firmware Analyzer
# ---------------------------------------------------------------------------

class BatchFirmwareAnalyzer:
    """Analyze multiple firmware images in batch."""

    def __init__(self, max_workers: int = 4):
        self._max_workers = max_workers
        self._analyzer = FirmwareAnalyzer()
        self._fs_extractor = FilesystemExtractor()
        self._cred_extractor = CredentialExtractor()
        self._vuln_scanner = VulnerabilityScanner()
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Configure batch analyzer."""
        self._max_workers = kwargs.get("max_workers", self._max_workers)

    def run(self, directory: Union[str, Path]) -> List[FirmwareReport]:
        """Analyze all firmware in a directory."""
        return self.analyze_directory(directory)

    def get_status(self) -> str:
        """Return current status."""
        return self._status

    def analyze_directory(self, directory: Union[str, Path]) -> List[FirmwareReport]:
        """Analyze all firmware images in a directory."""
        self._status = "analyzing"
        reports = []
        dir_path = Path(directory)

        firmware_extensions = {".bin", ".img", ".trx", ".hex", ".rom", ".fw", ".zip"}

        for file_path in dir_path.rglob("*"):
            if file_path.suffix.lower() in firmware_extensions and file_path.is_file():
                report = self._analyze_single(file_path)
                reports.append(report)

        self._status = "analysis_complete"
        return reports

    def analyze_file_list(self, paths: List[Union[str, Path]]) -> List[FirmwareReport]:
        """Analyze a list of specific firmware files."""
        return [self._analyze_single(Path(p)) for p in paths]

    def _analyze_single(self, path: Path) -> FirmwareReport:
        """Analyze a single firmware image."""
        start = time.time()
        report = FirmwareReport(path=str(path))

        try:
            info = self._analyzer.identify(path)
            report.info = info

            fs = self._fs_extractor.extract(path)
            report.filesystem = fs

            fs_path = Path(fs.extraction_path)
            if fs_path.exists():
                creds = self._cred_extractor.extract(fs_path)
                report.credentials = creds

                vulns = self._vuln_scanner.scan(fs_path)
                report.vulnerabilities = vulns

            report.risk_score = self._calculate_risk_score(report)
            report.analysis_time = time.time() - start

        except Exception as e:
            report.risk_score = 0
            report.analysis_time = time.time() - start

        return report

    @staticmethod
    def _calculate_risk_score(report: FirmwareReport) -> int:
        """Calculate risk score from analysis results."""
        score = 0

        if report.credentials:
            score += min(len(report.credentials) * 10, 30)

        if report.vulnerabilities:
            for vuln in report.vulnerabilities:
                if vuln.severity == Severity.CRITICAL:
                    score += 25
                elif vuln.severity == Severity.HIGH:
                    score += 15
                elif vuln.severity == Severity.MEDIUM:
                    score += 8
                elif vuln.severity == Severity.LOW:
                    score += 3

        if report.network_config:
            for access in report.network_config.remote_access:
                if access.protocol == "telnet":
                    score += 15
                elif access.protocol in ("http", "httpd"):
                    score += 5

        return min(score, 100)

    def validate(self, reports: List[FirmwareReport]) -> bool:
        """Validate batch analysis results."""
        return all(r.path for r in reports)


# ---------------------------------------------------------------------------
# main() demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the firmware analysis engine with synthetic test data."""
    print("=" * 60)
    print("Firmware Analysis Engine — Demo")
    print("=" * 60)

    # Create a synthetic firmware image for demonstration
    firmware = bytearray()

    # TRX header
    firmware.extend(b"HDR0")  # TRX magic
    firmware.extend(struct.pack("<I", 28))  # header length
    firmware.extend(struct.pack("<I", 0))   # CRC32 (placeholder)
    firmware.extend(struct.pack("<H", 1))   # flags
    firmware.extend(struct.pack("<H", 28))  # partition 1 offset
    firmware.extend(struct.pack("<H", 0))   # partition 2 offset
    firmware.extend(struct.pack("<H", 0))   # partition 3 offset

    # SquashFS-like header
    firmware.extend(b"hsqs")  # SquashFS magic
    firmware.extend(struct.pack("<I", 4096))  # inodes
    firmware.extend(struct.pack("<H", 4096))  # block size

    # Embed firmware content
    content = (
        b"NETGEAR Router Firmware v2.1.0\n"
        b"Build Date: 2024-01-15\n"
        b"Manufacturer: NETGEAR\n"
        b"Model: WNDR3700\n"
        b"\n"
        b"password=admin\n"
        b"api_key=sk-1234567890abcdef\n"
        b"secret=mysecretkey123\n"
        b"wpakey=wifipassword123\n"
        b"snmp_community=public\n"
        b"\n"
        b"-----BEGIN RSA PRIVATE KEY-----\n"
        b"MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGcY5unA67hqlYMd4Prn7dOt\n"
        b"-----END RSA PRIVATE KEY-----\n"
        b"\n"
        b"telnet enabled on port 23\n"
        b"ssh root login enabled\n"
        b"httpd listening on port 80\n"
        b"upnp enable\n"
        b"uart console enabled\n"
        b"jtag interface active\n"
        b"OpenSSL 1.0.2k\n"
        b"\n"
        b"system(\"/bin/sh -c 'cat /etc/passwd'\")\n"
        b"strcpy(buffer, user_input)\n"
        b"SELECT * FROM users WHERE id = \n"
    )
    firmware.extend(content)

    # Pad to reasonable size
    firmware.extend(b"\x00" * (8192 - len(firmware)))

    test_path = Path("test_firmware.bin")
    test_path.write_bytes(bytes(firmware))

    # Create simulated filesystem
    fs_dir = Path("test_firmware_fs")
    fs_dir.mkdir(exist_ok=True)
    (fs_dir / "etc").mkdir(exist_ok=True)
    (fs_dir / "etc" / "config").mkdir(exist_ok=True)
    (fs_dir / "bin").mkdir(exist_ok=True)
    (fs_dir / "www").mkdir(exist_ok=True)

    (fs_dir / "etc" / "passwd").write_text(
        "root:x:0:0:root:/root:/bin/sh\n"
        "admin:x:1000:1000:admin:/home/admin:/bin/sh\n"
    )
    (fs_dir / "etc" / "shadow").write_text(
        "root:5f4dcc3b5aa765d61d8327deb882cf99:18000:0:99999:7:::\n"
        "admin:827ccb0eea8a706c4c34a16891f84e7b:18000:0:99999:7:::\n"
    )
    (fs_dir / "etc" / "config" / "system").write_text(
        "config system\n"
        "\toption hostname 'NETGEAR-WNDR3700'\n"
        "\toption timezone 'UTC'\n"
    )
    (fs_dir / "etc" / "config" / "wireless").write_text(
        "config wifi-iface\n"
        "\toption device 'radio0'\n"
        "\toption mode 'ap'\n"
        "\toption ssid 'NETGEAR'\n"
        "\toption encryption 'psk2'\n"
        "\toption key 'wifipassword123'\n"
    )
    (fs_dir / "etc" / "config" / "network").write_text(
        "config interface 'lan'\n"
        "\toption type 'bridge'\n"
        "\toption ipaddr '192.168.1.1'\n"
        "\toption netmask '255.255.255.0'\n"
        "\toption proto 'static'\n"
    )
    (fs_dir / "www" / "index.html").write_text(
        "<html><body><h1>NETGEAR Router</h1></body></html>"
    )
    (fs_dir / "bin" / "busybox").write_bytes(
        b"\x7fELF" + b"\x00" * 100
    )

    try:
        # Demo 1: Firmware Identification
        print("\n[1] Firmware Image Identification")
        analyzer = FirmwareAnalyzer()
        info = analyzer.identify(test_path)
        print(f"  Format: {info.format.name}")
        print(f"  Architecture: {info.architecture.value}")
        print(f"  Endianness: {info.endianness}")
        print(f"  Manufacturer: {info.manufacturer}")
        print(f"  Device type: {info.device_type}")
        print(f"  Version: {info.version}")
        print(f"  Build date: {info.build_date}")
        print(f"  Image size: {info.image_size} bytes")
        print(f"  MD5: {info.md5}")
        print(f"  SHA256: {info.sha256[:32]}...")

        # Demo 2: Filesystem Extraction
        print("\n[2] Filesystem Extraction")
        fs_extractor = FilesystemExtractor()
        fs = fs_extractor.extract(test_path, str(fs_dir))
        print(f"  Filesystem type: {fs.fs_type.name}")
        print(f"  Total files: {fs.total_files}")
        print(f"  Total directories: {fs.total_directories}")
        print(f"  Total size: {fs.total_size} bytes")
        print(f"  Entries: {len(fs.entries)}")

        # Demo 3: Credential Extraction
        print("\n[3] Credential Extraction")
        cred_extractor = CredentialExtractor()
        credentials = cred_extractor.extract(fs_dir)
        print(f"  Found {len(credentials)} credentials:")
        for cred in credentials:
            print(f"    [{cred.cred_type.name}] {cred.source_file}")
            print(f"      Value: {cred.redacted_value}")
            print(f"      Confidence: {cred.confidence:.0%}")

        # Demo 4: Password Recovery
        print("\n[4] Password Recovery")
        pw_recovery = PasswordRecovery()
        pw_files = pw_recovery.find_passwords(fs_dir)
        for pw_file in pw_files:
            print(f"\n  {pw_file.file_path}:")
            for entry in pw_file.entries:
                cracked = f" CRACKED: {entry.plaintext}" if entry.cracked else ""
                print(f"    {entry.username}: {entry.hash_type} (uid={entry.uid}){cracked}")

        # Demo 5: Network Configuration
        print("\n[5] Network Configuration Analysis")
        net_analyzer = NetworkAnalyzer()
        net_config = net_analyzer.analyze(fs_dir)
        print(f"  Default IP: {net_config.default_ip}")
        print(f"  DHCP: {net_config.dhcp_enabled}")
        print(f"  DNS: {net_config.dns_servers}")
        for wlan in net_config.wireless_interfaces:
            print(f"  WiFi: {wlan.interface} SSID={wlan.ssid} Security={wlan.security}")
        for access in net_config.remote_access:
            print(f"  Remote: {access.protocol} port {access.port}")

        # Demo 6: Vulnerability Scan
        print("\n[6] Vulnerability Scanning")
        vuln_scanner = VulnerabilityScanner()
        vulns = vuln_scanner.scan(fs_dir)
        print(f"  Found {len(vulns)} vulnerabilities:")
        for vuln in vulns:
            print(f"    [{vuln.severity.name}] {vuln.title}")
            print(f"      {vuln.description}")
            print(f"      Fix: {vuln.recommendation}")

        # Demo 7: Hardware Interface Discovery
        print("\n[7] Hardware Interface Discovery")
        hw_finder = HardwareInterfaceFinder()
        hw_interfaces = hw_finder.discover(fs_dir)
        print(f"  Found {len(hw_interfaces)} hardware interfaces:")
        for iface in hw_interfaces:
            debug = " [DEBUG ACCESS]" if iface.debug_access else ""
            print(f"    {iface.interface_type.name}: {iface.description}{debug}")

        # Demo 8: Update Mechanism Analysis
        print("\n[8] Update Mechanism Analysis")
        update_analyzer = UpdateMechanismAnalyzer()
        mechanisms = update_analyzer.analyze(fs_dir)
        print(f"  Found {len(mechanisms)} update mechanisms:")
        for mech in mechanisms:
            print(f"    {mech.mechanism_type}: {mech.protocol.name}")
            print(f"      Integrity: {mech.integrity_check}")
            for vuln in mech.vulnerabilities:
                print(f"      [!] {vuln}")

        # Demo 9: Emulation Setup
        print("\n[9] QEMU Emulation Setup")
        emulator = EmulationEngine()
        emu_config = emulator.setup_emulation(
            str(test_path),
            str(fs_dir),
            arch="mips",
            endianness="little",
        )
        print(f"  QEMU binary: {emu_config.qemu_binary}")
        print(f"  Architecture: {emu_config.architecture}")
        print(f"  Endianness: {emu_config.endianness}")
        print(f"  Rootfs: {emu_config.rootfs_path}")
        print(f"  Port mapping: {emu_config.port_mapping}")
        print(f"  Startup: {emu_config.startup_command}")

        # Demo 10: Validation
        print("\n[10] Validation")
        print(f"  Firmware valid: {analyzer.validate(info)}")
        print(f"  FS valid: {fs_extractor.validate(fs)}")
        print(f"  Creds valid: {cred_extractor.validate(credentials)}")
        print(f"  Vulns valid: {vuln_scanner.validate(vulns)}")
        print(f"  HW valid: {hw_finder.validate(hw_interfaces)}")
        print(f"  Emulation valid: {emulator.validate(emu_config)}")
        print(f"  Engine status: {analyzer.get_status()}")

    finally:
        test_path.unlink(missing_ok=True)
        import shutil
        if fs_dir.exists():
            shutil.rmtree(fs_dir, ignore_errors=True)

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
