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

## Graph Algorithms: Foundation

### Breadth-First Search (BFS)

Explores nodes level by level, discovering shortest paths in unweighted graphs. Foundation for many network analysis algorithms.

```python
from collections import deque

def bfs_shortest_paths(graph, source):
    """BFS from source, returns distances and predecessors."""
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[source] = 0
    queue = deque([source])

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current] + 1
                predecessors[neighbor] = current
                queue.append(neighbor)

    return distances, predecessors

def reconstruct_path(predecessors, target):
    """Reconstruct shortest path from BFS predecessors."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = predecessors[current]
    return path[::-1]

# Example social network
social_graph = {
    'Alice': ['Bob', 'Carol', 'David'],
    'Bob': ['Alice', 'Eve', 'Frank'],
    'Carol': ['Alice', 'Grace'],
    'David': ['Alice', 'Heidi'],
    'Eve': ['Bob', 'Ivan'],
    'Frank': ['Bob'],
    'Grace': ['Carol'],
    'Heidi': ['David'],
    'Ivan': ['Eve']
}

distances, predecessors = bfs_shortest_paths(social_graph, 'Alice')
print(f"Alice to Ivan: {reconstruct_path(predecessors, 'Ivan')}")
# Output: ['Alice', 'Bob', 'Eve', 'Ivan'] - 3 hops
```

### Dijkstra's Algorithm for Weighted Networks

Handles weighted edges (e.g., interaction frequency, relationship strength). Uses priority queue for O((V + E) log V) complexity.

```python
import heapq

def dijkstra_weighted(graph, source, weights):
    """
    Shortest paths in weighted social network.
    graph: adjacency list
    weights: dict of (u, v) -> weight
    """
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[source] = 0
    pq = [(0, source)]

    while pq:
        dist, current = heapq.heappop(pq)
        if dist > distances[current]:
            continue
        for neighbor in graph[current]:
            weight = weights.get((current, neighbor), 1.0)
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, predecessors

# Weighted interactions (higher = stronger connection)
interaction_weights = {
    ('Alice', 'Bob'): 0.8,
    ('Alice', 'Carol'): 0.6,
    ('Alice', 'David'): 0.3,
    ('Bob', 'Eve'): 0.9,
    ('Eve', 'Ivan'): 0.4
}

dist, pred = dijkstra_weighted(social_graph, 'Alice', interaction_weights)
print(f"Weighted distance to Ivan: {dist['Ivan']:.2f}")
# Output: Weighted distance to Ivan: 2.10
```

### A* Heuristic Search

Accelerates shortest path with domain-specific heuristics. In social networks, geographic proximity or community membership can guide search.

```python
import heapq

def a_star_social(graph, source, target, heuristic, weights=None):
    """
    A* search for social network paths.
    heuristic: function(node) -> estimated distance to target
    """
    if weights is None:
        weights = {}

    g_score = {node: float('inf') for node in graph}
    g_score[source] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[source] = heuristic(source, target)
    came_from = {}
    open_set = [(f_score[source], source)]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(source)
            return path[::-1]

        for neighbor in graph[current]:
            weight = weights.get((current, neighbor), 1.0)
            tentative_g = g_score[current] + weight

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, target)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

# Heuristic: same community = 0, different community = 1
community_map = {'Alice': 'A', 'Bob': 'A', 'Eve': 'B', 'Ivan': 'B'}

def community_heuristic(node, target):
    return 0 if community_map.get(node) == community_map.get(target) else 1

path = a_star_social(social_graph, 'Alice', 'Ivan', community_heuristic)
print(f"A* path: {path}")
```

## Advanced Centrality Implementations

### PageRank

Recursive centrality where importance flows through the network. Each node distributes its rank equally to neighbors. Includes damping factor d (typically 0.85) representing probability of following a link vs random jump.

```python
import numpy as np

def pagerank(graph, damping=0.85, max_iter=100, tol=1e-6):
    """
    Compute PageRank for all nodes.
    Returns dict of node -> rank score.
    """
    nodes = list(graph.keys())
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}

    # Build adjacency matrix
    A = np.zeros((n, n))
    for node, neighbors in graph.items():
        if neighbors:
            for neighbor in neighbors:
                A[node_to_idx[neighbor]][node_to_idx[node]] = 1.0 / len(neighbors)

    # Handle dangling nodes (no outgoing links)
    dangling = np.array([
        1.0 / n if len(graph.get(nodes[i], [])) == 0 else 0
        for i in range(n)
    ])

    # Power iteration
    pr = np.ones(n) / n

    for iteration in range(max_iter):
        pr_new = (1 - damping) / n + damping * (A @ pr + dangling @ pr)

        if np.linalg.norm(pr_new - pr, ord=1) < tol:
            print(f"PageRank converged after {iteration + 1} iterations")
            break
        pr = pr_new

    return {nodes[i]: pr[i] for i in range(n)}

# Larger social network
large_graph = {
    'Alice': ['Bob', 'Carol', 'David'],
    'Bob': ['Alice', 'Carol', 'Eve', 'Frank'],
    'Carol': ['Alice', 'Bob', 'Grace'],
    'David': ['Alice', 'Heidi'],
    'Eve': ['Bob', 'Frank', 'Ivan'],
    'Frank': ['Bob', 'Eve'],
    'Grace': ['Carol'],
    'Heidi': ['David', 'Ivan'],
    'Ivan': ['Eve', 'Heidi'],
    'Judy': ['Alice', 'Bob', 'Carol']  # New connected node
}

ranks = pagerank(large_graph)
sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
for node, rank in sorted_ranks[:5]:
    print(f"{node}: {rank:.4f}")
# Output shows relative importance based on link structure
```

