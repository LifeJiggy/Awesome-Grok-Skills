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

---

## Advanced Configuration

### Config Source Hierarchy

Define multiple config sources with priority-based resolution.

```python
hierarchy = ConfigSourceHierarchy(
    sources=[
        ConfigSource("etcd", endpoint="etcd://cluster:2379", priority=3),
        ConfigSource("consul", endpoint="consul://cluster:8500", priority=2),
        ConfigSource("file", path="/etc/app/config.yaml", priority=1),
        ConfigSource("defaults", data=DEFAULT_CONFIG, priority=0),
    ],
    resolution="highest_priority",
)
```

### Config Transformation Pipeline

Apply transformations to config values before caching.

```python
pipeline = ConfigTransformPipeline([
    TransformDecrypt SecretsTransform(vault_client=vault),
    TransformTypeCoerce(),
    TransformValidation(schema="config_schema.json"),
    TransformLogging(sensitive_keys=["password", "api_key"]),
])
distributor.set_pipeline(pipeline)
```

### Config Subscription Patterns

Subscribe to specific config changes with fine-grained filtering.

```python
subscriber = ConfigSubscriber()
subscriber.subscribe(
    channel="database",
    filter=lambda change: change.key.startswith("pool."),
    callback=lambda change: update_connection_pool(change.new_value),
)
```

### Distributed Config Locking

Use distributed locks to coordinate config updates across instances.

```python
lock = DistributedConfigLock(
    backend="etcd",
    lock_key="config/update/lock",
    ttl_seconds=30,
)
with lock:
    config = get_current_config()
    config["pool_size"] = 50
    apply_config(config)
```

---

## Architecture Patterns

### Event-Sourced Configuration

Track all config changes as an event stream for complete auditability.

```python
event_store = ConfigEventStore(
    backend="kafka",
    topic="config-events",
    retention_days=90,
)

# All config changes become events
event_store.append(ConfigCreated(key="db.pool_size", value=20, user="admin"))
event_store.append(ConfigUpdated(key="db.pool_size", value=30, user="admin", reason="scaling"))
```

### Config as Stream

Treat configuration as a continuous stream of changes.

```python
config_stream = ConfigStream(
    source="etcd",
    key_prefix="/app/config/",
    decode="yaml",
)
async for change in config_stream:
    apply_config_change(change)
```

### Saga Pattern for Config Updates

Coordinate multi-service config updates with compensating actions.

```python
saga = ConfigSaga()
saga.add_step("update_service_a", compensator="rollback_service_a")
saga.add_step("update_service_b", compensator="rollback_service_b")
saga.add_step("update_service_c", compensator="rollback_service_c")
saga.execute({"service_a": new_config_a, "service_b": new_config_b, "service_c": new_config_c})
```

### Blue-Green Config Deployment

Deploy config changes to a subset of instances before full rollout.

```python
blue_green = BlueGreenConfigDeployer(
    service="my-app",
    rollout_percentage=10,
    health_check="/health",
    rollback_on_failure=True,
)
blue_green.deploy(new_config)
```

---

## Integration Guide

### etcd Integration

```python
from etcd3 import Client

etcd_client = Client(host="etcd-cluster", port=2379)
watcher = EtcdConfigWatcher(
    client=etcd_client,
    key_prefix="/app/config/",
    on_change=lambda event: update_config(event),
)
watcher.start()
```

### Consul Integration

```python
import consul

c = consul.Consul(host="consul-cluster", port=8500)
watcher = ConsulConfigWatcher(
    consul_client=c,
    key="app/config",
    on_change=lambda: reload_config(),
)
watcher.start()
```

### Redis Pub/Sub Integration

```python
import redis

r = redis.Redis(host="redis-cluster", port=6379)
pubsub = RedisConfigDistributor(
    redis_client=r,
    channel="config_updates",
)
pubsub.publish({"key": "db.pool_size", "value": 50})
```

### Kubernetes ConfigMap Watcher

```python
from kubernetes import client, watch

k8s_client = client.CoreV1Api()
watcher = K8sConfigMapWatcher(
    api=k8s_client,
    namespace="default",
    configmap_name="app-config",
    on_change=lambda cm: apply_configmap(cm),
)
watcher.start()
```

---

## Performance Optimization

### Config Caching Strategies

