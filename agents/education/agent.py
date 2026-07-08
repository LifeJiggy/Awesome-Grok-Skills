"""Education Agent — Learning management, curriculum design, and adaptive learning.

Covers course creation, module/lesson management, learner progress tracking,
adaptive assessments, quiz grading, certification, learning path optimization,
spaced repetition, cognitive load management, and educational analytics.
"""

import logging
import hashlib
import math
import random
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Union
from uuid import uuid4

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class CourseStatus(Enum):
    """Course lifecycle states."""
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"


class LessonType(Enum):
    """Types of lesson content."""
    VIDEO = "video"
    TEXT = "text"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    DISCUSSION = "discussion"
    LAB = "lab"
    PODCAST = "podcast"
    DOCUMENT = "document"
    LIVE_SESSION = "live_session"


class LearnerProgress(Enum):
    """Learner enrollment and progress states."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DROPPED = "dropped"
    PAUSED = "paused"


class AssessmentType(Enum):
    """Assessment format types."""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    CODING = "coding"
    FILL_BLANK = "fill_blank"
    MATCHING = "matching"
    ORDERING = "ordering"
    RUBRIC = "rubric"
    PEER_REVIEW = "peer_review"


class DifficultyLevel(Enum):
    """Content difficulty tiers."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class LearningStyle(Enum):
    """VARK learning style model."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING_WRITING = "reading_writing"
    KINESTHETIC = "kinesthetic"


class ContentType(Enum):
    """Content modality types."""
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    IMAGE = "image"
    INTERACTIVE = "interactive"
    SIMULATION = "simulation"
    CODE = "code"
    MIXED = "mixed"


class EngagementLevel(Enum):
    """Learner engagement classification."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DISENGAGED = "disengaged"


class FeedbackType(Enum):
    """Feedback delivery modes."""
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
    BATCH = "batch"
    PEER = "peer"
    AUTOMATED = "automated"


class CertificateStatus(Enum):
    """Certificate lifecycle states."""
    PENDING = "pending"
    ISSUED = "issued"
    REVOKED = "revoked"
    EXPIRED = "expired"


class NotificationType(Enum):
    """Learner notification categories."""
    COURSE_UPDATE = "course_update"
    ASSIGNMENT_DUE = "assignment_due"
    GRADE_POSTED = "grade_posted"
    CERTIFICATE_READY = "certificate_ready"
    ENROLLMENT_CONFIRMED = "enrollment_confirmed"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    REMINDER = "reminder"
    SYSTEM = "system"


class ContentAccess(Enum):
    """Content access levels."""
    FREE = "free"
    ENROLLED = "enrolled"
    PREMIUM = "premium"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class GamificationAction(Enum):
    """Gamification event types."""
    LESSON_COMPLETED = "lesson_completed"
    QUIZ_PASSED = "quiz_passed"
    STREAK_MAINTAINED = "streak_maintained"
    ACHIEVEMENT_EARNED = "achievement_earned"
    COURSE_COMPLETED = "course_completed"
    PEER_HELPED = "peer_helped"
    DISCUSSION_POSTED = "discussion_posted"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class LearningObjective:
    """A specific learning objective for a lesson or module."""
    objective_id: str = field(default_factory=lambda: str(uuid4()))
    description: str = ""
    bloom_level: str = "remember"
    measurable_outcome: str = ""
    assessment_criteria: List[str] = field(default_factory=list)

    BLOOM_LEVELS = [
        "remember", "understand", "apply", "analyze", "evaluate", "create"
    ]


@dataclass
class ContentResource:
    """A content resource attached to a lesson."""
    resource_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    url: str = ""
    content_type: ContentType = ContentType.TEXT
    file_size_bytes: int = 0
    duration_seconds: Optional[int] = None
    is_downloadable: bool = True
    access_level: ContentAccess = ContentAccess.ENROLLED
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Lesson:
    """A single lesson within a module."""
    lesson_id: str = field(default_factory=lambda: str(uuid4()))
    module_id: str = ""
    title: str = ""
    description: str = ""
    content: str = ""
    lesson_type: LessonType = LessonType.TEXT
    duration_minutes: int = 10
    order: int = 0
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    learning_objectives: List[LearningObjective] = field(default_factory=list)
    resources: List[ContentResource] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    is_mandatory: bool = True
    passing_score: float = 70.0
    max_attempts: int = 3
    estimated_effort_hours: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def has_objectives(self) -> bool:
        return len(self.learning_objectives) > 0

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.title:
            errors.append("Lesson title is required")
        if self.duration_minutes <= 0:
            errors.append("Duration must be positive")
        if self.passing_score < 0 or self.passing_score > 100:
            errors.append("Passing score must be 0-100")
        return errors


@dataclass
class Module:
    """A module grouping related lessons."""
    module_id: str = field(default_factory=lambda: str(uuid4()))
    course_id: str = ""
    title: str = ""
    description: str = ""
    order: int = 0
    lessons: List[str] = field(default_factory=list)
    is_mandatory: bool = True
    unlock_prerequisites: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def lesson_count(self) -> int:
        return len(self.lessons)

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.title:
            errors.append("Module title is required")
        return errors


