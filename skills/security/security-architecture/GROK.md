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

---

## Zero Trust Architecture Implementation

### Identity-Aware Proxy Pattern

```python
from security_architecture import IdentityAwareProxy, PolicyEngine, DeviceTrust

# Deploy identity-aware proxy in front of internal services
proxy = IdentityAwareProxy(
    upstream_services=[
        {"name": "dashboard", "url": "http://dashboard.internal:8080", "auth_required": True},
        {"name": "api", "url": "http://api.internal:3000", "auth_required": True},
        {"name": "admin", "url": "http://admin.internal:8443", "auth_required": True, "mfa_required": True},
    ],
    identity_provider="google_oauth2",
    device_trust=True,
    session_lifetime_hours=8,
)

# Define access policies
policies = [
    {
        "name": "engineering-dashboard",
        "effect": "allow",
        "identity": {"group": "engineering@company.com"},
        "device": {"trusted": True, "managed": True},
        "resource": "dashboard",
        "conditions": {"time_of_day": "08:00-20:00", "geo": "US,CA,GB"},
    },
    {
        "name": "admin-mfa-required",
        "effect": "allow",
        "identity": {"group": "admins@company.com"},
        "device": {"trusted": True},
        "mfa": {"age_max_hours": 1},
        "resource": "admin",
        "conditions": {"jit_approval_required": True},
    },
    {
        "name": "deny-all-default",
        "effect": "deny",
        "identity": {},
        "resource": "*",
    },
]

# Evaluate access request
result = proxy.evaluate(
    request={
        "user": "alice@company.com",
        "groups": ["engineering@company.com"],
        "device_id": "dev-abc-123",
        "device_managed": True,
        "device_trusted": True,
        "mfa_age_minutes": 30,
        "source_ip": "203.0.113.42",
        "geo": "US",
        "time": "14:30",
        "resource": "dashboard",
    },
    policies=policies
)

print(f"Access Decision: {result.decision}")
print(f"Matched Policy: {result.matched_policy}")
print(f"Session Lifetime: {result.session_lifetime_hours}h")
```

### Microsegmentation with Kubernetes NetworkPolicy

```python
from security_architecture import NetworkPolicyGenerator, SecurityTier

generator = NetworkPolicyGenerator(namespace="production")

# Generate tiered network policies
policies = generator.generate_tiered_policies(
    tiers=[
        SecurityTier(
            name="web",
            tier_level=1,
            allowed_egress=["api"],
            allowed_ingress=["0.0.0.0/0"],  # Public
            ports_ingress=[443],
            ports_egress=[8080],
        ),
        SecurityTier(
            name="api",
            tier_level=2,
            allowed_egress=["database", "cache"],
            allowed_ingress=["web"],
            ports_ingress=[8080],
            ports_egress=[5432, 6379],
        ),
        SecurityTier(
            name="database",
            tier_level=3,
            allowed_egress=[],
            allowed_ingress=["api"],
            ports_ingress=[5432],
            ports_egress=[],
        ),
        SecurityTier(
            name="cache",
            tier_level=3,
            allowed_egress=[],
            allowed_ingress=["api"],
            ports_ingress=[6379],
            ports_egress=[],
        ),
    ],
    default_deny_egress=True,
    default_deny_ingress=True,
    allow_dns=True,  # Always allow DNS
)

for policy in policies:
    print(f"--- {policy['metadata']['name']} ---")
    print(f"  Pod Selector: {policy['spec']['podSelector']}")
    print(f"  Ingress Rules: {len(policy['spec'].get('ingress', []))}")
    print(f"  Egress Rules: {len(policy['spec'].get('egress', []))}")
    print()
```

## Cloud Security Architecture

### AWS Security Hub Integration

```python
from security_architecture import AWSSecurityHub, SecurityFinding

hub = AWSSecurityHub(
    region="us-east-1",
    standards=[
        "aws-foundational-security-best-practices",
        "cis-aws-foundations-benchmark",
        "pci-dss-3.2.1",
    ]
)

# Generate security findings from architecture review
findings = [
    SecurityFinding(
        title="S3 bucket publicly accessible",
        severity="critical",
        compliance="CIS 2.1.5",
        resource="arn:aws:s3:::customer-data-prod",
        remediation="Enable S3 block public access and review bucket policy",
        evidence=["s3_bucket_policy.json"],
        auto_remediate=True,
        remediation_script="block_s3_public_access.py"
    ),
    SecurityFinding(
        title="Security group allows unrestricted ingress",
        severity="high",
        compliance="AWS-FSBP EC2.19",
        resource="arn:aws:ec2:us-east-1:123456789:security-group/sg-abc123",
        remediation="Restrict ingress to specific CIDR ranges",
        evidence=["sg_ingress_rules.json"],
        auto_remediate=False,
    ),
]

# Auto-remediate findings
for finding in findings:
    if finding.auto_remediate:
        result = hub.auto_remediate(finding)
        print(f"Remediated: {finding.title}")
        print(f"  Action: {result.action_taken}")
        print(f"  Verified: {result.verified}")
    else:
        print(f"Manual action needed: {finding.title}")
        print(f"  Remediation: {finding.remediation}")
        print(f"  Compliance: {finding.compliance}")
    print()
```

