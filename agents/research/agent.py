"""
Research Agent
===============
Comprehensive research methodology, literature review, experiment design,
data collection, analysis, academic writing, and citation management.

This agent provides a complete research operations framework including:
- Research question formulation
- Literature review and synthesis
- Experiment design and methodology
- Data collection and management
- Statistical analysis
- Academic writing and formatting
- Citation management (APA, MLA, IEEE, Harvard, Chicago)
- Knowledge graph construction
- Hypothesis generation and testing
"""

import hashlib
import logging
import re
import statistics
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


# =============================================================================
# Enums
# =============================================================================

class SourceType(Enum):
    """Types of research sources."""
    ACADEMIC = "academic"
    JOURNAL_ARTICLE = "journal_article"
    CONFERENCE_PAPER = "conference_paper"
    THESIS = "thesis"
    BOOK = "book"
    BOOK_CHAPTER = "book_chapter"
    INDUSTRY = "industry"
    WHITE_PAPER = "white_paper"
    TECH_REPORT = "tech_report"
    NEWS = "news"
    BLOG = "blog"
    DOCUMENTATION = "documentation"
    VIDEO = "video"
    PATENT = "patent"
    GOVERNMENT = "government"
    DATASET = "dataset"
    PREPRINT = "preprint"
    THESIS_DISSERTATION = "thesis_dissertation"


class CitationStyle(Enum):
    """Academic citation styles."""
    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"
    IEEE = "ieee"
    HARVARD = "harvard"
    VANCOUVER = "vancouver"
    ACS = "acs"
    AMA = "ama"
    TURABIAN = "turabian"


class ResearchPhase(Enum):
    """Phases of the research process."""
    QUESTION_FORMULATION = "question_formulation"
    LITERATURE_REVIEW = "literature_review"
    METHODOLOGY_DESIGN = "methodology_design"
    DATA_COLLECTION = "data_collection"
    DATA_ANALYSIS = "data_analysis"
    INTERPRETATION = "interpretation"
    WRITING = "writing"
    PEER_REVIEW = "peer_review"
    PUBLICATION = "publication"


class EvidenceStrength(Enum):
    """Strength of evidence."""
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    ANECDOTAL = "anecdotal"
    CONFLICTING = "conflicting"
    INSUFFICIENT = "insufficient"


class MethodologyType(Enum):
    """Research methodology types."""
    QUANTITATIVE = "quantitative"
    QUALITATIVE = "qualitative"
    MIXED_METHODS = "mixed_methods"
    EXPERIMENTAL = "experimental"
    OBSERVATIONAL = "observational"
    CASE_STUDY = "case_study"
    SURVEY = "survey"
    META_ANALYSIS = "meta_analysis"
    SYSTEMATIC_REVIEW = "systematic_review"
    ACTION_RESEARCH = "action_research"
    GROUNDED_THEORY = "grounded_theory"
    ETHNOGRAPHY = "ethnography"
    LONGITUDINAL = "longitudinal"
    CROSS_SECTIONAL = "cross_sectional"


class StatisticalTest(Enum):
    """Statistical tests for analysis."""
    T_TEST = "t_test"
    CHI_SQUARE = "chi_square"
    ANOVA = "anova"
    MANOVA = "manova"
    CORRELATION = "correlation"
    REGRESSION = "regression"
    LOGISTIC_REGRESSION = "logistic_regression"
    MANN_WHITNEY = "mann_whitney"
    KRUSKAL_WALLIS = "kruskal_wallis"
    WILCOXON = "wilcoxon"
    FISHER_EXACT = "fisher_exact"
    MCMC = "mcmc"
    BOOTSTRAP = "bootstrap"
    PERMUTATION = "permutation"


class BiasType(Enum):
    """Types of research bias."""
    SELECTION = "selection"
    CONFIRMATION = "confirmation"
    PUBLICATION = "publication"
    SURVIVORSHIP = "survivorship"
    ANCHORING = "anchoring"
    AVAILABILITY = "availability"
    DEMAND_CHARACTERISTICS = "demand_characteristics"
    EXPERIMENTER = "experimenter"
    RECALL = "recall"
    NON_RESPONSE = "non_response"
    MEASUREMENT = "measurement"
    ATTRITION = "attrition"


class WritingFormat(Enum):
    """Academic writing formats."""
    APA_PAPER = "apa_paper"
    IEEE_PAPER = "ieee_paper"
    LATEX = "latex"
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    LITERATURE_REVIEW = "literature_review"
    METHODOLOGY = "methodology"
    RESULTS = "results"
    DISCUSSION = "discussion"
    ABSTRACT = "abstract"
    EXECUTIVE_SUMMARY = "executive_summary"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class ResearchQuestion:
    """A formulated research question."""
    id: str
    question: str
    sub_questions: List[str] = field(default_factory=list)
    priority: int = 1
    keywords: List[str] = field(default_factory=list)
    methodology_suggestion: Optional[MethodologyType] = None
    scope: str = ""
    significance: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Source:
    """A research source/reference."""
    id: str
    title: str
    authors: List[str] = field(default_factory=list)
    source_type: SourceType = SourceType.ACADEMIC
    url: str = ""
    publication_date: Optional[datetime] = None
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    citations: int = 0
    relevance_score: float = 0.0
    doi: Optional[str] = None
    isbn: Optional[str] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    edition: Optional[str] = None
    access_date: Optional[datetime] = None
    peer_reviewed: bool = False
    impact_factor: Optional[float] = None


@dataclass
class ResearchFinding:
    """A finding from research analysis."""
    source_id: str
    finding: str
    evidence_strength: EvidenceStrength = EvidenceStrength.MODERATE
    page_number: Optional[int] = None
    quote: Optional[str] = None
    notes: str = ""
    themes: List[str] = field(default_factory=list)
    methodology_used: Optional[MethodologyType] = None
    sample_size: Optional[int] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    p_value: Optional[float] = None


@dataclass
class Hypothesis:
    """A research hypothesis."""
    id: str
    statement: str
    hypothesis_type: str = "alternative"  # null, alternative, directional
    variables: Dict[str, str] = field(default_factory=dict)
    operationalization: str = ""
    test_method: Optional[StatisticalTest] = None
    status: str = "proposed"  # proposed, tested, supported, rejected
    evidence_for: List[str] = field(default_factory=list)
    evidence_against: List[str] = field(default_factory=list)


@dataclass
class Experiment:
    """An experimental design."""
    id: str
    title: str
    hypothesis_id: str
    methodology: MethodologyType
    variables: Dict[str, List[str]] = field(default_factory=dict)
    sample_size: int = 0
    control_group: bool = True
    randomization: bool = True
    blinding: str = "none"  # none, single, double
    duration: Optional[str] = None
    irb_approval: bool = False
    power_analysis: Optional[float] = None
    effect_size: Optional[float] = None
    alpha: float = 0.05
    status: str = "designed"  # designed, running, completed, failed


@dataclass
class DataPoint:
    """A single data point."""
    id: str
    experiment_id: str
    variable: str
    value: Any
    unit: Optional[str] = None
    timestamp: Optional[datetime] = None
    participant_id: Optional[str] = None
    condition: Optional[str] = None
    notes: str = ""