@dataclass
class Course:
    """A complete course with modules and lessons."""
    course_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    short_description: str = ""
    instructor_id: str = ""
    instructor_name: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    status: CourseStatus = CourseStatus.DRAFT
    modules: List[str] = field(default_factory=list)
    thumbnail_url: Optional[str] = None
    price: float = 0.0
    currency: str = "USD"
    enrollment_count: int = 0
    rating: float = 0.0
    rating_count: int = 0
    estimated_hours: float = 0.0
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    published_at: Optional[datetime] = None
    language: str = "en"
    subtitle_languages: List[str] = field(default_factory=list)

    @property
    def is_published(self) -> bool:
        return self.status == CourseStatus.PUBLISHED

    @property
    def total_modules(self) -> int:
        return len(self.modules)

    @property
    def average_rating(self) -> float:
        return self.rating

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.title:
            errors.append("Course title is required")
        if not self.description:
            errors.append("Course description is required")
        if not self.instructor_id:
            errors.append("Instructor is required")
        if self.price < 0:
            errors.append("Price cannot be negative")
        return errors


@dataclass
class Quiz:
    """A quiz or assessment."""
    quiz_id: str = field(default_factory=lambda: str(uuid4()))
    course_id: str = ""
    module_id: Optional[str] = None
    lesson_id: Optional[str] = None
    title: str = ""
    description: str = ""
    questions: List[Dict[str, Any]] = field(default_factory=list)
    passing_score: float = 70.0
    time_limit_minutes: int = 30
    max_attempts: int = 3
    is_randomized: bool = False
    show_correct_answers: bool = True
    assessment_type: AssessmentType = AssessmentType.MULTIPLE_CHOICE
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def question_count(self) -> int:
        return len(self.questions)

    @property
    def total_points(self) -> int:
        return sum(q.get("points", 1) for q in self.questions)

    def add_question(
        self,
        question_text: str,
        options: List[str],
        correct_index: int,
        points: int = 1,
        explanation: str = "",
    ) -> str:
        question_id = f"q_{len(self.questions) + 1}"
        self.questions.append({
            "id": question_id,
            "question": question_text,
            "options": options,
            "correct_index": correct_index,
            "points": points,
            "explanation": explanation,
        })
        return question_id


@dataclass
class Enrollment:
    """A learner's enrollment in a course."""
    enrollment_id: str = field(default_factory=lambda: str(uuid4()))
    course_id: str = ""
    learner_id: str = ""
    status: LearnerProgress = LearnerProgress.NOT_STARTED
    progress_percent: float = 0.0
    completed_lessons: List[str] = field(default_factory=list)
    last_activity_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    enrolled_at: datetime = field(default_factory=datetime.now)
    time_spent_minutes: int = 0
    streak_days: int = 0
    last_streak_date: Optional[datetime] = None
    final_grade: Optional[float] = None

    @property
    def is_complete(self) -> bool:
        return self.status == LearnerProgress.COMPLETED

    @property
    def days_since_activity(self) -> int:
        if not self.last_activity_at:
            return (datetime.now() - self.enrolled_at).days
        return (datetime.now() - self.last_activity_at).days


@dataclass
class QuizAttempt:
    """A single quiz attempt by a learner."""
    attempt_id: str = field(default_factory=lambda: str(uuid4()))
    quiz_id: str = ""
    learner_id: str = ""
    answers: Dict[str, int] = field(default_factory=dict)
    score: float = 0.0
    total_points: int = 0
    percentage: float = 0.0
    passed: bool = False
    time_taken_seconds: int = 0
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    feedback: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Certificate:
    """A completion certificate."""
    certificate_id: str = field(default_factory=lambda: str(uuid4()))
    learner_id: str = ""
    course_id: str = ""
    learner_name: str = ""
    course_name: str = ""
    instructor_name: str = ""
    status: CertificateStatus = CertificateStatus.PENDING
    issued_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    certificate_number: str = ""
    final_grade: Optional[float] = None
    completion_date: Optional[datetime] = None
    verification_url: str = ""

    @property
    def is_valid(self) -> bool:
        if self.status != CertificateStatus.ISSUED:
            return False
        if self.expires_at and datetime.now() > self.expires_at:
            return False
        return True


@dataclass
class Achievement:
    """A gamification achievement."""
    achievement_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    icon_url: str = ""
    points: int = 0
    criteria: Dict[str, Any] = field(default_factory=dict)
    is_hidden: bool = False
    rarity: str = "common"

    RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]


@dataclass
class LearnerProfile:
    """Comprehensive learner profile with analytics."""
    learner_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    email: str = ""
    preferred_style: LearningStyle = LearningStyle.VISUAL
    difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER
    enrollments: List[str] = field(default_factory=list)
    completed_courses: int = 0
    total_time_minutes: int = 0
    achievements: List[str] = field(default_factory=list)
    streak_days: int = 0
    points: int = 0
    skill_levels: Dict[str, float] = field(default_factory=dict)
    learning_goals: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_active_at: Optional[datetime] = None

    @property
    def average_progress(self) -> float:
        return self.points / max(self.completed_courses, 1)

    def update_skill(self, skill: str, score: float) -> None:
        current = self.skill_levels.get(skill, 0.0)
        self.skill_levels[skill] = current * 0.7 + score * 0.3


