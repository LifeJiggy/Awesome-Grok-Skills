---
name: "dynamodb-optimization"
category: "nosql-databases"
version: "1.0.0"
tags: ["nosql-databases", "dynamodb-optimization"]
---

# Dynamodb Optimization

## Overview

Comprehensive dynamodb-optimization capabilities within the nosql-databases domain. This module provides tools, frameworks, and best practices for dynamodb-optimization operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from dynamodb-optimization import _module

engine = _module.Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in nosql-databases domain
- Integration points with external systems

---

## Advanced Configuration

### DynamoDB Table Configuration

```python
import boto3
from botocore.config import Config

# Client configuration with retry and connection settings
config = Config(
    region_name='us-east-1',
    retries={
        'max_attempts': 10,
        'mode': 'adaptive'
    },
    max_pool_connections=50,
    connect_timeout=5,
    read_timeout=10
)

dynamodb = boto3.resource('dynamodb', config=config)
client = boto3.client('dynamodb', config=config)

# Create table with advanced settings
table = dynamodb.create_table(
    TableName='Orders',
    KeySchema=[
        {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
        {'AttributeName': 'order_id', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'customer_id', 'AttributeType': 'S'},
        {'AttributeName': 'order_id', 'AttributeType': 'S'},
        {'AttributeName': 'status', 'AttributeType': 'S'},
        {'AttributeName': 'created_at', 'AttributeType': 'N'}
    ],
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'StatusDateIndex',
            'KeySchema': [
                {'AttributeName': 'status', 'KeyType': 'HASH'},
                {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
            ],
            'Projection': {'ProjectionType': 'ALL'},
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 100,
                'WriteCapacityUnits': 50
            }
        }
    ],
    LocalSecondaryIndexes=[
        {
            'IndexName': 'CustomerOrderIndex',
            'KeySchema': [
                {'AttributeName': 'customer_id', 'KeyType': 'HASH'},
                {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
            ],
            'Projection': {'ProjectionType': 'KEYS_ONLY'}
        }
    ],
    BillingMode='PAY_PER_REQUEST',
    StreamSpecification={
        'StreamEnabled': True,
        'StreamViewType': 'NEW_AND_OLD_IMAGES'
    },
    SSESpecification={
        'Enabled': True,
        'SSEType': 'KMS'
    },
    PointInTimeRecoverySpecification={
        'PointInTimeRecoveryEnabled': True
    },
    Tags=[
        {'Key': 'Environment', 'Value': 'production'},
        {'Key': 'Team', 'Value': 'platform'}
    ]
)
```

### DynamoDB Local Configuration

```yaml
# docker-compose.yml for DynamoDB Local
version: '3.8'
services:
  dynamodb-local:
    image: amazon/dynamodb-local
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    command: "-jar DynamoDBLocal.jar -sharedDb -inMemory -port 8000"
    environment:
      AWS_ACCESS_KEY_ID: local
      AWS_SECRET_ACCESS_KEY: local

  # Admin UI
  dynamodb-admin:
    image: aaronshaf/dynamodb-admin
    ports:
      - "8001:8001"
    environment:
      DYNAMO_ENDPOINT: http://dynamodb-local:8000
      AWS_REGION: us-east-1
```

## Architecture Patterns

### Single-Table Design Pattern

```
┌──────────────────────────────────────────────────────────────────┐
│                    Single-Table Design                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PK              │  SK                    │  Attributes          │
│  ─────────────────┼──────────────────────┼───────────────────── │
│  USER#123        │  PROFILE              │  name, email, phone   │
│  USER#123        │  ORDER#2024-001       │  amount, status       │
│  USER#123        │  ORDER#2024-002       │  amount, status       │
│  USER#123        │  SESSION#abc123       │  ip, user_agent       │
│  ORDER#2024-001  │  METADATA             │  customer, items      │
│  ORDER#2024-001  │  PAYMENT#pay_001      │  method, amount       │
│  PRODUCT#456     │  METADATA             │  name, price, stock   │
│  PRODUCT#456     │  REVIEW#rev_789       │  rating, text         │
│                                                                  │
│  GSI1PK: STATUS#active | GSI1SK: created_at                     │
│  GSI2PK: TYPE#order    | GSI2SK: amount                         │
└──────────────────────────────────────────────────────────────────┘
```

