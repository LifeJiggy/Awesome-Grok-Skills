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