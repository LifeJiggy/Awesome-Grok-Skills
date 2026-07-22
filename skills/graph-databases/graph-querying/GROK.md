---
name: graph-querying
category: graph-databases
version: 1.0.0
tags:
  - cypher
  - gremlin
  - sparql
  - graph-query
  - pattern-matching
  - traversal
difficulty: intermediate
estimated_time: 50 minutes
prerequisites:
  - graph-theory-basics
  - relational-databases
  - python-3.10+
---

# Graph Query Languages

Cross-platform guide to querying graph databases: Cypher for Neo4j, Gremlin for Apache TinkerPop, and SPARQL for RDF stores. Covers pattern matching, traversal strategies, shortest path algorithms, and language translation patterns.

## Cypher (Neo4j)

Cypher uses ASCII-art syntax for declarative graph pattern matching. It reads naturally as visual representations of graph patterns.

### Pattern Matching Syntax

```cypher
// Node with label and properties
MATCH (p:Person {name: 'Alice'})

// Relationship traversal
MATCH (p:Person)-[:KNOWS]->(friend:Person)

// Variable-length paths
MATCH (p:Person)-[:KNOWS*1..5]->(connected:Person)

// Multiple relationship types
MATCH (p:Person)-[:KNOWS|WORKS_WITH]->(colleague:Person)

// Typed properties
MATCH (e:Event) WHERE e.date > date('2024-01-01')
RETURN e ORDER BY e.date
```

### Shortest Path

```cypher
// Single shortest path
MATCH path = shortestPath(
  (a:Person {name: 'Alice'})-[*]-(b:Person {name: 'Bob'})
)
RETURN path, length(path) AS hops

// All shortest paths
MATCH path = allShortestPaths(
  (a:Person)-[:FRIEND]->(b:Person)
)
RETURN a.name, b.name, length(path)

// Dijkstra-style weighted shortest path
MATCH path = shortestPath(
  (a:City)-[:FLIGHT*]->(b:City)
)
WHERE ALL(r IN relationships(path) WHERE r.cost IS NOT NULL)
RETURN path, reduce(total = 0, r IN relationships(path) | total + r.cost) AS totalCost
```

### Aggregation Patterns

```cypher
// Degree centrality
MATCH (p:Person)
RETURN p.name, size([(p)-[:FRIEND]->() | 1]) AS outDegree,
       size([()-->(p) | 1]) AS inDegree
ORDER BY outDegree DESC

// Connected component detection
MATCH (p:Person)
WITH p, p.name AS name
OPTIONAL MATCH (p)-[:FRIEND*1..]-(connected:Person)
RETURN name, count(DISTINCT connected) AS componentSize

// Graph density
MATCH (a:Person), (b:Person) WHERE a <> b
OPTIONAL MATCH (a)-[r:FRIEND]->(b)
RETURN toFloat(count(r)) / (count(a) * count(b - 1)) AS density
```

### writes and Graph Construction

```cypher
// Create subgraph from query results
MATCH (p:Person)-[r:FRIEND]->(q:Person)
WHERE p.age > 30 AND q.age > 30
CREATE (p)-[:PEER]->(q)

// Merge with properties (upsert)
MERGE (n:Person {email: $email})
ON CREATE SET n.created = datetime()
ON MATCH SET n.lastSeen = datetime()

// Graph projection for analytics
CALL gds.graph.project(
  'social-graph',
  'Person',
  'FRIEND',
  { properties: ['age', 'score'] }
)
```

## Gremlin (Apache TinkerPop)

Gremlin is an imperative, step-based traversal language. Each step transforms the current traversal state, producing a pipeline of operations.

### Basic Traversals

```groovy
// Find all persons
g.V().hasLabel('Person')

// Filter by property
g.V().hasLabel('Person').has('age', gt(25))

// Outgoing relationships
g.V().has('name', 'Alice').out('KNOWS').path().by('name')

// Incoming relationships
g.V().has('name', 'Alice').in('KNOWS').path().by('name')

// Both directions
g.V().has('name', 'Alice').both('KNOWS').dedup().path().by('name')
```

