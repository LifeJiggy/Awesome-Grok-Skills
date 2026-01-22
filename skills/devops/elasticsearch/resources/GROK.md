# Elasticsearch

## Overview

Elasticsearch is a distributed search and analytics engine built on Apache Lucene, providing full-text search, structured search, analytics, and logging capabilities. This skill covers Elasticsearch cluster management, index design, query DSL, aggregations, and operational tooling. Elasticsearch powers search experiences and powers observability stacks across the industry.

## Core Capabilities

Inverted indexes enable fast full-text search across documents. Distributed architecture scales horizontally across nodes and clusters. RESTful API provides comprehensive access to all features. Query DSL supports complex queries, filters, and scoring.

Aggregations enable powerful analytics including metrics, buckets, and pipelines. Index lifecycle management automates data retention and optimization. Ingest pipelines transform documents during indexing. Cross-cluster search enables federated queries across clusters.

## Usage Examples

```python
from elasticsearch import Elasticsearch

es = Elasticsearch()

es.create_cluster(
    name="production-es",
    version="8.11",
    node_type="data"
)

index = es.create_index(
    index_name="products",
    settings={
        "number_of_shards": 3,
        "number_of_replicas": 1,
        "refresh_interval": "1s"
    },
    mappings=es.create_mapping(
        properties={
            **es.create_text_field("name", analyzer="standard"),
            **es.create_text_field("description", analyzer="english"),
            **es.create_keyword_field("sku"),
            **es.create_keyword_field("category"),
            **es.create_numeric_field("price", "double"),
            **es.create_date_field("created_at", format="yyyy-MM-dd'T'HH:mm:ss"),
            **es.create_geo_point_field("location")
        }
    )
)

es.create_custom_analyzer(
    analyzer_name="product_analyzer",
    tokenizer="standard",
    filter=["lowercase", "asciifolding", "product_synonym"]
)

pipeline = es.create_pipeline(
    pipeline_name="document-processing",
    processors=[
        es.create_ingest_attachment("attachment", "content"),
        es.create_ingest_grok("message", patterns=["%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}"]),
        es.create_ingest_date("timestamp", formats=["yyyy-MM-dd HH:mm:ss"])
    ]
)

query = es.create_query(
    query_type="bool",
    query_params={
        "must": [
            es.create_query("match", {"name": "laptop computer"}),
            es.create_query("term", {"category": "electronics"})
        ],
        "filter": [
            es.create_query("range", {"price": {"gte": 500, "lte": 2000}})
        ]
    }
)

aggregation = es.create_aggregation(
    agg_name="sales_by_category",
    agg_type="terms",
    params={"field": "category", "size": 10}
)

es.create_pit(index_name="products", keep_alive="1m")

es.create_snapshot_repository(
    repo_name="backup-repo",
    repo_type="fs",
    settings={"location": "/backup/elasticsearch"}
)

ilm_policy = es.create_ilm_policy(
    policy_name="data-retention",
    phases={
        "hot": es.create_ilm_hot_phase(
            min_age="0ms",
            actions={
                "rollover": {"max_age": "1d", "max_size": "50gb"}
            }
        ),
        "warm": es.create_ilm_warm_phase(
            min_age="7d",
            actions={
                "shrink": {"number_of_shards": 1},
                "forcemerge": {"max_num_segments": 1}
            }
        ),
        "cold": es.create_ilm_cold_phase(
            min_age="30d",
            actions={
                "freeze": {},
                "set_priority": {"priority": 0}
            }
        ),
        "delete": es.create_ilm_delete_phase(
            min_age="90d"
        )
    }
)

es.configure_security(
    anonymous_enabled=False,
    api_keys_enabled=True
)

role = es.create_role(
    role_name="product_reader",
    privileges=["read"] 
)
```

## Best Practices

Design mappings carefully as changing field types is limited. Use appropriate data types for each use case. Implement ILM policies to manage data lifecycle automatically. Configure proper sharding strategy based on data volume and query patterns.

Use aliases for zero-downtime index rotations. Implement proper security with role-based access control. Monitor cluster health and resource utilization. Use point-in-time for consistent pagination across searches. Test queries with explain API before production deployment.

## Related Skills

- Log Management (logging infrastructure)
- Business Intelligence (analytics)
- Data Warehousing (data storage)
- DevOps (operations)

## Use Cases

Enterprise search provides fast, relevant search across document repositories. Log aggregation centralizes and analyzes application and infrastructure logs. Application performance monitoring collects and analyzes traces and metrics. E-commerce search powers product discovery with faceted navigation. Security analytics enables threat detection and investigation.
