class MessageQueues:
    def __init__(self):
        self.brokers = {}

    def create_kafka_cluster(self, name, brokers=None, zookeeper=None, schema_registry=None):
        self.brokers[name] = {
            "type": "kafka",
            "brokers": brokers or ["localhost:9092"],
            "zookeeper": zookeeper or "localhost:2181",
            "schema_registry": schema_registry,
            "config": {
                "default_replication_factor": 3,
                "min_insync_replicas": 2,
                "auto_create_topics": True,
                "log_retention_hours": 168,
                "log_segment_bytes": 1073741824
            }
        }
        return self

    def create_topic(self, cluster_name, topic_name, partitions=3, replication_factor=3, config=None):
        return {
            "cluster": cluster_name,
            "topic": topic_name,
            "partitions": partitions,
            "replication_factor": replication_factor,
            "config": config or {
                "retention.ms": "604800000",
                "cleanup.policy": "delete"
            }
        }

    def create_consumer_group(self, group_id, topics=None, auto_offset_reset="earliest", enable_auto_commit=True):
        return {
            "group_id": group_id,
            "topics": topics or [],
            "auto_offset_reset": auto_offset_reset,
            "enable_auto_commit": enable_auto_commit,
            "session_timeout_ms": 30000,
            "heartbeat_interval_ms": 3000
        }

    def create_rabbitmq_cluster(self, name, host="localhost", port=5672, management_port=15672):
        self.brokers[name] = {
            "type": "rabbitmq",
            "host": host,
            "port": port,
            "management_port": management_port,
            "vhosts": ["/"],
            "config": {
                "default_user": "guest",
                "default_vhost": "/",
                "cluster": {"nodes": []}
            }
        }
        return self

    def create_exchange(self, cluster_name, exchange_name, exchange_type="direct", durable=True, config=None):
        return {
            "cluster": cluster_name,
            "exchange": exchange_name,
            "type": exchange_type,
            "durable": durable,
            "auto_delete": False,
            "internal": False,
            "config": config or {}
        }

    def create_queue(self, cluster_name, queue_name, durable=True, arguments=None):
        return {
            "cluster": cluster_name,
            "queue": queue_name,
            "durable": durable,
            "auto_delete": False,
            "exclusive": False,
            "arguments": arguments or {
                "x-message-ttl": 86400000,
                "x-max-length": 1000000
            }
        }

    def create_binding(self, cluster_name, exchange, queue, routing_key=None):
        return {
            "cluster": cluster_name,
            "exchange": exchange,
            "queue": queue,
            "routing_key": routing_key or "",
            "arguments": {}
        }

    def create_sqs_queue(self, name, region="us-east-1", config=None):
        return {
            "type": "sqs",
            "name": name,
            "region": region,
            "attributes": config or {
                "VisibilityTimeout": 30,
                "MessageRetentionPeriod": 345600,
                "MaximumMessageSize": 262144,
                "ReceiveMessageWaitTimeSeconds": 0
            },
            "redrive_policy": {
                "deadLetterTargetArn": None,
                "maxReceiveCount": 5
            }
        }

    def configure_consumer(self, queue_name, consumer_type="group", concurrency=1, prefetch_count=10):
        return {
            "queue": queue_name,
            "consumer_type": consumer_type,
            "concurrency": concurrency,
            "prefetch_count": prefetch_count,
            "ack_mode": "auto"
        }

    def create_publisher(self, topic, publisher_type="sync", batch_size=100, linger_ms=5):
        return {
            "topic": topic,
            "type": publisher_type,
            "batch_size": batch_size,
            "linger_ms": linger_ms,
            "compression": "lz4",
            "acks": "all"
        }

    def configure_schema_registry(self, cluster_name, compatibility="BACKWARD", schema_cache_size=1000):
        return {
            "cluster": cluster_name,
            "compatibility": compatibility,
            "schema_cache_size": schema_cache_size,
            "subjects": []
        }

    def create_avro_schema(self, schema_name, schema_def):
        return {
            "name": schema_name,
            "type": "avro",
            "schema": schema_def,
            "references": []
        }

    def create_protobuf_schema(self, schema_name, proto_def):
        return {
            "name": schema_name,
            "type": "protobuf",
            "proto": proto_def,
            "dependencies": []
        }

    def configure_monitoring(self, cluster_name, metrics_interval=30, alerting_rules=None):
        return {
            "cluster": cluster_name,
            "metrics_interval_seconds": metrics_interval,
            "alerting": alerting_rules or [
                {"metric": "under_replicated_partitions", "threshold": 0, "severity": "warning"},
                {"metric": "offline_partitions", "threshold": 0, "severity": "critical"}
            ]
        }

    def create_connectors(self, cluster_name, connectors=None):
        return {
            "cluster": cluster_name,
            "connectors": connectors or [],
            "worker_config": {
                "tasks.max": 5,
                "offset.flush.interval.ms": 60000
            }
        }

    def create_source_connector(self, name, source_class, config):
        return {
            "name": name,
            "type": "source",
            "class": source_class,
            "config": config
        }

    def create_sink_connector(self, name, sink_class, config):
        return {
            "name": name,
            "type": "sink",
            "class": sink_class,
            "config": config
        }

    def configure_stream_processing(self, application_id, processing_guarantee="exactly_once_v2", config=None):
        return {
            "application_id": application_id,
            "processing_guarantee": processing_guarantee,
            "config": config or {
                "bootstrap.servers": "localhost:9092",
                "commit_interval_ms": 1000,
                "replication_factor": 3
            }
        }

    def create_kstream(self, stream_name, topic, consumed_config=None, produced_config=None):
        return {
            "name": stream_name,
            "topic": topic,
            "consumed": consumed_config or {"auto.offset.reset": "earliest"},
            "produced": produced_config or {"acks": "all"}
        }

    def create_windowed_stream(self, stream_name, topic, window_type="tumbling", window_size_ms=60000):
        return {
            "name": stream_name,
            "topic": topic,
            "window": {
                "type": window_type,
                "size_ms": window_size_ms,
                "grace_period_ms": 60000
            }
        }
