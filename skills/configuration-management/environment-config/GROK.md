---
name: "environment-config"
category: "configuration-management"
version: "2.0.0"
tags: ["configuration-management", "environment-config", "env-vars", "12-factor", "multi-env"]
---

# Environment Configuration

## Overview

The Environment Configuration module provides tools for managing environment-specific configuration following the 12-factor app methodology. It covers environment variable management, .env file handling, configuration profiles, multi-environment promotion, and environment parity validation.

This skill is essential for DevOps engineers, application developers, and platform teams maintaining consistent configuration across development, staging, and production environments.

## Core Capabilities

- **Environment Variables**: Parse, validate, and inject environment variables with type coercion
- **Profile Management**: Environment profiles (dev, staging, prod) with override hierarchy
- **.env File Handling**: .env file loading, merging, and validation for local development
- **Config Promotion**: Promote configuration between environments with diff and approval
- **Environment Parity**: Validate configuration consistency across environments
- **12-Factor Compliance**: Config-as-process, backing service configuration, and port binding
- **Config Templates**: Generate environment-specific configs from templates
- **Drift Prevention**: Detect and prevent unauthorized environment configuration changes

## Usage Examples

```python
from environment_config import (
    EnvManager,
    ProfileManager,
    ConfigPromoter,
    ParityValidator,
    ConfigTemplate,
)

# --- Environment Variables ---
env = EnvManager()
db_url = env.get("DATABASE_URL", default="postgresql://localhost:5432/app")
port = env.get_int("PORT", default=8080)
debug = env.get_bool("DEBUG", default=False)
print(f"DB: {db_url[:30]}...")
print(f"Port: {port}, Debug: {debug}")

# --- Profile Management ---
profiles = ProfileManager()
profiles.load_profile("production")
current = profiles.get_active()
print(f"Active profile: {current.name}")
print(f"Settings: {list(current.settings.keys())}")

# --- Config Promotion ---
promoter = ConfigPromoter()
diff = promoter.diff_environments("staging", "production")
print(f"Staging vs Production: {diff.additions} additions, {diff.modifications} modifications")
promoter.promote("staging", "production", dry_run=True)

# --- Parity Validation ---
validator = ParityValidator()
parity = validator.check_parity(["development", "staging", "production"])
print(f"Parity status: {'PASS' if parity.is_consistent else 'FAIL'}")
for issue in parity.issues:
    print(f"  Issue: {issue}")

# --- Config Templates ---
template = ConfigTemplate()
config = template.generate(
    template_path="app_config.yaml.j2",
    environment="production",
    variables={"db_host": "prod-db.internal", "replicas": 3},
)
print(f"Generated config keys: {list(config.keys())}")
```

## Best Practices

- Follow 12-factor app: store config in environment, not in code
- Use environment profiles for local development, never use production config locally
- Validate all environment variables at application startup — fail fast on missing values
- Document all required environment variables with descriptions and examples
- Use config promotion workflows with approval gates for production changes
- Maintain environment parity — dev/staging should mirror production as closely as possible
- Never store secrets in environment variables in code — use secret managers
- Use .env files only for local development, never commit to version control
- Implement environment-specific resource limits (memory, CPU, connections)
- Use typed environment variable accessors (get_int, get_bool) for safety

## Related Modules

- **config-ops**: Base configuration management operations
- **dynamic-config**: Runtime configuration updates
- **secrets-management**: Secret environment variable injection
- **feature-flags**: Feature-flag driven environment configuration

---

## Advanced Configuration

### Environment Variable Type System

Define typed environment variables with validation and coercion.

```python
env_schema = EnvSchema({
    "PORT": {"type": "int", "default": 8080, "min": 1, "max": 65535},
    "DEBUG": {"type": "bool", "default": False},
    "DB_URL": {"type": "url", "required": True},
    "LOG_LEVEL": {"type": "enum", "values": ["debug", "info", "warning", "error"]},
})
env = TypedEnvManager(schema=env_schema)
```

### Environment Variable Templates

Generate environment variables from templates.

