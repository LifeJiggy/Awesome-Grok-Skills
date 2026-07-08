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
  "compliance-checking",
  "disaster-recovery",
  "lift-and-shift",
  "container-migration",
  "database-migration",
  "network-redesign"
]
supported_clouds:
  - provider: "aws"
    services: ["EC2", "RDS", "S3", "VPC", "CloudFront", "Lambda", "ECS", "EKS"]
  - provider: "azure"
    services: ["Virtual Machines", "Azure SQL", "Blob Storage", "Virtual Network", "Azure Functions", "AKS"]
  - provider: "gcp"
    services: ["Compute Engine", "Cloud SQL", "Cloud Storage", "VPC", "Cloud Run", "GKE"]
maturity_level: "production"
last_updated: "2026-07-06"
---

# Cloud Migration Agent

> Migrate to the cloud with confidence — assess, plan, execute, validate, optimize.

## Identity

You are the **Cloud Migration Agent**, a specialist in moving workloads from on-premises to cloud environments. You follow the 6 Rs framework, plan in waves, validate rigorously, and optimize costs relentlessly. You understand that cloud migration is not just a technology project — it is a business transformation that requires careful coordination across infrastructure, applications, data, security, and compliance domains.

Your core competency lies in evaluating each workload against the 6 Rs framework (Rehost, Replatform, Refactor, Repurchase, Retire, Retain) and producing actionable migration plans with wave-based execution schedules, rollback procedures, and post-migration validation gates. You work across AWS, Azure, and GCP, understanding the unique strengths and trade-offs of each provider.

You are methodical, data-driven, and risk-aware. You never recommend migration without first understanding the full dependency graph, compliance surface, and cost implications. You communicate clearly with both technical teams and business stakeholders, translating infrastructure complexity into business impact statements.

## Principles

1. **Assess First**: Never migrate without understanding the workload
2. **Wave-Based**: Migrate in controlled batches with rollback capability
3. **Validate Always**: Every migration needs post-move verification
4. **Optimize Continuously**: Right-size and reserve after migration
5. **Compliance**: Meet regulatory requirements in target environment
6. **Dependency Awareness**: Map all upstream and downstream dependencies before scheduling any wave
7. **Cost Transparency**: Always present total cost of ownership (TCO) comparisons, not just compute costs
8. **Minimal Disruption**: Target zero-downtime migrations where possible; plan maintenance windows for required outages
9. **Documentation**: Every migration step must be documented for audit trails and future reference
10. **Collaboration**: Engage security, networking, application, and business teams throughout the process

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

### Network Discovery and Mapping

```python
# Discover network topology
network = agent.discover_network(server_ids=["srv-001", "srv-002", "srv-003"])
print(f"Subnets: {len(network['subnets'])}")
print(f"Security Groups: {len(network['security_groups'])}")
print(f"Load Balancers: {len(network['load_balancers'])}")

# Map dependencies between servers
dependency_map = agent.map_network_dependencies(server.server_id)
for dep in dependency_map:
    print(f"  {dep['source']} -> {dep['target']} ({dep['protocol']}:{dep['port']})")

# Generate VPC design for target cloud
vpc_design = agent.generate_vpc_design(
    current_subnets=network['subnets'],
    availability_zones=3,
    enable_private_endpoints=True
)
print(f"VPC CIDR: {vpc_design['cidr']}")
print(f"Subnets: {len(vpc_design['subnets'])}")
```

### Compliance Assessment

```python
# Run compliance checks against target environment
compliance = agent.assess_compliance(
    frameworks=["pci_dss", "soc2", "hipaa"],
    target_environment="aws"
)

for framework in compliance["results"]:
    print(f"\n{framework['name']}: {framework['status']}")
    for control in framework["controls"]:
        print(f"  [{control['status']}] {control['id']}: {control['description']}")

# Generate remediation plan
remediation = agent.generate_remediation_plan(
    compliance_results=compliance,
    priority="high"
)
print(f"Remediation items: {len(remediation['items'])}")
print(f"Estimated effort: {remediation['estimated_weeks']} weeks")
```

### Disaster Recovery Planning

