---
name: "Security Hardening"
version: "2.0.0"
description: "Comprehensive database security hardening toolkit with authentication configuration, encryption management, access control, audit logging, vulnerability scanning, and compliance verification for production databases"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database-admin", "security", "encryption", "access-control", "audit", "compliance"]
category: "database-admin"
personality: "security-engineer"
use_cases: ["authentication setup", "encryption management", "access control", "audit logging", "compliance verification"]
---

# Security Hardening

> Production-grade database security framework providing authentication configuration, encryption management, access control, audit logging, vulnerability scanning, and compliance verification for hardened database deployments.

## Overview

The Security Hardening module provides a complete toolkit for securing database deployments against common attack vectors. It implements authentication method configuration (password, certificate, Kerberos), encryption at rest and in transit, role-based access control with least-privilege enforcement, comprehensive audit logging, vulnerability scanning, and compliance verification against standards like CIS, PCI-DSS, and SOC2. Every configuration includes rollback capability and change tracking.

## Core Capabilities

### 1. Authentication Configuration
- Password authentication with complexity rules
- Certificate-based authentication (mTLS)
- Kerberos/AD integration
- LDAP authentication
- Password rotation policies
- Account lockout configuration

### 2. Encryption Management
- TLS/SSL configuration for connections
- Encryption at rest (TDE) setup
- Key management and rotation
- Column-level encryption
- Backup encryption verification

### 3. Access Control
- Role-based access control (RBAC)
- Least-privilege enforcement
- Schema-level permissions
- Row-level security policies
- Column-level permissions
- Privilege escalation detection

### 4. Audit Logging
- DDL change tracking
- DML change tracking
- Login attempt logging
- Privilege change tracking
- Data access logging
- Audit log retention and rotation

### 5. Vulnerability Scanning
- Default credential detection
- Open port scanning
- Configuration weakness detection
- Outdated version detection
- Missing patch identification

### 6. Compliance Verification
- CIS benchmark checks
- PCI-DSS requirements
- SOC2 control verification
- GDPR data discovery
- HIPAA compliance checks

## Usage Examples

### Authentication Setup

```python
from security_hardening import AuthenticationManager, AuthMethod

auth = AuthenticationManager(connection_string="postgresql://admin:pass@localhost/postgres")

# Configure password policy
auth.configure_password_policy(
    min_length=12,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_special=True,
    max_age_days=90,
    history_count=5,
)

# Enable certificate authentication
auth.enable_certificate_auth(
    ca_cert="/etc/ssl/ca.pem",
    client_cert_required=True,
    crl_check=True,
)

# Set up account lockout
auth.configure_lockout(
    max_attempts=5,
    lockout_duration_minutes=30,
    reset_attempts_after_minutes=15,
)
```

### Encryption Configuration

```python
from security_hardening import EncryptionManager

encryption = EncryptionManager(connection_string="postgresql://admin:pass@localhost/postgres")

# Configure TLS for connections
encryption.configure_tls(
    cert_file="/etc/ssl/server.pem",
    key_file="/etc/ssl/server.key",
    ca_file="/etc/ssl/ca.pem",
    min_protocol="TLSv1.2",
    ciphers="HIGH:!aNULL:!MD5",
)

# Enable encryption at rest
encryption.enable_encryption_at_rest(
    algorithm="aes-256",
    key_rotation_days=90,
)

# Verify encryption status
status = encryption.get_encryption_status()
print(f"TLS active: {status.tls_active}")
print(f"At-rest encrypted: {status.at_rest_encrypted}")
print(f"Backup encrypted: {status.backup_encrypted}")
```

### Audit Logging

```python
from security_hardening import AuditManager

audit = AuditManager(connection_string="postgresql://admin:pass@localhost/postgres")

# Configure audit logging
audit.configure(
    log_ddl=True,
    log_dml=False,  # High volume — enable selectively
    log_logins=True,
    log_privileges=True,
    log_connections=True,
    retention_days=365,
)

# Query audit logs
logs = audit.get_recent_logs(
    hours=24,
    event_type="login",
    limit=100,
)

print(f"Audit events: {len(logs)}")
for log in logs[:5]:
    print(f"  {log.timestamp}: {log.event_type} by {log.user} - {log.detail}")
```

### Compliance Verification