```python
template = EnvTemplate(
    template="DATABASE_URL=postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}",
    variables={"DB_HOST": "localhost", "DB_PORT": "5432", "DB_NAME": "app"},
)
rendered = template.render()
```

### Environment Profiles

Manage multiple environment profiles with inheritance.

```python
profiles = ProfileManager(
    profiles={
        "base": {"LOG_LEVEL": "info", "METRICS_ENABLED": True},
        "development": {"extends": "base", "LOG_LEVEL": "debug", "DEBUG": True},
        "staging": {"extends": "base", "LOG_LEVEL": "info"},
        "production": {"extends": "base", "LOG_LEVEL": "warning"},
    },
)
profile = profiles.get("production")
```

### Environment Variable Encryption

Encrypt sensitive environment variables.

```python
encrypted_env = EncryptedEnvManager(
    encryption_key=get_kms_key("env-encryption"),
    encrypted_vars=["DATABASE_PASSWORD", "API_KEY"],
)
encrypted_env.load(".env.encrypted")
```

---

## Architecture Patterns

### Environment Promotion Pipeline

Promote configuration through environments with validation gates.

```python
pipeline = EnvironmentPromotionPipeline(
    stages=["development", "staging", "production"],
    gates=[
        ValidationGate("schema_check"),
        ValidationGate("security_scan"),
        ApprovalGate("human_approval"),
    ],
)
pipeline.promote("staging", "production")
```

### Environment Drift Detection

Detect configuration drift between environments.

```python
drift_detector = EnvironmentDriftDetector(
    environments=["development", "staging", "production"],
    track_keys=["DATABASE_URL", "REDIS_URL", "LOG_LEVEL"],
)
drift_report = drift_detector.check()
```

### Environment Bootstrap

Automatically bootstrap new environments.

```python
bootstrapper = EnvironmentBootstrapper(
    template_env="staging",
    new_env="production",
    overrides={"DB_HOST": "prod-db.internal", "REPLICAS": 6},
)
bootstrapper.bootstrap()
```

---

## Integration Guide

### Docker Environment Variables

```dockerfile
# Dockerfile
ENV APP_ENV=production
ENV LOG_LEVEL=info
ENV PORT=8080

# docker-compose.yml
environment:
  - DATABASE_URL=postgresql://db:5432/app
  - REDIS_URL=redis://redis:6379
```

### Kubernetes Environment Variables

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-env
data:
  APP_ENV: production
  LOG_LEVEL: info
---
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      envFrom:
        - configMapRef:
            name: app-env
        - secretRef:
            name: app-secrets
```

### CI/CD Environment Configuration

```yaml
# GitHub Actions
env:
  APP_ENV: ${{ matrix.environment }}
  DATABASE_URL: ${{ secrets[format('{0}_DATABASE_URL', matrix.environment)] }}
```

---

## Performance Optimization

### Environment Variable Caching

Cache parsed environment variables for fast access.

```python
env_cache = EnvCache(
    ttl_seconds=60,
    max_entries=1000,
)
# Subsequent reads: ~0.001ms vs ~0.1ms for os.environ
```

### Bulk Environment Loading

Load environment variables from multiple sources in parallel.

```python
loader = BulkEnvLoader(
    sources=[
        ".env",
        "env.yaml",
        "vault://secret/app/env",
    ],
    merge_strategy="priority",
)
env = loader.load_all()
```

---

## Security Considerations

### Environment Variable Scanning

Scan for sensitive data in environment variables.

```python
scanner = EnvScanner(
    patterns=[r"PASSWORD", r"SECRET", r"API_KEY", r"TOKEN"],
    action="warn",  # or "redact"
)
scanner.scan_process_env()
```

### Environment Isolation

Ensure environment variables are isolated per environment.

```python
isolation = EnvironmentIsolation(
    allowed_cross_env_vars=["TZ", "LANG"],
    blocked_vars=["DATABASE_PASSWORD", "API_KEY"],
)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Environment variable not found | Variable not set | Check .env file or environment |
| Type coercion error | Wrong format | Validate input format |
| Secret not injected | Vault connection failed | Check vault connectivity |
| Profile not loading | Profile not defined | Verify profile configuration |