@dataclass
class LearningPath:
    """An optimized learning path for a learner."""
    path_id: str = field(default_factory=lambda: str(uuid4()))
    learner_id: str = ""
    course_id: str = ""
    modules_order: List[str] = field(default_factory=list)
    estimated_duration_hours: float = 0.0
    checkpoints: List[Dict[str, Any]] = field(default_factory=list)
    adaptive_rules: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class EngagementMetrics:
    """Learner engagement data."""
    learner_id: str = ""
    course_id: str = ""
    total_sessions: int = 0
    total_time_minutes: int = 0
    lessons_viewed: int = 0
    lessons_completed: int = 0
    quizzes_attempted: int = 0
    average_quiz_score: float = 0.0
    forum_posts: int = 0
    peer_interactions: int = 0
    help_requests: int = 0
    last_session_at: Optional[datetime] = None
    engagement_level: EngagementLevel = EngagementLevel.MEDIUM
    computed_at: datetime = field(default_factory=datetime.now)

    @property
    def completion_rate(self) -> float:
        return self.lessons_completed / max(self.lessons_viewed, 1)

    @property
    def avg_session_minutes(self) -> float:
        return self.total_time_minutes / max(self.total_sessions, 1)


@dataclass
class SpacedRepetitionItem:
    """An item in the spaced repetition system."""
    item_id: str = field(default_factory=lambda: str(uuid4()))
    learner_id: str = ""
    content_id: str = ""
    memory_strength: float = 1.0
    ease_factor: float = 2.5
    interval_days: float = 1.0
    repetitions: int = 0
    last_review: Optional[datetime] = None
    next_review: Optional[datetime] = None

    @property
    def is_due(self) -> bool:
        if not self.next_review:
            return True
        return datetime.now() >= self.next_review

    @property
    def retention_probability(self) -> float:
        if not self.last_review or self.interval_days <= 0:
            return 1.0
        elapsed = (datetime.now() - self.last_review).total_seconds() / 86400
        return math.exp(-elapsed / self.interval_days) if self.interval_days > 0 else 0.0


# ---------------------------------------------------------------------------
# Core Engine Classes
# ---------------------------------------------------------------------------

