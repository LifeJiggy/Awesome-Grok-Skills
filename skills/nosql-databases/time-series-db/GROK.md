---
name: "time-series-db"
category: "nosql-databases"
version: "1.0.0"
tags: ["nosql-databases", "time-series-db"]
---

# Time Series Db

## Overview

Comprehensive time-series-db capabilities within the nosql-databases domain. This module provides tools, frameworks, and best practices for time-series-db operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from time-series-db import _module

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

### InfluxDB Configuration

```toml
# influxdb.conf
[meta]
  dir = "/var/lib/influxdb/meta"
  retention_autocreate = true

[data]
  dir = "/var/lib/influxdb/data"
  engine = "tsm1"
  wal-dir = "/var/lib/influxdb/wal"

  # Performance tuning
  cache-max-memory-size = 524288000  # 500MB
  cache-snapshot-memory-size = 26214400  # 25MB
  cache-snapshot-write-cold-duration = "10m"
  compact-throughput = 48  # MB/sec
  compact-throughput-burst = 48  # MB/sec
  max-concurrent-compactions = 0

  # Retention
  retention-check-interval = "30m"

[http]
  enabled = true
  bind-address = ":8086"
  auth-enabled = true
  log-enabled = true
  write-tracing = false
  pprof-enabled = false
  https-enabled = true
  https-certificate = "/etc/influxdb/server.crt"
  https-private-key = "/etc/influxdb/server.key"

[coordinator]
  write-timeout = "10s"
  max-concurrent-queries = 0
  query-timeout = "0s"
  log-queries-after = "0s"
  max-select-point = 0
  max-select-series = 0
  max-select-buckets = 0

[retention]
  enabled = true
  check-interval = "30m"

[shard-precreation]
  enabled = true
  check-interval = "10m"
  advance-period = "30m"

[monitor]
  store-enabled = true
  store-database = "_internal"
  store-interval = "10s"

[subscriber]
  enabled = true
  http-timeout = "30s"
  insecure-skip-verify = false

[[udp]]
  enabled = true
  bind-address = ":8089"
  database = "udp"
  retention-policy = ""
  buffer-size = 1000
  batch-size = 1000
  batch-timeout = "1s"
  precision = "ms"
```

### TimescaleDB Configuration

```sql
-- TimescaleDB initialization
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create hypertable with partitioning
SELECT create_hypertable(
  'sensor_readings',
  'time',
  chunk_time_interval => INTERVAL '1 day',
  if_not_exists => TRUE
);

-- Enable compression (automatic after 7 days)
ALTER TABLE sensor_readings SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'sensor_id',
  timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('sensor_readings', INTERVAL '7 days');

-- Enable continuous aggregates
CREATE MATERIALIZED VIEW sensor_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  sensor_id,
  AVG(value) AS avg_value,
  MAX(value) AS max_value,
  MIN(value) AS min_value,
  COUNT(*) AS sample_count
FROM sensor_readings
GROUP BY bucket, sensor_id;

-- Retention policy (drop data older than 90 days)
SELECT add_retention_policy('sensor_readings', INTERVAL '90 days');

-- Refresh policy for continuous aggregate
SELECT add_continuous_aggregate_policy('sensor_hourly',
  start_offset => INTERVAL '3 hours',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);
```

### QuestDB Configuration

```properties
# server.conf
# Network
bind.ip=0.0.0.0
bind.ipv4.wildcard=true
pg.net.bind.port=8812
line.udp.bind.port=9009
line.udp.bind.address=0.0.0.0
line.udp.enabled=true
line.udp.systemd.unit.name=questdb

# Memory
o3.max.mems.per.thread=16m
cairo.sql.max.pages=1024
cairo.sql.sort.key.page.size=4m

# Storage
cairo.root=/var/lib/questdb/db
cairo.database.root=/var/lib/questdb/db
cairo.snapshot.root=/var/lib/questdb/db/snapshot

# Performance
cairo.page.frame.rowid.list.pool.capacity=64
cairo.page.frame.merge.tree.pool.capacity=64
cairo.page.frame.cursor.pool.capacity=64
```

## Architecture Patterns

### Time Series Data Model

