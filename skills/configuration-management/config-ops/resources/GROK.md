# Configuration Management Agent

## Overview

The **Configuration Management Agent** provides comprehensive infrastructure and application configuration management including file parsing, environment management, secrets handling, feature flags, and configuration versioning. This agent enables consistent, secure, and manageable configurations.

## Core Capabilities

### 1. Configuration Loading
Parse and manage config files:
- **Multiple Formats**: YAML, JSON, TOML, ENV
- **Schema Validation**: Ensure data integrity
- **Config Merging**: Layered configurations
- **Template Generation**: Starter templates
- **Format Conversion**: Between formats

### 2. Environment Management
Manage environment variables:
- **Environment Isolation**: Dev, staging, prod
- **Variable Validation**: Required vs optional
- **Template Generation**: .env templates
- **Secret Integration**: Environment secrets
- **Override Management**: Precedence rules

### 3. Secrets Management
Secure sensitive data:
- **Secret Storage**: Encrypted storage
- **Secret Retrieval**: Access control
- **Secret Rotation**: Automatic updates
- **Version History**: Audit trail
- **Access Policies**: IAM integration

### 4. Feature Flags
Control feature rollout:
- **Toggle Management**: On/off switches
- **Gradual Rollouts**: Percentage-based
- **A/B Testing**: Variant testing
- **Targeting Rules**: User-based, time-based
- **Audit Logging**: Changes tracking

### 5. Version Control
Track configuration changes:
- **Version History**: Full history
- **Comparison**: Diff analysis
- **Rollback**: Previous versions
- **Approval Workflows**: Change management
- **Compliance**: Audit trails

### 6. Dynamic Configuration
Real-time updates:
- **Change Listeners**: Push notifications
- **Broadcast Updates**: Multiple systems
- **Scheduled Updates**: Time-based changes
- **Diff Analysis**: Change detection
- **Rollback**: Emergency recovery

## Usage Examples

### Configuration Loading

```python
from config_management import ConfigLoader, ConfigFormat

loader = ConfigLoader()
config = loader.load_config('app.yaml', ConfigFormat.YAML)
print(f"Sections: {list(config['data'].keys())}")

validation = loader.validate_config(
    config['data'],
    {'database': dict, 'cache': dict}
)
print(f"Valid: {validation['valid']}")

merged = loader.merge_configs(
    {'db': {'host': 'localhost'}},
    {'db': {'port': 5432}}
)
print(f"Merged: {merged}")
```

### Environment Management

```python
from config_management import EnvironmentManager

env = EnvironmentManager()
env_vars = env.set_environment('production', {
    'DATABASE_URL': {'default': 'localhost', 'description': 'DB connection'},
    'API_KEY': {'sensitive': True, 'description': 'External API key'}
})
print(f"Variables: {len(env_vars['variables'])}")

validation = env.validate_env_vars(
    ['DATABASE_URL'],
    {'DATABASE_URL': 'postgres://...'}
)
print(f"Valid: {validation['valid']}")

template = env.generate_env_template(env_vars)
print(template)
```

### Secrets Management

```python
from config_management import SecretManager

secrets = SecretManager()
stored = secrets.store_secret('api-key', 'secret123', {'app': 'myapp'})
print(f"Stored: {stored['secret_id']}")

retrieved = secrets.retrieve_secret('api-key')
print(f"Retrieved: {retrieved['retrieved']}")

rotated = secrets.rotate_secret('api-key')
print(f"Rotated: {rotated['rotated']}")
```

### Feature Flags

```python
from config_management import FeatureFlagManager

flags = FeatureFlagManager()
flags.create_flag('dark-mode', True)
result = flags.evaluate_flag('dark-mode', {'user_id': '123'})
print(f"Enabled: {result['enabled']}")

rollout = flags.create_gradual_rollout('new-feature', 25, {'region': 'US'})
print(f"Rollout: {rollout['rollout_percentage']}%")

ab_test = flags.create_ab_test(
    'checkout-button',
    [{'name': 'A', 'color': 'blue'}, {'name': 'B', 'color': 'green'}],
    {'A': 50, 'B': 50}
)
print(f"A/B Test: {len(ab_test['variants'])} variants")
```

### Version Control

