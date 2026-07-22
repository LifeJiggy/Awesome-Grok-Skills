---
name: Apollo Federation
category: graphql
version: 1.0.0
tags: [graphql, apollo, federation, supergraph, subgraph, entity-resolution]
difficulty: advanced
estimated_time: 75 minutes
prerequisites: [graphql-basics, schema-design, schema-stitching]
---

# Apollo Federation

## Overview

Apollo Federation is a powerful architecture for composing multiple GraphQL schemas into a unified supergraph. This skill covers supergraph architecture, entity resolution, @key/@external directives, and subgraph communication patterns.

## Core Concepts

### 1. Supergraph Architecture

**Subgraph Services:**
```graphql
# Users Subgraph
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
  profile: Profile!
}

# Posts Subgraph
type Post @key(fields: "id") {
  id: ID!
  title: String!
  content: String!
  author: User!
}

# Comments Subgraph
type Comment @key(fields: "id") {
  id: ID!
  content: String!
  author: User!
  post: Post!
}
```

**Router Configuration:**
```yaml
supergraph:
  listen: 0.0.0.0:4000
  introspection: false
subgraphs:
  users:
    routing_url: http://users-service:4001/graphql
    schema:
      subgraph_url: http://users-service:4001/graphql
  posts:
    routing_url: http://posts-service:4002/graphql
    schema:
      subgraph_url: http://posts-service:4002/graphql
  comments:
    routing_url: http://comments-service:4003/graphql
    schema:
      subgraph_url: http://comments-service:4003/graphql
```

### 2. Entity Resolution

**@key Directive:**
```graphql
# Entity with single-field key
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# Entity with compound key
type Product @key(fields: "upc") {
  upc: String!
  name: String!
  price: Float!
}

# Entity with nested key
type Order @key(fields: "id") {
  id: ID!
  product: Product!
  quantity: Int!
  total: Float!
}
```

**Entity Resolution Patterns:**
```graphql
# Reference resolver
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# In subgraph A (Users service)
extend type User @key(fields: "id") {
  id: ID! @external
  # Additional fields from this subgraph
  profile: Profile!
  settings: UserSettings!
}

# In subgraph B (Posts service)
extend type User @key(fields: "id") {
  id: ID! @external
  posts: [Post!]!
  postCount: Int!
}
```

### 3. @key and @external Directives

**@key Directive:**
```graphql
# Single-field key
type User @key(fields: "id") {
  id: ID!
  name: String!
}

# Compound key
type Product @key(fields: "upc manufacturer") {
  upc: String!
  manufacturer: String!
  name: String!
  price: Float!
}

# Multiple keys
type User @key(fields: "id") @key(fields: "email") {
  id: ID!
  email: String!
  name: String!
}
```

**@external Directive:**
```graphql
# External field reference
type User @key(fields: "id") {
  id: ID! @external
  name: String! @external
  email: String! @external
  # Fields resolved by this subgraph
  posts: [Post!]!
  profile: Profile!
}

# External field with @requires
type Post @key(fields: "id") {
  id: ID!
  title: String!
  author: User!
  # Requires author.name to be resolved
  authorName: String! @requires(fields: "author { name }")
}
```

### 4. Subgraph Communication

**Event-Driven Communication:**
```graphql
# Subgraph A publishes events
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

# Subgraph B subscribes to events
type Subscription {
  userCreated: User!
  userUpdated: User!
}
```

**Shared State:**
```graphql
# Shared context across subgraphs
type Context {
  currentUser: User
  requestId: String
  timestamp: DateTime
}

# Context injection
extend type Query {
  me: User! @inContext(field: "currentUser")
}
```

## Implementation Guide

### Step 1: Subgraph Design

1. Define entity types with @key
2. Identify cross-service relationships
3. Design entity resolution patterns
4. Plan data ownership

### Step 2: Subgraph Implementation

1. Implement entity resolvers
2. Add @external fields
3. Handle cross-service queries
4. Implement event publishing

### Step 3: Router Configuration

1. Configure subgraph endpoints
2. Set up authentication
3. Configure caching
4. Monitor performance

### Step 4: Testing and Deployment

1. Test entity resolution
2. Validate cross-service queries
3. Deploy subgraphs
4. Monitor supergraph health

## Common Patterns

### Entity Resolution with DataLoader
```javascript
// Users subgraph
const resolvers = {
  User: {
    __resolveReference(reference, { dataLoader }) {
      return dataLoader.user.load(reference.id);
    },
  },
  Query: {
    user: (_, { id }, { dataLoader }) => dataLoader.user.load(id),
  },
};
```

### Cross-Service Queries
```graphql
# Query spanning multiple subgraphs
query GetUserWithPosts($userId: ID!) {
  user(id: $userId) {
    id
    name
    email
    posts {
      id
      title
      content
      comments {
        id
        content
        author {
          name
        }
      }
    }
  }
}
```

### Entity Relationships
```graphql
# One-to-many relationship
type User @key(fields: "id") {
  id: ID!
  name: String!
  posts: [Post!]!
}

type Post @key(fields: "id") {
  id: ID!
  title: String!
  author: User!
}

# Many-to-many relationship
type User @key(fields: "id") {
  id: ID!
  name: String!
  groups: [Group!]!
}

type Group @key(fields: "id") {
  id: ID!
  name: String!
  members: [User!]!
}
```

## Advanced Topics

### Federation v2 Features
```graphql
# Shareable fields
type User @key(fields: "id") {
  id: ID!
  name: String! @shareable
  email: String!
}

# Override fields
type User @key(fields: "id") {
  id: ID!
  name: String! @override(from: "legacy-users")
  email: String!
}

# Inaccessible fields
type User @key(fields: "id") {
  id: ID!
  name: String!
  internalId: String! @inaccessible
}
```