### HITS (Hubs and Authorities)

Two-score system: hubs point to many authorities, authorities are pointed to by many hubs. Alternates between hub and authority updates until convergence.

```python
import numpy as np

def hits_algorithm(graph, max_iter=100, tol=1e-6):
    """
    HITS algorithm returning hub and authority scores.
    Useful for identifying information sources (authorities)
    and information brokers (hubs).
    """
    nodes = list(graph.keys())
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}

    # Build adjacency matrix
    A = np.zeros((n, n))
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor in node_to_idx:
                A[node_to_idx[neighbor]][node_to_idx[node]] = 1.0

    # Initialize
    h = np.ones(n) / n  # hub scores
    a = np.ones(n) / n  # authority scores

    for iteration in range(max_iter):
        # Update authorities: sum of hub scores of nodes pointing to this node
        a_new = A.T @ h
        a_new /= np.linalg.norm(a_new) if np.linalg.norm(a_new) > 0 else 1

        # Update hubs: sum of authority scores of nodes this node points to
        h_new = A @ a_new
        h_new /= np.linalg.norm(h_new) if np.linalg.norm(h_new) > 0 else 1

        if (np.linalg.norm(h_new - h) + np.linalg.norm(a_new - a)) < tol:
            print(f"HITS converged after {iteration + 1} iterations")
            break

        h, a = h_new, a_new

    return {
        'hubs': {nodes[i]: h[i] for i in range(n)},
        'authorities': {nodes[i]: a[i] for i in range(n)}
    }

hits = hits_algorithm(large_graph)
print("\nTop Hubs (information brokers):")
for node, score in sorted(hits['hubs'].items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"  {node}: {score:.4f}")

print("\nTop Authorities (information sources):")
for node, score in sorted(hits['authorities'].items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"  {node}: {score:.4f}")
```

### PageRank Variants

**Personalized PageRank (PPR)**: Random walk biased toward specific nodes. Identifies local neighborhoods and influence zones.

```python
def personalized_pagerank(graph, seed_nodes, damping=0.85, max_iter=100):
    """
    Personalized PageRank from seed nodes.
    Reveals local community structure around seeds.
    """
    nodes = list(graph.keys())
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}

    A = np.zeros((n, n))
    for node, neighbors in graph.items():
        if neighbors:
            for neighbor in neighbors:
                A[node_to_idx[neighbor]][node_to_idx[node]] = 1.0 / len(neighbors)

    # Personalization vector: concentrated on seed nodes
    personalization = np.zeros(n)
    for seed in seed_nodes:
        personalization[node_to_idx[seed]] = 1.0 / len(seed_nodes)

    # Handle dangling nodes
    dangling = np.zeros(n)
    for i, node in enumerate(nodes):
        if len(graph.get(node, [])) == 0:
            dangling[i] = 1.0

    pr = personalization.copy()

    for _ in range(max_iter):
        pr_new = (1 - damping) * personalization + damping * (A @ pr + (dangling @ pr) * personalization)

        if np.linalg.norm(pr_new - pr, ord=1) < 1e-8:
            break
        pr = pr_new

    return {nodes[i]: pr[i] for i in range(n)}

# Find nodes influenced by Alice
alice_influence = personalized_pagerank(large_graph, ['Alice'])
top_influenced = sorted(alice_influence.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nAlice's influence zone:")
for node, score in top_influenced:
    print(f"  {node}: {score:.4f}")
```

## Community Detection: Advanced Methods

### Modularity Optimization

Quantifies community quality. Q ranges from -0.5 to 1.0; values > 0.3 indicate significant community structure.

```python
def modularity(graph, communities):
    """
    Compute modularity Q for a given partition.
    communities: dict mapping node -> community_id
    """
    m = sum(len(neighbors) for neighbors in graph.values()) / 2
    if m == 0:
        return 0.0

    Q = 0.0
    nodes = list(graph.keys())

    for i in nodes:
        for j in nodes:
            if communities.get(i) == communities.get(j):
                # Number of edges between i and j (0 or 1 for simple graph)
                A_ij = 1.0 if j in graph.get(i, []) else 0.0
                k_i = len(graph.get(i, []))
                k_j = len(graph.get(j, []))
                Q += A_ij - (k_i * k_j) / (2 * m)

    return Q / (2 * m)

# Test different partitions
partition_1 = {node: 0 if node in ['Alice', 'Bob', 'Carol'] else 1
               for node in large_graph}
partition_2 = {node: 0 if node in ['Alice', 'Bob', 'Carol', 'Grace'] else 1
               for node in large_graph}

print(f"Partition 1 modularity: {modularity(large_graph, partition_1):.4f}")
print(f"Partition 2 modularity: {modularity(large_graph, partition_2):.4f}")
```

### Louvain Implementation

