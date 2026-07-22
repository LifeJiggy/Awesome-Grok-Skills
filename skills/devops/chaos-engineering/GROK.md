---
name: chaos-engineering
category: devops
version: 1.0.0
tags: [devops, chaos-engineering, resilience, fault-injection, reliability]
---

# Chaos Engineering

## Overview

Chaos Engineering is the discipline of experimenting on infrastructure to build confidence in the system's capability to withstand turbulent conditions in production. This module provides a comprehensive toolkit for designing, executing, and analyzing chaos experiments Ã¢â‚¬â€ from simple fault injection (killing processes, network latency) to complex multi-stage failure scenarios (cascading failures, region outages). The goal is not to break things randomly, but to systematically discover weaknesses before they cause production incidents.

The module implements the chaos engineering lifecycle: steady-state hypothesis Ã¢â€ â€™ experiment design Ã¢â€ â€™ fault injection Ã¢â€ â€™ observation Ã¢â€ â€™ analysis Ã¢â€ â€™ remediation. Each experiment is defined as code (declarative YAML or programmatic Python), with built-in safety mechanisms (automatic rollback, blast radius control, abort conditions). Experiments run in pre-defined phases: preparation, injection, observation, and recovery, with real-time monitoring of system health throughout.

Advanced capabilities include game day orchestration for team-based resilience exercises, steady-state detection using statistical analysis of metrics baselines, and automated chaos experiment generation based on architecture analysis. The module integrates with Kubernetes (Litmus, Chaos Mesh), AWS (AWS Fault Injection Simulator), and custom infrastructure through extensible fault injectors.

## Core Capabilities

- Declarative experiment definition with YAML or Python DSL
- Fault injection: process kill, network latency/loss, CPU/memory stress, disk I/O
- Kubernetes pod/container chaos: delete pods, inject network faults, modify resource limits
- Steady-state hypothesis validation with statistical analysis
- Blast radius control with namespace/node/pod targeting
- Automatic rollback and abort conditions
- Game day orchestration for team exercises
- Experiment scheduling and recurring experiments
- Integration with Prometheus, Grafana, and Datadog for observability

## Usage Examples

### Basic Fault Injection

```python
from chaos_engineering import ChaosEngine, FaultType

engine = ChaosEngine(target="kubernetes", namespace="staging")

# Kill random pods
experiment = engine.create_experiment(
    name="pod-kill",
    target={"app": "api-service"},
    fault=FaultType.POD_KILL,
    duration_s=300,
    blast_radius_pct=25,
)

result = engine.run(experiment)
print(f"Experiment: {result.experiment_id}")
print(f"Steady state maintained: {result.steady_state_holds}")
```

### Network Latency Injection

```python
from chaos_engineering import NetworkFault

network_fault = NetworkFault(
    target={"app": "api-service"},
    fault_type="latency",
    latency_ms=500,
    jitter_ms=100,
    duration_s=600,
    direction="both",
)

result = engine.run_network_fault(network_fault)
print(f"Latency added: {result.fault_applied}")
print(f"Error rate increase: {result.error_rate_delta:.2%}")
```

### Steady-State Hypothesis

```python
from chaos_engineering import SteadyStateHypothesis, MetricBaseline

hypothesis = SteadyStateHypothesis(
    name="api-service-resilience",
    baselines=[
        MetricBaseline(metric="http_requests_total", min_rate=100, max_rate=500),
        MetricBaseline(metric="http_error_rate", max_value=0.01),
        MetricBaseline(metric="http_latency_p99_ms", max_value=500),
    ],
    verification_duration_s=300,
)

engine.set_steady_state(hypothesis)
```

### Kubernetes Chaos

```python
from chaos_engineering import K8sChaos

k8s = K8sChaos(namespace="staging")

# Delete random pods
k8s.delete_pods(
    selector={"app": "api-service"},
    count=2,
    grace_period_seconds=30,
)

# Inject network latency
k8s.network_latency(
    selector={"app": "api-service"},
    latency_ms=200,
    duration_s=120,
)

# Stress CPU
k8s.cpu_stress(
    selector={"app": "worker"},
    cpu_workers=4,
    duration_s=300,
)
```

### Game Day Orchestration