### Cloud Security Posture Management

```python
from security_architecture import CloudPostureManager, PostureCheck

manager = CloudPostureManager(
    providers=["aws", "gcp", "azure"],
    checks=[
        PostureCheck(
            id="CSPM-001",
            title="Encryption at rest enabled for all storage",
            provider="aws",
            service="s3",
            query="aws.s3.buckets[?serverSideEncryptionConfiguration == null]",
            severity="high",
            compliance="PCI-DSS 3.4, SOC2 CC6.1"
        ),
        PostureCheck(
            id="CSPM-002",
            title="No public RDS instances",
            provider="aws",
            service="rds",
            query="aws.rds.instances[?publiclyAccessible == `true`]",
            severity="critical",
            compliance="PCI-DSS 1.3.1"
        ),
        PostureCheck(
            id="CSPM-003",
            title="CloudTrail logging enabled in all regions",
            provider="aws",
            service="cloudtrail",
            query="aws.cloudtrail.trails[?loggingStatus == `false`]",
            severity="high",
            compliance="PCI-DSS 10.1"
        ),
        PostureCheck(
            id="CSPM-004",
            title="No default VPC security groups with 0.0.0.0/0 ingress",
            provider="aws",
            service="ec2",
            query="aws.ec2.security_groups[?groupName == `default` && ipPermissions[?ipRanges[?cidrIp == `0.0.0.0/0`]]]",
            severity="critical",
            compliance="AWS-FSBP EC2.19"
        ),
    ]
)

# Run posture assessment
results = manager.assess()
print(f"=== Cloud Security Posture Report ===")
print(f"Total Checks: {results.total_checks}")
print(f"Passed: {results.passed}")
print(f"Failed: {results.failed}")
print(f"Score: {results.score:.1%}")

for finding in results.findings:
    print(f"\n[{finding.severity.upper()}] {finding.title}")
    print(f"  Resource: {finding.resource}")
    print(f"  Compliance: {finding.compliance}")
    print(f"  Remediation: {finding.remediation}")
```

## Container Security Architecture

### Container Runtime Security

```python
from security_architecture import ContainerSecurityPolicy, RuntimeSecurity

# Define container security baselines
container_policy = ContainerSecurityPolicy(
    image_scanning={
        "enabled": True,
        "block_on": ["critical", "high"],
        "warn_on": ["medium"],
        "scan_before_deploy": True,
    },
    runtime_security={
        "read_only_rootfs": True,
        "no_privilege_escalation": True,
        "drop_all_capabilities": True,
        "add_capabilities": [],  # No capabilities added
        "seccomp_profile": "RuntimeDefault",
        "apparmor_profile": "runtime-default",
        "no_host_network": True,
        "no_host_pid": True,
        "no_host_ipc": True,
    },
    resource_limits={
        "cpu": "2",
        "memory": "2Gi",
        "ephemeral_storage": "1Gi",
    },
    image_signing={
        "enabled": True,
        "verify_before_deploy": True,
        "trusted_registries": ["gcr.io/my-project", "docker.io/library"],
    },
)

# Generate Pod Security Standards manifest
manifest = container_policy.generate_pss_manifest(
    namespace="production",
    level="restricted",
    version="latest",
)
print(f"PSS Manifest: {json.dumps(manifest, indent=2)}")

# Runtime security monitoring
runtime = RuntimeSecurity(
    falco_rules_path="/etc/falco/rules.d",
    alert_channels=["slack-security", "pagerduty"],
)

# Define custom runtime rules
custom_rules = [
    {
        "rule": "Unauthorized process execution",
        "condition": " spawned_process and not proc.name in (allowed_processes)",
        "output": "Unauthorized process started (user=%user.name process=%proc.name)",
        "priority": "WARNING",
    },
    {
        "rule": "Sensitive file access",
        "condition": " open_read and fd.name in (/etc/shadow, /etc/passwd)",
        "output": "Sensitive file accessed (user=%user.name file=%fd.name)",
        "priority": "ERROR",
    },
    {
        "rule": "Network connection to external",
        "condition": " outbound and not dst.ip in (allowed_external_ips)",
        "output": "Outbound connection to unauthorized IP (ip=%dst.ip)",
        "priority": "WARNING",
    },
]
```

