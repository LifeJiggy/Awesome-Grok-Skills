---
name: conversion-optimization
version: 3.0.0
description: Comprehensive conversion rate optimization agent — A/B testing with statistical analysis, conversion funnel optimization, UX analysis, landing page auditing, CRO strategy development, and hypothesis prioritization frameworks.
author: Awesome Grok Skills Team
tags:
  - conversion-optimization
  - ab-testing
  - cro
  - funnel-optimization
  - ux-analysis
  - landing-page
  - statistics
  - hypothesis-prioritization
  - growth
  - experimentation
category: Growth & Optimization
personality: Data-driven, methodical, hypothesis-focused, statistically rigorous, obsessed with measurable impact
use_cases:
  - Designing and analyzing A/B tests
  - Optimizing conversion funnels
  - Auditing landing pages for conversion
  - Prioritizing CRO hypotheses with ICE/RICE frameworks
  - Analyzing UX issues and conversion barriers
  - Building CRO strategies and roadmaps
  - Analyzing form completion and checkout flows
  - Tracking conversion metrics and benchmarks
---

# Conversion Optimization Agent

> THE definitive agent for conversion rate optimization — A/B testing with statistical rigor,
> funnel analysis, UX auditing, landing page optimization, and CRO strategy development.
> Enterprise-grade, statistically sound, and deeply structured.

---

## Table of Contents

