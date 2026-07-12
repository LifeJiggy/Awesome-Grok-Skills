"""
Graph Algorithms Toolkit

Implementations of fundamental graph algorithms: PageRank, Louvain community
detection, shortest path (Dijkstra, Bellman-Ford, Floyd-Warshall), centrality
measures, graph coloring, BFS/DFS, and minimum spanning tree.
"""

from __future__ import annotations

import math
import heapq
import random
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import defaultdict, deque

logger = __import__("logging").getLogger(__name__)


# ---------------------------------------------------------------------------
# Domain Enums
# ---------------------------------------------------------------------------

class AlgorithmType(Enum):
    PAGERANK = auto()
    LOUVAIN = auto()
    DIJKSTRA = auto()
    BELLMAN_FORD = auto()
    FLOYD_WARSHALL = auto()
    GREEDY_COLORING = auto()
    WELSH_POWELL = auto()
    BFS = auto()
    DFS = auto()
    KRUSKAL = auto()
    PRIM = auto()


class TraversalState(Enum):
    UNVISITED = auto()
    VISITING = auto()
    VISITED = auto()


class EdgeType(Enum):
    TREE = auto()
    BACK = auto()
    FORWARD = auto()
    CROSS = auto()


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class GraphEdge:
    source: str
    target: str
    weight: float = 1.0
    directed: bool = False

    def __hash__(self) -> int:
        return hash((self.source, self.target, self.weight))


@dataclass
class ShortestPathResult:
    source: str
    distances: dict[str, float]
    predecessors: dict[str, Optional[str]]
    has_negative_cycle: bool = False

    def path_to(self, target: str) -> list[str]:
        path: list[str] = []
        current: Optional[str] = target
        while current is not None:
            path.append(current)
            current = self.predecessors.get(current)
        path.reverse()
        return path if path[0] == self.source else []

    def distance_to(self, target: str) -> float:
        return self.distances.get(target, float("inf"))


@dataclass
class PageRankResult:
    scores: dict[str, float]
    iterations: int
    converged: bool

    def top_nodes(self, k: int = 10) -> list[tuple[str, float]]:
        sorted_nodes = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:k]


@dataclass
class CommunityResult:
    communities: dict[str, int]
    modularity: float
    num_communities: int

    def get_community_members(self, community_id: int) -> set[str]:
        return {node for node, cid in self.communities.items() if cid == community_id}


@dataclass
class ColoringResult:
    colors: dict[str, int]
    num_colors: int
    is_valid: bool


@dataclass
class MSTResult:
    edges: list[GraphEdge]
    total_weight: float


@dataclass
class DFSResult:
    discovery_order: list[str]
    finish_order: list[str]
    tree_edges: list[tuple[str, str]]
    back_edges: list[tuple[str, str]]
    has_cycle: bool
    topological_order: Optional[list[str]] = None


# ---------------------------------------------------------------------------
# Graph Representation
# ---------------------------------------------------------------------------

class AdjacencyListGraph:
    """Weighted graph with adjacency list representation."""

    def __init__(self, directed: bool = True) -> None:
        self._directed = directed
        self._adjacency: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self._nodes: set[str] = set()
        self._edges: list[GraphEdge] = []

    @property
    def nodes(self) -> list[str]:
        return list(self._nodes)

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    def add_node(self, node: str) -> None:
        self._nodes.add(node)

    def add_edge(self, source: str, target: str, weight: float = 1.0) -> None:
        self._nodes.add(source)
        self._nodes.add(target)
        self._adjacency[source].append((target, weight))
        if not self._directed:
            self._adjacency[target].append((source, weight))
        self._edges.append(GraphEdge(source, target, weight, self._directed))

    def get_neighbors(self, node: str) -> list[tuple[str, float]]:
        return self._adjacency.get(node, [])

    def get_out_degree(self, node: str) -> int:
        return len(self._adjacency.get(node, []))

    def get_in_degree(self, node: str) -> int:
        if self._directed:
            return sum(1 for adj in self._adjacency.values() for target, _ in adj if target == node)
        return self.get_out_degree(node)

    def get_all_edges(self) -> list[GraphEdge]:
        return self._edges

    def subgraph(self, nodes: set[str]) -> AdjacencyListGraph:
        sub = AdjacencyListGraph(self._directed)
        for node in nodes:
            sub.add_node(node)
        for edge in self._edges:
            if edge.source in nodes and edge.target in nodes:
                sub.add_edge(edge.source, edge.target, edge.weight)
        return sub


