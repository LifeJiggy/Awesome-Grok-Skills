"""Architecture Review Agent - Software Architecture Assessment."""

from __future__ import annotations

import logging
import json
import re
import hashlib
import csv
import io
import time
from dataclasses import dataclass, field
from typing import (
    List,
    Dict,
    Any,
    Optional,
    Tuple,
    Set,
    Union,
    Sequence,
    Callable,
)
from enum import Enum
from pathlib import Path
from datetime import datetime, timedelta
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("architecture-review-agent")


class ArchitecturePattern(Enum):
    MICROSERVICES = "microservices"
    MONOLITHIC = "monolithic"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    CQRS = "cqrs"
    EVENT_SOURCING = "event_sourcing"
    PIPES_AND_FILTERS = "pipes_and_filters"
    BLACKBOARD = "blackboard"


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ReviewCategory(Enum):
    SECURITY = "security"
    SCALABILITY = "scalability"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    RELIABILITY = "reliability"
    COST = "cost"
    COMPLIANCE = "compliance"
    USABILITY = "usability"
    ACCESSIBILITY = "accessibility"
    OBSERVABILITY = "observability"


class ReviewType(Enum):
    FULL = "full"
    SECURITY = "security"
    PERFORMANCE = "performance"
    SCALABILITY = "scalability"
    QUICK = "quick"
    COMPLIANCE = "compliance"


class MetricStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class Config:
    review_type: str = "full"
    include_security: bool = True
    include_performance: bool = True
    include_scalability: bool = True
    include_maintainability: bool = True
    include_reliability: bool = True
    include_cost: bool = True
    include_compliance: bool = True
    include_observability: bool = True
    include_accessibility: bool = False
    include_usability: bool = False
    output_format: str = "json"
    score_threshold_pass: float = 70.0
    score_threshold_warning: float = 50.0
    max_findings: int = 50
    model_version: str = "v2"
    reviewer: str = "automated"
    tags: List[str] = field(default_factory=list)
    excluded_checks: List[str] = field(default_factory=list)
    custom_rules_path: Optional[str] = None
    benchmark_version: str = "2024-Q4"
    auto_fix_suggestions: bool = True
    generate_report: bool = True
    export_path: Optional[str] = None


@dataclass
class ReviewResult:
    score: float
    findings: List[Dict]
    recommendations: List[str]
    summary: str = ""
    categories: Dict[str, float] = field(default_factory=dict)
    patterns_detected: List[str] = field(default_factory=list)
    technical_debt_items: List[Dict] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    generated_at: str = ""
    review_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    compliance_results: Dict[str, Any] = field(default_factory=dict)
    architecture_snapshot: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Finding:
    category: ReviewCategory
    severity: Severity
    title: str
    description: str
    recommendation: str
    affected_components: List[str] = field(default_factory=list)
    code_example: Optional[str] = None
    references: List[str] = field(default_factory=list)
    effort: str = "medium"
    impact: str = "medium"
    auto_fixable: bool = False
    cwe_id: Optional[str] = None
    owasp_category: Optional[str] = None
    rule_id: str = ""
    remediation_steps: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    first_detected: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ArchitectureMetric:
    name: str
    value: float
    unit: str
    threshold: float
    status: str
    description: str = ""
    trend: str = "stable"
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ComplianceCheck:
    framework: str
    check_id: str
    name: str
    description: str
    status: str
    severity: str
    recommendation: str = ""
    references: List[str] = field(default_factory=list)


class PatternDetector:
    def __init__(self):
        self._patterns: Dict[ArchitecturePattern, List[str]] = {
            ArchitecturePattern.MICROSERVICES: [
                r"service[_\-\s]?mesh",
                r"api[_\-\s]?gateway",
                r"microservice",
                r"docker-compose",
                r"kubernetes",
                r"k8s",
                r"event[_\-\s]?bus",
                r"message[_\-\s]?queue",
            ],
            ArchitecturePattern.MONOLITHIC: [
                r"monolith",
                r"single[_\-\s]?application",
                r"all[_\-\s]?in[_\-\s]?one",
            ],
            ArchitecturePattern.SERVERLESS: [
                r"serverless",
                r"lambda",
                r"azure[_\-\s]?functions",
                r"cloud[_\-\s]?functions",
            ],
            ArchitecturePattern.EVENT_DRIVEN: [
                r"event[_\-\s]?driven",
                r"kafka",
                r"rabbitmq",
                r"pubsub",
            ],
            ArchitecturePattern.LAYERED: [
                r"controller",
                r"service[_\-\s]?layer",
                r"repository[_\-\s]?layer",
            ],
            ArchitecturePattern.HEXAGONAL: [
                r"hexagonal",
                r"ports[_\-\s]?adapters",
            ],
            ArchitecturePattern.CQRS: [
                r"cqrs",
                r"command[_\-\s]?query",
                r"read[_\-\s]?model",
            ],
            ArchitecturePattern.EVENT_SOURCING: [
                r"event[_\-\s]?sourcing",
                r"event[_\-\s]?store",
                r"append[_\-\s]?only",
            ],
            ArchitecturePattern.PIPES_AND_FILTERS: [
                r"pipes?[_\-\s]?and[_\-\s]?filters?",
                r"stream[_\-\s]?processing",
            ],
            ArchitecturePattern.BLACKBOARD: [
                r"blackboard",
                r"shared[_\-\s]?repository",
                r"knowledge[_\-\s]?base",
            ],
        }

    def detect_patterns(self, codebase: str) -> List[str]:
        detected = []
        codebase_lower = codebase.lower()
        for pattern, keywords in self._patterns.items():
            for keyword in keywords:
                if re.search(keyword, codebase_lower):
                    detected.append(pattern.value)
                    break
        return detected

    def get_primary_pattern(self, architecture: Dict) -> str:
        patterns = architecture.get("patterns", [])
        if ArchitecturePattern.MICROSERVICES.value in patterns:
            return ArchitecturePattern.MICROSERVICES.value
        if ArchitecturePattern.EVENT_DRIVEN.value in patterns:
            return ArchitecturePattern.EVENT_DRIVEN.value
        if ArchitecturePattern.SERVERLESS.value in patterns:
            return ArchitecturePattern.SERVERLESS.value
        if ArchitecturePattern.MONOLITHIC.value in patterns:
            return ArchitecturePattern.MONOLITHIC.value
        return ArchitecturePattern.LAYERED.value

    def analyze_pattern_usage(self, architecture: Dict) -> Dict[str, Any]:
        patterns = architecture.get("patterns", [])
        analysis = {"total_patterns": len(patterns), "breakdown": {}, "confidence": 0.0}
        for pattern in patterns:
            analysis["breakdown"][pattern] = analysis["breakdown"].get(pattern, 0) + 1
        unique_patterns = len(analysis["breakdown"])
        analysis["confidence"] = min(100.0, unique_patterns * 15 + 20)
        return analysis

    def compare_patterns(self, arch_a: Dict, arch_b: Dict) -> Dict[str, Any]:
        patterns_a = set(arch_a.get("patterns", []))
        patterns_b = set(arch_b.get("patterns", []))
        return {
            "common": list(patterns_a & patterns_b),
            "unique_to_a": list(patterns_a - patterns_b),
            "unique_to_b": list(patterns_b - patterns_a),
            "jaccard_index": len(patterns_a & patterns_b) / max(1, len(patterns_a | patterns_b)),
        }


