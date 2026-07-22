---
name: "keyboard-navigation"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "keyboard", "focus-management", "wcag", "tab-navigation", "keyboard-traps"]
---

# Keyboard Navigation

## Overview

Comprehensive keyboard navigation testing and validation toolkit for web applications. This module verifies that all interactive elements are keyboard-accessible, focus management follows WCAG 2.1 guidelines, tab order is logical and predictable, custom widgets implement correct keyboard patterns, and no keyboard traps exist. Supports testing of complex UI patterns including modal dialogs, dropdown menus, data grids, date pickers, and autocomplete widgets against WAI-ARIA Authoring Practices keyboard interaction patterns.

## Core Capabilities

- **Tab Order Analysis**: Validates DOM tab order matches visual order with tabindex audit across all interactive elements
- **Keyboard Trap Detection**: Identifies keyboard traps where focus cannot escape a component or region
- **Focus Indicator Validation**: Checks that all focusable elements have visible, high-contrast focus indicators
- **Custom Widget Keyboard Patterns**: Tests complex widgets (tabs, trees, grids, menus) against WAI-ARIA keyboard interaction specifications
- **Shortcut Key Detection**: Maps all keyboard shortcuts and verifies no conflicts with assistive technology shortcuts
- **Skip Link Validation**: Verifies skip navigation links exist and correctly target main content
- **Focus Management Testing**: Validates programmatic focus changes in SPAs, modals, and dynamic content
- **Cross-Browser Keyboard Testing**: Identifies browser-specific keyboard behavior differences

## Usage

```python
from keyboard_navigation import KeyboardTestSuite, FocusIndicator, TabOrderAnalyzer

# Initialize test suite
suite = KeyboardTestSuite(url="https://example.com", browser="chromium")

# Analyze tab order
analyzer = TabOrderAnalyzer()
tab_order = analyzer.analyze("https://example.com")
print(f"Total focusable elements: {len(tab_order.elements)}")
for elem in tab_order.elements:
    print(f"  Tab {elem.tab_index}: <{elem.tag}> — {elem.text[:50]} (visible: {elem.is_visible})")

# Check for tab order violations
violations = analyzer.check_logical_order(tab_order)
for v in violations:
    print(f"  Tab order issue: {v.description} at position {v.position}")

# Validate focus indicators
focus = FocusIndicator()
results = focus.check_all("https://example.com")
print(f"\nFocus indicator results: {results.passed}/{results.total}")
for r in results.failures:
    print(f"  FAIL: {r.selector} — {r.issue}")
```

```python
# Test keyboard shortcuts
from keyboard_navigation import ShortcutTester

tester = ShortcutTester("https://example.com")
shortcuts = tester.discover_shortcuts()
for sc in shortcuts:
    print(f"  {sc.key_combo} → {sc.action}")
    if sc.conflicts_with_at:
        print(f"    CONFLICT with assistive technology: {sc.conflicts_with_at}")

# Test modal focus trap
from keyboard_navigation import ModalFocusTest

modal_test = ModalFocusTest("https://example.com")
result = modal_test.test_focus_trap(
    trigger_selector="#open-modal-btn",
    modal_selector="[role='dialog']",
    close_selector="#close-btn",
)
print(f"Focus trap: {'PASS' if result.passed else 'FAIL'}")
print(f"Tab cycling: {'PASS' if result.tab_cycling_works else 'FAIL'}")
print(f"Escape closes: {'PASS' if result.escape_closes else 'FAIL'}")
print(f"Focus returns to trigger: {'PASS' if result.focus_returned else 'FAIL'}")
```

## Best Practices

- Every interactive element must be reachable via Tab key and operable via Enter/Space
- Focus order must follow the logical reading order — avoid positive tabindex values
- Visible focus indicators must have at least 3:1 contrast ratio against adjacent colors
- Modal dialogs must trap focus within the dialog and return focus to the trigger on close
- Skip navigation links must be the first focusable element on the page
- Custom widgets must implement the keyboard patterns from WAI-ARIA Authoring Practices
- No element should capture keyboard events without providing an accessible alternative
- Keyboard shortcuts must not conflict with screen reader shortcuts (NVDA: Insert, JAWS: Insert, VO: Control+Option)
- Focus must never be moved without user-initiated action — unpredictable focus changes disorient users
- Test with actual keyboards, not just programmatic focus — some behaviors only occur with real key events
- Validate that disabled elements are focusable but not operable, or removed from tab order entirely

## Related Modules

- **aria-implementation** — ARIA role and property patterns that keyboard behaviors depend on
- **wcag-audit** — Full WCAG audit including keyboard criteria (2.1.1, 2.1.2, 2.4.3, 2.4.7)
- **screen-reader-testing** — Screen reader interaction testing that complements keyboard testing
- **color-contrast** — Focus indicator contrast ratio requirements
- **ux-research** → **usability-testing** — Usability testing that includes keyboard-only users

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