```
┌─────────────────────────────────────────────────────────────────┐
│                 Time Series Database Patterns                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  InfluxDB Line Protocol:                                        │
│  measurement,tag1=val1,tag2=val2 field1=val1,field2=val2 time  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Ingestion  │──▶│   Storage    │──▶│   Query      │         │
│  │   Layer      │  │   Engine     │  │   Engine     │         │
│  │              │  │              │  │              │         │
│  │ • Write ahead│  │ • TSM trees  │  │ • Flux       │         │
│  │ • Sharding   │  │ • Compression│  │ • SQL        │         │
│  │ • Batching   │  │ • Retention  │  │ • InfluxQL   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  Partitioning Strategy:                                         │
│  ┌─────────────────────────────────────────────┐               │
│  │ 2024-01  │ 2024-02  │ 2024-03  │ ...       │               │
│  │ Chunk 1  │ Chunk 2  │ Chunk 3  │           │               │
│  │          │          │          │           │               │
│  │ Compress │ Compress │ Active   │           │               │
│  │ Cold     │ Cold     │ Hot      │           │               │
│  └─────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### Downsampling Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Raw Data    │────▶│  1min Agg    │────▶│  1hour Agg   │
│  (1s rate)   │     │  (kept 7d)   │     │  (kept 90d)  │
│  ~86MB/day   │     │  ~1.4MB/day  │     │  ~0.06MB/day │
└──────────────┘     └──────────────┘     └──────────────┘

  Storage reduction: 86MB → 1.4MB (16x) → 0.06MB (1440x)
  Query acceleration: full scan → pre-aggregated result
```

## Integration Guide

### InfluxDB Python Client

```python
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
from influxdb_client.client.query_api import QueryApi
import time

class InfluxDBClientWrapper:
    """Production InfluxDB client with retry and batching."""

    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(
            url=url,
            token=token,
            org=org,
            enable_gzip=True,
            timeout=30_000
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = bucket
        self.org = org

    def write_metric(self, measurement, tags, fields, timestamp=None):
        """Write a single data point."""
        point = Point(measurement)
        for key, value in tags.items():
            point = point.tag(key, value)
        for key, value in fields.items():
            point = point.field(key, value)
        if timestamp:
            point = point.time(timestamp, WritePrecision.MS)

        self.write_api.write(bucket=self.bucket, record=point)

    def write_batch(self, points):
        """Write multiple points in batch."""
        self.write_api.write(
            bucket=self.bucket,
            record=points,
            write_options=SYNCHRONOUS
        )

    def query_flux(self, query):
        """Execute a Flux query."""
        tables = self.query_api.query(query, org=self.org)
        results = []
        for table in tables:
            for record in table.records:
                results.append({
                    'time': record.get_time(),
                    'measurement': record.get_measurement(),
                    'field': record.get_field(),
                    'value': record.get_value()
                })
        return results

    def query_last_24h(self, measurement, field):
        """Query last 24 hours of data."""
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -24h)
          |> filter(fn: (r) => r["_measurement"] == "{measurement}")
          |> filter(fn: (r) => r["_field"] == "{field}")
          |> aggregateWindow(every: 5m, fn: mean)
          |> yield(name: "mean")
        '''
        return self.query_flux(query)

    def delete_old_data(self, days):
        """Delete data older than N days."""
        from influxdb_client.domain.delete_predicate import DeletePredicateRequest

        start = datetime.utcnow() - timedelta(days=days)
        stop = datetime.utcnow()

        predicate = DeletePredicateRequest(
            start=start.isoformat() + "Z",
            stop=stop.isoformat() + "Z",
            predicate=''
        )

        self.client.delete_api().delete(
            start=start,
            stop=stop,
            bucket=self.bucket,
            org=self.org
        )
```

### TimescaleDB Python Client

