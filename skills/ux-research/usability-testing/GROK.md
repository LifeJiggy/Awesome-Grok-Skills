---
name: "usability-testing"
category: "ux-research"
version: "1.0.0"
tags: ["ux-research", "usability-testing", "SUS", "task-analysis", "A-B-testing"]
---

# Usability Testing Toolkit

## Overview

Usability testing is the empirical backbone of user-centered design—systematically observing real users attempting real tasks to identify where interfaces fail. This module provides a comprehensive toolkit for planning, executing, analyzing, and reporting on usability studies across moderated, unmoderated, remote, and in-person methodologies. It covers the full measurement spectrum: task success rates, time-on-task, error rates, satisfaction scores (SUS, NPS, UMUX-Lite), think-aloud protocol analysis, clickstream and heatmap interpretation, A/B test design and statistical analysis, funnel conversion analysis, rage click detection, and severity rating frameworks.

The toolkit bridges raw usability data into actionable severity-ranked findings. It handles both quantitative metrics (completion rates, binary success/failure, time distributions) and qualitative insights (think-aloud transcripts, observer notes, satisfaction free-text). Severity ratings follow established frameworks (Nielsen's severity scale adapted for modern contexts) and link findings directly to design recommendations with confidence levels and effort estimates.

Built for UX researchers and product teams running continuous usability validation—from formative studies during early design through summative benchmark studies against competitor baselines—this module automates the tedious statistical work (confidence intervals, significance testing, effect sizes) while preserving researcher judgment for interpretive synthesis. All outputs are structured for both research-readers (detailed methodology) and stakeholder-readers (executive summary with priority actions).

## Core Capabilities

- **Task Success Rate Measurement**: Binary, dichotomous, and composite success scoring with confidence interval calculation, time-on-task distributions, and error rate tracking per task
- **SUS/NPS Scoring**: System Usability Scale administration, calculation, and benchmarking against industry percentiles; Net Promoter Score with segment analysis
- **Think-Aloud Protocol Analysis**: Structured coding of think-aloud transcripts using affinity diagramming, critical incident extraction, and coded behavioral taxonomy
- **Heatmap and Clickstream Analysis**: Aggregated click density interpretation, scroll depth analysis, navigation path identification, and dead-click/zero-click zone detection
- **A/B Test Design**: Sample size calculation, randomization validation, multi-variant test planning, and statistical significance evaluation with Bayes and frequentist approaches
- **Funnel Conversion Analysis**: Step-by-step funnel metrics, drop-off calculation, statistical comparison across funnel variants, and cohort-based funnel analysis
- **Rage Click Detection**: Automated identification of frustration patterns—rapid repeated clicks, dead-clicks, scroll-rage, and form abandonment signals
- **Severity Rating Framework**: Multi-factor severity scoring combining frequency × impact × persistence, mapped to prioritized design recommendations

## Usage Examples

### Measuring Task Success Rates

```python
from usability_testing import TaskSuccessStudy, SuccessMetric

study = TaskSuccessStudy(name="Checkout Flow v2 Benchmark")

study.add_task(
    task_id="T1",
    description="Complete a purchase as a guest user",
    steps=["Add item to cart", "Proceed to checkout", "Fill shipping info", "Submit order"],
    time_limit_seconds=300,
    metric=SuccessMetric.COMPOSITE
)

study.add_task(
    task_id="T2",
    description="Find and apply a discount code",
    steps=["Locate promo field", "Enter code", "Verify discount applied"],
    time_limit_seconds=120,
    metric=SuccessMetric.BINARY
)

# Record participant results
study.record_result(participant_id="P01", task_id="T1",
                    success=True, time_seconds=145, errors=0,
                    think_aloud_notes="Participant hesitated at shipping form")
study.record_result(participant_id="P01", task_id="T2",
                    success=True, time_seconds=42, errors=1,
                    think_aloud_notes="Initially looked in wrong section")

report = study.generate_report()
print(report)
# Output includes: success rates, 95% CIs, time distributions, error summaries
```

### SUS Score Analysis

```python
from usability_testing import SUSSurvey

sus = SUSSurvey(name="Post-Task SUS")

# 10 standard SUS questions (1-5 Likert)
sus.add_response("P01", [5, 4, 5, 3, 5, 2, 4, 5, 4, 5])
sus.add_response("P02", [4, 3, 4, 4, 4, 3, 3, 4, 3, 4])
sus.add_response("P03", [5, 5, 5, 4, 5, 3, 5, 5, 4, 5])

results = sus.analyze()
# results = {
#     "mean_sus_score": 78.3,
#     "percentile_rank": 72,
#     "adjective_rating": "Good",
#     "individual_scores": [...],
#     "confidence_interval": (71.2, 85.4)
# }
```

### Rage Click Detection

```python
from usability_testing import RageClickDetector, ClickEvent

detector = RageClickDetector(
    time_window_ms=1000,
    min_clicks=3,
    max_distance_px=50,
    dead_click_threshold_ms=500
)

# Ingest clickstream data
events = [
    ClickEvent(x=450, y=300, timestamp=1000, element_id="btn-submit", response_ms=200),
    ClickEvent(x=455, y=305, timestamp=1150, element_id="btn-submit", response_ms=None),
    ClickEvent(x=448, y=298, timestamp=1250, element_id="btn-submit", response_ms=None),
    ClickEvent(x=452, y=302, timestamp=1320, element_id="btn-submit", response_ms=None),
    ClickEvent(x=900, y=500, timestamp=5000, element_id="empty-div", response_ms=None),
    ClickEvent(x=910, y=510, timestamp=5050, element_id="empty-div", response_ms=None),
    ClickEvent(x=895, y=498, timestamp=5100, element_id="empty-div", response_ms=None),
]

rage_events = detector.detect(events)
# Finds rage click cluster on "btn-submit" and dead-click on "empty-div"
```

### A/B Test Statistical Analysis

```python
from usability_testing import ABTest

test = ABTest(
    name="New Checkout Button Color",
    primary_metric="conversion_rate",
    minimum_detectable_effect=0.05,
    power=0.8,
    significance_level=0.05
)

sample_size = test.calculate_sample_size(baseline_rate=0.12)
print(f"Required per variant: {sample_size}")

test.add_variant("control", conversions=150, visitors=1200)
test.add_variant("treatment", conversions=185, visitors=1200)

result = test.analyze()
# result = {
#     "control_rate": 0.125,
#     "treatment_rate": 0.154,
#     "lift": 0.029,
#     "p_value": 0.034,
#     "significant": True,
#     "winner": "treatment",
#     "confidence_interval": (0.003, 0.055)
# }
```

### Funnel Conversion Analysis

```python
from usability_testing import FunnelAnalyzer, FunnelStep

funnel = FunnelAnalyzer(name="E-commerce Checkout Funnel")
funnel.add_step(FunnelStep("Landing", users=10000))
funnel.add_step(FunnelStep("Product View", users=7200))
funnel.add_step(FunnelStep("Add to Cart", users=3500))
funnel.add_step(FunnelStep("Checkout Start", users=2100))
funnel.add_step(FunnelStep("Payment", users=1600))
funnel.add_step(FunnelStep("Order Complete", users=1400))

analysis = funnel.analyze()
print(f"Overall conversion: {analysis['overall_rate']:.1%}")
for step in analysis['steps']:
    print(f"  {step['name']}: {step['rate']:.1%} (drop-off: {step['drop_off']:.1%})")
```

### Severity Rating Framework

```python
from usability_testing import SeverityRating, SeverityFactor

finding = SeverityRating(
    issue="Users cannot find the password reset link",
    frequency=SeverityFactor.HIGH,     # 60%+ of users encountered this
    impact=SeverityFactor.CRITICAL,     # Complete task failure
    persistence=SeverityFactor.HIGH,    # Occurs every session
)
score = finding.calculate()
print(f"Severity score: {score}/100")
print(f"Priority: {finding.priority_label()}")
print(f"Recommendation: {finding.recommendation()}")
```

## Best Practices

1. **Plan before you test**: Define clear success criteria for each task before running the study. Pre-register your hypotheses and sample size rationale. Post-hoc rationalization erodes credibility and invites skepticism from stakeholders.

2. **Separate formative from summative**: Formative studies (during design) are exploratory and small-n (5-8 participants). Summative studies (after design) are statistical and require larger samples. Don't mix methodologies—a think-aloud protocol contaminates a benchmark metric.

3. **Use the severity framework consistently**: Apply the same severity rating rubric to every finding. Frequency × Impact × Persistence prevents the loudest stakeholder from overriding the most critical finding. Track severity across studies to spot regressions.

4. **Report confidence intervals, not just means**: A task success rate of 78% with a 95% CI of [65%, 88%] tells a very different story than [75%, 81%]. Small samples produce wide intervals—acknowledge uncertainty rather than hiding it behind averages.

5. **Distinguish frustration from confusion**: Rage clicks indicate frustration (user knows what they want but the interface blocks them). Long pauses indicate confusion (user doesn't know what to do). The interventions are different—remove friction vs. add guidance.

6. **Test with representative users**: Recruiting convenience participants (colleagues, friends) produces biased findings. Screen for task-relevant experience, not just demographics. A usability finding from the wrong user population is worse than no finding.

7. **Triangulate metrics**: Task success tells you if users can complete the task. Time-on-task tells you if they can do it efficiently. SUS tells you how they feel about the experience. All three together give a complete picture; any one alone is misleading.

8. **Close the loop**: Every study should produce a prioritized action list with owners and deadlines. Findings that don't become actions are expensive academic exercises. Track which findings were implemented and whether they improved metrics in the next round.

## Related Modules

- [user-research](../user-research/GROK.md) — Pre-test recruitment, persona validation, and think-aloud script design
- [information-architecture](../information-architecture/GROK.md) — Findability metrics and card sort inputs for IA-related usability issues
- [interaction-design](../interaction-design/GROK.md) — Micro-interaction and animation patterns that reduce usability friction
- [accessibility](../accessibility/GROK.md) — Accessibility-specific usability testing with assistive technologies
