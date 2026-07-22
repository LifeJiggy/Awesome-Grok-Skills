---
name: Schema Stitching
category: graphql
version: 1.0.0
tags: [graphql, schema-stitching, type-merging, remote-schemas, federation]
difficulty: advanced
estimated_time: 60 minutes
prerequisites: [graphql-basics, schema-design]
---

# Schema Stitching

## Overview

Schema stitching is the process of combining multiple GraphQL schemas into a single, unified schema. This skill covers combining schemas, type merging, conflict resolution, and remote schema integration.

## Core Concepts

### 1. Schema Stitching Approaches

**Declarative Stitching:**
```graphql
# Schema A
type User {
  id: ID!
  name: String!
  email: String!
}

# Schema B
type User {
  id: ID!
  posts: [Post!]!
  profile: Profile
}

# Stitched Schema
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  profile: Profile
}
```

**Programmatic Stitching:**
```javascript
const { stitchSchemas } = require('@graphql-tools/stitch');

const stitchedSchema = stitchSchemas({
  subschemas: [schemaA, schemaB],
  typeMergingConfig: {
    User: {
      selectionSet: '{ id }',
      fieldName: 'userById',
      args: (originalObject) => ({ id: originalObject.id }),
    },
  },
});
```

### 2. Type Merging

**Basic Type Merging:**
```graphql
# Subschema 1: User Service
type User {
  id: ID!
  name: String!
  email: String!
}

# Subschema 2: User Profile Service
type User {
  id: ID!
  bio: String
  avatar: String
  settings: UserSettings
}

# Merged Type
type User {
  id: ID!
  name: String!
  email: String!
  bio: String
  avatar: String
  settings: UserSettings
}
```

**Computed Fields:**
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  # Computed field from multiple services
  fullName: String!
  postCount: Int!
}
```

### 3. Conflict Resolution

**Field Conflict Resolution:**
```graphql
# Conflict: Same field, different types
type User {
  id: ID!
  createdAt: String!  # Schema A: String
  # Schema B: DateTime
}

# Resolution: Use consistent type
type User {
  id: ID!
  createdAt: DateTime!  # Unified type
}
```

**Type Conflict Resolution:**
```graphql
# Conflict: Same type name, different structures
type Post {
  id: ID!
  title: String!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

# Resolution: Merge types
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}
```

### 4. Remote Schema Integration

**Remote Schema Configuration:**
```javascript
const { introspectSchema } = require('@graphql-tools/wrap');
const { fetch } = require('node-fetch');

const remoteExecutor = async ({ document, variables }) => {
  const query = print(document);
  const response = await fetch('https://api.example.com/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ query, variables }),
  });
  return response.json();
};

const remoteSchema = {
  schema: await introspectSchema(remoteExecutor),
  executor: remoteExecutor,
};
```

## Implementation Guide

### Step 1: Schema Analysis

1. Identify overlapping types
2. Map field relationships
3. Detect conflicts
4. Plan merging strategy

### Step 2: Schema Stitching Setup

1. Configure subschemas
2. Define type merging rules
3. Set up remote executors
4. Handle authentication

### Step 3: Type Merging Implementation

1. Define selection sets
2. Configure merge keys
3. Handle nested types
4. Resolve conflicts

### Step 4: Testing and Validation

1. Test merged schema
2. Validate resolvers
3. Check performance
4. Monitor errors

## Common Patterns

### Schema Splitting
```graphql
# User Schema
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

# Post Schema
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
}

# Comment Schema
type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
}
```

### Schema Merging
```graphql
# Merged Schema
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  comments: [Comment!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
}
```

### Remote Schema Integration
```javascript
// Schema A: User Service
const userSchema = makeExecutableSchema({
  typeDefs: `
    type User {
      id: ID!
      name: String!
      email: String!
    }
    type Query {
      user(id: ID!): User
    }
  `,
  resolvers: {
    Query: {
      user: (_, { id }) => fetchUser(id),
    },
  },
});

// Schema B: Post Service
const postSchema = makeExecutableSchema({
  typeDefs: `
    type Post {
      id: ID!
      title: String!
      content: String!
      authorId: ID!
    }
    type Query {
      post(id: ID!): Post
      postsByAuthor(authorId: ID!): [Post!]!
    }
  `,
  resolvers: {
    Query: {
      post: (_, { id }) => fetchPost(id),
      postsByAuthor: (_, { authorId }) => fetchPostsByAuthor(authorId),
    },
  },
});
```

## Advanced Topics

### Schema Stitching with Federation
```graphql
# Federated Schema
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