---

## API Reference

### EnvManager

```python
class EnvManager:
    def get(key: str, default: Any = None) -> str
    def get_int(key: str, default: int = 0) -> int
    def get_bool(key: str, default: bool = False) -> bool
    def get_list(key: str, separator: str = ",") -> List[str]
    def set(key: str, value: Any) -> None
    def require(*keys: str) -> None
```

### ProfileManager

```python
class ProfileManager:
    def load_profile(name: str) -> Profile
    def get_active() -> Profile
    def list_profiles() -> List[str]
    def switch_profile(name: str) -> None
```

---

## Data Models

### Profile

```python
@dataclass
class Profile:
    name: str
    settings: dict
    extends: Optional[str]
    created_at: datetime
```

### EnvVar

```python
@dataclass
class EnvVar:
    key: str
    value: str
    type: str
    source: str  # env, .env, vault, template
    encrypted: bool
```

---

## Deployment Guide

### Environment Setup Checklist

- [ ] All required environment variables defined
- [ ] Secrets injected from vault, not committed to code
- [ ] Environment profile configured
- [ ] Validation gates passing in CI/CD
- [ ] Drift detection enabled

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `env.var.missing` | Missing required variables | > 0 |
| `env.drift.detected` | Environment drift events | Any drift |
| `env.promotion.failures` | Failed promotions | > 0 |

---

## Testing Strategy

### Environment Tests

```python
def test_env_loading():
    env = EnvManager()
    env.set("TEST_PORT", "8080")
    assert env.get_int("TEST_PORT") == 8080

def test_profile_switching():
    profiles = ProfileManager()
    profiles.load_profile("test")
    assert profiles.get_active().name == "test"
```

---

## Versioning & Migration

### Environment Schema Versioning

```yaml
schema_version: "2.0.0"
required_vars:
  - name: DATABASE_URL
    type: url
  - name: PORT
    type: int
    default: 8080
```

---

## Advanced Configuration (Extended)

### Environment Variable Validation Rules

Define validation rules for environment variables.

```python
validation_rules = {
    "DATABASE_URL": {
        "type": "url",
        "required": True,
        "pattern": r"^postgresql://.*",
    },
    "PORT": {
        "type": "int",
        "min": 1,
        "max": 65535,
        "required": True,
    },
    "LOG_LEVEL": {
        "type": "enum",
        "values": ["debug", "info", "warning", "error", "critical"],
        "default": "info",
    },
    "DEBUG": {
        "type": "bool",
        "default": False,
    },
}
```

### Environment Variable Templates

Generate environment variables from templates.

```python
class EnvTemplateEngine:
    def __init__(self):
        self.templates = {}

    def register_template(self, name, template):
        self.templates[name] = template

    def render(self, name, variables):
        template = self.templates[name]
        for key, value in variables.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template
```

### Environment-Specific Overrides

Apply environment-specific overrides to base configuration.

```python
class EnvironmentOverrideManager:
    def __init__(self):
        self.base_config = {}
        self.overrides = {}

    def set_base(self, config):
        self.base_config = config

    def set_override(self, environment, overrides):
        self.overrides[environment] = overrides

    def resolve(self, environment):
        config = copy.deepcopy(self.base_config)
        if environment in self.overrides:
            config = self.deep_merge(config, self.overrides[environment])
        return config
```

### Environment Variable Encryption

Encrypt sensitive environment variables.

```python
class EncryptedEnvManager:
    def __init__(self, encryption_key):
        self.encryption_key = encryption_key
        self.encrypted_vars = {}

    def set_encrypted(self, key, value):
        encrypted = self.encrypt(value)
        self.encrypted_vars[key] = encrypted

    def get_decrypted(self, key):
        encrypted = self.encrypted_vars.get(key)
        if encrypted:
            return self.decrypt(encrypted)
        return None
```

---

## Architecture Patterns (Extended)

### Environment Promotion Pipeline

Promote configuration through environments with validation.

