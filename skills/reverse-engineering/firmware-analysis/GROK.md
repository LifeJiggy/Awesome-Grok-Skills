---
name: "firmware-analysis"
category: "reverse-engineering"
version: "1.0.0"
tags: ["reverse-engineering", "firmware-analysis", "iot", "embedded", "extraction"]
---

# Firmware Analysis — Reverse Engineering Module

## Overview

Firmware analysis is the process of extracting, examining, and reverse engineering embedded software that runs on hardware devices — routers, IoT devices, industrial controllers, IoT gateways, smart home devices, medical devices, and more. Unlike general-purpose software, firmware is tightly coupled to specific hardware platforms, uses specialized file formats, and often contains sensitive configuration data, hardcoded credentials, and proprietary protocol implementations.

This module provides a comprehensive framework for the firmware analysis lifecycle: image acquisition, format identification, filesystem extraction, code analysis, configuration extraction, vulnerability discovery, and hardware interface identification. It supports common firmware formats (squashfs, JFFS2, CramFS, UBIFS, ROMFS, ZIP-based), embedded architectures (ARM, MIPS, x86, PowerPC), and analysis approaches (static, dynamic via emulation, and hardware-assisted).

Firmware analysis is critical for IoT security research, product security assessments, reverse engineering proprietary protocols, recovering hardcoded credentials, and identifying vulnerabilities in devices that cannot be easily updated. The unique challenge of firmware analysis is the tight integration between software and hardware — understanding the firmware requires understanding the device it runs on.

This module integrates with industry-standard tools (binwalk for extraction, QEMU for emulation, firmware-mod-kit for modification) and provides Python-native analysis pipelines for automated firmware characterization, filesystem analysis, and vulnerability scanning.

## Core Capabilities

### 1. Firmware Image Identification and Validation
Detect firmware file formats (raw flash dumps, TRX, uImage, FIT, ELF, ZIP-based), validate image integrity (checksum verification, signature validation), identify the target hardware platform (architecture, board type, bootloader), and extract embedded metadata (build dates, version strings, manufacturer information).

### 2. Filesystem Extraction and Analysis
Extract embedded filesystems (SquashFS, JFFS2, CramFS, UBIFS, ROMFS, ext2/ext3/ext4, FAT) from firmware images. Mount and analyze extracted filesystems: directory structure, file permissions, symlinks, and deleted file recovery. Parse configuration files, startup scripts, and embedded databases.

### 3. Binary and Code Analysis
Identify and extract executable binaries from firmware images. Determine architecture (ARM, MIPS, x86, PowerPC, RISC-V), endianness, and linking information. Apply binary analysis techniques (disassembly, decompilation, string extraction) to firmware-specific binaries, with special attention to embedded Linux userspace and kernel components.

### 4. Configuration and Credential Extraction
Extract hardcoded credentials from firmware: default passwords, API keys, certificates, private keys, and encryption secrets. Parse configuration files (UCI, CSV, JSON, proprietary formats) to extract device settings, network configurations, cloud service endpoints, and authentication tokens.

### 5. Hardware Interface Identification
Analyze firmware for hardware interfaces: UART, JTAG, SPI, I2C, GPIO, and debug ports. Extract bootloader configurations that reveal debug interfaces. Identify firmware update mechanisms that may be exploitable for firmware modification or extraction.

### 6. Emulation and Dynamic Analysis
Emulate firmware binaries using QEMU to observe runtime behavior: system calls, network interactions, file system access, and hardware interactions. Use firmware analysis frameworks (FAT, firmadyne) to build complete emulation environments for dynamic analysis.

### 7. Vulnerability Discovery
Scan firmware for known vulnerabilities: outdated libraries with known CVEs, hardcoded credentials, insecure protocols (telnet, HTTP with cleartext), improper access control on debug interfaces, and insecure firmware update mechanisms. Cross-reference extracted software versions against vulnerability databases.

### 8. Firmware Modification and Repackaging
Modify extracted firmware: replace binaries, inject scripts, change configurations, patch vulnerabilities, and repackage into a valid firmware image for testing. This capability supports authorized security testing and custom firmware development.

## Usage Examples

### Firmware Image Identification

```python
from firmware_analysis_engine import FirmwareAnalyzer, FirmwareFormat

analyzer = FirmwareAnalyzer()
info = analyzer.identify("/path/to/firmware.bin")

print(f"Format: {info.format.name}")
print(f"Architecture: {info.architecture}")
print(f"Target device: {info.device_type}")
print(f"Filesystem: {info.filesystem_type}")
print(f"Size: {info.image_size} bytes")
print(f"Checksum valid: {info.checksum_valid}")
print(f"Build date: {info.build_date}")
print(f"Version: {info.version}")
```

### Filesystem Extraction

```python
from firmware_analysis_engine import FilesystemExtractor

extractor = FilesystemExtractor()
fs = extractor.extract("/path/to/firmware.bin", output_dir="/tmp/firmware_fs")

print(f"Filesystem type: {fs.fs_type}")
print(f"Total files: {fs.total_files}")
print(f"Total size: {fs.total_size} bytes")

print("\nDirectory structure:")
for entry in fs.entries[:20]:
    perm = entry.permissions
    print(f"  {perm} {entry.size:>8} {entry.path}")
```

### Credential Extraction

```python
from firmware_analysis_engine import CredentialExtractor

extractor = CredentialExtractor()
credentials = extractor.extract("/tmp/firmware_fs")

print(f"Found {len(credentials)} credentials:\n")
for cred in credentials:
    print(f"  [{cred.cred_type.name}] {cred.source_file}")
    print(f"    Value: {cred.redacted_value}")
    print(f"    Context: {cred.context}")
    print(f"    Confidence: {cred.confidence:.0%}")
    print()
```

### Hardcoded Password Recovery

```python
from firmware_analysis_engine import PasswordRecovery

recovery = PasswordRecovery()
passwords = recovery.find_passwords("/tmp/firmware_fs")

print(f"Password files found:")
for pw_file in passwords:
    print(f"\n  {pw_file.file_path}")
    print(f"  Users:")
    for user in pw_file.entries:
        print(f"    {user.username}: {user.hash_type} (uid={user.uid})")
        if user.cracked:
            print(f"    Cracked: {user.plaintext}")
```

### Network Configuration Analysis

```python
from firmware_analysis_engine import NetworkAnalyzer

analyzer = NetworkAnalyzer()
config = analyzer.analyze("/tmp/firmware_fs")

print("Network Configuration:")
print(f"  Default IP: {config.default_ip}")
print(f"  DHCP enabled: {config.dhcp_enabled}")
print(f"  DNS servers: {config.dns_servers}")
print(f"  Open ports: {config.open_ports}")

print("\nWireless Configuration:")
for wlan in config.wireless_interfaces:
    print(f"  {wlan.interface}: SSID={wlan.ssid}, Security={wlan.security}")

print("\nRemote Access:")
for access in config.remote_access:
    print(f"  {access.protocol} on port {access.port}: {'Enabled' if access.enabled else 'Disabled'}")
```

### Binary Analysis within Firmware

