---
name: GraphQL Subscriptions
category: graphql
version: 1.0.0
tags: [graphql, subscriptions, websocket, real-time, scaling]
difficulty: advanced
estimated_time: 60 minutes
prerequisites: [graphql-basics, websocket-concepts]
---

# GraphQL Subscriptions

## Overview

GraphQL subscriptions enable real-time data updates over WebSocket connections. This skill covers WebSocket transport, real-time update patterns, filtering mechanisms, and scaling strategies.

## Core Concepts

### 1. WebSocket Transport

**Connection Setup:**
```javascript
// Client-side connection
const client = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:4000/graphql',
    connectionParams: {
      authToken: 'user-token',
    },
    on: {
      connected: () => console.log('Connected'),
      error: (err) => console.error('Error:', err),
    },
  })
);

// Server-side setup
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const serverCleanup = useServer(
  {
    schema,
    context: async (ctx) => {
      // Get user from connection params
      const token = ctx.connectionParams.authToken;
      const user = await getUser(token);
      return { user };
    },
  },
  wsServer
);
```

**Transport Protocols:**
```graphql
# Subscription protocol
subscription OnNewPost($authorId: ID!) {
  postCreated(authorId: $authorId) {
    id
    title
    content
    author {
      name
    }
    createdAt
  }
}

# With variables
subscription OnPostUpdates($postId: ID!) {
  postUpdated(postId: $postId) {
    id
    title
    content
    updatedAt
  }
}
```

### 2. Real-Time Update Patterns

**Event-Driven Updates:**
```graphql
# Post subscription
type Subscription {
  postCreated: Post!
  postUpdated(postId: ID): Post!
  postDeleted(postId: ID): Boolean!
}

# Comment subscription
type Subscription {
  commentAdded(postId: ID!): Comment!
  commentUpdated(postId: ID!): Comment!
  commentDeleted(postId: ID!): Boolean!
}

# User subscription
type Subscription {
  userStatusChanged(userId: ID!): UserStatus!
  userNotification(userId: ID!): Notification!
}
```

**Mutation-Triggered Updates:**
```graphql
# Mutation that triggers subscriptions
type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(id: ID!, input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): DeletePostPayload!
}

# Subscription triggers
type Subscription {
  postCreated: Post!
  postUpdated(postId: ID!): Post!
  postDeleted(postId: ID!): Boolean!
}
```

### 3. Filtering Mechanisms

**Topic-Based Filtering:**
```javascript
// Server-side filtering
const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator('POST_CREATED'),
        (payload, variables, context) => {
          // Filter by user permissions
          return context.user.permissions.includes('post:read');
        }
      ),
    },
    postUpdated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator('POST_UPDATED'),
        (payload, variables) => {
          // Filter by post ID
          return payload.postUpdated.id === variables.postId;
        }
      ),
    },
  },
};
```

**Field-Level Filtering:**
```graphql
# Subscription with field selection
subscription OnPostUpdates($postId: ID!) {
  postUpdated(postId: $postId) {
    id
    title
    content
    # Only receive these fields
  }
}
```

### 4. Scaling Strategies

**Horizontal Scaling:**
```javascript
// Redis pub/sub for horizontal scaling
const pubsub = new RedisPubSub({
  connection: {
    host: 'redis-server',
    port: 6379,
  },
});

// Multiple server instances
const server1 = createServer(schema, pubsub);
const server2 = createServer(schema, pubsub);
const server3 = createServer(schema, pubsub);
```

**Connection Management:**
```javascript
// Connection tracking
const connections = new Map();

// Heartbeat mechanism
setInterval(() => {
  connections.forEach((connection, id) => {
    if (!connection.isAlive) {
      connections.delete(id);
      connection.terminate();
    }
    connection.isAlive = false;
    connection.ping();
  });
}, 30000);
```

## Implementation Guide

### Step 1: Schema Design

1. Define subscription types
2. Add filtering arguments
3. Implement subscription resolvers
4. Handle connection lifecycle

### Step 2: WebSocket Setup

1. Configure WebSocket server
2. Implement authentication
3. Handle connection errors
4. Add heartbeat mechanism

### Step 3: Event Publishing

1. Create pub/sub system
2. Publish events from mutations
3. Implement filtering
4. Handle backpressure

### Step 4: Scaling and Monitoring

1. Implement horizontal scaling
2. Monitor connection counts
3. Track subscription performance
4. Handle connection drops

## Common Patterns

### Authentication
```javascript
// Authentication middleware
const server = new ApolloServer({
  schema,
  plugins: [
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
  context: async ({ req, connection }) => {
    // HTTP request
    if (req) {
      const user = await getUser(req.headers.authorization);
      return { user };
    }
    
    // WebSocket connection
    if (connection) {
      const user = await getUser(connection.context.authToken);
      return { user };
    }
  },
});
```

### Error Handling
```javascript
// Subscription error handling
const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: async function* (_, __, context) {
        try {
          const iterator = pubsub.asyncIterator('POST_CREATED');
          for await (const payload of iterator) {
            yield payload;
          }
        } catch (error) {
          console.error('Subscription error:', error);
          throw new GraphQLError('Subscription failed');
        }
      },
    },
  },
};
```

### Client-Side Implementation
```javascript
// React hook for subscriptions
function usePostSubscription(postId) {
  const { data, loading, error } = useSubscription(
    gql`
      subscription OnPostUpdates($postId: ID!) {
        postUpdated(postId: $postId) {
          id
          title
          content
          updatedAt
        }
      }
    `,
    {
      variables: { postId },
      onSubscriptionData: ({ subscriptionData }) => {
        // Handle real-time update
        console.log('Post updated:', subscriptionData.data.postUpdated);
      },
    }
  );

  return { data, loading, error };
}
```

