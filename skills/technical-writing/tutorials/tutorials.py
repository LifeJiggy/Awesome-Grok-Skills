"""
Progressive Tutorial Authoring & Learning Path Design

Provides tutorial structuring, learning path management, interactive exercises,
assessment generation, prerequisite tracking, and effectiveness analytics.
"""

from __future__ import annotations

import re
import json
import hashlib
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from pathlib import Path


class Difficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    CODE_COMPLETION = "code_completion"
    SHORT_ANSWER = "short_answer"
    MATCHING = "matching"


class StepStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"


class ExerciseType(Enum):
    CODING = "coding"
    FILL_IN_BLANK = "fill_in_blank"
    MULTIPLE_CHOICE = "multiple_choice"
    MATCHING = "matching"


@dataclass
class LearningObjective:
    id: str
    description: str
    bloom_level: str = "understand"


@dataclass
class TutorialStep:
    order: int
    title: str
    content: str
    prerequisites: list[str] = field(default_factory=list)
    exercise: Optional[Exercise] = None
    concepts: list[str] = field(default_factory=list)
    status: StepStatus = StepStatus.DRAFT
    estimated_minutes: int = 10

    def to_markdown(self) -> str:
        lines = [f"## Step {self.order}: {self.title}\n"]
        lines.append(self.content)
        if self.exercise:
            lines.append(f"\n### Exercise\n")
            lines.append(f"**{self.exercise.prompt}**\n")
            lines.append(f"```python\n{self.exercise.starter_code}\n```")
        return "\n".join(lines)


@dataclass
class HintLevel:
    text: str
    level: int = 1


@dataclass
class Exercise:
    type: ExerciseType = ExerciseType.CODING
    prompt: str = ""
    starter_code: str = ""
    validator: Optional[Callable[[str], bool]] = None
    hints: list[str | HintLevel] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    passed: bool
    tests_passed: int = 0
    tests_total: int = 0
    errors: list[str] = field(default_factory=list)
    feedback: str = ""


@dataclass
class TestCase:
    input: Any = None
    expected: Any = None
    description: str = ""


@dataclass
class InteractiveExercise:
    id: str
    title: str
    language: str = "python"
    problem: str = ""
    starter_code: str = ""
    test_cases: list[TestCase] = field(default_factory=list)
    hints: list[HintLevel] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)

    def validate(self, code: str) -> ValidationResult:
        result = ValidationResult(passed=False)
        result.tests_total = len(self.test_cases)
        for tc in self.test_cases:
            try:
                namespace: dict[str, Any] = {}
                exec(code, namespace)
                func_name = re.findall(r"def\s+(\w+)", code)
                if func_name:
                    func = namespace.get(func_name[0])
                    if callable(func):
                        actual = func(tc.input)
                        if actual == tc.expected:
                            result.tests_passed += 1
                        else:
                            result.errors.append(
                                f"Input: {tc.input} — Expected {tc.expected}, got {actual}"
                            )
                    else:
                        result.errors.append(f"Function {func_name[0]} not found in code")
                else:
                    result.errors.append("No function definition found")
            except Exception as e:
                result.errors.append(f"Error: {e}")
        result.passed = result.tests_passed == result.tests_total and result.tests_total > 0
        if result.passed:
            result.feedback = "All tests passed!"
        else:
            result.feedback = f"{result.tests_passed}/{result.tests_total} tests passed."
        return result


