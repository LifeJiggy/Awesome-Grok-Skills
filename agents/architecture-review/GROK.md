# Architecture Review Agent

> THE definitive agent for software architecture evaluation, pattern analysis, scalability
> assessment, security review, and technical debt identification. Enterprise-grade,
> standards-compliant, and deeply technical.

---

## Table of Contents

1. Overview
2. Key Features
3. Quick Start
4. Installation
5. Configuration
6. Core Concepts
7. API Reference
8. Usage Patterns
9. Report Formats
10. Pattern Reference
11. Scoring Model
12. Scalability Assessment
13. Security Assessment
14. Performance Assessment
15. Technical Debt Analysis
16. Compliance Checking
17. Batch Operations
18. Integration Hooks
19. Performance Tuning
20. Security & Privacy
21. Extending the Agent
22. Troubleshooting
23. FAQ
24. Contributing
25. License

---

## Overview

The ArchitectureReview Agent provides comprehensive software architecture evaluation. It detects architectural patterns, assesses scalability, security, performance, and reliability, identifies technical debt, checks compliance against major frameworks, and generates actionable recommendations with evidence-backed findings.

---

## Key Features

| Capability | Description |
|------------|-------------|
| Pattern Detection | Regex-based detection of microservices, monolith, serverless, event-driven, layered, hexagonal, CQRS. |
| Scalability Analysis | Horizontal, vertical, data, and network scaling scoring with bottleneck identification. |
| Security Analysis | Authentication, authorization, cryptography, network security, data protection, compliance scoring. |
| Performance Analysis | Latency, throughput, availability, error rate, resource usage, cold start, database scoring. |
| Tech Debt Analysis | Dependency currency, test coverage, documentation gaps, circular dependencies, observability. |
| Compliance Checking | OWASP, NIST, ISO27001, SOC2, GDPR, HIPAA, PCI-DSS, CSA-CCM framework verification. |
| Report Generation | JSON, Markdown, and CSV export. |
| Review Types | Full, security-only, performance-only, scalability-only, quick. |

---

## Quick Start

```python
from agents.architecture_review.agent import ArchitectureReviewAgent, Config

config = Config(
    review_type="full",
    include_security=True,
    include_performance=True,
    include_scalability=True,
    max_findings=50,
    output_format="json",
)

agent = ArchitectureReviewAgent(config=config)

architecture = {
    "patterns": ["microservices", "layered"],
    "authentication": {"type": "jwt", "mfa": True, "rbac": True},
    "load_balancer": True,
    "api_gateway": True,
    "database": {"type": "postgresql", "replication": True, "sharding": False},
    "caching": True,
    "monitoring": True,
    "cryptography": {"tls_enabled": True, "tls_version": "1.3", "encryption_at_rest": True, "key_management": "aws-kms"},
    "network_security": {"waf": True, "ddos_protection": True, "vpc": True, "zero_trust": False},
    "test_coverage": {"unit": True},
    "documentation": True,
    "containerized": True,
    "orchestration": "kubernetes",
    "stateless_services": True,
}

result = agent.review_architecture(
    design_document="microservices arch review",
    architecture=architecture,
)
status = agent.get_status()
history = agent.get_review_history()
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

No external dependencies required. Pure Python implementation.

---

## Configuration

```python
from agents.architecture_review.agent import Config

config = Config(
    review_type="full",             # full | security | performance | scalability | quick
    include_security=True,
    include_performance=True,
    include_scalability=True,
    include_maintainability=True,
    include_reliability=True,
    include_cost=True,
    include_compliance=True,
    include_observability=True,
    output_format="json",          # json | markdown | csv
    score_threshold_pass=70.0,     # Minimum passing score
    score_threshold_warning=50.0,  # Warning threshold
    max_findings=50,               # Maximum findings to report
    model_version="v2",
    reviewer="automated",
    auto_fix_suggestions=True,
    generate_report=True,
    benchmark_version="2024-Q4",
)