class ScalabilityAnalyzer:
    def assess_scalability(self, architecture: Dict) -> Dict[str, Any]:
        horizontal = self._score_horizontal(architecture)
        vertical = self._score_vertical(architecture)
        data = self._score_data(architecture)
        network = self._score_network(architecture)
        overall = round((horizontal + vertical + data + network) / 4, 2)
        return {
            "score": overall,
            "horizontal": horizontal,
            "vertical": vertical,
            "data": data,
            "network": network,
            "bottlenecks": self._identify_bottlenecks(architecture),
            "recommendations": self._get_recommendations(architecture, overall),
        }

    def _score_horizontal(self, a: Dict) -> float:
        score = 50.0
        if a.get("load_balancer"):
            score += 10.0
        if a.get("stateless_services"):
            score += 10.0
        if a.get("containerized"):
            score += 10.0
        if a.get("orchestration") in ["kubernetes", "docker-swarm"]:
            score += 10.0
        if a.get("edge_computing"):
            score += 5.0
        return min(100.0, score)

    def _score_vertical(self, a: Dict) -> float:
        score = 50.0
        if a.get("auto_scaling"):
            score += 15.0
        if a.get("resource_limits"):
            score += 10.0
        if a.get("elasticity"):
            score += 10.0
        if a.get("resource_monitoring"):
            score += 10.0
        return min(100.0, score)

    def _score_data(self, a: Dict) -> float:
        score = 40.0
        if a.get("database", {}).get("replication"):
            score += 15.0
        if a.get("caching"):
            score += 10.0
        if a.get("database", {}).get("sharding"):
            score += 10.0
        if a.get("cdn"):
            score += 10.0
        if a.get("database", {}).get("connection_pooling"):
            score += 5.0
        return min(100.0, score)

    def _score_network(self, a: Dict) -> float:
        score = 50.0
        if a.get("api_gateway"):
            score += 10.0
        if a.get("message_queue"):
            score += 10.0
        if a.get("service_mesh"):
            score += 15.0
        if a.get("edge_computing"):
            score += 10.0
        if a.get("cdn"):
            score += 5.0
        return min(100.0, score)

    def _identify_bottlenecks(self, a: Dict) -> List[Dict]:
        bottlenecks = []
        if not a.get("caching"):
            bottlenecks.append({"component": "cache", "severity": "high", "description": "No caching layer"})
        if not a.get("load_balancer"):
            bottlenecks.append({"component": "load_balancer", "severity": "medium", "description": "No load balance"})
        if not a.get("database", {}).get("replication"):
            bottlenecks.append({"component": "database", "severity": "high", "description": "Database replication missing"})
        if a.get("shared_database"):
            bottlenecks.append({"component": "database", "severity": "critical", "description": "Shared database"})
        if not a.get("auto_scaling"):
            bottlenecks.append({"component": "compute", "severity": "medium", "description": "No auto-scaling"})
        if not a.get("cdn") and a.get("static_assets"):
            bottlenecks.append({"component": "cdn", "severity": "low", "description": "No CDN for static assets"})
        return bottlenecks

    def _get_recommendations(self, a: Dict, score: float) -> List[str]:
        recs = []
        if score < 50:
            recs.append("Add load balancing and stateless services for horizontal scaling.")
            recs.append("Implement database sharding or read replicas.")
        if score < 70:
            recs.append("Add a distributed caching layer like Redis or Memcached.")
            recs.append("Consider containerization and orchestration for dynamic scaling.")
        if a.get("shared_database"):
            recs.append("Migrate to per-service databases to reduce coupling.")
        if not a.get("cdn") and a.get("static_assets"):
            recs.append("Add a CDN for static asset delivery.")
        recs.append("Monitor scaling metrics and set auto-scaling policies based on load.")
        return recs


