"""
API Versioning Module — Version strategies, compatibility analysis, deprecation workflows,
schema migration, and consumer tracking for API lifecycle management.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class VersionStrategy(Enum):
    URL_PATH = "url_path"
    QUERY_PARAM = "query_param"
    HEADER = "header"
    MEDIA_TYPE = "media_type"


class VersionStatus(Enum):
    CURRENT = "current"
    BETA = "beta"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


class ChangeSeverity(Enum):
    BREAKING = "breaking"
    DEPRECATION = "deprecation"
    ADDITIVE = "additive"
    PATCH = "patch"


class ChangeType(Enum):
    FIELD_REMOVED = "field_removed"
    FIELD_TYPE_CHANGED = "field_type_changed"
    FIELD_ADDED = "field_added"
    ENDPOINT_REMOVED = "endpoint_removed"
    ENDPOINT_ADDED = "endpoint_added"
    STATUS_CODE_CHANGED = "status_code_changed"
    PARAMETER_REMOVED = "parameter_removed"
    PARAMETER_ADDED = "parameter_added"
    AUTH_CHANGED = "auth_changed"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class APIVersion:
    """An API version definition."""
    version: str
    status: VersionStatus
    release_date: str = ""
    sunset_date: Optional[str] = None
    changelog: str = ""
    deprecated_reason: str = ""
    replacement_version: Optional[str] = None

    @property
    def is_sunset(self) -> bool:
        if not self.sunset_date:
            return False
        return datetime.fromisoformat(self.sunset_date) < datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "status": self.status.value,
            "release_date": self.release_date,
            "sunset_date": self.sunset_date,
        }


@dataclass
class APIChange:
    """A detected change between API versions."""
    change_type: ChangeType
    severity: ChangeSeverity
    description: str
    path: str = ""
    old_value: Any = None
    new_value: Any = None
    breaking: bool = False
    migration_guide: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.change_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "breaking": self.breaking,
        }


@dataclass
class CompatibilityResult:
    """Result of a compatibility check between versions."""
    old_version: str
    new_version: str
    compatible: bool
    changes: List[APIChange] = field(default_factory=list)

    @property
    def breaking_changes(self) -> int:
        return sum(1 for c in self.changes if c.breaking)

    @property
    def additive_changes(self) -> int:
        return sum(1 for c in self.changes if c.severity == ChangeSeverity.ADDITIVE)

    @property
    def deprecation_changes(self) -> int:
        return sum(1 for c in self.changes if c.severity == ChangeSeverity.DEPRECATION)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "old_version": self.old_version,
            "new_version": self.new_version,
            "compatible": self.compatible,
            "breaking": self.breaking_changes,
            "additive": self.additive_changes,
        }


@dataclass
class DeprecationRecord:
    """A deprecation notice record."""
    version: str
    sunset_date: str
    replacement: str
    reason: str
    migration_url: str = ""
    notice_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    consumers_notified: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "sunset_date": self.sunset_date,
            "replacement": self.replacement,
            "reason": self.reason,
        }


@dataclass
class ConsumerInfo:
    """Information about an API consumer."""
    consumer_id: str
    name: str
    current_version: str
    contact_email: str = ""
    last_request: str = ""
    migration_deadline: Optional[str] = None
    migration_status: str = "pending"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "consumer_id": self.consumer_id,
            "name": self.name,
            "current_version": self.current_version,
            "migration_status": self.migration_status,
        }


@dataclass
class VersionNegotiation:
    """Result of version negotiation from a request."""
    requested_version: Optional[str]
    resolved_version: str
    strategy_used: VersionStrategy
    fallback: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "requested": self.requested_version,
            "resolved": self.resolved_version,
            "strategy": self.strategy_used.value,
            "fallback": self.fallback,
        }


@dataclass
class DeprecationPolicy:
    """Policy governing API deprecation."""
    notice_period_days: int = 90
    require_sunset_header: bool = True
    notify_consumers: bool = True
    max_supported_versions: int = 3
    allow_rollback_period_days: int = 30

    def create_deprecation(
        self, version: str, replacement: str, reason: str = ""
    ) -> Dict[str, Any]:
        sunset_date = (datetime.now(timezone.utc) + timedelta(days=self.notice_period_days)).isoformat()
        return {
            "version": version,
            "sunset_date": sunset_date,
            "replacement": replacement,
            "reason": reason,
            "migration_url": f"https://docs.example.com/migration/{version}-to-{replacement}",
            "notice_period_days": self.notice_period_days,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class VersionManager:
    """Manage API versions and version-based routing."""

    def __init__(
        self,
        current_version: str = "1.0.0",
        strategy: VersionStrategy = VersionStrategy.URL_PATH,
        base_path: str = "/api",
    ):
        self.current_version = current_version
        self.strategy = strategy
        self.base_path = base_path
        self._versions: Dict[str, APIVersion] = {}
        self._deprecation_records: List[DeprecationRecord] = []
        self._consumers: Dict[str, ConsumerInfo] = {}

    def register_version(
        self, version: str, status: str = "current",
        sunset_date: Optional[str] = None, changelog: str = "",
    ) -> APIVersion:
        api_version = APIVersion(
            version=version,
            status=VersionStatus(status),
            release_date=datetime.now(timezone.utc).isoformat(),
            sunset_date=sunset_date,
            changelog=changelog,
        )
        self._versions[version] = api_version
        return api_version

    def resolve_version(self, request_headers: Dict[str, str],
                       request_path: str = "",
                       query_params: Optional[Dict[str, str]] = None) -> VersionNegotiation:
        """Resolve the API version from a request."""
        requested = None

        if self.strategy == VersionStrategy.URL_PATH:
            match = re.search(r"/v(\d+(?:\.\d+)?)/", request_path)
            requested = match.group(1) if match else None
        elif self.strategy == VersionStrategy.QUERY_PARAM:
            requested = (query_params or {}).get("version")
        elif self.strategy == VersionStrategy.HEADER:
            requested = request_headers.get("X-API-Version")
        elif self.strategy == VersionStrategy.MEDIA_TYPE:
            accept = request_headers.get("Accept", "")
            match = re.search(r"application/vnd\.api\.v(\d+)\+json", accept)
            requested = match.group(1) if match else None

        # Find best matching version
        resolved = self._find_best_version(requested)
        fallback = resolved != requested if requested else False

        return VersionNegotiation(
            requested_version=requested,
            resolved_version=resolved,
            strategy_used=self.strategy,
            fallback=fallback,
        )

    def _find_best_version(self, requested: Optional[str]) -> str:
        if requested and requested in self._versions:
            version = self._versions[requested]
            if version.status != VersionStatus.RETIRED:
                return requested

        # Fallback to current version
        for ver, v in self._versions.items():
            if v.status == VersionStatus.CURRENT:
                return ver
        return self.current_version

    def get_version_path(self, version: str) -> str:
        if self.strategy == VersionStrategy.URL_PATH:
            return f"{self.base_path}/v{version}"
        return self.base_path

    def list_versions(self) -> List[Dict[str, Any]]:
        return [v.to_dict() for v in self._versions.values()]

    def add_consumer(self, consumer: ConsumerInfo) -> None:
        self._consumers[consumer.consumer_id] = consumer

    def get_consumers_on_version(self, version: str) -> List[ConsumerInfo]:
        return [c for c in self._consumers.values() if c.current_version == version]

    def generate_sunset_headers(self, version: str) -> Dict[str, str]:
        headers = {}
        api_version = self._versions.get(version)
        if api_version and api_version.status == VersionStatus.DEPRECATED:
            if api_version.sunset_date:
                headers["Sunset"] = api_version.sunset_date
            headers["Deprecation"] = "true"
            if api_version.replacement_version:
                headers["Link"] = f'</v{api_version.replacement_version}>; rel="successor-version"'
        return headers


class CompatibilityChecker:
    """Check compatibility between API versions."""

    def check(self, old_schema: Dict[str, Any], new_schema: Dict[str, Any]) -> CompatibilityResult:
        """Check compatibility between two API schemas."""
        changes: List[APIChange] = []

        old_paths = old_schema.get("paths", {})
        new_paths = new_schema.get("paths", {})

        # Check for removed endpoints
        for path in old_paths:
            if path not in new_paths:
                changes.append(APIChange(
                    change_type=ChangeType.ENDPOINT_REMOVED,
                    severity=ChangeSeverity.BREAKING,
                    description=f"Endpoint {path} has been removed",
                    path=path,
                    breaking=True,
                    migration_guide=f"Use the replacement endpoint documented in the migration guide",
                ))

        # Check for added endpoints
        for path in new_paths:
            if path not in old_paths:
                changes.append(APIChange(
                    change_type=ChangeType.ENDPOINT_ADDED,
                    severity=ChangeSeverity.ADDITIVE,
                    description=f"New endpoint {path} added",
                    path=path,
                ))

        # Check schema changes
        old_schemas = old_schema.get("components", {}).get("schemas", {})
        new_schemas = new_schema.get("components", {}).get("schemas", {})

        for schema_name in old_schemas:
            if schema_name in new_schemas:
                old_props = old_schemas[schema_name].get("properties", {})
                new_props = new_schemas[schema_name].get("properties", {})

                for prop in old_props:
                    if prop not in new_props:
                        changes.append(APIChange(
                            change_type=ChangeType.FIELD_REMOVED,
                            severity=ChangeSeverity.BREAKING,
                            description=f"Field '{prop}' removed from {schema_name}",
                            breaking=True,
                        ))
                    elif old_props[prop] != new_props[prop]:
                        changes.append(APIChange(
                            change_type=ChangeType.FIELD_TYPE_CHANGED,
                            severity=ChangeSeverity.BREAKING,
                            description=f"Field '{prop}' type changed in {schema_name}",
                            old_value=old_props[prop],
                            new_value=new_props[prop],
                            breaking=True,
                        ))

                for prop in new_props:
                    if prop not in old_props:
                        changes.append(APIChange(
                            change_type=ChangeType.FIELD_ADDED,
                            severity=ChangeSeverity.ADDITIVE,
                            description=f"Field '{prop}' added to {schema_name}",
                        ))

        compatible = all(not c.breaking for c in changes)
        return CompatibilityResult(
            old_version=old_schema.get("info", {}).get("version", "?"),
            new_version=new_schema.get("info", {}).get("version", "?"),
            compatible=compatible,
            changes=changes,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the API versioning toolkit."""
    print("API Versioning Toolkit")
    print("=" * 60)

    vm = VersionManager(current_version="2.0.0", strategy=VersionStrategy.URL_PATH)
    vm.register_version("1.0.0", status="deprecated", sunset_date="2025-06-01")
    vm.register_version("1.1.0", status="deprecated", sunset_date="2025-06-01")
    vm.register_version("2.0.0", status="current")

    print(f"\nVersions: {[v['version'] for v in vm.list_versions()]}")

    # Version resolution
    neg = vm.resolve_version({}, request_path="/v1.1/users")
    print(f"\nNegotiation: {neg.resolved_version} (fallback={neg.fallback})")
    print(f"Sunset headers: {vm.generate_sunset_headers('1.0.0')}")

    # Compatibility check
    print("\n--- Compatibility Check ---")
    checker = CompatibilityChecker()
    old = {"info": {"version": "1.0"}, "paths": {"/users": {}, "/old-endpoint": {}},
           "components": {"schemas": {"User": {"properties": {"name": {"type": "string"}, "email": {"type": "string"}}}}}}
    new = {"info": {"version": "2.0"}, "paths": {"/users": {}, "/new-endpoint": {}},
           "components": {"schemas": {"User": {"properties": {"name": {"type": "string"}}}}}}
    result = checker.check(old, new)
    print(f"Compatible: {result.compatible}")
    print(f"Breaking: {result.breaking_changes}, Additive: {result.additive_changes}")
    for c in result.changes:
        print(f"  [{c.severity.value}] {c.description}")

    # Deprecation
    print("\n--- Deprecation ---")
    policy = DeprecationPolicy(notice_period_days=90)
    dep = policy.create_deprecation("1.0.0", "2.0.0", "Security improvements")
    print(f"Sunset: {dep['sunset_date']}")
    print(f"Migration: {dep['migration_url']}")


if __name__ == "__main__":
    main()