class CourseManager:
    """Course creation, module/lesson management, and publishing."""

    def __init__(self) -> None:
        self._courses: Dict[str, Course] = {}
        self._modules: Dict[str, Module] = {}
        self._lessons: Dict[str, Lesson] = {}
        logger.info("CourseManager initialized")

    def create_course(
        self,
        title: str,
        description: str,
        instructor_id: str,
        instructor_name: str = "",
        category: str = "",
        difficulty: DifficultyLevel = DifficultyLevel.BEGINNER,
        price: float = 0.0,
    ) -> Course:
        course = Course(
            title=title,
            description=description,
            instructor_id=instructor_id,
            instructor_name=instructor_name,
            category=category,
            difficulty=difficulty,
            price=price,
        )
        self._courses[course.course_id] = course
        logger.info("Course created: %s (%s)", title, course.course_id)
        return course

    def update_course(self, course_id: str, updates: Dict[str, Any]) -> Optional[Course]:
        course = self._courses.get(course_id)
        if not course:
            return None
        for key, value in updates.items():
            if hasattr(course, key):
                setattr(course, key, value)
        course.updated_at = datetime.now()
        return course

    def get_course(self, course_id: str) -> Optional[Course]:
        return self._courses.get(course_id)

    def delete_course(self, course_id: str) -> bool:
        if course_id not in self._courses:
            return False
        del self._courses[course_id]
        return True

    def add_module(
        self, course_id: str, title: str, description: str = "", order: int = 0
    ) -> Optional[Module]:
        course = self._courses.get(course_id)
        if not course:
            return None
        module = Module(
            course_id=course_id,
            title=title,
            description=description,
            order=order,
        )
        self._modules[module.module_id] = module
        course.modules.append(module.module_id)
        course.updated_at = datetime.now()
        return module

    def add_lesson(
        self,
        module_id: str,
        title: str,
        content: str,
        lesson_type: LessonType = LessonType.TEXT,
        duration_minutes: int = 10,
        difficulty: DifficultyLevel = DifficultyLevel.BEGINNER,
    ) -> Optional[Lesson]:
        module = self._modules.get(module_id)
        if not module:
            return None
        lesson = Lesson(
            module_id=module_id,
            title=title,
            content=content,
            lesson_type=lesson_type,
            duration_minutes=duration_minutes,
            difficulty=difficulty,
            order=len(module.lessons),
        )
        self._lessons[lesson.lesson_id] = lesson
        module.lessons.append(lesson.lesson_id)
        return lesson

    def publish_course(self, course_id: str) -> bool:
        course = self._courses.get(course_id)
        if not course:
            return False
        errors = course.validate()
        if errors:
            logger.warning("Cannot publish: %s", errors)
            return False
        course.status = CourseStatus.PUBLISHED
        course.published_at = datetime.now()
        course.updated_at = datetime.now()
        return True

    def archive_course(self, course_id: str) -> bool:
        course = self._courses.get(course_id)
        if not course:
            return False
        course.status = CourseStatus.ARCHIVED
        course.updated_at = datetime.now()
        return True

    def get_course_details(self, course_id: str) -> Optional[Dict[str, Any]]:
        course = self._courses.get(course_id)
        if not course:
            return None
        module_details = []
        for module_id in course.modules:
            module = self._modules.get(module_id)
            if not module:
                continue
            lesson_details = []
            for lesson_id in module.lessons:
                lesson = self._lessons.get(lesson_id)
                if lesson:
                    lesson_details.append({
                        "id": lesson.lesson_id,
                        "title": lesson.title,
                        "type": lesson.lesson_type.value,
                        "duration": lesson.duration_minutes,
                        "difficulty": lesson.difficulty.value,
                    })
            module_details.append({
                "id": module.module_id,
                "title": module.title,
                "description": module.description,
                "order": module.order,
                "lessons": lesson_details,
            })
        return {
            "course": {
                "id": course.course_id,
                "title": course.title,
                "description": course.description,
                "instructor": course.instructor_name,
                "status": course.status.value,
                "difficulty": course.difficulty.value,
                "price": course.price,
                "rating": course.rating,
                "enrollments": course.enrollment_count,
            },
            "modules": module_details,
        }

    def get_course_catalog(
        self,
        category: Optional[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
        published_only: bool = True,
    ) -> List[Dict[str, Any]]:
        courses = list(self._courses.values())
        if published_only:
            courses = [c for c in courses if c.status == CourseStatus.PUBLISHED]
        if category:
            courses = [c for c in courses if c.category == category]
        if difficulty:
            courses = [c for c in courses if c.difficulty == difficulty]
        return [
            {
                "id": c.course_id,
                "title": c.title,
                "description": c.short_description or c.description[:100],
                "instructor": c.instructor_name,
                "difficulty": c.difficulty.value,
                "price": c.price,
                "rating": c.rating,
                "enrollments": c.enrollment_count,
                "estimated_hours": c.estimated_hours,
            }
            for c in courses
        ]


class LearnerManager:
    """Learner enrollment, progress tracking, and dashboard."""

    def __init__(self, course_manager: CourseManager) -> None:
        self._enrollments: Dict[str, Enrollment] = {}
        self._learner_profiles: Dict[str, LearnerProfile] = {}
        self._course_manager = course_manager
        logger.info("LearnerManager initialized")

    def create_learner_profile(
        self, name: str, email: str, preferred_style: LearningStyle = LearningStyle.VISUAL
    ) -> LearnerProfile:
        profile = LearnerProfile(name=name, email=email, preferred_style=preferred_style)
        self._learner_profiles[profile.learner_id] = profile
        return profile

    def enroll_learner(self, course_id: str, learner_id: str) -> Optional[Enrollment]:
        course = self._course_manager.get_course(course_id)
        if not course:
            return None
        enrollment = Enrollment(course_id=course_id, learner_id=learner_id)
        self._enrollments[enrollment.enrollment_id] = enrollment
        course.enrollment_count += 1
        profile = self._learner_profiles.get(learner_id)
        if profile:
            profile.enrollments.append(enrollment.enrollment_id)
        logger.info("Learner %s enrolled in %s", learner_id, course_id)
        return enrollment

    def update_progress(
        self, enrollment_id: str, lesson_id: str, completed: bool = True
    ) -> Optional[Enrollment]:
        enrollment = self._enrollments.get(enrollment_id)
        if not enrollment:
            return None
        if enrollment.status == LearnerProgress.NOT_STARTED:
            enrollment.status = LearnerProgress.IN_PROGRESS
            enrollment.started_at = datetime.now()
        enrollment.last_activity_at = datetime.now()
        if completed and lesson_id not in enrollment.completed_lessons:
            enrollment.completed_lessons.append(lesson_id)
        enrollment.progress_percent = self._calculate_progress(enrollment)
        if enrollment.progress_percent >= 100:
            enrollment.status = LearnerProgress.COMPLETED
            enrollment.completed_at = datetime.now()
        return enrollment

    def record_time_spent(self, enrollment_id: str, minutes: int) -> None:
        enrollment = self._enrollments.get(enrollment_id)
        if enrollment:
            enrollment.time_spent_minutes += minutes
            enrollment.last_activity_at = datetime.now()

    def get_enrollment(self, enrollment_id: str) -> Optional[Enrollment]:
        return self._enrollments.get(enrollment_id)

    def get_learner_enrollments(self, learner_id: str) -> List[Enrollment]:
        return [
            e for e in self._enrollments.values()
            if e.learner_id == learner_id
        ]

    def get_learner_dashboard(self, learner_id: str) -> Dict[str, Any]:
        enrollments = self.get_learner_enrollments(learner_id)
        profile = self._learner_profiles.get(learner_id)
        in_progress = [e for e in enrollments if e.status == LearnerProgress.IN_PROGRESS]
        completed = [e for e in enrollments if e.status == LearnerProgress.COMPLETED]
        return {
            "learner_id": learner_id,
            "name": profile.name if profile else "",
            "total_enrollments": len(enrollments),
            "in_progress": len(in_progress),
            "completed": len(completed),
            "total_time_hours": round(sum(e.time_spent_minutes for e in enrollments) / 60, 1),
            "current_streak": profile.streak_days if profile else 0,
            "points": profile.points if profile else 0,
            "recent_activity": [
                {
                    "enrollment_id": e.enrollment_id,
                    "course_id": e.course_id,
                    "progress": e.progress_percent,
                    "last_activity": e.last_activity_at.isoformat() if e.last_activity_at else None,
                }
                for e in sorted(
                    enrollments,
                    key=lambda x: x.last_activity_at or datetime.min,
                    reverse=True,
                )[:5]
            ],
        }

    def _calculate_progress(self, enrollment: Enrollment) -> float:
        course = self._course_manager.get_course(enrollment.course_id)
        if not course:
            return 0.0
        total_lessons = 0
        for module_id in course.modules:
            module = self._course_manager._modules.get(module_id)
            if module:
                total_lessons += len(module.lessons)
        if total_lessons == 0:
            return 0.0
        return min(len(enrollment.completed_lessons) / total_lessons * 100, 100)


class QuizEngine:
    """Quiz creation, grading, and adaptive assessment."""

    def __init__(self) -> None:
        self._quizzes: Dict[str, Quiz] = {}
        self._attempts: Dict[str, List[QuizAttempt]] = {}
        logger.info("QuizEngine initialized")

    def create_quiz(
        self,
        title: str,
        course_id: str,
        passing_score: float = 70.0,
        time_limit_minutes: int = 30,
        max_attempts: int = 3,
    ) -> Quiz:
        quiz = Quiz(
            title=title,
            course_id=course_id,
            passing_score=passing_score,
            time_limit_minutes=time_limit_minutes,
            max_attempts=max_attempts,
        )
        self._quizzes[quiz.quiz_id] = quiz
        return quiz

    def add_question(
        self,
        quiz_id: str,
        question_text: str,
        options: List[str],
        correct_index: int,
        points: int = 1,
        explanation: str = "",
    ) -> Optional[str]:
        quiz = self._quizzes.get(quiz_id)
        if not quiz:
            return None
        return quiz.add_question(question_text, options, correct_index, points, explanation)

    def grade_quiz(
        self, quiz_id: str, learner_id: str, answers: Dict[str, int]
    ) -> Optional[QuizAttempt]:
        quiz = self._quizzes.get(quiz_id)
        if not quiz:
            return None
        attempts = self._attempts.get(quiz_id, [])
        learner_attempts = [a for a in attempts if a.learner_id == learner_id]
        if len(learner_attempts) >= quiz.max_attempts:
            return None
        total_points = quiz.total_points
        earned_points = 0
        feedback: List[Dict[str, Any]] = []
        for question in quiz.questions:
            qid = question["id"]
            user_answer = answers.get(qid)
            is_correct = user_answer == question["correct_index"]
            if is_correct:
                earned_points += question.get("points", 1)
            feedback.append({
                "question_id": qid,
                "correct": is_correct,
                "correct_answer": question["correct_index"],
                "explanation": question.get("explanation", ""),
            })
        percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            learner_id=learner_id,
            answers=answers,
            score=earned_points,
            total_points=total_points,
            percentage=round(percentage, 1),
            passed=percentage >= quiz.passing_score,
            completed_at=datetime.now(),
            feedback=feedback,
        )
        if quiz_id not in self._attempts:
            self._attempts[quiz_id] = []
        self._attempts[quiz_id].append(attempt)
        return attempt

    def get_quiz_results(self, quiz_id: str, learner_id: str) -> List[QuizAttempt]:
        attempts = self._attempts.get(quiz_id, [])
        return [a for a in attempts if a.learner_id == learner_id]

    def get_quiz_analytics(self, quiz_id: str) -> Dict[str, Any]:
        quiz = self._quizzes.get(quiz_id)
        if not quiz:
            return {"error": "Quiz not found"}
        attempts = self._attempts.get(quiz_id, [])
        if not attempts:
            return {"quiz_id": quiz_id, "total_attempts": 0}
        scores = [a.percentage for a in attempts]
        pass_rate = len([a for a in attempts if a.passed]) / len(attempts) * 100
        question_stats: Dict[str, Dict[str, Any]] = {}
        for question in quiz.questions:
            qid = question["id"]
            correct_count = 0
            total_count = 0
            for attempt in attempts:
                if qid in attempt.answers:
                    total_count += 1
                    if attempt.answers[qid] == question["correct_index"]:
                        correct_count += 1
            question_stats[qid] = {
                "correct_rate": correct_count / total_count if total_count else 0,
                "total_answers": total_count,
            }
        return {
            "quiz_id": quiz_id,
            "total_attempts": len(attempts),
            "average_score": round(sum(scores) / len(scores), 1),
            "pass_rate": round(pass_rate, 1),
            "highest_score": round(max(scores), 1),
            "lowest_score": round(min(scores), 1),
            "question_stats": question_stats,
        }


