---
name: "user-research"
category: "ux-research"
version: "1.0.0"
tags: ["ux-research", "user-research", "interviews", "surveys", "personas"]
---

# User Research Toolkit

## Overview

User research is the foundation of evidence-based product design. This module provides a comprehensive toolkit for conducting, analyzing, and synthesizing user research across multiple methodologies—from in-depth interviews and surveys to diary studies and card sorting. It enables researchers to move from raw qualitative and quantitative data to actionable personas, journey maps, and jobs-to-be-done frameworks that inform design decisions across product teams.

The toolkit supports the full research lifecycle: recruitment screener design, interview script creation with probing frameworks, survey methodology with statistical rigor, participant management, research repository organization, and multi-method synthesis. It handles both continuous discovery practices (weekly interview cadences, rolling diary studies) and discrete research sprints (generative explorations, evaluative usability rounds, concept testing).

Built for practitioners who need to produce defensible research artifacts at speed, the module enforces methodological best practices—triangulation across methods, saturation tracking, bias mitigation in persona development, and proper statistical treatment of MaxDiff and discrete choice data. All outputs are structured for stakeholder consumption, with severity-weighted findings, prioritized insights, and research-to-action translation.

## Core Capabilities

- **Interview Script Design**: Semi-structured interview guides with question scaffolding, probing frameworks, think-aloud prompts, and bias-aware question ordering
- **Survey Methodology**: Multi-scale survey construction with skip logic, sample size calculation, statistical significance testing, and response bias analysis
- **Persona Development**: Data-driven persona synthesis from behavioral clusters with confidence scoring, anti-persona generation, and empathy map integration
- **Journey Mapping**: Multi-touchpoint journey map construction with emotion tracking, opportunity identification, and cross-channel gap analysis
- **Jobs-to-be-Done Framework**: Outcome-driven JTBD capture, progress-making forces analysis, and opportunity scoring with underserved/overserved matrices
- **Diary Study Management**: Longitudinal study design with prompting schedules, engagement scoring, and temporal pattern analysis
- **Card Sorting Analysis**: Open, closed, and hybrid card sort evaluation with dendrogram clustering, similarity matrix computation, and agreement scoring
- **Research Repository**: Cross-study insight aggregation, tagged finding management, and longitudinal trend tracking across research cycles

## Usage Examples

### Designing an Interview Script

```python
from user_research import InterviewScript, QuestionType, ProbeType

script = InterviewScript(
    title="Onboarding Flow Exploration",
    target_duration_minutes=45,
    methodology="semi-structured"
)

script.add_section("Warm-up", questions=[
    {"text": "Tell me about the last time you set up a new tool for your team.",
     "type": QuestionType.OPEN_ENDED,
     "probes": [ProbeType.CLARIFY, ProbeType.EXPAND, "What made that experience memorable?"]},
    {"text": "How many tools does your team use regularly?",
     "type": QuestionType.SCALE,
     "scale_range": (1, 10)},
])

script.add_section("Core Exploration", questions=[
    {"text": "Walk me through what happens when you first log into a new application.",
     "type": QuestionType.THINK_ALOUD,
     "probes": [ProbeType.REPEAT, ProbeType.SPECIFIC_EXAMPLE]},
    {"text": "What would make you stop using a new tool in the first week?",
     "type": QuestionType.OPEN_ENDED,
     "follow_ups": ["Has that ever happened? What triggered it?"]},
])

script.validate_bias_patterns()  # Checks for leading questions, double-barreled queries
print(script.generate_facilitator_notes())
```

### Building Data-Driven Personas

```python
from user_research import PersonaBuilder, PersonaType, ConfidenceLevel

builder = PersonaBuilder(data_source="survey_and_interview")

builder.add_behavioral_cluster(
    name="Power Collaborators",
    traits=["daily active", "multi-project", "cross-functional"],
    demographics={"role": "Product Manager", "experience_years": "5+"},
    goals=["streamline cross-team communication", "reduce meeting overhead"],
    frustrations=["tool sprawl", "context switching between platforms"],
    behaviors={"session_length_minutes": 45, "features_used": 12, "login_frequency": "daily"},
    sample_size=34,
    confidence=ConfidenceLevel.HIGH
)

builder.add_behavioral_cluster(
    name="Occasional Checkers",
    traits=["weekly active", "single-project", "specialist"],
    demographics={"role": "Engineer", "experience_years": "3-5"},
    goals=["stay informed without constant context switching"],
    frustrations=["too many notifications", "irrelevant updates"],
    behaviors={"session_length_minutes": 12, "features_used": 4, "login_frequency": "weekly"},
    sample_size=28,
    confidence=ConfidenceLevel.MEDIUM
)

personas = builder.generate_personas()
builder.generate_anti_personas()  # Edge cases to test against
builder.export_empathy_maps(output_dir="./artifacts")
```