## Advanced Topics

### Subscription Multiplexing
```javascript
// Multiple subscriptions on same connection
const client = createClient({
  url: 'ws://localhost:4000/graphql',
});

// Subscribe to multiple events
const subscriptions = [
  client.subscribe({
    query: POST_CREATED_SUBSCRIPTION,
  }),
  client.subscribe({
    query: COMMENT_ADDED_SUBSCRIPTION,
    variables: { postId: '123' },
  }),
  client.subscribe({
    query: USER_STATUS_SUBSCRIPTION,
    variables: { userId: '456' },
  }),
];
```

### Live Queries (Alternative to Subscriptions)
```graphql
# Live query definition
type Query {
  post(id: ID!): Post @live
  posts: [Post!]! @live
}

# Live query with filtering
type Query {
  postsByAuthor(authorId: ID!): [Post!]! @live
}
```

### Subscription-Based Caching
```javascript
// Cache updates via subscriptions
const cache = new InMemoryCache();

const client = new ApolloClient({
  link: from([httpLink, wsLink]),
  cache,
  typeDefs,
  resolvers: {
    Mutation: {
      createPost: (_, { input }, { cache }) => {
        // Update cache
        const data = cache.readQuery({ query: GET_POSTS });
        cache.writeQuery({
          query: GET_POSTS,
          data: { posts: [...data.posts, newPost] },
        });
      },
    },
  },
});
```

## Best Practices

1. **Use authentication** - Secure WebSocket connections
2. **Implement filtering** - Reduce unnecessary updates
3. **Handle reconnection** - Client-side reconnection logic
4. **Monitor connections** - Track active subscriptions
5. **Implement heartbeats** - Detect dead connections
6. **Use connection pooling** - Optimize resource usage
7. **Add error handling** - Graceful error recovery
8. **Implement backpressure** - Handle slow consumers
9. **Use Redis pub/sub** - For horizontal scaling
10. **Monitor performance** - Track subscription latency

## Common Pitfalls

1. **Memory leaks** - Unsubscribed listeners
2. **Connection exhaustion** - Too many open connections
3. **Duplicate updates** - Multiple subscription triggers
4. **Stale data** - Missing updates
5. **Authentication gaps** - Unsecured connections
6. **Error propagation** - Subscription failures
7. **Scaling issues** - Single-server limitations
8. **Performance degradation** - Slow subscription handling

## Tools and Libraries

- **graphql-ws** - WebSocket transport for GraphQL
- **subscriptions-transport-ws** - Legacy WebSocket transport
- **Apollo Client** - Client-side subscription support
- **Redis Pub/Sub** - Horizontal scaling
- **Socket.io** - Alternative WebSocket implementation

## Real-World Examples

### Chat Application
```graphql
# Chat subscriptions
type Subscription {
  messageSent(channelId: ID!): Message!
  userJoined(channelId: ID!): User!
  userLeft(channelId: ID!): User!
}

# Chat mutations
type Mutation {
  sendMessage(channelId: ID!, content: String!): Message!
  joinChannel(channelId: ID!): User!
  leaveChannel(channelId: ID!): User!
}
```

### Real-Time Dashboard
```graphql
# Dashboard subscriptions
type Subscription {
  metricsUpdated: Metrics!
  alertTriggered: Alert!
  systemStatusChanged: SystemStatus!
}

# Dashboard queries
type Query {
  currentMetrics: Metrics!
  recentAlerts: [Alert!]!
  systemStatus: SystemStatus!
}
```

### Collaborative Editing
```graphql
# Collaboration subscriptions
type Subscription {
  documentUpdated(documentId: ID!): Document!
  cursorMoved(documentId: ID!): Cursor!
  userJoined(documentId: ID!): User!
  userLeft(documentId: ID!): User!
}

# Collaboration mutations
type Mutation {
  updateDocument(documentId: ID!, content: String!): Document!
  moveCursor(documentId: ID!, position: CursorPosition!): Cursor!
}
```

## Summary

GraphQL subscriptions enable real-time data updates over WebSocket connections. By understanding WebSocket transport, filtering mechanisms, and scaling strategies, you can build responsive, real-time applications with GraphQL.

## Advanced Configuration

### WebSocket Configuration
```javascript
// Advanced WebSocket server configuration
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
  maxPayload: 1024 * 1024, // 1MB
  backlog: 511,
  perMessageDeflate: {
    threshold: 1024,
  },
  verifyClient: (info, done) => {
    // Custom authentication
    const token = info.req.headers.authorization?.split(' ')[1];
    if (!token) {
      done(false, 401, 'Unauthorized');
      return;
    }
    
    try {
      const user = verifyToken(token);
      info.req.user = user;
      done(true);
    } catch (error) {
      done(false, 401, 'Invalid token');
    }
  },
});
```

### Subscription Configuration
```javascript
// Subscription engine configuration
const subscriptionConfig = {
  maxSubscriptionsPerClient: 10,
  maxSubscriptionsTotal: 10000,
  heartbeatInterval: 30000,
  keepAlive: 10000,
  connectionTimeout: 5000,
  retryAttempts: 3,
  retryDelay: 1000,
  maxBackpressure: 1024 * 1024, // 1MB
};
```

### Pub/Sub Configuration
```javascript
// Redis pub/sub configuration
const pubsubConfig = {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: process.env.REDIS_PORT || 6379,
    password: process.env.REDIS_PASSWORD,
    db: 0,
    retryDelayOnFailover: 100,
    maxRetriesPerRequest: 3,
  },
  prefix: 'graphql:subscriptions:',
  healthCheck: {
    enabled: true,
    interval: 5000,
  },
};
```

