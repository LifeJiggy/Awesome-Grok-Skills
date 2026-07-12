"""
education_access.py — Adaptive Learning & Offline-First Education Toolkit

Provides adaptive learning engines, offline content delivery, assistive learning
technologies, multilingual content management, and student progress tracking.
"""

from __future__ import annotations

import math
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict


class MasteryLevel(Enum):
    NOVICE = "novice"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"


class ContentType(Enum):
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    IMAGE = "image"


class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING = "reading"
    KINESTHETIC = "kinesthetic"


class SyncStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFLICT = "conflict"


class InterventionLevel(Enum):
    NONE = "none"
    WATCH = "watch"
    CONCERN = "concern"
    URGENT = "urgent"


@dataclass
class KnowledgeComponent:
    kc_id: str
    name: str
    subject: str
    prerequisites: list[str] = field(default_factory=list)
    difficulty: float = 0.5
    estimated_minutes: int = 30
    content_items: list[str] = field(default_factory=list)


@dataclass
class Student:
    student_id: str
    name: str
    language: str = "en"
    learning_style: LearningStyle = LearningStyle.READING
    disability_accommodations: list[str] = field(default_factory=list)
    enrollment_date: datetime = field(default_factory=datetime.now)


@dataclass
class KCMastery:
    student_id: str
    kc_id: str
    observations: list[bool] = field(default_factory=list)
    mastery_probability: float = 0.0
    last_practiced: datetime | None = None
    attempts: int = 0

    @property
    def accuracy(self) -> float:
        if not self.observations:
            return 0.0
        return sum(self.observations) / len(self.observations)

    @property
    def mastery_level(self) -> MasteryLevel:
        if self.mastery_probability >= 0.9:
            return MasteryLevel.ADVANCED
        elif self.mastery_probability >= 0.7:
            return MasteryLevel.PROFICIENT
        elif self.mastery_probability >= 0.4:
            return MasteryLevel.DEVELOPING
        return MasteryLevel.NOVICE


@dataclass
class ContentPackage:
    package_id: str
    title: str
    locale: str
    files: list[str]
    estimated_size_mb: float
    priority: int = 0
    content_type: ContentType = ContentType.TEXT
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SyncResult:
    synced_count: int
    pending_count: int
    failed_count: int
    conflicts: list[str]
    total_bytes: float


@dataclass
class LearningSession:
    session_id: str
    student_id: str
    subject: str
    duration_minutes: float
    exercises_completed: int
    correct_answers: int
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def accuracy(self) -> float:
        return self.correct_answers / self.exercises_completed if self.exercises_completed > 0 else 0.0


@dataclass
class StudentDashboard:
    student_id: str
    total_sessions: int
    total_minutes: float
    total_exercises: int
    overall_accuracy: float
    mastery_trend: list[float]
    velocity_exercises_per_hour: float
    intervention_recommended: InterventionLevel
    subjects_mastered: int
    subjects_in_progress: int


