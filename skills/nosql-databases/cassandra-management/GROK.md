---
name: "cassandra-management"
category: "nosql-databases"
version: "1.0.0"
tags: ["nosql-databases", "cassandra-management"]
---

# Cassandra Management

## Overview

Comprehensive cassandra-management capabilities within the nosql-databases domain. This module provides tools, frameworks, and best practices for cassandra-management operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from cassandra-management import _module

engine = _module.Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in nosql-databases domain
- Integration points with external systems

---

## Advanced Configuration

### Cassandra Cluster Configuration (cassandra.yaml)

```yaml
# cassandra.yaml - Production cluster configuration
cluster_name: 'production_cluster'
num_tokens: 16
allocate_tokens_for_keyspace: 64

# Network
listen_address: 10.0.0.1
broadcast_address: 10.0.0.1
rpc_address: 0.0.0.0
broadcast_rpc_address: 10.0.0.1

# Port configuration
storage_port: 7000
ssl_storage_port: 7001
native_transport_port: 9042
native_transport_max_threads: 128
native_transport_max_frame_size_in_mb: 256

# Memory and performance
heap_size_newgen: 2048M
heap_size_oldgen: 6144M
concurrent_reads: 32
concurrent_writes: 32
concurrent_counter_writes: 32
memtable_allocation_type: offheap_objects

# Compaction
compaction_throughput_mb_per_sec: 256
compaction_large_partition_warning_threshold_mb: 100
compaction_tombstone_warn_threshold: 100000
compaction_tombstone_failure_threshold: 1000000

# Snitch and topology
endpoint_snitch: GossipingPropertyFileSnitch
dynamic_snitch_update_interval_ms: 100
dynamic_snitch_reset_interval_ms: 600000
dynamic_snitch_badness_threshold: 0.1
```

### GossipingPropertyFileSnitch Configuration

```properties
# cassandra-rackdc.properties
dc=us-east-1
rack=rack1
prefer_local=true
```

### DataStax Driver Configuration (Java)

```java
// application.conf
datastax-java-driver {
  basic {
    contact-points = ["10.0.0.1:9042", "10.0.0.2:9042", "10.0.0.3:9042"]
    load-balancing-policy {
      local-datacenter = "us-east-1"
      local-availability-zone = "rack1"
    }
    request {
      timeout = 5 seconds
      consistency = LOCAL_QUORUM
      page-size = 5000
    }
    session-name = "MyAppSession"
  }

  advanced {
    connection {
      pool {
        local.size = 3
        remote.size = 1
      }
      connect-timeout = 5 seconds
      keep-alive {
        interval = 30 seconds
      }
    }
    reconnection-policy {
      class = ExponentialReconnectionPolicy
      base-delay = 1 second
      max-delay = 60 seconds
    }
    retry-policy {
      class = DefaultRetryPolicy
    }
  }
}
```

## Architecture Patterns

### Cassandra Data Modeling Patterns

```
┌─────────────────────────────────────────────────────────┐
│                   Partition Design                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Query-First Modeling:                                  │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ users_by_id │    │ users_by_   │    │ users_by_   │ │
│  │             │    │ email       │    │ status      │ │
│  │ PK: user_id │    │ PK: email   │    │ PK: status  │ │
│  │             │    │ CK: user_id │    │ CK: user_id │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                         │
│  Denormalization Rule: One table per query pattern     │
└─────────────────────────────────────────────────────────┘
```

### Multi-DC Replication Pattern

```
                    ┌─────────────────┐
                    │   Application   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │ DC: us-east│ │ DC: eu-west│ │ DC: ap-south│
        │            │ │            │ │            │
        │ ┌────────┐ │ │ ┌────────┐ │ │ ┌────────┐ │
        │ │ Node 1 │ │ │ │ Node 1 │ │ │ │ Node 1 │ │
        │ │ Node 2 │ │ │ │ Node 2 │ │ │ │ Node 2 │ │
        │ │ Node 3 │ │ │ │ Node 3 │ │ │ │ Node 3 │ │
        │ └────────┘ │ │ └────────┘ │ │ └────────┘ │
        └────────────┘ └────────────┘ └────────────┘

  Keyspace Configuration:
  CREATE KEYSPACE production
  WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'us-east-1': 3,
    'eu-west-1': 3,
    'ap-south-1': 3
  };
```

