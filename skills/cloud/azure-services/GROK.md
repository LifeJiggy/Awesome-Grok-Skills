---
name: "azure-services"
category: "cloud"
version: "2.0.0"
tags: ["cloud", "Azure", "architecture", "services", "enterprise"]
---

# Azure Services

## Overview

The Azure Services module provides comprehensive guidance for designing and managing Microsoft Azure cloud architectures. It covers Azure compute, networking, storage, databases, AI/ML services, and enterprise integration patterns. The module follows the Azure Well-Architected Framework and cloud adoption framework for enterprise deployments.

This skill is essential for Azure architects, cloud engineers, and enterprise teams building workloads on Microsoft Azure.

## Core Capabilities

- **Compute**: Virtual Machines, Azure Functions, AKS, Container Apps, and App Service selection and optimization
- **Networking**: VNet design, Azure Front Door, ExpressRoute, Private Link, and hybrid connectivity
- **Storage**: Blob Storage tiers, Managed Disks, Azure Files, and data lake architecture
- **Databases**: Azure SQL, Cosmos DB, PostgreSQL, and database service selection
- **Identity**: Azure AD/Entra ID, Managed Identity, Conditional Access, and zero-trust patterns
- **Security**: Microsoft Defender for Cloud, Key Vault, Sentinel, and security posture management
- **DevOps**: Azure DevOps, GitHub Actions, ARM/Bicep templates, and CI/CD pipelines
- **Cost Management**: Azure Cost Management, reservations, savings plans, and optimization

## Usage Examples

```python
from azure_services import (
    AzureWellArchitected,
    ComputeSelector,
    NetworkDesigner,
    SecurityReviewer,
    CostOptimizer,
)

# --- Well-Architected Review ---
review = AzureWellArchitected(workload="e-commerce-api")
review.assess(
    pillar="reliability",
    findings=["Single region deployment", "No health probes configured"],
    severity="high",
)

# --- Compute Selection ---
selector = ComputeSelector()
rec = selector.recommend(
    workload="web-api",
    requests_per_sec=500,
    memory_mb=1024,
    gpu_required=False,
)
print(f"Service: {rec.service}, Tier: {rec.tier}")

# --- VNet Design ---
designer = NetworkDesigner()
vnet = designer.design_vnet(
    name="production-vnet",
    address_space="10.0.0.0/16",
    subnets=[
        {"name": "web", "cidr": "10.0.1.0/24"},
        {"name": "app", "cidr": "10.0.2.0/24"},
        {"name": "data", "cidr": "10.0.3.0/24"},
    ],
    peerings=[{"vnet": "hub-vnet", "allow_forwarded": True}],
)
print(f"VNet: {vnet.name}, Subnets: {len(vnet.subnets)}")

# --- Security Review ---
security = SecurityReviewer()
findings = security.review_subscription(subscription_id="sub-001")
for f in findings:
    print(f"  [{f.severity}] {f.finding}")
```

## Best Practices

- Use Azure Entra ID (AAD) for all identity management — avoid local accounts
- Implement Private Endpoints for all PaaS services to avoid public exposure
- Use Azure Policy for governance guardrails at scale
- Enable Microsoft Defender for Cloud across all subscriptions
- Use Bicep templates for infrastructure-as-code — preferred over ARM JSON
- Implement hub-spoke network topology for enterprise environments
- Use Azure Front Door for global load balancing and WAF protection
- Enable diagnostic logging for all services and centralize in Log Analytics
- Use Azure Cost Management with budgets and alerts for spend governance
- Apply Azure Blueprints for consistent environment provisioning

## Related Modules

- **aws-architecture**: AWS cloud architecture patterns
- **gcp-platform**: GCP cloud architecture patterns
- **multi-cloud**: Cross-cloud strategies and portability
- **serverless**: Serverless-first patterns on Azure

## Advanced Configuration

### Azure CLI Configuration

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "subscription-id"

# Set default resource group
az configure --defaults group=myResourceGroup location=eastus
```

### Bicep Configuration

```bicep
// main.bicep
param location string = resourceGroup().location
param environment string = 'production'

