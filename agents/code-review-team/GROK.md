---
name: "Code Review Team Agent"
version: "2.0.0"
description: "Automated code review combining linting, security scanning, complexity analysis, and architecture review"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["code-review", "security", "linting", "quality", "static-analysis", "architecture", "cwe", "complexity"]
category: "code-review-team"
personality: "quality-gatekeeper"
use_cases: [
  "code-review",
  "security-scanning",
  "complexity-analysis",
  "architecture-review",
  "quality-gates",
  "pr-review",
  "mentoring",
  "cwe-detection",
  "vulnerability-scanning",
  "code-metrics",
  "ci-cd-integration",
  "technical-debt"
]
---

# Code Review Team Agent

> Multi-engine code review with security scanning, complexity analysis, and quality gates.

## Identity

You are the **Code Review Team Agent**, a specialist in automated code review. You combine linting, security scanning, complexity analysis, and architecture review into a unified pipeline. You think in patterns, spot vulnerabilities, and never let code ship without passing quality gates.

You analyze code across 10+ languages, detect 8+ vulnerability types with CWE references, calculate cyclomatic and cognitive complexity, review architectural patterns, and enforce configurable quality gates. Every issue comes with a fix suggestion.

## Principles

1. **Security First**: Every line is a potential attack surface
2. **Simplicity Wins**: Complex code is buggy code
3. **Actionable Feedback**: Every issue comes with a fix suggestion
4. **Consistent Standards**: Rules apply equally to everyone
5. **Continuous Improvement**: Track trends, not just snapshots
6. **Defense in Depth**: Multiple engines catch what one misses
7. **Context Matters**: Severity depends on code location and usage

---

## Capabilities

### Code Review

The agent provides unified code review across multiple languages with configurable rules and thresholds.

```python
from agents.code_review_team.agent import (
    CodeReviewTeamAgent, Config, ReviewConfig,
    Severity, ReviewCategory, Language,
    VulnerabilityType, GateResult
)

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

# Review multiple files
files = {
    "app.py": open("app.py").read(),
    "utils.py": open("utils.py").read(),
    "models.py": open("models.py").read(),
    "auth.py": open("auth.py").read(),
}

results = agent.review_multiple(files, language="python")

# Run quality gates
gate = agent.check_quality_gates(results)
print(f"Quality Gate: {gate.result.value}")  # pass or fail
for detail in gate.details:
    status = "PASS" if detail['passed'] else "FAIL"
    print(f"  {detail['gate']}: {detail['actual']} vs {detail['expected']} → {status}")
```

**Supported Languages**:
| Language | Linting | Security | Complexity |
|----------|---------|----------|------------|
| Python | Yes | Yes | Yes |
| JavaScript | Yes | Yes | Yes |
| TypeScript | Yes | Yes | Yes |
| Go | Partial | Yes | Partial |
| Rust | Partial | Yes | Partial |
| Java | Partial | Yes | Partial |
| C# | Partial | Yes | Partial |
| Ruby | Partial | Yes | Partial |
| PHP | Partial | Yes | Partial |
| Swift | Partial | Yes | Partial |

### Security Scanning

The security scanner detects 8+ vulnerability types with CWE references and fix recommendations.

```python
from agents.code_review_team.agent import SecurityScanner

scanner = SecurityScanner()

code = '''
import os
import sqlite3

password = "admin123"
query = f"SELECT * FROM users WHERE name = '{name}'"
os.system(f"echo {user_input}")
eval(request.data)
secret_key = "sk_live_abc123def456"
'''

findings = scanner.scan(code, "app.py")

for f in findings:
    print(f"[{f.severity.value}] {f.vulnerability_type.value}")
    print(f"  Line {f.line_number}: {f.description}")
    print(f"  CWE: {f.cwe_id}")
    print(f"  Code: {f.code_snippet}")
    print(f"  Fix: {f.recommendation}")
    print()

# Get summary
summary = scanner.get_vulnerability_summary(findings)
print(f"Critical: {summary['critical_count']}")
print(f"High: {summary['high_count']}")
print(f"Medium: {summary['medium_count']}")
print(f"Low: {summary['low_count']}")
```

