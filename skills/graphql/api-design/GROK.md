---
name: GraphQL API Design
category: graphql
version: 1.0.0
tags: [graphql, api-design, schema, mutations, pagination, performance]
difficulty: intermediate
estimated_time: 45 minutes
prerequisites: [basic-graphql, rest-api-concepts]
---

# GraphQL API Design

## Overview

GraphQL API design encompasses schema best practices, mutation patterns, cursor-based pagination, and N+1 query prevention. This skill provides a comprehensive guide to building robust, scalable GraphQL APIs.

## Core Concepts

### 1. Schema Design Principles

**Naming Conventions:**
- Types: `PascalCase` (e.g., `User`, `Post`)
- Fields: `camelCase` (e.g., `createdAt`, `userProfile`)
- Enums: `SCREAMING_SNAKE_CASE` (e.g., `POST_STATUS`)
- Mutations: Verb + Noun (e.g., `createUser`, `updatePost`)

**Type Relationships:**
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  status: PostStatus!
  createdAt: DateTime!
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}
```

### 2. Mutation Patterns

**Input Types:**
```graphql
input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

input UpdatePostInput {
  title: String
  content: String
  status: PostStatus
}

type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}
```

**Mutation Structure:**
```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}
```

### 3. Cursor-Based Pagination

**Connection Pattern:**
```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
    filter: UserFilter
  ): UserConnection!
}
```

### 4. N+1 Query Prevention

**DataLoader Pattern:**
```python
class UserDataLoader:
    def __init__(self, db):
        self.db = db
        self.cache = {}
    
    async def load(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]
        
        user = await self.db.get_user(user_id)
        self.cache[user_id] = user
        return user
    
    async def load_many(self, user_ids):
        users = await self.db.get_users_by_ids(user_ids)
        for user in users:
            self.cache[user.id] = user
        return [self.cache[uid] for uid in user_ids]
```

## Implementation Guide

### Step 1: Schema Definition

1. Define core types with clear relationships
2. Use input types for mutations
3. Implement connection pattern for pagination
4. Add custom scalars for complex types

### Step 2: Resolver Implementation

1. Implement query resolvers with DataLoader
2. Add mutation resolvers with validation
3. Handle errors consistently
4. Add authentication/authorization

### Step 3: Performance Optimization

1. Implement query complexity analysis
2. Add persisted queries
3. Use response caching
4. Monitor and optimize slow queries

## Common Patterns

### Error Handling
```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  AUTHENTICATION_ERROR
  NOT_FOUND
  CONFLICT
}
```

### Field Arguments
```graphql
type Query {
  user(id: ID!): User
  users(
    first: Int
    after: String
    filter: UserFilter
    sort: UserSort
  ): UserConnection!
}

input UserFilter {
  name: String
  email: String
  status: UserStatus
}

input UserSort {
  field: UserSortField!
  direction: SortDirection!
}

enum UserSortField {
  NAME
  EMAIL
  CREATED_AT
}