class SecurityAnalyzer:
    def assess_security(self, a: Dict) -> Dict[str, Any]:
        auth = self._score_auth(a)
        authz = self._score_authz(a)
        crypto = self._score_crypto(a)
        net = self._score_network(a)
        data = self._score_data(a)
        comp = self._score_compliance(a)
        overall = round((auth + authz + crypto + net + data + comp) / 6, 2)
        return {
            "score": overall,
            "authentication": auth,
            "authorization": authz,
            "cryptography": crypto,
            "network_security": net,
            "data_protection": data,
            "compliance": comp,
            "vulnerabilities": self._vulns(a),
            "recommendations": self._recs(a, overall),
        }

    def _score_auth(self, a: Dict) -> float:
        score = 30.0
        auth = a.get("authentication", {})
        if auth.get("type") in ["jwt", "oauth2", "oidc"]:
            score += 25.0
        if auth.get("mfa"):
            score += 15.0
        if auth.get("rbac"):
            score += 10.0
        if auth.get("session_management"):
            score += 5.0
        if auth.get("password_policy"):
            score += 5.0
        return min(100.0, score)

    def _score_authz(self, a: Dict) -> float:
        score = 30.0
        if a.get("authorization", {}).get("type") == "rbac":
            score += 20.0
        if a.get("authorization", {}).get("fine_grained"):
            score += 15.0
        if a.get("authorization", {}).get("least_privilege"):
            score += 10.0
        return min(100.0, score)

    def _score_crypto(self, a: Dict) -> float:
        score = 30.0
        c = a.get("cryptography", {})
        if c.get("tls_enabled"):
            score += 15.0
        if c.get("tls_version") in ["1.3", "TLS 1.3"]:
            score += 10.0
        if c.get("encryption_at_rest"):
            score += 15.0
        if c.get("key_management") in ["vault", "aws-kms", "azure-keyvault"]:
            score += 15.0
        if c.get("hashing_algorithm") in ["bcrypt", "argon2"]:
            score += 5.0
        return min(100.0, score)

    def _score_network(self, a: Dict) -> float:
        score = 30.0
        n = a.get("network_security", {})
        if n.get("waf"):
            score += 15.0
        if n.get("ddos_protection"):
            score += 10.0
        if n.get("vpc"):
            score += 10.0
        if n.get("zero_trust"):
            score += 15.0
        if n.get("private_endpoints"):
            score += 5.0
        return min(100.0, score)

    def _score_data(self, a: Dict) -> float:
        score = 30.0
        d = a.get("data_protection", {})
        if d.get("pii_encryption"):
            score += 15.0
        if d.get("access_logging"):
            score += 10.0
        if d.get("data_masking"):
            score += 10.0
        if d.get("backup_encryption"):
            score += 15.0
        return min(100.0, score)

    def _score_compliance(self, a: Dict) -> float:
        score = 30.0
        c = a.get("compliance", {})
        if c.get("gdpr"):
            score += 15.0
        if c.get("soc2"):
            score += 15.0
        if c.get("pci_dss"):
            score += 15.0
        if c.get("iso27001"):
            score += 10.0
        return min(100.0, score)

    def _vulns(self, a: Dict) -> List[Dict]:
        vulns = []
        if not a.get("authentication"):
            vulns.append({"category": "security", "severity": "critical", "title": "No authentication mechanism",
                          "description": "No authentication mechanism detected.",
                          "recommendation": "Add OAuth2/OIDC or JWT-based authentication with MFA support."})
        if not a.get("cryptography", {}).get("tls_enabled"):
            vulns.append({"category": "security", "severity": "high", "title": "No TLS encryption",
                          "description": "TLS is not enabled.",
                          "recommendation": "Enable TLS 1.3 and enforce HTTPS across all services."})
        if a.get("shared_database"):
            vulns.append({"category": "architecture", "severity": "critical", "title": "Shared database",
                          "description": "Shared database across services creates tight coupling.",
                          "recommendation": "Use per-service databases to reduce coupling and improve scalability."})
        if not a.get("authorization", {}).get("least_privilege"):
            vulns.append({"category": "security", "severity": "high", "title": "No least privilege",
                          "description": "Authorization model does not enforce least privilege.",
                          "recommendation": "Adopt RBAC with scoped permissions and regular access reviews."})
        if a.get("database", {}).get("public_access"):
            vulns.append({"category": "security", "severity": "critical", "title": "Public database access",
                          "description": "Database allows public access from the internet.",
                          "recommendation": "Restrict database access to known IP ranges or private networks only."})
        return vulns

    def _recs(self, a: Dict, score: float) -> List[str]:
        recs = []
        if score < 50:
            recs.append("Implement OAuth2/OIDC or JWT-based authentication with MFA support.")
            recs.append("Enable TLS 1.3 and enforce HTTPS across all services.")
        if score < 70:
            recs.append("Adopt RBAC with least-privilege access control.")
            recs.append("Encrypt data at rest and in transit using managed key services.")
        if score < 85:
            recs.append("Enable comprehensive audit logging for security events.")
            recs.append("Implement secrets management with a dedicated vault service.")
        recs.append("Conduct regular penetration tests and threat modeling sessions.")
        return recs