### Access Pattern Implementation

```python
class DynamoDBAccessPatterns:
    """Implement common access patterns for single-table design."""

    def __init__(self, table):
        self.table = table

    def get_user_profile(self, user_id):
        """Get user profile."""
        response = self.table.get_item(
            Key={
                'PK': f'USER#{user_id}',
                'SK': 'PROFILE'
            },
            ProjectionExpression='PK, SK, #name, email, phone',
            ExpressionAttributeNames={'#name': 'name'}
        )
        return response.get('Item')

    def get_user_orders(self, user_id, limit=20):
        """Get user orders sorted by date (newest first)."""
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f'USER#{user_id}') &
                                   Key('SK').begins_with('ORDER#'),
            ScanIndexForward=False,
            Limit=limit,
            ProjectionExpression='PK, SK, amount, #status, created_at',
            ExpressionAttributeNames={'#status': 'status'}
        )
        return response['Items']

    def get_orders_by_status(self, status, date_range=None):
        """Query GSI1 to get orders by status."""
        query_kwargs = {
            'IndexName': 'GSI1',
            'KeyConditionExpression': Key('GSI1PK').eq(f'STATUS#{status}'),
            'ScanIndexForward': False,
            'Limit': 50
        }

        if date_range:
            query_kwargs['KeyConditionExpression'] &= Key('GSI1SK').between(
                date_range['start'], date_range['end']
            )

        return self.table.query(**query_kwargs)['Items']

    def create_order(self, customer_id, order_data):
        """Create order with transaction."""
        order_id = f"ORDER#{uuid.uuid4().hex[:12]}"
        timestamp = int(time.time())

        self.table.transact_write_items(
            TransactItems=[
                {
                    'Put': {
                        'Item': {
                            'PK': f'USER#{customer_id}',
                            'SK': order_id,
                            'GSI1PK': f'STATUS#pending',
                            'GSI1SK': str(timestamp),
                            'amount': order_data['amount'],
                            'status': 'pending',
                            'created_at': timestamp,
                            **order_data
                        }
                    }
                },
                {
                    'Update': {
                        'Key': {
                            'PK': f'USER#{customer_id}',
                            'SK': 'PROFILE'
                        },
                        'UpdateExpression': 'SET order_count = order_count + :inc',
                        'ExpressionAttributeValues': {':inc': 1}
                    }
                }
            ]
        )
        return order_id
```

## Integration Guide

### AWS Lambda Integration

```python
import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    """Handle API Gateway events for orders."""
    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'GET' and '/orders' in path:
        customer_id = event['pathParameters']['customer_id']
        response = table.query(
            KeyConditionExpression=Key('PK').eq(f'USER#{customer_id}') &
                                   Key('SK').begins_with('ORDER#'),
            ScanIndexForward=False
        )
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response['Items'], default=decimal_default)
        }

    elif http_method == 'POST' and '/orders' in path:
        body = json.loads(event['body'])
        order_id = create_order(body)
        return {
            'statusCode': 201,
            'body': json.dumps({'order_id': order_id})
        }

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
```

### Step Functions Integration

