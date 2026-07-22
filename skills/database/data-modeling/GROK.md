---
name: "Data Modeling"
version: "2.0.0"
description: "Comprehensive data modeling toolkit with entity relationship design, schema generation, normalization analysis, denormalization strategies, and database-specific schema export for relational and NoSQL databases"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database", "data-modeling", "ER-diagram", "normalization", "schema-design", "relational", "nosql"]
category: "database"
personality: "data-architect"
use_cases: ["ER diagram design", "schema generation", "normalization", "denormalization", "cross-database modeling"]
---

# Data Modeling

> Production-grade data modeling framework providing entity relationship design, schema generation, normalization analysis, denormalization strategies, and multi-database schema export for designing robust data architectures.

## Overview

The Data Modeling module provides a complete toolkit for designing, analyzing, and deploying database schemas. It implements entity-relationship diagram construction, normalization form analysis (1NF through 5NF/BCNF), denormalization strategy recommendations, schema diffing and versioning, cross-database schema export (PostgreSQL, MySQL, MongoDB, Cassandra), and schema documentation generation. Every model includes validation, constraint analysis, and migration-ready DDL output.

## Core Capabilities

### 1. Entity-Relationship Design
- Visual ER diagram construction with entities, attributes, and relationships
- Cardinality specification (1:1, 1:N, M:N)
- Participation constraints (total/partial)
- Weak entity and aggregation support
- Inheritance/polymorphic relationships

### 2. Schema Generation
- DDL generation for PostgreSQL, MySQL, SQLite
- MongoDB schema validation rules
- Cassandra CQL table definitions
- GraphQL type definitions
- OpenAPI/JSON Schema for API contracts

### 3. Normalization Analysis
- First Normal Form (1NF) validation
- Second Normal Form (2NF) check
- Third Normal Form (3NF) analysis
- Boyce-Codd Normal Form (BCNF) verification
- Fourth and Fifth Normal Form checks
- Functional dependency discovery

### 4. Denormalization Strategies
- Materialized view recommendations
- Aggregate table suggestions
- Cache column generation
- Read-replica optimization hints
- Time-series denormalization patterns

### 5. Schema Migration
- Forward and backward migration generation
- Schema diff between versions
- Data migration scripts
- Constraint addition/removal
- Index creation scripts

### 6. Documentation and Validation
- Auto-generated schema documentation
- Constraint description and business rules
- Data dictionary export
- Schema compliance checking
- Naming convention enforcement

## Usage Examples

### Entity-Relationship Design

```python
from data_modeling import ERModel, Entity, Relationship, DataType

model = ERModel(name="ecommerce_schema")

# Define entities
customer = model.add_entity("customers", [
    {"name": "id", "type": DataType.UUID, "primary_key": True},
    {"name": "email", "type": DataType.VARCHAR(255), "unique": True, "nullable": False},
    {"name": "name", "type": DataType.VARCHAR(100), "nullable": False},
    {"name": "created_at", "type": DataType.TIMESTAMP, "default": "NOW()"},
])

order = model.add_entity("orders", [
    {"name": "id", "type": DataType.UUID, "primary_key": True},
    {"name": "customer_id", "type": DataType.UUID, "foreign_key": "customers.id"},
    {"name": "total", "type": DataType.DECIMAL(10, 2), "nullable": False},
    {"name": "status", "type": DataType.ENUM(["pending", "active", "completed"])},
    {"name": "created_at", "type": DataType.TIMESTAMP},
])

# Define relationships
model.add_relationship(
    name="customer_orders",
    source="customers",
    target="orders",
    cardinality="1:N",
    source_participation="total",
    target_participation="partial",
)

# Validate and generate DDL
validation = model.validate()
print(f"Valid: {validation.is_valid}")
print(f"Warnings: {validation.warnings}")

ddl = model.generate_ddl(target="postgresql")
print(ddl)
```

### Normalization Analysis

