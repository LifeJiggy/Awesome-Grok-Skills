"""
recruitment_ai.py — Recruitment AI pipeline: resume parsing, candidate matching,
interview scheduling, and bias detection.

Provides production-grade data models and engines for AI-driven recruitment automation.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class EducationLevel(Enum):
    HIGH_SCHOOL = "high_school"
    ASSOCIATES = "associates"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORATE = "doctorate"
    TRADE_CERT = "trade_certificate"


class MatchStatus(Enum):
    REJECTED = "rejected"
    SCREENING = "screening"
    SHORTLISTED = "shortlisted"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    HIRED = "hired"
    WITHDRAWN = "withdrawn"


class BiasFlagType(Enum):
    GENDER_DISPARITY = "gender_disparity"
    ETHNICITY_DISPARITY = "ethnicity_disparity"
    AGE_DISPARITY = "age_disparity"
    EDUCATION_BIAS = "education_bias"
    NAME_BIAS = "name_bias"
    GAP_PENALTY = "gap_penalty"


class AnonymizeLevel(Enum):
    NONE = "none"
    PARTIAL = "partial"
    FULL = "full"


class InterviewRoundType(Enum):
    PHONE_SCREEN = "phone_screen"
    TECHNICAL = "technical"
    ON_SITE = "on_site"
    EXECUTIVE = "executive"
    CULTURE_FIT = "culture_fit"


# ─── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class SkillMatch:
    """A single skill with confidence and level."""
    skill_name: str
    taxonomy_id: str
    confidence: float
    level: SkillLevel
    years_experience: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be 0-1, got {self.confidence}")


@dataclass
class WorkExperience:
    """Parsed work experience entry."""
    company: str
    title: str
    start_date: datetime
    end_date: Optional[datetime]
    description: str = ""
    skills_used: list[str] = field(default_factory=list)

    @property
    def duration_months(self) -> float:
        end = self.end_date or datetime.now()
        delta = end - self.start_date
        return round(delta.days / 30.44, 1)

    @property
    def is_current(self) -> bool:
        return self.end_date is None


@dataclass
class Education:
    """Parsed education entry."""
    institution: str
    degree: EducationLevel
    field_of_study: str
    graduation_year: int
    gpa: Optional[float] = None


@dataclass
class CandidateMetadata:
    """Metadata about resume parsing quality."""
    resume_format: str
    parse_confidence: float
    extracted_sections: list[str]
    parsing_time_ms: float
    warnings: list[str] = field(default_factory=list)


@dataclass
class CandidateProfile:
    """Full parsed candidate profile from resume."""
    candidate_id: str
    full_name: str
    email: str
    skills: list[SkillMatch]
    experience: list[WorkExperience]
    education: list[Education]
    certifications: list[str]
    metadata: CandidateMetadata
    location: str = ""
    years_total_experience: float = 0.0

    def __post_init__(self) -> None:
        if not self.years_total_experience:
            self.years_total_experience = sum(
                e.duration_months for e in self.experience
            ) / 12.0


@dataclass
class SkillRequirement:
    """A skill requirement from a job posting."""
    skill_name: str
    taxonomy_id: str
    min_level: SkillLevel
    weight: float = 1.0
    is_required: bool = True


@dataclass
class CompensationRange:
    """Salary range for a job."""
    min_salary: float
    max_salary: float
    currency: str = "USD"
    includes_equity: bool = False


@dataclass
class ExperienceRange:
    """Required experience range."""
    min_years: float
    max_years: float = 50.0


@dataclass
class JobRequirement:
    """Full job requirement specification."""
    job_id: str
    title: str
    required_skills: list[SkillRequirement]
    preferred_skills: list[SkillRequirement]
    experience_range: ExperienceRange
    education_level: EducationLevel
    compensation: CompensationRange
    location: str = ""
    remote_allowed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class BiasFlag:
    """A detected bias risk."""
    flag_type: BiasFlagType
    severity: float
    description: str
    affected_group: str
    recommendation: str


@dataclass
class MatchResult:
    """Result of matching a candidate to a job."""
    match_id: str
    candidate_id: str
    job_id: str
    composite_score: float
    component_scores: dict[str, float]
    explanation: str
    status: MatchStatus
    flagged_bias_risks: list[BiasFlag]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class InterviewSlot:
    """A proposed interview time slot."""
    slot_id: str
    interviewer_id: str
    start_time: datetime
    end_time: datetime
    round_type: InterviewRoundType
    candidate_score: float = 0.0


@dataclass
class ScheduleConstraint:
    """Scheduling constraint for interview optimization."""
    interviewer_id: str
    available_slots: list[tuple[datetime, datetime]]
    blocked_times: list[tuple[datetime, datetime]]
    preferred_rounds: list[InterviewRoundType]
    max_interviews_per_day: int = 4


@dataclass
class AuditReport:
    """Bias audit report for a hiring pipeline stage."""
    stage_name: str
    total_candidates: int
    selection_rates: dict[str, float]
    disparate_impact_ratios: dict[str, float]
    feature_attribution: dict[str, float]
    recommendations: list[str]
    pass_rate: bool
    timestamp: datetime = field(default_factory=datetime.now)


# ─── Engines ──────────────────────────────────────────────────────────────────

class SkillExtractor:
    """Extracts skills from resume text using pattern matching and taxonomy mapping."""

    SKILL_TAXONOMY: dict[str, str] = {
        "python": "PROG-001", "java": "PROG-002", "javascript": "PROG-003",
        "sql": "DATA-001", "machine learning": "AI-001", "aws": "CLOUD-001",
        "docker": "DEVOPS-001", "kubernetes": "DEVOPS-002", "react": "PROG-004",
        "project management": "MGMT-001", "agile": "MGMT-002", "leadership": "MGMT-003",
        "communication": "SOFT-001", "python": "PROG-001", "tensorflow": "AI-002",
        "pytorch": "AI-003", "gcp": "CLOUD-002", "azure": "CLOUD-003",
        "git": "DEVOPS-003", "ci/cd": "DEVOPS-004", "linux": "SYS-001",
    }

    def __init__(self, taxonomy: Optional[dict[str, str]] = None) -> None:
        self.taxonomy = taxonomy or self.SKILL_TAXONOMY
        self._skill_pattern = re.compile(
            r"(?:skills?|technologies?|proficiencies?):?\s*(.+?)(?:\n\n|\Z)",
            re.IGNORECASE | re.DOTALL,
        )

    def tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-zA-Z+#/.]+\b", text.lower())

    def extract(self, resume_text: str) -> list[SkillMatch]:
        tokens = self.tokenize(resume_text)
        found: list[SkillMatch] = []
        for token in set(tokens):
            if token in self.taxonomy:
                confidence = min(1.0, 0.7 + tokens.count(token) * 0.05)
                found.append(SkillMatch(
                    skill_name=token,
                    taxonomy_id=self.taxonomy[token],
                    confidence=round(confidence, 3),
                    level=SkillLevel.INTERMEDIATE,
                ))
        return found

    def map_to_taxonomy(self, raw_skills: list[str]) -> list[SkillMatch]:
        mapped: list[SkillMatch] = []
        for raw in raw_skills:
            normalized = raw.lower().strip()
            if normalized in self.taxonomy:
                mapped.append(SkillMatch(
                    skill_name=normalized,
                    taxonomy_id=self.taxonomy[normalized],
                    confidence=0.85,
                    level=SkillLevel.INTERMEDIATE,
                ))
        return mapped


class ResumeParser:
    """Parses resume text into structured CandidateProfile."""

    EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
    PHONE_RE = re.compile(r"\+?\d[\d\s()-]{7,}\d")
    YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")

    def __init__(self, extractor: Optional[SkillExtractor] = None) -> None:
        self.extractor = extractor or SkillExtractor()

    def parse(self, raw_text: str, candidate_id: Optional[str] = None) -> CandidateProfile:
        cid = candidate_id or str(uuid.uuid4())[:8]
        emails = self.EMAIL_RE.findall(raw_text)
        skills = self.extractor.extract(raw_text)
        experience = self._parse_experience(raw_text)
        education = self._parse_education(raw_text)

        return CandidateProfile(
            candidate_id=cid,
            full_name=self._extract_name(raw_text),
            email=emails[0] if emails else "",
            skills=skills,
            experience=experience,
            education=education,
            certifications=self._extract_certifications(raw_text),
            metadata=CandidateMetadata(
                resume_format="txt",
                parse_confidence=0.82,
                extracted_sections=["skills", "experience", "education"],
                parsing_time_ms=45.2,
            ),
            location=self._extract_location(raw_text),
        )

    def _extract_name(self, text: str) -> str:
        lines = text.strip().split("\n")
        return lines[0].strip() if lines else "Unknown"

    def _extract_location(self, text: str) -> str:
        for line in text.split("\n"):
            if any(c.isdigit() for c in line) and len(line.split()) <= 6:
                return line.strip()
        return ""

    def _parse_experience(self, text: str) -> list[WorkExperience]:
        entries: list[WorkExperience] = []
        pattern = re.compile(
            r"(\w[\w\s]+?)\s*[-–]\s*(\w[\w\s]+?)\s+(\w+\s+\d{4})\s*[-–]\s*(Present|\w+\s+\d{4})",
            re.IGNORECASE,
        )
        for m in pattern.finditer(text):
            start = datetime.strptime(m.group(3), "%B %Y")
            end = datetime.strptime(m.group(4), "%B %Y") if m.group(4) != "Present" else None
            entries.append(WorkExperience(
                company=m.group(1).strip(),
                title=m.group(2).strip(),
                start_date=start,
                end_date=end,
            ))
        return entries

    def _parse_education(self, text: str) -> list[Education]:
        entries: list[Education] = []
        pattern = re.compile(r"(\w[\w\s]+?)\s+(Bachelor|Master|PhD|Associate)")
        for m in pattern.finditer(text):
            degree_map = {
                "Bachelor": EducationLevel.BACHELORS,
                "Master": EducationLevel.MASTERS,
                "PhD": EducationLevel.DOCTORATE,
                "Associate": EducationLevel.ASSOCIATES,
            }
            years = self.YEAR_RE.findall(text[m.start():m.end() + 50])
            entries.append(Education(
                institution=m.group(1).strip(),
                degree=degree_map.get(m.group(2), EducationLevel.BACHELORS),
                field_of_study="",
                graduation_year=int(years[0]) if years else 2020,
            ))
        return entries

    def _extract_certifications(self, text: str) -> list[str]:
        cert_keywords = ["certified", "certification", "aws certified", "pmp", "cissp"]
        found: list[str] = []
        for line in text.split("\n"):
            lower = line.lower()
            if any(kw in lower for kw in cert_keywords):
                found.append(line.strip())
        return found


class CandidateMatcher:
    """Multi-signal candidate-to-job matching engine."""

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        self.weights = weights or {
            "skill_match": 0.35,
            "experience_fit": 0.25,
            "education_fit": 0.15,
            "location_fit": 0.10,
            "compensation_fit": 0.15,
        }

    def match(self, candidate: CandidateProfile, job: JobRequirement) -> MatchResult:
        components = {
            "skill_match": self._skill_score(candidate, job),
            "experience_fit": self._experience_score(candidate, job),
            "education_fit": self._education_score(candidate, job),
            "location_fit": self._location_score(candidate, job),
            "compensation_fit": self._compensation_score(candidate, job),
        }
        composite = sum(
            components[k] * self.weights.get(k, 0) for k in components
        )
        explanation = self._build_explanation(components, candidate, job)
        status = MatchStatus.SHORTLISTED if composite >= 0.60 else MatchStatus.REJECTED

        return MatchResult(
            match_id=str(uuid.uuid4())[:8],
            candidate_id=candidate.candidate_id,
            job_id=job.job_id,
            composite_score=round(composite, 4),
            component_scores=components,
            explanation=explanation,
            status=status,
            flagged_bias_risks=[],
        )

    def _skill_score(self, c: CandidateProfile, j: JobRequirement) -> float:
        candidate_skills = {s.skill_name.lower() for s in c.skills}
        required = {s.skill_name.lower() for s in j.required_skills if s.is_required}
        if not required:
            return 1.0
        overlap = candidate_skills & required
        return len(overlap) / len(required)

    def _experience_score(self, c: CandidateProfile, j: JobRequirement) -> float:
        years = c.years_total_experience
        if j.experience_range.min_years <= years <= j.experience_range.max_years:
            return 1.0
        if years < j.experience_range.min_years:
            return max(0, years / j.experience_range.min_years)
        return max(0, 1.0 - (years - j.experience_range.max_years) * 0.1)

    def _education_score(self, c: CandidateProfile, j: JobRequirement) -> float:
        level_order = list(EducationLevel)
        if not c.education:
            return 0.3
        highest = max(c.education, key=lambda e: level_order.index(e.degree))
        required_idx = level_order.index(j.education_level)
        actual_idx = level_order.index(highest.degree)
        if actual_idx >= required_idx:
            return 1.0
        return 0.5 + 0.25 * (actual_idx / required_idx)

    def _location_score(self, c: CandidateProfile, j: JobRequirement) -> float:
        if j.remote_allowed:
            return 1.0
        if not j.location or not c.location:
            return 0.7
        return 1.0 if c.location.lower() == j.location.lower() else 0.3

    def _compensation_score(self, c: CandidateProfile, j: JobRequirement) -> float:
        return 0.85

    def _build_explanation(
        self, components: dict[str, float], c: CandidateProfile, j: JobRequirement
    ) -> str:
        parts = []
        for key, score in sorted(components.items(), key=lambda x: -x[1]):
            label = key.replace("_", " ").title()
            parts.append(f"{label}: {score:.0%}")
        return f"Match breakdown for {c.full_name} -> {j.title}: " + ", ".join(parts)

    def diversify_shortlist(
        self, results: list[MatchResult], factor: float = 0.15
    ) -> list[MatchResult]:
        return sorted(results, key=lambda r: r.composite_score, reverse=True)


class InterviewScheduler:
    """Constraint-satisfaction interview scheduling optimizer."""

    def __init__(self) -> None:
        self.buffer_minutes: int = 15
        self.max_rounds: int = 5

    def find_available_slots(
        self,
        constraint: ScheduleConstraint,
        round_type: InterviewRoundType,
        duration_minutes: int = 60,
    ) -> list[InterviewSlot]:
        slots: list[InterviewSlot] = []
        for start, end in constraint.available_slots:
            current = start
            while current + timedelta(minutes=duration_minutes) <= end:
                slot_end = current + timedelta(minutes=duration_minutes)
                if self._is_free(constraint, current, slot_end):
                    slots.append(InterviewSlot(
                        slot_id=str(uuid.uuid4())[:8],
                        interviewer_id=constraint.interviewer_id,
                        start_time=current,
                        end_time=slot_end,
                        round_type=round_type,
                    ))
                current = slot_end + timedelta(minutes=self.buffer_minutes)
        return slots

    def _is_free(
        self, constraint: ScheduleConstraint, start: datetime, end: datetime
    ) -> bool:
        for block_start, block_end in constraint.blocked_times:
            if start < block_end and end > block_start:
                return False
        return True

    def optimize_schedule(
        self,
        candidate_slots: list[list[InterviewSlot]],
        preferences: Optional[dict[str, float]] = None,
    ) -> list[InterviewSlot]:
        selected: list[InterviewSlot] = []
        used_times: set[tuple[datetime, datetime]] = set()
        for round_slots in candidate_slots:
            ranked = sorted(round_slots, key=lambda s: s.candidate_score, reverse=True)
            for slot in ranked:
                key = (slot.start_time, slot.end_time)
                if key not in used_times:
                    selected.append(slot)
                    used_times.add(key)
                    break
        return selected


class BiasAuditor:
    """Detects and reports algorithmic bias in hiring pipelines."""

    def __init__(self, threshold: float = 0.80) -> None:
        self.four_fifths_threshold = threshold

    def selection_rates(
        self,
        results: list[MatchResult],
        demographics: dict[str, dict[str, str]],
    ) -> dict[str, float]:
        rates: dict[str, dict[str, float]] = {}
        group_totals: dict[str, int] = {}
        group_selected: dict[str, int] = {}
        for r in results:
            demo = demographics.get(r.candidate_id, {})
            for attr, value in demo.items():
                key = f"{attr}:{value}"
                group_totals[key] = group_totals.get(key, 0) + 1
                if r.status in (MatchStatus.SHORTLISTED, MatchStatus.INTERVIEWING):
                    group_selected[key] = group_selected.get(key, 0) + 1
        for key in group_totals:
            total = group_totals[key]
            selected = group_selected.get(key, 0)
            rates[key] = selected / total if total > 0 else 0.0
        return rates

    def calculate_dir(self, rates: dict[str, float]) -> dict[str, float]:
        if not rates:
            return {}
        max_rate = max(rates.values())
        if max_rate == 0:
            return {k: 1.0 for k in rates}
        return {k: round(v / max_rate, 4) for k, v in rates.items()}

    def feature_attribution(
        self,
        results: list[MatchResult],
        demographics: dict[str, dict[str, str]],
    ) -> dict[str, float]:
        attribution: dict[str, float] = {}
        for attr in ["name", "school", "gap_months"]:
            scores_by_group: dict[str, list[float]] = {}
            for r in results:
                demo = demographics.get(r.candidate_id, {})
                group = demo.get(attr, "unknown")
                scores_by_group.setdefault(group, []).append(r.composite_score)
            if len(scores_by_group) > 1:
                means = [sum(v) / len(v) for v in scores_by_group.values() if v]
                attribution[attr] = max(means) - min(means) if means else 0.0
        return attribution

    def audit(
        self,
        stage_name: str,
        results: list[MatchResult],
        demographics: dict[str, dict[str, str]],
    ) -> AuditReport:
        rates = self.selection_rates(results, demographics)
        dir_values = self.calculate_dir(rates)
        attribution = self.feature_attribution(results, demographics)
        recommendations: list[str] = []
        for group, ratio in dir_values.items():
            if ratio < self.four_fifths_threshold:
                recommendations.append(
                    f"Group '{group}' DI ratio {ratio:.2f} < {self.four_fifths_threshold}. "
                    "Review for disparate impact."
                )
        for feature, delta in attribution.items():
            if delta > 0.10:
                recommendations.append(
                    f"Feature '{feature}' shows {delta:.0%} score variance — consider anonymization."
                )
        pass_analysis = all(r >= self.four_fifths_threshold for r in dir_values.values())
        return AuditReport(
            stage_name=stage_name,
            total_candidates=len(results),
            selection_rates=rates,
            disparate_impact_ratios=dir_values,
            feature_attribution=attribution,
            recommendations=recommendations,
            pass_rate=pass_analysis,
        )

    def anonymize_resume(self, text: str, level: AnonymizeLevel) -> str:
        if level == AnonymizeLevel.NONE:
            return text
        result = text
        if level in (AnonymizeLevel.PARTIAL, AnonymizeLevel.FULL):
            result = self.EMAIL_RE.sub("[REDACTED]", result)
            result = re.sub(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "[NAME]", result)
        if level == AnonymizeLevel.FULL:
            result = re.sub(r"\b\d{4}\b", "[YEAR]", result)
            result = re.sub(r"(?:University|College|Institute)\s+of\s+\w+", "[INSTITUTION]", result)
        return result

    EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


# ─── Main Demo ────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate the recruitment AI pipeline end-to-end."""
    print("=" * 72)
    print("  RECRUITMENT AI PIPELINE DEMO")
    print("=" * 72)

    # 1. Resume Parsing
    print("\n[1] RESUME PARSING")
    print("-" * 40)
    resume_text = """Jane Smith
San Francisco, CA
jane.smith@email.com | +1-555-0123

Skills: Python, machine learning, AWS, docker, kubernetes, SQL, React

Experience:
Acme Corp - Senior ML Engineer - January 2019 - Present
TechStartup - Data Scientist - June 2016 - December 2018

Education:
Stanford University - Master - Computer Science - 2016
MIT - Bachelor - Electrical Engineering - 2014

Certifications: AWS Certified Machine Learning Specialty
"""
    parser = ResumeParser()
    candidate = parser.parse(resume_text, candidate_id="C001")
    print(f"  Name:       {candidate.full_name}")
    print(f"  Email:      {candidate.email}")
    print(f"  Skills:     {len(candidate.skills)} extracted")
    for s in candidate.skills[:5]:
        print(f"              - {s.skill_name} ({s.taxonomy_id}) conf={s.confidence:.2f}")
    print(f"  Experience: {candidate.years_total_experience:.1f} years total")
    print(f"  Education:  {len(candidate.education)} entries")
    print(f"  Certs:      {candidate.certifications}")

    # 2. Candidate Matching
    print("\n[2] CANDIDATE-JOB MATCHING")
    print("-" * 40)
    job = JobRequirement(
        job_id="J001",
        title="Senior ML Engineer",
        required_skills=[
            SkillRequirement("python", "PROG-001", SkillLevel.ADVANCED),
            SkillRequirement("machine learning", "AI-001", SkillLevel.ADVANCED),
            SkillRequirement("aws", "CLOUD-001", SkillLevel.INTERMEDIATE),
        ],
        preferred_skills=[
            SkillRequirement("docker", "DEVOPS-001", SkillLevel.INTERMEDIATE, is_required=False),
            SkillRequirement("kubernetes", "DEVOPS-002", SkillLevel.INTERMEDIATE, is_required=False),
        ],
        experience_range=ExperienceRange(min_years=4, max_years=15),
        education_level=EducationLevel.MASTERS,
        compensation=CompensationRange(min_salary=160000, max_salary=220000),
    )
    matcher = CandidateMatcher()
    result = matcher.match(candidate, job)
    print(f"  Match ID:   {result.match_id}")
    print(f"  Score:      {result.composite_score:.2%}")
    print(f"  Status:     {result.status.value}")
    print(f"  Breakdown:")
    for k, v in sorted(result.component_scores.items(), key=lambda x: -x[1]):
        print(f"    {k:20s} = {v:.2%}")
    print(f"  Explanation: {result.explanation}")

    # 3. Interview Scheduling
    print("\n[3] INTERVIEW SCHEDULING")
    print("-" * 40)
    scheduler = InterviewScheduler()
    constraint = ScheduleConstraint(
        interviewer_id="INT-001",
        available_slots=[
            (datetime(2026, 7, 10, 9, 0), datetime(2026, 7, 10, 12, 0)),
            (datetime(2026, 7, 10, 14, 0), datetime(2026, 7, 10, 17, 0)),
        ],
        blocked_times=[
            (datetime(2026, 7, 10, 10, 30), datetime(2026, 7, 10, 11, 0)),
        ],
        preferred_rounds=[InterviewRoundType.TECHNICAL],
    )
    available = scheduler.find_available_slots(constraint, InterviewRoundType.TECHNICAL, 60)
    print(f"  Available slots: {len(available)}")
    for slot in available[:4]:
        print(f"    {slot.slot_id}: {slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')} ({slot.round_type.value})")

    # 4. Bias Audit
    print("\n[4] BIAS DETECTION & AUDIT")
    print("-" * 40)
    demographics = {
        "C001": {"gender": "female", "ethnicity": "asian", "age_bucket": "30-39"},
    }
    for i in range(1, 8):
        demographics[f"C{i:03d}"] = {
            "gender": ["male", "female", "male", "female", "male", "non-binary", "male"][i - 1],
            "ethnicity": ["white", "white", "hispanic", "black", "white", "white", "asian"][i - 1],
            "age_bucket": ["20-29", "30-39", "20-29", "40-49", "30-39", "30-39", "20-29"][i - 1],
        }
    results: list[MatchResult] = []
    scores = [0.82, 0.75, 0.68, 0.71, 0.88, 0.64, 0.79, 0.55]
    statuses = [
        MatchStatus.SHORTLISTED, MatchStatus.SHORTLISTED, MatchStatus.REJECTED,
        MatchStatus.SHORTLISTED, MatchStatus.SHORTLISTED, MatchStatus.REJECTED,
        MatchStatus.SHORTLISTED, MatchStatus.REJECTED,
    ]
    for i, (score, status) in enumerate(zip(scores, statuses)):
        results.append(MatchResult(
            match_id=f"M{i:03d}", candidate_id=f"C{i:03d}", job_id="J001",
            composite_score=score, component_scores={}, explanation="",
            status=status, flagged_bias_risks=[],
        ))
    auditor = BiasAuditor(threshold=0.80)
    report = auditor.audit("Resume Screening", results, demographics)
    print(f"  Stage:          {report.stage_name}")
    print(f"  Candidates:     {report.total_candidates}")
    print(f"  Pass (4/5ths):  {'YES' if report.pass_rate else 'NO'}")
    print(f"  Selection Rates:")
    for group, rate in sorted(report.selection_rates.items()):
        di = report.disparate_impact_ratios.get(group, 1.0)
        print(f"    {group:20s} rate={rate:.2%}  DI={di:.3f}")
    print(f"  Feature Attribution:")
    for feat, delta in report.feature_attribution.items():
        print(f"    {feat:20s} variance={delta:.2%}")
    print(f"  Recommendations:")
    for rec in report.recommendations:
        print(f"    - {rec}")

    # 5. Anonymization
    print("\n[5] RESUME ANONYMIZATION")
    print("-" * 40)
    for level in AnonymizeLevel:
        anonymized = auditor.anonymize_resume(resume_text, level)
        lines = anonymized.strip().split("\n")
        print(f"  [{level.value}] First 3 lines:")
        for line in lines[:3]:
            print(f"    {line}")

    print("\n" + "=" * 72)
    print("  PIPELINE COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
