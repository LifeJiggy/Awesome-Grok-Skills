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

---

## Advanced Configuration

### Custom Severity Matrix

```python
from usability_testing import SeverityMatrix

matrix = SeverityMatrix(
    frequency_weights={"low": 1, "medium": 2, "high": 3},
    impact_weights={"minor": 1, "moderate": 2, "major": 3, "critical": 4},
    persistence_weights={"once": 1, "sometimes": 2, "always": 3},
)
score = matrix.calculate(frequency="high", impact="critical", persistence="always")
# score = 3 * 4 * 3 = 36 / max_possible * 100
```

### A/B Test Power Analysis

```python
from usability_testing import PowerAnalysis

analysis = PowerAnalysis(
    baseline_rate=0.12,
    minimum_detectable_effect=0.03,
    alpha=0.05,
    power=0.8,
)
sample = analysis.calculate_per_variant()
print(f"Required: {sample} per variant")
```

## Architecture Patterns

### Usability Study Workflow

```
Study Design
    │
    ▼
┌──────────────┐
│ Recruitment  │── Screener, scheduling, incentives
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Moderation   │── Think-aloud, task observation
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Data Capture │── Screen recording, clickstream, notes
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Analysis     │── Task metrics, behavioral coding, SUS
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Reporting    │── Severity ranking, recommendations
└──────────────┘
```

## Integration Guide

### Clickstream Analytics

```python
from usability_testing import ClickstreamAnalyzer

analyzer = ClickstreamAnalyzer()
analyzer.import_hotjar("session_recording.json")
analyzer.import_microsoft_clarity("clarity_export.csv")
heatmap = analyzer.generate_heatmap(page="/checkout")
```

### SUS Benchmarking

```python
from usability_testing import SUSBenchmark

benchmark = SUSBenchmark(industry="saas")
result = benchmark.compare(my_sus_score=72.5)
print(f"Percentile: {result.percentile_rank}")
print(f"Comparison: {result.industry_comparison}")
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Automated task success detection | 50% faster analysis |
| Clickstream clustering | Auto-detect rage click patterns |
| SUS score calculation | Instant scoring from raw responses |
| Funnel visualization | Real-time conversion tracking |

## Security Considerations

- **Participant data protection**: Encrypt screen recordings and session data
- **PII redaction**: Auto-redact personal information from recordings
- **Consent management**: Digital consent forms with clear usage terms
- **Data retention**: Auto-delete recordings after analysis period
- **Secure sharing**: Password-protected report links

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Low task completion | Task instructions unclear | Simplify task scenarios |
| High SUS variance | Mixed participant expertise | Screen for task-relevant experience |
| Rage click false positives | Click threshold too low | Increase min clicks to 4 |
| A/B test inconclusive | Sample size too small | Run longer or increase traffic allocation |
| Funnel drop-off spike | Step definition wrong | Verify funnel step boundaries |

## API Reference

### TaskSuccessStudy

```python
class TaskSuccessStudy:
    def __init__(self, name: str)
    def add_task(self, task_id: str, description: str, steps: list, time_limit_seconds: int, metric: SuccessMetric) -> None
    def record_result(self, participant_id: str, task_id: str, success: bool, time_seconds: float, errors: int, think_aloud_notes: str) -> None
    def generate_report(self) -> UsabilityReport
```

### ABTest

```python
class ABTest:
    def __init__(self, name: str, primary_metric: str, minimum_detectable_effect: float, power: float, significance_level: float)
    def calculate_sample_size(self, baseline_rate: float) -> int
    def add_variant(self, name: str, conversions: int, visitors: int) -> None
    def analyze(self) -> ABTestResult
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class SuccessMetric(Enum):
    BINARY = "binary"
    DICHOTOMOUS = "dichotomous"
    COMPOSITE = "composite"

@dataclass
class TaskResult:
    participant_id: str
    task_id: str
    success: bool
    time_seconds: float
    errors: int
    think_aloud_notes: str

@dataclass
class SUSResult:
    mean_sus_score: float
    percentile_rank: int
    adjective_rating: str
    confidence_interval: tuple
```

## Deployment Guide

### Installation

```bash
pip install usability-testing
```

### Study Setup

1. Define tasks and success criteria
2. Create participant screener
3. Configure recording tools (Lookback, UserTesting)
4. Set up clickstream tracking
5. Prepare moderation guide
6. Schedule sessions

## Monitoring & Observability

```python
from usability_testing import MetricsCollector

