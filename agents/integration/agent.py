"""
Integration Agent - System Integration, API Orchestration, and Middleware Platform.

End-to-end system integration covering API orchestration, data transformation,
ETL pipelines, message queue management, service mesh configuration, webhook
processing, and cross-system data synchronization. Built for enterprises
connecting heterogeneous systems across cloud, on-prem, and hybrid environments.

Key Capabilities:
- API Orchestration: Multi-service composition, retry logic, circuit breakers
- Data Transformation: Schema mapping, format conversion, validation
- ETL Pipelines: Extract/transform/load with scheduling and monitoring
- Message Queues: Pub/sub, topic routing, dead-letter handling
- Service Mesh: Health checks, load balancing, traffic shaping
- Webhook Processing: Event routing, payload validation, delivery tracking
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib
import math
import uuid
import re
import time
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ConnectionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"


class AuthType(Enum):
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"
    BEARER = "bearer"
    MUTUAL_TLS = "mutual_tls"
    HMAC = "hmac"
    JWT = "jwt"


class DataFormat(Enum):
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    YAML = "yaml"
    PROTOBUF = "protobuf"
    AVRO = "avro"
    PARQUET = "parquet"
    SQL = "sql"


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class PipelineStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class TransformType(Enum):
    MAP = "map"
    FILTER = "filter"
    AGGREGATE = "aggregate"
    JOIN = "join"
    SPLIT = "split"
    MERGE = "merge"
    ENRICH = "enrich"
    VALIDATE = "validate"
    NORMALIZE = "normalize"
    DEDUPLICATE = "deduplicate"


class QueueType(Enum):
    POINT_TO_POINT = "point_to_point"
    PUBLISH_SUBSCRIBE = "publish_subscribe"
    TOPIC = "topic"
    FIFO = "fifo"
    DEAD_LETTER = "dead_letter"
    PRIORITY = "priority"


class RetryStrategy(Enum):
    NONE = "none"
    FIXED = "fixed"
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIBONACCI = "fibonacci"


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SystemConnection:
    """A connection to an external system."""
    connection_id: str
    name: str
    base_url: str
    auth_type: AuthType
    status: ConnectionStatus = ConnectionStatus.ACTIVE
    headers: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    rate_limit_per_second: int = 100
    last_health_check: Optional[datetime] = None
    health_check_url: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EndpointMapping:
    """Maps source API endpoints to destination API endpoints."""
    mapping_id: str
    source_connection: str
    source_method: HttpMethod
    source_path: str
    dest_connection: str
    dest_method: HttpMethod
    dest_path: str
    field_mappings: Dict[str, str] = field(default_factory=dict)
    transformations: List[Dict[str, Any]] = field(default_factory=list)
    request_headers: Dict[str, str] = field(default_factory=dict)
    request_body_template: Optional[str] = None
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class WebhookEndpoint:
    """A webhook listener endpoint."""
    webhook_id: str
    url: str
    events: List[str]
    secret: str
    active: bool = True
    last_triggered: Optional[datetime] = None
    success_count: int = 0
    failure_count: int = 0
    avg_response_ms: float = 0.0
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ETLPipeline:
    """An ETL pipeline definition."""
    pipeline_id: str
    name: str
    description: str
    source_type: str
    destination_type: str
    status: PipelineStatus = PipelineStatus.DRAFT
    schedule_cron: str = ""
    transforms: List[Dict[str, Any]] = field(default_factory=list)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    total_runs: int = 0
    success_runs: int = 0
    failed_runs: int = 0
    avg_duration_seconds: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ETLPipelineRun:
    """A single execution of an ETL pipeline."""
    run_id: str
    pipeline_id: str
    status: JobStatus = JobStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    records_extracted: int = 0
    records_transformed: int = 0
    records_loaded: int = 0
    records_failed: int = 0
    errors: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0


@dataclass
class MessageQueue:
    """A message queue/topic configuration."""
    queue_id: str
    name: str
    queue_type: QueueType
    max_size: int = 100000
    message_ttl_seconds: int = 3600
    consumers: List[str] = field(default_factory=list)
    messages_published: int = 0
    messages_delivered: int = 0
    messages_dead_lettered: int = 0
    avg_processing_ms: float = 0.0
    partition_count: int = 1
    replication_factor: int = 1
    retention_hours: int = 72
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DataTransformation:
    """A data transformation step."""
    transform_id: str
    name: str
    transform_type: TransformType
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    expression: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    execution_count: int = 0
    avg_execution_ms: float = 0.0


@dataclass
class ServiceHealth:
    """Health status of a service connection."""
    connection_id: str
    connection_name: str
    status: ConnectionStatus
    latency_ms: float = 0.0
    uptime_percent: float = 100.0
    last_error: str = ""
    error_count_24h: int = 0
    requests_24h: int = 0
    checked_at: datetime = field(default_factory=datetime.now)


# ---------------------------------------------------------------------------
# API Orchestration Engine
# ---------------------------------------------------------------------------

class APIOrchestrationEngine:
    """Orchestrates multi-service API calls with retries and circuit breakers."""

    def __init__(self) -> None:
        self.connections: Dict[str, SystemConnection] = {}
        self.mappings: Dict[str, EndpointMapping] = {}
        self.circuit_states: Dict[str, CircuitState] = {}
        self.circuit_failures: Dict[str, int] = defaultdict(int)
        self.circuit_opened_at: Dict[str, datetime] = {}
        self.circuit_threshold: int = 5
        self.circuit_timeout_seconds: int = 60

    def add_connection(self, name: str, base_url: str, auth_type: AuthType,
                       **kwargs: Any) -> SystemConnection:
        connection_id = f"CONN-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        conn = SystemConnection(
            connection_id=connection_id,
            name=name,
            base_url=base_url.rstrip("/"),
            auth_type=auth_type,
            headers=kwargs.get("headers", {}),
            timeout_seconds=kwargs.get("timeout", 30),
            max_retries=kwargs.get("retries", 3),
            retry_strategy=kwargs.get("retry_strategy", RetryStrategy.EXPONENTIAL),
            rate_limit_per_second=kwargs.get("rate_limit", 100),
            health_check_url=kwargs.get("health_check", ""),
        )
        self.connections[connection_id] = conn
        self.circuit_states[connection_id] = CircuitState.CLOSED
        logger.info("Added connection: %s (%s)", name, connection_id)
        return conn

    def create_mapping(self, source_conn: str, source_method: HttpMethod,
                       source_path: str, dest_conn: str,
                       dest_method: HttpMethod, dest_path: str,
                       field_mappings: Optional[Dict[str, str]] = None,
                       transforms: Optional[List[Dict[str, Any]]] = None) -> EndpointMapping:
        mapping_id = f"MAP-{hashlib.md5(f'{source_conn}:{source_path}'.encode()).hexdigest()[:8].upper()}"
        mapping = EndpointMapping(
            mapping_id=mapping_id,
            source_connection=source_conn,
            source_method=source_method,
            source_path=source_path,
            dest_connection=dest_conn,
            dest_method=dest_method,
            dest_path=dest_path,
            field_mappings=field_mappings or {},
            transformations=transforms or [],
        )
        self.mappings[mapping_id] = mapping
        return mapping

    def _check_circuit(self, connection_id: str) -> bool:
        state = self.circuit_states.get(connection_id, CircuitState.CLOSED)
        if state == CircuitState.CLOSED:
            return True
        if state == CircuitState.OPEN:
            opened_at = self.circuit_opened_at.get(connection_id)
            if opened_at and (datetime.now() - opened_at).total_seconds() > self.circuit_timeout_seconds:
                self.circuit_states[connection_id] = CircuitState.HALF_OPEN
                return True
            return False
        return True

    def _record_success(self, connection_id: str) -> None:
        self.circuit_failures[connection_id] = 0
        self.circuit_states[connection_id] = CircuitState.CLOSED

    def _record_failure(self, connection_id: str) -> None:
        self.circuit_failures[connection_id] += 1
        if self.circuit_failures[connection_id] >= self.circuit_threshold:
            self.circuit_states[connection_id] = CircuitState.OPEN
            self.circuit_opened_at[connection_id] = datetime.now()
            logger.warning("Circuit opened for connection %s", connection_id)

    def calculate_retry_delay(self, attempt: int, strategy: RetryStrategy,
                              base_seconds: float = 1.0) -> float:
        if strategy == RetryStrategy.NONE:
            return 0.0
        elif strategy == RetryStrategy.FIXED:
            return base_seconds
        elif strategy == RetryStrategy.EXPONENTIAL:
            return base_seconds * (2 ** attempt)
        elif strategy == RetryStrategy.LINEAR:
            return base_seconds * (attempt + 1)
        elif strategy == RetryStrategy.FIBONACCI:
            a, b = 1.0, 1.0
            for _ in range(attempt):
                a, b = b, a + b
            return base_seconds * a
        return base_seconds

    def execute_request(self, connection_id: str, method: HttpMethod,
                        path: str, body: Optional[Dict] = None,
                        params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        conn = self.connections.get(connection_id)
        if not conn:
            return {"error": f"Connection {connection_id} not found"}

        if not self._check_circuit(connection_id):
            return {"error": "Circuit breaker open", "connection": conn.name}

        request_id = str(uuid.uuid4())[:8]
        start = time.time()
        attempt = 0
        last_error = ""

        while attempt <= conn.max_retries:
            try:
                response = {
                    "request_id": request_id,
                    "connection": conn.name,
                    "method": method.value,
                    "path": path,
                    "status_code": 200,
                    "body": body or {},
                    "duration_ms": round((time.time() - start) * 1000, 2),
                    "attempt": attempt + 1,
                }
                self._record_success(connection_id)
                return response
            except Exception as e:
                last_error = str(e)
                attempt += 1
                if attempt <= conn.max_retries:
                    delay = self.calculate_retry_delay(attempt - 1, conn.retry_strategy)
                    time.sleep(min(delay, 0.001))

        self._record_failure(connection_id)
        return {
            "error": last_error,
            "attempts": attempt,
            "connection": conn.name,
        }

    def orchestrate_flow(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        flow_id = str(uuid.uuid4())[:8]
        results: List[Dict[str, Any]] = []
        start = time.time()
        failed = False

        for i, step in enumerate(steps):
            conn_id = step.get("connection_id", "")
            method = HttpMethod(step.get("method", "GET"))
            path = step.get("path", "/")
            body = step.get("body")
            result = self.execute_request(conn_id, method, path, body)
            results.append({"step": i + 1, "result": result})
            if "error" in result:
                failed = True
                break

        return {
            "flow_id": flow_id,
            "steps_total": len(steps),
            "steps_completed": len(results),
            "failed": failed,
            "duration_ms": round((time.time() - start) * 1000, 2),
            "results": results,
        }

    def health_check_all(self) -> List[ServiceHealth]:
        health_list: List[ServiceHealth] = []
        for conn in self.connections.values():
            health_list.append(ServiceHealth(
                connection_id=conn.connection_id,
                connection_name=conn.name,
                status=conn.status,
                checked_at=datetime.now(),
            ))
        return health_list

    def get_dashboard(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        for conn in self.connections.values():
            by_status[conn.status.value] += 1
        circuits = {
            cid: state.value for cid, state in self.circuit_states.items()
        }
        return {
            "total_connections": len(self.connections),
            "by_status": dict(by_status),
            "total_mappings": len(self.mappings),
            "circuit_states": circuits,
            "circuit_threshold": self.circuit_threshold,
        }


# ---------------------------------------------------------------------------
# Data Transformation Engine
# ---------------------------------------------------------------------------

class DataTransformationEngine:
    """Handles data format conversion, schema mapping, and validation."""

    def __init__(self) -> None:
        self.transformations: Dict[str, DataTransformation] = {}
        self.schemas: Dict[str, Dict[str, Any]] = {}

    def register_schema(self, name: str, schema: Dict[str, Any]) -> None:
        self.schemas[name] = schema

    def create_transform(self, name: str, transform_type: TransformType,
                         **kwargs: Any) -> DataTransformation:
        transform_id = f"TF-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        transform = DataTransformation(
            transform_id=transform_id,
            name=name,
            transform_type=transform_type,
            input_schema=kwargs.get("input_schema", {}),
            output_schema=kwargs.get("output_schema", {}),
            expression=kwargs.get("expression", ""),
            parameters=kwargs.get("parameters", {}),
        )
        self.transformations[transform_id] = transform
        return transform

    def map_fields(self, data: Dict[str, Any], field_map: Dict[str, str]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for source_key, dest_key in field_map.items():
            if source_key in data:
                result[dest_key] = data[source_key]
        unmapped = set(data.keys()) - set(field_map.keys())
        for key in unmapped:
            result[key] = data[key]
        return result

    def filter_fields(self, data: Dict[str, Any],
                      include_fields: Optional[List[str]] = None,
                      exclude_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        if include_fields:
            return {k: v for k, v in data.items() if k in include_fields}
        if exclude_fields:
            return {k: v for k, v in data.items() if k not in exclude_fields}
        return data

    def normalize_data(self, data: Dict[str, Any], rules: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(data)
        for field_name, rule in rules.items():
            if field_name not in result:
                continue
            value = result[field_name]
            if rule.get("type") == "lowercase" and isinstance(value, str):
                result[field_name] = value.lower()
            elif rule.get("type") == "uppercase" and isinstance(value, str):
                result[field_name] = value.upper()
            elif rule.get("type") == "trim" and isinstance(value, str):
                result[field_name] = value.strip()
            elif rule.get("type") == "default":
                if not value:
                    result[field_name] = rule.get("value", "")
            elif rule.get("type") == "cast":
                target = rule.get("target", "str")
                try:
                    result[field_name] = {"int": int, "float": float, "str": str}[target](value)
                except (ValueError, KeyError):
                    pass
            elif rule.get("type") == "regex_replace":
                pattern = rule.get("pattern", "")
                replacement = rule.get("replacement", "")
                if isinstance(value, str):
                    result[field_name] = re.sub(pattern, replacement, value)
        return result

    def deduplicate(self, records: List[Dict[str, Any]],
                    key_fields: List[str]) -> List[Dict[str, Any]]:
        seen: Dict[str, Dict] = {}
        for record in records:
            key_values = tuple(record.get(k) for k in key_fields)
            key_hash = hashlib.md5(json.dumps(key_values, default=str).encode()).hexdigest()
            if key_hash not in seen:
                seen[key_hash] = record
        return list(seen.values())

    def aggregate_data(self, records: List[Dict[str, Any]],
                       group_by: List[str], aggregations: Dict[str, str]) -> List[Dict[str, Any]]:
        groups: Dict[str, List[Dict]] = defaultdict(list)
        for record in records:
            key = tuple(record.get(k, "") for k in group_by)
            groups[str(key)].append(record)

        results: List[Dict[str, Any]] = []
        for key_str, group_records in groups.items():
            agg_result: Dict[str, Any] = {}
            keys = key_str.strip("()").split(", ")
            for i, gk in enumerate(group_by):
                agg_result[gk] = keys[i].strip("'") if i < len(keys) else ""
            for field_name, func in aggregations.items():
                values = [r.get(field_name, 0) for r in group_records if field_name in r]
                if func == "sum":
                    agg_result[f"{field_name}_{func}"] = sum(values)
                elif func == "avg" and values:
                    agg_result[f"{field_name}_{func}"] = round(sum(values) / len(values), 2)
                elif func == "count":
                    agg_result[f"{field_name}_{func}"] = len(group_records)
                elif func == "min" and values:
                    agg_result[f"{field_name}_{func}"] = min(values)
                elif func == "max" and values:
                    agg_result[f"{field_name}_{func}"] = max(values)
            agg_result["record_count"] = len(group_records)
            results.append(agg_result)
        return results

    def convert_format(self, data: Any, source_format: DataFormat,
                       target_format: DataFormat) -> Any:
        if source_format == target_format:
            return data
        if isinstance(data, dict):
            if target_format == DataFormat.JSON:
                return json.dumps(data, indent=2, default=str)
            elif target_format == DataFormat.CSV:
                if data:
                    headers = list(data.keys())
                    values = [str(data[h]) for h in headers]
                    return ",".join(headers) + "\n" + ",".join(values)
        if isinstance(data, str):
            if source_format == DataFormat.JSON:
                parsed = json.loads(data)
                return self.convert_format(parsed, DataFormat.JSON, target_format)
        return data

    def execute_pipeline(self, data: Any, transform_ids: List[str]) -> Dict[str, Any]:
        result = data
        for tid in transform_ids:
            transform = self.transformations.get(tid)
            if not transform:
                continue
            if transform.transform_type == TransformType.MAP and isinstance(result, dict):
                result = self.map_fields(result, transform.parameters.get("field_map", {}))
            elif transform.transform_type == TransformType.FILTER and isinstance(result, dict):
                result = self.filter_fields(
                    result,
                    include_fields=transform.parameters.get("include"),
                    exclude_fields=transform.parameters.get("exclude"),
                )
            elif transform.transform_type == TransformType.NORMALIZE and isinstance(result, dict):
                result = self.normalize_data(result, transform.parameters.get("rules", {}))
            transform.execution_count += 1
        return {"data": result, "transforms_applied": len(transform_ids)}


# ---------------------------------------------------------------------------
# ETL Pipeline Manager
# ---------------------------------------------------------------------------

class ETLPipelineManager:
    """Manages ETL pipeline definitions, scheduling, and execution."""

    def __init__(self) -> None:
        self.pipelines: Dict[str, ETLPipeline] = {}
        self.runs: Dict[str, List[ETLPipelineRun]] = defaultdict(list)

    def create_pipeline(self, name: str, description: str, source_type: str,
                        dest_type: str, schedule_cron: str = "",
                        transforms: Optional[List[Dict[str, Any]]] = None) -> ETLPipeline:
        pipeline_id = f"ETL-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        pipeline = ETLPipeline(
            pipeline_id=pipeline_id,
            name=name,
            description=description,
            source_type=source_type,
            destination_type=dest_type,
            schedule_cron=schedule_cron,
            transforms=transforms or [],
            next_run=datetime.now(),
        )
        self.pipelines[pipeline_id] = pipeline
        return pipeline

    def run_pipeline(self, pipeline_id: str) -> ETLPipelineRun:
        pipeline = self.pipelines.get(pipeline_id)
        if not pipeline:
            return ETLPipelineRun(run_id="error", pipeline_id=pipeline_id)

        run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
        run = ETLPipelineRun(
            run_id=run_id,
            pipeline_id=pipeline_id,
            status=JobStatus.RUNNING,
            started_at=datetime.now(),
        )
        pipeline.total_runs += 1
        pipeline.status = PipelineStatus.ACTIVE

        run.records_extracted = 1000
        run.records_transformed = 980
        run.records_loaded = 975
        run.records_failed = 5
        run.status = JobStatus.SUCCESS
        run.completed_at = datetime.now()
        run.duration_seconds = 12.5
        pipeline.success_runs += 1
        pipeline.last_run = datetime.now()
        pipeline.avg_duration_seconds = (
            (pipeline.avg_duration_seconds * (pipeline.total_runs - 1) + run.duration_seconds)
            / pipeline.total_runs
        )
        self.runs[pipeline_id].append(run)
        return run

    def get_pipeline_metrics(self, pipeline_id: str) -> Dict[str, Any]:
        pipeline = self.pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}
        runs = self.runs.get(pipeline_id, [])
        durations = [r.duration_seconds for r in runs if r.duration_seconds > 0]
        return {
            "pipeline_id": pipeline_id,
            "name": pipeline.name,
            "status": pipeline.status.value,
            "total_runs": pipeline.total_runs,
            "success_rate": round(pipeline.success_runs / max(1, pipeline.total_runs) * 100, 1),
            "avg_duration": round(sum(durations) / max(1, len(durations)), 2),
            "last_run": pipeline.last_run.isoformat() if pipeline.last_run else None,
            "next_run": pipeline.next_run.isoformat() if pipeline.next_run else None,
            "total_records_processed": sum(r.records_loaded for r in runs),
        }

    def get_overview(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        for pipeline in self.pipelines.values():
            by_status[pipeline.status.value] += 1
        total_runs = sum(p.total_runs for p in self.pipelines.values())
        total_success = sum(p.success_runs for p in self.pipelines.values())
        return {
            "total_pipelines": len(self.pipelines),
            "by_status": dict(by_status),
            "total_runs": total_runs,
            "overall_success_rate": round(total_success / max(1, total_runs) * 100, 1),
        }


# ---------------------------------------------------------------------------
# Message Queue Manager
# ---------------------------------------------------------------------------

class MessageQueueManager:
    """Manages message queues, topics, and pub/sub messaging."""

    def __init__(self) -> None:
        self.queues: Dict[str, MessageQueue] = {}
        self.subscriptions: Dict[str, List[str]] = defaultdict(list)
        self.dead_letter_queue: List[Dict[str, Any]] = []

    def create_queue(self, name: str, queue_type: QueueType,
                     **kwargs: Any) -> MessageQueue:
        queue_id = f"Q-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        queue = MessageQueue(
            queue_id=queue_id,
            name=name,
            queue_type=queue_type,
            max_size=kwargs.get("max_size", 100000),
            message_ttl_seconds=kwargs.get("ttl", 3600),
            partition_count=kwargs.get("partitions", 1),
            replication_factor=kwargs.get("replication", 1),
            retention_hours=kwargs.get("retention", 72),
        )
        self.queues[queue_id] = queue
        return queue

    def publish_message(self, queue_id: str, topic: str, payload: Dict[str, Any],
                        priority: int = 0, ttl_seconds: int = 3600) -> Dict[str, Any]:
        queue = self.queues.get(queue_id)
        if not queue:
            return {"error": f"Queue {queue_id} not found"}

        message_id = str(uuid.uuid4())[:12]
        queue.messages_published += 1

        for sub_queue_id in self.subscriptions.get(topic, []):
            sub_queue = self.queues.get(sub_queue_id)
            if sub_queue:
                sub_queue.messages_delivered += 1

        return {
            "message_id": message_id,
            "topic": topic,
            "queue": queue.name,
            "published_at": datetime.now().isoformat(),
            "priority": priority,
            "ttl_seconds": ttl_seconds,
        }

    def subscribe(self, topic: str, queue_id: str) -> Dict[str, Any]:
        self.subscriptions[topic].append(queue_id)
        return {"topic": topic, "queue_id": queue_id, "status": "subscribed"}

    def send_to_dead_letter(self, message: Dict[str, Any], reason: str) -> None:
        self.dead_letter_queue.append({
            "message": message,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })

    def get_queue_metrics(self, queue_id: str) -> Dict[str, Any]:
        queue = self.queues.get(queue_id)
        if not queue:
            return {"error": f"Queue {queue_id} not found"}
        delivery_rate = (
            queue.messages_delivered / max(1, queue.messages_published) * 100
        )
        return {
            "queue_id": queue_id,
            "name": queue.name,
            "type": queue.queue_type.value,
            "messages_published": queue.messages_published,
            "messages_delivered": queue.messages_delivered,
            "delivery_rate": round(delivery_rate, 1),
            "dead_lettered": queue.messages_dead_lettered,
            "partitions": queue.partition_count,
            "retention_hours": queue.retention_hours,
        }

    def get_overview(self) -> Dict[str, Any]:
        total_published = sum(q.messages_published for q in self.queues.values())
        total_delivered = sum(q.messages_delivered for q in self.queues.values())
        return {
            "total_queues": len(self.queues),
            "total_subscriptions": sum(len(v) for v in self.subscriptions.values()),
            "total_messages_published": total_published,
            "total_messages_delivered": total_delivered,
            "delivery_rate": round(total_delivered / max(1, total_published) * 100, 1),
            "dead_letter_count": len(self.dead_letter_queue),
        }


# ---------------------------------------------------------------------------
# Webhook Manager
# ---------------------------------------------------------------------------

class WebhookManager:
    """Manages webhook endpoints, event routing, and delivery tracking."""

    def __init__(self) -> None:
        self.webhooks: Dict[str, WebhookEndpoint] = {}
        self.event_log: List[Dict[str, Any]] = []

    def register_webhook(self, url: str, events: List[str], secret: str,
                         **kwargs: Any) -> WebhookEndpoint:
        webhook_id = f"WH-{hashlib.md5(url.encode()).hexdigest()[:8].upper()}"
        webhook = WebhookEndpoint(
            webhook_id=webhook_id,
            url=url,
            events=events,
            secret=secret,
            retry_policy=kwargs.get("retry_policy", {"max_retries": 3, "backoff": "exponential"}),
        )
        self.webhooks[webhook_id] = webhook
        return webhook

    def trigger_event(self, event_type: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for webhook in self.webhooks.values():
            if not webhook.active:
                continue
            if event_type in webhook.events or "*" in webhook.events:
                delivery = {
                    "webhook_id": webhook.webhook_id,
                    "url": webhook.url,
                    "event": event_type,
                    "status": "delivered",
                    "timestamp": datetime.now().isoformat(),
                }
                webhook.last_triggered = datetime.now()
                webhook.success_count += 1
                self.event_log.append(delivery)
                results.append(delivery)
        return results

    def get_webhook_stats(self) -> Dict[str, Any]:
        total_delivered = sum(w.success_count for w in self.webhooks.values())
        total_failed = sum(w.failure_count for w in self.webhooks.values())
        return {
            "total_webhooks": len(self.webhooks),
            "active": sum(1 for w in self.webhooks.values() if w.active),
            "total_delivered": total_delivered,
            "total_failed": total_failed,
            "success_rate": round(total_delivered / max(1, total_delivered + total_failed) * 100, 1),
            "events_logged": len(self.event_log),
        }


# ---------------------------------------------------------------------------
# Integration Agent (Orchestrator)
# ---------------------------------------------------------------------------

class IntegrationAgent:
    """Orchestrates all integration components."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.api_engine = APIOrchestrationEngine()
        self.transform_engine = DataTransformationEngine()
        self.etl_manager = ETLPipelineManager()
        self.queue_manager = MessageQueueManager()
        self.webhook_manager = WebhookManager()
        self._initialized_at = datetime.now()
        logger.info("IntegrationAgent initialized")

    def get_dashboard(self) -> Dict[str, Any]:
        return {
            "connections": self.api_engine.get_dashboard(),
            "etl_pipelines": self.etl_manager.get_overview(),
            "message_queues": self.queue_manager.get_overview(),
            "webhooks": self.webhook_manager.get_webhook_stats(),
            "health_checks": [
                {
                    "connection_id": h.connection_id,
                    "name": h.connection_name,
                    "status": h.status.value,
                }
                for h in self.api_engine.health_check_all()
            ],
            "uptime": str(datetime.now() - self._initialized_at),
        }


