---
name: "api-documentation"
category: "api"
version: "2.0.0"
tags: ["api", "documentation", "openapi", "swagger", "interactive-docs", "sdk-generation"]
---

# API Documentation

## Overview

Automated API documentation generation platform that produces interactive, always-current documentation from OpenAPI 3.1 specifications, code annotations, and schema definitions. This module supports Swagger UI, Redoc, Stoplight Elements, and custom documentation themes with interactive try-it-now functionality, SDK code generation in 10+ languages, changelog generation, and documentation-as-code workflows with CI/CD integration.

## Core Capabilities

- **OpenAPI Generation**: Auto-generate OpenAPI 3.1 specs from FastAPI, Flask, Express, Django, and Spring Boot annotations
- **Interactive Docs**: Deploy Swagger UI, Redoc, or Stoplight Elements with try-it-now functionality
- **SDK Generation**: Auto-generate client SDKs in Python, TypeScript, Go, Java, Ruby, C#, PHP, and more
- **Multi-Version Docs**: Side-by-side documentation for multiple API versions with version switcher
- **Changelog Generation**: Auto-generate changelogs from OpenAPI schema diffs between versions
- **Code Samples**: Auto-generate code examples in multiple languages for every endpoint
- **Documentation Testing**: Validate documentation accuracy against running API endpoints
- **Theme Customization**: Custom branding, color schemes, and layout for documentation portals

## Usage

```python
from api_documentation import (
    DocGenerator, DocFormat, CodeSampleGenerator, SDKGenerator
)

# Generate documentation from OpenAPI spec
generator = DocGenerator(
    title="User Management API",
    version="2.0.0",
    description="RESTful API for user and organization management",
    contact={"name": "API Team", "email": "api@example.com"},
)

# Add endpoints
generator.add_endpoint(
    method="GET", path="/users",
    summary="List all users",
    description="Returns a paginated list of users with optional filtering",
    parameters=[
        {"name": "page[size]", "in": "query", "schema": {"type": "integer", "default": 20}},
        {"name": "filter[role]", "in": "query", "schema": {"type": "string", "enum": ["admin", "user"]}},
    ],
    response_schema={
        "type": "object",
        "properties": {
            "data": {"type": "array", "items": {"$ref": "#/components/schemas/User"}},
            "meta": {"$ref": "#/components/schemas/Pagination"},
        },
    },
    examples={
        "success": {"value": {"data": [{"id": "123", "name": "Alice"}], "meta": {"total": 42}}},
    },
)

# Generate docs
html = generator.generate(format=DocFormat.HTML)
swagger_json = generator.generate(format=DocFormat.OPENAPI_JSON)
print(f"Generated: {len(html)} chars HTML")
print(f"OpenAPI spec: {len(swagger_json)} chars JSON")

# Generate code samples
samples = CodeSampleGenerator()
for lang in ["python", "javascript", "go", "curl"]:
    code = samples.generate(
        method="GET", url="https://api.example.com/users",
        headers={"Authorization": "Bearer <token>"},
        language=lang,
    )
    print(f"\n{lang.upper()}:")
    print(f"  {code[:80]}...")
```

## Best Practices

- Generate documentation from the same schema used for validation — single source of truth
- Include request and response examples for every endpoint
- Document all error codes and their meanings with troubleshooting guidance
- Use API references (OpenAPI) separate from guides and tutorials
- Version documentation alongside the API — never let docs drift from implementation
- Include authentication guides with step-by-step getting started instructions
- Test documentation examples against the live API in CI/CD
- Provide SDK generation for popular languages to reduce integration friction
- Include rate limit and pagination documentation prominently
- Add changelog and migration guides for every version release

## Related Modules

- **api-design** — Resource design that drives documentation structure
- **api-versioning** — Version management for multi-version documentation
- **api-security** — Security documentation for authentication and authorization
- **api-monitoring** — API usage data to identify documentation gaps
- **backend** → **fastapi-best-practices** — FastAPI auto-documentation integration