enum SortDirection {
  ASC
  DESC
}
```

## Best Practices

1. **Use descriptive type names** - Avoid abbreviations
2. **Implement consistent error handling** - Use union types for errors
3. **Add deprecation notices** - Use `@deprecated` directive
4. **Version your schema** - Use schema versioning strategy
5. **Document everything** - Add descriptions to types and fields
6. **Use input types** - For complex mutations
7. **Implement pagination** - Use connection pattern
8. **Prevent N+1** - Use DataLoader pattern
9. **Validate inputs** - Add custom validation rules
10. **Monitor performance** - Track query complexity

## Tools and Libraries

- **Apollo Server** - GraphQL server implementation
- **GraphQL Yoga** - Feature-rich GraphQL HTTP library
- **Prisma** - Database toolkit and ORM
- **DataLoader** - Batching and caching library
- **GraphQL Code Generator** - Generate TypeScript types

## Common Pitfalls

1. **Over-fetching** - Requesting too much data
2. **Under-fetching** - Not requesting enough data
3. **N+1 queries** - Multiple database queries
4. **Missing validation** - No input validation
5. **Inconsistent errors** - Different error formats
6. **No pagination** - Loading all records at once
7. **Ignoring security** - No query complexity limits

## Advanced Topics

### Custom Scalars
```graphql
scalar DateTime
scalar JSON
scalar URL
scalar Email
```

### Directives
```graphql
directive @deprecated(reason: String) on FIELD_DEFINITION
directive @auth(requires: Role!) on FIELD_DEFINITION
directive @cacheControl(maxAge: Int!) on FIELD_DEFINITION
```

### Interfaces
```graphql
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type User implements Node & Timestamped {
  id: ID!
  name: String!
  createdAt: DateTime!
  updatedAt: DateTime!
}
```

## Summary

GraphQL API design requires careful consideration of schema structure, mutation patterns, pagination, and performance. By following these patterns and best practices, you can create robust, scalable APIs that provide excellent developer experience.

## Advanced Configuration

### Schema Configuration
```javascript
// Advanced schema configuration
const schemaConfig = {
  typeDefs: `
    scalar DateTime
    scalar JSON
    scalar URL
    
    directive @auth(requires: Role!) on FIELD_DEFINITION
    directive @cacheControl(maxAge: Int!) on FIELD_DEFINITION
    directive @deprecated(reason: String) on FIELD_DEFINITION
    
    type Query {
      me: User!
      user(id: ID!): User
      users(
        first: Int
        after: String
        filter: UserFilter
        sort: UserSort
      ): UserConnection!
    }
    
    type Mutation {
      createUser(input: CreateUserInput!): CreateUserPayload!
      updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
      deleteUser(id: ID!): DeleteUserPayload!
    }
  `,
  resolvers: {
    DateTime: DateTimeResolver,
    JSON: JSONResolver,
    URL: URLResolver,
  },
  validationRules: [
    depthLimit(10),
    createComplexityRule({
      maximumComplexity: 1000,
      estimators: [
        fieldExtensionsEstimator(),
        simpleEstimator({ defaultComplexity: 1 }),
      ],
    }),
  ],
};
```

### Authentication Configuration
```javascript
// Authentication configuration
const authConfig = {
  providers: {
    jwt: {
      secret: process.env.JWT_SECRET,
      expiresIn: '7d',
    },
    oauth: {
      github: {
        clientId: process.env.GITHUB_CLIENT_ID,
        clientSecret: process.env.GITHUB_CLIENT_SECRET,
      },
    },
  },
  permissions: {
    User: {
      '*': isAuthenticated,
      email: isOwner,
      posts: isAuthenticated,
    },
    Mutation: {
      '*': isAuthenticated,
      createUser: isPublic,
    },
  },
};
```

### Rate Limiting Configuration
```javascript
// Rate limiting configuration
const rateLimitConfig = {
  default: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100,
  },
  queries: {
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 30,
  },
  mutations: {
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 10,
  },
  subscriptions: {
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 5,
  },
};
```

## Architecture Patterns

### Schema-First Architecture
```javascript
// Schema-first architecture pattern
class SchemaFirstArchitect {
  constructor() {
    this.schema = null;
    this.resolvers = new Map();
    this.typeDefs = new Map();
  }

  async buildSchema() {
    // Load all type definitions
    const typeDefs = await this.loadTypeDefs();
    
    // Load all resolvers
    const resolvers = await this.loadResolvers();
    
    // Build executable schema
    this.schema = makeExecutableSchema({
      typeDefs,
      resolvers,
      schemaDirectives: {
        auth: AuthDirective,
        cacheControl: CacheControlDirective,
      },
    });
    
    return this.schema;
  }

  async loadTypeDefs() {
    const typeDefs = [];
    for (const [name, typeDef] of this.typeDefs) {
      typeDefs.push(typeDef);
    }
    return typeDefs;
  }

  async loadResolvers() {
    const resolvers = {};
    for (const [path, resolver] of this.resolvers) {
      const parts = path.split('.');
      let current = resolvers;
      
      for (let i = 0; i < parts.length - 1; i++) {
        if (!current[parts[i]]) {
          current[parts[i]] = {};
        }
        current = current[parts[i]];
      }
      
      current[parts[parts.length - 1]] = resolver;
    }
    return resolvers;
  }
}
```

### Code-First Architecture
```javascript
// Code-first architecture pattern
class CodeFirstArchitect {
  constructor() {
    this.types = new Map();
    this.fields = new Map();
    this.queries = new Map();
    this.mutations = new Map();
  }

  addType(name, definition) {
    this.types.set(name, definition);
  }

  addField(typeName, fieldName, definition) {
    const key = `${typeName}.${fieldName}`;
    this.fields.set(key, definition);
  }