module vnet './modules/vnet.bicep' = {
  name: 'vnet-deployment'
  params: {
    location: location
    environment: environment
  }
}
```

### Azure Policy Configuration

```json
{
  "properties": {
    "displayName": "Require HTTPS for web apps",
    "policyType": "Custom",
    "mode": "All",
    "parameters": {},
    "policyRule": {
      "if": {
        "allOf": [
          {
            "field": "type",
            "equals": "Microsoft.Web/sites"
          },
          {
            "field": "Microsoft.Web/sites/httpsOnly",
            "equals": "false"
          }
        ]
      },
      "then": {
        "effect": "modify"
      }
    }
  }
}
```

## Architecture Patterns

### Hub-Spoke Network Architecture

```
Hub VNet:
├── Azure Firewall
├── VPN Gateway
├── ExpressRoute Gateway
├── Azure Bastion
└── Shared Services (DNS, AD)

Spoke VNets:
├── Production
│   ├── Web Tier
│   ├── App Tier
│   └── Data Tier
├── Staging
│   ├── Web Tier
│   ├── App Tier
└── Data Tier

Connectivity:
├── VNet Peering (Hub ↔ Spokes)
├── Azure Firewall (Centralized routing)
└── Private Endpoints (PaaS services)
```

### Microservices Architecture

```
Microservices Stack:
├── API Gateway (Azure API Management)
├── Service Mesh (Istio on AKS)
├── Services
│   ├── Order Service (AKS)
│   ├── Payment Service (Functions)
│   ├── Inventory Service (AKS)
│   └── Notification Service (Logic Apps)
├── Data
│   ├── Cosmos DB (Order data)
│   ├── SQL Database (Payment data)
│   └── Redis Cache (Session)
└── Observability
    ├── Application Insights
    ├── Azure Monitor
    └── Log Analytics
```

### Data Platform Architecture

```
Data Platform Layers:
├── Ingestion
│   ├── Event Hubs (streaming)
│   ├── Data Factory (batch)
│   └── IoT Hub (IoT data)
├── Processing
│   ├── Databricks (Spark)
│   ├── Synapse Analytics
│   └── Stream Analytics
├── Storage
│   ├── Data Lake Storage Gen2
│   ├── Blob Storage
│   └── Cosmos DB
├── Analytics
│   ├── Power BI
│   ├── Synapse Serverless
│   └── Azure Analysis Services
└── Governance
    ├── Purview (data catalog)
    ├── Azure Policy
    └── Key Vault (secrets)
```

## Integration Guide

### Azure SDK Integration

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential,
)

# Upload blob
blob_client = blob_service.get_blob_client(container="mycontainer", blob="myblob")
with open("local-file.txt", "rb") as data:
    blob_client.upload_blob(data)
```

### Azure DevOps Integration

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.11'
    - script: pip install -r requirements.txt
    - script: python -m pytest tests/
    - task: PublishBuildArtifacts@1
```

### Terraform Azure Provider

```hcl
# main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "myResourceGroup"
  location = "East US"
}
```

## Performance Optimization

### Compute Optimization

| Service | Use Case | Scaling | Cost |
|---------|----------|---------|------|
| App Service | Web apps | Auto-scale | Medium |
| Azure Functions | Event-driven | Auto-scale | Low |
| AKS | Containers | Manual/auto | High |
| Container Apps | Microservices | Auto-scale | Medium |
| VM Scale Sets | Custom apps | Auto-scale | Variable |

### Storage Optimization

```
Blob Storage Tiers:
├── Hot — Frequent access
├── Cool — Infrequent access (30d min)
├── Cold — Rare access (90d min)
└── Archive — Offline (180d min)

Managed Disk Types:
├── Ultra SSD — Highest performance
├── Premium SSD v2 — High performance
├── Premium SSD — Production workloads
├── Standard SSD — Web servers, dev/test
└── Standard HDD — Backup, infrequent
```

### Network Optimization

```
Optimization Techniques:
├── Azure Front Door (global CDN)
├── Azure Caching for Redis
├── Accelerated Networking
├── Private Link (avoid public internet)
└── ExpressRoute (dedicated connectivity)
```

## Security Considerations

### Azure Security Best Practices

| Practice | Implementation | Priority |
|----------|---------------|----------|
| Azure AD/Entra ID | All identity management | Critical |
| Conditional Access | Context-aware policies | Critical |
| Managed Identity | No credentials in code | Critical |
| Key Vault | Secrets management | Critical |
| Defender for Cloud | Security posture | High |
| Sentinel | SIEM/SOAR | High |

### Identity Security

```
Azure AD Security:
├── Multi-Factor Authentication (MFA)
├── Conditional Access Policies
├── Privileged Identity Management (PIM)
├── Identity Protection
├── Password Protection
└── Self-service Password Reset
```

### Network Security

```
Network Security Layers:
├── Azure Firewall (network filtering)
├── DDoS Protection (volumetric attacks)
├── Network Security Groups (subnet filtering)
├── Application Gateway + WAF (application protection)
├── Private Endpoints (service access)
└── Just-in-Time VM Access (management)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Deployment Failure | ARM/Bicep error | Check permissions, template syntax |
| Connectivity Issues | Cannot reach service | Check NSGs, Private Endpoints |
| Performance | Slow response times | Check scale, caching, CDN |
| Cost Overrun | High bill | Check usage, reservations |
| Authentication | 401/403 errors | Check Azure AD config |

