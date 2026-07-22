---
name: GraphQL Performance
category: graphql
version: 1.0.0
tags: [graphql, performance, query-complexity, persisted-queries, caching, batching]
difficulty: advanced
estimated_time: 60 minutes
prerequisites: [graphql-basics, api-design]
---

# GraphQL Performance

## Overview

GraphQL performance optimization covers query complexity analysis, persisted queries, caching strategies, and batching techniques. This skill provides comprehensive guidance for building high-performance GraphQL APIs.

## Core Concepts

### 1. Query Complexity Analysis

**Complexity Calculation:**
```javascript
// Query complexity analysis
const complexityMap = {
  users: 10,
  user: 5,
  posts: 8,
  post: 3,
  comments: 6,
  comment: 2,
};

function calculateComplexity(query) {
  let complexity = 0;
  
  // Parse query and sum field costs
  const fields = extractFields(query);
  fields.forEach(field => {
    complexity += complexityMap[field] || 1;
  });
  
  // Multiply by list multipliers
  const listMultipliers = extractListMultipliers(query);
  listMultipliers.forEach(multiplier => {
    complexity *= multiplier;
  });
  
  return complexity;
}

// Query with complexity limit
const MAX_COMPLEXITY = 1000;

function validateComplexity(query) {
  const complexity = calculateComplexity(query);
  if (complexity > MAX_COMPLEXITY) {
    throw new Error(`Query too complex: ${complexity}/${MAX_COMPLEXITY}`);
  }
  return true;
}
```

**Depth Limiting:**
```javascript
// Depth limiting
const MAX_DEPTH = 10;

function validateDepth(query) {
  const depth = calculateDepth(query);
  if (depth > MAX_DEPTH) {
    throw new Error(`Query too deep: ${depth}/${MAX_DEPTH}`);
  }
  return true;
}

function calculateDepth(query) {
  let maxDepth = 0;
  let currentDepth = 0;
  
  // Parse query and track depth
  const tokens = tokenize(query);
  tokens.forEach(token => {
    if (token === '{') {
      currentDepth++;
      maxDepth = Math.max(maxDepth, currentDepth);
    } else if (token === '}') {
      currentDepth--;
    }
  });
  
  return maxDepth;
}
```

### 2. Persisted Queries

**Automatic Persisted Queries (APQ):**
```javascript
// Client sends query hash
const queryHash = sha256(query);
const response = await fetch('/graphql', {
  method: 'POST',
  body: JSON.stringify({
    extensions: {
      persistedQuery: {
        version: 1,
        sha256Hash: queryHash,
      },
    },
    variables,
  }),
});

// If not found, client sends full query
if (response.status === 404) {
  await fetch('/graphql', {
    method: 'POST',
    body: JSON.stringify({
      query,
      variables,
      extensions: {
        persistedQuery: {
          version: 1,
          sha256Hash: queryHash,
        },
      },
    }),
  });
}
```

**Static Persisted Queries:**
```javascript
// Pre-generated query map
const queryMap = {
  'abc123': `
    query GetUser($id: ID!) {
      user(id: $id) {
        id
        name
        email
      }
    }
  `,
  'def456': `
    query GetPosts($first: Int) {
      posts(first: $first) {
        id
        title
        content
      }
    }
  `,
};

// Server-side validation
function getPersistedQuery(hash) {
  return queryMap[hash] || null;
}
```

### 3. Caching Strategies

**Response Caching:**
```javascript
// Server-side response caching
const responseCache = new Map();

async function cachedExecute(query, variables, context) {
  const cacheKey = generateCacheKey(query, variables, context);
  
  // Check cache
  const cached = responseCache.get(cacheKey);
  if (cached && !isStale(cached)) {
    return cached.data;
  }
  
  // Execute query
  const result = await execute(query, variables, context);
  
  // Cache result
  responseCache.set(cacheKey, {
    data: result,
    timestamp: Date.now(),
    ttl: 300000, // 5 minutes
  });
  
  return result;
}

function generateCacheKey(query, variables, context) {
  const userId = context.user?.id || 'anonymous';
  return `${userId}:${hash(query)}:${hash(variables)}`;
}
```

**Field-Level Caching:**
```javascript
// Cache individual fields
const fieldCache = new Map();

const resolvers = {
  User: {
    posts: async (user, _, context) => {
      const cacheKey = `posts:${user.id}`;
      
      const cached = fieldCache.get(cacheKey);
      if (cached && !isStale(cached)) {
        return cached.data;
      }
      
      const posts = await fetchPostsByUserId(user.id);
      fieldCache.set(cacheKey, {
        data: posts,
        timestamp: Date.now(),
        ttl: 600000, // 10 minutes
      });
      
      return posts;
    },
  },
};
```

