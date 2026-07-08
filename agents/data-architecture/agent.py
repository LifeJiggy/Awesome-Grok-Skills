"""Data Architecture Agent - Data Architecture Design and Management Platform.

Comprehensive framework for data architecture including data modeling,
data integration, master data management, data mesh, data fabric,
and data governance.

Features:
- Data model design and management (logical, physical, conceptual)
- Data integration pipeline configuration
- Master Data Management (MDM)
- Data mesh domain management
- Data fabric connectivity
- Data catalog and discovery
- Data quality monitoring
- Schema management and evolution
- Data lineage tracking (table-level and column-level)
- Metadata management
- Data governance policies
- Schema registry with compatibility checks
- Data partitioning strategies
- Data masking and anonymization
- Dependency graph analysis
- Data retention management
- Cost tracking and optimization
- Data migration planning
"""

import hashlib
import json
import logging
import random
import statistics
import threading
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("data_architecture_agent")

# =============================================================================
# ENUMS
# =============================================================================

class ModelType(Enum):
    CONCEPTUAL = auto()
    LOGICAL = auto()
    PHYSICAL = auto()
    SEMANTIC = auto()

class DataType(Enum):
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    DATE = auto()
    DATETIME = auto()
    TIMESTAMP = auto()
    BINARY = auto()
    JSON = auto()
    ARRAY = auto()
    MAP = auto()
    DECIMAL = auto()
    UUID = auto()
    ENUM = auto()
    TEXT = auto()
    BLOB = auto()

class IntegrationPattern(Enum):
    ETL = auto()
    ELT = auto()
    CDC = auto()
    API_SYNC = auto()
    FILE_TRANSFER = auto()
    STREAMING = auto()
    EVENT_DRIVEN = auto()
    BATCH = auto()

class StorageType(Enum):
    RELATIONAL_DB = auto()
    DOCUMENT_DB = auto()
    KEY_VALUE_STORE = auto()
    COLUMN_FAMILY = auto()
    GRAPH_DB = auto()
    TIME_SERIES = auto()
    OBJECT_STORAGE = auto()
    DATA_LAKE = auto()
    DATA_WAREHOUSE = auto()
    CACHE = auto()

class DataDomain(Enum):
    CUSTOMER = auto()
    PRODUCT = auto()
    ORDER = auto()
    FINANCE = auto()
    INVENTORY = auto()
    ANALYTICS = auto()
    MARKETING = auto()
    HR = auto()
    SUPPLY_CHAIN = auto()
    CUSTOM = auto()

class QualityRuleType(Enum):
    NOT_NULL = auto()
    UNIQUE = auto()
    RANGE_CHECK = auto()
    PATTERN_MATCH = auto()
    REFERENTIAL_INTEGRITY = auto()
    FRESHNESS = auto()
    COMPLETENESS = auto()
    CONSISTENCY = auto()
    ACCURACY = auto()
    CUSTOM = auto()

class GovernancePolicy(Enum):
    DATA_CLASSIFICATION = auto()
    ACCESS_CONTROL = auto()
    RETENTION = auto()
    ENCRYPTION = auto()
    MASKING = auto()
    AUDIT_LOGGING = auto()
    COMPLIANCE = auto()
    QUALITY_STANDARD = auto()

class SchemaEvolution(Enum):
    ADD_COLUMN = auto()
    DROP_COLUMN = auto()
    RENAME_COLUMN = auto()
    CHANGE_TYPE = auto()
    ADD_TABLE = auto()
    DROP_TABLE = auto()
    ADD_INDEX = auto()
    DROP_INDEX = auto()

class LineageNodeType(Enum):
    SOURCE = auto()
    TRANSFORMATION = auto()
    DESTINATION = auto()
    QUALITY_CHECK = auto()
    AGGREGATION = auto()
    FILTER = auto()
    JOIN = auto()
    LOOKUP = auto()

class PartitionStrategy(Enum):
    NONE = auto()
    HASH = auto()
    RANGE = auto()
    LIST = auto()
    TIME_INTERVAL = auto()
    GEOGRAPHIC = auto()
    DIRECTORY = auto()

class MaskingType(Enum):
    FULL_REDACT = auto()
    PARTIAL = auto()
    HASH = auto()
    TOKENIZE = auto()
    SHUFFLE = auto()
    DATE_SHIFT = auto()
    NULL_OUT = auto()
    FORMAT_PRESERVING = auto()

class RetentionAction(Enum):
    DELETE = auto()
    ARCHIVE = auto()
    COMPRESS = auto()
    MOVE_TO_COLD = auto()
    KEEP_FOREVER = auto()
    ANONYMIZE = auto()

class MigrationStatus(Enum):
    PLANNED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    ROLLED_BACK = auto()
    PAUSED = auto()

class CostCategory(Enum):
    COMPUTE = auto()
    STORAGE = auto()
    NETWORK = auto()
    QUERY = auto()
    BACKUP = auto()
    LICENSE = auto()
    TRANSFORMATION = auto()
    MONITORING = auto()

class SchemaCompatibility(Enum):
    BACKWARD = auto()
    FORWARD = auto()
    FULL = auto()
    NONE = auto()

class DependencyType(Enum):
    TABLE_DEPENDS_ON = auto()
    PIPELINE_FEEDS = auto()
    QUALITY_RULE_CHECKS = auto()
    GOVERNANCE_POLICY_APPLIES = auto()
    SCHEMA_OWNED_BY = auto()
    DOMAIN_CONTAINS = auto()

# =============================================================================
# CONSTANTS
# =============================================================================

DATA_TYPE_SIZES: Dict[DataType, int] = {
    DataType.STRING: 256, DataType.INTEGER: 4, DataType.FLOAT: 8,
    DataType.BOOLEAN: 1, DataType.DATE: 4, DataType.DATETIME: 8,
    DataType.TIMESTAMP: 8, DataType.BINARY: 1024, DataType.JSON: 4096,
    DataType.ARRAY: 1024, DataType.MAP: 2048, DataType.DECIMAL: 16,
    DataType.UUID: 16, DataType.ENUM: 4, DataType.TEXT: 65536, DataType.BLOB: 1048576,
}

QUALITY_THRESHOLDS: Dict[QualityRuleType, float] = {
    QualityRuleType.NOT_NULL: 100.0,
    QualityRuleType.UNIQUE: 100.0,
    QualityRuleType.RANGE_CHECK: 99.0,
    QualityRuleType.PATTERN_MATCH: 99.5,
    QualityRuleType.REFERENTIAL_INTEGRITY: 100.0,
    QualityRuleType.FRESHNESS: 99.0,
    QualityRuleType.COMPLETENESS: 95.0,
    QualityRuleType.CONSISTENCY: 98.0,
    QualityRuleType.ACCURACY: 99.0,
}

MAX_LINEAGE_DEPTH = 20
MAX_CATALOG_SEARCH_RESULTS = 100
MAX_AUDIT_LOG_ENTRIES = 10000
DEFAULT_PARTITION_COUNT = 16

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DataField:
    field_id: str
    name: str
    data_type: DataType
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[str] = None
    default_value: Any = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    max_length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    masking_type: Optional[MaskingType] = None
    pii_flag: bool = False
    classification: str = "unclassified"

@dataclass
class DataTable:
    table_id: str
    name: str
    schema_name: str = "default"
    fields: List[DataField] = field(default_factory=list)
    description: str = ""
    storage_type: StorageType = StorageType.RELATIONAL_DB
    domain: DataDomain = DataDomain.CUSTOM
    row_count: int = 0
    size_bytes: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    owner: str = ""
    tags: List[str] = field(default_factory=list)
    partition_config: Optional["PartitionConfig"] = None
    retention_days: Optional[int] = None
    is_view: bool = False
    parent_table: Optional[str] = None

@dataclass
class DataModel:
    model_id: str
    name: str
    model_type: ModelType
    description: str = ""
    tables: List[DataTable] = field(default_factory=list)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    owner: str = ""
    tags: List[str] = field(default_factory=list)
    compatibility: SchemaCompatibility = SchemaCompatibility.BACKWARD

@dataclass
class IntegrationPipeline:
    pipeline_id: str
    name: str
    source: str
    destination: str
    pattern: IntegrationPattern
    schedule: str = ""
    is_active: bool = True
    last_run: Optional[datetime] = None
    last_status: str = "pending"
    records_processed: int = 0
    error_count: int = 0
    avg_duration_seconds: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    config: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 3
    timeout_seconds: int = 3600
    alert_on_failure: bool = True
    tags: List[str] = field(default_factory=list)

@dataclass
class MasterDataRecord:
    record_id: str
    entity_type: str
    golden_id: str
    source_ids: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0
    last_merged: datetime = field(default_factory=datetime.now)
    is_golden: bool = True
    quality_score: float = 1.0
    last_validated: Optional[datetime] = None
    lineage: List[str] = field(default_factory=list)

@dataclass
class DataDomain_:
    domain_id: str
    name: str
    description: str = ""
    owner: str = ""
    data_products: List[str] = field(default_factory=list)
    schemas: List[str] = field(default_factory=list)
    access_policies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    sla_targets: Dict[str, float] = field(default_factory=dict)
    status: str = "active"

@dataclass
class DataProduct:
    product_id: str
    name: str
    domain_id: str
    description: str = ""
    owner: str = ""
    schemas: List[str] = field(default_factory=list)
    endpoints: List[Dict[str, Any]] = field(default_factory=list)
    quality_sla: Dict[str, float] = field(default_factory=dict)
    is_public: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    upstream_products: List[str] = field(default_factory=list)
    downstream_products: List[str] = field(default_factory=list)

@dataclass
class QualityRule:
    rule_id: str
    name: str
    rule_type: QualityRuleType
    table_id: str
    field_id: Optional[str] = None
    threshold: float = 99.0
    expression: str = ""
    is_active: bool = True
    last_checked: Optional[datetime] = None
    last_result: Optional[bool] = None
    last_value: float = 0.0
    owner: str = ""
    severity: str = "warning"
    alert_channels: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class QualityCheckResult:
    check_id: str
    rule_id: str
    table_id: str
    passed: bool
    actual_value: float
    expected_threshold: float
    timestamp: datetime = field(default_factory=datetime.now)
    details: str = ""
    duration_ms: float = 0.0
    records_scanned: int = 0
    violations_found: int = 0

@dataclass
class LineageNode:
    node_id: str
    name: str
    node_type: LineageNodeType
    source_table: Optional[str] = None
    target_table: Optional[str] = None
    transformation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    is_active: bool = True

@dataclass
class LineageEdge:
    edge_id: str
    source_node: str
    target_node: str
    edge_type: str = "data_flow"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    weight: float = 1.0

@dataclass
class SchemaChange:
    change_id: str
    table_id: str
    change_type: SchemaEvolution
    details: Dict[str, Any] = field(default_factory=dict)
    applied_at: datetime = field(default_factory=datetime.now)
    applied_by: str = ""
    rollback_sql: str = ""
    status: str = "applied"
    breaking_change: bool = False

@dataclass
class GovernanceRule:
    rule_id: str
    name: str
    policy_type: GovernancePolicy
    description: str = ""
    scope: str = ""
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    enforcement_level: str = "advisory"
    exceptions: List[str] = field(default_factory=list)
    last_audit: Optional[datetime] = None

@dataclass
class MetadataEntry:
    entry_id: str
    entity_type: str
    entity_id: str
    key: str
    value: Any = None
    source: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0
    tags: List[str] = field(default_factory=list)

@dataclass
class PartitionConfig:
    config_id: str
    table_id: str
    strategy: PartitionStrategy
    column_name: str = ""
    partition_count: int = DEFAULT_PARTITION_COUNT
    range_start: Optional[str] = None
    range_end: Optional[str] = None
    interval: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    estimated_partitions: int = 0
    size_per_partition_bytes: int = 0

@dataclass
class MaskingRule:
    rule_id: str
    name: str
    table_id: str
    field_id: str
    masking_type: MaskingType
    pattern: str = ""
    replacement: str = "***"
    preserve_format: bool = False
    salt: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    description: str = ""

