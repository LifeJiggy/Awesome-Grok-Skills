---
name: "policy-automation"
category: "governance-tech"
version: "2.0.0"
tags: ["governance-tech", "policy-automation", "compliance", "regulatory", "policy-management"]
difficulty: "intermediate"
estimated_time: "40-55 minutes"
prerequisites: ["python", "governance-fundamentals"]
---

# Policy Automation

## Overview

Policy automation provides systematic tools for creating, managing, enforcing, and auditing organizational policies across IT security, data governance, regulatory compliance, and operational standards. This module covers policy authoring workflows, automated compliance checking, exception management, attestation campaigns, and policy-as-code implementations that transform static policy documents into enforceable, auditable, machine-readable rules.

## Core Capabilities

- **Policy Authoring**: Structured policy templates with version control, approval workflows, and multi-stakeholder review processes
- **Policy-as-Code**: Convert natural language policies into machine-enforceable rules using Rego (OPA), Cedar, or custom DSLs
- **Automated Compliance Checking**: Continuous evaluation of infrastructure, code, and configurations against policy requirements
- **Exception Management**: Workflow for policy exception requests with risk assessment, time-limited approvals, and renewal tracking
- **Attestation Campaigns**: Periodic policy acknowledgment and compliance attestation collection from employees and systems
- **Policy Impact Analysis**: Model the effect of policy changes on existing systems, workflows, and compliance posture
- **Regulatory Mapping**: Map internal policies to external regulatory requirements (GDPR, HIPAA, SOX, PCI-DSS)
- **Policy Dashboard**: Real-time compliance posture visibility across all policy domains
- **Change Detection**: Automated monitoring for policy-relevant changes in infrastructure, code, and configurations
- **Audit Evidence Generation**: Automatically collect evidence that policies are being followed for audit preparation

## Usage Examples

### Policy-as-Code

```python
from governance_tech.policy_automation import PolicyEngine, PolicyLanguage

engine = PolicyEngine(
    language=PolicyLanguage.REGO,
    policy_dir="policies/",
    decision_cache_ttl_seconds=60,
)

# Define a data residency policy
engine.define_policy(
    name="data_residency",
    description="Ensure customer data stays within approved regions",
    rules=[
        {"resource": "s3_bucket", "attribute": "region", "allowed_values": ["us-east-1", "us-west-2", "eu-west-1"]},
        {"resource": "rds_instance", "attribute": "region", "allowed_values": ["us-east-1", "us-west-2"]},
    ],
)

# Evaluate a resource against policies
result = engine.evaluate(
    resource_type="s3_bucket",
    resource_config={"name": "customer-data", "region": "ap-southeast-1"},
    policy="data_residency",
)

print(f"Decision: {result.decision}")
print(f"Violations: {result.violations}")
print(f"Remediation: {result.suggested_remediation}")
```

### Compliance Automation

```python
from governance_tech.policy_automation import ComplianceChecker

checker = ComplianceChecker(
    frameworks=["GDPR", "HIPAA", "PCI-DSS"],
    scan_schedule="daily",
)

# Run compliance scan
scan = checker.scan(
    scope="production",
    controls=["encryption_at_rest", "access_logging", "data_retention"],
)

print(f"Scan ID: {scan.scan_id}")
print(f"Controls Evaluated: {scan.controls_evaluated}")
print(f"Passed: {scan.controls_passed}")
print(f"Failed: {scan.controls_failed}")
print(f"Compliance Score: {scan.compliance_score:.1%}")

for violation in scan.violations[:5]:
    print(f"  FAIL: {violation.control}")
    print(f"    Resource: {violation.resource}")
    print(f"    Severity: {violation.severity}")
    print(f"    Fix: {violation.remediation}")
```

### Exception Management

