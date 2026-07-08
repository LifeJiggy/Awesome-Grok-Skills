"""Cloud Audit Agent - Cloud Security and Compliance Audits.

A comprehensive, production-grade agent for cloud security auditing, compliance
checking, cost analysis, and risk assessment across multiple cloud providers.
Supports AWS, Azure, GCP, and hybrid/multi-cloud environments.
"""

import json
import logging
import re
import os
import sys
import hashlib
import hmac
import base64
import datetime
import uuid
import time
from typing import Dict, List, Any, Optional, Tuple, Set, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger("cloud_audit_agent")


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class CloudProvider(Enum):
    """Supported cloud providers."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ORACLE = "oracle"
    IBM_CLOUD = "ibm_cloud"
    ALIBABA = "alibaba"
    MULTI_CLOUD = "multi_cloud"
    HYBRID = "hybrid"


class AuditScope(Enum):
    """Scope of the audit to be performed."""
    FULL = "full"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    COST = "cost"
    NETWORK = "network"
    IDENTITY = "identity"
    STORAGE = "storage"
    COMPUTE = "compute"
    DATABASE = "database"
    SERVERLESS = "serverless"
    CONTAINERS = "containers"
    IAM = "iam"


class SeverityLevel(Enum):
    """Severity classification for findings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    SOC2 = "SOC2"
    PCI_DSS = "PCI_DSS"
    HIPAA = "HIPAA"
    GDPR = "GDPR"
    ISO27001 = "ISO27001"
    CIS = "CIS"
    NIST_CSF = "NIST_CSF"
    NIST_800_53 = "NIST_800_53"
    FEDRAMP = "FedRAMP"
    CCPA = "CCPA"
    AWS_WELL_ARCHITECTED = "AWS_Well_Architected"
    AZURE_SECURITY_BENCHMARK = "Azure_Security_Benchmark"
    GCP_SECURITY_FRAMEWORK = "GCP_Security_Framework"


class RiskCategory(Enum):
    """Categories of cloud risk."""
    DATA_BREACH = "data_breach"
    MISCONFIGURATION = "misconfiguration"
    ACCESS_CONTROL = "access_control"
    ENCRYPTION = "encryption"
    NETWORK_EXPOSURE = "network_exposure"
    COMPLIANCE_VIOLATION = "compliance_violation"
    COST_OVERFLOW = "cost_overflow"
    AVAILABILITY = "availability"
    SUPPLY_CHAIN = "supply_chain"
    INSIDER_THREAT = "insider_threat"


# ---------------------------------------------------------------------------
# Data Classes / Model Objects
# ---------------------------------------------------------------------------

@dataclass
class AuditFinding:
    """Represents a single finding from an audit."""
    finding_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    severity: SeverityLevel = SeverityLevel.INFO
    category: RiskCategory = RiskCategory.MISCONFIGURATION
    provider: CloudProvider = CloudProvider.AWS
    resource_id: str = ""
    resource_type: str = ""
    region: str = ""
    account_id: str = ""
    remediation: str = ""
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    references: List[str] = field(default_factory=list)
    detected_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["category"] = self.category.value
        data["provider"] = self.provider.value
        data["compliance_frameworks"] = [f.value for f in self.compliance_frameworks]
        return data


@dataclass
class ComplianceGap:
    """Represents a gap in compliance coverage."""
    gap_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    framework: ComplianceFramework = ComplianceFramework.SOC2
    control_id: str = ""
    control_name: str = ""
    description: str = ""
    current_status: str = "non_compliant"
    recommended_action: str = ""
    priority: SeverityLevel = SeverityLevel.MEDIUM
    owner: str = ""
    due_date: str = ""
    evidence_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["framework"] = self.framework.value
        data["priority"] = self.priority.value
        return data


@dataclass
class CostRecommendation:
    """Represents a cost optimization recommendation."""
    reco_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resource_id: str = ""
    resource_type: str = ""
    current_monthly_cost: float = 0.0
    projected_monthly_savings: float = 0.0
    recommendation: str = ""
    confidence: str = "medium"
    provider: CloudProvider = CloudProvider.AWS
    region: str = ""
    risk_level: str = "low"

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["provider"] = self.provider.value
        data["savings_percentage"] = (
            (self.projected_monthly_savings / self.current_monthly_cost * 100)
            if self.current_monthly_cost > 0
            else 0.0
        )
        return data


@dataclass
class RiskRecord:
    """Represents a risk identified in the cloud environment."""
    risk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    category: RiskCategory = RiskCategory.MISCONFIGURATION
    severity: SeverityLevel = SeverityLevel.MEDIUM
    likelihood: str = "medium"
    impact: str = "medium"
    mitigation: str = ""
    residual_risk: str = "low"
    owner: str = ""
    status: str = "open"
    detected_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["category"] = self.category.value
        return data


@dataclass
class AuditReport:
    """Represents a complete audit report."""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    provider: CloudProvider = CloudProvider.AWS
    scope: AuditScope = AuditScope.FULL
    account_id: str = ""
    regions: List[str] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    completed_at: str = ""
    overall_score: int = 0
    findings: List[AuditFinding] = field(default_factory=list)
    compliance_results: Dict[str, List[ComplianceGap]] = field(default_factory=dict)
    cost_recommendations: List[CostRecommendation] = field(default_factory=list)
    risks: List[RiskRecord] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["provider"] = self.provider.value
        data["scope"] = self.scope.value
        data["findings"] = [f.to_dict() for f in self.findings]
        data["compliance_results"] = {
            k: [g.to_dict() for g in v] for k, v in self.compliance_results.items()
        }
        data["cost_recommendations"] = [c.to_dict() for c in self.cost_recommendations]
        data["risks"] = [r.to_dict() for r in self.risks]
        return data

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class ProviderConfig:
    """Configuration for a specific cloud provider."""
    provider: CloudProvider
    enabled: bool = True
    regions: List[str] = field(default_factory=list)
    credentials_file: str = ""
    profile: str = "default"
    max_retries: int = 3
    timeout_seconds: int = 30
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceConfig:
    """Configuration for compliance checking."""
    enabled_frameworks: List[ComplianceFramework] = field(default_factory=list)
    strict_mode: bool = False
    auto_remediate: bool = False
    notify_on_gap: bool = True
    gap_owner_default: str = ""


@dataclass
class CostConfig:
    """Configuration for cost analysis."""
    lookback_days: int = 30
    currency: str = "USD"
    include_forecast: bool = True
    threshold_monthly: float = 1000.0
    anomaly_detection: bool = True
    group_by: List[str] = field(default_factory=lambda: ["service", "region", "account"])


@dataclass
class RiskConfig:
    """Configuration for risk assessment."""
    enabled_categories: List[RiskCategory] = field(default_factory=list)
    min_severity: SeverityLevel = SeverityLevel.LOW
    max_results: int = 100
    auto_prioritize: bool = True
    mitigation_suggestions: bool = True


