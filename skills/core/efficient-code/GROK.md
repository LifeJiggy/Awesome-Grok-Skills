---
name: "efficient-code"
category: "core"
version: "2.0.0"
tags: ["core", "efficient-code", "optimization", "performance", "best-practices"]
---

# Efficient Code

## Overview

The Efficient Code module provides comprehensive guidance for writing clean, performant, and maintainable code across programming languages. It covers algorithm selection, data structure optimization, memory management, concurrency patterns, and code quality metrics. The module emphasizes practical optimization techniques with measurable impact.

This skill is essential for software engineers seeking to write code that is both correct and performant, and for tech leads establishing coding standards for their teams.

## Core Capabilities

- **Algorithm Selection**: Choosing optimal algorithms based on time/space complexity and input characteristics
- **Data Structure Optimization**: Selecting and implementing data structures for specific access patterns
- **Memory Management**: Object pooling, lazy evaluation, flyweight patterns, and memory-efficient data representations
- **Concurrency**: Thread-safe patterns, async/await optimization, lock-free data structures, and parallel processing
- **Code Quality**: Cyclomatic complexity, function length guidelines, naming conventions, and DRY principle application
- **Profiling**: Identifying bottlenecks, flame graph analysis, and systematic optimization approaches
- **Language-Specific**: Python, JavaScript, Go, Rust, and Java optimization idioms

## Usage Examples

```python
from efficient_code import (
    ComplexityAnalyzer,
    DataStructureSelector,
    MemoryOptimizer,
    ConcurrencyHelper,
    CodeQualityChecker,
)

# --- Complexity Analysis ---
analyzer = ComplexityAnalyzer()
analysis = analyzer.analyze_function(
    code="for i in range(n): for j in range(n): pass",
    input_sizes=[100, 1000, 10000],
)
print(f"Time complexity: {analysis.time_complexity}")
print(f"Space complexity: {analysis.space_complexity}")

# --- Data Structure Selection ---
selector = DataStructureSelector()
recommendation = selector.recommend(
    operations=["insert", "lookup", "delete"],
    access_pattern="random",
    size_estimate=100000,
    ordering_required=False,
)
print(f"Recommended: {recommendation.structure}")
print(f"Reason: {recommendation.reasoning}")

# --- Memory Optimization ---
optimizer = MemoryOptimizer()
suggestions = optimizer.analyze(
    code_sample="large_list = [dict() for _ in range(1000000)]",
    language="python",
)
for suggestion in suggestions:
    print(f"  {suggestion}")

# --- Concurrency ---
helper = ConcurrencyHelper()
pattern = helper.recommend_pattern(
    task_type="io_bound",
    parallelism_needed=True,
    shared_state=True,
)
print(f"Pattern: {pattern.name}")
print(f"Implementation: {pattern.implementation}")

# --- Code Quality ---
checker = CodeQualityChecker()
issues = checker.check("def f(x): return x+1 if x>0 else None")
for issue in issues:
    print(f"  [{issue.severity}] {issue.message}")
```

## Best Practices

- Profile before optimizing — premature optimization is the root of all evil
- Choose the right algorithm first, then optimize the implementation
- Use appropriate data structures: hash maps for lookups, arrays for sequential access
- Minimize object allocation in hot paths — use object pools where appropriate
- Prefer iteration over recursion for deep call stacks
- Use lazy evaluation to defer expensive computations until needed
- Apply the principle of least astonishment in API design
- Keep functions small and focused — single responsibility principle
- Write self-documenting code with clear naming — comments should explain WHY, not WHAT
- Measure everything — use benchmarks to validate optimization claims

## Related Modules

- **performance-tuning**: Runtime performance profiling and optimization
- **code-golf**: Minimal code solutions for educational purposes
- **algorithmic-art**: Creative algorithm implementations
- **meme-code-hybrids**: Fun and educational code patterns

---

## Advanced Configuration

### Complexity Thresholds

Configure acceptable complexity thresholds for your codebase.

```python
analyzer = ComplexityAnalyzer(
    thresholds={
        "cyclomatic": 10,
        "cognitive": 15,
        "function_length": 50,
        "class_length": 500,
        "nesting_depth": 4,
    },
    severity="warning",
)
```

### Optimization Profiles

Define optimization profiles for different contexts.