```python
from governance_tech.policy_automation import ExceptionManager, RiskLevel

manager = ExceptionManager(
    max_exception_duration_days=90,
    auto_escalation=True,
)

# Request policy exception
exception = manager.request_exception(
    policy="encryption_at_rest",
    resource="legacy-database-prod",
    business_justification="Migration to encrypted storage planned for Q3",
    requested_by="dba_team",
    risk_level=RiskLevel.MEDIUM,
    compensating_controls=["network_isolation", "enhanced_monitoring"],
)

print(f"Exception: {exception.exception_id}")
print(f"Status: {exception.status}")
print(f"Expires: {exception.expiry_date}")
print(f"Risk Accepted: {exception.risk_score:.2f}")
```

### Attestation Campaign

```python
from governance_tech.policy_automation import AttestationCampaign

campaign = AttestationCampaign(
    name="Annual Security Policy Attestation 2026",
    policies=["acceptable_use", "data_classification", "incident_reporting"],
    deadline_days=30,
    target_audience="all_employees",
)

# Launch campaign
launch = campaign.launch()
print(f"Campaign: {launch.campaign_id}")
print(f"Target: {launch.target_count} employees")
print(f"Deadline: {launch.deadline}")

# Check progress
progress = campaign.get_progress()
print(f"Completed: {progress.completed_count}/{progress.target_count}")
print(f"Completion Rate: {progress.completion_rate:.1%}")
```

## Best Practices

- Implement policy-as-code for technical policies that can be automatically enforced (access control, encryption, tagging)
- Keep human-readable policy documents as the source of truth; machine enforcement is the implementation
- Version all policies with clear change logs and effective dates
- Build policy exception workflows that require risk acceptance from appropriate authority levels
- Run compliance scans continuously, not just at audit time
- Map each internal control to specific regulatory requirements for audit traceability
- Automate evidence collection to reduce manual audit preparation burden
- Implement policy drift detection to catch when systems deviate from policy requirements
- Review and update policies at least annually or when regulations change
- Include remediation guidance in all compliance findings, not just violation reports

## Related Modules

- `governance-tech/compliance-framework` - Compliance framework management
- `governance-tech/audit-systems` - Audit evidence collection and management
- `governance-tech/regulatory-reporting` - Regulatory report generation
- `governance-tech/governance-dashboard` - Compliance posture visualization

## Advanced Configuration

### Policy-as-Code Configuration

```yaml
policy_as_code:
  languages:
    rego:
      enabled: true
      version: "0.60.0"
      bundle_format: "tar.gz"
      decision_cache_ttl: 60
      
    cedar:
      enabled: true
      version: "2.0"
      
    custom_dsl:
      enabled: false
      parser: "lark"
      
  policy_management:
    version_control: true
    git_integration: true
    branch_protection: true
    require_review: true
    min_reviewers: 2
    
  decision_engine:
    mode: "sidecar"
    port: 8181
    log_level: "info"
    metrics_enabled: true
    
  policy_bundles:
    - name: "security_policies"
      path: "/policies/security/"
      sync_frequency: "on_change"
      
    - name: "data_governance_policies"
      path: "/policies/data_governance/"
      sync_frequency: "daily"
      
    - name: "infrastructure_policies"
      path: "/policies/infrastructure/"
      sync_frequency: "on_change"
```

### Compliance Checking Configuration

```yaml
compliance_checking:
  frameworks:
    - name: "GDPR"
      version: "2024"
      controls:
        - "data_encryption"
        - "access_control"
        - "data_retention"
        - "breach_notification"
        
    - name: "HIPAA"
      version: "2023"
      controls:
        - "phi_protection"
        - "access_logging"
        - "encryption_at_rest"
        - "audit_trails"
        
    - name: "PCI-DSS"
      version: "4.0"
      controls:
        - "cardholder_data_protection"
        - "network_segmentation"
        - "access_control"
        - "vulnerability_management"
        
  scan_settings:
    frequency: "daily"
    scope: "production"
    parallel_scans: 5
    timeout_minutes: 30
    
  remediation:
    auto_remediation: false
    remediation_suggestions: true
    ticket_integration: true
    
  reporting:
    daily_summary: true
    weekly_trend: true
    monthly_executive: true
```

### Exception Management Configuration