```python
class EnvironmentPromotionPipeline:
    def __init__(self):
        self.stages = [
            ValidationStage(),
            ApprovalStage(),
            DeploymentStage(),
            VerificationStage(),
        ]

    def promote(self, config, from_env, to_env):
        context = {
            'config': config,
            'from_env': from_env,
            'to_env': to_env,
        }
        for stage in self.stages:
            context = stage.execute(context)
        return context['result']
```

### Environment Drift Detection

Detect configuration drift between environments.

```python
class EnvironmentDriftDetector:
    def __init__(self):
        self.baselines = {}

    def set_baseline(self, environment, config):
        self.baselines[environment] = config

    def detect_drift(self, environment, current_config):
        baseline = self.baselines.get(environment)
        if not baseline:
            return None
        return self.compare(baseline, current_config)
```

### Environment Bootstrap Pattern

Bootstrap new environments from existing ones.

```python
class EnvironmentBootstrapper:
    def __init__(self):
        self.templates = {}

    def bootstrap(self, template_env, new_env, overrides=None):
        template_config = self.get_config(template_env)
        if overrides:
            template_config = self.apply_overrides(template_config, overrides)
        self.create_environment(new_env, template_config)
```

---

## Integration Guide (Extended)

### Docker Compose Integration

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: myapp:latest
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://db:5432/app
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
      - .env.production
```

### Kubernetes ConfigMap Integration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: "production"
  DATABASE_HOST: "db.internal"
  LOG_LEVEL: "info"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: app
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secrets
```

### Ansible Integration

```yaml
# playbook.yml
- name: Configure application
  hosts: app_servers
  vars_files:
    - vars/base.yml
    - "vars/{{ inventory_hostname }}.yml"
  tasks:
    - name: Set environment variables
      lineinfile:
        path: /etc/environment
        line: "{{ item.key }}={{ item.value }}"
      loop: "{{ app_env | dict2items }}"
```

### Terraform Integration

```hcl
# variables.tf
variable "database_url" {
  type        = string
  description = "Database connection URL"
  sensitive   = true
}

variable "log_level" {
  type    = string
  default = "info"
  validation {
    condition     = contains(["debug", "info", "warning", "error"], var.log_level)
    error_message = "Log level must be debug, info, warning, or error."
  }
}
```

### CI/CD Integration

```yaml
# GitHub Actions
env:
  APP_ENV: ${{ matrix.environment }}
  DATABASE_URL: ${{ secrets[format('{0}_DATABASE_URL', matrix.environment)] }}
  API_KEY: ${{ secrets.API_KEY }}
```

---

## Performance Optimization (Extended)

### Environment Variable Caching

Cache environment variables for fast access.

```python
class CachedEnvManager:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 60

    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.cache_ttl:
                return entry['value']
        value = os.environ.get(key)
        self.cache[key] = {'value': value, 'timestamp': time.time()}
        return value
```

### Bulk Environment Loading

Load environment variables from multiple sources.

```python
class BulkEnvLoader:
    def __init__(self):
        self.sources = []

    def add_source(self, source):
        self.sources.append(source)

    def load_all(self):
        env = {}
        for source in self.sources:
            env.update(source.load())
        return env
```

### Environment Variable Profiling

Profile environment variable access patterns.

```python
class EnvProfiler:
    def __init__(self):
        self.access_counts = defaultdict(int)
        self.access_times = defaultdict(list)

    def profile_access(self, key):
        self.access_counts[key] += 1
        self.access_times[key].append(time.time())

    def get_report(self):
        return {
            key: {
                'count': self.access_counts[key],
                'avg_time': np.mean(self.access_times[key]),
            }
            for key in self.access_counts
        }
```

---

## Security Considerations (Extended)

### Environment Variable Scanning

Scan for sensitive data in environment variables.

```python
class EnvScanner:
    def __init__(self):
        self.patterns = [
            (r'PASSWORD', 'password'),
            (r'SECRET', 'secret'),
            (r'API_KEY', 'api_key'),
            (r'TOKEN', 'token'),
        ]

    def scan(self):
        findings = []
        for key, value in os.environ.items():
            for pattern, category in self.patterns:
                if re.search(pattern, key, re.IGNORECASE):
                    findings.append({
                        'key': key,
                        'category': category,
                        'risk': 'high',
                    })
        return findings
```