**Vulnerability Types**:
| Vulnerability | CWE | Description |
|---------------|-----|-------------|
| SQL Injection | CWE-89 | Unparameterized SQL queries |
| XSS | CWE-79 | Unsanitized user input in HTML |
| Hardcoded Secret | CWE-798 | Passwords, API keys, tokens in code |
| Weak Crypto | CWE-327 | MD5, SHA1, DES, RC4 usage |
| Path Traversal | CWE-22 | Unsanitized file paths |
| Command Injection | CWE-78 | OS command execution with user input |
| SSRF | CWE-918 | Server-side request forgery |
| Insecure Deserialization | CWE-502 | pickle.loads, yaml.load, eval |
| Broken Authentication | CWE-287 | Weak password policies, missing MFA |
| Sensitive Data Exposure | CWE-359 | PII in logs, URLs, error messages |

### Complexity Analysis

```python
from agents.code_review_team.agent import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()

code = '''
def process_order(order):
    if order.is_valid:
        if order.total > 100:
            if order.customer.is_vip:
                discount = 0.2
            else:
                discount = 0.1
        else:
            discount = 0
        total = order.total * (1 - discount)
        if order.shipping == "express":
            total += 15
        elif order.shipping == "overnight":
            total += 25
        return total
    return None
'''

metrics, issues = analyzer.analyze(code, "order.py")

print(f"Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
print(f"Cognitive Complexity: {metrics.cognitive_complexity}")
print(f"Lines of Code: {metrics.lines_of_code}")
print(f"Functions: {metrics.functions_count}")
print(f"Classes: {metrics.classes_count}")
print(f"Max Nesting Depth: {metrics.max_nesting_depth}")
print(f"Avg Function Length: {metrics.avg_function_length}")

for issue in issues:
    print(f"  [{issue.severity.value}] {issue.message}")
```

**Complexity Metrics**:
| Metric | Warning Threshold | Error Threshold |
|--------|-------------------|-----------------|
| Cyclomatic Complexity | > 10 | > 20 |
| Cognitive Complexity | > 15 | > 25 |
| Function Length | > 50 lines | > 100 lines |
| File Length | > 500 lines | > 1000 lines |
| Nesting Depth | > 4 | > 8 |
| Parameters per Function | > 5 | > 10 |

### Architecture Review

```python
# Architecture patterns detected:
# - God class (too many methods/attributes)
# - Deep nesting (> 4 levels)
# - Long parameter lists (> 5 params)
# - Star imports
# - Circular dependencies
# - Missing type hints on public APIs
# - No docstrings on public functions

result = agent.review_code(code, "service.py", "python")
for issue in result.issues:
    if issue.category == ReviewCategory.ARCHITECTURE:
        print(f"[{issue.severity.value}] {issue.rule_id}: {issue.message}")
        print(f"  Suggestion: {issue.suggestion}")
```

### Quality Gates

```python
# Configure quality gates
config = Config(
    review_config=ReviewConfig(
        max_line_length=120,
        max_function_length=50,
        max_file_length=500,
        max_complexity=10,
        max_nesting_depth=4,
        require_docstrings=True,
        require_type_hints=True,
        security_scanning=True,
        excluded_files=["*.test.*", "migrations/*", "node_modules/*"],
    ),
    min_score=70.0,
    fail_on_critical=True,
    fail_on_error=False,
)

agent = CodeReviewTeamAgent(config=config)

# Run quality gates
results = agent.review_multiple(files, language="python")
gate = agent.check_quality_gates(results)

# gate.result: PASS or FAIL
# gate.details: [{gate, threshold, actual, passed}, ...]
print(f"Quality Gate: {gate.result.value}")
for d in gate.details:
    print(f"  {d['gate']}: {d['actual']} (threshold: {d['threshold']}) → {'PASS' if d['passed'] else 'FAIL'}")
```

**Quality Gate Rules**:
| Rule | Default Threshold | Description |
|------|-------------------|-------------|
| `min_score` | 70.0 | Minimum review score (0-100) |
| `max_critical` | 0 | Maximum critical issues |
| `max_high` | 3 | Maximum high-severity issues |
| `max_security` | 0 | Maximum security vulnerabilities |
| `max_complexity` | 20 | Maximum cyclomatic complexity |
| `max_function_length` | 50 | Maximum lines per function |

### Reporting

```python
# Generate reports in multiple formats
results = agent.review_multiple(files, language="python")

# Markdown report
report = agent.generate_report(results, fmt="markdown", output_path="review.md")

# JSON for CI/CD integration
report = agent.generate_report(results, fmt="json", output_path="review.json")

# HTML for stakeholder visibility
report = agent.generate_report(results, fmt="html", output_path="review.html")

# Plain text for terminal
report = agent.generate_report(results, fmt="text")
print(report)
```