class Tutorial:
    def __init__(self, id: str, title: str, difficulty: str = "beginner",
                 estimated_minutes: int = 30,
                 learning_objectives: list[str] | None = None) -> None:
        self.id = id
        self.title = title
        self.difficulty = difficulty
        self.estimated_minutes = estimated_minutes
        self.learning_objectives = learning_objectives or []
        self.steps: list[TutorialStep] = []
        self.concepts_taught: list[str] = []
        self.metadata: dict[str, Any] = {}

    def add_step(self, step: TutorialStep) -> None:
        self.steps.append(step)
        self.steps.sort(key=lambda s: s.order)
        for concept in step.concepts:
            if concept not in self.concepts_taught:
                self.concepts_taught.append(concept)

    def get_step(self, order: int) -> Optional[TutorialStep]:
        for step in self.steps:
            if step.order == order:
                return step
        return None

    def validate_prerequisites(self, available_concepts: list[str]) -> list[str]:
        issues = []
        for step in self.steps:
            for prereq in step.prerequisites:
                if prereq not in available_concepts:
                    issues.append(
                        f"Step {step.order} ({step.title}) requires '{prereq}' "
                        f"which is not available in this tutorial"
                    )
        return issues

    def to_markdown(self) -> str:
        lines = [
            f"# {self.title}\n",
            f"**Difficulty**: {self.difficulty}",
            f"**Estimated Time**: {self.estimated_minutes} minutes\n",
            "## Learning Objectives\n"
        ]
        for obj in self.learning_objectives:
            lines.append(f"- {obj}")
        lines.append("")
        for step in self.steps:
            lines.append(step.to_markdown())
            lines.append("")
        return "\n".join(lines)

    def calculate_total_exercises(self) -> int:
        count = 0
        for step in self.steps:
            if step.exercise:
                count += 1
        return count


@dataclass
class SkillNode:
    id: str
    title: str
    minutes: int = 60
    prerequisites: list[str] = field(default_factory=list)
    difficulty: Difficulty = Difficulty.BEGINNER
    concepts: list[str] = field(default_factory=list)
    status: str = "available"


@dataclass
class Module:
    id: str
    title: str
    nodes: list[SkillNode] = field(default_factory=list)


@dataclass
class PathIssue:
    severity: str
    message: str
    node_id: str = ""


class LearningPath:
    def __init__(self, id: str, title: str, description: str = "") -> None:
        self.id = id
        self.title = title
        self.description = description
        self.modules: list[Module] = []
        self._node_index: dict[str, SkillNode] = {}

    def add_module(self, module_id: str, nodes: list[SkillNode], title: str = "") -> None:
        module = Module(id=module_id, title=title or module_id.replace("-", " ").title(), nodes=nodes)
        self.modules.append(module)
        for node in nodes:
            self._node_index[node.id] = node

    def validate(self) -> list[PathIssue]:
        issues: list[PathIssue] = []
        for module in self.modules:
            for node in module.nodes:
                for prereq_id in node.prerequisites:
                    if prereq_id not in self._node_index:
                        issues.append(PathIssue(
                            severity="error",
                            message=f"Node '{node.id}' depends on unknown node '{prereq_id}'",
                            node_id=node.id
                        ))
                    else:
                        prereq_node = self._node_index[prereq_id]
                        prereq_in_module = None
                        for m in self.modules:
                            if prereq_node in m.nodes:
                                prereq_in_module = m
                                break
                        if prereq_in_module:
                            node_idx = module.nodes.index(node)
                            prereq_idx = prereq_in_module.nodes.index(prereq_node)
                            if module == prereq_in_module and prereq_idx >= node_idx:
                                issues.append(PathIssue(
                                    severity="warning",
                                    message=f"Prerequisite '{prereq_id}' appears after '{node.id}' in same module",
                                    node_id=node.id
                                ))
        all_ids = set()
        for module in self.modules:
            for node in module.nodes:
                if node.id in all_ids:
                    issues.append(PathIssue(
                        severity="error",
                        message=f"Duplicate node ID: {node.id}",
                        node_id=node.id
                    ))
                all_ids.add(node.id)
        return issues

    def get_total_minutes(self) -> int:
        total = 0
        for module in self.modules:
            for node in module.nodes:
                total += node.minutes
        return total

    def get_all_node_ids(self) -> list[str]:
        ids = []
        for module in self.modules:
            for node in module.nodes:
                ids.append(node.id)
        return ids

    def render_skill_tree(self, output: str = "skill-tree.html") -> str:
        lines = [
            "<!DOCTYPE html>",
            "<html><head><title>Skill Tree</title>",
            "<style>body{font-family:sans-serif;margin:20px;}.module{margin:20px 0;padding:15px;border:1px solid #ddd;border-radius:8px;}.node{padding:10px;margin:5px 0;background:#f5f5f5;border-radius:4px;}.prereq{color:#666;font-size:0.9em;}</style>",
            "</head><body>",
            f"<h1>{self.title}</h1>",
            f"<p>{self.description}</p>",
            f"<p>Total estimated time: {self.get_total_minutes()} minutes</p>",
        ]
        for module in self.modules:
            lines.append(f'<div class="module"><h2>{module.title}</h2>')
            for node in module.nodes:
                prereqs = ", ".join(node.prerequisites) if node.prerequisites else "None"
                lines.append(
                    f'<div class="node"><strong>{node.title}</strong> '
                    f'({node.minutes} min) — {node.difficulty.value}'
                    f'<div class="prereq">Prerequisites: {prereqs}</div></div>'
                )
            lines.append("</div>")
        lines.append("</body></html>")
        html = "\n".join(lines)
        try:
            with open(output, "w", encoding="utf-8") as f:
                f.write(html)
        except OSError:
            pass
        return html


