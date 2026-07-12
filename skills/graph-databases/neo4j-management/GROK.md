---
name: neo4j-management
category: graph-databases
version: 1.0.0
tags:
  - neo4j
  - cypher
  - graph-database
  - administration
  - clustering
difficulty: intermediate
estimated_time: 45 minutes
prerequisites:
  - basic-sql
  - graph-theory-basics
  - python-3.10+
---

# Neo4j Database Management

Operational guide for running Neo4j in production and development: Cypher query patterns, index strategy, cluster administration, backup/restore pipelines, and performance tuning.

## Core Concepts

Neo4j stores data as nodes, relationships, and properties. Unlike relational databases, relationships are first-class citizens stored as pointers, enabling constant-time traversal regardless of graph size. This storage model makes graph-native queries orders of magnitude faster than JOIN-based equivalents for connected data.

### Property Graph Model

Every node can have zero or more labels (type tags) and key-value properties. Relationships always have a direction, a type, and optional properties. The property graph model is more flexible than RDF triples for application-level data because properties can live on both nodes and edges.

### ACID Transactions

Neo4j provides full ACID transactional guarantees. Every read and write operation occurs within a transaction that can be committed or rolled back. This is critical for maintaining graph consistency when updating multiple connected elements atomically.

## Cypher Query Language

Cypher is Neo4j's declarative graph query language. It uses ASCII-art pattern syntax where parentheses represent nodes and arrows represent relationships.

### Basic Pattern Matching

```cypher
// Find all persons who work at a company
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.name = 'Acme Corp'
RETURN p.name, p.email

// Variable-length paths: find all colleagues within 3 hops
MATCH (p:Person)-[:WORKS_AT*1..3]->(c:Company)
RETURN p.name, c.name

// Optional matching (LEFT JOIN equivalent)
MATCH (p:Person)
OPTIONAL MATCH (p)-[:OWNS]->(v:Vehicle)
RETURN p.name, v.model
```

### Aggregation and Grouping

```cypher
// Count connections per node
MATCH (p:Person)-[r:FRIEND]->(friend:Person)
RETURN p.name, count(friend) AS friendCount
ORDER BY friendCount DESC

// Average path length in network
MATCH path = (a:Person)-[:FRIEND*1..6]->(b:Person)
WHERE id(a) < id(b)
RETURN avg(length(path)) AS avgDistance
```

### writes and Updates

```cypher
// Create nodes and relationships atomically
CREATE (p:Person {name: $name, email: $email})
CREATE (c:Company {name: $company})
CREATE (p)-[:WORKS_AT {since: date()}]->(c)

// Merge: create if not exists, match if exists
MERGE (p:Person {email: $email})
ON CREATE SET p.created = datetime()
ON MATCH SET p.lastSeen = datetime()
```

## Index Management

Indexes are critical for query performance. Without indexes, Neo4j performs full graph scans for every property lookup.

### Index Types

```cypher
// B-tree index (default, good for equality and range)
CREATE INDEX person_email FOR (p:Person) ON (p.email)

// Full-text index for text search
CREATE FULLTEXT INDEX personSearch FOR (p:Person) ON EACH [p.name, p.email]

// Range index for numeric/date ranges
CREATE RANGE INDEX event_timestamp FOR (e:Event) ON (e.timestamp)

// Point index for geospatial queries
CREATE POINT INDEX location_index FOR (l:Location) ON (l.coordinates)

// Composite index for multi-property lookups
CREATE INDEX person_name_email FOR (p:Person) ON (p.name, p.email)
```

### Index Monitoring

```cypher
// Show all indexes and their state
SHOW INDEXES

// Check index usage statistics
CALL db.index.fulltext.queryNodes('personSearch', 'John')
YIELD node, score
RETURN node.name, score

// Drop unused indexes
DROP INDEX person_email IF EXISTS
```

## Cluster Administration

Neo4j Enterprise supports causal clustering with Core (consensus) and Read Replica servers.

### Cluster Operations

```cypher
// Check cluster status
CALL dbms.cluster.overview()

// Check instance role
CALL dbms.instance.role()

// Force leader re-election (maintenance only)
CALL dbms.cluster.forceLeaderReElection()

// Show cluster topology
CALL dbms.listConfig()
WHERE name = 'causal_clustering.member_discovery'
YIELD name, value
```

### Read Replicas

