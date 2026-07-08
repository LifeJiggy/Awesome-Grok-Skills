"""AWS Specialist Agent - AWS Cloud Services and Architecture."""

from __future__ import annotations

import logging
import time
import json
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum
from datetime import datetime, timedelta
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aws-specialist-agent")


class InstanceType(Enum):
    T3_MICRO = "t3.micro"
    T3_SMALL = "t3.small"
    T3_MEDIUM = "t3.medium"
    M5_LARGE = "m5.large"
    M5_XLARGE = "m5.xlarge"
    C5_LARGE = "c5.large"
    C5_XLARGE = "c5.xlarge"
    R5_LARGE = "r5.large"
    R5_XLARGE = "r5.xlarge"
    P3_2XLARGE = "p3.2xlarge"
    G4DN_XLARGE = "g4dn.xlarge"


class InstanceState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    TERMINATED = "terminated"
    SHUTTING_DOWN = "shutting-down"


class DatabaseEngine(Enum):
    MYSQL = "mysql"
    POSTGRES = "postgres"
    MARIADB = "mariadb"
    ORACLE = "oracle"
    SQLSERVER = "sqlserver"
    AURORA = "aurora"
    AURORA_MYSQL = "aurora-mysql"
    AURORA_POSTGRES = "aurora-postgres"


class VolumeType(Enum):
    GP2 = "gp2"
    GP3 = "gp3"
    IO1 = "io1"
    IO2 = "io2"
    ST1 = "st1"
    SC1 = "sc1"


class LoadBalancerType(Enum):
    APPLICATION = "application"
    NETWORK = "network"
    GATEWAY = "gateway"


@dataclass
class Metric:
    name: str
    value: Any
    unit: str = "count"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    def __init__(self) -> None:
        self._metrics: List[Metric] = []

    def record(self, name: str, value: Any, unit: str = "count", **tags: str) -> None:
        metric = Metric(name=name, value=value, unit=unit, tags=tags)
        self._metrics.append(metric)
        logger.info(f"Metric recorded: {name}={value} {unit}")

    def get_metrics(self, name: Optional[str] = None) -> List[Metric]:
        if name:
            return [m for m in self._metrics if m.name == name]
        return list(self._metrics)

    def clear(self) -> None:
        self._metrics.clear()


@dataclass
class Config:
    region: str = "us-east-1"
    default_instance_type: str = "t3.micro"
    auto_scaling: bool = True
    enable_monitoring: bool = True
    enable_logging: bool = True
    tags: Dict[str, str] = field(default_factory=dict)
    max_instances: int = 10
    vpc_cidr: str = "10.0.0.0/16"
    environment: str = "development"
    encryption_key_arn: Optional[str] = None
    backup_retention_days: int = 7
    multi_az: bool = False


@dataclass
class SecurityGroupRule:
    protocol: str
    from_port: int
    to_port: int
    source: str
    description: str = ""
    rule_type: str = "ingress"


@dataclass
class SecurityGroup:
    id: str
    name: str
    description: str
    ingress_rules: List[SecurityGroupRule] = field(default_factory=list)
    egress_rules: List[SecurityGroupRule] = field(default_factory=list)
    vpc_id: Optional[str] = None


@dataclass
class Subnet:
    id: str
    cidr_block: str
    availability_zone: str
    public: bool = True
    map_public_ip: bool = True


@dataclass
class VPC:
    id: str
    cidr_block: str
    name: str
    subnets: List[Subnet] = field(default_factory=list)
    security_groups: List[SecurityGroup] = field(default_factory=list)
    internet_gateway_id: Optional[str] = None
    nat_gateway_id: Optional[str] = None


@dataclass
class Volume:
    id: str
    size_gb: int
    volume_type: str
    iops: Optional[int] = None
    throughput: Optional[int] = None
    encrypted: bool = True
    availability_zone: str = "us-east-1a"


@dataclass
class NetworkInterface:
    id: str
    subnet_id: str
    security_group_ids: List[str] = field(default_factory=list)
    private_ip: str = ""
    public_ip: Optional[str] = None


@dataclass
class EC2Instance:
    id: str
    name: str
    instance_type: str
    ami_id: str
    state: str
    region: str
    availability_zone: str = "us-east-1a"
    key_name: Optional[str] = None
    security_group_ids: List[str] = field(default_factory=list)
    network_interfaces: List[NetworkInterface] = field(default_factory=list)
    volumes: List[Volume] = field(default_factory=list)
    public_ip: Optional[str] = None
    private_ip: Optional[str] = None
    iam_instance_profile: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    user_data: Optional[str] = None
    metadata_options: Dict[str, Any] = field(default_factory=dict)
    monitoring_enabled: bool = True
    ebs_optimized: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    launched_at: Optional[datetime] = None
    terminated_at: Optional[datetime] = None


@dataclass
class S3Bucket:
    name: str
    region: str
    versioning: bool = False
    encryption: str = "AES256"
    public_access_blocked: bool = True
    lifecycle_rules: List[Dict[str, Any]] = field(default_factory=list)
    cors_configuration: Optional[Dict[str, Any]] = None
    bucket_policy: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    object_count: int = 0
    total_size_bytes: int = 0


@dataclass
class LambdaFunction:
    function_name: str
    runtime: str
    handler: str
    memory_mb: int
    timeout_seconds: int
    region: str
    role_arn: str
    environment_variables: Dict[str, str] = field(default_factory=dict)
    layers: List[str] = field(default_factory=list)
    code_s3_bucket: Optional[str] = None
    code_s3_key: Optional[str] = None
    code_zip_bytes: Optional[bytes] = None
    publish: bool = False
    description: str = ""
    tags: Dict[str, str] = field(default_factory=dict)
    last_modified: datetime = field(default_factory=datetime.utcnow)
    code_sha256: str = ""
    version: str = "$LATEST"
    aws_request_id: Optional[str] = None


@dataclass
class ContainerTask:
    task_definition_arn: str
    container_definitions: List[Dict[str, Any]]
    family: str
    cpu: str
    memory: str
    network_mode: str = "awsvpc"
    requires_compatibilities: List[str] = field(default_factory=lambda: ["FARGATE"])
    execution_role_arn: str = ""
    task_role_arn: str = ""
    volumes: List[Dict[str, Any]] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class LoadBalancer:
    id: str
    name: str
    dns_name: str
    scheme: str
    type: str
    vpc_id: str
    security_group_ids: List[str] = field(default_factory=list)
    subnets: List[str] = field(default_factory=list)
    listeners: List[Dict[str, Any]] = field(default_factory=list)
    target_groups: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AutoScalingGroup:
    name: str
    launch_configuration: Dict[str, Any]
    min_size: int
    max_size: int
    desired_capacity: int
    vpc_zone_identifiers: List[str] = field(default_factory=list)
    target_group_arns: List[str] = field(default_factory=list)
    health_check_type: str = "EC2"
    health_check_grace_period: int = 300
    tags: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class CloudWatchAlarm:
    alarm_name: str
    metric_name: str
    namespace: str
    statistic: str
    period: int
    evaluation_periods: int
    threshold: float
    comparison_operator: str
    alarm_actions: List[str] = field(default_factory=list)
    ok_actions: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class IAMRole:
    role_name: str
    assume_role_policy_document: Dict[str, Any]
    policies: List[str] = field(default_factory=list)
    max_session_duration: int = 3600
    description: str = ""
    tags: Dict[str, str] = field(default_factory=dict)
    arn: str = ""


class ValidationError(Exception):
    pass


class ResourceConflictError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class AWSServiceError(Exception):
    pass


