"""
User Research Toolkit
====================
Interview script design, survey methodology, persona development,
journey mapping, JTBD analysis, diary studies, card sorting, MaxDiff,
and research repository management.

Usage:
    from user_research import InterviewScript, PersonaBuilder, ResearchRepository

    script = InterviewScript(title="Onboarding Study", target_duration_minutes=45)
    script.add_section("Warm-up", questions=[...])
    script.validate_bias_patterns()
"""

from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class QuestionType(Enum):
    OPEN_ENDED = auto()
    CLOSED_ENDED = auto()
    SCALE = auto()
    RANKING = auto()
    MULTIPLE_CHOICE = auto()
    THINK_ALOUD = auto()
    PROBE = auto()
    CARD_SORT = auto()


class ProbeType(Enum):
    CLARIFY = "Can you tell me more about that?"
    EXPAND = "What else comes to mind when you think about this?"
    SPECIFIC_EXAMPLE = "Can you give me a specific example?"
    REPEAT = "Just to make sure I understand — could you restate that?"
    HYPOTHETICAL = "What would you do if...?"
    CONTRAST = "How is that different from...?"


class FindingStatus(Enum):
    RAW = auto()
    VALIDATED = auto()
    PARTIALLY_VALIDATED = auto()
    DISPUTED = auto()
    OUTDATED = auto()


class InsightTag(Enum):
    ONBOARDING = "onboarding"
    NAVIGATION = "navigation"
    SEARCH = "search"
    ENGAGEMENT = "engagement"
    SOCIAL_FEATURES = "social-features"
    EXPECTATION_GAP = "expectation-gap"
    PERFORMANCE = "performance"
    TRUST = "trust"
    MOBILE = "mobile"
    ACCESSIBILITY = "accessibility"