agent = ArchitectureReviewAgent(config=config)
```

### Config Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `review_type` | str | `"full"` | Review scope |
| `include_security` | bool | `true` | Include security analysis |
| `include_performance` | bool | `true` | Include performance analysis |
| `include_scalability` | bool | `true` | Include scalability analysis |
| `include_maintainability` | bool | `true` | Include maintainability analysis |
| `include_reliability` | bool | `true` | Include reliability analysis |
| `include_cost` | bool | `true` | Include cost analysis |
| `include_compliance` | bool | `true` | Include compliance analysis |
| `include_observability` | bool | `true` | Include observability analysis |
| `output_format` | str | `"json"` | Report export format |
| `score_threshold_pass` | float | `70.0` | Minimum passing score |
| `max_findings` | int | `50` | Maximum findings to report |
| `model_version` | str | `"v2"` | Model version for tracking |
| `reviewer` | str | `"automated"` | Reviewer identifier |

---

## Core Concepts

### Review Types

| Type | Description | Categories Included |
|------|-------------|---------------------|
| `full` | Complete architecture review | All categories |
| `security` | Security-focused review | Authentication, authorization, cryptography, network, data, compliance |
| `performance` | Performance-focused review | Latency, throughput, availability, resources, cold start, database |
| `scalability` | Scalability-focused review | Horizontal, vertical, data, network scaling |
| `quick` | Rapid triage review | High-level checks for critical gaps |

### Severity Levels

| Severity | Description | Action |
|----------|-------------|--------|
| `critical` | Blocking issue, immediate action required | Fix before production |
| `high` | Significant risk, address in next sprint | Plan remediation |
| `medium` | Moderate concern, track and address | Schedule in roadmap |
| `low` | Minor issue, minimal impact | Address opportunistically |
| `info` | Informational, no action required | Awareness only |

### Finding Categories

| Category | Description |
|----------|-------------|
| `security` | Authentication, authorization, cryptography, network, data, compliance |
| `scalability` | Horizontal, vertical, data, network scaling |
| `performance` | Latency, throughput, availability, resources, cold start, database |
| `maintainability` | Code structure, documentation, debt |
| `reliability` | Fault tolerance, recovery, resilience |
| `cost` | Resource efficiency, waste |
| `compliance` | Regulatory and standard adherence |
| `usability` | Developer and operator experience |
| `accessibility` | Inclusivity and access |
| `observability` | Logging, metrics, tracing |

---

## API Reference

### Core Review

- `review_architecture(design_document, architecture=None) -> ReviewResult` - Perform full architecture review.
- `identify_patterns(architecture) -> List[str]` - Detect architectural patterns.
- `assess_scalability(architecture) -> Dict` - Assess scalability characteristics.
- `identify_tech_debt(codebase) -> List[Dict]` - Identify technical debt items.

### Compliance

- `run_compliance_check(architecture, frameworks=None) -> Dict` - Check compliance against frameworks.

### Export & History

- `export_report(review_id, format="json") -> Dict` - Export review report.
- `get_review_history(limit=10) -> List[Dict]` - Get review history.
- `compare_architectures(arch_a, arch_b) -> Dict` - Compare two architectures.
- `batch_review(documents) -> List[ReviewResult]` - Batch review multiple documents.

### Status

- `get_status() -> Dict` - Get agent status.

---

## Usage Patterns

### Pattern 1: Full Review

```python
architecture = {
    "patterns": ["microservices"],
    "authentication": {"type": "jwt", "mfa": True},
    "load_balancer": True,
    "caching": True,
}
result = agent.review_architecture(design_document="arch.md", architecture=architecture)
print(f"Score: {result.score}/100")
for finding in result.findings:
    print(f"- {finding['severity']}: {finding['title']}")
```

### Pattern 2: Security-Only Review

```python
config = Config(review_type="security", include_security=True)
agent = ArchitectureReviewAgent(config=config)
result = agent.review_architecture(design_document="arch.md", architecture=architecture)
```

### Pattern 3: Compare Architectures

```python
arch_a = {"patterns": ["microservices"], "load_balancer": True}
arch_b = {"patterns": ["monolithic"], "load_balancer": False}
comparison = agent.compare_architectures(arch_a, arch_b)
print(f"Difference: {comparison['difference']} points")
```

### Pattern 4: Compliance Check

```python
compliance = agent.run_compliance_check(architecture, frameworks=["OWASP", "GDPR", "SOC2"])
print(f"Overall score: {compliance['overall_score']}%")
for gap in compliance["gaps"]:
    print(f"- {gap['framework']}: {gap['name']}")