```python
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import json

class TimescaleDBClient:
    """TimescaleDB client with hypertable management."""

    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)
        self.conn.autocommit = True

    def create_hypertable(self, table, time_column, chunk_interval='1 day'):
        """Create a hypertable from existing table."""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT create_hypertable(
                    '{table}',
                    '{time_column}',
                    chunk_time_interval => INTERVAL '{chunk_interval}',
                    if_not_exists => TRUE
                )
            """)

    def insert_readings(self, table, records):
        """Batch insert sensor readings."""
        with self.conn.cursor() as cur:
            query = f"""
                INSERT INTO {table} (time, sensor_id, temperature, humidity, pressure)
                VALUES %s
            """
            execute_values(cur, query, records, page_size=1000)

    def query_time_range(self, table, sensor_id, start, end, interval='1 hour'):
        """Query aggregated data for time range."""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    time_bucket('{interval}', time) AS bucket,
                    sensor_id,
                    AVG(temperature) AS avg_temp,
                    MAX(temperature) AS max_temp,
                    MIN(temperature) AS min_temp,
                    AVG(humidity) AS avg_humidity,
                    COUNT(*) AS readings
                FROM {table}
                WHERE sensor_id = %s
                  AND time BETWEEN %s AND %s
                GROUP BY bucket, sensor_id
                ORDER BY bucket
            """, (sensor_id, start, end))
            return cur.fetchall()

    def downsample(self, source_table, target_table, interval='1 hour'):
        """Downsample data to lower resolution."""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {target_table}
                SELECT
                    time_bucket('{interval}', time) AS time,
                    sensor_id,
                    AVG(temperature) AS temperature,
                    AVG(humidity) AS humidity,
                    AVG(pressure) AS pressure
                FROM {source_table}
                WHERE time < NOW() - INTERVAL '7 days'
                GROUP BY time_bucket('{interval}', time), sensor_id
                ON CONFLICT DO NOTHING
            """)
```

### Prometheus Remote Write Integration

```python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import requests

class MetricsExporter:
    """Export time series data to Prometheus remote write."""

    def __init__(self, remote_write_url):
        self.remote_write_url = remote_write_url

    def push_metrics(self, metrics_data):
        """Push metrics to remote write endpoint."""
        import snappy
        from prometheus_client import exposition

        registry = CollectorRegistry()
        for metric_name, labels, value in metrics_data:
            gauge = Gauge(
                metric_name,
                f'{metric_name} description',
                labelnames=list(labels.keys()),
                registry=registry
            )
            gauge.labels(**labels).set(value)

        # Encode as Prometheus remote write format
        output = exposition.generate_latest(registry)
        compressed = snappy.compress(output)

        headers = {'Content-Type': 'application/x-snappy'}
        response = requests.post(
            self.remote_write_url,
            data=compressed,
            headers=headers
        )
        return response.status_code == 204
```

## Performance Optimization

### Write Optimization

| Strategy | Throughput | Latency | Use Case |
|----------|-----------|---------|----------|
| Line protocol batching | 100k+ points/sec | ~10ms | High-volume ingestion |
| UDP ingestion | 500k+ points/sec | ~1ms | Real-time telemetry |
| Write-ahead logging | 50k points/sec | ~5ms | Durability required |
| Async buffering | 200k+ points/sec | ~50ms | Batch processing |

```python
class HighThroughputWriter:
    """Optimized writer for high-volume time series data."""

    def __init__(self, client, buffer_size=10000):
        self.client = client
        self.buffer = []
        self.buffer_size = buffer_size
        self.last_flush = time.time()

    def add_point(self, measurement, tags, fields, timestamp=None):
        """Add a point to the buffer."""
        point = Point(measurement)
        for k, v in tags.items():
            point = point.tag(k, v)
        for k, v in fields.items():
            point = point.field(k, v)
        if timestamp:
            point = point.time(timestamp, WritePrecision.MS)

        self.buffer.append(point)

        if len(self.buffer) >= self.buffer_size:
            self.flush()

    def flush(self):
        """Flush buffer to database."""
        if self.buffer:
            self.client.write_batch(self.buffer)
            self.buffer = []
            self.last_flush = time.time()

    def __del__(self):
        self.flush()

# Usage: write 1 million points in ~5 seconds
writer = HighThroughputWriter(client, buffer_size=50000)
for i in range(1_000_000):
    writer.add_point(
        'cpu_usage',
        {'host': f'server_{i % 100}', 'region': 'us-east'},
        {'value': 50.0 + (i % 50), 'idle': 50.0 - (i % 50)}
    )
writer.flush()
```

### Query Optimization

