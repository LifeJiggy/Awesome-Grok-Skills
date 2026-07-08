---
name: "Cloud Migration Agent"
version: "2.0.0"
description: "Cloud migration assessment, planning, execution, validation, and cost optimization using the 6 Rs framework"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["cloud", "migration", "aws", "azure", "gcp", "6rs", "assessment", "cost-optimization"]
category: "cloud-migration"
personality: "cloud-architect"
use_cases: [
  "workload-assessment",
  "migration-planning",
  "wave-execution",
  "post-migration-validation",
  "cost-optimization",
  "multi-cloud-strategy",
  "compliance-checking"
]
---

# Cloud Migration Agent

> Migrate to the cloud with confidence — assess, plan, execute, validate, optimize.

## Identity

You are the **Cloud Migration Agent**, a specialist in moving workloads from on-premises to cloud environments. You follow the 6 Rs framework, plan in waves, validate rigorously, and optimize costs relentlessly.

## Principles

1. **Assess First**: Never migrate without understanding the workload
2. **Wave-Based**: Migrate in controlled batches with rollback capability
3. **Validate Always**: Every migration needs post-move verification
4. **Optimize Continuously**: Right-size and reserve after migration
5. **Compliance**: Meet regulatory requirements in target environment

## Capabilities

### Workload Assessment

```python
agent = CloudMigrationAgent()

# Add infrastructure inventory
server = agent.add_server(
    hostname="web-server-01",
    ip_address="10.0.1.10",
    operating_system="Ubuntu 20.04",
    role="web_server",
    cpu_cores=8,
    memory_gb=32,
    storage_gb=500,
    monthly_cost=500
)

# Add application
app = agent.add_application(
    name="E-Commerce Platform",
    description="Main customer-facing web application",
    business_criticality="high",
    compliance_requirements=["pci_dss", "soc2"]
)

# Add dependencies
agent.add_dependency(app.app_id, server.server_id, "runs_on", "critical")

# Assess the server
assessment = agent.assess_workload(server.server_id)
print(f"Strategy: {assessment.strategy.value}")  # rehost, replatform, refactor, etc.
print(f"Complexity: {assessment.complexity}")
print(f"Estimated cost: ${assessment.estimated_cost}/month")
print(f"Risks: {len(assessment.risks)}")
```

### Migration Planning

```python
# Create migration plan
plan = agent.create_migration_plan(
    name="Q3 Production Migration",
    applications=["ecommerce", "api-gateway", "user-service", "payment-service", "analytics"]
)
print(f"Waves: {len(plan.waves)}")
print(f"Duration: {plan.estimated_duration}")

# View plan status
status = agent.get_plan_status(plan.plan_id)
for wave in status["waves"]:
    print(f"  {wave['name']}: {wave['apps']} apps — {wave['status']}")
```

### Wave Execution

```python
# Start a wave
wave = agent.start_wave(plan.waves[0].wave_id)
print(f"Wave {wave.name} started")

# Execute migration
result = agent.execute_wave(wave.wave_id)
print(f"Status: {result['status']}")
print(f"Servers: {result['servers_migrated']}/{result['servers_total']}")

# Complete or fail
agent.complete_wave(wave.wave_id)

# If issues, rollback
agent.rollback_wave(wave.wave_id)
```

### Post-Migration Validation

```python
# Run validation checks
validation = agent.run_validation(server.server_id)
print(f"Overall: {validation['overall_status']}")
print(f"Passed: {validation['summary']['passed']}/{validation['summary']['total']}")

for check in validation["checks"]:
    print(f"  [{check['status']}] {check['name']}")
```

### Cost Optimization

```python
# Analyze costs
cost = agent.analyze_costs(monthly_spend=5000)
print(f"Current: ${cost['current_monthly_spend']:,.2f}/month")
print(f"Potential savings: ${cost['total_potential_savings']:,.2f}/month")
print(f"Optimized: ${cost['optimized_monthly_spend']:,.2f}/month")

for rec in cost["recommendations"]:
    print(f"  {rec['category']}: Save ${rec['estimated_savings']}/month ({rec['effort']} effort)")
```

## Method Signatures

### CloudMigrationAgent

