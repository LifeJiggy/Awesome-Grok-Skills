"""
Graph Querying Toolkit

Multi-dialect query builder and executor for Cypher, Gremlin, and SPARQL.
Includes pattern matching, traversal planning, shortest path computation,
and cross-language query translation.
"""

from __future__ import annotations

import re
import time
import hashlib
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional, Callable
from abc import ABC, abstractmethod
from collections import defaultdict

logger = __import__("logging").getLogger(__name__)


# ---------------------------------------------------------------------------
# Domain Enums
# ---------------------------------------------------------------------------

class QueryDialect(Enum):
    CYPHER = "cypher"
    GREMLIN = "gremlin"
    SPARQL = "sparql"


class TraversalDirection(Enum):
    OUTGOING = auto()
    INCOMING = auto()
    BOTH = auto()

    def to_cypher(self) -> str:
        return {TraversalDirection.OUTGOING: "->", TraversalDirection.INCOMING: "<-", TraversalDirection.BOTH: "--"}[self]

    def to_gremlin(self) -> str:
        return {TraversalDirection.OUTGOING: "out", TraversalDirection.INCOMING: "in", TraversalDirection.BOTH: "both"}[self]

    def to_sparql(self) -> str:
        return {TraversalDirection.OUTGOING: "?predicate", TraversalDirection.INCOMING: "?predicate", TraversalDirection.BOTH: "?predicate"}[self]


class PathStrategy(Enum):
    SHORTEST_PATH = auto()
    ALL_SHORTEST_PATHS = auto()
    DIJKSTRA = auto()
    BFS = auto()
    DFS = auto()


class JoinType(Enum):
    INNER = auto()
    OPTIONAL = auto()
    UNION = auto()


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class NodePattern:
    variable: str
    label: str = ""
    properties: dict[str, Any] = field(default_factory=dict)

    def to_cypher(self) -> str:
        label_part = f":{self.label}" if self.label else ""
        props = ""
        if self.properties:
            items = ", ".join(f"{k}: {repr(v)}" for k, v in self.properties.items())
            props = f" {{{items}}}"
        return f"({self.variable}{label_part}{props})"

    def to_gremlin(self) -> str:
        parts = [f".hasLabel('{self.label}')"] if self.label else []
        for k, v in self.properties.items():
            parts.append(f".has('{k}', {repr(v)})")
        return "".join(parts)

    def to_sparql(self) -> str:
        parts = []
        if self.label:
            parts.append(f"?{self.variable} a <{self.label}>")
        for k, v in self.properties.items():
            parts.append(f"?{self.variable} <{k}> \"{v}\"")
        return " ; ".join(parts) if parts else f"?{self.variable}"


@dataclass
class EdgePattern:
    variable: str
    rel_type: str = ""
    direction: TraversalDirection = TraversalDirection.OUTGOING
    properties: dict[str, Any] = field(default_factory=dict)

    def to_cypher(self) -> str:
        type_part = f":{self.rel_type}" if self.rel_type else ""
        props = ""
        if self.properties:
            items = ", ".join(f"{k}: {repr(v)}" for k, v in self.properties.items())
            props = f" {{{items}}}"
        dir_arrow = self.direction.to_cypher()
        return f"-[{self.variable}{type_part}{props}]{dir_arrow}"

    def to_gremlin(self) -> str:
        method = self.direction.to_gremlin()
        if self.rel_type:
            return f".{method}('{self.rel_type}')"
        return f".{method}()"


