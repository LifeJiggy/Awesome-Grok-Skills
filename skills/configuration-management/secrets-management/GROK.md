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

---

## Advanced Configuration

### Multi-Engine Secret Resolution

Resolve secrets from multiple backends with fallback support.

```python
resolver = SecretResolver(
    engines=[
        SecretEngine("vault", url="https://vault.internal:8200", priority=3),
        SecretEngine("aws-secrets-manager", region="us-east-1", priority=2),
        SecretEngine("env", prefix="SECRET_", priority=1),
    ],
    fallback_strategy="cascade",
)
secret = resolver.resolve("database/password")
```

### Secret Caching with Encrypted Local Store

Cache secrets locally with encryption for offline resilience.

```python
cache = EncryptedSecretCache(
    backend="sqlite",
    encryption_key=get_local_key(),
    ttl_seconds=3600,
    max_entries=500,
)
vault_client.set_cache(cache)
```

### Secret Injection into Process Environment

Inject secrets directly into process environment variables.

```python
injector = SecretInjector(
    vault_client=vault,
    mappings={
        "DB_PASSWORD": "secret/data/app/database#password",
        "API_KEY": "secret/data/app/api_key#key",
    },
)
injector.inject()  # Sets environment variables
```

### Secret Transforms

Apply transforms to secrets after retrieval.

```python
transforms = SecretTransformPipeline([
    Base64Decode(),
    TemplateSubstitute(variables={"host": "db.internal"}),
    JsonParse(),
])
secret = vault_client.read_secret("app/config", transforms=transforms)
```

---

## Architecture Patterns

### Secret Rotation Pattern

Implement zero-downtime secret rotation.

```python
class SecretRotationOrchestrator:
    def rotate(self, secret_path: str):
        new_secret = self.generate_new_secret(secret_path)
        self.update_vault(secret_path, new_secret)
        self.notify_consumers(secret_path, new_secret)
        self.verify_rotation(secret_path)
        self.revoke_old_secret(secret_path)
```

### Dynamic Secret Pattern

Generate short-lived credentials on demand.

```python
# Generate database credentials with 1 hour TTL
creds = vault.secrets.database.generate_credentials(
    name="app-readonly",
    ttl="1h",
    max_ttl="24h",
)
# creds.username = "hmac-app-readonly-abc123"
# creds.password = "A1b2C3d4E5f6"
```

### Secret Scanner Pattern

Scan code repositories for accidentally committed secrets.

```python
scanner = SecretScanner(
    patterns=SECRET_PATTERNS,
    exclude_paths=["*.test.js", "node_modules/"],
    exclude_entropy_threshold=4.5,
)
findings = scanner.scan_repo("https://github.com/org/app")
```

### Certificate Auto-Renewal Pattern

Automatically renew certificates before expiration.

```python
renewal = CertificateRenewalManager(
    cert_store="/etc/ssl/certs/",
    renewal_threshold_days=30,
    on_renew=lambda cert: reload_service(cert),
)
renewal.start_watcher()
```

---

## Integration Guide

### HashiCorp Vault Integration

```python
from hvac import Client

vault_client = Client(url="https://vault.internal:8200")
vault_client.auth.approle.login(role_id="xxx", secret_id="yyy")

secret = vault_client.secrets.kv.v2.read_secret_version(
    path="app/database",
    mount_point="secret",
)
```

### AWS Secrets Manager Integration

```python
import boto3

client = boto3.client("secretsmanager", region_name="us-east-1")
response = client.get_secret_value(SecretId="app/database")
secret = json.loads(response["SecretString"])
```

