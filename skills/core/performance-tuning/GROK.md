---
name: "performance-tuning"
category: "core"
version: "2.0.0"
tags: ["core", "performance", "profiling", "optimization", "benchmarks"]
---

# Performance Tuning

## Overview

The Performance Tuning module provides systematic approaches to identifying and resolving performance bottlenecks in software systems. It covers profiling methodologies, benchmarking frameworks, database query optimization, caching strategies, and runtime performance analysis across languages and platforms.

This skill is essential for performance engineers, backend developers, and SREs optimizing application performance and resource utilization.

## Core Capabilities

- **Profiling**: CPU profiling, memory profiling, I/O profiling, and flame graph generation
- **Benchmarking**: Micro-benchmarking, load testing, and comparative benchmarking frameworks
- **Database Optimization**: Query plan analysis, index optimization, N+1 detection, and connection pooling
- **Caching**: Multi-level caching strategies, cache invalidation patterns, and cache warming
- **Runtime Optimization**: JIT compilation awareness, garbage collection tuning, and memory layout optimization
- **Network Optimization**: Connection pooling, keep-alive, compression, and protocol optimization
- **Load Testing**: Stress testing, endurance testing, and capacity planning methodologies

## Usage Examples

```python
from performance_tuning import (
    Profiler,
    BenchmarkRunner,
    DBOptimizer,
    CacheStrategy,
    LoadTester,
)

# --- Profiling ---
profiler = Profiler()
profile = profiler.profile_function(
    target=my_function,
    args=(large_dataset,),
    profiler_type="memory",
)
print(f"Peak memory: {profile.peak_memory_mb:.1f} MB")
print(f"Allocations: {profile.allocations:,}")
print(f"Hotspots: {len(profile.hotspots)}")

# --- Benchmarking ---
runner = BenchmarkRunner()
result = runner.benchmark(
    functions=[solution_a, solution_b],
    input_sizes=[100, 1000, 10000],
    iterations=100,
)
for name, timings in result.results.items():
    print(f"  {name}: {timings['mean_ms']:.2f}ms (std: {timings['std_ms']:.2f}ms)")

# --- DB Optimization ---
db_opt = DBOptimizer()
analysis = db_opt.analyze_query(
    query="SELECT * FROM users WHERE email = ?",
    execution_plan=mock_plan,
)
print(f"Suggestions: {analysis.suggestions}")
print(f"Missing indexes: {analysis.missing_indexes}")

# --- Caching ---
cache = CacheStrategy()
strategy = cache.recommend(
    access_pattern="read_heavy",
    data_freshness="eventual",
    hit_rate_target=0.95,
)
print(f"Strategy: {strategy.level}")
print(f"Invalidation: {strategy.invalidation}")

# --- Load Testing ---
tester = LoadTester()
result = tester.run(
    target="https://api.example.com/health",
    concurrent_users=100,
    duration_seconds=60,
)
print(f"Throughput: {result.requests_per_second:.0f} req/s")
print(f"P99 latency: {result.p99_ms:.0f}ms")
print(f"Error rate: {result.error_rate:.2%}")
```

## Best Practices

- Always profile before optimizing — measure, don't guess
- Use statistical benchmarks with multiple iterations and warm-up
- Focus on the hottest code paths — 80/20 rule applies to performance
- Consider the full stack: code, database, network, and disk I/O
- Use flame graphs to identify optimization opportunities quickly
- Test with production-like data volumes and access patterns
- Monitor performance in production, not just in benchmarks
- Consider the cost/complexity vs. performance gain tradeoff
- Use A/B testing for performance optimizations in production
- Document performance baselines and regressions

## Related Modules

- **efficient-code**: Writing clean and efficient code
- **code-golf**: Extreme code minimization
- **algorithmic-art**: Algorithmic art and visualization
- **meme-code-hybrids**: Fun with code optimization

---

## Advanced Configuration

### Profiling Configuration

Configure profiling parameters for different environments.

```python
profiler_config = ProfilingConfig(
    production=ProfileConfig(
        sample_rate=0.01,
        max_overhead_ms=1,
        flame_graph_enabled=False,
    ),
    development=ProfileConfig(
        sample_rate=1.0,
        max_overhead_ms=100,
        flame_graph_enabled=True,
    ),
)
```

### Benchmark Configuration