@dataclass
class TraversalStep:
    operation: str
    arguments: dict[str, Any] = field(default_factory=dict)

    def to_cypher(self) -> str:
        if self.operation == "filter":
            prop = self.arguments.get("property", "")
            op = self.arguments.get("operator", "=")
            val = self.arguments.get("value")
            return f"WHERE {self.operation == 'filter' and f'n.{prop} {op} {repr(val)}' or ''}"
        if self.operation == "limit":
            return f"LIMIT {self.arguments.get('count', 10)}"
        if self.operation == "order":
            return f"ORDER BY n.{self.arguments.get('property', 'name')}"
        return ""

    def to_gremlin(self) -> str:
        if self.operation == "filter":
            prop = self.arguments.get("property", "")
            op = self.arguments.get("operator", "eq")
            val = self.arguments.get("value")
            gremlin_ops = {"=": "eq", ">": "gt", "<": "lt", ">=": "gte", "<=": "lte"}
            g_op = gremlin_ops.get(op, op)
            return f".has('{prop}', {g_op}({repr(val)}))"
        if self.operation == "limit":
            return f".limit({self.arguments.get('count', 10)})"
        if self.operation == "order":
            direction = self.arguments.get("direction", "incr")
            return f".order().by('{self.arguments.get('property', 'name')}', {direction})"
        return ""

    def to_sparql(self) -> str:
        if self.operation == "filter":
            prop = self.arguments.get("property", "")
            op = self.arguments.get("operator", "=")
            val = self.arguments.get("value")
            sparql_ops = {"=": "=", ">": ">", "<": "<", ">=": ">=", "<=": "<="}
            s_op = sparql_ops.get(op, op)
            return f"FILTER (?{prop} {s_op} \"{val}\")"
        if self.operation == "limit":
            return f"LIMIT {self.arguments.get('count', 10)}"
        if self.operation == "order":
            direction = self.arguments.get("direction", "ASC")
            return f"ORDER BY {direction}(?{self.arguments.get('property', 'name')})"
        return ""


@dataclass
class QueryResult:
    columns: list[str]
    rows: list[dict[str, Any]]
    execution_time_ms: float = 0
    dialect: QueryDialect = QueryDialect.CYPHER
    row_count: int = 0

    def __post_init__(self) -> None:
        self.row_count = len(self.rows)


@dataclass
class GraphPath:
    nodes: list[str]
    edges: list[str]
    total_cost: float = 0.0

    @property
    def length(self) -> int:
        return len(self.edges)


@dataclass
class QueryPlan:
    query_id: str
    dialect: QueryDialect
    estimated_cost: float
    steps: list[TraversalStep]
    uses_index: bool = False
    cacheable: bool = True


# ---------------------------------------------------------------------------
# Abstract Query Builder
# ---------------------------------------------------------------------------

class QueryBuilder(ABC):
    """Base class for dialect-specific query builders."""

    def __init__(self) -> None:
        self._node_patterns: list[NodePattern] = []
        self._edge_patterns: list[EdgePattern] = []
        self._steps: list[TraversalStep] = []
        self._return_vars: list[str] = []
        self._with_vars: list[str] = []

    @abstractmethod
    def build(self) -> str:
        ...

    def match(self, node: NodePattern) -> QueryBuilder:
        self._node_patterns.append(node)
        return self

    def traverse(self, edge: EdgePattern, target: NodePattern) -> QueryBuilder:
        self._edge_patterns.append(edge)
        self._node_patterns.append(target)
        return self

    def where(self, prop: str, op: str, value: Any) -> QueryBuilder:
        self._steps.append(TraversalStep("filter", {"property": prop, "operator": op, "value": value}))
        return self

    def order_by(self, prop: str, descending: bool = False) -> QueryBuilder:
        direction = "decr" if descending else "incr"
        self._steps.append(TraversalStep("order", {"property": prop, "direction": direction}))
        return self

    def limit(self, count: int) -> QueryBuilder:
        self._steps.append(TraversalStep("limit", {"count": count}))
        return self

    def returns(self, *vars: str) -> QueryBuilder:
        self._return_vars = list(vars)
        return self


# ---------------------------------------------------------------------------
# Cypher Builder
# ---------------------------------------------------------------------------

class CypherQueryBuilder(QueryBuilder):
    """Builds Cypher queries for Neo4j."""

    def build(self) -> str:
        parts: list[str] = []
        patterns: list[str] = []

        for i, node in enumerate(self._node_patterns):
            patterns.append(node.to_cypher())

        for i, edge in enumerate(self._edge_patterns):
            if i < len(self._node_patterns) - 1:
                src = self._node_patterns[i].variable
                tgt = self._node_patterns[i + 1].variable
                edge_str = edge.to_cypher()
                patterns.append(f"({src}){edge_str}({tgt})")

        if patterns:
            parts.append("MATCH " + ", ".join(patterns))

        for step in self._steps:
            clause = step.to_cypher()
            if clause:
                parts.append(clause)

        if self._return_vars:
            parts.append("RETURN " + ", ".join(self._return_vars))

        return "\n".join(parts)


# ---------------------------------------------------------------------------
# Gremlin Builder
# ---------------------------------------------------------------------------

