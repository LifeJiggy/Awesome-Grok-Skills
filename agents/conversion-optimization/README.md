# Conversion Optimization Agent

> Comprehensive CRO — A/B testing, funnel optimization, UX analysis, landing page auditing, and CRO strategy.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)](CHANGELOG.md)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [A/B Testing](#ab-testing)
  - [Hypothesis Management](#hypothesis-management)
  - [Funnel Analysis](#funnel-analysis)
  - [UX Analysis](#ux-analysis)
  - [Landing Page Audit](#landing-page-audit)
  - [CRO Strategy](#cro-strategy)
  - [Form & Checkout Analysis](#form--checkout-analysis)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Conversion Optimization Agent is a comprehensive system for managing the full CRO lifecycle. It handles hypothesis generation and prioritization, A/B test design and statistical analysis, conversion funnel optimization, UX analysis, landing page auditing, and CRO strategy development.

Built for growth teams, product managers, UX researchers, and marketing professionals who need a structured, statistically rigorous approach to improving conversion rates.

### What Makes This Agent Different

- **Statistically Rigorous**: Z-tests, p-values, confidence intervals — no guessing
- **Hypothesis-Driven**: Every test starts with a documented hypothesis
- **Full Lifecycle**: From hypothesis through implementation and monitoring
- **Multiple Frameworks**: ICE, RICE, PIE, and more for prioritization
- **Comprehensive Analysis**: Funnel, UX, landing page, form, and checkout analysis
- **Actionable Outputs**: Quick wins, test roadmaps, and recommendations

---

## Features

| Feature | Description |
|---------|-------------|
| A/B Testing | Full test lifecycle with statistical analysis |
| Hypothesis Management | Create, prioritize, and track hypotheses |
| Funnel Analysis | Step-by-step drop-off analysis with insights |
| UX Analysis | Comprehensive UX scoring and issue identification |
| Landing Page Audit | Element-by-element analysis with test roadmap |
| CRO Strategy | Strategic planning with KPIs and roadmaps |
| Form Analytics | Form completion and abandonment analysis |
| Checkout Analysis | Checkout flow optimization |
| Statistical Engine | Z-test, p-value, confidence intervals |
| Prioritization | ICE, RICE, PIE frameworks |
| Recommendations | Page-type-specific optimization suggestions |
| Dashboard | Test status and performance overview |
| Export | JSON, CSV, Markdown, PDF formats |
| Caching | TTL-based in-memory cache |
| Audit Trail | Full operation logging |

---

## Quick Start

```python
from agents.conversion_optimization.agent import ConversionOptimizationAgent

# Initialize agent
agent = ConversionOptimizationAgent()

# Create A/B test
test = agent.create_ab_test(
    name="CTA Button Test",
    url="/pricing",
    variants=[("Blue Control", True), ("Green Variant", False)],
)

# Analyze results
results = agent.analyze_test_results(test.test_id)
print(f"Winner: {results.winner}, Lift: {results.lift:.2%}")

# Get status
print(agent.get_status())
```

### Run the Demo

```bash
python agents/conversion-optimization/agent.py
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# No external dependencies required
# Python 3.10+ with standard library only
```

---

## Usage

### A/B Testing

```python
from agents.conversion_optimization.agent import ConversionOptimizationAgent, TestType, StatisticalSignificance

agent = ConversionOptimizationAgent()

# Create test
test = agent.create_ab_test(
    name="Hero Headline Test",
    url="/",
    variants=[
        ("Current Headline", True),
        ("Benefit-focused Headline", False),
        ("Question Headline", False),
    ],
    test_type=TestType.A_B_N,
)

# Manage lifecycle
agent.approve_test(test.test_id)
agent.start_test(test.test_id)

# Analyze with statistics
results = agent.analyze_test_results(test.test_id)
print(f"Significance: {results.significance.value}")
print(f"P-value: {results.p_value:.6f}")

if results.significance in [StatisticalSignificance.HIGH, StatisticalSignificance.VERY_HIGH]:
    print(f"Implement winner! Lift: {results.lift:.2%}")
```

### Hypothesis Management

```python
# Create hypothesis
hypothesis = agent.create_hypothesis(
    title="Social Proof Above Fold",
    observation="Social proof is below the fold on landing page",
    insight="Social proof near CTA increases conversion by 15-20%",
    hypothesis_statement="IF we add customer logos above the fold, THEN conversion rate will increase by 15%, BECAUSE social proof reduces purchase anxiety.",
    impact=8,
    confidence=7,
    ease=7,
)

# Prioritize all hypotheses
prioritized = agent.prioritize_hypotheses()
for i, h in enumerate(prioritized, 1):
    print(f"{i}. {h.title} (ICE: {h.ice_score:.1f})")
```

### Funnel Analysis

```python
# Analyze funnel
funnel = agent.analyze_funnel(
    name="SaaS Signup Funnel",
    steps=[
        {"name": "Homepage", "stage": "awareness", "visitors": 10000, "conversions": 8500},
        {"name": "Pricing", "stage": "consideration", "visitors": 8500, "conversions": 4200},
        {"name": "Signup", "stage": "intent", "visitors": 4200, "conversions": 2100},
        {"name": "Verify", "stage": "evaluation", "visitors": 2100, "conversions": 1800},
        {"name": "Activate", "stage": "activation", "visitors": 1800, "conversions": 1200},
    ],
)

print(f"Overall conversion: {funnel.overall_conversion_rate:.2%}")
print(f"Biggest drop-off: {funnel.biggest_drop_off}")
```

### UX Analysis

```python
# Analyze UX
ux_report = agent.analyze_ux(page_url="/pricing", page_type="pricing")

print(f"UX Score: {ux_report.overall_score:.1f}")
print(f"Issues: {len(ux_report.issues)}")
print(f"Conversion barriers: {len(ux_report.conversion_barriers)}")

for barrier in ux_report.conversion_barriers:
    print(f"  - {barrier}")
```

### Landing Page Audit

```python
# Audit landing page
audit = agent.audit_landing_page(url="/pricing", page_type="pricing")

print(f"Score: {audit.overall_score:.1f}")
print(f"Quick wins: {len(audit.quick_wins)}")
print(f"Test roadmap: {len(audit.ab_test_roadmap)} phases")

for qw in audit.quick_wins:
    print(f"  Quick win: {qw}")
```

### CRO Strategy

```python
# Create strategy
strategy = agent.create_cro_strategy(
    name="Q3 CRO Strategy",
    budget=50000,
    timeline_months=3,
)

# Add hypotheses
agent.add_hypothesis_to_strategy(strategy.strategy_id, hypothesis.hypothesis_id)

# Prioritize
strategy.prioritize_hypotheses()
```

### Form & Checkout Analysis

```python
# Analyze form
form = agent.analyze_form(
    form_name="Free Trial Signup",
    page_url="/signup",
    total_submissions=5000,
    successful_submissions=2800,
)
print(f"Completion rate: {form.completion_rate:.2%}")

# Analyze checkout
checkout = agent.analyze_checkout(
    steps=[
        {"name": "Cart", "visitors": 5000, "conversions": 4200},
        {"name": "Checkout", "visitors": 4200, "conversions": 3800},
        {"name": "Payment", "visitors": 3800, "conversions": 3200},
        {"name": "Confirm", "visitors": 3200, "conversions": 2600},
    ],
)
print(f"Completion rate: {checkout.overall_completion_rate:.2%}")
```

---

## API Reference

### ConversionOptimizationAgent

| Method | Description | Returns |
|--------|-------------|---------|
| `create_hypothesis()` | Create test hypothesis | `Hypothesis` |
| `update_hypothesis()` | Update hypothesis | `Hypothesis` |
| `get_hypothesis()` | Get hypothesis by ID | `Hypothesis` |
| `list_hypotheses()` | List all hypotheses | `List[Hypothesis]` |
| `prioritize_hypotheses()` | Prioritize using framework | `List[Hypothesis]` |
| `create_ab_test()` | Create A/B test | `ABTest` |
| `update_ab_test()` | Update test | `ABTest` |
| `approve_test()` | Approve for execution | `ABTest` |
| `start_test()` | Start running test | `ABTest` |
| `stop_test()` | Stop running test | `ABTest` |
| `analyze_test_results()` | Analyze with statistics | `ExperimentResult` |
| `get_test()` | Get test by ID | `ABTest` |
| `list_tests()` | List all tests | `List[ABTest]` |
| `get_test_dashboard()` | Get dashboard view | `Dict` |
| `analyze_funnel()` | Analyze conversion funnel | `FunnelAnalysis` |
| `compare_funnels()` | Compare two funnels | `Dict` |
| `get_funnel()` | Get funnel by ID | `FunnelAnalysis` |
| `list_funnels()` | List all funnels | `List[FunnelAnalysis]` |
| `analyze_ux()` | Analyze page UX | `UXReport` |
| `get_ux_report()` | Get UX report by ID | `UXReport` |
| `list_ux_reports()` | List all UX reports | `List[UXReport]` |
| `audit_landing_page()` | Audit landing page | `LandingPageAudit` |
| `get_landing_page_audit()` | Get audit by ID | `LandingPageAudit` |
| `list_landing_page_audits()` | List all audits | `List[LandingPageAudit]` |
| `create_cro_strategy()` | Create CRO strategy | `CROStrategy` |
| `add_hypothesis_to_strategy()` | Add hypothesis to strategy | `CROStrategy` |
| `get_cro_strategy()` | Get strategy by ID | `CROStrategy` |
| `list_cro_strategies()` | List all strategies | `List[CROStrategy]` |
| `analyze_form()` | Analyze form performance | `FormAnalytics` |
| `analyze_checkout()` | Analyze checkout flow | `CheckoutAnalysis` |
| `get_cro_recommendations()` | Get optimization recs | `List[Dict]` |
| `get_status()` | Get agent status | `Dict` |
| `get_operation_log()` | Get operation log | `List[Dict]` |
| `clear_cache()` | Clear cache | `int` |
| `export_data()` | Export all data | `str` |

---

## Examples

### Example 1: Complete CRO Workflow

```python
agent = ConversionOptimizationAgent()

# 1. Observe and hypothesize
h = agent.create_hypothesis(
    title="CTA Button Optimization",
    observation="Blue CTA button gets 2.1% CTR",
    insight="Green buttons perform 15% better for action CTAs",
    hypothesis_statement="IF we change CTA to green, THEN CTR will increase by 15%, BECAUSE green signals action.",
    impact=7, confidence=6, ease=9,
)

# 2. Create and run test
test = agent.create_ab_test(
    name="CTA Color Test",
    url="/pricing",
    variants=[("Blue", True), ("Green", False)],
    hypothesis_id=h.hypothesis_id,
)
agent.approve_test(test.test_id)
agent.start_test(test.test_id)

# 3. Analyze
results = agent.analyze_test_results(test.test_id)

# 4. Implement if significant
if results.significance in [StatisticalSignificance.HIGH, StatisticalSignificance.VERY_HIGH]:
    print(f"Winner found! Lift: {results.lift:.2%}")
else:
    print("No significant difference — iterate")
```

### Example 2: Funnel Optimization

```python
# Analyze and optimize
funnel = agent.analyze_funnel(
    name="Checkout Funnel",
    steps=[
        {"name": "Cart", "visitors": 10000, "conversions": 8000},
        {"name": "Shipping", "visitors": 8000, "conversions": 5000},
        {"name": "Payment", "visitors": 5000, "conversions": 4000},
        {"name": "Confirm", "visitors": 4000, "conversions": 3800},
    ],
)

# Focus on biggest drop-off
biggest = funnel.find_biggest_drop_off()
print(f"Optimize: {biggest.name} ({biggest.drop_off_rate:.1%} drop-off)")

# Get recommendations
recs = agent.get_cro_recommendations(page_type="checkout")
```

### Example 3: Landing Page Optimization

```python
# Audit → Quick wins → Test roadmap
audit = agent.audit_landing_page(url="/pricing")

# Quick wins (implement immediately)
for qw in audit.quick_wins[:3]:
    print(f"Do now: {qw}")

# Test roadmap (A/B test)
for phase in audit.ab_test_roadmap:
    for test in phase["tests"]:
        print(f"Test: {test}")
```

---

## Configuration

```python
from agents.conversion_optimization.agent import Config, TestConfig, FunnelConfig

config = Config(
    agent_name="MyCROAgent",
    version="1.0.0",
    log_level="DEBUG",
    enable_caching=True,
    cache_ttl_seconds=1800,
    ab_test=TestConfig(
        default_confidence_level=0.95,
        minimum_sample_size=200,
        maximum_test_duration_days=30,
        minimum_runtime_days=7,
        auto_stop_on_significance=True,
        false_positive_rate=0.05,
        minimum_detectable_effect=0.02,
    ),
    funnel=FunnelConfig(
        default_attribution_window_days=30,
        drop_off_threshold=0.10,
        cohort_analysis_enabled=True,
    ),
)

agent = ConversionOptimizationAgent(config=config)
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `agent_name` | str | `"ConversionOptimizationAgent"` | Agent name |
| `version` | str | `"3.0.0"` | Agent version |
| `log_level` | str | `"INFO"` | Logging level |
| `enable_caching` | bool | `True` | Enable cache |
| `cache_ttl_seconds` | int | `3600` | Cache TTL |
| `ab_test.default_confidence_level` | float | `0.95` | Confidence level |
| `ab_test.minimum_sample_size` | int | `100` | Min sample size |
| `ab_test.minimum_runtime_days` | int | `7` | Min test duration |
| `ab_test.false_positive_rate` | float | `0.05` | Alpha level |
| `ab_test.minimum_detectable_effect` | float | `0.02` | MDE |
| `funnel.drop_off_threshold` | float | `0.10` | High drop-off threshold |

---

## Best Practices

### A/B Testing

1. **Always start with a hypothesis** — no random testing
2. **One test per page** — avoid overlapping experiments
3. **Run for 7+ days minimum** — capture weekly patterns
4. **Wait for 95% confidence** — standard significance level
5. **100+ conversions per variant** — minimum for reliability
6. **Document everything** — hypothesis, setup, results, learnings

### Statistical Rigor

1. **Use proper statistical tests** — Z-test for proportions
2. **Calculate p-values** — don't just look at raw percentages
3. **Report confidence intervals** — show uncertainty
4. **Check sample size** — ensure adequate power
5. **Account for multiple comparisons** — Bonferroni correction

### Funnel Optimization

1. **5-7 steps maximum** — too many dilutes insights
2. **Focus on biggest drop-off** — highest impact
3. **Segment by source** — different behaviors
4. **Compare time periods** — identify trends
5. **Test one step at a time** — isolate impact

### Landing Page Optimization

1. **Above-fold first** — headline, CTA, social proof
2. **Quick wins before big tests** — immediate impact
3. **Mobile-first** — 60%+ traffic is mobile
4. **Page speed matters** — every 1s delay costs 7% conversion
5. **Clear value proposition** — answer "why should I care?"

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No statistical significance | Insufficient sample size | Run test longer or increase MDE |
| Funnel shows unexpected drop-off | Technical error on step | Check for bugs, tracking issues |
| Low landing page score | Multiple UX issues | Start with quick wins |
| Form completion < 50% | Too many fields | Reduce to essential fields only |
| High checkout abandonment | Unexpected costs | Show total cost early |
| Test results inconsistent | Overlapping tests | Ensure one test per page |

### Debug Mode

```python
config = Config(log_level="DEBUG")
agent = ConversionOptimizationAgent(config=config)

# Check operation log
log = agent.get_operation_log(limit=10)
for entry in log:
    print(f"{entry['timestamp']}: {entry['operation']}")

# Export data for inspection
data = agent.export_data(format="json")
print(data[:1000])
```

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
python agents/conversion-optimization/agent.py
```

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

*Conversion Optimization Agent v3.0.0 — Part of the Awesome Grok Skills collection.*

*Last updated: 2026-07-06*
