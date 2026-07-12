---
name: "feature-flags"
category: "configuration-management"
version: "2.0.0"
tags: ["configuration-management", "feature-flags", "feature-toggles", "rollout", "A/B-testing"]
---

# Feature Flags

## Overview

The Feature Flags module provides tools for managing feature toggles, gradual rollouts, A/B testing, and kill switches. It covers flag lifecycle management, targeting rules, percentage rollouts, user segmentation, and flag analytics. The module supports operational flags, experiment flags, and permission flags patterns.

This skill is essential for product engineers, release managers, and platform teams implementing progressive delivery and feature flag-driven development.

## Core Capabilities

- **Flag Management**: Create, update, archive feature flags with lifecycle tracking
- **Targeting Rules**: User segment targeting, attribute-based rules, and percentage rollouts
- **A/B Testing**: Experiment assignment, variant management, and statistical significance tracking
- **Kill Switches**: Emergency feature disable, circuit breaker patterns, and degraded mode activation
- **Scheduled Rollouts**: Time-based flag scheduling, phased rollouts, and calendar-based releases
- **Analytics**: Flag usage tracking, impression counting, and conversion attribution
- **Multi-Environment**: Flag configuration per environment (dev, staging, production)
- **SDK Integration**: Client-side and server-side flag evaluation patterns

## Usage Examples

```python
from feature_flags import (
    FlagManager,
    TargetingEngine,
    ExperimentRunner,
    RolloutScheduler,
    FlagAnalytics,
)

# --- Flag Management ---
manager = FlagManager()
flag = manager.create_flag(
    key="new_checkout_flow",
    name="New Checkout Flow",
    description="Redesigned checkout experience",
    default_value=False,
    flag_type="boolean",
)
print(f"Flag: {flag.key}")
print(f"Status: {flag.status}")

# --- Targeting ---
engine = TargetingEngine()
engine.set_targeting(
    flag_key="new_checkout_flow",
    rules=[
        {"attribute": "country", "operator": "in", "values": ["US", "CA"]},
        {"attribute": "beta_user", "operator": "equals", "value": True},
    ],
    percentage_rollout=25,
)
is_enabled = engine.evaluate(
    flag_key="new_checkout_flow",
    context={"user_id": "u123", "country": "US", "beta_user": True},
)
print(f"Flag enabled for user: {is_enabled}")

# --- A/B Testing ---
runner = ExperimentRunner()
experiment = runner.create_experiment(
    flag_key="new_checkout_flow",
    variants=[
        {"name": "control", "weight": 50},
        {"name": "treatment", "weight": 50},
    ],
    primary_metric="conversion_rate",
)
print(f"Experiment: {experiment.experiment_id}")
print(f"Variants: {[v['name'] for v in experiment.variants]}")

# --- Rollout Scheduler ---
scheduler = RolloutScheduler()
schedule = scheduler.schedule_rollout(
    flag_key="new_checkout_flow",
    phases=[
        {"percentage": 10, "duration_hours": 24},
        {"percentage": 25, "duration_hours": 48},
        {"percentage": 50, "duration_hours": 72},
        {"percentage": 100, "duration_hours": 0},
    ],
)
print(f"Rollout phases: {len(schedule.phases)}")

# --- Analytics ---
analytics = FlagAnalytics()
analytics.record_impression("new_checkout_flow", "u123", variant="treatment")
stats = analytics.get_stats("new_checkout_flow")
print(f"Impressions: {stats.impressions}")
print(f"Unique users: {stats.unique_users}")
```

## Best Practices

- Separate operational flags (kill switches) from release flags (new features) — different lifecycle
- Use flag key naming convention: `team.feature_name` (e.g., `payments.new_checkout`)
- Set flag expiration dates — stale flags accumulate technical debt
- Implement flag cleanup automation — remove flags after full rollout
- Use targeting rules with fallthrough values for reliable evaluation
- Log all flag evaluations for debugging and audit trails
- Implement flag hooks for analytics integration
- Test flag states in CI/CD — test with flag ON and OFF
- Use gradual rollouts (10% -> 25% -> 50% -> 100%) for high-risk features
- Document all flags with owner, purpose, and expected cleanup date

## Related Modules

- **dynamic-config**: Runtime configuration changes
- **config-ops**: Configuration management patterns
- **environment-config**: Environment-specific flag settings
- **secrets-management**: Secret flag values management
