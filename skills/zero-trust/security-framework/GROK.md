---
name: "security-framework"
category: "zero-trust"
version: "1.0.0"
tags: ["zero-trust", "security-framework", "NIST", "architecture"]
---

# Zero Trust Security Framework

## Overview

The Zero Trust Security Framework module provides a comprehensive implementation
of zero trust architecture (ZTA) principles aligned with NIST SP 800-207. This
framework eliminates the traditional perimeter-based security model and replaces
it with an identity-centric, least-privilege approach where every access request
is verified regardless of origin. The module implements policy decision points
(PDP), policy enforcement points (PEP), and trust engines that evaluate
contextual signals in real-time to make granular access decisions.

At its core, this framework treats every network location as hostile. It
continuously validates the integrity and posture of devices, users, and workloads
before granting access to resources. The trust engine aggregates signals from
identity verification, device health, network location, and behavioral analytics
to compute dynamic trust scores. These scores drive policy decisions that are
enforced at micro-perimeters around each resource, ensuring that access is always
justified by current conditions rather than historical trust assumptions.

The framework supports phased adoption through maturity models, allowing
organizations to transition incrementally from legacy VPN-based access to full
zero trust. It provides assessment tools for measuring current security posture
against NIST guidelines, gap analysis capabilities, and implementation roadmaps.
Integration with existing IAM, SIEM, and network infrastructure ensures that
zero trust principles can be layered onto current investments without wholesale
replacement.

## Core Capabilities

- NIST SP 800-207 aligned zero trust architecture with configurable trust
  evaluation pipelines
- Policy Decision Point (PDP) and Policy Enforcement Point (PEP) lifecycle
  management
- Dynamic trust scoring engine with multi-signal aggregation and decay functions
- Identity-centric access model with continuous posture assessment
- Micro-perimeter definition and resource classifier configuration
- Security posture assessment with maturity gap analysis and remediation
  recommendations
- Real-time policy enforcement with deny-by-default and least-privilege
  enforcement
- Integration adapters for legacy VPN, proxy, and API gateway infrastructure

## Architecture Deep Dive

The zero trust architecture consists of three primary planes:

**Control Plane** — The control plane houses the Policy Decision Point (PDP)
and Policy Administration Point (PAP). The PDP evaluates every access request
against the current policy set, trust scores, and contextual signals. The PAP
provides the interface for administrators to author, version, and deploy policies
across the enforcement infrastructure.

**Data Plane** — The data plane contains the Policy Enforcement Points (PEP)
deployed at each resource boundary. PEPs intercept all access requests, forward
them to the PDP for evaluation, and enforce the resulting decision. PEPs operate
as lightweight proxies, API gateways, or network functions depending on the
resource type.

**Management Plane** — The management plane handles trust signal collection,
device health attestation, identity provider integration, and telemetry
aggregation. It feeds continuous signals to the PDP and maintains the global
view of security posture across all protected resources.

Trust evaluation follows a pipeline architecture:

1. Signal Collection — Gather raw signals from identity, device, network sources
2. Signal Validation — Verify freshness, authenticity, and completeness
3. Trust Scoring — Apply configured algorithm to compute composite score
4. Policy Evaluation — Match request against policy set using trust score
5. Decision Output — Produce allow/deny/step-up decision with audit trail

## Usage Examples

```python
from security_framework import ZeroTrustEngine, TrustSignal, ResourceType

# Initialize the zero trust engine
engine = ZeroTrustEngine(
    policy_store="postgresql://localhost/zta_policies",
    trust_algorithm="weighted_sum",
    default_deny=True
)

# Register a protected resource
resource = engine.register_resource(
    resource_id="api-payments-001",
    resource_type=ResourceType.API_ENDPOINT,
    classification="confidential",
    owner_team="payments",
    required_trust_level=0.85
)

# Evaluate a trust decision
signals = [
    TrustSignal(signal_type="identity", value="verified_mfa", weight=0.3),
    TrustSignal(signal_type="device_health", value="compliant", weight=0.25),
    TrustSignal(signal_type="network_location", value="corporate", weight=0.2),
    TrustSignal(signal_type="behavior", value="normal", weight=0.25)
]

decision = engine.evaluate_access(
    subject="user:alice@corp.com",
    resource="api-payments-001",
    action="read",
    context_signals=signals
)

print(f"Access: {decision.granted}, Trust Score: {decision.trust_score:.2f}")
```

