# Behavioral Science Agent

## Overview

The Behavioral Science Agent is a sophisticated system designed to apply principles from behavioral economics, psychology, and decision science to analyze, predict, and influence human behavior. It integrates cognitive bias detection, persona-based segmentation, nudge design, habit loop modeling, A/B experimentation, and incentive system creation into a single coherent agentic workflow.

## Core Philosophy

This agent operates on the premise that human behavior is not purely rational, but influenced by systematic cognitive biases, environmental cues, social contexts, and emotional states. Instead of assuming users will act in their best interests given sufficient information, the agent designs interventions that account for how people actually behave.

The underlying philosophy follows three pillars:

- **Respect for Autonomy**: All nudges preserve user choice and avoid manipulation.
- **Transparency**: Every intervention is logged with rationale, bias linkage, and evidence path.
- **Iterative Learning**: Interventions improve over time through feedback, experimentation, and adaptation.

### Behavioral Economics Foundation

The agent is grounded in established behavioral economics frameworks:

- **Dual-Process Theory**: System 1 (fast, intuitive) vs System 2 (slow, deliberative) thinking
- **Prospect Theory**: People value gains and losses differently, with losses weighted ~2x gains
- **Bounded Rationality**: Decision-making is limited by available information, cognitive capacity, and time
- **Social Proof Theory**: People look to others' behavior to guide their own actions
- **Scarcity Heuristic**: Limited availability increases perceived value

### Ethical Guardrails

The agent implements several safeguards:

1. **No Dark Patterns**: Interventions avoid deceptive UI or manipulative framing
2. **Right to Opt Out**: All nudges include clear opt-out mechanisms
3. **Transparency**: Users can access their behavioral profiles and nudge history
4. **Least Intrusive Principle**: Agents select the minimally effective intervention first
5. **Bias Auditing**: Regular audits check for discriminatory outcomes across user segments

## Capabilities

### 1. Behavioral Analysis

The agent ingests behavioral events and produces structured analyses including detected cognitive biases, matched personas, risk factors, and recommended interventions.

**Sub-capabilities**:
- Bias detection across 10+ cognitive biases with confidence scoring
- Persona matching against 8 default behavioral archetypes
- Risk factor identification tied to specific biases
- Session-level behavior tracking and summarization
- Cohort retention analysis over arbitrary time windows
- User journey mapping with multi-stage drop-off detection
- Anomaly detection in behavioral sequences
- Trend analysis across bias, nudge, and experiment metrics

**Analysis Pipeline**:

```
Event Input -> Validation -> Bias Detection -> Persona Matching -> 
Nudge Recommendation -> Risk Scoring -> Session Storage -> Response
```

Each analysis produces:
- Session ID and timestamp
- List of triggered biases with confidence scores
- Candidate nudge types derived from biases
- Recommended nudges derived from persona matching
- Overall confidence score
- Identified risk factors
- Suggested interventions

### 2. Nudge Design

Creates targeted behavioral nudges tied to specific triggers and desired behaviors. Each nudge includes:

- **Type Selection**: Automatically selects the most effective nudge type based on behavior, context, and user profile
- **Strength Calibration**: Assigns a strength parameter (0.0 to 1.0) controlling nudge intensity
- **Implementation Notes**: Provides detailed guidance on deploying the nudge effectively
- **Success Metrics**: Defines measurable outcomes for evaluating effectiveness
- **Experiment Suggestions**: Recommends A/B tests, multivariate tests, and longitudinal studies
- **ROI Estimation**: Calculates expected return on investment
- **Scheduling Support**: Allows scheduling nudge delivery at optimal times

Supported nudge types include: default_effect, social_norm, commitment_device, reminders, simplification, framing, incentive_alignment, peer_comparison, friction_reduction, loss_aversion_framing, risk_reversal, default_safe_option, scarcity, progress_tracking, membership_benefits, ownership_framing, priming, testimonial_highlight, popularity_signals, limited_time, and limited_quantity.

**Nudge Design Process**:

1. User provides trigger, behavior, and optional context/strength/nudge_type
2. Agent selects nudge_type if not provided (based on behavior preferences)
3. Agent generates unique nudge_id using MD5 hash
4. Agent computes expected impact using base effectiveness * strength * variance
5. Agent generates implementation notes specific to nudge type
6. Agent defines 4 standard success metrics
7. Agent suggests 3 experiment designs
8. Nudge stored in nudge_library for later retrieval and evaluation

### 3. Cognitive Bias Index

The agent maintains an indexed catalog of cognitive biases with descriptions, applicable nudge strategies, and risk scores.

**Included Biases**:

| Bias | Description | Applicable Nudges | Risk Score |
|------|-------------|-------------------|------------|
| anchoring | Heavy influence by first encountered information | price_anchoring, reference_point_setting | 0.7 |
| confirmation | Seeks evidence confirming pre-existing beliefs | belief_consistent_framing, selective_evidence | 0.6 |
| availability | Overestimates probability of easily recalled events | priming, vivid_examples | 0.5 |
| loss_aversion | Prefers avoiding losses over acquiring equivalent gains | loss_framing, risk_reversal, default_safe_option | 0.8 |
| endowment | Values things more once owned | free_trial, preview, ownership_framing | 0.6 |
| sunk_cost | Continues behavior due to invested resources | progress_tracking, milestone_rewards | 0.7 |
| bandwagon | Does something because others are doing it | social_norm, popularity_signals | 0.6 |
| framing | Different conclusions from same information, based on presentation | positive_framing, negative_framing | 0.55 |
| social_proof | Looks to others to determine correct behavior | testimonials, user_counts, ratings | 0.5 |
| scarcity | Higher value placed on scarce resources | limited_time, limited_quantity, countdown | 0.75 |