## Architecture Patterns

### Subscription Manager Pattern
```javascript
// Subscription manager architecture
class SubscriptionManager {
  constructor(config) {
    this.subscriptions = new Map();
    this.pubsub = new PubSub(config.pubsub);
    this.metrics = new SubscriptionMetrics();
  }

  async subscribe(subscriptionId, query, variables, context) {
    // Validate subscription
    await this.validateSubscription(query, variables, context);
    
    // Create subscription
    const subscription = {
      id: subscriptionId,
      query,
      variables,
      context,
      createdAt: Date.now(),
      lastEventAt: null,
      eventCount: 0,
    };
    
    // Store subscription
    this.subscriptions.set(subscriptionId, subscription);
    
    // Set up event listener
    const iterator = this.pubsub.asyncIterator(query);
    subscription.iterator = iterator;
    
    // Track metrics
    this.metrics.recordSubscription(subscriptionId);
    
    return subscription;
  }

  async unsubscribe(subscriptionId) {
    const subscription = this.subscriptions.get(subscriptionId);
    if (!subscription) {
      return false;
    }
    
    // Clean up iterator
    if (subscription.iterator) {
      await subscription.iterator.return();
    }
    
    // Remove subscription
    this.subscriptions.delete(subscriptionId);
    
    // Track metrics
    this.metrics.recordUnsubscription(subscriptionId);
    
    return true;
  }

  async publish(eventType, payload) {
    await this.pubsub.publish(eventType, payload);
  }

  getActiveSubscriptions() {
    return Array.from(this.subscriptions.values());
  }
}
```

### Connection Pool Pattern
```javascript
// Connection pool for WebSocket connections
class ConnectionPool {
  constructor(config) {
    this.connections = new Map();
    this.maxConnections = config.maxConnections || 1000;
    this.heartbeatInterval = config.heartbeatInterval || 30000;
    this.connectionTimeout = config.connectionTimeout || 10000;
    
    this.startHeartbeat();
  }

  async addConnection(connectionId, socket) {
    if (this.connections.size >= this.maxConnections) {
      throw new Error('Maximum connections reached');
    }
    
    const connection = {
      id: connectionId,
      socket,
      isAlive: true,
      createdAt: Date.now(),
      lastActivity: Date.now(),
      subscriptions: new Set(),
    };
    
    this.connections.set(connectionId, connection);
    
    // Set up heartbeat
    socket.on('pong', () => {
      connection.isAlive = true;
      connection.lastActivity = Date.now();
    });
    
    return connection;
  }

  removeConnection(connectionId) {
    const connection = this.connections.get(connectionId);
    if (!connection) {
      return false;
    }
    
    // Clean up subscriptions
    for (const subscriptionId of connection.subscriptions) {
      // Remove subscription
    }
    
    // Close socket
    if (connection.socket.readyState === WebSocket.OPEN) {
      connection.socket.close();
    }
    
    this.connections.delete(connectionId);
    return true;
  }

  startHeartbeat() {
    setInterval(() => {
      this.connections.forEach((connection, id) => {
        if (!connection.isAlive) {
          this.removeConnection(id);
          return;
        }
        
        connection.isAlive = false;
        connection.socket.ping();
      });
    }, this.heartbeatInterval);
  }

  getConnectionStats() {
    return {
      total: this.connections.size,
      alive: Array.from(this.connections.values()).filter(c => c.isAlive).length,
      stale: Array.from(this.connections.values()).filter(c => !c.isAlive).length,
    };
  }
}
```

### Event Router Pattern
```javascript
// Event routing for subscriptions
class EventRouter {
  constructor() {
    this.routes = new Map();
    this.filters = new Map();
  }

  registerRoute(eventType, handler) {
    this.routes.set(eventType, handler);
  }

  registerFilter(eventType, filterFn) {
    this.filters.set(eventType, filterFn);
  }

  async routeEvent(eventType, payload, subscriptions) {
    const handler = this.routes.get(eventType);
    if (!handler) {
      throw new Error(`No handler for event type: ${eventType}`);
    }

    const filteredSubscriptions = [];
    for (const subscription of subscriptions) {
      const filter = this.filters.get(eventType);
      if (!filter || await filter(subscription, payload)) {
        filteredSubscriptions.push(subscription);
      }
    }

    // Execute handler for each subscription
    const results = await Promise.allSettled(
      filteredSubscriptions.map(subscription =>
        handler(subscription, payload)
      )
    );

    return results;
  }
}
```

## Integration Guide

### Apollo Server Integration
```javascript
// Apollo Server subscription setup
const { ApolloServer } = require('@apollo/server');
const { WebSocketServer } = require('ws');
const { useServer } = require('graphql-ws/lib/use/ws');

const httpServer = createServer(app);
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const serverCleanup = useServer(
  {
    schema,
    context: async (ctx) => {
      const token = ctx.connectionParams?.authToken;
      const user = await getUser(token);
      return { user };
    },
    onConnect: async (ctx) => {
      console.log('Client connected');
      return { userId: ctx.connectionParams?.userId };
    },
    onDisconnect: async (ctx, reason) => {
      console.log('Client disconnected', reason);
    },
  },
  wsServer
);

const server = new ApolloServer({
  schema,
  plugins: [
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});
```

