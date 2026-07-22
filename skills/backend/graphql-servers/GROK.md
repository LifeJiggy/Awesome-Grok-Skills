---
name: "graphql-servers"
category: "backend"
version: "2.0.0"
tags: ["backend", "graphql-servers", "api", "federation", "subscriptions"]
---

# GraphQL Servers

## Overview

Production-grade GraphQL server development guide covering schema design, resolver architecture, real-time subscriptions, DataLoader patterns for N+1 prevention, Apollo Federation for distributed schemas, authentication and authorization, query complexity analysis, response caching, and performance monitoring. This module provides patterns for building scalable, type-safe GraphQL APIs that serve mobile, web, and internal clients.

## Core Capabilities

- Schema-first and code-first design with SDL and resolvers
- Resolver architecture with context, field-level auth, and error handling
- WebSocket subscriptions with Apollo Server and Subscription-Transport-WS
- DataLoader batching and caching for N+1 query prevention
- Apollo Federation v2 for distributed microservice schemas
- Role-based and field-level authorization with directives
- Query depth limiting, complexity scoring, and cost analysis
- Response-level caching with Redis and in-memory stores
- Persisted queries and automatic persisted queries (APQ)
- Schema stitching, schema registry, and schema change notifications

## Usage

```graphql
# Schema Definition Language
type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: PaginationInput): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  userCreated: User!
  orderStatusChanged(orderId: ID!): OrderStatusUpdate!
}

type User {
  id: ID!
  email: String!
  name: String!
  orders(first: Int, after: String): OrderConnection!
  createdAt: DateTime!
}

input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input UserFilter {
  search: String
  role: Role
  createdAfter: DateTime
}
```

```python
# Python Strawberry implementation
import strawberry
from typing import Optional
from datetime import datetime

@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: str
    created_at: datetime

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID) -> Optional[User]:
        return await user_repository.get_by_id(id)

    @strawberry.field
    async def users(
        self,
        filter: Optional[UserFilter] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> UserConnection:
        return await user_repository.list(filter, pagination)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> User:
        return await user_repository.create(input)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

## Best Practices

- Design schemas around domain entities, not database tables
- Use connection types (Relay-style) for all list endpoints
- Implement field-level authorization, not just type-level
- Always use DataLoader for relational queries
- Set query depth limits (recommended: 10-15)
- Use query complexity scoring to prevent abuse
- Enable persisted queries for production clients
- Version schemas with `@deprecated` directives before removing fields
- Use custom scalars for dates, URLs, and domain-specific types
- Monitor resolver performance with tracing spans

## Related Modules

- `apollo-server` — TypeScript GraphQL server
- `strawberry` — Python GraphQL library
- `ariadne` — Python schema-first GraphQL
- `apollo-federation` — Distributed schema composition
- `graphiql` — Interactive GraphQL IDE

---

## Advanced Configuration

### Apollo Server Configuration

```typescript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginCacheControl } from '@apollo/server/plugin/cacheControl';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import depthLimit from 'graphql-depth-limit';
import { createComplexityRule } from 'graphql-query-complexity';
import express from 'express';
import http from 'http';

const typeDefs = `#graphql
  type Query {
    # ...
  }
`;

const resolvers = {
  Query: {
    // ...
  },
};

const schema = makeExecutableSchema({ typeDefs, resolvers });

const app = express();
const httpServer = http.createServer(app);

// WebSocket server for subscriptions
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const serverCleanup = useServer(
  {
    schema,
    context: async (ctx) => {
      const token = ctx.connectionParams?.authToken;
      return { user: await verifyToken(token) };
    },
  },
  wsServer
);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
    ApolloServerPluginCacheControl({ defaultMaxAge: 5 }),
  ],
  validationRules: [
    depthLimit(15),
    createComplexityRule({
      maximumComplexity: 1000,
      estimators: [
        simpleEstimator({ defaultComplexity: 1 }),
        fieldExtensionsEstimator(),
      ],
      onComplete: (complexity) => {
        if (complexity > 800) {
          console.warn(`High complexity query: ${complexity}`);
        }
      },
    }),
  ],
});

await server.start();

