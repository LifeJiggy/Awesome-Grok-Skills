---
name: "MongoDB Operations"
version: "2.0.0"
description: "Comprehensive MongoDB administration toolkit with document modeling, aggregation pipelines, replica set management, sharding, change streams, and performance optimization for production MongoDB deployments"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database", "mongodb", "nosql", "document-modeling", "aggregation", "sharding"]
category: "database"
personality: "mongodb-specialist"
use_cases: ["document modeling", "aggregation pipelines", "replica set management", "sharding", "change streams"]
---

# MongoDB Operations

> Production-grade MongoDB administration framework providing document modeling, aggregation pipelines, replica set management, sharding strategies, change streams, and performance optimization for reliable MongoDB deployments.

## Overview

The MongoDB Operations module provides a comprehensive toolkit for managing MongoDB in production environments. It implements document schema design with validation rules, aggregation pipeline construction with optimization, replica set monitoring and failover management, sharding strategy selection and balancer configuration, change stream processing for real-time data pipelines, and performance analysis with index optimization. Every operation includes retry logic, connection pooling, and structured logging.

## Core Capabilities

### 1. Document Modeling and Schema Design
- Schema validation with JSON Schema
- Reference vs embedding strategy guidance
- Polymorphic pattern implementation
- Attribute pattern for variable fields
- Bucket pattern for time-series data
- Schema versioning and migration

### 2. Aggregation Pipeline Builder
- Pipeline stage construction with type safety
- Pipeline optimization and explain analysis
- $lookup (join) optimization
- $graphLookup for hierarchical data
- $facet for multi-pipeline analysis
- $unionWith for cross-collection aggregation

### 3. Replica Set Management
- Health monitoring and election tracking
- Oplog analysis and lag monitoring
- Read preference configuration
- Write concern management
- Automatic failover handling
- Arbiter management

### 4. Sharding Strategy
- Hashed sharding for even distribution
- Range sharding for range queries
- Zone sharding for data locality
- Shard key selection guidance
- Balancer configuration and monitoring
- Chunk migration tracking

### 5. Change Streams
- Real-time change event processing
- Pipeline filtering for relevant changes
- Resume token management for reliability
- Full document lookup on updates
- Error recovery and reconnection

### 6. Performance Optimization
- Index usage analysis and recommendations
- Query plan analysis (explain)
- Slow query detection and profiling
- Connection pool monitoring
- Storage engine metrics
- WiredTiger cache analysis

## Usage Examples

### Document Schema Validation

```python
from mongodb import SchemaBuilder, Validator

schema = SchemaBuilder(collection="users")

schema.add_validation(
    validator=Validator({
        "bsonType": "object",
        "required": ["email", "name", "created_at"],
        "properties": {
            "email": {"bsonType": "string", "pattern": "^.+@.+$"},
            "name": {"bsonType": "string", "minLength": 1, "maxLength": 100},
            "age": {"bsonType": "int", "minimum": 0, "maximum": 150},
            "roles": {
                "bsonType": "array",
                "items": {"bsonType": "string", "enum": ["admin", "user", "viewer"]},
            },
            "created_at": {"bsonType": "date"},
        },
    }),
    level="strict",  # strict | moderate | off
)

schema.create()
```

### Aggregation Pipeline

```python
from mongodb import AggregationPipeline, Stage

pipeline = AggregationPipeline(collection="orders")

pipeline.add_stage(Stage.MATCH({
    "status": "completed",
    "created_at": {"$gte": "2024-01-01"},
}))

pipeline.add_stage(Stage.UNWIND("$items"))

pipeline.add_stage(Stage.GROUP(
    _id={"product": "$items.product_id", "month": {"$month": "$created_at"}},
    total_quantity={"$sum": "$items.quantity"},
    total_revenue={"$sum": {"$multiply": ["$items.price", "$items.quantity"]}},
    avg_order_value={"$avg": "$total"},
))

pipeline.add_stage(Stage.SORT({"total_revenue": -1}))

pipeline.add_stage(Stage.LIMIT(20))

# Execute and analyze
results = pipeline.execute()
explain = pipeline.explain()
print(f"Pipeline stages: {explain.stages}")
print(f"Execution time: {explain.execution_time_ms:.1f}ms")
print(f"Documents examined: {explain.total_docs_examined}")
```