class AdaptiveLearningEngine:
    LEARNING_RATE = 0.3
    SLIP_PROBABILITY = 0.1
    GUESS_PROBABILITY = 0.2
    MASTERY_THRESHOLD = 0.7

    def __init__(self):
        self.knowledge_components: dict[str, KnowledgeComponent] = {}
        self.mastery_data: dict[str, dict[str, KCMastery]] = defaultdict(dict)

    def add_knowledge_component(self, kc: KnowledgeComponent) -> None:
        self.knowledge_components[kc.kc_id] = kc

    def _get_mastery(self, student_id: str, kc_id: str) -> KCMastery:
        if kc_id not in self.mastery_data[student_id]:
            self.mastery_data[student_id][kc_id] = KCMastery(
                student_id=student_id,
                kc_id=kc_id,
            )
        return self.mastery_data[student_id][kc_id]

    def record_observation(self, student_id: str, kc_id: str, correct: bool) -> float:
        mastery = self._get_mastery(student_id, kc_id)
        mastery.observations.append(correct)
        mastery.attempts += 1
        mastery.last_practiced = datetime.now()

        p_prior = mastery.mastery_probability
        if correct:
            p_correct_given_mastered = 1 - self.SLIP_PROBABILITY
            p_correct_given_not_mastered = self.GUESS_PROBABILITY
        else:
            p_correct_given_mastered = self.SLIP_PROBABILITY
            p_correct_given_not_mastered = 1 - self.GUESS_PROBABILITY

        p_mastered = p_prior * p_correct_given_mastered
        p_not_mastered = (1 - p_prior) * p_correct_given_not_mastered
        p_total = p_mastered + p_not_mastered

        if p_total > 0:
            p_posterior = p_mastered / p_total
        else:
            p_posterior = p_prior

        p_posterior = max(0.01, min(0.99, p_posterior))
        mastery.mastery_probability = p_posterior
        return p_posterior

    def get_mastery(self, student_id: str, kc: KnowledgeComponent) -> float:
        mastery = self._get_mastery(student_id, kc.kc_id)
        return mastery.mastery_probability

    def get_mastery_level(self, student_id: str, kc_id: str) -> MasteryLevel:
        mastery = self._get_mastery(student_id, kc_id)
        return mastery.mastery_level

    def prerequisites_met(self, student_id: str, kc: KnowledgeComponent) -> bool:
        for prereq_id in kc.prerequisites:
            prereq_mastery = self._get_mastery(student_id, prereq_id)
            if prereq_mastery.mastery_probability < self.MASTERY_THRESHOLD:
                return False
        return True

    def recommend_next(self, student_id: str) -> KnowledgeComponent | None:
        candidates = []
        for kc in self.knowledge_components.values():
            mastery = self._get_mastery(student_id, kc.kc_id)
            if mastery.mastery_probability >= self.MASTERY_THRESHOLD:
                continue
            if not self.prerequisites_met(student_id, kc):
                continue
            priority = kc.difficulty * (1 - mastery.mastery_probability)
            candidates.append((kc, priority))

        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0] if candidates else None

    def generate_learning_path(self, student_id: str, max_items: int = 10) -> list[KnowledgeComponent]:
        path: list[KnowledgeComponent] = []
        visited: set[str] = set()

        for _ in range(max_items):
            next_kc = self.recommend_next(student_id)
            if not next_kc or next_kc.kc_id in visited:
                break
            path.append(next_kc)
            visited.add(next_kc.kc_id)

        return path

    def get_student_summary(self, student_id: str) -> dict:
        kc_data = self.mastery_data.get(student_id, {})
        mastered = sum(1 for m in kc_data.values() if m.mastery_probability >= self.MASTERY_THRESHOLD)
        in_progress = sum(1 for m in kc_data.values() if 0 < m.mastery_probability < self.MASTERY_THRESHOLD)
        avg_mastery = (
            sum(m.mastery_probability for m in kc_data.values()) / len(kc_data)
            if kc_data else 0.0
        )
        return {
            "student_id": student_id,
            "total_kcs": len(kc_data),
            "mastered": mastered,
            "in_progress": in_progress,
            "average_mastery": round(avg_mastery, 3),
            "total_attempts": sum(m.attempts for m in kc_data.values()),
        }


class OfflineContentManager:
    def __init__(self, storage_path: str = "/data/content"):
        self.storage_path = storage_path
        self.packages: dict[str, ContentPackage] = {}
        self.sync_log: list[dict] = []
        self._pkg_counter = 0

    def create_package(
        self,
        title: str,
        locale: str,
        files: list[str],
        estimated_size_mb: float,
        priority: int = 0,
    ) -> ContentPackage:
        self._pkg_counter += 1
        package = ContentPackage(
            package_id=f"pkg_{self._pkg_counter}",
            title=title,
            locale=locale,
            files=files,
            estimated_size_mb=estimated_size_mb,
            priority=priority,
        )
        self.packages[package.package_id] = package
        return package

    def set_priority(self, package_id: str, priority: int) -> None:
        if package_id in self.packages:
            self.packages[package_id].priority = priority

    def sync_available_packages(
        self,
        device_id: str,
        max_bandwidth_mb: float = 50.0,
    ) -> SyncResult:
        sorted_packages = sorted(
            self.packages.values(),
            key=lambda p: p.priority,
            reverse=True,
        )

        synced = 0
        pending = 0
        failed = 0
        conflicts: list[str] = []
        total_bytes = 0.0
        bandwidth_used = 0.0

        for pkg in sorted_packages:
            size = pkg.estimated_size_mb
            if bandwidth_used + size > max_bandwidth_mb:
                pending += 1
                continue

            content_hash = hashlib.md5(f"{pkg.package_id}_{device_id}".encode()).hexdigest()
            is_conflict = content_hash.endswith(("a", "b", "c"))

            if is_conflict:
                conflicts.append(pkg.package_id)
                failed += 1
            else:
                synced += 1
                bandwidth_used += size
                total_bytes += size * 1024 * 1024

        result = SyncResult(
            synced_count=synced,
            pending_count=pending,
            failed_count=failed,
            conflicts=conflicts,
            total_bytes=total_bytes,
        )

        self.sync_log.append({
            "device_id": device_id,
            "timestamp": datetime.now().isoformat(),
            "synced": synced,
            "pending": pending,
            "failed": failed,
        })

        return result

    def get_device_storage_summary(self, device_id: str) -> dict:
        device_packages = [
            p for p in self.packages.values()
            if hashlib.md5(f"{p.package_id}_{device_id}".encode()).hexdigest()[:2] in ("ab", "cd", "ef")
        ]
        total_size = sum(p.estimated_size_mb for p in device_packages)
        return {
            "device_id": device_id,
            "packages_stored": len(device_packages),
            "total_size_mb": round(total_size, 1),
            "locales": list(set(p.locale for p in device_packages)),
        }