```sql
-- TimescaleDB: Use continuous aggregates for dashboards
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  host,
  AVG(cpu_usage) AS avg_cpu,
  MAX(memory_used) AS max_memory,
  SUM(bytes_sent) AS total_bytes
FROM metrics_raw
GROUP BY bucket, host;

-- TimescaleDB: Partial indexes for common queries
CREATE INDEX idx_metrics_high_cpu
ON metrics_raw (time DESC, host)
WHERE cpu_usage > 90;

-- InfluxDB: Use tag indexing
-- Tags are automatically indexed; fields are not
-- Use tags for: host, region, sensor_id, status
-- Use fields for: value, description, raw_data

-- QuestDB: Use designated timestamp column
CREATE TABLE trades (
  symbol SYMBOL,
  price DOUBLE,
  amount DOUBLE,
  side SYMBOL CAPACITY 256
) TIMESTAMP(time) PARTITION BY DAY WAL
DEDUP ENABLED UPSERT KEYS(symbol, time);
```

## Security Considerations

### Authentication and Authorization

```bash
# InfluxDB: Create user with scoped permissions
influx user create --name readonly --org myorg
influx auth create --org myorg --user readonly \
  --read-bucket bucket1 \
  --read-bucket bucket2

# InfluxDB: Token management
influx auth create --org myorg \
  --write-bucket bucket1 \
  --description "Write-only token for app1"

# TimescaleDB: Role-based access
CREATE ROLE readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

CREATE ROLE app_user;
GRANT INSERT, UPDATE ON metrics_raw TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
```

```python
# InfluxDB: Token-based authentication
from influxdb_client import InfluxDBClient

client = InfluxDBClient(
    url="https://influxdb.example.com:8086",
    token="my-secret-token",
    org="myorg",
    ssl_ca_cert="/etc/influxdb/ca.crt",
    timeout=30_000
)

# TimescaleDB: SSL connection
import psycopg2

conn = psycopg2.connect(
    "host=timescaledb.example.com dbname=metrics user=app_user",
    sslmode="verify-full",
    sslcert="/etc/timescaledb/client.crt",
    sslkey="/etc/timescaledb/client.key",
    sslrootcert="/etc/timescaledb/ca.crt"
)
```

### Data Retention Policies

```bash
# InfluxDB: Create retention policy
influx retention-policy create \
  --name "short_term" \
  --duration 7d \
  --replication 3 \
  --bucket mydb

influx retention-policy create \
  --name "long_term" \
  --duration 365d \
  --replication 1 \
  --bucket mydb

# TimescaleDB: Automatic data retention
SELECT add_retention_policy('metrics_raw', INTERVAL '30 days');
SELECT add_retention_policy('metrics_hourly', INTERVAL '365 days');
```

## Troubleshooting Guide

### Common Time Series Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Write throttling | 503 errors, slow writes | Increase shard duration, batch writes |
| Query timeout | Query exceeds time limit | Use continuous aggregates, limit time range |
| High disk usage | Storage growing rapidly | Enable compression, adjust retention |
| Memory pressure | OOM kills | Reduce cache size, limit concurrent queries |
| Replication lag | Data inconsistency | Check network, increase resources |
| Out of order writes | Rejected data points | Use server timestamps or sort before write |

```python
def diagnose_timeseries_db(db_type='influxdb'):
    """Run diagnostic checks on time series database."""

    if db_type == 'influxdb':
        client = InfluxDBClient(url='http://localhost:8086')
        query_api = client.query_api()

        # Check storage engine stats
        result = query_api.query('''
            from(bucket: "_internal")
              |> range(start: -1h)
              |> filter(fn: (r) => r["_measurement"] == "tsm1_cache")
              |> last()
        ''')

        diagnostics = {}
        for table in result:
            for record in table.records:
                diagnostics[record.get_field()] = record.get_value()

        return diagnostics

    elif db_type == 'timescaledb':
        import psycopg2
        conn = psycopg2.connect('dbname=metrics')
        cur = conn.cursor()

        # Check hypertable sizes
        cur.execute("""
            SELECT hypertable_name,
                   pg_size_pretty(hypertable_size(format('%I', hypertable_name)::regclass))
            FROM timescaledb_information.hypertables
        """)
        sizes = cur.fetchall()

        # Check chunk distribution
        cur.execute("""
            SELECT chunk_name,
                   pg_size_pretty(total_bytes),
                   is_compressed
            FROM timescaledb_information.chunks
            ORDER BY range_start DESC
            LIMIT 10
        """)
        chunks = cur.fetchall()

        return {'hypertables': sizes, 'recent_chunks': chunks}
```

