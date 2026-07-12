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