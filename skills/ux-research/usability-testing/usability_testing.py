"""
Usability Testing Toolkit
========================
Task success measurement, SUS/NPS scoring, think-aloud analysis,
heatmap/clickstream analysis, A/B testing, funnel conversion,
rage click detection, and severity rating frameworks.

Usage:
    from usability_testing import TaskSuccessStudy, SUSSurvey, ABTest, RageClickDetector

    study = TaskSuccessStudy(name="Checkout Flow v2")
    study.record_result(participant_id="P01", task_id="T1", success=True, time_seconds=145)
    report = study.generate_report()
"""

from __future__ import annotations

import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SuccessMetric(Enum):
    BINARY = "binary"           # Pass / Fail
    DICHOTOMOUS = "dichotomous"  # Success / Failure with partial credit
    COMPOSITE = "composite"     # Weighted combination of success + time + errors


class SeverityLevel(Enum):
    COSMETIC = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    CRITICAL = 5


class SatisfactionScale(Enum):
    SUS = "sus"
    NPS = "nps"
    UMUX_LITE = "umux_lite"
    CSAT = "csat"


class ClickType(Enum):
    CLICK = auto()
    DOUBLE_CLICK = auto()
    RIGHT_CLICK = auto()
    SCROLL = auto()


class TestResult(Enum):
    SIGNIFICANT_POSITIVE = "significant_positive"
    SIGNIFICANT_NEGATIVE = "significant_negative"
    NOT_SIGNIFICANT = "not_significant"
    INCONCLUSIVE = "inconclusive"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class UsabilityTask:
    task_id: str
    description: str
    steps: list[str]
    time_limit_seconds: int = 300
    metric: SuccessMetric = SuccessMetric.BINARY


@dataclass
class TaskResult:
    participant_id: str
    task_id: str
    success: bool
    time_seconds: float
    errors: int = 0
    think_aloud_notes: str = ""
    partial_credit: float = 1.0
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ClickEvent:
    x: int
    y: int
    timestamp: int
    element_id: str = ""
    response_ms: Optional[int] = None
    click_type: ClickType = ClickType.CLICK
    viewport_width: int = 1920
    viewport_height: int = 1080


@dataclass
class RageClickCluster:
    x_center: int
    y_center: int
    element_id: str
    click_count: int
    duration_ms: int
    severity: SeverityLevel
    is_dead_click: bool = False


@dataclass
class FunnelStep:
    step_id: str
    name: str
    visitors: int = 0
    completions: int = 0

    @property
    def conversion_rate(self) -> float:
        return self.completions / self.visitors if self.visitors else 0.0

    @property
    def drop_off_rate(self) -> float:
        return 1.0 - self.conversion_rate


@dataclass
class SeverityFinding:
    finding_id: str
    description: str
    frequency: int        # How many participants hit this
    impact: int           # 1-5 scale
    persistence: int      # 1-5 scale (how long it persists across tasks)
    task_ids: list[str] = field(default_factory=list)
    participant_ids: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    @property
    def severity_score(self) -> float:
        return (self.frequency * self.impact * self.persistence) ** (1/3)

    @property
    def severity_level(self) -> SeverityLevel:
        score = self.severity_score
        if score >= 4.0:
            return SeverityLevel.CRITICAL
        elif score >= 3.0:
            return SeverityLevel.MAJOR
        elif score >= 2.0:
            return SeverityLevel.MODERATE
        elif score >= 1.0:
            return SeverityLevel.MINOR
        return SeverityLevel.COSMETIC


@dataclass
class VariantResult:
    name: str
    conversions: int
    visitors: int

    @property
    def conversion_rate(self) -> float:
        return self.conversions / self.visitors if self.visitors else 0.0


# ---------------------------------------------------------------------------
# Statistical Helpers
# ---------------------------------------------------------------------------

def _normal_cdf(x: float) -> float:
    """Approximation of the standard normal CDF."""
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    sign = 1 if x >= 0 else -1
    x = abs(x) / math.sqrt(2)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return 0.5 * (1.0 + sign * y)


def _confidence_interval_95(mean: float, stdev: float, n: int) -> tuple[float, float]:
    if n < 2:
        return (mean, mean)
    margin = 1.96 * (stdev / math.sqrt(n))
    return (round(mean - margin, 3), round(mean + margin, 3))