**CDN Caching:**
```javascript
// HTTP cache headers
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    {
      async requestDidStart() {
        return {
          async willSendResponse({ response }) {
            // Set cache headers
            response.http.headers.set(
              'Cache-Control',
              'public, max-age=300, s-maxage=600'
            );
            response.http.headers.set(
              'CDN-Cache-Control',
              'public, max-age=3600'
            );
          },
        };
      },
    },
  ],
});
```

### 4. Batching Techniques

**DataLoader Pattern:**
```javascript
// DataLoader for N+1 prevention
const DataLoader = require('dataloader');

const userLoader = new DataLoader(async (userIds) => {
  const users = await db.getUsersByIds(userIds);
  const userMap = new Map(users.map(user => [user.id, user]));
  return userIds.map(id => userMap.get(id));
});

const resolvers = {
  Post: {
    author: async (post) => {
      return userLoader.load(post.authorId);
    },
  },
};
```

**Query Batching:**
```javascript
// Batch multiple queries
const batchedQueries = [];
const batchTimeout = 10; // ms

function batchQuery(query, variables) {
  return new Promise((resolve, reject) => {
    batchedQueries.push({ query, variables, resolve, reject });
    
    if (batchedQueries.length === 1) {
      setTimeout(executeBatch, batchTimeout);
    }
  });
}

async function executeBatch() {
  const queries = batchedQueries.splice(0);
  
  const results = await Promise.all(
    queries.map(({ query, variables }) => execute(query, variables))
  );
  
  queries.forEach(({ resolve }, index) => {
    resolve(results[index]);
  });
}
```

**Request Batching:**
```javascript
// Apollo Client request batching
const client = new ApolloClient({
  link: new BatchHttpLink({
    uri: '/graphql',
    batchInterval: 10,
    batchMax: 10,
  }),
  cache: new InMemoryCache(),
});
```

## Implementation Guide

### Step 1: Complexity Analysis

1. Define field costs
2. Implement depth limiting
3. Add complexity validation
4. Monitor query patterns

### Step 2: Persisted Queries

1. Set up APQ or static queries
2. Implement query whitelisting
3. Add query versioning
4. Monitor query usage

### Step 3: Caching Strategy

1. Implement response caching
2. Add field-level caching
3. Configure CDN caching
4. Monitor cache hit rates

### Step 4: Batching Optimization

1. Implement DataLoader
2. Add query batching
3. Configure request batching
4. Monitor batch performance

## Common Patterns

### Query Cost Analysis
```graphql
# Query with complexity annotations
type Query {
  # Low complexity
  user(id: ID!): User @cost(complexity: 5)
  
  # Medium complexity
  posts(first: Int): [Post!]! @cost(complexity: 10, multiplier: "first")
  
  # High complexity
  users(first: Int): [User!]! @cost(complexity: 15, multiplier: "first")
}

# Complexity calculation
# user: 5
# posts(first: 10): 10 * 10 = 100
# users(first: 10): 15 * 10 = 150
```

### Cache Invalidation
```javascript
// Cache invalidation strategy
const cache = new InMemoryCache();

const resolvers = {
  Mutation: {
    updatePost: async (_, { id, input }, { cache }) => {
      const result = await updatePost(id, input);
      
      // Invalidate related caches
      cache.evict({ id: `Post:${id}` });
      cache.evict({ id: 'ROOT_QUERY', fieldName: 'posts' });
      
      // Refetch data
      cache.refetchQueries({
        include: ['GetPosts', 'GetPost'],
      });
      
      return result;
    },
  },
};
```

### Performance Monitoring
```javascript
// Performance monitoring
const performancePlugin = {
  async requestDidStart() {
    const start = Date.now();
    
    return {
      async willSendResponse({ response }) {
        const duration = Date.now() - start;
        
        // Log performance metrics
        console.log({
          query: response.extensions?.query,
          duration,
          complexity: response.extensions?.complexity,
          cached: response.extensions?.cached,
        });
        
        // Send to monitoring system
        await sendMetrics({
          type: 'graphql_request',
          duration,
          complexity: response.extensions?.complexity,
        });
      },
    };
  },
};
```

## Advanced Topics

### Adaptive Complexity
```javascript
// Adaptive complexity based on user role
function calculateComplexity(query, userRole) {
  const baseComplexity = calculateBaseComplexity(query);
  
  // Adjust based on user role
  const roleMultipliers = {
    admin: 1.0,
    editor: 0.8,
    viewer: 0.5,
  };
  
  return baseComplexity * (roleMultipliers[userRole] || 0.5);
}
```