```python
# LRU Cache with TTL
cache = LRUCache(
    max_size=1000,
    ttl_seconds=300,
    eviction_policy="lru",
)

# Write-through Cache
cache = WriteThroughCache(
    backend="redis",
    local_cache_size=500,
    sync_interval=10,
)
```

### Config Update Batching

Batch multiple config updates to reduce propagation overhead.

```python
batcher = ConfigUpdateBatcher(
    max_batch_size=10,
    max_wait_ms=100,
    on_batch=lambda updates: apply_updates(updates),
)
batcher.add({"key": "a", "value": 1})
batcher.add({"key": "b", "value": 2})
# Both applied in single batch after 100ms or when batch is full
```

### Lazy Config Evaluation

Compute config values only when accessed.

```python
lazy_config = LazyConfig({
    "db_url": LazyValue(lambda: build_database_url()),
    "cache_ttl": LazyValue(lambda: compute_optimal_ttl()),
})
```

---

## Security Considerations

### Config Encryption at Rest

Encrypt sensitive configuration values in distributed stores.

```python
encryptor = ConfigEncryptor(
    key_provider=AWSKMS(key_id="alias/config-key"),
    algorithm="AES-256-GCM",
    encrypted_prefix="ENC[",
)
encrypted_store = EncryptedConfigStore(
    backend=etcd_client,
    encryptor=encryptor,
)
```

### Config Access Audit

Log all config access for compliance and security.

```python
auditor = ConfigAuditor(
    log_destination="s3://audit-logs/config/",
    retention_days=365,
    capture_fields=["key", "action", "user", "timestamp", "ip_address"],
)
```

### Config Change Approval

Require approval for sensitive config changes.

```python
approval_workflow = ConfigApprovalWorkflow(
    sensitive_patterns=["database.*", "security.*", "payment.*"],
    approvers=["security-team", "platform-team"],
    approval_count=2,
    timeout_hours=24,
)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Config not updating | Watcher disconnected | Check watcher health and reconnect |
| Stale config values | Cache TTL too long | Reduce TTL or invalidate cache |
| Config propagation delay | Network latency | Check network connectivity |
| Config conflict | Concurrent writes | Use distributed locking |
| Config validation fails | Schema mismatch | Update config to match schema |

### Debug Logging

```python
import logging
logging.getLogger("dynamic_config").setLevel(logging.DEBUG)
# Shows config change events, cache hits/misses, propagation status
```

### Config Change Tracking

```python
tracker = ConfigChangeTracker()
history = tracker.get_history(key="db.pool_size", last_hours=24)
for change in history:
    print(f"{change.timestamp}: {change.old_value} -> {change.new_value} by {change.user}")
```

---

## API Reference

### ConfigWatcher

```python
class ConfigWatcher:
    def watch(path: str, callback: Callable) -> WatchHandle
    def unwatch(handle: WatchHandle) -> None
    def list_watches() -> List[WatchHandle]
```

### ConfigDistributor

```python
class ConfigDistributor:
    def publish(channel: str, config: dict) -> None
    def subscribe(channel: str, callback: Callable) -> Subscription
    def unsubscribe(subscription: Subscription) -> None
    def get_subscribers(channel: str) -> List[Subscription]
```

### ConfigCache

```python
class ConfigCache:
    def get(key: str) -> Optional[Any]
    def set(key: str, value: Any, ttl: int = None) -> None
    def invalidate(key: str) -> None
    def clear() -> None
    def stats() -> CacheStats
```

---

## Data Models

### ConfigChange

```python
@dataclass
class ConfigChange:
    key: str
    old_value: Any
    new_value: Any
    timestamp: datetime
    source: str
    version: int
```

### WatchHandle

```python
@dataclass
class WatchHandle:
    watch_id: str
    path: str
    callback: Callable
    created_at: datetime
    status: str  # active, paused, stopped
```

---

## Deployment Guide

### etcd Cluster Setup

```yaml
# docker-compose.yml
services:
  etcd1:
    image: quay.io/coreos/etcd:v3.5.10
    environment:
      ETCD_NAME: etcd1
      ETCD_INITIAL_CLUSTER: etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
    ports:
      - "2379:2379"
      - "2380:2380"
```

### Multi-Datacenter Config Replication

```python
replication = CrossDCConfigReplication(
    primary_dc="us-east-1",
    replica_dcs=["eu-west-1", "ap-southeast-1"],
    replication_mode="async",
    conflict_resolution="timestamp",
)
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `config.change.propagation_time` | Time for change to propagate | > 5s |
| `config.cache.hit_rate` | Cache hit rate | < 0.9 |
| `config.watcher.reconnects` | Watcher reconnection count | > 0 |
| `config.update.failures` | Failed config updates | > 0 |

