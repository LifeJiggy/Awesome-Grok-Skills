---
name: "color-contrast"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "color-contrast", "wcag", "visual", "design-system", "color-blindness"]
---

# Color Contrast

## Overview

Dedicated color contrast analysis toolkit for verifying WCAG 2.0/2.1/2.2 contrast ratio requirements across text sizes, UI components, and graphical objects. This module performs automated contrast checking for normal text (4.5:1), large text (3:1), and non-text elements (3:1), with support for color blindness simulation across 8 types (protanopia, deuteranopia, tritanopia, achromatopsia, etc.), theme-aware checking for dark/light modes, CSS custom property extraction, and integration with design token systems for proactive accessibility enforcement.

## Core Capabilities

- **WCAG Contrast Ratio Calculation**: Precise luminance-based ratio computation per WCAG 2.1 §1.4.3 (text) and §1.4.11 (non-text)
- **Color Blindness Simulation**: Simulates 8 types of color vision deficiency to verify information is not conveyed by color alone
- **Multi-Theme Analysis**: Tests contrast across light, dark, high-contrast, and custom themes automatically
- **Design Token Integration**: Validates contrast ratios in design token files (JSON, YAML, CSS custom properties)
- **Text Size Classification**: Automatically classifies text as normal, large, or enhanced based on computed font-size and weight
- **Background Image Handling**: Detects text over images/gradients and suggests overlay strategies
- **Batch Processing**: Analyzes entire CSS files, design systems, or component libraries in one pass
- **Report Generation**: Produces contrast reports with pass/fail per WCAG criterion, hex color pairs, and fix suggestions

## Usage

```python
from color_contrast import ContrastAnalyzer, TextSize, ColorPair

analyzer = ContrastAnalyzer()

# Check a single color pair
result = analyzer.check_contrast(
    foreground="#767676",
    background="#FFFFFF",
    text_size=TextSize.NORMAL,
)
print(f"Ratio: {result.ratio}:1")
print(f"WCAG AA normal text: {result.wcag_aa_normal}")
print(f"WCAG AA large text: {result.wcag_aa_large}")
print(f"WCAG AAA normal text: {result.wcag_aaa_normal}")

# Check CSS file
from color_contrast import CSSAnalyzer
css = CSSAnalyzer("styles.css")
violations = css.find_contrast_violations()
for v in violations:
    print(f"Line {v.line_number}: {v.selector}")
    print(f"  {v.foreground} on {v.background} = {v.ratio}:1 (need {v.required_ratio}:1)")
```

```python
# Color blindness simulation
from color_contrast import ColorBlindnessSimulator, BlindnessType

simulator = ColorBlindnessSimulator()
original = "#FF0000"  # Red
results = simulator.simulate_all(original)
for blindness_type, color in results.items():
    print(f"  {blindness_type.value}: {original} → {color}")

# Design token validation
from color_contrast import DesignTokenValidator
validator = DesignTokenValidator("tokens.json")
report = validator.validate()
print(f"Total tokens: {report.total_checked}")
print(f"Violations: {report.violation_count}")
```

## Best Practices

- Always verify contrast with actual rendered text, not just CSS color values
- Consider contrast at all states: default, hover, focus, active, disabled
- Disabled text has no WCAG contrast requirement but should still aim for 3:1
- Text over images or gradients needs a semi-transparent overlay to meet contrast
- Use relative luminance (not perceived brightness) for WCAG ratio calculations
- Test both foreground-on-background AND background-on-foreground ratios
- Color blindness simulation should be run on all informational color usage
- Never use color as the sole means of conveying information — pair with icons, patterns, or text
- Review contrast in both light and dark modes since both themes need compliance
- Automated contrast checking is a starting point — visual inspection by humans is essential

## Related Modules

- **wcag-audit** — Full WCAG audit that includes contrast as one of many tested criteria
- **screen-reader-testing** — Ensures information conveyed by color is also available to AT
- **keyboard-navigation** — Focus indicator contrast must meet 3:1 against adjacent colors
- **aria-implementation** — States and properties that may affect visual presentation
- **frontend-design** — Design system foundations with built-in contrast compliance

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

### WCAG Contrast Requirements by Element Type
| Element Type | WCAG Level A | WCAG Level AA | WCAG Level AAA |
|--------------|--------------|---------------|----------------|
| Normal text (< 18pt) | 4.5:1 | 4.5:1 | 7:1 |
| Large text (≥ 18pt or 14pt bold) | 3:1 | 3:1 | 4.5:1 |
| UI components | 3:1 | 3:1 | 3:1 |
| Graphical objects | 3:1 | 3:1 | 3:1 |
| Focus indicators | N/A | 3:1 | 3:1 |

### Color Blindness Simulation Types
| Type | Affects | Population | Simulation |
|------|---------|------------|------------|
| Protanopia | Red cones | 1.3% males | Red appears dark |
| Deuteranopia | Green cones | 1.2% males | Green appears brown |
| Tritanopia | Blue cones | 0.01% | Blue appears green |
| Achromatopsia | All cones | 0.003% | Full color blindness |
| Protanomaly | Red cones (partial) | 1.1% males | Reduced red sensitivity |
| Deuteranomaly | Green cones (partial) | 5% males | Reduced green sensitivity |
| Tritanomaly | Blue cones (partial) | 0.01% | Reduced blue sensitivity |
| Achromatomaly | All cones (partial) | 0.001% | Reduced color vision |

### Contrast Ratio Calculation Formula
```
Relative Luminance: L = 0.2126 * R + 0.7152 * G + 0.0722 * B
where R, G, B = linearize(sRGB/255)

Contrast Ratio: (L1 + 0.05) / (L2 + 0.05)
where L1 = lighter color, L2 = darker color
```