### Query Complexity Budgets
```javascript
// Query complexity budgets per user
const complexityBudgets = {
  free: 100,
  pro: 500,
  enterprise: 1000,
};

function validateComplexityBudget(query, userPlan) {
  const complexity = calculateComplexity(query);
  const budget = complexityBudgets[userPlan] || 100;
  
  if (complexity > budget) {
    throw new Error(
      `Query exceeds budget: ${complexity}/${budget} (${userPlan} plan)`
    );
  }
  
  return true;
}
```

### Performance Dashboards
```graphql
# Performance metrics query
type Query {
  performanceMetrics(
    timeRange: TimeRange!
    filter: MetricFilter
  ): PerformanceMetrics!
}

type PerformanceMetrics {
  averageQueryTime: Float!
  p95QueryTime: Float!
  p99QueryTime: Float!
  totalQueries: Int!
  cacheHitRate: Float!
  errorRate: Float!
  complexityDistribution: [ComplexityBucket!]!
}
```

## Best Practices

1. **Set complexity limits** - Prevent expensive queries
2. **Use persisted queries** - Reduce network overhead
3. **Implement caching** - Cache at multiple levels
4. **Batch requests** - Reduce HTTP overhead
5. **Monitor performance** - Track query metrics
6. **Optimize resolvers** - Use DataLoader for N+1
7. **Add query whitelisting** - Allow only known queries
8. **Implement query timeouts** - Prevent long-running queries
9. **Use connection pooling** - Optimize database connections
10. **Cache invalidation** - Implement smart invalidation

## Common Pitfalls

1. **N+1 queries** - Multiple database queries
2. **Over-caching** - Stale data issues
3. **Under-caching** - Performance degradation
4. **Complexity bypass** - Missing validation
5. **Query爆炸** - Unbounded queries
6. **Memory leaks** - Unclosed connections
7. **Cache stampede** - Thundering herd problem
8. **Stale caches** - Inconsistent data

## Tools and Libraries

- **DataLoader** - Batching and caching library
- **GraphQL Complexity** - Query complexity analysis
- **Apollo Server** - Built-in performance features
- **Redis** - Distributed caching
- **APQ** - Automatic Persisted Queries

## Real-World Examples

### E-commerce Platform
```graphql
# Optimized product query
query GetProduct($id: ID!) {
  product(id: $id) {
    id
    name
    price
    # Use fields with caching
    inventory @cacheControl(maxAge: 300)
    reviews(first: 5) {
      id
      rating
      comment
    }
  }
}
```

### Social Media Feed
```graphql
# Optimized feed query
query GetFeed($first: Int, $after: String) {
  feed(first: $first, after: $after) {
    edges {
      node {
        id
        content
        author {
          name
          avatar @cacheControl(maxAge: 3600)
        }
        likes
        comments(first: 3) {
          id
          content
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

## Summary

GraphQL performance optimization requires a multi-faceted approach including query complexity analysis, persisted queries, caching, and batching. By implementing these strategies, you can build high-performance GraphQL APIs that scale effectively.

## Advanced Configuration

### Query Complexity Configuration
```javascript
// Advanced complexity configuration
const complexityConfig = {
  maximumComplexity: 1000,
  depthLimit: 15,
  costAnalysis: {
    defaultCost: 1,
    scalarCost: 0,
    objectCost: 10,
    listFactor: 20,
    introspectionListFactor: 100,
  },
  estimators: [
    fieldExtensionsEstimator(),
    simpleEstimator({ defaultComplexity: 1 }),
  ],
  onComplete: (complexity) => {
    console.log(`Query complexity: ${complexity}`);
  },
};
```

### Cache Configuration
```javascript
// Multi-layer cache configuration
const cacheConfig = {
  inMemory: {
    maxSize: 10000,
    ttl: 300000, // 5 minutes
    evictionPolicy: 'lru',
  },
  distributed: {
    driver: 'redis',
    host: 'localhost',
    port: 6379,
    ttl: 600000, // 10 minutes
    prefix: 'graphql:',
  },
  cdn: {
    enabled: true,
    maxAge: 3600,
    staleWhileRevalidate: 86400,
  },
};
```

### DataLoader Configuration
```javascript
// DataLoader factory with batching constraints
const createLoader = (batchFn, options = {}) => {
  return new DataLoader(batchFn, {
    maxBatchSize: options.maxBatchSize || 100,
    cache: options.cache !== false,
    cacheKeyFn: options.cacheKeyFn || (key => key),
    batchScheduleFn: options.batchScheduleFn || (cb => setTimeout(cb, 0)),
  });
};
```

## Architecture Patterns

### Query Pipeline
```javascript
// Request pipeline architecture
class QueryPipeline {
  constructor() {
    this.middlewares = [];
    this.cache = new QueryCache();
    this.metrics = new MetricsCollector();
  }