```

### Pattern 5: Export Report

```python
export = agent.export_report(review_id="rev-1", format="markdown")
with open("review.md", "w") as f:
    f.write(export["content"])
```

---

## Report Formats

### JSON Report

```json
{
  "review_id": "rev-1",
  "score": 85.0,
  "summary": "Architecture review completed...",
  "categories": {
    "security": 85.0,
    "performance": 78.0,
    "scalability": 90.0
  },
  "patterns_detected": ["microservices", "layered"],
  "findings": [],
  "recommendations": [],
  "technical_debt_items": [],
  "metrics": {},
  "generated_at": "2026-06-04T06:00:00Z"
}
```

### Markdown Report

Standard Markdown with `# Review` headings, `## Findings`, `## Recommendations`, and `## Technical Debt` sections.

### CSV Export

One row per finding: `title,severity,category,effort,impact,auto_fixable,recommendation`.

---

## Pattern Reference

| Pattern | Detection Keywords | Best For |
|---------|-------------------|----------|
| `microservices` | service_mesh, api_gateway, docker-compose, kubernetes | Scalability, team autonomy |
| `monolithic` | monolith, single_application | Simplicity, small teams |
| `serverless` | serverless, lambda, cloud_functions | Event-driven, variable load |
| `event_driven` | event_driven, kafka, rabbitmq | Async, decoupled systems |
| `layered` | controller, service_layer, repository_layer | Maintainability |
| `hexagonal` | hexagonal, ports_adapters | Testability, independence |
| `cqrs` | cqrs, command_query, read_model | Complex read/write patterns |
| `event_sourcing` | event_sourcing, event_store | Audit trail, temporal queries |

---

## Scoring Model

### Overall Score

```
overall_score = average(category_scores)
```

### Severity Multipliers

| Severity | Multiplier |
|----------|-----------|
| Critical | 3.0 |
| High | 2.0 |
| Medium | 1.0 |
| Low | 0.5 |
| Info | 0.1 |

### Score Thresholds

| Threshold | Meaning |
|-----------|---------|
| `> score_threshold_pass` | Pass |
| `score_threshold_warning < score < score_threshold_pass` | Warning |
| `< score_threshold_warning` | Fail |

---

## Scalability Assessment

### Dimensions

| Dimension | Description |
|-----------|-------------|
| Horizontal | Load balancing, statelessness, containerization |
| Vertical | Auto-scaling, resource limits, elasticity |
| Data | Replication, sharding, caching, CDN |
| Network | API gateway, message queue, service mesh, edge computing |

### Bottleneck Severity

| Severity | Action |
|----------|--------|
| Critical | Immediate remediation required |
| High | Plan next sprint |
| Medium | Schedule in roadmap |
| Low | Monitor and address opportunistically |

---

## Security Assessment

### Sub-scores

| Sub-score | Description | Key Checks |
|-----------|-------------|-----------|
| Authentication | Identity verification | JWT, OAuth2, MFA, RBAC, session management |
| Authorization | Access control | RBAC, ABAC, policy engine, least privilege |
| Cryptography | Data protection | TLS 1.3, encryption at rest, key management |
| Network Security | Perimeter defense | WAF, DDoS, VPC, zero trust, security headers |
| Data Protection | Privacy and integrity | PII encryption, access logging, data masking, backup |
| Compliance | Regulatory adherence | GDPR, HIPAA, PCI-DSS, SOC2, ISO27001 |

---

## Performance Assessment

### Metrics and Thresholds

| Metric | Warn | Critical |
|--------|------|----------|
| `api_latency_p99_ms` | 500 | 1000 |
| `throughput_rps` | 1000 | 500 |
| `error_rate_percent` | 1.0 | 5.0 |
| `availability_percent` | 99.9 | 99.5 |
| `memory_usage_mb` | 512 | 1024 |
| `cpu_usage_percent` | 70.0 | 90.0 |
| `cold_start_ms` | 2000 | 5000 |
| `db_query_time_ms` | 100 | 500 |

---

## Technical Debt Analysis

### Debt Categories