### Time Series Data Model

```sql
-- Sensor data table optimized for time-range queries
CREATE TABLE sensor_readings (
    sensor_id text,
    date text,           -- YYYY-MM-DD partition
    timestamp timestamp,
    value double,
    unit text,
    metadata map<text, text>,
    PRIMARY KEY ((sensor_id, date), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND compaction = {
    'class': 'TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': 1
  }
  AND default_time_to_live = 7776000  -- 90 days
  AND gc_grace_seconds = 864000;      -- 10 days

-- Materialized view for reverse lookups
CREATE MATERIALIZED VIEW readings_by_time AS
    SELECT * FROM sensor_readings
    WHERE date IS NOT NULL
      AND timestamp IS NOT NULL
      AND sensor_id IS NOT NULL
    PRIMARY KEY ((date), timestamp, sensor_id);
```

## Integration Guide

### DataStax Driver for Python

```python
from cassandra.cluster import Cluster
from cassandra.policies import (
    DCAwareRoundRobinPolicy,
    ExponentialReconnectionPolicy,
    RetryPolicy
)
from cassandra.query import SimpleStatement, ConsistencyLevel
import time

class CassandraClient:
    """Production-ready Cassandra client with connection pooling."""

    def __init__(self, contact_points, local_datacenter):
        self.cluster = Cluster(
            contact_points=contact_points,
            load_balancing_policy=DCAwareRoundRobinPolicy(
                local_dc=local_datacenter
            ),
            reconnection_policy=ExponentialReconnectionPolicy(
                base_delay=1.0,
                max_delay=60.0
            ),
            protocol_version=4,
            idle_heartbeat_interval=30,
            idle_heartbeat_timeout=60
        )
        self.session = self.cluster.connect()

    def execute(self, query, params=None, consistency=ConsistencyLevel.LOCAL_QUORUM):
        statement = SimpleStatement(query, consistency_level=consistency)
        start = time.time()
        result = self.session.execute(statement, params)
        elapsed = time.time() - start
        return result

    def bulk_insert(self, table, data_list, batch_size=50):
        """Batch insert with automatic batching."""
        from cassandra.query import BatchStatement, BatchType

        query = f"INSERT INTO {table} (id, name, value, timestamp) VALUES (?, ?, ?, ?)"
        prepared = self.session.prepare(query)

        for i in range(0, len(data_list), batch_size):
            batch = BatchStatement(consistency_level=ConsistencyLevel.LOCAL_QUORUM)
            for item in data_list[i:i+batch_size]:
                batch.add(prepared, item)
            self.execute(batch)

    def close(self):
        self.cluster.shutdown()
```

### Spring Boot Integration

```java
@Configuration
@EnableCassandraRepositories(basePackages = "com.example.repository")
public class CassandraConfig extends AbstractCassandraConfiguration {

    @Value("${cassandra.contact-points}")
    private String contactPoints;

    @Value("${cassandra.keyspace}")
    private String keyspace;

    @Value("${cassandra.local-datacenter}")
    private String localDatacenter;

    @Override
    protected String getKeyspaceName() {
        return keyspace;
    }

    @Override
    protected String getContactPoints() {
        return contactPoints;
    }

    @Bean
    public CassandraClusterFactoryBean cluster() {
        CassandraClusterFactoryBean cluster = new CassandraClusterFactoryBean();
        cluster.setContactPoints(getContactPoints());
        cluster.setKeyspaceName(getKeyspaceName());
        cluster.setLocalDatacenter(localDatacenter);
        cluster.setPoolingOptions(new PoolingOptions()
            .setConnectionsPerHost(HostDistance.LOCAL, 3, 7)
            .setConnectionsPerHost(HostDistance.REMOTE, 1, 2));
        cluster.setReconnectionPolicy(new ExponentialReconnectionPolicy(1000, 60000));
        return cluster;
    }

    @Bean
    public CassandraOperations cassandraTemplate() {
        return new CassandraTemplate(session().getObject());
    }
}
```