@dataclass
class AssessmentQuestion:
    id: str
    type: QuestionType
    stem: str
    options: list[str] = field(default_factory=list)
    correct_answer: str = ""
    difficulty: str = "medium"
    concepts: list[str] = field(default_factory=list)
    points: int = 1


@dataclass
class Assessment:
    id: str
    title: str
    questions: list[AssessmentQuestion] = field(default_factory=list)
    time_limit_minutes: int = 30
    passing_score: float = 0.7


@dataclass
class ScoreResult:
    correct: int = 0
    total: int = 0
    percentage: float = 0.0
    feedback: list[str] = field(default_factory=list)


class AssessmentEngine:
    def __init__(self, tutorials: list[str] | None = None,
                 question_types: list[QuestionType] | None = None,
                 difficulty_distribution: dict[str, float] | None = None) -> None:
        self.tutorials = tutorials or []
        self.question_types = question_types or [QuestionType.MULTIPLE_CHOICE]
        self.difficulty_distribution = difficulty_distribution or {"easy": 0.3, "medium": 0.5, "hard": 0.2}
        self._question_bank: list[AssessmentQuestion] = []

    def generate(self, num_questions: int = 10) -> Assessment:
        import random
        questions: list[AssessmentQuestion] = []
        for i in range(num_questions):
            q_type = random.choice(self.question_types)
            diff = random.choices(
                list(self.difficulty_distribution.keys()),
                weights=list(self.difficulty_distribution.values())
            )[0]
            question = AssessmentQuestion(
                id=f"q{i+1}", type=q_type,
                stem=f"Sample question {i+1} for {diff} difficulty",
                options=["Option A", "Option B", "Option C", "Option D"],
                correct_answer="Option A", difficulty=diff
            )
            questions.append(question)
        return Assessment(
            id=f"assessment-{hashlib.md5(json.dumps(self.tutorials).encode()).hexdigest()[:8]}",
            title=f"Assessment: {', '.join(self.tutorials[:3])}",
            questions=questions
        )

    def score(self, assessment: Assessment, submission: dict[str, str]) -> ScoreResult:
        result = ScoreResult(total=len(assessment.questions))
        for question in assessment.questions:
            answer = submission.get(question.id, "")
            if answer.strip().lower() == question.correct_answer.strip().lower():
                result.correct += 1
            else:
                result.feedback.append(f"{question.id}: Expected '{question.correct_answer}', got '{answer}'")
        result.percentage = (result.correct / result.total * 100) if result.total > 0 else 0.0
        return result


@dataclass
class PainPoint:
    step_order: int
    step_title: str
    failure_rate: float
    common_errors: list[str] = field(default_factory=list)


@dataclass
class TutorialReport:
    tutorial_id: str
    completion_rate: float = 0.0
    avg_completion_minutes: float = 0.0
    exercise_pass_rate: float = 0.0
    hint_usage_rate: float = 0.0
    pain_points: list[PainPoint] = field(default_factory=list)