### Image Supply Chain Security

```python
from security_architecture import ImageSecurity, ProvenanceVerifier

image_security = ImageSecurity(
    registries=["gcr.io", "docker.io"],
    scanning_engine="trivy",
    signing_engine="cosign",
)

# Verify image before deployment
verification = image_security.verify_image(
    image="gcr.io/my-project/api-server:v1.2.3",
    checks=[
        "vulnerability_scan",     # No critical/high CVEs
        "signature_verification",  # Signed by trusted key
        "provenance_check",       # SBOM attestation present
        "base_image_check",       # Base image from trusted registry
        "malware_scan",           # No malware detected
    ]
)

print(f"Image Verification: {verification.passed}")
for check in verification.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"  [{status}] {check.name}: {check.detail}")

# Generate provenance attestation
provenance = image_security.generate_provenance(
    image="gcr.io/my-project/api-server:v1.2.3",
    build_config={
        "builder": "github-actions",
        "repo": "https://github.com/org/repo",
        "commit": "abc123def456",
        "workflow": "build-and-deploy.yml",
    },
    signing_key="vault://cosign-key",
    include_sbom=True,
    include_vulnerability_report=True,
)
print(f"Provenance attestation: {provenance.attestation_url}")
```

## Service Mesh Security

### Istio Security Configuration

```python
from security_architecture import ServiceMeshSecurity, IstioConfig

mesh_security = ServiceMeshSecurity(
    mesh_type="istio",
    namespace="production",
)

# Define mTLS policy
mtls_policy = mesh_security.generate_mtls_policy(
    strict_mode=True,  # Require mTLS, no plain text
    cert_rotation_days=1,
    min_tls_version="1.3",
)

# Define authorization policies
authz_policies = mesh_security.generate_authz_policies(
    rules=[
        {
            "name": "allow-frontend-to-api",
            "source": {"app": "frontend"},
            "destination": {"app": "api"},
            "http_methods": ["GET", "POST"],
            "paths": ["/api/v1/*"],
        },
        {
            "name": "allow-api-to-database",
            "source": {"app": "api"},
            "destination": {"app": "database"},
            "tcp_ports": [5432],
        },
        {
            "name": "deny-all-default",
            "source": {},
            "destination": {},
            "action": "DENY",
        },
    ]
)

# Generate Istio manifests
for policy in [mtls_policy] + authz_policies:
    print(f"--- {policy['kind']}: {policy['metadata']['name']} ---")
    print(f"  Namespace: {policy['metadata']['namespace']}")
    print()
```

## Infrastructure Hardening

### CIS Benchmark Implementation

```python
from security_architecture import CISBenchmark, BenchmarkResult

# Check CIS Ubuntu 22.04 benchmark compliance
ubuntu_benchmark = CISBenchmark(
    os="ubuntu",
    version="22.04",
    level="1",  # Level 1 = basic security, Level 2 = defense-in-depth
)

results = ubuntu_benchmark.check(host="web-prod-01")

print(f"=== CIS Benchmark Results ===")
print(f"Total Checks: {results.total}")
print(f"Pass: {results.passed}")
print(f"Fail: {results.failed}")
print(f"Not Applicable: {results.not_applicable}")
print(f"Score: {results.score:.1%}")

for check in results.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"\n[{status}] {check.id}: {check.title}")
    print(f"  Description: {check.description}")
    print(f"  Severity: {check.severity}")
    if not check.passed:
        print(f"  Current: {check.current_value}")
        print(f"  Expected: {check.expected_value}")
        print(f"  Fix: {check.remediation_command}")
```

### Linux Server Hardening

