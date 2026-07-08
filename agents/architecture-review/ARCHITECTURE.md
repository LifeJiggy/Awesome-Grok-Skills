# ArchitectureReview Agent Architecture

## Overview

This document describes the architecture for the ArchitectureReview Agent, a comprehensive system for evaluating software architecture quality, identifying patterns, assessing scalability, analyzing technical debt, and generating actionable recommendations.

The agent provides automated architecture reviews that combine pattern detection, multi-category analysis, scoring, and reporting. It supports multiple review types (full, security, performance, scalability, quick) and export formats (JSON, Markdown, CSV).

## System Components

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      ArchitectureReview Agent                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Pattern       │  │ Scalability  │  │ Security      │  │ Performance  │      │
│  │ Detector      │  │ Analyzer     │  │ Analyzer      │  │ Analyzer     │      │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤      │
│  │ - Regex rules │  │ - Horizontal │  │ - Auth        │  │ - Latency    │      │
│  │ - Pattern DB  │  │ - Vertical   │  │ - Authz       │  │ - Throughput │      │
│  │ - Confidence  │  │ - Data       │  │ - Crypto      │  │ - Availability│     │
│  │ - Scoring     │  │ - Network    │  │ - Network     │  │ - Error Rate │      │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤      │
│  │ Tech Debt     │  │ Compliance   │  │ Report        │  │ Review       │      │
│  │ Analyzer      │  │ Checker      │  │ Generator     │  │ Storage      │      │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤      │
│  │ - Dependencies│  │ - OWASP      │  │ - JSON        │  │ - JSON       │      │
│  │ - Coverage    │  │ - NIST       │  │ - Markdown    │  │ - History    │      │
│  │ - Docs        │  │ - ISO27001   │  │ - CSV         │  │ - Versioning │      │
│  │ - Circular    │  │ - SOC2       │  │ - PDF (opt)   │  │ - Export     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         Review Data Flow                                        │
│                                                                                 │
│  Input (design_document, architecture_dict, metrics_dict)                       │
│       │                                                                         │
│       ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐       │
│  │                    Pattern Detection                                │       │
│  │  - Scan design document for architecture patterns                  │       │
│  │  - Detect microservices, monolith, serverless, event-driven, etc.  │       │
│  │  - Assign confidence scores to detected patterns                   │       │
│  └─────────────────────────────────────────────────────────────────────┘       │
│       │                                                                         │
│       ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐       │
│  │                  Multi-Category Analysis                            │       │
│  │                                                                     │       │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐     │       │
│  │  │Security    │ │Performance │ │Scalability │ │Tech Debt   │     │       │
│  │  │Analysis    │ │Analysis    │ │Analysis    │ │Analysis    │     │       │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘     │       │
│  │                                                                     │       │
│  │  ┌────────────┐                                                    │       │
│  │  │Compliance  │                                                    │       │
│  │  │Check       │                                                    │       │
│  │  └────────────┘                                                    │       │
│  └─────────────────────────────────────────────────────────────────────┘       │
│       │                                                                         │
│       ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐       │
│  │                  Finding Generation                                 │       │
│  │  - Aggregate findings from all analyzers                           │       │
│  │  - Deduplicate and prioritize                                      │       │
│  │  - Assign severity and impact scores                               │       │
│  └─────────────────────────────────────────────────────────────────────┘       │
│       │                                                                         │
│       ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐       │
│  │                  Scoring                                            │       │
│  │  - Calculate category scores                                       │       │
│  │  - Compute overall score                                           │       │
│  │  - Determine pass/warning/fail                                     │       │
│  └─────────────────────────────────────────────────────────────────────┘       │
│       │                                                                         │
│       ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐       │
│  │                  Report Generation                                  │       │
│  │  - Executive summary                                               │       │
│  │  - Category breakdowns                                             │       │
│  │  - Findings with recommendations                                   │       │
│  │  - Remediation roadmap                                             │       │
│  │  - Export (JSON / Markdown / CSV)                                   │       │
│  └─────────────────────────────────────────────────────────────────────┘       │
│       │                                                                         │
│       ▼                                                                         │
│  Output (ReviewResult with scores, findings, recommendations)                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Core Processing

Orchestrates the full review workflow: pattern detection, category-specific analysis, finding aggregation, scoring, and report generation.

