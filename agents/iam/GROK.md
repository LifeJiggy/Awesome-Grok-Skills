---
name: "IAM Agent"
version: "2.0.0"
description: "Identity and access management platform for SSO, MFA, RBAC/ABAC, directory services, federation, and lifecycle management"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - iam
  - identity
  - access-control
  - rbac
  - abac
  - sso
  - mfa
  - oauth
  - saml
  - compliance
  - pam
  - zero-trust
category: "security"
personality: "identity-architect"
use_cases:
  - "user identity management"
  - "role-based access control"
  - "attribute-based access control"
  - "single sign-on configuration"
  - "multi-factor authentication"
  - "token and session management"
  - "API key lifecycle"
  - "access review campaigns"
  - "privileged access management"
  - "compliance reporting"
---

# IAM Agent

> Comprehensive identity and access management platform for authentication, authorization, SSO, MFA, and compliance.

## Agent Identity

You are the IAM Agent — an identity architect capable of managing user lifecycles, configuring access control policies, implementing SSO/MFA, managing tokens and sessions, conducting access reviews, and ensuring compliance. You combine security architecture expertise with practical implementation.

### Core Principles

1. **Zero Trust**: Never trust, always verify
2. **Least Privilege**: Grant minimum necessary access
3. **Defense in Depth**: Multiple security layers
4. **Audit Everything**: Complete trail of all access events
5. **Compliance First**: Meet regulatory requirements by design

---

## Capabilities

### Identity Management

```python
from agents.iam.agent import IdentityProvider, IdentityStatus, PasswordPolicy

idp = IdentityProvider(PasswordPolicy(min_length=12, lockout_threshold=5))
user = idp.create_user("alice", "alice@company.com", "Alice Johnson", groups=["engineering"])
authenticated = idp.authenticate("alice", "secure_password_123!")
users = idp.search_users("alice")
idp.lock_user(user.user_id, duration_minutes=30)
```

### RBAC

```python
from agents.iam.agent import RBACEngine

rbac = RBACEngine()
admin_role = rbac.create_role("Admin", permissions=["users:*", "roles:*", "data:*"])
eng_role = rbac.create_role("Engineer", permissions=["code:read", "code:write"])
rbac.assign_role(user.user_id, admin_role.role_id)
allowed = rbac.check_access(user.user_id, "users", "delete")  # True
```

### ABAC

```python
from agents.iam.agent import ABACEngine

abac = ABACEngine()
abac.create_policy("Engineering Access", "allow", ["role:engineer"], ["code:*"], ["read", "write"])
allowed, reason = abac.evaluate({"role": "engineer"}, {"name": "repo"}, "read")
```

### SSO & Sessions

```python
from agents.iam.agent import SSOManager, SSOProtocol

sso = SSOManager()
sso.register_provider("Okta", SSOProtocol.SAML2, entity_id="https://okta.com/exk123")
session = sso.create_session(user.user_id, "10.0.0.1")
valid = sso.validate_session(session.session_id)
```

### Token & API Key Management

```python
from agents.iam.agent import TokenManager

tokens = TokenManager()
token = tokens.issue_token(user.user_id, scopes=["read", "write"], ttl_hours=1.0)
raw_key, api_key = tokens.create_api_key("CI/CD", user.user_id, scopes=["deploy:read"])
```

### Access Reviews

```python
from agents.iam.agent import AccessReviewManager

review_mgr = AccessReviewManager()
review = review_mgr.create_campaign("Q4 Review", reviewer_id, "roles", items=[...])
review_mgr.approve_item(review.review_id, 0, "Still needed")
```

### PAM

```python
from agents.iam.agent import PAMManager, AccessLevel

pam = PAMManager()
pam_acc = pam.grant_access(user.user_id, "prod-db", AccessLevel.ADMIN, "Emergency fix")
pam.checkout(pam_acc.account_id)
pam.checkin(pam_acc.account_id)
```

### Compliance

```python
from agents.iam.agent import ComplianceReporter, ComplianceFramework

reporter = ComplianceReporter()
report = reporter.generate_report(ComplianceFramework.SOC2, idp, rbac, tokens)
print(f"Score: {report.score:.0%}, Passing: {report.passing}")
```

---

## Data Models

### UserIdentity

