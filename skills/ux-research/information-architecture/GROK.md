---
name: "information-architecture"
category: "ux-research"
version: "1.0.0"
tags: ["ux-research", "information-architecture", "taxonomy", "navigation", "findability"]
---

# Information Architecture Toolkit

## Overview

Information architecture (IA) is the structural design of shared information environments—the invisible scaffolding that determines whether users can find what they need, understand where they are, and predict where they can go. This module provides a comprehensive toolkit for designing, evaluating, and optimizing information architectures across digital products, from content-heavy editorial sites to complex enterprise applications.

The toolkit covers the full IA lifecycle: content taxonomy design with hierarchical and faceted classification, navigation structure optimization across primary/secondary/tertiary systems, site map generation with parent-child relationship modeling, labeling system design and A/B testing, mental model alignment through tree testing and reverse card sorting, findability metrics (direct vs. exploratory search, success rate, time-to-find), search analytics with zero-result analysis, and IA benchmarking against industry standards.

Built for information architects, content strategists, and UX designers who need to make structural decisions backed by user data rather than intuition, this module bridges card sort data into IA recommendations, converts tree test results into navigation redesign priorities, and tracks findability metrics longitudinally to detect IA regressions before they become user-facing crises. Every structural decision is traceable to evidence.

## Core Capabilities

- **Content Taxonomy Design**: Hierarchical classification with parent-child modeling, controlled vocabulary management, synonym mapping, and polyhierarchy handling for content that belongs in multiple categories
- **Navigation Structure Optimization**: Primary, secondary, and utility navigation modeling with breadth/depth analysis, cross-linking strategy, and persistent vs. contextual navigation pattern selection
- **Site Map Generation**: Automated site map construction from content inventory with relationship mapping, orphan page detection, and depth distribution analysis
- **Labeling Systems**: Consistent label taxonomy with user-preference testing, A/B label experiments, and terminology alignment with user mental models
- **Mental Model Alignment**: Tree testing (reverse card sorting), first-click testing, and open card sort analysis to validate IA decisions against user expectations
- **Findability Metrics**: Direct vs. exploratory search ratio, time-to-first-click, time-to-find, findability rate, and content avoidance detection
- **Search Analytics**: Zero-result query analysis, search refinement tracking, search-to-click-through rates, and synonym/redirect opportunity identification
- **IA Benchmarking**: Cross-study comparison, regression detection, and competitive IA analysis with standardized metrics

## Usage Examples

### Building a Content Taxonomy

```python
from information_architecture import ContentTaxonomy, TaxonomyNode

tax = ContentTaxonomy(name="Product Documentation", root_label="Docs")

# Hierarchical taxonomy
tax.add_node(label="Getting Started", parent_id="root", node_type="category",
             synonyms=["quickstart", "beginner", "intro"])
tax.add_node(label="Installation", parent_id="n1", node_type="category")
tax.add_node(label="System Requirements", parent_id="n2", node_type="content")
tax.add_node(label="Step-by-Step Guide", parent_id="n2", node_type="content")
tax.add_node(label="Configuration", parent_id="n1", node_type="category")
tax.add_node(label="API Reference", parent_id="root", node_type="category")
tax.add_node(label="Authentication", parent_id="n5", node_type="content")
tax.add_node(label="Rate Limits", parent_id="n5", node_type="content")

# Analyze taxonomy structure
depth = tax.depth_distribution()
print(f"Max depth: {depth['max_depth']}, Nodes at depth 1: {depth['distribution'][1]}")

# Find orphan pages (content with no parent)
orphans = tax.find_orphans()
print(f"Orphan pages: {len(orphans)}")
```

### Tree Testing for IA Validation

