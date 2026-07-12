---
name: "config-ops"
category: "configuration-management"
version: "2.0.0"
tags: ["configuration-management", "config-ops", "infrastructure", "automation"]
---

# Configuration Operations

## Overview

The Configuration Operations module provides tools for managing, validating, and automating configuration across infrastructure and applications. It covers configuration file management, template engines, environment-specific configurations, configuration drift detection, and infrastructure configuration as code patterns.

This skill is essential for DevOps engineers, platform teams, and SREs managing complex multi-environment configuration.

## Core Capabilities

- **Config File Management**: YAML/JSON/TOML parsing, validation, merging, and templating
- **Environment Configuration**: Environment variable management, .env file handling, and 12-factor app patterns
- **Template Engines**: Jinja2, Go templates, and Mustache for configuration generation
- **Config Drift Detection**: Detect and remediate configuration drift across environments
- **Schema Validation**: JSON Schema, YAML Schema, and custom validation rules
- **Secret Management**: Configuration with secrets injection, vault integration patterns
- **Diff and Merge**: Configuration diff tools, three-way merge, and conflict resolution
- **Version Control**: Git-based configuration versioning and change tracking

## Usage Examples

```python
from config_ops import (
    ConfigManager,
    TemplateEngine,
    DriftDetector,
    SchemaValidator,
    ConfigDiff,
)

# --- Config Management ---
manager = ConfigManager()
config = manager.load("app_config.yaml")
merged = manager.merge(
    base="base_config.yaml",
    overlay="production.yaml",
)
print(f"Config keys: {list(merged.keys())}")

# --- Template Engine ---
engine = TemplateEngine()
rendered = engine.render(
    template_path="deployment.yaml.j2",
    variables={"environment": "production", "replicas": 3},
)
print(f"Rendered config:\n{rendered[:200]}...")

# --- Drift Detection ---
detector = DriftDetector()
drift = detector.compare(
    expected="desired_config.yaml",
    actual="live_config.yaml",
)
print(f"Drift detected: {drift.has_drift}")
print(f"Differences: {len(drift.differences)}")

# --- Schema Validation ---
validator = SchemaValidator()
result = validator.validate(
    data={"host": "example.com", "port": 8080},
    schema="server_schema.json",
)
print(f"Valid: {result.is_valid}")
print(f"Errors: {result.errors}")

# --- Config Diff ---
differ = ConfigDiff()
diff = differ.diff("config_v1.yaml", "config_v2.yaml")
print(f"Changes: {diff.additions} additions, {diff.deletions} deletions, {diff.modifications} modifications")
```

## Best Practices

- Use environment-specific configuration overlays (base + override pattern)
- Validate all configuration at startup — fail fast on invalid config
- Never commit secrets to version control — use vault or environment variables
- Use configuration drift detection in CI/CD to prevent unapproved changes
- Implement config schema validation for all user-facing configuration
- Use semantic versioning for configuration changes
- Template configuration for infrastructure-as-code (Terraform, Ansible)
- Implement rollback mechanisms for configuration changes
- Use feature flags for gradual configuration rollout
- Document all configuration options with descriptions and default values

## Related Modules

- **feature-flags**: Feature flag management and rollout
- **dynamic-config**: Runtime configuration updates
- **secrets-management**: Secrets handling and vault integration
- **environment-config**: Environment-specific configuration patterns
