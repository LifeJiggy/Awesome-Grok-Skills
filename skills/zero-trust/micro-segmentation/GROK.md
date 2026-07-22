---
name: "micro-segmentation"
category: "zero-trust"
version: "1.0.0"
tags: ["zero-trust", "micro-segmentation", "SDN", "network-security"]
---

# Network Micro-Segmentation

## Overview

The Micro-Segmentation module implements network-level zero trust controls
through software-defined networking (SDN) policies, workload isolation, and
dynamic segmentation rules. In a zero trust architecture, micro-segmentation is
the mechanism that enforces the principle of least-privilege at the network
layer — each workload, container, and service communicates only with explicitly
authorized peers through defined segment boundaries. This eliminates the blast
radius of lateral movement attacks that exploit flat network topologies.

The module provides policy-as-code definitions that translate security intent
into enforceable network rules. Policies are authored declaratively and compiled
into platform-specific enforcement formats (iptables, nftables, Kubernetes
NetworkPolicy, cloud security groups). East-west traffic inspection capabilities
monitor intra-segment communication for anomalies, detecting lateral movement
attempts, data exfiltration, and unauthorized service-to-service calls. The
segmentation engine supports dynamic rules that adapt based on real-time threat
intelligence, workload identity, and behavioral baselines.

Segment boundaries are defined by workload attributes rather than IP addresses,
enabling policy portability across dynamic infrastructure where IPs change
constantly. The module supports multi-cloud and hybrid environments, enforcing
consistent segmentation policies across on-premises data centers, AWS VPCs,
Azure VNets, GCP VPCs, and Kubernetes clusters. Policy simulation tools allow
security teams to test segmentation changes in a dry-run mode before deploying
to production, preventing misconfigurations that could disrupt critical
communications.

## Core Capabilities

- Policy-as-code network segmentation with declarative intent language
- East-west traffic inspection and anomaly detection within segments
- Dynamic segmentation rules driven by threat intelligence and behavioral
  baselines
- Container network policy management for Kubernetes (Cilium, Calico, Istio)
- Multi-cloud enforcement across AWS, Azure, GCP, and on-premises
- Segment boundary definition by workload identity, not IP address
- Dry-run policy simulation before production deployment
- Automated compliance mapping to CIS benchmarks and regulatory frameworks

## Segmentation Models

**Flat Network (Before)** — Traditional networks have minimal internal
segmentation. Once an attacker gains a foothold, they can move laterally to any
resource. A single compromised workload exposes the entire network.

**Macro-Segmentation** — Divides the network into large zones (DMZ, internal,
management) with firewall rules between zones. Better than flat, but still
allows free movement within zones.

**Micro-Segmentation** — Each workload or small group of workloads has its own
segment with explicit ingress/egress rules. Lateral movement requires
compromising each segment individually, dramatically increasing attacker cost.

**Nano-Segmentation** — Individual process-level or container-level isolation
with per-connection authorization. Provides the strongest isolation but
requires sophisticated policy management.

## Policy-as-Code Patterns

Policies are authored as structured data that maps security intent to
enforcement rules:

```yaml
# Intent: Only checkout frontend can talk to payment API on port 443
segment: payments
ingress:
  - source: { app: "checkout-*", tier: "frontend" }
    ports: [443/tcp]
    action: allow
egress:
  - destination: { app: "db-payments-*" }
    ports: [5432/tcp]
    action: allow
  - destination: { app: "*" }
    action: deny
```

This intent compiles to platform-specific rules:
- Kubernetes: NetworkPolicy with podSelector and ingress/egress
- AWS: Security Groups with source/destination references
- iptables: Chain rules with source/destination matching
- Cilium: CiliumNetworkPolicy with L7 filtering

## Usage Examples