@dataclass
class RetentionRecord:
    record_id: str
    table_id: str
    action: RetentionAction
    retention_days: int = 365
    criteria: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    last_executed: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    affected_rows_last_run: int = 0
    next_scheduled: Optional[datetime] = None

@dataclass
class MigrationPlan:
    plan_id: str
    name: str
    source_system: str
    target_system: str
    tables: List[str] = field(default_factory=list)
    status: MigrationStatus = MigrationStatus.PLANNED
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration_hours: float = 0.0
    actual_duration_hours: float = 0.0
    rows_migrated: int = 0
    rows_total: int = 0
    errors: List[str] = field(default_factory=list)
    rollback_plan: str = ""
    priority: int = 0
    owner: str = ""

@dataclass
class CostEntry:
    entry_id: str
    category: CostCategory
    amount: float
    currency: str = "USD"
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    resource_id: str = ""
    resource_type: str = ""
    tags: List[str] = field(default_factory=list)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None

@dataclass
class ColumnLineage:
    lineage_id: str
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    transformation: str = ""
    confidence: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    description: str = ""

@dataclass
class DependencyNode:
    node_id: str
    entity_type: str
    entity_id: str
    name: str
    dependency_type: DependencyType
    depends_on: List[str] = field(default_factory=list)
    depended_by: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    depth: int = 0

@dataclass
class SchemaVersion:
    version_id: str
    table_id: str
    version_number: int
    schema_snapshot: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    change_description: str = ""
    is_active: bool = True

@dataclass
class DataPartition:
    partition_id: str
    table_id: str
    partition_key: str
    row_count: int = 0
    size_bytes: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: Optional[datetime] = None
    location: str = ""
    is_compressed: bool = False

# =============================================================================
# EXCEPTIONS
# =============================================================================

class DataArchitectureError(Exception):
    pass

class ModelError(DataArchitectureError):
    pass

class IntegrationError(DataArchitectureError):
    pass

class QualityError(DataArchitectureError):
    pass

class GovernanceError(DataArchitectureError):
    pass

class SchemaError(DataArchitectureError):
    pass

class SchemaRegistryError(DataArchitectureError):
    pass

class PartitionError(DataArchitectureError):
    pass

class MaskingError(DataArchitectureError):
    pass

class DependencyError(DataArchitectureError):
    pass

class RetentionError(DataArchitectureError):
    pass

class CostTrackingError(DataArchitectureError):
    pass

class MigrationError(DataArchitectureError):
    pass

class LineageError(DataArchitectureError):
    pass

# =============================================================================
# DATA MODEL MANAGER
# =============================================================================

class DataModelManager:
    def __init__(self):
        self._models: Dict[str, DataModel] = {}
        self._tables: Dict[str, DataTable] = {}
        self._schema_changes: List[SchemaChange] = []
        self._version_history: Dict[str, List[SchemaVersion]] = defaultdict(list)
        self._lock = threading.Lock()

    def create_model(self, model_id: str, name: str, model_type: ModelType,
                     description: str = "", owner: str = "",
                     tags: Optional[List[str]] = None) -> DataModel:
        if model_id in self._models:
            raise ModelError(f"Model {model_id} already exists")
        model = DataModel(
            model_id=model_id, name=name, model_type=model_type,
            description=description, owner=owner, tags=tags or [],
        )
        with self._lock:
            self._models[model_id] = model
        logger.info("Created data model %s: %s (%s)", model_id, name, model_type.name)
        return model

    def update_model(self, model_id: str, **kwargs) -> Optional[DataModel]:
        with self._lock:
            model = self._models.get(model_id)
            if not model:
                return None
            for key, value in kwargs.items():
                if hasattr(model, key):
                    setattr(model, key, value)
            model.updated_at = datetime.now()
            model.version += 1
        return model

    def delete_model(self, model_id: str) -> bool:
        with self._lock:
            if model_id in self._models:
                del self._models[model_id]
                return True
        return False

    def add_table(self, model_id: str, table: DataTable) -> bool:
        with self._lock:
            model = self._models.get(model_id)
            if model:
                model.tables.append(table)
                self._tables[table.table_id] = table
                return True
        return False

    def create_table(self, table_id: str, name: str, schema_name: str = "default",
                     fields: Optional[List[DataField]] = None,
                     storage_type: StorageType = StorageType.RELATIONAL_DB,
                     domain: DataDomain = DataDomain.CUSTOM,
                     owner: str = "", tags: Optional[List[str]] = None) -> DataTable:
        if table_id in self._tables:
            raise ModelError(f"Table {table_id} already exists")
        table = DataTable(
            table_id=table_id, name=name, schema_name=schema_name,
            fields=fields or [], storage_type=storage_type, domain=domain,
            owner=owner, tags=tags or [],
        )
        with self._lock:
            self._tables[table_id] = table
        logger.info("Created table %s: %s", table_id, name)
        return table

    def add_field(self, table_id: str, field: DataField) -> bool:
        with self._lock:
            table = self._tables.get(table_id)
            if table:
                table.fields.append(field)
                table.updated_at = datetime.now()
                return True
        return False

    def remove_field(self, table_id: str, field_id: str) -> bool:
        with self._lock:
            table = self._tables.get(table_id)
            if table:
                original_count = len(table.fields)
                table.fields = [f for f in table.fields if f.field_id != field_id]
                table.updated_at = datetime.now()
                return len(table.fields) < original_count
        return False

    def get_model(self, model_id: str) -> Optional[DataModel]:
        with self._lock:
            return self._models.get(model_id)

    def get_table(self, table_id: str) -> Optional[DataTable]:
        with self._lock:
            return self._tables.get(table_id)

    def get_all_models(self) -> List[DataModel]:
        with self._lock:
            return list(self._models.values())

    def get_all_tables(self) -> List[DataTable]:
        with self._lock:
            return list(self._tables.values())

    def get_tables_by_domain(self, domain: DataDomain) -> List[DataTable]:
        with self._lock:
            return [t for t in self._tables.values() if t.domain == domain]

    def get_tables_by_storage(self, storage_type: StorageType) -> List[DataTable]:
        with self._lock:
            return [t for t in self._tables.values() if t.storage_type == storage_type]

    def search_tables(self, query: str) -> List[DataTable]:
        q = query.lower()
        with self._lock:
            return [t for t in self._tables.values()
                    if q in t.name.lower() or q in t.description.lower()
                    or any(q in tag.lower() for tag in t.tags)]

    def record_schema_change(self, change: SchemaChange) -> None:
        with self._lock:
            self._schema_changes.append(change)

    def get_schema_changes(self, table_id: Optional[str] = None,
                           limit: int = 50) -> List[SchemaChange]:
        with self._lock:
            changes = list(self._schema_changes)
        if table_id:
            changes = [c for c in changes if c.table_id == table_id]
        return changes[-limit:]

    def calculate_table_size(self, table_id: str) -> int:
        table = self._tables.get(table_id)
        if not table:
            return 0
        return sum(DATA_TYPE_SIZES.get(f.data_type, 8) for f in table.fields)

    def get_model_summary(self) -> Dict[str, Any]:
        with self._lock:
            models = list(self._models.values())
            tables = list(self._tables.values())
        total_fields = sum(len(t.fields) for t in tables)
        total_size = sum(self.calculate_table_size(t.table_id) for t in tables)
        pii_count = sum(1 for t in tables for f in t.fields if f.pii_flag)
        return {
            "total_models": len(models),
            "total_tables": len(tables),
            "total_fields": total_fields,
            "total_size_bytes": total_size,
            "pii_fields_count": pii_count,
            "by_domain": {d.name: sum(1 for t in tables if t.domain == d) for d in DataDomain},
            "by_storage": {s.name: sum(1 for t in tables if t.storage_type == s) for s in StorageType},
        }

    def get_pii_fields(self) -> List[Dict[str, Any]]:
        results = []
        with self._lock:
            for table in self._tables.values():
                for f in table.fields:
                    if f.pii_flag:
                        results.append({
                            "table_id": table.table_id,
                            "table_name": table.name,
                            "field_id": f.field_id,
                            "field_name": f.name,
                            "masking_type": f.masking_type.name if f.masking_type else None,
                            "classification": f.classification,
                        })
        return results

    def clone_table(self, source_table_id: str, new_table_id: str, new_name: str) -> Optional[DataTable]:
        with self._lock:
            source = self._tables.get(source_table_id)
            if not source:
                return None
            import copy
            cloned = copy.deepcopy(source)
            cloned.table_id = new_table_id
            cloned.name = new_name
            cloned.created_at = datetime.now()
            cloned.updated_at = datetime.now()
            self._tables[new_table_id] = cloned
        return cloned

# =============================================================================
# INTEGRATION MANAGER
# =============================================================================

class IntegrationManager:
    def __init__(self):
        self._pipelines: Dict[str, IntegrationPipeline] = {}
        self._run_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._alerts: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def create_pipeline(self, pipeline_id: str, name: str, source: str,
                        destination: str, pattern: IntegrationPattern,
                        schedule: str = "", config: Optional[Dict[str, Any]] = None,
                        retry_count: int = 3, timeout_seconds: int = 3600,
                        tags: Optional[List[str]] = None) -> IntegrationPipeline:
        if pipeline_id in self._pipelines:
            raise IntegrationError(f"Pipeline {pipeline_id} already exists")
        pipeline = IntegrationPipeline(
            pipeline_id=pipeline_id, name=name, source=source,
            destination=destination, pattern=pattern, schedule=schedule,
            config=config or {}, retry_count=retry_count,
            timeout_seconds=timeout_seconds, tags=tags or [],
        )
        with self._lock:
            self._pipelines[pipeline_id] = pipeline
        logger.info("Created pipeline %s: %s -> %s (%s)", pipeline_id, source, destination, pattern.name)
        return pipeline

    def run_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        with self._lock:
            pipeline = self._pipelines.get(pipeline_id)
            if not pipeline:
                raise IntegrationError(f"Pipeline {pipeline_id} not found")
        records = random.randint(1000, 100000)
        duration = random.uniform(5, 300)
        success = random.random() > 0.05
        result = {
            "pipeline_id": pipeline_id, "status": "success" if success else "failed",
            "records_processed": records, "duration_seconds": round(duration, 2),
            "timestamp": datetime.now().isoformat(),
            "bytes_transferred": records * random.randint(100, 1000),
        }
        with self._lock:
            pipeline.last_run = datetime.now()
            pipeline.last_status = result["status"]
            pipeline.records_processed += records
            if not success:
                pipeline.error_count += 1
                if pipeline.alert_on_failure:
                    self._alerts.append({
                        "pipeline_id": pipeline_id,
                        "message": f"Pipeline {pipeline.name} failed",
                        "timestamp": datetime.now().isoformat(),
                    })
            pipeline.avg_duration_seconds = (
                (pipeline.avg_duration_seconds * 0.7) + (duration * 0.3)
            )
            self._run_history[pipeline_id].append(result)
        return result

    def pause_pipeline(self, pipeline_id: str) -> bool:
        with self._lock:
            pipeline = self._pipelines.get(pipeline_id)
            if pipeline:
                pipeline.is_active = False
                return True
        return False

    def resume_pipeline(self, pipeline_id: str) -> bool:
        with self._lock:
            pipeline = self._pipelines.get(pipeline_id)
            if pipeline:
                pipeline.is_active = True
                return True
        return False

    def delete_pipeline(self, pipeline_id: str) -> bool:
        with self._lock:
            if pipeline_id in self._pipelines:
                del self._pipelines[pipeline_id]
                self._run_history.pop(pipeline_id, None)
                return True
        return False

    def get_pipeline(self, pipeline_id: str) -> Optional[IntegrationPipeline]:
        with self._lock:
            return self._pipelines.get(pipeline_id)

    def get_all_pipelines(self) -> List[IntegrationPipeline]:
        with self._lock:
            return list(self._pipelines.values())

    def get_pipelines_by_pattern(self, pattern: IntegrationPattern) -> List[IntegrationPipeline]:
        with self._lock:
            return [p for p in self._pipelines.values() if p.pattern == pattern]

    def get_active_pipelines(self) -> List[IntegrationPipeline]:
        with self._lock:
            return [p for p in self._pipelines.values() if p.is_active]

    def get_pipeline_stats(self, pipeline_id: str) -> Dict[str, Any]:
        with self._lock:
            history = list(self._run_history.get(pipeline_id, []))
        if not history:
            return {"pipeline_id": pipeline_id, "runs": 0}
        total_runs = len(history)
        success_runs = sum(1 for h in history if h["status"] == "success")
        durations = [h["duration_seconds"] for h in history]
        total_records = sum(h["records_processed"] for h in history)
        total_bytes = sum(h.get("bytes_transferred", 0) for h in history)
        return {
            "pipeline_id": pipeline_id,
            "total_runs": total_runs,
            "success_rate": round(success_runs / total_runs, 4) if total_runs > 0 else 0,
            "avg_duration": round(statistics.mean(durations), 2),
            "p95_duration": round(sorted(durations)[int(len(durations) * 0.95)] if durations else 0, 2),
            "total_records": total_records,
            "total_bytes": total_bytes,
            "throughput_records_per_sec": round(total_records / max(sum(durations), 0.001), 2),
        }

    def get_all_pipeline_stats(self) -> Dict[str, Any]:
        stats = {}
        with self._lock:
            pipeline_ids = list(self._pipelines.keys())
        for pid in pipeline_ids:
            stats[pid] = self.get_pipeline_stats(pid)
        return stats

    def get_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._alerts)[-limit:]

    def clear_alerts(self) -> int:
        with self._lock:
            count = len(self._alerts)
            self._alerts.clear()
        return count

