---
name: "policy-engine"
category: "zero-trust"
version: "1.0.0"
tags: ["zero-trust", "policy-engine", "ABAC", "RBAC", "OPA"]
---

# Policy Engine for Zero Trust

## Overview

The Policy Engine module provides a comprehensive attribute-based access control (ABAC) and role-based access control (RBAC) framework purpose-built for zero trust architectures. It implements the two critical architectural components — Policy Decision Points (PDP) and Policy Enforcement Points (PEP) — that evaluate complex, context-rich authorization decisions in real-time. Policies are authored in a declarative language compatible with OPA/Rego, enabling fine-grained control over who can access what resources, under which conditions, and with what constraints. The engine serves as the central brain of a zero trust access fabric, replacing perimeter-based trust with continuous, attribute-driven evaluation.

The engine supports multi-dimensional policy evaluation where access decisions consider user attributes (role, department, clearance level, risk score), resource attributes (classification, owner, sensitivity, environment), action attributes (read, write, delete, admin, share), and environmental attributes (time of day, location, device trust level, network zone, threat level). This attribute-rich approach enables policies that are impossible to express in simple RBAC — such as "allow finance users to access payment records only during business hours from managed devices with a trust score above 0.8, but escalate to require MFA if the request originates from outside the corporate network."

Policy simulation and conflict resolution are critical capabilities for large-scale deployments where hundreds or thousands of policies interact. The engine provides dry-run evaluation that shows exactly which policies would fire for a given request, detects conflicting rules (allow vs deny on the same resource), identifies shadowed rules (a higher-priority rule makes a lower-priority rule unreachable), and suggests resolutions. Policy version control ensures that every change is tracked, diffable, and rollback-capable, supporting compliance requirements for audit trails of all authorization logic changes.

Compliance mapping translates regulatory requirements (GDPR, HIPAA, SOX, PCI DSS, NIST 800-53) into enforceable policies and generates compliance reports showing which policies satisfy which regulatory controls. This bridges the gap between security policy authors who understand regulations and engineers who implement access controls. The engine also supports policy-as-code workflows, enabling CI/CD integration where policy changes go through code review, automated testing, and staged rollouts — the same rigor applied to application code.

## Core Capabilities

- **ABAC with multi-dimensional evaluation**: Evaluate access requests across subject, resource, action, and environment attribute dimensions with nested condition logic
- **RBAC with hierarchical role inheritance**: Define role hierarchies where child roles inherit parent permissions, with static and dynamic separation-of-duty constraints
- **OPA/Rego policy authoring**: Write policies in Rego — a purpose-built policy language with data-flow reasoning, partial evaluation, and built-in support for JSON, YAML, and structured data
- **Policy decision points (PDP)**: Centralized evaluation service that receives authorization requests and returns permit/deny/indeterminate decisions with full evaluation traces
- **Policy enforcement points (PEP)**: Sidecar or inline interceptors that enforce PDP decisions at API gateways, service meshes, application middleware, and network boundaries
- **Policy simulation and dry-run**: Evaluate hypothetical requests against the current policy set without enforcing, detecting conflicts, shadowed rules, and unintended access grants
- **Policy version control and rollback**: Git-integrated policy storage with full diff history, branch-based policy testing, and instant rollback to any prior version
- **Compliance mapping**: Tag policies to regulatory controls (GDPR Art. 25, HIPAA §164.312, SOX §802, PCI DSS Req. 7) and generate automated compliance reports
- **Conflict resolution**: Priority-based, specificity-based, and most-restrictive resolution strategies for handling overlapping or contradictory policy rules
- **Decision audit logging**: Capture complete evaluation traces for every authorization decision, including which rules matched, which conditions evaluated true/false, and why the final decision was reached

## Usage Examples

### Initializing the Policy Engine

```python
from policy_engine import PolicyEngine, Policy, Attribute, EvaluationContext

# Initialize the policy engine with zero-trust defaults
engine = PolicyEngine(
    engine_id="authz-pdp-001",
    default_effect="deny",          # Zero trust: deny everything not explicitly permitted
    audit_logging=True,             # Capture every decision for compliance
    conflict_resolution="most_specific",  # Most specific matching policy wins
    max_evaluation_depth=10,        # Prevent infinite policy recursion
    evaluation_timeout_ms=50,       # Fail-closed if evaluation takes too long
)

# Load policies from a Rego bundle
engine.load_policy_bundle("./policies/rego-bundle.tar.gz")

# Or load individual policy files
engine.load_rego_policy(
    policy_id="data-access-policy",
    rego_file="./policies/data_access.rego",
)

print(f"Engine {engine.engine_id} initialized with {engine.policy_count} policies")
```

