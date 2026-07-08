"""
IAM Agent — Identity and Access Management, SSO, MFA, RBAC/ABAC,
directory services, federation, and lifecycle management.

This module provides comprehensive IAM tools including:
- User identity management and directory services
- Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC)
- Single Sign-On (SSO) configuration and management
- Multi-Factor Authentication (MFA) enrollment and verification
- OAuth 2.0 / OpenID Connect provider management
- SAML federation and trust configuration
- API key and service account management
- Access review and certification campaigns
- Privileged Access Management (PAM)
- Compliance reporting and audit trails
- Password policy enforcement
- Session management and token lifecycle
"""

from __future__ import annotations

import hashlib
import logging
import secrets
import string
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AuthMethod(Enum):
    PASSWORD = "password"
    MFA = "mfa"
    SSO = "sso"
    SAML = "saml"
    OAUTH2 = "oauth2"
    OPENID_CONNECT = "openid_connect"
    API_KEY = "api_key"
    CERTIFICATE = "certificate"
    BIOMETRIC = "biometric"

class MFAType(Enum):
    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    HARDWARE_KEY = "hardware_key"
    BACKUP_CODES = "backup_codes"

class IdentityStatus(Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LOCKED = "locked"
    PENDING = "pending"
    SUSPENDED = "suspended"
    DEPROVISIONED = "deprovisioned"

class AccessLevel(Enum):
    NONE = 0
    READ = 1
    WRITE = 2
    ADMIN = 3
    SUPER_ADMIN = 4

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    ID = "id"
    API_KEY = "api_key"
    SESSION = "session"

class SSOProtocol(Enum):
    SAML2 = "saml2"
    OIDC = "oidc"
    OAUTH2 = "oauth2"
    CAS = "cas"
    WS_FEDERATION = "ws_federation"

class ProvisioningSource(Enum):
    MANUAL = "manual"
    SCIM = "scim"
    LDAP = "ldap"
    JIT = "jit"
    CSV_IMPORT = "csv_import"

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REVOKED = "revoked"
    ESCALATED = "escalated"

class ComplianceFramework(Enum):
    SOC2 = "soc2"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    ISO27001 = "iso27001"
    NIST = "nist"
    SOX = "sox"

class SessionStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUSPENDED = "suspended"

class PasswordStrength(Enum):
    VERY_WEAK = 0
    WEAK = 1
    FAIR = 2
    STRONG = 3
    VERY_STRONG = 4

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class UserIdentity:
    user_id: str
    username: str
    email: str
    display_name: str = ""
    status: IdentityStatus = IdentityStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    password_hash: str = ""
    mfa_enabled: bool = False
    mfa_methods: List[MFAType] = field(default_factory=list)
    sso_provider: Optional[str] = None
    department: str = ""
    job_title: str = ""
    manager_id: Optional[str] = None
    groups: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None
    last_password_change: Optional[datetime] = None
    provisioning_source: ProvisioningSource = ProvisioningSource.MANUAL

    @property
    def is_active(self) -> bool:
        return self.status == IdentityStatus.ACTIVE

    @property
    def is_locked(self) -> bool:
        if not self.locked_until:
            return False
        if datetime.utcnow() < self.locked_until:
            return True
        self.locked_until = None
        return False

    @property
    def days_since_password_change(self) -> Optional[int]:
        if not self.last_password_change:
            return None
        return (datetime.utcnow() - self.last_password_change).days

    @property
    def password_expired(self) -> bool:
        days = self.days_since_password_change
        return days is not None and days > 90

    @property
    def has_mfa(self) -> bool:
        return self.mfa_enabled and len(self.mfa_methods) > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id, "username": self.username, "email": self.email,
            "status": self.status.value, "mfa_enabled": self.mfa_enabled,
            "groups": self.groups, "department": self.department,
        }

@dataclass
class Role:
    role_id: str
    name: str
    description: str = ""
    permissions: List[str] = field(default_factory=list)
    is_system: bool = False
    parent_role: Optional[str] = None
    max_users: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def effective_permissions(self) -> Set[str]:
        return set(self.permissions)

