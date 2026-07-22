---
name: graph-algorithms
category: graph-databases
version: 1.0.0
tags:
  - pagerank
  - louvain
  - shortest-path
  - centrality
  - graph-coloring
  - algorithms
difficulty: advanced
estimated_time: 50 minutes
prerequisites:
  - graph-theory-basics
  - linear-algebra
  - python-3.10+
---

# Graph Algorithms

Practical implementations of fundamental graph algorithms: PageRank, community detection, shortest path, centrality measures, graph coloring, and traversal strategies. Covers both theory and production-ready implementations.

## PageRank

Google's algorithm for ranking web pages by importance. Iteratively distributes rank from each page to its outgoing links. Converges to a stationary distribution of a random walk.

### Algorithm

```
PR(v) = (1 - d) / N + d * sum(PR(u) / outDegree(u)) for all u -> v
where d = damping factor (typically 0.85), N = number of nodes
```

### Convergence

PageRank converges when the L1 norm of the difference between successive iterations falls below a threshold (typically 1e-6). For most graphs, 50-100 iterations suffice.

### Damping Factor

The damping factor d represents the probability a random surfer follows a link rather than teleporting to a random page. d=0.85 is standard; higher values emphasize link structure, lower values make rankings more uniform.

### Variations

- **Personalized PageRank (PPR)**: Teleport set biased toward specific nodes
- **Topic-Sensitive PageRank**: Multiple random walkers for different topics
- **BlockRank**: Hierarchical PageRank for large web graphs

## Louvain Community Detection

Greedy modularity optimization. Fast hierarchical algorithm that detects communities by maximizing modularity Q.

### Modularity

```
Q = (1/2m) * sum[A_ij - (k_i * k_j) / (2m)] * delta(c_i, c_j)
where m = number of edges
A_ij = adjacency matrix entry
k_i = degree of node i
delta(c_i, c_j) = 1 if i,j in same community, 0 otherwise
```

### Algorithm Steps

1. **Phase 1**: Each node in its own community. Move nodes to maximize local modularity gain.
2. **Phase 2**: Build new graph where communities are super-nodes. Inter-community edges become weighted self-loops.
3. **Repeat** until no further improvement.

### Modularity Gain

Moving node i from community A to community B:

```
deltaQ = [SIGMA_in + 2*k_i,in] / (2m) - [(SIGMA_tot + k_i)^2 / (2m)^2]
       - [SIGMA_in / (2m) - (SIGMA_tot^2 / (2m)^2) - (k_i^2 / (2m)^2)]
where SIGMA_in = sum of weights inside community
SIGMA_tot = sum of weights incident to community
k_i,in = sum of weights from i to nodes in target community
```

## Shortest Path Algorithms

### Dijkstra's Algorithm

Finds shortest paths from a single source to all other nodes in graphs with non-negative edge weights. O((V + E) log V) with binary heap.

```
1. Initialize distances: dist[source] = 0, dist[v] = inf for all v
2. Add source to priority queue
3. While queue not empty:
   a. Extract minimum distance node u
   b. For each neighbor v of u:
      If dist[u] + weight(u,v) < dist[v]:
        dist[v] = dist[u] + weight(u,v)
        predecessor[v] = u
        decrease-key(v, dist[v])
```

### Bellman-Ford

Handles negative edge weights. O(V*E) complexity. Detects negative cycles.

```
1. Initialize distances: dist[source] = 0, dist[v] = inf
2. Repeat V-1 times:
   For each edge (u,v) with weight w:
     If dist[u] + w < dist[v]:
       dist[v] = dist[u] + w
       predecessor[v] = u
3. Check for negative cycles:
   For each edge (u,v) with weight w:
     If dist[u] + w < dist[v]:
       Graph contains negative cycle
```

### Floyd-Warshall

All-pairs shortest paths. O(V^3) complexity. Works with negative weights (no negative cycles).