### Schema Checks
```yaml
# Schema checks configuration
schema:
  check:
    breaking_changes: error
    non_breaking_changes: warning
    composition_errors: error
```

### Performance Optimization
```graphql
# Query complexity limits
query {
  users(first: 100) {
    edges {
      node {
        id
        name
        posts(first: 10) {
          edges {
            node {
              id
              title
              comments(first: 5) {
                edges {
                  node {
                    id
                    content
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## Best Practices

1. **Define clear entity boundaries** - Each subgraph owns specific entities
2. **Use compound keys** - When single fields aren't unique
3. **Implement efficient resolvers** - Use DataLoader for batching
4. **Monitor performance** - Track query latency across subgraphs
5. **Handle errors gracefully** - Implement fallback strategies
6. **Version your schemas** - Use schema versioning
7. **Test thoroughly** - Validate entity resolution
8. **Document cross-service dependencies** - Clear API contracts
9. **Implement caching** - Use distributed caching
10. **Monitor health** - Track subgraph availability

## Common Pitfalls

1. **Circular dependencies** - Subgraphs depending on each other
2. **N+1 queries** - Inefficient entity resolution
3. **Missing keys** - Entities without proper @key directives
4. **Over-fetching** - Requesting too much data
5. **Under-fetching** - Not enough data in single query
6. **Error propagation** - Errors in one subgraph affecting others
7. **Stale data** - Caching issues across services
8. **Composition errors** - Schema composition failures

## Tools and Libraries

- **Apollo Router** - High-performance GraphQL router
- **Apollo Federation** - Federation composition library
- **Apollo Studio** - Schema management and monitoring
- **GraphQL Code Generator** - Generate TypeScript types
- **DataLoader** - Batching and caching library

## Real-World Examples

### E-commerce Platform
```graphql
# Products subgraph
type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Float!
  inventory: Inventory!
}

# Orders subgraph
type Order @key(fields: "id") {
  id: ID!
  product: Product!
  quantity: Int!
  total: Float!
  user: User!
}

# Users subgraph
type User @key(fields: "id") {
  id: ID!
  name: String!
  orders: [Order!]!
  profile: Profile!
}
```

### Social Media Platform
```graphql
# Users subgraph
type User @key(fields: "id") {
  id: ID!
  name: String!
  followers: [User!]!
  following: [User!]!
}

# Posts subgraph
type Post @key(fields: "id") {
  id: ID!
  content: String!
  author: User!
  likes: [User!]!
  comments: [Comment!]!
}

# Notifications subgraph
type Notification @key(fields: "id") {
  id: ID!
  type: NotificationType!
  user: User!
  post: Post
}
```

## Summary

Apollo Federation enables building scalable, distributed GraphQL APIs. By understanding entity resolution, @key/@external directives, and subgraph communication, you can create robust, maintainable federated architectures.

## Advanced Configuration

### Federation Composition Configuration
```yaml
# Federation composition configuration
federation:
  version: 2
  subgraphs:
    users:
      routing_url: http://users-service:4001/graphql
      schema:
        subgraph_url: http://users-service:4001/graphql
      introspection: true
      timeout: 5000
      retry:
        maxAttempts: 3
        initialDelay: 1000
        maxDelay: 5000
    posts:
      routing_url: http://posts-service:4002/graphql
      schema:
        subgraph_url: http://posts-service:4002/graphql
      introspection: true
      timeout: 5000
      retry:
        maxAttempts: 3
        initialDelay: 1000
        maxDelay: 5000
  supergraph:
    listen: 0.0.0.0:4000
    introspection: false
    playground: false
    healthCheck: true
    landingPage: false
```

### Entity Resolution Configuration
```javascript
// Advanced entity resolution configuration
const entityConfig = {
  users: {
    entityType: 'User',
    keys: ['id', 'email'],
    resolveEndpoint: 'http://users-service:4001/graphql',
    batchSize: 100,
    cache: {
      enabled: true,
      ttl: 300000,
      maxEntries: 10000,
    },
    retry: {
      maxAttempts: 3,
      backoff: 'exponential',
    },
  },
  posts: {
    entityType: 'Post',
    keys: ['id', 'slug'],
    resolveEndpoint: 'http://posts-service:4002/graphql',
    batchSize: 50,
    cache: {
      enabled: true,
      ttl: 600000,
      maxEntries: 5000,
    },
  },
};
```

### Router Configuration
```yaml
# Apollo Router configuration
router:
  listen: 0.0.0.0:4000
  introspection: false
  playground: false
  healthCheck:
    enabled: true
    listen: 0.0.0.0:8088
    path: /health
  traffic_shaping:
    all:
      timeout: 30s
      retry:
        min_retries: 2
        max_retries: 5
        timeout: 10s
        backoff: 100ms
    subgraphs:
      users:
        timeout: 5s
        experimental_retry:
          min_retries: 1
          max_retries: 3
      posts:
        timeout: 10s
  authentication:
    router:
      jwt:
        jwks:
          url: http://auth-service:8080/.well-known/jwks.json
        header_name: Authorization
        header_value_prefix: Bearer
  coprocessor:
    url: http://coprocessor-service:4001
    timeout: 1s
    router:
      request:
        headers: true
        context: true
      response:
        headers: true
```

## Architecture Patterns

### Federation Gateway Pattern
```javascript
// Federation gateway implementation
class FederationGateway {
  constructor(config) {
    this.subgraphs = new Map();
    this.entityResolver = new EntityResolver(config);
    this.router = new Router(config);
  }