class PerformanceAnalyzer:
    def __init__(self):
        self._thresholds = {
            "api_latency_p99_ms": {"warn": 500, "critical": 1000},
            "throughput_rps": {"warn": 1000, "critical": 500},
            "error_rate_percent": {"warn": 1.0, "critical": 5.0},
            "availability_percent": {"warn": 99.9, "critical": 99.5},
            "memory_usage_mb": {"warn": 512, "critical": 1024},
            "cpu_usage_percent": {"warn": 70.0, "critical": 90.0},
            "cold_start_ms": {"warn": 2000, "critical": 5000},
            "db_query_time_ms": {"warn": 100, "critical": 500},
        }

    def analyze_performance(self, a: Dict, metrics: Optional[Dict] = None) -> Dict[str, Any]:
        metrics = metrics or {}
        latency = self._score(metrics.get("api_latency_p99_ms", 300), self._t["api_latency_p99_ms"])
        throughput = self._score(metrics.get("throughput_rps", 2000), self._t["throughput_rps"], inverted=True)
        error = self._score(metrics.get("error_rate_percent", 0.1), self._t["error_rate_percent"])
        avail = self._score(metrics.get("availability_percent", 99.99), self._t["availability_percent"])
        mem = self._score(metrics.get("memory_usage_mb", 256), self._t["memory_usage_mb"])
        cpu = self._score(metrics.get("cpu_usage_percent", 50.0), self._t["cpu_usage_percent"])
        cold = self._score(metrics.get("cold_start_ms", 800), self._t["cold_start_ms"])
        db = self._score(metrics.get("db_query_time_ms", 50), self._t["db_query_time_ms"])
        overall = round((latency + throughput + error + avail + mem + cpu + cold + db) / 8, 2)
        return {
            "score": overall,
            "latency": latency,
            "throughput": throughput,
            "availability": avail,
            "error_rate": error,
            "resource_usage": (mem + cpu) / 2,
            "cold_start": cold,
            "database": db,
            "recommendations": self._recs(metrics),
        }

    @property
    def _t(self) -> Dict[str, Dict]:
        return self._thresholds

    def _score(self, v: Optional[float], t: Dict[str, float], inverted: bool = False) -> float:
        if v is None:
            return 70.0
        critical = t.get("critical", 9999)
        warn = t.get("warn", 9999)
        if inverted:
            if v <= critical:
                return 30.0
            if v <= warn:
                return 60.0
            return 90.0
        else:
            if v >= critical:
                return 30.0
            if v >= warn:
                return 60.0
        return 90.0

    def _recs(self, m: Dict) -> List[str]:
        recs = []
        if m.get("api_latency_p99_ms", 0) > 500:
            recs.append("Optimize API latency: review slow endpoints and implement caching.")
        if m.get("throughput_rps", 10000) < 1000:
            recs.append("Increase throughput: scale horizontally and add load balancing.")
        if m.get("error_rate_percent", 0) > 1.0:
            recs.append("Reduce error rate: add circuit breakers and review error logs.")
        if m.get("cold_start_ms", 0) > 2000:
            recs.append("Improve cold start times: use provisioned concurrency or reserved instances.")
        if m.get("db_query_time_ms", 0) > 100:
            recs.append("Optimize database queries: add indexes and consider read replicas.")
        return recs


class TechDebtAnalyzer:
    def identify_tech_debt(self, codebase: str, arch: Dict) -> List[Dict]:
        debt = []
        if "requirements.txt" in codebase or "package.json" in codebase:
            debt.append({"area": "dependencies", "priority": "high",
                          "description": "Outdated dependencies detected.",
                          "recommendation": "Update to latest stable versions and enable automated updates."})
        if not arch.get("test_coverage", {}).get("unit"):
            debt.append({"area": "testing", "priority": "high",
                          "description": "Insufficient unit test coverage.",
                          "recommendation": "Increase unit test coverage to at least 80%."})
        if not arch.get("documentation"):
            debt.append({"area": "documentation", "priority": "medium",
                          "description": "Insufficient architectural documentation.",
                          "recommendation": "Create ADRs for major decisions."})
        if arch.get("circular_dependencies"):
            debt.append({"area": "code_structure", "priority": "critical",
                          "description": "Circular dependencies detected.",
                          "recommendation": "Refactor to remove circular dependencies."})
        if not arch.get("monitoring"):
            debt.append({"area": "observability", "priority": "medium",
                          "description": "No observability or monitoring strategy.",
                          "recommendation": "Implement structured logging, metrics, and tracing."})
        if arch.get("deprecated_apis"):
            debt.append({"area": "deprecation", "priority": "high",
                          "description": "Deprecated APIs still in use.",
                          "recommendation": "Migrate to supported API versions."})
        if not arch.get("backup_strategy"):
            debt.append({"area": "resilience", "priority": "high",
                          "description": "No backup strategy defined.",
                          "recommendation": "Implement regular backups and verify restore procedures."})
        return debt

    def estimate_tech_debt(self, debt_items: List[Dict]) -> Dict[str, Any]:
        priority_hours = {"critical": 40, "high": 16, "medium": 8, "low": 4}
        total = sum(priority_hours.get(item.get("priority", "low"), 4) for item in debt_items)
        return {"total_hours": total, "total_sprint_days": round(total / 8, 1)}


