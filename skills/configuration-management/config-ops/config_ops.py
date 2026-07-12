"""
Configuration Operations Module
Config management, templates, drift detection, validation, and diffing.
"""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ConfigFormat(Enum):
    YAML = "yaml"
    JSON = "json"
    TOML = "toml"
    INI = "ini"
    ENV = "env"


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ConfigDiffResult:
    """Configuration diff result."""
    has_drift: bool = False
    additions: int = 0
    deletions: int = 0
    modifications: int = 0
    differences: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ValidationResult:
    """Schema validation result."""
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DriftResult:
    """Configuration drift result."""
    has_drift: bool = False
    expected_hash: str = ""
    actual_hash: str = ""
    differences: List[Dict[str, Any]] = field(default_factory=list)
    severity: Severity = Severity.LOW


@dataclass
class TemplateVariable:
    """Template variable."""
    name: str
    value: Any
    required: bool = True
    default: Any = None
    description: str = ""


@dataclass
class ConfigVersion:
    """Configuration version tracking."""
    version: str
    hash: str
    author: str = ""
    message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    parent: str = ""


@dataclass
class EnvironmentConfig:
    """Environment-specific configuration."""
    environment: str
    base_config: Dict[str, Any]
    overrides: Dict[str, Any] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)

    @property
    def merged(self) -> Dict[str, Any]:
        result = copy.deepcopy(self.base_config)
        self._deep_merge(result, self.overrides)
        return result

    def _deep_merge(self, base: dict, overlay: dict) -> None:
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value


# ---------------------------------------------------------------------------
# Config Manager
# ---------------------------------------------------------------------------

class ConfigManager:
    """Manage configuration files and environments."""

    def __init__(self):
        self._configs: Dict[str, Dict[str, Any]] = {}
        self._versions: List[ConfigVersion] = []

    def load(self, path: str) -> Dict[str, Any]:
        """Load configuration from file (demo returns sample)."""
        config = {
            "server": {"host": "0.0.0.0", "port": 8080, "workers": 4},
            "database": {"host": "localhost", "port": 5432, "name": "app"},
            "logging": {"level": "INFO", "format": "json"},
        }
        self._configs[path] = config
        return config

    def save(self, path: str, config: Dict[str, Any]) -> None:
        self._configs[path] = config
        content = json.dumps(config, indent=2)
        version_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        self._versions.append(ConfigVersion(
            version=f"v{len(self._versions) + 1}",
            hash=version_hash,
        ))

    def merge(
        self,
        base: str,
        overlay: str,
    ) -> Dict[str, Any]:
        base_config = self._configs.get(base, {})
        overlay_config = self._configs.get(overlay, {})
        result = copy.deepcopy(base_config)
        self._deep_merge(result, overlay_config)
        return result

    def get_versions(self) -> List[ConfigVersion]:
        return self._versions

    def _deep_merge(self, base: dict, overlay: dict) -> None:
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value


# ---------------------------------------------------------------------------
# Template Engine
# ---------------------------------------------------------------------------

class TemplateEngine:
    """Render configuration templates."""

    def __init__(self):
        self._variables: Dict[str, Any] = {}

    def render(self, template_path: str, variables: Optional[Dict[str, Any]] = None) -> str:
        variables = variables or {}
        template = (
            "apiVersion: apps/v1\n"
            "kind: Deployment\n"
            "metadata:\n"
            "  name: {{ app_name }}\n"
            "  namespace: {{ environment }}\n"
            "spec:\n"
            "  replicas: {{ replicas }}\n"
            "  template:\n"
            "    spec:\n"
            "      containers:\n"
            "      - name: {{ app_name }}\n"
            "        image: {{ image }}\n"
            "        ports:\n"
            "        - containerPort: {{ port }}\n"
        )
        result = template
        for key, value in variables.items():
            result = result.replace("{{ " + key + " }}", str(value))
        result = re.sub(r'\{\{[^}]+\}\}', '""', result)
        return result

    def set_variable(self, name: str, value: Any) -> None:
        self._variables[name] = value

    def validate_template(self, template: str) -> ValidationResult:
        errors: List[str] = []
        variables = re.findall(r'\{\{\s*(\w+)\s*\}\}', template)
        for var in variables:
            if var not in self._variables:
                errors.append(f"Undefined variable: {var}")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)


# ---------------------------------------------------------------------------
# Drift Detector
# ---------------------------------------------------------------------------

