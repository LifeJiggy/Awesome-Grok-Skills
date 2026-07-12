"""
Social Network Analysis Toolkit

Graph-based social network analysis: centrality computation, community detection,
influence metrics, clustering coefficients, and structural analysis.
"""

from __future__ import annotations

import math
import random
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import defaultdict, deque
from itertools import combinations

logger = __import__("logging").getLogger(__name__)


# ---------------------------------------------------------------------------
# Domain Enums
# ---------------------------------------------------------------------------

class CentralityType(Enum):
    DEGREE = auto()
    BETWEENNESS = auto()
    CLOSENESS = auto()
    EIGENVECTOR = auto()
    KATZ = auto()


class CommunityAlgorithm(Enum):
    LOUVAIN = auto()
    LABEL_PROPAGATION = auto()
    GIRVAN_NEWMAN = auto()
    CONNECTED_COMPONENTS = auto()


class InfluenceModel(Enum):
    INDEPENDENT_CASCADE = auto()
    LINEAR_THRESHOLD = auto()


class NetworkProperty(Enum):
    DENSITY = auto()
    CLUSTERING_COEFFICIENT = auto()
    ASSORTATIVITY = auto()
    TRANSITIVITY = auto()
    RECIPROCITY = auto()


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SocialNode:
    id: str
    label: str = ""
    properties: dict[str, Any] = field(default_factory=dict)
    centrality_scores: dict[str, float] = field(default_factory=dict)
    community: int = -1
    degree: int = 0

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SocialNode) and self.id == other.id


@dataclass
class SocialEdge:
    source: str
    target: str
    weight: float = 1.0
    label: str = ""
    properties: dict[str, Any] = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash((self.source, self.target, self.label))


@dataclass
class Community:
    id: int
    nodes: set[str] = field(default_factory=set)
    internal_edges: int = 0
    external_edges: int = 0

    @property
    def size(self) -> int:
        return len(self.nodes)

    @property
    def density(self) -> int:
        possible = self.size * (self.size - 1)
        return self.internal_edges * 2 // possible if possible > 0 else 0


@dataclass
class CentralityResult:
    node_id: str
    centrality_type: CentralityType
    score: float
    rank: int = 0


@dataclass
class InfluenceResult:
    seed_nodes: list[str]
    total_reached: int
    spread_ratio: float
    rounds: int = 0


@dataclass
class NetworkMetrics:
    num_nodes: int
    num_edges: int
    density: float
    avg_degree: float
    clustering_coefficient: float
    avg_path_length: float = 0.0
    diameter: int = 0
    num_communities: int = 0


# ---------------------------------------------------------------------------
# Social Network Graph
# ---------------------------------------------------------------------------

class SocialNetworkGraph:
    """Undirected social graph with adjacency list representation."""

    def __init__(self, directed: bool = False) -> None:
        self._nodes: dict[str, SocialNode] = {}
        self._adjacency: dict[str, set[str]] = defaultdict(set)
        self._edge_weights: dict[tuple[str, str], float] = {}
        self._directed = directed
        self._edges: list[SocialEdge] = []

    @property
    def nodes(self) -> list[SocialNode]:
        return list(self._nodes.values())

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        if self._directed:
            return len(self._edges)
        return len(self._edges) // 2

    def add_node(self, node: SocialNode) -> None:
        self._nodes[node.id] = node

    def add_edge(self, edge: SocialEdge) -> None:
        self._nodes[edge.source].degree += 1
        self._nodes[edge.target].degree += 1
        self._adjacency[edge.source].add(edge.target)
        self._adjacency[edge.target].add(edge.source)
        self._edge_weights[(edge.source, edge.target)] = edge.weight
        self._edge_weights[(edge.target, edge.source)] = edge.weight
        self._edges.append(edge)

    def get_neighbors(self, node_id: str) -> set[str]:
        return self._adjacency.get(node_id, set())

    def get_weight(self, source: str, target: str) -> float:
        return self._edge_weights.get((source, target), 0.0)

    def get_node(self, node_id: str) -> Optional[SocialNode]:
        return self._nodes.get(node_id)

    def get_common_neighbors(self, node_a: str, node_b: str) -> set[str]:
        return self._adjacency.get(node_a, set()) & self._adjacency.get(node_b, set())