```python
# Configure a micro-perimeter around sensitive resources
perimeter = engine.define_micro_perimeter(
    perimeter_id="payments-zone",
    resources=["api-payments-*", "db-payments-*"],
    enforcement_mode="strict",
    default_action="deny",
    exceptions=[
        {"subject_pattern": "service:monitoring-*", "actions": ["read_metrics"]}
    ]
)

# Run posture assessment
assessment = engine.assess_posture(
    scope="payments-zone",
    framework="NIST_800_207",
    include_recommendations=True
)

for gap in assessment.gaps:
    print(f"[{gap.severity}] {gap.description}")
    print(f"  Remediation: {gap.remediation}")
```

```python
# Add policy rules for fine-grained access control
engine.add_policy_rule(
    rule_id="allow-monitoring-read",
    subject_pattern="service:monitoring-*",
    resource_pattern="api-payments-*",
    action="read",
    effect="allow",
    priority=500,
)

# Review audit log for compliance
audit_log = engine.get_audit_log(subject="user:alice@corp.com")
for entry in audit_log:
    print(f"{entry.request_id}: {entry.decision.value} - {entry.reason}")
```

## Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| policy_store | str | in_memory | Backend for policy storage |
| trust_algorithm | str | weighted_sum | Trust scoring algorithm |
| default_deny | bool | True | Default action for unmatched requests |
| trust_decay_rate | float | 0.05 | Per-second trust score decay |
| max_session_duration | int | 3600 | Maximum session lifetime in seconds |
| signal_staleness | float | 300.0 | Max age for trust signals in seconds |

Trust algorithm options:

- **weighted_sum** — Weighted combination of all signals, normalized
- **minimum_threshold** — Lowest individual signal score becomes the trust score
- **weighted_average** — Simple average across all signal weights
- **mandatory_signals** — Requires specific signal types, fails if absent

## Implementation Guide

Phase 1: Identity Foundation

Start by integrating your identity provider (IdP) with the trust engine. Map
existing MFA, SSO, and directory services to trust signal types. Establish
baseline trust scores for authenticated users.

Phase 2: Device Posture

Deploy device health attestation agents. Configure compliance checks for OS
version, disk encryption, antivirus status, and patch level. Feed device health
signals into the trust engine.

Phase 3: Network Segmentation

Define micro-perimeters around critical assets. Configure PEPs at resource
boundaries. Implement deny-by-default network policies with explicit allow rules.

Phase 4: Continuous Monitoring

Enable behavioral analytics and session monitoring. Configure anomaly detection
thresholds. Implement step-up authentication triggers for elevated risk.

Phase 5: Optimization

Tune trust scoring weights based on operational feedback. Refine policy rules to
reduce false positives. Automate posture assessment and remediation workflows.

## Best Practices

- **Deny-by-default**: Always start with a deny policy and explicitly grant
  access based on trust signals. This ensures that unknown or unauthenticated
  requests are blocked by default.

- **Least privilege per session**: Grant the minimum permissions needed for the
  specific session and action, not broad role-based access. Re-evaluate on every
  sensitive operation.

- **Continuous verification**: Trust is not a one-time decision. Continuously
  monitor session health, device posture, and behavioral signals throughout the
  access lifetime.

- **Segment resources by classification**: Define micro-perimeters around
  resources based on their sensitivity classification. Confidential and
  restricted resources require higher trust thresholds.

- **Fail closed**: When trust signals are unavailable or the engine cannot compute
  a score, default to deny. Never grant access on insufficient information.

- **Log every decision**: Maintain an immutable audit log of every trust
  evaluation, including all input signals and the final decision. This supports
  forensic analysis and compliance.

- **Decouple policy from enforcement**: Authorize policies in a centralized PDP
  but enforce them at distributed PEPs. This allows consistent policy evaluation
  across heterogeneous infrastructure.