```python
from security_hardening import ComplianceChecker

checker = ComplianceChecker(connection_string="postgresql://admin:pass@localhost/postgres")

# Run CIS benchmark checks
cis_results = checker.check_cis_benchmark()
print(f"CIS checks: {cis_results.total_checks}")
print(f"Passed: {cis_results.passed}")
print(f"Failed: {cis_results.failed}")
print(f"Score: {cis_results.score:.1f}%")

# Run PCI-DSS checks
pci_results = checker.check_pci_dss()
for check in pci_results.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"  [{status}] {check.description}")

# Run SOC2 checks
soc2_results = checker.check_soc2()
print(f"SOC2 score: {soc2_results.score:.1f}%")
```

## Best Practices

### Authentication
- Never use password authentication over unencrypted connections
- Enforce password complexity and rotation policies
- Use certificate-based authentication for service accounts
- Implement account lockout after failed attempts

### Encryption
- Enable TLS for all database connections (minimum TLSv1.2)
- Encrypt sensitive data at rest using TDE or column-level encryption
- Rotate encryption keys regularly (every 90 days minimum)
- Verify backup encryption before storing offsite

### Access Control
- Follow the principle of least privilege
- Use role-based access control (RBAC)
- Regularly review and audit user privileges
- Remove unused accounts and roles
- Implement row-level security for multi-tenant data

### Audit Logging
- Enable logging for all DDL changes
- Log all login attempts (success and failure)
- Retain audit logs for at least 1 year
- Monitor audit logs for suspicious activity

### Compliance
- Run CIS benchmark checks quarterly
- Address critical findings within 30 days
- Document all security configurations
- Maintain evidence for compliance audits

## Related Modules

- **db-management**: Database configuration and lifecycle
- **backup-recovery**: Backup encryption and security
- **monitoring**: Security event monitoring and alerting
- **performance-tuning**: Security configurations that may impact performance

---

## Advanced Configuration

### Advanced Authentication

```python
from security_hardening import AuthenticationManager, AuthMethod, CertificateConfig

auth = AuthenticationManager(connection_string="postgresql://admin:pass@localhost/postgres")

# Configure multi-factor authentication
auth.configure_mfa(
    methods=["password", "certificate"],
    password_policy={
        "min_length": 16,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_digits": True,
        "require_special": True,
        "max_age_days": 90,
        "history_count": 12,
        "complexity_check": True,
    },
    certificate_config=CertificateConfig(
        ca_cert="/etc/ssl/ca.pem",
        client_cert_required=True,
        crl_check=True,
        crl_file="/etc/ssl/crl.pem",
        ocsp_enabled=True,
        ocsp_responder="http://ocsp.example.com",
    ),
)

# Configure LDAP/AD integration
auth.configure_ldap(
    server="ldap://ldap.example.com",
    base_dn="dc=example,dc=com",
    bind_dn="cn=admin,dc=example,dc=com",
    bind_password_env="LDAP_PASSWORD",
    user_search_filter="(uid={username})",
    group_search_filter="(memberUid={username})",
    use_tls=True,
    tls_reqcert="demand",
)

# Configure Kerberos
auth.configure_kerberos(
    realm="EXAMPLE.COM",
    kdc="kdc.example.com",
    keytab="/etc/krb5.keytab",
    service_principal="postgres/db.example.com@EXAMPLE.COM",
)
```

### Advanced Encryption

```python
from security_hardening import EncryptionManager, KeyManager

encryption = EncryptionManager(connection_string="postgresql://admin:pass@localhost/postgres")

# Configure comprehensive encryption
encryption.configure(
    # TLS configuration
    tls=TLSConfig(
        cert_file="/etc/ssl/server.pem",
        key_file="/etc/ssl/server.key",
        ca_file="/etc/ssl/ca.pem",
        min_protocol="TLSv1.3",
        ciphers="TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256",
        prefer_server_ciphers=True,
        session_tickets=False,
    ),
    
    # Encryption at rest
    encryption_at_rest=EncryptionAtRestConfig(
        enabled=True,
        algorithm="AES-256-GCM",
        key_provider="aws-kms",
        key_arn="arn:aws:kms:us-east-1:123456:key/abc-123",
        rotation_enabled=True,
        rotation_interval_days=90,
    ),
    
    # Column-level encryption
    column_encryption=ColumnEncryptionConfig(
        enabled=True,
        encrypted_columns={
            "users.ssn": {"algorithm": "aes-256-gcm", "key_id": "ssn-key"},
            "users.email": {"algorithm": "aes-256-gcm", "key_id": "email-key"},
            "payments.card_number": {"algorithm": "aes-256-gcm", "key_id": "payment-key"},
        },
    ),
)

# Key management
key_manager = KeyManager()
key_manager.configure(
    provider="aws-kms",
    master_key_arn="arn:aws:kms:us-east-1:123456:key/master",
    automatic_rotation=True,
    rotation_period_days=90,
    key_deletion_days=30,
)
```

