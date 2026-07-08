# Cloud Migration Agent

> End-to-end cloud migration — assess workloads, plan waves, execute, validate, and optimize costs.

---

## Table of Contents

1. [Overview](#overview)
   - [What It Does](#what-it-does)
   - [Architecture](#architecture)
   - [Key Concepts](#key-concepts)
2. [Prerequisites](#prerequisites)
3. [Features](#features)
4. [Cloud Provider Support](#cloud-provider-support)
5. [Quick Start](#quick-start)
   - [Installation](#installation)
   - [Basic Setup](#basic-setup)
   - [First Migration](#first-migration)
6. [Usage](#usage)
   - [Complete Migration Workflow](#complete-migration-workflow)
   - [Workload Assessment](#workload-assessment)
   - [Wave Planning](#wave-planning)
   - [Migration Execution](#migration-execution)
   - [Post-Migration Validation](#post-migration-validation)
   - [Cost Optimization](#cost-optimization)
7. [API Reference](#api-reference)
   - [CloudMigrationAgent Methods](#cloudmigrationagent-methods)
   - [Data Models](#data-models)
   - [Enums](#enums)
   - [Configuration](#configuration-1)
8. [Data Model](#data-model)
   - [Server Model](#server-model)
   - [Application Model](#application-model)
   - [Dependency Model](#dependency-model)
   - [Assessment Model](#assessment-model)
   - [Migration Plan Model](#migration-plan-model)
   - [Wave Model](#wave-model)
   - [Validation Model](#validation-model)
   - [Cost Model](#cost-model)
9. [Examples](#examples)
   - [Strategy Selection Logic](#strategy-selection-logic)
   - [Multi-Cloud Migration](#multi-cloud-migration)
   - [Dependency-Aware Planning](#dependency-aware-planning)
   - [Compliance-Driven Migration](#compliance-driven-migration)
   - [Cost Optimization Analysis](#cost-optimization-analysis)
   - [Automated Validation Pipeline](#automated-validation-pipeline)
   - [Rollback and Recovery](#rollback-and-recovery)
   - [Custom Configuration](#custom-configuration)
10. [Extending the Agent](#extending-the-agent)
    - [Custom Strategies](#custom-strategies)
    - [Custom Validators](#custom-validators)
    - [Plugins](#plugins)
    - [Webhooks](#webhooks)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)
13. [FAQ](#faq)
14. [Files](#files)
15. [License](#license)

---

## Overview

The Cloud Migration Agent provides comprehensive cloud migration capabilities following the industry-standard 6 Rs framework. It handles the full lifecycle from workload assessment through post-migration validation and cost optimization.

### What It Does

- **Workload Assessment**: Evaluate servers and applications for migration readiness using the 6 Rs
- **Strategy Recommendation**: Automatically suggest Rehost, Replatform, Refactor, Repurchase, Retire, or Retain
- **Wave Planning**: Group applications into migration waves with timeline and dependency awareness
- **Migration Execution**: Step-by-step migration with tracking and rollback capability
- **Post-Migration Validation**: 8-category health check (network, DNS, services, database, backup, monitoring, security, performance)
- **Cost Optimization**: Analyze cloud spend and recommend reserved instances, right-sizing, spot instances, and storage tiering
- **Multi-Cloud Support**: AWS, Azure, GCP with provider-specific recommendations

### Architecture

The agent is built on a modular engine architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloud Migration Agent                     │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│ Assessment  │    Wave     │ Execution   │   Validation    │
│   Engine    │   Planner   │   Engine    │     Engine      │
├─────────────┼─────────────┼─────────────┼─────────────────┤
│ 6 Rs Logic  │ Dependency  │ Step-by-Step│ 8-Category     │
│ Risk Score  │ Graph       │ Tracking    │ Health Check   │
│ Complexity  │ Wave Batching│ Rollback   │ Compliance     │
└─────────────┴─────────────┴─────────────┴─────────────────┘
         │            │            │            │
         └────────────┴────────────┴────────────┘
                          │
              ┌───────────┴───────────┐
              │    Cost Optimizer     │
              │  Reserved Instances   │
              │  Right-Sizing         │
              │  Spot Instances       │
              │  Storage Tiering      │
              │  Scheduling           │
              └───────────────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **6 Rs** | Rehost, Replatform, Refactor, Repurchase, Retire, Retain — the industry-standard migration strategies |
| **Wave** | A batch of applications migrated together, typically 5-10 applications per wave |
| **Dependency Graph** | A mapping of application dependencies used for wave ordering |
| **Validation** | Post-migration health checks across 8 categories |
| **Rollback** | The ability to reverse a migration if issues are detected |

---

## Prerequisites

Before using the Cloud Migration Agent, ensure you have the following:

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8+ | 3.10+ |
| Memory | 2 GB | 8 GB |
| Disk Space | 500 MB | 2 GB |
| OS | Linux, macOS, Windows | Linux |

### Python Dependencies

```bash
pip install -r requirements.txt
```

Core dependencies:
- `pydantic` — Data models and validation
- `networkx` — Dependency graph operations
- `rich` — Terminal output formatting
- `pyyaml` — Configuration file parsing

### Cloud Provider Access

Depending on your target cloud, you'll need:

| Provider | Requirements |
|----------|--------------|
| **AWS** | AWS CLI configured, IAM role or access keys with migration permissions |
| **Azure** | Azure CLI authenticated, Contributor role on target subscription |
| **GCP** | gcloud CLI authenticated, Editor role on target project |

### Network Requirements

- Outbound internet access (for cloud provider APIs)
- VPN or DirectConnect/ExpressRoute to target environment (for live migrations)
- Firewall rules allowing migration traffic on required ports

---

## Features

| Feature | Description |
|---------|-------------|
| 6 Rs Framework | Industry-standard migration strategy classification |
| Server Inventory | Track hostname, OS, role, CPU, RAM, storage, cost |
| Application Mapping | Map servers to applications with dependencies |
| Risk Assessment | Identify and classify migration risks with scoring |
| Wave Planning | Batch applications into manageable migration waves |
| Step Tracking | 7-step migration execution with progress |
| Rollback | Reverse migration on failure |
| Validation | 8-category post-migration health check |
| Cost Optimization | 5 optimization categories with savings estimates |
| Compliance | SOC2, PCI-DSS, HIPAA, GDPR, ISO27001, FedRAMP |
| Dependency Graph | Visualize and analyze application dependencies |
| Timeline Estimation | Predict migration timelines based on wave cadence |
| Multi-Cloud | Provider-specific recommendations for AWS, Azure, GCP |
| Custom Strategies | Extend the 6 Rs with organization-specific strategies |
| Audit Logging | Complete audit trail of all migration activities |
| Export Reports | Generate PDF, JSON, and CSV migration reports |

---

## Cloud Provider Support

### AWS (Amazon Web Services)

| Feature | Support Level | Notes |
|---------|---------------|-------|
| EC2 | Full | Rehost (lift-and-shift) with conversion |
| RDS | Full | Replatform to managed database |
| S3 | Full | Storage tiering recommendations |
| Lambda | Partial | For Refactor strategy only |
| ECS/EKS | Partial | Container-based replatforming |
| Reserved Instances | Full | 1-year and 3-year recommendations |
| Spot Instances | Full | Fault-tolerant workload identification |

### Azure (Microsoft Azure)

| Feature | Support Level | Notes |
|---------|---------------|-------|
| Virtual Machines | Full | Rehost with Azure Migrate integration |
| Azure SQL | Full | Replatform to managed database |
| Blob Storage | Full | Hot/Cool/Archive tier recommendations |
| Azure Functions | Partial | For Refactor strategy only |
| AKS | Partial | Container-based replatforming |
| Reserved VM Instances | Full | 1-year and 3-year recommendations |
| Spot VMs | Full | Fault-tolerant workload identification |

### GCP (Google Cloud Platform)

| Feature | Support Level | Notes |
|---------|---------------|-------|
| Compute Engine | Full | Rehost with Migrate for Compute Engine |
| Cloud SQL | Full | Replatform to managed database |
| Cloud Storage | Full | Standard/Nearline/Coldline tier recommendations |
| Cloud Functions | Partial | For Refactor strategy only |
| GKE | Partial | Container-based replatforming |
| Committed Use | Full | 1-year and 3-year recommendations |
| Preemptible VMs | Full | Fault-tolerant workload identification |

### Provider Comparison

| Criteria | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Migration Tools | DMS, SMS, DMS | Azure Migrate, Site Recovery | Migrate for Compute Engine |
| Managed Databases | RDS, Aurora | Azure SQL, Cosmos DB | Cloud SQL, Spanner |
| Container Orchestration | ECS, EKS | AKS | GKE |
| Serverless | Lambda | Azure Functions | Cloud Functions |
| Pricing Model | Pay-as-you-go, RI, Savings Plans | Pay-as-you-go, RI, Hybrid Benefit | Pay-as-you-go, CUD, SUDs |

---

## Quick Start

### Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
pip install -r requirements.txt
```

### Basic Setup

```python
from agents.cloud_migration.agent import CloudMigrationAgent

# Initialize with default configuration
agent = CloudMigrationAgent()

# Add your first server
server = agent.add_server(
    hostname="web-01",
    ip_address="10.0.1.10",
    operating_system="Ubuntu 20.04",
    role="web_server",
    cpu_cores=8,
    memory_gb=32,
    storage_gb=500,
    monthly_cost=500
)

# Assess the server
assessment = agent.assess_workload(server.server_id)
print(f"Strategy: {assessment.strategy.value}")
print(f"Cost: ${assessment.estimated_cost}/month")
```

### First Migration

```python
# Add more servers
agent.add_server("api-01", "10.0.1.20", "Ubuntu 22.04", "app_server", 16, 64, 200, 800)
agent.add_server("db-01", "10.0.1.30", "Ubuntu 20.04", "database_server", 32, 128, 2000, 2000)

# Add an application
app = agent.add_application(
    name="ecommerce",
    description="E-commerce platform",
    business_criticality="high"
)

# Map server to application
agent.add_dependency(
    source="ecommerce",
    target="web-01",
    type="runs_on"
)

# Assess all servers
for server in agent.list_servers():
    assessment = agent.assess_workload(server.server_id)
    print(f"{server.hostname}: {assessment.strategy.value}")

# Create migration plan
plan = agent.create_migration_plan(
    name="E-commerce Migration",
    application_names=["ecommerce"]
)

# Execute first wave
for wave in plan.waves:
    agent.start_wave(wave.wave_id)
    agent.execute_wave(wave.wave_id)
    agent.complete_wave(wave.wave_id)
```

---

## Usage

### Complete Migration Workflow

```python
agent = CloudMigrationAgent()

# 1. Inventory
servers = [
    ("web-01", "10.0.1.10", "Ubuntu 20.04", "web_server", 8, 32, 500, 500),
    ("api-01", "10.0.1.20", "Ubuntu 22.04", "app_server", 16, 64, 200, 800),
    ("db-01", "10.0.1.30", "Ubuntu 20.04", "database_server", 32, 128, 2000, 2000),
    ("cache-01", "10.0.1.40", "Ubuntu 22.04", "cache_server", 8, 32, 100, 300),
]
for s in servers:
    agent.add_server(*s)

# 2. Assessment
for server in agent.list_servers():
    a = agent.assess_workload(server.server_id)
    print(f"{server.hostname}: {a.strategy.value} ({a.complexity})")

# 3. Planning
plan = agent.create_migration_plan("Q3 Migration", ["ecommerce", "api", "analytics"])

# 4. Execution
for wave in plan.waves:
    agent.start_wave(wave.wave_id)
    result = agent.execute_wave(wave.wave_id)
    if result["status"] == "in_progress":
        agent.complete_wave(wave.wave_id)

# 5. Validation
for server in agent.list_servers():
    v = agent.run_validation(server.server_id)
    print(f"{server.hostname}: {v['overall_status']} ({v['summary']['success_rate']}%)")

# 6. Cost Optimization
cost = agent.analyze_costs(monthly_spend=3600)
print(f"Savings: ${cost['total_potential_savings']}/month")
```

### Workload Assessment

The assessment engine evaluates each server and recommends a migration strategy:

```python
# Add servers with different characteristics
servers = [
    ("web-simple", "10.0.1.10", "Ubuntu 20.04", "web_server", 4, 8, 100, 200),
    ("web-complex", "10.0.1.11", "Ubuntu 22.04", "web_server", 16, 64, 500, 800),
    ("legacy-app", "10.0.1.12", "Windows Server 2012", "app_server", 4, 16, 200, 300),
    ("database", "10.0.1.13", "Ubuntu 20.04", "database_server", 32, 128, 2000, 2000),
]

for s in servers:
    server = agent.add_server(*s)
    assessment = agent.assess_workload(server.server_id)
    print(f"{server.hostname}:")
    print(f"  Strategy: {assessment.strategy.value}")
    print(f"  Complexity: {assessment.complexity}")
    print(f"  Risk Level: {assessment.risk_level.value}")
    print(f"  Estimated Cost: ${assessment.estimated_cost}/month")
    print(f"  Recommended Provider: {assessment.recommended_provider}")
    print()
```

### Wave Planning

Organize applications into migration waves with dependency awareness:

```python
# Add applications with dependencies
agent.add_application("frontend", "React frontend", business_criticality="high")
agent.add_application("api", "REST API", business_criticality="high")
agent.add_application("database", "PostgreSQL", business_criticality="critical")
agent.add_application("cache", "Redis cache", business_criticality="medium")
agent.add_application("analytics", "Analytics service", business_criticality="low")

# Map dependencies
agent.add_dependency("frontend", "api", "calls")
agent.add_dependency("api", "database", "reads_from")
agent.add_dependency("api", "cache", "reads_from")
agent.add_dependency("analytics", "database", "reads_from")

# Create migration plan
plan = agent.create_migration_plan(
    name="Platform Migration",
    application_names=["frontend", "api", "database", "cache", "analytics"]
)

# Review waves
for wave in plan.waves:
    print(f"Wave {wave.wave_number}:")
    print(f"  Applications: {', '.join(wave.application_names)}")
    print(f"  Estimated Duration: {wave.estimated_duration}")
    print(f"  Risk Level: {wave.risk_level.value}")
    print()
```

### Migration Execution

Execute migrations with tracking and rollback capability:

```python
# Execute a wave
wave = plan.waves[0]
agent.start_wave(wave.wave_id)

# Track execution
result = agent.execute_wave(wave.wave_id)
print(f"Status: {result['status']}")
print(f"Progress: {result['progress']}%")
print(f"Steps Completed: {result['steps_completed']}/{result['total_steps']}")

# If issues occur, rollback
if result['status'] == 'failed':
    agent.rollback_wave(wave.wave_id)
    print("Wave rolled back successfully")
```

### Post-Migration Validation

Validate migration success across 8 categories:

```python
# Run validation for a server
validation = agent.run_validation(server.server_id)

print(f"Overall Status: {validation['overall_status']}")
print(f"Success Rate: {validation['summary']['success_rate']}%")
print()

# Check each category
for category, result in validation['categories'].items():
    status = result['status']
    print(f"  {category}: {status}")
    if status == 'failed':
        for issue in result['issues']:
            print(f"    - {issue}")
```

### Cost Optimization

Analyze and optimize cloud spending:

```python
# Analyze costs with current monthly spend
cost_analysis = agent.analyze_costs(monthly_spend=15000)

print(f"Current Spend: ${cost_analysis['current_spend']}/month")
print(f"Optimized Spend: ${cost_analysis['optimized_spend']}/month")
print(f"Total Savings: ${cost_analysis['total_potential_savings']}/month")
print(f"Savings Percentage: {cost_analysis['savings_percentage']}%")
print()

# Get detailed recommendations
recommendations = agent.get_cost_recommendations()
for rec in recommendations:
    print(f"{rec['category']}:")
    print(f"  Action: {rec['action']}")
    print(f"  Savings: ${rec['monthly_savings']}/month")
    print(f"  Implementation Effort: {rec['effort']}")
    print()
```

---

## API Reference

### CloudMigrationAgent Methods

#### Server Management

| Method | Signature | Description |
|--------|-----------|-------------|
| `add_server` | `(hostname: str, ip_address: str, operating_system: str, role: str, cpu_cores: int, memory_gb: int, storage_gb: int, monthly_cost: float) -> Server` | Add server to inventory |
| `get_server` | `(server_id: str) -> Server` | Get server by ID |
| `update_server` | `(server_id: str, **kwargs) -> Server` | Update server properties |
| `delete_server` | `(server_id: str) -> bool` | Remove server from inventory |
| `list_servers` | `() -> List[Server]` | List all servers |
| `search_servers` | `(query: str) -> List[Server]` | Search servers by hostname or role |

#### Application Management

| Method | Signature | Description |
|--------|-----------|-------------|
| `add_application` | `(name: str, description: str, business_criticality: str = "medium") -> Application` | Add application |
| `get_application` | `(app_name: str) -> Application` | Get application by name |
| `update_application` | `(app_name: str, **kwargs) -> Application` | Update application properties |
| `delete_application` | `(app_name: str) -> bool` | Remove application |
| `list_applications` | `() -> List[Application]` | List all applications |
| `add_server_to_application` | `(app_name: str, server_id: str) -> bool` | Associate server with application |

#### Dependency Management

| Method | Signature | Description |
|--------|-----------|-------------|
| `add_dependency` | `(source: str, target: str, dep_type: str) -> Dependency` | Map dependency between applications |
| `remove_dependency` | `(source: str, target: str) -> bool` | Remove dependency |
| `list_dependencies` | `(app_name: str = None) -> List[Dependency]` | List dependencies, optionally filtered |
| `get_dependency_graph` | `() -> Dict` | Get full dependency graph |
| `detect_cycles` | `() -> List[List[str]]` | Detect circular dependencies |

#### Assessment

| Method | Signature | Description |
|--------|-----------|-------------|
| `assess_workload` | `(server_id: str) -> Assessment` | Assess server for migration |
| `get_assessment` | `(server_id: str) -> Assessment` | Get existing assessment |
| `get_assessment_summary` | `() -> Dict` | Assessment overview |
| `list_assessments` | `() -> List[Assessment]` | List all assessments |
| `export_assessments` | `(format: str = "json") -> str` | Export assessments to file |

#### Migration Planning

| Method | Signature | Description |
|--------|-----------|-------------|
| `create_migration_plan` | `(name: str, application_names: List[str]) -> MigrationPlan` | Create wave-based plan |
| `get_plan` | `(plan_id: str) -> MigrationPlan` | Get plan by ID |
| `list_plans` | `() -> List[MigrationPlan]` | List all plans |
| `update_plan` | `(plan_id: str, **kwargs) -> MigrationPlan` | Update plan properties |
| `delete_plan` | `(plan_id: str) -> bool` | Remove plan |
| `get_plan_status` | `(plan_id: str) -> Dict` | Get plan progress |

#### Wave Execution

| Method | Signature | Description |
|--------|-----------|-------------|
| `start_wave` | `(wave_id: str) -> Dict` | Begin wave execution |
| `execute_wave` | `(wave_id: str) -> Dict` | Execute migration steps |
| `complete_wave` | `(wave_id: str) -> Dict` | Mark wave complete |
| `fail_wave` | `(wave_id: str, reason: str) -> Dict` | Mark wave failed |
| `rollback_wave` | `(wave_id: str) -> Dict` | Rollback wave |
| `get_wave_status` | `(wave_id: str) -> Dict` | Get wave progress |
| `list_waves` | `(plan_id: str = None) -> List[Wave]` | List all waves |

#### Validation

| Method | Signature | Description |
|--------|-----------|-------------|
| `run_validation` | `(server_id: str) -> Dict` | Post-migration validation |
| `get_validation_results` | `(server_id: str) -> Dict` | Get validation details |
| `run_validation_category` | `(server_id: str, category: str) -> Dict` | Run specific validation category |
| `list_validations` | `() -> List[Dict]` | List all validation results |

#### Cost Optimization

| Method | Signature | Description |
|--------|-----------|-------------|
| `analyze_costs` | `(monthly_spend: float) -> Dict` | Cost optimization analysis |
| `get_cost_recommendations` | `() -> List[Dict]` | Get optimization recommendations |
| `calculate_savings` | `(recommendations: List[str]) -> Dict` | Calculate savings for specific recommendations |
| `export_cost_report` | `(format: str = "json") -> str` | Export cost report |

### Data Models

#### Server

```python
class Server:
    server_id: str              # Unique identifier (UUID)
    hostname: str               # Server hostname
    ip_address: str             # IP address
    operating_system: str       # OS name and version
    role: ServerRole            # Server role (web_server, app_server, etc.)
    cpu_cores: int              # Number of CPU cores
    memory_gb: float            # Memory in GB
    storage_gb: float           # Storage in GB
    monthly_cost: float         # Monthly cost in USD
    status: str                 # current, migrated, retired
    tags: Dict[str, str]        # Custom tags
    created_at: datetime        # Creation timestamp
    updated_at: datetime        # Last update timestamp
```

#### Application

```python
class Application:
    app_name: str               # Unique application name
    description: str            # Application description
    business_criticality: str   # low, medium, high, critical
    servers: List[str]          # List of server IDs
    dependencies: List[str]     # List of dependency targets
    tags: Dict[str, str]        # Custom tags
    created_at: datetime        # Creation timestamp
```

#### Assessment

```python
class Assessment:
    assessment_id: str          # Unique identifier (UUID)
    server_id: str              # Reference to server
    strategy: MigrationStrategy # 6 Rs strategy recommendation
    complexity: str             # low, medium, high
    risk_level: RiskLevel       # LOW, MEDIUM, HIGH, CRITICAL
    estimated_cost: float       # Estimated monthly cost in cloud
    estimated_savings: float    # Estimated savings vs current
    recommended_provider: str   # aws, azure, gcp
    recommendations: List[str]  # List of specific recommendations
    assessed_at: datetime       # Assessment timestamp
```

#### MigrationPlan

```python
class MigrationPlan:
    plan_id: str                # Unique identifier (UUID)
    name: str                   # Plan name
    waves: List[Wave]           # List of migration waves
    total_applications: int     # Total applications in plan
    estimated_duration: str     # Estimated total duration
    status: str                 # planned, in_progress, completed
    created_at: datetime        # Creation timestamp
```

#### Wave

```python
class Wave:
    wave_id: str                # Unique identifier (UUID)
    wave_number: int            # Wave sequence number
    application_names: List[str] # Applications in this wave
    server_ids: List[str]       # Servers in this wave
    estimated_duration: str     # Estimated duration
    risk_level: RiskLevel       # Overall risk level
    status: WaveStatus          # PLANNED, IN_PROGRESS, COMPLETED, FAILED, ROLLED_BACK
    started_at: Optional[datetime]  # Execution start time
    completed_at: Optional[datetime] # Execution completion time
    rollback_at: Optional[datetime]  # Rollback time
    error_message: Optional[str]     # Error if failed
```

### Enums

| Enum | Values |
|------|--------|
| `MigrationStrategy` | REHOST, REFACTOR, REPLATFORM, REPURCHASE, RETIRE, RETAIN |
| `ServerRole` | WEB_SERVER, APP_SERVER, DATABASE_SERVER, CACHE_SERVER, QUEUE_SERVER, PROXY_SERVER, MONITORING |
| `RiskLevel` | LOW, MEDIUM, HIGH, CRITICAL |
| `WaveStatus` | PLANNED, IN_PROGRESS, COMPLETED, FAILED, ROLLED_BACK |
| `ValidationStatus` | PENDING, PASSED, WARNING, FAILED |
| `ComplianceFramework` | SOC2, PCI_DSS, HIPAA, GDPR, ISO27001, FEDRAMP |
| `DependencyType` | CALLS, READS_FROM, WRITES_TO, DEPENDS_ON, SENDS_TO, RECEIVES_FROM |
| `BusinessCriticality` | LOW, MEDIUM, HIGH, CRITICAL |
| `ServerStatus` | CURRENT, MIGRATED, RETIRED, PENDING |

### Configuration

```python
from agent import Config

config = Config(
    # Provider settings
    default_provider="aws",          # aws, azure, gcp
    
    # Wave planning
    wave_size=5,                     # Applications per wave
    wave_cadence_weeks=2,            # Weeks between waves
    
    # Cost optimization
    cost_optimization_enabled=True,
    reserved_instance_term="1-year", # 1-year, 3-year
    
    # Compliance
    compliance_checking=True,
    compliance_frameworks=["SOC2", "PCI_DSS"],
    
    # Validation
    validation_categories=[
        "network", "dns", "services", "database",
        "backup", "monitoring", "security", "performance"
    ],
    
    # Output
    output_directory="./migration_reports",
    report_format="json",            # json, csv, pdf
    
    # Logging
    log_level="INFO",                # DEBUG, INFO, WARNING, ERROR
    audit_logging=True,
)
```

---

## Data Model

### Server Model

The Server model represents a physical or virtual server in the inventory.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `server_id` | str | Auto | Unique identifier (UUID) |
| `hostname` | str | Yes | Server hostname |
| `ip_address` | str | Yes | IPv4 or IPv6 address |
| `operating_system` | str | Yes | OS name and version |
| `role` | ServerRole | Yes | Server role |
| `cpu_cores` | int | Yes | Number of CPU cores |
| `memory_gb` | float | Yes | Memory in GB |
| `storage_gb` | float | Yes | Storage in GB |
| `monthly_cost` | float | Yes | Monthly cost in USD |
| `status` | str | Auto | current, migrated, retired |
| `tags` | Dict | No | Custom key-value tags |
| `created_at` | datetime | Auto | Creation timestamp |
| `updated_at` | datetime | Auto | Last update timestamp |

**Example:**

```python
server = agent.add_server(
    hostname="web-01",
    ip_address="10.0.1.10",
    operating_system="Ubuntu 20.04 LTS",
    role="web_server",
    cpu_cores=8,
    memory_gb=32,
    storage_gb=500,
    monthly_cost=500.00,
    tags={"environment": "production", "team": "platform"}
)
```

### Application Model

The Application model represents a logical application composed of one or more servers.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `app_name` | str | Yes | Unique application name |
| `description` | str | Yes | Application description |
| `business_criticality` | str | Yes | low, medium, high, critical |
| `servers` | List[str] | Auto | List of associated server IDs |
| `dependencies` | List[str] | Auto | List of dependency targets |
| `tags` | Dict | No | Custom key-value tags |
| `created_at` | datetime | Auto | Creation timestamp |

**Example:**

```python
app = agent.add_application(
    name="ecommerce",
    description="E-commerce platform frontend and backend",
    business_criticality="high",
    tags={"team": "commerce", "cost_center": "engineering"}
)
```

### Dependency Model

The Dependency model represents relationships between applications.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | str | Yes | Source application name |
| `target` | str | Yes | Target application name |
| `dep_type` | DependencyType | Yes | Type of dependency |
| `created_at` | datetime | Auto | Creation timestamp |

**Dependency Types:**

| Type | Description |
|------|-------------|
| `calls` | Source makes API calls to target |
| `reads_from` | Source reads data from target |
| `writes_to` | Source writes data to target |
| `depends_on` | Source requires target to function |
| `sends_to` | Source sends messages to target |
| `receives_from` | Source receives messages from target |

### Assessment Model

The Assessment model contains the results of a workload assessment.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `assessment_id` | str | Unique identifier (UUID) |
| `server_id` | str | Reference to assessed server |
| `strategy` | MigrationStrategy | 6 Rs recommendation |
| `complexity` | str | low, medium, high |
| `risk_level` | RiskLevel | Risk classification |
| `estimated_cost` | float | Estimated monthly cost in cloud |
| `estimated_savings` | float | Estimated savings vs current |
| `recommended_provider` | str | Recommended cloud provider |
| `recommendations` | List[str] | Specific recommendations |
| `assessed_at` | datetime | Assessment timestamp |

### Migration Plan Model

The MigrationPlan model contains waves and overall plan metadata.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `plan_id` | str | Unique identifier (UUID) |
| `name` | str | Human-readable plan name |
| `waves` | List[Wave] | Ordered list of migration waves |
| `total_applications` | int | Total applications in plan |
| `estimated_duration` | str | Estimated total duration |
| `status` | str | planned, in_progress, completed |
| `created_at` | datetime | Creation timestamp |

### Wave Model

The Wave model represents a batch of applications to migrate together.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `wave_id` | str | Unique identifier (UUID) |
| `wave_number` | int | Sequence number (1-based) |
| `application_names` | List[str] | Applications in this wave |
| `server_ids` | List[str] | Servers in this wave |
| `estimated_duration` | str | Estimated duration |
| `risk_level` | RiskLevel | Overall risk level |
| `status` | WaveStatus | Current status |
| `started_at` | Optional[datetime] | Execution start time |
| `completed_at` | Optional[datetime] | Completion time |
| `rollback_at` | Optional[datetime] | Rollback time |
| `error_message` | Optional[str] | Error if failed |

### Validation Model

The Validation model contains post-migration health check results.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `server_id` | str | Reference to validated server |
| `overall_status` | str | passed, warning, failed |
| `categories` | Dict[str, CategoryResult] | Results by category |
| `summary` | Dict | Summary statistics |
| `validated_at` | datetime | Validation timestamp |

**Validation Categories:**

| Category | Checks |
|----------|--------|
| `network` | Connectivity, latency, packet loss |
| `dns` | Resolution, TTL, propagation |
| `services` | Service availability, health endpoints |
| `database` | Connectivity, query performance, data integrity |
| `backup` | Backup status, recovery time |
| `monitoring` | Metrics collection, alerting |
| `security` | Firewall rules, access controls, SSL |
| `performance` | CPU, memory, disk I/O benchmarks |

### Cost Model

The Cost model contains optimization analysis results.

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `current_spend` | float | Current monthly spend |
| `optimized_spend` | float | Optimized monthly spend |
| `total_potential_savings` | float | Total savings amount |
| `savings_percentage` | float | Savings as percentage |
| `recommendations` | List[CostRecommendation] | Optimization recommendations |

---

## Examples

### Strategy Selection Logic

```python
# Low-cost servers → Retire or Rehost
# Database servers → Replatform (managed services)
# Legacy OS → Repurchase (SaaS alternative)
# High-cost, high-CPU → Refactor (cloud-native)

server = agent.add_server("legacy-01", "10.0.2.10", "Windows Server 2012", "app_server", 4, 16, 200, 200)
assessment = agent.assess_workload(server.server_id)
# → strategy: repurchase (legacy OS detected)
```

### Multi-Cloud Migration

```python
from agents.cloud_migration.agent import CloudMigrationAgent, Config

# Configure for multi-cloud
config = Config(
    default_provider="aws",
    enable_multi_cloud=True,
    cloud_preferences={
        "frontend": "aws",
        "backend": "azure",
        "analytics": "gcp"
    }
)

agent = CloudMigrationAgent(config=config)

# Add servers across providers
agent.add_server("web-aws", "10.0.1.10", "Ubuntu 20.04", "web_server", 8, 32, 500, 500)
agent.add_server("api-azure", "10.0.2.10", "Ubuntu 22.04", "app_server", 16, 64, 200, 800)
agent.add_server("data-gcp", "10.0.3.10", "Ubuntu 20.04", "database_server", 32, 128, 2000, 2000)

# Assess and get provider-specific recommendations
for server in agent.list_servers():
    assessment = agent.assess_workload(server.server_id)
    print(f"{server.hostname}: {assessment.recommended_provider}")
    # Output:
    # web-aws: aws
    # api-azure: azure
    # data-gcp: gcp
```

### Dependency-Aware Planning

```python
# Build complex dependency graph
agent.add_application("cdn", "CDN service", business_criticality="medium")
agent.add_application("frontend", "React SPA", business_criticality="high")
agent.add_application("api-gateway", "API Gateway", business_criticality="critical")
agent.add_application("auth", "Auth Service", business_criticality="critical")
agent.add_application("user-service", "User Service", business_criticality="high")
agent.add_application("order-service", "Order Service", business_criticality="high")
agent.add_application("inventory", "Inventory Service", business_criticality="medium")
agent.add_application("database", "PostgreSQL Cluster", business_criticality="critical")
agent.add_application("cache", "Redis Cluster", business_criticality="high")
agent.add_application("analytics", "Analytics Pipeline", business_criticality="low")

# Map dependencies
dependencies = [
    ("frontend", "cdn", "calls"),
    ("frontend", "api-gateway", "calls"),
    ("api-gateway", "auth", "calls"),
    ("api-gateway", "user-service", "calls"),
    ("api-gateway", "order-service", "calls"),
    ("user-service", "database", "reads_from"),
    ("user-service", "cache", "reads_from"),
    ("order-service", "database", "reads_from"),
    ("order-service", "inventory", "calls"),
    ("inventory", "database", "reads_from"),
    ("analytics", "database", "reads_from"),
]

for source, target, dep_type in dependencies:
    agent.add_dependency(source, target, dep_type)

# Create plan - waves are automatically ordered by dependencies
plan = agent.create_migration_plan("Full Platform Migration", 
    ["cdn", "frontend", "api-gateway", "auth", "user-service", 
     "order-service", "inventory", "database", "cache", "analytics"])

# Waves will be ordered:
# Wave 1: cache, database (no dependencies)
# Wave 2: auth, inventory (depend on wave 1)
# Wave 3: user-service, order-service (depend on wave 2)
# Wave 4: api-gateway (depends on wave 3)
# Wave 5: frontend, cdn (depends on wave 4)
# Wave 6: analytics (depends on wave 1)
```

### Compliance-Driven Migration

```python
from agents.cloud_migration.agent import CloudMigrationAgent, Config

# Configure with compliance requirements
config = Config(
    compliance_checking=True,
    compliance_frameworks=["PCI_DSS", "HIPAA", "SOC2"],
    require_encryption=True,
    audit_logging=True
)

agent = CloudMigrationAgent(config=config)

# Add PCI-scoped servers
agent.add_server("payment-01", "10.0.1.100", "Ubuntu 20.04", "app_server", 8, 32, 500, 1000)
agent.add_server("payment-db", "10.0.1.101", "Ubuntu 20.04", "database_server", 16, 64, 2000, 2000)

# Assess with compliance context
assessment = agent.assess_workload("payment-01")
print(f"Strategy: {assessment.strategy.value}")
print(f"Compliance Requirements: {assessment.compliance_requirements}")
# Output:
# Strategy: replatform
# Compliance Requirements: ['encryption_at_rest', 'encryption_in_transit', 'audit_logging', 'access_controls']
```

### Cost Optimization Analysis

```python
cost = agent.analyze_costs(monthly_spend=10000)
# Output:
# Current: $10,000/month
# Reserved Instances: save $3,000/month (30%)
# Right-sizing: save $1,500/month (15%)
# Spot Instances: save $2,000/month (20%)
# Storage Tiering: save $1,000/month (10%)
# Scheduling: save $800/month (8%)
# Total savings: $8,300/month (83%)
# Optimized: $1,700/month
```

### Automated Validation Pipeline

```python
# Run comprehensive validation after migration
validation_results = []
for server in agent.list_servers():
    if server.status == "migrated":
        result = agent.run_validation(server.server_id)
        validation_results.append({
            "hostname": server.hostname,
            "status": result["overall_status"],
            "success_rate": result["summary"]["success_rate"]
        })

# Generate validation report
print("Post-Migration Validation Report")
print("=" * 50)
for vr in validation_results:
    status_icon = "✓" if vr["status"] == "passed" else "✗"
    print(f"{status_icon} {vr['hostname']}: {vr['status']} ({vr['success_rate']}%)")

# Check for failures
failures = [vr for vr in validation_results if vr["status"] == "failed"]
if failures:
    print(f"\n{len(failures)} servers failed validation - investigate before proceeding")
else:
    print("\nAll servers passed validation - migration successful")
```

### Rollback and Recovery

```python
# Monitor wave execution and rollback on failure
for wave in plan.waves:
    print(f"\nExecuting Wave {wave.wave_number}...")
    agent.start_wave(wave.wave_id)
    
    result = agent.execute_wave(wave.wave_id)
    
    if result["status"] == "completed":
        agent.complete_wave(wave.wave_id)
        print(f"Wave {wave.wave_number} completed successfully")
    elif result["status"] == "failed":
        print(f"Wave {wave.wave_number} failed: {result.get('error', 'Unknown error')}")
        print("Initiating rollback...")
        rollback_result = agent.rollback_wave(wave.wave_id)
        if rollback_result["status"] == "rolled_back":
            print("Rollback completed successfully")
        else:
            print(f"Rollback failed: {rollback_result.get('error', 'Unknown error')}")
            # Alert operations team
            break
    else:
        # Wave in progress, wait and retry
        import time
        time.sleep(60)
        result = agent.execute_wave(wave.wave_id)
```

### Custom Configuration

```python
from agent import Config

# Production configuration
config = Config(
    # Provider
    default_provider="aws",
    enable_multi_cloud=False,
    
    # Wave planning
    wave_size=10,
    wave_cadence_weeks=2,
    max_parallel_migrations=3,
    
    # Cost optimization
    cost_optimization_enabled=True,
    reserved_instance_term="3-year",
    enable_spot_instances=True,
    spot_instance_max_discount=0.7,
    
    # Compliance
    compliance_checking=True,
    compliance_frameworks=["SOC2", "PCI_DSS"],
    require_encryption=True,
    
    # Validation
    validation_categories=[
        "network", "dns", "services", "database",
        "backup", "monitoring", "security", "performance"
    ],
    validation_timeout_seconds=300,
    
    # Output
    output_directory="./migration_reports",
    report_format="pdf",
    
    # Logging
    log_level="INFO",
    audit_logging=True,
    log_file="./logs/migration.log",
    
    # Notifications
    enable_notifications=True,
    notification_channels=["email", "slack"],
    notification_recipients=["ops@company.com"],
)

agent = CloudMigrationAgent(config=config)
```

---

## Extending the Agent

### Custom Strategies

You can extend the agent with custom migration strategies beyond the standard 6 Rs:

```python
from agents.cloud_migration import CloudMigrationAgent, MigrationStrategy

# Define custom strategy
class CustomStrategy(MigrationStrategy):
    CLOUD_NATIVE = "cloud_native"  # Build cloud-native from scratch
    HYBRID = "hybrid"              # Hybrid cloud approach
    EDGE = "edge"                  # Edge computing migration

# Register custom strategy logic
def assess_custom_strategy(server):
    if server.tags.get("compute_intensive"):
        return CustomStrategy.CLOUD_NATIVE
    elif server.tags.get("latency_sensitive"):
        return CustomStrategy.EDGE
    elif server.tags.get("hybrid_eligible"):
        return CustomStrategy.HYBRID
    return None

agent = CloudMigrationAgent()
agent.register_custom_assessor(assess_custom_strategy)
```

### Custom Validators

Add custom validation categories for organization-specific checks:

```python
def validate_custom_checks(server_id):
    """Custom validation checks."""
    results = {
        "license_compliance": {
            "status": "passed",
            "checks": ["license_valid", "seat_count_ok"]
        },
        "cost_allocation": {
            "status": "passed",
            "checks": ["cost_center_assigned", "budget_approved"]
        }
    }
    return results

agent = CloudMigrationAgent()
agent.register_custom_validator("license_compliance", validate_custom_checks)
```

### Plugins

Extend functionality with plugins:

```python
# Create a plugin
class CostAlertPlugin:
    def __init__(self, threshold=10000):
        self.threshold = threshold
    
    def on_cost_analysis(self, cost_result):
        if cost_result["current_spend"] > self.threshold:
            self.send_alert(cost_result)
    
    def send_alert(self, cost_result):
        print(f"ALERT: Monthly spend ${cost_result['current_spend']} exceeds threshold")

# Register plugin
agent = CloudMigrationAgent()
agent.register_plugin(CostAlertPlugin(threshold=15000))
```

### Webhooks

Receive notifications on migration events:

```python
# Configure webhooks
agent = CloudMigrationAgent()
agent.add_webhook("https://hooks.slack.com/services/xxx", events=["wave.completed", "wave.failed"])
agent.add_webhook("https://api.pagerduty.com/integrate", events=["validation.failed"])

# Webhook payload format
{
    "event": "wave.completed",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "wave_id": "wave-123",
        "wave_number": 1,
        "status": "completed",
        "applications": ["frontend", "api"]
    }
}
```

---

## Best Practices

1. **Assess Everything**: Never skip the assessment phase — it informs strategy, cost, and risk
2. **Start Small**: Pilot with low-risk, non-critical workloads before migrating production
3. **Map Dependencies**: Understand what connects to what before migrating to avoid outages
4. **Validate Thoroughly**: Run all 8 validation categories post-migration before declaring success
5. **Optimize After**: Right-size and purchase reservations after stabilizing in cloud
6. **Keep Rollback Ready**: Always have a rollback plan for each wave before execution
7. **Document Compliance**: Track which frameworks apply to each workload for audit purposes
8. **Monitor Costs**: Set up cost alerts and review spending weekly during migration
9. **Automate Testing**: Integrate automated tests into the validation pipeline
10. **Communicate Early**: Keep stakeholders informed about migration timelines and impacts
11. **Version Everything**: Track all configuration changes and migration artifacts
12. **Plan for Data**: Account for data migration bandwidth and storage requirements
13. **Security First**: Review security controls and access policies before and after migration
14. **Performance Baseline**: Capture performance metrics before migration for comparison

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Assessment shows RETIRE | Very low resource usage | Consider consolidating with other workloads |
| Wave deadlocked | Circular dependencies | Break dependency cycles before planning |
| Validation DNS fails | DNS propagation delay | Wait for TTL expiry or use force propagation |
| Cost estimate too high | Overestimated requirements | Review actual utilization metrics |
| Rollback fails | State mutated during migration | Implement idempotent rollback procedures |
| Server not found | Incorrect server_id | Verify with `list_servers()` and check IDs |
| Wave execution stuck | Network connectivity issues | Check VPN/firewall rules to target environment |
| Validation timeout | Slow service response | Increase timeout or check target performance |
| Dependency cycle detected | Circular application dependencies | Refactor dependencies to break cycles |
| Cost optimization low savings | Already optimized workloads | Focus on other migration priorities |
| Compliance check fails | Missing encryption/audit | Implement required controls before migration |
| Export fails | Invalid output path | Check directory permissions and path validity |
| Wave size exceeds limit | Too many applications | Increase `wave_size` in config or split manually |
| Assessment cache stale | Servers changed since last assessment | Clear cache with `agent.clear_assessment_cache()` |
| Multi-cloud routing failed | Provider quota exceeded | Request quota increase or redistribute workloads |

---

## FAQ

**Q: Can I migrate between clouds (e.g., AWS to Azure)?**
A: Yes, the agent supports cross-cloud migration planning. Configure source and target providers in the config, and the agent will recommend appropriate migration strategies.

**Q: How does the agent handle dependencies between applications?**
A: The agent builds a dependency graph and uses topological sorting to order migration waves. Applications with no dependencies migrate first, followed by dependent applications in sequence.

**Q: What happens if a migration wave fails?**
A: You can rollback the wave using `rollback_wave()`. The agent reverses all changes made during the wave. Implement idempotent rollback procedures for reliability.

**Q: Can I customize the validation categories?**
A: Yes, you can configure which categories to validate in the config. You can also register custom validators for organization-specific checks.

**Q: How accurate are the cost estimates?**
A: Cost estimates are based on server specifications and current cloud pricing. Actual costs may vary based on usage patterns, reserved instance purchases, and negotiated discounts. Use estimates as a baseline and adjust based on actual usage.

**Q: Does the agent support hybrid cloud migrations?**
A: Yes, the agent can plan hybrid cloud migrations where some workloads remain on-premises and others move to cloud. Use the RETAIN strategy for workloads that stay on-premises.

**Q: Can I run the agent in CI/CD pipelines?**
A: Yes, the agent supports CLI mode for automation. Use `--assess`, `--plan`, `--validate`, and `--cost` flags in your CI/CD pipeline.

**Q: How do I handle large database migrations?**
A: For large databases, use the REPLATFORM strategy to migrate to managed database services. Plan for data transfer time and consider using database replication for minimal downtime.

**Q: Can I track migration progress across multiple plans?**
A: Yes, use `list_plans()` and `get_plan_status()` to track progress across all migration plans. The agent maintains a complete audit trail.

**Q: What compliance frameworks are supported?**
A: The agent supports SOC2, PCI_DSS, HIPAA, GDPR, ISO27001, and FEDRAMP. You can configure which frameworks to check and add custom compliance requirements.

---

## Files

- `agent.py` — Full implementation with all engines
- `ARCHITECTURE.md` — System architecture with ASCII diagrams
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*Cloud Migration Agent v2.0 — Part of the Awesome Grok Skills collection.*