- **Adopt incrementally**: Use the maturity model to phase in zero trust. Start
  with identity verification, then layer on device posture, network segmentation,
  and continuous monitoring.

## Troubleshooting

Common issues and resolutions:

**Trust score always zero** — Check that signals are not stale. Default
staleness threshold is 300 seconds. Verify signal validators are registered
for each signal type used.

**Access denied despite valid credentials** — The trust score may be below
the resource's required_trust_level. Check device health signals and network
location signals which often carry significant weight.

**Step-up authentication loop** — If the step-up method does not increase the
trust score above threshold, the session will repeatedly request step-up.
Verify the step-up method contributes to the trust score via signal validators.

**Performance degradation at scale** — Trust computation is O(n) in signal
count. For high-throughput scenarios, enable the score cache and tune the
cache TTL based on session volatility.

## Related Modules

- [identity-verification](../identity-verification/GROK.md) — Multi-factor and
  biometric authentication pipelines
- [micro-segmentation](../micro-segmentation/GROK.md) — Network
  micro-segmentation policies and SDN controls
- [continuous-auth](../continuous-auth/GROK.md) — Session monitoring and
  behavioral analytics
- [policy-engine](../policy-engine/GROK.md) — ABAC/RBAC policy authoring and
  enforcement

---

## Advanced Configuration

### Trust Engine Tuning

```python
from security_framework import TrustEngineConfig

config = TrustEngineConfig(
    trust_algorithm="weighted_sum",
    signal_weights={
        "identity": 0.30,
        "device_health": 0.25,
        "network_location": 0.20,
        "behavior": 0.25,
    },
    trust_decay_rate=0.05,
    signal_staleness_seconds=300,
    score_cache_ttl_seconds=30,
    max_evaluation_depth=10,
)
```

### Micro-Perimeter Configuration

```python
from security_framework import MicroPerimeter

perimeter = MicroPerimeter(
    perimeter_id="finance-zone",
    resources=["api-finance-*", "db-finance-*"],
    enforcement_mode="strict",
    default_action="deny",
    trust_threshold=0.85,
    step_up_methods=["fido2", "biometric"],
)
```

## Architecture Patterns

### Zero Trust Architecture

```
Access Request
    │
    ▼
┌──────────────┐
│ Policy       │── Evaluate against policy set
│ Decision     │
│ Point (PDP)  │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Policy       │── Enforce decision at resource boundary
│ Enforcement  │
│ Point (PEP)  │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Resource     │── Protected asset
└──────────────┘

Signal inputs to PDP:
- Identity verification status
- Device health score
- Network location
- Behavioral analytics
- Threat intelligence
```

### Trust Evaluation Pipeline

```
Signal Collection → Validation → Trust Scoring → Policy Evaluation → Decision
```

## Integration Guide

### IAM Integration

```python
from security_framework import IAMIntegration

iam = IAMIntegration(provider="azure_ad")
engine.register_signal_source("identity", iam)
```

### SIEM Integration

```python
from security_framework import SIEMIntegration

siem = SIEMIntegration(provider="splunk", endpoint="https://splunk:8088")
engine.export_decisions(siem)
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Trust score caching | 10x faster repeated evaluations |
| Signal batching | Reduce collection overhead |
| Policy pre-compilation | O(1) policy lookup |
| Async signal collection | Parallel signal gathering |

## Security Considerations

- **Fail closed**: Deny when signals unavailable
- **Immutable audit logs**: Tamper-proof decision records
- **Signal freshness**: Reject stale trust signals
- **Policy versioning**: Track all policy changes
- **Encryption**: TLS for all PDP-PEP communication

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Trust score always 0 | Signals stale | Check signal freshness settings |
| Access denied with valid creds | Device health failing | Check device compliance |
| Step-up auth loop | Method doesn't increase score | Configure step-up signal contribution |
| PDP latency high | Too many policies | Enable policy caching |

## API Reference

### ZeroTrustEngine

```python
class ZeroTrustEngine:
    def __init__(self, policy_store: str, trust_algorithm: str, default_deny: bool)
    def register_resource(self, resource_id: str, resource_type: ResourceType, classification: str, required_trust_level: float) -> Resource
    def evaluate_access(self, subject: str, resource: str, action: str, context_signals: list) -> TrustDecision
    def define_micro_perimeter(self, perimeter_id: str, resources: list, enforcement_mode: str, default_action: str, exceptions: list = None) -> MicroPerimeter
    def assess_posture(self, scope: str, framework: str, include_recommendations: bool = True) -> PostureAssessment
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class ResourceType(Enum):
    API_ENDPOINT = "api_endpoint"
    DATABASE = "database"
    FILE_SHARE = "file_share"
    WEB_APPLICATION = "web_application"