```python
def louvain_single_pass(graph):
    """
    Single pass of Louvain algorithm.
    Returns new community assignments and aggregated graph.
    """
    nodes = list(graph.keys())
    communities = {node: i for i, node in enumerate(nodes)}  # Each node starts in own community
    m = sum(len(neighbors) for neighbors in graph.values()) / 2

    improved = True
    while improved:
        improved = False
        for node in nodes:
            current_comm = communities[node]
            best_comm = current_comm
            best_gain = 0.0

            # Sum of weights to neighbors in each community
            neighbor_comms = {}
            for neighbor in graph[node]:
                comm = communities[neighbor]
                neighbor_comms[comm] = neighbor_comms.get(comm, 0) + 1.0

            k_i = len(graph[node])

            # Try each neighboring community
            for comm, weight in neighbor_comms.items():
                if comm == current_comm:
                    continue

                # Modularity gain from moving node to comm
                sum_in = sum(1 for n in graph[node] if communities[n] == comm)
                sum_tot = sum(1 for n in nodes if communities[n] == comm)

                gain = (sum_in - sum_tot * k_i / (2 * m))

                if gain > best_gain:
                    best_gain = gain
                    best_comm = comm

            if best_comm != current_comm:
                communities[node] = best_comm
                improved = True

    return communities

communities = louvain_single_pass(large_graph)
print("\nLouvain communities:")
comm_groups = {}
for node, comm in communities.items():
    comm_groups.setdefault(comm, []).append(node)
for comm, members in comm_groups.items():
    print(f"  Community {comm}: {', '.join(members)}")
```

### Label Propagation with Weighted Edges

```python
import random

def weighted_label_propagation(graph, weights, max_iter=100):
    """
    Weighted label propagation for community detection.
    Weights influence label adoption probability.
    """
    labels = {node: node for node in graph}

    for iteration in range(max_iter):
        changed = False
        nodes = list(graph.keys())
        random.shuffle(nodes)

        for node in nodes:
            # Aggregate weights by neighbor labels
            label_weights = {}
            for neighbor in graph[node]:
                w = weights.get((node, neighbor), 1.0)
                lbl = labels[neighbor]
                label_weights[lbl] = label_weights.get(lbl, 0) + w

            if label_weights:
                # Select label with probability proportional to weight
                total = sum(label_weights.values())
                r = random.random() * total
                cumulative = 0.0
                for lbl, w in label_weights.items():
                    cumulative += w
                    if cumulative >= r:
                        if labels[node] != lbl:
                            labels[node] = lbl
                            changed = True
                        break

        if not changed:
            print(f"Label propagation converged after {iteration + 1} iterations")
            break

    return labels

weighted_labels = weighted_label_propagation(large_graph, interaction_weights)
print("\nWeighted label propagation results:")
wl_groups = {}
for node, lbl in weighted_labels.items():
    wl_groups.setdefault(lbl, []).append(node)
for lbl, members in wl_groups.items():
    print(f"  Group {lbl}: {', '.join(members)}")
```

### Spectral Clustering for Communities

Uses eigenvalues of graph Laplacian to embed nodes in low-dimensional space, then applies k-means.

```python
import numpy as np
from scipy import linalg

def spectral_clustering(graph, n_clusters):
    """
    Spectral clustering using normalized graph Laplacian.
    Maps nodes to eigenvector space, then clusters.
    """
    nodes = list(graph.keys())
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}

    # Adjacency matrix
    A = np.zeros((n, n))
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            A[node_to_idx[node]][node_to_idx[neighbor]] = 1.0
            A[node_to_idx[neighbor]][node_to_idx[node]] = 1.0

    # Degree matrix
    D = np.diag(A.sum(axis=1))

    # Normalized Laplacian: L_norm = I - D^(-1/2) A D^(-1/2)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(A.sum(axis=1) + 1e-10))
    L_norm = np.eye(n) - D_inv_sqrt @ A @ D_inv_sqrt

    # Eigendecomposition (smallest eigenvalues)
    eigenvalues, eigenvectors = linalg.eigh(L_norm)

    # Take first n_clusters eigenvectors
    U = eigenvectors[:, :n_clusters]

    # Normalize rows
    row_norms = np.linalg.norm(U, axis=1, keepdims=True)
    U = U / (row_norms + 1e-10)

    # K-means on rows of U
    # Simple k-means implementation
    centroids = U[:n_clusters].copy()
    labels = np.zeros(n, dtype=int)

    for _ in range(20):
        # Assign to nearest centroid
        for i in range(n):
            distances = [np.linalg.norm(U[i] - centroids[j]) for j in range(n_clusters)]
            labels[i] = np.argmin(distances)

        # Update centroids
        for j in range(n_clusters):
            members = U[labels == j]
            if len(members) > 0:
                centroids[j] = members.mean(axis=0)

    return {nodes[i]: int(labels[i]) for i in range(n)}

spectral_communities = spectral_clustering(large_graph, n_clusters=3)
print("\nSpectral clustering (3 communities):")
sc_groups = {}
for node, comm in spectral_communities.items():
    sc_groups.setdefault(comm, []).append(node)
for comm, members in sc_groups.items():
    print(f"  Cluster {comm}: {', '.join(members)}")
```

## Link Prediction

Predicting which edges will form in the future or which are missing.

### Common Neighbors and Jaccard