### Change Stream Processing

```python
from mongodb import ChangeStream, OperationType

stream = ChangeStream(
    collection="inventory",
    pipeline=[
        {"$match": {"operationType": {"$in": ["insert", "update"]}}},
        {"$match": {"fullDocument.quantity": {"$lt": 10}}},
    ],
)

# Process changes with automatic resume
for change in stream.listen(resume_token=None):
    print(f"Low stock alert: {change.full_document}")
    print(f"  Product: {change.full_document['product_id']}")
    print(f"  Quantity: {change.full_document['quantity']}")
    print(f"  Operation: {change.operation_type}")

    # Save resume token for reliability
    stream.save_resume_token(change.resume_token)
```

### Shard Management

```python
from mongodb import ShardManager, ShardingStrategy

shard_mgr = ShardManager()

# Enable sharding with hashed key
shard_mgr.enable_sharding(
    database="ecommerce",
    collection="orders",
    strategy=ShardingStrategy.HASHED,
    shard_key="customer_id",
)

# Configure zones for data locality
shard_mgr.add_zone_tag(
    shard="shard-us-east-1",
    zone="us-east",
    min_value={"region": "US"},
    max_value={"region": "USZZ"},
)

# Monitor balancer
status = shard_mgr.balancer_status()
print(f"Balancer active: {status.active}")
print(f"Currently balancing: {status.currently_balancing}")
print(f"Chunks migrated today: {status.chunks_migrated_today}")
```

### Index Optimization

```python
from mongodb import IndexAnalyzer, QueryProfiler

analyzer = IndexAnalyzer(collection="orders")

# Analyze index usage
usage = analyzer.index_usage_stats()
for idx in usage:
    print(f"  {idx.name}: {idx.accesses_ops} ops, {idx.size_mb:.1f} MB")

# Get recommendations
recommendations = analyzer.recommendations()
for rec in recommendations:
    print(f"  Recommendation: {rec.description}")
    print(f"    Impact: {rec.estimated_impact}")

# Profile slow queries
profiler = QueryProfiler(database="ecommerce", threshold_ms=100)
slow_queries = profiler.get_slow_queries(limit=5)
for q in slow_queries:
    print(f"  {q.duration_ms:.0f}ms: {q.command}")
```

## Best Practices

### Document Design
- Embed when data is accessed together; reference when data is independent
- Keep document size under 16MB; use GridFS for large files
- Use the bucket pattern for time-series data to avoid unbounded array growth
- Design schemas for your query patterns, not your data structure

### Aggregation
- Place $match and $sort before $lookup to reduce documents processed
- Use $project early to limit fields passed to subsequent stages
- Create indexes that support your aggregation pipeline's first $match stage
- Use $facet sparingly — it runs multiple pipelines on the same data

### Sharding
- Choose shard keys with high cardinality and low frequency
- Avoid monotonically increasing shard keys (like ObjectId) for write-heavy workloads
- Monitor chunk distribution — uneven chunks indicate poor shard key choice
- Use zone sharding for multi-region deployments

### Performance
- Use covered queries (index-only scans) whenever possible
- Limit result sets with .limit() — never fetch unbounded results
- Monitor the WiredTiger cache — evictions indicate memory pressure
- Enable the profiler only in development or for targeted troubleshooting

## Related Modules

- **database-administration**: Cross-database administration and connection pooling
- **query-optimization**: Query performance analysis applicable to MongoDB
- **data-modeling**: Schema design patterns and entity relationships
- **replication**: MongoDB replica set and high availability configuration

---

## Advanced Configuration

### Replica Set Configuration

```python
from mongodb import ReplicaSetManager, ReplicaSetConfig

config = ReplicaSetConfig(
    name="rs0",
    members=[
        {"host": "mongo-primary:27017", "priority": 10, "votes": 1},
        {"host": "mongo-secondary-1:27017", "priority": 5, "votes": 1},
        {"host": "mongo-secondary-2:27017", "priority": 5, "votes": 1},
        {"host": "mongo-arbiter:27017", "priority": 0, "votes": 1},
    ],
    settings={
        "chainingAllowed": True,
        "heartbeatTimeoutSecs": 10,
        "electionTimeoutMillis": 10000,
        "catchUpTimeoutMillis": 60000,
    }
)

rs_manager = ReplicaSetManager()
rs_manager.initiate(config)
```

