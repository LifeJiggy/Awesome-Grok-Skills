"""
GraphQL Performance Implementation

This module provides comprehensive GraphQL performance optimization patterns including:
- Query complexity analysis
- Persisted queries
- Caching strategies
- Batching techniques
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import asyncio
import hashlib
import json
import time
from collections import defaultdict
from functools import lru_cache
import uuid


# Enums
class CacheStrategy(Enum):
    """Caching strategies."""
    NO_CACHE = auto()
    IN_MEMORY = auto()
    REDIS = auto()
    CDN = auto()
    HYBRID = auto()


class QueryComplexityLevel(Enum):
    """Query complexity levels."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


class PerformanceMetric(Enum):
    """Performance metrics."""
    QUERY_TIME = auto()
    CACHE_HIT_RATE = auto()
    COMPLEXITY_SCORE = auto()
    ERROR_RATE = auto()
    THROUGHPUT = auto()


# Dataclasses
@dataclass
class ComplexityRule:
    """Rule for calculating query complexity."""
    field_name: str
    base_cost: int
    multiplier_field: Optional[str] = None
    multiplier_factor: int = 1
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'fieldName': self.field_name,
            'baseCost': self.base_cost,
            'multiplierField': self.multiplier_field,
            'multiplierFactor': self.multiplier_factor,
            'description': self.description
        }


@dataclass
class QueryComplexity:
    """Query complexity result."""
    total_cost: int
    max_cost: int
    level: QueryComplexityLevel
    field_costs: Dict[str, int]
    is_valid: bool
    message: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'totalCost': self.total_cost,
            'maxCost': self.max_cost,
            'level': self.level.name,
            'fieldCosts': self.field_costs,
            'isValid': self.is_valid,
            'message': self.message
        }


@dataclass
class CacheEntry:
    """Cache entry."""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    ttl: int = 300  # seconds
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)

    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return datetime.now() > self.created_at + timedelta(seconds=self.ttl)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'key': self.key,
            'createdAt': self.created_at.isoformat(),
            'ttl': self.ttl,
            'accessCount': self.access_count,
            'lastAccessed': self.last_accessed.isoformat(),
            'isExpired': self.is_expired()
        }


@dataclass
class PerformanceMetrics:
    """Performance metrics for monitoring."""
    total_queries: int = 0
    average_query_time: float = 0.0
    p95_query_time: float = 0.0
    p99_query_time: float = 0.0
    cache_hit_rate: float = 0.0
    error_rate: float = 0.0
    complexity_score: float = 0.0
    throughput: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'totalQueries': self.total_queries,
            'averageQueryTime': self.average_query_time,
            'p95QueryTime': self.p95_query_time,
            'p99QueryTime': self.p99_query_time,
            'cacheHitRate': self.cache_hit_rate,
            'errorRate': self.error_rate,
            'complexityScore': self.complexity_score,
            'throughput': self.throughput,
            'lastUpdated': self.last_updated.isoformat()
        }


@dataclass
class PersistedQuery:
    """Persisted query definition."""
    hash: str
    query: str
    name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'hash': self.hash,
            'query': self.query[:100] + '...' if len(self.query) > 100 else self.query,
            'name': self.name,
            'createdAt': self.created_at.isoformat(),
            'accessCount': self.access_count,
            'lastAccessed': self.last_accessed.isoformat()
        }


@dataclass
class QueryPlan:
    """Query execution plan."""
    steps: List[Dict[str, Any]]
    estimated_time: float
    parallelizable_steps: List[int]
    cacheable_steps: List[int]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'steps': self.steps,
            'estimatedTime': self.estimated_time,
            'parallelizableSteps': self.parallelizable_steps,
            'cacheableSteps': self.cacheable_steps
        }


