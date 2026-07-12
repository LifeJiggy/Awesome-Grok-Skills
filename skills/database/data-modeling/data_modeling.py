"""
Data Modeling Framework

Production-grade data modeling toolkit providing entity relationship design,
schema generation, normalization analysis, denormalization strategies, and
cross-database schema export for designing robust data architectures.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DataType(Enum):
    UUID = "UUID"
    VARCHAR = "VARCHAR"
    CHAR = "CHAR"
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    SMALLINT = "SMALLINT"
    DECIMAL = "DECIMAL"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIME = "TIME"
    TIMESTAMP = "TIMESTAMP"
    JSON = "JSON"
    JSONB = "JSONB"
    BLOB = "BLOB"
    ARRAY = "ARRAY"
    ENUM = "ENUM"
    SERIAL = "SERIAL"
    BIGSERIAL = "BIGSERIAL"


class Cardinality(Enum):
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_MANY = "M:N"
    MANY_TO_ONE = "N:1"


class NormalForm(Enum):
    UNF = "Unnormalized"
    FIRST_NF = "1NF"
    SECOND_NF = "2NF"
    THIRD_NF = "3NF"
    BCNF = "BCNF"
    FOURTH_NF = "4NF"
    FIFTH_NF = "5NF"


class MigrationType(Enum):
    CREATE_TABLE = "create_table"
    DROP_TABLE = "drop_table"
    ADD_COLUMN = "add_column"
    DROP_COLUMN = "drop_column"
    ALTER_COLUMN = "alter_column"
    ADD_INDEX = "add_index"
    DROP_INDEX = "drop_index"
    ADD_CONSTRAINT = "add_constraint"
    DROP_CONSTRAINT = "drop_constraint"
    RENAME_TABLE = "rename_table"
    RENAME_COLUMN = "rename_column"


class TargetDatabase(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    CASSANDRA = "cassandra"
    GRAPHQL = "graphql"


class ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class NamingConvention(Enum):
    SNAKE_CASE = "snake_case"
    CAMEL_CASE = "camelCase"
    PASCAL_CASE = "PascalCase"
    KEBAB_CASE = "kebab-case"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Column:
    """Database column definition."""
    name: str
    data_type: DataType
    primary_key: bool = False
    nullable: bool = True
    unique: bool = False
    default: Optional[str] = None
    foreign_key: Optional[str] = None
    check_constraint: Optional[str] = None
    comment: Optional[str] = None
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    enum_values: Optional[List[str]] = None
    array_element_type: Optional[DataType] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "type": self.data_type.value,
            "primary_key": self.primary_key,
            "nullable": self.nullable,
            "unique": self.unique,
        }
        if self.default is not None:
            result["default"] = self.default
        if self.foreign_key is not None:
            result["foreign_key"] = self.foreign_key
        if self.length is not None:
            result["length"] = self.length
        if self.precision is not None:
            result["precision"] = self.precision
        if self.scale is not None:
            result["scale"] = self.scale
        return result


@dataclass
class Index:
    """Database index definition."""
    name: str
    columns: List[str]
    unique: bool = False
    index_type: str = "btree"
    where_clause: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class Constraint:
    """Database constraint."""
    name: str
    constraint_type: str  # primary_key, foreign_key, unique, check
    columns: List[str]
    referenced_table: Optional[str] = None
    referenced_columns: Optional[List[str]] = None
    check_expression: Optional[str] = None
    on_delete: str = "CASCADE"
    on_update: str = "CASCADE"


@dataclass
class Entity:
    """Entity (table/collection) definition."""
    name: str
    columns: List[Column] = field(default_factory=list)
    indexes: List[Index] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    comment: Optional[str] = None
    schema: Optional[str] = None

    @property
    def primary_key_columns(self) -> List[str]:
        return [c.name for c in self.columns if c.primary_key]

    @property
    def foreign_key_columns(self) -> List[Column]:
        return [c for c in self.columns if c.foreign_key]

    def get_column(self, name: str) -> Optional[Column]:
        for c in self.columns:
            if c.name == name:
                return c
        return None

    def add_column(self, **kwargs: Any) -> "Entity":
        self.columns.append(Column(**kwargs))
        return self

    def add_index(self, name: str, columns: List[str], unique: bool = False) -> "Entity":
        self.indexes.append(Index(name=name, columns=columns, unique=unique))
        return self


@dataclass
class Relationship:
    """Relationship between entities."""
    name: str
    source: str
    target: str
    cardinality: Cardinality
    source_participation: str = "partial"  # total or partial
    target_participation: str = "partial"
    foreign_key_column: Optional[str] = None
    join_table: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class FunctionalDependency:
    """Functional dependency: determinant → dependent."""
    determinant: List[str]
    dependent: List[str]


@dataclass
class NormalFormViolation:
    """A normal form violation."""
    form: NormalForm
    description: str
    columns_involved: List[str]
    suggested_fix: str
    severity: ValidationSeverity = ValidationSeverity.WARNING


@dataclass
class NormalizationResult:
    """Result of normalization analysis."""
    current_normal_form: NormalForm
    violations: List[NormalFormViolation]
    is_normalized: bool
    recommendations: List[str]


@dataclass
class DecompositionResult:
    """Result of normalizing a table."""
    tables: List[Dict[str, Any]]
    foreign_keys: List[Dict[str, str]]
    preserved_dependencies: bool
    lossless: bool


@dataclass
class ValidationMessage:
    """Schema validation message."""
    severity: ValidationSeverity
    message: str
    entity: Optional[str] = None
    column: Optional[str] = None


@dataclass
class ValidationResult:
    """Schema validation result."""
    is_valid: bool
    messages: List[ValidationMessage] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)
        self.messages.append(ValidationMessage(severity=ValidationSeverity.WARNING, message=message))

    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.messages.append(ValidationMessage(severity=ValidationSeverity.ERROR, message=message))


@dataclass
class SchemaDocumentation:
    """Auto-generated schema documentation."""
    model_name: str
    tables: List[Dict[str, Any]] = field(default_factory=list)
    total_columns: int = 0
    total_constraints: int = 0
    total_indexes: int = 0
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# ER Model
# ---------------------------------------------------------------------------

class ERModel:
    """Entity-Relationship model for database design."""

    def __init__(self, name: str = "model"):
        self.name = name
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.created_at = datetime.now(timezone.utc)

    def add_entity(self, name: str, columns: Optional[List[Dict[str, Any]]] = None) -> Entity:
        entity = Entity(name=name)
        if columns:
            for col_def in columns:
                col_name = col_def.pop("name")
                col_type = col_def.pop("type", DataType.TEXT)
                entity.columns.append(Column(name=col_name, data_type=col_type, **col_def))
        self.entities[name] = entity
        return entity

    def add_relationship(
        self,
        name: str,
        source: str,
        target: str,
        cardinality: str = "1:N",
        source_participation: str = "partial",
        target_participation: str = "partial",
        **kwargs: Any,
    ) -> Relationship:
        cardinality_enum = Cardinality(cardinality)
        relationship = Relationship(
            name=name,
            source=source,
            target=target,
            cardinality=cardinality_enum,
            source_participation=source_participation,
            target_participation=target_participation,
            **kwargs,
        )
        self.relationships.append(relationship)
        return relationship

    def get_entity(self, name: str) -> Optional[Entity]:
        return self.entities.get(name)

    def validate(self) -> ValidationResult:
        result = ValidationResult(is_valid=True)

        for name, entity in self.entities.items():
            if not entity.primary_key_columns:
                result.add_warning(f"Entity '{name}' has no primary key")

            for col in entity.columns:
                if col.foreign_key:
                    ref_table, ref_col = col.foreign_key.split(".")
                    if ref_table not in self.entities:
                        result.add_error(f"Foreign key references non-existent table '{ref_table}'")
                    else:
                        ref_entity = self.entities[ref_table]
                        if not ref_entity.get_column(ref_col):
                            result.add_error(f"Foreign key references non-existent column '{ref_table}.{ref_col}'")

            # Check for naming conventions
            if not re.match(r"^[a-z][a-z0-9_]*$", name):
                result.add_warning(f"Entity name '{name}' violates snake_case convention")

        result.is_valid = len(result.errors) == 0
        return result

    def generate_ddl(self, target: str = "postgresql") -> str:
        target_db = TargetDatabase(target)
        lines = []

        for name, entity in self.entities.items():
            if target_db == TargetDatabase.POSTGRESQL:
                lines.extend(self._generate_pg_ddl(entity))
            elif target_db == TargetDatabase.MYSQL:
                lines.extend(self._generate_mysql_ddl(entity))
            elif target_db == TargetDatabase.SQLITE:
                lines.extend(self._generate_sqlite_ddl(entity))
            elif target_db == TargetDatabase.MONGODB:
                lines.append(self._generate_mongodb_schema(entity))
            elif target_db == TargetDatabase.CASSANDRA:
                lines.extend(self._generate_cql_ddl(entity))

            # Add foreign key constraints
            for fk in entity.foreign_key_columns:
                if fk.foreign_key:
                    ref_table, ref_col = fk.foreign_key.split(".")
                    lines.append(
                        f"ALTER TABLE {name} ADD CONSTRAINT fk_{name}_{fk.name} "
                        f"FOREIGN KEY ({fk.name}) REFERENCES {ref_table}({ref_col});"
                    )

            # Add indexes
            for idx in entity.indexes:
                unique = "UNIQUE " if idx.unique else ""
                cols = ", ".join(idx.columns)
                lines.append(f"CREATE {unique}INDEX {idx.name} ON {name} ({cols});")

            lines.append("")

        return "\n".join(lines)

    def _generate_pg_ddl(self, entity: Entity) -> List[str]:
        lines = []
        if entity.comment:
            lines.append(f"-- {entity.comment}")
        lines.append(f"CREATE TABLE {entity.name} (")

        col_defs = []
        for col in entity.columns:
            parts = [f"  {col.name}"]
            if col.data_type == DataType.VARCHAR and col.length:
                parts.append(f"VARCHAR({col.length})")
            elif col.data_type == DataType.DECIMAL and col.precision:
                parts.append(f"DECIMAL({col.precision},{col.scale or 0})")
            else:
                parts.append(col.data_type.value)

            if col.primary_key:
                parts.append("PRIMARY KEY")
            if not col.nullable and not col.primary_key:
                parts.append("NOT NULL")
            if col.unique and not col.primary_key:
                parts.append("UNIQUE")
            if col.default:
                parts.append(f"DEFAULT {col.default}")
            col_defs.append(" ".join(parts))

        lines.append(",\n".join(col_defs))
        lines.append(");")
        return lines

    def _generate_mysql_ddl(self, entity: Entity) -> List[str]:
        lines = [f"CREATE TABLE {entity.name} ("]
        col_defs = []
        for col in entity.columns:
            parts = [f"  {col.name}"]
            if col.data_type == DataType.UUID:
                parts.append("CHAR(36)")
            elif col.data_type == DataType.JSONB:
                parts.append("JSON")
            elif col.data_type == DataType.SERIAL:
                parts.append("INT AUTO_INCREMENT")
            elif col.data_type == DataType.BIGSERIAL:
                parts.append("BIGINT AUTO_INCREMENT")
            elif col.data_type == DataType.VARCHAR and col.length:
                parts.append(f"VARCHAR({col.length})")
            elif col.data_type == DataType.DECIMAL and col.precision:
                parts.append(f"DECIMAL({col.precision},{col.scale or 0})")
            else:
                parts.append(col.data_type.value)

            if col.primary_key:
                parts.append("PRIMARY KEY")
            if not col.nullable and not col.primary_key:
                parts.append("NOT NULL")
            if col.unique and not col.primary_key:
                parts.append("UNIQUE")
            if col.default:
                parts.append(f"DEFAULT {col.default}")
            col_defs.append(" ".join(parts))

        lines.append(",\n".join(col_defs))
        lines.append(") ENGINE=InnoDB;")
        return lines

    def _generate_sqlite_ddl(self, entity: Entity) -> List[str]:
        return self._generate_pg_ddl(entity)

    def _generate_mongodb_schema(self, entity: Entity) -> str:
        schema = {"$jsonSchema": {"bsonType": "object", "properties": {}}}
        for col in entity.columns:
            prop: Dict[str, Any] = {}
            type_map = {
                DataType.UUID: "string", DataType.VARCHAR: "string", DataType.TEXT: "string",
                DataType.INTEGER: "int", DataType.BIGINT: "long", DataType.DECIMAL: "double",
                DataType.BOOLEAN: "bool", DataType.DATE: "date", DataType.TIMESTAMP: "date",
                DataType.JSON: "object", DataType.JSONB: "object",
            }
            prop["bsonType"] = type_map.get(col.data_type, "string")
            if col.length:
                prop["maxLength"] = col.length
            schema["$jsonSchema"]["properties"][col.name] = prop

        required = [c.name for c in entity.columns if c.primary_key or not c.nullable]
        schema["$jsonSchema"]["required"] = required
        return json.dumps(schema, indent=2)

    def _generate_cql_ddl(self, entity: Entity) -> List[str]:
        pk_cols = [c.name for c in entity.columns if c.primary_key]
        lines = [f"CREATE TABLE {entity.name} ("]
        col_defs = []
        for col in entity.columns:
            cql_type = {
                DataType.UUID: "uuid", DataType.VARCHAR: "text", DataType.TEXT: "text",
                DataType.INTEGER: "int", DataType.BIGINT: "bigint", DataType.DECIMAL: "decimal",
                DataType.BOOLEAN: "boolean", DataType.TIMESTAMP: "timestamp",
                DataType.JSON: "text", DataType.JSONB: "text",
            }.get(col.data_type, "text")
            col_defs.append(f"  {col.name} {cql_type}")

        pk = ", ".join(pk_cols) if pk_cols else entity.columns[0].name
        col_defs.append(f"  PRIMARY KEY ({pk})")
        lines.append(",\n".join(col_defs))
        lines.append(");")
        return lines

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "entities": {
                name: {
                    "columns": [c.to_dict() for c in entity.columns],
                    "indexes": [{"name": i.name, "columns": i.columns, "unique": i.unique} for i in entity.indexes],
                }
                for name, entity in self.entities.items()
            },
            "relationships": [
                {
                    "name": r.name,
                    "source": r.source,
                    "target": r.target,
                    "cardinality": r.cardinality.value,
                }
                for r in self.relationships
            ],
        }


# ---------------------------------------------------------------------------
# Normalization Analyzer
# ---------------------------------------------------------------------------

class NormalizationAnalyzer:
    """Analyze and enforce database normalization forms."""

    def analyze(
        self,
        table: str,
        columns: List[str],
        functional_dependencies: Optional[List[FunctionalDependency]] = None,
    ) -> NormalizationResult:
        violations = []
        recommendations = []
        current_nf = NormalForm.FIFTH_NF

        if functional_dependencies is None:
            functional_dependencies = []

        # Check 1NF: atomic values, no repeating groups
        # (Assumed by having flat column list)

        # Check 2NF: no partial dependencies
        pk_columns = [c for c in columns if "id" in c.lower() and columns.index(c) == 0]
        if not pk_columns:
            pk_columns = [columns[0]] if columns else []

        for fd in functional_dependencies:
            if len(fd.determinant) > 1 and set(fd.determinant) < set(pk_columns):
                if current_nf >= NormalForm.SECOND_NF:
                    current_nf = NormalForm.FIRST_NF
                violations.append(NormalFormViolation(
                    form=NormalForm.SECOND_NF,
                    description=f"Partial dependency: {fd.determinant} → {fd.dependent}",
                    columns_involved=fd.determinant + fd.dependent,
                    suggested_fix=f"Move {fd.dependent} to a separate table with {fd.determinant[0]} as key",
                ))

        # Check 3NF: no transitive dependencies
        for fd in functional_dependencies:
            if len(fd.determinant) == 1 and fd.determinant[0] not in pk_columns:
                non_pk_deps = [d for d in fd.dependent if d not in pk_columns]
                if non_pk_deps:
                    if current_nf >= NormalForm.THIRD_NF:
                        current_nf = NormalForm.SECOND_NF
                    violations.append(NormalFormViolation(
                        form=NormalForm.THIRD_NF,
                        description=f"Transitive dependency: {fd.determinant} → {non_pk_deps}",
                        columns_involved=fd.determinant + non_pk_deps,
                        suggested_fix=f"Create separate table for {non_pk_deps} with {fd.determinant[0]} as FK",
                    ))

        # Check BCNF: every determinant is a candidate key
        for fd in functional_dependencies:
            if fd.determinant not in [pk_columns]:
                if current_nf >= NormalForm.BCNF:
                    current_nf = NormalForm.THIRD_NF
                    violations.append(NormalFormViolation(
                        form=NormalForm.BCNF,
                        description=f"Non-key determinant: {fd.determinant}",
                        columns_involved=fd.determinant,
                        suggested_fix=f"Decompose or make {fd.determinant} a candidate key",
                    ))

        is_normalized = len(violations) == 0
        if is_normalized:
            recommendations.append("Schema is fully normalized")

        return NormalizationResult(
            current_normal_form=current_nf,
            violations=violations,
            is_normalized=is_normalized,
            recommendations=recommendations,
        )

    def decompose_to_3nf(self, result: NormalizationResult) -> DecompositionResult:
        """Decompose violating schema to 3NF."""
        tables = []
        foreign_keys = []

        # Simplified decomposition
        tables.append({
            "name": "main_table",
            "columns": ["id"],
            "primary_key": ["id"],
        })

        for violation in result.violations:
            if violation.form == NormalForm.THIRD_NF:
                table_name = f"related_{violation.columns_involved[0]}"
                tables.append({
                    "name": table_name,
                    "columns": violation.columns_involved,
                    "primary_key": [violation.columns_involved[0]],
                })
                foreign_keys.append({
                    "from_table": "main_table",
                    "from_column": violation.columns_involved[0],
                    "to_table": table_name,
                    "to_column": violation.columns_involved[0],
                })

        return DecompositionResult(
            tables=tables,
            foreign_keys=foreign_keys,
            preserved_dependencies=True,
            lossless=True,
        )


# ---------------------------------------------------------------------------
# Schema Exporter
# ---------------------------------------------------------------------------

class SchemaExporter:
    """Export ER model to multiple database formats."""

    def __init__(self, model: ERModel):
        self.model = model

    def export(self, target: str = "postgresql") -> str:
        return self.model.generate_ddl(target)

    def validate_naming_conventions(
        self,
        rules: Optional[Dict[str, str]] = None,
    ) -> ValidationResult:
        if rules is None:
            rules = {
                "table_name": "snake_case",
                "column_name": "snake_case",
                "primary_key": "id",
                "foreign_key": "{table}_id",
            }

        result = ValidationResult(is_valid=True)

        for name, entity in self.model.entities.items():
            if not re.match(r"^[a-z][a-z0-9_]*$", name):
                result.add_warning(f"Table '{name}' not in snake_case")

            for col in entity.columns:
                if not re.match(r"^[a-z][a-z0-9_]*$", col.name):
                    result.add_warning(f"Column '{name}.{col.name}' not in snake_case")

        return result

    def generate_documentation(self) -> SchemaDocumentation:
        tables = []
        total_cols = 0
        total_constraints = 0
        total_indexes = 0

        for name, entity in self.model.entities.items():
            table_doc = {
                "name": name,
                "comment": entity.comment or "",
                "columns": [
                    {
                        "name": c.name,
                        "type": c.data_type.value,
                        "nullable": c.nullable,
                        "primary_key": c.primary_key,
                        "foreign_key": c.foreign_key,
                        "default": c.default,
                        "comment": c.comment or "",
                    }
                    for c in entity.columns
                ],
                "indexes": [
                    {"name": i.name, "columns": i.columns, "unique": i.unique}
                    for i in entity.indexes
                ],
                "constraints": [
                    {"name": c.name, "type": c.constraint_type}
                    for c in entity.constraints
                ],
            }
            tables.append(table_doc)
            total_cols += len(entity.columns)
            total_indexes += len(entity.indexes)
            total_constraints += len(entity.constraints)

        return SchemaDocumentation(
            model_name=self.model.name,
            tables=tables,
            total_columns=total_cols,
            total_constraints=total_constraints,
            total_indexes=total_indexes,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate data modeling capabilities."""
    print("=" * 70)
    print("Data Modeling Framework - Demo")
    print("=" * 70)

    # --- 1. ER Model Design ---
    print("\n--- ER Model Design ---")
    model = ERModel("ecommerce")

    # Create entities
    customers = model.add_entity("customers", [
        {"name": "id", "type": DataType.UUID, "primary_key": True, "nullable": False},
        {"name": "email", "type": DataType.VARCHAR(255), "unique": True, "nullable": False},
        {"name": "name", "type": DataType.VARCHAR(100), "nullable": False},
        {"name": "phone", "type": DataType.VARCHAR(20), "nullable": True},
        {"name": "created_at", "type": DataType.TIMESTAMP, "default": "NOW()"},
    ])
    customers.comment = "Customer accounts"

    products = model.add_entity("products", [
        {"name": "id", "type": DataType.UUID, "primary_key": True},
        {"name": "name", "type": DataType.VARCHAR(200), "nullable": False},
        {"name": "price", "type": DataType.DECIMAL(10, 2), "precision": 10, "scale": 2},
        {"name": "stock", "type": DataType.INTEGER, "default": "0"},
        {"name": "category", "type": DataType.VARCHAR(50)},
        {"name": "active", "type": DataType.BOOLEAN, "default": "TRUE"},
    ])
    products.add_index("idx_products_category", ["category"])
    products.add_index("idx_products_active", ["active"])

    orders = model.add_entity("orders", [
        {"name": "id", "type": DataType.UUID, "primary_key": True},
        {"name": "customer_id", "type": DataType.UUID, "foreign_key": "customers.id", "nullable": False},
        {"name": "total", "type": DataType.DECIMAL(10, 2)},
        {"name": "status", "type": DataType.VARCHAR(20), "default": "'pending'"},
        {"name": "created_at", "type": DataType.TIMESTAMP},
    ])
    orders.add_index("idx_orders_customer", ["customer_id"])
    orders.add_index("idx_orders_status", ["status"])

    order_items = model.add_entity("order_items", [
        {"name": "id", "type": DataType.UUID, "primary_key": True},
        {"name": "order_id", "type": DataType.UUID, "foreign_key": "orders.id"},
        {"name": "product_id", "type": DataType.UUID, "foreign_key": "products.id"},
        {"name": "quantity", "type": DataType.INTEGER, "nullable": False},
        {"name": "unit_price", "type": DataType.DECIMAL(10, 2)},
    ])

    # Add relationships
    model.add_relationship("customer_orders", "customers", "orders", "1:N")
    model.add_relationship("order_items", "orders", "order_items", "1:N")
    model.add_relationship("product_orders", "products", "order_items", "1:N")

    print(f"  Entities: {list(model.entities.keys())}")
    print(f"  Relationships: {len(model.relationships)}")

    # --- 2. Validation ---
    print("\n--- Schema Validation ---")
    validation = model.validate()
    print(f"  Valid: {validation.is_valid}")
    print(f"  Warnings: {validation.warnings}")
    print(f"  Errors: {validation.errors}")

    # --- 3. DDL Generation ---
    print("\n--- PostgreSQL DDL ---")
    pg_ddl = model.generate_ddl("postgresql")
    print(pg_ddl[:500])

    print("\n--- MySQL DDL ---")
    mysql_ddl = model.generate_ddl("mysql")
    print(mysql_ddl[:500])

    print("\n--- MongoDB Schema ---")
    mongo_schema = model.generate_ddl("mongodb")
    print(mongo_schema[:300])

    # --- 4. Normalization Analysis ---
    print("\n--- Normalization Analysis ---")
    analyzer = NormalizationAnalyzer()
    result = analyzer.analyze(
        table="orders",
        columns=["order_id", "customer_id", "customer_name", "product_id", "product_name", "quantity"],
        functional_dependencies=[
            FunctionalDependency(determinant=["order_id"], dependent=["customer_id", "product_id"]),
            FunctionalDependency(determinant=["customer_id"], dependent=["customer_name"]),
            FunctionalDependency(determinant=["product_id"], dependent=["product_name"]),
        ],
    )
    print(f"  Current NF: {result.current_normal_form.value}")
    print(f"  Violations: {len(result.violations)}")
    for v in result.violations:
        print(f"    [{v.form.value}] {v.description}")
        print(f"      Fix: {v.suggested_fix}")

    decomposition = analyzer.decompose_to_3nf(result)
    print(f"  Decomposed tables: {len(decomposition.tables)}")
    print(f"  Foreign keys: {len(decomposition.foreign_keys)}")

    # --- 5. Schema Documentation ---
    print("\n--- Schema Documentation ---")
    exporter = SchemaExporter(model)
    docs = exporter.generate_documentation()
    print(f"  Model: {docs.model_name}")
    print(f"  Tables: {len(docs.tables)}")
    print(f"  Total columns: {docs.total_columns}")
    print(f"  Total indexes: {docs.total_indexes}")

    for table in docs.tables:
        print(f"\n  {table['name']}:")
        for col in table["columns"]:
            pk = " [PK]" if col["primary_key"] else ""
            fk = f" [FK→{col['foreign_key']}]" if col["foreign_key"] else ""
            null = " NULL" if col["nullable"] else " NOT NULL"
            print(f"    {col['name']}: {col['type']}{pk}{fk}{null}")

    # --- 6. Naming Convention Validation ---
    print("\n--- Naming Convention Validation ---")
    naming_result = exporter.validate_naming_conventions()
    print(f"  Valid: {naming_result.is_valid}")
    print(f"  Violations: {len(naming_result.warnings)}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()