app.use(
  '/graphql',
  express.json({ limit: '1mb' }),
  expressMiddleware(server, {
    context: async ({ req }) => {
      const token = req.headers.authorization?.split(' ')[1];
      return {
        user: token ? await verifyToken(token) : null,
        dataloaders: createDataLoaders(),
      };
    },
  })
);
```

### Schema Registry and Composition

```yaml
# rover.config.yaml
schemas:
  users:
    graphref: production@current
    subgraph: users
  orders:
    graphref: production@current
    subgraph: orders
  products:
    graphref: production@current
    subgraph: products

composition:
  supergraph: ./supergraph.graphql
  check: true
  publish: true
```

### Federation Configuration

```typescript
// users subgraph
import { buildSubgraphSchema } from '@apollo/subgraph';
import { gql } from 'graphql-tag';

const typeDefs = gql`
  type Query {
    user(id: ID!): User
    users: [User!]!
  }

  type User @key(fields: "id") {
    id: ID!
    email: String!
    name: String!
    orders: [Order!]!
  }

  extend type Order @key(fields: "id") {
    id: ID! @external
    user: User! @external
    user_id: ID! @external
  }
`;

const resolvers = {
  User: {
    __resolveReference(user, { dataLoaders }) {
      return dataLoaders.userLoader.load(user.id);
    },
    orders(user, _, { dataLoaders }) {
      return dataLoaders.ordersByUserLoader.load(user.id);
    },
  },
};
```

---

## Architecture Patterns

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │  Web App  │  │ Mobile   │  │  Internal Services   │  │
│  │ (Apollo   │  │ (Apollo  │  │  (Direct GraphQL     │  │
│  │  Client)  │  │  Client) │  │   over HTTP)         │  │
│  └─────┬────┘  └────┬─────┘  └──────────┬───────────┘  │
└────────┼────────────┼────────────────────┼───────────────┘
         │            │                    │
         ▼            ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                  GraphQL Gateway                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Request Pipeline                     │  │
│  │  ┌──────┐ ┌───────┐ ┌──────┐ ┌───────────────┐ │  │
│  │  │Parse │→│Validate│→│Auth  │→│ Complexity    │ │  │
│  │  │      │ │       │ │      │ │ Check         │ │  │
│  │  └──────┘ └───────┘ └──────┘ └───────┬───────┘ │  │
│  └───────────────────────────────────────┼──────────┘  │
│                                          │              │
│  ┌───────────────────────────────────────▼──────────┐  │
│  │           Schema Composition (Federation)         │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────┐    │  │
│  │  │  Users   │ │  Orders  │ │   Products   │    │  │
│  │  │Subgraph  │ │Subgraph  │ │  Subgraph    │    │  │
│  │  └────┬─────┘ └────┬─────┘ └──────┬───────┘    │  │
│  └───────┼────────────┼───────────────┼─────────────┘  │
└──────────┼────────────┼───────────────┼─────────────────┘
           │            │               │
           ▼            ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Users DB    │ │  Orders DB   │ │  Products DB │
│  (PostgreSQL)│ │  (PostgreSQL)│ │  (MongoDB)   │
└──────────────┘ └──────────────┘ └──────────────┘

N+1 Prevention with DataLoader:

  Query {                                   
    users {                                 
      name                                  
      orders {        ← DataLoader batches
        total           all order loads     
        items {                           into single DB query  
          product {   ← DataLoader batches
            name        all product loads   
          }                                 
        }                                   
      }                                     
    }                                       
  }
```

### Subscription Flow

```
Client                     Server                      Database
  │                          │                            │
  │  WebSocket Connect       │                            │
  │─────────────────────────►│                            │
  │  Connection Ack          │                            │
  │◄─────────────────────────│                            │
  │                          │                            │
  │  Subscription Start      │                            │
  │  { orderStatusChanged }  │                            │
  │─────────────────────────►│                            │
  │                          │  Subscribe to topic        │
  │                          │───────────────────────────►│
  │                          │                            │
  │  ... time passes ...     │                            │
  │                          │                            │
  │                          │  Order updated event       │
  │                          │◄───────────────────────────│
  │                          │                            │
  │  Subscription Data       │                            │
  │  { orderStatusChanged }  │                            │
  │◄─────────────────────────│                            │
  │                          │                            │
```

---

## Integration Guide

### DataLoader Implementation