### Azure Key Vault Integration

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)
secret = client.get_secret("database-password")
```

### GCP Secret Manager Integration

```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
response = client.access_secret_version(name="projects/my-project/secrets/db-password/versions/latest")
secret = response.payload.data.decode("UTF-8")
```

---

## Performance Optimization

### Secret Caching

Cache secrets locally to reduce vault API calls.

```python
cache = SecretCache(
    backend="memory",
    ttl_seconds=300,
    max_entries=100,
    prefetch=["app/database", "app/api_key"],
)
vault_client.set_cache(cache)
```

### Connection Pooling

Pool vault connections for high-throughput applications.

```python
pool = VaultConnectionPool(
    url="https://vault.internal:8200",
    max_connections=20,
    max_keepalive=10,
    timeout=10,
)
vault_client = Client(pool=pool)
```

### Batch Secret Retrieval

Retrieve multiple secrets in a single request.

```python
secrets = vault_client.secrets.kv.v2.read_secrets_batch(
    paths=["app/database", "app/api_key", "app/redis"],
    mount_point="secret",
)
```

---

## Security Considerations

### Secret Access Policies

Define fine-grained access policies for secret consumers.

```python
policy = SecretAccessPolicy(
    rules=[
        {"path": "secret/data/app/database", "capabilities": ["read"], "allowed_consumers": ["app-service"]},
        {"path": "secret/data/app/admin", "capabilities": ["read", "write"], "allowed_consumers": ["admin-service"]},
    ],
)
```

### Secret Scanning in CI/CD

```yaml
# GitHub Actions workflow
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    extra_args: --only-verified
```

### Secret Encryption at Rest

Encrypt secrets before storage.

```python
encryptor = SecretEncryptor(
    algorithm="AES-256-GCM",
    key_provider=AWSKMS(key_id="alias/secret-key"),
)
encrypted = encryptor.encrypt(plaintext_secret)
```

### Secret Revocation

Immediately revoke compromised secrets.

```python
vault_client.secrets.kv.v2.delete_secret_version(
    path="app/database",
    mount_point="secret",
    versions=[1, 2, 3],
)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Secret access denied | Insufficient policy permissions | Check Vault policies |
| Secret not found | Wrong mount point or path | Verify secret path |
| Rotation failed | Consumer unavailable | Check consumer health |
| Certificate expired | Auto-renewal not configured | Enable certificate auto-renewal |
| Vault sealed | Unseal key required | Unseal vault with unseal keys |

### Debug Logging

```python
import logging
logging.getLogger("secrets_management").setLevel(logging.DEBUG)
```

### Secret Access Audit

```python
audit = SecretAuditLogger()
entries = audit.get_entries(
    secret_path="app/database",
    since_hours=24,
    action="read",
)
```

---

## API Reference

### VaultClient

```python
class VaultClient:
    def authenticate(method: str, **kwargs) -> None
    def read_secret(path: str, version: int = None) -> Secret
    def write_secret(path: str, data: dict) -> None
    def delete_secret(path: str) -> None
    def list_secrets(path: str) -> List[str]
    def rotate_secret(path: str) -> None
```

### SecretRotator

```python
class SecretRotator:
    def schedule_rotation(secret_path: str, policy: str, **kwargs) -> RotationSchedule
    def rotate_now(secret_path: str) -> RotationResult
    def get_next_rotation(secret_path: str) -> datetime
    def cancel_rotation(secret_path: str) -> None
```

### CertificateManager

```python
class CertificateManager:
    def issue_certificate(common_name: str, ttl_days: int, san: List[str]) -> Certificate
    def renew_certificate(cert_id: str) -> Certificate
    def revoke_certificate(cert_id: str) -> None
    def list_certificates() -> List[Certificate]
    def check_expiration(cert_id: str) -> ExpirationInfo
```

---

## Data Models

### Secret

```python
@dataclass
class Secret:
    path: str
    data: dict
    version: int
    created_at: datetime
    expires_at: Optional[datetime]
    metadata: dict
```

### Certificate

```python
@dataclass
class Certificate:
    serial_number: str
    common_name: str
    san: List[str]
    not_before: datetime
    not_after: datetime
    issuer: str
    pem: str
```

### RotationSchedule

```python
@dataclass
class RotationSchedule:
    secret_path: str
    policy: str
    next_rotation: datetime
    last_rotation: Optional[datetime]
    status: str  # active, paused, completed
```

---

## Deployment Guide

### Vault Cluster Setup

```yaml
# docker-compose.yml
services:
  vault:
    image: hashicorp/vault:latest
    cap_add:
      - IPC_LOCK
    environment:
      VAULT_ADDR: "https://0.0.0.0:8200"
    ports:
      - "8200:8200"
    volumes:
      - vault-data:/vault/data
```

### Secret Migration