# ---------------------------------------------------------------------------
# Centrality Calculator
# ---------------------------------------------------------------------------

class CentralityCalculator:
    """Computes various centrality measures on social graphs."""

    def __init__(self, graph: SocialNetworkGraph) -> None:
        self._graph = graph

    def degree_centrality(self) -> list[CentralityResult]:
        n = self._graph.node_count - 1
        if n == 0:
            return []
        results = []
        for node in self._graph.nodes:
            score = node.degree / n
            results.append(CentralityResult(node.id, CentralityType.DEGREE, score))
        results.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(results):
            r.rank = i + 1
        return results

    def betweenness_centrality(self, sample_size: int = 0) -> list[CentralityResult]:
        betweenness: dict[str, float] = defaultdict(float)
        nodes = self._graph.nodes
        sample = nodes
        if sample_size > 0 and sample_size < len(nodes):
            sample = random.sample(nodes, sample_size)

        for source in sample:
            stack: list[str] = []
            predecessors: dict[str, list[str]] = defaultdict(list)
            sigma: dict[str, float] = {n.id: 0 for n in nodes}
            sigma[source.id] = 1
            distance: dict[str, int] = {n.id: -1 for n in nodes}
            distance[source.id] = 0
            queue = deque([source.id])

            while queue:
                v = queue.popleft()
                stack.append(v)
                for w in self._graph.get_neighbors(v):
                    if distance[w] < 0:
                        distance[w] = distance[v] + 1
                        queue.append(w)
                    if distance[w] == distance[v] + 1:
                        sigma[w] += sigma[v]
                        predecessors[w].append(v)

            delta: dict[str, float] = {n.id: 0 for n in nodes}
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != source.id:
                    betweenness[w] += delta[w]

        n = self._graph.node_count
        norm = 1.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
        results = []
        for node in self._graph.nodes:
            results.append(CentralityResult(node.id, CentralityType.BETWEENNESS, betweenness[node.id] * norm))
        results.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(results):
            r.rank = i + 1
        return results

    def closeness_centrality(self) -> list[CentralityResult]:
        results: list[CentralityResult] = []
        for source in self._graph.nodes:
            dist: dict[str, int] = {source.id: 0}
            queue = deque([source.id])
            while queue:
                current = queue.popleft()
                for neighbor in self._graph.get_neighbors(current):
                    if neighbor not in dist:
                        dist[neighbor] = dist[current] + 1
                        queue.append(neighbor)
            total_dist = sum(dist.values())
            n = self._graph.node_count - 1
            score = n / total_dist if total_dist > 0 else 0.0
            results.append(CentralityResult(source.id, CentralityType.CLOSENESS, score))
        results.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(results):
            r.rank = i + 1
        return results

    def eigenvector_centrality(self, iterations: int = 100, tolerance: float = 1e-6) -> list[CentralityResult]:
        nodes = [n.id for n in self._graph.nodes]
        n = len(nodes)
        scores: dict[str, float] = {nid: 1.0 / n for nid in nodes}

        for _ in range(iterations):
            new_scores: dict[str, float] = defaultdict(float)
            for node_id in nodes:
                for neighbor in self._graph.get_neighbors(node_id):
                    new_scores[node_id] += scores[neighbor]
            norm = math.sqrt(sum(v ** 2 for v in new_scores.values()))
            if norm > 0:
                new_scores = {k: v / norm for k, v in new_scores.items()}
            diff = sum(abs(new_scores[nid] - scores[nid]) for nid in nodes)
            scores = new_scores
            if diff < tolerance:
                break

        results = [CentralityResult(nid, CentralityType.EIGENVECTOR, scores[nid]) for nid in nodes]
        results.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(results):
            r.rank = i + 1
        return results


# ---------------------------------------------------------------------------
# Community Detector
# ---------------------------------------------------------------------------