### Advanced Access Control

```python
from security_hardening import AccessControlManager, RBACPolicy

access = AccessControlManager(connection_string="postgresql://admin:pass@localhost/postgres")

# Configure comprehensive RBAC
rbac = RBACPolicy(
    roles=[
        {
            "name": "db_admin",
            "privileges": ["ALL"],
            "inherit": True,
            "superuser": True,
        },
        {
            "name": "app_readonly",
            "privileges": ["CONNECT", "SELECT"],
            "schemas": ["public", "app"],
            "tables": {"public": ["*"], "app": ["*"]},
        },
        {
            "name": "app_readwrite",
            "privileges": ["CONNECT", "SELECT", "INSERT", "UPDATE", "DELETE"],
            "schemas": ["app"],
            "tables": {"app": ["orders", "products", "customers"]},
        },
    ],
    row_level_security={
        "orders": "organization_id = current_setting('app.org_id')::uuid",
        "customers": "organization_id = current_setting('app.org_id')::uuid",
    },
    column_permissions={
        "users": {
            "ssn": ["admin", "hr"],
            "email": ["admin", "support"],
        },
    },
)

access.configure_rbac(rbac)
```

## Architecture Patterns

### Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Architecture                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Authentication Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Password   │  │ Certificate │  │  Kerberos   │ │   │
│  │  │  Auth       │  │  Auth       │  │  Auth       │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Authorization Layer                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │    RBAC     │  │   Row-Level  │  │   Column-   │ │   │
│  │  │             │  │   Security   │  │   Level     │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Encryption Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  TLS/SSL    │  │  At-Rest    │  │  Column     │ │   │
│  │  │  Transit    │  │  Encryption │  │  Encryption │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Audit Layer                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  DDL Audit  │  │  DML Audit  │  │  Login      │ │   │
│  │  │             │  │             │  │  Audit      │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Defense in Depth

```
┌─────────────────────────────────────────────────────────────┐
│                   Defense in Depth                          │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Network Security                                 │
│  └─► Firewall, VPC, Security Groups                        │
│                                                             │
│  Layer 2: Transport Security                                │
│  └─► TLS 1.3, mTLS, Certificate Pinning                    │
│                                                             │
│  Layer 3: Authentication                                    │
│  └─► Strong passwords, MFA, Certificate Auth                │
│                                                             │
│  Layer 4: Authorization                                     │
│  └─► RBAC, Least Privilege, Row/Column Security             │
│                                                             │
│  Layer 5: Data Protection                                   │
│  └─► Encryption at Rest, Column Encryption                  │
│                                                             │
│  Layer 6: Audit & Monitoring                                │
│  └─► Comprehensive Logging, Alerting, Anomaly Detection     │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with FastAPI
from fastapi import FastAPI, Depends, Security
from fastapi.security import HTTPBearer
from security_hardening import AuthenticationManager, AccessControlManager

app = FastAPI()
security = HTTPBearer()
auth = AuthenticationManager(connection_string=connection_string)
access = AccessControlManager(connection_string=connection_string)

async def get_current_user(token: str = Security(security)):
    user = await auth.verify_token(token.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/admin/users")
async def list_users(user = Depends(get_current_user)):
    # Check permission
    if not await access.check_permission(user, "users", "SELECT"):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return await conn.execute("SELECT * FROM users")
```

### Monitoring Integration

```python
# Integration with SIEM
from security_hardening import AuditLogger, SIEMExporter

audit = AuditLogger(connection_string=connection_string)
siem = SIEMExporter()

# Export audit logs to SIEM
audit_logs = audit.get_recent_logs(hours=24)
for log in audit_logs:
    siem.export_event(
        event_type=log.event_type,
        user=log.user,
        timestamp=log.timestamp,
        details=log.details,
        severity=log.severity,
    )
```