```typescript
import DataLoader from 'dataloader';
import { GraphQLError } from 'graphql';

// Batch function: receives array of keys, returns array of results
async function batchLoadUsers(ids: readonly string[]): Promise<User[]> {
  const users = await db.users.findMany({
    where: { id: { in: ids as string[] } },
  });

  // Map results back to original key order
  const userMap = new Map(users.map(u => [u.id, u]));
  return ids.map(id => userMap.get(id) || new Error(`User ${id} not found`));
}

// DataLoader factory per request (prevents caching across requests)
function createDataLoaders() {
  return {
    userLoader: new DataLoader(batchLoadUsers, {
      maxBatchSize: 100,
      cache: true,
    }),
    ordersByUserLoader: new DataLoader(async (userIds: readonly string[]) => {
      const orders = await db.orders.findMany({
        where: { userId: { in: userIds as string[] } },
      });
      const ordersByUser = new Map<string, Order[]>();
      userIds.forEach(id => ordersByUser.set(id, []));
      orders.forEach(order => {
        ordersByUser.get(order.userId)!.push(order);
      });
      return userIds.map(id => ordersByUser.get(id) || []);
    }),
  };
}

// Resolver using DataLoader
const resolvers = {
  User: {
    orders: async (parent: User, _, { dataloaders }) => {
      return dataloaders.ordersByUserLoader.load(parent.id);
    },
  },
};
```

### Subscription Implementation

```typescript
import { PubSub } from 'graphql-subscriptions';
import { RedisPubSub } from 'graphql-redis-subscriptions';

// Use Redis for distributed pub/sub
const pubsub = new RedisPubSub({
  connection: {
    host: 'redis-host',
    port: 6379,
  },
});

const EVENTS = {
  ORDER_STATUS_CHANGED: 'ORDER_STATUS_CHANGED',
  USER_CREATED: 'USER_CREATED',
};

const resolvers = {
  Subscription: {
    orderStatusChanged: {
      subscribe: withFilter(
        () => pubsub.asyncIterator([EVENTS.ORDER_STATUS_CHANGED]),
        (payload, variables) => {
          return payload.orderStatusChanged.orderId === variables.orderId;
        }
      ),
      resolve: (payload) => payload.orderStatusChanged,
    },
  },
  Mutation: {
    updateOrderStatus: async (_, { orderId, status }, { user }) => {
      const order = await db.orders.update({
        where: { id: orderId },
        data: { status },
      });

      pubsub.publish(EVENTS.ORDER_STATUS_CHANGED, {
        orderStatusChanged: { orderId, status, updatedAt: new Date() },
      });

      return order;
    },
  },
};
```

### Schema Design Patterns

```graphql
# Connection pattern (Relay-style pagination)
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

# Error union type (instead of exceptions)
union CreateUserResult = User | ValidationError | DuplicateEmailError

type ValidationError {
  field: String!
  message: String!
}

type DuplicateEmailError {
  email: String!
  existingUserId: ID!
}

# Custom scalars
scalar DateTime
scalar URL
scalar JSON
scalar PositiveInt

# Directives
directive @auth(requires: Role = USER) on FIELD_DEFINITION
directive @deprecated(reason: String = "Use newer field") on FIELD_DEFINITION
directive @cacheControl(maxAge: Int!) on FIELD_DEFINITION

enum Role {
  ADMIN
  MANAGER
  USER
}
```

---

## Performance Optimization

| Technique | Impact | When to Use |
|-----------|--------|-------------|
| DataLoader batching | 10-100x fewer DB queries | All relational fields |
| Response caching | 2-10x latency reduction | Read-heavy queries |
| Persisted queries | 30-50% bandwidth reduction | Production clients |
| Query complexity limiting | Prevents abuse | Always in production |
| Schema directive caching | Automatic cache control | Stable data fields |
| Query batching (ABQ) | Fewer HTTP round trips | Mobile clients |
| Fragment reuse | Smaller payloads | Complex UI components |
| Async resolver execution | Better concurrency | Independent field resolution |

### Response Caching

```typescript
import responseCachePlugin from '@apollo/server-plugin-response-cache';
import { RedisCache } from 'cache-manager-redis-store';

const server = new ApolloServer({
  plugins: [
    responseCachePlugin({
      sessionId: (requestContext) =>
        requestContext.request.http?.headers.get('authorization') || null,
    }),
  ],
});

// Redis cache backend
const cache = new RedisCache({
  host: 'redis',
  port: 6379,
  ttl: 300, // 5 minutes default
});

// Field-level cache hints
const typeDefs = gql`
  type Product {
    id: ID!
    name: String! @cacheControl(maxAge: 3600)
    price: Float! @cacheControl(maxAge: 60)
    reviews: [Review!]! @cacheControl(maxAge: 300)
  }
