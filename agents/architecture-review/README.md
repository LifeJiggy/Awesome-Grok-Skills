# ArchitectureReview Agent

> THE definitive agent for software architecture evaluation, pattern analysis,
> scalability assessment, security review, and technical debt identification.
> Enterprise-grade, standards-compliant.

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
12. Security Assessment
13. Performance Assessment
14. Technical Debt Analysis
15. Compliance Checking
16. Batch Operations
17. Integration Hooks
18. Performance Tuning
19. Security & Privacy
20. Extending the Agent
21. Troubleshooting
22. FAQ
23. Contributing
24. License

---

## Overview

The ArchitectureReview Agent provides comprehensive evaluation of software architecture quality. It detects patterns, assesses scalability, evaluates security architecture, and identifies technical debt.

### What It Does

- Evaluates system architecture quality across multiple dimensions.
- Identifies architectural patterns and anti-patterns using regex detection.
- Assesses scalability characteristics across horizontal, vertical, data, and network dimensions.
- Evaluates security architecture across authentication, authorization, cryptography, network, data, and compliance.
- Measures performance characteristics including latency, throughput, availability, error rates, resource usage, cold start, and database performance.
- Identifies and prioritizes technical debt with effort estimation.
- Checks compliance against OWASP, NIST, ISO27001, SOC2, GDPR, HIPAA, PCI-DSS, and CSA-CCM.
- Generates structured reports in JSON, Markdown, and CSV formats.
- Provides batch review and architecture comparison capabilities.

---

## Key Features

| Capability | Description |
|------------|-------------|
| Architecture Assessment | Evaluate overall system architecture quality |
| Pattern Analysis | Identify 10+ architectural patterns automatically |
| Scalability Review | Horizontal, vertical, data, and network scaling assessment |
| Security Review | 6-dimension security scoring and vulnerability detection |
| Performance Assessment | 8-dimension performance scoring with thresholds |
| Tech Debt Assessment | Identify and prioritize technical debt with effort estimates |
| Compliance Checking | 8+ compliance frameworks support |
| Report Generation | JSON, Markdown, and CSV export |
| Batch Operations | Review multiple architectures in batch |
| Architecture Comparison | Side-by-side architecture comparison |

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

result = agent.review_architecture(design_document="arch.md", architecture=architecture)
print(f"Score: {result.score}/100")
patterns = agent.identify_patterns(architecture)
status = agent.get_status()
compliance = agent.run_compliance_check(architecture, frameworks=["OWASP", "GDPR"])
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
    review_type="full",
    include_security=True,
    include_performance=True,
    include_scalability=True,
    include_maintainability=True,
    include_reliability=True,
    include_cost=True,
    include_compliance=True,
    include_observability=True,
    output_format="json",
    score_threshold_pass=70.0,
    max_findings=50,
    auto_fix_suggestions=True,
    generate_report=True,
)

agent = ArchitectureReviewAgent(config=config)
```

### Config Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `review_type` | str | `"full"` | Review scope: full, security, performance, scalability, quick |
| `include_security` | bool | `true` | Include security analysis |
| `include_performance` | bool | `true` | Include performance analysis |
| `include_scalability` | bool | `true` | Include scalability analysis |
| `output_format` | str | `"json"` | Report export format: json, markdown, csv |
| `score_threshold_pass` | float | `70.0` | Minimum passing score (0-100) |
| `max_findings` | int | `50` | Maximum findings to report per review |
| `model_version` | str | `"v2"` | Model version for tracking |
| `reviewer` | str | `"automated"` | Reviewer identifier |
| `auto_fix_suggestions` | bool | `true` | Include auto-fix suggestions in findings |
| `generate_report` | bool | `true` | Generate report after review |

---

## Core Concepts

### Review Types

| Type | Description | Categories Included |
|------|-------------|---------------------|
| `full` | Complete architecture review | All categories |
| `security` | Security-focused review | Authentication, authorization, cryptography, network, data, compliance |
| `performance` | Performance-focused review | Latency, throughput, availability, resources, cold start, database |
| `scalability` | Scalability-focused review | Horizontal, vertical, data, network scaling |
| `quick` | Rapid triage review | Critical gaps only (auth, monitoring, backup) |

### Severity Levels

| Severity | Description | Action |
|----------|-------------|--------|
| `critical` | Blocking issue, immediate action required | Fix before production |
| `high` | Significant risk, address in next sprint | Plan remediation |
| `medium` | Moderate concern, track and address | Schedule in roadmap |
| `low` | Minor issue, minimal impact | Address opportunistically |
| `info` | Informational, no action required | Awareness only |

### Finding Categories

- **Security**: Authentication, authorization, cryptography, network security, data protection, compliance.
- **Scalability**: Horizontal, vertical, data, network scaling dimensions.
- **Performance**: Latency, throughput, availability, error rate, resources, cold start, database.
- **Maintainability**: Code structure, documentation, circular dependencies.
- **Reliability**: Fault tolerance, recovery, resilience.
- **Cost**: Resource efficiency, waste identification.
- **Compliance**: Regulatory and standard adherence.

---

## API Reference

### Core Review

- `review_architecture(design_document, architecture=None) -> ReviewResult` - Perform full architecture review.
- `identify_patterns(architecture) -> List[str]` - Detect architectural patterns.
- `assess_scalability(architecture) -> Dict` - Assess scalability with bottleneck identification.
- `identify_tech_debt(codebase) -> List[Dict]` - Identify technical debt with effort estimates.

### Compliance

- `run_compliance_check(architecture, frameworks=None) -> Dict` - Check compliance against frameworks with gap analysis.

### Export & History

- `export_report(review_id, format="json") -> Dict` - Export review report.
- `get_review_history(limit=10) -> List[Dict]` - Get review history.
- `compare_architectures(arch_a, arch_b) -> Dict` - Compare two architectures side-by-side.
- `batch_review(documents) -> List[ReviewResult]` - Batch review multiple documents.

### Status

- `get_status() -> Dict` - Get agent status with latest review metadata.

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

### Pattern 2: Architecture Comparison

```python
arch_a = {"patterns": ["microservices"], "load_balancer": True}
arch_b = {"patterns": ["monolithic"], "load_balancer": False}
comparison = agent.compare_architectures(arch_a, arch_b)
print(f"Difference: {comparison['difference']} points (A: {comparison['architecture_a_score']}, B: {comparison['architecture_b_score']})")
```

### Pattern 3: Compliance Gate

```python
compliance = agent.run_compliance_check(architecture, frameworks=["OWASP", "GDPR", "SOC2"])
if compliance["overall_score"] < 80:
    remediation = compliance["remediation_plan"]