@dataclass
class Permission:
    permission_id: str
    resource: str
    action: str
    conditions: Dict[str, Any] = field(default_factory=dict)
    description: str = ""

    @property
    def key(self) -> str:
        return f"{self.resource}:{self.action}"

@dataclass
class Policy:
    policy_id: str
    name: str
    description: str = ""
    effect: str = "allow"  # allow, deny
    principals: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    enabled: bool = True

    @property
    def matches(self) -> bool:
        return bool(self.principals and self.resources and self.actions)

@dataclass
class AccessToken:
    token_id: str
    user_id: str
    token_type: TokenType = TokenType.ACCESS
    scopes: List[str] = field(default_factory=list)
    issued_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=1))
    revoked: bool = False
    client_id: str = ""
    ip_address: str = ""
    user_agent: str = ""

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired

    @property
    def remaining_seconds(self) -> float:
        remaining = (self.expires_at - datetime.utcnow()).total_seconds()
        return max(remaining, 0)

@dataclass
class Session:
    session_id: str
    user_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=8))
    status: SessionStatus = SessionStatus.ACTIVE
    ip_address: str = ""
    user_agent: str = ""
    last_activity: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_active(self) -> bool:
        return self.status == SessionStatus.ACTIVE and datetime.utcnow() < self.expires_at

    @property
    def idle_seconds(self) -> float:
        return (datetime.utcnow() - self.last_activity).total_seconds()

@dataclass
class SSOConfig:
    provider_id: str
    name: str
    protocol: SSOProtocol = SSOProtocol.SAML2
    entity_id: str = ""
    sso_url: str = ""
    slo_url: str = ""
    certificate: str = ""
    client_id: str = ""
    client_secret: str = ""
    scopes: List[str] = field(default_factory=list)
    attribute_mapping: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True
    jit_provisioning: bool = False

@dataclass
class APIKey:
    key_id: str
    name: str
    key_hash: str = ""
    user_id: str = ""
    scopes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool = True

    @property
    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

@dataclass
class AccessReview:
    review_id: str
    campaign_name: str
    reviewer_id: str = ""
    resource_type: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    status: ReviewStatus = ReviewStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def completion_pct(self) -> float:
        if not self.items:
            return 0.0
        reviewed = sum(1 for i in self.items if i.get("reviewed", False))
        return reviewed / len(self.items)

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status == ReviewStatus.PENDING

@dataclass
class PrivilegedAccount:
    account_id: str
    user_id: str
    system: str = ""
    access_level: AccessLevel = AccessLevel.ADMIN
    justification: str = ""
    approved_by: str = ""
    approved_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    checkout_active: bool = False

    @property
    def is_valid(self) -> bool:
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return self.approved_by != ""

    @property
    def requires_renewal(self) -> bool:
        if not self.expires_at:
            return False
        return (self.expires_at - datetime.utcnow()).days < 7

@dataclass
class PasswordPolicy:
    min_length: int = 12
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_special: bool = True
    max_age_days: int = 90
    history_count: int = 12
    lockout_threshold: int = 5
    lockout_duration_minutes: int = 30

    def check_strength(self, password: str) -> PasswordStrength:
        score = 0
        if len(password) >= self.min_length:
            score += 1
        if self.require_uppercase and any(c.isupper() for c in password):
            score += 1
        if self.require_lowercase and any(c.islower() for c in password):
            score += 1
        if self.require_digits and any(c.isdigit() for c in password):
            score += 1
        if self.require_special and any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        return PasswordStrength(min(score, 4))

    def validate(self, password: str) -> Tuple[bool, List[str]]:
        errors = []
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")
        if self.require_uppercase and not any(c.isupper() for c in password):
            errors.append("Must contain uppercase letter")
        if self.require_lowercase and not any(c.islower() for c in password):
            errors.append("Must contain lowercase letter")
        if self.require_digits and not any(c.isdigit() for c in password):
            errors.append("Must contain digit")
        if self.require_special and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Must contain special character")
        return len(errors) == 0, errors