class CertificationManager:
    """Certificate generation and verification."""

    def __init__(self) -> None:
        self._certificates: Dict[str, Certificate] = {}
        logger.info("CertificationManager initialized")

    def issue_certificate(
        self,
        learner_id: str,
        course_id: str,
        learner_name: str,
        course_name: str,
        instructor_name: str,
        final_grade: Optional[float] = None,
    ) -> Certificate:
        cert = Certificate(
            learner_id=learner_id,
            course_id=course_id,
            learner_name=learner_name,
            course_name=course_name,
            instructor_name=instructor_name,
            status=CertificateStatus.ISSUED,
            issued_at=datetime.now(),
            completion_date=datetime.now(),
            final_grade=final_grade,
            certificate_number=self._generate_cert_number(),
        )
        self._certificates[cert.certificate_id] = cert
        logger.info("Certificate issued: %s", cert.certificate_number)
        return cert

    def verify_certificate(self, certificate_number: str) -> Dict[str, Any]:
        for cert in self._certificates.values():
            if cert.certificate_number == certificate_number:
                return {
                    "valid": cert.is_valid,
                    "learner_name": cert.learner_name,
                    "course_name": cert.course_name,
                    "issued_at": cert.issued_at.isoformat() if cert.issued_at else None,
                    "status": cert.status.value,
                }
        return {"valid": False, "error": "Certificate not found"}

    def revoke_certificate(self, certificate_id: str, reason: str = "") -> bool:
        cert = self._certificates.get(certificate_id)
        if not cert:
            return False
        cert.status = CertificateStatus.REVOKED
        return True

    def get_learner_certificates(self, learner_id: str) -> List[Certificate]:
        return [
            c for c in self._certificates.values()
            if c.learner_id == learner_id
        ]

    def _generate_cert_number(self) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        rand = hashlib.md5(str(uuid4()).encode()).hexdigest()[:6].upper()
        return f"CERT-{date_str}-{rand}"


