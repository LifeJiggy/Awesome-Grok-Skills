"""Certification Prep Agent - Technical Certification Guidance."""

import asyncio
import json
import logging
import math
import os
import random
import re
import smtplib
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)


# ---------------------------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------------------------

class CertificationDomain(Enum):
    CLOUD = "cloud"
    DATA = "data"
    SECURITY = "security"
    DEVELOPMENT = "development"
    DEVOPS = "devops"
    NETWORKING = "networking"
    PROJECT_MANAGEMENT = "project_management"


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ResourceType(Enum):
    COURSE = "course"
    BOOK = "book"
    LAB = "lab"
    PRACTICE_TEST = "practice_test"
    DOCUMENTATION = "documentation"
    VIDEO = "video"
    PODCAST = "podcast"
    WORKSHOP = "workshop"


DEFAULT_STUDY_HOURS_PER_WEEK = 10
MIN_PRACTICE_QUESTIONS = 5
MAX_PRACTICE_QUESTIONS = 50
DEFAULT_RETENTION_DAYS = 90
PASS_THRESHOLD = 0.70
SMTP_DEFAULT_PORT = 587


class Config:
    """Configuration container for the agent and its runtime."""

    def __init__(
        self,
        default_domain: Optional[CertificationDomain] = None,
        default_difficulty: Optional[DifficultyLevel] = None,
        study_hours_per_week: int = DEFAULT_STUDY_HOURS_PER_WEEK,
        retention_days: int = DEFAULT_RETENTION_DAYS,
        storage_path: Optional[str] = None,
        verbose: bool = False,
        enable_notifications: bool = False,
        smtp_host: Optional[str] = None,
        smtp_port: int = SMTP_DEFAULT_PORT,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
        notification_email: Optional[str] = None,
        session_tracking: bool = True,
        competency_assessment: bool = True,
    ) -> None:
        self.default_domain = default_domain
        self.default_difficulty = default_difficulty or DifficultyLevel.INTERMEDIATE
        self.study_hours_per_week = study_hours_per_week
        self.retention_days = retention_days
        self.storage_path = storage_path or str(
            Path(__file__).with_name("certification_prep_data")
        )
        self.verbose = verbose
        self.enable_notifications = enable_notifications
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.notification_email = notification_email
        self.session_tracking = session_tracking
        self.competency_assessment = competency_assessment
        self._created_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "default_domain": (
                self.default_domain.value if self.default_domain else None
            ),
            "default_difficulty": self.default_difficulty.value,
            "study_hours_per_week": self.study_hours_per_week,
            "retention_days": self.retention_days,
            "storage_path": self.storage_path,
            "verbose": self.verbose,
            "enable_notifications": self.enable_notifications,
            "smtp_host": self.smtp_host,
            "smtp_port": self.smtp_port,
            "notification_email": self.notification_email,
            "session_tracking": self.session_tracking,
            "competency_assessment": self.competency_assessment,
            "created_at": self._created_at,
        }

    def __repr__(self) -> str:
        return f"Config({self.to_dict()})"


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class StudyPlan:
    """Representation of a generated study plan."""

    plan_id: str
    certification: str
    timeline_weeks: int
    topic: str
    difficulty: DifficultyLevel
    weekly_hours: float
    total_hours: float
    domains: List[str]
    schedule: List[str] = field(default_factory=list)
    milestones: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=datetime.utcnow().isoformat)
    updated_at: str = field(default_factory=datetime.utcnow().isoformat)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["difficulty"] = self.difficulty.value
        return data


@dataclass
class PracticeQuestion:
    """A single practice exam question."""

    question_id: str
    topic: str
    domain: str
    difficulty: DifficultyLevel
    text: str
    options: List[str]
    correct_index: int
    explanation: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=datetime.utcnow().isoformat)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["difficulty"] = self.difficulty.value
        data["correct_option"] = self.options[self.correct_index]
        return data


@dataclass
class ResourceRecommendation:
    """Structured representation of a curated resource."""

    resource_id: str
    resource_type: str
    name: str
    url: Optional[str] = None
    description: str = ""
    estimated_hours: float = 0.0
    priority: int = 5
    tags: List[str] = field(default_factory=list)
    rating: float = 0.0
    review_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProgressMetric:
    """Snapshot of learning progress for a given certification."""

    plan_id: str
    certification: str
    completion_percentage: float
    topics_completed: int
    topics_total: int
    practice_questions_answered: int
    practice_accuracy: float
    hours_studied: float
    current_streak: int
    last_activity: str = field(default_factory=datetime.utcnow().isoformat)
    confidence_score: float = 0.0
    weak_domains: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExamDomain:
    """Definition of an exam domain and its weight."""

    name: str
    weight: float
    topics: List[str]
    sub_domains: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CertificationRoute:
    """High-level description of a certification path."""

    certification_id: str
    display_name: str
    issuing_body: str
    domains: List[ExamDomain]
    prerequisites: List[str]
    recommended_experience: str
    typical_timeline_weeks: int
    difficulty: DifficultyLevel
    exam_format: str = "Multiple choice"
    exam_duration_minutes: int = 120
    passing_score: float = PASS_THRESHOLD
    registration_fee: Optional[float] = None
    validity_months: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["difficulty"] = self.difficulty.value
        return data


@dataclass
class EnrollmentRecord:
    """Tracks user enrollment status across certifications."""

    enrollment_id: str
    user_id: str
    certification: str
    plan_id: str
    status: str
    started_on: str
    target_date: str
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StudySession:
    """Tracks a single study session for analytics."""

    session_id: str
    plan_id: str
    started_at: str
    ended_at: Optional[str] = None
    duration_minutes: float = 0.0
    topics_covered: List[str] = field(default_factory=list)
    questions_answered: int = 0
    correct_answers: int = 0
    notes: str = ""
    mood_rating: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NotificationRecord:
    """Record of a sent notification."""

    notification_id: str
    recipient: str
    subject: str
    body: str
    sent_at: str
    status: str = "sent"
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CompetencyAssessment:
    """Assessment of user competency across topics."""

    assessment_id: str
    plan_id: str
    certification: str
    topic_scores: Dict[str, float]
    overall_score: float
    strong_areas: List[str]
    weak_areas: List[str]
    recommended_focus: List[str]
    assessed_at: str = field(default_factory=datetime.utcnow().isoformat)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Helper Classes (single Responsibility)
# ---------------------------------------------------------------------------

class ValidationUtils:
    """Static validation helpers for agent inputs."""

    @staticmethod
    def validate_plan_id(plan_id: str) -> str:
        if not plan_id or not isinstance(plan_id, str):
            raise ValueError("plan_id must be a non-empty string")
        if not re.match(r"^[a-zA-Z0-9_-]+$", plan_id):
            raise ValueError(
                "plan_id must contain only alphanumeric, underscore or hyphen characters"
            )
        return plan_id

    @staticmethod
    def validate_timeline(timeline: str) -> int:
        if not timeline or not isinstance(timeline, str):
            raise ValueError("timeline must be a non-empty string")
        m = re.search(r"^(\d+)\s*-(month|week|year)s?$", timeline, re.IGNORECASE)
        if not m:
            raise ValueError(
                f"Unable to parse timeline string: {timeline!r}. "
                "Expected format: '<integer>-<unit>' (e.g. '3-months', '12-weeks')."
            )
        value, unit = int(m.group(1)), m.group(2).lower()
        if value <= 0:
            raise ValueError("Timeline value must be a positive integer")
        multipliers = {"week": 1, "month": 4, "year": 52}
        weeks = value * multipliers[unit]
        if weeks > 520:
            raise ValueError("Timeline exceeds maximum of 10 years (520 weeks)")
        return weeks

    @staticmethod
    def validate_count(count: int, minimum: int = MIN_PRACTICE_QUESTIONS,
                       maximum: int = MAX_PRACTICE_QUESTIONS) -> int:
        if not isinstance(count, int):
            raise TypeError("count must be an integer")
        if count < minimum or count > maximum:
            raise ValueError(
                f"count must be between {minimum} and {maximum}, got {count}"
            )
        return count

    @staticmethod
    def validate_accuracy(accuracy: float) -> float:
        if not isinstance(accuracy, (int, float)):
            raise TypeError("accuracy must be a float")
        return max(0.0, min(float(accuracy), 1.0))

    @staticmethod
    def validate_non_negative(value: Union[int, float], name: str) -> Union[int, float]:
        if value < 0:
            raise ValueError(f"{name} must be non-negative, got {value}")
        return value