```python
from firmware_analysis_engine import FirmwareBinaryAnalyzer

analyzer = FirmwareBinaryAnalyzer()
results = analyzer.analyze_binaries("/tmp/firmware_fs")

print(f"Binaries found: {len(results)}")
for binary in results[:10]:
    print(f"\n  {binary.path}")
    print(f"    Architecture: {binary.architecture}")
    print(f"    Linked libraries: {binary.linked_libraries}")
    print(f"    Suspicious imports: {binary.suspicious_imports}")
    print(f"    Strings of interest: {len(binary.interesting_strings)}")
```

### Firmware Vulnerability Scan

```python
from firmware_analysis_engine import VulnerabilityScanner

scanner = VulnerabilityScanner()
findings = scanner.scan("/tmp/firmware_fs")

print(f"Vulnerabilities: {len(findings)}\n")
for finding in findings:
    print(f"  [{finding.severity}] {finding.title}")
    print(f"    File: {finding.file_path}")
    print(f"    Description: {finding.description}")
    print(f"    Recommendation: {finding.recommendation}")
    print()
```

### QEMU Emulation Setup

```python
from firmware_analysis_engine import EmulationEngine

emulator = EmulationEngine()
config = emulator.setup_emulation(
    firmware_path="/path/to/firmware.bin",
    extracted_fs="/tmp/firmware_fs",
    arch="mips",
    endianness="little",
    rootfs_type="squashfs",
)

print(f"Emulation configuration:")
print(f"  QEMU binary: {config.qemu_binary}")
print(f"  Kernel: {config.kernel_path}")
print(f"  Root filesystem: {config.rootfs_path}")
print(f"  Network: {config.network_config}")
print(f"  Ports mapped: {config.port_mapping}")

print(f"\nStartup command:")
print(f"  {config.startup_command}")
```

### Firmware Update Mechanism Analysis

```python
from firmware_analysis_engine import UpdateMechanismAnalyzer

analyzer = UpdateMechanismAnalyzer()
mechanisms = analyzer.analyze("/tmp/firmware_fs")

print("Firmware Update Mechanisms:")
for mech in mechanisms:
    print(f"\n  {mech.mechanism_type}")
    print(f"    Endpoint: {mech.endpoint}")
    print(f"    Protocol: {mech.protocol}")
    print(f"    Authentication: {mech.auth_method}")
    print(f"    Integrity check: {mech.integrity_check}")
    print(f"    Encryption: {mech.encryption}")
    if mech.vulnerabilities:
        print(f"    Vulnerabilities:")
        for vuln in mech.vulnerabilities:
            print(f"      {vuln}")
```

### Hardware Interface Discovery

```python
from firmware_analysis_engine import HardwareInterfaceFinder

finder = HardwareInterfaceFinder()
interfaces = finder.discover("/tmp/firmware_fs")

print("Hardware Interfaces:")
for iface in interfaces:
    print(f"\n  {iface.interface_type} ({iface.name})")
    print(f"    Address: 0x{iface.address:08x}" if iface.address else "    Address: N/A")
    print(f"    GPIO pins: {iface.gpio_pins}")
    print(f"    Description: {iface.description}")
    if iface.debug_access:
        print(f"    DEBUG ACCESS AVAILABLE")
```

### Batch Firmware Analysis

```python
from firmware_analysis_engine import BatchFirmwareAnalyzer

batch = BatchFirmwareAnalyzer(max_workers=4)
reports = batch.analyze_directory("/path/to/firmware_images/")

print(f"Analyzed {len(reports)} firmware images:\n")
for report in reports:
    print(f"  {Path(report.path).name}:")
    print(f"    Format: {report.format}")
    print(f"    Architecture: {report.architecture}")
    print(f"    Credentials: {len(report.credentials)}")
    print(f"    Vulnerabilities: {len(report.vulnerabilities)}")
    print()
```

## Best Practices

### 1. Work on Copies, Not Originals
Always work on copies of firmware images. Firmware extraction and modification processes can corrupt the image. Maintain the original image with its cryptographic hash for reference and evidence preservation.

### 2. Verify Image Integrity Before Analysis
Before analysis, verify firmware image integrity using embedded checksums (CRC32, MD5, SHA-256) or known-good references. Corrupted images produce misleading analysis results. If checksums don't match, attempt error correction or obtain a fresh copy.

### 3. Identify the Target Platform Early
Understanding the target hardware (CPU architecture, endianness, board type, peripherals) is essential for accurate analysis. Use binwalk, file, and readelf to identify the platform before deep analysis. Wrong architecture assumptions lead to incorrect disassembly and misinterpreted data.

### 4. Extract and Analyze Configuration Separately
Configuration files often contain the most immediately useful information: default credentials, network settings, cloud endpoints, API keys, and administrative URLs. Extract and analyze these before diving into binary analysis.

### 5. Be Aware of Anti-Analysis Techniques
Some firmware employs anti-tampering mechanisms: signed firmware images, encrypted filesystems, secure boot chains, and integrity verification. These must be identified and handled appropriately — bypassing secure boot requires hardware-level access in most cases.

### 6. Consider the Complete Attack Surface
Firmware security extends beyond the firmware image itself: update mechanisms, web interfaces, serial ports, Bluetooth/Zigbee/Z-Wave, cloud APIs, and mobile applications. Analyze the firmware in the context of the device's complete attack surface.

### 7. Document Hardware Connections
If you have physical access to the device, document all hardware connections, test points, debug headers (UART, JTAG), and chip markings before disassembly. Photograph everything. Hardware details are essential for firmware extraction from flash chips and for understanding hardware-firmware interactions.

### 8. Cross-Reference Against Known Vulnerabilities
Check extracted software versions (Linux kernel, BusyBox, OpenSSL, lighttpd, etc.) against known CVE databases. Outdated embedded software is extremely common in IoT devices and represents a significant portion of discovered vulnerabilities.

## Related Modules

| Module | Relationship |
|--------|-------------|
| `binary-analysis` | Firmware contains binaries that require the same analysis techniques |
| `malware-analysis` | Firmware may contain malware, rootkits, or backdoors requiring malware analysis |
| `decompilation` | Firmware executables require decompilation to recover source-level logic |
| `protocol-analysis` | Firmware implements network protocols that require protocol analysis |
| `web2-recon` | Firmware web interfaces and cloud APIs extend into the web attack surface |

## Firmware Extraction Deep Dive

### Binwalk-Based Extraction Pipeline

Automated firmware extraction using binwalk with post-processing for filesystem analysis.