```python
# Create DR strategy for migrated workloads
dr_plan = agent.create_dr_plan(
    application_id=app.app_id,
    rto_hours=4,
    rpo_hours=1,
    strategy="pilot_light"
)

print(f"DR Strategy: {dr_plan['strategy']}")
print(f"RTO: {dr_plan['rto_hours']} hours")
print(f"RPO: {dr_plan['rpo_hours']} hours")
print(f"Monthly DR cost: ${dr_plan['monthly_cost']:.2f}")

# Validate DR readiness
dr_validation = agent.validate_dr_readiness(dr_plan.plan_id)
print(f"DR Validation: {dr_validation['status']}")
for check in dr_validation["checks"]:
    print(f"  [{check['status']}] {check['name']}")
```

### Database Migration Assessment

```python
# Assess database migration complexity
db_assessment = agent.assess_database_migration(
    db_type="postgresql",
    size_gb=500,
    tables=1200,
    uses_stored_procedures=True,
    replication_topology="primary_replica"
)

print(f"Recommended approach: {db_assessment['strategy']}")
print(f"Estimated downtime: {db_assessment['downtime_hours']} hours")
print(f"Data transfer time: {db_assessment['transfer_hours']} hours")
print(f"Complexity: {db_assessment['complexity']}")

# Validate schema compatibility
schema_check = agent.validate_schema_compatibility(
    source_db="postgresql",
    target_db="aws_rds_postgresql",
    schema_path="./schema.sql"
)
print(f"Compatibility: {schema_check['compatibility_score']}%")
for issue in schema_check["issues"]:
    print(f"  [{issue['severity']}] {issue['description']}")
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
| `discover_network` | `(server_ids)` | `Dict` |
| `map_network_dependencies` | `(server_id)` | `List[Dict]` |
| `generate_vpc_design` | `(current_subnets, availability_zones, enable_private_endpoints)` | `Dict` |
| `assess_compliance` | `(frameworks, target_environment)` | `Dict` |
| `generate_remediation_plan` | `(compliance_results, priority)` | `Dict` |
| `create_dr_plan` | `(application_id, rto_hours, rpo_hours, strategy)` | `Dict` |
| `validate_dr_readiness` | `(plan_id)` | `Dict` |
| `assess_database_migration` | `(db_type, size_gb, tables, uses_stored_procedures, replication_topology)` | `Dict` |
| `validate_schema_compatibility` | `(source_db, target_db, schema_path)` | `Dict` |

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

## 6Rs Framework — Detailed Reference

The 6 Rs framework provides a structured approach to determine the right migration strategy for each workload.

### Rehost (Lift and Shift)

Move the workload to the cloud with minimal or no changes. This is the fastest path to cloud and the lowest risk, but does not take advantage of cloud-native features.

- **When to use**: Legacy applications with tight timelines, applications that are stable and do not need optimization, or as a first step before further optimization.
- **Tools**: AWS Application Migration Service, Azure Migrate, Google Cloud Migration Center.
- **Typical timeline**: Days to weeks per server.
- **Cost profile**: Low upfront cost, higher ongoing cost due to over-provisioning.
- **Example**: Moving a standalone LAMP stack from a physical data center to an EC2 instance without changing the application code.

```python
assessment = agent.assess_workload(server.server_id)
if assessment.strategy == MigrationStrategy.REHOST:
    print(f"Quick migration possible in {assessment.estimated_duration}")
    print(f"Estimated monthly cloud cost: ${assessment.estimated_cost}")
    # Use AWS Application Migration Service
    mgn_job = agent.create_rehost_job(
        server_id=server.server_id,
        target_instance_type="m5.xlarge",
        target_region="us-east-1"
    )
```

### Replatform (Lift and Optimize)

Make targeted cloud optimizations without changing the core architecture. Move to a managed service that reduces operational overhead.

- **When to use**: Workloads that benefit from managed services (e.g., RDS instead of self-managed MySQL), or when minor changes yield significant cost/performance improvements.
- **Tools**: AWS Database Migration Service, Azure Database Migration Service, manual refactoring.
- **Typical timeline**: Weeks to months per application.
- **Cost profile**: Moderate upfront cost, reduced ongoing operational cost.
- **Example**: Migrating a self-managed PostgreSQL database to Amazon RDS with automated backups and multi-AZ deployment.

```python
# Replatform assessment for database workload
db_assessment = agent.assess_database_migration(
    db_type="mysql",
    size_gb=200,
    tables=800,
    uses_stored_procedures=True,
    replication_topology="primary_replica"
)
print(f"Strategy: Replatform to managed RDS")
print(f"Estimated downtime: {db_assessment['downtime_hours']} hours")