@dataclass
class AuditEntry:
    entry_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_type: str = ""  # login, logout, access_grant, access_revoke, mfa_setup, password_change
    user_id: str = ""
    resource: str = ""
    action: str = ""
    outcome: str = "success"  # success, failure, denied
    ip_address: str = ""
    details: str = ""

@dataclass
class ComplianceReport:
    report_id: str
    framework: ComplianceFramework = ComplianceFramework.SOC2
    generated_at: datetime = field(default_factory=datetime.utcnow)
    findings: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    recommendations: List[str] = field(default_factory=list)

    @property
    def passing(self) -> bool:
        return self.score >= 0.8

# ---------------------------------------------------------------------------
# Identity Provider
# ---------------------------------------------------------------------------

class IdentityProvider:
    """Core identity management and authentication."""

    def __init__(self, policy: Optional[PasswordPolicy] = None) -> None:
        self.users: Dict[str, UserIdentity] = {}
        self.policy = policy or PasswordPolicy()
        self._user_counter = 0
        self.audit_log: List[AuditEntry] = []
        self._audit_counter = 0

    def create_user(self, username: str, email: str, display_name: str = "", **kwargs: Any) -> UserIdentity:
        self._user_counter += 1
        user_id = kwargs.pop("user_id", f"USR-{self._user_counter:06d}")
        user = UserIdentity(user_id=user_id, username=username, email=email,
                            display_name=display_name or username, **kwargs)
        self.users[user_id] = user
        self._log_event("user_created", user_id=user_id)
        return user

    def authenticate(self, username: str, password: str, ip_address: str = "") -> Optional[UserIdentity]:
        user = self._find_by_username(username)
        if not user:
            self._log_event("login_failed", details=f"user={username} reason=not_found", ip_address=ip_address)
            return None
        if user.is_locked:
            self._log_event("login_failed", user_id=user.user_id, details="account_locked", ip_address=ip_address)
            return None
        if not user.is_active:
            self._log_event("login_failed", user_id=user.user_id, details="account_disabled", ip_address=ip_address)
            return None
        valid, _ = self.policy.validate(password)
        if not valid or not self._verify_password(password, user.password_hash):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= self.policy.lockout_threshold:
                user.locked_until = datetime.utcnow() + timedelta(minutes=self.policy.lockout_duration_minutes)
                self._log_event("account_locked", user_id=user.user_id, ip_address=ip_address)
            self._log_event("login_failed", user_id=user.user_id, ip_address=ip_address)
            return None
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        self._log_event("login_success", user_id=user.user_id, ip_address=ip_address)
        return user

    def disable_user(self, user_id: str) -> bool:
        if user_id not in self.users:
            return False
        self.users[user_id].status = IdentityStatus.DISABLED
        self._log_event("user_disabled", user_id=user_id)
        return True

    def lock_user(self, user_id: str, duration_minutes: int = 30) -> bool:
        if user_id not in self.users:
            return False
        self.users[user_id].status = IdentityStatus.LOCKED
        self.users[user_id].locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self._log_event("user_locked", user_id=user_id)
        return True

    def search_users(self, query: str) -> List[UserIdentity]:
        q = query.lower()
        return [u for u in self.users.values()
                if q in u.username.lower() or q in u.email.lower() or q in u.display_name.lower()]

    def get_by_group(self, group: str) -> List[UserIdentity]:
        return [u for u in self.users.values() if group in u.groups]

    def _find_by_username(self, username: str) -> Optional[UserIdentity]:
        for u in self.users.values():
            if u.username.lower() == username.lower():
                return u
        return None

    def _verify_password(self, password: str, password_hash: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == password_hash

    def _log_event(self, event_type: str, user_id: str = "", details: str = "", ip_address: str = "") -> None:
        self._audit_counter += 1
        self.audit_log.append(AuditEntry(
            entry_id=f"AUD-{self._audit_counter:06d}", event_type=event_type,
            user_id=user_id, details=details, ip_address=ip_address))

    def get_audit_log(self, user_id: Optional[str] = None, limit: int = 100) -> List[AuditEntry]:
        log = self.audit_log if not user_id else [e for e in self.audit_log if e.user_id == user_id]
        return sorted(log, key=lambda e: e.timestamp, reverse=True)[:limit]

# ---------------------------------------------------------------------------
# RBAC Engine
# ---------------------------------------------------------------------------

class RBACEngine:
    """Role-Based Access Control engine."""

    def __init__(self) -> None:
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, Set[str]] = defaultdict(set)
        self.role_hierarchy: Dict[str, str] = {}
        self._role_counter = 0

    def create_role(self, name: str, description: str = "", permissions: List[str] = None, parent: str = None) -> Role:
        self._role_counter += 1
        role = Role(role_id=f"ROLE-{self._role_counter:04d}", name=name, description=description,
                    permissions=permissions or [], parent_role=parent)
        self.roles[role.role_id] = role
        return role

    def assign_role(self, user_id: str, role_id: str) -> bool:
        if role_id not in self.roles:
            return False
        self.user_roles[user_id].add(role_id)
        return True

    def revoke_role(self, user_id: str, role_id: str) -> bool:
        if role_id in self.user_roles.get(user_id, set()):
            self.user_roles[user_id].discard(role_id)
            return True
        return False

    def get_user_roles(self, user_id: str) -> List[Role]:
        return [self.roles[rid] for rid in self.user_roles.get(user_id, set()) if rid in self.roles]

    def get_effective_permissions(self, user_id: str) -> Set[str]:
        permissions = set()
        for role in self.get_user_roles(user_id):
            permissions |= role.effective_permissions
            if role.parent_role and role.parent_role in self.roles:
                permissions |= self.roles[role.parent_role].effective_permissions
        return permissions

    def check_access(self, user_id: str, resource: str, action: str) -> bool:
        perms = self.get_effective_permissions(user_id)
        if f"{resource}:*" in perms or f"*:*" in perms:
            return True
        return f"{resource}:{action}" in perms

    def get_role_users(self, role_id: str) -> List[str]:
        return [uid for uid, roles in self.user_roles.items() if role_id in roles]