### Path Traversal

```groovy
// Variable-length path
g.V().has('name', 'Alice')
  .repeat(out('KNOWS'))
  .until(has('name', 'Bob'))
  .path().by('name')

// Shortest path with loop limit
g.V().has('name', 'Alice')
  .repeat(out('KNOWS').simplePath())
  .until(has('name', 'Bob'))
  .limit(1)
  .path().by('name')

// Find all paths between two vertices
g.V().has('name', 'Alice').as('a')
  .V().has('name', 'Bob').as('b')
  .select('a', 'b')
  .sack(assign).by('name')
  .choose(unfold().select('a').out('KNOWS').count().is(gt(0)))
  .by(out('KNOWS').sack(add))
```

### Aggregation in Gremlin

```groovy
// Degree centrality
g.V().hasLabel('Person').project('name', 'degree')
  .by('name')
  .by(both().count())

// Group by label
g.V().groupCount().by(label)

// Connected components
g.V().connectedComponent()
  .group()
  .by(connectedComponent)
  .by(count())
  .unfold()

// PageRank (with TinkerPop)
g.V().pageRank().with('PageRank.iterations', 20)
  .values('pageRank')
  .order().by(decr)
```

### writes in Gremlin

```groovy
// Add vertex with properties
g.addV('Person')
  .property('name', 'Alice')
  .property('age', 30)
  .as('alice')
  .addV('Person')
  .property('name', 'Bob')
  .property('age', 28)
  .as('bob')
  .addE('FRIEND').from('alice').to('bob')
  .property('since', 2020)

// Update properties
g.V().has('name', 'Alice').property('age', 31)

// Drop subgraph
g.V().hasLabel('Person').has('age', lt(18)).drop()
```

## SPARQL (RDF Stores)

SPARQL is the W3C standard query language for RDF graphs. It queries triples (subject-predicate-object) and supports inference over ontologies.

### Basic Graph Patterns

```sparql
# Find all persons
SELECT ?person WHERE {
  ?person a <http://schema.org/Person> .
}

# Properties and values
SELECT ?name ?email WHERE {
  ?person a <http://schema.org/Person> ;
          <http://schema.org/name> ?name ;
          <http://schema.org/email> ?email .
}

# Filtering
SELECT ?name WHERE {
  ?person <http://schema.org/name> ?name ;
          <http://schema.org/age> ?age .
  FILTER (?age > 25)
}
```

### Property Paths (SPARQL 1.1)

```sparql
# Variable-length path (0 to 5 hops)
SELECT ?person WHERE {
  ?start <http://schema.org/name> "Alice" .
  ?start <http://schema.org/knows>+ ?person .
}

# Shortest path (non-standard but common extension)
SELECT ?path WHERE {
  ?start <http://schema.org/name> "Alice" .
  ?end <http://schema.org/name> "Bob" .
  SERVICE path:shortestPath {
    ?path path:start ?start ; path:end ?end .
  }
}

# Recursive relationship traversal
SELECT ?ancestor WHERE {
  ?person <http://schema.org/name> "Alice" .
  ?person <http://schema.org/ancestor>* ?ancestor .
}
```

### Advanced SPARQL Patterns

```sparql
# OPTIONAL (LEFT JOIN)
SELECT ?name ?email WHERE {
  ?person <http://schema.org/name> ?name .
  OPTIONAL { ?person <http://schema.org/email> ?email }
}

# UNION
SELECT ?type WHERE {
  { ?x a <http://schema.org/Person> } UNION { ?x a <http://schema.org/Organization> }
  BIND(afn:local-name(?x) AS ?type)
}

# Subqueries
SELECT ?name (SELECT COUNT(?friend) WHERE {
  ?person <http://schema.org/name> ?name .
  ?person <http://schema.org/knows> ?friend .
} AS ?friendCount) WHERE {
  ?person <http://schema.org/name> ?name .
}

# CONSTRUCT (create new graph)
CONSTRUCT {
  ?person <http://example.org/socialRank> ?rank .
} WHERE {
  SELECT ?person (COUNT(?friend) AS ?friendCount) WHERE {
    ?person <http://schema.org/knows> ?friend .
  } GROUP BY ?person
  BIND(?friendCount * 10 AS ?rank)
}
```