Define benchmark parameters for consistent results.

```python
benchmark_config = BenchmarkConfig(
    iterations=100,
    warmup_iterations=10,
    min_time_ms=1000,
    max_time_ms=5000,
    statistical_confidence=0.95,
)
```

### Caching Configuration

Configure multi-level caching strategy.

```python
cache_config = CacheConfig(
    l1={"type": "memory", "max_size": 1000, "ttl_seconds": 60},
    l2={"type": "redis", "host": "redis", "port": 6379, "ttl_seconds": 300},
    l3={"type": "filesystem", "path": "/tmp/cache", "ttl_seconds": 3600},
    invalidation_strategy="write_through",
)
```

---

## Architecture Patterns

### Performance Budget Pattern

```python
class PerformanceBudget:
    def __init__(self, budgets):
        self.budgets = budgets

    def check(self, metrics):
        violations = []
        for metric, limit in self.budgets.items():
            if metrics[metric] > limit:
                violations.append(f"{metric}: {metrics[metric]} > {limit}")
        return violations

budget = PerformanceBudget({
    "api_latency_p99_ms": 200,
    "memory_usage_mb": 512,
    "cpu_usage_percent": 80,
})
```

### Cache-Aside Pattern

```python
class CacheAside:
    def __init__(self, cache, db):
        self.cache = cache
        self.db = db

    def get(self, key):
        value = self.cache.get(key)
        if value is None:
            value = self.db.query(key)
            self.cache.set(key, value, ttl=300)
        return value
```

### Connection Pool Pattern

```python
class ConnectionPool:
    def __init__(self, factory, max_size=20, min_size=5):
        self.pool = Queue(maxsize=max_size)
        for _ in range(min_size):
            self.pool.put(factory())

    @contextmanager
    def connection(self):
        conn = self.pool.get()
        try:
            yield conn
        finally:
            self.pool.put(conn)
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "closed"
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError()
        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

---

## Integration Guide

### Prometheus Integration

```python
from prometheus_client import Histogram, Counter, Gauge