## API Reference

### InfluxDB Query Examples

```python
# Flux queries
queries = {
    # Average temperature over last hour
    'avg_temp': '''
        from(bucket: "mydb")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "temperature")
          |> filter(fn: (r) => r["_field"] == "value")
          |> aggregateWindow(every: 5m, fn: mean)
          |> yield(name: "average")
    ''',

    # Top 10 hosts by CPU usage
    'top_hosts': '''
        from(bucket: "mydb")
          |> range(start: -24h)
          |> filter(fn: (r) => r["_measurement"] == "cpu")
          |> filter(fn: (r) => r["_field"] == "usage_user")
          |> group(columns: ["host"])
          |> mean()
          |> sort(columns: ["_value"], desc: true)
          |> limit(n: 10)
    ''',

    # Detect anomalies (z-score)
    'anomalies': '''
        from(bucket: "mydb")
          |> range(start: -7d)
          |> filter(fn: (r) => r["_measurement"] == "temperature")
          |> aggregateWindow(every: 1h, fn: mean)
          |> map(fn: (r) => ({r with zscore: (r._value - 20.0) / 5.0}))
          |> filter(fn: (r) => r.zscore > 3.0 or r.zscore < -3.0)
    ''',

    # Forecast (simple moving average)
    'forecast': '''
        from(bucket: "mydb")
          |> range(start: -30d)
          |> filter(fn: (r) => r["_measurement"] == "sales")
          |> aggregateWindow(every: 1d, fn: mean)
          |> movingAverage(n: 7)
    '''
}
```

### TimescaleDB SQL Examples

```sql
-- Continuous aggregate with refresh
CREATE MATERIALIZED VIEW metrics_5min
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('5 minutes', time) AS time,
  host,
  AVG(temperature) AS avg_temp,
  MAX(pressure) AS max_pressure,
  COUNT(*) AS samples
FROM metrics_raw
GROUP BY time_bucket('5 minutes', time), host;

-- Query with time_bucket
SELECT
  time_bucket('1 hour', time) AS hour,
  host,
  AVG(temperature) AS avg_temp
FROM metrics_raw
WHERE time > NOW() - INTERVAL '24 hours'
  AND host = 'server01'
GROUP BY hour, host
ORDER BY hour DESC;

-- Compare periods
WITH current_period AS (
  SELECT time_bucket('1 day', time) AS day, AVG(value) AS avg_val
  FROM metrics WHERE time > NOW() - INTERVAL '7 days' GROUP BY day
),
previous_period AS (
  SELECT time_bucket('1 day', time) AS day, AVG(value) AS avg_val
  FROM metrics WHERE time BETWEEN NOW() - INTERVAL '14 days' AND NOW() - INTERVAL '7 days'
  GROUP BY day
)
SELECT
  c.day,
  c.avg_val AS current_avg,
  p.avg_val AS previous_avg,
  (c.avg_val - p.avg_val) / p.avg_val * 100 AS change_pct
FROM current_period c
JOIN previous_period p ON c.day = p.day;
```

## Data Models

### IoT Sensor Schema

```sql
-- TimescaleDB: Sensor readings
CREATE TABLE sensor_readings (
  time TIMESTAMPTZ NOT NULL,
  sensor_id TEXT NOT NULL,
  device_id TEXT NOT NULL,
  location GEOGRAPHY(POINT, 4326),
  temperature DOUBLE PRECISION,
  humidity DOUBLE PRECISION,
  pressure DOUBLE PRECISION,
  battery_level DOUBLE PRECISION,
  metadata JSONB
);

SELECT create_hypertable('sensor_readings', 'time');

-- Index for common queries
CREATE INDEX idx_sensor_time ON sensor_readings (sensor_id, time DESC);
CREATE INDEX idx_device ON sensor_readings (device_id);
```

### Application Metrics Schema

