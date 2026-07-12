"""
Dynamic Configuration Module
Config watching, distribution, caching, versioning, and rollback.
"""

from __future__ import annotations

import copy
import hashlib
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ConfigChangeType(Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"


class UpdateStrategy(Enum):
    IMMEDIATE = "immediate"
    DEBOUNCED = "debounced"
    SCHEDULED = "scheduled"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ConfigChange:
    """Configuration change event."""
    key: str
    change_type: ConfigChangeType
    old_value: Any = None
    new_value: Any = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ConfigVersion:
    """Configuration version."""
    version: int
    hash: str
    config: Dict[str, Any]
    message: str = ""
    author: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CacheEntry:
    """Cache entry with TTL."""
    key: str
    value: Any
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = 300

    @property
    def is_expired(self) -> bool:
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() > self.ttl_seconds


@dataclass
class Subscriber:
    """Config update subscriber."""
    subscriber_id: str
    channel: str
    callback: Optional[Callable] = None
    last_notified: Optional[datetime] = None


@dataclass
class DistributionEvent:
    """Config distribution event."""
    channel: str
    config: Dict[str, Any]
    version: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------------------------------------------------------------------------
# Config Watcher
# ---------------------------------------------------------------------------

class ConfigWatcher:
    """Watch configuration files for changes."""

    def __init__(self, path: str = "", poll_interval_seconds: int = 5):
        self.path = path
        self.poll_interval = poll_interval_seconds
        self._last_hash: str = ""
        self._config: Dict[str, Any] = {}

    def check_for_changes(self) -> Optional[ConfigChange]:
        current_hash = hashlib.sha256(
            str(sorted(self._config.items())).encode()
        ).hexdigest()
        if current_hash != self._last_hash and self._last_hash:
            self._last_hash = current_hash
            return ConfigChange(
                key=self.path,
                change_type=ConfigChangeType.MODIFIED,
            )
        self._last_hash = current_hash
        return None

    def update_config(self, new_config: Dict[str, Any]) -> List[ConfigChange]:
        changes: List[ConfigChange] = []
        all_keys = set(list(self._config.keys()) + list(new_config.keys()))
        for key in all_keys:
            if key not in self._config:
                changes.append(ConfigChange(key=key, change_type=ConfigChangeType.ADDED, new_value=new_config[key]))
            elif key not in new_config:
                changes.append(ConfigChange(key=key, change_type=ConfigChangeType.DELETED, old_value=self._config[key]))
            elif self._config[key] != new_config[key]:
                changes.append(ConfigChange(
                    key=key, change_type=ConfigChangeType.MODIFIED,
                    old_value=self._config[key], new_value=new_config[key],
                ))
        self._config = copy.deepcopy(new_config)
        return changes


# ---------------------------------------------------------------------------
# Config Distributor
# ---------------------------------------------------------------------------

class ConfigDistributor:
    """Distribute configuration updates via pub/sub."""

    def __init__(self):
        self._subscribers: Dict[str, List[Subscriber]] = defaultdict(list)
        self._channels: Dict[str, Dict[str, Any]] = {}
        self._history: List[DistributionEvent] = []

    def publish(self, channel: str, config: Dict[str, Any]) -> int:
        self._channels[channel] = config
        version = len(self._history) + 1
        event = DistributionEvent(channel=channel, config=config, version=version)
        self._history.append(event)
        notified = 0
        for sub in self._subscribers.get(channel, []):
            if sub.callback:
                sub.callback(config)
            sub.last_notified = datetime.now(timezone.utc)
            notified += 1
        return notified

    def subscribe(self, channel: str, callback: Optional[Callable] = None) -> Subscriber:
        sub = Subscriber(
            subscriber_id=f"sub_{len(self._subscribers[channel])}",
            channel=channel,
            callback=callback,
        )
        self._subscribers[channel].append(sub)
        return sub

    def get_subscribers(self, channel: str) -> List[Subscriber]:
        return self._subscribers.get(channel, [])

    def get_latest(self, channel: str) -> Optional[Dict[str, Any]]:
        return self._channels.get(channel)


# ---------------------------------------------------------------------------
# Config Cache
# ---------------------------------------------------------------------------

class ConfigCache:
    """In-memory configuration cache with TTL."""

    def __init__(self, ttl_seconds: int = 300):
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry and not entry.is_expired:
            return entry.value
        if entry:
            del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._cache[key] = CacheEntry(
            key=key, value=value, ttl_seconds=ttl or self._default_ttl,
        )

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def invalidate_all(self) -> int:
        count = len(self._cache)
        self._cache.clear()
        return count

    def get_many(self, keys: List[str]) -> Dict[str, Any]:
        return {k: self._cache[k].value for k in keys if k in self._cache and not self._cache[k].is_expired}

    def cleanup_expired(self) -> int:
        expired = [k for k, v in self._cache.items() if v.is_expired]
        for k in expired:
            del self._cache[k]
        return len(expired)


# ---------------------------------------------------------------------------
# Config Versioner
# ---------------------------------------------------------------------------

class ConfigVersioner:
    """Version configuration changes."""

    def __init__(self):
        self._versions: List[ConfigVersion] = []
        self._current: Optional[ConfigVersion] = None

    def commit(
        self, config: Dict[str, Any], message: str = "", author: str = ""
    ) -> ConfigVersion:
        version_num = len(self._versions) + 1
        config_hash = hashlib.sha256(
            str(sorted(config.items())).encode()
        ).hexdigest()[:12]
        v = ConfigVersion(
            version=version_num,
            hash=config_hash,
            config=copy.deepcopy(config),
            message=message,
            author=author,
        )
        self._versions.append(v)
        self._current = v
        return v

    def get_version(self, version_num: int) -> Optional[ConfigVersion]:
        for v in self._versions:
            if v.version == version_num:
                return v
        return None

    def get_current(self) -> Optional[ConfigVersion]:
        return self._current

    def list_versions(self) -> List[ConfigVersion]:
        return list(self._versions)

    def diff(self, v1: int, v2: int) -> Dict[str, Any]:
        ver1 = self.get_version(v1)
        ver2 = self.get_version(v2)
        if not ver1 or not ver2:
            return {}
        diffs: Dict[str, Any] = {}
        all_keys = set(list(ver1.config.keys()) + list(ver2.config.keys()))
        for key in all_keys:
            if key not in ver1.config:
                diffs[key] = {"type": "added", "value": ver2.config[key]}
            elif key not in ver2.config:
                diffs[key] = {"type": "deleted", "value": ver1.config[key]}
            elif ver1.config[key] != ver2.config[key]:
                diffs[key] = {"type": "modified", "from": ver1.config[key], "to": ver2.config[key]}
        return diffs


# ---------------------------------------------------------------------------
# Rollback Manager
# ---------------------------------------------------------------------------

class RollbackManager:
    """Manage configuration rollback."""

    def __init__(self, versioner: ConfigVersioner):
        self._versioner = versioner
        self._rollback_history: List[Dict[str, Any]] = []

    def rollback_to(self, version_num: int) -> Optional[ConfigVersion]:
        target = self._versioner.get_version(version_num)
        if target:
            self._rollback_history.append({
                "from": self._versioner.get_current().version if self._versioner.get_current() else 0,
                "to": version_num,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            self._versioner._current = target
        return target

    def get_current(self) -> Optional[ConfigVersion]:
        return self._versioner.get_current()

    def get_rollback_history(self) -> List[Dict[str, Any]]:
        return self._rollback_history


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Dynamic Configuration Demo")
    print("=" * 60)

    print("\n[1] Config Watching")
    watcher = ConfigWatcher("/etc/app/config.yaml")
    watcher.update_config({"host": "db1"})
    changes = watcher.update_config({"host": "db2", "port": 5432})
    print(f"  Changes: {len(changes)}")
    for c in changes:
        print(f"    {c.change_type.value}: {c.key}")

    print("\n[2] Config Distribution")
    distributor = ConfigDistributor()
    distributor.subscribe("app_config", lambda c: print(f"    Notified: {c}"))
    notified = distributor.publish("app_config", {"max_conn": 200})
    print(f"  Subscribers notified: {notified}")

    print("\n[3] Config Caching")
    cache = ConfigCache(ttl_seconds=300)
    cache.set("pool_size", 20)
    cache.set("timeout", 5000)
    print(f"  pool_size: {cache.get('pool_size')}")
    print(f"  Cleanup expired: {cache.cleanup_expired()}")

    print("\n[4] Versioning")
    versioner = ConfigVersioner()
    v1 = versioner.commit({"host": "db1"}, message="Initial")
    v2 = versioner.commit({"host": "db2"}, message="Failover")
    print(f"  v{v1.version} -> v{v2.version}")
    diffs = versioner.diff(1, 2)
    print(f"  Diff: {diffs}")

    print("\n[5] Rollback")
    rollback = RollbackManager(versioner)
    rollback.rollback_to(1)
    current = rollback.get_current()
    print(f"  Rolled back to: v{current.version}")
    print(f"  History: {len(rollback.get_rollback_history())} rollbacks")

    print("\n" + "=" * 60)
    print("  Dynamic config demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