# ---------------------------------------------------------------------------
# PageRank
# ---------------------------------------------------------------------------

class PageRank:
    """PageRank implementation with configurable damping factor."""

    def __init__(self, damping: float = 0.85, tolerance: float = 1e-6,
                 max_iterations: int = 100) -> None:
        self._damping = damping
        self._tolerance = tolerance
        self._max_iterations = max_iterations

    def compute(self, graph: AdjacencyListGraph) -> PageRankResult:
        nodes = graph.node_count
        if nodes == 0:
            return PageRankResult({}, 0, True)

        scores = {node: 1.0 / nodes for node in graph.nodes}
        converged = False
        iteration = 0

        for iteration in range(1, self._max_iterations + 1):
            new_scores: dict[str, float] = {}
            dangling_sum = sum(
                scores[node] for node in graph.nodes
                if graph.get_out_degree(node) == 0
            )

            for node in graph.nodes:
                link_contribution = 0.0
                for neighbor, _ in graph.get_neighbors(node):
                    out_degree = graph.get_out_degree(neighbor)
                    if out_degree > 0:
                        link_contribution += scores[neighbor] / out_degree

                new_scores[node] = (
                    (1 - self._damping) / nodes
                    + self._damping * (link_contribution + dangling_sum / nodes)
                )

            diff = sum(abs(new_scores[n] - scores[n]) for n in graph.nodes)
            scores = new_scores

            if diff < self._tolerance:
                converged = True
                break

        return PageRankResult(scores=scores, iterations=iteration, converged=converged)

    def personalized_pr(self, graph: AdjacencyListGraph, seeds: dict[str, float],
                        max_iterations: int = 50) -> PageRankResult:
        nodes = graph.node_count
        if nodes == 0:
            return PageRankResult({}, 0, True)

        scores = {node: seeds.get(node, 0.0) for node in graph.nodes}
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}

        for iteration in range(1, max_iterations + 1):
            new_scores: dict[str, float] = {}
            for node in graph.nodes:
                link_contribution = 0.0
                for neighbor, _ in graph.get_neighbors(node):
                    out_degree = graph.get_out_degree(neighbor)
                    if out_degree > 0:
                        link_contribution += scores[neighbor] / out_degree
                teleport = seeds.get(node, 0.0)
                new_scores[node] = (1 - self._damping) * teleport + self._damping * link_contribution
            diff = sum(abs(new_scores[n] - scores[n]) for n in graph.nodes)
            scores = new_scores
            if diff < self._tolerance:
                return PageRankResult(scores=scores, iterations=iteration, converged=True)

        return PageRankResult(scores=scores, iterations=max_iterations, converged=False)


# ---------------------------------------------------------------------------
# Louvain Community Detection
# ---------------------------------------------------------------------------

