---
name: postgresql
category: database
version: 1.0.0
tags: [database, postgresql]
---

# Postgresql

## Overview
Comprehensive postgresql within database domain.

## Usage
```python
from postgresql import PostgreSQL
db = PostgreSQL()
```

## Advanced Configuration

### Connection Pool Configuration

```python
from postgresql import PostgreSQLConfig, PoolConfig

# Advanced PostgreSQL configuration
config = PostgreSQLConfig(
    host="localhost",
    port=5432,
    database="myapp",
    user="app_user",
    password="secure_password",
    pool=PoolConfig(
        min_connections=5,
        max_connections=50,
        idle_timeout=30000,
        max_lifetime=1800000,
        connection_timeout=10000,
    ),
    ssl={
        "enabled": True,
        "mode": "verify-full",
        "ca_cert": "/path/to/ca.pem",
        "client_cert": "/path/to/client.pem",
        "client_key": "/path/to/client.key",
    },
    application_name="myapp",
    options="-c statement_timeout=30000 -c lock_timeout=10000",
)

db = PostgreSQL(config=config)
```

### Replication Configuration

```python
from postgresql import ReplicationConfig, ReplicaConfig

# Advanced replication configuration
replication_config = ReplicationConfig(
    primary={
        "host": "primary.db.example.com",
        "port": 5432,
        "wal_level": "replica",
        "max_wal_senders": 10,
        "wal_keep_size": "1GB",
        "synchronous_standby_names": ["replica1"],
    },
    replicas=[
        ReplicaConfig(
            host="replica1.db.example.com",
            port=5432,
            primary_slot_name="replica1_slot",
            recovery_target_timeline="latest",
            hot_standby=True,
        ),
        ReplicaConfig(
            host="replica2.db.example.com",
            port=5432,
            primary_slot_name="replica2_slot",
            recovery_target_timeline="latest",
            hot_standby=True,
        ),
    ],
    replication_mode="synchronous",
    failover_strategy="automatic",
)

db = PostgreSQL(replication_config=replication_config)
```

### Performance Tuning Configuration

```python
from postgresql import PerformanceConfig, QueryTuning

# Advanced performance configuration
performance_config = PerformanceConfig(
    shared_buffers="4GB",
    effective_cache_size="12GB",
    work_mem="256MB",
    maintenance_work_mem="1GB",
    max_connections=200,
    max_parallel_workers_per_gather=4,
    max_parallel_workers=8,
    max_parallel_maintenance_workers=4,
    random_page_cost=1.1,
    effective_io_concurrency=200,
    checkpoint_completion_target=0.9,
    wal_buffers="64MB",
    max_wal_size="4GB",
    min_wal_size="1GB",
    query_tuning=QueryTuning(
        enable_seqscan=True,
        enable_indexscan=True,
        enable_hashjoin=True,
        enable_mergejoin=True,
        enable_nestloop=True,
    ),
)

db = PostgreSQL(performance_config=performance_config)
```

## Architecture Patterns

### Repository Pattern

```python
from postgresql import Repository, Base

class UserRepository(Repository):
    def __init__(self, db):
        self.db = db
        self.table = "users"
    
    def find_by_id(self, user_id):
        query = f"SELECT * FROM {self.table} WHERE id = $1"
        return self.db.fetch_one(query, user_id)
    
    def find_by_email(self, email):
        query = f"SELECT * FROM {self.table} WHERE email = $1"
        return self.db.fetch_one(query, email)
    
    def create(self, user_data):
        query = f"""
            INSERT INTO {self.table} (name, email, created_at)
            VALUES ($1, $2, NOW())
            RETURNING *
        """
        return self.db.fetch_one(query, user_data["name"], user_data["email"])
    
    def update(self, user_id, update_data):
        query = f"""
            UPDATE {self.table}
            SET name = $1, email = $2, updated_at = NOW()
            WHERE id = $3
            RETURNING *
        """
        return self.db.fetch_one(query, update_data["name"], update_data["email"], user_id)
    
    def delete(self, user_id):
        query = f"DELETE FROM {self.table} WHERE id = $1"
        return self.db.execute(query, user_id)
    
    def find_all(self, limit=100, offset=0):
        query = f"SELECT * FROM {self.table} LIMIT $1 OFFSET $2"
        return self.db.fetch_all(query, limit, offset)

# Usage
user_repo = UserRepository(db)
user = user_repo.find_by_id(1)
```