```
For k = 1 to V:
  For i = 1 to V:
    For j = 1 to V:
      dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

## Centrality Measures

### Degree Centrality

Number of direct connections. Simplest measure of node importance.

### Betweenness Centrality

Fraction of shortest paths passing through a node. O(VE) on sparse graphs.

```
C_B(v) = sum(sigma_st(v) / sigma_st) for all s!=v!=t
```

### Closeness Centrality

Inverse of average shortest path distance to all other nodes. Measures how quickly a node can reach the network.

```
C_C(v) = (n-1) / sum(d(v,u)) for all u
```

### Eigenvector Centrality

Recursive importance: a node is important if it connects to important nodes.

```
C_E(v) = (1/lambda) * sum(A_vu * C_E(u))
```

### PageRank vs Eigenvector

PageRank adds a damping factor and normalizes by out-degree. Eigenvector centrality can diverge on directed graphs with sinks; PageRank's teleport ensures convergence.

## Graph Coloring

Assign colors to vertices so no two adjacent vertices share the same color. Applications: register allocation, scheduling, frequency assignment.

### Greedy Coloring

Process vertices in order, assign the smallest available color. O(V*Delta) where Delta is max degree. Not optimal but fast.

### Welsh-Powell Algorithm

Sort vertices by degree (descending). Process in order, assigning smallest available color. Often produces near-optimal results.

### Brooks' Theorem

For connected graphs that are neither complete graphs nor odd cycles, chromatic number <= Delta (max degree).

### Exact Algorithms

- **Backtracking**: Try all colorings, prune infeasible branches. Exponential worst-case.
- **DSATUR**: Dynamic ordering based on saturation degree (number of different colors among neighbors).

## BFS and DFS

### Breadth-First Search

Explores layer by layer from source. Finds shortest paths in unweighted graphs. O(V + E).

### Depth-First Search

Explores as far as possible along each branch. Detects cycles, finds connected components, topological sorting. O(V + E).

### Applications

- **Cycle detection**: DFS with coloring (white/gray/black)
- **Topological sort**: DFS post-order on DAGs
- **Connected components**: BFS/DFS from each unvisited node
- **Articulation points**: DFS with low-link values
- **Bridge detection**: DFS edge classification

## Minimum Spanning Tree

### Kruskal's Algorithm

Sort edges by weight. Add edges that don't create cycles (union-find). O(E log E).

### Prim's Algorithm

Start from arbitrary node. Always add the cheapest edge connecting the tree to a non-tree node. O(E log V) with binary heap.

### Applications

- Network design (minimize cable length)
- Clustering (remove edges above threshold weight)
- Approximation algorithms for NP-hard problems

## Production Considerations

### Parallelization

- PageRank: embarrassingly parallel (each node computation independent)
- BFS/DFS: level-synchronous parallelism for BFS
- Betweenness centrality: Brandes' algorithm with partial computation

### Approximation

- Betweenness: Sample shortest paths from subset of sources
- Clustering coefficient: Estimate via random neighbor sampling
- Connected components: Union-find with path compression and union by rank

### Streaming Graphs

- Maintain approximate centrality with sketches
- Community detection via streaming label propagation
- Incremental PageRank for edge insertions

## Algorithm Selection Guide

| Problem | Algorithm | Complexity | Parallel? |
|---------|-----------|------------|-----------|
| Node ranking | PageRank | O(k*E) | Yes |
| Communities | Louvain | O(E) | Limited |
| Shortest path | Dijkstra | O(E log V) | Yes |
| All-pairs shortest | Floyd-Warshall | O(V^3) | Limited |
| Graph coloring | Greedy/DSATUR | O(V*Delta) | Partial |
| Spanning tree | Kruskal | O(E log E) | Yes |
| Cycle detection | DFS | O(V+E) | Yes |
| Articulation points | Tarjan | O(V+E) | Limited |

## Advanced Configuration

### PageRank Configuration

```yaml
pagerank:
  parameters:
    damping_factor: 0.85
    max_iterations: 100
    tolerance: 1e-6
    initial_value: 1.0
    
  optimization:
    parallel_execution: true
    batch_size: 10000
    use_sparse_representation: true
    
  personalization:
    enabled: true
    teleport_set_size: 100
    
  output:
    include_ranking: true
    normalize_scores: true
    top_nodes_count: 100