```yaml
exception_management:
  max_exception_duration_days: 90
  renewal_required: true
  auto_escalation: true
  
  risk_levels:
    low:
      max_duration_days: 180
      approver_role: "policy_owner"
      required_approvals: 1
      
    medium:
      max_duration_days: 90
      approver_role: "security_manager"
      required_approvals: 2
      
    high:
      max_duration_days: 30
      approver_role: "ciso"
      required_approvals: 3
      
    critical:
      max_duration_days: 7
      approver_role: "ceo"
      required_approvals: 3
      
  compensating_controls:
    required: true
    min_controls: 1
    validation_required: true
    
  reporting:
    overdue_exceptions: true
    expiring_exceptions: true
    risk_summary: true
```

### Attestation Campaign Configuration

```yaml
attestation_campaigns:
  default_deadline_days: 30
  reminder_frequency_days: 7
  max_reminders: 3
  
  target_audiences:
    - name: "all_employees"
      filter: "department != 'contractor'"
      
    - name: "engineering"
      filter: "department == 'engineering'"
      
    - name: "finance"
      filter: "department == 'finance'"
      
  policies:
    annual_security:
      - "acceptable_use"
      - "data_classification"
      - "incident_reporting"
      - "password_policy"
      
    role_based:
      developer:
        - "secure_coding"
        - "code_review"
        - "access_management"
        
      administrator:
        - "privileged_access"
        - "change_management"
        - "backup_recovery"
        
  reporting:
    daily_progress: true
    weekly_summary: true
    non_completion_alerts: true
```

## Architecture Patterns

### Policy Engine Architecture

```python
class PolicyEngine:
    def __init__(self, policy_store, decision_cache):
        self.store = policy_store
        self.cache = decision_cache
    
    async def evaluate(
        self,
        resource_type: str,
        resource_config: Dict,
        policy_name: str,
    ) -> PolicyDecision:
        # Check cache first
        cache_key = f"{policy_name}:{resource_type}:{hash(json.dumps(resource_config, sort_keys=True))}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        # Get policy
        policy = await self.store.get_policy(policy_name)
        
        # Evaluate policy rules
        violations = []
        for rule in policy.rules:
            if not self.evaluate_rule(rule, resource_config):
                violations.append(Violation(
                    rule=rule.name,
                    resource=resource_config,
                    expected=rule.expected,
                    actual=self.get_actual_value(rule, resource_config),
                ))
        
        # Determine decision
        decision = "allow" if len(violations) == 0 else "deny"
        
        # Generate remediation suggestions
        remediation = self.generate_remediation(violations) if violations else []
        
        result = PolicyDecision(
            decision=decision,
            policy=policy_name,
            resource_type=resource_type,
            resource_config=resource_config,
            violations=violations,
            remediation=remediation,
            evaluated_at=datetime.utcnow(),
        )
        
        # Cache result
        await self.cache.set(cache_key, result, ttl=60)
        
        return result
```

### Compliance Checker Architecture

```python
class ComplianceChecker:
    def __init__(self, control_registry, evidence_collector):
        self.controls = control_registry
        self.evidence = evidence_collector
    
    async def scan(
        self,
        scope: str,
        controls: List[str],
        frameworks: List[str],
    ) -> ComplianceScanResult:
        # Get controls to evaluate
        control_list = await self.controls.get_controls(controls, frameworks)
        
        # Evaluate each control
        results = []
        for control in control_list:
            result = await self.evaluate_control(control, scope)
            results.append(result)
        
        # Collect evidence
        evidence = await self.evidence.collect(results)
        
        # Calculate compliance score
        passed = sum(1 for r in results if r.status == "passed")
        total = len(results)
        score = passed / total if total > 0 else 0
        
        # Identify violations
        violations = [r for r in results if r.status == "failed"]
        
        return ComplianceScanResult(
            scan_id=str(uuid.uuid4()),
            scope=scope,
            frameworks=frameworks,
            controls_evaluated=total,
            controls_passed=passed,
            controls_failed=len(violations),
            compliance_score=score,
            violations=violations,
            evidence=evidence,
            scanned_at=datetime.utcnow(),
        )
```

### Exception Manager Architecture

