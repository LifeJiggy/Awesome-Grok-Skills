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