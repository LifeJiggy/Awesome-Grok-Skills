# ArchitectureReview Agent Architecture

## Overview

This document describes the architecture for the ArchitectureReview Agent, a comprehensive system for evaluating software architecture quality, identifying patterns, assessing scalability, analyzing technical debt, and generating actionable recommendations.

## System Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ArchitectureReview Agent                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Pattern       │  │ Scalability  │  │ Security      │  │ Performance  │   │
│  │ Detector      │  │ Analyzer     │  │ Analyzer      │  │ Analyzer     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Tech Debt     │  │ Compliance   │  │ Report        │  │ Review       │   │
│  │ Analyzer      │  │ Checker      │  │ Generator     │  │ Storage      │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Input (design_document, architecture_dict)
  -> Pattern Detection -> Multi-category analysis (scalability, security, performance, debt)
       -> Findings generation -> Scoring -> Recommendations
            -> Report generation -> Export (JSON / Markdown / CSV)
```

## Key Components

### 1. Core Processing

Orchestrates the full review workflow: pattern detection, category-specific analysis, finding aggregation, scoring, and report generation.

### 2. Analysis Modules

- **PatternDetector**: Regex-based architectural pattern detection.
- **ScalabilityAnalyzer**: Horizontal, vertical, data, and network scaling assessment.
- **SecurityAnalyzer**: Authentication, authorization, cryptography, network, data, and compliance scoring.
- **PerformanceAnalyzer**: Latency, throughput, availability, error rate, resource usage, cold start, and database scoring.
- **TechDebtAnalyzer**: Dependency currency, test coverage, documentation, circular dependencies, and monitoring gaps.
- **ComplianceChecker**: Framework-specific compliance verification (OWASP, NIST, ISO27001, SOC2, GDPR, HIPAA, PCI-DSS, CSA-CCM).

### 3. Report Generation

- **ReportGenerator**: JSON, Markdown, and CSV export.

### 4. Persistence

- **ReviewStorage**: JSON persistence of review results and findings.

## Directory Structure

```
agents/architecture-review/
  agent.py              # Main agent, analyzers, storage, CLI
  ARCHITECTURE.md       # This file
  GROK.md               # Agent instructions and personality
  README.md             # User-facing documentation
```

## Configuration Reference

```yaml
architecture_review:
  review_type: "full"           # full | security | performance | scalability | quick
  include_security: true
  include_performance: true
  include_scalability: true
  include_maintainability: true
  include_reliability: true
  include_cost: true
  include_compliance: true
  include_observability: true
  output_format: "json"        # json | markdown | csv
  score_threshold_pass: 70.0
  score_threshold_warning: 50.0
  max_findings: 50
  model_version: "v2"
  reviewer: "automated"
  auto_fix_suggestions: true
  generate_report: true
  benchmark_version: "2024-Q4"
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `review_type` | str | `"full"` | Review scope: full, security, performance, scalability, quick |
| `include_security` | bool | `true` | Include security analysis |
| `include_performance` | bool | `true` | Include performance analysis |
| `include_scalability` | bool | `true` | Include scalability analysis |
| `output_format` | str | `"json"` | Report export format |
| `score_threshold_pass` | float | `70.0` | Minimum passing score |
| `max_findings` | int | `50` | Maximum findings to report |
| `auto_fix_suggestions` | bool | `true` | Include auto-fix suggestions |
| `benchmark_version` | str | `"2024-Q4"` | Benchmark version for comparison |

## Data Flow Diagrams

### Sequence: Full Review

```
User -> Agent: review_architecture(design_document, architecture)
  Agent -> PatternDetector: detect_patterns(design_document)
  Agent -> SecurityAnalyzer: assess_security(architecture)
  Agent -> PerformanceAnalyzer: analyze_performance(architecture)
  Agent -> ScalabilityAnalyzer: assess_scalability(architecture)
  Agent -> TechDebtAnalyzer: identify_tech_debt(design_document, architecture)
  Agent -> ReviewStorage: save_result(review)
  Agent -> ReportGenerator: generate_json(review)
  Agent -> User: ReviewResult
```

