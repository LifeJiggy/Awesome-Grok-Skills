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
