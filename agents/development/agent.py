"""
Development Agent
Software development analysis, architecture patterns, testing strategies,
code quality, documentation, CI/CD, security scanning, performance optimization,
refactoring, and code review.
"""

import re, math, logging, time, textwrap
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter
from abc import ABC, abstractmethod
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ── Enums ──────────────────────────────────────────────────────────────

class IssueSeverity(Enum):
    INFO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5
    def __ge__(self, o): return self.value >= o.value if self.__class__ is o.__class__ else NotImplemented
    def __gt__(self, o): return self.value > o.value if self.__class__ is o.__class__ else NotImplemented
    def __le__(self, o): return self.value <= o.value if self.__class__ is o.__class__ else NotImplemented
    def __lt__(self, o): return self.value < o.value if self.__class__ is o.__class__ else NotImplemented

class IssueType(Enum):
    BUG = "bug"; SECURITY = "security"; PERFORMANCE = "performance"
    CODE_QUALITY = "code_quality"; STYLE = "style"; DOCUMENTATION = "documentation"
    DESIGN = "design"; TESTING = "testing"; MAINTENANCE = "maintenance"

class CodeSmell(Enum):
    LONG_METHOD = "long_method"; LARGE_CLASS = "large_class"; DUPLICATED_CODE = "duplicated_code"
    DEAD_CODE = "dead_code"; GOD_CLASS = "god_class"; FEATURE_ENVY = "feature_envy"
    DATA_CLUMPS = "data_clumps"; SWITCH_STATEMENTS = "switch_statements"

class ArchitecturePattern(Enum):
    MVC = "mvc"; MVVM = "mvvm"; LAYERED = "layered"; MICROSERVICES = "microservices"
    EVENT_DRIVEN = "event_driven"; HEXAGONAL = "hexagonal"
    CLEAN_ARCHITECTURE = "clean_architecture"; REPOSITORY = "repository"

class TestType(Enum):
    UNIT = "unit"; INTEGRATION = "integration"; FUNCTIONAL = "functional"
    PERFORMANCE = "performance"; SECURITY = "security"; E2E = "e2e"

class TestFramework(Enum):
    PYTEST = "pytest"; UNITTEST = "unittest"; NOSE = "nose2"

class CICDStage(Enum):
    LINT = "lint"; BUILD = "build"; TEST = "test"; SECURITY_SCAN = "security_scan"
    DEPLOY_STAGING = "deploy_staging"; INTEGRATION_TEST = "integration_test"
    DEPLOY_PRODUCTION = "deploy_production"; MONITOR = "monitor"

class SecurityVulnCategory(Enum):
    INJECTION = "injection"; BROKEN_AUTH = "broken_authentication"
    SENSITIVE_DATA = "sensitive_data_exposure"; XSS = "cross_site_scripting"
    BROKEN_ACCESS = "broken_access_control"; SECURITY_MISCONFIG = "security_misconfiguration"
    INSECURE_DESER = "insecure_deserialization"; SSRF = "server_side_request_forgery"
    PATH_TRAVERSAL = "path_traversal"

class RefactoringType(Enum):
    EXTRACT_METHOD = "extract_method"; EXTRACT_CLASS = "extract_class"
    INLINE_METHOD = "inline_method"; RENAME_VARIABLE = "rename_variable"
    INTRODUCE_PARAMETER_OBJECT = "introduce_parameter_object"
    DECOMPOSE_CONDITIONAL = "decompose_conditional"

class QualityGateStatus(Enum):
    PASSED = "passed"; FAILED = "failed"; WARNING = "warning"; SKIPPED = "skipped"


# ── Data Classes ───────────────────────────────────────────────────────

@dataclass
class CodeIssue:
    issue_id: str; file_path: str; line_number: int; issue_type: IssueType; severity: IssueSeverity
    message: str; code_snippet: str; suggestion: str; rule_id: str
    column: int = 0; fix_available: bool = False; confidence: float = 1.0
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.issue_id, "file": self.file_path, "line": self.line_number,
                "type": self.issue_type.value, "severity": self.severity.name,
                "message": self.message, "snippet": self.code_snippet,
                "suggestion": self.suggestion, "rule_id": self.rule_id,
                "fix_available": self.fix_available, "confidence": self.confidence}

@dataclass
class RefactoringSuggestion:
    file_path: str; line_number: int; original_code: str; suggested_code: str
    reason: str; effort: str; refactoring_type: RefactoringType = RefactoringType.EXTRACT_METHOD
    risk_level: str = "low"; estimated_time_minutes: int = 15
    def to_dict(self) -> Dict[str, Any]:
        return {"file": self.file_path, "line": self.line_number, "original": self.original_code,
                "suggested": self.suggested_code, "reason": self.reason, "effort": self.effort,
                "type": self.refactoring_type.value, "risk": self.risk_level,
                "estimated_minutes": self.estimated_time_minutes}

@dataclass
class TestResult:
    test_id: str; test_name: str; test_type: TestType; status: str; duration_ms: float
    assertion_count: int = 0; error_message: str = ""; coverage_percent: float = 0.0; timestamp: str = ""
    def __post_init__(self):
        if not self.timestamp: self.timestamp = datetime.utcnow().isoformat()

@dataclass
class SecurityVulnerability:
    vuln_id: str; file_path: str; line_number: int; category: SecurityVulnCategory
    severity: IssueSeverity; title: str; description: str; cwe_id: str = ""
    cvss_score: float = 0.0; remediation: str = ""; references: List[str] = field(default_factory=list)
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.vuln_id, "file": self.file_path, "line": self.line_number,
                "category": self.category.value, "severity": self.severity.name,
                "title": self.title, "description": self.description,
                "cwe": self.cwe_id, "cvss": self.cvss_score, "remediation": self.remediation}

@dataclass
class PerformanceMetric:
    metric_name: str; value: float; unit: str; threshold: float; status: str = ""; context: str = ""
    def __post_init__(self):
        if not self.status: self.status = "pass" if self.value <= self.threshold else "fail"

@dataclass
class QualityGateResult:
    gate_name: str; status: QualityGateStatus
    checks: List[Dict[str, Any]] = field(default_factory=list); summary: str = ""; timestamp: str = ""
    def __post_init__(self):
        if not self.timestamp: self.timestamp = datetime.utcnow().isoformat()

@dataclass
class DocumentationNode:
    node_id: str; title: str; content: str; node_type: str
    children: List[str] = field(default_factory=list); parent_id: str = ""

@dataclass
class PipelineConfig:
    pipeline_id: str; name: str; stages: List[CICDStage] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    timeout_minutes: int = 60; parallel: bool = False

@dataclass
class CodeReviewComment:
    comment_id: str; file_path: str; line_number: int; author: str; content: str
    category: str; severity: IssueSeverity; is_resolved: bool = False; timestamp: str = ""
    def __post_init__(self):
        if not self.timestamp: self.timestamp = datetime.utcnow().isoformat()

@dataclass
class DependencyInfo:
    name: str; current_version: str; latest_version: str; license: str
    is_outdated: bool = False; is_vulnerable: bool = False
    vulnerability_ids: List[str] = field(default_factory=list)


# ── Abstract Base ──────────────────────────────────────────────────────

class AnalysisEngine(ABC):
    @abstractmethod
    def analyze(self, source_code: str, file_path: str = "") -> Dict[str, Any]: ...
    @abstractmethod
    def get_engine_name(self) -> str: ...


