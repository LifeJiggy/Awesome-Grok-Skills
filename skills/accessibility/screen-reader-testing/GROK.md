---
name: "screen-reader-testing"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "screen-reader", "assistive-technology", "nvda", "jaws", "voiceover", "aria"]
---

# Screen Reader Testing

## Overview

Specialized toolkit for testing web applications with screen readers including NVDA, JAWS, and VoiceOver. This module provides structured test plans for assistive technology compatibility, automated announcement verification, landmark navigation validation, live region monitoring, and comprehensive screen reader interaction profiling. Covers both desktop (Windows: NVDA/JAWS, macOS: VoiceOver) and mobile (iOS: VoiceOver, Android: TalkBack) platforms with device-specific test matrices.

## Core Capabilities

- **Multi-Reader Test Matrix**: Automated test orchestration across NVDA, JAWS, VoiceOver, and TalkBack with platform-specific behavior handling
- **Announcement Verification**: Validates that dynamic content changes produce correct screen reader announcements via ARIA live regions
- **Landmark Navigation Testing**: Verifies all landmark roles are present, unique, and navigable via screen reader shortcut keys
- **Reading Order Validation**: Ensures the DOM order matches the visual reading order for linear navigation modes
- **Form Association Testing**: Validates label-input associations, error message propagation, and required field announcements
- **Custom Control Profiling**: Tests ARIA widget patterns (tabs, trees, grids, dialogs) for correct role/state/value announcements
- **Interaction Recording**: Records and replays screen reader navigation sequences for regression testing
- **Cross-Platform Report Generation**: Unified reporting across all supported screen reader and OS combinations

## Usage

```python
from screen_reader_testing import (
    ScreenReaderTestSuite, TestPlatform, ReaderConfig, AnnouncementType
)

# Configure test for NVDA on Windows
config = ReaderConfig(
    platform=TestPlatform.WINDOWS,
    reader="NVDA",
    browser="Firefox",
    version="2024.1",
    voice_rate=50,
    output_format="text",
)

suite = ScreenReaderTestSuite(config)

# Test landmark navigation
landmarks = suite.test_landmarks("https://example.com")
print(f"Landmarks found: {len(landmarks)}")
for lm in landmarks:
    print(f"  {lm.role}: {lm.label} (navigable: {lm.is_navigable})")

# Test announcement of live region updates
live_tests = suite.test_live_regions(
    url="https://example.com/dashboard",
    triggers=[
        {"action": "click", "selector": "#refresh-btn"},
        {"action": "type", "selector": "#search", "value": "test"},
    ],
)
for test in live_tests:
    print(f"  {test.trigger} → '{test.announcement}' ({test.announcement_type})")
    print(f"  Expected: {test.expected}, Got: {test.actual}, Match: {test.passed}")
```

```python
# Full interaction test with reading order validation
from screen_reader_testing import ReadingOrderTest, InteractionProfile

profile = InteractionProfile(
    name="Login Flow",
    steps=[
        {"action": "navigate", "target": "https://example.com/login"},
        {"action": "tab_to", "target": "email input"},
        {"action": "type", "value": "user@example.com"},
        {"action": "tab_to", "target": "password input"},
        {"action": "type", "value": "password123"},
        {"action": "tab_to", "target": "submit button"},
        {"action": "activate"},
        {"action": "verify_announcement", "expected": "Login successful"},
    ],
)

result = suite.run_interaction(profile)
print(f"Profile '{profile.name}': {'PASS' if result.passed else 'FAIL'}")
for step in result.steps:
    print(f"  Step {step.index}: {step.action} — {step.status}")
    if step.announcement:
        print(f"    Announcement: '{step.announcement}'")
```

## Best Practices

- Always test with actual screen readers — automated tools cannot fully simulate the user experience
- Test at multiple verbosity levels (basic, advanced, verbose) as announcements vary
- Verify that all interactive elements receive visible focus with audible announcement
- Test with CSS/JavaScript disabled to verify graceful degradation
- Validate that modal dialogs trap focus and announce their content on open
- Test image alt text by navigating images list (NVDA: G key, VoiceOver: VO+U)
- Verify that error messages are announced when associated with form fields via aria-describedby
- Test heading navigation (NVDA: H key, VoiceOver: VO+Command+H) to verify document outline
- Check that data tables have proper th, scope, and caption elements for table navigation
- Test ARIA live regions with politeness levels: assertive for errors, polite for status updates
- Document screen reader version and browser combinations tested for each finding

## Related Modules

- **wcag-audit** — Automated WCAG compliance scanning that complements manual screen reader testing
- **color-contrast** — Color contrast analysis for visual accessibility
- **keyboard-navigation** — Keyboard-only navigation testing
- **aria-implementation** — ARIA role and property implementation guidelines
- **ux-research** → **usability-testing** — Usability testing methodologies that include AT users

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

### Screen Reader Keyboard Shortcuts Reference
| Screen Reader | Heading Nav | Landmark Nav | Form Field | Link List |
|--------------|-------------|--------------|------------|-----------|
| NVDA | H / Shift+H | D / Shift+D | F / Shift+F | K / Shift+K |
| JAWS | H / Shift+H | ; / Shift+; | Tab | Insert+F7 |
| VoiceOver (Mac) | VO+Cmd+H | VO+U (rotor) | VO+Cmd+L | VO+U (rotor) |
| VoiceOver (iOS) | Swipe left/right | Rotor menu | Swipe | Rotor menu |
| TalkBack | Swipe right | Explore by touch | Swipe right | Local context |