type Post @key(fields: "id") {
  id: ID!
  title: String!
  content: String!
  author: User!
}
```

### Schema Stitching with Subscriptions
```graphql
type Subscription {
  userCreated: User!
  postUpdated: Post!
  commentAdded(postId: ID!): Comment!
}
```

### Schema Stitching with Directives
```graphql
directive @merge(key: String!) on FIELD_DEFINITION
directive @remote on OBJECT

type User @remote {
  id: ID!
  name: String!
  email: String!
}

type Post {
  id: ID!
  title: String!
  author: User! @merge(key: "authorId")
}
```

## Best Practices

1. **Use consistent types** - Unified scalar types across schemas
2. **Define merge keys** - Clear identification for type merging
3. **Handle conflicts** - Explicit conflict resolution rules
4. **Monitor performance** - Track query execution times
5. **Test thoroughly** - Validate merged schema behavior
6. **Document schemas** - Clear documentation for each subschema
7. **Handle errors** - Consistent error handling across schemas
8. **Cache effectively** - Use caching for remote schema calls
9. **Secure access** - Authentication/authorization for remote schemas
10. **Version schemas** - Schema versioning strategy

## Common Pitfalls

1. **Type conflicts** - Same type name, different structures
2. **Field conflicts** - Same field, different types
3. **Circular dependencies** - Types that reference each other
4. **Performance issues** - N+1 queries in stitched schemas
5. **Authentication gaps** - Missing auth for remote schemas
6. **Error handling** - Inconsistent error formats
7. **Caching issues** - Stale data in stitched schemas
8. **Versioning problems** - Schema version mismatches

## Tools and Libraries

- **GraphQL Tools** - Schema stitching utilities
- **Apollo Federation** - Enterprise schema stitching
- **GraphQL Yoga** - GraphQL server with stitching support
- **PostGraphile** - Automatic schema generation
- **Hasura** - Instant GraphQL APIs

## Real-World Examples

### E-commerce Platform
```graphql
# Product Service
type Product {
  id: ID!
  name: String!
  price: Float!
  inventory: Inventory!
}

# Order Service
type Order {
  id: ID!
  product: Product!
  quantity: Int!
  total: Float!
}

# User Service
type User {
  id: ID!
  name: String!
  orders: [Order!]!
}
```

### Social Media Platform
```graphql
# User Service
type User {
  id: ID!
  name: String!
  followers: [User!]!
  following: [User!]!
}

# Post Service
type Post {
  id: ID!
  content: String!
  author: User!
  likes: [User!]!
  comments: [Comment!]!
}

# Notification Service
type Notification {
  id: ID!
  type: NotificationType!
  user: User!
  post: Post
  read: Boolean!
}
```

## Summary

Schema stitching enables building unified GraphQL APIs from multiple services. By understanding type merging, conflict resolution, and remote schema integration, you can create scalable, maintainable GraphQL architectures.

## Advanced Configuration

### Schema Stitching Configuration
```javascript
// Advanced schema stitching configuration
const stitchingConfig = {
  subschemas: [
    {
      name: 'users',
      schema: userSchema,
      executor: userExecutor,
      merge: {
        User: {
          selectionSet: '{ id }',
          fieldName: 'userById',
          args: (originalObject) => ({ id: originalObject.id }),
        },
      },
    },
    {
      name: 'posts',
      schema: postSchema,
      executor: postExecutor,
      merge: {
        Post: {
          selectionSet: '{ id }',
          fieldName: 'postById',
          args: (originalObject) => ({ id: originalObject.id }),
        },
      },
    },
  ],
  typeMergingConfig: {
    User: {
      selectionSet: '{ id }',
      fieldName: 'userById',
      args: (originalObject) => ({ id: originalObject.id }),
    },
    Post: {
      selectionSet: '{ id }',
      fieldName: 'postById',
      args: (originalObject) => ({ id: originalObject.id }),
    },
  },
};
```

### Remote Schema Configuration
```javascript
// Remote schema executor configuration
const remoteSchemaConfig = {
  timeout: 5000,
  retry: {
    maxAttempts: 3,
    initialDelay: 1000,
    maxDelay: 5000,
    backoff: 'exponential',
  },
  headers: {
    'User-Agent': 'GraphQL-Stitching',
  },
  cache: {
    enabled: true,
    ttl: 300000, // 5 minutes
    maxSize: 1000,
  },
};
```

### Type Merging Configuration
```javascript
// Advanced type merging configuration
const typeMergingConfig = {
  User: {
    selectionSet: '{ id }',
    fieldName: 'userById',
    args: (originalObject) => ({ id: originalObject.id }),
    batching: {
      enabled: true,
      maxBatchSize: 100,
    },
    caching: {
      enabled: true,
      ttl: 600000, // 10 minutes
    },
  },
  Post: {
    selectionSet: '{ id }',
    fieldName: 'postById',
    args: (originalObject) => ({ id: originalObject.id }),
    batching: {
      enabled: true,
      maxBatchSize: 50,
    },
  },
};
```

## Architecture Patterns

### Schema Stitching Architecture
```javascript
// Schema stitching architecture
class SchemaStitchingArchitect {
  constructor(config) {
    this.subschemas = new Map();
    this.mergedSchema = null;
    this.typeRegistry = new TypeRegistry();
  }

