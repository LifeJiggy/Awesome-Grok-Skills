"""
Terraform & CloudFormation Module
Infrastructure as Code management for cloud provisioning
"""

from __future__ import annotations

import json
import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProviderType(Enum):
    AWS = "aws"
    AZURE = "azurerm"
    GCP = "google"
    KUBERNETES = "kubernetes"
    ALICLOUD = "alicloud"
    DIGITALOCEAN = "digitalocean"


class ResourceType(Enum):
    COMPUTE = "compute"
    NETWORK = "network"
    STORAGE = "storage"
    DATABASE = "database"
    SECURITY = "security"
    MONITORING = "monitoring"
    DNS = "dns"


class ChangeAction(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    NO_OP = "no-op"


class StackStatus(Enum):
    CREATE_IN_PROGRESS = "CREATE_IN_PROGRESS"
    CREATE_COMPLETE = "CREATE_COMPLETE"
    CREATE_FAILED = "CREATE_FAILED"
    ROLLBACK_IN_PROGRESS = "ROLLBACK_IN_PROGRESS"
    ROLLBACK_COMPLETE = "ROLLBACK_COMPLETE"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_COMPLETE = "UPDATE_COMPLETE"
    UPDATE_FAILED = "UPDATE_FAILED"
    DELETE_IN_PROGRESS = "DELETE_IN_PROGRESS"
    DELETE_COMPLETE = "DELETE_COMPLETE"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Provider:
    """Cloud provider configuration."""
    name: str
    version: str = "latest"
    config: Dict[str, Any] = field(default_factory=dict)
    alias: Optional[str] = None

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType(self.name)


@dataclass
class Variable:
    """Terraform variable definition."""
    name: str
    type: str = "string"
    description: str = ""
    default: Any = None
    sensitive: bool = False
    validation: Optional[Dict[str, Any]] = None


@dataclass
class Output:
    """Terraform output definition."""
    name: str
    description: str = ""
    value: str = ""
    sensitive: bool = False


@dataclass
class Module:
    """Terraform module reference."""
    name: str
    source: str
    version: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)

    @property
    def source_id(self) -> str:
        return f"{self.source}@{self.version or 'latest'}"


@dataclass
class Resource:
    """CloudFormation or Terraform resource."""
    type: str
    logical_id: str
    properties: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    condition: Optional[str] = None


@dataclass
class PlanResult:
    """Result of a Terraform plan operation."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    added: int = 0
    changed: int = 0
    destroyed: int = 0
    unchanged: int = 0
    resource_changes: List[Dict[str, Any]] = field(default_factory=list)
    cost_estimate: str = "$0.00"
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return self.added > 0 or self.changed > 0 or self.destroyed > 0

    @property
    def total_changes(self) -> int:
        return self.added + self.changed + self.destroyed


@dataclass
class ApplyResult:
    """Result of a Terraform apply operation."""
    apply_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    resources_created: int = 0
    resources_updated: int = 0
    resources_destroyed: int = 0
    duration_seconds: float = 0.0
    state_serial: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


@dataclass
class ApprovalGate:
    """Approval gate for apply operations."""
    approvers: List[str] = field(default_factory=list)
    timeout_hours: int = 24
    required_approvals: int = 1
    _approvals: List[str] = field(default_factory=list, repr=False)

    def request_approval(self, plan: PlanResult) -> bool:
        logger.info("Approval requested from %s for plan %s", self.approvers, plan.plan_id)
        return len(self._approvals) >= self.required_approvals

    def approve(self, approver: str) -> None:
        if approver in self.approvers:
            self._approvals.append(approver)


@dataclass
class CloudFormationParameter:
    """CloudFormation template parameter."""
    parameter_key: str
    parameter_value: str
    use_previous_value: bool = False


@dataclass
class StackEvent:
    """CloudFormation stack event."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    logical_resource_id: str = ""
    physical_resource_id: str = ""
    resource_type: str = ""
    resource_status: str = ""
    status_reason: str = ""


@dataclass
class Stack:
    """CloudFormation stack."""
    name: str
    template: Dict[str, Any] = field(default_factory=dict)
    parameters: List[CloudFormationParameter] = field(default_factory=list)
    status: StackStatus = StackStatus.CREATE_COMPLETE
    events: List[StackEvent] = field(default_factory=list)
    outputs: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: Dict[str, str] = field(default_factory=dict)
    rollback_on_failure: bool = True


# ---------------------------------------------------------------------------
# Terraform Manager
# ---------------------------------------------------------------------------