```python
import subprocess
import os
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ExtractionResult:
    """Result of firmware extraction operation."""
    source_path: str
    output_dir: str
    filesystem_type: str
    architecture: str
    total_files: int
    total_size: int
    extraction_method: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class FirmwareExtractor:
    """Automated firmware extraction using binwalk and friends."""

    MAGIC_SIGNATURES = {
        b'hsqs': 'squashfs_lzma',
        b'sqsh': 'squashfs',
        b'UBI#': 'ubifs',
        b'\x85\x19\x03\x00': 'jffs2_little_endian',
        b'\x03\x01\x19\x85': 'jffs2_big_endian',
        b'CRC\x1a\x02': 'jffs2',
        b'-rom1fs-': 'romfs',
        b'\x19\x85': 'jffs2',
        b'UBI1': 'ubi',
        b'UBI2': 'ubi',
        b'\x7fELF': 'elf',
        b'MZ': 'pe',
    }

    def __init__(self, binwalk_path: str = 'binwalk'):
        self.binwalk_path = binwalk_path
        self.results: List[ExtractionResult] = []

    def scan_firmware(self, firmware_path: str) -> dict:
        """Scan firmware without extraction to identify embedded components."""
        cmd = [self.binwalk_path, '-M', '--json', firmware_path]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

        # Fallback: manual signature scan
        return self._manual_scan(firmware_path)

    def _manual_scan(self, firmware_path: str) -> dict:
        """Manual scan using magic byte signatures."""
        data = Path(firmware_path).read_bytes()
        findings = []

        for offset in range(0, min(len(data), 10 * 1024 * 1024)):
            for magic, fs_type in self.MAGIC_SIGNATURES.items():
                if data[offset:offset+len(magic)] == magic:
                    findings.append({
                        'offset': hex(offset),
                        'description': fs_type,
                        'magic': magic.hex(),
                    })

        return {'files': [{'path': firmware_path, 'signatures': findings}]}

    def extract(self, firmware_path: str, output_dir: str = None) -> ExtractionResult:
        """Extract firmware image to a directory."""
        if output_dir is None:
            output_dir = f"/tmp/firmware_extracted/{Path(firmware_path).stem}"

        os.makedirs(output_dir, exist_ok=True)

        # Calculate hash before extraction
        firmware_data = Path(firmware_path).read_bytes()
        sha256 = hashlib.sha256(firmware_data).hexdigest()

        # Run binwalk extraction
        cmd = [
            self.binwalk_path, '-e', '-C', output_dir,
            '--unsquash', firmware_path
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=600
            )
        except subprocess.TimeoutExpired:
            return ExtractionResult(
                source_path=firmware_path,
                output_dir=output_dir,
                filesystem_type='unknown',
                architecture='unknown',
                total_files=0,
                total_size=0,
                extraction_method='binwalk_timeout',
                errors=['Extraction timed out after 600 seconds'],
            )

        # Post-process extraction
        extracted_path = self._find_extracted_root(output_dir)
        fs_type = self._identify_filesystem(extracted_path)
        arch = self._detect_architecture(extracted_path)
        files = self._count_files(extracted_path)
        total_size = self._calculate_total_size(extracted_path)

        extraction_result = ExtractionResult(
            source_path=firmware_path,
            output_dir=str(extracted_path),
            filesystem_type=fs_type,
            architecture=arch,
            total_files=files,
            total_size=total_size,
            extraction_method='binwalk',
        )

        self.results.append(extraction_result)
        return extraction_result

    def _find_extracted_root(self, output_dir: str) -> Path:
        """Find the root of extracted filesystem."""
        output_path = Path(output_dir)

        # Look for squashfs-root or similar
        for item in output_path.rglob('*'):
            if item.is_dir() and 'squashfs' in item.name:
                return item
            if item.is_dir() and item.name == 'root':
                return item

        # Return the output directory itself
        return output_path

    def _identify_filesystem(self, path: Path) -> str:
        """Identify the filesystem type of extracted content."""
        # Check for common filesystem indicators
        if (path / 'etc' / 'passwd').exists():
            if (path / 'proc').exists():
                return 'linux_rootfs'
            return 'linux'

        if (path / 'etc' / 'romfs').exists():
            return 'romfs'

        if (path / 'ubifs_root').exists():
            return 'ubifs'

        # Check for SquashFS characteristics
        for item in path.iterdir():
            if item.name.startswith('squashfs'):
                return 'squashfs'

        return 'unknown'

    def _detect_architecture(self, path: Path) -> str:
        """Detect the target architecture from extracted binaries."""
        # Look for ELF binaries and check their headers
        for elf_file in path.rglob('*'):
            if elf_file.is_file():
                try:
                    data = elf_file.read_bytes()[:20]
                    if data[:4] == b'\x7fELF':
                        ei_class = data[4]
                        ei_data = data[5]

                        if ei_class == 1:  # 32-bit
                            machine = int.from_bytes(data[18:20],
                                                   'little' if ei_data == 1 else 'big')
                            arch_map = {
                                3: 'x86',
                                40: 'ARM',
                                8: 'MIPS',
                                20: 'PowerPC',
                            }
                            return arch_map.get(machine, f'unknown_32bit_{machine}')
                        elif ei_class == 2:  # 64-bit
                            machine = int.from_bytes(data[18:20],
                                                   'little' if ei_data == 1 else 'big')
                            arch_map = {
                                62: 'x86_64',
                                183: 'AArch64',
                                8: 'MIPS64',
                            }
                            return arch_map.get(machine, f'unknown_64bit_{machine}')
                except (IOError, IndexError):
                    continue

        return 'unknown'

    def _count_files(self, path: Path) -> int:
        """Count total files in extracted filesystem."""
        count = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    count += 1
        except (PermissionError, OSError):
            pass
        return count

    def _calculate_total_size(self, path: Path) -> int:
        """Calculate total size of extracted filesystem."""
        total = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    total += item.stat().st_size
        except (PermissionError, OSError):
            pass
        return total

    def extract_by_offset(self, firmware_path: str, offset: int,
                           size: int = 0, output_dir: str = None) -> str:
        """Extract a specific region from firmware by offset."""
        if output_dir is None:
            output_dir = f"/tmp/firmware_extracted/region_{offset:x}"

        os.makedirs(output_dir, exist_ok=True)

        # Use dd to extract the region
        cmd = [
            'dd', f'if={firmware_path}',
            f'of={output_dir}/region.bin',
            f'bs=1', f'skip={offset}',
        ]
        if size > 0:
            cmd.append(f'count={size}')

        subprocess.run(cmd, capture_output=True)

        # Try to identify and extract the region
        region_path = f"{output_dir}/region.bin"
        extract_cmd = [
            self.binwalk_path, '-e', '-C', output_dir, region_path
        ]
        subprocess.run(extract_cmd, capture_output=True)

        return output_dir
```

### Filesystem Analysis

Deep analysis of extracted firmware filesystems for security assessment.