```python
from information_architecture import TreeTest, TreeTestTask

tree = TreeTest(name="Navigation Validation")

tree.add_category("Products", children=[
    "Laptops", "Desktops", "Tablets", "Accessories", "Software"
])
tree.add_category("Support", children=[
    "Contact Us", "FAQ", "Warranty", "Repairs"
])
tree.add_category("Company", children=[
    "About", "Careers", "Press", "Investors"
])

# Define test tasks
tree.add_task(TreeTestTask(
    task_id="T1",
    prompt="You want to find out if your laptop is still under warranty.",
    correct_path=["Support", "Warranty"],
    direct_correct_path=True
))

tree.add_task(TreeTestTask(
    task_id="T2",
    prompt="You need to buy a new mouse and keyboard for your desk.",
    correct_path=["Products", "Accessories"],
    direct_correct_path=False
))

# Record participant results
tree.record_result(participant_id="P01", task_id="T1",
                   path=["Support", "Warranty"], success=True, time_seconds=12)
tree.record_result(participant_id="P01", task_id="T2",
                   path=["Products", "Accessories"], success=True, time_seconds=8)

report = tree.analyze()
print(f"Directness: {report['directness_rate']:.1%}")
print(f"Success rate: {report['success_rate']:.1%}")
```

### Site Map Generation

```python
from information_architecture import SiteMap, PageNode

sitemap = SiteMap(domain="docs.example.com")

sitemap.add_page(PageNode(url="/", title="Home", depth=0))
sitemap.add_page(PageNode(url="/products", title="Products", depth=1))
sitemap.add_page(PageNode(url="/products/laptops", title="Laptops", depth=2))
sitemap.add_page(PageNode(url="/products/laptops/model-x", title="Model X", depth=3))
sitemap.add_page(PageNode(url="/support", title="Support", depth=1))
sitemap.add_page(PageNode(url="/support/faq", title="FAQ", depth=2))

# Analysis
stats = sitemap.statistics()
print(f"Total pages: {stats['total_pages']}")
print(f"Max depth: {stats['max_depth']}")
print(f"Avg depth: {stats['avg_depth']:.1f}")

# Find depth distribution issues
deep_pages = sitemap.pages_at_depth(4)
print(f"Pages at depth 4+: {len(deep_pages)}")

# Generate visual sitemap
dot = sitemap.to_dot()
print(dot[:300])
```

### Findability Metrics

```python
from information_architecture import FindabilityAnalyzer, SearchEvent

analyzer = FindabilityAnalyzer()

# Log search events
analyzer.add_event(SearchEvent(query="warranty", results_count=12, clicked=True,
                               time_to_click_ms=3200, source="search_bar"))
analyzer.add_event(SearchEvent(query="how to reset", results_count=0, clicked=False,
                               time_to_click_ms=0, source="search_bar"))

# Analyze
metrics = analyzer.findability_metrics()
print(f"Search success rate: {metrics['search_success_rate']:.1%}")
print(f"Zero-result rate: {metrics['zero_result_rate']:.1%}")
print(f"Top zero-result queries: {metrics['top_zero_result_queries'][:5]}")
```

### Open Card Sort Analysis

```python
from information_architecture import CardSort, SortType

sort = CardSort(name="Documentation IA Card Sort", sort_type=SortType.OPEN, participant_count=25)

sort.add_participant("P01", categories={
    "Getting Started": ["Quickstart Guide", "Installation", "System Requirements"],
    "API Docs": ["Authentication", "Rate Limits", "Endpoints"],
    "Troubleshooting": ["FAQ", "Contact Support", "Bug Reports"],
})

sort.add_participant("P02", categories={
    "Setup": ["Quickstart Guide", "Installation"],
    "API Reference": ["Authentication", "Rate Limits", "Endpoints", "System Requirements"],
    "Help": ["FAQ", "Contact Support", "Bug Reports"],
})

results = sort.analyze()
print(f"Agreement score: {results['agreement_score']:.1%}")
print(f"Suggested categories: {results['suggested_categories']}")
for cat, items in results['dendrogram'].items():
    print(f"  {cat}: {', '.join(items)}")
```

## Best Practices

1. **Let users build your taxonomy**: Use open card sorts to discover natural groupings rather than imposing organizational logic. The way your team categorizes content (by department, by product) rarely matches how users think about it. Validate with at least 15-20 card sort participants per user segment.

2. **Test navigation before building it**: Tree testing is cheap insurance against structural failures. Run tree tests with 20+ participants before committing to a navigation structure. A failed tree test costs hours to fix; a failed navigation launch costs months.

3. **Depth vs. breadth is a false dichotomy**: The real question is "where does the user's mental model expect this to live?" Users tolerate depth when the path is intuitive ("Products > Laptops > Model X") but not when it's arbitrary ("Company > Resources > Technical > Laptops"). Design for mental model alignment, not arbitrary depth limits.

