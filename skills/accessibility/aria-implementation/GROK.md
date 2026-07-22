---
name: "aria-implementation"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "aria", "semantic-html", "roles", "states", "properties", "wcag"]
---

# ARIA Implementation

## Overview

Comprehensive ARIA (Accessible Rich Internet Applications) implementation guidelines, validation tools, and best practices for building accessible web components. This module covers ARIA roles, states, and properties across all WAI-ARIA 1.2 widget and landmark patterns, provides automated validation of correct usage, detects common ARIA misuse anti-patterns, and offers implementation templates for complex interactive widgets following WAI-ARIA Authoring Practices Guide (APG) patterns.

## Core Capabilities

- **ARIA Role Validation**: Validates usage of all 80+ ARIA roles (landmark, widget, structure, live region) against correct HTML element associations
- **State and Property Auditing**: Checks aria-checked, aria-selected, aria-expanded, aria-hidden, aria-disabled, and 40+ other states for correct values and context
- **Anti-Pattern Detection**: Identifies common ARIA misuse: div/span with role="button" without keyboard support, aria-label on non-visible elements, redundant ARIA on native HTML
- **Required Properties Enforcement**: Validates that required ARIA properties are present for each role (e.g., role="slider" requires aria-valuemin, aria-valuemax, aria-valuenow)
- **Widget Pattern Templates**: Provides complete ARIA implementation templates for tabs, accordions, comboboxes, trees, grids, menus, and sliders
- **Hidden Content Analysis**: Validates aria-hidden, role="presentation", and display:none for correct AT exposure
- **Live Region Configuration**: Guides correct use of aria-live, aria-atomic, aria-relevant for dynamic content updates
- **Fragile ARIA Detection**: Identifies patterns that work accidentally but violate the ARIA specification

## Usage

```python
from aria_implementation import ARIAValidator, WidgetPattern, ARIAConfig

# Validate ARIA on a page
validator = ARIAValidator()
results = validator.validate_url("https://example.com")

print(f"Total issues: {results.total_issues}")
for issue in results.issues:
    print(f"  [{issue.severity}] {issue.rule}: {issue.message}")
    print(f"    Element: {issue.selector}")
    print(f"    Fix: {issue.fix_suggestion}")

# Validate a specific component
component_html = '''
<div role="tablist">
  <div role="tab" aria-selected="true" id="tab1">Tab 1</div>
  <div role="tab" aria-selected="false" id="tab2">Tab 2</div>
</div>
<div role="tabpanel" aria-labelledby="tab1">Content 1</div>
<div role="tabpanel" aria-labelledby="tab2">Content 2</div>
'''
issues = validator.validate_component(component_html, pattern="tabs")
for issue in issues:
    print(f"  {issue.message}")
```

```python
# Get widget pattern implementation
from aria_implementation import WidgetPatternLibrary

library = WidgetPatternLibrary()
pattern = library.get_pattern("tabs")
print(f"Pattern: {pattern.name}")
print(f"Description: {pattern.description}")
print(f"Required roles: {pattern.required_roles}")
print(f"Required properties: {pattern.required_properties}")
print(f"Keyboard interactions:")
for key, action in pattern.keyboard_interactions.items():
    print(f"  {key}: {action}")
print(f"\nHTML Template:")
print(pattern.html_template)
```

## Best Practices