  use(middleware) {
    this.middlewares.push(middleware);
    return this;
  }

  async execute(query, variables, context) {
    const pipeline = this.middlewares;
    let index = 0;

    const next = async () => {
      if (index < pipeline.length) {
        const middleware = pipeline[index++];
        return middleware(query, variables, context, next);
      }
      return this.executeQuery(query, variables, context);
    };

    return next();
  }
}
```

### Caching Architecture
```javascript
// Multi-level caching architecture
class CacheHierarchy {
  constructor() {
    this.levels = [
      new L1Cache({ maxSize: 1000, ttl: 60000 }),
      new L2Cache({ maxSize: 10000, ttl: 300000 }),
      new L3Cache({ driver: 'redis', ttl: 3600000 }),
    ];
  }

  async get(key) {
    for (const level of this.levels) {
      const value = await level.get(key);
      if (value) {
        // Promote to higher levels
        await this.promote(key, value, level);
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
}
```

### Performance Monitoring Architecture
```javascript
// Metrics collection architecture
class PerformanceMonitor {
  constructor() {
    this.collectors = new Map();
    this.exporters = [];
  }

  registerCollector(name, collector) {
    this.collectors.set(name, collector);
  }

  addExporter(exporter) {
    this.exporters.push(exporter);
  }

  async collectMetrics() {
    const metrics = {};
    for (const [name, collector] of this.collectors) {
      metrics[name] = await collector.collect();
    }
    return metrics;
  }

  async exportMetrics(metrics) {
    for (const exporter of this.exporters) {
      await exporter.export(metrics);
    }
  }
}
```

## Integration Guide

### Apollo Server Integration
```javascript
// Apollo Server performance plugins
const { ApolloServerPluginCacheControl } = require('@apollo/server/plugin/cacheControl');
const { ApolloServerPluginLandingPageGraphQLPlayground } = require('@apollo/server/plugin/landingPage/graphql-playground');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginCacheControl({ defaultMaxAge: 5 }),
    ApolloServerPluginLandingPageGraphQLPlayground(),
    {
      async requestDidStart() {
        const start = Date.now();
        return {
          async willSendResponse({ response }) {
            const duration = Date.now() - start;
            await metrics.record('graphql_request_duration', duration);
          },
        };
      },
    },
  ],
});
```

### Express Middleware Integration
```javascript
// Express middleware for performance monitoring
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
      timestamp: new Date().toISOString(),
      duration: error.extensions?.duration,
    },
  }),
}));

// Performance monitoring middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    if (req.path === '/graphql') {
      metrics.record('http_request_duration', duration, {
        method: req.method,
        path: req.path,
        status: res.statusCode,
      });
    }
  });
  next();
});
```

### Redis Cache Integration
```javascript
// Redis cache adapter
const Redis = require('ioredis');

class RedisCache {
  constructor(config) {
    this.client = new Redis(config);
    this.prefix = config.prefix || 'graphql:';
  }

  async get(key) {
    const data = await this.client.get(this.prefix + key);
    return data ? JSON.parse(data) : null;
  }

  async set(key, value, ttl) {
    await this.client.set(
      this.prefix + key,
      JSON.stringify(value),
      'PX',
      ttl
    );
  }

  async delete(key) {
    await this.client.del(this.prefix + key);
  }

  async flush() {
    const keys = await this.client.keys(this.prefix + '*');
    if (keys.length > 0) {
      await this.client.del(...keys);
    }
  }
}
```

## Performance Optimization

### Query Optimization Techniques
```javascript
// Query optimization engine
class QueryOptimizer {
  constructor() {
    this.cache = new QueryCache();
    this.analyzer = new QueryAnalyzer();
  }

  async optimize(query, variables) {
    // Analyze query structure
    const analysis = this.analyzer.analyze(query);
    
    // Apply optimizations
    let optimized = query;
    optimized = this.flattenFragments(optimized);
    optimized = this.eliminateUnusedFields(optimized, analysis);
    optimized = this.inlineFragments(optimized);
    
    // Cache optimization results
    await this.cache.set(query, optimized, 3600000);
    
    return optimized;
  }

  flattenFragments(query) {
    // Implementation for fragment flattening
    return query;
  }

  eliminateUnusedFields(query, analysis) {
    // Implementation for field elimination
    return query;
  }

  inlineFragments(query) {
    // Implementation for fragment inlining
    return query;
  }
}
```

### Connection Pooling
```javascript
// Database connection pooling
class ConnectionPool {
  constructor(config) {
    this.pool = [];
    this.config = config;
    this.maxSize = config.maxSize || 10;
    this.minSize = config.minSize || 2;
  }

