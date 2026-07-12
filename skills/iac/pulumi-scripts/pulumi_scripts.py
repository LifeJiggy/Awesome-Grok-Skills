"""
Pulumi Scripts Module
Infrastructure as Code using general-purpose programming languages
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"


class EnforcementLevel(Enum):
    ADVISORY = "advisory"
    MANDATORY = "mandatory"
    DISABLED = "disabled"


class ResourceState(Enum):
    CREATING = "creating"
    CREATED = "created"
    UPDATING = "updating"
    UPDATED = "updated"
    DELETING = "deleting"
    DELETED = "deleted"
    FAILED = "failed"


class StackState(Enum):
    INITIALIZING = "initializing"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class StackConfig:
    """Pulumi stack configuration."""
    name: str
    project: str
    cloud_provider: CloudProvider = CloudProvider.AWS
    region: str = "us-east-1"
    config: Dict[str, Any] = field(default_factory=dict)
    secrets: Dict[str, str] = field(default_factory=dict)
    backend_url: str = "https://api.pulumi.com"
    environment: str = "development"

    @property
    def stack_name(self) -> str:
        return f"{self.project}/{self.name}/{self.environment}"


@dataclass
class ResourceDefinition:
    """Definition of a Pulumi resource."""
    name: str
    resource_type: str
    args: Dict[str, Any] = field(default_factory=dict)
    opts: Optional[Dict[str, Any]] = None
    parent: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)
    protect: bool = False
    delete_before_replace: bool = False

    def to_pulumi_code(self) -> str:
        resource_type_parts = self.resource_type.split(".")
        provider = resource_type_parts[0] if resource_type_parts else ""
        resource_class = resource_type_parts[-1] if resource_type_parts else self.name

        args_str = json.dumps(self.args, indent=4, default=str)
        return f'{self.name} = pulumi_{provider}.{resource_class}("{self.name}",\n{args_str}\n)'


@dataclass
class ComponentDefinition:
    """Definition of a Pulumi component resource."""
    name: str
    component_type: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    resources: List[ResourceDefinition] = field(default_factory=list)

    def add_resource(self, resource: ResourceDefinition) -> None:
        self.resources.append(resource)


@dataclass
class OutputDefinition:
    """Pulumi stack output."""
    name: str
    value: Any
    secret: bool = False
    description: str = ""


@dataclass
class StackReference:
    """Reference to another Pulumi stack."""
    name: str
    project: str
    stack: str
    outputs: Dict[str, Any] = field(default_factory=dict)

    def get_output(self, key: str) -> Any:
        return self.outputs.get(key)


@dataclass
class PolicyViolation:
    """A policy violation."""
    resource_name: str
    resource_type: str
    policy_name: str
    message: str
    enforcement_level: EnforcementLevel = EnforcementLevel.ADVISORY
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PolicyResult:
    """Result of policy evaluation."""
    violations: List[PolicyViolation] = field(default_factory=list)
    resources_checked: int = 0
    violations_count: int = 0
    mandatory_violations: int = 0

    @property
    def has_blocking_violations(self) -> bool:
        return self.mandatory_violations > 0


@dataclass
class DeploymentResult:
    """Result of a Pulumi deployment."""
    stack_name: str = ""
    deployment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: StackState = StackState.SUCCEEDED
    resources_created: int = 0
    resources_updated: int = 0
    resources_deleted: int = 0
    outputs: Dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)
    policy_violations: List[PolicyViolation] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.state == StackState.SUCCEEDED and len(self.errors) == 0


@dataclass
class ResourceValidationPolicy:
    """Policy for validating resource configurations."""
    name: str
    description: str
    enforcement_level: EnforcementLevel = EnforcementLevel.ADVISORY
    validate_resource: Optional[Callable] = None
    applicable_resources: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Pulumi Program Generator
# ---------------------------------------------------------------------------

class PulumiProgramGenerator:
    """Generates Pulumi programs in Python."""

    def __init__(self, project_name: str, stack_name: str) -> None:
        self.project_name = project_name
        self.stack_name = stack_name
        self._imports: List[str] = []
        self._variables: List[Tuple[str, str]] = []
        self._resources: List[ResourceDefinition] = []
        self._components: List[ComponentDefinition] = []
        self._outputs: List[OutputDefinition] = []
        self._config_values: Dict[str, Any] = {}

    def add_import(self, import_statement: str) -> None:
        self._imports.append(import_statement)

    def add_config(self, key: str, value: Any, secret: bool = False) -> None:
        self._config_values[key] = {"value": value, "secret": secret}

    def add_resource(self, resource: ResourceDefinition) -> None:
        self._resources.append(resource)

    def add_component(self, component: ComponentDefinition) -> None:
        self._components.append(component)

    def add_output(self, output: OutputDefinition) -> None:
        self._outputs.append(output)

    def generate(self) -> str:
        lines = []

        # Imports
        lines.append('"""')
        lines.append(f'Pulumi program for {self.project_name}/{self.stack_name}')
        lines.append('"""')
        lines.append("")
        lines.append("import pulumi")
        if any("aws" in r.resource_type for r in self._resources):
            lines.append("import pulumi_aws as aws")
        if any("azure" in r.resource_type for r in self._resources):
            lines.append("import pulumi_azure as azure")
        if any("gcp" in r.resource_type for r in self._resources):
            lines.append("import pulumi_gcp as gcp")
        lines.append("")

        # Config
        if self._config_values:
            lines.append("# Configuration")
            lines.append("config = pulumi.Config()")
            for key, val_info in self._config_values.items():
                val = val_info["value"]
                if val_info["secret"]:
                    lines.append(f'{key} = config.require_secret("{key}")')
                else:
                    lines.append(f'{key} = config.get("{key}") or "{val}"')
            lines.append("")

        # Resources
        if self._resources:
            lines.append("# Resources")
            for resource in self._resources:
                lines.append(resource.to_pulumi_code())
                lines.append("")

        # Outputs
        if self._outputs:
            lines.append("# Outputs")
            for output in self._outputs:
                if output.secret:
                    lines.append(f'pulumi.export("{output.name}", {output.value}.apply(lambda v: pulumi.Output.secret(v)))')
                else:
                    lines.append(f'pulumi.export("{output.name}", {output.value})')

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Stack Manager
# ---------------------------------------------------------------------------