```python
from micro_segmentation import SegmentationEngine, Segment, NetworkPolicy

# Initialize the segmentation engine
engine = SegmentationEngine(
    provider="kubernetes",
    default_action="deny",
    inspection_enabled=True,
)

# Define a segment for payment processing workloads
payment_segment = engine.create_segment(
    segment_id="payments",
    description="Payment processing workloads",
    classification="pci_dss_scope",
    workload_selectors={"app": "payment-*", "tier": "backend"},
    ingress_rules=[
        NetworkPolicy(
            name="allow-frontend",
            source_selectors={"app": "checkout-*", "tier": "frontend"},
            ports=[(443, "tcp")],
            action="allow",
        ),
    ],
    egress_rules=[
        NetworkPolicy(
            name="allow-database",
            destination_selectors={"app": "db-payments-*"},
            ports=[(5432, "tcp")],
            action="allow",
        ),
    ],
)

print(f"Segment created: {payment_segment.segment_id}")
print(f"  Workloads: {payment_segment.workload_selectors}")
```

```python
# Define cross-segment communication policy
engine.create_cross_segment_policy(
    policy_id="checkout-to-payments",
    source_segment="checkout",
    target_segment="payments",
    allowed_ports=[(443, "tcp")],
    conditions={
        "time_window": "business_hours",
        "max_requests_per_second": 100,
        "require_mutual_tls": True,
    },
)

# Run policy simulation
simulation = engine.simulate(
    source_workload={"app": "checkout-frontend", "namespace": "production"},
    target_workload={"app": "payment-api", "namespace": "production"},
    proposed_policies=["checkout-to-payments"],
)

print(f"Simulation result: {simulation.allowed}")
print(f"  Matched rules: {simulation.matched_rules}")
print(f"  Conflicts: {simulation.conflicts}")

# Deploy policies with dry-run check
deploy_result = engine.deploy(
    segment_ids=["payments", "checkout"],
    dry_run=False,
    validate_compliance=True,
)
print(f"Deployed: {deploy_result.success}")
print(f"  Rules applied: {deploy_result.rules_applied}")
```

```python
# Record traffic events for anomaly detection
engine.record_traffic_event(
    source_ip="10.0.1.15",
    destination_ip="10.0.2.20",
    port=443,
    bytes_transferred=10240,
)

# Check for anomalies
anomalies = engine.get_anomalies(segment_id="payments")
for anomaly in anomalies:
    print(f"Anomaly: {anomaly.anomaly_type} - {anomaly.description}")
```

## Kubernetes NetworkPolicy Integration

For Kubernetes environments, the engine generates native NetworkPolicy resources:

```python
# Compile segment to Kubernetes NetworkPolicy
k8s_policy = engine.compile_segment("payments")
print(k8s_policy)
# Output:
# {
#   "apiVersion": "networking.k8s.io/v1",
#   "kind": "NetworkPolicy",
#   "metadata": {"name": "policy-payments"},
#   "spec": {
#     "podSelector": {"matchLabels": {"app": "payment-*"}},
#     "policyTypes": ["Ingress", "Egress"],
#     "ingress": [...],
#     "egress": [...]
#   }
# }
```

Supported CNI plugins:
- **Calico** — Full NetworkPolicy support with global network policies
- **Cilium** — Enhanced policies with L7 filtering and identity-based rules
- **Weave Net** — NetworkPolicy with encryption support
- **AWS VPC CNI** — NetworkPolicy via security groups for pods

## Best Practices

- **Start with deny-all**: Initialize every segment with a default deny policy.
  Only add explicit allow rules for known, required communications. This ensures
  that new workloads cannot communicate until explicitly authorized.

- **Segment by workload identity**: Use workload labels, service identities,
  and namespace selectors rather than IP addresses. Workloads in dynamic
  environments change IPs frequently; identity-based policies remain stable.

- **Enforce mutual TLS between segments**: Require mTLS for all cross-segment
  communication. This provides encryption and cryptographic authentication,
  preventing both eavesdropping and spoofing between segments.

- **Inspect east-west traffic**: Deploy traffic inspection within segments to
  detect lateral movement. A compromised workload should not be able to freely
  communicate with other workloads in the same segment without detection.

- **Use policy-as-code with version control**: Author all segmentation policies
  in declarative format and store them in version control. This provides
  auditability, rollback capability, and peer review for all network changes.