  async getConnection() {
    if (this.pool.length > 0) {
      return this.pool.pop();
    }
    return this.createConnection();
  }

  async releaseConnection(connection) {
    if (this.pool.length < this.maxSize) {
      this.pool.push(connection);
    } else {
      await connection.close();
    }
  }

  async createConnection() {
    // Create new database connection
    return { /* connection object */ };
  }
}
```

### Query Deduplication
```javascript
// Query deduplication middleware
class QueryDeduplicator {
  constructor() {
    this.pending = new Map();
  }

  async deduplicate(query, variables, executor) {
    const key = this.generateKey(query, variables);
    
    if (this.pending.has(key)) {
      return this.pending.get(key);
    }
    
    const promise = executor(query, variables);
    this.pending.set(key, promise);
    
    try {
      const result = await promise;
      return result;
    } finally {
      this.pending.delete(key);
    }
  }

  generateKey(query, variables) {
    return `${hash(query)}:${hash(variables)}`;
  }
}
```

## Security Considerations

### Query Depth Validation
```javascript
// Security: Query depth limiting
class QueryDepthValidator {
  constructor(maxDepth = 10) {
    this.maxDepth = maxDepth;
  }

  validate(query) {
    const depth = this.calculateDepth(query);
    if (depth > this.maxDepth) {
      throw new Error(`Query depth ${depth} exceeds maximum ${this.maxDepth}`);
    }
    return true;
  }

  calculateDepth(query) {
    let depth = 0;
    let maxDepth = 0;
    
    const tokens = tokenize(query);
    for (const token of tokens) {
      if (token === '{') {
        depth++;
        maxDepth = Math.max(maxDepth, depth);
      } else if (token === '}') {
        depth--;
      }
    }
    
    return maxDepth;
  }
}
```

### Query Cost Analysis
```javascript
// Security: Cost-based query analysis
class QueryCostAnalyzer {
  constructor(config) {
    this.maxCost = config.maxCost || 1000;
    this.costMap = config.costMap || {};
  }

  analyze(query) {
    let cost = 0;
    const fields = extractFields(query);
    
    for (const field of fields) {
      cost += this.costMap[field] || 1;
    }
    
    if (cost > this.maxCost) {
      throw new Error(`Query cost ${cost} exceeds maximum ${this.maxCost}`);
    }
    
    return cost;
  }
}
```

### Rate Limiting
```javascript
// Security: Rate limiting per client
class RateLimiter {
  constructor(config) {
    this.limits = new Map();
    this.windowMs = config.windowMs || 60000;
    this.maxRequests = config.maxRequests || 100;
  }

  checkLimit(clientId) {
    const now = Date.now();
    const clientLimit = this.limits.get(clientId) || { count: 0, resetAt: now + this.windowMs };
    
    if (now > clientLimit.resetAt) {
      clientLimit.count = 0;
      clientLimit.resetAt = now + this.windowMs;
    }
    
    clientLimit.count++;
    this.limits.set(clientId, clientLimit);
    
    return clientLimit.count <= this.maxRequests;
  }
}
```

## Troubleshooting Guide

### Common Performance Issues

#### High Query Latency
```javascript
// Diagnostic: Identify slow queries
class SlowQueryDetector {
  constructor(threshold = 1000) {
    this.threshold = threshold;
    this.slowQueries = [];
  }

  async measure(query, executor) {
    const start = Date.now();
    const result = await executor(query);
    const duration = Date.now() - start;
    
    if (duration > this.threshold) {
      this.slowQueries.push({
        query,
        duration,
        timestamp: new Date(),
      });
    }
    
    return result;
  }

  getSlowQueries() {
    return this.slowQueries.sort((a, b) => b.duration - a.duration);
  }
}
```

#### Cache Miss Analysis
```javascript
// Diagnostic: Cache hit/miss analysis
class CacheAnalyzer {
  constructor() {
    this.hits = 0;
    this.misses = 0;
  }

  recordHit() {
    this.hits++;
  }

  recordMiss() {
    this.misses++;
  }

  getHitRate() {
    const total = this.hits + this.misses;
    return total > 0 ? this.hits / total : 0;
  }

  analyze() {
    return {
      hits: this.hits,
      misses: this.misses,
      hitRate: this.getHitRate(),
      recommendations: this.generateRecommendations(),
    };
  }

  generateRecommendations() {
    const recommendations = [];
    if (this.getHitRate() < 0.7) {
      recommendations.push('Consider increasing cache TTL');
      recommendations.push('Review cache invalidation strategy');
    }
    return recommendations;
  }
}
```

### Debugging Tools
```javascript
// Debugging: Query execution tracer
class QueryTracer {
  constructor() {
    this.traces = [];
  }