  async buildSchema() {
    // Register all subschemas
    for (const [name, config] of this.subschemas) {
      await this.registerSubschema(name, config);
    }

    // Resolve type conflicts
    await this.resolveConflicts();

    // Merge schemas
    this.mergedSchema = await this.mergeSchemas();

    // Validate merged schema
    await this.validateMergedSchema();

    return this.mergedSchema;
  }

  async registerSubschema(name, config) {
    const subschema = {
      name,
      schema: config.schema,
      executor: config.executor,
      mergeConfig: config.merge || {},
    };

    this.subschemas.set(name, subschema);
    this.typeRegistry.registerTypes(config.schema, name);
  }

  async resolveConflicts() {
    const conflicts = this.typeRegistry.getConflicts();
    
    for (const conflict of conflicts) {
      await this.resolveConflict(conflict);
    }
  }

  async mergeSchemas() {
    const schemas = Array.from(this.subschemas.values()).map(s => s.schema);
    
    return stitchSchemas({
      subschemas: schemas,
      typeMergingConfig: this.buildMergingConfig(),
    });
  }

  buildMergingConfig() {
    const config = {};
    
    for (const [name, subschema] of this.subschemas) {
      for (const [typeName, mergeConfig] of Object.entries(subschema.mergeConfig)) {
        if (!config[typeName]) {
          config[typeName] = {};
        }
        config[typeName] = {
          ...config[typeName],
          ...mergeConfig,
        };
      }
    }
    
    return config;
  }
}
```

### Type Registry Pattern
```javascript
// Type registry for schema stitching
class TypeRegistry {
  constructor() {
    this.types = new Map();
    this.conflicts = [];
  }

  registerTypes(schema, subschemaName) {
    const typeMap = schema.getTypeMap();
    
    for (const [typeName, type] of Object.entries(typeMap)) {
      if (!this.types.has(typeName)) {
        this.types.set(typeName, new Map());
      }
      
      this.types.get(typeName).set(subschemaName, {
        type,
        fields: type.getFields(),
        subschemaName,
      });
    }
  }

  getConflicts() {
    const conflicts = [];
    
    for (const [typeName, subschemas] of this.types) {
      if (subschemas.size > 1) {
        const fields = new Map();
        
        for (const [subschemaName, typeInfo] of subschemas) {
          for (const [fieldName, field] of Object.entries(typeInfo.fields)) {
            if (!fields.has(fieldName)) {
              fields.set(fieldName, new Map());
            }
            fields.get(fieldName).set(subschemaName, field);
          }
        }
        
        // Check for field conflicts
        for (const [fieldName, subschemaFields] of fields) {
          if (subschemaFields.size > 1) {
            conflicts.push({
              typeName,
              fieldName,
              subschemas: Array.from(subschemaFields.keys()),
              fields: subschemaFields,
            });
          }
        }
      }
    }
    
    return conflicts;
  }

  resolveConflict(conflict) {
    // Implement conflict resolution logic
    const { typeName, fieldName, subschemas } = conflict;
    
    // Simple resolution: take the first one
    const resolvedField = subschemas[0];
    
    return {
      type: typeName,
      field: fieldName,
      resolvedFrom: resolvedField,
    };
  }
}
```

### Remote Schema Executor Pattern
```javascript
// Remote schema executor pattern
class RemoteSchemaExecutor {
  constructor(config) {
    this.config = config;
    this.cache = new SchemaCache(config.cache);
    this.retryPolicy = config.retry || { maxAttempts: 3 };
  }