```python
from chaos_engineering import GameDay, Scenario

game_day = GameDay(
    name="Quarterly Resilience Test",
    participants=["sre-team", "backend-team"],
    scenarios=[
        Scenario(name="database-failover", fault="db_kill_primary", duration_s=600),
        Scenario(name="redis-cluster-failover", fault="redis_node_kill", duration_s=300),
        Scenario(name="network-partition", fault="network_split", duration_s=120),
    ],
)

game_day.schedule("2024-03-15T14:00:00Z")
```

## Advanced Configuration

### Experiment Scheduling

```python
from chaos_engineering import ExperimentScheduler

scheduler = ExperimentScheduler()
scheduler.schedule_recurring(
    experiment=experiment,
    cron="0 2 * * 1",  # Every Monday at 2 AM
    max_duration_s=3600,
    notify=["slack-sre"],
)
```

### Abort Conditions

```python
from chaos_engineering import AbortCondition

abort = AbortCondition(
    metrics=[
        {"metric": "http_error_rate", "threshold": 0.05, "duration_s": 60},
        {"metric": "pod_restart_count", "threshold": 10, "duration_s": 30},
    ],
    action="rollback_and_stop",
)
engine.set_abort_condition(abort)
```

## Architecture Patterns

### Chaos Engineering Lifecycle

```
Steady-State Hypothesis Ã¢â€ â€™ Experiment Design Ã¢â€ â€™ Fault Injection Ã¢â€ â€™ Observation Ã¢â€ â€™ Analysis Ã¢â€ â€™ Remediation
```

### Fault Injection Architecture

```
Chaos Controller
    Ã¢â€â€š
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€“Âº Process Faults (kill, signal, resource limits)
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€“Âº Network Faults (latency, loss, partition)
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€“Âº Storage Faults (disk full, slow I/O)
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€“Âº CPU/Memory Faults (stress, OOM)
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€“Âº Kubernetes Faults (pod delete, node cordon)
```

## Integration Guide

### Prometheus Integration

```python
from chaos_engineering import PrometheusIntegration

prom = PrometheusIntegration(url="http://prometheus:9090")
engine.attach_metrics(prom)
engine.set_steady_state_baselines_from_prometheus("api-service", lookback_days=7)
```

### Slack Notifications

```python
from chaos_engineering import SlackNotifier

notifier = SlackNotifier(webhook_url="https://hooks.slack.com/...")
engine.notify(notifier, events=["experiment_start", "experiment_end", "abort_triggered"])
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Parallel fault injection | Faster multi-target experiments |
| Metric pre-fetching | Baseline computation in seconds |
| Streaming observation | Real-time steady-state checking |
| Experiment caching | Skip re-computation for recurring experiments |

## Security Considerations

- **Access control**: Only authorized users can run chaos experiments
- **Blast radius limits**: Never target production without approval
- **Credential isolation**: Chaos agents don't need production credentials
- **Audit logging**: Record all experiments and their outcomes
- **Approval workflows**: Require sign-off for high-risk experiments

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Experiment stuck | Pod not terminating | Check grace period, force delete |
| Steady state false alarm | Baseline too strict | Recalibrate baselines |
| Fault not applying | Wrong selector | Verify pod labels |
| Recovery too slow | Missing health checks | Configure proper readiness probes |

## API Reference

### ChaosEngine

```python
class ChaosEngine:
    def __init__(self, target: str, namespace: str)
    def create_experiment(self, name: str, target: dict, fault: FaultType, duration_s: int, blast_radius_pct: int) -> Experiment
    def run(self, experiment: Experiment) -> ExperimentResult
    def set_steady_state(self, hypothesis: SteadyStateHypothesis) -> None
    def set_abort_condition(self, condition: AbortCondition) -> None
```

### K8sChaos

```python
class K8sChaos:
    def __init__(self, namespace: str)
    def delete_pods(self, selector: dict, count: int, grace_period_seconds: int) -> None
    def network_latency(self, selector: dict, latency_ms: int, duration_s: int) -> None
    def cpu_stress(self, selector: dict, cpu_workers: int, duration_s: int) -> None
    def memory_stress(self, selector: dict, memory_mb: int, duration_s: int) -> None
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class FaultType(Enum):
    POD_KILL = "pod_kill"
    NETWORK_LATENCY = "network_latency"
    NETWORK_LOSS = "network_loss"
    CPU_STRESS = "cpu_stress"
    MEMORY_STRESS = "memory_stress"
    DISK_STRESS = "disk_stress"

