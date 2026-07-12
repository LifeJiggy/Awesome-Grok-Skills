"""
Environment Configuration Module
Environment variables, profiles, promotion, parity, and templates.
"""

from __future__ import annotations

import copy
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


class ParityStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class EnvProfile:
    """Environment profile."""
    name: str
    environment: str
    settings: Dict[str, Any] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)
    description: str = ""

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@dataclass
class ConfigDiff:
    """Configuration diff between environments."""
    source_env: str
    target_env: str
    additions: int = 0
    deletions: int = 0
    modifications: int = 0
    differences: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ParityCheck:
    """Environment parity check result."""
    environments: List[str]
    is_consistent: bool = True
    status: ParityStatus = ParityStatus.PASS
    issues: List[str] = field(default_factory=list)
    checked_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PromotionResult:
    """Config promotion result."""
    source: str
    target: str
    dry_run: bool = True
    changes_applied: int = 0
    approved_by: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class EnvVarDefinition:
    """Environment variable definition."""
    name: str
    required: bool = True
    default: Any = None
    var_type: str = "string"
    description: str = ""
    sensitive: bool = False


# ---------------------------------------------------------------------------
# Environment Manager
# ---------------------------------------------------------------------------

class EnvManager:
    """Manage environment variables."""

    def __init__(self, prefix: str = ""):
        self._prefix = prefix
        self._cache: Dict[str, Any] = {}
        self._definitions: Dict[str, EnvVarDefinition] = {}

    def get(self, name: str, default: Any = None) -> Optional[str]:
        key = f"{self._prefix}{name}" if self._prefix else name
        if key in self._cache:
            return str(self._cache[key])
        return os.environ.get(key, str(default) if default is not None else None)

    def get_int(self, name: str, default: int = 0) -> int:
        val = self.get(name, str(default))
        try:
            return int(val) if val else default
        except (ValueError, TypeError):
            return default

    def get_bool(self, name: str, default: bool = False) -> bool:
        val = self.get(name, str(default))
        if val is None:
            return default
        return val.lower() in ("true", "1", "yes", "on")

    def get_float(self, name: str, default: float = 0.0) -> float:
        val = self.get(name, str(default))
        try:
            return float(val) if val else default
        except (ValueError, TypeError):
            return default

    def get_list(self, name: str, separator: str = ",", default: Optional[List[str]] = None) -> List[str]:
        val = self.get(name)
        if val:
            return [v.strip() for v in val.split(separator)]
        return default or []

    def set(self, name: str, value: Any) -> None:
        self._cache[name] = value

    def define(self, definition: EnvVarDefinition) -> None:
        self._definitions[definition.name] = definition

    def validate_all(self) -> List[str]:
        errors: List[str] = []
        for name, defn in self._definitions.items():
            if defn.required and self.get(name) is None and defn.default is None:
                errors.append(f"Missing required env var: {name}")
        return errors


# ---------------------------------------------------------------------------
# Profile Manager
# ---------------------------------------------------------------------------

class ProfileManager:
    """Manage environment profiles."""

    DEFAULT_PROFILES = {
        "development": EnvProfile(
            name="development",
            environment="development",
            settings={
                "debug": True, "log_level": "DEBUG", "db_host": "localhost",
                "db_port": 5432, "cache_ttl": 60, "replicas": 1,
            },
        ),
        "staging": EnvProfile(
            name="staging",
            environment="staging",
            settings={
                "debug": False, "log_level": "INFO", "db_host": "staging-db.internal",
                "db_port": 5432, "cache_ttl": 300, "replicas": 2,
            },
        ),
        "production": EnvProfile(
            name="production",
            environment="production",
            settings={
                "debug": False, "log_level": "WARNING", "db_host": "prod-db.internal",
                "db_port": 5432, "cache_ttl": 3600, "replicas": 3,
            },
        ),
    }

    def __init__(self):
        self._profiles = dict(self.DEFAULT_PROFILES)
        self._active: Optional[str] = None

    def load_profile(self, name: str) -> Optional[EnvProfile]:
        self._active = name
        return self._profiles.get(name)

    def get_active(self) -> EnvProfile:
        if self._active and self._active in self._profiles:
            return self._profiles[self._active]
        return self._profiles.get("development", EnvProfile(name="default", environment="development"))

    def get_setting(self, key: str, default: Any = None) -> Any:
        profile = self.get_active()
        return profile.settings.get(key, default)

    def list_profiles(self) -> List[str]:
        return list(self._profiles.keys())