# =============================================================================
# MDM MANAGER
# =============================================================================

class MDMManager:
    def __init__(self):
        self._records: Dict[str, MasterDataRecord] = {}
        self._entity_indices: Dict[str, Set[str]] = defaultdict(set)
        self._match_history: List[Dict[str, Any]] = []
        self._survivorship_rules: Dict[str, str] = {}
        self._lock = threading.Lock()

    def create_record(self, entity_type: str, attributes: Dict[str, Any],
                      source_id: str = "", quality_score: float = 1.0) -> MasterDataRecord:
        record_id = str(uuid.uuid4())
        golden_id = f"G_{entity_type}_{record_id[:8]}"
        record = MasterDataRecord(
            record_id=record_id, entity_type=entity_type,
            golden_id=golden_id, source_ids=[source_id] if source_id else [],
            attributes=attributes, confidence_score=0.8,
            quality_score=quality_score,
        )
        with self._lock:
            self._records[record_id] = record
            self._entity_indices[entity_type].add(record_id)
        logger.info("Created MDM record %s for %s", record_id[:8], entity_type)
        return record

    def merge_records(self, record_id_1: str, record_id_2: str,
                      strategy: str = "r1_priority") -> Optional[MasterDataRecord]:
        with self._lock:
            r1 = self._records.get(record_id_1)
            r2 = self._records.get(record_id_2)
            if not r1 or not r2 or r1.entity_type != r2.entity_type:
                return None
            if strategy == "r1_priority":
                merged_attrs = {**r2.attributes, **r1.attributes}
            elif strategy == "r2_priority":
                merged_attrs = {**r1.attributes, **r2.attributes}
            elif strategy == "latest_wins":
                merged_attrs = {**r2.attributes, **r1.attributes} if r1.last_merged >= r2.last_merged else {**r1.attributes, **r2.attributes}
            elif strategy == "highest_quality":
                if r1.quality_score >= r2.quality_score:
                    merged_attrs = {**r2.attributes, **r1.attributes}
                else:
                    merged_attrs = {**r1.attributes, **r2.attributes}
            else:
                merged_attrs = {**r2.attributes, **r1.attributes}
            r1.attributes = merged_attrs
            r1.source_ids.extend(r2.source_ids)
            r1.source_ids = list(set(r1.source_ids))
            r1.confidence_score = min(1.0, r1.confidence_score + 0.1)
            r1.last_merged = datetime.now()
            r1.quality_score = max(r1.quality_score, r2.quality_score)
            del self._records[record_id_2]
            self._entity_indices[r1.entity_type].discard(record_id_2)
            self._match_history.append({
                "merged": [record_id_1, record_id_2],
                "strategy": strategy,
                "timestamp": datetime.now().isoformat(),
            })
        return r1

    def set_survivorship_rule(self, entity_type: str, field_name: str,
                              rule: str) -> None:
        key = f"{entity_type}.{field_name}"
        with self._lock:
            self._survivorship_rules[key] = rule
        logger.info("Set survivorship rule %s: %s", key, rule)

    def apply_survivorship(self, record_id: str) -> Optional[MasterDataRecord]:
        with self._lock:
            record = self._records.get(record_id)
        if not record:
            return None
        for key, rule in self._survivorship_rules.items():
            entity_type, field_name = key.split(".", 1)
            if entity_type == record.entity_type and field_name in record.attributes:
                value = record.attributes[field_name]
                if rule == "uppercase" and isinstance(value, str):
                    record.attributes[field_name] = value.upper()
                elif rule == "trim" and isinstance(value, str):
                    record.attributes[field_name] = value.strip()
        return record

    def match_records(self, entity_type: str, match_criteria: Dict[str, Any]) -> List[Tuple[str, str]]:
        matches = []
        with self._lock:
            entity_ids = list(self._entity_indices.get(entity_type, set()))
            records = [self._records[rid] for rid in entity_ids if rid in self._records]
        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                r1, r2 = records[i], records[j]
                is_match = all(
                    str(r1.attributes.get(k)).lower() == str(r2.attributes.get(k)).lower()
                    for k in match_criteria.keys()
                )
                if is_match:
                    matches.append((r1.record_id, r2.record_id))
        return matches

    def fuzzy_match(self, entity_type: str, field: str, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
        with self._lock:
            entity_ids = list(self._entity_indices.get(entity_type, set()))
            records = [self._records[rid] for rid in entity_ids if rid in self._records]
        matches = []
        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                v1 = str(records[i].attributes.get(field, ""))
                v2 = str(records[j].attributes.get(field, ""))
                similarity = self._simple_similarity(v1, v2)
                if similarity >= threshold:
                    matches.append((records[i].record_id, records[j].record_id, similarity))
        return matches

    @staticmethod
    def _simple_similarity(a: str, b: str) -> float:
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0
        a_set = set(a.lower().split())
        b_set = set(b.lower().split())
        intersection = a_set & b_set
        union = a_set | b_set
        return len(intersection) / len(union) if union else 0.0

    def get_record(self, record_id: str) -> Optional[MasterDataRecord]:
        with self._lock:
            return self._records.get(record_id)

    def get_records_by_entity(self, entity_type: str) -> List[MasterDataRecord]:
        with self._lock:
            ids = list(self._entity_indices.get(entity_type, set()))
            return [self._records[rid] for rid in ids if rid in self._records]

    def search_records(self, entity_type: str, query: Dict[str, Any]) -> List[MasterDataRecord]:
        records = self.get_records_by_entity(entity_type)
        results = []
        for record in records:
            match = all(record.attributes.get(k) == v for k, v in query.items())
            if match:
                results.append(record)
        return results

    def get_mdm_stats(self) -> Dict[str, Any]:
        with self._lock:
            records = list(self._records.values())
        by_entity = defaultdict(int)
        for r in records:
            by_entity[r.entity_type] += 1
        avg_confidence = statistics.mean([r.confidence_score for r in records]) if records else 0
        avg_quality = statistics.mean([r.quality_score for r in records]) if records else 0
        return {
            "total_records": len(records),
            "by_entity": dict(by_entity),
            "avg_confidence": round(avg_confidence, 3),
            "avg_quality_score": round(avg_quality, 3),
            "total_merges": len(self._match_history),
            "survivorship_rules_count": len(self._survivorship_rules),
        }

    def get_duplicates(self, entity_type: str, field: str) -> List[List[str]]:
        records = self.get_records_by_entity(entity_type)
        value_map: Dict[str, List[str]] = defaultdict(list)
        for r in records:
            val = str(r.attributes.get(field, "")).lower().strip()
            if val:
                value_map[val].append(r.record_id)
        return [ids for ids in value_map.values() if len(ids) > 1]

# =============================================================================
# DATA CATALOG
# =============================================================================

class DataCatalog:
    def __init__(self, model_manager: DataModelManager):
        self._model_manager = model_manager
        self._metadata: Dict[str, MetadataEntry] = {}
        self._search_index: Dict[str, Set[str]] = defaultdict(set)
        self._lineage_entries: Dict[str, List[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add_metadata(self, entity_type: str, entity_id: str, key: str,
                     value: Any, source: str = "", tags: Optional[List[str]] = None) -> MetadataEntry:
        entry_id = f"{entity_type}_{entity_id}_{key}"
        entry = MetadataEntry(
            entry_id=entry_id, entity_type=entity_type,
            entity_id=entity_id, key=key, value=value, source=source,
            tags=tags or [],
        )
        with self._lock:
            self._metadata[entry_id] = entry
            tokens = key.lower().split()
            for token in tokens:
                self._search_index[token].add(entry_id)
            if isinstance(value, str):
                for token in value.lower().split():
                    self._search_index[token].add(entry_id)
        return entry

    def update_metadata(self, entry_id: str, value: Any) -> bool:
        with self._lock:
            entry = self._metadata.get(entry_id)
            if entry:
                entry.value = value
                entry.updated_at = datetime.now()
                return True
        return False

    def delete_metadata(self, entry_id: str) -> bool:
        with self._lock:
            if entry_id in self._metadata:
                entry = self._metadata[entry_id]
                tokens = entry.key.lower().split()
                for token in tokens:
                    self._search_index.get(token, set()).discard(entry_id)
                del self._metadata[entry_id]
                return True
        return False

    def search(self, query: str, entity_type: Optional[str] = None,
               max_results: int = MAX_CATALOG_SEARCH_RESULTS) -> List[MetadataEntry]:
        tokens = query.lower().split()
        matching_ids: Set[str] = set()
        first = True
        for token in tokens:
            token_ids = self._search_index.get(token, set())
            if first:
                matching_ids = set(token_ids)
                first = False
            else:
                matching_ids &= token_ids
        with self._lock:
            results = [self._metadata[eid] for eid in matching_ids if eid in self._metadata]
        if entity_type:
            results = [e for e in results if e.entity_type == entity_type]
        return results[:max_results]

    def get_entity_metadata(self, entity_type: str, entity_id: str) -> Dict[str, Any]:
        with self._lock:
            return {e.key: e.value for e in self._metadata.values()
                    if e.entity_type == entity_type and e.entity_id == entity_id}

    def get_all_metadata(self, entity_type: Optional[str] = None) -> List[MetadataEntry]:
        with self._lock:
            entries = list(self._metadata.values())
        if entity_type:
            entries = [e for e in entries if e.entity_type == entity_type]
        return entries

    def get_catalog_stats(self) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._metadata.values())
        by_entity = defaultdict(int)
        by_source = defaultdict(int)
        for e in entries:
            by_entity[e.entity_type] += 1
            if e.source:
                by_source[e.source] += 1
        return {
            "total_entries": len(entries),
            "by_entity_type": dict(by_entity),
            "by_source": dict(by_source),
            "unique_keys": len(set(e.key for e in entries)),
        }

    def auto_discover(self) -> Dict[str, Any]:
        discovered = 0
        tables = self._model_manager.get_all_tables()
        for table in tables:
            key = f"table_{table.table_id}_schema"
            if not any(e.entity_id == table.table_id and e.key == "schema"
                       for e in self._metadata.values()):
                self.add_metadata("table", table.table_id, "schema", table.schema_name,
                                  source="auto_discover")
                discovered += 1
        return {"discovered": discovered, "total_tables": len(tables)}

# =============================================================================
# DATA QUALITY MANAGER
# =============================================================================

class DataQualityManager:
    def __init__(self):
        self._rules: Dict[str, QualityRule] = {}
        self._results: Dict[str, List[QualityCheckResult]] = defaultdict(list)
        self._score_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def create_rule(self, rule_id: str, name: str, rule_type: QualityRuleType,
                    table_id: str, field_id: Optional[str] = None,
                    threshold: float = 99.0, owner: str = "",
                    severity: str = "warning",
                    tags: Optional[List[str]] = None) -> QualityRule:
        if rule_id in self._rules:
            raise QualityError(f"Rule {rule_id} already exists")
        rule = QualityRule(
            rule_id=rule_id, name=name, rule_type=rule_type,
            table_id=table_id, field_id=field_id, threshold=threshold,
            owner=owner, severity=severity, tags=tags or [],
        )
        with self._lock:
            self._rules[rule_id] = rule
        return rule

    def delete_rule(self, rule_id: str) -> bool:
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                self._results.pop(rule_id, None)
                return True
        return False

    def run_check(self, rule_id: str) -> QualityCheckResult:
        with self._lock:
            rule = self._rules.get(rule_id)
        if not rule:
            return QualityCheckResult(
                check_id=str(uuid.uuid4()), rule_id=rule_id,
                table_id="", passed=False, actual_value=0,
                expected_threshold=0, details="Rule not found",
            )
        start = time.time()
        actual_value = random.uniform(90, 100)
        passed = actual_value >= rule.threshold
        duration_ms = (time.time() - start) * 1000
        result = QualityCheckResult(
            check_id=str(uuid.uuid4()), rule_id=rule_id,
            table_id=rule.table_id, passed=passed,
            actual_value=round(actual_value, 2),
            expected_threshold=rule.threshold,
            duration_ms=round(duration_ms, 2),
            records_scanned=random.randint(1000, 1000000),
            violations_found=0 if passed else random.randint(1, 100),
        )
        with self._lock:
            rule.last_checked = datetime.now()
            rule.last_result = passed
            rule.last_value = actual_value
            self._results[rule_id].append(result)
        return result

    def run_all_checks(self) -> List[QualityCheckResult]:
        results = []
        with self._lock:
            rule_ids = list(self._rules.keys())
        for rid in rule_ids:
            results.append(self.run_check(rid))
        passing = sum(1 for r in results if r.passed)
        self._score_history.append({
            "timestamp": datetime.now().isoformat(),
            "total": len(results),
            "passing": passing,
            "score": round(passing / len(results) * 100, 2) if results else 0,
        })
        return results

    def get_rule(self, rule_id: str) -> Optional[QualityRule]:
        with self._lock:
            return self._rules.get(rule_id)

    def get_rules_for_table(self, table_id: str) -> List[QualityRule]:
        with self._lock:
            return [r for r in self._rules.values() if r.table_id == table_id]

    def get_rules_by_type(self, rule_type: QualityRuleType) -> List[QualityRule]:
        with self._lock:
            return [r for r in self._rules.values() if r.rule_type == rule_type]

    def get_rules_by_severity(self, severity: str) -> List[QualityRule]:
        with self._lock:
            return [r for r in self._rules.values() if r.severity == severity]

    def get_check_history(self, rule_id: str, limit: int = 50) -> List[QualityCheckResult]:
        with self._lock:
            return list(self._results.get(rule_id, []))[-limit:]

    def get_quality_dashboard(self) -> Dict[str, Any]:
        with self._lock:
            rules = list(self._rules.values())
        total = len(rules)
        passing = sum(1 for r in rules if r.last_result is True)
        failing = sum(1 for r in rules if r.last_result is False)
        not_checked = total - passing - failing
        by_type = defaultdict(lambda: {"passing": 0, "failing": 0})
        for r in rules:
            if r.last_result is True:
                by_type[r.rule_type.name]["passing"] += 1
            elif r.last_result is False:
                by_type[r.rule_type.name]["failing"] += 1
        return {
            "total_rules": total, "passing": passing, "failing": failing,
            "not_checked": not_checked,
            "pass_rate": round(passing / total, 4) if total > 0 else 0,
            "by_type": dict(by_type),
        }

    def get_score_history(self, limit: int = 30) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._score_history)[-limit:]

    def get_all_rules(self) -> List[QualityRule]:
        with self._lock:
            return list(self._rules.values())

# =============================================================================
# DATA LINEAGE
# =============================================================================

class DataLineage:
    def __init__(self):
        self._nodes: Dict[str, LineageNode] = {}
        self._edges: List[LineageEdge] = []
        self._lock = threading.Lock()

    def add_node(self, node_id: str, name: str, node_type: LineageNodeType,
                 **kwargs) -> LineageNode:
        node = LineageNode(
            node_id=node_id, name=name, node_type=node_type,
            source_table=kwargs.get("source_table"),
            target_table=kwargs.get("target_table"),
            transformation=kwargs.get("transformation", ""),
            owner=kwargs.get("owner", ""),
            tags=kwargs.get("tags", []),
        )
        with self._lock:
            self._nodes[node_id] = node
        return node

    def remove_node(self, node_id: str) -> bool:
        with self._lock:
            if node_id in self._nodes:
                del self._nodes[node_id]
                self._edges = [e for e in self._edges
                               if e.source_node != node_id and e.target_node != node_id]
                return True
        return False

    def add_edge(self, source_node: str, target_node: str,
                 edge_type: str = "data_flow",
                 metadata: Optional[Dict[str, Any]] = None) -> LineageEdge:
        with self._lock:
            if source_node not in self._nodes or target_node not in self._nodes:
                raise LineageError(f"Node not found: {source_node} or {target_node}")
            edge = LineageEdge(
                edge_id=str(uuid.uuid4()), source_node=source_node,
                target_node=target_node, edge_type=edge_type,
                metadata=metadata or {},
            )
            self._edges.append(edge)
        return edge

    def remove_edge(self, edge_id: str) -> bool:
        with self._lock:
            original_count = len(self._edges)
            self._edges = [e for e in self._edges if e.edge_id != edge_id]
            return len(self._edges) < original_count

    def get_upstream(self, node_id: str, depth: int = MAX_LINEAGE_DEPTH) -> List[str]:
        visited: Set[str] = set()
        queue = [node_id]
        for _ in range(min(depth, MAX_LINEAGE_DEPTH)):
            next_queue = []
            for nid in queue:
                if nid in visited:
                    continue
                visited.add(nid)
                with self._lock:
                    for edge in self._edges:
                        if edge.target_node == nid:
                            next_queue.append(edge.source_node)
            queue = next_queue
        return list(visited - {node_id})

    def get_downstream(self, node_id: str, depth: int = MAX_LINEAGE_DEPTH) -> List[str]:
        visited: Set[str] = set()
        queue = [node_id]
        for _ in range(min(depth, MAX_LINEAGE_DEPTH)):
            next_queue = []
            for nid in queue:
                if nid in visited:
                    continue
                visited.add(nid)
                with self._lock:
                    for edge in self._edges:
                        if edge.source_node == nid:
                            next_queue.append(edge.target_node)
            queue = next_queue
        return list(visited - {node_id})

    def get_impact_analysis(self, node_id: str) -> Dict[str, Any]:
        upstream = self.get_upstream(node_id)
        downstream = self.get_downstream(node_id)
        with self._lock:
            node = self._nodes.get(node_id)
        return {
            "node_id": node_id,
            "node_name": node.name if node else "unknown",
            "node_type": node.node_type.name if node else "unknown",
            "upstream_count": len(upstream),
            "downstream_count": len(downstream),
            "upstream_nodes": upstream,
            "downstream_nodes": downstream,
            "critical_path_length": len(upstream) + len(downstream),
        }

    def get_shortest_path(self, source: str, target: str) -> Optional[List[str]]:
        if source == target:
            return [source]
        visited: Set[str] = {source}
        queue: List[Tuple[str, List[str]]] = [(source, [source])]
        while queue:
            current, path = queue.pop(0)
            with self._lock:
                for edge in self._edges:
                    if edge.source_node == current and edge.target_node not in visited:
                        new_path = path + [edge.target_node]
                        if edge.target_node == target:
                            return new_path
                        visited.add(edge.target_node)
                        queue.append((edge.target_node, new_path))
        return None

    def get_all_nodes(self) -> List[LineageNode]:
        with self._lock:
            return list(self._nodes.values())

    def get_all_edges(self) -> List[LineageEdge]:
        with self._lock:
            return list(self._edges)

    def get_nodes_by_type(self, node_type: LineageNodeType) -> List[LineageNode]:
        with self._lock:
            return [n for n in self._nodes.values() if n.node_type == node_type]

    def get_lineage_stats(self) -> Dict[str, Any]:
        with self._lock:
            nodes = list(self._nodes.values())
            edges = list(self._edges)
        by_type = defaultdict(int)
        for n in nodes:
            by_type[n.node_type.name] += 1
        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "by_type": dict(by_type),
            "avg_out_degree": round(len(edges) / max(len(nodes), 1), 2),
        }