class CommunityDetector:
    """Detects communities using various algorithms."""

    def __init__(self, graph: SocialNetworkGraph) -> None:
        self._graph = graph

    def connected_components(self) -> list[Community]:
        visited: set[str] = set()
        communities: list[Community] = []
        community_id = 0

        for node in self._graph.nodes:
            if node.id not in visited:
                component = Community(id=community_id)
                queue = deque([node.id])
                while queue:
                    current = queue.popleft()
                    if current in visited:
                        continue
                    visited.add(current)
                    component.nodes.add(current)
                    for neighbor in self._graph.get_neighbors(current):
                        if neighbor not in visited:
                            queue.append(neighbor)
                            component.internal_edges += 1
                communities.append(component)
                community_id += 1
        return communities

    def label_propagation(self, max_iterations: int = 100) -> list[Community]:
        labels: dict[str, int] = {n.id: i for i, n in enumerate(self._graph.nodes)}

        for _ in range(max_iterations):
            changed = False
            nodes = list(self._graph.nodes)
            random.shuffle(nodes)
            for node in nodes:
                neighbor_labels: dict[int, int] = defaultdict(int)
                for neighbor in self._graph.get_neighbors(node.id):
                    neighbor_labels[labels[neighbor]] += 1
                if neighbor_labels:
                    best_label = max(neighbor_labels, key=neighbor_labels.get)  # type: ignore[arg-type]
                    if labels[node.id] != best_label:
                        labels[node.id] = best_label
                        changed = True
            if not changed:
                break

        community_map: dict[int, Community] = {}
        for nid, label in labels.items():
            if label not in community_map:
                community_map[label] = Community(id=label)
            community_map[label].nodes.add(nid)

        for community in community_map.values():
            for nid in community.nodes:
                for neighbor in self._graph.get_neighbors(nid):
                    if neighbor in community.nodes:
                        community.internal_edges += 1
            community.internal_edges //= 2

        return list(community_map.values())

    def modularity(self, communities: list[Community]) -> float:
        m = self._graph.edge_count
        if m == 0:
            return 0.0
        q = 0.0
        node_community: dict[str, int] = {}
        for comm in communities:
            for nid in comm.nodes:
                node_community[nid] = comm.id

        for comm in communities:
            for i in comm.nodes:
                for j in comm.nodes:
                    a_ij = 1.0 if j in self._graph.get_neighbors(i) else 0.0
                    k_i = self._graph.nodes_dict[i].degree if hasattr(self._graph, 'nodes_dict') else len(self._graph.get_neighbors(i))
                    k_j = self._graph.nodes_dict[j].degree if hasattr(self._graph, 'nodes_dict') else len(self._graph.get_neighbors(j))
                    if node_community.get(i) == node_community.get(j):
                        q += a_ij - (k_i * k_j) / (2 * m)
        return q / (2 * m)


# ---------------------------------------------------------------------------
# Influence Propagator
# ---------------------------------------------------------------------------

class InfluencePropagator:
    """Simulates influence propagation using cascade models."""

    def __init__(self, graph: SocialNetworkGraph) -> None:
        self._graph = graph

    def independent_cascade(self, seeds: list[str], probability: float = 0.1,
                            max_rounds: int = 10) -> InfluenceResult:
        active = set(seeds)
        frontier = set(seeds)
        rounds = 0

        for _ in range(max_rounds):
            new_active: set[str] = set()
            for node in frontier:
                for neighbor in self._graph.get_neighbors(node):
                    if neighbor not in active:
                        if random.random() < probability:
                            new_active.add(neighbor)
            if not new_active:
                break
            active |= new_active
            frontier = new_active
            rounds += 1

        total = self._graph.node_count
        return InfluenceResult(
            seed_nodes=seeds,
            total_reached=len(active),
            spread_ratio=len(active) / total if total > 0 else 0,
            rounds=rounds,
        )

    def linear_threshold(self, seeds: list[str],
                         threshold_map: Optional[dict[str, float]] = None) -> InfluenceResult:
        active = set(seeds)
        thresholds = threshold_map or {n.id: 0.5 for n in self._graph.nodes}

        changed = True
        rounds = 0
        while changed:
            changed = False
            new_active: set[str] = set()
            for node in self._graph.nodes:
                if node.id in active:
                    continue
                weight_sum = sum(
                    self._graph.get_weight(neighbor, node.id)
                    for neighbor in self._graph.get_neighbors(node.id)
                    if neighbor in active
                )
                if weight_sum >= thresholds.get(node.id, 0.5):
                    new_active.add(node.id)
                    changed = True
            active |= new_active
            rounds += 1

        total = self._graph.node_count
        return InfluenceResult(
            seed_nodes=seeds,
            total_reached=len(active),
            spread_ratio=len(active) / total if total > 0 else 0,
            rounds=rounds,
        )

    def greedy_seed_selection(self, k: int, probability: float = 0.1) -> list[str]:
        seeds: list[str] = []
        remaining = {n.id for n in self._graph.nodes}

        for _ in range(k):
            best_node = ""
            best_spread = -1
            for candidate in remaining:
                test_seeds = seeds + [candidate]
                result = self.independent_cascade(test_seeds, probability, max_rounds=5)
                if result.total_reached > best_spread:
                    best_spread = result.total_reached
                    best_node = candidate
            if best_node:
                seeds.append(best_node)
                remaining.discard(best_node)

        return seeds