```python
from data_modeling import NormalizationAnalyzer

analyzer = NormalizationAnalyzer()

# Analyze a table for normal form violations
result = analyzer.analyze(
    table="orders",
    columns=["order_id", "customer_id", "customer_name", "customer_email",
             "product_id", "product_name", "product_price", "quantity", "total"],
    functional_dependencies=[
        {"determinant": ["order_id"], "dependent": ["customer_id", "total"]},
        {"determinant": ["customer_id"], "dependent": ["customer_name", "customer_email"]},
        {"determinant": ["product_id"], "dependent": ["product_name", "product_price"]},
        {"determinant": ["order_id", "product_id"], "dependent": ["quantity"]},
    ],
)

print(f"Current NF: {result.current_normal_form}")
print(f"Violations: {len(result.violations)}")
for v in result.violations:
    print(f"  {v.form}: {v.description}")
    print(f"    Fix: {v.suggested_fix}")

# Decompose to 3NF
decomposition = analyzer.decompose_to_3nf(result)
for table in decomposition.tables:
    print(f"  Table: {table.name}")
    print(f"    Columns: {table.columns}")
    print(f"    Primary key: {table.primary_key}")
```

### Schema Documentation

```python
from data_modeling import SchemaDocumentation

doc = SchemaDocumentation(model)

# Generate complete documentation
docs = doc.generate(
    format="markdown",
    include_constraints=True,
    include_indexes=True,
    include_examples=True,
)

print(docs)

# Export as data dictionary
dictionary = doc.export_data_dictionary()
print(f"Tables: {len(dictionary.tables)}")
print(f"Total columns: {dictionary.total_columns}")
print(f"Total constraints: {dictionary.total_constraints}")
```

### Cross-Database Schema Export

```python
from data_modeling import SchemaExporter

exporter = SchemaExporter(model)

# Export for different databases
postgresql_ddl = exporter.export(target="postgresql")
mysql_ddl = exporter.export(target="mysql")
mongodb_schema = exporter.export(target="mongodb")
cassandra_cql = exporter.export(target="cassandra")

# Validate against naming conventions
validation = exporter.validate_naming_conventions(
    rules={
        "table_name": "snake_case",
        "column_name": "snake_case",
        "primary_key": "id",
        "foreign_key": "{table}_id",
    }
)
print(f"Naming violations: {len(validation.violations)}")
```

## Best Practices

### Entity Design
- Use meaningful entity and attribute names (customers, not tbl1)
- Always include primary keys — prefer surrogate keys (UUID/serial) over natural keys
- Add created_at and updated_at timestamps to all entities
- Use ENUM types for columns with a fixed set of values

### Normalization
- Target 3NF for most OLTP databases — it balances integrity and performance
- Denormalize selectively for read-heavy tables (analytics, reporting)
- Document denormalization decisions — future developers need to understand the tradeoff
- Check for transitive dependencies (A→B→C means A and C should not be in the same table)

### Naming Conventions
- Use snake_case for table and column names
- Pluralize table names (customers, orders)
- Use singular for column names (customer_id, not customer_ids)
- Prefix foreign key columns with the referenced table name
- Avoid reserved words (select, order, group)

### Schema Migration
- Never modify production schemas manually — always use migrations
- Make migrations reversible (always provide up and down)
- Test migrations against production-sized data before deploying
- Add indexes concurrently to avoid table locks

## Related Modules

- **database-administration**: Schema management and migration execution
- **query-optimization**: Index design based on query patterns
- **mongodb**: NoSQL-specific document modeling patterns
- **replication**: Schema considerations for replicated databases

---

## Advanced Configuration

### Complex Entity Relationships

```python
from data_modeling import ERModel, Entity, Relationship, DataType

model = ERModel(name="enterprise_schema")

# Multi-tenant organization hierarchy
tenant = model.add_entity("tenants", [
    {"name": "id", "type": DataType.UUID, "primary_key": True},
    {"name": "name", "type": DataType.VARCHAR(100), "nullable": False},
    {"name": "parent_id", "type": DataType.UUID, "foreign_key": "tenants.id"},
    {"name": "level", "type": DataType.INTEGER, "default": 0},
])

# Polymorphic associations
content = model.add_entity("content", [
    {"name": "id", "type": DataType.UUID, "primary_key": True},
    {"name": "content_type", "type": DataType.ENUM(["article", "video", "podcast"])},
    {"name": "title", "type": DataType.VARCHAR(255)},
    {"name": "body", "type": DataType.TEXT},
    {"name": "metadata", "type": DataType.JSONB},
])

# Many-to-many with attributes
model.add_relationship(
    name="content_tags",
    source="content",
    target="tags",
    cardinality="M:N",
    attributes=[
        {"name": "added_by", "type": DataType.UUID},
        {"name": "added_at", "type": DataType.TIMESTAMP},
    ],
)
```