### Debugging Commands

```bash
# Check resource group
az resource list --resource-group myResourceGroup

# Check VM status
az vm get-instance-view --name myVM --resource-group myResourceGroup

# Check network configuration
az network vnet list --resource-group myResourceGroup
az network nsg rule list --nsg-name myNSG --resource-group myResourceGroup

# Check Activity Log
az monitor activity-log list --resource-group myResourceGroup --max-events 10
```

## API Reference

### Azure SDK Examples

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

# Resource Management
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)

# List resources
for resource in resource_client.resources.list_by_resource_group("myResourceGroup"):
    print(f"{resource.type}: {resource.name}")

# Compute Management
compute_client = ComputeManagementClient(credential, subscription_id)

# List VMs
for vm in compute_client.virtual_machines.list():
    print(f"VM: {vm.name}, Status: {vm.provisioning_state}")
```

## Data Models

### Azure Resource

```
AzureResource:
  id: str                    # Resource ID
  name: str                  # Resource name
  type: str                  # Resource type
  location: str              # Region
  resource_group: str        # Resource group
  tags: dict                 # Tags
  provisioning_state: str    # Current state
```

### Azure Function

```
AzureFunction:
  name: str
  runtime: str               # dotnet, node, python, etc.
  entry_point: str
  bindings: list[Binding]
  app_settings: dict
  timeout_seconds: int
  memory_mb: int
```

### App Service Plan

```
AppServicePlan:
  name: str
  tier: str                  # Free, Basic, Standard, Premium
  size: str                  # B1, S1, P1v2, etc.
  capacity: int              # Instance count
  os_type: str               # Windows, Linux
  max_instances: int
```

## Deployment Guide

### Azure Deployment Steps

```
1. Prerequisites
   ├── Azure subscription
   ├── Azure CLI installed
   ├── Contributor role
   └── Resource group created

2. Deployment
   ├── Validate templates (What-If)
   ├── Deploy infrastructure
   ├── Configure networking
   ├── Set up monitoring
   └── Enable security

3. Post-Deployment
   ├── Verify resources
   ├── Configure alerts
   ├── Set up backup
   └── Document configuration
```

### CI/CD Pipeline

```yaml
# .github/workflows/azure-deploy.yml
name: Deploy to Azure
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - uses: azure/arm-deploy@v1
        with:
          resourceGroupName: myResourceGroup
          template: azuredeploy.json
          parameters: azuredeploy.parameters.json
```

## Monitoring & Observability

### Key Metrics

| Metric | Service | Target |
|--------|---------|--------|
| Response Time | App Service | <500ms P95 |
| CPU Usage | VMs/App Service | <70% |
| Memory Usage | VMs/App Service | <80% |
| Error Rate | All services | <0.1% |
| Availability | All services | >99.9% |
| Cost | All resources | Within budget |

### Azure Monitor Configuration

```python
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

# Query logs
response = client.query_workspace(
    workspace_id="workspace-id",
    query="AppRequests | summarize avg(DurationMs) by bin(TimeGenerated, 5m)",
    timespan="PT1H",
)
```

## Testing Strategy

### Testing Approach

```
1. Unit Tests
   ├── Function logic
   ├── API handlers
   └── Data transformations

2. Integration Tests
   ├── Azure service integration
   ├── End-to-end workflows
   └── Authentication flows

3. Load Tests
   ├── Azure Load Testing
   ├── Stress testing
   └── Endurance testing

4. Security Tests
   ├── Penetration testing
   ├── Azure Security Center
   └── Conditional Access testing
```

## Versioning & Migration

### Azure Versioning

```
Major: Service migration
├── Example: VM → Container Apps
├── Requires: Full testing, rollback plan
└── Risk: High