```python
profiles = {
    "production": OptimizationProfile(
        priority="latency",
        trade_space="memory",
        target_p99_ms=100,
    ),
    "batch": OptimizationProfile(
        priority="throughput",
        trade_space="cpu",
        target_batch_size=10000,
    ),
}
```

### Code Quality Rules

Customize code quality rules for your team.

```python
quality_rules = CodeQualityRules(
    rules=[
        {"name": "no_nested_loops", "max_depth": 2, "severity": "warning"},
        {"name": "function_length", "max_lines": 50, "severity": "error"},
        {"name": "argument_count", "max_args": 5, "severity": "warning"},
    ],
)
```

---

## Architecture Patterns

### Algorithm Selection Strategy

```python
# Decision tree for algorithm selection
def select_algorithm(operation_type, data_size, access_pattern):
    if operation_type == "search":
        if access_pattern == "sequential":
            return BinarySearch if is_sorted else LinearSearch
        elif access_pattern == "random":
            return HashMapLookup if data_size > 1000 else LinearScan
    elif operation_type == "sort":
        if data_size < 50:
            return InsertionSort
        elif data_size < 10000:
            return TimSort
        else:
            return ParallelMergeSort
```

### Memory Layout Optimization

```python
# Struct of Arrays vs Array of Structs
class ParticleAoS:  # Array of Structs
    def __init__(self):
        self.particles = [{"x": 0, "y": 0, "z": 0, "mass": 1.0} for _ in range(N)]

class ParticleSoA:  # Struct of Arrays
    def __init__(self):
        self.x = array('f', [0.0] * N)
        self.y = array('f', [0.0] * N)
        self.z = array('f', [0.0] * N)
        self.mass = array('f', [1.0] * N)
# SoA: 3-5x faster for cache-friendly iteration
```

### Concurrency Patterns

```python
# Producer-Consumer with backpressure
from queue import Queue
from threading import Thread

def producer_consumer_pattern():
    queue = Queue(maxsize=100)  # Backpressure
    def producer():
        while True:
            item = produce()
            queue.put(item)  # Blocks if full
    def consumer():
        while True:
            item = queue.get()  # Blocks if empty
            process(item)
            queue.task_done()
```

### Lazy Evaluation Patterns

```python
# Lazy list with memoization
class LazyList:
    def __init__(self, generator):
        self._generator = generator
        self._cache = []
        self._exhausted = False

    def __getitem__(self, index):
        while len(self._cache) <= index and not self._exhausted:
            try:
                self._cache.append(next(self._generator))
            except StopIteration:
                self._exhausted = True
                raise IndexError
        return self._cache[index]
```

---

## Integration Guide

### Python Integration

```python
# Using efficient_code for optimization
from efficient_code import ComplexityAnalyzer, DataStructureSelector

analyzer = ComplexityAnalyzer()
analysis = analyzer.analyze_function(my_function)
if analysis.time_complexity == "O(n^2)":
    suggestion = DataStructureSelector().recommend(
        operations=analysis.detected_operations,
        size_estimate=analysis.estimated_input_size,
    )
    print(f"Optimize with: {suggestion.structure}")
```

### JavaScript Integration

```javascript
// Using efficient patterns in JS
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};
```

### Go Integration

```go
// Using efficient patterns in Go
type ObjectPool struct {
    pool sync.Pool
}

func NewObjectPool() *ObjectPool {
    return &ObjectPool{
        pool: sync.Pool{
            New: func() interface{} {
                return &bytes.Buffer{}
            },
        },
    }
}
```

---

## Performance Optimization

### Hot Path Optimization

```python
# Identify and optimize hot paths
profiler = HotPathProfiler()
hot_paths = profiler.find_hot_paths(
    code=application_code,
    threshold_ms=10,
)
for path in hot_paths:
    print(f"Hot path: {path.function} ({path.avg_ms:.1f}ms avg)")
    print(f"  Optimization: {path.suggested_optimization}")
```

### Object Pool Pattern

```python
# Reuse objects to reduce allocation pressure
class ObjectPool:
    def __init__(self, factory, max_size=100):
        self.factory = factory
        self.pool = Queue(maxsize=max_size)

    def acquire(self):
        if not self.pool.empty():
            return self.pool.get()
        return self.factory()

    def release(self, obj):
        if self.pool.qsize() < self.pool.maxsize:
            self.pool.put(obj)
```