  async initialize() {
    // Register subgraphs
    for (const [name, config] of Object.entries(config.subgraphs)) {
      const subgraph = await this.createSubgraph(name, config);
      this.subgraphs.set(name, subgraph);
    }

    // Compose schema
    this.schema = await this.composeSchema();
    
    // Start router
    await this.router.start(this.schema);
  }

  async createSubgraph(name, config) {
    const subgraph = new Subgraph(name, config);
    await subgraph.connect();
    return subgraph;
  }

  async composeSchema() {
    const schemas = [];
    for (const [name, subgraph] of this.subgraphs) {
      schemas.push({
        name,
        typeDefs: subgraph.schema,
        resolvers: subgraph.resolvers,
      });
    }
    return compose(schemas);
  }
}
```

### Entity Resolution Pattern
```javascript
// Entity resolution with caching
class EntityResolver {
  constructor(config) {
    this.cache = new EntityCache(config.cache);
    this.loaders = new Map();
  }

  async resolve(typeName, representation) {
    const cacheKey = `${typeName}:${JSON.stringify(representation)}`;
    
    // Check cache
    const cached = await this.cache.get(cacheKey);
    if (cached) {
      return cached;
    }

    // Resolve entity
    const entity = await this.fetchEntity(typeName, representation);
    
    // Cache result
    if (entity) {
      await this.cache.set(cacheKey, entity);
    }
    
    return entity;
  }

  async fetchEntity(typeName, representation) {
    const loader = this.getLoader(typeName);
    return loader.load(representation);
  }

  getLoader(typeName) {
    if (!this.loaders.has(typeName)) {
      this.loaders.set(typeName, new DataLoader(async (representations) => {
        // Batch entity resolution
        const entities = await Promise.all(
          representations.map(rep => this.resolveSingle(typeName, rep))
        );
        return entities;
      }, {
        maxBatchSize: 100,
        cacheKeyFn: (rep) => JSON.stringify(rep),
      }));
    }
    return this.loaders.get(typeName);
  }
}
```

### Schema Composition Pattern
```javascript
// Schema composition with validation
class SchemaComposer {
  constructor() {
    this.validators = [];
    this.transformers = [];
  }

  async compose(subgraphs) {
    // Validate individual schemas
    for (const subgraph of subgraphs) {
      await this.validateSchema(subgraph);
    }

    // Check composition errors
    const compositionResult = composeServices(subgraphs);
    if (compositionResult.errors) {
      throw new CompositionError(compositionResult.errors);
    }

    // Apply transformations
    let schema = compositionResult.schema;
    for (const transformer of this.transformers) {
      schema = await transformer.transform(schema);
    }

    return schema;
  }

  async validateSchema(subgraph) {
    for (const validator of this.validators) {
      const errors = await validator.validate(subgraph);
      if (errors.length > 0) {
        throw new ValidationError(subgraph.name, errors);
      }
    }
  }
}
```

## Integration Guide

### Apollo Router Integration
```yaml
# Apollo Router configuration
supergraph:
  listen: 0.0.0.0:4000
  introspection: false
  playground: false
  healthCheck: true
subgraphs:
  users:
    routing_url: http://users-service:4001/graphql
    schema:
      subgraph_url: http://users-service:4001/graphql
  posts:
    routing_url: http://posts-service:4002/graphql
    schema:
      subgraph_url: http://posts-service:4002/graphql
plugins:
  telemetry:
    metrics:
      prometheus:
        enabled: true
        listen: 0.0.0.0:9090
        path: /metrics
    tracing:
      enabled: true
      sampler: 1.0
  authentication:
    router:
      jwt:
        jwks:
          url: http://auth-service:8080/.well-known/jwks.json
  coprocessor:
    url: http://coprocessor-service:4001
    timeout: 1s
    router:
      request:
        headers: true
        context: true
      response:
        headers: true
```

### Apollo Federation Integration
```javascript
// Apollo Federation setup
const { ApolloServer } = require('@apollo/server');
const { ApolloGateway, IntrospectAndCompose } = require('@apollo/gateway');

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'users', url: 'http://users-service:4001/graphql' },
      { name: 'posts', url: 'http://posts-service:4002/graphql' },
      { name: 'comments', url: 'http://comments-service:4003/graphql' },
    ],
  }),
  buildService({ url }) {
    return new ApolloFetch({ uri: url });
  },
});

const server = new ApolloServer({
  gateway,
  plugins: [
    {
      async requestDidStart() {
        return {
          async willSendResponse({ response }) {
            // Add federation metadata
            response.extensions = {
              ...response.extensions,
              federation: {
                subgraphs: gateway.serviceMap.size,
                queryPlan: response.extensions?.queryPlan,
              },
            };
          },
        };
      },
    },
  ],
});
```

### Event-Driven Integration
```javascript
// Event-driven subgraph communication
class EventDrivenFederation {
  constructor(config) {
    this.eventBus = new EventBus(config.eventBus);
    this.subgraphs = new Map();
  }

  async publishEvent(eventName, payload) {
    await this.eventBus.publish(eventName, payload);
  }

  async subscribeToEvent(eventName, handler) {
    await this.eventBus.subscribe(eventName, handler);
  }

  async registerSubgraph(name, config) {
    const subgraph = new EventDrivenSubgraph(name, config);
    this.subgraphs.set(name, subgraph);
    
    // Subscribe to relevant events
    for (const event of config.events) {
      await this.subscribeToEvent(event, async (payload) => {
        await subgraph.handleEvent(event, payload);
      });
    }
    
    return subgraph;
  }
}
```

## Performance Optimization

### Query Planning Optimization
```javascript
// Query planning optimization
class QueryPlanner {
  constructor(schema) {
    this.schema = schema;
    this.cache = new QueryPlanCache();
  }

