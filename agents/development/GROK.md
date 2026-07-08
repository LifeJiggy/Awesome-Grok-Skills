---
name: "Development Agent"
version: "2.0.0"
description: "Comprehensive software development analysis, generation, and quality assurance agent with architecture patterns, testing strategies, security scanning, and CI/CD pipeline management."
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - development
  - code-analysis
  - refactoring
  - quality-assurance
  - security-scanning
  - testing
  - ci-cd
  - architecture-patterns
  - performance-optimization
  - code-review
  - documentation-generation
category: "development"
personality: "code-architect"
use_cases:
  - static-analysis
  - code-quality
  - refactoring
  - documentation
  - security-scanning
  - performance-profiling
  - test-generation
  - ci-cd-pipeline
  - code-review
  - architecture-evaluation
---

# Development Agent

> Systematic software development analysis with analytical precision and engineering rigor.

## Agent Identity

The Development Agent is a comprehensive software development analysis and generation
system. It combines static analysis, security scanning, performance profiling, testing
strategy, code quality management, documentation generation, CI/CD pipeline management,
architecture evaluation, refactoring, and code review into a unified, composable toolkit.

### Personality Traits

- **Methodical** — follows systematic analysis procedures with reproducible results
- **Precise** — provides exact line numbers, severity levels, and CWE references
- **Constructive** — every finding comes with a concrete remediation suggestion
- **Comprehensive** — examines code from multiple angles simultaneously
- **Pragmatic** — focuses on actionable improvements, not theoretical perfection

### When to Use This Agent

| Scenario | Agent Method |
|----------|-------------|
| New codebase review | `analyze_project()` |
| Single file analysis | `analyze_code()` |
| Security audit | `SecurityScanner.scan_source()` |
| Refactoring planning | `CodeRefactoringEngine.analyze_for_refactoring()` |
| Test plan creation | `TestingStrategies.generate_test_plan()` |
| CI/CD setup | `CICDPipeline.generate_pipeline_config()` |
| Documentation generation | `DocumentationGenerator.generate_api_docs()` |
| Code review | `CodeReviewAssistant.review_diff()` |
| Architecture evaluation | `ArchitecturePatterns.evaluate_codebase_pattern()` |
| Performance optimization | `PerformanceOptimizer.analyze_performance()` |

---

## Core Principles

### 1. Evidence-Based Analysis

Every finding must be grounded in measurable data — line numbers, complexity scores,
pattern matches. No speculative warnings.

```python
# CORRECT — evidence-based
CodeIssue(
    issue_id="SA-00042",
    file_path="auth.py",
    line_number=42,
    issue_type=IssueType.SECURITY,
    severity=IssueSeverity.CRITICAL,
    message="SQL injection vulnerability",
    code_snippet=f"cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
    suggestion="Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
    rule_id="SQL injection via f-string",
)

# WRONG — vague
{"type": "warning", "message": "possible security issue somewhere"}
```

### 2. Severity Calibration

Severity is assigned based on exploitability and impact, not just code presence:

| Severity | Criteria | Example |
|----------|----------|---------|
| CRITICAL | Direct exploitation path, data breach potential | SQL injection, eval() on user input |
| HIGH | Significant risk, requires chaining or specific conditions | Hardcoded secrets, shell=True |
| MEDIUM | Design issue, potential for future problems | Broad exception handling, global vars |
| LOW | Code smell, minor quality concern | Print statements, missing docstrings |
| INFO | Observation, no immediate action needed | TODO comments, type ignore comments |

### 3. Actionable Suggestions

Every finding includes a concrete remediation step, not just a problem description.

```python
# CORRECT — actionable
suggestion="Replace with: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"

# WRONG — vague
suggestion="Fix this"
```

### 4. Reproducible Results

Analysis of the same source code always produces the same findings, in the same order,
with the same severity assignments.

---

## Capabilities

### 1. Static Analysis

Scans source code for security vulnerabilities, code quality issues, and style violations
using pattern-based detection with CWE mapping.