`;
```

### Persisted Queries

```typescript
// Automatic Persisted Queries (APQ)
import { ApolloServerPluginCacheControl } from '@apollo/server/plugin/cacheControl';

const server = new ApolloServer({
  persistedQueries: {
    cache: new KeyvCacheInterface(new RedisCache({ host: 'redis' })),
  },
});

// Client-side: send hash instead of full query
// Client sends: { extensions: { persistedQuery: { sha256Hash: "..." } } }
// Server looks up query by hash, reducing bandwidth
```

---

## Security Considerations

### Query Depth and Complexity

```typescript
import depthLimit from 'graphql-depth-limit';
import { createComplexityRule } from 'graphql-query-complexity';

const server = new ApolloServer({
  validationRules: [
    depthLimit(15),
    createComplexityRule({
      maximumComplexity: 1000,
      estimators: [
        simpleEstimator({ defaultComplexity: 1 }),
        fieldExtensionsEstimator(),
      ],
      onComplete: (complexity) => {
        if (complexity > 800) {
          console.warn(`High complexity: ${complexity}`);
        }
      },
    }),
  ],
});
```

### Field-Level Authorization

```typescript
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';

function authDirectiveTransformer(schema) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const authDirective = getDirective(schema, fieldConfig, 'auth')?.[0];
      if (authDirective) {
        const requires = authDirective.requires || 'USER';
        const originalResolve = fieldConfig.resolve;
        fieldConfig.resolve = (source, args, context, info) => {
          if (!context.user) {
            throw new GraphQLError('Not authenticated');
          }
          if (!hasRole(context.user, requires)) {
            throw new GraphQLError('Not authorized');
          }
          return originalResolve(source, args, context, info);
        };
      }
      return fieldConfig;
    },
  });
}

// Usage in schema
const typeDefs = gql`
  type AdminDashboard {
    systemMetrics: Metrics! @auth(requires: ADMIN)
    userAnalytics: Analytics! @auth(requires: MANAGER)
  }
`;
```

### Introspection Control

```typescript
// Disable introspection in production
const server = new ApolloServer({
  introspection: process.env.NODE_ENV !== 'production',
  allowBatchedHttpRequests: true,
});

// Or disable via plugin
import { ApolloServerPluginLandingPageDisabled } from '@apollo/server/plugin/disabled';

const server = new ApolloServer({
  plugins: [
    process.env.NODE_ENV === 'production'
      ? ApolloServerPluginLandingPageDisabled()
      : ApolloServerPluginLandingPageLocalDefault(),
  ],
});
```

### Rate Limiting

```typescript
import { GraphQLError } from 'graphql';

// Per-query rate limiting
const queryComplexityLimits = {
  QUERY: 1000,
  MUTATION: 500,
  SUBSCRIPTION: 200,
};

async function checkRateLimit(context, operationType) {
  const key = `graphql:${context.user?.id || context.ip}:${operationType}`;
  const count = await redis.incr(key);
  if (count === 1) {
    await redis.expire(key, 60); // 1 minute window
  }

  const limit = queryComplexityLimits[operationType] || 500;
  if (count > limit) {
    throw new GraphQLError('Rate limit exceeded', {
      extensions: { code: 'RATE_LIMITED', retryAfter: 60 },
    });
  }
}
```

---

## Troubleshooting Guide

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| N+1 query errors | Missing DataLoader | Add DataLoader for every relational field |
| `Cannot return null` | Resolver returns null for non-null field | Check resolver logic and data availability |
| Subscription not firing | Wrong PubSub backend for distributed | Use Redis PubSub instead of in-memory |
| Schema composition fails | Federation key mismatch | Verify `@key` fields match across subgraphs |
| Query timeout | Too much data or missing indexes | Add query complexity limits, optimize resolvers |
| Memory leak | DataLoader cache not per-request | Create new DataLoader instances per request |
| Auth bypass | Authorization only at type level | Add field-level `@auth` directives |
| Slow first request | JIT compilation, cold cache | Warm up with health check queries |
| CORS error | Missing origin in config | Add client origin to CORS configuration |
| `Schema must contain types` | Missing directive or scalar definition | Define all custom scalars and directives |
| Introspection exposed | `introspection: true` in production | Disable introspection in production config |

