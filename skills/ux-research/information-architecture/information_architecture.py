"""
Information Architecture Toolkit
================================
Content taxonomy design, navigation structure optimization, site map
generation, labeling systems, mental model alignment, findability metrics,
search analytics, and hierarchical/faceted classification.
"""

from __future__ import annotations

import uuid
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import Counter, defaultdict
from datetime import datetime


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class NavType(Enum):
    GLOBAL = "global"
    LOCAL = "local"
    CONTEXTUAL = "contextual"
    SUPPLEMENTAL = "supplemental"


class ContentType(Enum):
    LANDING = "landing"
    CATEGORY = "category"
    PRODUCT = "product"
    ARTICLE = "article"
    INFORMATIONAL = "informational"
    FORM = "form"
    UTILITY = "utility"
    MEDIA = "media"
    TOOL = "tool"


class RelationshipType(Enum):
    BROADER = "broader"
    NARROWER = "narrower"
    RELATED = "related"
    SYNONYM = "synonym"
    USE_FOR = "use_for"


class SortMode(Enum):
    OPEN = "open"
    CLOSED = "closed"
    HYBRID = "hybrid"


class LabelQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    FAILED = "failed"


class ClassificationSystem(Enum):
    MONOHIERARCHICAL = "monohierarchical"
    POLYHIERARCHICAL = "polyhierarchical"
    FACETED = "faceted"
    FLAT = "flat"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Term:
    id: str
    label: str
    parent_id: str | None = None
    level: int = 0
    variant_of: str | None = None
    description: str = ""
    synonyms: list[str] = field(default_factory=list)
    scope_note: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TermRelationship:
    source_id: str
    target_id: str
    relationship: RelationshipType


@dataclass
class NavItem:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    label: str = ""
    nav_type: NavType = NavType.GLOBAL
    parent_id: str | None = None
    url: str = ""
    priority: int = 0
    children: list[str] = field(default_factory=list)  # child IDs


@dataclass
class NavigationMetrics:
    max_depth: int
    breadth_at_levels: list[int]
    total_items: int
    global_count: int
    local_count: int
    recommendation: str


@dataclass
class PageNode:
    url: str
    title: str
    content_type: ContentType = ContentType.INFORMATIONAL
    parent_url: str | None = None
    word_count: int = 0
    last_updated: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TreeTestTask:
    description: str
    target_url: str
    participant_id: str = ""
    first_click_url: str = ""
    success: bool = False
    clicks: int = 0
    time_seconds: float = 0.0
    direct_hits: int = 0


@dataclass
class SearchEvent:
    query: str
    results_count: int = 0
    clicked_rank: int = 0
    success: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)
    session_id: str = ""


@dataclass
class CardSortResponse:
    participant_id: str
    groupings: dict[str, list[str]] = field(default_factory=dict)
    labels: dict[str, str] = field(default_factory=dict)
    time_seconds: float = 0.0


@dataclass
class LabelEvaluation:
    label: str
    comprehension_rate: float  # % who understood correctly
    consistency_score: float   # agreement across evaluators
    quality: LabelQuality
    suggestions: list[str] = field(default_factory=list)


@dataclass
class FindabilityReport:
    task_completion_rate: float
    mean_clicks: float
    median_clicks: float
    mean_time_seconds: float
    search_success_rate: float
    zero_result_rate: float
    first_click_accuracy: float
    recommendations: list[str]


@dataclass
class IAComparison:
    system_a_score: float
    system_b_score: str
    metric_name: str
    difference: float
    significant: bool


@dataclass
class FacetDefinition:
    name: str
    values: list[str] = field(default_factory=list)
    is_required: bool = False
    allows_multiple: bool = False
    priority: int = 0