# =============================================================================
# GOVERNANCE MANAGER
# =============================================================================

class GovernanceManager:
    def __init__(self):
        self._policies: Dict[str, GovernanceRule] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self._compliance_checks: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def create_policy(self, rule_id: str, name: str, policy_type: GovernancePolicy,
                      description: str = "", scope: str = "",
                      enforcement_level: str = "advisory") -> GovernanceRule:
        if rule_id in self._policies:
            raise GovernanceError(f"Policy {rule_id} already exists")
        rule = GovernanceRule(
            rule_id=rule_id, name=name, policy_type=policy_type,
            description=description, scope=scope,
            enforcement_level=enforcement_level,
        )
        with self._lock:
            self._policies[rule_id] = rule
        logger.info("Created governance policy %s: %s", rule_id, name)
        return rule

    def update_policy(self, rule_id: str, **kwargs) -> bool:
        with self._lock:
            policy = self._policies.get(rule_id)
            if policy:
                for key, value in kwargs.items():
                    if hasattr(policy, key):
                        setattr(policy, key, value)
                return True
        return False

    def delete_policy(self, rule_id: str) -> bool:
        with self._lock:
            if rule_id in self._policies:
                del self._policies[rule_id]
                return True
        return False

    def log_audit_event(self, event_type: str, entity_type: str, entity_id: str,
                        user: str, details: str = "",
                        ip_address: str = "") -> None:
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type, "entity_type": entity_type,
            "entity_id": entity_id, "user": user, "details": details,
            "ip_address": ip_address,
            "timestamp": datetime.now().isoformat(),
        }
        with self._lock:
            self._audit_log.append(event)
            if len(self._audit_log) > MAX_AUDIT_LOG_ENTRIES:
                self._audit_log = self._audit_log[-MAX_AUDIT_LOG_ENTRIES:]

    def get_audit_log(self, entity_type: Optional[str] = None,
                      user: Optional[str] = None,
                      event_type: Optional[str] = None,
                      limit: int = 100) -> List[Dict[str, Any]]:
        with self._lock:
            log = list(self._audit_log)
        if entity_type:
            log = [e for e in log if e["entity_type"] == entity_type]
        if user:
            log = [e for e in log if e["user"] == user]
        if event_type:
            log = [e for e in log if e["event_type"] == event_type]
        return log[-limit:]

    def run_compliance_check(self, policy_id: str) -> Dict[str, Any]:
        with self._lock:
            policy = self._policies.get(policy_id)
        if not policy:
            return {"error": "Policy not found"}
        passed = random.random() > 0.1
        result = {
            "check_id": str(uuid.uuid4()),
            "policy_id": policy_id,
            "policy_name": policy.name,
            "passed": passed,
            "timestamp": datetime.now().isoformat(),
            "details": "Compliance check passed" if passed else "Non-compliance detected",
        }
        with self._lock:
            self._compliance_checks.append(result)
            policy.last_audit = datetime.now()
        return result

    def get_policy(self, rule_id: str) -> Optional[GovernanceRule]:
        with self._lock:
            return self._policies.get(rule_id)

    def get_policies_by_type(self, policy_type: GovernancePolicy) -> List[GovernanceRule]:
        with self._lock:
            return [p for p in self._policies.values() if p.policy_type == policy_type]

    def get_policies_by_enforcement(self, level: str) -> List[GovernanceRule]:
        with self._lock:
            return [p for p in self._policies.values() if p.enforcement_level == level]

    def get_governance_summary(self) -> Dict[str, Any]:
        with self._lock:
            policies = list(self._policies.values())
        by_type = defaultdict(int)
        by_enforcement = defaultdict(int)
        for p in policies:
            by_type[p.policy_type.name] += 1
            by_enforcement[p.enforcement_level] += 1
        recent_compliance = self._compliance_checks[-10:]
        compliance_rate = (
            sum(1 for c in recent_compliance if c["passed"]) / len(recent_compliance)
            if recent_compliance else 0
        )
        return {
            "total_policies": len(policies),
            "by_type": dict(by_type),
            "by_enforcement": dict(by_enforcement),
            "audit_events": len(self._audit_log),
            "compliance_rate": round(compliance_rate, 4),
            "total_compliance_checks": len(self._compliance_checks),
        }