### Vectorization

```python
# Vectorize operations for numpy arrays
import numpy as np

# Slow: Python loop
result = [x * 2 for x in range(1000000)]

# Fast: Vectorized numpy
result = np.arange(1000000) * 2
# 10-100x faster
```

---

## Security Considerations

### Input Validation

```python
# Validate inputs to prevent injection and overflow
def safe_index(arr, index):
    if not isinstance(index, int):
        raise TypeError("Index must be integer")
    if index < 0 or index >= len(arr):
        raise IndexError("Index out of bounds")
    return arr[index]
```

### Resource Limits

```python
# Prevent DoS via resource exhaustion
import resource

def set_limits():
    # Max 1GB memory
    resource.setrlimit(resource.RLIMIT_AS, (1024*1024*1024, -1))
    # Max 1000 files open
    resource.setrlimit(resource.RLIMIT_NOFILE, (1000, 1000))
```

---

## Troubleshooting Guide

### Performance Regression Detection

```python
regression = PerformanceRegressionDetector(
    baseline_metrics=baseline,
    current_metrics=current,
    threshold_pct=10,
)
if regression.detected:
    print(f"Regression in {regression.affected_functions}")
```

### Memory Leak Detection

```python
leak_detector = MemoryLeakDetector(
    sample_interval_mb=10,
    growth_threshold_pct=10,
)
leak_detector.start_monitoring()
```

---

## API Reference

### ComplexityAnalyzer

```python
class ComplexityAnalyzer:
    def analyze_function(code: str, input_sizes: List[int]) -> ComplexityResult
    def analyze_class(code: str) -> ClassComplexityResult
    def compare_implementations(code_a: str, code_b: str) -> ComparisonResult
```

### DataStructureSelector

```python
class DataStructureSelector:
    def recommend(operations: List[str], access_pattern: str,
                  size_estimate: int, ordering_required: bool) -> Recommendation
```

### MemoryOptimizer

```python
class MemoryOptimizer:
    def analyze(code_sample: str, language: str) -> List[MemorySuggestion]
    def estimate_memory_usage(code: str) -> MemoryEstimate
```

---

## Data Models

### ComplexityResult

```python
@dataclass
class ComplexityResult:
    time_complexity: str  # O(n), O(n log n), O(n^2)
    space_complexity: str
    best_case: str
    worst_case: str
    average_case: str
```

### Recommendation

```python
@dataclass
class Recommendation:
    structure: str
    reasoning: str
    time_complexity: str
    space_complexity: str
    tradeoffs: List[str]
```

---

## Deployment Guide

### Profiling in Production

```python
# Safe profiling in production
profiler = SafeProductionProfiler(
    sample_rate=0.01,  # 1% of requests
    max_overhead_ms=1,
    output="profiler_results",
)
profiler.start()
```

### CI/CD Integration

```yaml
# GitHub Actions workflow
- name: Run efficiency checks
  run: |
    python -m efficient_code analyze src/ --max-complexity 10
    python -m efficient_code benchmark src/ --min-improvement 5%
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `code.complexity.cyclomatic` | Cyclomatic complexity | > 10 |
| `code.complexity.cognitive` | Cognitive complexity | > 15 |
| `code.function.length.lines` | Function length | > 50 |
| `code.nesting.depth` | Maximum nesting depth | > 4 |

---

## Testing Strategy

### Complexity Tests

```python
def test_function_complexity():
    analyzer = ComplexityAnalyzer()
    result = analyzer.analyze_function("def f(x): return x + 1")
    assert result.time_complexity == "O(1)"
    assert result.space_complexity == "O(1)"
