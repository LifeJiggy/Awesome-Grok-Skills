---
name: "document-stores"
category: "nosql-databases"
version: "1.0.0"
tags: ["nosql-databases", "document-stores"]
---

# Document Stores

## Overview

Comprehensive document-stores capabilities within the nosql-databases domain. This module provides tools, frameworks, and best practices for document-stores operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from document-stores import _module

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

### CouchDB Configuration

```ini
# local.ini - CouchDB production configuration
[chttpd]
port = 5984
bind_address = 0.0.0.0
require_valid_user = true
max_http_request_size = 4294967296
enable_cors = false

[httpd]
WWW-Authenticate = Basic realm="CouchDB"
require_valid_user = true
authentication_redirect = /_utils/session.html

[couchdb]
max_document_size = 50000000
uuids = sequential
max_dbs_open = 100
fd_limit = 65536

[cluster]
n = 3
q = 2
r = 2
w = 2

[compactions]
db = [{db_name, "_default"}, {single_from, 0}, {schedule, "0 1 * * *"}]

[replicator]
max_replication_retry_count = 10
checkpoint_interval = 10000
worker_processes = 4
```

### RethinkDB Configuration

```javascript
// rethinkdb.conf
-- Cluster configuration
cluster-port = 29015
driver-port = 28015
http-port = 8080
bind = all

-- Cache configuration
cache-size = 1024  // MB per core

-- Replication
hard-reconnect-timeout = 30
heartbeat-period = 10

-- Logging
log = /var/log/rethinkdb
log-level = info

-- Security
web-cert-file = /etc/rethinkdb/ssl/server.crt
web-key-file = /etc/rethinkdb/ssl/server.key
```

### ArangoDB Configuration

```json
// arangod.conf
{
  "server": {
    "address": "0.0.0.0",
    "port": 8529,
    "authentication": true,
    "cluster-sample-size": 1000
  },
  "database": {
    "path": "/var/lib/arangodb3",
    "max-database-size": "8G"
  },
  "log": {
    "level": "info",
    "file": "/var/log/arangod.log",
    "color": false
  },
  "rocksdb": {
    "cache-size": "2G",
    "max-threads": 8,
    "block-cache-size": "1G"
  },
  "cluster": {
    "my-address": "10.0.0.1:8529",
    "my-role": "AUTO",
    "default-replication-factor": 3
  }
}
```

## Architecture Patterns

### Document Store Pattern Variants

```
┌─────────────────────────────────────────────────────────────────┐
│                    Document Store Patterns                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Embedding (denormalization)                                 │
│  ┌─────────────────────────────────┐                            │
│  │ {                               │                            │
│  │   "id": "order_123",           │                            │
│  │   "customer": {                │                            │
│  │     "name": "Alice",           │  ← Embedded subdocument    │
│  │     "email": "a@b.com"         │                            │
│  │   },                           │                            │
│  │   "items": [                   │  ← Embedded array          │
│  │     {"product": "X", "qty": 2} │                            │
│  │   ]                            │                            │
│  │ }                              │                            │
│  └─────────────────────────────────┘                            │
│                                                                 │
│  2. Referencing (normalization)                                 │
│  ┌────────────────────┐  ┌────────────────────┐                │
│  │ {                  │  │ {                  │                │
│  │   "id": "order_1" │  │   "id": "cust_1"  │                │
│  │   "customer_id": ─┼──┼→ "name": "Alice"  │                │
│  │ }                  │  │ }                  │                │
│  └────────────────────┘  └────────────────────┘                │
│                                                                 │
│  3. Bucket pattern (time-series)                               │
│  ┌─────────────────────────────────┐                            │
│  │ {                               │                            │
│  │   "sensor_id": "s1",           │                            │
│  │   "date": "2024-01-15",        │                            │
│  │   "readings": [                │  ← Time-bucketed data     │
│  │     {"t": 1705312800, "v": 23.5},│                          │
│  │     {"t": 1705312860, "v": 24.1} │                          │
│  │   ]                            │                            │
│  │ }                              │                            │
│  └─────────────────────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

### Replication Topology

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Primary    │────▶│  Secondary   │────▶│  Secondary   │
│   Node       │     │  Node 1      │     │  Node 2      │
└──────────────┘     └──────────────┘     └──────────────┘
       │
       │    ┌──────────────┐     ┌──────────────┐
       └───▶│  Secondary   │────▶│  Secondary   │
            │  Node 3      │     │  Node 4      │
            └──────────────┘     └──────────────┘

  Replication Factor: 3
  Read Consistency: majority
  Write Consistency: majority
  Automatic failover: enabled
```

