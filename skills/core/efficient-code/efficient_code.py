"""
Efficient Code Module
Complexity analysis, data structure selection, memory optimization, and code quality.
"""

from __future__ import annotations

import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ComplexityClass(Enum):
    O_1 = "O(1)"
    O_LOG_N = "O(log n)"
    O_N = "O(n)"
    O_N_LOG_N = "O(n log n)"
    O_N2 = "O(n^2)"
    O_N3 = "O(n^3)"
    O_2N = "O(2^n)"
    O_NF = "O(n!)"


class DataStructure(Enum):
    ARRAY = "array"
    LINKED_LIST = "linked_list"
    HASH_MAP = "hash_map"
    TREE = "binary_tree"
    HEAP = "heap"
    TRIE = "trie"
    GRAPH = "graph"
    DEQUE = "deque"
    SORTED_LIST = "sorted_list"


class TaskType(Enum):
    IO_BOUND = "io_bound"
    CPU_BOUND = "cpu_bound"
    MIXED = "mixed"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ComplexityAnalysis:
    """Code complexity analysis result."""
    time_complexity: str
    space_complexity: str
    estimated_operations: Dict[int, int] = field(default_factory=dict)
    bottlenecks: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class StructureRecommendation:
    """Data structure recommendation."""
    structure: str
    time_complexity: Dict[str, str] = field(default_factory=dict)
    reasoning: str = ""
    tradeoffs: List[str] = field(default_factory=list)
    implementation_notes: str = ""


@dataclass
class MemorySuggestion:
    """Memory optimization suggestion."""
    description: str
    impact: str = "medium"
    code_example: str = ""
    estimated_savings: str = ""


@dataclass
class ConcurrencyPattern:
    """Concurrency pattern recommendation."""
    name: str
    implementation: str
    use_case: str = ""
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    complexity: str = "medium"


@dataclass
class QualityIssue:
    """Code quality issue."""
    message: str
    severity: str = "info"
    line: int = 0
    suggestion: str = ""
    rule: str = ""


@dataclass
class BenchmarkResult:
    """Benchmark execution result."""
    function_name: str
    input_size: int
    execution_time_ms: float
    memory_usage_bytes: int = 0
    operations_per_second: float = 0.0


# ---------------------------------------------------------------------------
# Complexity Analyzer
# ---------------------------------------------------------------------------

class ComplexityAnalyzer:
    """Analyze code complexity."""

    PATTERNS = {
        ComplexityClass.O_N2: [r'for.*for', r'for.*in.*for'],
        ComplexityClass.O_N: [r'for.*in', r'while'],
        ComplexityClass.O_LOG_N: [r'while.*//', r'//=\s*2', r'bisect'],
        ComplexityClass.O_1: [r'dict\[', r'hash', r'\.get\('],
    }

    def analyze_function(
        self,
        code: str,
        input_sizes: Optional[List[int]] = None,
    ) -> ComplexityAnalysis:
        input_sizes = input_sizes or [100, 1000, 10000]
        time_complexity = "O(n)"
        space_complexity = "O(1)"
        bottlenecks: List[str] = []
        suggestions: List[str] = []

        nested_loops = len(re.findall(r'for\s+.*in\s+', code))
        if nested_loops >= 3:
            time_complexity = "O(n^3)"
            bottlenecks.append("Triple nested loop detected")
        elif nested_loops >= 2:
            time_complexity = "O(n^2)"
            bottlenecks.append("Nested loop detected")
        elif 'while' in code and '//' in code:
            time_complexity = "O(log n)"
        elif 'for' in code or 'while' in code:
            time_complexity = "O(n)"

        if 'append' in code or 'list(' in code:
            space_complexity = "O(n)"
        if 'dict' in code or '{}' in code:
            space_complexity = "O(n)"

        if time_complexity == "O(n^2)":
            suggestions.append("Consider using a hash map for O(1) lookups instead of nested iteration")
        if time_complexity == "O(n^3)":
            suggestions.append("Reduce nesting with dynamic programming or divide-and-conquer")

        estimated = {}
        for size in input_sizes:
            if 'n^2' in time_complexity:
                estimated[size] = size ** 2
            elif 'n^3' in time_complexity:
                estimated[size] = size ** 3
            elif 'log n' in time_complexity:
                import math
                estimated[size] = int(size * math.log2(size)) if size > 0 else 0
            else:
                estimated[size] = size

        return ComplexityAnalysis(
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            estimated_operations=estimated,
            bottlenecks=bottlenecks,
            suggestions=suggestions,
        )


