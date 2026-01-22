from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.backends import default_backend
import time
import hashlib
import secrets
import json


class DeviceAuthMethod(Enum):
    CERTIFICATE = "certificate"
    PRE_SHARED_KEY = "psk"
    TOKEN = "token"
    X509 = "x509"


class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class IoTCertificate:
    cert_id: str
    device_id: str
    public_key: Any
    issuer: str
    subject: str
    not_before: float
    not_after: float
    is_revoked: bool = False
    extensions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeviceIdentity:
    device_id: str
    auth_method: DeviceAuthMethod
    credentials: Dict[str, Any]
    certificates: List[str] = field(default_factory=list)
    is_verified: bool = False
    last_auth: Optional[float] = None
    security_level: SecurityLevel = SecurityLevel.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityEvent:
    event_id: str
    timestamp: float
    event_type: str
    device_id: str
    severity: SecurityLevel
    source_ip: str
    details: Dict[str, Any]
    handled: bool = False


class IoTSecurityManager:
    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.devices: Dict[str, DeviceIdentity] = {}
        self.certificates: Dict[str, IoTCertificate] = {}
        self.security_events: List[SecurityEvent] = []
        self.threat_signatures: Dict[str, Dict] = {}
        self.access_policies: Dict[str, Dict] = {}
        self._private_key = None
        self._initialize_ca()

    def _initialize_ca(self):
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    def register_device(self, device: DeviceIdentity) -> Dict:
        if device.device_id in self.devices:
            return {"status": "error", "message": "Device already registered"}
        self.devices[device.device_id] = device
        return {"status": "success", "device_id": device.device_id}

    def generate_certificate(self, device_id: str, validity_days: int = 365) -> Dict:
        if device_id not in self.devices:
            return {"status": "error", "message": "Device not found"}
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        now = time.time()
        cert = IoTCertificate(
            cert_id=f"cert-{secrets.token_hex(8)}",
            device_id=device_id,
            public_key=public_key,
            issuer="IoT-CA",
            subject=device_id,
            not_before=now,
            not_after=now + (validity_days * 86400)
        )
        self.certificates[cert.cert_id] = cert
        self.devices[device_id].certificates.append(cert.cert_id)
        return {
            "status": "success",
            "cert_id": cert.cert_id,
            "valid_until": cert.not_after
        }

    def authenticate_device(self, device_id: str, credentials: Dict) -> Dict:
        if device_id not in self.devices:
            return {"status": "error", "message": "Device not found", "authenticated": False}
        device = self.devices[device_id]
        if device.auth_method == DeviceAuthMethod.CERTIFICATE:
            return self._authenticate_certificate(device_id, credentials)
        elif device.auth_method == DeviceAuthMethod.PRE_SHARED_KEY:
            return self._authenticate_psk(device_id, credentials)
        elif device.auth_method == DeviceAuthMethod.TOKEN:
            return self._authenticate_token(device_id, credentials)
        return {"status": "error", "message": "Unsupported auth method", "authenticated": False}

    def _authenticate_certificate(self, device_id: str, credentials: Dict) -> Dict:
        cert_id = credentials.get("certificate_id")
        if cert_id in self.certificates and not self.certificates[cert_id].is_revoked:
            self.devices[device_id].last_auth = time.time()
            self.devices[device_id].is_verified = True
            return {"status": "success", "authenticated": True, "method": "certificate"}
        self._log_security_event(device_id, "authentication_failure", SecurityLevel.HIGH, {"reason": "invalid_certificate"})
        return {"status": "error", "authenticated": False, "reason": "Invalid certificate"}

    def _authenticate_psk(self, device_id: str, credentials: Dict) -> Dict:
        provided_key = credentials.get("psk")
        stored_key = self.devices[device_id].credentials.get("psk")
        if provided_key == stored_key:
            self.devices[device_id].last_auth = time.time()
            self.devices[device_id].is_verified = True
            return {"status": "success", "authenticated": True, "method": "psk"}
        self._log_security_event(device_id, "authentication_failure", SecurityLevel.HIGH, {"reason": "invalid_psk"})
        return {"status": "error", "authenticated": False, "reason": "Invalid PSK"}

    def _authenticate_token(self, device_id: str, credentials: Dict) -> Dict:
        token = credentials.get("token")
        stored_token = self.devices[device_id].credentials.get("token")
        if token == stored_token:
            self.devices[device_id].last_auth = time.time()
            self.devices[device_id].is_verified = True
            return {"status": "success", "authenticated": True, "method": "token"}
        self._log_security_event(device_id, "authentication_failure", SecurityLevel.MEDIUM, {"reason": "invalid_token"})
        return {"status": "error", "authenticated": False, "reason": "Invalid token"}

    def revoke_certificate(self, cert_id: str) -> Dict:
        if cert_id in self.certificates:
            self.certificates[cert_id].is_revoked = True
            device_id = self.certificates[cert_id].device_id
            if device_id in self.devices and cert_id in self.devices[device_id].certificates:
                self.devices[device_id].certificates.remove(cert_id)
            self._log_security_event(device_id, "certificate_revocation", SecurityLevel.HIGH, {"cert_id": cert_id})
            return {"status": "success", "revoked": cert_id}
        return {"status": "error", "message": "Certificate not found"}

    def _log_security_event(self, device_id: str, event_type: str, severity: SecurityLevel, details: Dict):
        event = SecurityEvent(
            event_id=f"evt-{secrets.token_hex(6)}",
            timestamp=time.time(),
            event_type=event_type,
            device_id=device_id,
            severity=severity,
            source_ip="192.168.1.100",
            details=details
        )
        self.security_events.append(event)

    def analyze_threat(self, telemetry: Dict) -> Dict:
        threats = []
        anomaly_score = 0
        if telemetry.get("connection_attempts", 0) > 10:
            threats.append({"type": "brute_force", "confidence": 0.85})
            anomaly_score += 30
        if telemetry.get("unusual_traffic_pattern", False):
            threats.append({"type": "data_exfiltration", "confidence": 0.70})
            anomaly_score += 25
        if telemetry.get("failed_auths", 0) > 5:
            threats.append({"type": "credential_stuffing", "confidence": 0.75})
            anomaly_score += 20
        if telemetry.get("port_scan", False):
            threats.append({"type": "reconnaissance", "confidence": 0.80})
            anomaly_score += 15
        return {
            "threats": threats,
            "anomaly_score": min(100, anomaly_score),
            "risk_level": self._calculate_risk_level(anomaly_score)
        }

    def _calculate_risk_level(self, score: float) -> str:
        if score >= 70:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 30:
            return "medium"
        return "low"

    def encrypt_payload(self, device_id: str, payload: Dict) -> Dict:
        if device_id not in self.devices:
            raise ValueError("Device not registered")
        public_key = None
        for cert_id in self.devices[device_id].certificates:
            if not self.certificates[cert_id].is_revoked:
                public_key = self.certificates[cert_id].public_key
                break
        if not public_key:
            raise ValueError("No valid certificate found")
        encrypted = public_key.encrypt(
            json.dumps(payload).encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return {
            "encrypted_data": encrypted.hex(),
            "algorithm": "RSA-OAEP-SHA256"
        }

    def decrypt_payload(self, device_id: str, encrypted_data: str) -> Dict:
        private_key = self._private_key
        decrypted = private_key.decrypt(
            bytes.fromhex(encrypted_data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return json.loads(decrypted.decode())

    def get_security_dashboard(self) -> Dict:
        total_devices = len(self.devices)
        verified_devices = sum(1 for d in self.devices.values() if d.is_verified)
        recent_events = [e for e in self.security_events if time.time() - e.timestamp < 86400]
        critical_events = [e for e in recent_events if e.severity == SecurityLevel.CRITICAL]
        return {
            "organization_id": self.organization_id,
            "devices": {
                "total": total_devices,
                "verified": verified_devices,
                "unverified": total_devices - verified_devices
            },
            "certificates": {
                "total": len(self.certificates),
                "active": sum(1 for c in self.certificates.values() if not c.is_revoked),
                "revoked": sum(1 for c in self.certificates.values() if c.is_revoked)
            },
            "security_events": {
                "last_24h": len(recent_events),
                "critical": len(critical_events)
            }
        }

    def apply_access_policy(self, policy_id: str, policy: Dict):
        self.access_policies[policy_id] = policy

    def check_access(self, device_id: str, resource: str, action: str) -> bool:
        for policy_id, policy in self.access_policies.items():
            if policy.get("device_pattern", "") in device_id:
                if resource in policy.get("resources", []):
                    if action in policy.get("actions", {}).get(resource, []):
                        return policy["actions"][resource][action]
        return False


class IoTFirewall:
    def __init__(self):
        self.rules: List[Dict] = []
        self.blocked_ips: set = set()
        self.rate_limits: Dict[str, List[float]] = {}

    def add_rule(self, rule: Dict):
        self.rules.append(rule)

    def check_packet(self, packet: Dict) -> Dict:
        for rule in self.rules:
            if self._matches_rule(packet, rule):
                if rule.get("action") == "allow":
                    return {"action": "allow", "rule": rule.get("id")}
                else:
                    return {"action": "deny", "rule": rule.get("id")}
        return {"action": "allow", "rule": "default"}

    def _matches_rule(self, packet: Dict, rule: Dict) -> bool:
        if rule.get("source_ip") and packet.get("source_ip") != rule["source_ip"]:
            return False
        if rule.get("destination_port") and packet.get("destination_port") != rule["destination_port"]:
            return False
        if rule.get("protocol") and packet.get("protocol") != rule["protocol"]:
            return False
        return True

    def check_rate_limit(self, client_ip: str, limit: int = 100, window: int = 60) -> bool:
        now = time.time()
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = []
        self.rate_limits[client_ip] = [t for t in self.rate_limits[client_ip] if now - t < window]
        if len(self.rate_limits[client_ip]) >= limit:
            return False
        self.rate_limits[client_ip].append(now)
        return True