4. **Label with user language, not internal jargon**: Your product team calls it "Configuration" but users call it "Settings." Your taxonomy labels should use the vocabulary your users actually use. Validate labels through first-click testing and search log analysis, not stakeholder meetings.

5. **Monitor findability continuously**: IA doesn't fail in a single dramatic moment—it degrades as content accumulates. Track zero-result search queries weekly, monitor content avoidance patterns, and run annual tree tests against your navigation. IA regression is a slow crisis.

6. **Treat search as an IA failure signal**: When users search, navigation has already failed them. Track the search-to-navigate ratio. High search usage on specific topics suggests those topics are poorly surfaced in navigation. Fix the structure, not the search engine.

7. **Polyhierarchy is acceptable**: Content that genuinely belongs in two categories should appear in both. Forced single-categorization creates artificial boundaries. Use cross-links and faceted navigation to handle legitimate polyhierarchy without creating confusion.

8. **Document your IA decisions**: Every structural choice should be traceable to user data. "We placed 'Pricing' under 'Products' because 87% of tree test participants found it there." This evidence trail protects your IA from stakeholder whims and organizational politics.

## Related Modules

- [user-research](../user-research/GROK.md) — Card sort and tree test participant recruitment and persona alignment
- [usability-testing](../usability-testing/GROK.md) — Task success measurement for IA-related tasks
- [interaction-design](../interaction-design/GROK.md) — Navigation interaction patterns and micro-interactions
- [accessibility](../accessibility/GROK.md) — Accessible navigation patterns and screen reader IA

## When to Use This Module

Use this module whenever structural decisions about content organization, navigation labeling, or findability metrics are needed. It is particularly valuable during early product planning (taxonomy and navigation design), after major content expansions (regression testing via tree tests), and when search analytics reveal persistent zero-result patterns indicating structural gaps.

---

## Advanced Configuration

### Taxonomy Governance Rules

```python
from information_architecture import TaxonomyGovernance

governance = TaxonomyGovernance(
    max_depth=4,
    max_children_per_node=8,
    require_synonyms=True,
    require_description=True,
    allow_polyhierarchy=True,
    duplicate_detection=True,
)
violations = governance.validate(taxonomy)
```

### Search Analytics Pipeline

```python
from information_architecture import SearchAnalyticsPipeline

pipeline = SearchAnalyticsPipeline(
    data_source="elasticsearch",
    index="search_logs",
    zero_result_threshold=0.15,
    refinement_tracking=True,
)
pipeline.run_daily_analysis()
```

## Architecture Patterns

### IA Lifecycle

```
Content Audit
    │
    ▼
┌──────────────┐
│ Taxonomy     │── Card sort, controlled vocabulary
│ Design       │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Navigation   │── Tree test, first-click test
│ Validation   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Implementation│── Breadcrumbs, sitemap, labels
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Monitoring   │── Findability metrics, search analytics
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Iteration    │── Regression testing, optimization
└──────────────┘
```

## Integration Guide

### CMS Integration

```python
from information_architecture import CMSBridge

bridge = CMSBridge(provider="contentful")
bridge.sync_taxonomy(taxonomy)
bridge.validate_url_structure()
```

### Analytics Integration

```python
from information_architecture import AnalyticsBridge

analytics = AnalyticsBridge(provider="google_analytics")
search_data = analytics.get_search_queries(time_range="30d")
findability = analyzer.analyze_search_data(search_data)
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Cached tree tests | Instant re-testing after changes |
| Automated taxonomy validation | Catch structural issues early |
| Search log aggregation | Real-time findability monitoring |
| Dendrogram caching | Fast card sort re-analysis |

## Security Considerations

- **Content access controls**: IA must respect role-based content visibility
- **URL security**: Prevent information leakage through URL patterns
- **Search privacy**: Don't log PII in search queries
- **Taxonomy versioning**: Audit trail for structural changes

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Low tree test success | Navigation labels unclear | Test alternative labels |
| High zero-result rate | Missing content or poor labels | Add content or fix taxonomy |
| Card sort low agreement | Cards too similar or ambiguous | Split or clarify card labels |
| Deep navigation (>4 levels) | Over-categorization | Flatten with cross-links |
| Search-to-navigate ratio high | Navigation fails for common tasks | Surface popular search topics in nav |

## API Reference

### ContentTaxonomy

```python
class ContentTaxonomy:
    def __init__(self, name: str, root_label: str)
    def add_node(self, label: str, parent_id: str, node_type: str, synonyms: list = None) -> TaxonomyNode
    def depth_distribution(self) -> dict
    def find_orphans(self) -> list
    def validate(self, governance: TaxonomyGovernance = None) -> list