Minor: Service additions
├── Example: Add Redis Cache
├── Requires: Testing, documentation
└── Risk: Low

Patch: Configuration changes
├── Example: Update VM size
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| AKS | Azure Kubernetes Service |
| Azure AD | Azure Active Directory (now Entra ID) |
| Bicep | Domain-specific language for Azure deployment |
| ExpressRoute | Dedicated private connection to Azure |
| Key Vault | Secrets and key management service |
| NSG | Network Security Group |
| PIM | Privileged Identity Management |
| RBAC | Role-Based Access Control |
| Sentinel | Cloud-native SIEM/SOAR |
| VNet | Virtual Network |

## Changelog

### 2.0.0 (2024-12-01)
- Added Bicep templates
- Added Container Apps patterns
- Improved security hardening
- Added Azure Purview integration

### 1.2.0 (2024-08-15)
- Added AKS patterns
- Added data platform architecture
- Improved networking

### 1.1.0 (2024-05-20)
- Added serverless patterns
- Added microservices architecture
- Improved monitoring

### 1.0.0 (2024-02-01)
- Initial release with basic compute patterns
- Simple networking guidance
- Basic security

## Contributing Guidelines

### Adding New Patterns

1. Document the pattern
2. Include Bicep/ARM templates
3. Provide working code examples
4. Add cost estimates
5. Submit PR with review

### Code Quality

- All examples must be deployable
- Include RBAC permissions
- Document costs
- Test in multiple regions

## Azure AI/ML Services Integration Patterns

### Azure Cognitive Services Integration

```python
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.translation import TextTranslationClient
from azure.ai.vision.imageanalysis import ImageAnalysisClient

credential = DefaultAzureCredential()

# Text Analytics - Sentiment Analysis
text_client = TextAnalyticsClient(
    endpoint="https://mytext.cognitiveservices.azure.com/",
    credential=credential,
)
documents = ["I love this product!", "This is terrible service."]
result = text_client.analyze_sentiment(documents=documents)
for doc in result:
    print(f"Sentiment: {doc.sentiment}, Scores: {doc.confidence_scores}")

# Computer Vision - Image Analysis
vision_client = ImageAnalysisClient(
    endpoint="https://myvision.cognitiveservices.azure.com/",
    credential=credential,
)
with open("image.jpg", "rb") as f:
    result = vision_client.analyze(
        image=f,
        features=["caption", "tags", "objects"],
    )
print(f"Caption: {result.caption.text}")
for tag in result.tags:
    print(f"Tag: {tag.name}, Confidence: {tag.confidence}")
```

### Azure Machine Learning Pipeline

```python
from azure.ai.ml import MLClient
from azure.ai.ml import dsl, Input, Output
from azure.ai.ml.entities import (
    Model,
    Environment,
    CommandComponent,
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
)

# Connect to ML workspace
ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="subscription-id",
    resource_group_name="myResourceGroup",
    workspace_name="myMLWorkspace",
)

# Define training pipeline
@dsl.pipeline(
    default_compute="cpu-cluster",
    default_datastore="workspaceblobstore",
)
def training_pipeline(raw_data: Input):
    preprocess = command_component(
        name="preprocess",
        display_name="Data Preprocessing",
        command="python preprocess.py --input ${{inputs.raw_data}} --output ${{outputs.preprocessed}}",
        environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu:1",
        inputs={"raw_data": Input(type="uri_folder")},
        outputs={"preprocessed": Output(type="uri_folder")},
    )
    train = command_component(
        name="train",
        display_name="Model Training",
        command="python train.py --data ${{inputs.preprocessed}} --model ${{outputs.model}}",
        environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu:1",
        inputs={"preprocessed": Input(type="uri_folder")},
        outputs={"model": Output(type="uri_model")},
    )
    preprocess_step = preprocess(raw_data=raw_data)
    train_step = train(preprocessed=preprocess_step.outputs.preprocessed)
    return {"model": train_step.outputs.model}

# Submit pipeline
pipeline = training_pipeline(raw_data=Input(path="azureml:raw-data:1"))
pipeline_job = ml_client.jobs.create_or_update(pipeline)
ml_client.jobs.stream(pipeline_job.name)
```

### Azure OpenAI Service Integration

