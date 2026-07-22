# Performance Testing

## Overview

Performance Testing evaluates system responsiveness, stability, scalability, and resource utilization under varying load conditions. This skill covers load testing, stress testing, endurance testing, spike testing, and scalability testing methodologies. Performance testing identifies bottlenecks, validates SLA compliance, and ensures applications can handle expected and peak user traffic.

## Core Capabilities

Load testing simulates expected user traffic to validate performance under normal conditions. Stress testing pushes systems beyond normal capacity to identify breaking points and failure modes. Endurance testing (soak testing) evaluates system behavior under sustained load over extended periods. Spike testing measures system response to sudden traffic surges.

Performance profiling identifies bottlenecks in application code, database queries, network calls, and infrastructure. Real User Monitoring (RUM) captures actual user experience metrics. Synthetic monitoring provides consistent baseline measurements. Capacity planning uses performance data to predict future infrastructure needs.

## Usage Examples

```python
from performance_testing import PerformanceTestFramework, LoadType

framework = PerformanceTestFramework()

# Create load test
test = framework.create_load_test(
    name="User Login Load Test",
    target_url="https://api.example.com/login",
    virtual_users=100,
    duration_seconds=300,
    ramp_up_seconds=60
)

# Execute and analyze
results = framework.execute_test(test)
print(f"Throughput: {results['requests_per_second']} req/s")
print(f"Avg Response: {results['avg_response_time']}ms")
print(f"Error Rate: {results['error_rate']}%")

# Stress test
stress = framework.create_stress_test(
    name="Breaking Point Test",
    target_url="https://api.example.com",
    max_virtual_users=1000,
    step_duration=60
)

# Endurance test
endurance = framework.create_endurance_test(
    name="24-Hour Soak Test",
    target_url="https://api.example.com",
    virtual_users=50,
    duration_hours=24
)
```

## Best Practices

Establish performance baselines before making changes. Test in production-like environments with realistic data volumes. Include think time between requests to simulate real user behavior. Monitor server-side metrics alongside client-side performance. Test from multiple geographic locations to validate global performance.

Run performance tests in CI/CD pipelines to catch regressions early. Use realistic test data that represents actual production patterns. Document performance requirements as SLAs with specific thresholds. Analyze both average and percentile metrics (p50, p95, p99) for complete performance visibility.

## Related Skills

- Load Testing (traffic simulation)
- Stress Testing (breaking point analysis)
- Profiling (bottleneck identification)
- Capacity Planning (infrastructure forecasting)

## Use Cases

Web application performance validation ensures pages load within acceptable timeframes. API performance testing validates throughput and latency requirements for service endpoints. Mobile app performance testing measures battery impact, memory usage, and network efficiency. Database performance testing identifies query optimization opportunities and connection pool sizing.

## Advanced Configuration

### Load Test Advanced Configuration

```python
from performance_testing import LoadTestConfig, LoadProfile, ThinkTime

# Advanced load test configuration
config = LoadTestConfig(
    name="E-commerce Checkout Load Test",
    target_url="https://api.example.com",
    protocol="https",
    virtual_users=500,
    duration_seconds=600,
    ramp_up_seconds=120,
    ramp_up_profile=LoadProfile.LINEAR,
    think_time=ThinkTime.BETWEEN(1, 3),  # 1-3 seconds between requests
    connection_pool_size=100,
    timeout_seconds=30,
    retry_count=3,
    retry_delay_ms=1000,
    headers={
        "Authorization": "Bearer ${token}",
        "Content-Type": "application/json",
        "X-Request-ID": "${uuid}",
    },
    cookies={"session": "${session_id}"},
    ssl_verify=True,
    follow_redirects=True,
)

test = framework.create_load_test(config=config)
```

### Stress Test Advanced Configuration

```python
from performance_testing import StressTestConfig, StepConfig

# Advanced stress test configuration
stress_config = StressTestConfig(
    name="Breaking Point Analysis",
    target_url="https://api.example.com",
    initial_users=10,
    max_users=1000,
    step_config=StepConfig(
        users_per_step=50,
        step_duration_seconds=60,
        hold_duration_seconds=30,
        ramp_up_seconds=10,
    ),
    abort_on_error_rate=50,  # Stop if 50% errors
    abort_on_response_time=10000,  # Stop if avg response > 10s
    metrics_collection=True,
    server_monitoring=True,
)

stress = framework.create_stress_test(config=stress_config)
```

