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

*Code Review Team Agent Architecture v2.0 — Part of the Awesome Grok Skills collection.*