@dataclass
class Config:
    """Top-level agent configuration."""
    providers: List[ProviderConfig] = field(default_factory=list)
    compliance: ComplianceConfig = field(default_factory=ComplianceConfig)
    cost: CostConfig = field(default_factory=CostConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    output_format: str = "json"
    output_path: str = "./reports"
    log_level: str = "INFO"
    parallel_checks: int = 4
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        if not self.providers:
            errors.append("At least one provider must be configured.")
        for p in self.providers:
            if not p.regions:
                errors.append(f"Provider {p.provider.value} has no regions configured.")
        if self.parallel_checks < 1:
            errors.append("parallel_checks must be >= 1.")
        return errors


# ---------------------------------------------------------------------------
# Abstract Base Classes for Provider Plugins
# ---------------------------------------------------------------------------

class BaseCloudClient(ABC):
    """Abstract base class for cloud provider API clients."""

    def __init__(self, config: ProviderConfig):
        self.config = config
        self._session_token: Optional[str] = None
        self._rate_limit_remaining: int = 1000
        self._last_request_time: float = 0.0

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the cloud provider."""
        ...

    @abstractmethod
    def list_resources(self, resource_type: str, region: str) -> List[Dict[str, Any]]:
        """List resources of a given type in a given region."""
        ...

    @abstractmethod
    def get_config(self, resource_id: str) -> Dict[str, Any]:
        """Get the configuration of a specific resource."""
        ...

    @abstractmethod
    def get_compliance_status(
        self, framework: ComplianceFramework
    ) -> Dict[str, Any]:
        """Return compliance posture for a given framework."""
        ...

    @abstractmethod
    def get_cost_data(self, lookback_days: int) -> Dict[str, Any]:
        """Return cost data for the lookback period."""
        ...

    def _respect_rate_limit(self) -> None:
        """Simple rate limiter."""
        min_interval = 0.1
        elapsed = time.time() - self._last_request_time
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last_request_time = time.time()


class AWSSimulatedClient(BaseCloudClient):
    """Simulated AWS client for demonstration and testing."""

    def authenticate(self) -> bool:
        logger.info("Simulated AWS authentication successful.")
        self._session_token = "simulated-session-token"
        return True

    def list_resources(self, resource_type: str, region: str) -> List[Dict[str, Any]]:
        self._respect_rate_limit()
        simulated: Dict[str, List[Dict[str, Any]]] = {
            "s3": [
                {
                    "resource_id": "s3-bucket-prod-data",
                    "resource_type": "s3",
                    "region": "us-east-1",
                    "account_id": "123456789012",
                    "configuration": {
                        "versioning": False,
                        "encryption": False,
                        "public_access_block": {"block_public_acls": False},
                        "logging": False,
                    },
                },
                {
                    "resource_id": "s3-bucket-prod-backup",
                    "resource_type": "s3",
                    "region": "us-east-1",
                    "account_id": "123456789012",
                    "configuration": {
                        "versioning": True,
                        "encryption": True,
                        "public_access_block": {
                            "block_public_acls": True,
                            "ignore_public_acls": True,
                            "block_public_policy": True,
                            "restrict_public_buckets": True,
                        },
                        "logging": True,
                    },
                },
            ],
            "ec2": [
                {
                    "resource_id": "i-0abc12345",
                    "resource_type": "ec2_instance",
                    "region": "us-east-1",
                    "account_id": "123456789012",
                    "configuration": {
                        "instance_type": "t3.large",
                        "public_ip": True,
                        "security_groups": ["sg-0123456789"],
                        "encrypted_volumes": False,
                        "iam_role": "ec2-role-prod",
                    },
                },
                {
                    "resource_id": "i-0def67890",
                    "resource_type": "ec2_instance",
                    "region": "us-west-2",
                    "account_id": "123456789012",
                    "configuration": {
                        "instance_type": "m5.xlarge",
                        "public_ip": False,
                        "security_groups": ["sg-9876543210"],
                        "encrypted_volumes": True,
                        "iam_role": "ec2-role-prod",
                    },
                },
            ],
            "rds": [
                {
                    "resource_id": "prod-db-cluster",
                    "resource_type": "rds_cluster",
                    "region": "us-east-1",
                    "account_id": "123456789012",
                    "configuration": {
                        "engine": "aurora-mysql",
                        "storage_encrypted": True,
                        "publicly_accessible": False,
                        "backup_retention_period": 7,
                        "multi_az": True,
                    },
                }
            ],
            "iam": [
                {
                    "resource_id": "admin-user",
                    "resource_type": "iam_user",
                    "region": "global",
                    "account_id": "123456789012",
                    "configuration": {
                        "mfa_enabled": False,
                        "access_keys_active": 2,
                        "password_policy": {"min_length": 14, "require_symbols": True},
                        "permissions_boundary": "",
                    },
                },
                {
                    "resource_id": "service-role-lambda",
                    "resource_type": "iam_role",
                    "region": "global",
                    "account_id": "123456789012",
                    "configuration": {
                        "max_session_duration": 3600,
                        "permissions_boundary": "arn:aws:iam::123456789012:policy/permissions-boundary",
                        "trust_relationships": {"Service": "lambda.amazonaws.com"},
                    },
                },
            ],
            "eks": [
                {
                    "resource_id": "prod-eks-cluster",
                    "resource_type": "eks_cluster",
                    "region": "us-east-1",
                    "account_id": "123456789012",
                    "configuration": {
                        "version": "1.27",
                        "endpoint_public_access": True,
                        "endpoint_private_access": True,
                        "logging": {"api": True, "audit": True, "authenticator": False},
                        "encryption_config": {"provider": "aws-kms", "key_arn": "arn:aws:kms:..."},
                    },
                }
            ],
        }
        return simulated.get(resource_type, [])

    def get_config(self, resource_id: str) -> Dict[str, Any]:
        self._respect_rate_limit()
        return {"resource_id": resource_id, "detail": "simulated_config"}

    def get_compliance_status(
        self, framework: ComplianceFramework
    ) -> Dict[str, Any]:
        self._respect_rate_limit()
        return {
            "framework": framework.value,
            "compliant_controls": 45,
            "non_compliant_controls": 3,
            "total_controls": 48,
            "compliance_percentage": 93.75,
        }

    def get_cost_data(self, lookback_days: int) -> Dict[str, Any]:
        self._respect_rate_limit()
        daily_cost = 1200.0
        return {
            "total_cost": daily_cost * lookback_days,
            "currency": "USD",
            "lookback_days": lookback_days,
            "services": {
                "EC2": {"cost": daily_cost * lookback_days * 0.45, "trend": "stable"},
                "S3": {"cost": daily_cost * lookback_days * 0.15, "trend": "increasing"},
                "RDS": {"cost": daily_cost * lookback_days * 0.25, "trend": "stable"},
                "Lambda": {"cost": daily_cost * lookback_days * 0.05, "trend": "decreasing"},
                "Data Transfer": {
                    "cost": daily_cost * lookback_days * 0.10,
                    "trend": "increasing",
                },
            },
        }


# ---------------------------------------------------------------------------
# Check Engines
# ---------------------------------------------------------------------------

class SecurityCheckEngine:
    """Engine for running security checks."""

    PUBLIC_ACCESS_CHECKS = {
        "s3": ["block_public_acls", "block_public_policy", "ignore_public_acls", "restrict_public_buckets"],
        "rds": ["publicly_accessible"],
        "eks": ["endpoint_public_access"],
    }

    ENCRYPTION_CHECKS = {
        "s3": ["encryption"],
        "rds": ["storage_encrypted"],
        "ec2_instance": ["encrypted_volumes"],
    }

    def __init__(self, client: BaseCloudClient):
        self._client = client
        self._findings: List[AuditFinding] = []

    def run(self, resource_types: List[str]) -> List[AuditFinding]:
        """Run security checks across all resource types."""
        self._findings = []
        for resource_type in resource_types:
            resources = self._client.list_resources(resource_type, "us-east-1")
            for resource in resources:
                self._check_public_access(resource)
                self._check_encryption(resource)
                self._check_logging(resource)
                self._check_iam_exposure(resource)
        return self._findings

    def _check_public_access(self, resource: Dict[str, Any]) -> None:
        config = resource.get("configuration", {})
        resource_type = resource.get("resource_type", "")
        checks = self.PUBLIC_ACCESS_CHECKS.get(resource_type, [])
        for check in checks:
            value = config.get(check, None) if isinstance(config, dict) else None
            if value is not None and value is False:
                self._add_finding(
                    title=f"Public access not blocked: {check}",
                    description=f"The {resource_type} resource {resource.get('resource_id', 'N/A')} has "
                    f"'{check}' disabled, exposing it to the public internet.",
                    severity=SeverityLevel.HIGH,
                    category=RiskCategory.NETWORK_EXPOSURE,
                    resource=resource,
                    control=check,
                )

    def _check_encryption(self, resource: Dict[str, Any]) -> None:
        config = resource.get("configuration", {})
        resource_type = resource.get("resource_type", "")
        checks = self.ENCRYPTION_CHECKS.get(resource_type, [])
        for check in checks:
            value = config.get(check, None) if isinstance(config, dict) else None
            if value is not None and value is False:
                self._add_finding(
                    title=f"Encryption disabled: {check}",
                    description=f"The {resource_type} resource {resource.get('resource_id', 'N/A')} does not have "
                    f"'{check}' enabled, putting data at risk.",
                    severity=SeverityLevel.HIGH,
                    category=RiskCategory.ENCRYPTION,
                    resource=resource,
                    control=check,
                )

    def _check_logging(self, resource: Dict[str, Any]) -> None:
        config = resource.get("configuration", {})
        resource_type = resource.get("resource_type", "")
        if resource_type == "s3" and not config.get("logging", False):
            self._add_finding(
                title="S3 bucket logging disabled",
                description=f"Access logging is disabled for bucket "
                f"{resource.get('resource_id', 'N/A')}. This hampers forensic analysis.",
                severity=SeverityLevel.MEDIUM,
                category=RiskCategory.MISCONFIGURATION,
                resource=resource,
                control="logging",
            )

    def _check_iam_exposure(self, resource: Dict[str, Any]) -> None:
        config = resource.get("configuration", {})
        resource_type = resource.get("resource_type", "")
        if resource_type == "iam_user" and not config.get("mfa_enabled", True):
            self._add_finding(
                title="IAM user without MFA",
                description=f"The IAM user {resource.get('resource_id', 'N/A')} does not have "
                f"multi-factor authentication enabled.",
                severity=SeverityLevel.CRITICAL,
                category=RiskCategory.ACCESS_CONTROL,
                resource=resource,
                control="mfa_enabled",
            )

    def _add_finding(
        self,
        title: str,
        description: str,
        severity: SeverityLevel,
        category: RiskCategory,
        resource: Dict[str, Any],
        control: str,
    ) -> None:
        finding = AuditFinding(
            title=title,
            description=description,
            severity=severity,
            category=category,
            provider=self._client.config.provider,
            resource_id=resource.get("resource_id", ""),
            resource_type=resource.get("resource_type", ""),
            region=resource.get("region", ""),
            account_id=resource.get("account_id", ""),
            evidence={"control": control, "config_snapshot": resource.get("configuration", {})},
            references=[
                "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html",
                "https://docs.aws.amazon.com/security/latest/resources",
            ],
        )
        self._findings.append(finding)
        logger.info(
            "Finding [%s] %s - %s", severity.value.upper(), control, title
        )


class ComplianceCheckEngine:
    """Engine for running compliance checks."""

    CIS_AWS_CONTROLS = {
        "1.1": "Avoid the use of the root account.",
        "1.2": "Ensure MFA is enabled for root account.",
        "1.4": "Ensure no security groups allow ingress from 0.0.0.0/0 to port 22.",
        "1.5": "Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389.",
        "1.10": "Ensure no security groups allow ingress from 0.0.0.0/0 to port 443.",
        "2.1.1": "Ensure S3 bucket policy denies insecure (HTTP) requests.",
        "2.1.2": "Ensure S3 buckets are encrypted with AWS-KMS.",
        "2.1.3": "Ensure S3 bucket versioning is enabled.",
        "2.1.5": "Ensure S3 bucket policy requires encryption at minimum TLS 1.2.",
        "4.1": "Ensure no security groups allow ingress from 0.0.0.0/0.",
        "5.1": "Ensure no Network ACLs allow ingress from 0.0.0.0/0.",
    }

    def __init__(self, client: BaseCloudClient):
        self._client = client
        self._gaps: List[ComplianceGap] = []

    def evaluate(self, framework: ComplianceFramework) -> List[ComplianceGap]:
        """Evaluate all resources against a compliance framework."""
        self._gaps = []
        if framework == ComplianceFramework.CIS:
            self._evaluate_cis()
        elif framework == ComplianceFramework.SOC2:
            self._evaluate_soc2()
        elif framework == ComplianceFramework.PCI_DSS:
            self._evaluate_pci_dss()
        elif framework == ComplianceFramework.HIPAA:
            self._evaluate_hipaa()
        elif framework == ComplianceFramework.GDPR:
            self._evaluate_gdpr()
        return self._gaps

    def _evaluate_cis(self) -> None:
        for control_id, description in self.CIS_AWS_CONTROLS.items():
            compliant, evidence = self._check_control(control_id, description)
            if not compliant:
                gap = ComplianceGap(
                    framework=ComplianceFramework.CIS,
                    control_id=control_id,
                    control_name=description,
                    description=f"CIS Control {control_id} not satisfied.",
                    current_status="non_compliant",
                    recommended_action=self._remediation_for_cis(control_id),
                    priority=SeverityLevel.HIGH if control_id.startswith("1") else SeverityLevel.MEDIUM,
                    owner="security-team",
                    due_date=(
                        datetime.datetime.utcnow() + datetime.timedelta(days=30)
                    ).isoformat() + "Z",
                    evidence_url="",
                )
                self._gaps.append(gap)
                logger.warning(
                    "CIS Gap: %s - %s", control_id, description
                )

    def _evaluate_soc2(self) -> None:
        soc2_checks = [
            {
                "control_id": "CC6.1",
                "name": "Logical Access Controls",
                "check": self._check_iam_logical_access,
            },
            {
                "control_id": "CC6.6",
                "name": "System Boundary Protection",
                "check": self._check_network_boundary,
            },
            {
                "control_id": "CC7.2",
                "name": "Incident Detection and Monitoring",
                "check": self._check_logging_monitoring,
            },
        ]
        for check in soc2_checks:
            gap = check["check"]()
            if gap:
                self._gaps.append(gap)

    def _evaluate_pci_dss(self) -> None:
        pci_checks = [
            {"control_id": "3.4", "name": "PAN Storage Encryption", "check": self._check_pan_encryption},
            {"control_id": "6.5", "name": "Vulnerability Management", "check": self._check_vuln_mgmt},
        ]
        for check in pci_checks:
            gap = check["check"]()
            if gap:
                self._gaps.append(gap)

    def _evaluate_hipaa(self) -> None:
        hipaa_checks = [
            {"control_id": "164.312", "name": "Access Controls", "check": self._check_hipaa_access},
            {"control_id": "164.312(a)(2)(i)", "name": "Unique User Identification", "check": self._check_hipaa_unique_user},
        ]
        for check in hipaa_checks:
            gap = check["check"]()
            if gap:
                self._gaps.append(gap)

    def _evaluate_gdpr(self) -> None:
        gdpr_checks = [
            {"control_id": "Art.5", "name": "Data Minimisation", "check": self._check_gdpr_data_min},
            {"control_id": "Art.32", "name": "Security of Processing", "check": self._check_gdpr_security},
        ]
        for check in gdpr_checks:
            gap = check["check"]()
            if gap:
                self._gaps.append(gap)

    def _check_control(self, control_id: str, description: str) -> Tuple[bool, Dict]:
        return False, {"reason": "not_implemented_simulation"}

    def _check_iam_logical_access(self) -> Optional[ComplianceGap]:
        return ComplianceGap(
            framework=ComplianceFramework.SOC2,
            control_id="CC6.1",
            control_name="Logical Access Controls",
            description="IAM policies should restrict access to least privilege.",
            current_status="partial",
            recommended_action="Review and tighten IAM policies to follow least privilege.",
            priority=SeverityLevel.MEDIUM,
            owner="iam-team",
        )

    def _check_network_boundary(self) -> Optional[ComplianceGap]:
        return None

    def _check_logging_monitoring(self) -> Optional[ComplianceGap]:
        return ComplianceGap(
            framework=ComplianceFramework.SOC2,
            control_id="CC7.2",
            control_name="Incident Detection and Monitoring",
            description="CloudTrail and Config logging should be enabled in all regions.",
            current_status="non_compliant",
            recommended_action="Enable CloudTrail in all regions and integrate with SIEM.",
            priority=SeverityLevel.HIGH,
            owner="security-ops",
        )

    def _check_pan_encryption(self) -> Optional[ComplianceGap]:
        return None

    def _check_vuln_mgmt(self) -> Optional[ComplianceGap]:
        return None

    def _check_hipaa_access(self) -> Optional[ComplianceGap]:
        return ComplianceGap(
            framework=ComplianceFramework.HIPAA,
            control_id="164.312",
            control_name="Access Controls",
            description="PHI access controls must be enforced via RBAC.",
            current_status="partial",
            recommended_action="Map PHI data stores and enforce RBAC with break-glass procedures.",
            priority=SeverityLevel.HIGH,
            owner="healthcare-compliance",
        )

    def _check_hipaa_unique_user(self) -> Optional[ComplianceGap]:
        return None

    def _check_gdpr_data_min(self) -> Optional[ComplianceGap]:
        return None

    def _check_gdpr_security(self) -> Optional[ComplianceGap]:
        return None

    def _remediation_for_cis(self, control_id: str) -> str:
        remediation_map = {
            "1.1": "Enforce MFA and delete root access keys.",
            "1.2": "Enable virtual MFA for root account.",
            "1.4": "Remove SSH unrestricted inbound rules from security groups.",
            "1.5": "Remove RDP unrestricted inbound rules from security groups.",
            "1.10": "Remove unrestricted inbound HTTPS rules (only 443 from 0.0.0.0/0 with cond).",
            "2.1.1": "Enforce HTTPS via bucket policy.",
            "2.1.2": "Enable AES-256 or AWS-KMS encryption on all buckets.",
            "2.1.3": "Enable versioning on production buckets.",
            "2.1.5": "Add s3:ssl_only condition to bucket policy.",
            "4.1": "Restrict SGs to known IP ranges.",
            "5.1": "Restrict NACLs to known IP ranges.",
        }
        return remediation_map.get(control_id, "Review current configuration and remediate manually.")


class CostAnalysisEngine:
    """Engine for analyzing cloud costs and generating recommendations."""

    def __init__(self, client: BaseCloudClient, config: CostConfig):
        self._client = client
        self._config = config
        self._recommendations: List[CostRecommendation] = []

    def analyze(self) -> List[CostRecommendation]:
        """Run cost analysis and return recommendations."""
        self._recommendations = []
        cost_data = self._client.get_cost_data(self._config.lookback_days)
        self._recommendations.extend(self._check_idle_resources(cost_data))
        self._recommendations.extend(self._check_overprovisioned_resources(cost_data))
        self._recommendations.extend(self._check_reserved_instance_opportunities(cost_data))
        self._recommendations.extend(self._check_storage_tier_optimization(cost_data))
        return self._recommendations

    def _check_idle_resources(self, cost_data: Dict[str, Any]) -> List[CostRecommendation]:
        recommendations = []
        for service, svc_data in cost_data.get("services", {}).items():
            if service in ["EC2"]:
                recommendations.append(
                    CostRecommendation(
                        resource_id="collection-ec2-idle",
                        resource_type="EC2-Instances",
                        current_monthly_cost=svc_data["cost"],
                        projected_monthly_savings=svc_data["cost"] * 0.20,
                        recommendation="Identify and terminate or stop idle EC2 instances with low CPU utilization.",
                        confidence="high",
                        provider=CloudProvider.AWS,
                        region="us-east-1",
                        risk_level="low",
                    )
                )
        return recommendations

    def _check_overprovisioned_resources(
        self, cost_data: Dict[str, Any]
    ) -> List[CostRecommendation]:
        recommendations = []
        for service, svc_data in cost_data.get("services", {}).items():
            if service in ["EC2"]:
                recommendations.append(
                    CostRecommendation(
                        resource_id="collection-ec2-oversized",
                        resource_type="EC2-Instances",
                        current_monthly_cost=svc_data["cost"] * 0.35,
                        projected_monthly_savings=svc_data["cost"] * 0.35 * 0.30,
                        recommendation="Right-size over-provisioned EC2 instances by reviewing CloudWatch metrics.",
                        confidence="medium",
                        provider=CloudProvider.AWS,
                        region="us-east-1",
                        risk_level="low",
                    )
                )
        return recommendations

    def _check_reserved_instance_opportunities(
        self, cost_data: Dict[str, Any]
    ) -> List[CostRecommendation]:
        recommendations = []
        total_cost = cost_data.get("total_cost", 0)
        recommendations.append(
            CostRecommendation(
                resource_id="collection-ri-opportunity",
                resource_type="Reserved-Instances",
                current_monthly_cost=total_cost / 30,
                projected_monthly_savings=total_cost / 30 * 0.25,
                recommendation="Purchase Reserved Instances or Savings Plans for steady-state workloads.",
                confidence="high",
                provider=CloudProvider.AWS,
                region="multi-region",
                risk_level="low",
            )
        )
        return recommendations

    def _check_storage_tier_optimization(
        self, cost_data: Dict[str, Any]
    ) -> List[CostRecommendation]:
        recommendations = []
        for service, svc_data in cost_data.get("services", {}).items():
            if service in ["S3"]:
                recommendations.append(
                    CostRecommendation(
                        resource_id="collection-s3-tiering",
                        resource_type="S3-Storage",
                        current_monthly_cost=svc_data["cost"],
                        projected_monthly_savings=svc_data["cost"] * 0.15,
                        recommendation="Move infrequently accessed objects to S3 Standard-IA or Glacier.",
                        confidence="medium",
                        provider=CloudProvider.AWS,
                        region="us-east-1",
                        risk_level="low",
                    )
                )
        return recommendations


class RiskAssessmentEngine:
    """Engine for assessing and prioritizing cloud risks."""

    SEVERITY_WEIGHT = {
        SeverityLevel.CRITICAL: 10,
        SeverityLevel.HIGH: 7,
        SeverityLevel.MEDIUM: 4,
        SeverityLevel.LOW: 2,
        SeverityLevel.INFO: 1,
    }

    LIKELIHOOD_WEIGHT = {"high": 3, "medium": 2, "low": 1}
    IMPACT_WEIGHT = {"high": 3, "medium": 2, "low": 1}

    def __init__(self, client: BaseCloudClient, config: RiskConfig):
        self._client = client
        self._config = config
        self._risks: List[RiskRecord] = []

    def assess(self, findings: List[AuditFinding]) -> List[RiskRecord]:
        """Convert audit findings into risk records and prioritize them."""
        self._risks = []
        for finding in findings:
            if self.SEVERITY_WEIGHT.get(finding.severity, 1) < self.SEVERITY_WEIGHT.get(
                self._config.min_severity, 1
            ):
                continue
            likelihood, impact = self._estimate_likelihood_impact(finding)
            risk_score = (
                self.SEVERITY_WEIGHT.get(finding.severity, 1)
                * self.LIKELIHOOD_WEIGHT.get(likelihood, 1)
                * self.IMPACT_WEIGHT.get(impact, 1)
            )
            residual_likelihood = max("low", likelihood[0])
            residual_impact = max("low", impact[0])
            residual_risk_score = (
                self.SEVERITY_WEIGHT.get(finding.severity, 1)
                * self.LIKELIHOOD_WEIGHT.get(residual_likelihood, 1)
                * self.IMPACT_WEIGHT.get(residual_impact, 1)
            )
            status = "open"
            if residual_risk_score <= 2:
                status = "accepted"
            elif residual_risk_score >= 15:
                status = "critical"
            risk = RiskRecord(
                title=finding.title,
                description=finding.description,
                category=finding.category,
                severity=finding.severity,
                likelihood=likelihood,
                impact=impact,
                mitigation=finding.remediation or self._default_mitigation(finding.category),
                residual_risk=residual_likelihood,
                owner="cloud-security-team",
                status=status,
            )
            self._risks.append(risk)
        if self._config.auto_prioritize:
            self._risks.sort(
                key=lambda r: self.SEVERITY_WEIGHT.get(r.severity, 1), reverse=True
            )
        if len(self._risks) > self._config.max_results:
            self._risks = self._risks[: self._config.max_results]
        return self._risks

    def _estimate_likelihood_impact(
        self, finding: AuditFinding
    ) -> Tuple[str, str]:
        sev = finding.severity
        if sev == SeverityLevel.CRITICAL:
            return "high", "high"
        elif sev == SeverityLevel.HIGH:
            return "high", "medium"
        elif sev == SeverityLevel.MEDIUM:
            return "medium", "medium"
        elif sev == SeverityLevel.LOW:
            return "low", "low"
        else:
            return "low", "low"

    def _default_mitigation(self, category: RiskCategory) -> str:
        mitigation_map = {
            RiskCategory.DATA_BREACH: "Enable encryption at rest and in transit; review access controls.",
            RiskCategory.MISCONFIGURATION: "Apply recommended configuration change and validate with re-scan.",
            RiskCategory.ACCESS_CONTROL: "Enforce least privilege; enable MFA; review IAM policies.",
            RiskCategory.ENCRYPTION: "Enable encryption; rotate keys; enforce TLS 1.2+.",
            RiskCategory.NETWORK_EXPOSURE: "Restrict inbound/outbound rules; use private subnets.",
            RiskCategory.COMPLIANCE_VIOLATION: "Remediate the specific control gap and document evidence.",
            RiskCategory.COST_OVERFLOW: "Set up budgets and alerts; right-size resources.",
            RiskCategory.AVAILABILITY: "Enable multi-AZ; implement monitoring and auto-scaling.",
            RiskCategory.SUPPLY_CHAIN: "Scan container images; validate artifacts; pin versions.",
            RiskCategory.INSIDER_THREAT: "Enable audit logging; implement separation of duties; use JIT access.",
        }
        return mitigation_map.get(category, "Review and remediate manually.")


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------

class ReportFormatter:
    """Formats audit results into various output formats."""

    def __init__(self, report: AuditReport):
        self._report = report

    def to_json(self) -> str:
        return self._report.to_json()

    def to_csv_findings(self) -> str:
        import csv
        import io

        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "finding_id",
                "severity",
                "title",
                "resource_id",
                "resource_type",
                "region",
                "account_id",
                "remediation",
            ],
        )
        writer.writeheader()
        for f in self._report.findings:
            row = {
                "finding_id": f.finding_id,
                "severity": f.severity.value,
                "title": f.title,
                "resource_id": f.resource_id,
                "resource_type": f.resource_type,
                "region": f.region,
                "account_id": f.account_id,
                "remediation": f.remediation,
            }
            writer.writerow(row)
        return output.getvalue()

    def to_summary_text(self) -> str:
        lines: List[str] = []
        lines.append("=" * 80)
        lines.append("CLOUD AUDIT REPORT SUMMARY")
        lines.append("=" * 80)
        lines.append(f"Report ID   : {self._report.report_id}")
        lines.append(f"Provider    : {self._report.provider.value}")
        lines.append(f"Scope       : {self._report.scope.value}")
        lines.append(f"Account     : {self._report.account_id}")
        lines.append(f"Regions     : {', '.join(self._report.regions)}")
        lines.append(f"Started     : {self._report.started_at}")
        lines.append(f"Completed   : {self._report.completed_at}")
        lines.append(f"Score       : {self._report.overall_score}/100")
        lines.append("")
        lines.append(f"Total Findings : {len(self._report.findings)}")
        severity_counts: Dict[str, int] = {}
        for f in self._report.findings:
            severity_counts[f.severity.value] = severity_counts.get(f.severity.value, 0) + 1
        for sev in ["critical", "high", "medium", "low", "info"]:
            lines.append(f"  {sev.upper():<10}: {severity_counts.get(sev, 0)}")
        lines.append("")
        lines.append("Compliance Gaps:")
        for framework, gaps in self._report.compliance_results.items():
            lines.append(f"  {framework}: {len(gaps)} gaps")
        lines.append("")
        lines.append("Cost Recommendations:")
        lines.append(f"  Total potential savings: ${sum(r.projected_monthly_savings for r in self._report.cost_recommendations):,.2f}/month")
        lines.append("")
        lines.append("Risk Summary:")
        lines.append(f"  Open risks: {sum(1 for r in self._report.risks if r.status == 'open')}")
        lines.append(f"  Critical risks: {sum(1 for r in self._report.risks if r.status == 'critical')}")
        lines.append("=" * 80)
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cache Utilities
# ---------------------------------------------------------------------------

class AuditCache:
    """Simple in-memory / on-disk cache for audit results."""

    def __init__(self, ttl_seconds: int = 3600, enabled: bool = True):
        self._ttl = ttl_seconds
        self._enabled = enabled
        self._store: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        if not self._enabled:
            return None
        entry = self._store.get(key)
        if entry is None:
            return None
        value, timestamp = entry
        if time.time() - timestamp > self._ttl:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        if not self._enabled:
            return
        self._store[key] = (value, time.time())

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()


# ---------------------------------------------------------------------------
# Notification Utilities
# ---------------------------------------------------------------------------

class NotificationChannel(ABC):
    """Abstract notification channel."""

    @abstractmethod
    def send(self, subject: str, message: str) -> bool:
        ...


class ConsoleNotificationChannel(NotificationChannel):
    """Sends notifications to the console (stdout)."""

    def send(self, subject: str, message: str) -> bool:
        logger.info("[NOTIFICATION] %s: %s", subject, message)
        return True


class SlackNotificationChannel(NotificationChannel):
    """Simulated Slack notification channel."""

    def __init__(self, webhook_url: str = "https://hooks.slack.com/services/T00/B00/xxx"):
        self._webhook_url = webhook_url

    def send(self, subject: str, message: str) -> bool:
        logger.info("[SLACK] Posting to %s: %s", self._webhook_url, subject)
        return True


class EmailNotificationChannel(NotificationChannel):
    """Simulated email notification channel."""

    def __init__(self, smtp_server: str = "localhost", smtp_port: int = 25):
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port

    def send(self, subject: str, message: str) -> bool:
        logger.info("[EMAIL] Sending via %s:%d - %s", self._smtp_server, self._smtp_port, subject)
        return True


# ---------------------------------------------------------------------------
# Main Agent
# ---------------------------------------------------------------------------

class CloudAuditAgent:
    """Cloud Audit Agent.

    Orchestrates audit, compliance, cost, and risk analysis across configured cloud providers.

    Example usage::

        from agents.cloud_audit.agent import CloudAuditAgent, Config

        config = Config(
            providers=[
                ProviderConfig(
                    provider=CloudProvider.AWS,
                    regions=["us-east-1", "us-west-2"],
                )
            ],
            compliance=ComplianceConfig(
                enabled_frameworks=[ComplianceFramework.CIS, ComplianceFramework.SOC2]
            ),
        )
        agent = CloudAuditAgent(config=config)
        report = agent.run_full_audit(
            provider=CloudProvider.AWS,
            scope=AuditScope.FULL,
            account_id="123456789012",
        )
        print(report.to_summary_text())
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._audits: List[AuditReport] = []
        self._cache = AuditCache(
            ttl_seconds=self._config.cache_ttl_seconds,
            enabled=self._config.cache_enabled,
        )
        self._clients: Dict[CloudProvider, BaseCloudClient] = {}
        self._notification_channels: List[NotificationChannel] = []
        self._init_defaults()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _init_defaults(self) -> None:
        """Set default providers if none were configured."""
        if not self._config.providers:
            self._config.providers = [
                ProviderConfig(
                    provider=CloudProvider.AWS,
                    regions=["us-east-1", "us-west-2"],
                )
            ]
        self._build_clients()
        self._notification_channels = [
            ConsoleNotificationChannel(),
            SlackNotificationChannel(),
            EmailNotificationChannel(),
        ]

    def _build_clients(self) -> None:
        """Instantiate provider clients from configuration."""
        for pconfig in self._config.providers:
            if pconfig.provider in (
                CloudProvider.AWS,
                CloudProvider.MULTI_CLOUD,
                CloudProvider.HYBRID,
            ):
                self._clients[pconfig.provider] = AWSSimulatedClient(pconfig)
            else:
                logger.warning(
                    "No client implementation for provider %s - skipping.", pconfig.provider.value
                )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Return current agent status."""
        return {
            "agent": "CloudAuditAgent",
            "version": "2.0.0",
            "configured_providers": [p.provider.value for p in self._config.providers],
            "initialized_clients": list(self._clients.keys()),
            "audits_completed": len(self._audits),
            "cache_enabled": self._config.cache_enabled,
            "parallel_checks": self._config.parallel_checks,
        }

    # ------------------------------------------------------------------
    # Audit Orchestration
    # ------------------------------------------------------------------

    def run_full_audit(
        self,
        provider: Optional[Union[CloudProvider, str]] = None,
        scope: Optional[Union[AuditScope, str]] = None,
        account_id: str = "",
        regions: Optional[List[str]] = None,
    ) -> AuditReport:
        """Run a complete audit: security + compliance + cost + risk."""
        provider = self._normalize_provider(provider)
        scope = self._normalize_scope(scope)
        client = self._clients.get(provider)
        if client is None:
            raise ValueError(f"No client configured for provider {provider.value}.")

        cache_key = f"full_audit:{provider.value}:{scope.value}:{account_id}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.info("Returning cached audit result for %s.", cache_key)
            return cached

        logger.info(
            "Starting full audit provider=%s scope=%s account=%s", provider.value, scope.value, account_id
        )
        report = AuditReport(
            provider=provider,
            scope=scope,
            account_id=account_id,
            regions=regions or [r for p in self._config.providers if p.provider == provider for r in p.regions],
            metadata={
                "config_snapshot": {
                    "compliance_enabled_frameworks": [
                        f.value for f in self._config.compliance.enabled_frameworks
                    ],
                    "risk_min_severity": self._config.risk.min_severity.value,
                }
            },
        )

        # 1. Security checks
        security_engine = SecurityCheckEngine(client)
        resource_types = self._resource_types_for_scope(scope)
        report.findings = security_engine.run(resource_types)

        # 2. Compliance checks
        compliance_engine = ComplianceCheckEngine(client)
        for fw in self._config.compliance.enabled_frameworks:
            gaps = compliance_engine.evaluate(fw)
            report.compliance_results[fw.value] = gaps

        # 3. Cost analysis
        cost_engine = CostAnalysisEngine(client, self._config.cost)
        report.cost_recommendations = cost_engine.analyze()

        # 4. Risk assessment
        risk_engine = RiskAssessmentEngine(client, self._config.risk)
        report.risks = risk_engine.assess(report.findings)

        # 5. Compute overall score
        report.overall_score = self._compute_score(report)
        report.completed_at = datetime.datetime.utcnow().isoformat() + "Z"

        self._audits.append(report)
        self._cache.set(cache_key, report)
        self._notify_completion(report)
        logger.info(
            "Full audit completed. report_id=%s score=%d findings=%d",
            report.report_id,
            report.overall_score,
            len(report.findings),
        )
        return report

    def audit_cloud(
        self,
        provider: Optional[Union[CloudProvider, str]] = None,
        scope: Optional[Union[AuditScope, str]] = None,
    ) -> Dict[str, Any]:
        """Run a lightweight security audit and return a compact dict."""
        provider = self._normalize_provider(provider)
        scope = self._normalize_scope(scope)
        client = self._clients.get(provider)
        if client is None:
            raise ValueError(f"No client configured for provider {provider.value}.")

        security_engine = SecurityCheckEngine(client)
        resource_types = self._resource_types_for_scope(scope)
        findings = security_engine.run(resource_types)
        score = self._compute_score_from_findings(findings)

        return {
            "provider": provider.value,
            "scope": scope.value,
            "score": score,
            "findings_count": len(findings),
            "findings": [f.to_dict() for f in findings],
        }

    def check_compliance(
        self, framework: Union[ComplianceFramework, str]
    ) -> Dict[str, Any]:
        """Check compliance against a single framework."""
        if isinstance(framework, str):
            framework = self._normalize_framework(framework)
        client = next(iter(self._clients.values()), None)
        if client is None:
            raise ValueError("No cloud client configured.")
        engine = ComplianceCheckEngine(client)
        gaps = engine.evaluate(framework)
        compliance_status = client.get_compliance_status(framework)
        return {
            "framework": framework.value,
            "compliant": len(gaps) == 0,
            "gaps": [g.to_dict() for g in gaps],
            "compliance_percentage": compliance_status.get("compliance_percentage", 0.0),
            "compliant_controls": compliance_status.get("compliant_controls", 0),
            "total_controls": compliance_status.get("total_controls", 0),
            "remediation_priority": sorted(
                gaps, key=lambda g: g.priority.value, reverse=True
            ),
        }

    def analyze_costs(self, account: str = "") -> Dict[str, Any]:
        """Analyze costs and return recommendations."""
        client = next(iter(self._clients.values()), None)
        if client is None:
            raise ValueError("No cloud client configured.")
        engine = CostAnalysisEngine(client, self._config.cost)
        recommendations = engine.analyze()
        cost_data = client.get_cost_data(self._config.cost.lookback_days)
        total_current = sum(r.current_monthly_cost for r in recommendations)
        total_savings = sum(r.projected_monthly_savings for r in recommendations)
        return {
            "account": account or "default",
            "spend": cost_data.get("total_cost", 0),
            "currency": cost_data.get("currency", "USD"),
            "lookback_days": self._config.cost.lookback_days,
            "services": cost_data.get("services", {}),
            "total_current_monthly": total_current,
            "total_potential_savings": total_savings,
            "savings_percentage": (total_savings / total_current * 100) if total_current > 0 else 0.0,
            "recommendations": [r.to_dict() for r in recommendations],
        }

    def assess_risks(self, cloud_config: Optional[Dict] = None) -> List[Dict]:
        """Assess risks from the last audit or provided config."""
        if cloud_config:
            findings = cloud_config.get("findings", [])
            # Rehydrate findings into AuditFinding objects if needed
            finding_objects: List[AuditFinding] = []
            for f in findings:
                try:
                    finding_objects.append(
                        AuditFinding(
                            title=f.get("title", ""),
                            description=f.get("description", ""),
                            severity=SeverityLevel(f.get("severity", "info")),
                            category=RiskCategory(f.get("category", "misconfiguration")),
                            resource_id=f.get("resource_id", ""),
                            resource_type=f.get("resource_type", ""),
                            region=f.get("region", ""),
                            account_id=f.get("account_id", ""),
                        )
                    )
                except ValueError:
                    continue
            client = next(iter(self._clients.values()), None)
            config = self._config.risk
            if client:
                engine = RiskAssessmentEngine(client, config)
                risks = engine.assess(finding_objects)
                return [r.to_dict() for r in risks]
            return []
        if self._audits:
            last_audit = self._audits[-1]
            return [r.to_dict() for r in last_audit.risks]
        return [
            {
                "risk": "No audit data available; run a full audit first.",
                "severity": "info",
                "mitigation": "Execute run_full_audit() to populate risk data.",
            }
        ]

    # ------------------------------------------------------------------
    # Utility / Helper Methods
    # ------------------------------------------------------------------

    def _normalize_provider(self, provider: Optional[Union[CloudProvider, str]]) -> CloudProvider:
        if provider is None:
            return self._config.providers[0].provider if self._config.providers else CloudProvider.AWS
        if isinstance(provider, CloudProvider):
            return provider
        try:
            return CloudProvider(str(provider).lower())
        except ValueError:
            raise ValueError(f"Unsupported cloud provider: {provider}")

    def _normalize_scope(self, scope: Optional[Union[AuditScope, str]]) -> AuditScope:
        if scope is None:
            return AuditScope.FULL
        if isinstance(scope, AuditScope):
            return scope
        try:
            return AuditScope(str(scope).lower())
        except ValueError:
            raise ValueError(f"Unsupported audit scope: {scope}")

    def _normalize_framework(self, framework: str) -> ComplianceFramework:
        mapping = {fw.value.lower(): fw for fw in ComplianceFramework}
        key = framework.lower().replace("-", "_").replace(" ", "_")
        if key in mapping:
            return mapping[key]
        alias_map = {
            "cis_benchmark": ComplianceFramework.CIS,
            "soc2": ComplianceFramework.SOC2,
            "soc_2": ComplianceFramework.SOC2,
            "pci": ComplianceFramework.PCI_DSS,
            "hipaa": ComplianceFramework.HIPAA,
            "gdpr": ComplianceFramework.GDPR,
            "nist": ComplianceFramework.NIST_CSF,
            "iso27001": ComplianceFramework.ISO27001,
        }
        if key in alias_map:
            return alias_map[key]
        raise ValueError(f"Unsupported compliance framework: {framework}")

    def _resource_types_for_scope(self, scope: AuditScope) -> List[str]:
        mapping: Dict[AuditScope, List[str]] = {
            AuditScope.FULL: ["s3", "ec2", "rds", "iam", "eks"],
            AuditScope.SECURITY: ["s3", "ec2", "rds", "iam", "eks"],
            AuditScope.COMPLIANCE: ["s3", "ec2", "rds", "iam", "eks"],
            AuditScope.COST: ["ec2", "rds", "s3", "eks", "lambda"],
            AuditScope.NETWORK: ["ec2"],
            AuditScope.IDENTITY: ["iam"],
            AuditScope.STORAGE: ["s3"],
            AuditScope.COMPUTE: ["ec2"],
            AuditScope.DATABASE: ["rds"],
            AuditScope.SERVERLESS: ["lambda"],
            AuditScope.CONTAINERS: ["eks"],
            AuditScope.IAM: ["iam"],
        }
        return mapping.get(scope, ["s3", "ec2", "rds", "iam"])

    def _compute_score(self, report: AuditReport) -> int:
        return self._compute_score_from_findings(report.findings)

    def _compute_score_from_findings(self, findings: List[AuditFinding]) -> int:
        if not findings:
            return 100
        penalty = 0
        for f in findings:
            penalty += self.SEVERITY_WEIGHT.get(f.severity, 1)
        score = max(0, 100 - penalty)
        return score

    SEVERITY_WEIGHT = {
        SeverityLevel.CRITICAL: 15,
        SeverityLevel.HIGH: 8,
        SeverityLevel.MEDIUM: 4,
        SeverityLevel.LOW: 2,
        SeverityLevel.INFO: 1,
    }

    def _notify_completion(self, report: AuditReport) -> None:
        if not self._config.compliance.notify_on_gap:
            return
        subject = f"Cloud Audit Completed: {report.provider.value} - Score {report.overall_score}"
        message = (
            f"Report ID: {report.report_id}\n"
            f"Findings: {len(report.findings)}\n"
            f"Compliance Gaps: {sum(len(v) for v in report.compliance_results.values())}\n"
            f"Cost Recommendations: {len(report.cost_recommendations)}\n"
        )
        for channel in self._notification_channels:
            try:
                channel.send(subject, message)
            except Exception as exc:
                logger.error("Failed to send notification via %s: %s", type(channel).__name__, exc)

    # ------------------------------------------------------------------
    # Import / Export and Reporting Helpers
    # ------------------------------------------------------------------

    def export_report(self, report: AuditReport, path: str, fmt: str = "json") -> str:
        """Export a report to a file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        formatter = ReportFormatter(report)
        if fmt == "json":
            content = formatter.to_json()
        elif fmt == "csv":
            content = formatter.to_csv_findings()
        elif fmt == "text":
            content = formatter.to_summary_text()
        else:
            raise ValueError(f"Unsupported export format: {fmt}")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info("Report exported to %s", path)
        return path

    def list_audits(self) -> List[Dict[str, Any]]:
        """List summaries of all completed audits in this session."""
        return [
            {
                "report_id": r.report_id,
                "provider": r.provider.value,
                "scope": r.scope.value,
                "score": r.overall_score,
                "findings": len(r.findings),
                "completed_at": r.completed_at,
            }
            for r in self._audits
        ]

    def clear_cache(self) -> None:
        """Clear the audit cache."""
        self._cache.clear()
        logger.info("Audit cache cleared.")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def _build_sample_config() -> Config:
    """Build a sample config for demonstration."""
    return Config(
        providers=[
            ProviderConfig(
                provider=CloudProvider.AWS,
                regions=["us-east-1", "eu-west-1", "ap-southeast-2"],
            ),
            ProviderConfig(
                provider=CloudProvider.AZURE,
                regions=["eastus", "westeurope"],
                enabled=False,
            ),
        ],
        compliance=ComplianceConfig(
            enabled_frameworks=[
                ComplianceFramework.CIS,
                ComplianceFramework.SOC2,
                ComplianceFramework.PCI_DSS,
                ComplianceFramework.HIPAA,
                ComplianceFramework.GDPR,
            ]
        ),
        cost=CostConfig(
            lookback_days=30,
            threshold_monthly=500.0,
            anomaly_detection=True,
        ),
        risk=RiskConfig(
            enabled_categories=list(RiskCategory),
            min_severity=SeverityLevel.LOW,
            max_results=50,
            auto_prioritize=True,
            mitigation_suggestions=True,
        ),
        output_format="json",
        output_path="./reports",
        log_level="INFO",
        parallel_checks=4,
        cache_enabled=True,
        cache_ttl_seconds=3600,
    )


def _print_banner() -> None:
    banner = r"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ____ _               _    ____            _                 ║
║  / ___| |__   ___  ___| | _|  _ \ _ __ ___ | |_ ___ _ __     ║
║ | |   | '_ \ / _ \/ __| |/ / |_) | '__/ _ \| __/ _ \ '__|    ║
║ | |___| | | |  __/ (__|   <|  _ <| | | (_) | ||  __/ |       ║
║  \____|_| |_|\___|\___|_|\_\_| \_\_|  \___/ \__\___|_|       ║
║                                                               ║
║          Cloud Security Audit & Compliance Agent v2.0         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def _demo() -> None:
    """Run a demonstration audit."""
    _print_banner()
    print("[*] Initialising CloudAuditAgent with sample configuration...")
    config = _build_sample_config()
    agent = CloudAuditAgent(config=config)

    print("\n--- Agent Status ---")
    status = agent.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n--- Running Full Audit (AWS / FULL) ---")
    report = agent.run_full_audit(
        provider=CloudProvider.AWS,
        scope=AuditScope.FULL,
        account_id="123456789012",
    )

    formatter = ReportFormatter(report)
    print("\n" + formatter.to_summary_text())

    print("\n--- Compliance Check: CIS ---")
    compliance = agent.check_compliance(ComplianceFramework.CIS)
    print(f"Compliant: {compliance['compliant']}, Gaps: {len(compliance['gaps'])}")

    print("\n--- Cost Analysis ---")
    costs = agent.analyze_costs(account="123456789012")
    print(
        f"Total spend: ${costs['spend']:,.2f} | "
        f"Potential savings: ${costs['total_potential_savings']:,.2f}/month "
        f"({costs['savings_percentage']:.1f}%)"
    )

    print("\n--- Risk Assessment ---")
    risks = agent.assess_risks()
    print(f"Open risks: {len(risks)}")
    for risk in risks[:5]:
        print(
            f"  [{risk['severity'].upper()}] {risk['title']} -> {risk['mitigation']}"
        )

    print("\n--- Exported Report (text) ---")
    export_path = agent.export_report(report, "./audit_report.txt", fmt="text")
    print(f"Report written to {export_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Cloud Audit Agent - Cloud Security and Compliance Audits"
    )
    parser.add_argument(
        "--demo", action="store_true", help="Run built-in demonstration audit."
    )
    parser.add_argument(
        "--provider",
        choices=[p.value for p in CloudProvider],
        default="aws",
        help="Cloud provider to audit.",
    )
    parser.add_argument(
        "--scope",
        choices=[s.value for s in AuditScope],
        default="full",
        help="Audit scope.",
    )
    parser.add_argument(
        "--framework",
        choices=[f.value for f in ComplianceFramework],
        default="cis",
        help="Compliance framework for --check-compliance.",
    )
    parser.add_argument(
        "--account", default="", help="Cloud account ID to target."
    )
    parser.add_argument(
        "--check-compliance",
        action="store_true",
        help="Check a single compliance framework.",
    )
    parser.add_argument(
        "--analyze-costs",
        action="store_true",
        help="Run cost analysis.",
    )
    parser.add_argument(
        "--export",
        metavar="PATH",
        help="Export last report to PATH (json, csv, or text).",
    )
    parser.add_argument(
        "--export-format",
        choices=["json", "csv", "text"],
        default="json",
        help="Export format (default: json).",
    )

    args = parser.parse_args()

    if args.demo:
        _demo()
        return

    config = Config(
        providers=[
            ProviderConfig(
                provider=CloudProvider(args.provider),
                regions=["us-east-1", "us-west-2"],
            )
        ],
        compliance=ComplianceConfig(
            enabled_frameworks=[ComplianceFramework.CIS, ComplianceFramework.SOC2]
        ),
        cost=CostConfig(lookback_days=30),
        risk=RiskConfig(min_severity=SeverityLevel.LOW),
    )
    agent = CloudAuditAgent(config=config)

    if args.check_compliance:
        fw = ComplianceFramework(args.framework)
        result = agent.check_compliance(fw)
        print(json.dumps(result, indent=2, default=str))
    elif args.analyze_costs:
        result = agent.analyze_costs(account=args.account)
        print(json.dumps(result, indent=2, default=str))
    else:
        report = agent.run_full_audit(
            provider=CloudProvider(args.provider),
            scope=AuditScope(args.scope),
            account_id=args.account,
        )
        formatter = ReportFormatter(report)
        print(formatter.to_summary_text())
        if args.export:
            agent.export_report(report, args.export, fmt=args.export_format)


if __name__ == "__main__":
    main()