```python
class ExceptionManager:
    def __init__(self, approval_workflow, risk_calculator):
        self.approvals = approval_workflow
        self.risk_calc = risk_calculator
    
    async def request_exception(
        self,
        policy: str,
        resource: str,
        business_justification: str,
        requested_by: str,
        risk_level: str,
        compensating_controls: List[str],
    ) -> PolicyException:
        # Calculate risk score
        risk_score = await self.risk_calc.calculate(
            policy=policy,
            resource=resource,
            risk_level=risk_level,
            compensating_controls=compensating_controls,
        )
        
        # Create exception request
        exception = PolicyException(
            exception_id=str(uuid.uuid4()),
            policy=policy,
            resource=resource,
            business_justification=business_justification,
            requested_by=requested_by,
            risk_level=risk_level,
            risk_score=risk_score,
            compensating_controls=compensating_controls,
            status="pending_approval",
            created_at=datetime.utcnow(),
        )
        
        # Submit for approval
        await self.approvals.submit(exception)
        
        return exception
```

### Attestation Campaign Architecture

```python
class AttestationCampaign:
    def __init__(self, user_registry, notification_service):
        self.users = user_registry
        self.notifier = notification_service
    
    async def launch(
        self,
        name: str,
        policies: List[str],
        deadline_days: int,
        target_audience: str,
    ) -> CampaignLaunch:
        # Get target users
        target_users = await self.users.get_users(target_audience)
        
        # Create campaign
        campaign = Campaign(
            campaign_id=str(uuid.uuid4()),
            name=name,
            policies=policies,
            deadline=datetime.utcnow() + timedelta(days=deadline_days),
            target_count=len(target_users),
            status="active",
            created_at=datetime.utcnow(),
        )
        
        # Send notifications
        for user in target_users:
            await self.notifier.send_attestation_request(
                user=user,
                campaign=campaign,
            )
        
        return CampaignLaunch(
            campaign_id=campaign.campaign_id,
            target_count=len(target_users),
            deadline=campaign.deadline,
        )
```

## Integration Guide

### Open Policy Agent Integration

```python
class OPAIntegration:
    def __init__(self, opa_url: str):
        self.opa_url = opa_url
    
    async def evaluate_policy(
        self,
        policy_path: str,
        input_data: Dict,
    ) -> OPAResult:
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "input": input_data,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.opa_url}/v1/data/{policy_path}",
                headers=headers,
                json=payload,
            )
        
        return self.parse_result(response.json())
    
    async def update_policy_bundle(self, bundle_path: str) -> bool:
        with open(bundle_path, "rb") as f:
            bundle_data = f.read()
        
        headers = {
            "Content-Type": "application/gzip",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.opa_url}/v1/bundles/policies",
                headers=headers,
                data=bundle_data,
            )
        
        return response.status_code == 200
```

### Terraform Integration

```python
class TerraformIntegration:
    def __init__(self, terraform_cloud_url: str, api_token: str):
        self.url = terraform_cloud_url
        self.api_token = api_token
    
    async def run_policy_check(
        self,
        workspace_id: str,
        policy_set_id: str,
    ) -> PolicyCheckResult:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "attributes": {
                "path": "plan",
                "workspace_id": workspace_id,
            },
            "type": "policy-checks",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/api/v2/policy-sets/{policy_set_id}/runs",
                headers=headers,
                json=payload,
            )
        
        return self.parse_policy_check(response.json())
```

### Kubernetes Admission Controller Integration

```python
class K8sAdmissionIntegration:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def validate_admission(
        self,
        admission_review: AdmissionReview,
    ) -> AdmissionResponse:
        headers = {
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.webhook_url,
                headers=headers,
                json=admission_review.to_dict(),
            )
        
        return self.parse_admission_response(response.json())
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_policies_status ON policies (status, effective_date);
CREATE INDEX idx_exceptions_status ON policy_exceptions (status, expiry_date);
CREATE INDEX idx_attestation_campaigns ON attestation_campaigns (status, deadline);

-- Create materialized view for compliance metrics
CREATE MATERIALIZED VIEW compliance_metrics_summary AS
SELECT 
    framework,
    DATE(scan_date) as scan_date,
    COUNT(*) as total_controls,
    SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passed_controls,
    AVG(CASE WHEN status = 'passed' THEN 100 ELSE 0 END) as compliance_score
FROM compliance_scan_results
GROUP BY framework, DATE(scan_date);

-- Partition compliance results by date
CREATE TABLE compliance_scan_results (
    id UUID PRIMARY KEY,
    scan_id VARCHAR(100),
    framework VARCHAR(50),
    control_id VARCHAR(100),
    status VARCHAR(20),
    scan_date TIMESTAMP
) PARTITION BY RANGE (scan_date);
```

