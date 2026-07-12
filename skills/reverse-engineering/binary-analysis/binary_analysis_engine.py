"""
Binary Analysis Engine — Python-native reverse engineering toolkit for ELF, PE, and Mach-O binaries.

Provides structured analysis of binary executables including format detection, header parsing,
section analysis, string extraction, entropy calculation, import/export mapping, and YARA matching.
Designed for security researchers, malware analysts, and CTF players who need reproducible,
scriptable binary analysis pipelines.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import struct
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BinaryFormat(Enum):
    """Detected binary file format."""
    ELF = auto()
    PE = auto()
    MACHO = auto()
    UNKNOWN = auto()


class Architecture(Enum):
    """Target CPU architecture."""
    X86 = "x86"
    X86_64 = "x86-64"
    ARM = "ARM"
    ARM64 = "ARM64"
    MIPS = "MIPS"
    PPC = "PowerPC"
    RISCV = "RISC-V"
    UNKNOWN = "unknown"


class SectionType(Enum):
    """Semantic classification of binary sections."""
    CODE = auto()
    DATA = auto()
    BSS = auto()
    RODATA = auto()
    SYMBOLS = auto()
    DEBUG = auto()
    OTHER = auto()


class StringEncoding(Enum):
    """Detected string encoding format."""
    ASCII = auto()
    UTF16_LE = auto()
    UTF16_BE = auto()
    UTF8 = auto()
    BASE64 = auto()
    HEX = auto()
    XOR_ENCODED = auto()
    UNKNOWN = auto()


class CapabilityFlag(Enum):
    """Behavioral capabilities inferred from imports."""
    NETWORK = auto()
    CRYPTO = auto()
    FILE_IO = auto()
    REGISTRY = auto()
    PROCESS_CREATE = auto()
    ANTI_DEBUG = auto()
    DLL_INJECTION = auto()
    PERSISTENCE = auto()
    PRIVILEGE_ESCALATION = auto()
    DATA_EXFIL = auto()


class PackerType(Enum):
    """Known binary packer/protector families."""
    UPX = auto()
    THEMIDA = auto()
    VMPROTECT = auto()
    ASPACK = auto()
    PECompact = auto()
    Custom = auto()
    None_ = auto()


class RiskLevel(Enum):
    """Triage risk assessment."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SectionInfo:
    """Parsed section header information."""
    name: str
    virtual_address: int
    virtual_size: int
    raw_offset: int
    raw_size: int
    characteristics: int
    entropy: float = 0.0
    section_type: SectionType = SectionType.OTHER
    is_executable: bool = False
    is_writable: bool = False
    is_readable: bool = False


@dataclass
class ImportEntry:
    """Single import table entry."""
    name: str
    dll: str = ""
    ordinal: Optional[int] = None
    hint: Optional[int] = None
    address: int = 0


@dataclass
class ExportEntry:
    """Single export table entry."""
    name: str
    ordinal: Optional[int] = None
    address: int = 0
    forwarded: bool = False


@dataclass
class ExtractedString:
    """String found within binary data."""
    text: str
    offset: int
    encoding: StringEncoding = StringEncoding.ASCII
    entropy: float = 0.0
    is_printable: bool = True
    section: str = ""
    raw_bytes: bytes = b""

    def decode_base64(self) -> str:
        """Attempt base64 decode of the string content."""
        import base64
        try:
            return base64.b64decode(self.text).decode("utf-8", errors="replace")
        except Exception:
            return ""


@dataclass
class CFGNode:
    """Basic block in a control flow graph."""
    address: int
    size: int
    instructions: List[Dict[str, str]] = field(default_factory=list)
    successors: List[int] = field(default_factory=list)
    predecessors: List[int] = field(default_factory=list)


@dataclass
class CFGGraph:
    """Control flow graph representation."""
    entry_point: int
    nodes: List[CFGNode] = field(default_factory=list)
    edges: List[Tuple[int, int]] = field(default_factory=list)
    function_name: str = ""


@dataclass
class FunctionDiff:
    """Result of comparing a function between two binaries."""
    name: str
    old_address: int = 0
    new_address: int = 0
    change_type: str = "modified"
    changes: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class BinaryDiff:
    """Full result of comparing two binaries."""
    old_path: str
    new_path: str
    modified: List[FunctionDiff] = field(default_factory=list)
    added: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)
    unchanged_count: int = 0