class LouvainCommunity:
    """Louvain modularity optimization for community detection."""

    def __init__(self, resolution: float = 1.0) -> None:
        self._resolution = resolution

    def detect(self, graph: AdjacencyListGraph) -> CommunityResult:
        node_to_community = {node: i for i, node in enumerate(graph.nodes)}
        total_weight = sum(e.weight for e in graph.get_all_edges())
        if total_weight == 0:
            return CommunityResult(node_to_community, 0.0, graph.node_count)

        degree_sum = defaultdict(float)
        for edge in graph.get_all_edges():
            degree_sum[edge.source] += edge.weight
            degree_sum[edge.target] += edge.weight

        internal_weights = defaultdict(float)
        for edge in graph.get_all_edges():
            if node_to_community[edge.source] == node_to_community[edge.target]:
                internal_weights[node_to_community[edge.source]] += edge.weight

        community_total = defaultdict(float)
        for node in graph.nodes:
            cid = node_to_community[node]
            community_total[cid] += degree_sum[node]

        improved = True
        while improved:
            improved = False
            for node in graph.nodes:
                current_community = node_to_community[node]
                best_community = current_community
                best_gain = 0.0

                neighbor_communities: dict[int, float] = defaultdict(float)
                for neighbor, weight in graph.get_neighbors(node):
                    nc = node_to_community[neighbor]
                    neighbor_communities[nc] += weight

                node_degree = degree_sum[node]

                for neighbor_comm, edge_weight_to_comm in neighbor_communities.items():
                    if neighbor_comm == current_community:
                        continue

                    gain = (
                        edge_weight_to_comm / total_weight
                        - self._resolution * node_degree * community_total[neighbor_comm] / (2 * total_weight * total_weight)
                    )
                    if gain > best_gain:
                        best_gain = gain
                        best_community = neighbor_comm

                if best_community != current_community:
                    internal_weights[current_community] -= (
                        internal_weights.get(current_community, 0) * node_degree / community_total[current_community]
                    )
                    community_total[current_community] -= node_degree
                    node_to_community[node] = best_community
                    community_total[best_community] += node_degree
                    improved = True

        unique_communities = {v: i for i, v in enumerate(set(node_to_community.values()))}
        node_to_community = {k: unique_communities[v] for k, v in node_to_community.items()}

        modularity = self._compute_modularity(graph, node_to_community, total_weight)
        return CommunityResult(
            communities=node_to_community,
            modularity=modularity,
            num_communities=len(unique_communities),
        )

    def _compute_modularity(self, graph: AdjacencyListGraph,
                            communities: dict[str, int], total_weight: float) -> float:
        if total_weight == 0:
            return 0.0
        q = 0.0
        for edge in graph.get_all_edges():
            if communities[edge.source] == communities[edge.target]:
                q += edge.weight
        q = q / total_weight
        q -= self._resolution * sum(
            (sum(e.weight for e in graph.get_all_edges() if e.source == n or e.target == n) / (2 * total_weight)) ** 2
            for n in graph.nodes
        )
        return q


# ---------------------------------------------------------------------------
# Shortest Path Algorithms
# ---------------------------------------------------------------------------

class Dijkstra:
    """Single-source shortest paths with non-negative weights."""

    def compute(self, graph: AdjacencyListGraph, source: str) -> ShortestPathResult:
        distances = {node: float("inf") for node in graph.nodes}
        predecessors: dict[str, Optional[str]] = {node: None for node in graph.nodes}
        distances[source] = 0
        heap: list[tuple[float, str]] = [(0, source)]
        visited: set[str] = set()

        while heap:
            dist, node = heapq.heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            for neighbor, weight in graph.get_neighbors(node):
                if weight < 0:
                    raise ValueError("Dijkstra does not support negative weights")
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = node
                    heapq.heappush(heap, (new_dist, neighbor))

        return ShortestPathResult(source=source, distances=distances, predecessors=predecessors)


class BellmanFord:
    """Single-source shortest paths handling negative weights."""

    def compute(self, graph: AdjacencyListGraph, source: str) -> ShortestPathResult:
        distances = {node: float("inf") for node in graph.nodes}
        predecessors: dict[str, Optional[str]] = {node: None for node in graph.nodes}
        distances[source] = 0

        edges = graph.get_all_edges()
        n = graph.node_count

        for _ in range(n - 1):
            updated = False
            for edge in edges:
                if distances[edge.source] + edge.weight < distances[edge.target]:
                    distances[edge.target] = distances[edge.source] + edge.weight
                    predecessors[edge.target] = edge.source
                    updated = True
            if not updated:
                break

        has_negative_cycle = False
        for edge in edges:
            if distances[edge.source] + edge.weight < distances[edge.target]:
                has_negative_cycle = True
                break

        return ShortestPathResult(
            source=source, distances=distances,
            predecessors=predecessors, has_negative_cycle=has_negative_cycle,
        )