# Query Complexity Analyzer
class QueryComplexityAnalyzer:
    """Analyze query complexity."""
    
    def __init__(self, max_complexity: int = 1000):
        self.max_complexity = max_complexity
        self.complexity_rules: List[ComplexityRule] = []
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default complexity rules."""
        default_rules = [
            ComplexityRule("user", 5, description="Single user query"),
            ComplexityRule("users", 10, "first", 10, "User list with pagination"),
            ComplexityRule("post", 3, description="Single post query"),
            ComplexityRule("posts", 8, "first", 10, "Post list with pagination"),
            ComplexityRule("comments", 6, "first", 5, "Comment list with pagination"),
            ComplexityRule("comment", 2, description="Single comment query"),
            ComplexityRule("profile", 4, description="User profile"),
            ComplexityRule("settings", 3, description="User settings"),
        ]
        self.complexity_rules.extend(default_rules)
    
    def add_rule(self, rule: ComplexityRule):
        """Add a complexity rule."""
        self.complexity_rules.append(rule)
    
    def analyze(self, query: str, variables: Optional[Dict] = None) -> QueryComplexity:
        """Analyze query complexity."""
        print(f"Analyzing query complexity...")
        
        # Parse query to extract fields
        fields = self._extract_fields(query)
        
        # Calculate field costs
        field_costs = {}
        total_cost = 0
        
        for field_name in fields:
            cost = self._calculate_field_cost(field_name, variables or {})
            field_costs[field_name] = cost
            total_cost += cost
        
        # Determine complexity level
        level = self._determine_complexity_level(total_cost)
        
        # Validate complexity
        is_valid = total_cost <= self.max_complexity
        message = None if is_valid else f"Query too complex: {total_cost}/{self.max_complexity}"
        
        return QueryComplexity(
            total_cost=total_cost,
            max_cost=self.max_complexity,
            level=level,
            field_costs=field_costs,
            is_valid=is_valid,
            message=message
        )
    
    def _extract_fields(self, query: str) -> List[str]:
        """Extract field names from query."""
        # Simple field extraction (in real implementation, use AST)
        fields = []
        
        # Remove query/mutation/subscription keywords
        query = query.replace("query", "").replace("mutation", "").replace("subscription", "")
        
        # Extract field names (simplified)
        import re
        field_pattern = r'(\w+)\s*(?:\(|{)'
        matches = re.findall(field_pattern, query)
        
        # Filter out common keywords
        keywords = {'query', 'mutation', 'subscription', 'fragment', 'on', 'type', 'input'}
        fields = [f for f in matches if f.lower() not in keywords]
        
        return fields
    
    def _calculate_field_cost(self, field_name: str, variables: Dict) -> int:
        """Calculate cost for a field."""
        # Find matching rule
        for rule in self.complexity_rules:
            if rule.field_name == field_name:
                base_cost = rule.base_cost
                
                # Apply multiplier if applicable
                if rule.multiplier_field and rule.multiplier_field in variables:
                    multiplier = variables[rule.multiplier_field]
                    if isinstance(multiplier, (int, float)):
                        base_cost *= int(multiplier) * rule.multiplier_factor
                
                return base_cost
        
        # Default cost for unknown fields
        return 1
    
    def _determine_complexity_level(self, cost: int) -> QueryComplexityLevel:
        """Determine complexity level."""
        if cost <= 100:
            return QueryComplexityLevel.LOW
        elif cost <= 500:
            return QueryComplexityLevel.MEDIUM
        elif cost <= 1000:
            return QueryComplexityLevel.HIGH
        else:
            return QueryComplexityLevel.CRITICAL


# Query Depth Limiter
class QueryDepthLimiter:
    """Limit query depth."""
    
    def __init__(self, max_depth: int = 10):
        self.max_depth = max_depth
    
    def validate_depth(self, query: str) -> Tuple[bool, int, Optional[str]]:
        """Validate query depth."""
        depth = self._calculate_depth(query)
        is_valid = depth <= self.max_depth
        message = None if is_valid else f"Query too deep: {depth}/{self.max_depth}"
        
        return is_valid, depth, message
    
    def _calculate_depth(self, query: str) -> int:
        """Calculate query depth."""
        max_depth = 0
        current_depth = 0
        
        # Simple depth calculation
        for char in query:
            if char == '{':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == '}':
                current_depth -= 1
        
        return max_depth


# Cache Manager
class CacheManager:
    """Manage caching for GraphQL queries."""
    
    def __init__(self, strategy: CacheStrategy = CacheStrategy.IN_MEMORY, default_ttl: int = 300):
        self.strategy = strategy
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.metrics = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        entry = self.cache.get(key)
        
        if entry is None:
            self.metrics['misses'] += 1
            return None
        
        if entry.is_expired():
            del self.cache[key]
            self.metrics['evictions'] += 1
            self.metrics['misses'] += 1
            return None
        
        # Update access stats
        entry.access_count += 1
        entry.last_accessed = datetime.now()
        self.metrics['hits'] += 1
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache."""
        entry = CacheEntry(
            key=key,
            value=value,
            ttl=ttl or self.default_ttl
        )
        
        self.cache[key] = entry
        self.metrics['size'] = len(self.cache)
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self.cache:
            del self.cache[key]
            self.metrics['size'] = len(self.cache)
            return True
        return False
    
    def clear(self):
        """Clear all cache."""
        self.cache.clear()
        self.metrics['size'] = 0
    
    def get_hit_rate(self) -> float:
        """Get cache hit rate."""
        total = self.metrics['hits'] + self.metrics['misses']
        if total == 0:
            return 0.0
        return self.metrics['hits'] / total
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get cache metrics."""
        return {
            **self.metrics,
            'hitRate': self.get_hit_rate(),
            'strategy': self.strategy.name
        }


# Persisted Query Manager
class PersistedQueryManager:
    """Manage persisted queries."""
    
    def __init__(self):
        self.queries: Dict[str, PersistedQuery] = {}
        self.enabled: bool = True
    
    def register_query(self, query: str, name: Optional[str] = None) -> str:
        """Register a persisted query."""
        query_hash = self._generate_hash(query)
        
        persisted_query = PersistedQuery(
            hash=query_hash,
            query=query,
            name=name
        )
        
        self.queries[query_hash] = persisted_query
        print(f"Registered persisted query: {query_hash}")
        
        return query_hash
    
    def get_query(self, hash_value: str) -> Optional[str]:
        """Get query by hash."""
        persisted_query = self.queries.get(hash_value)
        
        if persisted_query:
            persisted_query.access_count += 1
            persisted_query.last_accessed = datetime.now()
            return persisted_query.query
        
        return None
    
    def has_query(self, hash_value: str) -> bool:
        """Check if query exists."""
        return hash_value in self.queries
    
    def remove_query(self, hash_value: str) -> bool:
        """Remove a persisted query."""
        if hash_value in self.queries:
            del self.queries[hash_value]
            return True
        return False
    
    def get_all_queries(self) -> List[PersistedQuery]:
        """Get all persisted queries."""
        return list(self.queries.values())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get query statistics."""
        queries = list(self.queries.values())
        
        if not queries:
            return {'total': 0, 'totalAccesses': 0}
        
        total_accesses = sum(q.access_count for q in queries)
        
        return {
            'total': len(queries),
            'totalAccesses': total_accesses,
            'averageAccesses': total_accesses / len(queries) if queries else 0
        }
    
    def _generate_hash(self, query: str) -> str:
        """Generate hash for query."""
        return hashlib.sha256(query.encode()).hexdigest()[:16]