## Language Translation Patterns

Converting between Cypher, Gremlin, and SPARQL for polyglot graph architectures.

### Cypher to Gremlin

| Cypher | Gremlin |
|--------|---------|
| `MATCH (n:Person) RETURN n` | `g.V().hasLabel('Person')` |
| `MATCH (a)-[:FRIEND]->(b) RETURN a, b` | `g.V().outE('FRIEND').inV().path()` |
| `WHERE n.age > 25` | `.has('age', gt(25))` |
| `ORDER BY n.name LIMIT 10` | `.order().by('name').limit(10)` |
| `RETURN count(n)` | `.count()` |
| `MERGE` | `coalesce` + `addV`/`addE` |

### Cypher to SPARQL

| Cypher | SPARQL |
|--------|--------|
| `MATCH (n:Person) RETURN n` | `SELECT ?n WHERE { ?n a <Person> }` |
| `WHERE n.age > 25` | `FILTER (?age > 25)` |
| `OPTIONAL MATCH` | `OPTIONAL { ... }` |
| `RETURN count(n)` | `SELECT (COUNT(?n) AS ?count)` |
| `CREATE (n:Person {name: $name})` | `INSERT DATA { _:bnode a <Person> ; <name> $name }` |

## Query Optimization Strategies

### Index-Driven Traversal

Starting traversal from indexed nodes rather than scanning all nodes. The starting point of a query determines performance: always anchor on indexed properties.

### Bidirectional Traversal

For shortest path queries, traverse from both endpoints simultaneously and intersect. Reduces search space from exponential to polynomial.

### Early Filtering

Apply WHERE/FILTER clauses as early as possible in the traversal pipeline to reduce intermediate result sets.

### Result Set Materialization

Use WITH/MATCH chains in Cypher, or `store()`/`select()` in Gremlin, to materialize intermediate results and avoid recomputation.

### Limit and Pagination

Always use LIMIT for exploration queries. For large result sets, use cursor-based pagination rather than OFFSET/SKIP.

## Common Anti-patterns

1. **Unanchored traversal**: Starting from all vertices instead of a specific entry point
2. **Missing RETURN/collect**: Performing traversals without producing output
3. **Over-fetching properties**: Requesting all properties when only a few are needed
4. **Cartesian products**: Matching disconnected patterns accidentally
5. **Recursive without limit**: Unbounded variable-length paths consuming all memory

## Integration Example

```python
# Cross-language query builder
class GraphQueryBuilder:
    def __init__(self, dialect: str = "cypher"):
        self._dialect = dialect

    def match_node(self, label: str, prop: str, value: str) -> str:
        if self._dialect == "cypher":
            return f"MATCH (n:{label} {{{prop}: '{value}'}})"
        if self._dialect == "gremlin":
            return f"g.V().has('{label}', '{prop}', '{value}')"
        if self._dialect == "sparql":
            return f"?s a <{label}> ; <{prop}> \"{value}\""
        raise ValueError(f"Unknown dialect: {self._dialect}")
```

## Advanced Configuration

### Neo4j Configuration

```yaml
neo4j:
  connection:
    uri: "bolt://localhost:7687"
    username: "neo4j"
    password: "${NEO4J_PASSWORD}"
    encrypted: true
    trust_strategy: "TRUST_SIGNED_CERTIFICATES"
    
  pool:
    max_connection_pool_size: 100
    connection_acquisition_timeout_seconds: 60
    max_transaction_retry_time_seconds: 30
    
  clustering:
    enabled: true
    cluster_name: "neo4j-cluster"
    core_nodes: 3
    read_replicas: 2
    
  performance:
    page_cache_size: "2G"
    heap_size: "4G"
    query_memory_limit: "2G"
    
  monitoring:
    metrics_enabled: true
    metrics_prefix: "neo4j"
    slow_query_threshold_ms: 1000
```

