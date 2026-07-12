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