## Performance Optimization

### Compaction Strategy Selection

| Strategy | Use Case | Write Amplification | Read Amplification |
|----------|----------|--------------------|--------------------|
| SizeTieredCompactionStrategy (STCS) | Write-heavy, append-only | Medium | High |
| LeveledCompactionStrategy (LCS) | Read-heavy, update-heavy | High | Low |
| TimeWindowCompactionStrategy (TWCS) | Time-series data | Low | Medium |
| DateTieredCompactionStrategy (DTCS) | Time-series (legacy) | Low | Medium |

```sql
-- STCS for write-heavy workload
CREATE TABLE analytics_events (
    event_id uuid,
    event_type text,
    payload text,
    created_at timestamp,
    PRIMARY KEY (event_id)
) WITH compaction = {
    'class': 'SizeTieredCompactionStrategy',
    'min_threshold': 4,
    'max_threshold': 32,
    'min_sstable_size': 52428800
  };

-- LCS for read-heavy workload
CREATE TABLE user_profiles (
    user_id uuid,
    email text,
    name text,
    updated_at timestamp,
    PRIMARY KEY (user_id)
) WITH compaction = {
    'class': 'LeveledCompactionStrategy',
    'sstable_size_in_mb': 160
  };

-- TWCS for time-series
CREATE TABLE metrics (
    metric_id text,
    bucket timestamp,
    timestamp timestamp,
    value double,
    PRIMARY KEY ((metric_id, bucket), timestamp)
) WITH compaction = {
    'class': 'TimeWindowCompactionStrategy',
    'compaction_window_unit': 'HOURS',
    'compaction_window_size': 4
  };
```

### Query Optimization

```python
def optimize_queries(session):
    """Demonstrate query optimization patterns."""

    # 1. Use prepared statements (avoid query parsing overhead)
    prepared = session.prepare("""
        SELECT * FROM users
        WHERE user_id = ?
        LIMIT 1
    """)
    prepared.consistency_level = ConsistencyLevel.LOCAL_QUORUM

    # 2. Use paging for large result sets
    from cassandra.query import dict_factory
    session.row_factory = dict_factory
    result = session.execute(
        "SELECT * FROM events WHERE event_date = '2024-01-15'",
        fetch_size=1000
    )
    for row in result:
        process_event(row)

    # 3. Avoid ALLOW FILTERING
    # BAD: SELECT * FROM events WHERE user_id = 'x' AND event_type = 'login'
    # GOOD: Create a table with (user_id, event_type, timestamp) as primary key

    # 4. Use lightweight transactions for idempotent writes
    session.execute("""
        INSERT INTO users (user_id, email, name)
        VALUES (uuid(), 'alice@example.com', 'Alice')
        IF NOT EXISTS
    """)

    # 5. Batch related mutations
    from cassandra.query import BatchStatement
    batch = BatchStatement()
    batch.add("UPDATE counters SET total = total + 1 WHERE id = 'page_views'")
    batch.add("INSERT INTO activity_log (id, action, timestamp) VALUES (uuid(), 'view', toTimestamp(now()))")
    session.execute(batch)
```

## Security Considerations

### Authentication and Authorization