### Unit of Work Pattern

```python
from postgresql import UnitOfWork, Transaction

class OrderUnitOfWork(UnitOfWork):
    def __init__(self, db):
        super().__init__(db)
        self.orders = OrderRepository(db)
        self.items = OrderItemRepository(db)
        self.inventory = InventoryRepository(db)
    
    def commit(self):
        try:
            # Validate business rules
            self.validate_order()
            
            # Execute operations
            super().commit()
            
            # Publish events
            self.publish_events()
        except Exception as e:
            self.rollback()
            raise e
    
    def validate_order(self):
        # Check inventory
        for item in self.pending_items:
            stock = self.inventory.get_stock(item.product_id)
            if stock < item.quantity:
                raise InsufficientStockError(item.product_id)
    
    def publish_events(self):
        for event in self.pending_events:
            event_bus.publish(event)

# Usage
with OrderUnitOfWork(db) as uow:
    order = uow.orders.create(order_data)
    for item in items:
        uow.items.create({"order_id": order.id, **item})
        uow.inventory.decrement(item["product_id"], item["quantity"])
    # Auto-commit on successful exit
```

### Query Builder Pattern

```python
from postgresql import QueryBuilder

# Build complex queries
query = (
    QueryBuilder()
    .select("u.id", "u.name", "u.email", "o.id as order_id")
    .from_("users", "u")
    .join("orders", "o", "u.id = o.user_id", type_="LEFT")
    .where("u.created_at > $1", datetime(2024, 1, 1))
    .where("o.status = $2", "completed")
    .order_by("u.created_at", "DESC")
    .limit(100)
    .offset(0)
    .build()
)

print(f"SQL: {query.sql}")
print(f"Params: {query.params}")

# Execute
results = db.fetch_all(query.sql, *query.params)
```

## Integration Guide

### SQLAlchemy Integration

```python
from postgresql import SQLAlchemyIntegration, Model

# Define model
class User(Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Use with SQLAlchemy
integration = SQLAlchemyIntegration(config)
session = integration.create_session()

users = session.query(User).filter(User.created_at > datetime(2024, 1, 1)).all()
```

### Alembic Integration

```python
from postgresql import AlembicIntegration, MigrationConfig

# Configure Alembic
alembic_config = MigrationConfig(
    alembic_dir="migrations",
    script_location="migrations",
    sqlalchemy_url="postgresql://user:pass@localhost/myapp",
)

integration = AlembicIntegration(alembic_config)

# Generate migration
integration.generate_revision(message="add_users_table")

# Run migration
integration.upgrade("head")

# Rollback
integration.downgrade("-1")
```

## Performance Optimization

### Index Optimization

```python
from postgresql import IndexOptimizer

optimizer = IndexOptimizer(db)

# Analyze query performance
analysis = optimizer.analyze_query(
    query="SELECT * FROM users WHERE email = $1",
    params=["test@example.com"],
)

print(f"Execution time: {analysis.execution_time_ms:.2f}ms")
print(f"Index used: {analysis.index_used}")
print(f"Rows examined: {analysis.rows_examined}")

# Create recommended indexes
for index in analysis.recommended_indexes:
    optimizer.create_index(index)
    print(f"Created index: {index.name}")
```

### Query Optimization

```python
from postgresql import QueryOptimizer

optimizer = QueryOptimizer(db)

# Analyze slow queries
slow_queries = optimizer.find_slow_queries(
    threshold_ms=100,
    time_range_hours=24,
)

for query in slow_queries:
    print(f"Query: {query.sql[:100]}...")
    print(f"  Avg time: {query.avg_time_ms:.2f}ms")
    print(f"  Calls: {query.call_count}")
    print(f"  Recommendation: {query.recommendation}")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Connection Pool Exhaustion

**Symptom**: Too many connections error

**Solution**:
```python
# Increase pool size
config.pool.max_connections = 100

# Add connection monitoring
from postgresql import PoolMonitor
monitor = PoolMonitor(db)
monitor.check_connections()
```

#### 2. Slow Queries

**Symptom**: Query performance degrades

**Solution**:
```python
# Analyze query
analysis = db.analyze_query("SELECT * FROM users WHERE email = $1", ["test@example.com"])
print(f"Execution plan: {analysis.explain_plan}")

# Add index
db.execute("CREATE INDEX idx_users_email ON users(email)")
```

#### 3. Lock Contention

**Symptom**: Queries waiting for locks

**Solution**:
```python
# Check lock status
locks = db.query("SELECT * FROM pg_locks WHERE NOT granted")
print(f"Waiting locks: {len(locks)}")

# Kill blocking queries
blocking = db.query("SELECT pid, query FROM pg_stat_activity WHERE wait_event_type = 'Lock'")
for proc in blocking:
    db.execute(f"SELECT pg_terminate_backend({proc['pid']})")
```

## API Reference

### Core Classes

#### `PostgreSQL`
```python
class PostgreSQL:
    def __init__(self, config: PostgreSQLConfig) -> None: ...
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def execute(self, query: str, *params) -> Result: ...
    def fetch_one(self, query: str, *params) -> Optional[Row]: ...
    def fetch_all(self, query: str, *params) -> List[Row]: ...
    def execute_many(self, query: str, params_list: List[Tuple]) -> Result: ...
```

## Data Models

### Table Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM postgres:15-alpine

COPY init.sql /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql/postgresql.conf

ENV POSTGRES_DB=myapp
ENV POSTGRES_USER=app_user
ENV POSTGRES_PASSWORD=secure_password

EXPOSE 5432

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
```

## Monitoring & Observability

### Metrics Collection

```python
from postgresql import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("pg_connections_active", type="gauge")
collector.register_metric("pg_query_duration", type="histogram")
collector.register_metric("pg_transactions_total", type="counter")
collector.register_metric("pg_cache_hit_ratio", type="gauge")

collector.set("pg_connections_active", active_connections)
collector.observe("pg_query_duration", query_time_ms)
collector.inc("pg_transactions_total")
collector.set("pg_cache_hit_ratio", cache_hit_ratio)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from postgresql import PostgreSQL, PostgreSQLConfig

class TestPostgreSQL:
    def setup_method(self):
        self.config = PostgreSQLConfig(
            host="localhost",
            database="test_db",
            user="test_user",
            password="test_pass",
        )
        self.db = PostgreSQL(self.config)
    
    def test_execute_query(self):
        result = self.db.execute("SELECT 1 as value")
        assert result.rowcount == 1
    
    def test_fetch_one(self):
        result = self.db.fetch_one("SELECT 1 as value")
        assert result["value"] == 1
    
    def test_transaction(self):
        with self.db.transaction() as tx:
            tx.execute("INSERT INTO test (name) VALUES ($1)", "test")
        result = self.db.fetch_one("SELECT * FROM test WHERE name = $1", "test")
        assert result is not None
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Connection pooling
- **Added**: Query builder
- **Improved**: 2x faster queries
- **Fixed**: Memory leaks

## Glossary

| Term | Definition |
|------|------------|
| **ACID** | Atomicity, Consistency, Isolation, Durability |
| **MVCC** | Multi-Version Concurrency Control |
| **WAL** | Write-Ahead Logging |
| **VACUUM** | Process to reclaim storage |
| **EXPLAIN** | Command to show query execution plan |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/postgresql.git
cd postgresql
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 PostgreSQL Contributors

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

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Data Validation

### Query Validation

```python
from postgresql import QueryValidator

validator = QueryValidator()

# Validate query
validator.validate_query(query)
validator.validate_parameters(params)
validator.validate_result(result)

### Connection Pool Validation

```python
from postgresql import PoolValidator

validator = PoolValidator()

# Validate pool configuration
validator.validate_pool_config(pool_config)
validator.validate_connection_settings(connection_settings)
```
```

## Advanced Patterns

### Connection Pool Monitoring

```python
from postgresql import PoolMonitor, PoolStats

monitor = PoolMonitor(db)

# Get pool statistics
stats = monitor.get_stats()
print(f"Active connections: {stats.active}")
print(f"Idle connections: {stats.idle}")
print(f"Total connections: {stats.total}")
print(f"Waiting requests: {stats.waiting}")

# Monitor pool health
health = monitor.check_health()
print(f"Pool status: {health.status}")
print(f"Recommendations: {health.recommendations}")
```

### Query Performance Analysis

```python
from postgresql import QueryAnalyzer, QueryPlan

analyzer = QueryAnalyzer(db)

# Analyze query
plan = analyzer.analyze(
    query="SELECT * FROM users WHERE email = $1 AND created_at > $2",
    params=["test@example.com", datetime(2024, 1, 1)],
)

print(f"Execution time: {plan.execution_time_ms:.2f}ms")
print(f"Rows examined: {plan.rows_examined}")
print(f"Index used: {plan.index_used}")
print(f"Cost: {plan.cost}")
print(f"Recommendations: {plan.recommendations}")
```

### Index Management

```python
from postgresql import IndexManager

manager = IndexManager(db)

# List all indexes
indexes = manager.list_indexes(table="users")
for idx in indexes:
    print(f"Index: {idx.name}")
    print(f"  Columns: {idx.columns}")
    print(f"  Size: {idx.size_mb:.2f} MB")
    print(f"  Usage: {idx.usage_count}")

# Analyze index usage
usage = manager.analyze_usage(table="users")
print(f"Unused indexes: {usage.unused}")
print(f"Missing indexes: {usage.missing}")

# Create index
manager.create_index(
    table="users",
    columns=["email", "created_at"],
    unique=True,
    name="idx_users_email_created",
)
```

### Backup and Recovery

```python
from postgresql import BackupManager, BackupConfig

backup_config = BackupConfig(
    backup_dir="/backups",
    retention_days=30,
    compression=True,
    encryption=True,
    encryption_key="/path/to/encryption.key",
)

manager = BackupManager(db, backup_config)

# Create backup
backup = manager.create_backup(name="daily_backup")
print(f"Backup created: {backup.path}")
print(f"Size: {backup.size_mb:.2f} MB")

# List backups
backups = manager.list_backups()
for b in backups:
    print(f"Backup: {b.name}, Date: {b.date}, Size: {b.size_mb:.2f} MB")

# Restore backup
manager.restore_backup(backup.name)
```

### Replication Monitoring

```python
from postgresql import ReplicationMonitor

monitor = ReplicationMonitor(db)

# Get replication status
status = monitor.get_status()
for replica in status.replicas:
    print(f"Replica: {replica.host}")
    print(f"  State: {replica.state}")
    print(f"  Lag: {replica.lag_bytes} bytes")
    print(f"  WAL position: {replica.wal_position}")

# Check replication health
health = monitor.check_health()
print(f"Overall status: {health.status}")
print(f"Issues: {health.issues}")
```

### Connection Pool Optimization

```python
from postgresql import PoolOptimizer

optimizer = PoolOptimizer(db)

