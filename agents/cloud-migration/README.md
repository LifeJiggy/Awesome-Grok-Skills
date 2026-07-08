# Cloud Migration Agent

> End-to-end cloud migration — assess workloads, plan waves, execute, validate, and optimize costs.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

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

---

## Features

| Feature | Description |
|---------|-------------|
| 6 Rs Framework | Industry-standard migration strategy classification |
| Server Inventory | Track hostname, OS, role, CPU, RAM, storage, cost |
| Application Mapping | Map servers to applications with dependencies |
| Risk Assessment | Identify and classify migration risks |
| Wave Planning | Batch applications into manageable migration waves |
| Step Tracking | 7-step migration execution with progress |
| Rollback | Reverse migration on failure |
| Validation | 8-category post-migration health check |
| Cost Optimization | 5 optimization categories with savings estimates |
| Compliance | SOC2, PCI-DSS, HIPAA, GDPR, ISO27001, FedRAMP |

---

## Quick Start

```python
from agents.cloud_migration.agent import CloudMigrationAgent

agent = CloudMigrationAgent()

# Add a server
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

# Assess it
assessment = agent.assess_workload(server.server_id)
print(f"Strategy: {assessment.strategy.value}")
print(f"Cost: ${assessment.estimated_cost}/month")

# Create migration plan
plan = agent.create_migration_plan("Production Migration", ["web-app", "api-service"])

# Validate after migration
validation = agent.run_validation(server.server_id)
print(f"Status: {validation['overall_status']}")
```

### Run the Agent

```bash
python agents/cloud-migration/agent.py --assess
python agents/cloud-migration/agent.py --plan
python agents/cloud-migration/agent.py --validate
python agents/cloud-migration/agent.py --cost 5000
python agents/cloud-migration/agent.py --status
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
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

---

## API Reference

### CloudMigrationAgent

| Method | Description |
|--------|-------------|
| `add_server(hostname, ip, os, role, cpu, mem, storage, cost)` | Add server to inventory |
| `add_application(name, description, ...)` | Add application |
| `add_dependency(source, target, type)` | Map dependency |
| `assess_workload(server_id)` | Assess server for migration |
| `get_assessment_summary()` | Assessment overview |
| `list_servers()` | List all servers |
| `list_applications()` | List all applications |
| `list_assessments()` | List all assessments |
| `create_migration_plan(name, apps)` | Create wave-based plan |
| `start_wave(wave_id)` | Begin wave execution |
| `complete_wave(wave_id)` | Mark wave complete |
| `fail_wave(wave_id, reason)` | Mark wave failed |
| `rollback_wave(wave_id)` | Rollback wave |
| `get_plan_status(plan_id)` | Plan progress |
| `list_plans()` | List all plans |
| `execute_wave(wave_id)` | Execute migration steps |
| `get_execution_status(exec_id)` | Execution progress |
| `list_executions()` | List all executions |
| `run_validation(server_id)` | Post-migration validation |
| `get_validation_results(server_id)` | Validation details |
| `analyze_costs(monthly_spend)` | Cost optimization analysis |
| `get_cost_recommendations()` | Optimization recommendations |

### Enums

| Enum | Values |
|------|--------|
| `MigrationStrategy` | REHOST, REFACTOR, REPLATFORM, REPURCHASE, RETIRE, RETAIN |
| `ServerRole` | WEB_SERVER, APP_SERVER, DATABASE_SERVER, CACHE_SERVER, QUEUE_SERVER, PROXY_SERVER, MONITORING |
| `RiskLevel` | LOW, MEDIUM, HIGH, CRITICAL |
| `WaveStatus` | PLANNED, IN_PROGRESS, COMPLETED, FAILED, ROLLED_BACK |
| `ValidationStatus` | PENDING, PASSED, WARNING, FAILED |
| `ComplianceFramework` | SOC2, PCI_DSS, HIPAA, GDPR, ISO27001, FEDRAMP |

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

---

## Configuration

```python
from agent import Config

config = Config(
    default_provider="aws",
    wave_size=5,
    wave_cadence_weeks=2,
    cost_optimization_enabled=True,
    compliance_checking=True,
    output_directory="./migration_reports",
)

agent = CloudMigrationAgent(config=config)
```

---

## Best Practices

1. **Assess Everything**: Never skip the assessment phase
2. **Start Small**: Pilot with low-risk, non-critical workloads
3. **Map Dependencies**: Understand what connects to what before migrating
4. **Validate Thoroughly**: Run all 8 validation categories post-migration
5. **Optimize After**: Right-size and purchase reservations after stabilizing
6. **Keep Rollback Ready**: Always have a rollback plan for each wave
7. **Document Compliance**: Track which frameworks apply to each workload

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Assessment shows RETIRE | Very low resource usage | Consider consolidating with other workloads |
| Wave deadlocked | Circular dependencies | Break dependency cycles before planning |
| Validation DNS fails | DNS propagation delay | Wait for TTL expiry or use force propagation |
| Cost estimate too high | Overestimated requirements | Review actual utilization metrics |
| Rollback fails | State mutated during migration | Implement idempotent rollback procedures |

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