# ---------------------------------------------------------------------------
# ABAC Engine
# ---------------------------------------------------------------------------

class ABACEngine:
    """Attribute-Based Access Control engine."""

    def __init__(self) -> None:
        self.policies: List[Policy] = []
        self._policy_counter = 0

    def create_policy(self, name: str, effect: str = "allow", principals: List[str] = None,
                      resources: List[str] = None, actions: List[str] = None,
                      conditions: Dict[str, Any] = None, priority: int = 0) -> Policy:
        self._policy_counter += 1
        policy = Policy(policy_id=f"POL-{self._policy_counter:04d}", name=name, effect=effect,
                        principals=principals or [], resources=resources or [],
                        actions=actions or [], conditions=conditions or {}, priority=priority)
        self.policies.append(policy)
        return policy

    def evaluate(self, principal_attrs: Dict[str, Any], resource_attrs: Dict[str, Any],
                 action: str, context: Dict[str, Any] = None) -> Tuple[bool, str]:
        context = context or {}
        matching = []
        for policy in sorted(self.policies, key=lambda p: p.priority, reverse=True):
            if not policy.enabled:
                continue
            if self._matches_policy(policy, principal_attrs, resource_attrs, action, context):
                matching.append(policy)
        if not matching:
            return False, "no_matching_policy"
        for policy in matching:
            if policy.effect == "deny":
                return False, f"denied_by:{policy.name}"
        return True, f"allowed_by:{matching[0].name}"

    def _matches_policy(self, policy: Policy, principal: Dict[str, Any],
                        resource: Dict[str, Any], action: str, context: Dict[str, Any]) -> bool:
        if policy.actions and action not in policy.actions:
            return False
        if policy.principals:
            matched = any(self._match_attribute(p, principal) for p in policy.principals)
            if not matched:
                return False
        if policy.resources:
            matched = any(self._match_attribute(r, resource) for r in policy.resources)
            if not matched:
                return False
        for key, expected in policy.conditions.items():
            actual = context.get(key, principal.get(key, resource.get(key)))
            if actual != expected:
                return False
        return True

    def _match_attribute(self, pattern: str, attrs: Dict[str, Any]) -> bool:
        if "*" in pattern:
            return True
        if ":" in pattern:
            key, value = pattern.split(":", 1)
            return str(attrs.get(key, "")) == value
        return pattern in attrs.values()

