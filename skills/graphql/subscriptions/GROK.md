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