```python
from agents.development.agent import StaticAnalysisEngine, IssueType, IssueSeverity

engine = StaticAnalysisEngine()

source_code = '''
password = "admin123"
api_key = "sk-live-abcdef1234567890"

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = cursor.execute(query)
    return result

def process(data):
    return eval(data)
'''

results = engine.analyze(source_code, "auth.py")
# results = {
#     'file': 'auth.py',
#     'lines_of_code': 12,
#     'issue_count': 4,
#     'issues': [
#         {'id': 'SA-00001', 'severity': 'HIGH', 'type': 'security', 'message': 'Hardcoded password detected'},
#         {'id': 'SA-00002', 'severity': 'HIGH', 'type': 'security', 'message': 'Hardcoded API key detected'},
#         {'id': 'SA-00003', 'severity': 'CRITICAL', 'type': 'security', 'message': 'SQL injection vulnerability'},
#         {'id': 'SA-00004', 'severity': 'HIGH', 'type': 'security', 'message': 'Dangerous eval() usage'},
#     ],
#     'complexity': 1,
#     'maintainability_index': 72.0,
# }
```

**Detection patterns include:**

- Hardcoded secrets (passwords, API keys, tokens)
- SQL injection (f-string and string concatenation in queries)
- Dangerous function calls (eval, exec, pickle.loads)
- Subprocess shell injection
- Weak cryptography (MD5, SHA-1)
- Code quality issues (bare excepts, print statements, empty pass blocks)
- Documentation gaps (TODO/FIXME markers)

### 2. Refactoring Engine

Identifies opportunities for code improvement across multiple dimensions:

```python
from agents.development.agent import CodeRefactoringEngine, RefactoringType

engine = CodeRefactoringEngine()

source_code = '''
def process_order(order_id, user_id, amount, currency, tax_rate, discount, shipping):
    """Process an order with too many parameters."""
    total = amount * (1 - discount) * (1 + tax_rate) + shipping
    return total

class OrderManager:
    def process_all_orders(self, orders):
        results = []
        for order in orders:
            for item in order.items:
                for detail in item.details:
                    for line in detail.lines:
                        results.append(line.process())
        return results
'''

results = engine.analyze(source_code, "orders.py")
# Detects:
# - Function with 7 parameters (threshold: 5)
# - Triple-nested loop (nesting depth > 4)
# - Returns RefactoringSuggestion with type, effort, risk, estimated time
```

**Refactoring types detected:**

| Type | Threshold | Effort |
|------|-----------|--------|
| EXTRACT_METHOD | Method > 50 lines | medium |
| INTRODUCE_PARAMETER_OBJECT | > 5 parameters | medium |
| RENAME_VARIABLE | Non-descriptive names (x, temp, data, etc.) | low |
| DECOMPOSE_CONDITIONAL | Nesting depth > 4 | medium |
| Missing main guard | Module without `if __name__` | low |

### 3. Security Scanner

OWASP-aligned vulnerability detection with CWE mapping and risk scoring:

```python
from agents.development.agent import SecurityScanner

scanner = SecurityScanner()

source_code = '''
import yaml
import requests

# Unsafe YAML deserialization
config = yaml.load(open("config.yaml"), Loader=yaml.UnsafeLoader)

# SSL verification disabled
response = requests.get("https://api.example.com", verify=False)

# Path traversal risk
file_path = os.path.join("/uploads", request.args.get("filename"))

# Overly permissive CORS
app.config["CORS_ALLOW_ORIGINS"] = ["*"]
'''

vulns = scanner.scan_source(source_code, "app.py")
# Returns SecurityVulnerability objects with:
# - vuln_id, category, CWE ID, severity, title, description, remediation

risk = scanner.calculate_risk_score(vulns)
# risk = {
#     'total_vulnerabilities': 4,
#     'total_risk_score': 32.5,
#     'risk_level': 'HIGH',
#     'by_category': {'insecure_deserialization': 1, 'security_misconfiguration': 2, 'path_traversal': 1},
# }
```

**Vulnerability categories covered:**

| Category | CWE | Detection |
|----------|-----|-----------|
| SQL Injection | CWE-89 | f-string in SQL queries |
| XSS | CWE-79 | innerHTML, document.write |
| Path Traversal | CWE-22 | os.path.join + request input |
| SSL Bypass | CWE-295 | verify=False |
| Insecure Deserialization | CWE-502 | yaml.load with UnsafeLoader |
| Overly Permissive CORS | CWE-942 | allow_origins=["*"] |
| Weak RNG | CWE-330 | random module for security |

### 4. Code Quality Manager

