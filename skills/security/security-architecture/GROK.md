---
name: "security-architecture"
category: "security"
version: "2.0.0"
tags: ["security", "architecture", "zero-trust", "defense-in-depth", "network-security", "IAM", "kubernetes", "cloud-security"]
---

# Security Architecture

## Overview

Security architecture is the discipline of designing systems where security is an intrinsic property embedded from inception, not an afterthought bolted onto an insecure design. This module provides comprehensive tooling for zero-trust architecture design, network segmentation and microsegmentation, identity and access management patterns, secure communication design, infrastructure hardening, secrets management, and resilience engineering. Security architecture defines the structural controls that make secure coding possible and threat model mitigations enforceable — it operates at the system level where individual code fixes address specific bugs, but architecture prevents entire categories of exploitation.

The fundamental principle is "never trust, always verify." Zero-trust architecture eliminates implicit trust based on network location, requiring authentication and authorization for every request regardless of source. This is achieved through microsegmentation (network-level isolation), continuous authentication (identity verification at every access), least-privilege access (minimum permissions for each component), and encrypted everything (data in transit and at rest). The result is a system where compromising one component does not grant access to others — blast radius containment through architectural design.

This module bridges the gap between abstract security principles and implementable infrastructure. Every pattern includes concrete configurations: Kubernetes NetworkPolicy manifests, AWS IAM role definitions, mTLS certificate management, Vault secrets engine setup, container security baselines, and immutable infrastructure deployment patterns. Security architecture is the foundation that makes compliance possible, threat model mitigations enforceable, and secure coding effective at scale.

## Core Capabilities

1. **Zero Trust Architecture** — Implement "never trust, always verify" patterns: microsegmentation, continuous authentication, least-privilege access, encrypted everything, and device identity verification. Design zero-trust networks that eliminate lateral movement.

2. **Network Segmentation & Microsegmentation** — Design network zones (DMZ, application, data, management) with controlled ingress/egress. Implement microsegmentation for container and cloud workloads using Kubernetes NetworkPolicy, AWS Security Groups, or cloud-native firewalls.

3. **Identity & Access Management (IAM)** — Design role-based access control (RBAC), attribute-based access control (ABAC), federated identity (SAML, OIDC), and service-to-service authentication (mTLS, SPIFFE/SPIRE). Implement least-privilege IAM policies with conditions and resource boundaries.

4. **Secure Communication** — TLS termination patterns, mutual TLS (mTLS) for service-to-service, certificate lifecycle management, API authentication (OAuth 2.0, JWT, API keys), and encryption at rest (AES-256-GCM, KMS-managed keys).

5. **Infrastructure Hardening** — Server hardening baselines (CIS Benchmarks), container security (image scanning, runtime policies, read-only root filesystems), Kubernetes security (Pod Security Standards, OPA Gatekeeper), and cloud security configuration (AWS Config Rules, GCP Security Command Center).

6. **Secrets Management** — Centralized secrets storage (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager), automated rotation, dynamic secrets (short-lived database credentials), and secrets injection into workloads.

7. **Secure Deployment** — Blue-green deployments with security gates, canary releases with rollback triggers, immutable infrastructure (build, deploy, terminate — never patch), and supply-chain security (signed images, provenance verification).

8. **Resilience & Recovery** — Disaster recovery design (RPO/RTO targets), backup encryption, incident response architecture, and business continuity patterns. Design for graceful degradation under attack.

## Usage Examples

### Zero Trust Network Policy Generator