  addQuery(fieldName, definition) {
    this.queries.set(fieldName, definition);
  }

  addMutation(fieldName, definition) {
    this.mutations.set(fieldName, definition);
  }

  buildSchema() {
    const typeDefs = this.generateTypeDefs();
    const resolvers = this.generateResolvers();
    
    return makeExecutableSchema({ typeDefs, resolvers });
  }

  generateTypeDefs() {
    let typeDefs = '';
    
    // Generate types
    for (const [name, definition] of this.types) {
      typeDefs += `type ${name} {\n`;
      
      // Add fields
      for (const [fieldName, fieldDef] of this.fields) {
        if (fieldName.startsWith(name + '.')) {
          typeDefs += `  ${fieldName.split('.')[1]}: ${fieldDef.type}\n`;
        }
      }
      
      typeDefs += '}\n\n';
    }
    
    // Generate Query type
    typeDefs += 'type Query {\n';
    for (const [fieldName, fieldDef] of this.queries) {
      typeDefs += `  ${fieldName}(${fieldDef.args || ''}): ${fieldDef.type}\n`;
    }
    typeDefs += '}\n\n';
    
    // Generate Mutation type
    typeDefs += 'type Mutation {\n';
    for (const [fieldName, fieldDef] of this.mutations) {
      typeDefs += `  ${fieldName}(${fieldDef.args || ''}): ${fieldDef.type}\n`;
    }
    typeDefs += '}\n';
    
    return typeDefs;
  }

  generateResolvers() {
    const resolvers = {
      Query: {},
      Mutation: {},
    };
    
    for (const [fieldName, fieldDef] of this.queries) {
      resolvers.Query[fieldName] = fieldDef.resolve;
    }
    
    for (const [fieldName, fieldDef] of this.mutations) {
      resolvers.Mutation[fieldName] = fieldDef.resolve;
    }
    
    return resolvers;
  }
}
```

### Hybrid Architecture
```javascript
// Hybrid architecture pattern
class HybridArchitect {
  constructor() {
    this.schemaFirst = new SchemaFirstArchitect();
    this.codeFirst = new CodeFirstArchitect();
    this.stitcher = new SchemaStitcher();
  }

  async buildSchema() {
    // Build schemas from both approaches
    const schemaFirstSchema = await this.schemaFirst.buildSchema();
    const codeFirstSchema = this.codeFirst.buildSchema();
    
    // Stitch schemas together
    const stitchedSchema = await this.stitcher.stitch([
      schemaFirstSchema,
      codeFirstSchema,
    ]);
    
    return stitchedSchema;
  }
}
```

## Integration Guide

### Apollo Server Integration
```javascript
// Apollo Server integration
const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { all: true },
    }),
    ApolloServerPluginCacheControl({ defaultMaxAge: 5 }),
  ],
  validationRules: [
    depthLimit(10),
    createComplexityRule({
      maximumComplexity: 1000,
      estimators: [
        fieldExtensionsEstimator(),
        simpleEstimator({ defaultComplexity: 1 }),
      ],
    }),
  ],
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
});
```

### Express Integration
```javascript
// Express integration
const express = require('express');
const { graphqlHTTP } = require('express-graphql');

const app = express();

app.use('/graphql', graphqlHTTP({
  schema,
  graphiql: true,
  customFormatErrorFn: (error) => ({
    message: error.message,
    locations: error.locations,
    path: error.path,
    extensions: {
      code: error.extensions?.code,
      timestamp: new Date().toISOString(),
    },
  }),
}));
```

### Fastify Integration
```javascript
// Fastify integration
const fastify = require('fastify')({ logger: true });
const { Mercurius } = require('mercurius');

fastify.register(Mercurius, {
  schema,
  graphiql: true,
  context: (request, reply) => ({
    user: request.user,
    loaders: createLoaders(),
  }),
});
```

## Performance Optimization

### Query Optimization
```javascript
// Query optimization engine
class QueryOptimizer {
  constructor(schema) {
    this.schema = schema;
    this.cache = new QueryCache();
  }

  async optimizeQuery(query, variables) {
    const cacheKey = this.generateCacheKey(query, variables);
    
    // Check cache
    const cached = await this.cache.get(cacheKey);
    if (cached) {
      return cached;
    }

    // Analyze query
    const analysis = this.analyzeQuery(query);
    
    // Optimize execution
    const optimized = this.optimizeExecution(analysis);
    
    // Cache result
    await this.cache.set(cacheKey, optimized);
    
    return optimized;
  }