## Performance Optimization

### Security Performance Impact

| Feature | CPU Impact | I/O Impact | Memory Impact |
|---------|------------|------------|---------------|
| TLS 1.3 | 1-2% | 0% | 0% |
| Audit Logging (DDL) | 0.5% | 1% | 0.5% |
| Audit Logging (DML) | 5-10% | 5-10% | 2% |
| Row-Level Security | 2-5% | 0% | 1% |
| Column Encryption | 3-5% | 2% | 1% |
| Encryption at Rest | 1-3% | 1% | 0% |

### Optimized Security Configuration

```python
from security_hardening import PerformanceOptimizedSecurity

optimizer = PerformanceOptimizedSecurity()

# Configure security with minimal performance impact
config = optimizer.optimize(
    tls_version="1.3",
    audit_level="ddl",  # DDL only, not DML
    rls_enabled=True,
    column_encryption=False,  # Disabled for performance
    at_rest_encryption=True,
)

print(f"Estimated performance impact: {config.estimated_overhead:.1f}%")
```

## Security Considerations

### Security Checklist

- [ ] TLS enabled for all connections (minimum TLSv1.2)
- [ ] Strong password policy enforced
- [ ] Account lockout configured
- [ ] RBAC implemented with least privilege
- [ ] Audit logging enabled for DDL changes
- [ ] Encryption at rest enabled
- [ ] Backup encryption verified
- [ ] Unused accounts removed
- [ ] Default credentials changed
- [ ] Network access restricted

### Vulnerability Scanning

```python
from security_hardening import VulnerabilityScanner

scanner = VulnerabilityScanner(connection_string=connection_string)

# Run comprehensive security scan
results = scanner.scan()
print(f"Security score: {results.score:.1f}%")
print(f"Critical issues: {results.critical_count}")
print(f"High issues: {results.high_count}")
print(f"Medium issues: {results.medium_count}")

for issue in results.issues:
    print(f"\n  [{issue.severity}] {issue.title}")
    print(f"    Description: {issue.description}")
    print(f"    Recommendation: {issue.recommendation}")
    print(f"    Reference: {issue.reference}")
```

### Compliance Verification

```python
from security_hardening import ComplianceChecker

checker = ComplianceChecker(connection_string=connection_string)

# Check PCI-DSS compliance
pci = checker.check_pci_dss()
print(f"PCI-DSS score: {pci.score:.1f}%")
for control in pci.controls:
    status = "PASS" if control.passed else "FAIL"
    print(f"  [{status}] {control.requirement}: {control.description}")

# Check SOC2 compliance
soc2 = checker.check_soc2()
print(f"\nSOC2 score: {soc2.score:.1f}%")

# Check GDPR compliance
gdpr = checker.check_gdpr()
print(f"\nGDPR score: {gdpr.score:.1f}%")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| TLS errors | Connection refused | Check certificate validity, protocol version |
| Auth failures | Login rejected | Verify credentials, check lockout status |
| Permission denied | Access error | Check role assignments, RLS policies |
| Audit gaps | Missing audit entries | Verify audit configuration, check log rotation |
| Key rotation | Encryption errors | Verify key access, check rotation schedule |

### Diagnostic Queries

```sql
-- Check TLS configuration
SHOW ssl;
SHOW ssl_cert_file;
SHOW ssl_key_file;
SHOW ssl_ca_file;

-- Check authentication configuration
SELECT
    rolname,
    rolsuper,
    rolcreaterole,
    rolcreatedb,
    rolcanlogin,
    rolreplication,
    rolconnlimit
FROM pg_roles
WHERE rolname NOT LIKE 'pg_%'
ORDER BY rolname;

-- Check row-level security
SELECT
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
AND rowsecurity = true;

-- Check audit configuration
SHOW log_statement;
SHOW log_connections;
SHOW log_disconnections;
SHOW log_duration;
```

## API Reference

### AuthenticationManager

```python
class AuthenticationManager:
    def __init__(self, connection_string: str)
    def configure_password_policy(self, **kwargs) -> ConfigResult
    def enable_certificate_auth(self, **kwargs) -> ConfigResult
    def configure_ldap(self, **kwargs) -> ConfigResult
    def configure_kerberos(self, **kwargs) -> ConfigResult
    def configure_lockout(self, **kwargs) -> ConfigResult
    def get_auth_status(self) -> AuthStatus
    def rotate_password(self, username: str) -> RotationResult
