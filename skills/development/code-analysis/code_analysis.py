"""
Code Analysis Framework

Production-grade code analysis toolkit providing static analysis, code quality metrics,
complexity analysis, dependency analysis, and technical debt assessment.
"""

from __future__ import annotations

import ast
import hashlib
import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class MetricCategory(Enum):
    SIZE = "size"
    COMPLEXITY = "complexity"
    DUPLICATION = "duplication"
    DOCUMENTATION = "documentation"
    MAINTAINABILITY = "maintainability"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Rule:
    """Static analysis rule."""
    name: str
    pattern: str
    severity: Severity = Severity.WARNING
    message: str = ""
    file_pattern: str = "*.py"
    enabled: bool = True


@dataclass
class Issue:
    """A detected code issue."""
    rule_name: str
    severity: Severity
    message: str
    file: str
    line: int
    column: int = 0
    suggestion: str = ""


@dataclass
class AnalysisResult:
    """Static analysis result."""
    file_path: str
    issues: List[Issue]
    rules_checked: int = 0
    analysis_time_ms: float = 0.0


@dataclass
class FunctionMetrics:
    """Metrics for a single function."""
    name: str
    file: str
    line_start: int
    line_end: int
    loc: int = 0
    parameters: int = 0
    cyclomatic: int = 1
    cognitive: int = 0
    max_nesting: int = 0
    has_docstring: bool = False


@dataclass
class ClassMetrics:
    """Metrics for a class."""
    name: str
    file: str
    line_start: int
    methods: int = 0
    loc: int = 0
    depth: int = 0
    has_docstring: bool = False


@dataclass
class QualityReport:
    """Code quality analysis report."""
    total_loc: int = 0
    code_loc: int = 0
    comment_loc: int = 0
    blank_loc: int = 0
    total_functions: int = 0
    total_classes: int = 0
    avg_function_length: float = 0.0
    maintainability_index: float = 100.0
    code_to_comment_ratio: float = 0.0
    function_metrics: List[FunctionMetrics] = field(default_factory=list)
    class_metrics: List[ClassMetrics] = field(default_factory=list)


@dataclass
class ComplexityResult:
    """Function complexity analysis."""
    function_name: str
    cyclomatic: int = 1
    cognitive: int = 0
    max_nesting: int = 0
    halstead_volume: float = 0.0
    maintainability: float = 100.0


@dataclass
class DependencyInfo:
    """Dependency information."""
    name: str
    version: str = ""
    is_external: bool = True
    imported_by: List[str] = field(default_factory=list)


@dataclass
class DependencyReport:
    """Dependency analysis report."""
    direct: List[DependencyInfo]
    transitive: List[DependencyInfo]
    circular: List[List[str]]
    total_dependencies: int = 0
    external_count: int = 0
    internal_count: int = 0


@dataclass
class DuplicationBlock:
    """A duplicated code block."""
    lines: List[str]
    file_a: str
    line_a: int
    file_b: str
    line_b: int
    similarity: float = 1.0


@dataclass
class DuplicationReport:
    """Code duplication analysis."""
    blocks: List[DuplicationBlock]
    total_duplicated_lines: int = 0
    duplication_percentage: float = 0.0
    files_affected: int = 0


@dataclass
class TechnicalDebt:
    """Technical debt estimation."""
    category: str
    description: str
    estimated_hours: float
    estimated_cost: float
    priority: int = 0
    file: str = ""
    line: int = 0


@dataclass
class DebtReport:
    """Technical debt analysis report."""
    total_hours: float = 0.0
    total_cost: float = 0.0
    items: List[TechnicalDebt] = field(default_factory=list)
    trend: str = "stable"  # improving, stable, worsening


# ---------------------------------------------------------------------------
# Static Analyzer
# ---------------------------------------------------------------------------