  analyzeQuery(query) {
    const document = parse(query);
    
    return {
      depth: this.calculateDepth(document),
      complexity: this.calculateComplexity(document),
      fields: this.extractFields(document),
    };
  }

  optimizeExecution(analysis) {
    // Optimize based on analysis
    return {
      ...analysis,
      optimized: true,
    };
  }
}
```

### DataLoader Implementation
```javascript
// Advanced DataLoader implementation
class AdvancedDataLoader {
  constructor(batchFn, options = {}) {
    this.batchFn = batchFn;
    this.cache = new Map();
    this.pending = new Map();
    this.maxBatchSize = options.maxBatchSize || 100;
    this.cacheKeyFn = options.cacheKeyFn || (key => key);
  }

  async load(key) {
    const cacheKey = this.cacheKeyFn(key);
    
    // Check cache
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }
    
    // Check pending batch
    if (this.pending.has(cacheKey)) {
      return this.pending.get(cacheKey);
    }
    
    // Create new batch
    const promise = new Promise((resolve, reject) => {
      this.pending.set(cacheKey, { resolve, reject, key });
      
      if (this.pending.size >= this.maxBatchSize) {
        this.processBatch();
      }
    });
    
    // Schedule batch processing
    setTimeout(() => this.processBatch(), 0);
    
    const result = await promise;
    this.cache.set(cacheKey, result);
    
    return result;
  }

  async processBatch() {
    const pending = Array.from(this.pending.entries());
    this.pending.clear();
    
    if (pending.length === 0) return;
    
    const keys = pending.map(([_, { key }]) => key);
    
    try {
      const results = await this.batchFn(keys);
      
      pending.forEach(([cacheKey, { resolve }], index) => {
        resolve(results[index]);
      });
    } catch (error) {
      pending.forEach(([_, { reject }]) => {
        reject(error);
      });
    }
  }
}
```

### Caching Strategy
```javascript
// Multi-level caching strategy
class MultiLevelCache {
  constructor() {
    this.levels = [
      new L1Cache({ maxSize: 1000, ttl: 60000 }), // In-memory
      new L2Cache({ maxSize: 10000, ttl: 300000 }), // Redis
      new L3Cache({ maxSize: 100000, ttl: 3600000 }), // Database
    ];
  }

  async get(key) {
    for (let i = 0; i < this.levels.length; i++) {
      const value = await this.levels[i].get(key);
      if (value) {
        // Promote to higher levels
        for (let j = 0; j < i; j++) {
          await this.levels[j].set(key, value);
        }
        return value;
      }
    }
    return null;
  }

  async set(key, value, ttl) {
    for (const level of this.levels) {
      await level.set(key, value, ttl);
    }
  }

  async invalidate(key) {
    for (const level of this.levels) {
      await level.delete(key);
    }
  }
}
```

## Security Considerations

### Authentication
```javascript
// Authentication middleware
class AuthenticationMiddleware {
  constructor(config) {
    this.config = config;
  }

  async authenticate(request) {
    const token = this.extractToken(request);
    if (!token) {
      throw new AuthenticationError('No token provided');
    }

    const user = await this.validateToken(token);
    if (!user) {
      throw new AuthenticationError('Invalid token');
    }

    return user;
  }

  extractToken(request) {
    const authHeader = request.headers.authorization;
    if (authHeader?.startsWith('Bearer ')) {
      return authHeader.slice(7);
    }
    return null;
  }

  async validateToken(token) {
    try {
      const decoded = jwt.verify(token, this.config.secret);
      return await this.loadUser(decoded.userId);
    } catch (error) {
      return null;
    }
  }
}
```

### Authorization
```javascript
// Authorization middleware
class AuthorizationMiddleware {
  constructor(permissions) {
    this.permissions = permissions;
  }

  async authorize(user, operation, context) {
    const permission = this.getPermission(operation);
    if (!permission) {
      return true; // No permission required
    }

    return permission(user, context);
  }

  getPermission(operation) {
    const parts = operation.split('.');
    let current = this.permissions;
    
    for (const part of parts) {
      if (current[part]) {
        current = current[part];
      } else if (current['*']) {
        return current['*'];
      } else {
        return null;
      }
    }
    
    return current;
  }
}
```

### Input Validation
```javascript
// Input validation middleware
class InputValidator {
  constructor(schema) {
    this.schema = schema;
  }