### Express Integration
```javascript
// Express WebSocket integration
const express = require('express');
const http = require('http');
const { WebSocketServer } = require('ws');

const app = express();
const httpServer = http.createServer(app);

const wss = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

wss.on('connection', (ws, req) => {
  console.log('New WebSocket connection');
  
  // Authenticate connection
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    ws.close(4001, 'Unauthorized');
    return;
  }
  
  // Handle messages
  ws.on('message', (data) => {
    try {
      const message = JSON.parse(data);
      handleMessage(ws, message);
    } catch (error) {
      ws.send(JSON.stringify({ error: 'Invalid message format' }));
    }
  });
  
  // Handle close
  ws.on('close', () => {
    console.log('WebSocket closed');
  });
});
```

### Redis Pub/Sub Integration
```javascript
// Redis pub/sub for distributed subscriptions
const Redis = require('ioredis');
const { RedisPubSub } = require('graphql-redis-subscriptions');

const pubsub = new RedisPubSub({
  publisher: new Redis({
    host: process.env.REDIS_HOST,
    port: process.env.REDIS_PORT,
    password: process.env.REDIS_PASSWORD,
  }),
  subscriber: new Redis({
    host: process.env.REDIS_HOST,
    port: process.env.REDIS_PORT,
    password: process.env.REDIS_PASSWORD,
  }),
});

// Use in resolvers
const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator(['POST_CREATED']),
    },
  },
  Mutation: {
    createPost: async (_, { input }, context) => {
      const post = await createPost(input);
      
      // Publish event
      await pubsub.publish('POST_CREATED', {
        postCreated: post,
      });
      
      return post;
    },
  },
};
```

## Performance Optimization

### Subscription Optimization
```javascript
// Optimized subscription handling
class OptimizedSubscriptionManager {
  constructor() {
    this.subscriptions = new Map();
    this.batching = new SubscriptionBatcher();
    this.deduplication = new SubscriptionDeduplicator();
  }

  async subscribe(subscriptionId, query, variables, context) {
    // Check for duplicate subscriptions
    const existing = this.deduplication.findDuplicate(query, variables);
    if (existing) {
      return this.addToExistingSubscription(existing, subscriptionId);
    }

    // Create new subscription
    const subscription = await this.createSubscription(subscriptionId, query, variables, context);
    
    // Register for deduplication
    this.deduplication.register(subscription);
    
    return subscription;
  }

  async publish(eventType, payload) {
    // Batch events for efficiency
    await this.batching.batch(eventType, payload);
  }

  getMetrics() {
    return {
      activeSubscriptions: this.subscriptions.size,
      batchedEvents: this.batching.getBatchCount(),
      deduplicated: this.deduplication.getDeduplicationCount(),
    };
  }
}
```

### Event Batching
```javascript
// Event batching for performance
class SubscriptionBatcher {
  constructor(batchSize = 100, batchInterval = 10) {
    this.batchSize = batchSize;
    this.batchInterval = batchInterval;
    this.batches = new Map();
    this.batchCount = 0;
  }

  async batch(eventType, payload) {
    if (!this.batches.has(eventType)) {
      this.batches.set(eventType, []);
    }

    const batch = this.batches.get(eventType);
    batch.push({
      payload,
      timestamp: Date.now(),
    });

    // Send batch if full or interval reached
    if (batch.length >= this.batchSize) {
      await this.sendBatch(eventType);
    }
  }

  async sendBatch(eventType) {
    const batch = this.batches.get(eventType);
    if (!batch || batch.length === 0) {
      return;
    }

    // Send all events in batch
    await Promise.all(
      batch.map(event => this.sendEvent(eventType, event.payload))
    );

    // Clear batch
    this.batches.set(eventType, []);
    this.batchCount++;
  }

  getBatchCount() {
    return this.batchCount;
  }
}
```

### Memory Management
```javascript
// Memory-efficient subscription management
class MemoryEfficientSubscriptions {
  constructor(config) {
    this.subscriptions = new Map();
    this.maxSubscriptions = config.maxSubscriptions || 10000;
    this.cleanupInterval = config.cleanupInterval || 60000;
    this.inactiveTimeout = config.inactiveTimeout || 300000; // 5 minutes
    
    this.startCleanup();
  }

  addSubscription(id, subscription) {
    if (this.subscriptions.size >= this.maxSubscriptions) {
      this.cleanupInactiveSubscriptions();
      
      if (this.subscriptions.size >= this.maxSubscriptions) {
        throw new Error('Maximum subscriptions reached');
      }
    }

    this.subscriptions.set(id, {
      ...subscription,
      lastActivity: Date.now(),
      createdAt: Date.now(),
    });
  }

  removeSubscription(id) {
    this.subscriptions.delete(id);
  }

  updateActivity(id) {
    const subscription = this.subscriptions.get(id);
    if (subscription) {
      subscription.lastActivity = Date.now();
    }
  }

  cleanupInactiveSubscriptions() {
    const now = Date.now();
    for (const [id, subscription] of this.subscriptions) {
      if (now - subscription.lastActivity > this.inactiveTimeout) {
        this.subscriptions.delete(id);
      }
    }
  }

  startCleanup() {
    setInterval(() => {
      this.cleanupInactiveSubscriptions();
    }, this.cleanupInterval);
  }

  getMemoryUsage() {
    return {
      subscriptions: this.subscriptions.size,
      maxSubscriptions: this.maxSubscriptions,
      memoryEstimate: this.estimateMemory(),
    };
  }

  estimateMemory() {
    // Rough memory estimation
    return this.subscriptions.size * 1024; // 1KB per subscription
  }
}
```

## Security Considerations