```

### Pattern 4: Export Report

```python
export = agent.export_report(review_id="rev-1", format="markdown")
with open("architecture_review.md", "w") as f:
    f.write(export["content"])
```

### Pattern 5: Batch Review

```python
documents = [
    ("service A", {"patterns": ["microservices"]}),
    ("service B", {"patterns": ["microservices"]}),
    ("service C", {"patterns": ["monolithic"]}),
]
results = agent.batch_review(documents)
```

---

## Report Formats

### JSON Report

Standard JSON with score, categories, findings, recommendations, technical debt, metrics, and metadata.

### Markdown Report

```markdown
# Architecture Review Report

**Review ID**: rev-1
**Score**: 85/100
**Date**: 2026-06-04

## Summary
...

## Findings
- **High**: No caching layer
- **Medium**: Missing observability

## Recommendations
- Add distributed caching
- Implement structured logging

## Technical Debt
...
```

### CSV Export

One row per finding: `title,severity,category,effort,impact,auto_fixable,recommendation`.

---

## Pattern Reference

| Pattern | Detection Keywords | Best For |
|---------|-------------------|----------|
| `microservices` | service_mesh, api_gateway, docker-compose, kubernetes | Scalability, team autonomy |
| `monolithic` | monolith, single_application, all_in_one | Simplicity, small teams |
| `serverless` | serverless, lambda, cloud_functions | Event-driven, variable load |
| `event_driven` | event_driven, kafka, rabbitmq, pubsub | Async, decoupled systems |
| `layered` | controller, service_layer, repository_layer | Maintainability |
| `hexagonal` | hexagonal, ports_adapters | Testability, framework independence |
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

| Status | Condition |
|--------|-----------|
| Pass | `score >= score_threshold_pass` |
| Warning | `score_threshold_warning <= score < score_threshold_pass` |
| Fail | `score < score_threshold_warning` |

---

## Security Assessment

### Six Dimensions

1. **Authentication**: JWT, OAuth2, OIDC, MFA, RBAC, session management.
2. **Authorization**: RBAC, ABAC, policy engines, least privilege.
3. **Cryptography**: TLS 1.3+, encryption at rest, managed key services.
4. **Network Security**: WAF, DDoS protection, VPC, zero trust, security headers.
5. **Data Protection**: PII encryption, access logging, data masking, backup encryption.
6. **Compliance**: GDPR, HIPAA, SOC2, PCI-DSS, ISO27001.

### Key Questions

- Is TLS 1.3 enforced end-to-end?
- Are API keys and secrets stored in vaults?
- Is RBAC implemented with least privilege?
- Is audit logging enabled for all security events?

---

## Performance Assessment

### Eight Dimensions and Thresholds

| Metric | Warn | Critical | Description |
|--------|------|----------|-------------|
| `api_latency_p99_ms` | 500 | 1000 | 99th percentile API response time |
| `throughput_rps` | 1000 | 500 | Requests per second capacity |
| `error_rate_percent` | 1.0 | 5.0 | HTTP 4xx/5xx error rate |
| `availability_percent` | 99.9 | 99.5 | Service availability SLA |
| `memory_usage_mb` | 512 | 1024 | Peak memory consumption |
| `cpu_usage_percent` | 70.0 | 90.0 | CPU utilization |
| `cold_start_ms` | 2000 | 5000 | Cold start latency |
| `db_query_time_ms` | 100 | 500 | Database query latency |

---

## Technical Debt Analysis

### Debt Categories

| Category | Description | Typical Effort |
|----------|-------------|---------------|
| `outdated_dependencies` | Stale packages | Low |
| `missing_tests` | Insufficient test coverage | High |
| `documentation_gaps` | Missing ADRs | Medium |
| `circular_dependencies` | Coupling between modules | High |
| `legacy_patterns` | Missing observability | High |

### Debt Calculation

```python
debt_analyzer = TechDebtAnalyzer()
debt = debt_analyzer.identify_tech_debt(codebase="", architecture=a)
estimates = debt_analyzer.estimate_tech_debt(debt)
# estimates["total_hours"], estimates["total_sprint_days"]
```

---

## Compliance Checking

### Supported Frameworks

| Framework | Focus | Key Checks |
|-----------|-------|-----------|
| OWASP | Web app security | Top 10 controls |
| NIST | Cybersecurity | Identify, Protect, Detect, Respond, Recover |
| ISO27001 | Info security management | Policies, asset management |
| SOC2 | Trust services | Security, Availability, Confidentiality |
| GDPR | Data protection | Data minimization, subject rights |
| HIPAA | Healthcare data | Access controls, audit logs |
| PCI-DSS | Payment card data | Firewall, encryption |
| CSA-CCM | Cloud security | Data security, incident management |

### Compliance Output

```json
{
  "overall_score": 75.0,
  "frameworks_checked": ["OWASP", "GDPR"],
  "total_checks": 10,
  "passed_checks": 7,
  "gaps": [{"framework": "GDPR", "check_id": "gdpr_02", "name": "Data Subject Rights", "severity": "high"}],
  "remediation_plan": [{"step": 1, "action": "Implement data subject workflow", "framework": "GDPR"}]
}
```

---

## Batch Operations

### Batch Review

```python
documents = [
    ("service A", {"patterns": ["microservices"]}),
    ("service B", {"patterns": ["microservices"]}),
    ("service C", {"patterns": ["monolithic"]}),
]
results = agent.batch_review(documents)
```

### Batch Compliance

```python
frameworks = ["OWASP", "NIST", "SOC2"]
for arch in architectures:
    compliance = agent.run_compliance_check(arch, frameworks=frameworks)