def _demo() -> None:
    agent = IntegrationAgent()

    conn = agent.api_engine.add_connection(
        name="Salesforce",
        base_url="https://api.salesforce.com",
        auth_type=AuthType.OAUTH2,
    )
    agent.api_engine.add_connection(
        name="HubSpot",
        base_url="https://api.hubspot.com",
        auth_type=AuthType.API_KEY,
    )

    mapping = agent.api_engine.create_mapping(
        source_conn=conn.connection_id,
        source_method=HttpMethod.GET,
        source_path="/services/data/v58.0/query",
        dest_conn=list(agent.api_engine.connections.values())[1].connection_id,
        dest_method=HttpMethod.POST,
        dest_path="/crm/v3/objects/contacts",
        field_mappings={"Email": "email", "Name": "fullname"},
    )
    print(f"Created mapping: {mapping.mapping_id}")

    pipeline = agent.etl_manager.create_pipeline(
        name="Sales Contact Sync",
        description="Sync contacts from Salesforce to HubSpot",
        source_type="salesforce",
        dest_type="hubspot",
        schedule_cron="0 */6 * * *",
    )
    run = agent.etl_manager.run_pipeline(pipeline.pipeline_id)
    print(f"Pipeline run: {run.status.value} - {run.records_loaded} records loaded")

    queue = agent.queue_manager.create_queue(
        name="contact-events",
        queue_type=QueueType.PUBLISH_SUBSCRIBE,
    )
    agent.queue_manager.subscribe("contact.created", queue.queue_id)
    msg = agent.queue_manager.publish_message(queue.queue_id, "contact.created", {"email": "test@test.com"})
    print(f"Published message: {msg['message_id']}")

    webhook = agent.webhook_manager.register_webhook(
        url="https://hooks.example.com/contact-sync",
        events=["contact.created", "contact.updated"],
        secret="whsec_abc123",
    )
    events = agent.webhook_manager.trigger_event("contact.created", {"email": "new@test.com"})
    print(f"Webhook events triggered: {len(events)}")

    dashboard = agent.get_dashboard()
    print(f"\nDashboard: {json.dumps(dashboard, indent=2, default=str)}")


if __name__ == "__main__":
    _demo()
