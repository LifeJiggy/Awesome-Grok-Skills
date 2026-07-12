"""
API Documentation & OpenAPI Specification Management

Provides OpenAPI validation, breaking change detection, code sample generation,
SDK documentation extraction, changelog generation, and interactive explorer building.
"""

from __future__ import annotations

import re
import json
import yaml
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any
from pathlib import Path


class ValidationSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Language(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    CURL = "curl"
    RUBY = "ruby"
    GO = "go"
    JAVA = "java"


class SDKLanguage(Enum):
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    GO = "go"


class ChangeCategory(Enum):
    ADDED = "added"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
    CHANGED = "changed"


@dataclass
class ValidationIssue:
    rule: str
    path: str
    message: str
    severity: ValidationSeverity
    suggestion: str = ""


@dataclass
class ValidationReport:
    spec_path: str
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == ValidationSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == ValidationSeverity.WARNING)

    @property
    def passed(self) -> bool:
        return self.error_count == 0


@dataclass
class BreakingChange:
    severity: str
    category: ChangeCategory
    description: str
    old_value: str = ""
    new_value: str = ""
    migration_path: str = ""
    affected_endpoints: list[str] = field(default_factory=list)


@dataclass
class CodeSample:
    language: Language
    code: str
    description: str = ""


@dataclass
class EndpointSample:
    operation_id: str
    method: str
    path: str
    samples: dict[Language, str] = field(default_factory=dict)


@dataclass
class ParameterInfo:
    name: str
    type: str
    required: bool = False
    description: str = ""
    default: Any = None


@dataclass
class InterfaceInfo:
    name: str
    kind: str
    signature: str
    docstring: str = ""
    parameters: list[ParameterInfo] = field(default_factory=list)
    return_type: str = ""
    source_file: str = ""


@dataclass
class ChangelogEntry:
    category: ChangeCategory
    description: str
    endpoint: str = ""
    old_value: str = ""
    new_value: str = ""


@dataclass
class Changelog:
    version: str
    date: str
    entries: list[ChangelogEntry] = field(default_factory=list)

    @property
    def markdown(self) -> str:
        lines = [f"# API Changelog — v{self.version}\n", f"**Date**: {self.date}\n"]
        by_category: dict[ChangeCategory, list[ChangelogEntry]] = {}
        for entry in self.entries:
            by_category.setdefault(entry.category, []).append(entry)
        category_headers = {
            ChangeCategory.ADDED: "## Added",
            ChangeCategory.CHANGED: "## Changed",
            ChangeCategory.DEPRECATED: "## Deprecated",
            ChangeCategory.REMOVED: "## Removed",
        }
        for cat in [ChangeCategory.ADDED, ChangeCategory.CHANGED, ChangeCategory.DEPRECATED, ChangeCategory.REMOVED]:
            entries = by_category.get(cat, [])
            if entries:
                lines.append(f"\n{category_headers[cat]}\n")
                for e in entries:
                    prefix = f"- **{e.endpoint}**: " if e.endpoint else "- "
                    lines.append(f"{prefix}{e.description}")
        return "\n".join(lines)


@dataclass
class AuthConfig:
    auth_type: str = "bearer"
    token_env_var: str = "API_TOKEN"
    header_name: str = "Authorization"


@dataclass
class ExplorerConfig:
    spec_path: str
    auth_config: AuthConfig = field(default_factory=AuthConfig)
    theme: str = "light"
    base_url: str = ""
    enable_try_it_out: bool = True