```

---

## Integration Hooks

### CI/CD Gate

```python
result = agent.review_architecture(design_document=doc, architecture=arch)
if result.score < config.score_threshold_pass:
    raise Exception(f"Architecture review failed with score {result.score}")
```

### Dashboard Export

```python
export = agent.export_report(review_id, format="json")
# Push to monitoring dashboard or reporting system
```

---

## Performance

| Operation | Target | Notes |
|-----------|--------|-------|
| Full review | < 500ms | All analyzers |
| Pattern detection | < 100ms | Regex matching |
| Security analysis | < 200ms | Multi-dimension scoring |
| Scalability analysis | < 150ms | Bottleneck identification |
| Performance analysis | < 150ms | Threshold comparisons |
| Tech debt analysis | < 200ms | Codebase scanning |
| Report generation | < 50ms | JSON/MD/CSV |

---

## Security & Privacy

- No secrets stored in ReviewResult or Finding.
- Design documents are not persisted by default.
- Compliance checks only assess configuration presence.
- Regenerate benchmark version for new assessments.

---

## Extending the Agent

### Custom Patterns

Add regex patterns to `PatternDetector._patterns`.

### Custom Compliance Frameworks

Extend `ComplianceChecker._frameworks` and implement checks in `_get_framework_checks()`.

### Custom Metric Thresholds

Update `PerformanceAnalyzer._thresholds` dictionary.

### Custom Review Types

Add new handler to `review_types` dict in `review_architecture()` method.

---

## Troubleshooting

### Problem: Review score seems unexpectedly low

- Check which categories are enabled in Config.
- Review individual category scores in `result.categories`.
- Examine `result.findings` for specific issues.

### Problem: Patterns not detected

- Verify design_document contains keywords matching patterns.
- Add new patterns to `PatternDetector._patterns`.
- Check case sensitivity in regex matching.

### Problem: Compliance check returns many gaps

- Review architecture dict keys match framework checks.
- Extend framework rules for custom architecture patterns.
- Verify expected configuration values.

---

## FAQ

**Q: Does this generate real architecture?**
A: It evaluates existing architecture. Use design agents for generation.

**Q: Can I add custom compliance frameworks?**
A: Yes, extend `ComplianceChecker._frameworks` with framework name and checks.

**Q: How is the overall score calculated?**
A: Average of all enabled category scores.

**Q: Can I run security-only review?**
A: Yes, set `review_type="security"`.

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
- **OWASP**: Open Web Application Security Project.
- **Debt**: Technical or architectural deficiency.
- **Compliance**: Adherence to standards and regulations.
- **ADR**: Architecture Decision Record.

---

*ArchitectureReview Agent v2.1.0 - Part of the Awesome Grok Skills collection.*

*Last updated: 2026-06-04*