class ContentSimplifier:
    READING_LEVEL_THRESHOLDS = {
        "basic": 50,
        "intermediate": 100,
        "advanced": 150,
    }

    def simplify_text(self, text: str, target_level: str = "basic") -> dict:
        sentences = text.split(".")
        words = text.split()
        avg_word_length = sum(len(w) for w in words) / max(len(words), 1)

        if target_level == "basic":
            simplified = self._split_long_sentences(sentences)
            simplified = self._replace_complex_words(simplified)
        elif target_level == "intermediate":
            simplified = self._split_long_sentences(sentences)
        else:
            simplified = text

        return {
            "original": text,
            "simplified": simplified,
            "original_word_count": len(words),
            "simplified_word_count": len(simplified.split()),
            "reading_level": target_level,
        }

    def _split_long_sentences(self, sentences: list[str]) -> str:
        result = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            words = sentence.split()
            if len(words) > 20:
                mid = len(words) // 2
                result.append(" ".join(words[:mid]) + ".")
                result.append(" ".join(words[mid:]) + ".")
            else:
                result.append(sentence)
        return " ".join(result)

    def _replace_complex_words(self, text: str) -> str:
        replacements = {
            "utilize": "use",
            "demonstrate": "show",
            "approximately": "about",
            "subsequently": "then",
            "nevertheless": "but",
            "facilitate": "help",
            "commence": "start",
            "terminate": "end",
            "endeavor": "try",
            "ascertain": "find out",
        }
        for complex_word, simple_word in replacements.items():
            text = text.replace(complex_word, simple_word)
        return text

    def generate_dyslexia_friendly_format(self, text: str) -> dict:
        return {
            "font_recommendation": "OpenDyslexic or Comic Sans MS",
            "line_height": "1.5",
            "letter_spacing": "0.1em",
            "word_spacing": "0.2em",
            "background_color": "#FFF8E7",  # Cream/yellow
            "text_color": "#333333",
            "max_line_length": "70 characters",
            "paragraph_spacing": "1.5em",
            "alignment": "left",
            "formatted_text": text,
        }


class MultilingualContentManager:
    RTL_LANGUAGES = {"ar", "he", "fa", "ur", "yi", "ps", "sd", "ckb"}
    CJK_LANGUAGES = {"zh", "ja", "ko"}

    def __init__(self):
        self.content_store: dict[str, list[dict]] = defaultdict(list)
        self.translation_queue: list[dict] = []

    def add_content(
        self,
        content_id: str,
        language: str,
        text: str,
        title: str = "",
    ) -> None:
        self.content_store[content_id].append({
            "language": language,
            "text": text,
            "title": title,
            "added_at": datetime.now().isoformat(),
        })

    def request_translation(
        self,
        content_id: str,
        source_language: str,
        target_language: str,
    ) -> str:
        translation_id = f"trans_{hashlib.md5(f'{content_id}_{target_language}'.encode()).hexdigest()[:8]}"
        self.translation_queue.append({
            "translation_id": translation_id,
            "content_id": content_id,
            "source_language": source_language,
            "target_language": target_language,
            "status": "pending",
            "requested_at": datetime.now().isoformat(),
        })
        return translation_id

    def get_content(self, content_id: str, language: str) -> dict | None:
        for item in self.content_store.get(content_id, []):
            if item["language"] == language:
                return item
        fallbacks = self.content_store.get(content_id, [])
        return fallbacks[0] if fallbacks else None

    def is_rtl(self, language: str) -> bool:
        return language in self.RTL_LANGUAGES

    def get_typography_settings(self, language: str) -> dict:
        is_rtl = self.is_rtl(language)
        is_cjk = language in self.CJK_LANGUAGES
        settings = {
            "direction": "rtl" if is_rtl else "ltr",
            "text_align": "right" if is_rtl else "left",
            "font_family": "system-ui",
        }
        if is_cjk:
            settings["line_break_strict"] = True
            settings["word_break"] = "break-all"
        if is_rtl:
            settings["mirrored_icons"] = True
        return settings

    def get_translation_stats(self) -> dict:
        status_counts = defaultdict(int)
        for t in self.translation_queue:
            status_counts[t["status"]] += 1
        return {
            "total_translations": len(self.translation_queue),
            "by_status": dict(status_counts),
            "languages_served": list(set(
                item["language"]
                for items in self.content_store.values()
                for item in items
            )),
        }