- **Simulate before deploying**: Always run policy simulation in dry-run mode
  before deploying to production. Check for conflicts, overly broad rules, and
  unintended communication paths that could create vulnerabilities.

- **Map segments to compliance scopes**: Align segment boundaries with
  regulatory boundaries (PCI DSS, HIPAA, SOX). This simplifies compliance
  reporting and ensures that audit trails cover all relevant traffic.

- **Monitor segment health continuously**: Track metrics like denied connection
  attempts, unusual traffic patterns, and policy violations within each segment.
  Anomalous activity may indicate a compromised workload attempting lateral
  movement.

## Compliance Mapping

Segment boundaries can be aligned with regulatory requirements:

| Regulation | Segment Requirement | Description |
|-----------|---------------------|-------------|
| PCI DSS | Cardholder Data Environment | Isolate systems that store/process card data |
| HIPAA | PHI Segmentation | Separate systems handling protected health info |
| SOX | Financial Systems | Isolate financial reporting systems |
| GDPR | Data Residency | Segment by data jurisdiction boundaries |
| NERC CIP | Bulk Electric Systems | Isolate critical cyber assets |

## Related Modules

- [security-framework](../security-framework/GROK.md) — Zero trust architecture
  and trust engine
- [policy-engine](../policy-engine/GROK.md) — Policy authoring and conflict
  resolution
- [continuous-auth](../continuous-auth/GROK.md) — Session and behavioral
  monitoring
- [identity-verification](../identity-verification/GROK.md) — Workload identity
  verification

---

## Advanced Configuration

### Cilium Network Policy

```python
from micro_segmentation import CiliumPolicy

policy = CiliumPolicy(
    name="api-network-policy",
    endpoint_selector={"app": "api-service"},
    ingress_rules=[
        {"from": [{"pod_selector": {"app": "frontend"}}], "ports": [{"port": 8080, "protocol": "TCP"}]},
    ],
    egress_rules=[
        {"to": [{"pod_selector": {"app": "database"}}], "ports": [{"port": 5432, "protocol": "TCP"}]},
    ],
    l7_rules={"http": [{"method": "GET", "path": "/api/*"}]},
)
```

### Threat Intelligence Integration

```python
from micro_segmentation import ThreatIntelConfig

threat_config = ThreatIntelConfig(
    feeds=["abuseipdb", "virustotal", "internal_siem"],
    update_interval_minutes=15,
    auto_block=True,
    confidence_threshold=0.8,
)
```

## Architecture Patterns

### Segmentation Models

```
Flat Network → Macro-Segmentation → Micro-Segmentation → Nano-Segmentation
(blast radius: all) (blast radius: zone) (blast radius: workload) (blast radius: process)
```

### Policy Enforcement Points

```
Workload → Container → Pod → Namespace → VPC/Cloud Account
```

## Integration Guide

### Kubernetes NetworkPolicy

```python
from micro_segmentation import K8sNetworkPolicy

netpol = K8sNetworkPolicy(
    name="deny-all-default",
    namespace="production",
    pod_selector={},
    ingress_rules=[],
    egress_rules=[],
    policy_types=["Ingress", "Egress"],
)
```

### Cloud Security Groups

