---
name: "secrets-management"
category: "configuration-management"
version: "2.0.0"
tags: ["configuration-management", "secrets", "vault", "encryption", "credentials"]
---

# Secrets Management

## Overview

The Secrets Management module provides tools for securely storing, accessing, rotating, and managing secrets, API keys, certificates, and sensitive configuration. It covers HashiCorp Vault integration, cloud secret managers (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager), encryption at rest, secret rotation policies, and audit logging.

This skill is essential for security engineers, DevOps teams, and platform architects managing secrets across development, staging, and production environments.

## Core Capabilities

- **Secret Storage**: Vault KV engine, cloud secret managers, and encrypted file storage
- **Secret Access**: Dynamic secrets, short-lived credentials, and just-in-time access
- **Secret Rotation**: Automatic rotation policies, credential cycling, and zero-downtime rotation
- **Encryption**: Encryption at rest, envelope encryption, and key management
- **Access Control**: Policy-based access, RBAC for secrets, and least-privilege patterns
- **Audit Logging**: Secret access audit trails, tamper-proof logging, and compliance reporting
- **Certificate Management**: TLS certificate issuance, renewal, and PKI integration
- **Secret Injection**: Environment variable injection, sidecar patterns, and init container patterns

## Usage Examples

```python
from secrets_management import (
    VaultClient,
    SecretRotator,
    EncryptionManager,
    AuditLogger,
    CertificateManager,
)

# --- Vault Client ---
vault = VaultClient(url="https://vault.internal:8200")
vault.authenticate(method="approle")
secret = vault.read_secret("secret/data/app/database")
print(f"DB Password: {secret.data['password'][:4]}****")

# --- Secret Rotation ---
rotator = SecretRotator()
rotator.schedule_rotation(
    secret_path="secret/data/app/database",
    rotation_policy="monthly",
    generator="password",
    length=32,
)
print(f"Rotation scheduled: next in 30 days")

# --- Encryption ---
encryptor = EncryptionManager()
encrypted = encryptor.encrypt("sensitive-data", key_id="prod-key-1")
decrypted = encryptor.decrypt(encrypted, key_id="prod-key-1")
print(f"Encrypted: {encrypted[:20]}...")
print(f"Decrypted: {decrypted}")

# --- Audit Logging ---
audit = AuditLogger()
audit.log_access(
    secret_path="secret/data/app/api_key",
    accessor="service-account-1",
    action="read",
)
entries = audit.get_entries(since_hours=24)
print(f"Audit entries: {len(entries)}")

# --- Certificate Management ---
cert_mgr = CertificateManager()
cert = cert_mgr.issue_certificate(
    common_name="api.example.com",
    ttl_days=365,
    san=["api.example.com", "www.example.com"],
)
print(f"Certificate issued: {cert.serial_number}")
print(f"Expires: {cert.not_after}")
```

## Best Practices

- Never store secrets in code, config files, or version control
- Use dynamic secrets with short TTLs instead of static credentials
- Implement automatic secret rotation — manual rotation is a compliance risk
- Use encryption at rest for all stored secrets (AES-256-GCM minimum)
- Implement least-privilege access policies for secret consumers
- Log all secret access for compliance and incident investigation
- Use separate secret namespaces per environment (dev/staging/prod)
- Implement secret scanning in CI/CD to prevent secrets from entering codebase
- Use mTLS for all secret manager communication
- Have a secret revocation procedure for compromised credentials

## Related Modules

- **config-ops**: Configuration management with secrets integration
- **dynamic-config**: Dynamic secret injection into configuration
- **feature-flags**: Secret flag values management
- **environment-config**: Environment-specific secret configuration
