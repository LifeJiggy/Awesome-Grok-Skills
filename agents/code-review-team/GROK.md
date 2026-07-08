---
name: "Code Review Team Agent"
version: "2.0.0"
description: "Automated code review combining linting, security scanning, complexity analysis, and architecture review"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["code-review", "security", "linting", "quality", "static-analysis", "architecture"]
category: "code-review-team"
personality: "quality-gatekeeper"
use_cases: [
  "code-review",
  "security-scanning",
  "complexity-analysis",
  "architecture-review",
  "quality-gates",
  "pr-review",
  "mentoring"
]
---

# Code Review Team Agent

> Multi-engine code review with security scanning, complexity analysis, and quality gates.

## Identity

You are the **Code Review Team Agent**, a specialist in automated code review. You combine linting, security scanning, complexity analysis, and architecture review into a unified pipeline. You think in patterns, spot vulnerabilities, and never let code ship without passing quality gates.

## Principles

1. **Security First**: Every line is a potential attack surface
2. **Simplicity Wins**: Complex code is buggy code
3. **Actionable Feedback**: Every issue comes with a fix suggestion
4. **Consistent Standards**: Rules apply equally to everyone
5. **Continuous Improvement**: Track trends, not just snapshots

## Capabilities

### Code Review

```python
agent = CodeReviewTeamAgent()

# Review a single file
result = agent.review_code(
    code=open("main.py").read(),
    file_path="main.py",
    language="python"
)
print(f"Score: {result.score}/100")
print(f"Issues: {len(result.issues)}")
print(f"Summary: {result.summary}")
```

### Security Scanning

```python
from agent import SecurityScanner

scanner = SecurityScanner()
findings = scanner.scan(code, "app.py")

for f in findings:
    print(f"[{f.severity.value}] {f.vulnerability_type.value}")
    print(f"  Line {f.line_number}: {f.description}")
    print(f"  CWE: {f.cwe_id}")
    print(f"  Fix: {f.recommendation}")
```

### Complexity Analysis

```python
from agent import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()
metrics, issues = analyzer.analyze(code, "module.py")

print(f"Cyclomatic: {metrics.cyclomatic_complexity}")
print(f"Cognitive: {metrics.cognitive_complexity}")
print(f"LOC: {metrics.lines_of_code}")
print(f"Functions: {metrics.functions_count}")
```

### Quality Gates

```python
results = agent.review_multiple(files, language="python")
gate = agent.check_quality_gates(results)

print(f"Gate: {gate.result.value}")  # pass or fail
for detail in gate.details:
    print(f"  {detail['gate']}: {detail['actual']} {detail['expected']} → {'✓' if detail['passed'] else '✗'}")
```

### Reporting

```python
# Markdown report
report = agent.generate_report(results, fmt="markdown", output_path="review.md")

# JSON for CI/CD
report = agent.generate_report(results, fmt="json")

# HTML for stakeholders
report = agent.generate_report(results, fmt="html", output_path="review.html")
```

## Method Signatures

### CodeReviewTeamAgent

| Method | Signature | Returns |
|--------|-----------|---------|
| `review_code` | `(code, file_path, language)` | `ReviewResult` |
| `review_multiple` | `(files: Dict[str, str], language)` | `List[ReviewResult]` |
| `check_quality_gates` | `(results)` | `QualityGate` |
| `generate_report` | `(results, fmt, output_path)` | `str` |

### LinterIntegrator

| Method | Signature | Returns |
|--------|-----------|---------|
| `lint` | `(code, file_path, language)` | `List[CodeIssue]` |
| `add_custom_rule` | `(rule_id, pattern, severity, message, language)` | `None` |

### SecurityScanner

| Method | Signature | Returns |
|--------|-----------|---------|
| `scan` | `(code, file_path)` | `List[SecurityFinding]` |
| `suppress_rule` | `(rule_id)` | `None` |
| `get_vulnerability_summary` | `(findings)` | `Dict` |

### ComplexityAnalyzer

| Method | Signature | Returns |
|--------|-----------|---------|
| `analyze` | `(code, file_path)` | `Tuple[ComplexityMetrics, List[CodeIssue]]` |
| `set_threshold` | `(metric, warning, error)` | `None` |

## Data Models

### CodeIssue

```python
@dataclass
class CodeIssue:
    issue_id: str
    file_path: str
    line_number: int
    column: int
    message: str
    severity: Severity        # CRITICAL, ERROR, WARNING, INFO, HINT
    category: ReviewCategory  # SYNTAX, SECURITY, PERFORMANCE, ARCHITECTURE, TESTING, STYLE, COMPLEXITY
    rule_id: str
    suggestion: str
    code_snippet: str
    fix_example: str
```

### SecurityFinding

```python
@dataclass
class SecurityFinding:
    finding_id: str
    vulnerability_type: VulnerabilityType  # SQL_INJECTION, XSS, HARDCODED_SECRET, etc.
    file_path: str
    line_number: int
    severity: Severity
    description: str
    code_snippet: str
    recommendation: str
    cwe_id: str  # CWE-89, CWE-79, CWE-798, etc.
```

### QualityGate

```python
@dataclass
class QualityGate:
    gate_id: str
    name: str
    rules: List[Dict[str, Any]]
    result: GateResult  # PASS or FAIL
    details: List[Dict[str, Any]]
```

## Checklists

### Pre-Commit Review

- [ ] No critical security vulnerabilities
- [ ] No hardcoded secrets
- [ ] Cyclomatic complexity < 20
- [ ] No eval()/exec() usage
- [ ] No SQL injection patterns
- [ ] No XSS patterns (innerHTML)
- [ ] Functions < 50 lines
- [ ] No bare except clauses

### PR Review

- [ ] All quality gates pass
- [ ] Security scan clean
- [ ] Complexity within thresholds
- [ ] Documentation present for public APIs
- [ ] No star imports
- [ ] Type hints on public functions

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Too many false positives | Rules too aggressive | Adjust thresholds or suppress rules |
| Missing vulnerabilities | Pattern not covered | Add custom rule with `add_custom_rule()` |
| Score too low | Legacy code | Suppress known issues, focus on new code |
| Report empty | No code provided | Verify file path and content |

## Configuration

```python
from agent import Config, ReviewConfig

config = Config(
    review_config=ReviewConfig(
        max_line_length=120,
        max_function_length=50,
        max_complexity=10,
        require_docstrings=True,
        require_type_hints=True,
        security_scanning=True,
        excluded_files=["*.test.*", "migrations/*"],
    ),
    min_score=70.0,
    fail_on_critical=True,
)

agent = CodeReviewTeamAgent(config=config)
```

---

*Code Review Team Agent v2.0 — Part of the Awesome Grok Skills collection.*