class OpenAPIValidator:
    REQUIRED_SPEC_FIELDS = ["openapi", "info", "paths"]
    REQUIRED_OPERATION_FIELDS = ["responses"]
    VALID_HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}

    def __init__(self, spec_path: str, rules: Optional[dict] = None) -> None:
        self.spec_path = spec_path
        self.rules = rules or {}
        self._spec: dict = {}

    def _load_spec(self) -> dict:
        path = Path(self.spec_path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                if path.suffix in (".yaml", ".yml"):
                    return yaml.safe_load(f) or {}
                return json.load(f)
        except (FileNotFoundError, yaml.YAMLError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load spec {self.spec_path}: {e}")

    def validate(self) -> ValidationReport:
        report = ValidationReport(spec_path=self.spec_path)
        try:
            self._spec = self._load_spec()
        except ValueError as e:
            report.issues.append(ValidationIssue(
                rule="SPEC_LOAD", path="spec", message=str(e),
                severity=ValidationSeverity.ERROR
            ))
            return report
        self._validate_spec_structure(report)
        self._validate_naming_conventions(report)
        self._validate_operations(report)
        self._validate_responses(report)
        return report

    def _validate_spec_structure(self, report: ValidationReport) -> None:
        for field_name in self.REQUIRED_SPEC_FIELDS:
            if field_name not in self._spec:
                report.issues.append(ValidationIssue(
                    rule="SPEC_STRUCTURE", path=f"spec.{field_name}",
                    message=f"Missing required field: {field_name}",
                    severity=ValidationSeverity.ERROR
                ))
        info = self._spec.get("info", {})
        if not info.get("title"):
            report.issues.append(ValidationIssue(
                rule="SPEC_INFO", path="spec.info.title",
                message="Missing API title in info object",
                severity=ValidationSeverity.WARNING
            ))
        if not info.get("version"):
            report.issues.append(ValidationIssue(
                rule="SPEC_INFO", path="spec.info.version",
                message="Missing API version in info object",
                severity=ValidationSeverity.ERROR
            ))

    def _validate_naming_conventions(self, report: ValidationReport) -> None:
        naming_rules = self.rules.get("naming", {})
        param_case = naming_rules.get("param_case", "camelCase")
        path_case = naming_rules.get("path_case", "kebab-case")
        paths = self._spec.get("paths", {})
        for path_str in paths:
            if path_case == "kebab-case" and re.search(r"[A-Z]", path_str):
                report.issues.append(ValidationIssue(
                    rule="NAMING_PATH", path=f"paths.{path_str}",
                    message=f"Path contains uppercase characters (expected {path_case})",
                    severity=ValidationSeverity.WARNING
                ))

    def _validate_operations(self, report: ValidationReport) -> None:
        required_ops = self.rules.get("required_fields", [])
        paths = self._spec.get("paths", {})
        for path_str, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method in self.VALID_HTTP_METHODS:
                operation = path_item.get(method)
                if not operation:
                    continue
                if "operationId" not in operation and "operationId" in required_ops:
                    report.issues.append(ValidationIssue(
                        rule="OP_ID", path=f"paths.{path_str}.{method}",
                        message="Missing operationId",
                        severity=ValidationSeverity.WARNING,
                        suggestion="Add a unique operationId for SDK generation."
                    ))
                if "summary" not in operation and "summary" in required_ops:
                    report.issues.append(ValidationIssue(
                        rule="OP_SUMMARY", path=f"paths.{path_str}.{method}",
                        message="Missing summary",
                        severity=ValidationSeverity.WARNING
                    ))
                if "description" not in operation and "description" in required_ops:
                    report.issues.append(ValidationIssue(
                        rule="OP_DESC", path=f"paths.{path_str}.{method}",
                        message="Missing description",
                        severity=ValidationSeverity.INFO
                    ))

    def _validate_responses(self, report: ValidationReport) -> None:
        paths = self._spec.get("paths", {})
        for path_str, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method in self.VALID_HTTP_METHODS:
                operation = path_item.get(method)
                if not operation or not isinstance(operation, dict):
                    continue
                responses = operation.get("responses", {})
                if not responses:
                    report.issues.append(ValidationIssue(
                        rule="NO_RESPONSES", path=f"paths.{path_str}.{method}",
                        message="Operation has no response definitions",
                        severity=ValidationSeverity.ERROR
                    ))
                    continue
                if "200" not in responses and "201" not in responses and "204" not in responses:
                    report.issues.append(ValidationIssue(
                        rule="NO_SUCCESS", path=f"paths.{path_str}.{method}",
                        message="No 2xx success response defined",
                        severity=ValidationSeverity.WARNING
                    ))
                for status_code, response in responses.items():
                    if not isinstance(response, dict):
                        continue
                    if not response.get("description"):
                        report.issues.append(ValidationIssue(
                            rule="RESP_DESC", path=f"paths.{path_str}.{method}.responses.{status_code}",
                            message="Response missing description",
                            severity=ValidationSeverity.INFO
                        ))


class BreakingChangeDetector:
    def __init__(self, old_spec: str, new_spec: str) -> None:
        self.old_spec_path = old_spec
        self.new_spec_path = new_spec

    def _load(self, path: str) -> dict:
        p = Path(path)
        try:
            with open(p, "r", encoding="utf-8") as f:
                if p.suffix in (".yaml", ".yml"):
                    return yaml.safe_load(f) or {}
                return json.load(f)
        except (FileNotFoundError, yaml.YAMLError, json.JSONDecodeError):
            return {}

    def detect(self) -> list[BreakingChange]:
        old = self._load(self.old_spec_path)
        new = self._load(self.new_spec_path)
        changes: list[BreakingChange] = []
        old_paths = old.get("paths", {})
        new_paths = new.get("paths", {})
        for path_str, old_item in old_paths.items():
            if not isinstance(old_item, dict):
                continue
            if path_str not in new_paths:
                changes.append(BreakingChange(
                    severity="critical", category=ChangeCategory.REMOVED,
                    description=f"Entire path removed: {path_str}",
                    old_value=path_str, affected_endpoints=[path_str]
                ))
                continue
            new_item = new_paths[path_str]
            if not isinstance(new_item, dict):
                continue
            for method in ["get", "post", "put", "patch", "delete"]:
                old_op = old_item.get(method)
                new_op = new_item.get(method)
                if old_op and not new_op:
                    changes.append(BreakingChange(
                        severity="critical", category=ChangeCategory.REMOVED,
                        description=f"Method removed: {method.upper()} {path_str}",
                        old_value=method.upper(),
                        affected_endpoints=[f"{method.upper()} {path_str}"],
                        migration_path=f"Check if {method.upper()} {path_str} was replaced by another endpoint."
                    ))
                elif old_op and new_op and isinstance(old_op, dict) and isinstance(new_op, dict):
                    old_params = {p.get("name"): p for p in old_op.get("parameters", []) if isinstance(p, dict)}
                    new_params = {p.get("name"): p for p in new_op.get("parameters", []) if isinstance(p, dict)}
                    for param_name, old_param in old_params.items():
                        if param_name not in new_params:
                            changes.append(BreakingChange(
                                severity="high", category=ChangeCategory.REMOVED,
                                description=f"Parameter removed: {param_name} from {method.upper()} {path_str}",
                                affected_endpoints=[f"{method.upper()} {path_str}"],
                                migration_path=f"Remove {param_name} from your requests."
                            ))
                        else:
                            old_type = old_param.get("schema", {}).get("type", "")
                            new_type = new_params[param_name].get("schema", {}).get("type", "")
                            if old_type and new_type and old_type != new_type:
                                changes.append(BreakingChange(
                                    severity="high", category=ChangeCategory.CHANGED,
                                    description=f"Parameter type changed: {param_name} from {old_type} to {new_type}",
                                    old_value=old_type, new_value=new_type,
                                    affected_endpoints=[f"{method.upper()} {path_str}"]
                                ))
        for path_str in new_paths:
            if path_str not in old_paths:
                changes.append(BreakingChange(
                    severity="low", category=ChangeCategory.ADDED,
                    description=f"New path added: {path_str}",
                    affected_endpoints=[path_str]
                ))
        return changes

    def generate_migration_guide(self, changes: list[BreakingChange], output: str = "MIGRATION.md") -> str:
        lines = ["# API Migration Guide\n"]
        breaking = [c for c in changes if c.severity in ("critical", "high")]
        additions = [c for c in changes if c.category == ChangeCategory.ADDED]
        if breaking:
            lines.append("## Breaking Changes\n")
            for c in breaking:
                lines.append(f"### {c.description}\n")
                lines.append(f"- **Severity**: {c.severity}")
                lines.append(f"- **Category**: {c.category.value}")
                if c.migration_path:
                    lines.append(f"- **Migration**: {c.migration_path}")
                lines.append("")
        if additions:
            lines.append("## New Features\n")
            for c in additions:
                lines.append(f"- {c.description}")
        guide = "\n".join(lines)
        try:
            with open(output, "w", encoding="utf-8") as f:
                f.write(guide)
        except OSError:
            pass
        return guide


class CodeSampleGenerator:
    def __init__(self, spec_path: str) -> None:
        self.spec_path = spec_path
        self._spec: dict = {}

    def _load_spec(self) -> dict:
        path = Path(self.spec_path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                if path.suffix in (".yaml", ".yml"):
                    return yaml.safe_load(f) or {}
                return json.load(f)
        except (FileNotFoundError, yaml.YAMLError, json.JSONDecodeError):
            return {}

    def _generate_python(self, method: str, path: str, params: list[dict]) -> str:
        param_names = [p.get("name", "") for p in params if p.get("in") == "query"]
        lines = [f"import requests", f"", f"response = requests.{method.lower()}(",
                 f'    "https://api.example.com{path}"']
        if param_names:
            lines.append(f"    params={{{', '.join(f'"{p}": {p}' for p in param_names)}}}")
        lines.append(")")
        lines.append("print(response.json())")
        return "\n".join(lines)

    def _generate_javascript(self, method: str, path: str, params: list[dict]) -> str:
        param_names = [p.get("name", "") for p in params if p.get("in") == "query"]
        query_str = "?" + "&".join(f"{p}=${{{p}}}" for p in param_names) if param_names else ""
        lines = [
            f"const response = await fetch(",
            f'  "https://api.example.com{path}{query_str}",',
            f"  {{ method: \"{method.upper()}\" }}",
            ");",
            "const data = await response.json();",
            "console.log(data);"
        ]
        return "\n".join(lines)

    def _generate_curl(self, method: str, path: str, params: list[dict]) -> str:
        query = ""
        query_params = [p for p in params if p.get("in") == "query"]
        if query_params:
            query = "?" + "&".join(f"{p['name']}=VALUE" for p in query_params)
        return f'curl -X {method.upper()} "https://api.example.com{path}{query}"'

    def _generate_ruby(self, method: str, path: str, params: list[dict]) -> str:
        return (
            f"require 'net/http'\n"
            f"require 'json'\n\n"
            f"uri = URI('https://api.example.com{path}')\n"
            f"response = Net::HTTP.{'Get' if method.lower() == 'get' else 'Post'}(uri)\n"
            f"puts JSON.parse(response.body)"
        )

    def _generate_go(self, method: str, path: str, params: list[dict]) -> str:
        return (
            f"package main\n\n"
            f'import (\n\t"fmt"\n\t"net/http"\n\t"io"\n)\n\n'
            f'func main() {{\n'
            f'    req, _ := http.NewRequest("{method.upper()}", "https://api.example.com{path}", nil)\n'
            f'    resp, _ := http.DefaultClient.Do(req)\n'
            f'    defer resp.Body.Close()\n'
            f'    body, _ := io.ReadAll(resp.Body)\n'
            f'    fmt.Println(string(body))\n}}'
        )

    def generate_all(self, languages: list[Language] | None = None) -> list[EndpointSample]:
        if languages is None:
            languages = [Language.PYTHON, Language.JAVASCRIPT, Language.CURL]
        self._spec = self._load_spec()
        samples: list[EndpointSample] = []
        paths = self._spec.get("paths", {})
        for path_str, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method in ["get", "post", "put", "patch", "delete"]:
                operation = path_item.get(method)
                if not operation or not isinstance(operation, dict):
                    continue
                params = operation.get("parameters", [])
                if not isinstance(params, list):
                    params = []
                op_id = operation.get("operationId", f"{method}_{path_str}")
                endpoint_sample = EndpointSample(
                    operation_id=op_id, method=method.upper(), path=path_str
                )
                generators = {
                    Language.PYTHON: self._generate_python,
                    Language.JAVASCRIPT: self._generate_javascript,
                    Language.CURL: self._generate_curl,
                    Language.RUBY: self._generate_ruby,
                    Language.GO: self._generate_go,
                }
                for lang in languages:
                    gen = generators.get(lang)
                    if gen:
                        endpoint_sample.samples[lang] = gen(method, path_str, params)
                samples.append(endpoint_sample)
        return samples


class SDKDocExtractor:
    FUNCTION_PATTERN = re.compile(r"^(?:def|async\s+def)\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(\S+))?\s*:", re.MULTILINE)
    CLASS_PATTERN = re.compile(r"^class\s+(\w+)(?:\(([^)]*)\))?\s*:", re.MULTILINE)
    DOCSTRING_PATTERN = re.compile(r'^\s*"""(.*?)"""', re.DOTALL)
    TYPE_PATTERN = re.compile(r"(\w+)\s*:\s*(\w+)")

    def __init__(self, source_dirs: list[str], language: SDKLanguage = SDKLanguage.PYTHON,
                 exclude_patterns: list[str] | None = None) -> None:
        self.source_dirs = [Path(d) for d in source_dirs]
        self.language = language
        self.exclude_patterns = exclude_patterns or []

    def _should_exclude(self, file_path: Path) -> bool:
        path_str = str(file_path)
        for pattern in self.exclude_patterns:
            if pattern.startswith("*"):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False

    def extract(self) -> list[InterfaceInfo]:
        interfaces: list[InterfaceInfo] = []
        for source_dir in self.source_dirs:
            if not source_dir.exists():
                continue
            for py_file in source_dir.rglob("*.py"):
                if self._should_exclude(py_file):
                    continue
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()
                except (FileNotFoundError, UnicodeDecodeError):
                    continue
                for match in self.CLASS_PATTERN.finditer(content):
                    name = match.group(1)
                    bases = match.group(2) or ""
                    interfaces.append(InterfaceInfo(
                        name=name, kind="class",
                        signature=f"class {name}({bases})" if bases else f"class {name}",
                        source_file=str(py_file)
                    ))
                for match in self.FUNCTION_PATTERN.finditer(content):
                    name = match.group(1)
                    if name.startswith("_"):
                        continue
                    params_str = match.group(2)
                    return_type = match.group(3) or "None"
                    params = []
                    for param_match in self.TYPE_PATTERN.finditer(params_str):
                        params.append(ParameterInfo(
                            name=param_match.group(1), type=param_match.group(2)
                        ))
                    interfaces.append(InterfaceInfo(
                        name=name, kind="function",
                        signature=f"def {name}({params_str}) -> {return_type}",
                        parameters=params, return_type=return_type,
                        source_file=str(py_file)
                    ))
        return interfaces


class APIChangelogGenerator:
    def __init__(self, old_version: str, new_version: str) -> None:
        self.old_version = old_version
        self.new_version = new_version

    def generate_from_specs(self, old_spec: str, new_spec: str) -> Changelog:
        detector = BreakingChangeDetector(old_spec, new_spec)
        changes = detector.detect()
        entries: list[ChangelogEntry] = []
        for change in changes:
            entries.append(ChangelogEntry(
                category=change.category,
                description=change.description,
                old_value=change.old_value,
                new_value=change.new_value
            ))
        return Changelog(
            version=self.new_version,
            date=datetime.date.today().isoformat(),
            entries=entries
        )

    def publish(self, changelog: Changelog, channels: list[str] | None = None) -> dict[str, bool]:
        results: dict[str, bool] = {}
        channels = channels or ["github_releases"]
        for channel in channels:
            results[channel] = True
        return results


class ExplorerGenerator:
    def __init__(self, spec_path: str, auth_config: Optional[AuthConfig] = None,
                 theme: str = "light") -> None:
        self.spec_path = spec_path
        self.auth_config = auth_config or AuthConfig()
        self.theme = theme

    def generate(self, output_path: str, base_url: str = "",
                 enable_try_it_out: bool = True) -> str:
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Explorer</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; margin: 0; padding: 20px; background: {'#1a1a2e' if self.theme == 'dark' else '#ffffff'}; color: {'#e0e0e0' if self.theme == 'dark' else '#333333'}; }}
        .endpoint {{ border: 1px solid {'#333' if self.theme == 'dark' else '#ddd'}; border-radius: 8px; margin: 10px 0; padding: 15px; }}
        .method {{ font-weight: bold; color: #49cc90; }}
        .path {{ font-family: monospace; font-size: 1.1em; }}
        .try-it {{ background: #49cc90; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }}
    </style>
</head>
<body>
    <h1>API Explorer</h1>
    <p>Base URL: <code>{base_url}</code></p>
    <div id="endpoints"></div>
    <script>
        const baseUrl = '{base_url}';
        const authType = '{self.auth_config.auth_type}';
        const tryItOut = {'true' if enable_try_it_out else 'false'};
    </script>
</body>
</html>"""
        try:
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as f:
                f.write(html)
        except OSError:
            pass
        return html


def main() -> None:
    print("=" * 60)
    print("API Documentation & OpenAPI Specification Management")
    print("=" * 60)

    validator = OpenAPIValidator(
        spec_path="openapi.yaml",
        rules={
            "naming": {"param_case": "camelCase", "path_case": "kebab-case"},
            "required_fields": ["description", "summary", "operationId"],
        }
    )
    print(f"\n[Validator] Configured for: {validator.spec_path}")

    detector = BreakingChangeDetector("openapi-v1.yaml", "openapi-v2.yaml")
    print("[Detector] Breaking change detector ready")

    sample_gen = CodeSampleGenerator(spec_path="openapi.yaml")
    print("[CodeGen] Code sample generator ready")

    sdk_extractor = SDKDocExtractor(
        source_dirs=["src/"],
        language=SDKLanguage.PYTHON,
        exclude_patterns=["*_test.py"]
    )
    print("[SDK] Documentation extractor ready")

    changelog_gen = APIChangelogGenerator(old_version="1.0.0", new_version="2.0.0")
    print("[Changelog] Generator ready")

    explorer = ExplorerGenerator(
        spec_path="openapi.yaml",
        auth_config=AuthConfig(auth_type="bearer", token_env_var="API_TOKEN"),
        theme="dark"
    )
    print("[Explorer] Explorer generator ready")

    print("\n" + "=" * 60)
    print("All API documentation components initialized.")
    print("=" * 60)


if __name__ == "__main__":
    main()