```

---

## Versioning & Migration

### Version Policy

Follow semantic versioning for API changes. Minor versions for new optimizations, major for breaking changes.

---

## Advanced Configuration (Extended)

### Code Quality Thresholds

Configure thresholds for different code quality metrics.

```python
quality_thresholds = QualityThresholds(
    cyclomatic_complexity=10,
    cognitive_complexity=15,
    function_length=50,
    class_length=500,
    nesting_depth=4,
    parameter_count=5,
    return_statement_count=3,
    duplicate_lines_percentage=5,
)
```

### Optimization Profiles

Define optimization profiles for different contexts.

```python
optimization_profiles = {
    "production": OptimizationProfile(
        priority="latency",
        trade_space="memory",
        target_p99_ms=100,
        max_memory_mb=512,
    ),
    "batch": OptimizationProfile(
        priority="throughput",
        trade_space="cpu",
        target_batch_size=10000,
        max_duration_seconds=300,
    ),
    "embedded": OptimizationProfile(
        priority="memory",
        trade_space="cpu",
        max_memory_kb=64,
        max_code_size_kb=32,
    ),
}
```

### Language-Specific Rules

Configure rules per programming language.

```python
language_rules = {
    "python": {
        "max_line_length": 88,
        "use_type_hints": True,
        "prefer_comprehensions": True,
    },
    "javascript": {
        "max_line_length": 100,
        "use_strict": True,
        "prefer_const": True,
    },
    "go": {
        "max_line_length": 120,
        "gofmt": True,
        "golint": True,
    },
}
```

---

## Architecture Patterns (Extended)

### Algorithm Selection Framework

```python
class AlgorithmSelector:
    def __init__(self):
        self.algorithms = {}
        self.benchmarks = {}

    def register(self, name, algorithm, complexity):
        self.algorithms[name] = {
            'func': algorithm,
            'time_complexity': complexity['time'],
            'space_complexity': complexity['space'],
        }

    def select(self, operation_type, data_size, constraints):
        candidates = self.filter_by_constraints(constraints)
        return self.rank_by_complexity(candidates, data_size)
```

### Data Structure Recommendation Engine

```python
class DataStructureRecommender:
    def __init__(self):
        self.recommendations = {
            'lookup': {'hash_map': 'O(1)', 'tree': 'O(log n)'},
            'ordered': {'tree': 'O(log n)', 'sorted_array': 'O(log n)'},
            'sequential': {'array': 'O(1)', 'linked_list': 'O(1)'},
        }

    def recommend(self, operations, size, ordering_required):
        if ordering_required:
            return 'tree'
        if 'lookup' in operations and size > 1000:
            return 'hash_map'
        return 'array'
```

### Memory Layout Optimizer

```python
class MemoryLayoutOptimizer:
    def optimize_struct(self, fields):
        # Sort fields by size for optimal alignment
        sorted_fields = sorted(fields, key=lambda f: f.size, reverse=True)
        return StructLayout(sorted_fields)

    def optimize_array(self, array_type, access_pattern):
        if access_pattern == 'sequential':
            return ArrayOfStructs(array_type)
        elif access_pattern == 'random':
            return StructOfArrays(array_type)
```

---

## Integration Guide (Extended)

### Python Integration

```python
# Using efficient_code for optimization
from efficient_code import ComplexityAnalyzer, DataStructureSelector

analyzer = ComplexityAnalyzer()
analysis = analyzer.analyze_function(my_function)

if analysis.time_complexity == "O(n^2)":
    suggestion = DataStructureSelector().recommend(
        operations=analysis.detected_operations,
        size_estimate=analysis.estimated_input_size,
    )
    print(f"Optimize with: {suggestion.structure}")
```

### JavaScript Integration

```javascript
// Using efficient patterns in JS
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};

const fastDebounce = (fn, ms) => {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
};
```

### Go Integration

```go
// Using efficient patterns in Go
type ObjectPool struct {
    pool sync.Pool
}

func NewObjectPool() *ObjectPool {
    return &ObjectPool{
        pool: sync.Pool{
            New: func() interface{} {
                return &bytes.Buffer{}
            },
        },
    }
}

// Concurrent map operations
func ConcurrentMapProcess(input map[string]int, workers int) map[string]int {
    result := make(map[string]int)
    var mu sync.Mutex
    var wg sync.WaitGroup
    
    for key, value := range input {
        wg.Add(1)
        go func(k string, v int) {
            defer wg.Done()
            processed := processValue(v)
            mu.Lock()
            result[k] = processed
            mu.Unlock()
        }(key, value)
    }
    wg.Wait()
    return result
}
```

---

## Performance Optimization (Extended)

### Hot Path Optimization

```python
class HotPathOptimizer:
    def __init__(self):
        self.profiler = Profiler()
        self.optimizer = Optimizer()

    def optimize_hot_paths(self, code, threshold_ms=10):
        profile = self.profiler.profile(code)
        hot_paths = [p for p in profile if p.avg_ms > threshold_ms]
        
        optimizations = []
        for path in hot_paths:
            opt = self.optimizer.optimize(path)
            optimizations.append(opt)
        
        return optimizations
