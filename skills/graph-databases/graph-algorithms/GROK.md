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