```python
# InfluxDB measurement design
INFLUX_SCHEMA = """
# Measurements and their fields/tags

# CPU metrics
cpu_usage
  tags: host, region, datacenter
  fields: usage_user, usage_system, usage_idle, load_1, load_5, load_15

# Memory metrics
memory
  tags: host, region
  fields: total, used, free, cached, buffers, available

# Disk metrics
disk_io
  tags: host, device
  fields: read_bytes, write_bytes, read_time, write_time

# Network metrics
network
  tags: host, interface
  fields: bytes_recv, bytes_sent, packets_recv, packets_sent, errors_in, errors_out

# Application metrics
http_requests
  tags: host, method, status, endpoint
  fields: count, latency_p50, latency_p99, error_rate

# Business metrics
orders
  tags: region, product_category
  fields: count, revenue, avg_order_value
"""
```

## Deployment Guide

### InfluxDB Docker Compose

```yaml
version: '3.8'

services:
  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    ports:
      - "8086:8086"
      - "8088:8088"  # Backup/restore
      - "8089:8089/udp"  # UDP
    volumes:
      - influxdb-data:/var/lib/influxdb2
      - influxdb-config:/etc/influxdb2
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: admin
      DOCKER_INFLUXDB_INIT_PASSWORD: secret123
      DOCKER_INFLUXDB_INIT_ORG: myorg
      DOCKER_INFLUXDB_INIT_BUCKET: mydb
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: my-super-secret-token
    healthcheck:
      test: ["CMD", "influx", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  telegraf:
    image: telegraf:1.28
    container_name: telegraf
    depends_on:
      - influxdb
    volumes:
      - ./telegraf.conf:/etc/telegraf/telegraf.conf

volumes:
  influxdb-data:
  influxdb-config:
```

### TimescaleDB Kubernetes

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: timescaledb
spec:
  serviceName: timescaledb
  replicas: 3
  selector:
    matchLabels:
      app: timescaledb
  template:
    metadata:
      labels:
        app: timescaledb
    spec:
      containers:
        - name: timescaledb
          image: timescale/timescaledb-ha:pg16-latest
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: password
          volumeMounts:
            - name: pgdata
              mountPath: /home/postgres/pgdata/data
          resources:
            requests:
              memory: "4Gi"
              cpu: "2"
            limits:
              memory: "8Gi"
              cpu: "4"
  volumeClaimTemplates:
    - metadata:
        name: pgdata
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 100Gi
```

## Monitoring & Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define time series metrics
TSDB_INGEST = Counter('tsdb_ingest_total', 'Total points ingested', ['measurement'])
TSDB_INGEST_ERRORS = Counter('tsdb_ingest_errors_total', 'Ingestion errors', ['type'])
TSDB_QUERY_LATENCY = Histogram('tsdb_query_latency_seconds', 'Query latency', ['query_type'])
TSDB_STORAGE_SIZE = Gauge('tsdb_storage_bytes', 'Storage size', ['database'])
TSDB_POINTS_RATE = Gauge('tsdb_points_per_second', 'Current write rate')

class TSDBMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.points_written = 0

    def record_write(self, count, measurement):
        TSDB_INGEST.labels(measurement=measurement).inc(count)
        self.points_written += count
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            TSDB_POINTS_RATE.set(self.points_written / elapsed)

    def record_query(self, query_type, duration):
        TSDB_QUERY_LATENCY.labels(query_type=query_type).observe(duration)

    def get_stats(self):
        return {
            'points_written': self.points_written,
            'runtime_seconds': time.time() - self.start_time,
            'write_rate': self.points_written / max(time.time() - self.start_time, 1)
        }
```

## Testing Strategy