```python
from micro_segmentation import AWSSecurityGroup

sg = AWSSecurityGroup(
    name="payments-sg",
    vpc_id="vpc-12345",
    ingress_rules=[{"from_port": 443, "to_port": 443, "protocol": "tcp", "source": "sg-frontend"}],
    egress_rules=[{"from_port": 5432, "to_port": 5432, "protocol": "tcp", "destination": "sg-database"}],
)
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Policy caching | Skip recompilation |
| Parallel policy evaluation | Faster multi-segment checks |
| Compiled iptables rules | Kernel-speed enforcement |
| Identity-based lookup | O(1) vs O(n) IP matching |

## Security Considerations

- **Deny-all default**: Start restrictive, add allows
- **Mutual TLS between segments**: Encrypt east-west traffic
- **Policy-as-code**: Version control all policies
- **Dry-run before deploy**: Prevent misconfigurations
- **Audit all policy changes**: Compliance trail

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Connection denied | Missing allow rule | Add explicit egress rule |
| Policy not enforcing | CNI plugin mismatch | Verify CNI supports NetworkPolicy |
| East-west anomaly detected | Possible lateral movement | Investigate workload compromise |
| Policy conflict | Overlapping rules | Run conflict detection |

## API Reference

### SegmentationEngine

```python
class SegmentationEngine:
    def __init__(self, provider: str, default_action: str, inspection_enabled: bool)
    def create_segment(self, segment_id: str, description: str, classification: str, workload_selectors: dict, ingress_rules: list, egress_rules: list) -> Segment
    def simulate(self, source_workload: dict, target_workload: dict, proposed_policies: list) -> SimulationResult
    def deploy(self, segment_ids: list, dry_run: bool, validate_compliance: bool) -> DeployResult
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class Segment:
    segment_id: str
    description: str
    classification: str
    workload_selectors: dict
    ingress_rules: list
    egress_rules: list

@dataclass
class NetworkPolicy:
    name: str
    source_selectors: dict
    destination_selectors: dict
    ports: list
    action: str
```

## Deployment Guide

### Installation

```bash
pip install micro-segmentation
```

### Segmentation Rollout

1. Audit current network topology
2. Define segments by workload identity
3. Write deny-all default policies
4. Add explicit allow rules
5. Run dry-run simulation
6. Deploy with gradual rollout
7. Monitor denied connections

## Monitoring & Observability

```python
from micro_segmentation import MetricsCollector

collector = MetricsCollector()
collector.counter("segment.denied_connections", count, tags={"segment": seg})
collector.counter("segment.allowed_connections", count, tags={"segment": seg})
collector.gauge("segment.workload_count", count, tags={"segment": seg})
collector.counter("segment.policy_violations", count)
```

## Testing Strategy

```python
import pytest
from micro_segmentation import SegmentationEngine

def test_deny_all_default():
    engine = SegmentationEngine(provider="kubernetes", default_action="deny", inspection_enabled=False)
    segment = engine.create_segment("test", "test", "internal", {"app": "test"}, [], [])
    simulation = engine.simulate({"app": "a"}, {"app": "b"}, [])
    assert simulation.allowed is False
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added Cilium support | Install Cilium CNI |
| 2.0.0 | New policy format | Migrate policies |

## Glossary

| Term | Definition |
|------|-----------|
| **Micro-Segmentation** | Per-workload network isolation |
| **East-West Traffic** | Traffic between workloads within a network |
| **CNI** | Container Network Interface |
| **NetworkPolicy** | Kubernetes network isolation resource |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with policy-as-code
- East-west traffic inspection
- Kubernetes NetworkPolicy generation
- Multi-cloud enforcement

## Contributing Guidelines

```bash
git clone https://github.com/example/micro-segmentation.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Segmentation Model Comparison

| Model | Blast Radius | Complexity | Performance | Use Case |
|-------|-------------|------------|-------------|----------|
| Flat network | All | None | Best | Small, trusted |
| Macro-segment | Zone | Low | Good | Traditional DC |
| Micro-segment | Workload | Medium | Good | Cloud-native |
| Nano-segment | Process | High | Overhead | High-security |

### CNI Plugin Comparison

| Plugin | NetworkPolicy | L7 Filtering | Encryption | Performance |
|--------|--------------|-------------|------------|-------------|
| Calico | Full | Limited | WireGuard | High |
| Cilium | Full | Full (HTTP) | WireGuard/IPsec | Very High |
| Weave Net | Basic | No | IPsec | Medium |
| Flannel | No | No | No | High |
| AWS VPC CNI | Via SG | No | No | Very High |

### Network Policy Templates

```yaml
# Default deny all
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

# Allow frontend to backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080

# Allow DNS
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
spec:
  podSelector: {}
  egress:
  - to: []
    ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP
```

### Compliance Mapping Reference

| Regulation | Requirement | Segment Type | Description |
|-----------|-------------|-------------|-------------|
| PCI DSS | Req 1.3 | CDE | Cardholder data environment |
| HIPAA | §164.312 | PHI | Protected health information |
| SOX | §802 | Financial | Financial reporting systems |
| GDPR | Art. 25 | PII | Personal data processing |
| NIST 800-53 | SC-7 | Boundary | Boundary protection |

### Traffic Inspection Reference

| Inspection Type | Depth | Performance | Use Case |
|----------------|-------|-------------|----------|
| L3/L4 | IP/Port | Fast | Basic filtering |
| L7 HTTP | HTTP headers/body | Medium | Web application security |
| L7 gRPC | gRPC methods | Medium | Microservice security |
| L7 DNS | DNS queries | Fast | DNS security |
| TLS inspection | Decrypted payload | Slow | Encrypted traffic |

## Real-World Scenarios

### Scenario 1: PCI DSS Cardholder Data Environment

A retail company needs to isolate its Cardholder Data Environment (CDE) from
the rest of the network. The CDE contains payment processing services that
handle credit card data.

```python
# Define the CDE micro-segment
cde_segment = engine.create_segment(
    segment_id="cde-environment",
    description="Cardholder Data Environment per PCI DSS",
    classification="pci_cde",
    workload_selectors={"compliance": "pci", "tier": "cde"},
    ingress_rules=[
        NetworkPolicy(
            name="allow-web-to-payment",
            source_selectors={"app": "web-frontend-*", "compliance": "pci"},
            ports=[(443, "tcp")],
            action="allow",
        ),
        NetworkPolicy(
            name="allow-monitoring",
            source_selectors={"app": "monitoring-*"},
            ports=[(9090, "tcp")],
            action="allow",
        ),
    ],
    egress_rules=[
        NetworkPolicy(
            name="allow-to-payment-processor",
            destination_selectors={"app": "payment-processor-*"},
            ports=[(443, "tcp")],
            action="allow",
        ),
        NetworkPolicy(
            name="allow-to-vault",
            destination_selectors={"app": "secrets-vault-*"},
            ports=[(8200, "tcp")],
            action="allow",
        ),
        NetworkPolicy(
            name="deny-all-egress",
            destination_selectors={"app": "*"},
            action="deny",
        ),
    ],
)

# Deploy with compliance validation
deploy_result = engine.deploy(
    segment_ids=["cde-environment"],
    dry_run=False,
    validate_compliance=True,
    compliance_framework="PCI-DSS",
)
print(f"PCI DSS compliance: {deploy_result.compliance_status}")
```

### Scenario 2: Kubernetes Multi-Tenant Isolation

A SaaS platform hosts multiple tenants on a shared Kubernetes cluster. Each
tenant's workloads must be isolated from other tenants:

```python
# Create tenant-specific segments
for tenant in ["tenant-acme", "tenant-beta", "tenant-gamma"]:
    engine.create_segment(
        segment_id=f"{tenant}-production",
        description=f"Production workloads for {tenant}",
        classification="tenant_isolated",
        workload_selectors={"tenant": tenant, "environment": "production"},
        ingress_rules=[
            NetworkPolicy(
                name="allow-own-frontend",
                source_selectors={"tenant": tenant, "tier": "frontend"},
                ports=[(443, "tcp")],
                action="allow",
            ),
            NetworkPolicy(
                name="allow-api-gateway",
                source_selectors={"app": "api-gateway", "tier": "edge"},
                ports=[(8080, "tcp")],
                action="allow",
            ),
        ],
        egress_rules=[
            NetworkPolicy(
                name="allow-own-database",
                destination_selectors={"tenant": tenant, "tier": "database"},
                ports=[(5432, "tcp")],
                action="allow",
            ),
            NetworkPolicy(
                name="allow-dns",
                destination_selectors={"app": "coredns"},
                ports=[(53, "udp"), (53, "tcp")],
                action="allow",
            ),
            NetworkPolicy(
                name="deny-cross-tenant",
                destination_selectors={"tenant": "*"},
                action="deny",
            ),
        ],
    )