### Screen Reader Compatibility Matrix
| Feature | NVDA + Firefox | NVDA + Chrome | JAWS + Edge | VO + Safari | TalkBack + Chrome |
|---------|----------------|---------------|-------------|-------------|-------------------|
| ARIA live regions | Full | Full | Full | Partial | Full |
| aria-hidden | Full | Full | Full | Full | Partial |
| aria-label | Full | Full | Full | Full | Full |
| aria-describedby | Full | Full | Full | Partial | Partial |
| role=combobox | Full | Partial | Full | Partial | Partial |
| role=tree | Full | Partial | Full | Partial | Minimal |
| role=grid | Full | Minimal | Full | Partial | Minimal |
| Drag and drop | Limited | Limited | Limited | Limited | Limited |
| Canvas/SVG | Partial | Partial | Partial | Partial | Minimal |

### Test Scenario Templates

#### Login Flow Test
```python
login_test = {
    "name": "Login Flow Screen Reader Test",
    "steps": [
        {"action": "navigate", "url": "/login"},
        {"action": "verify_heading", "expected": "Sign In"},
        {"action": "verify_landmark", "expected": "form"},
        {"action": "tab_to", "target": "email input"},
        {"action": "verify_label", "expected": "Email address"},
        {"action": "type", "value": "user@example.com"},
        {"action": "tab_to", "target": "password input"},
        {"action": "verify_label", "expected": "Password"},
        {"action": "type", "value": "password123"},
        {"action": "tab_to", "target": "submit button"},
        {"action": "verify_label", "expected": "Sign In"},
        {"action": "activate"},
        {"action": "verify_announcement", "expected": "Login successful"},
    ]
}
```

#### Navigation Menu Test
```python
nav_test = {
    "name": "Main Navigation Screen Reader Test",
    "steps": [
        {"action": "navigate", "url": "/"},
        {"action": "verify_landmark", "expected": "navigation"},
        {"action": "verify_label", "expected": "Main menu"},
        {"action": "navigate_to", "target": "menu items"},
        {"action": "verify_count", "expected": 5},
        {"action": "verify_item", "index": 0, "expected": "Home"},
        {"action": "activate_item", "index": 0},
        {"action": "verify_page_change", "expected": "Home page"},
    ]
}
```

#### Form Validation Test
```python
validation_test = {
    "name": "Form Validation Messages Test",
    "steps": [
        {"action": "navigate", "url": "/contact"},
        {"action": "tab_to", "target": "submit button"},
        {"action": "activate"},
        {"action": "verify_error_count", "expected": 3},
        {"action": "verify_error", "field": "name", "expected": "Name is required"},
        {"action": "verify_error", "field": "email", "expected": "Email is required"},
        {"action": "verify_error", "field": "message", "expected": "Message is required"},
        {"action": "tab_to", "target": "name input"},
        {"action": "type", "value": "John Doe"},
        {"action": "verify_error_dismissed", "field": "name"},
    ]
}
```

### Common Screen Reader Issues and Fixes
| Issue | Screen Reader | Cause | Fix |
|-------|--------------|-------|-----|
| Silent button | All | Missing accessible name | Add aria-label or visible text |
| Double announcement | NVDA | Both aria-label and text present | Remove aria-label, use text only |
| Missing list semantics | JAWS | ul/li without role=list | Ensure proper HTML list structure |
| Inconsistent tab behavior | All | role=tab without aria-selected | Add aria-selected state |
| Live region not announced | All | Dynamic content without aria-live | Add aria-live="polite" or "assertive" |
| Modal not announced | VO | Missing role=dialog | Add role="dialog" and aria-modal="true" |
| Table data unreadable | All | Missing th/scope | Add th elements with scope attribute |

### Performance Metrics for Screen Reader Testing
| Metric | Target | Description |
|--------|--------|-------------|
| Announcement delay | < 200ms | Time for screen reader to announce content change |
| Navigation speed | < 500ms | Time to navigate between landmarks |
| Form feedback | < 300ms | Time for error messages to be announced |
| Page load | < 3s | Full page load with screen reader ready |

### Screen Reader Testing Workflow
```
1. Preparation
   ├── Install latest screen reader versions
   ├── Configure verbosity levels
   ├── Prepare test accounts/data
   └── Set up recording tools

2. Automated Checks
   ├── Run axe-core for ARIA issues
   ├── Check landmark structure
   ├── Validate heading hierarchy
   └── Test form label associations

3. Manual Testing
   ├── Linear navigation (Tab, arrow keys)
   ├── Landmark navigation
   ├── Heading navigation
   ├── Form field testing
   ├── Dynamic content testing
   └── Error handling verification

4. Cross-Platform Testing
   ├── Desktop screen readers
   ├── Mobile screen readers
   └── Browser combinations

5. Documentation
   ├── Record findings with steps
   ├── Capture screenshots
   ├── Document workarounds
   └── Prioritize issues
```

### Accessibility Testing Tools Integration
| Tool | Purpose | Integration Point |
|------|---------|-------------------|
| NVDA | Manual testing | Desktop testing environment |
| JAWS | Manual testing | Enterprise desktop testing |
| VoiceOver | Manual testing | macOS/iOS testing |
| TalkBack | Manual testing | Android testing |
| axe-core | Automated testing | CI/CD pipeline |
| pa11y | Automated testing | CLI integration |
| Lighthouse | Automated testing | Chrome DevTools |
| ScreenReader.js | Programmatic testing | Automated test suites |

### Summary
Screen reader testing is essential for verifying that web content is accessible to users who rely on assistive technologies. This guide covers the key aspects of testing with multiple screen readers across platforms.