```python
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set
import re
import hashlib

@dataclass
class FilesystemAnalysis:
    """Comprehensive analysis of an extracted firmware filesystem."""
    root_path: str
    total_files: int
    total_directories: int
    total_size: int
    file_types: Dict[str, int]
    permissions_issues: List[dict]
    suspicious_files: List[dict]
    credential_files: List[dict]
    configuration_files: List[dict]
    startup_scripts: List[dict]
    network_config: List[dict]
    crypto_material: List[dict]
    debug_interfaces: List[dict]

class FilesystemAnalyzer:
    """Analyze extracted firmware filesystems."""

    CREDENTIAL_PATTERNS = [
        (re.compile(r'password\s*[:=]\s*(.+)', re.I), 'password'),
        (re.compile(r'secret\s*[:=]\s*(.+)', re.I), 'secret'),
        (re.compile(r'api[_-]?key\s*[:=]\s*(.+)', re.I), 'api_key'),
        (re.compile(r'token\s*[:=]\s*(.+)', re.I), 'token'),
        (re.compile(r'credentials?\s*[:=]\s*(.+)', re.I), 'credentials'),
    ]

    SUSPICIOUS_EXECUTABLE_PATTERNS = [
        'telnetd', 'dropbear', 'sshd', 'tftp',
        'busybox', 'wget', 'curl', 'nc', 'netcat',
        'python', 'perl', 'lua', 'php',
    ]

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)

    def full_analysis(self) -> FilesystemAnalysis:
        """Perform comprehensive filesystem analysis."""
        files = list(self.root_path.rglob('*'))

        return FilesystemAnalysis(
            root_path=str(self.root_path),
            total_files=sum(1 for f in files if f.is_file()),
            total_directories=sum(1 for f in files if f.is_dir()),
            total_size=sum(f.stat().st_size for f in files if f.is_file()),
            file_types=self._categorize_file_types(files),
            permissions_issues=self._check_permissions(files),
            suspicious_files=self._find_suspicious_files(files),
            credential_files=self._find_credentials(files),
            configuration_files=self._find_config_files(files),
            startup_scripts=self._find_startup_scripts(files),
            network_config=self._analyze_network_config(files),
            crypto_material=self._find_crypto_material(files),
            debug_interfaces=self._find_debug_interfaces(files),
        )

    def _categorize_file_types(self, files: List[Path]) -> Dict[str, int]:
        """Categorize files by type."""
        categories = {}
        for f in files:
            if f.is_file():
                ext = f.suffix.lower() or 'no_extension'
                categories[ext] = categories.get(ext, 0) + 1
        return dict(sorted(categories.items(), key=lambda x: -x[1]))

    def _check_permissions(self, files: List[Path]) -> List[dict]:
        """Check for permission-related security issues."""
        issues = []
        for f in files:
            if f.is_file():
                try:
                    stat = f.stat()
                    mode = stat.st_mode

                    # World-writable files
                    if mode & 0o002:
                        issues.append({
                            'type': 'world_writable',
                            'path': str(f.relative_to(self.root_path)),
                            'mode': oct(mode),
                        })

                    # Setuid/setgid binaries
                    if mode & 0o4000 or mode & 0o2000:
                        issues.append({
                            'type': 'setuid_setgid',
                            'path': str(f.relative_to(self.root_path)),
                            'mode': oct(mode),
                            'is_setuid': bool(mode & 0o4000),
                            'is_setgid': bool(mode & 0o2000),
                        })

                    # Executable with world-read
                    if mode & 0o111 and mode & 0o004:
                        issues.append({
                            'type': 'executable_world_readable',
                            'path': str(f.relative_to(self.root_path)),
                            'mode': oct(mode),
                        })

                except (PermissionError, OSError):
                    pass

        return issues

    def _find_suspicious_files(self, files: List[Path]) -> List[dict]:
        """Find files that may indicate backdoors or suspicious functionality."""
        suspicious = []
        for f in files:
            if f.is_file():
                name = f.name.lower()
                for pattern in self.SUSPICIOUS_EXECUTABLE_PATTERNS:
                    if pattern in name:
                        suspicious.append({
                            'type': 'suspicious_executable',
                            'path': str(f.relative_to(self.root_path)),
                            'name': f.name,
                            'size': f.stat().st_size,
                        })
                        break

                # Check for hidden files
                if f.name.startswith('.') and f.name != '.' and f.name != '..':
                    suspicious.append({
                        'type': 'hidden_file',
                        'path': str(f.relative_to(self.root_path)),
                        'name': f.name,
                    })

        return suspicious

    def _find_credentials(self, files: List[Path]) -> List[dict]:
        """Find hardcoded credentials in files."""
        credentials = []
        credential_files = ['passwd', 'shadow', 'wpa_supplicant.conf',
                           'hostapd.conf', '.htpasswd', 'credentials',
                           'secrets', '.ssh', 'id_rsa']

        for f in files:
            if f.is_file():
                # Check if filename matches known credential files
                if any(cf in f.name.lower() for cf in credential_files):
                    credentials.append({
                        'type': 'credential_file',
                        'path': str(f.relative_to(self.root_path)),
                        'name': f.name,
                        'size': f.stat().st_size,
                    })

                # Scan file contents for credential patterns
                try:
                    content = f.read_text(errors='ignore')[:10000]
                    for pattern, cred_type in self.CREDENTIAL_PATTERNS:
                        matches = pattern.findall(content)
                        for match in matches:
                            credentials.append({
                                'type': 'hardcoded_credential',
                                'path': str(f.relative_to(self.root_path)),
                                'credential_type': cred_type,
                                'context': match[:100],
                            })
                except (PermissionError, IOError):
                    pass

        return credentials

    def _find_config_files(self, files: List[Path]) -> List[dict]:
        """Find configuration files."""
        configs = []
        config_extensions = ['.conf', '.cfg', '.ini', '.json', '.xml',
                            '.yaml', '.yml', '.properties']

        for f in files:
            if f.is_file():
                if f.suffix.lower() in config_extensions:
                    configs.append({
                        'type': 'configuration_file',
                        'path': str(f.relative_to(self.root_path)),
                        'extension': f.suffix,
                        'size': f.stat().st_size,
                    })

        return configs

    def _find_startup_scripts(self, files: List[Path]) -> List[dict]:
        """Find startup and initialization scripts."""
        scripts = []
        startup_dirs = ['init.d', 'rc.d', 'systemd', 'startup', 'boot']

        for f in files:
            if f.is_file():
                # Check if in startup directory
                if any(sd in str(f.parent).lower() for sd in startup_dirs):
                    scripts.append({
                        'type': 'startup_script',
                        'path': str(f.relative_to(self.root_path)),
                        'name': f.name,
                    })

                # Check for common init script names
                if f.name in ['inittab', 'rcS', 'rc.local', 'S99startup']:
                    scripts.append({
                        'type': 'init_script',
                        'path': str(f.relative_to(self.root_path)),
                        'name': f.name,
                    })

        return scripts

    def _analyze_network_config(self, files: List[Path]) -> List[dict]:
        """Analyze network configuration files."""
        network_configs = []
        network_files = ['interfaces', 'resolv.conf', 'wpa_supplicant.conf',
                        'hostapd.conf', 'dhcpd.conf', 'dnsmasq.conf',
                        'iptables', 'firewall']

        for f in files:
            if f.is_file():
                if f.name.lower() in network_files:
                    network_configs.append({
                        'type': 'network_config',
                        'path': str(f.relative_to(self.root_path)),
                        'name': f.name,
                    })

        return network_configs

    def _find_crypto_material(self, files: List[Path]) -> List[dict]:
        """Find cryptographic material (keys, certificates)."""
        crypto = []
        crypto_patterns = [
            ('.pem', 'PEM certificate/key'),
            ('.key', 'private key'),
            ('.crt', 'certificate'),
            ('.cert', 'certificate'),
            ('.p12', 'PKCS12 bundle'),
            ('.pfx', 'PKCS12 bundle'),
            ('id_rsa', 'SSH private key'),
            ('id_dsa', 'SSH DSA key'),
            ('id_ecdsa', 'SSH ECDSA key'),
            ('id_ed25519', 'SSH Ed25519 key'),
        ]

        for f in files:
            if f.is_file():
                for pattern, desc in crypto_patterns:
                    if pattern in f.name:
                        crypto.append({
                            'type': desc,
                            'path': str(f.relative_to(self.root_path)),
                            'name': f.name,
                            'size': f.stat().st_size,
                        })
                        break

        return crypto

    def _find_debug_interfaces(self, files: List[Path]) -> List[dict]:
        """Find references to debug interfaces."""
        debug = []
        debug_indicators = ['uart', 'jtag', 'serial', 'console', 'debug',
                           'telnet', 'gdb', 'strace']

        for f in files:
            if f.is_file():
                name_lower = f.name.lower()
                for indicator in debug_indicators:
                    if indicator in name_lower:
                        debug.append({
                            'type': 'debug_interface_reference',
                            'path': str(f.relative_to(self.root_path)),
                            'name': f.name,
                            'indicator': indicator,
                        })
                        break

        return debug

    def generate_report(self, analysis: FilesystemAnalysis) -> str:
        """Generate a comprehensive filesystem analysis report."""
        lines = ['# Firmware Filesystem Analysis Report\n']

        lines.append('## Overview\n')
        lines.append(f'- Root path: {analysis.root_path}')
        lines.append(f'- Total files: {analysis.total_files}')
        lines.append(f'- Total directories: {analysis.total_directories}')
        lines.append(f'- Total size: {analysis.total_size / 1024:.1f} KB\n')

        lines.append('## File Type Distribution\n')
        for ext, count in sorted(analysis.file_types.items(), key=lambda x: -x[1])[:20]:
            lines.append(f'- {ext}: {count}')
        lines.append('')

        if analysis.permissions_issues:
            lines.append(f'## Permission Issues ({len(analysis.permissions_issues)})\n')
            for issue in analysis.permissions_issues[:20]:
                lines.append(f'- [{issue["type"]}] {issue["path"]} ({issue["mode"]})')
            lines.append('')

        if analysis.credential_files:
            lines.append(f'## Credentials Found ({len(analysis.credential_files)})\n')
            for cred in analysis.credential_files:
                lines.append(f'- [{cred["type"]}] {cred["path"]}')
            lines.append('')

        if analysis.suspicious_files:
            lines.append(f'## Suspicious Files ({len(analysis.suspicious_files)})\n')
            for sus in analysis.suspicious_files:
                lines.append(f'- [{sus["type"]}] {sus["path"]}')
            lines.append('')

        if analysis.crypto_material:
            lines.append(f'## Cryptographic Material ({len(analysis.crypto_material)})\n')
            for crypto in analysis.crypto_material:
                lines.append(f'- [{crypto["type"]}] {crypto["path"]}')
            lines.append('')

        if analysis.debug_interfaces:
            lines.append(f'## Debug Interfaces ({len(analysis.debug_interfaces)})\n')
            for dbg in analysis.debug_interfaces:
                lines.append(f'- [{dbg["indicator"]}] {dbg["path"]}')
            lines.append('')

        return '\n'.join(lines)
```

