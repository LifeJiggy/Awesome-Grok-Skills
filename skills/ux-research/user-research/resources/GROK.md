# UX Research Agent

## Overview

The **UX Research Agent** provides comprehensive user research capabilities including persona development, usability testing, journey mapping, and A/B testing. This agent helps understand user needs and optimize user experiences.

## Core Capabilities

### 1. User Research Management
Plan and conduct research:
- **Research Planning**: Method selection, participant recruitment
- **Interview Facilitation**: User interviews, focus groups
- **Survey Design**: Questionnaires, sampling
- **Diary Studies**: Longitudinal observation
- **Usability Testing**: Task-based evaluation

### 2. Persona Development
Create user archetypes:
- **Demographic Profiling**: Age, occupation, location
- **Behavioral Analysis**: Goals, frustrations, behaviors
- **Persona Cards**: Visual summaries
- **Journey Mapping**: User experience paths
- **Persona Comparison**: Differentiation analysis

### 3. Usability Testing
Evaluate user interfaces:
- **Task Analysis**: User task definition
- **Session Recording**: Video and audio capture
- **Heuristic Evaluation**: Expert review
- **Accessibility Testing**: WCAG compliance
- **Remote Testing**: Distributed evaluation

### 4. Journey Mapping
Visualize user experiences:
- **Touchpoint Mapping**: User interactions
- **Emotion Analysis**: Sentiment tracking
- **Pain Point Identification**: Problem areas
- **Opportunity Discovery**: Improvement areas
- **Journey Scoring**: Quantitative assessment

### 5. A/B Testing
Data-driven optimization:
- **Test Design**: Hypothesis formulation
- **Sample Calculation**: Statistical power
- **Test Execution**: A/B/n testing
- **Statistical Analysis**: Significance testing
- **Results Interpretation**: Actionable insights

## Usage Examples

### Conduct User Research

```python
from ux_research import UserResearch

research = UserResearch()
plan = research.create_research_plan(
    method=ResearchMethod.INTERVIEW,
    objectives=['Understand pain points', 'Identify needs'],
    target_audience=[UserSegment.NEW_USER, UserSegment.POWER_USER],
    timeline='2 weeks'
)
results = research.analyze_interviews(['int_1', 'int_2'])
```

### Create Persona

```python
from ux_research import PersonaDevelopment

personas = PersonaDevelopment()
p1 = personas.create_persona(
    name='Alice Power',
    demographic={'age': '30-40', 'occupation': 'Engineer'},
    goals=['Quick workflows', 'Advanced features'],
    frustrations=['Too many clicks', 'Slow loading'],
    behaviors=['Uses keyboard shortcuts', 'Daily login'],
    quote="I need efficiency in everything I do."
)
card = personas.create_persona_card(p1)
```

### Run Usability Test

```python
from ux_research import UsabilityTesting

usability = UsabilityTesting()
test = usability.create_test_plan(
    task='Complete purchase',
    success_criteria=['Cart viewed', 'Payment entered', 'Confirmation shown'],
    participant_count=5
)
results = usability.aggregate_test_results(['s1', 's2', 's3'])
print(f"Completion rate: {results['completion_rate']}")
```

### A/B Testing

```python
from ux_research import ABTesting

ab = ABTesting()
experiment = ab.design_experiment(
    control={'button_color': 'blue'},
    variant={'button_color': 'green'},
    metric='conversion_rate',
    sample_size=1000
)
analysis = ab.analyze_experiment('exp_1')
print(f"Significant: {analysis['statistically_significant']}")
```

## Research Methods

### Qualitative Methods
| Method | Description | Best For |
|--------|-------------|----------|
| Interviews | 1:1 conversations | Deep insights |
| Focus Groups | Group discussion | Ideas generation |
| Contextual Inquiry | In-context observation | Real behavior |
| Diary Studies | Self-reported logs | Longitudinal patterns |
| Card Sorting | Information architecture | Content organization |

### Quantitative Methods
| Method | Description | Best For |
|--------|-------------|----------|
| Surveys | Large-scale questionnaires | Statistical validation |
| A/B Testing | Controlled experiments | Optimization |
| Tree Testing | Navigation testing | IA validation |
| Task Analysis | Task metrics | Usability metrics |
| System Usability Scale | Standardized questionnaire | Benchmarking |

## Persona Development

### Persona Elements
```
┌────────────────────────────────────────┐
│           Persona: Alice Power          │
├────────────────────────────────────────┤
│  Photo / Avatar                         │
├────────────────────────────────────────┤
│  Demographics                           │
│  - Age: 30-40                           │
│  - Job: Software Engineer               │
│  - Location: San Francisco              │
├────────────────────────────────────────┤
│  Goals                                  │
│  - Speed and efficiency                 │
│  - Advanced functionality               │
├────────────────────────────────────────┤
│  Frustrations                           │
│  - Slow interfaces                      │
│  - Too many clicks                      │
├────────────────────────────────────────┤
│  Behaviors                              │
│  - Uses keyboard shortcuts              │
│  - Daily active user                    │
├────────────────────────────────────────┤
│  Quote                                  │
│  "I value my time above all else"       │
└────────────────────────────────────────┘
```

## Usability Testing

### Test Session Structure
1. **Introduction**: Welcome, consent, instructions
2. **Warm-up**: Simple practice task
3. **Main Tasks**: 3-5 core scenarios
4. **Debriefing**: Open discussion
5. **Thank You**: Compensation, next steps

### Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| Success Rate | % completing task | >80% |
| Time on Task | Duration to complete | Minimize |
| Error Rate | Mistakes made | Minimize |
| Satisfaction | User rating | >4/5 |
| SUS Score | System Usability Scale | >68 |

## Journey Mapping

### Journey Components
- **Stages**: Awareness, Consideration, Decision, Retention, Advocacy
- **Touchpoints**: Interactions with product/service
- **Emotions**: Sentiment at each stage
- **Pain Points**: Frustrations and barriers
- **Opportunities**: Areas for improvement
- **Metrics**: Quantitative measurements

## A/B Testing

### Test Design
```python
# Sample size calculation
ab.calculate_sample_size(
    baseline_rate=0.05,
    minimum_detectable_effect=0.01,
    power=0.8
)
```

### Statistical Analysis
- **Hypothesis Testing**: Null vs alternative
- **P-value**: Significance level (<0.05)
- **Confidence Interval**: Range of effect
- **Sample Size**: Power analysis
- **Multiple Comparisons**: Bonferroni correction

## Research Tools

### Discovery Tools
- **UserTesting**: Remote usability testing
- **Lookback**: User interview recording
- **Calendly**: Scheduling
- **Typeform**: Survey creation

### Analysis Tools
- **Dovetail**: Qualitative analysis
- **Miro**: Journey mapping
- **Optimal Workshop**: Card sorting, tree testing
- **Amplitude**: Product analytics

## Deliverables

### Research Reports
- Executive summary
- Key findings
- Recommendations
- Supporting data
- Appendices

### Personas
- Persona cards
- Persona comparison
- Use cases
- Quotations

### Test Reports
- Methodology
- Findings
- Recommendations
- Video clips
- Metrics

## Related Skills

- [Technical Writing](./technical-writing/documentation/README.md) - Documentation
- [Analytics](../analytics/data-analysis/README.md) - Data analysis
- [Design Systems](../design/ui-design/README.md) - Design implementation

---

**File Path**: `skills/ux-research/user-research/resources/ux_research.py`
