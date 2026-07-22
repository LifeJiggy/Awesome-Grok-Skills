---
name: "wcag-audit"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "wcag", "audit", "compliance", "screen-reader", "section-508", "ada"]
---

# WCAG Audit

## Overview

Comprehensive Web Content Accessibility Guidelines (WCAG) audit toolkit for evaluating web applications against WCAG 2.0, 2.1, and 2.2 success criteria at AA and AAA conformance levels. This module automates the detection of accessibility violations, generates compliance reports with severity scoring, tracks remediation progress, and integrates with CI/CD pipelines for continuous compliance monitoring. Supports both manual and automated audit workflows with role-based report generation for developers, designers, and compliance officers.

## Core Capabilities

- **Automated WCAG Criterion Checking**: Validates all 78 success criteria (A, AA, AAA) across the four principles: Perceivable, Operable, Understandable, and Robust
- **Violation Severity Classification**: Categorizes issues as Critical, Serious, Moderate, Minor, or Best Practice with CVSS-like scoring
- **Multi-Format Reporting**: Generates HTML, JSON, PDF, and JUnit XML reports for different stakeholders
- **Remediation Tracking**: Links violations to specific code locations with fix suggestions and estimated effort
- **Baseline Comparison**: Tracks accessibility regression across releases with delta reports
- **CI/CD Integration**: Provides exit codes and gate policies for build pipelines
- **Custom Rule Engine**: Extend built-in rules with XPath, CSS selector, and JavaScript-based custom validators
- **Screenshot Evidence**: Captures annotated screenshots of violations for visual documentation

## Usage

```python
from wcag_audit import WCAGAuditor, AuditConfig, Severity, ConformanceLevel

# Configure audit for WCAG 2.1 AA
config = AuditConfig(
    url="https://example.com",
    conformance_level=ConformanceLevel.AA,
    wcag_version="2.1",
    include_screenshots=True,
    custom_rules_path="./rules",
    excluded_paths=["/admin", "/legacy"],
    viewport_width=1440,
    viewport_height=900,
    wait_for_load=5.0,
    max_pages=50,
    follow_links=True,
)

auditor = WCAGAuditor(config)
results = auditor.run()

# Process results
print(f"Total violations: {results.total_violations}")
print(f"Critical: {results.by_severity[Severity.CRITICAL]}")
print(f"Score: {results.compliance_score}/100")

# Generate reports
auditor.export_html_report(results, "report.html")
auditor.export_junit_xml(results, "junit.xml")
auditor.export_json(results, "results.json")

# Baseline comparison
previous = auditor.load_baseline("baseline.json")
delta = auditor.compare(results, previous)
print(f"Regressions: {delta.regressions}")
print(f"Fixes: {delta.fixes}")
```

```python
# CI/CD gate usage
from wcag_audit import CIIntegration, GatePolicy

gate = CIIntegration(
    policy=GatePolicy(
        max_critical=0,
        max_serious=5,
        fail_on_regression=True,
        baseline_file="accessibility-baseline.json",
    )
)

exit_code = gate.evaluate("https://staging.example.com")
sys.exit(exit_code)  # 0 = pass, 1 = fail
```

## Best Practices

- Run audits on every pull request and before each release to catch regressions early
- Maintain a baseline file in version control and update it only after conscious triage decisions
- Combine automated scanning with manual testing — automated tools catch ~30-40% of real-world issues
- Prioritize Critical and Serious violations before moving to Moderate issues
- Use ARIA landmarks and semantic HTML as first-line defenses rather than ARIA patching
- Test with actual assistive technologies (NVDA, JAWS, VoiceOver) alongside automated checks
- Document accepted risks in an accessibility conformance report (ACR) per VPAT template
- Run audits against both desktop (1440px) and mobile (375px) viewports
- Include color contrast checks for all text sizes including placeholder text and disabled states
- Validate that focus indicators are visible on all interactive elements
- Audit dynamic content updates using ARIA live regions

## Related Modules

- **screen-reader-testing** — Manual and automated screen reader interaction testing with NVDA, JAWS, and VoiceOver
- **color-contrast** — Dedicated contrast ratio analysis with color blindness simulation
- **keyboard-navigation** — Full keyboard traversal testing and focus management validation
- **aria-implementation** — ARIA role, state, and property implementation guidelines and validators
- **api** → **api-documentation** — Accessible API documentation generation
- **frontend-design** — Accessible design system foundations

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

### WCAG 2.2 Success Criteria Reference
| Criterion | Level | Description |
|-----------|-------|-------------|
| 2.4.11 Focus Not Obscured (Minimum) | AA | Focused element must not be entirely hidden |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | Focused element must not be hidden by any content |
| 2.4.13 Focus Appearance | AAA | Focus indicator must have sufficient size and contrast |
| 2.5.7 Dragging Movements | AA | Functionality operable without dragging |
| 2.5.8 Target Size (Minimum) | AA | Touch targets must be at least 24x24 CSS pixels |
| 3.2.6 Consistent Help | A | Help mechanisms appear in consistent location |
| 3.3.7 Redundant Entry | A | Previously entered info auto-populated or selectable |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive function test for authentication |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | No object or content recognition for authentication |

### VPAT Template Sections
1. **Product Name** -- Identify the product being evaluated
2. **Executive Summary** -- High-level accessibility statement
3. **Conformance Level** -- Full/Partial/Not Applicable per table
4. **Remarks and Explanations** -- Additional context for findings
5. **Legal Disclaimer** -- Standard VPAT legal language