# Generate cross-tenant deny-all policy
engine.create_global_policy(
    policy_id="deny-cross-tenant-communication",
    description="Prevent any cross-tenant network communication",
    default_action="deny",
    exceptions=[
        {"source": {"app": "api-gateway"}, "destination": {"app": "monitoring"}, "ports": [(9090, "tcp")]}
    ],
)
```

### Scenario 3: East-West Traffic Inspection for Threat Detection

Monitor intra-segment traffic to detect lateral movement by compromised
workloads:

```python
from micro_segmentation import TrafficInspector

inspector = TrafficInspector(
    segments=["payments", "user-data", "admin"],
    inspection_depth="l7_http",
    baseline_window_hours=168,  # 7 days
    anomaly_sensitivity=0.85,
)

# Record baseline traffic patterns
inspector.record_baseline(
    segment_id="payments",
    source_app="payment-api",
    destination_app="payment-db",
    normal_patterns={
        "avg_requests_per_minute": 150,
        "avg_bytes_per_request": 2048,
        "allowed_methods": ["GET", "POST"],
        "allowed_paths": ["/api/v1/payments/*", "/api/v1/refunds/*"],
    },
)

# Detect anomalies
anomalies = inspector.detect_anomalies(
    segment_id="payments",
    time_window="5m",
)

for anomaly in anomalies:
    print(f"Anomaly detected: {anomaly.anomaly_type}")
    print(f"  Source: {anomaly.source_workload}")
    print(f"  Destination: {anomaly.destination_workload}")
    print(f"  Description: {anomaly.description}")
    print(f"  Severity: {anomaly.severity}")
    if anomaly.severity in ["high", "critical"]:
        inspector.trigger_response(
            anomaly_id=anomaly.anomaly_id,
            response="isolate_workload",
            notify=["security-ops"],
        )
```

## Network Policy Templates

### Default Deny All (Kubernetes)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow Specific Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-gateway-ingress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          environment: production
    ports:
    - port: 8080
      protocol: TCP
```

### Namespace Isolation

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-cross-namespace
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: production
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
```

## East-West Traffic Control Patterns

### Service Mesh Integration

For Istio-based service mesh deployments, the engine generates
AuthorizationPolicy resources:

```python
from micro_segmentation import IstioPolicy

# Generate Istio AuthorizationPolicy
istio_policy = IstioPolicy(
    name="payment-service-policy",
    namespace="production",
    selector={"matchLabels": {"app": "payment-api"}},
    rules=[
        {
            "from": [{"source": {"principals": ["cluster.local/ns/production/sa/checkout"]}}],
            "to": [{"operation": {"methods": ["GET", "POST"], "paths": ["/api/v1/payments/*"]}}],
        },
    ],
    action="ALLOW",
)

engine.deploy_istio_policy(istio_policy)
```

### Cilium L7 Network Policies

```python
from micro_segmentation import CiliumL7Policy

l7_policy = CiliumL7Policy(
    name="payment-api-l7",
    endpoint_selector={"app": "payment-api"},
    ingress_rules=[
        {
            "from": [{"endpoint_selector": {"app": "checkout"}}],
            "to_ports": [
                {
                    "ports": [{"port": "443", "protocol": "TCP"}],
                    "rules": {
                        "http": [
                            {"method": "GET", "path": "/api/v1/payments"},
                            {"method": "POST", "path": "/api/v1/payments"},
                            {"method": "GET", "path": "/api/v1/payments/:id"},
                        ],
                    },
                }
            ],
        }
    ],
    egress_rules=[
        {
            "to": [{"endpoint_selector": {"app": "payment-db"}}],
            "to_ports": [
                {"ports": [{"port": "5432", "protocol": "TCP"}]}
            ],
        }
    ],
)
```

## Multi-Cloud Segmentation

### AWS VPC Security Groups

```python
from micro_segmentation import AWSSegment

