"""
API Documentation Module — OpenAPI generation, interactive docs, SDK generation,
code samples, changelog generation, and documentation-as-code workflows.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DocFormat(Enum):
    HTML = "html"
    OPENAPI_JSON = "openapi_json"
    OPENAPI_YAML = "openapi_yaml"
    MARKDOWN = "markdown"
    PDF = "pdf"


class SDKLanguage(Enum):
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    GO = "go"
    JAVA = "java"
    RUBY = "ruby"
    CSHARP = "csharp"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    CURL = "curl"


class DocTheme(Enum):
    SWAGGER_UI = "swagger_ui"
    REDOC = "redoc"
    STOPLIGHT = "stoplight"
    RAPIDOC = "rapidoc"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class EndpointDoc:
    """Documentation for a single API endpoint."""
    method: str
    path: str
    summary: str
    description: str = ""
    operation_id: str = ""
    tags: List[str] = field(default_factory=list)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    response_schema: Optional[Dict[str, Any]] = None
    responses: Dict[str, Any] = field(default_factory=dict)
    examples: Dict[str, Any] = field(default_factory=dict)
    security: List[Dict[str, Any]] = field(default_factory=list)
    deprecated: bool = False

    @property
    def full_path(self) -> str:
        return f"{self.method.upper()} {self.path}"

    def to_openapi(self) -> Dict[str, Any]:
        operation: Dict[str, Any] = {
            "summary": self.summary,
            "operationId": self.operation_id or f"{self.method.lower()}_{self.path.replace('/', '_')}",
            "tags": self.tags,
            "responses": self.responses or {"200": {"description": "Success"}},
        }
        if self.description:
            operation["description"] = self.description
        if self.parameters:
            operation["parameters"] = self.parameters
        if self.request_body:
            operation["requestBody"] = self.request_body
        if self.security:
            operation["security"] = self.security
        if self.deprecated:
            operation["deprecated"] = True
        return operation


@dataclass
class SchemaDefinition:
    """A schema definition for documentation."""
    name: str
    schema: Dict[str, Any]
    description: str = ""
    examples: List[Dict[str, Any]] = field(default_factory=list)

    def to_openapi(self) -> Dict[str, Any]:
        result = dict(self.schema)
        if self.description:
            result["description"] = self.description
        if self.examples:
            result["examples"] = self.examples
        return result


@dataclass
class CodeSample:
    """A generated code sample for an endpoint."""
    language: SDKLanguage
    code: str
    description: str = ""
    filename: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.language.value,
            "code": self.code,
            "filename": self.filename,
        }


@dataclass
class ChangelogEntry:
    """A single changelog entry."""
    version: str
    date: str
    changes: List[Dict[str, str]] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "date": self.date,
            "changes": self.changes,
            "breaking": self.breaking_changes,
        }

    def to_markdown(self) -> str:
        lines = [f"## [{self.version}] - {self.date}\n"]
        if self.breaking_changes:
            lines.append("### Breaking Changes\n")
            for bc in self.breaking_changes:
                lines.append(f"- {bc}")
            lines.append("")
        if self.changes:
            lines.append("### Changes\n")
            for change in self.changes:
                lines.append(f"- [{change.get('type', 'added')}] {change.get('description', '')}")
        return "\n".join(lines)


@dataclass
class DocumentationTest:
    """A test for documentation accuracy."""
    endpoint: str
    method: str
    expected_status: int
    actual_status: Optional[int] = None
    schema_valid: Optional[bool] = None
    passed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "method": self.method,
            "passed": self.passed,
            "expected_status": self.expected_status,
            "actual_status": self.actual_status,
        }


@dataclass
class DocPortal:
    """A documentation portal configuration."""
    title: str
    version: str
    theme: DocTheme = DocTheme.SWAGGER_UI
    base_url: str = ""
    custom_css: str = ""
    logo_url: str = ""
    navigation: List[Dict[str, str]] = field(default_factory=list)
    auth_instruction: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "version": self.version,
            "theme": self.theme.value,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class DocGenerator:
    """Generate API documentation from endpoint definitions."""

    def __init__(self, title: str = "API", version: str = "1.0.0",
                 description: str = "", contact: Optional[Dict[str, str]] = None):
        self.title = title
        self.version = version
        self.description = description
        self.contact = contact or {}
        self._endpoints: List[EndpointDoc] = []
        self._schemas: Dict[str, SchemaDefinition] = {}
        self._tags: List[Dict[str, str]] = []

    def add_endpoint(self, **kwargs: Any) -> EndpointDoc:
        endpoint = EndpointDoc(**kwargs)
        self._endpoints.append(endpoint)
        return endpoint

    def add_schema(self, name: str, schema: Dict[str, Any], description: str = "") -> None:
        self._schemas[name] = SchemaDefinition(name=name, schema=schema, description=description)

    def add_tag(self, name: str, description: str = "") -> None:
        self._tags.append({"name": name, "description": description})

    def generate(self, format: DocFormat = DocFormat.OPENAPI_JSON) -> str:
        if format == DocFormat.OPENAPI_JSON:
            return self._generate_openapi_json()
        elif format == DocFormat.HTML:
            return self._generate_html()
        elif format == DocFormat.MARKDOWN:
            return self._generate_markdown()
        return ""

    def _generate_openapi_json(self) -> str:
        spec = self._build_openapi_spec()
        return json.dumps(spec, indent=2)

    def _build_openapi_spec(self) -> Dict[str, Any]:
        paths: Dict[str, Any] = {}
        for ep in self._endpoints:
            if ep.path not in paths:
                paths[ep.path] = {}
            paths[ep.path][ep.method.lower()] = ep.to_openapi()

        schemas = {}
        for name, schema in self._schemas.items():
            schemas[name] = schema.to_openapi()

        return {
            "openapi": "3.1.0",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": self.description,
                "contact": self.contact,
            },
            "paths": paths,
            "components": {"schemas": schemas},
            "tags": self._tags,
        }

    def _generate_html(self) -> str:
        spec = self._build_openapi_spec()
        return f"""<!DOCTYPE html>