class TerraformManager:
    """Manages Terraform configurations and operations."""

    def __init__(self, work_dir: str = ".") -> None:
        self.work_dir = work_dir
        self._providers: List[Provider] = []
        self._modules: List[Module] = []
        self._variables: List[Variable] = []
        self._outputs: List[Output] = []

    def add_provider(self, provider: Provider) -> None:
        self._providers.append(provider)

    def add_module(self, module: Module) -> None:
        self._modules.append(module)

    def add_variable(self, variable: Variable) -> None:
        self._variables.append(variable)

    def add_output(self, output: Output) -> None:
        self._outputs.append(output)

    def generate(self) -> str:
        parts = []

        # Generate provider blocks
        for provider in self._providers:
            block = f'provider "{provider.name}" {{\n'
            for key, value in provider.config.items():
                block += f'  {key} = "{value}"\n'
            block += "}\n"
            parts.append(block)

        # Generate module blocks
        for module in self._modules:
            block = f'module "{module.name}" {{\n'
            block += f'  source  = "{module.source}"\n'
            if module.version:
                block += f'  version = "{module.version}"\n'
            for key, value in module.variables.items():
                if isinstance(value, str):
                    block += f'  {key} = "{value}"\n'
                elif isinstance(value, list):
                    block += f'  {key} = {json.dumps(value)}\n'
                elif isinstance(value, bool):
                    block += f'  {key} = {"true" if value else "false"}\n'
                else:
                    block += f'  {key} = {value}\n'
            block += "}\n"
            parts.append(block)

        # Generate variable blocks
        for var in self._variables:
            block = f'variable "{var.name}" {{\n'
            block += f'  type    = {var.type}\n'
            if var.description:
                block += f'  description = "{var.description}"\n'
            if var.default is not None:
                if isinstance(var.default, str):
                    block += f'  default     = "{var.default}"\n'
                else:
                    block += f'  default     = {json.dumps(var.default)}\n'
            if var.sensitive:
                block += '  sensitive   = true\n'
            block += "}\n"
            parts.append(block)

        # Generate output blocks
        for output in self._outputs:
            block = f'output "{output.name}" {{\n'
            block += f'  value = {output.value}\n'
            if output.description:
                block += f'  description = "{output.description}"\n'
            if output.sensitive:
                block += '  sensitive = true\n'
            block += "}\n"
            parts.append(block)

        return "\n".join(parts)


# ---------------------------------------------------------------------------
# Terraform Workflow
# ---------------------------------------------------------------------------

class TerraformWorkflow:
    """Orchestrates Terraform plan/apply workflows."""

    def __init__(self, work_dir: str = ".") -> None:
        self.work_dir = work_dir
        self._plan_history: List[PlanResult] = []

    def plan(
        self,
        var_file: Optional[str] = None,
        parallelism: int = 10,
        target: Optional[str] = None,
    ) -> PlanResult:
        plan = PlanResult(
            added=3,
            changed=2,
            destroyed=0,
            unchanged=15,
            cost_estimate="$45.20/month",
            resource_changes=[
                {"address": "aws_instance.web", "action": "create"},
                {"address": "aws_security_group.web", "action": "create"},
                {"address": "aws_s3_bucket.data", "action": "create"},
                {"address": "aws_route53_record.app", "action": "update"},
                {"address": "aws_iam_role.lambda", "action": "update"},
            ],
        )
        self._plan_history.append(plan)
        return plan

    def apply(self, auto_approve: bool = False) -> ApplyResult:
        return ApplyResult(
            resources_created=3,
            resources_updated=2,
            resources_destroyed=0,
            duration_seconds=45.2,
            state_serial=42,
        )

    def destroy(self, target: Optional[str] = None) -> ApplyResult:
        return ApplyResult(
            resources_destroyed=5,
            duration_seconds=30.1,
        )


# ---------------------------------------------------------------------------
# CloudFormation Generator
# ---------------------------------------------------------------------------

class CloudFormationGenerator:
    """Generates AWS CloudFormation templates."""

    def __init__(self, template_name: str = "", description: str = "") -> None:
        self.template_name = template_name
        self.description = description
        self._resources: List[Resource] = []
        self._parameters: List[Dict[str, Any]] = []
        self._outputs: List[Dict[str, Any]] = []
        self._conditions: Dict[str, Any] = {}

    def add_resource(self, resource: Resource) -> None:
        self._resources.append(resource)

    def add_parameter(self, name: str, type: str = "String", description: str = "", default: Any = None) -> None:
        param: Dict[str, Any] = {"Type": type}
        if description:
            param["Description"] = description
        if default is not None:
            param["Default"] = default
        self._parameters.append({"ParameterKey": name, **param})

    def add_output(self, name: str, description: str = "", value: Any = None, export_name: Optional[str] = None) -> None:
        output: Dict[str, Any] = {"Description": description}
        if value:
            output["Value"] = value
        if export_name:
            output["Export"] = {"Name": export_name}
        self._outputs.append({"OutputKey": name, **output})

    def add_condition(self, name: str, condition: Any) -> None:
        self._conditions[name] = condition

    def generate(self) -> str:
        template: Dict[str, Any] = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": self.description,
        }

        if self._parameters:
            template["Parameters"] = {
                p["ParameterKey"]: {k: v for k, v in p.items() if k != "ParameterKey"}
                for p in self._parameters
            }

        if self._conditions:
            template["Conditions"] = self._conditions

        template["Resources"] = {
            r.logical_id: {
                "Type": r.type,
                "Properties": r.properties,
            }
            for r in self._resources
        }

        if self._outputs:
            template["Outputs"] = {
                o["OutputKey"]: {k: v for k, v in o.items() if k != "OutputKey"}
                for o in self._outputs
            }

        return json.dumps(template, indent=2)