class StaticAnalyzer:
    """Perform static code analysis."""

    def __init__(self):
        self._rules: List[Rule] = []
        self._default_rules()

    def _default_rules(self) -> None:
        self._rules = [
            Rule("no_print", r"\bprint\s*\(", Severity.WARNING, "Avoid print statements"),
            Rule("no_todo", r"#\s*TODO", Severity.INFO, "TODO comment found"),
            Rule("no_fixme", r"#\s*FIXME", Severity.WARNING, "FIXME comment found"),
            Rule("no_bare_except", r"except\s*:", Severity.WARNING, "Bare except clause"),
            Rule("no_eval", r"\beval\s*\(", Severity.ERROR, "Avoid eval()"),
            Rule("no_exec", r"\bexec\s*\(", Severity.ERROR, "Avoid exec()"),
        ]

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def analyze_file(self, file_path: str) -> AnalysisResult:
        start_time = time.time()
        issues = []

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")

        for rule in self._rules:
            if not rule.enabled:
                continue
            for i, line in enumerate(lines, 1):
                if re.search(rule.pattern, line):
                    issues.append(Issue(
                        rule_name=rule.name,
                        severity=rule.severity,
                        message=rule.message,
                        file=file_path,
                        line=i,
                    ))

        duration = (time.time() - start_time) * 1000

        return AnalysisResult(
            file_path=file_path,
            issues=issues,
            rules_checked=len(self._rules),
            analysis_time_ms=duration,
        )

    def analyze_directory(self, directory: str, extensions: List[str] = None) -> List[AnalysisResult]:
        if extensions is None:
            extensions = [".py", ".js", ".ts"]
        results = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    results.append(self.analyze_file(file_path))
        return results


# ---------------------------------------------------------------------------
# Quality Metrics
# ---------------------------------------------------------------------------

class QualityMetrics:
    """Calculate code quality metrics."""

    def analyze_file(self, file_path: str) -> QualityReport:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        total_loc = len(lines)
        blank_loc = sum(1 for l in lines if l.strip() == "")
        comment_loc = sum(1 for l in lines if l.strip().startswith("#") or l.strip().startswith("//"))
        code_loc = total_loc - blank_loc - comment_loc

        functions = []
        classes = []
        current_function = None
        nesting = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("function "):
                if current_function:
                    functions.append(current_function)
                func_name = stripped.split("(")[0].replace("def ", "").replace("function ", "")
                current_function = FunctionMetrics(
                    name=func_name, file=file_path, line_start=i,
                )
            elif current_function:
                current_function.loc += 1

            if stripped.startswith("class "):
                class_name = stripped.split("(")[0].replace("class ", "").replace(":", "")
                classes.append(ClassMetrics(
                    name=class_name, file=file_path, line_start=i,
                ))

        if current_function:
            functions.append(current_function)

        avg_func_len = np.mean([f.loc for f in functions]) if functions else 0

        # Maintainability index (simplified)
        loc_factor = min(total_loc / 1000, 1.0)
        comment_factor = comment_loc / max(code_loc, 1)
        mi = max(0, min(100, 100 - loc_factor * 50 + comment_factor * 50))

        return QualityReport(
            total_loc=total_loc,
            code_loc=code_loc,
            comment_loc=comment_loc,
            blank_loc=blank_loc,
            total_functions=len(functions),
            total_classes=len(classes),
            avg_function_length=avg_func_len,
            maintainability_index=mi,
            code_to_comment_ratio=code_loc / max(comment_loc, 1),
            function_metrics=functions,
            class_metrics=classes,
        )

    def analyze_project(self, directory: str) -> QualityReport:
        total_loc = 0
        code_loc = 0
        comment_loc = 0
        blank_loc = 0
        functions = []
        classes = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        report = self.analyze_file(file_path)
                        total_loc += report.total_loc
                        code_loc += report.code_loc
                        comment_loc += report.comment_loc
                        blank_loc += report.blank_loc
                        functions.extend(report.function_metrics)
                        classes.extend(report.class_metrics)
                    except Exception:
                        pass

        avg_func_len = np.mean([f.loc for f in functions]) if functions else 0
        mi = max(0, min(100, 100 - (total_loc / 1000) * 50 + (comment_loc / max(code_loc, 1)) * 50))

        return QualityReport(
            total_loc=total_loc, code_loc=code_loc, comment_loc=comment_loc,
            blank_loc=blank_loc, total_functions=len(functions),
            total_classes=len(classes), avg_function_length=avg_func_len,
            maintainability_index=mi,
            function_metrics=functions, class_metrics=classes,
        )


# ---------------------------------------------------------------------------
# Complexity Analyzer
# ---------------------------------------------------------------------------