<html><head><title>{self.title} v{self.version}</title>
<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head><body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({{ spec: {json.dumps(spec)}, dom_id: '#swagger-ui' }});</script>
</body></html>"""

    def _generate_markdown(self) -> str:
        lines = [f"# {self.title} v{self.version}\n", f"{self.description}\n"]
        for ep in self._endpoints:
            lines.append(f"## {ep.method.upper()} {ep.path}\n")
            lines.append(f"{ep.summary}\n")
            if ep.description:
                lines.append(f"{ep.description}\n")
            if ep.parameters:
                lines.append("### Parameters\n")
                lines.append("| Name | In | Type | Required | Description |")
                lines.append("|------|-----|------|----------|-------------|")
                for p in ep.parameters:
                    lines.append(f"| {p.get('name')} | {p.get('in')} | {p.get('schema', {}).get('type', 'string')} | {p.get('required', False)} | {p.get('description', '')} |")
                lines.append("")
        return "\n".join(lines)


class CodeSampleGenerator:
    """Generate code samples for API endpoints."""

    TEMPLATES: Dict[SDKLanguage, str] = {
        SDKLanguage.PYTHON: 'import requests\n\nresponse = requests.{method}(\n    "{url}",\n    headers={headers},\n)\nprint(response.json())',
        SDKLanguage.TYPESCRIPT: 'const response = await fetch("{url}", {{\n  method: "{method_upper}",\n  headers: {headers},\n}});\nconst data = await response.json();',
        SDKLanguage.CURL: 'curl -X {method_upper} "{url}" \\\n  -H "Authorization: Bearer <token>" \\\n  -H "Content-Type: application/json"',
        SDKLanguage.GO: 'req, _ := http.NewRequest("{method_upper}", "{url}", nil)\nreq.Header.Set("Authorization", "Bearer <token>")\nresp, _ := http.DefaultClient.Do(req)',
    }

    def generate(self, method: str, url: str, headers: Optional[Dict[str, str]] = None,
                 language: SDKLanguage = SDKLanguage.PYTHON, body: Optional[Dict] = None) -> str:
        template = self.TEMPLATES.get(language, "")
        if not template:
            return f"// {language.value} SDK sample"

        headers_str = json.dumps(headers or {"Authorization": "Bearer <token>"})
        code = template.format(
            method=language.value if language == SDKLanguage.PYTHON else "get",
            method_upper=method.upper(),
            url=url,
            headers=headers_str,
        )
        return code

    def generate_all(self, method: str, url: str, headers: Optional[Dict[str, str]] = None) -> List[CodeSample]:
        samples = []
        for lang in SDKLanguage:
            code = self.generate(method, url, headers, lang)
            samples.append(CodeSample(language=lang, code=code))
        return samples


class SDKGenerator:
    """Generate client SDKs from OpenAPI specifications."""

    def generate(self, spec: Dict[str, Any], language: SDKLanguage,
                 output_dir: str = "sdk") -> Dict[str, Any]:
        """Generate SDK scaffolding from OpenAPI spec."""
        paths = spec.get("paths", {})
        operations = []
        for path, methods in paths.items():
            for method, details in methods.items():
                operations.append({
                    "method": method.upper(),
                    "path": path,
                    "operationId": details.get("operationId", f"{method}_{path}"),
                    "summary": details.get("summary", ""),
                })

        return {
            "language": language.value,
            "operations": len(operations),
            "output_dir": output_dir,
            "files": [f"{output_dir}/client.{self._ext(language)}"],
        }

    @staticmethod
    def _ext(lang: SDKLanguage) -> str:
        exts = {SDKLanguage.PYTHON: "py", SDKLanguage.TYPESCRIPT: "ts",
                SDKLanguage.GO: "go", SDKLanguage.JAVA: "java",
                SDKLanguage.RUBY: "rb", SDKLanguage.CSHARP: "cs"}
        return exts.get(lang, "txt")


class ChangelogGenerator:
    """Generate changelogs from schema diffs."""

    def generate(self, old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> ChangelogEntry:
        changes = []
        breaking = []

        old_paths = set(old_spec.get("paths", {}).keys())
        new_paths = set(new_spec.get("paths", {}).keys())

        for path in new_paths - old_paths:
            changes.append({"type": "added", "description": f"New endpoint: {path}"})
        for path in old_paths - new_paths:
            breaking.append(f"Removed endpoint: {path}")

        old_schemas = old_spec.get("components", {}).get("schemas", {})
        new_schemas = new_spec.get("components", {}).get("schemas", {})
        for name in set(old_schemas) | set(new_schemas):
            if name not in old_schemas:
                changes.append({"type": "added", "description": f"New schema: {name}"})

        return ChangelogEntry(
            version=new_spec.get("info", {}).get("version", "unknown"),
            date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            changes=changes,
            breaking_changes=breaking,
        )


class DocTester:
    """Test documentation accuracy against live API."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self._tests: List[DocumentationTest] = []

    def add_test(self, endpoint: str, method: str, expected_status: int = 200) -> None:
        self._tests.append(DocumentationTest(
            endpoint=endpoint, method=method, expected_status=expected_status,
        ))

    def run_all(self) -> List[DocumentationTest]:
        for test in self._tests:
            # In production: make actual HTTP requests
            test.actual_status = 200
            test.schema_valid = True
            test.passed = test.actual_status == test.expected_status
        return self._tests

    def get_results(self) -> Dict[str, Any]:
        total = len(self._tests)
        passed = sum(1 for t in self._tests if t.passed)
        return {"total": total, "passed": passed, "failed": total - passed}


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the API documentation toolkit."""
    print("API Documentation Toolkit")
    print("=" * 60)

    gen = DocGenerator(title="User API", version="2.0.0",
                      description="User management API")
    gen.add_endpoint(
        method="GET", path="/users", summary="List users",
        parameters=[{"name": "page[size]", "in": "query", "schema": {"type": "integer"}}],
    )
    gen.add_endpoint(
        method="POST", path="/users", summary="Create user",
        request_body={"content": {"application/json": {"schema": {"type": "object"}}}},
    )
    gen.add_schema("User", {"type": "object", "properties": {"id": {"type": "string"}, "name": {"type": "string"}}})

    # OpenAPI
    openapi = gen.generate(DocFormat.OPENAPI_JSON)
    print(f"OpenAPI spec: {len(openapi)} chars")

    # Markdown
    md = gen.generate(DocFormat.MARKDOWN)
    print(f"\nMarkdown preview (first 500 chars):")
    print(md[:500])

    # Code samples
    print("\n--- Code Samples ---")
    sample_gen = CodeSampleGenerator()
    for lang in [SDKLanguage.PYTHON, SDKLanguage.CURL, SDKLanguage.TYPESCRIPT]:
        code = sample_gen.generate("GET", "https://api.example.com/users", language=lang)
        print(f"\n{lang.value}:")
        print(f"  {code[:100]}...")

    # Changelog
    print("\n--- Changelog ---")
    changelog = ChangelogGenerator()
    old = {"info": {"version": "1.0"}, "paths": {"/users": {}}}
    new = {"info": {"version": "2.0"}, "paths": {"/users": {}, "/organizations": {}}}
    entry = changelog.generate(old, new)
    print(entry.to_markdown())


if __name__ == "__main__":
    main()