collector = MetricsCollector()
collector.gauge("usability.task.success_rate", rate, tags={"task_id": tid})
collector.histogram("usability.task.time_seconds", time)
collector.counter("usability.rage_clicks", count, tags={"page": page})
collector.gauge("usability.sus.score", score)
```

## Testing Strategy

```python
import pytest
from usability_testing import TaskSuccessStudy, SuccessMetric

def test_task_success_rate():
    study = TaskSuccessStudy(name="Test Study")
    study.add_task("T1", "Complete checkout", ["Step 1"], 300, SuccessMetric.BINARY)
    study.record_result("P01", "T1", success=True, time_seconds=120, errors=0, think_aloud_notes="")
    report = study.generate_report()
    assert report.task_success_rate("T1") == 1.0
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added rage click detection | Enable clickstream tracking |
| 2.0.0 | New severity framework | Re-rate existing findings |

## Glossary

| Term | Definition |
|------|-----------|
| **SUS** | System Usability Scale — 10-question standard survey |
| **Think-Aloud** | Verbal protocol where users narrate their actions |
| **NPS** | Net Promoter Score — likelihood to recommend |
| **Rage Click** | Rapid repeated clicks indicating frustration |
| **Task Success** | Whether the user completed the intended task |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with task success measurement
- SUS/NPS scoring and benchmarking
- A/B test design and analysis
- Severity rating framework

## Contributing Guidelines

```bash
git clone https://github.com/example/usability-testing.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Task Success Metrics Reference

| Metric | Calculation | Range | Use Case |
|--------|------------|-------|----------|
| Binary success | 1 if completed, 0 if not | 0-1 | Simple tasks |
| Composite success | Weighted combination | 0-1 | Complex tasks |
| Time-on-task | Seconds to complete | 0-∞ | Efficiency |
| Error count | Number of errors | 0-∞ | Accuracy |
| Recovery rate | Recovered errors / total errors | 0-1 | Resilience |
| Help usage | Used help / total attempts | 0-1 | Learnability |

### SUS Score Interpretation

| Score Range | Adjective | Percentile | Grade |
|------------|-----------|-----------|-------|
| 80-100 | Best imaginable | 90+ | A |
| 70-79 | Good | 70-89 | B |
| 50-69 | OK | 40-69 | C |
| 30-49 | Poor | 15-39 | D |
| 0-29 | Worst imaginable | <15 | F |

### Common Usability Issues by Severity

| Severity | Issue Type | Example | Impact |
|----------|-----------|---------|--------|
| Critical | Blocker | Can't complete checkout | Task failure |
| Major | Significant friction | Confusing navigation | High error rate |
| Minor | Annoyance | Inconsistent button labels | Low efficiency |
| Cosmetic | Visual | Misaligned elements | Low satisfaction |

### A/B Test Decision Framework

```
Result is statistically significant?
├── YES → Is the effect size meaningful?
│   ├── YES → Implement the winning variant
│   └── NO → Consider cost vs. benefit
└── NO → Is the sample size sufficient?
    ├── YES → Result is inconclusive, move on
    └── NO → Continue test until sufficient sample
```

### Think-Aloud Coding Taxonomy

| Code | Category | Description |
|------|----------|-------------|
| confusion | Cognitive | User doesn't understand |
| error | Behavioral | User makes a mistake |
| frustration | Emotional | User expresses frustration |
| success | Behavioral | User completes task |
| discovery | Cognitive | User finds new information |
| expectation | Cognitive | User's mental model differs |
| workaround | Behavioral | User finds alternative path |

### Clickstream Analysis Reference

| Pattern | Meaning | Action |
|---------|---------|--------|
| Rage click | Frustration with non-responsive element | Fix element or add feedback |
| Dead click | Clicking non-interactive element | Make element interactive or remove |
| U-turn | Navigating back immediately | Confusing navigation, fix IA |
| Loop | Repeating same sequence | User stuck, add guidance |
| Quick exit | Very short session | Content doesn't match expectation |

### Usability Report Template

```markdown
# Usability Test Report

## Study Overview
- Date: [Date]
- Participants: [Number]
- Method: [Moderated/Unmoderated]
- Tasks tested: [Number]

## Key Findings
1. [Finding with evidence]
2. [Finding with evidence]
3. [Finding with evidence]

## Task Metrics
| Task | Success Rate | Avg Time | Errors |
|------|-------------|----------|--------|
| T1 | 85% | 45s | 0.3 |
| T2 | 70% | 90s | 1.2 |

