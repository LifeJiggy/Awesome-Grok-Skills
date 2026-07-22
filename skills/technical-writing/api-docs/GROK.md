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

## Advanced Configuration

### OpenAPI Validator Configuration

Customize validation rules through a configuration file:

```yaml
# api-docs-config.yml
validation:
  naming:
    param_case: camelCase
    path_case: kebab-case
    header_case: Pascal-Case
    enum_case: UPPER_SNAKE_CASE
  required_fields:
    - description
    - summary
    - operationId
    - responses
  response_schemas:
    require_examples: true
    max_depth: 4
    require_error_schemas: true
  security:
    require_security_definitions: true
    validate_scopes: true
```

### Code Sample Templates

Customize generated code samples with Jinja2 templates:

```python
from api_docs import CodeSampleGenerator, TemplateConfig

generator = CodeSampleGenerator(
    spec_path="openapi.yaml",
    template_config=TemplateConfig(
        python={
            "imports": "import requests\nimport os",
            "auth_header": "Authorization: Bearer {token}",
            "base_url_var": "API_BASE_URL",
            "error_handling": "raise_for_status",
        },
        javascript={
            "imports": "const fetch = require('node-fetch');",
            "auth_header": "Authorization: Bearer {token}",
            "base_url_var": "API_BASE_URL",
        }
    )
)
```

### Breaking Change Detection Rules

Configure which changes are considered breaking:

```yaml
breaking_changes:
  always_breaking:
    - removed_endpoint
    - removed_required_parameter
    - changed_parameter_type
    - narrowed_enum_values
  never_breaking:
    - added_optional_parameter
    - added_response_field
    - added_endpoint
  context_dependent:
    - changed_response_schema
    - renamed_parameter
    - changed_default_value
```

## Architecture Patterns

### Specification Pipeline

The API documentation system uses a pipeline architecture with distinct stages:

```
Source Code -> Extraction -> Normalization -> Validation -> Enrichment -> Output
                |              |              |              |            |
           Decorators     Schema         Rules         Samples      Renderers
           Annotations    Conversion     Checking      Generation   (HTML/PDF)
```

### Code Sample Generation Architecture

Code samples are generated from templates that receive endpoint metadata:

```python
from api_docs import CodeSampleGenerator, TemplateRegistry

# Register custom language template
registry = TemplateRegistry()
registry.register("rust", "templates/code-samples/rust.j2")

generator = CodeSampleGenerator(
    spec_path="openapi.yaml",
    template_registry=registry
)

samples = generator.generate_all(languages=["python", "rust"])
```

Template example (`templates/code-samples/rust.j2`):

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct {{ operation_id }}Request {
    {% for param in parameters %}
    pub {{ param.name }}: {{ param.type }},
    {% endfor %}
}

pub async fn {{ operation_id }}(client: &Client, base_url: &str) -> Result<{{ response_type }}, reqwest::Error> {
    let response = client
        .{{ method }}(format!("{}{{ path }}", base_url))
        .{% if has_body %}.json(&request){% endif %}
        .send()
        .await?;

    response.json().await
}
```

### SDK Documentation Extraction Pipeline

```
Source Files -> Parsing -> Interface Extraction -> Documentation Generation -> Output
                  |              |                        |                      |
            AST Analysis    Public API Filter       Docstring Parse        Markdown/PDF
            Type Resolution  Signature Build        Example Extraction     Site Builder
```

## Integration Guide

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

### IDE Integration

Real-time API documentation validation through Language Server Protocol:

```python
from api_docs import APIDocsLSPServer

server = APIDocsLSPServer(
    spec_path="openapi.yaml",
    watch_patterns=["openapi*.yaml", "src/**/*.py"],
    live_validation=True
)
server.start()
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

## Performance Optimization

### Caching Generated Samples

Cache code samples to avoid regeneration on unchanged endpoints:

```python
from api_docs import CodeSampleGenerator, CacheConfig

generator = CodeSampleGenerator(
    spec_path="openapi.yaml",
    cache_config=CacheConfig(
        enabled=True,
        cache_dir=".api-docs-cache/",
        ttl_seconds=3600
    )
)

# Only regenerates samples for changed endpoints
samples = generator.generate_all(languages=["python", "javascript"])
```

### Parallel Validation

Validate large specifications in parallel:

```python
from api_docs import OpenAPIValidator, ParallelConfig

validator = OpenAPIValidator(
    spec_path="openapi.yaml",
    parallel_config=ParallelConfig(
        enabled=True,
        workers=4,
        chunk_size=20
    )
)

report = validator.validate()
```

### Incremental Breaking Change Detection

Only compare changed endpoints between specification versions:

```python
from api_docs import BreakingChangeDetector, DiffMode

detector = BreakingChangeDetector(
    old_spec="openapi-v1.yaml",
    new_spec="openapi-v2.yaml",
    diff_mode=DiffMode.INCREMENTAL  # Only compare changed paths
)

changes = detector.detect()
```