### QEMU Emulation for Firmware

Setting up QEMU-based emulation for dynamic firmware analysis.

```python
import subprocess
import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class EmulationConfig:
    """QEMU emulation configuration for firmware."""
    firmware_path: str
    extracted_fs: str
    architecture: str
    endianness: str  # 'little' or 'big'
    kernel_path: Optional[str] = None
    rootfs_path: Optional[str] = None
    qemu_binary: str = ''
    network_config: str = 'user'  # user, tap, none
    port_mapping: Dict[int, int] = field(default_factory=dict)
    memory_mb: int = 256
    extra_args: List[str] = field(default_factory=list)

class QEMUEmulator:
    """Manage QEMU-based firmware emulation."""

    ARCH_BINARY_MAP = {
        'mips': {
            'little': 'qemu-mipsel',
            'big': 'qemu-mips',
        },
        'mips64': {
            'little': 'qemu-mips64el',
            'big': 'qemu-mips64',
        },
        'arm': {
            'little': 'qemu-arm',
            'big': 'qemu-armeb',
        },
        'arm64': {
            'little': 'qemu-aarch64',
            'big': 'qemu-aarch64_be',
        },
        'x86': {
            'little': 'qemu-i386',
        },
        'x86_64': {
            'little': 'qemu-x86_64',
        },
        'powerpc': {
            'big': 'qemu-ppc',
        },
    }

    def __init__(self):
        self.configs: Dict[str, EmulationConfig] = {}

    def setup_emulation(self, firmware_path: str, extracted_fs: str,
                        arch: str, endianness: str = 'little') -> EmulationConfig:
        """Set up QEMU emulation for a firmware image."""
        qemu_binary = self.ARCH_BINARY_MAP.get(arch, {}).get(endianness, '')

        config = EmulationConfig(
            firmware_path=firmware_path,
            extracted_fs=extracted_fs,
            architecture=arch,
            endianness=endianness,
            qemu_binary=qemu_binary,
            network_config='user',
            port_mapping={8080: 80, 2222: 22},
        )

        # Find kernel if available
        config.kernel_path = self._find_kernel(extracted_fs, arch)

        # Find rootfs
        config.rootfs_path = self._find_rootfs(extracted_fs)

        self.configs[firmware_path] = config
        return config

    def _find_kernel(self, extracted_fs: str, arch: str) -> Optional[str]:
        """Find a kernel image in extracted filesystem."""
        root = Path(extracted_fs)

        kernel_patterns = ['vmlinuz', 'vmlinux', 'zImage', 'uImage', 'bzImage']
        for pattern in kernel_patterns:
            for kernel in root.rglob(f'*{pattern}*'):
                if kernel.is_file():
                    return str(kernel)

        # Check boot directory
        boot_dir = root / 'boot'
        if boot_dir.exists():
            for f in boot_dir.iterdir():
                if f.is_file() and ('vmlinux' in f.name or 'zImage' in f.name):
                    return str(f)

        return None

    def _find_rootfs(self, extracted_fs: str) -> Optional[str]:
        """Find root filesystem image."""
        root = Path(extracted_fs)

        # Look for squashfs images
        for fs in root.rglob('*squashfs*'):
            if fs.is_file():
                return str(fs)

        # Look for ext2/ext3/ext4 images
        for fs in root.rglob('*.img'):
            if fs.is_file():
                return str(fs)

        # Use the extracted directory itself
        return extracted_fs

    def build_startup_command(self, config: EmulationConfig) -> str:
        """Build QEMU startup command."""
        if not config.qemu_binary:
            return f"# No QEMU binary found for {config.architecture}_{config.endianness}"

        cmd_parts = [config.qemu_binary]

        # Memory
        cmd_parts.extend(['-m', str(config.memory_mb)])

        # Kernel
        if config.kernel_path:
            cmd_parts.extend(['-kernel', config.kernel_path])

        # Root filesystem
        if config.rootfs_path:
            if config.rootfs_path.endswith(('.img', '.bin')):
                cmd_parts.extend(['-drive', f'file={config.rootfs_path},if=sd,format=raw'])
            else:
                # Directory-based rootfs — use initrd or 9p
                cmd_parts.extend(['-initrd', config.rootfs_path])

        # Network
        if config.network_config == 'user':
            cmd_parts.append('-netdev')
            netdev = 'user,id=net0'
            for host_port, guest_port in config.port_mapping.items():
                netdev += f',hostfwd=tcp::{host_port}-:{guest_port}'
            cmd_parts.append(netdev)
            cmd_parts.extend(['-device', 'virtio-net,netdev=net0'])
        elif config.network_config == 'none':
            cmd_parts.append('-net')
            cmd_parts.append('none')

        # Extra arguments
        cmd_parts.extend(config.extra_args)

        # Console
        cmd_parts.extend(['-nographic', '-serial', 'mon:stdio'])

        return ' '.join(cmd_parts)

    def generate_docker_compose(self, config: EmulationConfig) -> str:
        """Generate docker-compose.yml for containerized emulation."""
        compose = {
            'version': '3',
            'services': {
                'firmware': {
                    'image': f'firmadyne/{config.architecture}',
                    'command': self.build_startup_command(config),
                    'ports': [
                        f'{host}:{guest}'
                        for host, guest in config.port_mapping.items()
                    ],
                    'volumes': [
                        f'{config.extracted_fs}:/firmware:ro',
                    ],
                    'network_mode': 'bridge',
                    'cap_add': ['NET_ADMIN'],
                    'devices': ['/dev/net/tun:/dev/net/tun'],
                }
            }
        }

        import yaml
        return yaml.dump(compose, default_flow_style=False)

    def monitor_emulation(self, config: EmulationConfig, timeout: int = 60) -> dict:
        """Monitor emulation for observable behavior."""
        # This would typically involve:
        # 1. Starting QEMU in background
        # 2. Capturing serial console output
        # 3. Monitoring network traffic
        # 4. Taking periodic screenshots (if display available)

        return {
            'status': 'monitoring_started',
            'config': {
                'architecture': config.architecture,
                'qemu_binary': config.qemu_binary,
                'ports': config.port_mapping,
            },
            'monitoring_capabilities': [
                'serial_console',
                'network_capture',
                'process_list',
                'file_system_changes',
            ]
        }
```

