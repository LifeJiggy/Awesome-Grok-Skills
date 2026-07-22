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

## Advanced Configuration

### Neo4j Cluster Configuration

```yaml
neo4j_cluster:
  discovery:
    type: "native"
    seed_members: ["neo4j-core-1:5000", "neo4j-core-2:5000", "neo4j-core-3:5000"]
    
  core_nodes:
    - name: "neo4j-core-1"
      host: "10.0.1.10"
      port: 5000
      raft_port: 6000
      role: "core"
      
    - name: "neo4j-core-2"
      host: "10.0.1.11"
      port: 5000
      raft_port: 6000
      role: "core"
      
    - name: "neo4j-core-3"
      host: "10.0.1.12"
      port: 5000
      raft_port: 6000
      role: "core"
      
  read_replicas:
    - name: "neo4j-replica-1"
      host: "10.0.1.20"
      port: 5000
      role: "read_replica"
      
    - name: "neo4j-replica-2"
      host: "10.0.1.21"
      port: 5000
      role: "read_replica"
      
  causal_clustering:
    minimum_core_cluster_size_at_core: 3
    minimum_core_cluster_size_at_learner: 3
    leader_election_timeout: "7s"
    catch_up_batch_size: 1024
    tx_commit_timeout: "1s"
    
  backup:
    enabled: true
    path: "/backups/neo4j/"
    frequency: "daily"
    retention_days: 30
    
  monitoring:
    metrics_enabled: true
    metrics_prefix: "neo4j.cluster"
    health_check_interval: "10s"
```

### Index Strategy Configuration

```yaml
neo4j_indexes:
  composite_indexes:
    - name: "person_name_email"
      label: "Person"
      properties: ["name", "email"]
      type: "range"
      
    - name: "company_industry_country"
      label: "Company"
      properties: ["industry", "country"]
      type: "range"
      
  fulltext_indexes:
    - name: "person_fulltext"
      label: "Person"
      properties: ["name", "bio"]
      type: "fulltext"
      analyzer: "english"
      
    - name: "company_fulltext"
      label: "Company"
      properties: ["name", "description"]
      type: "fulltext"
      analyzer: "english"
      
  text_indexes:
    - name: "product_name"
      label: "Product"
      properties: ["name"]
      type: "text"
      
  point_indexes:
    - name: "location_point"
      label: "Location"
      properties: ["coordinates"]
      type: "point"
      
  range_indexes:
    - name: "event_timestamp"
      label: "Event"
      properties: ["timestamp"]
      type: "range"
      
  unique_constraints:
    - name: "person_email_unique"
      label: "Person"
      property: "email"
      
    - name: "company_domain_unique"
      label: "Company"
      property: "domain"
```

### Performance Tuning Configuration

```yaml
neo4j_performance:
  memory:
    page_cache: "4G"
    heap_initial: "2G"
    heap_max: "4G"
    query_memory_limit: "2G"
    
  execution:
    parallel_recommendation: true
    enable_adaptive_query_planner: true
    enable_cost_based_planner: true
    
  transaction:
    timeout: "60s"
    dead_lock_timeout: "5s"
    max_concurrent_transactions: 100
    
  query:
    log_queries_above_ms: 1000
    enable_query_log: true
    slow_query_threshold: "1s"
    
  storage:
    dbms_storage_total_space: "100G"
    dbms_storage_logs_directory: "/var/log/neo4j"
    dbms_storage_data_directory: "/var/lib/neo4j/data"
    
  network:
    bolt_connector_port: 7687
    http_connector_port: 7474
    https_connector_port: 7473
    listen_address: "0.0.0.0"
```

## Architecture Patterns

### Neo4j High Availability Architecture

```python
class Neo4jHAArchitecture:
    def __init__(self, cluster_config):
        self.config = cluster_config
        self.core_members = cluster_config.core_nodes
        self.replicas = cluster_config.read_replicas
    
    async def get_read_connection(self) -> Neo4jDriver:
        """Get connection to read replica for read operations"""
        replica = self.select_replica()
        return self.create_driver(replica)
    
    async def get_write_connection(self) -> Neo4jDriver:
        """Get connection to core node for write operations"""
        core = self.select_core()
        return self.create_driver(core)
    
    async def execute_with_retry(self, func, max_retries=3):
        """Execute function with automatic retry on failure"""
        for attempt in range(max_retries):
            try:
                return await func()
            except ServiceUnavailableError:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)
```

### Graph Data Migration Pipeline