### JTBD Opportunity Scoring

```python
from user_research import JTBDAnalyzer, ImportanceLevel, SatisfactionLevel

analyzer = JTBDAnalyzer()

analyzer.add_job(
    statement="When I start a new project, I want to set up a shared workspace so that my team stays aligned from day one.",
    context="project initiation",
    metric="time_to_first_team_alignment"
)

analyzer.add_job(
    statement="When I receive stakeholder feedback, I want to route it to the right owners so that nothing falls through the cracks.",
    context="feedback management",
    metric="feedback_resolution_rate"
)

# Rate importance and current satisfaction (1-10 scale)
ratings = [
    {"job_id": "job_1", "importance": 9, "satisfaction": 4},
    {"job_id": "job_2", "importance": 8, "satisfaction": 3},
]

opportunities = analyzer.compute_opportunity_scores(ratings)
# Opportunities = Importance + max(Importance - Satisfaction, 0)
# High opportunity = high importance + low satisfaction = underserved

analyzer.plot_opportunity_matrix()
analyzer.export_underserved_report()
```

### Research Repository Management

```python
from user_research import ResearchRepository, FindingStatus, InsightTag

repo = ResearchRepository(project="collaboration-platform")

repo.add_finding(
    study="onboarding-interviews-q1-2026",
    insight="Users consistently expect a guided setup wizard; 8 of 12 participants described their ideal first-run as 'step-by-step hand-holding'",
    evidence=["interview-transcript-04", "interview-transcript-09"],
    status=FindingStatus.VALIDATED,
    tags=[InsightTag.ONBOARDING, InsightTag.NAVIGATION, InsightTag.EXPECTATION_GAP],
    confidence=0.85,
    linked_personas=["Power Collaborators"]
)

repo.add_finding(
    study="diary-study-weekly-engagement",
    insight="Engagement drops 60% after day 3 if user has not invited at least one collaborator",
    evidence=["diary-day3-log", "analytics-cohort-data"],
    status=FindingStatus.PARTIALLY_VALIDATED,
    tags=[InsightTag.ENGAGEMENT, InsightTag.SOCIAL_FEATURES],
    confidence=0.72
)

# Query the repository
insights = repo.query(tags=[InsightTag.ONBOARDING], status=FindingStatus.VALIDATED)
report = repo.generate_insight_summary()
repo.export_for_stakeholders(format="markdown")
```

### Diary Study Management

```python
from user_research import DiaryStudy, PromptType, EngagementLevel

study = DiaryStudy(
    name="Weekly Collaboration Habits",
    duration_days=21,
    participant_count=15,
)

study.schedule_prompt(
    day=1, prompt_type=PromptType.TEXT,
    question="Describe your first experience setting up a workspace.",
)
study.schedule_prompt(
    day=7, prompt_type=PromptType.TEXT,
    question="What has changed in how you collaborate this week?",
)
study.schedule_prompt(
    day=14, prompt_type=PromptType.SCALE,
    question="Rate your satisfaction with the collaboration tools this week (1-10).",
)
study.schedule_prompt(
    day=21, prompt_type=PromptType.TEXT,
    question="If you could change one thing about the tool, what would it be?",
)

# Analyze engagement
engagement = study.engagement_analysis()
print(f"Completion rate: {engagement['completion_rate']:.1%}")
print(f"Average engagement: {engagement['avg_engagement']}")
for day, level in engagement['daily_breakdown'].items():
    print(f"  Day {day}: {level}")
```

### Survey Methodology

