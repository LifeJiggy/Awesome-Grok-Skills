---
name: "api-versioning"
category: "api"
version: "2.0.0"
tags: ["api", "versioning", "backward-compatibility", "deprecation", "openapi", "migration"]
---

# API Versioning

## Overview

API versioning strategies and tooling for evolving APIs without breaking existing consumers. This module covers URL path versioning, header-based versioning, query parameter versioning, content negotiation (media type versioning), semantic versioning for APIs, deprecation workflows, backward/forward compatibility analysis, and automated migration tooling. Supports both REST and GraphQL APIs with version lifecycle management and consumer notification automation.

## Core Capabilities

- **Versioning Strategies**: URL path (/v1/users), query parameter (?version=2), custom header (X-API-Version), and media type (Accept: application/vnd.api.v2+json)
- **Semantic Versioning**: Major (breaking), minor (additive), and patch (fix) version management with automatic changelog generation
- **Compatibility Analysis**: Detect breaking changes between API versions (field removal, type changes, endpoint deletion, status code changes)
- **Deprecation Workflow**: Scheduled deprecation with sunset headers, migration guides, and consumer notification
- **Version Routing**: Route requests to the correct version handler with version negotiation and fallback
- **Schema Migration**: Generate migration scripts between OpenAPI schema versions
- **Consumer Tracking**: Monitor which API versions are in use and which consumers need migration
- **Dual-Version Support**: Run multiple API versions simultaneously with shared business logic

## Usage

```python
from api_versioning import (
    VersionManager, VersionStrategy, CompatibilityChecker, DeprecationPolicy
)

# Configure versioning
vm = VersionManager(
    current_version="2.0.0",
    strategy=VersionStrategy.URL_PATH,
    base_path="/api",
)

# Register versions
vm.register_version("1.0.0", status="deprecated", sunset_date="2025-06-01")
vm.register_version("1.1.0", status="deprecated", sunset_date="2025-06-01")
vm.register_version("2.0.0", status="current")
vm.register_version("2.1.0", status="beta")

# Check compatibility between versions
checker = CompatibilityChecker()
result = checker.check(
    old_schema="openapi_v1.json",
    new_schema="openapi_v2.json",
)
print(f"Breaking changes: {result.breaking_changes}")
print(f"Additive changes: {result.additive_changes}")
for change in result.changes:
    print(f"  [{change.severity}] {change.description}")
    if change.breaking:
        print(f"    Migration: {change.migration_guide}")

# Deprecation policy
policy = DeprecationPolicy(
    notice_period_days=90,
    require_sunset_header=True,
    notify_consumers=True,
    max_supported_versions=3,
)
deprecation = policy.create_deprecation(
    version="1.0.0",
    replacement="2.0.0",
    reason="Security improvements and new features",
)
print(f"\nDeprecation notice:")
print(f"  Sunset: {deprecation['sunset_date']}")
print(f"  Link: {deprecation['migration_url']}")
```

## Best Practices

- Use semantic versioning: increment major for breaking changes, minor for additions, patch for fixes
- Always support at least 2 major versions simultaneously during transition periods
- Use URL path versioning (/v1/, /v2/) for maximum visibility and ease of implementation
- Add Sunset and Deprecation headers to all responses for deprecated versions
- Provide migration guides with before/after examples for every breaking change
- Monitor API version usage to identify consumers still on old versions
- Use feature flags within versions to gradually roll out new behavior
- Never remove a field or endpoint in a minor version — deprecate first
- Support content negotiation for clients that cannot change URLs easily
- Automate compatibility checking in CI/CD to catch accidental breaking changes

## Related Modules

- **api-design** — Resource and endpoint design principles that versioning preserves
- **api-security** — Authentication changes that may require version coordination
- **api-documentation** — Version-specific documentation generation
- **api-monitoring** — Track version usage and migration progress
- **backend** → **fastapi-best-practices** — FastAPI versioning implementation patterns