```

### TreeTest

```python
class TreeTest:
    def __init__(self, name: str)
    def add_category(self, name: str, children: list) -> None
    def add_task(self, task: TreeTestTask) -> None
    def record_result(self, participant_id: str, task_id: str, path: list, success: bool, time_seconds: float) -> None
    def analyze(self) -> TreeTestReport
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class TaxonomyNode:
    id: str
    label: str
    parent_id: str
    node_type: str
    synonyms: list
    children: list

@dataclass
class TreeTestTask:
    task_id: str
    prompt: str
    correct_path: list
    direct_correct_path: bool

@dataclass
class FindabilityMetrics:
    search_success_rate: float
    zero_result_rate: float
    time_to_find_avg_ms: float
    search_to_navigate_ratio: float
```

## Deployment Guide

### Installation

```bash
pip install information-architecture
```

### IA Review Cadence

1. Quarterly tree tests on navigation
2. Monthly search analytics review
3. Annual full taxonomy audit
4. Continuous zero-result monitoring

## Monitoring & Observability

```python
from information_architecture import MetricsCollector

collector = MetricsCollector()
collector.gauge("ia.findability.rate", rate)
collector.counter("ia.search.zero_result", count, tags={"query": query})
collector.histogram("ia.time_to_find_ms", duration)
collector.gauge("ia.tree_test.success_rate", rate, tags={"task_id": tid})
```

## Testing Strategy

```python
import pytest
from information_architecture import ContentTaxonomy, TreeTest

def test_taxonomy_depth():
    tax = ContentTaxonomy(name="Test", root_label="Root")
    tax.add_node("A", "root", "category")
    tax.add_node("A1", "n1", "content")
    dist = tax.depth_distribution()
    assert dist["max_depth"] == 2
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added search analytics | Connect search data source |
| 2.0.0 | New taxonomy format | Run migration script |

## Glossary

| Term | Definition |
|------|-----------|
| **Tree Test** | Validates navigation by testing findability in a text-only hierarchy |
| **Card Sort** | Participants group content items into categories |
| **Dendrogram** | Tree diagram showing card sort clustering results |
| **Findability** | Ease of locating specific content |
| **Polyhierarchy** | Item belonging to multiple parent categories |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with taxonomy design and tree testing
- Card sort analysis with dendrogram clustering
- Findability metrics and search analytics
- Site map generation

## Contributing Guidelines

```bash
git clone https://github.com/example/information-architecture.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Tree Test Metrics Reference

| Metric | Calculation | Target |
|--------|------------|--------|
| Success rate | Correct path / total attempts | > 70% |
| Directness | First click on correct path | > 60% |
| Time to find | Seconds from start to find | < 30s |
| Post-find confidence | Self-reported confidence | > 3.5/5 |
| Path similarity | Similarity to ideal path | > 0.7 |

### Card Sort Analysis Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Agreement score | How much participants agree | > 60% |
| Similarity matrix | Pairwise card grouping frequency | — |
| Dendrogram clusters | Natural groupings found | — |
| Variability score | How much agreement varies | < 0.3 |
| Recommended categories | Optimal number of categories | 5-8 |

### Navigation Depth Guidelines

| Depth | User Expectation | Example |
|-------|-----------------|---------|
| 1 click | Most important tasks | Home → Dashboard |
| 2 clicks | Common tasks | Home → Products → Laptops |
| 3 clicks | Secondary tasks | Home → Support → Warranty → Status |
| 4+ clicks | Deep content | Home → Resources → Technical → Specs → Model X |

### Label Quality Criteria

| Criterion | Good Example | Bad Example |
|-----------|-------------|-------------|
| Specific | "Pricing Plans" | "Info" |
| Familiar | "Settings" | "Configuration Panel" |
| Concise | "Contact Us" | "Get In Touch With Our Team" |
| Consistent | "My Account" | "User Profile" (mixed) |
| Action-oriented | "Write a Review" | "Reviews" |

### Search Analytics Reference

| Metric | Calculation | Target |
|--------|------------|--------|
| Search usage rate | Searches / sessions | < 30% |
| Zero-result rate | Zero-result searches / total | < 5% |
| Search success rate | Clicked result / searches | > 70% |
| Search refinement rate | Refined searches / total | < 20% |
| Time to first click | Time from search to click | < 5s |

### IA Governance Checklist

```
QUARTERLY IA REVIEW
    □ Run tree test on current navigation
    □ Analyze search logs for zero-result queries
    □ Review content inventory for orphans
    □ Check taxonomy for new content
    □ Validate label consistency
    □ Test new navigation concepts
    □ Update sitemap
    □ Document changes