```

### EncryptionManager

```python
class EncryptionManager:
    def __init__(self, connection_string: str)
    def configure_tls(self, **kwargs) -> ConfigResult
    def enable_encryption_at_rest(self, **kwargs) -> ConfigResult
    def configure_column_encryption(self, **kwargs) -> ConfigResult
    def get_encryption_status(self) -> EncryptionStatus
    def rotate_keys(self) -> RotationResult
    def verify_encryption(self) -> VerificationResult
```

### AccessControlManager

```python
class AccessControlManager:
    def __init__(self, connection_string: str)
    def configure_rbac(self, policy: RBACPolicy) -> ConfigResult
    def enable_row_level_security(self, table: str, policy: str) -> ConfigResult
    def configure_column_permissions(self, **kwargs) -> ConfigResult
    def audit_privileges(self) -> PrivilegeAudit
    def check_permission(self, user: str, resource: str, action: str) -> bool
    def grant_role(self, user: str, role: str) -> GrantResult
    def revoke_role(self, user: str, role: str) -> RevokeResult
```

### ComplianceChecker

```python
class ComplianceChecker:
    def __init__(self, connection_string: str)
    def check_cis_benchmark(self) -> ComplianceResult
    def check_pci_dss(self) -> ComplianceResult
    def check_soc2(self) -> ComplianceResult
    def check_gdpr(self) -> ComplianceResult
    def check_hipaa(self) -> ComplianceResult
    def generate_report(self, standard: str) -> str
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class AuthMethod(Enum):
    PASSWORD = "password"
    CERTIFICATE = "certificate"
    KERBEROS = "kerberos"
    LDAP = "ldap"

class Severity(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityIssue:
    title: str
    description: str
    severity: Severity
    recommendation: str
    reference: str
    affected_resource: str
    discovered_at: datetime

@dataclass
class ComplianceControl:
    requirement: str
    description: str
    passed: bool
    evidence: str
    remediation: Optional[str]

@dataclass
class AuditEntry:
    timestamp: datetime
    event_type: str
    user: str
    database: str
    detail: str
    client_ip: str
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./ssl:/etc/ssl
      - postgres_data:/var/lib/postgresql/data
    command: >
      postgres
      -c ssl=on
      -c ssl_cert_file=/etc/ssl/server.pem
      -c ssl_key_file=/etc/ssl/server.key
      -c ssl_ca_file=/etc/ssl/ca.pem
      -c log_statement=ddl
      -c log_connections=on
      -c log_disconnections=on
```

## Monitoring & Observability

### Security Metrics

```python
from security_hardening import MetricsCollector

collector = MetricsCollector()

# Collect security metrics
collector.counter("db.auth.login_attempts", 1, tags={"status": status, "user": user})
collector.counter("db.auth.login_failures", 1, tags={"reason": reason})
collector.counter("db.audit.ddl_events", 1, tags={"object": object})
collector.gauge("db.security.compliance_score", score, tags={"standard": standard})
```

### Alerting Rules

```yaml
groups:
  - name: security_alerts
    rules:
      - alert: ExcessiveLoginFailures
        expr: rate(db_auth_login_failures_total[5m]) > 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High rate of login failures"
          
      - alert: ComplianceScoreLow
        expr: db_security_compliance_score < 80
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Compliance score below 80%"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from security_hardening import AuthenticationManager

@pytest.fixture
def auth():
    return AuthenticationManager(connection_string="postgresql://localhost/test")

def test_password_policy(auth):
    result = auth.configure_password_policy(min_length=16)
    assert result.success

def test_tls_config(auth):
    result = auth.enable_tls(cert_file="test.pem", key_file="test.key")
    assert result.success
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| PostgreSQL | 12 | 15+ |
| OpenSSL | 1.1.1 | 3.0+ |

## Glossary

| Term | Definition |
|------|------------|
| **mTLS** | Mutual TLS - both client and server authenticate |
| **RBAC** | Role-Based Access Control |
| **RLS** | Row-Level Security |
| **TDE** | Transparent Data Encryption |
| **CIS** | Center for Internet Security |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added LDAP/Kerberos support
- New compliance checking
- Improved audit logging
- Added vulnerability scanning

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/security-hardening.git
cd security-hardening
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills