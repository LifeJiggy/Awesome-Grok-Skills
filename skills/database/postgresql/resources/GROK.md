# PostgreSQL

## Overview

PostgreSQL is a powerful open-source relational database system known for its reliability, feature robustness, and standards compliance. This skill covers PostgreSQL administration, advanced SQL features, performance optimization, and high availability configurations. PostgreSQL supports complex queries, foreign keys, triggers, updatable views, and transactional integrity with full ACID compliance.

## Core Capabilities

Advanced SQL features include CTEs, window functions, recursive queries, and complex joins. Table partitioning enables large table management through range, list, and hash partitions. Full-text search provides native text search capabilities with multiple language support. JSON/JSONB support enables document-style data alongside relational tables.

Replication capabilities include streaming replication with synchronous and asynchronous modes. Logical replication enables selective table replication and cross-version replication. Extensions like PostGIS for geospatial data, pg_cron for scheduling, and pg_partman for partition management extend functionality.

## Usage Examples

```python
from postgresql import PostgreSQL

pg = PostgreSQL()

pg.create_cluster(
    name="production",
    version="16",
    data_directory="/var/lib/postgresql/data"
)

pg.configure_connection(max_connections=200)

pg.enable_extension("postgis")
pg.enable_extension("pg_cron")
pg.enable_extension("pg_partman")

table = pg.create_table(
    table_name="orders",
    columns=[
        {"name": "id", "type": "BIGSERIAL", "primary_key": True},
        {"name": "customer_id", "type": "BIGINT", "references": "customers(id)"},
        {"name": "order_date", "type": "TIMESTAMP", "not_null": True},
        {"name": "status", "type": "VARCHAR(20)", "not_null": True},
        {"name": "total_amount", "type": "DECIMAL(10,2)"}
    ],
    primary_key=["id"]
)

index = pg.create_index(
    table_name="orders",
    column_name="order_date",
    index_type="BRIN",
    options={"pages_per_range": 32}
)

partitioned_table = pg.create_partitioned_table(
    table_name="orders_partitioned",
    partition_key="RANGE",
    columns=[{"name": "order_date", "type": "TIMESTAMP"}]
)

pg.add_partition(
    parent_table="orders_partitioned",
    partition_name="orders_2024_q1",
    bounds="FROM ('2024-01-01') TO ('2024-04-01')"
)

replication = pg.configure_replication(
    primary_conninfo="host=primary-db user=repl password=secret",
    slot_name="replication_slot"
)

publication = pg.create_publication(
    publication_name="orders_pub",
    tables=["orders", "order_items"],
    publish="insert,update,delete"
)

subscription = pg.create_subscription(
    subscription_name="orders_sub",
    conninfo="host=primary-db user=repl password=secret dbname=app",
    publication_names=["orders_pub"]
)

pg.create_materialized_view(
    view_name="daily_sales_mv",
    query="SELECT DATE(order_date) as sale_date, SUM(total_amount) as total FROM orders GROUP BY 1"
)

fts = pg.configure_full_text_search(
    column_name="description",
    dictionary="english"
)

pg.explain_analyze("SELECT * FROM orders WHERE status = 'pending'")

pg.vacuum_analyze("orders")

pg.configure_pgbench(scale_factor=100, transactions=10000)
```

## Best Practices

Use appropriate data types and constraints to ensure data integrity at the database level. Implement proper indexing strategies based on query patterns and access methods. Configure shared_buffers to approximately 25% of available RAM for typical workloads. Use connection pooling to manage database connections efficiently.

Partition large tables to improve query performance and simplify data management. Regularly vacuum and analyze tables to maintain query planner accuracy. Use EXPLAIN ANALYZE to understand query execution plans and identify optimization opportunities. Implement proper backup and disaster recovery procedures.

## Related Skills

- Database Administration (general DBA skills)
- SQL Programming (database querying)
- Data Warehousing (analytical databases)
- NoSQL (alternative database paradigms)

## Use Cases

Web applications leverage PostgreSQL for transactional data with complex query requirements. Geospatial applications use PostGIS for location-based data and queries. Data warehousing uses PostgreSQL for analytical workloads with large fact tables. Financial systems rely on PostgreSQL for ACID compliance and data integrity.