### Sharding Configuration

```python
from mongodb import ShardManager, ShardConfig

# Configure sharded cluster
cluster_config = ShardConfig(
    config_servers=[
        {"host": "config1:27019", "replSet": "configRS"},
        {"host": "config2:27019", "replSet": "configRS"},
        {"host": "config3:27019", "replSet": "configRS"},
    ],
    shards=[
        {"name": "shard1", "host": "shard1:27018"},
        {"name": "shard2", "host": "shard2:27018"},
        {"name": "shard3", "host": "shard3:27018"},
    ],
    mongos_servers=["mongos1:27017", "mongos2:27017"],
)

shard_manager = ShardManager(cluster_config)
shard_manager.initialize()
```

### Encryption at Rest

```python
from mongodb import EncryptionManager

encryption = EncryptionManager()

# Configure Client-Side Field Level Encryption (CSFLE)
csfle_config = {
    "keyVaultNamespace": "encryption.__keyVault",
    "kmsProviders": {
        "aws": {
            "accessKeyId": os.environ["AWS_ACCESS_KEY_ID"],
            "secretAccessKey": os.environ["AWS_SECRET_ACCESS_KEY"],
        }
    },
    "schemaMap": {
        "users.users": {
            "bsonType": "object",
            "properties": {
                "email": {
                    "encrypt": {
                        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
                        "keyId": {"$ref": "encryption.dataKey"},
                    }
                },
                "ssn": {
                    "encrypt": {
                        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
                        "keyId": {"$ref": "encryption.dataKey"},
                    }
                }
            }
        }
    }
}

encryption.configure(csrf_config)
```

## Architecture Patterns

### Document Reference Pattern

```
┌─────────────────┐      ┌─────────────────┐
│     orders      │      │     products    │
├─────────────────┤      ├─────────────────┤
│ _id             │      │ _id             │
│ customer_id ────┼──────│ name            │
│ items: [        │      │ price           │
│   {             │      │ category        │
│     product_id ─┼──────│                 │
│     quantity    │      └─────────────────┘
│   }             │
│ ]               │
└─────────────────┘
```

### Bucket Pattern (Time Series)

```
┌─────────────────────────────────────────┐
│            sensor_readings              │
├─────────────────────────────────────────┤
│ _id: ObjectId                          │
│ sensor_id: "temp-001"                  │
│ date: ISODate("2024-01-15")            │
│ measurements: [                        │
│   { time: 14:00, value: 22.5 },       │
│   { time: 14:01, value: 22.6 },       │
│   ... (up to 1440 entries per day)     │
│ ]                                      │
└─────────────────────────────────────────┘
```

### Outbox Pattern (Change Data Capture)

```
┌─────────────────┐      ┌─────────────────┐
│   orders        │      │   outbox        │
├─────────────────┤      ├─────────────────┤
│ _id             │◄─────│ aggregate_id    │
│ total           │      │ event_type      │
│ status          │      │ payload         │
└─────────────────┘      │ created_at      │
                         │ processed       │
                         └─────────────────┘
```

## Integration Guide

### Express.js Integration

```javascript
const { MongoClient } = require('mongodb');

const client = new MongoClient(process.env.MONGODB_URI, {
  maxPoolSize: 50,
  minPoolSize: 10,
  maxIdleTimeMS: 30000,
  connectTimeoutMS: 5000,
  retryWrites: true,
  retryReads: true,
  readPreference: 'secondaryPreferred',
  readConcern: { level: 'majority' },
  writeConcern: { w: 'majority', j: true, wtimeout: 5000 },
});

async function getCollection(name) {
  const db = client.db('production');
  return db.collection(name);
}
```

### Node.js Mongoose Integration

```javascript
const mongoose = require('mongoose');

const connectionOptions = {
  maxPoolSize: 50,
  minPoolSize: 10,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
  family: 4,
};

mongoose.connect(process.env.MONGODB_URI, connectionOptions);

mongoose.connection.on('connected', () => {
  console.log('MongoDB connected successfully');
});

mongoose.connection.on('error', (err) => {
  console.error('MongoDB connection error:', err);
});
```