@dataclass
class TrustDecision:
    granted: bool
    trust_score: float
    reason: str
    step_up_required: bool
    audit_entry: dict

@dataclass
class TrustSignal:
    signal_type: str
    value: str
    weight: float
    timestamp: float
```

## Deployment Guide

### Installation

```bash
pip install security-framework
```

### Deployment Checklist

1. Deploy PDP with policy store
2. Deploy PEPs at resource boundaries
3. Configure signal sources
4. Set trust thresholds per resource
5. Enable audit logging
6. Test with synthetic requests

## Monitoring & Observability

```python
from security_framework import MetricsCollector

collector = MetricsCollector()
collector.counter("zta.access.total", count, tags={"decision": decision})
collector.histogram("zta.evaluation.duration_ms", duration)
collector.gauge("zta.trust.score", score, tags={"subject": subject})
collector.counter("zta.policy.violations", count)
```

## Testing Strategy

```python
import pytest
from security_framework import ZeroTrustEngine, TrustSignal

def test_deny_by_default():
    engine = ZeroTrustEngine(policy_store="memory", trust_algorithm="weighted_sum", default_deny=True)
    signals = [TrustSignal(signal_type="identity", value="unverified", weight=1.0)]
    decision = engine.evaluate_access("user:anon", "api-test", "read", signals)
    assert decision.granted is False
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added posture assessment | Run initial assessment |
| 2.0.0 | New trust algorithm | Reconfigure signal weights |

## Glossary

| Term | Definition |
|------|-----------|
| **PDP** | Policy Decision Point — evaluates access requests |
| **PEP** | Policy Enforcement Point — enforces PDP decisions |
| **ZTA** | Zero Trust Architecture |
| **Trust Score** | Composite score from multiple signals |
| **Micro-Perimeter** | Security boundary around individual resources |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with NIST SP 800-207 alignment
- PDP/PEP lifecycle management
- Dynamic trust scoring
- Micro-perimeter definition

## Contributing Guidelines

```bash
git clone https://github.com/example/security-framework.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Trust Signal Types

| Signal Type | Source | Weight Range | Freshness |
|------------|--------|-------------|-----------|
| Identity verification | IdP | 0.2-0.4 | 5 min |
| Device health | EDR/MDM | 0.15-0.3 | 15 min |
| Network location | Network | 0.1-0.25 | 1 min |
| Behavioral analytics | UEBA | 0.1-0.25 | 5 min |
| Threat intelligence | TI feeds | 0.05-0.15 | 1 hour |
| Location/geofence | GPS/IP | 0.05-0.15 | 5 min |

### NIST SP 800-207 Components

| Component | Description | Implementation |
|-----------|-------------|----------------|
| PDP | Policy Decision Point | Centralized evaluation |
| PEP | Policy Enforcement Point | Distributed enforcement |
| PAP | Policy Administration Point | Policy authoring UI |
| PIN | Policy Information Point | Signal collection |
| PA | Policy Administrator | PDP-PEP communication |

### Zero Trust Maturity Model

| Level | Description | Characteristics |
|-------|-------------|----------------|
| Traditional | Perimeter-based | VPN, static roles |
| Initial | Partial identity | Some MFA, basic segmentation |
| Advanced | Identity-centric | Continuous verification, micro-segmentation |
| Optimal | Fully zero trust | Dynamic policies, automated response |

### Trust Score Calculation Example

```python
# Weighted sum trust score
signals = {
    "identity_verified": 0.95,      # MFA completed
    "device_compliant": 0.85,       # EDR reports healthy
    "network_corporate": 0.80,      # On corporate network
    "behavior_normal": 0.90,        # No anomalies detected
}