```python
# Step Function state machine definition
step_function_definition = {
    "Comment": "Order Processing Pipeline",
    "StartAt": "ValidateOrder",
    "States": {
        "ValidateOrder": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:123456789012:function:validate-order",
            "Next": "CheckInventory"
        },
        "CheckInventory": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:123456789012:function:check-inventory",
            "Next": "ProcessPayment"
        },
        "ProcessPayment": {
            "Type": "Task",
            "Resource": "arn:aws:states:::dynamodb:updateItem",
            "Parameters": {
                "TableName": "Orders",
                "Key": {"PK": {"S.$": "$.customer_id"}, "SK": {"S.$": "$.order_id"}},
                "UpdateExpression": "SET #status = :status, payment_info = :payment",
                "ExpressionAttributeNames": {"#status": "status"},
                "ExpressionAttributeValues": {
                    ":status": {"S": "paid"},
                    ":payment": {"M.$": "$.payment_result"}
                }
            },
            "End": True
        }
    }
}
```

## Performance Optimization

### Capacity Planning

| Workload Type | Read/Write Ratio | Recommended Mode | Strategy |
|--------------|------------------|------------------|----------|
| Read-heavy analytics | 100:1 | On-Demand | GSI for query patterns |
| Write-heavy logging | 1:100 | Provisioned + Auto-scaling | Sparse indexes |
| Balanced e-commerce | 10:1 | On-Demand | Single-table design |
| Time-series IoT | 1:10 | Provisioned | Timestream or sparse index |

### Batch Operations

```python
def batch_write_items(table, items, batch_size=25):
    """Write items in batches of 25 (DynamoDB limit)."""
    responses = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        request_items = {
            'Orders': [
                {'PutRequest': {'Item': item}} for item in batch
            ]
        }

        response = dynamodb.meta.client.batch_write_item(
            RequestItems=request_items
        )

        # Handle unprocessed items
        unprocessed = response.get('UnprocessedItems', {})
        while unprocessed:
            response = dynamodb.meta.client.batch_write_item(
                RequestItems=unprocessed
            )
            unprocessed = response.get('UnprocessedItems', {})

        responses.append(response)

    return responses


def batch_get_items(table, keys, batch_size=100):
    """Read items in batches of 100 (DynamoDB limit)."""
    results = []

    for i in range(0, len(keys), batch_size):
        batch = keys[i:i + batch_size]
        response = dynamodb.meta.client.batch_get_item(
            RequestItems={
                'Orders': {
                    'Keys': [{'PK': k['pk'], 'SK': k['sk']} for k in batch],
                    'ProjectionExpression': 'PK, SK, amount, #status',
                    'ExpressionAttributeNames': {'#status': 'status'}
                }
            }
        )

        results.extend(response['Responses']['Orders'])

        # Handle unprocessed keys
        unprocessed = response.get('UnprocessedKeys', {})
        while unprocessed:
            response = dynamodb.meta.client.batch_get_item(
                RequestItems=unprocessed
            )
            results.extend(response['Responses']['Orders'])
            unprocessed = response.get('UnprocessedKeys', {})

    return results
```

### DAX Caching Layer

```python
import amazondax

# DAX client for in-memory caching
dax_client = amazondax.AmazonDaxClient(
    endpoints=['my-dax-cluster.abc123.dax-clusters.us-east-1.amazonaws.com:8111'],
    region_name='us-east-1'
)

# Transparent caching - same API as DynamoDB
response = dax_client.get_item(
    TableName='Orders',
    Key={'PK': {'S': 'USER#123'}, 'SK': {'S': 'ORDER#001'}}
)

# DAX benefits:
# - Microsecond latency for reads
# - Automatic cache invalidation via DynamoDB Streams
# - Multi-layer caching (item cache + query cache)
# - Write-through caching for consistency
```

## Security Considerations

### IAM Policy Configuration

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowReadWriteOrders",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:123456789012:table/Orders",
        "arn:aws:dynamodb:us-east-1:123456789012:table/Orders/index/*"
      ],
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": ["${aws:PrincipalTag/user_id}"]
        }
      }
    },
    {
      "Sid": "DenyLargeQueries",
      "Effect": "Deny",
      "Action": "dynamodb:Scan",
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/Orders",
      "Condition": {
        "NumericGreaterThan": {"dynamodb:Limit": "1000"}
      }
    }
  ]
}
```

### Encryption and Access Control

```python
# Client-side encryption
from aws_encryption_sdk import (
    KMSMasterKeyProvider,
    CachingCryptographicMaterialsManager,
    LocalCryptographicMaterialsCache
)

