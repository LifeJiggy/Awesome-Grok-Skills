# GraphQL

## Overview

GraphQL is a query language and runtime for APIs that enables clients to request exactly the data they need and nothing more. This skill covers schema design, query language, mutations, subscriptions, and tooling. GraphQL addresses over-fetching and under-fetching problems common with REST APIs by giving clients the power to specify their data requirements.

## Core Capabilities

Type system defines the schema with objects, scalars, enums, unions, and interfaces. Queries fetch data with flexible selection sets and arguments. Mutations modify data with input types for complex payloads. Subscriptions enable real-time updates through server-sent events.

Connections pattern implements pagination with edges and nodes. Directives customize schema behavior with @auth, @cache, and custom directives. Introspection enables powerful developer tools and IDE integration. Code generation produces type-safe client code from schemas.

## Usage Examples

```python
from graphql import GraphQL

gql = GraphQL()

gql.create_schema()

gql.create_scalar_type("DateTime", "ISO 8601 datetime string")
gql.create_scalar_type("UUID", "Universally unique identifier")

gql.create_enum_type(
    "OrderStatus",
    ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"],
    "Status of an order"
)

gql.create_object_type(
    "Product",
    {
        "id": {"type": {"kind": "SCALAR", "name": "ID"}},
        "name": {"type": {"kind": "SCALAR", "name": "String"}},
        "description": {"type": {"kind": "SCALAR", "name": "String"}},
        "price": {"type": {"kind": "SCALAR", "name": "Float"}},
        "category": {"type": {"kind": "SCALAR", "name": "String"}},
        "inStock": {"type": {"kind": "SCALAR", "name": "Boolean"}}
    },
    description="A product in the catalog"
)

gql.create_input_type(
    "CreateProductInput",
    {
        "name": {"type": {"kind": "SCALAR", "name": "String"}},
        "description": {"type": {"kind": "SCALAR", "name": "String"}},
        "price": {"type": {"kind": "SCALAR", "name": "Float"}},
        "category": {"type": {"kind": "SCALAR", "name": "String"}}
    },
    description="Input for creating a product"
)

gql.create_interface_type(
    "Node",
    {
        "id": {"type": {"kind": "SCALAR", "name": "ID"}}
    },
    description="An object with an ID"
)

gql.create_union_type(
    "SearchResult",
    ["Product", "Category", "Article"],
    description="Result of a search query"
)

gql.create_connection_type("Product")
gql.create_pagination_info()
gql.create_order_enum()

gql.create_query_type([
    gql.create_query_field("products", {"kind": "LIST", "ofType": {"kind": "OBJECT", "name": "Product"}}, [
        {"name": "category", "type": {"kind": "SCALAR", "name": "String"}},
        {"name": "first", "type": {"kind": "SCALAR", "name": "Int"}},
        {"name": "after", "type": {"kind": "SCALAR", "name": "String"}}
    ], "Get all products with pagination"),
    gql.create_query_field("product", {"kind": "OBJECT", "name": "Product"}, [
        {"name": "id", "type": {"kind": "NON_NULL", "ofType": {"kind": "SCALAR", "name": "ID"}}}
    ], "Get a single product"),
    gql.create_query_field("search", {"kind": "LIST", "ofType": {"kind": "UNION", "name": "SearchResult"}}, [
        {"name": "query", "type": {"kind": "SCALAR", "name": "String"}}
    ], "Search products and categories")
])

gql.create_mutation_type([
    gql.create_mutation_field("createProduct", "CreateProductInput", {"kind": "OBJECT", "name": "Product"}, "Create a new product"),
    gql.create_mutation_field("updateProduct", "UpdateProductInput", {"kind": "OBJECT", "name": "Product"}, "Update an existing product"),
    gql.create_mutation_field("deleteProduct", "DeleteProductInput", {"kind": "SCALAR", "name": "Boolean"}, "Delete a product")
])

gql.create_subscription_type([
    gql.create_subscription_field("productCreated", {"kind": "OBJECT", "name": "Product"}, "Subscribe to new products"),
    gql.create_subscription_field("productUpdated", {"kind": "OBJECT", "name": "Product"}, "Subscribe to product updates")
])

gql.configure_auth_directive(requires_auth=True, roles=["admin", "user"])
gql.configure_cache_directive(max_age=3600, scope="PUBLIC")
```

## Best Practices

Design schemas around domain objects and use cases, not endpoints. Use non-null fields consistently to indicate required data. Implement pagination with cursor-based connections following Relay specification. Use input types for mutations to support evolution.

Leverage interfaces and unions for polymorphic responses. Add descriptions to all types and fields for documentation. Implement proper error handling with union types. Use batching and caching to resolve N+1 query problems.

## Related Skills

- API Design (REST and general API patterns)
- Microservices (distributed system patterns)
- Database Administration (data layer patterns)
- Real-time Systems (subscription patterns)

## Use Cases

Mobile applications benefit from reduced data transfer by requesting only needed fields. B2B integrations enable partners to build custom data shapes without API changes. Analytics platforms aggregate data from multiple sources with flexible queries. Internal tools reduce frontend complexity with declarative data requirements.