Enforces configurable quality standards and runs quality gates:

```python
from agents.development.agent import CodeQualityManager

manager = CodeQualityManager()

# Evaluate against standards
metrics = {
    "avg_complexity": 12,  # Exceeds threshold of 10
    "avg_maintainability": 45,  # Below threshold of 60
    "test_coverage": 75,  # Below threshold of 80
    "issues_by_severity": {"critical": 3, "high": 8},
}

gate = manager.evaluate_quality_gate(metrics)
# gate.status == QualityGateStatus.FAILED
# gate.checks == [
#     {"name": "Cyclomatic Complexity", "status": "failed", "actual": 12, "threshold": 10},
#     {"name": "Test Coverage", "status": "failed", "actual": 75, "threshold": 80},
#     {"name": "Maintainability Index", "status": "failed", "actual": 45, "threshold": 60},
#     {"name": "Critical/High Issues", "status": "failed", "actual": "3 critical, 8 high", "threshold": "0 critical, ≤5 high"},
# ]

# Estimate technical debt
from agents.development.agent import CodeIssue, IssueType, IssueSeverity
issues = [
    CodeIssue("1", "a.py", 1, IssueType.SECURITY, IssueSeverity.CRITICAL, "SQLi", "", "", ""),
    CodeIssue("2", "b.py", 1, IssueType.BUG, IssueSeverity.HIGH, "NPE", "", "", ""),
]
debt = manager.calculate_technical_debt(issues)
# debt = {"total_hours": 6.0, "by_type": {"security": 4.0, "bug": 2.0}}
```

**Configurable standards:**

| Standard | Default | Unit |
|----------|---------|------|
| Max function length | 30 | lines |
| Max class length | 300 | lines |
| Max cyclomatic complexity | 10 | McCabe |
| Min test coverage | 80 | % |
| Max line length | 120 | chars |
| Min docstring coverage | 70 | % |
| Max nesting depth | 4 | levels |
| Max params per function | 5 | params |
| Min maintainability index | 60 | index |

### 5. Testing Strategies

Generates test plans and assesses test quality:

```python
from agents.development.agent import TestingStrategies

tester = TestingStrategies()

source_code = '''
class UserService:
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id):
        return self.db.query("SELECT * FROM users WHERE id = ?", user_id)

    def create_user(self, name, email):
        return self.db.insert("users", {"name": name, "email": email})
'''

plan = tester.generate_test_plan(source_code, "user_service.py")
# plan = {
#     'test_cases': [
#         {
#             'class': 'UserService',
#             'test_type': 'unit',
#             'cases': [
#                 {'name': 'test_UserService_instantiation', 'description': 'Object creation with valid parameters'},
#                 {'name': 'test_UserService_methods', 'description': 'All public methods work correctly'},
#             ],
#         },
#     ],
#     'total_test_cases': 8,
#     'coverage_target': 80.0,
# }

# Assess test quality
test_code = '''
def test_create_user():
    result = service.create_user("Alice", "alice@example.com")
    assert result is not None
    assert result.name == "Alice"
'''

quality = tester.assess_test_quality(test_code)
# quality = {'test_functions': 1, 'assertions': 3, 'quality_score': 65.0, ...}
```

### 6. Documentation Generator

Produces Markdown documentation, type stubs, changelogs, and README templates:

```python
from agents.development.agent import DocumentationGenerator

doc_gen = DocumentationGenerator()

source_code = '''
class UserManager:
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id):
        """Fetch a user by ID."""
        return self.db.query(user_id)

    def delete_user(self, user_id):
        """Remove a user."""
        return self.db.delete(user_id)

def calculate_metrics(data):
    """Calculate aggregate metrics."""
    return sum(data) / len(data)
'''

api_docs = doc_gen.generate_api_docs(source_code, "User Service API")
# Outputs Markdown with class/function sections, signatures, and descriptions

changelog = doc_gen.generate_changelog([
    {"category": "added", "description": "User deletion endpoint"},
    {"category": "fixed", "description": "Memory leak in metrics calculation"},
], version="1.2.0")
# Outputs: ## [1.2.0] - 2026-07-06

readme = doc_gen.generate_readme_template("User Service", "A lightweight user management service")
# Outputs README.md template with installation, usage, config sections
```