```python
from user_research import SurveyBuilder, ScaleType, SkipLogic

survey = SurveyBuilder(
    name="Feature Satisfaction Survey",
    target_population="Active users (30-day)",
    target_response_rate=0.30,
)

survey.add_question(
    text="How satisfied are you with the new dashboard?",
    scale=ScaleType.LIKERT_5,
    required=True,
)
survey.add_question(
    text="Which features do you use most?",
    scale=ScaleType.MULTI_SELECT,
    options=["Analytics", "Reports", "Collaboration", "Integrations"],
    required=True,
)
survey.add_question(
    text="How likely are you to recommend this product?",
    scale=ScaleType.NPS,
    required=True,
)

# Skip logic: only show if user selected "Integrations"
survey.add_question(
    text="Which integrations are most important to you?",
    scale=ScaleType.OPEN_TEXT,
    required=False,
    skip_logic=SkipLogic(condition="multi_select contains 'Integrations'"),
)

# Sample size calculation
sample = survey.calculate_sample_size(
    population_size=5000,
    confidence_level=0.95,
    margin_of_error=0.05,
)
print(f"Minimum responses needed: {sample}")
```

## Best Practices

1. **Triangulate methods**: Never rely on a single research method. Combine interviews with surveys, diary studies with analytics. When findings converge across methods, confidence increases dramatically; when they diverge, investigate why.

2. **Recruit for behavioral diversity**: Demographics alone are insufficient for recruitment. Screen for behavioral patterns, usage frequency, and task expertise. A persona built on behavior is actionable; one built on age and job title is not.

3. **Track saturation explicitly**: Maintain a saturation matrix as you analyze data. When new interviews stop yielding novel themes, document the saturation point and justify your sample size. This prevents both premature closure and over-research.

4. **Mitigate bias in persona development**: Use clustering algorithms or affinity diagramming rather than starting with hypothesized segments. Let the data reveal natural groupings. Generate anti-personas alongside primary personas to stress-test design decisions.

5. **Separate observations from interpretations**: In your research repository, tag findings as either raw observations ("the participant paused for 30 seconds at step 3") or interpretations ("the participant was confused at step 3"). Interpretations need evidence chains; observations stand alone.

6. **Design surveys with statistical rigor**: Calculate minimum sample size before launching. Use validated scales (SUS, NPS, PMF) rather than ad-hoc questions. Include attention checks and reverse-coded items. Analyze response bias by comparing early vs. late respondents.

7. **Maintain a living research repository**: Don't let findings die in slide decks. Tag, link, and date every insight. Review quarterly for trends, contradictions, and gaps that warrant new research. A stale repository is worse than no repository.

8. **Translate research to action**: Every study should produce not just insights but specific design recommendations with confidence levels. Stakeholders consume actions, not observations. Bridge the gap with clear next-step ownership and timelines.

## Related Modules

- [usability-testing](../usability-testing/GROK.md) — Task success measurement, think-aloud analysis, and severity rating
- [information-architecture](../information-architecture/GROK.md) — Card sort and tree test analysis for IA decisions
- [interaction-design](../interaction-design/GROK.md) — Micro-interaction patterns informed by user research findings
- [accessibility](../accessibility/GROK.md) — Inclusive research methods and accessibility-specific participant recruitment

---

## Advanced Configuration

### Interview Bias Detection

```python
from user_research import BiasDetector

detector = BiasDetector()
biases = detector.analyze_script(script)
for bias in biases:
    print(f"[{bias.severity}] {bias.type}: {bias.question_text}")
    print(f"  Suggestion: {bias.suggestion}")
```

### Statistical Significance Testing

```python
from user_research import StatisticalTests

tests = StatisticalTests()
significance = tests.mann_whitney_u(
    group_a=[3.2, 4.1, 3.8, 4.5, 3.9],
    group_b=[2.8, 3.1, 2.5, 3.0, 2.7],
    alpha=0.05,
)
print(f"Significant: {significance.is_significant}, p={significance.p_value:.4f}")
```

## Architecture Patterns

### Research Pipeline

```
Research Question
    │
    ▼
┌──────────────┐
│ Method       │── Interview, Survey, Diary, Card Sort
│ Selection    │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Recruitment  │── Screener, demographics, behavioral criteria
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Data         │── Transcripts, responses, observations
│ Collection   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Analysis     │── Thematic coding, affinity diagramming, stats
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Synthesis    │── Personas, journey maps, JTBD
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Delivery     │── Stakeholder report, action items
└──────────────┘
```

## Integration Guide

### Research Repository Integration