@dataclass
class AnalysisResult:
    """Result of a statistical analysis."""
    test: StatisticalTest
    statistic: float
    p_value: float
    effect_size: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    interpretation: str = ""
    significant: bool = False
    assumptions_met: bool = True
    assumptions_violated: List[str] = field(default_factory=list)


@dataclass
class LiteratureReview:
    """A completed literature review."""
    id: str
    topic: str
    research_questions: List[ResearchQuestion] = field(default_factory=list)
    sources: List[Source] = field(default_factory=list)
    findings: List[ResearchFinding] = field(default_factory=list)
    themes: Dict[str, List[str]] = field(default_factory=dict)
    gaps: List[str] = field(default_factory=list)
    contradictions: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    executive_summary: str = ""
    word_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ResearchPaper:
    """A research paper structure."""
    id: str
    title: str
    authors: List[str] = field(default_factory=list)
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    introduction: str = ""
    literature_review: str = ""
    methodology: str = ""
    results: str = ""
    discussion: str = ""
    conclusion: str = ""
    references: List[Source] = field(default_factory=list)
    appendices: Dict[str, str] = field(default_factory=dict)
    citations_style: CitationStyle = CitationStyle.APA
    word_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class KnowledgeNode:
    """A node in the knowledge graph."""
    id: str
    label: str
    node_type: str  # concept, entity, finding, methodology
    properties: Dict[str, Any] = field(default_factory=dict)
    connections: List[str] = field(default_factory=list)


@dataclass
class KnowledgeEdge:
    """An edge in the knowledge graph."""
    source_id: str
    target_id: str
    relationship: str  # supports, contradicts, extends, uses
    weight: float = 1.0
    evidence: List[str] = field(default_factory=list)


# =============================================================================
# Research Indexer
# =============================================================================