## Integration Guide

### CouchDB Python Client

```python
import requests
from requests.auth import HTTPBasicAuth
import json

class CouchDBClient:
    """CouchDB client with replication support."""

    def __init__(self, host, port, username, password):
        self.base_url = f"http://{host}:{port}"
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({'Content-Type': 'application/json'})

    def create_database(self, db_name):
        """Create a new database."""
        response = self.session.put(f"{self.base_url}/{db_name}")
        return response.status_code == 201

    def put_document(self, db_name, doc_id, document):
        """Insert or update a document."""
        response = self.session.put(
            f"{self.base_url}/{db_name}/{doc_id}",
            data=json.dumps(document)
        )
        return response.json()

    def get_document(self, db_name, doc_id):
        """Retrieve a document."""
        response = self.session.get(f"{self.base_url}/{db_name}/{doc_id}")
        if response.status_code == 200:
            return response.json()
        return None

    def query_view(self, db_name, design_doc, view_name, key=None):
        """Query a MapReduce view."""
        params = {}
        if key:
            params['key'] = json.dumps(key)

        response = self.session.get(
            f"{self.base_url}/{db_name}/_design/{design_doc}/_view/{view_name}",
            params=params
        )
        return response.json()

    def bulk_insert(self, db_name, documents):
        """Bulk insert documents."""
        payload = {'docs': documents}
        response = self.session.post(
            f"{self.base_url}/{db_name}/_bulk_docs",
            data=json.dumps(payload)
        )
        return response.json()

    def replicate(self, source_db, target_db):
        """Trigger replication between databases."""
        payload = {
            'source': source_db,
            'target': target_db,
            'create_target': True
        }
        response = self.session.post(
            f"{self.base_url}/_replicate",
            data=json.dumps(payload)
        )
        return response.json()
```

### RethinkDB Python Client

```python
import rethinkdb as r

class RethinkDBClient:
    """RethinkDB client with Changefeed support."""

    def __init__(self, host='localhost', port=28015):
        self.conn = r.connect(host, port)

    def create_table(self, db_name, table_name):
        """Create database and table."""
        r.db_create(db_name).run(self.conn)
        r.db(db_name).table_create(table_name).run(self.conn)

    def insert(self, db_name, table_name, documents):
        """Insert documents."""
        result = r.db(db_name).table(table_name).insert(documents).run(self.conn)
        return result

    def query(self, db_name, table_name, filter_func=None):
        """Query with optional filter."""
        query = r.db(db_name).table(table_name)
        if filter_func:
            query = query.filter(filter_func)
        return list(query.run(self.conn))

    def update(self, db_name, table_name, doc_id, updates):
        """Update a document."""
        result = r.db(db_name).table(table_name).get(doc_id).update(updates).run(self.conn)
        return result

    def watch_changes(self, db_name, table_name, callback):
        """Watch for real-time changes."""
        def on_change(feed):
            for change in feed:
                callback(change)

        r.db(db_name).table(table_name).changes().run(self.conn, on_change)
```

### ArangoDB Python Client