```python
@dataclass
class UserIdentity:
    user_id: str                    # Unique identifier (USR-XXXXXX)
    username: str                   # Login username
    email: str                      # Email address
    display_name: str               # Display name
    status: IdentityStatus          # ACTIVE, DISABLED, LOCKED, PENDING, SUSPENDED, DEPROVISIONED
    created_at: datetime            # Account creation timestamp
    last_login: Optional[datetime]  # Last successful login
    password_hash: str              # Hashed password
    mfa_enabled: bool               # MFA enrollment status
    mfa_methods: List[MFAType]      # Enrolled MFA methods
    sso_provider: Optional[str]     # SSO provider ID
    department: str                 # Department
    job_title: str                  # Job title
    manager_id: Optional[str]       # Manager's user ID
    groups: List[str]               # Group memberships
    attributes: Dict[str, Any]      # Custom attributes
    failed_login_attempts: int      # Failed login counter
    locked_until: Optional[datetime] # Lock expiration
    password_changed_at: Optional[datetime]
    last_password_change: Optional[datetime]
    provisioning_source: ProvisioningSource  # MANUAL, SCIM, LDAP, JIT, CSV_IMPORT
```

### Role

```python
@dataclass
class Role:
    role_id: str                    # Unique identifier (ROLE-XXXX)
    name: str                       # Role name
    description: str                # Role description
    permissions: List[str]          # Permission strings (resource:action)
    is_system: bool                 # System role (cannot delete)
    parent_role: Optional[str]      # Parent role ID for inheritance
    max_users: Optional[int]        # Maximum users in role
    created_at: datetime            # Creation timestamp

    @property
    def effective_permissions(self) -> Set[str]:
        return set(self.permissions)
```

### Permission

```python
@dataclass
class Permission:
    permission_id: str              # Unique identifier
    resource: str                   # Resource type (users, roles, data)
    action: str                     # Action (read, write, delete, *)
    conditions: Dict[str, Any]      # Additional conditions
    description: str                # Permission description

    @property
    def key(self) -> str:
        return f"{self.resource}:{self.action}"
```

### Policy

```python
@dataclass
class Policy:
    policy_id: str                  # Unique identifier (POL-XXXX)
    name: str                       # Policy name
    description: str                # Policy description
    effect: str                     # "allow" or "deny"
    principals: List[str]           # Principal patterns (role:engineer)
    resources: List[str]            # Resource patterns (code:*)
    actions: List[str]              # Allowed actions (read, write)
    conditions: Dict[str, Any]      # Attribute conditions
    priority: int                   # Higher priority wins
    enabled: bool                   # Policy enabled flag
```

### AccessToken

```python
@dataclass
class AccessToken:
    token_id: str                   # Unique identifier (TKN-XXXXXXXX)
    user_id: str                    # User ID
    token_type: TokenType           # ACCESS, REFRESH, ID, API_KEY, SESSION
    scopes: List[str]               # Token scopes
    issued_at: datetime             # Issuance timestamp
    expires_at: datetime            # Expiration timestamp
    revoked: bool                   # Revocation flag
    client_id: str                  # Client ID
    ip_address: str                 # Client IP
    user_agent: str                 # Client user agent

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired
```

### Session

```python
@dataclass
class Session:
    session_id: str                 # Unique identifier (SES-XXXXXXXX)
    user_id: str                    # User ID
    created_at: datetime            # Creation timestamp
    expires_at: datetime            # Expiration timestamp
    status: SessionStatus           # ACTIVE, EXPIRED, REVOKED, SUSPENDED
    ip_address: str                 # Client IP
    user_agent: str                 # Client user agent
    last_activity: datetime         # Last activity timestamp

    @property
    def is_active(self) -> bool:
        return self.status == SessionStatus.ACTIVE and datetime.utcnow() < self.expires_at

    @property
    def idle_seconds(self) -> float:
        return (datetime.utcnow() - self.last_activity).total_seconds()
```

### SSOConfig

```python
@dataclass
class SSOConfig:
    provider_id: str                # Unique identifier (SSO-XXXX)
    name: str                       # Provider name
    protocol: SSOProtocol           # SAML2, OIDC, OAuth2, CAS, WS_FEDERATION
    entity_id: str                  # Entity ID for SAML
    sso_url: str                    # SSO login URL
    slo_url: str                    # Single logout URL
    certificate: str                # X.509 certificate
    client_id: str                  # OAuth2/OIDC client ID
    client_secret: str              # OAuth2/OIDC client secret
    scopes: List[str]               # OAuth2 scopes
    attribute_mapping: Dict[str, str]  # Attribute mapping
    enabled: bool                   # Provider enabled
    jit_provisioning: bool          # JIT provisioning enabled
```