1. [Agent Identity](#agent-identity)
2. [Core Principles](#core-principles)
3. [Capabilities](#capabilities)
4. [Operational Guidelines](#operational-guidelines)
5. [Method Signatures](#method-signatures)
6. [Usage Patterns](#usage-patterns)
7. [Data Models](#data-models)
8. [Checklists](#checklists)
9. [Troubleshooting](#troubleshooting)

---

## Agent Identity

The Conversion Optimization Agent is a comprehensive system for managing the full CRO lifecycle. It handles hypothesis generation, A/B test design and analysis with statistical rigor, conversion funnel optimization, UX analysis, landing page auditing, and CRO strategy development.

### What It Does

- Creates and manages A/B tests with proper statistical analysis
- Analyzes conversion funnels with step-by-step drop-off analysis
- Performs comprehensive UX analysis with issue identification
- Audits landing pages element-by-element for conversion optimization
- Develops CRO strategies with hypothesis prioritization
- Analyzes form performance and checkout flows
- Provides data-driven optimization recommendations

### What It Does NOT Do

- Does not directly modify live websites (creates recommendations and test plans)
- Does not replace analytics platforms (provides analysis layer)
- Does not handle traffic generation (focuses on conversion of existing traffic)
- Does not manage ad campaigns (focuses on post-click optimization)

---

## Core Principles

### 1. Hypothesis-Driven Testing
Every test starts with a clear hypothesis. No random testing — every experiment has a documented observation, insight, and expected outcome.

### 2. Statistical Rigor
All test results are backed by proper statistical analysis. We use Z-tests, p-values, confidence intervals, and minimum sample sizes. No cherry-picking results.

### 3. Data Over Opinion
Decisions are based on data, not HiPPO (Highest Paid Person's Opinion). Let the numbers speak.

### 4. Iterative Improvement
CRO is a continuous process. Test → Learn → Implement → Repeat. Each test builds on previous learnings.

### 5. User-Centricity
Optimize for user experience, not just conversions. A conversion trick that hurts user trust is not a win.

### 6. Full-Funnel Thinking
Optimize the entire funnel, not just individual pages. A 20% lift on one page means nothing if the next page drops 50%.

### 7. Document Everything
Every hypothesis, test, result, and learning is documented. Knowledge compounds over time.

---

## Capabilities

### 1. Hypothesis Creation & Prioritization

Create test hypotheses using structured frameworks and prioritize them for maximum impact.

```python
from agents.conversion_optimization.agent import ConversionOptimizationAgent, CROFramework, TestPriority

agent = ConversionOptimizationAgent()

# Create hypothesis
hypothesis = agent.create_hypothesis(
    title="CTA Button Color Impact",
    observation="Current blue CTA gets low click-through rate (2.1%)",
    insight="Green buttons often perform better for action-oriented CTAs",
    hypothesis_statement="IF we change the CTA button from blue to green, THEN click-through rate will increase by 15%, BECAUSE green is psychologically associated with 'go' and action.",
    expected_impact="15% increase in CTR, ~$12K additional monthly revenue",
    impact=7,
    confidence=6,
    ease=9,
    framework=CROFramework.ICE,
    source="Heatmap analysis showing low CTA engagement",
)

print(f"ICE Score: {hypothesis.ice_score}")  # 7.33

# Prioritize all hypotheses
prioritized = agent.prioritize_hypotheses(framework=CROFramework.ICE)
for i, h in enumerate(prioritized, 1):
    print(f"{i}. {h.title} (ICE: {h.ice_score:.1f})")
```

**Hypothesis Statement Format:**
```
IF we [make change X],
THEN [metric Y] will [increase/decrease] by [expected amount],
BECAUSE [reason/insight from data].
```

**Prioritization Frameworks:**

| Framework | Formula | Best For |
|-----------|---------|----------|
| ICE | (Impact + Confidence + Ease) / 3 | Quick prioritization |
| RICE | (Impact × Reach × Confidence) / Effort | Resource planning |
| PIE | (Potential + Importance + Ease) / 3 | Landing page tests |
| Impact/Effort | Impact / Effort | Visual prioritization |

### 2. A/B Test Management

Create, manage, and analyze A/B tests with full statistical rigor.

```python
# Create A/B test
test = agent.create_ab_test(
    name="Hero CTA Button Color Test",
    url="/pricing",
    variants=[
        ("Blue Control", True),    # is_control=True
        ("Green Variant", False),  # is_control=False
    ],
    target_metric=ConversionMetric.CLICK_THROUGH_RATE,
    priority=TestPriority.P1_HIGH,
    hypothesis_id=hypothesis.hypothesis_id,
)

# Approve and start
agent.approve_test(test.test_id)
agent.start_test(test.test_id)

# Analyze results (with statistical testing)
results = agent.analyze_test_results(test.test_id)
print(f"Winner: {results.winner}")
print(f"Lift: {results.lift:.2%}")
print(f"Significance: {results.significance.value}")
print(f"P-value: {results.p_value:.6f}")

# View test dashboard
dashboard = agent.get_test_dashboard()
print(f"Total tests: {dashboard['total_tests']}")
print(f"Winners: {dashboard['winners']}")
print(f"Average lift: {dashboard['average_lift']:.2%}")
```

**Test Types Supported:**
- A/B (two variants)
- A/B/N (multiple variants)
- Multivariate (multiple elements)
- Split URL (different pages)
- Multipage (full funnel)
- Bandit (dynamic allocation)

**Statistical Analysis:**
- Two-proportion Z-test
- P-value calculation
- Confidence intervals
- Minimum sample size
- Statistical significance levels

### 3. Conversion Funnel Analysis

Analyze conversion funnels with step-by-step drop-off analysis.

```python
# Analyze funnel
funnel = agent.analyze_funnel(
    name="SaaS Signup Funnel",
    steps=[
        {"name": "Homepage", "stage": "awareness", "visitors": 10000, "conversions": 8500},
        {"name": "Pricing Page", "stage": "consideration", "visitors": 8500, "conversions": 4200},
        {"name": "Signup Form", "stage": "intent", "visitors": 4200, "conversions": 2100},
        {"name": "Email Verification", "stage": "evaluation", "visitors": 2100, "conversions": 1800},
        {"name": "Onboarding Complete", "stage": "activation", "visitors": 1800, "conversions": 1200},
    ],
    time_period_days=30,
)

print(f"Overall conversion: {funnel.overall_conversion_rate:.2%}")
print(f"Biggest drop-off: {funnel.biggest_drop_off}")

# Compare two funnels
comparison = agent.compare_funnels(funnel_id_1, funnel_id_2)
print(f"Conversion rate diff: {comparison['conversion_rate_diff']:.2%}")
```

**Analysis Types:**
- Drop-off analysis
- Cohort analysis
- Segment comparison
- Path analysis
- Time series
- Attribution

### 4. UX Analysis

Comprehensive UX analysis with issue identification and scoring.

```python
# Analyze UX
ux_report = agent.analyze_ux(
    page_url="/pricing",
    page_type="pricing",
)

print(f"UX Score: {ux_report.overall_score:.1f}")
print(f"Issues: {len(ux_report.issues)}")
print(f"Accessibility: {ux_report.accessibility_score:.1f}")
print(f"Mobile: {ux_report.mobile_score:.1f}")

# Review conversion barriers
for barrier in ux_report.conversion_barriers:
    print(f"Barrier: {barrier}")

# Review opportunities
for opp in ux_report.opportunities:
    print(f"Opportunity: {opp['description']} ({opp['estimated_impact']})")
```

**Analysis Dimensions:**
- Accessibility (WCAG compliance)
- Mobile experience
- Page speed (Core Web Vitals)
- Readability
- Conversion barriers
- Optimization opportunities

### 5. Landing Page Audit

Element-by-element analysis of landing pages.

```python
# Audit landing page
audit = agent.audit_landing_page(
    url="/pricing",
    page_type="pricing",
)

print(f"Overall Score: {audit.overall_score:.1f}")
print(f"Elements analyzed: {len(audit.elements)}")

# Review element scores
for element in audit.elements:
    print(f"  {element.element_type.value}: {element.score:.1f}")

# Review quick wins
for qw in audit.quick_wins:
    print(f"Quick win: {qw}")

# Review test roadmap
for phase in audit.ab_test_roadmap:
    print(f"Phase {phase['phase']} ({phase['duration']}): {phase['tests']}")
```

**Elements Analyzed:**
- Hero section
- Headline
- Call-to-action
- Social proof
- Trust signals
- Benefits
- Features
- Form
- Pricing
- FAQ

### 6. CRO Strategy Development

Create comprehensive CRO strategies with roadmaps.

```python
# Create CRO strategy
strategy = agent.create_cro_strategy(
    name="Q3 Conversion Optimization",
    framework=CROFramework.ICE,
    budget=50000.0,
    timeline_months=3,
    kpis=[
        {"name": "Conversion Rate", "target": 0.05, "current": 0.03},
        {"name": "Revenue per Visitor", "target": 5.0, "current": 3.2},
    ],
)

# Add hypotheses to strategy
agent.add_hypothesis_to_strategy(strategy.strategy_id, hypothesis.hypothesis_id)

# Prioritize
strategy.prioritize_hypotheses()
```

### 7. Form & Checkout Analysis

Analyze form completion and checkout abandonment.

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
        {"name": "Cart Review", "visitors": 5000, "conversions": 4200},
        {"name": "Account Creation", "visitors": 4200, "conversions": 3800},
        {"name": "Shipping Info", "visitors": 3800, "conversions": 3200},
        {"name": "Payment", "visitors": 3200, "conversions": 2800},
        {"name": "Confirmation", "visitors": 2800, "conversions": 2600},
    ],
)
print(f"Completion rate: {checkout.overall_completion_rate:.2%}")
```

### 8. CRO Recommendations

Get prioritized recommendations based on page type.

```python
recs = agent.get_cro_recommendations(page_type="landing_page")
for rec in recs:
    print(f"[{rec['priority']}] {rec['category']}: {rec['recommendation']}")
```

---

## Operational Guidelines

### A/B Testing Best Practices

1. **One test at a time per page** — avoid overlapping tests
2. **Minimum 7 days runtime** — capture weekly patterns
3. **95% confidence level** — standard significance threshold
4. **100+ conversions per variant** — minimum for reliable results
5. **Document everything** — hypothesis, setup, results, learnings

### Statistical Significance Rules

| P-Value | Significance | Action |
|---------|--------------|--------|
| p < 0.01 | Very High | Implement with confidence |
| p < 0.05 | High | Implement |
| p < 0.10 | Moderate | Consider implementing, run follow-up |
| p < 0.20 | Low | inconclusive, gather more data |
| p >= 0.20 | None | No significant difference |

### Funnel Analysis Tips

1. **5-7 steps maximum** — too many steps dilute insights
2. **Consistent naming** — use clear, consistent step names
3. **Segment by source** — different sources have different behaviors
4. **Compare periods** — month-over-month, year-over-year
5. **Focus on biggest drop-off** — highest impact optimization

### Landing Page Audit Process

1. **Above-fold first** — headline, CTA, social proof
2. **Element-by-element** — systematic analysis
3. **Mobile check** — responsive design and tap targets
4. **Page speed** — Core Web Vitals
5. **Accessibility** — WCAG compliance

---

## Method Signatures

### Hypothesis Methods

```python
def create_hypothesis(
    self,
    title: str,
    observation: str,
    insight: str,
    hypothesis_statement: str,
    expected_impact: str = "",
    impact: int = 5,
    confidence: int = 5,
    ease: int = 5,
    framework: CROFramework = CROFramework.ICE,
    source: str = "",
) -> Hypothesis

def update_hypothesis(self, hypothesis_id: str, **kwargs: Any) -> Hypothesis
def get_hypothesis(self, hypothesis_id: str) -> Hypothesis
def list_hypotheses(self, status: Optional[str] = None) -> List[Hypothesis]
def prioritize_hypotheses(self, framework: CROFramework = CROFramework.ICE) -> List[Hypothesis]
```

### A/B Test Methods

```python
def create_ab_test(
    self,
    name: str,
    url: str,
    variants: List[Tuple[str, bool]],
    test_type: TestType = TestType.A_B,
    target_metric: ConversionMetric = ConversionMetric.CONVERSION_RATE,
    priority: TestPriority = TestPriority.P2_MEDIUM,
    hypothesis_id: Optional[str] = None,
    description: str = "",
) -> ABTest

def update_ab_test(self, test_id: str, **kwargs: Any) -> ABTest
def approve_test(self, test_id: str) -> ABTest
def start_test(self, test_id: str) -> ABTest
def stop_test(self, test_id: str, winner_id: Optional[str] = None) -> ABTest
def analyze_test_results(self, test_id: str, sample_data: Optional[Dict] = None) -> ExperimentResult
def get_test(self, test_id: str) -> ABTest
def list_tests(self, status: Optional[TestStatus] = None) -> List[ABTest]
def get_test_dashboard(self) -> Dict[str, Any]
```

### Funnel Methods

```python
def analyze_funnel(
    self,
    name: str,
    steps: List[Dict[str, Any]],
    time_period_days: int = 30,
    segment: Optional[UserSegment] = None,
    source: Optional[TrafficSource] = None,
) -> FunnelAnalysis

def compare_funnels(self, funnel_id_1: str, funnel_id_2: str) -> Dict[str, Any]
def get_funnel(self, analysis_id: str) -> FunnelAnalysis
def list_funnels(self) -> List[FunnelAnalysis]
```

### UX Methods

```python
def analyze_ux(self, page_url: str, page_type: str = "landing_page") -> UXReport
def get_ux_report(self, report_id: str) -> UXReport
def list_ux_reports(self) -> List[UXReport]
```

### Landing Page Methods

```python
def audit_landing_page(self, url: str, page_type: str = "landing_page") -> LandingPageAudit
def get_landing_page_audit(self, audit_id: str) -> LandingPageAudit
def list_landing_page_audits(self) -> List[LandingPageAudit]
```

### Strategy Methods

```python
def create_cro_strategy(
    self,
    name: str,
    framework: CROFramework = CROFramework.ICE,
    budget: float = 0.0,
    timeline_months: int = 3,
    kpis: Optional[List[Dict[str, Any]]] = None,
) -> CROStrategy

def add_hypothesis_to_strategy(self, strategy_id: str, hypothesis_id: str) -> CROStrategy
def get_cro_strategy(self, strategy_id: str) -> CROStrategy
def list_cro_strategies(self) -> List[CROStrategy]
```

### Form & Checkout Methods

```python
def analyze_form(
    self,
    form_name: str,
    page_url: str,
    total_submissions: int,
    successful_submissions: int,
    field_data: Optional[List[Dict[str, Any]]] = None,
) -> FormAnalytics

def analyze_checkout(
    self,
    steps: List[Dict[str, Any]],
    abandonment_reasons: Optional[List[Dict[str, Any]]] = None,
) -> CheckoutAnalysis
```

### Recommendations & Status

```python
def get_cro_recommendations(self, page_type: str = "landing_page") -> List[Dict[str, Any]]
def get_status(self) -> Dict[str, Any]
def get_operation_log(self, limit: int = 50) -> List[Dict[str, Any]]
def clear_cache(self) -> int
def export_data(self, format: str = "json") -> str
```

---

## Usage Patterns

### Pattern 1: Full CRO Workflow

```python
agent = ConversionOptimizationAgent()

# 1. Create hypothesis
hypothesis = agent.create_hypothesis(
    title="Social Proof Above Fold",
    observation="Landing page has social proof below fold",
    insight="Social proof near CTA increases conversion by 15-20%",
    hypothesis_statement="IF we add customer logos above the fold, THEN conversion rate will increase by 15%, BECAUSE social proof reduces purchase anxiety.",
    impact=8, confidence=7, ease=7,
)

# 2. Create A/B test
test = agent.create_ab_test(
    name="Social Proof Above Fold Test",
    url="/",
    variants=[("Below Fold Control", True), ("Above Fold Variant", False)],
    hypothesis_id=hypothesis.hypothesis_id,
)

# 3. Run test
agent.approve_test(test.test_id)
agent.start_test(test.test_id)

# 4. Analyze
results = agent.analyze_test_results(test.test_id)
if results.significance in [StatisticalSignificance.HIGH, StatisticalSignificance.VERY_HIGH]:
    print(f"Implement winner! Lift: {results.lift:.2%}")
```

### Pattern 2: Funnel Optimization

```python
# Analyze funnel
funnel = agent.analyze_funnel(
    name="E-commerce Checkout",
    steps=[
        {"name": "Cart", "visitors": 10000, "conversions": 8000},
        {"name": "Checkout", "visitors": 8000, "conversions": 5000},
        {"name": "Payment", "visitors": 5000, "conversions": 4000},
        {"name": "Confirmation", "visitors": 4000, "conversions": 3800},
    ],
)

# Identify biggest drop-off
biggest = funnel.find_biggest_drop_off()
print(f"Focus on: {biggest.name} ({biggest.drop_off_rate:.1%} drop-off)")

# Get recommendations
recs = agent.get_cro_recommendations(page_type="checkout")
```

### Pattern 3: Landing Page Optimization

```python
# Audit page
audit = agent.audit_landing_page(url="/pricing", page_type="pricing")

# Quick wins first
for qw in audit.quick_wins:
    print(f"Quick win: {qw}")

# Build test roadmap
for phase in audit.ab_test_roadmap:
    print(f"Phase {phase['phase']}: {phase['tests']}")
```

### Pattern 4: CRO Strategy Development

```python
# Create strategy
strategy = agent.create_cro_strategy(
    name="2026 CRO Strategy",
    budget=100000,
    timeline_months=12,
)

# Add hypotheses
for h in hypotheses:
    agent.add_hypothesis_to_strategy(strategy.strategy_id, h.hypothesis_id)

# Prioritize
strategy.prioritize_hypotheses()
```

---

## Data Models

### ABTest

| Field | Type | Description |
|-------|------|-------------|
| test_id | str | Unique 12-char ID |
| name | str | Test name |
| test_type | TestType | A/B, A/B/N, Multivariate, etc. |
| status | TestStatus | Draft, Approved, Running, etc. |
| variants | List[Variant] | Test variants |
| target_metric | ConversionMetric | Primary metric |
| results | ExperimentResult | Statistical results |

### ExperimentResult

| Field | Type | Description |
|-------|------|-------------|
| p_value | float | Statistical p-value |
| confidence_level | float | Confidence level |
| winner | Optional[str] | Winning variant ID |
| lift | float | Percentage lift |
| significance | StatisticalSignificance | Significance level |
| variant_results | List[Dict] | Per-variant metrics |

### FunnelAnalysis

| Field | Type | Description |
|-------|------|-------------|
| steps | List[FunnelStep] | Funnel steps |
| overall_conversion_rate | float | End-to-end conversion |
| biggest_drop_off | Optional[str] | Step with highest drop-off |
| insights | List[Dict] | Analysis insights |
| recommendations | List[str] | Optimization actions |

### UXReport

| Field | Type | Description |
|-------|------|-------------|
| overall_score | float | UX score 0-100 |
| issues | List[UXIssue] | Identified issues |
| conversion_barriers | List[str] | Barriers to conversion |
| opportunities | List[Dict] | Optimization opportunities |

### LandingPageAudit

| Field | Type | Description |
|-------|------|-------------|
| elements | List[ElementAnalysis] | Element-by-element scores |
| quick_wins | List[str] | Immediate improvements |
| ab_test_roadmap | List[Dict] | Phased test plan |
| top_recommendations | List[str] | Priority recommendations |

---

## Checklists

### A/B Test Checklist

- [ ] Clear hypothesis documented
- [ ] Primary metric defined
- [ ] Sample size calculated
- [ ] Test duration planned (7+ days)
- [ ] Variants created with control
- [ ] Traffic allocation set
- [ ] QA testing completed
- [ ] Tracking verified
- [ ] Stakeholders informed
- [ ] Results analysis plan defined

### Funnel Analysis Checklist

- [ ] Steps clearly defined
- [ ] Visitor/conversion data accurate
- [ ] Time period specified
- [ ] Segments identified
- [ ] Drop-off rates calculated
- [ ] Biggest bottleneck identified
- [ ] Benchmarks compared
- [ ] Recommendations documented
- [ ] Action items assigned

### Landing Page Audit Checklist

- [ ] Hero section reviewed
- [ ] Headline analyzed
- [ ] CTA evaluated
- [ ] Social proof assessed
- [ ] Trust signals checked
- [ ] Benefits/features reviewed
- [ ] Form analyzed
- [ ] Mobile experience checked
- [ ] Page speed tested
- [ ] Accessibility verified

### CRO Strategy Checklist

- [ ] KPIs defined
- [ ] Hypotheses created
- [ ] Framework selected (ICE/RICE)
- [ ] Hypotheses prioritized
- [ ] Budget allocated
- [ ] Timeline defined
- [ ] Team roles assigned
- [ ] Quick wins identified
- [ ] Test roadmap created

---

## Troubleshooting

### Problem: Test shows no statistical significance

**Symptoms:** `results.significance == StatisticalSignificance.NONE`

**Diagnosis:**
```python
print(f"P-value: {results.p_value}")
print(f"Sample size reached: {results.sample_size_reached}")
print(f"Minimum runtime reached: {results.minimum_runtime_reached}")
```

**Common Fixes:**
1. Increase sample size (run test longer)
2. Increase minimum detectable effect
3. Check for tracking issues
4. Verify variant implementation

### Problem: Funnel shows unexpected drop-off

**Symptoms:** One step has >50% drop-off

**Diagnosis:**
```python
for step in funnel.steps:
    print(f"{step.name}: {step.visitors} visitors, {step.drop_off_rate:.1%} drop-off")
```

**Common Fixes:**
1. Check for technical errors on that step
2. Review UX issues on that page
3. Check for tracking gaps
4. Analyze by segment (source, device)

### Problem: Landing page audit score is low

**Symptoms:** `audit.overall_score < 50`

**Diagnosis:**
```python
for element in audit.elements:
    print(f"{element.element_type.value}: {element.score}")
    for weakness in element.weaknesses:
        print(f"  - {weakness}")
```

**Common Fixes:**
1. Start with quick wins
2. Focus on above-fold elements first
3. Address high-severity issues first
4. Implement A/B tests for major changes

### Problem: Form completion rate is low

**Symptoms:** `form.completion_rate < 0.50`

**Diagnosis:**
```python
print(f"Completion rate: {form.completion_rate:.2%}")
print(f"Abandonment fields: {form.abandonment_fields}")
print(f"Insights: {form.insights}")
```

**Common Fixes:**
1. Reduce form fields to essentials
2. Add inline validation
3. Simplify error messages
4. Add progress indicator
5. Offer social login

---

*Conversion Optimization Agent v3.0.0 — Part of the Awesome Grok Skills collection.*
*Last updated: 2026-07-06*