### Environment Isolation

Ensure environment variables are isolated per environment.

```python
class EnvironmentIsolation:
    def __init__(self):
        self.allowed_cross_env = ['TZ', 'LANG']
        self.blocked_vars = ['DATABASE_PASSWORD', 'API_KEY']

    def check_isolation(self, environment):
        violations = []
        for var in self.blocked_vars:
            if var in os.environ and environment != 'production':
                violations.append(var)
        return violations
```

### Environment Variable Encryption

Encrypt sensitive environment variables at rest.

```python
class EnvEncryptionManager:
    def __init__(self, encryption_key):
        self.key = encryption_key

    def encrypt_file(self, input_path, output_path):
        with open(input_path, 'r') as f:
            env_vars = self.parse_env_file(f.read())
        encrypted = {}
        for key, value in env_vars.items():
            if self.is_sensitive(key):
                encrypted[key] = self.encrypt(value)
            else:
                encrypted[key] = value
        self.write_env_file(output_path, encrypted)
```

---

## Troubleshooting Guide (Extended)

### Environment Variable Debugging

```python
class EnvDebugger:
    def debug(self, key):
        return {
            'key': key,
            'value': os.environ.get(key),
            'source': self.get_source(key),
            'type': self.get_type(key),
            'validation': self.validate(key),
        }
```

### Common Environment Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Variable not found | Not set in environment | Check .env file or environment |
| Type coercion error | Wrong format | Validate input format |
| Secret not injected | Vault connection failed | Check vault connectivity |
| Profile not loading | Profile not defined | Verify profile configuration |
| Drift detected | Manual changes | Apply desired state |
| Validation failed | Invalid value | Fix value to match rules |

### Environment Health Check

```python
class EnvHealthCheck:
    def check_all(self):
        return {
            'required_vars': self.check_required_vars(),
            'type_validation': self.check_types(),
            'secret_injection': self.check_secrets(),
            'profile_status': self.check_profiles(),
        }
```

---

## API Reference (Extended)

### EnvManager (Extended)

```python
class EnvManager:
    def get(key: str, default: Any = None) -> str
    def get_int(key: str, default: int = 0) -> int
    def get_bool(key: str, default: bool = False) -> bool
    def get_list(key: str, separator: str = ",") -> List[str]
    def get_dict(key: str) -> dict
    def set(key: str, value: Any) -> None
    def require(*keys: str) -> None
    def validate(key: str, rules: dict) -> bool
    def list_all() -> dict
    def get_with_source(key: str) -> Tuple[Any, str]
```

### ProfileManager (Extended)

```python
class ProfileManager:
    def load_profile(name: str) -> Profile
    def get_active() -> Profile
    def list_profiles() -> List[str]
    def switch_profile(name: str) -> None
    def create_profile(name: str, config: dict) -> Profile
    def delete_profile(name: str) -> None
    def export_profile(name: str, path: str) -> None
    def import_profile(path: str) -> Profile
```

### ConfigPromoter (Extended)

```python
class ConfigPromoter:
    def diff_environments(from_env: str, to_env: str) -> ConfigDiff
    def promote(from_env: str, to_env: str, dry_run: bool = True) -> PromotionResult
    def approve_promotion(promotion_id: str, approver: str) -> None
    def rollback_promotion(promotion_id: str) -> None
    def get_promotion_history() -> List[PromotionEntry]
```

---

## Data Models (Extended)

### Profile

```python
@dataclass
class Profile:
    name: str
    settings: dict
    extends: Optional[str]
    created_at: datetime
    updated_at: datetime
    description: str
    is_default: bool
```

### EnvVar

```python
@dataclass
class EnvVar:
    key: str
    value: str
    type: str
    source: str  # env, .env, vault, template
    encrypted: bool
    required: bool
    default: Optional[str]
    validation_rules: Optional[dict]
```

### EnvironmentDrift

```python
@dataclass
class EnvironmentDrift:
    environment: str
    drift_detected: bool
    differences: List[DriftDifference]
    detected_at: datetime
    baseline_version: str
    current_version: str
```

