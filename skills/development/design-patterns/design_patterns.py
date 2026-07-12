"""
Design Patterns Framework

Production-grade design patterns toolkit providing pattern detection, implementation
guidance, anti-pattern identification, and pattern selection for software architecture.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PatternCategory(Enum):
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"


class PatternType(Enum):
    SINGLETON = "singleton"
    FACTORY_METHOD = "factory_method"
    ABSTRACT_FACTORY = "abstract_factory"
    BUILDER = "builder"
    PROTOTYPE = "prototype"
    ADAPTER = "adapter"
    BRIDGE = "bridge"
    COMPOSITE = "composite"
    DECORATOR = "decorator"
    FACADE = "facade"
    PROXY = "proxy"
    OBSERVER = "observer"
    STRATEGY = "strategy"
    COMMAND = "command"
    STATE = "state"
    TEMPLATE_METHOD = "template_method"
    ITERATOR = "iterator"


class AntiPatternType(Enum):
    GOD_OBJECT = "god_object"
    SPAGHETTI_CODE = "spaghetti_code"
    GOLDEN_HAMMER = "golden_hammer"
    LAVA_FLOW = "lava_flow"
    PREMATURE_OPTIMIZATION = "premature_optimization"


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PatternInfo:
    """Information about a detected pattern."""
    name: str
    pattern_type: PatternType
    category: PatternCategory
    file: str
    line: int
    confidence: float
    description: str = ""
    related_patterns: List[str] = field(default_factory=list)


@dataclass
class AntiPatternInfo:
    """Information about a detected anti-pattern."""
    name: str
    anti_pattern_type: AntiPatternType
    severity: Severity
    description: str
    file: str
    line: int
    impact: str = ""
    refactoring_suggestion: str = ""


@dataclass
class PatternImplementation:
    """Pattern implementation template."""
    name: str
    pattern_type: PatternType
    language: str
    code: str
    usage_example: str = ""
    description: str = ""
    trade_offs: str = ""


@dataclass
class PatternRecommendation:
    """Pattern recommendation."""
    name: str
    pattern_type: PatternType
    reason: str
    trade_offs: str = ""
    complexity: str = ""
    effort: str = ""


@dataclass
class PatternDefinition:
    """Complete pattern definition."""
    name: str
    pattern_type: PatternType
    category: PatternCategory
    intent: str
    structure: str
    participants: List[str]
    collaborations: List[str]
    consequences: List[str]
    implementation_notes: str = ""
    related_patterns: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Pattern Catalog
# ---------------------------------------------------------------------------

PATTERN_CATALOG: Dict[PatternType, PatternDefinition] = {
    PatternType.SINGLETON: PatternDefinition(
        name="Singleton",
        pattern_type=PatternType.SINGLETON,
        category=PatternCategory.CREATIONAL,
        intent="Ensure a class has only one instance and provide a global point of access to it.",
        structure="Class with private constructor and static instance method",
        participants=["Singleton"],
        collaborations=["Client accesses Singleton via getInstance()"],
        consequences=[
            "Controlled access to sole instance",
            "Reduced namespace pollution",
            "Permits fine-grained control of instance lifecycle",
            "Can mask bad design (global state)",
        ],
    ),
    PatternType.OBSERVER: PatternDefinition(
        name="Observer",
        pattern_type=PatternType.OBSERVER,
        category=PatternCategory.BEHAVIORAL,
        intent="Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.",
        structure="Subject with attach/detach/notify, Observer with update method",
        participants=["Subject", "Observer", "ConcreteSubject", "ConcreteObserver"],
        collaborations=["Subject notifies Observers of state changes"],
        consequences=[
            "Loose coupling between Subject and Observer",
            "Support for broadcast communication",
            "Unexpected updates possible",
            "Memory leaks if observers not properly detached",
        ],
    ),
    PatternType.STRATEGY: PatternDefinition(
        name="Strategy",
        pattern_type=PatternType.STRATEGY,
        category=PatternCategory.BEHAVIORAL,
        intent="Define a family of algorithms, encapsulate each one, and make them interchangeable.",
        structure="Context with Strategy interface, concrete strategies implement algorithm",
        participants=["Context", "Strategy", "ConcreteStrategy"],
        collaborations=["Context delegates to Strategy"],
        consequences=[
            "Algorithms can be swapped at runtime",
            "Eliminates conditional statements",
            "Clients must be aware of different strategies",
            "Communication overhead between Context and Strategy",
        ],
    ),
    PatternType.FACADE: PatternDefinition(
        name="Facade",
        pattern_type=PatternType.FACADE,
        category=PatternCategory.STRUCTURAL,
        intent="Provide a unified interface to a set of interfaces in a subsystem.",
        structure="Facade class providing simplified methods",
        participants=["Facade", "Subsystem classes"],
        collaborations=["Facade delegates to subsystem objects"],
        consequences=[
            "Simplifies interface to subsystem",
            "Doesn't prevent direct subsystem access",
            "May become God Object if not careful",
        ],
    ),
    PatternType.DECORATOR: PatternDefinition(
        name="Decorator",
        pattern_type=PatternType.DECORATOR,
        category=PatternCategory.STRUCTURAL,
        intent="Attach additional responsibilities to an object dynamically.",
        structure="Component interface, ConcreteComponent, Decorator with inheritance",
        participants=["Component", "ConcreteComponent", "Decorator", "ConcreteDecorator"],
        collaborations=["Decorator wraps Component, delegates and adds behavior"],
        consequences=[
            "More flexible than inheritance",
            "Small, focused classes",
            "Can result in many small objects",
        ],
    ),
}


# ---------------------------------------------------------------------------
# Pattern Detector
# ---------------------------------------------------------------------------

class PatternDetector:
    """Detect design patterns in code."""

    def detect_file(self, file_path: str) -> List[PatternInfo]:
        patterns = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")

        # Singleton detection
        if "__instance" in content or "getInstance" in content:
            patterns.append(PatternInfo(
                name="Singleton",
                pattern_type=PatternType.SINGLETON,
                category=PatternCategory.CREATIONAL,
                file=file_path,
                line=1,
                confidence=0.85,
                description="Class with instance control mechanism",
            ))

        # Observer detection
        if "subscribe" in content.lower() or "notify" in content.lower() or "observer" in content.lower():
            patterns.append(PatternInfo(
                name="Observer",
                pattern_type=PatternType.OBSERVER,
                category=PatternCategory.BEHAVIORAL,
                file=file_path,
                line=1,
                confidence=0.75,
                description="Subscription/notification mechanism detected",
            ))

        # Strategy detection
        if "strategy" in content.lower() or re.search(r"def\s+execute.*strategy", content, re.IGNORECASE):
            patterns.append(PatternInfo(
                name="Strategy",
                pattern_type=PatternType.STRATEGY,
                category=PatternCategory.BEHAVIORAL,
                file=file_path,
                line=1,
                confidence=0.70,
                description="Strategy-like interface detected",
            ))

        # Factory detection
        if "factory" in content.lower() or re.search(r"def\s+create.*\(", content):
            patterns.append(PatternInfo(
                name="Factory Method",
                pattern_type=PatternType.FACTORY_METHOD,
                category=PatternCategory.CREATIONAL,
                file=file_path,
                line=1,
                confidence=0.65,
                description="Factory-like creation method detected",
            ))

        return patterns

    def detect_directory(self, directory: str) -> List[PatternInfo]:
        all_patterns = []
        import os
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        all_patterns.extend(self.detect_file(file_path))
                    except Exception:
                        pass
        return all_patterns


# ---------------------------------------------------------------------------
# Anti-Pattern Detector
# ---------------------------------------------------------------------------

class AntiPatternDetector:
    """Detect anti-patterns in code."""

    def detect(self, file_path: str) -> List[AntiPatternInfo]:
        anti_patterns = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # God Object detection
        class_methods = 0
        for line in lines:
            if line.strip().startswith("def "):
                class_methods += 1
        if class_methods > 20:
            anti_patterns.append(AntiPatternInfo(
                name="God Object",
                anti_pattern_type=AntiPatternType.GOD_OBJECT,
                severity=Severity.HIGH,
                description=f"Class has {class_methods} methods (threshold: 20)",
                file=file_path,
                line=1,
                impact="Hard to maintain, test, and understand",
                refactoring_suggestion="Extract Class: split into smaller, focused classes",
            ))

        # Spaghetti Code detection
        max_indent = 0
        for line in lines:
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            max_indent = max(max_indent, indent)
        if max_indent > 20:
            anti_patterns.append(AntiPatternInfo(
                name="Spaghetti Code",
                anti_pattern_type=AntiPatternType.SPAGHETTI_CODE,
                severity=Severity.MEDIUM,
                description=f"Maximum nesting depth: {max_indent // 4} levels",
                file=file_path,
                line=1,
                impact="Hard to follow and maintain",
                refactoring_suggestion="Extract Method and reduce nesting",
            ))

        # Long Method
        func_len = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("def "):
                func_len = 0
            func_len += 1
            if func_len > 50:
                anti_patterns.append(AntiPatternInfo(
                    name="Long Method",
                    anti_pattern_type=AntiPatternType.SPAGHETTI_CODE,
                    severity=Severity.MEDIUM,
                    description=f"Function exceeds 50 lines",
                    file=file_path,
                    line=i + 1,
                    impact="Hard to understand and test",
                    refactoring_suggestion="Extract Method: break into smaller functions",
                ))
                break

        return anti_patterns


# ---------------------------------------------------------------------------
# Pattern Implemenation Generator
# ---------------------------------------------------------------------------

class PatternImplGenerator:
    """Generate pattern implementations."""

    def generate(
        self,
        pattern: PatternType,
        language: str = "python",
        subject_class: str = "Subject",
        observer_class: str = "Observer",
    ) -> PatternImplementation:
        implementations = {
            PatternType.OBSERVER: PatternImplementation(
                name="Observer",
                pattern_type=PatternType.OBSERVER,
                language=language,
                code="""class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)