kms_key_provider = KMSMasterKeyProvider(
    key_ids=['arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012']
)

crypto_materials_cache = LocalCryptographicMaterialsCache(max_entries=1000)
cmm = CachingCryptographicMaterialsManager(
    underlying_cmm=kms_key_provider,
    cache=crypto_materials_cache,
    max_message_cache_entry_ttl=600
)

# Encrypt before writing
from aws_encryption_sdk import encrypt
ciphertext, header = encrypt(
    source=b"sensitive data",
    key_provider=kms_key_provider
)

# Put encrypted item
table.put_item(Item={
    'PK': 'USER#123',
    'SK': 'SECRET#001',
    'encrypted_data': ciphertext
})
```

## Troubleshooting Guide

### Common DynamoDB Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Throttling | `ProvisionedThroughputExceededException` | Enable auto-scaling, use DAX |
| Hot partition | Uneven latency, throttling on specific keys | Add random suffix, use sparse indexes |
| Large item | `Item size limit exceeded` | Normalize data, use S3 for large objects |
| Query limit | `Query results too large` | Use pagination, implement pagination tokens |
| Transaction conflict | `TransactionCanceledException` | Reduce transaction scope, exponential backoff |
| GSI overuse | High GSI costs | Review access patterns, consolidate GSIs |

```python
def diagnose_dynamodb_issues(table_name):
    """Run diagnostic checks on DynamoDB table."""
    table = dynamodb.Table(table_name)
    client = boto3.client('dynamodb')

    # Check table status
    desc = client.describe_table(TableName=table_name)
    status = desc['Table']['TableStatus']
    print(f"Table Status: {status}")

    # Check capacity
    if 'ProvisionedThroughput' in desc['Table']:
        pt = desc['Table']['ProvisionedThroughput']
        print(f"Provisioned Read: {pt['ReadCapacityUnits']} RU/s")
        print(f"Provisioned Write: {pt['WriteCapacityUnits']} WU/s")

    # Check GSI count
    gsis = desc['Table'].get('GlobalSecondaryIndexes', [])
    print(f"GSIs: {len(gsis)}")
    for gsi in gsis:
        print(f"  - {gsi['IndexName']}: {gsi['IndexStatus']}")

    # Check size
    size_bytes = desc['Table']['TableSizeBytes']
    item_count = desc['Table']['ItemCount']
    print(f"Size: {size_bytes / 1024 / 1024:.2f} MB")
    print(f"Items: {item_count:,}")

    return {
        'status': status,
        'size_mb': size_bytes / 1024 / 1024,
        'item_count': item_count,
        'gsi_count': len(gsis)
    }
```

## API Reference

### DynamoDB CRUD Operations

```python
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Put item
table.put_item(
    Item={
        'user_id': '123',
        'name': 'Alice',
        'email': 'alice@example.com',
        'age': 30,
        'tags': ['admin', 'premium'],
        'address': {
            'street': '123 Main St',
            'city': 'Seattle',
            'state': 'WA'
        }
    }
)

# Get item
response = table.get_item(
    Key={'user_id': '123'},
    ProjectionExpression='user_id, #n, email',
    ExpressionAttributeNames={'#n': 'name'}
)
item = response.get('Item')

# Update item
table.update_item(
    Key={'user_id': '123'},
    UpdateExpression='SET age = :age, #n = :name',
    ExpressionAttributeValues={':age': 31, ':name': 'Alice Smith'},
    ExpressionAttributeNames={'#n': 'name'}
)

# Query
response = table.query(
    IndexName='EmailIndex',
    KeyConditionExpression=Key('email').eq('alice@example.com')
)