# ---------------------------------------------------------------------------
# SSO Manager
# ---------------------------------------------------------------------------

class SSOManager:
    """Single Sign-On configuration and session management."""

    def __init__(self) -> None:
        self.providers: Dict[str, SSOConfig] = {}
        self.sessions: Dict[str, Session] = {}
        self._session_counter = 0

    def register_provider(self, name: str, protocol: SSOProtocol, **kwargs: Any) -> SSOConfig:
        provider_id = f"SSO-{len(self.providers) + 1:04d}"
        config = SSOConfig(provider_id=provider_id, name=name, protocol=protocol, **kwargs)
        self.providers[provider_id] = config
        return config

    def create_session(self, user_id: str, ip_address: str = "", user_agent: str = "") -> Session:
        self._session_counter += 1
        session = Session(session_id=f"SES-{self._session_counter:08d}", user_id=user_id,
                          ip_address=ip_address, user_agent=user_agent)
        self.sessions[session.session_id] = session
        return session

    def validate_session(self, session_id: str) -> Optional[Session]:
        session = self.sessions.get(session_id)
        if session and session.is_active:
            session.last_activity = datetime.utcnow()
            return session
        return None

    def revoke_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            self.sessions[session_id].status = SessionStatus.REVOKED
            return True
        return False

    def revoke_all_user_sessions(self, user_id: str) -> int:
        count = 0
        for session in self.sessions.values():
            if session.user_id == user_id and session.is_active:
                session.status = SessionStatus.REVOKED
                count += 1
        return count

    def get_active_sessions(self, user_id: Optional[str] = None) -> List[Session]:
        sessions = [s for s in self.sessions.values() if s.is_active]
        if user_id:
            sessions = [s for s in sessions if s.user_id == user_id]
        return sessions

# ---------------------------------------------------------------------------
# Token Manager
# ---------------------------------------------------------------------------

class TokenManager:
    """Access token and API key management."""

    def __init__(self) -> None:
        self.tokens: Dict[str, AccessToken] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self._token_counter = 0
        self._key_counter = 0

    def issue_token(self, user_id: str, scopes: List[str] = None, ttl_hours: float = 1.0,
                    client_id: str = "", ip_address: str = "") -> AccessToken:
        self._token_counter += 1
        token = AccessToken(
            token_id=f"TKN-{self._token_counter:08d}", user_id=user_id,
            scopes=scopes or [], client_id=client_id, ip_address=ip_address,
            expires_at=datetime.utcnow() + timedelta(hours=ttl_hours))
        self.tokens[token.token_id] = token
        return token

    def validate_token(self, token_id: str) -> Optional[AccessToken]:
        token = self.tokens.get(token_id)
        if token and token.is_valid:
            return token
        return None

    def revoke_token(self, token_id: str) -> bool:
        if token_id in self.tokens:
            self.tokens[token_id].revoked = True
            return True
        return False

    def create_api_key(self, name: str, user_id: str, scopes: List[str] = None,
                       expires_days: int = 365) -> Tuple[str, APIKey]:
        self._key_counter += 1
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        api_key = APIKey(
            key_id=f"KEY-{self._key_counter:05d}", name=name, key_hash=key_hash,
            user_id=user_id, scopes=scopes or [],
            expires_at=datetime.utcnow() + timedelta(days=expires_days))
        self.api_keys[api_key.key_id] = api_key
        return raw_key, api_key

    def validate_api_key(self, raw_key: str) -> Optional[APIKey]:
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        for key in self.api_keys.values():
            if key.key_hash == key_hash and key.is_active and not key.is_expired:
                key.last_used = datetime.utcnow()
                return key
        return None

    def get_user_tokens(self, user_id: str) -> List[AccessToken]:
        return [t for t in self.tokens.values() if t.user_id == user_id]

    def get_user_api_keys(self, user_id: str) -> List[APIKey]:
        return [k for k in self.api_keys.values() if k.user_id == user_id]

    def cleanup_expired(self) -> int:
        expired = [tid for tid, t in self.tokens.items() if t.is_expired]
        for tid in expired:
            del self.tokens[tid]
        return len(expired)