@dataclass
class ExperimentResult:
    experiment_id: str
    steady_state_holds: bool
    duration_s: float
    faults_injected: int
    observations: list

@dataclass
class MetricBaseline:
    metric: str
    min_value: float = None
    max_value: float = None
    min_rate: float = None
    max_rate: float = None
```

## Deployment Guide

### Installation

```bash
pip install chaos-engineering
# With Kubernetes support
pip install chaos-engineering[k8s]
```

### Kubernetes Setup

```bash
kubectl apply -f https://raw.githubusercontent.com/chaos-mesh/chaos-mesh/main/manifests/dashboard.yaml
```

## Monitoring & Observability

```python
from chaos_engineering import MetricsCollector

collector = MetricsCollector()
collector.counter("chaos.experiments.total", count, tags={"result": result})
collector.counter("chaos.faults.injected", count, tags={"type": fault_type})
collector.gauge("chaos.steady_state.holds", 1 if holds else 0)
collector.histogram("chaos.experiment.duration_s", duration)
```

## Testing Strategy

```python
import pytest
from chaos_engineering import ChaosEngine

def test_experiment_creation():
    engine = ChaosEngine(target="kubernetes", namespace="test")
    experiment = engine.create_experiment("test", {"app": "test"}, FaultType.POD_KILL, 60, 10)
    assert experiment.name == "test"
    assert experiment.blast_radius_pct == 10
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added game day support | Configure scenarios |
| 2.0.0 | New experiment format | Migrate YAML definitions |

## Glossary

| Term | Definition |
|------|-----------|
| **Steady-State** | Normal operating condition before experiment |
| **Blast Radius** | Percentage of infrastructure affected |
| **Game Day** | Team exercise simulating production failures |
| **Hypothesis** | Expected system behavior during fault injection |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with fault injection
- Kubernetes chaos support
- Steady-state hypothesis validation
- Game day orchestration

## Contributing Guidelines

```bash
git clone https://github.com/example/chaos-engineering.git
pip install -e ".[dev]"
pytest tests/
```

## Advanced Chaos Experiments

### Cascading Failure Simulation

Simulate real-world cascading failures where one service failure triggers downstream failures.

```python
from chaos_engineering import CascadingFailure, FailureChain

chain = FailureChain(
    name="database-cascade",
    steps=[
        {"service": "database", "fault": FaultType.PROCESS_KILL, "delay_s": 0},
        {"service": "cache", "fault": FaultType.NETWORK_LOSS, "delay_s": 5, "depends_on": "database"},
        {"service": "api-gateway", "fault": FaultType.CPU_STRESS, "delay_s": 10, "depends_on": "cache"},
        {"service": "frontend", "fault": FaultType.LATENCY_INJECT, "latency_ms": 2000, "delay_s": 15, "depends_on": "api-gateway"},
    ],
    abort_if={
        "metric": "http_error_rate",
        "threshold": 0.50,
        "duration_s": 60,
    },
)

result = engine.run_cascade(chain)
print(f"Cascade reached step: {result.max_step_reached}")
print(f"Recovery time: {result.recovery_time_s}s")
```

### AWS Fault Injection Simulator Integration

```python
from chaos_engineering import AWSFIS

fis = AWSFIS(
    region="us-east-1",
    role_arn="arn:aws:iam::123456789:role/ChaosRole",
)

# Create experiment template
template = fis.create_template(
    name="ec2-instance-failure",
    targets={"instance-type": {"resource_type": "aws:ec2:instance", "selection_mode": "COUNT(2)"}},
    actions=[
        {"action_type": "aws:ec2:stop-instances", "parameters": {"duration": "PT5M"}},
        {"action_type": "aws:ec2:detach-volume", "parameters": {"device_name": "/dev/sda1"}},
    ],
    stop_conditions=[
        {"source": "aws:cloudwatch:alarm", "value": "arn:aws:cloudwatch:...:alarm:HighErrorRate"},
    ],
)

# Run experiment
experiment = fis.run(template.id, duration_s=300)
print(f"Experiment: {experiment.id}")
print(f"State: {experiment.state}")
```

### Network Partition Testing