CONTENT MIGRATION CHECKLIST
    □ Audit all existing content
    □ Map content to new taxonomy
    □ Set up redirects for moved content
    □ Test all internal links
    □ Update search index
    □ Train content editors
    □ Monitor 404 errors post-launch
```

### IA Documentation Template

```markdown
# Information Architecture Document

## Navigation Structure
### Primary Navigation
- [Item 1] → [URL]
- [Item 2] → [URL]
  - [Sub-item 2.1] → [URL]
  - [Sub-item 2.2] → [URL]

### Secondary Navigation
- [Item] → [URL]

## Taxonomy
### Categories
- [Category 1]
  - [Subcategory 1.1]
  - [Subcategory 1.2]
- [Category 2]

## Labels
| Location | Current Label | User-tested Label | Status |
|----------|--------------|-------------------|--------|
| Nav item 1 | Products | Products | Approved |
| Nav item 2 | Resources | Help Center | Needs update |

## Sitemap
[Visual sitemap or tree diagram]
```

### Complete Search Analytics Reference

| Query Type | Example | Action |
|-----------|---------|--------|
| Zero-result | "xyz123" | Add content or synonyms |
| High refinement | "pricing cost" → "plans" | Improve labels |
| High exit | "contact" → leave | Make contact easier |
| Low CTR | "help" → no clicks | Improve result snippets |
| Brand + feature | "Acme pricing" | Ensure brand pages rank |

### Complete Content Inventory Template

| URL | Title | Type | Status | Owner | Last Updated | Views | Bounce Rate |
|-----|-------|------|--------|-------|-------------|-------|-------------|
| / | Home | Page | Live | Marketing | 2024-01 | 10,000 | 30% |
| /products | Products | Page | Live | Product | 2024-01 | 5,000 | 25% |
| /blog/post-1 | Blog Post | Article | Live | Content | 2024-01 | 2,000 | 45% |
| /old-page | Old Page | Page | Redirect | — | 2023-06 | 100 | 90% |

### Complete URL Structure Reference

| Pattern | Example | Use Case |
|---------|---------|----------|
| /category | /products | Top-level category |
| /category/item | /products/laptops | Item in category |
| /category/item/detail | /products/laptops/model-x | Specific item |
| /blog/year/month/slug | /blog/2024/01/post | Blog posts |
| /support/topic | /support/billing | Support topic |
| /support/topic/item | /support/billing/refund | Specific article |

### Navigation System Design Reference

| Navigation Type | Use Case | Depth Support | Examples |
|----------------|----------|---------------|----------|
| Primary navigation | Top-level sections | 1-2 levels | Header bar, sidebar |
| Secondary navigation | Within a section | 2-3 levels | Section submenus |
| Utility navigation | Account, settings | 1 level | Header right side |
| Breadcrumbs | Current location path | Shows full path | Home > Products > Laptops |
| Footer navigation | Supplemental links | 1-2 levels | Site map, legal links |
| Contextual navigation | Related content | 1 level | "See also" links |
| Faceted navigation | Filtered browsing | Variable | Category filters |
| Tag-based navigation | Topic discovery | Flat | Tag clouds, tag pages |

### Content Organization Patterns

| Pattern | Description | Best For | Avoid When |
|---------|-------------|----------|------------|
| Hierarchical | Tree with parent-child | Large content sets | Content belongs in multiple places |
| Faceted | Multiple orthogonal dimensions | E-commerce, catalogs | Simple sites with few items |
| Chronological | Time-ordered | News, blogs, changelogs | Evergreen reference content |
| Task-based | Organized by user goals | Support sites, tools | Content spans many tasks |
| Audience-based | Segmented by user type | B2B with distinct personas | Overlapping audience needs |
| Topic-based | Grouped by subject matter | Documentation, wikis | No clear topic boundaries |
| Alphabetical | A-Z listing | Directories, glossaries | Large content sets (>500 items) |
| Hybrid | Combination of above | Most real-world sites | Never (always recommended) |

### Taxonomy Governance Template

```markdown
# Taxonomy Governance Policy