# ---------------------------------------------------------------------------
# Access Review
# ---------------------------------------------------------------------------

class AccessReviewManager:
    """Access review and certification campaigns."""

    def __init__(self) -> None:
        self.reviews: Dict[str, AccessReview] = {}
        self._review_counter = 0

    def create_campaign(self, name: str, reviewer_id: str, resource_type: str,
                        items: List[Dict[str, Any]], due_days: int = 30) -> AccessReview:
        self._review_counter += 1
        review = AccessReview(
            review_id=f"REV-{self._review_counter:04d}", campaign_name=name,
            reviewer_id=reviewer_id, resource_type=resource_type, items=items,
            due_date=datetime.utcnow() + timedelta(days=due_days))
        self.reviews[review.review_id] = review
        return review

    def approve_item(self, review_id: str, item_index: int, notes: str = "") -> bool:
        if review_id not in self.reviews:
            return False
        review = self.reviews[review_id]
        if 0 <= item_index < len(review.items):
            review.items[item_index]["reviewed"] = True
            review.items[item_index]["decision"] = "approved"
            review.items[item_index]["notes"] = notes
            return True
        return False

    def revoke_item(self, review_id: str, item_index: int, notes: str = "") -> bool:
        if review_id not in self.reviews:
            return False
        review = self.reviews[review_id]
        if 0 <= item_index < len(review.items):
            review.items[item_index]["reviewed"] = True
            review.items[item_index]["decision"] = "revoked"
            review.items[item_index]["notes"] = notes
            return True
        return False

    def complete_review(self, review_id: str) -> bool:
        if review_id not in self.reviews:
            return False
        self.reviews[review_id].status = ReviewStatus.APPROVED
        self.reviews[review_id].completed_at = datetime.utcnow()
        return True

    def get_pending_reviews(self) -> List[AccessReview]:
        return [r for r in self.reviews.values() if r.status == ReviewStatus.PENDING]

    def get_overdue_reviews(self) -> List[AccessReview]:
        return [r for r in self.reviews.values() if r.is_overdue]

    def review_stats(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        for r in self.reviews.values():
            by_status[r.status.value] += 1
        return {"total": len(self.reviews), "by_status": dict(by_status),
                "overdue": len(self.get_overdue_reviews())}

# ---------------------------------------------------------------------------
# PAM Manager
# ---------------------------------------------------------------------------

class PAMManager:
    """Privileged Access Management."""

    def __init__(self) -> None:
        self.accounts: Dict[str, PrivilegedAccount] = {}
        self._counter = 0

    def grant_access(self, user_id: str, system: str, access_level: AccessLevel,
                     justification: str = "", approved_by: str = "",
                     expires_hours: int = 24) -> PrivilegedAccount:
        self._counter += 1
        account = PrivilegedAccount(
            account_id=f"PAM-{self._counter:05d}", user_id=user_id, system=system,
            access_level=access_level, justification=justification,
            approved_by=approved_by, approved_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=expires_hours))
        self.accounts[account.account_id] = account
        return account

    def checkout(self, account_id: str) -> bool:
        if account_id not in self.accounts:
            return False
        self.accounts[account_id].checkout_active = True
        self.accounts[account_id].last_used = datetime.utcnow()
        return True

    def checkin(self, account_id: str) -> bool:
        if account_id not in self.accounts:
            return False
        self.accounts[account_id].checkout_active = False
        return True

    def revoke_access(self, account_id: str) -> bool:
        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        return False

    def get_expiring_soon(self, days: int = 7) -> List[PrivilegedAccount]:
        cutoff = datetime.utcnow() + timedelta(days=days)
        return [a for a in self.accounts.values() if a.expires_at and a.expires_at <= cutoff]

    def get_active_checkouts(self) -> List[PrivilegedAccount]:
        return [a for a in self.accounts.values() if a.checkout_active]

