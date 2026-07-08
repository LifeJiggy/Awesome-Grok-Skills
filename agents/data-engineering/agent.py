"""
Data Engineering Agent - ETL/ELT Pipeline Management
Author: Awesome Grok Skills | License: MIT | Version: 2.0.0
"""

import logging
import uuid
import json
import re
import time
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("data_engineering")


# ═══════════════════════════════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════════════════════════════

class PipelineStatus(Enum):
    CREATED = "created"; PENDING = "pending"; RUNNING = "running"
    PAUSED = "paused"; SUCCESS = "success"; FAILED = "failed"
    CANCELLED = "cancelled"; RETRYING = "retrying"


class DataQualityLevel(Enum):
    EXCELLENT = "excellent"; GOOD = "good"; FAIR = "fair"
    POOR = "poor"; CRITICAL = "critical"


class Severity(Enum):
    INFO = "info"; LOW = "low"; MEDIUM = "medium"
    HIGH = "high"; CRITICAL = "critical"


class StorageFormat(Enum):
    PARQUET = "parquet"; ORC = "orc"; AVRO = "avro"; CSV = "csv"
    JSON = "json"; DELTA = "delta"; ICEBERG = "iceberg"


class PipelineType(Enum):
    ETL = "etl"; ELT = "elt"; STREAMING = "streaming"
    BATCH = "batch"; HYBRID = "hybrid"; LAMBDA = "lambda"; KAPPA = "kappa"


class WarehouseLayer(Enum):
    RAW = "raw"; STAGING = "staging"; CURATED = "curated"
    ANALYTICS = "analytics"; MART = "mart"; ARCHIVE = "archive"


class StreamingMode(Enum):
    EXACTLY_ONCE = "exactly_once"; AT_LEAST_ONCE = "at_least_once"; BEST_EFFORT = "best_effort"


class IaCTemplateType(Enum):
    TERRAFORM = "terraform"; CLOUDFORMATION = "cloudformation"
    PULUMI = "pulumi"; CDK = "cdk"; ANSIBLE = "ansible"


class SchemaEvolutionStrategy(Enum):
    FAIL = "fail"; IGNORE = "ignore"
    ADD_COLUMNS = "add_columns"; TYPE_PROMOTION = "type_promotion"


class CatalogEntryType(Enum):
    TABLE = "table"; VIEW = "view"; DASHBOARD = "dashboard"
    PIPELINE = "pipeline"; DATASET = "dataset"; TOPIC = "topic"


# ═══════════════════════════════════════════════════════════════════════════
# Data Classes
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ColumnDefinition:
    name: str; data_type: str; nullable: bool = True
    primary_key: bool = False; description: str = ""
    default_value: Any = None; validation_rules: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class SchemaDefinition:
    schema_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""; version: int = 1
    columns: List[ColumnDefinition] = field(default_factory=list)
    partition_keys: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    compatibility: SchemaEvolutionStrategy = SchemaEvolutionStrategy.ADD_COLUMNS
    description: str = ""


@dataclass
class PipelineConfig:
    pipeline_id: str = field(default_factory=lambda: f"pipe_{uuid.uuid4().hex[:12]}")
    name: str = ""; pipeline_type: PipelineType = PipelineType.ETL
    source: Dict[str, Any] = field(default_factory=dict)
    transforms: List[Dict[str, Any]] = field(default_factory=list)
    sink: Dict[str, Any] = field(default_factory=dict)
    schedule: str = "0 * * * *"; retry_count: int = 3
    timeout_seconds: int = 3600; enabled: bool = True
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PipelineRun:
    run_id: str = field(default_factory=lambda: f"run_{uuid.uuid4().hex[:12]}")
    pipeline_id: str = ""; status: PipelineStatus = PipelineStatus.PENDING
    started_at: Optional[datetime] = None; finished_at: Optional[datetime] = None
    records_extracted: int = 0; records_transformed: int = 0
    records_loaded: int = 0; records_failed: int = 0
    error_message: Optional[str] = None
    stages: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityCheck:
    check_id: str = field(default_factory=lambda: f"qc_{uuid.uuid4().hex[:8]}")
    name: str = ""; column: str = ""; rule: str = ""
    severity: Severity = Severity.MEDIUM; enabled: bool = True; description: str = ""


@dataclass
class QualityResult:
    check_id: str = ""; check_name: str = ""; passed: bool = True
    records_checked: int = 0; records_failed: int = 0
    severity: Severity = Severity.MEDIUM; message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LineageNode:
    node_id: str = ""; name: str = ""; node_type: str = "table"
    upstream: List[str] = field(default_factory=list)
    downstream: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    owner: str = ""; last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class StreamingTopic:
    topic_id: str = field(default_factory=lambda: f"topic_{uuid.uuid4().hex[:8]}")
    name: str = ""; partitions: int = 6; replication_factor: int = 3
    retention_hours: int = 168; schema_registry_subject: str = ""
    mode: StreamingMode = StreamingMode.AT_LEAST_ONCE


@dataclass
class CatalogEntry:
    entry_id: str = field(default_factory=lambda: f"cat_{uuid.uuid4().hex[:8]}")
    name: str = ""; entry_type: CatalogEntryType = CatalogEntryType.TABLE
    description: str = ""; owner: str = ""
    tags: List[str] = field(default_factory=list)
    schema: Optional[SchemaDefinition] = None; location: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    access_level: str = "internal"


@dataclass
class IaCResource:
    resource_id: str = field(default_factory=lambda: f"iac_{uuid.uuid4().hex[:8]}")
    name: str = ""; resource_type: str = ""
    template_type: IaCTemplateType = IaCTemplateType.TERRAFORM
    config: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list); status: str = "planned"