**Bias Interaction Patterns**:

Certain biases frequently co-occur. The agent computes a bias correlation matrix to identify these patterns:

- Loss aversion + framing: Often simultaneously active in pricing decisions
- Anchoring + availability: Initial price exposure makes similar products more "available"
- Social proof + bandwagon: Reinforce each other in group settings
- Endowment + sunk cost: Ownership increases commitment to prior investment

### 4. Persona Segmentation

The agent includes 8 default behavioral personas, each with triggers, risk factors, and recommended nudges. Custom personas can be created with trait profiles and behavioral tendencies.

**Default Personas**:

| Persona | Description | Key Triggers | Recommended Nudges |
|---------|-------------|--------------|-------------------|
| impulsive_spender | Quick purchase decisions driven by emotion | limited_time_offer, flash_sale, countdown_timer | scarcity, social_proof, friction_reduction |
| deliberate_planner | Researches options thoroughly before acting | comparison_charts, detailed_specs, reviews | commitment_device, progress_tracking, simplification |
| social_adaptor | Heavily influenced by peers and social norms | peer_reviews, social_proof, community_ratings | social_norm, peer_comparison, testimonial_highlight |
| risk_averse | Avoids loss and uncertainty | guarantees, warranty_info, return_policy | loss_aversion_framing, risk_reversal, default_safe_option |
| novelty_seeker | Enjoys new experiences and products | new_arrivals, trending, early_access | scarcity, exclusivity, gamification |
| price_sensitive | Prioritizes cost savings and discounts | coupons, price_drops, bulk_discounts | anchoring_discount, bundle_value, loyalty_points |
| brand_loyal | Sticks to familiar and trusted brands | brand_story, heritage, repeat_purchase_rewards | exclusivity, membership_benefits, brand_community |
| convenience_driven | Values speed and ease above all | express_checkout, one_click, auto_reorder | simplification, friction_reduction, auto_fill |

**Custom Persona Creation**:

Users can define custom personas by specifying:

- **Persona name**: Unique identifier
- **Traits**: Dictionary of behavioral traits (impulsivity, price_sensitivity, social_influence, risk_tolerance, novelty_seeking, habit_strength, deliberation, loss_aversion)
  - Each trait value: 0.0 to 1.0
- **Behavioral tendencies**: List of behavioral patterns (procrastination, brand_switching, comparison_shopping, content_consumption, etc.)
- **Description**: Human-readable description

The agent automatically derives recommended nudges and risk factors from trait profiles using rule-based mappings.

**Persona Matching Algorithm**:

1. Serialize event_data to lowercase string
2. Search for persona trigger keywords (+1.0 per match)
3. Search for risk factor keywords (+0.5 per match)
4. Return match if total score >= 1.0 threshold
5. All matching personas returned with confidence scores

### 5. Habit Loop Management

Implements the cue-routine-reward framework based on Duhigg's habit loop model and Lally's habit formation research.

**Features**:
- Register habit loops with cue, routine, reward, cadence, and strength
- Track reinforcement history with reward quality and timing
- Monitor streaks, break attempts, and success counts
- Predict future habit execution probability over time horizons
- Build statistics including success rate, trigger rate, and average reward quality
- Adjust loop_strength dynamically based on reinforcement outcomes
- Detect habit decay patterns early

**Supported cadences**: hourly, daily, weekly, biweekly, monthly, variable

**Habit Formation Timeline**:

Based on Lally et al. (2010), habit formation averages 66 days but ranges from 18 to 254 days. The agent models this as:

```
Day 1-7:   Awareness phase - high cognitive load, low automation
Day 8-21:  Formation phase - decreasing cognitive load, increasing automation
Day 22-66: Stabilization phase - high context-response binding
Day 66+:   Maintenance phase - low cognitive load, high resistance to extinction
```

**Reinforcement Schedule Optimization**:

The agent recommends reinforcement schedules based on habit strength:

- Weak habit (0.0 - 0.3): Continuous reinforcement (every occurrence)
- Forming habit (0.3 - 0.6): Variable ratio schedule (70% of occurrences)
- Strong habit (0.6 - 0.8): Variable interval schedule (every 2-3 occurrences)
- Stable habit (0.8 - 1.0): Maintenance schedule (weekly check-ins)

**Decay Detection**:

- Compares success rate in recent 7 records vs previous 7 records
- Decay_magnitude = older_success_rate - recent_success_rate
- If decay_magnitude > decay_threshold (default 0.3), decay_detected = True
- System recommends increasing reward salience or simplifying cue-response pathway

### 6. Incentive System Design

Creates behavior-based incentive programs with multiple reward types and anti-gaming safeguards.

**Supported reward types**: monetary, points, badge, status, access, discount, donation, charity

**Features**:
- Define eligibility criteria and tracking mechanisms
- Generate automated incentive rules for target behaviors
- Include streak bonuses and cooldown periods
- Built-in anti-gaming measures: rate limits, fraud detection, validation checks, graduated penalties
- Track enrollment, redemption, and total value distributed
- Calculate ROI and break-even analysis