### Inheritance Patterns

```python
# Class Table Inheritance
payment = model.add_entity("payments", [
    {"name": "id", "type": DataType.UUID, "primary_key": True},
    {"name": "amount", "type": DataType.DECIMAL(10, 2)},
    {"name": "currency", "type": DataType.VARCHAR(3)},
    {"name": "created_at", "type": DataType.TIMESTAMP},
])

credit_card = model.add_entity("credit_card_payments", [
    {"name": "payment_id", "type": DataType.UUID, "primary_key": True, "foreign_key": "payments.id"},
    {"name": "card_last_four", "type": DataType.VARCHAR(4)},
    {"name": "card_brand", "type": DataType.ENUM(["visa", "mastercard", "amex"])},
])

bank_transfer = model.add_entity("bank_transfers", [
    {"name": "payment_id", "type": DataType.UUID, "primary_key": True, "foreign_key": "payments.id"},
    {"name": "bank_name", "type": DataType.VARCHAR(100)},
    {"name": "routing_number", "type": DataType.VARCHAR(9)},
    {"name": "account_last_four", "type": DataType.VARCHAR(4)},
])
```

### Temporal Data Patterns

```python
# Bi-temporal data model
model.add_entity("product_prices", [
    {"name": "id", "type": DataType.UUID, "primary_key": True},
    {"name": "product_id", "type": DataType.UUID, "foreign_key": "products.id"},
    {"name": "price", "type": DataType.DECIMAL(10, 2)},
    {"name": "valid_from", "type": DataType.TIMESTAMP, "description": "Business time start"},
    {"name": "valid_to", "type": DataType.TIMESTAMP, "description": "Business time end"},
    {"name": "recorded_at", "type": DataType.TIMESTAMP, "description": "System time recorded"},
    {"name": "expired_at", "type": DataType.TIMESTAMP, "description": "System time expired"},
])
```

## Architecture Patterns

### Star Schema (Data Warehouse)

```
                    ┌─────────────────┐
                    │  dim_date       │
                    ├─────────────────┤
                    │ date_key (PK)   │
                    │ date            │
                    │ year            │
                    │ month           │
                    │ day             │
                    │ quarter         │
                    │ is_weekend      │
                    └────────┬────────┘
                             │
┌─────────────────┐         │         ┌─────────────────┐
│  dim_product    │         │         │  dim_customer   │
├─────────────────┤         │         ├─────────────────┤
│ product_key(PK) │◄────────┼─────────│ customer_key(PK)│
│ product_name    │         │         │ customer_name   │
│ category        │         │         │ segment         │
│ brand           │         │         │ region          │
└────────┬────────┘         │         └────────┬────────┘
         │                  │                  │
         └──────────┬───────┴───────┬──────────┘
                    │               │
              ┌─────┴─────┐        │
              │fact_sales │        │
              ├───────────┤        │
              │ date_key  │◄───────┘
              │product_key│
              │customer_key│
              │ quantity   │
              │ amount     │
              └───────────┘
```

### Data Vault Pattern

```
┌─────────────────┐
│  hub_customer   │
├─────────────────┤
│ customer_hk (PK)│
│ customer_bk     │
│ load_date       │
│ record_source   │
└────────┬────────┘
         │
         │
┌────────┴────────┐
│  link_customer_ │
│     order       │
├─────────────────┤
│ link_hk (PK)    │
│ customer_hk (FK)│
│ order_hk (FK)   │
│ load_date       │
│ record_source   │
└─────────────────┘
         │
┌────────┴────────┐
│  sat_order      │
│     details     │
├─────────────────┤
│ order_hk (FK)   │
│ load_date       │
│ load_end_date   │
│ amount          │
│ status          │
│ record_source   │
└─────────────────┘
```

### Event Sourcing Pattern

```
┌─────────────────┐
│   events        │
├─────────────────┤
│ event_id (PK)   │
│ aggregate_id    │
│ aggregate_type  │
│ event_type      │
│ event_data (JSON)│
│ metadata (JSON) │
│ version         │
│ created_at      │
└─────────────────┘

┌─────────────────┐
│   snapshots     │
├─────────────────┤
│ snapshot_id (PK)│
│ aggregate_id    │
│ aggregate_type  │
│ state (JSON)    │
│ version         │
│ created_at      │
└─────────────────┘
```

## Integration Guide