### WebSocket Authentication
```javascript
// Secure WebSocket authentication
class WebSocketAuth {
  constructor(config) {
    this.tokenValidator = config.tokenValidator;
    this.rateLimiter = config.rateLimiter;
  }

  async authenticateConnection(socket, req) {
    // Extract token
    const token = this.extractToken(req);
    if (!token) {
      throw new AuthenticationError('No token provided');
    }

    // Validate token
    const user = await this.tokenValidator.validate(token);
    if (!user) {
      throw new AuthenticationError('Invalid token');
    }

    // Check rate limits
    const allowed = await this.rateLimiter.checkLimit(user.id);
    if (!allowed) {
      throw new RateLimitError('Too many connections');
    }

    return user;
  }

  extractToken(req) {
    // Check Authorization header
    const authHeader = req.headers.authorization;
    if (authHeader?.startsWith('Bearer ')) {
      return authHeader.slice(7);
    }

    // Check query string
    const url = new URL(req.url, `http://${req.headers.host}`);
    return url.searchParams.get('token');
  }

  async validateSubscription(user, subscription) {
    // Check user permissions
    const hasPermission = await this.checkPermission(user, subscription);
    if (!hasPermission) {
      throw new ForbiddenError('Insufficient permissions');
    }

    // Check subscription limits
    const withinLimits = await this.checkSubscriptionLimits(user);
    if (!withinLimits) {
      throw new RateLimitError('Subscription limit exceeded');
    }

    return true;
  }
}
```

### Input Validation
```javascript
// Subscription input validation
class SubscriptionValidator {
  constructor(schema) {
    this.schema = schema;
    this.maxDepth = 10;
    this.maxComplexity = 1000;
  }

  validate(query, variables) {
    // Parse query
    const document = parse(query);
    
    // Validate query depth
    const depth = this.calculateDepth(document);
    if (depth > this.maxDepth) {
      throw new ValidationError(`Query depth ${depth} exceeds maximum ${this.maxDepth}`);
    }

    // Validate query complexity
    const complexity = this.calculateComplexity(document);
    if (complexity > this.maxComplexity) {
      throw new ValidationError(`Query complexity ${complexity} exceeds maximum ${this.maxComplexity}`);
    }

    // Validate variables
    this.validateVariables(document, variables);

    return true;
  }

  calculateDepth(document) {
    let maxDepth = 0;
    
    const visit = (node, depth = 0) => {
      if (node.selectionSet) {
        maxDepth = Math.max(maxDepth, depth + 1);
        node.selectionSet.selections.forEach(selection => {
          visit(selection, depth + 1);
        });
      }
    };

    document.definitions.forEach(definition => {
      visit(definition);
    });

    return maxDepth;
  }

  calculateComplexity(document) {
    // Implement complexity calculation
    return 1;
  }

  validateVariables(document, variables) {
    // Validate variable types
    const variableDefinitions = document.definitions[0]?.variableDefinitions || [];
    
    for (const varDef of variableDefinitions) {
      const varName = varDef.variable.name.value;
      const varType = varDef.type;
      
      if (!(varName in variables)) {
        if (varDef.defaultValue) {
          continue; // Has default value
        }
        throw new ValidationError(`Missing required variable: ${varName}`);
      }
      
      // Type validation
      this.validateVariableType(varName, variables[varName], varType);
    }
  }

  validateVariableType(name, value, expectedType) {
    // Implement type validation
  }
}
```

### Rate Limiting
```javascript
// Subscription rate limiting
class SubscriptionRateLimiter {
  constructor(config) {
    this.limits = new Map();
    this.windowMs = config.windowMs || 60000;
    this.maxSubscriptions = config.maxSubscriptions || 10;
    this.maxEventsPerSecond = config.maxEventsPerSecond || 100;
  }

  async checkSubscriptionLimit(userId) {
    const userLimits = this.getUserLimits(userId);
    const now = Date.now();
    
    // Reset window if expired
    if (now - userLimits.windowStart > this.windowMs) {
      userLimits.windowStart = now;
      userLimits.subscriptionCount = 0;
    }
    
    userLimits.subscriptionCount++;
    
    if (userLimits.subscriptionCount > this.maxSubscriptions) {
      throw new RateLimitError('Subscription limit exceeded');
    }
    
    return true;
  }

  async checkEventRate(userId) {
    const userLimits = this.getUserLimits(userId);
    const now = Date.now();
    
    // Reset if needed
    if (now - userLimits.eventWindowStart > 1000) {
      userLimits.eventWindowStart = now;
      userLimits.eventCount = 0;
    }
    
    userLimits.eventCount++;
    
    if (userLimits.eventCount > this.maxEventsPerSecond) {
      throw new RateLimitError('Event rate limit exceeded');
    }
    
    return true;
  }

  getUserLimits(userId) {
    if (!this.limits.has(userId)) {
      this.limits.set(userId, {
        windowStart: Date.now(),
        subscriptionCount: 0,
        eventWindowStart: Date.now(),
        eventCount: 0,
      });
    }
    return this.limits.get(userId);
  }
}
```

## Troubleshooting Guide

### Common Subscription Issues

#### Connection Problems
```javascript
// Debugging connection issues
class ConnectionDebugger {
  constructor() {
    this.logs = [];
  }

  async debugConnection(socket, req) {
    const debugInfo = {
      timestamp: new Date(),
      url: req.url,
      headers: req.headers,
      clientIp: req.socket.remoteAddress,
    };

    try {
      // Test authentication
      const token = req.headers.authorization?.split(' ')[1];
      debugInfo.hasToken = !!token;
      
      if (token) {
        const user = await verifyToken(token);
        debugInfo.userId = user?.id;
        debugInfo.isAuthenticated = !!user;
      }

      // Test WebSocket upgrade
      debugInfo.upgradeHeaders = req.headers.upgrade;

      this.log('Connection debug', debugInfo);
      return debugInfo;
    } catch (error) {
      debugInfo.error = error.message;
      this.log('Connection debug failed', debugInfo);
      throw error;
    }
  }