---

## Testing Strategy

### Config Change Tests

```python
def test_config_propagation():
    distributor = TestConfigDistributor()
    received = []
    distributor.subscribe("test_channel", lambda c: received.append(c))
    distributor.publish("test_channel", {"key": "value"})
    assert len(received) == 1
    assert received[0]["key"] == "value"
```

---

## Versioning & Migration

### Config Version Management

```python
versioner = ConfigVersionManager(
    max_versions=50,
    auto_cleanup=True,
)
versioner.commit("db.pool_size", 50, "Increased pool for scaling")
versioner.rollback("db.pool_size", target_version=3)
```

---

## Advanced Configuration (Extended)

### Config Conflict Resolution

Handle conflicts when multiple writers update configuration simultaneously.

```python
conflict_resolver = ConflictResolver(
    strategies={
        "last_writer_wins": LastWriterWinsStrategy(),
        "merge": DeepMergeStrategy(),
        "custom": CustomResolverStrategy(resolver_func),
    },
    default_strategy="last_writer_wins",
    conflict_detection=True,
    conflict_notification=True,
)
```

### Config Propagation Control

Fine-tune how configuration changes propagate across services.

```python
propagation = PropagationController(
    propagation_modes={
        "instant": {"delay_ms": 0, "retry": False},
        "gradual": {"delay_ms": 1000, "percentage_per_step": 10},
        "scheduled": {"cron": "0 2 * * *", "timezone": "UTC"},
    },
    affected_services=["payments", "auth", "search"],
    health_check_required=True,
)
```

### Config Audit Trail

Maintain detailed audit trail for all configuration changes.

```python
audit_trail = ConfigAuditTrail(
    storage="s3://config-audit-logs/",
    retention_days=365,
    capture_fields=[
        "config_key", "old_value", "new_value",
        "changed_by", "timestamp", "change_reason",
        "approved_by", "deployment_id",
    ],
    compliance_mode="soc2",
)
```

### Config Dependency Graph

Track dependencies between configuration keys.

```python
dependency_graph = ConfigDependencyGraph()
dependency_graph.add_dependency("database.pool_size", "database.url")
dependency_graph.add_dependency("cache.ttl", "database.pool_size")
# If database.url changes, dependent configs are re-validated
```

### Config Migration System

Migrate configuration between versions automatically.

```python
migration_system = ConfigMigrationSystem(
    migrations={
        "1.0->2.0": Migration1to2(),
        "2.0->2.1": Migration2to2_1(),
    },
    auto_migrate=True,
    backup_before_migration=True,
)
```

---

## Architecture Patterns (Extended)

### Event Sourcing Configuration Pattern

Track all configuration changes as immutable events.

```python
class EventSourcedConfig:
    def __init__(self):
        self.event_store = EventStore()
        self.projections = {}

    def apply(self, event):
        self.event_store.append(event)
        self.update_projections(event)

    def get_state(self, key):
        return self.projections.get(key, None)

    def rebuild_projection(self, key):
        events = self.event_store.get_events(key)
        state = None
        for event in events:
            state = self.apply_event(state, event)
        self.projections[key] = state
```

### Configuration Mesh Pattern

Distribute configuration across a mesh of nodes with eventual consistency.

```python
class ConfigMesh:
    def __init__(self):
        self.nodes = []
        self.replication_factor = 3

    def update(self, key, value):
        event = ConfigUpdate(key, value)
        affected_nodes = self.select_nodes(key)
        for node in affected_nodes:
            node.apply(event)
```

### Config-as-Stream Pattern

Treat configuration as a continuous stream of changes.

```python
class ConfigStream:
    def __init__(self, source):
        self.source = source
        self.processors = []

    def pipe(self, processor):
        self.processors.append(processor)
        return self

    def subscribe(self, callback):
        async for event in self.source:
            result = event
            for processor in self.processors:
                result = processor.process(result)
            callback(result)
```

### Configuration Snapshot Pattern

Take periodic snapshots for fast recovery.