# Analyze pool usage
analysis = optimizer.analyze_pool()
print(f"Optimal pool size: {analysis.optimal_size}")
print(f"Current pool size: {analysis.current_size}")
print(f"Recommendation: {analysis.recommendation}")

# Optimize pool
optimizer.optimize(
    min_connections=5,
    max_connections=50,
    idle_timeout=30000,
)
```

### Query Caching

```python
from postgresql import QueryCache

cache = QueryCache(db, ttl=300)

# Cache query results
@cache.memoize(ttl=600)
def get_user(user_id):
    return db.fetch_one("SELECT * FROM users WHERE id = $1", user_id)

# Use cached query
user = get_user(123)  # Database query
user = get_user(123)  # Cache hit

# Invalidate cache
cache.invalidate("get_user:123")
```

### Database Migration Management

```python
from postgresql import MigrationManager, Migration

manager = MigrationManager(db)

# Create migration
migration = Migration(
    name="add_users_table",
    up="""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """,
    down="DROP TABLE users;",
)

# Apply migration
manager.apply(migration)

# Check migration status
status = manager.get_status()
print(f"Applied migrations: {len(status.applied)}")
print(f"Pending migrations: {len(status.pending)}")
```

### Data Export/Import

```python
from postgresql import DataExporter, DataImporter

exporter = DataExporter(db)

# Export table to CSV
exporter.export_to_csv(
    table="users",
    output_path="/exports/users.csv",
    delimiter=",",
    include_header=True,
)

# Export to JSON
exporter.export_to_json(
    table="users",
    output_path="/exports/users.json",
    format="array",
)

# Import from CSV
importer = DataImporter(db)
importer.import_from_csv(
    table="users",
    input_path="/imports/users.csv",
    delimiter=",",
    skip_header=True,
)
```

### Query Builder Advanced

```python
from postgresql import AdvancedQueryBuilder

builder = AdvancedQueryBuilder()

# Complex query with CTEs
query = (
    builder
    .with_cte("active_users", "SELECT * FROM users WHERE active = true")
    .with_cte("recent_orders", "SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '7 days'")
    .select("u.id", "u.name", "COUNT(o.id) as order_count")
    .from_("active_users", "u")
    .join("recent_orders", "o", "u.id = o.user_id")
    .group_by("u.id", "u.name")
    .having("COUNT(o.id) > 5")
    .order_by("order_count", "DESC")
    .limit(10)
    .build()
)

print(f"SQL: {query.sql}")
print(f"Params: {query.params}")

results = db.fetch_all(query.sql, *query.params)
```

### Stored Procedures

```python
from postgresql import StoredProcedure

# Create stored procedure
sp = StoredProcedure(db)
sp.create(
    name="process_order",
    parameters=[
        {"name": "p_order_id", "type": "INTEGER", "mode": "IN"},
        {"name": "p_status", "type": "VARCHAR(20)", "mode": "OUT"},
    ],
    language="plpgsql",
    body="""
    BEGIN
        UPDATE orders SET status = 'processed' WHERE id = p_order_id;
        p_status := 'success';
    END;
    """,
)

# Call stored procedure
result = sp.call("process_order", p_order_id=123)
print(f"Status: {result.p_status}")
```

### Database Triggers

```python
from postgresql import TriggerManager

trigger_manager = TriggerManager(db)

# Create trigger
trigger_manager.create(
    table="orders",
    name="audit_order_changes",
    timing="AFTER",
    event="UPDATE",
    body="""
    BEGIN
        INSERT INTO audit_log (table_name, record_id, action, old_data, new_data)
        VALUES ('orders', NEW.id, 'UPDATE', OLD, NEW);
    END;
    """,
)

# List triggers
triggers = trigger_manager.list_triggers(table="orders")
for trigger in triggers:
    print(f"Trigger: {trigger.name}")
    print(f"  Timing: {trigger.timing}")
    print(f"  Event: {trigger.event}")
```