```python
from chaos_engineering import NetworkPartition

partition = NetworkPartition(
    name="cross-region-partition",
    groups={
        "group_a": {"selector": {"region": "us-east-1"}},
        "group_b": {"selector": {"region": "eu-west-1"}},
    },
    rules=[
        {"from": "group_a", "to": "group_b", "action": "drop_all"},
        {"from": "group_b", "to": "group_a", "action": "drop_all"},
    ],
    duration_s=600,
    validate_consistency=True,
)

result = engine.run_partition(partition)
print(f"Consistency maintained: {result.consistent}")
print(f"Split brain detected: {result.split_brain}")
```

### Steady-State Detection Algorithms

```python
from chaos_engineering import SteadyStateDetector

detector = SteadyStateDetector(
    algorithm="ewma",  # Exponentially Weighted Moving Average
    sensitivity=0.1,
    min_samples=30,
)

# Learn baseline from production traffic
baseline = detector.learn(
    metrics=["http_requests_total", "http_error_rate", "latency_p99"],
    lookback_days=14,
    confidence_level=0.95,
)

# Detect anomalies during experiment
is_stable = detector.check(baseline, current_metrics)
print(f"Steady state: {is_stable}")
print(f"Deviations: {detector.get_deviations()}")
```

### Chaos Experiment Taxonomy

| Fault Category | Examples | Impact | Recovery Time |
|----------------|----------|--------|---------------|
| Process faults | Kill pod, SIGTERM, OOM | Service restart | 10-30s |
| Network faults | Latency, loss, partition | Request failures | 0s (transient) |
| Resource faults | CPU, memory, disk pressure | Performance degradation | 0s (transient) |
| State faults | Data corruption, clock skew | Data inconsistency | Minutes-hours |
| Dependency faults | DNS failure, upstream timeout | Cascading failures | Seconds-minutes |

### Game Day Runbook Template

```yaml
name: Quarterly Resilience Test
date: 2024-03-15T14:00:00Z
duration: 4 hours
participants:
  - role: Incident Commander
    name: "Alice"
  - role: Observer
    name: "Bob"
  - role: Safety Officer
    name: "Carol"

scenarios:
  - name: Database Failover
    description: Primary MySQL goes down, replica promotes
    fault: mysql_kill_primary
    expected_behavior: >
      Application continues serving reads from replica.
      Writes queue and replay after failover completes.
    abort_condition: "Error rate > 10% for > 2 minutes"
    max_duration: 10 minutes

  - name: Redis Cluster Split
    description: Network partition between Redis nodes
    fault: redis_network_split
    expected_behavior: >
      Application degrades gracefully.
      Stale data served from local cache.
    abort_condition: "Data inconsistency detected"
    max_duration: 5 minutes

  - name: CDN Origin Failure
    description: Origin server becomes unreachable
    fault: origin_server_kill
    expected_behavior: >
      CDN serves cached content.
      Stale content served for up to TTL.
    abort_condition: "Cache hit rate < 50%"
    max_duration: 15 minutes
```

### Automated Chaos Experiment Generation

```python
from chaos_engineering import ExperimentGenerator

generator = ExperimentGenerator(
    architecture_graph=arch_graph,
    risk_scores=risk_db,
)

# Auto-generate experiments based on architecture
experiments = generator.generate(
    focus=["single_point_of_failure", "missing_redundancy", "weak_failover"],
    max_experiments=10,
    safety_level="staging_only",
)

for exp in experiments:
    print(f"Experiment: {exp.name}")
    print(f"  Target: {exp.target}")
    print(f"  Fault: {exp.fault_type}")
    print(f"  Risk: {exp.risk_score:.2f}")
```

### Chaos Engineering Maturity Model

| Level | Practice | Tools |
|-------|----------|-------|
| 1 Ã¢â‚¬â€ Ad hoc | Manual fault injection | SSH, kubectl delete |
| 2 Ã¢â‚¬â€ Defined | Scheduled experiments | Chaos Mesh, Litmus |
| 3 Ã¢â‚¬â€ Managed | Automated steady-state detection | Custom metrics pipeline |
| 4 Ã¢â‚¬â€ Measurable | Game days with metrics | Full observability stack |
| 5 Ã¢â‚¬â€ Optimized | Auto-generated experiments | Architecture-aware generator |

### Experiment Result Analysis