## Severity Ratings
| Issue | Frequency | Impact | Severity |
|-------|-----------|--------|----------|
| Issue 1 | High | Critical | 8/10 |
| Issue 2 | Medium | Major | 5/10 |

## Recommendations
1. [Recommendation with rationale]
2. [Recommendation with rationale]

## Next Steps
- [Action item]
- [Action item]
```

### Complete Usability Metrics Reference

| Metric | Calculation | Target | Tool |
|--------|------------|--------|------|
| Task success rate | Successful / Total | > 80% | Observation |
| Time on task | Seconds from start to end | < 60s | Timer |
| Error rate | Errors / Total attempts | < 2 | Observation |
| Page views per task | Views / Task completion | < 3 | Analytics |
| Help usage | Help clicks / Total attempts | < 10% | Analytics |
| Satisfaction (CSAT) | Sum / Count | > 4.0/5.0 | Survey |
| SUS score | Standard calculation | > 70 | Survey |
| NPS | Promoters - Detractors | > 30 | Survey |

### Complete A/B Test Reference

| Parameter | Small Effect | Medium Effect | Large Effect |
|-----------|-------------|---------------|--------------|
| Conversion rate | 0.5% lift | 2% lift | 5%+ lift |
| Sample size needed | 10,000+ per variant | 2,500 per variant | 500 per variant |
| Test duration | 4+ weeks | 2-4 weeks | 1-2 weeks |
| Statistical power | 80% | 80% | 80% |

### Complete Funnel Analysis Reference

| Funnel Stage | Good Conversion | Average | Poor |
|-------------|----------------|---------|------|
| Visit → View | > 60% | 40-60% | < 40% |
| View → Add to Cart | > 30% | 15-30% | < 15% |
| Add to Cart → Checkout | > 70% | 50-70% | < 50% |
| Checkout → Purchase | > 80% | 60-80% | < 60% |
| Overall conversion | > 3% | 1-3% | < 1% |

### Complete Severity Rating Examples

| Issue | Frequency | Impact | Persistence | Score | Priority |
|-------|-----------|--------|-------------|-------|----------|
| Can't complete checkout | Universal | Critical | Always | 9/10 | P0 |
| Confusing navigation | Common | Major | Always | 7/10 | P1 |
| Slow page load | Occasional | Moderate | Sometimes | 4/10 | P2 |
| Misaligned button | Rare | Minor | Once | 1/10 | P3 |
| Inconsistent color | Universal | Minor | Always | 3/10 | P2 |

### Remote Usability Testing Setup Guide

| Component | Tool Options | Key Consideration |
|-----------|-------------|-------------------|
| Screen recording | Lookback, UserTesting, Maze | Consent + auto-redact PII |
| Think-aloud | Video call + recording | Practice think-aloud beforehand |
| Clickstream | Hotjar, Clarity, FullStory | Respect privacy settings |
| Moderation | Zoom, Teams, Google Meet | Backup platform ready |
| Recruitment | UserTesting, Respondent.io | Screen for task-relevant experience |
| Incentive | Gift cards, product credit | $50-100/hour for B2B, $25-50 for B2C |
| Scheduling | Calendly, SavvyCal | Timezone-aware, buffer between sessions |
| Analysis | Dovetail, Condens, Dovetail | Tag in real-time during sessions |

### Usability Test Moderator Script Template

```markdown
# Moderator Guide: [Study Name]

## Pre-Session Checklist (5 min before)
- [ ] Recording software tested
- [ ] Screen share working
- [ ] Backup platform ready
- [ ] Participant info pulled up
- [ ] Consent form ready
- [ ] Notes template open

## Opening Script (3 min)
"Thank you for joining us today. My name is [Name], and I'm a 
researcher at [Company]. We're testing [product/feature], NOT you. 
There are no right or wrong answers—we want to learn from your 
experience.

This session will take about [X] minutes. I'll ask you to complete 
a few tasks while thinking aloud—just telling me what you're 
thinking as you go.

Do you have any questions before we begin?"

## Consent Script
"Before we start, I need your verbal consent to record this session. 
The recording will only be used by our research team and will not 
be shared publicly. Do you consent to being recorded?"

## Think-Aloud Prompt
- "What are you thinking right now?"
- "Tell me what you're looking for."
- "I noticed you paused—what went through your mind?"
- "Can you describe what you expected to happen?"

## Closing Script (3 min)
"Thank you so much for your time. Your feedback is incredibly 
valuable and will help us improve [product]. 
Do you have any final thoughts or questions?"