### JanusGraph Configuration

```yaml
janusgraph:
  storage:
    backend: "cql"
    hostname: "localhost:9042"
    keyspace: "janusgraph"
    
  index:
    search:
      backend: "elasticsearch"
      hostname: "localhost:9200"
      index_name: "janusgraph"
      
  cache:
    db-cache: true
    db-cache-size: 10000
    db-cache-time: 10000
    
  tx:
    transaction-recovery: true
    storage-transactional: true
    
  query:
    force-index: false
    batch: true
    fast-property: true
```

### Neptune Configuration

```yaml
neptune:
  endpoint: "your-neptune-cluster.us-east-1.neptune.amazonaws.com"
  port: 8182
  region: "us-east-1"
  
  iam_auth:
    enabled: true
    role_arn: "arn:aws:iam::role/neptune-role"
    
  gremlin:
    traversal_source: "g"
    serializer: "graphbinary"
    
  sparql:
    endpoint: "https://your-neptune-cluster.us-east-1.neptune.amazonaws.com:8182/sparql"
    
  performance:
    enable_partitioned_gremlin_queries: true
    enable_neptune_ml: false
```

## Architecture Patterns

### Graph Query Execution Pipeline

```python
class GraphQueryPipeline:
    def __init__(self, query_parser, optimizer, executor):
        self.parser = query_parser
        self.optimizer = optimizer
        self.executor = executor
    
    async def execute(self, query: str, params: Dict = None) -> QueryResult:
        # Parse query
        parsed = self.parser.parse(query)
        
        # Optimize query plan
        optimized = self.optimizer.optimize(parsed)
        
        # Execute query
        result = await self.executor.execute(optimized, params)
        
        return QueryResult(
            query=query,
            records=result.records,
            summary=result.summary,
            execution_time_ms=result.execution_time_ms,
        )
```

### Pattern Matching Engine

```python
class PatternMatchingEngine:
    def __init__(self, graph_store, index_manager):
        self.graph = graph_store
        self.indexes = index_manager
    
    async def find_patterns(
        self,
        patterns: List[GraphPattern],
        constraints: Dict = None,
    ) -> List[PatternMatch]:
        matches = []
        
        for pattern in patterns:
            # Use index for initial filtering
            candidates = await self.indexes.find_candidates(pattern)
            
            # Apply full pattern matching
            for candidate in candidates:
                if await self.verify_pattern(candidate, pattern, constraints):
                    match = PatternMatch(
                        pattern=pattern,
                        bindings=candidate.bindings,
                        score=self.calculate_score(candidate),
                    )
                    matches.append(match)
        
        return matches
```

### Graph Traversal Optimizer

```python
class GraphTraversalOptimizer:
    def __init__(self, cost_model, statistics):
        self.cost_model = cost_model
        self.stats = statistics
    
    async def optimize_traversal(
        self,
        traversal: GraphTraversal,
    ) -> OptimizedTraversal:
        # Estimate costs for different strategies
        strategies = [
            self.optimize_depth_first(traversal),
            self.optimize_breadth_first(traversal),
            self.optimize_index_first(traversal),
            self.optimize_hybrid(traversal),
        ]
        
        # Select best strategy
        best = min(strategies, key=lambda s: s.estimated_cost)
        
        return OptimizedTraversal(
            original=traversal,
            optimized_plan=best.plan,
            estimated_cost=best.estimated_cost,
            estimated_rows=best.estimated_rows,
        )
```

### Result Materialization Engine

