---
name: "zero-trust-security"
category: "cybersecurity"
version: "2.0.0"
tags: ["cybersecurity", "zero-trust", "security-architecture", "identity", "microsegmentation"]
---

# Zero Trust Security

## Overview

The Zero Trust Security module provides comprehensive guidance for implementing zero trust architecture principles across enterprise environments. It covers identity-centric security, microsegmentation, continuous verification, least-privilege access, and zero trust network architecture design.

This skill is essential for security architects, CISOs, and platform engineers implementing zero trust security models.

## Core Capabilities

- **Identity Verification**: Continuous authentication, MFA, and identity-aware proxy patterns
- **Microsegmentation**: Network segmentation, workload isolation, and east-west traffic control
- **Least Privilege**: Just-in-time access, just-enough-access, and privilege escalation controls
- **Device Trust**: Device posture assessment, MDM integration, and endpoint verification
- **Data Protection**: Data classification, encryption in transit/at rest, and DLP patterns
- **Network Architecture**: Software-defined perimeter, ZTNA, and SASE patterns
- **Policy Engine**: Policy-as-code, attribute-based access control, and dynamic policy evaluation
- **Monitoring**: Continuous monitoring, anomaly detection, and behavioral analytics

## Usage Examples

```python
from zero_trust_security import (
    IdentityVerifier,
    MicrosegmentationPlanner,
    LeastPrivilegeEngine,
    DeviceTrustChecker,
    PolicyEngine,
)

# --- Identity Verification ---
verifier = IdentityVerifier()
auth_result = verifier.authenticate(
    user_id="user@company.com",
    mfa_method="totp",
    device_id="dev-001",
    source_ip="192.168.1.100",
)
print(f"Authenticated: {auth_result.success}")
print(f"Risk score: {auth_result.risk_score}")
print(f"MFA verified: {auth_result.mfa_verified}")

# --- Microsegmentation ---
planner = MicrosegmentationPlanner()
segments = planner.design_segments(
    workloads=["web-tier", "app-tier", "db-tier", "mgmt-tier"],
    traffic_rules=[
        {"from": "web", "to": "app", "ports": [443]},
        {"from": "app", "to": "db", "ports": [5432]},
    ],
)
print(f"Segments: {len(segments)}")
print(f"Rules: {sum(len(s.allowed_traffic) for s in segments)}")

# --- Least Privilege ---
lpe = LeastPrivilegeEngine()
access = lpe.request_access(
    user="engineer@company.com",
    resource="prod-database",
    action="read",
    duration_hours=4,
    justification=" debugging production issue #1234",
)
print(f"Access granted: {access.granted}")
print(f"Duration: {access.duration_hours}h")
print(f"Auto-revoke: {access.auto_revoke}")

# --- Device Trust ---
device_checker = DeviceTrustChecker()
trust = device_checker.check_device(
    device_id="dev-001",
    os_version="Windows 11 23H2",
    disk_encrypted=True,
    antivirus_updated=True,
    compliant=True,
)
print(f"Device trust: {trust.trust_level}")
print(f"Score: {trust.score}/100")

# --- Policy Engine ---
policy_engine = PolicyEngine()
decision = policy_engine.evaluate(
    subject="engineer@company.com",
    resource="prod-server-01",
    action="ssh",
    context={"device_trust": "high", "location": "office", "time": "10:00"},
)
print(f"Decision: {decision.allow}")
print(f"Policy: {decision.matched_policy}")
```

## Best Practices

- Never trust, always verify — authenticate and authorize every request
- Implement least-privilege access with just-in-time elevation for production
- Use identity as the new perimeter — all access decisions based on identity
- Microsegment networks at workload level, not just subnet level
- Continuously evaluate trust — session re-authentication on risk changes
- Encrypt all traffic, even east-west within the network
- Implement device posture checks before granting access
- Use policy-as-code for auditable, version-controlled access rules
- Monitor all access patterns for behavioral anomaly detection
- Implement break-glass procedures for emergency access with full audit

## Related Modules

- **penetration-testing**: Testing zero trust implementations
- **security-audit**: Auditing zero trust architecture compliance
- **threat-intelligence**: Threat data for zero trust policy decisions
- **incident-response**: Zero trust impact on incident response

---

## Advanced Configuration

### Policy Engine Configuration

Configure attribute-based access control policies.