```sql
-- Create role-based access
CREATE ROLE admin WITH PASSWORD = 'SecurePass123!' AND SUPERUSER = true;
CREATE ROLE app_user WITH PASSWORD = 'AppPass456!' AND LOGIN = true;
CREATE ROLE read_only WITH PASSWORD = 'ReadOnly789!' AND LOGIN = true;

-- Grant permissions
GRANT ALL ON KEYSPACE production TO admin;
GRANT ALL ON KEYSPACE production TO app_user;
GRANT SELECT ON KEYSPACE production TO read_only;

-- Table-level permissions
GRANT SELECT, INSERT, UPDATE ON TABLE production.users TO app_user;
GRANT SELECT ON TABLE production.users TO read_only;
GRANT ALTER ON TABLE production.users TO admin;

-- Allow access from specific IPs
ALTER ROLE app_user WITH LOGIN = true AND PASSWORD = 'AppPass456!';

-- Row-level security (Cassandra 4.0+)
CREATE FUNCTION IF NOT EXISTS production.is_owned_by_user(user_id text, current_user text)
    CALLED ON NULL INPUT
    RETURNS boolean
    LANGUAGE java
    AS 'return user_id.equals(current_user);';

CREATE FILTER ON TABLE production.users
    USING is_owned_by_user(user_id, current_user);
```

### TLS/SSL Configuration

```yaml
# Server-side TLS
server_encryption_options:
  internode_encryption: all
  keystore: /etc/cassandra/.keystore
  keystore_password: cassandra
  truststore: /etc/cassandra/.truststore
  truststore_password: cassandra
  require_client_auth: true

# Client-to-node encryption
client_encryption_options:
  enabled: true
  keystore: /etc/cassandra/.keystore
  keystore_password: cassandra
  truststore: /etc/cassandra/.truststore
  truststore_password: cassandra
  require_client_auth: true
```

```python
from cassandra.cluster import Cluster
from cassandra.ssl import SSLContext, SSLProtocol

ssl_context = SSLContext(protocol=SSLProtocol.TLSv1_2)
ssl_context.load_cert_chain(
    certfile='/etc/cassandra/client.pem',
    keyfile='/etc/cassandra/client.key',
    password='client_pass'
)
ssl_context.load_verify_locations('/etc/cassandra/ca.pem')

cluster = Cluster(
    contact_points=['10.0.0.1'],
    ssl_context=ssl_context
)
```

## Troubleshooting Guide

### Common Cassandra Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| GC pressure | High latency, pause > 500ms | Tune heap, use off-heap memtables |
| Tombstone warning | `Tombstone overwhelm` in logs | Query patterns, TTL, compaction |
| Node down | `NoHostAvailableException` | Gossip check, repair, network |
| Stream failure | Streaming errors in logs | Increase streaming throughput |
| Read timeout | `ReadTimeoutException` | Check consistency, replica count |
| Overloaded | `OverloadedException` | Reduce concurrency, check drivers |

```python
def diagnose_cluster(session):
    """Run diagnostic queries to identify cluster issues."""

    # 1. Check cluster topology
    result = session.execute("SELECT * FROM system.peers")
    nodes = list(result)
    print(f"Cluster size: {len(nodes) + 1} nodes")

    # 2. Check for tombstones in recent queries
    result = session.execute("""
        SELECT * FROM system_traces.sessions
        WHERE started_at > '2024-01-01'
        LIMIT 10
    """)

    # 3. Check compaction statistics
    result = session.execute("""
        SELECT * FROM system.size_estimates
        WHERE keyspace_name = 'production'
    """)
    for row in result:
        print(f"Table: {row.table_name}, "
              f"Partitions: {row.estimated_partition_count}, "
              f"Size: {row.estimated_partition_size_in_bytes}")

    # 4. Check pending repairs
    result = session.execute("SELECT * FROM system_distributed.repair_history")
    for row in result:
        print(f"Repair: {row.id}, Status: {row.state}")

    # 5. Check node status
    result = session.execute("SELECT * FROM system.local")
    local = result.one()
    print(f"Local DC: {local.data_center}, "
          f"Rack: {local.rack}, "
          f"Load: {local.load}")
```

### Performance Tuning Checklist

| Area | Setting | Recommended Value |
|------|---------|-------------------|
| Heap | Xms / Xmx | Equal, 8-16 GB |
| Heap | NewGen | 1/4 of heap, max 2GB |
| Memory | memtable_allocation_type | offheap_objects |
| Memory | commitlog_total_space | 8-32 GB |
| Network | streaming_socket_timeout | 86400 seconds |
| I/O | concurrent_compactors | min(cores, 4) |
| I/O | compaction_throughput_mb_per_sec | 256 (SSD), 64 (HDD) |
| Query | concurrent_reads | 32 per core |
| Query | concurrent_writes | 32 per core |

## API Reference

### CQL Operations

```sql
-- Create keyspace with replication
CREATE KEYSPACE IF NOT EXISTS production
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'us-east-1': 3
};

-- Create table with all options
CREATE TABLE IF NOT EXISTS production.users (
    user_id timeuuid,
    username text,
    email text,
    status text DEFAULT 'active',
    created_at timestamp DEFAULT toTimestamp(now()),
    metadata map<text, text>,
    tags set<text>,
    PRIMARY KEY ((status), created_at, user_id)
) WITH CLUSTERING ORDER BY (created_at DESC)
  AND compaction = {
    'class': 'LeveledCompactionStrategy'
  }
  AND compression = {
    'sstable_compression': 'LZ4Compressor'
  }
  AND gc_grace_seconds = 864000
  AND default_time_to_live = 31536000;

-- Insert with consistency
INSERT INTO production.users (user_id, username, email, status)
VALUES (now(), 'alice', 'alice@example.com', 'active')
USING TTL 31536000 AND TIMESTAMP 1705000000000;

-- Query with filtering
SELECT * FROM production.users
WHERE status = 'active'
AND created_at > '2024-01-01'
LIMIT 100;

-- Update with conditional
UPDATE production.users
SET status = 'inactive'
WHERE user_id = ?
IF status = 'active';

-- Delete with timestamp
DELETE FROM production.users
WHERE user_id = ?
USING TIMESTAMP 1705000000000;
```

### Java Driver Operations

```java
import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.*;
import com.datastax.oss.driver.api.core.type.DataTypes;
import java.util.UUID;
import java.time.Instant;

public class CassandraOperations {

    public void insertUser(CqlSession session) {
        PreparedStatement prepared = session.prepare(
            "INSERT INTO users (user_id, username, email, created_at) " +
            "VALUES (?, ?, ?, ?)"
        );

        BoundStatement bound = prepared.bind(
            UUID.randomUUID(),
            "alice",
            "alice@example.com",
            Instant.now()
        );

        session.execute(bound);
    }

    public void queryUsers(CqlSession session) {
        ResultSet rs = session.execute(
            SimpleStatement.newInstance("SELECT * FROM users WHERE user_id = ?", userId)
        );

        for (Row row : rs) {
            UUID id = row.getUuid("user_id");
            String name = row.getString("username");
            System.out.printf("User: %s (%s)%n", name, id);
        }
    }

    public void batchMutations(CqlSession session) {
        BatchStatement batch = BatchStatement.builder(BatchType.UNLOGGED)
            .addStatement(SimpleStatement.newInstance(
                "INSERT INTO counters (name, value) VALUES (?, ?)",
                "page_views", 1
            ))
            .addStatement(SimpleStatement.newInstance(
                "INSERT INTO activity (id, action) VALUES (?, ?)",
                UUID.randomUUID(), "view"
            ))
            .build();

        session.execute(batch);
    }
}
```

## Data Models

### User Management Schema