class GremlinQueryBuilder(QueryBuilder):
    """Builds Gremlin traversals for Apache TinkerPop."""

    def build(self) -> str:
        parts: list[str] = ["g"]

        if self._node_patterns:
            first = self._node_patterns[0]
            parts.append(f".V(){first.to_gremlin()}")

        for i, edge in enumerate(self._edge_patterns):
            parts.append(edge.to_gremlin())
            if i + 1 < len(self._node_patterns):
                parts.append(self._node_patterns[i + 1].to_gremlin())

        for step in self._steps:
            clause = step.to_gremlin()
            if clause:
                parts.append(clause)

        if self._return_vars:
            parts.append(f".path().by('{self._return_vars[0]}')")

        return "".join(parts)


# ---------------------------------------------------------------------------
# SPARQL Builder
# ---------------------------------------------------------------------------

class SparqlQueryBuilder(QueryBuilder):
    """Builds SPARQL queries for RDF stores."""

    def __init__(self) -> None:
        super().__init__()
        self._prefixes: dict[str, str] = {}

    def prefix(self, name: str, uri: str) -> SparqlQueryBuilder:
        self._prefixes[name] = uri
        return self

    def build(self) -> str:
        parts: list[str] = []

        for name, uri in self._prefixes.items():
            parts.append(f"PREFIX {name}: <{uri}>")

        parts.append("SELECT " + " ".join(f"?{v}" for v in self._return_vars))

        parts.append("WHERE {")
        where_clauses: list[str] = []
        for node in self._node_patterns:
            where_clauses.append(f"    {node.to_sparql()} .")
        for step in self._steps:
            clause = step.to_sparql()
            if clause:
                where_clauses.append(f"    {clause}")
        parts.append("\n".join(where_clauses))
        parts.append("}")

        for step in self._steps:
            clause = step.to_sparql()
            if clause and "LIMIT" in clause.upper():
                parts.append(clause)
            elif clause and "ORDER" in clause.upper():
                parts.append(clause)

        return "\n".join(parts)


# ---------------------------------------------------------------------------
# Shortest Path Finder
# ---------------------------------------------------------------------------

class ShortestPathFinder:
    """Finds shortest paths in adjacency-list graph representations."""

    def __init__(self, directed: bool = True) -> None:
        self._adjacency: dict[str, list[tuple[str, float]]] = defaultdict(list)
        self._directed = directed

    def add_edge(self, source: str, target: str, weight: float = 1.0) -> None:
        self._adjacency[source].append((target, weight))
        if not self._directed:
            self._adjacency[target].append((source, weight))

    def dijkstra(self, start: str, end: str) -> Optional[GraphPath]:
        import heapq
        distances: dict[str, float] = defaultdict(lambda: float("inf"))
        predecessors: dict[str, Optional[str]] = defaultdict(lambda: None)
        distances[start] = 0
        heap: list[tuple[float, str]] = [(0, start)]
        visited: set[str] = set()

        while heap:
            dist, node = heapq.heappop(heap)
            if node in visited:
                continue
            visited.add(node)
            if node == end:
                break
            for neighbor, weight in self._adjacency[node]:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = node
                    heapq.heappush(heap, (new_dist, neighbor))

        if distances[end] == float("inf"):
            return None

        path_nodes: list[str] = []
        current: Optional[str] = end
        while current is not None:
            path_nodes.append(current)
            current = predecessors[current]
        path_nodes.reverse()
        return GraphPath(nodes=path_nodes, edges=[f"{path_nodes[i]}->{path_nodes[i+1]}" for i in range(len(path_nodes) - 1)], total_cost=distances[end])

    def bfs(self, start: str, end: str) -> Optional[GraphPath]:
        from collections import deque
        queue: deque[tuple[str, list[str]]] = deque([(start, [start])])
        visited: set[str] = {start}

        while queue:
            node, path = queue.popleft()
            if node == end:
                return GraphPath(nodes=path, edges=[f"{path[i]}->{path[i+1]}" for i in range(len(path) - 1)])
            for neighbor, _ in self._adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def all_shortest_paths(self, start: str, end: str) -> list[GraphPath]:
        from collections import deque
        queue: deque[tuple[str, list[str], float]] = deque([(start, [start], 0.0)])
        shortest_cost = float("inf")
        results: list[GraphPath] = []
        visited_costs: dict[str, float] = {start: 0}

        while queue:
            node, path, cost = queue.popleft()
            if cost > shortest_cost:
                continue
            if node == end:
                if cost < shortest_cost:
                    shortest_cost = cost
                    results = []
                results.append(GraphPath(nodes=path, edges=[f"{path[i]}->{path[i+1]}" for i in range(len(path) - 1)], total_cost=cost))
                continue
            for neighbor, weight in self._adjacency[node]:
                new_cost = cost + weight
                if new_cost <= shortest_cost and new_cost < visited_costs.get(neighbor, float("inf")):
                    visited_costs[neighbor] = new_cost
                    queue.append((neighbor, path + [neighbor], new_cost))
        return results