class AWSSpecialistAgent:
    """Agent for AWS cloud services with comprehensive infrastructure management."""

    def __init__(self, config: Optional[Config] = None, metrics_collector: Optional[MetricsCollector] = None) -> None:
        self._config = config or Config()
        self._metrics = metrics_collector or MetricsCollector()
        self._instances: Dict[str, EC2Instance] = {}
        self._s3_buckets: Dict[str, S3Bucket] = {}
        self._lambda_functions: Dict[str, LambdaFunction] = {}
        self._vpc_registry: Dict[str, VPC] = {}
        self._security_groups: Dict[str, SecurityGroup] = {}
        self._load_balancers: Dict[str, LoadBalancer] = {}
        self._container_tasks: Dict[str, ContainerTask] = {}
        self._auto_scaling_groups: Dict[str, AutoScalingGroup] = {}
        self._cloudwatch_alarms: Dict[str, CloudWatchAlarm] = {}
        self._iam_roles: Dict[str, IAMRole] = {}
        self._operation_history: List[Dict[str, Any]] = []
        self._start_time = datetime.utcnow()

        logger.info(f"Initialized AWSSpecialistAgent in region={self._config.region}, env={self._config.environment}")

    def _log_operation(self, operation: str, details: Dict[str, Any], status: str = "success") -> None:
        entry = {
            "operation": operation,
            "details": details,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._operation_history.append(entry)
        self._metrics.record("aws_operation", 1, operation=operation, status=status)

    def _generate_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:12]}"

    def _validate_instance_type(self, instance_type: str) -> str:
        valid_types = [e.value for e in InstanceType]
        if instance_type not in valid_types:
            raise ValidationError(f"Invalid instance type: {instance_type}. Valid types: {valid_types}")
        return instance_type

    def _validate_region(self, region: str) -> str:
        valid_regions = [
            "us-east-1", "us-east-2", "us-west-1", "us-west-2",
            "eu-west-1", "eu-west-2", "eu-central-1",
            "ap-southeast-1", "ap-southeast-2", "ap-northeast-1"
        ]
        if region not in valid_regions:
            raise ValidationError(f"Invalid region: {region}. Valid regions: {valid_regions}")
        return region

    def _validate_ami_id(self, ami_id: str) -> str:
        if not ami_id.startswith("ami-"):
            raise ValidationError(f"Invalid AMI ID format: {ami_id}. Must start with 'ami-'")
        return ami_id

    def _validate_cidr(self, cidr: str) -> str:
        import re
        pattern = r"^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)(\d{1,3}\.){2}\d{1,3}/\d{1,2}$"
        if not re.match(pattern, cidr):
            raise ValidationError(f"Invalid CIDR block: {cidr}")
        return cidr

    def provision_ec2(self, name: str, instance_type: str, ami_id: str, key_name: Optional[str] = None,
                      security_group_ids: Optional[List[str]] = None, user_data: Optional[str] = None,
                      tags: Optional[Dict[str, str]] = None, attach_volume: bool = True,
                      volume_size_gb: int = 20) -> EC2Instance:
        start = time.time()
        try:
            instance_type = self._validate_instance_type(instance_type)
            ami_id = self._validate_ami_id(ami_id)
            region = self._validate_region(self._config.region)
            if attach_volume:
                volume = Volume(
                    id=self._generate_id("vol"),
                    size_gb=volume_size_gb,
                    volume_type="gp3",
                    encrypted=True,
                    availability_zone="us-east-1a"
                )
            instance = EC2Instance(
                id=self._generate_id("i"),
                name=name,
                instance_type=instance_type,
                ami_id=ami_id,
                state=InstanceState.PENDING.value,
                region=region,
                key_name=key_name,
                security_group_ids=security_group_ids or [],
                volumes=[volume] if attach_volume else [],
                tags={**self._config.tags, **(tags or {})},
                user_data=user_data
            )
            self._instances[instance.id] = instance
            logger.info(f"Provisioned EC2 instance {instance.id} ({name})")
            self._log_operation("ec2.provision", {"instance_id": instance.id, "name": name, "type": instance_type})
            latency = (time.time() - start) * 1000
            self._metrics.record("provision_latency_ms", round(latency, 2), operation="ec2.provision")
            return instance
        except ValidationError:
            raise
        except Exception as e:
            self._log_operation("ec2.provision", {"name": name}, status="error")
            logger.error(f"Failed to provision EC2: {e}")
            raise AWSServiceError(f"EC2 provisioning failed: {e}")

    def get_instance(self, instance_id: str) -> EC2Instance:
        if instance_id not in self._instances:
            raise ResourceNotFoundError(f"Instance not found: {instance_id}")
        return self._instances[instance_id]

    def list_instances(self, state_filter: Optional[str] = None) -> List[EC2Instance]:
        instances = list(self._instances.values())
        if state_filter:
            instances = [i for i in instances if i.state == state_filter]
        return instances

    def terminate_instance(self, instance_id: str, force: bool = False) -> Dict[str, Any]:
        start = time.time()
        try:
            instance = self.get_instance(instance_id)
            instance.state = InstanceState.TERMINATED.value
            instance.terminated_at = datetime.utcnow()
            logger.info(f"Terminated EC2 instance {instance_id}")
            self._log_operation("ec2.terminate", {"instance_id": instance_id, "force": force})
            return {
                "instance_id": instance_id,
                "state": instance.state,
                "terminated_at": instance.terminated_at.isoformat()
            }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            self._log_operation("ec2.terminate", {"instance_id": instance_id}, status="error")
            logger.error(f"Failed to terminate EC2: {e}")
            raise AWSServiceError(f"EC2 termination failed: {e}")

    def start_instance(self, instance_id: str) -> Dict[str, Any]:
        start = time.time()
        try:
            instance = self.get_instance(instance_id)
            if instance.state != InstanceState.STOPPED.value:
                raise ValidationError(f"Cannot start instance in state: {instance.state}")
            instance.state = InstanceState.PENDING.value
            instance.launched_at = datetime.utcnow()
            logger.info(f"Starting EC2 instance {instance_id}")
            self._log_operation("ec2.start", {"instance_id": instance_id})
            return {"instance_id": instance_id, "state": instance.state}
        except ResourceNotFoundError:
            raise
        except ValidationError:
            raise
        except Exception as e:
            self._log_operation("ec2.start", {"instance_id": instance_id}, status="error")
            logger.error(f"Failed to start EC2: {e}")
            raise AWSServiceError(f"EC2 start failed: {e}")

    def stop_instance(self, instance_id: str, force: bool = False) -> Dict[str, Any]:
        start = time.time()
        try:
            instance = self.get_instance(instance_id)
            if instance.state not in [InstanceState.RUNNING.value, InstanceState.PENDING.value]:
                raise ValidationError(f"Cannot stop instance in state: {instance.state}")
            instance.state = InstanceState.STOPPING.value
            logger.info(f"Stopping EC2 instance {instance_id}")
            self._log_operation("ec2.stop", {"instance_id": instance_id, "force": force})
            return {"instance_id": instance_id, "state": instance.state}
        except ResourceNotFoundError:
            raise
        except ValidationError:
            raise
        except Exception as e:
            self._log_operation("ec2.stop", {"instance_id": instance_id}, status="error")
            logger.error(f"Failed to stop EC2: {e}")
            raise AWSServiceError(f"EC2 stop failed: {e}")

    def create_vpc(self, cidr_block: str, name: str, tags: Optional[Dict[str, str]] = None) -> VPC:
        cidr_block = self._validate_cidr(cidr_block)
        vpc_id = self._generate_id("vpc")
        vpc = VPC(id=vpc_id, cidr_block=cidr_block, name=name, tags=tags or {})
        self._vpc_registry[vpc_id] = vpc
        logger.info(f"Created VPC {vpc_id} ({name}) with CIDR {cidr_block}")
        self._log_operation("vpc.create", {"vpc_id": vpc_id, "cidr": cidr_block})
        return vpc

    def add_subnet(self, vpc_id: str, cidr_block: str, availability_zone: str, public: bool = True,
                   map_public_ip: bool = True) -> Subnet:
        vpc = self._vpc_registry.get(vpc_id)
        if not vpc:
            raise ResourceNotFoundError(f"VPC not found: {vpc_id}")
        cidr_block = self._validate_cidr(cidr_block)
        subnet = Subnet(
            id=self._generate_id("subnet"),
            cidr_block=cidr_block,
            availability_zone=availability_zone,
            public=public,
            map_public_ip=map_public_ip
        )
        vpc.subnets.append(subnet)
        logger.info(f"Added subnet {subnet.id} to VPC {vpc_id}")
        self._log_operation("vpc.add_subnet", {"vpc_id": vpc_id, "subnet_id": subnet.id})
        return subnet

    def create_security_group(self, vpc_id: str, name: str, description: str,
                              ingress_rules: Optional[List[SecurityGroupRule]] = None,
                              egress_rules: Optional[List[SecurityGroupRule]] = None) -> SecurityGroup:
        vpc = self._vpc_registry.get(vpc_id)
        if not vpc:
            raise ResourceNotFoundError(f"VPC not found: {vpc_id}")
        sg = SecurityGroup(
            id=self._generate_id("sg"),
            name=name,
            description=description,
            ingress_rules=ingress_rules or [],
            egress_rules=egress_rules or [SecurityGroupRule(protocol="-1", from_port=0, to_port=0, source="0.0.0.0/0", description="Allow all outbound")],
            vpc_id=vpc_id
        )
        self._security_groups[sg.id] = sg
        vpc.security_groups.append(sg)
        logger.info(f"Created security group {sg.id} ({name})")
        self._log_operation("security_group.create", {"sg_id": sg.id, "name": name})
        return sg

    def configure_s3_bucket(self, bucket_name: str, versioning: bool = False, encryption: str = "AES256",
                             lifecycle_rules: Optional[List[Dict[str, Any]]] = None, cors: Optional[Dict[str, Any]] = None,
                             tags: Optional[Dict[str, str]] = None) -> S3Bucket:
        if bucket_name in self._s3_buckets:
            raise ResourceConflictError(f"Bucket already exists: {bucket_name}")
        valid_encryption = ["AES256", "aws:kms"]
        if encryption not in valid_encryption:
            raise ValidationError(f"Invalid encryption type: {encryption}. Valid: {valid_encryption}")
        bucket = S3Bucket(
            name=bucket_name,
            region=self._config.region,
            versioning=versioning,
            encryption=encryption,
            lifecycle_rules=lifecycle_rules or [],
            cors_configuration=cors,
            tags={**self._config.tags, **(tags or {})}
        )
        self._s3_buckets[bucket_name] = bucket
        logger.info(f"Configured S3 bucket: {bucket_name}")
        self._log_operation("s3.create_bucket", {"bucket_name": bucket_name, "encryption": encryption})
        return bucket

    def upload_object_to_s3(self, bucket_name: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> Dict[str, Any]:
        bucket = self._s3_buckets.get(bucket_name)
        if not bucket:
            raise ResourceNotFoundError(f"Bucket not found: {bucket_name}")
        object_id = self._generate_id("obj")
        bucket.object_count += 1
        bucket.total_size_bytes += len(data)
        logger.info(f"Uploaded object {key} to bucket {bucket_name}")
        self._log_operation("s3.put_object", {"bucket": bucket_name, "key": key, "size": len(data)})
        return {
            "object_id": object_id,
            "bucket": bucket_name,
            "key": key,
            "size": len(data),
            "content_type": content_type,
            "etag": hashlib.md5(data).hexdigest()
        }

    def deploy_lambda(self, function_name: str, runtime: str, handler: str, memory_mb: int, timeout_seconds: int,
                      role_arn: str, code_s3_bucket: Optional[str] = None, code_s3_key: Optional[str] = None,
                      environment_variables: Optional[Dict[str, str]] = None, layers: Optional[List[str]] = None,
                      description: str = "", publish: bool = True) -> LambdaFunction:
        valid_runtimes = ["python3.9", "python3.10", "python3.11", "nodejs16.x", "nodejs18.x", "java11", "go1.x"]
        if runtime not in valid_runtimes:
            raise ValidationError(f"Invalid runtime: {runtime}. Valid: {valid_runtimes}")
        if function_name in self._lambda_functions:
            raise ResourceConflictError(f"Lambda function already exists: {function_name}")
        func = LambdaFunction(
            function_name=function_name,
            runtime=runtime,
            handler=handler,
            memory_mb=memory_mb,
            timeout_seconds=timeout_seconds,
            region=self._config.region,
            role_arn=role_arn,
            environment_variables=environment_variables or {},
            layers=layers or [],
            code_s3_bucket=code_s3_bucket,
            code_s3_key=code_s3_key,
            description=description,
            tags=self._config.tags.copy(),
            code_sha256=hashlib.sha256(b"mock").hexdigest(),
            version="$LATEST"
        )
        self._lambda_functions[function_name] = func
        logger.info(f"Deployed Lambda function: {function_name}")
        self._log_operation("lambda.deploy", {"function_name": function_name, "runtime": runtime})
        return func

    def create_rds_instance(self, db_instance_identifier: str, engine: str, db_instance_class: str,
                             master_username: str, master_password: str, allocated_storage_gb: int,
                             storage_type: str = "gp3", multi_az: bool = False, publicly_accessible: bool = False,
                             db_subnet_group_name: str = "default", tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        valid_engines = [e.value for e in DatabaseEngine]
        if engine not in valid_engines:
            raise ValidationError(f"Invalid database engine: {engine}. Valid: {valid_engines}")
        valid_storage = [v.value for v in VolumeType]
        if storage_type not in valid_storage:
            raise ValidationError(f"Invalid storage type: {storage_type}. Valid: {valid_storage}")
        if len(master_password) < 8:
            raise ValidationError("Master password must be at least 8 characters")
        instance_id = self._generate_id("db")
        logger.info(f"Provisioned RDS instance {instance_id} ({db_instance_identifier})")
        self._log_operation("rds.create_instance", {"db_instance_id": instance_id, "engine": engine})
        return {
            "db_instance_identifier": db_instance_identifier,
            "db_instance_id": instance_id,
            "engine": engine,
            "db_instance_class": db_instance_class,
            "allocated_storage": allocated_storage_gb,
            "storage_type": storage_type,
            "engine_version": "13.7",
            "multi_az": multi_az,
            "publicly_accessible": publicly_accessible,
            "status": "available",
            "endpoint": f"{db_instance_identifier}.{self._config.region}.rds.amazonaws.com",
            "port": 3306 if engine in ["mysql", "mariadb", "aurora", "aurora-mysql"] else 5432
        }

    def setup_container_service(self, service_name: str, cpu: str = "256", memory: str = "512",
                                desired_count: int = 1, launch_type: str = "FARGATE",
                                network_configuration: Optional[Dict[str, Any]] = None,
                                task_role_arn: str = "", execution_role_arn: str = "",
                                environment_variables: Optional[Dict[str, str]] = None,
                                secrets: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        cluster_arn = f"arn:aws:ecs:{self._config.region}:123456789012:cluster/{service_name}-cluster"
        task_def_arn = f"arn:aws:ecs:{self._config.region}:123456789012:task-definition/{service_name}-task:1"
        service_arn = f"arn:aws:ecs:{self._config.region}:123456789012:service/{service_name}-service"
        task = ContainerTask(
            task_definition_arn=task_def_arn,
            container_definitions=[{
                "name": service_name,
                "image": f"{service_name}:latest",
                "cpu": int(cpu),
                "memory": int(memory),
                "essential": True,
                "environment": [{"name": k, "value": v} for k, v in (environment_variables or {}).items()],
                "secrets": [{"name": k, "valueFrom": v} for k, v in (secrets or {}).items()]
            }],
            family=service_name,
            cpu=cpu,
            memory=memory,
            execution_role_arn=execution_role_arn,
            task_role_arn=task_role_arn
        )
        self._container_tasks[service_name] = task
        logger.info(f"Setup container service: {service_name}")
        self._log_operation("ecs.create_service", {"service_name": service_name, "desired_count": desired_count})
        return {
            "service": service_name,
            "cluster_arn": cluster_arn,
            "service_arn": service_arn,
            "task_definition_arn": task_def_arn,
            "status": "ACTIVE",
            "desired_count": desired_count,
            "running_count": desired_count,
            "launch_type": launch_type,
            "network_configuration": network_configuration or {}
        }

    def create_load_balancer(self, name: str, scheme: str = "internet-facing", lb_type: str = "application",
                             vpc_id: str = "", subnet_ids: Optional[List[str]] = None,
                             security_group_ids: Optional[List[str]] = None,
                             listeners: Optional[List[Dict[str, Any]]] = None) -> LoadBalancer:
        if lb_type == LoadBalancerType.APPLICATION.value:
            lb_type = LoadBalancerType.APPLICATION.value
        dns_name = f"{name}-{uuid.uuid4().hex[:8]}.elb.amazonaws.com"
        lb = LoadBalancer(
            id=self._generate_id("lb"),
            name=name,
            dns_name=dns_name,
            scheme=scheme,
            type=lb_type,
            vpc_id=vpc_id,
            security_group_ids=security_group_ids or [],
            subnets=subnet_ids or [],
            listeners=listeners or []
        )
        self._load_balancers[lb.id] = lb
        logger.info(f"Created load balancer {lb.id} ({name})")
        self._log_operation("elb.create", {"lb_id": lb.id, "name": name, "type": lb_type})
        return lb

    def setup_auto_scaling(self, name: str, launch_configuration: Dict[str, Any], min_size: int, max_size: int,
                           desired_capacity: int, vpc_zone_identifiers: Optional[List[str]] = None,
                           target_group_arns: Optional[List[str]] = None,
                           health_check_type: str = "EC2") -> AutoScalingGroup:
        if min_size > max_size:
            raise ValidationError(f"min_size ({min_size}) cannot be greater than max_size ({max_size})")
        if desired_capacity > max_size or desired_capacity < min_size:
            raise ValidationError(f"desired_capacity ({desired_capacity}) must be between min_size and max_size")
        asg = AutoScalingGroup(
            name=name,
            launch_configuration=launch_configuration,
            min_size=min_size,
            max_size=max_size,
            desired_capacity=desired_capacity,
            vpc_zone_identifiers=vpc_zone_identifiers or [],
            target_group_arns=target_group_arns or [],
            health_check_type=health_check_type
        )
        self._auto_scaling_groups[name] = asg
        logger.info(f"Created auto scaling group: {name}")
        self._log_operation("autoscaling.create_group", {"asg_name": name, "min": min_size, "max": max_size})
        return asg

    def scale_auto_scaling_group(self, name: str, new_capacity: int) -> Dict[str, Any]:
        asg = self._auto_scaling_groups.get(name)
        if not asg:
            raise ResourceNotFoundError(f"AutoScaling group not found: {name}")
        if new_capacity < asg.min_size or new_capacity > asg.max_size:
            raise ValidationError(f"Capacity {new_capacity} outside bounds [{asg.min_size}, {asg.max_size}]")
        old_capacity = asg.desired_capacity
        asg.desired_capacity = new_capacity
        logger.info(f"Scaled ASG {name} from {old_capacity} to {new_capacity}")
        self._log_operation("autoscaling.scale", {"asg_name": name, "old_capacity": old_capacity, "new_capacity": new_capacity})
        return {"asg_name": name, "old_desired_capacity": old_capacity, "new_desired_capacity": new_capacity}

    def create_cloudwatch_alarm(self, alarm_name: str, metric_name: str, namespace: str,
                                 statistic: str, period: int, evaluation_periods: int,
                                 threshold: float, comparison_operator: str,
                                 alarm_actions: Optional[List[str]] = None, description: str = "") -> CloudWatchAlarm:
        valid_stats = ["Sum", "Average", "Maximum", "Minimum", "SampleCount", "p99", "p95", "p50"]
        if statistic not in valid_stats:
            raise ValidationError(f"Invalid statistic: {statistic}. Valid: {valid_stats}")
        valid_ops = ["GreaterThanThreshold", "GreaterThanOrEqualToThreshold", "LessThanThreshold", "LessThanOrEqualToThreshold"]
        if comparison_operator not in valid_ops:
            raise ValidationError(f"Invalid comparison operator: {comparison_operator}. Valid: {valid_ops}")
        alarm = CloudWatchAlarm(
            alarm_name=alarm_name,
            metric_name=metric_name,
            namespace=namespace,
            statistic=statistic,
            period=period,
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            comparison_operator=comparison_operator,
            alarm_actions=alarm_actions or [],
            description=description
        )
        self._cloudwatch_alarms[alarm_name] = alarm
        logger.info(f"Created CloudWatch alarm: {alarm_name}")
        self._log_operation("cloudwatch.create_alarm", {"alarm_name": alarm_name, "metric": metric_name})
        return alarm

    def create_iam_role(self, role_name: str, assume_role_policy: Dict[str, Any],
                        policies: Optional[List[str]] = None, max_session_duration: int = 3600,
                        description: str = "") -> IAMRole:
        role = IAMRole(
            role_name=role_name,
            assume_role_policy_document=assume_role_policy,
            policies=policies or [],
            max_session_duration=max_session_duration,
            description=description,
            arn=f"arn:aws:iam::123456789012:role/{role_name}"
        )
        self._iam_roles[role_name] = role
        logger.info(f"Created IAM role: {role_name}")
        self._log_operation("iam.create_role", {"role_name": role_name})
        return role

    def deploy_cloudformation_stack(self, stack_name: str, template_body: str,
                                    parameters: Optional[Dict[str, str]] = None,
                                    capabilities: Optional[List[str]] = None,
                                    tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        stack_id = self._generate_id("stack")
        logger.info(f"Deploying CloudFormation stack: {stack_name}")
        self._log_operation("cloudformation.deploy", {"stack_name": stack_name})
        return {
            "stack_id": stack_id,
            "stack_name": stack_name,
            "status": "CREATE_COMPLETE",
            "creation_time": datetime.utcnow().isoformat(),
            "parameters": parameters or {},
            "capabilities": capabilities or ["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
            "outputs": {
                "VpcId": self._generate_id("vpc"),
                "LoadBalancerDNS": f"{stack_name}-alb.elb.amazonaws.com"
            }
        }

    def setup_route53(self, zone_name: str, private: bool = False, vpc_id: Optional[str] = None) -> Dict[str, Any]:
        hosted_zone_id = self._generate_id("Z")
        logger.info(f"Created Route53 hosted zone: {zone_name}")
        self._log_operation("route53.create_zone", {"zone_name": zone_name, "private": private})
        return {
            "hosted_zone_id": hosted_zone_id,
            "name": zone_name,
            "private_zone": private,
            "name_servers": [f"ns-1.awsdns-1.com", f"ns-2.awsdns-2.net"],
            "vpc_id": vpc_id
        }

    def create_cloudfront_distribution(self, origin_domain: str, origin_path: str = "",
                                      enabled: bool = True, comment: str = "",
                                      price_class: str = "PriceClass_100") -> Dict[str, Any]:
        distribution_id = self._generate_id("E")
        domain_name = f"{distribution_id}.cloudfront.net"
        logger.info(f"Created CloudFront distribution: {distribution_id}")
        self._log_operation("cloudfront.create_distribution", {"distribution_id": distribution_id, "origin": origin_domain})
        return {
            "distribution_id": distribution_id,
            "domain_name": domain_name,
            "status": "Deployed",
            "enabled": enabled,
            "price_class": price_class,
            "origin": {"domain_name": origin_domain, "origin_path": origin_path},
            "last_modified_time": datetime.utcnow().isoformat()
        }

    def publish_sns_topic(self, topic_name: str, display_name: str = "",
                          fifo: bool = False, tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        topic_arn = f"arn:aws:sns:{self._config.region}:123456789012:{topic_name}"
        logger.info(f"Created SNS topic: {topic_name}")
        self._log_operation("sns.create_topic", {"topic_name": topic_name})
        return {
            "topic_arn": topic_arn,
            "name": topic_name,
            "display_name": display_name or topic_name,
            "fifo_topic": fifo,
            "effective_delivery_policy": {"http": {"defaultRequestPolicy": {"headerContentType": "text/json"}}},
            "tags": tags or {}
        }

    def send_sqs_message(self, queue_url: str, message_body: str, delay_seconds: int = 0,
                         message_attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        message_id = self._generate_id("msg")
        logger.info(f"Sent SQS message to {queue_url}")
        self._log_operation("sqs.send_message", {"queue_url": queue_url})
        return {
            "message_id": message_id,
            "md5_of_body": hashlib.md5(message_body.encode()).hexdigest(),
            "sequence_number": str(uuid.uuid4().int),
            "queue_url": queue_url
        }

    def create_dynamodb_table(self, table_name: str, partition_key: str, partition_key_type: str = "S",
                              sort_key: Optional[Tuple[str, str]] = None, billing_mode: str = "PAY_PER_REQUEST",
                              read_capacity_units: int = 5, write_capacity_units: int = 5) -> Dict[str, Any]:
        if partition_key_type not in ["S", "N", "B"]:
            raise ValidationError(f"Invalid key type: {partition_key_type}. Valid: S, N, B")
        table_id = self._generate_id("table")
        logger.info(f"Created DynamoDB table: {table_name}")
        self._log_operation("dynamodb.create_table", {"table_name": table_name})
        return {
            "table_name": table_name,
            "table_id": table_id,
            "status": "ACTIVE",
            "partition_key": {"attribute_name": partition_key, "key_type": "HASH", "attribute_type": partition_key_type},
            "sort_key": {"attribute_name": sort_key[0], "key_type": "RANGE", "attribute_type": sort_key[1]} if sort_key else None,
            "billing_mode": billing_mode,
            "read_capacity_units": read_capacity_units if billing_mode == "PROVISIONED" else 0,
            "write_capacity_units": write_capacity_units if billing_mode == "PROVISIONED" else 0,
            "creation_date_time": datetime.utcnow().isoformat(),
            "table_arn": f"arn:aws:dynamodb:{self._config.region}:123456789012:table/{table_name}"
        }

    def publish_cloudformation_template(self, stack_name: str, template_url: str,
                                        parameters: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        stack_id = self._generate_id("stack")
        logger.info(f"Published CloudFormation template for stack: {stack_name}")
        self._log_operation("cloudformation.publish", {"stack_name": stack_name, "template_url": template_url})
        return {
            "stack_id": stack_id,
            "stack_name": stack_name,
            "template_url": template_url,
            "status": "REVIEW_IN_PROGRESS",
            "parameters": parameters or {}
        }

    def add_permissions_boundary(self, role_arn: str, permissions_boundary_arn: str) -> Dict[str, Any]:
        logger.info(f"Added permissions boundary to role: {role_arn}")
        self._log_operation("iam.add_permissions_boundary", {"role_arn": role_arn, "boundary": permissions_boundary_arn})
        return {
            "role_arn": role_arn,
            "permissions_boundary_arn": permissions_boundary_arn,
            "updated_at": datetime.utcnow().isoformat()
        }

    def configure_vpc_peering(self, requester_vpc_id: str, accepter_vpc_id: str,
                              tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        peering_id = self._generate_id("pcx")
        logger.info(f"Created VPC peering connection: {peering_id}")
        self._log_operation("vpc.create_peering", {"peering_id": peering_id})
        return {
            "vpc_peering_connection_id": peering_id,
            "requester_vpc_id": requester_vpc_id,
            "accepter_vpc_id": accepter_vpc_id,
            "status": {"code": "pending-acceptance"},
            "tags": tags or {}
        }

    def create_eks_cluster(self, cluster_name: str, kubernetes_version: str = "1.24",
                           endpoint_public_access: bool = True, tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        cluster_arn = f"arn:aws:eks:{self._config.region}:123456789012:cluster/{cluster_name}"
        logger.info(f"Created EKS cluster: {cluster_name}")
        self._log_operation("eks.create_cluster", {"cluster_name": cluster_name})
        return {
            "cluster_name": cluster_name,
            "cluster_arn": cluster_arn,
            "status": "ACTIVE",
            "kubernetes_version": kubernetes_version,
            "endpoint": f"https://{cluster_name}.{self._config.region}.eks.amazonaws.com",
            "endpoint_public_access": endpoint_public_access,
            "tags": tags or {},
            "created_at": datetime.utcnow().isoformat()
        }

    def create_kms_key(self, description: str = "", key_usage: str = "ENCRYPT_DECRYPT",
                       origin: str = "AWS_KMS", tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        key_id = self._generate_id("key")
        key_arn = f"arn:aws:kms:{self._config.region}:123456789012:key/{key_id}"
        logger.info(f"Created KMS key: {key_id}")
        self._log_operation("kms.create_key", {"key_id": key_id})
        return {
            "key_id": key_id,
            "key_arn": key_arn,
            "description": description,
            "key_usage": key_usage,
            "origin": origin,
            "enabled": True,
            "key_state": "Enabled",
            "tags": tags or {}
        }

    def estimate_cost(self, services: List[str], hourly: bool = True) -> Dict[str, Any]:
        pricing = {
            "t3.micro": 0.0104, "t3.small": 0.0208, "t3.medium": 0.0416,
            "m5.large": 0.096, "m5.xlarge": 0.192, "c5.large": 0.085,
            "r5.large": 0.126, "p3.2xlarge": 3.06, "g4dn.xlarge": 0.526
        }
        lambda_pricing = 0.0000166667
        s3_storage = 0.023
        total = 0.0
        details = {}
        for svc in services:
            if svc in pricing:
                cost = pricing[svc]
                details[svc] = {"hourly": cost, "daily": round(cost * 24, 4), "monthly": round(cost * 730, 2)}
                total += cost
            elif svc == "lambda":
                details["lambda"] = {"hourly": lambda_pricing, "daily": round(lambda_pricing * 24, 6), "monthly": round(lambda_pricing * 730, 4)}
                total += lambda_pricing
            elif svc == "s3":
                details["s3"] = {"hourly": f"{s3_storage}/GB-month", "daily": f"{round(s3_storage * 24, 4)}/GB-month", "monthly": s3_storage}
                total += s3_storage
        period = "hour" if hourly else "month"
        logger.info(f"Estimated AWS cost for {len(services)} services")
        self._log_operation("cost_estimate", {"services": services, "hourly": hourly})
        return {
            "services": details,
            "total_hourly": round(total, 4) if hourly else round(total * 730, 2),
            "total_monthly": round(total * 730, 2),
            "currency": "USD",
            "region": self._config.region
        }

    def generate_iam_policy(self, actions: List[str], resources: List[str],
                            effect: str = "Allow", sid: str = "") -> Dict[str, Any]:
        valid_actions = [a.strip() for a in actions if a.strip()]
        valid_resources = [r.strip() for r in resources if r.strip()]
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": sid or f"Statement{uuid.uuid4().hex[:6]}",
                    "Effect": effect,
                    "Action": valid_actions,
                    "Resource": valid_resources
                }
            ]
        }
        logger.info(f"Generated IAM policy with {len(valid_actions)} actions")
        self._log_operation("iam.generate_policy", {"actions_count": len(valid_actions)})
        return policy

    def deploy_infrastructure_as_code(self, infrastructure_code: str, format_type: str = "terraform",
                                      variables: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if format_type not in ["terraform", "cloudformation", "cdk", "pulumi"]:
            raise ValidationError(f"Invalid IaC format: {format_type}. Valid: terraform, cloudformation, cdk, pulumi")
        deploy_id = self._generate_id("deploy")
        logger.info(f"Initiating {format_type} deployment")
        self._log_operation("iac.deploy", {"format": format_type})
        return {
            "deployment_id": deploy_id,
            "format": format_type,
            "status": "APPLY_COMPLETE",
            "resources_created": 12,
            "resources_updated": 2,
            "resources_deleted": 0,
            "duration_seconds": 145,
            "outputs": {
                "vpc_id": self._generate_id("vpc"),
                "public_subnet_ids": [self._generate_id("subnet"), self._generate_id("subnet")],
                "private_subnet_ids": [self._generate_id("subnet"), self._generate_id("subnet")],
                "ec2_instance_id": self._generate_id("i"),
                "rds_endpoint": f"db.{deploy_id}.{self._config.region}.rds.amazonaws.com"
            }
        }

    def create_sns_subscription(self, topic_arn: str, protocol: str, endpoint: str,
                                 attributes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        valid_protocols = ["http", "https", "email", "email-json", "sms", "sqs", "application", "lambda"]
        if protocol not in valid_protocols:
            raise ValidationError(f"Invalid protocol: {protocol}. Valid: {valid_protocols}")
        subscription_arn = f"arn:aws:sns:{self._config.region}:123456789012:{uuid.uuid4().hex[:16]}:{endpoint.split('@')[0] if '@' in endpoint else endpoint}"
        logger.info(f"Created SNS subscription: {protocol}:{endpoint}")
        self._log_operation("sns.subscribe", {"topic_arn": topic_arn, "protocol": protocol, "endpoint": endpoint})
        return {
            "subscription_arn": subscription_arn,
            "topic_arn": topic_arn,
            "protocol": protocol,
            "endpoint": endpoint,
            "attributes": attributes or {}
        }

    def create_cloudwatch_metric_stream(self, name: str, output_format: str = "JSON",
                                        include_filters: Optional[List[str]] = None,
                                        tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        stream_arn = f"arn:aws:cloudwatch::{self._config.region}:123456789012:metric-stream/{name}"
        logger.info(f"Created CloudWatch metric stream: {name}")
        self._log_operation("cloudwatch.create_metric_stream", {"name": name})
        return {
            "arn": stream_arn,
            "name": name,
            "output_format": output_format,
            "include_filters": include_filters or [],
            "state": "RUNNING",
            "creation_date": datetime.utcnow().isoformat(),
            "tags": tags or {}
        }

    def authorize_security_group_ingress(self, security_group_id: str, ip_protocol: str,
                                         from_port: int, to_port: int,
                                         cidr_ip: str, description: str = "") -> Dict[str, Any]:
        sg = self._security_groups.get(security_group_id)
        if not sg:
            raise ResourceNotFoundError(f"Security group not found: {security_group_id}")
        rule = SecurityGroupRule(
            protocol=ip_protocol,
            from_port=from_port,
            to_port=to_port,
            source=cidr_ip,
            description=description,
            rule_type="ingress"
        )
        sg.ingress_rules.append(rule)
        logger.info(f"Added ingress rule to security group {security_group_id}")
        self._log_operation("security_group.authorize_ingress", {"sg_id": security_group_id, "cidr": cidr_ip})
        return {"security_group_id": security_group_id, "rule_added": True}

    def attach_internet_gateway(self, vpc_id: str, gateway_id: str) -> Dict[str, Any]:
        vpc = self._vpc_registry.get(vpc_id)
        if not vpc:
            raise ResourceNotFoundError(f"VPC not found: {vpc_id}")
        vpc.internet_gateway_id = gateway_id
        logger.info(f"Attached IGW {gateway_id} to VPC {vpc_id}")
        self._log_operation("vpc.attach_igw", {"vpc_id": vpc_id, "gateway_id": gateway_id})
        return {"vpc_id": vpc_id, "internet_gateway_id": gateway_id}

    def create_db_subnet_group(self, name: str, subnet_ids: List[str], description: str = "") -> Dict[str, Any]:
        if len(subnet_ids) < 2:
            raise ValidationError("At least 2 subnets are required for a DB subnet group")
        group_arn = f"arn:aws:rds:{self._config.region}:123456789012:subgrp:{name}"
        logger.info(f"Created DB subnet group: {name}")
        self._log_operation("rds.create_subnet_group", {"name": name, "subnets": subnet_ids})
        return {
            "db_subnet_group_name": name,
            "db_subnet_group_arn": group_arn,
            "description": description,
            "subnet_ids": subnet_ids,
            "status": "Complete"
        }

    def get_infrastructure_summary(self) -> Dict[str, Any]:
        summary = {
            "region": self._config.region,
            "environment": self._config.environment,
            "vpcs": len(self._vpc_registry),
            "ec2_instances": len(self._instances),
            "s3_buckets": len(self._s3_buckets),
            "lambda_functions": len(self._lambda_functions),
            "security_groups": len(self._security_groups),
            "load_balancers": len(self._load_balancers),
            "container_services": len(self._container_tasks),
            "auto_scaling_groups": len(self._auto_scaling_groups),
            "cloudwatch_alarms": len(self._cloudwatch_alarms),
            "iam_roles": len(self._iam_roles),
            "uptime_seconds": (datetime.utcnow() - self._start_time).total_seconds()
        }
        logger.info(f"Infrastructure summary: {summary}")
        return summary

    def get_metrics_report(self) -> Dict[str, Any]:
        return {
            "total_metrics_recorded": len(self._metrics.get_metrics()),
            "operations": len(self._operation_history),
            "success_rate": self._calculate_success_rate(),
            "average_latency_ms": self._calculate_avg_latency(),
            "entities": {
                "vpc": len(self._vpc_registry),
                "subnet": sum(len(v.subnets) for v in self._vpc_registry.values()),
                "security_group": len(self._security_groups),
                "ec2_instance": len(self._instances),
                "s3_bucket": len(self._s3_buckets),
                "lambda": len(self._lambda_functions),
                "load_balancer": len(self._load_balancers),
                "container_task": len(self._container_tasks),
                "auto_scaling_group": len(self._auto_scaling_groups),
                "cloudwatch_alarm": len(self._cloudwatch_alarms),
                "iam_role": len(self._iam_roles)
            }
        }

    def _calculate_success_rate(self) -> float:
        if not self._operation_history:
            return 0.0
        success = sum(1 for op in self._operation_history if op.get("status") == "success")
        return round(success / len(self._operation_history), 4)

    def _calculate_avg_latency(self) -> Optional[float]:
        latencies = [m.value for m in self._metrics.get_metrics("provision_latency_ms")]
        if not latencies:
            return None
        return round(sum(latencies) / len(latencies), 2)

    def export_state(self) -> str:
        state = {
            "region": self._config.region,
            "environment": self._config.environment,
            "vpc_registry": {k: {
                "id": v.id,
                "cidr_block": v.cidr_block,
                "name": v.name,
                "subnets": [{"id": s.id, "cidr_block": s.cidr_block, "availability_zone": s.availability_zone} for s in v.subnets],
                "security_groups": [{"id": g.id, "name": g.name} for g in v.security_groups]
            } for k, v in self._vpc_registry.items()},
            "security_groups": {k: {
                "id": v.id,
                "name": v.name,
                "ingress_rules": [{"protocol": r.protocol, "from_port": r.from_port, "to_port": r.to_port, "source": r.source} for r in v.ingress_rules],
                "egress_rules": [{"protocol": r.protocol, "from_port": r.from_port, "to_port": r.to_port, "source": r.source} for r in v.egress_rules]
            } for k, v in self._security_groups.items()},
            "ec2_instances": {k: {
                "id": v.id, "name": v.name, "instance_type": v.instance_type,
                "state": v.state, "public_ip": v.public_ip, "private_ip": v.private_ip
            } for k, v in self._instances.items()},
            "s3_buckets": list(self._s3_buckets.keys()),
            "lambda_functions": list(self._lambda_functions.keys()),
            "load_balancers": [v.name for v in self._load_balancers.values()],
            "container_services": list(self._container_tasks.keys()),
            "auto_scaling_groups": list(self._auto_scaling_groups.keys()),
            "cloudwatch_alarms": list(self._cloudwatch_alarms.keys()),
            "iam_roles": list(self._iam_roles.keys())
        }
        return json.dumps(state, indent=2, default=str)

    def import_state(self, state_json: str) -> None:
        state = json.loads(state_json)
        logger.info(f"Importing infrastructure state with {len(state)} entities")
        self._log_operation("state.import", {"state_keys": list(state.keys())})

    def validate_configuration(self) -> List[Dict[str, Any]]:
        issues = []
        for sg_id, sg in self._security_groups.items():
            if any(r.source == "0.0.0.0/0" and r.port == 22 for r in sg.ingress_rules if hasattr(r, 'port') or r.from_port in [22] or '22' in str([r.from_port, r.to_port])):
                issues.append({
                    "type": "security",
                    "severity": "high",
                    "resource_id": sg_id,
                    "message": "SSH open to the world"
                })
        for inst_id, inst in self._instances.items():
            if inst.state == InstanceState.RUNNING.value and not inst.security_group_ids:
                issues.append({
                    "type": "security",
                    "severity": "medium",
                    "resource_id": inst_id,
                    "message": "EC2 instance has no security groups"
                })
        logger.info(f"Configuration validation found {len(issues)} issues")
        return issues

    def optimize_costs(self) -> Dict[str, Any]:
        savings = 0.0
        recommendations = []
        for inst_id, inst in self._instances.items():
            if inst.state == InstanceState.RUNNING.value and inst.instance_type in ["m5.xlarge", "c5.xlarge"]:
                savings += 0.10
                recommendations.append({
                    "resource": inst_id,
                    "action": "rightsizing",
                    "current_type": inst.instance_type,
                    "suggested_type": "m5.large",
                    "estimated_savings_per_hour": 0.10
                })
        for alb_name, alb in self._load_balancers.items():
            if len(alb.listeners) == 0:
                savings += 0.0225
                recommendations.append({
                    "resource": alb_name,
                    "action": "remove_unused_load_balancer",
                    "estimated_savings_per_hour": 0.0225
                })
        logger.info(f"Cost optimization: ${round(savings, 4)}/hour potential savings")
        self._log_operation("optimize.costs", {"savings_per_hour": round(savings, 4)})
        return {
            "potential_savings_hourly": round(savings, 4),
            "potential_savings_monthly": round(savings * 730, 2),
            "recommendations": recommendations
        }

    def setup_tailscale_vpn(self, vpc_id: str, subnet_id: str) -> Dict[str, Any]:
        tailscale_ami = "ami-0c55b159cbfafe1f0"
        instance = self.provision_ec2(
            name="tailscale-vpn",
            instance_type="t3.micro",
            ami_id=tailscale_ami,
            tags={"Purpose": "VPN", "Managed": "true"}
        )
        logger.info(f"Provisioned Tailscale VPN node in VPC {vpc_id}")
        self._log_operation("vpn.setup", {"vpc_id": vpc_id, "instance_id": instance.id, "type": "tailscale"})
        return {
            "vpc_id": vpc_id,
            "subnet_id": subnet_id,
            "instance_id": instance.id,
            "vpn_type": "tailscale",
            "status": "READY"
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AWSSpecialistAgent",
            "region": self._config.region,
            "environment": self._config.environment,
            "instances_managed": len(self._instances),
            "vpcs_managed": len(self._vpc_registry),
            "s3_buckets_managed": len(self._s3_buckets),
            "lambda_functions_managed": len(self._lambda_functions),
            "security_groups_managed": len(self._security_groups),
            "load_balancers_managed": len(self._load_balancers),
            "container_services_managed": len(self._container_tasks),
            "auto_scaling_groups_managed": len(self._auto_scaling_groups),
            "cloudwatch_alarms_managed": len(self._cloudwatch_alarms),
            "iam_roles_managed": len(self._iam_roles),
            "uptime_seconds": (datetime.utcnow() - self._start_time).total_seconds(),
            "operations_performed": len(self._operation_history),
            "success_rate": self._calculate_success_rate()
        }


def demonstrate_provisioning(agent: AWSSpecialistAgent) -> None:
    print("\n=== EC2 Provisioning ===")
    instance = agent.provision_ec2(
        name="web-server",
        instance_type="t3.micro",
        ami_id="ami-0abcdef1234567890",
        key_name="my-key",
        tags={"Environment": "production", "Team": "platform"}
    )
    print(f"Created: {instance.id} | Name: {instance.name} | Type: {instance.instance_type} | State: {instance.state}")


def demonstrate_vpc_networking(agent: AWSSpecialistAgent) -> None:
    print("\n=== VPC Networking ===")
    vpc = agent.create_vpc(cidr_block="10.0.0.0/16", name="main-vpc", tags={"Env": "prod"})
    print(f"Created VPC: {vpc.id} | CIDR: {vpc.cidr_block}")
    for az in ["us-east-1a", "us-east-1b"]:
        subnet = agent.add_subnet(vpc_id=vpc.id, cidr_block=f"10.0.{1 if 'a' in az else 2}.0/24",
                                  availability_zone=az, public=(az == "us-east-1a"))
        print(f"  Subnet: {subnet.id} | AZ: {subnet.availability_zone} | Public: {subnet.public}")
    sg = agent.create_security_group(
        vpc_id=vpc.id,
        name="web-sg",
        description="Security group for web servers",
        ingress_rules=[
            SecurityGroupRule(protocol="tcp", from_port=443, to_port=443, source="0.0.0.0/0", description="HTTPS"),
            SecurityGroupRule(protocol="tcp", from_port=80, to_port=80, source="0.0.0.0/0", description="HTTP")
        ]
    )
    print(f"  Security Group: {sg.id} | Rules: {len(sg.ingress_rules)} ingress")


def demonstrate_storage_compute(agent: AWSSpecialistAgent) -> None:
    print("\n=== S3 & Lambda ===")
    bucket = agent.configure_s3_bucket(
        bucket_name="my-app-assets-prod",
        versioning=True,
        encryption="AES256",
        lifecycle_rules=[{"id": "transition-to-ia", "status": "Enabled", "transition": {"storage_class": "STANDARD_IA", "days": 30}}],
        tags={"Environment": "production"}
    )
    print(f"S3 Bucket: {bucket.name} | Versioning: {bucket.versioning} | Encryption: {bucket.encryption}")
    func = agent.deploy_lambda(
        function_name="api-processor",
        runtime="python3.11",
        handler="index.handler",
        memory_mb=512,
        timeout_seconds=30,
        role_arn="arn:aws:iam::123456789012:role/lambda-execution-role",
        description="Process API requests"
    )
    print(f"Lambda: {func.function_name} | Runtime: {func.runtime} | Memory: {func.memory_mb}MB | Timeout: {func.timeout_seconds}s")


def demonstrate_load_scaling(agent: AWSSpecialistAgent) -> None:
    print("\n=== Load Balancing & Auto Scaling ===")
    lb = agent.create_load_balancer(
        name="app-lb",
        scheme="internet-facing",
        lb_type="application",
        listeners=[
            {"port": 443, "protocol": "HTTPS", "certificate_arn": "arn:aws:acm:us-east-1:123456789012:certificate/abcd-efgh-ijkl"},
            {"port": 80, "protocol": "HTTP", "redirect_to": 443}
        ]
    )
    print(f"Load Balancer: {lb.name} | DNS: {lb.dns_name} | Type: {lb.type}")
    asg = agent.setup_auto_scaling(
        name="web-tier-asg",
        launch_configuration={"ami": "ami-0abcdef1234567890", "instance_type": "t3.micro", "security_groups": [sg.id for sg in agent._security_groups.values()]},
        min_size=2,
        max_size=10,
        desired_capacity=2
    )
    print(f"AutoScaling Group: {asg.name} | Min: {asg.min_size} | Desired: {asg.desired_capacity} | Max: {asg.max_size}")


def demonstrate_databases(agent: AWSSpecialistAgent) -> None:
    print("\n=== RDS & DynamoDB ===")
    rds = agent.create_rds_instance(
        db_instance_identifier="prod-web-db",
        engine="postgres",
        db_instance_class="db.t3.micro",
        master_username="dbadmin",
        master_password="SuperSecret123!",
        allocated_storage_gb=20,
        multi_az=True,
        publicly_accessible=False
    )
    print(f"RDS Instance: {rds['db_instance_identifier']} | Engine: {rds['engine']} | Endpoint: {rds['endpoint']}")
    table = agent.create_dynamodb_table(
        table_name="UserSessions",
        partition_key="session_id",
        partition_key_type="S",
        sort_key=("created_at", "N"),
        billing_mode="PAY_PER_REQUEST"
    )
    print(f"DynamoDB: {table['table_name']} | Status: {table['status']} | Billing: {table['billing_mode']}")


def demonstrate_eks_kms(agent: AWSSpecialistAgent) -> None:
    print("\n=== EKS & Security ===")
    eks = agent.create_eks_cluster(
        cluster_name="production-eks",
        kubernetes_version="1.24",
        endpoint_public_access=True
    )
    print(f"EKS: {eks['cluster_name']} | Version: {eks['kubernetes_version']}")
    kms = agent.create_kms_key(
        description="KMS key for application secrets",
        key_usage="ENCRYPT_DECRYPT"
    )
    print(f"KMS Key: {kms['key_id']} | ARN: {kms['key_arn']}")
    role = agent.create_iam_role(
        role_name="EksClusterRole",
        assume_role_policy={
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Principal": {"Service": "eks.amazonaws.com"}, "Action": "sts:AssumeRole"}]
        },
        description="EKS cluster role"
    )
    print(f"IAM Role: {role.role_name} | ARN: {role.arn}")


def demonstrate_monitoring_alarms(agent: AWSSpecialistAgent) -> None:
    print("\n=== Monitoring & Alarms ===")
    alarm = agent.create_cloudwatch_alarm(
        alarm_name="high-cpu-alarm",
        metric_name="CPUUtilization",
        namespace="AWS/EC2",
        statistic="Average",
        period=300,
        evaluation_periods=2,
        threshold=80.0,
        comparison_operator="GreaterThanThreshold",
        alarm_actions=["arn:aws:sns:us-east-1:123456789012:oncall-alerts"],
        description="Trigger when CPU > 80%"
    )
    print(f"CloudWatch Alarm: {alarm.alarm_name} | Metric: {alarm.metric_name} | Threshold: {alarm.threshold}")

    stream = agent.create_cloudwatch_metric_stream(
        name="metrics-to-firehose",
        output_format="JSON",
        include_filters=["AWS/EC2", "AWS/RDS", "AWS/Lambda"]
    )
    print(f"Metric Stream: {stream['name']} | Output: {stream['output_format']}")


def demonstrate_route53_cdn(agent: AWSSpecialistAgent) -> None:
    zone = agent.setup_route53(zone_name="example.com.")
    print(f"\nRoute53 Zone: {zone['name']} | Private: {zone['private_zone']}")
    cf = agent.create_cloudfront_distribution(
        origin_domain="my-app.s3.amazonaws.com",
        origin_path="/assets",
        comment="CDN for static assets"
    )
    print(f"CloudFront: {cf['domain_name']} | Origin: {cf['origin']['domain_name']}")


def demonstrate_sns_sqs(agent: AWSSpecialistAgent) -> None:
    topic = agent.publish_sns_topic(topic_name="order-events", display_name="Order Processing Events", fifo=False)
    print(f"\nSNS Topic: {topic['name']} | ARN: {topic['topic_arn']}")
    sub = agent.create_sns_subscription(
        topic_arn=topic["topic_arn"],
        protocol="email",
        endpoint="admin@example.com"
    )
    print(f"SNS Subscription: {sub['protocol']} -> {sub['endpoint']}")
    msg = agent.send_sqs_message(
        queue_url="https://sqs.us-east-1.amazonaws.com/123456789012/order-processing-queue",
        message_body='{"order_id": "12345", "status": "created"}'
    )
    print(f"SQS Message: {msg['message_id']} | Queue: {msg['queue_url']}")


def demonstrate_iam_policy(agent: AWSSpecialistAgent) -> None:
    print("\n=== IAM Policy Generation ===")
    policy = agent.generate_iam_policy(
        actions=["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
        resources=["arn:aws:s3:::my-bucket/*", "arn:aws:s3:::my-bucket"],
        effect="Allow",
        sid="S3AccessPolicy"
    )
    print(f"IAM Policy JSON snippet: {json.dumps(policy, indent=2)[:200]}...")


def demonstrate_cost_estimation(agent: AWSSpecialistAgent) -> None:
    print("\n=== Cost Estimation ===")
    costs = agent.estimate_cost(services=["t3.micro", "lambda", "s3"], hourly=True)
    print(f"Estimated hourly cost: ${costs['total_hourly']}")
    print(f"Estimated monthly cost: ${costs['total_monthly']}")


def demonstrate_validation_reporting(agent: AWSSpecialistAgent) -> None:
    print("\n=== Validation & Reporting ===")
    summary = agent.get_infrastructure_summary()
    print("Infrastructure Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    metrics = agent.get_metrics_report()
    print(f"\nMetrics Report: {metrics['operations']} operations, {metrics['success_rate']:.0%} success rate")
    issues = agent.validate_configuration()
    if issues:
        print(f"\nValidation Issues ({len(issues)}):")
        for issue in issues:
            print(f"  [{issue['severity'].upper()}] {issue['resource_id']}: {issue['message']}")
    state_export = agent.export_state()
    print(f"\nExported state: {len(state_export)} characters")


def main() -> None:
    print("AWS Specialist Agent Demo")
    print("=" * 50)
    config = Config(
        region="us-east-1",
        environment="development",
        tags={"Project": "Demo", "ManagedBy": "AWSSpecialistAgent"}
    )
    agent = AWSSpecialistAgent(config=config)
    print(agent.get_status())
    demonstrate_vpc_networking(agent)
    demonstrate_provisioning(agent)
    demonstrate_storage_compute(agent)
    demonstrate_load_scaling(agent)
    demonstrate_databases(agent)
    demonstrate_eks_kms(agent)
    demonstrate_monitoring_alarms(agent)
    demonstrate_route53_cdn(agent)
    demonstrate_sns_sqs(agent)
    demonstrate_iam_policy(agent)
    demonstrate_cost_estimation(agent)
    demonstrate_validation_reporting(agent)
    print("\n" + "=" * 50)
    print("Demo completed.")


if __name__ == "__main__":
    main()
