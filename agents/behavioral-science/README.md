# BehavioralScience Agent

Behavioral Science Agent - Behavior Analysis and Nudges.

## Quick Start

```python
from agents.behavioral-science.agent import BehavioralScienceAgent

agent = BehavioralScienceAgent()
result = agent.run()
print(result)
```

## Run the Agent

```bash
python agents/behavioral-science/agent.py
```

## Files

- `agent.py` - Main implementation
- `GROK.md` - Agent instructions
- `ARCHITECTURE.md` - System architecture
- `README.md` - This file

## Table of Contents

1. [Introduction](#introduction)
2. [What is the BehavioralScience Agent?](#what-is-the-behavioralscience-agent)
3. [Key Concepts](#key-concepts)
4. [Installation](#installation)
5. [Quick Start](#quick-start)
6. [Core Features](#core-features)
7. [API Usage](#api-usage)
8. [Configuration](#configuration)
9. [Examples](#examples)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)
13. [References](#references)
14. [Appendix](#appendix)
15. [Performance Guide](#performance-guide)
16. [Security Considerations](#security-considerations)
17. [Frequently Asked Questions](#frequently-asked-questions)

## Introduction

The Behavioral Science Agent is a comprehensive software module that applies principles from behavioral economics, cognitive psychology, and decision science to real-world user behavior data. It is designed to be a drop-in agent that can be integrated into larger systems, providing immediate value through bias detection, persona matching, nudge generation, and experimentation support.

This README provides a complete guide to understanding, installing, configuring, and using the Behavioral Science Agent across a variety of deployment contexts.

### Who Should Use This Agent?

- **Product Teams**: To optimize user flows and increase conversion rates
- **Behavioral Scientists**: To apply theoretical frameworks at scale
- **Data Scientists**: To run rigorous experiments on behavioral interventions
- **UX Researchers**: To understand user decision-making patterns
- **Marketing Teams**: To design evidence-based campaigns
- **Engineering Teams**: To integrate behavioral intelligence into products

### Key Benefits

1. **Evidence-Based**: All recommendations grounded in peer-reviewed research
2. **Modular Design**: Use individual components or full pipeline
3. **Production-Ready**: Includes error handling, logging, and state management
4. **Extensible**: Add custom biases, personas, and nudge types
5. **Statistically Rigorous**: Proper experiment design and analysis
6. **Privacy-Conscious**: Designed with data governance in mind

## What is the BehavioralScience Agent?

The Behavioral Science Agent is a specialized agent that focuses on understanding how and why users behave the way they do. Rather than treating users as purely rational actors, it acknowledges that human decisions are influenced by:

- **Cognitive Biases**: Systematic patterns of deviation from rationality that affect judgment and decision-making.
- **Emotional States**: Temporary mood and affect that shift behavior in predictable ways.
- **Social Context**: Peer behavior, social norms, and community signals that drive conformity.
- **Environmental Cues**: External triggers that initiate automatic behaviors through habit loops.
- **Decision Architecture**: The way choices are presented (framing, defaults, ordering) that changes preferences.

By modeling these influences, the agent can recommend interventions - called nudges - that help users make better decisions while preserving freedom of choice. It also provides the statistical infrastructure to test whether those interventions are actually working.

### The Behavioral Science Stack

The agent combines multiple disciplines:

| Discipline | Contribution to Agent |
|------------|----------------------|
| Behavioral Economics | Bias detection, nudge design, incentive theory |
| Cognitive Psychology | Persona modeling, decision architecture |
| Social Psychology | Social proof, conformity, influence principles |
| Experimental Psychology | A/B testing design, power analysis |
| Data Science | Statistical rigor, pattern mining, cohort analysis |
| Computer Science | Software architecture, API design, state management |

### Comparison to Alternatives

| Approach | Strengths | Limitations |
|----------|-----------|-------------|
| Behavioral Science Agent | Comprehensive, statistically rigorous, extensible | Requires behavioral event tagging |
| Rule-based personalization | Simple, interpretable | Limited to predefined rules |
| ML recommendation systems | Data-hungry, self-improving | Black box, requires large datasets |
| A/B testing platforms | Industry standard | No automatic nudge generation |
| Analytics dashboards | Visualization, reporting | No intervention design |

## Key Concepts

### Behavioral Events

A behavioral event is a structured data point representing a user action or interaction. Events include tags, properties, and context that allow the agent to detect biases, match personas, and recommend nudges.

Example event:

```json
{
  "event_id": "evt_12345",
  "user_id": "user_abc",
  "event_type": "add_to_cart",
  "timestamp": "2025-01-15T10:30:00Z",
  "tags": ["product_view", "checkout_begin"],
  "properties": {
    "device": "mobile",
    "channel": "app",
    "value": 49.99
  },
  "context": {
    "page_depth": 3,
    "session_duration": 120
  }
}
```

**Event Tagging Best Practices**:

- Use consistent tag vocabulary across all event sources
- Tag both the action and the context (e.g., "checkout_begin" + "cart_abandon")
- Include device and channel information in tags
- Add emotional or situational tags (e.g., "time_pressure", "research_mode")
- Update tag dictionary as new patterns emerge

### Nudges

Nudges are behavioral interventions designed to alter behavior in a predictable way without forbidding any options or significantly changing economic incentives. Examples include changing default settings, reframing messages, displaying social proof, or reducing friction.

**Nudge Design Principles**:

1. **Libertarian Paternalism**: Guide choices while preserving freedom
2. **Transparency**: Make the nudge visible and explainable
3. **Easy Opt-Out**: Allow reversal at any time
4. **Minimal Intervention**: Use weakest effective nudge
5. **Evidence-Based**: Ground in research, not assumptions

**Nudge Strength Guidelines**:

| Strength | Use Case | Risk Level |
|----------|----------|-----------|
| 0.1 - 0.3 | Subtle suggestions, low-risk contexts | Very Low |
| 0.3 - 0.5 | Standard nudges, general population | Low |
| 0.5 - 0.7 | Targeted interventions, known segments | Medium |
| 0.7 - 0.9 | High-stakes decisions, carefully reviewed | High |
| 0.9 - 1.0 | Critical interventions, legal review required | Very High |

### Cognitive Biases

Cognitive biases are systematic deviations from normative judgment. The agent tracks 10+ biases including loss aversion, anchoring, confirmation bias, availability heuristic, endowment effect, sunk cost fallacy, bandwagon effect, framing effect, social proof, and scarcity heuristic.

**Bias Severity Classification**:

| Bias | Severity | Reversibility | Common Domains |
|------|----------|---------------|----------------|
| loss_aversion | High | Medium | Finance, health, insurance |
| anchoring | Medium | High | Pricing, negotiations |
| confirmation | High | Low | Information search, beliefs |
| availability | Medium | High | Risk perception, marketing |
| endowment | Medium | Medium | Ownership, trials |
| sunk_cost | High | Low | Project continuation |
| bandwagon | Medium | High | Social products, trends |
| framing | High | High | Messaging, compliance |
| social_proof | Low | High | Social products, reviews |
| scarcity | High | Medium | E-commerce, events |

### Personas

Personas are behavioral archetypes representing distinct user segments. Each persona is defined by trait profiles (e.g., impulsivity, price sensitivity) and behavioral tendencies. The agent comes with 8 default personas and supports custom persona creation.

**Persona Trait Definitions**:

- **impulsivity**: Tendency to make quick, emotion-driven decisions (0.0 = highly deliberative, 1.0 = highly impulsive)
- **price_sensitivity**: Degree to which cost influences decisions (0.0 = price indifferent, 1.0 = highly price sensitive)
- **social_influence**: Susceptibility to peer behavior and social norms (0.0 = independent, 1.0 = highly conforming)
- **risk_tolerance**: Comfort with uncertainty and potential losses (0.0 = highly risk averse, 1.0 = risk seeking)
- **novelty_seeking**: Preference for new experiences over familiar ones (0.0 = routine preference, 1.0 = novelty preference)
- **habit_strength**: Degree of automaticity in behavior patterns (0.0 = fully deliberate, 1.0 = fully automatic)
- **deliberation**: Tendency to think deeply before deciding (0.0 = intuitive, 1.0 = highly deliberative)
- **loss_aversion**: Sensitivity to potential losses vs equivalent gains (0.0 = neutral, 1.0 = highly loss averse)

### Habit Loops

Based on Duhigg's habit loop model, a habit consists of a cue (trigger), routine (behavior), and reward. The agent tracks habit execution, reinforcement, streaks, and break attempts to understand and influence habit formation.

**Habit Loop Components**:

```
Cue (Trigger) -> Routine (Behavior) -> Reward -> Increased Likelihood of Recurrence
```

**Habit Strength Scale**:

| Strength | Description | Intervention Strategy |
|----------|-------------|----------------------|
| 0.0 - 0.2 | Non-existent | Build from scratch with continuous reinforcement |
| 0.2 - 0.4 | Emerging | Increase cue salience, ensure immediate rewards |
| 0.4 - 0.6 | Developing | Variable reinforcement, reduce friction |
| 0.6 - 0.8 | Strong | Maintenance schedule, prevent decay |
| 0.8 - 1.0 | Automatic | Minimal reinforcement needed |

### Experiments

The agent supports rigorous A/B testing with statistical calculations including p-values, effect sizes (Cohen's h), confidence intervals, and power analysis. Experiments can be A/B, multivariate, time-series, or cohort-based.

**Experiment Decision Framework**:

1. **Formulate Hypothesis**: Clear statement of expected effect
2. **Calculate Sample Size**: Use compute_power_analysis()
3. **Design Variants**: Control and treatment with meaningful differences
4. **Launch Experiment**: Use run_ab_test() or run_ab_test_multivariate()
5. **Monitor**: Track intermediate results, check for significance
6. **Analyze**: Use record_experiment_observation() to accumulate data
7. **Conclude**: Use close_ab_test() to compute final statistics
8. **Act**: Implement winner or iterate based on findings

**Effect Size Interpretation (Cohen's h)**:

| h Value | Interpretation | Practical Meaning |
|---------|----------------|-------------------|
| 0.00 - 0.20 | Negligible | Not worth implementing |
| 0.20 - 0.50 | Small | Meaningful at scale (high traffic) |
| 0.50 - 0.80 | Medium | Clearly noticeable effect |
| 0.80+ | Large | Highly impactful change |

## Installation

### Prerequisites

- Python 3.8 or higher
- No external dependencies required for core functionality
- Optional: pytest for running tests

### Setup Steps

1. Clone or copy the repository:

```bash
git clone https://github.com/yourorg/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills/agents/behavioral-science
```

2. Verify the agent files are present:

```bash
ls -la
# Should show: agent.py, GROK.md, ARCHITECTURE.md, README.md
```

3. Test import:

```bash
python -c "from agents.behavioral-science.agent import BehavioralScienceAgent; print('OK')"
```

### Optional: Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # If requirements file exists
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app/agents/behavioral-science
CMD ["python", "agent.py", "--config", "/config/config.yaml"]
```

### Verification Steps

```python
# Quick verification script
from agents.behavioral-science.agent import BehavioralScienceAgent

agent = BehavioralScienceAgent()
print(f"Agent initialized: {agent}")
print(f"Personas loaded: {agent.list_personas()}")
print(f"Biases indexed: {list(agent.cognitive_biases_index.keys())}")
```

## Quick Start

The fastest way to start using the agent:

```python
from agents.behavioral-science.agent import BehavioralScienceAgent

agent = BehavioralScienceAgent()
result = agent.run(user_input="quick_start")
print(result)
```

Expected output:

```json
{
  "agent": "BehavioralScience",
  "session_id": "a1b2c3d4e5f6g7h8",
  "status": "completed",
  "analysis": {
    "session_id": "...",
    "triggered_biases": [],
    "recommended_nudges": ["default_effect"],
    "overall_confidence": 0.0
  },
  "nudge": {
    "nudge_id": "nudge_abc1234",
    "nudge_type": "default_effect",
    "strength": 0.5,
    "status": "draft"
  }
}
```

### First 5 Minutes

1. **Initialize** the agent with `BehavioralScienceAgent()`
2. **Analyze** a sample event to see bias detection in action
3. **Design** your first nudge for a common behavior
4. **Run** a sample A/B test to see experiment tracking
5. **Export** state to verify persistence

### Common First Tasks

| Task | Code Snippet |
|------|-------------|
| Detect biases | `agent.analyze_behavior("user_1", {"tags": ["checkout", "cart_abandon"]})` |
| Design nudge | `agent.design_nudge("checkout", "purchase", strength=0.6)` |
| Create habit | `agent.register_habit_loop("login", "notification", "open", "points")` |
| Run experiment | `agent.run_ab_test("test", "A", "B")` |
| Track feedback | `agent.record_feedback("user_1", "nudge_click", {"rating": 5})` |

## Core Features

### 1. Behavior Analysis

Analyze any behavioral event to detect cognitive biases, match personas, and get intervention recommendations.

```python
event = {
    "tags": ["checkout", "cart_abandon", "loss_aversion_message"],
    "session_duration": 200,
    "value": 89.99
}
analysis = agent.analyze_behavior("user_123", event)
# Returns triggered_biases, recommended_nudges, risk_factors, confidence
```

**Analysis Output Fields**:

| Field | Type | Description |
|-------|------|-------------|
| session_id | string | Unique identifier for this analysis session |
| user_id | string | User or session identifier |
| timestamp | ISO 8601 | When analysis was performed |
| triggered_biases | list | Detected biases with confidence scores |
| nudge_candidates | list | Nudge types derived from biases |
| recommended_nudges | list | Final nudge recommendations (bias + persona) |
| overall_confidence | float | Aggregate confidence score (0.0-1.0) |
| persona_matches | list | Matched personas with confidence |
| risk_factors | list | Bias-linked risk factors |
| suggested_interventions | list | Specific intervention recommendations |

### 2. Nudge Design

Design evidence-based nudges with automatic type selection, strength calibration, and success metrics.

```python
nudge = agent.design_nudge(
    trigger="checkout",
    behavior="purchase",
    context={"device": "mobile"},
    strength=0.7
)
# Returns nudge_id, description, expected_impact, implementation_notes
```

**Nudge Design Options**:

| Parameter | Required | Default | Options |
|-----------|----------|---------|---------|
| trigger | Yes | - | Any descriptive string |
| behavior | Yes | - | purchase, engagement, retention, etc. |
| context | No | {} | Arbitrary context dictionary |
| strength | No | 0.5 | 0.0 - 1.0 |
| nudge_type | No | Auto-selected | default_effect, social_norm, etc. |

### 3. Habit Loop Management

Create and reinforce habit loops with automatic strength adjustment and streak tracking.

```python
loop = agent.register_habit_loop(
    habit_name="daily_login",
    trigger="morning_push",
    behavior="open_app",
    reward="daily_reward",
    cadence="daily"
)
# Reinforce and watch loop_strength evolve
```

**Reinforcement Outcome Tracking**:

After each `reinforce_habit()` call:

- Success count updates (trigger + reward both given)
- Current streak increments or resets
- Max streak updates if current exceeds it
- Loop strength adjusts: +0.02 * reward_quality for success, -0.05 for break

### 4. A/B Testing

Run statistically rigorous experiments with automatic significance tracking.

```python
exp = agent.run_ab_test("button_test", "blue", "green", power=0.8, alpha=0.05)
# Record observations and close with automatic winner selection
```

**Experiment Methods**:

| Method | Purpose |
|--------|---------|
| `run_ab_test()` | Create new A/B test experiment |
| `record_experiment_observation()` | Add data point to experiment |
| `_compute_intermediate_experiment_stats()` | Compute current statistics |
| `close_ab_test()` | Finalize experiment and select winner |
| `validate_experiment_design()` | Check experiment parameters |

### 5. Persona Management

Use default personas or create custom behavioral profiles.

```python
profile = agent.create_persona_profile(
    "my_persona",
    traits={"impulsivity": 0.8, "deliberation": 0.2},
    behavioral_tendencies=["impulse_buying", "brand_switching"]
)
```

**Creating Effective Personas**:

- Base traits on research or observed data (not assumptions)
- Use 3-5 behavioral tendencies (too many reduces specificity)
- Write clear descriptions distinguishing from other personas
- Validate personas against actual session data
- Refine thresholds using `optimize_persona_thresholds()`

## API Usage

### Initialization

```python
from agents.behavioral-science.agent import BehavioralScienceAgent

# With defaults
agent = BehavioralScienceAgent()

# With custom config
agent = BehavioralScienceAgent(config_path="config.yaml")
```

### Full Workflow Example

```python
from agents.behavioral-science.agent import BehavioralScienceAgent
import random

agent = BehavioralScienceAgent()

# Analyze behavior
analysis = agent.analyze_behavior(
    user_id="user_001",
    event_data={
        "tags": ["checkout", "cart_abandon", "time_pressure"],
        "value": 129.99,
        "session_duration": 180
    }
)

# Design nudge based on analysis
nudge = agent.design_nudge(
    trigger="checkout",
    behavior="purchase",
    strength=0.65
)

# Create habit loop
loop = agent.register_habit_loop(
    habit_name="repeat_purchase",
    trigger="reorder_prompt",
    behavior="confirm_reorder",
    reward="loyalty_points",
    loop_strength=0.4
)

# Create incentive system
system = agent.create_incentive_system(
    name="Points Program",
    target_behaviors=["purchase", "review"],
    reward_type="points",
    reward_value=100,
    tracking_mechanism="point_based"
)

# Run experiment
exp = agent.run_ab_test("homepage_test", "control", "treatment", 0.8, 0.05)
for _ in range(200):
    agent.record_experiment_observation(
        exp["experiment_id"],
        random.choice(["control", "treatment"]),
        random.random() < 0.12
    )
results = agent.close_ab_test(exp["experiment_id"])
```

### Advanced Usage Patterns

#### Batch Processing

```python
# Analyze multiple users efficiently
user_ids = [f"user_{i}" for i in range(1, 101)]
results = agent.advanced_analysis(user_ids, analysis_type="comprehensive")
```

#### Pipeline Pattern

```python
# Build a complete behavioral pipeline
def behavioral_pipeline(agent, user_id, events):
    analyses = [agent.analyze_behavior(user_id, e) for e in events]
    nudges = [agent.design_nudge("pipeline", "engagement") for _ in analyses]
    return {"analyses": analyses, "nudges": nudges}
```

#### State Management

```python
# Export before major changes
agent.export_state("pre_deployment_backup.json")

# Make changes...

# Rollback if needed
new_agent = BehavioralScienceAgent()
new_agent.import_state("pre_deployment_backup.json")
```

## Configuration

### Full Config File Example

Create a `config.yaml` file:

```yaml
agent:
  version: "1.0.0"
  log_level: "INFO"
  data_retention_days: 90
  max_history_size: 10000

analysis:
  default_nudge_strength: 0.5
  analysis_timeout: 30
  confidence_threshold: 0.75
  bias_correction_enabled: true

experiments:
  default_power: 0.8
  default_alpha: 0.05
  minimum_sample_size: 1000
  peeking_correction: "bonferroni"

habits:
  default_cadence: "daily"
  loop_iterations: 21
  streak_bonus_threshold: 7

personas:
  max_segments: 20
  auto_discovery: false

integrations:
  webhook_timeout_seconds: 10
  max_retries: 3

security:
  pii_redaction_enabled: true
  encryption_at_rest: true
```

### Common Configurations

**Production deployment**:
```yaml
log_level: WARNING
max_history_size: 50000
data_retention_days: 180
bias_correction_enabled: true
confidence_threshold: 0.80
```

**Development / Testing**:
```yaml
log_level: DEBUG
max_history_size: 500
data_retention_days: 7
random_seed: 42
```

**High-Traffic Deployment**:
```yaml
max_history_size: 100000
enable_caching: true
analysis_timeout: 10
```

**Low-Resource Deployment**:
```yaml
max_history_size: 100
enable_caching: false
data_retention_days: 1
```

## Examples

### Example 1: Detect Biases in Checkout Flow

```python
agent = BehavioralScienceAgent()

cart_abandon_event = {
    "tags": ["checkout", "cart_abandon", "shipping_surprise", "pain_point"],
    "value": 149.99,
    "session_duration": 240,
    "context": {"steps_completed": 3, "steps_remaining": 2}
}

analysis = agent.analyze_behavior("user_456", cart_abandon_event)
print("Detected biases:", [b["bias"] for b in analysis["triggered_biases"]])
print("Recommended nudges:", analysis["recommended_nudges"])
print("Risk factors:", analysis["risk_factors"])
```

### Example 2: Batch Nudge Design for Marketing Campaign

```python
agent = BehavioralScienceAgent()

requests = [
    {"trigger": "homepage_visit", "behavior": "signup", "strength": 0.5, "nudge_type": "social_norm"},
    {"trigger": "browse", "behavior": "add_to_cart", "strength": 0.4, "nudge_type": "scarcity"},
    {"trigger": "cart_view", "behavior": "checkout", "strength": 0.6, "nudge_type": "default_effect"},
    {"trigger": "post_purchase", "behavior": "review", "strength": 0.3, "nudge_type": "reminders"},
    {"trigger": "checkout", "behavior": "share", "strength": 0.2, "nudge_type": "incentive_alignment"}
]

nudges = agent.batch_design_nudges(requests)
for n in nudges:
    print(f"{n['nudge_id']}: {n['nudge_type']} -> {n['target_behavior']}")
```

### Example 3: Cohort Retention Analysis

```python
cohort_data = {
    "0": 5000,
    "1": 3200,
    "3": 2800,
    "7": 2400,
    "14": 2100,
    "30": 1800,
    "60": 1500,
    "90": 1300
}

retention = agent.compute_cohort_retention("jan_2025_signups", cohort_data)
print(f"Day 1: {retention['day_1_retention']:.1%}")
print(f"Day 7: {retention['day_7_retention']:.1%}")
print(f"Day 30: {retention['day_30_retention']:.1%}")
```

### Example 4: Advanced Multi-User Analysis

```python
user_ids = [f"user_{i}" for i in range(1, 21)]
results = agent.advanced_analysis(user_ids, analysis_type="comprehensive")

total_biases = results["summary"]["total_biases_detected"]
total_nudges = results["summary"]["total_nudges_generated"]
print(f"Analyzed {results['user_count']} users")
print(f"Total biases detected: {total_biases}")
print(f"Total nudges generated: {total_nudges}")
```

### Example 5: State Persistence

```python
# Run some operations
agent = BehavioralScienceAgent()
for i in range(10):
    agent.analyze_behavior(f"user_{i}", {"tags": ["test"], "value": i * 10})

# Export
agent.export_state("behavioral_state_backup.json")

# Import into fresh agent
fresh_agent = BehavioralScienceAgent()
fresh_agent.import_state("behavioral_state_backup.json")
print(f"Restored {len(fresh_agent.session_history)} sessions")
```

### Example 6: Optimize Nudge Timing

```python
timing = agent.optimize_nudge_timing(
    user_id="user_123",
    nudge_id="nudge_83a1b2",
    time_windows=[
        {"start": "09:00", "end": "12:00"},
        {"start": "12:00", "end": "15:00"},
        {"start": "18:00", "end": "21:00"}
    ]
)
for window in timing["timing_recommendations"]:
    print(f"{window['start']}-{window['end']}: {window['expected_engagement_score']}")
```

### Example 7: Evaluate Nudge Performance

```python
performance = agent.evaluate_nudge_performance(
    nudge_id="nudge_abc1234",
    impressions=50000,
    clicks=2250,
    conversions=340,
    exposures_per_user=1.5
)
print(f"CTR: {performance['ctr']:.2%}")
print(f"CVR: {performance['cvr']:.2%}")
print(f"Status: {performance['status']}")
print(f"Effectiveness: {performance['effectiveness_score']:.2%}")
```

### Example 8: Habit Decay Detection

```python
decay = agent.detect_habit_decay(
    loop_id="loop_abc123",
    decay_threshold=0.3
)
if decay["decay_detected"]:
    print(f"Habit decay detected! Magnitude: {decay['decay_magnitude']}")
    print(f"Recommendation: {decay['recommendation']}")
else:
    print("No decay detected")
```

### Example 9: Power Analysis for Experiment Planning

```python
power = agent.compute_power_analysis(
    baseline_rate=0.10,
    minimum_detectable_effect=0.02,
    alpha=0.05,
    desired_power=0.8,
    ratio=1.0
)
print(f"Need {power['required_sample_size_per_group']} per group")
print(f"Total: {power['total_sample_size']}")
```

### Example 10: Generate User Segment Report

```python
report = agent.generate_user_segment_report(
    segment_filter={"since": "2025-01-01"},
    min_confidence=0.7
)
print("Top personas:", report["persona_distribution"])
print("Top biases:", report["bias_distribution"])
print("Top nudges:", report["nudge_distribution"])
```

## Troubleshooting

### Common Issues

**Import Errors**

Make sure you're running from the correct directory or have the project in your Python path.

```bash
# From project root
python -c "import sys; sys.path.insert(0, '.'); from agents.behavioral-science.agent import BehavioralScienceAgent"
```

**Empty Analysis Results**

If analyze_behavior returns no biases, check that your event_data.tags contain known trigger keywords. Add custom bias triggers or expand tag vocabulary.

**Experiment Stuck in Running State**

Ensure you're calling record_experiment_observation with correct variant names matching control_variant and treatment_variant exactly.

**High Memory Usage**

Reduce max_history_size in config or implement periodic session archival to external storage. Use reset_session() in long-running processes.

### Debug Mode

Enable debug logging:

```python
agent = BehavioralScienceAgent(config_path="config_dev.yaml")
# Or modify default_config:
# log_level: "DEBUG"
```

### Performance Tips

- Disable caching for debugging: `enable_caching: false`
- Reduce max_history_size for constrained environments
- Use batch_design_nudges for bulk operations
- Periodically call reset_session() in long-running services
- Export state to file rather than relying solely on in-memory storage

### Debugging Checklist

1. Verify event_data structure matches expected schema
2. Check that tags contain bias trigger keywords
3. Confirm config values are within valid ranges
4. Review session_history for unexpected entries
5. Validate experiment variant names match exactly
6. Check for exhausted history limits (max_history_size)
7. Verify file paths for import/export operations

### Error Reference

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| ValueError: event_data must not be empty | Empty dict passed | Provide valid event_data |
| ValueError: strength must be between 0.0 and 1.0 | Invalid strength parameter | Use float in [0.0, 1.0] |
| ValueError: loop_strength must be between 0.0 and 1.0 | Invalid habit strength | Use float in [0.0, 1.0] |
| KeyError: Nudge X not found | Invalid nudge_id | Use ID from nudge_library |
| KeyError: Experiment X not found | Invalid experiment_id | Use ID from experiment_registry |
| KeyError: Habit loop X not found | Invalid loop_id | Use ID from habit_loops |
| ValueError: variant must be either | Wrong variant name | Match control_variant or treatment_variant exactly |
| ValueError: p must be between 0 and 1 exclusive | Invalid probability | Use float in (0.0, 1.0) |
| FileNotFoundError: config path invalid | Config file missing | Create or correct config path |

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all public methods
- Include type hints for all function signatures
- Write tests for new functionality

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=agents/behavioral-science tests/

# Run specific test file
pytest tests/test_agent.py

# Run with verbose output
pytest -v tests/
```

### Pull Request Process

1. Update README.md with documentation for new features
2. Update GROK.md with any new capabilities
3. Add tests achieving >90% coverage for new code
4. Ensure ARCHITECTURE.md reflects any structural changes
5. Run full test suite before submitting

## License

MIT License - see LICENSE file for details.

## References

### Academic Papers

1. Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. Econometrica.
2. Thaler, R. H., & Sunstein, C. R. (2008). Nudge: Improving decisions about health, wealth, and happiness.
3. Lally, P., et al. (2010). How are habits formed: Modelling habit formation in the real world. European Journal of Social Psychology.
4. Cialdini, R. B. (2001). Influence: Science and practice. Allyn & Bacon.
5. Ajzen, I. (1991). The theory of planned behavior. Organizational Behavior and Human Decision Processes.
6. Duhigg, C. (2012). The power of habit: Why we do what we do in life and business. Random House.
7. Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. Science.
8. Ariely, D. (2008). Predictably irrational: The hidden forces that shape our decisions. HarperCollins.
9. Sherif, M. (1936). The psychology of social norms. Harper & Brothers.
10. Festinger, L. (1957). A theory of cognitive dissonance. Stanford University Press.

### Books

- Thinking, Fast and Slow - Daniel Kahneman
- Nudge - Richard Thaler and Cass Sunstein
- Predictably Irrational - Dan Ariely
- Influence - Robert Cialdini
- The Power of Habit - Charles Duhigg
- Atomic Habits - James Clear
- Hooked - Nir Eyal

### Online Resources

- Behavioral Economics: https://www.behavioraleconomics.com
- Nudge Theory: https://en.wikipedia.org/wiki/Nudge_theory
- Decision Science News: https://www.decisionsciencenews.com
- LessWrong: https://www.lesswrong.com

## Appendix

### Appendix A: Complete Method Signatures

```python
class BehavioralScienceAgent:
    def __init__(self, config_path: Optional[str] = None) -> None

    def analyze_behavior(self, user_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]
    def design_nudge(self, trigger: str, behavior: str, context: Optional[Dict[str, Any]] = None,
                     strength: Optional[float] = None, nudge_type: Optional[str] = None) -> Dict[str, Any]
    def register_habit_loop(self, habit_name: str, trigger: str, behavior: str, reward: str,
                            loop_strength: float = 0.5, cadence: str = "daily",
                            notes: Optional[str] = None) -> Dict[str, Any]
    def reinforce_habit(self, loop_id: str, reward_given: bool = True,
                        reward_quality: float = 1.0, trigger_occurred: bool = True,
                        metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
    def create_incentive_system(self, name: str, target_behaviors: List[str], reward_type: str,
                                reward_value: Union[int, float, str], eligibility_criteria: Optional[Dict[str, Any]] = None,
                                tracking_mechanism: str = "point_based", expiration_days: Optional[int] = None) -> Dict[str, Any]
    def run_ab_test(self, experiment_name: str, control_variant: str, treatment_variant: str,
                    power: float = 0.8, alpha: float = 0.05) -> Dict[str, Any]
    def record_experiment_observation(self, experiment_id: str, variant: str, converted: bool,
                                      metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
    def record_feedback(self, user_id: str, event_type: str, response_data: Dict[str, Any],
                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
    def create_persona_profile(self, persona_name: str, traits: Dict[str, float],
                               behavioral_tendencies: List[str], description: str = "") -> Dict[str, Any]
    def build_user_journey(self, user_id: str, journey_name: str, stages: List[Dict[str, Any]],
                           start_date: Optional[str] = None) -> Dict[str, Any]
    def evaluate_journey_stage(self, journey: Dict[str, Any], user_event: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[str]]
    def compute_journey_completion(self, journey: Dict[str, Any]) -> Dict[str, Any]
    def compute_cohort_retention(self, cohort_label: str, daily_active_user_counts: Dict[str, int]) -> Dict[str, Any]
    def simulate_behavior(self, user_id: str, scenario_type: str, parameters: Dict[str, Any],
                          iterations: int = 1000) -> Dict[str, Any]
    def optimize_nudge_timing(self, user_id: str, nudge_id: str,
                              time_windows: List[Dict[str, str]]) -> Dict[str, Any]
    def evaluate_nudge_performance(self, nudge_id: str, impressions: int, clicks: int, conversions: int,
                                   exposures_per_user: Optional[int] = None) -> Dict[str, Any]
    def tag_behavior_event(self, event_id: str, tags: List[str], confidence: float = 1.0,
                           metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
    def summarize_sessions(self, since: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]
    def recommend_intervention(self, user_id: str, current_state: Dict[str, Any],
                               recent_events: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]
    def batch_design_nudges(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]
    def advanced_analysis(self, user_ids: List[str], analysis_type: str = "comprehensive") -> Dict[str, Any]
    def compute_habit_predictions(self, loop_id: str, horizon_days: int = 30) -> Dict[str, Any]
    def close_ab_test(self, experiment_id: str, stopping_reason: str = "significance_reached") -> Dict[str, Any]
    def export_state(self, path: str) -> None
    def import_state(self, path: str) -> None
    def reset_session(self) -> Dict[str, Any]
    def get_nudge(self, nudge_id: str) -> Dict[str, Any]
    def get_experiment(self, experiment_id: str) -> Dict[str, Any]
    def get_habit_loop(self, loop_id: str) -> Dict[str, Any]
    def list_personas(self) -> List[str]
    def list_nudges(self) -> List[Dict[str, Any]]
    def list_experiments(self) -> List[Dict[str, Any]]
    def list_habit_loops(self) -> List[Dict[str, Any]]
    def run(self, user_input: Optional[str] = None) -> Dict[str, Any]
    def calculate_nudge_roi(self, nudge_id: str, cost_per_impression: float,
                            conversion_value: float, impressions: int, conversions: int) -> Dict[str, Any]
    def detect_behavioral_anomalies(self, user_id: str, event_sequence: List[Dict[str, Any]],
                                    sensitivity: float = 0.7) -> Dict[str, Any]
    def generate_user_segment_report(self, segment_filter: Optional[Dict[str, Any]] = None,
                                     min_confidence: float = 0.5) -> Dict[str, Any]
    def compute_power_analysis(self, baseline_rate: float, minimum_detectable_effect: float,
                               alpha: float = 0.05, desired_power: float = 0.8, ratio: float = 1.0) -> Dict[str, Any]
    def validate_experiment_design(self, control_variant: str, treatment_variant: str,
                                   power: float = 0.8, alpha: float = 0.05,
                                   minimum_sample_size: int = 1000) -> Dict[str, Any]
    def schedule_nudge(self, nudge_id: str, user_id: str, scheduled_at: str,
                       metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
    def cancel_nudge(self, schedule_id: str) -> Dict[str, Any]
    def get_behavioral_trends(self, metric: str = "bias_detection_rate", window_size: int = 7,
                              user_id: Optional[str] = None) -> Dict[str, Any]
    def export_audit_log(self, path: str, since: Optional[str] = None) -> None
    def import_audit_log(self, path: str) -> Dict[str, Any]
    def compute_bias_correlation_matrix(self) -> Dict[str, Any]
    def optimize_persona_thresholds(self, persona_name: str, target_precision: float = 0.9,
                                     max_iterations: int = 50) -> Dict[str, Any]
    def detect_habit_decay(self, loop_id: str, decay_threshold: float = 0.3) -> Dict[str, Any]
    def recommend_nudge_sequence(self, user_id: str, max_nudges: int = 3,
                                 strategy: str = "diversity") -> Dict[str, Any]
    def compute_intervention_effectiveness(self, intervention_id: str,
                                           pre_metrics: Dict[str, float],
                                           post_metrics: Dict[str, float]) -> Dict[str, Any]
    def get(self, item: str, default: Any = None) -> Any
    def __repr__(self) -> str
```

### Appendix B: Error Codes

| Error | Condition | Recovery |
|-------|-----------|----------|
| ValueError | Invalid parameter values | Validate inputs against constraints |
| KeyError | Resource not found (nudge, experiment, habit) | Check IDs before accessing |
| TypeError | Wrong data type passed | Strict type checking |
| OverflowError | Numerical computation overflow | Check input ranges |
| FileNotFoundError | State import/export path invalid | Verify file path exists |
| json.JSONDecodeError | Invalid JSON in state file | Validate JSON format before import |

### Appendix C: Related Projects

- **Awesome Grok Skills**: Parent repository of agents
- **Persuasive Technology**: Related field focused on attitude and behavior change through computing
- **Choice Architecture**: Design of environments that influence decision-making
- **Digital Behavior Change**: Application of behavioral science to digital products

### Appendix D: Roadmap

- [ ] Machine learning-based bias prediction
- [ ] Real-time nudge deployment adapter
- [ ] Dashboard for experiment visualization
- [ ] Integration with popular analytics platforms
- [ ] Multi-language support for nudge descriptions
- [ ] Advanced simulated user population testing
- [ ] Seasonal and trend-aware bias weighting
- [ ] Auto-generated experiment reports in PDF format

## Performance Guide

### Recommended Configurations by Scale

| Scale | Sessions/Day | max_history_size | Replicas | Memory per Instance |
|-------|--------------|------------------|----------|---------------------|
| Small | < 1,000 | 1,000 | 1 | 150 MB |
| Medium | 1,000 - 10,000 | 10,000 | 2-3 | 300 MB |
| Large | 10,000 - 100,000 | 50,000 | 3-5 | 500 MB |
| Enterprise | > 100,000 | 100,000 | 5+ | 1 GB |

### Benchmarking

```python
import time

agent = BehavioralScienceAgent()
start = time.time()
for i in range(1000):
    agent.analyze_behavior(f"user_{i}", {"tags": ["test"], "value": i})
elapsed = time.time() - start
print(f"1000 analyses in {elapsed:.2f}s ({1000/elapsed:.0f} ops/sec)")
```

## Security Considerations

### Data Privacy

- Always hash or pseudonymize user_id before processing
- Redact PII from event_data before ingestion
- Encrypt exported state files
- Audit all state access and modifications

### API Security

- Require authentication for all endpoints
- Use HTTPS for all communication
- Implement rate limiting per API key
- Rotate API keys regularly

### Compliance Notes

- Review nudge designs for jurisdictional compliance
- Document all data processing activities
- Provide user access to behavioral profiles
- Implement right-to-deletion workflows

## Frequently Asked Questions

**Q: Is this agent ethical to use?**

A: The agent is designed to support ethical, transparent behavior change. All nudges preserve freedom of choice and avoid manipulation. Review nudge designs for your specific context and jurisdiction.

**Q: Can I use this with my existing analytics data?**

A: Yes. Format your behavioral data to match the event schema described in GROK.md or ARCHITECTURE.md and pass it to analyze_behavior.

**Q: How accurate is bias detection?**

A: Bias detection uses rule-based trigger matching. Accuracy depends on comprehensive event tagging. For best results, tag events with behaviorally relevant keywords.

**Q: What if I get no biases detected?**

A: Expand your event_data.tags to include keywords from the bias trigger vocabulary. You can also customize the _check_bias_trigger method.

**Q: Do I need statistical background to run experiments?**

A: Basic understanding of A/B testing concepts helps. The agent handles statistical calculations automatically, but you should understand power, significance levels, and sample sizes.

**Q: Can I deploy this in production?**

A: Yes, with appropriate configuration, monitoring, and data governance policies. See ARCHITECTURE.md for deployment guidance.

**Q: What Python versions are supported?**

A: Python 3.8 and higher. Tested on 3.8, 3.9, 3.10, 3.11, and 3.12.

**Q: Is there a REST API?**

A: The core implementation is a Python library. For REST API deployment, wrap the methods in your preferred web framework (FastAPI, Flask, etc.). See ARCHITECTURE.md for API contract examples.

**Q: How do I extend the agent?**

A: See the Extension Guide in GROK.md. You can add biases, personas, nudge types, and custom methods without modifying core code.

**Q: What's the difference between a persona and a bias?**

A: Biases are cognitive tendencies detected from specific events. Personas are stable behavioral archetypes matched across sessions. An event can trigger multiple biases and match multiple personas simultaneously.