# Scan with filter
response = table.scan(
    FilterExpression=Attr('age').gte(25) & Attr('tags').contains('premium'),
    ProjectionExpression='user_id, #n, age',
    ExpressionAttributeNames={'#n': 'name'}
)

# Delete
table.delete_item(Key={'user_id': '123'})

# Transaction
dynamodb.meta.client.transact_write_items(
    TransactItems=[
        {'Put': {'TableName': 'Users', 'Item': {'user_id': '456', 'name': 'Bob'}}},
        {'Update': {
            'TableName': 'Counters',
            'Key': {'counter_id': 'users'},
            'UpdateExpression': 'SET count = count + :inc',
            'ExpressionAttributeValues': {':inc': 1}
        }}
    ]
)
```

### DynamoDB Streams Consumer

```python
import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb Streams = boto3.client('dynamodbstreams')
deserializer = TypeDeserializer()

def process_stream_records(event):
    """Process DynamoDB Stream records."""
    for record in event['Records']:
        event_name = record['eventName']
        dynamodb_data = record['dynamodb']

        if event_name == 'INSERT':
            new_image = {k: deserializer.deserialize(v)
                        for k, v in dynamodb_data['NewImage'].items()}
            handle_insert(new_image)

        elif event_name == 'MODIFY':
            old_image = {k: deserializer.deserialize(v)
                        for k, v in dynamodb_data['OldImage'].items()}
            new_image = {k: deserializer.deserialize(v)
                        for k, v in dynamodb_data['NewImage'].items()}
            handle_modify(old_image, new_image)

        elif event_name == 'REMOVE':
            old_image = {k: deserializer.deserialize(v)
                        for k, v in dynamodb_data['OldImage'].items()}
            handle_remove(old_image)

def lambda_stream_handler(event, context):
    """Lambda handler for DynamoDB Streams."""
    process_stream_records(event)
    return {'statusCode': 200, 'body': 'Processed'}
```

## Data Models

### E-Commerce Single-Table Design

```python
# Schema definition
ECOMMERCE_SCHEMA = {
    'TableName': 'EcommerceApp',
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI2PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI2SK', 'AttributeType': 'N'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': 'GSI1',
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
            ]
        },
        {
            'IndexName': 'GSI2',
            'KeySchema': [
                {'AttributeName': 'GSI2PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI2SK', 'KeyType': 'RANGE'}
            ]
        }
    ]
}

# Access patterns
ACCESS_PATTERNS = """
| Pattern | Table | GSI | Key Conditions |
|---------|-------|-----|----------------|
| Get user profile | Users | - | PK=USER#id, SK=PROFILE |
| Get user orders | Users | - | PK=USER#id, SK begins_with ORDER# |
| Get order details | Orders | - | PK=ORDER#id, SK=METADATA |
| Get orders by status | - | GSI1 | GSI1PK=STATUS#x, GSI1SK=date |
| Get recent products | - | GSI2 | GSI2PK=PRODUCT#active, GSI2SK=created |
| Get cart items | Users | - | PK=USER#id, SK begins_with CART# |
| Get product reviews | Products | - | PK=PRODUCT#id, SK begins_with REVIEW# |
"""
```

## Deployment Guide

### CloudFormation Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: DynamoDB Orders Table

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues: [development, staging, production]

Resources:
  OrdersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${Environment}-orders'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: PK
          AttributeType: S
        - AttributeName: SK
          AttributeType: S
        - AttributeName: GSI1PK
          AttributeType: S
        - AttributeName: GSI1SK
          AttributeType: S
      KeySchema:
        - AttributeName: PK
          KeyType: HASH
        - AttributeName: SK
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: GSI1
          KeySchema:
            - AttributeName: GSI1PK
              KeyType: HASH
            - AttributeName: GSI1SK
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      SSESpecification:
        SSEEnabled: true
        SSEType: KMS
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment

  AutoScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      MaxCapacity: 1000
      MinCapacity: 5
      ResourceId: !Sub 'table/${OrdersTable}'
      ScalableDimension: dynamodb:table:ReadCapacityUnits
      ServiceNamespace: dynamodb
```