```python
class ResultMaterializationEngine:
    def __init__(self, graph_store, cache_manager):
        self.graph = graph_store
        self.cache = cache_manager
    
    async def materialize(
        self,
        query: QueryResult,
        materialization_config: MaterializationConfig,
    ) -> MaterializedResult:
        # Check cache first
        cache_key = self.generate_cache_key(query)
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        # Materialize results
        if materialization_config.mode == "full":
            result = await self.materialize_full(query)
        elif materialization_config.mode == "lazy":
            result = await self.materialize_lazy(query)
        elif materialization_config.mode == "streaming":
            result = await self.materialize_streaming(query)
        
        # Cache materialized result
        await self.cache.set(cache_key, result, ttl=materialization_config.cache_ttl)
        
        return result
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
```

### JanusGraph Python Integration

```python
from gremlin_python.driver import client as gremlin_client

class JanusGraphIntegration:
    def __init__(self, endpoint: str):
        self.client = gremlin_client.Client(endpoint, 'g')
    
    async def run_query(self, traversal: str) -> List[Dict]:
        result = await self.client.submit_async(traversal)
        return await result.all()
```

### TinkerPop Integration

```python
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.remote_driver import RemoteConnection

class TinkerPopIntegration:
    def __init__(self, endpoint: str):
        self.connection = RemoteConnection(endpoint, 'g')
        self.g = traversal().withRemote(self.connection)
    
    async def query(self, traversal_func):
        return traversal_func(self.g).toList()
```

## Performance Optimization

### Database Optimization

```sql
-- Neo4j index creation
CREATE INDEX FOR (p:Person) ON (p.name);
CREATE INDEX FOR (p:Person) ON (p.email);
CREATE CONSTRAINT FOR (p:Person) REQUIRE p.id IS UNIQUE;

-- JanusGraph index management
mgmt = graph.openManagement()
nameIndex = mgmt.buildIndex('nameIndex', Vertex.class).addKey(name).build()
mgmt.commit()

-- Query optimization hints
MATCH (p:Person)-[:KNOWS]->(f:Person)
WHERE p.name = 'Alice'
USING INDEX p:Person(name)
RETURN f.name
```

### Caching Strategy

```python
class GraphQueryCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_query_result(self, query_hash: str) -> Optional[QueryResult]:
        cache_key = f"graph_query:{query_hash}"
        cached = await self.redis.get(cache_key)
        if cached:
            return QueryResult.from_json(cached)
        return None
    
    async def cache_query_result(self, query_hash: str, result: QueryResult):
        cache_key = f"graph_query:{query_hash}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            result.to_json()
        )
```

### Batch Processing

```python
class GraphQueryBatchProcessor:
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
    
    async def process_batch(self, queries: List[str], executor: GraphExecutor):
        batches = [
            queries[i:i+self.batch_size]
            for i in range(0, len(queries), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                executor.execute(q) for q in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Query Security

```python
class GraphQuerySecurity:
    def __init__(self, query_validator, access_control):
        self.validator = query_validator
        self.access_control = access_control
    
    async def validate_query(self, query: str, user: str) -> bool:
        # Check query syntax
        if not self.validator.validate_syntax(query):
            raise InvalidQueryError("Invalid query syntax")
        
        # Check for dangerous patterns
        if self.validator.has_dangerous_patterns(query):
            raise SecurityError("Query contains dangerous patterns")
        
        # Check access control
        if not await self.access_control.check_access(query, user):
            raise AccessDeniedError("Insufficient permissions")
        
        return True
```

### Data Encryption

```python
from cryptography.fernet import Fernet

class GraphDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive graph data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive graph data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class GraphAccessControl:
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

**Issue: Query timeout**
```python
async def diagnose_query_timeout(query: str):
    # Analyze query plan
    plan = await analyze_query_plan(query)
    
    print(f"Query Analysis:")
    print(f"  Estimated rows: {plan.estimated_rows}")
    print(f"  Estimated cost: {plan.estimated_cost}")
    
    # Check for missing indexes
    if plan.requires_index_scan:
        print(f"  WARNING: Query requires full index scan")
        print(f"  Recommendation: Create appropriate index")
    
    # Check for cartesian products
    if plan.has_cartesian_product:
        print(f"  WARNING: Cartesian product detected")
        print(f"  Recommendation: Add WHERE clause to reduce combinations")
```