class ComplianceChecker:
    def __init__(self):
        self._frameworks = self._init_frameworks()

    def _init_frameworks(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        return {
            "OWASP": {
                "A01": {"name": "Broken Access Control", "cat": "security", "sev": "critical"},
                "A02": {"name": "Cryptographic Failures", "cat": "security", "sev": "high"},
                "A03": {"name": "Injection", "cat": "security", "sev": "critical"},
                "A04": {"name": "Insecure Design", "cat": "security", "sev": "high"},
                "A05": {"name": "Security Misconfiguration", "cat": "security", "sev": "high"},
                "A06": {"name": "Vulnerable and Outdated Components", "cat": "security", "sev": "high"},
                "A07": {"name": "Identification and Authentication Failures", "cat": "security", "sev": "high"},
                "A08": {"name": "Software and Data Integrity Failures", "cat": "security", "sev": "medium"},
                "A09": {"name": "Security Logging and Monitoring Failures", "cat": "security", "sev": "medium"},
                "A10": {"name": "Server-Side Request Forgery", "cat": "security", "sev": "medium"},
            },
            "GDPR": {
                "gdpr_01": {"name": "Lawfulness and fairness", "cat": "compliance", "sev": "high"},
                "gdpr_02": {"name": "Purpose limitation", "cat": "compliance", "sev": "medium"},
                "gdpr_03": {"name": "Data minimization", "cat": "compliance", "sev": "medium"},
                "gdpr_04": {"name": "Accuracy", "cat": "compliance", "sev": "medium"},
                "gdpr_05": {"name": "Storage limitation", "cat": "compliance", "sev": "medium"},
                "gdpr_06": {"name": "Integrity and confidentiality", "cat": "compliance", "sev": "high"},
                "gdpr_07": {"name": "Data subject rights", "cat": "compliance", "sev": "high"},
            },
            "SOC2": {
                "soc2_cc": {"name": "Common Criteria", "cat": "compliance", "sev": "high"},
                "soc2_a": {"name": "Availability", "cat": "reliability", "sev": "high"},
                "soc2_c": {"name": "Confidentiality", "cat": "security", "sev": "high"},
                "soc2_p": {"name": "Privacy", "cat": "compliance", "sev": "high"},
            },
            "PCI-DSS": {
                "pci_01": {"name": "Install and maintain a firewall", "cat": "security", "sev": "high"},
                "pci_02": {"name": "Do not use vendor defaults", "cat": "security", "sev": "high"},
                "pci_03": {"name": "Protect stored cardholder data", "cat": "security", "sev": "critical"},
                "pci_04": {"name": "Encrypt transmission of cardholder data", "cat": "security", "sev": "critical"},
                "pci_05": {"name": "Protect against malware", "cat": "security", "sev": "high"},
            },
            "NIST": {
                "nist_id": {"name": "Identify", "cat": "compliance", "sev": "high"},
                "nist_pr": {"name": "Protect", "cat": "security", "sev": "high"},
                "nist_de": {"name": "Detect", "cat": "observability", "sev": "medium"},
                "nist_rs": {"name": "Respond", "cat": "reliability", "sev": "medium"},
                "nist_rc": {"name": "Recover", "cat": "reliability", "sev": "medium"},
            },
            "ISO27001": {
                "iso_04": {"name": "Information security policies", "cat": "compliance", "sev": "high"},
                "iso_05": {"name": "Organization of information security", "cat": "compliance", "sev": "medium"},
                "iso_06": {"name": "Human resource security", "cat": "compliance", "sev": "medium"},
                "iso_07": {"name": "Asset management", "cat": "compliance", "sev": "high"},
                "iso_08": {"name": "Access control", "cat": "security", "sev": "high"},
                "iso_09": {"name": "Cryptography", "cat": "security", "sev": "high"},
                "iso_12": {"name": "Operations security", "cat": "security", "sev": "medium"},
                "iso_14": {"name": "Business continuity", "cat": "reliability", "sev": "high"},
                "iso_16": {"name": "Incident management", "cat": "reliability", "sev": "high"},
            },
            "HIPAA": {
                "hipaa_ac": {"name": "Access control", "cat": "security", "sev": "critical"},
                "hipaa_at": {"name": "Audit controls", "cat": "observability", "sev": "high"},
                "hipaa_ia": {"name": "Integrity controls", "cat": "security", "sev": "high"},
                "hipaa_tr": {"name": "Transmission security", "cat": "security", "sev": "high"},
            },
            "CSA-CCM": {
                "cmm_ds": {"name": "Data security and information lifecycle management", "cat": "security", "sev": "high"},
                "cmm_ig": {"name": "Identity and access management", "cat": "security", "sev": "high"},
                "cmm_is": {"name": "Infrastructure and virtualization security", "cat": "security", "sev": "medium"},
                "cmm_rs": {"name": "Resilience and incident management", "cat": "reliability", "sev": "high"},
            },
        }

    def get_frameworks(self) -> List[str]:
        return list(self._frameworks.keys())

    def run_check(self, architecture: Dict, frameworks: Optional[List[str]] = None) -> Dict[str, Any]:
        frameworks = frameworks or list(self._frameworks.keys())
        results: Dict[str, List[Dict]] = {}
        all_checks = []
        passed = 0
        failed = 0
        for fw in frameworks:
            fw_checks = self._frameworks.get(fw, {})
            for check_id, check in fw_checks.items():
                result = self._evaluate_check(architecture, check_id, check)
                all_checks.append(result)
                results.setdefault(fw, []).append(result)
                if result["status"] == "passed":
                    passed += 1
                else:
                    failed += 1
        gaps = [c for c in all_checks if c["status"] != "passed"]
        remediation = [{"framework": c["framework"], "step": i + 1, "action": c["recommendation"], "severity": c["severity"]}
                       for i, c in enumerate(gaps[:20])]
        overall = round((passed / max(1, len(all_checks))) * 100, 2)
        return {
            "overall_score": overall,
            "frameworks_checked": frameworks,
            "total_checks": len(all_checks),
            "passed_checks": passed,
            "failed_checks": failed,
            "gaps": gaps,
            "remediation_plan": remediation,
        }

    def _evaluate_check(self, architecture: Dict, check_id: str, check: Dict) -> Dict[str, Any]:
        status, rationale = self._evaluate(architecture, check_id, check)
        return {
            "framework": check.get("framework", ""),
            "check_id": check_id,
            "name": check["name"],
            "category": check["cat"],
            "severity": check["sev"],
            "status": status,
            "rationale": rationale,
            "recommendation": check.get("recommendation", f"Address {check_id}"),
        }

    def _evaluate(self, arch: Dict, check_id: str, check: Dict) -> Tuple[str, str]:
        cat = check["cat"]
        if cat == "security":
            if check_id in ["A01"] and not arch.get("cryptography", {}).get("tls_enabled"):
                return "failed", "TLS not enabled"
            if check_id in ["A02"] and arch.get("authentication", {}).get("type") not in ["jwt", "oauth2", "oidc"]:
                return "failed", "Weak authentication"
            if check_id in ["A03"] and not arch.get("input_validation"):
                return "failed", "No input validation"
            if check_id in ["A05"] and arch.get("shared_database"):
                return "failed", "Misconfigured shared database"
            if check_id in ["A07"] and not arch.get("authorization", {}).get("least_privilege"):
                return "failed", "No least privilege"
            if check_id in ["A09"] and not arch.get("monitoring"):
                return "failed", "No security monitoring"
            return "passed", "Check passed"
        if cat == "compliance":
            if check_id in ["gdpr_06"] and not arch.get("cryptography", {}).get("encryption_at_rest"):
                return "failed", "Encryption at rest missing"
            if check_id in ["pci_03"] and not arch.get("data_protection", {}).get("pii_encryption"):
                return "failed", "PII encryption missing"
            return "passed", "Check passed"
        return "passed", "Check not applicable"


class MetricsCollector:
    def __init__(self) -> None:
        self._metrics: List[ArchitectureMetric] = []

    def record(self, metric: ArchitectureMetric) -> None:
        self._metrics.append(metric)
        logger.info(f"Metric recorded: {metric.name}={metric.value}{metric.unit} ({metric.status})")

    def get_by_name(self, name: str) -> Optional[ArchitectureMetric]:
        for m in self._metrics[::-1]:
            if m.name == name:
                return m
        return None

    def get_latest(self) -> List[ArchitectureMetric]:
        seen: Dict[str, Any] = {}
        for m in self._metrics[::-1]:
            seen.setdefault(m.name, m)
        return list(seen.values())

    def get_summary(self) -> Dict[str, Any]:
        latest = self.get_latest()
        return {
            m.name: {"value": m.value, "unit": m.unit, "status": m.status, "trend": m.trend}
            for m in latest
        }

    def clear(self) -> None:
        self._metrics.clear()


class ReportGenerator:
    def __init__(self, export_path: Optional[str] = None):
        self.export_path = export_path or "."

    def to_json(self, review: ReviewResult) -> str:
        data = {
            "review_id": review.review_id,
            "score": review.score,
            "summary": review.summary,
            "categories": review.categories,
            "patterns_detected": review.patterns_detected,
            "findings_count": len(review.findings),
            "technical_debt_count": len(review.technical_debt_items),
            "recommendations": review.recommendations,
            "generated_at": review.generated_at,
            "metadata": review.metadata,
        }
        return json.dumps(data, indent=2, default=str)

    def to_markdown(self, review: ReviewResult) -> str:
        md = f"# Architecture Review Report\n\n"
        md += f"**Review ID**: {review.review_id}\n"
        md += f"**Score**: {review.score}/100\n"
        md += f"**Date**: {review.generated_at}\n\n"
        md += f"## Summary\n\n{review.summary}\n\n"
        if review.patterns_detected:
            md += "## Detected Patterns\n\n"
            for p in review.patterns_detected:
                md += f"- {p}\n"
            md += "\n"
        if review.findings:
            md += "## Findings\n\n"
            for f in review.findings:
                md += f"- **{f.get('severity', '?').upper()}** {f.get('title', '')}: {f.get('description', '')}\n"
                if f.get("recommendation"):
                    md += f"  - *Recommendation*: {f['recommendation']}\n"
            md += "\n"
        md += "## Recommendations\n\n"
        for r in review.recommendations:
            md += f"- {r}\n"
        if review.technical_debt_items:
            md += "\n## Technical Debt\n\n"
            for d in review.technical_debt_items:
                md += f"- **{d.get('priority', '?').upper()}** [{d.get('area', 'general')}] {d.get('description', '')}\n"
        if review.compliance_results:
            md += "\n## Compliance\n\n"
            cr = review.compliance_results
            md += f"- Overall compliance score: {cr.get('overall_score', 0)}%\n"
            md += f"- Passed: {cr.get('passed_checks', 0)}/{cr.get('total_checks', 0)}\n"
            if cr.get("gaps"):
                md += "\n### Gaps\n\n"
                for g in cr["gaps"]:
                    md += f"- [{g['framework']}] {g['name']} ({g.get('severity', '?')})\n"
        return md

    def to_csv(self, review: ReviewResult) -> str:
        if not review.findings:
            return "title,severity,category,effort,impact,auto_fixable,recommendation\n"
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["title", "severity", "category", "effort", "impact", "auto_fixable", "recommendation"])
        writer.writeheader()
        for f in review.findings:
            writer.writerow({
                "title": f.get("title", ""),
                "severity": f.get("severity", ""),
                "category": f.get("category", ""),
                "effort": f.get("effort", "medium"),
                "impact": f.get("impact", "medium"),
                "auto_fixable": f.get("auto_fixable", False),
                "recommendation": f.get("recommendation", ""),
            })
        return output.getvalue()


