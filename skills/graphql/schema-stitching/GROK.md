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