weights = {
    "identity_verified": 0.30,
    "device_compliant": 0.25,
    "network_corporate": 0.20,
    "behavior_normal": 0.25,
}

trust_score = sum(signals[k] * weights[k] for k in signals)
# trust_score = 0.95*0.30 + 0.85*0.25 + 0.80*0.20 + 0.90*0.25
# trust_score = 0.285 + 0.2125 + 0.16 + 0.225 = 0.8825
```

### Micro-Perimeter Configuration

| Resource Classification | Required Trust | Step-Up Method | Timeout |
|------------------------|---------------|----------------|---------|
| Public | 0.0 | None | 24h |
| Internal | 0.5 | None | 8h |
| Confidential | 0.75 | MFA | 4h |
| Restricted | 0.85 | FIDO2 | 1h |
| Critical | 0.95 | Biometric | 30 min |

### Common Trust Evaluation Scenarios

| Scenario | Signals | Score | Decision |
|----------|---------|-------|----------|
| Corporate + MFA + healthy | All positive | 0.90 | Allow |
| VPN + password only | No device check | 0.65 | Step-up |
| Unknown device + public WiFi | Low trust | 0.35 | Deny |
| Personal device + compliant | Medium trust | 0.70 | Allow with restrictions |
| After-hours + unusual location | Anomaly detected | 0.45 | Step-up |

## Real-World Scenarios

### Scenario 1: Corporate Application Access

A remote employee attempts to access a financial application from a personal laptop
over a hotel Wi-Fi network. The trust engine evaluates the following signals:

```python
signals = [
    TrustSignal(signal_type="identity", value="verified_mfa", weight=0.30),
    TrustSignal(signal_type="device_health", value="unmanaged", weight=0.25),
    TrustSignal(signal_type="network_location", value="public_wifi", weight=0.20),
    TrustSignal(signal_type="behavior", value="normal", weight=0.25),
]
# Score: 0.30 + 0.08 + 0.06 + 0.225 = 0.665
# Required: 0.85 for financial application
# Decision: Step-up required
```

The engine triggers step-up authentication requiring FIDO2 verification. Upon
successful step-up, the trust score increases to 0.88 and access is granted
with a reduced session timeout of 1 hour and field masking on sensitive data.

### Scenario 2: Service-to-Service Communication

Two microservices communicate within a Kubernetes cluster. The payment service
calls the order service to retrieve order details. The trust engine evaluates
workload identity via SPIFFE/SPIRE:

```python
service_signals = [
    TrustSignal(signal_type="workload_identity", value="spiffe://corp/payment", weight=0.40),
    TrustSignal(signal_type="device_health", value="container_healthy", weight=0.20),
    TrustSignal(signal_type="network_location", value="cluster_internal", weight=0.20),
    TrustSignal(signal_type="policy_compliance", value="all_policies_met", weight=0.20),
]
# Score: 0.36 + 0.17 + 0.16 + 0.18 = 0.87
# Required: 0.75 for internal service call
# Decision: Allow
```

### Scenario 3: Privileged Admin Access

An administrator attempts to access production database consoles. The trust engine
enforces the highest trust threshold for critical resources:

```python
admin_signals = [
    TrustSignal(signal_type="identity", value="verified_fido2", weight=0.30),
    TrustSignal(signal_type="device_health", value="managed_compliant", weight=0.25),
    TrustSignal(signal_type="network_location", value="management_vlan", weight=0.20),
    TrustSignal(signal_type="behavior", value="normal", weight=0.15),
    TrustSignal(signal_type="threat_intel", value="no_indicators", weight=0.10),
]
# Score: 0.93
# Required: 0.95 for production database
# Decision: Step-up biometric required
```

## NIST SP 800-207 Implementation Checklist

| Control | Description | Status |
|---------|-------------|--------|
| CP-1 | Access control policy documented | Required |
| AC-2 | Account management with lifecycle | Required |
| AC-3 | Access enforcement via PEP | Required |
| AC-4 | Information flow enforcement | Required |
| AC-6 | Least privilege per session | Required |
| AC-7 | Unsuccessful login attempts | Required |
| AC-17 | Remote access via zero trust | Required |
| AU-2 | Audit events for all decisions | Required |
| AU-3 | Content of audit records | Required |
| IA-2 | Identification and authentication | Required |
| IA-5 | Authenticator management | Required |
| SC-7 | Boundary protection via PEP | Required |
| SC-8 | Transmission confidentiality | Required |

## Zero Trust Principles Reference

The foundational principles that drive the security framework design:

1. **Never trust, always verify** — Every access request must be authenticated
   and authorized regardless of network location. Internal traffic is treated
   with the same scrutiny as external traffic.

2. **Assume breach** — Design systems assuming an attacker is already inside
   the network. Limit blast radius through segmentation and monitor for
   lateral movement.

3. **Verify explicitly** — Use all available signals (identity, device, location,
   behavior) to make access decisions. Never rely on a single factor.

4. **Least privilege access** — Grant the minimum permissions needed for the
   specific task and time window. Use just-in-time and just-enough-access.

5. **Micro-segment** — Create granular per-resource boundaries rather than
   relying on network perimeter controls.

6. **Encrypt everything** — All traffic should be encrypted end-to-end,
   including east-west traffic within the internal network.

7. **Continuously monitor** — Trust is not a one-time event. Continuously
   evaluate signals and adjust access accordingly.

## Implementation Patterns

### Identity-Centric Security Pattern

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Identity   │────▶│   Trust     │────▶│  Resource   │
│  Provider   │     │   Engine    │     │  PEP        │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                    │
       ▼                   ▼                    ▼
  Verify user         Evaluate signals     Enforce decision
  Check MFA           Compute trust score  Allow/Deny/Step-up
  Map attributes      Apply policies       Log decision
```