```

### Object Pool Implementation

```python
class ObjectPool:
    def __init__(self, factory, max_size=100):
        self.factory = factory
        self.pool = Queue(maxsize=max_size)
        self.active_count = 0

    @contextmanager
    def acquire(self):
        obj = self.pool.get() if not self.pool.empty() else self.factory()
        self.active_count += 1
        try:
            yield obj
        finally:
            self.active_count -= 1
            if self.pool.qsize() < self.pool.maxsize:
                self.pool.put(obj)
```

### Vectorization Patterns

```python
# Vectorized operations with NumPy
import numpy as np

def vectorized_distance(points1, points2):
    # Vectorized Euclidean distance
    diff = points1 - points2
    return np.sqrt(np.sum(diff ** 2, axis=1))

def vectorized_filter(array, condition):
    return array[condition]

def vectorized_aggregate(array, groups, func):
    return np.array([func(array[groups == g]) for g in np.unique(groups)])
```

### String Optimization

```python
# Efficient string operations
def efficient_string_concat(strings):
    # Use join instead of + for multiple concatenations
    return ''.join(strings)

def efficient_string_search(haystack, needle):
    # Use built-in search methods
    return needle in haystack

def efficient_regex(text, pattern):
    # Compile regex for reuse
    compiled = re.compile(pattern)
    return compiled.findall(text)
```

---

## Security Considerations (Extended)

### Input Validation

```python
class InputValidator:
    def validate_integer(self, value, min_val=None, max_val=None):
        if not isinstance(value, int):
            raise TypeError("Value must be integer")
        if min_val is not None and value < min_val:
            raise ValueError(f"Value must be >= {min_val}")
        if max_val is not None and value > max_val:
            raise ValueError(f"Value must be <= {max_val}")
        return value

    def validate_string(self, value, max_length=None, pattern=None):
        if not isinstance(value, str):
            raise TypeError("Value must be string")
        if max_length and len(value) > max_length:
            raise ValueError(f"String too long (max {max_length})")
        if pattern and not re.match(pattern, value):
            raise ValueError("String doesn't match pattern")
        return value
```

### Resource Limits

```python
class ResourceLimiter:
    def __init__(self, max_memory_mb=512, max_cpu_seconds=30):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.max_cpu = max_cpu_seconds

    def check_memory(self):
        import psutil
        process = psutil.Process()
        if process.memory_info().rss > self.max_memory:
            raise MemoryError("Memory limit exceeded")

    def check_cpu(self):
        import signal
        def timeout_handler(signum, frame):
            raise TimeoutError("CPU time limit exceeded")
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.max_cpu)
```

---

## Troubleshooting Guide (Extended)

### Performance Regression Detection

```python
class PerformanceRegressionDetector:
    def __init__(self):
        self.baselines = {}

    def set_baseline(self, metric_name, value):
        self.baselines[metric_name] = value

    def detect_regression(self, metric_name, current_value, threshold_pct=10):
        baseline = self.baselines.get(metric_name)
        if baseline:
            regression = (current_value - baseline) / baseline * 100
            if regression > threshold_pct:
                return True, regression
        return False, 0
```

### Memory Leak Detection

```python
class MemoryLeakDetector:
    def __init__(self):
        self.snapshots = []

    def take_snapshot(self):
        import tracemalloc
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append(snapshot)

    def detect_leak(self):
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

---

## API Reference (Extended)

### ComplexityAnalyzer (Extended)

```python
class ComplexityAnalyzer:
    def analyze_function(code: str, input_sizes: List[int]) -> ComplexityResult
    def analyze_class(code: str) -> ClassComplexityResult
    def compare_implementations(code_a: str, code_b: str) -> ComparisonResult
    def estimate_runtime(code: str, input_size: int) -> RuntimeEstimate
    def suggest_optimization(code: str) -> List[OptimizationSuggestion]
```

### DataStructureSelector (Extended)

```python
class DataStructureSelector:
    def recommend(operations: List[str], access_pattern: str,
                  size_estimate: int, ordering_required: bool) -> Recommendation
    def compare(structures: List[str], operations: List[str]) -> ComparisonResult
    def benchmark(structure: str, operations: List[str], sizes: List[int]) -> BenchmarkResult
```