### Caching Strategy

```python
class PolicyAutomationCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_policy_decision(
        self,
        policy_name: str,
        resource_hash: str,
    ) -> Optional[PolicyDecision]:
        cache_key = f"policy_decision:{policy_name}:{resource_hash}"
        cached = await self.redis.get(cache_key)
        if cached:
            return PolicyDecision.from_json(cached)
        return None
    
    async def cache_policy_decision(
        self,
        policy_name: str,
        resource_hash: str,
        decision: PolicyDecision,
    ):
        cache_key = f"policy_decision:{policy_name}:{resource_hash}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            decision.to_json()
        )
```

### Batch Processing

```python
class PolicyAutomationBatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
    
    async def process_batch(self, items: List, processor: Callable):
        batches = [
            items[i:i+self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                processor(item) for item in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class PolicyDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive policy data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive policy data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class PolicyAutomationAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            role_permissions = self.permissions.get(role, [])
            if action in role_permissions:
                return True
        return False
    
    def grant_role(self, user_id: str, role: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        self.roles[user_id].append(role)
```

### Audit Logging

```python
class PolicyAutomationAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'action': event.action,
            'resource_id': event.resource_id,
            'details': event.details,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: Policy evaluation errors**
```python
async def diagnose_policy_evaluation(policy_name: str, resource: Dict):
    # Check policy exists
    policy = await get_policy(policy_name)
    if not policy:
        print(f"Policy {policy_name} not found")
        return
    
    print(f"Policy: {policy_name}")
    print(f"  Rules: {len(policy.rules)}")
    
    # Try evaluation
    try:
        result = await policy_engine.evaluate(
            resource_type=resource['type'],
            resource_config=resource,
            policy_name=policy_name,
        )
        
        print(f"  Decision: {result.decision}")
        print(f"  Violations: {len(result.violations)}")
        
        for violation in result.violations:
            print(f"    - {violation.rule}: {violation.expected} vs {violation.actual}")
            
    except Exception as e:
        print(f"  ERROR: {e}")
        print(f"  Recommendation: Check policy syntax and resource format")
```

**Issue: Compliance scan failures**
```python
async def diagnose_compliance_failure(scan_id: str):
    scan = await get_compliance_scan(scan_id)
    
    print(f"Compliance Scan {scan_id}:")
    print(f"  Framework: {scan.framework}")
    print(f"  Status: {scan.status}")
    print(f"  Error: {scan.error_message}")
    
    # Common errors
    solutions = {
        "connection": "Check connectivity to scanned resources",
        "authentication": "Verify service account credentials",
        "timeout": "Increase scan timeout or reduce scope",
        "permission": "Ensure scanner has required permissions",
    }
    
    for key, solution in solutions.items():
        if key in scan.error_message.lower():
            print(f"\nSolution: {solution}")
```

**Issue: Attestation low completion rate**
```python
async def diagnose_attestation_completion(campaign_id: str):
    campaign = await get_attestation_campaign(campaign_id)
    
    print(f"Attestation Campaign: {campaign.name}")
    print(f"  Status: {campaign.status}")
    print(f"  Target: {campaign.target_count}")
    print(f"  Completed: {campaign.completed_count}")
    print(f"  Completion Rate: {campaign.completion_rate:.1%}")
    
    # Check by department
    by_department = await get_completion_by_department(campaign_id)
    
    print(f"\nBy Department:")
    for dept, rate in by_department.items():
        print(f"  {dept}: {rate:.1%}")
        
    if campaign.completion_rate < 0.8:
        print(f"\n  WARNING: Low completion rate")
        print(f"  Recommendations:")
        print(f"    1. Send reminder emails")
        print(f"    2. Escalate to managers")
        print(f"    3. Extend deadline if needed")