  log(message, data) {
    this.logs.push({
      message,
      data,
      timestamp: new Date(),
    });
  }
}
```

#### Subscription Performance Issues
```javascript
// Performance debugging for subscriptions
class SubscriptionPerformanceDebugger {
  constructor() {
    this.metrics = new Map();
  }

  async measureSubscription(subscriptionId, operation) {
    const start = Date.now();
    const metrics = {
      subscriptionId,
      startTime: start,
      operations: [],
    };

    try {
      const result = await operation();
      metrics.endTime = Date.now();
      metrics.duration = metrics.endTime - metrics.startTime;
      metrics.success = true;
      
      this.recordMetrics(metrics);
      return result;
    } catch (error) {
      metrics.endTime = Date.now();
      metrics.duration = metrics.endTime - metrics.startTime;
      metrics.success = false;
      metrics.error = error.message;
      
      this.recordMetrics(metrics);
      throw error;
    }
  }

  recordMetrics(metrics) {
    const key = metrics.subscriptionId;
    if (!this.metrics.has(key)) {
      this.metrics.set(key, []);
    }
    this.metrics.get(key).push(metrics);
  }

  getPerformanceReport() {
    const report = {};
    
    for (const [subscriptionId, metrics] of this.metrics) {
      const durations = metrics.map(m => m.duration);
      report[subscriptionId] = {
        count: metrics.length,
        averageDuration: durations.reduce((a, b) => a + b, 0) / durations.length,
        maxDuration: Math.max(...durations),
        minDuration: Math.min(...durations),
        successRate: metrics.filter(m => m.success).length / metrics.length,
      };
    }
    
    return report;
  }
}
```

### Debugging Tools
```javascript
// Subscription debugging tools
class SubscriptionDebugger {
  constructor() {
    this.traces = new Map();
  }

  startTrace(subscriptionId) {
    const trace = {
      subscriptionId,
      startTime: Date.now(),
      events: [],
    };
    this.traces.set(subscriptionId, trace);
    return trace;
  }

  addEvent(subscriptionId, event) {
    const trace = this.traces.get(subscriptionId);
    if (trace) {
      trace.events.push({
        ...event,
        timestamp: Date.now(),
      });
    }
  }

  endTrace(subscriptionId) {
    const trace = this.traces.get(subscriptionId);
    if (trace) {
      trace.endTime = Date.now();
      trace.duration = trace.endTime - trace.startTime;
    }
    return trace;
  }

  getTraceReport() {
    const report = [];
    
    for (const [subscriptionId, trace] of this.traces) {
      report.push({
        subscriptionId,
        duration: trace.duration,
        eventCount: trace.events.length,
        events: trace.events,
      });
    }
    
    return report;
  }
}
```

## API Reference

### Subscription Schema API
```graphql
# Subscription schema types
type SubscriptionConfig {
  maxSubscriptionsPerClient: Int!
  maxSubscriptionsTotal: Int!
  heartbeatInterval: Int!
  keepAlive: Int!
  connectionTimeout: Int!
}

type SubscriptionMetrics {
  activeSubscriptions: Int!
  totalSubscriptions: Int!
  eventsPerSecond: Float!
  averageLatency: Float!
  errorRate: Float!
}

type ConnectionInfo {
  id: ID!
  userId: ID!
  createdAt: DateTime!
  lastActivity: DateTime!
  subscriptions: [Subscription!]!
}

type Subscription {
  id: ID!
  query: String!
  variables: JSON
  userId: ID!
  createdAt: DateTime!
  lastEventAt: DateTime
  eventCount: Int!
}
```

### Subscription Management API
```javascript
// Subscription management interface
class SubscriptionAPI {
  constructor(config) {
    this.manager = new SubscriptionManager(config);
  }

  async createSubscription(userId, query, variables) {
    const subscriptionId = generateId();
    
    await this.manager.subscribe(subscriptionId, query, variables, {
      userId,
      createdAt: new Date(),
    });

    return {
      id: subscriptionId,
      query,
      variables,
      userId,
      createdAt: new Date(),
    };
  }

  async cancelSubscription(subscriptionId) {
    const success = await this.manager.unsubscribe(subscriptionId);
    return { success };
  }

  async listSubscriptions(userId) {
    const subscriptions = this.manager.getActiveSubscriptions();
    return subscriptions.filter(s => s.context.userId === userId);
  }

  async getSubscriptionMetrics() {
    return this.manager.getMetrics();
  }
}
```

## Data Models

### Subscription Data Model
```javascript
// Data model for subscriptions
class SubscriptionModel {
  constructor() {
    this.subscriptions = new Map();
    this.connections = new Map();
    this.events = new Map();
  }

  createSubscription(data) {
    const subscription = {
      id: data.id || generateId(),
      query: data.query,
      variables: data.variables,
      userId: data.userId,
      connectionId: data.connectionId,
      createdAt: data.createdAt || new Date(),
      lastEventAt: null,
      eventCount: 0,
      status: 'active',
    };

    this.subscriptions.set(subscription.id, subscription);
    return subscription;
  }

  updateSubscription(id, updates) {
    const subscription = this.subscriptions.get(id);
    if (!subscription) {
      return null;
    }

    Object.assign(subscription, updates);
    return subscription;
  }

  deleteSubscription(id) {
    return this.subscriptions.delete(id);
  }