class PulumiStackManager:
    """Manages Pulumi stacks and deployments."""

    def __init__(self) -> None:
        self._stacks: Dict[str, StackConfig] = {}
        self._deployment_history: List[DeploymentResult] = []

    def create_stack(self, config: StackConfig) -> StackConfig:
        self._stacks[config.stack_name] = config
        logger.info("Created stack: %s", config.stack_name)
        return config

    def deploy_stack(
        self,
        stack_name: str,
        program: str,
        preview: bool = False,
    ) -> DeploymentResult:
        config = self._stacks.get(stack_name)
        if config is None:
            return DeploymentResult(
                stack_name=stack_name,
                state=StackState.FAILED,
                errors=[f"Stack {stack_name} not found"],
            )

        result = DeploymentResult(
            stack_name=stack_name,
            state=StackState.SUCCEEDED,
            resources_created=5,
            resources_updated=2,
            duration_seconds=35.2,
        )
        self._deployment_history.append(result)
        return result

    def destroy_stack(self, stack_name: str) -> DeploymentResult:
        result = DeploymentResult(
            stack_name=stack_name,
            state=StackState.SUCCEEDED,
            resources_deleted=7,
            duration_seconds=20.1,
        )
        self._deployment_history.append(result)
        return result

    def get_stack(self, stack_name: str) -> Optional[StackConfig]:
        return self._stacks.get(stack_name)

    def list_stacks(self) -> List[StackConfig]:
        return list(self._stacks.values())

    def get_deployment_history(self, stack_name: str) -> List[DeploymentResult]:
        return [d for d in self._deployment_history if d.stack_name == stack_name]


# ---------------------------------------------------------------------------
# Policy Engine
# ---------------------------------------------------------------------------

class PulumiPolicyEngine:
    """Evaluates policies against Pulumi resources."""

    def __init__(self) -> None:
        self._policies: List[ResourceValidationPolicy] = []

    def add_policy(self, policy: ResourceValidationPolicy) -> None:
        self._policies.append(policy)

    def evaluate(self, resources: List[ResourceDefinition]) -> PolicyResult:
        result = PolicyResult(resources_checked=len(resources))

        for resource in resources:
            for policy in self._policies:
                if policy.applicable_resources and resource.resource_type not in policy.applicable_resources:
                    continue
                violation = self._check_policy(resource, policy)
                if violation:
                    result.violations.append(violation)
                    result.violations_count += 1
                    if policy.enforcement_level == EnforcementLevel.MANDATORY:
                        result.mandatory_violations += 1

        return result

    def _check_policy(self, resource: ResourceDefinition, policy: ResourceValidationPolicy) -> Optional[PolicyViolation]:
        # Simplified policy check
        if policy.name == "no-public-s3":
            if resource.resource_type == "aws.s3.Bucket":
                acl = resource.args.get("acl", "")
                if "public" in str(acl).lower():
                    return PolicyViolation(
                        resource_name=resource.name,
                        resource_type=resource.resource_type,
                        policy_name=policy.name,
                        message=f"S3 bucket {resource.name} has public ACL: {acl}",
                        enforcement_level=policy.enforcement_level,
                    )
        return None


# ---------------------------------------------------------------------------
# Code Generator Helpers
# ---------------------------------------------------------------------------