### Defining ABAC Policies

```python
# Create an ABAC policy for finance payment access
finance_policy = engine.create_policy(
    policy_id="allow-finance-read-payments",
    description="Allow finance department to read payment records during business hours from managed devices",
    effect="permit",
    priority=100,
    target={
        "subject.role": "finance_analyst",
        "subject.department": "finance",
        "resource.type": "payment_record",
        "action": "read",
    },
    conditions=[
        {"attribute": "environment.time_of_day", "operator": "in_range", "value": "08:00-18:00"},
        {"attribute": "environment.day_of_week", "operator": "in", "value": ["monday","tuesday","wednesday","thursday","friday"]},
        {"attribute": "device.trust_score", "operator": "gte", "value": 0.7},
        {"attribute": "device.managed", "operator": "equals", "value": True},
        {"attribute": "network.zone", "operator": "in", "value": ["corporate", "vpn"]},
    ],
    obligations=[
        {"type": "audit_log", "detail": "finance_payment_read"},
        {"type": "mask_fields", "fields": ["card_number", "cvv", "account_number"]},
        {"type": "rate_limit", "max_requests": 100, "window_seconds": 3600},
    ],
)

# Create a deny policy for cross-department access
deny_cross_dept = engine.create_policy(
    policy_id="deny-cross-department-access",
    description="Deny access to resources owned by a different department unless explicitly permitted",
    effect="deny",
    priority=50,
    target={
        "action": "read",
    },
    conditions=[
        {"attribute": "subject.department", "operator": "not_equals", "value": "${resource.owner}"},
        {"attribute": "resource.classification", "operator": "in", "value": ["confidential", "restricted"]},
    ],
)

# Create an escalation policy that requires MFA for high-risk scenarios
mfa_escalation = engine.create_policy(
    policy_id="require-mfa-high-risk",
    description="Require MFA for access when risk score is elevated",
    effect="permit",
    priority=200,  # Higher priority overrides base permits
    target={
        "action": "write",
        "resource.classification": "restricted",
    },
    conditions=[
        {"attribute": "auth.mfa_verified", "operator": "equals", "value": True},
        {"attribute": "risk.score", "operator": "gte", "value": 0.5},
    ],
    obligations=[
        {"type": "audit_log", "detail": "mfa_escalation_triggered"},
        {"type": "alert", "channel": "security-ops", "severity": "high"},
    ],
)

print(f"Created {len(engine.list_policies())} policies")
```

### RBAC Role Hierarchies

```python
# Define role hierarchy with inheritance
engine.define_role_hierarchy({
    "employee": {
        "permissions": ["read:public_docs", "read:own_profile"],
        "inherits_from": [],
    },
    "analyst": {
        "permissions": ["read:reports", "write:own_reports", "read:analytics"],
        "inherits_from": ["employee"],
    },
    "finance_analyst": {
        "permissions": ["read:payment_records", "read:invoices", "write:expense_reports"],
        "inherits_from": ["analyst"],
    },
    "finance_manager": {
        "permissions": ["approve:expenses", "read:all_finance", "write:budget_plans"],
        "inherits_from": ["finance_analyst"],
        "constraints": {
            "separation_of_duty": ["auditor"],  # Cannot also hold auditor role
            "max_concurrent_sessions": 3,
        },
    },
    "auditor": {
        "permissions": ["read:all_records", "read:audit_logs", "write:audit_findings"],
        "inherits_from": ["analyst"],
        "constraints": {
            "separation_of_duty": ["finance_manager"],
            "time_restricted": {"allowed_hours": "09:00-17:00", "timezone": "UTC"},
        },
    },
})

# Check effective permissions for a role
effective = engine.get_effective_permissions("finance_manager")
print(f"Finance Manager has {len(effective)} effective permissions:")
for perm in sorted(effective):
    print(f"  - {perm}")
```

### Evaluating Access Requests