### ORM Integration

```python
# SQLAlchemy integration
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(String(36), primary_key=True)
    customer_id = Column(String(36), ForeignKey('customers.id'), nullable=False)
    total = Column(Integer, nullable=False)
    
    customer = relationship("Customer", back_populates="orders")
```

### GraphQL Schema Generation

```python
from data_modeling import GraphQLGenerator

generator = GraphQLGenerator(model)

# Generate GraphQL types
graphql_schema = generator.generate()
print(graphql_schema)

# Output:
# type Customer {
#   id: ID!
#   email: String!
#   name: String!
#   orders: [Order!]!
# }
#
# type Order {
#   id: ID!
#   customer: Customer!
#   total: Float!
#   status: OrderStatus!
# }
#
# enum OrderStatus {
#   PENDING
#   COMPLETED
#   CANCELLED
# }
```

### OpenAPI Schema Export

```python
from data_modeling import OpenAPIGenerator

api_generator = OpenAPIGenerator(model)

# Generate OpenAPI 3.0 schema
openapi_schema = api_generator.generate(
    title="E-commerce API",
    version="1.0.0",
    include_crud=True,
    include_pagination=True,
    include_filtering=True,
)

# Export as YAML or JSON
api_generator.export_yaml("openapi.yaml")
api_generator.export_json("openapi.json")
```

## Performance Optimization

### Index Design Patterns

```sql
-- Composite index for common query patterns
CREATE INDEX idx_orders_customer_status 
ON orders(customer_id, status, created_at DESC);

-- Partial index for filtered queries
CREATE INDEX idx_active_users 
ON users(email) 
WHERE deleted_at IS NULL;

-- Covering index for index-only scans
CREATE INDEX idx_products_category_price 
ON products(category_id, price) 
INCLUDE (name, description);

-- GIN index for JSONB queries
CREATE INDEX idx_metadata_gin 
ON products USING gin(metadata);
```

### Query Optimization

```sql
-- Use EXPLAIN ANALYZE to analyze query performance
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders 
WHERE customer_id = '123' 
AND status = 'active' 
ORDER BY created_at DESC 
LIMIT 10;

-- Analyze index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Find missing indexes
SELECT
    relname AS table_name,
    seq_scan,
    seq_tup_read,
    idx_scan,
    CASE WHEN seq_scan > 0 THEN seq_tup_read / seq_scan ELSE 0 END AS avg_seq_tup
FROM pg_stat_user_tables
WHERE seq_scan > 100
ORDER BY seq_tup_read DESC;
```

## Security Considerations

### Column-Level Security

```sql
-- Create schema for sensitive data
CREATE SCHEMA sensitive;

-- Move sensitive columns to separate table
CREATE TABLE sensitive.customer_pii (
    customer_id UUID PRIMARY KEY REFERENCES customers(id),
    email VARCHAR(255),
    phone VARCHAR(20),
    ssn VARCHAR(11),
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Grant limited access
GRANT SELECT ON sensitive.customer_pii TO app_readonly;
REVOKE ALL ON sensitive.customer_pii FROM app_readonly;
GRANT SELECT (customer_id, email) ON sensitive.customer_pii TO app_readonly;
```

### Data Classification

```python
from data_modeling import DataClassifier, SensitivityLevel

classifier = DataClassifier(model)

# Classify columns by sensitivity
classifications = classifier.classify()
for table, columns in classifications.items():
    for col, level in columns.items():
        print(f"{table}.{col}: {level.value}")

# Output:
# customers.email: CONFIDENTIAL
# customers.ssn: RESTRICTED
# orders.total: INTERNAL
# products.name: PUBLIC
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Circular dependencies | Migration fails | Use nullable foreign keys or junction tables |
| N+1 query problem | Slow API responses | Use eager loading or batch queries |
| Missing indexes | Full table scans | Analyze query patterns, add appropriate indexes |
| Data redundancy | Inconsistent data | Normalize to 3NF, use foreign keys |
| Large table joins | Poor query performance | Denormalize, add materialized views |

### Schema Validation

```python
from data_modeling import SchemaValidator

validator = SchemaValidator(model)

# Validate naming conventions
naming_issues = validator.validate_naming(
    rules={
        "table": "snake_case_plural",
        "column": "snake_case_singular",
        "primary_key": "id",
        "foreign_key": "{table}_id",
    }
)

