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

## Advanced Configuration

### RDF Store Configuration

```yaml
rdf_store:
  triplestore:
    type: "blazegraph"
    endpoint: "https://blazegraph.example.com/blazegraph"
    namespace: "kb"
    
  virtuoso:
    endpoint: "https://virtuoso.example.com/sparql"
    graph: "urn:graph:knowledge"
    
  fuseki:
    endpoint: "https://fuseki.example.com/dataset/query"
    dataset: "knowledge_graph"
    
  storage:
    persistent: true
    data_directory: "/data/rdf/"
    backup_enabled: true
    backup_frequency: "daily"
    
  query_limits:
    max_query_time_ms: 30000
    max_results_returned: 10000
    max_query_depth: 10
    
  loading:
    batch_size: 10000
    parallel_loaders: 4
    commit_each_batch: true
```

### Ontology Configuration

```yaml
ontology:
  base_uri: "https://example.com/ontology/"
  prefix:
    - "ex"
    - "schema"
    - "dcterms"
    
  classes:
    - name: "Person"
      parent: "schema:Thing"
      properties:
        - "schema:name"
        - "schema:email"
        - "schema:birthDate"
      restrictions:
        - property: "schema:name"
          type: "exactlyOne"
          value: "xsd:string"
          
    - name: "Organization"
      parent: "schema:Thing"
      properties:
        - "schema:name"
        - "schema:url"
        - "schema:location"
        
    - name: "Event"
      parent: "schema:Thing"
      properties:
        - "schema:name"
        - "schema:startDate"
        - "schema:location"
        
  object_properties:
    - name: "knows"
      domain: "Person"
      range: "Person"
      characteristics: ["symmetric"]
      
    - name: "worksAt"
      domain: "Person"
      range: "Organization"
      
    - name: "attendedBy"
      domain: "Event"
      range: "Person"
      
  data_properties:
    - name: "email"
      domain: "Person"
      range: "xsd:string"
      
    - name: "birthDate"
      domain: "Person"
      range: "xsd:date"
      
  reasoning:
    enabled: true
    reasoner: "hermit"
    inference_depth: 10
    materialize_inferences: false
```

### Entity Linking Configuration

```yaml
entity_linking:
  disambiguation:
    algorithm: "wikifier"
    confidence_threshold: 0.7
    max_candidates: 10
    
  named_entity_recognition:
    models:
      - name: "spacy"
        model: "en_core_web_trf"
        entities: ["PERSON", "ORG", "GPE", "DATE"]
        
      - name: "flair"
        model: "ner-english-large"
        
    ensemble_method: "voting"
    min_votes: 2
    
  entity_resolution:
    algorithm: "blocking"
    blocking_key: "name"
    similarity_threshold: 0.85
    max_comparison_pairs: 1000000
    
  linking_targets:
    wikidata:
      enabled: true
      api_endpoint: "https://www.wikidata.org/w/api.php"
      
    dbpedia:
      enabled: true
      api_endpoint: "https://dbpedia.org/sparql"
      
  post_processing:
    confidence_calibration: true
    conflict_resolution: "highest_confidence"
    human_in_the_loop: false
```

### Graph Embeddings Configuration

```yaml
graph_embeddings:
  algorithms:
    node2vec:
      dimensions: 128
      walk_length: 80
      num_walks: 10
      p: 0.5  # Return parameter
      q: 2.0  # In-out parameter
      window_size: 10
      min_count: 1
      workers: 8
      
    transE:
      embedding_dim: 100
      learning_rate: 0.01
      margin: 1.0
      batch_size: 256
      num_epochs: 1000
      
    graphSAGE:
      layers: [128, 64]
      num_samples: [10, 5]
      aggregator: "mean"
      batch_size: 256
      
    rotate:
      embedding_dim: 100
      learning_rate: 0.001
      negative_samples: 10
      regularization_weight: 0.01
      
  training:
    split_ratio: [0.8, 0.1, 0.1]  # train, val, test
    early_stopping: true
    patience: 10
    
  evaluation:
    metrics: ["link_prediction", "node_classification", "cluster_quality"]
    test_set_size: 0.2
    
  serving:
    model_path: "/models/embeddings/"
    update_frequency: "weekly"
    cache_enabled: true
```

