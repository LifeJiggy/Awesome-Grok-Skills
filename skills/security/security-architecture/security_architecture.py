"""
Security Architecture Framework
================================

Provides zero-trust policy generation, IAM role definitions, network
segmentation, Kubernetes security policies, and secrets management
configuration for building secure-by-design systems.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TrustTier(Enum):
    PUBLIC = "public"
    SEMI_TRUSTED = "semi-trusted"
    TRUSTED = "trusted"
    INTERNAL = "internal"
    RESTRICTED = "restricted"


class Protocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    ANY = "ANY"


class AuthMethod(Enum):
    NONE = "none"
    API_KEY = "api_key"
    JWT = "jwt"
    OAUTH2 = "oauth2"
    MTLS = "mtls"
    KUBERNETES = "kubernetes"


class PodSecurityStandard(Enum):
    PRIVILEGED = "privileged"
    BASELINE = "baseline"
    RESTRICTED = "restricted"


class EncryptionAtRest(Enum):
    NONE = "none"
    AES256 = "aes256"
    KMS = "kms"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class NetworkSegment:
    """A network segment with access rules."""
    name: str
    tier: str = "internal"
    cidr: str = "10.0.0.0/24"
    allowed_inbound: list[str] = field(default_factory=list)
    allowed_outbound: list[str] = field(default_factory=list)
    protocols: list[str] = field(default_factory=lambda: ["TCP"])
    description: str = ""


@dataclass
class FirewallRule:
    """A generated firewall rule."""
    source_cidr: str
    dest_cidr: str
    protocol: str = "TCP"
    port: int = 443
    action: str = "ALLOW"
    description: str = ""
    logging: bool = True


@dataclass
class IAMPermissionSet:
    """IAM permissions for a role."""
    allow: list[str] = field(default_factory=list)
    deny: list[str] = field(default_factory=list)
    conditions: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceScope:
    """Resource scope for IAM policy."""
    arn_pattern: str = ""
    account_ids: list[str] = field(default_factory=list)
    regions: list[str] = field(default_factory=lambda: ["*"])


@dataclass
class IAMRole:
    """An IAM role definition."""
    name: str
    permissions: IAMPermissionSet = field(default_factory=IAMPermissionSet)
    scope: ResourceScope = field(default_factory=ResourceScope)
    session_duration_max_hours: int = 1
    require_mfa: bool = True
    description: str = ""
    trust_policy: dict[str, Any] = field(default_factory=dict)


@dataclass
class ServiceMeshConfig:
    """Service mesh (Istio/Linkerd) configuration."""
    name: str = "default"
    mtls_mode: str = "STRICT"
    egress_control: str = "REGISTRY_ONLY"
    timeout_seconds: int = 30
    retry_attempts: int = 3
    circuit_breaker: bool = True


@dataclass
class K8sNetworkPolicy:
    """Kubernetes network policy manifest."""
    name: str = ""
    namespace: str = "default"
    pod_selector: dict[str, Any] = field(default_factory=dict)
    ingress_rules: list[dict[str, Any]] = field(default_factory=list)
    egress_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SecretsConfig:
    """Secrets management configuration."""
    backend: str = "vault"
    addr: str = ""
    auth_method: AuthMethod = AuthMethod.KUBERNETES
    mount_path: str = "secret"
    rotation_interval_days: int = 30
    notification_channels: list[str] = field(default_factory=list)


@dataclass
class DeploymentPolicy:
    """Deployment security policy."""
    require_signed_images: bool = True
    allowed_registries: list[str] = field(default_factory=list)
    require_resource_limits: bool = True
    require_read_only_rootfs: bool = True
    max_replicas: int = 10
    health_check_required: bool = True


# ---------------------------------------------------------------------------
# Zero Trust Policy Generator
# ---------------------------------------------------------------------------

class ZeroTrustPolicy:
    """Generate zero-trust network policies from segment definitions."""

    def __init__(self, segments: list[NetworkSegment]) -> None:
        self.segments = {s.name: s for s in segments}
        self._rules: list[FirewallRule] = []

    def generate_rules(self) -> list[FirewallRule]:
        """Generate explicit allow rules between segments."""
        self._rules = []
        for seg in self.segments.values():
            for dest_cidr in seg.allowed_outbound:
                rule = FirewallRule(
                    source_cidr=seg.cidr,
                    dest_cidr=dest_cidr,
                    protocol="TCP",
                    port=443,
                    description=f"{seg.name} → {dest_cidr}",
                )
                self._rules.append(rule)
        return self._rules

    def validate_no_direct_access(self) -> list[str]:
        """Verify that restricted segments are not directly accessible."""
        violations: list[str] = []
        restricted = [
            s for s in self.segments.values()
            if s.tier in ("restricted", "internal")
        ]
        for seg in restricted:
            # Check if any non-internal segment can reach restricted
            for other in self.segments.values():
                if other.name == seg.name:
                    continue
                if other.tier in ("restricted", "internal"):
                    continue
                if seg.cidr in other.allowed_outbound:
                    violations.append(
                        f"VIOLATION: {other.name} ({other.tier}) can reach "
                        f"{seg.name} ({seg.tier}) at {seg.cidr}"
                    )
        return violations

    def get_policy_summary(self) -> dict[str, Any]:
        """Get a summary of the zero-trust policy."""
        return {
            "segments": len(self.segments),
            "rules": len(self._rules),
            "restricted_segments": sum(
                1 for s in self.segments.values()
                if s.tier in ("restricted", "internal")
            ),
        }


# ---------------------------------------------------------------------------
# IAM Policy Builder
# ---------------------------------------------------------------------------

class IAMPolicyBuilder:
    """Build and validate IAM role definitions."""

    def __init__(self) -> None:
        self._roles: dict[str, IAMRole] = {}

    def add_role(self, role: IAMRole) -> None:
        self._roles[role.name] = role

    def get_role(self, name: str) -> Optional[IAMRole]:
        return self._roles.get(name)

    def validate_least_privilege(self) -> list[str]:
        """Check for overly permissive policies."""
        warnings: list[str] = []
        for name, role in self._roles.items():
            for perm in role.permissions.allow:
                if perm == "*" or perm.endswith("*"):
                    warnings.append(
                        f"ROLE {name}: wildcard permission '{perm}' "
                        f"violates least privilege"
                    )
            if not role.require_mfa and role.session_duration_max_hours > 4:
                warnings.append(
                    f"ROLE {name}: no MFA required with long session duration"
                )
        return warnings

    def generate_aws_policy(self, role: IAMRole) -> dict[str, Any]:
        """Generate an AWS IAM policy document."""
        statements = []
        if role.permissions.allow:
            statements.append({
                "Effect": "Allow",
                "Action": role.permissions.allow,
                "Resource": role.scope.arn_pattern,
            })
        if role.permissions.deny:
            statements.append({
                "Effect": "Deny",
                "Action": role.permissions.deny,
                "Resource": "*",
            })
        return {
            "Version": "2012-10-17",
            "Statement": statements,
        }

    def list_roles(self) -> list[dict[str, Any]]:
        return [
            {"name": r.name, "mfa": r.require_mfa,
             "max_session_h": r.session_duration_max_hours}
            for r in self._roles.values()
        ]


# ---------------------------------------------------------------------------
# Kubernetes Security
# ---------------------------------------------------------------------------

class K8sSecurityPolicy:
    """Generate Kubernetes security policies and network policies."""

    def __init__(self, namespace: str = "default",
                 standard: PodSecurityStandard = PodSecurityStandard.RESTRICTED) -> None:
        self.namespace = namespace
        self.standard = standard
        self._network_policies: list[K8sNetworkPolicy] = []

    def generate_network_policies(self) -> list[dict[str, Any]]:
        """Generate default-deny + allow network policies."""
        policies = []

        # Default deny all ingress and egress
        policies.append({
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "default-deny-all",
                "namespace": self.namespace,
            },
            "spec": {
                "podSelector": {},
                "policyTypes": ["Ingress", "Egress"],
            },
        })

        # Allow DNS egress
        policies.append({
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "allow-dns",
                "namespace": self.namespace,
            },
            "spec": {
                "podSelector": {},
                "policyTypes": ["Egress"],
                "egress": [{
                    "to": [{"namespaceSelector": {"matchLabels": {"name": "kube-system"}}}],
                    "ports": [{"protocol": "UDP", "port": 53}],
                }],
            },
        })

        return policies

    def generate_pod_security(self) -> dict[str, Any]:
        """Generate pod security standards configuration."""
        if self.standard == PodSecurityStandard.RESTRICTED:
            return {
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": self.namespace,
                    "labels": {
                        "pod-security.kubernetes.io/enforce": "restricted",
                        "pod-security.kubernetes.io/audit": "restricted",
                        "pod-security.kubernetes.io/warn": "restricted",
                    },
                },
            }
        return {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": self.namespace,
                "labels": {
                    "pod-security.kubernetes.io/enforce": self.standard.value,
                },
            },
        }


# ---------------------------------------------------------------------------
# Secrets Management
# ---------------------------------------------------------------------------

class SecretsManager:
    """Configure and manage secrets across environments."""

    def __init__(self, config: SecretsConfig | None = None) -> None:
        self.config = config or SecretsConfig()
        self._rotation_schedule: dict[str, int] = {}

    def configure_rotation(self, path: str, rotation_interval_days: int = 30,
                           notification_channels: list[str] | None = None) -> None:
        """Configure automatic secret rotation for a path."""
        self._rotation_schedule[path] = rotation_interval_days
        if notification_channels:
            self.config.notification_channels = notification_channels

    def generate_k8s_secret(self, name: str, namespace: str,
                            secret_data: dict[str, str] | None = None) -> dict[str, Any]:
        """Generate a Kubernetes Secret manifest."""
        data = secret_data or {"placeholder": "change-me"}
        import base64
        encoded = {k: base64.b64encode(v.encode()).decode() for k, v in data.items()}
        return {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {
                "name": name,
                "namespace": namespace,
                "labels": {
                    "managed-by": "security-architecture",
                },
            },
            "type": "Opaque",
            "data": encoded,
        }

    def generate_vault_policy(self, path: str, capabilities: list[str]) -> dict[str, Any]:
        """Generate a HashiCorp Vault policy."""
        return {
            "path": {
                f"secret/data/{path}": {
                    "capabilities": capabilities,
                },
            },
        }

    def get_rotation_schedule(self) -> dict[str, int]:
        return dict(self._rotation_schedule)


# ---------------------------------------------------------------------------
# Service Mesh Configuration
# ---------------------------------------------------------------------------

class ServiceMeshConfigurator:
    """Configure service mesh security settings."""

    def __init__(self, mesh_name: str = "istio") -> None:
        self.mesh_name = mesh_name
        self._services: dict[str, ServiceMeshConfig] = {}

    def configure_service(self, name: str, **kwargs: Any) -> ServiceMeshConfig:
        """Configure security for a service."""
        config = ServiceMeshConfig(name=name, **kwargs)
        self._services[name] = config
        return config

    def get_mtls_status(self) -> dict[str, str]:
        return {name: cfg.mtls_mode for name, cfg in self._services.items()}

    def validate_all_strict_mtls(self) -> list[str]:
        """Check that all services enforce strict mTLS."""
        violations: list[str] = []
        for name, cfg in self._services.items():
            if cfg.mtls_mode != "STRICT":
                violations.append(
                    f"Service '{name}' mTLS is '{cfg.mtls_mode}', expected 'STRICT'"
                )
        return violations


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the security architecture framework."""
    print("=" * 60)
    print("  Security Architecture Framework Demo")
    print("=" * 60)

    # --- Zero Trust Network ---
    print("\n--- Zero Trust Network Policy ---")
    segments = [
        NetworkSegment(name="web", tier="public", cidr="10.0.1.0/24",
                       allowed_inbound=["0.0.0.0/0"],
                       allowed_outbound=["10.0.2.0/24"]),
        NetworkSegment(name="app", tier="internal", cidr="10.0.2.0/24",
                       allowed_inbound=["10.0.1.0/24"],
                       allowed_outbound=["10.0.3.0/24"]),
        NetworkSegment(name="data", tier="restricted", cidr="10.0.3.0/24",
                       allowed_inbound=["10.0.2.0/24"],
                       allowed_outbound=[]),
    ]
    zt = ZeroTrustPolicy(segments)
    rules = zt.generate_rules()
    for r in rules:
        print(f"  ALLOW {r.protocol}:{r.port} {r.source_cidr} → {r.dest_cidr}")

    violations = zt.validate_no_direct_access()
    if violations:
        for v in violations:
            print(f"  ⚠ {v}")
    else:
        print("  ✓ No direct access violations detected")

    # --- IAM Roles ---
    print("\n--- IAM Role Definitions ---")
    iam = IAMPolicyBuilder()
    iam.add_role(IAMRole(
        name="deployment-role",
        permissions=IAMPermissionSet(
            allow=["s3:GetObject", "s3:PutObject"],
            deny=["s3:DeleteBucket"],
        ),
        scope=ResourceScope(arn_pattern="arn:aws:s3:::prod-deploy-*"),
        session_duration_max_hours=1, require_mfa=True,
    ))
    iam.add_role(IAMRole(
        name="admin-role",
        permissions=IAMPermissionSet(allow=["*"]),
        scope=ResourceScope(arn_pattern="*"),
        session_duration_max_hours=8, require_mfa=True,
    ))

    warnings = iam.validate_least_privilege()
    for w in warnings:
        print(f"  ⚠ {w}")

    roles = iam.list_roles()
    for r in roles:
        print(f"  Role: {r['name']}, MFA: {r['mfa']}, "
              f"Session: {r['max_session_h']}h")

    # --- Kubernetes Security ---
    print("\n--- Kubernetes Security ---")
    k8s = K8sSecurityPolicy(namespace="production",
                             standard=PodSecurityStandard.RESTRICTED)
    net_policies = k8s.generate_network_policies()
    print(f"  Network policies: {len(net_policies)}")
    for p in net_policies:
        print(f"    - {p['metadata']['name']}")

    pod_sec = k8s.generate_pod_security()
    enforce = pod_sec["metadata"]["labels"].get("pod-security.kubernetes.io/enforce")
    print(f"  Pod security enforce: {enforce}")

    # --- Secrets Management ---
    print("\n--- Secrets Management ---")
    secrets_mgr = SecretsManager(SecretsConfig(
        backend="vault", addr="https://vault.internal:8200",
        auth_method=AuthMethod.KUBERNETES,
    ))
    secrets_mgr.configure_rotation("database/prod", rotation_interval_days=30)
    secrets_mgr.configure_rotation("api-keys/prod", rotation_interval_days=7)

    k8s_secret = secrets_mgr.generate_k8s_secret(
        "db-credentials", "production",
        {"username": "admin", "password": "s3cret!pass"}
    )
    print(f"  K8s Secret: {k8s_secret['metadata']['name']} "
          f"({len(k8s_secret['data'])} fields)")

    vault_policy = secrets_mgr.generate_vault_policy(
        "database/prod", ["read", "list"]
    )
    print(f"  Vault policy: {list(vault_policy['path'].keys())}")
    print(f"  Rotation schedule: {secrets_mgr.get_rotation_schedule()}")

    # --- Service Mesh ---
    print("\n--- Service Mesh ---")
    mesh = ServiceMeshConfigurator("istio")
    mesh.configure_service("web-frontend", mtls_mode="STRICT")
    mesh.configure_service("api-backend", mtls_mode="STRICT")
    mesh.configure_service("legacy-service", mtls_mode="PERMISSIVE")

    mtls_status = mesh.get_mtls_status()
    for svc, mode in mtls_status.items():
        print(f"  {svc}: mTLS={mode}")

    violations = mesh.validate_all_strict_mtls()
    for v in violations:
        print(f"  ⚠ {v}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