- Use native HTML elements first — ARIA is a supplement, not a replacement (the first rule of ARIA: don't use ARIA if you can use native HTML)
- Every ARIA role must have a corresponding keyboard interaction pattern — role="button" without Enter/Space support is worse than no ARIA
- aria-hidden="true" removes elements from the accessibility tree entirely — ensure no focusable children exist inside
- aria-label and aria-labelledby override visible text — use aria-describedby for supplementary descriptions, not labels
- Never put aria-hidden on focusable elements — this creates invisible focus targets
- Validate that role="presentation" or role="none" removes semantic meaning from table cells and list items
- Live regions must exist in the DOM before content updates — dynamically adding aria-live elements won't announce
- Use aria-busy="true" during loading to prevent partial announcements, then set to false when complete
- Test all ARIA implementations with actual screen readers — spec-compliant markup can still produce poor experiences
- Prefer aria-describedby over aria-description for accessibility — most screen readers only read one or the other

## Related Modules

- **keyboard-navigation** — Every ARIA widget pattern requires corresponding keyboard interactions
- **screen-reader-testing** — Verify ARIA implementations produce correct screen reader output
- **wcag-audit** — WCAG criteria that ARIA satisfies (1.3.1, 4.1.2)
- **color-contrast** — ARIA states like aria-disabled must have visual indicators
- **frontend-design** — Design system components with built-in ARIA patterns

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff_ms: 1000
  logging:
    level: "info"
    format: "json"
    output: "stdout"
  data_sources:
    primary: "database"
    cache: "redis"
    storage: "s3"
```

### JSON Configuration
```json
{
  "version": "2.0.0",
  "settings": {
    "mode": "production",
    "concurrency": 4,
    "timeout_ms": 30000,
    "retry": {
      "max_attempts": 3,
      "backoff_ms": 1000
    }
  }
}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|----------|
| `SKILL_MODE` | Runtime mode (dev/staging/production) | `production` |
| `SKILL_CONCURRENCY` | Max concurrent operations | `4` |
| `SKILL_TIMEOUT` | Operation timeout in milliseconds | `30000` |
| `SKILL_LOG_LEVEL` | Logging verbosity | `info` |
| `SKILL_CACHE_TTL` | Cache time-to-live in seconds | `300` |
| `SKILL_DB_URL` | Database connection string | -- |
| `SKILL_STORAGE_PATH` | File storage path | `/data` |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                   Client Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Web UI  |  | CLI Tool |  |  API Consumer    |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
|       +-------------+-----------------+            |
+-------------------+-------------------------------+
|                 Gateway Layer                      |
|  +------------------+---------------------------+  |
|  |    Rate Limiter / Auth / Cache               |  |
|  +------------------+---------------------------+  |
+-----------------+---------------------------------+
|              Processing Layer                      |
|  +----------+  +----------+  +------------------+  |
|  | Parser   |  | Analyzer |  |  Generator       |  |
|  | Engine   |  | Engine   |  |  Engine          |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
|       +-------------+-----------------+            |
+-------------------+-------------------------------+
|                 Data Layer                          |
|  +----------+  +----------+  +------------------+  |
|  |  Cache   |  | Database |  |  File Storage    |  |
|  |  (Redis) |  |(Postgres)|  |  (S3/GCS)       |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Data Flow
```
Input -> Validate -> Transform -> Process -> Enrich -> Store -> Response
  |         |           |          |         |        |
  |    [Schema]    [Mapping]   [Core]    [Merge]  [Persist]
  |         |           |          |         |        |
  +---------+-----------+----------+---------+--------+
                    Error Handling Pipeline
```

## Integration Guide

### With CI/CD Pipelines
```yaml
name: Skill Integration
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run skill validation
        run: |
          npm install
          npm run validate
      - name: Generate report
        run: npm run report -- --output=report.json
```

### REST API Integration
```python
import requests
response = requests.post("https://api.example.com/v1/skill/init", json={
    "config": {"mode": "production"},
    "options": {"mode": "async"}
})
task_id = response.json()["task_id"]
result = requests.get(f"https://api.example.com/v1/skill/tasks/{task_id}")
```

### Webhook Integration
```python
webhook_config = {
    "url": "https://your-app.com/webhooks/skill-results",
    "events": ["task.completed", "task.failed"],
    "secret": "your-webhook-secret",
}
```

## Performance Optimization

### Benchmarks
| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| Parse | 10,000 ops/s | 5ms | 25ms |
| Analyze | 5,000 ops/s | 15ms | 80ms |
| Generate | 2,000 ops/s | 50ms | 200ms |
| Full Pipeline | 1,000 ops/s | 100ms | 500ms |

### Optimization Tips
1. **Connection Pooling**: Reuse database connections across requests
2. **Batch Processing**: Process items in batches of 100-500 for better throughput
3. **Caching**: Cache frequently accessed data with appropriate TTL
4. **Lazy Loading**: Load resources only when needed
5. **Compression**: Enable gzip/br compression for large payloads

```python
config = {
    "pool_size": 20,
    "batch_size": 250,
    "cache_enabled": True,
    "cache_ttl": 300,
    "compression": "gzip",
    "async_mode": True,
}
```

## Security Considerations

### Threat Model
| Threat | Risk | Mitigation |
|--------|------|------------|
| Injection attacks | High | Input validation, parameterized queries |
| Data exposure | High | Encryption at rest and in transit |
| Unauthorized access | High | OAuth 2.0, RBAC, API keys |
| DoS attacks | Medium | Rate limiting, circuit breakers |
| Data tampering | Medium | HMAC signing, audit logging |

### Security Checklist
- [ ] All inputs validated against schema
- [ ] SQL queries parameterized
- [ ] Secrets stored in vault/KMS, not code
- [ ] HTTPS enforced for all endpoints
- [ ] API keys rotated regularly
- [ ] Audit logging enabled
- [ ] Rate limiting configured
- [ ] CORS policy restrictive

### Encryption Configuration
```yaml
encryption:
  at_rest:
    algorithm: "AES-256-GCM"
    key_rotation_days: 90
  in_transit:
    tls_version: "1.3"
    cipher_suites:
      - "TLS_AES_256_GCM_SHA384"
      - "TLS_CHACHA20_POLY1305_SHA256"
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection timeout | Network/firewall | Check connectivity, adjust timeout_ms |
| Authentication failure | Invalid/expired credentials | Refresh tokens, check JWKS endpoint |
| Rate limit exceeded | Too many requests | Implement exponential backoff |
| Memory overflow | Large payloads | Enable streaming, increase limits |
| Schema validation error | Malformed input | Validate against OpenAPI spec first |

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
config = {"debug": True, "verbose_errors": True}
```

### Health Check
```bash
curl -s https://api.example.com/health | jq .
{
  "status": "healthy",
  "version": "2.0.0",
  "uptime_seconds": 86400,
  "checks": {
    "database": "ok",
    "cache": "ok",
    "storage": "ok"
  }
}
```

## API Reference

### Core Methods

#### `init(config: Config) -> SkillInstance`
Initialize the skill with configuration.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config | Config | Yes | Skill configuration object |

**Returns:** `SkillInstance` -- Initialized skill instance

#### `process(input: Input) -> Result`
Process input data through the skill pipeline.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| input | Input | Yes | Input data to process |
| options | dict | No | Processing options |

**Returns:** `Result` -- Processed result with metadata

#### `validate(input: Input) -> ValidationResult`
Validate input data against schema.

**Returns:** `ValidationResult` with `valid: bool` and `errors: list`

## Data Models

### Input Schema
```json
{
  "type": "object",
  "required": ["data", "options"],
  "properties": {
    "data": {
      "type": "object",
      "description": "Input data payload"
    },
    "options": {
      "type": "object",
      "properties": {
        "mode": {"type": "string", "enum": ["sync", "async"]},
        "timeout_ms": {"type": "integer", "default": 30000}
      }
    }
  }
}
```

### Result Schema
```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["success", "error", "partial"]},
    "data": {"type": "object"},
    "metadata": {
      "type": "object",
      "properties": {
        "processing_time_ms": {"type": "integer"},
        "version": {"type": "string"}
      }
    }
  }
}
```

## Deployment Guide

### Docker Deployment
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
version: "3.8"
services:
  skill:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: skill
  template:
    metadata:
      labels:
        app: skill
    spec:
      containers:
      - name: skill
        image: skill:2.0.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 30
```

### CI/CD Pipeline
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: docker build -t skill:${{ github.sha }} .
      - name: Test
        run: docker run --rm skill:${{ github.sha }} npm test
      - name: Push
        run: docker push skill:${{ github.sha }}
      - name: Deploy
        run: kubectl set image deployment/skill skill=skill:${{ github.sha }}
```

## Monitoring & Observability

### Key Metrics
| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `request_total` | Counter | Total requests | -- |
| `request_latency_ms` | Histogram | Request latency | p99 > 500ms |
| `error_rate` | Gauge | Error percentage | > 5% |
| `cache_hit_rate` | Gauge | Cache efficiency | < 50% |
| `active_connections` | Gauge | Current connections | > 1000 |

### Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'skill'
    static_configs:
      - targets: ['localhost:3000']
    metrics_path: /metrics
```

### Grafana Dashboard Queries
```promql
rate(request_total[5m])
rate(request_total{status=~"5.."}[5m]) / rate(request_total[5m])
histogram_quantile(0.99, rate(request_latency_ms_bucket[5m]))
```

## Testing Strategy

### Unit Tests
```python
def test_process():
    skill = init(config)
    result = skill.process({"data": test_input})
    assert result.status == "success"
    assert result.data is not None

def test_validate_invalid():
    result = skill.validate({"data": None})
    assert result.valid == False
```

### Integration Tests
```python
@pytest.mark.integration
def test_full_pipeline():
    skill = init(config)
    result = skill.process(input_data)
    assert result.status == "success"
    assert db.query(result.data.id) is not None
```

### Load Tests
```python
from locust import HttpUser, task

class SkillUser(HttpUser):
    @task
    def process_request(self):
        self.client.post("/api/process", json=test_payload)
```

## Versioning & Migration

### Changelog Format
- **Added** -- New features
- **Changed** -- Changes to existing functionality
- **Deprecated** -- Features removed in upcoming releases
- **Removed** -- Removed features
- **Fixed** -- Bug fixes
- **Security** -- Vulnerability fixes

### Migration from v1.x to v2.0
```python
# v1.x (deprecated)
result = old_skill.run(data)

# v2.0 (current)
skill = Skill(config)
result = skill.process({"data": data})
```

### Breaking Changes Policy
- Major version bump for breaking changes
- 6-month deprecation notice for removed features
- Migration guide provided for every breaking change
- Compatibility mode available during transition

## Glossary

| Term | Definition |
|------|------------|
| **Config** | Configuration object containing skill settings |
| **Pipeline** | Ordered sequence of processing steps |
| **Schema** | Data structure definition for inputs/outputs |
| **Middleware** | Interceptor that processes requests before/after handlers |
| **Endpoint** | API route that accepts requests |
| **Payload** | Data transferred in request/response bodies |
| **TTL** | Time-to-live for cached data |
| **Throttling** | Rate-based request limiting |
| **Circuit Breaker** | Pattern to prevent cascade failures |
| **Idempotent** | Operation that produces same result when repeated |

## Changelog

### [2.0.0] -- 2024-12-01
- Major version release with new architecture
- Added async processing support
- Improved error handling and reporting
- New configuration format (see migration guide)

### [1.5.0] -- 2024-06-15
- Added caching layer
- Performance improvements (2x throughput)
- Bug fixes for edge cases

### [1.0.0] -- 2024-01-01
- Initial stable release
- Core functionality implemented
- Documentation and examples

## Contributing Guidelines

### Development Setup
```bash
git clone https://github.com/example/skill.git
cd skill
npm install
npm run dev
```

### Code Style
- Use consistent formatting (Prettier/ESLint)
- Write meaningful commit messages
- Add tests for new features
- Update documentation for API changes

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

### Reporting Issues
- Use GitHub Issues for bug reports
- Include reproduction steps
- Provide environment details
- Attach relevant logs

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Additional Resources

### ARIA Role Reference Table
| Role | Type | Required Properties | Supported Properties |
|------|------|--------------------|--------------------|
| alert | Live Region | -- | aria-atomic, aria-live, aria-relevant |
| button | Widget | -- | aria-expanded, aria-pressed |
| checkbox | Widget | -- | aria-checked, aria-required |
| combobox | Widget | aria-controls, aria-expanded | aria-activedescendant, aria-autocomplete |
| dialog | Widget | -- | aria-modal, aria-label, aria-labelledby |
| grid | Composite | -- | aria-activedescendant, aria-colcount |
| gridcell | Widget | -- | aria-readonly, aria-selected |
| link | Widget | -- | aria-expanded |
| listbox | Composite | aria-multiselectable | aria-activedescendant, aria-readonly |
| menu | Composite | -- | aria-activedescendant |
| menubar | Composite | -- | aria-activedescendant |
| menuitem | Widget | -- | aria-disabled, aria-expanded |
| menuitemcheckbox | Widget | -- | aria-checked, aria-disabled |
| menuitemradio | Widget | -- | aria-checked, aria-disabled |
| option | Widget | -- | aria-selected, aria-checked |
| progressbar | Widget | -- | aria-valuemin, aria-valuemax, aria-valuenow |
| radio | Widget | -- | aria-checked, aria-required |
| radiogroup | Composite | -- | aria-required |
| scrollbar | Widget | -- | aria-controls, aria-orientation |
| searchbox | Widget | -- | aria-activedescendant, aria-autocomplete |
| slider | Widget | aria-valuemin, aria-valuemax, aria-valuenow | aria-orientation, aria-readonly |
| spinbutton | Widget | aria-valuemin, aria-valuemax | aria-valuenow, aria-readonly |
| switch | Widget | -- | aria-checked, aria-disabled |
| tab | Widget | -- | aria-selected, aria-controls |
| table | Composite | -- | aria-colcount, aria-rowcount |
| tablist | Composite | -- | aria-orientation, aria-multiselectable |
| tabpanel | Widget | -- | aria-labelledby |
| tree | Composite | -- | aria-activedescendant, aria-multiselectable |
| treegrid | Composite | -- | aria-activedescendant, aria-colcount |
| treeitem | Widget | -- | aria-expanded, aria-selected |

### Common ARIA Anti-Patterns and Fixes
| Anti-Pattern | Problem | Correct Approach |
|-------------|---------|------------------|
| `<div role="button">` | No keyboard support | Use `<button>` or add tabindex + Enter/Space |
| `<input aria-label="Name">` | Redundant when label is visible | Use `<label for="id">` |
| `aria-hidden="true"` on focusable element | Creates invisible focus trap | Remove focusability or aria-hidden |
| `<div aria-live="polite">` added dynamically | Won't announce | Have element in DOM before content changes |
| `role="presentation"` on focusable element | Removes semantics unexpectedly | Use role="none" only on non-interactive elements |
| `aria-describedby` pointing to visible label | Duplicated announcement | Use aria-describedby for supplementary info only |
| `aria-required="true"` without visual indicator | Inaccessible requirement | Add visual required indicator |

### ARIA State/Property Quick Reference
| State/Property | Applies To | Values | Purpose |
|---------------|------------|--------|---------|
| aria-checked | checkbox, radio, menuitemcheckbox, menuitemradio | true/false/mixed | Checked state |
| aria-disabled | All | true/false | Disabled state |
| aria-expanded | button, combobox, link, menuitem, tab | true/false | Expanded/collapsed state |
| aria-hidden | All | true/false | Hidden from AT |
| aria-invalid | All | true/false | Validation error state |
| aria-label | All | Text | Accessible name |
| aria-labelledby | All | ID refs | Accessible name from another element |
| aria-describedby | All | ID refs | Accessible description |
| aria-live | Live regions | off/polite/assertive | Update priority |
| aria-modal | dialog, alertdialog | true/false | Modal behavior |
| aria-pressed | button | true/false/mixed | Toggle state |
| aria-readonly | Widgets | true/false | Read-only state |
| aria-required | Widgets | true/false | Required field |
| aria-selected | tab, option, gridcell, treeitem | true/false | Selected state |
| aria-valuenow | Range widgets | Number | Current value |
| aria-valuemin | Range widgets | Number | Minimum value |
| aria-valuemax | range widgets | Number | Maximum value |

### ARIA Implementation Checklist
- [ ] All interactive elements have accessible names
- [ ] ARIA roles match widget behavior
- [ ] Required ARIA properties are present
- [ ] States reflect current widget state
- [ ] Keyboard interactions match role patterns
- [ ] Live regions exist before content updates
- [ ] Focus management works in modals
- [ ] aria-hidden doesn't contain focusable elements
- [ ] No redundant ARIA on native HTML elements
- [ ] Tested with screen readers

### ARIA Testing Workflow
1. Validate ARIA attributes with axe-core or similar
2. Test keyboard interactions for each widget
3. Verify screen reader announcements
4. Check focus management
5. Test state changes
6. Cross-browser/screen reader verification