class StudyPlanGenerator:
    """Generate structured study plans for a given certification."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def build_plan(
        self,
        certification: str,
        timeline: str,
        topic: Optional[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
    ) -> StudyPlan:
        """Build a StudyPlan model from user parameters.

        Parameters
        ----------
        certification:
            Identifier for the certification (for example, ``"aws-saa"``).
        timeline:
            Human-readable timeline (for example, ``"3-months"``).
        topic:
            Optional specific topic to focus on.
        difficulty:
            Override the default difficulty level from **config**.

        Returns
        -------
        StudyPlan
            Fully populated study plan data structure.
        """
        parsed_timeline = self._parse_timeline(timeline)
        effective_difficulty = difficulty or self.config.default_difficulty
        plan_id = f"plan-{certification}-{int(time.time())}"

        weekly_hours = self.config.study_hours_per_week
        total_hours = round(weekly_hours * parsed_timeline, 2)

        domains = self._resolve_domains(certification)
        schedule = self._generate_schedule(parsed_timeline, domains)
        milestones = self._generate_milestones(parsed_timeline, certification)

        metadata = {
            "timeline_source": timeline,
            "domain_weights": {d.name: d.weight for d in domains},
            "session_count_estimate": parsed_timeline * 5,
        }

        return StudyPlan(
            plan_id=plan_id,
            certification=certification,
            timeline_weeks=parsed_timeline,
            topic=topic or certification,
            difficulty=effective_difficulty,
            weekly_hours=weekly_hours,
            total_hours=total_hours,
            domains=[d.name for d in domains],
            schedule=schedule,
            milestones=milestones,
            metadata=metadata,
        )

    # -- internal helpers --

    @staticmethod
    def _parse_timeline(timeline: str) -> int:
        """Convert strings like '3-months' or '6-weeks' into weeks."""
        return ValidationUtils.validate_timeline(timeline)

    def _resolve_domains(self, certification: str) -> List[ExamDomain]:
        """Return default domains used by the plan generator."""
        return [
            ExamDomain(
                name="Core Concepts",
                weight=0.30,
                topics=[f"{certification}-fundamentals", f"{certification}-overview"],
                sub_domains=["Definitions", "Principles", "Architecture"],
            ),
            ExamDomain(
                name="Implementation",
                weight=0.40,
                topics=[f"{certification}-practical", f"{certification}-hands-on"],
                sub_domains=["Setup", "Configuration", "Deployment", "Testing"],
            ),
            ExamDomain(
                name="Troubleshooting",
                weight=0.20,
                topics=[f"{certification}-debug", f"{certification}-common-issues"],
                sub_domains=["Logging", "Monitoring", "Incident Response"],
            ),
            ExamDomain(
                name="Best Practices",
                weight=0.10,
                topics=[f"{certification}-patterns", f"{certification}-standards"],
                sub_domains=["Security", "Optimization", "Governance"],
            ),
        ]

    def _generate_schedule(
        self, weeks: int, domains: List[ExamDomain]
    ) -> List[str]:
        items: List[str] = []
        week_cursor = 1
        for domain in domains:
            domain_weeks = max(1, int(weeks * domain.weight))
            end = min(week_cursor + domain_weeks, weeks + 1)
            while week_cursor < end:
                for topic in domain.topics[:2]:
                    items.append(f"Week {week_cursor}: {topic}")
                week_cursor += 1
        return items

    @staticmethod
    def _generate_milestones(weeks: int, certification: str) -> List[str]:
        return [
            f"Week {weeks // 4}: Initial knowledge check ({certification})",
            f"Week {weeks // 2}: Mid-point assessment ({certification})",
            f"Week {weeks - 1}: Final mock exam ({certification})",
            f"Week {weeks}: Certification exam date",
        ]


class QuestionBank:
    """Generates and filters practice exam questions."""

    QUESTION_TEMPLATES: Dict[str, List[str]] = {
        "cloud": [
            "Which service is best suited for {feature} in {provider}?",
            "What is the primary benefit of {concept}?",
            "Select the correct configuration for {scenario}.",
            "Which pricing model applies to {resource}?",
            "What is the recommended approach for {task}?",
        ],
        "data": [
            "What is the primary advantage of using {tool}?",
            "Which query returns {insight} from {source}?",
            "What normalization form eliminates {anomaly}?",
            "Which indexing strategy improves {operation}?",
            "What is the purpose of {component} in a pipeline?",
        ],
        "security": [
            "Which control mitigates {threat}?",
            "What is the primary purpose of {mechanism}?",
            "Which compliance framework addresses {requirement}?",
            "What type of attack exploits {vulnerability}?",
            "Which encryption standard protects {asset}?",
        ],
        "development": [
            "Which pattern is best for {scenario}?",
            "What is the time complexity of {algorithm}?",
            "Which language feature supports {paradigm}?",
            "What does the {concept} principle state?",
            "Which testing strategy validates {condition}?",
        ],
        "devops": [
            "Which tool automates {task}?",
            "What is the purpose of {component} in a CI pipeline?",
            "Which strategy minimises {risk} during deployment?",
            "What does {metric} indicate in monitoring?",
            "Which practice improves {outcome}?",
        ],
        "networking": [
            "Which protocol handles {operation}?",
            "What is the primary function of {device}?",
            "Which OSI layer is responsible for {function}?",
            "What does {acronym} stand for?",
            "Which topology minimises {issue}?",
        ],
        "default": [
            "What is the main purpose of {concept}?",
            "Which option describes {topic} most accurately?",
            "How would you troubleshoot {issue}?",
            "Which pattern is used for {scenario}?",
            "What are the key benefits of {practice}?",
        ],
    }

    def __init__(self, config: Config) -> None:
        self.config = config
        self._question_history: List[str] = []

    def generate(
        self,
        topic: str,
        count: int = 10,
        difficulty: Optional[DifficultyLevel] = None,
        seed: Optional[int] = None,
        domain_weights: Optional[Dict[str, float]] = None,
    ) -> List[PracticeQuestion]:
        """Generate *count* practice questions for *topic*.

        Parameters
        ----------
        topic:
            Subject area (for example, ``"aws-saa"`` or ``"python-data"``).
        count:
            Number of questions to return, clamped to
            ``MIN_PRACTICE_QUESTIONS`` – ``MAX_PRACTICE_QUESTIONS``.
        difficulty:
            Target difficulty; defaults to ``config.default_difficulty``.
        seed:
            Optional random seed for reproducibility.
        domain_weights:
            Optional mapping of domain to weight for distribution control.

        Returns
        -------
        List[PracticeQuestion]
        """
        if seed is not None:
            random.seed(seed)
        count = max(MIN_PRACTICE_QUESTIONS, min(count, MAX_PRACTICE_QUESTIONS))
        effective_difficulty = difficulty or self.config.default_difficulty
        base_templates = self._pick_templates(topic)

        questions: List[PracticeQuestion] = []
        for idx in range(count):
            template = random.choice(base_templates)
            filled = self._fill_template(template, topic)
            options = self._make_options(topic, idx)
            correct_index = random.randint(0, len(options) - 1)
            domain = self._guess_domain(topic)
            tag_set = {topic, effective_difficulty.value, domain.lower()}
            question = PracticeQuestion(
                question_id=f"{topic}-q{idx+1:03d}",
                topic=topic,
                domain=domain,
                difficulty=effective_difficulty,
                text=filled,
                options=options,
                correct_index=correct_index,
                explanation=self._default_explanation(topic, idx, domain),
                tags=sorted(tag_set),
            )
            questions.append(question)
            self._question_history.append(question.question_id)
        return questions

    # -- internal helpers --

    @staticmethod
    def _pick_templates(topic: str) -> List[str]:
        topic_lower = topic.lower()
        for key, templates in QuestionBank.QUESTION_TEMPLATES.items():
            if key in topic_lower and key != "default":
                return templates
        return QuestionBank.QUESTION_TEMPLATES["default"]

    @staticmethod
    def _fill_template(template: str, topic: str) -> str:
        placeholders = re.findall(r"\{(\w+)\}", template)
        glossary = {
            "feature": "high availability",
            "provider": "AWS",
            "concept": topic,
            "scenario": f"{topic} deployment",
            "resource": f"{topic} resource",
            "task": f"deploying {topic}",
            "tool": topic,
            "insight": "aggregated metrics",
            "source": f"{topic} dataset",
            "anomaly": "update anomalies",
            "operation": f"{topic} lookups",
            "component": f"{topic} orchestrator",
            "topic": topic,
            "issue": f"{topic} degradation",
            "practice": f"{topic} best practices",
            "threat": "unauthorised access",
            "mechanism": "encryption",
            "requirement": "data protection",
            "vulnerability": "buffer overflow",
            "asset": "sensitive data",
            "algorithm": "binary search",
            "paradigm": "functional programming",
            "condition": "edge cases",
            "task": "build automation",
            "metric": "latency",
            "risk": "downtime",
            "outcome": "reliability",
            "device": "router",
            "function": "routing",
            "acronym": "TCP",
            "issue": "packet loss",
        }
        for ph in placeholders:
            replacement = glossary.get(ph, ph)
            template = template.replace("{" + ph + "}", replacement)
        return template

    @staticmethod
    def _make_options(topic: str, seed_offset: int) -> List[str]:
        base = [
            f"Use managed service for {topic}",
            f"Build custom {topic} solution",
            f"Outsource {topic} to third party",
            f"Defer {topic} implementation",
            "None of the above",
        ]
        random.shuffle(base)
        return base[: random.randint(3, 5)]

    @staticmethod
    def _guess_domain(topic: str) -> str:
        mapping = {
            "aws": "Cloud",
            "gcp": "Cloud",
            "azure": "Cloud",
            "python": "Development",
            "data": "Data",
            "sec": "Security",
            "network": "Networking",
            "docker": "DevOps",
            "k8s": "DevOps",
            "terraform": "DevOps",
        }
        for key, val in mapping.items():
            if key in topic.lower():
                return val
        return "General"

    @staticmethod
    def _default_explanation(topic: str, idx: int, domain: str) -> str:
        return (
            f"Review {topic} documentation focusing on {domain.lower()} concepts. "
            f"Practice hands-on labs and review common exam scenarios for question {idx + 1}."
        )

    def get_history(self) -> List[str]:
        """Return all generated question IDs."""
        return list(self._question_history)

    def clear_history(self) -> None:
        """Reset question generation history."""
        self._question_history.clear()


class ResourceCurator:
    """Curates and ranks learning resources for a certification."""

    RESOURCE_DATABASE: Dict[str, List[Dict[str, Any]]] = {
        "aws-saa": [
            {"type": "course", "name": "AWS Certified Solutions Architect Course", "platform": "Udemy", "hours": 18, "priority": 1},
            {"type": "book", "name": "AWS Certified Solutions Architect Official Study Guide", "hours": 20, "priority": 2},
            {"type": "lab", "name": "AWS Skill Builder", "hours": 12, "priority": 2},
            {"type": "practice_test", "name": "AWS Official Practice Exam", "hours": 2, "priority": 3},
            {"type": "video", "name": "AWS Training and Certification Videos", "hours": 8, "priority": 4},
        ],
        "gcp-data": [
            {"type": "course", "name": "Google Cloud Data Engineer Learning Path", "platform": "Coursera", "hours": 24, "priority": 1},
            {"type": "lab", "name": "Google Cloud Skills Boost", "hours": 15, "priority": 2},
            {"type": "book", "name": "Google Cloud Professional Data Engineer Guide", "hours": 18, "priority": 3},
        ],
        "python-dev": [
            {"type": "course", "name": "Python Developer Bootcamp", "platform": "edX", "hours": 16, "priority": 1},
            {"type": "book", "name": "Python Cookbook", "hours": 22, "priority": 2},
            {"type": "documentation", "name": "Python Official Documentation", "hours": 8, "priority": 3},
        ],
        "ccna": [
            {"type": "course", "name": "CCNA Complete Guide", "platform": "Udemy", "hours": 25, "priority": 1},
            {"type": "lab", "name": "Cisco Packet Tracer Labs", "hours": 20, "priority": 1},
            {"type": "book", "name": "CCNA Official Cert Guide", "hours": 28, "priority": 2},
        ],
        "default": [
            {"type": "course", "name": "General Certification Prep Course", "platform": "Udemy", "hours": 14, "priority": 1},
            {"type": "book", "name": "Official Certification Study Guide", "hours": 18, "priority": 2},
            {"type": "practice_test", "name": "Practice Exam Set", "hours": 3, "priority": 3},
        ],
    }

    def __init__(self, config: Config) -> None:
        self.config = config

    def recommend(
        self,
        certification: str,
        max_resources: int = 5,
        min_priority: int = 1,
        resource_types: Optional[List[str]] = None,
    ) -> List[ResourceRecommendation]:
        """Return ranked resource recommendations.

        Parameters
        ----------
        certification:
            Target certification identifier.
        max_resources:
            Maximum number of items to return.
        min_priority:
            Only return resources with priority >= this value.
        resource_types:
            Optional filter to only include specific resource types.

        Returns
        -------
        List[ResourceRecommendation]
        """
        candidates = self.RESOURCE_DATABASE.get(
            certification, self.RESOURCE_DATABASE["default"]
        )
        results: List[ResourceRecommendation] = []
        for idx, item in enumerate(candidates, start=1):
            if item.get("priority", 5) < min_priority:
                continue
            if resource_types and item.get("type") not in resource_types:
                continue
            rec = ResourceRecommendation(
                resource_id=f"{certification}-res-{idx:02d}",
                resource_type=item["type"],
                name=item["name"],
                url=item.get("url"),
                description=item.get("description", ""),
                estimated_hours=item.get("hours", 0.0),
                priority=item.get("priority", idx),
                tags=[certification, item.get("platform", "generic")],
                rating=item.get("rating", 0.0),
                review_count=item.get("review_count", 0),
            )
            results.append(rec)
            if len(results) >= max_resources:
                break
        return results

    def add_resource(
        self,
        certification: str,
        resource_type: str,
        name: str,
        url: Optional[str] = None,
        estimated_hours: float = 0.0,
        description: str = "",
        priority: int = 5,
        rating: float = 0.0,
        platform: str = "custom",
    ) -> None:
        """Dynamically register a new resource for *certification*."""
        self.RESOURCE_DATABASE.setdefault(certification, []).append(
            {
                "type": resource_type,
                "name": name,
                "url": url,
                "description": description,
                "hours": estimated_hours,
                "priority": priority,
                "rating": rating,
                "platform": platform,
            }
        )

    def get_catalogue(self) -> Dict[str, List[str]]:
        """Return summary of available certification catalogues."""
        return {cert: [r["name"] for r in items]
                for cert, items in self.RESOURCE_DATABASE.items()}


class ProgressTracker:
    """Tracks and updates progress metrics for a given study plan."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._records: Dict[str, ProgressMetric] = {}
        self._history_log: List[Tuple[str, str]] = []

    def update(
        self,
        plan_id: str,
        certification: str,
        topics_completed: int,
        topics_total: int,
        practice_questions_answered: int,
        practice_accuracy: float,
        hours_studied: float,
        current_streak: int,
    ) -> ProgressMetric:
        """Create or refresh a ProgressMetric for *plan_id*."""
        completion_pct = self._compute_completion(
            topics_completed, topics_total, practice_accuracy
        )
        confidence = self._estimate_confidence(
            topics_completed, topics_total, practice_accuracy
        )
        weak = self._identify_weak_domains(practice_accuracy, 0.0)
        metric = ProgressMetric(
            plan_id=plan_id,
            certification=certification,
            completion_percentage=round(completion_pct, 2),
            topics_completed=topics_completed,
            topics_total=topics_total,
            practice_questions_answered=practice_questions_answered,
            practice_accuracy=round(practice_accuracy, 4),
            hours_studied=round(hours_studied, 2),
            current_streak=current_streak,
            confidence_score=round(confidence, 4),
            weak_domains=weak,
        )
        self._records[plan_id] = metric
        self._history_log.append((plan_id, datetime.utcnow().isoformat()))
        return metric

    def get(self, plan_id: str) -> Optional[ProgressMetric]:
        """Return the latest progress metric for *plan_id*, if present."""
        return self._records.get(plan_id)

    def history(self, plan_id: str) -> List[ProgressMetric]:
        """Return recorded progress snapshots (read-only view)."""
        return [self._records[plan_id]] if plan_id in self._records else []

    def get_all_plan_ids(self) -> List[str]:
        """Return all tracked plan identifiers."""
        return list(self._records.keys())

    def delete(self, plan_id: str) -> bool:
        """Remove progress data for *plan_id*. Returns True if removed."""
        if plan_id in self._records:
            del self._records[plan_id]
            return True
        return False

    # -- internal helpers --

    @staticmethod
    def _compute_completion(
        topics_completed: int,
        topics_total: int,
        practice_accuracy: float,
    ) -> float:
        topic_ratio = topics_completed / max(topics_total, 1)
        accuracy_component = ValidationUtils.validate_accuracy(practice_accuracy) * 0.4
        return min(100.0, (topic_ratio * 0.6) + accuracy_component * 100.0) if topic_ratio <= 1.0 else 100.0

    @staticmethod
    def _estimate_confidence(topics_completed: int, topics_total: int,
                             practice_accuracy: float) -> float:
        completion = ProgressTracker._compute_completion(
            topics_completed, topics_total, practice_accuracy
        ) / 100.0
        days_factor = 1.0
        return min(1.0, completion * days_factor)

    @staticmethod
    def _identify_weak_domains(practice_accuracy: float, threshold: float = 0.6) -> List[str]:
        if practice_accuracy < threshold:
            return ["General"]
        return []