  trace(query, variables, context) {
    const traceId = generateTraceId();
    const span = {
      traceId,
      query,
      variables,
      startTime: Date.now(),
      spans: [],
    };

    return {
      startSpan: (name) => {
        const spanStart = Date.now();
        return {
          end: () => {
            span.spans.push({
              name,
              duration: Date.now() - spanStart,
            });
          },
        };
      },
      end: () => {
        span.endTime = Date.now();
        span.duration = span.endTime - span.startTime;
        this.traces.push(span);
        return traceId;
      },
    };
  }

  getTraces() {
    return this.traces;
  }
}
```

## API Reference

### Performance Metrics API
```graphql
# Performance metrics query
type Query {
  performanceMetrics(
    timeRange: TimeRange!
    filter: MetricFilter
  ): PerformanceMetrics!
}

type PerformanceMetrics {
  averageQueryTime: Float!
  p95QueryTime: Float!
  p99QueryTime: Float!
  totalQueries: Int!
  cacheHitRate: Float!
  errorRate: Float!
  complexityDistribution: [ComplexityBucket!]!
}

type ComplexityBucket {
  min: Int!
  max: Int!
  count: Int!
  percentage: Float!
}

input TimeRange {
  start: DateTime!
  end: DateTime!
}

input MetricFilter {
  operationName: String
  fieldName: String
  clientName: String
}
```

### Cache Management API
```javascript
// Cache management interface
class CacheManager {
  constructor(config) {
    this.cache = new CacheHierarchy(config);
    this.stats = new CacheStats();
  }

  async get(key) {
    const start = Date.now();
    const value = await this.cache.get(key);
    const duration = Date.now() - start;
    
    this.stats.record('get', duration, value !== null);
    return value;
  }

  async set(key, value, ttl) {
    const start = Date.now();
    await this.cache.set(key, value, ttl);
    const duration = Date.now() - start;
    
    this.stats.record('set', duration);
  }

  async invalidate(pattern) {
    const start = Date.now();
    await this.cache.invalidate(pattern);
    const duration = Date.now() - start;
    
    this.stats.record('invalidate', duration);
  }

  getStats() {
    return this.stats.getStats();
  }
}
```

## Data Models

### Performance Metrics Model
```javascript
// Data model for performance metrics
class PerformanceMetrics {
  constructor() {
    this.queryMetrics = new Map();
    this.fieldMetrics = new Map();
    this.userMetrics = new Map();
  }

  recordQuery(operationName, duration, complexity, cached) {
    const metric = this.queryMetrics.get(operationName) || {
      count: 0,
      totalDuration: 0,
      maxDuration: 0,
      minDuration: Infinity,
      complexities: [],
    };

    metric.count++;
    metric.totalDuration += duration;
    metric.maxDuration = Math.max(metric.maxDuration, duration);
    metric.minDuration = Math.min(metric.minDuration, duration);
    metric.complexities.push(complexity);

    this.queryMetrics.set(operationName, metric);
  }

  getFieldMetrics(fieldName) {
    return this.fieldMetrics.get(fieldName) || {
      calls: 0,
      totalDuration: 0,
      errors: 0,
    };
  }

  getUserMetrics(userId) {
    return this.userMetrics.get(userId) || {
      queries: 0,
      totalComplexity: 0,
      cacheHits: 0,
    };
  }
}
```

### Cache Data Model
```javascript
// Data model for cache entries
class CacheEntry {
  constructor(key, value, ttl) {
    this.key = key;
    this.value = value;
    this.ttl = ttl;
    this.createdAt = Date.now();
    this.accessCount = 0;
    this.lastAccessed = Date.now();
  }

  isExpired() {
    return Date.now() - this.createdAt > this.ttl;
  }

  access() {
    this.accessCount++;
    this.lastAccessed = Date.now();
  }

  getAge() {
    return Date.now() - this.createdAt;
  }