### 7. CI/CD Pipeline Manager

Generates and simulates CI/CD pipelines:

```python
from agents.development.agent import CICDPipeline

pipeline = CICDPipeline()

# Generate a pipeline configuration
config = pipeline.generate_pipeline_config("python", "fastapi")
# config.stages == [LINT, BUILD, TEST, SECURITY_SCAN, DEPLOY_STAGING, ...]
# config.environment_variables == {"PYTHON_VERSION": "3.11", "POETRY_VERSION": "1.7.0"}

# Simulate pipeline execution
results = pipeline.simulate_pipeline_run(config.pipeline_id)
# results = {
#     'pipeline_id': 'pipeline-python-1234567890',
#     'overall_status': 'success',
#     'total_duration': 48.3,
#     'stages': [{'stage': 'lint', 'status': 'success', 'duration_seconds': 3.5}, ...],
# }

# Generate GitHub Actions YAML
yaml_config = pipeline.generate_github_actions_config(config)
# Returns a complete .github/workflows/*.yml content string
```

### 8. Architecture Pattern Analysis

Evaluates codebases for architecture patterns and recommends designs:

```python
from agents.development.agent import ArchitecturePatterns

arch = ArchitecturePatterns()

# Recommend patterns for a project
recommendations = arch.analyze_pattern_fit(
    project_type="enterprise",
    team_size=15,
    scale_requirements="high"
)
# recommendations = [
#     {'pattern': 'microservices', 'fit_score': 0.9, 'reason': 'High scale requirements...'},
#     {'pattern': 'clean_architecture', 'fit_score': 0.85, 'reason': 'Enterprise application...'},
# ]

# Detect existing pattern in codebase
source_code = '''
class OrderController:
    def handle_request(self):
        model = OrderModel()
        view = OrderView()
        return view.render(model.get_data())
'''

detected = arch.evaluate_codebase_pattern(source_code)
# detected = {'detected_pattern': 'mvc', 'confidence': 0.7, ...}
```

### 9. Performance Optimizer

Identifies performance anti-patterns and profiles function execution:

```python
from agents.development.agent import PerformanceOptimizer

optimizer = PerformanceOptimizer()

source_code = '''
def process_matrix(matrix):
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for k in range(len(matrix)):
                result.append(matrix[i][j] * matrix[k][j])
    return result
'''

perf = optimizer.analyze_performance(source_code, "matrix.py")
# perf = {
#     'performance_issues': [
#         {'type': 'nested_loops', 'severity': 'high', 'message': 'Triple-nested loop at line 2; O(n^3)'},
#     ],
#     'optimization_potential': 'high',
# }
```

### 10. Code Review Assistant

Analyzes diffs and generates structured review comments:

```python
from agents.development.agent import CodeReviewAssistant

reviewer = CodeReviewAssistant()

diff = """
@@ -10,6 +10,8 @@
 def process_input(data):
+    password = "admin123"
+    result = eval(data)
     return process(data)
"""

comments = reviewer.review_diff(diff, "auth.py")
# comments = [
#     CodeReviewComment(severity=CRITICAL, content="Hardcoded password detected..."),
#     CodeReviewComment(severity=HIGH, content="Dynamic code execution detected..."),
# ]

summary = reviewer.generate_review_summary(comments)
# summary = {'approval_recommendation': 'request_changes', 'unresolved_comments': 2, ...}
```

---

## Method Signatures

### DevelopmentDashboard

```python
class DevelopmentDashboard:
    def __init__(self) -> None: ...

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Run comprehensive analysis on an entire project.
        Returns: summary, total_issues, quality_gate, technical_debt, dependency_analysis
        """

    def analyze_code(self, source_code: str, file_path: str = "analyzed.py") -> Dict[str, Any]:
        """
        Run all analyses on a single source file.
        Returns: static_analysis, refactoring, security, performance, test_plan, documentation
        """

    def generate_code(self, request_type: str, parameters: Dict[str, Any]) -> str:
        """
        Generate code based on request type.
        Types: 'class', 'api', 'test', 'docs', 'readme', 'pipeline', 'changelog'
        Returns: Generated code as a string
        """
```

### StaticAnalysisEngine

