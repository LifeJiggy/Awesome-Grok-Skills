---
name: "serverless"
category: "cloud"
version: "2.0.0"
tags: ["cloud", "serverless", "FaaS", "event-driven", "managed-services"]
---

# Serverless

## Overview

The Serverless module provides comprehensive guidance for designing, building, and operating serverless applications across cloud providers. It covers Function-as-a-Service (FaaS), Backend-as-a-Service (BaaS), event-driven architectures, serverless databases, API gateways, and serverless-first design patterns. The module addresses cold start optimization, cost modeling, testing strategies, and production operations.

This skill is essential for serverless architects, cloud-native developers, and teams adopting event-driven, serverless-first architectures.

## Core Capabilities

- **FaaS Platforms**: AWS Lambda, Azure Functions, Google Cloud Functions, and Cloudflare Workers patterns
- **Event-Driven Design**: EventBridge/Event Grid patterns, pub/sub architectures, and event sourcing
- **Serverless APIs**: API Gateway + Lambda patterns, AppSync GraphQL, and HTTP API design
- **Serverless Databases**: DynamoDB, Cosmos DB serverless, PlanetScale, Aurora Serverless, and Fauna
- **Orchestration**: Step Functions, Durable Functions, and workflow engines for multi-step processes
- **Cold Start Optimization**: Provisioned concurrency, connection pooling, and runtime optimization
- **Serverless Storage**: S3, Blob Storage, and file-based serverless patterns
- **Cost Modeling**: Pay-per-request pricing analysis, cost comparison vs containerized, and optimization

## Usage Examples

```python
from serverless import (
    ServerlessArchitect,
    ColdStartOptimizer,
    CostModeler,
    EventDrivenDesigner,
    ServerlessAPIBuilder,
)

# --- Architecture Design ---
architect = ServerlessArchitect()
arch = architect.design(
    workload="e-commerce-api",
    traffic_pattern="bursty",
    data_volume_gb=100,
    concurrent_users=10000,
)
print(f"Compute: {arch.compute_service}")
print(f"Database: {arch.database_service}")
print(f"Storage: {arch.storage_service}")
print(f"Est monthly cost: ${arch.estimated_cost:.0f}")

# --- Cold Start Optimization ---
optimizer = ColdStartOptimizer()
optimization = optimizer.optimize(
    runtime="python3.11",
    memory_mb=1024,
    package_size_mb=50,
    vpc_enabled=True,
    cold_start_ms=3000,
)
print(f"Optimized cold start: {optimization.optimized_ms:.0f}ms")
print(f"Techniques: {', '.join(optimization.techniques)}")

# --- Cost Modeling ---
modeler = CostModeler()
comparison = modeler.compare(
    requests_per_month=10_000_000,
    avg_duration_ms=200,
    memory_mb=256,
    alternative_instance="t3.medium",
)
print(f"Serverless: ${comparison.serverless_cost:.0f}/month")
print(f"EC2 equivalent: ${comparison.container_cost:.0f}/month")
print(f"Savings: ${comparison.savings:.0f}/month")

# --- Event-Driven Design ---
designer = EventDrivenDesigner()
design = designer.design_order_flow(
    steps=["validate", "process_payment", "fulfill", "notify"],
    error_handling="dead_letter_queue",
    saga_pattern=True,
)
print(f"Events: {design.event_count}")
print(f"Steps: {len(design.steps)}")

# --- Serverless API ---
api = ServerlessAPIBuilder()
spec = api.build_rest_api(
    name="orders-api",
    endpoints=[
        {"method": "POST", "path": "/orders", "handler": "create_order"},
        {"method": "GET", "path": "/orders/{id}", "handler": "get_order"},
        {"method": "PUT", "path": "/orders/{id}/status", "handler": "update_status"},
    ],
    auth="cognito",
    throttling=10000,
)
print(f"Endpoints: {len(spec.endpoints)}")
print(f"Auth: {spec.auth_type}")
```

## Best Practices