  async plan(query, variables) {
    const cacheKey = this.generateCacheKey(query, variables);
    
    // Check cache
    const cachedPlan = await this.cache.get(cacheKey);
    if (cachedPlan) {
      return cachedPlan;
    }

    // Generate query plan
    const plan = this.generatePlan(query, variables);
    
    // Optimize plan
    const optimizedPlan = this.optimizePlan(plan);
    
    // Cache plan
    await this.cache.set(cacheKey, optimizedPlan);
    
    return optimizedPlan;
  }

  generatePlan(query, variables) {
    // Parse query and identify subgraph operations
    const operations = this.extractOperations(query);
    
    // Build execution plan
    const plan = {
      fetches: [],
      sequences: [],
      parallel: [],
    };

    for (const operation of operations) {
      const fetch = {
        subgraph: operation.subgraph,
        operation: operation.query,
        variables: operation.variables,
      };
      
      if (operation.dependencies.length > 0) {
        plan.sequences.push({
          dependsOn: operation.dependencies,
          fetch,
        });
      } else {
        plan.parallel.push(fetch);
      }
    }

    return plan;
  }

  optimizePlan(plan) {
    // Merge compatible fetches
    const optimized = this.mergeFetches(plan);
    
    // Eliminate redundant fetches
    const deduplicated = this.deduplicateFetches(optimized);
    
    return deduplicated;
  }
}
```

### DataLoader Configuration
```javascript
// Advanced DataLoader configuration
class DataLoaderManager {
  constructor(config) {
    this.loaders = new Map();
    this.config = config;
  }

  getLoader(name, batchFn) {
    if (!this.loaders.has(name)) {
      const loader = new DataLoader(batchFn, {
        maxBatchSize: this.config.maxBatchSize || 100,
        cache: this.config.cache !== false,
        cacheKeyFn: this.config.cacheKeyFn || (key => JSON.stringify(key)),
        batchScheduleFn: this.config.batchScheduleFn || (cb => setTimeout(cb, 0)),
      });
      
      this.loaders.set(name, {
        loader,
        metrics: {
          loads: 0,
          batches: 0,
          cacheHits: 0,
        },
      });
    }
    
    const loaderInfo = this.loaders.get(name);
    const originalLoad = loaderInfo.loader.load.bind(loaderInfo.loader);
    
    loaderInfo.loader.load = async (key) => {
      loaderInfo.metrics.loads++;
      return originalLoad(key);
    };
    
    return loaderInfo.loader;
  }

  getMetrics() {
    const metrics = {};
    for (const [name, info] of this.loaders) {
      metrics[name] = {
        loads: info.metrics.loads,
        batches: info.metrics.batches,
        cacheHits: info.metrics.cacheHits,
        hitRate: info.metrics.loads > 0 
          ? info.metrics.cacheHits / info.metrics.loads 
          : 0,
      };
    }
    return metrics;
  }
}
```

### Caching Strategies
```javascript
// Federation caching strategies
class FederationCache {
  constructor(config) {
    this.entityCache = new EntityCache(config.entityCache);
    this.responseCache = new ResponseCache(config.responseCache);
    this.plannerCache = new PlannerCache(config.plannerCache);
  }

  async cacheEntity(typeName, representation, data) {
    const key = `entity:${typeName}:${JSON.stringify(representation)}`;
    await this.entityCache.set(key, data, {
      ttl: this.config.entityTTL || 300000,
      tags: [`type:${typeName}`],
    });
  }

  async getCachedResponse(query, variables) {
    const key = `response:${hash(query)}:${hash(variables)}`;
    return this.responseCache.get(key);
  }

  async setCachedResponse(query, variables, response) {
    const key = `response:${hash(query)}:${hash(variables)}`;
    await this.responseCache.set(key, response, {
      ttl: this.config.responseTTL || 60000,
    });
  }

  async invalidateType(typeName) {
    await this.entityCache.invalidateByTag(`type:${typeName}`);
  }
}
```

## Security Considerations

### Authentication and Authorization
```javascript
// Federation authentication
class FederationAuth {
  constructor(config) {
    this.authService = config.authService;
    this.tokenValidator = config.tokenValidator;
  }

  async authenticateRequest(request) {
    const token = request.headers.authorization?.split(' ')[1];
    if (!token) {
      throw new AuthenticationError('No token provided');
    }

    const user = await this.tokenValidator.validate(token);
    if (!user) {
      throw new AuthenticationError('Invalid token');
    }

    return {
      user,
      permissions: await this.authService.getPermissions(user.id),
    };
  }

  async authorizeOperation(operation, context) {
    const requiredPermissions = this.getRequiredPermissions(operation);
    const userPermissions = context.permissions;
    
    for (const permission of requiredPermissions) {
      if (!userPermissions.includes(permission)) {
        throw new ForbiddenError(`Missing permission: ${permission}`);
      }
    }
    
    return true;
  }

  getRequiredPermissions(operation) {
    // Map operation to required permissions
    const permissionMap = {
      'Query.user': ['read:users'],
      'Query.users': ['read:users'],
      'Mutation.createUser': ['write:users'],
      'Mutation.updateUser': ['write:users'],
      'Mutation.deleteUser': ['delete:users'],
    };
    
    return permissionMap[operation] || [];
  }
}
```

### Rate Limiting
```javascript
// Federation rate limiting
class FederationRateLimiter {
  constructor(config) {
    this.limiter = new RateLimiter(config);
    this.subgraphLimiters = new Map();
  }

