# GraphQL Agent

## Overview

The **GraphQL Agent** provides comprehensive GraphQL API development capabilities including schema design, query construction, execution optimization, and security analysis. This agent enables building efficient, type-safe APIs that solve over-fetching and under-fetching problems.

## Core Capabilities

### 1. Schema Design
Build and manage GraphQL schemas:
- **Type Definitions**: Object, scalar, enum, union, interface
- **Schema Generation**: From code or introspection
- **Directives**: Custom behavior annotation
- **Federation**: Multi-service schema composition

### 2. Query Building
Construct efficient GraphQL operations:
- **Queries**: Data fetching operations
- **Mutations**: Data modification operations
- **Subscriptions**: Real-time updates
- **Fragments**: Reusable field sets
- **Variables**: Dynamic query parameters

### 3. Query Execution
Execute and optimize queries:
- **Resolver Functions**: Data fetching logic
- **Batching**: Reduce database queries
- **Caching**: Response caching strategies
- **Error Handling**: Structured error responses

### 4. Performance Optimization
Optimize API performance:
- **Query Complexity Analysis**: Prevent expensive queries
- **Depth Limiting**: Prevent nested attacks
- **DataLoader Batching**: N+1 query prevention
- **Response Caching**: CDN integration

### 5. Security Analysis
Secure GraphQL implementations:
- **Authentication**: JWT, API keys, OAuth
- **Authorization**: Field-level permissions
- **Rate Limiting**: Query cost limits
- **Introspection Control**: Production security

## Usage Examples

### Build Schema

```python
from graphql import GraphQLSchemaBuilder, TypeDefinition, Field

builder = GraphQLSchemaBuilder()
builder.add_type(TypeDefinition(
    name='User',
    kind='OBJECT',
    fields=[
        Field(name='id', graphql_type='ID!'),
        Field(name='name', graphql_type='String!'),
        Field(name='email', graphql_type='String!')
    ]
))
builder.add_query(Field(name='users', graphql_type='[User!]!'))

schema = builder.generate_schema()
print(schema)
```

### Build Query

```python
from graphql import GraphQLOperation

ops = GraphQLOperation()
query = ops.build_query('GetUsers', ['id', 'name', 'email'])
print(query['query'])
```

### Execute Query

```python
from graphql import GraphQLExecutor

executor = GraphQLExecutor()
result = executor.execute_query('{ users { id name } }')
print(f"Data: {result['data']}")
```

### Performance Analysis

```python
from graphql import GraphQLPerformance

perf = GraphQLPerformance()
analysis = perf.analyze_query_complexity('{ users { posts { comments { author } } } }')
print(f"Complexity: {analysis['complexity_score']}")
```

## GraphQL Types

### Scalar Types
- `String`: Text data
- `Int`: 32-bit integer
- `Float`: Double precision
- `Boolean`: True/false
- `ID`: Unique identifier

### Object Type
```graphql
type User {
  id: ID!
  name: String!
  email: String
  posts: [Post!]!
}
```

### Complex Types
- **Enum**: Restricted value set
- **Union**: Multiple possible types
- **Interface**: Common field contract
- **Input**: Mutation input type

## Query Optimization

### DataLoader Pattern
```python
class UserLoader:
    async def load_many(self, ids):
        # Batch load users in single query
        return db.users.where(id in ids)
```

### Caching Strategy
- **Response Caching**: Store full responses
- **Partial Caching**: Cache resolver results
- **CDN Integration**: Edge caching
- **Invalidation**: Cache purging

### Query Cost Analysis
```graphql
query Expensive {
  users(first: 100) {
    posts(first: 100) {
      comments(first: 100) {
        author { name }
      }
    }
  }
}
```

## Security Best Practices

### 1. Depth Limiting
```python
max_depth = 10
```

### 2. Query Cost Limits
```python
max_cost = 1000
```

### 3. Field Masking
```python
hidden_fields = ['password', 'ssn']
```

### 4. Disable Introspection
```python
introspection_disabled = True  # Production only
```

## GraphQL vs REST

| Aspect | GraphQL | REST |
|--------|---------|------|
| Data Fetching | Single request | Multiple endpoints |
| Over-fetching | No | Common |
| Under-fetching | No | Common |
| Type Safety | Built-in | Optional (OpenAPI) |
| Versioning | Deprecation | New endpoints |
| Learning Curve | Moderate | Lower |

## Popular GraphQL Tools

### Servers
- **Apollo Server**: Full-featured, production-ready
- **GraphQL Yoga**: Lightweight, Express-based
- **Hasura**: GraphQL over PostgreSQL
- **StepZen**: GraphQL composition

### Clients
- **Apollo Client**: React integration
- **URQL**: Lightweight React client
- **GraphQL Request**: Simple HTTP client

### Development Tools
- **GraphiQL**: In-browser IDE
- **GraphQL Playground**: Advanced dev tool
- **Apollo Studio**: Monitoring platform

## Federation Architecture

### GraphQL Federation
```
┌─────────────────┐     ┌─────────────────┐
│  User Service   │     │ Order Service   │
│   (GraphQL)     │     │   (GraphQL)     │
└────────┬────────┘     └────────┬────────┘
         │                      │
         └──────────┬───────────┘
                    │
         ┌──────────▼───────────┐
         │   Apollo Gateway     │
         │   (Federated Graph)  │
         └──────────────────────┘
```

### Federation Benefits
- Schema composition
- Distributed ownership
- Single endpoint
- Type consistency

## Use Cases

### 1. Mobile Applications
- Single endpoint for all data
- Reduced bandwidth
- Offline support

### 2. Microservices
- API aggregation
- Schema stitching
- Service orchestration

### 3. B2B Integration
- Custom data shapes
- Partner-specific fields
- Version migration

## Performance Monitoring

### Metrics
- **Query Duration**: Response time
- **Error Rate**: Failed queries
- **Cache Hit Rate**: Cache efficiency
- **Resolver Time**: Per-field timing

### Tools
- **Apollo Studio**: Query monitoring
- **GraphQL Armor**: Security metrics
- **Custom Instrumentation**: Application metrics

## Related Skills

- [API Design](../api/rest-api-design/README.md) - REST API patterns
- [Microservices Architecture](../microservices/service-architecture/README.md) - Service design
- [Performance Optimization](../performance/caching-strategies/README.md) - Caching strategies

---

**File Path**: `skills/graphql/api-design/resources/graphql.py`