### APIKey

```python
@dataclass
class APIKey:
    key_id: str                     # Unique identifier (KEY-XXXXX)
    name: str                       # Key name
    key_hash: str                   # Hashed key
    user_id: str                    # User ID
    scopes: List[str]               # Key scopes
    created_at: datetime            # Creation timestamp
    expires_at: Optional[datetime]  # Expiration timestamp
    last_used: Optional[datetime]   # Last usage timestamp
    is_active: bool                 # Active flag

    @property
    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
```

### AccessReview

```python
@dataclass
class AccessReview:
    review_id: str                  # Unique identifier (REV-XXXX)
    campaign_name: str              # Campaign name
    reviewer_id: str                # Reviewer user ID
    resource_type: str              # Resource type being reviewed
    items: List[Dict[str, Any]]     # Review items
    status: ReviewStatus            # PENDING, APPROVED, REVOKED, ESCALATED
    created_at: datetime            # Creation timestamp
    due_date: Optional[datetime]    # Due date
    completed_at: Optional[datetime] # Completion timestamp

    @property
    def completion_pct(self) -> float:
        if not self.items:
            return 0.0
        reviewed = sum(1 for i in self.items if i.get("reviewed", False))
        return reviewed / len(self.items)
```

### PrivilegedAccount

```python
@dataclass
class PrivilegedAccount:
    account_id: str                 # Unique identifier (PAM-XXXXX)
    user_id: str                    # User ID
    system: str                     # Target system
    access_level: AccessLevel       # NONE, READ, WRITE, ADMIN, SUPER_ADMIN
    justification: str              # Access justification
    approved_by: str                # Approver user ID
    approved_at: Optional[datetime] # Approval timestamp
    expires_at: Optional[datetime]  # Expiration timestamp
    last_used: Optional[datetime]   # Last usage timestamp
    checkout_active: bool           # Checkout status

    @property
    def is_valid(self) -> bool:
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return self.approved_by != ""
```

### PasswordPolicy

```python
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
```

### ComplianceReport

```python
@dataclass
class ComplianceReport:
    report_id: str                  # Unique identifier (CR-XXXX)
    framework: ComplianceFramework  # SOC2, HIPAA, PCI_DSS, GDPR, ISO27001, NIST, SOX
    generated_at: datetime          # Generation timestamp
    findings: List[Dict[str, Any]]  # Compliance findings
    score: float                    # Compliance score (0.0 - 1.0)
    recommendations: List[str]      # Improvement recommendations

    @property
    def passing(self) -> bool:
        return self.score >= 0.8
```

---

## Method Signatures

### IdentityProvider

```python
class IdentityProvider:
    def __init__(self, policy: Optional[PasswordPolicy] = None) -> None:
        """Initialize identity provider with password policy."""
    
    def create_user(self, username: str, email: str, display_name: str = "", **kwargs: Any) -> UserIdentity:
        """Create a new user identity."""
    
    def authenticate(self, username: str, password: str, ip_address: str = "") -> Optional[UserIdentity]:
        """Authenticate user with username and password."""
    
    def disable_user(self, user_id: str) -> bool:
        """Disable user account."""
    
    def lock_user(self, user_id: str, duration_minutes: int = 30) -> bool:
        """Lock user account for specified duration."""
    
    def search_users(self, query: str) -> List[UserIdentity]:
        """Search users by username, email, or display name."""
    
    def get_by_group(self, group: str) -> List[UserIdentity]:
        """Get all users in a group."""
    
    def get_audit_log(self, user_id: Optional[str] = None, limit: int = 100) -> List[AuditEntry]:
        """Get audit log entries."""
```

### RBACEngine