# ---------------------------------------------------------------------------
# Compliance Reporter
# ---------------------------------------------------------------------------

class ComplianceReporter:
    """IAM compliance reporting and audit."""

    def __init__(self) -> None:
        self.reports: List[ComplianceReport] = []

    def generate_report(self, framework: ComplianceFramework, idp: IdentityProvider,
                        rbac: RBACEngine, tokens: TokenManager) -> ComplianceReport:
        findings = []
        recommendations = []

        # Check password policy
        weak_users = sum(1 for u in idp.users.values()
                         if u.last_password_change and (datetime.utcnow() - u.last_password_change).days > 90)
        if weak_users > 0:
            findings.append({"check": "password_age", "status": "warning", "count": weak_users})
            recommendations.append("Enforce password rotation for stale accounts")

        # Check MFA
        no_mfa = sum(1 for u in idp.users.values() if u.is_active and not u.mfa_enabled)
        if no_mfa > 0:
            findings.append({"check": "mfa_coverage", "status": "fail", "count": no_mfa})
            recommendations.append("Enable MFA for all active users")

        # Check locked accounts
        locked = sum(1 for u in idp.users.values() if u.is_locked)
        if locked > 0:
            findings.append({"check": "locked_accounts", "status": "info", "count": locked})

        # Check orphaned roles
        all_roles = set(rbac.roles.keys())
        used_roles = set()
        for roles in rbac.user_roles.values():
            used_roles |= roles
        orphaned = all_roles - used_roles
        if orphaned:
            findings.append({"check": "orphaned_roles", "status": "warning", "count": len(orphaned)})
            recommendations.append("Remove unused roles")

        # Check expired tokens
        expired = sum(1 for t in tokens.tokens.values() if t.is_expired)
        if expired > 0:
            findings.append({"check": "expired_tokens", "status": "info", "count": expired})

        total = len(findings)
        passed = sum(1 for f in findings if f["status"] in ("pass", "info"))
        score = passed / total if total > 0 else 1.0

        report = ComplianceReport(report_id=f"CR-{len(self.reports)+1:04d}", framework=framework,
                                  findings=findings, score=score, recommendations=recommendations)
        self.reports.append(report)
        return report

    def check_framework_requirements(self, framework: ComplianceFramework) -> List[Dict[str, Any]]:
        requirements = {
            ComplianceFramework.SOC2: [
                {"id": "CC6.1", "name": "Logical Access Controls", "status": "required"},
                {"id": "CC6.2", "name": "Authentication", "status": "required"},
                {"id": "CC6.3", "name": "Authorization", "status": "required"},
                {"id": "CC6.6", "name": "Boundary Protection", "status": "required"},
            ],
            ComplianceFramework.HIPAA: [
                {"id": "164.312(a)(1)", "name": "Access Control", "status": "required"},
                {"id": "164.312(d)", "name": "Person Authentication", "status": "required"},
                {"id": "164.312(b)", "name": "Audit Controls", "status": "required"},
            ],
            ComplianceFramework.PCI_DSS: [
                {"id": "Req 7", "name": "Restrict Access", "status": "required"},
                {"id": "Req 8", "name": "Identify Users", "status": "required"},
                {"id": "Req 10", "name": "Track Access", "status": "required"},
            ],
        }
        return requirements.get(framework, [])

# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("IAM Agent - Comprehensive Demo")
    print("=" * 60)

    # Identity Provider
    idp = IdentityProvider(PasswordPolicy(min_length=12, lockout_threshold=3))
    user1 = idp.create_user("alice", "alice@company.com", "Alice Johnson", groups=["engineering", "admin"])
    user2 = idp.create_user("bob", "bob@company.com", "Bob Smith", groups=["engineering"])
    user3 = idp.create_user("carol", "carol@company.com", "Carol Williams", groups=["hr"])
    print(f"\nUsers created: {len(idp.users)}")

    # RBAC
    rbac = RBACEngine()
    admin_role = rbac.create_role("Admin", "Full access", ["users:*", "roles:*", "data:*"])
    eng_role = rbac.create_role("Engineer", "Engineering access", ["code:read", "code:write", "deploy:read"])
    rbac.assign_role(user1.user_id, admin_role.role_id)
    rbac.assign_role(user2.user_id, eng_role.role_id)
    print(f"Roles: {len(rbac.roles)}")
    print(f"Admin check: {rbac.check_access(user1.user_id, 'users', 'delete')}")
    print(f"Engineer admin check: {rbac.check_access(user2.user_id, 'users', 'delete')}")

    # ABAC
    abac = ABACEngine()
    abac.create_policy("Engineering Access", "allow", ["role:engineer"], ["code:*"], ["read", "write"],
                       conditions={"department": "engineering"})
    allowed, reason = abac.evaluate({"role": "engineer", "department": "engineering"}, {"name": "repo1"}, "read")
    print(f"ABAC check: {allowed} ({reason})")

    # SSO
    sso = SSOManager()
    sso.register_provider("Okta", SSOProtocol.SAML2, entity_id="https://okta.com/exk123")
    session = sso.create_session(user1.user_id, "10.0.0.1")
    valid = sso.validate_session(session.session_id)
    print(f"Session valid: {valid is not None}")

    # Tokens
    tokens = TokenManager()
    token = tokens.issue_token(user1.user_id, ["read", "write"], ttl_hours=1.0)
    valid_token = tokens.validate_token(token.token_id)
    print(f"Token valid: {valid_token is not None}")
    raw_key, api_key = tokens.create_api_key("CI/CD", user2.user_id, ["deploy:read"])
    print(f"API key created: {api_key.key_id}")

    # Access Review
    review_mgr = AccessReviewManager()
    review = review_mgr.create_campaign("Q4 Access Review", user1.user_id, "roles",
                                         [{"user": "bob", "role": "engineer", "reviewed": False}])
    review_mgr.approve_item(review.review_id, 0, "Approved - still needed")
    print(f"Review completion: {review.completion_pct:.0%}")

    # PAM
    pam = PAMManager()
    pam_acc = pam.grant_access(user1.user_id, "production-db", AccessLevel.ADMIN,
                               "Emergency fix", approved_by="auto", expires_hours=4)
    pam.checkout(pam_acc.account_id)
    print(f"PAM active checkouts: {len(pam.get_active_checkouts())}")

    # Compliance
    compliance = ComplianceReporter()
    report = compliance.generate_report(ComplianceFramework.SOC2, idp, rbac, tokens)
    print(f"\nCompliance ({report.framework.value}): score={report.score:.0%}, passing={report.passing}")
    for finding in report.findings:
        print(f"  {finding['check']}: {finding['status']}")
    for rec in report.recommendations:
        print(f"  Recommendation: {rec}")

    # Audit Log
    audit = idp.get_audit_log(limit=5)
    print(f"\nAudit log ({len(audit)} entries):")
    for entry in audit[:3]:
        print(f"  {entry.event_type}: {entry.details or entry.user_id}")

    print("\n" + "=" * 60)
    print("IAM Agent demo complete.")
    print("=" * 60)