```

## API Reference

### Policy Management API

```python
# Create policy
POST /api/v1/policies
Request:
{
    "name": "data_residency",
    "description": "Ensure customer data stays within approved regions",
    "type": "technical",
    "language": "rego",
    "rules": [...],
    "effective_date": "2026-07-01"
}

Response:
{
    "policy_id": "POL-001",
    "name": "data_residency",
    "status": "active",
    "version": "1.0",
    "created_at": "2026-07-01T10:00:00Z"
}

# Evaluate policy
POST /api/v1/policies/evaluate
Request:
{
    "policy_name": "data_residency",
    "resource_type": "s3_bucket",
    "resource_config": {"name": "customer-data", "region": "us-east-1"}
}

Response:
{
    "decision": "allow",
    "violations": [],
    "evaluated_at": "2026-07-01T10:00:00Z"
}
```

### Compliance Scanning API

```python
# Run compliance scan
POST /api/v1/compliance/scan
Request:
{
    "framework": "GDPR",
    "scope": "production",
    "controls": ["data_encryption", "access_control"]
}

Response:
{
    "scan_id": "SCAN-001",
    "status": "running",
    "estimated_completion": "2026-07-01T10:05:00Z"
}

# Get scan results
GET /api/v1/compliance/scan/{scan_id}
Response:
{
    "scan_id": "SCAN-001",
    "status": "completed",
    "controls_evaluated": 50,
    "controls_passed": 45,
    "compliance_score": 0.90,
    "violations": [...]
}
```

### Exception Management API

```python
# Request exception
POST /api/v1/exceptions
Request:
{
    "policy": "encryption_at_rest",
    "resource": "legacy-database-prod",
    "business_justification": "Migration planned for Q3",
    "risk_level": "medium",
    "compensating_controls": ["network_isolation"]
}

Response:
{
    "exception_id": "EXC-001",
    "status": "pending_approval",
    "risk_score": 0.65,
    "created_at": "2026-07-01T10:00:00Z"
}

# Approve exception
PUT /api/v1/exceptions/{exception_id}/approve
Request:
{
    "approver": "security_manager",
    "notes": "Approved with 90-day limit"
}

Response:
{
    "exception_id": "EXC-001",
    "status": "approved",
    "expiry_date": "2026-09-29"
}
```

## Data Models

### Policy Model

```python
class Policy:
    policy_id: str
    name: str
    description: str
    type: str  # technical, administrative, physical
    language: Optional[str]  # rego, cedar, custom_dsl
    rules: List[PolicyRule]
    effective_date: date
    review_date: Optional[date]
    owner: str
    status: str  # draft, active, deprecated
    version: str
    created_at: datetime
    updated_at: datetime
```

### Policy Decision Model

```python
class PolicyDecision:
    decision_id: str
    decision: str  # allow, deny
    policy: str
    resource_type: str
    resource_config: Dict
    violations: List[Violation]
    remediation: List[RemediationSuggestion]
    evaluated_at: datetime
```

### Exception Model

```python
class PolicyException:
    exception_id: str
    policy: str
    resource: str
    business_justification: str
    requested_by: str
    risk_level: str
    risk_score: float
    compensating_controls: List[str]
    status: str  # pending_approval, approved, denied, expired
    approver: Optional[str]
    approval_date: Optional[datetime]
    expiry_date: Optional[date]
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: policy-automation-service
  namespace: governance-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: policy-automation-service
  template:
    metadata:
      labels:
        app: policy-automation-service
    spec:
      containers:
      - name: policy-automation
        image: your-registry/policy-automation-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Policy evaluation metrics
policy_evaluations_counter = Counter(
    'governance_policy_evaluations_total',
    'Total policy evaluations',
    ['policy_name', 'decision']
)

policy_evaluation_duration = Histogram(
    'governance_policy_evaluation_duration_seconds',
    'Policy evaluation duration',
    ['policy_name'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0]
)