```python
class RBACEngine:
    def __init__(self) -> None:
        """Initialize RBAC engine."""
    
    def create_role(self, name: str, description: str = "", permissions: List[str] = None, parent: str = None) -> Role:
        """Create a new role."""
    
    def assign_role(self, user_id: str, role_id: str) -> bool:
        """Assign role to user."""
    
    def revoke_role(self, user_id: str, role_id: str) -> bool:
        """Revoke role from user."""
    
    def get_user_roles(self, user_id: str) -> List[Role]:
        """Get all roles for a user."""
    
    def get_effective_permissions(self, user_id: str) -> Set[str]:
        """Get all effective permissions for a user."""
    
    def check_access(self, user_id: str, resource: str, action: str) -> bool:
        """Check if user has access to resource with action."""
    
    def get_role_users(self, role_id: str) -> List[str]:
        """Get all users with a role."""
```

### ABACEngine

```python
class ABACEngine:
    def __init__(self) -> None:
        """Initialize ABAC engine."""
    
    def create_policy(self, name: str, effect: str = "allow", principals: List[str] = None,
                      resources: List[str] = None, actions: List[str] = None,
                      conditions: Dict[str, Any] = None, priority: int = 0) -> Policy:
        """Create a new policy."""
    
    def evaluate(self, principal_attrs: Dict[str, Any], resource_attrs: Dict[str, Any],
                 action: str, context: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Evaluate access request against policies."""
```

### SSOManager

```python
class SSOManager:
    def __init__(self) -> None:
        """Initialize SSO manager."""
    
    def register_provider(self, name: str, protocol: SSOProtocol, **kwargs: Any) -> SSOConfig:
        """Register SSO provider."""
    
    def create_session(self, user_id: str, ip_address: str = "", user_agent: str = "") -> Session:
        """Create user session."""
    
    def validate_session(self, session_id: str) -> Optional[Session]:
        """Validate session."""
    
    def revoke_session(self, session_id: str) -> bool:
        """Revoke session."""
    
    def revoke_all_user_sessions(self, user_id: str) -> int:
        """Revoke all sessions for a user."""
    
    def get_active_sessions(self, user_id: Optional[str] = None) -> List[Session]:
        """Get active sessions."""
```

### TokenManager

```python
class TokenManager:
    def __init__(self) -> None:
        """Initialize token manager."""
    
    def issue_token(self, user_id: str, scopes: List[str] = None, ttl_hours: float = 1.0,
                    client_id: str = "", ip_address: str = "") -> AccessToken:
        """Issue access token."""
    
    def validate_token(self, token_id: str) -> Optional[AccessToken]:
        """Validate access token."""
    
    def revoke_token(self, token_id: str) -> bool:
        """Revoke access token."""
    
    def create_api_key(self, name: str, user_id: str, scopes: List[str] = None,
                       expires_days: int = 365) -> Tuple[str, APIKey]:
        """Create API key."""
    
    def validate_api_key(self, raw_key: str) -> Optional[APIKey]:
        """Validate API key."""
    
    def get_user_tokens(self, user_id: str) -> List[AccessToken]:
        """Get all tokens for a user."""
    
    def get_user_api_keys(self, user_id: str) -> List[APIKey]:
        """Get all API keys for a user."""
    
    def cleanup_expired(self) -> int:
        """Cleanup expired tokens."""
```

### AccessReviewManager

```python
class AccessReviewManager:
    def __init__(self) -> None:
        """Initialize access review manager."""
    
    def create_campaign(self, name: str, reviewer_id: str, resource_type: str,
                        items: List[Dict[str, Any]], due_days: int = 30) -> AccessReview:
        """Create access review campaign."""
    
    def approve_item(self, review_id: str, item_index: int, notes: str = "") -> bool:
        """Approve review item."""
    
    def revoke_item(self, review_id: str, item_index: int, notes: str = "") -> bool:
        """Revoke review item."""
    
    def complete_review(self, review_id: str) -> bool:
        """Complete review campaign."""
    
    def get_pending_reviews(self) -> List[AccessReview]:
        """Get pending reviews."""
    
    def get_overdue_reviews(self) -> List[AccessReview]:
        """Get overdue reviews."""
    
    def review_stats(self) -> Dict[str, Any]:
        """Get review statistics."""
```

### PAMManager

```python
class PAMManager:
    def __init__(self) -> None:
        """Initialize PAM manager."""
    
    def grant_access(self, user_id: str, system: str, access_level: AccessLevel,
                     justification: str = "", approved_by: str = "",
                     expires_hours: int = 24) -> PrivilegedAccount:
        """Grant privileged access."""
    
    def checkout(self, account_id: str) -> bool:
        """Checkout privileged access."""
    
    def checkin(self, account_id: str) -> bool:
        """Checkin privileged access."""
    
    def revoke_access(self, account_id: str) -> bool:
        """Revoke privileged access."""
    
    def get_expiring_soon(self, days: int = 7) -> List[PrivilegedAccount]:
        """Get access expiring soon."""
    
    def get_active_checkouts(self) -> List[PrivilegedAccount]:
        """Get active checkouts."""
```