# =============================================================================
# SCHEMA REGISTRY
# =============================================================================

class SchemaRegistry:
    def __init__(self, model_manager: DataModelManager):
        self._model_manager = model_manager
        self._versions: Dict[str, List[SchemaVersion]] = defaultdict(list)
        self._compatibility_cache: Dict[str, SchemaCompatibility] = {}
        self._lock = threading.Lock()

    def register_schema(self, table_id: str, schema_snapshot: Dict[str, Any],
                        created_by: str = "",
                        description: str = "") -> SchemaVersion:
        with self._lock:
            versions = self._versions[table_id]
            version_number = len(versions) + 1
        version = SchemaVersion(
            version_id=str(uuid.uuid4()),
            table_id=table_id,
            version_number=version_number,
            schema_snapshot=schema_snapshot,
            created_by=created_by,
            change_description=description,
        )
        with self._lock:
            self._versions[table_id].append(version)
        logger.info("Registered schema v%d for table %s", version_number, table_id)
        return version

    def get_latest_version(self, table_id: str) -> Optional[SchemaVersion]:
        with self._lock:
            versions = self._versions.get(table_id, [])
        return versions[-1] if versions else None

    def get_version(self, table_id: str, version_number: int) -> Optional[SchemaVersion]:
        with self._lock:
            versions = self._versions.get(table_id, [])
        if 1 <= version_number <= len(versions):
            return versions[version_number - 1]
        return None

    def get_all_versions(self, table_id: str) -> List[SchemaVersion]:
        with self._lock:
            return list(self._versions.get(table_id, []))

    def check_compatibility(self, table_id: str,
                            new_schema: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            versions = self._versions.get(table_id, [])
        if not versions:
            return {"compatible": True, "reason": "No existing schema"}
        latest = versions[-1]
        old_fields = set(latest.schema_snapshot.get("fields", {}).keys())
        new_fields = set(new_schema.get("fields", {}).keys())
        added = new_fields - old_fields
        removed = old_fields - new_fields
        modified = set()
        for field_name in old_fields & new_fields:
            if latest.schema_snapshot["fields"].get(field_name) != new_schema["fields"].get(field_name):
                modified.add(field_name)
        compatible = len(removed) == 0 and len(modified) == 0
        return {
            "compatible": compatible,
            "added_fields": list(added),
            "removed_fields": list(removed),
            "modified_fields": list(modified),
            "base_version": latest.version_number,
        }

    def evolve_schema(self, table_id: str, change_type: SchemaEvolution,
                      details: Dict[str, Any], applied_by: str = "") -> SchemaChange:
        latest = self.get_latest_version(table_id)
        if latest is None:
            raise SchemaRegistryError(f"No schema registered for table {table_id}")
        new_snapshot = dict(latest.schema_snapshot)
        fields = dict(new_snapshot.get("fields", {}))
        breaking = False
        if change_type == SchemaEvolution.ADD_COLUMN:
            fields[details["field_name"]] = details.get("field_type", "STRING")
        elif change_type == SchemaEvolution.DROP_COLUMN:
            fields.pop(details["field_name"], None)
            breaking = True
        elif change_type == SchemaEvolution.RENAME_COLUMN:
            old_name = details["old_name"]
            new_name = details["new_name"]
            if old_name in fields:
                fields[new_name] = fields.pop(old_name)
            breaking = True
        elif change_type == SchemaEvolution.CHANGE_TYPE:
            field_name = details["field_name"]
            if field_name in fields:
                fields[field_name] = details["new_type"]
            breaking = True
        new_snapshot["fields"] = fields
        change = SchemaChange(
            change_id=str(uuid.uuid4()),
            table_id=table_id,
            change_type=change_type,
            details=details,
            applied_by=applied_by,
            breaking_change=breaking,
        )
        self._model_manager.record_schema_change(change)
        self.register_schema(table_id, new_snapshot, created_by=applied_by,
                             description=f"Schema evolution: {change_type.name}")
        return change

    def get_schema_diff(self, table_id: str, version_a: int, version_b: int) -> Dict[str, Any]:
        with self._lock:
            versions = self._versions.get(table_id, [])
        if version_a < 1 or version_b < 1 or version_a > len(versions) or version_b > len(versions):
            return {"error": "Invalid version numbers"}
        a = versions[version_a - 1].schema_snapshot
        b = versions[version_b - 1].schema_snapshot
        a_fields = set(a.get("fields", {}).keys())
        b_fields = set(b.get("fields", {}).keys())
        return {
            "added": list(b_fields - a_fields),
            "removed": list(a_fields - b_fields),
            "common": list(a_fields & b_fields),
        }

# =============================================================================
# DATA PARTITIONER
# =============================================================================

class DataPartitioner:
    def __init__(self):
        self._configs: Dict[str, PartitionConfig] = {}
        self._partitions: Dict[str, List[DataPartition]] = defaultdict(list)
        self._lock = threading.Lock()

    def create_partition_config(self, config_id: str, table_id: str,
                                strategy: PartitionStrategy,
                                column_name: str = "",
                                partition_count: int = DEFAULT_PARTITION_COUNT,
                                interval: Optional[str] = None) -> PartitionConfig:
        config = PartitionConfig(
            config_id=config_id, table_id=table_id,
            strategy=strategy, column_name=column_name,
            partition_count=partition_count, interval=interval,
        )
        with self._lock:
            self._configs[config_id] = config
        logger.info("Created partition config %s for table %s (%s)",
                    config_id, table_id, strategy.name)
        return config

    def compute_partition(self, config_id: str, partition_key: Any) -> int:
        with self._lock:
            config = self._configs.get(config_id)
        if not config:
            raise PartitionError(f"Partition config {config_id} not found")
        if config.strategy == PartitionStrategy.HASH:
            return hash(str(partition_key)) % config.partition_count
        elif config.strategy == PartitionStrategy.RANGE:
            return min(int(partition_key) % config.partition_count, config.partition_count - 1)
        elif config.strategy == PartitionStrategy.TIME_INTERVAL:
            return int(time.time()) // 86400 % config.partition_count
        return 0

    def get_partition_for_key(self, table_id: str, key: Any) -> Optional[DataPartition]:
        with self._lock:
            for config in self._configs.values():
                if config.table_id == table_id:
                    idx = self.compute_partition(config.config_id, key)
                    partitions = self._partitions.get(table_id, [])
                    if idx < len(partitions):
                        return partitions[idx]
        return None

    def init_partitions(self, config_id: str) -> List[DataPartition]:
        with self._lock:
            config = self._configs.get(config_id)
            if not config:
                return []
        partitions = []
        for i in range(config.partition_count):
            partition = DataPartition(
                partition_id=f"{config.table_id}_p{i}",
                table_id=config.table_id,
                partition_key=str(i),
            )
            partitions.append(partition)
        with self._lock:
            self._partitions[config.table_id] = partitions
        return partitions

    def get_config(self, config_id: str) -> Optional[PartitionConfig]:
        with self._lock:
            return self._configs.get(config_id)

    def get_partitions_for_table(self, table_id: str) -> List[DataPartition]:
        with self._lock:
            return list(self._partitions.get(table_id, []))

    def get_partition_stats(self, table_id: str) -> Dict[str, Any]:
        with self._lock:
            partitions = list(self._partitions.get(table_id, []))
        total_rows = sum(p.row_count for p in partitions)
        total_size = sum(p.size_bytes for p in partitions)
        return {
            "table_id": table_id,
            "partition_count": len(partitions),
            "total_rows": total_rows,
            "total_size_bytes": total_size,
            "avg_rows_per_partition": round(total_rows / max(len(partitions), 1)),
            "avg_size_per_partition": round(total_size / max(len(partitions), 1)),
        }

# =============================================================================
# DATA MASKING ENGINE
# =============================================================================

class DataMaskingEngine:
    def __init__(self):
        self._rules: Dict[str, MaskingRule] = {}
        self._masking_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def create_rule(self, rule_id: str, name: str, table_id: str,
                    field_id: str, masking_type: MaskingType,
                    pattern: str = "", replacement: str = "***",
                    salt: str = "") -> MaskingRule:
        rule = MaskingRule(
            rule_id=rule_id, name=name, table_id=table_id,
            field_id=field_id, masking_type=masking_type,
            pattern=pattern, replacement=replacement, salt=salt,
        )
        with self._lock:
            self._rules[rule_id] = rule
        logger.info("Created masking rule %s: %s", rule_id, masking_type.name)
        return rule

    def mask_value(self, rule_id: str, value: Any) -> Any:
        with self._lock:
            rule = self._rules.get(rule_id)
        if not rule:
            return value
        if value is None:
            return None
        if rule.masking_type == MaskingType.FULL_REDACT:
            return rule.replacement * len(str(value)) if str(value) else rule.replacement
        elif rule.masking_type == MaskingType.PARTIAL:
            s = str(value)
            if len(s) <= 4:
                return rule.replacement
            return s[:2] + rule.replacement + s[-2:]
        elif rule.masking_type == MaskingType.HASH:
            to_hash = f"{rule.salt}{value}" if rule.salt else str(value)
            return hashlib.sha256(to_hash.encode()).hexdigest()[:16]
        elif rule.masking_type == MaskingType.TOKENIZE:
            return f"TOKEN_{hashlib.md5(str(value).encode()).hexdigest()[:8]}"
        elif rule.masking_type == MaskingType.NULL_OUT:
            return None
        elif rule.masking_type == MaskingType.SHUFFLE:
            chars = list(str(value))
            random.shuffle(chars)
            return "".join(chars)
        elif rule.masking_type == MaskingType.DATE_SHIFT:
            try:
                if isinstance(value, str):
                    return value
                dt = datetime.fromisoformat(str(value))
                shifted = dt + timedelta(days=random.randint(1, 30))
                return shifted.isoformat()
            except (ValueError, TypeError):
                return str(value)
        return value

    def apply_rules_to_record(self, table_id: str,
                              record: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            rules = [r for r in self._rules.values() if r.table_id == table_id and r.is_active]
        masked = dict(record)
        for rule in rules:
            if rule.field_id in masked:
                masked[rule.field_id] = self.mask_value(rule.rule_id, masked[rule.field_id])
        if rules:
            self._masking_history.append({
                "table_id": table_id,
                "fields_masked": len(rules),
                "timestamp": datetime.now().isoformat(),
            })
        return masked

    def get_rule(self, rule_id: str) -> Optional[MaskingRule]:
        with self._lock:
            return self._rules.get(rule_id)

    def get_rules_for_table(self, table_id: str) -> List[MaskingRule]:
        with self._lock:
            return [r for r in self._rules.values() if r.table_id == table_id]

    def delete_rule(self, rule_id: str) -> bool:
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
        return False

    def get_masking_stats(self) -> Dict[str, Any]:
        with self._lock:
            rules = list(self._rules.values())
        by_type = defaultdict(int)
        for r in rules:
            by_type[r.masking_type.name] += 1
        return {
            "total_rules": len(rules),
            "by_type": dict(by_type),
            "total_applications": len(self._masking_history),
        }

# =============================================================================
# DEPENDENCY GRAPH BUILDER
# =============================================================================

class DependencyGraphBuilder:
    def __init__(self):
        self._nodes: Dict[str, DependencyNode] = {}
        self._adjacency: Dict[str, Set[str]] = defaultdict(set)
        self._reverse_adjacency: Dict[str, Set[str]] = defaultdict(set)
        self._lock = threading.Lock()

    def add_node(self, node_id: str, entity_type: str, entity_id: str,
                 name: str, dependency_type: DependencyType) -> DependencyNode:
        node = DependencyNode(
            node_id=node_id, entity_type=entity_type,
            entity_id=entity_id, name=name,
            dependency_type=dependency_type,
        )
        with self._lock:
            self._nodes[node_id] = node
        return node

    def add_dependency(self, source_id: str, target_id: str) -> bool:
        with self._lock:
            if source_id not in self._nodes or target_id not in self._nodes:
                return False
            self._adjacency[source_id].add(target_id)
            self._reverse_adjacency[target_id].add(source_id)
            self._nodes[source_id].depends_on.append(target_id)
            self._nodes[target_id].depended_by.append(source_id)
        return True

    def remove_dependency(self, source_id: str, target_id: str) -> bool:
        with self._lock:
            self._adjacency[source_id].discard(target_id)
            self._reverse_adjacency[target_id].discard(source_id)
            if source_id in self._nodes:
                self._nodes[source_id].depends_on = [
                    d for d in self._nodes[source_id].depends_on if d != target_id
                ]
            if target_id in self._nodes:
                self._nodes[target_id].depended_by = [
                    d for d in self._nodes[target_id].depended_by if d != source_id
                ]
        return True

    def get_dependents(self, node_id: str) -> List[DependencyNode]:
        with self._lock:
            dep_ids = self._adjacency.get(node_id, set())
        return [self._nodes[did] for did in dep_ids if did in self._nodes]

    def get_dependencies(self, node_id: str) -> List[DependencyNode]:
        with self._lock:
            dep_ids = self._reverse_adjacency.get(node_id, set())
        return [self._nodes[did] for did in dep_ids if did in self._nodes]

    def get_all_nodes(self) -> List[DependencyNode]:
        with self._lock:
            return list(self._nodes.values())

    def topological_sort(self) -> List[str]:
        with self._lock:
            in_degree = defaultdict(int)
            for node_id in self._nodes:
                in_degree[node_id]  # ensure exists
            for source, targets in self._adjacency.items():
                for target in targets:
                    in_degree[target] += 1
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        result = []
        while queue:
            node_id = queue.pop(0)
            result.append(node_id)
            with self._lock:
                for target in self._adjacency.get(node_id, set()):
                    in_degree[target] -= 1
                    if in_degree[target] == 0:
                        queue.append(target)
        return result

    def get_critical_path(self) -> List[str]:
        sort = self.topological_sort()
        if not sort:
            return []
        max_depth = 0
        critical_node = sort[0]
        depths = {nid: 0 for nid in sort}
        for nid in sort:
            with self._lock:
                for dep in self._adjacency.get(nid, set()):
                    depths[dep] = max(depths[dep], depths[nid] + 1)
                    if depths[dep] > max_depth:
                        max_depth = depths[dep]
                        critical_node = dep
        path = [critical_node]
        current = critical_node
        while True:
            with self._lock:
                parents = list(self._reverse_adjacency.get(current, set()))
            if not parents:
                break
            best_parent = max(parents, key=lambda p: depths.get(p, 0))
            path.append(best_parent)
            current = best_parent
        path.reverse()
        return path

    def get_graph_stats(self) -> Dict[str, Any]:
        with self._lock:
            total_edges = sum(len(targets) for targets in self._adjacency.values())
        by_type = defaultdict(int)
        for node in self._nodes.values():
            by_type[node.dependency_type.name] += 1
        return {
            "total_nodes": len(self._nodes),
            "total_edges": total_edges,
            "by_type": dict(by_type),
            "avg_edges_per_node": round(total_edges / max(len(self._nodes), 1), 2),
        }

# =============================================================================
# DATA RETENTION MANAGER
# =============================================================================

class DataRetentionManager:
    def __init__(self):
        self._records: Dict[str, RetentionRecord] = {}
        self._execution_log: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def create_retention_rule(self, record_id: str, table_id: str,
                              action: RetentionAction, retention_days: int = 365,
                              criteria: Optional[Dict[str, Any]] = None) -> RetentionRecord:
        record = RetentionRecord(
            record_id=record_id, table_id=table_id,
            action=action, retention_days=retention_days,
            criteria=criteria or {},
            next_scheduled=datetime.now() + timedelta(days=retention_days),
        )
        with self._lock:
            self._records[record_id] = record
        logger.info("Created retention rule %s for table %s: %s after %d days",
                    record_id, table_id, action.name, retention_days)
        return record

    def execute_retention(self, record_id: str) -> Dict[str, Any]:
        with self._lock:
            record = self._records.get(record_id)
        if not record:
            return {"error": "Retention record not found"}
        affected = random.randint(0, 10000)
        result = {
            "record_id": record_id,
            "action": record.action.name,
            "table_id": record.table_id,
            "affected_rows": affected,
            "timestamp": datetime.now().isoformat(),
            "status": "executed",
        }
        with self._lock:
            record.last_executed = datetime.now()
            record.affected_rows_last_run = affected
            record.next_scheduled = datetime.now() + timedelta(days=record.retention_days)
            self._execution_log.append(result)
        return result

    def get_due_rules(self) -> List[RetentionRecord]:
        now = datetime.now()
        with self._lock:
            return [r for r in self._records.values()
                    if r.next_scheduled and r.next_scheduled <= now and r.is_active]

    def get_record(self, record_id: str) -> Optional[RetentionRecord]:
        with self._lock:
            return self._records.get(record_id)

    def get_rules_for_table(self, table_id: str) -> List[RetentionRecord]:
        with self._lock:
            return [r for r in self._records.values() if r.table_id == table_id]

    def delete_rule(self, record_id: str) -> bool:
        with self._lock:
            if record_id in self._records:
                del self._records[record_id]
                return True
        return False

    def get_retention_stats(self) -> Dict[str, Any]:
        with self._lock:
            records = list(self._records.values())
        by_action = defaultdict(int)
        total_affected = 0
        for r in records:
            by_action[r.action.name] += 1
            total_affected += r.affected_rows_last_run
        return {
            "total_rules": len(records),
            "by_action": dict(by_action),
            "total_rows_affected": total_affected,
            "total_executions": len(self._execution_log),
            "due_rules": len(self.get_due_rules()),
        }

# =============================================================================
# COST TRACKER
# =============================================================================

class CostTracker:
    def __init__(self):
        self._entries: List[CostEntry] = []
        self._budgets: Dict[CostCategory, float] = {}
        self._lock = threading.Lock()

    def record_cost(self, category: CostCategory, amount: float,
                    description: str = "", resource_id: str = "",
                    resource_type: str = "",
                    tags: Optional[List[str]] = None) -> CostEntry:
        entry = CostEntry(
            entry_id=str(uuid.uuid4()),
            category=category, amount=amount,
            description=description, resource_id=resource_id,
            resource_type=resource_type, tags=tags or [],
        )
        with self._lock:
            self._entries.append(entry)
        logger.info("Recorded cost: $%.2f (%s)", amount, category.name)
        return entry

    def set_budget(self, category: CostCategory, amount: float) -> None:
        with self._lock:
            self._budgets[category] = amount

    def get_total_cost(self, category: Optional[CostCategory] = None,
                       start: Optional[datetime] = None,
                       end: Optional[datetime] = None) -> float:
        with self._lock:
            entries = list(self._entries)
        if category:
            entries = [e for e in entries if e.category == category]
        if start:
            entries = [e for e in entries if e.timestamp >= start]
        if end:
            entries = [e for e in entries if e.timestamp <= end]
        return sum(e.amount for e in entries)

    def get_cost_by_category(self) -> Dict[str, float]:
        with self._lock:
            entries = list(self._entries)
        by_category = defaultdict(float)
        for e in entries:
            by_category[e.category.name] += e.amount
        return dict(by_category)

    def get_cost_by_resource(self) -> Dict[str, float]:
        with self._lock:
            entries = list(self._entries)
        by_resource = defaultdict(float)
        for e in entries:
            key = f"{e.resource_type}:{e.resource_id}" if e.resource_id else e.resource_type
            by_resource[key] += e.amount
        return dict(by_resource)

    def get_budget_status(self) -> Dict[str, Any]:
        with self._lock:
            budgets = dict(self._budgets)
        status = {}
        for cat, budget in budgets.items():
            spent = self.get_total_cost(cat)
            status[cat.name] = {
                "budget": budget,
                "spent": round(spent, 2),
                "remaining": round(budget - spent, 2),
                "utilization": round(spent / budget * 100, 2) if budget > 0 else 0,
            }
        return status

    def get_cost_report(self) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._entries)
        total = sum(e.amount for e in entries)
        by_category = self.get_cost_by_category()
        return {
            "total_cost": round(total, 2),
            "total_entries": len(entries),
            "by_category": by_category,
            "avg_cost_per_entry": round(total / max(len(entries), 1), 4),
        }

    def get_entries(self, category: Optional[CostCategory] = None,
                    limit: int = 100) -> List[CostEntry]:
        with self._lock:
            entries = list(self._entries)
        if category:
            entries = [e for e in entries if e.category == category]
        return entries[-limit:]

# =============================================================================
# DATA MIGRATION PLANNER
# =============================================================================

class DataMigrationPlanner:
    def __init__(self):
        self._plans: Dict[str, MigrationPlan] = {}
        self._step_log: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def create_plan(self, plan_id: str, name: str, source_system: str,
                    target_system: str, tables: Optional[List[str]] = None,
                    estimated_hours: float = 0.0, owner: str = "",
                    priority: int = 0) -> MigrationPlan:
        plan = MigrationPlan(
            plan_id=plan_id, name=name,
            source_system=source_system, target_system=target_system,
            tables=tables or [], estimated_duration_hours=estimated_hours,
            owner=owner, priority=priority,
        )
        with self._lock:
            self._plans[plan_id] = plan
        logger.info("Created migration plan %s: %s", plan_id, name)
        return plan

    def start_migration(self, plan_id: str) -> Dict[str, Any]:
        with self._lock:
            plan = self._plans.get(plan_id)
            if not plan:
                return {"error": "Plan not found"}
            plan.status = MigrationStatus.IN_PROGRESS
            plan.started_at = datetime.now()
        return {"plan_id": plan_id, "status": "started"}

    def complete_migration(self, plan_id: str, rows_migrated: int) -> Dict[str, Any]:
        with self._lock:
            plan = self._plans.get(plan_id)
            if not plan:
                return {"error": "Plan not found"}
            plan.status = MigrationStatus.COMPLETED
            plan.completed_at = datetime.now()
            plan.rows_migrated = rows_migrated
            if plan.started_at:
                delta = plan.completed_at - plan.started_at
                plan.actual_duration_hours = delta.total_seconds() / 3600
        return {"plan_id": plan_id, "status": "completed", "rows_migrated": rows_migrated}

    def fail_migration(self, plan_id: str, error: str) -> Dict[str, Any]:
        with self._lock:
            plan = self._plans.get(plan_id)
            if not plan:
                return {"error": "Plan not found"}
            plan.status = MigrationStatus.FAILED
            plan.errors.append(error)
        return {"plan_id": plan_id, "status": "failed", "error": error}

    def rollback_migration(self, plan_id: str) -> Dict[str, Any]:
        with self._lock:
            plan = self._plans.get(plan_id)
            if not plan:
                return {"error": "Plan not found"}
            plan.status = MigrationStatus.ROLLED_BACK
        return {"plan_id": plan_id, "status": "rolled_back"}

    def get_plan(self, plan_id: str) -> Optional[MigrationPlan]:
        with self._lock:
            return self._plans.get(plan_id)

    def get_all_plans(self) -> List[MigrationPlan]:
        with self._lock:
            return list(self._plans.values())

    def get_plans_by_status(self, status: MigrationStatus) -> List[MigrationPlan]:
        with self._lock:
            return [p for p in self._plans.values() if p.status == status]

    def get_migration_stats(self) -> Dict[str, Any]:
        with self._lock:
            plans = list(self._plans.values())
        by_status = defaultdict(int)
        total_rows = 0
        for p in plans:
            by_status[p.status.name] += 1
            total_rows += p.rows_migrated
        return {
            "total_plans": len(plans),
            "by_status": dict(by_status),
            "total_rows_migrated": total_rows,
            "avg_duration_hours": round(
                statistics.mean([p.actual_duration_hours for p in plans
                                 if p.actual_duration_hours > 0]) if plans else 0, 2
            ),
        }

# =============================================================================
# COLUMN LINEAGE TRACKER
# =============================================================================

class ColumnLineageTracker:
    def __init__(self):
        self._lineages: Dict[str, ColumnLineage] = {}
        self._by_target: Dict[str, List[str]] = defaultdict(list)
        self._by_source: Dict[str, List[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add_column_lineage(self, lineage_id: str, source_table: str,
                           source_column: str, target_table: str,
                           target_column: str, transformation: str = "",
                           description: str = "") -> ColumnLineage:
        lineage = ColumnLineage(
            lineage_id=lineage_id, source_table=source_table,
            source_column=source_column, target_table=target_table,
            target_column=target_column, transformation=transformation,
            description=description,
        )
        with self._lock:
            self._lineages[lineage_id] = lineage
            src_key = f"{source_table}.{source_column}"
            tgt_key = f"{target_table}.{target_column}"
            self._by_source[src_key].append(lineage_id)
            self._by_target[tgt_key].append(lineage_id)
        return lineage

    def get_column_upstream(self, table: str, column: str) -> List[ColumnLineage]:
        key = f"{table}.{column}"
        with self._lock:
            lineage_ids = self._by_target.get(key, [])
            return [self._lineages[lid] for lid in lineage_ids if lid in self._lineages]

    def get_column_downstream(self, table: str, column: str) -> List[ColumnLineage]:
        key = f"{table}.{column}"
        with self._lock:
            lineage_ids = self._by_source.get(key, [])
            return [self._lineages[lid] for lid in lineage_ids if lid in self._lineages]

    def trace_full_path(self, table: str, column: str, max_depth: int = 10) -> List[Dict[str, Any]]:
        path: List[Dict[str, Any]] = []
        visited: Set[str] = set()
        queue = [(table, column)]
        for _ in range(min(max_depth, MAX_LINEAGE_DEPTH)):
            next_queue = []
            for t, c in queue:
                key = f"{t}.{c}"
                if key in visited:
                    continue
                visited.add(key)
                downstream = self.get_column_downstream(t, c)
                for dl in downstream:
                    path.append({
                        "source": f"{dl.source_table}.{dl.source_column}",
                        "target": f"{dl.target_table}.{dl.target_column}",
                        "transformation": dl.transformation,
                    })
                    next_queue.append((dl.target_table, dl.target_column))
            queue = next_queue
        return path

    def get_lineage(self, lineage_id: str) -> Optional[ColumnLineage]:
        with self._lock:
            return self._lineages.get(lineage_id)

    def get_all_lineages(self) -> List[ColumnLineage]:
        with self._lock:
            return list(self._lineages.values())

    def delete_lineage(self, lineage_id: str) -> bool:
        with self._lock:
            if lineage_id in self._lineages:
                lineage = self._lineages[lineage_id]
                src_key = f"{lineage.source_table}.{lineage.source_column}"
                tgt_key = f"{lineage.target_table}.{lineage.target_column}"
                self._by_source[src_key] = [lid for lid in self._by_source[src_key] if lid != lineage_id]
                self._by_target[tgt_key] = [lid for lid in self._by_target[tgt_key] if lid != lineage_id]
                del self._lineages[lineage_id]
                return True
        return False

    def get_column_lineage_stats(self) -> Dict[str, Any]:
        with self._lock:
            lineages = list(self._lineages.values())
        unique_sources = set(f"{l.source_table}.{l.source_column}" for l in lineages)
        unique_targets = set(f"{l.target_table}.{l.target_column}" for l in lineages)
        return {
            "total_lineages": len(lineages),
            "unique_source_columns": len(unique_sources),
            "unique_target_columns": len(unique_targets),
            "avg_transformations_per_target": round(
                len(lineages) / max(len(unique_targets), 1), 2
            ),
        }

# =============================================================================
# CONFIG
# =============================================================================

class Config:
    def __init__(self, default_storage: StorageType = StorageType.RELATIONAL_DB,
                 quality_check_interval: str = "daily",
                 lineage_depth: int = MAX_LINEAGE_DEPTH,
                 enable_cdc: bool = True,
                 enable_column_lineage: bool = True,
                 enable_cost_tracking: bool = True,
                 enable_partitioning: bool = True,
                 enable_masking: bool = True,
                 enable_retention: bool = True,
                 enable_schema_registry: bool = True,
                 enable_dependency_graph: bool = True,
                 enable_migration_planner: bool = True):
        self.default_storage = default_storage
        self.quality_check_interval = quality_check_interval
        self.lineage_depth = lineage_depth
        self.enable_cdc = enable_cdc
        self.enable_column_lineage = enable_column_lineage
        self.enable_cost_tracking = enable_cost_tracking
        self.enable_partitioning = enable_partitioning
        self.enable_masking = enable_masking
        self.enable_retention = enable_retention
        self.enable_schema_registry = enable_schema_registry
        self.enable_dependency_graph = enable_dependency_graph
        self.enable_migration_planner = enable_migration_planner

# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class DataArchitectureAgent:
    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._model_manager = DataModelManager()
        self._integration_manager = IntegrationManager()
        self._mdm_manager = MDMManager()
        self._catalog = DataCatalog(self._model_manager)
        self._quality_manager = DataQualityManager()
        self._lineage = DataLineage()
        self._governance = GovernanceManager()
        self._schema_registry = SchemaRegistry(self._model_manager)
        self._partitioner = DataPartitioner()
        self._masking_engine = DataMaskingEngine()
        self._dependency_graph = DependencyGraphBuilder()
        self._retention_manager = DataRetentionManager()
        self._cost_tracker = CostTracker()
        self._migration_planner = DataMigrationPlanner()
        self._column_lineage = ColumnLineageTracker()
        self._running = False
        self._started_at: Optional[datetime] = None
        self._lock = threading.Lock()

    def initialize(self) -> Dict[str, Any]:
        logger.info("Initializing DataArchitectureAgent")
        self._running = True
        self._started_at = datetime.now()
        return {"status": "initialized", "config": {
            "default_storage": self._config.default_storage.name,
            "quality_interval": self._config.quality_check_interval,
            "lineage_depth": self._config.lineage_depth,
            "column_lineage": self._config.enable_column_lineage,
            "cost_tracking": self._config.enable_cost_tracking,
            "partitioning": self._config.enable_partitioning,
            "masking": self._config.enable_masking,
            "retention": self._config.enable_retention,
            "schema_registry": self._config.enable_schema_registry,
            "dependency_graph": self._config.enable_dependency_graph,
            "migration_planner": self._config.enable_migration_planner,
        }}

    def shutdown(self) -> Dict[str, Any]:
        self._running = False
        logger.info("DataArchitectureAgent shutdown complete")
        return {"status": "shutdown"}

    # --- Model operations ---

    def create_model(self, model_id: str, name: str, model_type: ModelType,
                     description: str = "", owner: str = "",
                     tags: Optional[List[str]] = None) -> Dict[str, Any]:
        model = self._model_manager.create_model(model_id, name, model_type, description, owner, tags)
        return {"model_id": model.model_id, "name": name, "type": model_type.name}

    def create_table(self, table_id: str, name: str, fields: Optional[List[DataField]] = None,
                     storage_type: StorageType = StorageType.RELATIONAL_DB,
                     domain: DataDomain = DataDomain.CUSTOM,
                     owner: str = "") -> Dict[str, Any]:
        table = self._model_manager.create_table(table_id, name, fields=fields,
                                                  storage_type=storage_type, domain=domain, owner=owner)
        return {"table_id": table.table_id, "name": name, "storage": storage_type.name,
                "fields": len(fields or [])}

    def add_field(self, table_id: str, field_id: str, name: str, data_type: DataType,
                  nullable: bool = True, primary_key: bool = False,
                  pii_flag: bool = False) -> Dict[str, Any]:
        field = DataField(field_id=field_id, name=name, data_type=data_type,
                          nullable=nullable, primary_key=primary_key, pii_flag=pii_flag)
        success = self._model_manager.add_field(table_id, field)
        return {"added": success, "table_id": table_id, "field": name}

    # --- Pipeline operations ---

    def create_pipeline(self, pipeline_id: str, name: str, source: str,
                        destination: str, pattern: IntegrationPattern,
                        schedule: str = "") -> Dict[str, Any]:
        pipeline = self._integration_manager.create_pipeline(
            pipeline_id, name, source, destination, pattern, schedule,
        )
        return {"pipeline_id": pipeline.pipeline_id, "name": name, "pattern": pattern.name}

    def run_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        return self._integration_manager.run_pipeline(pipeline_id)

    # --- MDM operations ---

    def create_mdm_record(self, entity_type: str, attributes: Dict[str, Any],
                          source_id: str = "") -> Dict[str, Any]:
        record = self._mdm_manager.create_record(entity_type, attributes, source_id)
        return {"record_id": record.record_id, "golden_id": record.golden_id}

    def merge_mdm_records(self, record_id_1: str, record_id_2: str,
                          strategy: str = "r1_priority") -> Dict[str, Any]:
        merged = self._mdm_manager.merge_records(record_id_1, record_id_2, strategy)
        if not merged:
            return {"error": "Merge failed"}
        return {"merged_id": merged.record_id, "sources": merged.source_ids, "strategy": strategy}

    # --- Catalog operations ---

    def add_metadata(self, entity_type: str, entity_id: str, key: str, value: Any) -> Dict[str, Any]:
        entry = self._catalog.add_metadata(entity_type, entity_id, key, value)
        return {"entry_id": entry.entry_id, "key": key}

    def search_catalog(self, query: str, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        results = self._catalog.search(query, entity_type)
        return [{"entity_type": e.entity_type, "entity_id": e.entity_id,
                 "key": e.key, "value": e.value} for e in results]

    # --- Quality operations ---

    def create_quality_rule(self, rule_id: str, name: str, rule_type: QualityRuleType,
                            table_id: str, threshold: float = 99.0,
                            severity: str = "warning") -> Dict[str, Any]:
        rule = self._quality_manager.create_rule(rule_id, name, rule_type, table_id,
                                                  threshold=threshold, severity=severity)
        return {"rule_id": rule.rule_id, "name": name, "type": rule_type.name}

    def run_quality_checks(self) -> Dict[str, Any]:
        results = self._quality_manager.run_all_checks()
        passed = sum(1 for r in results if r.passed)
        return {"total": len(results), "passed": passed, "failed": len(results) - passed}

    def get_quality_dashboard(self) -> Dict[str, Any]:
        return self._quality_manager.get_quality_dashboard()

    # --- Lineage operations ---

    def add_lineage_node(self, node_id: str, name: str, node_type: LineageNodeType,
                         **kwargs) -> Dict[str, Any]:
        node = self._lineage.add_node(node_id, name, node_type, **kwargs)
        return {"node_id": node.node_id, "name": name, "type": node_type.name}

    def add_lineage_edge(self, source: str, target: str,
                         edge_type: str = "data_flow") -> Dict[str, Any]:
        edge = self._lineage.add_edge(source, target, edge_type)
        return {"edge_id": edge.edge_id, "source": source, "target": target}

    def get_lineage_impact(self, node_id: str) -> Dict[str, Any]:
        return self._lineage.get_impact_analysis(node_id)

    # --- Governance operations ---

    def create_governance_policy(self, rule_id: str, name: str,
                                  policy_type: GovernancePolicy,
                                  enforcement_level: str = "advisory") -> Dict[str, Any]:
        rule = self._governance.create_policy(rule_id, name, policy_type,
                                               enforcement_level=enforcement_level)
        return {"rule_id": rule.rule_id, "name": name, "type": policy_type.name}

    def log_audit(self, event_type: str, entity_type: str, entity_id: str,
                  user: str, details: str = "") -> Dict[str, Any]:
        self._governance.log_audit_event(event_type, entity_type, entity_id, user, details)
        return {"logged": True, "event_type": event_type}

    # --- Schema registry operations ---

    def register_schema(self, table_id: str, schema: Dict[str, Any],
                        created_by: str = "") -> Dict[str, Any]:
        version = self._schema_registry.register_schema(table_id, schema, created_by)
        return {"version_id": version.version_id, "version": version.version_number}

    def check_schema_compatibility(self, table_id: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        return self._schema_registry.check_compatibility(table_id, schema)

    # --- Partitioning operations ---

    def create_partition(self, config_id: str, table_id: str,
                         strategy: PartitionStrategy,
                         partition_count: int = DEFAULT_PARTITION_COUNT) -> Dict[str, Any]:
        config = self._partitioner.create_partition_config(config_id, table_id, strategy,
                                                            partition_count=partition_count)
        return {"config_id": config.config_id, "strategy": strategy.name,
                "partitions": partition_count}

    # --- Masking operations ---

    def create_masking_rule(self, rule_id: str, name: str, table_id: str,
                            field_id: str, masking_type: MaskingType) -> Dict[str, Any]:
        rule = self._masking_engine.create_rule(rule_id, name, table_id, field_id, masking_type)
        return {"rule_id": rule.rule_id, "type": masking_type.name}

    def mask_data(self, table_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        return self._masking_engine.apply_rules_to_record(table_id, record)

    # --- Dependency graph operations ---

    def add_dependency_node(self, node_id: str, entity_type: str, entity_id: str,
                            name: str, dependency_type: DependencyType) -> Dict[str, Any]:
        node = self._dependency_graph.add_node(node_id, entity_type, entity_id, name, dependency_type)
        return {"node_id": node.node_id, "type": dependency_type.name}

    def add_dependency_edge(self, source: str, target: str) -> Dict[str, Any]:
        success = self._dependency_graph.add_dependency(source, target)
        return {"added": success, "source": source, "target": target}

    def get_dependency_order(self) -> List[str]:
        return self._dependency_graph.topological_sort()

    # --- Retention operations ---

    def create_retention_rule(self, rule_id: str, table_id: str,
                              action: RetentionAction,
                              retention_days: int = 365) -> Dict[str, Any]:
        record = self._retention_manager.create_retention_rule(rule_id, table_id, action, retention_days)
        return {"record_id": record.record_id, "action": action.name, "retention_days": retention_days}

    # --- Cost tracking ---

    def record_cost(self, category: CostCategory, amount: float,
                    description: str = "") -> Dict[str, Any]:
        entry = self._cost_tracker.record_cost(category, amount, description)
        return {"entry_id": entry.entry_id, "amount": amount, "category": category.name}

    def get_cost_report(self) -> Dict[str, Any]:
        return self._cost_tracker.get_cost_report()

    # --- Migration operations ---

    def create_migration_plan(self, plan_id: str, name: str, source: str,
                              target: str, tables: Optional[List[str]] = None,
                              estimated_hours: float = 0.0) -> Dict[str, Any]:
        plan = self._migration_planner.create_plan(plan_id, name, source, target,
                                                    tables, estimated_hours)
        return {"plan_id": plan.plan_id, "status": plan.status.name}

    # --- Column lineage operations ---

    def add_column_lineage(self, lineage_id: str, source_table: str, source_column: str,
                           target_table: str, target_column: str,
                           transformation: str = "") -> Dict[str, Any]:
        lineage = self._column_lineage.add_column_lineage(lineage_id, source_table,
                                                           source_column, target_table,
                                                           target_column, transformation)
        return {"lineage_id": lineage.lineage_id,
                "path": f"{source_table}.{source_column} -> {target_table}.{target_column}"}

    # --- Aggregate stats ---

    def get_model_summary(self) -> Dict[str, Any]:
        return self._model_manager.get_model_summary()

    def get_pipeline_stats(self) -> Dict[str, Any]:
        return self._integration_manager.get_all_pipeline_stats()

    def get_mdm_stats(self) -> Dict[str, Any]:
        return self._mdm_manager.get_mdm_stats()

    def get_governance_summary(self) -> Dict[str, Any]:
        return self._governance.get_governance_summary()

    def get_catalog_stats(self) -> Dict[str, Any]:
        return self._catalog.get_catalog_stats()

    def get_lineage_stats(self) -> Dict[str, Any]:
        return self._lineage.get_lineage_stats()

    def get_dependency_stats(self) -> Dict[str, Any]:
        return self._dependency_graph.get_graph_stats()

    def get_retention_stats(self) -> Dict[str, Any]:
        return self._retention_manager.get_retention_stats()

    def get_masking_stats(self) -> Dict[str, Any]:
        return self._masking_engine.get_masking_stats()

    def get_migration_stats(self) -> Dict[str, Any]:
        return self._migration_planner.get_migration_stats()

    def get_column_lineage_stats(self) -> Dict[str, Any]:
        return self._column_lineage.get_column_lineage_stats()

    def get_status(self) -> Dict[str, Any]:
        uptime = 0.0
        if self._started_at:
            uptime = (datetime.now() - self._started_at).total_seconds()
        return {
            "agent": "DataArchitectureAgent",
            "running": self._running,
            "uptime_seconds": round(uptime, 1),
            "models": len(self._model_manager.get_all_models()),
            "tables": len(self._model_manager.get_all_tables()),
            "pipelines": len(self._integration_manager.get_all_pipelines()),
            "quality_rules": len(self._quality_manager.get_all_rules()),
            "lineage_nodes": len(self._lineage.get_all_nodes()),
            "governance_policies": len(self._governance.get_policies_by_type(GovernancePolicy.DATA_CLASSIFICATION)) + len(self._governance.get_policies_by_type(GovernancePolicy.ACCESS_CONTROL)),
            "dependency_nodes": len(self._dependency_graph.get_all_nodes()),
            "retention_rules": len(self._retention_manager.get_due_rules()),
            "masking_rules": len(self._masking_engine.get_rules_for_table("")),
            "migration_plans": len(self._migration_planner.get_all_plans()),
            "column_lineages": len(self._column_lineage.get_all_lineages()),
        }

    def get_full_report(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": self.get_status(),
            "model_summary": self.get_model_summary(),
            "quality_dashboard": self.get_quality_dashboard(),
            "mdm_stats": self.get_mdm_stats(),
            "lineage_stats": self.get_lineage_stats(),
            "governance_summary": self.get_governance_summary(),
            "catalog_stats": self.get_catalog_stats(),
            "dependency_stats": self.get_dependency_stats(),
            "retention_stats": self.get_retention_stats(),
            "masking_stats": self.get_masking_stats(),
            "cost_report": self.get_cost_report(),
            "migration_stats": self.get_migration_stats(),
            "column_lineage_stats": self.get_column_lineage_stats(),
        }

# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    print("=" * 60)
    print("  Data Architecture Agent - Comprehensive Demo")
    print("=" * 60)
    agent = DataArchitectureAgent(Config())
    status = agent.initialize()
    print(f"Initialized with {len(status['config'])} features enabled")

    model = agent.create_model("model_001", "Customer Domain", ModelType.LOGICAL,
                               "Customer data model", owner="data_team")
    print(f"Created model: {model['name']}")

    fields = [
        DataField("f1", "customer_id", DataType.UUID, nullable=False, primary_key=True),
        DataField("f2", "name", DataType.STRING, max_length=255, pii_flag=True,
                  masking_type=MaskingType.PARTIAL, classification="pii"),
        DataField("f3", "email", DataType.STRING, max_length=255, pii_flag=True,
                  masking_type=MaskingType.HASH, classification="pii"),
        DataField("f4", "created_at", DataType.DATETIME),
        DataField("f5", "revenue", DataType.DECIMAL, precision=10, scale=2),
    ]
    table = agent.create_table("tbl_customers", "customers", fields, domain=DataDomain.CUSTOMER,
                               owner="data_team")
    print(f"Created table: {table['name']} with {table['fields']} fields")

    pipeline = agent.create_pipeline("pipe_001", "ETL Customers", "source_db",
                                     "data_warehouse", IntegrationPattern.ETL,
                                     schedule="0 2 * * *")
    result = agent.run_pipeline("pipe_001")
    print(f"Pipeline run: {result['status']} ({result['records_processed']} records)")

    record = agent.create_mdm_record("customer",
                                     {"name": "Acme Corp", "email": "info@acme.com"})
    print(f"MDM record: {record['golden_id']}")

    record2 = agent.create_mdm_record("customer",
                                      {"name": "Acme Corporation", "email": "info@acme.com"})
    merged = agent.merge_mdm_records(record["record_id"], record2["record_id"],
                                     strategy="highest_quality")
    print(f"Merge: {merged.get('strategy', 'failed')}")

    agent.add_quality_rule("qr_001", "Email Not Null", QualityRuleType.NOT_NULL,
                           "tbl_customers", 100.0, severity="critical")
    quality = agent.run_quality_checks()
    print(f"Quality: {quality['passed']}/{quality['total']} passed")

    agent.add_lineage_node("src_customers", "Source: Customers", LineageNodeType.SOURCE)
    agent.add_lineage_node("tfm_customers", "Transform: Clean", LineageNodeType.TRANSFORMATION)
    agent.add_lineage_node("dim_customers", "Dim: Customers", LineageNodeType.DESTINATION)
    agent.add_lineage_edge("src_customers", "tfm_customers")
    agent.add_lineage_edge("tfm_customers", "dim_customers")

    agent.create_governance_policy("gov_001", "Data Classification",
                                   GovernancePolicy.DATA_CLASSIFICATION,
                                   enforcement_level="mandatory")
    agent.log_audit("read", "table", "tbl_customers", "analyst_001")

    agent.register_schema("tbl_customers", {"fields": {"customer_id": "UUID", "name": "STRING"}},
                          created_by="data_engineer")
    compat = agent.check_schema_compatibility("tbl_customers",
                                               {"fields": {"customer_id": "UUID", "name": "STRING",
                                                           "email": "STRING"}})
    print(f"Schema compatibility: {compat['compatible']}")

    agent.create_partition("part_001", "tbl_customers", PartitionStrategy.HASH, 8)
    agent.create_masking_rule("mask_001", "Mask Name", "tbl_customers", "f2", MaskingType.PARTIAL)
    masked = agent.mask_data("tbl_customers", {"name": "John Doe", "email": "john@test.com"})
    print(f"Masked name: {masked['name']}")

    agent.add_dependency_node("dep_001", "table", "tbl_customers", "customers", DependencyType.TABLE_DEPENDS_ON)
    agent.add_dependency_node("dep_002", "pipeline", "pipe_001", "ETL Customers", DependencyType.PIPELINE_FEEDS)
    agent.add_dependency_edge("dep_002", "dep_001")
    order = agent.get_dependency_order()
    print(f"Dependency order: {len(order)} nodes")

    agent.create_retention_rule("ret_001", "tbl_customers", RetentionAction.ARCHIVE, 730)
    agent.record_cost(CostCategory.COMPUTE, 150.0, "Daily compute cost")
    agent.record_cost(CostCategory.STORAGE, 75.0, "Monthly storage")
    agent.create_migration_plan("mig_001", "Migrate to Cloud", "on_prem_db", "cloud_warehouse",
                                ["tbl_customers"], estimated_hours=4.0)
    agent.add_column_lineage("cl_001", "source_db", "cust_name", "tbl_customers", "name",
                             transformation="UPPER()")

    summary = agent.get_model_summary()
    print(f"Summary: {summary['total_models']} models, {summary['total_tables']} tables, "
          f"{summary.get('pii_fields_count', 0)} PII fields")

    report = agent.get_full_report()
    print(f"\nReport generated at {report['timestamp']}")
    print(f"Status: {report['status']['running']}")
    print(f"Cost report: ${report['cost_report']['total_cost']}")

    agent.shutdown()
    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