```python
class ArchitectureReviewAgent:
    def review_architecture(
        self,
        design_document: str,
        architecture: Dict,
        metrics: Optional[Dict] = None,
        review_type: str = "full"
    ) -> ReviewResult:
        # 1. Pattern detection
        patterns = self.pattern_detector.detect_patterns(design_document)
        
        # 2. Category analysis
        findings = []
        scores = {}
        
        if self.config.include_security:
            security_result = self.security_analyzer.assess_security(architecture)
            findings.extend(security_result.findings)
            scores["security"] = security_result.score
        
        # ... other analyzers
        
        # 3. Scoring
        overall_score = self._calculate_overall_score(scores)
        
        # 4. Report generation
        return ReviewResult(
            score=overall_score,
            findings=findings,
            scores=scores,
            patterns=patterns
        )
```

### 2. Analysis Modules

- **PatternDetector**: Regex-based architectural pattern detection
  - Supports: microservices, monolith, serverless, event-driven, layered, hexagonal, CQRS, etc.
  - Returns: detected patterns with confidence scores

- **ScalabilityAnalyzer**: Horizontal, vertical, data, and network scaling assessment
  - Checks: load balancer, caching, database replication, CDN
  - Returns: scalability score and bottleneck identification

- **SecurityAnalyzer**: Authentication, authorization, cryptography, network, data, and compliance scoring
  - Checks: auth mechanisms, encryption, network isolation, data protection
  - Returns: security score and vulnerability findings

- **PerformanceAnalyzer**: Latency, throughput, availability, error rate, resource usage, cold start, and database scoring
  - Checks: response times, throughput targets, error handling, resource limits
  - Returns: performance score and optimization recommendations

- **TechDebtAnalyzer**: Dependency currency, test coverage, documentation, circular dependencies, and monitoring gaps
  - Checks: outdated dependencies, missing tests, documentation coverage
  - Returns: tech debt score and remediation priorities

- **ComplianceChecker**: Framework-specific compliance verification (OWASP, NIST, ISO27001, SOC2, GDPR, HIPAA, PCI-DSS, CSA-CCM)
  - Checks: control implementation status
  - Returns: compliance score and gap analysis

### 3. Report Generation

- **ReportGenerator**: JSON, Markdown, and CSV export
  - Executive summary with overall score
  - Category breakdowns with detailed findings
  - Remediation roadmap prioritized by effort and impact
  - Trend analysis for recurring reviews

### 4. Persistence

- **ReviewStorage**: JSON persistence of review results and findings
  - Stores complete review history
  - Enables trend analysis and comparison
  - Supports version control of architecture decisions

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
| `score_threshold_warning` | float | `50.0` | Warning threshold |
| `max_findings` | int | `50` | Maximum findings to report |
| `auto_fix_suggestions` | bool | `true` | Include auto-fix suggestions |
| `benchmark_version` | str | `"2024-Q4"` | Benchmark version for comparison |

## Data Flow Diagrams