**Issue: Memory exhaustion**
```python
async def diagnose_memory_exhaustion(query: str):
    # Check query memory usage
    memory_usage = await estimate_memory_usage(query)
    
    print(f"Memory Analysis:")
    print(f"  Estimated memory: {memory_usage.estimated_mb:.1f} MB")
    print(f"  Available memory: {memory_usage.available_mb:.1f} MB")
    
    if memory_usage.estimated_mb > memory_usage.available_mb:
        print(f"  WARNING: Query may exhaust memory")
        print(f"  Recommendations:")
        print(f"    1. Add LIMIT clause")
        print(f"    2. Use MERGE instead of CREATE")
        print(f"    3. Break query into smaller parts")
```

**Issue: Slow traversal performance**
```python
async def diagnose_slow_traversal(traversal: str):
    # Profile traversal
    profile = await profile_traversal(traversal)
    
    print(f"Traversal Profile:")
    print(f"  Total time: {profile.total_time_ms:.1f} ms")
    print(f"  Rows processed: {profile.rows_processed}")
    print(f"  Steps: {len(profile.steps)}")
    
    for step in profile.steps:
        print(f"    {step.name}: {step.time_ms:.1f} ms ({step.rows} rows)")
        
    # Identify bottlenecks
    slow_steps = [s for s in profile.steps if s.time_ms > 100]
    if slow_steps:
        print(f"\n  Slow steps (>100ms):")
        for step in slow_steps:
            print(f"    {step.name}: {step.time_ms:.1f} ms")
            print(f"    Recommendation: Optimize this step")
```

## API Reference

### Graph Query API

```python
# Execute Cypher query
POST /api/v1/query/cypher
Request:
{
    "query": "MATCH (p:Person)-[:KNOWS]->(f:Person) WHERE p.name = $name RETURN f",
    "params": {"name": "Alice"},
    "database": "neo4j"
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

# Execute Gremlin query
POST /api/v1/query/gremlin
Request:
{
    "query": "g.V().has('Person', 'name', 'Alice').out('KNOWS').valueMap(true)",
    "database": "janusgraph"
}

Response:
{
    "result": [
        {"name": ["Bob"], "age": [30]},
        {"name": ["Charlie"], "age": [25]}
    ],
    "execution_time_ms": 20
}
```

### Graph Schema API

```python
# Get graph schema
GET /api/v1/schema
Response:
{
    "labels": [
        {"name": "Person", "count": 10000},
        {"name": "Movie", "count": 5000}
    ],
    "relationship_types": [
        {"name": "ACTED_IN", "count": 25000},
        {"name": "KNOWS", "count": 50000}
    ],
    "indexes": [
        {"name": "person_name", "type": "range", "labels": ["Person"]}
    ]
}

# Get query statistics
GET /api/v1/stats
Response:
{
    "total_queries": 15000,
    "avg_execution_time_ms": 25,
    "slow_queries": 150,
    "cache_hit_rate": 0.85
}
```

## Data Models

### Query Result Model

```python
class QueryResult:
    query: str
    records: List[Dict]
    summary: QuerySummary
    execution_time_ms: float
    cached: bool = False
    created_at: datetime
```

### Graph Schema Model

```python
class GraphSchema:
    labels: List[NodeLabel]
    relationship_types: List[RelationshipType]
    indexes: List[Index]
    constraints: List[Constraint]
    updated_at: datetime
```

### Traversal Profile Model

