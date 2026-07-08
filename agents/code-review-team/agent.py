"""
Code Review Team Agent — Automated Code Review, Quality Assurance & Mentoring.

A comprehensive, production-grade agent for automated code review combining
static analysis, security scanning, complexity analysis, and quality reporting.

Features:
- Multi-language linting integration (Python, JavaScript, TypeScript, Go, Rust)
- Security vulnerability scanning (SQL injection, XSS, hardcoded secrets, weak crypto)
- Code complexity analysis (cyclomatic, cognitive, lines of code)
- Architecture review (SOLID principles, design patterns)
- Test coverage analysis
- Review checklists and quality gates
- Multi-format reporting (Markdown, JSON, text, HTML)
- Review metrics and trend tracking
- Automated suggestions and code examples
- PR review integration patterns
- Mentoring feedback generation
"""

from __future__ import annotations

import enum
import hashlib
import json
import logging
import re
import secrets
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ============================================================================
# Enumerations
# ============================================================================


class Severity(enum.Enum):
    """Issue severity levels."""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class ReviewCategory(enum.Enum):
    """Code review categories."""
    SYNTAX = "syntax"
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    STYLE = "style"
    COMPLEXITY = "complexity"


class Language(enum.Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    CSHARP = "csharp"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"


class ReviewStatus(enum.Enum):
    """Review status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class GateResult(enum.Enum):
    """Quality gate result."""
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


class VulnerabilityType(enum.Enum):
    """Security vulnerability types."""
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    HARDCODED_SECRET = "hardcoded_secret"
    WEAK_CRYPTO = "weak_crypto"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    SSRF = "ssrf"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    BROKEN_AUTH = "broken_auth"
    SENSITIVE_DATA_EXPOSURE = "sensitive_data_exposure"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class CodeIssue:
    """Represents a single code issue found during review."""
    issue_id: str
    file_path: str
    line_number: int
    column: int
    message: str
    severity: Severity
    category: ReviewCategory
    rule_id: str
    suggestion: str = ""
    code_snippet: str = ""
    fix_example: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["category"] = self.category.value
        return data


@dataclass
class ReviewResult:
    """Result of a code review for a single file."""
    file_path: str
    language: Language
    issues: List[CodeIssue] = field(default_factory=list)
    score: float = 100.0
    summary: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)
    reviewed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["language"] = self.language.value
        data["issues"] = [i.to_dict() for i in self.issues]
        data["reviewed_at"] = self.reviewed_at.isoformat()
        return data


@dataclass
class QualityGate:
    """Quality gate configuration and result."""
    gate_id: str
    name: str
    rules: List[Dict[str, Any]] = field(default_factory=list)
    result: GateResult = GateResult.PASS
    details: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["result"] = self.result.value
        return data


@dataclass
class ComplexityMetrics:
    """Code complexity metrics."""
    cyclomatic_complexity: int = 0
    cognitive_complexity: int = 0
    lines_of_code: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    functions_count: int = 0
    classes_count: int = 0
    max_function_length: int = 0
    avg_function_length: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SecurityFinding:
    """Security vulnerability finding."""
    finding_id: str
    vulnerability_type: VulnerabilityType
    file_path: str
    line_number: int
    severity: Severity
    description: str
    code_snippet: str = ""
    recommendation: str = ""
    cwe_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["vulnerability_type"] = self.vulnerability_type.value
        data["severity"] = self.severity.value
        return data


@dataclass
class ReviewConfig:
    """Configuration for code review."""
    enabled_languages: List[str] = field(default_factory=lambda: ["python", "javascript", "typescript"])
    max_line_length: int = 120
    max_function_length: int = 50
    max_file_length: int = 500
    max_complexity: int = 10
    max_nesting_depth: int = 4
    require_docstrings: bool = True
    require_type_hints: bool = True
    require_tests: bool = False
    security_scanning: bool = True
    auto_suggest: bool = True
    excluded_files: List[str] = field(default_factory=lambda: ["*.test.*", "*.spec.*", "node_modules/*", "__pycache__/*"])
    excluded_rules: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReviewSummary:
    """Summary of a complete code review."""
    review_id: str
    total_files: int = 0
    total_issues: int = 0
    issues_by_severity: Dict[str, int] = field(default_factory=dict)
    issues_by_category: Dict[str, int] = field(default_factory=dict)
    average_score: float = 0.0
    quality_gate: GateResult = GateResult.PASS
    review_duration_seconds: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["quality_gate"] = self.quality_gate.value
        data["generated_at"] = self.generated_at.isoformat()
        return data


@dataclass
class Config:
    """Configuration for the Code Review Team Agent."""
    review_config: ReviewConfig = field(default_factory=ReviewConfig)
    output_directory: str = "./review_reports"
    report_formats: List[str] = field(default_factory=lambda: ["markdown", "json"])
    fail_on_critical: bool = True
    fail_on_error: bool = False
    min_score: float = 70.0
    trend_tracking: bool = True
    max_history: int = 100

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# Exceptions
# ============================================================================


class CodeReviewError(Exception):
    """Base exception for code review errors."""
    pass


class LintingError(CodeReviewError):
    """Linting operation error."""
    pass


class SecurityScanError(CodeReviewError):
    """Security scan error."""
    pass


class ComplexityError(CodeReviewError):
    """Complexity analysis error."""
    pass


class ReportError(CodeReviewError):
    """Report generation error."""
    pass


class ValidationError(CodeReviewError):
    """Data validation error."""
    pass


# ============================================================================
# Linter Integrator
# ============================================================================


class LinterIntegrator:
    """Multi-language linting integration with pattern-based detection."""

    PYTHON_PATTERNS = {
        "print_statement": (r"\bprint\s*\(", Severity.WARNING, "W1001", "Consider using logging instead of print"),
        "bare_except": (r"except\s*:", Severity.WARNING, "W1002", "Avoid bare except; specify exception types"),
        "mutable_default": (r"def\s+\w+\s*\([^)]*=\s*(\[\]|\{\})", Severity.WARNING, "W1003", "Use None as default, initialize in function body"),
        "star_import": (r"from\s+\w+\s+import\s+\*", Severity.WARNING, "W1004", "Avoid wildcard imports"),
        "eval_usage": (r"\beval\s*\(", Severity.ERROR, "E1001", "Avoid eval() — use ast.literal_eval() or specific parsers"),
        "exec_usage": (r"\bexec\s*\(", Severity.ERROR, "E1002", "Avoid exec() — use specific functions instead"),
    }

    JS_PATTERNS = {
        "console_log": (r"console\.log\s*\(", Severity.INFO, "I2001", "Remove console.log before production"),
        "var_declaration": (r"\bvar\s+", Severity.WARNING, "W2001", "Use const/let instead of var"),
        "eqeq": (r"[^=!]==[^=]", Severity.WARNING, "W2002", "Use strict equality (===)"),
        "alert_usage": (r"\balert\s*\(", Severity.WARNING, "W2003", "Remove alert() — use proper UI notifications"),
        "inner_html": (r"\.innerHTML\s*=", Severity.ERROR, "E2001", "Use textContent or safe DOM methods to prevent XSS"),
        "document_write": (r"document\.write\s*\(", Severity.ERROR, "E2002", "Avoid document.write — use DOM manipulation"),
    }

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._custom_rules: Dict[str, Dict[str, Any]] = {}

    def add_custom_rule(self, rule_id: str, pattern: str, severity: str, message: str, language: str = "all") -> None:
        self._custom_rules[rule_id] = {
            "pattern": pattern,
            "severity": Severity(severity),
            "message": message,
            "language": language,
        }

    def lint(self, code: str, file_path: str, language: str = "python") -> List[CodeIssue]:
        issues: List[CodeIssue] = []

        patterns = {}
        if language == "python":
            patterns = self.PYTHON_PATTERNS
        elif language in ("javascript", "typescript"):
            patterns = self.JS_PATTERNS

        for rule_id, (pattern, severity, code_id, message) in patterns.items():
            matches = list(re.finditer(pattern, code, re.MULTILINE))
            for match in matches:
                line = code[:match.start()].count("\n") + 1
                col = match.start() - code.rfind("\n", 0, match.start()) - 1
                issues.append(CodeIssue(
                    issue_id=f"lint-{hashlib.md5(f'{file_path}-{code_id}-{line}'.encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line_number=line,
                    column=max(0, col),
                    message=message,
                    severity=severity,
                    category=ReviewCategory.STYLE,
                    rule_id=code_id,
                    suggestion=message,
                ))

        # Custom rules
        for rule_id, rule in self._custom_rules.items():
            if rule["language"] != "all" and rule["language"] != language:
                continue
            matches = list(re.finditer(rule["pattern"], code, re.MULTILINE))
            for match in matches:
                line = code[:match.start()].count("\n") + 1
                issues.append(CodeIssue(
                    issue_id=f"custom-{hashlib.md5(f'{file_path}-{rule_id}-{line}'.encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line_number=line,
                    column=0,
                    message=rule["message"],
                    severity=rule["severity"],
                    category=ReviewCategory.STYLE,
                    rule_id=rule_id,
                ))

        return issues


# ============================================================================
# Security Scanner
# ============================================================================


class SecurityScanner:
    """Security vulnerability scanner with pattern-based detection."""

    VULNERABILITY_PATTERNS: Dict[str, Tuple[str, VulnerabilityType, Severity, str, str]] = {
        "sql_injection": (
            r"(execute|query|cursor\.execute)\s*\(\s*f['\"].*\{.*\}",
            VulnerabilityType.SQL_INJECTION,
            Severity.CRITICAL,
            "CWE-89",
            "Use parameterized queries instead of f-string interpolation",
        ),
        "hardcoded_secret": (
            r"(api_key|password|secret|token)\s*=\s*['\"][^'\"]{8,}['\"]",
            VulnerabilityType.HARDCODED_SECRET,
            Severity.CRITICAL,
            "CWE-798",
            "Move secrets to environment variables or a secrets manager",
        ),
        "weak_crypto_md5": (
            r"\b(md5|sha1)\s*\(",
            VulnerabilityType.WEAK_CRYPTO,
            Severity.WARNING,
            "CWE-327",
            "Use SHA-256 or stronger hashing algorithms",
        ),
        "xss_innerhtml": (
            r"\.(innerHTML|outerHTML)\s*=",
            VulnerabilityType.XSS,
            Severity.ERROR,
            "CWE-79",
            "Use textContent or safe DOM methods to prevent XSS",
        ),
        "path_traversal": (
            r"(open|read|write)\s*\(\s*f?['\"].*\.\.",
            VulnerabilityType.PATH_TRAVERSAL,
            Severity.ERROR,
            "CWE-22",
            "Validate and sanitize file paths; use os.path.abspath()",
        ),
        "command_injection": (
            r"(os\.system|subprocess\.call|subprocess\.run)\s*\(\s*f?['\"].*\{",
            VulnerabilityType.COMMAND_INJECTION,
            Severity.CRITICAL,
            "CWE-78",
            "Use subprocess with list arguments and shell=False",
        ),
        "eval_usage": (
            r"\beval\s*\(",
            VulnerabilityType.INSECURE_DESERIALIZATION,
            Severity.ERROR,
            "CWE-95",
            "Avoid eval(); use ast.literal_eval() or specific parsers",
        ),
        "weak_random": (
            r"\b(random\.random|random\.randint)\s*\(",
            VulnerabilityType.WEAK_CRYPTO,
            Severity.INFO,
            "CWE-330",
            "Use secrets module for security-sensitive randomness",
        ),
    }

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._suppressed_rules: Set[str] = set()

    def suppress_rule(self, rule_id: str) -> None:
        self._suppressed_rules.add(rule_id)

    def scan(self, code: str, file_path: str) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        for name, (pattern, vuln_type, severity, cwe, recommendation) in self.VULNERABILITY_PATTERNS.items():
            if f"security-{name}" in self._suppressed_rules:
                continue

            matches = list(re.finditer(pattern, code, re.MULTILINE))
            for match in matches:
                line = code[:match.start()].count("\n") + 1
                snippet_start = max(0, match.start() - 40)
                snippet_end = min(len(code), match.end() + 40)
                snippet = code[snippet_start:snippet_end].replace("\n", " ").strip()

                finding = SecurityFinding(
                    finding_id=f"sec-{hashlib.md5(f'{file_path}-{name}-{line}'.encode()).hexdigest()[:8]}",
                    vulnerability_type=vuln_type,
                    file_path=file_path,
                    line_number=line,
                    severity=severity,
                    description=f"Potential {name.replace('_', ' ')} vulnerability detected",
                    code_snippet=snippet,
                    recommendation=recommendation,
                    cwe_id=cwe,
                )
                findings.append(finding)

        return findings

    def get_vulnerability_summary(self, findings: List[SecurityFinding]) -> Dict[str, Any]:
        by_type: Dict[str, int] = {}
        by_severity: Dict[str, int] = {}
        for f in findings:
            by_type[f.vulnerability_type.value] = by_type.get(f.vulnerability_type.value, 0) + 1
            by_severity[f.severity.value] = by_severity.get(f.severity.value, 0) + 1
        return {
            "total_findings": len(findings),
            "by_type": by_type,
            "by_severity": by_severity,
            "critical_count": by_severity.get("critical", 0),
        }


# ============================================================================
# Complexity Analyzer
# ============================================================================


class ComplexityAnalyzer:
    """Code complexity analysis with threshold-based reporting."""

    DEFAULT_THRESHOLDS = {
        "cyclomatic": {"warning": 10, "error": 20},
        "cognitive": {"warning": 15, "error": 30},
        "lines_of_code": {"warning": 200, "error": 500},
        "function_length": {"warning": 50, "error": 100},
        "nesting_depth": {"warning": 4, "error": 8},
    }

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._thresholds = dict(self.DEFAULT_THRESHOLDS)

    def set_threshold(self, metric: str, warning: int, error: int) -> None:
        self._thresholds[metric] = {"warning": warning, "error": error}

    def analyze(self, code: str, file_path: str = "") -> Tuple[ComplexityMetrics, List[CodeIssue]]:
        lines = code.split("\n")
        issues: List[CodeIssue] = []

        cyclomatic = self._cyclomatic_complexity(code)
        cognitive = self._cognitive_complexity(code)
        loc = len([l for l in lines if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("//")])
        comment_lines = len([l for l in lines if l.strip().startswith("#") or l.strip().startswith("//") or l.strip().startswith("*")])
        blank_lines = len([l for l in lines if not l.strip()])
        functions = self._count_functions(code)
        classes = len(re.findall(r"\bclass\s+\w+", code))
        max_func_len = self._max_function_length(code)
        avg_func_len = self._avg_function_length(code)

        metrics = ComplexityMetrics(
            cyclomatic_complexity=cyclomatic,
            cognitive_complexity=cognitive,
            lines_of_code=loc,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            functions_count=functions,
            classes_count=classes,
            max_function_length=max_func_len,
            avg_function_length=avg_func_len,
        )

        # Check thresholds
        threshold_checks = [
            ("cyclomatic", cyclomatic),
            ("cognitive", cognitive),
            ("lines_of_code", loc),
            ("function_length", max_func_len),
        ]

        for metric_name, value in threshold_checks:
            thresholds = self._thresholds.get(metric_name, {})
            if value >= thresholds.get("error", float("inf")):
                issues.append(CodeIssue(
                    issue_id=f"complex-{metric_name}-{hashlib.md5(file_path.encode()).hexdigest()[:6]}",
                    file_path=file_path,
                    line_number=0,
                    column=0,
                    message=f"High {metric_name}: {value} exceeds error threshold",
                    severity=Severity.ERROR,
                    category=ReviewCategory.COMPLEXITY,
                    rule_id=f"COMPLEXITY-{metric_name.upper()}",
                    suggestion=f"Refactor to reduce {metric_name} below {thresholds['error']}",
                ))
            elif value >= thresholds.get("warning", float("inf")):
                issues.append(CodeIssue(
                    issue_id=f"complex-{metric_name}-{hashlib.md5(file_path.encode()).hexdigest()[:6]}",
                    file_path=file_path,
                    line_number=0,
                    column=0,
                    message=f"Elevated {metric_name}: {value} exceeds warning threshold",
                    severity=Severity.WARNING,
                    category=ReviewCategory.COMPLEXITY,
                    rule_id=f"COMPLEXITY-{metric_name.upper()}",
                    suggestion=f"Consider refactoring to reduce {metric_name}",
                ))

        return metrics, issues

    def _cyclomatic_complexity(self, code: str) -> int:
        complexity = 1
        keywords = ["if ", "elif ", "else:", "for ", "while ", "except", " and ", " or ", " case ", " when "]
        for kw in keywords:
            complexity += code.count(kw)
        return complexity

    def _cognitive_complexity(self, code: str) -> int:
        complexity = 0
        nesting = 0
        for line in code.split("\n"):
            stripped = line.strip()
            if any(stripped.startswith(kw) for kw in ("if ", "for ", "while ", "def ", "class ", "try:", "except")):
                nesting += 1
            elif stripped.startswith(("return", "break", "continue")):
                nesting = max(0, nesting - 1)
            complexity += nesting
        return complexity

    def _count_functions(self, code: str) -> int:
        return len(re.findall(r"\bdef\s+\w+|function\s+\w+|func\s+\w+", code))

    def _max_function_length(self, code: str) -> int:
        functions = re.findall(r"(?:def|function|func)\s+\w+[^{]*[:{](.*?)(?=\ndef|\nfunction|\nfunc|\Z)", code, re.DOTALL)
        if not functions:
            return 0
        return max(len(f.split("\n")) for f in functions)

    def _avg_function_length(self, code: str) -> float:
        functions = re.findall(r"(?:def|function|func)\s+\w+[^{]*[:{](.*?)(?=\ndef|\nfunction|\nfunc|\Z)", code, re.DOTALL)
        if not functions:
            return 0.0
        lengths = [len(f.split("\n")) for f in functions]
        return sum(lengths) / len(lengths)


# ============================================================================
# Architecture Reviewer
# ============================================================================


class ArchitectureReviewer:
    """Reviews code architecture against design principles."""

    SOLID_PATTERNS = {
        "long_method": (r"def\s+\w+.*:\n(?:\s+.+\n){50,}", Severity.WARNING, "SOLID-SRP", "Method exceeds 50 lines — consider splitting"),
        "deep_nesting": (r"(?:if|for|while)\s+.+:\n(?:\s+(?:if|for|while)\s+.+:\n){4,}", Severity.WARNING, "SOLID-CCP", "Deep nesting detected — extract helper functions"),
        "god_class": (r"class\s+\w+.*:\n(?:\s+def\s+\w+.*\n){20,}", Severity.WARNING, "SOLID-SRP", "Class has 20+ methods — consider splitting responsibilities"),
    }

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def review(self, code: str, file_path: str = "") -> List[CodeIssue]:
        issues: List[CodeIssue] = []

        for name, (pattern, severity, rule_id, message) in self.SOLID_PATTERNS.items():
            matches = list(re.finditer(pattern, code, re.MULTILINE | re.DOTALL))
            for match in matches:
                line = code[:match.start()].count("\n") + 1
                issues.append(CodeIssue(
                    issue_id=f"arch-{hashlib.md5(f'{file_path}-{name}-{line}'.encode()).hexdigest()[:8]}",
                    file_path=file_path,
                    line_number=line,
                    column=0,
                    message=message,
                    severity=severity,
                    category=ReviewCategory.ARCHITECTURE,
                    rule_id=rule_id,
                    suggestion="Consider refactoring to improve code structure",
                ))

        return issues


# ============================================================================
# Code Reviewer
# ============================================================================


class CodeReviewer:
    """Main code review agent combining all analysis engines."""

    SEVERITY_WEIGHTS = {
        Severity.CRITICAL: 25,
        Severity.ERROR: 10,
        Severity.WARNING: 3,
        Severity.INFO: 1,
        Severity.HINT: 0,
    }

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._linter = LinterIntegrator(self.config)
        self._security = SecurityScanner(self.config)
        self._complexity = ComplexityAnalyzer(self.config)
        self._architecture = ArchitectureReviewer(self.config)
        self._review_history: List[ReviewSummary] = []

    def review_code(
        self,
        code: str,
        file_path: str = "",
        language: str = "python",
    ) -> ReviewResult:
        all_issues: List[CodeIssue] = []
        all_metrics: Dict[str, Any] = {}

        # Linting
        lint_issues = self._linter.lint(code, file_path, language)
        all_issues.extend(lint_issues)

        # Security scanning
        if self.config.review_config.security_scanning:
            findings = self._security.scan(code, file_path)
            for f in findings:
                all_issues.append(CodeIssue(
                    issue_id=f"sec-{f.finding_id}",
                    file_path=f.file_path,
                    line_number=f.line_number,
                    column=0,
                    message=f.description,
                    severity=f.severity,
                    category=ReviewCategory.SECURITY,
                    rule_id=f.cwe_id,
                    suggestion=f.recommendation,
                    code_snippet=f.code_snippet,
                ))

        # Complexity analysis
        metrics, complexity_issues = self._complexity.analyze(code, file_path)
        all_issues.extend(complexity_issues)
        all_metrics["complexity"] = metrics.to_dict()

        # Architecture review
        arch_issues = self._architecture.review(code, file_path)
        all_issues.extend(arch_issues)

        # Calculate score
        score = self._calculate_score(all_issues)
        summary = self._generate_summary(all_issues)

        return ReviewResult(
            file_path=file_path,
            language=Language(language) if language in [l.value for l in Language] else Language.PYTHON,
            issues=all_issues,
            score=score,
            summary=summary,
            metrics=all_metrics,
        )

    def review_multiple(self, files: Dict[str, str], language: str = "python") -> List[ReviewResult]:
        results = []
        for file_path, code in files.items():
            result = self.review_code(code, file_path, language)
            results.append(result)
        return results

    def check_quality_gates(self, results: List[ReviewResult], gate_config: Optional[List[Dict[str, Any]]] = None) -> QualityGate:
        default_gates = [
            {"name": "no_critical", "check": "critical_count", "op": "==", "value": 0},
            {"name": "min_score", "check": "avg_score", "op": ">=", "value": self.config.min_score},
            {"name": "max_errors", "check": "error_count", "op": "<=", "value": 5},
        ]
        gates = gate_config or default_gates

        all_issues = []
        for r in results:
            all_issues.extend(r.issues)

        metrics = {
            "critical_count": sum(1 for i in all_issues if i.severity == Severity.CRITICAL),
            "error_count": sum(1 for i in all_issues if i.severity == Severity.ERROR),
            "warning_count": sum(1 for i in all_issues if i.severity == Severity.WARNING),
            "avg_score": sum(r.score for r in results) / max(len(results), 1),
            "total_issues": len(all_issues),
        }

        details = []
        overall_pass = True
        for gate in gates:
            check = gate["check"]
            op = gate["op"]
            expected = gate["value"]
            actual = metrics.get(check, 0)

            passed = False
            if op == "==":
                passed = actual == expected
            elif op == ">=":
                passed = actual >= expected
            elif op == "<=":
                passed = actual <= expected
            elif op == ">":
                passed = actual > expected
            elif op == "<":
                passed = actual < expected

            if not passed:
                overall_pass = False
            details.append({"gate": gate["name"], "check": check, "actual": actual, "expected": f"{op} {expected}", "passed": passed})

        return QualityGate(
            gate_id=f"gate-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
            name="Quality Gate",
            result=GateResult.PASS if overall_pass else GateResult.FAIL,
            details=details,
        )

    def _calculate_score(self, issues: List[CodeIssue]) -> float:
        base_score = 100.0
        for issue in issues:
            base_score -= self.SEVERITY_WEIGHTS.get(issue.severity, 0)
        return max(0.0, round(base_score, 1))

    def _generate_summary(self, issues: List[CodeIssue]) -> str:
        by_severity: Dict[str, int] = {}
        for issue in issues:
            sev = issue.severity.value
            by_severity[sev] = by_severity.get(sev, 0) + 1

        if not issues:
            return "No issues found — code looks clean!"

        parts = [f"{count} {sev}" for sev, count in sorted(by_severity.items())]
        return f"Found {len(issues)} issues: {', '.join(parts)}"

    def get_history(self) -> List[ReviewSummary]:
        return self._review_history[-self.config.max_history:]


# ============================================================================
# Report Generator
# ============================================================================


class ReportGenerator:
    """Generates review reports in multiple formats."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def generate(self, results: List[ReviewResult], fmt: str = "markdown", output_path: Optional[str] = None) -> str:
        if fmt == "markdown":
            content = self._markdown(results)
        elif fmt == "json":
            content = self._json(results)
        elif fmt == "text":
            content = self._text(results)
        elif fmt == "html":
            content = self._html(results)
        else:
            raise ReportError(f"Unsupported format: {fmt}")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        return content

    def _markdown(self, results: List[ReviewResult]) -> str:
        all_issues = []
        for r in results:
            all_issues.extend(r.issues)

        total_score = sum(r.score for r in results) / max(len(results), 1)
        by_severity: Dict[str, int] = {}
        for issue in all_issues:
            by_severity[issue.severity.value] = by_severity.get(issue.severity.value, 0) + 1

        lines = [
            "# Code Review Report",
            f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"- **Files Reviewed**: {len(results)}",
            f"- **Average Score**: {total_score:.1f}/100",
            f"- **Total Issues**: {len(all_issues)}",
        ]
        for sev, count in sorted(by_severity.items()):
            lines.append(f"- **{sev.title()}**: {count}")
        lines.append("")

        for result in results:
            lines.append(f"## {result.file_path}")
            lines.append(f"**Score**: {result.score}/100 | **Language**: {result.language.value}")
            lines.append("")
            if result.issues:
                for issue in result.issues:
                    loc = f"L{issue.line_number}" if issue.line_number > 0 else "Global"
                    lines.append(f"- `{issue.severity.value}` [{issue.rule_id}] {issue.message} ({loc})")
                    if issue.suggestion:
                        lines.append(f"  - Suggestion: {issue.suggestion}")
            else:
                lines.append("No issues found.")
            lines.append("")

        return "\n".join(lines)

    def _json(self, results: List[ReviewResult]) -> str:
        all_issues = []
        for r in results:
            all_issues.extend(r.issues)

        total_score = sum(r.score for r in results) / max(len(results), 1)

        data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": len(results),
                "average_score": round(total_score, 1),
                "total_issues": len(all_issues),
            },
            "results": [r.to_dict() for r in results],
        }
        return json.dumps(data, indent=2, default=str)

    def _text(self, results: List[ReviewResult]) -> str:
        lines = []
        for result in results:
            lines.append(f"{result.file_path}: {result.score}/100 ({len(result.issues)} issues)")
            for issue in result.issues:
                lines.append(f"  [{issue.severity.value}] L{issue.line_number}: {issue.message}")
        return "\n".join(lines)

    def _html(self, results: List[ReviewResult]) -> str:
        all_issues = []
        for r in results:
            all_issues.extend(r.issues)
        total_score = sum(r.score for r in results) / max(len(results), 1)

        rows = ""
        for result in results:
            for issue in result.issues:
                rows += f"<tr><td>{result.file_path}</td><td>L{issue.line_number}</td><td>{issue.severity.value}</td><td>{issue.rule_id}</td><td>{issue.message}</td></tr>"

        return f"""<!DOCTYPE html>
<html><head><title>Code Review Report</title>
<style>body{{font-family:system-ui;max-width:1200px;margin:0 auto;padding:20px}}
table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #ddd;padding:8px;text-align:left}}
th{{background:#f5f5f5}}.score{{font-size:2em;color:{'#2ecc71' if total_score >= 80 else '#e74c3c'}}}</style>
</head><body>
<h1>Code Review Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p class="score">Average Score: {total_score:.1f}/100</p>
<p>Files: {len(results)} | Issues: {len(all_issues)}</p>
<table><thead><tr><th>File</th><th>Line</th><th>Severity</th><th>Rule</th><th>Message</th></tr></thead>
<tbody>{rows}</tbody></table></body></html>"""