class AnalyticsEngine:
    """Aggregates raw metrics and produces analytical outputs."""

    def __init__(self, tracker: ProgressTracker) -> None:
        self.tracker = tracker

    def summary_for(self, plan_id: str) -> Dict[str, Any]:
        metric = self.tracker.get(plan_id)
        if metric is None:
            raise KeyError(f"No progress data for plan_id {plan_id}")
        hours_spent = metric.hours_studied
        remaining = max(metric.topics_total - metric.topics_completed, 0)
        hours_per_topic = hours_spent / max(metric.topics_completed, 1)
        return {
            "plan_id": plan_id,
            "certification": metric.certification,
            "completion_percentage": metric.completion_percentage,
            "topics_remaining": remaining,
            "estimated_hours_remaining": round(
                remaining * hours_per_topic, 2
            ),
            "practice_accuracy": metric.practice_accuracy,
            "current_streak": metric.current_streak,
            "confidence_score": metric.confidence_score,
            "weak_domains": metric.weak_domains,
            "recent_activities": self.tracker.history(plan_id),
            "hours_per_topic_avg": round(hours_per_topic, 2),
        }

    def rank_resources(
        self,
        recommendations: List[ResourceRecommendation],
        rating_fn: Optional[Callable[[ResourceRecommendation], float]] = None,
    ) -> List[ResourceRecommendation]:
        if rating_fn is None:
            rating_fn = lambda r: (6 - r.priority) + (r.estimated_hours / 10) + (r.rating / 2.0)
        return sorted(recommendations, key=lambda r: (rating_fn(r), r.priority))

    def learning_velocity(self, plan_id: str) -> Dict[str, float]:
        """Estimate topics per hour and hours per week."""
        metric = self.tracker.get(plan_id)
        if metric is None or metric.hours_studied == 0:
            return {"topics_per_hour": 0.0, "hours_per_week": 0.0}
        return {
            "topics_per_hour": round(metric.topics_completed / metric.hours_studied, 4),
            "hours_per_week": round(metric.hours_studied / max(1, metric.current_streak / 7.0), 2),
        }