```python
class ConfigSnapshot:
    def __init__(self, interval_seconds=300):
        self.interval = interval_seconds
        self.snapshots = []

    def take_snapshot(self, config):
        snapshot = {
            "timestamp": time.time(),
            "config": copy.deepcopy(config),
            "checksum": calculate_checksum(config),
        }
        self.snapshots.append(snapshot)
        return snapshot

    def restore_snapshot(self, snapshot_id):
        snapshot = self.get_snapshot(snapshot_id)
        return copy.deepcopy(snapshot["config"])
```

---

## Integration Guide (Extended)

### Apache Kafka Integration

```python
from kafka import KafkaConsumer, KafkaProducer

# Produce config events
producer = KafkaProducer(bootstrap_servers='kafka:9092')
producer.send('config-updates', key=b'db.pool_size', value=json.dumps({"value": 50}))

# Consume config events
consumer = KafkaConsumer('config-updates', group_id='config-consumers')
for message in consumer:
    config_update = json.loads(message.value)
    apply_config(message.key.decode(), config_update)
```

### etcd v3 Integration

```python
import etcd3

client = etcd3.client(host='etcd', port=2379)

# Watch for changes
events_iterator, cancel = client.watch_prefix('/app/config/')
for event in events_iterator:
    key = event.key.decode()
    value = json.loads(event.value.decode())
    apply_config_change(key, value)
```

### Consul Watch Integration

```python
import consul

c = consul.Consul(host='consul', port=8500)

# Watch key for changes
index = None
while True:
    index, data = c.kv.get('app/config', index=index)
    if data:
        config = json.loads(data['Value'])
        apply_config(config)
```

### Redis Pub/Sub Integration

```python
import redis

r = redis.Redis(host='redis', port=6379)
pubsub = r.pubsub()
pubsub.subscribe('config-updates')

for message in pubsub.listen():
    if message['type'] == 'message':
        update = json.loads(message['data'])
        apply_config(update['key'], update['value'])
```

### Apollo Federation Config

```python
# Dynamic config for GraphQL federation
class FederationConfig:
    def __init__(self):
        self.supergraph_config = {}

    def update_supergraph(self, config):
        self.supergraph_config = config
        # Hot-reload schema
        self.schema_registry.update_schema(config['schema'])
```

### Envoy Proxy Config

```python
# Dynamic Envoy configuration
class EnvoyConfigManager:
    def __init__(self):
        self.xds_server = XDSGrpcServer()

    def update_route(self, route_config):
        self.xds_server.push_route_config(route_config)
        # Envoy hot-reloads without restart
```

---

## Performance Optimization (Extended)

### Config Compression

Compress configuration for network transfer.

```python
class ConfigCompressor:
    def compress(self, config_data):
        return zlib.compress(json.dumps(config_data).encode())

    def decompress(self, compressed_data):
        return json.loads(zlib.decompress(compressed_data))
```

### Config Sharding

Shard configuration across multiple stores for scalability.

```python
class ConfigShardManager:
    def __init__(self, n_shards=16):
        self.shards = [ConfigShard(i) for i in range(n_shards)]

    def get_shard(self, key):
        shard_id = hash(key) % len(self.shards)
        return self.shards[shard_id]

    def update(self, key, value):
        shard = self.get_shard(key)
        shard.update(key, value)
```

### Config Prefetching

Prefetch configuration based on access patterns.

```python
class ConfigPrefetcher:
    def __init__(self):
        self.access_patterns = defaultdict(list)
        self.prefetch_cache = {}

    def record_access(self, key):
        self.access_patterns[key].append(time.time())

    def should_prefetch(self, key):
        accesses = self.access_patterns.get(key, [])
        if len(accesses) > 5:
            return True  # Frequently accessed
        return False

    def prefetch(self, keys):
        for key in keys:
            if self.should_prefetch(key):
                self.prefetch_cache[key] = self.fetch(key)
```

### Config Deduplication

Deduplicate configuration updates to reduce processing overhead.

```python
class ConfigDeduplicator:
    def __init__(self):
        self.seen_updates = {}
        self.dedup_window_seconds = 5

    def is_duplicate(self, key, value, timestamp):
        last_seen = self.seen_updates.get(key)
        if last_seen and (timestamp - last_seen['timestamp']) < self.dedup_window_seconds:
            if last_seen['value'] == value:
                return True
        self.seen_updates[key] = {'value': value, 'timestamp': timestamp}
        return False
```

---

## Security Considerations (Extended)

### Config Tampering Detection

Detect unauthorized configuration changes.