  getSubscriptionsByUser(userId) {
    return Array.from(this.subscriptions.values())
      .filter(s => s.userId === userId);
  }

  getSubscriptionsByConnection(connectionId) {
    return Array.from(this.subscriptions.values())
      .filter(s => s.connectionId === connectionId);
  }
}
```

### Event Data Model
```javascript
// Data model for events
class EventModel {
  constructor() {
    this.events = new Map();
    this.eventTypes = new Set();
  }

  createEvent(data) {
    const event = {
      id: generateId(),
      type: data.type,
      payload: data.payload,
      createdAt: data.createdAt || new Date(),
      metadata: data.metadata || {},
    };

    this.events.set(event.id, event);
    this.eventTypes.add(event.type);
    
    return event;
  }

  getEvent(id) {
    return this.events.get(id);
  }

  getEventsByType(type) {
    return Array.from(this.events.values())
      .filter(e => e.type === type);
  }

  getEventsByTimeRange(start, end) {
    return Array.from(this.events.values())
      .filter(e => e.createdAt >= start && e.createdAt <= end);
  }

  getEventTypes() {
    return Array.from(this.eventTypes);
  }
}
```

## Deployment Guide

### Docker Deployment
```dockerfile
# Dockerfile for subscription service
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
ENV WS_PORT=4000

# Expose ports
EXPOSE 4000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:9090/health || exit 1

# Start application
CMD ["node", "server.js"]
```

### Kubernetes Deployment
```yaml
# kubernetes/subscription-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subscription-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: subscription-service
  template:
    metadata:
      labels:
        app: subscription-service
    spec:
      containers:
      - name: subscription
        image: subscription-service:latest
        ports:
        - containerPort: 4000
        - containerPort: 9090
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
            port: 9090
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 9090
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: subscription-service
spec:
  selector:
    app: subscription-service
  ports:
  - name: http
    port: 4000
    targetPort: 4000
  - name: metrics
    port: 9090
    targetPort: 9090
  type: ClusterIP
```

## Monitoring & Observability

### Metrics Collection
```javascript
// Subscription metrics collection
const promClient = require('prom-client');

const subscriptionMetrics = {
  activeSubscriptions: new promClient.Gauge({
    name: 'graphql_subscriptions_active',
    help: 'Number of active subscriptions',
  }),

  subscriptionEvents: new promClient.Counter({
    name: 'graphql_subscription_events_total',
    help: 'Total number of subscription events',
    labelNames: ['event_type', 'status'],
  }),

  subscriptionLatency: new promClient.Histogram({
    name: 'graphql_subscription_latency_seconds',
    help: 'Subscription event latency',
    labelNames: ['event_type'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
  }),

  connectionCount: new promClient.Gauge({
    name: 'graphql_websocket_connections',
    help: 'Number of active WebSocket connections',
  }),

  connectionErrors: new promClient.Counter({
    name: 'graphql_websocket_errors_total',
    help: 'Total WebSocket connection errors',
    labelNames: ['error_type'],
  }),
};
```

### Logging Configuration
```javascript
// Structured logging for subscriptions
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'subscription-service' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'subscriptions.log' }),
  ],
});