class SpacedRepetitionEngine:
    """Spaced repetition system for long-term retention."""

    def __init__(self) -> None:
        self._items: Dict[str, SpacedRepetitionItem] = {}
        logger.info("SpacedRepetitionEngine initialized")

    def add_item(self, learner_id: str, content_id: str) -> SpacedRepetitionItem:
        item = SpacedRepetitionItem(
            learner_id=learner_id,
            content_id=content_id,
            next_review=datetime.now(),
        )
        self._items[item.item_id] = item
        return item

    def record_review(
        self, item_id: str, quality: int
    ) -> Optional[SpacedRepetitionItem]:
        item = self._items.get(item_id)
        if not item:
            return None
        if quality < 0 or quality > 5:
            quality = max(0, min(5, quality))
        if quality >= 4:
            if item.repetitions == 0:
                item.interval_days = 1
            elif item.repetitions == 1:
                item.interval_days = 6
            else:
                item.interval_days = item.interval_days * item.ease_factor
            item.repetitions += 1
        elif quality >= 3:
            item.interval_days = max(1, item.interval_days * 1.2)
            item.repetitions += 1
        else:
            item.repetitions = 0
            item.interval_days = 1
        item.ease_factor = max(
            1.3,
            item.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        )
        item.last_review = datetime.now()
        item.next_review = datetime.now() + timedelta(days=item.interval_days)
        item.memory_strength = min(5.0, item.memory_strength * (1 + quality * 0.2))
        return item

    def get_due_items(self, learner_id: str) -> List[SpacedRepetitionItem]:
        return [
            item for item in self._items.values()
            if item.learner_id == learner_id and item.is_due
        ]

    def get_retention_stats(self, learner_id: str) -> Dict[str, Any]:
        items = [i for i in self._items.values() if i.learner_id == learner_id]
        if not items:
            return {"total_items": 0}
        avg_strength = sum(i.memory_strength for i in items) / len(items)
        avg_ease = sum(i.ease_factor for i in items) / len(items)
        due_count = len([i for i in items if i.is_due])
        return {
            "total_items": len(items),
            "due_for_review": due_count,
            "average_memory_strength": round(avg_strength, 2),
            "average_ease_factor": round(avg_ease, 2),
        }


class LearningPathOptimizer:
    """Generates and optimizes personalized learning paths."""

    def __init__(self, course_manager: CourseManager) -> None:
        self._paths: Dict[str, LearningPath] = {}
        self._course_manager = course_manager
        logger.info("LearningPathOptimizer initialized")

    def create_learning_path(
        self,
        learner_id: str,
        course_id: str,
        learner_profile: Optional[LearnerProfile] = None,
    ) -> Optional[LearningPath]:
        course = self._course_manager.get_course(course_id)
        if not course:
            return None
        modules_order = list(course.modules)
        if learner_profile and learner_profile.difficulty_level == DifficultyLevel.BEGINNER:
            modules_order = modules_order
        checkpoints = []
        for i, module_id in enumerate(modules_order):
            module = self._course_manager._modules.get(module_id)
            if module:
                checkpoints.append({
                    "module_id": module_id,
                    "module_title": module.title,
                    "position": i + 1,
                    "type": "module_completion",
                })
        path = LearningPath(
            learner_id=learner_id,
            course_id=course_id,
            modules_order=modules_order,
            estimated_duration_hours=course.estimated_hours,
            checkpoints=checkpoints,
        )
        self._paths[path.path_id] = path
        return path

    def get_path(self, path_id: str) -> Optional[LearningPath]:
        return self._paths.get(path_id)

    def optimize_for_style(
        self, path_id: str, learning_style: LearningStyle
    ) -> Optional[LearningPath]:
        path = self._paths.get(path_id)
        if not path:
            return None
        path.adaptive_rules.append({
            "rule": "learning_style_adjustment",
            "style": learning_style.value,
            "applied_at": datetime.now().isoformat(),
        })
        return path