### Hardware Interface Discovery

Identifying and documenting hardware interfaces in firmware for physical security assessment.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path
import re

@dataclass
class HardwareInterface:
    """Detected hardware interface."""
    interface_type: str  # UART, JTAG, SPI, I2C, GPIO, etc.
    name: str
    address: Optional[int] = None
    pins: List[int] = field(default_factory=list)
    baud_rate: Optional[int] = None
    description: str = ''
    confidence: float = 0.0
    source: str = ''  # Device tree, config file, binary analysis

class HardwareInterfaceFinder:
    """Discover hardware interfaces from firmware analysis."""

    # Device tree compatible strings for known interfaces
    UART_COMPATIBLE = [
        'ns16550', 'ns16550a', 'pl011', 'max3100',
        'serial8250', 'earlycon', 'console',
    ]

    JTAG_COMPATIBLE = [
        'jtag', 'arm,jtag', 'boundary-scan',
    ]

    SPI_COMPATIBLE = [
        'spi', 'spi-gpio', 'spi-master', 'spi-slave',
    ]

    I2C_COMPATIBLE = [
        'i2c', 'i2c-gpio', 'i2c-master', 'i2c-slave',
    ]

    def __init__(self, firmware_root: str):
        self.root = Path(firmware_root)
        self.interfaces: List[HardwareInterface] = []

    def discover_all(self) -> List[HardwareInterface]:
        """Discover all hardware interfaces."""
        self.interfaces = []

        # Check device tree blobs
        self._scan_device_trees()

        # Check kernel configuration
        self._scan_kernel_config()

        # Check boot logs / configuration
        self._scan_boot_config()

        # Check binary strings
        self._scan_binary_strings()

        return self.interfaces

    def _scan_device_trees(self):
        """Scan device tree files for hardware interfaces."""
        for dtb in self.root.rglob('*.dtb'):
            # Parse device tree binary (simplified)
            try:
                data = dtb.read_bytes()
                # Look for compatible strings
                for compat in self.UART_COMPATIBLE:
                    if compat.encode() in data:
                        self.interfaces.append(HardwareInterface(
                            interface_type='UART',
                            name=compat,
                            description=f'UART interface detected in {dtb.name}',
                            confidence=0.8,
                            source='device_tree',
                        ))

                for compat in self.JTAG_COMPATIBLE:
                    if compat.encode() in data:
                        self.interfaces.append(HardwareInterface(
                            interface_type='JTAG',
                            name=compat,
                            description=f'JTAG interface detected in {dtb.name}',
                            confidence=0.8,
                            source='device_tree',
                        ))

                for compat in self.SPI_COMPATIBLE:
                    if compat.encode() in data:
                        self.interfaces.append(HardwareInterface(
                            interface_type='SPI',
                            name=compat,
                            description=f'SPI interface detected in {dtb.name}',
                            confidence=0.8,
                            source='device_tree',
                        ))

                for compat in self.I2C_COMPATIBLE:
                    if compat.encode() in data:
                        self.interfaces.append(HardwareInterface(
                            interface_type='I2C',
                            name=compat,
                            description=f'I2C interface detected in {dtb.name}',
                            confidence=0.8,
                            source='device_tree',
                        ))
            except (IOError, OSError):
                continue

    def _scan_kernel_config(self):
        """Scan kernel configuration for enabled interfaces."""
        config_files = [
            self.root / 'boot' / 'config',
            self.root / '.config',
            self.root / 'config.gz',
        ]

        for config_path in config_files:
            if config_path.exists():
                try:
                    if config_path.suffix == '.gz':
                        import gzip
                        content = gzip.decompress(config_path.read_bytes()).decode('utf-8', errors='ignore')
                    else:
                        content = config_path.read_text(errors='ignore')

                    # Check for UART
                    if 'CONFIG_SERIAL_8250=y' in content:
                        self.interfaces.append(HardwareInterface(
                            interface_type='UART',
                            name='8250/16550',
                            description='8250/16550 UART enabled in kernel',
                            confidence=0.9,
                            source='kernel_config',
                        ))

                    if 'CONFIG_SERIAL_PL011=y' in content:
                        self.interfaces.append(HardwareInterface(
                            interface_type='UART',
                            name='PL011',
                            description='ARM PL011 UART enabled',
                            confidence=0.9,
                            source='kernel_config',
                        ))

                    # Check for JTAG
                    if 'CONFIG_JTAG=y' in content:
                        self.interfaces.append(HardwareInterface(
                            interface_type='JTAG',
                            name='JTAG',
                            description='JTAG support enabled in kernel',
                            confidence=0.9,
                            source='kernel_config',
                        ))

                    # Check for SPI
                    if 'CONFIG_SPI=y' in content:
                        self.interfaces.append(HardwareInterface(
                            interface_type='SPI',
                            name='SPI',
                            description='SPI support enabled',
                            confidence=0.9,
                            source='kernel_config',
                        ))

                    # Check for I2C
                    if 'CONFIG_I2C=y' in content:
                        self.interfaces.append(HardwareInterface(
                            interface_type='I2C',
                            name='I2C',
                            description='I2C support enabled',
                            confidence=0.9,
                            source='kernel_config',
                        ))

                except (IOError, OSError):
                    continue

    def _scan_boot_config(self):
        """Scan boot configuration for console/UART settings."""
        boot_files = ['bootargs', 'u-boot.env', 'env.txt', 'boot.config']

        for boot_file in boot_files:
            for f in self.root.rglob(boot_file):
                try:
                    content = f.read_text(errors='ignore')

                    # Look for console settings
                    console_match = re.search(
                        r'console\s*=\s*(\w+),(\d+)', content
                    )
                    if console_match:
                        self.interfaces.append(HardwareInterface(
                            interface_type='UART',
                            name=console_match.group(1),
                            baud_rate=int(console_match.group(2)),
                            description=f'Console UART: {console_match.group(1)} @ {console_match.group(2)} baud',
                            confidence=0.95,
                            source='boot_config',
                        ))

                except (IOError, OSError):
                    continue

    def _scan_binary_strings(self):
        """Scan binary strings for hardware interface references."""
        interface_patterns = [
            (re.compile(r'/dev/ttyS\d+'), 'UART', 'Serial device node'),
            (re.compile(r'/dev/ttyUSB\d+'), 'USB-UART', 'USB serial adapter'),
            (re.compile(r'/dev/jtag\d*'), 'JTAG', 'JTAG device node'),
            (re.compile(r'/dev/spidev\d+'), 'SPI', 'SPI device node'),
            (re.compile(r'/dev/i2c-\d+'), 'I2C', 'I2C device node'),
            (re.compile(r'/dev/gpio\d+'), 'GPIO', 'GPIO device node'),
        ]

        for binary in self.root.rglob('*'):
            if binary.is_file() and binary.stat().st_size < 10 * 1024 * 1024:
                try:
                    content = binary.read_bytes()
                    for pattern, iface_type, desc in interface_patterns:
                        matches = pattern.findall(content.decode('ascii', errors='ignore'))
                        for match in matches:
                            self.interfaces.append(HardwareInterface(
                                interface_type=iface_type,
                                name=match,
                                description=desc,
                                confidence=0.6,
                                source='binary_strings',
                            ))
                except (IOError, OSError):
                    continue

    def generate_hardware_map(self) -> str:
        """Generate a hardware interface map document."""
        lines = ['# Hardware Interface Map\n']

        # Group by type
        by_type = {}
        for iface in self.interfaces:
            if iface.interface_type not in by_type:
                by_type[iface.interface_type] = []
            by_type[iface.interface_type].append(iface)

        for iface_type, ifaces in sorted(by_type.items()):
            lines.append(f'## {iface_type} Interfaces\n')
            for iface in ifaces:
                lines.append(f'### {iface.name}')
                lines.append(f'- Type: {iface.interface_type}')
                lines.append(f'- Description: {iface.description}')
                if iface.address:
                    lines.append(f'- Address: 0x{iface.address:08x}')
                if iface.baud_rate:
                    lines.append(f'- Baud Rate: {iface.baud_rate}')
                lines.append(f'- Confidence: {iface.confidence:.0%}')
                lines.append(f'- Source: {iface.source}\n')

        return '\n'.join(lines)