class ArchitectureReviewAgent:
    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._reviews: List[ReviewResult] = []
        self._findings: List[Finding] = []
        self._storage: Dict[str, ReviewResult] = {}
        self._metrics_collector = MetricsCollector()
        self._pattern_detector = PatternDetector()
        self._scalability_analyzer = ScalabilityAnalyzer()
        self._security_analyzer = SecurityAnalyzer()
        self._performance_analyzer = PerformanceAnalyzer()
        self._tech_debt_analyzer = TechDebtAnalyzer()
        self._compliance_checker = ComplianceChecker()
        self._report_generator = ReportGenerator(self._config.export_path)
        self._lock = threading.Lock()

    def _log(self, msg: str, level: int = logging.INFO) -> None:
        logger.log(level, f"[{self._config.reviewer}] {msg}")

    def review_architecture(self, design_document: str, architecture: Optional[Dict] = None) -> ReviewResult:
        start = time.time()
        with self._lock:
            a = architecture or {}
            review_id = f"rev-{len(self._reviews) + 1}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            review = self._full_review(a, design_document)
            review.review_id = review_id
            review.generated_at = datetime.now().isoformat()
            review.metadata = {"review_type": self._config.review_type, "reviewer": self._config.reviewer,
                               "benchmark_version": self._config.benchmark_version}
            review.architecture_snapshot = json.loads(json.dumps(a, default=str))
            if self._config.include_compliance:
                review.compliance_results = self._compliance_checker.run_check(a)
            dept = self._tech_debt_analyzer.identify_tech_debt(design_document, a)
            review.technical_debt_items = dept
            if self._config.generate_report:
                review.metrics["report_preview"] = {
                    "json_preview": review.summary[:100],
                    "markdown_available": True,
                    "csv_available": True,
                }
            self._reviews.append(review)
            self._storage[review_id] = review
            latency = time.time() - start
            metric = ArchitectureMetric(name="review_duration_seconds", value=round(latency, 3), unit="s",
                                        threshold=1.0, status="healthy" if latency < 1.0 else "warning",
                                        description="Total review wall-clock time")
            self._metrics_collector.record(metric)
            self._log(f"Review {review_id} completed in {latency:.3f}s score={review.score}")
            return review

    def _full_review(self, a: Dict, doc: str) -> ReviewResult:
        cats: Dict[str, Any] = {}
        if self._config.include_security:
            s = self._security_analyzer.assess_security(a)
            cats["security"] = s
            self._metrics_collector.record(ArchitectureMetric(name="security_score", value=s["score"], unit="pts",
                                                              threshold=self._config.score_threshold_pass,
                                                              status="healthy" if s["score"] >= self._config.score_threshold_pass else "warning"))
        if self._config.include_performance:
            p = self._performance_analyzer.analyze_performance(a)
            cats["performance"] = p
            self._metrics_collector.record(ArchitectureMetric(name="performance_score", value=p["score"], unit="pts",
                                                              threshold=self._config.score_threshold_pass,
                                                              status="healthy" if p["score"] >= self._config.score_threshold_pass else "warning"))
        if self._config.include_scalability:
            sc = self._scalability_analyzer.assess_scalability(a)
            cats["scalability"] = sc
            self._metrics_collector.record(ArchitectureMetric(name="scalability_score", value=sc["score"], unit="pts",
                                                              threshold=self._config.score_threshold_pass,
                                                              status="healthy" if sc["score"] >= self._config.score_threshold_pass else "warning"))
        if self._config.include_maintainability:
            debt = self._tech_debt_analyzer.identify_tech_debt(doc, a)
            est = self._tech_debt_analyzer.estimate_tech_debt(debt)
            maint_score = max(0, 100 - est["total_hours"] * 0.5)
            cats["maintainability"] = {"score": maint_score, "technical_debt": debt, "estimates": est}
            self._metrics_collector.record(ArchitectureMetric(name="maintainability_score", value=maint_score, unit="pts",
                                                              threshold=self._config.score_threshold_pass,
                                                              status="healthy" if maint_score >= self._config.score_threshold_pass else "warning"))
        findings: List[Dict] = []
        for cat_name, data in cats.items():
            if isinstance(data, dict):
                findings.extend(data.get("vulnerabilities", []))
                if "bottlenecks" in data:
                    for b in data["bottlenecks"]:
                        findings.append({"title": b["component"], "category": "scalability", "severity": b["severity"],
                                         "description": b["description"],
                                         "recommendation": "Address bottleneck to improve throughput."})
        overall = round(sum(c.get("score", 70) for c in cats.values()) / max(1, len(cats)), 2)
        summary = f"Review complete. Score: {overall}/100. Categories: {len(cats)}. Findings: {len(findings)}."
        return ReviewResult(score=overall, findings=findings,
                            recommendations=[r for data in cats.values() for r in data.get("recommendations", [])],
                            summary=summary, categories={k: v.get("score", 0) for k, v in cats.items()},
                            patterns_detected=self._pattern_detector.detect_patterns(doc))

    def identify_patterns(self, arch: Dict) -> List[str]:
        return self._pattern_detector.detect_patterns(str(arch))

    def assess_scalability(self, arch: Dict) -> Dict[str, Any]:
        return self._scalability_analyzer.assess_scalability(arch)

    def identify_tech_debt(self, codebase: str) -> List[Dict]:
        return self._tech_debt_analyzer.identify_tech_debt(codebase, {})

    def run_compliance_check(self, architecture: Dict, frameworks: Optional[List[str]] = None) -> Dict[str, Any]:
        return self._compliance_checker.run_check(architecture, frameworks)

    def get_status(self) -> Dict[str, Any]:
        latest = self._reviews[-1] if self._reviews else None
        return {
            "agent": "ArchitectureReviewAgent",
            "reviews": len(self._reviews),
            "latest_score": latest.score if latest else None,
            "latest_review_id": latest.review_id if latest else None,
            "config": {"review_type": self._config.review_type, "include_security": self._config.include_security},
        }

    def get_review_history(self, limit: int = 10) -> List[Dict]:
        return [{"review_id": r.review_id, "score": r.score, "summary": r.summary,
                 "generated_at": r.generated_at, "findings": len(r.findings)} for r in self._reviews[-limit:]]

    def compare_architectures(self, a1: Dict, a2: Dict) -> Dict[str, Any]:
        r1 = self._full_review(a1, str(a1))
        r2 = self._full_review(a2, str(a2))
        comp = self._pattern_detector.compare_patterns(a1, a2)
        return {
            "architecture_a_score": r1.score,
            "architecture_b_score": r2.score,
            "difference": round(r1.score - r2.score, 2),
            "patterns_common": comp["common"],
            "patterns_only_a": comp["unique_to_a"],
            "patterns_only_b": comp["unique_to_b"],
            "jaccard_similarity": comp["jaccard_index"],
        }

    def batch_review(self, documents: List[Tuple[str, Dict]]) -> List[ReviewResult]:
        results: List[ReviewResult] = []
        for design_doc, arch in documents:
            results.append(self.review_architecture(design_doc, arch))
        return results

    def export_report(self, review_id: str, fmt: str = "json") -> Dict[str, Any]:
        r = self._storage.get(review_id)
        if not r:
            return {"status": "error", "message": "Review not found"}
        if fmt == "json":
            payload = json.loads(self._report_generator.to_json(r))
            return {"review_id": review_id, "status": "exported", "format": "json", "report": payload}
        elif fmt == "markdown":
            md = self._report_generator.to_markdown(r)
            return {"review_id": review_id, "status": "exported", "format": "markdown", "report": {"content": md}}
        elif fmt == "csv":
            csv_text = self._report_generator.to_csv(r)
            return {"review_id": review_id, "status": "exported", "format": "csv", "report": {"content": csv_text}}
        return {"status": "error", "message": f"Unsupported format: {fmt}"}

    def export_state(self) -> str:
        with self._lock:
            state = {
                "config": {
                    "review_type": self._config.review_type,
                    "include_security": self._config.include_security,
                    "include_performance": self._config.include_performance,
                    "include_scalability": self._config.include_scalability,
                    "score_threshold_pass": self._config.score_threshold_pass,
                    "score_threshold_warning": self._config.score_threshold_warning,
                    "max_findings": self._config.max_findings,
                    "benchmark_version": self._config.benchmark_version,
                },
                "reviews_count": len(self._reviews),
                "review_ids": [r.review_id for r in self._reviews],
                "latest_score": self._reviews[-1].score if self._reviews else None,
            }
            return json.dumps(state, indent=2, default=str)

    def import_state(self, state_json: str) -> Dict[str, Any]:
        with self._lock:
            state = json.loads(state_json)
            self._config.review_type = state.get("config", {}).get("review_type", self._config.review_type)
            self._log(f"Imported state for {state.get('reviews_count', 0)} prior reviews")
            return {"status": "imported", "state_keys": list(state.keys())}

    def get_metrics_summary(self) -> Dict[str, Any]:
        return {
            "metrics": self._metrics_collector.get_summary(),
            "total_reviews": len(self._reviews),
            "total_findings": sum(len(r.findings) for r in self._reviews),
            "avg_score": round(sum(r.score for r in self._reviews) / max(1, len(self._reviews)), 2),
        }


def main():
    print("Architecture Review Agent Demo")
    agent = ArchitectureReviewAgent()
    architecture = {
        "patterns": ["microservices", "layered"],
        "authentication": {"type": "jwt", "mfa": True, "rbac": True},
        "load_balancer": True,
        "api_gateway": True,
        "database": {"type": "postgresql", "replication": True, "sharding": False},
        "caching": True,
        "monitoring": True,
        "cryptography": {"tls_enabled": True, "tls_version": "1.3", "encryption_at_rest": True, "key_management": "aws-kms"},
        "network_security": {"waf": True, "ddos_protection": True, "vpc": True, "zero_trust": False},
        "test_coverage": {"unit": True},
        "documentation": True,
        "containerized": True,
        "orchestration": "kubernetes",
        "stateless_services": True,
    }
    result = agent.review_architecture(design_document="microservices arch review", architecture=architecture)
    status = agent.get_status()
    print(status)
    print(f"Score: {result.score}")
    print(f"Findings: {len(result.findings)}")
    print(f"Patterns: {result.patterns_detected}")
    export = agent.export_report(review_id=result.review_id, fmt="markdown")
    print(f"Export status: {export['status']}")


if __name__ == "__main__":
    main()