  async checkLimit(clientId, operation, subgraphs) {
    // Check overall rate limit
    const overallAllowed = await this.limiter.checkLimit(clientId);
    if (!overallAllowed) {
      throw new RateLimitError('Overall rate limit exceeded');
    }

    // Check per-subgraph rate limits
    for (const subgraph of subgraphs) {
      const subgraphLimiter = this.getSubgraphLimiter(subgraph);
      const allowed = await subgraphLimiter.checkLimit(clientId);
      if (!allowed) {
        throw new RateLimitError(`Rate limit exceeded for subgraph: ${subgraph}`);
      }
    }

    return true;
  }

  getSubgraphLimiter(subgraph) {
    if (!this.subgraphLimiters.has(subgraph)) {
      this.subgraphLimiters.set(subgraph, new RateLimiter({
        maxRequests: this.config.subgraphLimits?.[subgraph] || 100,
        windowMs: this.config.windowMs || 60000,
      }));
    }
    return this.subgraphLimiters.get(subgraph);
  }
}
```

### Input Validation
```javascript
// Federation input validation
class InputValidator {
  constructor(schema) {
    this.schema = schema;
    this.validators = new Map();
  }

  validate(operation, variables) {
    const validator = this.validators.get(operation);
    if (!validator) {
      throw new Error(`No validator for operation: ${operation}`);
    }

    const errors = validator(variables);
    if (errors.length > 0) {
      throw new ValidationError('Input validation failed', errors);
    }

    return true;
  }

  registerValidator(operation, validatorFn) {
    this.validators.set(operation, validatorFn);
  }
}

// Example validators
const validators = {
  createUser: (input) => {
    const errors = [];
    if (!input.name || input.name.length < 2) {
      errors.push({ field: 'name', message: 'Name must be at least 2 characters' });
    }
    if (!input.email || !isValidEmail(input.email)) {
      errors.push({ field: 'email', message: 'Invalid email format' });
    }
    return errors;
  },
};
```

## Troubleshooting Guide

### Common Federation Issues

#### Schema Composition Errors
```javascript
// Debugging schema composition
class CompositionDebugger {
  constructor() {
    this.logs = [];
  }

  async debugComposition(subgraphs) {
    const steps = [
      { name: 'validate', fn: () => this.validateSubgraphs(subgraphs) },
      { name: 'compose', fn: () => this.composeSchemas(subgraphs) },
      { name: 'validate_composition', fn: (result) => this.validateComposition(result) },
      { name: 'optimize', fn: (result) => this.optimizeSchema(result) },
    ];

    let result = null;
    for (const step of steps) {
      try {
        this.log(`Starting step: ${step.name}`);
        result = await step.fn(result);
        this.log(`Completed step: ${step.name}`);
      } catch (error) {
        this.log(`Failed step: ${step.name}`, error);
        throw error;
      }
    }

    return result;
  }

  log(message, error = null) {
    this.logs.push({
      timestamp: new Date(),
      message,
      error: error?.message,
    });
  }
}
```

#### Entity Resolution Failures
```javascript
// Debugging entity resolution
class EntityResolverDebugger {
  constructor(resolver) {
    this.resolver = resolver;
    this.traces = [];
  }

  async debugResolve(typeName, representation) {
    const trace = {
      typeName,
      representation,
      startTime: Date.now(),
      steps: [],
    };

    try {
      // Check cache
      const cacheStart = Date.now();
      const cached = await this.resolver.cache.get(typeName, representation);
      trace.steps.push({
        name: 'cache_check',
        duration: Date.now() - cacheStart,
        hit: cached !== null,
      });

      if (cached) {
        trace.endTime = Date.now();
        this.traces.push(trace);
        return cached;
      }

      // Resolve entity
      const resolveStart = Date.now();
      const entity = await this.resolver.resolveEntity(typeName, representation);
      trace.steps.push({
        name: 'resolve',
        duration: Date.now() - resolveStart,
        found: entity !== null,
      });

      trace.endTime = Date.now();
      this.traces.push(trace);
      return entity;
    } catch (error) {
      trace.error = error.message;
      trace.endTime = Date.now();
      this.traces.push(trace);
      throw error;
    }
  }
}
```

### Performance Debugging
```javascript
// Performance debugging tools
class PerformanceDebugger {
  constructor() {
    this.metrics = new Map();
  }

  async measureOperation(name, operation) {
    const start = Date.now();
    const result = await operation();
    const duration = Date.now() - start;

    this.recordMetric(name, duration);
    return result;
  }

  recordMetric(name, duration) {
    if (!this.metrics.has(name)) {
      this.metrics.set(name, {
        count: 0,
        totalDuration: 0,
        maxDuration: 0,
        minDuration: Infinity,
      });
    }

    const metric = this.metrics.get(name);
    metric.count++;
    metric.totalDuration += duration;
    metric.maxDuration = Math.max(metric.maxDuration, duration);
    metric.minDuration = Math.min(metric.minDuration, duration);
  }

  getMetrics() {
    const result = {};
    for (const [name, metric] of this.metrics) {
      result[name] = {
        ...metric,
        averageDuration: metric.totalDuration / metric.count,
      };
    }
    return result;
  }
}
```

## API Reference

### Federation Schema API
```graphql
# Federation schema types
type FederationConfig {
  version: String!
  subgraphs: [SubgraphConfig!]!
  router: RouterConfig
}

type SubgraphConfig {
  name: String!
  routingUrl: String!
  schemaUrl: String!
  introspection: Boolean!
  timeout: Int
  retry: RetryConfig
}

type RouterConfig {
  listen: String!
  introspection: Boolean!
  playground: Boolean!
  healthCheck: Boolean!
}

type RetryConfig {
  maxAttempts: Int!
  initialDelay: Int!
  maxDelay: Int!
}

# Entity resolution types
type EntityRepresentation {
  __typename: String!
  key: String!
  fields: [EntityField!]!
}