```python
class ConfigTamperDetector:
    def __init__(self):
        self.checksums = {}

    def record_checksum(self, key, value):
        self.checksums[key] = hashlib.sha256(json.dumps(value).encode()).hexdigest()

    def verify_integrity(self, key, value):
        current_hash = hashlib.sha256(json.dumps(value).encode()).hexdigest()
        expected_hash = self.checksums.get(key)
        if current_hash != expected_hash:
            raise ConfigTamperedError(f"Config {key} has been tampered with")
        return True
```

### Config Secret Rotation

Automatically rotate secrets in configuration.

```python
class SecretRotationManager:
    def __init__(self, vault_client):
        self.vault = vault_client

    def rotate_secret(self, secret_path, rotation_policy):
        new_secret = self.vault.generate_secret(rotation_policy)
        self.vault.write_secret(secret_path, new_secret)
        # Notify affected services
        self.notify_services(secret_path, new_secret)
```

### Config Encryption in Transit

Encrypt configuration during propagation.

```python
class TransitEncryption:
    def __init__(self, tls_config):
        self.tls = tls_config

    def encrypt_for_transport(self, config_data):
        return self.tls.encrypt(json.dumps(config_data).encode())

    def decrypt_after_transport(self, encrypted_data):
        return json.loads(self.tls.decrypt(encrypted_data))
```

### Config Access Control

Implement fine-grained access control for configuration.

```python
class ConfigAccessControl:
    def __init__(self):
        self.acl_rules = {}

    def add_rule(self, key_pattern, allowed_roles, actions):
        self.acl_rules[key_pattern] = {
            'roles': allowed_roles,
            'actions': actions,
        }

    def check_access(self, key, user_role, action):
        for pattern, rules in self.acl_rules.items():
            if fnmatch.fnmatch(key, pattern):
                if user_role in rules['roles'] and action in rules['actions']:
                    return True
                return False
        return False  # Default deny
```

---

## Troubleshooting Guide (Extended)

### Debugging Configuration Propagation

```python
class ConfigPropagDebugger:
    def trace_propagation(self, key, start_time):
        """Trace how a config change propagates through the system."""
        events = self.get_events(key, start_time)
        for event in events:
            print(f"{event.timestamp}: {event.service} received {key}={event.value}")
            print(f"  Latency: {event.latency_ms}ms")
```

### Configuration Health Dashboard

```python
class ConfigHealthDashboard:
    def get_status(self):
        return {
            'total_keys': self.count_keys(),
            'active_watchers': self.count_watchers(),
            'cache_hit_rate': self.get_cache_hit_rate(),
            'propagation_latency_ms': self.get_avg_propagation_latency(),
            'recent_changes': self.get_recent_changes(limit=10),
        }
```

### Common Configuration Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Config not propagating | Network partition | Check network connectivity |
| Stale cache | TTL too long | Reduce TTL or invalidate |
| Conflict detected | Concurrent writes | Use distributed locking |
| Propagation delay | High latency | Check service health |
| Memory leak | Cache not evicting | Set max cache size |
| Config corruption | Serialization error | Validate before applying |

### Configuration Debugging Commands

```bash
# Check config watcher status
config-cli watcher status

# View config change history
config-cli history --key db.pool_size --last 10

# Force config refresh
config-cli refresh --key db.pool_size

# Validate config schema
config-cli validate --config /etc/app/config.yaml --schema schema.json

# Test config propagation
config-cli test-propagation --key test.key --value test.value
```

---

## API Reference (Extended)

### ConfigWatcher (Extended)

```python
class ConfigWatcher:
    def watch(path: str, callback: Callable, filters: dict = None) -> WatchHandle
    def unwatch(handle: WatchHandle) -> None
    def list_watches() -> List[WatchHandle]
    def get_watch_status(handle: WatchHandle) -> WatchStatus
    def pause(handle: WatchHandle) -> None
    def resume(handle: WatchHandle) -> None
```

### ConfigDistributor (Extended)

```python
class ConfigDistributor:
    def publish(channel: str, config: dict, priority: int = 0) -> None
    def subscribe(channel: str, callback: Callable, filter_func: Callable = None) -> Subscription
    def unsubscribe(subscription: Subscription) -> None
    def get_subscribers(channel: str) -> List[Subscription]
    def publish_batch(channel: str, configs: List[dict]) -> None
    def get_publish_stats() -> PublishStats
```

### ConfigCache (Extended)