## Architecture Patterns

### Knowledge Graph Construction Pipeline

```python
class KnowledgeGraphPipeline:
    def __init__(self, extractor, linker, reasoner):
        self.extractor = extractor
        self.linker = linker
        self.reasoner = reasoner
    
    async def build_kg(self, documents: List[Document]) -> KnowledgeGraph:
        # Extract entities and relations
        extracted = []
        for doc in documents:
            entities = await self.extractor.extract(doc)
            relations = await self.extractor.extract_relations(doc)
            extracted.append((entities, relations))
        
        # Link entities to knowledge base
        linked = await self.linker.link_entities(extracted)
        
        # Reason and infer new facts
        inferences = await self.reasoner.infer(linked)
        
        # Build graph
        graph = self.assemble_graph(linked, inferences)
        
        return KnowledgeGraph(
            entities=graph.entities,
            relations=graph.relations,
            inferences=inferences,
            statistics=graph.statistics,
        )
```

### Ontology Reasoning Engine

```python
class OntologyReasoningEngine:
    def __init__(self, reasoner, ontology):
        self.reasoner = reasoner
        self.ontology = ontology
    
    async def infer_facts(self, known_facts: List[Fact]) -> List[Inference]:
        # Load ontology and facts
        self.reasoner.load_ontology(self.ontology)
        self.reasoner.add_facts(known_facts)
        
        # Run reasoning
        inferred = await self.reasoner.reason()
        
        # Validate inferences
        valid_inferences = self.validate_inferences(inferred)
        
        return valid_inferences
    
    def validate_inferences(self, inferences: List[Inference]) -> List[Inference]:
        valid = []
        for inference in inferences:
            if self.is_consistent(inference):
                valid.append(inference)
        return valid
```

### Entity Resolution Engine

```python
class EntityResolutionEngine:
    def __init__(self, blocking_strategy, similarity_metric):
        self.blocking = blocking_strategy
        self.similarity = similarity_metric
    
    async def resolve_entities(
        self,
        entities: List[Entity],
    ) -> List[EntityCluster]:
        # Block entities for comparison
        blocks = self.blocking.create_blocks(entities)
        
        # Compare entities within blocks
        comparisons = []
        for block in blocks:
            for i in range(len(block)):
                for j in range(i + 1, len(block)):
                    sim = self.similarity.compare(block[i], block[j])
                    if sim > self.similarity.threshold:
                        comparisons.append((block[i], block[j], sim))
        
        # Cluster matching entities
        clusters = self.cluster_entities(comparisons)
        
        return clusters
```

### Graph Embedding Training Pipeline

```python
class GraphEmbeddingPipeline:
    def __init__(self, graph_store, embedding_model):
        self.graph = graph_store
        self.model = embedding_model
    
    async def train_embeddings(
        self,
        algorithm: str,
        config: EmbeddingConfig,
    ) -> TrainedEmbeddings:
        # Prepare training data
        triples = await self.graph.export_triples()
        
        # Split data
        train, val, test = self.split_data(triples, config.split_ratio)
        
        # Train model
        model = self.model.train(
            algorithm=algorithm,
            train_data=train,
            config=config,
        )
        
        # Evaluate
        metrics = self.evaluate(model, val, test)
        
        return TrainedEmbeddings(
            model=model,
            metrics=metrics,
            algorithm=algorithm,
            trained_at=datetime.utcnow(),
        )
```

## Integration Guide

### SPARQL Endpoint Integration

```python
class SPARQLIntegration:
    def __init__(self, endpoint_url: str):
        self.endpoint = endpoint_url
    
    async def query(self, sparql_query: str) -> SPARQLResult:
        headers = {
            "Accept": "application/sparql-results+json",
        }
        
        params = {
            "query": sparql_query,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.endpoint,
                headers=headers,
                params=params,
            )
        
        return self.parse_sparql_result(response.json())
    
    async def update(self, sparql_update: str) -> bool:
        headers = {
            "Content-Type": "application/sparql-update",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                headers=headers,
                data=sparql_update,
            )
        
        return response.status_code == 200
```

### Wikidata Integration