  getFrequency() {
    const ageHours = this.getAge() / (1000 * 60 * 60);
    return ageHours > 0 ? this.accessCount / ageHours : 0;
  }
}
```

## Deployment Guide

### Environment Configuration
```javascript
// Configuration for different environments
const config = {
  development: {
    cache: {
      driver: 'memory',
      ttl: 60000,
    },
    complexity: {
      maximum: 1000,
      depthLimit: 10,
    },
    logging: {
      level: 'debug',
    },
  },
  production: {
    cache: {
      driver: 'redis',
      host: process.env.REDIS_HOST,
      port: process.env.REDIS_PORT,
      ttl: 300000,
    },
    complexity: {
      maximum: 500,
      depthLimit: 8,
    },
    logging: {
      level: 'info',
    },
  },
  testing: {
    cache: {
      driver: 'memory',
      ttl: 0,
    },
    complexity: {
      maximum: 10000,
      depthLimit: 20,
    },
    logging: {
      level: 'warn',
    },
  },
};
```

### Docker Configuration
```dockerfile
# Dockerfile for GraphQL performance service
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

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
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graphql-performance
spec:
  replicas: 3
  selector:
    matchLabels:
      app: graphql-performance
  template:
    metadata:
      labels:
        app: graphql-performance
    spec:
      containers:
      - name: graphql
        image: graphql-performance:latest
        ports:
        - containerPort: 4000
        env:
        - name: REDIS_HOST
          value: "redis-service"
        - name: REDIS_PORT
          value: "6379"
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
```

## Monitoring & Observability

### Metrics Collection
```javascript
// Prometheus metrics collection
const promClient = require('prom-client');

const httpRequestDuration = new promClient.Histogram({
  name: 'graphql_http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'operation_name', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
});

const graphqlQueryDuration = new promClient.Histogram({
  name: 'graphql_query_duration_seconds',
  help: 'Duration of GraphQL queries in seconds',
  labelNames: ['operation_name', 'complexity'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
});

const cacheHitRate = new promClient.Gauge({
  name: 'graphql_cache_hit_rate',
  help: 'Cache hit rate',
  labelNames: ['cache_level'],
});
```

### Logging Configuration
```javascript
// Structured logging for performance
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'graphql-performance.log' }),
  ],
});