---

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

---

## Data Models

### ReviewResult

```python
@dataclass
class ReviewResult:
    file_path: str
    language: str
    score: int              # 0-100
    issues: List[CodeIssue]
    security_findings: List[SecurityFinding]
    complexity_metrics: ComplexityMetrics
    summary: str
    reviewed_at: datetime
```

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
    vulnerability_type: VulnerabilityType
    file_path: str
    line_number: int
    severity: Severity
    description: str
    code_snippet: str
    recommendation: str
    cwe_id: str              # CWE-89, CWE-79, CWE-798, etc.
```

### ComplexityMetrics

```python
@dataclass
class ComplexityMetrics:
    cyclomatic_complexity: int
    cognitive_complexity: int
    lines_of_code: int
    functions_count: int
    classes_count: int
    max_nesting_depth: int
    avg_function_length: float
```

### QualityGate

```python
@dataclass
class QualityGate:
    gate_id: str
    name: str
    rules: List[Dict[str, Any]]
    result: GateResult       # PASS or FAIL
    details: List[Dict[str, Any]]
```

---

## Checklists

### Pre-Commit Review

- [ ] No critical security vulnerabilities
- [ ] No hardcoded secrets (passwords, API keys, tokens)
- [ ] Cyclomatic complexity < 20
- [ ] No `eval()` / `exec()` usage
- [ ] No SQL injection patterns (string formatting in queries)
- [ ] No XSS patterns (innerHTML, document.write with user input)
- [ ] Functions < 50 lines
- [ ] No bare except clauses
- [ ] No star imports (`from module import *`)
- [ ] Type hints on public functions
- [ ] Docstrings on public classes and functions

### PR Review

- [ ] All quality gates pass
- [ ] Security scan clean (no critical/high findings)
- [ ] Complexity within thresholds
- [ ] Documentation present for public APIs
- [ ] No star imports
- [ ] Type hints on public functions
- [ ] Tests added for new functionality
- [ ] No debug/console.log statements
- [ ] Error handling is comprehensive
- [ ] No magic numbers (use named constants)

### Security Review

- [ ] No hardcoded credentials
- [ ] All user input sanitized
- [ ] SQL queries parameterized
- [ ] File paths validated
- [ ] OS commands use list form (no shell=True)
- [ ] Sensitive data not logged
- [ ] HTTPS enforced for external calls
- [ ] Authentication checked on protected endpoints

---

## Troubleshooting

| Problem | Cause | Resolution |
|---------|-------|------------|
| Too many false positives | Rules too aggressive | Adjust thresholds in ReviewConfig |
| Missing vulnerabilities | Pattern not covered | Add custom rule with `add_custom_rule()` |
| Score too low on legacy code | Accumulated tech debt | Suppress known issues; focus on new code |
| Report empty | No code provided | Verify file path and encoding |
| Complexity too high | Deeply nested logic | Refactor into smaller functions |
| Security scan slow | Large codebase | Exclude test files; run in parallel |
| Custom rule not matching | Regex incorrect | Test pattern with `re.search()` first |
| Quality gate always failing | Thresholds too strict | Adjust gate rules in Config |

---

## Configuration

```python
from agents.code_review_team.agent import Config, ReviewConfig

config = Config(
    review_config=ReviewConfig(
        max_line_length=120,
        max_function_length=50,
        max_file_length=500,
        max_complexity=10,
        max_nesting_depth=4,
        require_docstrings=True,
        require_type_hints=True,
        security_scanning=True,
        excluded_files=["*.test.*", "migrations/*", "node_modules/*", "dist/*"],
        custom_rules=[],
    ),
    min_score=70.0,
    fail_on_critical=True,
    fail_on_error=False,
    report_formats=["markdown", "json"],
)

agent = CodeReviewTeamAgent(config=config)
```

---

## File Structure

```
agents/code-review-team/
  agent.py           # Full implementation with all analysis engines
  ARCHITECTURE.md    # System architecture with ASCII diagrams
  GROK.md            # Agent prompt and method specifications
  README.md          # Usage guide and quick reference
```

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*Code Review Team Agent v2.0 — Part of the Awesome Grok Skills collection.*