```python
policy_config = PolicyConfig(
    evaluation_mode="deny_by_default",
    context_attributes=["device_trust", "location", "time", "risk_score"],
    risk_thresholds={
        "low": 0,
        "medium": 30,
        "high": 60,
        "critical": 80,
    },
    re_authentication_triggers=["risk_score_change", "location_change", "device_change"],
)
```

### Microsegmentation Configuration

Configure network segmentation rules.

```python
segmentation_config = SegmentationConfig(
    zones={
        "dmz": {"level": "public", "east_west": "deny"},
        "web": {"level": "semi-public", "east_west": "allow_web_to_app"},
        "app": {"level": "internal", "east_west": "allow_app_to_db"},
        "db": {"level": "restricted", "east_west": "deny_all"},
        "mgmt": {"level": "highly_restricted", "east_west": "allow_mgmt"},
    },
    default_action="deny",
    logging=True,
)
```

### Device Trust Configuration

Configure device posture assessment.

```python
device_trust_config = DeviceTrustConfig(
    required_checks=[
        "disk_encryption",
        "os_version",
        "antivirus_updated",
        "firewall_enabled",
        "screen_lock",
        "certificate_present",
    ],
    trust_levels={
        "untrusted": 0,
        "low": 25,
        "medium": 50,
        "high": 75,
        "full": 100,
    },
    auto_remediation=True,
)
```

---

## Architecture Patterns

### Identity-Aware Proxy Pattern

```python
class IdentityAwareProxy:
    def __init__(self):
        self.identity_provider = IdentityProvider()
        self.policy_engine = PolicyEngine()

    def handle_request(self, request):
        # Authenticate user
        identity = self.identity_provider.authenticate(request)
        if not identity:
            return Response(status=401)

        # Evaluate policy
        decision = self.policy_engine.evaluate(
            subject=identity,
            resource=request.resource,
            action=request.method,
            context=request.context,
        )

        if decision.allow:
            return self.forward_request(request)
        else:
            return Response(status=403)
```

### Just-In-Time Access Pattern

```python
class JITAccess:
    def request_access(self, user, resource, duration_hours, justification):
        # Check baseline access
        if not self.can_request(user, resource):
            return AccessDenied("Not eligible for JIT access")

        # Create time-bound access
        access = TemporaryAccess(
            user=user,
            resource=resource,
            duration=timedelta(hours=duration_hours),
            justification=justification,
            auto_revoke=True,
        )
        return access
```

### Continuous Verification Pattern

```python
class ContinuousVerification:
    def __init__(self):
        self.session_risk = SessionRiskCalculator()

    def check_session(self, session):
        risk = self.session_risk.calculate(session)
        if risk > session.threshold:
            return self.require_reauthentication(session)
        return session
```

### Software-Defined Perimeter Pattern

```python
class SDP:
    def __init__(self):
        self.controllers = []
        self.gateways = []

    def authenticate_and_connect(self, user, device, resource):
        # Control plane authentication
        controller_auth = self.authenticate_controller(user, device)
        if not controller_auth.success:
            return ConnectionDenied()

        # Data plane connection
        gateway = self.select_gateway(resource)
        return gateway.connect(user, resource, controller_auth.token)
```

---

## Integration Guide

### Okta Integration

```python
import okta

client = okta.Client({"orgUrl": "https://company.okta.com", "token": "..."})

# Verify user identity
user = client.users.get_user(user_id)
groups = client.users.list_user_groups(user.id)

# Check device trust
device = client.devices.get_device(device_id)
trust_level = device.status  # " ACTIVE", " SUSPENDED", etc.
```

### Azure AD Integration

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

credential = DefaultAzureCredential()
client = AuthorizationManagementClient(credential, subscription_id)

# Check user permissions
role_assignments = client.role_assignments.list_for_scope(
    scope=f"/subscriptions/{subscription_id}",
    filter=f"principalId eq '{user_id}'",
)
```

### CrowdStrike Integration

```python
import falconpy

falcon = falconpy.FalconClient(client_id="...", client_secret="...")