class ProgressTracker:
    def __init__(self):
        self.sessions: list[LearningSession] = []
        self._session_counter = 0

    def record_session(
        self,
        student_id: str,
        subject: str,
        duration_minutes: float,
        exercises_completed: int,
        correct: int,
    ) -> LearningSession:
        self._session_counter += 1
        session = LearningSession(
            session_id=f"sess_{self._session_counter}",
            student_id=student_id,
            subject=subject,
            duration_minutes=duration_minutes,
            exercises_completed=exercises_completed,
            correct_answers=correct,
        )
        self.sessions.append(session)
        return session

    def get_student_sessions(self, student_id: str) -> list[LearningSession]:
        return [s for s in self.sessions if s.student_id == student_id]

    def get_dashboard(self, student_id: str) -> StudentDashboard:
        student_sessions = self.get_student_sessions(student_id)
        if not student_sessions:
            return StudentDashboard(
                student_id=student_id, total_sessions=0, total_minutes=0,
                total_exercises=0, overall_accuracy=0, mastery_trend=[],
                velocity_exercises_per_hour=0, intervention_recommended=InterventionLevel.NONE,
                subjects_mastered=0, subjects_in_progress=0,
            )

        total_minutes = sum(s.duration_minutes for s in student_sessions)
        total_exercises = sum(s.exercises_completed for s in student_sessions)
        total_correct = sum(s.correct_answers for s in student_sessions)

        accuracy_by_date = defaultdict(list)
        for s in student_sessions:
            day = s.timestamp.date().isoformat()
            accuracy_by_date[day].append(s.accuracy)

        mastery_trend = []
        for day in sorted(accuracy_by_date.keys()):
            day_accs = accuracy_by_date[day]
            mastery_trend.append(sum(day_accs) / len(day_accs))

        velocity = total_exercises / max(total_minutes / 60, 0.01)
        subjects = set(s.subject for s in student_sessions)

        intervention = InterventionLevel.NONE
        if len(student_sessions) >= 3:
            recent_accuracy = sum(s.accuracy for s in student_sessions[-3:]) / 3
            if recent_accuracy < 0.4:
                intervention = InterventionLevel.URGENT
            elif recent_accuracy < 0.6:
                intervention = InterventionLevel.CONCERN
            elif len(student_sessions) < 2 and total_minutes < 30:
                intervention = InterventionLevel.WATCH

        return StudentDashboard(
            student_id=student_id,
            total_sessions=len(student_sessions),
            total_minutes=round(total_minutes, 1),
            total_exercises=total_exercises,
            overall_accuracy=round(total_correct / max(total_exercises, 1), 3),
            mastery_trend=mastery_trend,
            velocity_exercises_per_hour=round(velocity, 1),
            intervention_recommended=intervention,
            subjects_mastered=0,
            subjects_in_progress=len(subjects),
        )


class ResourceMatcher:
    def __init__(self):
        self.tutors: list[dict] = []
        self.learners: list[dict] = []

    def add_tutor(
        self,
        tutor_id: str,
        name: str,
        subjects: list[str],
        languages: list[str],
        availability: list[str],
        hourly_rate: float = 0.0,
    ) -> None:
        self.tutors.append({
            "tutor_id": tutor_id,
            "name": name,
            "subjects": subjects,
            "languages": languages,
            "availability": availability,
            "hourly_rate": hourly_rate,
        })

    def add_learner(
        self,
        learner_id: str,
        name: str,
        subjects_needed: list[str],
        language: str,
        availability: list[str],
        skill_level: str = "beginner",
    ) -> None:
        self.learners.append({
            "learner_id": learner_id,
            "name": name,
            "subjects_needed": subjects_needed,
            "language": language,
            "availability": availability,
            "skill_level": skill_level,
        })

    def match(self, learner_id: str) -> list[dict]:
        learner = next((l for l in self.learners if l["learner_id"] == learner_id), None)
        if not learner:
            return []

        matches = []
        for tutor in self.tutors:
            subject_overlap = set(learner["subjects_needed"]) & set(tutor["subjects"])
            if not subject_overlap:
                continue

            language_match = learner["language"] in tutor["languages"]
            availability_match = bool(set(learner["availability"]) & set(tutor["availability"]))

            score = 0.0
            if language_match:
                score += 0.4
            if availability_match:
                score += 0.3
            score += len(subject_overlap) / max(len(learner["subjects_needed"]), 1) * 0.3

            matches.append({
                "tutor": tutor,
                "score": round(score, 3),
                "subjects_matched": list(subject_overlap),
                "language_match": language_match,
                "availability_match": availability_match,
            })

        matches.sort(key=lambda m: m["score"], reverse=True)
        return matches


