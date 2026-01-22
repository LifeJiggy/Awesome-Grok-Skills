# Chaos Engineering

## Overview

Chaos Engineering is the discipline of experimenting on systems to build confidence in their capability to withstand turbulent conditions. This skill covers experiment design, failure injection techniques, and observability integration. Chaos Engineering proactively identifies weaknesses before they cause outages.

## Core Capabilities

Experiment design formulates hypotheses about system behavior under failure. Failure injection introduces various fault types including latency, crashes, and resource exhaustion. Steady state verification measures normal system behavior to compare against experiment results. Blast radius controls limit the impact of experiments.

Automated experiments run continuously in CI/CD pipelines. Game days coordinate large-scale chaos testing with teams. Analysis and learning extract insights from experiment results. Remediation addresses discovered weaknesses.

## Usage Examples

```python
from chaos_engineering import ChaosEngineering

chaos = ChaosEngineering()

experiment = chaos.create_experiment(
    name="API Resilience Test",
    hypothesis="If the database becomes slow, the API will degrade gracefully instead of failing",
    method="Inject 500ms latency into database queries",
    steady_state="API responds with 200 OK within 2 seconds"
)

chaos.add_chaos_injection(
    experiment,
    failure_type="latency",
    target="database",
    params={"delay_ms": 500, "jitter_ms": 50}
)

latency_injection = chaos.create_latency_injection(
    target="database-primary",
    delay_ms=500,
    jitter_ms=100
)

failure_injection = chaos.create_failure_injection(
    target="payment-service",
    failure_type="abort",
    percentage=25
)

network_partition = chaos.create_network_partition(
    partitions=["zone-a", "zone-b"],
    isolation_level="zone"
)

steady_state = chaos.configure_steady_state_monitor(
    experiment=experiment,
    metrics=["error_rate", "latency_p95", "availability"],
    threshold={"error_rate": 0.05, "latency_p95": 2000}
)

termination = chaos.configure_termination_conditions(
    experiment=experiment,
    conditions=[
        {"metric": "error_rate", "threshold": 0.3, "duration_seconds": 30},
        {"metric": "latency_p99", "threshold": 10000, "duration_seconds": 60}
    ]
)

rollback = chaos.add_rollback(
    experiment=experiment,
    action="remove_latency_injection",
    params={}
)

blast_radius = chaos.create_blast_radius(
    target_scope={"service": "payment-service", "percentage": 10},
    containment_strategy="canary_deployment"
)

observability = chaos.configure_observability_integration(
    tools=["prometheus", "grafana", "jaeger"]
)

game_day = chaos.create_game_day(
    name="Q1 Game Day",
    scenarios=[
        "Database failure",
        "Network partition",
        "High CPU load"
    ],
    participants=["sre-team", "dev-team", "ops-team"],
    observer="security-team"
)

report = chaos.create_experiment_report(
    experiment=experiment,
    results={
        "hypothesis_confirmed": True,
        "error_rate_increase": 0.02,
        "latency_increase": 450,
        "recovery_time_seconds": 5
    },
    conclusion="System degrades gracefully as expected"
)
```

## Best Practices

Start with controlled experiments in staging environments. Define steady state before injecting failures. Limit blast radius to minimize potential impact. Have rollback procedures ready before starting experiments.

Observe metrics continuously during experiments. Run experiments regularly, not just once. Share learnings across teams. Automate experiments for continuous validation.

## Related Skills

- Site Reliability Engineering (reliability practices)
- Observability (monitoring)
- Incident Management (response procedures)
- Testing (general testing)

## Use Cases

Cloud reliability testing validates multi-region failover capabilities. Microservices resilience validates circuit breaker and retry logic. Database HA validates primary-replica failover. Network resilience validates routing during partition events.
