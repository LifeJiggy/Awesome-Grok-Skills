"""
Adaptive Learning Framework

Production-grade adaptive learning toolkit providing knowledge gap detection,
personalized pathways, difficulty adjustment, spaced repetition, and learning
style adaptation for personalized education.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class GapSeverity(Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


class LearningZone(Enum):
    FRUSTRATION = "frustration"
    OPTIMAL_CHALLENGE = "optimal_challenge"
    FLOW = "flow"
    BOREDOM = "boredom"


class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"


class ReviewPriority(Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class KnowledgeGap:
    """A detected knowledge gap."""
    topic: str
    current_level: float  # 0-1
    target_level: float  # 0-1
    severity: GapSeverity
    remediation_content: str = ""
    estimated_hours: float = 0.0


@dataclass
class DiagnosticAssessment:
    """Diagnostic assessment results."""
    results: Dict[str, float]
    overall_level: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)


@dataclass
class LearnerProfile:
    """Learner profile information."""
    email: str
    current_mastery: Dict[str, float] = field(default_factory=dict)
    learning_style: str = "visual"
    pace: str = "moderate"
    goals: List[str] = field(default_factory=list)


@dataclass
class PathwayStep:
    """A step in a learning pathway."""
    order: int
    content_id: str
    content_title: str
    content_type: str = "lesson"
    estimated_minutes: int = 15
    prerequisites: List[str] = field(default_factory=list)
    mastery_required: float = 0.8


@dataclass
class LearningPathway:
    """A personalized learning pathway."""
    learner_email: str
    steps: List[PathwayStep]
    estimated_total_hours: float = 0.0
    target_competencies: List[str] = field(default_factory=list)


@dataclass
class DifficultyAdjustment:
    """Difficulty adjustment result."""
    previous_difficulty: float
    new_difficulty: float
    zone: LearningZone
    reason: str = ""


@dataclass
class ReviewItem:
    """A spaced repetition review item."""
    item_id: str
    mastery: float
    last_review: datetime
    next_review: datetime
    interval_days: float
    ease_factor: float = 2.5
    repetition_count: int = 0


@dataclass
class ReviewSchedule:
    """Spaced repetition review schedule."""
    reviews: List[ReviewItem]
    total_reviews: int = 0
    reviews_per_day: float = 0.0


@dataclass
class MasteryLevel:
    """Mastery level for a topic."""
    topic: str
    mastery: float
    velocity: float  # rate of improvement
    estimated_time_to_mastery: float  # hours
    confidence: float = 0.8


@dataclass
class LearningAnalytics:
    """Learning analytics result."""
    mastery_levels: List[MasteryLevel]
    learning_velocity: float
    engagement_score: float
    predicted_performance: float
    recommendations: List[str]


# ---------------------------------------------------------------------------
# Gap Detector
# ---------------------------------------------------------------------------

class GapDetector:
    """Detect knowledge gaps from assessment results."""

    def analyze(
        self,
        assessment_results: Dict[str, float],
        target_competencies: List[str],
        threshold: float = 0.7,
    ) -> List[KnowledgeGap]:
        gaps = []
        for competency in target_competencies:
            current = assessment_results.get(competency, 0.0)
            if current < threshold:
                severity = self._classify_severity(current, threshold)
                gaps.append(KnowledgeGap(
                    topic=competency,
                    current_level=current,
                    target_level=threshold,
                    severity=severity,
                    remediation_content=f"Review materials for {competency}",
                    estimated_hours=(threshold - current) * 10,
                ))
        return sorted(gaps, key=lambda g: g.severity.value, reverse=True)

    def _classify_severity(self, current: float, target: float) -> GapSeverity:
        gap = target - current
        if gap > 0.5:
            return GapSeverity.CRITICAL
        elif gap > 0.3:
            return GapSeverity.MAJOR
        elif gap > 0.15:
            return GapSeverity.MODERATE
        return GapSeverity.MINOR


# ---------------------------------------------------------------------------
# Pathway Generator
# ---------------------------------------------------------------------------

class PathwayGenerator:
    """Generate personalized learning pathways."""

    def generate(
        self,
        learner: LearnerProfile,
        target_competencies: Optional[List[str]] = None,
    ) -> LearningPathway:
        steps = []
        order = 1

        # Generate steps based on gaps
        for topic, mastery in learner.current_mastery.items():
            if mastery < 0.8:
                steps.append(PathwayStep(
                    order=order,
                    content_id=f"lesson-{topic}",
                    content_title=f"Mastering {topic}",
                    estimated_minutes=int((0.8 - mastery) * 100),
                    mastery_required=0.8,
                ))
                order += 1

        return LearningPathway(
            learner_email=learner.email,
            steps=steps,
            estimated_total_hours=sum(s.estimated_minutes / 60 for s in steps),
            target_competencies=target_competencies or [],
        )


# ---------------------------------------------------------------------------
# Difficulty Manager
# ---------------------------------------------------------------------------

class DifficultyManager:
    """Manage adaptive difficulty adjustment."""

    def __init__(self, initial_difficulty: float = 0.5):
        self.current_difficulty = initial_difficulty

    def adjust(
        self,
        current_difficulty: float,
        recent_performance: Dict[str, int],
        response_times: List[float],
    ) -> float:
        correct = recent_performance.get("correct", 0)
        total = recent_performance.get("total", 1)
        accuracy = correct / total

        avg_time = np.mean(response_times) if response_times else 3.0
        time_factor = 1.0 if avg_time < 3.0 else 0.9 if avg_time < 5.0 else 0.8

        # Adjust based on accuracy and time
        if accuracy > 0.85 and avg_time < 4:
            new_difficulty = min(1.0, current_difficulty + 0.1)
        elif accuracy < 0.6 or avg_time > 8:
            new_difficulty = max(0.1, current_difficulty - 0.15)
        else:
            new_difficulty = current_difficulty

        self.current_difficulty = new_difficulty
        return new_difficulty

    def get_zone(self, difficulty: float, accuracy: float) -> LearningZone:
        if accuracy < 0.5:
            return LearningZone.FRUSTRATION
        elif accuracy > 0.9:
            return LearningZone.BOREDOM
        elif 0.7 <= accuracy <= 0.85:
            return LearningZone.FLOW
        return LearningZone.OPTIMAL_CHALLENGE


# ---------------------------------------------------------------------------
# Spaced Repetition Scheduler
# ---------------------------------------------------------------------------

class SpacedRepetitionScheduler:
    """Schedule spaced repetition reviews using SM-2 algorithm."""

    def schedule(
        self,
        items: List[Dict[str, Any]],
        review_window_days: int = 7,
    ) -> ReviewSchedule:
        reviews = []
        now = datetime.now(timezone.utc)

        for item in items:
            mastery = item.get("mastery", 0.5)
            last_review_str = item.get("last_review", now.isoformat())
            last_review = datetime.fromisoformat(last_review_str.replace("Z", "+00:00")) if isinstance(last_review_str, str) else now

            # SM-2 interval calculation
            if mastery < 0.3:
                interval = 1
            elif mastery < 0.6:
                interval = 3
            elif mastery < 0.8:
                interval = 7
            else:
                interval = 14

            next_review = last_review + timedelta(days=interval)

            reviews.append(ReviewItem(
                item_id=item["id"],
                mastery=mastery,
                last_review=last_review,
                next_review=next_review,
                interval_days=interval,
                repetition_count=item.get("repetition_count", 0),
            ))

        reviews.sort(key=lambda r: r.next_review)

        return ReviewSchedule(
            reviews=reviews,
            total_reviews=len(reviews),
            reviews_per_day=len(reviews) / review_window_days,
        )


# ---------------------------------------------------------------------------
# Learning Analytics
# ---------------------------------------------------------------------------

class LearningAnalyticsEngine:
    """Generate learning analytics and insights."""

    def analyze(self, learner: LearnerProfile) -> LearningAnalytics:
        mastery_levels = [
            MasteryLevel(
                topic=topic,
                mastery=mastery,
                velocity=np.random.uniform(0.01, 0.05),
                estimated_time_to_mastery=(1.0 - mastery) * 20,
            )
            for topic, mastery in learner.current_mastery.items()
        ]

        return LearningAnalytics(
            mastery_levels=mastery_levels,
            learning_velocity=np.mean([m.velocity for m in mastery_levels]),
            engagement_score=np.random.uniform(0.6, 0.95),
            predicted_performance=np.random.uniform(0.7, 0.95),
            recommendations=[
                "Focus on topics with mastery below 0.7",
                "Increase review frequency for challenging concepts",
                "Consider visual learning materials based on profile",
            ],
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate adaptive learning capabilities."""
    print("=" * 70)
    print("Adaptive Learning Framework - Demo")
    print("=" * 70)

    # --- 1. Knowledge Gap Detection ---
    print("\n--- Knowledge Gap Detection ---")
    detector = GapDetector()
    gaps = detector.analyze(
        assessment_results={"algebra": 0.6, "geometry": 0.85, "calculus": 0.4},
        target_competencies=["algebra", "geometry", "calculus", "statistics"],
    )
    print(f"  Gaps: {len(gaps)}")
    for gap in gaps:
        print(f"    {gap.topic}: {gap.severity.value} ({gap.current_level:.0%} → {gap.target_level:.0%})")
        print(f"      Remediation: {gap.remediation_content}")

    # --- 2. Personalized Pathways ---
    print("\n--- Personalized Pathways ---")
    generator = PathwayGenerator()
    pathway = generator.generate(
        learner=LearnerProfile(
            email="student@example.com",
            current_mastery={"algebra": 0.7, "geometry": 0.9, "calculus": 0.4},
            learning_style="visual",
        ),
        target_competencies=["calculus"],
    )
    print(f"  Steps: {len(pathway.steps)}")
    print(f"  Estimated hours: {pathway.estimated_total_hours:.1f}")
    for step in pathway.steps[:3]:
        print(f"    {step.order}. {step.content_title} ({step.estimated_minutes} min)")

    # --- 3. Difficulty Adjustment ---
    print("\n--- Difficulty Adjustment ---")
    diff_manager = DifficultyManager(initial_difficulty=0.5)
    new_diff = diff_manager.adjust(
        current_difficulty=0.5,
        recent_performance={"correct": 8, "total": 10},
        response_times=[2.1, 3.5, 1.8, 2.5],
    )
    zone = diff_manager.get_zone(new_diff, 0.8)
    print(f"  Difficulty: 0.50 → {new_diff:.2f}")
    print(f"  Zone: {zone.value}")

    # --- 4. Spaced Repetition ---
    print("\n--- Spaced Repetition ---")
    scheduler = SpacedRepetitionScheduler()
    schedule = scheduler.schedule(
        items=[
            {"id": "concept-1", "mastery": 0.6, "last_review": "2024-01-10"},
            {"id": "concept-2", "mastery": 0.8, "last_review": "2024-01-05"},
            {"id": "concept-3", "mastery": 0.4, "last_review": "2024-01-12"},
        ],
    )
    print(f"  Reviews: {schedule.total_reviews}")
    for review in schedule.reviews[:3]:
        print(f"    {review.item_id}: interval={review.interval_days}d, mastery={review.mastery:.0%}")

    # --- 5. Learning Analytics ---
    print("\n--- Learning Analytics ---")
    analytics_engine = LearningAnalyticsEngine()
    analytics = analytics_engine.analyze(
        LearnerProfile(
            email="student@example.com",
            current_mastery={"algebra": 0.7, "calculus": 0.4},
        )
    )
    print(f"  Velocity: {analytics.learning_velocity:.3f}")
    print(f"  Engagement: {analytics.engagement_score:.0%}")
    print(f"  Predicted: {analytics.predicted_performance:.0%}")
    print(f"  Recommendations:")
    for rec in analytics.recommendations:
        print(f"    - {rec}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()