```python
from azure.identity import DefaultAzureCredential
from azure.ai.openai import OpenAIClient
from openai import AzureOpenAI

# Azure OpenAI Client
client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2024-02-01",
    azure_endpoint="https://myopenai.openai.azure.com/",
)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Azure Functions"},
    ],
    max_tokens=500,
    temperature=0.7,
)
print(response.choices[0].message.content)

# Embeddings
embedding_client = OpenAIClient(
    credential=DefaultAzureCredential(),
    endpoint="https://myopenai.openai.azure.com/",
)
embedding = embedding_client.embeddings.create(
    model="text-embedding-ada-002",
    input="Azure cloud architecture",
)
print(f"Embedding dimensions: {len(embedding.data[0].embedding)}")
```

## Azure Cost Management Optimization

### Cost Analysis and Budgeting

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.consumption import ConsumptionManagementClient

credential = DefaultAzureCredential()
cost_client = CostManagementClient(credential)

# Query cost data
query = {
    "type": "ActualCost",
    "timeframe": "MonthToDate",
    "dataset": {
        "granularity": "Daily",
        "aggregation": {
            "totalCost": {
                "name": "PreTaxCost",
                "function": "Sum",
            }
        },
        "grouping": [
            {"type": "Dimension", "name": "ResourceGroup"},
        ],
    },
}

result = cost_client.query.usage(
    scope="/subscriptions/sub-001",
    parameters=query,
)
for row in result.rows:
    print(f"Date: {row[1]}, Resource Group: {row[2]}, Cost: ${row[0]:.2f}")

# Set budget alerts
consumption_client = ConsumptionManagementClient(credential)
budget = consumption_client.budgets.create_or_update(
    scope="/subscriptions/sub-001",
    budget_name="monthly-budget",
    parameters={
        "category": "Cost",
        "amount": 10000.0,
        "timeGrain": "Monthly",
        "timePeriod": {
            "startDate": "2024-01-01",
            "endDate": "2024-12-31",
        },
        "notifications": {
            "80": {
                "enabled": True,
                "operator": "GreaterThan",
                "threshold": 80,
                "contactEmails": ["admin@company.com"],
            },
        },
    },
)
```

### Cost Optimization Strategies

```python
# Azure Advisor Recommendations API
from azure.identity import DefaultAzureCredential
from azure.mgmt.advisor import AdvisorManagementClient

credential = DefaultAzureCredential()
advisor_client = AdvisorManagementClient(credential, subscription_id)

# Get cost recommendations
recommendations = advisor_client.recommendations.list(
    filter="category eq 'Cost'"
)
for rec in recommendations:
    print(f"Impact: {rec.impact}, Category: {rec.category}")
    print(f"Description: {rec.short_description.problem}")
    print(f"Remediation: {rec.extended_properties.remediation}")
    print("---")
```

### Reserved Instance Recommendations

```python
# Analyze usage patterns for reserved instances
from azure.identity import DefaultAzureCredential
from azure.mgmt.consumption import ConsumptionManagementClient

credential = DefaultAzureCredential()
consumption_client = ConsumptionManagementClient(credential)

# Get reserved instance recommendations
recommendations = consumption_client.reserved_instances_recommendations.list(
    scope="/subscriptions/sub-001",
    filter="properties.lookBackPeriod eq 'Last30Days' "
           "and properties.term eq 'P1Y'",
)
for rec in recommendations:
    print(f"SKU: {rec.sku_name}")
    print(f"Current On-Demand Cost: ${rec.current_on_demand_cost:.2f}")
    print(f"Recommended RI Cost: ${rec.total_ri_cost:.2f}")
    print(f"Savings: ${rec.savings:.2f} ({rec.savings_percentage:.1f}%)")
    print(f"Recommended Quantity: {rec.recommended_quantity}")
    print("---")
```

## Azure Functions Event-Driven Architecture

### Timer Trigger Function (Python)

```python
# function_app.py
import azure.functions as func
import logging
import json
from datetime import datetime

app = func.FunctionApp()

