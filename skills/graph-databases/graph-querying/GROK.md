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