@dataclass
class YaraMatch:
    """YARA rule match result."""
    rule_name: str
    namespace: str = "default"
    tags: List[str] = field(default_factory=list)
    matched_strings: List[Tuple[int, str]] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BinaryMetadata:
    """Complete metadata for a loaded binary."""
    path: str
    format: BinaryFormat
    architecture: Architecture
    entry_point: int
    base_address: int = 0
    size: int = 0
    md5: str = ""
    sha256: str = ""
    sha1: str = ""
    sections: List[SectionInfo] = field(default_factory=list)
    imports: List[ImportEntry] = field(default_factory=list)
    exports: List[ExportEntry] = field(default_factory=list)
    linked_libraries: List[str] = field(default_factory=list)
    compiler_info: str = ""
    compile_timestamp: Optional[int] = None
    is_stripped: bool = False
    is_pie: bool = False
    is_64bit: bool = False


@dataclass
class TriageReport:
    """Automated triage result for a binary sample."""
    metadata: BinaryMetadata
    risk_level: RiskLevel = RiskLevel.LOW
    risk_score: int = 0
    packer: PackerType = PackerType.None_
    capabilities: List[CapabilityFlag] = field(default_factory=list)
    interesting_strings: List[ExtractedString] = field(default_factory=list)
    yara_matches: List[YaraMatch] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)

    @staticmethod
    def format_text(report: "TriageReport") -> str:
        """Format triage report as human-readable text."""
        lines = [
            "=" * 60,
            "BINARY TRIAGE REPORT",
            "=" * 60,
            f"File: {report.metadata.path}",
            f"Format: {report.metadata.format.name}",
            f"Architecture: {report.metadata.architecture.value}",
            f"Size: {report.metadata.size} bytes",
            f"SHA-256: {report.metadata.sha256}",
            "",
            "--- Sections ---",
        ]
        for sec in report.metadata.sections:
            lines.append(
                f"  {sec.name:<16} VA=0x{sec.virtual_address:08x} "
                f"Size=0x{sec.virtual_size:08x} Entropy={sec.entropy:.2f} "
                f"{'[EXEC]' if sec.is_executable else ''}"
            )
        lines.append(f"\nPacker: {report.packer.name}")
        lines.append(f"Risk: {report.risk_level.name} (score={report.risk_score})")
        lines.append(f"Capabilities: {', '.join(c.name for c in report.capabilities)}")
        if report.yara_matches:
            lines.append(f"YARA Matches: {', '.join(m.rule_name for m in report.yara_matches)}")
        if report.indicators:
            lines.append("\nIndicators:")
            for ind in report.indicators:
                lines.append(f"  [!] {ind}")
        lines.append("=" * 60)
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helper Utilities
# ---------------------------------------------------------------------------