# ---------------------------------------------------------------------------
# Stack Manager
# ---------------------------------------------------------------------------

class StackManager:
    """Manages CloudFormation stacks."""

    def __init__(self) -> None:
        self._stacks: Dict[str, Stack] = {}

    def create_stack(self, stack: Stack) -> Stack:
        stack.status = StackStatus.CREATE_IN_PROGRESS
        stack.events.append(StackEvent(
            logical_resource_id=stack.name,
            resource_type="AWS::CloudFormation::Stack",
            resource_status="CREATE_IN_PROGRESS",
        ))
        # Simulate successful creation
        stack.status = StackStatus.CREATE_COMPLETE
        stack.events.append(StackEvent(
            logical_resource_id=stack.name,
            resource_type="AWS::CloudFormation::Stack",
            resource_status="CREATE_COMPLETE",
        ))
        self._stacks[stack.name] = stack
        return stack

    def update_stack(self, stack_name: str, template: Dict[str, Any]) -> Optional[Stack]:
        stack = self._stacks.get(stack_name)
        if stack is None:
            return None
        stack.status = StackStatus.UPDATE_IN_PROGRESS
        stack.template = template
        stack.updated_at = datetime.utcnow()
        stack.status = StackStatus.UPDATE_COMPLETE
        return stack

    def delete_stack(self, stack_name: str) -> bool:
        stack = self._stacks.get(stack_name)
        if stack is None:
            return False
        stack.status = StackStatus.DELETE_IN_PROGRESS
        stack.status = StackStatus.DELETE_COMPLETE
        del self._stacks[stack_name]
        return True

    def describe_stack(self, stack_name: str) -> Optional[Stack]:
        return self._stacks.get(stack_name)

    def list_stacks(self) -> List[Stack]:
        return list(self._stacks.values())


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Terraform & CloudFormation module."""
    print("=" * 60)
    print("  Terraform & CloudFormation Module — Demo")
    print("=" * 60)

    # Terraform configuration
    tf_manager = TerraformManager(work_dir="/infra/terraform")
    tf_manager.add_provider(Provider(name="aws", version="~> 5.0", config={"region": "us-east-1"}))
    tf_manager.add_module(Module(
        name="vpc",
        source="terraform-aws-modules/vpc/aws",
        version="5.0.0",
        variables={"cidr": "10.0.0.0/16", "azs": ["us-east-1a", "us-east-1b"]},
    ))
    tf_manager.add_variable(Variable(name="environment", type="string", default="production"))
    tf_manager.add_output(Output(name="vpc_id", value="module.vpc.vpc_id"))

    config = tf_manager.generate()
    print(f"\n[+] Terraform Configuration ({len(config)} chars):")
    print(config[:300] + "...")

    # Plan workflow
    workflow = TerraformWorkflow(work_dir="/infra/terraform")
    plan = workflow.plan(var_file="production.tfvars")
    print(f"\n[+] Plan Result:")
    print(f"    Added: {plan.added}, Changed: {plan.changed}, Destroyed: {plan.destroyed}")
    print(f"    Cost: {plan.cost_estimate}")
    print(f"    Has Changes: {plan.has_changes}")

    # Apply
    if plan.has_changes:
        apply_result = workflow.apply()
        print(f"\n[+] Apply Result:")
        print(f"    Created: {apply_result.resources_created}, Updated: {apply_result.resources_updated}")
        print(f"    Duration: {apply_result.duration_seconds:.1f}s")

    # CloudFormation
    cf_generator = CloudFormationGenerator(
        template_name="production-stack",
        description="Production infrastructure stack",
    )
    cf_generator.add_parameter("Environment", type="String", default="production")
    cf_generator.add_resource(Resource(
        type="AWS::EC2::VPC",
        logical_id="ProductionVPC",
        properties={"CidrBlock": "10.0.0.0/16", "EnableDnsHostnames": True},
    ))
    cf_generator.add_resource(Resource(
        type="AWS::EC2::Subnet",
        logical_id="PublicSubnet1",
        properties={"VpcId": {"Ref": "ProductionVPC"}, "CidrBlock": "10.0.1.0/24"},
    ))
    cf_generator.add_output("VPCId", description="Production VPC ID", value={"Ref": "ProductionVPC"})

    template = cf_generator.generate()
    print(f"\n[+] CloudFormation Template ({len(template)} chars):")
    print(template[:300] + "...")

    # Stack management
    stack_manager = StackManager()
    stack = stack_manager.create_stack(Stack(
        name="production-stack",
        template=json.loads(template),
    ))
    print(f"\n[+] Stack Created:")
    print(f"    Name: {stack.name}")
    print(f"    Status: {stack.status.value}")
    print(f"    Events: {len(stack.events)}")

    stacks = stack_manager.list_stacks()
    print(f"    Total Stacks: {len(stacks)}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