# ---------------------------------------------------------------------------
# Query Translator
# ---------------------------------------------------------------------------

class QueryTranslator:
    """Translates queries between Cypher, Gremlin, and SPARQL dialects."""

    def __init__(self) -> None:
        self._dialect = QueryDialect.CYPHER

    def translate_cypher_to_gremlin(self, cypher: str) -> str:
        result = cypher
        result = re.sub(r"MATCH\s+\((\w+):(\w+)\)", r"g.V().hasLabel('\2').as('\1')", result)
        result = re.sub(r"-\[:(\w+)\]->", r".out('\1')", result)
        result = re.sub(r"<-\[:(\w+)\]-", r".in('\1')", result)
        result = re.sub(r"WHERE\s+(\w+)\.(\w+)\s*=\s*'([^']+)'", r".has('\2', eq('\3'))", result)
        result = re.sub(r"LIMIT\s+(\d+)", r".limit(\1)", result)
        result = re.sub(r"RETURN\s+(.+)", r".path().by('\1')", result)
        return result

    def translate_cypher_to_sparql(self, cypher: str) -> str:
        lines = ["SELECT ?s WHERE {"]
        match = re.search(r"MATCH\s+\((\w+):(\w+)\)", cypher)
        if match:
            var, label = match.groups()
            lines.append(f"  ?{var} a <{label}> .")
        prop_match = re.search(r"WHERE\s+\w+\.(\w+)\s*=\s*'([^']+)'", cypher)
        if prop_match:
            prop, val = prop_match.groups()
            lines.append(f"  ?s <{prop}> \"{val}\" .")
        limit_match = re.search(r"LIMIT\s+(\d+)", cypher)
        if limit_match:
            lines.append(f"}} LIMIT {limit_match.group(1)}")
        else:
            lines.append("}")
        return "\n".join(lines)

    def translate_gremlin_to_cypher(self, gremlin: str) -> str:
        result = gremlin
        result = re.sub(r"g\.V\(\)\.hasLabel\('(\w+)'\)", r"MATCH (n:\1)", result)
        result = re.sub(r"\.out\('(\w+)'\)\.inV\(\)", r"-[:\1]->(m)", result)
        result = re.sub(r"\.has\('(\w+)', eq\('([^']+)'\)\)", r"WHERE n.\1 = '\2'", result)
        return result

    def translate(self, query: str, source: QueryDialect, target: QueryDialect) -> str:
        if source == target:
            return query
        if source == QueryDialect.CYPHER and target == QueryDialect.GREMLIN:
            return self.translate_cypher_to_gremlin(query)
        if source == QueryDialect.CYPHER and target == QueryDialect.SPARQL:
            return self.translate_cypher_to_sparql(query)
        if source == QueryDialect.GREMLIN and target == QueryDialect.CYPHER:
            return self.translate_gremlin_to_cypher(query)
        raise ValueError(f"Translation from {source.value} to {target.value} not implemented")


# ---------------------------------------------------------------------------
# Query Cache
# ---------------------------------------------------------------------------

class QueryCache:
    """LRU cache for query results with TTL support."""

    def __init__(self, max_size: int = 1000, ttl_seconds: float = 300.0) -> None:
        self._cache: dict[str, tuple[QueryResult, float]] = {}
        self._max_size = max_size
        self._ttl = ttl_seconds
        self._hits = 0
        self._misses = 0

    def _make_key(self, query: str, params: dict[str, Any]) -> str:
        raw = f"{query}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, query: str, params: Optional[dict[str, Any]] = None) -> Optional[QueryResult]:
        key = self._make_key(query, params or {})
        if key in self._cache:
            result, ts = self._cache[key]
            if time.time() - ts < self._ttl:
                self._hits += 1
                return result
            del self._cache[key]
        self._misses += 1
        return None

    def put(self, query: str, params: dict[str, Any], result: QueryResult) -> None:
        if len(self._cache) >= self._max_size:
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        key = self._make_key(query, params)
        self._cache[key] = (result, time.time())

    def clear(self) -> None:
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0