```python
class TraversalProfile:
    traversal: str
    total_time_ms: float
    rows_processed: int
    steps: List[TraversalStep]
    memory_usage_mb: float
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graph-querying-service
  namespace: graph-databases-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: graph-querying-service
  template:
    metadata:
      labels:
        app: graph-querying-service
    spec:
      containers:
      - name: graph-querying
        image: your-registry/graph-querying-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "1Gi"
            cpu: "1000m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Query metrics
queries_counter = Counter(
    'graph_queries_total',
    'Total graph queries',
    ['database', 'query_type', 'status']
)

query_duration = Histogram(
    'graph_query_duration_seconds',
    'Graph query duration',
    ['database', 'query_type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

# Graph metrics
graph_nodes_gauge = Gauge(
    'graph_nodes_total',
    'Total graph nodes',
    ['label']
)

graph_relationships_gauge = Gauge(
    'graph_relationships_total',
    'Total graph relationships',
    ['type']
)

# Cache metrics
cache_hits_counter = Counter(
    'graph_cache_hits_total',
    'Total cache hits',
    ['database']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Graph Querying",
    "panels": [
      {
        "title": "Query Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(graph_queries_total[5m])",
            "legendFormat": "{{database}} - {{query_type}}"
          }
        ]
      },
      {
        "title": "Query Latency",
        "type": "heatmap",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(graph_query_duration_seconds_bucket[5m]))",
            "legendFormat": "P95"
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
- name: graph_alerts
  rules:
  - alert: HighQueryLatency
    expr: histogram_quantile(0.95, rate(graph_query_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Graph query latency exceeds 1 second"
      
  - alert: QueryErrors
    expr: rate(graph_queries_total{status="error"}[5m]) > 0.01
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High graph query error rate"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestGraphQuerying:
    def test_cypher_query(self, graph_executor):
        result = graph_executor.execute(
            query="MATCH (p:Person) WHERE p.name = $name RETURN p",
            params={"name": "Alice"},
        )
        
        assert result.records is not None
        assert len(result.records) >= 0
    
    def test_gremlin_query(self, graph_executor):
        result = graph_executor.execute(
            query="g.V().has('Person', 'name', 'Alice')",
        )
        
        assert result.records is not None
```

### Integration Tests

```python
class TestEndToEndGraphQuerying:
    async def test_query_flow(self, graph_system):
        # Execute query
        result = await graph_system.execute_query(
            database="neo4j",
            query="MATCH (p:Person) RETURN count(p) as count",
        )
        
        assert result.summary.execution_time_ms > 0
        assert len(result.records) > 0
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class GraphQueryUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def execute_cypher(self):
        self.client.post("/api/v1/query/cypher", json={
            "query": "MATCH (p:Person) RETURN p LIMIT 10",
        })
    
    @task(5)
    def execute_gremlin(self):
        self.client.post("/api/v1/query/gremlin", json={
            "query": "g.V().limit(10)",
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/query/cypher", methods=["POST"])
@app.route("/api/v2/query/cypher", methods=["POST"])
async def execute_cypher():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await execute_cypher_v2()
    return await execute_cypher_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **Cypher**: Graph query language for Neo4j
- **Gremlin**: Graph traversal language for Apache TinkerPop
- **SPARQL**: Query language for RDF data
- **Pattern Matching**: Finding subgraphs that match a specified pattern
- **Traversal**: Walking through graph structure following relationships
- **Index**: Data structure for fast node/relationship lookup
- **Cartesian Product**: Result of combining all rows from two sets
- **Execution Plan**: Step-by-step strategy for executing a query
- **Materialization**: Converting lazy evaluation to concrete results
- **Query Optimization**: Improving query performance through rewriting

## Changelog

### Version 2.0.0 (2026-07-01)
- Added SPARQL support
- Implemented query optimization
- Enhanced caching strategy
- Added batch processing

### Version 1.5.0 (2026-01-15)
- Added Gremlin support
- Implemented pattern matching
- Enhanced security controls

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
    """Execute a graph query.
    
    Args:
        query: Query string.
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

Copyright (c) 2026 Graph Querying Platform

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