def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy of a byte sequence (0.0 to 8.0)."""
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    entropy = 0.0
    for count in counts.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log2(probability)
    return entropy


def compute_hashes(data: bytes) -> Dict[str, str]:
    """Compute MD5, SHA-1, and SHA-256 hashes for binary data."""
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def detect_format(data: bytes) -> BinaryFormat:
    """Detect binary format from magic bytes."""
    if len(data) < 4:
        return BinaryFormat.UNKNOWN
    if data[:4] == b"\x7fELF":
        return BinaryFormat.ELF
    if data[:2] == b"MZ" or data[:4] == b"\x00\x00\x00\x00" and len(data) > 0x3C:
        pe_offset = struct.unpack_from("<I", data, 0x3C)[0] if len(data) > 0x3F else 0
        if pe_offset < len(data) - 4 and data[pe_offset:pe_offset + 4] == b"PE\x00\x00":
            return BinaryFormat.PE
    if data[:2] in (b"\xfe\xed", b"\xce\xfa", b"\xfe\xfa", b"\xcf\xfa"):
        return BinaryFormat.MACHO
    if data[0:4] in (b"\xca\xfe\xba\xbe", b"\xbe\xba\xfe\xca"):
        return BinaryFormat.MACHO
    return BinaryFormat.UNKNOWN


def extract_printable_strings(
    data: bytes,
    min_length: int = 4,
    offset_base: int = 0,
) -> List[ExtractedString]:
    """Extract ASCII printable strings from raw bytes."""
    results = []
    current = []
    start = 0
    for i, byte in enumerate(data):
        if 0x20 <= byte <= 0x7E:
            if not current:
                start = i
            current.append(chr(byte))
        else:
            if len(current) >= min_length:
                text = "".join(current)
                raw = bytes(current)
                results.append(
                    ExtractedString(
                        text=text,
                        offset=offset_base + start,
                        encoding=StringEncoding.ASCII,
                        entropy=calculate_entropy(raw),
                        raw_bytes=raw,
                    )
                )
            current = []
    if len(current) >= min_length:
        text = "".join(current)
        raw = bytes(current)
        results.append(
            ExtractedString(
                text=text,
                offset=offset_base + start,
                encoding=StringEncoding.ASCII,
                entropy=calculate_entropy(raw),
                raw_bytes=raw,
            )
        )
    return results


# ---------------------------------------------------------------------------
# API Capability Mapping
# ---------------------------------------------------------------------------

NETWORK_APIS = {
    "socket", "connect", "bind", "listen", "accept", "send", "recv",
    "sendto", "recvfrom", "getaddrinfo", "gethostbyname",
    "InternetOpenA", "InternetOpenW", "InternetConnectA", "InternetConnectW",
    "HttpOpenRequestA", "HttpOpenRequestW", "HttpSendRequestA",
    "URLDownloadToFileA", "URLDownloadToFileW", "WinHttpOpen",
    "WinHttpConnect", "WinHttpSendRequest", "WSAStartup",
    "send", "recv", "WSASend", "WSARecv",
}

CRYPTO_APIS = {
    "CryptEncrypt", "CryptDecrypt", "CryptCreateHash", "CryptHashData",
    "CryptDeriveKey", "CryptAcquireContext", "CryptGenKey",
    "BCryptEncrypt", "BCryptDecrypt", "EVP_EncryptUpdate",
    "EVP_DecryptUpdate", "AES_set_encrypt_key", "AES_set_decrypt_key",
    "RSA_public_encrypt", "RSA_private_decrypt",
}

FILE_APIS = {
    "CreateFileA", "CreateFileW", "ReadFile", "WriteFile", "DeleteFileA",
    "DeleteFileW", "CopyFileA", "CopyFileW", "MoveFileA", "MoveFileW",
    "FindFirstFileA", "FindFirstFileW", "FindNextFileA", "FindNextFileW",
    "fopen", "fread", "fwrite", "fclose", "open", "read", "write", "close",
    "mmap", "CreateFileMappingA", "CreateFileMappingW",
}

REGISTRY_APIS = {
    "RegOpenKeyExA", "RegOpenKeyExW", "RegSetValueExA", "RegSetValueExW",
    "RegQueryValueExA", "RegQueryValueExW", "RegCreateKeyExA",
    "RegCreateKeyExW", "RegDeleteKeyA", "RegDeleteKeyW",
}

PROCESS_APIS = {
    "CreateProcessA", "CreateProcessW", "OpenProcess", "VirtualAllocEx",
    "WriteProcessMemory", "CreateRemoteThread", "NtCreateThreadEx",
    "QueueUserAPC", "SetWindowsHookExA", "SetWindowsHookExW",
    "fork", "execve", "ptrace", "dlopen",
}

ANTI_DEBUG_APIS = {
    "IsDebuggerPresent", "CheckRemoteDebuggerPresent",
    "NtQueryInformationProcess", "OutputDebugStringA",
    "GetTickCount", "QueryPerformanceCounter", "rdtsc",
}

CAPABILITY_MAP: Dict[CapabilityFlag, Set[str]] = {
    CapabilityFlag.NETWORK: NETWORK_APIS,
    CapabilityFlag.CRYPTO: CRYPTO_APIS,
    CapabilityFlag.FILE_IO: FILE_APIS,
    CapabilityFlag.REGISTRY: REGISTRY_APIS,
    CapabilityFlag.PROCESS_CREATE: PROCESS_APIS,
    CapabilityFlag.ANTI_DEBUG: ANTI_DEBUG_APIS,
    CapabilityFlag.DLL_INJECTION: {"LoadLibraryA", "LoadLibraryW", "GetProcAddress", "LdrLoadDll"},
    CapabilityFlag.PERSISTENCE: {
        "RegSetValueExA", "RegSetValueExW", "CreateServiceA", "CreateServiceW",
        "SchTasksCreate", "HKEY_LOCAL_MACHINE",
    },
    CapabilityFlag.PRIVILEGE_ESCALATION: {
        "AdjustTokenPrivileges", "ImpersonateLoggedOnUser",
        "SetThreadToken", "DuplicateTokenEx",
    },
    CapabilityFlag.DATA_EXFIL: {
        "InternetOpenA", "InternetOpenW", "HttpSendRequestA",
        "URLDownloadToFileA", "send", "WSASend",
    },
}


# ---------------------------------------------------------------------------
# Main Engine Class
# ---------------------------------------------------------------------------

class BinaryAnalyzer:
    """
    Primary engine for loading and analyzing binary executables.

    Usage:
        analyzer = BinaryAnalyzer()
        metadata = analyzer.load("/path/to/binary")
        print(metadata.sections)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or {}
        self._metadata: Optional[BinaryMetadata] = None
        self._raw_data: Optional[bytes] = None
        self._status: str = "idle"

    def configure(self, **kwargs: Any) -> None:
        """Update engine configuration parameters."""
        self._config.update(kwargs)

    def get_status(self) -> str:
        """Return current engine status."""
        return self._status

    def load(self, path: Union[str, Path]) -> BinaryMetadata:
        """Load a binary file and parse its metadata."""
        self._status = "loading"
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Binary not found: {path}")

        self._raw_data = path.read_bytes()
        fmt = detect_format(self._raw_data)
        hashes = compute_hashes(self._raw_data)

        self._metadata = BinaryMetadata(
            path=str(path),
            format=fmt,
            architecture=Architecture.UNKNOWN,
            entry_point=0,
            size=len(self._raw_data),
            md5=hashes["md5"],
            sha1=hashes["sha1"],
            sha256=hashes["sha256"],
        )

        if fmt == BinaryFormat.ELF:
            self._parse_elf()
        elif fmt == BinaryFormat.PE:
            self._parse_pe()
        else:
            self._status = "loaded (format not fully supported)"
            return self._metadata

        self._status = "loaded"
        return self._metadata

    def validate(self) -> bool:
        """Validate that the loaded binary has been parsed correctly."""
        if self._metadata is None:
            return False
        if self._metadata.format == BinaryFormat.UNKNOWN:
            return False
        return True

    def get_sections(self) -> List[SectionInfo]:
        """Return parsed sections from the loaded binary."""
        if self._metadata is None:
            return []
        return self._metadata.sections

    def get_imports(self) -> List[ImportEntry]:
        """Return parsed imports from the loaded binary."""
        if self._metadata is None:
            return []
        return self._metadata.imports

    def extract_strings(
        self, min_length: int = 4, section_filter: Optional[str] = None
    ) -> List[ExtractedString]:
        """Extract printable strings from the binary or a specific section."""
        if self._raw_data is None:
            return []
        if section_filter and self._metadata:
            for sec in self._metadata.sections:
                if sec.name == section_filter:
                    start = sec.raw_offset
                    end = start + sec.raw_size
                    data = self._raw_data[start:end]
                    return extract_printable_strings(data, min_length, offset_base=start)
        return extract_printable_strings(self._raw_data, min_length)

    def calculate_section_entropies(self) -> Dict[str, float]:
        """Calculate entropy for each section."""
        results = {}
        if self._raw_data is None or self._metadata is None:
            return results
        for sec in self._metadata.sections:
            start = sec.raw_offset
            end = start + sec.raw_size
            if end <= len(self._raw_data):
                sec.entropy = calculate_entropy(self._raw_data[start:end])
                results[sec.name] = sec.entropy
        return results

    def infer_capabilities(self) -> List[CapabilityFlag]:
        """Infer behavioral capabilities from the import table."""
        if self._metadata is None:
            return []
        import_names = {imp.name.lower() for imp in self._metadata.imports}
        detected = []
        for cap, api_set in CAPABILITY_MAP.items():
            if any(api.lower() in import_names for api in api_set):
                detected.append(cap)
        return detected

    def detect_packer(self) -> PackerType:
        """Heuristic packer detection based on entropy and signatures."""
        if self._raw_data is None or self._metadata is None:
            return PackerType.None_

        text = b""
        for sec in self._metadata.sections:
            if sec.is_executable:
                start = sec.raw_offset
                end = start + sec.raw_size
                if end <= len(self._raw_data):
                    text += self._raw_data[start:end]

        if not text:
            return PackerType.None_

        entropy = calculate_entropy(text)
        data_str = self._raw_data[:4096]

        if b"UPX!" in data_str or b"UPX0" in data_str or b"UPX1" in data_str:
            return PackerType.UPX
        if b".themida" in data_str or b"Xenocode" in data_str:
            return PackerType.THEMIDA
        if b".vmp0" in data_str or b".vmp1" in data_str:
            return PackerType.VMPROTECT
        if entropy > 7.8:
            return PackerType.Custom

        return PackerType.None_

    def diff(self, other_path: Union[str, Path]) -> BinaryDiff:
        """Perform a structural diff between this binary and another."""
        other = BinaryAnalyzer()
        other.load(other_path)

        diff_result = BinaryDiff(
            old_path=self._metadata.path if self._metadata else "",
            new_path=str(other_path),
        )

        old_imports = {imp.name for imp in (self._metadata.imports if self._metadata else [])}
        new_imports = {imp.name for imp in other.get_imports()}

        added = new_imports - old_imports
        removed = old_imports - new_imports

        diff_result.added = list(added)
        diff_result.removed = list(removed)
        diff_result.unchanged_count = len(old_imports & new_imports)

        for name in old_imports & new_imports:
            diff_result.modified.append(
                FunctionDiff(name=name, change_type="unchanged")
            )

        return diff_result

    # ------------------------------------------------------------------
    # Internal parsers
    # ------------------------------------------------------------------

    def _parse_elf(self) -> None:
        """Parse ELF header and section headers."""
        if self._raw_data is None or self._metadata is None:
            return
        data = self._raw_data
        if len(data) < 52:
            return

        ei_class = data[4]
        is_64 = ei_class == 2
        self._metadata.is_64bit = is_64

        if is_64:
            if len(data) < 64:
                return
            e_machine = struct.unpack_from("<H", data, 18)[0]
            e_entry = struct.unpack_from("<Q", data, 24)[0]
            e_phoff = struct.unpack_from("<Q", data, 32)[0]
            e_shoff = struct.unpack_from("<Q", data, 40)[0]
            e_shentsize = struct.unpack_from("<H", data, 58)[0]
            e_shnum = struct.unpack_from("<H", data, 60)[0]
            e_shstrndx = struct.unpack_from("<H", data, 62)[0]
        else:
            e_machine = struct.unpack_from("<H", data, 18)[0]
            e_entry = struct.unpack_from("<I", data, 24)[0]
            e_phoff = struct.unpack_from("<I", data, 28)[0]
            e_shoff = struct.unpack_from("<I", data, 32)[0]
            e_shentsize = struct.unpack_from("<H", data, 46)[0]
            e_shnum = struct.unpack_from("<H", data, 48)[0]
            e_shstrndx = struct.unpack_from("<H", data, 50)[0]

        self._metadata.entry_point = e_entry
        self._metadata.architecture = self._elf_machine_to_arch(e_machine)

        if e_shoff == 0 or e_shnum == 0:
            return

        strtab_off = e_shoff + e_shstrndx * e_shentsize
        if strtab_off + e_shentsize > len(data):
            return
        strtab_offset = struct.unpack_from("<Q" if is_64 else "<I", data, strtab_off + 24 if is_64 else strtab_off + 16)[0]
        strtab_size = struct.unpack_from("<Q" if is_64 else "<I", data, strtab_off + 32 if is_64 else strtab_off + 20)[0]
        strtab_data = data[strtab_offset:strtab_offset + strtab_size]

        for i in range(e_shnum):
            off = e_shoff + i * e_shentsize
            if off + e_shentsize > len(data):
                break
            sh_name_idx = struct.unpack_from("<I", data, off)[0]
            sh_flags = struct.unpack_from("<Q" if is_64 else "<I", data, off + 4 if is_64 else off + 8)[0]
            sh_addr = struct.unpack_from("<Q" if is_64 else "<I", data, off + 16 if is_64 else off + 12)[0]
            sh_offset = struct.unpack_from("<Q" if is_64 else "<I", data, off + 24 if is_64 else off + 16)[0]
            sh_size = struct.unpack_from("<Q" if is_64 else "<I", data, off + 32 if is_64 else off + 20)[0]

            name_end = strtab_data.find(b"\x00", sh_name_idx)
            name = strtab_data[sh_name_idx:name_end].decode("utf-8", errors="replace") if name_end > sh_name_idx else f"sec_{i}"

            sec_data = data[sh_offset:sh_offset + sh_size] if sh_offset + sh_size <= len(data) else b""
            entropy = calculate_entropy(sec_data) if sec_data else 0.0

            section = SectionInfo(
                name=name,
                virtual_address=sh_addr,
                virtual_size=sh_size,
                raw_offset=sh_offset,
                raw_size=sh_size,
                characteristics=sh_flags,
                entropy=entropy,
                is_executable=bool(sh_flags & 0x4),
                is_writable=bool(sh_flags & 0x1),
                is_readable=True,
            )
            self._metadata.sections.append(section)

    def _parse_pe(self) -> None:
        """Parse PE header and section table."""
        if self._raw_data is None or self._metadata is None:
            return
        data = self._raw_data
        if len(data) < 0x40:
            return

        pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
        if pe_offset + 24 > len(data):
            return
        if data[pe_offset:pe_offset + 4] != b"PE\x00\x00":
            return

        coff_offset = pe_offset + 4
        machine = struct.unpack_from("<H", data, coff_offset)[0]
        num_sections = struct.unpack_from("<H", data, coff_offset + 2)[0]
        opt_hdr_size = struct.unpack_from("<H", data, coff_offset + 16)[0]
        opt_offset = coff_offset + 20

        self._metadata.architecture = self._pe_machine_to_arch(machine)
        self._metadata.is_64bit = machine in (0x8664, 0xAA64)

        if opt_offset + opt_hdr_size > len(data):
            return

        if self._metadata.is_64bit:
            magic = struct.unpack_from("<H", data, opt_offset)[0]
            if magic == 0x20B:
                self._metadata.entry_point = struct.unpack_from("<I", data, opt_offset + 16)[0]
                self._metadata.base_address = struct.unpack_from("<Q", data, opt_offset + 24)[0]
        else:
            self._metadata.entry_point = struct.unpack_from("<I", data, opt_offset + 16)[0]
            self._metadata.base_address = struct.unpack_from("<I", data, opt_offset + 28)[0]

        sec_offset = opt_offset + opt_hdr_size
        for i in range(min(num_sections, 96)):
            off = sec_offset + i * 40
            if off + 40 > len(data):
                break
            name_raw = data[off:off + 8]
            name = name_raw.rstrip(b"\x00").decode("utf-8", errors="replace")
            vsize = struct.unpack_from("<I", data, off + 8)[0]
            va = struct.unpack_from("<I", data, off + 12)[0]
            raw_size = struct.unpack_from("<I", data, off + 16)[0]
            raw_ptr = struct.unpack_from("<I", data, off + 20)[0]
            chars = struct.unpack_from("<I", data, off + 36)[0]

            sec_data = data[raw_ptr:raw_ptr + raw_size] if raw_ptr + raw_size <= len(data) else b""
            entropy = calculate_entropy(sec_data) if sec_data else 0.0

            section = SectionInfo(
                name=name,
                virtual_address=va,
                virtual_size=vsize,
                raw_offset=raw_ptr,
                raw_size=raw_size,
                characteristics=chars,
                entropy=entropy,
                is_executable=bool(chars & 0x20000000),
                is_writable=bool(chars & 0x80000000),
                is_readable=bool(chars & 0x40000000),
            )
            self._metadata.sections.append(section)

    @staticmethod
    def _elf_machine_to_arch(machine: int) -> Architecture:
        """Map ELF e_machine value to Architecture enum."""
        mapping = {
            0x03: Architecture.X86,
            0x3E: Architecture.X86_64,
            0x28: Architecture.ARM,
            0xB7: Architecture.ARM64,
            0x08: Architecture.MIPS,
            0x14: Architecture.PPC,
            0xF3: Architecture.RISCV,
        }
        return mapping.get(machine, Architecture.UNKNOWN)

    @staticmethod
    def _pe_machine_to_arch(machine: int) -> Architecture:
        """Map PE Machine value to Architecture enum."""
        mapping = {
            0x14C: Architecture.X86,
            0x8664: Architecture.X86_64,
            0x1C0: Architecture.ARM,
            0xAA64: Architecture.ARM64,
            0x01F0: Architecture.PPC,
        }
        return mapping.get(machine, Architecture.UNKNOWN)