```python
class WikidataIntegration:
    def __init__(self, api_url: str = "https://www.wikidata.org/w/api.php"):
        self.api_url = api_url
    
    async def search_entity(self, query: str) -> List[WikidataEntity]:
        params = {
            "action": "wbsearchentities",
            "search": query,
            "language": "en",
            "format": "json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url, params=params)
        
        return self.parse_search_results(response.json())
    
    async def get_entity(self, entity_id: str) -> WikidataEntity:
        params = {
            "action": "wbgetentities",
            "ids": entity_id,
            "format": "json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url, params=params)
        
        return self.parse_entity(response.json())
```

### DBpedia Integration

```python
class DBpediaIntegration:
    def __init__(self, sparql_endpoint: str = "https://dbpedia.org/sparql"):
        self.sparql = SPARQLIntegration(sparql_endpoint)
    
    async def get_entity_data(self, uri: str) -> Dict:
        query = f"""
        SELECT ?property ?value WHERE {{
            <{uri}> ?property ?value .
        }}
        LIMIT 100
        """
        
        result = await self.sparql.query(query)
        return self.parse_entity_data(result)
    
    async def find_related_entities(self, uri: str, max_results: int = 10) -> List[Dict]:
        query = f"""
        SELECT ?related ?relatedLabel ?relation WHERE {{
            <{uri}> ?relation ?related .
            ?related rdfs:label ?relatedLabel .
            FILTER(LANG(?relatedLabel) = 'en')
        }}
        LIMIT {max_results}
        """
        
        result = await self.sparql.query(query)
        return self.parse_related_entities(result)
```

## Performance Optimization

### Database Optimization

```sql
-- RDF triple indexing
CREATE INDEX ON triples (subject)
CREATE INDEX ON triples (predicate)
CREATE INDEX ON triples (object)
CREATE INDEX ON triples (subject, predicate)
CREATE INDEX ON triples (predicate, object)

-- Full-text search index
CREATE FULLTEXT INDEX ON triples (object)
WHERE predicate = 'rdfs:label'

-- Materialized views for common queries
CREATE MATERIALIZED VIEW entity_counts AS
SELECT subject, COUNT(*) as triple_count
FROM triples
GROUP BY subject;
```

### Caching Strategy

```python
class KnowledgeGraphCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_sparql_result(self, query_hash: str) -> Optional[SPARQLResult]:
        cache_key = f"kg_sparql:{query_hash}"
        cached = await self.redis.get(cache_key)
        if cached:
            return SPARQLResult.from_json(cached)
        return None
    
    async def cache_sparql_result(self, query_hash: str, result: SPARQLResult):
        cache_key = f"kg_sparql:{query_hash}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            result.to_json()
        )
```

### Batch Processing

```python
class KnowledgeGraphBatchProcessor:
    def __init__(self, batch_size: int = 10000):
        self.batch_size = batch_size
    
    async def process_batch(self, items: List, processor: Callable):
        batches = [
            items[i:i+self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await processor(batch)
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class KnowledgeGraphEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive knowledge graph data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive knowledge graph data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class KnowledgeGraphAccessControl:
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

### Audit Logging

```python
class KnowledgeGraphAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'action': event.action,
            'resource_id': event.resource_id,
            'details': event.details,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: SPARQL query timeout**
```python
async def diagnose_sparql_timeout(query: str):
    # Analyze query complexity
    complexity = await analyze_query_complexity(query)
    
    print(f"SPARQL Query Analysis:")
    print(f"  Triple patterns: {complexity.triple_patterns}")
    print(f"  Join operations: {complexity.joins}")
    print(f"  Optional clauses: {complexity.optionals}")
    
    if complexity.triple_patterns > 5:
        print(f"  WARNING: Complex query")
        print(f"  Recommendations:")
        print(f"    1. Add LIMIT clause")
        print(f"    2. Use property paths sparingly")
        print(f"    3. Consider materialized views")
```

**Issue: Entity linking low accuracy**
```python
async def diagnose_entity_linking_accuracy(documents: List[Document]):
    # Get linking results
    results = await entity_linker.link_documents(documents)
    
    print(f"Entity Linking Results:")
    print(f"  Total mentions: {len(results.mentions)}")
    print(f"  Linked: {len(results.linked)}")
    print(f"  Unlinked: {len(results.unlinked)}")
    
    # Analyze by entity type
    by_type = defaultdict(list)
    for mention in results.linked:
        by_type[mention.entity_type].append(mention)
    
    print(f"\nBy Entity Type:")
    for entity_type, mentions in by_type.items():
        avg_confidence = sum(m.confidence for m in mentions) / len(mentions)
        print(f"  {entity_type}: {len(mentions)} (avg confidence: {avg_confidence:.2f})")
```