```python
class ConfigCache:
    def get(key: str) -> Optional[Any]
    def set(key: str, value: Any, ttl: int = None, tags: List[str] = None) -> None
    def invalidate(key: str) -> None
    def invalidate_by_tag(tag: str) -> None
    def clear() -> None
    def stats() -> CacheStats
    def warm(keys: List[str]) -> None
    def get_many(keys: List[str]) -> Dict[str, Any]
```

### ConfigVersioner (Extended)

```python
class ConfigVersioner:
    def commit(config: dict, message: str, author: str = None) -> ConfigVersion
    def get_version(version: int) -> ConfigVersion
    def list_versions(key: str = None, limit: int = 50) -> List[ConfigVersion]
    def rollback(version: int) -> ConfigVersion
    def diff(version1: int, version2: int) -> ConfigDiff
    def blame(key: str) -> List[BlameEntry]
```

### RollbackManager (Extended)

```python
class RollbackManager:
    def rollback_to(version: int) -> ConfigVersion
    def rollback_last(n_changes: int = 1) -> ConfigVersion
    def get_current() -> ConfigVersion
    def get_rollback_history() -> List[RollbackEntry]
    def auto_rollback_on_failure(threshold: float = 0.1) -> None
```

---

## Data Models (Extended)

### ConfigEvent

```python
@dataclass
class ConfigEvent:
    event_id: str
    event_type: str  # created, updated, deleted
    key: str
    old_value: Any
    new_value: Any
    timestamp: datetime
    source: str
    actor: str
    metadata: dict
```

### PropagationStatus

```python
@dataclass
class PropagationStatus:
    key: str
    total_services: int
    propagated_to: int
    failed_services: List[str]
    pending_services: List[str]
    started_at: datetime
    completed_at: Optional[datetime]
    status: str  # in_progress, completed, failed
```

### ConfigHealth

```python
@dataclass
class ConfigHealth:
    overall_status: str  # healthy, degraded, unhealthy
    watchers_active: int
    cache_hit_rate: float
    avg_propagation_latency_ms: float
    recent_errors: List[ConfigError]
    last_check: datetime
```

### ConfigSnapshot

```python
@dataclass
class ConfigSnapshot:
    snapshot_id: str
    timestamp: datetime
    config: dict
    checksum: str
    size_bytes: int
    keys_count: int
```

---

## Deployment Guide (Extended)

### Multi-Region Deployment

```python
class MultiRegionConfigDeployer:
    def __init__(self):
        self.regions = ['us-east-1', 'eu-west-1', 'ap-southeast-1']
        self.replication_mode = 'async'

    def deploy(self, config):
        for region in self.regions:
            self.deploy_to_region(region, config)

    def deploy_to_region(self, region, config):
        regional_store = self.get_regional_store(region)
        regional_store.update(config)
```

### Blue-Green Config Deployment

```python
class BlueGreenConfigDeployer:
    def __init__(self):
        self.blue_store = ConfigStore('blue')
        self.green_store = ConfigStore('green')
        self.active = 'blue'

    def deploy(self, config):
        inactive = 'green' if self.active == 'blue' else 'blue'
        self.get_store(inactive).update(config)
        # Validate before switching
        if self.validate(inactive):
            self.switch_active(inactive)

    def rollback(self):
        inactive = 'green' if self.active == 'blue' else 'blue'
        self.switch_active(inactive)
```

### Canary Config Deployment

```python
class CanaryConfigDeployer:
    def __init__(self):
        self.canary_percentage = 5
        self.increase_step = 5

    def deploy(self, config):
        # Start with small percentage
        self.deploy_to_canary(config, percentage=5)
        # Monitor and increase
        while self.canary_percentage < 100:
            if self.metrics_healthy():
                self.increase_canary(self.increase_step)
            else:
                self.rollback_canary()
                break
```

---

## Monitoring & Observability (Extended)

### Advanced Metrics

```python
# Custom metrics for config operations
config_operations_counter = Counter('config_operations_total', 'Total config operations', ['operation', 'status'])
config_propagation_latency = Histogram('config_propagation_latency_seconds', 'Propagation latency')
config_cache_hits = Counter('config_cache_hits_total', 'Cache hits', ['key_pattern'])
config_conflicts = Counter('config_conflicts_total', 'Config conflicts detected')
```

### Distributed Tracing