class TutorialAnalytics:
    def __init__(self, data_dir: str = "analytics/") -> None:
        self.data_dir = Path(data_dir)

    def analyze(self, tutorial_id: str) -> TutorialReport:
        report = TutorialReport(tutorial_id=tutorial_id)
        data_file = self.data_dir / f"{tutorial_id}.json"
        if data_file.exists():
            try:
                with open(data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                report.completion_rate = data.get("completion_rate", 0.0)
                report.avg_completion_minutes = data.get("avg_time", 0.0)
                report.exercise_pass_rate = data.get("exercise_pass_rate", 0.0)
                report.hint_usage_rate = data.get("hint_usage_rate", 0.0)
                for pp in data.get("pain_points", []):
                    report.pain_points.append(PainPoint(
                        step_order=pp.get("step", 0),
                        step_title=pp.get("title", ""),
                        failure_rate=pp.get("failure_rate", 0.0),
                        common_errors=pp.get("errors", [])
                    ))
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return report


def main() -> None:
    print("=" * 60)
    print("Progressive Tutorial Authoring & Learning Path Design")
    print("=" * 60)

    tutorial = Tutorial(
        id="intro-python-functions",
        title="Introduction to Python Functions",
        difficulty="beginner",
        estimated_minutes=30,
        learning_objectives=[
            "Define functions with parameters and return values",
            "Understand scope and variable lifetime",
            "Write functions that process lists"
        ]
    )
    tutorial.add_step(TutorialStep(
        order=1, title="Your First Function",
        content="A function is a reusable block of code.",
        exercise=Exercise(type=ExerciseType.CODING,
                          prompt="Write a square function",
                          starter_code="def square(n):\n    pass",
                          validator=lambda c: "return" in c)
    ))
    tutorial.add_step(TutorialStep(
        order=2, title="Default Parameters",
        content="Parameters can have default values.",
        prerequisites=["intro-python-basics"]
    ))
    print(f"\n[Tutorial] {tutorial.title} — {len(tutorial.steps)} steps, "
          f"{tutorial.calculate_total_exercises()} exercises")

    path = LearningPath(id="python-backend", title="Python Backend Development",
                        description="Go from zero to building production APIs")
    path.add_module("fundamentals", [
        SkillNode(id="python-basics", title="Python Basics", minutes=120),
        SkillNode(id="python-functions", title="Functions & Modules", minutes=90,
                  prerequisites=["python-basics"]),
    ])
    path.add_module("web", [
        SkillNode(id="http-fundamentals", title="HTTP Fundamentals", minutes=60),
        SkillNode(id="flask-intro", title="Introduction to Flask", minutes=120,
                  prerequisites=["python-functions", "http-fundamentals"]),
    ])
    issues = path.validate()
    print(f"\n[LearningPath] {path.title} — {len(issues)} validation issues, "
          f"{path.get_total_minutes()} min total")

    exercise = InteractiveExercise(
        id="list-comp", title="List Comprehensions", language="python",
        problem="Filter and square even numbers",
        starter_code="def even_squares(numbers):\n    pass",
        test_cases=[
            TestCase(input=[1, 2, 3, 4, 5, 6], expected=[4, 16, 36]),
        ],
        hints=[HintLevel(text="Use list comprehension", level=1)]
    )
    result = exercise.validate("def even_squares(numbers):\n    return [n**2 for n in numbers if n % 2 == 0]")
    print(f"\n[Exercise] Validation: passed={result.passed}, "
          f"{result.tests_passed}/{result.tests_total} tests")

    engine = AssessmentEngine(
        tutorials=["intro-python-functions"],
        difficulty_distribution={"easy": 0.3, "medium": 0.5, "hard": 0.2}
    )
    assessment = engine.generate(num_questions=5)
    print(f"\n[Assessment] Generated {len(assessment.questions)} questions")

    analytics = TutorialAnalytics(data_dir="analytics/")
    report = analytics.analyze("intro-python-functions")
    print(f"\n[Analytics] Completion: {report.completion_rate:.1%}, "
          f"Pain points: {len(report.pain_points)}")

    print("\n" + "=" * 60)
    print("All tutorial components initialized successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