## Monitoring & Observability

### CloudWatch Metrics and Alarms

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def create_dynamodb_alarms(table_name):
    """Create CloudWatch alarms for DynamoDB metrics."""

    # Throttled requests alarm
    cloudwatch.put_metric_alarm(
        AlarmName=f'{table_name}-throttled-requests',
        AlarmDescription=f'Throttled requests detected on {table_name}',
        Namespace='AWS/DynamoDB',
        MetricName='ThrottledRequests',
        Dimensions=[{'Name': 'TableName', 'Value': table_name}],
        Statistic='Sum',
        Period=300,
        EvaluationPeriods=2,
        Threshold=10,
        ComparisonOperator='GreaterThanThreshold',
        AlarmActions=['arn:aws:sns:us-east-1:123456789012:alerts']
    )

    # Read capacity alarm
    cloudwatch.put_metric_alarm(
        AlarmName=f'{table_name}-read-capacity',
        Namespace='AWS/DynamoDB',
        MetricName='ConsumedReadCapacityUnits',
        Dimensions=[{'Name': 'TableName', 'Value': table_name}],
        Statistic='Average',
        Period=300,
        EvaluationPeriods=3,
        Threshold=800,
        ComparisonOperator='GreaterThanThreshold'
    )

    # Latency alarm (p99)
    cloudwatch.put_metric_alarm(
        AlarmName=f'{table_name}-high-latency',
        Namespace='AWS/DynamoDB',
        MetricName='SuccessfulRequestLatency',
        Dimensions=[
            {'Name': 'TableName', 'Value': table_name},
            {'Name': 'Operation', 'Value': 'GetItem'}
        ],
        Statistic='p99',
        Period=300,
        EvaluationPeriods=2,
        Threshold=50,  # 50ms
        ComparisonOperator='GreaterThanThreshold'
    )
```

## Testing Strategy

### Local Testing with DynamoDB Local

```python
import boto3
import pytest
from moto import mock_dynamodb2

@pytest.fixture
def dynamodb_table():
    """Create mock DynamoDB table for testing."""
    with mock_dynamodb2():
        client = boto3.client('dynamodb', region_name='us-east-1')
        client.create_table(
            TableName='TestOrders',
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('TestOrders')
        yield table

class TestDynamoDBOperations:
    def test_put_and_get(self, dynamodb_table):
        dynamodb_table.put_item(Item={
            'PK': 'USER#123',
            'SK': 'PROFILE',
            'name': 'Alice'
        })

        response = dynamodb_table.get_item(
            Key={'PK': 'USER#123', 'SK': 'PROFILE'}
        )
        assert response['Item']['name'] == 'Alice'

    def test_query_by_prefix(self, dynamodb_table):
        for i in range(5):
            dynamodb_table.put_item(Item={
                'PK': 'USER#123',
                'SK': f'ORDER#{i:03d}',
                'amount': i * 100
            })

        response = dynamodb_table.query(
            KeyConditionExpression=Key('PK').eq('USER#123') &
                                   Key('SK').begins_with('ORDER#')
        )
        assert len(response['Items']) == 5

    def test_transaction(self, dynamodb_table):
        dynamodb_table.put_item(Item={'PK': 'USER#123', 'SK': 'PROFILE', 'balance': 100})

        dynamodb.meta.client.transact_write_items(
            TransactItems=[
                {'Update': {
                    'Key': {'PK': 'USER#123', 'SK': 'PROFILE'},
                    'UpdateExpression': 'SET balance = balance - :amount',
                    'ExpressionAttributeValues': {':amount': 50}
                }},
                {'Put': {
                    'Item': {
                        'PK': 'USER#123',
                        'SK': 'TRANSACTION#001',
                        'amount': 50,
                        'type': 'debit'
                    }
                }}
            ]
        )

        response = dynamodb_table.get_item(
            Key={'PK': 'USER#123', 'SK': 'PROFILE'}
        )
        assert response['Item']['balance'] == 50
```

## Versioning & Migration

### Schema Migration Script

```python
import boto3
from datetime import datetime

class DynamoDBMigrator:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb')
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def add_gsi(self, gsi_definition):
        """Add a GSI to existing table."""
        self.client.update_table(
            TableName=self.table_name,
            GlobalSecondaryIndexUpdates=[
                {'Create': gsi_definition}
            ]
        )
        # Wait for index to be active
        waiter = self.client.get_waiter('table_exists')
        waiter.wait(TableName=self.table_name)

    def migrate_data(self, transform_func, scan_params=None):
        """Scan and transform all items in table."""
        items = []
        response = self.table.scan(**(scan_params or {}))
        items.extend(response['Items'])

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'],
                **(scan_params or {})
            )
            items.extend(response['Items'])

        # Batch transform and write
        for i in range(0, len(items), 25):
            batch = items[i:i + 25]
            with self.table.batch_writer() as batch_writer:
                for item in batch:
                    transformed = transform_func(item)
                    batch_writer.put_item(Item=transformed)

        return len(items)