  async execute(document, variables, context) {
    const query = print(document);
    const cacheKey = this.generateCacheKey(query, variables);
    
    // Check cache
    const cached = await this.cache.get(cacheKey);
    if (cached) {
      return cached;
    }

    // Execute with retry
    let lastError;
    for (let attempt = 1; attempt <= this.retryPolicy.maxAttempts; attempt++) {
      try {
        const result = await this.executeRemote(query, variables, context);
        
        // Cache result
        await this.cache.set(cacheKey, result, this.config.cache?.ttl || 300000);
        
        return result;
      } catch (error) {
        lastError = error;
        if (attempt < this.retryPolicy.maxAttempts) {
          await this.delay(attempt);
        }
      }
    }
    
    throw lastError;
  }

  async executeRemote(query, variables, context) {
    const response = await fetch(this.config.url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.config.headers,
        ...context.headers,
      },
      body: JSON.stringify({ query, variables }),
      signal: AbortSignal.timeout(this.config.timeout || 5000),
    });

    if (!response.ok) {
      throw new Error(`Remote schema error: ${response.statusText}`);
    }

    return response.json();
  }

  generateCacheKey(query, variables) {
    return `${hash(query)}:${hash(variables)}`;
  }

  delay(attempt) {
    const delay = Math.pow(2, attempt) * 1000;
    return new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

## Integration Guide

### GraphQL Tools Integration
```javascript
// GraphQL Tools schema stitching
const { stitchSchemas } = require('@graphql-tools/stitch');
const { introspectSchema } = require('@graphql-tools/wrap');
const { fetch } = require('node-fetch');

// Create remote executors
const userExecutor = async ({ document, variables }) => {
  const query = print(document);
  const response = await fetch('http://users-service:4001/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });
  return response.json();
};

const postExecutor = async ({ document, variables }) => {
  const query = print(document);
  const response = await fetch('http://posts-service:4002/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });
  return response.json();
};

// Stitch schemas
const stitchedSchema = stitchSchemas({
  subschemas: [
    {
      schema: await introspectSchema(userExecutor),
      executor: userExecutor,
    },
    {
      schema: await introspectSchema(postExecutor),
      executor: postExecutor,
    },
  ],
  typeMergingConfig: {
    User: {
      selectionSet: '{ id }',
      fieldName: 'userById',
      args: (originalObject) => ({ id: originalObject.id }),
    },
  },
});
```

### Apollo Server Integration
```javascript
// Apollo Server with schema stitching
const { ApolloServer } = require('@apollo/server');

const server = new ApolloServer({
  schema: stitchedSchema,
  plugins: [
    {
      async requestDidStart() {
        return {
          async willSendResponse({ response }) {
            // Add stitching metadata
            response.extensions = {
              ...response.extensions,
              stitching: {
                subschemas: Array.from(subschemas.keys()),
                mergedTypes: getMergedTypes(),
              },
            };
          },
        };
      },
    },
  ],
});
```

### Express Integration
```javascript
// Express with schema stitching
const express = require('express');
const { graphqlHTTP } = require('express-graphql');

const app = express();

app.use('/graphql', graphqlHTTP({
  schema: stitchedSchema,
  graphiql: true,
  customFormatErrorFn: (error) => ({
    message: error.message,
    locations: error.locations,
    path: error.path,
    extensions: {
      stitching: error.extensions?.stitching,
    },
  }),
}));
```

## Performance Optimization

### Query Optimization
```javascript
// Query optimization for stitched schemas
class StitchingQueryOptimizer {
  constructor(schema) {
    this.schema = schema;
    this.cache = new QueryPlanCache();
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
    
    // Optimize execution plan
    const optimizedPlan = this.optimizeExecutionPlan(analysis);
    
    // Cache plan
    await this.cache.set(cacheKey, optimizedPlan);
    
    return optimizedPlan;
  }

  analyzeQuery(query) {
    const document = parse(query);
    const operations = this.extractOperations(document);
    
    return {
      operations,
      complexity: this.calculateComplexity(document),
      depth: this.calculateDepth(document),
    };
  }

  optimizeExecutionPlan(analysis) {
    const { operations } = analysis;
    
    // Group operations by subschema
    const grouped = this.groupBySubschema(operations);
    
    // Optimize each group
    const optimized = {};
    for (const [subschema, ops] of Object.entries(grouped)) {
      optimized[subschema] = this.optimizeGroup(ops);
    }
    
    return optimized;
  }

  groupBySubschema(operations) {
    const grouped = {};
    
    for (const operation of operations) {
      const subschema = this.getSubschemaForType(operation.typeName);
      if (!grouped[subschema]) {
        grouped[subschema] = [];
      }
      grouped[subschema].push(operation);
    }
    
    return grouped;
  }
}
```

### DataLoader Integration
```javascript
// DataLoader for stitched schemas
class StitchingDataLoader {
  constructor(config) {
    this.loaders = new Map();
    this.config = config;
  }

  getLoader(typeName, subschema) {
    const key = `${typeName}:${subschema}`;
    
    if (!this.loaders.has(key)) {
      const loader = new DataLoader(async (ids) => {
        return this.batchLoad(typeName, subschema, ids);
      }, {
        maxBatchSize: this.config.maxBatchSize || 100,
        cache: true,
      });
      
      this.loaders.set(key, loader);
    }
    
    return this.loaders.get(key);
  }

  async batchLoad(typeName, subschema, ids) {
    const executor = this.getExecutor(subschema);
    
    const query = `
      query BatchLoad($ids: [ID!]!) {
        ${typeName.toLowerCase()}s(ids: $ids) {
          id
          ...${typeName}Fields
        }
      }
    `;
    
    const result = await executor({
      document: parse(query),
      variables: { ids },
    });
    
    return ids.map(id => 
      result.data[`${typeName.toLowerCase()}s`].find(item => item.id === id)
    );
  }

  getExecutor(subschema) {
    // Get executor for subschema
    return this.config.executors[subschema];
  }
}
```

### Caching Strategy
```javascript
// Caching for stitched schemas
class StitchingCache {
  constructor(config) {
    this.schemaCache = new SchemaCache(config.schemaCache);
    this.responseCache = new ResponseCache(config.responseCache);
    this.typeCache = new TypeCache(config.typeCache);
  }

  async cacheSchema(schema, subschema) {
    const key = `schema:${subschema}`;
    await this.schemaCache.set(key, schema, {
      ttl: this.config.schemaTTL || 3600000, // 1 hour
    });
  }

  async getCachedResponse(query, variables) {
    const key = this.generateResponseKey(query, variables);
    return this.responseCache.get(key);
  }

  async setCachedResponse(query, variables, response) {
    const key = this.generateResponseKey(query, variables);
    await this.responseCache.set(key, response, {
      ttl: this.config.responseTTL || 60000, // 1 minute
    });
  }

  async cacheType(typeName, typeData, subschema) {
    const key = `type:${typeName}:${subschema}`;
    await this.typeCache.set(key, typeData, {
      ttl: this.config.typeTTL || 300000, // 5 minutes
    });
  }

  generateResponseKey(query, variables) {
    return `response:${hash(query)}:${hash(variables)}`;
  }
}
```

## Security Considerations

### Authentication
```javascript
// Authentication for stitched schemas
class StitchingAuth {
  constructor(config) {
    this.authenticators = new Map();
    this.authorizers = new Map();
  }

  async authenticate(subschema, request) {
    const authenticator = this.authenticators.get(subschema);
    if (!authenticator) {
      throw new Error(`No authenticator for subschema: ${subschema}`);
    }

    const user = await authenticator.authenticate(request);
    return user;
  }

  async authorize(subschema, user, operation) {
    const authorizer = this.authorizers.get(subschema);
    if (!authorizer) {
      return true; // No authorization required
    }

    return authorizer.authorize(user, operation);
  }

  registerAuthenticator(subschema, authenticator) {
    this.authenticators.set(subschema, authenticator);
  }

  registerAuthorizer(subschema, authorizer) {
    this.authorizers.set(subschema, authorizer);
  }
}
```

### Input Validation
```javascript
// Input validation for stitched schemas
class StitchingValidator {
  constructor(schema) {
    this.schema = schema;
    this.validators = new Map();
  }

  validate(operation, variables) {
    const validator = this.validators.get(operation);
    if (!validator) {
      return true; // No validation required
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

### Rate Limiting
```javascript
// Rate limiting for stitched schemas
class StitchingRateLimiter {
  constructor(config) {
    this.limiters = new Map();
    this.config = config;
  }

  async checkLimit(subschema, clientId, operation) {
    const key = `${subschema}:${clientId}:${operation}`;
    const limiter = this.getLimiter(key);
    
    return limiter.check();
  }

  getLimiter(key) {
    if (!this.limiters.has(key)) {
      this.limiters.set(key, new RateLimiter({
        maxRequests: this.config.maxRequests || 100,
        windowMs: this.config.windowMs || 60000,
      }));
    }
    return this.limiters.get(key);
  }
}
```

## Troubleshooting Guide

### Common Stitching Issues

#### Schema Composition Errors
```javascript
// Debugging schema composition
class CompositionDebugger {
  constructor() {
    this.logs = [];
  }

  async debugComposition(subschemas) {
    const steps = [
      { name: 'validate', fn: () => this.validateSubschemas(subschemas) },
      { name: 'merge', fn: () => this.mergeSchemas(subschemas) },
      { name: 'validate_merged', fn: (result) => this.validateMergedSchema(result) },
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

#### Type Resolution Errors
```javascript
// Debugging type resolution
class TypeResolutionDebugger {
  constructor(stitcher) {
    this.stitcher = stitcher;
    this.traces = [];
  }

  async debugTypeResolution(typeName, representation) {
    const trace = {
      typeName,
      representation,
      startTime: Date.now(),
      steps: [],
    };

    try {
      // Find subschemas that define this type
      const subschemas = this.stitcher.getSubschemasForType(typeName);
      trace.steps.push({
        name: 'find_subschemas',
        subschemas: subschemas.map(s => s.name),
      });

      // Resolve type from each subschema
      for (const subschema of subschemas) {
        const resolveStart = Date.now();
        const resolved = await subschema.resolve(typeName, representation);
        trace.steps.push({
          name: `resolve_${subschema.name}`,
          duration: Date.now() - resolveStart,
          found: resolved !== null,
        });
      }

      trace.endTime = Date.now();
      this.traces.push(trace);
      return trace;
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
// Performance debugging for stitching
class StitchingPerformanceDebugger {
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

### Schema Stitching API
```graphql
# Schema stitching types
type StitchingConfig {
  subschemas: [SubschemaConfig!]!
  typeMergingConfig: JSON
  mergeTypes: Boolean!
}

type SubschemaConfig {
  name: String!
  schema: String!
  executor: String
  merge: JSON
}

type StitchingResult {
  schema: String!
  subschemas: [String!]!
  mergedTypes: [String!]!
  conflicts: [TypeConflict!]!
}

type TypeConflict {
  typeName: String!
  fieldName: String!
  subschemas: [String!]!
  resolution: String!
}

# Stitching operations
type Mutation {
  addSubschema(config: SubschemaConfigInput!): StitchingResult!
  removeSubschema(name: String!): StitchingResult!
  refreshSchema: StitchingResult!
}

type Query {
  stitchingStatus: StitchingStatus!
  subschemaHealth(name: String): SubschemaHealth!
}
```

### Type Merging API
```javascript
// Type merging interface
class TypeMergingAPI {
  constructor(stitcher) {
    this.stitcher = stitcher;
  }

  async mergeType(typeName, representations) {
    const merged = await this.stitcher.mergeType(typeName, representations);
    return {
      typeName,
      merged,
      timestamp: new Date(),
    };
  }

  async resolveType(typeName, representation, subschema) {
    const resolved = await this.stitcher.resolveType(typeName, representation, subschema);
    return {
      typeName,
      subschema,
      resolved,
      timestamp: new Date(),
    };
  }

  async getMergeStats() {
    return this.stitcher.getMergeStats();
  }
}
```

## Data Models

### Schema Stitching Data Model
```javascript
// Data model for schema stitching
class StitchingModel {
  constructor() {
    this.subschemas = new Map();
    this.mergedTypes = new Map();
    this.conflicts = new Map();
  }

  addSubschema(name, config) {
    this.subschemas.set(name, {
      name,
      ...config,
      status: 'active',
      metrics: {
        requests: 0,
        errors: 0,
        latency: 0,
      },
    });
  }

  removeSubschema(name) {
    this.subschemas.delete(name);
  }

  registerMergedType(typeName, subschemas) {
    this.mergedTypes.set(typeName, {
      typeName,
      subschemas,
      mergedAt: new Date(),
      status: 'active',
    });
  }

  addConflict(typeName, conflict) {
    if (!this.conflicts.has(typeName)) {
      this.conflicts.set(typeName, []);
    }
    this.conflicts.get(typeName).push({
      ...conflict,
      detectedAt: new Date(),
      resolved: false,
    });
  }

  getStats() {
    return {
      subschemas: this.subschemas.size,
      mergedTypes: this.mergedTypes.size,
      conflicts: Array.from(this.conflicts.values()).flat().length,
      unresolvedConflicts: Array.from(this.conflicts.values())
        .flat()
        .filter(c => !c.resolved).length,
    };
  }
}
```

### Type Conflict Data Model
```javascript
// Data model for type conflicts
class TypeConflictModel {
  constructor() {
    this.conflicts = new Map();
    this.resolutions = new Map();
  }

  addConflict(typeName, field, subschemas) {
    const conflictId = `${typeName}:${field}`;
    
    this.conflicts.set(conflictId, {
      id: conflictId,
      typeName,
      field,
      subschemas,
      detectedAt: new Date(),
      status: 'unresolved',
    });
  }

  resolveConflict(typeName, field, resolution) {
    const conflictId = `${typeName}:${field}`;
    const conflict = this.conflicts.get(conflictId);
    
    if (!conflict) {
      return false;
    }

    conflict.status = 'resolved';
    conflict.resolvedAt = new Date();
    conflict.resolution = resolution;

    this.resolutions.set(conflictId, {
      conflictId,
      resolution,
      resolvedAt: new Date(),
    });

    return true;
  }

  getConflict(typeName, field) {
    return this.conflicts.get(`${typeName}:${field}`);
  }

  getUnresolvedConflicts() {
    return Array.from(this.conflicts.values())
      .filter(c => c.status === 'unresolved');
  }
}
```

## Deployment Guide

### Docker Deployment
```dockerfile
# Dockerfile for schema stitching service
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV USER_SERVICE_URL=http://users-service:4001/graphql
ENV POST_SERVICE_URL=http://posts-service:4002/graphql

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
# kubernetes/stitching-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: schema-stitching
spec:
  replicas: 3
  selector:
    matchLabels:
      app: schema-stitching
  template:
    metadata:
      labels:
        app: schema-stitching
    spec:
      containers:
      - name: stitching
        image: schema-stitching:latest
        ports:
        - containerPort: 4000
        env:
        - name: USER_SERVICE_URL
          value: "http://users-service:4001/graphql"
        - name: POST_SERVICE_URL
          value: "http://posts-service:4002/graphql"
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
  name: schema-stitching
spec:
  selector:
    app: schema-stitching
  ports:
  - name: http
    port: 4000
    targetPort: 4000
  type: ClusterIP
```

## Monitoring & Observability

### Metrics Collection
```javascript
// Schema stitching metrics
const promClient = require('prom-client');

const stitchingMetrics = {
  requests: new promClient.Counter({
    name: 'schema_stitching_requests_total',
    help: 'Total stitching requests',
    labelNames: ['subschema', 'operation', 'status'],
  }),

  latency: new promClient.Histogram({
    name: 'schema_stitching_latency_seconds',
    help: 'Stitching request latency',
    labelNames: ['subschema', 'operation'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
  }),

  typeResolutions: new promClient.Counter({
    name: 'schema_stitching_type_resolutions_total',
    help: 'Total type resolutions',
    labelNames: ['type', 'subschema', 'status'],
  }),

  conflicts: new promClient.Counter({
    name: 'schema_stitching_conflicts_total',
    help: 'Total type conflicts',
    labelNames: ['type', 'field', 'resolved'],
  }),
};
```

### Logging Configuration
```javascript
// Structured logging for stitching
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'schema-stitching' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'stitching.log' }),
  ],
});

