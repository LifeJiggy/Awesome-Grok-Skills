# Code Review Team Agent — Architecture

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Deep Dives](#component-deep-dives)
- [Data Flow](#data-flow)
- [Data Models](#data-models)
- [Design Patterns](#design-patterns)
- [Tech Stack](#tech-stack)
- [Security Architecture](#security-architecture)
- [Scalability](#scalability)
- [Deployment](#deployment)

---

## Overview

The Code Review Team Agent combines multiple analysis engines — linting, security scanning, complexity analysis, and architecture review — into a unified code review pipeline. It produces actionable feedback with quality gates and multi-format reporting.

### Core Capabilities

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Code Review Team Agent                            │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Linter     │  │  Security    │  │  Complexity  │             │
│  │ Integrator   │  │  Scanner     │  │  Analyzer    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Architecture │  │   Quality    │  │   Report     │             │
│  │  Reviewer    │  │    Gate      │  │  Generator   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## System Architecture

### High-Level Architecture

```
                         ┌─────────────────────┐
                         │ Code Review Team    │
                         │      Agent          │
                         └──────────┬──────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
   ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
   │   Linter   │          │   Security    │          │  Complexity  │
   │ Integrator │          │   Scanner     │          │   Analyzer   │
   │            │          │               │          │              │
   │ • Python   │          │ • SQLi        │          │ • Cyclomatic │
   │ • JS/TS    │          │ • XSS         │          │ • Cognitive  │
   │ • Custom   │          │ • Secrets     │          │ • LOC        │
   │            │          │ • Crypto      │          │ • Nesting    │
   └─────┬──────┘          └───────┬───────┘          └───────┬──────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
   ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
   │ Architecture│          │   Quality     │          │   Report     │
   │  Reviewer  │          │    Gate       │          │  Generator   │
   │            │          │               │          │              │
   │ • SOLID    │          │ • Pass/Fail   │          │ • Markdown   │
   │ • Patterns │          │ • Thresholds  │          │ • JSON       │
   │ • Coupling │          │ • Metrics     │          │ • HTML       │
   └────────────┘          └───────────────┘          └──────────────┘
```

---

## Component Deep Dives

### 1. Linter Integrator

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Linter Integrator                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Python Rules                                                │   │
│  │  • W1001: print() usage → use logging                       │   │
│  │  • W1002: bare except → specify exception types              │   │
│  │  • W1003: mutable default args → use None                    │   │
│  │  • W1004: star imports → explicit imports                    │   │
│  │  • E1001: eval() usage → safe alternatives                   │   │
│  │  • E1002: exec() usage → specific functions                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  JavaScript/TypeScript Rules                                 │   │
│  │  • I2001: console.log → remove before production             │   │
│  │  • W2001: var → const/let                                    │   │
│  │  • W2002: == → === (strict equality)                        │   │
│  │  • W2003: alert() → proper UI notifications                  │   │
│  │  • E2001: innerHTML → textContent (XSS prevention)          │   │
│  │  • E2002: document.write → DOM manipulation                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Custom Rules:                                                      │
│  add_custom_rule(rule_id, pattern, severity, message, language)    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2. Security Scanner

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Security Scanner                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Vulnerability Patterns                                      │   │
│  │                                                              │   │
│  │  ┌─────────────────┬──────────┬──────────────────────────┐ │   │
│  │  │ Type            │ Severity │ CWE                      │ │   │
│  │  ├─────────────────┼──────────┼──────────────────────────┤ │   │
│  │  │ SQL Injection   │ CRITICAL │ CWE-89                   │ │   │
│  │  │ Hardcoded Secret│ CRITICAL │ CWE-798                  │ │   │
│  │  │ Command Inject. │ CRITICAL │ CWE-78                   │ │   │
│  │  │ XSS (innerHTML) │ ERROR    │ CWE-79                   │ │   │
│  │  │ Path Traversal  │ ERROR    │ CWE-22                   │ │   │
│  │  │ Insecure Deser. │ ERROR    │ CWE-95                   │ │   │
│  │  │ Weak Crypto     │ WARNING  │ CWE-327                  │ │   │
│  │  │ Weak Random     │ INFO     │ CWE-330                  │ │   │
│  │  └─────────────────┴──────────┴──────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Output: SecurityFinding with file, line, snippet, recommendation  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3. Complexity Analyzer

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Complexity Analyzer                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Metrics                                                     │   │
│  │                                                              │   │
│  │  Cyclomatic Complexity: branching keywords count + 1         │   │
│  │  Cognitive Complexity: nesting-weighted structure count      │   │
│  │  Lines of Code: non-blank, non-comment lines                 │   │
│  │  Max Function Length: longest function in file               │   │
│  │  Functions Count: total function definitions                 │   │
│  │  Classes Count: total class definitions                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Thresholds                                                  │   │
│  │                                                              │   │
│  │  Metric          │ Warning │ Error                          │   │
│  │  ────────────────┼─────────┼─────────                       │   │
│  │  Cyclomatic      │ 10      │ 20                             │   │
│  │  Cognitive       │ 15      │ 30                             │   │
│  │  Lines of Code   │ 200     │ 500                            │   │
│  │  Function Length │ 50      │ 100                            │   │
│  │  Nesting Depth   │ 4       │ 8                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4. Quality Gate

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Quality Gate                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Default Gates:                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Gate             │ Condition        │ Result               │   │
│  │  ─────────────────┼──────────────────┼─────────────         │   │
│  │  No Critical      │ critical == 0    │ Pass/Fail            │   │
│  │  Min Score        │ score >= 70      │ Pass/Fail            │   │
│  │  Max Errors       │ errors <= 5      │ Pass/Fail            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Overall: PASS if all gates pass, FAIL if any gate fails            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Review Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Review Pipeline                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Input: Source Code                                                 │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────┐                                                   │
│  │  Linting    │ ──▶ Style & convention issues                     │
│  └──────┬──────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                   │
│  │  Security   │ ──▶ Vulnerability findings                        │
│  │  Scan       │                                                   │
│  └──────┬──────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                   │
│  │ Complexity  │ ──▶ Metrics + threshold violations                │
│  │ Analysis    │                                                   │
│  └──────┬──────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                   │
│  │Architecture │ ──▶ Design principle violations                   │
│  │ Review      │                                                   │
│  └──────┬──────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                   │
│  │   Score     │ ──▶ Quality score + summary                       │
│  │ Calculation │                                                   │
│  └──────┬──────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                   │
│  │  Quality    │ ──▶ Pass/Fail decision                            │
│  │  Gate       │                                                   │
│  └──────┬──────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                   │
│  │  Report     │ ──▶ Markdown / JSON / HTML / Text                 │
│  │  Generation │                                                   │
│  └─────────────┘                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Models

### Entity Relationship

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Entity Relationships                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ReviewResult ─────────┬──── CodeIssue[]                            │
│       │                 │                                             │
│       │                 ├── severity (Severity)                      │
│       │                 │                                             │
│       │                 ├── category (ReviewCategory)                │
│       │                 │                                             │
│       │                 └── rule_id (str)                            │
│       │                                                              │
│       ├── complexity (ComplexityMetrics)                             │
│       │                                                              │
│       └── language (Language)                                        │
│                                                                     │
│  SecurityFinding ─────┬──── vulnerability_type (VulnerabilityType)  │
│                       │                                              │
│                       ├── cwe_id (str)                               │
│                       │                                              │
│                       └── recommendation (str)                       │
│                                                                     │
│  QualityGate ─────────┬──── rules[] (gate conditions)                │
│                       │                                              │
│                       └── result (GateResult: PASS/FAIL)             │
│                                                                     │
│  ReviewSummary ───────┬──── issues_by_severity                       │
│                       │                                              │
│                       ├── issues_by_category                         │
│                       │                                              │
│                       └── quality_gate (GateResult)                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Design Patterns

### 1. Pipeline Pattern — Review Flow

```python
# Sequential analysis stages
lint_issues = linter.lint(code)
security_findings = scanner.scan(code)
metrics, complexity_issues = analyzer.analyze(code)
arch_issues = reviewer.review(code)
# Aggregate all issues
```

### 2. Strategy Pattern — Language Support

```python
# Different patterns per language
if language == "python":
    patterns = PYTHON_PATTERNS
elif language in ("javascript", "typescript"):
    patterns = JS_PATTERNS
```

### 3. Chain of Responsibility — Quality Gates

```python
for gate in gates:
    passed = check_gate(gate, metrics)
    if not passed:
        overall_fail = True
```

### 4. Template Method — Report Generation

```python
def generate(self, results, fmt):
    if fmt == "markdown": return self._markdown(results)
    elif fmt == "json": return self._json(results)
    # ...
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Regex | `re` module | Pattern matching |
| Hashing | `hashlib` | ID generation |
| Data Models | `dataclasses` | Typed containers |
| JSON | `json` | Serialization |
| Logging | `logging` | Observability |

---

## Security Architecture

### Scanner Security

- Patterns are pre-compiled regex — no user-supplied regex execution
- Findings include CWE references for industry alignment
- Suppression rules prevent false positive fatigue
- Code snippets are truncated to prevent data leakage in reports

---

## Scalability

### Performance

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Lint | O(n × p) | n = lines, p = patterns |
| Security scan | O(n × v) | v = vulnerability patterns |
| Complexity | O(n) | Single pass |
| Architecture | O(n × a) | a = architecture patterns |
| Report | O(i) | i = total issues |

### Scaling Strategies

1. **Current**: In-memory, single file — suitable for <10K LOC
2. **Parallel**: Review multiple files concurrently
3. **Cached**: Cache results for unchanged files
4. **Distributed**: Shard by directory for large codebases

---

## Deployment

### CLI Usage

```bash
python agents/code-review-team/agent.py --file main.py --language python
python agents/code-review-team/agent.py --code "print('hello')" --language python
python agents/code-review-team/agent.py --status
```

### Integration

```python
from agent import CodeReviewTeamAgent

agent = CodeReviewTeamAgent()
result = agent.review_code(code, "main.py", "python")
gate = agent.check_quality_gates([result])
if gate.result.value == "fail":
    raise Exception("Quality gate failed")
```

---

## Code Examples

### Linting Python Code

```python
from agent import LinterIntegrator

linter = LinterIntegrator()

code = '''
import os
import sys
from os import *

def process(data):
    print("processing")
    result = eval(data)
    return result
'''

issues = linter.lint(code, "app.py", "python")
for issue in issues:
    print(f"[{issue.severity.value}] {issue.rule_id}: {issue.message}")
    print(f"  Line {issue.line_number}: {issue.code_snippet}")
    print(f"  Fix: {issue.suggestion}")
```

### Scanning JavaScript Code

```python
code = '''
const password = "admin123";
const query = "SELECT * FROM users WHERE id=" + userId;
document.innerHTML = userInput;
eval(userCode);
'''

findings = scanner.scan(code, "app.js")
for f in findings:
    print(f"[{f.severity.value}] {f.vulnerability_type.value}")
    print(f"  CWE: {f.cwe_id}")
    print(f"  Fix: {f.recommendation}")
```

### Analyzing Complex Code

```python
code = '''
def complex_logic(data):
    if data:
        for item in data:
            if item.active:
                if item.type == "a":
                    for sub in item.children:
                        if sub.valid:
                            process(sub)
                        else:
                            skip(sub)
                elif item.type == "b":
                    handle_b(item)
                else:
                    handle_other(item)
            else:
                log_inactive(item)
    return result
'''

metrics, issues = analyzer.analyze(code, "logic.py")
print(f"Cyclomatic: {metrics.cyclomatic_complexity}")  # 10
print(f"Cognitive: {metrics.cognitive_complexity}")    # 15
print(f"Max Nesting: {metrics.max_nesting_depth}")    # 5
```

---

## Configuration Examples

### Strict Configuration (Enterprise)

```python
config = Config(
    review_config=ReviewConfig(
        max_line_length=100,
        max_function_length=30,
        max_file_length=300,
        max_complexity=5,
        max_nesting_depth=3,
        require_docstrings=True,
        require_type_hints=True,
        security_scanning=True,
        excluded_files=["*.test.*", "migrations/*"],
    ),
    min_score=85.0,
    fail_on_critical=True,
    fail_on_error=True,  # Strict: fail on errors too
    report_formats=["markdown", "json"],
)
```

### Relaxed Configuration (Legacy Code)

```python
config = Config(
    review_config=ReviewConfig(
        max_line_length=150,
        max_function_length=100,
        max_file_length=1000,
        max_complexity=20,
        max_nesting_depth=6,
        require_docstrings=False,
        require_type_hints=False,
        security_scanning=True,
        excluded_files=["*.test.*", "migrations/*", "legacy/*"],
    ),
    min_score=50.0,
    fail_on_critical=True,
    fail_on_error=False,
    report_formats=["text"],
)
```

---

## Integration Examples

### GitHub Actions Integration

```yaml
# .github/workflows/code-review.yml
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Review
        run: |
          python agents/code-review-team/agent.py \
            --changed-files "${{ steps.changed.outputs.files }}" \
            --language python \
            --output review.json
      - name: Check Quality Gate
        run: |
          python -c "
          import json
          with open('review.json') as f:
              data = json.load(f)
          if data['gate'] == 'FAIL':
              exit(1)
          "
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -z "$CHANGED_FILES" ]; then
    exit 0
fi

python agents/code-review-team/agent.py \
    --files $CHANGED_FILES \
    --language python \
    --output review.json

GATE=$(python -c "import json; print(json.load(open('review.json'))['gate'])")

if [ "$GATE" = "FAIL" ]; then
    echo "❌ Code review failed. Fix issues before committing."
    exit 1
fi

echo "✅ Code review passed."
```

### Slack Notification Integration

```python
import json
import requests

def notify_slack(review_result, webhook_url):
    if review_result.gate == "FAIL":
        color = "danger"
        emoji = "❌"
    else:
        color = "good"
        emoji = "✅"

    payload = {
        "attachments": [{
            "color": color,
            "title": f"{emoji} Code Review: {review_result.file_path}",
            "fields": [
                {"title": "Score", "value": f"{review_result.score}/100", "short": True},
                {"title": "Issues", "value": str(len(review_result.issues)), "short": True},
                {"title": "Gate", "value": review_result.gate, "short": True},
            ],
            "footer": "Code Review Team Agent",
        }]
    }
    requests.post(webhook_url, json=payload)
```

---

## Testing Strategy Examples

### Unit Test for Linter

```python
def test_lint_detects_print():
    linter = LinterIntegrator()
    code = 'print("hello")'
    issues = linter.lint(code, "test.py", "python")
    assert len(issues) == 1
    assert issues[0].rule_id == "W1001"
    assert issues[0].severity == Severity.WARNING
```

### Unit Test for Security Scanner

```python
def test_scan_detects_sql_injection():
    scanner = SecurityScanner()
    code = 'query = f"SELECT * FROM users WHERE id = {user_id}"'
    findings = scanner.scan(code, "test.py")
    assert len(findings) == 1
    assert findings[0].vulnerability_type == VulnerabilityType.SQL_INJECTION
    assert findings[0].cwe_id == "CWE-89"
```

### Unit Test for Quality Gate

```python
def test_quality_gate_passes():
    gate = QualityGate()
    results = [
        ReviewResult(score=85, issues=[], complexity=ComplexityMetrics(...)),
    ]
    gate_result = gate.check(results)
    assert gate_result == GateResult.PASS

def test_quality_gate_fails_on_critical():
    gate = QualityGate()
    results = [
        ReviewResult(score=90, issues=[
            CodeIssue(severity=Severity.CRITICAL, ...)
        ], complexity=ComplexityMetrics(...)),
    ]
    gate_result = gate.check(results)
    assert gate_result == GateResult.FAIL
```

---

## Configuration Examples

### Python Project Configuration

```python
python_config = Config(
    review_config=ReviewConfig(
        max_line_length=88,           # Black formatter default
        max_function_length=50,
        max_file_length=500,
        max_complexity=10,
        max_cognitive_complexity=15,
        max_nesting_depth=4,
        max_parameters=5,
        require_docstrings=True,
        require_type_hints=True,
        security_scanning=True,
        excluded_files=[
            "*.test.*",
            "test_*",
            "conftest.py",
            "migrations/*",
            "__pycache__/*",
            "venv/*",
            ".venv/*",
        ],
    ),
    min_score=75.0,
    fail_on_critical=True,
    fail_on_error=False,
)
```

### JavaScript/TypeScript Configuration

```python
js_config = Config(
    review_config=ReviewConfig(
        max_line_length=100,
        max_function_length=40,
        max_file_length=400,
        max_complexity=8,
        max_nesting_depth=3,
        require_docstrings=False,  # JSDoc optional
        require_type_hints=False,
        security_scanning=True,
        excluded_files=[
            "node_modules/*",
            "dist/*",
            "build/*",
            "*.min.js",
            "*.test.js",
            "*.spec.js",
        ],
    ),
    min_score=70.0,
    fail_on_critical=True,
    fail_on_error=False,
)
```

---

## Severity Levels Guide

### CRITICAL

Security vulnerabilities that allow immediate exploitation:
- SQL Injection
- Command Injection
- Hardcoded secrets/credentials
- Remote Code Execution

**Action**: Must fix before merge. Block deployment.

### ERROR

Serious issues affecting reliability or security:
- XSS vulnerabilities
- Path traversal
- Insecure deserialization
- Missing authentication

**Action**: Should fix before merge. Flag in PR review.

### WARNING

Code quality issues that may cause bugs:
- Bare except clauses
- Mutable default arguments
- Console.log in production
- var usage in JavaScript

**Action**: Fix when possible. Track in tech debt.

### INFO

Style and convention violations:
- TODO comments
- Missing type hints
- Long lines
- Magic numbers

**Action**: Fix in follow-up. Don't block merge.

### HINT

Suggestions for improvement:
- Alternative approaches
- Performance optimizations
- Readability improvements

**Action**: Consider during refactoring.

---

## Quality Score Calculation

```python
def calculate_score(issues, complexity_metrics):
    """Calculate quality score (0-100)."""
    score = 100.0

    # Deductions by severity
    deductions = {
        Severity.CRITICAL: 25,
        Severity.ERROR: 10,
        Severity.WARNING: 3,
        Severity.INFO: 1,
        Severity.HINT: 0,
    }

    for issue in issues:
        score -= deductions.get(issue.severity, 0)

    # Complexity penalties
    if complexity_metrics.cyclomatic_complexity > 20:
        score -= 10
    elif complexity_metrics.cyclomatic_complexity > 10:
        score -= 5

    if complexity_metrics.max_nesting_depth > 8:
        score -= 10
    elif complexity_metrics.max_nesting_depth > 4:
        score -= 5

    return max(0.0, min(100.0, score))
```

---

## Report Format Examples

### Markdown Report

```markdown
# Code Review Report

**File**: app.py
**Language**: Python
**Score**: 85/100
**Gate**: PASS

## Summary
- Critical: 0
- Error: 0
- Warning: 3
- Info: 5

## Issues

### [WARNING] W1001: print() usage
- **Line**: 15
- **Code**: `print("debug info")`
- **Fix**: Use logging module instead

### [INFO] I1001: TODO comment
- **Line**: 23
- **Code**: `# TODO: optimize this`
- **Fix**: Resolve before merge
```

### JSON Report

```json
{
  "file_path": "app.py",
  "language": "python",
  "score": 85.0,
  "gate": "PASS",
  "issues": [
    {
      "rule_id": "W1001",
      "severity": "WARNING",
      "line_number": 15,
      "message": "print() usage",
      "suggestion": "Use logging module"
    }
  ],
  "complexity": {
    "cyclomatic": 8,
    "cognitive": 12,
    "loc": 150,
    "max_function_length": 45
  }
}
```

---

*Code Review Team Agent Architecture v2.0 — Part of the Awesome Grok Skills collection.*
