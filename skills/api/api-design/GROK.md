---
name: "api-design"
category: "api"
version: "2.0.0"
tags: ["api", "rest", "design", "openapi", "http", "api-design", "best-practices"]
---

# API Design

## Overview

Comprehensive API design framework for creating consistent, intuitive, and scalable REST, GraphQL, and gRPC APIs. This module covers resource modeling, URL design, HTTP method semantics, request/response formatting, error handling, pagination, filtering, sorting, HATEOAS, content negotiation, and API-first design workflows. Includes OpenAPI 3.1 specification generation, design system enforcement, and API review checklists for teams building public and internal APIs.

## Core Capabilities

- **Resource Modeling**: Define resources with consistent naming, nesting depth limits, and relationship patterns (REST), schema design (GraphQL), and service definitions (gRPC)
- **URL Design**: RESTful URL patterns with proper pluralization, versioning paths, query parameter conventions, and path parameter guidelines
- **HTTP Semantics**: Correct use of methods (GET, POST, PUT, PATCH, DELETE), status codes (2xx, 3xx, 4xx, 5xx), and headers (ETag, Cache-Control, Location)
- **Response Formatting**: JSON:API, HAL, Siren, and custom envelope formats with consistent field naming (camelCase vs snake_case) and ISO 8601 timestamps
- **Error Handling**: RFC 7807 Problem Details, structured error responses, error codes, and retryable vs non-retryable error classification
- **Pagination**: Cursor-based, offset-based, and keyset pagination with consistent link headers and response metadata
- **Filtering & Sorting**: Query parameter conventions for filtering (operators, ranges), sorting (multi-field, direction), and field selection (sparse fieldsets)
- **OpenAPI Generation**: Auto-generate OpenAPI 3.1 specifications from code annotations or design-first schemas

## Usage

```python
from api_design import APIBuilder, Resource, Endpoint, HTTPMethod, ErrorCode

# Design an API with resources
api = APIBuilder(
    title="User Management API",
    version="1.0.0",
    base_url="https://api.example.com/v1",
    style="json_api",
)

# Define resources
api.add_resource(Resource(
    name="User",
    path="/users",
    fields={"name": "string", "email": "string", "role": "enum[admin,user]", "created_at": "datetime"},
    relationships={"organization": "Organization", "teams": "Team[]"},
    searchable_fields=["name", "email", "role"],
    sortable_fields=["name", "created_at", "email"],
    filterable_fields={"role": ["admin", "user"], "status": ["active", "inactive"]},
))

api.add_resource(Resource(
    name="Organization",
    path="/organizations",
    fields={"name": "string", "plan": "enum[free,pro,enterprise]", "member_count": "integer"},
    relationships={"users": "User[]"},
))

# Generate endpoints
endpoints = api.generate_endpoints("User")
for ep in endpoints:
    print(f"  {ep.method.value:7s} {ep.path}")
    print(f"    Description: {ep.description}")
    if ep.query_params:
        print(f"    Query params: {ep.query_params}")
    print(f"    Response: {ep.response_schema}")
```

```python
# Generate OpenAPI spec
openapi = api.to_openapi()
print(f"\nOpenAPI version: {openapi['openapi']}")
print(f"Paths: {len(openapi.get('paths', {}))}")
print(f"Schemas: {len(openapi.get('components', {}).get('schemas', {}))}")

# Validate design
from api_design import DesignValidator
validator = DesignValidator()
issues = validator.validate(api)
for issue in issues:
    print(f"  [{issue.severity}] {issue.message}")
```

## Best Practices

- Design APIs resource-oriented, not action-oriented — use /users not /getUsers
- Always pluralize resource names (/users, not /user)
- Limit resource nesting to 3 levels maximum (/users/{id}/teams/{id}/projects is too deep)
- Use HTTP methods correctly: GET (safe), POST (create), PUT (replace), PATCH (update), DELETE (idempotent)
- Return 201 with Location header for successful resource creation
- Use 204 No Content for successful deletions with no response body
- Implement consistent pagination with next/prev/first/last links
- Use ETags for conditional requests and optimistic concurrency control
- Return RFC 7807 Problem Details for all error responses
- Document every endpoint with request/response examples in OpenAPI

## Related Modules

- **api-versioning** — Version management strategies for API evolution
- **api-security** — Authentication and authorization for API endpoints
- **api-documentation** — Interactive documentation generation
- **api-monitoring** — API usage analytics and performance monitoring
- **backend** → **fastapi-best-practices** — FastAPI implementation of design principles