// Subscription event logging
const eventLogger = {
  logEvent(eventType, payload, subscriptionId) {
    logger.info('Subscription event', {
      eventType,
      subscriptionId,
      payloadSize: JSON.stringify(payload).length,
      timestamp: new Date().toISOString(),
    });
  },

  logError(error, subscriptionId) {
    logger.error('Subscription error', {
      error: error.message,
      stack: error.stack,
      subscriptionId,
      timestamp: new Date().toISOString(),
    });
  },
};
```

### Alerting Rules
```yaml
# alerting/subscription-alerts.yaml
groups:
- name: subscription-alerts
  rules:
  - alert: HighSubscriptionLatency
    expr: histogram_quantile(0.95, rate(graphql_subscription_latency_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High subscription latency"
      description: "P95 subscription latency is above 1 second"

  - alert: HighSubscriptionErrorRate
    expr: rate(graphql_subscription_events_total{status="error"}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High subscription error rate"
      description: "Error rate is above 10%"

  - alert: TooManyConnections
    expr: graphql_websocket_connections > 1000
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Too many WebSocket connections"
      description: "Connection count exceeds 1000"
```

## Testing Strategy

### Unit Testing
```javascript
// Unit tests for subscription functionality
describe('Subscription Manager', () => {
  let manager;

  beforeEach(() => {
    manager = new SubscriptionManager();
  });

  test('creates subscription successfully', async () => {
    const subscription = await manager.subscribe(
      'sub1',
      'subscription { postCreated { id } }',
      {},
      { userId: 'user1' }
    );

    expect(subscription.id).toBe('sub1');
    expect(subscription.query).toContain('postCreated');
  });

  test('removes subscription successfully', async () => {
    await manager.subscribe('sub1', 'subscription { postCreated { id } }', {}, {});
    
    const result = await manager.unsubscribe('sub1');
    expect(result).toBe(true);
    
    const subscriptions = manager.getActiveSubscriptions();
    expect(subscriptions.length).toBe(0);
  });

  test('handles multiple subscriptions', async () => {
    await manager.subscribe('sub1', 'subscription { postCreated { id } }', {}, {});
    await manager.subscribe('sub2', 'subscription { commentAdded { id } }', {}, {});
    
    const subscriptions = manager.getActiveSubscriptions();
    expect(subscriptions.length).toBe(2);
  });
});
```

### Integration Testing
```javascript
// Integration tests for WebSocket connections
describe('WebSocket Integration', () => {
  let wsServer;
  let client;

  beforeAll(async () => {
    wsServer = await createWebSocketServer();
  });

  afterAll(async () => {
    await wsServer.close();
  });

  test('establishes WebSocket connection', async () => {
    client = new WebSocket('ws://localhost:4000/graphql');
    
    await new Promise((resolve, reject) => {
      client.on('open', resolve);
      client.on('error', reject);
    });

    expect(client.readyState).toBe(WebSocket.OPEN);
  });

  test('receives subscription updates', async () => {
    const subscription = {
      id: 'sub1',
      type: 'start',
      payload: {
        query: 'subscription { postCreated { id } }',
      },
    };

    client.send(JSON.stringify(subscription));

    // Wait for event
    const event = await new Promise((resolve) => {
      client.on('message', (data) => {
        const message = JSON.parse(data);
        if (message.type === 'data') {
          resolve(message);
        }
      });
    });

    expect(event.payload.data).toBeDefined();
  });

  test('handles connection errors', async () => {
    const invalidClient = new WebSocket('ws://localhost:4000/invalid');
    
    await new Promise((resolve) => {
      invalidClient.on('error', (error) => {
        expect(error).toBeDefined();
        resolve();
      });
    });
  });
});
```

### Performance Testing
```javascript
// Performance tests for subscriptions
describe('Subscription Performance', () => {
  test('handles high concurrency', async () => {
    const concurrentSubscriptions = 100;
    const manager = new SubscriptionManager();
    
    const startTime = Date.now();
    
    const promises = [];
    for (let i = 0; i < concurrentSubscriptions; i++) {
      promises.push(
        manager.subscribe(`sub${i}`, 'subscription { postCreated { id } }', {}, {})
      );
    }
    
    await Promise.all(promises);
    
    const duration = Date.now() - startTime;
    expect(duration).toBeLessThan(5000); // Should complete in under 5 seconds
    
    const subscriptions = manager.getActiveSubscriptions();
    expect(subscriptions.length).toBe(concurrentSubscriptions);
  });

  test('handles event throughput', async () => {
    const manager = new SubscriptionManager();
    const eventCount = 1000;
    
    // Create subscriptions
    for (let i = 0; i < 10; i++) {
      await manager.subscribe(`sub${i}`, 'subscription { postCreated { id } }', {}, {});
    }
    
    const startTime = Date.now();
    
    // Publish events
    for (let i = 0; i < eventCount; i++) {
      await manager.publish('POST_CREATED', { id: i });
    }
    
    const duration = Date.now() - startTime;
    const eventsPerSecond = eventCount / (duration / 1000);
    
    expect(eventsPerSecond).toBeGreaterThan(100); // Should handle >100 events/second
  });
});
```

## Versioning & Migration

### Subscription Versioning
```javascript
// Subscription versioning strategy
class SubscriptionVersionManager {
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
      migrationGuide: `Migrate from ${version} to ${replacementVersion}`,
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
// Migration strategy for subscription changes
class SubscriptionMigration {
  constructor(config) {
    this.config = config;
    this.steps = [];
  }

  async migrate(fromVersion, toVersion) {
    // Analyze changes
    const changes = this.analyzeChanges(fromVersion, toVersion);
    
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

  analyzeChanges(fromVersion, toVersion) {
    return {
      schemaChanges: [],
      protocolChanges: [],
      breakingChanges: [],
    };
  }

  generateMigrationSteps(changes) {
    const steps = [];
    
    // Handle schema changes
    for (const change of changes.schemaChanges) {
      steps.push({
        type: 'schema_update',
        change,
        action: 'update',
      });
    }
    
    // Handle breaking changes
    for (const change of changes.breakingChanges) {
      steps.push({
        type: 'breaking_change',
        change,
        action: 'migrate',
      });
    }
    
    return steps;
  }

  async executeStep(step) {
    switch (step.type) {
      case 'schema_update':
        await this.updateSchema(step.change);
        break;
      case 'breaking_change':
        await this.handleBreakingChange(step.change);
        break;
      default:
        throw new Error(`Unknown step type: ${step.type}`);
    }
  }
}
```

## Glossary

### Subscription Terms

- **Subscription**: A GraphQL operation that maintains a long-lived connection for real-time updates
- **WebSocket**: The underlying protocol for GraphQL subscriptions
- **Pub/Sub**: Publish/Subscribe pattern for event distribution
- **Heartbeat**: Periodic ping/pong to detect dead connections
- **Backpressure**: Mechanism to handle slow consumers
- **Multiplexing**: Multiple subscriptions on a single connection
- **Filtering**: Selective delivery of subscription events
- **Reconnection**: Automatic re-establishment of broken connections

### Architecture Terms

- **Event Router**: Component that routes events to appropriate subscriptions
- **Connection Pool**: Management of multiple WebSocket connections
- **Subscription Manager**: Central component managing all active subscriptions
- **Event Batching**: Grouping multiple events for efficient delivery
- **Deduplication**: Eliminating duplicate subscription events

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
- WebSocket transport
- Real-time update patterns
- Filtering mechanisms
- Scaling strategies

## Contributing Guidelines

### Development Setup
1. Clone the repository
2. Install dependencies: `npm install`
3. Start Redis: `docker-compose up redis`
4. Run tests: `npm test`
5. Start development server: `npm run dev`

### Code Standards
- Use TypeScript for new implementations
- Follow WebSocket best practices
- Write comprehensive tests
- Update documentation for changes

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Run performance tests
4. Update documentation
5. Submit pull request with description
6. Address review feedback

## License

MIT License

Copyright (c) 2024 GraphQL Subscriptions Team

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