@dataclass
class FacetedResult:
    facet_name: str
    selected_values: list[str]
    matching_count: int
    total_count: int
    facets_used: dict[str, list[str]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Taxonomy Builder
# ---------------------------------------------------------------------------

class Taxonomy:
    def __init__(self, name: str = "Untitled Taxonomy"):
        self.name = name
        self._terms: dict[str, Term] = {}
        self._relationships: list[TermRelationship] = []
        self._created_at = datetime.utcnow()

    def add_term(self, term: Term) -> None:
        if term.id in self._terms:
            raise ValueError(f"Term '{term.id}' already exists")
        if term.parent_id and term.parent_id not in self._terms:
            raise ValueError(f"Parent term '{term.parent_id}' not found")
        self._terms[term.id] = term
        if term.variant_of and term.variant_of in self._terms:
            self._relationships.append(TermRelationship(
                source_id=term.id, target_id=term.variant_of,
                relationship=RelationshipType.SYNONYM,
            ))

    def get_term(self, term_id: str) -> Term:
        if term_id not in self._terms:
            raise KeyError(f"Term '{term_id}' not found")
        return self._terms[term_id]

    def children(self, parent_id: str) -> list[Term]:
        return [t for t in self._terms.values() if t.parent_id == parent_id]

    def siblings(self, term_id: str) -> list[Term]:
        term = self.get_term(term_id)
        if term.parent_id is None:
            return [t for t in self._terms.values()
                    if t.parent_id is None and t.id != term_id]
        return [t for t in self._terms.values()
                if t.parent_id == term.parent_id and t.id != term_id]

    def path_to_root(self, term_id: str) -> list[Term]:
        path = []
        current = self.get_term(term_id)
        while current.parent_id is not None:
            path.append(current)
            current = self.get_term(current.parent_id)
        path.append(current)
        return list(reversed(path))

    def depth(self) -> int:
        if not self._terms:
            return 0
        return max(t.level for t in self._terms.values())

    def breadth_by_level(self) -> dict[int, int]:
        counts: Counter = Counter(t.level for t in self._terms.values())
        return dict(sorted(counts.items()))

    def validate(self) -> list[str]:
        issues = []
        # Check for orphaned terms
        for term in self._terms.values():
            if term.parent_id and term.parent_id not in self._terms:
                issues.append(f"Orphaned term '{term.id}': parent '{term.parent_id}' not found")
        # Check for cycles
        for term in self._terms.values():
            path = self.path_to_root(term.id)
            ids = [t.id for t in path]
            if len(ids) != len(set(ids)):
                issues.append(f"Cycle detected involving term '{term.id}'")
        # Check breadth at each level
        for level, count in self.breadth_by_level().items():
            if count > 12:
                issues.append(f"Level {level} has {count} items (>12 may overwhelm users)")
        return issues

    def render_hierarchy(self) -> str:
        lines = [f"# {self.name}"]
        top_terms = [t for t in self._terms.values() if t.parent_id is None]
        for term in sorted(top_terms, key=lambda t: t.label):
            lines.append(f"  {term.label}")
            self._render_children(term.id, lines, indent=4)
        return "\n".join(lines)

    def _render_children(self, parent_id: str, lines: list[str], indent: int) -> None:
        children = self.children(parent_id)
        for child in sorted(children, key=lambda t: t.label):
            prefix = " " * indent + ("├── " if child != children[-1] else "└── ")
            variant_note = f" [{child.variant_of}]" if child.variant_of else ""
            lines.append(f"{prefix}{child.label}{variant_note}")
            self._render_children(child.id, lines, indent + 4)


# ---------------------------------------------------------------------------
# Navigation Structure
# ---------------------------------------------------------------------------

class NavigationStructure:
    def __init__(self, name: str = "Navigation"):
        self.name = name
        self._items: dict[str, NavItem] = {}

    def add_item(
        self, label: str, nav_type: NavType = NavType.GLOBAL,
        parent: str | None = None, priority: int = 0, url: str = "",
    ) -> NavItem:
        item = NavItem(
            label=label, nav_type=nav_type, priority=priority, url=url,
            parent_id=parent,
        )
        if parent and parent in self._items:
            self._items[parent].children.append(item.id)
        self._items[item.id] = item
        return item

    def get_item(self, item_id: str) -> NavItem:
        if item_id not in self._items:
            raise KeyError(f"Nav item '{item_id}' not found")
        return self._items[item_id]

    def _compute_depth(self, item_id: str) -> int:
        item = self._items.get(item_id)
        if not item or not item.children:
            return 0
        return 1 + max(self._compute_depth(c) for c in item.children)

    def evaluate(self) -> NavigationMetrics:
        roots = [i for i in self._items.values() if i.parent_id is None]
        max_depth = max((self._compute_depth(r.id) for r in roots), default=0)
        breadth: list[int] = []
        queue = list(roots)
        while queue:
            breadth.append(len(queue))
            next_queue = []
            for item in queue:
                next_queue.extend(
                    self._items[cid] for cid in item.children if cid in self._items
                )
            queue = next_queue

        global_count = sum(1 for i in self._items.values() if i.nav_type == NavType.GLOBAL)
        local_count = sum(1 for i in self._items.values() if i.nav_type == NavType.LOCAL)

        rec = "OK"
        if max_depth > 4:
            rec = "Consider flattening: depth >4 may confuse users"
        if breadth and breadth[0] > 8:
            rec = "Consider grouping: level 1 has >8 items"
        if global_count > 7:
            rec = "Too many global nav items (recommended: ≤7)"

        return NavigationMetrics(
            max_depth=max_depth,
            breadth_at_levels=breadth,
            total_items=len(self._items),
            global_count=global_count,
            local_count=local_count,
            recommendation=rec,
        )

    def render(self) -> str:
        roots = sorted(
            [i for i in self._items.values() if i.parent_id is None],
            key=lambda i: i.priority,
        )
        lines = [f"# {self.name}"]
        for root in roots:
            lines.append(f"  [{root.nav_type.value}] {root.label}")
            self._render_nav_children(root.id, lines, indent=4)
        return "\n".join(lines)

    def _render_nav_children(self, parent_id: str, lines: list[str], indent: int) -> None:
        item = self._items.get(parent_id)
        if not item:
            return
        for cid in item.children:
            child = self._items.get(cid)
            if child:
                lines.append(f"{' ' * indent}├── [{child.nav_type.value}] {child.label}")
                self._render_nav_children(cid, lines, indent + 4)


# ---------------------------------------------------------------------------
# Site Map
# ---------------------------------------------------------------------------

class SiteMap:
    def __init__(self, domain: str = ""):
        self.domain = domain
        self._pages: dict[str, PageNode] = {}

    def add_page(self, page: PageNode) -> None:
        self._pages[page.url] = page

    def get_page(self, url: str) -> PageNode:
        if url not in self._pages:
            raise KeyError(f"Page '{url}' not found")
        return self._pages[url]

    def children(self, parent_url: str) -> list[PageNode]:
        return [p for p in self._pages.values() if p.parent_url == parent_url]

    @property
    def page_count(self) -> int:
        return len(self._pages)

    @property
    def max_depth(self) -> int:
        def depth(url: str) -> int:
            page = self._pages.get(url)
            if not page or page.parent_url is None:
                return 0
            return 1 + depth(page.parent_url)
        if not self._pages:
            return 0
        return max(depth(url) for url in self._pages)

    def content_distribution(self) -> dict[str, int]:
        return dict(Counter(p.content_type.value for p in self._pages.values()))

    def orphan_pages(self) -> list[PageNode]:
        return [p for p in self._pages.values()
                if p.parent_url and p.parent_url not in self._pages]

    def render_tree(self) -> str:
        roots = [p for p in self._pages.values() if p.parent_url is None]
        lines = [f"# Site Map: {self.domain}"]
        for root in sorted(roots, key=lambda p: p.title):
            lines.append(f"  /{root.url.strip('/')} [{root.content_type.value}] — {root.title}")
            self._render_page_children(root.url, lines, indent=4)
        return "\n".join(lines)

    def _render_page_children(self, parent_url: str, lines: list[str], indent: int) -> None:
        children = self.children(parent_url)
        for child in sorted(children, key=lambda p: p.title):
            prefix = " " * indent + "├── "
            lines.append(f"{prefix}/{child.url.strip('/')} [{child.content_type.value}] — {child.title}")
            self._render_page_children(child.url, lines, indent + 4)


# ---------------------------------------------------------------------------
# Labeling System
# ---------------------------------------------------------------------------

class LabelingSystem:
    def __init__(self, name: str = "Labeling System"):
        self.name = name
        self._labels: dict[str, list[str]] = defaultdict(list)  # label -> [user interpretations]
        self._evaluations: list[LabelEvaluation] = []

    def add_label(self, label: str, user_interpretations: list[str]) -> None:
        self._labels[label] = user_interpretations

    def evaluate_label(
        self, label: str, expected_meaning: str, evaluators: list[str]
    ) -> LabelEvaluation:
        interpretations = self._labels.get(label, [])
        correct = sum(1 for i in interpretations if expected_meaning.lower() in i.lower())
        comprehension = correct / max(len(interpretations), 1)

        unique_interpretations = len(set(interpretations))
        consistency = 1.0 - (unique_interpretations - 1) / max(len(interpretations) - 1, 1)
        consistency = max(0, consistency)

        if comprehension >= 0.9 and consistency >= 0.8:
            quality = LabelQuality.EXCELLENT
        elif comprehension >= 0.75 and consistency >= 0.6:
            quality = LabelQuality.GOOD
        elif comprehension >= 0.5:
            quality = LabelQuality.ACCEPTABLE
        elif comprehension >= 0.3:
            quality = LabelQuality.POOR
        else:
            quality = LabelQuality.FAILED

        suggestions = []
        if comprehension < 0.7:
            suggestions.append("Consider a more descriptive or common term")
        if consistency < 0.5:
            suggestions.append("Users interpret this label inconsistently; consider splitting")
        if len(label) > 20:
            suggestions.append("Label may be too long for navigation context")

        evaluation = LabelEvaluation(
            label=label,
            comprehension_rate=round(comprehension, 3),
            consistency_score=round(consistency, 3),
            quality=quality,
            suggestions=suggestions,
        )
        self._evaluations.append(evaluation)
        return evaluation

    def label_quality_report(self) -> str:
        lines = [f"# {self.name} — Label Quality Report"]
        for ev in sorted(self._evaluations, key=lambda e: e.comprehension_rate):
            lines.append(f"\n## {ev.label} [{ev.quality.value.upper()}]")
            lines.append(f"  Comprehension: {ev.comprehension_rate:.0%}")
            lines.append(f"  Consistency: {ev.consistency_score:.2f}")
            for s in ev.suggestions:
                lines.append(f"  → {s}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Findability Analyzer
# ---------------------------------------------------------------------------

class FindabilityAnalyzer:
    def __init__(self) -> None:
        self._tasks: list[TreeTestTask] = []
        self._searches: list[SearchEvent] = []

    def record_task(self, task: TreeTestTask) -> None:
        self._tasks.append(task)

    def record_search(self, query: str, results_count: int = 0,
                      clicked_rank: int = 0, success: bool = False) -> None:
        self._searches.append(SearchEvent(
            query=query, results_count=results_count,
            clicked_rank=clicked_rank, success=success,
        ))

    def generate_report(self) -> FindabilityReport:
        # Task metrics
        task_success = sum(1 for t in self._tasks if t.success)
        task_rate = task_success / max(len(self._tasks), 1)
        clicks = [t.clicks for t in self._tasks]
        times = [t.time_seconds for t in self._tasks]
        mean_clicks = sum(clicks) / max(len(clicks), 1)
        sorted_clicks = sorted(clicks)
        median_clicks = sorted_clicks[len(sorted_clicks) // 2] if sorted_clicks else 0
        mean_time = sum(times) / max(len(times), 1)

        # Search metrics
        search_success = sum(1 for s in self._searches if s.success)
        search_rate = search_success / max(len(self._searches), 1)
        zero_results = sum(1 for s in self._searches if s.results_count == 0)
        zero_rate = zero_results / max(len(self._searches), 1)

        # First click accuracy
        first_click_correct = sum(
            1 for t in self._tasks
            if t.first_click_url and t.target_url.startswith(t.first_click_url)
        )
        fc_accuracy = first_click_correct / max(len(self._tasks), 1)

        # Recommendations
        recs = []
        if task_rate < 0.7:
            recs.append("Task completion rate below 70% — navigation structure needs revision")
        if mean_clicks > 4:
            recs.append("Average clicks to target >4 — consider adding shortcuts or breadcrumbs")
        if zero_rate > 0.1:
            recs.append("High zero-result search rate — improve synonym coverage or search relevance")
        if fc_accuracy < 0.5:
            recs.append("First-click accuracy <50% — category labels may be misleading")

        return FindabilityReport(
            task_completion_rate=round(task_rate, 3),
            mean_clicks=round(mean_clicks, 1),
            median_clicks=median_clicks,
            mean_time_seconds=round(mean_time, 1),
            search_success_rate=round(search_rate, 3),
            zero_result_rate=round(zero_rate, 3),
            first_click_accuracy=round(fc_accuracy, 3),
            recommendations=recs,
        )


# ---------------------------------------------------------------------------
# Card Sort Analyzer
# ---------------------------------------------------------------------------

class CardSortAnalyzer:
    def __init__(self, mode: SortMode = SortMode.OPEN):
        self.mode = mode
        self._responses: list[CardSortResponse] = []

    def add_response(self, response: CardSortResponse) -> None:
        self._responses.append(response)

    def agreement_matrix(self) -> dict[tuple[str, str], float]:
        pair_counts: Counter[tuple[str, str]] = Counter()
        for resp in self._responses:
            for _group_name, cards in resp.groupings.items():
                for i, a in enumerate(cards):
                    for b in cards[i + 1:]:
                        pair = tuple(sorted([a, b]))
                        pair_counts[pair] += 1
        total = len(self._responses)
        return {p: round(c / max(total, 1), 3) for p, c in pair_counts.items()}

    def recommended_groups(self, threshold: float = 0.5) -> list[list[str]]:
        matrix = self.agreement_matrix()
        # Build adjacency from high-agreement pairs
        adj: dict[str, set[str]] = defaultdict(set)
        for (a, b), agreement in matrix.items():
            if agreement >= threshold:
                adj[a].add(b)
                adj[b].add(a)
        # Simple connected components
        visited: set[str] = set()
        groups: list[list[str]] = []
        for node in adj:
            if node in visited:
                continue
            component = []
            stack = [node]
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                component.append(current)
                stack.extend(adj[current] - visited)
            if component:
                groups.append(sorted(component))
        return groups

    def label_analysis(self) -> dict[str, int]:
        label_counts: Counter = Counter()
        for resp in self._responses:
            label_counts.update(resp.labels.values())
        return dict(label_counts.most_common())

    def consensus_score(self) -> float:
        matrix = self.agreement_matrix()
        if not matrix:
            return 0.0
        return round(sum(matrix.values()) / len(matrix), 3)


# ---------------------------------------------------------------------------
# Faceted Classification
# ---------------------------------------------------------------------------

class FacetedClassification:
    def __init__(self, name: str = "Faceted System"):
        self.name = name
        self._facets: dict[str, FacetDefinition] = {}
        self._items: list[dict[str, Any]] = []

    def add_facet(self, facet: FacetDefinition) -> None:
        self._facets[facet.name] = facet

    def add_item(self, item: dict[str, Any]) -> None:
        self._items.append(item)

    def filter(self, **facet_filters: list[str]) -> list[dict[str, Any]]:
        results = self._items
        for facet_name, values in facet_filters.items():
            results = [
                item for item in results
                if item.get(facet_name) in values
            ]
        return results

    def facet_counts(self, current_filters: dict[str, list[str]] | None = None) -> dict[str, dict[str, int]]:
        filtered = self.filter(**(current_filters or {}))
        counts: dict[str, dict[str, int]] = {}
        for facet_name, facet_def in self._facets.items():
            facet_counts: Counter = Counter()
            for item in filtered:
                val = item.get(facet_name)
                if val:
                    facet_counts[val] += 1
            counts[facet_name] = dict(facet_counts.most_common())
        return counts

    def validate_items(self) -> list[str]:
        issues = []
        for i, item in enumerate(self._items):
            for facet_name, facet_def in self._facets.items():
                if facet_def.is_required and facet_name not in item:
                    issues.append(f"Item {i} missing required facet '{facet_name}'")
                if facet_name in item and not facet_def.allows_multiple:
                    if isinstance(item[facet_name], list):
                        issues.append(f"Item {facet_name} has multiple values but facet is single-select")
        return issues


# ---------------------------------------------------------------------------
# IA Benchmarking
# ---------------------------------------------------------------------------

class IABenchmark:
    INDUSTRY_BENCHMARKS = {
        "task_completion_rate": {"target": 0.78, "excellent": 0.90},
        "first_click_accuracy": {"target": 0.65, "excellent": 0.80},
        "search_success_rate": {"target": 0.60, "excellent": 0.75},
        "zero_result_rate": {"target": 0.05, "excellent": 0.02},
        "mean_clicks_to_target": {"target": 3.5, "excellent": 2.5},
    }

    @classmethod
    def evaluate(cls, metric_name: str, value: float) -> str:
        bench = cls.INDUSTRY_BENCHMARKS.get(metric_name)
        if not bench:
            return "Unknown metric"
        target = bench["target"]
        excellent = bench["excellent"]

        if metric_name == "zero_result_rate":
            if value <= excellent:
                return "Excellent"
            if value <= target:
                return "On Target"
            return "Below Target"
        else:
            if value >= excellent:
                return "Excellent"
            if value >= target:
                return "On Target"
            return "Below Target"

    @classmethod
    def compare_systems(cls, metric_name: str, value_a: float, value_b: float) -> IAComparison:
        bench = cls.INDUSTRY_BENCHMARKS.get(metric_name, {})
        diff = value_a - value_b
        # Simple heuristic: if difference > 10% of target, consider significant
        target = bench.get("target", 1.0)
        significant = abs(diff) > target * 0.1
        winner = "A" if diff > 0 else "B"
        return IAComparison(
            system_a_score=value_a,
            system_b_score=f"{value_b} ({winner} wins)",
            metric_name=metric_name,
            difference=round(diff, 4),
            significant=significant,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  INFORMATION ARCHITECTURE TOOLKIT — DEMONSTRATION")
    print("=" * 60)

    # 1. Taxonomy
    print("\n--- Taxonomy Builder ---")
    tax = Taxonomy(name="SaaS Product Taxonomy")
    tax.add_term(Term(id="platform", label="Platform", level=0))
    tax.add_term(Term(id="analytics", label="Analytics", parent_id="platform", level=1))
    tax.add_term(Term(id="reports", label="Reports & Dashboards", parent_id="analytics", level=2))
    tax.add_term(Term(id="realtime", label="Real-Time Monitoring", parent_id="analytics", level=2))
    tax.add_term(Term(id="automation", label="Automation", parent_id="platform", level=1))
    tax.add_term(Term(id="integrations", label="Integrations", parent_id="platform", level=1))
    tax.add_term(Term(id="help", label="Help Center", level=0))
    tax.add_term(Term(id="docs", label="Documentation", parent_id="help", level=1))
    tax.add_term(Term(id="tutorials", label="Tutorials", parent_id="help", level=1))
    issues = tax.validate()
    for issue in issues:
        print(f"  ⚠ {issue}")
    print(tax.render_hierarchy())
    print(f"  Depth: {tax.depth()}, Breadth: {tax.breadth_by_level()}")

    # 2. Navigation Structure
    print("\n--- Navigation Structure ---")
    nav = NavigationStructure(name="Main Navigation")
    nav.add_item("Products", nav_type=NavType.GLOBAL, priority=1)
    nav.add_item("Platform", nav_type=NavType.LOCAL, parent="Products", priority=1)
    nav.add_item("Analytics", nav_type=NavType.LOCAL, parent="Products", priority=2)
    nav.add_item("Automation", nav_type=NavType.LOCAL, parent="Products", priority=3)
    nav.add_item("Solutions", nav_type=NavType.GLOBAL, priority=2)
    nav.add_item("Enterprise", nav_type=NavType.LOCAL, parent="Solutions", priority=1)
    nav.add_item("Startups", nav_type=NavType.LOCAL, parent="Solutions", priority=2)
    nav.add_item("Pricing", nav_type=NavType.GLOBAL, priority=3)
    nav.add_item("Resources", nav_type=NavType.GLOBAL, priority=4)
    nav.add_item("Blog", nav_type=NavType.LOCAL, parent="Resources", priority=1)
    nav.add_item("Webinars", nav_type=NavType.LOCAL, parent="Resources", priority=2)
    nav.add_item("Contact", nav_type=NavType.GLOBAL, priority=5)
    metrics = nav.evaluate()
    print(f"  Max depth: {metrics.max_depth}")
    print(f"  Breadth: {metrics.breadth_at_levels}")
    print(f"  Global items: {metrics.global_count}, Local: {metrics.local_count}")
    print(f"  Recommendation: {metrics.recommendation}")

    # 3. Site Map
    print("\n--- Site Map ---")
    sitemap = SiteMap(domain="saas-example.com")
    sitemap.add_page(PageNode(url="/", title="Home", content_type=ContentType.LANDING))
    sitemap.add_page(PageNode(url="/platform", title="Platform", content_type=ContentType.LANDING, parent_url="/"))
    sitemap.add_page(PageNode(url="/platform/analytics", title="Analytics", content_type=ContentType.CATEGORY, parent_url="/platform"))
    sitemap.add_page(PageNode(url="/platform/automation", title="Automation", content_type=ContentType.CATEGORY, parent_url="/platform"))
    sitemap.add_page(PageNode(url="/pricing", title="Pricing", content_type=ContentType.INFORMATIONAL, parent_url="/"))
    sitemap.add_page(PageNode(url="/blog", title="Blog", content_type=ContentType.ARTICLE, parent_url="/"))
    sitemap.add_page(PageNode(url="/blog/post-1", title="Getting Started Guide", content_type=ContentType.ARTICLE, parent_url="/blog"))
    print(sitemap.render_tree())
    print(f"\n  Total pages: {sitemap.page_count}")
    print(f"  Max depth: {sitemap.max_depth}")
    print(f"  Content types: {sitemap.content_distribution()}")

    # 4. Findability Analysis
    print("\n--- Findability Analysis ---")
    fa = FindabilityAnalyzer()
    tasks = [
        TreeTestTask("Find pricing page", "/pricing", "P01", "/pricing", True, 1, 8),
        TreeTestTask("Find analytics dashboard", "/platform/analytics", "P01", "/platform", True, 2, 15),
        TreeTestTask("Find API documentation", "/docs/api", "P02", "/blog", False, 5, 90),
        TreeTestTask("Find contact form", "/contact", "P02", "/contact", True, 1, 5),
        TreeTestTask("Find tutorial videos", "/resources/tutorials", "P03", "/resources", True, 3, 25),
        TreeTestTask("Find enterprise plan", "/pricing/enterprise", "P03", "/solutions", False, 4, 60),
    ]
    for t in tasks:
        fa.record_task(t)
    fa.record_search("pricing", 3, 1, True)
    fa.record_search("analytics dashboard", 8, 2, True)
    fa.record_search("api docs", 0, 0, False)
    fa.record_search("contact us", 2, 1, True)
    fa.record_search("tutorial videos", 5, 1, True)
    fa.record_search("enterprise pricing", 0, 0, False)
    report = fa.generate_report()
    print(f"  Task completion: {report.task_completion_rate:.0%}")
    print(f"  Mean clicks: {report.mean_clicks}")
    print(f"  Search success: {report.search_success_rate:.0%}")
    print(f"  Zero-result rate: {report.zero_result_rate:.0%}")
    print(f"  First-click accuracy: {report.first_click_accuracy:.0%}")
    for r in report.recommendations:
        print(f"  → {r}")

    # 5. IA Benchmarking
    print("\n--- IA Benchmarking ---")
    benchmarks = [
        ("task_completion_rate", report.task_completion_rate),
        ("search_success_rate", report.search_success_rate),
        ("zero_result_rate", report.zero_result_rate),
        ("mean_clicks_to_target", report.mean_clicks),
    ]
    for name, value in benchmarks:
        rating = IABenchmark.evaluate(name, value)
        print(f"  {name}: {value} [{rating}]")

    comparison = IABenchmark.compare_systems("task_completion_rate", 0.85, 0.72)
    print(f"\n  Comparison A vs B ({comparison.metric_name}):")
    print(f"    A={comparison.system_a_score}, B={comparison.system_b_score}")
    print(f"    Diff: {comparison.difference}, Significant: {comparison.significant}")

    # 6. Labeling System
    print("\n--- Labeling System ---")
    ls = LabelingSystem(name="Navigation Labels")
    ls.add_label("Solutions", ["Enterprise software options", "Product categories", "What the company offers"])
    ls.add_label("Resources", ["Help articles", "Blog and learning", "Marketing materials", "Downloads"])
    ls.add_label("Pricing", ["How much does it cost", "Subscription plans", "Pricing page"])
    ev1 = ls.evaluate_label("Solutions", "Product categories", ["Enterprise software options", "Product categories", "What the company offers"])
    ev2 = ls.evaluate_label("Resources", "Help articles", ["Help articles", "Blog and learning", "Marketing materials", "Downloads"])
    ev3 = ls.evaluate_label("Pricing", "How much does it cost", ["How much does it cost", "Subscription plans", "Pricing page"])
    for ev in [ev1, ev2, ev3]:
        print(f"  {ev.label} [{ev.quality.value}]: comprehension={ev.comprehension_rate:.0%}, consistency={ev.consistency_score:.2f}")

    # 7. Faceted Classification
    print("\n--- Faceted Classification ---")
    fc = FacetedClassification(name="Product Catalog")
    fc.add_facet(FacetDefinition(name="category", values=["Software", "Hardware", "Service"], is_required=True))
    fc.add_facet(FacetDefinition(name="price_range", values=["Budget", "Mid", "Premium"]))
    fc.add_facet(FacetDefinition(name="platform", values=["Web", "iOS", "Android", "Desktop"]))
    fc.add_item({"name": "Analytics Pro", "category": "Software", "price_range": "Premium", "platform": "Web"})
    fc.add_item({"name": "Mobile SDK", "category": "Software", "price_range": "Mid", "platform": "iOS"})
    fc.add_item({"name": "Sensor Kit", "category": "Hardware", "price_range": "Budget", "platform": "Desktop"})
    fc.add_item({"name": "Consulting", "category": "Service", "price_range": "Premium", "platform": "Web"})
    fc.add_item({"name": "Analytics Lite", "category": "Software", "price_range": "Budget", "platform": "Web"})
    results = fc.filter(category=["Software"])
    print(f"  Software items: {[r['name'] for r in results]}")
    counts = fc.facet_counts()
    print(f"  Category distribution: {counts.get('category', {})}")
    print(f"  Price distribution: {counts.get('price_range', {})}")

    print("\n" + "=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