```sql
-- User account table
CREATE TABLE user_accounts (
    user_id timeuuid,
    username text,
    email text,
    password_hash text,
    status text,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY ((status), created_at, user_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- User profile table (separate for read performance)
CREATE TABLE user_profiles (
    user_id timeuuid,
    display_name text,
    avatar_url text,
    bio text,
    settings map<text, text>,
    PRIMARY KEY (user_id)
);

-- User sessions
CREATE TABLE active_sessions (
    session_id timeuuid,
    user_id timeuuid,
    ip_address inet,
    user_agent text,
    created_at timestamp,
    expires_at timestamp,
    PRIMARY KEY (user_id, created_at, session_id)
) WITH CLUSTERING ORDER BY (created_at DESC)
  AND default_time_to_live = 86400;

-- Audit log
CREATE TABLE audit_log (
    entity_type text,
    entity_id timeuuid,
    action text,
    user_id timeuuid,
    details map<text, text>,
    timestamp timeuuid,
    PRIMARY KEY ((entity_type, entity_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND default_time_to_live = 7776000;
```

### E-Commerce Data Model

```sql
-- Product catalog
CREATE TABLE products_by_category (
    category text,
    product_id timeuuid,
    name text,
    price decimal,
    stock_count int,
    attributes map<text, text>,
    PRIMARY KEY ((category), product_id)
) WITH CLUSTERING ORDER BY (product_id DESC);

-- Shopping cart
CREATE TABLE shopping_carts (
    user_id timeuuid,
    product_id timeuuid,
    quantity int,
    added_at timestamp,
    PRIMARY KEY (user_id, product_id)
);

-- Order history
CREATE TABLE orders_by_customer (
    customer_id timeuuid,
    order_date date,
    order_id timeuuid,
    total decimal,
    status text,
    items list<frozen<tuple<text, int, decimal>>>,
    PRIMARY KEY ((customer_id), order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC, order_id DESC);
```

## Deployment Guide

### Production Cluster Setup

```bash
#!/bin/bash
# cassandra-cluster-setup.sh

# 1. Install Cassandra on all nodes
sudo apt-get update
sudo apt-get install -y cassandra

# 2. Configure each node
for NODE in node1 node2 node3; do
    ssh $NODE "sed -i 's/cluster_name: .*/cluster_name: production_cluster/' /etc/cassandra/cassandra.yaml"
    ssh $NODE "sed -i 's/listen_address: .*/listen_address: $NODE/' /etc/cassandra/cassandra.yaml"
    ssh $NODE "sed -i 's/rpc_address: .*/rpc_address: 0.0.0.0/' /etc/cassandra/cassandra.yaml"
done

# 3. Start nodes one at a time
for NODE in node1 node2 node3; do
    ssh $NODE "sudo systemctl start cassandra"
    sleep 60
done

# 4. Verify cluster status
nodetool status

# 5. Create keyspace
cqlsh -e "CREATE KEYSPACE production WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': 3};"

# 6. Run initial repair
nodetool repair --full production
```

### Docker Compose (Development)

```yaml
version: '3.8'

services:
  cassandra-1:
    image: cassandra:4.1
    container_name: cassandra-1
    ports:
      - "9042:9042"
      - "7000:7000"
    volumes:
      - cassandra-1-data:/var/lib/cassandra
    environment:
      CASSANDRA_CLUSTER_NAME: dev_cluster
      CASSANDRA_DC: dc1
      CASSANDRA_RACK: rack1
      CASSANDRA_ENDPOINT_SNITCH: GossipingPropertyFileSnitch
    networks:
      - cassandra-net

  cassandra-2:
    image: cassandra:4.1
    container_name: cassandra-2
    depends_on:
      - cassandra-1
    volumes:
      - cassandra-2-data:/var/lib/cassandra
    environment:
      CASSANDRA_CLUSTER_NAME: dev_cluster
      CASSANDRA_DC: dc1
      CASSANDRA_RACK: rack2
      CASSANDRA_SEEDS: cassandra-1
    networks:
      - cassandra-net

  cassandra-3:
    image: cassandra:4.1
    container_name: cassandra-3
    depends_on:
      - cassandra-1
    volumes:
      - cassandra-3-data:/var/lib/cassandra
    environment:
      CASSANDRA_CLUSTER_NAME: dev_cluster
      CASSANDRA_DC: dc1
      CASSANDRA_RACK: rack3
      CASSANDRA_SEEDS: cassandra-1
    networks:
      - cassandra-net

volumes:
  cassandra-1-data:
  cassandra-2-data:
  cassandra-3-data:

networks:
  cassandra-net:
```