# Query Batch Processor
class QueryBatchProcessor:
    """Batch multiple queries for efficiency."""
    
    def __init__(self, batch_size: int = 10, batch_interval: float = 0.01):
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        self.pending_queries: List[Dict[str, Any]] = []
        self.batch_stats = {
            'total_batches': 0,
            'total_queries': 0,
            'average_batch_size': 0.0
        }
    
    async def add_query(self, query: str, variables: Optional[Dict] = None) -> asyncio.Future:
        """Add query to batch."""
        future = asyncio.get_event_loop().create_future()
        
        self.pending_queries.append({
            'query': query,
            'variables': variables or {},
            'future': future
        })
        
        # Trigger batch if size reached
        if len(self.pending_queries) >= self.batch_size:
            await self._execute_batch()
        
        return future
    
    async def _execute_batch(self):
        """Execute batched queries."""
        if not self.pending_queries:
            return
        
        queries = self.pending_queries.copy()
        self.pending_queries.clear()
        
        print(f"Executing batch of {len(queries)} queries")
        
        # Execute queries in parallel
        results = await asyncio.gather(
            *[self._execute_single_query(q) for q in queries],
            return_exceptions=True
        )
        
        # Resolve futures
        for query_info, result in zip(queries, results):
            future = query_info['future']
            if not future.done():
                if isinstance(result, Exception):
                    future.set_exception(result)
                else:
                    future.set_result(result)
        
        # Update stats
        self.batch_stats['total_batches'] += 1
        self.batch_stats['total_queries'] += len(queries)
        self.batch_stats['average_batch_size'] = (
            self.batch_stats['total_queries'] / self.batch_stats['total_batches']
        )
    
    async def _execute_single_query(self, query_info: Dict[str, Any]) -> Any:
        """Execute a single query."""
        # Mock execution
        await asyncio.sleep(0.001)  # Simulate network latency
        
        return {
            'data': {'mock': 'result'},
            'extensions': {
                'batched': True,
                'query': query_info['query'][:50]
            }
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get batch statistics."""
        return self.batch_stats.copy()


# Performance Monitor
class PerformanceMonitor:
    """Monitor GraphQL performance."""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.query_times: List[float] = []
        self.complexity_scores: List[int] = []
        self.error_count: int = 0
        self.total_count: int = 0
    
    def record_query(self, duration: float, complexity: int, success: bool = True):
        """Record query execution."""
        self.query_times.append(duration)
        self.complexity_scores.append(complexity)
        self.total_count += 1
        
        if not success:
            self.error_count += 1
        
        # Update metrics
        self._update_metrics()
    
    def _update_metrics(self):
        """Update performance metrics."""
        if not self.query_times:
            return
        
        # Calculate averages
        self.metrics.average_query_time = sum(self.query_times) / len(self.query_times)
        
        # Calculate percentiles
        sorted_times = sorted(self.query_times)
        p95_index = int(len(sorted_times) * 0.95)
        p99_index = int(len(sorted_times) * 0.99)
        
        self.metrics.p95_query_time = sorted_times[p95_index] if p95_index < len(sorted_times) else 0
        self.metrics.p99_query_time = sorted_times[p99_index] if p99_index < len(sorted_times) else 0
        
        # Calculate complexity score
        if self.complexity_scores:
            self.metrics.complexity_score = sum(self.complexity_scores) / len(self.complexity_scores)
        
        # Calculate error rate
        self.metrics.error_rate = self.error_count / self.total_count if self.total_count > 0 else 0
        
        # Update total queries
        self.metrics.total_queries = self.total_count
        
        self.metrics.last_updated = datetime.now()
    
    def get_metrics(self) -> PerformanceMetrics:
        """Get current metrics."""
        return self.metrics
    
    def get_slow_queries(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """Get slow queries above threshold."""
        # In real implementation, track query details
        return []


# Query Optimizer
class QueryOptimizer:
    """Optimize GraphQL queries."""
    
    def __init__(self):
        self.optimization_rules: List[Callable] = []
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default optimization rules."""
        self.optimization_rules = [
            self._optimize_field_selection,
            self._optimize_list_arguments,
            self._optimize_redundant_fragments,
        ]
    
    def optimize(self, query: str, variables: Optional[Dict] = None) -> str:
        """Optimize a query."""
        print(f"Optimizing query...")
        
        optimized = query
        
        for rule in self.optimization_rules:
            optimized = rule(optimized, variables or {})
        
        return optimized
    
    def _optimize_field_selection(self, query: str, variables: Dict) -> str:
        """Optimize field selection."""
        # Remove redundant fields (simplified)
        # In real implementation, use AST analysis
        return query
    
    def _optimize_list_arguments(self, query: str, variables: Dict) -> str:
        """Optimize list arguments."""
        # Add default pagination limits
        if 'first:' not in query and 'last:' not in query:
            # Add default limit
            query = query.replace('{', '{ first: 10 ', 1)
        return query
    
    def _optimize_redundant_fragments(self, query: str, variables: Dict) -> str:
        """Remove redundant fragments."""
        # Simple fragment removal (simplified)
        return query
    
    def analyze_optimization_potential(self, query: str) -> Dict[str, Any]:
        """Analyze optimization potential."""
        potential = {
            'field_selection': 0,
            'list_optimization': 0,
            'fragment_optimization': 0,
            'total_potential': 0
        }
        
        # Analyze field selection
        field_count = query.count('{') - query.count('}')
        potential['field_selection'] = max(0, field_count - 5) * 10
        
        # Analyze list optimization
        if 'first:' not in query and 'last:' not in query:
            potential['list_optimization'] = 20
        
        # Analyze fragments
        fragment_count = query.lower().count('fragment')
        potential['fragment_optimization'] = fragment_count * 5
        
        potential['total_potential'] = sum(potential.values())
        
        return potential


# Cache Strategy Manager
class CacheStrategyManager:
    """Manage caching strategies."""
    
    def __init__(self):
        self.strategies: Dict[str, CacheStrategy] = {}
        self.cache_configs: Dict[str, Dict[str, Any]] = {}
    
    def register_strategy(self, name: str, strategy: CacheStrategy, config: Optional[Dict] = None):
        """Register a caching strategy."""
        self.strategies[name] = strategy
        self.cache_configs[name] = config or {}
        print(f"Registered strategy: {name}")
    
    def get_strategy(self, name: str) -> Optional[CacheStrategy]:
        """Get a caching strategy."""
        return self.strategies.get(name)
    
    def get_config(self, name: str) -> Dict[str, Any]:
        """Get cache configuration."""
        return self.cache_configs.get(name, {})
    
    def apply_strategy(self, query: str, strategy_name: str) -> Dict[str, Any]:
        """Apply caching strategy to query."""
        strategy = self.get_strategy(strategy_name)
        if not strategy:
            return {'applied': False, 'reason': 'Strategy not found'}
        
        config = self.get_config(strategy_name)
        
        return {
            'applied': True,
            'strategy': strategy.name,
            'config': config,
            'query': query
        }


# Performance Optimizer
class PerformanceOptimizer:
    """Main performance optimization engine."""
    
    def __init__(self):
        self.complexity_analyzer = QueryComplexityAnalyzer()
        self.depth_limiter = QueryDepthLimiter()
        self.cache_manager = CacheManager()
        self.persisted_query_manager = PersistedQueryManager()
        self.batch_processor = QueryBatchProcessor()
        self.performance_monitor = PerformanceMonitor()
        self.query_optimizer = QueryOptimizer()
    
    async def optimize_query(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Optimize a GraphQL query."""
        print(f"Optimizing query: {query[:50]}...")
        
        start_time = time.time()
        
        # Analyze complexity
        complexity = self.complexity_analyzer.analyze(query, variables)
        
        # Validate depth
        is_valid_depth, depth, depth_message = self.depth_limiter.validate_depth(query)
        
        # Check persisted queries
        query_hash = hashlib.sha256(query.encode()).hexdigest()[:16]
        is_persisted = self.persisted_query_manager.has_query(query_hash)
        
        # Check cache
        cache_key = f"{query_hash}:{hashlib.md5(json.dumps(variables or {}).encode()).hexdigest()}"
        cached_result = self.cache_manager.get(cache_key)
        
        # Optimize query
        optimized_query = self.query_optimizer.optimize(query, variables)
        
        # Calculate optimization potential
        optimization_potential = self.query_optimizer.analyze_optimization_potential(query)
        
        # Record performance
        duration = time.time() - start_time
        self.performance_monitor.record_query(duration, complexity.total_cost, complexity.is_valid)
        
        return {
            'original_query': query,
            'optimized_query': optimized_query,
            'complexity': complexity.to_dict(),
            'depth': {
                'valid': is_valid_depth,
                'depth': depth,
                'message': depth_message
            },
            'persisted': {
                'isPersisted': is_persisted,
                'hash': query_hash
            },
            'cache': {
                'hit': cached_result is not None,
                'key': cache_key
            },
            'optimization': optimization_potential,
            'duration': duration
        }
    
    async def execute_optimized_query(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute an optimized query."""
        # Optimize query
        optimization_result = await self.optimize_query(query, variables)
        
        if not optimization_result['complexity']['isValid']:
            return {
                'error': 'Query too complex',
                'details': optimization_result['complexity']
            }
        
        # Execute query (mock)
        start_time = time.time()
        result = {
            'data': {'mock': 'result'},
            'extensions': {
                'complexity': optimization_result['complexity'],
                'cached': optimization_result['cache']['hit'],
                'persisted': optimization_result['persisted']['isPersisted']
            }
        }
        
        duration = time.time() - start_time
        
        # Cache result
        if not optimization_result['cache']['hit']:
            self.cache_manager.set(
                optimization_result['cache']['key'],
                result,
                ttl=300
            )
        
        return result
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report."""
        return {
            'metrics': self.performance_monitor.get_metrics().to_dict(),
            'cache': self.cache_manager.get_metrics(),
            'persistedQueries': self.persisted_query_manager.get_statistics(),
            'batchProcessor': self.batch_processor.get_stats()
        }


# Main demo function
async def main():
    """Demonstrate GraphQL performance optimization patterns."""
    print("=== GraphQL Performance Demo ===\n")
    
    # Demo 1: Query Complexity Analysis
    print("1. Query Complexity Analysis:")
    
    analyzer = QueryComplexityAnalyzer(max_complexity=1000)
    
    test_queries = [
        "query { user(id: \"1\") { name email } }",
        "query { users(first: 10) { id name posts { id title } } }",
        "query { users(first: 100) { id name posts(first: 50) { id title comments { id content } } } }",
    ]
    
    for query in test_queries:
        complexity = analyzer.analyze(query)
        print(f"   Query: {query[:50]}...")
        print(f"   Complexity: {complexity.total_cost} ({complexity.level.name})")
        print(f"   Valid: {complexity.is_valid}")
        print()
    
    # Demo 2: Query Depth Limiting
    print("2. Query Depth Limiting:")
    
    depth_limiter = QueryDepthLimiter(max_depth=5)
    
    depth_queries = [
        "query { user { name } }",
        "query { user { posts { comments { author { name } } } } }",
        "query { user { posts { comments { author { posts { title } } } } } }",
    ]
    
    for query in depth_queries:
        is_valid, depth, message = depth_limiter.validate_depth(query)
        print(f"   Query: {query[:50]}...")
        print(f"   Depth: {depth}, Valid: {is_valid}")
        if message:
            print(f"   Message: {message}")
        print()
    
    # Demo 3: Cache Manager
    print("3. Cache Manager:")
    
    cache = CacheManager(strategy=CacheStrategy.IN_MEMORY, default_ttl=60)
    
    # Cache some data
    cache.set("user:1", {"id": "1", "name": "Alice"})
    cache.set("user:2", {"id": "2", "name": "Bob"})
    
    # Get from cache
    user1 = cache.get("user:1")
    user2 = cache.get("user:2")
    user3 = cache.get("user:3")  # Miss
    
    print(f"   Cache hit for user:1: {user1 is not None}")
    print(f"   Cache hit for user:2: {user2 is not None}")
    print(f"   Cache hit for user:3: {user3 is not None}")
    print(f"   Cache metrics: {cache.get_metrics()}")
    
    # Demo 4: Persisted Queries
    print("\n4. Persisted Queries:")
    
    persisted_manager = PersistedQueryManager()
    
    # Register queries
    query1 = "query { user(id: \"1\") { name email } }"
    query2 = "query { posts(first: 10) { id title } }"
    
    hash1 = persisted_manager.register_query(query1, "GetUser")
    hash2 = persisted_manager.register_query(query2, "GetPosts")
    
    # Get queries
    retrieved_query1 = persisted_manager.get_query(hash1)
    retrieved_query2 = persisted_manager.get_query(hash2)
    
    print(f"   Registered {len(persisted_manager.get_all_queries())} queries")
    print(f"   Query 1 hash: {hash1}")
    print(f"   Query 2 hash: {hash2}")
    print(f"   Statistics: {persisted_manager.get_statistics()}")
    
    # Demo 5: Query Batching
    print("\n5. Query Batching:")
    
    batch_processor = QueryBatchProcessor(batch_size=3, batch_interval=0.01)
    
    # Add queries to batch
    queries = [
        "query { user(id: \"1\") { name } }",
        "query { user(id: \"2\") { name } }",
        "query { user(id: \"3\") { name } }",
    ]
    
    futures = []
    for query in queries:
        future = await batch_processor.add_query(query)
        futures.append(future)
    
    # Wait for batch to execute
    results = await asyncio.gather(*futures)
    
    print(f"   Batch stats: {batch_processor.get_stats()}")
    
    # Demo 6: Performance Monitor
    print("\n6. Performance Monitor:")
    
    monitor = PerformanceMonitor()
    
    # Record some queries
    monitor.record_query(0.1, 50, success=True)
    monitor.record_query(0.2, 100, success=True)
    monitor.record_query(0.05, 25, success=True)
    monitor.record_query(1.5, 500, success=False)  # Slow and failed
    
    metrics = monitor.get_metrics()
    print(f"   Total queries: {metrics.total_queries}")
    print(f"   Average query time: {metrics.average_query_time:.3f}s")
    print(f"   Error rate: {metrics.error_rate:.2%}")
    print(f"   Complexity score: {metrics.complexity_score:.1f}")
    
    # Demo 7: Query Optimizer
    print("\n7. Query Optimizer:")
    
    optimizer = QueryOptimizer()
    
    test_query = "query { users { id name email posts { id title } } }"
    optimized = optimizer.optimize(test_query)
    
    potential = optimizer.analyze_optimization_potential(test_query)
    print(f"   Original: {test_query}")
    print(f"   Optimized: {optimized}")
    print(f"   Optimization potential: {potential}")
    
    # Demo 8: Cache Strategy Manager
    print("\n8. Cache Strategy Manager:")
    
    strategy_manager = CacheStrategyManager()
    strategy_manager.register_strategy("aggressive", CacheStrategy.REDIS, {'ttl': 600})
    strategy_manager.register_strategy("conservative", CacheStrategy.IN_MEMORY, {'ttl': 60})
    
    aggressive_config = strategy_manager.get_config("aggressive")
    conservative_config = strategy_manager.get_config("conservative")
    
    print(f"   Aggressive strategy: {aggressive_config}")
    print(f"   Conservative strategy: {conservative_config}")
    
    # Demo 9: Performance Optimizer
    print("\n9. Performance Optimizer:")
    
    perf_optimizer = PerformanceOptimizer()
    
    # Register persisted query
    test_query = "query { user(id: \"1\") { name email posts { id title } } }"
    perf_optimizer.persisted_query_manager.register_query(test_query)
    
    # Optimize and execute query
    result = await perf_optimizer.execute_optimized_query(
        test_query,
        {"id": "1"}
    )
    
    print(f"   Query executed successfully")
    print(f"   Extensions: {result.get('extensions', {})}")
    
    # Get performance report
    report = perf_optimizer.get_performance_report()
    print(f"   Performance report:")
    print(f"     Metrics: {report['metrics']['totalQueries']} queries")
    print(f"     Cache hit rate: {report['cache']['hitRate']:.2%}")
    
    # Demo 10: Comprehensive Analysis
    print("\n10. Comprehensive Analysis:")
    
    # Analyze multiple queries
    analysis_queries = [
        "query { user(id: \"1\") { name } }",
        "query { posts(first: 5) { id title } }",
        "query { users(first: 20) { id name posts { id } } }",
    ]
    
    for query in analysis_queries:
        optimization = await perf_optimizer.optimize_query(query)
        print(f"\n   Query: {query[:50]}...")
        print(f"   Complexity: {optimization['complexity']['totalCost']}")
        print(f"   Valid: {optimization['complexity']['isValid']}")
        print(f"   Persisted: {optimization['persisted']['isPersisted']}")
        print(f"   Cache hit: {optimization['cache']['hit']}")
        print(f"   Duration: {optimization['duration']:.4f}s")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(main())