```python
class StaticAnalysisEngine:
    def __init__(self) -> None: ...

    def analyze(self, source_code: str, file_path: str = "") -> Dict[str, Any]: ...
    def scan_for_issues(self, source_code: str, file_path: str = "") -> List[CodeIssue]: ...
    def calculate_cyclomatic_complexity(self, source_code: str) -> int: ...
    def calculate_halstead_volume(self, source_code: str) -> float: ...
    def calculate_metrics(self, source_code: str) -> Dict[str, Any]: ...
    def calculate_maintainability(self, metrics: Dict[str, Any], complexity: int) -> float: ...
```

### SecurityScanner

```python
class SecurityScanner:
    def __init__(self) -> None: ...
    def scan_source(self, source_code: str, file_path: str = "") -> List[SecurityVulnerability]: ...
    def calculate_risk_score(self, vulns: List[SecurityVulnerability]) -> Dict[str, Any]: ...
```

### CodeRefactoringEngine

```python
class CodeRefactoringEngine:
    def __init__(self) -> None: ...
    def analyze(self, source_code: str, file_path: str = "") -> Dict[str, Any]: ...
    def analyze_for_refactoring(self, source_code: str, file_path: str = "") -> List[RefactoringSuggestion]: ...
    def suggest_naming_improvements(self, source_code: str, file_path: str = "") -> List[RefactoringSuggestion]: ...
```

### TestingStrategies

```python
class TestingStrategies:
    def __init__(self) -> None: ...
    def generate_test_plan(self, source_code: str, file_path: str = "") -> Dict[str, Any]: ...
    def calculate_test_coverage(self, tested_lines: Set[int], total_lines: int) -> float: ...
    def assess_test_quality(self, test_code: str) -> Dict[str, Any]: ...
```

### CodeQualityManager

```python
class CodeQualityManager:
    def __init__(self) -> None: ...
    def evaluate_quality_gate(self, metrics: Dict[str, Any]) -> QualityGateResult: ...
    def calculate_technical_debt(self, issues: List[CodeIssue]) -> Dict[str, Any]: ...
```

### DocumentationGenerator

```python
class DocumentationGenerator:
    def __init__(self) -> None: ...
    def generate_api_docs(self, source_code: str, title: str = "API Reference") -> str: ...
    def generate_changelog(self, changes: List[Dict[str, str]], version: str = "1.0.0") -> str: ...
    def generate_readme_template(self, project_name: str, description: str) -> str: ...
    def generate_type_stubs(self, source_code: str) -> str: ...
```

### CICDPipeline

```python
class CICDPipeline:
    def __init__(self) -> None: ...
    def create_pipeline(self, config: PipelineConfig) -> PipelineConfig: ...
    def generate_pipeline_config(self, project_type: str, framework: str) -> PipelineConfig: ...
    def simulate_pipeline_run(self, pipeline_id: str) -> Dict[str, Any]: ...
    def generate_github_actions_config(self, config: PipelineConfig) -> str: ...
```

### PerformanceOptimizer

```python
class PerformanceOptimizer:
    def __init__(self) -> None: ...
    def analyze_performance(self, source_code: str, file_path: str = "") -> Dict[str, Any]: ...
    def profile_function(self, func_name: str, call_count: int, total_time_ms: float) -> PerformanceMetric: ...
```

### CodeReviewAssistant

```python
class CodeReviewAssistant:
    def __init__(self) -> None: ...
    def review_diff(self, diff_content: str, file_path: str = "") -> List[CodeReviewComment]: ...
    def generate_review_summary(self, comments: List[CodeReviewComment]) -> Dict[str, Any]: ...
```

### ArchitecturePatterns

```python
class ArchitecturePatterns:
    def __init__(self) -> None: ...
    def analyze_pattern_fit(self, project_type: str, team_size: int, scale_requirements: str) -> List[Dict[str, Any]]: ...
    def get_pattern_details(self, pattern: ArchitecturePattern) -> Dict[str, str]: ...
    def evaluate_codebase_pattern(self, source_code: str) -> Dict[str, Any]: ...
```

### DependencyAnalyzer

```python
class DependencyAnalyzer:
    def __init__(self) -> None: ...
    def analyze_dependencies(self, package_file: str = "requirements.txt", lock_file: str = "") -> Dict[str, Any]: ...
    def find_dependency_conflicts(self, dependencies: Dict[str, Any]) -> List[Dict[str, Any]]: ...
    def compute_dependency_score(self, analysis: Dict[str, Any]) -> float: ...
```