# Check device posture
device_id = "abc123"
response = falcon.DeviceCompositeScore.get(id=device_id)
trust_score = response.body["resources"][0]["score"]
```

---

## Performance Optimization

### Policy Caching

```python
# Cache policy evaluation results
policy_cache = PolicyCache(
    ttl_seconds=300,
    max_entries=10000,
    invalidation_triggers=["policy_change", "user_role_change"],
)
```

### Session State Optimization

```python
# Efficient session state management
session_store = SessionStore(
    backend="redis",
    ttl_seconds=3600,
    compression=True,
    encryption=True,
)
```

---

## Security Considerations

### Break-Glass Procedures

```python
class BreakGlassProcedure:
    def emergency_access(self, user, resource, reason):
        # Log emergency access
        audit_log.log_emergency_access(user, resource, reason)

        # Grant time-limited access
        access = TemporaryAccess(
            user=user,
            resource=resource,
            duration=timedelta(hours=1),
            requires_approval=False,
            audit_level="enhanced",
        )

        # Notify security team
        notify_security_team(f"Emergency access granted: {user} -> {resource}")

        return access
```

### Continuous Monitoring

```python
class ContinuousMonitor:
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.threat_intel = ThreatIntelFeed()

    def monitor(self, event):
        # Check for anomalies
        anomaly_score = self.anomaly_detector.score(event)
        if anomaly_score > 0.8:
            self.alert(event, "anomaly_detected")

        # Check threat intel
        iocs = self.threat_intel.check(event.indicators)
        if iocs:
            self.alert(event, "threat_intel_match")
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Access denied | Policy violation | Check policy rules |
| Session expired | Risk threshold exceeded | Re-authenticate |
| Device not trusted | Failed posture check | Update device compliance |
| MFA required | Risk score elevated | Complete MFA challenge |

---

## API Reference

### IdentityVerifier

```python
class IdentityVerifier:
    def authenticate(user_id, mfa_method, device_id, source_ip) -> AuthResult
    def verify_session(session_id, context) -> bool
    def revoke_session(session_id) -> None
    def get_risk_score(user_id, context) -> float
```

### PolicyEngine

```python
class PolicyEngine:
    def evaluate(subject, resource, action, context) -> PolicyDecision
    def add_policy(policy) -> None
    def remove_policy(policy_id) -> None
    def list_policies(filters) -> List[Policy]
```

### MicrosegmentationPlanner

```python
class MicrosegmentationPlanner:
    def design_segments(workloads, traffic_rules) -> List[Segment]
    def validate_rules(segments) -> ValidationResult
    def generate_firewall_rules(segments) -> List[FirewallRule]
```

---

## Data Models

### PolicyDecision

```python
@dataclass
class PolicyDecision:
    allow: bool
    reason: str
    matched_policy: str
    risk_score: float
    conditions: List[str]
```

### DeviceTrust

```python
@dataclass
class DeviceTrust:
    device_id: str
    trust_level: str
    score: int
    last_check: datetime
    compliance_status: dict
```

---

## Deployment Guide

### Zero Trust Deployment Checklist

- [ ] Identity provider configured
- [ ] MFA enabled for all users
- [ ] Device posture checks enabled
- [ ] Microsegmentation rules defined
- [ ] Policy engine deployed
- [ ] Monitoring and alerting configured
- [ ] Break-glass procedures documented

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `ztna.access.deny` | Access denied rate | Spike |
| `ztna.device.untrusted` | Untrusted devices | > 10% |
| `ztna.mfa.challenge` | MFA challenges | Spike |
| `ztna.risk.score` | Average risk score | > 50 |

---

## Testing Strategy

### Zero Trust Tests

```python
def test_access_control():
    engine = PolicyEngine()
    decision = engine.evaluate(
        subject="user@company.com",
        resource="prod-server",
        action="ssh",
        context={"device_trust": "high", "location": "office"},
    )
    assert decision.allow
```

---

## Versioning & Migration

### Policy Versioning

Track policy versions for audit and rollback.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Zero Trust** | Security model that never trusts, always verifies |
| **Microsegmentation** | Network segmentation at workload level |
| **JIT Access** | Just-in-time access with automatic expiration |
| **Device Posture** | Assessment of device security compliance |
| **ZTNA** | Zero Trust Network Access |

---

## Changelog

### v2.0.0
- Added continuous verification
- Device posture assessment
- JIT access patterns

### v1.0.0
- Initial release with identity verification

---

## Contributing Guidelines

- Document all policy decisions
- Test access controls thoroughly
- Maintain audit logs

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