# Compliance metrics
compliance_scans_counter = Counter(
    'governance_compliance_scans_total',
    'Total compliance scans',
    ['framework', 'status']
)

compliance_score_gauge = Gauge(
    'governance_compliance_score',
    'Current compliance score',
    ['framework']
)

# Exception metrics
exceptions_counter = Counter(
    'governance_exceptions_total',
    'Total policy exceptions',
    ['status', 'risk_level']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Policy Automation",
    "panels": [
      {
        "title": "Policy Evaluations",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(governance_policy_evaluations_total[5m])",
            "legendFormat": "{{policy_name}} - {{decision}}"
          }
        ]
      },
      {
        "title": "Compliance Score",
        "type": "gauge",
        "targets": [
          {
            "expr": "governance_compliance_score",
            "legendFormat": "{{framework}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: policy_alerts
  rules:
  - alert: ComplianceScoreLow
    expr: governance_compliance_score < 0.8
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Compliance score below 80%"
      
  - alert: PolicyEvaluationErrors
    expr: rate(governance_policy_evaluations_total{decision="error"}[5m]) > 0.01
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High policy evaluation error rate"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestPolicyEvaluation:
    def test_allow_decision(self, policy_engine):
        result = policy_engine.evaluate(
            resource_type="s3_bucket",
            resource_config={"region": "us-east-1"},
            policy_name="data_residency",
        )
        
        assert result.decision == "allow"
        assert len(result.violations) == 0
    
    def test_deny_decision(self, policy_engine):
        result = policy_engine.evaluate(
            resource_type="s3_bucket",
            resource_config={"region": "ap-southeast-1"},
            policy_name="data_residency",
        )
        
        assert result.decision == "deny"
        assert len(result.violations) > 0
```

### Integration Tests

```python
class TestEndToEndPolicyAutomation:
    async def test_compliance_scan_flow(self, policy_system):
        # Run compliance scan
        scan = await policy_system.run_scan(
            framework="GDPR",
            scope="production",
        )
        
        assert scan.scan_id is not None
        assert scan.status == "completed"
        
        # Get results
        results = await policy_system.get_scan_results(scan.scan_id)
        assert results.controls_evaluated > 0
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class PolicyAutomationUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def evaluate_policy(self):
        self.client.post("/api/v1/policies/evaluate", json={
            "policy_name": "data_residency",
            "resource_type": "s3_bucket",
            "resource_config": {"region": "us-east-1"},
        })
    
    @task(5)
    def get_compliance_score(self):
        self.client.get("/api/v1/compliance/score/GDPR")
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/policies", methods=["POST"])
@app.route("/api/v2/policies", methods=["POST"])
async def create_policy():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await create_policy_v2()
    return await create_policy_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **OPA**: Open Policy Agent - general-purpose policy engine
- **Rego**: Policy language for OPA
- **Cedar**: Policy language developed by AWS
- **Policy-as-Code**: Machine-readable policy definitions
- **Compensating Control**: Alternative control when primary control cannot be implemented
- **Attestation**: Formal declaration of compliance
- **Policy Drift**: Deviation from policy requirements over time
- **Exception Management**: Process for handling policy deviations
- **Compliance Score**: Measure of adherence to policies
- **Audit Evidence**: Documentation proving policy compliance

## Changelog

### Version 2.0.0 (2026-07-01)
- Added policy-as-code support
- Implemented continuous compliance checking
- Enhanced exception management
- Added attestation campaigns

### Version 1.5.0 (2026-01-15)
- Added regulatory mapping
- Implemented policy versioning
- Enhanced audit evidence generation

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic policy management
- Manual compliance checking

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def evaluate_policy(
    policy_name: str,
    resource_type: str,
    resource_config: Dict,
) -> PolicyDecision:
    """Evaluate a policy against a resource.
    
    Args:
        policy_name: Name of the policy.
        resource_type: Type of resource.
        resource_config: Resource configuration.
    
    Returns:
        Policy decision.
    
    Raises:
        EvaluationError: If evaluation fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Policy Automation Platform

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
