"""
API Design Module — Resource modeling, URL design, HTTP semantics, response formatting,
error handling, pagination, and OpenAPI specification generation.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class APIStyle(Enum):
    REST = "rest"
    JSON_API = "json_api"
    GRAPHQL = "graphql"
    GRPC = "grpc"
    HAL = "hal"
    SIREN = "siren"


class PaginationStyle(Enum):
    OFFSET = "offset"
    CURSOR = "cursor"
    KEYSET = "keyset"
    LINK_HEADER = "link_header"


class ErrorCode(Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class FieldDefinition:
    """Definition of an API resource field."""
    name: str
    field_type: str
    required: bool = True
    nullable: bool = False
    default: Any = None
    description: str = ""
    example: Any = None
    enum_values: Optional[List[str]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None

    def to_openapi_schema(self) -> Dict[str, Any]:
        schema: Dict[str, Any] = {"type": self._map_type()}
        if self.field_type.startswith("enum["):
            values = self.field_type[5:-1].split(",")
            schema["enum"] = values
        if self.description:
            schema["description"] = self.description
        if self.example:
            schema["example"] = self.example
        if not self.required:
            pass  # handled at property level
        return schema

    def _map_type(self) -> str:
        mapping = {
            "string": "string", "integer": "integer", "number": "number",
            "boolean": "boolean", "datetime": "string",
        }
        base = self.field_type.split("[")[0]
        return mapping.get(base, "string")


@dataclass
class Resource:
    """An API resource definition."""
    name: str
    path: str
    fields: Dict[str, str] = field(default_factory=dict)
    relationships: Dict[str, str] = field(default_factory=dict)
    searchable_fields: List[str] = field(default_factory=list)
    sortable_fields: List[str] = field(default_factory=list)
    filterable_fields: Dict[str, List[str]] = field(default_factory=dict)
    description: str = ""
    example: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    @property
    def plural_name(self) -> str:
        if self.name.endswith("s"):
            return self.name + "es"
        return self.name + "s"

    @property
    def field_definitions(self) -> List[FieldDefinition]:
        defs = []
        for fname, ftype in self.fields.items():
            defs.append(FieldDefinition(name=fname, field_type=ftype))
        return defs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "fields": self.fields,
            "relationships": self.relationships,
        }


@dataclass
class Endpoint:
    """A generated API endpoint."""
    method: HTTPMethod
    path: str
    description: str
    request_schema: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    query_params: Optional[Dict[str, str]] = None
    path_params: Optional[Dict[str, str]] = None
    status_codes: Dict[int, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    authentication_required: bool = True
    rate_limit: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.method.value,
            "path": self.path,
            "description": self.description,
            "auth_required": self.authentication_required,
        }


@dataclass
class PaginationConfig:
    """Pagination configuration."""
    style: PaginationStyle = PaginationStyle.CURSOR
    default_page_size: int = 20
    max_page_size: int = 100
    page_size_param: str = "page[size]"
    page_number_param: str = "page[number]"
    cursor_param: str = "page[cursor]"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "style": self.style.value,
            "default_size": self.default_page_size,
            "max_size": self.max_page_size,
        }


@dataclass
class ErrorDetail:
    """A structured error detail."""
    code: ErrorCode
    message: str
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    retryable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "code": self.code.value,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.field:
            result["field"] = self.field
        if self.details:
            result["details"] = self.details
        return result


@dataclass
class ErrorResponse:
    """RFC 7807 Problem Details error response."""
    type: str = "about:blank"
    title: str = "Error"
    status: int = 400
    detail: str = ""
    instance: str = ""
    errors: List[ErrorDetail] = field(default_factory=list)
    request_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
        }
        if self.instance:
            result["instance"] = self.instance
        if self.errors:
            result["errors"] = [e.to_dict() for e in self.errors]
        if self.request_id:
            result["request_id"] = self.request_id
        return result


@dataclass
class DesignIssue:
    """A design review issue."""
    rule: str
    message: str
    severity: Severity
    path: str = ""
    suggestion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "message": self.message,
            "severity": self.severity.value,
        }


@dataclass
class OpenAPISpec:
    """Generated OpenAPI specification."""
    openapi_version: str = "3.1.0"
    info: Dict[str, Any] = field(default_factory=dict)
    servers: List[Dict[str, str]] = field(default_factory=list)
    paths: Dict[str, Any] = field(default_factory=dict)
    components: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "openapi": self.openapi_version,
            "info": self.info,
            "servers": self.servers,
            "paths": self.paths,
            "components": self.components,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class APIBuilder:
    """Build and manage API resource definitions and generate endpoints."""

    def __init__(
        self,
        title: str = "API",
        version: str = "1.0.0",
        base_url: str = "https://api.example.com",
        style: str = "rest",
        description: str = "",
    ):
        self.title = title
        self.version = version
        self.base_url = base_url
        self.style = APIStyle(style)
        self.description = description
        self._resources: Dict[str, Resource] = {}
        self._custom_endpoints: List[Endpoint] = []
        self._pagination = PaginationConfig()
        self._error_responses: Dict[int, ErrorResponse] = {}

    def add_resource(self, resource: Resource) -> None:
        self._resources[resource.name] = resource

    def get_resource(self, name: str) -> Optional[Resource]:
        return self._resources.get(name)

    def set_pagination(self, config: PaginationConfig) -> None:
        self._pagination = config

    def generate_endpoints(self, resource_name: str) -> List[Endpoint]:
        """Generate standard CRUD endpoints for a resource."""
        resource = self._resources.get(resource_name)
        if not resource:
            return []

        base_path = resource.path
        single_path = f"{base_path}/{{id}}"

        endpoints = [
            Endpoint(
                method=HTTPMethod.GET,
                path=base_path,
                description=f"List all {resource.plural_name}",
                query_params={
                    "page[size]": "integer (default: 20)",
                    "page[number]": "integer (default: 1)",
                    "sort": f"string (fields: {', '.join(resource.sortable_fields)})",
                    "filter[field]": "string",
                    "fields": "string (sparse fieldsets)",
                },
                response_schema={"type": "array", "items": resource.name},
                tags=[resource.name],
            ),
            Endpoint(
                method=HTTPMethod.POST,
                path=base_path,
                description=f"Create a new {resource.name}",
                request_schema=resource.fields,
                response_schema=resource.fields,
                status_codes={201: "Created", 400: "Validation Error", 409: "Conflict"},
                tags=[resource.name],
            ),
            Endpoint(
                method=HTTPMethod.GET,
                path=single_path,
                description=f"Get a {resource.name} by ID",
                path_params={"id": "string (UUID)"},
                response_schema=resource.fields,
                tags=[resource.name],
            ),
            Endpoint(
                method=HTTPMethod.PUT,
                path=single_path,
                description=f"Replace a {resource.name}",
                request_schema=resource.fields,
                response_schema=resource.fields,
                status_codes={200: "OK", 404: "Not Found", 400: "Validation Error"},
                tags=[resource.name],
            ),
            Endpoint(
                method=HTTPMethod.PATCH,
                path=single_path,
                description=f"Partially update a {resource.name}",
                request_schema={k: f"optional<{v}>" for k, v in resource.fields.items()},
                response_schema=resource.fields,
                tags=[resource.name],
            ),
            Endpoint(
                method=HTTPMethod.DELETE,
                path=single_path,
                description=f"Delete a {resource.name}",
                status_codes={204: "No Content", 404: "Not Found"},
                tags=[resource.name],
            ),
        ]

        # Add relationship endpoints
        for rel_name, rel_type in resource.relationships.items():
            rel_path = f"{base_path}/{{id}}/{rel_name}"
            endpoints.append(Endpoint(
                method=HTTPMethod.GET,
                path=rel_path,
                description=f"Get {rel_name} for a {resource.name}",
                path_params={"id": "string (UUID)"},
                response_schema={"type": "relationship", "target": rel_type},
                tags=[resource.name, rel_name],
            ))

        return endpoints

    def to_openapi(self) -> OpenAPISpec:
        """Generate OpenAPI 3.1 specification."""
        spec = OpenAPISpec(
            info={"title": self.title, "version": self.version, "description": self.description},
            servers=[{"url": self.base_url}],
        )

        schemas = {}
        for name, resource in self._resources.items():
            properties = {}
            for fname, ftype in resource.fields.items():
                prop_type = ftype.split("[")[0] if "[" in ftype else ftype
                properties[fname] = {"type": prop_type}
            schemas[name] = {"type": "object", "properties": properties}

            # Generate paths
            endpoints = self.generate_endpoints(name)
            for ep in endpoints:
                if ep.path not in spec.paths:
                    spec.paths[ep.path] = {}
                operation = {
                    "summary": ep.description,
                    "tags": ep.tags,
                    "responses": {
                        str(code): {"description": desc}
                        for code, desc in ep.status_codes.items()
                    } if ep.status_codes else {"200": {"description": "Success"}},
                }
                spec.paths[ep.path][ep.method.value.lower()] = operation

        spec.components["schemas"] = schemas
        return spec


class DesignValidator:
    """Validate API design against best practices."""

    RULES = [
        ("plural-nouns", "Resource paths must use plural nouns", Severity.ERROR),
        ("no-actions-in-url", "URLs must not contain verbs (use HTTP methods instead)", Severity.ERROR),
        ("max-nesting", "Resource nesting should not exceed 3 levels", Severity.WARNING),
        ("consistent-naming", "URL segments should use kebab-case", Severity.WARNING),
        ("no-trailing-slash", "URLs should not have trailing slashes", Severity.WARNING),
        ("use-https", "Base URL should use HTTPS", Severity.ERROR),
        ("pagination", "List endpoints should support pagination", Severity.WARNING),
        ("error-format", "Errors should follow RFC 7807 Problem Details", Severity.WARNING),
    ]

    def validate(self, api: APIBuilder) -> List[DesignIssue]:
        issues = []

        if not api.base_url.startswith("https"):
            issues.append(DesignIssue(
                rule="use-https", message="Base URL does not use HTTPS",
                severity=Severity.ERROR, suggestion="Change to HTTPS",
            ))

        for name, resource in api._resources.items():
            path_parts = [p for p in resource.path.split("/") if p]
            if len(path_parts) > 3:
                issues.append(DesignIssue(
                    rule="max-nesting",
                    message=f"Resource '{name}' has {len(path_parts)} path segments (max recommended: 3)",
                    severity=Severity.WARNING,
                    path=resource.path,
                ))

            for part in path_parts:
                if not re.match(r"^[a-z0-9\-]+$", part) and not part.startswith("{"):
                    issues.append(DesignIssue(
                        rule="consistent-naming",
                        message=f"Path segment '{part}' should use kebab-case",
                        severity=Severity.WARNING,
                        path=resource.path,
                    ))

        return issues


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the API design toolkit."""
    print("API Design Toolkit")
    print("=" * 60)

    api = APIBuilder(
        title="User Management API",
        version="2.0.0",
        base_url="https://api.example.com/v1",
        style="json_api",
    )

    api.add_resource(Resource(
        name="User", path="/users",
        fields={"name": "string", "email": "string", "role": "enum[admin,user]", "created_at": "datetime"},
        relationships={"organization": "Organization"},
        sortable_fields=["name", "created_at"],
        filterable_fields={"role": ["admin", "user"]},
    ))
    api.add_resource(Resource(
        name="Organization", path="/organizations",
        fields={"name": "string", "plan": "enum[free,pro,enterprise]", "member_count": "integer"},
    ))

    print(f"\nResources: {list(api._resources.keys())}")

    # Generate endpoints
    print("\n--- User Endpoints ---")
    endpoints = api.generate_endpoints("User")
    for ep in endpoints:
        print(f"  {ep.method.value:7s} {ep.path} — {ep.description}")

    # OpenAPI
    openapi = api.to_openapi()
    print(f"\nOpenAPI: {len(openapi.paths)} paths, {len(openapi.components.get('schemas', {}))} schemas")

    # Validation
    print("\n--- Design Validation ---")
    validator = DesignValidator()
    issues = validator.validate(api)
    if issues:
        for issue in issues:
            print(f"  [{issue.severity.value}] {issue.message}")
    else:
        print("  No issues found!")

    # Error response example
    error = ErrorResponse(
        status=422, title="Validation Error",
        detail="The request body contains invalid fields",
        errors=[ErrorDetail(code=ErrorCode.VALIDATION_ERROR, message="Email is required", field="email")],
    )
    print(f"\nError response: {json.dumps(error.to_dict(), indent=2)}")


if __name__ == "__main__":
    main()