### Automated Testing Tools Comparison
| Tool | Coverage | Speed | Cost | Integration |
|------|----------|-------|------|-------------|
| axe-core | 57% | Fast | Free | CI/CD, Browser |
| Lighthouse | 42% | Fast | Free | Chrome DevTools |
| WAVE | 35% | Medium | Free/Paid | Browser Extension |
| Pa11y | 45% | Fast | Free | CLI, CI/CD |
| SiteImprove | 80% | Slow | Paid | SaaS |
| Deque WorldSpace | 85% | Medium | Paid | Enterprise |

### Accessibility Testing Checklist
- [ ] All images have appropriate alt text
- [ ] Form inputs have associated labels
- [ ] Color is not the only way to convey information
- [ ] Focus order is logical and predictable
- [ ] Skip navigation links are present
- [ ] ARIA landmarks are correctly implemented
- [ ] Heading hierarchy is sequential (h1 -> h2 -> h3)
- [ ] Tables have headers and captions
- [ ] Links have descriptive text (not "click here")
- [ ] Dynamic content uses ARIA live regions
- [ ] Error messages are associated with form fields
- [ ] Language attribute is set on html element
- [ ] Page has a descriptive title
- [ ] Content is readable without CSS/JavaScript
- [ ] Touch targets are at least 44x44 pixels

### Common WCAG Violation Patterns
| Pattern | WCAG Criterion | Example | Fix |
|---------|----------------|---------|-----|
| Missing alt text | 1.1.1 | `<img src="logo.png">` | `<img src="logo.png" alt="Company Logo">` |
| No label association | 1.3.1 | `<input type="text">` | `<label for="name">Name</label><input id="name">` |
| Low contrast text | 1.4.3 | Gray text on white bg | Use color contrast checker, aim for 4.5:1 |
| Missing keyboard access | 2.1.1 | `<div onclick="...">` | Use `<button>` or add tabindex + key handlers |
| No skip navigation | 2.4.1 | Direct tab to content | Add skip link as first focusable element |
| Auto-playing media | 1.4.2 | `<video autoplay>` | Provide pause/stop controls |
| Missing document title | 2.4.2 | `<html>` without title | Add descriptive `<title>` element |
| No focus indicator | 2.4.7 | CSS removes outlines | Ensure visible focus styles |

### Remediation Priority Matrix
| Severity | Response Time | Examples |
|----------|---------------|----------|
| Critical | Immediate | Keyboard trap, no keyboard access, missing alt on essential image |
| Serious | 1 sprint | Missing form labels, low contrast, no skip link |
| Moderate | 2-3 sprints | Redundant ARIA, heading order, table structure |
| Minor | Backlog | Decorative image alt, redundant links, verbose labels |

### Accessibility Conformance Report (ACR) Template
```markdown
# Accessibility Conformance Report
## [Product Name] - [Version]

### Report Date
[Date]

### Evaluation Methods
- Automated testing with axe-core 4.x
- Manual testing with NVDA 2024.1 + Firefox
- Manual testing with VoiceOver + Safari
- Keyboard-only navigation testing

### Conformance Level
- **WCAG 2.1 Level A**: [Partial/Full]
- **WCAG 2.1 Level AA**: [Partial/Full]
- **WCAG 2.1 Level AAA**: [Partial/Full]

### Identified Issues
[Table of issues with severity, criterion, and status]

### Remediation Plan
[Prioritized list of fixes with timeline]
```

### WCAG Audit Workflow
```
1. Scope Definition
   ├── Identify target URLs
   ├── Define conformance level
   └── Set up test environment

2. Automated Scan
   ├── Run axe-core baseline
   ├── Collect all violations
   └── Export raw results

3. Manual Testing
   ├── Keyboard navigation
   ├── Screen reader testing
   ├── Color contrast verification
   └── Content structure review

4. Analysis & Reporting
   ├── Deduplicate findings
   ├── Classify severity
   ├── Generate remediation plan
   └── Create stakeholder reports

5. Follow-up
   ├── Track remediation progress
   ├── Verify fixes
   └── Update baseline
```

### Integration Examples

#### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Accessibility Test') {
            steps {
                sh 'npm run test:a11y'
                junit 'reports/accessibility.xml'
            }
        }
    }
    post {
        failure {
            emailext body: 'Accessibility tests failed', subject: 'A11y Test Failure'
        }
    }
}
```

#### GitHub Actions with PR Comments
```yaml
- name: Run axe-core
  uses: dequelabs/axe-core-action@v4
  with:
    urls: http://localhost:3000
    result-file: axe-results.json

- name: Comment PR
  uses: actions/github-script@v7
  with:
    script: |
      const results = require('./axe-results.json');
      const violations = results.violations.length;
      const body = `## Accessibility Scan Results\n\n**Violations found:** ${violations}`;
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        body: body
      });
```

### Performance Considerations for Large-Scale Audits
| Page Count | Recommended Approach |
|------------|---------------------|
| 1-50 pages | Direct scan, parallel browsers |
| 50-500 pages | Queue-based scanning, rate limiting |
| 500-5000 pages | Distributed scanning, database storage |
| 5000+ pages | Sampling strategy, focus on templates |

### Accessibility Metrics Dashboard
```json
{
  "dashboard": {
    "title": "Accessibility Compliance",
    "panels": [
      {"metric": "total_violations", "type": "gauge", "thresholds": [0, 10, 50]},
      {"metric": "critical_violations", "type": "stat", "thresholds": [0, 1, 5]},
      {"metric": "compliance_score", "type": "gauge", "min": 0, "max": 100},
      {"metric": "pages_audited", "type": "counter"},
      {"metric": "remediation_rate", "type": "line", "period": "30d"}
    ]
  }
}
```
