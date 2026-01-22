class MongoDB:
    def __init__(self):
        self.cluster = None
        self.databases = {}

    def create_cluster(self, name, cluster_type="replica_set", mongo_version="7.0"):
        self.cluster = {
            "name": name,
            "type": cluster_type,  # standalone, replica_set, sharded_cluster
            "version": mongo_version,
            "feature_compatibility_version": mongo_version
        }
        return self

    def add_replica_set_member(self, member_id, host, priority=1, votes=1):
        if "members" not in self.cluster:
            self.cluster["members"] = []
        self.cluster["members"].append({
            "_id": member_id,
            "host": host,
            "priority": priority,
            "votes": votes,
            "arbiter_only": False,
            "hidden": False,
            "slave_delay": {"hours": 0}
        })
        return self

    def add_shard(self, shard_name, replica_set_name):
        if "shards" not in self.cluster:
            self.cluster["shards"] = []
        self.cluster["shards"].append({
            "_id": shard_name,
            "host": f"{replica_set_name}/host1:27017,host2:27017,host3:27017"
        })
        return self

    def configure_config_server(self, replica_set_name):
        self.cluster["config_server"] = {
            "replica_set": replica_set_name,
            "members": []
        }
        return self

    def configure_mongos(self):
        self.cluster["mongos"] = {
            "instances": [],
            "config_db": self.cluster.get("config_server", {}).get("replica_set")
        }
        return self

    def create_database(self, database_name):
        self.databases[database_name] = {
            "name": database_name,
            "collections": {},
            "views": {}
        }
        return self

    def create_collection(self, database_name, collection_name, options=None):
        if database_name in self.databases:
            self.databases[database_name]["collections"][collection_name] = {
                "name": collection_name,
                "capped": False,
                "size": None,
                "max": None,
                "validator": None,
                "indexes": []
            }
        return self

    def create_index(self, database_name, collection_name, keys, index_type="single", options=None):
        return {
            "database": database_name,
            "collection": collection_name,
            "keys": keys,  # [{"field": "name", "direction": "asc"}]
            "index_type": index_type,  # single, compound, text, 2dsphere, hashed
            "options": options or {
                "unique": False,
                "sparse": False,
                "background": True
            }
        }

    def create_text_index(self, database_name, collection_name, fields, default_language="english"):
        return {
            "database": database_name,
            "collection": collection_name,
            "keys": fields,
            "index_type": "text",
            "options": {
                "default_language": default_language,
                "weights": {},
                "language_override": "language"
            }
        }

    def create_2dsphere_index(self, database_name, collection_name, field):
        return {
            "database": database_name,
            "collection": collection_name,
            "keys": [{field: "2dsphere"}],
            "index_type": "2dsphere"
        }

    def create_atlas_search_index(self, database_name, collection_name, definition):
        return {
            "database": database_name,
            "collection": collection_name,
            "type": "search",
            "definition": definition,
            "mappings": {"dynamic": True}
        }

    def create_user(self, username, password, roles, database="admin"):
        return {
            "user": username,
            "pwd": password,
            "roles": roles,  # [{"role": "readWrite", "db": "myapp"}]
            "authenticationRestrictions": [],
            "mechanisms": ["SCRAM-SHA-256"]
        }

    def create_role(self, role_name, privileges, roles=None):
        return {
            "role": role_name,
            "privileges": privileges,  # [{"resource": {"db": "myapp", "collection": "users"}, "actions": ["find", "update"]}]
            "roles": roles or []
        }

    def create_view(self, database_name, view_name, source_collection, pipeline):
        if database_name in self.databases:
            self.databases[database_name]["views"][view_name] = {
                "view_on": source_collection,
                "pipeline": pipeline,
                "collation": None
            }
        return self

    def create_lookup_pipeline(self, from_collection, local_field, foreign_field, as_field):
        return [
            {"$lookup": {
                "from": from_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_field
            }}
        ]

    def configure_change_stream(self, database_name, collection_name, pipeline=None):
        return {
            "database": database_name,
            "collection": collection_name,
            "pipeline": pipeline or [],
            "full_document": "updateLookup",
            "resume_after": None
        }

    def create_aggregation_pipeline(self, stages):
        return {
            "stages": stages,
            "allow_disk_use": True,
            "batch_size": 101
        }

    def configure_atlas_search(self, database_name, collection_name):
        return {
            "database": database_name,
            "collection": collection_name,
            "analyzers": [{"name": "standard", "tokenizer": {"type": "standard"}}],
            "indexes": []
        }

    def create_transaction(self, session, operations):
        with session.start_transaction():
            for op in operations:
                session.execute_operation(op)
        return {"status": "committed", "transaction_id": None}

    def configure_backup(self, method="cloud", retention_days=30):
        return {
            "method": method,  # cloud, file_system, blockstore
            "retention_days": retention_days,
            "snapshot_interval_hours": 6,
            "oplog_grab_frequency_seconds": 6
        }

    def configure_mongos_load_balancing(self, sharded_cluster_name):
        return {
            "cluster_name": sharded_cluster_name,
            "load_balancing": True,
            "consistent_routing": True,
            "sort_pass_merges": True
        }

    def create_atlas_cluster(self, name, provider, instance_size, region, backup_enabled=True):
        return {
            "name": name,
            "provider": provider,  # AWS, GCP, Azure
            "instance_size": instance_size,
            "region": region,
            "backup_enabled": backup_enabled,
            "auto_scaling": {"compute_enabled": True, "disk_gb_enabled": True}
        }

    def configure_performance_advisor(self, cluster_name, enabled=True):
        return {
            "cluster_name": cluster_name,
            "enabled": enabled,
            "sampling_rate": 60,
            "recommendations": []
        }

    def create_data_lake(self, name, storage_provider, storage_path, regions):
        return {
            "name": name,
            "storage_provider": storage_provider,
            "storage_path": storage_path,
            "regions": regions,
            "data_processors": []
        }