type EntityField {
  name: String!
  value: String!
}

# Query plan types
type QueryPlan {
  fetches: [Fetch!]!
  sequences: [Sequence!]!
  parallel: [Fetch!]!
}

type Fetch {
  subgraph: String!
  operation: String!
  variables: JSON
}

type Sequence {
  dependsOn: [String!]!
  fetch: Fetch!
}
```

### Entity Resolution API
```javascript
// Entity resolution API
const entityResolvers = {
  User: {
    __resolveReference(reference, context) {
      // Resolve user by key
      return context.dataLoader.user.load(reference.id);
    },
  },
  Post: {
    __resolveReference(reference, context) {
      // Resolve post by key
      return context.dataLoader.post.load(reference.id);
    },
  },
};

// Entity resolution with context
async function resolveEntities(typeName, representations, context) {
  const loader = context.dataLoader[typeName.toLowerCase()];
  if (!loader) {
    throw new Error(`No loader for entity type: ${typeName}`);
  }

  return Promise.all(
    representations.map(rep => loader.load(rep))
  );
}
```

## Data Models

### Federation Data Model
```javascript
// Data model for federation configuration
class FederationModel {
  constructor() {
    this.subgraphs = new Map();
    this.entities = new Map();
    this.schema = null;
  }

  addSubgraph(name, config) {
    this.subgraphs.set(name, {
      name,
      ...config,
      status: 'connected',
      metrics: {
        requests: 0,
        errors: 0,
        latency: 0,
      },
    });
  }

  registerEntity(typeName, subgraph, keys) {
    if (!this.entities.has(typeName)) {
      this.entities.set(typeName, new Map());
    }
    
    this.entities.get(typeName).set(subgraph, {
      keys,
      resolver: null,
      cache: null,
    });
  }

  getEntityResolutionPath(typeName) {
    const entitySubgraphs = this.entities.get(typeName);
    if (!entitySubgraphs) {
      throw new Error(`Entity type not found: ${typeName}`);
    }

    return Array.from(entitySubgraphs.keys());
  }
}
```

### Query Plan Data Model
```javascript
// Data model for query plans
class QueryPlanModel {
  constructor() {
    this.plans = new Map();
    this.metrics = new Map();
  }

  generatePlan(query, variables) {
    const planId = this.generatePlanId(query, variables);
    
    if (this.plans.has(planId)) {
      return this.plans.get(planId);
    }

    const plan = {
      id: planId,
      query,
      variables,
      steps: [],
      estimatedCost: 0,
      createdAt: Date.now(),
    };

    // Analyze query and generate steps
    const analysis = this.analyzeQuery(query);
    for (const step of analysis.steps) {
      plan.steps.push({
        type: step.type,
        subgraph: step.subgraph,
        operation: step.operation,
        dependencies: step.dependencies,
      });
    }

    // Calculate estimated cost
    plan.estimatedCost = this.calculateCost(plan);

    // Cache plan
    this.plans.set(planId, plan);
    
    return plan;
  }

  analyzeQuery(query) {
    // Parse query and identify operations
    return {
      steps: [
        { type: 'fetch', subgraph: 'users', operation: 'getUser', dependencies: [] },
        { type: 'fetch', subgraph: 'posts', operation: 'getUserPosts', dependencies: ['users'] },
      ],
    };
  }

  calculateCost(plan) {
    let cost = 0;
    for (const step of plan.steps) {
      cost += this.getStepCost(step);
    }
    return cost;
  }
}
```

## Deployment Guide

### Docker Deployment
```dockerfile
# Dockerfile for Apollo Router
FROM apollo-router:latest

# Copy configuration
COPY router.yaml /etc/apollo/router.yaml

# Copy supergraph schema
COPY supergraph.graphql /etc/apollo/supergraph.graphql

# Expose ports
EXPOSE 4000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:9090/health || exit 1

# Start router
CMD ["apollo-router", "--config", "/etc/apollo/router.yaml", "--supergraph", "/etc/apollo/supergraph.graphql"]
```

### Kubernetes Deployment
```yaml
# kubernetes/federation-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apollo-router
spec:
  replicas: 3
  selector:
    matchLabels:
      app: apollo-router
  template:
    metadata:
      labels:
        app: apollo-router
    spec:
      containers:
      - name: router
        image: apollo-router:latest
        ports:
        - containerPort: 4000
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/apollo
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 9090
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 9090
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: apollo-router-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: apollo-router-config
data:
  router.yaml: |
    supergraph:
      listen: 0.0.0.0:4000
      introspection: false
    subgraphs:
      users:
        routing_url: http://users-service:4001/graphql
        schema:
          subgraph_url: http://users-service:4001/graphql
      posts:
        routing_url: http://posts-service:4002/graphql
        schema:
          subgraph_url: http://posts-service:4002/graphql
```

### CI/CD Pipeline
```yaml
# .github/workflows/federation-deploy.yml
name: Deploy Federation

on:
  push:
    branches: [main]
    paths:
      - 'supergraph/**'
      - 'subgraphs/**'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run schema checks
      run: npm run schema:check
    
    - name: Build subgraphs
      run: npm run build:subgraphs
    
    - name: Compose supergraph
      run: npm run compose:supergraph
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/
        kubectl rollout status deployment/apollo-router
```

## Monitoring & Observability

### Metrics Collection
```javascript
// Federation metrics collection
const promClient = require('prom-client');