## Security Considerations

### Authentication Configuration

Configure authentication for the interactive explorer:

```python
from api_docs import ExplorerGenerator, AuthConfig

explorer = ExplorerGenerator(
    spec_path="openapi.yaml",
    auth_config=AuthConfig(
        type="oauth2",
        flows={
            "authorizationCode": {
                "authorizationUrl": "https://auth.example.com/authorize",
                "tokenUrl": "https://auth.example.com/token",
                "scopes": ["read", "write", "admin"]
            }
        }
    )
)
```

### Input Validation

Validate all inputs to the documentation pipeline:

```python
from api_docs import InputValidator

validator = InputValidator(
    rules={
        "spec_path": {"required": True, "extension": [".yaml", ".json"]},
        "output_dir": {"required": True, "writable": True},
        "languages": {"allowed": ["python", "javascript", "typescript", "go", "ruby", "curl"]},
    }
)

validator.validate({"spec_path": "openapi.yaml", "output_dir": "_build/"})
```

### Rate Limiting

Protect the interactive explorer from abuse:

```python
from api_docs import ExplorerGenerator, RateLimitConfig

explorer = ExplorerGenerator(
    spec_path="openapi.yaml",
    rate_limit_config=RateLimitConfig(
        enabled=True,
        requests_per_minute=60,
        burst_size=10
    )
)
```

### Secure Credential Handling

Never embed credentials in generated documentation:

```python
from api_docs import SecurityFilter

filter = SecurityFilter(
    patterns=[
        r"password\s*[:=]\s*\S+",
        r"api[_-]?key\s*[:=]\s*\S+",
        r"secret\s*[:=]\s*\S+",
        r"AKIA[0-9A-Z]{16}",
    ],
    replacement="[REDACTED]"
)

filter.scan_directory("docs/")
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Spec validation fails | Missing required fields | Add description, summary, operationId to endpoints |
| Breaking changes false positive | Normalization issue | Update breaking_changes config to mark as non-breaking |
| Code samples missing | Template not found | Check template registry for language support |
| Explorer won't load | CORS or CSP issues | Configure server headers to allow explorer origin |
| SDK extraction misses methods | Access control too strict | Update exclude_patterns in SDKDocExtractor |

### Debug Commands

```bash
# Validate spec with verbose output
python -m api_docs.validate --spec openapi.yaml --verbose

# Debug breaking change detection
python -m api_docs.breaking --old v1.yaml --new v2.yaml --debug

# Inspect extracted SDK interfaces
python -m api_docs.sdk --source src/ --language python --inspect
```

### Log Output

```
[DEBUG] api_docs.validator: Checking 47 endpoints against rules
[DEBUG] api_docs.breaking: Normalizing paths for comparison
[WARNING] api_docs.breaking: Parameter rename detected: user_id -> userId (POST /users)
[ERROR] api_docs.validator: Missing description on GET /admin/stats
[INFO] api_docs.samples: Generated 141 code samples (47 endpoints x 3 languages)
```

## API Reference

### OpenAPIValidator

```python
class OpenAPIValidator:
    def __init__(self, spec_path: str, rules: dict = None,
                 parallel_config: ParallelConfig = None):
        """Initialize the OpenAPI validator."""

    def validate(self) -> ValidationReport:
        """Run full validation and return report."""

    def validate_endpoint(self, path: str, method: str) -> List[ValidationIssue]:
        """Validate a single endpoint."""
```

### BreakingChangeDetector

```python
class BreakingChangeDetector:
    def __init__(self, old_spec: str, new_spec: str,
                 diff_mode: DiffMode = DiffMode.FULL):
        """Initialize the breaking change detector."""

    def detect(self) -> List[BreakingChange]:
        """Detect breaking changes between specifications."""

    def generate_migration_guide(self, changes: List[BreakingChange],
                                 output: str) -> MigrationGuide:
        """Generate a consumer-facing migration guide."""
```

### CodeSampleGenerator

```python
class CodeSampleGenerator:
    def __init__(self, spec_path: str,
                 template_config: TemplateConfig = None,
                 template_registry: TemplateRegistry = None,
                 cache_config: CacheConfig = None):
        """Initialize the code sample generator."""

    def generate_all(self, languages: List[str]) -> Dict[str, Dict[str, str]]:
        """Generate samples for all endpoints in all languages."""

    def generate_endpoint(self, path: str, method: str,
                          languages: List[str]) -> Dict[str, str]:
        """Generate samples for a single endpoint."""
```

## Data Models

### OpenAPISpec

```python
@dataclass
class OpenAPISpec:
    id: str
    version: str
    title: str
    description: str
    paths: Dict[str, PathItem]
    components: Components
    security: List[SecurityRequirement]
    metadata: Dict[str, Any]
```

### ValidationReport

```python
@dataclass
class ValidationReport:
    passed: bool
    error_count: int
    warning_count: int
    info_count: int
    issues: List[ValidationIssue]
    spec_version: str
    validated_at: datetime