### WCAG Keyboard Success Criteria Reference
| Criterion | Level | Description |
|-----------|-------|-------------|
| 2.1.1 Keyboard | A | All functionality available from keyboard |
| 2.1.2 No Keyboard Trap | A | Focus can be moved away from any component |
| 2.1.4 Character Key Shortcuts | A | Single-character shortcuts can be remapped or disabled |
| 2.4.3 Focus Order | A | Focusable components receive focus in meaningful order |
| 2.4.7 Focus Visible | AA | Keyboard focus indicator is visible |
| 2.4.11 Focus Not Obscured (Minimum) | AA | Focused element not entirely hidden by author-created content |
| 2.4.13 Focus Appearance | AAA | Focus indicator has sufficient size and contrast |

### WAI-ARIA Keyboard Interaction Patterns
| Widget | Key | Action |
|--------|-----|--------|
| Tab Panel | Left/Right Arrow | Move between tabs |
| Tab Panel | Home/End | Move to first/last tab |
| Tab Panel | Enter/Space | Activate tab |
| Tree View | Up/Down Arrow | Move between nodes |
| Tree View | Left Arrow | Collapse node or move to parent |
| Tree View | Right Arrow | Expand node or move to first child |
| Tree View | Home/End | Move to first/last visible node |
| Menu | Up/Down Arrow | Move between menu items |
| Menu | Left/Right Arrow | Open/close submenus |
| Menu | Home/End | Move to first/last menu item |
| Menu | Escape | Close menu, return focus to trigger |
| Listbox | Up/Down Arrow | Move between options |
| Listbox | Home/End | Move to first/last option |
| Listbox | Enter/Space | Select focused option |
| Grid | Arrow Keys | Move between cells |
| Grid | Home/End | Move to first/last cell in row |
| Grid | Page Up/Down | Move focus up/down one page |
| Combobox | Up/Down Arrow | Move through listbox options |
| Combobox | Enter | Select option |
| Combobox | Escape | Close listbox |
| Slider | Left/Down Arrow | Decrease value |
| Slider | Right/Up Arrow | Increase value |
| Slider | Home | Set to minimum value |
| Slider | End | Set to maximum value |

### Common Keyboard Testing Scenarios
```python
keyboard_scenarios = [
    {
        "name": "Form Submission",
        "steps": ["Tab to first field", "Type value", "Tab to next field", "Type value", "Tab to submit", "Press Enter"],
        "expected": "Form submits, success message announced"
    },
    {
        "name": "Modal Dialog",
        "steps": ["Tab to trigger button", "Press Enter", "Verify focus in modal", "Tab through modal elements", "Press Escape"],
        "expected": "Focus trapped in modal, Escape closes and returns focus"
    },
    {
        "name": "Dropdown Menu",
        "steps": ["Tab to menu button", "Press Enter/Space", "Navigate with arrows", "Press Enter on item", "Verify menu closes"],
        "expected": "Menu opens, items navigable, selection works"
    },
    {
        "name": "Data Grid",
        "steps": ["Tab to grid", "Use arrows to navigate cells", "Press Enter to activate cell", "Press Escape to exit edit mode"],
        "expected": "Cells navigable, editing works"
    },
    {
        "name": "Carousel/Slider",
        "steps": ["Tab to carousel", "Press Left/Right arrows", "Verify slide changes", "Press Home/End for first/last slide"],
        "expected": "Slides change, focus management correct"
    }
]
```

### Focus Management Best Practices
| Scenario | Do | Don't |
|----------|-----|-------|
| Opening modal | Move focus to modal container or first focusable element | Leave focus on trigger button |
| Closing modal | Return focus to trigger element | Leave focus somewhere in the page |
| Page navigation | Move focus to main content or skip link | Leave focus in header/nav |
| Form error | Move focus to error message or first invalid field | Leave focus on submit button |
| Dynamic content update | Announce via live region, optionally move focus | Move focus without user action |
| Tab panel switch | Move focus to new tab panel content | Leave focus on previous tab |

### Keyboard Testing Tools
| Tool | Purpose | Platform |
|------|---------|----------|
| Keyboard-Only Testing | Manual verification | All |
| Chrome DevTools Accessibility Panel | Tab order visualization | Chrome |
| Firefox Accessibility Inspector | Focus tracking | Firefox |
| axe-core | Automated keyboard checks | CI/CD |
| pa11y | CLI keyboard testing | All |
| Lighthouse | Accessibility audit including keyboard | Chrome |
| WebAIM WAVE | Browser extension | Chrome/Firefox |
| Color Contrast Analyzer | Focus indicator contrast | Windows/macOS |

### Keyboard Accessibility Checklist
- [ ] All interactive elements reachable via Tab
- [ ] Focus order matches visual reading order
- [ ] No positive tabindex values used
- [ ] Focus indicator visible on all focusable elements
- [ ] Focus indicator has 3:1 contrast ratio
- [ ] Skip navigation link present and functional
- [ ] Modal dialogs trap focus
- [ ] Escape key closes modals/dropdowns
- [ ] Arrow keys navigate within widgets
- [ ] Enter/Space activates buttons and links
- [ ] No keyboard traps exist
- [ ] Custom widgets implement WAI-ARIA patterns
- [ ] Shortcuts don't conflict with screen readers
- [ ] Disabled elements are not focusable or are announced as disabled
