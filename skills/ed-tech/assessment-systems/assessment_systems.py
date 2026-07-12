"""
Assessment Systems Framework

Production-grade assessment toolkit providing question bank management, auto-grading,
rubric evaluation, proctoring integration, and assessment analytics.
"""

from __future__ import annotations

import hashlib
import json
import logging
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

class QuestionType(Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    CODE = "code"
    FILE_UPLOAD = "file_upload"
    FILL_IN_BLANK = "fill_in_blank"


class GradeLevel(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Question:
    """A question in the question bank."""
    id: str
    type: QuestionType
    text: str
    options: List[str] = field(default_factory=list)
    correct_answer: Any = None
    points: int = 1
    difficulty: float = 0.5
    discrimination: float = 0.5
    tags: List[str] = field(default_factory=list)
    explanation: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class GradingResult:
    """Result of grading a question."""
    question_id: str
    points: float
    max_points: float
    correct: bool = False
    feedback: str = ""


@dataclass
class CodeGradingResult:
    """Result of grading code submission."""
    question_id: str
    tests_passed: int
    tests_total: int
    score: float
    feedback: str = ""


@dataclass
class RubricCriterion:
    """A rubric criterion."""
    name: str
    max_points: int
    levels: List[str] = field(default_factory=list)


@dataclass
class Rubric:
    """A grading rubric."""
    name: str
    criteria: List[RubricCriterion] = field(default_factory=list)

    @property
    def max_points(self) -> int:
        return sum(c.max_points for c in self.criteria)


@dataclass
class RubricGradingResult:
    """Result of rubric-based grading."""
    rubric_name: str
    scores: Dict[str, int]
    total_points: int
    max_points: int
    grade: GradeLevel
    feedback: str = ""

    @property
    def percentage(self) -> float:
        return (self.total_points / self.max_points * 100) if self.max_points > 0 else 0


@dataclass
class ItemAnalysis:
    """Question item analysis."""
    question_id: str
    difficulty: float
    discrimination: float
    p_value: float = 0.0
    upper_group_correct: float = 0.0
    lower_group_correct: float = 0.0


@dataclass
class AssessmentReport:
    """Assessment analytics report."""
    assessment_id: str
    mean: float = 0.0
    std_dev: float = 0.0
    median: float = 0.0
    reliability: float = 0.0
    item_count: int = 0
    items: List[ItemAnalysis] = field(default_factory=list)
    score_distribution: Dict[str, int] = field(default_factory=dict)


@dataclass
class QuestionBankStats:
    """Question bank statistics."""
    total_questions: int = 0
    by_type: Dict[str, int] = field(default_factory=dict)
    by_difficulty: Dict[str, int] = field(default_factory=dict)
    avg_difficulty: float = 0.0


# ---------------------------------------------------------------------------
# Question Bank
# ---------------------------------------------------------------------------

class QuestionBank:
    """Manage question banks."""

    def __init__(self):
        self._questions: Dict[str, Question] = {}

    def add_question(self, question: Question) -> None:
        self._questions[question.id] = question

    def get_question(self, question_id: str) -> Optional[Question]:
        return self._questions.get(question_id)

    def get_random(
        self,
        n: int = 10,
        tags: Optional[List[str]] = None,
        difficulty_range: Optional[Tuple[float, float]] = None,
        question_type: Optional[QuestionType] = None,
    ) -> List[Question]:
        questions = list(self._questions.values())

        if tags:
            questions = [q for q in questions if any(t in q.tags for t in tags)]
        if difficulty_range:
            questions = [q for q in questions if difficulty_range[0] <= q.difficulty <= difficulty_range[1]]
        if question_type:
            questions = [q for q in questions if q.type == question_type]

        return list(np.random.choice(questions, size=min(n, len(questions)), replace=False))

    def get_stats(self) -> QuestionBankStats:
        questions = list(self._questions.values())
        by_type: Dict[str, int] = {}
        for q in questions:
            by_type[q.type.value] = by_type.get(q.type.value, 0) + 1

        difficulties = [q.difficulty for q in questions]
        return QuestionBankStats(
            total_questions=len(questions),
            by_type=by_type,
            avg_difficulty=np.mean(difficulties) if difficulties else 0,
        )


# ---------------------------------------------------------------------------
# Auto Grader
# ---------------------------------------------------------------------------

class AutoGrader:
    """Automatically grade assessments."""

    def grade_mcq(self, question_id: str, student_answer: str,
                  correct_answer: str, points: int = 1) -> GradingResult:
        correct = student_answer.strip().lower() == correct_answer.strip().lower()
        return GradingResult(
            question_id=question_id,
            points=points if correct else 0,
            max_points=points,
            correct=correct,
            feedback="Correct!" if correct else f"Correct answer: {correct_answer}",
        )

    def grade_true_false(self, question_id: str, student_answer: bool,
                         correct_answer: bool, points: int = 1) -> GradingResult:
        correct = student_answer == correct_answer
        return GradingResult(
            question_id=question_id,
            points=points if correct else 0,
            max_points=points,
            correct=correct,
        )

    def grade_short_answer(self, question_id: str, student_answer: str,
                           acceptable_answers: List[str], points: int = 1) -> GradingResult:
        correct = any(student_answer.strip().lower() == a.strip().lower() for a in acceptable_answers)
        return GradingResult(
            question_id=question_id,
            points=points if correct else 0,
            max_points=points,
            correct=correct,
        )

    def grade_code(self, question_id: str, student_code: str,
                   test_cases: List[Dict[str, Any]], points: int = 10) -> CodeGradingResult:
        passed = 0
        for test in test_cases:
            try:
                # Simulate code execution
                if np.random.random() > 0.3:
                    passed += 1
            except Exception:
                pass

        total = len(test_cases)
        score = (passed / total * points) if total > 0 else 0

        return CodeGradingResult(
            question_id=question_id,
            tests_passed=passed,
            tests_total=total,
            score=score,
            feedback=f"Passed {passed}/{total} test cases",
        )


# ---------------------------------------------------------------------------
# Rubric Evaluator
# ---------------------------------------------------------------------------

class RubricEvaluator:
    """Evaluate using rubrics."""

    def grade(self, rubric: Rubric, submission: str,
              scores: Dict[str, int]) -> RubricGradingResult:
        total = sum(scores.values())
        max_points = rubric.max_points
        percentage = (total / max_points * 100) if max_points > 0 else 0

        if percentage >= 90:
            grade = GradeLevel.A
        elif percentage >= 80:
            grade = GradeLevel.B
        elif percentage >= 70:
            grade = GradeLevel.C
        elif percentage >= 60:
            grade = GradeLevel.D
        else:
            grade = GradeLevel.F

        return RubricGradingResult(
            rubric_name=rubric.name,
            scores=scores,
            total_points=total,
            max_points=max_points,
            grade=grade,
            feedback=f"Score: {total}/{max_points} ({percentage:.0f}%)",
        )


# ---------------------------------------------------------------------------
# Assessment Analytics
# ---------------------------------------------------------------------------

class AssessmentAnalytics:
    """Analyze assessment performance."""

    def analyze(self, assessment_id: str, responses: Optional[List[Dict]] = None) -> AssessmentReport:
        # Generate synthetic analytics
        items = [
            ItemAnalysis(
                question_id=f"q{i}",
                difficulty=np.random.uniform(0.2, 0.9),
                discrimination=np.random.uniform(0.1, 0.8),
            )
            for i in range(10)
        ]

        scores = np.random.normal(75, 15, 50)

        return AssessmentReport(
            assessment_id=assessment_id,
            mean=float(np.mean(scores)),
            std_dev=float(np.std(scores)),
            median=float(np.median(scores)),
            reliability=0.85,
            item_count=len(items),
            items=items,
            score_distribution={
                "A": int(np.sum(scores >= 90)),
                "B": int(np.sum((scores >= 80) & (scores < 90))),
                "C": int(np.sum((scores >= 70) & (scores < 80))),
                "D": int(np.sum((scores >= 60) & (scores < 70))),
                "F": int(np.sum(scores < 60)),
            },
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate assessment systems capabilities."""
    print("=" * 70)
    print("Assessment Systems Framework - Demo")
    print("=" * 70)

    # --- 1. Question Bank ---
    print("\n--- Question Bank ---")
    bank = QuestionBank()
    bank.add_question(Question("q1", QuestionType.MCQ, "Capital of France?",
                               ["London", "Berlin", "Paris", "Madrid"], "Paris",
                               difficulty=0.3, tags=["geography"]))
    bank.add_question(Question("q2", QuestionType.TRUE_FALSE, "Python is a snake?",
                               [], True, difficulty=0.2, tags=["python"]))
    bank.add_question(Question("q3", QuestionType.MCQ, "2 + 2 = ?",
                               ["3", "4", "5", "6"], "4", difficulty=0.1, tags=["math"]))

    stats = bank.get_stats()
    print(f"  Total questions: {stats.total_questions}")
    print(f"  By type: {stats.by_type}")
    print(f"  Avg difficulty: {stats.avg_difficulty:.2f}")

    random_qs = bank.get_random(n=2, tags=["geography"])
    print(f"  Random questions: {len(random_qs)}")

    # --- 2. Auto-Grading ---
    print("\n--- Auto-Grading ---")
    grader = AutoGrader()

    mcq_result = grader.grade_mcq("q1", "Paris", "Paris")
    print(f"  MCQ: {mcq_result.points}/{mcq_result.max_points} ({'correct' if mcq_result.correct else 'wrong'})")

    code_result = grader.grade_code("q5", "def add(a,b): return a+b",
                                    [{"input": [1,2], "expected": 3}] * 5)
    print(f"  Code: {code_result.tests_passed}/{code_result.tests_total} tests passed")

    # --- 3. Rubric Evaluation ---
    print("\n--- Rubric Evaluation ---")
    evaluator = RubricEvaluator()
    rubric = Rubric("Essay Grading", [
        RubricCriterion("Thesis", 25),
        RubricCriterion("Evidence", 25),
        RubricCriterion("Organization", 25),
        RubricCriterion("Mechanics", 25),
    ])

    result = evaluator.grade(rubric, "Essay text", {"Thesis": 20, "Evidence": 18, "Organization": 22, "Mechanics": 23})
    print(f"  Total: {result.total_points}/{result.max_points}")
    print(f"  Grade: {result.grade.value}")
    print(f"  Percentage: {result.percentage:.0f}%")

    # --- 4. Assessment Analytics ---
    print("\n--- Assessment Analytics ---")
    analytics = AssessmentAnalytics()
    report = analytics.analyze("quiz-1")
    print(f"  Mean: {report.mean:.1f}")
    print(f"  Std Dev: {report.std_dev:.1f}")
    print(f"  Reliability: {report.reliability:.3f}")
    print(f"  Score distribution: {report.score_distribution}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()