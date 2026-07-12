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
