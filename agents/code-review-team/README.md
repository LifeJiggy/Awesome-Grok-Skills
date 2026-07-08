# Code Review Team Agent

> Automated code review combining linting, security scanning, complexity analysis, and quality gates.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

---

## Overview

The Code Review Team Agent combines four analysis engines into a unified code review pipeline. It detects style violations, security vulnerabilities, complexity issues, and architecture problems — then enforces quality gates before code ships.

### What It Does

- **Linting**: Multi-language pattern-based detection (Python, JavaScript, TypeScript, Go, Rust, Java, C#, Ruby, PHP, Swift)
- **Security Scanning**: 10 vulnerability types with CWE references and fix recommendations
- **Complexity Analysis**: Cyclomatic/cognitive complexity, function length, nesting depth
- **Architecture Review**: SOLID principle violations, design pattern issues, god classes
- **Quality Gates**: Configurable pass/fail thresholds for CI/CD integration
- **Reporting**: Markdown, JSON, HTML, and plain text output formats

---

## Features

| Feature | Description |
|---------|-------------|
| Multi-Language | Python, JavaScript, TypeScript, Go, Rust, Java, C#, Ruby, PHP, Swift |
| Security Scanning | SQLi, XSS, hardcoded secrets, weak crypto, path traversal, command injection, SSRF, insecure deserialization |
| Complexity Metrics | Cyclomatic, cognitive, LOC, function length, nesting depth, parameter count |
| Architecture Review | SOLID violations, god classes, deep nesting, star imports, missing type hints |
| Quality Gates | Configurable thresholds with pass/fail for CI/CD |
| Custom Rules | Add your own regex-based linting rules per language |
| Multi-Format | Markdown, JSON, HTML, text reports |
| CWE References | Industry-standard vulnerability classification (CWE-89, CWE-79, CWE-798, etc.) |
| Fix Suggestions | Every issue comes with a recommended fix |
| Exclude Patterns | Glob-based file exclusion (test files, migrations, etc.) |

---

## Quick Start

```python
from agents.code_review_team.agent import CodeReviewTeamAgent

agent = CodeReviewTeamAgent()

code = '''
def process(user_id):
    password = "secret123"
    query = f"SELECT * FROM users WHERE id = {user_id}"
    eval(user_input)
    print("done")
'''

result = agent.review_code(code, "app.py", "python")
print(f"Score: {result.score}/100")
print(f"Issues: {len(result.issues)}")
for issue in result.issues:
    print(f"  [{issue.severity.value}] {issue.message}")
```

### Run the Agent

```bash
python agents/code-review-team/agent.py --file main.py
python agents/code-review-team/agent.py --code "print('hello')" --language python
python agents/code-review-team/agent.py --status
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

---

## Usage

### Single File Review

```python
agent = CodeReviewTeamAgent()

with open("app.py") as f:
    code = f.read()

result = agent.review_code(code, "app.py", "python")
print(f"Score: {result.score}/100")
print(f"Summary: {result.summary}")

# View issues by severity
for issue in result.issues:
    print(f"  [{issue.severity.value}] Line {issue.line_number}: {issue.message}")
    print(f"    Fix: {issue.suggestion}")
```

### Multiple Files

```python
files = {
    "app.py": open("app.py").read(),
    "utils.py": open("utils.py").read(),
    "models.py": open("models.py").read(),
    "auth.py": open("auth.py").read(),
}

results = agent.review_multiple(files, language="python")

# Aggregate scores
total_score = sum(r.score for r in results) / len(results)
total_issues = sum(len(r.issues) for r in results)
print(f"Average score: {total_score:.0f}/100")
print(f"Total issues: {total_issues}")

# Run quality gate
gate = agent.check_quality_gates(results)
print(f"Quality Gate: {gate.result.value}")
```

### Custom Rules

```python
from agents.code_review_team.agent import LinterIntegrator

linter = LinterIntegrator()

# Add a rule to catch TODO comments
linter.add_custom_rule(
    rule_id="no-todo",
    pattern=r"#\s*TODO",
    severity="info",
    message="TODO found — resolve before merge",
    language="python"
)

# Add a rule for print statements in production code
linter.add_custom_rule(
    rule_id="no-print",
    pattern=r"^\s*print\(",
    severity="warning",
    message="print() found — use logging instead",
    language="python"
)

# Add a rule for magic numbers
linter.add_custom_rule(
    rule_id="no-magic-numbers",
    pattern=r"(?<!\w)\d{3,}(?!\w)",
    severity="info",
    message="Magic number found — use a named constant",
    language="python"
)
```

### Security Scan Only

```python
from agents.code_review_team.agent import SecurityScanner

scanner = SecurityScanner()

code = '''
import os
password = "super_secret_123"
query = f"SELECT * FROM users WHERE name = '{name}'"
os.system(f"echo {user_input}")
eval(request.data)
'''

findings = scanner.scan(code, "vulnerable.py")
summary = scanner.get_vulnerability_summary(findings)

print(f"Critical: {summary['critical_count']}")
print(f"High: {summary['high_count']}")
print(f"Medium: {summary['medium_count']}")
print(f"Low: {summary['low_count']}")

for f in findings:
    print(f"[{f.severity.value}] {f.vulnerability_type.value} (CWE: {f.cwe_id})")
    print(f"  {f.description}")
    print(f"  Fix: {f.recommendation}")
```

### Complexity Check

```python
from agents.code_review_team.agent import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()

code = '''
def complex_function(data):
    if data:
        for item in data:
            if item.active:
                if item.type == "a":
                    for sub in item.children:
                        if sub.valid:
                            process(sub)
'''

metrics, issues = analyzer.analyze(code, "complex.py")
print(f"Cyclomatic: {metrics.cyclomatic_complexity}")
print(f"Cognitive: {metrics.cognitive_complexity}")
print(f"Max Nesting: {metrics.max_nesting_depth}")

for issue in issues:
    print(f"  [{issue.severity.value}] {issue.message}")
```

### Report Generation

```python
results = agent.review_multiple(files, language="python")

# Markdown for documentation
agent.generate_report(results, "markdown", output_path="review.md")

# JSON for CI/CD pipeline
agent.generate_report(results, "json", output_path="review.json")

# HTML for stakeholder review
agent.generate_report(results, "html", output_path="review.html")

# Plain text for terminal
report = agent.generate_report(results, "text")
print(report)
```

---

## API Reference

### CodeReviewTeamAgent

| Method | Description |
|--------|-------------|
| `review_code(code, file_path, language)` | Review single file |
| `review_multiple(files, language)` | Review multiple files |
| `check_quality_gates(results)` | Run quality gates |
| `generate_report(results, fmt, output_path)` | Generate report |

### LinterIntegrator

| Method | Description |
|--------|-------------|
| `lint(code, file_path, language)` | Run linting |
| `add_custom_rule(rule_id, pattern, severity, message, language)` | Add custom rule |

### SecurityScanner

| Method | Description |
|--------|-------------|
| `scan(code, file_path)` | Scan for vulnerabilities |
| `suppress_rule(rule_id)` | Suppress a rule |
| `get_vulnerability_summary(findings)` | Get summary |

### ComplexityAnalyzer

| Method | Description |
|--------|-------------|
| `analyze(code, file_path)` | Analyze complexity |
| `set_threshold(metric, warning, error)` | Set thresholds |

### Enums

| Enum | Values |
|------|--------|
| `Severity` | CRITICAL, ERROR, WARNING, INFO, HINT |
| `ReviewCategory` | SYNTAX, SECURITY, PERFORMANCE, ARCHITECTURE, TESTING, DOCUMENTATION, STYLE, COMPLEXITY |
| `Language` | PYTHON, JAVASCRIPT, TYPESCRIPT, GO, RUST, JAVA, CSHARP, RUBY, PHP, SWIFT |
| `VulnerabilityType` | SQL_INJECTION, XSS, HARDCODED_SECRET, WEAK_CRYPTO, PATH_TRAVERSAL, COMMAND_INJECTION, SSRF, INSECURE_DESERIALIZATION, BROKEN_AUTH, SENSITIVE_DATA_EXPOSURE |
| `GateResult` | PASS, FAIL |

---

## Examples

### Detect Security Vulnerabilities

```python
code = '''
import os
password = "super_secret_123"
query = f"SELECT * FROM users WHERE name = '{name}'"
os.system(f"echo {user_input}")
eval(request.data)
'''

result = agent.review_code(code, "vulnerable.py")
for issue in result.issues:
    if issue.category.value == "security":
        print(f"[{issue.severity.value}] {issue.rule_id}: {issue.message}")
        print(f"  Line {issue.line_number}: {issue.code_snippet}")
        print(f"  Fix: {issue.suggestion}")
        print()
```

### Full Review Pipeline

```python
files = {
    "auth.py": open("auth.py").read(),
    "database.py": open("database.py").read(),
    "api.py": open("api.py").read(),
    "utils.py": open("utils.py").read(),
}

# 1. Review all files
results = agent.review_multiple(files, language="python")

# 2. Check quality gates
gate = agent.check_quality_gates(results)
if gate.result.value == "fail":
    print("Quality gate FAILED — blocking merge")
    for d in gate.details:
        if not d['passed']:
            print(f"  FAIL: {d['gate']}")
    exit(1)

# 3. Generate reports
agent.generate_report(results, "markdown", output_path="review.md")
agent.generate_report(results, "json", output_path="review.json")

print("Quality gate PASSED — ready to merge")
```

### CI/CD Integration

```python
import sys
from agents.code_review_team.agent import CodeReviewTeamAgent

agent = CodeReviewTeamAgent()

# Read changed files from git diff
import subprocess
changed_files = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD~1"]
).decode().strip().split("\n")

