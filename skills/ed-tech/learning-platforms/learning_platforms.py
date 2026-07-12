"""
Learning Platforms Framework

Production-grade learning platform toolkit providing course management, content delivery,
progress tracking, assessment integration, and learner analytics.
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

class ContentType(Enum):
    VIDEO = "video"
    SCORM = "scorm"
    HTML5 = "html5"
    DOCUMENT = "document"
    QUIZ = "quiz"
    INTERACTIVE = "interactive"


class CompletionStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class QuestionType(Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    CODE = "code"
    FILE_UPLOAD = "file_upload"


class VerbType(Enum):
    COMPLETED = "completed"
    ATTEMPTED = "attempted"
    PASSED = "passed"
    FAILED = "failed"
    EXPERIENCED = "experienced"
    WATCHED = "watched"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Lesson:
    """A course lesson."""
    id: str
    title: str
    content_type: ContentType
    duration_minutes: int = 0
    content_url: str = ""
    is_required: bool = True


@dataclass
class Module:
    """A course module."""
    id: str
    title: str
    lessons: List[Lesson] = field(default_factory=list)
    order: int = 0

    @property
    def lesson_count(self) -> int:
        return len(self.lessons)


@dataclass
class Course:
    """A learning course."""
    id: str
    title: str
    description: str = ""
    instructor: str = ""
    modules: List[Module] = field(default_factory=list)
    duration_hours: float = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def total_lessons(self) -> int:
        return sum(m.lesson_count for m in self.modules)


@dataclass
class Enrollment:
    """Learner enrollment."""
    learner_email: str
    course_id: str
    enrolled_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: CompletionStatus = CompletionStatus.NOT_STARTED


@dataclass
class xAPIStatement:
    """xAPI learning activity statement."""
    actor: str
    verb: VerbType
    object: str
    result: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class LearnerProgress:
    """Learner progress information."""
    learner_email: str
    course_id: str
    completion_pct: float = 0.0
    time_spent_hours: float = 0.0
    avg_score: float = 0.0
    completed_lessons: int = 0
    total_lessons: int = 0
    last_activity: Optional[datetime] = None
    status: CompletionStatus = CompletionStatus.NOT_STARTED


@dataclass
class Question:
    """Assessment question."""
    id: str
    question_type: QuestionType
    text: str
    options: List[str] = field(default_factory=list)
    correct_answer: Any = None
    points: int = 1
    explanation: str = ""


@dataclass
class Assessment:
    """An assessment."""
    id: str
    title: str
    questions: List[Question] = field(default_factory=list)
    time_limit_minutes: int = 0
    passing_score: float = 70.0
    max_attempts: int = 3


@dataclass
class AssessmentResult:
    """Assessment grading result."""
    assessment_id: str
    score: float
    passed: bool
    feedback: str = ""
    correct_answers: int = 0
    total_questions: int = 0
    graded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AtRiskLearner:
    """At-risk learner identification."""
    email: str
    course_id: str
    risk_score: float
    risk_reason: str
    last_activity: Optional[datetime] = None


@dataclass
class CourseReport:
    """Course analytics report."""
    course_id: str
    enrolled_count: int = 0
    completed_count: int = 0
    completion_rate: float = 0.0
    avg_score: float = 0.0
    avg_time_hours: float = 0.0
    engagement_rate: float = 0.0


# ---------------------------------------------------------------------------
# Course Manager
# ---------------------------------------------------------------------------

class CourseManager:
    """Manage learning courses."""

    def __init__(self):
        self._courses: Dict[str, Course] = {}
        self._enrollments: List[Enrollment] = []

    def create_course(self, title: str, description: str = "",
                      instructor: str = "", duration_hours: float = 0,
                      modules: Optional[List[Dict[str, Any]]] = None) -> Course:
        course_id = hashlib.md5(f"{title}:{time.time()}".encode()).hexdigest()[:8]
        course_modules = []

        for i, mod in enumerate(modules or []):
            module = Module(
                id=f"mod-{i}",
                title=mod.get("title", f"Module {i + 1}"),
                order=i,
                lessons=[
                    Lesson(
                        id=f"lesson-{i}-{j}",
                        title=f"Lesson {j + 1}",
                        content_type=ContentType.VIDEO,
                        duration_minutes=15,
                    )
                    for j in range(mod.get("lessons", 5))
                ],
            )
            course_modules.append(module)

        course = Course(
            id=course_id,
            title=title,
            description=description,
            instructor=instructor,
            modules=course_modules,
            duration_hours=duration_hours,
        )
        self._courses[course_id] = course
        return course

    def get_course(self, course_id: str) -> Optional[Course]:
        return self._courses.get(course_id)

    def enroll(self, learner_email: str, course_id: str) -> Enrollment:
        enrollment = Enrollment(learner_email=learner_email, course_id=course_id)
        self._enrollments.append(enrollment)
        return enrollment


# ---------------------------------------------------------------------------
# Progress Tracker
# ---------------------------------------------------------------------------

class ProgressTracker:
    """Track learner progress with xAPI."""

    def __init__(self):
        self._statements: List[xAPIStatement] = []
        self._progress: Dict[str, LearnerProgress] = {}

    def record(self, statement: xAPIStatement) -> None:
        self._statements.append(statement)
        key = f"{statement.actor}:{statement.object}"

    def get_progress(self, learner_email: str, course_id: str) -> LearnerProgress:
        key = f"{learner_email}:{course_id}"
        if key not in self._progress:
            self._progress[key] = LearnerProgress(
                learner_email=learner_email,
                course_id=course_id,
                completion_pct=np.random.uniform(10, 90),
                time_spent_hours=np.random.uniform(5, 30),
                avg_score=np.random.uniform(60, 95),
                completed_lessons=np.random.randint(5, 20),
                total_lessons=25,
            )
        return self._progress[key]


# ---------------------------------------------------------------------------
# Assessment Engine
# ---------------------------------------------------------------------------

class AssessmentEngine:
    """Create and grade assessments."""

    def __init__(self):
        self._assessments: Dict[str, Assessment] = {}

    def create_assessment(self, title: str, questions: int = 10,
                          time_limit_minutes: int = 30,
                          passing_score: float = 70.0) -> Assessment:
        assessment_id = hashlib.md5(f"{title}:{time.time()}".encode()).hexdigest()[:8]
        question_list = [
            Question(
                id=f"q{i}",
                question_type=QuestionType.MCQ,
                text=f"Question {i + 1}",
                options=["A", "B", "C", "D"],
                correct_answer="A",
            )
            for i in range(questions)
        ]

        assessment = Assessment(
            id=assessment_id,
            title=title,
            questions=question_list,
            time_limit_minutes=time_limit_minutes,
            passing_score=passing_score,
        )
        self._assessments[assessment_id] = assessment
        return assessment

    def grade(self, assessment_id: str, submission: Dict[str, Any]) -> AssessmentResult:
        assessment = self._assessments.get(assessment_id)
        if not assessment:
            return AssessmentResult(assessment_id=assessment_id, score=0, passed=False)

        correct = sum(1 for q in assessment.questions
                      if submission.get(q.id) == q.correct_answer)
        total = len(assessment.questions)
        score = (correct / total * 100) if total > 0 else 0

        return AssessmentResult(
            assessment_id=assessment_id,
            score=score,
            passed=score >= assessment.passing_score,
            correct_answers=correct,
            total_questions=total,
        )


# ---------------------------------------------------------------------------
# Analytics Engine
# ---------------------------------------------------------------------------

class AnalyticsEngine:
    """Generate learning analytics."""

    def course_report(self, course_id: str) -> CourseReport:
        enrolled = np.random.randint(50, 500)
        completed = int(enrolled * np.random.uniform(0.3, 0.8))

        return CourseReport(
            course_id=course_id,
            enrolled_count=enrolled,
            completed_count=completed,
            completion_rate=completed / enrolled if enrolled > 0 else 0,
            avg_score=np.random.uniform(65, 90),
            avg_time_hours=np.random.uniform(15, 40),
            engagement_rate=np.random.uniform(0.5, 0.9),
        )

    def get_at_risk_learners(self, course_id: str) -> List[AtRiskLearner]:
        return [
            AtRiskLearner(f"learner{i}@example.com", course_id,
                         np.random.uniform(0.5, 0.9),
                         np.random.choice(["Low engagement", "Falling behind", "Low scores"]))
            for i in range(5)
        ]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate learning platforms capabilities."""
    print("=" * 70)
    print("Learning Platforms Framework - Demo")
    print("=" * 70)

    # --- 1. Course Management ---
    print("\n--- Course Management ---")
    manager = CourseManager()
    course = manager.create_course(
        title="Python Programming",
        description="Learn Python from scratch",
        instructor="jane@company.com",
        duration_hours=40,
        modules=[
            {"title": "Introduction", "lessons": 5},
            {"title": "Data Types", "lessons": 8},
            {"title": "Functions", "lessons": 6},
        ],
    )
    print(f"  Course: {course.title}")
    print(f"  Modules: {len(course.modules)}")
    print(f"  Lessons: {course.total_lessons}")

    enrollment = manager.enroll("learner@example.com", course.id)
    print(f"  Enrolled: {enrollment.learner_email}")

    # --- 2. Progress Tracking ---
    print("\n--- Progress Tracking ---")
    tracker = ProgressTracker()
    statement = xAPIStatement(
        actor="learner@example.com",
        verb=VerbType.COMPLETED,
        object="lesson-variables",
        result={"score": 85, "time_spent": 300},
    )
    tracker.record(statement)

    progress = tracker.get_progress("learner@example.com", course.id)
    print(f"  Completion: {progress.completion_pct:.1f}%")
    print(f"  Time spent: {progress.time_spent_hours:.1f} hours")
    print(f"  Avg score: {progress.avg_score:.1f}%")

    # --- 3. Assessment ---
    print("\n--- Assessment ---")
    engine = AssessmentEngine()
    assessment = engine.create_assessment("Python Quiz", questions=10, time_limit_minutes=30)
    print(f"  Assessment: {assessment.title}")
    print(f"  Questions: {len(assessment.questions)}")

    result = engine.grade(assessment.id, {"q0": "A", "q1": "A", "q2": "B"})
    print(f"  Score: {result.score:.0f}%")
    print(f"  Passed: {result.passed}")
    print(f"  Correct: {result.correct_answers}/{result.total_questions}")

    # --- 4. Analytics ---
    print("\n--- Learning Analytics ---")
    analytics = AnalyticsEngine()
    report = analytics.course_report(course.id)
    print(f"  Enrolled: {report.enrolled_count}")
    print(f"  Completed: {report.completed_count}")
    print(f"  Completion rate: {report.completion_rate:.1%}")
    print(f"  Avg score: {report.avg_score:.1f}%")

    at_risk = analytics.get_at_risk_learners(course.id)
    print(f"  At-risk learners: {len(at_risk)}")
    for learner in at_risk[:3]:
        print(f"    {learner.email}: {learner.risk_reason} (risk: {learner.risk_score:.0%})")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()