---

## API Reference

### Query Operations

| Operation | Type | Description | Complexity |
|-----------|------|-------------|------------|
| `user(id)` | Query | Fetch single user by ID | 1 |
| `users(filter, pagination)` | Query | List users with filtering | 10 |
| `product(id)` | Query | Fetch single product | 1 |
| `order(id)` | Query | Fetch single order | 2 |
| `orders(userId)` | Query | List user's orders | 5 |

### Mutation Operations

| Operation | Type | Description | Complexity |
|-----------|------|-------------|------------|
| `createUser(input)` | Mutation | Create new user | 5 |
| `updateUser(id, input)` | Mutation | Update user | 5 |
| `deleteUser(id)` | Mutation | Delete user | 3 |
| `createOrder(input)` | Mutation | Create order | 10 |
| `updateOrderStatus(id, status)` | Mutation | Update order status | 5 |

### Subscription Operations

| Operation | Type | Description | Trigger |
|-----------|------|-------------|---------|
| `userCreated` | Subscription | New user registered | `createUser` mutation |
| `orderStatusChanged(orderId)` | Subscription | Order status update | `updateOrderStatus` mutation |

### Response Types

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Standard error response
type GraphQLError {
  message: String!
  path: [String!]
  extensions: ErrorExtensions
}

type ErrorExtensions {
  code: String!
  timestamp: DateTime
  details: JSON
}
```

---

## Data Models

### Core Types

```graphql
scalar DateTime
scalar URL
scalar JSON
scalar PositiveInt
scalar EmailAddress

enum Role {
  ADMIN
  MANAGER
  USER
}

enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

enum SortDirection {
  ASC
  DESC
}
```

### Entity Types

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  role: Role!
  orders(first: Int, after: String): OrderConnection!
  profile: Profile
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Profile {
  bio: String
  avatarUrl: URL
  website: URL
}

type Product {
  id: ID!
  name: String!
  description: String
  price: PositiveInt!
  category: Category!
  reviews(first: Int, after: String): ReviewConnection!
  averageRating: Float
  inStock: Boolean!
  createdAt: DateTime!
}

type Order {
  id: ID!
  user: User!
  items: [OrderItem!]!
  total: PositiveInt!
  status: OrderStatus!
  shippingAddress: Address!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type OrderItem {
  product: Product!
  quantity: PositiveInt!
  unitPrice: PositiveInt!
}
```

### Input Types

```graphql
input CreateUserInput {
  email: EmailAddress!
  name: String!
  password: String!
  role: Role = USER
}

input UpdateUserInput {
  name: String
  email: EmailAddress
  role: Role
}

input CreateOrderInput {
  items: [OrderItemInput!]!
  shippingAddress: AddressInput!
}

input OrderItemInput {
  productId: ID!
  quantity: PositiveInt!
}

input AddressInput {
  street: String!
  city: String!
  state: String!
  zipCode: String!
  country: String!
}

input UserFilter {
  search: String
  role: Role
  createdAfter: DateTime
  createdBefore: DateTime
}

input PaginationInput {
  first: Int
  after: String
  last: Int
  before: String
}

input SortInput {
  field: String!
  direction: SortDirection = ASC
}
```

---

## Deployment Guide

### Docker Configuration

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime

RUN addgroup -g 1001 -S appgroup
RUN adduser -S appuser -u 1001 -G appgroup

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER appuser

EXPOSE 4000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Docker Compose

```yaml
version: "3.9"
services:
  graphql:
    build: .
    ports:
      - "4000:4000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  gateway:
    image: ghcr.io/apollographql/router:latest
    ports:
      - "4000:4000"
    volumes:
      - ./supergraph.graphql:/etc/config/supergraph.graphql
    command: >
      --config /etc/config/router.yaml
      --supergraph /etc/config/supergraph.graphql
```