### PromotionResult

```python
@dataclass
class PromotionResult:
    promotion_id: str
    from_env: str
    to_env: str
    status: str  # pending, approved, deployed, failed
    changes: List[ConfigChange]
    approved_by: Optional[str]
    deployed_at: Optional[datetime]
```

---

## Deployment Guide (Extended)

### Multi-Environment Deployment

```python
class MultiEnvironmentDeployer:
    def __init__(self):
        self.environments = ['development', 'staging', 'production']
        self.promotion_order = {
            'development': 'staging',
            'staging': 'production',
        }

    def deploy_to_all(self, config):
        for env in self.environments:
            self.deploy(env, config)
```

### Environment Setup Automation

```python
class EnvironmentSetupAutomation:
    def setup(self, environment):
        self.create_variables(environment)
        self.configure_secrets(environment)
        self.set_profiles(environment)
        self.validate_setup(environment)
```

---

## Monitoring & Observability (Extended)

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `env.var.missing` | Missing required variables | > 0 |
| `env.drift.detected` | Environment drift events | Any drift |
| `env.promotion.failures` | Failed promotions | > 0 |
| `env.validation.errors` | Validation errors | > 0 |
| `env.profile.load.time` | Profile load time | > 1s |

---

## Testing Strategy (Extended)

### Environment Tests

```python
def test_env_loading():
    env = EnvManager()
    env.set("TEST_PORT", "8080")
    assert env.get_int("TEST_PORT") == 8080

def test_profile_switching():
    profiles = ProfileManager()
    profiles.load_profile("test")
    assert profiles.get_active().name == "test"

def test_env_validation():
    env = EnvManager()
    assert env.validate("PORT", {"type": "int", "min": 1, "max": 65535})

def test_config_promotion():
    promoter = ConfigPromoter()
    diff = promoter.diff_environments("staging", "production")
    assert diff is not None
```

---

## Versioning & Migration (Extended)

### Environment Schema Versioning

```yaml
schema_version: "2.0.0"
required_vars:
  - name: DATABASE_URL
    type: url
    required: true
  - name: PORT
    type: int
    default: 8080
    min: 1
    max: 65535
  - name: LOG_LEVEL
    type: enum
    values: [debug, info, warning, error]
    default: info
```

### Migration Scripts

```python
def migrate_v1_to_v2():
    """Migrate environment configuration from v1 to v2 format."""
    v1_config = load_config("v1_config.yaml")
    v2_config = {
        'schema_version': '2.0.0',
        'variables': {},
    }
    for key, value in v1_config.items():
        v2_config['variables'][key] = {
            'value': value,
            'type': infer_type(value),
            'required': True,
        }
    save_config("v2_config.yaml", v2_config)
```

---

## Glossary (Extended)

| Term | Definition |
|------|-----------|
| **Environment Variable** | Key-value pair injected into process environment |
| **Profile** | Named set of environment configuration |
| **Config Promotion** | Moving configuration between environments |
| **Environment Parity** | Consistency of configuration across environments |
| **12-Factor App** | Methodology for building modern applications |
| **.env File** | File containing environment variable definitions |
| **Environment Drift** | Differences between expected and actual env state |
| **Environment Isolation** | Preventing cross-environment variable leakage |
| **Env Scanning** | Detecting sensitive data in environment variables |
| **Profile Inheritance** | One environment profile extending another |
| **Environment Bootstrap** | Creating new environments from templates |
| **Env Validation** | Checking environment variables match rules |

---

## Changelog

### v2.0.0
- Added typed environment variables
- Environment promotion pipeline
- Profile inheritance

### v1.5.0
- Environment drift detection
- Encrypted environment variables

### v1.0.0
- Initial release with env var management
- .env file support
- Basic profile management

---

## Contributing Guidelines

### Environment Variable Naming

- Use SCREAMING_SNAKE_CASE
- Prefix with service name: `PAYMENTS_DB_URL`
- Use descriptive names: `DATABASE_CONNECTION_TIMEOUT` not `DB_TIMEOUT`

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
