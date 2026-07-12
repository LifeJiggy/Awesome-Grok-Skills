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