## Performance Optimization

### Index Optimization

```javascript
// Create compound indexes for common queries
db.orders.createIndex({ customer_id: 1, created_at: -1 });
db.orders.createIndex({ status: 1, total: -1 });

// Create partial indexes for filtered queries
db.users.createIndex(
  { email: 1 },
  { unique: true, partialFilterExpression: { deleted: false } }
);

// Create TTL indexes for automatic expiration
db.sessions.createIndex(
  { created_at: 1 },
  { expireAfterSeconds: 3600 }
);
```

### Query Performance

```javascript
// Use explain to analyze query performance
db.orders.find({ customer_id: "cust123", status: "active" })
  .explain("executionStats");

// Optimize with projection to reduce document size
db.orders.find(
  { customer_id: "cust123" },
  { items: 0 }  // Exclude large array field
);

// Use covered queries (index-only scans)
db.users.find(
  { email: "user@example.com" },
  { email: 1, _id: 0 }
);
```

### Bulk Operations

```javascript
// Bulk insert
const ops = orders.map(order => ({
  insertOne: { document: order }
}));
await db.orders.bulkWrite(ops, { ordered: false });

// Bulk upsert
const upserts = products.map(product => ({
  updateOne: {
    filter: { sku: product.sku },
    update: { $set: product },
    upsert: true,
  }
}));
await db.products.bulkWrite(upserts);
```

## Security Considerations

### Role-Based Access Control

```javascript
// Create application user with limited privileges
db.createUser({
  user: "app_readonly",
  pwd: process.env.DB_PASSWORD,
  roles: [
    { role: "read", db: "production" }
  ]
});

// Create admin user with specific permissions
db.createUser({
  user: "db_admin",
  pwd: process.env.ADMIN_PASSWORD,
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
});
```

### Network Security

```javascript
// Bind to specific interfaces
// mongod --bind_ip 127.0.0.1,10.0.0.1

// Enable TLS
// mongod --tlsMode requireTLS --tlsCertificateKeyFile /path/to/cert.pem

// Configure audit logging
// mongod --auditDestination file --auditPath /var/log/mongodb/audit.json
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Connection refused | Cannot connect to MongoDB | Check mongod is running, port is correct, firewall allows connection |
| Replication lag | Secondary out of sync | Check network, increase oplog size, verify secondary reads |
| Memory pressure | High resident memory | Increase WiredTiger cache size, add RAM, optimize queries |
| Slow queries | High latency | Add indexes, use explain(), optimize aggregation pipelines |
| Chunk migration | Balancer issues | Check shard key distribution, verify balancer window |

### Diagnostic Commands

```javascript
// Check replica set status
rs.status();

// Check current operations
db.currentOp();

// Check server status
db.serverStatus();

// Check database stats
db.stats();

// Check collection stats
db.orders.stats();

// Analyze slow queries
db.setProfilingLevel(1, { slowms: 100 });
db.system.profile.find().sort({ ts: -1 }).limit(10);
```

## API Reference

### Collection Operations

```typescript
interface Collection {
  insertOne(doc: Document): Promise<InsertOneResult>;
  insertMany(docs: Document[]): Promise<InsertManyResult>;
  find(filter: Filter, options?: FindOptions): FindCursor;
  findOne(filter: Filter, options?: FindOptions): Promise<Document | null>;
  updateOne(filter: Filter, update: Update, options?: UpdateOptions): Promise<UpdateResult>;
  updateMany(filter: Filter, update: Update, options?: UpdateOptions): Promise<UpdateResult>;
  deleteOne(filter: Filter): Promise<DeleteResult>;
  deleteMany(filter: Filter): Promise<DeleteResult>;
  aggregate(pipeline: PipelineStage[]): AggregationCursor;
  createIndex(spec: IndexSpecification, options?: CreateIndexesOptions): Promise<string>;
  dropIndex(name: string): Promise<Document>;
}
```

### Aggregation Pipeline Stages

```typescript
type PipelineStage =
  | { $match: Filter }
  | { $group: { _id: any; [key: string]: Accumulator } }
  | { $sort: { [key: string]: 1 | -1 } }
  | { $project: { [key: string]: 0 | 1 | Expression } }
  | { $limit: number }
  | { $skip: number }
  | { $unwind: string | { path: string; includeArrayIndex?: string } }
  | { $lookup: LookupStage }
  | { $facet: { [key: string]: PipelineStage[] } }
  | { $addFields: { [key: string]: Expression } }
  | { $bucket: BucketStage }
  | { $bucketAuto: BucketAutoStage }
  | { $count: string }
  | { $densify: DensifyStage }
  | { $fill: FillStage }
  | { $graphLookup: GraphLookupStage }
  | { $merge: MergeStage }
  | { $out: string | { db: string; coll: string } }
  | { $replaceRoot: { newRoot: Expression } }
  | { $set: { [key: string]: Expression } }
  | { $unionWith: string | { coll: string; pipeline?: PipelineStage[] } }
  | { $unset: string | string[] }
  | { $sample: { size: number } }
  | { $shuffle: { outputField?: string } };
