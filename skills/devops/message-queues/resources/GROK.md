# Message Queues

## Overview

Message Queues enable asynchronous communication between distributed systems, providing decoupling, reliability, and scalability. This skill covers message broker configuration, queue management, pub/sub patterns, and streaming platforms. Message queues are fundamental to event-driven architectures and microservices communication.

## Core Capabilities

Kafka provides distributed, fault-tolerant streaming with high throughput and durability. RabbitMQ offers flexible routing with exchanges, bindings, and queues. Amazon SQS provides fully managed queue infrastructure with automatic scaling. Pub/sub patterns enable one-to-many message distribution.

Consumer groups enable parallel processing with coordinated offset management. Dead letter queues capture failed messages for analysis and reprocessing. Schema registries ensure message compatibility across producers and consumers. Stream processing enables real-time data transformation and analytics.

## Usage Examples

```python
from message_queues import MessageQueues

mq = MessageQueues()

mq.create_kafka_cluster(
    name="production-kafka",
    brokers=["kafka1:9092", "kafka2:9092", "kafka3:9092"],
    schema_registry="http://schema-registry:8081"
)

topic = mq.create_topic(
    cluster_name="production-kafka",
    topic_name="orders",
    partitions=12,
    replication_factor=3,
    config={
        "retention.ms": "604800000",
        "cleanup.policy": "delete",
        "min.insync.replicas": "2"
    }
)

consumer_group = mq.create_consumer_group(
    group_id="order-processors",
    topics=["orders", "order-events"],
    auto_offset_reset="earliest",
    enable_auto_commit=False
)

mq.create_rabbitmq_cluster(
    name="production-rabbitmq",
    host="rabbitmq.example.com",
    port=5672,
    management_port=15672
)

exchange = mq.create_exchange(
    cluster_name="production-rabbitmq",
    exchange_name="orders",
    exchange_type="topic",
    durable=True
)

queue = mq.create_queue(
    cluster_name="production-rabbitmq",
    queue_name="order-processing",
    durable=True,
    arguments={
        "x-message-ttl": 86400000,
        "x-max-length": 100000
    }
)

binding = mq.create_binding(
    cluster_name="production-rabbitmq",
    exchange="orders",
    queue="order-processing",
    routing_key="order.created"
)

sqs_queue = mq.create_sqs_queue(
    name="order-notifications",
    region="us-east-1",
    config={
        "VisibilityTimeout": 30,
        "MessageRetentionPeriod": 345600,
        "ReceiveMessageWaitTimeSeconds": 20
    }
)

publisher = mq.create_publisher(
    topic="orders",
    publisher_type="async",
    batch_size=100,
    linger_ms=5
)

consumer = mq.configure_consumer(
    queue_name="orders",
    consumer_type="group",
    concurrency=4,
    prefetch_count=50
)

schema_registry = mq.configure_schema_registry(
    cluster_name="production-kafka",
    compatibility="BACKWARD",
    schema_cache_size=1000
)

avro_schema = mq.create_avro_schema(
    schema_name="OrderEvent",
    schema_def={
        "type": "record",
        "name": "OrderEvent",
        "fields": [
            {"name": "order_id", "type": "string"},
            {"name": "event_type", "type": "string"},
            {"name": "timestamp", "type": "long"}
        ]
    }
)

monitoring = mq.configure_monitoring(
    cluster_name="production-kafka",
    metrics_interval=30,
    alerting_rules=[
        {"metric": "under_replicated_partitions", "threshold": 0, "severity": "warning"},
        {"metric": "offline_partitions", "threshold": 0, "severity": "critical"},
        {"metric": "consumer_lag", "threshold": 10000, "severity": "warning"}
    ]
)

connectors = mq.create_connectors(
    cluster_name="production-kafka",
    connectors=[
        mq.create_source_connector(
            name="db-connector",
            source_class="io.confluent.connect.jdbc.JdbcSourceConnector",
            config={
                "connection.url": "jdbc:postgresql://db:5432/app",
                "topic.prefix": "db-"
            }
        ),
        mq.create_sink_connector(
            name="elastic-connector",
            sink_class="io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
            config={
                "connection.url": "http://elasticsearch:9200",
                "topics": "orders"
            }
        )
    ]
)

stream_config = mq.configure_stream_processing(
    application_id="order-analytics",
    processing_guarantee="exactly_once_v2",
    config={
        "bootstrap.servers": "kafka1:9092",
        "commit_interval_ms": 1000,
        "replication_factor": 3
    }
)

kstream = mq.create_kstream(
    stream_name="order-stats",
    topic="orders",
    consumed_config={"auto.offset.reset": "earliest"},
    produced_config={"acks": "all"}
)

windowed_stream = mq.create_windowed_stream(
    stream_name="order-tumbling-window",
    topic="orders",
    window_type="tumbling",
    window_size_ms=60000
)
```

## Best Practices

Design topics and queues with clear naming conventions and ownership. Implement idempotent producers to handle duplicate messages. Use consumer groups for parallel processing with proper offset management. Monitor consumer lag and set up alerts for processing delays.

Configure appropriate retention policies based on data requirements. Use dead letter queues for failed message handling. Implement schema evolution with backward compatibility. Use compression for high-volume topics. Set up monitoring for queue depth, throughput, and error rates.

## Related Skills

- Event-Driven Architecture (event patterns)
- Microservices (distributed communication)
- Stream Processing (real-time analytics)
- Kafka (streaming platform)

## Use Cases

E-commerce order processing uses message queues to coordinate inventory, payment, and fulfillment. Real-time analytics pipelines stream data through Kafka for processing. Notification systems use queues to manage high-volume message delivery. Microservices communicate asynchronously through message brokers. Data synchronization between systems uses reliable message delivery.
