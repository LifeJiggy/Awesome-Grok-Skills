---
name: "api-docs"
category: "technical-writing"
version: "1.0.0"
tags: ["technical-writing", "api-docs", "openapi", "swagger", "sdk", "changelog"]
---

# API Documentation & OpenAPI Specification Management

## Overview

API documentation is the contract between a service and its consumers. This module provides tooling for generating, validating, and maintaining API reference documentation from OpenAPI specifications, SDK source code, and live API endpoints. It covers the full API documentation lifecycle: from specification authoring through breaking change detection, code sample generation, and interactive explorer deployment.

The module's core strength is keeping documentation synchronized with the actual API. It can introspect OpenAPI 3.x specifications, validate them against the official schema, extract endpoint metadata from source code decorators, generate code samples in multiple languages, and detect breaking changes between specification versions. The changelog generator produces human-readable release notes specifically formatted for API consumers, categorizing changes as additions, modifications, deprecations, or removals.

For SDK documentation, the module parses Python, TypeScript, and Go source files to extract public interfaces, type signatures, docstrings, and usage examples. It then renders these into structured reference pages with consistent formatting. The interactive API explorer component generates a self-contained HTML page that allows developers to make authenticated requests against live API endpoints directly from the documentation.

The specification validation engine enforces organizational standards across all API documentation: consistent naming conventions, required field completeness, response schema quality, and example coverage. It integrates with CI pipelines to catch documentation drift before it reaches consumers.

## Core Capabilities

- **OpenAPI Specification Generation**: Parse, validate, and generate OpenAPI 3.x specifications from source code decorators, YAML/JSON files, or live endpoint introspection.
- **Breaking Change Detection**: Compare two specification versions and identify backward-incompatible changes (removed endpoints, renamed parameters, changed types) with severity classification.
- **Code Sample Generation**: Automatically generate code samples in Python, JavaScript, cURL, Ruby, and Go from OpenAPI operation definitions with customizable templates.
- **SDK Documentation**: Extract public interfaces from Python, TypeScript, and Go source files and render structured reference documentation with type signatures and examples.
- **Changelog Management**: Produce API-specific changelogs categorized by change type (added, changed, deprecated, removed) with migration guidance for breaking changes.
- **Interactive API Explorer**: Generate self-contained HTML explorers with request builder, response viewer, and authentication configuration from OpenAPI specs.
- **Specification Validation**: Enforce naming conventions, required field completeness, response schema consistency, and example coverage across all endpoints.
- **Endpoint Coverage Reporting**: Measure documentation completeness against the actual API surface, identifying undocumented endpoints and missing response schemas.

## Usage Examples

### OpenAPI Specification Validation

```python
from api_docs import OpenAPIValidator, ValidationSeverity

validator = OpenAPIValidator(
    spec_path="openapi.yaml",
    rules={
        "naming": {"param_case": "camelCase", "path_case": "kebab-case"},
        "required_fields": ["description", "summary", "operationId"],
        "response_schemas": {"require_examples": True, "max_depth": 4}
    }
)

# Full validation
report = validator.validate()
print(f"Errors: {report.error_count}")
print(f"Warnings: {report.warning_count}")

for issue in report.issues:
    if issue.severity == ValidationSeverity.ERROR:
        print(f"  ERROR [{issue.rule}] {issue.path}: {issue.message}")
```

### Breaking Change Detection

```python
from api_docs import BreakingChangeDetector

detector = BreakingChangeDetector(
    old_spec="openapi-v1.yaml",
    new_spec="openapi-v2.yaml"
)

changes = detector.detect()
for change in changes:
    print(f"[{change.severity}] {change.category}: {change.description}")
    if change.migration_path:
        print(f"  Migration: {change.migration_path}")

# Generate consumer-facing migration guide
detector.generate_migration_guide(changes, output="MIGRATION-v1-to-v2.md")
```

### Code Sample Generation

```python
from api_docs import CodeSampleGenerator, Language

generator = CodeSampleGenerator(spec_path="openapi.yaml")

# Generate samples for all endpoints
samples = generator.generate_all(languages=[Language.PYTHON, Language.JAVASCRIPT, Language.CURL])

for endpoint, lang_samples in samples.items():
    print(f"\n## {endpoint}")
    for lang, code in lang_samples.items():
        print(f"\n### {lang.value}")
        print(code)
```

### SDK Documentation Extraction

```python
from api_docs import SDKDocExtractor, SDKLanguage

extractor = SDKDocExtractor(
    source_dirs=["src/"],
    language=SDKLanguage.PYTHON,
    exclude_patterns=["*_test.py", "internal/*"]
)

# Extract all public interfaces
interfaces = extractor.extract()
for iface in interfaces:
    print(f"\n### {iface.name}")
    print(f"Type: {iface.kind}")
    print(f"Signature: {iface.signature}")
    print(f"Docstring: {iface.docstring}")
    for param in iface.parameters:
        print(f"  - {param.name} ({param.type}): {param.description}")
```