**Issue: Graph embedding quality**
```python
async def diagnose_embedding_quality(embeddings: TrainedEmbeddings):
    print(f"Graph Embedding Quality:")
    print(f"  Algorithm: {embeddings.algorithm}")
    print(f"  Dimensions: {embeddings.dimensions}")
    
    # Evaluate metrics
    metrics = embeddings.metrics
    
    print(f"\nMetrics:")
    print(f"  Link Prediction (MRR): {metrics.link_prediction_mrr:.4f}")
    print(f"  Link Prediction (Hits@10): {metrics.link_prediction_hits10:.4f}")
    print(f"  Node Classification: {metrics.node_classification_f1:.4f}")
    
    if metrics.link_prediction_mrr < 0.5:
        print(f"\n  WARNING: Low embedding quality")
        print(f"  Recommendations:")
        print(f"    1. Increase embedding dimensions")
        print(f"    2. Add more training epochs")
        print(f"    3. Try different algorithm")
```

## API Reference

### Knowledge Graph Query API

```python
# SPARQL query
POST /api/v1/sparql
Request:
{
    "query": "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10",
    "format": "json"
}

Response:
{
    "results": [
        {"s": "http://example.com/person/1", "p": "http://schema.org/name", "o": "Alice"},
        {"s": "http://example.com/person/1", "p": "http://schema.org/email", "o": "alice@example.com"}
    ],
    "execution_time_ms": 150
}
```

### Entity Resolution API

```python
# Resolve entities
POST /api/v1/entities/resolve
Request:
{
    "entities": [
        {"id": "1", "name": "Alice Smith", "type": "Person"},
        {"id": "2", "name": "Alice S.", "type": "Person"}
    ],
    "algorithm": "blocking",
    "similarity_threshold": 0.85
}

Response:
{
    "clusters": [
        {
            "cluster_id": "C-001",
            "entities": ["1", "2"],
            "confidence": 0.92
        }
    ],
    "resolved_count": 1
}
```

### Graph Embedding API

```python
# Get entity embeddings
GET /api/v1/embeddings/{entity_id}
Response:
{
    "entity_id": "person/1",
    "algorithm": "node2vec",
    "embedding": [0.1, 0.2, 0.3, ...],
    "dimensions": 128
}

# Find similar entities
POST /api/v1/embeddings/similar
Request:
{
    "entity_id": "person/1",
    "algorithm": "node2vec",
    "top_k": 10
}

Response:
{
    "similar_entities": [
        {"entity_id": "person/2", "similarity": 0.85},
        {"entity_id": "person/3", "similarity": 0.78}
    ]
}
```

## Data Models

### Knowledge Graph Model

```python
class KnowledgeGraph:
    graph_id: str
    name: str
    description: str
    entities: List[Entity]
    relations: List[Relation]
    ontology: Ontology
    statistics: GraphStatistics
    created_at: datetime
    updated_at: datetime
```

### Entity Model

```python
class Entity:
    entity_id: str
    name: str
    entity_type: str
    properties: Dict[str, Any]
    source: Optional[str]
    confidence: Optional[float]
    created_at: datetime
    updated_at: datetime
```

### Relation Model

```python
class Relation:
    relation_id: str
    source_entity_id: str
    target_entity_id: str
    relation_type: str
    properties: Dict[str, Any]
    confidence: Optional[float]
    created_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: knowledge-graph-service
  namespace: knowledge-graphs-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: knowledge-graph-service
  template:
    metadata:
      labels:
        app: knowledge-graph-service
    spec:
      containers:
      - name: knowledge-graph
        image: your-registry/knowledge-graph-service:2.0.0
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
sparql_queries_counter = Counter(
    'kg_sparql_queries_total',
    'Total SPARQL queries',
    ['status']
)

sparql_query_duration = Histogram(
    'kg_sparql_query_duration_seconds',
    'SPARQL query duration',
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0]
)

# Entity metrics
entities_counter = Counter(
    'kg_entities_total',
    'Total entities',
    ['type']
)

relations_counter = Counter(
    'kg_relations_total',
    'Total relations',
    ['type']
)

# Embedding metrics
embeddings_training_duration = Histogram(
    'kg_embeddings_training_duration_seconds',
    'Embedding training duration',
    ['algorithm'],
    buckets=[60, 300, 600, 1800, 3600]
)
```