```

## Data Models

### Common Document Schemas

```javascript
// User document
{
  _id: ObjectId,
  email: String,
  name: String,
  profile: {
    avatar: String,
    bio: String,
    preferences: {
      theme: String,
      language: String,
      notifications: Boolean
    }
  },
  roles: [String],
  organization_id: ObjectId,
  created_at: Date,
  updated_at: Date,
  deleted_at: Date
}

// Order document
{
  _id: ObjectId,
  customer_id: ObjectId,
  order_number: String,
  status: String,
  items: [{
    product_id: ObjectId,
    name: String,
    quantity: Number,
    price: Number
  }],
  subtotal: Number,
  tax: Number,
  total: Number,
  shipping_address: {
    street: String,
    city: String,
    state: String,
    zip: String,
    country: String
  },
  created_at: Date,
  updated_at: Date
}
```

## Deployment Guide

### Docker Compose

```yaml
version: '3.8'
services:
  mongo1:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all
    ports:
      - "27017:27017"
    volumes:
      - mongo1_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}

  mongo2:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all
    ports:
      - "27018:27017"
    volumes:
      - mongo2_data:/data/db

  mongo3:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all
    ports:
      - "27019:27017"
    volumes:
      - mongo3_data:/data/db

volumes:
  mongo1_data:
  mongo2_data:
  mongo3_data:
```

### Kubernetes StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
spec:
  serviceName: mongodb
  replicas: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongo
        image: mongo:7.0
        ports:
        - containerPort: 27017
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: username
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: password
        volumeMounts:
        - name: data
          mountPath: /data/db
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

## Monitoring & Observability

### Prometheus Metrics

```javascript
// Custom metrics for MongoDB
const client = require('prom-client');

const mongoOperations = new client.Counter({
  name: 'mongo_operations_total',
  help: 'Total MongoDB operations',
  labelNames: ['operation', 'collection', 'status']
});