```python
class GraphDataMigration:
    def __init__(self, source_driver, target_driver, schema_mapper):
        self.source = source_driver
        self.target = target_driver
        self.mapper = schema_mapper
    
    async def migrate_data(self, batch_size=1000):
        """Migrate data from source to target with schema transformation"""
        
        # Extract nodes
        nodes = await self.extract_nodes()
        migrated_nodes = await self.transform_nodes(nodes)
        await self.load_nodes(migrated_nodes, batch_size)
        
        # Extract relationships
        relationships = await self.extract_relationships()
        migrated_rels = await self.transform_relationships(relationships)
        await self.load_relationships(migrated_rels, batch_size)
        
        # Verify migration
        await self.verify_migration()
    
    async def extract_nodes(self):
        """Extract all nodes from source"""
        query = "MATCH (n) RETURN n, labels(n) as labels, id(n) as source_id"
        return await self.source.run_query(query)
    
    async def transform_nodes(self, nodes):
        """Transform node schema for target"""
        transformed = []
        for node in nodes:
            new_node = self.mapper.map_node(node)
            transformed.append(new_node)
        return transformed
```

### Neo4j Monitoring Architecture

```python
class Neo4jMonitoring:
    def __init__(self, metrics_collector, alert_manager):
        self.metrics = metrics_collector
        self.alerts = alert_manager
    
    async def collect_metrics(self):
        """Collect Neo4j metrics"""
        
        # Query metrics
        query_count = await self.get_query_count()
        avg_query_time = await self.get_avg_query_time()
        
        # Connection metrics
        active_connections = await self.get_active_connections()
        
        # Memory metrics
        page_cache_hit_ratio = await self.get_page_cache_hit_ratio()
        
        # Store metrics
        self.metrics.record("neo4j.query.count", query_count)
        self.metrics.record("neo4j.query.avg_time", avg_query_time)
        self.metrics.record("neo4j.connections.active", active_connections)
        self.metrics.record("neo4j.page_cache.hit_ratio", page_cache_hit_ratio)
        
        # Check thresholds
        if avg_query_time > 1000:  # 1 second
            await self.alerts.send_alert(
                "slow_queries",
                f"Average query time: {avg_query_time}ms"
            )
```

## Integration Guide

### Neo4j Python Driver Integration

```python
from neo4j import GraphDatabase

class Neo4jIntegration:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    async def run_query(self, query: str, params: Dict = None) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
    
    async def run_transaction(self, tx_func) -> Any:
        with self.driver.session() as session:
            return session.execute_write(tx_func)
    
    async def bulk_import(self, data: List[Dict], batch_size: int = 1000):
        """Bulk import data with batching"""
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            await self.import_batch(batch)
    
    async def import_batch(self, batch: List[Dict]):
        """Import a single batch of data"""
        query = """
        UNWIND $batch AS item
        CREATE (n:Node {id: item.id, name: item.name})
        """
        with self.driver.session() as session:
            session.run(query, batch=batch)
```

### APOC Integration

```python
class APOCIntegration:
    def __init__(self, driver):
        self.driver = driver
    
    async def export_to_json(self, query: str, file_path: str):
        """Export query results to JSON using APOC"""
        export_query = f"""
        CALL apoc.export.json.query(null, '{query}', {{file: '{file_path}'}})
        YIELD nodes, relationships, time
        RETURN nodes, relationships, time
        """
        return await self.run_query(export_query)
    
    async def import_from_json(self, file_path: str):
        """Import data from JSON using APOC"""
        import_query = f"""
        CALL apoc.load.json('{file_path}') YIELD value
        CREATE (n:ImportedNode {{data: value}})
        """
        return await self.run_query(import_query)
    
    async def create_uuid_index(self, label: str, property: str):
        """Create UUID index using APOC"""
        query = f"""
        CALL apoc.index.addNode('{label}', '{property}')
        """
        return await self.run_query(query)
```

### Neo4j Streams Integration

```python
class Neo4jStreamsIntegration:
    def __init__(self, kafka_config):
        self.kafka_config = kafka_config
    
    async def publish_event(self, topic: str, event: Dict):
        """Publish event to Neo4j Streams"""
        publish_query = """
        CALL streams.publish($topic, $event)
        """
        return await self.run_query(publish_query, {"topic": topic, "event": event})
    
    async def subscribe_to_events(self, topic: str, handler):
        """Subscribe to events from Neo4j Streams"""
        subscribe_query = f"""
        CALL streams.consume('{topic}', handlerFunction)
        """
        return await self.run_query(subscribe_query)
```