```python
from arango import ArangoClient

class ArangoDBClient:
    """ArangoDB client with graph support."""

    def __init__(self, hosts, username, password):
        self.client = ArangoClient(hosts=hosts)
        self.db = self.client.db(
            'mydb',
            username=username,
            password=password
        )

    def create_graph(self, graph_name, edge_collections):
        """Create an ArangoDB graph."""
        if not self.db.has_graph(graph_name):
            graph = self.db.create_graph(graph_name)
            for edge_name in edge_collections:
                graph.create_edge_definition(
                    edge_collection=edge_name,
                    from_vertex_collections=['users', 'posts'],
                    to_vertex_collections=['users', 'posts']
                )

    def aql_query(self, query, bind_vars=None):
        """Execute an AQL query."""
        cursor = self.db.aql.execute(query, bind_vars=bind_vars or {})
        return list(cursor)

    def traverse_graph(self, graph_name, start_vertex, depth=2):
        """Graph traversal query."""
        query = """
        FOR v, e, p IN 1..@depth OUTBOUND @start GRAPH @graph
            RETURN {vertex: v, edge: e, path: p}
        """
        return self.aql_query(query, {
            'graph': graph_name,
            'start': start_vertex,
            'depth': depth
        })
```

## Performance Optimization

### Indexing Strategies

```javascript
// CouchDB MapReduce indexes
// _design/products/_view/by_category
{
  "map": "function(doc) { if (doc.type === 'product') emit(doc.category, doc.price); }",
  "reduce": "_sum"
}

// CouchDB Mango indexes
{
  "index": {
    "fields": ["type", "category", "price"]
  },
  "type": "json",
  "name": "product_search_index"
}

// RethinkDB secondary indexes
r.table('products').indexCreate('category_price', [r.row('category'), r.row('price')]).run(conn)
r.table('products').indexStatus('category_price').run(conn)

// ArangoDB indexes
db.products.ensureIndex({type: 'hash', fields: ['category']})
db.products.ensureIndex({type: 'skiplist', fields: ['price', 'rating']})
db.products.ensureIndex({type: 'fulltext', fields: ['name', 'description']})
```

### Query Optimization Table

| Database | Operation | Unoptimized | Optimized |
|----------|-----------|-------------|-----------|
| CouchDB | Range query | Full scan | Mango index |
| RethinkDB | Filter | `filter()` | Secondary index + `between()` |
| ArangoDB | Graph traversal | `FOR v IN 1..10` | `OUTBOUND` with index |
| MongoDB | Text search | `$where` | `$text` index |

```python
# Performance comparison
def benchmark_queries(db_client, iterations=1000):
    """Benchmark different query patterns."""
    import time

    # Unoptimized: full table scan
    start = time.time()
    for _ in range(iterations):
        db_client.query('products', filter_func=lambda doc: doc['price'] < 50)
    scan_time = time.time() - start

    # Optimized: indexed query
    start = time.time()
    for _ in range(iterations):
        db_client.table('products').between({'price': 0}, {'price': 50}).run(db_client.conn)
    index_time = time.time() - start

    return {
        'scan': scan_time,
        'index': index_time,
        'speedup': scan_time / index_time
    }
```

## Security Considerations

### Authentication Configuration

```javascript
// CouchDB: Create admin user
curl -X PUT http://localhost:5984/_users/org.couchdb.user:admin \
  -H "Content-Type: application/json" \
  -d '{"name":"admin", "password":"secret", "roles":[], "type":"user"}'

// CouchDB: Create database-specific user
curl -X PUT http://localhost:5984/_users/org.couchdb.user:appuser \
  -H "Content-Type: application/json" \
  -d '{"name":"appuser", "password":"pass123", "roles":["db_reader"], "type":"user"}'

// CouchDB: Set database security
curl -X PUT http://localhost:5984/mydb/_security \
  -H "Content-Type: application/json" \
  -d '{
    "admins": {"names": ["admin"], "roles": []},
    "members": {"names": ["appuser"], "roles": ["db_reader"]}
  }'
```

```python
# RethinkDB: Enable authentication
# In rethinkdb.conf:
# server-password = <hashed_password>

# RethinkDB: Create user table
r.db('rethinkdb').table('users').insert({
    'id': 'appuser',
    'password': hashed_password,
    'databases': {'mydb': ['read', 'write']}
}).run(conn)
```

### SSL/TLS Setup