```python
# Evaluate an access request with full context
evaluation = engine.evaluate(
    subject=Attribute(
        principal="user:alice@corp.com",
        attributes={
            "role": "finance_analyst",
            "department": "finance",
            "clearance_level": 3,
            "risk_score": 0.2,
        },
    ),
    resource=Attribute(
        principal="resource:payment-record-001",
        attributes={
            "type": "payment_record",
            "classification": "confidential",
            "owner": "finance",
            "sensitivity": "high",
        },
    ),
    action="read",
    environment={
        "time_of_day": "10:30",
        "day_of_week": "monday",
        "ip_address": "10.0.1.50",
        "device_trust_score": 0.85,
        "device_managed": True,
        "network_zone": "corporate",
        "auth.mfa_verified": True,
    },
)

print(f"Evaluation Result:")
print(f"  Decision: {evaluation.decision}")            # permit or deny
print(f"  Matched policies: {evaluation.matched_policies}")
print(f"  Obligations: {evaluation.obligations}")
print(f"  Evaluation time: {evaluation.evaluation_time_ms}ms")

# Access the full evaluation trace for debugging
for step in evaluation.trace:
    print(f"  [{step.rule_id}] {step.condition} -> {step.result}")
```

### Policy Simulation and Dry-Run

```python
# Simulate a request without enforcing — useful for testing before deployment
simulation = engine.simulate(
    subject_attributes={"role": "finance_analyst", "department": "finance"},
    resource_attributes={"type": "payment_record", "classification": "confidential"},
    action="read",
    environment={"time_of_day": "22:00", "device_managed": True},  # After hours
)

print(f"Simulation (after-hours access attempt):")
print(f"  Would allow: {simulation.would_allow}")
print(f"  Blocking policies: {simulation.blocking_policies}")
print(f"  Reason: {simulation.deny_reason}")

# Batch simulation across multiple scenarios
scenarios = [
    {"subject": {"role": "analyst"}, "resource": {"type": "payment_record"}, "action": "read",
     "env": {"time_of_day": "10:00", "device_managed": True}},
    {"subject": {"role": "analyst"}, "resource": {"type": "payment_record"}, "action": "read",
     "env": {"time_of_day": "22:00", "device_managed": False}},
    {"subject": {"role": "finance_manager"}, "resource": {"type": "budget_plan"}, "action": "write",
     "env": {"time_of_day": "14:00", "device_managed": True}},
]

results = engine.batch_simulate(scenarios)
for i, result in enumerate(results):
    status = "ALLOW" if result.would_allow else "DENY"
    print(f"  Scenario {i+1}: {status} ({result.matched_policy_count} policies matched)")
```

### OPA/Rego Policy Authoring

```python
# Write policies in Rego for complex attribute-based logic
rego_policy = """
package authz

default allow = false

# Allow finance analysts to read payment records during business hours
allow {
    input.subject.role == "finance_analyst"
    input.subject.department == "finance"
    input.resource.type == "payment_record"
    input.action == "read"
    business_hours
    managed_device
    trusted_network
}

# Allow managers to approve expenses
allow {
    input.subject.role == "finance_manager"
    input.resource.type == "expense_report"
    input.action == "approve"
    input.auth.mfa_verified == true
}

# Deny access to terminated employees
deny {
    input.subject.status == "terminated"
}

# Helper rules
business_hours {
    time.parse_rfc3339_ns(input.environment.timestamp) >= time.parse_rfc3339_ns("2024-01-01T08:00:00Z")
    time.parse_rfc3339_ns(input.environment.timestamp) <= time.parse_rfc3339_ns("2024-01-01T18:00:00Z")
}

managed_device {
    input.device.managed == true
    input.device.trust_score >= 0.7
}

trusted_network {
    input.network.zone == "corporate"
}

# Obligations for permitted access
obligations[result] {
    allow
    result := {"type": "audit_log", "detail": "data_access"}
}

obligations[result] {
    allow
    input.resource.classification == "confidential"
    result := {"type": "mask_fields", "fields": ["ssn", "card_number"]}
}
"""

# Register the Rego policy
engine.register_rego_policy(
    policy_id="data-access-rego",
    rego_source=rego_policy,
    description="OPA/Rego data access policy with business hour and device constraints",
)
```

### Policy Version Control and Diff