## Post-Session Notes
- Key observations:
- Notable quotes:
- Technical issues:
- Follow-up needed:
```

### Think-Aloud Analysis Framework

| Code Category | Code | Definition | Example |
|---------------|------|------------|---------|
| Cognitive | confusion | User doesn't understand | "I don't know what this means" |
| Cognitive | expectation | Mental model differs | "I expected it to be over here" |
| Cognitive | discovery | Found new information | "Oh, I didn't know that existed" |
| Cognitive | decision-making | Weighing options | "Should I click this or that?" |
| Behavioral | error | Made a mistake | Clicked wrong element |
| Behavioral | workaround | Found alternative path | Used search instead of nav |
| Behavioral | success | Completed task | Reached goal state |
| Behavioral | backtracking | Returned to previous step | Clicked back button |
| Emotional | frustration | Expresses frustration | "This is so annoying" |
| Emotional | satisfaction | Expresses delight | "That was easy!" |
| Emotional | confusion-emotional | Visibly confused | Long pause, sighing |
| Emotional | anxiety | Worried about outcome | "I hope this works" |

### Task Analysis Deep Dive

| Metric | Calculation | Interpretation | Action Threshold |
|--------|------------|----------------|------------------|
| Completion rate | Completed / Total attempted | Can users finish? | < 70% = investigate |
| Time on task | Median time to completion | Efficiency of path | 2x baseline = problematic |
| Error rate | Errors / Total attempts | Accuracy of interface | > 2 errors/task = redesign |
| Error recovery rate | Recovered / Total errors | Resilience of design | < 50% = add guidance |
| Help usage | Used help / Total attempts | Learnability burden | > 20% = improve labeling |
| Satisfaction | Post-task CSAT score | Emotional response | < 3.5/5 = friction present |
| Confidence | Post-task confidence | Perceived ease | Low confidence = trust issue |
| Path efficiency | Actual clicks / Minimum clicks | Navigation quality | > 2x minimum = inefficient |

### Remote Testing Technical Checklist

```
PRE-TEST TECHNICAL SETUP
    □ Test internet connection (upload/download speed)
    □ Verify screen sharing works
    □ Test recording software (audio + video)
    □ Confirm backup platform (Zoom backup link)
    □ Check participant can join from their device
    □ Verify consent form is accessible
    □ Test think-aloud prompts are visible
    □ Ensure notes template is open

DURING TEST
    □ Confirm participant can see screen
    □ Verify audio quality (no echo, clear voice)
    □ Monitor for lag or connection issues
    □ Keep backup platform ready to switch
    □ Take timestamped notes

POST-TEST
    □ Save recording immediately
    □ Export clickstream data
    □ Complete session notes within 1 hour
    □ Tag key moments in recording
    □ Send incentive within 24 hours
    □ Schedule debrief with team
```

### Usability Finding Prioritization Matrix

| Finding | Severity | Frequency | Fix Effort | Priority Score | Quarter |
|---------|----------|-----------|------------|----------------|---------|
| Can't complete checkout | Critical | 80% users | Medium | 9/10 | Q1 |
| Confusing nav labels | Major | 60% users | Low | 8/10 | Q1 |
| Slow page load | Moderate | 40% users | High | 5/10 | Q2 |
| Misaligned button | Minor | 20% users | Low | 3/10 | Q3 |
| Inconsistent spacing | Cosmetic | Universal | Low | 2/10 | Q3 |

### A/B Test Analysis Report Template

```markdown
# A/B Test Report: [Test Name]

## Hypothesis
If we [change], then [metric] will [improve/decrease] by [amount] 
because [rationale].

## Test Configuration
- Primary metric: [metric]
- Secondary metrics: [list]
- Minimum detectable effect: [%]
- Statistical power: [%]
- Significance level: [%]
- Duration: [days]

## Results Summary
| Variant | Visitors | Conversions | Rate | Lift | p-value |
|---------|----------|-------------|------|------|---------|
| Control | [N] | [N] | [%] | — | — |
| Treatment | [N] | [N] | [%] | [%] | [X] |

## Statistical Analysis
- Confidence interval: [X, Y]
- Effect size (Cohen's h): [X]
- Bayesian probability: [%]

## Decision
- [ ] Implement winning variant
- [ ] Continue test (insufficient data)
- [ ] No significant difference, ship original
- [ ] Test failed, investigate

## Next Steps
- [Action item 1]
- [Action item 2]
```