  validate(operation, variables) {
    const validator = this.getValidator(operation);
    if (!validator) {
      return true;
    }

    const errors = validator(variables);
    if (errors.length > 0) {
      throw new ValidationError('Input validation failed', errors);
    }

    return true;
  }

  getValidator(operation) {
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

    return validators[operation];
  }
}
```

## Troubleshooting Guide

### Common Issues

#### N+1 Query Problems
```javascript
// Debugging N+1 queries
class N1QueryDebugger {
  constructor() {
    this.queries = [];
  }

  async debugQuery(query, variables) {
    const queries = [];
    const originalExecute = this.schema.execute;
    
    this.schema.execute = async (document, variables) => {
      queries.push({
        query: print(document),
        variables,
        timestamp: Date.now(),
      });
      return originalExecute(document, variables);
    };

    await graphql(this.schema, query, null, {}, variables);
    
    this.queries = queries;
    return this.analyzeQueries(queries);
  }

  analyzeQueries(queries) {
    const grouped = {};
    
    for (const q of queries) {
      const table = this.extractTable(q.query);
      if (!grouped[table]) {
        grouped[table] = [];
      }
      grouped[table].push(q);
    }

    return {
      totalQueries: queries.length,
      queriesByTable: grouped,
      n1Detected: Object.values(grouped).some(qs => qs.length > 1),
    };
  }
}
```

#### Performance Issues
```javascript
// Performance debugging
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

### Schema API
```graphql
# Schema types
type SchemaConfig {
  typeDefs: String!
  resolvers: JSON
  directives: [Directive!]!
  validationRules: [String!]
}

type Schema {
  id: ID!
  name: String!
  typeDefs: String!
  resolvers: JSON
  createdAt: DateTime!
  updatedAt: DateTime!
  status: SchemaStatus!
}

enum SchemaStatus {
  ACTIVE
  DEPRECATED
  ARCHIVED
}

# Schema operations
type Query {
  schema(id: ID!): Schema
  schemas: [Schema!]!
  schemaVersion(version: String!): Schema
}

type Mutation {
  createSchema(input: CreateSchemaInput!): Schema!
  updateSchema(id: ID!, input: UpdateSchemaInput!): Schema!
  deleteSchema(id: ID!): Boolean!
  deploySchema(id: ID!): Schema!
}
```

### Type System API
```javascript
// Type system interface
class TypeSystemAPI {
  constructor(schema) {
    this.schema = schema;
    this.typeMap = schema.getTypeMap();
  }

  getType(typeName) {
    return this.typeMap[typeName];
  }

  getTypes() {
    return Object.keys(this.typeMap);
  }

  getFields(typeName) {
    const type = this.typeMap[typeName];
    if (!type) return null;
    
    return type.getFields();
  }

  getInputType(typeName) {
    const type = this.typeMap[typeName];
    if (!type || !type.getFields) return null;
    
    return type.getFields();
  }

  getEnumValues(typeName) {
    const type = this.typeMap[typeName];
    if (!type || !type.getValues) return null;
    
    return type.getValues();
  }
}
```

## Data Models

### Schema Data Model
```javascript
// Schema data model
class SchemaModel {
  constructor() {
    this.schemas = new Map();
    this.versions = new Map();
    this.deployments = new Map();
  }

  createSchema(data) {
    const schema = {
      id: generateId(),
      name: data.name,
      typeDefs: data.typeDefs,
      resolvers: data.resolvers,
      createdAt: new Date(),
      updatedAt: new Date(),
      status: 'ACTIVE',
      version: '1.0.0',
    };

    this.schemas.set(schema.id, schema);
    return schema;
  }

  updateSchema(id, updates) {
    const schema = this.schemas.get(id);
    if (!schema) {
      return null;
    }

    Object.assign(schema, updates, { updatedAt: new Date() });
    return schema;
  }

  deleteSchema(id) {
    return this.schemas.delete(id);
  }

  deploySchema(id) {
    const schema = this.schemas.get(id);
    if (!schema) {
      return null;
    }

    schema.status = 'DEPLOYED';
    schema.deployedAt = new Date();
    return schema;
  }
}
```