### MemoryOptimizer (Extended)

```python
class MemoryOptimizer:
    def analyze(code_sample: str, language: str) -> List[MemorySuggestion]
    def estimate_memory_usage(code: str) -> MemoryEstimate
    def profile_memory(target: Callable, args: tuple) -> MemoryProfile
    def suggest_pooling(code: str) -> PoolingSuggestion
```

---

## Data Models (Extended)

### ComplexityResult

```python
@dataclass
class ComplexityResult:
    time_complexity: str  # O(n), O(n log n), O(n^2)
    space_complexity: str
    best_case: str
    worst_case: str
    average_case: str
    cyclomatic_complexity: int
    cognitive_complexity: int
```

### Recommendation

```python
@dataclass
class Recommendation:
    structure: str
    reasoning: str
    time_complexity: str
    space_complexity: str
    tradeoffs: List[str]
    implementation_example: str
    benchmark_results: Optional[dict]
```

### OptimizationSuggestion

```python
@dataclass
class OptimizationSuggestion:
    category: str  # algorithm, data_structure, memory, concurrency
    description: str
    estimated_improvement: str
    complexity_change: str
    code_example: str
    priority: int
```

---

## Deployment Guide (Extended)

### CI/CD Integration

```yaml
# GitHub Actions workflow
name: Code Efficiency Checks
on: [push, pull_request]
jobs:
  efficiency:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run efficiency analysis
        run: |
          python -m efficient_code analyze src/ --max-complexity 10
          python -m efficient_code benchmark src/ --min-improvement 5%
      - name: Check for regressions
        run: |
          python -m efficient_code compare --baseline main --current HEAD
```

### Production Profiling

```python
class ProductionProfiler:
    def __init__(self):
        self.sampler = Sampler(sample_rate=0.01)
        self.analyzer = HotPathAnalyzer()

    def profile_in_production(self):
        while True:
            request = self.sampler.sample_request()
            profile = self.analyzer.analyze(request)
            if profile.is_hot_path:
                self.alert(profile)
```

---

## Monitoring & Observability (Extended)

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `code.complexity.cyclomatic` | Cyclomatic complexity | > 10 |
| `code.complexity.cognitive` | Cognitive complexity | > 15 |
| `code.function.length.lines` | Function length | > 50 |
| `code.nesting.depth` | Maximum nesting depth | > 4 |
| `code.duplicate.lines` | Duplicate lines percentage | > 5% |
| `code.memory.allocations` | Memory allocations per call | > 1000 |

---

## Testing Strategy (Extended)

### Complexity Tests

```python
def test_function_complexity():
    analyzer = ComplexityAnalyzer()
    result = analyzer.analyze_function("def f(x): return x + 1")
    assert result.time_complexity == "O(1)"
    assert result.space_complexity == "O(1)"
    assert result.cyclomatic_complexity == 1

def test_optimization_suggestion():
    analyzer = ComplexityAnalyzer()
    suggestions = analyzer.suggest_optimization(
        "for i in range(n): for j in range(n): pass"
    )
    assert len(suggestions) > 0
    assert suggestions[0].category == "algorithm"
```

---

## Versioning & Migration (Extended)

### Version Policy

Follow semantic versioning for API changes. Minor versions for new optimizations, major for breaking changes.

---

## Glossary (Extended)

| Term | Definition |
|------|-----------|
| **Cyclomatic Complexity** | Number of independent paths through code |
| **Cognitive Complexity** | How difficult code is to understand |
| **Flyweight Pattern** | Share common state to reduce memory |
| **Object Pool** | Reuse objects to reduce allocation |
| **Lazy Evaluation** | Defer computation until needed |
| **Vectorization** | Applying operations to entire arrays at once |
| **Hot Path** | Code section that executes frequently |
| **Memory Pool** | Pre-allocated memory for reuse |
| **String Interning** | Sharing identical strings to save memory |
| **Tail Call Optimization** | Recursion optimization by compiler |

---

## Changelog

### v2.0.0
- Added cognitive complexity analysis
- Memory optimization suggestions
- Concurrency pattern recommendations

### v1.0.0
- Initial release with algorithm analysis
- Data structure recommendations

---

## Contributing Guidelines

- Benchmark before and after optimizations
- Document performance tradeoffs
- Include complexity analysis in PR descriptions

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
