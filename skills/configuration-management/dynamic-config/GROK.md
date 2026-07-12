---
name: "dynamic-config"
category: "configuration-management"
version: "2.0.0"
tags: ["configuration-management", "dynamic-config", "runtime-config", "config-updates"]
---

# Dynamic Configuration

## Overview

The Dynamic Configuration module provides tools for updating application configuration at runtime without restarts. It covers config watchers, pub/sub config distribution, caching strategies, config versioning, rollback mechanisms, and real-time configuration propagation across distributed systems.

This skill is essential for platform engineers building systems that require hot-reloading configuration, runtime feature control, and zero-downtime configuration updates.

## Core Capabilities

- **Config Watching**: File system watchers, etcd/Consul watchers, and polling-based config change detection
- **Config Distribution**: Pub/sub config propagation, push-based updates, and event-driven config sync
- **Config Caching**: In-memory config cache with TTL, distributed cache coordination, and cache invalidation
- **Versioning**: Config version tracking, diff generation, and audit trail for all changes
- **Rollback**: Automatic rollback on validation failure, manual rollback to previous versions
- **Real-Time Updates**: WebSocket-based config push, Server-Sent Events, and long-polling
- **Config Validation**: Schema validation on update, custom validators, and circuit breaker on invalid config
- **Conflict Resolution**: Multi-writer conflict resolution, CRDT-based config merging

## Usage Examples

```python
from dynamic_config import (
    ConfigWatcher,
    ConfigDistributor,
    ConfigCache,
    ConfigVersioner,
    RollbackManager,
)

# --- Config Watching ---
watcher = ConfigWatcher(path="/etc/app/config.yaml")
changes = watcher.check_for_changes()
if changes:
    print(f"Config changed: {changes.changed_keys}")

# --- Config Distribution ---
distributor = ConfigDistributor()
distributor.publish(
    channel="app_config",
    config={"max_connections": 200, "timeout_ms": 5000},
)
subscribers = distributor.get_subscribers("app_config")
print(f"Subscribers notified: {len(subscribers)}")

# --- Config Caching ---
cache = ConfigCache(ttl_seconds=300)
cache.set("db_pool_size", 20)
value = cache.get("db_pool_size")
print(f"Cached value: {value}")

# --- Versioning ---
versioner = ConfigVersioner()
v1 = versioner.commit({"host": "db1.example.com"}, message="Initial config")
v2 = versioner.commit({"host": "db2.example.com"}, message="Failover to db2")
print(f"Versions: v{v1.version} -> v{v2.version}")

# --- Rollback ---
rollback = RollbackManager(versioner)
rollback.rollback_to(v1.version)
current = rollback.get_current()
print(f"Rolled back to: v{current.version}")
```

## Best Practices

- Use etcd or Consul for distributed config watching in production clusters
- Implement config validation before applying changes — never apply invalid config
- Cache configuration locally with TTL to avoid repeated external lookups
- Log all configuration changes with timestamps and change reasons
- Implement automatic rollback when new config causes health check failures
- Use pub/sub for multi-service config propagation rather than polling
- Version all configuration for audit trails and rollback capability
- Test configuration changes in staging before production deployment
- Use circuit breakers to prevent cascading failures from bad config
- Implement gradual config rollout using percentage-based propagation

## Related Modules

- **config-ops**: Base configuration management operations
- **feature-flags**: Feature-flag driven dynamic configuration
- **secrets-management**: Dynamic secret rotation and injection
- **environment-config**: Environment-specific runtime configuration
