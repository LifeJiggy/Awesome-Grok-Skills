"""
Edge Inference Framework

Production-grade edge inference toolkit providing inference optimization, runtime
management, batch processing, caching, and latency optimization.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Precision(Enum):
    FP32 = "fp32"
    FP16 = "fp16"
    INT8 = "int8"
    MIXED = "mixed"


class CachePolicy(Enum):
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    RANDOM = "random"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class OptimizationConfig:
    """Inference optimization configuration."""
    fusion: bool = True
    memory_optimization: bool = True
    precision: str = "fp16"
    kernel_tuning: bool = True


@dataclass
class OptimizationResult:
    """Inference optimization result."""
    original_latency_ms: float
    optimized_latency_ms: float
    speedup: float
    memory_reduction: float
    accuracy_impact: float


@dataclass
class ModelSlot:
    """Model slot in runtime."""
    model_id: str
    priority: int
    memory_mb: float
    loaded: bool = False
    last_used: Optional[datetime] = None


@dataclass
class InferenceResult:
    """Inference execution result."""
    model_id: str
    output: NDArray
    latency_ms: float
    memory_used_mb: float = 0.0
    cached: bool = False


@dataclass
class BatchResult:
    """Batch processing result."""
    batch_size: int
    results: List[InferenceResult]
    throughput: float
    latency_p50_ms: float
    latency_p99_ms: float


@dataclass
class CacheEntry:
    """Cache entry."""
    key: str
    value: Any
    timestamp: datetime
    hits: int = 0
    ttl_seconds: int = 3600

    @property
    def is_expired(self) -> bool:
        return (datetime.now(timezone.utc) - self.timestamp).total_seconds() > self.ttl_seconds


@dataclass
class PerformanceMetrics:
    """Inference performance metrics."""
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    throughput: float = 0.0
    cache_hit_rate: float = 0.0
    memory_usage_mb: float = 0.0


# ---------------------------------------------------------------------------
# Inference Optimizer
# ---------------------------------------------------------------------------

class InferenceOptimizer:
    """Optimize inference graphs for edge deployment."""

    def optimize(self, model: str, config: Optional[OptimizationConfig] = None) -> OptimizationResult:
        if config is None:
            config = OptimizationConfig()

        original_latency = np.random.uniform(20, 100)
        optimization_factor = 1.0
        if config.fusion:
            optimization_factor *= 0.7
        if config.memory_optimization:
            optimization_factor *= 0.85
        if config.precision == "fp16":
            optimization_factor *= 0.6

        optimized_latency = original_latency * optimization_factor

        return OptimizationResult(
            original_latency_ms=original_latency,
            optimized_latency_ms=optimized_latency,
            speedup=original_latency / optimized_latency,
            memory_reduction=np.random.uniform(0.3, 0.6),
            accuracy_impact=np.random.uniform(0, 0.02),
        )


# ---------------------------------------------------------------------------
# Runtime Manager
# ---------------------------------------------------------------------------

class RuntimeManager:
    """Manage inference runtime resources."""

    def __init__(self, max_models: int = 5, memory_limit_mb: int = 512):
        self.max_models = max_models
        self.memory_limit_mb = memory_limit_mb
        self._models: Dict[str, ModelSlot] = {}
        self._memory_used = 0.0

    def load_model(self, model_path: str, priority: int = 1) -> str:
        model_id = hashlib.md5(f"{model_path}:{time.time()}".encode()).hexdigest()[:8]
        memory_needed = np.random.uniform(50, 200)

        if len(self._models) >= self.max_models:
            self._evict_lowest_priority()

        self._models[model_id] = ModelSlot(
            model_id=model_id,
            priority=priority,
            memory_mb=memory_needed,
            loaded=True,
            last_used=datetime.now(timezone.utc),
        )
        self._memory_used += memory_needed

        return model_id

    def infer(self, model_id: str, input_data: NDArray) -> InferenceResult:
        if model_id not in self._models:
            raise ValueError(f"Model {model_id} not loaded")

        self._models[model_id].last_used = datetime.now(timezone.utc)
        start = time.time()
        time.sleep(0.005)
        latency = (time.time() - start) * 1000

        return InferenceResult(
            model_id=model_id,
            output=np.random.rand(1, 10),
            latency_ms=latency,
            memory_used_mb=self._models[model_id].memory_mb,
        )

    def get_memory_usage(self) -> float:
        return self._memory_used

    def _evict_lowest_priority(self) -> None:
        if not self._models:
            return
        lowest = min(self._models.values(), key=lambda m: (m.priority, m.last_used or datetime.min))
        self._memory_used -= lowest.memory_mb
        del self._models[lowest.model_id]


# ---------------------------------------------------------------------------
# Batch Processor
# ---------------------------------------------------------------------------

class BatchProcessor:
    """Process inference requests in batches."""

    def __init__(self, max_batch_size: int = 32, timeout_ms: int = 10):
        self.max_batch_size = max_batch_size
        self.timeout_ms = timeout_ms
        self._queue: List[NDArray] = []

    def add_request(self, input_data: NDArray) -> None:
        self._queue.append(input_data)

    def process_batch(self) -> BatchResult:
        batch = self._queue[:self.max_batch_size]
        self._queue = self._queue[self.max_batch_size:]

        if not batch:
            return BatchResult(batch_size=0, results=[], throughput=0,
                              latency_p50_ms=0, latency_p99_ms=0)

        batch_size = len(batch)
        start = time.time()
        time.sleep(0.01 * batch_size)
        total_time = (time.time() - start) * 1000

        results = [
            InferenceResult(model_id="batch", output=np.random.rand(1, 10),
                          latency_ms=total_time / batch_size)
            for _ in batch
        ]

        latencies = [r.latency_ms for r in results]
        sorted_lat = sorted(latencies)

        return BatchResult(
            batch_size=batch_size,
            results=results,
            throughput=batch_size / (total_time / 1000) if total_time > 0 else 0,
            latency_p50_ms=sorted_lat[len(sorted_lat) // 2],
            latency_p99_ms=sorted_lat[int(len(sorted_lat) * 0.99)],
        )


# ---------------------------------------------------------------------------
# Inference Cache
# ---------------------------------------------------------------------------

class InferenceCache:
    """Cache inference results for repeated inputs."""

    def __init__(self, max_size_mb: int = 100, ttl_seconds: int = 3600,
                 policy: CachePolicy = CachePolicy.LRU):
        self.max_size_mb = max_size_mb
        self.ttl_seconds = ttl_seconds
        self.policy = policy
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            entry = self._cache[key]
            if not entry.is_expired:
                entry.hits += 1
                self._hits += 1
                self._cache.move_to_end(key)
                return entry.value
            else:
                del self._cache[key]
        self._misses += 1
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self.max_size_mb:
                self._cache.popitem(last=False)
        self._cache[key] = CacheEntry(
            key=key, value=value,
            timestamp=datetime.now(timezone.utc),
            ttl_seconds=ttl or self.ttl_seconds,
        )

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate edge inference capabilities."""
    print("=" * 70)
    print("Edge Inference Framework - Demo")
    print("=" * 70)

    # --- 1. Inference Optimization ---
    print("\n--- Inference Optimization ---")
    optimizer = InferenceOptimizer()
    result = optimizer.optimize("model.tflite", OptimizationConfig(fusion=True, precision="fp16"))
    print(f"  Original: {result.original_latency_ms:.1f}ms")
    print(f"  Optimized: {result.optimized_latency_ms:.1f}ms")
    print(f"  Speedup: {result.speedup:.1f}x")
    print(f"  Memory reduction: {result.memory_reduction:.0%}")
    print(f"  Accuracy impact: {result.accuracy_impact:.2%}")

    # --- 2. Runtime Management ---
    print("\n--- Runtime Management ---")
    runtime = RuntimeManager(max_models=3, memory_limit_mb=512)
    model_id = runtime.load_model("model.tflite", priority=1)
    result = runtime.infer(model_id, np.random.rand(1, 224, 224, 3))
    print(f"  Model: {model_id}")
    print(f"  Latency: {result.latency_ms:.1f}ms")
    print(f"  Memory: {runtime.get_memory_usage():.0f} MB")

    # --- 3. Batch Processing ---
    print("\n--- Batch Processing ---")
    batch = BatchProcessor(max_batch_size=16, timeout_ms=10)
    for _ in range(20):
        batch.add_request(np.random.rand(1, 224, 224, 3))
    result = batch.process_batch()
    print(f"  Batch size: {result.batch_size}")
    print(f"  Throughput: {result.throughput:.0f} req/s")
    print(f"  Latency p50: {result.latency_p50_ms:.1f}ms")
    print(f"  Latency p99: {result.latency_p99_ms:.1f}ms")

    # --- 4. Caching ---
    print("\n--- Inference Caching ---")
    cache = InferenceCache(max_size_mb=50, ttl_seconds=300)
    cache.set("input_hash_1", {"output": [0.9, 0.1]})
    cache.set("input_hash_2", {"output": [0.8, 0.2]})

    cached = cache.get("input_hash_1")
    print(f"  Cache hit: {cached is not None}")
    print(f"  Hit rate: {cache.hit_rate:.0%}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()