```python
def common_neighbors_score(graph, node_a, node_b):
    """Score = |neighbors(A) ∩ neighbors(B)|"""
    return len(set(graph.get(node_a, [])) & set(graph.get(node_b, [])))

def jaccard_coefficient(graph, node_a, node_b):
    """Jaccard = |intersection| / |union|"""
    neighbors_a = set(graph.get(node_a, []))
    neighbors_b = set(graph.get(node_b, []))
    intersection = len(neighbors_a & neighbors_b)
    union = len(neighbors_a | neighbors_b)
    return intersection / union if union > 0 else 0.0

def adamic_adar(graph, node_a, node_b):
    """
    Adamic-Adar: sum(1 / log(degree(z))) for shared neighbors z.
    Nodes with fewer neighbors as common neighbors score higher.
    """
    common = set(graph.get(node_a, [])) & set(graph.get(node_b, []))
    score = 0.0
    for z in common:
        degree_z = len(graph.get(z, []))
        if degree_z > 1:
            score += 1.0 / np.log(degree_z)
    return score

# Predict missing edges
print("\nLink prediction scores:")
nodes = list(large_graph.keys())
candidate_pairs = []
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        if nodes[j] not in large_graph.get(nodes[i], []):
            candidate_pairs.append((nodes[i], nodes[j]))

predictions = []
for a, b in candidate_pairs:
    cn = common_neighbors_score(large_graph, a, b)
    if cn > 0:
        jac = jaccard_coefficient(large_graph, a, b)
        aa = adamic_adar(large_graph, a, b)
        predictions.append((a, b, cn, jac, aa))

predictions.sort(key=lambda x: x[4], reverse=True)
print("Top predicted links (Adamic-Adar):")
for a, b, cn, jac, aa in predictions[:5]:
    print(f"  {a} <-> {b}: CN={cn}, Jaccard={jac:.3f}, AA={aa:.3f}")
```

### Preferential Attachment

```python
def preferential_attachment(graph, node_a, node_b):
    """
    P(A, B) = |neighbors(A)| * |neighbors(B)|.
    Hub nodes more likely to connect (rich get richer).
    """
    return len(graph.get(node_a, [])) * len(graph.get(node_b, []))

# Resource Allocation Index
def resource_allocation(graph, node_a, node_b):
    """
    RA = sum(1 / |neighbors(z)|) for shared neighbors z.
    Similar to Adamic-Adar but uses degree instead of log(degree).
    """
    common = set(graph.get(node_a, [])) & set(graph.get(node_b, []))
    return sum(1.0 / len(graph.get(z, [])) for z in common)

print("\nPreferential attachment scores:")
for a, b, *_ in predictions[:5]:
    pa = preferential_attachment(large_graph, a, b)
    ra = resource_allocation(large_graph, a, b)
    print(f"  {a} <-> {b}: PA={pa}, RA={ra:.3f}")
```

## Information Diffusion Models

### Independent Cascade Model

```python
import random

def independent_cascade(graph, seeds, probability=0.1, max_steps=10):
    """
    Independent Cascade diffusion model.
    Each active node gets one chance to activate each inactive neighbor.
    Returns set of activated nodes per step.
    """
    active = set(seeds)
    newly_active = set(seeds)
    history = [set(seeds)]

    for step in range(max_steps):
        next_active = set()
        for node in newly_active:
            for neighbor in graph.get(node, []):
                if neighbor not in active and random.random() < probability:
                    next_active.add(neighbor)

        if not next_active:
            break

        active.update(next_active)
        newly_active = next_active
        history.append(set(next_active))

    return active, history

# Run multiple simulations
n_simulations = 100
spread_counts = []
for _ in range(n_simulations):
    activated, _ = independent_cascade(large_graph, ['Alice'], probability=0.3)
    spread_counts.append(len(activated))

avg_spread = sum(spread_counts) / len(spread_counts)
print(f"\nIC Model (p=0.3, seed=Alice):")
print(f"  Average spread: {avg_spread:.1f} nodes")
print(f"  Min spread: {min(spread_counts)}")
print(f"  Max spread: {max(spread_counts)}")
```

### Linear Threshold Model

```python
def linear_threshold(graph, seeds, thresholds=None, weights=None):
    """
    Linear Threshold diffusion model.
    Node activates when weighted input from active neighbors >= threshold.
    """
    if thresholds is None:
        thresholds = {node: 0.5 for node in graph}
    if weights is None:
        # Uniform weights normalized by degree
        weights = {}
        for node, neighbors in graph.items():
            w = 1.0 / len(neighbors) if neighbors else 0
            for neighbor in neighbors:
                weights[(node, neighbor)] = w

    active = set(seeds)
    history = [set(seeds)]

    changed = True
    while changed:
        changed = False
        next_active = set()

        for node in graph:
            if node not in active:
                influence = sum(
                    weights.get((neighbor, node), 0)
                    for neighbor in active
                    if neighbor in graph and node in graph[neighbor]
                )
                if influence >= thresholds[node]:
                    next_active.add(node)
                    changed = True

        active.update(next_active)
        if next_active:
            history.append(set(next_active))

    return active, history

# Define custom thresholds (influential nodes harder to activate)
thresholds = {
    'Alice': 0.8,  # Hard to influence
    'Bob': 0.3,    # Easily influenced
    'Eve': 0.4,
    'Ivan': 0.5
}

lt_active, lt_history = linear_threshold(large_graph, ['Alice'], thresholds)
print(f"\nLT Model (seed=Alice):")
print(f"  Total activated: {len(lt_active)} nodes")
print(f"  Steps: {len(lt_history)}")
for step, activated in enumerate(lt_history):
    print(f"  Step {step}: {', '.join(sorted(activated))}")
```

### SIR Epidemic Model

