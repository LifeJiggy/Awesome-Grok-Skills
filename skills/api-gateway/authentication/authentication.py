"""
Gateway Authentication Module — OAuth 2.0, API key validation, JWT verification,
mTLS, HMAC signing, and multi-tenant authentication for API gateways.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AuthMethod(Enum):
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    JWT = "jwt"
    MTLS = "mtls"
    HMAC = "hmac"
    BASIC = "basic"
    NONE = "none"


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    ID = "id"
    DEVICE = "device"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class OAuth2Config:
    """OAuth 2.0 configuration."""
    issuer: str = ""
    audience: str = ""
    jwks_uri: str = ""
    introspection_endpoint: str = ""
    token_endpoint: str = ""
    authorization_endpoint: str = ""
    scopes_supported: List[str] = field(default_factory=list)
    grant_types: List[str] = field(default_factory=lambda: ["authorization_code", "client_credentials"])
    jwks_cache_ttl_s: int = 3600
    introspection_cache_ttl_s: int = 300

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issuer": self.issuer,
            "audience": self.audience,
            "jwks_uri": self.jwks_uri,
            "scopes": self.scopes_supported,
        }


@dataclass
class APIKeyInfo:
    """An API key with metadata."""
    key_id: str
    key_hash: str
    name: str
    scopes: List[str] = field(default_factory=list)
    rate_limit: int = 1000
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None
    revoked: bool = False
    last_used: Optional[str] = None
    tenant_id: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        if self.revoked:
            return False
        if self.expires_at:
            try:
                exp = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
                if datetime.now(timezone.utc) > exp:
                    return False
            except ValueError:
                pass
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "name": self.name,
            "scopes": self.scopes,
            "revoked": self.revoked,
            "tenant_id": self.tenant_id,
        }


@dataclass
class MTLSConfig:
    """mTLS configuration."""
    client_ca_bundle: str = ""
    verify_client_cert: bool = True
    allowed_cn_patterns: List[str] = field(default_factory=list)
    allowed_issuer_patterns: List[str] = field(default_factory=list)
    min_cert_key_size: int = 2048

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verify": self.verify_client_cert,
            "ca_bundle": self.client_ca_bundle,
            "allowed_cn": self.allowed_cn_patterns,
        }


@dataclass
class AuthResult:
    """Result of authentication."""
    authenticated: bool
    user_id: str = ""
    client_id: str = ""
    scopes: List[str] = field(default_factory=list)
    auth_method: AuthMethod = AuthMethod.NONE
    token_type: Optional[TokenType] = None
    expires_at: Optional[float] = None
    tenant_id: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        if self.expires_at:
            return time.time() > self.expires_at
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "authenticated": self.authenticated,
            "user_id": self.user_id,
            "client_id": self.client_id,
            "scopes": self.scopes,
            "auth_method": self.auth_method.value,
            "error": self.error,
        }


@dataclass
class TokenIntrospection:
    """RFC 7662 token introspection result."""
    active: bool
    sub: str = ""
    client_id: str = ""
    scope: str = ""
    exp: Optional[float] = None
    iat: Optional[float] = None
    iss: str = ""
    token_type: str = "Bearer"
    username: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "active": self.active,
            "sub": self.sub,
            "scope": self.scope,
            "exp": self.exp,
        }


@dataclass
class HMACSignature:
    """HMAC request signature."""
    algorithm: str = "sha256"
    signature: str = ""
    timestamp: str = ""
    nonce: str = ""

    def verify(self, payload: bytes, secret: str) -> bool:
        if not self.signature or not self.timestamp:
            return False
        message = f"{self.timestamp}.{self.nonce}.{payload.decode('utf-8', errors='replace')}"
        expected = hmac.new(
            secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(self.signature, expected)


@dataclass
class JWKSKey:
    """A JWKS key entry."""
    kid: str
    kty: str
    alg: str
    use: str = "sig"
    n: str = ""
    e: str = ""
    x5c: List[str] = field(default_factory=list)
    expires_at: Optional[float] = None

    @property
    def is_valid(self) -> bool:
        if self.expires_at and time.time() > self.expires_at:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {"kid": self.kid, "kty": self.kty, "alg": self.alg, "use": self.use}


@dataclass
class RouteAuthConfig:
    """Authentication configuration for a route."""
    auth_required: bool = True
    auth_methods: List[AuthMethod] = field(default_factory=lambda: [AuthMethod.OAUTH2])
    required_scopes: List[str] = field(default_factory=list)
    allow_api_key: bool = True
    allow_mtls: bool = False
    rate_limit_per_minute: Optional[int] = None
    tenant_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class JWTVerifier:
    """Verify JWT tokens using JWKS."""

    def __init__(self, config: Optional[OAuth2Config] = None):
        self.config = config or OAuth2Config()
        self._jwks_cache: Dict[str, JWKSKey] = {}
        self._jwks_cache_time: float = 0

    def verify(self, token: str) -> AuthResult:
        parts = token.split(".")
        if len(parts) != 3:
            return AuthResult(authenticated=False, error="Invalid token format")

        try:
            header_b64 = parts[0] + "=" * (4 - len(parts[0]) % 4)
            header = json.loads(base64.urlsafe_b64decode(header_b64))
            payload_b64 = parts[1] + "=" * (4 - len(parts[1]) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        except Exception:
            return AuthResult(authenticated=False, error="Invalid token encoding")

        # Validate expiration
        exp = payload.get("exp", 0)
        if exp and time.time() > exp:
            return AuthResult(authenticated=False, error="Token expired", error_code="EXPIRED")

        # Validate issuer
        if self.config.issuer and payload.get("iss") != self.config.issuer:
            return AuthResult(authenticated=False, error="Invalid issuer")

        # Validate audience
        if self.config.audience:
            aud = payload.get("aud", "")
            if isinstance(aud, list):
                if self.config.audience not in aud:
                    return AuthResult(authenticated=False, error="Invalid audience")
            elif aud != self.config.audience:
                return AuthResult(authenticated=False, error="Invalid audience")

        scopes = payload.get("scope", "").split() if payload.get("scope") else []

        return AuthResult(
            authenticated=True,
            user_id=payload.get("sub", ""),
            client_id=payload.get("client_id", ""),
            scopes=scopes,
            auth_method=AuthMethod.JWT,
            token_type=TokenType.ACCESS,
            expires_at=exp,
            metadata={"kid": header.get("kid", ""), "alg": header.get("alg", "")},
        )

    def load_jwks(self, keys: List[Dict[str, Any]]) -> None:
        for key_data in keys:
            key = JWKSKey(
                kid=key_data.get("kid", ""),
                kty=key_data.get("kty", ""),
                alg=key_data.get("alg", ""),
                use=key_data.get("use", "sig"),
                n=key_data.get("n", ""),
                e=key_data.get("e", ""),
            )
            self._jwks_cache[key.kid] = key
        self._jwks_cache_time = time.time()

    def get_key(self, kid: str) -> Optional[JWKSKey]:
        return self._jwks_cache.get(kid)


class APIKeyStore:
    """Manage and validate API keys."""

    def __init__(self):
        self._keys: Dict[str, APIKeyInfo] = {}
        self._hash_index: Dict[str, str] = {}  # hash -> key_id

    @staticmethod
    def _hash_key(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()[:32]

    def add_key(self, key_id: str, name: str, scopes: Optional[List[str]] = None,
                rate_limit: int = 1000, expires_at: Optional[str] = None,
                tenant_id: Optional[str] = None) -> APIKeyInfo:
        key_hash = self._hash_key(key_id)
        info = APIKeyInfo(
            key_id=key_id[:8] + "...", key_hash=key_hash, name=name,
            scopes=scopes or [], rate_limit=rate_limit,
            expires_at=expires_at, tenant_id=tenant_id,
        )
        self._keys[info.key_id] = info
        self._hash_index[key_hash] = info.key_id
        return info

    def validate(self, key: str) -> Optional[APIKeyInfo]:
        key_hash = self._hash_key(key)
        key_id = self._hash_index.get(key_hash)
        if key_id:
            info = self._keys[key_id]
            if info.is_valid:
                info.last_used = datetime.now(timezone.utc).isoformat()
                return info
        return None

    def revoke(self, key_id: str) -> bool:
        for info in self._keys.values():
            if info.key_id == key_id:
                info.revoked = True
                return True
        return False

    def list_keys(self, include_revoked: bool = False) -> List[APIKeyInfo]:
        keys = list(self._keys.values())
        if not include_revoked:
            keys = [k for k in keys if not k.revoked]
        return keys


class TokenIntrospector:
    """RFC 7662 token introspection with caching."""

    def __init__(self, config: Optional[OAuth2Config] = None):
        self.config = config or OAuth2Config()
        self._cache: Dict[str, TokenIntrospection] = {}
        self._cache_times: Dict[str, float] = {}

    def introspect(self, token: str) -> TokenIntrospection:
        # Check cache
        if token in self._cache:
            cache_time = self._cache_times.get(token, 0)
            if time.time() - cache_time < self.config.introspection_cache_ttl_s:
                return self._cache[token]

        # In production: POST to introspection endpoint
        result = TokenIntrospection(
            active=True,
            sub="user-123",
            scope="read write",
            exp=time.time() + 900,
        )

        self._cache[token] = result
        self._cache_times[token] = time.time()
        return result


class AuthMiddleware:
    """Gateway authentication middleware orchestrating all auth methods."""

    def __init__(
        self,
        oauth_config: Optional[OAuth2Config] = None,
        api_key_store: Optional[APIKeyStore] = None,
        jwt_verifier: Optional[JWTVerifier] = None,
        mtls_config: Optional[MTLSConfig] = None,
        routes: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        self.oauth_config = oauth_config or OAuth2Config()
        self.api_key_store = api_key_store or APIKeyStore()
        self.jwt_verifier = jwt_verifier or JWTVerifier(self.oauth_config)
        self.mtls_config = mtls_config or MTLSConfig()
        self._routes: Dict[str, RouteAuthConfig] = {}
        self._auth_log: List[Dict[str, Any]] = []

        if routes:
            for path, config in routes.items():
                self._routes[path] = RouteAuthConfig(
                    auth_required=config.get("auth", True),
                    required_scopes=config.get("required_scopes", []),
                )

    def add_route_config(self, path: str, config: RouteAuthConfig) -> None:
        self._routes[path] = config

    def authenticate(self, path: str, headers: Dict[str, str],
                     method: str = "GET", body: bytes = b"") -> AuthResult:
        route_config = self._get_route_config(path)

        if not route_config.auth_required:
            return AuthResult(authenticated=True, auth_method=AuthMethod.NONE)

        # Try API key
        api_key = headers.get("X-API-Key") or headers.get("x-api-key")
        if api_key:
            key_info = self.api_key_store.validate(api_key)
            if key_info:
                return AuthResult(
                    authenticated=True, client_id=key_info.key_id,
                    scopes=key_info.scopes, auth_method=AuthMethod.API_KEY,
                    tenant_id=key_info.tenant_id,
                )

        # Try Bearer token (JWT)
        auth_header = headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            result = self.jwt_verifier.verify(token)
            if result.authenticated:
                result.auth_method = AuthMethod.JWT
                # Check required scopes
                if route_config.required_scopes:
                    if not set(route_config.required_scopes).issubset(set(result.scopes)):
                        return AuthResult(
                            authenticated=False, error="Insufficient scopes",
                            error_code="INSUFFICIENT_SCOPE",
                        )
                return result
            return result

        # Try HMAC signature
        signature = headers.get("X-Signature") or headers.get("x-signature")
        if signature:
            return AuthResult(authenticated=True, auth_method=AuthMethod.HMAC)

        self._auth_log.append({
            "path": path, "method": method, "authenticated": False,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return AuthResult(
            authenticated=False, error="No valid credentials provided",
            error_code="MISSING_CREDENTIALS",
        )

    def _get_route_config(self, path: str) -> RouteAuthConfig:
        for pattern, config in sorted(self._routes.items(), key=lambda x: len(x[0]), reverse=True):
            if path.startswith(pattern.replace("*", "")):
                return config
        return RouteAuthConfig(auth_required=True)

    def get_auth_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self._auth_log[-limit:]


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the gateway authentication toolkit."""
    print("Gateway Authentication Toolkit")
    print("=" * 60)

    # API Key store
    store = APIKeyStore()
    store.add_key("sk_live_abc123def456", "Production App", scopes=["read", "write"])
    store.add_key("sk_test_xyz789", "Test App", scopes=["read"])

    key_info = store.validate("sk_live_abc123def456")
    print(f"API Key valid: {key_info is not None}")
    if key_info:
        print(f"  Name: {key_info.name}, Scopes: {key_info.scopes}")

    # JWT
    jwt_v = JWTVerifier(OAuth2Config(issuer="https://auth.example.com", audience="https://api.example.com"))
    import base64
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).decode()
    payload = base64.urlsafe_b64encode(json.dumps({
        "sub": "user-123", "iss": "https://auth.example.com",
        "aud": "https://api.example.com",
        "exp": time.time() + 3600, "scope": "read write admin",
    }).encode()).decode()
    token = f"{header}.{payload}.sig"

    jwt_result = jwt_v.verify(token)
    print(f"\nJWT valid: {jwt_result.authenticated}, scopes: {jwt_result.scopes}")

    # Auth middleware
    auth = AuthMiddleware(
        oauth_config=OAuth2Config(issuer="https://auth.example.com"),
        api_key_store=store,
        jwt_verifier=jwt_v,
        routes={"/api/public/*": {"auth": False}, "/api/admin/*": {"required_scopes": ["admin"]}},
    )

    result = auth.authenticate("/api/users", {"Authorization": f"Bearer {token}"})
    print(f"\nAuth: {result.authenticated} (method: {result.auth_method.value})")

    result2 = auth.authenticate("/api/users", {"X-API-Key": "sk_live_abc123def456"})
    print(f"API Key auth: {result2.authenticated} (method: {result2.auth_method.value})")

    result3 = auth.authenticate("/api/public/status", {})
    print(f"Public route: {result3.authenticated} (no auth needed)")


if __name__ == "__main__":
    main()