# ---------------------------------------------------------------------------
# High-level Triage Engine
# ---------------------------------------------------------------------------

class TriageEngine:
    """
    Automated binary triage — produces a structured report with risk scoring.

    Usage:
        engine = TriageEngine()
        report = engine.triage("/path/to/sample")
        print(TriageReport.format_text(report))
    """

    def __init__(self, yara_rules_dir: Optional[str] = None):
        self._analyzer = BinaryAnalyzer()
        self._yara_rules_dir = yara_rules_dir

    def configure(self, **kwargs: Any) -> None:
        """Configure the underlying analyzer."""
        self._analyzer.configure(**kwargs)

    def run(self, path: Union[str, Path]) -> TriageReport:
        """Execute full triage pipeline and return structured report."""
        return self.triage(path)

    def triage(self, path: Union[str, Path]) -> TriageReport:
        """Perform automated triage on a binary sample."""
        metadata = self._analyzer.load(path)
        self._analyzer.calculate_section_entropies()

        packer = self._analyzer.detect_packer()
        capabilities = self._analyzer.infer_capabilities()
        strings = self._analyzer.extract_strings(min_length=6)
        interesting = self._filter_interesting_strings(strings)

        risk_score = self._calculate_risk_score(metadata, packer, capabilities, interesting)
        risk_level = self._score_to_level(risk_score)
        indicators = self._generate_indicators(metadata, packer, capabilities)

        return TriageReport(
            metadata=metadata,
            risk_level=risk_level,
            risk_score=risk_score,
            packer=packer,
            capabilities=capabilities,
            interesting_strings=interesting,
            indicators=indicators,
        )

    def validate(self, report: TriageReport) -> bool:
        """Validate that a triage report is complete and internally consistent."""
        if report.metadata.format == BinaryFormat.UNKNOWN:
            return False
        if report.risk_score < 0 or report.risk_score > 100:
            return False
        return True

    def get_status(self) -> str:
        """Return the current triage engine status."""
        return self._analyzer.get_status()

    @staticmethod
    def _filter_interesting_strings(strings: List[ExtractedString]) -> List[ExtractedString]:
        """Filter strings to those likely relevant for triage."""
        interesting = []
        indicators = [
            "password", "passwd", "secret", "token", "api_key", "apikey",
            "http://", "https://", "ftp://", "mailto:", "\\\\", "cmd.exe",
            "/bin/sh", "/bin/bash", "select ", "insert ", "update ",
            "drop ", "union ", "eval(", "exec(", "system(",
        ]
        for s in strings:
            lower = s.text.lower()
            if any(ind in lower for ind in indicators):
                interesting.append(s)
            elif s.entropy > 5.5 and len(s.text) > 8:
                interesting.append(s)
        return interesting[:50]

    @staticmethod
    def _calculate_risk_score(
        metadata: BinaryMetadata,
        packer: PackerType,
        capabilities: List[CapabilityFlag],
        strings: List[ExtractedString],
    ) -> int:
        """Calculate a 0-100 risk score based on analysis results."""
        score = 0
        if packer != PackerType.None_:
            score += 20
        if CapabilityFlag.ANTI_DEBUG in capabilities:
            score += 15
        if CapabilityFlag.NETWORK in capabilities:
            score += 10
        if CapabilityFlag.PROCESS_CREATE in capabilities:
            score += 15
        if CapabilityFlag.DLL_INJECTION in capabilities:
            score += 20
        if CapabilityFlag.REGISTRY in capabilities:
            score += 5
        high_entropy_sections = sum(
            1 for sec in metadata.sections if sec.entropy > 7.0
        )
        score += min(high_entropy_sections * 5, 15)
        score += min(len(strings) // 2, 10)
        return min(score, 100)

    @staticmethod
    def _score_to_level(score: int) -> RiskLevel:
        """Map numeric risk score to RiskLevel enum."""
        if score < 20:
            return RiskLevel.LOW
        if score < 50:
            return RiskLevel.MEDIUM
        if score < 75:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    @staticmethod
    def _generate_indicators(
        metadata: BinaryMetadata,
        packer: PackerType,
        capabilities: List[CapabilityFlag],
    ) -> List[str]:
        """Generate human-readable risk indicators."""
        indicators = []
        if packer != PackerType.None_:
            indicators.append(f"Packer detected: {packer.name}")
        if CapabilityFlag.ANTI_DEBUG in capabilities:
            indicators.append("Anti-debugging techniques present")
        if CapabilityFlag.DLL_INJECTION in capabilities:
            indicators.append("DLL injection capability detected")
        if CapabilityFlag.NETWORK in capabilities and CapabilityFlag.CRYPTO in capabilities:
            indicators.append("Network + Crypto: potential C2 communication")
        high_ent = [s for s in metadata.sections if s.entropy > 7.5]
        if high_ent:
            indicators.append(
                f"High-entropy sections: {', '.join(s.name for s in high_ent)}"
            )
        if metadata.is_stripped:
            indicators.append("Binary is stripped (no symbols)")
        return indicators


# ---------------------------------------------------------------------------
# main() demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the binary analysis engine with a synthetic test binary."""
    print("=" * 60)
    print("Binary Analysis Engine — Demo")
    print("=" * 60)

    # Create a synthetic minimal PE-like binary for demonstration
    pe_header = bytearray(1024)
    pe_header[0:2] = b"MZ"
    struct.pack_into("<I", pe_header, 0x3C, 0x80)
    pe_header[0x80:0x84] = b"PE\x00\x00"
    struct.pack_into("<H", pe_header, 0x84, 0x14C)  # i386
    struct.pack_into("<H", pe_header, 0x86, 1)  # 1 section
    struct.pack_into("<I", pe_header, 0xA0, 0x1000)  # entry point

    # Add a section with some printable data
    section_data = b"This is a test string with some data"
    section_data += b"\x00" * (512 - len(section_data))
    section_data += b"AAAA" * 128  # high entropy region

    test_binary = bytes(pe_header) + section_data
    test_path = Path("test_sample.bin")
    test_path.write_bytes(test_binary)

    try:
        # Demo 1: Basic Analysis
        print("\n[1] Basic Analysis")
        analyzer = BinaryAnalyzer()
        metadata = analyzer.load(test_path)
        print(f"  Format: {metadata.format.name}")
        print(f"  Architecture: {metadata.architecture.value}")
        print(f"  Size: {metadata.size} bytes")
        print(f"  MD5: {metadata.md5}")
        print(f"  Sections: {len(metadata.sections)}")

        # Demo 2: Section Analysis
        print("\n[2] Section Analysis")
        for sec in analyzer.get_sections():
            print(f"  {sec.name}: VA=0x{sec.virtual_address:08x} "
                  f"Entropy={sec.entropy:.2f} Exec={sec.is_executable}")

        # Demo 3: String Extraction
        print("\n[3] String Extraction")
        strings = analyzer.extract_strings(min_length=5)
        for s in strings[:10]:
            print(f"  0x{s.offset:04x}: {s.text}")

        # Demo 4: Capability Inference
        print("\n[4] Capability Inference")
        caps = analyzer.infer_capabilities()
        if caps:
            for cap in caps:
                print(f"  [+] {cap.name}")
        else:
            print("  No capabilities detected (minimal binary)")

        # Demo 5: Packer Detection
        print("\n[5] Packer Detection")
        packer = analyzer.detect_packer()
        print(f"  Packer: {packer.name}")

        # Demo 6: Triage Report
        print("\n[6] Automated Triage")
        engine = TriageEngine()
        report = engine.triage(test_path)
        print(TriageReport.format_text(report))

        # Demo 7: Validation
        print("\n[7] Validation")
        print(f"  Analyzer valid: {analyzer.validate()}")
        print(f"  Triage valid: {engine.validate(report)}")
        print(f"  Engine status: {analyzer.get_status()}")

    finally:
        test_path.unlink(missing_ok=True)

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