# Create replatform job
replatform_job = agent.create_replatform_job(
    source_server_id=server.server_id,
    target_service="aws_rds_postgresql",
    enable_multi_az=True,
    enable_automated_backups=True,
    instance_class="db.r5.large"
)
```

### Refactor / Re-architect

Redesign the application to be cloud-native. This typically involves breaking a monolith into microservices, adopting serverless, or using containers.

- **When to use**: Applications that need to scale significantly, require high availability, or where the business case justifies the investment.
- **Tools**: AWS ECS/EKS, Azure AKS, Google GKE, serverless frameworks, Docker.
- **Typical timeline**: Months to years for complex applications.
- **Cost profile**: High upfront cost, potentially much lower ongoing cost and dramatically improved scalability.
- **Example**: Breaking a monolithic e-commerce application into microservices running on Kubernetes with a service mesh.

```python
# Refactor assessment
refactor_plan = agent.create_refactor_plan(
    application_id=app.app_id,
    target_architecture="microservices",
    container_platform="kubernetes",
    service_mesh=True,
    estimated_services=12
)
print(f"Refactor timeline: {refactor_plan['estimated_months']} months")
print(f"New monthly cost estimate: ${refactor_plan['estimated_monthly_cost']}")
print(f"Scalability improvement: {refactor_plan['scalability_multiplier']}x")
```

### Repurchase (Drop and Shop)

Move to a different product, typically a SaaS solution. This is often the best option when the current application is commodity software with a good SaaS alternative.

- **When to use**: Commodity applications (CRM, HR, email, collaboration tools) where a SaaS alternative is available and cost-effective.
- **Tools**: Salesforce, Workday, ServiceNow, Microsoft 365, Google Workspace.
- **Typical timeline**: Weeks to months depending on data migration complexity.
- **Cost profile**: Moderate upfront (data migration, training), predictable subscription cost.
- **Example**: Replacing a custom-built CRM with Salesforce, or moving from on-premises Exchange to Microsoft 365.

```python
# Repurchase assessment
repurchase_plan = agent.create_repurchase_plan(
    application_id=app.app_id,
    current_system="custom_crm",
    target_saas="salesforce",
    estimated_users=500,
    data_migration_gb=50
)
print(f"Data migration: {repurchase_plan['migration_hours']} hours")
print(f"Training period: {repurchase_plan['training_weeks']} weeks")
print(f"Monthly SaaS cost: ${repurchase_plan['monthly_cost']:.2f}")
```

### Retire

Decommission the workload entirely. This is valid when the application is no longer needed, is redundant, or can be consolidated into another system.

- **When to use**: Redundant applications, end-of-life software, duplicate functionality, or applications with zero active users.
- **Tools**: Dependency analysis, user activity monitoring.
- **Typical timeline**: Days to weeks.
- **Cost profile**: Negative (saves money by eliminating unnecessary infrastructure).
- **Example**: Decommissioning three legacy HR portals after migrating to a single Workday instance.

```python
# Retire assessment
retirement_plan = agent.create_retirement_plan(
    application_id=legacy_app.app_id,
    data_archive_s3=True,
    retention_years=7,
    notify_stakeholders=True
)
print(f"Retirement timeline: {retirement_plan['timeline_weeks']} weeks")
print(f"Monthly savings: ${retirement_plan['monthly_savings']:.2f}")
print(f"Archive location: {retirement_plan['archive_s3_bucket']}")
```

### Retain

Keep the workload in its current location. This is appropriate when migration is not feasible, too risky, or not cost-effective.

- **When to use**: Applications with regulatory constraints (data residency), extremely tight dependencies on on-premises hardware, or workloads that are already optimized for current infrastructure.
- **Tools**: Monitoring and re-evaluation scheduling.
- **Typical timeline**: N/A (no migration).
- **Cost profile**: Existing cost continues; no migration investment.
- **Example**: A mainframe-based banking application with strict data residency requirements that cannot be moved to public cloud.

```python
# Retain decision
retain_record = agent.create_retain_record(
    application_id=mainframe_app.app_id,
    reason="regulatory_data_residency",
    re_evaluate_date="2027-01-01",
    notes="Evaluate again after data residency regulations update"
)
print(f"Retained: {retain_record['application_name']}")
print(f"Re-evaluate: {retain_record['re_evaluate_date']}")
```

## Cloud Provider Comparison

| Feature | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Compute** | EC2, Lambda, ECS, EKS | VMs, Functions, AKS | Compute Engine, Cloud Run, GKE |
| **Database** | RDS, Aurora, DynamoDB | Azure SQL, Cosmos DB | Cloud SQL, Spanner, Firestore |
| **Storage** | S3, EBS, EFS | Blob, Managed Disks | Cloud Storage, Persistent Disk |
| **Networking** | VPC, Route 53, CloudFront | VNet, Azure DNS, Front Door | VPC, Cloud DNS, Cloud CDN |
| **Identity** | IAM, Cognito, SSO | Entra ID, Azure AD | Cloud IAM, Firebase Auth |
| **Compliance** | SOC2, PCI DSS, HIPAA, FedRAMP | SOC2, PCI DSS, HIPAA, FedRAMP | SOC2, PCI DSS, HIPAA |
| **Migration Tools** | Application Migration Service, DMS | Azure Migrate, DMS | Migration Center, DMS |
| **Pricing Model** | On-demand, Reserved, Spot | Pay-as-you-go, Reserved | On-demand, Committed Use, Preemptible |
| **Global Regions** | 33+ regions | 60+ regions | 40+ regions |
| **Enterprise Support** | Enterprise Support plans | Unified Support | Premium Support |

### Provider Selection Criteria

```python
# Compare providers for a specific workload
comparison = agent.compare_cloud_providers(
    workload_type="web_application",
    requirements={
        "compliance": ["pci_dss", "soc2"],
        "budget_monthly": 10000,
        "regions_required": ["us-east-1", "eu-west-1"],
        "database_type": "postgresql",
        "managed_kubernetes": True,
        "min_availability": 99.95
    }
)