const federationMetrics = {
  requests: new promClient.Counter({
    name: 'federation_requests_total',
    help: 'Total number of federation requests',
    labelNames: ['subgraph', 'operation', 'status'],
  }),

  latency: new promClient.Histogram({
    name: 'federation_request_duration_seconds',
    help: 'Duration of federation requests',
    labelNames: ['subgraph', 'operation'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
  }),

  entityResolution: new promClient.Counter({
    name: 'federation_entity_resolution_total',
    help: 'Total number of entity resolutions',
    labelNames: ['type', 'subgraph', 'status'],
  }),

  queryPlanDuration: new promClient.Histogram({
    name: 'federation_query_plan_duration_seconds',
    help: 'Duration of query planning',
    buckets: [0.001, 0.005, 0.01, 0.05, 0.1],
  }),
};
```

### Logging Configuration
```javascript
// Structured logging for federation
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'apollo-router' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'federation.log' }),
  ],
});

// Request logging middleware
const requestLogger = {
  async requestDidStart({ request }) {
    const start = Date.now();
    logger.info('Federation request started', {
      operationName: request.operationName,
      query: request.query,
      variables: request.variables,
    });

    return {
      async willSendResponse({ response }) {
        const duration = Date.now() - start;
        logger.info('Federation request completed', {
          operationName: request.operationName,
          duration,
          status: response.errors ? 'error' : 'success',
          errors: response.errors?.map(e => e.message),
        });
      },
    };
  },
};
```

### Distributed Tracing
```javascript
// Distributed tracing implementation
const { trace, context, SpanKind, SpanStatusCode } = require('@opentelemetry/api');

class FederationTracer {
  constructor() {
    this.tracer = trace.getTracer('federation');
  }

  async traceOperation(operationName, operation) {
    const span = this.tracer.startSpan(operationName, {
      kind: SpanKind.SERVER,
      attributes: {
        'federation.operation': operationName,
      },
    });

    try {
      const result = await operation();
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error.message,
      });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  }

  async traceSubgraphCall(subgraph, operation) {
    const span = this.tracer.startSpan(`subgraph.${subgraph}`, {
      kind: SpanKind.CLIENT,
      attributes: {
        'federation.subgraph': subgraph,
      },
    });

    try {
      const result = await operation();
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error.message,
      });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  }
}
```

## Testing Strategy

### Integration Testing
```javascript
// Federation integration tests
describe('Federation Integration', () => {
  let gateway;
  let subgraphs;

  beforeAll(async () => {
    // Start subgraphs
    subgraphs = await startSubgraphs();
    
    // Create gateway
    gateway = new ApolloGateway({
      serviceList: Object.entries(subgraphs).map(([name, url]) => ({
        name,
        url,
      })),
    });
  });

  afterAll(async () => {
    await gateway.stop();
    await stopSubgraphs(subgraphs);
  });

  test('resolves cross-service queries', async () => {
    const query = `
      query GetUserWithPosts($userId: ID!) {
        user(id: $userId) {
          id
          name
          posts {
            id
            title
          }
        }
      }
    `;

    const result = await gateway.executeOperation({
      query,
      variables: { userId: '1' },
    });

    expect(result.errors).toBeUndefined();
    expect(result.data.user).toBeDefined();
    expect(result.data.user.posts).toBeDefined();
  });

  test('handles entity resolution errors', async () => {
    const query = `
      query GetUserWithInvalidPosts($userId: ID!) {
        user(id: $userId) {
          id
          posts {
            id
            invalidField
          }
        }
      }
    `;

    const result = await gateway.executeOperation({
      query,
      variables: { userId: '1' },
    });

    expect(result.errors).toBeDefined();
  });
});
```

### Performance Testing
```javascript
// Federation performance tests
describe('Federation Performance', () => {
  test('handles high concurrency', async () => {
    const concurrentRequests = 100;
    const promises = [];

    for (let i = 0; i < concurrentRequests; i++) {
      promises.push(
        gateway.executeOperation({
          query: `query { user(id: "${i}") { id name } }`,
        })
      );
    }

    const results = await Promise.all(promises);
    const errors = results.filter(r => r.errors);
    
    expect(errors.length).toBe(0);
  });

  test('maintains performance under load', async () => {
    const iterations = 1000;
    const latencies = [];

    for (let i = 0; i < iterations; i++) {
      const start = Date.now();
      await gateway.executeOperation({
        query: `query { user(id: "1") { id name } }`,
      });
      latencies.push(Date.now() - start);
    }

    const p95 = latencies.sort((a, b) => a - b)[Math.floor(iterations * 0.95)];
    expect(p95).toBeLessThan(1000); // 1 second P95
  });
});
```

### Schema Testing
```javascript
// Schema composition tests
describe('Schema Composition', () => {
  test('composes valid schemas', async () => {
    const subgraphs = [
      {
        name: 'users',
        typeDefs: gql`
          type User @key(fields: "id") {
            id: ID!
            name: String!
          }
        `,
      },
      {
        name: 'posts',
        typeDefs: gql`
          type Post @key(fields: "id") {
            id: ID!
            title: String!
            author: User!
          }
          
          extend type User @key(fields: "id") {
            id: ID! @external
            posts: [Post!]!
          }
        `,
      },
    ];

    const result = composeServices(subgraphs);
    expect(result.errors).toBeUndefined();
    expect(result.schema).toBeDefined();
  });

  test('catches composition errors', async () => {
    const subgraphs = [
      {
        name: 'users',
        typeDefs: gql`
          type User @key(fields: "id") {
            id: ID!
            name: String!
          }
        `,
      },
      {
        name: 'posts',
        typeDefs: gql`
          type Post @key(fields: "id") {
            id: ID!
            title: String!
            author: User!
          }
          
          # Missing @external on User.id
          extend type User @key(fields: "id") {
            id: ID!
            posts: [Post!]!
          }
        `,
      },
    ];

    const result = composeServices(subgraphs);
    expect(result.errors).toBeDefined();
  });
});
```

## Versioning & Migration

### Schema Versioning
```javascript
// Schema versioning strategy
class SchemaVersionManager {
  constructor() {
    this.versions = new Map();
    this.deprecations = new Map();
  }