**Reward Type Selection Guide**:

| Use Case | Best Reward Type | Rationale |
|----------|------------------|-----------|
| Immediate behavior change | monetary | Highest effectiveness, clear value |
| Long-term engagement | points | Token economy supports sustained participation |
| Achievement motivation | badge | Low cost, high symbolic value |
| Status-driven users | status | Taps into social hierarchy needs |
| Exclusive experiences | access | Leverages scarcity principle |
| Price-sensitive segments | discount | Directly addresses cost concerns |
| Socially-minded users | donation | Warm glow effect, altruism signaling |

**Anti-Gaming Measures**:

Every incentive system includes:

1. **Rate Limits**: Hourly (10), daily (50), weekly (200) caps
2. **Fraud Detection**: Pattern analysis, velocity checks, device fingerprinting, IP monitoring
3. **Validation Checks**: Behavior completion verification, unique event deduplication, session integrity
4. **Graduated Penalties**: Warning -> points freeze (24h) -> account review

### 7. A/B Testing and Experimentation

Runs controlled experiments with full statistical rigor including p-value calculation, effect size estimation (Cohen's h), confidence intervals, power analysis, and multiple comparison corrections.

**Experiment types supported**:
- A/B tests (two-variant comparison)
- Multivariate tests (multiple factors and interactions)
- Time-series experiments (longitudinal validation)
- Cohort retention analysis

**Statistical methods**:
- Two-proportion z-test with normal approximation
- Bonferroni correction for multiple comparisons
- Confidence interval computation using normal distribution
- Effect size calculation using Cohen's h formula
- Sample size guidance based on desired power and significance level
- Power analysis for pre-launch sample sizing

**Experiment Lifecycle Management**:

1. **Design Phase**: Define variants, power, alpha, minimum sample size
2. **Validation Phase**: Validate design parameters, check for common errors
3. **Launch Phase**: Start experiment, begin observation recording
4. **Monitor Phase**: Track intermediate results, detect early significance
5. **Analyze Phase**: Compute final statistics, determine winner
6. **Report Phase**: Document findings, recommend actions, archive results

**Stopping Rules**:

- Significance reached: p-value < alpha (with Bonferroni correction)
- Sample size met: Both groups reach minimum sample size
- Time limit: Maximum runtime exceeded
- Manual stop: User-initiated termination

**Interpretation Guidelines**:

| Outcome | Action |
|---------|--------|
| Significant, positive lift | Roll out treatment variant |
| Significant, negative lift | Reject treatment, investigate causes |
| Not significant, p > 0.1 | Extend experiment or accept null hypothesis |
| Not significant, 0.05 < p < 0.1 | Consider extending with more samples |
| Effect size < 0.2 | Statistically significant but practically insignificant |

### 8. Feedback Collection and Analysis

Captures and categorizes user feedback to inform intervention refinement.

**Feedback categories**: speed, clarity, pricing, design, support, recommendation_quality, general

**Features**:
- Sentiment estimation using keyword-based analysis
- Automatic categorization into behavioral taxonomy
- Sentiment tracking and trend analysis over time
- Feedback linkage to specific nudges and experiments
- Batch import/export of feedback data

**Sentiment Analysis Details**:

The _estimate_sentiment method:

1. Serializes response_data to lowercase string
2. Counts positive keywords (great, love, amazing, helpful, easy, perfect)
3. Counts negative keywords (bad, hate, terrible, confusing, annoying, hard)
4. Returns "positive" if score > 0, "negative" if score < 0, "neutral" otherwise

**Feedback-to-Insight Pipeline**:

```
Raw Feedback -> Sentiment Classification -> Category Tagging ->
Aggregation -> Trend Detection -> Intervention Recommendations
```

### 9. User Journey Mapping

Tracks multi-stage user journeys identifying bottlenecks and intervention opportunities.

**Features**:
- Define stages with required event sequences
- Track stage transitions with timestamps and trigger events
- Identify primary drop-off points
- Compute journey completion rates
- Provide behavioral insights tied to journey stages
- Recommend nudges at transition points

**Journey Stage Schema**:

```json
{
  "stage_name": "landing",
  "required_events": ["page_view"],
  "nudge_hint": "simplification",
  "timeout_seconds": 30,
  "success_criteria": {},
  "fallback_stage": null
}
```

**Drop-off Analysis**:

The agent identifies drop-off points by tracking stage transitions:

1. Count transitions from each stage
2. Stage with highest transition count is primary attrition point
3. Insight message generated: "Primary attrition at stage X of Y"
4. Recommendations generated for high-attrition stages

### 10. Timing Optimization

Recommends optimal deployment windows for nudges based on expected engagement scores.

**Features**:
- Evaluate multiple time windows for a nudge
- Score each window based on expected engagement
- Identify optimal window with clear recommendation
- Supports custom window definitions with start/end times
- Considers user timezone and historical activity patterns

**Timing Evaluation Process**:

1. User provides time_windows list with start/end times
2. Agent evaluates each window:
   - Simulates engagement score based on random distribution (configured bounds)
   - Considers user's historical activity patterns if available
   - Factors in nudge type (some nudges work better at specific times)
3. Returns ranked list of windows with scores
4. Best window marked as recommended

### 11. Nudge Performance Evaluation

Evaluates deployed nudges against key performance indicators.

**Metrics tracked**:
- Click-through rate (CTR)
- Conversion rate (CVR)
- Cost per mille (CPM)
- Cost per click (CPC)
- Lift score vs baseline
- Effectiveness score (actual vs expected)
- Status classification: high_performing, moderate, underperforming

**Performance Thresholds**:

| Status | CTR Threshold | Action |
|--------|---------------|--------|
| high_performing | > 10% | Scale exposure, test other segments |
| moderate | 4% - 10% | Iterate on creative, analyze segments |
| underperforming | < 4% | Review design, test alternative framing |

**Effectiveness Computation**:

```
effectiveness = actual_conversions / (expected_impact * impressions)
```

Clamped to [0.0, 1.0]. Score > 0.7 indicates strong performance; < 0.3 indicates need for redesign.

### 12. State Management

Provides full import/export and reset capabilities for agent state.

**Exported state includes**: config, nudge_library, behavior_profiles, session_history, experiment_registry, habit_loops, incentive_systems, persona_segments, intervention_log, cognitive_biases_index, feedback_data, pattern_cache.

**Export Format**:

```json
{
  "config": {},
  "nudge_library": {},
  "behavior_profiles": {},
  "session_history": [],
  "experiment_registry": {},
  "habit_loops": {},
  "incentive_systems": {},
  "persona_segments": {},
  "intervention_log": [],
  "cognitive_biases_index": {},
  "feedback_data": [],
  "pattern_cache": {},
  "exported_at": "ISO 8601 timestamp"
}
```

**Import Behavior**:

1. Reads JSON file
2. Merges with current state (existing keys preserved if not in import)
3. Validates structure of imported objects
4. Updates all in-memory stores
5. Returns confirmation with imported counts

**Reset Operations**:

The reset_session method clears:
- session_history
- intervention_log
- feedback_data
- pattern_cache

Persistent data (config, nudge_library, habit_loops, etc.) is preserved.

## Usage

### Basic Setup

```python
from agents.behavioral-science.agent import BehavioralScienceAgent

# Initialize with optional config path
agent = BehavioralScienceAgent(config_path="config.yaml")

# Or use defaults
agent = BehavioralScienceAgent()
```

### Analyze Behavior

```python
event_data = {
    "tags": ["checkout", "cart_abandon", "loss_aversion_message_shown"],
    "session_duration": 145,
    "value": 79.99,
    "context": {"device": "mobile", "referrer": "email_campaign"}
}

result = agent.analyze_behavior(user_id="user_123", event_data=event_data)
print(result["triggered_biases"])
print(result["recommended_nudges"])
```

### Design a Nudge

```python
nudge = agent.design_nudge(
    trigger="checkout",
    behavior="purchase",
    context={"device": "mobile"},
    strength=0.6,
    nudge_type="default_effect"
)
print(nudge["nudge_id"], nudge["description"], nudge["expected_impact"])
```

### Create a Habit Loop

```python
loop = agent.register_habit_loop(
    habit_name="daily_purchase",
    trigger="push_notification_morning",
    behavior="open_app_and_browse",
    reward="loyalty_points",
    loop_strength=0.5,
    cadence="daily",
    notes="Target morning engagement cohort"
)

# Reinforce the habit after completion
result = agent.reinforce_habit(
    loop_id=loop["loop_id"],
    reward_given=True,
    reward_quality=0.9,
    trigger_occurred=True
)
```

### Build an Incentive System

```python
system = agent.create_incentive_system(
    name="Summer Rewards 2024",
    target_behaviors=["purchase", "review", "referral"],
    reward_type="points",
    reward_value=50,
    tracking_mechanism="point_based",
    expiration_days=90
)
```

### Run an A/B Experiment

```python
experiment = agent.run_ab_test(
    experiment_name="purchase_nudge_test",
    control_variant="old_checkout",
    treatment_variant="new_checkout_with_nudge",
    power=0.8,
    alpha=0.05
)

# Record observations
for _ in range(100):
    variant = random.choice(["old_checkout", "new_checkout_with_nudge"])
    converted = random.random() < (0.12 if variant == "new_checkout_with_nudge" else 0.10)
    agent.record_experiment_observation(experiment["experiment_id"], variant, converted)

# Close the experiment
results = agent.close_ab_test(experiment["experiment_id"])
print(results["recommended_winner"], results["final_stats"])
```

### Create Persona Profile

```python
profile = agent.create_persona_profile(
    persona_name="weekend_shopper",
    traits={
        "impulsivity": 0.7,
        "price_sensitivity": 0.4,
        "social_influence": 0.3,
        "risk_tolerance": 0.5,
        "novelty_seeking": 0.6,
        "habit_strength": 0.3,
        "deliberation": 0.2,
        "loss_aversion": 0.5
    },
    behavioral_tendencies=["comparison_shopping", "content_consumption"],
    description="Shops primarily on weekends with low deliberation time"
)
```

### Create a User Journey

```python
journey = agent.build_user_journey(
    user_id="user_123",
    journey_name="onboarding_flow",
    stages=[
        {"stage_name": "landing", "required_events": ["page_view"]},
        {"stage_name": "signup", "required_events": ["form_submit"], "nudge_hint": "simplification"},
        {"stage_name": "first_action", "required_events": ["button_click"], "nudge_hint": "commitment_device"},
        {"stage_name": "engagement", "required_events": ["content_interaction"], "nudge_hint": "social_norm"}
    ]
)

# Evaluate next stage
advance, nudge_hint = agent.evaluate_journey_stage(journey, {"button_click": True})
completion = agent.compute_journey_completion(journey)
```

### Compute Cohort Retention

```python
daily_counts = {
    "0": 1000,
    "1": 650,
    "7": 420,
    "30": 280
}
retention = agent.compute_cohort_retention("signup_week_23", daily_counts)
print(retention["day_1_retention"], retention["day_30_retention"])
```

### Track Feedback

```python
feedback = agent.record_feedback(
    user_id="user_123",
    event_type="nudge_dismissal",
    response_data={"reason": "too_persistent", "rating": 2},
    context={"nudge_id": "nudge_83a1b2"}
)
```

### Export and Import State

```python
# Export all state
agent.export_state("behavioral_agent_backup.json")

# Import state in new instance
new_agent = BehavioralScienceAgent()
new_agent.import_state("behavioral_agent_backup.json")

# Reset session history
agent.reset_session()
```

### Run the Agent

```python
result = agent.run(user_input="Analyze checkout abandonment patterns")
```

### Batch Nudge Design

```python
requests = [
    {"trigger": "checkout", "behavior": "purchase", "strength": 0.7},
    {"trigger": "onboarding", "behavior": "engagement", "strength": 0.5},
    {"trigger": "empty_cart", "behavior": "review", "strength": 0.4}
]
nudges = agent.batch_design_nudges(requests)
```

### Advanced Analysis

```python
results = agent.advanced_analysis(
    user_ids=["user_1", "user_2", "user_3"],
    analysis_type="comprehensive"
)
```

### Habit Prediction

```python
predictions = agent.compute_habit_predictions(
    loop_id="loop_abc123",
    horizon_days=30
)
```

### Optimize Nudge Timing

```python
timing = agent.optimize_nudge_timing(
    user_id="user_123",
    nudge_id="nudge_83a1b2",
    time_windows=[
        {"start": "09:00", "end": "12:00"},
        {"start": "12:00", "end": "15:00"},
        {"start": "15:00", "end": "18:00"}
    ]
)
```

### Evaluate Nudge Performance

```python
performance = agent.evaluate_nudge_performance(
    nudge_id="nudge_83a1b2",
    impressions=10000,
    clicks=450,
    conversions=67,
    exposures_per_user=2
)
```

### Compute Cohort Retention

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

### Compute Power Analysis

```python
power = agent.compute_power_analysis(
    baseline_rate=0.10,
    minimum_detectable_effect=0.02,
    alpha=0.05,
    desired_power=0.8
)
print(f"Required sample size per group: {power['required_sample_size_per_group']}")
```

### Schedule a Nudge

```python
scheduled = agent.schedule_nudge(
    nudge_id="nudge_83a1b2",
    user_id="user_123",
    scheduled_at="2025-01-15T14:00:00Z",
    metadata={"campaign": "checkout_optimization"}
)
```

### Detect Behavioral Anomalies

```python
anomalies = agent.detect_behavioral_anomalies(
    user_id="user_123",
    event_sequence=[...],
    sensitivity=0.7
)
```

### Compute Bias Correlation Matrix

```python
correlation = agent.compute_bias_correlation_matrix()
```

### Recommend Nudge Sequence

```python
sequence = agent.recommend_nudge_sequence(
    user_id="user_123",
    max_nudges=3,
    strategy="diversity"
)
```

### Compute Intervention Effectiveness

```python
effectiveness = agent.compute_intervention_effectiveness(
    intervention_id="intervention_abc",
    pre_metrics={"conversion_rate": 0.10, "avg_order_value": 50.0},
    post_metrics={"conversion_rate": 0.12, "avg_order_value": 55.0}
)
```

## Command Line Interface

### Basic Execution

```bash
python agents/behavioral-science/agent.py
```

### With Custom Configuration

```bash
python agents/behavioral-science/agent.py --config /path/to/config.yaml
```

### Expected CLI Output

```
[INFO] BehavioralScience Agent initialized
[INFO] Config loaded from default
[INFO] 8 personas registered
[INFO] 10 biases indexed
[INFO] Running default analysis cycle
[INFO] Session ID: a1b2c3d4e5f6g7h8
[INFO] Analysis complete: 2 biases detected, 3 nudges recommended
[INFO] Agent run completed successfully
```

### Argument Reference

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| --config | No | None | Path to YAML/JSON configuration file |
| --user-id | No | system | User ID for analysis |
| --input | No | None | JSON string or file path for event_data |
| --output | No | None | File path for JSON output |
| --log-level | No | INFO | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| --seed | No | 42 | Random seed for reproducibility |

## Configuration

### Default Configuration

The agent ships with a comprehensive default configuration covering all modules:

```yaml
default_nudge_strength: 0.5
analysis_timeout: 30
confidence_threshold: 0.75
max_persona_segments: 10
habit_loop_iterations: 21
experiment_significance_level: 0.05
data_retention_days: 90
enable_caching: true
log_level: INFO
max_history_size: 1000
bias_correction_enabled: true
random_seed: 42
```

### Supported Configuration Keys

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| default_nudge_strength | float | 0.5 | Default strength for designed nudges |
| analysis_timeout | int | 30 | Timeout in seconds for analysis operations |
| confidence_threshold | float | 0.75 | Minimum confidence for recommending interventions |
| max_persona_segments | int | 10 | Maximum registered persona segments |
| habit_loop_iterations | int | 21 | Default iterations for habit tracking |
| experiment_significance_level | float | 0.05 | Alpha level for statistical tests |
| data_retention_days | int | 90 | Days to retain session and feedback data |
| enable_caching | bool | true | Enable internal pattern caching |
| log_level | str | INFO | Logging verbosity |
| max_history_size | int | 1000 | Maximum session/fedback records in memory |
| bias_correction_enabled | bool | true | Enable bias detection |
| random_seed | int | 42 | Seed for reproducibility in simulations |

### Advanced Configuration Options

```yaml
bias_detection:
  confidence_bounds:
    min: 0.5
    max: 0.99
  co_occurrence_threshold: 0.3

habit_loops:
  default_cadence: "daily"
  streak_bonus_threshold: 7
  decay_detection_window: 14
  reinforcement_cap: 100

incentive_systems:
  default_reward_types: ["points", "monetary", "badge"]
  anti_gaming_enabled: true
  rate_limit_hourly: 10

experiments:
  default_power: 0.8
  default_alpha: 0.05
  minimum_sample_size: 1000
  peeking_correction: "bonferroni"
  auto_conclude_on_significance: true

personas:
  max_segments: 10
  auto_discovery: false
  similarity_threshold: 0.75
  matching_threshold: 1.0

journeys:
  max_stages: 20
  default_stage_timeout: 30

nudges:
  max_per_user: 5
  default_ttl_hours: 72
  performance_evaluation_window: 7

security:
  pii_redaction_enabled: true
  encryption_at_rest: true
  audit_logging: true
  required_scopes:
    analyze: behavioral:read
    design: behavioral:write
    experiment: experiments:write
```

## API Reference

### Core Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| analyze_behavior | user_id, event_data | Dict | Full behavioral analysis |
| design_nudge | trigger, behavior, context, strength, nudge_type | Dict | Creates a nudge |
| register_habit_loop | habit_name, trigger, behavior, reward, loop_strength, cadence, notes | Dict | Registers a habit loop |
| reinforce_habit | loop_id, reward_given, reward_quality, trigger_occurred, metadata | Dict | Records habit reinforcement |
| create_incentive_system | name, target_behaviors, reward_type, reward_value, eligibility_criteria, tracking_mechanism, expiration_days | Dict | Creates incentive system |
| run_ab_test | experiment_name, control_variant, treatment_variant, power, alpha | Dict | Starts an A/B experiment |
| record_experiment_observation | experiment_id, variant, converted, metadata | Dict | Records experiment data point |
| record_feedback | user_id, event_type, response_data, context | Dict | Records user feedback |
| create_persona_profile | persona_name, traits, behavioral_tendencies, description | Dict | Creates custom persona |
| build_user_journey | user_id, journey_name, stages, start_date | Dict | Creates user journey |
| evaluate_journey_stage | journey, user_event | Tuple[Dict, Optional[str]] | Evaluates journey progress |
| compute_cohort_retention | cohort_label, daily_active_user_counts | Dict | Compute retention curve |
| simulate_behavior | user_id, scenario_type, parameters, iterations | Dict | Monte Carlo simulation |
| optimize_nudge_timing | user_id, nudge_id, time_windows | Dict | Optimize delivery timing |
| evaluate_nudge_performance | nudge_id, impressions, clicks, conversions, exposures_per_user | Dict | Evaluate nudge ROI |
| tag_behavior_event | event_id, tags, confidence, metadata | Dict | Tag behavioral event |
| summarize_sessions | since, user_id | Dict | Aggregate session statistics |
| recommend_intervention | user_id, current_state, recent_events | Dict | Generate intervention plan |
| batch_design_nudges | requests | List[Dict] | Batch nudge creation |
| advanced_analysis | user_ids, analysis_type | Dict | Multi-user analysis |
| compute_habit_predictions | loop_id, horizon_days | Dict | Predict habit trajectories |
| close_ab_test | experiment_id, stopping_reason | Dict | Conclude experiment |
| calculate_nudge_roi | nudge_id, cost_per_impression, conversion_value, impressions, conversions | Dict | Compute nudge ROI |
| detect_behavioral_anomalies | user_id, event_sequence, sensitivity | Dict | Detect anomalies |
| generate_persona_report | persona_name, max_insights | Dict | Generate persona insights |
| compute_power_analysis | baseline_rate, minimum_detectable_effect, alpha, desired_power | Dict | Sample size estimation |
| validate_experiment_design | control_variant, treatment_variant, power, alpha, minimum_sample_size | Dict | Validate experiment |
| schedule_nudge | nudge_id, user_id, scheduled_at, metadata | Dict | Schedule nudge delivery |
| cancel_nudge | schedule_id | Dict | Cancel scheduled nudge |
| get_behavioral_trends | metric, window_size, user_id | Dict | Trend analysis |
| export_audit_log | path, since | None | Export audit trail |
| import_audit_log | path | Dict | Import audit trail |
| compute_bias_correlation_matrix | - | Dict | Bias co-occurrence analysis |
| optimize_persona_thresholds | persona_name, target_precision, max_iterations | Dict | Optimize matching |
| detect_habit_decay | loop_id, decay_threshold | Dict | Detect decay patterns |
| recommend_nudge_sequence | user_id, max_nudges, strategy | Dict | Generate sequence |
| compute_intervention_effectiveness | intervention_id, pre_metrics, post_metrics | Dict | Measure effectiveness |

### Convenience Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| get_nudge | nudge_id | Dict | Retrieve nudge by ID |
| get_experiment | experiment_id | Dict | Retrieve experiment by ID |
| get_habit_loop | loop_id | Dict | Retrieve habit loop by ID |
| list_personas | None | List[str] | List all personas |
| list_nudges | None | List[Dict] | List all nudges |
| list_experiments | None | List[Dict] | List all experiments |
| list_habit_loops | None | List[Dict] | List all habit loops |
| summarize_sessions | since, user_id | Dict | Aggregate session statistics |
| reset_session | None | Dict | Clear in-memory history |
| export_state | path | None | Export state to JSON |
| import_state | path | None | Import state from JSON |

## Data Models

### Nudge Object

```json
{
  "nudge_id": "string",
  "trigger": "string",
  "target_behavior": "string",
  "nudge_type": "string",
  "strength": 0.0,
  "context": {},
  "created_at": "ISO 8601 timestamp",
  "status": "draft",
  "description": "string",
  "expected_impact": 0.0,
  "implementation_notes": [],
  "success_metrics": [],
  "related_nudges": [],
  "experiment_suggestions": []
}
```

### Experiment Object

```json
{
  "experiment_id": "string",
  "name": "string",
  "control_variant": "string",
  "treatment_variant": "string",
  "power": 0.0,
  "alpha": 0.0,
  "status": "running",
  "started_at": "ISO 8601",
  "ended_at": "ISO 8601 or null",
  "control_group_size": 0,
  "treatment_group_size": 0,
  "control_conversions": 0,
  "treatment_conversions": 0,
  "significance_achieved": false,
  "p_value": 0.0 or null,
  "effect_size": 0.0 or null,
  "confidence_interval": [],
  "recommended_winner": "string or null",
  "stopping_reason": "string or null",
  "intermediate_results": []
}
```

### Habit Loop Object

```json
{
  "loop_id": "md5-derived-unique-id",
  "habit_name": "string",
  "cue": "string",
  "routine": "string",
  "reward": "string",
  "loop_strength": 0.5,
  "cadence": "daily",
  "notes": "string",
  "created_at": "ISO 8601",
  "status": "active",
  "reinforcement_history": [],
  "break_attempts": 0,
  "success_count": 0,
  "current_streak": 0,
  "max_streak": 0,
  "predictions": []
}
```

### Persona Profile Object

```json
{
  "profile_id": "string",
  "persona_name": "string",
  "traits": {},
  "behavioral_tendencies": [],
  "description": "string",
  "created_at": "ISO 8601",
  "updated_at": "ISO 8601",
  "sample_size": 0,
  "confidence_score": 0.0,
  "recommended_nudges": [],
  "risk_factors": [],
  "example_events": []
}
```

### Incentive System Object

```json
{
  "system_id": "md5-derived-unique-id",
  "name": "string",
  "target_behaviors": ["list"],
  "reward_type": "points",
  "reward_value": 100,
  "eligibility_criteria": {},
  "tracking_mechanism": "point_based",
  "expiration": {
    "days": 365,
    "expiration_date": "ISO 8601 or null"
  },
  "created_at": "ISO 8601",
  "status": "active",
  "enrollment_count": 0,
  "redemption_count": 0,
  "total_value_distributed": 0.0,
  "rules": [],
  "anti_gaming_measures": {}
}
```

### Session Analysis Object

```json
{
  "session_id": "string",
  "user_id": "string",
  "timestamp": "ISO 8601",
  "triggered_biases": [],
  "nudge_candidates": [],
  "recommended_nudges": [],
  "overall_confidence": 0.0,
  "persona_matches": [],
  "risk_factors": [],
  "suggested_interventions": []
}
```

## Extension Guide

### Adding a New Bias

```python
agent.cognitive_biases_index["new_bias"] = {
    "description": "Description of the new bias",
    "applicable_nudges": ["nudge_type_1", "nudge_type_2"],
    "risk": 0.6
}

# Add trigger conditions in _check_bias_trigger method by extending:
# bias_triggers["new_bias"] = ["trigger_keyword_1", "trigger_keyword_2"]
```

### Adding a Custom Persona

```python
profile = agent.create_persona_profile(
    persona_name="my_custom_persona",
    traits={"impulsivity": 0.3, "price_sensitivity": 0.8},
    behavioral_tendencies=["deal_hunting", "comparison_shopping"],
    description="Detailed description of this persona"
)
```

### Adding a New Nudge Type

1. Add description in `_describe_nudge`:
   ```python
   "new_nudge_type": "Description of what this nudge does."
   ```
2. Add base effectiveness in `_estimate_impact`:
   ```python
   "new_nudge_type": 0.15
   ```
3. Add implementation notes in `_implementation_notes`:
   ```python
   "new_nudge_type": [
       "Note 1 for implementation",
       "Note 2 for best practices",
       "Note 3 for measurement"
   ]
   ```
4. Add preference candidates in `_select_nudge_type` for relevant behaviors:
   ```python
   "target_behavior": ["new_nudge_type", "existing_nudge_type"]
   ```

### Custom Bias Trigger Logic

Override `_check_bias_trigger` to implement domain-specific logic:

```python
def _check_bias_trigger(self, bias_name: str, event_data: Dict[str, Any]) -> bool:
    # Custom logic for domain-specific bias detection
    if bias_name == "custom_bias":
        return event_data.get("custom_field", 0) > 0.5
    # Fall back to default
    return super()._check_bias_trigger(bias_name, event_data)
```

### Creating a Plugin Module

```python
class CustomBehavioralPlugin:
    def __init__(self, agent):
        self.agent = agent

    def on_analyze_complete(self, result):
        # Post-process analysis results
        pass

    def on_nudge_designed(self, nudge):
        # Customize or validate nudge
        pass

# Register plugin
agent.register_plugin(CustomBehavioralPlugin(agent))
```

## Best Practices

- Always validate event_data schema before passing to analyze_behavior
- Set appropriate confidence thresholds for production deployments
- Review all nudge designs for ethical implications before promotion
- Use A/B tests with adequate sample sizes to achieve target statistical power
- Export state regularly for disaster recovery
- Monitor reactance rates closely - values above 5% warrant design review
- Avoid deploying high-risk nudges (scarcity, framing) without legal review
- Rotate experiment hypotheses to avoid statistical p-hacking
- Document context and business objectives alongside experiment designs
- Use persona segmentation to avoid one-size-fits-all interventions
- Test nudge timing optimization before full deployment
- Implement gradual rollout for new nudge types (10% -> 50% -> 100%)
- Review bias correlation matrix quarterly for emerging patterns
- Archive completed experiments with full statistical documentation

## Performance Optimization

### Memory Management

- Reduce `max_history_size` for constrained environments
- Call `reset_session()` periodically in long-running services
- Use `export_state()` for long-term storage instead of relying solely on in-memory
- Process feedback in batches rather than one at a time
- Clear `pattern_cache` if memory usage approaches limits

### Throughput Optimization

- Use `batch_design_nudges()` for bulk nudge creation
- Pre-load persona and bias data at startup (warm cache)
- Avoid redundant analysis by caching results for identical inputs
- Use `advanced_analysis()` for multi-user batch processing
- Schedule experiments during off-peak hours for resource-intensive operations

### Latency Reduction

- Disable caching only for debugging: `enable_caching: false`
- Limit `session_history` queries with `since` and `user_id` filters
- Use `compute_cohort_retention()` with pre-aggregated data
- Cache intermediate experiment stats for repeated access
- Pre-compute persona statistics during low-traffic periods

## Research Foundation

The Behavioral Science Agent is built on peer-reviewed research including:

- **Kahneman and Tversky (1979)**: Prospect Theory and cognitive biases
- **Thaler and Sunstein (2008)**: Nudge theory and libertarian paternalism
- **Lally et al. (2010)**: Habit formation in real-world contexts (66-day average)
- **Cialdini (2001)**: Influence principles including social proof and scarcity
- **Ajzen (1991)**: Theory of Planned Behavior
- **Duhigg (2012)**: Habit loop framework (cue-routine-reward)
- **Tversky and Kahneman (1974)**: Heuristics and biases research
- **Ariely (2008)**: Predictably irrational behavior patterns
- **Sherif (1936)**: Social judgment theory and conformity
- **Festinger (1957)**: A theory of cognitive dissonance
- **Skinner (1953)**: Science and Human Behavior (reinforcement theory)
- **Bandura (1977)**: Social Learning Theory
- **Deci and Ryan (1985)**: Self-Determination Theory (intrinsic vs extrinsic motivation)
- **Goleman (1995)**: Emotional Intelligence
- **Kahneman (2011)**: Thinking, Fast and Slow (System 1/System 2)

## Appendix A: Complete Method Signatures

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

## Appendix B: Error Codes

| Error | Condition | Recovery |
|-------|-----------|----------|
| ValueError | Invalid parameter values | Validate inputs against constraints |
| KeyError | Resource not found (nudge, experiment, habit) | Check IDs before accessing |
| TypeError | Wrong data type passed | Strict type checking |
| OverflowError | Numerical computation overflow | Check input ranges |
| FileNotFoundError | State import/export path invalid | Verify file path exists |
| json.JSONDecodeError | Invalid JSON in state file | Validate JSON format before import |

## Appendix C: Related Projects

- **Awesome Grok Skills**: Parent repository of agents
- **Persuasive Technology**: Related field focused on attitude and behavior change through computing
- **Choice Architecture**: Design of environments that influence decision-making
- **Digital Behavior Change**: Application of behavioral science to digital products

## Appendix D: Roadmap

- [ ] Machine learning-based bias prediction
- [ ] Real-time nudge deployment adapter
- [ ] Dashboard for experiment visualization
- [ ] Integration with popular analytics platforms
- [ ] Multi-language support for nudge descriptions
- [ ] Advanced simulated user population testing
- [ ] Seasonal and trend-aware bias weighting
- [ ] Auto-generated experiment reports in PDF format

## Appendix E: FAQ

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

**Q: How does the agent handle different timezones?**

A: The agent uses UTC internally. Timezone conversion should happen at the integration layer before passing data to the agent.

**Q: What happens when max_history_size is reached?**

A: Oldest sessions are evicted using FIFO (first in, first out) to make room for new sessions.

**Q: Can I run multiple experiments simultaneously?**

A: Yes. The experiment_registry supports concurrent experiments with independent tracking.

**Q: How do I interpret effect size (Cohen's h)?**

A: h around 0.2 is considered small, 0.5 medium, 0.8 large. In practice, even small effects can be meaningful at scale.