```python
from user_research import ResearchRepository

repo = ResearchRepository(project="my-product")
repo.sync_with_notion(database_id="xxx")
repo.sync_with_dovetail(api_key="yyy")
```

### Survey Platform Integration

```python
from user_research import SurveyBuilder

survey = SurveyBuilder(name="NPS Survey")
survey.export_qualtrics("nps_survey.qsf")
survey.export_google_forms()
survey.export_typeform()
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Transcript auto-tagging | 60% faster analysis |
| AI-assisted affinity diagramming | Consistent thematic coding |
| Template reuse | 3x faster study setup |
| Automated saturation tracking | Prevent over-research |
| Batch export | One-click stakeholder delivery |

## Security Considerations

- **Participant PII**: Encrypt all participant contact information
- **Transcript confidentiality**: Store transcripts in access-controlled repositories
- **Recording consent**: Written consent before all sessions, stored securely
- **Data retention**: Define and enforce retention policies per study
- **Anonymization**: Strip identifying information before sharing findings

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Low survey response rate | Survey too long, poor timing | Shorten survey, send at optimal time |
| Saturation not reached | Insufficient sample diversity | Recruit for behavioral diversity |
| Persona confidence low | Small sample per cluster | Increase targeted recruitment |
| Diary study drop-off | Prompt fatigue | Reduce prompt frequency, add gamification |
| Card sort disagreement | Ambiguous card labels | Rewrite labels using user language |

## API Reference

### InterviewScript

```python
class InterviewScript:
    def __init__(self, title: str, target_duration_minutes: int, methodology: str)
    def add_section(self, name: str, questions: list) -> None
    def validate_bias_patterns(self) -> list[BiasReport]
    def generate_facilitator_notes(self) -> str
    def export(self, format: str) -> str
```

### PersonaBuilder

```python
class PersonaBuilder:
    def __init__(self, data_source: str)
    def add_behavioral_cluster(self, **kwargs) -> None
    def generate_personas(self) -> list[Persona]
    def generate_anti_personas(self) -> list[AntiPersona]
    def export_empathy_maps(self, output_dir: str) -> None
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class ConfidenceLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Persona:
    name: str
    traits: list
    demographics: dict
    goals: list
    frustrations: list
    behaviors: dict
    confidence: ConfidenceLevel

@dataclass
class Finding:
    study: str
    insight: str
    evidence: list
    status: str
    tags: list
    confidence: float
```

## Deployment Guide

### Installation

```bash
pip install user-research
```

### Team Setup

1. Create project repository structure
2. Configure participant management system
3. Set up recording and transcription pipeline
4. Connect analysis tools (Miro, FigJam, Dovetail)
5. Define research cadence and rituals

## Monitoring & Observability

```python
from user_research import MetricsCollector

collector = MetricsCollector()
collector.gauge("research.studies.active", count)
collector.gauge("research.participants.recruited", count)
collector.counter("research.findings.generated", count, tags={"status": status})
collector.histogram("research.study.duration_days", duration)
```

## Testing Strategy

```python
import pytest
from user_research import InterviewScript, PersonaBuilder

def test_bias_detection():
    script = InterviewScript(title="Test", target_duration_minutes=30, methodology="semi-structured")
    script.add_section("Test", questions=[{"text": "Don't you agree this is great?", "type": "OPEN_ENDED"}])
    biases = script.validate_bias_patterns()
    assert any(b.type == "leading_question" for b in biases)
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | AI-assisted analysis | Enable AI features in config |
| 2.0.0 | New repository schema | Migrate findings to new format |

## Glossary

| Term | Definition |
|------|-----------|
| **Saturation** | Point where new data yields no new themes |
| **Triangulation** | Using multiple methods to validate findings |
| **JTBD** | Jobs-to-be-Done framework |
| **Affinity Diagram** | Grouping related observations into themes |
| **Memo** | Researcher reflection during analysis |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with interview, survey, and diary study tools
- Persona development with behavioral clustering
- JTBD opportunity scoring
- Research repository management

## Contributing Guidelines