@dataclass
class AlertRule:
    alert_id: str = field(default_factory=lambda: f"alert_{uuid.uuid4().hex[:8]}")
    name: str = ""; metric: str = ""; threshold: float = 0.0
    operator: str = "gt"; severity: Severity = Severity.MEDIUM
    channels: List[str] = field(default_factory=list); enabled: bool = True


# ═══════════════════════════════════════════════════════════════════════════
# Abstract Base & Transform Implementations
# ═══════════════════════════════════════════════════════════════════════════

class ComponentBase(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"data_engineering.{name}")
        self._metrics: Dict[str, Any] = defaultdict(int)
        self._start_time: Optional[datetime] = None

    def start(self):
        self._start_time = datetime.now()
        self.logger.info("Component '%s' started", self.name)

    def stop(self):
        elapsed = (datetime.now() - self._start_time).total_seconds() if self._start_time else 0
        self.logger.info("Component '%s' stopped after %.2fs", self.name, elapsed)

    def increment_metric(self, key: str, value: int = 1):
        self._metrics[key] += value

    def get_metrics(self) -> Dict[str, Any]:
        return dict(self._metrics)


class TransformBase(ABC):
    @abstractmethod
    def execute(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]: ...
    @abstractmethod
    def validate_input(self, data: List[Dict[str, Any]]) -> bool: ...