class ResearchIndexer:
    """Indexes, searches, and manages research sources."""

    def __init__(self) -> None:
        self.index: Dict[str, List[str]] = defaultdict(list)
        self.sources: Dict[str, Source] = {}
        self.keyword_map: Dict[str, Set[str]] = defaultdict(set)
        self.author_index: Dict[str, Set[str]] = defaultdict(set)
        self.year_index: Dict[int, Set[str]] = defaultdict(set)
        self.type_index: Dict[SourceType, Set[str]] = defaultdict(set)

    def add_source(self, source: Source) -> None:
        """Add a source to the index."""
        self.sources[source.id] = source

        # Index by keywords
        for keyword in source.keywords:
            kw_lower = keyword.lower()
            self.keyword_map[kw_lower].add(source.id)
            for token in kw_lower.split():
                self.index[token].add(source.id)

        # Index by authors
        for author in source.authors:
            self.author_index[author.lower()].add(source.id)

        # Index by year
        if source.publication_date:
            self.year_index[source.publication_date.year].add(source.id)

        # Index by type
        self.type_index[source.source_type].add(source.id)

        logger.info(f"Source indexed: {source.id} ({source.title})")

    def search(self, query: str, source_type: Optional[SourceType] = None,
               limit: int = 10, min_relevance: float = 0.0) -> List[Source]:
        """Search indexed sources with relevance ranking."""
        query_terms = query.lower().split()
        scores: Dict[str, float] = defaultdict(float)

        for term in query_terms:
            for source_id in self.index.get(term, []):
                scores[source_id] += 1.0
                if source_id in self.sources:
                    source = self.sources[source_id]
                    if any(term in kw.lower() for kw in source.keywords):
                        scores[source_id] += 0.5
                    if term in source.title.lower():
                        scores[source_id] += 1.0
                    if any(term in a.lower() for a in source.authors):
                        scores[source_id] += 0.3

        sorted_ids = sorted(scores.items(), key=lambda x: -x[1])
        results: List[Source] = []

        for source_id, score in sorted_ids:
            if source_id in self.sources:
                source = self.sources[source_id]
                if source_type and source.source_type != source_type:
                    continue
                if score / max(len(query_terms), 1) < min_relevance:
                    continue
                source.relevance_score = score / max(len(query_terms), 1)
                results.append(source)
                if len(results) >= limit:
                    break

        return results

    def search_by_author(self, author: str) -> List[Source]:
        """Search sources by author name."""
        author_lower = author.lower()
        source_ids = set()
        for indexed_author, ids in self.author_index.items():
            if author_lower in indexed_author:
                source_ids.update(ids)
        return [self.sources[sid] for sid in source_ids if sid in self.sources]

    def search_by_year(self, year: int) -> List[Source]:
        """Search sources by publication year."""
        source_ids = self.year_index.get(year, set())
        return [self.sources[sid] for sid in source_ids if sid in self.sources]

    def get_cited_by(self, source_id: str) -> List[Source]:
        """Find sources that cite a given source."""
        cited_by: List[Source] = []
        for source in self.sources.values():
            if source_id in source.abstract.lower() or source_id in source.keywords:
                cited_by.append(source)
        return cited_by

    def get_most_cited(self, limit: int = 10) -> List[Source]:
        """Get the most cited sources."""
        sorted_sources = sorted(
            self.sources.values(),
            key=lambda s: s.citations,
            reverse=True
        )
        return sorted_sources[:limit]

    def get_recent(self, days: int = 365, limit: int = 10) -> List[Source]:
        """Get recently published sources."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            s for s in self.sources.values()
            if s.publication_date and s.publication_date >= cutoff
        ]
        return sorted(recent, key=lambda s: s.publication_date or datetime.min, reverse=True)[:limit]


# =============================================================================
# Literature Analyzer
# =============================================================================

class LiteratureAnalyzer:
    """Analyzes literature for themes, gaps, trends, and patterns."""

    def __init__(self) -> None:
        self.themes: Dict[str, List[str]] = defaultdict(list)
        self.timeline: Dict[int, List[str]] = defaultdict(list)
        self.citation_network: Dict[str, Set[str]] = defaultdict(set)
        self.methodology_distribution: Dict[str, int] = Counter()
        self.geographic_distribution: Dict[str, int] = Counter()

    def analyze(self, sources: List[Source]) -> Dict[str, Any]:
        """Perform comprehensive literature analysis."""
        for source in sources:
            self._extract_themes(source)
            self._build_timeline(source)
            self._build_citation_network(source)
            self._analyze_methodology(source)

        return {
            "themes": dict(self.themes),
            "publication_timeline": dict(self.timeline),
            "citation_patterns": {k: list(v) for k, v in self.citation_network.items()},
            "methodology_distribution": dict(self.methodology_distribution),
            "total_sources": len(sources),
            "year_range": self._get_year_range(),
            "avg_citations": self._avg_citations(sources),
        }

    def identify_gaps(self, sources: List[Source],
                      research_questions: List[ResearchQuestion]) -> List[str]:
        """Identify gaps in the literature."""
        gaps: List[str] = []

        # Check for sub-questions without coverage
        for rq in research_questions:
            for sub_q in rq.sub_questions:
                covered = False
                for source in sources:
                    if any(kw in source.abstract.lower() for kw in sub_q.lower().split()):
                        covered = True
                        break
                if not covered:
                    gaps.append(f"No coverage for sub-question: {sub_q}")

        # Check for methodology gaps
        method_counts = self.methodology_distribution
        if method_counts.get("experimental", 0) < 3:
            gaps.append("Limited experimental studies")
        if method_counts.get("meta_analysis", 0) < 1:
            gaps.append("No meta-analysis found")
        if method_counts.get("longitudinal", 0) < 2:
            gaps.append("Few longitudinal studies")

        # Check for temporal gaps
        years = sorted(self.timeline.keys())
        if len(years) >= 2:
            gaps_in_years = []
            for i in range(len(years) - 1):
                if years[i + 1] - years[i] > 2:
                    gaps_in_years.append(f"Publication gap between {years[i]} and {years[i+1]}")
            gaps.extend(gaps_in_years)

        # Check for contradiction-based gaps
        contradictions = self.detect_contradictions(sources)
        if contradictions:
            gaps.append(f"{len(contradictions)} contradictory findings need resolution")

        return gaps

    def detect_contradictions(self, sources: List[Source]) -> List[Dict[str, Any]]:
        """Detect contradictory findings across sources."""
        contradictions: List[Dict[str, Any]] = []

        source_list = list(sources)
        for i, s1 in enumerate(source_list):
            for s2 in source_list[i + 1:]:
                similarity = self._text_similarity(s1.abstract, s2.abstract)
                if 0.1 < similarity < 0.4:
                    contradictions.append({
                        "source_1": s1.id,
                        "source_2": s2.id,
                        "title_1": s1.title,
                        "title_2": s2.title,
                        "similarity": similarity,
                        "note": "Low similarity with overlapping keywords may indicate contradiction",
                    })

        return contradictions

    def generate_trend_analysis(self, sources: List[Source]) -> Dict[str, Any]:
        """Analyze publication trends over time."""
        year_counts: Dict[int, int] = Counter()
        for source in sources:
            if source.publication_date:
                year_counts[source.publication_date.year] += 1

        years = sorted(year_counts.keys())
        counts = [year_counts[y] for y in years]

        trend = "increasing" if len(counts) > 1 and counts[-1] > counts[0] else "stable"

        return {
            "year_range": f"{min(years)}-{max(years)}" if years else "N/A",
            "total_publications": len(sources),
            "publications_per_year": dict(year_counts),
            "trend": trend,
            "peak_year": max(year_counts, key=year_counts.get) if year_counts else None,
        }

    def _extract_themes(self, source: Source) -> None:
        """Extract themes from a source."""
        theme_keywords = [
            "methodology", "theory", "application", "review", "empirical",
            "case_study", "experiment", "survey", "meta_analysis", "framework",
            "model", "algorithm", "optimization", "evaluation", "comparison",
        ]
        text = (source.abstract + " " + " ".join(source.keywords)).lower()
        for theme in theme_keywords:
            if theme in text:
                self.themes[theme].append(source.id)

    def _build_timeline(self, source: Source) -> None:
        """Add source to publication timeline."""
        if source.publication_date:
            year = source.publication_date.year
            self.timeline[year].append(source.id)

    def _build_citation_network(self, source: Source) -> None:
        """Build citation relationships."""
        for keyword in source.keywords:
            self.citation_network[source.id].add(keyword)

    def _analyze_methodology(self, source: Source) -> None:
        """Extract methodology information from source."""
        text = (source.abstract + " " + source.title).lower()
        methods = {
            "experimental": ["experiment", "controlled", "randomized"],
            "survey": ["survey", "questionnaire", "respondents"],
            "case_study": ["case study", "case studies", "qualitative"],
            "meta_analysis": ["meta-analysis", "systematic review", "pooled"],
            "longitudinal": ["longitudinal", "follow-up", "over time"],
            "cross_sectional": ["cross-sectional", "snapshot", "prevalence"],
        }
        for method, keywords in methods.items():
            if any(kw in text for kw in keywords):
                self.methodology_distribution[method] += 1

    def _get_year_range(self) -> str:
        """Get the year range of publications."""
        years = sorted(self.timeline.keys())
        if not years:
            return "N/A"
        return f"{min(years)}-{max(years)}"

    def _avg_citations(self, sources: List[Source]) -> float:
        """Calculate average citations."""
        if not sources:
            return 0.0
        return sum(s.citations for s in sources) / len(sources)

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0


# =============================================================================
# Research Synthesizer
# =============================================================================

class ResearchSynthesizer:
    """Synthesizes research findings into coherent narratives."""

    def __init__(self) -> None:
        self.findings: List[ResearchFinding] = []
        self.theme_groups: Dict[str, List[ResearchFinding]] = defaultdict(list)
        self.evidence_hierarchy: Dict[EvidenceStrength, List[ResearchFinding]] = defaultdict(list)

    def add_finding(self, finding: ResearchFinding) -> None:
        """Add a research finding."""
        self.findings.append(finding)
        self.evidence_hierarchy[finding.evidence_strength].append(finding)
        for theme in finding.themes:
            self.theme_groups[theme].append(finding)

    def synthesize(self, research_questions: List[ResearchQuestion]) -> Dict[str, Any]:
        """Synthesize findings into answers for research questions."""
        answers: Dict[str, Any] = {}

        for question in research_questions:
            relevant = self._get_relevant_findings(question)

            if relevant:
                strong = [f for f in relevant if f.evidence_strength == EvidenceStrength.STRONG]
                moderate = [f for f in relevant if f.evidence_strength == EvidenceStrength.MODERATE]
                weak = [f for f in relevant if f.evidence_strength == EvidenceStrength.WEAK]

                answers[question.id] = {
                    "question": question.question,
                    "summary": self._generate_summary(relevant),
                    "strong_evidence_count": len(strong),
                    "moderate_evidence_count": len(moderate),
                    "weak_evidence_count": len(weak),
                    "total_evidence": len(relevant),
                    "evidence_gaps": self._identify_gaps(relevant, question),
                    "confidence_level": self._calculate_confidence(strong, moderate, weak),
                    "key_findings": [f.finding for f in strong[:5]],
                }
            else:
                answers[question.id] = {
                    "question": question.question,
                    "summary": "Insufficient evidence found",
                    "strong_evidence_count": 0,
                    "moderate_evidence_count": 0,
                    "weak_evidence_count": 0,
                    "total_evidence": 0,
                    "evidence_gaps": [f"No evidence found for: {question.question}"],
                    "confidence_level": "none",
                    "key_findings": [],
                }

        return answers

    def generate_narrative(self, theme: Optional[str] = None) -> str:
        """Generate a narrative synthesis of findings."""
        if theme:
            findings = self.theme_groups.get(theme, [])
        else:
            findings = self.findings

        if not findings:
            return "No findings to synthesize."

        narrative_parts = [
            f"The synthesis of {len(findings)} findings reveals the following key insights:",
            "",
        ]

        # Group by evidence strength
        for strength in [EvidenceStrength.STRONG, EvidenceStrength.MODERATE, EvidenceStrength.WEAK]:
            strength_findings = [f for f in findings if f.evidence_strength == strength]
            if strength_findings:
                narrative_parts.append(f"**{strength.value.capitalize()} Evidence ({len(strength_findings)} findings):**")
                for f in strength_findings[:3]:
                    narrative_parts.append(f"- {f.finding}")
                narrative_parts.append("")

        # Identify convergent themes
        all_themes = set()
        for f in findings:
            all_themes.update(f.themes)

        if all_themes:
            narrative_parts.append("**Cross-cutting themes:**")
            for theme in sorted(all_themes):
                count = len(self.theme_groups.get(theme, []))
                narrative_parts.append(f"- {theme}: {count} related findings")

        return "\n".join(narrative_parts)

    def identify_contradictions(self) -> List[Dict[str, Any]]:
        """Identify contradictory findings."""
        contradictions: List[Dict[str, Any]] = []

        for i, f1 in enumerate(self.findings):
            for f2 in self.findings[i + 1:]:
                similarity = self._calculate_similarity(f1.finding, f2.finding)
                if similarity < 0.2:
                    contradictions.append({
                        "finding_1": f1.finding[:150],
                        "finding_2": f2.finding[:150],
                        "source_1": f1.source_id,
                        "source_2": f2.source_id,
                        "evidence_1": f1.evidence_strength.value,
                        "evidence_2": f2.evidence_strength.value,
                    })

        return contradictions

    def _get_relevant_findings(self, question: ResearchQuestion) -> List[ResearchFinding]:
        """Get findings relevant to a research question."""
        relevant: List[ResearchFinding] = []
        keywords = set(kw.lower() for kw in question.keywords)
        question_words = set(question.question.lower().split())

        for finding in self.findings:
            finding_words = set(finding.finding.lower().split())
            theme_words = set(t.lower() for t in finding.themes)

            # Check keyword overlap
            if keywords & finding_words or keywords & theme_words:
                relevant.append(finding)
            # Check question word overlap (need at least 2)
            elif len(question_words & finding_words) >= 2:
                relevant.append(finding)

        return relevant

    def _generate_summary(self, findings: List[ResearchFinding]) -> str:
        """Generate a summary from findings."""
        if not findings:
            return "No findings available."

        key_points = set()
        for f in findings:
            sentences = f.finding.split(".")
            for sent in sentences[:2]:
                cleaned = sent.strip()
                if cleaned and len(cleaned) > 10:
                    key_points.add(cleaned)

        return ". ".join(sorted(key_points)[:5])

    def _identify_gaps(self, findings: List[ResearchFinding],
                       question: ResearchQuestion) -> List[str]:
        """Identify gaps in evidence for a question."""
        gaps: List[str] = []
        answered_subqs = set()

        for f in findings:
            for sub_q in question.sub_questions:
                if sub_q.lower() in f.finding.lower():
                    answered_subqs.add(sub_q)

        for sub_q in question.sub_questions:
            if sub_q not in answered_subqs:
                gaps.append(f"Sub-question not addressed: {sub_q}")

        return gaps

    def _calculate_confidence(self, strong: List, moderate: List,
                              weak: List) -> str:
        """Calculate overall confidence level."""
        total = len(strong) + len(moderate) + len(weak)
        if total == 0:
            return "none"
        strong_ratio = len(strong) / total
        if strong_ratio >= 0.6:
            return "high"
        elif strong_ratio >= 0.3:
            return "moderate"
        elif len(strong) > 0:
            return "low"
        return "very_low"

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)


# =============================================================================
# Citation Manager
# =============================================================================

class CitationManager:
    """Manages citations, references, and bibliographies."""

    def __init__(self) -> None:
        self.references: Dict[str, Source] = {}
        self.citation_map: Dict[str, List[str]] = defaultdict(list)
        self.style_formatters: Dict[CitationStyle, Callable] = {
            CitationStyle.APA: self._format_apa,
            CitationStyle.MLA: self._format_mla,
            CitationStyle.IEEE: self._format_ieee,
            CitationStyle.HARVARD: self._format_harvard,
            CitationStyle.CHICAGO: self._format_chicago,
            CitationStyle.VANCOUVER: self._format_vancouver,
        }

    def add_reference(self, source: Source) -> None:
        """Add a source to the reference library."""
        self.references[source.id] = source

    def format_citation(self, source: Source, style: CitationStyle,
                        citation_number: Optional[int] = None) -> str:
        """Format a single citation in the specified style."""
        formatter = self.style_formatters.get(style, self._format_apa)
        return formatter(source, citation_number)

    def generate_bibliography(self, source_ids: List[str],
                              style: CitationStyle) -> List[str]:
        """Generate a formatted bibliography."""
        citations: List[str] = []
        for i, source_id in enumerate(source_ids, 1):
            if source_id in self.references:
                citation = self.format_citation(
                    self.references[source_id], style, citation_number=i
                )
                citations.append(citation)
        return sorted(citations)

    def generate_in_text_citation(self, source: Source, style: CitationStyle,
                                  page: Optional[int] = None) -> str:
        """Generate an in-text citation."""
        if style == CitationStyle.APA:
            authors = source.authors
            year = source.publication_date.year if source.publication_date else "n.d."
            if len(authors) == 1:
                return f"({authors[0].split()[-1]}, {year})"
            elif len(authors) == 2:
                return f"({authors[0].split()[-1]} & {authors[1].split()[-1]}, {year})"
            elif len(authors) > 2:
                return f"({authors[0].split()[-1]} et al., {year})"
            return f"(Unknown, {year})"
        elif style == CitationStyle.IEEE:
            num = list(self.references.keys()).index(source.id) + 1
            return f"[{num}]"
        return f"({source.authors[0].split()[-1]}, {source.publication_date.year if source.publication_date else 'n.d.'})"

    def _format_apa(self, source: Source, num: Optional[int] = None) -> str:
        """Format citation in APA style."""
        authors = ", ".join(source.authors)
        year = source.publication_date.year if source.publication_date else "n.d."
        title = source.title
        journal = source.journal or ""
        doi = f" DOI: {source.doi}" if source.doi else ""
        url = f" {source.url}" if source.url and not source.doi else ""

        if journal:
            vol = f", {source.volume}" if source.volume else ""
            issue = f"({source.issue})" if source.issue else ""
            pages = f", {source.pages}" if source.pages else ""
            return f"{authors} ({year}). {title}. *{journal}*{vol}{issue}{pages}.{doi}"
        return f"{authors} ({year}). *{title}*.{url}{doi}"

    def _format_mla(self, source: Source, num: Optional[int] = None) -> str:
        """Format citation in MLA style."""
        authors = ", ".join(source.authors)
        title = f'"{source.title}"' if source.journal else f"*{source.title}*"
        journal = f"*{source.journal}*," if source.journal else ""
        year = source.publication_date.year if source.publication_date else ""
        pages = f" pp. {source.pages}" if source.pages else ""
        url = f" {source.url}" if source.url else ""

        return f"{authors}. {title} {journal} {year}{pages}.{url}"

    def _format_ieee(self, source: Source, num: Optional[int] = None) -> str:
        """Format citation in IEEE style."""
        authors = ", ".join(source.authors[:6])
        if len(source.authors) > 6:
            authors += ", et al."
        title = f'"{source.title},"'
        journal = f" *{source.journal}*," if source.journal else ""
        vol = f" vol. {source.volume}," if source.volume else ""
        pages = f" pp. {source.pages}," if source.pages else ""
        year = source.publication_date.year if source.publication_date else ""

        return f"{authors}, {title}{journal}{vol}{pages} {year}."

    def _format_harvard(self, source: Source, num: Optional[int] = None) -> str:
        """Format citation in Harvard style."""
        authors = " & ".join(source.authors)
        year = source.publication_date.year if source.publication_date else "n.d."
        title = source.title
        journal = source.journal or ""
        url = f" Available at: {source.url}" if source.url else ""

        if journal:
            return f"{authors} ({year}) '{title}', *{journal}*.{url}"
        return f"{authors} ({year}) *{title}*.{url}"

    def _format_chicago(self, source: Source, num: Optional[int] = None) -> str:
        """Format citation in Chicago style."""
        authors = ", ".join(source.authors)
        title = f'"{source.title}"' if source.journal else f"*{source.title}*"
        journal = f"*{source.journal}*" if source.journal else ""
        year = source.publication_date.year if source.publication_date else ""
        pages = f": {source.pages}" if source.pages else ""

        return f"{authors}. {title} {journal} {year}{pages}."

    def _format_vancouver(self, source: Source, num: Optional[int] = None) -> str:
        """Format citation in Vancouver style."""
        authors = ", ".join(source.authors[:3])
        if len(source.authors) > 3:
            authors += ", et al."
        title = source.title
        journal = source.journal or ""
        year = source.publication_date.year if source.publication_date else ""
        pages = f";{source.pages}" if source.pages else ""

        return f"{authors}. {title}. {journal}. {year}{pages}."


# =============================================================================
# Experiment Designer
# =============================================================================

class ExperimentDesigner:
    """Designs experiments with proper methodology."""

    def __init__(self) -> None:
        self.experiments: Dict[str, Experiment] = {}
        self.hypotheses: Dict[str, Hypothesis] = {}

    def create_hypothesis(self, statement: str,
                          variables: Optional[Dict[str, str]] = None,
                          test_method: Optional[StatisticalTest] = None) -> Hypothesis:
        """Create a research hypothesis."""
        hyp_id = f"hyp_{uuid.uuid4().hex[:8]}"
        hypothesis = Hypothesis(
            id=hyp_id,
            statement=statement,
            variables=variables or {},
            test_method=test_method,
        )
        self.hypotheses[hyp_id] = hypothesis
        return hypothesis

    def design_experiment(self, title: str, hypothesis_id: str,
                          methodology: MethodologyType,
                          sample_size: int = 100,
                          alpha: float = 0.05) -> Experiment:
        """Design an experiment."""
        exp_id = f"exp_{uuid.uuid4().hex[:8]}"

        experiment = Experiment(
            id=exp_id,
            title=title,
            hypothesis_id=hypothesis_id,
            methodology=methodology,
            sample_size=sample_size,
            alpha=alpha,
            power_analysis=self._calculate_power(sample_size, alpha),
        )

        self.experiments[exp_id] = experiment
        return experiment

    def calculate_sample_size(self, effect_size: float, alpha: float = 0.05,
                              power: float = 0.80) -> int:
        """Calculate required sample size for desired power."""
        # Simplified power analysis approximation
        z_alpha = 1.96 if alpha == 0.05 else 2.576
        z_beta = 0.842 if power == 0.80 else 1.282

        n = ((z_alpha + z_beta) ** 2 * 2) / (effect_size ** 2)
        return max(30, int(n) + 1)

    def check_assumptions(self, data: List[float],
                          test: StatisticalTest) -> Dict[str, Any]:
        """Check statistical test assumptions."""
        assumptions: Dict[str, Any] = {}

        if test in [StatisticalTest.T_TEST, StatisticalTest.ANOVA,
                     StatisticalTest.CORRELATION, StatisticalTest.REGRESSION]:
            # Normality check (simplified)
            mean = statistics.mean(data)
            stdev = statistics.stdev(data) if len(data) > 1 else 0
            cv = stdev / mean if mean != 0 else 0
            assumptions["normality"] = cv < 0.5  # Rough heuristic

            # Homogeneity of variance
            assumptions["equal_variances"] = True  # Placeholder

        assumptions["independence"] = True  # Assumed
        assumptions["sample_size_adequate"] = len(data) >= 30

        return assumptions

    def _calculate_power(self, sample_size: int, alpha: float) -> float:
        """Estimate statistical power."""
        # Simplified power estimation
        if sample_size >= 100:
            return 0.95
        elif sample_size >= 50:
            return 0.80
        elif sample_size >= 30:
            return 0.65
        return 0.50


# =============================================================================
# Statistical Analyzer
# =============================================================================

class StatisticalAnalyzer:
    """Performs statistical analysis on research data."""

    def __init__(self) -> None:
        self.results: Dict[str, AnalysisResult] = {}

    def analyze(self, data_group1: List[float], data_group2: List[float],
                test: StatisticalTest,
                alpha: float = 0.05) -> AnalysisResult:
        """Perform statistical analysis."""
        if test == StatisticalTest.T_TEST:
            return self._t_test(data_group1, data_group2, alpha)
        elif test == StatisticalTest.CORRELATION:
            return self._correlation(data_group1, data_group2, alpha)
        elif test == StatisticalTest.CHI_SQUARE:
            return self._chi_square(data_group1, data_group2, alpha)
        elif test == StatisticalTest.ANOVA:
            return self._anova([data_group1, data_group2], alpha)
        else:
            return AnalysisResult(
                test=test, statistic=0.0, p_value=1.0,
                interpretation="Test not implemented",
                significant=False,
            )

    def descriptive_statistics(self, data: List[float]) -> Dict[str, float]:
        """Calculate descriptive statistics."""
        if not data:
            return {}

        return {
            "n": len(data),
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "mode": statistics.mode(data) if len(set(data)) < len(data) else None,
            "stdev": statistics.stdev(data) if len(data) > 1 else 0,
            "variance": statistics.variance(data) if len(data) > 1 else 0,
            "min": min(data),
            "max": max(data),
            "range": max(data) - min(data),
            "q1": self._percentile(data, 25),
            "q3": self._percentile(data, 75),
            "iqr": self._percentile(data, 75) - self._percentile(data, 25),
            "skewness": self._skewness(data),
            "kurtosis": self._kurtosis(data),
        }

    def effect_size_cohens_d(self, group1: List[float],
                              group2: List[float]) -> float:
        """Calculate Cohen's d effect size."""
        if not group1 or not group2:
            return 0.0

        mean1 = statistics.mean(group1)
        mean2 = statistics.mean(group2)
        var1 = statistics.variance(group1) if len(group1) > 1 else 0
        var2 = statistics.variance(group2) if len(group2) > 1 else 0

        pooled_stdev = ((var1 + var2) / 2) ** 0.5
        if pooled_stdev == 0:
            return 0.0

        return (mean1 - mean2) / pooled_stdev

    def _t_test(self, group1: List[float], group2: List[float],
                alpha: float) -> AnalysisResult:
        """Perform independent samples t-test."""
        n1, n2 = len(group1), len(group2)
        mean1, mean2 = statistics.mean(group1), statistics.mean(group2)
        var1 = statistics.variance(group1) if n1 > 1 else 0
        var2 = statistics.variance(group2) if n2 > 1 else 0

        se = ((var1 / n1) + (var2 / n2)) ** 0.5
        t_stat = (mean1 - mean2) / se if se > 0 else 0.0

        df = n1 + n2 - 2
        p_value = self._t_test_p_value(abs(t_stat), df)
        significant = p_value < alpha

        effect = self.effect_size_cohens_d(group1, group2)

        return AnalysisResult(
            test=StatisticalTest.T_TEST,
            statistic=t_stat,
            p_value=p_value,
            effect_size=effect,
            significant=significant,
            interpretation=f"t({df}) = {t_stat:.3f}, p = {p_value:.4f}, d = {effect:.3f}",
        )

    def _correlation(self, x: List[float], y: List[float],
                     alpha: float) -> AnalysisResult:
        """Calculate Pearson correlation."""
        n = min(len(x), len(y))
        if n < 3:
            return AnalysisResult(
                test=StatisticalTest.CORRELATION,
                statistic=0.0, p_value=1.0,
                interpretation="Insufficient data",
                significant=False,
            )

        mean_x = statistics.mean(x[:n])
        mean_y = statistics.mean(y[:n])

        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = (sum((xi - mean_x) ** 2 for xi in x[:n]) / n) ** 0.5
        std_y = (sum((yi - mean_y) ** 2 for yi in y[:n]) / n) ** 0.5

        r = cov / (std_x * std_y) if (std_x * std_y) > 0 else 0.0
        t_stat = r * ((n - 2) / (1 - r ** 2)) ** 0.5 if abs(r) < 1 else 0.0
        p_value = self._t_test_p_value(abs(t_stat), n - 2)

        return AnalysisResult(
            test=StatisticalTest.CORRELATION,
            statistic=r,
            p_value=p_value,
            effect_size=r,
            significant=p_value < alpha,
            interpretation=f"r({n-2}) = {r:.3f}, p = {p_value:.4f}",
        )

    def _chi_square(self, observed: List[float], expected: List[float],
                    alpha: float) -> AnalysisResult:
        """Calculate chi-square test."""
        n = min(len(observed), len(expected))
        chi2 = sum(
            (observed[i] - expected[i]) ** 2 / max(expected[i], 0.001)
            for i in range(n)
        )
        df = n - 1
        p_value = max(0.001, 1.0 - chi2 / (df * 2))  # Rough approximation

        return AnalysisResult(
            test=StatisticalTest.CHI_SQUARE,
            statistic=chi2,
            p_value=p_value,
            significant=p_value < alpha,
            interpretation=f"Chi2({df}) = {chi2:.3f}, p = {p_value:.4f}",
        )

    def _anova(self, groups: List[List[float]], alpha: float) -> AnalysisResult:
        """Perform one-way ANOVA."""
        all_data = [x for group in groups for x in group]
        grand_mean = statistics.mean(all_data)

        between_var = sum(
            len(g) * (statistics.mean(g) - grand_mean) ** 2
            for g in groups if g
        ) / (len(groups) - 1)

        within_var = sum(
            sum((x - statistics.mean(g)) ** 2 for x in g)
            for g in groups if g
        ) / (len(all_data) - len(groups))

        f_stat = between_var / within_var if within_var > 0 else 0.0
        p_value = max(0.001, 1.0 - f_stat / 10)  # Rough approximation

        return AnalysisResult(
            test=StatisticalTest.ANOVA,
            statistic=f_stat,
            p_value=p_value,
            significant=p_value < alpha,
            interpretation=f"F({len(groups)-1}, {len(all_data)-len(groups)}) = {f_stat:.3f}, p = {p_value:.4f}",
        )

    def _t_test_p_value(self, t_stat: float, df: int) -> float:
        """Approximate p-value for t-test."""
        x = df / (df + t_stat ** 2)
        return max(0.0001, min(1.0, x))

    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile."""
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        lower = int(index)
        upper = lower + 1
        if upper >= len(sorted_data):
            return sorted_data[-1]
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight

    def _skewness(self, data: List[float]) -> float:
        """Calculate skewness."""
        n = len(data)
        if n < 3:
            return 0.0
        mean = statistics.mean(data)
        stdev = statistics.stdev(data)
        if stdev == 0:
            return 0.0
        return sum((x - mean) ** 3 for x in data) / (n * stdev ** 3)

    def _kurtosis(self, data: List[float]) -> float:
        """Calculate excess kurtosis."""
        n = len(data)
        if n < 4:
            return 0.0
        mean = statistics.mean(data)
        stdev = statistics.stdev(data)
        if stdev == 0:
            return 0.0
        return sum((x - mean) ** 4 for x in data) / (n * stdev ** 4) - 3.0


# =============================================================================
# Knowledge Graph
# =============================================================================

class KnowledgeGraph:
    """Constructs and queries a knowledge graph from research."""

    def __init__(self) -> None:
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []

    def add_node(self, label: str, node_type: str,
                 properties: Optional[Dict[str, Any]] = None) -> KnowledgeNode:
        """Add a node to the knowledge graph."""
        node_id = f"node_{uuid.uuid4().hex[:8]}"
        node = KnowledgeNode(
            id=node_id,
            label=label,
            node_type=node_type,
            properties=properties or {},
        )
        self.nodes[node_id] = node
        return node

    def add_edge(self, source_id: str, target_id: str,
                 relationship: str, weight: float = 1.0) -> KnowledgeEdge:
        """Add an edge between two nodes."""
        edge = KnowledgeEdge(
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
            weight=weight,
        )
        self.edges.append(edge)
        if source_id in self.nodes:
            self.nodes[source_id].connections.append(target_id)
        return edge

    def find_paths(self, start_id: str, end_id: str,
                   max_depth: int = 5) -> List[List[str]]:
        """Find paths between two nodes."""
        paths: List[List[str]] = []
        self._dfs(start_id, end_id, [start_id], paths, max_depth, set())
        return paths

    def get_connected(self, node_id: str) -> List[KnowledgeNode]:
        """Get all nodes connected to a given node."""
        connected_ids = set()
        for edge in self.edges:
            if edge.source_id == node_id:
                connected_ids.add(edge.target_id)
            elif edge.target_id == node_id:
                connected_ids.add(edge.source_id)
        return [self.nodes[nid] for nid in connected_ids if nid in self.nodes]

    def get_subgraph(self, node_id: str, depth: int = 2) -> Dict[str, Any]:
        """Get a subgraph around a node."""
        visited = set()
        nodes = []
        edges = []
        self._bfs_subgraph(node_id, depth, visited, nodes, edges)
        return {"nodes": nodes, "edges": edges}

    def _dfs(self, current: str, target: str, path: List[str],
             all_paths: List[List[str]], max_depth: int,
             visited: Set[str]) -> None:
        """Depth-first search for paths."""
        if len(path) > max_depth:
            return
        if current == target and len(path) > 1:
            all_paths.append(list(path))
            return
        visited.add(current)
        for edge in self.edges:
            next_node = None
            if edge.source_id == current and edge.target_id not in visited:
                next_node = edge.target_id
            elif edge.target_id == current and edge.source_id not in visited:
                next_node = edge.source_id
            if next_node:
                path.append(next_node)
                self._dfs(next_node, target, path, all_paths, max_depth, visited)
                path.pop()
        visited.discard(current)

    def _bfs_subgraph(self, start_id: str, depth: int,
                       visited: Set[str], nodes: List, edges: List) -> None:
        """BFS to collect subgraph."""
        if depth < 0 or start_id in visited:
            return
        visited.add(start_id)
        if start_id in self.nodes:
            nodes.append({
                "id": start_id,
                "label": self.nodes[start_id].label,
                "type": self.nodes[start_id].node_type,
            })
        for edge in self.edges:
            if edge.source_id == start_id:
                edges.append({
                    "source": edge.source_id,
                    "target": edge.target_id,
                    "relationship": edge.relationship,
                })
                self._bfs_subgraph(edge.target_id, depth - 1, visited, nodes, edges)
            elif edge.target_id == start_id:
                edges.append({
                    "source": edge.source_id,
                    "target": edge.target_id,
                    "relationship": edge.relationship,
                })
                self._bfs_subgraph(edge.source_id, depth - 1, visited, nodes, edges)


# =============================================================================
# Academic Writer
# =============================================================================

class AcademicWriter:
    """Generates academic writing in various formats."""

    def __init__(self, citation_manager: CitationManager) -> None:
        self.citation_manager = citation_manager

    def write_abstract(self, title: str, research_questions: List[ResearchQuestion],
                       findings_summary: str, conclusions: str,
                       word_limit: int = 300) -> str:
        """Write an abstract."""
        sections = [
            f"**Background:** This study addresses the research area of {title.lower()}.",
            "",
            f"**Objective:** {'; '.join(rq.question for rq in research_questions[:3])}",
            "",
            f"**Methods:** A systematic review was conducted following PRISMA guidelines.",
            "",
            f"**Results:** {findings_summary}",
            "",
            f"**Conclusions:** {conclusions}",
        ]
        abstract = "\n".join(sections)

        # Truncate to word limit
        words = abstract.split()
        if len(words) > word_limit:
            abstract = " ".join(words[:word_limit]) + "..."

        return abstract

    def write_literature_review(self, review: LiteratureReview,
                                format_type: WritingFormat = WritingFormat.MARKDOWN) -> str:
        """Write a literature review section."""
        sections = [
            f"# Literature Review: {review.topic}",
            "",
            "## Introduction",
            f"This review examines {len(review.sources)} sources related to {review.topic}.",
            "",
            "## Themes Identified",
        ]

        for theme, source_ids in review.themes.items():
            sections.append(f"\n### {theme.replace('_', ' ').title()}")
            sections.append(f"Found {len(source_ids)} sources discussing {theme}.")

        if review.gaps:
            sections.append("\n## Research Gaps")
            for gap in review.gaps:
                sections.append(f"- {gap}")

        if review.contradictions:
            sections.append("\n## Contradictions")
            for contradiction in review.contradictions:
                sections.append(
                    f"- Contradiction between {contradiction.get('source_1', 'unknown')} "
                    f"and {contradiction.get('source_2', 'unknown')}"
                )

        if review.recommendations:
            sections.append("\n## Recommendations")
            for rec in review.recommendations:
                sections.append(f"- {rec}")

        return "\n".join(sections)

    def write_methodology(self, methodology: MethodologyType,
                          sample_size: int, variables: Dict[str, str],
                          procedures: List[str]) -> str:
        """Write a methodology section."""
        sections = [
            f"## Methodology",
            f"\n### Research Design",
            f"This study employs a {methodology.value} approach.",
            f"\n### Participants/Sample",
            f"The sample consisted of {sample_size} participants.",
            f"\n### Variables",
        ]

        for var_name, var_desc in variables.items():
            sections.append(f"- **{var_name}:** {var_desc}")

        sections.append("\n### Procedure")
        for i, procedure in enumerate(procedures, 1):
            sections.append(f"{i}. {procedure}")

        return "\n".join(sections)

    def write_results(self, descriptive_stats: Dict[str, Dict[str, float]],
                      analysis_results: List[AnalysisResult],
                      tables: Optional[List[Dict[str, Any]]] = None) -> str:
        """Write a results section."""
        sections = ["## Results", "\n### Descriptive Statistics"]

        for variable, stats in descriptive_stats.items():
            sections.append(f"\n**{variable}:**")
            sections.append(f"- Mean = {stats.get('mean', 'N/A'):.2f}")
            sections.append(f"- SD = {stats.get('stdev', 'N/A'):.2f}")
            sections.append(f"- Range = [{stats.get('min', 'N/A'):.2f}, {stats.get('max', 'N/A'):.2f}]")

        if analysis_results:
            sections.append("\n### Statistical Tests")
            for result in analysis_results:
                sig = "significant" if result.significant else "not significant"
                sections.append(f"\n**{result.test.value}:** {result.interpretation} ({sig})")

        return "\n".join(sections)

    def write_discussion(self, findings_summary: str, limitations: List[str],
                         implications: List[str],
                         future_research: List[str]) -> str:
        """Write a discussion section."""
        sections = [
            "## Discussion",
            f"\n### Summary of Findings",
            findings_summary,
            "\n### Limitations",
        ]
        for lim in limitations:
            sections.append(f"- {lim}")

        sections.append("\n### Implications")
        for imp in implications:
            sections.append(f"- {imp}")

        sections.append("\n### Future Research")
        for fr in future_research:
            sections.append(f"- {fr}")

        return "\n".join(sections)


# =============================================================================
# Research Agent (Main Orchestrator)
# =============================================================================

class ResearchAgent:
    """Main research agent orchestrating all components."""

    def __init__(self) -> None:
        self.indexer = ResearchIndexer()
        self.analyzer = LiteratureAnalyzer()
        self.synthesizer = ResearchSynthesizer()
        self.citation_manager = CitationManager()
        self.experiment_designer = ExperimentDesigner()
        self.stat_analyzer = StatisticalAnalyzer()
        self.knowledge_graph = KnowledgeGraph()
        self.academic_writer = AcademicWriter(self.citation_manager)
        self.research_questions: List[ResearchQuestion] = []
        self.papers: List[ResearchPaper] = []
        self.reviews: List[LiteratureReview] = []

    def add_research_question(self, question: str, priority: int = 1,
                              sub_questions: Optional[List[str]] = None,
                              keywords: Optional[List[str]] = None) -> ResearchQuestion:
        """Add a research question."""
        rq = ResearchQuestion(
            id=f"rq_{len(self.research_questions)}",
            question=question,
            sub_questions=sub_questions or [],
            priority=priority,
            keywords=keywords or [],
        )
        self.research_questions.append(rq)
        return rq

    def conduct_research(self, query: str,
                         source_types: Optional[List[SourceType]] = None,
                         max_sources: int = 20) -> Dict[str, Any]:
        """Conduct comprehensive research on a query."""
        all_findings: List[ResearchFinding] = []

        types_to_search = source_types or list(SourceType)
        for source_type in types_to_search:
            sources = self.indexer.search(query, source_type=source_type, limit=max_sources)
            for source in sources:
                self.citation_manager.add_reference(source)
                finding = ResearchFinding(
                    source_id=source.id,
                    finding=source.abstract,
                    evidence_strength=EvidenceStrength.MODERATE,
                )
                all_findings.append(finding)
                self.synthesizer.add_finding(finding)

        analysis = self.analyzer.analyze(list(self.indexer.sources.values()))
        synthesis = self.synthesizer.synthesize(self.research_questions)

        return {
            "sources_found": len(self.indexer.sources),
            "findings_count": len(all_findings),
            "analysis": analysis,
            "synthesis": synthesis,
            "contradictions": self.synthesizer.identify_contradictions(),
        }

    def literature_review(self, topic: str) -> Dict[str, Any]:
        """Perform a literature review on a topic."""
        results = self.conduct_research(topic, max_sources=50)
        gaps = self.analyzer.identify_gaps(
            list(self.indexer.sources.values()),
            self.research_questions,
        )
        recommendations = self._generate_recommendations(results, gaps)

        review = LiteratureReview(
            id=f"rev_{uuid.uuid4().hex[:8]}",
            topic=topic,
            research_questions=self.research_questions,
            sources=list(self.indexer.sources.values()),
            findings=self.synthesizer.findings,
            themes=results["analysis"]["themes"],
            gaps=gaps,
            contradictions=results["contradictions"],
            recommendations=recommendations,
        )
        self.reviews.append(review)

        return {
            "topic": topic,
            "executive_summary": self.synthesizer.generate_narrative(),
            "key_themes": list(results["analysis"]["themes"].keys()),
            "publication_trend": results["analysis"]["publication_timeline"],
            "critical_analysis": {
                "contradictions": results["contradictions"],
                "gaps": gaps,
            },
            "recommendations": recommendations,
        }

    def generate_report(self, title: str,
                        style: CitationStyle = CitationStyle.APA) -> Dict[str, Any]:
        """Generate a comprehensive research report."""
        bibliography = self.citation_manager.generate_bibliography(
            list(self.citation_manager.references.keys()), style
        )

        return {
            "title": title,
            "date": datetime.now().isoformat(),
            "research_questions": [rq.question for rq in self.research_questions],
            "findings": self.synthesizer.synthesize(self.research_questions),
            "bibliography": bibliography,
            "total_sources": len(self.citation_manager.references),
            "narrative": self.synthesizer.generate_narrative(),
        }

    def write_paper(self, title: str, authors: List[str],
                    style: CitationStyle = CitationStyle.APA) -> ResearchPaper:
        """Write a complete research paper."""
        abstract = self.academic_writer.write_abstract(
            title, self.research_questions,
            self.synthesizer.generate_narrative()[:200],
            "This research contributes to the understanding of the field.",
        )

        paper = ResearchPaper(
            id=f"paper_{uuid.uuid4().hex[:8]}",
            title=title,
            authors=authors,
            abstract=abstract,
            references=list(self.indexer.sources.values()),
            citations_style=style,
        )
        self.papers.append(paper)
        return paper

    def analyze_data(self, data_group1: List[float], data_group2: List[float],
                     test: StatisticalTest = StatisticalTest.T_TEST) -> AnalysisResult:
        """Analyze data with statistical tests."""
        return self.stat_analyzer.analyze(data_group1, data_group2, test)

    def add_to_knowledge_graph(self, concept: str, node_type: str,
                                connections: Optional[List[Tuple[str, str]]] = None) -> KnowledgeNode:
        """Add a concept to the knowledge graph."""
        node = self.knowledge_graph.add_node(concept, node_type)
        if connections:
            for target_label, relationship in connections:
                target_nodes = [
                    n for n in self.knowledge_graph.nodes.values()
                    if n.label == target_label
                ]
                for target in target_nodes:
                    self.knowledge_graph.add_edge(node.id, target.id, relationship)
        return node

    def _generate_recommendations(self, results: Dict[str, Any],
                                   gaps: List[str]) -> List[str]:
        """Generate research recommendations."""
        recommendations: List[str] = []

        if results["contradictions"]:
            recommendations.append("Resolve contradictory findings through additional research")

        for gap in gaps:
            recommendations.append(f"Address gap: {gap}")

        recommendations.extend([
            "Conduct longitudinal studies for temporal validation",
            "Expand sample diversity in future research",
            "Consider mixed-methods approaches for triangulation",
            "Replicate key findings across different populations",
        ])

        return recommendations


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> None:
    """Demonstrate the Research Agent."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    agent = ResearchAgent()

    # Add research questions
    agent.add_research_question(
        "What are the main challenges in AI alignment?",
        priority=1,
        sub_questions=[
            "What methods exist for alignment?",
            "What are the limitations of current approaches?",
            "What future directions show promise?",
        ],
        keywords=["AI alignment", "safety", "ethics", "machine learning"],
    )

    agent.add_research_question(
        "How effective are current red team methodologies?",
        priority=2,
        sub_questions=[
            "What metrics measure red team effectiveness?",
            "How do adversary emulation techniques compare?",
        ],
        keywords=["red team", "penetration testing", "adversary emulation"],
    )

    # Conduct literature review
    review_results = agent.literature_review("AI alignment research")
    print(f"Review completed: {len(review_results.get('key_themes', []))} themes identified")

    # Generate report
    report = agent.generate_report("AI Alignment Research Review")
    print(f"Report generated with {report['total_sources']} sources")

    # Write paper
    paper = agent.write_paper(
        "A Comprehensive Review of AI Alignment Challenges",
        ["Research Agent"],
    )
    print(f"Paper written: {paper.title} (ID: {paper.id})")

    # Statistical analysis
    group1 = [23.5, 25.1, 22.8, 24.3, 26.0, 23.9, 25.5, 24.8, 22.1, 25.7]
    group2 = [21.2, 20.8, 22.5, 19.9, 21.7, 20.3, 22.0, 21.1, 20.5, 21.8]

    result = agent.analyze_data(group1, group2, StatisticalTest.T_TEST)
    print(f"Statistical analysis: {result.interpretation}")

    # Knowledge graph
    ai_node = agent.add_to_knowledge_graph("AI Alignment", "concept")
    safety_node = agent.add_to_knowledge_graph("AI Safety", "concept")
    agent.add_to_knowledge_graph("Machine Learning", "concept", [("AI Alignment", "part_of")])

    print(f"\nKnowledge graph: {len(agent.knowledge_graph.nodes)} nodes, "
          f"{len(agent.knowledge_graph.edges)} edges")
    print("\nDone!")


if __name__ == "__main__":
    main()