```python
import ssl
import requests

# CouchDB with SSL
ssl_context = ssl.create_default_context()
ssl_context.load_cert_chain('/etc/couchdb/server.crt', '/etc/couchdb/server.key')
ssl_context.load_verify_locations('/etc/couchdb/ca.crt')

session = requests.Session()
session.verify = '/etc/couchdb/ca.crt'
session.cert = ('/etc/couchdb/client.crt', '/etc/couchdb/client.key')

# Connect to CouchDB over HTTPS
response = session.get('https://couchdb-server:6984/')
```

## Troubleshooting Guide

### Common Document Store Issues

| Issue | Database | Symptom | Resolution |
|-------|----------|---------|------------|
| Conflict resolution | CouchDB | 409 Conflict | Use `rev` field, implement conflict handler |
| Shard imbalance | CouchDB | Uneven load | Rebalance shards with `shard_reshard` |
| Changefeed lag | RethinkDB | Delayed updates | Increase `feed_queue_size`, check disk |
| Index bloat | ArangoDB | Slow queries | Run `UNLOAD` and reindex |
| Memory leak | All | Growing RSS | Check connection pools, restart workers |

```python
def diagnose_couchdb(conflict_threshold=10):
    """Diagnose CouchDB issues."""
    import requests

    # Check cluster status
    response = requests.get('http://localhost:5984/_membership')
    membership = response.json()

    print(f"Cluster nodes: {len(membership['cluster_nodes'])}")
    print(f"All nodes: {len(membership['all_nodes'])}")

    # Check active tasks
    response = requests.get('http://localhost:5984/_active_tasks')
    tasks = response.json()
    print(f"Active tasks: {len(tasks)}")

    # Check for conflicts in recent documents
    response = requests.get('http://localhost:5984/mydb/_changes?include_docs=true&limit=100')
    changes = response.json()
    conflicts = sum(1 for row in changes['results'] if '_conflicts' in row.get('doc', {}))
    if conflicts > conflict_threshold:
        print(f"WARNING: {conflicts} documents have conflicts")

    return {
        'nodes': len(membership['cluster_nodes']),
        'tasks': len(tasks),
        'conflicts': conflicts
    }
```

## API Reference

### CouchDB REST API

```bash
# Create database
curl -X PUT http://localhost:5984/mydb

# Insert document
curl -X POST http://localhost:5984/mydb \
  -H "Content-Type: application/json" \
  -d '{"type": "user", "name": "Alice"}'

# Get document
curl http://localhost:5984/mydb/doc_id

# Update document (with revision)
curl -X PUT http://localhost:5984/mydb/doc_id \
  -H "Content-Type: application/json" \
  -d '{"_rev": "1-abc", "name": "Alice Updated"}'

# Delete document
curl -X DELETE http://localhost:5984/mydb/doc_id?rev=1-abc

# Query view
curl "http://localhost:5984/mydb/_design/app/_view/users?include_docs=true&limit=10"

# Mango query
curl -X POST http://localhost:5984/mydb/_find \
  -H "Content-Type: application/json" \
  -d '{
    "selector": {"type": "user", "age": {"$gte": 21}},
    "sort": [{"age": "asc"}],
    "limit": 50
  }'
```

### RethinkDB ReQL API

```python
import rethinkdb as r

# Create table with durability
r.db('mydb').table_create('users', durability='hard').run(conn)

# Insert with return changes
result = r.db('mydb').table('users').insert(
    {'name': 'Alice', 'email': 'alice@example.com'},
    return_changes=True
).run(conn)

# Advanced query with chaining
result = r.db('mydb').table('orders') \
    .between(r.time(2024, 1, 1), r.time(2024, 12, 31)) \
    .filter(lambda order: order['status'] == 'completed') \
    .group('customer_id') \
    .sum('amount') \
    .ungroup() \
    .order_by(r.desc('reduction')) \
    .limit(10) \
    .run(conn)

# Geospatial query
r.db('mydb').table('stores') \
    .getNear(37.7749, -122.4194, maxDist=5000) \
    .run(conn)

# Changefeed
def on_change(change):
    print(f"Change: {change['new_val']}")

r.db('mydb').table('users').changes().run(conn, on_change)
```

## Data Models

### Product Catalog (CouchDB)