# ── Static Analysis Engine ────────────────────────────────────────────

class StaticAnalysisEngine(AnalysisEngine):
    SECURITY_PATTERNS: List[Tuple[str, IssueType, IssueSeverity, str, str]] = [
        (r'password\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH, "Hardcoded password detected", "Use environment variables or a secure vault"),
        (r'secret\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH, "Hardcoded secret detected", "Use secure secret management"),
        (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH, "Hardcoded API key detected", "Rotate the key and use an environment variable"),
        (r'SQL\s*:\s*["\'][^"\']*["\']', IssueType.SECURITY, IssueSeverity.CRITICAL, "SQL injection vulnerability", "Use parameterized queries or an ORM"),
        (r'eval\s*\(', IssueType.SECURITY, IssueSeverity.HIGH, "Dangerous eval() usage", "Avoid eval; use ast.literal_eval or a safe parser"),
        (r'exec\s*\(', IssueType.SECURITY, IssueSeverity.HIGH, "Dangerous exec() usage", "Refactor to avoid dynamic code execution"),
        (r'pickle\.loads?\s*\(', IssueType.SECURITY, IssueSeverity.MEDIUM, "Unsafe pickle deserialization", "Use JSON or a safe serialization format"),
        (r'subprocess\.call.*shell\s*=\s*True', IssueType.SECURITY, IssueSeverity.HIGH, "Shell injection via subprocess", "Use a list of arguments instead of shell=True"),
        (r'os\.system\s*\(', IssueType.SECURITY, IssueSeverity.MEDIUM, "System call detected", "Use subprocess with a list of arguments"),
        (r'hashlib\.md5\s*\(', IssueType.SECURITY, IssueSeverity.LOW, "MD5 hash usage", "Use SHA-256 or stronger for security purposes"),
    ]
    QUALITY_PATTERNS: List[Tuple[str, IssueType, IssueSeverity, str, str]] = [
        (r'\bTODO\b', IssueType.DOCUMENTATION, IssueSeverity.INFO, "TODO comment found", "Address the TODO or create a tracking ticket"),
        (r'\bFIXME\b', IssueType.CODE_QUALITY, IssueSeverity.LOW, "FIXME comment found", "Resolve the technical debt"),
        (r'\bHACK\b', IssueType.CODE_QUALITY, IssueSeverity.MEDIUM, "HACK comment found", "Replace with a proper implementation"),
        (r'except\s*:', IssueType.BUG, IssueSeverity.MEDIUM, "Bare except clause", "Catch specific exceptions for proper error handling"),
        (r'except\s+Exception\s*:', IssueType.BUG, IssueSeverity.LOW, "Broad Exception catch", "Catch more specific exception types"),
        (r'\bpass\s*$', IssueType.CODE_QUALITY, IssueSeverity.LOW, "Empty pass statement", "Add implementation, a docstring, or raise NotImplementedError"),
        (r'\bprint\s*\(', IssueType.CODE_QUALITY, IssueSeverity.LOW, "Debug print statement", "Replace with logging for production code"),
        (r'\bglobal\s+\w+', IssueType.CODE_QUALITY, IssueSeverity.MEDIUM, "Global variable usage", "Use class attributes, parameters, or dependency injection"),
    ]

    def __init__(self):
        self.issues: List[CodeIssue] = []
        self._counter: int = 0

    def get_engine_name(self) -> str: return "StaticAnalysisEngine"

    def analyze(self, source_code: str, file_path: str = "") -> Dict[str, Any]:
        logger.info("Analyzing file: %s (%d bytes)", file_path, len(source_code))
        lines = source_code.split("\n")
        non_empty = [line for line in lines if line.strip()]
        issues = self.scan_for_issues(source_code, file_path)
        complexity = self.calculate_cyclomatic_complexity(source_code)
        metrics = self.calculate_metrics(source_code)
        maintainability = self.calculate_maintainability(metrics, complexity)
        results = {
            "file": file_path, "lines_of_code": len(non_empty),
            "total_lines": len(lines),
            "issues": [i.to_dict() for i in issues], "issue_count": len(issues),
            "complexity": complexity, "metrics": metrics,
            "maintainability_index": maintainability,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.issues.extend(issues)
        logger.info("Analysis complete: %d issues, complexity=%d, maintainability=%.1f",
                     len(issues), complexity, maintainability)
        return results

    def scan_for_issues(self, source_code: str, file_path: str = "") -> List[CodeIssue]:
        issues: List[CodeIssue] = []
        for pattern, itype, sev, msg, sug in self.SECURITY_PATTERNS + self.QUALITY_PATTERNS:
            for line_num in self._find_matches(source_code, pattern):
                self._counter += 1
                issues.append(CodeIssue(
                    issue_id=f"SA-{self._counter:05d}", file_path=file_path,
                    line_number=line_num, issue_type=itype, severity=sev,
                    message=msg, code_snippet=self._get_line(source_code, line_num),
                    suggestion=sug, rule_id=pattern[:30]))
        issues.sort(key=lambda i: (-i.severity.value, i.line_number))
        return issues

    def _find_matches(self, source_code: str, pattern: str) -> List[int]:
        return [idx for idx, line in enumerate(source_code.split("\n"), 1)
                if re.search(pattern, line, re.IGNORECASE)]

    @staticmethod
    def _get_line(source_code: str, line_number: int) -> str:
        lines = source_code.split("\n")
        return lines[line_number - 1].rstrip() if 1 <= line_number <= len(lines) else ""

    def calculate_cyclomatic_complexity(self, source_code: str) -> int:
        complexity = 1
        for kw in ["if", "elif", "for", "while", "except", "with", "assert", "and", "or"]:
            complexity += source_code.lower().count(kw)
        return complexity

    def calculate_halstead_volume(self, source_code: str) -> float:
        operators: Set[str] = set()
        operands: Set[str] = set()
        op_words = {"if", "else", "elif", "for", "while", "return", "def", "class",
                     "import", "from", "try", "except", "with", "as", "and", "or", "not", "in", "is"}
        for line in source_code.split("\n"):
            for token in line.split():
                if token in op_words: operators.add(token)
                elif re.match(r'^[a-zA-Z_]\w*$', token): operands.add(token)
                elif re.match(r'^\d+(\.\d+)?$', token): operands.add(token)
        n = len(operators) + len(operands) or 1
        return round(n * math.log2(n) if n > 1 else 0, 2)

    def calculate_metrics(self, source_code: str) -> Dict[str, Any]:
        lines = source_code.split("\n")
        non_empty = [l for l in lines if l.strip()]
        comments = [l for l in lines if l.strip().startswith("#")]
        blanks = [l for l in lines if not l.strip()]
        fns = len(re.findall(r'^\s*def\s+\w+', source_code, re.MULTILINE))
        cls = len(re.findall(r'^\s*class\s+\w+', source_code, re.MULTILINE))
        imps = len(re.findall(r'^\s*(?:import|from)\s+', source_code, re.MULTILINE))
        avg_len = sum(len(l) for l in non_empty) / len(non_empty) if non_empty else 0
        max_len = max((len(l) for l in non_empty), default=0)
        long_lines = sum(1 for l in non_empty if len(l) > 120)
        return {
            "lines_of_code": len(non_empty), "total_lines": len(lines),
            "blank_lines": len(blanks), "comment_lines": len(comments),
            "comment_ratio": round(len(comments) / len(non_empty), 3) if non_empty else 0,
            "function_count": fns, "class_count": cls, "import_count": imps,
            "average_line_length": round(avg_len, 1), "max_line_length": max_len,
            "long_lines_count": long_lines,
            "halstead_volume": self.calculate_halstead_volume(source_code),
        }

    def calculate_maintainability(self, metrics: Dict[str, Any], complexity: int) -> float:
        loc = max(metrics.get("lines_of_code", 100), 1)
        fc = max(metrics.get("function_count", 1), 1)
        cr = metrics.get("comment_ratio", 0)
        raw = 171 - 5.2 * math.log(loc) - 0.23 * complexity - 16.2 * math.log(fc) + cr * 10
        return round(max(0.0, min(100.0, raw)), 1)


# ── Code Refactoring Engine ──────────────────────────────────────────

class CodeRefactoringEngine(AnalysisEngine):
    def __init__(self):
        self.suggestions: List[RefactoringSuggestion] = []
        self._counter: int = 0

    def get_engine_name(self) -> str: return "CodeRefactoringEngine"

    def analyze(self, source_code: str, file_path: str = "") -> Dict[str, Any]:
        suggestions = self.analyze_for_refactoring(source_code, file_path)
        naming = self.suggest_naming_improvements(source_code, file_path)
        all_s = suggestions + naming
        effort: Dict[str, int] = defaultdict(int)
        for s in all_s: effort[s.effort] += 1
        return {"file": file_path, "suggestions": [s.to_dict() for s in all_s],
                "total_suggestions": len(all_s), "effort_breakdown": dict(effort)}

    def analyze_for_refactoring(self, source_code: str, file_path: str = "target.py") -> List[RefactoringSuggestion]:
        suggestions: List[RefactoringSuggestion] = []
        lines = source_code.split("\n")
        # Long methods
        method_lines, method_start, in_method = 0, 0, False
        for i, line in enumerate(lines):
            if re.match(r'^\s*def\s+', line):
                if in_method and method_lines > 50:
                    self._counter += 1
                    suggestions.append(RefactoringSuggestion(
                        file_path=file_path, line_number=method_start + 1,
                        original_code=f"Method at line {method_start + 1} ({method_lines} lines)",
                        suggested_code="Split into smaller, focused methods",
                        reason=f"Method spans {method_lines} lines; aim for <30",
                        effort="medium", refactoring_type=RefactoringType.EXTRACT_METHOD,
                        risk_level="medium", estimated_time_minutes=30))
                in_method = True; method_start = i; method_lines = 0
            elif in_method:
                if line.strip() and not line.strip().startswith("#"): method_lines += 1
                if line.strip() and not line.startswith(" ") and not line.startswith("\t") and not line.strip().startswith("def"):
                    in_method = False
        # Global variables
        for i, line in enumerate(lines):
            if re.match(r'^\s*global\s+\w+', line):
                self._counter += 1
                suggestions.append(RefactoringSuggestion(
                    file_path=file_path, line_number=i + 1,
                    original_code=line.strip(),
                    suggested_code="Use class attributes, parameters, or dependency injection",
                    reason="Global variables make code harder to test and maintain",
                    effort="medium", refactoring_type=RefactoringType.RENAME_VARIABLE))
        # Missing main guard
        if "if __name__" not in source_code and len(lines) > 20:
            self._counter += 1
            suggestions.append(RefactoringSuggestion(
                file_path=file_path, line_number=len(lines),
                original_code="# Module-level execution code",
                suggested_code='if __name__ == "__main__":\n    main()',
                reason="Add a main guard to prevent code execution on import",
                effort="low", estimated_time_minutes=5))
        # Too many parameters
        for match in re.finditer(r'^\s*def\s+\w+\s*\(([^)]*)\)', source_code, re.MULTILINE):
            params = [p.strip().split(":")[0].strip() for p in match.group(1).split(",")
                      if p.strip() and p.strip() != "self"]
            if len(params) > 5:
                self._counter += 1
                suggestions.append(RefactoringSuggestion(
                    file_path=file_path,
                    line_number=source_code[:match.start()].count("\n") + 1,
                    original_code=match.group(0).strip(),
                    suggested_code="Introduce a parameter object or dataclass",
                    reason=f"Function has {len(params)} parameters; aim for ≤5",
                    effort="medium", refactoring_type=RefactoringType.INTRODUCE_PARAMETER_OBJECT))
        # Deep nesting
        max_depth = 0
        for line in lines:
            if line.strip() and not line.strip().startswith("#"):
                depth = (len(line) - len(line.lstrip())) // 4
                max_depth = max(max_depth, depth)
        if max_depth > 4:
            self._counter += 1
            suggestions.append(RefactoringSuggestion(
                file_path=file_path, line_number=1,
                original_code=f"Maximum nesting depth: {max_depth}",
                suggested_code="Extract nested logic into helper methods or use early returns",
                reason=f"Nesting depth of {max_depth} reduces readability; aim for ≤3",
                effort="medium", refactoring_type=RefactoringType.DECOMPOSE_CONDITIONAL))
        self.suggestions.extend(suggestions)
        return suggestions

    def suggest_naming_improvements(self, source_code: str, file_path: str = "target.py") -> List[RefactoringSuggestion]:
        suggestions: List[RefactoringSuggestion] = []
        bad_names = [
            ("x", "x_coord", "Use descriptive variable names"),
            ("y", "y_coord", "Use descriptive variable names"),
            ("temp", "temporary_value", "Avoid vague temp variables"),
            ("data", "user_data", "Be more specific about data type"),
            ("info", "account_info", "Be more specific about info type"),
            ("lst", "item_list", "Avoid abbreviations"),
            ("dict", "config_dict", "Avoid Python builtins as variable names"),
            ("list", "item_list", "Avoid Python builtins as variable names"),
            ("val", "computed_value", "Use descriptive names"),
            ("cnt", "count", "Use full word"),
        ]
        for bad, good, reason in bad_names:
            if re.search(rf'\b{bad}\b', source_code):
                self._counter += 1
                suggestions.append(RefactoringSuggestion(
                    file_path=file_path, line_number=1, original_code=bad,
                    suggested_code=good, reason=reason, effort="low",
                    refactoring_type=RefactoringType.RENAME_VARIABLE,
                    estimated_time_minutes=5))
        return suggestions

# ── Dependency Analyzer ──────────────────────────────────────────────

class DependencyAnalyzer:
    def __init__(self): self.dependencies: Dict[str, DependencyInfo] = {}

    def analyze_dependencies(self, package_file: str = "requirements.txt", lock_file: str = "") -> Dict[str, Any]:
        direct = {"requests": {"version": "2.28.0", "latest": "2.31.0"},
                  "flask": {"version": "2.3.0", "latest": "3.0.0"},
                  "numpy": {"version": "1.24.0", "latest": "1.26.0"},
                  "pandas": {"version": "2.0.0", "latest": "2.1.0"},
                  "django": {"version": "4.2.0", "latest": "4.2.7"},
                  "fastapi": {"version": "0.100.0", "latest": "0.104.1"}}
        transitive = {"certifi": "2023.7.22", "urllib3": "2.1.0", "werkzeug": "3.0.1",
                      "jinja2": "3.1.2", "click": "8.1.7"}
        outdated = [{"name": n, "current": v["version"], "latest": v["latest"],
                     "update_type": "major" if v["version"].split(".")[0] != v["latest"].split(".")[0] else "minor"}
                    for n, v in direct.items() if v["version"] != v["latest"]]
        vulnerable = [
            {"name": "requests", "version": "2.28.0", "cve": "CVE-2023-32681", "severity": "medium"},
            {"name": "werkzeug", "version": "2.3.0", "cve": "CVE-2023-46136", "severity": "high"},
        ]
        licenses = [{"package": "requests", "license": "Apache-2.0", "compatible": True},
                    {"package": "flask", "license": "BSD-3-Clause", "compatible": True},
                    {"package": "gpl-lib", "license": "GPL-2.0", "compatible": False,
                     "warning": "GPL-2.0 may impose copyleft requirements"}]
        return {"direct_dependencies": direct, "transitive_dependencies": transitive,
                "outdated_packages": outdated, "vulnerable_packages": vulnerable,
                "license_analysis": licenses, "total_direct": len(direct),
                "outdated_count": len(outdated), "vulnerable_count": len(vulnerable)}

    def compute_dependency_score(self, analysis: Dict[str, Any]) -> float:
        total = analysis.get("total_direct", 1) or 1
        fresh = max(0, 100 - (analysis.get("outdated_count", 0) / total * 100))
        sec = max(0, 100 - (analysis.get("vulnerable_count", 0) / total * 200))
        return round(fresh * 0.6 + sec * 0.4, 1)


# ── Code Generation Engine ───────────────────────────────────────────

class CodeGenerationEngine:
    def __init__(self): self._count: int = 0

    def generate_class(self, class_name: str, attributes: List[str], methods: List[str],
                       base_class: str = "", include_repr: bool = True) -> str:
        self._count += 1
        inh = f"({base_class})" if base_class else ""
        lines = [f"class {class_name}{inh}:", f'    """Auto-generated {class_name} class."""', ""]
        params = ", ".join(f"{a}: Any = None" for a in attributes) if attributes else ""
        lines.append(f"    def __init__(self{params}):")
        for a in attributes: lines.append(f"        self.{a} = {a}")
        if not attributes: lines.append("        pass")
        lines.append("")
        for m in methods:
            lines.extend([f"    def {m}(self) -> None:", f'        """TODO: Implement {m}."""',
                          "        raise NotImplementedError", ""])
        if include_repr:
            attrs = ", ".join(f"{a}={{self.{a}!r}}" for a in attributes) if attributes else ""
            lines.extend([f"    def __repr__(self) -> str:", f'        return f"{class_name}({attrs})"', ""])
        return "\n".join(lines)

    def generate_api_endpoint(self, method: str, path: str, handler_name: str,
                              request_model: str = "", auth_required: bool = False) -> str:
        self._count += 1
        lines = [f'@app.{method.lower()}("{path}")']
        if auth_required: lines.append("    # Requires authentication middleware")
        params = [f"body: {request_model}"] if request_model else ["request: Request"]
        lines.extend([f"async def {handler_name}({', '.join(params)}) -> Dict[str, Any]:",
                      f'    """Handle {method.upper()} {path}."""',
                      "    # TODO: Implement handler logic", '    return {"status": "success"}', ""])
        return "\n".join(lines)

    def generate_unit_test(self, class_name: str, test_cases: List[Dict[str, str]],
                           framework: TestFramework = TestFramework.PYTEST) -> str:
        self._count += 1
        lines = ["import pytest", f"from {class_name.lower()} import {class_name}", "", "",
                 f"class Test{class_name}:", f'    """Tests for {class_name}."""', "",
                 "    def setup_method(self):", '        """Set up test fixtures."""',
                 f"        self.instance = {class_name}()", ""]
        for tc in test_cases:
            lines.extend([f"    def test_{tc.get('name', 'unnamed')}(self):",
                          f"        result = {tc.get('call', 'self.instance.method()')}",
                          f"        assert {tc.get('assertion', 'result is not None')}", ""])
        return "\n".join(lines)

    def generate_documentation(self, source_code: str) -> str:
        self._count += 1
        doc = ["# Auto-generated Documentation", ""]
        for match in re.finditer(r'^class\s+(\w+)', source_code, re.MULTILINE):
            doc.extend([f"### `{match.group(1)}`", "", "*No description provided.*", ""])
        for match in re.finditer(r'^def\s+(\w+)\s*\(([^)]*)\)', source_code, re.MULTILINE):
            doc.extend([f"### `{match.group(1)}({match.group(2)})`", "",
                        "*No description provided.*", ""])
        return "\n".join(doc)

    def _extract_classes(self, source_code: str) -> List[Dict[str, Any]]:
        classes: List[Dict[str, Any]] = []
        for line in source_code.split("\n"):
            if line.strip().startswith("class "):
                name = line.split("class ")[1].split(":")[0].split("(")[0].strip()
                classes.append({"name": name, "docstring": "", "methods": []})
        return classes

    def _extract_functions(self, source_code: str) -> List[Dict[str, Any]]:
        functions: List[Dict[str, Any]] = []
        for m in re.finditer(r'^def\s+(\w+)\s*\(([^)]*)\)', source_code, re.MULTILINE):
            args = [a.strip().split(":")[0].strip() for a in m.group(2).split(",")
                    if a.strip() and a.strip() != "self"]
            functions.append({"name": m.group(1), "args": args})
        return functions

# ── Architecture Patterns ────────────────────────────────────────────

class ArchitecturePatterns:
    PATTERN_DESCRIPTIONS: Dict[ArchitecturePattern, Dict[str, str]] = {
        ArchitecturePattern.MVC: {"name": "Model-View-Controller",
            "description": "Separates application into three interconnected components",
            "pros": "Clear separation of concerns, testable", "best_for": "Web applications"},
        ArchitecturePattern.MICROSERVICES: {"name": "Microservices Architecture",
            "description": "Application composed of small, independent services",
            "pros": "Scalable, independent deployment", "best_for": "Large-scale distributed systems"},
        ArchitecturePattern.EVENT_DRIVEN: {"name": "Event-Driven Architecture",
            "description": "Components communicate via events",
            "pros": "Loose coupling, scalable", "best_for": "Real-time systems, IoT"},
        ArchitecturePattern.CLEAN_ARCHITECTURE: {"name": "Clean Architecture",
            "description": "Concentric layers with dependency rule",
            "pros": "Testable, framework-independent", "best_for": "Enterprise applications"},
        ArchitecturePattern.HEXAGONAL: {"name": "Hexagonal (Ports and Adapters)",
            "description": "Application core with ports and adapters",
            "pros": "Flexible infrastructure, clear boundaries", "best_for": "Multi-interface apps"},
    }

    def analyze_pattern_fit(self, project_type: str, team_size: int, scale_requirements: str) -> List[Dict[str, Any]]:
        recs: List[Dict[str, Any]] = []
        if project_type == "web" and team_size < 5:
            recs.append({"pattern": ArchitecturePattern.MVC, "fit_score": 0.9,
                         "reason": "Small team; MVC provides clear structure without overhead"})
        if project_type == "web" and team_size >= 10:
            recs.append({"pattern": ArchitecturePattern.MICROSERVICES, "fit_score": 0.8,
                         "reason": "Large team; microservices enable independent development"})
        if scale_requirements == "high":
            recs.append({"pattern": ArchitecturePattern.MICROSERVICES, "fit_score": 0.9,
                         "reason": "High scale requirements suit horizontal scaling"})
        if project_type == "enterprise":
            recs.append({"pattern": ArchitecturePattern.CLEAN_ARCHITECTURE, "fit_score": 0.85,
                         "reason": "Clean architecture enforces boundaries for long-lived apps"})
        recs.sort(key=lambda r: r["fit_score"], reverse=True)
        return recs

    def evaluate_codebase_pattern(self, source_code: str) -> Dict[str, Any]:
        indicators: Dict[str, float] = defaultdict(float)
        if re.search(r'class\s+\w*Controller\b', source_code): indicators["mvc"] += 0.3
        if re.search(r'class\s+\w*Model\b', source_code): indicators["mvc"] += 0.2
        if re.search(r'class\s+\w*View\b', source_code): indicators["mvc"] += 0.2
        if re.search(r'class\s+\w*ViewModel\b', source_code): indicators["mvvm"] += 0.4
        if re.search(r'class\s+\w*Service\b', source_code): indicators["layered"] += 0.2
        if re.search(r'class\s+\w*Repository\b', source_code): indicators["repository"] += 0.3
        if re.search(r'(Event|Signal|publish|subscribe|emit)', source_code): indicators["event_driven"] += 0.3
        if not indicators: indicators["unknown"] = 1.0
        best = max(indicators, key=indicators.get)
        return {"detected_pattern": best, "confidence": round(indicators[best], 2),
                "all_indicators": dict(indicators)}

# ── Testing Strategies ───────────────────────────────────────────────

class TestingStrategies:
    def __init__(self): self.test_results: List[TestResult] = []

    def generate_test_plan(self, source_code: str, file_path: str = "") -> Dict[str, Any]:
        classes = re.findall(r'class\s+(\w+)', source_code)
        functions = [f for f in re.findall(r'def\s+(\w+)\s*\(', source_code) if not f.startswith("_")]
        test_cases: List[Dict[str, Any]] = []
        for fn in functions:
            test_cases.append({"function": fn, "test_type": TestType.UNIT.value,
                "cases": [{"name": f"test_{fn}_happy_path", "description": "Normal input"},
                          {"name": f"test_{fn}_edge_case", "description": "Boundary conditions"},
                          {"name": f"test_{fn}_error", "description": "Invalid input handling"}]})
        for cls in classes:
            test_cases.append({"class": cls, "test_type": TestType.UNIT.value,
                "cases": [{"name": f"test_{cls}_init", "description": "Object creation"},
                          {"name": f"test_{cls}_methods", "description": "Public methods"}]})
        return {"file": file_path, "test_framework": TestFramework.PYTEST.value,
                "total_test_cases": sum(len(tc.get("cases", [])) for tc in test_cases),
                "test_cases": test_cases, "coverage_target": 80.0}

    def calculate_test_coverage(self, tested_lines: Set[int], total_lines: int) -> float:
        return round((len(tested_lines) / max(total_lines, 1)) * 100, 2)

    def assess_test_quality(self, test_code: str) -> Dict[str, Any]:
        assertions = len(re.findall(r'(assert|assertEqual|assertTrue|assertFalse|pytest\.raises)', test_code))
        test_fns = len(re.findall(r'def test_', test_code))
        setups = len(re.findall(r'(setUp|setup_method|fixture)', test_code))
        mocking = len(re.findall(r'(mock|patch|MagicMock)', test_code))
        score = min(100, (assertions / max(test_fns, 1)) * 30 + min(setups * 10, 30) + min(mocking * 5, 20) + (20 if test_fns > 0 else 0))
        recs = []
        if assertions < test_fns: recs.append("Add more assertions per test")
        if mocking == 0 and test_fns > 3: recs.append("Consider using mocks")
        if setups == 0 and test_fns > 2: recs.append("Use setup fixtures")
        return {"test_functions": test_fns, "assertions": assertions, "quality_score": round(score, 1), "recommendations": recs}

# ── Code Quality Manager ─────────────────────────────────────────────

class CodeQualityManager:
    QUALITY_STANDARDS: Dict[str, Dict[str, Any]] = {
        "max_function_length": {"value": 30, "unit": "lines"},
        "max_class_length": {"value": 300, "unit": "lines"},
        "max_complexity": {"value": 10, "unit": " McCabe"},
        "min_test_coverage": {"value": 80, "unit": "%"},
        "max_line_length": {"value": 120, "unit": "chars"},
        "min_docstring_coverage": {"value": 70, "unit": "%"},
        "max_nesting_depth": {"value": 4, "unit": "levels"},
        "max_params_per_function": {"value": 5, "unit": "params"},
        "min_maintainability_index": {"value": 60, "unit": "index"},
    }

    def __init__(self): self.standards = dict(self.QUALITY_STANDARDS)

    def evaluate_quality_gate(self, metrics: Dict[str, Any]) -> QualityGateResult:
        checks: List[Dict[str, Any]] = []
        all_passed = True
        for name, actual, threshold, compare in [
            ("Cyclomatic Complexity", metrics.get("avg_complexity", 0), self.standards["max_complexity"]["value"], "le"),
            ("Test Coverage", metrics.get("test_coverage", 0), self.standards["min_test_coverage"]["value"], "ge"),
            ("Maintainability Index", metrics.get("avg_maintainability", 100), self.standards["min_maintainability_index"]["value"], "ge"),
        ]:
            passed = actual <= threshold if compare == "le" else actual >= threshold
            checks.append({"name": name, "status": QualityGateStatus.PASSED.value if passed else QualityGateStatus.FAILED.value,
                           "actual": actual, "threshold": threshold})
            if not passed: all_passed = False
        crit = metrics.get("issues_by_severity", {}).get("critical", 0)
        high = metrics.get("issues_by_severity", {}).get("high", 0)
        passed = crit == 0 and high <= 5
        checks.append({"name": "Critical/High Issues", "status": QualityGateStatus.PASSED.value if passed else QualityGateStatus.FAILED.value,
                        "actual": f"{crit} critical, {high} high", "threshold": "0 critical, ≤5 high"})
        if not passed: all_passed = False
        return QualityGateResult(gate_name="main_quality_gate",
            status=QualityGateStatus.PASSED if all_passed else QualityGateStatus.FAILED,
            checks=checks, summary="All checks passed" if all_passed else "One or more checks failed")

    def calculate_technical_debt(self, issues: List[CodeIssue]) -> Dict[str, Any]:
        effort = {IssueSeverity.CRITICAL: 4.0, IssueSeverity.HIGH: 2.0, IssueSeverity.MEDIUM: 0.5,
                  IssueSeverity.LOW: 0.25, IssueSeverity.INFO: 0.1}
        total = sum(effort.get(i.severity, 0.25) for i in issues)
        by_type: Dict[str, float] = defaultdict(float)
        for i in issues: by_type[i.issue_type.value] += effort.get(i.severity, 0.25)
        return {"total_hours": round(total, 2), "by_type": {k: round(v, 2) for k, v in by_type.items()},
                "issue_count": len(issues), "avg_effort_per_issue": round(total / max(len(issues), 1), 2)}

# ── Documentation Generator ──────────────────────────────────────────

class DocumentationGenerator:
    def __init__(self): self._count: int = 0

    def generate_api_docs(self, source_code: str, title: str = "API Reference") -> str:
        self._count += 1
        lines = [f"# {title}", "", "---", ""]
        for m in re.finditer(r'class\s+(\w+)(?:\(([^)]*)\))?:', source_code):
            inh = f" inherits from `{m.group(2)}`" if m.group(2) else ""
            lines.extend([f"### `{m.group(1)}`{inh}", ""])
            class_body = re.search(rf'class\s+{m.group(1)}.*?(?=\nclass\s|\Z)', source_code, re.DOTALL)
            if class_body:
                methods = re.findall(r'def\s+(\w+)\s*\(', class_body.group())
                if [x for x in methods if x != "__init__"]:
                    lines.append("**Methods:**")
                    for m2 in methods:
                        if m2 != "__init__": lines.append(f"- `{m2}()`")
                    lines.append("")
        for m in re.finditer(r'^def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(\w+))?', source_code, re.MULTILINE):
            ret = f" -> `{m.group(3)}`" if m.group(3) else ""
            lines.extend([f"### `{m.group(1)}({m.group(2)})`{ret}", "",
                          "*No description available.*", ""])
        return "\n".join(lines)

    def generate_changelog(self, changes: List[Dict[str, str]], version: str = "1.0.0") -> str:
        lines = [f"## [{version}] - {datetime.utcnow().strftime('%Y-%m-%d')}", ""]
        for c in changes: lines.append(f"- **{c.get('category', 'misc')}**: {c.get('description', '')}")
        return "\n".join(lines)

    def generate_readme_template(self, project_name: str, description: str) -> str:
        slug = project_name.lower().replace(" ", "-")
        return textwrap.dedent(f"""\
            # {project_name}

            {description}

            ## Installation

            ```bash
            pip install {slug}
            ```

            ## Usage

            ```python
            import {slug.replace("-", "_")}
            ```

            ## License

            MIT License. See LICENSE for details.
        """)

    def generate_type_stubs(self, source_code: str) -> str:
        stubs: List[str] = []
        for m in re.finditer(r'class\s+(\w+)(?:\(([^)]*)\))?:', source_code):
            inh = f"({m.group(2)})" if m.group(2) else ""
            stubs.extend([f"class {m.group(1)}{inh}:", "    ...", ""])
        for m in re.finditer(r'^def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(.+?))?\s*:', source_code, re.MULTILINE):
            ret = f" -> {m.group(3).strip()}" if m.group(3) else ""
            stubs.append(f"def {m.group(1)}({m.group(2)}){ret}: ...")
        return "\n".join(stubs)

# ── CI/CD Pipeline ───────────────────────────────────────────────────

class CICDPipeline:
    DEFAULT_STAGES: List[Dict[str, Any]] = [
        {"stage": CICDStage.LINT, "name": "Lint & Format", "timeout": 5},
        {"stage": CICDStage.BUILD, "name": "Build", "timeout": 15},
        {"stage": CICDStage.TEST, "name": "Unit Tests", "timeout": 20},
        {"stage": CICDStage.SECURITY_SCAN, "name": "Security Scan", "timeout": 10},
        {"stage": CICDStage.DEPLOY_STAGING, "name": "Deploy to Staging", "timeout": 15},
        {"stage": CICDStage.INTEGRATION_TEST, "name": "Integration Tests", "timeout": 30},
        {"stage": CICDStage.DEPLOY_PRODUCTION, "name": "Deploy to Production", "timeout": 20},
        {"stage": CICDStage.MONITOR, "name": "Post-deploy Monitoring", "timeout": 10},
    ]

    def __init__(self): self.pipelines: Dict[str, PipelineConfig] = {}; self.history: List[Dict[str, Any]] = []

    def create_pipeline(self, config: PipelineConfig) -> PipelineConfig:
        self.pipelines[config.pipeline_id] = config
        logger.info("Created pipeline: %s (%s)", config.name, config.pipeline_id)
        return config

    def generate_pipeline_config(self, project_type: str, framework: str) -> PipelineConfig:
        pid = f"pipeline-{project_type}-{int(time.time())}"
        env = {"PYTHON_VERSION": "3.11", "POETRY_VERSION": "1.7.0"} if project_type == "python" else {"NODE_VERSION": "20"}
        config = PipelineConfig(pipeline_id=pid, name=f"{project_type.title()} CI/CD Pipeline",
            stages=[s["stage"] for s in self.DEFAULT_STAGES], triggers=["push", "pull_request"],
            environment_variables=env, timeout_minutes=120, parallel=False)
        return self.create_pipeline(config)

    def simulate_pipeline_run(self, pipeline_id: str) -> Dict[str, Any]:
        if pipeline_id not in self.pipelines: raise ValueError(f"Pipeline not found: {pipeline_id}")
        config = self.pipelines[pipeline_id]
        stages = [{"stage": s["stage"].value, "name": s["name"], "status": "success",
                   "duration_seconds": round(s["timeout"] * 0.7, 1), "timestamp": datetime.utcnow().isoformat()}
                  for s in self.DEFAULT_STAGES if s["stage"] in config.stages]
        run = {"pipeline_id": pipeline_id, "run_id": f"run-{int(time.time())}",
               "stages": stages, "overall_status": "success",
               "total_duration": sum(s["duration_seconds"] for s in stages)}
        self.history.append(run)
        return run

    def generate_github_actions_config(self, config: PipelineConfig) -> str:
        lines = [f"name: {config.name}", "", "on:"]
        for t in config.triggers:
            lines.append(f"  {t}:")
            if t == "push": lines.append("    branches: [main, develop]")
            elif t == "pull_request": lines.append("    branches: [main]")
        lines.extend(["", "jobs:"])
        for stage in config.stages:
            sn = stage.value.replace("_", "-")
            lines.extend([f"  {sn}:", "    runs-on: ubuntu-latest",
                          f"    timeout-minutes: {config.timeout_minutes // len(config.stages)}",
                          "    steps:", "      - uses: actions/checkout@v4",
                          f"      - name: Run {stage.value.replace('_', ' ').title()}",
                          f"        run: echo 'Running {stage.value}'", ""])
        return "\n".join(lines)

# ── Security Scanner ─────────────────────────────────────────────────

class SecurityScanner:
    VULNERABILITY_PATTERNS: List[Dict[str, Any]] = [
        {"pattern": r'f["\'].*\{.*\}.*(?:SELECT|INSERT|UPDATE|DELETE)',
         "category": SecurityVulnCategory.INJECTION, "cwe": "CWE-89",
         "title": "SQL Injection via f-string", "severity": IssueSeverity.CRITICAL,
         "description": "User input in f-strings used in SQL queries", "remediation": "Use parameterized queries"},
        {"pattern": r'innerHTML\s*=|document\.write\(',
         "category": SecurityVulnCategory.XSS, "cwe": "CWE-79",
         "title": "Potential XSS via innerHTML", "severity": IssueSeverity.HIGH,
         "description": "Direct DOM manipulation without sanitization", "remediation": "Use textContent or sanitize"},
        {"pattern": r'os\.path\.join\s*\(.*request\.',
         "category": SecurityVulnCategory.PATH_TRAVERSAL, "cwe": "CWE-22",
         "title": "Path Traversal Risk", "severity": IssueSeverity.HIGH,
         "description": "User-controlled input in file path", "remediation": "Validate and sanitize file paths"},
        {"pattern": r'requests\.(get|post|put|delete)\s*\([^)]*verify\s*=\s*False',
         "category": SecurityVulnCategory.SECURITY_MISCONFIG, "cwe": "CWE-295",
         "title": "SSL Verification Disabled", "severity": IssueSeverity.HIGH,
         "description": "TLS verification disabled", "remediation": "Enable SSL verification (verify=True)"},
        {"pattern": r'yaml\.load\s*\([^)]*Loader\s*=\s*yaml\.UnsafeLoader',
         "category": SecurityVulnCategory.INSECURE_DESER, "cwe": "CWE-502",
         "title": "Insecure YAML Deserialization", "severity": IssueSeverity.HIGH,
         "description": "Loading YAML with unsafe loader", "remediation": "Use yaml.safe_load()"},
        {"pattern": r'allow_origins\s*=\s*\["?\*"?\]',
         "category": SecurityVulnCategory.SECURITY_MISCONFIG, "cwe": "CWE-942",
         "title": "Overly Permissive CORS", "severity": IssueSeverity.MEDIUM,
         "description": "CORS allows all origins", "remediation": "Restrict allowed origins"},
        {"pattern": r'random\.(random|randint|choice|sample)\s*\(',
         "category": SecurityVulnCategory.SECURITY_MISCONFIG, "cwe": "CWE-330",
         "title": "Weak Random Number Generator", "severity": IssueSeverity.MEDIUM,
         "description": "Non-cryptographic RNG for security", "remediation": "Use secrets module"},
    ]

    def __init__(self): self.vulnerabilities: List[SecurityVulnerability] = []; self._counter: int = 0

    def scan_source(self, source_code: str, file_path: str = "") -> List[SecurityVulnerability]:
        vulns: List[SecurityVulnerability] = []
        for vdef in self.VULNERABILITY_PATTERNS:
            for idx, line in enumerate(source_code.split("\n"), 1):
                if re.search(vdef["pattern"], line, re.IGNORECASE):
                    self._counter += 1
                    vulns.append(SecurityVulnerability(
                        vuln_id=f"SEC-{self._counter:05d}", file_path=file_path,
                        line_number=idx, category=vdef["category"], severity=vdef["severity"],
                        title=vdef["title"], description=vdef["description"],
                        cwe_id=vdef["cwe"], remediation=vdef["remediation"]))
        self.vulnerabilities.extend(vulns)
        return vulns

    def calculate_risk_score(self, vulns: List[SecurityVulnerability]) -> Dict[str, Any]:
        weights = {IssueSeverity.CRITICAL: 10.0, IssueSeverity.HIGH: 7.5, IssueSeverity.MEDIUM: 5.0,
                   IssueSeverity.LOW: 2.5, IssueSeverity.INFO: 1.0}
        total = sum(weights.get(v.severity, 1.0) for v in vulns)
        levels = [(50, "CRITICAL"), (30, "HIGH"), (15, "MEDIUM"), (5, "LOW")]
        level = next((l for t, l in levels if total >= t), "INFO")
        return {"total_vulnerabilities": len(vulns), "total_risk_score": round(total, 1),
                "risk_level": level, "by_category": dict(Counter(v.category.value for v in vulns)),
                "by_severity": dict(Counter(v.severity.name for v in vulns))}

# ── Performance Optimizer ────────────────────────────────────────────

class PerformanceOptimizer:
    def __init__(self): self.metrics: List[PerformanceMetric] = []

    def analyze_performance(self, source_code: str, file_path: str = "") -> Dict[str, Any]:
        issues: List[Dict[str, Any]] = []
        lines = source_code.split("\n")
        for_depth = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("for ") or stripped.startswith("while "):
                for_depth += 1
                if for_depth >= 3:
                    issues.append({"line": i + 1, "type": "nested_loops", "severity": "high",
                                   "message": f"Triple-nested loop at line {i + 1}; O(n^3) complexity",
                                   "suggestion": "Restructure algorithm or use lookup data structures"})
            elif stripped and not stripped.startswith("#") and not line.startswith(" ") and not line.startswith("\t"):
                for_depth = 0
        if re.search(r'for\s+.*:\s*\n\s+.*\+=\s*["\']', source_code):
            issues.append({"line": 0, "type": "string_concat_loop", "severity": "medium",
                           "message": "String concatenation in loop detected",
                           "suggestion": "Use ''.join() or io.StringIO"})
        for call, count in Counter(re.findall(r'(\w+\([^)]*\))', source_code)).items():
            if count >= 3 and "(" in call:
                issues.append({"line": 0, "type": "repeated_computation", "severity": "low",
                               "message": f"Function call '{call}' repeated {count} times",
                               "suggestion": "Cache the result in a local variable"})
        if re.search(r'for\s+\w+\s+in\s+range\(len\(', source_code):
            issues.append({"line": 0, "type": "range_len_pattern", "severity": "low",
                           "message": "Using range(len()) instead of enumerate()",
                           "suggestion": "Use enumerate() for cleaner iteration"})
        append_count = len(re.findall(r'\.append\(', source_code))
        if append_count > 2:
            issues.append({"line": 0, "type": "append_in_loop", "severity": "low",
                           "message": "Multiple .append() calls could use list comprehensions",
                           "suggestion": "Consider list comprehensions or generator expressions"})
        score = sum({"high": 3, "medium": 2, "low": 1}.get(i.get("severity", "low"), 1) for i in issues)
        potential = "high" if score >= 9 else "medium" if score >= 4 else "low"
        return {"file": file_path, "performance_issues": issues, "issue_count": len(issues),
                "optimization_potential": potential}

    def profile_function(self, func_name: str, call_count: int, total_time_ms: float) -> PerformanceMetric:
        avg = total_time_ms / max(call_count, 1)
        m = PerformanceMetric(metric_name=f"{func_name}_avg_time", value=avg,
            unit="ms", threshold=10.0, context=f"{call_count} calls, total {total_time_ms:.1f}ms")
        self.metrics.append(m)
        return m


# ── Code Review Assistant ────────────────────────────────────────────

class CodeReviewAssistant:
    def __init__(self): self.comments: List[CodeReviewComment] = []; self._counter: int = 0

    def review_diff(self, diff_content: str, file_path: str = "") -> List[CodeReviewComment]:
        comments: List[CodeReviewComment] = []
        current_line = 0
        for line in diff_content.split("\n"):
            if line.startswith("@@"):
                m = re.search(r'\+(\d+)', line)
                if m: current_line = int(m.group(1))
                continue
            if line.startswith("+") and not line.startswith("+++"):
                current_line += 1
                content = line[1:].strip()
                if "TODO" in content or "FIXME" in content:
                    comments.append(self._comment(file_path, current_line,
                        "TODO/FIXME should be addressed before merging or tracked.", "maintenance", IssueSeverity.INFO))
                if re.search(r'password\s*=\s*["\']', content, re.IGNORECASE):
                    comments.append(self._comment(file_path, current_line,
                        "Hardcoded password. Use environment variables.", "security", IssueSeverity.CRITICAL))
                if "except:" in content or "except Exception:" in content:
                    comments.append(self._comment(file_path, current_line,
                        "Bare/broad exception. Catch specific exceptions.", "quality", IssueSeverity.MEDIUM))
                if "print(" in content:
                    comments.append(self._comment(file_path, current_line,
                        "Debug print. Replace with logging.", "quality", IssueSeverity.LOW))
                if len(content) > 120:
                    comments.append(self._comment(file_path, current_line,
                        f"Line exceeds 120 chars ({len(content)}).", "style", IssueSeverity.INFO))
                if "eval(" in content or "exec(" in content:
                    comments.append(self._comment(file_path, current_line,
                        "Dynamic code execution. Security risk.", "security", IssueSeverity.HIGH))
        self.comments.extend(comments)
        return comments

    def _comment(self, fp: str, ln: int, content: str, cat: str, sev: IssueSeverity) -> CodeReviewComment:
        self._counter += 1
        return CodeReviewComment(comment_id=f"CR-{self._counter:05d}", file_path=fp,
            line_number=ln, author="CodeReviewAssistant", content=content, category=cat, severity=sev)

    def generate_review_summary(self, comments: List[CodeReviewComment]) -> Dict[str, Any]:
        unresolved = [c for c in comments if not c.is_resolved]
        return {"total_comments": len(comments), "unresolved_comments": len(unresolved),
                "by_severity": dict(Counter(c.severity.name for c in comments)),
                "by_category": dict(Counter(c.category for c in comments)),
                "approval_recommendation": "approve" if not unresolved else "request_changes"}

# ── Development Dashboard ────────────────────────────────────────────

class DevelopmentDashboard:
    def __init__(self):
        self.static_analysis = StaticAnalysisEngine()
        self.refactoring = CodeRefactoringEngine()
        self.dependencies = DependencyAnalyzer()
        self.code_gen = CodeGenerationEngine()
        self.architecture = ArchitecturePatterns()
        self.testing = TestingStrategies()
        self.quality = CodeQualityManager()
        self.documentation = DocumentationGenerator()
        self.cicd = CICDPipeline()
        self.security = SecurityScanner()
        self.performance = PerformanceOptimizer()
        self.review = CodeReviewAssistant()

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        logger.info("Starting project analysis: %s", project_path)
        metrics = {"avg_complexity": 5.2, "avg_maintainability": 72.0, "test_coverage": 85.0,
                   "issues_by_severity": {"critical": 2, "high": 5, "medium": 10, "low": 8}}
        quality_gate = self.quality.evaluate_quality_gate(metrics)
        debt = self.quality.calculate_technical_debt(self.static_analysis.issues)
        return {"summary": {"total_files": 50, "total_lines": 10000,
                "languages": {"python": 7000, "javascript": 3000},
                "complexity_score": metrics["avg_complexity"],
                "maintainability_score": metrics["avg_maintainability"]},
                "quality_gate": {"status": quality_gate.status.value, "checks": quality_gate.checks},
                "technical_debt": debt,
                "dependency_analysis": self.dependencies.analyze_dependencies(),
                "timestamp": datetime.utcnow().isoformat()}

    def analyze_code(self, source_code: str, file_path: str = "analyzed.py") -> Dict[str, Any]:
        logger.info("Analyzing code: %s (%d bytes)", file_path, len(source_code))
        return {"file": file_path,
                "static_analysis": self.static_analysis.analyze(source_code, file_path),
                "refactoring": self.refactoring.analyze(source_code, file_path),
                "security": [v.to_dict() for v in self.security.scan_source(source_code, file_path)],
                "performance": self.performance.analyze_performance(source_code, file_path),
                "test_plan": self.testing.generate_test_plan(source_code, file_path),
                "documentation": self.documentation.generate_api_docs(source_code, file_path),
                "timestamp": datetime.utcnow().isoformat()}

    def generate_code(self, request_type: str, parameters: Dict[str, Any]) -> str:
        if request_type == "class":
            return self.code_gen.generate_class(parameters.get("name", "NewClass"),
                parameters.get("attributes", []), parameters.get("methods", []),
                parameters.get("base_class", ""))
        elif request_type == "api":
            return self.code_gen.generate_api_endpoint(parameters.get("method", "GET"),
                parameters.get("path", "/endpoint"), parameters.get("handler", "handle_request"),
                parameters.get("request_model", ""), parameters.get("auth_required", False))
        elif request_type == "test":
            return self.code_gen.generate_unit_test(parameters.get("class_name", "TestClass"),
                parameters.get("test_cases", []))
        elif request_type == "docs":
            return self.documentation.generate_api_docs(parameters.get("source_code", ""),
                parameters.get("title", "API Reference"))
        elif request_type == "readme":
            return self.documentation.generate_readme_template(
                parameters.get("project_name", "MyProject"), parameters.get("description", "A new project"))
        elif request_type == "pipeline":
            config = self.cicd.generate_pipeline_config(
                parameters.get("project_type", "python"), parameters.get("framework", "fastapi"))
            return self.cicd.generate_github_actions_config(config)
        elif request_type == "changelog":
            return self.documentation.generate_changelog(
                parameters.get("changes", []), parameters.get("version", "1.0.0"))
        return ""

# ── Main ──────────────────────────────────────────────────────────────

def main() -> None:
    print("\n" + "=" * 70)
    print("  Development Agent — Comprehensive Software Development Analysis")
    print("=" * 70 + "\n")
    dashboard = DevelopmentDashboard()
    project_results = dashboard.analyze_project("/path/to/project")
    print("Project Analysis Summary:")
    print(f"  Total files:        {project_results['summary']['total_files']}")
    print(f"  Total lines:        {project_results['summary']['total_lines']}")
    print(f"  Quality gate:       {project_results['quality_gate']['status']}")
    print(f"  Technical debt:     {project_results['technical_debt']['total_hours']} hours\n")

    sample_code = '''
import os, hashlib
password = "supersecret123"
api_key = "sk-abcdef1234567890"

def calculate_fibonacci(n):
    if n <= 0: return []
    elif n == 1: return [0]
    elif n == 2: return [0, 1]
    fib = [0, 1]
    for i in range(2, n): fib.append(fib[i-1] + fib[i-2])
    return fib

def process_data(data, x, y, z, flag, mode, extra):
    temp = x + y
    result = eval(data)
    print(f"Result: {result}")
    return result

class UserManager:
    def __init__(self): self.users = []
    def create_user(self, name): self.users.append(name); return name
    def get_user(self, index): return self.users[index]
'''
    print("Code Analysis:")
    code_results = dashboard.analyze_code(sample_code, "sample.py")
    print(f"  Issues found:       {code_results['static_analysis']['issue_count']}")
    print(f"  Complexity:         {code_results['static_analysis']['complexity']}")
    print(f"  Maintainability:    {code_results['static_analysis']['maintainability_index']}")
    print(f"  Security vulns:     {len(code_results['security'])}")
    print(f"  Performance issues: {code_results['performance']['issue_count']}")
    print(f"  Refactoring ideas:  {code_results['refactoring']['total_suggestions']}\n")

    class_code = dashboard.generate_code("class", {
        "name": "UserManager", "attributes": ["user_id", "username", "email"],
        "methods": ["create_user", "delete_user", "get_user"]})
    print("Generated Class:")
    print(class_code)

    print("Security Scan Results:")
    for v in code_results["security"]:
        print(f"  [{v['severity']}] {v['title']} at line {v['line']}")
    print(f"\nTest Plan: {code_results['test_plan']['total_test_cases']} test cases planned\n")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