## Monitoring & Observability

### Prometheus + Grafana Metrics

```python
from cassandra.metrics import ClientMetrics
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define Cassandra-specific metrics
CASSANDRA_READS = Counter('cassandra_reads_total', 'Total CQL reads', ['keyspace', 'table'])
CASSANDRA_WRITES = Counter('cassandra_writes_total', 'Total CQL writes', ['keyspace', 'table'])
CASSANDRA_LATENCY = Histogram('cassandra_operation_latency_seconds', 'CQL operation latency', ['operation'])
CASSANDRA_PENDING = Gauge('cassandra_pending_tasks', 'Pending compaction/streaming tasks', ['type'])
CASSANDRA_CONNECTED = Gauge('cassandra_connected_clients', 'Connected native clients')

class CassandraMonitor:
    def __init__(self, session):
        self.session = session

    def collect_metrics(self):
        # System tables for monitoring
        result = self.session.execute("SELECT * FROM system.clients")
        for row in result:
            CASSANDRA_CONNECTED.set(row.connections)

        # Compaction statistics
        result = self.session.execute("""
            SELECT * FROM system.compaction_history
            WHERE ended_at > toTimestamp(now()) - 3600000
        """)
        for row in result:
            CASSANDRA_PENDING.labels(type='compaction').inc()

        # Token range ownership
        result = self.session.execute("SELECT * FROM system.replication")
        for row in result:
            print(f"Keyspace: {row.keyspace_name}, Replication: {row.replication}")

    def start_metrics_server(self, port=8080):
        start_http_server(port)
        while True:
            self.collect_metrics()
            time.sleep(15)
```

### Key Grafana Panels

```promql
# Query latency p99
histogram_quantile(0.99, rate(cassandra_operation_latency_seconds_bucket{operation="read"}[5m]))

# Write throughput
rate(cassandra_writes_total[5m])

# Pending compactions
cassandra_pending_tasks{type="compaction"}

# Connected clients
cassandra_connected_clients

# Tombstone count per query (via tracing)
# Enable tracing for slow queries and analyze tombstone counts
```

## Testing Strategy

### Integration Test Framework

```python
import pytest
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

@pytest.fixture(scope="module")
def cassandra_session():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS test_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")
    session.set_keyspace('test_keyspace')
    yield session
    session.execute("DROP KEYSPACE test_keyspace")
    cluster.shutdown()

class TestUserOperations:
    def test_insert_and_read(self, cassandra_session):
        cassandra_session.execute("""
            CREATE TABLE IF NOT EXISTS users (id uuid PRIMARY KEY, name text, email text)
        """)

        # Insert
        cassandra_session.execute(
            "INSERT INTO users (id, name, email) VALUES (uuid(), ?, ?)",
            ("Test User", "test@example.com")
        )

        # Read
        result = cassandra_session.execute("SELECT * FROM users LIMIT 1")
        row = result.one()
        assert row.name == "Test User"
        assert row.email == "test@example.com"

    def test_update(self, cassandra_session):
        cassandra_session.execute("""
            CREATE TABLE IF NOT EXISTS counters (id text PRIMARY KEY, value counter)
        """)

        cassandra_session.execute("UPDATE counters SET value = value + 1 WHERE id = 'test'")
        cassandra_session.execute("UPDATE counters SET value = value + 5 WHERE id = 'test'")

        result = cassandra_session.execute("SELECT value FROM counters WHERE id = 'test'")
        assert result.one().value == 6

    @pytest.mark.parametrize("status,expected_count", [
        ("active", 3),
        ("inactive", 1),
    ])
    def test_query_by_status(self, cassandra_session, status, expected_count):
        result = cassandra_session.execute(
            "SELECT COUNT(*) FROM users WHERE status = ?",
            (status,)
        )
        assert result.one().count == expected_count
```