### Type Data Model
```javascript
// Type data model
class TypeModel {
  constructor() {
    this.types = new Map();
    this.fields = new Map();
    this.relationships = new Map();
  }

  addType(name, definition) {
    this.types.set(name, {
      name,
      ...definition,
      createdAt: new Date(),
    });
  }

  addField(typeName, fieldName, definition) {
    const key = `${typeName}.${fieldName}`;
    this.fields.set(key, {
      typeName,
      fieldName,
      ...definition,
    });
  }

  addRelationship(typeName, fieldName, relatedType) {
    const key = `${typeName}.${fieldName}`;
    this.relationships.set(key, {
      typeName,
      fieldName,
      relatedType,
      type: 'relationship',
    });
  }

  getFields(typeName) {
    return Array.from(this.fields.values())
      .filter(field => field.typeName === typeName);
  }

  getRelationships(typeName) {
    return Array.from(this.relationships.values())
      .filter(rel => rel.typeName === typeName);
  }
}
```

## Deployment Guide

### Docker Deployment
```dockerfile
# Dockerfile for GraphQL API
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV PORT=4000
ENV DATABASE_URL=postgresql://user:password@db:5432/graphql

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:4000/health || exit 1

# Start application
CMD ["node", "server.js"]
```

### Kubernetes Deployment
```yaml
# kubernetes/graphql-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graphql-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: graphql-api
  template:
    metadata:
      labels:
        app: graphql-api
    spec:
      containers:
      - name: graphql
        image: graphql-api:latest
        ports:
        - containerPort: 4000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: graphql-secrets
              key: database-url
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
            port: 4000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 4000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: graphql-api
spec:
  selector:
    app: graphql-api
  ports:
  - name: http
    port: 4000
    targetPort: 4000
  type: ClusterIP
```

## Monitoring & Observability

### Metrics Collection
```javascript
// GraphQL metrics collection
const promClient = require('prom-client');

const graphqlMetrics = {
  requests: new promClient.Counter({
    name: 'graphql_requests_total',
    help: 'Total GraphQL requests',
    labelNames: ['operation', 'status'],
  }),

  latency: new promClient.Histogram({
    name: 'graphql_request_duration_seconds',
    help: 'GraphQL request latency',
    labelNames: ['operation'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
  }),

  errors: new promClient.Counter({
    name: 'graphql_errors_total',
    help: 'Total GraphQL errors',
    labelNames: ['operation', 'error_code'],
  }),

  complexity: new promClient.Histogram({
    name: 'graphql_query_complexity',
    help: 'GraphQL query complexity',
    buckets: [10, 50, 100, 500, 1000],
  }),
};
```

### Logging Configuration
```javascript
// Structured logging
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'graphql-api' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'graphql.log' }),
  ],
});

// Request logging
const requestLogger = {
  async requestDidStart({ request }) {
    const start = Date.now();
    logger.info('GraphQL request started', {
      operationName: request.operationName,
      query: request.query,
    });

    return {
      async willSendResponse({ response }) {
        const duration = Date.now() - start;
        logger.info('GraphQL request completed', {
          operationName: request.operationName,
          duration,
          status: response.errors ? 'error' : 'success',
        });
      },
    };
  },
};
```

## Testing Strategy

### Unit Testing
```javascript
// Unit tests for GraphQL API
describe('GraphQL API', () => {
  let server;

  beforeAll(async () => {
    server = await createTestServer();
  });

  afterAll(async () => {
    await server.close();
  });

  test('fetches user by id', async () => {
    const query = `
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          email
        }
      }
    `;

    const result = await server.executeOperation({
      query,
      variables: { id: '1' },
    });

    expect(result.errors).toBeUndefined();
    expect(result.data.user).toBeDefined();
  });

  test('creates user', async () => {
    const mutation = `
      mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) {
          user {
            id
            name
            email
          }
          errors {
            field
            message
            code
          }
        }
      }
    `;

    const result = await server.executeOperation({
      query: mutation,
      variables: {
        input: {
          name: 'John Doe',
          email: 'john@example.com',
        },
      },
    });

    expect(result.errors).toBeUndefined();
    expect(result.data.createUser.user).toBeDefined();
  });
});
```

