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