# IAM Agent

> Comprehensive identity and access management platform for authentication, authorization, SSO, MFA, RBAC/ABAC, and compliance.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Security](#security)
- [Compliance](#compliance)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The IAM Agent provides a complete identity and access management toolkit for modern applications. It implements industry-standard protocols and best practices for secure authentication, authorization, and compliance management.

### Key Capabilities

- **Identity Provider**: User lifecycle, authentication, account management
- **RBAC Engine**: Role hierarchy, permission inheritance, access checks
- **ABAC Engine**: Attribute-based policies with conditions and priorities
- **SSO Manager**: SAML/OIDC provider configuration, session management
- **Token Manager**: Access tokens, API keys, expiration management
- **Access Review Manager**: Certification campaigns, approval workflows
- **PAM Manager**: Privileged access checkout/checkin tracking
- **Compliance Reporter**: SOC2, HIPAA, PCI DSS compliance checks

### Design Principles

1. **Zero Trust**: Never trust, always verify
2. **Least Privilege**: Grant minimum necessary access
3. **Defense in Depth**: Multiple security layers
4. **Audit Everything**: Complete trail of all access events
5. **Compliance First**: Meet regulatory requirements by design

---

## Features

| Category | Capabilities |
|----------|-------------|
| Identity | User creation, authentication, account management, directory services |
| Authorization | RBAC, ABAC, policy evaluation, permission inheritance |
| SSO | SAML 2.0, OAuth 2.0, OpenID Connect, CAS, WS-Federation |
| MFA | TOTP, SMS, Email, Push, Hardware Key, Backup Codes |
| Sessions | Creation, validation, revocation, timeout management |
| Tokens | Access tokens, refresh tokens, API keys, lifecycle management |
| Access Reviews | Campaign creation, approval workflows, completion tracking |
| PAM | Privileged access grant, checkout/checkin, expiration tracking |
| Compliance | SOC2, HIPAA, PCI DSS, GDPR, ISO27001, NIST, SOX |
| Audit | Complete audit trail, logging, reporting |

---

## Quick Start

### Basic Usage

```python
from agents.iam.agent import IdentityProvider, RBACEngine, PasswordPolicy

# Create identity provider
idp = IdentityProvider(PasswordPolicy(min_length=12))

# Create user
user = idp.create_user("alice", "alice@co.com", "Alice Johnson")

# Create RBAC engine and assign role
rbac = RBACEngine()
admin = rbac.create_role("Admin", permissions=["users:*", "data:*"])
rbac.assign_role(user.user_id, admin.role_id)

# Check access
print(rbac.check_access(user.user_id, "users", "delete"))  # True
```

### Run the Agent

```bash
python agents/iam/agent.py
```

### Full Example

```python
from agents.iam.agent import (
    IdentityProvider, RBACEngine, ABACEngine, SSOManager, TokenManager,
    AccessReviewManager, PAMManager, ComplianceReporter,
    PasswordPolicy, SSOProtocol, AccessLevel, ComplianceFramework
)

# Initialize components
idp = IdentityProvider(PasswordPolicy(min_length=12, lockout_threshold=5))
rbac = RBACEngine()
abac = ABACEngine()
sso = SSOManager()
tokens = TokenManager()
review_mgr = AccessReviewManager()
pam = PAMManager()
compliance = ComplianceReporter()

# Create users
user1 = idp.create_user("alice", "alice@company.com", "Alice Johnson", groups=["engineering", "admin"])
user2 = idp.create_user("bob", "bob@company.com", "Bob Smith", groups=["engineering"])

# Create roles
admin_role = rbac.create_role("Admin", "Full access", ["users:*", "roles:*", "data:*"])
eng_role = rbac.create_role("Engineer", "Engineering access", ["code:read", "code:write", "deploy:read"])
rbac.assign_role(user1.user_id, admin_role.role_id)
rbac.assign_role(user2.user_id, eng_role.role_id)

# Create ABAC policy
abac.create_policy("Engineering Access", "allow", ["role:engineer"], ["code:*"], ["read", "write"],
                   conditions={"department": "engineering"})

# Register SSO provider
sso.register_provider("Okta", SSOProtocol.SAML2, entity_id="https://okta.com/exk123")

# Create session
session = sso.create_session(user1.user_id, "10.0.0.1")

# Issue token
token = tokens.issue_token(user1.user_id, ["read", "write"], ttl_hours=1.0)

# Create API key
raw_key, api_key = tokens.create_api_key("CI/CD", user2.user_id, ["deploy:read"])

# Create access review
review = review_mgr.create_campaign("Q4 Access Review", user1.user_id, "roles",
                                    [{"user": "bob", "role": "engineer", "reviewed": False}])
review_mgr.approve_item(review.review_id, 0, "Approved - still needed")

# Grant privileged access
pam_acc = pam.grant_access(user1.user_id, "production-db", AccessLevel.ADMIN,
                           "Emergency fix", approved_by="auto", expires_hours=4)
pam.checkout(pam_acc.account_id)

# Generate compliance report
report = compliance.generate_report(ComplianceFramework.SOC2, idp, rbac, tokens)
print(f"Compliance Score: {report.score:.0%}")
```

---

## Installation

### From Source

```bash
git clone https://github.com/awesome-grok-skills/iam-agent.git
cd iam-agent
pip install -e .
```

### Dependencies

The IAM Agent uses only Python standard library modules. No external dependencies required.

### Requirements

- Python 3.8+
- No external packages required

---

## Usage

### Identity Provider

```python
from agents.iam.agent import IdentityProvider, PasswordPolicy

idp = IdentityProvider(PasswordPolicy(min_length=12))

# Create user
user = idp.create_user("alice", "alice@company.com", "Alice Johnson")

# Authenticate
authenticated = idp.authenticate("alice", "secure_password_123!")

# Search users
users = idp.search_users("alice")

# Lock user
idp.lock_user(user.user_id, duration_minutes=30)

# Disable user
idp.disable_user(user.user_id)

# Get audit log
audit = idp.get_audit_log(user_id=user.user_id, limit=50)
```

### RBAC Engine

```python
from agents.iam.agent import RBACEngine

rbac = RBACEngine()

# Create roles
admin_role = rbac.create_role("Admin", permissions=["users:*", "roles:*", "data:*"])
eng_role = rbac.create_role("Engineer", permissions=["code:read", "code:write"])

# Assign roles
rbac.assign_role(user.user_id, admin_role.role_id)

# Check access
allowed = rbac.check_access(user.user_id, "users", "delete")  # True

# Get user roles
roles = rbac.get_user_roles(user.user_id)

# Get effective permissions
permissions = rbac.get_effective_permissions(user.user_id)

# Revoke role
rbac.revoke_role(user.user_id, admin_role.role_id)
```

### ABAC Engine

```python
from agents.iam.agent import ABACEngine

abac = ABACEngine()

# Create policy
abac.create_policy("Engineering Access", "allow", ["role:engineer"], ["code:*"], ["read", "write"])

# Evaluate access
allowed, reason = abac.evaluate(
    {"role": "engineer", "department": "engineering"},
    {"name": "repo1"},
    "read"
)
print(f"Access: {allowed}, Reason: {reason}")
```

### SSO & Sessions

```python
from agents.iam.agent import SSOManager, SSOProtocol

sso = SSOManager()

# Register provider
sso.register_provider("Okta", SSOProtocol.SAML2, entity_id="https://okta.com/exk123")

# Create session
session = sso.create_session(user.user_id, "10.0.0.1")

# Validate session
valid = sso.validate_session(session.session_id)

# Revoke session
sso.revoke_session(session.session_id)

# Revoke all user sessions
count = sso.revoke_all_user_sessions(user.user_id)

# Get active sessions
sessions = sso.get_active_sessions(user.user_id)
```

### Token & API Key Management

```python
from agents.iam.agent import TokenManager

tokens = TokenManager()

# Issue token
token = tokens.issue_token(user.user_id, scopes=["read", "write"], ttl_hours=1.0)

# Validate token
valid_token = tokens.validate_token(token.token_id)

# Revoke token
tokens.revoke_token(token.token_id)

# Create API key
raw_key, api_key = tokens.create_api_key("CI/CD", user.user_id, scopes=["deploy:read"])

# Validate API key
valid_key = tokens.validate_api_key(raw_key)

# Cleanup expired tokens
cleaned = tokens.cleanup_expired()
```

### Access Reviews

```python
from agents.iam.agent import AccessReviewManager

review_mgr = AccessReviewManager()

# Create campaign
review = review_mgr.create_campaign("Q4 Review", reviewer_id, "roles",
                                    [{"user": "bob", "role": "engineer", "reviewed": False}])

# Approve item
review_mgr.approve_item(review.review_id, 0, "Still needed")

# Revoke item
review_mgr.revoke_item(review.review_id, 1, "No longer needed")

# Complete review
review_mgr.complete_review(review.review_id)

# Get pending reviews
pending = review_mgr.get_pending_reviews()

# Get overdue reviews
overdue = review_mgr.get_overdue_reviews()

# Get stats
stats = review_mgr.review_stats()
```

### PAM

```python
from agents.iam.agent import PAMManager, AccessLevel

pam = PAMManager()

# Grant access
pam_acc = pam.grant_access(user.user_id, "prod-db", AccessLevel.ADMIN, "Emergency fix")

# Checkout
pam.checkout(pam_acc.account_id)

# Checkin
pam.checkin(pam_acc.account_id)

# Revoke
pam.revoke_access(pam_acc.account_id)

# Get expiring soon
expiring = pam.get_expiring_soon(days=7)

# Get active checkouts
checkouts = pam.get_active_checkouts()
```

### Compliance

```python
from agents.iam.agent import ComplianceReporter, ComplianceFramework

reporter = ComplianceReporter()

# Generate report
report = reporter.generate_report(ComplianceFramework.SOC2, idp, rbac, tokens)
print(f"Score: {report.score:.0%}, Passing: {report.passing}")

# Check framework requirements
requirements = reporter.check_framework_requirements(ComplianceFramework.HIPAA)
```

---

## API Reference

### IdentityProvider

| Method | Description |
|--------|-------------|
| `create_user(username, email, display_name, **kwargs)` | Create new user |
| `authenticate(username, password, ip_address)` | Authenticate user |
| `disable_user(user_id)` | Disable user account |
| `lock_user(user_id, duration_minutes)` | Lock user account |
| `search_users(query)` | Search users |
| `get_by_group(group)` | Get users in group |
| `get_audit_log(user_id, limit)` | Get audit log |

### RBACEngine

| Method | Description |
|--------|-------------|
| `create_role(name, description, permissions, parent)` | Create role |
| `assign_role(user_id, role_id)` | Assign role to user |
| `revoke_role(user_id, role_id)` | Revoke role from user |
| `get_user_roles(user_id)` | Get user roles |
| `get_effective_permissions(user_id)` | Get effective permissions |
| `check_access(user_id, resource, action)` | Check access |
| `get_role_users(role_id)` | Get role users |

### ABACEngine

| Method | Description |
|--------|-------------|
| `create_policy(name, effect, principals, resources, actions, conditions, priority)` | Create policy |
| `evaluate(principal_attrs, resource_attrs, action, context)` | Evaluate access |

### SSOManager

| Method | Description |
|--------|-------------|
| `register_provider(name, protocol, **kwargs)` | Register SSO provider |
| `create_session(user_id, ip_address, user_agent)` | Create session |
| `validate_session(session_id)` | Validate session |
| `revoke_session(session_id)` | Revoke session |
| `revoke_all_user_sessions(user_id)` | Revoke all user sessions |
| `get_active_sessions(user_id)` | Get active sessions |

### TokenManager

| Method | Description |
|--------|-------------|
| `issue_token(user_id, scopes, ttl_hours, client_id, ip_address)` | Issue token |
| `validate_token(token_id)` | Validate token |
| `revoke_token(token_id)` | Revoke token |
| `create_api_key(name, user_id, scopes, expires_days)` | Create API key |
| `validate_api_key(raw_key)` | Validate API key |
| `get_user_tokens(user_id)` | Get user tokens |
| `get_user_api_keys(user_id)` | Get user API keys |
| `cleanup_expired()` | Cleanup expired tokens |

### AccessReviewManager

| Method | Description |
|--------|-------------|
| `create_campaign(name, reviewer_id, resource_type, items, due_days)` | Create campaign |
| `approve_item(review_id, item_index, notes)` | Approve item |
| `revoke_item(review_id, item_index, notes)` | Revoke item |
| `complete_review(review_id)` | Complete review |
| `get_pending_reviews()` | Get pending reviews |
| `get_overdue_reviews()` | Get overdue reviews |
| `review_stats()` | Get review stats |

### PAMManager

| Method | Description |
|--------|-------------|
| `grant_access(user_id, system, access_level, justification, approved_by, expires_hours)` | Grant access |
| `checkout(account_id)` | Checkout access |
| `checkin(account_id)` | Checkin access |
| `revoke_access(account_id)` | Revoke access |
| `get_expiring_soon(days)` | Get expiring soon |
| `get_active_checkouts()` | Get active checkouts |

### ComplianceReporter

| Method | Description |
|--------|-------------|
| `generate_report(framework, idp, rbac, tokens)` | Generate report |
| `check_framework_requirements(framework)` | Check requirements |

---

## Configuration

### Password Policy

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
from agents.iam.agent import SSOManager, Session
from datetime import datetime, timedelta

sso = SSOManager()

# Custom session timeout
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

## Examples

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

## Architecture

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

### High-Level Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           IAM AGENT                                       │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Identity    │  │    RBAC      │  │    ABAC      │  │    SSO     │  │
│  │  Provider    │  │   Engine     │  │   Engine     │  │  Manager   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   Token      │  │   Access     │  │    PAM       │  │ Compliance │  │
│  │  Manager     │  │   Review     │  │   Manager    │  │  Reporter  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │    Data Models (User, Role, Policy, Token, Session, APIKey)      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Security

### Authentication Security

- Passwords hashed with SHA-256 (use bcrypt/argon2 in production)
- Configurable password policy (length, complexity, history)
- Account lockout after configurable threshold
- MFA support (TOTP, SMS, Email, Push, Hardware Key, Backup Codes)
- Session timeout (idle and absolute)
- Token expiration and revocation

### Authorization Security

- Role hierarchy with permission inheritance
- Attribute-based policies with conditions
- Deny-overrides in ABAC evaluation
- Wildcard permission support (resource:*, *:*)
- Audit trail for all access decisions

### Data Security

- Token encryption at rest
- API key hashing
- PHI de-identification for compliance
- Audit log immutability
- Secure session management

---

## Compliance

### Supported Frameworks

| Framework | Key Requirements |
|-----------|-----------------|
| SOC 2 | Logical access, authentication, authorization, audit |
| HIPAA | Access control, person authentication, audit controls |
| PCI DSS | Restrict access, identify users, track access |
| GDPR | Data access rights, consent management |
| ISO 27001 | Access management policy, user registration |
| NIST | Identification, authentication, authorization |
| SOX | Financial reporting controls, access management |

### Compliance Checks

```python
from agents.iam.agent import ComplianceReporter, ComplianceFramework

reporter = ComplianceReporter()

# Generate report
report = reporter.generate_report(ComplianceFramework.SOC2, idp, rbac, tokens)

# Check requirements
requirements = reporter.check_framework_requirements(ComplianceFramework.HIPAA)
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/iam-agent.git
cd iam-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

---

## License

MIT License. See [LICENSE](../../LICENSE) for details.

---

## Files

- `agent.py` — Full implementation (~1022 lines)
- `ARCHITECTURE.md` — System architecture (~900 lines)
- `GROK.md` — Agent identity and patterns (~900 lines)
- `README.md` — This file (~900 lines)

---

## Support

- Documentation: [GROK.md](GROK.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Issues: GitHub Issues
- Email: support@awesome-grok-skills.com

---

*Trust nothing, verify everything, audit always.*