### Integration Testing
```javascript
// Integration tests
describe('GraphQL Integration', () => {
  test('resolves nested queries', async () => {
    const query = `
      query GetUserWithPosts($userId: ID!) {
        user(id: $userId) {
          id
          name
          posts {
            id
            title
            comments {
              id
              content
            }
          }
        }
      }
    `;

    const result = await graphql(schema, query, null, {}, { userId: '1' });
    
    expect(result.errors).toBeUndefined();
    expect(result.data.user.posts).toBeDefined();
  });

  test('handles pagination', async () => {
    const query = `
      query GetUsers($first: Int, $after: String) {
        users(first: $first, after: $after) {
          edges {
            node {
              id
              name
            }
            cursor
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    `;

    const result = await graphql(schema, query, null, {}, { first: 10 });
    
    expect(result.errors).toBeUndefined();
    expect(result.data.users.edges).toBeDefined();
  });
});
```

## Versioning & Migration

### Schema Versioning
```javascript
// Schema versioning
class SchemaVersionManager {
  constructor() {
    this.versions = new Map();
    this.deprecations = new Map();
  }

  registerVersion(version, schema) {
    this.versions.set(version, {
      schema,
      registeredAt: new Date(),
      status: 'active',
    });
  }

  deprecateVersion(version, replacementVersion) {
    const versionInfo = this.versions.get(version);
    if (!versionInfo) {
      throw new Error(`Version ${version} not found`);
    }

    versionInfo.status = 'deprecated';
    this.deprecations.set(version, {
      replacement: replacementVersion,
      deprecatedAt: new Date(),
    });
  }

  getVersion(version) {
    return this.versions.get(version);
  }

  getActiveVersions() {
    return Array.from(this.versions.entries())
      .filter(([_, info]) => info.status === 'active')
      .map(([version, _]) => version);
  }
}
```

### Migration Strategies
```javascript
// Migration strategy
class SchemaMigration {
  constructor(config) {
    this.config = config;
    this.steps = [];
  }

  async migrate(fromVersion, toVersion) {
    const fromSchema = this.getVersion(fromVersion);
    const toSchema = this.getVersion(toVersion);

    const changes = this.analyzeChanges(fromSchema, toSchema);
    this.steps = this.generateMigrationSteps(changes);

    for (const step of this.steps) {
      await this.executeStep(step);
    }

    return {
      success: true,
      steps: this.steps,
      duration: Date.now() - this.startTime,
    };
  }

  analyzeChanges(fromSchema, toSchema) {
    return {
      addedTypes: [],
      removedTypes: [],
      modifiedTypes: [],
      addedFields: [],
      removedFields: [],
    };
  }

  generateMigrationSteps(changes) {
    const steps = [];

    for (const type of changes.addedTypes) {
      steps.push({
        type: 'add_type',
        name: type,
        action: 'add',
      });
    }

    for (const type of changes.removedTypes) {
      steps.push({
        type: 'remove_type',
        name: type,
        action: 'remove',
      });
    }

    return steps;
  }
}
```

## Glossary

### API Design Terms

- **Schema**: The type system that defines the API structure
- **Resolver**: Function that fetches data for a field
- **Type**: Building block of the schema representing a data structure
- **Field**: Property of a type
- **Input Type**: Special type for mutation arguments
- **Enum**: Set of named values
- **Interface**: Abstract type defining a contract
- **Union**: Type that can be one of several types
- **Scalar**: Primitive type (String, Int, Float, Boolean, ID)
- **Directive**: Annotation that modifies type system behavior

### Performance Terms

- **N+1 Problem**: When a query triggers multiple database queries
- **DataLoader**: Library for batching and caching data requests
- **Query Complexity**: Numerical value representing query cost
- **Persisted Query**: Pre-registered query identified by hash
- **Connection Pattern**: Pagination pattern using edges and nodes

## Changelog

### Version 1.1.0 (2024-01-15)
- Added advanced configuration section
- Added architecture patterns
- Added integration guide
- Added performance optimization techniques
- Added security considerations
- Added troubleshooting guide

### Version 1.0.0 (2024-01-01)
- Initial release
- Schema design principles
- Mutation patterns
- Cursor-based pagination
- N+1 query prevention

## Contributing Guidelines

### Development Setup
1. Clone the repository
2. Install dependencies: `npm install`
3. Run tests: `npm test`
4. Start development server: `npm run dev`

### Code Standards
- Use TypeScript for new implementations
- Follow GraphQL best practices
- Write comprehensive tests
- Update documentation for changes

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Run schema validation
4. Update documentation
5. Submit pull request with description
6. Address review feedback

## License

MIT License

Copyright (c) 2024 GraphQL API Design Team

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