```python
from config_management import ConfigVersionControl

vcs = ConfigVersionControl()
saved = vcs.save_version('app-config', {'setting': 'value'}, '1.0.0')
print(f"Saved version: {saved['version']}")

version = vcs.get_version('app-config', '1.0.0')
print(f"Retrieved: {version['data']}")

diff = vcs.compare_versions('app-config', '1.0.0', '1.1.0')
print(f"Changes: {diff['summary']}")

rollback = vcs.rollback_config('app-config', '1.0.0')
print(f"Rolled back to: {rollback['rolled_back_to']}")
```

## Configuration Patterns

### Layered Configuration
```
┌─────────────────────────────────────┐
│     Environment Override             │
├─────────────────────────────────────┤
│     Application Config              │
├─────────────────────────────────────┤
│     Base Default Config            │
└─────────────────────────────────────┘
```

### 12-Factor App Config
1. **Codebase**: One repo per app
2. **Dependencies**: Explicit declaration
3. **Config**: Store config in environment
4. **Backing Services**: Treat as attached resources
5. **Build/Release/Run**: Strict separation
6. **Processes**: Stateless
7. **Port Binding**: Export via port
8. **Concurrency**: Scale via process model
9. **Disposability**: Fast startup/shutdown
10. **Dev/Prod Parity**: Keep environments similar
11. **Logs**: Treat as event streams
12. **Admin Processes**: Run identically

## Configuration Formats

### YAML Example
```yaml
database:
  host: localhost
  port: 5432
  name: myapp
  ssl: true

cache:
  host: localhost
  port: 6379

features:
  dark_mode: true
  new_checkout: false
```

### JSON Example
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "myapp"
  },
  "features": {
    "dark_mode": true
  }
}
```

### Environment Variables
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=myapp
FEATURE_DARK_MODE=true
```

## Secret Management Best Practices

### Storage Solutions
| Tool | Use Case | Features |
|------|----------|-----------|
| HashiCorp Vault | Enterprise secrets | Dynamic secrets, ACL |
| AWS Secrets Manager | AWS integration | Automatic rotation |
| Azure Key Vault | Azure services | HSM-backed |
| CyberArk | Privileged credentials | Session management |

### Security Guidelines
1. **Never commit secrets**: Use .gitignore
2. **Encrypt secrets**: At rest and in transit
3. **Rotate regularly**: Automated rotation
4. **Audit access**: Log all retrievals
5. **Least privilege**: Limit access scope

## Feature Flag Strategies

### Flag Types
| Type | Purpose | Example |
|------|---------|---------|
| Release | New features | canary, percentage rollout |
| Operational | System behavior | circuit breaker, timeout |
| Permission | User access | beta features, premium |
| Experiment | A/B testing | UI variants |

### Best Practices
1. **Default to off**: Safe rollout
2. **Time-based expiry**: Clean up old flags
3. **Monitoring**: Track flag metrics
4. **Documentation**: Track flag purpose
5. **Cleanup**: Remove unused flags

## Tools and Platforms

### Configuration Management
- **Ansible**: Configuration management
- **Puppet**: Enterprise automation
- **Chef**: Infrastructure as code
- **CFEngine**: Policy-based

### Secret Management
- **HashiCorp Vault**: Industry standard
- **AWS Secrets Manager**: Cloud native
- **Azure Key Vault**: Microsoft ecosystem
- **1Password Secrets**: Developer-focused

### Feature Flags
- **LaunchDarkly**: Feature management platform
- **Optimizely**: Experimentation
- **Split**: Feature flag platform
- **Configu**: Feature configuration

## Use Cases

### 1. Multi-Environment Deployment
- Development, staging, production
- Environment-specific settings
- Automated deployments

### 2. Secret Rotation
- API key rotation
- Database credential rotation
- Certificate management

### 3. Feature Rollout
- Gradual percentage rollout
- Geographic restrictions
- User targeting

### 4. Emergency Changes
- Quick configuration updates
- Rollback capabilities
- Audit trail

## Related Skills

- [Infrastructure as Code](../iac/terraform-cloudformation/README.md) - IaC
- [DevOps](../devops/ci-cd-pipelines/README.md) - CI/CD
- [Security Operations](../blue-team/soc-operations/README.md) - Security

---

**File Path**: `skills/configuration-management/config-ops/resources/config_management.py`