### Micro-Perimeter Enforcement Pattern

```
Resource A                    Resource B
┌──────────────┐              ┌──────────────┐
│              │              │              │
│   Workload   │              │   Workload   │
│              │              │              │
└──────┬───────┘              └──────┬───────┘
       │                             │
  ┌────┴────┐                   ┌────┴────┐
  │   PEP   │◄──── PDP ────▶   │   PEP   │
  └─────────┘                   └─────────┘
       │                             │
  Allow traffic              Allow traffic
  only to authorized         only from authorized
  destinations               sources
```

### Trust Decay and Refresh Pattern

```python
import time
from security_framework import TrustDecay

class TrustDecayManager:
    """Manages trust score decay and refresh cycles."""

    def __init__(self, decay_rate: float = 0.05, refresh_interval: float = 60.0):
        self.decay_rate = decay_rate
        self.refresh_interval = refresh_interval

    def apply_decay(self, trust_score: float, elapsed_seconds: float) -> float:
        """Apply exponential decay to trust score over time."""
        decayed = trust_score * (2.718 ** (-self.decay_rate * elapsed_seconds))
        return max(0.0, decayed)

    def should_refresh(self, last_refresh: float) -> bool:
        """Check if signals need refreshing."""
        return (time.time() - last_refresh) >= self.refresh_interval

    def compute_effective_trust(self, base_score: float, last_eval: float,
                                 current_time: float) -> float:
        elapsed = current_time - last_eval
        return self.apply_decay(base_score, elapsed)
```

## Enterprise Deployment Patterns

### Hub-and-Spoke Model

In this model, a centralized PDP serves multiple distributed PEPs across the
enterprise network. The PDP maintains the global policy view while PEPs enforce
decisions at local resource boundaries.

```
                    ┌──────────────┐
                    │   Central    │
                    │     PDP      │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │  PEP    │       │  PEP    │       │  PEP    │
    │  DC1    │       │  DC2    │       │  Cloud  │
    └─────────┘       └─────────┘       └─────────┘
```

### Mesh Model