### Kubernetes Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: graphql-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: graphql-server
  template:
    metadata:
      labels:
        app: graphql-server
    spec:
      containers:
        - name: graphql
          image: registry.example.com/graphql:2.0.0
          ports:
            - containerPort: 4000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: graphql-secrets
                  key: database-url
          livenessProbe:
            httpGet:
              path: /health
              port: 4000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 4000
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

---

## Monitoring and Observability

### Tracing and Metrics

```typescript
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting';
import { ApolloServerPluginInlineTrace } from '@apollo/server/plugin/inlineTrace';
import { v4 as uuidv4 } from 'uuid';

const server = new ApolloServer({
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { none: true },
      sendHeaders: { onlyNames: ['authorization'] },
    }),
    ApolloServerPluginInlineTrace(),
  ],
});

// Custom tracing plugin
const tracingPlugin = {
  async requestDidStart(requestContext) {
    const requestId = uuidv4();
    const startTime = Date.now();

    console.log(`[${requestId}] Query started`);

    return {
      async willSendResponse(requestContext) {
        const duration = Date.now() - startTime;
        console.log(`[${requestId}] Query completed in ${duration}ms`);
      },
      async didEncounterErrors(requestContext) {
        for (const error of requestContext.errors) {
          console.error(`[${requestId}] Error:`, error.message);
        }
      },
    };
  },
};
```

### Prometheus Metrics

```typescript
import { Counter, Histogram, Gauge } from 'prom-client';

const graphqlRequests = new Counter({
  name: 'graphql_requests_total',
  help: 'Total GraphQL requests',
  labelNames: ['operation', 'status'],
});

const graphqlDuration = new Histogram({
  name: 'graphql_request_duration_seconds',
  help: 'GraphQL request duration',
  labelNames: ['operation'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
});

const activeSubscriptions = new Gauge({
  name: 'graphql_active_subscriptions',
  help: 'Number of active subscriptions',
});

// In resolver context
const metricsPlugin = {
  async requestDidStart() {
    const start = Date.now();
    return {
      async willSendResponse({ operationName }) {
        const duration = (Date.now() - start) / 1000;
        graphqlDuration.observe({ operation: operationName }, duration);
        graphqlRequests.inc({ operation: operationName, status: 'success' });
      },
    };
  },
};
```

### Health Checks

```typescript
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', version: '2.0.0' });
});

app.get('/ready', async (req, res) => {
  const checks = {};

  try {
    await db.query('SELECT 1');
    checks.database = 'ok';
  } catch {
    checks.database = 'failed';
  }

  try {
    await redis.ping();
    checks.redis = 'ok';
  } catch {
    checks.redis = 'failed';
  }

  const allHealthy = Object.values(checks).every(v => v === 'ok');
  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'ready' : 'not_ready',
    checks,
  });
});
```

---

## Testing Strategy

### Resolver Unit Tests

```typescript
import { createTestClient } from '@apollo/server/testing';
import { ApolloServer } from '@apollo/server';

describe('User Resolvers', () => {
  let server: ApolloServer;

  beforeEach(async () => {
    server = new ApolloServer({
      typeDefs,
      resolvers,
      context: () => ({
        user: mockUser,
        dataloaders: createMockDataLoaders(),
      }),
    });
  });

  it('fetches user by ID', async () => {
    const { body } = await server.executeOperation({
      query: `query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          email
        }
      }`,
      variables: { id: '1' },
    });

    const result = JSON.parse(JSON.stringify(body));
    expect(result.singleResult.data.user.name).toBe('Test User');
  });

  it('returns null for non-existent user', async () => {
    const { body } = await server.executeOperation({
      query: `query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
        }
      }`,
      variables: { id: '999' },
    });

    const result = JSON.parse(JSON.stringify(body));
    expect(result.singleResult.data.user).toBeNull();
  });
});
```

### Integration Tests

```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

describe('GraphQL Integration', () => {
  let server: ApolloServer;
  let url: string;

  beforeAll(async () => {
    server = new ApolloServer({ typeDefs, resolvers });
    ({ url } = await startStandaloneServer(server, { listen: { port: 0 } }));
  });

  afterAll(async () => {
    await server.stop();
  });

  it('creates and retrieves a user', async () => {
    const createResult = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `mutation CreateUser($input: CreateUserInput!) {
          createUser(input: $input) { id name email }
        }`,
        variables: { input: { email: 'test@example.com', name: 'Test', password: 'securepass123' } },
      }),
    });

    const { data } = await createResult.json();
    expect(data.createUser.id).toBeDefined();

    const getResult = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `query GetUser($id: ID!) { user(id: $id) { id name } }`,
        variables: { id: data.createUser.id },
      }),
    });

    const { data: userData } = await getResult.json();
    expect(userData.user.name).toBe('Test');
  });
});
```