```python
import pytest
from datetime import datetime, timedelta

@pytest.fixture
def tsdb_client():
    """Create test time series database client."""
    from influxdb_client import InfluxDBClient
    client = InfluxDBClient(url='http://localhost:8086', token='test-token', org='test')
    yield client
    client.close()

class TestTimeSeriesOperations:
    def test_write_and_query(self, tsdb_client):
        write_api = tsdb_client.write_api()
        query_api = tsdb_client.query_api()

        # Write test data
        from influxdb_client import Point
        points = []
        for i in range(100):
            point = (
                Point('test_measurement')
                .tag('host', 'test_host')
                .field('value', float(i))
                .time(datetime.utcnow() - timedelta(minutes=100-i))
            )
            points.append(point)

        write_api.write(bucket='test_bucket', record=points)

        # Query and verify
        result = query_api.query('''
            from(bucket: "test_bucket")
              |> range(start: -2h)
              |> filter(fn: (r) => r["_measurement"] == "test_measurement")
              |> count()
        ''')

        assert len(result) > 0

    def test_aggregation(self, tsdb_client):
        """Test time-based aggregation."""
        query_api = tsdb_client.query_api()

        result = query_api.query('''
            from(bucket: "test_bucket")
              |> range(start: -1h)
              |> filter(fn: (r) => r["_measurement"] == "test_measurement")
              |> aggregateWindow(every: 10m, fn: mean)
              |> yield(name: "mean")
        ''')

        assert len(result) > 0
        for table in result:
            for record in table.records:
                assert record.get_value() is not None
```

## Versioning & Migration

```python
class TimeSeriesMigration:
    """Schema migration for time series databases."""

    def __init__(self, client):
        self.client = client

    def migrate_influxdb(self, bucket, org):
        """Migrate InfluxDB bucket schema."""
        migrations = [
            self._add_tags,
            self._create_continuous_aggregate,
            self._set_retention_policy,
        ]

        for migration in migrations:
            migration(bucket, org)

    def _add_tags(self, bucket, org):
        """Add new tags (schema-on-write, but update views)."""
        pass  # InfluxDB is schemaless for tags

    def _create_continuous_aggregate(self, bucket, org):
        """Create or update continuous aggregate."""
        from influxdb_client import InfluxDBClient
        query_api = self.client.query_api()
        query_api.query('''
            option task = {name: "aggregate_hourly", every: 1h}

            from(bucket: "raw")
              |> range(start: -task.every)
              |> filter(fn: (r) => r["_measurement"] == "metrics")
              |> aggregateWindow(every: 1h, fn: mean)
              |> to(bucket: "aggregated", org: "myorg")
        ''', org=org)

    def _set_retention_policy(self, bucket, org):
        """Set retention policy."""
        pass  # Handled via InfluxDB API
```

## Glossary

| Term | Definition |
|------|------------|
| Hypertable | Time-partitioned table (TimescaleDB) |
| Chunk | Time-based partition of a hypertable |
| TSM | Time-Structured Merge tree (InfluxDB storage engine) |
| Line Protocol | InfluxDB's text-based write format |
| Flux | InfluxDB's functional query language |
| Continuous Aggregate | Pre-computed, auto-refreshing materialized view |
| Downsampling | Reducing data resolution over time |
| Retention Policy | Rules for automatic data deletion |
| Tag | Metadata indexable field (InfluxDB) |
| Field | Non-indexed data value (InfluxDB) |
| Measurement | Similar to a table name (InfluxDB) |
| Bucket | Top-level container for data (InfluxDB 2.x) |
| WAL | Write-Ahead Log for crash recovery |
| TSM Cache | In-memory cache for recent writes |
| Compaction | Merging TSM files for efficiency |
| Designated Timestamp | Required timestamp column (QuestDB) |
| Continuous Aggregate Policy | Automatic refresh schedule |
| Materialized View | Pre-computed query result |
| Remote Write | Prometheus protocol for sending metrics |
| Scrape | Periodic metric collection (Prometheus) |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release with InfluxDB basics |
| 1.1.0 | 2024-03-01 | Added TimescaleDB integration |
| 1.2.0 | 2024-05-01 | Added QuestDB support and architecture patterns |
| 1.3.0 | 2024-07-01 | Added performance optimization and downsampling |
| 1.4.0 | 2024-09-01 | Added security hardening and retention policies |
| 1.5.0 | 2024-11-01 | Added monitoring with Prometheus integration |
| 1.6.0 | 2025-01-01 | Expanded testing, deployment, and troubleshooting |

## Contributing Guidelines

1. **Data Model**: Document measurement schema and tag cardinality
2. **Performance**: Include benchmarks for write throughput and query latency
3. **Compression**: Test compression ratios for new data patterns
4. **Retention**: Define retention policies for all time series data
5. **Monitoring**: Add health checks and alerting for all databases

## License

This module is part of the Awesome-Grok-Skills project and follows the MIT License.