// Request logging
const requestLogger = {
  async requestDidStart({ request }) {
    const start = Date.now();
    logger.info('Stitching request started', {
      operationName: request.operationName,
      query: request.query,
    });

    return {
      async willSendResponse({ response }) {
        const duration = Date.now() - start;
        logger.info('Stitching request completed', {
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
// Unit tests for schema stitching
describe('Schema Stitching', () => {
  let stitcher;

  beforeEach(() => {
    stitcher = new SchemaStitcher();
  });

  test('stitches schemas successfully', async () => {
    const userSchema = makeExecutableSchema({
      typeDefs: `
        type User {
          id: ID!
          name: String!
        }
        type Query {
          user(id: ID!): User
        }
      `,
    });

    const postSchema = makeExecutableSchema({
      typeDefs: `
        type Post {
          id: ID!
          title: String!
          authorId: ID!
        }
        type Query {
          post(id: ID!): Post
        }
      `,
    });

    const stitched = await stitcher.stitch([userSchema, postSchema]);
    expect(stitched).toBeDefined();
  });

  test('resolves type conflicts', async () => {
    const schema1 = makeExecutableSchema({
      typeDefs: `
        type User {
          id: ID!
          name: String!
        }
      `,
    });

    const schema2 = makeExecutableSchema({
      typeDefs: `
        type User {
          id: ID!
          email: String!
        }
      `,
    });

    const stitched = await stitcher.stitch([schema1, schema2]);
    expect(stitched.getType('User')).toBeDefined();
  });
});
```

### Integration Testing
```javascript
// Integration tests for stitching
describe('Stitching Integration', () => {
  test('resolves cross-schema queries', async () => {
    const query = `
      query {
        user(id: "1") {
          id
          name
          posts {
            id
            title
          }
        }
      }
    `;

    const result = await graphql(stitchedSchema, query);
    expect(result.errors).toBeUndefined();
    expect(result.data.user).toBeDefined();
  });

  test('handles remote schema errors', async () => {
    const query = `
      query {
        user(id: "999") {
          id
          name
        }
      }
    `;

    const result = await graphql(stitchedSchema, query);
    expect(result.errors).toBeDefined();
  });
});
```

## Versioning & Migration

### Schema Versioning
```javascript
// Schema versioning for stitching
class SchemaVersionManager {
  constructor() {
    this.versions = new Map();
    this.deprecations = new Map();
  }

  registerVersion(subschema, version, schema) {
    if (!this.versions.has(subschema)) {
      this.versions.set(subschema, new Map());
    }
    this.versions.get(subschema).set(version, {
      schema,
      registeredAt: new Date(),
      status: 'active',
    });
  }

  deprecateVersion(subschema, version, replacementVersion) {
    const versionInfo = this.versions.get(subschema)?.get(version);
    if (!versionInfo) {
      throw new Error(`Version ${version} not found`);
    }

    versionInfo.status = 'deprecated';
    this.deprecations.set(`${subschema}:${version}`, {
      replacement: replacementVersion,
      deprecatedAt: new Date(),
    });
  }

  getVersion(subschema, version) {
    return this.versions.get(subschema)?.get(version);
  }

  getActiveVersions(subschema) {
    const versions = this.versions.get(subschema);
    if (!versions) {
      return [];
    }

    return Array.from(versions.entries())
      .filter(([_, info]) => info.status === 'active')
      .map(([version, _]) => version);
  }
}
```

### Migration Strategies
```javascript
// Migration strategy for stitching changes
class StitchingMigration {
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
    return {
      addedSubschemas: [],
      removedSubschemas: [],
      modifiedSubschemas: [],
      addedTypes: [],
      removedTypes: [],
    };
  }

  generateMigrationSteps(changes) {
    const steps = [];
    
    // Add new subschemas
    for (const subschema of changes.addedSubschemas) {
      steps.push({
        type: 'add_subschema',
        subschema,
        action: 'add',
      });
    }
    
    // Remove old subschemas
    for (const subschema of changes.removedSubschemas) {
      steps.push({
        type: 'remove_subschema',
        subschema,
        action: 'remove',
      });
    }
    
    return steps;
  }

  async executeStep(step) {
    switch (step.type) {
      case 'add_subschema':
        await this.addSubschema(step.subschema);
        break;
      case 'remove_subschema':
        await this.removeSubschema(step.subschema);
        break;
      default:
        throw new Error(`Unknown step type: ${step.type}`);
    }
  }
}
```

## Glossary

### Stitching Terms

- **Schema Stitching**: Combining multiple GraphQL schemas into a unified schema
- **Type Merging**: Combining type definitions from multiple schemas
- **Subschema**: An individual GraphQL schema that is part of the stitched schema
- **Merge Key**: The field(s) used to uniquely identify types for merging
- **Conflict Resolution**: Handling differences between type definitions
- **Remote Schema**: A schema hosted on a separate service
- **Executor**: Function that executes queries against a remote schema
- **Type Registry**: System that tracks types across schemas

### Architecture Terms

- **Stitching Gateway**: Entry point for the unified schema
- **Type Map**: Mapping of type names to their definitions
- **Field Resolution**: Process of resolving fields across schemas
- **Schema Composition**: Combining schemas into a single schema
- **Query Planning**: Optimizing query execution across schemas

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
- Schema stitching approaches
- Type merging
- Conflict resolution
- Remote schema integration

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

Copyright (c) 2024 Schema Stitching Team

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