"""
API Security Module — OAuth 2.0, JWT validation, RBAC, rate limiting, input validation,
security headers, and OWASP API Top 10 protections.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AuthMethod(Enum):
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    JWT = "jwt"
    MTLS = "mtls"
    BASIC = "basic"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    MANAGE = "manage"


class RateLimitStrategy(Enum):
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"
    FIXED_WINDOW = "fixed_window"


class SecuritySeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class OWASPCategory(Enum):
    BOLA = "api1"           # Broken Object Level Authorization
    BROKEN_AUTH = "api2"    # Broken Authentication
    EXCESSIVE_DATA = "api3" # Excessive Data Exposure
    LACK_RESOURCES = "api4" # Lack of Resources & Rate Limiting
    BROKEN_FUNCTION = "api5" # Broken Function Level Authorization
    MASS_ASSIGNMENT = "api6" # Mass Assignment
    SSRF = "api7"           # Security Misconfiguration
    INJECTION = "api8"      # Injection
    IMPROPER资产管理 = "api9"  # Improper Assets Management
    INSUFFICIENT_LOGGING = "api10" # Insufficient Logging & Monitoring


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class OAuthConfig:
    """OAuth 2.0 configuration."""
    issuer: str = ""
    audience: str = ""
    scopes: List[str] = field(default_factory=list)
    token_endpoint: str = ""
    jwks_uri: str = ""
    introspection_endpoint: str = ""
    grant_types: List[str] = field(default_factory=lambda: ["authorization_code", "client_credentials"])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issuer": self.issuer,
            "audience": self.audience,
            "scopes": self.scopes,
            "grant_types": self.grant_types,
        }


@dataclass
class JWTClaims:
    """Decoded JWT claims."""
    sub: str = ""
    iss: str = ""
    aud: str = ""
    exp: float = 0
    iat: float = 0
    scopes: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    custom: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        return time.time() > self.exp

    def to_dict(self) -> Dict[str, Any]:
        return {"sub": self.sub, "iss": self.iss, "scopes": self.scopes, "roles": self.roles}


@dataclass
class JWTValidationResult:
    """Result of JWT validation."""
    valid: bool
    claims: Optional[JWTClaims] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    expires_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "error": self.error,
            "scopes": self.scopes,
        }


@dataclass
class APIKey:
    """An API key for authentication."""
    key_id: str
    key_hash: str
    name: str
    scopes: List[str] = field(default_factory=list)
    rate_limit: int = 100
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None
    revoked: bool = False
    last_used: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "name": self.name,
            "scopes": self.scopes,
            "revoked": self.revoked,
        }


@dataclass
class RBACRole:
    """A role with assigned permissions."""
    role_id: str
    name: str
    permissions: List[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"role_id": self.role_id, "name": self.name, "permissions": self.permissions}


@dataclass
class AuthorizationResult:
    """Result of an authorization check."""
    authorized: bool
    user_id: str
    resource: str
    action: str
    role: Optional[str] = None
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authorized": self.authorized,
            "user_id": self.user_id,
            "resource": self.resource,
            "action": self.action,
            "reason": self.reason,
        }


@dataclass
class RateLimitResult:
    """Result of rate limit check."""
    allowed: bool
    limit: int
    remaining: int
    reset_at: float
    retry_after: Optional[float] = None

    @property
    def headers(self) -> Dict[str, str]:
        headers = {
            "X-RateLimit-Limit": str(self.limit),
            "X-RateLimit-Remaining": str(self.remaining),
            "X-RateLimit-Reset": str(int(self.reset_at)),
        }
        if not self.allowed and self.retry_after:
            headers["Retry-After"] = str(int(self.retry_after))
        return headers


@dataclass
class SecurityHeader:
    """A security header configuration."""
    name: str
    value: str
    description: str = ""

    def to_tuple(self) -> Tuple[str, str]:
        return (self.name, self.value)


@dataclass
class SecurityAuditEntry:
    """An API security audit log entry."""
    timestamp: str
    user_id: str
    endpoint: str
    method: str
    status_code: int
    ip_address: str
    user_agent: str = ""
    response_time_ms: float = 0
    auth_method: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "endpoint": self.endpoint,
            "status": self.status_code,
        }


@dataclass
class ValidationRule:
    """Input validation rule."""
    field: str
    rule_type: str  # "type", "regex", "min_length", "max_length", "enum", "custom"
    value: Any = None
    error_message: str = ""

    def validate(self, data: Any) -> bool:
        if self.rule_type == "type" and self.value == "string":
            return isinstance(data, str)
        elif self.rule_type == "type" and self.value == "integer":
            return isinstance(data, int)
        elif self.rule_type == "regex":
            return bool(re.match(self.value, str(data)))
        elif self.rule_type == "min_length":
            return len(str(data)) >= self.value
        elif self.rule_type == "max_length":
            return len(str(data)) <= self.value
        elif self.rule_type == "enum":
            return data in self.value
        return True


@dataclass
class SecurityScanResult:
    """Result of an API security scan."""
    endpoint: str
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    owasp_issues: List[OWASPCategory] = field(default_factory=list)
    severity: SecuritySeverity = SecuritySeverity.INFO
    recommendations: List[str] = field(default_factory=list)

    @property
    def is_secure(self) -> bool:
        return len(self.vulnerabilities) == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "vulnerabilities": len(self.vulnerabilities),
            "owasp_issues": [i.value for i in self.owasp_issues],
            "severity": self.severity.value,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class JWTValidator:
    """Validate JWT tokens."""

    def __init__(self, config: Optional[OAuthConfig] = None):
        self.config = config or OAuthConfig()

    def validate(self, token: str) -> JWTValidationResult:
        """Validate a JWT token."""
        parts = token.split(".")
        if len(parts) != 3:
            return JWTValidationResult(valid=False, error="Invalid token format", error_code="INVALID_FORMAT")

        try:
            payload_b64 = parts[1] + "=" * (4 - len(parts[1]) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        except Exception:
            return JWTValidationResult(valid=False, error="Invalid token payload", error_code="INVALID_PAYLOAD")

        claims = JWTClaims(
            sub=payload.get("sub", ""),
            iss=payload.get("iss", ""),
            aud=payload.get("aud", ""),
            exp=payload.get("exp", 0),
            iat=payload.get("iat", 0),
            scopes=payload.get("scope", "").split() if payload.get("scope") else [],
            roles=payload.get("roles", []),
        )

        if claims.is_expired:
            return JWTValidationResult(valid=False, error="Token expired", error_code="EXPIRED")

        if self.config.issuer and claims.iss != self.config.issuer:
            return JWTValidationResult(valid=False, error="Invalid issuer", error_code="INVALID_ISSUER")

        return JWTValidationResult(
            valid=True, claims=claims,
            scopes=claims.scopes,
            expires_at=datetime.fromtimestamp(claims.exp, tz=timezone.utc).isoformat(),
        )

    def create_token(
        self, subject: str, scopes: List[str], expires_in: int = 900,
        roles: Optional[List[str]] = None, **claims: Any,
    ) -> str:
        """Create a JWT token (simplified for demo)."""
        now = time.time()
        payload = {
            "sub": subject,
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "iat": now,
            "exp": now + expires_in,
            "scope": " ".join(scopes),
            "roles": roles or [],
            **claims,
        }
        header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).decode()
        body = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
        return f"{header}.{body}.signature"


class RBACPolicy:
    """Role-based access control policy."""

    def __init__(self):
        self._roles: Dict[str, RBACRole] = {}
        self._assignments: Dict[str, str] = {}  # user_id -> role_id
        self._resource_permissions: Dict[str, List[str]] = {}

    def add_role(self, name: str, permissions: List[str], description: str = "") -> RBACRole:
        role = RBACRole(role_id=f"role-{uuid.uuid4().hex[:8]}", name=name,
                       permissions=permissions, description=description)
        self._roles[name] = role
        return role

    def add_assignment(self, user_id: str, role_name: str) -> None:
        self._assignments[user_id] = role_name

    def get_role(self, user_id: str) -> Optional[RBACRole]:
        role_name = self._assignments.get(user_id)
        return self._roles.get(role_name) if role_name else None

    def check(self, user_id: str, permission: str, resource: str = "*") -> AuthorizationResult:
        role = self.get_role(user_id)
        if not role:
            return AuthorizationResult(
                authorized=False, user_id=user_id, resource=resource,
                action=permission, reason="No role assigned",
            )

        if "*" in role.permissions or permission in role.permissions:
            return AuthorizationResult(
                authorized=True, user_id=user_id, resource=resource,
                action=permission, role=role.name,
            )

        return AuthorizationResult(
            authorized=False, user_id=user_id, resource=resource,
            action=permission, role=role.name,
            reason=f"Permission '{permission}' not in role '{role.name}'",
        )

    def add_resource_permission(self, resource: str, permissions: List[str]) -> None:
        self._resource_permissions[resource] = permissions

    def list_roles(self) -> List[RBACRole]:
        return list(self._roles.values())


class RateLimiter:
    """Rate limiter with multiple strategies."""

    def __init__(
        self,
        default_limit: int = 100,
        window_seconds: int = 60,
        strategy: str = "sliding_window",
    ):
        self.default_limit = default_limit
        self.window = window_seconds
        self.strategy = RateLimitStrategy(strategy)
        self._limits: Dict[str, int] = {}
        self._usage: Dict[str, List[float]] = {}

    def add_limit(self, endpoint: str, limit: int, window: int = 60) -> None:
        self._limits[endpoint] = limit

    def check(self, identifier: str, endpoint: str) -> RateLimitResult:
        limit = self._limits.get(endpoint, self.default_limit)
        key = f"{identifier}:{endpoint}"
        now = time.time()

        if key not in self._usage:
            self._usage[key] = []

        # Clean old entries
        self._usage[key] = [t for t in self._usage[key] if now - t < self.window]

        current = len(self._usage[key])
        if current < limit:
            self._usage[key].append(now)
            return RateLimitResult(
                allowed=True, limit=limit, remaining=limit - current - 1,
                reset_at=now + self.window,
            )
        else:
            oldest = self._usage[key][0] if self._usage[key] else now
            return RateLimitResult(
                allowed=False, limit=limit, remaining=0,
                reset_at=oldest + self.window,
                retry_after=oldest + self.window - now,
            )

    def reset(self, identifier: str, endpoint: str) -> None:
        key = f"{identifier}:{endpoint}"
        self._usage.pop(key, None)


class InputValidator:
    """Validate API request inputs against schemas."""

    def __init__(self):
        self._rules: Dict[str, List[ValidationRule]] = {}

    def add_rule(self, endpoint: str, field: str, rule_type: str,
                 value: Any = None, error_message: str = "") -> None:
        if endpoint not in self._rules:
            self._rules[endpoint] = []
        self._rules[endpoint].append(ValidationRule(field=field, rule_type=rule_type,
                                                     value=value, error_message=error_message))

    def validate(self, endpoint: str, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        rules = self._rules.get(endpoint, [])
        for rule in rules:
            field_value = data.get(rule.field)
            if field_value is not None and not rule.validate(field_value):
                errors.append(rule.error_message or f"Validation failed for {rule.field}")
        return len(errors) == 0, errors

    @staticmethod
    def detect_injection(value: str) -> bool:
        patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\b)",
            r"(--|;|/\*|\*/|@@|@)",
            r"(<script[^>]*>|javascript:)",
            r"(\.\.\/|\.\.\\)",
        ]
        for pattern in patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False


class SecurityHeaders:
    """Manage API security headers."""

    @staticmethod
    def get_default_headers() -> Dict[str, str]:
        return {
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Pragma": "no-cache",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

    @staticmethod
    def get_cors_headers(allow_origins: List[str], allow_methods: List[str],
                         allow_headers: List[str], max_age: int = 86400) -> Dict[str, str]:
        origin = ", ".join(allow_origins)
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": ", ".join(allow_methods),
            "Access-Control-Allow-Headers": ", ".join(allow_headers),
            "Access-Control-Max-Age": str(max_age),
            "Access-Control-Allow-Credentials": "true" if "*" not in allow_origins else "false",
        }


class APISecurityScanner:
    """Scan API endpoints for security vulnerabilities."""

    def scan_endpoint(self, endpoint: str, method: str = "GET",
                     requires_auth: bool = True) -> SecurityScanResult:
        result = SecurityScanResult(endpoint=endpoint)

        if not requires_auth and method in ("POST", "PUT", "DELETE"):
            result.vulnerabilities.append({
                "type": "broken_authentication",
                "owasp": OWASPCategory.BROKEN_AUTH.value,
                "severity": "critical",
                "description": f"Endpoint {method} {endpoint} does not require authentication",
            })
            result.owasp_issues.append(OWASPCategory.BROKEN_AUTH)

        if "user_id" in endpoint or "userId" in endpoint:
            result.vulnerabilities.append({
                "type": "bola",
                "owasp": OWASPCategory.BOLA.value,
                "severity": "high",
                "description": "Endpoint may be vulnerable to Broken Object Level Authorization",
            })
            result.owasp_issues.append(OWASPCategory.BOLA)
            result.recommendations.append("Implement resource-level authorization checks")

        if not result.is_secure:
            result.severity = SecuritySeverity.HIGH

        return result


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the API security toolkit."""
    print("API Security Toolkit")
    print("=" * 60)

    # JWT
    oauth = OAuthConfig(issuer="https://auth.example.com", audience="https://api.example.com")
    jwt_v = JWTValidator(oauth)
    token = jwt_v.create_token("user-123", ["read:users", "write:users"], roles=["admin"])
    result = jwt_v.validate(token)
    print(f"\nJWT valid: {result.valid}, scopes: {result.scopes}")

    # RBAC
    rbac = RBACPolicy()
    rbac.add_role("admin", permissions=["read:*", "write:*", "delete:*"])
    rbac.add_role("user", permissions=["read:own", "write:own"])
    rbac.add_assignment("user-123", "admin")
    auth = rbac.check("user-123", "write:users")
    print(f"RBAC: {auth.authorized} (role: {auth.role})")

    # Rate limiting
    limiter = RateLimiter(default_limit=5, window_seconds=60)
    limiter.add_limit("POST /api/users", limit=3, window=60)
    for i in range(5):
        r = limiter.check("user-123", "POST /api/users")
        print(f"  Request {i+1}: {'ALLOWED' if r.allowed else 'BLOCKED'} (remaining: {r.remaining})")

    # Input validation
    validator = InputValidator()
    validator.add_rule("/api/users", "email", "regex", r"^[^@]+@[^@]+\.[^@]+$", "Invalid email")
    valid, errors = validator.validate("/api/users", {"email": "not-an-email"})
    print(f"\nValidation: valid={valid}, errors={errors}")

    # Injection detection
    print(f"\nSQL injection detected: {InputValidator.detect_injection('1; DROP TABLE users--')}")
    print(f"XSS detected: {InputValidator.detect_injection('<script>alert(1)</script>')}")

    # Security headers
    headers = SecurityHeaders.get_default_headers()
    print(f"\nSecurity headers: {len(headers)} configured")

    # Security scan
    scanner = APISecurityScanner()
    scan = scanner.scan_endpoint("/api/users/{id}", "GET", requires_auth=False)
    print(f"\nSecurity scan: {scan.endpoint}")
    print(f"  Vulnerabilities: {len(scan.vulnerabilities)}")
    print(f"  OWASP issues: {[i.value for i in scan.owasp_issues]}")


if __name__ == "__main__":
    main()