class GamificationEngine:
    """Gamification — achievements, points, streaks, leaderboards."""

    def __init__(self) -> None:
        self._achievements: Dict[str, Achievement] = {}
        self._earned: Dict[str, List[str]] = {}
        self._points: Dict[str, int] = {}
        logger.info("GamificationEngine initialized")

    def create_achievement(
        self,
        name: str,
        description: str,
        points: int,
        criteria: Dict[str, Any],
        rarity: str = "common",
    ) -> Achievement:
        achievement = Achievement(
            name=name,
            description=description,
            points=points,
            criteria=criteria,
            rarity=rarity,
        )
        self._achievements[achievement.achievement_id] = achievement
        return achievement

    def award_achievement(self, learner_id: str, achievement_id: str) -> bool:
        achievement = self._achievements.get(achievement_id)
        if not achievement:
            return False
        if learner_id not in self._earned:
            self._earned[learner_id] = []
        if achievement_id in self._earned[learner_id]:
            return False
        self._earned[learner_id].append(achievement_id)
        self._points[learner_id] = self._points.get(learner_id, 0) + achievement.points
        return True

    def add_points(self, learner_id: str, points: int, action: GamificationAction) -> None:
        self._points[learner_id] = self._points.get(learner_id, 0) + points

    def get_leaderboard(self, top_n: int = 10) -> List[Dict[str, Any]]:
        sorted_learners = sorted(
            self._points.items(), key=lambda x: x[1], reverse=True
        )
        return [
            {"rank": i + 1, "learner_id": lid, "points": pts}
            for i, (lid, pts) in enumerate(sorted_learners[:top_n])
        ]

    def get_learner_achievements(self, learner_id: str) -> List[Dict[str, Any]]:
        earned_ids = self._earned.get(learner_id, [])
        return [
            {
                "achievement_id": aid,
                "name": self._achievements[aid].name,
                "description": self._achievements[aid].description,
                "points": self._achievements[aid].points,
                "rarity": self._achievements[aid].rarity,
            }
            for aid in earned_ids
            if aid in self._achievements
        ]

    def get_learner_points(self, learner_id: str) -> int:
        return self._points.get(learner_id, 0)


class AnalyticsReporting:
    """Educational analytics and reporting."""

    def __init__(
        self,
        course_manager: CourseManager,
        learner_manager: LearnerManager,
        quiz_engine: QuizEngine,
    ) -> None:
        self._course_manager = course_manager
        self._learner_manager = learner_manager
        self._quiz_engine = quiz_engine
        self._engagement_data: Dict[str, EngagementMetrics] = {}
        logger.info("AnalyticsReporting initialized")

    def get_course_analytics(self, course_id: str) -> Dict[str, Any]:
        course = self._course_manager.get_course(course_id)
        if not course:
            return {"error": "Course not found"}
        enrollments = [
            e for e in self._learner_manager._enrollments.values()
            if e.course_id == course_id
        ]
        completed = [e for e in enrollments if e.status == LearnerProgress.COMPLETED]
        in_progress = [e for e in enrollments if e.status == LearnerProgress.IN_PROGRESS]
        avg_progress = (
            sum(e.progress_percent for e in enrollments) / len(enrollments)
            if enrollments else 0
        )
        avg_time = (
            sum(e.time_spent_minutes for e in enrollments) / len(enrollments)
            if enrollments else 0
        )
        return {
            "course_id": course_id,
            "course_title": course.title,
            "total_enrollments": len(enrollments),
            "active_learners": len(in_progress),
            "completed": len(completed),
            "completion_rate": round(len(completed) / max(len(enrollments), 1) * 100, 1),
            "average_progress": round(avg_progress, 1),
            "average_time_minutes": round(avg_time, 1),
            "rating": course.rating,
            "rating_count": course.rating_count,
        }

    def get_learner_analytics(self, learner_id: str) -> Dict[str, Any]:
        enrollments = self._learner_manager.get_learner_enrollments(learner_id)
        profile = self._learner_manager._learner_profiles.get(learner_id)
        total_time = sum(e.time_spent_minutes for e in enrollments)
        completed = [e for e in enrollments if e.status == LearnerProgress.COMPLETED]
        avg_progress = (
            sum(e.progress_percent for e in enrollments) / len(enrollments)
            if enrollments else 0
        )
        return {
            "learner_id": learner_id,
            "name": profile.name if profile else "",
            "total_enrollments": len(enrollments),
            "completed_courses": len(completed),
            "total_time_hours": round(total_time / 60, 1),
            "average_progress": round(avg_progress, 1),
            "preferred_style": profile.preferred_style.value if profile else "unknown",
            "skill_levels": profile.skill_levels if profile else {},
            "points": profile.points if profile else 0,
        }

    def get_platform_overview(self) -> Dict[str, Any]:
        all_enrollments = list(self._learner_manager._enrollments.values())
        all_courses = list(self._course_manager._courses.values())
        return {
            "total_courses": len(all_courses),
            "published_courses": len([c for c in all_courses if c.is_published]),
            "total_enrollments": len(all_enrollments),
            "total_learners": len(self._learner_manager._learner_profiles),
            "overall_completion_rate": round(
                len([e for e in all_enrollments if e.status == LearnerProgress.COMPLETED])
                / max(len(all_enrollments), 1) * 100, 1
            ),
            "average_course_rating": round(
                sum(c.rating for c in all_courses) / max(len(all_courses), 1), 1
            ),
        }

    def identify_at_risk_learners(
        self, threshold_days: int = 7
    ) -> List[Dict[str, Any]]:
        at_risk: List[Dict[str, Any]] = []
        for enrollment in self._learner_manager._enrollments.values():
            if enrollment.status != LearnerProgress.IN_PROGRESS:
                continue
            if enrollment.days_since_activity >= threshold_days:
                at_risk.append({
                    "enrollment_id": enrollment.enrollment_id,
                    "learner_id": enrollment.learner_id,
                    "course_id": enrollment.course_id,
                    "days_inactive": enrollment.days_since_activity,
                    "progress": enrollment.progress_percent,
                })
        return sorted(at_risk, key=lambda x: x["days_inactive"], reverse=True)


# ---------------------------------------------------------------------------
# Main Agent Orchestrator
# ---------------------------------------------------------------------------