# Migration example: Add GSI for status queries
migrator = DynamoDBMigrator('Orders')
migrator.add_gsi({
    'IndexName': 'StatusIndex',
    'KeySchema': [
        {'AttributeName': 'status', 'KeyType': 'HASH'},
        {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
    ],
    'Projection': {'ProjectionType': 'ALL'},
    'ProvisionedThroughput': {'ReadCapacityUnits': 10, 'WriteCapacityUnits': 5}
})
```

## Glossary

| Term | Definition |
|------|------------|
| Partition Key | Attribute used to distribute data across partitions |
| Sort Key | Attribute used to sort items within a partition |
| GSI | Global Secondary Index - separate partition/sort key |
| LSI | Local Secondary Index - shares partition key with table |
| Capacity Unit | Read (4KB) or Write (1KB) unit of throughput |
| On-Demand | Pay-per-request billing mode |
| Provisioned | Pre-allocated capacity billing mode |
| DAX | DynamoDB Accelerator - in-memory caching layer |
| Stream | Change data capture mechanism for table modifications |
| Transaction | ACID operation across multiple items |
| Item | A single data record (like a row) |
| Attribute | A key-value pair within an item (like a column) |
| Scan | Read operation examining every item in table |
| Query | Read operation using key conditions (efficient) |
| Filter Expression | Server-side filtering after query/scan |
| Projection | Attributes returned from an index query |
| Sparse Index | GSI with many null/missing attributes |
| Hot Partition | Uneven access pattern causing throttling |
| Adaptive Capacity | Automatic throughput redistribution |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release with DynamoDB configuration basics |
| 1.1.0 | 2024-02-15 | Added single-table design patterns |
| 1.2.0 | 2024-04-01 | Added DAX caching and batch operations |
| 1.3.0 | 2024-06-01 | Added Lambda and Step Functions integration |
| 1.4.0 | 2024-08-01 | Added security (IAM, encryption) section |
| 1.5.0 | 2024-10-01 | Added monitoring with CloudWatch |
| 1.6.0 | 2025-01-01 | Added testing, migration, and troubleshooting |

## Contributing Guidelines

1. **Naming**: Use consistent PK/SK naming (ENTITY#id pattern)
2. **Testing**: Use moto or DynamoDB Local for unit tests
3. **Documentation**: Document access patterns for all GSIs
4. **Cost**: Review On-Demand vs Provisioned for each use case
5. **Security**: Use IAM policies with least privilege

## License

This module is part of the Awesome-Grok-Skills project and follows the MIT License.