### Sequence: Full Review

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  User -> Agent: review_architecture(design_document, architecture)             │
│                                                                                 │
│  Agent -> PatternDetector: detect_patterns(design_document)                     │
│  PatternDetector -> Agent: [microservices, event_driven]                       │
│                                                                                 │
│  Agent -> SecurityAnalyzer: assess_security(architecture)                       │
│  SecurityAnalyzer -> Agent: SecurityResult(score=85, findings=[...])           │
│                                                                                 │
│  Agent -> PerformanceAnalyzer: analyze_performance(architecture, metrics)      │
│  PerformanceAnalyzer -> Agent: PerformanceResult(score=78, findings=[...])     │
│                                                                                 │
│  Agent -> ScalabilityAnalyzer: assess_scalability(architecture)                 │
│  ScalabilityAnalyzer -> Agent: ScalabilityResult(score=90, findings=[...])     │
│                                                                                 │
│  Agent -> TechDebtAnalyzer: identify_tech_debt(design_document, architecture) │
│  TechDebtAnalyzer -> Agent: TechDebtResult(score=65, findings=[...])           │
│                                                                                 │
│  Agent -> ReviewStorage: save_result(review)                                    │
│  ReviewStorage -> Agent: saved                                                  │
│                                                                                 │
│  Agent -> ReportGenerator: generate_json(review)                               │
│  ReportGenerator -> Agent: report_json                                         │
│                                                                                 │
│  Agent -> User: ReviewResult                                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Component Dependencies

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Component Dependencies                                                        │
│                                                                                 │
│  PatternDetector                                                                │
│  ├── Depends on: Architecture enum, regex rules                                │
│  └── Outputs: List[str] (detected patterns)                                    │
│                                                                                 │
│  ScalabilityAnalyzer                                                            │
│  ├── Depends on: Architecture dict (load_balancer, caching, db)                │
│  └── Outputs: ScalabilityResult (score, findings, bottleneck)                  │
│                                                                                 │
│  SecurityAnalyzer                                                               │
│  ├── Depends on: Architecture dict (auth, crypto, compliance)                  │
│  └── Outputs: SecurityResult (score, findings, vulnerabilities)                │
│                                                                                 │
│  PerformanceAnalyzer                                                            │
│  ├── Depends on: Metrics dict, Architecture dict                               │
│  └── Outputs: PerformanceResult (score, findings, bottlenecks)                 │
│                                                                                 │
│  TechDebtAnalyzer                                                               │
│  ├── Depends on: Design document string, Architecture dict                     │
│  └── Outputs: TechDebtResult (score, findings, debt_items)                     │
│                                                                                 │
│  ComplianceChecker                                                              │
│  ├── Depends on: Architecture dict, framework rules                            │
│  └── Outputs: ComplianceResult (score, gaps, remediation)                      │
│                                                                                 │
│  ReportGenerator                                                                │
│  ├── Depends on: ReviewResult dataclass                                        │
│  └── Outputs: str (JSON/Markdown/CSV)                                          │
│                                                                                 │
│  ReviewStorage                                                                  │
│  ├── Depends on: File system (JSON)                                            │
│  └── Outputs: saved/retrieved ReviewResult                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Contracts

### ReviewResult

```json
{
  "review_id": "rev-1",
  "score": 85.0,
  "grade": "B",
  "summary": "Architecture review completed with strong security posture...",
  "review_type": "full",
  "categories": {
    "security": 85.0,
    "performance": 78.0,
    "scalability": 90.0,
    "maintainability": 72.0,
    "compliance": 88.0
  },
  "patterns_detected": ["microservices", "event-driven", "api-gateway"],
  "findings": [
    {
      "category": "security",
      "severity": "high",
      "title": "Missing rate limiting on auth endpoints",
      "description": "Authentication endpoints lack rate limiting...",
      "recommendation": "Implement rate limiting with exponential backoff",
      "affected_components": ["auth-service", "api-gateway"],
      "effort": "medium",
      "impact": "high",
      "auto_fixable": false,
      "references": ["OWASP-001", "CWE-307"]
    }
  ],
  "recommendations": [
    {
      "priority": 1,
      "category": "security",
      "action": "Implement rate limiting",
      "effort": "medium",
      "impact": "high"
    }
  ],
  "technical_debt_items": [
    {
      "type": "dependency",
      "description": "3 outdated dependencies with known CVEs",
      "severity": "high",
      "remediation": "Update to latest versions"
    }
  ],
  "metrics": {
    "api_latency_p99_ms": 300.0,
    "error_rate_pct": 0.5,
    "test_coverage_pct": 72.0,
    "dependency_freshness": 0.85
  },
  "generated_at": "2026-06-04T06:00:00Z",
  "model_version": "v2"
}
```

### Finding

```json
{
  "id": "FIND-001",
  "category": "security",
  "severity": "high",
  "title": "No authentication mechanism",
  "description": "API endpoints accessible without authentication",
  "recommendation": "Add OAuth2/OIDC or JWT-based authentication",
  "affected_components": ["api-gateway", "user-service"],
  "code_example": null,
  "references": ["OWASP-A07", "CWE-306"],
  "effort": "high",
  "impact": "high",
  "auto_fixable": false,
  "detected_at": "2026-06-04T06:00:00Z"
}
```

### ArchitectureMetric

```json
{
  "name": "api_latency_p99_ms",
  "value": 300.0,
  "unit": "ms",
  "threshold": 500.0,
  "status": "healthy",
  "trend": "stable"
}
```

## Scoring Model

### Overall Score Calculation

```
overall_score = average(category_scores)

Where category_scores includes:
- security (if enabled)
- performance (if enabled)
- scalability (if enabled)
- maintainability (if enabled)
- compliance (if enabled)
```

### Category Scores