# Define AWS-specific micro-segments
aws_segment = AWSSegment(
    vpc_id="vpc-12345678",
    segment_name="payments-vpc",
    subnets=["subnet-pri-1", "subnet-pri-2"],
    security_groups=[
        {
            "name": "payments-sg",
            "ingress": [
                {"from_port": 443, "to_port": 443, "protocol": "tcp",
                 "source_sg": "sg-frontend"},
            ],
            "egress": [
                {"from_port": 5432, "to_port": 5432, "protocol": "tcp",
                 "destination_sg": "sg-database"},
            ],
        }
    ],
    vpc_endpoints=["com.amazonaws.us-east-1.s3"],
)
```

### Azure Network Security Groups

```python
from micro_segmentation import AzureSegment

azure_segment = AzureSegment(
    resource_group="prod-rg",
    vnet_name="prod-vnet",
    subnet_name="payments-subnet",
    nsg_rules=[
        {
            "name": "allow-frontend-to-payments",
            "priority": 100,
            "direction": "Inbound",
            "access": "Allow",
            "protocol": "Tcp",
            "source_address_prefix": "10.1.0.0/16",
            "destination_address_prefix": "10.2.0.0/16",
            "source_port_range": "*",
            "destination_port_range": "443",
        },
        {
            "name": "deny-all-inbound",
            "priority": 4096,
            "direction": "Inbound",
            "access": "Deny",
            "protocol": "*",
            "source_address_prefix": "*",
            "destination_address_prefix": "*",
            "source_port_range": "*",
            "destination_port_range": "*",
        },
    ],
)
```

## Workload Identity Integration

### SPIFFE/SPIRE for Service Identity

```python
from micro_segmentation import SPIFFESegment

spiffe_segment = SPIFFESegment(
    trust_domain="corp.example.com",
    spire_server="https://spire:8081",
    workload_selectors=[
        {"spiffe_id": "spiffe://corp.example.com/payment-api"},
        {"spiffe_id": "spiffe://corp.example.com/checkout-*"},
    ],
    registration_ownership="payments-team",
)

# Register workloads with SPIRE
spiffe_segment.register_workload(
    spiffe_id="spiffe://corp.example.com/payment-api",
    selectors=[
        {"type": "k8s", "value": "ns:production:sa:payment-sa"},
        {"type": "k8s", "value": "pod-label:app:payment-api"},
    ],
    dns_name=["payment-api.production.svc.cluster.local"],
)
```

## Policy Conflict Resolution

When overlapping policies exist, the engine resolves conflicts:

| Strategy | Description | Example |
|----------|-------------|---------|
| Most Specific | Narrowest selector wins | `app:payment-api` > `app:payment-*` |
| Most Restrictive | Deny wins over allow | Deny overrides allow on overlap |
| Priority | Highest priority number wins | Priority 1000 > Priority 100 |
| Last Added | Most recently added wins | Newest policy takes precedence |

```python
# Detect and resolve policy conflicts
conflicts = engine.detect_conflicts(segment_ids=["payments", "checkout"])

for conflict in conflicts:
    print(f"Conflict: {conflict.description}")
    print(f"  Policy A: {conflict.policy_a} ({conflict.effect_a})")
    print(f"  Policy B: {conflict.policy_b} ({conflict.effect_b})")

# Auto-resolve using most-specific strategy
resolution = engine.resolve_conflicts(
    strategy="most_specific",
    dry_run=True,
)

for action in resolution.planned_actions:
    print(f"  Will: {action}")
```

## Compliance Audit Reports

### PCI DSS Network Segmentation Report

```python
report = engine.generate_compliance_report(
    segment_id="cde-environment",
    framework="PCI-DSS",
    include_evidence=True,
)

print(f"PCI DSS Compliance Report")
print(f"  CDE segments: {report.segment_count}")
print(f"  Total rules: {report.rule_count}")
print(f"  Allow rules: {report.allow_rules}")
print(f"  Deny rules: {report.deny_rules}")
print(f"  Compliance score: {report.compliance_score:.1%}")
print(f"  Gaps:")
for gap in report.gaps:
    print(f"    - {gap.control}: {gap.description}")
```