```python
from security_architecture import ZeroTrustPolicy, NetworkSegment, PolicyEngine

# Define network segments with explicit trust boundaries
segments = [
    NetworkSegment(
        name="public-web",
        tier="public",
        cidr="10.0.1.0/24",
        data_classification="medium",
        allowed_inbound=["0.0.0.0/0"],
        allowed_outbound=["10.0.2.0/24"],
        required_controls=["WAF", "Rate Limiting", "TLS 1.3"]
    ),
    NetworkSegment(
        name="application",
        tier="internal",
        cidr="10.0.2.0/24",
        data_classification="high",
        allowed_inbound=["10.0.1.0/24"],
        allowed_outbound=["10.0.3.0/24", "10.0.4.0/24"],
        required_controls=["mTLS", "AuthZ", "Logging"]
    ),
    NetworkSegment(
        name="database",
        tier="restricted",
        cidr="10.0.3.0/24",
        data_classification="critical",
        allowed_inbound=["10.0.2.0/24"],
        allowed_outbound=[],
        required_controls=["mTLS", "Encryption at Rest", "Audit Logging"]
    ),
    NetworkSegment(
        name="management",
        tier="restricted",
        cidr="10.0.4.0/24",
        data_classification="high",
        allowed_inbound=["10.0.2.0/24"],
        allowed_outbound=["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"],
        required_controls=["MFA", "Session Recording", "Just-in-Time Access"]
    ),
]

policy = ZeroTrustPolicy(segments)
rules = policy.generate_rules()

for rule in rules:
    print(f"ALLOW {rule.protocol}:{rule.port} "
          f"FROM {rule.source_cidr} TO {rule.dest_cidr} "
          f"({rule.description})")

# Validate no overly permissive rules exist
violations = policy.validate()
if violations:
    print(f"\nPolicy violations found: {len(violations)}")
    for v in violations:
        print(f"  WARNING: {v}")
```

### IAM Role Definitions with Least Privilege

```python
from security_architecture import IAMRole, PermissionSet, ResourceScope, ConditionSet

# Define granular roles with least-privilege permissions
roles = {
    "deployment": IAMRole(
        name="deployment-role",
        description="Allow CI/CD to deploy artifacts to S3",
        permissions=PermissionSet(
            allow=[
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl",
            ],
            deny=[
                "s3:DeleteBucket",
                "s3:PutBucketPolicy",
                "s3:PutBucketAcl",
            ],
        ),
        scope=ResourceScope(
            arn_pattern="arn:aws:s3:::prod-deploy-*",
            resource_tags={"Environment": "production"}
        ),
        conditions=ConditionSet(
            aws_source_ip="203.0.113.0/24",  # CI/CD network only
            s3_prefix=["deploy/", "releases/"]
        ),
        session_duration_max_hours=1,
        require_mfa=True,
        require_external_id=True
    ),
    "monitoring": IAMRole(
        name="monitoring-role",
        description="Allow Datadog to read CloudWatch metrics",
        permissions=PermissionSet(
            allow=[
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics",
                "logs:GetLogEvents",
                "logs:FilterLogEvents",
                "logs:DescribeLogGroups",
            ],
            deny=[]
        ),
        scope=ResourceScope(
            arn_pattern="arn:aws:logs:*:*:log-group:/app/*"
        ),
        conditions=ConditionSet(),
        session_duration_max_hours=4,
        require_mfa=False
    ),
    "emergency-break-glass": IAMRole(
        name="break-glass-role",
        description="Emergency admin access with strict controls",
        permissions=PermissionSet(
            allow=["*"],  # Full access for emergencies
            deny=[
                "iam:DeleteUser",
                "iam:DeleteRole",
                "organizations:*"
            ]
        ),
        scope=ResourceScope(arn_pattern="*"),
        conditions=ConditionSet(
            mfa_age_max_hours=1,  # Must have MFA within last hour
        ),
        session_duration_max_hours=1,
        require_mfa=True,
        requires_approval=True,
        approval_contacts=["security-team", "ciso"]
    ),
}

for name, role in roles.items():
    print(f"\n=== {role.name} ===")
    print(f"  Description: {role.description}")
    print(f"  Allow: {role.permissions.allow}")
    print(f"  Deny:  {role.permissions.deny}")
    print(f"  Scope: {role.scope.arn_pattern}")
    print(f"  MFA:   {role.require_mfa}")
    print(f"  Max Session: {role.session_duration_max_hours}h")
```

### Kubernetes Security Policy