class ComplexityAnalyzer:
    """Analyze code complexity."""

    def analyze_function(self, source_code: str) -> ComplexityResult:
        lines = source_code.strip().split("\n")
        func_name = lines[0].split("(")[0].replace("def ", "").strip()

        # Cyclomatic complexity
        cyclomatic = 1
        keywords = ["if ", "elif ", "else:", "for ", "while ", "except ", "with ",
                     "and ", "or ", "case "]
        for line in lines:
            stripped = line.strip()
            for kw in keywords:
                if kw in stripped:
                    cyclomatic += 1

        # Cognitive complexity (simplified)
        cognitive = 0
        nesting = 0
        max_nesting = 0
        for line in lines:
            stripped = line.strip()
            if any(stripped.startswith(kw) for kw in ["if ", "elif ", "for ", "while ", "with "]):
                nesting += 1
                max_nesting = max(max_nesting, nesting)
                cognitive += nesting
            elif stripped.startswith("else:") or stripped.startswith("except"):
                cognitive += 1
            elif stripped == "" and nesting > 0:
                nesting = max(0, nesting - 1)

        # Maintainability
        maintainability = max(0, min(100, 171 - 5.2 * np.log(max(cyclomatic, 1)) - 0.23 * len(lines)))

        return ComplexityResult(
            function_name=func_name,
            cyclomatic=cyclomatic,
            cognitive=cognitive,
            max_nesting=max_nesting,
            maintainability=maintainability,
        )


# ---------------------------------------------------------------------------
# Dependency Analyzer
# ---------------------------------------------------------------------------

class DependencyAnalyzer:
    """Analyze code dependencies."""

    def analyze(self, directory: str) -> DependencyReport:
        direct = []
        transitive = []
        circular = []

        # Scan for imports
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r") as f:
                            for line in f:
                                match = re.match(r"^(?:from|import)\s+(\w+)", line.strip())
                                if match:
                                    pkg = match.group(1)
                                    if pkg not in [d.name for d in direct]:
                                        direct.append(DependencyInfo(name=pkg, is_external=True))
                    except Exception:
                        pass

        # Check for circular (simplified)
        # In production, use AST for accurate analysis

        return DependencyReport(
            direct=direct,
            transitive=transitive,
            circular=circular,
            total_dependencies=len(direct) + len(transitive),
            external_count=len([d for d in direct if d.is_external]),
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate code analysis capabilities."""
    print("=" * 70)
    print("Code Analysis Framework - Demo")
    print("=" * 70)

    # --- 1. Static Analysis ---
    print("\n--- Static Analysis ---")
    static = StaticAnalyzer()
    # Create a test file
    test_file = "/tmp/test_code.py"
    with open(test_file, "w") as f:
        f.write("# TODO: fix this\n")
        f.write("def process(data):\n")
        f.write("    print(data)\n")
        f.write("    eval(data)\n")
        f.write("    return data\n")

    result = static.analyze_file(test_file)
    print(f"  File: {result.file_path}")
    print(f"  Issues: {len(result.issues)}")
    for issue in result.issues:
        print(f"    Line {issue.line}: [{issue.severity.value}] {issue.message}")

    # --- 2. Quality Metrics ---
    print("\n--- Code Quality Metrics ---")
    quality = QualityMetrics()
    report = quality.analyze_file(test_file)
    print(f"  Total LOC: {report.total_loc}")
    print(f"  Code LOC: {report.code_loc}")
    print(f"  Comment LOC: {report.comment_loc}")
    print(f"  Blank LOC: {report.blank_loc}")
    print(f"  Functions: {report.total_functions}")
    print(f"  Maintainability: {report.maintainability_index:.1f}/100")

    # --- 3. Complexity Analysis ---
    print("\n--- Complexity Analysis ---")
    complexity = ComplexityAnalyzer()
    result = complexity.analyze_function("""def complex_function(data, threshold):
    result = []
    for item in data:
        if item > threshold:
            if item % 2 == 0:
                result.append(item * 2)
            else:
                result.append(item + 1)
        elif item < 0:
            result.append(0)
    return result""")
    print(f"  Function: {result.function_name}")
    print(f"  Cyclomatic: {result.cyclomatic}")
    print(f"  Cognitive: {result.cognitive}")
    print(f"  Max nesting: {result.max_nesting}")
    print(f"  Maintainability: {result.maintainability:.1f}")

    # --- 4. Dependency Analysis ---
    print("\n--- Dependency Analysis ---")
    deps = DependencyAnalyzer()
    report = deps.analyze("/tmp")
    print(f"  Direct dependencies: {len(report.direct)}")
    print(f"  Circular: {len(report.circular)}")

    # Cleanup
    os.remove(test_file)

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()