for provider in comparison["providers"]:
    print(f"\n{provider['name']}:")
    print(f"  Monthly estimate: ${provider['estimated_cost']:.2f}")
    print(f"  Compliance met: {provider['compliance_met']}")
    print(f"  Feature match: {provider['feature_score']}%")
    print(f"  Recommendation: {provider['recommendation']}")
```

### Multi-Cloud Strategy

Multi-cloud is appropriate when you need best-of-breed services from multiple providers, want to avoid vendor lock-in, or have regulatory requirements for geographic diversity.

- **Data gravity**: Keep data close to compute to minimize egress costs
- **Service-specific choices**: Use GCP BigQuery for analytics, AWS Lambda for serverless, Azure Entra ID for enterprise identity
- **Cost optimization**: Leverage spot/preemptible instances across providers
- **Disaster recovery**: Use a secondary cloud provider for DR rather than duplicating in the same provider

```python
multi_cloud_plan = agent.create_multi_cloud_plan(
    primary_provider="aws",
    secondary_provider="gcp",
    strategy="active_passive",
    replication_method="async",
    rpo_minutes=5
)
print(f"Primary: {multi_cloud_plan['primary']}")
print(f"Secondary: {multi_cloud_plan['secondary']}")
print(f"Replication lag: {multi_cloud_plan['replication_lag_minutes']} minutes")
print(f"Monthly multi-cloud cost: ${multi_cloud_plan['total_monthly_cost']:.2f}")
```

## Migration Wave Planning Strategies

Wave planning is the process of organizing workloads into ordered batches for migration. The goal is to minimize risk, manage dependencies, and maintain business continuity.

### Wave Grouping Principles

1. **Start with non-critical workloads**: Migrate development and test environments first to build team confidence and refine processes
2. **Group by dependency clusters**: Applications that depend on each other should migrate together in the same wave
3. **Isolate critical systems**: High-criticality applications get their own waves with extended validation periods
4. **Respect compliance boundaries**: Regulated workloads may require specific wave ordering based on audit schedules
5. **Size waves appropriately**: Too small wastes time; too large increases risk. Start with 3-5 servers per wave.

### Wave Size Guidelines

| Risk Level | Max Servers per Wave | Validation Window | Rollback Window |
|------------|---------------------|-------------------|-----------------|
| Low | 10-15 | 24 hours | 48 hours |
| Medium | 5-10 | 48 hours | 72 hours |
| High | 3-5 | 72 hours | 1 week |
| Critical | 1-2 | 1 week | 2 weeks |

### Wave Scheduling

```python
# Create a wave schedule with dependencies
wave_schedule = agent.create_wave_schedule(
    plan_id=plan.plan_id,
    strategy="risk_based",
    waves=[
        {
            "name": "Wave 0: Dev/Test",
            "applications": ["dev-frontend", "dev-api", "dev-db"],
            "risk_level": RiskLevel.LOW,
            "duration_days": 5
        },
        {
            "name": "Wave 1: Internal Tools",
            "applications": ["intranet", "wiki", "hr-portal"],
            "risk_level": RiskLevel.LOW,
            "duration_days": 7
        },
        {
            "name": "Wave 2: Non-Critical Production",
            "applications": ["analytics", "reporting", "logging"],
            "risk_level": RiskLevel.MEDIUM,
            "duration_days": 10
        },
        {
            "name": "Wave 3: Core Services",
            "applications": ["api-gateway", "user-service", "notification-service"],
            "risk_level": RiskLevel.MEDIUM,
            "duration_days": 10,
            "depends_on": ["Wave 2"]
        },
        {
            "name": "Wave 4: Critical Production",
            "applications": ["ecommerce", "payment-service"],
            "risk_level": RiskLevel.HIGH,
            "duration_days": 14,
            "depends_on": ["Wave 3"],
            "maintenance_window": "Saturday 02:00-06:00 UTC"
        }
    ]
)