class DriftDetector:
    """Detect configuration drift."""

    def __init__(self):
        self._baseline: Dict[str, Any] = {}

    def set_baseline(self, config: Dict[str, Any]) -> None:
        self._baseline = copy.deepcopy(config)

    def compare(
        self,
        expected: str = "",
        actual: str = "",
        expected_config: Optional[Dict[str, Any]] = None,
        actual_config: Optional[Dict[str, Any]] = None,
    ) -> DriftResult:
        exp = expected_config or {}
        act = actual_config or {}
        exp_hash = hashlib.sha256(json.dumps(exp, sort_keys=True).encode()).hexdigest()[:16]
        act_hash = hashlib.sha256(json.dumps(act, sort_keys=True).encode()).hexdigest()[:16]
        diffs = self._find_differences(exp, act)
        return DriftResult(
            has_drift=len(diffs) > 0,
            expected_hash=exp_hash,
            actual_hash=act_hash,
            differences=diffs,
            severity=Severity.HIGH if len(diffs) > 5 else Severity.LOW,
        )

    def _find_differences(
        self, expected: Dict[str, Any], actual: Dict[str, Any], prefix: str = ""
    ) -> List[Dict[str, Any]]:
        diffs: List[Dict[str, Any]] = []
        all_keys = set(list(expected.keys()) + list(actual.keys()))
        for key in all_keys:
            path = f"{prefix}.{key}" if prefix else key
            if key not in expected:
                diffs.append({"path": path, "type": "addition", "value": actual[key]})
            elif key not in actual:
                diffs.append({"path": path, "type": "deletion", "value": expected[key]})
            elif isinstance(expected[key], dict) and isinstance(actual[key], dict):
                diffs.extend(self._find_differences(expected[key], actual[key], path))
            elif expected[key] != actual[key]:
                diffs.append({
                    "path": path,
                    "type": "modification",
                    "expected": expected[key],
                    "actual": actual[key],
                })
        return diffs


# ---------------------------------------------------------------------------
# Schema Validator
# ---------------------------------------------------------------------------

class SchemaValidator:
    """Validate configuration against schemas."""

    def validate(
        self,
        data: Dict[str, Any],
        schema: str = "",
        required_fields: Optional[List[str]] = None,
    ) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []
        required = required_fields or ["host", "port"]
        for field_name in required:
            if field_name not in data:
                errors.append(f"Missing required field: {field_name}")
        for key, value in data.items():
            if key == "port" and not isinstance(value, int):
                errors.append(f"Field 'port' must be integer, got {type(value).__name__}")
            if key == "port" and isinstance(value, int) and (value < 1 or value > 65535):
                errors.append(f"Field 'port' must be between 1 and 65535, got {value}")
            if key == "host" and not isinstance(value, str):
                errors.append(f"Field 'host' must be string")
        return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


# ---------------------------------------------------------------------------
# Config Diff
# ---------------------------------------------------------------------------

class ConfigDiff:
    """Diff configuration files."""

    def diff(
        self,
        config_a: str = "",
        config_b: str = "",
        data_a: Optional[Dict[str, Any]] = None,
        data_b: Optional[Dict[str, Any]] = None,
    ) -> ConfigDiffResult:
        a = data_a or {}
        b = data_b or {}
        detector = DriftDetector()
        result = detector.compare(expected_config=a, actual_config=b)
        return ConfigDiffResult(
            has_drift=result.has_drift,
            additions=sum(1 for d in result.differences if d["type"] == "addition"),
            deletions=sum(1 for d in result.differences if d["type"] == "deletion"),
            modifications=sum(1 for d in result.differences if d["type"] == "modification"),
            differences=result.differences,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Configuration Operations Demo")
    print("=" * 60)

    print("\n[1] Config Management")
    manager = ConfigManager()
    config = manager.load("app_config.yaml")
    print(f"  Keys: {list(config.keys())}")
    manager.save("app_config.yaml", config)
    print(f"  Versions: {len(manager.get_versions())}")

    print("\n[2] Template Rendering")
    engine = TemplateEngine()
    rendered = engine.render("deploy.yaml.j2", {
        "app_name": "myapp", "environment": "prod", "replicas": 3,
        "image": "myapp:v1.0", "port": 8080,
    })
    print(f"  Rendered:\n{rendered[:200]}...")

    print("\n[3] Drift Detection")
    detector = DriftDetector()
    drift = detector.compare(
        expected_config={"host": "prod.db.com", "port": 5432},
        actual_config={"host": "prod.db.com", "port": 5433, "extra": True},
    )
    print(f"  Drift: {drift.has_drift}")
    print(f"  Differences: {len(drift.differences)}")

    print("\n[4] Schema Validation")
    validator = SchemaValidator()
    result = validator.validate({"host": "example.com", "port": 8080})
    print(f"  Valid: {result.is_valid}")
    result2 = validator.validate({"host": "example.com"})
    print(f"  Missing port: {result2.is_valid}, errors: {result2.errors}")

    print("\n[5] Config Diff")
    differ = ConfigDiff()
    diff = differ.diff(
        data_a={"a": 1, "b": 2},
        data_b={"a": 1, "b": 3, "c": 4},
    )
    print(f"  Additions: {diff.additions}, Modifications: {diff.modifications}")

    print("\n" + "=" * 60)
    print("  Config ops demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