```

### BreakingChange

```python
@dataclass
class BreakingChange:
    severity: str  # critical, major, minor
    category: str  # endpoint_removed, parameter_changed, type_changed
    path: str
    description: str
    migration_path: Optional[str]
    affected_consumers: List[str]
```

### CodeSample

```python
@dataclass
class CodeSample:
    endpoint: str
    language: str
    code: str
    imports: List[str]
    auth_required: bool
    dependencies: List[str]
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "-m", "api_docs.server", "--host", "0.0.0.0", "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-docs-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api-docs
  template:
    spec:
      containers:
        - name: api-docs
          image: api-docs:latest
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 1Gi
```

## Monitoring & Observability

### Metrics Collection

```python
from api_docs import MetricsCollector

metrics = MetricsCollector(prefix="api_docs")

# Record validation metrics
metrics.histogram("spec_validation_duration_seconds", duration)
metrics.counter("spec_validations_total", count, labels={"result": "passed"})

# Record breaking change metrics
metrics.counter("breaking_changes_total", count, labels={"severity": "critical"})
```

### Alerting Rules

```yaml
groups:
  - name: api-docs
    rules:
      - alert: SpecValidationFailing
        expr: api_docs_spec_validation_errors > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "API spec validation is failing"

      - alert: HighBreakingChangeRate
        expr: rate(api_docs_breaking_changes_total[1h]) > 5
        labels:
          severity: warning
        annotations:
          summary: "High rate of breaking changes detected"
```

## Testing Strategy

### Unit Tests

```python
def test_spec_validation_catches_missing_description():
    validator = OpenAPIValidator(spec_path="test/fixtures/bad-spec.yaml")
    report = validator.validate()
    assert not report.passed
    assert any("description" in i.message for i in report.issues)

def test_breaking_change_detection():
    detector = BreakingChangeDetector(
        old_spec="test/fixtures/v1.yaml",
        new_spec="test/fixtures/v2.yaml"
    )
    changes = detector.detect()
    assert len(changes) >= 1
    assert any(c.category == "endpoint_removed" for c in changes)
```

### Integration Tests

```python
def test_full_pipeline():
    validator = OpenAPIValidator(spec_path="openapi.yaml")
    report = validator.validate()
    assert report.passed

    generator = CodeSampleGenerator(spec_path="openapi.yaml")
    samples = generator.generate_all(languages=["python", "curl"])
    assert len(samples) > 0
```

## Versioning & Migration

### Semantic Versioning

The API docs module follows semantic versioning:
- **Major**: Breaking changes to public API or configuration format
- **Minor**: New features, new language support, new validators
- **Patch**: Bug fixes, improved error messages

### Deprecation Policy

Deprecated features are marked with warnings for one minor version before removal. Migration guides are provided for all breaking changes.

## Glossary

| Term | Definition |
|------|-----------|
| **OpenAPI Specification** | A standard format for describing RESTful APIs |
| **Breaking Change** | A modification that is not backward-compatible with existing consumers |
| **Code Sample** | Auto-generated client code demonstrating API endpoint usage |
| **Interactive Explorer** | A self-contained HTML page for testing API endpoints |
| **SDK Documentation** | Reference documentation extracted from source code |
| **Semantic Versioning** | Version numbering scheme (MAJOR.MINOR.PATCH) that communicates change scope |

## Changelog

### v1.4.0 (Latest)
- Added interactive API explorer generation
- Added SDK documentation extraction for Python, TypeScript, Go
- Improved breaking change detection accuracy

### v1.3.0
- Added code sample generation for Rust and Ruby
- Improved spec validation with custom rules
- Added incremental breaking change detection

### v1.2.0
- Added migration guide generation for breaking changes
- Improved code sample templates
- Added caching for generated samples

### v1.1.0
- Added multi-language code sample generation
- Improved breaking change detection
- Added spec validation with custom rules

### v1.0.0
- Initial release with OpenAPI validation
- Breaking change detection
- Code sample generation
- Changelog generation

## Contributing Guidelines

### How to Contribute

1. Fork the repository and create a feature branch
2. Follow existing code style and patterns
3. Write tests for new features
4. Update documentation as needed
5. Ensure all CI checks pass
6. Submit a pull request with a clear description

### Adding New Language Support

1. Create a new template file in `templates/code-samples/`
2. Register the template in `TemplateRegistry`
3. Add language to the `Language` enum
4. Write tests for the new language
5. Update documentation

## License

MIT License

Copyright (c) 2025 Example Organization

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

### Dependencies

- `pyyaml` >= 6.0 — YAML parsing for OpenAPI specifications
- `requests` >= 2.31 — HTTP client for API testing
- `jinja2` >= 3.1 — Template rendering for code samples
- `pygments` >= 2.15 — Syntax highlighting in code samples
- `jsonschema` >= 4.17 — OpenAPI schema validation