```python
migrator = SecretMigrator(
    source=VaultClient(url="https://old-vault:8200"),
    target=VaultClient(url="https://new-vault:8200"),
    mapping={"old/path": "new/path"},
)
migrator.migrate(dry_run=True)
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `secret.access.count` | Secret access frequency | Anomaly detection |
| `secret.rotation.failures` | Failed rotations | > 0 |
| `secret.expiration.days` | Days until expiration | < 30 |
| `vault.seal.status` | Vault seal status | != unsealed |

---

## Testing Strategy

### Secret Access Tests

```python
def test_secret_access():
    vault = MockVaultClient()
    vault.write_secret("test/secret", {"key": "value"})
    secret = vault.read_secret("test/secret")
    assert secret.data["key"] == "value"
```

---

## Versioning & Migration

### Secret Version Management

```python
# Keep last 5 versions of each secret
versioner = SecretVersionManager(max_versions=5)
versioner.rotate("app/database", new_data={"password": generate_password()})
```

---

## Advanced Configuration (Extended)

### Secret Lifecycle Management

Manage the complete lifecycle of secrets from creation to retirement.

```python
lifecycle_manager = SecretLifecycleManager(
    stages={
        "creation": {"approval_required": True, "encryption": True},
        "active": {"rotation_enabled": True, "access_logging": True},
        "rotation": {"grace_period_hours": 24, "notify_consumers": True},
        "retirement": {"backup_required": True, "audit_log": True},
    },
    auto_retirement_days=365,
)
```

### Secret Namespace Management

Organize secrets into namespaces for multi-tenant environments.

```python
namespace_manager = SecretNamespaceManager(
    namespaces={
        "production": {"encryption_level": "high", "audit": True},
        "staging": {"encryption_level": "medium", "audit": False},
        "development": {"encryption_level": "low", "audit": False},
    },
    cross_namespace_access=False,
)
```

### Secret Backup and Recovery

Implement backup and recovery for secrets.

```python
backup_manager = SecretBackupManager(
    backup_schedule="0 2 * * *",  # Daily at 2 AM
    backup_location="s3://secret-backups/",
    retention_days=90,
    encryption_key="backup-encryption-key",
    restore_timeout_seconds=300,
)
```

### Secret Compliance Rules

Define compliance rules for secret management.

```python
compliance_rules = SecretComplianceRules(
    rules={
        "min_password_length": 16,
        "max_secret_age_days": 90,
        "require_rotation": True,
        "require_encryption": True,
        "require_audit_logging": True,
    },
    enforcement="strict",
    violation_action="alert_and_block",
)
```

---

## Architecture Patterns (Extended)

### Secret Injection Pipeline Pattern

Inject secrets into applications through a defined pipeline.

```python
class SecretInjectionPipeline:
    def __init__(self):
        self.stages = [
            SecretResolver(),
            SecretDecryptor(),
            SecretValidator(),
            SecretInjector(),
            SecretAuditor(),
        ]

    def inject(self, secret_path, target):
        context = {"secret_path": secret_path, "target": target}
        for stage in self.stages:
            context = stage.process(context)
        return context['injected']
```

### Secret Caching Pattern

Implement multi-level secret caching for performance.

```python
class SecretCachingPattern:
    def __init__(self):
        self.l1_cache = MemoryCache(ttl=60)
        self.l2_cache = RedisCache(ttl=300)
        self.l3_cache = DiskCache(ttl=3600)

    def get_secret(self, path):
        # Check L1
        secret = self.l1_cache.get(path)
        if secret:
            return secret
        # Check L2
        secret = self.l2_cache.get(path)
        if secret:
            self.l1_cache.set(path, secret)
            return secret
        # Check L3
        secret = self.l3_cache.get(path)
        if secret:
            self.l2_cache.set(path, secret)
            self.l1_cache.set(path, secret)
            return secret
        # Fetch from vault
        secret = self.vault.read_secret(path)
        self.l3_cache.set(path, secret)
        return secret
```

### Secret Distribution Pattern

Distribute secrets to multiple services securely.

```python
class SecretDistributor:
    def __init__(self):
        self.channels = {
            "kafka": KafkaSecretChannel(),
            "redis": RedisSecretChannel(),
            "etcd": EtcdSecretChannel(),
        }

    def distribute(self, secret, services):
        for service in services:
            channel = self.get_channel(service)
            encrypted = self.encrypt_for_service(secret, service)
            channel.send(service, encrypted)
```

---

## Integration Guide (Extended)

### Kubernetes Secret Integration

```python
from kubernetes import client, config

config.load_incluster_config()
v1 = client.CoreV1Api()

