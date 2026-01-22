class Redis:
    def __init__(self):
        self.cluster = None
        self.databases = {}

    def create_cluster(self, name, cluster_mode="sentinel", redis_version="7.2"):
        self.cluster = {
            "name": name,
            "mode": cluster_mode,  # standalone, sentinel, cluster
            "version": redis_version,
            "port": 6379,
            "bind": "0.0.0.0"
        }
        return self

    def configure_sentinel(self, master_name, quorum=2, down_after_milliseconds=30000):
        if "sentinel" not in self.cluster:
            self.cluster["sentinel"] = {}
        self.cluster["sentinel"] = {
            "monitor": master_name,
            "quorum": quorum,
            "down_after_milliseconds": down_after_milliseconds,
            "parallel_syncs": 1,
            "notification_script": None,
            "client_reconfig_script": None
        }
        return self

    def add_sentinel_monitor(self, master_name, host, port, quorum):
        if "monitors" not in self.cluster.get("sentinel", {}):
            self.cluster["sentinel"]["monitors"] = []
        self.cluster["sentinel"]["monitors"].append({
            "name": master_name,
            "host": host,
            "port": port,
            "quorum": quorum
        })
        return self

    def configure_cluster_mode(self, enable=True, resharding=True):
        self.cluster["cluster"] = {
            "enabled": enable,
            "node_timeout": 15000,
            "resharding": {
                "enabled": resharding,
                "migrate_slots_too": True
            },
            "read_replica": True
        }
        return self

    def create_replication(self, master_host, replica_of=None):
        return {
            "master_host": master_host,
            "replicaof": replica_of,
            "slave_read_only": True,
            "slave_priority": 100,
            "min_slaves_to_write": 0,
            "min_slaves_max_lag": 10
        }

    def create_data_structure(self, key, data_type, value, ttl=None):
        return {
            "key": key,
            "type": data_type,  # string, list, set, sorted_set, hash, stream
            "value": value,
            "ttl_seconds": ttl,
            "nx": False,
            "xx": False
        }

    def create_stream(self, stream_name, max_length=None, approximate=True):
        return {
            "stream_name": stream_name,
            "max_length": max_length,
            "approximate_trimming": approximate,
            "consumer_groups": []
        }

    def create_consumer_group(self, stream_name, group_name, consumer_name):
        return {
            "stream": stream_name,
            "group_name": group_name,
            "consumer_name": consumer_name,
            "start_id": "0",
            "pending_entries_limit": 1000
        }

    def create_sorted_set(self, key, members_scores):
        return {
            "key": key,
            "type": "sorted_set",
            "members": members_scores,  # [(member, score)]
            "options": {"nx": False, "xx": False, "ch": False}
        }

    def create_hash(self, key, fields_values):
        return {
            "key": key,
            "type": "hash",
            "fields": fields_values,  # {field: value}
            "options": {"nx": False, "xx": False}
        }

    def configure_persistence(self, rdb_enabled=True, aof_enabled=True):
        return {
            "rdb": {
                "enabled": rdb_enabled,
                "save": "900 1 300 100 60 10000",
                "compression": True,
                "checksum": True
            },
            "aof": {
                "enabled": aof_enabled,
                "rewrite_aof_pct": 100,
                "rewrite_aof_min_size": "64mb",
                "fsync": "everysec"
            }
        }

    def configure_security(self, requirepass=None, acl_enabled=False):
        return {
            "requirepass": requirepass,
            "acl": {
                "enabled": acl_enabled,
                "default_user": {"enabled": True, "rules": ["~* +@all"]}
            },
            "rename_commands": {}
        }

    def configure_performance(self, maxclients=10000, timeout=0):
        return {
            "maxclients": maxclients,
            "timeout": timeout,
            "tcp_keepalive": 300,
            "tcp_backlog": 511,
            "maxmemory": None,
            "maxmemory_policy": "noeviction"
        }

    def configure_slow_log(self, slowlog_log_slower_than=10000, slowlog_max_len=128):
        return {
            "slowlog_log_slower_than": slowlog_log_slower_than,
            "slowlog_max_len": slowlog_max_len,
            "log_level": "notice"
        }

    def create_lua_script(self, script_name, script_body):
        return {
            "name": script_name,
            "body": script_body,
            "sha1": None,
            "evalsha_enabled": True
        }

    def configure_pubsub(self, channels=None, patterns=None):
        return {
            "channels": channels or [],
            "patterns": patterns or [],
            "sharded_pubsub": True
        }

    def create_geospatial_index(self, key, members_locations):
        return {
            "key": key,
            "type": "geospatial",
            "members": members_locations,  # [(member, longitude, latitude)]
            "options": {"stored_mode": "GEOHASH", "distance_unit": "m"}
        }

    def configure_module(self, module_name, module_args=None):
        return {
            "module": module_name,
            "args": module_args or [],
            "config_settings": {}
        }

    def create_bloom_filter(self, key, error_rate=0.01, initial_capacity=100):
        return {
            "key": key,
            "error_rate": error_rate,
            "initial_capacity": initial_capacity,
            "module": "redisbloom"
        }

    def configure_rate_limiting(self, key, max_requests, window_seconds):
        return {
            "key": key,
            "max_requests": max_requests,
            "window_seconds": window_seconds,
            "strategy": "sliding_window"
        }

    def create_circuit_breaker(self, key, failure_threshold, reset_timeout):
        return {
            "key": key,
            "failure_threshold": failure_threshold,
            "reset_timeout": reset_timeout,
            "half_open_requests": 3
        }

    def configure_memory_optimization(self):
        return {
            "activedefrag": True,
            "activedefrag_threshold_lower": 10,
            "activedefrag_threshold_upper": 20,
            "activedefrag_ignore_bytes": "100mb",
            "maxmemory_fragmentation_ratio": 1.0
        }

    def create_search_index(self, index_name, prefix, schema):
        return {
            "index_name": index_name,
            "prefix": prefix,
            "schema": schema,  # [{"field": "name", "type": "text"}]
            "options": {"on": "hash", "score": None}
        }