- Design functions to be idempotent — serverless platforms may retry failed invocations
- Minimize package size — include only required dependencies for faster cold starts
- Use provisioned concurrency for latency-sensitive production workloads
- Implement dead-letter queues for all async invocations to capture failures
- Use environment variables for configuration — never hardcode in function code
- Implement structured logging (JSON) for machine-parseable observability
- Set appropriate memory allocation — more memory = more CPU = faster execution
- Use API Gateway caching for frequently accessed, slow-to-generate responses
- Design for eventual consistency — serverless databases often have read-after-write lag
- Implement circuit breakers for external service calls to prevent cascade failures

## Related Modules

- **aws-architecture**: AWS serverless services and patterns
- **azure-services**: Azure Functions and Durable Functions patterns
- **gcp-platform**: Cloud Functions and Cloud Run patterns
- **multi-cloud**: Serverless patterns that work across providers

## Advanced Configuration

### Serverless Framework Configuration

```yaml
# serverless.yml
service: my-service
frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  stage: ${opt:stage, 'dev'}
  memorySize: 256
  timeout: 30
  environment:
    TABLE_NAME: ${self:service}-${self:provider.stage}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:Scan
            - dynamodb:GetItem
            - dynamodb:PutItem
          Resource: arn:aws:dynamodb:${self:provider.region}:*:table/${self:provider.environment.TABLE_NAME}

functions:
  api:
    handler: handler.api
    events:
      - httpApi:
          path: /{proxy+}
          method: ANY
      - httpApi:
          path: /
          method: ANY
```

### AWS SAM Configuration

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    MemorySize: 256
    Runtime: python3.11

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      CodeUri: src/
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: any
            RestApiId: !Ref MyApi
```

### Environment Configuration

```yaml
environments:
  dev:
    LOG_LEVEL: debug
    TABLE_NAME: my-table-dev
    STAGE: dev
  staging:
    LOG_LEVEL: info
    TABLE_NAME: my-table-staging
    STAGE: staging
  production:
    LOG_LEVEL: warn
    TABLE_NAME: my-table-prod
    STAGE: production
```

## Architecture Patterns

### Serverless Architecture

```
Serverless Architecture:
├── API Layer
│   ├── API Gateway (REST/HTTP)
│   ├── AppSync (GraphQL)
│   └── CloudFront (CDN)
├── Compute Layer
│   ├── Lambda (FaaS)
│   ├── Step Functions (orchestration)
│   └── Fargate (containers)
├── Data Layer
│   ├── DynamoDB (NoSQL)
│   ├── Aurora Serverless (SQL)
│   ├── S3 (objects)
│   └── ElastiCache (cache)
├── Event Layer
│   ├── EventBridge (events)
│   ├── SQS (queues)
│   ├── SNS (notifications)
│   └── Kinesis (streams)
└── Integration
    ├── Cognito (auth)
    ├── AppSync (GraphQL)
    └── Secrets Manager
```

### Event-Driven Architecture

```
Event Flow:
├── Event Sources
│   ├── API Gateway (HTTP)
│   ├── S3 (object events)
│   ├── DynamoDB (stream events)
│   ├── SQS (message events)
│   ├── IoT (device events)
│   └── CloudWatch (scheduled)
├── Event Processing
│   ├── Lambda (processing)
│   ├── Step Functions (workflow)
│   └── EventBridge (routing)
├── Event Targets
│   ├── DynamoDB (state)
│   ├── S3 (storage)
│   ├── SNS (notification)
│   └── External systems
└── Event Patterns
    ├── Content-based filtering
    ├── Time-based scheduling
    └── Fan-out distribution
```

### Saga Pattern Architecture

```
Saga Steps:
├── Order Service
│   ├── Create order
│   ├── Reserve inventory
│   └── Process payment
├── Compensation
│   ├── Payment failed → Release inventory
│   ├── Inventory failed → Cancel order
│   └── All failed → Notify customer
└── Orchestration
    ├── Step Functions (orchestration)
    ├── Lambda (processing)
    └── SQS (async communication)
```

## Integration Guide

### AWS SDK Integration

```python
import boto3
import json

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('my-table')
table.put_item(Item={'id': '123', 'name': 'test'})

# S3
s3 = boto3.client('s3')
s3.put_object(Bucket='my-bucket', Key='test.txt', Body='Hello')