# Create Kubernetes secret
secret = client.V1Secret(
    metadata=client.V1ObjectMeta(name="app-secrets"),
    data={"password": base64.b64encode(password.encode()).decode()}
)
v1.create_namespaced_secret(namespace="default", body=secret)
```

### Docker Secrets Integration

```python
# Docker Swarm secrets
import docker

client = docker.from_env()
secret = client.secrets.create(
    name="db_password",
    data=password.encode(),
)
```

### AWS Secrets Manager Integration

```python
import boto3

client = boto3.client('secretsmanager')

# Create secret
client.create_secret(
    Name='app/database/password',
    Description='Database password',
    SecretString=password,
)

# Rotate secret
client.rotate_secret(SecretId='app/database/password')
```

### Azure Key Vault Integration

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)

# Set secret
client.set_secret("database-password", password, expires_on=datetime(2025, 12, 31))
```

### GCP Secret Manager Integration

```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()

# Create secret
parent = f"projects/{project_id}"
secret = client.create_secret(
    parent=parent,
    secret_id="database-password",
    secret=secretmanager.Secret()
)
```

### HashiCorp Vault Integration

```python
import hvac

client = hvac.Client(url='https://vault.internal:8200')
client.auth.token.login(token='...')

# Write secret
client.secrets.kv.v2.create_or_update_secret(
    path='app/database',
    secret={'password': password},
    mount_point='secret'
)
```

---

## Performance Optimization (Extended)

### Secret Connection Pooling

Pool connections to secret managers for high-throughput applications.

```python
class SecretConnectionPool:
    def __init__(self, max_connections=20):
        self.pool = Queue(maxsize=max_connections)
        for _ in range(max_connections):
            self.pool.put(self.create_connection())

    def get_connection(self):
        return self.pool.get()

    def return_connection(self, conn):
        self.pool.put(conn)
```

### Secret Batch Operations

Batch secret operations for efficiency.

```python
class SecretBatchProcessor:
    def read_secrets_batch(self, paths):
        secrets = {}
        for path in paths:
            secrets[path] = self.vault.read_secret(path)
        return secrets

    def write_secrets_batch(self, secrets_dict):
        for path, value in secrets_dict.items():
            self.vault.write_secret(path, value)
```

### Secret Compression

Compress large secrets for storage efficiency.

```python
class SecretCompressor:
    def compress(self, secret_data):
        return zlib.compress(json.dumps(secret_data).encode())

    def decompress(self, compressed_data):
        return json.loads(zlib.decompress(compressed_data))
```

---

## Security Considerations (Extended)

### Secret Access Patterns

Detect unusual secret access patterns.

```python
class SecretAccessAnalyzer:
    def __init__(self):
        self.access_history = defaultdict(list)

    def analyze_access(self, secret_path, accessor, timestamp):
        history = self.access_history[secret_path]
        history.append({'accessor': accessor, 'timestamp': timestamp})

        # Detect anomalies
        if self.is_anomaly(history):
            self.alert_unusual_access(secret_path, accessor)

    def is_anomaly(self, history):
        if len(history) < 10:
            return False
        recent = [h for h in history if h['timestamp'] > time.time() - 3600]
        if len(recent) > 100:  # More than 100 accesses per hour
            return True
        return False
```

### Secret Encryption at Rest

Encrypt secrets before storage in any backend.

```python
class SecretEncryptionManager:
    def __init__(self, key_provider):
        self.key_provider = key_provider

    def encrypt_secret(self, secret_data):
        key = self.key_provider.get_key('secret-encryption')
        return self.aes_encrypt(secret_data, key)

    def decrypt_secret(self, encrypted_data):
        key = self.key_provider.get_key('secret-encryption')
        return self.aes_decrypt(encrypted_data, key)
```

### Secret Access Control

Implement fine-grained access control for secrets.

```python
class SecretAccessControl:
    def __init__(self):
        self.acl = {}

    def grant_access(self, secret_path, principal, permissions):
        if secret_path not in self.acl:
            self.acl[secret_path] = {}
        self.acl[secret_path][principal] = permissions

    def check_access(self, secret_path, principal, action):
        permissions = self.acl.get(secret_path, {}).get(principal, [])
        return action in permissions
```

### Secret Audit Trail

Maintain detailed audit trail for secret access.

```python
class SecretAuditTrail:
    def __init__(self):
        self.audit_log = []

    def log_access(self, secret_path, accessor, action, timestamp, success):
        entry = {
            'secret_path': secret_path,
            'accessor': accessor,
            'action': action,
            'timestamp': timestamp,
            'success': success,
        }
        self.audit_log.append(entry)
```