// Performance logging middleware
const performanceLogger = {
  async requestDidStart() {
    const start = Date.now();
    return {
      async willSendResponse({ response }) {
        const duration = Date.now() - start;
        logger.info('GraphQL request completed', {
          operationName: response.extensions?.operationName,
          duration,
          complexity: response.extensions?.complexity,
          cached: response.extensions?.cached,
          timestamp: new Date().toISOString(),
        });
      },
    };
  },
};
```

### Alerting Rules
```yaml
# alerting/prometheus-rules.yaml
groups:
- name: graphql-performance
  rules:
  - alert: HighQueryLatency
    expr: histogram_quantile(0.95, rate(graphql_query_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High GraphQL query latency"
      description: "P95 query latency is above 1 second for 5 minutes"

  - alert: HighErrorRate
    expr: rate(graphql_errors_total[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High GraphQL error rate"
      description: "Error rate is above 10% for 5 minutes"

  - alert: LowCacheHitRate
    expr: graphql_cache_hit_rate < 0.7
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Low cache hit rate"
      description: "Cache hit rate is below 70% for 10 minutes"
```

## Testing Strategy

### Performance Testing
```javascript
// Load testing with Artillery
module.exports = {
  config: {
    target: 'http://localhost:4000',
    phases: [
      { duration: 60, arrivalRate: 10 },
      { duration: 120, arrivalRate: 50 },
      { duration: 60, arrivalRate: 100 },
    ],
    defaults: {
      headers: {
        'Content-Type': 'application/json',
      },
    },
  },
  scenarios: [
    {
      name: 'Simple Query',
      flow: [
        {
          post: {
            url: '/graphql',
            json: {
              query: `query { user(id: "1") { id name } }`,
            },
          },
        },
      ],
    },
    {
      name: 'Complex Query',
      flow: [
        {
          post: {
            url: '/graphql',
            json: {
              query: `query { users(first: 10) { id name posts { id title } } }`,
            },
          },
        },
      ],
    },
  ],
};
```

### Unit Testing
```javascript
// Unit tests for performance utilities
describe('Query Complexity Analyzer', () => {
  test('calculates simple query complexity', () => {
    const query = `{ user(id: "1") { id name } }`;
    const complexity = analyzeComplexity(query);
    expect(complexity).toBe(6); // user(5) + id(1) + name(1)
  });

  test('rejects queries exceeding complexity limit', () => {
    const query = `{ users(first: 100) { id name posts { id } } }`;
    expect(() => analyzeComplexity(query, { maxComplexity: 50 }))
      .toThrow('Query complexity exceeds limit');
  });
});

describe('Cache Manager', () => {
  test('returns cached value', async () => {
    const cache = new CacheManager({ driver: 'memory' });
    await cache.set('key1', 'value1', 60000);
    const value = await cache.get('key1');
    expect(value).toBe('value1');
  });

  test('returns null for expired cache', async () => {
    const cache = new CacheManager({ driver: 'memory' });
    await cache.set('key1', 'value1', 1); // 1ms TTL
    await new Promise(resolve => setTimeout(resolve, 10));
    const value = await cache.get('key1');
    expect(value).toBeNull();
  });
});
```

### Integration Testing
```javascript
// Integration tests for performance monitoring
describe('Performance Monitoring Integration', () => {
  let server;
  let metrics;

  beforeAll(async () => {
    server = await createTestServer();
    metrics = new PerformanceMetrics();
  });

  afterAll(async () => {
    await server.close();
  });

  test('records query metrics', async () => {
    const query = `{ user(id: "1") { id name } }`;
    await server.executeOperation({ query });
    
    const queryMetrics = metrics.getQueryMetrics('user');
    expect(queryMetrics.count).toBe(1);
    expect(queryMetrics.totalDuration).toBeGreaterThan(0);
  });

  test('tracks cache performance', async () => {
    const query = `{ user(id: "1") { id name } }`;
    
    // First request - cache miss
    await server.executeOperation({ query });
    
    // Second request - cache hit
    await server.executeOperation({ query });
    
    const cacheStats = metrics.getCacheStats();
    expect(cacheStats.hits).toBe(1);
    expect(cacheStats.misses).toBe(1);
  });
});
```

## Versioning & Migration

### Query Versioning
```javascript
// Query versioning strategy
class QueryVersionManager {
  constructor() {
    this.versions = new Map();
    this.deprecations = new Map();
  }

  registerVersion(queryId, version, query) {
    if (!this.versions.has(queryId)) {
      this.versions.set(queryId, new Map());
    }
    this.versions.get(queryId).set(version, query);
  }

  deprecateVersion(queryId, version, replacementVersion) {
    this.deprecations.set(`${queryId}:${version}`, {
      replacement: replacementVersion,
      deprecatedAt: new Date(),
    });
  }

  getVersion(queryId, version) {
    const query = this.versions.get(queryId)?.get(version);
    const deprecation = this.deprecations.get(`${queryId}:${version}`);
    
    return {
      query,
      deprecated: !!deprecation,
      replacement: deprecation?.replacement,
    };
  }
}
```

### Migration Strategies
```javascript
// Migration strategy for cache changes
class CacheMigration {
  constructor(config) {
    this.oldCache = config.oldCache;
    this.newCache = config.newCache;
    this.batchSize = config.batchSize || 100;
  }

  async migrate() {
    const keys = await this.oldCache.keys();
    const batches = this.chunk(keys, this.batchSize);
    
    for (const batch of batches) {
      await Promise.all(
        batch.map(async (key) => {
          const value = await this.oldCache.get(key);
          if (value) {
            await this.newCache.set(key, value);
          }
        })
      );
      
      console.log(`Migrated ${batch.length} keys`);
    }
  }

  chunk(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }
}
```

## Glossary

### Performance Terms

- **Query Complexity**: A numerical value representing the computational cost of executing a GraphQL query
- **Depth Limiting**: Restricting the maximum nesting level of GraphQL queries
- **Persisted Queries**: Pre-registered queries identified by hash rather than full query text
- **DataLoader**: A batching and caching library for reducing database requests
- **N+1 Problem**: When a query for a list of items triggers additional queries for each item's related data
- **Cache Hit Rate**: The percentage of cache lookups that return valid data
- **Query Deduplication**: Combining identical queries to execute only once
- **Connection Pooling**: Reusing database connections across multiple requests
- **Request Batching**: Combining multiple HTTP requests into a single batch
- **Cache Stampede**: When many clients simultaneously request uncached data

### Architecture Terms

- **Query Pipeline**: The sequence of processing steps a GraphQL query goes through
- **Cache Hierarchy**: Multiple levels of caching (L1, L2, L3) with different characteristics
- **Metrics Collector**: Components that gather performance data
- **Exporter**: Systems that send metrics to external monitoring tools
- **Middleware**: Components that process requests before they reach resolvers

## Changelog

### Version 1.1.0 (2024-01-15)
- Added advanced configuration section
- Added architecture patterns
- Added integration guide
- Added performance optimization techniques
- Added security considerations

### Version 1.0.0 (2024-01-01)
- Initial release
- Query complexity analysis
- Persisted queries
- Caching strategies
- Batching techniques

## Contributing Guidelines

### Development Setup
1. Clone the repository
2. Install dependencies: `npm install`
3. Run tests: `npm test`
4. Start development server: `npm run dev`

### Code Standards
- Use TypeScript for new implementations
- Follow ESLint configuration
- Write unit tests for new features
- Update documentation for changes

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Update documentation
4. Submit pull request with description
5. Address review feedback

## License

MIT License

Copyright (c) 2024 GraphQL Performance Team

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