```python
def sir_model(graph, seeds, beta=0.3, gamma=0.1, max_steps=50):
    """
    SIR (Susceptible-Infected-Recovered) model.
    beta: infection probability per contact
    gamma: recovery probability per step
    Returns trajectory of S, I, R counts.
    """
    susceptible = set(graph.keys()) - set(seeds)
    infected = set(seeds)
    recovered = set()

    trajectory = [(len(susceptible), len(infected), len(recovered))]

    for step in range(max_steps):
        new_infected = set()
        new_recovered = set()

        # Infection phase
        for node in infected:
            for neighbor in graph.get(node, []):
                if neighbor in susceptible and random.random() < beta:
                    new_infected.add(neighbor)

        # Recovery phase
        for node in infected:
            if random.random() < gamma:
                new_recovered.add(node)

        susceptible -= new_infected
        infected = (infected - new_recovered) | new_infected
        recovered |= new_recovered

        trajectory.append((len(susceptible), len(infected), len(recovered)))

        if not infected:
            break

    return trajectory

# Simulate epidemic
trajectory = sir_model(large_graph, seeds=['Alice'], beta=0.4, gamma=0.1)
print(f"\nSIR Model (beta=0.4, gamma=0.1, seed=Alice):")
print(f"  Peak infected: {max(t[1] for t in trajectory)} at step "
      f"{next(i for i, t in enumerate(trajectory) if t[1] == max(t2[1] for t2 in trajectory))}")
print(f"  Final recovered: {trajectory[-1][2]}")
print(f"  Total epidemic duration: {len(trajectory) - 1} steps")
```

## Graph Neural Networks for Social Analysis

### Graph Convolutional Network (GCN)

Aggregates features from neighbors, enabling node classification and link prediction.

```python
import numpy as np

class SimpleGCN:
    """
    Simplified Graph Convolutional Network.
    H^(l+1) = sigma(D^(-1/2) A D^(-1/2) H^(l) W^(l))
    """
    def __init__(self, adjacency, input_dim, hidden_dim, output_dim):
        self.A = adjacency.astype(float)
        self.n = self.A.shape[0]

        # Add self-loops
        self.A += np.eye(self.n)

        # Degree matrix
        D = np.diag(self.A.sum(axis=1))
        D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D) + 1e-10))

        # Normalized adjacency
        self.A_norm = D_inv_sqrt @ self.A @ D_inv_sqrt

        # Initialize weights
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.01
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.01

    def relu(self, x):
        return np.maximum(0, x)

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / exp_x.sum(axis=1, keepdims=True)

    def forward(self, X):
        """
        X: (n_nodes, input_dim) feature matrix
        """
        # Layer 1
        H = self.relu(self.A_norm @ X @ self.W1)
        # Layer 2
        H = self.A_norm @ H @ self.W2
        return self.softmax(H)

# Create feature matrix (node degree as feature + random features)
n_nodes = len(large_graph)
nodes = list(large_graph.keys())
node_to_idx = {node: i for i, node in enumerate(nodes)}

features = np.zeros((n_nodes, 4))
for i, node in enumerate(nodes):
    features[i, 0] = len(large_graph[node])  # Degree
    features[i, 1] = np.random.randn()  # Random feature 1
    features[i, 2] = np.random.randn()  # Random feature 2
    features[i, 3] = np.random.randn()  # Random feature 3

# Adjacency matrix
A = np.zeros((n_nodes, n_nodes))
for node, neighbors in large_graph.items():
    for neighbor in neighbors:
        if neighbor in node_to_idx:
            A[node_to_idx[node]][node_to_idx[neighbor]] = 1.0

# Create and run GCN
gcn = SimpleGCN(A, input_dim=4, hidden_dim=8, output_dim=3)
output = gcn.forward(features)

print("\nGCN node embeddings (output probabilities):")
for i, node in enumerate(nodes):
    print(f"  {node}: [{', '.join(f'{p:.3f}' for p in output[i])}]")
```

### Graph Attention Network (GAT)

Learns attention weights for neighbor importance, enabling adaptive feature aggregation.

```python
class SimpleGAT:
    """
    Simplified Graph Attention Network.
    alpha_ij = softmax_j(LeakyReLU(a^T [Wh_i || Wh_j]))
    """
    def __init__(self, adjacency, input_dim, hidden_dim, n_heads=2):
        self.A = adjacency.astype(float)
        self.n = self.A.shape[0]
        self.n_heads = n_heads

        # Add self-loops
        self.A += np.eye(self.n)

        # Weight matrices per head
        self.W_heads = [
            np.random.randn(input_dim, hidden_dim) * 0.01
            for _ in range(n_heads)
        ]
        self.a_vectors = [
            np.random.randn(2 * hidden_dim, 1) * 0.01
            for _ in range(n_heads)
        ]

    def leaky_relu(self, x, alpha=0.2):
        return np.where(x > 0, x, alpha * x)

    def forward(self, X):
        """
        Returns concatenated multi-head attention output.
        """
        outputs = []

        for head in range(self.n_heads):
            Wh = X @ self.W_heads[head]  # (n, hidden_dim)

            # Compute attention scores
            attention_scores = np.zeros((self.n, self.n))
            for i in range(self.n):
                for j in range(self.n):
                    if self.A[i, j] > 0:
                        pair = np.concatenate([Wh[i], Wh[j]])
                        attention_scores[i, j] = self.a_vectors[head].T @ pair

            # Mask non-neighbors
            attention_scores = attention_scores * self.A
            attention_scores = self.leaky_relu(attention_scores)

            # Softmax per row
            exp_scores = np.exp(attention_scores - attention_scores.max(axis=1, keepdims=True))
            attention_weights = exp_scores / (exp_scores.sum(axis=1, keepdims=True) + 1e-10)

            # Aggregate
            head_output = attention_weights @ Wh
            outputs.append(head_output)

        return np.concatenate(outputs, axis=1)

gat = SimpleGAT(A, input_dim=4, hidden_dim=4, n_heads=2)
gat_output = gat.forward(features)
print(f"\nGAT output shape: {gat_output.shape}")
print("GAT node representations (first 3 nodes):")
for i in range(min(3, len(nodes))):
    print(f"  {nodes[i]}: {gat_output[i, :4]}")
```