```

### Bootloader Analysis

Analyzing bootloader configurations for firmware modification and security assessment.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path
import re

@dataclass
class BootloaderConfig:
    """Parsed bootloader configuration."""
    bootloader_type: str  # U-Boot, GRUB, Barebox, etc.
    version: str
    environment: Dict[str, str]
    boot_args: str
    kernel_load_address: str
    rootfs_device: str
    console_settings: str
    network_boot: bool
    security_features: List[str]
    debug_enabled: bool

class BootloaderAnalyzer:
    """Analyze bootloader configuration and security."""

    UBOOT_ENV_PATTERNS = [
        (re.compile(r'bootcmd\s*=\s*(.+)'), 'bootcmd'),
        (re.compile(r'bootargs\s*=\s*(.+)'), 'bootargs'),
        (re.compile(r'bootdelay\s*=\s*(\d+)'), 'bootdelay'),
        (re.compile(r'baudrate\s*=\s*(\d+)'), 'baudrate'),
        (re.compile(r'ipaddr\s*=\s*(.+)'), 'ipaddr'),
        (re.compile(r'serverip\s*=\s*(.+)'), 'serverip'),
        (re.compile(r'autoload\s*=\s*(\w+)'), 'autoload'),
        (re.compile(r'autoboot\s*=\s*(\w+)'), 'autoboot'),
    ]

    SECURITY_INDICATORS = {
        'secure_boot': ['secure', 'verified', 'signed', 'auth'],
        'password_protected': ['password', 'pass=', 'passwd'],
        'encryption': ['encrypt', 'decrypt', 'aes', 'tpm'],
        'disabled_debug': ['nodbg', 'quiet'],
        'read_only_rootfs': ['ro', 'read_only'],
    }

    def __init__(self, firmware_root: str):
        self.root = Path(firmware_root)

    def analyze_uboot(self) -> Optional[BootloaderConfig]:
        """Analyze U-Boot bootloader configuration."""
        env_files = list(self.root.rglob('u-boot.env')) + \
                   list(self.root.rglob('u_env.txt')) + \
                   list(self.root.rglob('env.txt'))

        if not env_files:
            return None

        env_content = ''
        for env_file in env_files:
            try:
                env_content = env_file.read_text(errors='ignore')
                break
            except (IOError, OSError):
                continue

        if not env_content:
            return None

        # Parse environment variables
        environment = {}
        for line in env_content.splitlines():
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, _, value = line.partition('=')
                environment[key.strip()] = value.strip()

        # Analyze boot arguments
        boot_args = environment.get('bootargs', '')
        console_match = re.search(r'console=(\w+),(\d+)', boot_args)

        # Detect security features
        security = []
        for feature, indicators in self.SECURITY_INDICATORS.items():
            if any(ind in env_content.lower() for ind in indicators):
                security.append(feature)

        # Check for debug mode
        debug_enabled = 'debug' in boot_args.lower() or 'loglevel' in boot_args.lower()

        return BootloaderConfig(
            bootloader_type='U-Boot',
            version=environment.get('ver', 'unknown'),
            environment=environment,
            boot_args=boot_args,
            kernel_load_address=environment.get('loadaddr', 'unknown'),
            rootfs_device=self._extract_rootfs_device(boot_args),
            console_settings=f'{console_match.group(1)},{console_match.group(2)}' if console_match else 'unknown',
            network_boot='nfs' in boot_args.lower() or 'tftp' in boot_args.lower(),
            security_features=security,
            debug_enabled=debug_enabled,
        )

    def _extract_rootfs_device(self, boot_args: str) -> str:
        """Extract root filesystem device from boot arguments."""
        root_match = re.search(r'root=(\S+)', boot_args)
        return root_match.group(1) if root_match else 'unknown'

    def analyze_barebox(self) -> Optional[BootloaderConfig]:
        """Analyze Barebox bootloader configuration."""
        barebox_files = list(self.root.rglob('barebox.env'))
        if not barebox_files:
            return None

        env_content = ''
        for f in barebox_files:
            try:
                env_content = f.read_text(errors='ignore')
                break
            except (IOError, OSError):
                continue

        environment = {}
        for line in env_content.splitlines():
            if '=' in line and not line.startswith('#'):
                key, _, value = line.partition('=')
                environment[key.strip()] = value.strip()

        return BootloaderConfig(
            bootloader_type='Barebox',
            version=environment.get('version', 'unknown'),
            environment=environment,
            boot_args=environment.get('bootargs', ''),
            kernel_load_address=environment.get('kernel_addr', 'unknown'),
            rootfs_device=self._extract_rootfs_device(environment.get('bootargs', '')),
            console_settings=environment.get('console', 'unknown'),
            network_boot='nfs' in environment.get('bootargs', '').lower(),
            security_features=[],
            debug_enabled='debug' in environment.get('bootargs', '').lower(),
        )

    def check_boot_security(self, config: BootloaderConfig) -> List[dict]:
        """Check bootloader security configuration."""
        findings = []

        # Check for password protection
        if 'password_protected' not in config.security_features:
            findings.append({
                'type': 'no_boot_password',
                'severity': 'medium',
                'description': 'Bootloader has no password protection',
                'recommendation': 'Set a bootloader password to prevent unauthorized boot modifications',
            })

        # Check for secure boot
        if 'secure_boot' not in config.security_features:
            findings.append({
                'type': 'no_secure_boot',
                'severity': 'high',
                'description': 'Secure boot is not enabled',
                'recommendation': 'Enable secure boot to verify kernel and rootfs integrity',
            })

        # Check for debug mode
        if config.debug_enabled:
            findings.append({
                'type': 'debug_enabled',
                'severity': 'medium',
                'description': 'Bootloader debug mode is enabled',
                'recommendation': 'Disable debug mode in production firmware',
            })

        # Check for network boot
        if config.network_boot:
            findings.append({
                'type': 'network_boot_enabled',
                'severity': 'high',
                'description': 'Network boot (NFS/TFTP) is enabled',
                'recommendation': 'Disable network boot unless required, as it can be used for unauthorized firmware loading',
            })

        # Check for console settings
        if config.console_settings != 'unknown':
            findings.append({
                'type': 'console_accessible',
                'severity': 'info',
                'description': f'Serial console enabled: {config.console_settings}',
                'recommendation': 'Ensure physical access to console is restricted',
            })

        # Check boot delay
        boot_delay = config.environment.get('bootdelay', '0')
        if boot_delay and boot_delay != '0':
            findings.append({
                'type': 'boot_delay_present',
                'severity': 'info',
                'description': f'Boot delay is {boot_delay} seconds',
                'recommendation': 'Set bootdelay to 0 to prevent interactive boot access',
            })

        return findings

    def generate_report(self, config: BootloaderConfig) -> str:
        """Generate bootloader analysis report."""
        lines = [f'# {config.bootloader_type} Analysis Report\n']

        lines.append('## Configuration\n')
        lines.append(f'- Version: {config.version}')
        lines.append(f'- Boot Arguments: {config.boot_args}')
        lines.append(f'- Kernel Load Address: {config.kernel_load_address}')
        lines.append(f'- Root Filesystem: {config.rootfs_device}')
        lines.append(f'- Console: {config.console_settings}')
        lines.append(f'- Network Boot: {"Enabled" if config.network_boot else "Disabled"}')
        lines.append(f'- Debug Mode: {"Enabled" if config.debug_enabled else "Disabled"}')
        lines.append(f'- Security Features: {", ".join(config.security_features) or "None"}\n')

        lines.append('## Environment Variables\n')
        for key, value in sorted(config.environment.items()):
            lines.append(f'- {key}={value}')
        lines.append('')

        security_findings = self.check_boot_security(config)
        if security_findings:
            lines.append('## Security Findings\n')
            for finding in security_findings:
                lines.append(f'### [{finding["severity"].upper()}] {finding["type"]}')
                lines.append(f'- Description: {finding["description"]}')
                lines.append(f'- Recommendation: {finding["recommendation"]}\n')

        return '\n'.join(lines)
```

