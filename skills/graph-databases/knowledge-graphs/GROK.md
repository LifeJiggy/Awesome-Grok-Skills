---
name: knowledge-graphs
category: graph-databases
version: 1.0.0
tags:
  - knowledge-graph
  - ontology
  - rdf
  - owl
  - entity-linking
  - graph-embeddings
difficulty: advanced
estimated_time: 55 minutes
prerequisites:
  - graph-theory-basics
  - semantic-web-basics
  - python-3.10+
---

# Knowledge Graphs

Design, build, and query knowledge graphs: ontology engineering with OWL/RDF, entity linking, graph embeddings, and reasoning over semantic networks.

## Ontology Design

Ontologies define the conceptual structure of a knowledge graph: classes, properties, relationships, and constraints. Good ontologies enable reasoning, data integration, and semantic interoperability.

### OWL (Web Ontology Language)

OWL is the W3C standard for representing rich ontologies. It supports description logic for formal reasoning over class hierarchies and property constraints.

```turtle
# Class hierarchy
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix schema: <http://schema.org/> .

# Person class with restrictions
schema:Person rdf:type owl:Class ;
    rdfs:subClassOf schema:Thing ;
    owl:equivalentClass [
        rdf:type owl:Class ;
        owl:intersectionOf (
            schema:Thing
            [ rdf:type owl:Restriction ;
              owl:onProperty schema:knows ;
              owl:minCardinality 0 ]
        )
    ] .

# Properties with domain and range
schema:knows rdf:type owl:ObjectProperty ;
    rdfs:domain schema:Person ;
    rdfs:range schema:Person ;
    owl:propertyChainAxiom ( schema:knows schema:knows ) ;
    rdfs:label "knows"@en .

schema:name rdf:type owl:DatatypeProperty ;
    rdfs:domain schema:Thing ;
    rdfs:range xsd:string ;
    owl:maxCardinality 1 .

schema:email rdf:type owl:DatatypeProperty ;
    rdfs:domain schema:Person ;
    rdfs:range xsd:string ;
    owl:cardinality 1 .
```

### RDF Triples

RDF represents knowledge as subject-predicate-object triples. Each triple is a statement about the world.

```turtle
# Instance data
_:alice rdf:type schema:Person ;
    schema:name "Alice Smith" ;
    schema:email "alice@example.com" ;
    schema:knows _:bob ;
    schema:knows _:carol ;
    schema:age 30 .

_:bob rdf:type schema:Person ;
    schema:name "Bob Jones" ;
    schema:knows _:carol ;
    schema:worksAt _:acme .

_:acme rdf:type schema:Organization ;
    schema:name "Acme Corp" ;
    schema:location "New York" .

_:carol rdf:type schema:Person ;
    schema:name "Carol Davis" ;
    schema:worksAt _:acme ;
    schema:knows _:alice .
```

### Property Graph vs RDF

| Aspect | Property Graph | RDF |
|--------|---------------|-----|
| Structure | Nodes + labeled edges + properties | Triples (subject, predicate, object) |
| Properties | On nodes and edges | On subjects |
| Schema | Optional, flexible | Optional but formal (OWL) |
| Reasoning | Limited | Full description logic |
| Tooling | Neo4j, JanusGraph, TigerGraph | Jena, Stardog, GraphDB |
| Use case | Application data, social graphs | Interoperability, linked data |

## Entity Linking

Connecting mentions in text to entities in the knowledge graph.

### Named Entity Recognition + Linking Pipeline

```python
# Entity linking workflow
class EntityLinker:
    def link(self, text: str) -> list[LinkedEntity]:
        mentions = self.ner_extract(text)
        candidates = self.candidate_generation(mentions)
        ranked = self.entity_ranking(candidates)
        return self.disambiguation(ranked)
```

### Disambiguation Strategies

1. **String matching**: Exact and fuzzy match against entity labels
2. **Context similarity**: Compare mention context with entity description
3. **Graph proximity**: Prefer entities connected to already-linked entities
4. **Type compatibility**: Filter candidates by expected entity type
5. **Popularity priors**: Weight popular entities higher in candidate ranking

### Entity Resolution Across Sources

```cypher
// Find potential duplicates in Neo4j
MATCH (a:Person), (b:Person)
WHERE a <> b
  AND a.name = b.name
  AND a.email = b.email
MERGE (a)-[:SAME_AS]->(b)

// Fuzzy matching with Levenshtein distance
MATCH (a:Person), (b:Person)
WHERE a <> b
  AND apoc.text.distance(toLower(a.name), toLower(b.name)) < 3
  AND abs(a.birthYear - b.birthYear) < 2
RETURN a.name, b.name, apoc.text.distance(a.name, b.name) AS dist
ORDER BY dist
```

