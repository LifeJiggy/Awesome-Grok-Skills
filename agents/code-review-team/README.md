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

- **Linting**: Multi-language pattern-based detection (Python, JavaScript, TypeScript)
- **Security Scanning**: 8 vulnerability types with CWE references and fix recommendations
- **Complexity Analysis**: Cyclomatic/cognitive complexity, function length, nesting depth
- **Architecture Review**: SOLID principle violations, design pattern issues
- **Quality Gates**: Configurable pass/fail thresholds
- **Reporting**: Markdown, JSON, HTML, and plain text output

---

## Features

| Feature | Description |
|---------|-------------|
| Multi-Language | Python, JavaScript, TypeScript, Go, Rust, Java, C#, Ruby, PHP, Swift |
| Security Scanning | SQLi, XSS, hardcoded secrets, weak crypto, path traversal, command injection |
| Complexity Metrics | Cyclomatic, cognitive, LOC, function length, nesting depth |
| Architecture Review | SOLID violations, god classes, deep nesting |
| Quality Gates | Configurable thresholds with pass/fail |
| Custom Rules | Add your own regex-based linting rules |
| Multi-Format | Markdown, JSON, HTML, text reports |
| CWE References | Industry-standard vulnerability classification |

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
print(result.summary)
```

### Multiple Files

```python
files = {
    "app.py": open("app.py").read(),
    "utils.py": open("utils.py").read(),
    "models.py": open("models.py").read(),
}

results = agent.review_multiple(files, language="python")

# Quality gate
gate = agent.check_quality_gates(results)
print(f"Quality Gate: {gate.result.value}")
```

### Custom Rules

```python
from agent import LinterIntegrator

linter = LinterIntegrator()
linter.add_custom_rule(
    rule_id="no-todo",
    pattern=r"#\s*TODO",
    severity="info",
    message="TODO found — resolve before merge",
    language="python"
)
```

### Security Scan Only

```python
from agent import SecurityScanner

scanner = SecurityScanner()
findings = scanner.scan(code, "app.py")
summary = scanner.get_vulnerability_summary(findings)
print(f"Critical: {summary['critical_count']}")
```

### Report Generation

```python
results = agent.review_multiple(files)

# Markdown
agent.generate_report(results, "markdown", output_path="review.md")

# JSON for CI/CD
agent.generate_report(results, "json", output_path="review.json")

# HTML for stakeholders
agent.generate_report(results, "html", output_path="review.html")
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
        print(f"  Fix: {issue.suggestion}")
```

### Complexity Check

```python
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

result = agent.review_code(code, "complex.py")
for issue in result.issues:
    if issue.category.value == "complexity":
        print(f"{issue.message}")
```

---

## Configuration

```python
from agent import Config, ReviewConfig

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
```

---

## Best Practices

1. **Run on Every PR**: Integrate into CI/CD pipeline
2. **Fail on Critical**: Block merges with critical security issues
3. **Custom Rules**: Add project-specific patterns
4. **Suppress Wisely**: Only suppress known false positives
5. **Track Trends**: Monitor score over time, not just per PR
6. **Review Reports**: Use HTML reports for stakeholder visibility

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Too many false positives | Rules too aggressive | Adjust thresholds or suppress rules |
| Missing vulnerabilities | Pattern not covered | Add custom rule |
| Score too low on legacy | accumulated tech debt | Suppress known issues, focus on new code |
| Report empty | No code provided | Check file path and encoding |

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