### Firmware Modification and Repackaging

Modifying and repackaging firmware for authorized security testing.

```python
import subprocess
import hashlib
import os
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class FirmwareModResult:
    """Result of a firmware modification operation."""
    original_path: str
    modified_path: str
    original_hash: str
    modified_hash: str
    changes: list
    success: bool
    errors: list

class FirmwareModifier:
    """Modify and repackage firmware images."""

    def __init__(self, work_dir: str = '/tmp/firmware_work'):
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def unpack(self, firmware_path: str, output_dir: str = None) -> str:
        """Unpack firmware for modification."""
        if output_dir is None:
            output_dir = str(self.work_dir / Path(firmware_path).stem)

        os.makedirs(output_dir, exist_ok=True)

        # Use binwalk to extract
        cmd = ['binwalk', '-e', '-C', output_dir, firmware_path]
        subprocess.run(cmd, capture_output=True, timeout=300)

        return output_dir

    def modify_binary(self, binary_path: str, offset: int,
                      new_bytes: bytes) -> bool:
        """Modify bytes in a binary file."""
        try:
            data = bytearray(Path(binary_path).read_bytes())
            if offset + len(new_bytes) > len(data):
                return False
            data[offset:offset+len(new_bytes)] = new_bytes
            Path(binary_path).write_bytes(bytes(data))
            return True
        except (IOError, OSError):
            return False

    def replace_file(self, extracted_fs: str, relative_path: str,
                     new_content: bytes) -> bool:
        """Replace a file in the extracted filesystem."""
        target = Path(extracted_fs) / relative_path
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(new_content)
            return True
        except (IOError, OSError):
            return False

    def add_startup_script(self, extracted_fs: str, script_name: str,
                           script_content: str, priority: int = 99) -> bool:
        """Add a startup script to the firmware."""
        # Determine init system
        init_d = Path(extracted_fs) / 'etc' / 'init.d'
        if init_d.exists():
            script_path = init_d / f'S{priority:02d}{script_name}'
        else:
            # Create init.d if it doesn't exist
            init_d.mkdir(parents=True, exist_ok=True)
            script_path = init_d / f'S{priority:02d}{script_name}'

        try:
            script_path.write_text(f'#!/bin/sh\n{script_content}\n')
            os.chmod(script_path, 0o755)
            return True
        except (IOError, OSError):
            return False

    def inject_webshell(self, extracted_fs: str, web_root: str = 'www',
                        shell_name: str = 'shell.php') -> bool:
        """Inject a web shell for authorized testing."""
        web_path = Path(extracted_fs) / web_root / shell_name
        try:
            web_path.parent.mkdir(parents=True, exist_ok=True)
            # Minimal test shell for authorized security testing
            shell_content = '<?php echo "test"; ?>'
            web_path.write_text(shell_content)
            return True
        except (IOError, OSError):
            return False

    def repackage_squashfs(self, extracted_dir: str,
                           output_path: str) -> bool:
        """Repackage a SquashFS filesystem."""
        cmd = [
            'mksquashfs', extracted_dir, output_path,
            '-comp', 'xz', '-b', '131072',
            '-no-xattrs', '-noappend',
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=600)
        return result.returncode == 0

    def calculate_checksums(self, firmware_path: str) -> dict:
        """Calculate cryptographic checksums of firmware."""
        data = Path(firmware_path).read_bytes()
        return {
            'md5': hashlib.md5(data).hexdigest(),
            'sha1': hashlib.sha1(data).hexdigest(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'size': len(data),
        }

    def generate_modification_report(self, original: str, modified: str,
                                      changes: list) -> str:
        """Generate a report of firmware modifications."""
        orig_hashes = self.calculate_checksums(original)
        mod_hashes = self.calculate_checksums(modified)

        lines = ['# Firmware Modification Report\n']

        lines.append('## Original Firmware\n')
        lines.append(f'- Path: {original}')
        lines.append(f'- MD5: {orig_hashes["md5"]}')
        lines.append(f'- SHA256: {orig_hashes["sha256"]}')
        lines.append(f'- Size: {orig_hashes["size"]} bytes\n')

        lines.append('## Modified Firmware\n')
        lines.append(f'- Path: {modified}')
        lines.append(f'- MD5: {mod_hashes["md5"]}')
        lines.append(f'- SHA256: {mod_hashes["sha256"]}')
        lines.append(f'- Size: {mod_hashes["size"]} bytes\n')

        lines.append('## Changes Applied\n')
        for i, change in enumerate(changes, 1):
            lines.append(f'{i}. {change}')
        lines.append('')

        return '\n'.join(lines)
```