class FilterTransform(TransformBase):
    def __init__(self, column: str, operator: str, value: Any):
        self.column = column; self.operator = operator; self.value = value

    def validate_input(self, data: List[Dict[str, Any]]) -> bool:
        return not data or self.column in data[0]

    def execute(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ops = {
            "eq": lambda v, t: v == t, "ne": lambda v, t: v != t,
            "gt": lambda v, t: v > t, "lt": lambda v, t: v < t,
            "gte": lambda v, t: v >= t, "lte": lambda v, t: v <= t,
            "contains": lambda v, t: str(t) in str(v),
            "not_contains": lambda v, t: str(t) not in str(v),
            "in": lambda v, t: v in t if isinstance(t, (list, set, tuple)) else False,
        }
        fn = ops.get(self.operator)
        if fn is None:
            raise ValueError(f"Unsupported operator: {self.operator}")
        return [row for row in data if fn(row.get(self.column), self.value)]


class AggregateTransform(TransformBase):
    def __init__(self, group_keys: List[str], aggregations: Dict[str, str]):
        self.group_keys = group_keys; self.aggregations = aggregations

    def validate_input(self, data: List[Dict[str, Any]]) -> bool:
        if not data: return True
        sample = data[0]
        return all(k in sample for k in self.group_keys) and all(c in sample for c in self.aggregations)

    def execute(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        groups: Dict[tuple, List[Dict]] = defaultdict(list)
        for row in data:
            groups[tuple(row.get(k) for k in self.group_keys)].append(row)
        agg_fns = {
            "sum": lambda v: sum(v), "avg": lambda v: sum(v)/len(v) if v else 0,
            "min": lambda v: min(v) if v else None, "max": lambda v: max(v) if v else None,
            "count": lambda v: len(v), "count_distinct": lambda v: len(set(v)),
        }
        results = []
        for gk, rows in groups.items():
            result = {self.group_keys[i]: gk[i] for i in range(len(self.group_keys))}
            for col, an in self.aggregations.items():
                vals = [r.get(col) for r in rows if r.get(col) is not None]
                fn = agg_fns.get(an)
                if fn: result[f"{an}_{col}"] = fn(vals)
            results.append(result)
        return results


class JoinTransform(TransformBase):
    def __init__(self, right_data: List[Dict[str, Any]], join_keys: List[str], join_type: str = "inner"):
        self.right_data = right_data; self.join_keys = join_keys; self.join_type = join_type

    def validate_input(self, data: List[Dict[str, Any]]) -> bool: return True

    def execute(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ri: Dict[tuple, List[Dict]] = defaultdict(list)
        for row in self.right_data:
            ri[tuple(row.get(k) for k in self.join_keys)].append(row)
        results, matched = [], set()
        for lr in data:
            lk = tuple(lr.get(k) for k in self.join_keys)
            for rr in ri.get(lk, []):
                matched.add(lk)
                merged = {**lr}
                for rk, rv in rr.items():
                    merged[f"right_{rk}" if rk in merged else rk] = rv
                results.append(merged)
        if self.join_type == "left":
            for lr in data:
                if tuple(lr.get(k) for k in self.join_keys) not in matched:
                    results.append(lr)
        if self.join_type == "full":
            for rk, rr in ri.items():
                if rk not in matched: results.extend(rr)
        return results


class RenameTransform(TransformBase):
    def __init__(self, renames: Dict[str, str]): self.renames = renames
    def validate_input(self, data: List[Dict[str, Any]]) -> bool: return True
    def execute(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{self.renames.get(k, k): v for k, v in row.items()} for row in data]


# ═══════════════════════════════════════════════════════════════════════════
# PipelineManager
# ═══════════════════════════════════════════════════════════════════════════

class PipelineManager(ComponentBase):
    def __init__(self):
        super().__init__("PipelineManager")
        self._pipelines: Dict[str, PipelineConfig] = {}
        self._runs: Dict[str, List[PipelineRun]] = defaultdict(list)
        self._lock = threading.Lock()

    def create_pipeline(self, name: str, source_config: Dict[str, Any],
                        transforms: List[Dict[str, Any]], sink_config: Dict[str, Any],
                        pipeline_type: PipelineType = PipelineType.ETL,
                        schedule: str = "0 * * * *",
                        tags: Optional[List[str]] = None) -> PipelineConfig:
        config = PipelineConfig(name=name, pipeline_type=pipeline_type, source=source_config,
                                transforms=transforms, sink=sink_config, schedule=schedule, tags=tags or [])
        with self._lock:
            self._pipelines[config.pipeline_id] = config
        self.increment_metric("pipelines_created")
        self.logger.info("Pipeline '%s' created (id=%s)", name, config.pipeline_id)
        return config

    def get_pipeline(self, pipeline_id: str) -> Optional[PipelineConfig]:
        return self._pipelines.get(pipeline_id)

    def list_pipelines(self, pipeline_type: Optional[PipelineType] = None,
                       tags: Optional[List[str]] = None) -> List[PipelineConfig]:
        results = list(self._pipelines.values())
        if pipeline_type: results = [p for p in results if p.pipeline_type == pipeline_type]
        if tags: results = [p for p in results if set(tags).issubset(set(p.tags))]
        return results

    def delete_pipeline(self, pipeline_id: str) -> bool:
        if pipeline_id in self._pipelines:
            del self._pipelines[pipeline_id]; return True
        return False

    def execute_pipeline(self, pipeline_id: str) -> PipelineRun:
        config = self._pipelines.get(pipeline_id)
        if not config: raise ValueError(f"Pipeline {pipeline_id} not found")
        run = PipelineRun(pipeline_id=pipeline_id, status=PipelineStatus.RUNNING, started_at=datetime.now())
        self.logger.info("Executing pipeline '%s' (run=%s)", config.name, run.run_id)
        try:
            data = self._extract(config)
            run.records_extracted = len(data)
            run.stages.append({"name": "extract", "status": "completed", "records": len(data)})
            data = self._transform(config, data)
            run.records_transformed = len(data)
            run.stages.append({"name": "transform", "status": "completed", "records": len(data)})
            loaded = self._load(config, data)
            run.records_loaded = loaded
            run.stages.append({"name": "load", "status": "completed", "records": loaded})
            run.status = PipelineStatus.SUCCESS
        except Exception as exc:
            run.status = PipelineStatus.FAILED; run.error_message = str(exc)
            self.logger.error("Pipeline %s failed: %s", pipeline_id, exc)
        run.finished_at = datetime.now()
        run.metrics = {"duration_seconds": (run.finished_at - run.started_at).total_seconds() if run.started_at else 0,
                       "records_extracted": run.records_extracted, "records_transformed": run.records_transformed,
                       "records_loaded": run.records_loaded}
        with self._lock: self._runs[pipeline_id].append(run)
        self.increment_metric(f"runs_{run.status.value}")
        return run

    def _extract(self, config: PipelineConfig) -> List[Dict[str, Any]]:
        count = config.source.get("sample_count", 100)
        return [{"record_id": i, "source": config.source.get("type", "unknown")} for i in range(count)]

    def _transform(self, config: PipelineConfig, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for t in config.transforms:
            tt = t.get("type", "")
            if tt == "filter": data = FilterTransform(t["column"], t.get("op", "eq"), t.get("value")).execute(data)
            elif tt == "rename": data = RenameTransform(t.get("renames", {})).execute(data)
            elif tt == "aggregate": data = AggregateTransform(t.get("group_keys", []), t.get("aggregations", {})).execute(data)
        return data

    def _load(self, config: PipelineConfig, data: List[Dict[str, Any]]) -> int:
        return len(data)

    def get_pipeline_runs(self, pipeline_id: str) -> List[PipelineRun]:
        return self._runs.get(pipeline_id, [])

    def get_pipeline_health(self) -> Dict[str, Any]:
        all_runs = [r for runs in self._runs.values() for r in runs]
        success = sum(1 for r in all_runs if r.status == PipelineStatus.SUCCESS)
        failed = sum(1 for r in all_runs if r.status == PipelineStatus.FAILED)
        durations = [(r.finished_at - r.started_at).total_seconds() for r in all_runs if r.started_at and r.finished_at]
        return {"total_pipelines": len(self._pipelines), "total_runs": len(all_runs),
                "success_count": success, "failed_count": failed,
                "success_rate": (success / len(all_runs) * 100) if all_runs else 0,
                "avg_duration_seconds": round(sum(durations) / len(durations), 2) if durations else 0}


# ═══════════════════════════════════════════════════════════════════════════
# DataQualityManager
# ═══════════════════════════════════════════════════════════════════════════

class DataQualityManager(ComponentBase):
    def __init__(self):
        super().__init__("DataQualityManager")
        self._checks: Dict[str, List[QualityCheck]] = defaultdict(list)
        self._results: Dict[str, List[QualityResult]] = defaultdict(list)

    def add_check(self, dataset: str, check: QualityCheck) -> QualityCheck:
        self._checks[dataset].append(check)
        self.logger.info("Quality check '%s' added for '%s'", check.name, dataset)
        return check

    def remove_check(self, dataset: str, check_id: str) -> bool:
        before = len(self._checks[dataset])
        self._checks[dataset] = [c for c in self._checks[dataset] if c.check_id != check_id]
        return len(self._checks[dataset]) < before

    def run_checks(self, dataset: str, data: List[Dict[str, Any]]) -> List[QualityResult]:
        results = []
        for check in self._checks.get(dataset, []):
            if not check.enabled: continue
            result = self._evaluate_check(check, data)
            self._results[dataset].append(result)
            results.append(result)
            self.increment_metric("checks_run")
            if not result.passed: self.increment_metric("checks_failed")
        return results

    def _evaluate_check(self, check: QualityCheck, data: List[Dict[str, Any]]) -> QualityResult:
        rule = check.rule.upper()
        if "NOT NULL" in rule:
            failed = sum(1 for row in data if row.get(check.column) is None)
            return QualityResult(check_id=check.check_id, check_name=check.name, passed=failed == 0,
                                 records_checked=len(data), records_failed=failed, severity=check.severity,
                                 message=f"NOT NULL on '{check.column}': {failed} nulls")
        if "UNIQUE" in rule:
            vals = [row.get(check.column) for row in data]
            failed = len(vals) - len(set(vals))
            return QualityResult(check_id=check.check_id, check_name=check.name, passed=failed == 0,
                                 records_checked=len(data), records_failed=failed, severity=check.severity,
                                 message=f"UNIQUE on '{check.column}': {failed} duplicates")
        if "RANGE" in rule:
            parts = rule.replace("RANGE", "").strip().split(",")
            lo, hi = float(parts[0]), float(parts[1])
            vals = [row.get(check.column) for row in data if row.get(check.column) is not None]
            failed = sum(1 for v in vals if not (lo <= float(v) <= hi))
            return QualityResult(check_id=check.check_id, check_name=check.name, passed=failed == 0,
                                 records_checked=len(data), records_failed=failed, severity=check.severity,
                                 message=f"RANGE on '{check.column}': {failed} out of bounds")
        if "REGEX" in rule:
            pattern = rule.replace("REGEX", "").strip()
            vals = [str(row.get(check.column, "")) for row in data]
            failed = sum(1 for v in vals if not re.match(pattern, v))
            return QualityResult(check_id=check.check_id, check_name=check.name, passed=failed == 0,
                                 records_checked=len(data), records_failed=failed, severity=check.severity,
                                 message=f"REGEX on '{check.column}': {failed} non-matching")
        return QualityResult(check_id=check.check_id, check_name=check.name, passed=True,
                             records_checked=len(data), severity=check.severity, message="Unknown rule, skipped")

    def profile_dataset(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not data: return {"total_records": 0, "columns": {}}
        profile: Dict[str, Any] = {"total_records": len(data), "columns": {}}
        for col in list(data[0].keys()):
            values = [row.get(col) for row in data]
            non_null = [v for v in values if v is not None]
            cp: Dict[str, Any] = {"total_count": len(values), "null_count": len(values) - len(non_null),
                                  "null_pct": round((len(values) - len(non_null)) / len(values) * 100, 2),
                                  "distinct_count": len(set(str(v) for v in non_null))}
            if non_null and all(isinstance(v, (int, float)) for v in non_null):
                nums = [float(v) for v in non_null]
                cp.update({"type": "numeric", "min": min(nums), "max": max(nums),
                           "mean": round(sum(nums)/len(nums), 4), "median": sorted(nums)[len(nums)//2]})
            elif non_null and all(isinstance(v, str) for v in non_null):
                cp.update({"type": "string", "min_length": min(len(v) for v in non_null),
                           "max_length": max(len(v) for v in non_null),
                           "avg_length": round(sum(len(v) for v in non_null)/len(non_null), 2)})
            else:
                cp["type"] = "mixed"
            profile["columns"][col] = cp
        return profile

    def compute_quality_score(self, results: List[QualityResult]) -> float:
        if not results: return 100.0
        w = {Severity.INFO: 1, Severity.LOW: 2, Severity.MEDIUM: 5, Severity.HIGH: 10, Severity.CRITICAL: 25}
        tw = sum(w.get(r.severity, 5) for r in results)
        fw = sum(w.get(r.severity, 5) for r in results if not r.passed)
        return round(max(0, 100 - (fw / tw * 100)), 2) if tw else 100.0

    def get_quality_summary(self, dataset: str) -> Dict[str, Any]:
        results = self._results.get(dataset, [])
        score = self.compute_quality_score(results)
        return {"dataset": dataset, "total_checks": len(results), "passed": sum(1 for r in results if r.passed),
                "failed": sum(1 for r in results if not r.passed), "score": score,
                "level": self._score_to_level(score)}

    @staticmethod
    def _score_to_level(score: float) -> str:
        if score >= 95: return DataQualityLevel.EXCELLENT.value
        if score >= 85: return DataQualityLevel.GOOD.value
        if score >= 70: return DataQualityLevel.FAIR.value
        if score >= 50: return DataQualityLevel.POOR.value
        return DataQualityLevel.CRITICAL.value


# ═══════════════════════════════════════════════════════════════════════════
# ETLOrchestrator
# ═══════════════════════════════════════════════════════════════════════════

class ETLOrchestrator(ComponentBase):
    def __init__(self):
        super().__init__("ETLOrchestrator")
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._dag: Dict[str, List[str]] = {}
        self._job_runs: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def register_job(self, job_name: str, schedule: str, dependencies: Optional[List[str]] = None,
                     timeout: int = 3600, retry_count: int = 3) -> Dict[str, Any]:
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        job = {"job_id": job_id, "job_name": job_name, "schedule": schedule,
               "dependencies": dependencies or [], "timeout": timeout, "retry_count": retry_count,
               "status": "scheduled", "created_at": datetime.now().isoformat()}
        self._jobs[job_id] = job; self._dag[job_id] = dependencies or []
        self.logger.info("Job '%s' registered (id=%s)", job_name, job_id)
        return job

    def resolve_dependencies(self, job_id: str) -> List[str]:
        visited: Set[str] = set(); order: List[str] = []
        self._topo_sort(job_id, visited, order); return order

    def _topo_sort(self, job_id: str, visited: Set[str], order: List[str]):
        if job_id in visited: return
        visited.add(job_id)
        for dep in self._dag.get(job_id, []): self._topo_sort(dep, visited, order)
        order.append(job_id)

    def execute_job(self, job_id: str) -> Dict[str, Any]:
        job = self._jobs.get(job_id)
        if not job: raise ValueError(f"Job {job_id} not found")
        start = datetime.now()
        run_record = {"run_id": f"jrun_{uuid.uuid4().hex[:8]}", "job_id": job_id,
                      "status": "running", "started_at": start.isoformat(), "steps": []}
        for dep_id in self.resolve_dependencies(job_id):
            ss = datetime.now(); step = {"job_id": dep_id, "status": "success", "duration_seconds": 0}
            try: time.sleep(0.001)
            except Exception as exc:
                step["status"] = "failed"; step["error"] = str(exc); run_record["status"] = "failed"
            step["duration_seconds"] = (datetime.now() - ss).total_seconds()
            run_record["steps"].append(step)
        if run_record["status"] != "failed": run_record["status"] = "success"
        run_record["finished_at"] = datetime.now().isoformat()
        run_record["total_duration"] = (datetime.now() - start).total_seconds()
        self._job_runs[job_id].append(run_record)
        self.increment_metric(f"job_runs_{run_record['status']}")
        return run_record

    def get_dag_visualization(self) -> str:
        lines = ["DAG Visualization:"]
        for jid, deps in self._dag.items():
            name = self._jobs.get(jid, {}).get("job_name", jid)
            if deps:
                lines.append(f"  {name} <- {', '.join(self._jobs.get(d, {}).get('job_name', d) for d in deps)}")
            else: lines.append(f"  {name} (root)")
        return "\n".join(lines)

    def monitor_jobs(self) -> Dict[str, Any]:
        all_runs = [r for runs in self._job_runs.values() for r in runs]
        success = sum(1 for r in all_runs if r["status"] == "success")
        failed = sum(1 for r in all_runs if r["status"] == "failed")
        return {"total_jobs": len(self._jobs), "total_runs": len(all_runs), "success": success,
                "failed": failed, "success_rate": round(success/len(all_runs)*100, 2) if all_runs else 0,
                "dag": self.get_dag_visualization()}


# ═══════════════════════════════════════════════════════════════════════════
# DataWarehouseManager
# ═══════════════════════════════════════════════════════════════════════════

class DataWarehouseManager(ComponentBase):
    def __init__(self):
        super().__init__("DataWarehouseManager")
        self._tables: Dict[str, Dict[str, Any]] = {}
        self._schemas: Dict[str, SchemaDefinition] = {}

    def create_table(self, name: str, layer: WarehouseLayer, schema: SchemaDefinition,
                     partition_keys: Optional[List[str]] = None,
                     storage_format: StorageFormat = StorageFormat.PARQUET) -> Dict[str, Any]:
        tid = f"tbl_{uuid.uuid4().hex[:8]}"
        table = {"table_id": tid, "name": name, "layer": layer.value, "schema_id": schema.schema_id,
                 "partition_keys": partition_keys or [], "storage_format": storage_format.value,
                 "row_count": 0, "size_bytes": 0, "created_at": datetime.now().isoformat()}
        self._tables[tid] = table; self._schemas[schema.schema_id] = schema
        self.logger.info("Table '%s' created in layer '%s'", name, layer.value)
        return table

    def drop_table(self, table_id: str) -> bool:
        if table_id in self._tables: del self._tables[table_id]; return True
        return False

    def list_tables(self, layer: Optional[WarehouseLayer] = None) -> List[Dict[str, Any]]:
        tables = list(self._tables.values())
        if layer: tables = [t for t in tables if t["layer"] == layer.value]
        return tables

    def get_storage_stats(self) -> Dict[str, Any]:
        by_layer: Dict[str, int] = defaultdict(int)
        total_size = 0
        for t in self._tables.values(): by_layer[t["layer"]] += 1; total_size += t["size_bytes"]
        return {"total_tables": len(self._tables), "by_layer": dict(by_layer),
                "total_size_bytes": total_size, "total_size_gb": round(total_size / (1024**3), 2)}

    def optimize_table(self, table_id: str) -> Dict[str, Any]:
        table = self._tables.get(table_id)
        if not table: raise ValueError(f"Table {table_id} not found")
        table["row_count"] = max(table["row_count"], 1000); table["size_bytes"] = table["row_count"] * 256
        return {"table_id": table_id, "optimizations": ["compacted", "statistics updated", "metadata refreshed"]}

    def generate_ddl(self, table_id: str) -> str:
        table = self._tables.get(table_id)
        if not table: raise ValueError(f"Table {table_id} not found")
        schema = self._schemas.get(table["schema_id"])
        col_defs = []
        if schema:
            for col in schema.columns:
                parts = [f"  {col.name} {col.data_type}"]
                if not col.nullable: parts.append("NOT NULL")
                if col.primary_key: parts.append("PRIMARY KEY")
                col_defs.append(" ".join(parts))
        cols_str = ",\n".join(col_defs) if col_defs else "  id INT PRIMARY KEY"
        part_str = f"\nPARTITIONED BY ({', '.join(table['partition_keys'])})" if table["partition_keys"] else ""
        return f"CREATE TABLE IF NOT EXISTS {table['name']} (\n{cols_str}\n){part_str}\nSTORED AS {table['storage_format'].upper()};"


# ═══════════════════════════════════════════════════════════════════════════
# DataLineageTracker
# ═══════════════════════════════════════════════════════════════════════════

class DataLineageTracker(ComponentBase):
    def __init__(self):
        super().__init__("DataLineageTracker")
        self._nodes: Dict[str, LineageNode] = {}
        self._edges: List[Tuple[str, str]] = []

    def register_node(self, node: LineageNode) -> LineageNode:
        self._nodes[node.node_id] = node; return node

    def add_edge(self, upstream_id: str, downstream_id: str) -> bool:
        if upstream_id not in self._nodes or downstream_id not in self._nodes: return False
        self._nodes[upstream_id].downstream.append(downstream_id)
        self._nodes[downstream_id].upstream.append(upstream_id)
        self._edges.append((upstream_id, downstream_id)); return True

    def get_upstream(self, node_id: str, max_depth: int = 10) -> List[LineageNode]:
        visited: Set[str] = set(); result: List[LineageNode] = []
        self._traverse(node_id, 0, max_depth, visited, result, "up"); return result

    def get_downstream(self, node_id: str, max_depth: int = 10) -> List[LineageNode]:
        visited: Set[str] = set(); result: List[LineageNode] = []
        self._traverse(node_id, 0, max_depth, visited, result, "down"); return result

    def _traverse(self, nid: str, depth: int, max_depth: int, visited: Set[str],
                  result: List[LineageNode], direction: str):
        if depth >= max_depth or nid in visited: return
        visited.add(nid); node = self._nodes.get(nid)
        if not node: return
        related = node.upstream if direction == "up" else node.downstream
        for rid in related:
            rnode = self._nodes.get(rid)
            if rnode:
                result.append(rnode)
                self._traverse(rid, depth + 1, max_depth, visited, result, direction)

    def get_impact_analysis(self, node_id: str) -> Dict[str, Any]:
        ds = self.get_downstream(node_id)
        return {"source_node": node_id, "affected_nodes": len(ds),
                "affected_names": [n.name for n in ds],
                "recommendation": "Review all downstream consumers before modifying"}

    def visualize(self) -> str:
        lines = ["Lineage Graph:"]
        for node in self._nodes.values():
            up = [self._nodes[u].name for u in node.upstream if u in self._nodes]
            down = [self._nodes[d].name for d in node.downstream if d in self._nodes]
            lines.append(f"  [{node.name}]")
            if up: lines.append(f"    <- {', '.join(up)}")
            if down: lines.append(f"    -> {', '.join(down)}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# StreamingManager
# ═══════════════════════════════════════════════════════════════════════════

class StreamingManager(ComponentBase):
    def __init__(self):
        super().__init__("StreamingManager")
        self._topics: Dict[str, StreamingTopic] = {}
        self._consumers: Dict[str, Dict[str, Any]] = {}
        self._buffers: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def create_topic(self, name: str, partitions: int = 6,
                     replication_factor: int = 3, retention_hours: int = 168) -> StreamingTopic:
        topic = StreamingTopic(name=name, partitions=partitions,
                               replication_factor=replication_factor, retention_hours=retention_hours)
        self._topics[topic.topic_id] = topic
        self.logger.info("Topic '%s' created (id=%s)", name, topic.topic_id)
        return topic

    def produce(self, topic_id: str, key: str, value: Dict[str, Any]) -> bool:
        if topic_id not in self._topics: return False
        partition = hash(key) % self._topics[topic_id].partitions
        self._buffers[topic_id].append({"key": key, "value": value, "partition": partition,
                                         "timestamp": datetime.now().isoformat(),
                                         "offset": len(self._buffers[topic_id])})
        self.increment_metric("messages_produced"); return True

    def consume(self, topic_id: str, consumer_id: str, max_messages: int = 10) -> List[Dict[str, Any]]:
        if topic_id not in self._topics: return []
        buf = self._buffers[topic_id]; consumed = buf[:max_messages]
        self._buffers[topic_id] = buf[max_messages:]
        self.increment_metric("messages_consumed", len(consumed)); return consumed

    def register_consumer(self, topic_id: str, consumer_group: str) -> Dict[str, Any]:
        cid = f"cons_{uuid.uuid4().hex[:8]}"
        self._consumers[cid] = {"consumer_id": cid, "topic_id": topic_id,
                                 "consumer_group": consumer_group, "status": "active"}
        return self._consumers[cid]

    def get_topic_stats(self) -> Dict[str, Any]:
        return {t.name: {"partitions": t.partitions, "replication_factor": t.replication_factor,
                         "buffer_size": len(self._buffers.get(t.topic_id, [])),
                         "retention_hours": t.retention_hours} for t in self._topics.values()}


# ═══════════════════════════════════════════════════════════════════════════
# SchemaRegistry
# ═══════════════════════════════════════════════════════════════════════════

class SchemaRegistry(ComponentBase):
    def __init__(self):
        super().__init__("SchemaRegistry")
        self._schemas: Dict[str, List[SchemaDefinition]] = defaultdict(list)
        self._compatibility: Dict[str, SchemaEvolutionStrategy] = {}

    def register_schema(self, schema: SchemaDefinition) -> SchemaDefinition:
        existing = self._schemas.get(schema.name, [])
        if existing: schema.version = max(s.version for s in existing) + 1
        self._schemas[schema.name].append(schema)
        self._compatibility[schema.name] = schema.compatibility
        self.logger.info("Schema '%s' v%d registered", schema.name, schema.version)
        return schema

    def get_schema(self, name: str, version: Optional[int] = None) -> Optional[SchemaDefinition]:
        versions = self._schemas.get(name, [])
        if not versions: return None
        if version is not None: return next((s for s in versions if s.version == version), None)
        return max(versions, key=lambda s: s.version)

    def list_schemas(self) -> List[Dict[str, Any]]:
        return [{"name": n, "latest_version": max(s.version for s in v), "total_versions": len(v),
                 "columns": len(max(v, key=lambda s: s.version).columns)}
                for n, v in self._schemas.items()]

    def check_compatibility(self, name: str, new_schema: SchemaDefinition) -> Dict[str, Any]:
        existing = self.get_schema(name)
        if not existing: return {"compatible": True, "message": "No existing schema"}
        existing_cols = {c.name: c for c in existing.columns}
        strategy = self._compatibility.get(name, SchemaEvolutionStrategy.ADD_COLUMNS)
        issues = []
        for cn, nc in {c.name: c for c in new_schema.columns}.items():
            if cn not in existing_cols and strategy == SchemaEvolutionStrategy.FAIL:
                issues.append(f"New column '{cn}' not allowed under FAIL")
            elif cn in existing_cols and existing_cols[cn].data_type != nc.data_type:
                if strategy == SchemaEvolutionStrategy.FAIL:
                    issues.append(f"Type change on '{cn}'")
        return {"compatible": len(issues) == 0, "issues": issues, "strategy": strategy.value}


# ═══════════════════════════════════════════════════════════════════════════
# DataCatalog
# ═══════════════════════════════════════════════════════════════════════════

class DataCatalog(ComponentBase):
    def __init__(self):
        super().__init__("DataCatalog")
        self._entries: Dict[str, CatalogEntry] = {}
        self._tags_index: Dict[str, Set[str]] = defaultdict(set)
        self._owner_index: Dict[str, Set[str]] = defaultdict(set)

    def add_entry(self, entry: CatalogEntry) -> CatalogEntry:
        self._entries[entry.entry_id] = entry
        for tag in entry.tags: self._tags_index[tag].add(entry.entry_id)
        if entry.owner: self._owner_index[entry.owner].add(entry.entry_id)
        return entry

    def get_entry(self, entry_id: str) -> Optional[CatalogEntry]:
        return self._entries.get(entry_id)

    def search(self, query: str, entry_type: Optional[CatalogEntryType] = None) -> List[CatalogEntry]:
        q = query.lower()
        return [e for e in self._entries.values()
                if (entry_type is None or e.entry_type == entry_type)
                and (q in e.name.lower() or q in e.description.lower() or q in " ".join(e.tags).lower())]

    def get_entries_by_tag(self, tag: str) -> List[CatalogEntry]:
        return [self._entries[eid] for eid in self._tags_index.get(tag, set()) if eid in self._entries]

    def get_entries_by_owner(self, owner: str) -> List[CatalogEntry]:
        return [self._entries[eid] for eid in self._owner_index.get(owner, set()) if eid in self._entries]

    def get_catalog_stats(self) -> Dict[str, Any]:
        by_type: Dict[str, int] = defaultdict(int)
        for e in self._entries.values(): by_type[e.entry_type.value] += 1
        return {"total_entries": len(self._entries), "by_type": dict(by_type),
                "unique_tags": len(self._tags_index), "unique_owners": len(self._owner_index)}


# ═══════════════════════════════════════════════════════════════════════════
# InfrastructureAsCodeManager
# ═══════════════════════════════════════════════════════════════════════════

class InfrastructureAsCodeManager(ComponentBase):
    def __init__(self):
        super().__init__("InfrastructureAsCodeManager")
        self._resources: Dict[str, IaCResource] = {}
        self._deployments: List[Dict[str, Any]] = []

    def define_resource(self, name: str, resource_type: str, template_type: IaCTemplateType,
                        config: Dict[str, Any], dependencies: Optional[List[str]] = None) -> IaCResource:
        r = IaCResource(name=name, resource_type=resource_type, template_type=template_type,
                        config=config, dependencies=dependencies or [])
        self._resources[r.resource_id] = r; return r

    def generate_template(self, resource_id: str) -> str:
        r = self._resources.get(resource_id)
        if not r: raise ValueError(f"Resource {resource_id} not found")
        if r.template_type == IaCTemplateType.TERRAFORM: return self._gen_tf(r)
        if r.template_type == IaCTemplateType.CLOUDFORMATION: return self._gen_cfn(r)
        return f"# Template for {r.name} ({r.template_type.value})"

    @staticmethod
    def _gen_tf(r: IaCResource) -> str:
        lines = [f'resource "{r.resource_type}" "{r.name}" {{']
        for k, v in r.config.items():
            if isinstance(v, str): lines.append(f'  {k} = "{v}"')
            elif isinstance(v, bool): lines.append(f'  {k} = {"true" if v else "false"}')
            elif isinstance(v, (int, float)): lines.append(f'  {k} = {v}')
            elif isinstance(v, list): lines.append(f'  {k} = {json.dumps(v)}')
        lines.append("}"); return "\n".join(lines)

    @staticmethod
    def _gen_cfn(r: IaCResource) -> str:
        return json.dumps({"AWSTemplateFormatVersion": "2010-09-09",
                           "Resources": {r.name: {"Type": r.resource_type, "Properties": r.config}}}, indent=2)

    def plan_deployment(self, resource_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        targets = resource_ids or list(self._resources.keys())
        plan = {"resources_to_add": 0, "steps": []}
        for rid in targets:
            r = self._resources.get(rid)
            if r: plan["resources_to_add"] += 1; plan["steps"].append(
                {"resource": r.name, "action": "create", "type": r.resource_type, "depends_on": r.dependencies})
        return plan

    def deploy(self, resource_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        plan = self.plan_deployment(resource_ids)
        d = {"deployment_id": f"deploy_{uuid.uuid4().hex[:8]}", "plan": plan, "status": "completed"}
        self._deployments.append(d); self.increment_metric("deployments"); return d


# ═══════════════════════════════════════════════════════════════════════════
# MonitoringManager
# ═══════════════════════════════════════════════════════════════════════════

class MonitoringManager(ComponentBase):
    def __init__(self):
        super().__init__("MonitoringManager")
        self._alert_rules: Dict[str, AlertRule] = {}
        self._fired_alerts: List[Dict[str, Any]] = []
        self._metrics_store: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)

    def add_alert_rule(self, rule: AlertRule) -> AlertRule:
        self._alert_rules[rule.alert_id] = rule; return rule

    def record_metric(self, metric_name: str, value: float):
        self._metrics_store[metric_name].append((datetime.now(), value))
        self._evaluate_alerts(metric_name, value)

    def _evaluate_alerts(self, metric_name: str, value: float):
        for rule in self._alert_rules.values():
            if rule.metric != metric_name or not rule.enabled: continue
            triggered = ((rule.operator == "gt" and value > rule.threshold) or
                         (rule.operator == "lt" and value < rule.threshold) or
                         (rule.operator == "eq" and value == rule.threshold))
            if triggered:
                self._fired_alerts.append({"alert_id": rule.alert_id, "name": rule.name,
                                           "metric": metric_name, "value": value,
                                           "severity": rule.severity.value, "channels": rule.channels,
                                           "fired_at": datetime.now().isoformat()})
                self.logger.warning("Alert '%s' fired: %s=%f", rule.name, metric_name, value)

    def get_metric_history(self, metric_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        return [{"timestamp": ts.isoformat(), "value": val}
                for ts, val in self._metrics_store.get(metric_name, [])[-limit:]]

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        return self._fired_alerts[-50:]

    def get_monitoring_summary(self) -> Dict[str, Any]:
        return {"total_rules": len(self._alert_rules), "total_metrics_tracked": len(self._metrics_store),
                "total_alerts_fired": len(self._fired_alerts), "recent_alerts": self._fired_alerts[-5:]}


# ═══════════════════════════════════════════════════════════════════════════
# DataEngineeringAgent — Top-level Orchestrator
# ═══════════════════════════════════════════════════════════════════════════

class DataEngineeringAgent:
    def __init__(self):
        self.pipeline_manager = PipelineManager()
        self.quality_manager = DataQualityManager()
        self.etl_orchestrator = ETLOrchestrator()
        self.warehouse_manager = DataWarehouseManager()
        self.lineage_tracker = DataLineageTracker()
        self.streaming_manager = StreamingManager()
        self.schema_registry = SchemaRegistry()
        self.data_catalog = DataCatalog()
        self.iac_manager = InfrastructureAsCodeManager()
        self.monitoring = MonitoringManager()
        self.logger = logging.getLogger("data_engineering.agent")
        self._components = [self.pipeline_manager, self.quality_manager, self.etl_orchestrator,
                            self.warehouse_manager, self.lineage_tracker, self.streaming_manager,
                            self.schema_registry, self.data_catalog, self.iac_manager, self.monitoring]
        for comp in self._components: comp.start()
        self.logger.info("DataEngineeringAgent initialized with %d components", len(self._components))

    def create_full_pipeline(self, name: str, source: Dict[str, Any], transforms: List[Dict[str, Any]],
                             sink: Dict[str, Any], pipeline_type: PipelineType = PipelineType.ETL) -> PipelineConfig:
        config = self.pipeline_manager.create_pipeline(name, source, transforms, sink, pipeline_type)
        self.lineage_tracker.register_node(LineageNode(
            node_id=config.pipeline_id, name=name, node_type="pipeline", metadata={"type": pipeline_type.value}))
        self.data_catalog.add_entry(CatalogEntry(
            name=name, entry_type=CatalogEntryType.PIPELINE,
            description=f"{pipeline_type.value} pipeline: {name}", tags=[pipeline_type.value, "auto-created"]))
        return config

    def run_quality_assessment(self, dataset: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = self.quality_manager.run_checks(dataset, data)
        score = self.quality_manager.compute_quality_score(results)
        self.monitoring.record_metric(f"quality.{dataset}", score)
        return {"dataset": dataset, "score": score,
                "level": DataQualityManager._score_to_level(score),
                "results": [{"check": r.check_name, "passed": r.passed, "message": r.message} for r in results]}

    def get_system_status(self) -> Dict[str, Any]:
        return {"agent": "DataEngineeringAgent", "version": "2.0.0",
                "components": {c.name: c.get_metrics() for c in self._components},
                "pipeline_health": self.pipeline_manager.get_pipeline_health(),
                "warehouse_stats": self.warehouse_manager.get_storage_stats(),
                "catalog_stats": self.data_catalog.get_catalog_stats(),
                "schema_count": len(self.schema_registry.list_schemas()),
                "streaming_topics": len(self.streaming_manager._topics),
                "monitoring": self.monitoring.get_monitoring_summary()}

    def shutdown(self):
        for comp in self._components: comp.stop()
        self.logger.info("DataEngineeringAgent shutdown complete")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    agent = DataEngineeringAgent()
    pipeline = agent.create_full_pipeline(
        name="user_analytics_etl",
        source={"type": "postgres", "connection": "prod_db", "query": "SELECT * FROM users"},
        transforms=[
            {"type": "filter", "column": "status", "op": "eq", "value": "active"},
            {"type": "rename", "renames": {"user_id": "id", "created_at": "ts"}},
        ],
        sink={"type": "bigquery", "table": "analytics.users_active"},
        pipeline_type=PipelineType.ETL,
    )
    print(f"Pipeline created: {pipeline.pipeline_id}")
    run = agent.pipeline_manager.execute_pipeline(pipeline.pipeline_id)
    print(f"Run status: {run.status.value}, records: {run.records_loaded}")
    agent.quality_manager.add_check("user_data", QualityCheck(name="email_nn", column="email", rule="NOT NULL", severity=Severity.HIGH))
    agent.quality_manager.add_check("user_data", QualityCheck(name="age_range", column="age", rule="RANGE 0,120", severity=Severity.MEDIUM))
    sample_data = [{"email": "a@test.com", "age": 25}, {"email": "b@test.com", "age": 30}, {"email": None, "age": 150}]
    qa = agent.run_quality_assessment("user_data", sample_data)
    print(f"Quality score: {qa['score']}, level: {qa['level']}")
    topic = agent.streaming_manager.create_topic("events", partitions=3)
    agent.streaming_manager.produce(topic.topic_id, "evt_1", {"type": "click", "page": "/home"})
    msgs = agent.streaming_manager.consume(topic.topic_id, "consumer", max_messages=5)
    print(f"Consumed {len(msgs)} messages")
    status = agent.get_system_status()
    print(f"\nSystem status: {json.dumps(status, indent=2, default=str)[:500]}")
    agent.shutdown()