| Category | Sub-scores | Max | Weight |
|----------|-----------|-----|--------|
| Security | auth, authz, crypto, network, data, compliance | 100 | 0.25 |
| Scalability | horizontal, vertical, data, network | 100 | 0.20 |
| Performance | latency, throughput, avail, errors, resources, cold start, db | 100 | 0.25 |
| Maintainability | from technical debt analysis | 100 | 0.15 |
| Compliance | per framework | 100 | 0.15 |

### Grade Mapping

| Grade | Score Range | Interpretation |
|-------|-------------|----------------|
| A | 90-100 | Excellent - production-ready |
| B | 80-89 | Good - minor improvements needed |
| C | 70-79 | Fair - significant improvements needed |
| D | 60-69 | Poor - major issues to address |
| F | 0-59 | Critical - not production-ready |

### Severity Weights

| Severity | Impact Multiplier | Description |
|----------|------------------|-------------|
| Critical | 3.0 | Immediate action required |
| High | 2.0 | Urgent fix needed |
| Medium | 1.0 | Should be addressed |
| Low | 0.5 | Minor improvement |
| Info | 0.1 | Informational |

## Scaling Limits

| Dimension | Limit | Notes |
|-----------|-------|-------|
| Reviews in memory | ~10,000 | Per process |
| Findings per review | Configurable | Default 50 max |
| Compliance frameworks | 50+ | Memory-bound |
| Architecture patterns | 10+ | Enum-defined |
| Metrics per analysis | 20+ | Fixed set |
| Review history | Unlimited | File-based storage |
| Concurrent reviews | 16 | Thread pool limit |

## Security Considerations

- No secrets stored in ReviewResult or Finding
- Design documents are not persisted by default
- Compliance checks only assess configuration presence, not content
- Regenerate benchmark version for new assessments
- Review results may contain sensitive architecture details
- Access control recommended for review storage
- Audit logging for review access and modifications

## Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Full review latency | < 500ms | All analyzers |
| Pattern detection | < 100ms | Regex-based |
| Security analysis | < 200ms | Rule-based |
| Scalability analysis | < 150ms | Configuration check |
| Performance analysis | < 150ms | Metric evaluation |
| Tech debt analysis | < 200ms | Dependency scan |
| Compliance check | < 100ms | Rule matching |
| Report generation | < 50ms | Template-based |
| JSON export | < 10ms | Serialization |
| Storage write | < 20ms | File I/O |

## Extension Points

### Custom Patterns

Add to `PatternDetector._patterns`:

```python
PatternDetector._patterns = {
    "custom_pattern": {
        "keywords": ["keyword1", "keyword2"],
        "description": "Custom architecture pattern",
        "confidence_boost": 0.1
    }
}
```

### Custom Compliance Frameworks

Add to `ComplianceChecker._frameworks` and `_get_framework_checks`:

```python
ComplianceChecker._frameworks["CUSTOM"] = {
    "CTRL-1": ("Control Name", "Description", "category"),
    "CTRL-2": ("Another Control", "Description", "category"),
}
```

### Custom Metric Thresholds

Update `PerformanceAnalyzer._thresholds`:

```python
PerformanceAnalyzer._thresholds = {
    "api_latency_p99_ms": 300.0,
    "error_rate_pct": 1.0,
    "availability_pct": 99.9,
    "throughput_rps": 1000.0
}
```

### Custom Review Types

Add handler to `review_types` dict in `review_architecture()`:

```python
review_types = {
    "full": full_review_handler,
    "security": security_review_handler,
    "custom": custom_review_handler
}
```

## Monitoring & Observability

- `get_status()` returns agent state and latest review metadata
- `get_review_history()` returns all previous review summaries
- Findings include CWE and OWASP references for traceability
- Metrics are timestamped for trend analysis
- Audit logs for all review operations

## Glossary

- **Pattern**: Architectural style (microservices, monolith, serverless)
- **Bottleneck**: Scalability constraint limiting system performance
- **Finding**: Identified issue with severity, recommendation, and affected components
- **Debt**: Technical or architectural deficiency requiring future remediation
- **Compliance**: Adherence to standards (GDPR, HIPAA, PCI-DSS)
- **CWE**: Common Weakness Enumeration identifier
- **OWASP**: Open Web Application Security Project category
- **SLA**: Service Level Agreement defining performance targets
- **RTO**: Recovery Time Objective for disaster recovery
- **RPO**: Recovery Point Objective for data loss tolerance
