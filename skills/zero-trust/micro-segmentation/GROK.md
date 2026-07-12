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