```json
{
  "_id": "product:12345",
  "_rev": "3-abc123",
  "type": "product",
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "category": "electronics",
  "price": 29.99,
  "inventory": {
    "warehouse_a": 150,
    "warehouse_b": 200
  },
  "attributes": {
    "color": "black",
    "weight": "120g",
    "connectivity": "Bluetooth 5.0"
  },
  "reviews": [
    {"user": "bob", "rating": 5, "text": "Great mouse!"},
    {"user": "carol", "rating": 4, "text": "Good value"}
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-06-20T14:22:00Z"
}
```

### Social Network Graph (ArangoDB)

```javascript
// Vertex collections
// users: {_key: "u1", name: "Alice", email: "a@b.com"}
// posts: {_key: "p1", title: "Hello World", content: "...", author: "u1"}

// Edge collection
// follows: {_key: "f1", _from: "users/u1", _from: "users/u2", since: "2024-01-01"}
// likes: {_key: "l1", _from: "users/u2", _to: "posts/p1", timestamp: "2024-01-15"}

// AQL graph query
FOR v, e, p IN 1..3 OUTBOUND 'users/u1' follows, likes
  FILTER v.type == 'user'
  RETURN DISTINCT {
    name: v.name,
    distance: LENGTH(p.edges),
    last_edge: p.edges[-1].type
  }
```

## Deployment Guide

### CouchDB Cluster Docker Compose

```yaml
version: '3.8'

services:
  couchdb1:
    image: couchdb:3.3
    container_name: couchdb1
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: secret
      NODENAME: couchdb1
    ports:
      - "5984:5984"
    volumes:
      - couchdb1-data:/opt/couchdb/data
    command: >
      bash -c "
        echo '[couchdb]' > /opt/couchdb/etc/local.ini &&
        echo 'single_node=true' >> /opt/couchdb/etc/local.ini &&
        /docker-entrypoint.sh /opt/couchdb/bin/couchdb
      "

  couchdb2:
    image: couchdb:3.3
    container_name: couchdb2
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: secret
      NODENAME: couchdb2
    volumes:
      - couchdb2-data:/opt/couchdb/data
    depends_on:
      - couchdb1

  couchdb3:
    image: couchdb:3.3
    container_name: couchdb3
    environment:
      COUCHDB_USER: admin
      COUCHDB_PASSWORD: secret
      NODENAME: couchdb3
    volumes:
      - couchdb3-data:/opt/couchdb/data
    depends_on:
      - couchdb1

volumes:
  couchdb1-data:
  couchdb2-data:
  couchdb3-data:
```

## Monitoring & Observability

### CouchDB Statistics

```python
import requests
import time

class CouchDBMonitor:
    def __init__(self, host, port, username, password):
        self.base_url = f"http://{host}:{port}"
        self.auth = (username, password)

    def get_server_stats(self):
        """Get CouchDB server statistics."""
        response = requests.get(
            f"{self.base_url}/_stats",
            auth=self.auth
        )
        stats = response.json()

        return {
            'httpd_requests': stats.get('couchdb', {}).get('httpd', {}).get('request_methods', {}),
            'open_databases': stats.get('couchdb', {}).get('open_databases', {}).get('value', 0),
            'open_connections': stats.get('couchdb', {}).get('open_connections', {}).get('value', 0),
            'disk_size': stats.get('couchdb', {}).get('disk_size', {}).get('value', 0),
            'document_count': stats.get('couchdb', {}).get('document_count', {}).get('value', 0)
        }

    def get_active_tasks(self):
        """Get currently running tasks."""
        response = requests.get(
            f"{self.base_url}/_active_tasks",
            auth=self.auth
        )
        return response.json()

    def monitor_loop(self, interval=30):
        """Continuously monitor CouchDB."""
        while True:
            stats = self.get_server_stats()
            print(f"Databases: {stats['open_databases']}, "
                  f"Connections: {stats['open_connections']}, "
                  f"Documents: {stats['document_count']:,}")
            time.sleep(interval)
```

## Testing Strategy

### CouchDB Unit Tests