# ---------------------------------------------------------------------------
# Data Structure Selector
# ---------------------------------------------------------------------------

class DataStructureSelector:
    """Recommend optimal data structures."""

    def recommend(
        self,
        operations: Optional[List[str]] = None,
        access_pattern: str = "random",
        size_estimate: int = 1000,
        ordering_required: bool = False,
    ) -> StructureRecommendation:
        operations = operations or ["lookup"]
        ops = set(operations)

        if "lookup" in ops and "insert" in ops and not ordering_required:
            return StructureRecommendation(
                structure="hash_map",
                time_complexity={"lookup": "O(1)", "insert": "O(1)", "delete": "O(1)"},
                reasoning="Hash map provides O(1) for all operations when ordering is not needed",
            )
        elif "peek" in ops or "min" in ops or "max" in ops:
            return StructureRecommendation(
                structure="heap",
                time_complexity={"peek": "O(1)", "insert": "O(log n)", "delete_min": "O(log n)"},
                reasoning="Heap provides O(1) peek for min/max element",
            )
        elif ordering_required and "lookup" in ops:
            return StructureRecommendation(
                structure="sorted_list",
                time_complexity={"lookup": "O(log n)", "insert": "O(n)", "delete": "O(n)"},
                reasoning="Sorted list with binary search when ordering is required",
            )
        elif "prefix_search" in ops:
            return StructureRecommendation(
                structure="trie",
                time_complexity={"lookup": "O(m)", "insert": "O(m)", "prefix_search": "O(m)"},
                reasoning="Trie for prefix-based lookups where m is key length",
            )
        elif "push" in ops and "pop" in ops:
            return StructureRecommendation(
                structure="deque",
                time_complexity={"push": "O(1)", "pop": "O(1)", "peek": "O(1)"},
                reasoning="Deque for efficient push/pop from both ends",
            )
        return StructureRecommendation(
            structure="array",
            time_complexity={"lookup": "O(1)", "insert_end": "O(1)", "insert_middle": "O(n)"},
            reasoning="Array for sequential access patterns with index-based lookup",
        )


# ---------------------------------------------------------------------------
# Memory Optimizer
# ---------------------------------------------------------------------------

class MemoryOptimizer:
    """Suggest memory optimizations."""

    def analyze(
        self, code_sample: str = "", language: str = "python"
    ) -> List[MemorySuggestion]:
        suggestions: List[MemorySuggestion] = []
        if 'list(' in code_sample or '[ ' in code_sample:
            suggestions.append(MemorySuggestion(
                description="Use generator expressions instead of list comprehensions for large datasets",
                impact="high",
                code_example="[x for x in range(n)] -> (x for x in range(n))",
                estimated_savings="50-90% memory for large datasets",
            ))
        if 'dict' in code_sample:
            suggestions.append(MemorySuggestion(
                description="Use __slots__ on classes to reduce instance memory",
                impact="medium",
                code_example="class Point: __slots__ = ['x', 'y']",
                estimated_savings="40-50% per instance",
            ))
        if 'import' in code_sample and 'copy' in code_sample:
            suggestions.append(MemorySuggestion(
                description="Avoid deep copying when shallow copy suffices",
                impact="medium",
                estimated_savings="Variable based on object graph depth",
            ))
        suggestions.append(MemorySuggestion(
            description="Use array.array or numpy for numeric data instead of lists",
            impact="high",
            code_example="import array; arr = array.array('i', range(n))",
            estimated_savings="4-8x less memory for numeric data",
        ))
        return suggestions


# ---------------------------------------------------------------------------
# Concurrency Helper
# ---------------------------------------------------------------------------