## Naming Conventions
- Labels: Title Case, max 40 characters
- Synonyms: lowercase, pipe-delimited
- Descriptions: max 100 characters

## Structural Rules
- Max depth: 4 levels
- Max children per node: 8
- Min children for branch: 2 (or flatten)
- Polyhierarchy allowed: Yes (with cross-links)

## Maintenance Schedule
- Weekly: New content categorization
- Monthly: Label consistency audit
- Quarterly: Full taxonomy review
- Annually: Structural redesign assessment

## Change Management
1. Propose change with rationale
2. Test with 5+ users (first-click test)
3. Document decision and evidence
4. Implement with redirects
5. Monitor findability metrics
```

### Search System Design Reference

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| Query processing | Parse and normalize user input | Tokenization, stemming, spell-check |
| Ranking algorithm | Order results by relevance | BM25, TF-IDF, or ML-based |
| Faceted search | Allow filtering by attributes | Category, date, type filters |
| Auto-suggest | As-you-type recommendations | Prefix matching, popularity-weighted |
| Zero-result handling | Help when nothing matches | Synonyms, "Did you mean?", related content |
| Search analytics | Track what users search for | Query logging, click tracking |
| Synonym management | Map alternate terms | User-tested synonym pairs |
| Redirect rules | Direct known queries to content | High-volume queries to landing pages |

### Findability Scorecard Template

```markdown
# Findability Scorecard: [Section]

## Direct Navigation (Users find without searching)
- Target: > 70% first-click success
- Actual: [X]%
- Status: Pass/Fail

## Search Recovery (Users find via search when nav fails)
- Target: > 60% search success rate
- Actual: [X]%
- Status: Pass/Fail

## Time to Find
- Target: < 30 seconds
- Actual: [X] seconds
- Status: Pass/Fail

## Label Clarity
- Target: > 80% agreement on meaning
- Actual: [X]%
- Status: Pass/Fail

## Navigation Depth
- Target: ≤ 3 clicks to any page
- Actual: [X] clicks average
- Status: Pass/Fail

## Overall Findability Score: [X]/100
```

### Card Sort Best Practices Quick Reference

| Aspect | Recommendation |
|--------|---------------|
| Participant count | 15-20 per user segment |
| Card count | 30-50 items |
| Session duration | 30-45 minutes |
| Incentive | Comparable to interview rates |
| Open sort | Use for discovering categories |
| Closed sort | Use for validating proposed structure |
| Hybrid sort | Use when you have partial structure |
| Remote vs. in-person | Remote for scale, in-person for depth |
| Analysis method | Dendrogram + similarity matrix |
| Agreement threshold | > 60% considered good |

### Tree Test Task Design Guide

```markdown
# Tree Test Task Design

## Task Writing Rules
1. Use realistic scenarios, not abstract navigation instructions
2. Include context ("You want to...") not commands ("Find...")
3. Avoid using words that appear in navigation labels
4. Test both known-item and exploratory tasks
5. Include 5-10 tasks per test

## Good vs. Bad Tasks

GOOD: "You just bought a laptop and want to check if it's covered 
       under warranty."
BAD:  "Click on 'Support' then 'Warranty'."

GOOD: "You want to compare the features of two different tablets 
       before making a purchase."
BAD:  "Go to the products page and find tablets."

GOOD: "A friend recommended a software tool. You want to find out 
       what it does and if it would work for your team."
BAD:  "Navigate to the software section."

## Task Types
- Known-item: User knows what they're looking for
- Exploratory: User is browsing or researching
- Recovery: User is lost and trying to find their way back
- Discrete: Single correct answer
- Ambiguous: Multiple valid paths
```