```python
from security_architecture import LinuxHardening, HardeningProfile

hardening = LinuxHardening(
    profile=HardeningProfile.CIS_L1,
    target_os="ubuntu",
)

# Generate hardening configuration
config = hardening.generate_config(
    ssh_config={
        "permit_root_login": "no",
        "password_authentication": "no",
        "pubkey_authentication": "yes",
        "protocol": 2,
        "max_auth_tries": 3,
        "client_alive_interval": 300,
        "client_alive_count_max": 2,
        "allow_groups": ["admin", "deploy"],
        "ciphers": ["chacha20-poly1305@openssh.com", "aes256-gcm@openssh.com"],
        "macs": ["hmac-sha2-512-etm@openssh.com", "hmac-sha2-256-etm@openssh.com"],
        "kex_algorithms": ["curve25519-sha256", "diffie-hellman-group16-sha512"],
    },
    firewall_config={
        "default_incoming": "deny",
        "default_outgoing": "allow",
        "allowed_incoming": [
            {"port": 22, "source": "10.0.0.0/8", "comment": "SSH from management network"},
            {"port": 443, "source": "0.0.0.0/0", "comment": "HTTPS from internet"},
        ],
    },
    sysctl_config={
        "net.ipv4.ip_forward": 0,
        "net.ipv4.conf.all.send_redirects": 0,
        "net.ipv4.conf.all.accept_redirects": 0,
        "net.ipv4.conf.all.log_martians": 1,
        "kernel.randomize_va_space": 2,
        "fs.suid_dumpable": 0,
    },
    audit_config={
        "audit_rules": [
            "-w /etc/passwd -p wa -k identity",
            "-w /etc/shadow -p wa -k identity",
            "-w /etc/group -p wa -k identity",
            "-w /etc/sudoers -p wa -k sudoers",
            "-w /var/log/auth.log -p wa -k auth_log",
        ],
    }
)

print(f"Hardening config generated: {config.path}")
print(f"SSH config: {config.ssh_config_path}")
print(f"Firewall config: {config.firewall_config_path}")
print(f"Audit rules: {config.audit_config_path}")
```

## Secure Deployment Architecture

### Blue-Green Deployment with Security Gates

```python
from security_architecture import SecureDeployment, DeploymentGate

deployment = SecureDeployment(
    strategy="blue-green",
    security_gates=[
        DeploymentGate(
            name="vulnerability_scan",
            gate_type="automated",
            tool="trivy",
            pass_criteria={"critical": 0, "high": 0},
            blocking=True,
        ),
        DeploymentGate(
            name="secret_scan",
            gate_type="automated",
            tool="gitleaks",
            pass_criteria={"secrets_found": 0},
            blocking=True,
        ),
        DeploymentGate(
            name="image_signature",
            gate_type="automated",
            tool="cosign",
            pass_criteria={"signature_valid": True},
            blocking=True,
        ),
        DeploymentGate(
            name="security_review",
            gate_type="manual",
            approvers=["security-team"],
            pass_criteria={"approved": True},
            blocking=True,
        ),
    ],
    rollback_triggers=[
        {"metric": "error_rate", "threshold": 0.05, "window": "5m"},
        {"metric": "p99_latency", "threshold": 1000, "window": "5m"},
    ],
)

# Execute deployment
result = deployment.deploy(
    image="gcr.io/my-project/api-server:v1.2.3",
    environment="production",
    namespace="production",
    replicas=3,
)

print(f"Deployment Status: {result.status}")
print(f"Blue Environment: {result.blue_status}")
print(f"Green Environment: {result.green_status}")
print(f"Traffic Switch: {result.traffic_percentage}%")
print(f"Gates Passed: {result.gates_passed}/{result.gates_total}")

if not result.success:
    print(f"Deployment failed at gate: {result.failed_gate}")
    print(f"Rollback triggered: {result.rollback_triggered}")
```

## Disaster Recovery Architecture

### Backup and Recovery Design

```python
from security_architecture import DisasterRecovery, RecoveryPlan

dr_plan = DisasterRecovery(
    rpo_hours=1,    # Recovery Point Objective: max 1 hour data loss
    rto_hours=4,    # Recovery Time Objective: max 4 hours downtime
    backup_encryption="AES-256-GCM",
    backup_storage=["aws-s3", "gcp-gcs"],  # Cross-cloud backup
)

# Define recovery procedures
recovery_procedures = RecoveryPlan(
    procedures=[
        {
            "phase": "Assessment",
            "steps": [
                "Verify backup integrity",
                "Assess data loss scope",
                "Determine recovery scope",
                "Notify stakeholders",
            ],
            "time_estimate_minutes": 30,
            "responsible": "incident-commander",
        },
        {
            "phase": "Infrastructure Recovery",
            "steps": [
                "Provision replacement infrastructure",
                "Restore network configuration",
                "Restore IAM policies",
                "Verify network connectivity",
            ],
            "time_estimate_minutes": 60,
            "responsible": "platform-team",
        },
        {
            "phase": "Data Recovery",
            "steps": [
                "Restore database from backup",
                "Apply WAL logs (point-in-time recovery)",
                "Restore file storage",
                "Verify data integrity",
            ],
            "time_estimate_minutes": 120,
            "responsible": "database-team",
        },
        {
            "phase": "Application Recovery",
            "steps": [
                "Deploy application to recovered infrastructure",
                "Run smoke tests",
                "Verify application health",
                "Enable traffic routing",
            ],
            "time_estimate_minutes": 60,
            "responsible": "engineering-team",
        },
        {
            "phase": "Verification",
            "steps": [
                "Run full test suite",
                "Verify monitoring and alerting",
                "Confirm data integrity",
                "Post-incident review",
            ],
            "time_estimate_minutes": 30,
            "responsible": "qa-team",
        },
    ],
    communication_plan={
        "internal": "slack-incident",
        "external": "status-page",
        "customer_email": "incident@company.com",
    }
)

# Generate DR runbook
runbook = recovery_procedures.generate_runbook(
    format="markdown",
    include_checklists=True,
    include_contact_info=True,
    include_verification_steps=True,
)
print(f"DR Runbook: {runbook.path}")
```