```python
# Policy changes are version-controlled automatically
change = engine.commit_policy_change(
    policy_id="allow-finance-read-payments",
    author="alice@corp.com",
    description="Added network zone restriction for PCI DSS compliance",
    change_type="update",
    compliance_tags=["PCI-DSS-Req-7.2.1"],
)

# View the diff between versions
diff = engine.get_policy_diff(
    policy_id="allow-finance-read-payments",
    from_version=3,
    to_version=4,
)

print(f"Policy diff (v3 -> v4):")
for line in diff.lines:
    print(f"  {line}")

# Rollback to a previous version if needed
engine.rollback_policy(
    policy_id="allow-finance-read-payments",
    target_version=3,
    reason="Version 4 introduced unintended cross-department access",
    approved_by="ciso@corp.com",
)

# List all versions with metadata
versions = engine.list_policy_versions("allow-finance-read-payments")
for v in versions:
    print(f"  v{v.version}: {v.description} ({v.author}, {v.created_at})")
```

### Compliance Mapping and Reporting

```python
# Tag policies with compliance requirements
engine.tag_compliance(
    policy_id="allow-finance-read-payments",
    controls=[
        {"framework": "PCI-DSS", "requirement": "Req 7.2.1", "description": "Access to cardholder data restricted to need-to-know"},
        {"framework": "SOX", "requirement": "§802", "description": "Audit trail for financial record access"},
        {"framework": "NIST-800-53", "requirement": "AC-6", "description": "Least privilege"},
    ],
)

# Generate compliance report
report = engine.generate_compliance_report(
    framework="PCI-DSS",
    scope="all",
    include_evidence=True,
)

print(f"Compliance Report: PCI-DSS")
print(f"  Total controls: {report.total_controls}")
print(f"  Covered: {report.covered_controls}")
print(f"  Gaps: {report.gap_count}")
for gap in report.gaps:
    print(f"    - {gap.control}: {gap.description}")

# Check which policies cover a specific control
policies = engine.find_policies_by_control("HIPAA", "§164.312(a)(1)")
print(f"\nPolicies covering HIPAA §164.312(a)(1):")
for p in policies:
    print(f"  - {p.policy_id}: {p.effect} (priority {p.priority})")
```

### Conflict Detection and Resolution

```python
# Detect conflicts between policies
conflicts = engine.detect_conflicts()

print(f"Found {len(conflicts)} policy conflicts:")
for conflict in conflicts:
    print(f"\n  Conflict: {conflict.description}")
    print(f"    Policy A: {conflict.policy_a_id} ({conflict.policy_a_effect})")
    print(f"    Policy B: {conflict.policy_b_id} ({conflict.policy_b_effect})")
    print(f"    Severity: {conflict.severity}")
    print(f"    Resolution: {conflict.suggested_resolution}")

# Auto-resolve conflicts using the configured strategy
resolution_result = engine.resolve_conflicts(
    strategy="most_specific",  # or "most_restrictive", "priority_based"
    dry_run=True,  # Preview changes before applying
)

print(f"\nAuto-resolution preview:")
for action in resolution_result.planned_actions:
    print(f"  - {action}")

# Manually override a conflict resolution
engine.override_conflict(
    conflict_id=conflicts[0].conflict_id,
    winning_policy=conflicts[0].policy_a_id,
    reason="Business justification: finance access required for quarterly audit",
    approved_by="ciso@corp.com",
)
```

### Audit Logging and Decision Traces

```python
# Query the audit log for recent decisions
audit_entries = engine.query_audit_log(
    time_range="24h",
    filters={
        "subject.department": "finance",
        "decision": "deny",
        "resource.type": "payment_record",
    },
    limit=50,
)

print(f"Denied finance payment access in last 24h: {len(audit_entries)}")
for entry in audit_entries:
    print(f"  {entry.timestamp} | {entry.subject} | {entry.resource} | {entry.deny_reason}")

# Get full evaluation trace for a specific decision
trace = engine.get_decision_trace(decision_id="dec-2024-01-15-001234")
print(f"\nDecision Trace:")
print(f"  Request: {trace.subject} -> {trace.resource} ({trace.action})")
print(f"  Decision: {trace.decision}")
print(f"  Evaluation steps:")
for step in trace.evaluation_steps:
    marker = "+" if step.matched else "-"
    print(f"    [{marker}] Rule {step.rule_id}: {step.condition} = {step.result}")
print(f"  Total evaluation time: {trace.evaluation_time_ms}ms")

# Export audit logs for external SIEM integration
engine.export_audit_logs(
    format="json",
    output_path="/var/log/policy-engine/audit.jsonl",
    time_range="7d",
    include_traces=True,
)
```