### Component Dependencies

```
PatternDetector     -> Architecture enum and regex rules
ScalabilityAnalyzer -> Architecture dict reads (load_balancer, caching, db)
SecurityAnalyzer    -> Architecture dict reads (auth, crypto, compliance)
PerformanceAnalyzer -> Metrics dict and architecture dict
TechDebtAnalyzer    -> Design document string and architecture dict
ComplianceChecker   -> Architecture dict and framework rules
ReportGenerator     -> ReviewResult dataclass
ReviewStorage       -> File system (JSON)
```

## Data Contracts

### ReviewResult

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

### Finding

```json
{
  "category": "security",
  "severity": "high",
  "title": "No authentication mechanism",
  "description": "",
  "recommendation": "Add OAuth2/OIDC or JWT-based authentication",
  "affected_components": ["api-gateway", "user-service"],
  "code_example": null,
  "references": [],
  "effort": "high",
  "impact": "high",
  "auto_fixable": false
}
```

### ArchitectureMetric

```json
{
  "name": "api_latency_p99_ms",
  "value": 300.0,
  "unit": "ms",
  "threshold": 500.0,
  "status": "healthy"
}
```

## Scoring Model

### Overall Score Calculation

```
overall_score = average(category_scores)
```

### Category Scores

| Category | Sub-scores | Max |
|----------|-----------|-----|
| Security | auth, authz, crypto, network, data, compliance | 100 |
| Scalability | horizontal, vertical, data, network | 100 |
| Performance | latency, throughput, avail, errors, resources, cold start, db | 100 |
| Maintainability | from technical debt analysis | 100 |
| Compliance | per framework | 100 |

### Severity Weights

| Severity | Impact Multiplier |
|----------|------------------|
| Critical | 3.0 |
| High | 2.0 |
| Medium | 1.0 |
| Low | 0.5 |
| Info | 0.1 |

## Scaling Limits

| Dimension | Limit | Notes |
|-----------|-------|-------|
| Reviews in memory | ~10,000 | Per process |
| Findings per review | Configurable | Default 50 max |
| Compliance frameworks | 50+ | Memory-bound |
| Architecture patterns | 10+ | Enum-defined |
| Metrics per analysis | 20+ | Fixed set |

## Security Considerations

- No secrets stored in ReviewResult or Finding.
- Design documents are not persisted by default.
- Compliance checks only assess configuration presence, not content.
- Regenerate benchmark version for new assessments.

## Performance

| Metric | Target |
|--------|--------|
| Full review latency | < 500ms |
| Pattern detection | < 100ms |
| Security analysis | < 200ms |
| Scalability analysis | < 150ms |
| Performance analysis | < 150ms |
| Tech debt analysis | < 200ms |
| Report generation | < 50ms |
| JSON export | < 10ms |

## Extension Points

### Custom Patterns

Add to `PatternDetector._patterns`.

### Custom Compliance Frameworks

Add to `ComplianceChecker._frameworks` and `_get_framework_checks`.

### Custom Metric Thresholds

Update `PerformanceAnalyzer._thresholds`.

### Custom Review Types

Add handler to `review_types` dict in `review_architecture()`.

## Monitoring & Observability

- `get_status()` returns agent state and latest review metadata.
- `get_review_history()` returns all previous review summaries.
- Findings include CWE and OWASP references for traceability.

## Glossary

- **Pattern**: Architectural style (microservices, monolith, serverless).
- **Bottleneck**: Scalability constraint.
- **Finding**: Identified issue with severity and recommendation.
- **Debt**: Technical or architectural deficiency.
- **Compliance**: Adherence to standards (GDPR, HIPAA, PCI-DSS).
- **CWE**: Common Weakness Enumeration identifier.
- **OWASP**: Open Web Application Security Project category.