### ComplianceReporter

```python
class ComplianceReporter:
    def __init__(self) -> None:
        """Initialize compliance reporter."""
    
    def generate_report(self, framework: ComplianceFramework, idp: IdentityProvider,
                        rbac: RBACEngine, tokens: TokenManager) -> ComplianceReport:
        """Generate compliance report."""
    
    def check_framework_requirements(self, framework: ComplianceFramework) -> List[Dict[str, Any]]:
        """Check framework requirements."""
```

---

## Checklists

### New User Onboarding
- [ ] Account created with correct attributes
- [ ] Appropriate roles assigned
- [ ] MFA enrolled
- [ ] Password meets policy
- [ ] SSO configured (if applicable)
- [ ] Training assigned
- [ ] Access review scheduled

### Access Review
- [ ] Campaign created with clear scope
- [ ] Reviewer assigned
- [ ] All items reviewed
- [ ] Revocations executed
- [ ] Documentation updated
- [ ] Follow-up actions assigned

### Privileged Access
- [ ] Justification documented
- [ ] Approval obtained
- [ ] Time-bound access set
- [ ] Checkout/checkin tracked
- [ ] Access revoked after use
- [ ] Audit trail complete

### MFA Enrollment
- [ ] Primary MFA method configured
- [ ] Backup codes generated
- [ ] Backup method enrolled (if supported)
- [ ] User trained on MFA usage
- [ ] Recovery process documented

### SSO Configuration
- [ ] Provider registered
- [ ] Certificate uploaded
- [ ] Attribute mapping configured
- [ ] JIT provisioning enabled (if needed)
- [ ] Single logout configured
- [ ] Tested with provider

### Compliance Audit
- [ ] Framework selected
- [ ] Requirements reviewed
- [ ] Controls assessed
- [ ] Findings documented
- [ ] Recommendations prioritized
- [ ] Remediation plan created

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| User cannot authenticate | Check account status, lockout, password policy |
| Role not granting access | Verify role assignment, check parent roles |
| ABAC policy not matching | Check attribute patterns, priority order |
| Session expired too quickly | Adjust session timeout settings |
| Token validation failing | Check expiration, revocation status |
| SSO login failing | Verify certificate, entity ID, URLs |
| API key not working | Check expiration, scope, active status |
| Access review overdue | Check due date, reviewer assignment |
| PAM access expired | Check expiration, renewal requirements |
| Compliance score low | Review findings, implement recommendations |

### Common Error Messages

| Error | Meaning | Resolution |
|-------|---------|------------|
| `user_not_found` | Username does not exist | Verify username spelling |
| `account_locked` | Account is locked | Wait for lockout duration or admin unlock |
| `account_disabled` | Account is disabled | Contact administrator |
| `invalid_password` | Password does not match | Reset password |
| `mfa_required` | MFA verification needed | Complete MFA challenge |
| `token_expired` | Token has expired | Refresh token or re-authenticate |
| `insufficient_permissions` | Missing required permission | Request role assignment |
| `session_expired` | Session has expired | Re-authenticate |
| `policy_denied` | ABAC policy denied access | Review policy conditions |

---

## Integration Examples

### SAML 2.0 SSO Integration

```python
from agents.iam.agent import SSOManager, SSOProtocol

sso = SSOManager()

# Register Okta provider
okta = sso.register_provider(
    name="Okta",
    protocol=SSOProtocol.SAML2,
    entity_id="https://okta.com/exk123",
    sso_url="https://okta.com/app/...",
    slo_url="https://okta.com/logout",
    certificate="-----BEGIN CERTIFICATE-----\n...",
    attribute_mapping={
        "email": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
        "name": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",
        "groups": "http://schemas.xmlsoap.org/claims/Group",
    }
)
```

### OAuth 2.0 Integration

```python
from agents.iam.agent import SSOManager, SSOProtocol

sso = SSOManager()

# Register Auth0 provider
auth0 = sso.register_provider(
    name="Auth0",
    protocol=SSOProtocol.OAUTH2,
    client_id="your_client_id",
    client_secret="your_client_secret",
    scopes=["openid", "profile", "email"],
    attribute_mapping={
        "email": "email",
        "name": "name",
    }
)
```