## Graph Embeddings

Vector representations of graph structure for machine learning.

### TransE (Translation Embedding)

Learns embeddings where relationships are translations in vector space: h + r ≈ t for valid triples (head, relation, tail).

### Node2Vec

Random walk-based embeddings that capture both local (BFS-like) and global (DFS-like) graph structure. Produces node vectors compatible with downstream ML tasks.

### Graph Neural Networks (GNNs)

Message-passing neural networks that aggregate information from a node's neighborhood.

- **GCN (Graph Convolutional Network)**: Spectral convolution approximation
- **GraphSAGE**: Inductive embeddings via neighbor sampling
- **GAT (Graph Attention Network)**: Attention-weighted neighbor aggregation

### Embedding Applications

1. **Link prediction**: Predict missing edges using embedding similarity
2. **Node classification**: Classify nodes using embedding features
3. **Knowledge graph completion**: Predict missing triples
4. **Similarity search**: Find similar entities in embedding space
5. **Clustering**: Group entities by embedding proximity

## RDF Data Management

### SPARQL Endpoint Configuration

```turtle
# Stardog server configuration
@prefix sd: <http://www.w3.org/ns/sparql-service-description#> .

_:endpoint rdf:type sd:Service ;
    sd:endpoint <http://localhost:8080/sparql> ;
    sd:supportedLanguage sd:SPARQL11Query ;
    sd:feature sd:EmptyGraphs ;
    sd:defaultDataset [
        sd:namedGraph [
            sd:name <http://example.org/graph1> ;
            sd:graph [
                rdf:type sd:Graph ;
                sd:name <http://example.org/graph1>
            ]
        ]
    ] .
```

### RDF Serialization Formats

| Format | Extension | Human-readable | Streaming | Compression |
|--------|-----------|----------------|-----------|-------------|
| Turtle | .ttl | Yes | Yes | Moderate |
| N-Triples | .nt | Yes | Yes | Low |
| JSON-LD | .jsonld | Yes | Yes | High |
| RDF/XML | .rdf | Moderate | Yes | High |
| N3 | .n3 | Yes | Yes | Moderate |

### Data Validation with SHACL

```turtle
# Shapes for validating Person instances
@prefix sh: <http://www.w3.org/ns/shacl#> .

PersonShape rdf:type sh:NodeShape ;
    sh:targetClass schema:Person ;
    sh:property [
        sh:path schema:name ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
    ] ;
    sh:property [
        sh:path schema:email ;
        sh:datatype xsd:string ;
        sh:pattern "^[^@]+@[^@]+$" ;
        sh:minCount 1 ;
    ] ;
    sh:property [
        sh:path schema:age ;
        sh:datatype xsd:integer ;
        sh:minInclusive 0 ;
        sh:maxInclusive 150 ;
    ] .
```

## Knowledge Graph Construction

### Schema-First Approach

1. Define ontology (classes, properties, constraints)
2. Create validation shapes (SHACL/ShEx)
3. Design entity linking strategy
4. Build ETL pipeline with schema validation
5. Populate with instance data
6. Reason over populated graph for inference

### Schema-Last Approach (Bottom-Up)

1. Extract triples from raw data
2. Cluster extracted entities
3. Infer schema from entity clusters
4. Align inferred schema with existing ontologies
5. Refine and validate
6. Reason for consistency

## Query Optimization for Knowledge Graphs

1. **Materialize inferences**: Pre-compute OWL deductions for frequently used rules
2. **Partition by named graph**: Separate datasets for query scoping
3. **Property chains**: Define transitive properties for path-based queries
4. **Index subject/predicate/object**: Standard triple-store indexing for BGP patterns
5. **Cache popular subgraphs**: Materialize frequently accessed subgraphs

## Quality Assurance

### Consistency Checking

```cypher
// Find orphan nodes (no incoming or outgoing edges)
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n), count(n)

// Find type conflicts
MATCH (n:Person)-[:WORKS_AT]->(m)
WHERE NOT m:Organization
RETURN n.name, labels(m)

// Find missing required properties
MATCH (p:Person)
WHERE p.email IS NULL OR p.name IS NULL
RETURN p
```

### Completeness Metrics

- **Attribute completeness**: % of entities with each attribute
- **Relationship completeness**: % of expected relationships present
- **Class coverage**: % of ontology classes populated
- **Referential integrity**: % of links pointing to existing entities