class ScheduleOptimizer:
    """Optimizes study schedules around user constraints."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def optimize(
        self,
        plan: StudyPlan,
        unavailable: List[str],
        preferred_days: List[str] = None,
        session_length_hours: float = 1.5,
        max_sessions_per_day: int = 2,
    ) -> List[Dict[str, Any]]:
        """Return an optimized weekly schedule.

        Parameters
        ----------
        plan:
            Base study plan.
        unavailable:
            Day names the user cannot study (e.g. ``["Sunday"]``).
        preferred_days:
            Days the user prefers (defaults to weekdays).
        session_length_hours:
            Length of each study session in hours.
        max_sessions_per_day:
            Maximum study sessions per day.

        Returns
        -------
        List[Dict[str, Any]]
            Each entry is a dictionary describing a study session.
        """
        preferred_days = preferred_days or [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        ]
        available_days = [d for d in preferred_days if d not in unavailable]
        if not available_days:
            available_days = preferred_days[:1]

        sessions: List[Dict[str, Any]] = []
        current_week = 1
        week_hours_used = 0.0
        week_capacity = self.config.study_hours_per_week
        day_session_count: Dict[str, int] = {}

        for entry in plan.schedule:
            day_match = re.match(r"Week (\d+): (.+)", entry)
            if not day_match:
                continue
            week_num = int(day_match.group(1))
            topic = day_match.group(2)
            day_of_week = self._select_day(
                week_num, available_days, day_session_count, max_sessions_per_day
            )
            sessions.append({
                "week": week_num,
                "day": day_of_week,
                "topic": topic,
                "duration_hours": session_length_hours,
            })
            day_session_count[day_of_week] = day_session_count.get(day_of_week, 0) + 1
            week_hours_used += session_length_hours
            if week_hours_used >= week_capacity and week_num != current_week:
                current_week = week_num
                week_hours_used = 0.0
                day_session_count.clear()
        return sessions

    @staticmethod
    def _select_day(week_num: int, available_days: List[str],
                    day_session_count: Dict[str, int],
                    max_per_day: int) -> str:
        candidates = [d for d in available_days if day_session_count.get(d, 0) < max_per_day]
        if not candidates:
            candidates = available_days
        return candidates[(week_num - 1) % len(candidates)]


class MockExamSimulator:
    """Simulates a timed mock exam environment."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._exam_history: List[Dict[str, Any]] = []

    def run(
        self,
        questions: List[PracticeQuestion],
        time_limit_minutes: int = 60,
        shuffle: bool = True,
        domain_weights: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """Simulate an exam and return a result summary.

        Parameters
        ----------
        questions:
            Pool of questions to draw from.
        time_limit_minutes:
            Virtual budget for the exam.
        shuffle:
            Whether to shuffle the question order.
        domain_weights:
            Optional weights for domain distribution.

        Returns
        -------
        Dict[str, Any]
            Score, pass/fail status, and per-topic breakdown.
        """
        pool = list(questions)
        if shuffle:
            random.shuffle(pool)
        min_q, max_q = 20, 45
        selected = pool[: random.randint(min_q, max_q)]
        correct_count = 0
        topic_breakdown: Dict[str, Dict[str, int]] = {}
        for q in selected:
            user_choice = random.randint(0, len(q.options) - 1)
            is_correct = user_choice == q.correct_index
            if is_correct:
                correct_count += 1
            topic_breakdown.setdefault(q.domain, {"correct": 0, "total": 0})
            topic_breakdown[q.domain]["total"] += 1
            topic_breakdown[q.domain]["correct"] += int(is_correct)
        score = correct_count / len(selected) if selected else 0.0
        passed = score >= PASS_THRESHOLD
        result = {
            "total_questions": len(selected),
            "correct": correct_count,
            "score": round(score, 4),
            "pass": passed,
            "time_limit_minutes": time_limit_minutes,
            "topic_breakdown": topic_breakdown,
        }
        self._exam_history.append(result)
        return result

    def get_history(self) -> List[Dict[str, Any]]:
        """Return history of simulated exams."""
        return list(self._exam_history)


class StudyNoteGenerator:
    """Generates study notes from practice questions and resources."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def generate_notes(
        self,
        questions: List[PracticeQuestion],
        resources: List[ResourceRecommendation],
        output_path: Optional[str] = None,
        title: str = "Study Notes",
    ) -> str:
        """Produce a Markdown study note document.

        Parameters
        ----------
        questions:
            Practice questions to reference in notes.
        resources:
            Curated resources to list.
        output_path:
            Optional path to persist notes to disk.
        title:
            Document title.

        Returns
        -------
        str
            Markdown content.
        """
        lines: List[str] = [f"# {title}", ""]
        lines.append("## Key Concepts")
        seen = set()
        for q in questions:
            if q.domain not in seen:
                seen.add(q.domain)
                lines.append(f"- **{q.domain}**: core topics and patterns")
        lines.append("")
        lines.append("## Recommended Resources")
        for r in resources:
            url = r.url if r.url else "#"
            lines.append(f"- {r.resource_type.title()}: [{r.name}]({url}) "
                         f"(~{r.estimated_hours}h, priority {r.priority})")
        lines.append("")
        lines.append("## Practice Questions Summary")
        for q in questions[:10]:
            lines.append(f"### {q.question_id}")
            lines.append(q.text)
            for opt_idx, opt in enumerate(q.options):
                lines.append(f"- {chr(65+opt_idx)}. {opt}")
            lines.append(f"> **Explanation**: {q.explanation}")
            lines.append("")
        content = "\n".join(lines)
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return content


class ExamStrategyAdvisor:
    """Provides high-level strategy advice for certification exams."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def strategy_for(self, certification: str, days_remaining: int) -> Dict[str, Any]:
        """Return a study strategy given *days_remaining* until exam date.

        Returns
        -------
        Dict[str, Any]
            Recommended actions, focus ratio, and rest guidance.
        """
        days_remaining = max(days_remaining, 0)
        if days_remaining > 60:
            focus = "Foundation building"
            actions = [
                "Review official exam guide",
                "Complete foundational courses",
                "Build a hands-on lab environment",
                "Join community discussions",
                "Create a structured study plan",
                "Identify weak areas early",
            ]
        elif days_remaining > 14:
            focus = "Intensive practice"
            actions = [
                "Take practice exams daily",
                "Review weak domains",
                "Drill scenario-based questions",
                "Refine time management",
                "Maintain consistent study schedule",
                "Form or join a study group",
            ]
        elif days_remaining > 0:
            focus = "Exam readiness"
            actions = [
                "Take a single timed mock exam",
                "Review high-level summaries",
                "Rest and sleep adequately",
                "Gather identification and logistics",
                "Confirm test centre details",
                "Prepare materials for exam day",
            ]
        else:
            focus = "Already past exam date"
            actions = ["Review performance if exam taken", "Plan re-certification"]
        day_ratio = days_remaining / 90.0
        return {
            "certification": certification,
            "days_remaining": days_remaining,
            "focus": focus,
            "actions": actions,
            "recommended_hours_per_day": round(
                day_ratio * self.config.study_hours_per_week / 7.0, 2
            ),
            "rest_days_before": max(1, min(3, days_remaining // 10)),
            "confidence_score": round(min(day_ratio, 1.0), 2),
            "exam_readiness": "Ready" if days_remaining <= 14 and day_ratio > 0.5 else "In Progress",
        }


class CompetencyAssessor:
    """Evaluates user competency and identifies knowledge gaps."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def assess_from_questions(
        self, questions: List[PracticeQuestion], user_answers: Dict[str, int]
    ) -> CompetencyAssessment:
        """Assess competency based on question performance."""
        domain_scores: Dict[str, List[float]] = {}
        for q in questions:
            domain = q.domain
            domain_scores.setdefault(domain, []).append(
                1.0 if user_answers.get(q.question_id) == q.correct_index else 0.0
            )
        topic_scores = {d: round(sum(scores) / len(scores), 4)
                        for d, scores in domain_scores.items()}
        overall = sum(topic_scores.values()) / max(len(topic_scores), 1)
        strong = [d for d, s in topic_scores.items() if s >= 0.7]
        weak = [d for d, s in topic_scores.items() if s < 0.7]
        recommended = sorted(weak, key=lambda d: topic_scores[d])[:3]
        return CompetencyAssessment(
            assessment_id=f"assessment-{int(time.time())}",
            plan_id="",
            certification="",
            topic_scores=topic_scores,
            overall_score=round(overall, 4),
            strong_areas=strong,
            weak_areas=weak,
            recommended_focus=recommended,
        )

    def suggest_next_difficulty(
        self, recent_accuracy: float, current_difficulty: DifficultyLevel
    ) -> DifficultyLevel:
        """Suggest adjusted difficulty based on recent performance."""
        if recent_accuracy >= 0.85 and current_difficulty != DifficultyLevel.EXPERT:
            next_level = {
                DifficultyLevel.BEGINNER: DifficultyLevel.INTERMEDIATE,
                DifficultyLevel.INTERMEDIATE: DifficultyLevel.ADVANCED,
                DifficultyLevel.ADVANCED: DifficultyLevel.EXPERT,
            }.get(current_difficulty, current_difficulty)
            return next_level
        elif recent_accuracy <= 0.4 and current_difficulty != DifficultyLevel.BEGINNER:
            prev_level = {
                DifficultyLevel.INTERMEDIATE: DifficultyLevel.BEGINNER,
                DifficultyLevel.ADVANCED: DifficultyLevel.INTERMEDIATE,
                DifficultyLevel.EXPERT: DifficultyLevel.ADVANCED,
            }.get(current_difficulty, current_difficulty)
            return prev_level
        return current_difficulty


class SessionManager:
    """Tracks study sessions for a plan."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._sessions: Dict[str, StudySession] = {}
        self._active: Dict[str, str] = {}

    def start_session(self, plan_id: str, topics: Optional[List[str]] = None) -> StudySession:
        """Begin a new study session."""
        ValidationUtils.validate_plan_id(plan_id)
        if plan_id in self._active:
            raise RuntimeError(f"Session already active for plan {plan_id}")
        sessions = [s for s in self._sessions.values() if s.plan_id == plan_id]
        session_id = f"session-{plan_id}-{len(sessions)+1}-{int(time.time())}"
        session = StudySession(
            session_id=session_id,
            plan_id=plan_id,
            started_at=datetime.utcnow().isoformat(),
            topics_covered=topics or [],
        )
        self._sessions[session_id] = session
        self._active[plan_id] = session_id
        return session

    def end_session(self, plan_id: str, questions_answered: int = 0,
                    correct_answers: int = 0) -> Optional[StudySession]:
        """End the active session for a plan."""
        if plan_id not in self._active:
            return None
        session_id = self._active.pop(plan_id)
        session = self._sessions[session_id]
        session.ended_at = datetime.utcnow().isoformat()
        started = datetime.fromisoformat(session.started_at)
        ended = datetime.fromisoformat(session.ended_at)
        session.duration_minutes = (ended - started).total_seconds() / 60.0
        session.questions_answered = questions_answered
        session.correct_answers = correct_answers
        return session

    def get_session(self, session_id: str) -> Optional[StudySession]:
        """Return a specific session."""
        return self._sessions.get(session_id)

    def get_sessions_for_plan(self, plan_id: str) -> List[StudySession]:
        """Return all sessions for a plan."""
        return [s for s in self._sessions.values() if s.plan_id == plan_id]

    def get_active_session(self, plan_id: str) -> Optional[StudySession]:
        """Return the active session, if any."""
        if plan_id in self._active:
            return self._sessions.get(self._active[plan_id])
        return None


class NotificationService:
    """Sends notifications via email or other channels."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._sent: List[NotificationRecord] = []

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send an email notification. Returns True on success."""
        if not self.config.enable_notifications or not self.config.smtp_host:
            logging.debug("Notifications disabled or SMTP not configured.")
            return False
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.config.smtp_user or "agent@example.com"
            msg["To"] = recipient
            with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
                if self.config.smtp_password:
                    server.starttls()
                    server.login(self.config.smtp_user or "", self.config.smtp_password)
                server.send_message(msg)
            record = NotificationRecord(
                notification_id=f"notif-{int(time.time())}",
                recipient=recipient,
                subject=subject,
                body=body,
                sent_at=datetime.utcnow().isoformat(),
            )
            self._sent.append(record)
            return True
        except Exception as exc:
            record = NotificationRecord(
                notification_id=f"notif-{int(time.time())}",
                recipient=recipient,
                subject=subject,
                body=body,
                sent_at=datetime.utcnow().isoformat(),
                status="failed",
                error_message=str(exc),
            )
            self._sent.append(record)
            return False

    def send_milestone_reminder(self, recipient: str, certification: str, milestone: str) -> bool:
        body = (
            f"Reminder: You have an upcoming milestone '{milestone}' "
            f"for certification {certification}. Stay on track with your study plan!"
        )
        return self.send_email(recipient, f"Study Milestone: {milestone}", body)

    def get_sent_history(self) -> List[Dict[str, Any]]:
        """Return all sent notification records."""
        return [r.to_dict() for r in self._sent]


class TemplateEngine:
    """Advanced template processing for question generation."""

    def __init__(self) -> None:
        self._custom_templates: Dict[str, List[str]] = {}

    def register_templates(self, domain: str, templates: List[str]) -> None:
        """Register custom templates for a domain."""
        self._custom_templates[domain] = templates

    def render(self, template: str, context: Dict[str, str]) -> str:
        """Render a template string with the given context."""
        result = template
        for key, value in context.items():
            result = result.replace("{" + key + "}", value)
        return result

    def get_available_domains(self) -> List[str]:
        """Return all registered template domains."""
        return list(self._custom_templates.keys())


class CertificationRouteManager:
    """Manages certification route metadata."""

    ROUTE_DATABASE: Dict[str, CertificationRoute] = {
        "aws-saa": CertificationRoute(
            certification_id="aws-saa",
            display_name="AWS Certified Solutions Architect - Associate",
            issuing_body="Amazon Web Services",
            domains=[
                ExamDomain("Design Resilient Architectures", 0.30,
                           ["Reliable / Resilient / Scalable Infrastructure",
                            "Decoupling Mechanisms", "High-Performing Architectures"]),
                ExamDomain("Design High-Performing Architectures", 0.28,
                           ["Elastic and Scalable Compute", "High-Performing Storage",
                            "High-Performing Data Stores", "High-Performing Networks"]),
                ExamDomain("Design Secure Applications", 0.26,
                           ["IAM", "Encryption", "Network Security", "Data Protection"]),
                ExamDomain("Design Cost-Optimised Architectures", 0.16,
                           ["Cost-Effective Storage", "Cost-Effective Compute"]),
            ],
            prerequisites=["No formal prerequisites", "12+ months AWS experience recommended"],
            recommended_experience="1-2 years hands-on AWS experience",
            typical_timeline_weeks=12,
            difficulty=DifficultyLevel.INTERMEDIATE,
            exam_duration_minutes=130,
            passing_score=0.72,
        ),
        "gcp-data": CertificationRoute(
            certification_id="gcp-data",
            display_name="Google Cloud Professional Data Engineer",
            issuing_body="Google Cloud",
            domains=[
                ExamDomain("Design Data Processing Systems", 0.25, []),
                ExamDomain("Build and Operationalise Data Systems", 0.30, []),
                ExamDomain("Operationalise Machine Learning Models", 0.25, []),
                ExamDomain("Ensure Data Privacy and Compliance", 0.20, []),
            ],
            prerequisites=["3+ years industry experience", "1+ years GCP experience"],
            recommended_experience="Data engineering on Google Cloud",
            typical_timeline_weeks=16,
            difficulty=DifficultyLevel.ADVANCED,
        ),
        "ccna": CertificationRoute(
            certification_id="ccna",
            display_name="Cisco Certified Network Associate",
            issuing_body="Cisco",
            domains=[
                ExamDomain("Network Fundamentals", 0.20, []),
                ExamDomain("Network Access", 0.20, []),
                ExamDomain("IP Connectivity", 0.25, []),
                ExamDomain("IP Services", 0.15, []),
                ExamDomain("Security Fundamentals", 0.10, []),
                ExamDomain("Automation and Programmability", 0.10, []),
            ],
            prerequisites=["None"],
            recommended_experience="0-1 years networking experience",
            typical_timeline_weeks=8,
            difficulty=DifficultyLevel.BEGINNER,
            exam_duration_minutes=120,
            passing_score=0.825,
        ),
    }

    def __init__(self, config: Config) -> None:
        self.config = config

    def get_route(self, certification: str) -> Optional[CertificationRoute]:
        """Return a certification route by identifier."""
        return self.ROUTE_DATABASE.get(certification)

    def get_all_routes(self) -> List[CertificationRoute]:
        """Return all registered certification routes."""
        return list(self.ROUTE_DATABASE.values())

    def register_route(self, route: CertificationRoute) -> None:
        """Register a new certification route."""
        self.ROUTE_DATABASE[route.certification_id] = route


# ---------------------------------------------------------------------------
# Main Agent
# ---------------------------------------------------------------------------

class CertificationPrepAgent:
    """Primary interface for certification preparation workflows.

    This agent exposes a high-level API for study plan generation,
    practice test creation, progress tracking, resource curation and
    exam strategy advising.  Internally it delegates to specialised
    helper classes for single-responsibility logic.
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._plans: List[StudyPlan] = []
        self._plan_generator = StudyPlanGenerator(self._config)
        self._question_bank = QuestionBank(self._config)
        self._resource_curator = ResourceCurator(self._config)
        self._progress_tracker = ProgressTracker(self._config)
        self._analytics = AnalyticsEngine(self._progress_tracker)
        self._schedule_optimizer = ScheduleOptimizer(self._config)
        self._mock_simulator = MockExamSimulator(self._config)
        self._note_generator = StudyNoteGenerator(self._config)
        self._strategy_advisor = ExamStrategyAdvisor(self._config)
        self._competency_assessor = CompetencyAssessor(self._config)
        self._session_manager = SessionManager(self._config)
        self._notification_service = NotificationService(self._config)
        self._template_engine = TemplateEngine()
        self._route_manager = CertificationRouteManager(self._config)

    # -- Plan Management --

    def create_study_plan(
        self,
        certification: str,
        timeline: str,
        topic: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new study plan.

        Parameters
        ----------
        certification:
            Certification identifier.
        timeline:
            Human-readable timeline.
        topic:
            Optional focused topic.

        Returns
        -------
        Dict[str, Any]
        """
        plan = self._plan_generator.build_plan(certification, timeline, topic)
        self._plans.append(plan)
        return plan.to_dict()

    def get_plans(self) -> List[Dict[str, Any]]:
        """Return all created study plans."""
        return [p.to_dict() for p in self._plans]

    def get_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Return a single plan identified by **plan_id**."""
        ValidationUtils.validate_plan_id(plan_id)
        for p in self._plans:
            if p.plan_id == plan_id:
                return p.to_dict()
        return None

    def delete_plan(self, plan_id: str) -> bool:
        """Delete a study plan by ID. Returns True if removed."""
        ValidationUtils.validate_plan_id(plan_id)
        self._progress_tracker.delete(plan_id)
        for idx, p in enumerate(self._plans):
            if p.plan_id == plan_id:
                self._plans.pop(idx)
                return True
        return False

    # -- Exam Question Generation --

    def generate_practice_test(
        self,
        topic: str,
        count: int = 10,
        difficulty: Optional[DifficultyLevel] = None,
        seed: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Generate *count* practice questions for *topic*.

        Returns list of question dictionaries.
        """
        count = max(MIN_PRACTICE_QUESTIONS, min(count, MAX_PRACTICE_QUESTIONS))
        difficulty = difficulty or self._config.default_difficulty
        questions = self._question_bank.generate(
            topic, count=count, difficulty=difficulty, seed=seed
        )
        return [q.to_dict() for q in questions]

    def batch_generate_questions(
        self, topics: List[str], count_per_topic: int = 10
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Generate questions for multiple topics in one call."""
        result: Dict[str, List[Dict[str, Any]]] = {}
        for topic in topics:
            result[topic] = self.generate_practice_test(topic, count=count_per_topic)
        return result

    def run_mock_exam(
        self,
        topic: str,
        count: int = 20,
        time_limit_minutes: int = 60,
    ) -> Dict[str, Any]:
        """Run a simulated mock exam and return a score summary."""
        questions = self._question_bank.generate(
            topic, count=count,
        )
        return self._mock_simulator.run(
            questions, time_limit_minutes=time_limit_minutes
        )

    # -- Progress Tracking --

    def track_progress(
        self,
        plan_id: str,
        topics_completed: int = 0,
        topics_total: int = 1,
        practice_questions_answered: int = 0,
        practice_accuracy: float = 0.0,
        hours_studied: float = 0.0,
        current_streak: int = 0,
    ) -> Dict[str, Any]:
        """Update progress for a given plan and return the metric snapshot."""
        ValidationUtils.validate_plan_id(plan_id)
        if not plan_id:
            raise ValueError("plan_id must be a non-empty string")
        plan = self.get_plan(plan_id)
        if plan is None:
            raise KeyError(f"Plan {plan_id} not found")
        cert = plan["certification"]
        metric = self._progress_tracker.update(
            plan_id=plan_id,
            certification=cert,
            topics_completed=max(topics_completed, 0),
            topics_total=max(topics_total, 1),
            practice_questions_answered=max(practice_questions_answered, 0),
            practice_accuracy=ValidationUtils.validate_accuracy(practice_accuracy),
            hours_studied=max(hours_studied, 0.0),
            current_streak=max(current_streak, 0),
        )
        return metric.to_dict()

    def get_progress(self, plan_id: str) -> Dict[str, Any]:
        """Return the latest progress snapshot for **plan_id**."""
        ValidationUtils.validate_plan_id(plan_id)
        metric = self._progress_tracker.get(plan_id)
        if metric is None:
            return {"plan_id": plan_id, "status": "not_found"}
        return self._analytics.summary_for(plan_id)

    def get_learning_velocity(self, plan_id: str) -> Dict[str, float]:
        """Return learning velocity metrics."""
        return self._analytics.learning_velocity(plan_id)

    # -- Resource Curation --

    def recommend_resources(
        self, certification: str, max_resources: int = 5, resource_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Return curated resource recommendations for **certification**."""
        recs = self._resource_curator.recommend(
            certification, max_resources=max_resources, resource_types=resource_types
        )
        return [r.to_dict() for r in recs]

    # -- Scheduling & Strategy --

    def optimize_schedule(
        self,
        plan_id: str,
        unavailable: Optional[List[str]] = None,
        preferred_days: Optional[List[str]] = None,
        session_length_hours: float = 1.5,
    ) -> List[Dict[str, Any]]:
        """Return an optimized study schedule for an existing plan."""
        plan = self.get_plan(plan_id)
        if plan is None:
            raise KeyError(f"Plan {plan_id} not found")
        study_plan = StudyPlan(
            plan_id=plan["plan_id"],
            certification=plan["certification"],
            timeline_weeks=plan["timeline_weeks"],
            topic=plan["topic"],
            difficulty=DifficultyLevel(plan["difficulty"]),
            weekly_hours=plan["weekly_hours"],
            total_hours=plan["total_hours"],
            domains=plan["domains"],
            schedule=plan["schedule"],
            milestones=plan["milestones"],
            created_at=plan["created_at"],
            updated_at=plan["updated_at"],
            metadata=plan.get("metadata", {}),
        )
        return self._schedule_optimizer.optimize(
            plan=study_plan,
            unavailable=unavailable or [],
            preferred_days=preferred_days,
            session_length_hours=session_length_hours,
        )

    def exam_strategy(self, certification: str, days_remaining: int) -> Dict[str, Any]:
        """Return a high-level exam strategy."""
        return self._strategy_advisor.strategy_for(certification, days_remaining)

    # -- Notes Export --

    def export_study_notes(
        self,
        topic: str,
        output_path: Optional[str] = None,
        title: str = "Study Notes",
    ) -> str:
        """Generate and optionally persist study notes for *topic*."""
        questions = self.generate_practice_test(topic, count=20)
        resources = self.recommend_resources(topic, max_resources=10)
        return self._note_generator.generate_notes(
            questions=[
                PracticeQuestion(
                    question_id=q["question_id"],
                    topic=q["topic"],
                    domain=q["domain"],
                    difficulty=DifficultyLevel(q["difficulty"]),
                    text=q["text"],
                    options=q["options"],
                    correct_index=q["correct_index"],
                    explanation=q["explanation"],
                    tags=q.get("tags", []),
                )
                for q in questions
            ],
            resources=[
                ResourceRecommendation(
                    resource_id=r["resource_id"],
                    resource_type=r["resource_type"],
                    name=r["name"],
                    url=r.get("url"),
                    description=r.get("description", ""),
                    estimated_hours=r.get("estimated_hours", 0.0),
                    priority=r.get("priority", 5),
                    tags=r.get("tags", []),
                )
                for r in resources
            ],
            output_path=output_path,
            title=title,
        )

    # -- Session Tracking --

    def start_study_session(self, plan_id: str, topics: Optional[List[str]] = None) -> Dict[str, Any]:
        """Start tracking a study session."""
        session = self._session_manager.start_session(plan_id, topics)
        return session.to_dict()

    def end_study_session(self, plan_id: str, questions_answered: int = 0,
                          correct_answers: int = 0) -> Optional[Dict[str, Any]]:
        """End the active study session."""
        session = self._session_manager.end_session(
            plan_id, questions_answered, correct_answers
        )
        return session.to_dict() if session else None

    def get_sessions(self, plan_id: str) -> List[Dict[str, Any]]:
        """Return all sessions for a plan."""
        return [s.to_dict() for s in self._session_manager.get_sessions_for_plan(plan_id)]

    # -- Competency & Assessment --

    def assess_competency(
        self, questions: List[Dict[str, Any]], user_answers: Dict[str, int]
    ) -> Dict[str, Any]:
        """Assess competency from a set of questions and user answers."""
        q_objects = [
            PracticeQuestion(
                question_id=q["question_id"],
                topic=q["topic"],
                domain=q["domain"],
                difficulty=DifficultyLevel(q["difficulty"]),
                text=q["text"],
                options=q["options"],
                correct_index=q["correct_index"],
                explanation=q["explanation"],
            )
            for q in questions
        ]
        assessment = self._competency_assessor.assess_from_questions(
            q_objects, user_answers
        )
        return assessment.to_dict()

    def suggest_difficulty(
        self, recent_accuracy: float, current_difficulty: DifficultyLevel
    ) -> str:
        """Suggest a difficulty adjustment."""
        suggested = self._competency_assessor.suggest_next_difficulty(
            recent_accuracy, current_difficulty
        )
        return suggested.value

    # -- Notifications --

    def send_notification(self, recipient: str, subject: str, body: str) -> bool:
        """Send a notification via available channels."""
        return self._notification_service.send_email(recipient, subject, body)

    def send_milestone_reminder(self, recipient: str, certification: str,
                                milestone: str) -> bool:
        """Send a milestone reminder notification."""
        return self._notification_service.send_milestone_reminder(
            recipient, certification, milestone
        )

    # -- Certification Routes --

    def get_certification_route(self, certification: str) -> Optional[Dict[str, Any]]:
        """Return certification route metadata."""
        route = self._route_manager.get_route(certification)
        return route.to_dict() if route else None

    def list_certification_routes(self) -> List[Dict[str, Any]]:
        """Return all available certification routes."""
        return [r.to_dict() for r in self._route_manager.get_all_routes()]

    # -- Async convenience wrappers --

    async def async_generate_practice_test(
        self,
        topic: str,
        count: int = 10,
        difficulty: Optional[DifficultyLevel] = None,
    ) -> List[Dict[str, Any]]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.generate_practice_test,
            topic,
            count,
            difficulty,
        )

    async def async_recommend_resources(
        self,
        certification: str,
        max_resources: int = 5,
    ) -> List[Dict[str, Any]]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.recommend_resources,
            certification,
            max_resources,
        )

    async def async_track_progress(
        self, plan_id: str, **kwargs: Any
    ) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.track_progress, plan_id, **kwargs)

    # -- Serialization & Persistence --

    def to_json(self, plan_id: str, indent: int = 2) -> str:
        ValidationUtils.validate_plan_id(plan_id)
        plan = self.get_plan(plan_id)
        if plan is None:
            raise KeyError(f"Plan {plan_id} not found")
        metric = self._progress_tracker.get(plan_id)
        payload: Dict[str, Any] = {
            "plan": plan,
            "progress": metric.to_dict() if metric else None,
            "resources": self.recommend_resources(plan["certification"], max_resources=10),
            "sessions": self.get_sessions(plan_id),
        }
        return json.dumps(payload, indent=indent)

    def load_plans_from_path(self, path: str) -> None:
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"{path} does not exist or is not a file")
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            for entry in data:
                if "plan_id" in entry and "certification" in entry:
                    self._plans.append(StudyPlan(**{
                        k: DifficultyLevel(v) if k == "difficulty" else v
                        for k, v in entry.items()
                    }))

    def save_plans_to_path(self, path: str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = [p.to_dict() for p in self._plans]
        p.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def export_full_backup(self, path: str) -> None:
        """Export all agent state to a comprehensive backup file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        backup = {
            "plans": [p.to_dict() for p in self._plans],
            "progress": {pid: m.to_dict() for pid, m in self._progress_tracker._records.items()},
            "sessions": [s.to_dict() for s in self._session_manager._sessions.values()],
            "exam_history": self._mock_simulator.get_history(),
            "notification_history": self._notification_service.get_sent_history(),
            "exported_at": datetime.utcnow().isoformat(),
        }
        p.write_text(json.dumps(backup, indent=2), encoding="utf-8")

    # -- Status & Health --

    def get_status(self) -> Dict[str, Any]:
        """Return an overall status snapshot for the agent."""
        return {
            "agent": "CertificationPrepAgent",
            "plans": len(self._plans),
            "config": self._config.to_dict(),
            "components": [
                "StudyPlanGenerator",
                "QuestionBank",
                "ResourceCurator",
                "ProgressTracker",
                "AnalyticsEngine",
                "ScheduleOptimizer",
                "MockExamSimulator",
                "StudyNoteGenerator",
                "ExamStrategyAdvisor",
                "CompetencyAssessor",
                "SessionManager",
                "NotificationService",
                "TemplateEngine",
                "CertificationRouteManager",
            ],
            "ready": True,
        }

    def calculate_readiness(self, plan_id: str) -> Dict[str, Any]:
        """Calculate comprehensive exam readiness score."""
        metric = self._progress_tracker.get(plan_id)
        if metric is None:
            raise KeyError(f"No progress data for plan_id {plan_id}")
        base_score = metric.completion_percentage / 100.0
        accuracy_factor = metric.practice_accuracy
        streak_factor = min(metric.current_streak / 14.0, 1.0)
        readiness = round(
            (base_score * 0.4) + (accuracy_factor * 0.4) + (streak_factor * 0.2), 4
        )
        return {
            "plan_id": plan_id,
            "readiness_score": readiness,
            "status": "Ready" if readiness >= 0.75 else "In Progress",
            "breakdown": {
                "completion_weight": round(base_score * 0.4, 4),
                "accuracy_weight": round(accuracy_factor * 0.4, 4),
                "streak_weight": round(streak_factor * 0.2, 4),
            },
        }

    def import_resources(self, certification: str, file_path: str) -> int:
        """Import resources from a JSON file. Returns count imported."""
        p = Path(file_path)
        if not p.is_file():
            raise FileNotFoundError(f"{file_path} does not exist")
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array of resource objects")
        count = 0
        for item in data:
            self._resource_curator.add_resource(
                certification=certification,
                resource_type=item.get("type", "course"),
                name=item.get("name", f"Resource {count+1}"),
                url=item.get("url"),
                estimated_hours=item.get("hours", 0.0),
                description=item.get("description", ""),
                priority=item.get("priority", 5),
                platform=item.get("platform", "imported"),
            )
            count += 1
        return count

    def generate_study_roadmap(self, plan_id: str) -> Dict[str, Any]:
        """Generate a comprehensive study roadmap with weekly breakdowns."""
        plan = self.get_plan(plan_id)
        if not plan:
            raise KeyError(f"Plan {plan_id} not found")
        progress = self._progress_tracker.get(plan_id)
        roadmap = {
            "plan_id": plan_id,
            "certification": plan["certification"],
            "timeline_weeks": plan["timeline_weeks"],
            "domains": plan["domains"],
            "milestones": plan["milestones"],
            "weekly_breakdown": [],
        }
        for idx, entry in enumerate(plan["schedule"], start=1):
            roadmap["weekly_breakdown"].append({
                "week": idx,
                "activity": entry,
                "estimated_hours": plan["weekly_hours"] / len(plan["schedule"]) * 4,
            })
        if progress:
            roadmap["current_progress"] = {
                "completed_percentage": progress.completion_percentage,
                "topics_remaining": max(progress.topics_total - progress.topics_completed, 0),
            }
        return roadmap


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def _cli_demo() -> None:
    """Interactive CLI demonstration of the agent's main capabilities."""
    agent = CertificationPrepAgent()
    print("=" * 60)
    print("Certification Prep Agent - CLI Demo")
    print("=" * 60)

    status = agent.get_status()
    print(f"\n[Agent Status] plans: {status['plans']}")

    plan = agent.create_study_plan("aws-saa", "3-months")
    print("\n[Study Plan]")
    print(json.dumps(plan, indent=2))

    questions = agent.generate_practice_test("aws-saa", count=5)
    print("\n[Practice Questions (first 2)]")
    for q in questions[:2]:
        print(f"- {q['question_id']}: {q['text']}")

    resources = agent.recommend_resources("aws-saa", max_resources=3)
    print("\n[Resources]")
    for r in resources:
        print(f"- {r['resource_type'].title()}: {r['name']}")

    progress = agent.track_progress(
        plan_id=plan["plan_id"],
        topics_completed=3,
        topics_total=10,
        practice_questions_answered=25,
        practice_accuracy=0.72,
        hours_studied=12.5,
        current_streak=3,
    )
    print("\n[Progress]")
    print(json.dumps(progress, indent=2))

    analytics = agent._analytics.summary_for(plan["plan_id"])
    print("\n[Analytics Summary]")
    print(json.dumps(analytics, indent=2))

    schedule = agent.optimize_schedule(
        plan["plan_id"], unavailable=[], session_length_hours=1.5
    )
    print("\n[Optimized Schedule (first 3 entries)]")
    for entry in schedule[:3]:
        print(json.dumps(entry))

    mock_exam = agent.run_mock_exam("aws-saa", count=10, time_limit_minutes=45)
    print("\n[Mock Exam Result]")
    print(json.dumps(mock_exam, indent=2))

    strategy = agent.exam_strategy("aws-saa", days_remaining=21)
    print("\n[Exam Strategy]")
    print(json.dumps(strategy, indent=2))

    notes_path = Path(__file__).with_name("study_notes.md")
    notes = agent.export_study_notes("aws-saa", output_path=str(notes_path))
    print(f"\n[Study Notes] exported to {notes_path}")
    print(notes[:500] + "...")


def _cli_plan(args: Any) -> None:
    agent = CertificationPrepAgent(
        config=Config(verbose=getattr(args, "verbose", False))
    )
    try:
        plan = agent.create_study_plan(args.certification, args.timeline)
        print("Created plan:", plan["plan_id"])
        if getattr(args, "questions", 5) > 0:
            questions = agent.generate_practice_test(
                args.certification, count=args.questions
            )
            print(
                "Generated questions:",
                [q["question_id"] for q in questions],
            )
    except ValueError as e:
        print(f"Error: {e}")


def _cli_status(args: Any) -> None:
    agent = CertificationPrepAgent(
        config=Config(verbose=getattr(args, "verbose", False))
    )
    print(agent.get_status())


def _cli_difficulty(args: Any) -> None:
    agent = CertificationPrepAgent()
    advisor = CompetencyAssessor(Config())
    current = DifficultyLevel(args.current)
    suggested = advisor.suggest_next_difficulty(args.accuracy, current)
    print(f"Suggested difficulty: {suggested}")


def _cli_route(args: Any) -> None:
    agent = CertificationPrepAgent()
    route = agent.get_certification_route(args.certification)
    if route:
        print(f"\n{route['display_name']} ({route['issuing_body']})")
        print(f"Duration: {route['typical_timeline_weeks']} weeks")
        print(f"Passing score: {route['passing_score']:.0%}")
        print("Domains:")
        for d in route["domains"]:
            print(f"  - {d['name']} ({d['weight']:.0%})")
    else:
        print(f"No route found for {args.certification}")


def main() -> None:
    """Entry point when executed directly."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Certification Prep Agent CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    p_demo = subparsers.add_parser("demo", help="Run interactive demo")
    p_demo.add_argument("--verbose", action="store_true")

    p_plan = subparsers.add_parser("plan", help="Create a study plan")
    p_plan.add_argument("--certification", required=True, help="Target certification identifier")
    p_plan.add_argument("--timeline", default="3-months", help="Study timeline string")
    p_plan.add_argument("--questions", type=int, default=5, help="Number of practice questions")
    p_plan.add_argument("--verbose", action="store_true")

    p_status = subparsers.add_parser("status", help="Show agent status")
    p_status.add_argument("--verbose", action="store_true")

    p_diff = subparsers.add_parser("suggest-difficulty", help="Suggest difficulty adjustment")
    p_diff.add_argument("--current", required=True,
                        choices=[d.value for d in DifficultyLevel],
                        help="Current difficulty level")
    p_diff.add_argument("--accuracy", type=float, required=True, help="Recent accuracy (0.0-1.0)")

    p_route = subparsers.add_parser("route", help="Show certification route details")
    p_route.add_argument("--certification", required=True, help="Certification identifier")

    args = parser.parse_args()

    if args.verbose:
        import logging
        logging.basicConfig(level=logging.INFO)

    if args.command == "demo":
        _cli_demo()
    elif args.command == "plan":
        _cli_plan(args)
    elif args.command == "status":
        _cli_status(args)
    elif args.command == "suggest-difficulty":
        _cli_difficulty(args)
    elif args.command == "route":
        _cli_route(args)
    else:
        agent = CertificationPrepAgent(
            config=Config(verbose=getattr(args, "verbose", False))
        )
        print("Certification Prep Agent Ready")
        print(agent.get_status())


if __name__ == "__main__":
    main()