### Policy PDP/PEP Architecture

```python
# Policy Decision Point (PDP) — centralized evaluation service
pdp = engine.create_pdp(
    pdp_id="pdp-primary",
    listen_address="0.0.0.0",
    listen_port=8443,
    tls_cert="/etc/policy-engine/tls/server.crt",
    tls_key="/etc/policy-engine/tls/server.key",
    cache_ttl_seconds=30,
    max_concurrent_evaluations=1000,
)

# Policy Enforcement Point (PEP) — sidecar that intercepts requests
pep = engine.create_pep(
    pep_id="pep-api-gateway",
    pdp_endpoint="https://pdp-primary:8443/evaluate",
    mode="sidecar",  # or "inline", "middleware"
    fail_open=False,  # Deny if PDP is unreachable (zero trust default)
    cache_enabled=True,
    cache_ttl_seconds=10,
    timeout_ms=50,
)

# Register PEP with the PDP
pdp.register_pep(pep)

# PEP enforces decisions at the API gateway
pep.intercept_route(
    route="POST /api/v1/payments",
    resource_extractor="request.body.merchant_id",
    action_map={"POST": "create", "GET": "read", "PUT": "update", "DELETE": "delete"},
)

print(f"PDP {pdp.pdp_id} serving {len(pdp.registered_peps)} PEPs")
```

## Best Practices

- **Default deny with explicit permits**: Always set the engine default effect to `deny`. Only create explicit permit policies for known, authorized access patterns. This ensures that any request without a matching policy is rejected — the fundamental zero trust principle.
- **Use least-privilege policy granularity**: Author policies that grant the minimum access needed. Avoid wildcard subjects or overly broad resource patterns. A policy allowing "finance users to read payment records" is far safer than "finance users to access all records."
- **Version control all policies as code**: Store policy definitions in a Git repository with the same rigor as application code. Every policy change must include a description of why the change was made, who approved it, and what compliance requirement it addresses.
- **Simulate before deploying**: Always run policy simulation in dry-run mode before deploying new or modified policies. Check for conflicts, shadowed rules, and unintended access grants that could create vulnerabilities or compliance gaps.
- **Implement conflict resolution consistently**: Define a clear conflict resolution strategy (most specific, most restrictive, or priority-based) and apply it uniformly across all policies. Document the strategy so policy authors understand how overlapping rules are resolved.
- **Map every policy to compliance requirements**: Tag each policy with the regulatory control it satisfies. This enables automated compliance reporting and ensures every access control has a documented business and regulatory justification.
- **Audit every decision with full traces**: Enable comprehensive audit logging for all policy evaluations. The audit log must capture the complete evaluation trace — which rules were checked, which matched, and why the final decision was reached — for forensic and compliance purposes.
- **Review policies on a regular cadence**: Schedule quarterly policy reviews to remove stale rules, update conditions based on changing requirements, verify that policies still align with current compliance mandates, and test that conflict resolution is behaving as expected.
- **Test policies in CI/CD pipelines**: Integrate policy simulation into your CI pipeline so every policy change is automatically tested against a corpus of known-good and known-bad access requests before merge.
- **Use obligation policies for post-decision actions**: Beyond permit/deny, encode obligations like audit logging, field masking, rate limiting, and alerting. These ensure that even permitted access follows organizational data handling requirements.

## Related Modules

- [security-framework](../security-framework/GROK.md) — Trust engine and zero trust architecture foundation
- [identity-verification](../identity-verification/GROK.md) — Identity verification, proofing, and lifecycle management
- [micro-segmentation](../micro-segmentation/GROK.md) — Network-level policy enforcement and segmentation
- [continuous-auth](../continuous-auth/GROK.md) — Session risk assessment and behavioral signals
- [data-classification](../data-classification/GROK.md) — Data sensitivity labeling and classification policies
- [threat-intelligence](../threat-intelligence/GROK.md) — Real-time threat feeds for risk-based policy adjustments
