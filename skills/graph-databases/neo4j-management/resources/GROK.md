# Graph Database Agent

## Overview

The **Graph Database Agent** provides comprehensive graph database management using Neo4j and similar technologies. This agent enables relationship-focused data modeling, graph analytics, and knowledge graph construction.

## Core Capabilities

### 1. Neo4j Operations
Database management and operations:
- **Node Management**: Create, read, update, delete nodes
- **Relationship Management**: Connect and traverse relationships
- **Index Management**: Performance optimization
- **Constraints**: Data integrity enforcement
- **Transactions**: ACID-compliant operations

### 2. Graph Traversal
Navigate graph structures:
- **Breadth-First Search**: Level-order traversal
- **Depth-First Search**: Path exploration
- **Shortest Path**: Dijkstra, A* algorithms
- **All Paths**: Multiple path discovery
- **Cycle Detection**: Graph cycle identification

### 3. Knowledge Graphs
Build and query knowledge bases:
- **Entity Management**: Create and link entities
- **Relationship Extraction**: Connect related concepts
- **Semantic Search**: Find related entities
- **Inference Engine**: Deduce new relationships
- **Ontology Management**: Schema definition

### 4. Graph Analytics
Analyze graph structures:
- **Centrality Analysis**: Degree, betweenness, PageRank
- **Community Detection**: Louvain, label propagation
- **Link Prediction**: Predict missing connections
- **Similarity Analysis**: Node similarity scoring
- **Graph Embedding**: Vector representation

## Usage Examples

### Connect to Neo4j

```python
from graph_db import Neo4jConnector

neo4j = Neo4jConnector()
conn = neo4j.connect(uri="bolt://localhost:7687", user="neo4j", password="password")
print(f"Connected: {conn['connected']}")
```

### Create Nodes and Relationships

```python
from graph_db import KnowledgeGraph

graph = KnowledgeGraph()
graph.add_entity('Person', 'john', {'name': 'John', 'age': 30})
graph.add_entity('Person', 'jane', {'name': 'Jane', 'age': 25})
graph.add_relation('john', 'jane', 'KNOWS', {'since': '2020'})
query = graph.query_entity('john')
```

### Graph Traversal

```python
from graph_db import GraphTraversal

traversal = GraphTraversal()
paths = traversal.find_shortest_path('user1', 'user5')
print(f"Path: {paths['path']}, Length: {paths['length']}")
```

### Analytics

```python
from graph_db import GraphAnalytics

analytics = GraphAnalytics()
centrality = analytics.calculate_centrality('john')
communities = analytics.detect_communities('louvain')
```

## Cypher Query Language

### Basic Queries
```cypher
// Create node
CREATE (p:Person {name: 'John', age: 30})

// Match nodes
MATCH (p:Person) WHERE p.age > 25 RETURN p

// Create relationship
MATCH (a:Person {name: 'John'}), (b:Person {name: 'Jane'})
CREATE (a)-[r:KNOWS {since: '2020'}]->(b)
```

### Advanced Queries
```cypher
// Shortest path
MATCH (a:Person {name: 'A'}), (b:Person {name: 'B'})
MATCH p = shortestPath((a)-[*]->(b))
RETURN p

// Community detection
CALL algo.louvain('Person', 'KNOWS', {write: true})
```

## Graph Algorithms

### Path Finding
| Algorithm | Use Case | Complexity |
|-----------|----------|------------|
| BFS | Level-order traversal | O(V+E) |
| DFS | Deep exploration | O(V+E) |
| Dijkstra | Weighted shortest path | O(E + V log V) |
| A* | Heuristic shortest path | O(E) |

### Centrality Measures
| Measure | Description | Use Case |
|---------|-------------|----------|
| Degree | Number of connections | Hub identification |
| Betweenness | Bridge importance | Influencers |
| Closeness | Average distance | Reachability |
| PageRank | Importance score | Search ranking |

## Graph Embedding Techniques

### Node Embeddings
- **Node2Vec**: Random walk-based
- **GraphSAGE**: Inductive learning
- **DeepWalk**: Skip-gram on walks
- **TransE**: Translational embedding

### Applications
- **Similarity Search**: Find similar nodes
- **Node Classification**: Predict node labels
- **Link Prediction**: Predict edges
- **Clustering**: Community detection

## Knowledge Graph Architecture

### Components
```
┌─────────────────────────────────────────┐
│           Knowledge Graph               │
├─────────────────────────────────────────┤
│  Entities: Person, Organization, Event  │
│  Relationships: KNOWS, WORKS_AT         │
│  Properties: name, date, location       │
└─────────────────────────────────────────┘
```

### Ontology Design
- **Classes**: Entity types
- **Properties**: Attributes
- **Relationships**: Connections
- **Rules**: Constraints and inferences

## Use Cases

### 1. Social Networks
- Friend recommendations
- Influence analysis
- Community detection
- Trend analysis

### 2. Fraud Detection
- Transaction patterns
- Account linking
- Anomaly detection
- Investigation trails

### 3. Recommendation Systems
- Product recommendations
- Content personalization
- Collaborative filtering
- Knowledge-based suggestions

### 4. Master Data Management
- Customer 360
- Product relationships
- Organizational hierarchy
- Reference data

### 5. Supply Chain
- Supplier networks
- Dependency mapping
- Risk analysis
- Optimization

## Performance Optimization

### Indexing
- **Node Indexes**: Property-based lookup
- **Relationship Indexes**: Type and property search
- **Full-text**: Text search capability
- **Spatial**: Geographic queries

### Query Optimization
- **EXPLAIN**: Query plan analysis
- **PROFILE**: Execution metrics
- **Caching**: Result caching
- **Constraints**: Data pruning

## Related Skills

- [Data Engineering](../data-engineering/data-pipelines/README.md) - Data pipelines
- [Machine Learning Operations](../ml-ops/model-deployment/README.md) - ML models
- [Analytics](../analytics/data-analysis/README.md) - Data analysis

---

**File Path**: `skills/graph-databases/neo4j-management/resources/graph_db.py`