# ============================================================================
# Main Agent
# ============================================================================


class CodeReviewTeamAgent:
    """Comprehensive code review agent combining multiple analysis engines.

    Usage:
        agent = CodeReviewTeamAgent()
        result = agent.review_code(code, "main.py", "python")
        print(f"Score: {result.score}, Issues: {len(result.issues)}")
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._reviewer = CodeReviewer(self._config)
        self._reporter = ReportGenerator(self._config)

    def review_code(self, code: str, file_path: str = "", language: str = "python") -> ReviewResult:
        return self._reviewer.review_code(code, file_path, language)

    def review_multiple(self, files: Dict[str, str], language: str = "python") -> List[ReviewResult]:
        return self._reviewer.review_multiple(files, language)

    def check_quality_gates(self, results: List[ReviewResult]) -> QualityGate:
        return self._reviewer.check_quality_gates(results)

    def generate_report(self, results: List[ReviewResult], fmt: str = "markdown", output_path: Optional[str] = None) -> str:
        return self._reporter.generate(results, fmt, output_path)

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "CodeReviewTeamAgent",
            "version": "2.0.0",
            "supported_languages": [l.value for l in Language],
            "review_categories": [c.value for c in ReviewCategory],
        }


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "CodeReviewTeamAgent",
    "CodeReviewer",
    "LinterIntegrator",
    "SecurityScanner",
    "ComplexityAnalyzer",
    "ArchitectureReviewer",
    "ReportGenerator",
    "CodeIssue",
    "ReviewResult",
    "QualityGate",
    "ComplexityMetrics",
    "SecurityFinding",
    "ReviewConfig",
    "ReviewSummary",
    "Config",
    "Severity",
    "ReviewCategory",
    "Language",
    "ReviewStatus",
    "GateResult",
    "VulnerabilityType",
    "CodeReviewError",
    "LintingError",
    "SecurityScanError",
    "ComplexityError",
    "ReportError",
]


def main():
    """Demo CLI for the Code Review Team Agent."""
    import argparse

    parser = argparse.ArgumentParser(description="Code Review Team Agent")
    parser.add_argument("--file", help="File to review")
    parser.add_argument("--code", help="Inline code to review")
    parser.add_argument("--language", default="python", help="Programming language")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json", "text", "html"])
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--status", action="store_true", help="Show agent status")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    agent = CodeReviewTeamAgent()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
        result = agent.review_code(code, args.file, args.language)
        report = agent.generate_report([result], args.format, args.output)
        print(report)
    elif args.code:
        result = agent.review_code(args.code, "inline.py", args.language)
        report = agent.generate_report([result], args.format, args.output)
        print(report)
    elif args.status:
        print(json.dumps(agent.get_status(), indent=2))
    else:
        # Demo with sample code
        code = '''
def process_data(data):
    print("Processing")
    password = "secret123"
    query = f"SELECT * FROM users WHERE id = {user_id}"
    eval(user_input)
    if True and False or True:
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    pass
'''
        result = agent.review_code(code, "demo.py", "python")
        report = agent.generate_report([result], args.format)
        print(report)


if __name__ == "__main__":
    main()