## Network Robustness and Percolation

### Targeted vs Random Attack Simulation

```python
import random

def attack_simulation(graph, strategy='random', removal_fraction=0.1):
    """
    Simulate network under attack by removing nodes.
    strategy: 'random', 'degree', 'betweenness'
    Returns list of (fraction_removed, largest_component_size) pairs.
    """
    nodes = list(graph.keys())
    n_original = len(nodes)
    remaining = set(nodes)
    results = []

    # Pre-compute attack order
    if strategy == 'degree':
        attack_order = sorted(nodes, key=lambda n: len(graph.get(n, [])), reverse=True)
    elif strategy == 'betweenness':
        # Approximate betweenness for attack ordering
        betweenness = {}
        for node in nodes:
            paths_through = 0
            total_paths = 0
            for source in nodes:
                if source == node:
                    continue
                for target in nodes:
                    if target == source or target == node:
                        continue
                    # Simple path counting
                    if target in graph.get(source, []):
                        total_paths += 1
                        if node in graph.get(source, []):
                            paths_through += 1
            betweenness[node] = paths_through / max(total_paths, 1)
        attack_order = sorted(nodes, key=lambda n: betweenness[n], reverse=True)
    else:
        attack_order = nodes.copy()
        random.shuffle(attack_order)

    # Remove nodes and track largest component
    n_remove = int(n_original * removal_fraction)
    for i in range(0, n_original, max(1, n_original // 10)):
        # Find largest connected component in remaining graph
        visited = set()
        largest = 0

        for node in remaining:
            if node not in visited:
                component = set()
                stack = [node]
                while stack:
                    current = stack.pop()
                    if current in component:
                        continue
                    component.add(current)
                    visited.add(current)
                    for neighbor in graph.get(current, []):
                        if neighbor in remaining and neighbor not in component:
                            stack.append(neighbor)
                largest = max(largest, len(component))

        fraction_removed = 1.0 - len(remaining) / n_original
        results.append((fraction_removed, largest / n_original))

        # Remove next nodes
        nodes_to_remove = attack_order[i:i + max(1, n_original // 10)]
        for node in nodes_to_remove:
            remaining.discard(node)

    return results

# Compare attack strategies
print("\nNetwork robustness under different attack strategies:")
for strategy in ['random', 'degree', 'betweenness']:
    results = attack_simulation(large_graph, strategy)
    critical_point = next((f for f, s in results if s < 0.5), 1.0)
    print(f"  {strategy:12} attack: critical failure at {critical_point:.1%} removal")
```

## Temporal Network Analysis

### Time-Sliced Analysis

```python
def temporal_sliced_analysis(interactions, window_size=5):
    """
    Analyze network evolution over time windows.
    interactions: list of (timestamp, source, target) tuples
    """
    # Sort by timestamp
    interactions.sort(key=lambda x: x[0])

    # Create time windows
    timestamps = [t for t, _, _ in interactions]
    min_time, max_time = min(timestamps), max(timestamps)

    windows = []
    current_start = min_time

    while current_start < max_time:
        current_end = current_start + window_size
        window_interactions = [
            (t, s, target) for t, s, target in interactions
            if current_start <= t < current_end
        ]

        # Build graph for this window
        window_graph = {}
        for _, source, target in window_interactions:
            window_graph.setdefault(source, set()).add(target)
            window_graph.setdefault(target, set()).add(source)

        # Compute metrics for this window
        metrics = {
            'n_nodes': len(window_graph),
            'n_edges': sum(len(neighbors) for neighbors in window_graph.values()) // 2,
            'density': 0,
            'avg_degree': 0
        }

        if metrics['n_nodes'] > 1:
            metrics['density'] = (
                2 * metrics['n_edges'] /
                (metrics['n_nodes'] * (metrics['n_nodes'] - 1))
            )
            metrics['avg_degree'] = (
                sum(len(n) for n in window_graph.values()) / metrics['n_nodes']
            )

        windows.append({
            'start': current_start,
            'end': current_end,
            'metrics': metrics
        })
        current_start = current_end

    return windows

# Simulate temporal interactions
temporal_interactions = []
for i in range(100):
    t = i * 0.5
    source = random.choice(list(large_graph.keys()))
    target = random.choice(list(large_graph.get(source, [])))
    temporal_interactions.append((t, source, target))

windows = temporal_sliced_analysis(temporal_interactions, window_size=10)
print("\nTemporal network evolution:")
for w in windows:
    m = w['metrics']
    print(f"  [{w['start']:.1f}-{w['end']:.1f}]: "
          f"nodes={m['n_nodes']}, edges={m['n_edges']}, "
          f"density={m['density']:.3f}")
```

## Ego Network Analysis