  registerVersion(subgraph, version, schema) {
    if (!this.versions.has(subgraph)) {
      this.versions.set(subgraph, new Map());
    }
    this.versions.get(subgraph).set(version, schema);
  }

  deprecateVersion(subgraph, version, replacementVersion) {
    const key = `${subgraph}:${version}`;
    this.deprecations.set(key, {
      replacement: replacementVersion,
      deprecatedAt: new Date(),
      migrationGuide: `Migrate from ${version} to ${replacementVersion}`,
    });
  }

  getVersion(subgraph, version) {
    const schema = this.versions.get(subgraph)?.get(version);
    const deprecation = this.deprecations.get(`${subgraph}:${version}`);
    
    return {
      schema,
      deprecated: !!deprecation,
      replacement: deprecation?.replacement,
      migrationGuide: deprecation?.migrationGuide,
    };
  }

  async migrateSchema(subgraph, fromVersion, toVersion) {
    const fromSchema = this.getVersion(subgraph, fromVersion);
    const toSchema = this.getVersion(subgraph, toVersion);
    
    if (!fromSchema.schema || !toSchema.schema) {
      throw new Error('Schema versions not found');
    }

    const migration = new SchemaMigration(fromSchema.schema, toSchema.schema);
    return migration.migrate();
  }
}
```

### Migration Strategies
```javascript
// Migration strategy for federation changes
class FederationMigration {
  constructor(config) {
    this.config = config;
    this.steps = [];
  }

  async migrate(fromConfig, toConfig) {
    // Analyze changes
    const changes = this.analyzeChanges(fromConfig, toConfig);
    
    // Generate migration steps
    this.steps = this.generateMigrationSteps(changes);
    
    // Execute migration
    for (const step of this.steps) {
      await this.executeStep(step);
    }
    
    return {
      success: true,
      steps: this.steps,
      duration: Date.now() - this.startTime,
    };
  }

  analyzeChanges(fromConfig, toConfig) {
    const changes = {
      addedSubgraphs: [],
      removedSubgraphs: [],
      modifiedSubgraphs: [],
      addedEntities: [],
      removedEntities: [],
    };

    // Compare subgraphs
    const fromSubgraphs = new Set(Object.keys(fromConfig.subgraphs));
    const toSubgraphs = new Set(Object.keys(toConfig.subgraphs));

    for (const subgraph of toSubgraphs) {
      if (!fromSubgraphs.has(subgraph)) {
        changes.addedSubgraphs.push(subgraph);
      } else {
        changes.modifiedSubgraphs.push(subgraph);
      }
    }

    for (const subgraph of fromSubgraphs) {
      if (!toSubgraphs.has(subgraph)) {
        changes.removedSubgraphs.push(subgraph);
      }
    }

    return changes;
  }

  generateMigrationSteps(changes) {
    const steps = [];

    // Add new subgraphs
    for (const subgraph of changes.addedSubgraphs) {
      steps.push({
        type: 'add_subgraph',
        subgraph,
        action: 'deploy',
      });
    }

    // Remove old subgraphs
    for (const subgraph of changes.removedSubgraphs) {
      steps.push({
        type: 'remove_subgraph',
        subgraph,
        action: 'undeploy',
      });
    }

    return steps;
  }

  async executeStep(step) {
    switch (step.type) {
      case 'add_subgraph':
        await this.addSubgraph(step.subgraph);
        break;
      case 'remove_subgraph':
        await this.removeSubgraph(step.subgraph);
        break;
      default:
        throw new Error(`Unknown step type: ${step.type}`);
    }
  }
}
```

## Glossary

### Federation Terms

- **Supergraph**: The unified GraphQL schema composed from multiple subgraphs
- **Subgraph**: An individual GraphQL service that owns specific types and fields
- **Entity**: A type that can be referenced and resolved across multiple subgraphs
- **@key**: Directive that defines how to uniquely identify an entity
- **@external**: Directive marking a field as owned by another subgraph
- **@requires**: Directive specifying field dependencies
- **@provides**: Directive indicating fields this subgraph can provide
- **Query Plan**: The execution plan for resolving a federated query
- **Entity Resolution**: The process of fetching entity data from the owning subgraph
- **Composition**: The process of merging subgraph schemas into a supergraph

### Architecture Terms

- **Gateway**: The entry point that routes queries to appropriate subgraphs
- **Router**: The component that executes query plans across subgraphs
- **Federation Protocol**: The communication protocol between router and subgraphs
- **Schema Registry**: Service for storing and versioning schemas
- **Schema Composition**: Merging multiple schemas into a unified schema

## Changelog

### Version 2.0.0 (2024-01-15)
- Added advanced configuration section
- Added architecture patterns
- Added integration guide
- Added performance optimization techniques
- Added security considerations
- Added troubleshooting guide

### Version 1.0.0 (2024-01-01)
- Initial release
- Supergraph architecture
- Entity resolution
- @key/@external directives
- Subgraph communication

## Contributing Guidelines

### Development Setup
1. Clone the repository
2. Install dependencies: `npm install`
3. Start development environment: `docker-compose up`
4. Run tests: `npm test`
5. Run schema checks: `npm run schema:check`

### Code Standards
- Use TypeScript for new implementations
- Follow Apollo Federation best practices
- Write comprehensive tests
- Update documentation for changes

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Run schema composition checks
4. Update documentation
5. Submit pull request with description
6. Address review feedback

## License

MIT License

Copyright (c) 2024 Apollo Federation Team

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