class ConcurrencyHelper:
    """Recommend concurrency patterns."""

    def recommend_pattern(
        self,
        task_type: str = "io_bound",
        parallelism_needed: bool = True,
        shared_state: bool = False,
    ) -> ConcurrencyPattern:
        if task_type == "io_bound" and not shared_state:
            return ConcurrencyPattern(
                name="asyncio",
                implementation="async/await with event loop",
                pros=["Lightweight", "High concurrency", "Low overhead"],
                cons=["Requires async-aware libraries"],
            )
        elif task_type == "io_bound" and shared_state:
            return ConcurrencyPattern(
                name="ThreadPoolExecutor",
                implementation="concurrent.futures.ThreadPoolExecutor",
                pros=["Shared state via GIL", "Simple mental model"],
                cons=["GIL limits CPU parallelism"],
            )
        elif task_type == "cpu_bound":
            return ConcurrencyPattern(
                name="ProcessPoolExecutor",
                implementation="concurrent.futures.ProcessPoolExecutor",
                pros=["True parallelism", "Bypasses GIL"],
                cons=["Process startup overhead", "Serialization required"],
            )
        return ConcurrencyPattern(
            name="basic_threading",
            implementation="threading.Thread",
            pros=["Simple to implement"],
            cons=["GIL limitations"],
        )


# ---------------------------------------------------------------------------
# Code Quality Checker
# ---------------------------------------------------------------------------

class CodeQualityChecker:
    """Check code quality metrics."""

    def check(self, code: str) -> List[QualityIssue]:
        issues: List[QualityIssue] = []
        lines = code.split("\n")
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                issues.append(QualityIssue(
                    message=f"Line exceeds 100 characters ({len(line)} chars)",
                    severity="warning", line=i, rule="line_length",
                ))
            if line.strip().startswith("def ") and len(line) > 60:
                issues.append(QualityIssue(
                    message="Function name/description too long",
                    severity="info", line=i, rule="function_length",
                ))
            if re.search(r'\bTODO\b|\bFIXME\b|\bHACK\b', line):
                issues.append(QualityIssue(
                    message="Unresolved TODO/FIXME comment",
                    severity="info", line=i, rule="todo_comment",
                ))
        if "eval(" in code:
            issues.append(QualityIssue(
                message="Avoid eval() — use ast.literal_eval() or specific parsers",
                severity="high", rule="security",
            ))
        if code.count("\n") > 50:
            issues.append(QualityIssue(
                message="Function exceeds 50 lines — consider refactoring",
                severity="warning", rule="function_length",
            ))
        return issues

    def calculate_cyclomatic_complexity(self, code: str) -> int:
        complexity = 1
        complexity += len(re.findall(r'\bif\b|\belif\b|\bwhile\b', code))
        complexity += len(re.findall(r'\band\b|\bor\b', code))
        complexity += len(re.findall(r'for\b', code))
        return complexity


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Efficient Code Demo")
    print("=" * 60)

    print("\n[1] Complexity Analysis")
    analyzer = ComplexityAnalyzer()
    analysis = analyzer.analyze_function(
        "for i in range(n): for j in range(n): total += arr[i][j]",
        [100, 1000, 10000],
    )
    print(f"  Time: {analysis.time_complexity}")
    print(f"  Space: {analysis.space_complexity}")
    print(f"  Bottlenecks: {analysis.bottlenecks}")

    print("\n[2] Data Structure Selection")
    selector = DataStructureSelector()
    rec = selector.recommend(["lookup", "insert"], "random", 100000, False)
    print(f"  Recommended: {rec.structure}")
    print(f"  Complexity: {rec.time_complexity}")

    print("\n[3] Memory Optimization")
    optimizer = MemoryOptimizer()
    suggestions = optimizer.analyze("large_list = [dict() for _ in range(1000000)]")
    for s in suggestions:
        print(f"  [{s.impact}] {s.description}")

    print("\n[4] Concurrency Patterns")
    helper = ConcurrencyHelper()
    pattern = helper.recommend_pattern("io_bound", True, False)
    print(f"  Pattern: {pattern.name}")
    print(f"  Pros: {pattern.pros}")

    print("\n[5] Code Quality")
    checker = CodeQualityChecker()
    issues = checker.check("def f(x): return x+1 if x>0 else None")
    for issue in issues:
        print(f"  [{issue.severity}] {issue.message}")
    complexity = checker.calculate_cyclomatic_complexity("if a: if b: return 1")
    print(f"  Cyclomatic complexity: {complexity}")

    print("\n" + "=" * 60)
    print("  Efficient code demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