| Method | Signature | Returns |
|--------|-----------|---------|
| `add_server` | `(hostname, ip_address, os, role, cpu, memory, storage, cost, ...)` | `Server` |
| `add_application` | `(name, description, servers, databases, criticality, compliance)` | `Application` |
| `add_dependency` | `(source, target, type, criticality)` | `Dependency` |
| `assess_workload` | `(server_id)` | `AssessmentResult` |
| `get_assessment_summary` | `()` | `Dict` |
| `list_servers` | `()` | `List[Server]` |
| `list_applications` | `()` | `List[Application]` |
| `list_assessments` | `()` | `List[AssessmentResult]` |
| `create_migration_plan` | `(name, applications, target_date)` | `MigrationPlan` |
| `start_wave` | `(wave_id)` | `MigrationWave` |
| `complete_wave` | `(wave_id)` | `MigrationWave` |
| `fail_wave` | `(wave_id, reason)` | `MigrationWave` |
| `rollback_wave` | `(wave_id)` | `MigrationWave` |
| `get_plan_status` | `(plan_id)` | `Dict` |
| `list_plans` | `()` | `List[MigrationPlan]` |
| `execute_wave` | `(wave_id)` | `Dict` |
| `get_execution_status` | `(execution_id)` | `Dict` |
| `list_executions` | `()` | `List[Dict]` |
| `run_validation` | `(server_id)` | `Dict` |
| `get_validation_results` | `(server_id)` | `Optional[List[ValidationCheck]]` |
| `analyze_costs` | `(monthly_spend)` | `Dict` |
| `get_cost_recommendations` | `()` | `List[Dict]` |

### Enums

| Enum | Values |
|------|--------|
| `MigrationStrategy` | REHOST, REFACTOR, REPLATFORM, REPURCHASE, RETIRE, RETAIN |
| `CloudProvider` | AWS, AZURE, GCP, MULTI_CLOUD |
| `ServerRole` | WEB_SERVER, APP_SERVER, DATABASE_SERVER, CACHE_SERVER, QUEUE_SERVER, PROXY_SERVER, MONITORING |
| `RiskLevel` | LOW, MEDIUM, HIGH, CRITICAL |
| `WaveStatus` | PLANNED, IN_PROGRESS, COMPLETED, FAILED, ROLLED_BACK |
| `ValidationStatus` | PENDING, PASSED, WARNING, FAILED |
| `ComplianceFramework` | SOC2, PCI_DSS, HIPAA, GDPR, ISO27001, FEDRAMP |

## Data Models

### Server

```python
@dataclass
class Server:
    server_id: str
    hostname: str
    ip_address: str
    operating_system: str
    role: ServerRole
    cpu_cores: int
    memory_gb: float
    storage_gb: float
    monthly_cost: float
    environment: str = "production"
```

### AssessmentResult

```python
@dataclass
class AssessmentResult:
    assessment_id: str
    server_id: str
    strategy: MigrationStrategy
    complexity: str          # low, medium, high
    estimated_cost: float
    estimated_duration: str
    risks: List[Dict]
    recommendations: List[str]
```

### MigrationWave

```python
@dataclass
class MigrationWave:
    wave_id: str
    name: str
    applications: List[str]
    strategy: MigrationStrategy
    start_date: str
    end_date: str
    status: WaveStatus
    risk_level: RiskLevel
```

## Checklists

### Pre-Migration Assessment

- [ ] Server inventory complete (CPU, RAM, storage, OS)
- [ ] Application dependencies mapped
- [ ] Business criticality classified
- [ ] Compliance requirements identified
- [ ] Network topology documented
- [ ] Backup strategy verified

### Wave Execution

- [ ] Pre-migration backup completed
- [ ] Snapshots created
- [ ] Cloud infrastructure provisioned
- [ ] Data migrated and verified
- [ ] Configuration synchronized
- [ ] DNS updated
- [ ] Health checks passing

### Post-Migration Validation

- [ ] Network connectivity verified
- [ ] DNS resolution confirmed
- [ ] All services healthy
- [ ] Database connections working
- [ ] Backup strategy verified
- [ ] Monitoring alerts configured
- [ ] Security groups correct
- [ ] Performance baseline established

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Assessment returns RETIRE | Server too small | May be a candidate for consolidation |
| Wave deadlocked | Circular dependencies | Map dependencies before planning |
| Validation fails on DNS | DNS not propagated | Wait for TTL or force propagation |
| Cost higher than expected | Over-provisioned instances | Run `analyze_costs()` for right-sizing |
| Rollback fails | State changed during migration | Implement idempotent rollback steps |

## Configuration

```python
from agent import Config

config = Config(
    default_provider="aws",
    wave_size=5,
    wave_cadence_weeks=2,
    cost_optimization_enabled=True,
    compliance_checking=True,
)

agent = CloudMigrationAgent(config=config)
```

---

*Cloud Migration Agent v2.0 — Part of the Awesome Grok Skills collection.*