## Performance Optimization

### Query Optimization Techniques

```python
class QueryOptimizer:
    def __init__(self, statistics_collector):
        self.stats = statistics_collector
    
    async def optimize_query(self, query: str) -> OptimizedQuery:
        # Analyze query
        analysis = await self.analyze_query(query)
        
        # Apply optimizations
        optimized = query
        
        # 1. Add USING INDEX hint if appropriate
        if analysis.needs_index_hint:
            optimized = self.add_index_hint(optimized, analysis)
        
        # 2. Rewrite optional matches
        if analysis.has_optional_match:
            optimized = self.rewrite_optional_match(optimized, analysis)
        
        # 3. Add LIMIT if not present
        if not analysis.has_limit:
            optimized = self.add_limit(optimized)
        
        # 4. Optimize WHERE clause order
        optimized = self.optimize_where_clause(optimized, analysis)
        
        return OptimizedQuery(
            original=query,
            optimized=optimized,
            optimizations_applied=analysis.optimizations,
            estimated_improvement=analysis.estimated_improvement,
        )
```

### Caching Strategy

```python
class Neo4jQueryCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_query_result(self, query_hash: str) -> Optional[QueryResult]:
        cache_key = f"neo4j_query:{query_hash}"
        cached = await self.redis.get(cache_key)
        if cached:
            return QueryResult.from_json(cached)
        return None
    
    async def cache_query_result(self, query_hash: str, result: QueryResult):
        cache_key = f"neo4j_query:{query_hash}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            result.to_json()
        )
```

### Batch Processing

```python
class Neo4jBatchProcessor:
    def __init__(self, driver, batch_size: int = 1000):
        self.driver = driver
        self.batch_size = batch_size
    
    async def process_batch(self, items: List, query: str):
        """Process items in batches"""
        batches = [
            items[i:i+self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            result = await self.driver.run_query(query, {"batch": batch})
            results.extend(result)
        
        return results
```

## Security Considerations

### Neo4j Security Configuration

```yaml
neo4j_security:
  authentication:
    enabled: true
    native_provider: true
    ldap_provider: false
    
  authorization:
    enabled: true
    default_user: "neo4j"
    admin_roles: ["admin"]
    
  bolt_connector:
    tls_level: "REQUIRED"
    certificate_path: "/certs/neo4j.crt"
    key_path: "/certs/neo4j.key"
    
  https_connector:
    enabled: true
    certificate_path: "/certs/neo4j.crt"
    key_path: "/certs/neo4j.key"
    
  audit_log:
    enabled: true
    log_path: "/var/log/neo4j/audit.log"
    rotation_policy: "size"
    max_file_size: "100M"
    max_files: 10
    
  role_based_access:
    roles:
      - name: "reader"
        permissions:
          - "read"
          
      - name: "writer"
        permissions:
          - "read"
          - "write"
          
      - name: "admin"
        permissions:
          - "read"
          - "write"
          - "admin"
```

### Data Encryption

```python
from cryptography.fernet import Fernet

class Neo4jDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive Neo4j data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive Neo4j data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class Neo4jAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            role_permissions = self.permissions.get(role, [])
            if action in role_permissions:
                return True
        return False
    
    def grant_role(self, user_id: str, role: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        self.roles[user_id].append(role)
```

## Troubleshooting Guide

### Common Issues

**Issue: Cluster connectivity problems**
```python
async def diagnose_cluster_connectivity():
    # Check cluster status
    status = await get_cluster_status()
    
    print(f"Cluster Status:")
    print(f"  Core members: {len(status.core_members)}")
    print(f"  Read replicas: {len(status.read_replicas)}")
    
    for member in status.core_members:
        print(f"\n  {member.name}:")
        print(f"    Role: {member.role}")
        print(f"    Status: {member.status}")
        print(f"    Leader: {member.is_leader}")
        
        if member.status != "online":
            print(f"    WARNING: Member offline")
            print(f"    Recommendation: Check network connectivity")
```

**Issue: Query performance degradation**
```python
async def diagnose_query_performance(query: str):
    # Get query execution plan
    plan = await get_query_plan(query)
    
    print(f"Query Plan:")
    print(f"  Estimated rows: {plan.estimated_rows}")
    print(f"  Estimated cost: {plan.estimated_cost}")
    
    # Check for table scans
    if plan.has_full_scan:
        print(f"  WARNING: Full scan detected")
        print(f"  Recommendation: Add appropriate index")
    
    # Check for cartesian products
    if plan.has_cartesian_product:
        print(f"  WARNING: Cartesian product detected")
        print(f"  Recommendation: Add WHERE clause")
```