---

## Troubleshooting Guide (Extended)

### Secret Debugging Commands

```bash
# Check secret access permissions
vault read sys/policy/app-policy

# List secrets in a path
vault list secret/app/

# Read secret with debug
vault read -debug secret/app/database

# Check secret rotation status
vault read -field=rotation_status secret/app/database

# Verify secret encryption
vault read -field=encrypted secret/app/database
```

### Common Secret Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Secret access denied | Insufficient policy | Check Vault policies |
| Secret not found | Wrong mount point | Verify secret path |
| Rotation failed | Consumer unavailable | Check consumer health |
| Certificate expired | Auto-renewal not configured | Enable auto-renewal |
| Vault sealed | Unseal key required | Unseal vault |
| Secret corruption | Storage failure | Restore from backup |
| Performance slow | No caching | Enable secret caching |

### Secret Health Check

```python
class SecretHealthCheck:
    def check_all(self):
        return {
            'vault_status': self.check_vault_status(),
            'secret_expiry': self.check_expiring_secrets(),
            'rotation_status': self.check_rotation_status(),
            'access_patterns': self.check_access_patterns(),
        }
```

---

## API Reference (Extended)

### VaultClient (Extended)

```python
class VaultClient:
    def authenticate(method: str, **kwargs) -> None
    def read_secret(path: str, version: int = None) -> Secret
    def write_secret(path: str, data: dict) -> None
    def delete_secret(path: str) -> None
    def list_secrets(path: str) -> List[str]
    def rotate_secret(path: str) -> None
    def get_secret_versions(path: str) -> List[SecretVersion]
    def restore_secret(path: str, version: int) -> None
    def seal_status() -> SealStatus
    def unseal(keys: List[str]) -> None
```

### SecretRotator (Extended)

```python
class SecretRotator:
    def schedule_rotation(secret_path: str, policy: str, **kwargs) -> RotationSchedule
    def rotate_now(secret_path: str) -> RotationResult
    def get_next_rotation(secret_path: str) -> datetime
    def cancel_rotation(secret_path: str) -> None
    def get_rotation_history(secret_path: str) -> List[RotationEntry]
    def force_rotation(secret_path: str) -> RotationResult
```

### CertificateManager (Extended)

```python
class CertificateManager:
    def issue_certificate(common_name: str, ttl_days: int, san: List[str]) -> Certificate
    def renew_certificate(cert_id: str) -> Certificate
    def revoke_certificate(cert_id: str) -> None
    def list_certificates() -> List[Certificate]
    def check_expiration(cert_id: str) -> ExpirationInfo
    def export_certificate(cert_id: str, format: str) -> str
    def import_certificate(cert_path: str) -> Certificate
```

---

## Data Models (Extended)

### Secret

```python
@dataclass
class Secret:
    path: str
    data: dict
    version: int
    created_at: datetime
    expires_at: Optional[datetime]
    metadata: dict
    encrypted: bool
    rotation_policy: Optional[str]
    last_rotated: Optional[datetime]
```

### Certificate

```python
@dataclass
class Certificate:
    serial_number: str
    common_name: str
    san: List[str]
    not_before: datetime
    not_after: datetime
    issuer: str
    pem: str
    chain: List[str]
    key_algorithm: str
    key_size: int
```

### SecretAccessLog

```python
@dataclass
class SecretAccessLog:
    log_id: str
    secret_path: str
    accessor: str
    action: str
    timestamp: datetime
    success: bool
    source_ip: str
    user_agent: str
```

---

## Deployment Guide (Extended)

### Vault HA Deployment

```yaml
# docker-compose.yml for Vault HA
services:
  vault1:
    image: hashicorp/vault:latest
    cap_add: [IPC_LOCK]
    environment:
      VAULT_ADDR: "https://0.0.0.0:8200"
      VAULT_RAFT_NODE_ID: "vault1"
    ports:
      - "8200:8200"
    volumes:
      - vault1-data:/vault/data

  vault2:
    image: hashicorp/vault:latest
    cap_add: [IPC_LOCK]
    environment:
      VAULT_ADDR: "https://0.0.0.0:8200"
      VAULT_RAFT_NODE_ID: "vault2"
    ports:
      - "8201:8200"
    volumes:
      - vault2-data:/vault/data
```