In this model, PEPs form a mesh network where each resource has its own PEP
that communicates with neighboring PEPs for distributed policy evaluation.
This reduces single points of failure but increases complexity.

```
PEP A ◄──────► PEP B
  │  ╲      ╱  │
  │    ╲  ╱    │
  │     ╳     │
  │    ╱  ╲    │
  │  ╱      ╲  │
PEP C ◄──────► PEP D
```

## Migration from Legacy VPN

### Phase 1: Assessment (Weeks 1-4)

1. Inventory all applications and their access patterns
2. Document current VPN configurations and split tunneling rules
3. Identify high-priority applications for zero trust migration
4. Map user populations and their access requirements

### Phase 2: Pilot (Weeks 5-8)

1. Deploy PDP/PEP for 2-3 low-risk applications
2. Configure trust engine with basic signals (identity + device)
3. Enable monitoring mode — log decisions without enforcement
4. Tune trust scoring thresholds based on pilot observations

### Phase 3: Expansion (Weeks 9-16)

1. Roll out to additional applications in priority order
2. Enable enforcement mode on pilot applications
3. Add device health and network location signals
4. Implement micro-segmentation for sensitive resources

### Phase 4: Optimization (Weeks 17-24)

1. Add behavioral analytics signals
2. Enable continuous session monitoring
3. Decommission VPN access for migrated applications
4. Implement automated posture assessment and remediation

## Reference Architectures

### AWS Zero Trust Deployment

```python
# AWS-specific configuration
from security_framework import AWSZeroTrust

aws_config = AWSZeroTrust(
    region="us-east-1",
    iam_integration=True,
    vpc_peering=True,
    security_hub_enabled=True,
    cloudtrail_integration=True,
    kms_key_rotation_days=90,
)

# Protect S3 buckets with zero trust
aws_config.protect_s3_bucket(
    bucket_name="corp-sensitive-data",
    required_trust_level=0.90,
    encryption_required=True,
    access_logging=True,
    block_public_access=True,
)
```

### Azure Zero Trust Deployment

```python
from security_framework import AzureZeroTrust

azure_config = AzureZeroTrust(
    tenant_id="corp-tenant-id",
    subscription_id="prod-subscription",
    conditional_access=True,
    intune_compliance=True,
    defender_for_cloud=True,
)

# Protect Azure SQL with zero trust
azure_config.protect_sql_server(
    server_name="corp-sql-prod",
    required_trust_level=0.85,
    auditing_enabled=True,
    tde_enabled=True,
    aad_auth_only=True,
)
```

## Incident Response Integration

When a trust engine detects a critical risk event, it triggers an automated
incident response workflow:

```python
from security_framework import IncidentResponse

ir = IncidentResponse(
    siem_endpoint="https://splunk:8088",
    soar_endpoint="https://demisto:8443",
    notification_channel="security-ops",
)

# Register incident response handlers
ir.on_critical_risk(
    handler="revoke_session",
    notify=["security-ops", "incident-response"],
    escalate_after_minutes=5,
)

ir.on_lateral_movement_detected(
    handler="isolate_workload",
    notify=["security-ops"],
    auto_contain=True,
)

ir.on_policy_violation(
    handler="log_and_alert",
    notify=["compliance-team"],
    require_ack=True,
)
```

## Zero Trust Maturity Assessment

Use this rubric to assess your organization's zero trust maturity:

| Domain | Traditional | Initial | Advanced | Optimal |
|--------|-------------|---------|----------|---------|
| Identity | Password-only | Basic MFA | FIDO2 + continuous | Adaptive identity |
| Device | No visibility | Basic compliance | Full posture | Continuous attestation |
| Network | Flat network | VPN-based | Micro-segmented | Per-workload isolation |
| Application | Perimeter auth | App-level auth | API-level PEP | Every request verified |
| Data | No classification | Basic labels | Dynamic classification | Auto-classification |
| Visibility | Minimal logs | SIEM integration | Real-time analytics | AI-driven anomaly detection |
| Automation | Manual response | Basic playbooks | Automated response | Self-healing infrastructure |