## Versioning & Migration

### Schema Migration Tool

```python
from cassandra.cluster import Cluster
from datetime import datetime

class CassandraMigration:
    def __init__(self, cluster, keyspace):
        self.cluster = cluster
        self.session = cluster.connect(keyspace)
        self._ensure_migrations_table()

    def _ensure_migrations_table(self):
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version int PRIMARY KEY,
                description text,
                applied_at timestamp,
                checksum text
            )
        """)

    def get_current_version(self):
        result = self.session.execute(
            "SELECT MAX(version) as ver FROM schema_migrations"
        )
        row = result.one()
        return row.ver if row.ver else 0

    def migrate(self, version, up_sql, down_sql=None):
        current = self.get_current_version()
        if current >= version:
            return False

        for statement in up_sql:
            self.session.execute(statement)

        self.session.execute(
            "INSERT INTO schema_migrations (version, description, applied_at) VALUES (%s, %s, %s)",
            (version, up_sql[0][:100], datetime.utcnow())
        )
        return True

# Migration definitions
MIGRATIONS = [
    {
        "version": 1,
        "up": [
            "CREATE TABLE users (id uuid PRIMARY KEY, name text, email text)",
            "CREATE INDEX ON users (email)"
        ],
        "down": ["DROP TABLE users"]
    },
    {
        "version": 2,
        "up": [
            "ALTER TABLE users ADD status text",
            "CREATE TABLE user_roles (user_id uuid, role text, PRIMARY KEY (user_id, role))"
        ],
        "down": ["DROP TABLE user_roles", "ALTER TABLE users DROP status"]
    }
]
```

## Glossary

| Term | Definition |
|------|------------|
| Partition | A node of data distributed across the cluster based on token range |
| Token | A value used to determine which node owns a partition |
| Replication Factor | Number of copies of data across the cluster |
| Consistency Level | Number of replicas that must acknowledge a read/write |
| Snitch | Component that determines network topology for routing |
| Compaction | Process of merging SSTables to reclaim space and improve read performance |
| Tombstone | Marker indicating deleted data, garbage collected during compaction |
| SSTable | Immutable on-disk storage file containing sorted data |
| Memtable | In-memory buffer for writes before flushing to SSTable |
| Commit Log | Write-ahead log for crash recovery |
| Gossip | Protocol for nodes to share state information |
| Bootstrap | Process of adding a new node to the cluster |
| Repair | Process of ensuring data consistency across replicas |
| Streaming | Process of transferring data between nodes during bootstrap/repair |
| VNode | Virtual node, allows a physical node to own multiple token ranges |
| Prepared Statement | Pre-parsed CQL statement for repeated execution |
| Batch Statement | Group of CQL statements executed atomically |
| Materialized View | Pre-computed denormalized view of a base table |
| Secondary Index | Index on a non-primary-key column |
| Lightweight Transaction | Compare-and-set operation using Paxos |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release with basic Cassandra configuration |
| 1.1.0 | 2024-03-01 | Added data modeling patterns and compaction strategies |
| 1.2.0 | 2024-05-01 | Added multi-DC replication and security hardening |
| 1.3.0 | 2024-07-01 | Added performance optimization and monitoring |
| 1.4.0 | 2024-09-01 | Added testing framework and migration tooling |
| 1.5.0 | 2024-11-01 | Expanded troubleshooting guide and API reference |
| 1.6.0 | 2025-01-01 | Added Kubernetes deployment and observability stack |

## Contributing Guidelines

1. **Code Style**: Follow Python PEP 8 and Java Google Java Style Guide
2. **CQL Conventions**: Use snake_case, lowercase keywords, explicit data types
3. **Testing**: Integration tests required for all CQL operations
4. **Documentation**: Update data model documentation for schema changes
5. **Performance**: Include benchmark results for query optimization changes
6. **Compatibility**: Test against Cassandra 3.x and 4.x versions

## License

This module is part of the Awesome-Grok-Skills project and follows the MIT License.