### Subscription Tests

```typescript
import { WebSocket } from 'ws';

describe('GraphQL Subscriptions', () => {
  it('receives order status updates', (done) => {
    const ws = new WebSocket(url.replace('http', 'ws') + '/graphql', {
      headers: { Authorization: `Bearer ${token}` },
    });

    ws.on('open', () => {
      ws.send(JSON.stringify({
        type: 'connection_init',
      }));
    });

    ws.on('message', (data) => {
      const msg = JSON.parse(data.toString());

      if (msg.type === 'connection_ack') {
        ws.send(JSON.stringify({
          id: '1',
          type: 'start',
          payload: {
            query: `subscription OnOrderStatus($orderId: ID!) {
              orderStatusChanged(orderId: $orderId) { status updatedAt }
            }`,
            variables: { orderId: 'order-1' },
          },
        }));
      }

      if (msg.type === 'data' && msg.id === '1') {
        expect(msg.payload.data.orderStatusChanged.status).toBe('SHIPPED');
        ws.close();
        done();
      }
    });
  });
});
```

---

## Versioning and Migration

### Schema Versioning Strategy

```graphql
# Add new fields with @deprecated on old ones
type User {
  id: ID!
  name: String! @deprecated(reason: "Use profile.fullName instead")
  email: String!
  profile: Profile!
}

# Version via headers
# X-GraphQL-Version: 2024-01
# Or via URL: /graphql/v2

# Use schema directives for version tracking
# @since(version: "2.0.0")
# @deprecated(since: "2.0.0", removalVersion: "3.0.0")
```

### Migration Process

```typescript
// 1. Add new field alongside old
type User {
  id: ID!
  email: String!  # old
  contactEmail: String!  # new, same value
}

// 2. Update clients to use new field
// 3. Mark old field as deprecated
type User {
  id: ID!
  email: String! @deprecated(reason: "Use contactEmail")
  contactEmail: String!
}

// 4. Monitor usage of deprecated field
// 5. Remove old field in next major version
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **Schema** | Type definitions describing your GraphQL API (types, queries, mutations, subscriptions) |
| **Resolver** | Function that fetches data for a single field in your schema |
| **DataLoader** | Batching and caching library that prevents N+1 queries |
| **Federation** | Architecture for composing a single schema from multiple subgraphs |
| **Subgraph** | A service owning a portion of a federated schema |
| **Supergraph** | The composed schema from all subgraphs in a federation |
| **Persisted Query** | Server-side stored query identified by hash, reducing bandwidth |
| **PubSub** | Publish-Subscribe pattern for real-time subscription delivery |
| **Connection** | Relay-style pagination pattern with edges, nodes, and cursors |
| **Introspection** | Ability to query the schema itself for documentation and tooling |

---

## Changelog

### 2.0.0 (2024-12-01)

- Added Apollo Federation v2 patterns and configuration
- Added DataLoader implementation guide with batching strategies
- Added query complexity analysis and depth limiting
- Added response caching with Redis backend
- Added persisted queries (APQ) configuration
- Added comprehensive subscription patterns with Redis PubSub
- Expanded testing strategy with integration and subscription tests

### 1.1.0 (2024-06-15)

- Added field-level authorization patterns
- Added error union types pattern
- Added schema design best practices

### 1.0.0 (2024-01-01)

- Initial release
- Core schema design patterns
- Basic resolver architecture
- Subscription fundamentals

---

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Follow GraphQL naming conventions (PascalCase for types, camelCase for fields)
3. Add tests for new patterns (target: 90% coverage)
4. Update this document for any new patterns
5. Validate schema changes with `rover subgraph check`
6. Submit a pull request with a clear description

### Schema Style Guide

- Use descriptive field names that convey meaning
- Always use non-null (`!`) for required fields
- Use enums for bounded sets of values
- Provide default values for optional arguments
- Use input types for mutation arguments
- Return connection types for list queries

---

## License

MIT License. See [LICENSE](LICENSE) for details.