```

### Community Detection Configuration

```yaml
community_detection:
  louvain:
    resolution: 1.0
    max_levels: 10
    min_modularity_gain: 0.001
    random_seed: 42
    
  leiden:
    resolution: 1.0
    iterations: 10
    max_levels: 10
    
  label_propagation:
    max_iterations: 100
    tolerance: 1e-6
    
  output:
    min_community_size: 5
    max_communities: 1000
    export_community_assignments: true
```

### Shortest Path Configuration

```yaml
shortest_path:
  dijkstra:
    max_distance: 1000000
    heuristic: "euclidean"
    
  bellman_ford:
    max_iterations: 1000
    detect_negative_cycles: true
    
  a_star:
    heuristic: "manhattan"
    
  all_pairs:
    max_pairs: 1000000
    batch_size: 1000
    
  output:
    include_path: true
    include_distance: true
    max_paths: 100
```

### Centrality Configuration

```yaml
centrality:
  betweenness:
    approximation: true
    sample_size: 1000
    normalized: true
    
  closeness:
    normalized: true
    handle_disconnected: true
    
  degree:
    normalized: true
    include_self_loops: false
    
  eigenvector:
    max_iterations: 100
    tolerance: 1e-6
    
  output:
    top_nodes_count: 100
    include_distribution: true
```

### Graph Coloring Configuration

```yaml
graph_coloring:
  greedy:
    order: "largest_first"
    
  dsatur:
    max_iterations: 100
    
  backtracking:
    max_depth: 1000
    timeout_seconds: 60
    
  output:
    min_colors: true
    color_distribution: true
    conflict_detection: true
```

## Architecture Patterns

### Graph Algorithm Execution Engine

```python
class GraphAlgorithmEngine:
    def __init__(self, graph_store, algorithm_registry):
        self.graph = graph_store
        self.algorithms = algorithm_registry
    
    async def execute_algorithm(
        self,
        algorithm_name: str,
        params: Dict = None,
    ) -> AlgorithmResult:
        # Get algorithm implementation
        algorithm = self.algorithms.get(algorithm_name)
        
        # Load graph data
        graph_data = await self.graph.export_data()
        
        # Execute algorithm
        result = await algorithm.execute(graph_data, params)
        
        # Store results
        await self.store_results(algorithm_name, result)
        
        return AlgorithmResult(
            algorithm=algorithm_name,
            parameters=params,
            result=result,
            execution_time_ms=result.execution_time_ms,
        )