@app.timer_trigger(
    schedule="0 0 8 * * *",  # 8 AM daily
    arg_name="myTimer",
    run_on_startup=False,
)
def daily_report(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.warning("Timer is past due!")

    logging.info("Daily report function started at %s", datetime.utcnow())
    
    # Generate daily metrics
    metrics = {
        "date": datetime.utcnow().isoformat(),
        "total_requests": 15420,
        "error_rate": 0.02,
        "avg_response_time_ms": 245,
    }
    
    # Store in Cosmos DB
    logging.info("Generated metrics: %s", json.dumps(metrics))
```

### Queue Trigger Function (Python)

```python
import azure.functions as func
import json
import logging

app = func.FunctionApp()

@app.queue_trigger(
    arg_name="msg",
    queue_name="order-queue",
    connection="AzureWebJobsStorage",
)
def process_order(msg: func.QueueMessage) -> None:
    order_data = json.loads(msg.get_body().decode("utf-8"))
    
    logging.info("Processing order: %s", order_data["order_id"])
    
    # Validate order
    if not order_data.get("items"):
        logging.warning("Order %s has no items", order_data["order_id"])
        return
    
    # Process payment
    payment_result = process_payment(order_data["payment_info"])
    
    # Update inventory
    for item in order_data["items"]:
        update_inventory(item["sku"], item["quantity"])
    
    # Send confirmation email
    send_confirmation_email(order_data["customer_email"], order_data["order_id"])
    
    logging.info("Order %s processed successfully", order_data["order_id"])

def process_payment(payment_info: dict) -> dict:
    # Payment processing logic
    return {"status": "success", "transaction_id": "txn-123"}

def update_inventory(sku: str, quantity: int) -> None:
    # Inventory update logic
    pass

def send_confirmation_email(email: str, order_id: str) -> None:
    # Email sending logic
    pass
```

### Cosmos DB Trigger Function (Python)

```python
import azure.functions as func
import json
import logging
from azure.cosmos import CosmosClient

app = func.FunctionApp()

@app.cosmos_db_trigger(
    arg_name="documents",
    database_name="orders-db",
    collection_name="orders",
    connection_string_setting="CosmosDBConnection",
)
def process_new_order(documents: func.DocumentList) -> None:
    for doc in documents:
        order = dict(doc)
        
        logging.info("New order detected: %s", order["id"])
        
        # Validate order
        if validate_order(order):
            # Trigger fulfillment workflow
            trigger_fulfillment(order)
            
            # Update analytics
            update_order_analytics(order)
        else:
            logging.warning("Invalid order: %s", order["id"])

def validate_order(order: dict) -> bool:
    required_fields = ["id", "items", "total", "customer_id"]
    return all(field in order for field in required_fields)

def trigger_fulfillment(order: dict) -> None:
    # Fulfillment logic
    pass

def update_order_analytics(order: dict) -> None:
    # Analytics update logic
    pass
```

### Event Grid Trigger Function (Python)

```python
import azure.functions as func
import json
import logging

app = func.FunctionApp()

@app.event_grid_trigger(arg_name="event")
def handle_blob_created(event: func.EventGridEvent) -> None:
    event_data = event.get_json()
    
    logging.info("Blob created event received")
    logging.info("Blob URL: %s", event_data["data"]["url"])
    logging.info("Blob size: %s bytes", event_data["data"]["contentLength"])
    
    # Process uploaded file
    blob_url = event_data["data"]["url"]
    blob_name = event_data["data"]["blobName"]
    
    if blob_name.endswith(".csv"):
        process_csv_file(blob_url)
    elif blob_name.endswith(".json"):
        process_json_file(blob_url)
    else:
        logging.info("Unsupported file type: %s", blob_name)

def process_csv_file(url: str) -> None:
    # CSV processing logic
    pass

def process_json_file(url: str) -> None:
    # JSON processing logic
    pass
```

### Service Bus Trigger Function (Python)

```python
import azure.functions as func
import json
import logging
from datetime import datetime

app = func.FunctionApp()

@app.service_bus_queue_trigger(
    arg_name="message",
    queue_name="notification-queue",
    connection="ServiceBusConnection",
)
def send_notification(message: func.ServiceBusMessage) -> None:
    notification = json.loads(message.get_body().decode("utf-8"))
    
    logging.info("Processing notification: %s", notification["id"])
    
    # Route based on notification type
    notification_type = notification.get("type")
    
    if notification_type == "email":
        send_email_notification(notification)
    elif notification_type == "sms":
        send_sms_notification(notification)
    elif notification_type == "push":
        send_push_notification(notification)
    else:
        logging.warning("Unknown notification type: %s", notification_type)

def send_email_notification(notification: dict) -> None:
    # Email sending logic
    pass

def send_sms_notification(notification: dict) -> None:
    # SMS sending logic
    pass

def send_push_notification(notification: dict) -> None:
    # Push notification logic
    pass
```

### HTTP Trigger with Durable Functions (Python)

```python
import azure.functions as func
import json
import logging
from azure.durable_functions import (
    DurableOrchestrationContext,
    DurableOrchestrationClient,
)

app = func.FunctionApp()

@app.route(route="orchestrators/{functionName}")
@app.durable_client_input(name="client")
async def http_start(
    req: func.HttpRequest,
    client: DurableOrchestrationClient,
) -> func.HttpResponse:
    function_name = req.route_params.get("functionName")
    instance_id = await client.start_new(function_name)
    logging.info("Started orchestration with ID: %s", instance_id)
    
    return client.create_check_status_response(req, instance_id)

@app.orchestration_trigger(context_name="context")
def order_processing_orchestrator(context: DurableOrchestrationContext):
    order = context.get_input()
    
    # Step 1: Validate order
    validation_result = yield context.call_activity(
        "validate_order", order
    )
    if not validation_result["valid"]:
        return {"status": "failed", "reason": validation_result["reason"]}
    
    # Step 2: Process payment
    payment_result = yield context.call_activity(
        "process_payment", order["payment_info"]
    )
    
    # Step 3: Update inventory (parallel)
    inventory_tasks = [
        context.call_activity("update_inventory", item)
        for item in order["items"]
    ]
    inventory_results = yield context.task_all(inventory_tasks)
    
    # Step 4: Send confirmation
    yield context.call_activity("send_confirmation", order)
    
    return {
        "status": "completed",
        "order_id": order["id"],
        "payment_id": payment_result["transaction_id"],
    }

@app.activity_trigger(input_name="order")
def validate_order(order: dict) -> dict:
    # Validation logic
    return {"valid": True, "reason": None}

@app.activity_trigger(input_name="payment_info")
def process_payment(payment_info: dict) -> dict:
    # Payment processing logic
    return {"transaction_id": "txn-123", "status": "success"}

@app.activity_trigger(input_name="item")
def update_inventory(item: dict) -> dict:
    # Inventory update logic
    return {"sku": item["sku"], "updated": True}

@app.activity_trigger(input_name="order")
def send_confirmation(order: dict) -> None:
    # Confirmation sending logic
    pass
```

### Event-Driven Architecture Patterns

```
Event-Driven Patterns on Azure Functions:
├── Fan-out/Fan-in
│   ├── Parallel processing
│   ├── Aggregation
│   └── Timeout handling
├── Async HTTP APIs
│   ├── Long-running operations
│   ├── Status polling
│   └── Webhook callbacks
├── Monitor Pattern
│   ├── Event monitoring
│   ├── Alerting
│   └── Auto-remediation
├── Human Interaction
│   ├── Approval workflows
│   ├── Escalation
│   └── Time-out handling
└── Chaining
    ├── Sequential processing
    ├── Error handling
    └── Retry policies
```

### Durable Functions Entity Pattern (Python)

```python
import azure.functions as func
import json
import logging
from azure.durable_functions import DurableEntityContext

app = func.FunctionApp()

@app.entity_trigger(context_name="context")
def counter_entity(context: DurableEntityContext) -> None:
    current_value = context.get_state(lambda: 0)
    operation = context.get_input()
    
    if operation["action"] == "increment":
        current_value += operation.get("amount", 1)
    elif operation["action"] == "decrement":
        current_value -= operation.get("amount", 1)
    elif operation["action"] == "reset":
        current_value = 0
    
    context.set_state(current_value)
    context.set_result(current_value)

# HTTP trigger to interact with entity
@app.route(route="counter/{entityKey}")
@app.durable_client_input(name="client")
async def counter_http(
    req: func.HttpRequest,
    client: DurableOrchestrationClient,
) -> func.HttpResponse:
    entity_key = req.route_params["entityKey"]
    entity_id = ("counter", entity_key)
    
    if req.method == "GET":
        state = await client.read_entity_state(entity_id)
        return func.HttpResponse(
            json.dumps({"value": state.state if state.exists else 0}),
            mimetype="application/json",
        )
    elif req.method == "POST":
        body = req.get_json()
        await client.signal_entity(entity_id, body)
        return func.HttpResponse(
            json.dumps({"status": "signaled"}),
            mimetype="application/json",
        )
    else:
        return func.HttpResponse("Method not allowed", status_code=405)
```

## License

MIT License

Copyright (c) 2024 Azure Services Contributors

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