class FloydWarshall:
    """All-pairs shortest paths."""

    def compute(self, graph: AdjacencyListGraph) -> dict[str, ShortestPathResult]:
        nodes = graph.nodes
        n = len(nodes)
        idx = {node: i for i, node in enumerate(nodes)}
        dist = [[float("inf")] * n for _ in range(n)]
        next_node = [[None] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0

        for edge in graph.get_all_edges():
            i, j = idx[edge.source], idx[edge.target]
            dist[i][j] = edge.weight
            next_node[i][j] = edge.target

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

        results: dict[str, ShortestPathResult] = {}
        for source in nodes:
            distances = {node: dist[idx[source]][idx[node]] for node in nodes}
            predecessors: dict[str, Optional[str]] = {}
            for target in nodes:
                if target == source:
                    predecessors[target] = None
                elif next_node[idx[source]][idx[target]] is not None:
                    predecessors[target] = source
                else:
                    predecessors[target] = None
            results[source] = ShortestPathResult(source=source, distances=distances, predecessors=predecessors)
        return results


# ---------------------------------------------------------------------------
# Centrality Measures
# ---------------------------------------------------------------------------

class CentralityCalculator:
    """Degree, betweenness, closeness, and eigenvector centrality."""

    def __init__(self, graph: AdjacencyListGraph) -> None:
        self._graph = graph

    def degree_centrality(self) -> dict[str, float]:
        n = self._graph.node_count - 1
        if n == 0:
            return {}
        return {node: self._graph.get_out_degree(node) / n for node in self._graph.nodes}

    def betweenness_centrality(self, sample_size: int = 0) -> dict[str, float]:
        betweenness = defaultdict(float)
        nodes = self._graph.nodes
        sample = nodes
        if 0 < sample_size < len(nodes):
            sample = random.sample(nodes, sample_size)

        for source in sample:
            stack: list[str] = []
            predecessors: dict[str, list[str]] = defaultdict(list)
            sigma = {n: 0.0 for n in nodes}
            sigma[source] = 1.0
            distance = {n: -1 for n in nodes}
            distance[source] = 0
            queue = deque([source])

            while queue:
                v = queue.popleft()
                stack.append(v)
                for w, _ in self._graph.get_neighbors(v):
                    if distance[w] < 0:
                        distance[w] = distance[v] + 1
                        queue.append(w)
                    if distance[w] == distance[v] + 1:
                        sigma[w] += sigma[v]
                        predecessors[w].append(v)

            delta = {n: 0.0 for n in nodes}
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != source:
                    betweenness[w] += delta[w]

        n = self._graph.node_count
        norm = 1.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
        return {k: v * norm for k, v in betweenness.items()}

    def closeness_centrality(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for source in self._graph.nodes:
            dist: dict[str, int] = {source: 0}
            queue = deque([source])
            while queue:
                current = queue.popleft()
                for neighbor, _ in self._graph.get_neighbors(current):
                    if neighbor not in dist:
                        dist[neighbor] = dist[current] + 1
                        queue.append(neighbor)
            total_dist = sum(dist.values())
            n = self._graph.node_count - 1
            result[source] = n / total_dist if total_dist > 0 else 0.0
        return result

    def eigenvector_centrality(self, iterations: int = 100, tolerance: float = 1e-6) -> dict[str, float]:
        nodes = self._graph.nodes
        n = len(nodes)
        scores = {node: 1.0 / n for node in nodes}

        for _ in range(iterations):
            new_scores: dict[str, float] = defaultdict(float)
            for node in nodes:
                for neighbor, _ in self._graph.get_neighbors(node):
                    new_scores[node] += scores[neighbor]
            norm = math.sqrt(sum(v ** 2 for v in new_scores.values()))
            if norm > 0:
                new_scores = {k: v / norm for k, v in new_scores.items()}
            if sum(abs(new_scores[nid] - scores[nid]) for nid in nodes) < tolerance:
                scores = new_scores
                break
            scores = new_scores
        return scores


# ---------------------------------------------------------------------------
# Graph Coloring
# ---------------------------------------------------------------------------

class GraphColorer:
    """Greedy and Welsh-Powell graph coloring algorithms."""

    def __init__(self, graph: AdjacencyListGraph) -> None:
        self._graph = graph

    def greedy_coloring(self) -> ColoringResult:
        colors: dict[str, int] = {}
        for node in self._graph.nodes:
            neighbor_colors = {colors[n] for n, _ in self._graph.get_neighbors(node) if n in colors}
            color = 0
            while color in neighbor_colors:
                color += 1
            colors[node] = color
        is_valid = self._validate(colors)
        return ColoringResult(colors=colors, num_colors=max(colors.values()) + 1 if colors else 0, is_valid=is_valid)

    def welsh_powell(self) -> ColoringResult:
        sorted_nodes = sorted(self._graph.nodes, key=lambda n: self._graph.get_out_degree(n), reverse=True)
        colors: dict[str, int] = {}
        for node in sorted_nodes:
            neighbor_colors = {colors[n] for n, _ in self._graph.get_neighbors(node) if n in colors}
            color = 0
            while color in neighbor_colors:
                color += 1
            colors[node] = color
        is_valid = self._validate(colors)
        return ColoringResult(colors=colors, num_colors=max(colors.values()) + 1 if colors else 0, is_valid=is_valid)

    def _validate(self, colors: dict[str, int]) -> bool:
        for node in self._graph.nodes:
            for neighbor, _ in self._graph.get_neighbors(node):
                if colors.get(node) == colors.get(neighbor):
                    return False
        return True


# ---------------------------------------------------------------------------
# BFS and DFS
# ---------------------------------------------------------------------------

class GraphTraversal:
    """BFS and DFS traversal with cycle detection and topological sorting."""

    def __init__(self, graph: AdjacencyListGraph) -> None:
        self._graph = graph

    def bfs(self, source: str) -> list[str]:
        visited: set[str] = {source}
        queue = deque([source])
        order: list[str] = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor, _ in self._graph.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, source: Optional[str] = None) -> DFSResult:
        state = {node: TraversalState.UNVISITED for node in self._graph.nodes}
        discovery: list[str] = []
        finish: list[str] = []
        tree_edges: list[tuple[str, str]] = []
        back_edges: list[tuple[str, str]] = []
        has_cycle = False
        time_counter = [0]

        def visit(node: str) -> None:
            state[node] = TraversalState.VISITING
            discovery.append(node)
            time_counter[0] += 1
            for neighbor, _ in self._graph.get_neighbors(node):
                if state[neighbor] == TraversalState.UNVISITED:
                    tree_edges.append((node, neighbor))
                    visit(neighbor)
                elif state[neighbor] == TraversalState.VISITING:
                    back_edges.append((node, neighbor))
                    has_cycle = True
            state[node] = TraversalState.VISITED
            finish.append(node)

        if source:
            if source in state and state[source] == TraversalState.UNVISITED:
                visit(source)
        else:
            for node in self._graph.nodes:
                if state[node] == TraversalState.UNVISITED:
                    visit(node)

        topo_order = list(reversed(finish)) if not has_cycle else None

        return DFSResult(
            discovery_order=discovery, finish_order=finish,
            tree_edges=tree_edges, back_edges=back_edges,
            has_cycle=has_cycle, topological_order=topo_order,
        )


# ---------------------------------------------------------------------------
# Minimum Spanning Tree
# ---------------------------------------------------------------------------

class UnionFind:
    """Disjoint set with path compression and union by rank."""

    def __init__(self, elements: list[str]) -> None:
        self._parent = {e: e for e in elements}
        self._rank = {e: 0 for e in elements}

    def find(self, x: str) -> str:
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x: str, y: str) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        return True