```

### Batch Algorithm Processor

```python
class BatchAlgorithmProcessor:
    def __init__(self, algorithm_engine, batch_size=1000):
        self.engine = algorithm_engine
        self.batch_size = batch_size
    
    async def process_batch(
        self,
        nodes: List[str],
        algorithm: str,
        params: Dict = None,
    ) -> List[AlgorithmResult]:
        # Process nodes in batches
        batches = [
            nodes[i:i+self.batch_size]
            for i in range(0, len(nodes), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_result = await self.engine.execute_on_subgraph(
                algorithm=algorithm,
                nodes=batch,
                params=params,
            )
            results.extend(batch_result)
        
        return results
```

### Algorithm Result Aggregator

```python
class AlgorithmResultAggregator:
    def __init__(self, result_store):
        self.store = result_store
    
    async def aggregate_results(
        self,
        results: List[AlgorithmResult],
    ) -> AggregatedResult:
        # Group by algorithm
        by_algorithm = defaultdict(list)
        for result in results:
            by_algorithm[result.algorithm].append(result)
        
        # Aggregate each algorithm's results
        aggregated = {}
        for algorithm, algo_results in by_algorithm.items():
            aggregated[algorithm] = self.aggregate_algorithm(
                algorithm,
                algo_results,
            )
        
        return AggregatedResult(
            algorithms=list(aggregated.keys()),
            results=aggregated,
            total_nodes=sum(r.node_count for r in results),
        )
```

### Incremental Algorithm Updater

```python
class IncrementalAlgorithmUpdater:
    def __init__(self, algorithm_engine, change_detector):
        self.engine = algorithm_engine
        self.detector = change_detector
    
    async def update_incremental(
        self,
        algorithm: str,
        changes: List[GraphChange],
    ) -> UpdateResult:
        # Detect affected nodes
        affected_nodes = self.detector.detect_affected(changes)
        
        # Update algorithm results incrementally
        if algorithm == "pagerank":
            result = await self.update_pagerank_incremental(affected_nodes)
        elif algorithm == "community":
            result = await self.update_community_incremental(affected_nodes)
        else:
            # Full recomputation for non-incremental algorithms
            result = await self.engine.execute_algorithm(algorithm)
        
        return UpdateResult(
            algorithm=algorithm,
            affected_nodes=len(affected_nodes),
            incremental=True,
            result=result,
        )
```

## Integration Guide

### Neo4j GDS Integration

```python
from neo4j import GraphDatabase

class Neo4jGDSIntegration:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    async def run_pagerank(self, params: Dict = None) -> List[Dict]:
        query = """
        CALL gds.pageRank.stream('myGraph')
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).name AS name, score
        ORDER BY score DESC
        """
        return await self.run_query(query)
    
    async def run_louvain(self) -> List[Dict]:
        query = """
        CALL gds.louvain.stream('myGraph')
        YIELD nodeId, communityId
        RETURN gds.util.asNode(nodeId).name AS name, communityId
        """
        return await self.run_query(query)
    
    async def run_shortest_path(self, start: str, end: str) -> List[Dict]:
        query = """
        MATCH (source:Person {name: $start}), (target:Person {name: $end})
        CALL gds.shortestPath.dijkstra.stream('myGraph', {
            sourceNode: source,
            targetNode: target
        })
        YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
        RETURN path
        """
        return await self.run_query(query, {"start": start, "end": end})
```

### NetworkX Integration

```python
import networkx as nx

class NetworkXIntegration:
    def __init__(self):
        self.G = nx.DiGraph()
    
    async def load_graph(self, nodes: List[Dict], edges: List[Dict]):
        # Add nodes
        for node in nodes:
            self.G.add_node(node["id"], **node["properties"])
        
        # Add edges
        for edge in edges:
            self.G.add_edge(edge["source"], edge["target"], **edge["properties"])
    
    async def run_pagerank(self, params: Dict = None) -> Dict:
        return nx.pagerank(self.G, **(params or {}))
    
    async def run_louvain(self) -> Dict:
        undirected = self.G.to_undirected()
        return nx.community.louvain_communities(undirected)
    
    async def run_shortest_path(self, source: str, target: str) -> List:
        return nx.shortest_path(self.G, source, target)
```

### GraphBLAS Integration

```python
class GraphBLASIntegration:
    def __init__(self):
        pass
    
    async def run_pagerank(self, adjacency_matrix, params: Dict = None) -> np.ndarray:
        # Use GraphBLAS for efficient matrix operations
        import grblas as gb
        
        # Convert adjacency matrix to GrB matrix
        A = gb.Matrix.from_numpy(adjacency_matrix)
        
        # Compute PageRank
        d = params.get("damping_factor", 0.85)
        n = A.shape[0]
        
        # Iterative computation
        pr = gb.Vector.from_numpy(np.ones(n) / n)
        for _ in range(params.get("max_iterations", 100)):
            pr_new = (1 - d) / n + d * A.T @ pr
            if gb.isclose(pr_new, pr, atol=params.get("tolerance", 1e-6)):
                break
            pr = pr_new
        
        return pr.to_numpy()
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for algorithm queries
CREATE INDEX idx_nodes_id ON nodes (id);
CREATE INDEX idx_edges_source_target ON edges (source_id, target_id);
CREATE INDEX idx_algorithm_results ON algorithm_results (algorithm, node_id);

-- Create materialized view for common queries
CREATE MATERIALIZED VIEW pagerank_results AS
SELECT node_id, score, rank
FROM algorithm_results
WHERE algorithm = 'pagerank'
ORDER BY score DESC;

-- Partition algorithm results
CREATE TABLE algorithm_results (
    id UUID PRIMARY KEY,
    algorithm VARCHAR(50),
    node_id VARCHAR(100),
    score DECIMAL(10,6),
    computed_at TIMESTAMP
) PARTITION BY RANGE (computed_at);
```

### Caching Strategy

```python
class GraphAlgorithmCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_algorithm_result(
        self,
        algorithm: str,
        params_hash: str,
    ) -> Optional[AlgorithmResult]:
        cache_key = f"algo:{algorithm}:{params_hash}"
        cached = await self.redis.get(cache_key)
        if cached:
            return AlgorithmResult.from_json(cached)
        return None
    
    async def cache_algorithm_result(
        self,
        algorithm: str,
        params_hash: str,
        result: AlgorithmResult,
    ):
        cache_key = f"algo:{algorithm}:{params_hash}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            result.to_json()
        )
```

### Parallel Processing

```python
class ParallelAlgorithmProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_parallel(
        self,
        tasks: List[Callable],
    ) -> List[Any]:
        # Execute tasks in parallel
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(self.executor, task)
            for task in tasks
        ]
        
        results = await asyncio.gather(*futures)
        return results