**Issue: Memory exhaustion**
```python
async def diagnose_memory_exhaustion():
    # Check memory usage
    memory = await get_memory_usage()
    
    print(f"Memory Usage:")
    print(f"  Page cache: {memory.page_cache_used_mb:.1f} / {memory.page_cache_total_mb:.1f} MB")
    print(f"  Heap: {memory.heap_used_mb:.1f} / {memory.heap_max_mb:.1f} MB")
    
    if memory.page_cache_hit_ratio < 0.9:
        print(f"\n  WARNING: Low page cache hit ratio")
        print(f"  Recommendation: Increase page cache size")
    
    if memory.heap_used_mb > memory.heap_max_mb * 0.8:
        print(f"\n  WARNING: High heap usage")
        print(f"  Recommendation: Increase heap size or optimize queries")
```

## API Reference

### Neo4j Query API

```python
# Execute Cypher query
POST /api/v1/query
Request:
{
    "query": "MATCH (p:Person)-[:KNOWS]->(f:Person) WHERE p.name = $name RETURN f",
    "params": {"name": "Alice"},
    "database": "production"
}

Response:
{
    "records": [
        {"f": {"name": "Bob", "age": 30}},
        {"f": {"name": "Charlie", "age": 25}}
    ],
    "summary": {
        "nodes_created": 0,
        "relationships_created": 0,
        "execution_time_ms": 15
    }
}
```

### Cluster Management API

```python
# Get cluster status
GET /api/v1/cluster/status
Response:
{
    "core_members": [
        {"name": "neo4j-core-1", "status": "online", "role": "leader"},
        {"name": "neo4j-core-2", "status": "online", "role": "follower"},
        {"name": "neo4j-core-3", "status": "online", "role": "follower"}
    ],
    "read_replicas": [
        {"name": "neo4j-replica-1", "status": "online"},
        {"name": "neo4j-replica-2", "status": "online"}
    ]
}
```

### Index Management API

```python
# Create index
POST /api/v1/indexes
Request:
{
    "label": "Person",
    "properties": ["name", "email"],
    "type": "composite"
}

Response:
{
    "index_id": "IDX-001",
    "label": "Person",
    "properties": ["name", "email"],
    "status": "created"
}

# Get indexes
GET /api/v1/indexes
Response:
{
    "indexes": [
        {"id": "IDX-001", "label": "Person", "properties": ["name", "email"]},
        {"id": "IDX-002", "label": "Company", "properties": ["domain"]}
    ]
}
```

## Data Models

### Neo4j Node Model

```python
class Neo4jNode:
    id: int
    labels: List[str]
    properties: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

### Neo4j Relationship Model

```python
class Neo4jRelationship:
    id: int
    type: str
    start_node_id: int
    end_node_id: int
    properties: Dict[str, Any]
    created_at: datetime
```

### Neo4j Index Model

```python
class Neo4jIndex:
    id: str
    label: str
    properties: List[str]
    type: str  # range, fulltext, composite, etc.
    status: str  # created, online, offline
    created_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: neo4j
  namespace: graph-databases-production
spec:
  serviceName: neo4j
  replicas: 3
  selector:
    matchLabels:
      app: neo4j
  template:
    metadata:
      labels:
        app: neo4j
    spec:
      containers:
      - name: neo4j
        image: neo4j:5.12.0-enterprise
        ports:
        - containerPort: 7474
          name: http
        - containerPort: 7687
          name: bolt
        - containerPort: 5000
          name: discovery
        - containerPort: 6000
          name: raft
        - containerPort: 7000
          name: transaction
        env:
        - name: NEO4J_AUTH
          value: "neo4j/password"
        - name: NEO4J_ACCEPT_LICENSE_AGREEMENT
          value: "yes"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        volumeMounts:
        - name: data
          mountPath: /data
        - name: logs
          mountPath: /logs
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

### Database Migration

