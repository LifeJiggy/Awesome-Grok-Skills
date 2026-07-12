"""
IoT Security Module
IoT device security, firmware protection, and secure communication
"""

from __future__ import annotations

import hashlib
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AuthMethod(Enum):
    PSK = "psk"
    X509 = "x509_certificate"
    TPM = "tpm"
    SECURE_ELEMENT = "secure_element"

class VulnerabilitySeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BootStage(Enum):
    BOOTLOADER = "bootloader"
    FIRMWARE = "firmware"
    CONFIG = "config"
    APPLICATION = "application"

@dataclass
class BootChain:
    stages: List[Dict[str, str]] = field(default_factory=list)

@dataclass
class BootValidationResult:
    is_valid: bool = True
    stages_verified: int = 0
    stages_failed: int = 0
    failed_stages: List[str] = field(default_factory=list)

@dataclass
class SecureBootManager:
    hardware_root_of_trust: str = "tpm2.0"
    secure_boot_enabled: bool = True

    def validate_boot_chain(self, chain: BootChain) -> BootValidationResult:
        verified = 0
        failed = 0
        failed_stages = []
        for stage in chain.stages:
            if stage.get("signature") == "verified":
                verified += 1
            else:
                failed += 1
                failed_stages.append(stage.get("stage", "unknown"))
        return BootValidationResult(is_valid=failed == 0, stages_verified=verified, stages_failed=failed, failed_stages=failed_stages)

@dataclass
class Certificate:
    subject: str = ""
    issuer: str = ""
    not_before: datetime = field(default_factory=datetime.utcnow)
    not_after: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=365))
    fingerprint: str = ""
    key_size: int = 2048
    serial_number: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class DeviceAuthenticator:
    auth_method: AuthMethod = AuthMethod.X509
    ca_cert_path: str = ""

    def generate_certificate(self, device_id: str, validity_days: int = 365, key_size: int = 2048) -> Certificate:
        fingerprint = hashlib.sha256(device_id.encode()).hexdigest()[:32]
        return Certificate(subject=f"CN={device_id}", issuer="CN=IoT-CA", not_after=datetime.utcnow() + timedelta(days=validity_days), fingerprint=fingerprint, key_size=key_size)

    def validate_certificate(self, cert: Certificate) -> bool:
        return cert.not_after > datetime.utcnow()

@dataclass
class Vulnerability:
    cve_id: str = ""
    description: str = ""
    severity: VulnerabilitySeverity = VulnerabilitySeverity.LOW
    affected_component: str = ""
    cvss_score: float = 0.0
    remediation: str = ""

@dataclass
class ScanResult:
    firmware_path: str = ""
    vulnerability_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    scanned_at: datetime = field(default_factory=datetime.utcnow)

class FirmwareScanner:
    def __init__(self, vulnerability_db: str = "nvd") -> None:
        self.vulnerability_db = vulnerability_db
        self._known_vulns = [
            Vulnerability(cve_id="CVE-2024-0001", description="Buffer overflow in TLS parser", severity=VulnerabilitySeverity.CRITICAL, cvss_score=9.8),
            Vulnerability(cve_id="CVE-2024-0002", description="Weak default credentials", severity=VulnerabilitySeverity.HIGH, cvss_score=7.5),
        ]

    def scan_firmware(self, firmware_path: str) -> ScanResult:
        vulns = self._known_vulns[:2]
        return ScanResult(firmware_path=firmware_path, vulnerability_count=len(vulns), critical_count=1, high_count=1, vulnerabilities=vulns)

@dataclass
class SecurityProfile:
    name: str = ""
    rules: List[str] = field(default_factory=list)

@dataclass
class HardeningResult:
    rules_applied: int = 0
    score_before: float = 0.5
    score_after: float = 0.85
    changes: List[str] = field(default_factory=list)

class HardeningEngine:
    def apply_profile(self, device_config: Any, profile: SecurityProfile) -> HardeningResult:
        return HardeningResult(rules_applied=len(profile.rules), score_before=0.5, score_after=0.5 + len(profile.rules) * 0.1, changes=profile.rules)

def main() -> None:
    print("=" * 60)
    print("  IoT Security Module — Demo")
    print("=" * 60)

    boot_mgr = SecureBootManager()
    chain = BootChain(stages=[{"stage": "bootloader", "signature": "verified"}, {"stage": "firmware", "signature": "verified"}])
    result = boot_mgr.validate_boot_chain(chain)
    print(f"\n[+] Boot Chain: {'Valid' if result.is_valid else 'Invalid'} ({result.stages_verified} stages)")

    auth = DeviceAuthenticator()
    cert = auth.generate_certificate("sensor-001")
    print(f"\n[+] Certificate: {cert.subject} (fingerprint: {cert.fingerprint})")

    scanner = FirmwareScanner()
    scan = scanner.scan_firmware("/firmware/device.bin")
    print(f"\n[+] Firmware Scan: {scan.vulnerability_count} vulnerabilities")
    for v in scan.vulnerabilities:
        print(f"    {v.cve_id}: {v.severity.value} - {v.description}")

    hardening = HardeningEngine()
    profile = SecurityProfile(name="basic", rules=["disable_telnet", "enable_ssh", "enable_firewall"])
    hr = hardening.apply_profile(None, profile)
    print(f"\n[+] Hardening: {hr.rules_applied} rules applied, score {hr.score_before:.0%} -> {hr.score_after:.0%}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