# Validate data types
type_issues = validator.validate_types()

# Validate relationships
relationship_issues = validator.validate_relationships()

for issue in naming_issues + type_issues + relationship_issues:
    print(f"[{issue.severity}] {issue.message}")
```

## API Reference

### ERModel

```python
class ERModel:
    def __init__(self, name: str)
    def add_entity(self, name: str, columns: list[dict]) -> Entity
    def add_relationship(self, name: str, source: str, target: str, cardinality: str, **kwargs)
    def validate(self) -> ValidationResult
    def generate_ddl(self, target: str) -> str
    def to_dict(self) -> dict
    def from_dict(self, data: dict) -> ERModel
    def diff(self, other: ERModel) -> SchemaDiff
```

### NormalizationAnalyzer

```python
class NormalizationAnalyzer:
    def __init__(self)
    def analyze(self, table: str, columns: list[str], functional_dependencies: list[dict]) -> NormalFormResult
    def decompose_to_3nf(self, result: NormalFormResult) -> DecompositionResult
    def decompose_to_bcnf(self, result: NormalFormResult) -> DecompositionResult
    def find_candidate_keys(self, columns: list[str], dependencies: list[dict]) -> list[list[str]]
    def check_lossless_join(self, decomposition: DecompositionResult) -> bool
    def check_dependency_preservation(self, decomposition: DecompositionResult, dependencies: list[dict]) -> bool
```

### SchemaExporter

```python
class SchemaExporter:
    def __init__(self, model: ERModel)
    def export(self, target: str) -> str
    def export_postgresql(self) -> str
    def export_mysql(self) -> str
    def export_mongodb(self) -> dict
    def export_cassandra(self) -> str
    def export_graphql(self) -> str
    def validate_naming_conventions(self, rules: dict) -> ValidationResult
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class DataType(Enum):
    UUID = "uuid"
    VARCHAR = "varchar"
    TEXT = "text"
    INTEGER = "integer"
    BIGINT = "bigint"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    DATE = "date"
    JSON = "json"
    JSONB = "jsonb"
    ENUM = "enum"
    ARRAY = "array"

class Cardinality(Enum):
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:N"
    MANY_TO_MANY = "M:N"

class NormalForm(Enum):
    UNNORMALIZED = 0
    FIRST_NF = 1
    SECOND_NF = 2
    THIRD_NF = 3
    BCNF = 4
    FOURTH_NF = 5
    FIFTH_NF = 6

@dataclass
class Column:
    name: str
    type: DataType
    primary_key: bool = False
    nullable: bool = True
    unique: bool = False
    default: Optional[str] = None
    foreign_key: Optional[str] = None
    description: Optional[str] = None

@dataclass
class Entity:
    name: str
    columns: List[Column]
    description: Optional[str] = None

@dataclass
class Relationship:
    name: str
    source: str
    target: str
    cardinality: Cardinality
    source_participation: str = "partial"
    target_participation: str = "partial"
    attributes: List[Column] = field(default_factory=list)

@dataclass
class FunctionalDependency:
    determinant: List[str]
    dependent: List[str]

@dataclass
class ValidationResult:
    is_valid: bool
    warnings: List[str]
    errors: List[str]
    suggestions: List[str]
```

## Deployment Guide

### Schema Migration Workflow

```bash
# Generate migration from model changes
python -m data_modeling.generate_migration \
  --model schema.json \
  --target postgresql \
  --output migrations/

# Validate migration
python -m data_modeling.validate_migration \
  --migration migrations/20240115_001_add_user_preferences.sql \
  --database test_db

# Apply migration
python -m data_modeling.apply_migration \
  --migration migrations/20240115_001_add_user_preferences.sql \
  --database production
```

### CI/CD Integration

```yaml
# .github/workflows/schema-validation.yml
name: Schema Validation

on:
  pull_request:
    paths:
      - 'schema/**'
      - 'migrations/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install data-modeling
        
      - name: Validate schema
        run: python -m data_modeling.validate --model schema.json
        
      - name: Check naming conventions
        run: python -m data_modeling.check_naming --rules rules.json
        
      - name: Generate migration diff
        run: python -m data_modeling.diff --base main --head ${{ github.sha }}
```

## Monitoring & Observability

### Schema Metrics

```python
from data_modeling import SchemaMetrics

metrics = SchemaMetrics(model)