---

## Data Models

### CodeIssue

| Field | Type | Description |
|-------|------|-------------|
| issue_id | str | Unique identifier (e.g., "SA-00042") |
| file_path | str | Source file path |
| line_number | int | 1-indexed line number |
| issue_type | IssueType | Classification (BUG, SECURITY, PERFORMANCE, etc.) |
| severity | IssueSeverity | Impact level (INFO, LOW, MEDIUM, HIGH, CRITICAL) |
| message | str | Human-readable description |
| code_snippet | str | The offending code line |
| suggestion | str | Concrete remediation step |
| rule_id | str | Pattern or rule identifier |
| column | int | Column position (0-indexed) |
| fix_available | bool | Whether an auto-fix is available |
| confidence | float | Detection confidence (0.0-1.0) |

### SecurityVulnerability

| Field | Type | Description |
|-------|------|-------------|
| vuln_id | str | Unique identifier (e.g., "SEC-00001") |
| file_path | str | Source file path |
| line_number | int | 1-indexed line number |
| category | SecurityVulnCategory | OWASP category |
| severity | IssueSeverity | Impact level |
| title | str | Short vulnerability title |
| description | str | Detailed description |
| cwe_id | str | CWE reference (e.g., "CWE-89") |
| cvss_score | float | CVSS v3.1 score (0.0-10.0) |
| remediation | str | Fix instructions |

### RefactoringSuggestion

| Field | Type | Description |
|-------|------|-------------|
| file_path | str | Source file path |
| line_number | int | 1-indexed line number |
| original_code | str | Current code |
| suggested_code | str | Proposed replacement |
| reason | str | Why this refactoring is beneficial |
| effort | str | Estimated effort (low/medium/high) |
| refactoring_type | RefactoringType | Classification of transformation |
| risk_level | str | Risk of applying change (low/medium/high) |
| estimated_time_minutes | int | Estimated implementation time |

### QualityGateResult

| Field | Type | Description |
|-------|------|-------------|
| gate_name | str | Name of the quality gate |
| status | QualityGateStatus | PASSED, FAILED, WARNING, SKIPPED |
| checks | List[Dict] | Individual check results |
| summary | str | Human-readable summary |
| duration_ms | float | Gate execution time |

### PipelineConfig

| Field | Type | Description |
|-------|------|-------------|
| pipeline_id | str | Unique pipeline identifier |
| name | str | Human-readable pipeline name |
| stages | List[CICDStage] | Ordered pipeline stages |
| triggers | List[str] | Event triggers (push, PR, schedule) |
| environment_variables | Dict[str, str] | CI environment variables |
| timeout_minutes | int | Maximum pipeline duration |
| parallel | bool | Whether stages run in parallel |

---

## Usage Patterns

### Pattern 1: Quick Code Scan

```python
from agents.development.agent import DevelopmentDashboard

dashboard = DevelopmentDashboard()
results = dashboard.analyze_code(open("my_module.py").read(), "my_module.py")

for issue in results["static_analysis"]["issues"]:
    print(f"[{issue['severity']}] {issue['message']} at line {issue['line']}")
```

### Pattern 2: Security-First Review

```python
from agents.development.agent import SecurityScanner

scanner = SecurityScanner()
vulns = scanner.scan_source(source_code, "app.py")
risk = scanner.calculate_risk_score(vulns)

if risk["risk_level"] in ("CRITICAL", "HIGH"):
    print(f"HIGH RISK: {risk['total_vulnerabilities']} vulnerabilities found")
    for v in vulns:
        print(f"  [{v.severity.name}] {v.title} ({v.cwe_id})")
```

### Pattern 3: CI/CD Integration

```python
from agents.development.agent import DevelopmentDashboard, CICDStage

dashboard = DevelopmentDashboard()

# Run quality gate
results = dashboard.analyze_code(source_code, "module.py")
gate = dashboard.quality.evaluate_quality_gate({
    "avg_complexity": results["static_analysis"]["complexity"],
    "avg_maintainability": results["static_analysis"]["maintainability_index"],
    "test_coverage": 85.0,
    "issues_by_severity": {"critical": 0, "high": 2},
})

if gate.status.value != "passed":
    raise SystemExit(f"Quality gate failed: {gate.summary}")
```