class PersonaType(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ANTI = "anti"
    EDGE = "edge"


class ConfidenceLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DiaryEntryMood(Enum):
    VERY_NEGATIVE = 1
    NEGATIVE = 2
    NEUTRAL = 3
    POSITIVE = 4
    VERY_POSITIVE = 5


class CardSortMode(Enum):
    OPEN = "open"
    CLOSED = "closed"
    HYBRID = "hybrid"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class InterviewQuestion:
    text: str
    question_type: QuestionType
    probes: list[str | ProbeType] = field(default_factory=list)
    follow_ups: list[str] = field(default_factory=list)
    time_estimate_seconds: int = 120
    required: bool = True

    def validate(self) -> list[str]:
        warnings = []
        if len(self.text) > 200:
            warnings.append(f"Question is {len(self.text)} chars — consider shortening")
        if self.question_type == QuestionType.SCALE and "?" not in self.text:
            warnings.append("Scale question should be phrased as a question")
        if "?" not in self.text and self.question_type in (
            QuestionType.OPEN_ENDED, QuestionType.THINK_ALOUD
        ):
            warnings.append("Open-ended question typically ends with '?'")
        return warnings


@dataclass
class InterviewSection:
    name: str
    questions: list[InterviewQuestion] = field(default_factory=list)
    transition_notes: str = ""

    @property
    def estimated_duration_seconds(self) -> int:
        return sum(q.time_estimate_seconds for q in self.questions)

    @property
    def question_count(self) -> int:
        return len(self.questions)


@dataclass
class PersonaCluster:
    name: str
    traits: list[str]
    demographics: dict[str, str]
    goals: list[str]
    frustrations: list[str]
    behaviors: dict[str, Any]
    sample_size: int
    confidence: ConfidenceLevel
    persona_type: PersonaType = PersonaType.PRIMARY

    @property
    def behavioral_diversity_score(self) -> float:
        """Heuristic: more traits + behaviors = more descriptive persona."""
        return min(1.0, (len(self.traits) + len(self.behaviors)) / 12.0)


@dataclass
class JourneyTouchpoint:
    stage: str
    action: str
    emotion: DiaryEntryMood
    pain_points: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    channel: str = "web"
    duration_seconds: Optional[int] = None


@dataclass
class JTBDJob:
    statement: str
    context: str
    metric: str
    job_id: str = ""
    importance_ratings: list[int] = field(default_factory=list)
    satisfaction_ratings: list[int] = field(default_factory=list)

    @property
    def importance_mean(self) -> float:
        return statistics.mean(self.importance_ratings) if self.importance_ratings else 0.0

    @property
    def satisfaction_mean(self) -> float:
        return statistics.mean(self.satisfaction_ratings) if self.satisfaction_ratings else 0.0

    @property
    def opportunity_score(self) -> float:
        """Christensen opportunity score: importance + max(importance - satisfaction, 0)."""
        imp = self.importance_mean
        sat = self.satisfaction_mean
        return imp + max(imp - sat, 0)


@dataclass
class DiaryEntry:
    participant_id: str
    day: int
    timestamp: datetime
    prompt_response: str
    mood: DiaryEntryMood
    media_attachments: list[str] = field(default_factory=list)
    time_spent_seconds: int = 0


@dataclass
class ResearchFinding:
    finding_id: str
    study: str
    insight: str
    evidence: list[str]
    status: FindingStatus
    tags: list[InsightTag]
    confidence: float
    linked_personas: list[str] = field(default_factory=list)
    date_added: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

BIAS_PATTERNS = [
    ("leading", ["don't you think", "isn't it true", "obviously", "everyone knows"]),
    ("double_barreled", ["and also", "as well as", "both"]),
    ("assumptive", ["when you use", "how often do you always", "you must"]),
    ("loaded", ["amazing", "terrible", "horrible", "incredible"]),
]


class InterviewScript:
    """Design, validate, and manage semi-structured interview scripts."""

    def __init__(self, title: str, target_duration_minutes: int = 60,
                 methodology: str = "semi-structured"):
        self.title = title
        self.target_duration_minutes = target_duration_minutes
        self.methodology = methodology
        self.sections: list[InterviewSection] = []
        self._metadata: dict[str, Any] = {}

    def add_section(self, name: str, questions: list[dict] | None = None,
                    transition_notes: str = "") -> InterviewSection:
        section = InterviewSection(name=name, transition_notes=transition_notes)
        if questions:
            for q in questions:
                iq = InterviewQuestion(
                    text=q["text"],
                    question_type=q.get("type", QuestionType.OPEN_ENDED),
                    probes=[ProbeType(p) if isinstance(p, str) and p in [e.value for e in ProbeType]
                            else p for p in q.get("probes", [])],
                    follow_ups=q.get("follow_ups", []),
                )
                section.questions.append(iq)
        self.sections.append(section)
        return section

    def validate_bias_patterns(self) -> list[dict[str, str]]:
        results = []
        for section in self.sections:
            for q in section.questions:
                lower = q.text.lower()
                for pattern_name, triggers in BIAS_PATTERNS:
                    for trigger in triggers:
                        if trigger in lower:
                            results.append({
                                "section": section.name,
                                "question": q.text[:80],
                                "pattern": pattern_name,
                                "trigger": trigger,
                            })
        return results

    def estimated_duration_seconds(self) -> int:
        return sum(s.estimated_duration_seconds for s in self.sections)

    def total_questions(self) -> int:
        return sum(s.question_count for s in self.sections)

    def generate_facilitator_notes(self) -> str:
        lines = [f"# Facilitator Notes: {self.title}", ""]
        lines.append(f"Methodology: {self.methodology}")
        lines.append(f"Target Duration: {self.target_duration_minutes} min")
        lines.append(f"Estimated Duration: {self.estimated_duration_seconds() // 60} min")
        lines.append(f"Total Questions: {self.total_questions()}")
        lines.append("")
        for i, section in enumerate(self.sections, 1):
            lines.append(f"## Section {i}: {section.name}")
            if section.transition_notes:
                lines.append(f"Transition: {section.transition_notes}")
            for q in section.questions:
                lines.append(f"  - [{q.question_type.name}] {q.text}")
                for probe in q.probes:
                    lines.append(f"      Probe: {probe.value if isinstance(probe, ProbeType) else probe}")
            lines.append("")
        return "\n".join(lines)

    def reorder_sections(self, order: list[str]) -> None:
        name_map = {s.name: s for s in self.sections}
        self.sections = [name_map[name] for name in order if name in name_map]

    def export_json(self) -> dict:
        return {
            "title": self.title,
            "methodology": self.methodology,
            "target_duration_minutes": self.target_duration_minutes,
            "estimated_duration_seconds": self.estimated_duration_seconds(),
            "sections": [
                {
                    "name": s.name,
                    "questions": [{"text": q.text, "type": q.question_type.name} for q in s.questions],
                }
                for s in self.sections
            ],
        }


class SurveyAnalyzer:
    """Survey design, sample size calculation, and response analysis."""

    def __init__(self, confidence_level: float = 0.95, margin_of_error: float = 0.05):
        self.confidence_level = confidence_level
        self.margin_of_error = margin_of_error
        self.responses: list[dict] = []
        self.questions: list[dict] = []

    def calculate_sample_size(self, population_size: int) -> int:
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(self.confidence_level, 1.96)
        p = 0.5
        e = self.margin_of_error
        numerator = (z ** 2) * p * (1 - p)
        denominator = e ** 2
        n0 = numerator / denominator
        adjusted = n0 / (1 + ((n0 - 1) / population_size))
        return int(adjusted) + 1

    def add_question(self, q_id: str, text: str, q_type: str,
                     scale: tuple[int, int] | None = None) -> None:
        self.questions.append({
            "id": q_id, "text": text, "type": q_type, "scale": scale
        })

    def add_response(self, participant_id: str, answers: dict[str, Any]) -> None:
        self.responses.append({"participant_id": participant_id, "answers": answers})

    def analyze_likert(self, question_id: str) -> dict:
        values = [r["answers"].get(question_id) for r in self.responses
                  if question_id in r["answers"]]
        nums = [v for v in values if isinstance(v, (int, float))]
        if not nums:
            return {"question_id": question_id, "n": 0}
        return {
            "question_id": question_id,
            "n": len(nums),
            "mean": round(statistics.mean(nums), 2),
            "median": statistics.median(nums),
            "stdev": round(statistics.stdev(nums), 2) if len(nums) > 1 else 0.0,
            "mode": statistics.mode(nums) if nums else None,
        }

    def detect_response_bias(self, threshold_hours: float = 2.0) -> dict:
        if len(self.responses) < 4:
            return {"bias_detected": False, "reason": "insufficient_responses"}
        mid = len(self.responses) // 2
        first_half = self.responses[:mid]
        second_half = self.responses[mid:]
        first_means = []
        second_means = []
        for r in first_half:
            nums = [v for v in r["answers"].values() if isinstance(v, (int, float))]
            if nums:
                first_means.append(statistics.mean(nums))
        for r in second_half:
            nums = [v for v in r["answers"].values() if isinstance(v, (int, float))]
            if nums:
                second_means.append(statistics.mean(nums))
        if not first_means or not second_means:
            return {"bias_detected": False, "reason": "insufficient_numeric_data"}
        diff = abs(statistics.mean(first_means) - statistics.mean(second_means))
        return {
            "bias_detected": diff > 1.0,
            "early_mean": round(statistics.mean(first_means), 2),
            "late_mean": round(statistics.mean(second_means), 2),
            "difference": round(diff, 2),
        }


class PersonaBuilder:
    """Build data-driven personas from behavioral clusters."""

    def __init__(self, data_source: str = "mixed"):
        self.data_source = data_source
        self.clusters: list[PersonaCluster] = []

    def add_behavioral_cluster(self, name: str, traits: list[str],
                                demographics: dict[str, str],
                                goals: list[str], frustrations: list[str],
                                behaviors: dict[str, Any],
                                sample_size: int,
                                confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM,
                                persona_type: PersonaType = PersonaType.PRIMARY) -> PersonaCluster:
        cluster = PersonaCluster(
            name=name, traits=traits, demographics=demographics,
            goals=goals, frustrations=frustrations, behaviors=behaviors,
            sample_size=sample_size, confidence=confidence,
            persona_type=persona_type,
        )
        self.clusters.append(cluster)
        return cluster

    def generate_personas(self) -> list[PersonaCluster]:
        return [c for c in self.clusters if c.persona_type == PersonaType.PRIMARY]

    def generate_anti_personas(self) -> list[PersonaCluster]:
        if not any(c.persona_type == PersonaType.ANTI for c in self.clusters):
            for cluster in self.clusters[:1]:
                anti = PersonaCluster(
                    name=f"Anti-{cluster.name}",
                    traits=[f"NOT: {t}" for t in cluster.traits],
                    demographics={"note": "edge case / invalid user"},
                    goals=["goals that contradict primary persona"],
                    frustrations=["opposite pain points"],
                    behaviors={"session_length_minutes": 2, "login_frequency": "rare"},
                    sample_size=0,
                    confidence=ConfidenceLevel.LOW,
                    persona_type=PersonaType.ANTI,
                )
                self.clusters.append(anti)
        return [c for c in self.clusters if c.persona_type == PersonaType.ANTI]

    def export_empathy_maps(self, output_dir: str = "./artifacts") -> dict[str, str]:
        maps = {}
        for cluster in self.clusters:
            if cluster.persona_type != PersonaType.ANTI:
                maps[cluster.name] = (
                    f"THINKS: {', '.join(cluster.goals)}\n"
                    f"FEELS: {', '.join(cluster.frustrations)}\n"
                    f"DOES: {', '.join(cluster.traits)}\n"
                    f"SAYS: demographics={cluster.demographics}"
                )
        return maps

    def compare_clusters(self) -> dict:
        if len(self.clusters) < 2:
            return {"error": "need_at_least_two_clusters"}
        result = {}
        for i, c1 in enumerate(self.clusters):
            for c2 in self.clusters[i + 1:]:
                overlap = set(c1.traits) & set(c2.traits)
                result[f"{c1.name}_vs_{c2.name}"] = {
                    "trait_overlap": len(overlap),
                    "sample_sizes": [c1.sample_size, c2.sample_size],
                    "confidence_gap": [c1.confidence.value, c2.confidence.value],
                }
        return result


class JourneyMapper:
    """Construct and analyze multi-touchpoint journey maps."""

    def __init__(self, persona_name: str, journey_name: str):
        self.persona_name = persona_name
        self.journey_name = journey_name
        self.touchpoints: list[JourneyTouchpoint] = []

    def add_touchpoint(self, stage: str, action: str, emotion: DiaryEntryMood,
                       pain_points: list[str] | None = None,
                       opportunities: list[str] | None = None,
                       channel: str = "web",
                       duration_seconds: int | None = None) -> JourneyTouchpoint:
        tp = JourneyTouchpoint(
            stage=stage, action=action, emotion=emotion,
            pain_points=pain_points or [], opportunities=opportunities or [],
            channel=channel, duration_seconds=duration_seconds,
        )
        self.touchpoints.append(tp)
        return tp

    def emotion_timeline(self) -> list[dict]:
        return [
            {"stage": tp.stage, "emotion": tp.emotion.value, "action": tp.action}
            for tp in self.touchpoints
        ]

    def critical_moments(self, threshold: int = 2) -> list[JourneyTouchpoint]:
        return [tp for tp in self.touchpoints if tp.emotion.value <= threshold]

    def opportunity_count(self) -> int:
        return sum(len(tp.opportunities) for tp in self.touchpoints)

    def channel_breakdown(self) -> dict[str, int]:
        return dict(Counter(tp.channel for tp in self.touchpoints))

    def export_visual_data(self) -> dict:
        return {
            "persona": self.persona_name,
            "journey": self.journey_name,
            "touchpoints": len(self.touchpoints),
            "emotion_timeline": self.emotion_timeline(),
            "critical_moments": [tp.stage for tp in self.critical_moments()],
            "total_opportunities": self.opportunity_count(),
        }


class JTBDAnalyzer:
    """Jobs-to-be-Done framework analysis with opportunity scoring."""

    def __init__(self):
        self.jobs: list[JTBDJob] = []
        self._job_counter = 0

    def add_job(self, statement: str, context: str, metric: str,
                job_id: str = "") -> JTBDJob:
        self._job_counter += 1
        jid = job_id or f"job_{self._job_counter}"
        job = JTBDJob(statement=statement, context=context, metric=metric, job_id=jid)
        self.jobs.append(job)
        return job

    def add_ratings(self, job_id: str, importance: int, satisfaction: int) -> None:
        for job in self.jobs:
            if job.job_id == job_id:
                job.importance_ratings.append(importance)
                job.satisfaction_ratings.append(satisfaction)
                return
        raise ValueError(f"Job {job_id} not found")

    def compute_opportunity_scores(self, ratings: list[dict] | None = None) -> list[dict]:
        if ratings:
            for r in ratings:
                self.add_ratings(r["job_id"], r["importance"], r["satisfaction"])
        results = []
        for job in self.jobs:
            results.append({
                "job_id": job.job_id,
                "statement": job.statement[:80],
                "importance": round(job.importance_mean, 2),
                "satisfaction": round(job.satisfaction_mean, 2),
                "opportunity_score": round(job.opportunity_score, 2),
                "segment": (
                    "OVERSERVED" if job.importance_mean < job.satisfaction_mean
                    else "UNSERVED" if job.opportunity_score >= 12
                    else "ADEQUATELY_SERVED"
                ),
            })
        results.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return results

    def plot_opportunity_matrix(self) -> str:
        lines = ["Opportunity Matrix (text):", "Satisfaction (x) vs Importance (y)", ""]
        for job in self.jobs:
            x = job.satisfaction_mean
            y = job.importance_mean
            lines.append(f"  [{x:.1f}, {y:.1f}] {job.job_id}: {job.statement[:50]}")
        return "\n".join(lines)

    def export_underserved_report(self) -> list[dict]:
        return [j for j in self.compute_opportunity_scores() if j["segment"] == "UNSERVED"]


class DiaryStudyManager:
    """Manage longitudinal diary studies with prompting and analysis."""

    def __init__(self, study_name: str, duration_days: int = 14,
                 daily_prompt: str = "Describe your experience today."):
        self.study_name = study_name
        self.duration_days = duration_days
        self.daily_prompt = daily_prompt
        self.entries: list[DiaryEntry] = []
        self.participants: list[str] = []

    def add_participant(self, participant_id: str) -> None:
        if participant_id not in self.participants:
            self.participants.append(participant_id)

    def log_entry(self, participant_id: str, day: int,
                  prompt_response: str, mood: DiaryEntryMood,
                  media: list[str] | None = None,
                  time_spent_seconds: int = 0) -> DiaryEntry:
        entry = DiaryEntry(
            participant_id=participant_id, day=day,
            timestamp=datetime.utcnow(), prompt_response=prompt_response,
            mood=mood, media_attachments=media or [],
            time_spent_seconds=time_spent_seconds,
        )
        self.entries.append(entry)
        return entry

    def engagement_rate(self) -> dict[str, float]:
        expected = len(self.participants) * self.duration_days
        actual = len(self.entries)
        overall = actual / expected if expected else 0.0
        per_participant = {}
        for p in self.participants:
            p_entries = [e for e in self.entries if e.participant_id == p]
            per_participant[p] = len(p_entries) / self.duration_days
        return {"overall_rate": round(overall, 3), "per_participant": per_participant}

    def mood_trend(self) -> dict[str, list[int]]:
        by_participant: dict[str, list[int]] = defaultdict(list)
        for entry in sorted(self.entries, key=lambda e: e.day):
            by_participant[entry.participant_id].append(entry.mood.value)
        return dict(by_participant)

    def drop_off_analysis(self) -> list[dict]:
        by_day: dict[int, set[str]] = defaultdict(set)
        for e in self.entries:
            by_day[e.day].add(e.participant_id)
        result = []
        for day in range(1, self.duration_days + 1):
            active = by_day.get(day, set())
            previous = by_day.get(day - 1, set()) if day > 1 else set(self.participants)
            dropped = previous - active
            result.append({"day": day, "active": len(active), "dropped": len(dropped)})
        return result


class CardSortAnalyzer:
    """Analyze open, closed, and hybrid card sort results."""

    def __init__(self, mode: CardSortMode = CardSortMode.OPEN):
        self.mode = mode
        self.results: list[dict[str, Any]] = []

    def add_result(self, participant_id: str, card_groups: dict[str, str]) -> None:
        self.results.append({
            "participant_id": participant_id,
            "groups": card_groups,
        })

    def agreement_score(self) -> float:
        if len(self.results) < 2:
            return 0.0
        card_assignments: dict[str, list[str]] = defaultdict(list)
        for r in self.results:
            for card, group in r["groups"].items():
                card_assignments[card].append(group)
        scores = []
        for card, groups in card_assignments.items():
            mode_group = Counter(groups).most_common(1)[0]
            agreement = mode_group[1] / len(groups)
            scores.append(agreement)
        return round(statistics.mean(scores), 3) if scores else 0.0

    def category_sizes(self) -> dict[str, int]:
        all_groups: list[str] = []
        for r in self.results:
            all_groups.extend(r["groups"].values())
        return dict(Counter(all_groups).most_common())

    def confusion_matrix(self) -> dict[str, dict[str, int]]:
        matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for r in self.results:
            cards = list(r["groups"].keys())
            for i, c1 in enumerate(cards):
                for c2 in cards[i + 1:]:
                    g1, g2 = r["groups"][c1], r["groups"][c2]
                    if g1 == g2:
                        matrix[c1][c2] += 1
                        matrix[c2][c1] += 1
        return {k: dict(v) for k, v in matrix.items()}

    def dendrogram_data(self) -> dict:
        similarity = {}
        n = len(self.results)
        cards = set()
        for r in self.results:
            cards.update(r["groups"].keys())
        for c1 in cards:
            for c2 in cards:
                if c1 >= c2:
                    continue
                together = 0
                for r in self.results:
                    if r["groups"].get(c1) == r["groups"].get(c2):
                        together += 1
                similarity[f"{c1}-{c2}"] = round(together / n, 3) if n else 0.0
        return {"cards": sorted(cards), "similarity": similarity}


class MaxDiffAnalyzer:
    """Analyze Maximum Difference Scaling (MaxDiff) data."""

    def __init__(self, items: list[str]):
        self.items = items
        self.responses: list[dict[str, str]] = []

    def add_response(self, participant_id: str, best: str, worst: str) -> None:
        self.responses.append({"participant_id": participant_id, "best": best, "worst": worst})

    def compute_scores(self) -> list[dict]:
        best_counts = Counter(r["best"] for r in self.responses)
        worst_counts = Counter(r["worst"] for r in self.responses)
        n = len(self.responses) or 1
        scores = []
        for item in self.items:
            best_pct = best_counts.get(item, 0) / n
            worst_pct = worst_counts.get(item, 0) / n
            utility = round(best_pct - worst_pct, 3)
            scores.append({
                "item": item,
                "best_pct": round(best_pct * 100, 1),
                "worst_pct": round(worst_pct * 100, 1),
                "utility_score": utility,
                "rank": 0,
            })
        scores.sort(key=lambda x: x["utility_score"], reverse=True)
        for i, s in enumerate(scores, 1):
            s["rank"] = i
        return scores

    def response_consistency(self) -> float:
        if len(self.responses) < 2:
            return 0.0
        participant_scores: dict[str, dict[str, int]] = defaultdict(lambda: {"best": 0, "worst": 0})
        for r in self.responses:
            participant_scores[r["participant_id"]]["best"] += 1
            participant_scores[r["participant_id"]]["worst"] += 1
        return round(1.0, 3) if participant_scores else 0.0


class ResearchRepository:
    """Cross-study insight repository with tagging and querying."""

    def __init__(self, project: str):
        self.project = project
        self.findings: list[ResearchFinding] = []
        self._finding_counter = 0

    def add_finding(self, study: str, insight: str, evidence: list[str],
                    status: FindingStatus, tags: list[InsightTag],
                    confidence: float,
                    linked_personas: list[str] | None = None,
                    notes: str = "") -> ResearchFinding:
        self._finding_counter += 1
        fid = f"F-{self._finding_counter:04d}"
        finding = ResearchFinding(
            finding_id=fid, study=study, insight=insight, evidence=evidence,
            status=status, tags=tags, confidence=confidence,
            linked_personas=linked_personas or [], notes=notes,
        )
        self.findings.append(finding)
        return finding

    def query(self, tags: list[InsightTag] | None = None,
              status: FindingStatus | None = None,
              min_confidence: float = 0.0) -> list[ResearchFinding]:
        results = self.findings
        if tags:
            tag_set = set(tags)
            results = [f for f in results if tag_set & set(f.tags)]
        if status:
            results = [f for f in results if f.status == status]
        if min_confidence > 0:
            results = [f for f in results if f.confidence >= min_confidence]
        return results

    def tag_frequency(self) -> dict[str, int]:
        counter: Counter = Counter()
        for f in self.findings:
            for tag in f.tags:
                counter[tag.value] += 1
        return dict(counter.most_common())

    def generate_insight_summary(self) -> str:
        lines = [f"# Research Insights: {self.project}", ""]
        by_status = defaultdict(list)
        for f in self.findings:
            by_status[f.status.name].append(f)
        for status_name, findings in by_status.items():
            lines.append(f"## {status_name} ({len(findings)})")
            for f in findings:
                lines.append(f"- [{f.finding_id}] {f.insight[:100]}")
            lines.append("")
        return "\n".join(lines)

    def export_for_stakeholders(self, format: str = "markdown") -> str:
        if format == "markdown":
            return self.generate_insight_summary()
        return str({"project": self.project, "total_findings": len(self.findings)})


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("User Research Toolkit — Demo")
    print("=" * 70)

    # --- Interview Script ---
    script = InterviewScript(title="Onboarding Flow Exploration", target_duration_minutes=45)
    script.add_section("Warm-up", questions=[
        {"text": "Tell me about the last time you set up a new tool for your team.",
         "type": QuestionType.OPEN_ENDED, "probes": ["Can you tell me more about that?"]},
        {"text": "How many tools does your team use regularly?",
         "type": QuestionType.SCALE, "probes": ["What else comes to mind when you think about this?"]},
    ])
    script.add_section("Core", questions=[
        {"text": "Walk me through what happens when you first log into a new application.",
         "type": QuestionType.THINK_ALOUD},
        {"text": "What would make you stop using a new tool in the first week?",
         "type": QuestionType.OPEN_ENDED, "follow_ups": ["Has that ever happened?"]},
    ])
    bias = script.validate_bias_patterns()
    print(f"\n[Interview] Questions: {script.total_questions()}, "
          f"Est: {script.estimated_duration_seconds() // 60} min")
    print(f"[Interview] Bias warnings: {len(bias)}")
    print(script.generate_facilitator_notes()[:400])

    # --- Survey ---
    survey = SurveyAnalyzer(confidence_level=0.95, margin_of_error=0.05)
    n = survey.calculate_sample_size(population_size=5000)
    print(f"\n[Survey] Required sample size for 5000 population: {n}")

    # --- Persona ---
    builder = PersonaBuilder(data_source="survey_and_interview")
    builder.add_behavioral_cluster(
        name="Power Collaborators", traits=["daily active", "multi-project"],
        demographics={"role": "PM"}, goals=["streamline communication"],
        frustrations=["tool sprawl"], behaviors={"login_frequency": "daily"},
        sample_size=34, confidence=ConfidenceLevel.HIGH,
    )
    builder.add_behavioral_cluster(
        name="Occasional Checkers", traits=["weekly active", "single-project"],
        demographics={"role": "Engineer"}, goals=["stay informed"],
        frustrations=["too many notifications"], behaviors={"login_frequency": "weekly"},
        sample_size=28, confidence=ConfidenceLevel.MEDIUM,
    )
    personas = builder.generate_personas()
    builder.generate_anti_personas()
    empathy = builder.export_empathy_maps()
    print(f"\n[Personas] Generated {len(personas)} primary + anti-personas")
    for name, content in empathy.items():
        print(f"  {name}: {content[:60]}...")

    # --- Journey Map ---
    jm = JourneyMapper(persona_name="Power Collaborators", journey_name="Onboarding")
    jm.add_touchpoint("Discovery", "Lands on product page", DiaryEntryMood.POSITIVE,
                      channel="web")
    jm.add_touchpoint("Signup", "Fills out registration form", DiaryEntryMood.NEUTRAL,
                      pain_points=["too many fields"], channel="web")
    jm.add_touchpoint("Onboarding", "Walks through wizard", DiaryEntryMood.VERY_NEGATIVE,
                      pain_points=["skip button hidden", "no progress indicator"],
                      opportunities=["add progress bar", "make skip visible"])
    critical = jm.critical_moments()
    print(f"\n[Journey] Touchpoints: {len(jm.touchpoints)}, Critical: {len(critical)}")

    # --- JTBD ---
    jtbd = JTBDAnalyzer()
    jtbd.add_job("When I start a project, I want to set up a shared workspace.", "init", "setup_time")
    jtbd.add_job("When I receive feedback, I want to route it to owners.", "feedback", "resolution_rate")
    jtbd.add_ratings("job_1", importance=9, satisfaction=4)
    jtbd.add_ratings("job_2", importance=8, satisfaction=3)
    opps = jtbd.compute_opportunity_scores()
    print(f"\n[JtBD] Top opportunity: {opps[0]['job_id']} "
          f"(score={opps[0]['opportunity_score']})")

    # --- Card Sort ---
    cs = CardSortAnalyzer(mode=CardSortMode.OPEN)
    cs.add_result("p1", {"Card A": "Group 1", "Card B": "Group 1", "Card C": "Group 2"})
    cs.add_result("p2", {"Card A": "Group 1", "Card B": "Group 2", "Card C": "Group 2"})
    cs.add_result("p3", {"Card A": "Group 1", "Card B": "Group 1", "Card C": "Group 2"})
    print(f"\n[CardSort] Agreement: {cs.agreement_score()}, "
          f"Categories: {cs.category_sizes()}")

    # --- MaxDiff ---
    md = MaxDiffAnalyzer(items=["Feature A", "Feature B", "Feature C"])
    md.add_response("p1", best="Feature A", worst="Feature C")
    md.add_response("p2", best="Feature B", worst="Feature C")
    md.add_response("p3", best="Feature A", worst="Feature B")
    scores = md.compute_scores()
    print(f"\n[MaxDiff] Top item: {scores[0]['item']} "
          f"(utility={scores[0]['utility_score']})")

    # --- Repository ---
    repo = ResearchRepository(project="collaboration-platform")
    repo.add_finding(
        study="onboarding-interviews", insight="Users expect guided setup wizard",
        evidence=["transcript-04"], status=FindingStatus.VALIDATED,
        tags=[InsightTag.ONBOARDING], confidence=0.85,
    )
    repo.add_finding(
        study="diary-study", insight="Engagement drops after day 3 without collaborator invite",
        evidence=["day3-log"], status=FindingStatus.PARTIALLY_VALIDATED,
        tags=[InsightTag.ENGAGEMENT], confidence=0.72,
    )
    print(f"\n[Repository] Findings: {len(repo.findings)}")
    print(f"[Repository] Tag frequency: {repo.tag_frequency()}")
    print(repo.generate_insight_summary()[:300])

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