```bash
# Backup database
neo4j-admin database backup neo4j --to-path=/backups/

# Restore database
neo4j-admin database restore neo4j --from-path=/backups/

# Upgrade database
neo4j-admin database migrate neo4j
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Query metrics
neo4j_queries_counter = Counter(
    'neo4j_queries_total',
    'Total Neo4j queries',
    ['database', 'query_type', 'status']
)

neo4j_query_duration = Histogram(
    'neo4j_query_duration_seconds',
    'Neo4j query duration',
    ['database', 'query_type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

# Cluster metrics
neo4j_cluster_members_gauge = Gauge(
    'neo4j_cluster_members',
    'Number of cluster members',
    ['role']
)

neo4j_cluster_leader_gauge = Gauge(
    'neo4j_cluster_leader',
    'Current cluster leader',
    ['member']
)

# Memory metrics
neo4j_page_cache_hit_ratio = Gauge(
    'neo4j_page_cache_hit_ratio',
    'Page cache hit ratio'
)

neo4j_heap_usage = Gauge(
    'neo4j_heap_usage_bytes',
    'Heap memory usage'
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Neo4j Management",
    "panels": [
      {
        "title": "Query Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(neo4j_queries_total[5m])",
            "legendFormat": "{{database}} - {{query_type}}"
          }
        ]
      },
      {
        "title": "Cluster Status",
        "type": "stat",
        "targets": [
          {
            "expr": "neo4j_cluster_members",
            "legendFormat": "{{role}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: neo4j_alerts
  rules:
  - alert: Neo4jClusterMemberDown
    expr: neo4j_cluster_members < 3
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Neo4j cluster member down"
      
  - alert: Neo4jHighQueryLatency
    expr: histogram_quantile(0.95, rate(neo4j_query_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Neo4j query latency exceeds 1 second"
      
  - alert: Neo4jLowPageCacheHitRatio
    expr: neo4j_page_cache_hit_ratio < 0.9
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Neo4j page cache hit ratio below 90%"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestNeo4jOperations:
    def test_create_node(self, neo4j_driver):
        result = neo4j_driver.run_query(
            "CREATE (p:Person {name: $name, age: $age}) RETURN p",
            {"name": "Alice", "age": 30}
        )
        
        assert len(result) == 1
        assert result[0]["p"]["name"] == "Alice"
    
    def test_create_relationship(self, neo4j_driver):
        result = neo4j_driver.run_query("""
            CREATE (a:Person {name: 'Alice'})
            CREATE (b:Person {name: 'Bob'})
            CREATE (a)-[:KNOWS]->(b)
            RETURN a, b
        """)
        
        assert len(result) == 1
```

### Integration Tests

```python
class TestEndToEndNeo4j:
    async def test_query_flow(self, neo4j_system):
        # Create test data
        await neo4j_system.create_test_data()
        
        # Execute query
        result = await neo4j_system.execute_query(
            "MATCH (p:Person) RETURN count(p) as count"
        )
        
        assert result[0]["count"] > 0
        
        # Cleanup
        await neo4j_system.cleanup_test_data()
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class Neo4jUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def execute_query(self):
        self.client.post("/api/v1/query", json={
            "query": "MATCH (p:Person) RETURN p LIMIT 10",
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/query", methods=["POST"])
@app.route("/api/v2/query", methods=["POST"])
async def execute_query():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await execute_query_v2()
    return await execute_query_v1()
```

### Database Migration Strategy

```bash
# Backup before migration
neo4j-admin database backup neo4j --to-path=/backups/pre-migration/

# Run migration
neo4j-admin database migrate neo4j

# Verify migration
neo4j-admin database check neo4j
```

## Glossary

- **Cypher**: Neo4j's declarative graph query language
- **Bolt**: Neo4j's binary protocol for client-server communication
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **Cluster**: Group of Neo4j instances working together
- **Core Node**: Node that participates in consensus and can accept writes
- **Read Replica**: Node that only accepts read queries
- **Page Cache**: In-memory cache for graph data
- **APOC**: Awesome Procedures On Cypher - Neo4j utility library
- **Index**: Data structure for fast lookup
- **Constraint**: Rule that ensures data integrity

## Changelog

### Version 2.0.0 (2026-07-01)
- Added cluster management
- Implemented index optimization
- Enhanced monitoring
- Added APOC integration

### Version 1.5.0 (2026-01-15)
- Added backup/restore
- Implemented query optimization
- Enhanced security

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic Cypher support
- Simple query execution

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def execute_query(
    query: str,
    params: Dict = None,
    database: str = "neo4j",
) -> QueryResult:
    """Execute a Neo4j query.
    
    Args:
        query: Cypher query string.
        params: Query parameters.
        database: Target database.
    
    Returns:
        Query result.
    
    Raises:
        QueryError: If query execution fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Neo4j Management Platform

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
