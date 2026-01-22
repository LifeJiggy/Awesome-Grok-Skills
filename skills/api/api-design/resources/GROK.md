# API Design

## Overview

API Design encompasses the principles, patterns, and best practices for designing interfaces that enable software systems to communicate effectively. This skill covers RESTful design principles, OpenAPI specification, versioning strategies, and API security patterns. Well-designed APIs provide intuitive, consistent, and evolvable interfaces that developers can easily understand and integrate with.

## Core Capabilities

RESTful architecture provides resource-oriented URLs with HTTP methods for CRUD operations. OpenAPI specification enables documentation, code generation, and tooling integration. Pagination, filtering, and sorting patterns handle large data sets. Error handling provides meaningful responses with appropriate status codes.

Authentication and authorization patterns including OAuth 2.0, API keys, and JWT tokens secure APIs. Rate limiting protects services from abuse. Versioning strategies ensure backward compatibility during evolution. HATEOAS enables discoverable APIs through hypermedia controls.

## Usage Examples

```python
from api_design import APIDesign

api = APIDesign()

api.create_openapi_spec(
    title="Product Catalog API",
    version="1.0.0",
    description="API for managing product catalog"
)

api.add_server(
    url="https://api.example.com/v1",
    description="Production server"
)

api.add_server(
    url="https://staging-api.example.com/v1",
    description="Staging server"
)

api.add_tag(name="Products", description="Product management endpoints")
api.add_tag(name="Orders", description="Order management endpoints")

user_schema = api.create_schema(
    schema_name="User",
    properties={
        "id": {"type": "string", "format": "uuid"},
        "email": {"type": "string", "format": "email"},
        "name": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"}
    },
    required=["email", "name"]
)

product_schema = api.create_schema(
    schema_name="Product",
    properties={
        "id": {"type": "string", "format": "uuid"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "price": {"type": "number", "format": "decimal"},
        "category": {"type": "string"},
        "in_stock": {"type": "boolean"}
    },
    required=["name", "price"]
)

api.create_security_scheme(
    scheme_name="bearerAuth",
    scheme_type="http",
    bearer_format="JWT"
)

api.create_security_scheme(
    scheme_name="apiKeyAuth",
    scheme_type="apiKey"
)

api.create_path(
    path="/products",
    operations={
        "get": {
            "operationId": "listProducts",
            "summary": "List all products",
            "tags": ["Products"],
            "parameters": api.create_pagination_params() + api.create_sorting_params(),
            "responses": {
                "200": api.create_response(200, "List of products", schema={"type": "array", "items": api.create_reference("Product")})
            }
        },
        "post": {
            "operationId": "createProduct",
            "summary": "Create a new product",
            "tags": ["Products"],
            "requestBody": api.create_request_body(
                description="Product data",
                required=True,
                schema=api.create_reference("Product")
            ),
            "responses": {
                "201": api.create_response(201, "Product created", schema=api.create_reference("Product")),
                "400": api.create_response(400, "Invalid input")
            }
        }
    }
)

api.create_path(
    path="/products/{productId}",
    operations={
        "get": {
            "operationId": "getProduct",
            "summary": "Get a product by ID",
            "tags": ["Products"],
            "parameters": [
                api.create_parameter("productId", "path", "Product ID", required=True, schema={"type": "string", "format": "uuid"})
            ],
            "responses": {
                "200": api.create_response(200, "Product details", schema=api.create_reference("Product")),
                "404": api.create_response(404, "Product not found")
            }
        },
        "put": {
            "operationId": "updateProduct",
            "summary": "Update a product",
            "tags": ["Products"],
            "parameters": [
                api.create_parameter("productId", "path", "Product ID", required=True, schema={"type": "string"})
            ],
            "requestBody": api.create_request_body(schema=api.create_reference("Product")),
            "responses": {
                "200": api.create_response(200, "Product updated"),
                "404": api.create_response(404, "Product not found")
            }
        },
        "delete": {
            "operationId": "deleteProduct",
            "summary": "Delete a product",
            "tags": ["Products"],
            "parameters": [
                api.create_parameter("productId", "path", "Product ID", required=True)
            ],
            "responses": {
                "204": api.create_response(204, "Product deleted"),
                "404": api.create_response(404, "Product not found")
            }
        }
    }
)

api.create_path(
    path="/orders",
    operations={
        "get": {
            "operationId": "listOrders",
            "summary": "List user's orders",
            "tags": ["Orders"],
            "security": [{"bearerAuth": []}],
            "parameters": api.create_pagination_params(),
            "responses": {
                "200": api.create_response(200, "List of orders")
            }
        },
        "post": {
            "operationId": "createOrder",
            "summary": "Create a new order",
            "tags": ["Orders"],
            "requestBody": api.create_request_body(
                required=True,
                schema={
                    "type": "object",
                    "properties": {
                        "product_ids": {"type": "array", "items": {"type": "string"}},
                        "quantity": {"type": "integer"}
                    }
                }
            ),
            "responses": {
                "201": api.create_response(201, "Order created")
            }
        }
    }
)

api.configure_rate_limiting(requests_per_minute=100, burst=200)

api.create_versioning_strategy(
    strategy="url",
    header_name="API-Version",
    url_pattern="/v{version}"
)

api.add_deprecation_notice(
    deprecation_date="2024-06-01",
    sunset_date="2024-12-31",
    alternative="/v2/products"
)

api.add_example(
    example_name="SampleProduct",
    value={"name": "Laptop", "price": 999.99},
    summary="Sample product",
    description="A sample laptop product"
)
```

## Best Practices

Design APIs around resources and use consistent URL patterns. Use proper HTTP methods and status codes for semantics. Implement pagination for all list endpoints to handle large datasets. Version APIs from the start and maintain backward compatibility.

Document all endpoints thoroughly with examples. Use consistent error response formats across the API. Implement proper authentication and authorization for all endpoints. Use OpenAPI for documentation and tooling integration.

## Related Skills

- RESTful Services (implementation patterns)
- Microservices (architecture patterns)
- API Security (authentication patterns)
- GraphQL (alternative API paradigm)

## Use Cases

Public APIs enable third-party developers to build integrations. Internal APIs connect microservices in distributed architectures. Mobile backends expose data and functionality to mobile applications. Partner APIs securely share data with business partners.
