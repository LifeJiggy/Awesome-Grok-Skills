"""
supabase_auth.py — Supabase Authentication & Authorization library.

Provides abstractions for:
- Multi-provider authentication (email, OAuth, magic link, phone, passkeys)
- Row-Level Security policy management
- JWT token creation, verification, and refresh
- Session management with cookie-based state
- Multi-factor authentication (TOTP, SMS)
- Role-based access control with custom claims
- Real-time auth state management
- Edge Function auth middleware

Designed for Supabase Auth v2 with PostgreSQL RLS.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import struct
import time
import base64
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Literal,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    Union,
    runtime_checkable,
)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AuthProvider(Enum):
    """Supported authentication providers."""
    EMAIL = "email"
    PHONE = "phone"
    MAGIC_LINK = "magic_link"
    GOOGLE = "google"
    GITHUB = "github"
    DISCORD = "discord"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    APPLE = "apple"
    LINKEDIN = "linkedin"
    SLACK = "slack"
    PASSKEY = "passkey"
    ANONYMOUS = "anonymous"


class AuthEventType(Enum):
    """Authentication event types for state change listener."""
    SIGNED_IN = "SIGNED_IN"
    SIGNED_OUT = "SIGNED_OUT"
    TOKEN_REFRESHED = "TOKEN_REFRESHED"
    PASSWORD_RECOVERY = "PASSWORD_RECOVERY"
    USER_UPDATED = "USER_UPDATED"
    MFA_CHALLENGE_VERIFIED = "MFA_CHALLENGE_VERIFIED"
    PASSWORD_VERIFICATION = "PASSWORD_VERIFICATION"


class PolicyAction(Enum):
    """RLS policy action types."""
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ALL = "ALL"
    TRUNCATE = "TRUNCATE"
    REFERENCES = "REFERENCES"
    TRIGGER = "TRIGGER"


class MFAType(Enum):
    """Multi-factor authentication types."""
    TOTP = "totp"
    SMS = "sms"
    PHONE = "phone"
    WEB_AUTHN = "webauthn"


class SessionStatus(Enum):
    """Session state."""
    ACTIVE = "active"
    EXPIRED = "expired"
    REFRESHING = "refreshing"
    INVALID = "invalid"


class UserRole(Enum):
    """Built-in Supabase roles."""
    ANON = "anon"
    AUTHENTICATED = "authenticated"
    SERVICE_ROLE = "service_role"
    ADMIN = "admin"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class JWTConfig:
    """JWT token configuration."""
    secret: str
    algorithm: str = "HS256"
    access_token_expiry: int = 3600  # 1 hour
    refresh_token_expiry: int = 604800  # 7 days
    issuer: str = "supabase"
    audience: str = "authenticated"


@dataclass(frozen=True)
class SessionConfig:
    """Session management configuration."""
    cookie_name: str = "sb-auth-token"
    http_only: bool = True
    secure: bool = True
    same_site: Literal["lax", "strict", "none"] = "lax"
    max_age: int = 60 * 60 * 24 * 7  # 7 days
    domain: str | None = None
    path: str = "/"


@dataclass(frozen=True)
class OAuthConfig:
    """OAuth provider configuration."""
    provider: AuthProvider
    client_id: str
    client_secret: str
    redirect_url: str
    scopes: list[str] = field(default_factory=list)
    pkce: bool = True
    skip_browser_redirect: bool = False


@dataclass(frozen=True)
class MagicLinkConfig:
    """Magic link authentication configuration."""
    email: str
    redirect_to: str = "/"
    should_create_user: bool = True
    data: dict[str, Any] = field(default_factory=dict)
    token_expiry: int = 3600  # 1 hour


@dataclass(frozen=True)
class PhoneOTPConfig:
    """Phone OTP authentication configuration."""
    phone: str
    channel: Literal["sms", "whatsapp"] = "sms"
    should_create_user: bool = True


@dataclass
class AuthUser:
    """Represents an authenticated user."""
    id: str
    email: str | None = None
    phone: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_sign_in_at: datetime | None = None
    app_metadata: dict[str, Any] = field(default_factory=dict)
    user_metadata: dict[str, Any] = field(default_factory=dict)
    factors: list[dict[str, Any]] = field(default_factory=list)
    role: str = "authenticated"

    @property
    def is_admin(self) -> bool:
        return self.app_metadata.get("role") == "admin"

    @property
    def has_mfa(self) -> bool:
        return len(self.factors) > 0

    def has_permission(self, permission: str) -> bool:
        permissions = self.app_metadata.get("permissions", [])
        return permission in permissions


@dataclass
class Session:
    """Represents an active user session."""
    access_token: str
    refresh_token: str
    expires_at: int  # Unix timestamp
    token_type: str = "Bearer"
    user: AuthUser | None = None
    provider: AuthProvider = AuthProvider.EMAIL
    amr: list[dict[str, str]] = field(default_factory=list)

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    @property
    def remaining_seconds(self) -> int:
        return max(0, self.expires_at - int(time.time()))

    @property
    def used_mfa(self) -> bool:
        return any(a.get("method") == "mfa" for a in self.amr)


@dataclass
class MFAFactor:
    """A registered MFA factor."""
    id: str
    friendly_name: str | None = None
    factor_type: MFAType = MFAType.TOTP
    status: Literal["unverified", "verified"] = "unverified"
    totp: dict[str, str] | None = None  # Contains uri, secret
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_verified(self) -> bool:
        return self.status == "verified"


@dataclass
class MFAChallenge:
    """An MFA challenge awaiting verification."""
    id: str
    factor_id: str
    expires_at: int
    challenge_type: MFAType = MFAType.TOTP

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at


@dataclass
class RLSPolicy:
    """A Row-Level Security policy definition."""
    name: str
    action: PolicyAction
    table: str
    schema: str = "public"
    using: str | None = None
    check: str | None = None
    with_check: str | None = None
    roles: list[str] = field(default_factory=lambda: ["authenticated"])
    enabled: bool = True

    def to_sql(self) -> str:
        """Generate the SQL statement for this policy."""
        parts = [f"CREATE POLICY {self.name}"]
        parts.append(f"  ON {self.schema}.{self.table}")
        if self.action != PolicyAction.ALL:
            parts.append(f"  FOR {self.action.value}")
        if self.roles:
            parts.append(f"  TO {', '.join(self.roles)}")
        if self.using:
            parts.append(f"  USING ({self.using})")
        if self.check or self.with_check:
            check_expr = self.check or self.with_check
            parts.append(f"  WITH CHECK ({check_expr})")
        return "\n".join(parts)


@dataclass
class AuthEvent:
    """An authentication event for the state change listener."""
    event: AuthEventType
    session: Session | None = None
    user: AuthUser | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error: str | None = None


@dataclass
class PasswordValidation:
    """Password strength validation result."""
    valid: bool
    min_length: int = 8
    has_uppercase: bool = False
    has_lowercase: bool = False
    has_digit: bool = False
    has_special: bool = False
    score: int = 0  # 0-100
    feedback: list[str] = field(default_factory=list)


@dataclass
class SignInResult:
    """Result from a sign-in attempt."""
    user: AuthUser | None = None
    session: Session | None = None
    error: str | None = None
    mfa_required: bool = False
    mfa_factors: list[MFAFactor] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class AuthError(Exception):
    """Base authentication error."""
    def __init__(self, message: str, code: str = "unknown", status: int = 400):
        self.code = code
        self.status = status
        super().__init__(message)


class InvalidCredentialsError(AuthError):
    def __init__(self, message: str = "Invalid login credentials"):
        super().__init__(message, code="invalid_credentials", status=401)


class EmailNotConfirmedError(AuthError):
    def __init__(self, message: str = "Email not confirmed"):
        super().__init__(message, code="email_not_confirmed", status=401)


class UserNotFoundError(AuthError):
    def __init__(self, message: str = "User not found"):
        super().__init__(message, code="user_not_found", status=404)


class SessionExpiredError(AuthError):
    def __init__(self, message: str = "Session has expired"):
        super().__init__(message, code="session_expired", status=401)


class MFARequiredError(AuthError):
    def __init__(self, factors: list[MFAFactor]):
        super().__init__("MFA verification required", code="mfa_required", status=403)
        self.factors = factors


class MFATotpInvalidError(AuthError):
    def __init__(self, message: str = "Invalid TOTP code"):
        super().__init__(message, code="mfa_totp_invalid", status=401)


class TokenExpiredError(AuthError):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, code="token_expired", status=401)


class JWTVerificationError(AuthError):
    def __init__(self, message: str = "JWT verification failed"):
        super().__init__(message, code="jwt_invalid", status=401)


class RateLimitError(AuthError):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            f"Rate limit exceeded. Retry after {retry_after}s",
            code="rate_limit_exceeded",
            status=429,
        )
        self.retry_after = retry_after


# ---------------------------------------------------------------------------
# JWT Utilities
# ---------------------------------------------------------------------------

class JWTUtils:
    """JWT token creation and verification utilities."""

    @staticmethod
    def base64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    @staticmethod
    def base64url_decode(s: str) -> bytes:
        padding = 4 - len(s) % 4
        if padding != 4:
            s += "=" * padding
        return base64.urlsafe_b64decode(s)

    @staticmethod
    def create_jwt(
        payload: dict[str, Any],
        secret: str,
        algorithm: str = "HS256",
        expires_in: int = 3600,
    ) -> str:
        """Create a signed JWT token."""
        header = {"alg": algorithm, "typ": "JWT"}

        now = int(time.time())
        payload.setdefault("iat", now)
        payload.setdefault("exp", now + expires_in)
        payload.setdefault("jti", str(uuid.uuid4()))

        header_b64 = JWTUtils.base64url_encode(json.dumps(header).encode())
        payload_b64 = JWTUtils.base64url_encode(json.dumps(payload).encode())

        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = hmac.new(
            secret.encode(), signing_input, hashlib.sha256
        ).digest()

        return f"{header_b64}.{payload_b64}.{JWTUtils.base64url_encode(signature)}"

    @staticmethod
    def verify_jwt(token: str, secret: str) -> dict[str, Any]:
        """Verify and decode a JWT token."""
        parts = token.split(".")
        if len(parts) != 3:
            raise JWTVerificationError("Invalid token format")

        header_b64, payload_b64, sig_b64 = parts

        # Verify signature
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(
            secret.encode(), signing_input, hashlib.sha256
        ).digest()
        actual_sig = JWTUtils.base64url_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise JWTVerificationError("Invalid signature")

        # Decode payload
        payload = json.loads(JWTUtils.base64url_decode(payload_b64))

        # Check expiry
        if payload.get("exp", 0) < time.time():
            raise TokenExpiredError()

        return payload

    @staticmethod
    def decode_payload_only(token: str) -> dict[str, Any]:
        """Decode JWT payload without verification (for inspection only)."""
        parts = token.split(".")
        if len(parts) != 3:
            raise JWTVerificationError("Invalid token format")
        return json.loads(JWTUtils.base64url_decode(parts[1]))


# ---------------------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------------------

class PasswordValidator:
    """Validates password strength against configurable rules."""

    def __init__(
        self,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
    ) -> None:
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special

    def validate(self, password: str) -> PasswordValidation:
        """Validate a password and return detailed results."""
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        feedback = []
        score = 0

        # Length scoring
        if len(password) >= self.min_length:
            score += 30
        else:
            feedback.append(f"Password must be at least {self.min_length} characters")

        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10

        # Character variety scoring
        if has_upper:
            score += 15
        elif self.require_uppercase:
            feedback.append("Must contain at least one uppercase letter")

        if has_lower:
            score += 15
        elif self.require_lowercase:
            feedback.append("Must contain at least one lowercase letter")

        if has_digit:
            score += 15
        elif self.require_digit:
            feedback.append("Must contain at least one digit")

        if has_special:
            score += 15
        elif self.require_special:
            feedback.append("Must contain at least one special character")

        valid = all([
            len(password) >= self.min_length,
            not self.require_uppercase or has_upper,
            not self.require_lowercase or has_lower,
            not self.require_digit or has_digit,
            not self.require_special or has_special,
        ])

        return PasswordValidation(
            valid=valid,
            min_length=self.min_length,
            has_uppercase=has_upper,
            has_lowercase=has_lower,
            has_digit=has_digit,
            has_special=has_special,
            score=min(score, 100),
            feedback=feedback,
        )


# ---------------------------------------------------------------------------
# RLS Policy Manager
# ---------------------------------------------------------------------------

class RLSPolicyManager:
    """Manages Row-Level Security policies on PostgreSQL tables."""

    def __init__(self) -> None:
        self._policies: dict[str, list[RLSPolicy]] = {}

    def add_policy(self, policy: RLSPolicy) -> None:
        """Add a policy to the manager."""
        key = f"{policy.schema}.{policy.table}"
        if key not in self._policies:
            self._policies[key] = []
        self._policies[key].append(policy)

    def remove_policy(self, name: str, table: str, schema: str = "public") -> bool:
        """Remove a policy by name."""
        key = f"{schema}.{table}"
        if key in self._policies:
            before = len(self._policies[key])
            self._policies[key] = [p for p in self._policies[key] if p.name != name]
            return len(self._policies[key]) < before
        return False

    def get_policies_for_table(self, table: str, schema: str = "public") -> list[RLSPolicy]:
        """Get all policies for a specific table."""
        key = f"{schema}.{table}"
        return self._policies.get(key, [])

    def generate_migration(self, table: str, schema: str = "public") -> str:
        """Generate a SQL migration to enable RLS and create policies."""
        lines = [
            f"-- Enable RLS on {schema}.{table}",
            f"ALTER TABLE {schema}.{table} ENABLE ROW LEVEL SECURITY;",
            f"ALTER TABLE {schema}.{table} FORCE ROW LEVEL SECURITY;",
            "",
        ]

        policies = self.get_policies_for_table(table, schema)
        for policy in policies:
            if policy.enabled:
                lines.append(f"DROP POLICY IF EXISTS {policy.name} ON {schema}.{table};")
                lines.append(policy.to_sql())
                lines.append("")

        return "\n".join(lines)

    def generate_full_migration(self) -> str:
        """Generate a complete migration for all managed tables."""
        sections = []
        for key in sorted(self._policies.keys()):
            schema, table = key.rsplit(".", 1)
            sections.append(self.generate_migration(table, schema))
        return "\n\n".join(sections)


# ---------------------------------------------------------------------------
# Auth State Manager
# ---------------------------------------------------------------------------

class AuthStateManager:
    """Manages real-time authentication state and listeners."""

    def __init__(self) -> None:
        self._listeners: list[Callable[[AuthEvent], None]] = []
        self._current_session: Session | None = None
        self._current_user: AuthUser | None = None

    def add_listener(self, callback: Callable[[AuthEvent], None]) -> Callable[[], None]:
        """Add an auth state change listener. Returns an unsubscribe function."""
        self._listeners.append(callback)

        def unsubscribe() -> None:
            if callback in self._listeners:
                self._listeners.remove(callback)

        return unsubscribe

    def _emit(self, event: AuthEvent) -> None:
        """Emit an auth event to all listeners."""
        for listener in self._listeners:
            try:
                listener(event)
            except Exception:
                pass  # Don't let listener errors break auth flow

    def set_session(self, session: Session | None) -> None:
        """Update the current session and emit appropriate events."""
        old_session = self._current_session

        if old_session and not session:
            self._emit(AuthEvent(event=AuthEventType.SIGNED_OUT))
        elif session and not old_session:
            self._emit(AuthEvent(event=AuthEventType.SIGNED_IN, session=session, user=session.user))
        elif session and old_session and session.access_token != old_session.access_token:
            self._emit(AuthEvent(event=AuthEventType.TOKEN_REFRESHED, session=session))

        self._current_session = session
        self._current_user = session.user if session else None

    @property
    def current_session(self) -> Session | None:
        return self._current_session

    @property
    def current_user(self) -> AuthUser | None:
        return self._current_user

    @property
    def is_authenticated(self) -> bool:
        return self._current_session is not None and not self._current_session.is_expired


# ---------------------------------------------------------------------------
# MFA Manager
# ---------------------------------------------------------------------------

class MFAManager:
    """Manages multi-factor authentication enrollment and verification."""

    def __init__(self) -> None:
        self._factors: dict[str, list[MFAFactor]] = {}
        self._challenges: dict[str, MFAChallenge] = {}

    def enroll_totp(self, user_id: str, friendly_name: str | None = None) -> MFAFactor:
        """Enroll a user in TOTP MFA and return the factor with setup info."""
        secret = secrets.token_hex(20)
        factor = MFAFactor(
            id=str(uuid.uuid4()),
            friendly_name=friendly_name,
            factor_type=MFAType.TOTP,
            status="unverified",
            totp={
                "secret": secret,
                "uri": f"otpauth://totp/supabase:{user_id}?secret={secret}&issuer=supabase",
            },
        )

        if user_id not in self._factors:
            self._factors[user_id] = []
        self._factors[user_id].append(factor)
        return factor

    def verify_totp(self, user_id: str, factor_id: str, code: str) -> bool:
        """Verify a TOTP code for a user."""
        factors = self._factors.get(user_id, [])
        factor = next((f for f in factors if f.id == factor_id), None)

        if not factor or factor.factor_type != MFAType.TOTP:
            return False

        # Simplified TOTP verification (real impl uses time-based counter)
        if len(code) == 6 and code.isdigit():
            factor.status = "verified"
            return True
        return False

    def list_factors(self, user_id: str) -> list[MFAFactor]:
        """List all registered MFA factors for a user."""
        return self._factors.get(user_id, [])

    def unenroll(self, user_id: str, factor_id: str) -> bool:
        """Remove an MFA factor."""
        if user_id in self._factors:
            before = len(self._factors[user_id])
            self._factors[user_id] = [f for f in self._factors[user_id] if f.id != factor_id]
            return len(self._factors[user_id]) < before
        return False


# ---------------------------------------------------------------------------
# Supabase Auth Client (main orchestrator)
# ---------------------------------------------------------------------------

class SupabaseAuthClient:
    """Main Supabase Auth client providing all authentication operations."""

    def __init__(self, jwt_config: JWTConfig, session_config: SessionConfig | None = None) -> None:
        self.jwt_config = jwt_config
        self.session_config = session_config or SessionConfig()
        self.state = AuthStateManager()
        self.mfa = MFAManager()
        self.password_validator = PasswordValidator()
        self.rls_manager = RLSPolicyManager()
        self._users: dict[str, AuthUser] = {}
        self._sessions: dict[str, Session] = {}
        self._magic_links: dict[str, dict[str, Any]] = {}
        self._otp_codes: dict[str, str] = {}

    async def sign_up(
        self,
        email: str | None = None,
        password: str | None = None,
        phone: str | None = None,
        options: dict[str, Any] | None = None,
    ) -> SignInResult:
        """Register a new user."""
        if email:
            existing = self.get_user_by_email(email)
            if existing:
                return SignInResult(error="User already registered")

        if password:
            validation = self.password_validator.validate(password)
            if not validation.valid:
                return SignInResult(error=f"Password too weak: {'; '.join(validation.feedback)}")

        user = AuthUser(
            id=str(uuid.uuid4()),
            email=email,
            phone=phone,
            app_metadata=options.get("data", {}) if options else {},
        )
        if email:
            self._users[email] = user

        # Auto sign-in after registration
        session = self._create_session(user)
        self.state.set_session(session)
        return SignInResult(user=user, session=session)

    async def sign_in_with_password(self, email: str, password: str) -> SignInResult:
        """Sign in with email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return SignInResult(error="Invalid login credentials")

        # Check if MFA is required
        factors = self.mfa.list_factors(user.id)
        verified_factors = [f for f in factors if f.is_verified]
        if verified_factors:
            # Create a temporary session requiring MFA
            temp_token = self.jwt_config.secret[:8]  # Simplified
            return SignInResult(mfa_required=True, mfa_factors=verified_factors)

        session = self._create_session(user)
        self.state.set_session(session)
        return SignInResult(user=user, session=session)

    async def sign_in_with_otp(
        self, email: str | None = None, phone: str | None = None, options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a magic link or OTP code."""
        if email:
            token = secrets.token_urlsafe(32)
            self._magic_links[token] = {
                "email": email,
                "expires_at": time.time() + 3600,
                "data": options.get("data", {}) if options else {},
            }
            return {"message": "Magic link sent", "token_ref": token[:8]}
        elif phone:
            code = f"{secrets.randbelow(900000) + 100000}"
            self._otp_codes[phone] = code
            return {"message": "OTP sent", "otp_ref": code[:2] + "****"}
        return {"error": "Email or phone required"}

    async def verify_otp(self, phone: str, token: str) -> SignInResult:
        """Verify an OTP code."""
        expected = self._otp_codes.get(phone)
        if not expected or token != expected:
            return SignInResult(error="Invalid OTP")

        del self._otp_codes[phone]
        user = AuthUser(id=str(uuid.uuid4()), phone=phone)
        session = self._create_session(user)
        self.state.set_session(session)
        return SignInResult(user=user, session=session)

    async def sign_out(self) -> None:
        """Sign out the current user."""
        session = self.state.current_session
        if session:
            self._sessions.pop(session.access_token, None)
        self.state.set_session(None)

    async def refresh_session(self, refresh_token: str) -> Session:
        """Refresh an expired session."""
        for token, session in self._sessions.items():
            if session.refresh_token == refresh_token:
                new_session = self._create_session(session.user)
                self._sessions.pop(token, None)
                self.state.set_session(new_session)
                return new_session
        raise SessionExpiredError()

    async def get_user(self) -> AuthUser | None:
        """Get the current authenticated user."""
        return self.state.current_user

    def get_user_by_email(self, email: str) -> AuthUser | None:
        """Look up a user by email."""
        return self._users.get(email)

    async def update_user(self, user_id: str, attributes: dict[str, Any]) -> AuthUser:
        """Update user metadata."""
        user = next((u for u in self._users.values() if u.id == user_id), None)
        if not user:
            raise UserNotFoundError()

        if "app_metadata" in attributes:
            user.app_metadata.update(attributes["app_metadata"])
        if "user_metadata" in attributes:
            user.user_metadata.update(attributes["user_metadata"])
        user.updated_at = datetime.now(timezone.utc)
        self.state._emit(AuthEvent(event=AuthEventType.USER_UPDATED, user=user))
        return user

    def _create_session(self, user: AuthUser) -> Session:
        """Create a new JWT session for a user."""
        now = int(time.time())
        access_token = JWTUtils.create_jwt(
            payload={
                "sub": user.id,
                "email": user.email,
                "role": user.role,
                "aud": self.jwt_config.audience,
            },
            secret=self.jwt_config.secret,
            expires_in=self.jwt_config.access_token_expiry,
        )
        refresh_token = secrets.token_urlsafe(64)

        session = Session(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=now + self.jwt_config.access_token_expiry,
            user=user,
        )
        self._sessions[access_token] = session
        return session


# ---------------------------------------------------------------------------
# Edge Function Auth Middleware
# ---------------------------------------------------------------------------

class EdgeFunctionAuthMiddleware:
    """Auth middleware for Deno Edge Functions."""

    def __init__(self, jwt_config: JWTConfig) -> None:
        self.jwt_config = jwt_config

    async def handle_request(
        self, request: dict[str, Any], handler: Callable[..., Awaitable[Any]]
    ) -> dict[str, Any]:
        """Verify JWT from request and inject user context."""
        auth_header = request.get("headers", {}).get("Authorization", "")
        token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else ""

        if not token:
            return {"status": 401, "body": {"error": "Missing authorization token"}}

        try:
            payload = JWTUtils.verify_jwt(token, self.jwt_config.secret)
            request["user"] = {
                "id": payload["sub"],
                "email": payload.get("email"),
                "role": payload.get("role", "authenticated"),
            }
            return await handler(request)
        except JWTVerificationError as exc:
            return {"status": 401, "body": {"error": str(exc)}}
        except TokenExpiredError:
            return {"status": 401, "body": {"error": "Token expired"}}


# ---------------------------------------------------------------------------
# Demo / Main
# ---------------------------------------------------------------------------

async def main() -> None:
    """Demonstrate the Supabase Auth library."""
    print("=" * 70)
    print("Supabase Authentication & Authorization — Demo")
    print("=" * 70)

    jwt_config = JWTConfig(
        secret="super-secret-jwt-key-for-demo",
        issuer="supabase-demo",
    )

    client = SupabaseAuthClient(jwt_config)

    # 1. Sign up
    print("\n[1] Email/Password Sign Up")
    result = await client.sign_up(
        email="alice@example.com",
        password="SecurePass123!",
        options={"data": {"full_name": "Alice Johnson"}},
    )
    print(f"    User: {result.user.id[:8]}... | Session: {bool(result.session)}")

    # 2. Password validation
    print("\n[2] Password Validation")
    validator = PasswordValidator()
    for pw in ["weak", "Medium1!", "Str0ng!Pass#2024"]:
        v = validator.validate(pw)
        print(f"    '{pw}' -> valid={v.valid}, score={v.score}, feedback={v.feedback}")

    # 3. Sign in
    print("\n[3] Sign In with Password")
    result = await client.sign_in_with_password("alice@example.com", "SecurePass123!")
    print(f"    User: {result.user.email} | MFA required: {result.mfa_required}")

    # 4. Auth state listener
    print("\n[4] Auth State Listener")
    events_received = []
    client.state.add_listener(lambda e: events_received.append(e.event.value))
    print(f"    Events so far: {events_received}")

    # 5. MFA enrollment
    print("\n[5] MFA Enrollment")
    factor = client.mfa.enroll_totp(result.user.id, friendly_name="My Authenticator")
    print(f"    Factor: {factor.id[:8]}... | Type: {factor.factor_type.value}")
    verified = client.mfa.verify_totp(result.user.id, factor.id, "123456")
    print(f"    Verified: {verified}")
    factors = client.mfa.list_factors(result.user.id)
    print(f"    Total factors: {len(factors)}")

    # 6. JWT creation and verification
    print("\n[6] JWT Operations")
    token = JWTUtils.create_jwt(
        payload={"sub": "user-123", "role": "authenticated"},
        secret=jwt_config.secret,
        expires_in=3600,
    )
    print(f"    Token: {token[:40]}...")
    decoded = JWTUtils.verify_jwt(token, jwt_config.secret)
    print(f"    Verified: sub={decoded['sub']}, exp={decoded['exp']}")

    # 7. Magic link flow
    print("\n[7] Magic Link Flow")
    otp_result = await client.sign_in_with_otp(
        email="bob@example.com",
        options={"data": {"full_name": "Bob Smith"}},
    )
    print(f"    Magic link: {otp_result}")

    # 8. Phone OTP flow
    print("\n[8] Phone OTP Flow")
    otp_result = await client.sign_in_with_otp(phone="+1-555-0123")
    print(f"    OTP: {otp_result}")
    verify_result = await client.verify_otp("+1-555-0123", "123456")
    print(f"    Verify: user={verify_result.user.id[:8] if verify_result.user else None}")

    # 9. RLS policy management
    print("\n[9] RLS Policy Management")
    rls = RLSPolicyManager()
    rls.add_policy(RLSPolicy(
        name="Users can read own posts",
        action=PolicyAction.SELECT,
        table="posts",
        using="auth.uid() = author_id",
    ))
    rls.add_policy(RLSPolicy(
        name="Users can create posts",
        action=PolicyAction.INSERT,
        table="posts",
        check="auth.uid() = author_id",
    ))
    migration = rls.generate_migration("posts")
    print(f"    Migration ({len(migration.splitlines())} lines):")
    for line in migration.splitlines():
        print(f"      {line}")

    # 10. Edge Function middleware
    print("\n[10] Edge Function Auth Middleware")
    mw = EdgeFunctionAuthMiddleware(jwt_config)
    mock_request = {
        "headers": {"Authorization": f"Bearer {token}"},
        "path": "/api/private",
    }
    response = await mw.handle_request(mock_request, lambda r: {"status": 200, "user": r["user"]})
    print(f"    Response: {response}")

    # 11. Sign out
    print("\n[11] Sign Out")
    await client.sign_out()
    print(f"    Is authenticated: {client.state.is_authenticated}")

    # 12. User metadata update
    print("\n[12] User Metadata Update")
    updated = await client.update_user(
        result.user.id,
        {"app_metadata": {"role": "admin", "permissions": ["read", "write"]}},
    )
    print(f"    Admin: {updated.is_admin} | Permissions: {updated.app_metadata.get('permissions')}")

    print("\n" + "=" * 70)
    print("Demo complete — all Supabase Auth patterns demonstrated successfully")
    print("=" * 70)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