### Endurance Test Advanced Configuration

```python
from performance_testing import EnduranceTestConfig, MemoryLeakDetection

# Advanced endurance test configuration
endurance_config = EnduranceTestConfig(
    name="24-Hour Soak Test",
    target_url="https://api.example.com",
    virtual_users=100,
    duration_hours=24,
    ramp_up_minutes=30,
    metrics_interval_seconds=60,
    memory_leak_detection=MemoryLeakDetection(
        enabled=True,
        threshold_mb=50,  # Alert if memory increases > 50MB
        check_interval_minutes=5,
        baseline_snapshot=True,
    ),
    connection_leak_detection=True,
    thread_leak_detection=True,
)

endurance = framework.create_endurance_test(config=endurance_config)
```

### Spike Test Configuration

```python
from performance_testing import SpikeTestConfig, SpikeProfile

spike_config = SpikeTestConfig(
    name="Flash Sale Spike Test",
    target_url="https://api.example.com/checkout",
    baseline_users=50,
    spike_users=1000,
    spike_duration_seconds=60,
    recovery_duration_seconds=120,
    spike_profile=SpikeProfile.INSTANT,
    num_spikes=5,
    spike_interval_seconds=300,
)

spike = framework.create_spike_test(config=spike_config)
```

## Architecture Patterns

### Performance Test Pipeline Pattern

```python
from performance_testing import PerformancePipeline, PipelineStage

pipeline = PerformancePipeline(stages=[
    PipelineStage(
        name="baseline_measurement",
        type="load",
        config=baseline_config,
    ),
    PipelineStage(
        name="load_test",
        type="load",
        config=load_config,
    ),
    PipelineStage(
        name="stress_test",
        type="stress",
        config=stress_config,
    ),
    PipelineStage(
        name="endurance_test",
        type="endurance",
        config=endurance_config,
    ),
    PipelineStage(
        name="analysis",
        type="analysis",
        processor=lambda results: analyze_results(results),
    ),
])

results = pipeline.execute()
```

### Real User Monitoring Pattern

```python
from performance_testing import RealUserMonitor, RUMConfig

rum_config = RUMConfig(
    enabled=True,
    sample_rate=0.1,  # 10% of users
    metrics=[
        "first_contentful_paint",
        "largest_contentful_paint",
        "first_input_delay",
        "cumulative_layout_shift",
        "time_to_first_byte",
    ],
    session_tracking=True,
    error_tracking=True,
    performance_budget={
        "fcp_ms": 1500,
        "lcp_ms": 2500,
        "fid_ms": 100,
        "cls": 0.1,
    },
)

rum = RealUserMonitor(config=rum_config)
rum.start()
```

### Synthetic Monitoring Pattern

```python
from performance_testing import SyntheticMonitor, MonitorConfig

monitor_config = MonitorConfig(
    name="API Health Check",
    url="https://api.example.com/health",
    method="GET",
    expected_status=200,
    expected_response_time_ms=500,
    check_interval_seconds=60,
    timeout_seconds=10,
    locations=["us-east-1", "eu-west-1", "ap-southeast-1"],
    alert_channels=["slack", "email", "pagerduty"],
)

monitor = SyntheticMonitor(config=monitor_config)
monitor.start()
```

## Integration Guide

### JMeter Integration

```python
from performance_testing import JMeterAdapter

adapter = JMeterAdapter(
    jmeter_path="/opt/jmeter/bin/jmeter",
    test_plan_template="templates/api_test.jmx",
)

# Convert to JMeter test plan
test_plan = adapter.create_test_plan(
    test_config=config,
    thread_groups=[
        {"name": "login", "threads": 100, "ramp_up": 60, "duration": 300},
        {"name": "search", "threads": 200, "ramp_up": 30, "duration": 300},
    ],
)

adapter.execute(test_plan)
results = adapter.parse_results(test_plan)
```

### Grafana Integration

```python
from performance_testing import GrafanaIntegration, GrafanaConfig

grafana_config = GrafanaConfig(
    server_url="http://grafana:3000",
    api_key="${GRAFANA_API_KEY}",
    dashboard_folder="Performance Testing",
    auto_create_dashboard=True,
)

grafana = GrafanaIntegration(config=grafana_config)

# Create dashboard from results
dashboard = grafana.create_dashboard(
    name="Load Test Results",
    metrics=results.metrics,
    time_range="last-24h",
)

print(f"Dashboard URL: {dashboard.url}")
```