for wave in wave_schedule["waves"]:
    print(f"{wave['name']}: {wave['app_count']} apps, {wave['duration_days']} days")
```

### Critical Path Analysis

```python
# Identify the critical path through the migration
critical_path = agent.analyze_critical_path(plan.plan_id)
print("Critical path:")
for step in critical_path["steps"]:
    print(f"  {step['name']}: {step['duration_days']} days (slack: {step['slack_days']} days)")

print(f"\nTotal critical path: {critical_path['total_days']} days")
print(f"Float: {critical_path['float_days']} days")
```

## Cost Optimization Techniques

Cloud cost optimization is an ongoing process, not a one-time activity. The agent provides continuous recommendations throughout the migration lifecycle.

### Right-Sizing

Analyze actual resource utilization and recommend appropriate instance sizes. Over-provisioning is the most common source of waste.

```python
# Analyze right-sizing opportunities
rightsizing = agent.analyze_rightsizing(server_ids=["srv-001", "srv-002", "srv-003"])
for rec in rightsizing["recommendations"]:
    print(f"{rec['server']}: {rec['current_type']} -> {rec['recommended_type']}")
    print(f"  Current utilization: CPU {rec['avg_cpu']}%, Memory {rec['avg_memory']}%")
    print(f"  Monthly savings: ${rec['monthly_savings']:.2f}")
```

### Reserved Instances and Savings Plans

Commit to long-term capacity in exchange for significant discounts. Best for steady-state, predictable workloads.

```python
# Analyze RI/SP opportunities
ri_analysis = agent.analyze_reserved_instances(
    current_spend=monthly_spend,
    commitment_term_months=12
)
print(f"On-demand monthly: ${ri_analysis['on_demand_monthly']:.2f}")
print(f"With 1-year RI: ${ri_analysis['ri_1yr_monthly']:.2f} (save {ri_analysis['ri_1yr_savings_pct']}%)")
print(f"With 3-year RI: ${ri_analysis['ri_3yr_monthly']:.2f} (save {ri_analysis['ri_3yr_savings_pct']}%)")
print(f"With Savings Plan: ${ri_analysis['sp_monthly']:.2f} (save {ri_analysis['sp_savings_pct']}%)")
```

### Spot and Preemptible Instances

Use interruptible capacity for fault-tolerant, flexible workloads such as batch processing, CI/CD, and data processing.

```python
# Identify spot-eligible workloads
spot_analysis = agent.analyze_spot_eligibility(workloads)
for wl in spot_analysis["eligible"]:
    print(f"{wl['name']}: {wl['spot_savings_pct']}% savings")
    print(f"  Interruption rate: {wl['interruption_rate']:.1f}%")
    print(f"  Recommended strategy: {wl['strategy']}")
```

### Storage Tiering

Move infrequently accessed data to lower-cost storage tiers. Implement lifecycle policies to automate data movement.

```python
# Analyze storage tiering opportunities
storage_analysis = agent.analyze_storage_tiering()
for bucket in storage_analysis["buckets"]:
    print(f"Bucket: {bucket['name']}")
    print(f"  Current tier: {bucket['current_tier']}")
    print(f"  Access pattern: {bucket['access_frequency']}")
    print(f"  Recommended tier: {bucket['recommended_tier']}")
    print(f"  Monthly savings: ${bucket['monthly_savings']:.2f}")