```bash
git clone https://github.com/example/user-research.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Interview Question Bank

| Category | Question | Purpose |
|----------|----------|---------|
| Warm-up | Tell me about your role | Build rapport |
| Warm-up | Walk me through a typical day | Context setting |
| Exploration | What tools do you use daily? | Current behavior |
| Exploration | What frustrates you most? | Pain points |
| Exploration | How do you solve X problem? | Workarounds |
| Probing | Can you give me an example? | Specific evidence |
| Probing | Why do you do it that way? | Motivation |
| Probing | What would ideal look like? | Aspirations |
| Wrap-up | What would you change? | Open-ended insight |
| Wrap-up | Is there anything I didn't ask? | Catch-all |

### Survey Scale Reference

| Scale | Type | Use Case | Min | Max |
|-------|------|----------|-----|-----|
| Likert | Agreement | Satisfaction, agreement | 1 | 5 |
| NPS | Recommendation | Loyalty, advocacy | 0 | 10 |
| SUS | Usability | System usability | 1 | 5 |
| PMF | Product-Market Fit | Fit assessment | 1 | 4 |
| CSAT | Satisfaction | Feature satisfaction | 1 | 5 |
| Semantic Differential | Perception | Brand perception | 1 | 7 |

### Sample Size Calculator

| Population | 95% CI, ±5% | 95% CI, ±3% | 99% CI, ±5% |
|-----------|-------------|-------------|-------------|
| 100 | 80 | 92 | 87 |
| 500 | 217 | 341 | 278 |
| 1,000 | 278 | 516 | 333 |
| 5,000 | 357 | 879 | 400 |
| 10,000 | 370 | 964 | 414 |
| 100,000+ | 384 | 1,067 | 429 |

### Persona Template

```markdown
# [Persona Name]

## Demographics
- Role: [Job title]
- Experience: [Years]
- Company size: [Range]
- Industry: [Sector]

## Behavioral Patterns
- Usage frequency: [Daily/Weekly/Monthly]
- Session length: [Minutes]
- Features used: [List]
- Device preference: [Mobile/Desktop/Both]

## Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

## Frustrations
1. [Pain point 1]
2. [Pain point 2]
3. [Pain point 3]

## Quotes
> "[Direct quote from interview]"

## Scenario
[Story describing how this persona interacts with the product]
```

### Research Cadence Template

| Activity | Frequency | Duration | Participants | Output |
|----------|-----------|----------|-------------|--------|
| User interviews | Weekly | 45 min | 3-5 | Transcripts, insights |
| Usability testing | Bi-weekly | 60 min | 5-8 | Task metrics, findings |
| Survey | Monthly | 15 min | 200+ | Quantitative data |
| Diary study | Quarterly | 21 days | 15-20 | Behavioral patterns |
| Card sort | Quarterly | 30 min | 20-30 | IA recommendations |
| A/B test analysis | Weekly | 30 min | — | Statistical results |

### Common Research Biases

| Bias | Description | Mitigation |
|------|-------------|------------|
| Confirmation | Seeking confirming evidence | Use structured protocols |
| Selection | Recruiting similar participants | Screen for diversity |
| Social desirability | Participants giving "correct" answers | Observe behavior, not just words |
| Recency | Overweighting recent experiences | Use structured timelines |
| Anchoring | First answer influences later ones | Randomize question order |
| Leading | Questions that suggest answers | Use neutral phrasing |

### Research Repository Structure

```
research-repo/
├── studies/
│   ├── 2024-q1-onboarding-interviews/
│   │   ├── protocol.md
│   │   ├── transcripts/
│   │   ├── analysis/
│   │   └── findings.md
│   ├── 2024-q1-usability-testing/
│   └── 2024-q2-diary-study/
├── personas/
│   ├── power-collaborator.md
│   └── occasional-checker.md
├── journey-maps/
│   └── onboarding-journey.md
├── insights/
│   ├── onboarding.md
│   └── engagement.md
└── reports/
    └── q1-research-report.md
```

### Research Ethics Checklist

```
ETHICS REVIEW
    □ Informed consent obtained
    □ Right to withdraw explained
    □ Data anonymization plan in place
    □ Recording consent obtained
    □ Incentive amount appropriate (not coercive)
    □ PII storage and retention defined
    □ Data sharing restrictions documented
    □ Vulnerable populations considerations
    □ Accessibility accommodations planned
    □ IRB approval (if required)
```

### Complete Interview Script Template

```markdown
# Interview Script: [Project Name]

## Pre-Interview Setup
- Recording device ready
- Consent form prepared
- Notes template open
- Participant info collected