### Datadog Integration

```python
from performance_testing import DatadogIntegration, DatadogConfig

datadog_config = DatadogConfig(
    api_key="${DD_API_KEY}",
    app_key="${DD_APP_KEY}",
    site="datadoghq.com",
    service="performance-testing",
    environment="staging",
)

datadog = DatadogIntegration(config=datadog_config)

# Send metrics
datadog.send_metrics(
    metrics=[
        {"name": "perf.test.throughput", "value": results.throughput, "tags": ["test:load"]},
        {"name": "perf.test.latency.p99", "value": results.p99_latency, "tags": ["test:load"]},
    ],
)
```

## Performance Optimization

### Test Execution Optimization

```python
from performance_testing import TestOptimizer

optimizer = TestOptimizer(
    parallel_execution=True,
    max_workers=10,
    distributed_testing=True,
    master_node="master.example.com",
    worker_nodes=["worker1.example.com", "worker2.example.com"],
    resource_monitoring=True,
)

optimized_results = optimizer.optimize(test)
print(f"Execution time reduced: {optimizer.time_savings:.1%}")
print(f"Resource utilization: {optimizer.resource_utilization:.1%}")
```

### Data Generation Optimization

```python
from performance_testing import TestDataGenerator

generator = TestDataGenerator(
    strategy="realistic",
    volume=1000000,
    distribution="pareto",
    relationships=True,
    PII_masking=True,
    correlation_id_tracking=True,
)

test_data = generator.generate()
print(f"Generated {len(test_data)} test records")
print(f"Generation time: {generator.generation_time_seconds:.1f}s")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. High Error Rate During Load Test

**Symptom**: Many 5xx errors or connection failures

**Solution**:
```python
# Reduce virtual users
config.virtual_users = 100  # From 500

# Increase timeout
config.timeout_seconds = 60

# Add retry logic
config.retry_count = 5
config.retry_delay_ms = 2000

# Check server capacity
monitor.check_server_resources()
```

#### 2. Response Time Degradation

**Symptom**: Average response time increases over time

**Solution**:
```python
# Check for memory leaks
endurance_config.memory_leak_detection.enabled = True

# Monitor connection pool
config.connection_pool_size = 200  # Increase pool

# Check database queries
profiler.analyze_slow_queries()
```

#### 3. Inconsistent Results

**Symptom**: Different results between runs

**Solution**:
```python
# Use fixed seeds for data generation
config.random_seed = 42

# Control think time precisely
config.think_time = ThinkTime.FIXED(2.0)

# Use dedicated test environment
config.target_url = "https://staging.example.com"
```

#### 4. Test Environment Issues

**Symptom**: Environment not ready or unstable

**Solution**:
```python
# Add health check before test
health_check = framework.create_health_check(
    url="https://api.example.com/health",
    max_retries=10,
    retry_interval_seconds=5,
)

# Wait for environment
health_check.wait_for_healthy()

# Run test
results = framework.execute_test(test)
```

## API Reference

### Core Classes

#### `PerformanceTestFramework`
```python
class PerformanceTestFramework:
    def __init__(self, config: Optional[TestConfig] = None) -> None: ...
    def create_load_test(self, config: LoadTestConfig) -> LoadTest: ...
    def create_stress_test(self, config: StressTestConfig) -> StressTest: ...
    def create_endurance_test(self, config: EnduranceTestConfig) -> EnduranceTest: ...
    def create_spike_test(self, config: SpikeTestConfig) -> SpikeTest: ...
    def execute_test(self, test: Test) -> TestResults: ...
```

#### `TestResults`
```python
@dataclass
class TestResults:
    test_name: str
    status: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    requests_per_second: float
    avg_response_time_ms: float
    p50_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    min_response_time_ms: float
    max_response_time_ms: float
    error_rate: float
    throughput_bytes_per_second: float
    execution_time_seconds: float
    metrics: Dict[str, Any]