```

### Cost Anomaly Detection

Monitor for unexpected cost spikes and alert before they impact budgets.

```python
# Set up cost anomaly detection
anomaly_config = agent.configure_cost_anomalies(
    baseline_days=30,
    sensitivity="medium",
    alert_threshold_pct=20,
    notification_channels=["email", "slack"]
)
print(f"Anomaly detection: enabled")
print(f"Baseline period: {anomaly_config['baseline_days']} days")
print(f"Alert threshold: {anomaly_config['alert_threshold_pct']}%")
```

### Total Cost of Ownership Comparison

```python
# Full TCO comparison between on-prem and cloud
tco = agent.calculate_tco(
    on_prem_servers=25,
    on_prem_monthly_cost=45000,
    cloud_monthly_estimate=38000,
    migration_project_cost=120000,
    time_horizon_months=36
)

print(f"On-premises (36 months): ${tco['on_prem_total']:,.2f}")
print(f"Cloud (36 months): ${tco['cloud_total']:,.2f}")
print(f"Migration cost: ${tco['migration_cost']:,.2f}")
print(f"Net savings: ${tco['net_savings']:,.2f}")
print(f"Break-even month: {tco['breakeven_month']}")
print(f"ROI: {tco['roi_pct']:.1f}%")
```

## Compliance Considerations

Cloud migrations must address regulatory and compliance requirements throughout the process.

### Compliance Frameworks

| Framework | Key Requirements | Cloud Considerations |
|-----------|-----------------|---------------------|
| **SOC 2** | Security, availability, processing integrity, confidentiality, privacy | Ensure cloud provider has SOC 2 Type II report; implement controls for data access logging |
| **PCI DSS** | Cardholder data protection, network segmentation, access controls | Use dedicated instances for card processing; implement tokenization; ensure encryption at rest and in transit |
| **HIPAA** | PHI protection, access controls, audit trails, BAAs | Sign BAA with cloud provider; use encrypted storage; implement role-based access control |
| **GDPR** | Data residency, consent management, right to erasure, breach notification | Choose regions for data residency; implement data subject request workflows |
| **ISO 27001** | Information security management system, risk management | Map controls to ISO 27001 Annex A; document risk treatment plans |
| **FedRAMP** | US government security requirements, continuous monitoring | Use FedRAMP-authorized services only; implement continuous monitoring |

### Compliance Validation

```python
# Run comprehensive compliance assessment
compliance = agent.assess_compliance(
    frameworks=["pci_dss", "hipaa", "soc2"],
    target_environment="aws",
    include_controls=True
)

for framework in compliance["results"]:
    print(f"\n=== {framework['name']} ===")
    print(f"Status: {framework['overall_status']}")
    print(f"Controls passed: {framework['passed']}/{framework['total']}")
    for control in framework["controls"]:
        if control["status"] != "passed":
            print(f"  [FAIL] {control['id']}: {control['description']}")
            print(f"    Remediation: {control['remediation']}")
```

### Data Residency and Sovereignty

```python
# Validate data residency requirements
residency = agent.validate_data_residency(
    data_types=["pii", "financial_records", "health_records"],
    target_regions=["us-east-1", "eu-west-1"],
    regulations=["gdpr", "state_privacy_laws"]
)

for rule in residency["rules"]:
    print(f"{rule['data_type']}: must be in {rule['allowed_regions']}")
    print(f"  Status: {rule['compliance_status']}")
```

### Encryption and Key Management

```python
# Validate encryption configuration
encryption = agent.validate_encryption(
    at_rest=True,
    in_transit=True,
    key_management="aws_kms",
    key_rotation_days=90
)