class EducationAgent:
    """Top-level orchestrator for all education operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._course_manager = CourseManager()
        self._learner_manager = LearnerManager(self._course_manager)
        self._quiz_engine = QuizEngine()
        self._cert_manager = CertificationManager()
        self._spaced_rep = SpacedRepetitionEngine()
        self._path_optimizer = LearningPathOptimizer(self._course_manager)
        self._gamification = GamificationEngine()
        self._analytics = AnalyticsReporting(
            self._course_manager, self._learner_manager, self._quiz_engine
        )
        logger.info("EducationAgent initialized")

    @property
    def course_manager(self) -> CourseManager:
        return self._course_manager

    @property
    def learner_manager(self) -> LearnerManager:
        return self._learner_manager

    @property
    def quiz_engine(self) -> QuizEngine:
        return self._quiz_engine

    @property
    def cert_manager(self) -> CertificationManager:
        return self._cert_manager

    @property
    def spaced_repetition(self) -> SpacedRepetitionEngine:
        return self._spaced_rep

    @property
    def path_optimizer(self) -> LearningPathOptimizer:
        return self._path_optimizer

    @property
    def gamification(self) -> GamificationEngine:
        return self._gamification

    @property
    def analytics(self) -> AnalyticsReporting:
        return self._analytics

    def create_course_with_content(
        self,
        title: str,
        description: str,
        instructor_id: str,
        modules_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        course = self._course_manager.create_course(
            title=title,
            description=description,
            instructor_id=instructor_id,
        )
        for mod_data in modules_data:
            module = self._course_manager.add_module(
                course.course_id,
                title=mod_data["title"],
                description=mod_data.get("description", ""),
            )
            if module:
                for lesson_data in mod_data.get("lessons", []):
                    self._course_manager.add_lesson(
                        module.module_id,
                        title=lesson_data["title"],
                        content=lesson_data.get("content", ""),
                        lesson_type=LessonType(lesson_data.get("type", "text")),
                        duration_minutes=lesson_data.get("duration", 10),
                    )
        self._course_manager.publish_course(course.course_id)
        return {
            "course_id": course.course_id,
            "title": course.title,
            "modules": len(course.modules),
            "status": course.status.value,
        }

    def get_education_dashboard(self) -> Dict[str, Any]:
        platform = self._analytics.get_platform_overview()
        at_risk = self._analytics.identify_at_risk_learners()
        leaderboard = self._gamification.get_leaderboard()
        return {
            "platform": platform,
            "at_risk_learners": len(at_risk),
            "top_learners": leaderboard[:10],
            "generated_at": datetime.now().isoformat(),
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "EducationAgent",
            "courses": len(self._course_manager._courses),
            "modules": len(self._course_manager._modules),
            "lessons": len(self._course_manager._lessons),
            "enrollments": len(self._learner_manager._enrollments),
            "quizzes": len(self._quiz_engine._quizzes),
            "certificates": len(self._cert_manager._certificates),
        }


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    print("=== Education Agent Demo ===")
    agent = EducationAgent()

    course = agent.course_manager.create_course(
        title="Python Programming Basics",
        description="Learn Python from scratch",
        instructor_id="inst_001",
        instructor_name="Dr. Smith",
        category="Programming",
        difficulty=DifficultyLevel.BEGINNER,
    )

    module = agent.course_manager.add_module(course.course_id, "Getting Started", "Introduction to Python")
    lesson1 = agent.course_manager.add_lesson(
        module.module_id, "What is Python?", "Python is a programming language...", LessonType.VIDEO, 15
    )
    lesson2 = agent.course_manager.add_lesson(
        module.module_id, "Setting Up", "Install Python...", LessonType.TEXT, 10
    )

    agent.course_manager.publish_course(course.course_id)
    print(f"Course published: {course.title}")

    profile = agent.learner_manager.create_learner_profile("Alice", "alice@example.com")
    enrollment = agent.learner_manager.enroll_learner(course.course_id, profile.learner_id)
    agent.learner_manager.update_progress(enrollment.enrollment_id, lesson1.lesson_id)
    agent.learner_manager.update_progress(enrollment.enrollment_id, lesson2.lesson_id)

    dashboard = agent.learner_manager.get_learner_dashboard(profile.learner_id)
    print(f"Alice progress: {dashboard['completed']} courses completed")

    quiz = agent.quiz_engine.create_quiz("Python Basics Quiz", course.course_id)
    agent.quiz_engine.add_question(quiz.quiz_id, "What is Python?", ["Language", "Snake", "Game"], 0, 10)
    attempt = agent.quiz_engine.grade_quiz(quiz.quiz_id, profile.learner_id, {"q_1": 0})
    print(f"Quiz score: {attempt.percentage}%, Passed: {attempt.passed}")

    cert = agent.cert_manager.issue_certificate(
        profile.learner_id, course.course_id, "Alice", course.title, "Dr. Smith"
    )
    verification = agent.cert_manager.verify_certificate(cert.certificate_number)
    print(f"Certificate valid: {verification['valid']}")

    agent.gamification.award_achievement(profile.learner_id, "first_course")
    points = agent.gamification.get_learner_points(profile.learner_id)

    edu_dashboard = agent.get_education_dashboard()
    print(f"Platform courses: {edu_dashboard['platform']['total_courses']}")

    status = agent.get_status()
    print(f"Agent status: {status}")


if __name__ == "__main__":
    main()