```

## Data Models

### Performance Test Configuration Schema

```json
{
  "name": "Load Test",
  "type": "load",
  "target": {
    "url": "https://api.example.com",
    "protocol": "https",
    "timeout_seconds": 30
  },
  "load": {
    "virtual_users": 100,
    "duration_seconds": 300,
    "ramp_up_seconds": 60,
    "ramp_up_profile": "linear"
  },
  "think_time": {
    "type": "between",
    "min_seconds": 1,
    "max_seconds": 3
  },
  "metrics": {
    "collect_interval_seconds": 10,
    "percentiles": [50, 90, 95, 99]
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM grafana/k6:latest

COPY performance_testing/ /app/performance_testing/
WORKDIR /app

ENV K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090
ENV K6_OUT=output-prometheus-rw

ENTRYPOINT ["k6", "run"]
CMD ["/app/test.js"]
```

### Kubernetes Deployment

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: performance-test
spec:
  parallelism: 5
  template:
    spec:
      containers:
      - name: k6
        image: grafana/k6:latest
        command: ["k6", "run", "/scripts/test.js"]
        env:
        - name: K6_PROMETHEUS_RW_SERVER_URL
          value: "http://prometheus:9090"
```

## Monitoring & Observability

### Metrics Collection

```python
from performance_testing import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("perf_test_throughput", type="gauge")
collector.register_metric("perf_test_latency_p99", type="gauge")
collector.register_metric("perf_test_error_rate", type="gauge")
collector.register_metric("perf_test_virtual_users", type="gauge")

collector.set("perf_test_throughput", results.throughput)
collector.set("perf_test_latency_p99", results.p99_latency)
collector.set("perf_test_error_rate", results.error_rate)
collector.set("perf_test_virtual_users", results.virtual_users)
```

### Distributed Tracing

```python
from performance_testing import Tracer

tracer = Tracer(service="performance-test")

with tracer.start_span("load_test") as span:
    span.set_attribute("virtual_users", 100)
    span.set_attribute("duration_seconds", 300)
    
    with tracer.start_span("ramp_up"):
        ramp_up_phase()
    
    with tracer.start_span("sustained_load"):
        sustained_phase()
    
    span.set_attribute("total_requests", results.total_requests)
    span.set_attribute("avg_latency_ms", results.avg_response_time_ms)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from performance_testing import PerformanceTestFramework, LoadTestConfig

class TestPerformanceFramework:
    def setup_method(self):
        self.framework = PerformanceTestFramework()
    
    def test_create_load_test(self):
        config = LoadTestConfig(
            target_url="http://localhost:8080",
            virtual_users=10,
            duration_seconds=10,
        )
        test = self.framework.create_load_test(config)
        assert test is not None
    
    def test_execute_test(self):
        config = LoadTestConfig(
            target_url="http://localhost:8080",
            virtual_users=5,
            duration_seconds=5,
        )
        test = self.framework.create_load_test(config)
        results = self.framework.execute_test(test)
        assert results.status == "completed"
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Spike testing support
- **Added**: Memory leak detection
- **Improved**: 3x faster test execution
- **Fixed**: Distributed testing synchronization

## Glossary

| Term | Definition |
|------|------------|
| **Load Test** | Test under expected user load |
| **Stress Test** | Test beyond normal capacity |
| **Endurance Test** | Extended duration test |
| **Spike Test** | Test with sudden traffic surge |
| **Throughput** | Requests per second |
| **Latency** | Response time measurement |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/performance-testing.git
cd performance-testing
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Performance Testing Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Advanced Patterns

### Load Test Orchestration

```python
from performance_testing import LoadTestOrchestrator, OrchestrationConfig

orchestrator = LoadTestOrchestrator(
    config=OrchestrationConfig(
        phases=[
            {"name": "warmup", "users": 10, "duration": 60},
            {"name": "ramp_up", "users": 100, "duration": 120},
            {"name": "sustained", "users": 100, "duration": 300},
            {"name": "spike", "users": 500, "duration": 60},
            {"name": "cool_down", "users": 10, "duration": 60},
        ],
        metrics_collection=True,
        real_time_dashboard=True,
    ),
)

# Execute orchestrated load test
results = orchestrator.execute()
print(f"Peak throughput: {results.peak_throughput:.1f} req/s")
print(f"Average latency: {results.avg_latency_ms:.1f}ms")
```

### Performance Budget Monitoring

```python
from performance_testing import PerformanceBudget, BudgetConfig

budget = PerformanceBudget(
    config=BudgetConfig(
        budgets={
            "fcp_ms": 1500,
            "lcp_ms": 2500,
            "fid_ms": 100,
            "cls": 0.1,
            "ttfb_ms": 200,
            "page_load_ms": 3000,
        },
        alert_channels=["slack", "email"],
        threshold_warning=0.8,
        threshold_critical=0.95,
    ),
)

# Check performance budget
result = budget.check(current_metrics)
print(f"Budget status: {result.status}")
print(f"Violations: {result.violations}")
```

### Capacity Planning

```python
from performance_testing import CapacityPlanner, PlanningConfig

planner = CapacityPlanner(
    config=PlanningConfig(
        current_metrics=baseline_metrics,
        growth_rate=0.2,  # 20% monthly growth
        target_sla=99.9,
        planning_horizon_months=12,
    ),
)

# Generate capacity plan
plan = planner.plan()
print(f"Current capacity: {plan.current_capacity:.0f} req/s")
print(f"Projected demand: {plan.projected_demand:.0f} req/s")
print(f"Required scaling: {plan.scaling_factor:.1f}x")
print(f"Recommended infrastructure: {plan.recommendations}")
```

### Service Level Objective Monitoring

```python
from performance_testing import SLOMonitor, SLOConfig

slo_monitor = SLOMonitor(
    config=SLOConfig(
        objectives=[
            {"name": "availability", "target": 99.9, "window": "30d"},
            {"name": "latency_p99", "target": 500, "window": "7d"},
            {"name": "error_rate", "target": 0.1, "window": "24h"},
        ],
        alert_channels=["pagerduty"],
        burn_rate_threshold=2.0,
    ),
)

# Monitor SLOs
status = slo_monitor.check()
print(f"Availability SLO: {status.availability:.3f}%")
print(f"Latency SLO: {status.latency_p99:.1f}ms")
print(f"Error rate SLO: {status.error_rate:.3f}%")
print(f"SLO status: {status.overall_status}")
```

### Root Cause Analysis

```python
from performance_testing import RootCauseAnalyzer, AnalysisConfig

analyzer = RootCauseAnalyzer(
    config=AnalysisConfig(
        correlation_window_minutes=5,
        metrics_to_analyze=[
            "cpu_usage",
            "memory_usage",
            "disk_io",
            "network_io",
            "database_queries",
            "cache_hit_rate",
        ],
        ml_enabled=True,
    ),
)

# Analyze root cause
analysis = analyzer.analyze(
    incident_timestamp=datetime.utcnow(),
    symptoms=["latency_spike", "error_rate_increase"],
)

print(f"Root cause: {analysis.root_cause}")
print(f"Confidence: {analysis.confidence:.1%}")
print(f"Contributing factors: {analysis.contributing_factors}")
print(f"Recommended actions: {analysis.recommendations}")
```

### Performance Regression Detection

```python
from performance_testing import RegressionDetector, RegressionConfig

detector = RegressionDetector(
    config=RegressionConfig(
        baseline_metrics=baseline_metrics,
        comparison_window="7d",
        significance_level=0.05,
        min_effect_size=0.1,
        metrics_to_monitor=["latency_p99", "throughput", "error_rate"],
    ),
)

# Detect regressions
regressions = detector.detect(current_metrics)
for reg in regressions:
    print(f"Regression detected in {reg.metric}")
    print(f"  Baseline: {reg.baseline_value:.2f}")
    print(f"  Current: {reg.current_value:.2f}")
    print(f"  Change: {reg.change_percent:.1f}%")
    print(f"  Significance: {reg.p_value:.4f}")
```

### Load Test Data Management

```python
from performance_testing import TestDataManager, DataConfig

data_manager = DataManager(
    config=DataConfig(
        strategy="realistic",
        volume=1000000,
        distribution="pareto",
        correlations=True,
        PII_masking=True,
        seed=42,
    ),
)

# Generate test data
test_data = data_manager.generate()
print(f"Generated {len(test_data)} records")
print(f"Generation time: {data_manager.generation_time_seconds:.1f}s")
print(f"Data size: {data_manager.data_size_mb:.1f} MB")
```

### Geographic Distribution Testing

```python
from performance_testing import GeoTestOrchestrator, GeoConfig

geo_orchestrator = GeoTestOrchestrator(
    config=GeoConfig(
        regions=[
            {"name": "us-east-1", "users": 50, "weight": 0.4},
            {"name": "eu-west-1", "users": 30, "weight": 0.3},
            {"name": "ap-southeast-1", "users": 20, "weight": 0.3},
        ],
        test_duration_seconds=300,
        ramp_up_seconds=60,
    ),
)

# Execute geo-distributed test
results = geo_orchestrator.execute()
for region, result in results.items():
    print(f"{region}: {result.throughput:.1f} req/s, {result.latency_p99:.1f}ms")
```