```

## Security Considerations

### Algorithm Access Control

```python
class AlgorithmAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, algorithm: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            if algorithm in self.permissions.get(role, []):
                return True
        return False
    
    def grant_algorithm_access(self, user_id: str, algorithm: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        if algorithm not in self.permissions:
            self.permissions[algorithm] = []
        self.permissions[algorithm].append(user_id)
```

### Result Data Encryption

```python
from cryptography.fernet import Fernet

class AlgorithmResultEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_result(self, result: str) -> str:
        """Encrypt algorithm result"""
        return self.fernet.encrypt(result.encode()).decode()
    
    def decrypt_result(self, encrypted: str) -> str:
        """Decrypt algorithm result"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Audit Logging

```python
class AlgorithmAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'algorithm': event.algorithm,
            'action': event.action,
            'parameters': event.parameters,
            'result_summary': event.result_summary,
            'execution_time_ms': event.execution_time_ms,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: PageRank not converging**
```python
async def diagnose_pagerank_convergence(pagerank_result: PageRankResult):
    print(f"PageRank Convergence Analysis:")
    print(f"  Iterations: {pagerank_result.iterations}")
    print(f"  Final L1 norm: {pagerank_result.final_l1_norm}")
    print(f"  Converged: {pagerank_result.converged}")
    
    if not pagerank_result.converged:
        print(f"\n  WARNING: PageRank did not converge")
        print(f"  Recommendations:")
        print(f"    1. Increase max_iterations")
        print(f"    2. Check for dangling nodes")
        print(f"    3. Verify damping factor (current: {pagerank_result.damping_factor})")
    
    # Check for disconnected components
    if pagerank_result.disconnected_components > 1:
        print(f"\n  WARNING: {pagerank_result.disconnected_components} disconnected components")
        print(f"  Recommendation: Consider using Personalized PageRank")
```

**Issue: Community detection fragmentation**
```python
async def diagnose_community_fragmentation(community_result: CommunityResult):
    print(f"Community Detection Analysis:")
    print(f"  Communities found: {community_result.num_communities}")
    print(f"  Modularity: {community_result.modularity:.4f}")
    
    # Analyze community sizes
    sizes = [c.size for c in community_result.communities]
    print(f"\n  Community Sizes:")
    print(f"    Min: {min(sizes)}")
    print(f"    Max: {max(sizes)}")
    print(f"    Mean: {sum(sizes)/len(sizes):.1f}")
    print(f"    Median: {sorted(sizes)[len(sizes)//2]}")
    
    # Check for small communities
    small_communities = [c for c in community_result.communities if c.size < 5]
    if small_communities:
        print(f"\n  WARNING: {len(small_communities)} communities with < 5 nodes")
        print(f"  Recommendation: Increase min_community_size parameter")
```

**Issue: Shortest path not found**
```python
async def diagnose_shortest_path(source: str, target: str, graph):
    # Check if nodes exist
    source_exists = await graph.node_exists(source)
    target_exists = await graph.node_exists(target)
    
    print(f"Shortest Path Analysis: {source} → {target}")
    print(f"  Source exists: {source_exists}")
    print(f"  Target exists: {target_exists}")
    
    if not source_exists or not target_exists:
        print(f"\n  ERROR: Node(s) not found")
        return
    
    # Check connectivity
    is_connected = await graph.are_connected(source, target)
    print(f"  Connected: {is_connected}")
    
    if not is_connected:
        print(f"\n  WARNING: No path exists between nodes")
        print(f"  Recommendation: Check edge direction and connectivity")
```

## API Reference

### Graph Algorithm API

```python
# Execute PageRank
POST /api/v1/algorithms/pagerank
Request:
{
    "damping_factor": 0.85,
    "max_iterations": 100,
    "tolerance": 1e-6
}

Response:
{
    "algorithm": "pagerank",
    "iterations": 45,
    "converged": true,
    "results": [
        {"node_id": "node1", "score": 0.15},
        {"node_id": "node2", "score": 0.12}
    ],
    "execution_time_ms": 2500
}

# Execute Community Detection
POST /api/v1/algorithms/community
Request:
{
    "algorithm": "louvain",
    "resolution": 1.0
}

Response:
{
    "algorithm": "louvain",
    "num_communities": 5,
    "modularity": 0.45,
    "results": [
        {"node_id": "node1", "community_id": 1},
        {"node_id": "node2", "community_id": 1}
    ],
    "execution_time_ms": 1500
}

# Execute Shortest Path
POST /api/v1/algorithms/shortest-path
Request:
{
    "source": "node1",
    "target": "node5",
    "algorithm": "dijkstra"
}

Response:
{
    "algorithm": "dijkstra",
    "path": ["node1", "node3", "node5"],
    "distance": 2.5,
    "execution_time_ms": 150
}
```

### Algorithm Management API

```python
# List available algorithms
GET /api/v1/algorithms
Response:
{
    "algorithms": [
        {"name": "pagerank", "type": "centrality", "complexity": "O(k*E)"},
        {"name": "louvain", "type": "community", "complexity": "O(E)"},
        {"name": "dijkstra", "type": "shortest_path", "complexity": "O(E log V)"}
    ]
}

# Get algorithm execution history
GET /api/v1/algorithms/{algorithm}/history
Response:
{
    "algorithm": "pagerank",
    "history": [
        {"timestamp": "2026-07-01T10:00:00Z", "parameters": {...}, "execution_time_ms": 2500}
    ]
}
```

## Data Models

### Algorithm Result Model

```python
class AlgorithmResult:
    result_id: str
    algorithm: str
    parameters: Dict[str, Any]
    node_results: Dict[str, float]
    execution_time_ms: float
    iterations: Optional[int]
    converged: Optional[bool]
    computed_at: datetime
```

### Community Result Model

```python
class CommunityResult:
    result_id: str
    algorithm: str
    num_communities: int
    modularity: float
    communities: List[Community]
    computed_at: datetime
```

### Shortest Path Result Model

```python
class ShortestPathResult:
    result_id: str
    algorithm: str
    source: str
    target: str
    path: List[str]
    distance: float
    computed_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graph-algorithms-service
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
      app: graph-algorithms-service
  template:
    metadata:
      labels:
        app: graph-algorithms-service
    spec:
      containers:
      - name: graph-algorithms
        image: your-registry/graph-algorithms-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "2Gi"
            cpu: "2000m"
          limits:
            memory: "4Gi"
            cpu: "4000m"
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

# Algorithm execution metrics
algorithm_executions_counter = Counter(
    'graph_algorithm_executions_total',
    'Total algorithm executions',
    ['algorithm', 'status']
)

algorithm_execution_duration = Histogram(
    'graph_algorithm_execution_duration_seconds',
    'Algorithm execution duration',
    ['algorithm'],
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 60.0]
)

# Result metrics
algorithm_results_gauge = Gauge(
    'graph_algorithm_results',
    'Algorithm results',
    ['algorithm', 'metric']
)

# Community metrics
community_count_gauge = Gauge(
    'graph_communities_count',
    'Number of communities detected'
)

modularity_gauge = Gauge(
    'graph_modularity',
    'Community detection modularity'
)
```

### Grafana Dashboard

```json
{
    "dashboard": {
        "title": "Graph Algorithms",
        "panels": [
            {
                "title": "Algorithm Execution Rate",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(graph_algorithm_executions_total[5m])",
                        "legendFormat": "{{algorithm}} - {{status}}"
                    }
                ]
            },
            {
                "title": "Execution Duration",
                "type": "heatmap",
                "targets": [
                    {
                        "expr": "histogram_quantile(0.95, rate(graph_algorithm_execution_duration_seconds_bucket[5m]))",
                        "legendFormat": "{{algorithm}}"
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
- name: graph_algorithm_alerts
  rules:
  - alert: AlgorithmExecutionSlow
    expr: histogram_quantile(0.95, rate(graph_algorithm_execution_duration_seconds_bucket[5m])) > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Graph algorithm execution exceeds 10 seconds"
      
  - alert: AlgorithmExecutionFailed
    expr: rate(graph_algorithm_executions_total{status="failed"}[5m]) > 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Graph algorithm execution failed"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestPageRank:
    def test_pagerank_simple(self, algorithm_engine):
        # Create simple graph
        graph = create_simple_graph()
        
        result = algorithm_engine.execute("pagerank", graph)
        
        assert result.converged == True
        assert len(result.node_results) > 0
    
    def test_pagerank_convergence(self, algorithm_engine):
        graph = create_random_graph(100, 500)
        
        result = algorithm_engine.execute("pagerank", graph, {"max_iterations": 100})
        
        assert result.iterations <= 100
        assert result.final_l1_norm < 1e-6
```

### Integration Tests

```python
class TestEndToEndAlgorithms:
    async def test_algorithm_flow(self, algorithm_system):
        # Load test graph
        await algorithm_system.load_test_graph()
        
        # Execute PageRank
        pagerank_result = await algorithm_system.execute_algorithm("pagerank")
        assert pagerank_result.converged == True
        
        # Execute Community Detection
        community_result = await algorithm_system.execute_algorithm("louvain")
        assert community_result.num_communities > 0
        
        # Execute Shortest Path
        path_result = await algorithm_system.execute_algorithm(
            "shortest_path",
            {"source": "node1", "target": "node100"}
        )
        assert path_result.distance > 0
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class GraphAlgorithmUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def execute_pagerank(self):
        self.client.post("/api/v1/algorithms/pagerank", json={
            "damping_factor": 0.85,
            "max_iterations": 100
        })
    
    @task(5)
    def execute_community(self):
        self.client.post("/api/v1/algorithms/community", json={
            "algorithm": "louvain"
        })
    
    @task(3)
    def execute_shortest_path(self):
        self.client.post("/api/v1/algorithms/shortest-path", json={
            "source": f"node-{self.source_counter}",
            "target": f"node-{self.target_counter}"
        })
        self.source_counter += 1
        self.target_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/algorithms/pagerank", methods=["POST"])
@app.route("/api/v2/algorithms/pagerank", methods=["POST"])
async def execute_pagerank():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await execute_pagerank_v2()
    return await execute_pagerank_v1()
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

- **PageRank**: Algorithm for ranking nodes by importance
- **Community Detection**: Identifying groups of densely connected nodes
- **Centrality**: Measure of node importance in a graph
- **Shortest Path**: Minimum distance path between two nodes
- **Graph Coloring**: Assigning colors to nodes such that no adjacent nodes share the same color
- **Modularity**: Quality metric for community structure
- **Damping Factor**: PageRank parameter controlling random walk behavior
- **Betweenness Centrality**: Measure of node importance based on shortest paths
- **Louvain Algorithm**: Greedy modularity optimization for community detection
- **Dijkstra's Algorithm**: Shortest path algorithm for weighted graphs

## Changelog

### Version 2.0.0 (2026-07-01)
- Added incremental algorithm updates
- Implemented parallel processing
- Enhanced result caching
- Added GraphBLAS integration

### Version 1.5.0 (2026-01-15)
- Added community detection algorithms
- Implemented centrality measures
- Enhanced visualization

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic PageRank
- Simple shortest path

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def execute_algorithm(
    algorithm: str,
    graph_data: Dict,
    params: Dict = None,
) -> AlgorithmResult:
    """Execute a graph algorithm.
    
    Args:
        algorithm: Algorithm name.
        graph_data: Graph data.
        params: Algorithm parameters.
    
    Returns:
        Algorithm result.
    
    Raises:
        AlgorithmError: If algorithm execution fails.
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

Copyright (c) 2026 Graph Algorithms Platform

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