| Category | Description | Typical Effort |
|----------|-------------|---------------|
| `outdated_dependencies` | Stale packages | Low |
| `missing_tests` | Insufficient test coverage | High |
| `documentation_gaps` | Missing ADRs or docs | Medium |
| `circular_dependencies` | Coupling between modules | High |
| `legacy_patterns` | Missing observability | High |

### Debt Measurement

```
total_hours = sum(debt_items[estimated_hours])
sprint_days = total_hours / 8
```

---

## Compliance Checking

### Supported Frameworks

| Framework | Focus |
|-----------|-------|
| OWASP | Web application security (Top 10) |
| NIST | Cybersecurity framework (Identify, Protect, Detect, Respond, Recover) |
| ISO27001 | Information security management |
| SOC2 | Trust service criteria (Security, Availability, Confidentiality) |
| GDPR | EU data protection regulation |
| HIPAA | US healthcare data protection |
| PCI-DSS | Payment card industry data security |
| CSA-CCM | Cloud security alliance control matrix |

### Compliance Output

```json
{
  "overall_score": 75.0,
  "frameworks_checked": ["OWASP", "GDPR"],
  "total_checks": 10,
  "passed_checks": 7,
  "gaps": [],
  "remediation_plan": []
}
```

---

## Batch Operations

### Batch Review

```python
documents = [
    ("arch A", {"patterns": ["microservices"]}),
    ("arch B", {"patterns": ["monolithic"]}),
]
results = agent.batch_review(documents)
```

### Batch Compliance

```python
for arch in architectures:
    compliance = agent.run_compliance_check(arch, frameworks=["OWASP", "GDPR"])
```

---

## Integration Hooks

### CI/CD Gate

```python
result = agent.review_architecture(design_document=doc, architecture=arch)
if result.score < config.score_threshold_pass:
    raise Exception("Architecture review failed")
```

### Dashboard Export

```python
export = agent.export_report(review_id, format="json")
push_to_dashboard(export)
```

---

## Performance

| Operation | Target |
|-----------|--------|
| Full review | < 500ms |
| Pattern detection | < 100ms |
| Security analysis | < 200ms |
| Scalability analysis | < 150ms |
| Performance analysis | < 150ms |
| Tech debt analysis | < 200ms |
| Report generation | < 50ms |

---

## Security & Privacy

- No secrets stored in ReviewResult or Finding.
- Design documents are not persisted by default.
- Compliance checks only assess configuration presence.
- Regenerate benchmark version for new assessments.

---

## Extending the Agent

### Custom Patterns

Add to `PatternDetector._patterns`.

### Custom Compliance Frameworks

Add to `ComplianceChecker._frameworks` and `_get_framework_checks`.

### Custom Metric Thresholds

Update `PerformanceAnalyzer._thresholds`.

### Custom Review Types

Add handler to `review_types` dict in `review_architecture()`.

---

## Troubleshooting

### Problem: Review score seems low

- Check which categories are enabled in Config.
- Review specific category scores in `result.categories`.
- Examine findings for remediation steps.

### Problem: Patterns not detected

- Verify design_document contains keywords matching patterns.
- Add new keyword patterns to `PatternDetector._patterns`.
- Check for typos or case sensitivity issues.

### Problem: Compliance check fails for valid configuration

- Review framework rules in `ComplianceChecker._get_framework_checks()`.
- Extend rule set to match your architecture.
- Check for false positives in `gaps` list.

---

## FAQ

**Q: Does this generate real architecture?**
A: It evaluates existing architecture. Use create/design agents for generation.

**Q: Can I add custom compliance frameworks?**
A: Yes, extend `ComplianceChecker._frameworks` and register checks.

**Q: How is the overall score calculated?**
A: Average of enabled category scores.

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

## Glossary

- **Pattern**: Architectural style (microservices, monolith, serverless).
- **Bottleneck**: Scalability constraint.
- **Finding**: Identified issue with severity and recommendation.
- **CWE**: Common Weakness Enumeration identifier.
- **OWASP**: Open Web Application Security Project category.
- **Debt**: Technical or architectural deficiency.
- **Compliance**: Adherence to standards (GDPR, HIPAA, PCI-DSS).

---

*ArchitectureReview Agent v2.1.0 - Part of the Awesome Grok Skills collection.*

*Last updated: 2026-06-04*