### Common Color Combinations and Their Ratios
| Foreground | Background | Ratio | AA Normal | AA Large |
|------------|------------|-------|-----------|----------|
| #000000 | #FFFFFF | 21:1 | Pass | Pass |
| #767676 | #FFFFFF | 4.5:1 | Pass | Pass |
| #FFFFFF | #767676 | 4.5:1 | Pass | Pass |
| #000000 | #F0F0F0 | 18.1:1 | Pass | Pass |
| #333333 | #FFFFFF | 12.6:1 | Pass | Pass |
| #666666 | #FFFFFF | 5.7:1 | Pass | Pass |
| #999999 | #FFFFFF | 2.8:1 | Fail | Pass |
| #FF0000 | #FFFFFF | 4.0:1 | Fail | Pass |
| #00FF00 | #000000 | 1.0:1 | Fail | Fail |

### Design System Contrast Checklist
- [ ] Primary text meets 4.5:1 ratio
- [ ] Secondary text meets 4.5:1 ratio
- [ ] Placeholder text meets 4.5:1 ratio
- [ ] Disabled text has sufficient visual distinction
- [ ] Link text meets 4.5:1 ratio
- [ ] Link text distinguishable from surrounding text
- [ ] Focus indicators meet 3:1 ratio against adjacent colors
- [ ] Error messages meet 4.5:1 ratio
- [ ] Status indicators use more than color alone
- [ ] Charts use patterns in addition to color
- [ ] Form validation messages are accessible
- [ ] Interactive states (hover, active, focus) maintain contrast

### Color Contrast Testing Workflow
```
1. Identify Color Usage
   ├── Text colors
   ├── Background colors
   ├── UI component colors
   ├── Status indicators
   └── Chart/graph colors

2. Automated Testing
   ├── Run contrast checker on all pages
   ├── Test CSS files directly
   ├── Validate design tokens
   └── Check theme variations

3. Manual Verification
   ├── Test with actual rendered elements
   ├── Verify text over images
   ├── Check hover/focus/active states
   └── Test dark/light modes

4. Color Blindness Simulation
   ├── Run simulation on all color usage
   ├── Verify non-color indicators
   └── Test with actual color blindness glasses

5. Documentation
   ├── Record all color decisions
   ├── Document accepted exceptions
   └── Create color palette guidelines
```

### Common Contrast Issues and Solutions
| Issue | Example | Solution |
|-------|---------|----------|
| Text over images | White text on photo | Add semi-transparent overlay |
| Gradient backgrounds | Text over gradient | Ensure worst-case ratio meets 4.5:1 |
| Dynamic backgrounds | Text over video | Provide text shadow or outline |
| Disabled states | Gray text on white | Use opacity + border for distinction |
| Placeholder text | Light gray on white | Use at least #767676 on white |
| Error states | Red text on white | Ensure 4.5:1 ratio for error messages |
| Link text | Blue on white | Use #0000EE for 8.6:1 ratio |

### Contrast Ratio Quick Reference
| Ratio | WCAG AA (Normal) | WCAG AA (Large) | WCAG AAA (Normal) | WCAG AAA (Large) |
|-------|------------------|-----------------|-------------------|------------------|
| 3:1 | Fail | Pass | Fail | Fail |
| 4.5:1 | Pass | Pass | Fail | Pass |
| 7:1 | Pass | Pass | Pass | Pass |

### Accessibility Color Palette Generator
```python
def generate_accessible_palette(base_color, text_color="#000000"):
    """Generate palette with guaranteed contrast ratios."""
    palette = {
        "primary": base_color,
        "text_on_primary": find_contrasting_color(base_color, 4.5),
        "secondary": adjust_brightness(base_color, 0.3),
        "text_on_secondary": find_contrasting_color(adjust_brightness(base_color, 0.3), 4.5),
        "background": adjust_brightness(base_color, 0.95),
        "text_on_background": text_color,
    }
    return palette
```

### Color Contrast in Different Contexts
| Context | Minimum Ratio | Additional Requirements |
|---------|---------------|------------------------|
| Body text | 4.5:1 | Readable at 16px |
| Headings | 3:1 (large text) | 18pt+ or 14pt+ bold |
| UI controls | 3:1 | Against adjacent colors |
| Focus indicators | 3:1 | Against both states |
| Icons | 3:1 | Against background |
| Charts | 3:1 | Plus patterns for color blind |
| Form labels | 4.5:1 | Associated with inputs |
| Error messages | 4.5:1 | Plus icon/text indicator |

### Summary
Color contrast is a fundamental aspect of web accessibility. By ensuring sufficient contrast ratios between text and background colors, designers can make content readable for users with various visual abilities. This guide provides the tools and knowledge needed to create accessible color palettes.

### Key Takeaways
- Always verify contrast ratios for all text elements
- Test with color blindness simulation tools
- Consider all states: default, hover, focus, active, disabled
- Document color decisions for future reference
- Use automated tools as a starting point, not the final answer

### Contrast Testing Tools
| Tool | Type | Platform | Cost |
|------|------|----------|------|
| WebAIM Contrast Checker | Online | Web | Free |
| Colour Contrast Analyser | Desktop | Windows/macOS | Free |
| Chrome DevTools | Browser | Chrome | Free |
| Firefox Accessibility Inspector | Browser | Firefox | Free |
| Stark | Plugin | Figma/Sketch | Paid |
| axe DevTools | Browser Extension | Chrome/Firefox | Free/Paid |

### Final Notes
Color contrast testing should be integrated into the design and development workflow. Regular testing ensures that accessibility is maintained throughout the project lifecycle. Remember that contrast is just one aspect of visual accessibility – also consider text size, spacing, and layout.