## Warm-Up (5 minutes)
1. Thank you for joining us today.
2. Can you tell me a bit about your role and what you do day-to-day?
3. How long have you been in this role?

## Background (10 minutes)
4. Walk me through a typical workday from start to finish.
5. What tools or applications do you use most frequently?
6. How do you currently handle [specific task related to research question]?

## Core Exploration (20 minutes)
7. Tell me about the last time you [specific task]. Walk me through it step by step.
8. What was the most challenging part of that experience?
9. How did you overcome that challenge?
10. What would you do differently if you could do it again?
11. What tools or workarounds have you created to help with this?
12. Can you show me how you currently [specific workflow]?

## Deep Dive (10 minutes)
13. What frustrates you most about the current process?
14. If you could wave a magic wand and change one thing, what would it be?
15. How does this affect your team or organization?
16. What would an ideal solution look like to you?

## Wrap-Up (5 minutes)
17. Is there anything I didn't ask about that you think is important?
18. Would you be willing to participate in a follow-up study?
19. Thank you for your time!

## Post-Interview Notes
- Key observations:
- Notable quotes:
- Surprising findings:
- Follow-up questions:
```

### Complete Survey Template

```markdown
# Survey: [Product/Feature Name]

## Section 1: Demographics (3 questions)
1. What is your role? [Dropdown]
2. How long have you used this product? [Dropdown]
3. How frequently do you use this product? [Scale: Daily/Weekly/Monthly/Rarely]

## Section 2: Satisfaction (5 questions)
4. How satisfied are you with [feature]? [Likert 1-5]
5. How easy is it to use [feature]? [Likert 1-5]
6. How likely are you to recommend [product]? [NPS 0-10]
7. How does [product] compare to alternatives? [Better/Same/Worse]
8. Overall, how satisfied are you with [product]? [CSAT 1-5]

## Section 3: Specific Features (5 questions)
9. Which features do you use most? [Multi-select]
10. Which features do you use least? [Multi-select]
11. How important is [feature X]? [Scale: Not important to Very important]
12. How well does [feature X] meet your needs? [Scale: Not at all to Completely]
13. What features are missing that you would like to see? [Open text]

## Section 4: Open Feedback (2 questions)
14. What do you like most about [product]? [Open text]
15. What would you improve about [product]? [Open text]

## Thank You
Thank you for completing this survey! Your feedback helps us improve.
```

### Journey Map Template

```markdown
# Journey Map: [User Type] - [Scenario]

## Touchpoints
| Phase | Actions | Thoughts | Emotions | Pain Points | Opportunities |
|-------|---------|----------|----------|-------------|---------------|
| Awareness | Discovers product via ad | "Looks interesting" | Curious | Information overload | Clearer value proposition |
| Consideration | Visits website, reads reviews | "Is this right for me?" | Hopeful | Unclear pricing | Transparent pricing page |
| Onboarding | Signs up, creates account | "How do I get started?" | Excited | Complex setup | Guided onboarding |
| First Use | Uses core feature | "This is easier than I thought" | Satisfied | Learning curve | In-app tutorials |
| Regular Use | Uses product daily | "Part of my workflow" | Confident | Feature gaps | Feature requests |
| Advocacy | Recommends to others | "You should try this" | Enthusiastic | Nothing to share | Referral program |

## Key Metrics by Phase
| Phase | Metric | Current | Target |
|-------|--------|---------|--------|
| Awareness | Brand awareness | 20% | 40% |
| Consideration | Website conversion | 5% | 10% |
| Onboarding | Completion rate | 60% | 80% |
| First Use | Feature adoption | 40% | 70% |
| Regular Use | DAU/MAU ratio | 30% | 50% |
| Advocacy | NPS | 20 | 50 |
```

### Research Insight Format

```markdown
## Insight: [Title]

**Source:** [Study name and date]
**Confidence:** [High/Medium/Low]
**Status:** [Validated/Partially Validated/New]

### Observation
[What we observed in the research]

### Evidence
- [Participant quote or data point 1]
- [Participant quote or data point 2]
- [Participant quote or data point 3]

### Interpretation
[What this means for our users and product]

### Implications
- [Design implication 1]
- [Design implication 2]

### Recommendations
- [Specific recommendation 1]
- [Specific recommendation 2]

### Linked Personas
- [Persona 1]
- [Persona 2]
```
