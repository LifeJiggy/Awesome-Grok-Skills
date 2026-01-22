# Database Administration

## Overview

Database Administration (DBA) encompasses the management, optimization, and maintenance of database systems that store and retrieve organizational data. This skill covers database installation, configuration, security, backup/recovery, performance tuning, and high availability. Database administrators ensure data integrity, availability, and security across the enterprise data infrastructure.

## Core Capabilities

Database installation and configuration optimizes settings for workload characteristics. User management and security implements authentication, authorization, and encryption. Backup and recovery procedures protect against data loss and enable point-in-time restoration. Performance tuning analyzes query execution plans and optimizes database configuration.

High availability configurations using replication, clustering, and failover protect against downtime. Capacity planning projects storage and resource needs based on growth trends. Monitoring and alerting track database health metrics and notify on anomalies. Disaster recovery planning ensures business continuity across geographic locations.

## Usage Examples

```python
from database_administration import DatabaseAdministration

dba = DatabaseAdministration()

dba.add_database(
    name="production_db",
    db_type="postgresql",
    version="16",
    host="db-prod-01.company.com",
    port=5432,
    role="primary"
)

dba.configure_backup(
    strategy="full",
    retention_days=30
)

dba.setup_monitoring(
    tool="prometheus",
    metrics_interval=15
)

user = dba.create_user(
    database="production_db",
    username="app_user",
    roles=["read_write"],
    privileges=["SELECT", "INSERT", "UPDATE", "DELETE"]
)

replication = dba.configure_replication(
    primary_db="production_db",
    replica_db="replica_db",
    sync_mode="async"
)

ha = dba.setup_high_availability(
    cluster_name="prod-pg-cluster",
    nodes=["db-prod-01", "db-prod-02", "db-prod-03"],
    ha_type="patroni"
)

pool = dba.configure_connection_pooling(
    pool_name="app-pool",
    database="production_db",
    min_connections=10,
    max_connections=100
)

dba.create_index(
    database="production_db",
    table="orders",
    columns=["customer_id", "order_date"],
    index_type="btree"
)

query_analysis = dba.analyze_query(
    database="production_db",
    query="SELECT * FROM orders WHERE status = 'pending'"
)

disaster_recovery = dba.setup_disaster_recovery(
    primary_site="us-east",
    replica_site="us-west",
    rpo_hours=4,
    rto_hours=24
)

capacity = dba.plan_capacity_expansion(
    current_usage={"size_gb": 500, "iops": 5000},
    growth_rate_percent=20,
    forecast_months=12
)

performance_report = dba.generate_performance_report(
    database="production_db",
    time_range="last_24h"
)
```

## Best Practices

Implement defense in depth with multiple security layers including network, authentication, and authorization. Automate routine maintenance tasks including backups, statistics updates, and index maintenance. Monitor proactively with alerting on metrics before they become critical. Document all procedures and maintain runbooks for common operations.

Test recovery procedures regularly to ensure they work when needed. Plan capacity well ahead of actual needs to avoid emergency upgrades. Implement least privilege principles for database access. Use connection pooling to manage database connections efficiently.

## Related Skills

- PostgreSQL (PostgreSQL database management)
- MongoDB (NoSQL database management)
- SQL Programming (database querying)
- Data Warehousing (enterprise data storage)

## Use Cases

Enterprise database administration manages mission-critical systems supporting ERP and CRM applications. Web application databases serve high-traffic applications with demanding performance requirements. Data warehouse administration supports business intelligence and reporting workloads. Distributed database management spans multiple geographic regions for global applications.