```cypher
// Create a read replica (from cluster leader)
:POST /db/manage/server/causalclustering/add-replica
{
  "serverId": "replica-01",
  "address": "replica01.internal:6366"
}

// Route read queries to replicas automatically
:POST /db/{dbname}/tx/commit
{
  "statements": [{
    "query": "MATCH (n) RETURN count(n)",
    "parameters": {},
    "resultDataContents": ["row"]
  }],
  "metadata": {
    "route": "read"
  }
}
```

## Backup and Restore

### Online Backup

```bash
# Backup from running instance (Enterprise)
neo4j-admin database backup --from=neo4j://core01:6362 \
  --backup-dir=/backups/neo4j \
  --name=graph.db-backup

# Verify backup integrity
neo4j-admin database backup verify --backup-dir=/backups/neo4j

# Restore from backup
neo4j-admin database restore --from=/backups/neo4j/graph.db-backup \
  --to=graph.db
```

### Consistency Checks

```bash
# Check database consistency before upgrade
neo4j-admin database check --store=/data/databases/graph.db

# Fix detected inconsistencies
neo4j-admin database recover --store=/data/databases/graph.db
```

## Performance Tuning

### Query Optimization

```cypher
// Use EXPLAIN to check query plan
EXPLAIN MATCH (p:Person)-[:FRIEND]->(f:Person)
WHERE p.age > 25
RETURN p.name, f.name

// Profile query execution
PROFILE MATCH (p:Person)-[:FRIEND]->(f:Person)
WHERE p.age > 25
RETURN p.name, f.name

// Use hints to force specific index usage
MATCH (p:Person)
USING INDEX p:Person(email)
WHERE p.email = 'alice@example.com'
RETURN p
```

### Memory and Cache

```properties
# neo4j.conf performance settings
dbms.memory.heap.initial_size=4G
dbms.memory.heap.max_size=4G
dbms.memory.pagecache.size=8G

# Transaction memory allocation
dbms.memory.transaction.total.max=4G

# Query memory limits
dbms.query.memory.limit=2G
```

### Connection Pool Tuning

```properties
# Bolt connector pool
server.bolt.session_pools.default maxSize=400
server.bolt.session_pools.default connection_timeout=30s

# HTTP connector
server.http.enabled=true
server.http.listen_address=0.0.0.0:7474
```

## Monitoring and Metrics

### Built-in Monitoring

```cypher
// Active queries
CALL dbms.listQueries()

// Kill long-running queries
CALL dbms.killQuery($queryId)

// Transaction metrics
CALL dbms.listTransactions()

// JVM metrics
CALL dbms.jvm.metrics()
```

### Prometheus Integration

```properties
# Enable Prometheus metrics endpoint
metrics.enabled=true
metrics.prometheus.enabled=true
metrics.prometheus.endpoint=localhost:2004
```

## Security Configuration

```properties
# Authentication
dbms.security.auth_enabled=true

# Role-based access control
dbms.security.auth_providers=native

# SSL/TLS
dbms.ssl.policy.bolt.enabled=true
dbms.ssl.policy.bolt.private_key=/certs/neo4j.key
dbms.ssl.policy.bolt.certificate=/certs/neo4j.crt

# IP whitelisting
dbms.connector.bolt.listen_address=0.0.0.0:7687
```

## Common Anti-patterns

1. **Cartesian products**: Accidentally matching disconnected patterns returns all combinations. Use `WHERE` clauses or connect patterns.
2. **Missing labels**: Queries without labels scan all nodes. Always label your patterns.
3. **Over-indexing**: Too many indexes slow down writes. Index only frequently-queried properties.
4. **Unbounded variable-length paths**: `MATCH (a)-[*]->(b)` can traverse the entire graph. Always set limits.
5. **Returning full paths**: Return only needed properties, not entire path objects, to reduce memory.

## Integration with Application Code

```python
from neo4j import GraphDatabase

# Connection pooling and driver configuration
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password"),
    max_connection_pool_size=50,
    connection_acquisition_timeout=60,
    max_transaction_retry_time=30,
)

# Parameterized queries prevent injection
with driver.session(database="production") as session:
    result = session.run(
        "MATCH (p:Person {email: $email}) RETURN p",
        email=user_email
    )
    record = result.single()
```

## Version Migration Checklist

1. Back up current database
2. Run consistency check on current version
3. Test application against new version in staging
4. Check deprecated Cypher syntax
5. Update drivers to match server version
6. Rollback plan: restore backup if migration fails