# Collect schema statistics
stats = metrics.collect()
print(f"Total tables: {stats.table_count}")
print(f"Total columns: {stats.column_count}")
print(f"Total indexes: {stats.index_count}")
print(f"Total foreign keys: {stats.foreign_key_count}")

# Monitor schema changes
@metrics.on_change
def handle_schema_change(change):
    print(f"Schema change detected: {change.type} on {change.table}")
    print(f"Details: {change.description}")
```

### Data Quality Monitoring

```python
from data_modeling import DataQualityMonitor

monitor = DataQualityMonitor(model)

# Define quality rules
monitor.add_rule(
    name="email_format",
    table="customers",
    column="email",
    rule="REGEXP_LIKE(email, '^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$')"
)

monitor.add_rule(
    name="valid_dates",
    table="orders",
    column="created_at",
    rule="created_at <= NOW()"
)

# Run quality checks
results = monitor.check()
for rule, result in results.items():
    status = "PASS" if result.passed else "FAIL"
    print(f"[{status}] {rule}: {result.message}")
```

## Testing Strategy

### Unit Tests

```python
import pytest
from data_modeling import ERModel, DataType

@pytest.fixture
def model():
    model = ERModel(name="test_schema")
    model.add_entity("users", [
        {"name": "id", "type": DataType.UUID, "primary_key": True},
        {"name": "email", "type": DataType.VARCHAR(255), "unique": True},
    ])
    return model

def test_model_validation(model):
    result = model.validate()
    assert result.is_valid

def test_ddl_generation(model):
    ddl = model.generate_ddl(target="postgresql")
    assert "CREATE TABLE users" in ddl
    assert "id UUID PRIMARY KEY" in ddl
```

### Integration Tests

```python
@pytest.mark.integration
def test_schema_deployment():
    model = load_model("schema.json")
    exporter = SchemaExporter(model)
    
    # Generate DDL
    ddl = exporter.export(target="postgresql")
    
    # Deploy to test database
    with test_db.cursor() as cursor:
        cursor.execute(ddl)
    
    # Verify tables exist
    result = test_db.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    )
    tables = [row[0] for row in result]
    
    assert "users" in tables
    assert "orders" in tables
```

## Versioning & Migration

### Schema Versioning

```python
from data_modeling import SchemaVersionManager

version_manager = SchemaVersionManager(model)

# Check current version
current = version_manager.current_version()
print(f"Current schema version: {current}")

# Generate diff between versions
diff = version_manager.diff(
    from_version="1.0.0",
    to_version="2.0.0"
)

for change in diff.changes:
    print(f"{change.type}: {change.description}")
```

### Backward Compatibility

```python
# Check backward compatibility
compatibility = version_manager.check_compatibility(
    from_version="1.0.0",
    to_version="2.0.0"
)

print(f"Backward compatible: {compatibility.backward_compatible}")
print(f"Forward compatible: {compatibility.forward_compatible}")
for issue in compatibility.issues:
    print(f"  Issue: {issue}")
```

## Glossary

| Term | Definition |
|------|------------|
| **ER Diagram** | Entity-Relationship Diagram |
| **1NF** | First Normal Form - atomic values, no repeating groups |
| **2NF** | Second Normal Form - 1NF + no partial dependencies |
| **3NF** | Third Normal Form - 2NF + no transitive dependencies |
| **BCNF** | Boyce-Codd Normal Form - every determinant is a candidate key |
| **Surrogate Key** | System-generated unique identifier |
| **Natural Key** | Business-meaningful unique identifier |
| **Junction Table** | Table that resolves many-to-many relationships |
| **Star Schema** | Data warehouse schema with fact and dimension tables |
| **Data Vault** | Modeling technique for agile data warehousing |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added temporal data modeling support
- New Data Vault pattern support
- Improved normalization analysis
- Added GraphQL schema generation

### Version 2.5.0 (2023-12-01)
- Added Cassandra CQL export
- New schema documentation generator
- Improved naming convention validation
- Added data classification tools

### Version 2.0.0 (2023-09-15)
- Major API redesign
- Added multi-database support
- New denormalization recommendations
- Improved ER diagram generation

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/awesome-grok/data-modeling.git
cd data-modeling

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy .
```

### Code Style

- Follow PEP 8
- Use type hints for all public functions
- Write docstrings in Google style
- Keep functions under 40 lines
- Use dataclasses for data structures

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.