"""
Zero Trust Security Module
Identity verification, microsegmentation, least privilege, device trust, and policy engine.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TrustLevel(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    FULL = "full"


class AuthMethod(Enum):
    PASSWORD = "password"
    TOTP = "totp"
    WEBAUTHN = "webauthn"
    PUSH = "push"
    SAML = "saml"
    OIDC = "oidc"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class AuthResult:
    """Authentication result."""
    success: bool
    user_id: str
    risk_score: float
    mfa_verified: bool
    device_trust: str = "medium"
    session_id: str = ""
    expires_at: str = ""


@dataclass
class MicroSegment:
    """Network microsegment."""
    segment_id: str
    name: str
    allowed_traffic: List[Dict[str, Any]] = field(default_factory=list)
    deny_all_default: bool = True
    encryption_required: bool = True


@dataclass
class AccessGrant:
    """Least-privilege access grant."""
    grant_id: str
    user: str
    resource: str
    action: str
    granted: bool
    duration_hours: float
    auto_revoke: bool = True
    justification: str = ""
    expires_at: str = ""


@dataclass
class DeviceTrust:
    """Device trust assessment."""
    device_id: str
    trust_level: TrustLevel
    score: int
    checks_passed: int = 0
    checks_failed: int = 0
    last_checked: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    risk_factors: List[str] = field(default_factory=list)


@dataclass
class PolicyDecision:
    """Policy engine decision."""
    allow: bool
    matched_policy: str
    reason: str = ""
    risk_score: float = 0.0
    conditions: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Identity Verifier
# ---------------------------------------------------------------------------

class IdentityVerifier:
    """Verify identity with continuous authentication."""

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def authenticate(
        self,
        user_id: str,
        mfa_method: str = "totp",
        device_id: str = "",
        source_ip: str = "",
    ) -> AuthResult:
        risk_score = 0.0
        mfa_verified = True
        if mfa_method == "password":
            risk_score += 0.3
        if not device_id:
            risk_score += 0.2
        session_id = secrets.token_hex(16)
        expires = (datetime.now(timezone.utc) + timedelta(hours=8)).isoformat()
        self._sessions[session_id] = {
            "user_id": user_id,
            "created": datetime.now(timezone.utc).isoformat(),
            "expires": expires,
        }
        return AuthResult(
            success=True,
            user_id=user_id,
            risk_score=round(risk_score, 2),
            mfa_verified=mfa_verified,
            session_id=session_id,
            expires_at=expires,
        )

    def validate_session(self, session_id: str) -> bool:
        session = self._sessions.get(session_id)
        if not session:
            return False
        return datetime.now(timezone.utc).isoformat() < session["expires"]

    def revoke_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False


# ---------------------------------------------------------------------------
# Microsegmentation Planner
# ---------------------------------------------------------------------------

class MicrosegmentationPlanner:
    """Design network microsegments."""

    def __init__(self):
        self._segments: Dict[str, MicroSegment] = {}

    def design_segments(
        self,
        workloads: List[str],
        traffic_rules: Optional[List[Dict[str, Any]]] = None,
    ) -> List[MicroSegment]:
        segments: List[MicroSegment] = []
        for wl in workloads:
            seg = MicroSegment(
                segment_id=f"SEG-{len(segments) + 1}",
                name=wl,
                deny_all_default=True,
                encryption_required=True,
            )
            self._segments[wl] = seg
            segments.append(seg)
        if traffic_rules:
            for rule in traffic_rules:
                src = rule.get("from", "")
                dst = rule.get("to", "")
                if src in self._segments:
                    self._segments[src].allowed_traffic.append({
                        "destination": dst,
                        "ports": rule.get("ports", []),
                        "protocol": rule.get("protocol", "tcp"),
                    })
        return segments

    def get_segment(self, name: str) -> Optional[MicroSegment]:
        return self._segments.get(name)

    def validate_traffic(self, src: str, dst: str, port: int) -> bool:
        seg = self._segments.get(src)
        if not seg:
            return False
        for rule in seg.allowed_traffic:
            if rule["destination"] == dst and port in rule.get("ports", []):
                return True
        return False


# ---------------------------------------------------------------------------
# Least Privilege Engine
# ---------------------------------------------------------------------------

class LeastPrivilegeEngine:
    """Manage least-privilege access."""

    def __init__(self, max_duration_hours: float = 8):
        self.max_duration = max_duration_hours
        self._grants: List[AccessGrant] = []

    def request_access(
        self,
        user: str,
        resource: str,
        action: str,
        duration_hours: float = 1,
        justification: str = "",
    ) -> AccessGrant:
        duration = min(duration_hours, self.max_duration)
        granted = duration <= self.max_duration
        grant = AccessGrant(
            grant_id=f"GRANT-{secrets.token_hex(4).upper()}",
            user=user,
            resource=resource,
            action=action,
            granted=granted,
            duration_hours=duration,
            auto_revoke=True,
            justification=justification,
            expires_at=(datetime.now(timezone.utc) + timedelta(hours=duration)).isoformat(),
        )
        if granted:
            self._grants.append(grant)
        return grant

    def revoke_expired(self) -> int:
        now = datetime.now(timezone.utc)
        before = len(self._grants)
        self._grants = [
            g for g in self._grants
            if datetime.fromisoformat(g.expires_at) > now
        ]
        return before - len(self._grants)

    def get_active_grants(self, user: str) -> List[AccessGrant]:
        return [g for g in self._grants if g.user == user]


# ---------------------------------------------------------------------------
# Device Trust Checker
# ---------------------------------------------------------------------------

class DeviceTrustChecker:
    """Assess device trust."""

    def check_device(
        self,
        device_id: str,
        os_version: str = "",
        disk_encrypted: bool = True,
        antivirus_updated: bool = True,
        compliant: bool = True,
    ) -> DeviceTrust:
        score = 0
        passed = 0
        failed = 0
        risk_factors: List[str] = []
        if disk_encrypted:
            score += 25; passed += 1
        else:
            failed += 1; risk_factors.append("Disk not encrypted")
        if antivirus_updated:
            score += 25; passed += 1
        else:
            failed += 1; risk_factors.append("Antivirus not updated")
        if compliant:
            score += 25; passed += 1
        else:
            failed += 1; risk_factors.append("Device non-compliant")
        if os_version and "Windows 11" in os_version:
            score += 25; passed += 1
        elif os_version:
            score += 15; passed += 1
        else:
            failed += 1; risk_factors.append("OS version unknown")
        if score >= 75:
            level = TrustLevel.HIGH
        elif score >= 50:
            level = TrustLevel.MEDIUM
        elif score >= 25:
            level = TrustLevel.LOW
        else:
            level = TrustLevel.NONE
        return DeviceTrust(
            device_id=device_id,
            trust_level=level,
            score=score,
            checks_passed=passed,
            checks_failed=failed,
            risk_factors=risk_factors,
        )


# ---------------------------------------------------------------------------
# Policy Engine
# ---------------------------------------------------------------------------

class PolicyEngine:
    """Evaluate zero trust policies."""

    def __init__(self):
        self._policies: List[Dict[str, Any]] = []

    def add_policy(
        self,
        name: str,
        conditions: Dict[str, Any],
        effect: str = "allow",
    ) -> None:
        self._policies.append({"name": name, "conditions": conditions, "effect": effect})

    def evaluate(
        self,
        subject: str,
        resource: str,
        action: str,
        context: Optional[Dict[str, str]] = None,
    ) -> PolicyDecision:
        context = context or {}
        for policy in self._policies:
            if self._matches(policy, subject, resource, action, context):
                return PolicyDecision(
                    allow=policy["effect"] == "allow",
                    matched_policy=policy["name"],
                    risk_score=0.2 if context.get("device_trust") != "high" else 0.0,
                )
        return PolicyDecision(
            allow=False,
            matched_policy="default_deny",
            reason="No matching policy — default deny",
        )

    def _matches(
        self,
        policy: Dict,
        subject: str,
        resource: str,
        action: str,
        context: Dict[str, str],
    ) -> bool:
        conds = policy.get("conditions", {})
        if "subject" in conds and subject != conds["subject"]:
            return False
        if "resource" in conds and resource != conds["resource"]:
            return False
        if "action" in conds and action != conds["action"]:
            return False
        for key, value in conds.items():
            if key in ("subject", "resource", "action"):
                continue
            if context.get(key) != value:
                return False
        return True


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Zero Trust Security Demo")
    print("=" * 60)

    print("\n[1] Identity Verification")
    verifier = IdentityVerifier()
    auth = verifier.authenticate("user@company.com", "totp", "dev-001", "192.168.1.100")
    print(f"  Success: {auth.success}")
    print(f"  Risk: {auth.risk_score}")
    print(f"  MFA: {auth.mfa_verified}")
    print(f"  Session valid: {verifier.validate_session(auth.session_id)}")

    print("\n[2] Microsegmentation")
    planner = MicrosegmentationPlanner()
    segments = planner.design_segments(
        ["web", "app", "db"],
        [{"from": "web", "to": "app", "ports": [443]}, {"from": "app", "to": "db", "ports": [5432]}],
    )
    print(f"  Segments: {len(segments)}")
    print(f"  Web->App:443: {planner.validate_traffic('web', 'app', 443)}")
    print(f"  Web->DB:5432: {planner.validate_traffic('web', 'db', 5432)}")

    print("\n[3] Least Privilege")
    lpe = LeastPrivilegeEngine()
    access = lpe.request_access("engineer@co.com", "prod-db", "read", 4, "debug #1234")
    print(f"  Granted: {access.granted}")
    print(f"  Duration: {access.duration_hours}h")

    print("\n[4] Device Trust")
    device_checker = DeviceTrustChecker()
    trust = device_checker.check_device("dev-001", "Windows 11", True, True, True)
    print(f"  Trust: {trust.trust_level.value}")
    print(f"  Score: {trust.score}/100")

    print("\n[5] Policy Engine")
    engine = PolicyEngine()
    engine.add_policy("office_hours", {"device_trust": "high", "location": "office"}, "allow")
    decision = engine.evaluate("user@co.com", "server-01", "ssh", {"device_trust": "high", "location": "office"})
    print(f"  Allow: {decision.allow}")
    print(f"  Policy: {decision.matched_policy}")

    print("\n" + "=" * 60)
    print("  Zero trust security demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