## Security Monitoring Architecture

### SIEM Integration and Alerting

```python
from security_architecture import SIEMIntegration, AlertRule, CorrelationRule

siem = SIEMIntegration(
    backend="splunk",
    index="security",
    retention_days=90,
)

# Define alert rules
alert_rules = [
    AlertRule(
        name="Brute Force Detection",
        query="index=security action=failure | stats count by src_ip user | where count > 10",
        severity="high",
        notification=["slack-security", "pagerduty"],
        suppression_window_minutes=30,
        run_frequency_minutes=5,
    ),
    AlertRule(
        name="Privilege Escalation",
        query="index=security action=escalation OR action=policy_change",
        severity="critical",
        notification=["slack-security", "pagerduty", "email-ciso"],
        suppression_window_minutes=60,
        run_frequency_minutes=1,
    ),
    AlertRule(
        name="Data Exfiltration",
        query="index=security action=download bytes_out > 100000000 | stats sum(bytes_out) by user | where sum > 100000000",
        severity="critical",
        notification=["slack-security", "pagerduty"],
        suppression_window_minutes=120,
        run_frequency_minutes=5,
    ),
]

# Define correlation rules (multi-event detection)
correlation_rules = [
    CorrelationRule(
        name="Compromised Account Chain",
        events=[
            {"query": "action=failure AND src_ip=*", "within": "1h", "count": 20},
            {"query": "action=success AND src_ip=*", "within": "5m"},
            {"query": "action=download OR action=export", "within": "30m"},
        ],
        severity="critical",
        description="Failed logins followed by success and data access",
        notification=["pagerduty"],
    ),
]

# Deploy rules to SIEM
for rule in alert_rules + correlation_rules:
    siem.deploy_rule(rule)
    print(f"Deployed: {rule.name} (severity: {rule.severity})")
```

## API Gateway Security

### Rate Limiting and Throttling

```python
from security_architecture import APIGateway, RateLimitPolicy, ThrottlePolicy

gateway = APIGateway(
    backend="kong",
    plugins=["rate-limiting", "ip-restriction", "jwt-validation", "cors"],
)

# Define rate limiting policies
rate_limits = RateLimitPolicy(
    tiers={
        "anonymous": {"requests": 10, "window": 60, "burst": 5},
        "authenticated": {"requests": 100, "window": 60, "burst": 20},
        "premium": {"requests": 1000, "window": 60, "burst": 100},
        "internal": {"requests": 10000, "window": 60, "burst": 500},
    },
    key_by="consumer",  # Rate limit by API consumer
    fault_tolerant=True,  # Fail open if Redis is down
)

# Define throttling policies per endpoint
throttle_policies = [
    ThrottlePolicy(
        endpoint="/api/v1/search",
        rate_limit="100/minute",
        burst_limit=20,
        key_by="user",
    ),
    ThrottlePolicy(
        endpoint="/api/v1/export",
        rate_limit="5/minute",
        burst_limit=1,
        key_by="user",
    ),
    ThrottlePolicy(
        endpoint="/api/v1/login",
        rate_limit="5/minute",
        burst_limit=3,
        key_by="ip",
    ),
]

# Deploy to gateway
gateway.configure_rate_limiting(rate_limits)
gateway.configure_throttling(throttle_policies)

# Configure IP restrictions
gateway.configure_ip_restriction(
    admin_endpoints=["/admin/*"],
    allowed_ips=["10.0.0.0/8", "192.168.0.0/16"],
    block_message="Admin access restricted to internal network",
)
```