# Review changed files
files = {}
for f in changed_files:
    if f.endswith(".py"):
        with open(f) as fh:
            files[f] = fh.read()

if not files:
    print("No Python files changed")
    sys.exit(0)

results = agent.review_multiple(files, language="python")
gate = agent.check_quality_gates(results)

# Generate JSON report for CI
agent.generate_report(results, "json", output_path="review.json")

if gate.result.value == "fail":
    print("Code review FAILED")
    sys.exit(1)
else:
    print("Code review PASSED")
    sys.exit(0)
```

### Custom Rule for Project Conventions

```python
linter = LinterIntegrator()

# Enforce logging instead of print
linter.add_custom_rule(
    rule_id="use-logger",
    pattern=r"^\s*print\(",
    severity="warning",
    message="Use logging module instead of print()",
    language="python"
)

# Enforce type hints on function definitions
linter.add_custom_rule(
    rule_id="return-type-hint",
    pattern=r"def \w+\([^)]*\)\s*:",
    severity="info",
    message="Missing return type hint on function",
    language="python"
)

# Catch TODO/FIXME/HACK comments
linter.add_custom_rule(
    rule_id="resolve-todos",
    pattern=r"#\s*(TODO|FIXME|HACK|XXX)",
    severity="info",
    message="Unresolved comment found — resolve before merge",
    language="python"
)
```

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
        excluded_files=["*.test.*", "migrations/*", "node_modules/*", "dist/*", "__pycache__/*"],
        custom_rules=[],
    ),
    min_score=70.0,
    fail_on_critical=True,
    fail_on_error=False,
    report_formats=["markdown", "json"],
)

agent = CodeReviewTeamAgent(config=config)
```

### Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_line_length` | int | 120 | Maximum characters per line |
| `max_function_length` | int | 50 | Maximum lines per function |
| `max_file_length` | int | 500 | Maximum lines per file |
| `max_complexity` | int | 10 | Maximum cyclomatic complexity |
| `max_nesting_depth` | int | 4 | Maximum nesting depth |
| `require_docstrings` | bool | True | Require docstrings on public APIs |
| `require_type_hints` | bool | True | Require type hints on public functions |
| `security_scanning` | bool | True | Enable security vulnerability scanning |
| `excluded_files` | List[str] | [] | Glob patterns to exclude |
| `min_score` | float | 70.0 | Minimum review score to pass gate |
| `fail_on_critical` | bool | True | Fail gate on critical issues |
| `fail_on_error` | bool | False | Fail gate on error-level issues |

---

## Best Practices

1. **Run on Every PR**: Integrate into CI/CD pipeline for automated quality checks
2. **Fail on Critical**: Block merges with critical security issues
3. **Custom Rules**: Add project-specific patterns (logging conventions, naming rules)
4. **Suppress Wisely**: Only suppress known false positives with comments
5. **Track Trends**: Monitor score over time, not just per PR
6. **Review Reports**: Use HTML reports for stakeholder visibility
7. **Exclude Test Files**: Don't lint test files with production rules
8. **Set Realistic Thresholds**: Start loose, tighten as codebase improves
9. **Combine with Human Review**: Automated review catches patterns; humans catch logic
10. **Regular Rule Reviews**: Prune unused custom rules quarterly

---

## Troubleshooting

| Problem | Cause | Resolution |
|---------|-------|------------|
| Too many false positives | Rules too aggressive | Adjust thresholds in ReviewConfig |
| Missing vulnerabilities | Pattern not covered | Add custom rule with `add_custom_rule()` |
| Score too low on legacy code | Accumulated tech debt | Suppress known issues; focus on new code |
| Report empty | No code provided | Check file path and encoding |
| Complexity too high | Deeply nested logic | Refactor into smaller functions |
| Security scan slow | Large codebase | Exclude test files; run engines in parallel |
| Custom rule not matching | Regex incorrect | Test pattern with `re.search()` in Python REPL |
| Quality gate always failing | Thresholds too strict | Adjust gate rules in Config |

---

## Files

- `agent.py` — Full implementation with all analysis engines
- `ARCHITECTURE.md` — System architecture with ASCII diagrams
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*Code Review Team Agent v2.0 — Part of the Awesome Grok Skills collection.*