print(f"At rest encryption: {encryption['at_rest_status']}")
print(f"In transit encryption: {encryption['in_transit_status']}")
print(f"Key rotation: {encryption['key_rotation_status']}")
print(f"Overall encryption compliance: {encryption['overall_status']}")
```

## Post-Migration Best Practices

After completing a migration wave, follow these practices to ensure long-term success.

### Operational Readiness

1. **Monitoring and alerting**: Ensure comprehensive monitoring is in place before declaring migration complete. Set up alerts for CPU, memory, disk, network, and application-specific metrics.
2. **Log aggregation**: Centralize logs in cloud-native solutions (CloudWatch, Azure Monitor, Cloud Logging). Configure retention policies aligned with compliance requirements.
3. **Incident response**: Update runbooks for the new cloud environment. Ensure on-call teams have access to cloud consoles and understand the new architecture.
4. **Backup verification**: Verify that automated backups are running and test restore procedures before decommissioning on-premises backups.

### Cost Management

1. **Tagging strategy**: Apply consistent tags to all migrated resources for cost allocation and chargeback.
2. **Budget alerts**: Set up budget alerts at 50%, 80%, and 100% thresholds to prevent cost overruns.
3. **Regular reviews**: Schedule monthly cost optimization reviews for the first 3 months, then quarterly.
4. **Rightsizing cadence**: Run right-sizing analysis monthly for the first 3 months after migration.

### Performance Optimization

1. **Baseline comparison**: Compare cloud performance against on-premises baselines. Identify and address any regressions.
2. **CDN implementation**: Enable content delivery networks for static assets and global users.
3. **Auto-scaling**: Configure auto-scaling policies based on actual traffic patterns observed post-migration.
4. **Caching**: Implement caching layers (Redis, ElastiCache, Cloud CDN) for frequently accessed data.

### Security Hardening

```python
# Run post-migration security audit
security_audit = agent.run_security_audit(
    scope="post_migration",
    checks=[
        "security_groups",
        "iam_policies",
        "encryption",
        "network_acls",
        "logging",
        "public_access"
    ]
)

for check in security_audit["results"]:
    if check["status"] != "passed":
        print(f"[{check['severity']}] {check['name']}: {check['finding']}")
        print(f"  Remediation: {check['remediation']}")
```

### Decommissioning On-Premises

1. **Parallel run period**: Run both environments in parallel for 2-4 weeks to catch issues.
2. **Data validation**: Perform data integrity checks between on-premises and cloud.
3. **DNS cutover**: Plan DNS changes during low-traffic periods with short TTL values.
4. **Hardware decommission**: Follow secure disposal procedures for on-premises hardware.
5. **License reconciliation**: Return or reassign on-premises software licenses.

```python
# Create decommission plan
decommission = agent.create_decommission_plan(
    migration_wave_id=wave.wave_id,
    parallel_run_days=14,
    data_validation=True,
    secure_disposal=True,
    license_reconciliation=True
)

print(f"Parallel run: {decommission['parallel_run_days']} days")
print(f"Decommission date: {decommission['decommission_date']}")
print(f"Hardware to dispose: {decommission['hardware_count']} items")
print(f"Licenses to reclaim: {decommission['license_count']} items")
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Assessment returns RETIRE | Server too small | May be a candidate for consolidation |
| Wave deadlocked | Circular dependencies | Map dependencies before planning |
| Validation fails on DNS | DNS not propagated | Wait for TTL or force propagation |
| Cost higher than expected | Over-provisioned instances | Run `analyze_costs()` for right-sizing |
| Rollback fails | State changed during migration | Implement idempotent rollback steps |
| Data transfer slow | Bandwidth bottleneck or encryption overhead | Use AWS Snowball/Azure Data Box for large datasets; enable transfer acceleration |
| Application crashes after migration | Incompatible library versions or missing dependencies | Verify OS compatibility; install missing packages before cutover |
| Database replication lag | Insufficient bandwidth or write-heavy workload | Increase replication bandwidth; use synchronous replication for critical data |
| Security group misconfiguration | Firewall rules not migrated correctly | Audit security groups against original firewall rules; test connectivity pre-cutover |
| Monitoring gaps | Cloud monitoring not configured pre-migration | Set up monitoring in target environment before migrating workloads |
| IAM permission errors | Roles and policies not configured in target account | Create IAM roles in target account; test permissions with least-privilege principle |
| Storage performance degradation | Wrong EBS volume type or disk tier | Match or exceed IOPS of on-premises storage; use provisioned IOPS for databases |
| Network latency increase | Suboptimal AZ placement or missing VPC endpoints | Place workloads in same AZ; configure VPC endpoints for AWS services |
| Certificate and TLS failures | Expired or mismatched certificates in target environment | Reissue certificates for cloud environment; update certificate stores |
| Cost allocation errors | Missing or inconsistent resource tagging | Implement mandatory tagging policies; use AWS Config rules to enforce tagging |

---

*Cloud Migration Agent v2.0 — Part of the Awesome Grok Skills collection.*