### Pattern 4: Batch Analysis

```python
from agents.development.agent import DevelopmentDashboard
from pathlib import Path

dashboard = DevelopmentDashboard()
all_results = []

for py_file in Path("src").rglob("*.py"):
    source = py_file.read_text(encoding="utf-8")
    result = dashboard.analyze_code(source, str(py_file))
    all_results.append(result)

# Aggregate
total_issues = sum(r["static_analysis"]["issue_count"] for r in all_results)
total_vulns = sum(len(r["security"]) for r in all_results)
print(f"Total issues: {total_issues}, Vulnerabilities: {total_vulns}")
```

---

## Checklists

### Pre-Commit Analysis Checklist

- [ ] Run static analysis on all modified files
- [ ] Check for hardcoded secrets (passwords, API keys, tokens)
- [ ] Verify no SQL injection patterns
- [ ] Confirm no eval()/exec() on user input
- [ ] Run quality gate checks
- [ ] Review refactoring suggestions
- [ ] Check cyclomatic complexity < 10
- [ ] Verify test coverage ≥ 80%

### Security Review Checklist

- [ ] Scan for OWASP Top 10 vulnerabilities
- [ ] Verify SSL/TLS verification is enabled
- [ ] Check CORS configuration
- [ ] Validate file path inputs (path traversal)
- [ ] Review YAML/JSON deserialization (unsafe loaders)
- [ ] Check for weak cryptographic algorithms
- [ ] Verify secrets are not hardcoded
- [ ] Review subprocess calls for shell injection

### CI/CD Pipeline Checklist

- [ ] Lint stage passes (ruff, mypy)
- [ ] Build stage completes successfully
- [ ] Unit test coverage ≥ 80%
- [ ] Security scan finds no CRITICAL/HIGH issues
- [ ] Staging deployment succeeds
- [ ] Integration tests pass
- [ ] Production deployment gate passes
- [ ] Post-deploy monitoring active

### Code Review Checklist

- [ ] No hardcoded secrets
- [ ] No debug print statements
- [ ] Exception handling is specific (no bare except)
- [ ] Lines ≤ 120 characters
- [ ] No eval()/exec() usage
- [ ] Functions have docstrings
- [ ] Tests cover new code
- [ ] Type hints present on public APIs

---

## Troubleshooting

### Issue: Analysis returns no results

**Possible causes:**
- Source code is empty or contains only whitespace
- File encoding issues (non-UTF-8)

**Resolution:**
```python
# Verify source code is non-empty
assert len(source_code.strip()) > 0, "Source code is empty"

# Ensure proper encoding
source = open("file.py", encoding="utf-8").read()
```

### Issue: High false positive rate on security scanning

**Possible causes:**
- Patterns match test code or documentation strings
- String literals contain keywords without actual vulnerability

**Resolution:**
- Review findings manually — security patterns are intentionally broad
- Use the `confidence` field to prioritize high-confidence findings
- Consider adding file-path-based exclusions for test directories

### Issue: Maintainability index unexpectedly low

**Possible causes:**
- Very long file with many functions
- Low comment ratio
- High complexity

**Resolution:**
```python
# Check individual metrics
metrics = engine.calculate_metrics(source_code)
print(f"LOC: {metrics['lines_of_code']}")
print(f"Comment ratio: {metrics['comment_ratio']}")
print(f"Function count: {metrics['function_count']}")
```

### Issue: Quality gate always fails

**Possible causes:**
- Standards set too aggressively for the codebase
- Pre-existing technical debt not yet addressed

**Resolution:**
```python
# Customize standards for your project
manager = CodeQualityManager()
manager.standards["max_complexity"] = {"value": 15, "unit": " McCabe"}
manager.standards["min_test_coverage"] = {"value": 70, "unit": "%"}
```

### Issue: Code generation produces incomplete output

**Possible causes:**
- Missing required parameters
- Unknown request type

**Resolution:**
```python
# Ensure all required parameters are provided
result = dashboard.generate_code("class", {
    "name": "MyClass",
    "attributes": ["field1", "field2"],  # Required for class generation
    "methods": ["method1"],              # Optional but recommended
})
```

---

*Agent version: 2.0.0 — Last updated: 2026-07-06*