### Secret Migration Strategy

```python
class SecretMigrationStrategy:
    def migrate(self, source_vault, target_vault, paths):
        for path in paths:
            secret = source_vault.read_secret(path)
            target_vault.write_secret(path, secret)
            source_vault.delete_secret(path)
```

---

## Monitoring & Observability (Extended)

### Secret Metrics

```python
# Prometheus metrics for secrets
secret_access_total = Counter('secret_access_total', 'Total secret accesses', ['path', 'action', 'success'])
secret_rotation_total = Counter('secret_rotation_total', 'Total secret rotations', ['path', 'success'])
secret_expiry_days = Gauge('secret_expiry_days', 'Days until secret expires', ['path'])
vault_status = Gauge('vault_status', 'Vault seal status')
```

### Alerting Rules

```yaml
groups:
  - name: secrets
    rules:
      - alert: SecretExpiringSoon
        expr: secret_expiry_days < 30
        for: 1h
        labels:
          severity: warning
      - alert: VaultSealed
        expr: vault_status == 1
        for: 5m
        labels:
          severity: critical
```

---

## Testing Strategy (Extended)

### Secret Access Tests

```python
def test_secret_access():
    vault = MockVaultClient()
    vault.write_secret("test/secret", {"key": "value"})
    secret = vault.read_secret("test/secret")
    assert secret.data["key"] == "value"

def test_secret_rotation():
    rotator = SecretRotator()
    result = rotator.rotate_now("test/secret")
    assert result.success

def test_certificate_renewal():
    cert_mgr = CertificateManager()
    cert = cert_mgr.issue_certificate("test.example.com", 365, ["test.example.com"])
    renewed = cert_mgr.renew_certificate(cert.serial_number)
    assert renewed.not_after > cert.not_after
```

---

## Versioning & Migration (Extended)

### Secret Version Management

```python
class SecretVersionManager:
    def __init__(self, max_versions=10):
        self.max_versions = max_versions

    def rotate(self, path, new_data):
        current = self.vault.read_secret(path)
        self.vault.write_secret(path, new_data)
        # Cleanup old versions
        versions = self.vault.get_secret_versions(path)
        if len(versions) > self.max_versions:
            for v in versions[:-self.max_versions]:
                self.vault.delete_secret_version(path, v.version)
```

### Migration Scripts

```python
def migrate_vault_v1_to_v2():
    """Migrate secrets from Vault KV v1 to v2."""
    v1_client = hvac.Client(url='https://vault:8200')
    v2_client = hvac.Client(url='https://vault:8200')

    secrets = v1_client.secrets.kv.list_secrets(path='app')
    for secret_name in secrets['data']['keys']:
        data = v1_client.secrets.kv.read_secret(path=f'app/{secret_name}')
        v2_client.secrets.kv.v2.create_or_update_secret(
            path=f'app/{secret_name}',
            secret=data['data'],
            mount_point='secret'
        )
```

---

## Glossary (Extended)

| Term | Definition |
|------|-----------|
| **Dynamic Secret** | Short-lived credential generated on demand |
| **Secret Rotation** | Process of replacing secrets with new values |
| **Secret Scanning** | Detecting secrets accidentally committed to code |
| **Certificate Auto-Renewal** | Automatically renewing TLS certificates |
| **Secret Injection** | Loading secrets into application environment |
| **Vault** | Centralized secret storage and access management |
| **Secret Namespace** | Isolated container for organizing secrets |
| **Secret Lifecycle** | Complete journey from creation to retirement |
| **Secret Caching** | Local storage of secrets for faster access |
| **Secret Backup** | Copy of secrets for disaster recovery |
| **Secret Compliance** | Adherence to secret management policies |
| **Secret Audit Trail** | Log of all secret access and changes |

---

## Changelog

### v2.0.0
- Added multi-engine secret resolution
- Certificate auto-reenewal
- Secret scanning integration

### v1.5.0
- Secret rotation scheduling
- Encrypted local cache
- Audit logging

### v1.0.0
- Initial release with Vault integration
- Basic secret storage and retrieval
- Environment variable injection

---

## Contributing Guidelines

### Secret Handling Rules

- Never log secret values
- Never store secrets in code or config files
- Use short-lived dynamic secrets when possible
- Rotate secrets regularly (minimum every 90 days)
- Implement secret scanning in CI/CD

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