const mongoDuration = new client.Histogram({
  name: 'mongo_operation_duration_seconds',
  help: 'MongoDB operation duration',
  labelNames: ['operation', 'collection'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
});

// Instrument collection operations
function instrumentCollection(collection) {
  const original = collection.find.bind(collection);
  collection.find = async function(...args) {
    const end = mongoDuration.startTimer({ operation: 'find', collection: collection.collectionName });
    try {
      const result = await original(...args);
      mongoOperations.inc({ operation: 'find', collection: collection.collectionName, status: 'success' });
      return result;
    } catch (err) {
      mongoOperations.inc({ operation: 'find', collection: collection.collectionName, status: 'error' });
      throw err;
    } finally {
      end();
    }
  };
}
```

### Alerting Rules

```yaml
groups:
  - name: mongodb_alerts
    rules:
      - alert: MongoDBReplicationLag
        expr: mongodb_replication_lag_seconds > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "MongoDB replication lag exceeds threshold"
          
      - alert: MongoDBConnectionPoolExhausted
        expr: mongodb_connections_active / mongodb_connections_max > 0.9
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "MongoDB connection pool nearly exhausted"
          
      - alert: MongoDBSlowQueries
        expr: rate(mongodb_slow_queries_total[5m]) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High rate of slow MongoDB queries"
```

## Testing Strategy

### Unit Tests

```javascript
const { MongoMemoryServer } = require('mongodb-memory-server');
const { MongoClient } = require('mongodb');

describe('MongoDB Operations', () => {
  let mongod;
  let client;
  let db;

  beforeAll(async () => {
    mongod = await MongoMemoryServer.create();
    client = await MongoClient.connect(mongod.getUri());
    db = client.db('test');
  });

  afterAll(async () => {
    await client.close();
    await mongod.stop();
  });

  test('should insert and retrieve document', async () => {
    const collection = db.collection('users');
    await collection.insertOne({ name: 'John', email: 'john@example.com' });
    
    const user = await collection.findOne({ name: 'John' });
    expect(user.email).toBe('john@example.com');
  });

  test('should handle aggregation pipeline', async () => {
    const collection = db.collection('orders');
    await collection.insertMany([
      { status: 'active', total: 100 },
      { status: 'active', total: 200 },
      { status: 'completed', total: 300 },
    ]);

    const result = await collection.aggregate([
      { $match: { status: 'active' } },
      { $group: { _id: null, total: { $sum: '$total' } } }
    ]).toArray();

    expect(result[0].total).toBe(300);
  });
});
```

### Integration Tests

```javascript
describe('Replica Set Operations', () => {
  test('should handle failover', async () => {
    // Simulate primary failure
    const primary = rs.status().members.find(m => m.stateStr === 'PRIMARY');
    await mongoStop(primary.name);
    
    // Wait for election
    await sleep(10000);
    
    // Verify new primary exists
    const newStatus = rs.status();
    const newPrimary = newStatus.members.find(m => m.stateStr === 'PRIMARY');
    expect(newPrimary).toBeDefined();
    expect(newPrimary.name).not.toBe(primary.name);
  });
});
```

## Versioning & Migration

### Schema Versioning

```javascript
// Define schema versions
const schemas = {
  v1: {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["email", "name"],
        properties: {
          email: { bsonType: "string" },
          name: { bsonType: "string" }
        }
      }
    }
  },
  v2: {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["email", "name", "created_at"],
        properties: {
          email: { bsonType: "string" },
          name: { bsonType: "string" },
          created_at: { bsonType: "date" }
        }
      }
    }
  }
};

// Migration function
async function migrateSchema(db, collectionName, fromVersion, toVersion) {
  const collection = db.collection(collectionName);
  const schema = schemas[toVersion];
  
  // Update validation
  await db.command({
    collMod: collectionName,
    validator: schema.validator,
    validationLevel: 'strict'
  });
}
```

## Glossary

| Term | Definition |
|------|------------|
| **BSON** | Binary JSON - MongoDB's binary encoding of JSON |
| **Oplog** | Operations log -用于replication的操作日志 |
| **WiredTiger** | MongoDB的默认存储引擎 |
| **Replica Set** | 一组维护相同数据集的mongod进程 |
| **Shard** | 分片集群中的数据分片 |
| **Chunk** | 分片中的连续范围数据块 |
| **Balancer** | 负责在分片间迁移chunks的进程 |
| **CSFLE** | Client-Side Field Level Encryption |
| **Change Stream** | 实时数据变更事件流 |
| **Aggregation Pipeline** | 数据处理管道 |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added MongoDB 7.0 support
- New CSFLE encryption manager
- Improved sharding configuration API
- Added time series collection support

### Version 2.5.0 (2023-12-01)
- Added change stream improvements
- New aggregation pipeline builder
- Improved replica set monitoring
- Added Kubernetes deployment templates

### Version 2.0.0 (2023-09-15)
- Major API redesign
- Added sharding support
- New schema validation system
- Improved performance optimization tools

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/awesome-grok/mongodb-operations.git
cd mongodb-operations

# Install dependencies
npm install

# Run tests
npm test

# Run linting
npm run lint

# Start local MongoDB
docker-compose up -d
```

### Code Style

- Use TypeScript for type safety
- Follow Airbnb JavaScript Style Guide
- Write JSDoc comments for public functions
- Use async/await over callbacks
- Keep functions under 30 lines

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