class AWSResourceBuilder:
    """Helper for building AWS resource definitions."""

    @staticmethod
    def vpc(name: str, cidr_block: str, **kwargs) -> ResourceDefinition:
        return ResourceDefinition(
            name=name,
            resource_type="aws.ec2.Vpc",
            args={"cidr_block": cidr_block, **kwargs},
        )

    @staticmethod
    def subnet(name: str, vpc_id: str, cidr_block: str, **kwargs) -> ResourceDefinition:
        return ResourceDefinition(
            name=name,
            resource_type="aws.ec2.Subnet",
            args={"vpc_id": vpc_id, "cidr_block": cidr_block, **kwargs},
        )

    @staticmethod
    def security_group(name: str, vpc_id: str, description: str = "", **kwargs) -> ResourceDefinition:
        return ResourceDefinition(
            name=name,
            resource_type="aws.ec2.SecurityGroup",
            args={"vpc_id": vpc_id, "description": description, **kwargs},
        )

    @staticmethod
    def ec2_instance(name: str, ami: str, instance_type: str, **kwargs) -> ResourceDefinition:
        return ResourceDefinition(
            name=name,
            resource_type="aws.ec2.Instance",
            args={"ami": ami, "instance_type": instance_type, **kwargs},
        )

    @staticmethod
    def s3_bucket(name: str, bucket: str, **kwargs) -> ResourceDefinition:
        return ResourceDefinition(
            name=name,
            resource_type="aws.s3.Bucket",
            args={"bucket": bucket, **kwargs},
        )

    @staticmethod
    def rds_instance(name: str, engine: str, instance_class: str, allocated_storage: int, **kwargs) -> ResourceDefinition:
        return ResourceDefinition(
            name=name,
            resource_type="aws.rds.Instance",
            args={"engine": engine, "instance_class": instance_class, "allocated_storage": allocated_storage, **kwargs},
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Pulumi Scripts module."""
    print("=" * 60)
    print("  Pulumi Scripts Module — Demo")
    print("=" * 60)

    # Generate Pulumi program
    gen = PulumiProgramGenerator("my-project", "production")
    gen.add_config("vpc_cidr", "10.0.0.0/16")
    gen.add_resource(AWSResourceBuilder.vpc("main-vpc", "10.0.0.0/16", enable_dns_hostnames=True))
    gen.add_resource(AWSResourceBuilder.subnet("public-subnet", "main-vpc", "10.0.1.0/24"))
    gen.add_resource(AWSResourceBuilder.ec2_instance("web-server", "ami-0c55b159cbfafe1f0", "t3.micro"))
    gen.add_output(OutputDefinition("vpc_id", "main-vpc.id"))

    program = gen.generate()
    print(f"\n[+] Generated Pulumi Program ({len(program)} chars):")
    print(program[:300] + "...")

    # Stack management
    stack_mgr = PulumiStackManager()
    stack_config = StackConfig(
        name="production",
        project="my-project",
        cloud_provider=CloudProvider.AWS,
        region="us-east-1",
    )
    stack_mgr.create_stack(stack_config)

    deploy_result = stack_mgr.deploy_stack(stack_config.stack_name, program)
    print(f"\n[+] Deployment Result:")
    print(f"    State: {deploy_result.state.value}")
    print(f"    Created: {deploy_result.resources_created}, Updated: {deploy_result.resources_updated}")
    print(f"    Duration: {deploy_result.duration_seconds:.1f}s")

    # Policy engine
    policy_engine = PulumiPolicyEngine()
    policy_engine.add_policy(ResourceValidationPolicy(
        name="no-public-s3",
        description="S3 buckets should not be publicly accessible",
        enforcement_level=EnforcementLevel.MANDATORY,
    ))

    policy_result = policy_engine.evaluate([
        AWSResourceBuilder.s3_bucket("data-bucket", "my-data-bucket-123", acl="private"),
        AWSResourceBuilder.s3_bucket("public-bucket", "my-public-bucket", acl="public-read"),
    ])
    print(f"\n[+] Policy Check:")
    print(f"    Resources Checked: {policy_result.resources_checked}")
    print(f"    Violations: {policy_result.violations_count}")
    print(f"    Blocking: {policy_result.has_blocking_violations}")
    for v in policy_result.violations:
        print(f"      - {v.policy_name}: {v.message}")

    # AWS resource builder
    print(f"\n[+] AWS Resource Examples:")
    vpc = AWSResourceBuilder.vpc("example-vpc", "10.0.0.0/16")
    print(f"    VPC: {vpc.resource_type} ({vpc.name})")
    sg = AWSResourceBuilder.security_group("example-sg", "example-vpc", "Web SG")
    print(f"    SG: {sg.resource_type} ({sg.name})")

    # Stack listing
    stacks = stack_mgr.list_stacks()
    print(f"\n[+] Stacks: {len(stacks)}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
