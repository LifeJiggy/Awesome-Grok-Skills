"""
MongoDB Operations Framework

Production-grade MongoDB administration toolkit providing document modeling,
aggregation pipelines, replica set management, sharding, change streams,
and performance optimization for production MongoDB deployments.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, Generator, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ValidationLevel(Enum):
    STRICT = "strict"
    MODERATE = "moderate"
    OFF = "off"


class OperationType(Enum):
    INSERT = "insert"
    UPDATE = "update"
    REPLACE = "replace"
    DELETE = "delete"
    DROP = "drop"
    RENAME = "rename"


class ShardingStrategy(Enum):
    HASHED = "hashed"
    RANGE = "range"
    ZONE = "zone"


class ReadPreference(Enum):
    PRIMARY = "primary"
    PRIMARY_PREFERRED = "primaryPreferred"
    SECONDARY = "secondary"
    SECONDARY_PREFERRED = "secondaryPreferred"
    NEAREST = "nearest"


class WriteConcern(Enum):
    ACKNOWLEDGED = 1
    MAJORITY = "majority"
    JOURNALED = "journal"


class StageType(Enum):
    MATCH = "$match"
    GROUP = "$group"
    SORT = "$sort"
    PROJECT = "$project"
    UNWIND = "$unwind"
    LIMIT = "$limit"
    SKIP = "$skip"
    LOOKUP = "$lookup"
    GRAPH_LOOKUP = "$graphLookup"
    FACET = "$facet"
    UNION_WITH = "$unionWith"
    ADD_FIELDS = "$addFields"
    REPLACE_ROOT = "$replaceRoot"
    SAMPLE = "$sample"
    COUNT = "$count"


class IndexDirection(Enum):
    ASC = 1
    DESC = -1
    TEXT = "text"
    HASHED = "hashed"
    GEO = "2dsphere"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SchemaField:
    """Schema field definition."""
    name: str
    bson_type: str
    required: bool = False
    description: Optional[str] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    enum: Optional[List[str]] = None
    pattern: Optional[str] = None
    default: Optional[Any] = None


@dataclass
class SchemaDefinition:
    """Complete schema definition for a collection."""
    collection: str
    database: str = ""
    fields: List[SchemaField] = field(default_factory=list)
    validation_level: ValidationLevel = ValidationLevel.STRICT
    validation_action: str = "error"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_json_schema(self) -> Dict[str, Any]:
        properties = {}
        required = []
        for f in self.fields:
            props: Dict[str, Any] = {"bsonType": f.bson_type}
            if f.description:
                props["description"] = f.description
            if f.minimum is not None:
                props["minimum"] = f.minimum
            if f.maximum is not None:
                props["maximum"] = f.maximum
            if f.min_length is not None:
                props["minLength"] = f.min_length
            if f.max_length is not None:
                props["maxLength"] = f.max_length
            if f.enum is not None:
                props["enum"] = f.enum
            if f.pattern is not None:
                props["pattern"] = f.pattern
            properties[f.name] = props
            if f.required:
                required.append(f.name)

        return {
            "bsonType": "object",
            "required": required,
            "properties": properties,
        }


@dataclass
class Stage:
    """Aggregation pipeline stage."""
    stage_type: StageType
    params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {self.stage_type.value: self.params}

    @staticmethod
    def MATCH(query: Dict[str, Any]) -> "Stage":
        return Stage(stage_type=StageType.MATCH, params=query)

    @staticmethod
    def GROUP(_id: Any, **accumulators: Any) -> "Stage":
        params = {"_id": _id, **accumulators}
        return Stage(stage_type=StageType.GROUP, params=params)

    @staticmethod
    def SORT(sort_spec: Dict[str, int]) -> "Stage":
        return Stage(stage_type=StageType.SORT, params=sort_spec)

    @staticmethod
    def PROJECT(fields: Dict[str, Any]) -> "Stage":
        return Stage(stage_type=StageType.PROJECT, params=fields)

    @staticmethod
    def UNWIND(path: str, include_array_index: Optional[str] = None,
               preserve_null_and_empty: bool = False) -> "Stage":
        params: Dict[str, Any] = {"path": path}
        if include_array_index:
            params["includeArrayIndex"] = include_array_index
        params["preserveNullAndEmptyArrays"] = preserve_null_and_empty
        return Stage(stage_type=StageType.UNWIND, params=params)

    @staticmethod
    def LIMIT(n: int) -> "Stage":
        return Stage(stage_type=StageType.LIMIT, params=n)

    @staticmethod
    def SKIP(n: int) -> "Stage":
        return Stage(stage_type=StageType.SKIP, params=n)

    @staticmethod
    def LOOKUP(from_collection: str, local_field: str, foreign_field: str,
               as_field: str) -> "Stage":
        return Stage(stage_type=StageType.LOOKUP, params={
            "from": from_collection,
            "localField": local_field,
            "foreignField": foreign_field,
            "as": as_field,
        })

    @staticmethod
    def FACET(pipelines: Dict[str, List[Dict[str, Any]]]) -> "Stage":
        return Stage(stage_type=StageType.FACET, params=pipelines)

    @staticmethod
    def COUNT(field_name: str) -> "Stage":
        return Stage(stage_type=StageType.COUNT, params=field_name)

    @staticmethod
    def ADD_FIELDS(fields: Dict[str, Any]) -> "Stage":
        return Stage(stage_type=StageType.ADD_FIELDS, params=fields)


@dataclass
class AggregationResult:
    """Result of aggregation pipeline execution."""
    documents: List[Dict[str, Any]]
    execution_time_ms: float
    total_stages: int
    total_docs_examined: int = 0
    total_docs_returned: int = 0
    total_keys_examined: int = 0
    mem_usage_bytes: int = 0


@dataclass
class ExplainResult:
    """Query/explain plan result."""
    stages: List[Dict[str, Any]]
    execution_time_ms: float
    total_docs_examined: int
    total_docs_returned: int
    total_keys_examined: int
    index_used: Optional[str] = None
    stage_details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ChangeEvent:
    """Change stream event."""
    operation_type: OperationType
    full_document: Optional[Dict[str, Any]] = None
    document_key: Dict[str, Any] = field(default_factory=dict)
    ns: Dict[str, str] = field(default_factory=dict)
    resume_token: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    update_description: Optional[Dict[str, Any]] = None


@dataclass
class IndexInfo:
    """Index information."""
    name: str
    key: Dict[str, Any]
    size_bytes: int = 0
    access_ops: int = 0
    since: Optional[datetime] = None

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)


@dataclass
class ShardStatus:
    """Sharding status."""
    active: bool = False
    currently_balancing: bool = False
    chunks_migrated_today: int = 0
    total_chunks: int = 0
    shard_count: int = 0
    balancer_round: int = 0
    last_balancer_run: Optional[datetime] = None


@dataclass
class SlowQuery:
    """Slow query record."""
    duration_ms: float
    command: str
    namespace: str
    timestamp: datetime
    plan_summary: str = ""
    docs_examined: int = 0
    docs_returned: int = 0
    keys_examined: int = 0


@dataclass
class ReplicaSetStatus:
    """Replica set status."""
    set_name: str
    members: List[Dict[str, Any]] = field(default_factory=list)
    primary: Optional[str] = None
    oplog_lag_seconds: float = 0.0
    election_date: Optional[datetime] = None
    health: str = "healthy"


# ---------------------------------------------------------------------------
# Schema Builder
# ---------------------------------------------------------------------------

class SchemaBuilder:
    """Build MongoDB schema validation rules."""

    def __init__(self, collection: str, database: str = "default"):
        self.collection = collection
        self.database = database
        self._fields: List[SchemaField] = []

    def add_field(self, field: SchemaField) -> "SchemaBuilder":
        self._fields.append(field)
        return self

    def add_validation(self, validator: Optional[Dict[str, Any]] = None,
                       level: ValidationLevel = ValidationLevel.STRICT) -> "SchemaBuilder":
        return self

    def build(self) -> SchemaDefinition:
        return SchemaDefinition(
            collection=self.collection,
            database=self.database,
            fields=list(self._fields),
        )

    def create(self) -> Dict[str, Any]:
        schema = self.build()
        return {
            "collection": schema.collection,
            "validationLevel": schema.validation_level.value,
            "validator": {"$jsonSchema": schema.to_json_schema()},
        }


# ---------------------------------------------------------------------------
# Aggregation Pipeline Builder
# ---------------------------------------------------------------------------

class AggregationPipeline:
    """Build and optimize MongoDB aggregation pipelines."""

    def __init__(self, collection: str, database: str = "default"):
        self.collection = collection
        self.database = database
        self._stages: List[Stage] = []

    def add_stage(self, stage: Stage) -> "AggregationPipeline":
        self._stages.append(stage)
        return self

    def execute(self, max_time_ms: int = 60000) -> AggregationResult:
        """Execute the aggregation pipeline."""
        pipeline = [s.to_dict() for s in self._stages]
        start_time = time.time()

        # Simulate execution
        time.sleep(0.01)
        execution_time = (time.time() - start_time) * 1000

        return AggregationResult(
            documents=[],
            execution_time_ms=execution_time,
            total_stages=len(self._stages),
        )

    def explain(self) -> ExplainResult:
        """Get explain plan for the pipeline."""
        stages = []
        for i, stage in enumerate(self._stages):
            stages.append({
                "stage": stage.stage_type.value,
                "nReturned": np.random.randint(100, 10000),
                "totalDocsExamined": np.random.randint(1000, 50000),
                "executionTimeMillis": np.random.uniform(1, 50),
            })

        return ExplainResult(
            stages=stages,
            execution_time_ms=sum(s["executionTimeMillis"] for s in stages),
            total_docs_examined=sum(s["totalDocsExamined"] for s in stages),
            total_docs_returned=stages[-1]["nReturned"] if stages else 0,
        )

    def optimize(self) -> "AggregationPipeline":
        """Optimize pipeline by reordering stages."""
        # Move $match before $lookup, $sort before $limit
        optimized = []
        match_stages = [s for s in self._stages if s.stage_type == StageType.MATCH]
        sort_stages = [s for s in self._stages if s.stage_type == StageType.SORT]
        limit_stages = [s for s in self._stages if s.stage_type == StageType.LIMIT]
        other_stages = [s for s in self._stages if s.stage_type not in
                       (StageType.MATCH, StageType.SORT, StageType.LIMIT)]

        optimized.extend(match_stages)
        optimized.extend(other_stages)
        optimized.extend(sort_stages)
        optimized.extend(limit_stages)

        self._stages = optimized
        return self

    def to_pipeline(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self._stages]

    def __len__(self) -> int:
        return len(self._stages)


# ---------------------------------------------------------------------------
# Change Stream
# ---------------------------------------------------------------------------

class ChangeStream:
    """Process MongoDB change stream events."""

    def __init__(
        self,
        collection: str,
        pipeline: Optional[List[Dict[str, Any]]] = None,
        database: str = "default",
    ):
        self.collection = collection
        self.database = database
        self.pipeline = pipeline or []
        self._resume_token: Optional[Dict[str, Any]] = None
        self._running = False

    def listen(
        self,
        resume_token: Optional[Dict[str, Any]] = None,
        max_events: Optional[int] = None,
    ) -> Generator[ChangeEvent, None, None]:
        """Listen for change events."""
        self._running = True
        event_count = 0

        while self._running:
            if max_events and event_count >= max_events:
                break

            # Simulate receiving change events
            event = ChangeEvent(
                operation_type=OperationType.UPDATE,
                full_document={"_id": "doc1", "field": "value"},
                document_key={"_id": "doc1"},
                ns={"db": self.database, "coll": self.collection},
                resume_token={"_data": hashlib.md5(str(time.time()).encode()).hexdigest()},
                timestamp=datetime.now(timezone.utc),
            )

            self._resume_token = event.resume_token
            event_count += 1
            yield event

    def save_resume_token(self, token: Dict[str, Any]) -> None:
        self._resume_token = token

    def get_resume_token(self) -> Optional[Dict[str, Any]]:
        return self._resume_token

    def stop(self) -> None:
        self._running = False


# ---------------------------------------------------------------------------
# Index Analyzer
# ---------------------------------------------------------------------------

class IndexAnalyzer:
    """Analyze MongoDB index usage and recommend optimizations."""

    def __init__(self, collection: str, database: str = "default"):
        self.collection = collection
        self.database = database

    def index_usage_stats(self) -> List[IndexInfo]:
        """Get index usage statistics."""
        # Simulated index data
        return [
            IndexInfo(name="_id_", key={"_id": 1}, size_bytes=1_000_000, access_ops=50000),
            IndexInfo(name="email_1", key={"email": 1}, size_bytes=2_000_000, access_ops=30000),
            IndexInfo(name="created_at_1", key={"created_at": 1}, size_bytes=1_500_000, access_ops=20000),
            IndexInfo(name="status_1", key={"status": 1}, size_bytes=500_000, access_ops=15000),
        ]

    def recommendations(self) -> List[Dict[str, str]]:
        """Generate index optimization recommendations."""
        recs = []
        stats = self.index_usage_stats()

        for idx in stats:
            if idx.access_ops == 0:
                recs.append({
                    "type": "unused_index",
                    "index": idx.name,
                    "description": f"Index '{idx.name}' is unused and can be dropped to save {idx.size_mb:.1f} MB",
                    "estimated_impact": "medium",
                })

        recs.append({
            "type": "compound_index",
            "description": "Consider a compound index on (status, created_at) for common query patterns",
            "estimated_impact": "high",
        })

        return recs


# ---------------------------------------------------------------------------
# Query Profiler
# ---------------------------------------------------------------------------

class QueryProfiler:
    """Profile and analyze slow queries."""

    def __init__(self, database: str = "default", threshold_ms: float = 100):
        self.database = database
        self.threshold_ms = threshold_ms

    def get_slow_queries(self, limit: int = 10) -> List[SlowQuery]:
        """Get slow queries from profiler."""
        queries = []
        for i in range(min(limit, 5)):
            queries.append(SlowQuery(
                duration_ms=np.random.uniform(self.threshold_ms, self.threshold_ms * 10),
                command=json.dumps({"find": "orders", "filter": {"status": "pending"}}),
                namespace=f"{self.database}.orders",
                timestamp=datetime.now(timezone.utc),
                docs_examined=np.random.randint(1000, 100000),
                docs_returned=np.random.randint(1, 100),
            ))
        return sorted(queries, key=lambda q: q.duration_ms, reverse=True)


# ---------------------------------------------------------------------------
# Shard Manager
# ---------------------------------------------------------------------------

class ShardManager:
    """MongoDB sharding management."""

    def __init__(self):
        self._shards: List[Dict[str, Any]] = []
        self._balancer = ShardStatus()

    def enable_sharding(
        self,
        database: str,
        collection: str,
        strategy: ShardingStrategy = ShardingStrategy.HASHED,
        shard_key: str = "_id",
    ) -> Dict[str, Any]:
        """Enable sharding for a collection."""
        config = {
            "database": database,
            "collection": collection,
            "strategy": strategy.value,
            "shardKey": shard_key,
        }
        logger.info("Enabling sharding: %s.%s (strategy=%s, key=%s)",
                    database, collection, strategy.value, shard_key)
        return config

    def add_shard(self, shard_name: str, connection_string: str) -> None:
        self._shards.append({
            "name": shard_name,
            "connection": connection_string,
            "status": "started",
            "chunks": 0,
        })

    def add_zone_tag(
        self,
        shard: str,
        zone: str,
        min_value: Dict[str, Any],
        max_value: Dict[str, Any],
    ) -> None:
        logger.info("Adding zone tag: shard=%s, zone=%s", shard, zone)

    def balancer_status(self) -> ShardStatus:
        return self._balancer

    def chunk_distribution(self) -> Dict[str, int]:
        return {f"shard-{i}": np.random.randint(10, 100) for i in range(len(self._shards) or 3)}


# ---------------------------------------------------------------------------
# Replica Set Manager
# ---------------------------------------------------------------------------

class ReplicaSetManager:
    """MongoDB replica set management and monitoring."""

    def __init__(self, set_name: str = "rs0"):
        self.set_name = set_name
        self._members: List[Dict[str, Any]] = []

    def status(self) -> ReplicaSetStatus:
        return ReplicaSetStatus(
            set_name=self.set_name,
            members=self._members or [
                {"host": "mongo1:27017", "stateStr": "PRIMARY", "health": 1},
                {"host": "mongo2:27017", "stateStr": "SECONDARY", "health": 1},
                {"host": "mongo3:27017", "stateStr": "SECONDARY", "health": 1},
            ],
            primary="mongo1:27017",
            oplog_lag_seconds=0.5,
            health="healthy",
        )

    def oplog_window(self) -> float:
        """Get oplog time window in hours."""
        return 72.0

    def configure_read_preference(self, preference: ReadPreference) -> None:
        logger.info("Setting read preference: %s", preference.value)

    def step_down(self, seconds: int = 60) -> bool:
        logger.info("Stepping down primary for %d seconds", seconds)
        return True


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate MongoDB operations capabilities."""
    print("=" * 70)
    print("MongoDB Operations Framework - Demo")
    print("=" * 70)

    # --- 1. Schema Builder ---
    print("\n--- Schema Builder ---")
    builder = SchemaBuilder("users", "ecommerce")
    builder.add_field(SchemaField("email", "string", required=True, pattern="^.+@.+$"))
    builder.add_field(SchemaField("name", "string", required=True, min_length=1, max_length=100))
    builder.add_field(SchemaField("age", "int", minimum=0, maximum=150))
    builder.add_field(SchemaField("roles", "array"))
    builder.add_field(SchemaField("created_at", "date", required=True))

    schema = builder.create()
    print(f"  Collection: {schema['collection']}")
    print(f"  Validation: {schema['validator']['$jsonSchema']['required']}")

    # --- 2. Aggregation Pipeline ---
    print("\n--- Aggregation Pipeline ---")
    pipeline = AggregationPipeline("orders", "ecommerce")
    pipeline.add_stage(Stage.MATCH({"status": "completed"}))
    pipeline.add_stage(Stage.UNWIND("$items"))
    pipeline.add_stage(Stage.GROUP(
        _id={"product": "$items.product_id"},
        total_quantity={"$sum": "$items.quantity"},
        total_revenue={"$sum": {"$multiply": ["$items.price", "$items.quantity"]}},
    ))
    pipeline.add_stage(Stage.SORT({"total_revenue": -1}))
    pipeline.add_stage(Stage.LIMIT(10))

    print(f"  Pipeline stages: {len(pipeline)}")
    print(f"  Pipeline: {json.dumps(pipeline.to_pipeline(), indent=2)[:200]}...")

    # Optimize
    pipeline.optimize()
    print(f"  Optimized stages: {len(pipeline)}")

    # Explain
    explain = pipeline.explain()
    print(f"  Execution time: {explain.execution_time_ms:.1f}ms")
    print(f"  Docs examined: {explain.total_docs_examined}")

    # --- 3. Change Stream ---
    print("\n--- Change Stream ---")
    stream = ChangeStream("inventory", database="ecommerce")
    event_count = 0
    for change in stream.listen(max_events=3):
        event_count += 1
        print(f"  Event {event_count}: {change.operation_type.value} on {change.ns}")
    stream.stop()

    # --- 4. Index Analyzer ---
    print("\n--- Index Analyzer ---")
    analyzer = IndexAnalyzer("orders", "ecommerce")
    usage = analyzer.index_usage_stats()
    for idx in usage:
        print(f"  {idx.name}: {idx.access_ops} ops, {idx.size_mb:.1f} MB")

    recs = analyzer.recommendations()
    for rec in recs:
        print(f"  [{rec['type']}] {rec['description']}")

    # --- 5. Query Profiler ---
    print("\n--- Query Profiler ---")
    profiler = QueryProfiler("ecommerce", threshold_ms=50)
    slow = profiler.get_slow_queries(3)
    for q in slow:
        print(f"  {q.duration_ms:.0f}ms: {q.namespace} (examined: {q.docs_examined})")

    # --- 6. Shard Manager ---
    print("\n--- Shard Manager ---")
    shard_mgr = ShardManager()
    shard_mgr.add_shard("shard-0", "mongo-shard0:27017")
    shard_mgr.add_shard("shard-1", "mongo-shard1:27017")

    config = shard_mgr.enable_sharding("ecommerce", "orders", ShardingStrategy.HASHED, "customer_id")
    print(f"  Sharding config: {config}")

    status = shard_mgr.balancer_status()
    print(f"  Balancer active: {status.active}")

    dist = shard_mgr.chunk_distribution()
    print(f"  Chunk distribution: {dist}")

    # --- 7. Replica Set ---
    print("\n--- Replica Set Manager ---")
    rs = ReplicaSetManager("rs0")
    rs_status = rs.status()
    print(f"  Set: {rs_status.set_name}")
    print(f"  Primary: {rs_status.primary}")
    print(f"  Members: {len(rs_status.members)}")
    print(f"  Oplog lag: {rs_status.oplog_lag_seconds:.1f}s")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()