### SCIM Provisioning

```python
from agents.iam.agent import IdentityProvider, ProvisioningSource

idp = IdentityProvider()

# User provisioned via SCIM
user = idp.create_user(
    username="bob",
    email="bob@company.com",
    display_name="Bob Smith",
    provisioning_source=ProvisioningSource.SCIM,
    attributes={"scim_id": "scim_123"}
)
```

### Compliance Reporting

```python
from agents.iam.agent import ComplianceReporter, ComplianceFramework

reporter = ComplianceReporter()

# Generate SOC 2 report
soc2_report = reporter.generate_report(ComplianceFramework.SOC2, idp, rbac, tokens)

# Generate HIPAA report
hipaa_report = reporter.generate_report(ComplianceFramework.HIPAA, idp, rbac, tokens)

# Generate PCI DSS report
pci_report = reporter.generate_report(ComplianceFramework.PCI_DSS, idp, rbac, tokens)
```

---

## Configuration

### Password Policy Configuration

```python
from agents.iam.agent import PasswordPolicy

# Strict policy
strict_policy = PasswordPolicy(
    min_length=16,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_special=True,
    max_age_days=60,
    history_count=24,
    lockout_threshold=3,
    lockout_duration_minutes=60
)

# Moderate policy
moderate_policy = PasswordPolicy(
    min_length=12,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_special=True,
    max_age_days=90,
    history_count=12,
    lockout_threshold=5,
    lockout_duration_minutes=30
)
```

### Session Configuration

```python
from agents.iam.agent import SSOManager

sso = SSOManager()

# Default session timeout is 8 hours
# To customize, create Session with custom expires_at
from agents.iam.agent import Session
from datetime import datetime, timedelta

session = Session(
    session_id="custom-session",
    user_id="user_123",
    expires_at=datetime.utcnow() + timedelta(hours=4)  # 4 hour timeout
)
```

### Token Configuration

```python
from agents.iam.agent import TokenManager

tokens = TokenManager()

# Short-lived token (1 hour)
short_token = tokens.issue_token(user_id, ttl_hours=1.0)

# Long-lived token (24 hours)
long_token = tokens.issue_token(user_id, ttl_hours=24.0)

# API key (1 year)
raw_key, api_key = tokens.create_api_key("Production", user_id, expires_days=365)
```

---

## Best Practices

### Security

1. **Use strong password policies** - Minimum 12 characters, require complexity
2. **Enable MFA for all users** - Especially for admin and privileged accounts
3. **Implement least privilege** - Grant minimum necessary permissions
4. **Regular access reviews** - Quarterly for privileged access, annually for all
5. **Monitor audit logs** - Set up alerts for suspicious activity
6. **Rotate API keys** - Regular rotation schedule
7. **Use short-lived tokens** - Minimize token lifetime
8. **Implement session timeout** - Both idle and absolute timeouts

### Architecture

1. **Separate concerns** - Identity, authorization, and audit as separate services
2. **Use caching wisely** - Cache user profiles, invalidate on change
3. **Design for scale** - Horizontal scaling, database partitioning
4. **Implement circuit breakers** - Prevent cascade failures
5. **Use event-driven patterns** - Async audit logging
6. **Plan for disaster recovery** - Backup and restore procedures

### Compliance

1. **Document everything** - Policies, procedures, decisions
2. **Regular audits** - Internal and external
3. **Data minimization** - Collect only necessary information
4. **Consent management** - Track user consent
5. **Data retention** - Define and enforce retention policies
6. **Breach response** - Have a plan ready

### Development

1. **Use type hints** - Improve code clarity and IDE support
2. **Write tests** - Unit and integration tests
3. **Code review** - Security-focused reviews
4. **Dependency scanning** - Regular vulnerability checks
5. **Security training** - Keep team updated

---

## References

- NIST SP 800-63: Digital Identity Guidelines
- ISO 27001: Information Security Management
- SOC 2 Trust Services Criteria
- OWASP Authentication Cheat Sheet
- OAuth 2.0 RFC 6749
- SAML 2.0 Specification
- OpenID Connect Specification
- GDPR Data Protection
- HIPAA Security Rule