```python
from opentelemetry import trace

tracer = trace.get_tracer('config-service')

def trace_config_propagation(key, value):
    with tracer.start_as_current_span('config.propagate') as span:
        span.set_attribute('config.key', key)
        span.set_attribute('config.size', len(json.dumps(value)))
        # Propagate config
        propagate(key, value)
        span.add_event('config.propagated')
```

### Alerting Rules

```yaml
groups:
  - name: dynamic-config
    rules:
      - alert: ConfigPropagationSlow
        expr: histogram_quantile(0.99, config_propagation_latency_seconds) > 5
        for: 5m
        labels:
          severity: warning
      - alert: ConfigConflictRateHigh
        expr: rate(config_conflicts_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
```

---

## Testing Strategy (Extended)

### Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.dictionaries(st.text(), st.text()))
def test_config_merge_idempotent(config):
    merger = ConfigMerger()
    result1 = merger.merge(config, {})
    result2 = merger.merge(config, {})
    assert result1 == result2
```

### Chaos Testing

```python
class ConfigChaosTest:
    def test_network_partition(self):
        # Simulate network partition
        with self.partition_services():
            # Config should eventually converge
            self.wait_for_convergence(timeout=30)

    def test_store_failure(self):
        # Simulate store failure
        with self.fail_store():
            # Should fall back to cache
            config = self.get_config('key')
            assert config is not None
```

### Load Testing

```python
class ConfigLoadTest:
    def test_concurrent_updates(self):
        # Test concurrent config updates
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = []
            for i in range(1000):
                futures.append(executor.submit(self.update_config, f'key_{i}', f'value_{i}'))
            results = [f.result() for f in futures]
            assert all(r.success for r in results)
```

---

## Versioning & Migration (Extended)

### Config Schema Evolution

```python
class ConfigSchemaEvolver:
    def __init__(self):
        self.schemas = {
            '1.0': Schema1_0(),
            '2.0': Schema2_0(),
            '2.1': Schema2_1(),
        }
        self.migrations = {
            ('1.0', '2.0'): Migration1to2(),
            ('2.0', '2.1'): Migration2to2_1(),
        }

    def evolve(self, config, target_version):
        current_version = config.get('schema_version', '1.0')
        while current_version != target_version:
            next_version = self.get_next_version(current_version)
            migration = self.migrations[(current_version, next_version)]
            config = migration.migrate(config)
            current_version = next_version
        return config
```

### Backward Compatibility

```python
class BackwardCompatibleConfig:
    def __init__(self):
        self.deprecated_keys = {}
        self.alias_map = {}

    def add_deprecation(self, old_key, new_key, removal_version):
        self.deprecated_keys[old_key] = {
            'new_key': new_key,
            'removal_version': removal_version,
        }

    def get(self, key):
        # Check for alias
        actual_key = self.alias_map.get(key, key)
        # Check for deprecation
        if actual_key in self.deprecated_keys:
            self.warn_deprecated(actual_key)
        return self.config.get(actual_key)
```

---

## Glossary (Extended)

| Term | Definition |
|------|-----------|
| **Config Watcher** | Monitors config stores for changes and triggers callbacks |
| **Config Distribution** | Propagating config changes to multiple services |
| **Config Caching** | Storing config locally to reduce external lookups |
| **Config Versioning** | Tracking config change history for rollback |
| **Hot-Reload** | Applying config changes without restarting services |
| **Config Drift** | Differences between expected and actual config state |
| **Config Lock** | Distributed lock to coordinate concurrent config updates |
| **Event Sourcing** | Storing changes as immutable events |
| **Config Mesh** | Distributed configuration across node mesh |
| **Config Snapshot** | Point-in-time capture of configuration state |
| **Propagation Delay** | Time for config change to reach all services |
| **Config Conflict** | Simultaneous conflicting configuration changes |
| **Config Sharding** | Distributing configuration across multiple stores |
| **Config Prefetch** | Loading config before it's needed based on patterns |
| **Config Deduplication** | Removing redundant configuration updates |

---

## Changelog

### v2.0.0
- Added etcd and Consul watcher support
- Distributed config locking
- Config event sourcing

### v1.5.0
- Config caching with LRU eviction
- WebSocket-based real-time updates
- Config validation on update

### v1.0.0
- Initial release with file-based config watching
- Basic pub/sub config distribution
- In-memory config caching

---

## Contributing Guidelines

### Config Key Naming

- Use dot notation for hierarchical keys: `database.pool.size`
- Use snake_case for all config keys
- Prefix with service name: `payments.database.pool_size`

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