def main() -> None:
    print("=== Education Access Demo ===\n")

    # 1. Adaptive Learning Engine
    print("--- Adaptive Learning Engine ---")
    engine = AdaptiveLearningEngine()
    engine.add_knowledge_component(KnowledgeComponent("math_1", "Basic Arithmetic", "math", [], 0.3))
    engine.add_knowledge_component(KnowledgeComponent("math_2", "Fractions", "math", ["math_1"], 0.5))
    engine.add_knowledge_component(KnowledgeComponent("math_3", "Algebra", "math", ["math_2"], 0.7))
    engine.add_knowledge_component(KnowledgeComponent("eng_1", "Reading Comprehension", "english", [], 0.4))

    for _ in range(4):
        engine.record_observation("s001", "math_1", correct=True)
    engine.record_observation("s001", "math_1", correct=False)

    summary = engine.get_student_summary("s001")
    print(f"  Student s001: {summary}")

    path = engine.generate_learning_path("s001", max_items=3)
    print(f"  Learning path: {[kc.name for kc in path]}")

    # 2. Offline Content
    print("\n--- Offline Content Management ---")
    ocm = OfflineContentManager()
    pkg1 = ocm.create_package("Science Unit 1", "sw", ["text.html", "diagram.png"], 25.0, priority=2)
    pkg2 = ocm.create_package("Math Basics", "sw", ["text.html", "quiz.json"], 15.0, priority=1)
    sync = ocm.sync_available_packages("tablet_042", max_bandwidth_mb=30)
    print(f"  Sync: {sync.synced_count} synced, {sync.pending_count} pending")

    # 3. Content Simplification
    print("\n--- Content Simplification ---")
    cs = ContentSimplifier()
    result = cs.simplify_text(
        "The utilization of appropriate pedagogical methodologies facilitates approximately "
        "superior educational outcomes. Subsequently, educators endeavor to demonstrate "
        "effective teaching practices.",
        target_level="basic",
    )
    print(f"  Simplified: {result['simplified'][:100]}...")

    dyslexia = cs.generate_dyslexia_friendly_format("This is sample text for dyslexia-friendly formatting.")
    print(f"  Dyslexia format: font={dyslexia['font_recommendation']}, spacing={dyslexia['letter_spacing']}")

    # 4. Multilingual
    print("\n--- Multilingual Content ---")
    mcm = MultilingualContentManager()
    mcm.add_content("lesson_1", "en", "The water cycle describes how water moves through Earth.")
    mcm.add_content("lesson_1", "sw", "Mzunguko wa maji unaeleza jinsi maji yanavyosonga.")
    mcm.request_translation("lesson_1", "en", "ar")
    mcm.request_translation("lesson_1", "en", "zh")
    print(f"  RTL for Arabic: {mcm.is_rtl('ar')}")
    print(f"  Typography (ar): {mcm.get_typography_settings('ar')}")
    print(f"  Stats: {mcm.get_translation_stats()}")

    # 5. Progress Tracking
    print("\n--- Progress Tracking ---")
    pt = ProgressTracker()
    pt.record_session("s001", "math", 30, 15, 12)
    pt.record_session("s001", "math", 25, 12, 10)
    pt.record_session("s001", "math", 20, 10, 5)
    dashboard = pt.get_dashboard("s001")
    print(f"  Sessions: {dashboard.total_sessions}, Accuracy: {dashboard.overall_accuracy}")
    print(f"  Velocity: {dashboard.velocity_exercises_per_hour}/hr")
    print(f"  Intervention: {dashboard.intervention_recommended.value}")

    # 6. Resource Matching
    print("\n--- Resource Matching ---")
    rm = ResourceMatcher()
    rm.add_tutor("t1", "Mr. Kimani", ["math", "science"], ["en", "sw"], ["weekday_morning", "weekday_evening"])
    rm.add_tutor("t2", "Ms. Priya", ["english", "history"], ["en", "hi"], ["weekend"])
    rm.add_learner("l1", "Amina", ["math", "english"], "sw", ["weekday_morning", "weekend"])
    matches = rm.match("l1")
    for m in matches:
        print(f"  {m['tutor']['name']}: score={m['score']}, subjects={m['subjects_matched']}")


if __name__ == "__main__":
    main()