# SQS
sqs = boto3.client('sqs')
sqs.send_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/123456789/my-queue', MessageBody='test')
```

### Step Functions Integration

```python
import boto3
import json

sfn = boto3.client('stepfunctions')

# Start execution
response = sfn.start_execution(
    stateMachineArn='arn:aws:states:us-east-1:123456789:stateMachine:my-machine',
    input=json.dumps({'order_id': '123', 'amount': 100})
)
print(f"Execution ARN: {response['executionArn']}")
```

### EventBridge Integration

```python
import boto3
import json

events = boto3.client('events')

# Put event
events.put_entries(
    Entries=[
        {
            'Source': 'my.app',
            'DetailType': 'OrderCreated',
            'Detail': json.dumps({'order_id': '123', 'amount': 100}),
            'EventBusName': 'default',
        }
    ]
)
```

## Performance Optimization

### Cold Start Optimization

| Technique | Description | Impact |
|-----------|-------------|--------|
| Provisioned Concurrency | Keep instances warm | Eliminates cold starts |
| Smaller packages | Reduce deployment size | 10-50% faster |
| Lazy loading | Defer initialization | 20-40% faster |
| Connection pooling | Reuse connections | 30-50% faster |
| ARM64/Graviton | Better price/performance | 20% faster, 20% cheaper |

### Memory Optimization

```
Memory-CPU Relationship (AWS Lambda):
├── 128 MB — 0.08 vCPU
├── 256 MB — 0.17 vCPU
├── 512 MB — 0.33 vCPU
├── 1024 MB — 0.58 vCPU
├── 2048 MB — 1.0 vCPU
└── 4096 MB — 2.0 vCPU

Recommendation: Start at 256MB, increase if CPU-bound
```

### Cost Optimization

```
Cost Optimization Strategies:
├── Right-size memory (price varies linearly)
├── Use ARM64 (20% cheaper)
├── Minimize execution time
├── Use S3 Select instead of Lambda
├── Use DynamoDB Accelerator (DAX) for caching
└── Use API Gateway caching
```

## Security Considerations

### Serverless Security

| Control | Description | Implementation |
|---------|-------------|----------------|
| Least Privilege | Minimal IAM roles | IAM policies |
| VPC | Isolate functions | VPC configuration |
| Encryption | Data protection | KMS, TLS |
| WAF | Web application firewall | AWS WAF |
| Secrets | Secure credentials | Secrets Manager |
| Logging | Audit trail | CloudWatch Logs |

### IAM Best Practices

```python
# Minimal IAM role
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/my-table"
        }
    ]
}
```

### Secret Management

```python
import boto3
import json

secrets = boto3.client('secretsmanager')
secret = secrets.get_secret_value(SecretId='my-secret')
credentials = json.loads(secret['SecretString'])
```

## Troubleshooting Guide

### Common Serverless Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Cold Start | Slow initial response | Provisioned concurrency |
| Timeout | Function timeout | Increase timeout, optimize code |
| Memory Error | Out of memory | Increase memory allocation |
| Permission Error | Access denied | Check IAM role |
| Throttling | Too many requests | Increase concurrency limit |

### Debugging Lambda

```python
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    logger.info(f"Function: {context.function_name}")
    logger.info(f"Memory: {context.memory_limit_in_mb}MB")
    logger.info(f"Timeout: {context.get_remaining_time_in_milliseconds()}ms remaining")
```

### CloudWatch Insights

```
# Find errors
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20

# Find slow invocations
fields @timestamp, @duration
| filter @duration > 5000
| sort @duration desc
| limit 20
```

## API Reference

### Lambda Function

```python
def handler(event, context):
    """Lambda handler function."""
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello'}),
    }
```

### DynamoDB Operations

```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('my-table')

# Put item
table.put_item(Item={'id': '123', 'name': 'test'})

# Get item
response = table.get_item(Key={'id': '123'})
item = response.get('Item')

# Query
response = table.query(
    KeyConditionExpression=Key('id').eq('123')
)
items = response['Items']
```

## Data Models

### Lambda Context

```
LambdaContext:
  function_name: str
  function_version: str
  invoked_function_arn: str
  memory_limit_in_mb: int
  aws_request_id: str
  log_group_name: str
  log_stream_name: str
  remaining_time_ms: int
  identity: dict
  client_context: dict