# Re-export json for QueryCache
import json as json


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("GRAPH QUERYING TOOLKIT DEMO")
    print("=" * 70)

    # --- Cypher Query Building ---
    print("\n--- Cypher Query Building ---")
    builder = CypherQueryBuilder()
    query = (
        builder
        .match(NodePattern("p", "Person", {"active": True}))
        .traverse(EdgePattern("r", "KNOWS"), NodePattern("f", "Person"))
        .where("p.age", ">", 25)
        .order_by("f.name")
        .limit(10)
        .returns("p.name", "f.name")
        .build()
    )
    print(f"  Query:\n{query}")

    # --- Gremlin Query Building ---
    print("\n--- Gremlin Query Building ---")
    gbuilder = GremlinQueryBuilder()
    gquery = (
        gbuilder
        .match(NodePattern("p", "Person"))
        .traverse(EdgePattern("r", "WORKS_AT"), NodePattern("c", "Company"))
        .where("p.age", ">", 30)
        .limit(5)
        .returns("p.name")
        .build()
    )
    print(f"  Query:\n{gquery}")

    # --- SPARQL Query Building ---
    print("\n--- SPARQL Query Building ---")
    sbuilder = SparqlQueryBuilder()
    squery = (
        sbuilder
        .prefix("schema", "http://schema.org/")
        .match(NodePattern("person", "http://schema.org/Person"))
        .where("age", ">", "25")
        .limit(10)
        .returns("person", "name")
        .build()
    )
    print(f"  Query:\n{squery}")

    # --- Shortest Path ---
    print("\n--- Shortest Path Finding ---")
    spf = ShortestPathFinder(directed=True)
    spf.add_edge("A", "B", 1.0)
    spf.add_edge("A", "C", 4.0)
    spf.add_edge("B", "C", 2.0)
    spf.add_edge("B", "D", 6.0)
    spf.add_edge("C", "D", 3.0)
    spf.add_edge("D", "E", 1.0)
    spf.add_edge("B", "E", 10.0)

    dijkstra_result = spf.dijkstra("A", "E")
    if dijkstra_result:
        print(f"  Dijkstra A->E: {' -> '.join(dijkstra_result.nodes)} (cost={dijkstra_result.total_cost})")

    bfs_result = spf.bfs("A", "E")
    if bfs_result:
        print(f"  BFS A->E: {' -> '.join(bfs_result.nodes)} (length={bfs_result.length})")

    all_paths = spf.all_shortest_paths("A", "D")
    for p in all_paths:
        print(f"  All shortest A->D: {' -> '.join(p.nodes)} (cost={p.total_cost})")

    # --- Query Translation ---
    print("\n--- Query Translation ---")
    translator = QueryTranslator()
    cypher_q = "MATCH (p:Person)-[:FRIEND]->(f:Person) WHERE p.age > 25 RETURN f.name LIMIT 10"
    gremlin_q = translator.translate(cypher_q, QueryDialect.CYPHER, QueryDialect.GREMLIN)
    sparql_q = translator.translate(cypher_q, QueryDialect.CYPHER, QueryDialect.SPARQL)
    print(f"  Cypher:   {cypher_q}")
    print(f"  Gremlin:  {gremlin_q}")
    print(f"  SPARQL:   {sparql_q}")

    # --- Query Cache ---
    print("\n--- Query Cache ---")
    cache = QueryCache(max_size=5, ttl_seconds=60)
    result = QueryResult(columns=["name"], rows=[{"name": "Alice"}], execution_time_ms=5.0)
    cache.put("MATCH (n:Person) RETURN n", {}, result)
    cached = cache.get("MATCH (n:Person) RETURN n")
    miss = cache.get("MATCH (n:Company) RETURN n")
    print(f"  Hit rate: {cache.hit_rate:.1%}")
    print(f"  Cached result rows: {cached.row_count if cached else 0}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")


if __name__ == "__main__":
    main()
