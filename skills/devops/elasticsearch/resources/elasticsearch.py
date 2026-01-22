class Elasticsearch:
    def __init__(self):
        self.cluster = None

    def create_cluster(self, name, version="8.11", node_type="data"):
        self.cluster = {
            "name": name,
            "version": version,
            "node": {
                "name": f"{name}-node-1",
                "type": node_type,
                "data_paths": ["/var/lib/elasticsearch"],
                "max_local_storage_nodes": 1
            },
            "network": {
                "host": "0.0.0.0",
                "port": 9200,
                "http_compression": True
            }
        }
        return self

    def create_index(self, index_name, settings=None, mappings=None):
        return {
            "index": index_name,
            "settings": settings or {
                "number_of_shards": 1,
                "number_of_replicas": 1,
                "refresh_interval": "1s"
            },
            "mappings": mappings or {
                "properties": {}
            }
        }

    def create_mapping(self, properties):
        return {
            "properties": properties
        }

    def create_field(self, field_name, field_type, analyzer=None):
        field_def = {"type": field_type}
        if analyzer:
            field_def["analyzer"] = analyzer
        return {field_name: field_def}

    def create_text_field(self, field_name, analyzer="standard"):
        return self.create_field(field_name, "text", analyzer)

    def create_keyword_field(self, field_name):
        return self.create_field(field_name, "keyword")

    def create_date_field(self, field_name, format=None):
        field_def = {"type": "date"}
        if format:
            field_def["format"] = format
        return {field_name: field_def}

    def create_numeric_field(self, field_name, numeric_type="long"):
        return self.create_field(field_name, numeric_type)

    def create_geo_point_field(self, field_name):
        return self.create_field(field_name, "geo_point")

    def create_object_field(self, field_name, properties):
        return {field_name: {"type": "object", "properties": properties}}

    def create_nested_field(self, field_name, properties):
        return {field_name: {"type": "nested", "properties": properties}}

    def configure_analyzer(self, analyzer_name, analyzer_type, settings=None):
        return {
            "analyzer": {
                analyzer_name: {
                    "type": analyzer_type,
                    **(settings or {})
                }
            }
        }

    def create_custom_analyzer(self, analyzer_name, tokenizer, filter=None):
        return {
            "analyzer": {
                analyzer_name: {
                    "type": "custom",
                    "tokenizer": tokenizer,
                    "filter": filter or ["lowercase"]
                }
            }
        }

    def create_search_template(self, template_id, source):
        return {
            "id": template_id,
            "source": source
        }

    def create_pipeline(self, pipeline_name, processors):
        return {
            "description": f"Pipeline: {pipeline_name}",
            "processors": processors
        }

    def create_ingest_attachment(self, field_name, target_field="content"):
        return {
            "processor": "attachment",
            "field": field_name,
            "target_field": target_field
        }

    def create_ingest_grok(self, field_name, patterns):
        return {
            "processor": "grok",
            "field": field_name,
            "patterns": patterns
        }

    def create_ingest_date(self, field_name, target_field=None, formats=None):
        return {
            "processor": "date",
            "field": field_name,
            "target_field": target_field or "@timestamp",
            "formats": formats or ["yyyy-MM-dd HH:mm:ss"]
        }

    def create_query(self, query_type, query_params):
        queries = {
            "match": {"match": query_params},
            "term": {"term": query_params},
            "terms": {"terms": query_params},
            "range": {"range": query_params},
            "bool": {"bool": query_params},
            "match_all": {"match_all": query_params},
            "multi_match": {"multi_match": query_params},
            "exists": {"exists": query_params},
            "nested": {"nested": query_params},
            "geo_distance": {"geo_distance": query_params}
        }
        return queries.get(query_type, {})

    def create_aggregation(self, agg_name, agg_type, params):
        aggs = {
            "terms": {"terms": params},
            "date_histogram": {"date_histogram": params},
            "histogram": {"histogram": params},
            "sum": {"sum": params},
            "avg": {"avg": params},
            "min": {"min": params},
            "max": {"max": params},
            "cardinality": {"cardinality": params},
            "nested": {"nested": params},
            "reverse_nested": {"reverse_nested": params},
            "top_hits": {"top_hits": params},
            "bucket_script": {"bucket_script": params}
        }
        return {agg_name: aggs.get(agg_type, {})}

    def create_pit(self, index_name, keep_alive="1m"):
        return {
            "index": index_name,
            "keep_alive": keep_alive
        }

    def create_snapshot_repository(self, repo_name, repo_type, settings):
        return {
            "type": repo_type,
            "settings": settings
        }

    def create_snapshot(self, repo_name, snapshot_name, indices=None):
        return {
            "repository": repo_name,
            "snapshot": snapshot_name,
            "indices": indices or ["*"],
            "include_global_state": True
        }

    def create_ilm_policy(self, policy_name, phases):
        return {
            "policy": {
                "phases": phases
            }
        }

    def create_ilm_hot_phase(self, min_age="0ms", actions=None):
        return {
            "min_age": min_age,
            "actions": actions or {
                "rollover": {
                    "max_age": "1d",
                    "max_size": "50gb"
                }
            }
        }

    def create_ilm_warm_phase(self, min_age, actions):
        return {
            "min_age": min_age,
            "actions": actions or {
                "shrink": {"number_of_shards": 1},
                "forcemerge": {"max_num_segments": 1}
            }
        }

    def create_ilm_cold_phase(self, min_age, actions=None):
        return {
            "min_age": min_age,
            "actions": actions or {
                "freeze": {},
                "set_priority": {"priority": 0}
            }
        }

    def create_ilm_delete_phase(self, min_age, actions=None):
        return {
            "min_age": min_age,
            "actions": actions or {
                "delete": {}
            }
        }

    def configure_security(self, anonymous_enabled=False, api_keys_enabled=True):
        return {
            "anonymous": {
                "enabled": anonymous_enabled
            },
            "api_key": {
                "enabled": api_keys_enabled
            },
            "transport": {
                "ssl": {"enabled": True}
            },
            "http": {
                "ssl": {"enabled": True}
            }
        }

    def create_role(self, role_name, privileges):
        return {
            "role": {
                "role": role_name,
                "privileges": privileges
            }
        }

    def create_user(self, username, password, roles=None):
        return {
            "username": username,
            "password": password,
            "roles": roles or []
        }

    def create_apm_integration(self, service_name):
        return {
            "service": {
                "name": service_name
            },
            "labels": {}
        }

    def create_ml_job(self, job_id, job_type, analysis_config):
        return {
            "job_id": job_id,
            "job_type": job_type,
            "analysis_config": analysis_config,
            "data_description": {}
        }

    def create_data_feed(self, feed_id, job_id, indices, query=None):
        return {
            "job_id": job_id,
            "indices": indices,
            "query": query or {"match_all": {}}
        }

    def create_watcher(self, watch_id, trigger, condition, actions):
        return {
            "trigger": trigger,
            "condition": condition,
            "actions": actions
        }
