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