class Observer:
    def update(self, event):
        raise NotImplementedError


class ConcreteObserver(Observer):
    def update(self, event):
        print(f"Observer received: {event}")""",
                usage_example="""subject = Subject()
observer = ConcreteObserver()
subject.attach(observer)
subject.notify("order_placed")""",
            ),
            PatternType.STRATEGY: PatternImplementation(
                name="Strategy",
                pattern_type=PatternType.STRATEGY,
                language=language,
                code="""class Strategy:
    def execute(self, data):
        raise NotImplementedError


class ConcreteStrategyA(Strategy):
    def execute(self, data):
        return sorted(data)


class ConcreteStrategyB(Strategy):
    def execute(self, data):
        return sorted(data, reverse=True)


class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def execute(self, data):
        return self._strategy.execute(data)""",
                usage_example="""context = Context(ConcreteStrategyA())
result = context.execute([3, 1, 2])
context.set_strategy(ConcreteStrategyB())
result = context.execute([3, 1, 2])""",
            ),
        }

        return implementations.get(pattern, PatternImplementation(
            name=pattern.value,
            pattern_type=pattern,
            language=language,
            code=f"# {pattern.value} implementation for {language}",
        ))


# ---------------------------------------------------------------------------
# Pattern Selector
# ---------------------------------------------------------------------------

class PatternSelector:
    """Recommend patterns based on requirements."""

    def recommend(
        self,
        requirements: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[PatternRecommendation]:
        recommendations = []
        req_text = " ".join(requirements).lower()

        if "notify" in req_text or "subscribe" in req_text:
            recommendations.append(PatternRecommendation(
                name="Observer",
                pattern_type=PatternType.OBSERVER,
                reason="Requirements mention notification/subscription",
                trade_offs="Loose coupling but potential memory leaks",
                complexity="medium",
                effort="2-4 hours",
            ))

        if "algorithm" in req_text or "strategy" in req_text or "interchangeable" in req_text:
            recommendations.append(PatternRecommendation(
                name="Strategy",
                pattern_type=PatternType.STRATEGY,
                reason="Requirements mention interchangeable algorithms",
                trade_offs="Flexible but increases class count",
                complexity="low",
                effort="1-3 hours",
            ))

        if "simplify" in req_text or "interface" in req_text or "subsystem" in req_text:
            recommendations.append(PatternRecommendation(
                name="Facade",
                pattern_type=PatternType.FACADE,
                reason="Requirements mention simplifying complex interfaces",
                trade_offs="Simplifies but may hide important details",
                complexity="low",
                effort="1-2 hours",
            ))

        if "singleton" in req_text or "single instance" in req_text:
            recommendations.append(PatternRecommendation(
                name="Singleton",
                pattern_type=PatternType.SINGLETON,
                reason="Requirements mention single instance",
                trade_offs="Global access but testing difficulties",
                complexity="low",
                effort="0.5-1 hours",
            ))

        if not recommendations:
            recommendations.append(PatternRecommendation(
                name="Facade",
                pattern_type=PatternType.FACADE,
                reason="Good default for simplifying interfaces",
                trade_offs="May oversimplify complex systems",
                complexity="low",
                effort="1-2 hours",
            ))

        return recommendations

    def get_pattern_info(self, pattern: PatternType) -> Optional[PatternDefinition]:
        return PATTERN_CATALOG.get(pattern)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate design patterns capabilities."""
    print("=" * 70)
    print("Design Patterns Framework - Demo")
    print("=" * 70)

    # --- 1. Pattern Detection ---
    print("\n--- Pattern Detection ---")
    detector = PatternDetector()
    # Create test file
    test_file = "/tmp/test_patterns.py"
    with open(test_file, "w") as f:
        f.write("class OrderService:\n")
        f.write("    _instance = None\n")
        f.write("    def getInstance(cls):\n")
        f.write("        if cls._instance is None:\n")
        f.write("            cls._instance = cls()\n")
        f.write("        return cls._instance\n")
        f.write("    def subscribe(self, observer):\n")
        f.write("        self.observers.append(observer)\n")
        f.write("    def notify(self, event):\n")
        f.write("        for obs in self.observers:\n")
        f.write("            obs.update(event)\n")

    patterns = detector.detect_file(test_file)
    print(f"  Patterns found: {len(patterns)}")
    for p in patterns:
        print(f"    {p.name} ({p.category.value}): {p.description}")
        print(f"      Confidence: {p.confidence:.0%}")

    # --- 2. Anti-Pattern Detection ---
    print("\n--- Anti-Pattern Detection ---")
    anti_detector = AntiPatternDetector()
    anti_patterns = anti_detector.detect(test_file)
    print(f"  Anti-patterns: {len(anti_patterns)}")
    for ap in anti_patterns:
        print(f"    {ap.name} ({ap.severity.value}): {ap.description}")
        print(f"      Fix: {ap.refactoring_suggestion}")

    # --- 3. Pattern Implementation ---
    print("\n--- Pattern Implementation ---")
    impl_gen = PatternImplGenerator()
    observer_impl = impl_gen.generate(PatternType.OBSERVER)
    print(f"  Pattern: {observer_impl.name}")
    print(f"  Language: {observer_impl.language}")
    print(f"  Code length: {len(observer_impl.code)} chars")
    print(f"  Usage example:")
    print(f"    {observer_impl.usage_example[:100]}...")

    # --- 4. Pattern Selection ---
    print("\n--- Pattern Selection ---")
    selector = PatternSelector()
    recs = selector.recommend(
        requirements=["notify multiple components", "decouple sender and receiver"],
        context={"language": "python", "complexity": "medium"},
    )
    print(f"  Recommendations: {len(recs)}")
    for rec in recs:
        print(f"    {rec.name}: {rec.reason}")
        print(f"      Trade-offs: {rec.trade_offs}")
        print(f"      Effort: {rec.effort}")

    # --- 5. Pattern Catalog ---
    print("\n--- Pattern Catalog ---")
    print(f"  Available patterns: {len(PATTERN_CATALOG)}")
    for ptype, pdef in PATTERN_CATALOG.items():
        print(f"    {pdef.name}: {pdef.intent[:60]}...")

    # Cleanup
    import os
    os.remove(test_file)

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()