# ---------------------------------------------------------------------------
# Network Metrics Calculator
# ---------------------------------------------------------------------------

class NetworkMetricsCalculator:
    """Computes graph-level network metrics."""

    def __init__(self, graph: SocialNetworkGraph) -> None:
        self._graph = graph

    def density(self) -> float:
        n = self._graph.node_count
        e = self._graph.edge_count
        possible = n * (n - 1)
        return 2 * e / possible if possible > 0 else 0.0

    def average_degree(self) -> float:
        n = self._graph.node_count
        if n == 0:
            return 0.0
        return sum(node.degree for node in self._graph.nodes) / n

    def clustering_coefficient(self) -> float:
        total = 0.0
        for node in self._graph.nodes:
            neighbors = self._graph.get_neighbors(node.id)
            k = len(neighbors)
            if k < 2:
                continue
            triangles = 0
            for n1, n2 in combinations(neighbors, 2):
                if n2 in self._graph.get_neighbors(n1):
                    triangles += 1
            total += 2 * triangles / (k * (k - 1))
        n = self._graph.node_count
        return total / n if n > 0 else 0.0

    def average_path_length(self, sample_size: int = 100) -> float:
        nodes = [n.id for n in self._graph.nodes]
        sample = random.sample(nodes, min(sample_size, len(nodes)))
        total_dist = 0
        count = 0

        for source in sample:
            dist: dict[str, int] = {source: 0}
            queue = deque([source])
            while queue:
                current = queue.popleft()
                for neighbor in self._graph.get_neighbors(current):
                    if neighbor not in dist:
                        dist[neighbor] = dist[current] + 1
                        queue.append(neighbor)
            for d in dist.values():
                if d > 0:
                    total_dist += d
                    count += 1

        return total_dist / count if count > 0 else 0.0

    def diameter(self) -> int:
        max_d = 0
        for node in self._graph.nodes[:min(50, len(self._graph.nodes))]:
            dist: dict[str, int] = {node.id: 0}
            queue = deque([node.id])
            while queue:
                current = queue.popleft()
                for neighbor in self._graph.get_neighbors(current):
                    if neighbor not in dist:
                        dist[neighbor] = dist[current] + 1
                        queue.append(neighbor)
            if dist:
                max_d = max(max_d, max(dist.values()))
        return max_d

    def compute_all(self, sample_size: int = 100) -> NetworkMetrics:
        return NetworkMetrics(
            num_nodes=self._graph.node_count,
            num_edges=self._graph.edge_count,
            density=self.density(),
            avg_degree=self.average_degree(),
            clustering_coefficient=self.clustering_coefficient(),
            avg_path_length=self.average_path_length(sample_size),
            diameter=self.diameter(),
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("SOCIAL NETWORK ANALYSIS TOOLKIT DEMO")
    print("=" * 70)

    # Build sample social graph
    graph = SocialNetworkGraph(directed=False)
    people = [
        SocialNode("alice", "Alice", {"age": 30}),
        SocialNode("bob", "Bob", {"age": 25}),
        SocialNode("carol", "Carol", {"age": 35}),
        SocialNode("dave", "Dave", {"age": 28}),
        SocialNode("eve", "Eve", {"age": 32}),
        SocialNode("frank", "Frank", {"age": 40}),
        SocialNode("grace", "Grace", {"age": 22}),
        SocialNode("hank", "Hank", {"age": 45}),
        SocialNode("ivy", "Ivy", {"age": 27}),
        SocialNode("jack", "Jack", {"age": 33}),
    ]
    for person in people:
        graph.add_node(person)

    edges = [
        SocialEdge("alice", "bob", 1.0),
        SocialEdge("alice", "carol", 1.0),
        SocialEdge("alice", "dave", 1.0),
        SocialEdge("bob", "carol", 1.0),
        SocialEdge("bob", "eve", 1.0),
        SocialEdge("carol", "frank", 1.0),
        SocialEdge("dave", "eve", 1.0),
        SocialEdge("dave", "grace", 1.0),
        SocialEdge("eve", "frank", 1.0),
        SocialEdge("frank", "hank", 1.0),
        SocialEdge("grace", "ivy", 1.0),
        SocialEdge("hank", "ivy", 1.0),
        SocialEdge("ivy", "jack", 1.0),
        SocialEdge("jack", "alice", 1.0),
        SocialEdge("eve", "grace", 1.0),
    ]
    for edge in edges:
        graph.add_edge(edge)

    # Centrality
    print("\n--- Centrality Measures ---")
    calc = CentralityCalculator(graph)
    degree_cent = calc.degree_centrality()
    print("  Degree centrality (top 5):")
    for r in degree_cent[:5]:
        print(f"    {r.node_id}: {r.score:.3f} (rank {r.rank})")

    betweenness = calc.betweenness_centrality()
    print("  Betweenness centrality (top 5):")
    for r in betweenness[:5]:
        print(f"    {r.node_id}: {r.score:.3f} (rank {r.rank})")

    closeness = calc.closeness_centrality()
    print("  Closeness centrality (top 5):")
    for r in closeness[:5]:
        print(f"    {r.node_id}: {r.score:.3f} (rank {r.rank})")

    eigenvector = calc.eigenvector_centrality(iterations=50)
    print("  Eigenvector centrality (top 5):")
    for r in eigenvector[:5]:
        print(f"    {r.node_id}: {r.score:.3f} (rank {r.rank})")

    # Community Detection
    print("\n--- Community Detection ---")
    detector = CommunityDetector(graph)
    components = detector.connected_components()
    print(f"  Connected components: {len(components)}")
    for c in components:
        print(f"    Component {c.id}: {c.nodes}")

    label_communities = detector.label_propagation(max_iterations=20)
    print(f"  Label propagation communities: {len(label_communities)}")
    for c in label_communities:
        print(f"    Community {c.id}: {c.nodes} (size={c.size})")

    # Influence Propagation
    print("\n--- Influence Propagation ---")
    influencer = InfluencePropagator(graph)
    ic_result = influencer.independent_cascade(["alice", "bob"], probability=0.3, max_rounds=5)
    print(f"  Independent Cascade: reached {ic_result.total_reached}/{graph.node_count} ({ic_result.spread_ratio:.1%}) in {ic_result.rounds} rounds")

    lt_result = influencer.linear_threshold(["alice"], threshold_map={n.id: 0.3 for n in graph.nodes})
    print(f"  Linear Threshold: reached {lt_result.total_reached}/{graph.node_count} ({lt_result.spread_ratio:.1%}) in {lt_result.rounds} rounds")

    seeds = influencer.greedy_seed_selection(k=3, probability=0.3)
    print(f"  Greedy seed selection (k=3): {seeds}")

    # Network Metrics
    print("\n--- Network Metrics ---")
    metrics_calc = NetworkMetricsCalculator(graph)
    metrics = metrics_calc.compute_all()
    print(f"  Nodes: {metrics.num_nodes}")
    print(f"  Edges: {metrics.num_edges}")
    print(f"  Density: {metrics.density:.4f}")
    print(f"  Average degree: {metrics.avg_degree:.2f}")
    print(f"  Clustering coefficient: {metrics.clustering_coefficient:.4f}")
    print(f"  Average path length: {metrics.avg_path_length:.2f}")
    print(f"  Diameter: {metrics.diameter}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")


if __name__ == "__main__":
    main()