# ---------------------------------------------------------------------------
# Config Promoter
# ---------------------------------------------------------------------------

class ConfigPromoter:
    """Promote configuration between environments."""

    def diff_environments(self, source: str, target: str) -> ConfigDiff:
        source_config = {"db_host": "staging-db", "replicas": 2, "debug": False}
        target_config = {"db_host": "prod-db", "replicas": 3, "debug": False}
        diffs: List[Dict[str, Any]] = []
        all_keys = set(list(source_config.keys()) + list(target_config.keys()))
        for key in all_keys:
            if key in source_config and key not in target_config:
                diffs.append({"key": key, "type": "addition"})
            elif key not in source_config and key in target_config:
                diffs.append({"key": key, "type": "deletion"})
            elif source_config.get(key) != target_config.get(key):
                diffs.append({"key": key, "type": "modification", "from": source_config.get(key), "to": target_config.get(key)})
        additions = sum(1 for d in diffs if d["type"] == "addition")
        deletions = sum(1 for d in diffs if d["type"] == "deletion")
        mods = sum(1 for d in diffs if d["type"] == "modification")
        return ConfigDiff(source_env=source, target_env=target, additions=additions, deletions=deletions, modifications=mods, differences=diffs)

    def promote(
        self, source: str, target: str, dry_run: bool = True
    ) -> PromotionResult:
        diff = self.diff_environments(source, target)
        return PromotionResult(
            source=source, target=target, dry_run=dry_run,
            changes_applied=0 if dry_run else diff.additions + diff.modifications,
        )


# ---------------------------------------------------------------------------
# Parity Validator
# ---------------------------------------------------------------------------

class ParityValidator:
    """Validate configuration parity across environments."""

    def check_parity(self, environments: List[str]) -> ParityCheck:
        issues: List[str] = []
        env_configs = {
            "development": {"debug": True, "replicas": 1},
            "staging": {"debug": False, "replicas": 2},
            "production": {"debug": False, "replicas": 3},
        }
        for env in environments:
            config = env_configs.get(env, {})
            if env != "development" and config.get("debug"):
                issues.append(f"{env}: debug should be False in non-dev environments")
        is_consistent = len(issues) == 0
        return ParityCheck(
            environments=environments,
            is_consistent=is_consistent,
            status=ParityStatus.PASS if is_consistent else ParityStatus.FAIL,
            issues=issues,
        )


# ---------------------------------------------------------------------------
# Config Template
# ---------------------------------------------------------------------------

class ConfigTemplate:
    """Generate environment-specific configs from templates."""

    def generate(
        self,
        template_path: str = "",
        environment: str = "development",
        variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        defaults = {
            "development": {"debug": True, "log_level": "DEBUG"},
            "staging": {"debug": False, "log_level": "INFO"},
            "production": {"debug": False, "log_level": "WARNING"},
        }
        config = dict(defaults.get(environment, defaults["development"]))
        if variables:
            config.update(variables)
        return config


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Environment Configuration Demo")
    print("=" * 60)

    print("\n[1] Environment Variables")
    env = EnvManager()
    env.set("DATABASE_URL", "postgresql://localhost:5432/app")
    env.set("PORT", "8080")
    env.set("DEBUG", "true")
    print(f"  DB: {env.get('DATABASE_URL')[:30]}...")
    print(f"  Port: {env.get_int('PORT')}")
    print(f"  Debug: {env.get_bool('DEBUG')}")

    print("\n[2] Profile Management")
    profiles = ProfileManager()
    profiles.load_profile("production")
    active = profiles.get_active()
    print(f"  Active: {active.name}")
    print(f"  DB host: {active.settings.get('db_host')}")

    print("\n[3] Config Promotion")
    promoter = ConfigPromoter()
    diff = promoter.diff_environments("staging", "production")
    print(f"  Diff: +{diff.additions} -{diff.deletions} ~{diff.modifications}")
    result = promoter.promote("staging", "production", dry_run=True)
    print(f"  Dry run: {result.dry_run}")

    print("\n[4] Parity Validation")
    validator = ParityValidator()
    parity = validator.check_parity(["development", "staging", "production"])
    print(f"  Consistent: {parity.is_consistent}")
    print(f"  Issues: {parity.issues}")

    print("\n[5] Config Templates")
    template = ConfigTemplate()
    config = template.generate(environment="production", variables={"db_host": "prod-db"})
    print(f"  Config: {config}")

    print("\n" + "=" * 60)
    print("  Environment config demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
