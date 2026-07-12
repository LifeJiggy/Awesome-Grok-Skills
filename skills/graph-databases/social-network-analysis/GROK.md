---
name: social-network-analysis
category: graph-databases
version: 1.0.0
tags:
  - social-network
  - centrality
  - community-detection
  - graph-metrics
  - influence
difficulty: intermediate
estimated_time: 45 minutes
prerequisites:
  - graph-theory-basics
  - linear-algebra
  - python-3.10+
---

# Social Network Analysis

Computational methods for analyzing social graphs: centrality measures, community detection, influence propagation, and graph-level metrics. Practical implementations using graph databases and Python.

## Centrality Measures

Centrality quantifies the importance of nodes within a network. Different centrality measures capture different notions of "importance."

### Degree Centrality

The simplest centrality measure: count of direct connections. In directed graphs, distinguish in-degree (popularity) from out-degree (activity).

```
Degree Centrality = degree(v) / (n - 1)
```

High degree centrality identifies hub nodes but misses nodes that serve as bridges between communities.

### Betweenness Centrality

Measures how often a node lies on shortest paths between other nodes. Nodes with high betweenness act as information brokers controlling flow between communities.

```
Betweenness(v) = sum(sigma_st(v) / sigma_st) for all s,t pairs
where sigma_st = number of shortest paths from s to t
sigma_st(v) = number passing through v
```

### Closeness Centrality

Measures how close a node is to all other nodes. High closeness means a node can reach the entire network quickly, important for information dissemination speed.

```
Closeness(v) = (n - 1) / sum(d(v, u)) for all u
```

### Eigenvector Centrality

Generalizes degree centrality by weighting connections based on the importance of connected nodes. A node is important if it connects to other important nodes. Basis of Google's PageRank.

```
Centrality(v) = (1 / lambda) * sum(A_vu * Centrality(u))
where A is the adjacency matrix, lambda is the largest eigenvalue
```

### Katz Centrality

Like eigenvector centrality but includes a damping factor. Accounts for all paths (not just shortest) with exponential decay by path length.

```
Katz(v) = alpha * sum(A_vu * Katz(u)) + beta
```

## Community Detection

Finding groups of densely connected nodes that are sparsely connected to other groups.

### Louvain Algorithm

Greedy modularity optimization. Fast hierarchical algorithm that detects communities by maximizing the modularity measure Q.

```
Q = (1/2m) * sum[A_ij - (k_i * k_j) / (2m)] * delta(c_i, c_j)
where m = number of edges, k_i = degree of node i
```

### Label Propagation

Simple and near-linear time. Each node adopts the most common label among its neighbors. Fast but non-deterministic; may not converge for some graphs.

### Girvan-Newman

Edge betweenness-based divisive clustering. Iteratively removes edges with highest betweenness centrality until desired number of communities is reached. O(VE^2) complexity; suitable for small graphs only.

### Label Propagation for Communities (LPA)

Each node starts with a unique label. In each iteration, each node adopts the label that appears most frequently among its neighbors. Converges quickly for most real-world networks.

## Influence Metrics

### Diffusion Models

**Independent Cascade**: Each active node gets one chance to activate each inactive neighbor with probability p.

**Linear Threshold**: Node becomes active when the sum of weights from active neighbors exceeds a threshold.

### Influence Maximization

Finding k seed nodes that maximize spread. NP-hard problem; greedy approximation with (1 - 1/e) guarantee via submodular function optimization.

### Structural Holes

Nodes bridging otherwise disconnected communities hold structural holes. Their removal fragments the network, making them critical for information flow.

## Graph Metrics

### Clustering Coefficient

Measures the tendency of nodes to form triangles. High clustering indicates tight-knit communities.

```
Local clustering = 2 * triangles(v) / (k * (k-1))
Global clustering = 3 * triangles / triangles_possible
```

### Assortativity

Correlation between connected nodes' properties. Social networks are typically assortative (popular nodes connect to popular nodes); technological networks are often disassortative.

### Small-World Property

Most pairs connected by short paths (small average path length) while maintaining high clustering. Real social networks typically have average path length ~6 (six degrees of separation).

### Network Density

```
Density = 2 * |E| / (|V| * (|V| - 1))
```

Complete graph has density 1. Real social networks are extremely sparse (density < 0.01).

## Graph Database Queries

### Centrality Queries in Cypher

```cypher
// Degree centrality
MATCH (p:Person)
RETURN p.name, size([(p)-[:FRIEND]->() | 1]) AS outDegree
ORDER BY outDegree DESC LIMIT 10

// Betweenness approximation via path sampling
MATCH (s:Person), (t:Person)
WHERE id(s) < id(t)
MATCH path = shortestPath((s)-[:FRIEND*]-(t))
UNWIND nodes(path) AS n
RETURN n.name, count(*) AS betweenness
ORDER BY betweenness DESC LIMIT 10

// Clustering coefficient
MATCH (p:Person)-[:FRIEND]-(friend:Person)
WITH p, collect(friend) AS friends
UNWIND friends AS f1
UNWIND friends AS f2
WITH p, f1, f2 WHERE f1 <> f2
OPTIONAL MATCH (f1)-[:FRIEND]-(f2)
RETURN p.name,
       count(DISTINCT f1) AS friends,
       count(DISTINCT f1) - count(DISTINCT CASE WHEN f1 = f2 THEN null END) AS triangles
```

### Community Detection in Cypher

```cypher
// Connected components
MATCH (p:Person)
OPTIONAL MATCH path = (p)-[:FRIEND*1..]-(connected:Person)
RETURN min(id(p)) AS componentId, count(DISTINCT connected) AS size
ORDER BY size DESC

// Find bridges (edges whose removal disconnects the graph)
MATCH (a)-[r:FRIEND]->(b)
WHERE NOT EXISTS {
  MATCH (a)-[:FRIEND*2..]-(b) WHERE NOT (a)-[r]->(b)
}
RETURN a.name, b.name
```

## Practical Considerations

1. **Scale**: Betweenness centrality is O(V*E) on sparse graphs. Use approximation via sampling for graphs > 1M nodes.
2. **Dynamic networks**: Recompute metrics incrementally as the graph evolves rather than from scratch.
3. **Weighted vs unweighted**: Most algorithms assume unweighted edges; extend with log-transformed weights for weighted analysis.
4. **Directed vs undirected**: Centrality measures differ significantly for directed graphs. Ensure your analysis matches your graph semantics.
5. **Temporal analysis**: Social connections change over time. Time-sliced analysis captures different patterns than static snapshots.

## Visualization Guidelines

1. Force-directed layouts for small networks (< 1000 nodes)
2. Community coloring for modular graphs
3. Node size proportional to centrality
4. Edge opacity for weight representation
5. Focus+context for large networks: show ego network + summary of broader structure
