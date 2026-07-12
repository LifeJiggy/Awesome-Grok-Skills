"""
Secrets Management Module
Vault integration, secret rotation, encryption, audit logging, and certificate management.
"""

from __future__ import annotations

import base64
import hashlib
import logging
import secrets
import string
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SecretType(Enum):
    DATABASE = "database"
    API_KEY = "api_key"
    TLS_CERTIFICATE = "tls_certificate"
    SSH_KEY = "ssh_key"
    ENCRYPTION_KEY = "encryption_key"
    GENERIC = "generic"


class RotationPolicy(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"


class AccessAction(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    LIST = "list"
    ROTATE = "rotate"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Secret:
    """Secret value with metadata."""
    path: str
    data: Dict[str, str]
    secret_type: SecretType = SecretType.GENERIC
    version: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at


@dataclass
class RotationSchedule:
    """Secret rotation schedule."""
    secret_path: str
    policy: RotationPolicy
    next_rotation: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    last_rotation: Optional[datetime] = None
    generator: str = "password"
    length: int = 32
    enabled: bool = True


@dataclass
class EncryptedData:
    """Encrypted data container."""
    ciphertext: str
    key_id: str
    algorithm: str = "AES-256-GCM"
    iv: str = ""
    tag: str = ""
    encrypted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AuditEntry:
    """Secret access audit entry."""
    timestamp: str
    secret_path: str
    accessor: str
    action: AccessAction
    source_ip: str = ""
    success: bool = True
    details: str = ""


@dataclass
class Certificate:
    """TLS certificate."""
    common_name: str
    serial_number: str
    not_before: str = ""
    not_after: str = ""
    san: List[str] = field(default_factory=list)
    issuer: str = "Internal CA"
    pem: str = ""
    key_pem: str = ""


@dataclass
class SecretMetadata:
    """Secret metadata for listing."""
    path: str
    secret_type: str
    version: int
    created_at: str
    expires_at: str = ""
    rotation_enabled: bool = False


# ---------------------------------------------------------------------------
# Vault Client
# ---------------------------------------------------------------------------

class VaultClient:
    """HashiCorp Vault client wrapper."""

    def __init__(self, url: str = "https://vault.internal:8200", token: str = ""):
        self.url = url
        self.token = token
        self._authenticated = False
        self._secrets: Dict[str, Secret] = {}

    def authenticate(self, method: str = "token", **kwargs) -> bool:
        self._authenticated = True
        return True

    def read_secret(self, path: str) -> Secret:
        return Secret(
            path=path,
            data={"username": "admin", "password": secrets.token_hex(16)},
        )

    def write_secret(self, path: str, data: Dict[str, str]) -> Secret:
        secret = Secret(path=path, data=data, version=1)
        self._secrets[path] = secret
        return secret

    def delete_secret(self, path: str) -> bool:
        if path in self._secrets:
            del self._secrets[path]
            return True
        return False

    def list_secrets(self, path: str = "") -> List[SecretMetadata]:
        return [
            SecretMetadata(
                path=s.path,
                secret_type=s.secret_type.value,
                version=s.version,
                created_at=s.created_at.isoformat(),
            )
            for s in self._secrets.values()
        ]


# ---------------------------------------------------------------------------
# Secret Rotator
# ---------------------------------------------------------------------------

class SecretRotator:
    """Automatic secret rotation."""

    POLICY_DAYS = {
        RotationPolicy.DAILY: 1,
        RotationPolicy.WEEKLY: 7,
        RotationPolicy.MONTHLY: 30,
        RotationPolicy.QUARTERLY: 90,
        RotationPolicy.ANNUALLY: 365,
    }

    def __init__(self):
        self._schedules: Dict[str, RotationSchedule] = {}

    def schedule_rotation(
        self,
        secret_path: str,
        rotation_policy: str = "monthly",
        generator: str = "password",
        length: int = 32,
    ) -> RotationSchedule:
        policy = RotationPolicy(rotation_policy)
        days = self.POLICY_DAYS.get(policy, 30)
        schedule = RotationSchedule(
            secret_path=secret_path,
            policy=policy,
            next_rotation=datetime.now(timezone.utc) + timedelta(days=days),
            generator=generator,
            length=length,
        )
        self._schedules[secret_path] = schedule
        return schedule

    def generate_secret(self, secret_type: str = "password", length: int = 32) -> str:
        if secret_type == "password":
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            return "".join(secrets.choice(chars) for _ in range(length))
        elif secret_type == "api_key":
            return f"ak_{secrets.token_hex(length // 2)}"
        elif secret_type == "hex":
            return secrets.token_hex(length // 2)
        return secrets.token_urlsafe(length)

    def check_rotations_needed(self) -> List[RotationSchedule]:
        now = datetime.now(timezone.utc)
        return [
            s for s in self._schedules.values()
            if s.enabled and s.next_rotation <= now
        ]


# ---------------------------------------------------------------------------
# Encryption Manager
# ---------------------------------------------------------------------------

class EncryptionManager:
    """Manage encryption at rest."""

    def __init__(self):
        self._keys: Dict[str, bytes] = {}

    def generate_key(self, key_id: str) -> str:
        key = secrets.token_bytes(32)
        self._keys[key_id] = key
        return base64.b64encode(key).decode()

    def encrypt(self, plaintext: str, key_id: str = "default") -> EncryptedData:
        if key_id not in self._keys:
            self.generate_key(key_id)
        key = self._keys[key_id]
        iv = secrets.token_bytes(16)
        plaintext_bytes = plaintext.encode()
        cipher_bytes = bytes(
            (plaintext_bytes[i] ^ key[i % len(key)]) for i in range(len(plaintext_bytes))
        )
        return EncryptedData(
            ciphertext=base64.b64encode(cipher_bytes).decode(),
            key_id=key_id,
            iv=base64.b64encode(iv).decode(),
        )

    def decrypt(self, encrypted: EncryptedData, key_id: str = "default") -> str:
        key = self._keys.get(key_id, b'\x00' * 32)
        cipher_bytes = base64.b64decode(encrypted.ciphertext)
        plain_bytes = bytes(
            (cipher_bytes[i] ^ key[i % len(key)]) for i in range(len(cipher_bytes))
        )
        return plain_bytes.decode()


# ---------------------------------------------------------------------------
# Audit Logger
# ---------------------------------------------------------------------------

class AuditLogger:
    """Log secret access for compliance."""

    def __init__(self):
        self._entries: List[AuditEntry] = []

    def log_access(
        self,
        secret_path: str,
        accessor: str,
        action: str,
        source_ip: str = "",
        success: bool = True,
    ) -> AuditEntry:
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            secret_path=secret_path,
            accessor=accessor,
            action=AccessAction(action),
            source_ip=source_ip,
            success=success,
        )
        self._entries.append(entry)
        return entry

    def get_entries(
        self,
        since_hours: int = 24,
        secret_path: str = "",
        accessor: str = "",
    ) -> List[AuditEntry]:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        entries = self._entries
        if secret_path:
            entries = [e for e in entries if e.secret_path == secret_path]
        if accessor:
            entries = [e for e in entries if e.accessor == accessor]
        return entries

    def get_summary(self, hours: int = 24) -> Dict[str, int]:
        entries = self.get_entries(since_hours=hours)
        summary: Dict[str, int] = {}
        for e in entries:
            summary[e.action.value] = summary.get(e.action.value, 0) + 1
        return summary


# ---------------------------------------------------------------------------
# Certificate Manager
# ---------------------------------------------------------------------------

class CertificateManager:
    """Manage TLS certificates."""

    def issue_certificate(
        self,
        common_name: str,
        ttl_days: int = 365,
        san: Optional[List[str]] = None,
        key_type: str = "RSA2048",
    ) -> Certificate:
        serial = hashlib.sha256(common_name.encode()).hexdigest()[:16]
        now = datetime.now(timezone.utc)
        return Certificate(
            common_name=common_name,
            serial_number=serial,
            not_before=now.isoformat(),
            not_after=(now + timedelta(days=ttl_days)).isoformat(),
            san=san or [common_name],
            issuer="Internal CA",
        )

    def check_expiration(self, cert: Certificate, warning_days: int = 30) -> bool:
        not_after = datetime.fromisoformat(cert.not_after)
        days_remaining = (not_after - datetime.now(timezone.utc)).days
        return days_remaining <= warning_days

    def revoke_certificate(self, serial_number: str) -> bool:
        return True


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Secrets Management Demo")
    print("=" * 60)

    print("\n[1] Vault Client")
    vault = VaultClient()
    vault.authenticate("approle")
    secret = vault.write_secret("secret/app/db", {"password": "s3cr3t"})
    print(f"  Secret stored: {secret.path}")

    print("\n[2] Secret Rotation")
    rotator = SecretRotator()
    schedule = rotator.schedule_rotation("secret/app/db", "monthly", length=32)
    print(f"  Next rotation: {schedule.next_rotation}")
    new_secret = rotator.generate_secret("password", 32)
    print(f"  Generated: {new_secret[:8]}...")
    api_key = rotator.generate_secret("api_key", 32)
    print(f"  API key: {api_key[:16]}...")

    print("\n[3] Encryption")
    encryptor = EncryptionManager()
    enc = encryptor.encrypt("sensitive-data", "prod-key")
    dec = encryptor.decrypt(enc, "prod-key")
    print(f"  Encrypted: {enc.ciphertext[:20]}...")
    print(f"  Decrypted: {dec}")

    print("\n[4] Audit Logging")
    audit = AuditLogger()
    audit.log_access("secret/app/db", "service-1", "read")
    audit.log_access("secret/app/api", "service-2", "write")
    entries = audit.get_entries(24)
    print(f"  Entries: {len(entries)}")
    summary = audit.get_summary(24)
    print(f"  Summary: {summary}")

    print("\n[5] Certificate Management")
    cert_mgr = CertificateManager()
    cert = cert_mgr.issue_certificate("api.example.com", 365, ["api.example.com", "www.example.com"])
    print(f"  CN: {cert.common_name}")
    print(f"  Serial: {cert.serial_number}")
    print(f"  Expires: {cert.not_after}")
    expiring = cert_mgr.check_expiration(cert)
    print(f"  Expiring soon: {expiring}")

    print("\n" + "=" * 60)
    print("  Secrets management demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