```python
from security_architecture import K8sSecurityPolicy, PodSecurityStandard, NetworkPolicyGenerator

# Define Pod Security Standards for production namespace
policy = K8sSecurityPolicy(
    namespace="production",
    standard=PodSecurityStandard.RESTRICTED,
    rules=[
        {
            "apiGroups": [""],
            "resources": ["pods"],
            "verbs": ["create", "update"],
            "validate": {
                "runAsNonRoot": True,
                "readOnlyRootFilesystem": True,
                "allowPrivilegeEscalation": False,
                "capabilities_drop": ["ALL"],
                "capabilities_add": [],  # No capabilities added
                "seccomp_profile": "RuntimeDefault",
                "hostNetwork": False,
                "hostPID": False,
                "hostIPC": False,
            }
        },
    ]
)

# Generate network policies
net_gen = NetworkPolicyGenerator(namespace="production")
network_policies = net_gen.generate(
    allow_from=["ingress-controller"],
    allow_to=["redis", "database"],
    deny_all_egress=False,  # Allow DNS resolution
)

for m in network_policies:
    print(f"--- {m['metadata']['name']} ---")
    print(f"  Namespace: {m['metadata']['namespace']}")
    print(f"  Policy type: {m['spec']['policyTypes']}")
    print(f"  Ingress rules: {len(m['spec'].get('ingress', []))}")
    print(f"  Egress rules: {len(m['spec'].get('egress', []))}")
```

### Secrets Management with Vault

```python
from security_architecture import SecretsManager, SecretRotationPolicy

vault = SecretsManager(
    backend="vault",
    addr="https://vault.internal:8200",
    auth_method="kubernetes",
    mount_path="secret"
)

# Configure automated secret rotation
vault.configure_rotation(
    path="database/prod",
    rotation_interval_days=30,
    notification_channels=["slack-security", "email-oncall"],
    rotation_script="rotate-db-creds.sh"
)

# Generate dynamic database credentials (short-lived)
dynamic_cred = vault.generate_dynamic_secret(
    mount="database",
    role="readonly",
    ttl="1h"  # Auto-expire after 1 hour
)
print(f"Username: {dynamic_cred.username}")
print(f"Password: {dynamic_cred.password}")
print(f"Expires:  {dynamic_cred.lease_duration}s")

# Generate Kubernetes secret manifest
manifest = vault.generate_k8s_secret(
    name="db-credentials",
    namespace="production",
    secret_paths=["database/prod/creds"],
    annotations={
        "vault.hashicorp.com/agent-inject": "true",
        "vault.hashicorp.com/role": "database"
    }
)
```

## Architecture

The security architecture module follows a defense-in-depth layered model:

```
┌──────────────────────────────────────────────────────────────┐
│                    PERIMETER LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   WAF    │  │   DDoS   │  │  Rate    │  │   CDN    │    │
│  │          │  │Protection│  │ Limiting │  │          │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       └──────────────┼───────────┼──────────────┘           │
│                      │           │                          │
└──────────────────────┼───────────┼──────────────────────────┘
                       │           │
┌──────────────────────▼───────────▼──────────────────────────┐
│                    IDENTITY LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   MFA    │  │  OAuth   │  │   RBAC   │  │  Device  │    │
│  │  AuthN   │  │  2.0     │  │  / ABAC  │  │ Identity │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       └──────────────┼───────────┼──────────────┘           │
│                      │           │                          │
└──────────────────────┼───────────┼──────────────────────────┘
                       │           │
┌──────────────────────▼───────────▼──────────────────────────┐
│                    NETWORK LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Network │  │   mTLS   │  │  Micro-  │  │   DNS    │    │
│  │Zones/VPN │  │  Between │  │segment   │  │ Security │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       └──────────────┼───────────┼──────────────┘           │
│                      │           │                          │
└──────────────────────┼───────────┼──────────────────────────┘
                       │           │
┌──────────────────────▼───────────▼──────────────────────────┐
│                    APPLICATION LAYER                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Input   │  │  Output  │  │  Session │  │   CSRF   │    │
│  │Validation│  │ Encoding │  │ Management│  │Protection│    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       └──────────────┼───────────┼──────────────┘           │
│                      │           │                          │
└──────────────────────┼───────────┼──────────────────────────┘
                       │           │
┌──────────────────────▼───────────▼──────────────────────────┐
│                    DATA LAYER                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │Encryption│  │  Backup  │  │   Key    │  │  Data    │    │
│  │at Rest   │  │Encryption│  │Management│  │Masking   │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Assume breach** — Design as if attackers are already inside the network. Every access request must be authenticated, authorized, and encrypted regardless of network location. Zero trust eliminates implicit trust.

2. **Segment by data sensitivity** — Separate systems by data classification. Production databases containing PII should not be accessible from developer workstations. Use network zones with controlled ingress/egress.

3. **Use mutual TLS everywhere** — Don't rely on network-level trust for service-to-service communication. Authenticate both client and server with mTLS. Use SPIFFE/SPIRE for identity issuance in dynamic environments.

4. **Automate secrets rotation** — No hardcoded credentials anywhere. Rotate all secrets automatically on a schedule and on compromise detection. Use dynamic secrets (short-lived) where possible.

5. **Immutable infrastructure** — Don't patch running servers. Build new images, deploy, and terminate old instances. This eliminates configuration drift and ensures known-good state.

6. **Apply least privilege at every layer** — IAM roles, network rules, container capabilities, database permissions, API scopes, and Kubernetes RBAC. Each layer independently limits blast radius.

7. **Design for auditability** — Every access decision, configuration change, and data access should be logged and auditable. Use centralized logging with tamper-evident storage.

8. **Test architecture under attack** — Run chaos engineering and red team exercises against architectural controls. Architecture is only validated by testing under realistic attack conditions.

## Performance Considerations

- **mTLS overhead**: TLS 1.3 with mTLS adds <2ms latency per connection. Use connection pooling to amortize handshake cost across requests.
- **Network policies**: Kubernetes NetworkPolicy enforcement is O(n) per packet rule. Large numbers of rules (>100) may impact high-throughput workloads. Use tiered policies for efficiency.
- **Secrets access**: Vault API calls add ~5-10ms per secret retrieval. Cache secrets locally with appropriate TTL to reduce latency.
- **Encryption at rest**: AES-256-GCM encryption adds negligible overhead for most workloads. Hardware-accelerated AES (AES-NI) on modern CPUs makes encryption effectively free.
- **IAM policy evaluation**: Complex IAM policies with many conditions increase evaluation time. Keep policies simple and use resource boundaries for coarse-grained control.

## Security Considerations

- **Secrets in environment variables**: Environment variables are visible via `/proc` and container inspection. Use volume mounts or init containers for secrets injection instead.
- **Kubernetes RBAC escalation**: Users with `bind` permission on ClusterRoles can escalate privileges. Audit RBAC policies regularly for privilege escalation paths.
- **Cloud misconfiguration**: Default cloud configurations are permissive. Use AWS Config Rules, GCP Security Command Center, or Azure Security Center to detect misconfigurations.
- **Certificate management**: Expired certificates cause outages. Automate certificate renewal with cert-manager or Let's Encrypt with sufficient lead time.
- **Network policy gaps**: Default-allow policies in Kubernetes provide no network isolation. Always define explicit NetworkPolicies and use a CNI that enforces them.

## Related Modules

- **threat-modeling** — Identify threats that architecture must address
- **secure-coding** — Implement code-level controls within the architectural framework
- **vulnerability-management** — Verify that architectural controls are functioning
- **compliance** — Map architectural controls to regulatory requirements (NIST 800-53, CIS Benchmarks, PCI DSS 1.x)
- **cloud-iam-deep** — AWS/Azure/GCP IAM attack patterns and privilege escalation
- **hunt-cloud-misconfig** — Cloud infrastructure misconfiguration detection
- **hunt-subdomain** — Subdomain takeover risks in architecture design

## References

- NIST SP 800-207 (Zero Trust Architecture): https://csrc.nist.gov/publications/detail/sp/800-207/final
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks/
- Kubernetes Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- SPIFFE/SPIRE Identity Framework: https://spiffe.io/
- HashiCorp Vault: https://www.vaultproject.io/
- AWS Well-Architected Framework — Security Pillar: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
- Google BeyondCorp (Zero Trust): https://cloud.google.com/beyondcorp
- Microsoft Zero Trust Architecture: https://docs.microsoft.com/en-us/security/zero-trust/
- OWASP Application Security Architecture: https://owasp.org/www-project-application-security-verification-standard/
- NIST SP 800-123 (General Server Security): https://csrc.nist.gov/publications/detail/sp/800-123/final