```python
def ego_network(graph, node, depth=2):
    """
    Extract ego network (local neighborhood) around a node.
    Returns ego-centric graph with ego at center.
    """
    ego_nodes = set()
    ego_edges = set()
    frontier = {node}
    ego_nodes.add(node)

    for d in range(depth):
        next_frontier = set()
        for current in frontier:
            for neighbor in graph.get(current, []):
                if neighbor not in ego_nodes:
                    next_frontier.add(neighbor)
                    ego_nodes.add(neighbor)
                    ego_edges.add((current, neighbor))
                elif (neighbor, current) not in ego_edges:
                    ego_edges.add((current, neighbor))
        frontier = next_frontier

    # Build ego graph
    ego_graph = {n: set() for n in ego_nodes}
    for s, t in ego_edges:
        ego_graph[s].add(t)
        ego_graph[t].add(s)

    return ego_graph, ego_nodes, ego_edges

# Analyze ego networks
print("\nEgo network analysis:")
for node in ['Alice', 'Bob', 'Ivan']:
    ego_g, ego_n, ego_e = ego_network(large_graph, node, depth=2)
    density = 2 * len(ego_e) / (len(ego_n) * (len(ego_n) - 1)) if len(ego_n) > 1 else 0
    print(f"\n  {node}'s ego network (depth=2):")
    print(f"    Size: {len(ego_n)} nodes, {len(ego_e)} edges")
    print(f"    Density: {density:.3f}")
    print(f"    Members: {', '.join(sorted(ego_n))}")
```

## Configuration Patterns

### Analysis Pipeline Configuration

```yaml
# social_network_analysis_config.yaml
analysis:
  centrality:
    measures:
      - degree
      - betweenness
      - closeness
      - eigenvector
      - pagerank
    top_k: 10
    betweenness_sampling: 1000  # Sample paths for approximation

  communities:
    algorithm: louvain  # louvain | label_propagation | spectral | girvan_newman
    resolution: 1.0     # Higher = more communities
    min_community_size: 3

  diffusion:
    model: independent_cascade  # independent_cascade | linear_threshold | sir
    simulations: 100
    probability: 0.3
    seed_nodes: []

  link_prediction:
    metrics:
      - common_neighbors
      - jaccard
      - adamic_adar
      - preferential_attachment
    top_k: 20

  temporal:
    window_size: 3600     # seconds
    slide_size: 1800      # overlap control

database:
  type: neo4j  # neo4j | arangodb | tinkergraph
  uri: bolt://localhost:7687
  credentials:
    username: neo4j
    password_env: NEO4J_PASSWORD

output:
  format: json  # json | csv | graphml
  directory: ./results
  visualizations:
    enabled: true
    format: png
    layout: force_atlas2
```

### Neo4j Integration

```python
from neo4j import GraphDatabase

class SocialNetworkAnalyzer:
    """Neo4j-backed social network analysis."""

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def compute_degree_centrality(self, limit=10):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Person)
                WHERE (p)-[:FRIEND]->()
                RETURN p.name AS name,
                       size([(p)-[:FRIEND]->() | 1]) AS outDegree,
                       size([()<-[:FRIEND]-(p) | 1]) AS inDegree
                ORDER BY outDegree DESC
                LIMIT $limit
            """, limit=limit)
            return [dict(record) for record in result]

    def detect_communities_louvain(self):
        with self.driver.session() as session:
            result = session.run("""
                CALL gds.louvain.stream({
                    nodeProjection: 'Person',
                    relationshipProjection: 'FRIEND'
                })
                YIELD nodeId, communityId
                RETURN gds.util.asNode(nodeId).name AS name,
                       communityId
                ORDER BY communityId, name
            """)
            return [dict(record) for record in result]

    def find_influencers(self, seed, depth=3, limit=10):
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (seed:Person {name: $seed})-[:FRIEND*1..$depth]-(target:Person)
                RETURN target.name AS name,
                       count(path) AS influenceScore,
                       min(length(path)) AS minDistance
                ORDER BY influenceScore DESC
                LIMIT $limit
            """, seed=seed, depth=depth, limit=limit)
            return [dict(record) for record in result]

    def predict_links(self, threshold=0.5):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Person), (b:Person)
                WHERE a <> b
                  AND NOT (a)-[:FRIEND]->(b)
                  AND NOT (a)<-[:FRIEND]-(b)
                WITH a, b,
                     size([(a)-[:FRIEND]-(c)-[:FRIEND]-(b) | c]) AS commonFriends
                WHERE commonFriends > $threshold
                RETURN a.name AS source,
                       b.name AS target,
                       commonFriends
                ORDER BY commonFriends DESC
                LIMIT 20
            """, threshold=threshold)
            return [dict(record) for record in result]

# Usage
analyzer = SocialNetworkAnalyzer(
    "bolt://localhost:7687",
    "neo4j",
    os.environ.get("NEO4J_PASSWORD", "password")
)

try:
    degree = analyzer.compute_degree_centrality()
    print("\nTop users by degree centrality:")
    for record in degree:
        print(f"  {record['name']}: out={record['outDegree']}, in={record['inDegree']}")

    communities = analyzer.detect_communities_louvain()
    print(f"\nDetected {len(set(c['communityId'] for c in communities))} communities")

    influencers = analyzer.find_influencers('Alice')
    print("\nAlice's influencers:")
    for inf in influencers:
        print(f"  {inf['name']}: score={inf['influenceScore']}, distance={inf['minDistance']}")
finally:
    analyzer.close()
```

## Benchmarking and Performance

### Large-Scale Graph Metrics