```python
import pytest
import requests
from couchdb_client import CouchDBClient

@pytest.fixture
def couch_client():
    return CouchDBClient('localhost', 5984, 'admin', 'secret')

class TestCouchDB:
    def test_create_database(self, couch_client):
        assert couch_client.create_database('test_db')
        # Cleanup
        requests.delete('http://localhost:5984/test_db', auth=('admin', 'secret'))

    def test_insert_and_get(self, couch_client):
        couch_client.create_database('test_db')
        doc = {'type': 'user', 'name': 'Alice'}
        result = couch_client.put_document('test_db', 'user1', doc)
        assert 'ok' in result

        retrieved = couch_client.get_document('test_db', 'user1')
        assert retrieved['name'] == 'Alice'

        requests.delete('http://localhost:5984/test_db', auth=('admin', 'secret'))

    def test_bulk_insert(self, couch_client):
        couch_client.create_database('test_db')
        docs = [
            {'_id': f'doc{i}', 'type': 'test', 'value': i}
            for i in range(100)
        ]
        result = couch_client.bulk_insert('test_db', docs)
        assert len(result['results']) == 100

        requests.delete('http://localhost:5984/test_db', auth=('admin', 'secret'))
```

## Versioning & Migration

```python
class DocumentStoreMigration:
    """Version-controlled migrations for document stores."""

    def __init__(self, client, db_name):
        self.client = client
        self.db_name = db_name
        self._ensure_migrations_db()

    def _ensure_migrations_db(self):
        self.client.create_database('_migrations')

    def get_current_version(self):
        doc = self.client.get_document('_migrations', 'schema_version')
        return doc['version'] if doc else 0

    def migrate(self, version, up_func):
        current = self.get_current_version()
        if current >= version:
            return False

        up_func(self.client, self.db_name)

        self.client.put_document('_migrations', 'schema_version', {
            'version': version,
            'applied_at': datetime.utcnow().isoformat()
        })
        return True

# Example migrations
def v1_add_email_index(client, db_name):
    """Create email index."""
    requests.post(
        f"http://localhost:5984/{db_name}/_index",
        json={
            "index": {"fields": ["email"]},
            "type": "json",
            "name": "email_index"
        }
    )

def v2_normalize_reviews(client, db_name):
    """Normalize review structure."""
    # Migration logic here
    pass
```

## Glossary

| Term | Definition |
|------|------------|
| Document | A self-contained data structure (JSON, BSON, etc.) |
| Collection | Group of related documents (like a table) |
| View | Pre-computed query result (CouchDB MapReduce) |
| Mango | MongoDB-style query language for CouchDB |
| Changefeed | Real-time notification of document changes |
| Revision | Version identifier for conflict detection |
| Conflict | Concurrent modifications to the same document |
| Shard | Horizontal partition of data across nodes |
| Replication | Copying data between nodes for redundancy |
| Upsert | Insert or update if exists operation |
| Embedding | Storing related data within a document |
| Referencing | Storing references to other documents |
| Index | Data structure for fast query execution |
| Partition | Logical grouping of data in some stores |
| Durability | Guarantee that writes persist to disk |
| Write-ahead log | Pre-write log for crash recovery |
| Buffer pool | In-memory cache for frequently accessed data |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release with CouchDB, RethinkDB basics |
| 1.1.0 | 2024-03-01 | Added ArangoDB integration and graph patterns |
| 1.2.0 | 2024-05-01 | Added performance optimization and indexing |
| 1.3.0 | 2024-07-01 | Added security hardening and SSL setup |
| 1.4.0 | 2024-09-01 | Added monitoring and observability |
| 1.5.0 | 2024-11-01 | Added testing and migration patterns |
| 1.6.0 | 2025-01-01 | Expanded API reference and troubleshooting |

## Contributing Guidelines

1. **Database Choice**: Justify database selection based on use case
2. **Schema Design**: Document access patterns and index strategy
3. **Testing**: Include integration tests with actual database instances
4. **Security**: Never hardcode credentials; use secrets management
5. **Documentation**: Update access pattern documentation

## License

This module is part of the Awesome-Grok-Skills project and follows the MIT License.