class MSTFinder:
    """Kruskal and Prim minimum spanning tree algorithms."""

    def __init__(self, graph: AdjacencyListGraph) -> None:
        self._graph = graph

    def kruskal(self) -> MSTResult:
        edges = sorted(self._graph.get_all_edges(), key=lambda e: e.weight)
        uf = UnionFind(self._graph.nodes)
        mst_edges: list[GraphEdge] = []

        for edge in edges:
            if uf.union(edge.source, edge.target):
                mst_edges.append(edge)
                if len(mst_edges) == self._graph.node_count - 1:
                    break

        total = sum(e.weight for e in mst_edges)
        return MSTResult(edges=mst_edges, total_weight=total)

    def prim(self, start: Optional[str] = None) -> MSTResult:
        if not self._graph.nodes:
            return MSTResult([], 0.0)
        source = start or self._graph.nodes[0]
        in_mst: set[str] = {source}
        mst_edges: list[GraphEdge] = []
        heap: list[tuple[float, str, str]] = []

        for neighbor, weight in self._graph.get_neighbors(source):
            heapq.heappush(heap, (weight, source, neighbor))

        while heap and len(in_mst) < self._graph.node_count:
            weight, src, node = heapq.heappop(heap)
            if node in in_mst:
                continue
            in_mst.add(node)
            mst_edges.append(GraphEdge(src, node, weight))
            for neighbor, w in self._graph.get_neighbors(node):
                if neighbor not in in_mst:
                    heapq.heappush(heap, (w, node, neighbor))

        total = sum(e.weight for e in mst_edges)
        return MSTResult(edges=mst_edges, total_weight=total)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("GRAPH ALGORITHMS TOOLKIT DEMO")
    print("=" * 70)

    # Build sample graph
    graph = AdjacencyListGraph(directed=True)
    for node in ["A", "B", "C", "D", "E", "F", "G"]:
        graph.add_node(node)
    graph.add_edge("A", "B", 1.0)
    graph.add_edge("A", "C", 4.0)
    graph.add_edge("B", "C", 2.0)
    graph.add_edge("B", "D", 6.0)
    graph.add_edge("C", "D", 3.0)
    graph.add_edge("D", "E", 1.0)
    graph.add_edge("E", "F", 2.0)
    graph.add_edge("F", "G", 1.0)
    graph.add_edge("B", "E", 10.0)
    graph.add_edge("G", "A", 3.0)

    # PageRank
    print("\n--- PageRank ---")
    pr = PageRank(damping=0.85, max_iterations=50)
    pr_result = pr.compute(graph)
    print(f"  Iterations: {pr_result.iterations}, Converged: {pr_result.converged}")
    for node, score in pr_result.top_nodes(5):
        print(f"    {node}: {score:.4f}")

    # Louvain Community Detection
    print("\n--- Louvain Community Detection ---")
    undirected = AdjacencyListGraph(directed=False)
    for edge in graph.get_all_edges():
        undirected.add_edge(edge.source, edge.target, edge.weight)
    louvain = LouvainCommunity(resolution=1.0)
    comm_result = louvain.detect(undirected)
    print(f"  Communities: {comm_result.num_communities}, Modularity: {comm_result.modularity:.4f}")
    for cid in range(comm_result.num_communities):
        members = comm_result.get_community_members(cid)
        print(f"    Community {cid}: {members}")

    # Shortest Path
    print("\n--- Shortest Path ---")
    dijkstra = Dijkstra()
    d_result = dijkstra.compute(graph, "A")
    print(f"  Dijkstra from A:")
    for node in ["A", "B", "C", "D", "E", "F", "G"]:
        path = d_result.path_to(node)
        dist = d_result.distance_to(node)
        print(f"    A->{node}: dist={dist}, path={' -> '.join(path)}")

    bellman = BellmanFord()
    bf_result = bellman.compute(graph, "A")
    print(f"  Bellman-Ford from A (D->E): dist={bf_result.distance_to('E')}")

    fw = FloydWarshall()
    fw_results = fw.compute(graph)
    print(f"  Floyd-Warshall A->G: {fw_results['A'].distance_to('G')}")

    # Centrality
    print("\n--- Centrality Measures ---")
    cent = CentralityCalculator(graph)
    degree = cent.degree_centrality()
    print("  Degree centrality:")
    for node, score in sorted(degree.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {node}: {score:.4f}")

    betweenness = cent.betweenness_centrality()
    print("  Betweenness centrality:")
    for node, score in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {node}: {score:.4f}")

    closeness = cent.closeness_centrality()
    print("  Closeness centrality:")
    for node, score in sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {node}: {score:.4f}")

    eigen = cent.eigenvector_centrality()
    print("  Eigenvector centrality:")
    for node, score in sorted(eigen.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {node}: {score:.4f}")

    # Graph Coloring
    print("\n--- Graph Coloring ---")
    colorer = GraphColorer(undirected)
    greedy = colorer.greedy_coloring()
    print(f"  Greedy: {greedy.num_colors} colors, valid={greedy.is_valid}")
    wp = colorer.welsh_powell()
    print(f"  Welsh-Powell: {wp.num_colors} colors, valid={wp.is_valid}")
    print(f"  Colors: {greedy.colors}")

    # BFS and DFS
    print("\n--- BFS and DFS ---")
    trav = GraphTraversal(graph)
    bfs_order = trav.bfs("A")
    print(f"  BFS from A: {bfs_order}")

    dfs_result = trav.dfs("A")
    print(f"  DFS from A: {dfs_result.discovery_order}")
    print(f"  Has cycle: {dfs_result.has_cycle}")
    if dfs_result.topological_order:
        print(f"  Topological order: {dfs_result.topological_order}")

    # Minimum Spanning Tree
    print("\n--- Minimum Spanning Tree ---")
    mst_finder = MSTFinder(undirected)
    kruskal = mst_finder.kruskal()
    print(f"  Kruskal: {len(kruskal.edges)} edges, total weight={kruskal.total_weight}")
    for e in kruskal.edges:
        print(f"    {e.source}--{e.target} (w={e.weight})")

    prim = mst_finder.prim()
    print(f"  Prim: {len(prim.edges)} edges, total weight={prim.total_weight}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")


if __name__ == "__main__":
    main()