```python
import time
from collections import defaultdict

def benchmark_centralities(graph, iterations=3):
    """Benchmark different centrality algorithms."""
    results = {}

    # Degree centrality (fastest)
    start = time.time()
    for _ in range(iterations):
        degree = {node: len(neighbors) for node, neighbors in graph.items()}
    results['degree'] = (time.time() - start) / iterations

    # BFS-based closeness (medium)
    start = time.time()
    for _ in range(iterations):
        closeness = {}
        for source in graph:
            distances = bfs_shortest_paths(graph, source)[0]
            total_dist = sum(d for d in distances.values() if d < float('inf'))
            closeness[source] = (len(graph) - 1) / total_dist if total_dist > 0 else 0
    results['closeness'] = (time.time() - start) / iterations

    # PageRank (medium-slow)
    start = time.time()
    for _ in range(iterations):
        pagerank(graph, max_iter=50)
    results['pagerank'] = (time.time() - start) / iterations

    return results

# Generate larger test graph
def generate_random_graph(n_nodes, avg_degree=6):
    """Generate Erdos-Renyi-like random graph."""
    graph = {f"node_{i}": set() for i in range(n_nodes)}
    nodes = list(graph.keys())

    for i in range(n_nodes):
        n_edges = random.randint(avg_degree // 2, avg_degree)
        targets = random.sample(nodes, min(n_edges, n_nodes - 1))
        for target in targets:
            if target != f"node_{i}":
                graph[f"node_{i}"].add(target)
                graph[target].add(f"node_{i}")

    return graph

# Benchmark
test_graph = generate_random_graph(500, avg_degree=10)
print("\nBenchmark results (500 nodes):")
benchmarks = benchmark_centralities(test_graph)
for algo, elapsed in sorted(benchmarks.items(), key=lambda x: x[1]):
    print(f"  {algo:12}: {elapsed*1000:.1f}ms")
```

## Common Pitfalls and Solutions

### Pitfall: Centrality in Disconnected Graphs

```python
def robust_centrality(graph, measure='betweenness'):
    """
    Handle disconnected graphs by computing centrality per component.
    Prevents misleading results where nodes in small components
    dominate due to local structure.
    """
    # Find connected components
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            component = set()
            stack = [node]
            while stack:
                current = stack.pop()
                if current in component:
                    continue
                component.add(current)
                visited.add(current)
                for neighbor in graph.get(current, []):
                    if neighbor not in component:
                        stack.append(neighbor)
            components.append(component)

    # Compute centrality per component, normalized by component size
    centrality = {}
    for component in components:
        subgraph = {n: graph[n] & component for n in component}
        n = len(component)

        if measure == 'degree':
            for node in component:
                centrality[node] = len(subgraph[node]) / max(1, n - 1)
        elif measure == 'pagerank':
            pr = pagerank(subgraph)
            centrality.update(pr)

    return centrality

# Test on disconnected graph
disconnected_graph = {
    'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'A', 'B'},
    'D': {'E'}, 'E': {'D'}
}

print("\nRobust centrality for disconnected graph:")
robust_c = robust_centrality(disconnected_graph, measure='degree')
for node, score in sorted(robust_c.items()):
    print(f"  {node}: {score:.3f}")
```

### Pitfall: Weighted vs Unweighted Interpretation

```python
def adaptive_centrality(graph, weights=None):
    """
    Automatically choose between weighted and unweighted analysis
    based on weight distribution.
    """
    if weights is None:
        # Unweighted - use simple degree
        return {node: len(neighbors) for node, neighbors in graph.items()}

    # Analyze weight distribution
    weight_values = list(weights.values())
    if not weight_values:
        return {node: len(neighbors) for node, neighbors in graph.items()}

    mean_w = np.mean(weight_values)
    std_w = np.std(weight_values)
    cv = std_w / mean_w if mean_w > 0 else 0

    if cv < 0.3:
        # Low variance - weights are similar, use unweighted
        print("Low weight variance (CV={:.2f}), using unweighted analysis".format(cv))
        return {node: len(neighbors) for node, neighbors in graph.items()}
    else:
        # High variance - weights matter
        print("High weight variance (CV={:.2f}), using weighted analysis".format(cv))
        centrality = {}
        for node in graph:
            weighted_degree = sum(
                weights.get((node, n), weights.get((n, node), 1.0))
                for n in graph[node]
            )
            centrality[node] = weighted_degree
        return centrality

adaptive_c = adaptive_centrality(large_graph, interaction_weights)
print("\nAdaptive centrality scores:")
for node, score in sorted(adaptive_c.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {node}: {score:.3f}")
```

## Summary of Metrics and Use Cases

| Metric | Best For | Complexity | Scales To |
|--------|----------|------------|-----------|
| Degree Centrality | Hub detection | O(V) | Millions |
| Betweenness | Information brokers | O(V*E) | ~100K (sampled) |
| Closeness | Information speed | O(V*(V+E)) | ~10K |
| Eigenvector | Recursive importance | O(V*E * iter) | ~100K |
| PageRank | Web/social importance | O(V*E * iter) | Millions |
| HITS | Hubs vs authorities | O(V*E * iter) | ~100K |
| Louvain | Community detection | O(V*log V) | Millions |
| Label Propagation | Fast communities | O(V*E) | Millions |
| Spectral | Balanced clusters | O(V^3) | ~10K |
| GCN/GAT | Node classification | O(V*E*d) | ~100K (batched) |
| Link Prediction | Missing edges | O(V^2) | ~10K |
| IC/LT Diffusion | Influence spread | O(V*E * sim) | ~100K |

## Further Reading

- **Network Science** by Albert-László Barabási (comprehensive textbook)
- **Social Network Analysis for Startups** by Maksim Tsvetovat
- **Networks, Crowds, and Markets** by Easley and Kleinberg (free online)
- **Graph Neural Networks** by Wu et al., 2020 (survey paper)
- **Community Detection** by Fortunato, 2010 (review article)
- NetworkX documentation: https://networkx.org
- igraph documentation: https://igraph.org
- Neo4j Graph Data Science: https://neo4j.com/docs/graph-data-science