### Changelog Generation

```python
from api_docs import APIChangelogGenerator

generator = APIChangelogGenerator(
    old_version="1.4.0",
    new_version="1.5.0"
)

changelog = generator.generate_from_specs("openapi-v1.4.yaml", "openapi-v1.5.yaml")
print(changelog.markdown)

# Publish to multiple channels
generator.publish(changelog, channels=["github_releases", "slack", "email"])
```

### Interactive Explorer Generation

```python
from api_docs import ExplorerGenerator

explorer = ExplorerGenerator(
    spec_path="openapi.yaml",
    auth_config={
        "type": "bearer",
        "token_env_var": "API_TOKEN"
    },
    theme="dark"
)

explorer.generate(
    output_path="_build/explorer.html",
    base_url="https://api.example.com",
    enable_try_it_out=True
)
```

## Best Practices

1. **Generate specs from code, not code from specs**: When possible, use source code decorators or annotations to generate OpenAPI specs automatically. This ensures the documentation stays synchronized with the actual implementation.
2. **Validate every specification change**: Run OpenAPI validation in CI before merging any specification change. Catch naming inconsistencies, missing descriptions, and schema errors before they reach consumers.
3. **Detect and document breaking changes**: Use automated breaking change detection between specification versions. Any breaking change must include a migration guide.
4. **Provide code samples in at least 3 languages**: Developers use different languages. Always include cURL for universal access, plus the two most common client languages for your API.
5. **Version your documentation with your API**: Documentation version should match API version. Maintain documentation archives for older versions that are still supported.
6. **Test documentation examples**: Treat code samples as executable tests. Run them against your staging API to ensure they actually work.
7. **Document error responses**: Every endpoint should document all possible error responses with status codes, error types, and example error bodies.
8. **Use consistent naming conventions**: Enforce a single naming convention (camelCase for parameters, kebab-case for paths) across the entire specification and validate it automatically.
9. **Include request and response examples**: Every endpoint should include example requests and responses with realistic data. This helps consumers understand expected formats without trial and error.
10. **Document rate limiting**: Clearly document rate limits per endpoint or per API key, including headers that convey current limits and retry-after guidance.

## Integration Patterns

### CI/CD Pipeline Integration

```yaml
# .github/workflows/api-docs.yml
name: API Documentation
on:
  push:
    paths: ['openapi.yaml', 'src/**']
jobs:
  validate-spec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate OpenAPI Spec
        run: python -m api_docs.validate --spec openapi.yaml --fail-on error
      - name: Check Breaking Changes
        run: python -m api_docs.breaking --old openapi-v1.yaml --new openapi.yaml
      - name: Generate Samples
        run: python -m api_docs.samples --spec openapi.yaml --langs python,javascript,curl
      - name: Build Explorer
        run: python -m api_docs.explorer --spec openapi.yaml --output _build/explorer.html
```

### Webhook-triggered Spec Updates

```python
from api_docs import OpenAPIValidator, CodeSampleGenerator

def on_spec_change(spec_path: str) -> None:
    """Called by file watcher when openapi.yaml changes."""
    validator = OpenAPIValidator(spec_path=spec_path)
    report = validator.validate()
    if not report.passed:
        notify_team(f"Spec validation failed: {report.error_count} errors")
        return
    
    generator = CodeSampleGenerator(spec_path=spec_path)
    samples = generator.generate_all()
    publish_samples_to_docs_site(samples)
```

## Architecture Notes

The module maintains a separation between specification parsing and documentation generation. The `OpenAPIValidator` only reads and validates specs — it never modifies them. Code sample generation uses a template system where each language has a Jinja2 template that receives endpoint metadata and produces formatted code.

Breaking change detection works by computing a structural diff between two specs. It normalizes paths, parameters, and response schemas before comparison, so renaming a parameter from `user_id` to `userId` is detected as a breaking change (type/structure change), while adding a new optional parameter is classified as non-breaking.

The interactive explorer generates a self-contained HTML file with no external dependencies. All CSS and JavaScript are inlined, making it suitable for air-gapped environments and offline documentation packages.

## Related Modules

- [documentation](../documentation/GROK.md) — General technical documentation authoring and lifecycle management
- [tutorials](../tutorials/GROK.md) — Progressive tutorial authoring and learning path design
- [architecture-docs](../architecture-docs/GROK.md) — Architecture Decision Records and system design documentation
- [release-notes](../release-notes/GROK.md) — Automated release note generation and changelog management