```python
from chaos_engineering import ExperimentAnalyzer

analyzer = ExperimentAnalyzer()

# Analyze experiment results
analysis = analyzer.analyze(experiment_result)
print(f"Resilience score: {analysis.resilience_score:.1f}/100")
print(f"Recovery time: {analysis.recovery_time_s}s")
print(f"Blast radius actual: {analysis.actual_blast_radius:.1%}")
print(f"Impact on error budget: {analysis.error_budget_impact:.2f}%")

# Recommendations
for rec in analysis.recommendations:
    print(f"  [{rec.priority}] {rec.description}")
    print(f"    Mitigation: {rec.mitigation}")
```

### Kubernetes Pod Chaos (Advanced)

```python
from chaos_engineering import K8sAdvancedChaos

k8s = K8sAdvancedChaos(namespace="production")

# Pod resource limit modification
k8s.modify_resources(
    selector={"app": "api-service"},
    cpu_limit="100m",  # Reduce to 100m
    memory_limit="128Mi",
    duration_s=300,
)

# Pod DNS failure
k8s.dns_failure(
    selector={"app": "api-service"},
    domain="database.internal",
    duration_s=120,
)

# Pod node pressure
k8s.node_pressure(
    node_selector={"role": "worker"},
    pressure_type="memory",
    threshold_pct=95,
    duration_s=600,
)

# Pod eviction
k8s.evict_pods(
    selector={"app": "worker"},
    count=3,
    grace_period_seconds=30,
)
```

### Chaos Mesh Integration

```python
from chaos_engineering import ChaosMeshIntegration

mesh = ChaosMeshIntegration(
    dashboard_url="http://chaos-dashboard:2333",
    namespace="chaos-testing",
)

# Create NetworkChaos experiment
mesh.create_network_chaos(
    name="api-latency-inject",
    selector={"app": "api-service"},
    mode="all",
    action="delay",
    delay={"latency": "500ms", "jitter": "100ms"},
    duration="10m",
)

# Create PodChaos experiment
mesh.create_pod_chaos(
    name="pod-kill-random",
    selector={"app": "worker"},
    mode="random-one",
    action="pod-kill",
    grace_period=30,
)
```

### Disaster Recovery Testing

```python
from chaos_engineering import DRTest

dr = DRTest(
    name="Region Failover Test",
    primary_region="us-east-1",
    dr_region="us-west-2",
)

# Execute failover test
result = dr.execute(
    steps=[
        "simulate_primary_outage",
        "verify_dns_failover",
        "validate_data_consistency",
        "measure_rto",
        "measure_rpo",
        "execute_failback",
    ],
    max_rto_seconds=300,
    max_rpo_seconds=60,
)

print(f"RTO achieved: {result.rto_seconds}s (target: {result.max_rto}s)")
print(f"RPO achieved: {result.rpo_seconds}s (target: {result.max_rpo}s)")
print(f"DR test passed: {result.passed}")
```

### Disaster Recovery Testing

```python
from chaos_engineering import DRTest

dr = DRTest(
    name="Region Failover Test",
    primary_region="us-east-1",
    dr_region="us-west-2",
)

# Execute failover test
result = dr.execute(
    steps=[
        "simulate_primary_outage",
        "verify_dns_failover",
        "validate_data_consistency",
        "measure_rto",
        "measure_rpo",
        "execute_failback",
    ],
    max_rto_seconds=300,
    max_rpo_seconds=60,
)

print(f"RTO achieved: {result.rto_seconds}s (target: {result.max_rto}s)")
print(f"RPO achieved: {result.rpo_seconds}s (target: {result.max_rpo}s)")
print(f"DR test passed: {result.passed}")
```

### Chaos Experiment YAML Schema

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: api-latency-test
  namespace: staging
spec:
  action: delay
  mode: all
  selector:
    namespaces: [staging]
    labelSelectors:
      app: api-service
  delay:
    latency: "500ms"
    jitter: "100ms"
    correlation: "50"
  duration: "10m"
  direction: both
```

### Game Day Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Mean Time to Detect (MTTD) | < 5 min | Alert Ã¢â€ â€™ Acknowledgment |
| Mean Time to Mitigate (MTTM) | < 15 min | Detection Ã¢â€ â€™ Mitigation |
| Mean Time to Recover (MTTR) | < 30 min | Mitigation Ã¢â€ â€™ Full Recovery |
| Runbook Accuracy | > 90% | Steps followed successfully |
| Team Communication | Pass/Fail | No missed escalations |
| Blast Radius Control | < 20% | Actual impact vs planned |

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