REQUEST_LATENCY = Histogram('http_request_seconds', 'Request latency', ['method', 'endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'Total errors', ['status'])
ACTIVE_CONNECTIONS = Gauge('db_connections_active', 'Active DB connections')

@REQUEST_LATENCY.time()
def handle_request():
    pass
```

### Grafana Dashboard

```json
{
  "panels": [
    {"title": "P99 Latency", "query": "histogram_quantile(0.99, http_request_seconds)"},
    {"title": "Error Rate", "query": "rate(http_errors_total[5m])"},
    {"title": "Active Connections", "query": "db_connections_active"}
  ]
}
```

### Distributed Tracing (OpenTelemetry)

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def handle_request():
    with tracer.start_as_current_span("process_request") as span:
        span.set_attribute("request.id", request_id)
        result = process()
        span.set_attribute("result.size", len(result))
        return result
```

---

## Performance Optimization

### Database Query Optimization

```python
# N+1 Query Detection
class NPlusOneDetector:
    def __init__(self):
        self.query_counts = defaultdict(int)

    def track(self, query):
        self.query_counts[query] += 1

    def detect(self):
        return {q: c for q, c in self.query_counts.items() if c > 10}
```

### Memory Pool

```python
class MemoryPool:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.free_blocks = Queue()
        for _ in range(num_blocks):
            self.free_blocks.put(bytearray(block_size))

    def acquire(self):
        return self.free_blocks.get()

    def release(self, block):
        self.free_blocks.put(block)
```

### String Interning

```python
# Intern frequently used strings
interned_strings = {}

def intern_string(s):
    if s not in interned_strings:
        interned_strings[s] = s
    return interned_strings[s]
```

---

## Security Considerations

### Resource Exhaustion Prevention

```python
class ResourceLimiter:
    def __init__(self, max_memory_mb=512, max_cpu_seconds=30):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.max_cpu = max_cpu_seconds

    def check(self):
        usage = resource.getrusage(resource.RUSAGE_SELF)
        if usage.ru_maxrss > self.max_memory:
            raise ResourceExhausted("Memory limit exceeded")
```

---

## Troubleshooting Guide

### Performance Bottleneck Analysis

```python
analyzer = BottleneckAnalyzer()
bottlenecks = analyzer.analyze(
    profile_data=profile_results,
    threshold_ms=10,
)
for b in bottlenecks:
    print(f"{b.function}: {b.avg_ms:.1f}ms avg, {b.suggestion}")
```

### Memory Leak Detection

```python
tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

---

## API Reference

### Profiler

```python
class Profiler:
    def profile_function(target: Callable, args: tuple, profiler_type: str) -> ProfileResult
    def profile_code(code: str, globals_dict: dict) -> ProfileResult
    def generate_flame_graph(profile: ProfileResult) -> str
```

### BenchmarkRunner

```python
class BenchmarkRunner:
    def benchmark(functions: List[Callable], input_sizes: List[int],
                  iterations: int) -> BenchmarkResult
    def compare(function_a: Callable, function_b: Callable,
                input_sizes: List[int]) -> ComparisonResult
```

### CacheStrategy

```python
class CacheStrategy:
    def recommend(access_pattern: str, data_freshness: str,
                  hit_rate_target: float) -> CacheRecommendation
    def implement_lru(max_size: int, ttl_seconds: int) -> LRUCache
```

---

## Data Models

### ProfileResult

```python
@dataclass
class ProfileResult:
    function: str
    total_time_ms: float
    call_count: int
    avg_time_ms: float
    peak_memory_mb: float
    allocations: int
    hotspots: List[Hotspot]
```

### BenchmarkResult

```python
@dataclass
class BenchmarkResult:
    results: Dict[str, Dict[str, float]]
    statistical_significance: float
    winner: Optional[str]
```

---

## Deployment Guide

### Production Profiling

```python
# Safe production profiling
profiler = SafeProductionProfiler(
    sample_rate=0.01,
    max_overhead_ms=1,
    output_dir="/var/log/profiler",
)
profiler.start()
```

### Load Testing Setup

```bash
# k6 load test
k6 run --vus 100 --duration 60s load_test.js
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `request.latency.p99` | P99 latency | > 200ms |
| `memory.usage.mb` | Memory usage | > 512MB |
| `cpu.usage.percent` | CPU usage | > 80% |
| `cache.hit_rate` | Cache hit rate | < 0.9 |

---

## Testing Strategy

### Performance Tests

```python
def test_api_latency():
    runner = BenchmarkRunner()
    result = runner.benchmark(handle_request, input_sizes=[100], iterations=100)
    assert result.results["handle_request"]["p99_ms"] < 200
```

---

## Versioning & Migration

### Benchmark Versioning

Track benchmark results across versions for regression detection.

---

## Advanced Configuration (Extended)

### Profiling Configuration

Configure profiling parameters for different environments.

```python
profiler_config = ProfilingConfig(
    production=ProfileConfig(
        sample_rate=0.01,
        max_overhead_ms=1,
        flame_graph_enabled=False,
        memory_profiling=True,
        cpu_profiling=True,
    ),
    development=ProfileConfig(
        sample_rate=1.0,
        max_overhead_ms=100,
        flame_graph_enabled=True,
        memory_profiling=True,
        cpu_profiling=True,
    ),
)
```

### Benchmark Configuration

Define benchmark parameters for consistent results.

```python
benchmark_config = BenchmarkConfig(
    iterations=100,
    warmup_iterations=10,
    min_time_ms=1000,
    max_time_ms=5000,
    statistical_confidence=0.95,
    outlier_removal=True,
    parallel_execution=True,
)
```

### Caching Configuration

Configure multi-level caching strategy.

```python
cache_config = CacheConfig(
    l1={"type": "memory", "max_size": 1000, "ttl_seconds": 60},
    l2={"type": "redis", "host": "redis", "port": 6379, "ttl_seconds": 300},
    l3={"type": "filesystem", "path": "/tmp/cache", "ttl_seconds": 3600},
    invalidation_strategy="write_through",
    consistency_model="eventual",
)
```

---

## Architecture Patterns (Extended)

### Performance Budget Pattern

```python
class PerformanceBudget:
    def __init__(self, budgets):
        self.budgets = budgets
        self.measurements = []

    def check(self, metrics):
        violations = []
        for metric, limit in self.budgets.items():
            if metric in metrics:
                if metrics[metric] > limit:
                    violations.append({
                        'metric': metric,
                        'value': metrics[metric],
                        'limit': limit,
                        'overage_pct': (metrics[metric] - limit) / limit * 100,
                    })
        return violations
```

### Cache-Aside Pattern

```python
class CacheAside:
    def __init__(self, cache, db):
        self.cache = cache
        self.db = db

    def get(self, key):
        # Check cache first
        value = self.cache.get(key)
        if value is not None:
            return value
        
        # Cache miss - fetch from DB
        value = self.db.query(key)
        if value is not None:
            self.cache.set(key, value, ttl=300)
        return value

    def invalidate(self, key):
        self.cache.delete(key)
        self.db.invalidate(key)
```

### Connection Pool Pattern

```python
class ConnectionPool:
    def __init__(self, factory, max_size=20, min_size=5):
        self.factory = factory
        self.pool = Queue(maxsize=max_size)
        self.min_size = min_size
        
        # Pre-create minimum connections
        for _ in range(min_size):
            self.pool.put(factory())

    @contextmanager
    def connection(self):
        conn = self.pool.get()
        try:
            yield conn
        finally:
            self.pool.put(conn)
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "closed"
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError()
        
        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

### Rate Limiter Pattern

```python
class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def allow(self, key):
        now = time.time()
        window_start = now - self.window_seconds
        
        # Remove old requests
        self.requests[key] = [r for r in self.requests[key] if r > window_start]
        
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(now)
            return True
        return False
```

---

## Integration Guide (Extended)

### Prometheus Integration

```python
from prometheus_client import Histogram, Counter, Gauge, Summary

# Define metrics
REQUEST_LATENCY = Histogram('http_request_seconds', 'Request latency', ['method', 'endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'Total errors', ['status'])
ACTIVE_CONNECTIONS = Gauge('db_connections_active', 'Active DB connections')
REQUEST_SIZE = Summary('request_size_bytes', 'Request size', ['method'])

@REQUEST_LATENCY.time()
def handle_request():
    pass

@REQUEST_SIZE.time()
def process_request(request):
    return len(request.body)
```

### Grafana Dashboard

```json
{
  "panels": [
    {
      "title": "P99 Latency",
      "type": "graph",
      "query": "histogram_quantile(0.99, http_request_seconds_bucket)",
      "thresholds": [
        {"value": 0.2, "color": "red"}
      ]
    },
    {
      "title": "Error Rate",
      "type": "singlestat",
      "query": "rate(http_errors_total[5m]) / rate(http_requests_total[5m])"
    }
  ]
}
```

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

def handle_request():
    with tracer.start_as_current_span("process_request") as span:
        span.set_attribute("request.id", request_id)
        result = process()
        span.set_attribute("result.size", len(result))
        return result
```

---

## Performance Optimization (Extended)

### Database Query Optimization

```python
class QueryOptimizer:
    def __init__(self):
        self.query_stats = defaultdict(lambda: {'count': 0, 'total_time': 0})

    def analyze_query(self, query, execution_time):
        self.query_stats[query]['count'] += 1
        self.query_stats[query]['total_time'] += execution_time

    def get_slow_queries(self, threshold_ms=100):
        slow = []
        for query, stats in self.query_stats.items():
            avg_time = stats['total_time'] / stats['count']
            if avg_time > threshold_ms:
                slow.append({'query': query, 'avg_time': avg_time, 'count': stats['count']})
        return slow
```

### Memory Pool Implementation

```python
class MemoryPool:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.free_blocks = Queue()
        self.used_blocks = set()
        
        for _ in range(num_blocks):
            self.free_blocks.put(bytearray(block_size))

    def acquire(self):
        if self.free_blocks.empty():
            raise MemoryPoolExhausted()
        block = self.free_blocks.get()
        self.used_blocks.add(id(block))
        return block

    def release(self, block):
        if id(block) in self.used_blocks:
            self.used_blocks.remove(id(block))
            self.free_blocks.put(block)
```

### String Interning

```python
class StringInterner:
    def __init__(self):
        self.interned = {}

    def intern(self, s):
        if s not in self.interned:
            self.interned[s] = s
        return self.interned[s]

    def clear(self):
        self.interned.clear()
```

### Batch Processing

```python
class BatchProcessor:
    def __init__(self, batch_size=1000):
        self.batch_size = batch_size
        self.buffer = []

    def add(self, item):
        self.buffer.append(item)
        if len(self.buffer) >= self.batch_size:
            self.flush()

    def flush(self):
        if self.buffer:
            self.process_batch(self.buffer)
            self.buffer.clear()
```

---

## Security Considerations (Extended)

### Resource Exhaustion Prevention

```python
class ResourceLimiter:
    def __init__(self, max_memory_mb=512, max_cpu_seconds=30, max_open_files=1000):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.max_cpu = max_cpu_seconds
        self.max_open_files = max_open_files

    def check_resources(self):
        import resource, psutil
        
        # Check memory
        process = psutil.Process()
        if process.memory_info().rss > self.max_memory:
            raise ResourceExhausted("Memory limit exceeded")
        
        # Check CPU time
        cpu_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
        if cpu_time > self.max_cpu:
            raise ResourceExhausted("CPU time limit exceeded")
        
        # Check open files
        open_files = len(process.open_files())
        if open_files > self.max_open_files:
            raise ResourceExhausted("Too many open files")
```

### Input Validation

```python
class InputValidator:
    def validate_request_size(self, request, max_size_mb=10):
        if len(request.body) > max_size_mb * 1024 * 1024:
            raise RequestTooLarge(f"Request exceeds {max_size_mb}MB limit")

    def validate_query_complexity(self, query, max_complexity=10):
        complexity = self.calculate_complexity(query)
        if complexity > max_complexity:
            raise QueryTooComplex(f"Query complexity {complexity} exceeds limit")
```

---

## Troubleshooting Guide (Extended)

### Performance Bottleneck Analysis

```python
class BottleneckAnalyzer:
    def __init__(self):
        self.profiler = cProfile.Profile()

    def analyze(self, func, *args, **kwargs):
        self.profiler.enable()
        result = func(*args, **kwargs)
        self.profiler.disable()
        
        # Get top bottlenecks
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        return stats.print_stats(10)
```

### Memory Leak Detection

```python
class MemoryLeakDetector:
    def __init__(self):
        import tracemalloc
        tracemalloc.start()
        self.snapshots = []

    def take_snapshot(self):
        import tracemalloc
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append(snapshot)

    def compare_snapshots(self):
        if len(self.snapshots) < 2:
            return None
        top_stats = self.snapshots[-1].statistics('lineno')
        return top_stats[:10]
```

### CPU Profiling

```python
class CPUProfiler:
    def profile(self, func, *args, **kwargs):
        import cProfile
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        return result, profiler.getstats()
```

### Network Profiling

```python
class NetworkProfiler:
    def __init__(self):
        self.connections = []

    def profile_connection(self, host, port):
        import socket
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        latency = time.time() - start
        sock.close()
        return latency
```

---

## API Reference (Extended)

### Profiler (Extended)

```python
class Profiler:
    def profile_function(target: Callable, args: tuple, profiler_type: str) -> ProfileResult
    def profile_code(code: str, globals_dict: dict) -> ProfileResult
    def generate_flame_graph(profile: ProfileResult) -> str
    def compare_profiles(profile1: ProfileResult, profile2: ProfileResult) -> ComparisonResult
    def export_profile(profile: ProfileResult, format: str) -> str
```

### BenchmarkRunner (Extended)

```python
class BenchmarkRunner:
    def benchmark(functions: List[Callable], input_sizes: List[int],
                  iterations: int) -> BenchmarkResult
    def compare(function_a: Callable, function_b: Callable,
                input_sizes: List[int]) -> ComparisonResult
    def regression_test(baseline: BenchmarkResult, current: BenchmarkResult,
                        threshold_pct: float) -> RegressionResult
    def visualize_results(result: BenchmarkResult) -> str
```

### CacheStrategy (Extended)

```python
class CacheStrategy:
    def recommend(access_pattern: str, data_freshness: str,
                  hit_rate_target: float) -> CacheRecommendation
    def implement_lru(max_size: int, ttl_seconds: int) -> LRUCache
    def implement_write_through(cache, db) -> WriteThroughCache
    def implement_write_around(cache, db) -> WriteAroundCache
    def implement_write_back(cache, db) -> WriteBackCache
```

---

## Data Models (Extended)

### ProfileResult

```python
@dataclass
class ProfileResult:
    function: str
    total_time_ms: float
    call_count: int
    avg_time_ms: float
    peak_memory_mb: float
    allocations: int
    hotspots: List[Hotspot]
    flame_graph: Optional[str]
    cpu_usage_percent: float
```

### BenchmarkResult

```python
@dataclass
class BenchmarkResult:
    results: Dict[str, Dict[str, float]]
    statistical_significance: float
    winner: Optional[str]
    iterations: int
    warmup_iterations: int
    input_sizes: List[int]
    regression_detected: bool
```

---

## Deployment Guide (Extended)

### Production Profiling Setup

```python
# Safe production profiling
profiler = SafeProductionProfiler(
    sample_rate=0.01,
    max_overhead_ms=1,
    output_dir="/var/log/profiler",
    enable_flame_graphs=False,
    enable_memory_profiling=True,
)
profiler.start()

# Graceful shutdown
atexit.register(profiler.stop)
```

### Load Testing Setup

```bash
# k6 load test
k6 run --vus 100 --duration 60s load_test.js

# Locust load test
locust -f load_test.py --host=https://api.example.com

# Apache Bench
ab -n 10000 -c 100 https://api.example.com/endpoint
```

### A/B Testing Setup

```python
class PerformanceABTest:
    def __init__(self):
        self.variants = {}
        self.metrics = defaultdict(list)

    def add_variant(self, name, func):
        self.variants[name] = func

    def run_test(self, iterations=1000):
        for i in range(iterations):
            variant = random.choice(list(self.variants.keys()))
            start = time.time()
            self.variants[variant]()
            duration = time.time() - start
            self.metrics[variant].append(duration)

    def get_results(self):
        results = {}
        for variant, durations in self.metrics.items():
            results[variant] = {
                'mean': np.mean(durations),
                'p99': np.percentile(durations, 99),
                'std': np.std(durations),
            }
        return results
```

---

## Monitoring & Observability (Extended)

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `request.latency.p99` | P99 latency | > 200ms |
| `memory.usage.mb` | Memory usage | > 512MB |
| `cpu.usage.percent` | CPU usage | > 80% |
| `cache.hit_rate` | Cache hit rate | < 0.9 |
| `db.query.slow` | Slow queries | > 100ms |
| `connection.pool.active` | Active connections | > 80% |

---

## Testing Strategy (Extended)

### Performance Tests

```python
def test_api_latency():
    runner = BenchmarkRunner()
    result = runner.benchmark(handle_request, input_sizes=[100], iterations=100)
    assert result.results["handle_request"]["p99_ms"] < 200

def test_memory_usage():
    profiler = Profiler()
    result = profiler.profile_function(my_function, (large_dataset,), "memory")
    assert result.peak_memory_mb < 512

def test_cache_hit_rate():
    cache = CacheStrategy().implement_lru(max_size=1000, ttl_seconds=60)
    # Simulate access pattern
    for i in range(1000):
        cache.get(f"key_{i % 100}")
    assert cache.hit_rate > 0.9
```

---

## Versioning & Migration (Extended)

### Benchmark Versioning

Track benchmark results across versions for regression detection.

```python
class BenchmarkVersioner:
    def __init__(self):
        self.versions = {}

    def save_version(self, version_name, result):
        self.versions[version_name] = {
            'timestamp': time.time(),
            'result': result,
        }

    def compare_versions(self, v1, v2):
        r1 = self.versions[v1]['result']
        r2 = self.versions[v2]['result']
        return self.compare_results(r1, r2)
```

---

## Glossary (Extended)

| Term | Definition |
|------|-----------|
| **Flame Graph** | Visualization of stack traces showing time distribution |
| **P99 Latency** | 99th percentile latency |
| **Connection Pool** | Reusable database connections |
| **Circuit Breaker** | Pattern to prevent cascading failures |
| **Cache Hit Rate** | Percentage of cache hits vs misses |
| **Rate Limiter** | Controls request rate to prevent overload |
| **Memory Pool** | Pre-allocated memory blocks for reuse |
| **String Interning** | Sharing identical strings to save memory |
| **Batch Processing** | Processing multiple items together for efficiency |
| **Write-Through Cache** | Cache that writes to backing store synchronously |

---

## Changelog

### v2.0.0
- Added OpenTelemetry integration
- Circuit breaker pattern
- Connection pool optimization

### v1.0.0
- Initial release with profiling and benchmarking

---

## Contributing Guidelines

- Always benchmark before and after changes
- Document performance impact in PRs
- Include profiling results for significant changes

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