```

### API Gateway Event

```
APIGatewayEvent:
  http_method: str
  path: str
  headers: dict
  query_string_parameters: dict
  path_parameters: dict
  body: str
  is_base64_encoded: bool
  request_context: dict
  resource: str
  stage_variables: dict
```

## Deployment Guide

### Serverless Deployment

```
1. Prerequisites
   ├── AWS CLI configured
   ├── Serverless Framework installed
   ├── Node.js installed
   └── IAM permissions

2. Deployment Steps
   ├── Install dependencies
   ├── Package functions
   ├── Deploy to AWS
   ├── Verify deployment
   └── Set up monitoring

3. Post-Deployment
   ├── Test endpoints
   ├── Configure alerts
   ├── Set up logging
   └── Document APIs
```

### CI/CD Pipeline

```yaml
# buildspec.yml
version: 0.2
phases:
  install:
    runtime-versions:
      nodejs: 18
  pre_build:
    commands:
      - npm install
      - npm test
  build:
    commands:
      - npx serverless package
  post_build:
    commands:
      - npx serverless deploy --stage production
```

## Monitoring & Observability

### Key Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Duration | <5s | Function execution time |
| Errors | <0.1% | Error rate |
| Throttles | 0 | Throttled requests |
| Concurrent Executions | <100 | Concurrent instances |
| Invocations | Monitor | Request volume |
| Duration P99 | <10s | Tail latency |

### CloudWatch Dashboard

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Create dashboard
cloudwatch.put_dashboard(
    DashboardName='MyServerlessApp',
    DashboardBody=json.dumps({
        'widgets': [
            {
                'type': 'metric',
                'properties': {
                    'metrics': [
                        ['AWS/Lambda', 'Duration', 'FunctionName', 'my-function'],
                    ],
                    'period': 300,
                    'stat': 'Average',
                    'region': 'us-east-1',
                },
            }
        ]
    })
)
```

## Testing Strategy

### Serverless Testing

```
1. Unit Tests
   ├── Handler logic
   ├── Data transformations
   └── Business logic

2. Integration Tests
   ├── Lambda + DynamoDB
   ├── API Gateway + Lambda
   └── Step Functions workflows

3. Load Tests
   ├── Artillery (load testing)
   ├── AWS Load Testing Service
   └── Locust (distributed)

4. Contract Tests
   ├── API schema validation
   ├── Event schema validation
   └── Service contracts
```

## Versioning & Migration

### Serverless Versioning

```
Major: Architecture change
├── Example: Monolith → Serverless
├── Requires: Full testing, rollback plan
└── Risk: High

Minor: New functions/endpoints
├── Example: Add new API endpoint
├── Requires: API documentation
└── Risk: Low

Patch: Bug fixes
├── Example: Fix validation logic
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| BaaS | Backend as a Service |
| Cold Start | Initial invocation latency |
| Edge Function | Code running at CDN edge |
| FaaS | Function as a Service |
| Provisioned Concurrency | Pre-warmed Lambda instances |
| Serverless | No server management required |
| Step Functions | Serverless workflow orchestration |
| Throttling | Request limiting |
| Warm Start | Subsequent invocation |
| Zero Scaling | Scale to zero when idle |

## Changelog

### 2.0.0 (2024-12-01)
- Added event-driven patterns
- Added saga pattern
- Improved cold start optimization
- Added security hardening

### 1.2.0 (2024-08-15)
- Added Step Functions
- Added EventBridge integration
- Improved monitoring

### 1.1.0 (2024-05-20)
- Added API Gateway patterns
- Added DynamoDB patterns
- Improved documentation

### 1.0.0 (2024-02-01)
- Initial release with basic Lambda
- Simple API patterns
- Basic DynamoDB integration

## Contributing Guidelines

### Adding New Patterns

1. Document the pattern
2. Include working code examples
3. Provide deployment instructions
4. Add monitoring guidance
5. Submit PR with review

## License

MIT License

Copyright (c) 2024 Serverless Contributors

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