### Grafana Dashboard

```json
{
    "dashboard": {
        "title": "Knowledge Graphs",
        "panels": [
            {
                "title": "SPARQL Query Rate",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(kg_sparql_queries_total[5m])",
                        "legendFormat": "{{status}}"
                    }
                ]
            },
            {
                "title": "Entity Count",
                "type": "stat",
                "targets": [
                    {
                        "expr": "kg_entities_total",
                        "legendFormat": "{{type}}"
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
- name: kg_alerts
  rules:
  - alert: HighSparqlLatency
    expr: histogram_quantile(0.95, rate(kg_sparql_query_duration_seconds_bucket[5m])) > 5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "SPARQL query latency exceeds 5 seconds"
      
  - alert: LowEntityCount
    expr: kg_entities_total < 1000
    for: 24h
    labels:
      severity: info
    annotations:
      summary: "Knowledge graph has low entity count"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestKnowledgeGraph:
    def test_add_entity(self, knowledge_graph):
        entity = Entity(
            entity_id="person/1",
            name="Alice",
            entity_type="Person",
        )
        
        knowledge_graph.add_entity(entity)
        
        assert knowledge_graph.get_entity("person/1") is not None
    
    def test_add_relation(self, knowledge_graph):
        relation = Relation(
            source_entity_id="person/1",
            target_entity_id="person/2",
            relation_type="knows",
        )
        
        knowledge_graph.add_relation(relation)
        
        relations = knowledge_graph.get_relations("person/1")
        assert len(relations) > 0
```

### Integration Tests

```python
class TestEndToEndKnowledgeGraph:
    async def test_kg_construction(self, kg_system):
        # Build knowledge graph
        documents = await kg_system.load_documents()
        
        kg = await kg_system.build_kg(documents)
        
        assert len(kg.entities) > 0
        assert len(kg.relations) > 0
        
        # Query knowledge graph
        results = await kg_system.query(
            "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
        )
        
        assert len(results) > 0
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class KnowledgeGraphUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def query_sparql(self):
        self.client.post("/api/v1/sparql", json={
            "query": "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10",
        })
    
    @task(5)
    def get_entity(self):
        self.client.get(f"/api/v1/entities/entity-{self.entity_counter}")
        self.entity_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/sparql", methods=["POST"])
@app.route("/api/v2/sparql", methods=["POST"])
async def sparql_query():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await sparql_query_v2()
    return await sparql_query_v1()
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

- **RDF**: Resource Description Framework - W3C standard for data interchange
- **OWL**: Web Ontology Language - W3C standard for ontologies
- **SPARQL**: Query language for RDF data
- **Ontology**: Formal specification of a domain's conceptualization
- **Entity Linking**: Mapping textual mentions to knowledge base entities
- **Knowledge Graph**: Graph-structured knowledge base with entities and relations
- **Graph Embeddings**: Low-dimensional vector representations of graph elements
- **Triple**: RDF statement consisting of subject, predicate, object
- **Reasoning**: Inferring new facts from existing knowledge
- **Entity Resolution**: Identifying and merging duplicate entities

## Changelog

### Version 2.0.0 (2026-07-01)
- Added graph embeddings support
- Implemented entity resolution
- Enhanced reasoning capabilities
- Added Wikidata integration

### Version 1.5.0 (2026-01-15)
- Added SPARQL support
- Implemented entity linking
- Enhanced ontology management

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic RDF support
- Simple query execution

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def query_knowledge_graph(
    sparql_query: str,
    format: str = "json",
) -> SPARQLResult:
    """Query knowledge graph with SPARQL.
    
    Args:
        sparql_query: SPARQL query string.
        format: Result format.
    
    Returns:
        SPARQL query result.
    
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

Copyright (c) 2026 Knowledge Graph Platform

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