def _proportion_ci(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    p = successes / total
    margin = z * math.sqrt(p * (1 - p) / total)
    return (round(max(0, p - margin), 4), round(min(1, p + margin), 4))


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class TaskSuccessStudy:
    """Measure task success rates with confidence intervals and time analysis."""

    def __init__(self, name: str):
        self.name = name
        self.tasks: dict[str, UsabilityTask] = {}
        self.results: list[TaskResult] = []

    def add_task(self, task_id: str, description: str, steps: list[str],
                 time_limit_seconds: int = 300,
                 metric: SuccessMetric = SuccessMetric.BINARY) -> UsabilityTask:
        task = UsabilityTask(
            task_id=task_id, description=description, steps=steps,
            time_limit_seconds=time_limit_seconds, metric=metric,
        )
        self.tasks[task_id] = task
        return task

    def record_result(self, participant_id: str, task_id: str, success: bool,
                      time_seconds: float, errors: int = 0,
                      think_aloud_notes: str = "",
                      partial_credit: float = 1.0) -> TaskResult:
        result = TaskResult(
            participant_id=participant_id, task_id=task_id, success=success,
            time_seconds=time_seconds, errors=errors,
            think_aloud_notes=think_aloud_notes, partial_credit=partial_credit,
        )
        self.results.append(result)
        return result

    def task_success_rate(self, task_id: str) -> dict:
        task_results = [r for r in self.results if r.task_id == task_id]
        if not task_results:
            return {"task_id": task_id, "n": 0}
        successes = sum(1 for r in task_results if r.success)
        n = len(task_results)
        rate = successes / n
        ci = _proportion_ci(successes, n)
        times = [r.time_seconds for r in task_results]
        return {
            "task_id": task_id,
            "description": self.tasks[task_id].description,
            "n": n,
            "successes": successes,
            "success_rate": round(rate, 3),
            "ci_lower": ci[0],
            "ci_upper": ci[1],
            "mean_time_seconds": round(statistics.mean(times), 1),
            "median_time_seconds": round(statistics.median(times), 1),
            "stdev_time_seconds": round(statistics.stdev(times), 2) if len(times) > 1 else 0,
            "mean_errors": round(statistics.mean(r.errors for r in task_results), 2),
        }

    def overall_success_rate(self) -> dict:
        all_successes = sum(1 for r in self.results if r.success)
        all_n = len(self.results)
        rate = all_successes / all_n if all_n else 0.0
        ci = _proportion_ci(all_successes, all_n)
        return {
            "total_attempts": all_n,
            "total_successes": all_successes,
            "overall_rate": round(rate, 3),
            "ci_lower": ci[0],
            "ci_upper": ci[1],
        }

    def time_on_task_analysis(self, task_id: str) -> dict:
        times = [r.time_seconds for r in self.results if r.task_id == task_id]
        if not times:
            return {}
        times_sorted = sorted(times)
        n = len(times_sorted)
        return {
            "n": n,
            "mean": round(statistics.mean(times), 1),
            "median": round(statistics.median(times), 1),
            "stdev": round(statistics.stdev(times), 2) if n > 1 else 0,
            "min": times_sorted[0],
            "max": times_sorted[-1],
            "p25": times_sorted[n // 4],
            "p75": times_sorted[3 * n // 4],
            "timeouts": sum(1 for r in self.results
                           if r.task_id == task_id and r.time_seconds >= self.tasks[task_id].time_limit_seconds),
        }

    def generate_report(self) -> str:
        lines = [f"# Usability Report: {self.name}", ""]
        overall = self.overall_success_rate()
        lines.append(f"## Overall: {overall['overall_rate']:.1%} success "
                     f"(n={overall['total_attempts']})")
        lines.append(f"95% CI: [{overall['ci_lower']:.1%}, {overall['ci_upper']:.1%}]")
        lines.append("")
        for task_id in self.tasks:
            data = self.task_success_rate(task_id)
            if data["n"] > 0:
                lines.append(f"### Task {task_id}: {self.tasks[task_id].description}")
                lines.append(f"- Success rate: {data['success_rate']:.1%} "
                             f"(n={data['n']}, CI=[{data['ci_lower']:.1%}, {data['ci_upper']:.1%}])")
                lines.append(f"- Mean time: {data['mean_time_seconds']}s "
                             f"(median={data['median_time_seconds']}s)")
                lines.append(f"- Mean errors: {data['mean_errors']}")
                lines.append("")
        return "\n".join(lines)


class SUSSurvey:
    """System Usability Scale administration and analysis."""

    # SUS question scoring: odd items score (response - 1), even items score (5 - response)
    ODD_ITEMS = [0, 2, 4, 6, 8]  # 0-indexed
    EVEN_ITEMS = [1, 3, 5, 7, 9]

    def __init__(self, name: str = "SUS Survey"):
        self.name = name
        self.responses: dict[str, list[int]] = {}

    def add_response(self, participant_id: str, answers: list[int]) -> None:
        if len(answers) != 10:
            raise ValueError("SUS requires exactly 10 responses")
        if not all(1 <= a <= 5 for a in answers):
            raise ValueError("SUS responses must be between 1 and 5")
        self.responses[participant_id] = answers

    def calculate_sus_score(self, participant_id: str) -> float:
        answers = self.responses[participant_id]
        score = 0
        for i in self.ODD_ITEMS:
            score += (answers[i] - 1) * 2.5
        for i in self.EVEN_ITEMS:
            score += (5 - answers[i]) * 2.5
        return round(score, 1)

    def analyze(self) -> dict:
        if not self.responses:
            return {"error": "no_responses"}
        scores = [self.calculate_sus_score(pid) for pid in self.responses]
        mean_score = statistics.mean(scores)
        stdev_score = statistics.stdev(scores) if len(scores) > 1 else 0
        ci = _confidence_interval_95(mean_score, stdev_score, len(scores))
        percentile = self._percentile_rank(mean_score)
        adjective = self._adjective_rating(mean_score)
        return {
            "n": len(scores),
            "mean_sus_score": round(mean_score, 1),
            "stdev": round(stdev_score, 2),
            "confidence_interval": ci,
            "percentile_rank": percentile,
            "adjective_rating": adjective,
            "individual_scores": {pid: self.calculate_sus_score(pid) for pid in self.responses},
        }

    def _percentile_rank(self, score: float) -> int:
        # Approximate percentile ranks from Sauro's research
        thresholds = [
            (90, 85.5), (80, 78.8), (70, 72.5), (60, 65.0),
            (50, 58.5), (40, 51.0), (30, 43.5), (20, 32.0), (10, 19.0),
        ]
        for pct, threshold in thresholds:
            if score >= threshold:
                return pct
        return 5

    def _adjective_rating(self, score: float) -> str:
        if score >= 80.3:
            return "Best imaginable"
        elif score >= 72.5:
            return "Excellent"
        elif score >= 62.8:
            return "Good"
        elif score >= 51.4:
            return "OK"
        elif score >= 38.7:
            return "Poor"
        elif score >= 25.6:
            return "Frustrating"
        return "Worst imaginable"


class NPSAnalyzer:
    """Net Promoter Score analysis."""

    def __init__(self, name: str = "NPS Survey"):
        self.name = name
        self.responses: dict[str, int] = {}

    def add_response(self, participant_id: str, score: int) -> None:
        if not 0 <= score <= 10:
            raise ValueError("NPS scores must be between 0 and 10")
        self.responses[participant_id] = score

    def analyze(self) -> dict:
        if not self.responses:
            return {"error": "no_responses"}
        scores = list(self.responses.values())
        promoters = sum(1 for s in scores if s >= 9)
        passives = sum(1 for s in scores if 7 <= s <= 8)
        detractors = sum(1 for s in scores if s <= 6)
        n = len(scores)
        nps = round(((promoters - detractors) / n) * 100, 1)
        return {
            "n": n,
            "nps": nps,
            "promoters_pct": round(promoters / n * 100, 1),
            "passives_pct": round(passives / n * 100, 1),
            "detractors_pct": round(detractors / n * 100, 1),
            "mean_score": round(statistics.mean(scores), 2),
        }


class ThinkAloudAnalyzer:
    """Structured coding and analysis of think-aloud transcripts."""

    def __init__(self):
        self.transcripts: list[dict] = []
        self.codes: dict[str, list[str]] = defaultdict(list)

    def add_transcript(self, participant_id: str, task_id: str, segments: list[dict]) -> None:
        self.transcripts.append({
            "participant_id": participant_id,
            "task_id": task_id,
            "segments": segments,
        })

    def code_segments(self, participant_id: str, task_id: str,
                      code_definitions: dict[str, str]) -> dict[str, int]:
        counts: dict[str, int] = Counter()
        for t in self.transcripts:
            if t["participant_id"] == participant_id and t["task_id"] == task_id:
                for seg in t["segments"]:
                    text = seg.get("text", "").lower()
                    for code, keywords in code_definitions.items():
                        if any(kw.lower() in text for kw in keywords.split(",")):
                            counts[code] += 1
                            self.codes[code].append(f"{participant_id}:{task_id}")
        return dict(counts)

    def critical_incidents(self, task_id: str | None = None) -> list[dict]:
        incidents = []
        for t in self.transcripts:
            if task_id and t["task_id"] != task_id:
                continue
            for seg in t["segments"]:
                if seg.get("is_critical_incident", False):
                    incidents.append({
                        "participant": t["participant_id"],
                        "task": t["task_id"],
                        "text": seg["text"],
                        "type": seg.get("incident_type", "unknown"),
                    })
        return incidents

    def summary(self) -> dict:
        return {
            "total_transcripts": len(self.transcripts),
            "total_segments": sum(len(t["segments"]) for t in self.transcripts),
            "codes_applied": dict(Counter({k: len(v) for k, v in self.codes.items()})),
        }


class RageClickDetector:
    """Detect frustration patterns in clickstream data."""

    def __init__(self, time_window_ms: int = 1000, min_clicks: int = 3,
                 max_distance_px: int = 50,
                 dead_click_threshold_ms: int = 500):
        self.time_window_ms = time_window_ms
        self.min_clicks = min_clicks
        self.max_distance_px = max_distance_px
        self.dead_click_threshold_ms = dead_click_threshold_ms

    def _distance(self, c1: ClickEvent, c2: ClickEvent) -> float:
        return math.sqrt((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2)

    def detect(self, events: list[ClickEvent]) -> list[RageClickCluster]:
        if not events:
            return []
        clusters: list[RageClickCluster] = []
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        i = 0
        while i < len(sorted_events):
            cluster_events = [sorted_events[i]]
            j = i + 1
            while j < len(sorted_events):
                dt = sorted_events[j].timestamp - cluster_events[0].timestamp
                if dt > self.time_window_ms:
                    break
                if self._distance(sorted_events[j], cluster_events[-1]) <= self.max_distance_px:
                    cluster_events.append(sorted_events[j])
                j += 1
            if len(cluster_events) >= self.min_clicks:
                x_center = int(statistics.mean(e.x for e in cluster_events))
                y_center = int(statistics.mean(e.y for e in cluster_events))
                duration = cluster_events[-1].timestamp - cluster_events[0].timestamp
                is_dead = all(e.response_ms is None for e in cluster_events)
                severity = (
                    SeverityLevel.CRITICAL if len(cluster_events) >= 5
                    else SeverityLevel.MAJOR if len(cluster_events) >= 4
                    else SeverityLevel.MODERATE
                )
                clusters.append(RageClickCluster(
                    x_center=x_center, y_center=y_center,
                    element_id=cluster_events[0].element_id,
                    click_count=len(cluster_events),
                    duration_ms=duration, severity=severity,
                    is_dead_click=is_dead,
                ))
            i = j if j > i + 1 else i + 1
        return clusters

    def dead_click_report(self, events: list[ClickEvent]) -> list[dict]:
        non_responsive = [e for e in events if e.response_ms is None and e.element_id]
        by_element = defaultdict(list)
        for e in non_responsive:
            by_element[e.element_id].append(e)
        return [
            {"element_id": elem, "click_count": len(clicks),
             "dead_click_rate": len(clicks) / len(events) * 100 if events else 0}
            for elem, clicks in sorted(by_element.items(), key=lambda x: -len(x[1]))
        ]


class ABTest:
    """A/B test design and statistical analysis."""

    def __init__(self, name: str, primary_metric: str,
                 minimum_detectable_effect: float = 0.05,
                 power: float = 0.8, significance_level: float = 0.05):
        self.name = name
        self.primary_metric = primary_metric
        self.mde = minimum_detectable_effect
        self.power = power
        self.alpha = significance_level
        self.variants: list[VariantResult] = []

    def calculate_sample_size(self, baseline_rate: float) -> int:
        z_alpha = 1.96 if self.alpha == 0.05 else 2.576 if self.alpha == 0.01 else 1.645
        z_beta = 0.842 if self.power == 0.8 else 1.282 if self.power == 0.9 else 0.842
        p1 = baseline_rate
        p2 = baseline_rate + self.mde
        pooled_p = (p1 + p2) / 2
        n = ((z_alpha * math.sqrt(2 * pooled_p * (1 - pooled_p)) +
              z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (self.mde ** 2)
        return int(math.ceil(n))

    def add_variant(self, name: str, conversions: int, visitors: int) -> None:
        self.variants.append(VariantResult(name=name, conversions=conversions, visitors=visitors))

    def analyze(self) -> dict:
        if len(self.variants) < 2:
            return {"error": "need_at_least_two_variants"}
        control = self.variants[0]
        treatment = self.variants[1]
        p1 = control.conversion_rate
        p2 = treatment.conversion_rate
        n1, n2 = control.visitors, treatment.visitors
        se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
        if se == 0:
            return {"error": "zero_standard_error"}
        z = (p2 - p1) / se
        p_value = 2 * (1 - _normal_cdf(abs(z)))
        significant = p_value < self.alpha
        lift = (p2 - p1) / p1 if p1 > 0 else 0
        ci_margin = 1.96 * se
        return {
            "control": {"name": control.name, "rate": round(p1, 4), "n": n1},
            "treatment": {"name": treatment.name, "rate": round(p2, 4), "n": n2},
            "lift": round(lift, 4),
            "absolute_diff": round(p2 - p1, 4),
            "z_score": round(z, 3),
            "p_value": round(p_value, 4),
            "significant": significant,
            "confidence_interval": (round(p2 - p1 - ci_margin, 4), round(p2 - p1 + ci_margin, 4)),
            "winner": treatment.name if significant and p2 > p1 else control.name if significant else None,
            "result": (
                TestResult.SIGNIFICANT_POSITIVE.value if significant and p2 > p1
                else TestResult.SIGNIFICANT_NEGATIVE.value if significant and p2 < p1
                else TestResult.NOT_SIGNIFICANT.value
            ),
        }


class FunnelAnalyzer:
    """Analyze conversion funnels with drop-off detection."""

    def __init__(self, name: str):
        self.name = name
        self.steps: list[FunnelStep] = []

    def add_step(self, step_id: str, name: str, visitors: int = 0,
                 completions: int = 0) -> FunnelStep:
        step = FunnelStep(step_id=step_id, name=name,
                          visitors=visitors, completions=completions)
        self.steps.append(step)
        return step

    def overall_conversion(self) -> float:
        if not self.steps:
            return 0.0
        return self.steps[-1].completions / self.steps[0].visitors if self.steps[0].visitors else 0.0

    def drop_off_analysis(self) -> list[dict]:
        results = []
        for i, step in enumerate(self.steps):
            prev_completions = self.steps[i - 1].completions if i > 0 else step.visitors
            drop_off = prev_completions - step.completions if i > 0 else 0
            drop_off_pct = drop_off / prev_completions if prev_completions else 0
            results.append({
                "step_id": step.step_id,
                "name": step.name,
                "visitors": step.visitors,
                "completions": step.completions,
                "step_conversion": round(step.conversion_rate, 3),
                "drop_off_count": drop_off,
                "drop_off_pct": round(drop_off_pct, 3),
            })
        return results

    def worst_drop_off(self) -> dict | None:
        analysis = self.drop_off_analysis()
        if len(analysis) < 2:
            return None
        return max(analysis[1:], key=lambda x: x["drop_off_pct"])

    def compare_funnels(self, other: "FunnelAnalyzer") -> dict:
        if len(self.steps) != len(other.steps):
            return {"error": "funnels_have_different_step_count"}
        comparisons = []
        for s1, s2 in zip(self.steps, other.steps):
            diff = s1.conversion_rate - s2.conversion_rate
            comparisons.append({
                "step": s1.name,
                "this_rate": round(s1.conversion_rate, 3),
                "other_rate": round(s2.conversion_rate, 3),
                "difference": round(diff, 3),
            })
        return {
            "this_overall": round(self.overall_conversion(), 3),
            "other_overall": round(other.overall_conversion(), 3),
            "step_comparisons": comparisons,
        }


class SeverityRatingFramework:
    """Multi-factor severity rating for usability findings."""

    def __init__(self):
        self.findings: list[SeverityFinding] = []
        self._counter = 0

    def add_finding(self, description: str, frequency: int, impact: int,
                    persistence: int, task_ids: list[str] | None = None,
                    participant_ids: list[str] | None = None,
                    evidence: list[str] | None = None) -> SeverityFinding:
        self._counter += 1
        finding = SeverityFinding(
            finding_id=f"SF-{self._counter:03d}",
            description=description,
            frequency=frequency, impact=impact, persistence=persistence,
            task_ids=task_ids or [], participant_ids=participant_ids or [],
            evidence=evidence or [],
        )
        self.findings.append(finding)
        return finding

    def ranked_findings(self) -> list[SeverityFinding]:
        return sorted(self.findings, key=lambda f: f.severity_score, reverse=True)

    def by_level(self, level: SeverityLevel) -> list[SeverityFinding]:
        return [f for f in self.findings if f.severity_level == level]

    def summary_report(self) -> str:
        ranked = self.ranked_findings()
        lines = [f"# Severity Summary ({len(ranked)} findings)", ""]
        level_counts = Counter(f.severity_level for f in ranked)
        for level in reversed(list(SeverityLevel)):
            count = level_counts.get(level, 0)
            if count:
                lines.append(f"- {level.name}: {count}")
        lines.append("")
        for f in ranked:
            lines.append(
                f"[{f.severity_level.name}] {f.finding_id}: {f.description} "
                f"(freq={f.frequency}, impact={f.impact}, persist={f.persistence}, "
                f"score={f.severity_score:.2f})"
            )
        return "\n".join(lines)


class UsabilityMetricsDashboard:
    """Aggregate all usability metrics into a single dashboard."""

    def __init__(self, study_name: str):
        self.study_name = study_name
        self.task_study: Optional[TaskSuccessStudy] = None
        self.sus: Optional[SUSSurvey] = None
        self.nps: Optional[NPSAnalyzer] = None
        self.ab_test: Optional[ABTest] = None
        self.funnel: Optional[FunnelAnalyzer] = None
        self.severity: SeverityRatingFramework = SeverityRatingFramework()

    def set_task_study(self, study: TaskSuccessStudy) -> None:
        self.task_study = study

    def set_sus(self, sus: SUSSurvey) -> None:
        self.sus = sus

    def set_nps(self, nps: NPSAnalyzer) -> None:
        self.nps = nps

    def generate_executive_summary(self) -> str:
        lines = [f"# Executive Summary: {self.study_name}", ""]
        if self.task_study:
            overall = self.task_study.overall_success_rate()
            lines.append(f"Task Success Rate: {overall['overall_rate']:.1%} "
                         f"(n={overall['total_attempts']})")
        if self.sus:
            sus_result = self.sus.analyze()
            lines.append(f"SUS Score: {sus_result.get('mean_sus_score', 'N/A')} "
                         f"({sus_result.get('adjective_rating', 'N/A')})")
        if self.nps:
            nps_result = self.nps.analyze()
            lines.append(f"NPS: {nps_result.get('nps', 'N/A')}")
        lines.append(f"\nSeverity Findings: {len(self.severity.findings)}")
        critical = self.severity.by_level(SeverityLevel.CRITICAL)
        if critical:
            lines.append(f"  CRITICAL: {len(critical)} — immediate action required")
        lines.append("")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("Usability Testing Toolkit — Demo")
    print("=" * 70)

    # --- Task Success Study ---
    study = TaskSuccessStudy(name="Checkout Flow v2 Benchmark")
    study.add_task("T1", "Complete a purchase as guest", ["Add item", "Checkout", "Pay"],
                   time_limit_seconds=300, metric=SuccessMetric.COMPOSITE)
    study.add_task("T2", "Apply a discount code", ["Find field", "Enter code", "Verify"],
                   time_limit_seconds=120, metric=SuccessMetric.BINARY)

    for pid in ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08"]:
        import random
        random.seed(hash(pid))
        t1_time = random.randint(90, 280)
        t1_ok = t1_time < 250
        t2_time = random.randint(20, 100)
        t2_ok = t2_time < 80
        study.record_result(pid, "T1", t1_ok, t1_time, errors=random.randint(0, 3),
                           think_aloud_notes="Sample note")
        study.record_result(pid, "T2", t2_ok, t2_time, errors=random.randint(0, 2))

    print(study.generate_report()[:500])

    # --- SUS ---
    sus = SUSSurvey("Post-Task SUS")
    import random
    random.seed(42)
    for i in range(15):
        answers = [random.randint(3, 5) for _ in range(10)]
        sus.add_response(f"P{i+1:02d}", answers)
    sus_result = sus.analyze()
    print(f"\n[SUS] Mean: {sus_result['mean_sus_score']}, "
          f"Rating: {sus_result['adjective_rating']}, "
          f"Percentile: {sus_result['percentile_rank']}")

    # --- Rage Click Detection ---
    detector = RageClickDetector(time_window_ms=1000, min_clicks=3)
    events = [
        ClickEvent(x=450, y=300, timestamp=1000, element_id="btn-submit", response_ms=200),
        ClickEvent(x=455, y=305, timestamp=1150, element_id="btn-submit"),
        ClickEvent(x=448, y=298, timestamp=1250, element_id="btn-submit"),
        ClickEvent(x=452, y=302, timestamp=1320, element_id="btn-submit"),
        ClickEvent(x=900, y=500, timestamp=5000, element_id="empty-div"),
        ClickEvent(x=910, y=510, timestamp=5050, element_id="empty-div"),
        ClickEvent(x=895, y=498, timestamp=5100, element_id="empty-div"),
    ]
    clusters = detector.detect(events)
    print(f"\n[Rage Clicks] Found {len(clusters)} clusters:")
    for c in clusters:
        print(f"  Element={c.element_id}, clicks={c.click_count}, "
              f"severity={c.severity.name}, dead={c.is_dead_click}")

    # --- A/B Test ---
    ab = ABTest("New Checkout Button", "conversion_rate", mde=0.03)
    sample = ab.calculate_sample_size(baseline_rate=0.12)
    print(f"\n[A/B] Required sample per variant: {sample}")
    ab.add_variant("control", conversions=150, visitors=1200)
    ab.add_variant("treatment", conversions=185, visitors=1200)
    ab_result = ab.analyze()
    print(f"[A/B] Control={ab_result['control']['rate']:.3f}, "
          f"Treatment={ab_result['treatment']['rate']:.3f}, "
          f"p={ab_result['p_value']}, sig={ab_result['significant']}")

    # --- Funnel ---
    funnel = FunnelAnalyzer("Purchase Funnel")
    funnel.add_step("S1", "Product View", visitors=5000, completions=5000)
    funnel.add_step("S2", "Add to Cart", visitors=5000, completions=2500)
    funnel.add_step("S3", "Checkout", visitors=5000, completions=1200)
    funnel.add_step("S4", "Purchase", visitors=5000, completions=800)
    worst = funnel.worst_drop_off()
    print(f"\n[Funnel] Overall conversion: {funnel.overall_conversion():.1%}")
    if worst:
        print(f"[Funnel] Worst drop-off: {worst['name']} ({worst['drop_off_pct']:.1%})")

    # --- Severity ---
    severity = SeverityRatingFramework()
    severity.add_finding("Submit button unresponsive on mobile", frequency=7, impact=5,
                        persistence=4, task_ids=["T1"],
                        participant_ids=[f"P{i}" for i in range(1, 8)])
    severity.add_finding("Discount code field hard to locate", frequency=4, impact=3,
                        persistence=2, task_ids=["T2"])
    print(f"\n{severity.summary_report()}")

    # --- Dashboard ---
    dashboard = UsabilityMetricsDashboard("Q1 2026 Checkout Study")
    dashboard.set_task_study(study)
    dashboard.set_sus(sus)
    dashboard.severity = severity
    print(dashboard.generate_executive_summary())

    print("=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
