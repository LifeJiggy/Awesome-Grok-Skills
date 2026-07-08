#!/usr/bin/env python3
"""
DevOps Agent - Enterprise-Grade Infrastructure Automation and Operations.

Comprehensive DevOps capabilities including infrastructure automation,
container orchestration, monitoring, incident management, SRE practices,
GitOps workflows, secret management, and configuration management.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import json
import hashlib
import logging
import secrets
import time
import threading
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("devops-agent")


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class Environment(Enum):
    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"
    DR = "dr"
    CANARY = "canary"


class PipelineStage(Enum):
    CHECKOUT = "checkout"
    BUILD = "build"
    TEST = "test"
    SECURITY_SCAN = "security_scan"
    DEPLOY = "deploy"
    VERIFY = "verify"
    NOTIFY = "notify"
    ROLLBACK = "rollback"


class DeploymentStrategy(Enum):
    ROLLING = "rolling"
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    RECREATE = "recreate"
    A_B = "a_b"


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class IncidentStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"
    POSTMORTEM = "postmortem"


class CloudProvider(Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    DIGITALOCEAN = "digitalocean"


class InfraProvider(Enum):
    TERRAFORM = "terraform"
    ANSIBLE = "ansible"
    CLOUDFORMATION = "cloudformation"
    PULUMI = "pulumi"


class SecretEngine(Enum):
    VAULT = "vault"
    SEALED_SECRETS = "sealed_secrets"
    AWS_SECRETS_MANAGER = "aws_secrets_manager"
    GCP_SECRET_MANAGER = "gcp_secret_manager"
    AZURE_KEY_VAULT = "azure_key_vault"


# ──────────────────────────────────────────────
# Dataclasses
# ──────────────────────────────────────────────

@dataclass
class PipelineConfig:
    name: str
    stages: List[Dict[str, Any]]
    triggers: Dict[str, Any] = field(default_factory=dict)
    environment: Environment = Environment.DEVELOPMENT
    timeout_minutes: int = 60
    retry_count: int = 1
    approval_required: bool = False

    def validate(self) -> bool:
        if not self.name:
            raise ValueError("Pipeline name is required")
        if not self.stages:
            raise ValueError("At least one stage is required")
        for stage in self.stages:
            if "name" not in stage:
                raise ValueError("Each stage must have a name")
        return True


@dataclass
class DeploymentConfig:
    service_name: str
    version: str
    environment: Environment
    strategy: DeploymentStrategy
    replica_count: int = 3
    resources: Dict[str, Any] = field(default_factory=dict)
    health_checks: Dict[str, Any] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)
    namespace: str = "default"
    node_selector: Dict[str, str] = field(default_factory=dict)

    def to_k8s_labels(self) -> Dict[str, str]:
        return {"app": self.service_name, "version": self.version, "environment": self.environment.value, "managed-by": "devops-agent"}


@dataclass
class KubernetesManifest:
    api_version: str
    kind: str
    metadata: Dict[str, Any]
    spec: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"apiVersion": self.api_version, "kind": self.kind, "metadata": self.metadata, "spec": self.spec}


@dataclass
class SLIDefinition:
    name: str
    description: str
    metric_query: str
    good_event: str
    total_event: str
    window_minutes: int = 60


@dataclass
class SLODefinition:
    name: str
    target_percentage: float
    window_days: int = 30
    sli: Optional[SLIDefinition] = None
    error_budget_remaining: float = 100.0


@dataclass
class Incident:
    id: str
    title: str
    severity: Severity
    status: IncidentStatus
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[str] = None
    description: str = ""
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    affected_services: List[str] = field(default_factory=list)


@dataclass
class GitOpsApplication:
    name: str
    repo_url: str
    target_revision: str
    target_namespace: str
    sync_policy: str = "auto"
    auto_prune: bool = True
    self_heal: bool = True


@dataclass
class SecretEntry:
    name: str
    engine: SecretEngine
    path: str
    data: Dict[str, str] = field(default_factory=dict)
    ttl_seconds: int = 3600
    rotation_enabled: bool = False
    rotation_interval_days: int = 90


@dataclass
class ConfigItem:
    key: str
    value: Any
    namespace: str = "default"
    encrypted: bool = False
    version: int = 1
    last_modified: datetime = field(default_factory=datetime.utcnow)
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class SLOStatus:
    slo_name: str
    current_value: float
    target_value: float
    error_budget_total: float
    error_budget_remaining: float
    status: str
    burn_rate: float
    breach_forecast_hours: Optional[float]


# ──────────────────────────────────────────────
# Infrastructure Automation
# ──────────────────────────────────────────────

class InfrastructureAutomation:
    """Manages infrastructure-as-code workflows across cloud providers."""

    def __init__(self, default_provider: CloudProvider = CloudProvider.AWS):
        self.default_provider = default_provider
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.state_store: Dict[str, Dict[str, Any]] = {}
        self.providers: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        logger.info("InfrastructureAutomation initialized with provider=%s", default_provider.value)

    def register_provider(self, name: str, credentials: Dict[str, str], provider_type: InfraProvider) -> Dict[str, Any]:
        with self._lock:
            pid = hashlib.sha256(name.encode()).hexdigest()[:12]
            self.providers[name] = {"id": pid, "type": provider_type.value, "credentials_hash": hashlib.sha256(json.dumps(credentials).encode()).hexdigest(), "status": "active", "registered_at": datetime.utcnow().isoformat()}
            logger.info("Provider registered: %s (%s)", name, provider_type.value)
            return {"provider_id": pid, "status": "registered"}

    def plan_infrastructure(self, provider_name: str, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not found")
        plan_id = f"plan_{int(time.time())}_{hashlib.md5(str(resources).encode()).hexdigest()[:8]}"
        changes = [{"resource_type": r.get("type", "unknown"), "resource_name": r.get("name", "unnamed"), "action": r.get("action", "create"), "will_change": True} for r in resources]
        plan = {"plan_id": plan_id, "provider": provider_name, "resource_count": len(resources), "changes": changes, "estimated_cost": self._estimate_cost(changes), "created_at": datetime.utcnow().isoformat(), "status": "planned"}
        with self._lock:
            self.state_store[plan_id] = plan
        logger.info("Infrastructure plan created: %s with %d resources", plan_id, len(resources))
        return plan

    def apply_infrastructure(self, plan_id: str) -> Dict[str, Any]:
        if plan_id not in self.state_store:
            raise ValueError(f"Plan {plan_id} not found")
        plan = self.state_store[plan_id]
        if plan["status"] != "planned":
            raise ValueError(f"Plan {plan_id} is not in 'planned' state")
        results = [{"resource": c["resource_name"], "type": c["resource_type"], "action": c["action"], "status": "applied", "applied_at": datetime.utcnow().isoformat()} for c in plan["changes"]]
        plan["status"] = "applied"
        plan["results"] = results
        self.resources[plan_id] = results
        logger.info("Infrastructure plan applied: %s", plan_id)
        return {"plan_id": plan_id, "status": "applied", "resources_applied": len(results)}

    def destroy_infrastructure(self, plan_id: str, force: bool = False) -> Dict[str, Any]:
        if plan_id not in self.resources:
            raise ValueError(f"No applied resources found for plan {plan_id}")
        if not force:
            return {"plan_id": plan_id, "status": "requires_confirmation"}
        resources = self.resources.pop(plan_id)
        destroyed = [{"resource": r["resource"], "type": r["type"], "action": "destroy", "status": "destroyed"} for r in resources]
        self.state_store[plan_id]["status"] = "destroyed"
        logger.info("Infrastructure destroyed for plan %s", plan_id)
        return {"plan_id": plan_id, "status": "destroyed", "resources_destroyed": len(destroyed)}

    def generate_terraform_module(self, name: str, resources: List[Dict[str, Any]], provider: CloudProvider) -> str:
        lines = [f"# Auto-generated Terraform module: {name}", f"# Provider: {provider.value}", "", f'resource "{provider.value}_resource" "{name}" {{']
        for resource in resources:
            for key, value in resource.items():
                if isinstance(value, str):
                    lines.append(f'  {key} = "{value}"')
                elif isinstance(value, (int, float, bool)):
                    lines.append(f'  {key} = {value}')
        lines.extend(["}", "", f'output "{name}_id" {{', f'  value = {provider.value}_resource.{name}.id', "}"])
        return "\n".join(lines)

    def generate_ansible_playbook(self, name: str, hosts: str, tasks: List[Dict[str, Any]]) -> str:
        playbook = {"name": name, "hosts": hosts, "become": True, "tasks": []}
        for task in tasks:
            entry = {"name": task.get("name", "unnamed task")}
            for key in ("shell", "template", "copy"):
                if key in task:
                    entry[key] = task[key]
                    break
            if "package" in task:
                entry["apt"] = {"name": task["package"], "state": task.get("state", "present")}
            playbook["tasks"].append(entry)
        return json.dumps([playbook], indent=2)

    def _estimate_cost(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        cost_map = {"ec2_instance": 0.0116, "rds_instance": 0.017, "s3_bucket": 0.023, "load_balancer": 0.0225, "nat_gateway": 0.045}
        total = sum(cost_map.get(c.get("resource_type", "unknown"), 0.005) for c in changes)
        per_resource = [{"resource": c["resource_name"], "hourly_usd": cost_map.get(c.get("resource_type", "unknown"), 0.005)} for c in changes]
        return {"hourly_usd": round(total, 4), "monthly_usd": round(total * 730, 2), "per_resource": per_resource}

    def get_state(self, plan_id: Optional[str] = None) -> Dict[str, Any]:
        if plan_id:
            return self.state_store.get(plan_id, {"error": "Plan not found"})
        return {"total_plans": len(self.state_store), "total_resources": len(self.resources)}


# ──────────────────────────────────────────────
# Container Orchestration
# ──────────────────────────────────────────────

class ContainerOrchestration:
    """Kubernetes and Docker orchestration management."""

    def __init__(self):
        self.clusters: Dict[str, Dict[str, Any]] = {}
        self.deployments: Dict[str, Dict[str, Any]] = {}
        self.services: Dict[str, Dict[str, Any]] = {}
        self.ingresses: Dict[str, Dict[str, Any]] = {}
        self.hpas: Dict[str, Dict[str, Any]] = {}
        self.helm_releases: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        logger.info("ContainerOrchestration initialized")

    def register_cluster(self, name: str, kubeconfig_path: str, context: str = "default", provider: str = "eks") -> Dict[str, Any]:
        cid = hashlib.sha256(name.encode()).hexdigest()[:12]
        with self._lock:
            self.clusters[name] = {"id": cid, "name": name, "kubeconfig": kubeconfig_path, "context": context, "provider": provider, "connected": True, "version": "1.28.4", "nodes": 0, "registered_at": datetime.utcnow().isoformat()}
        logger.info("Cluster registered: %s (%s)", name, provider)
        return {"cluster_id": cid, "status": "registered"}

    def create_namespace(self, name: str, cluster: str, labels: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if cluster not in self.clusters:
            raise ValueError(f"Cluster {cluster} not found")
        ns = {"name": name, "cluster": cluster, "labels": labels or {"managed-by": "devops-agent"}, "status": "active", "created_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.services[f"{cluster}/{name}/_ns"] = ns
        logger.info("Namespace created: %s in cluster %s", name, cluster)
        return ns

    def create_deployment(self, config: DeploymentConfig, cluster: str = "default") -> Dict[str, Any]:
        did = f"deploy_{config.service_name}_{int(time.time())}"
        manifest = self._generate_deployment_manifest(config)
        with self._lock:
            self.deployments[did] = {"id": did, "service": config.service_name, "version": config.version, "cluster": cluster, "replicas": config.replica_count, "manifest": manifest, "status": "creating", "created_at": datetime.utcnow().isoformat(), "strategy": config.strategy.value}
        logger.info("Deployment created: %s -> %s", config.service_name, config.version)
        return {"deployment_id": did, "manifest": manifest, "strategy": config.strategy.value}

    def _generate_deployment_manifest(self, config: DeploymentConfig) -> Dict[str, Any]:
        if config.strategy == DeploymentStrategy.ROLLING:
            strategy_spec = {"type": "RollingUpdate", "rollingUpdate": {"maxSurge": "25%", "maxUnavailable": "0"}}
        else:
            strategy_spec = {"type": "Recreate"}
        resources = config.resources or {"requests": {"cpu": "200m", "memory": "256Mi"}, "limits": {"cpu": "500m", "memory": "512Mi"}}
        env_vars = [{"name": k, "value": str(v)} for k, v in config.environment_variables.items()]
        for secret_name in config.secrets:
            env_vars.append({"name": secret_name.upper(), "valueFrom": {"secretKeyRef": {"name": f"{config.service_name}-secrets", "key": secret_name.lower()}}})
        container = {"name": config.service_name, "image": f"{config.service_name}:{config.version}", "ports": [{"containerPort": 8080}], "env": env_vars, "resources": resources, "livenessProbe": config.health_checks.get("liveness", {"httpGet": {"path": "/health", "port": 8080}, "initialDelaySeconds": 30, "periodSeconds": 10}), "readinessProbe": config.health_checks.get("readiness", {"httpGet": {"path": "/ready", "port": 8080}, "initialDelaySeconds": 5, "periodSeconds": 5})}
        template_spec: Dict[str, Any] = {"containers": [container]}
        if config.node_selector:
            template_spec["nodeSelector"] = config.node_selector
        return {"apiVersion": "apps/v1", "kind": "Deployment", "metadata": {"name": config.service_name, "namespace": config.namespace, "labels": config.to_k8s_labels()}, "spec": {"replicas": config.replica_count, "strategy": strategy_spec, "selector": {"matchLabels": {"app": config.service_name}}, "template": {"metadata": {"labels": config.to_k8s_labels()}, "spec": template_spec}}}

    def create_service(self, name: str, selector: Dict[str, str], port: int = 80, target_port: int = 8080, service_type: str = "ClusterIP", namespace: str = "default") -> Dict[str, Any]:
        svc = {"apiVersion": "v1", "kind": "Service", "metadata": {"name": name, "namespace": namespace}, "spec": {"type": service_type, "selector": selector, "ports": [{"protocol": "TCP", "port": port, "targetPort": target_port}]}}
        with self._lock:
            self.services[f"{namespace}/{name}"] = svc
        logger.info("Service created: %s (type=%s)", name, service_type)
        return svc

    def create_ingress(self, name: str, host: str, path: str, service_name: str, service_port: int = 80, namespace: str = "default", tls_secret: Optional[str] = None, annotations: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        annotations = annotations or {"nginx.ingress.kubernetes.io/ssl-redirect": "true"}
        spec: Dict[str, Any] = {"ingressClassName": "nginx", "rules": [{"host": host, "http": {"paths": [{"path": path, "pathType": "Prefix", "backend": {"service": {"name": service_name, "port": {"number": service_port}}}}]}}]}
        if tls_secret:
            annotations["cert-manager.io/cluster-issuer"] = "letsencrypt-prod"
            spec["tls"] = [{"hosts": [host], "secretName": tls_secret}]
        ingress = {"apiVersion": "networking.k8s.io/v1", "kind": "Ingress", "metadata": {"name": name, "namespace": namespace, "annotations": annotations}, "spec": spec}
        with self._lock:
            self.ingresses[f"{namespace}/{name}"] = ingress
        logger.info("Ingress created: %s -> %s", name, host)
        return ingress

    def create_hpa(self, name: str, deployment_name: str, min_replicas: int = 2, max_replicas: int = 10, cpu_target: int = 70, memory_target: int = 80, namespace: str = "default") -> Dict[str, Any]:
        hpa = {"apiVersion": "autoscaling/v2", "kind": "HorizontalPodAutoscaler", "metadata": {"name": name, "namespace": namespace}, "spec": {"scaleTargetRef": {"apiVersion": "apps/v1", "kind": "Deployment", "name": deployment_name}, "minReplicas": min_replicas, "maxReplicas": max_replicas, "metrics": [{"type": "Resource", "resource": {"name": "cpu", "target": {"type": "Utilization", "averageUtilization": cpu_target}}}, {"type": "Resource", "resource": {"name": "memory", "target": {"type": "Utilization", "averageUtilization": memory_target}}}]}}
        with self._lock:
            self.hpas[f"{namespace}/{name}"] = hpa
        logger.info("HPA created: %s (min=%d, max=%d)", name, min_replicas, max_replicas)
        return hpa

    def scale_deployment(self, deployment_id: str, replicas: int) -> Dict[str, Any]:
        if deployment_id not in self.deployments:
            raise ValueError(f"Deployment {deployment_id} not found")
        old = self.deployments[deployment_id]["replicas"]
        self.deployments[deployment_id]["replicas"] = replicas
        self.deployments[deployment_id]["scaled_at"] = datetime.utcnow().isoformat()
        logger.info("Deployment %s scaled: %d -> %d", deployment_id, old, replicas)
        return {"deployment_id": deployment_id, "old_replicas": old, "new_replicas": replicas, "status": "scaled"}

    def rollback_deployment(self, deployment_id: str, target_version: Optional[str] = None) -> Dict[str, Any]:
        if deployment_id not in self.deployments:
            raise ValueError(f"Deployment {deployment_id} not found")
        dep = self.deployments[deployment_id]
        prev = dep["version"]
        dep["version"] = target_version or f"{dep['service']}:previous"
        dep["status"] = "rolled_back"
        dep["rolled_back_at"] = datetime.utcnow().isoformat()
        logger.info("Deployment %s rolled back: %s -> %s", deployment_id, prev, dep["version"])
        return {"deployment_id": deployment_id, "from": prev, "to": dep["version"], "status": "rolled_back"}

    def apply_helm_chart(self, release_name: str, chart: str, namespace: str = "default", values: Optional[Dict[str, Any]] = None, version: Optional[str] = None) -> Dict[str, Any]:
        release = {"name": release_name, "chart": chart, "namespace": namespace, "version": version or "latest", "values": values or {}, "status": "deployed", "deployed_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.helm_releases[release_name] = release
        logger.info("Helm release deployed: %s (chart=%s)", release_name, chart)
        return release

    def get_cluster_resources(self, cluster: str) -> Dict[str, Any]:
        if cluster not in self.clusters:
            raise ValueError(f"Cluster {cluster} not found")
        deps = [d for d in self.deployments.values() if d.get("cluster") == cluster]
        total_replicas = sum(d.get("replicas", 0) for d in deps)
        return {"cluster": cluster, "deployments": len(deps), "total_replicas": total_replicas, "services": len(self.services), "ingresses": len(self.ingresses), "hpas": len(self.hpas)}


# ──────────────────────────────────────────────
# Monitoring Manager
# ──────────────────────────────────────────────

class MonitoringManager:
    """Monitoring, alerting, and observability management."""

    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.thresholds: Dict[str, Dict[str, Any]] = {}
        self.dashboards: Dict[str, Dict[str, Any]] = {}
        self.synthetic_tests: List[Dict[str, Any]] = []
        self.slo_metrics: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._lock = threading.Lock()
        logger.info("MonitoringManager initialized")

    def set_threshold(self, metric: str, warning: float, critical: float, operator: str = "gt", unit: str = "") -> Dict[str, Any]:
        self.thresholds[metric] = {"warning": warning, "critical": critical, "operator": operator, "unit": unit, "created_at": datetime.utcnow().isoformat()}
        logger.info("Threshold set for %s: warning=%.1f, critical=%.1f", metric, warning, critical)
        return {"metric": metric, "warning": warning, "critical": critical, "operator": operator}

    def collect_metrics(self, source: str, metrics: Dict[str, float], timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        ts = timestamp or datetime.utcnow()
        entry = {"timestamp": ts.isoformat(), "values": metrics, "source": source}
        with self._lock:
            self.metrics[source] = entry
        new_alerts = self._evaluate_alerts(metrics, source)
        return {"source": source, "metrics_count": len(metrics), "new_alerts": len(new_alerts)}

    def _evaluate_alerts(self, metrics: Dict[str, float], source: str) -> List[Dict[str, Any]]:
        triggered = []
        for metric_name, value in metrics.items():
            if metric_name not in self.thresholds:
                continue
            th = self.thresholds[metric_name]
            op = th["operator"]
            crit_met = (value > th["critical"]) if op == "gt" else (value < th["critical"])
            warn_met = (value > th["warning"]) if op == "gt" else (value < th["warning"])
            if crit_met:
                alert = {"metric": metric_name, "value": value, "severity": Severity.CRITICAL.value, "message": f"{metric_name} critically high: {value}", "source": source, "timestamp": datetime.utcnow().isoformat()}
                triggered.append(alert)
                with self._lock:
                    self.alerts.append(alert)
            elif warn_met:
                alert = {"metric": metric_name, "value": value, "severity": Severity.WARNING.value, "message": f"{metric_name} elevated: {value}", "source": source, "timestamp": datetime.utcnow().isoformat()}
                triggered.append(alert)
                with self._lock:
                    self.alerts.append(alert)
        return triggered

    def create_dashboard(self, name: str, panels: List[Dict[str, Any]], refresh_interval_seconds: int = 30) -> Dict[str, Any]:
        dashboard = {"name": name, "panels": panels, "refresh_interval": refresh_interval_seconds, "created_at": datetime.utcnow().isoformat(), "panel_count": len(panels)}
        with self._lock:
            self.dashboards[name] = dashboard
        logger.info("Dashboard created: %s (%d panels)", name, len(panels))
        return dashboard

    def run_synthetic_test(self, name: str, url: str, method: str = "GET", expectations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        result = {"test": name, "url": url, "method": method, "timestamp": datetime.utcnow().isoformat(), "passed": True, "response_time_ms": 145, "status_code": 200}
        if expectations:
            for key, expected in expectations.items():
                if key == "status_code" and result.get("status_code") != expected:
                    result["passed"] = False
                    result["error"] = f"Expected status {expected}, got {result['status_code']}"
                elif key == "max_response_ms" and result.get("response_time_ms", 0) > expected:
                    result["passed"] = False
                    result["error"] = f"Response time {result['response_time_ms']}ms exceeds max {expected}ms"
        with self._lock:
            self.synthetic_tests.append(result)
        return result

    def record_slo_measurement(self, slo_name: str, good_events: int, total_events: int) -> Dict[str, Any]:
        pct = (good_events / total_events * 100) if total_events > 0 else 100.0
        measurement = {"slo_name": slo_name, "good_events": good_events, "total_events": total_events, "percentage": round(pct, 4), "timestamp": datetime.utcnow().isoformat()}
        with self._lock:
            self.slo_metrics[slo_name].append(measurement)
        return measurement

    def analyze_error_patterns(self, logs: List[Dict[str, Any]], time_range_hours: int = 24) -> Dict[str, Any]:
        error_counts: Dict[str, int] = defaultdict(int)
        error_services: Dict[str, int] = defaultdict(int)
        for log_entry in logs:
            if log_entry.get("level") in ("ERROR", "CRITICAL"):
                error_counts[log_entry.get("error_type", "UnknownError")] += 1
                error_services[log_entry.get("service", "unknown")] += 1
        total = sum(error_counts.values())
        top = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        return {"time_range_hours": time_range_hours, "total_errors": total, "unique_error_types": len(error_counts), "top_errors": [{"type": et, "count": c} for et, c in top], "errors_by_service": dict(error_services), "error_rate": round(total / max(len(logs), 1) * 100, 2)}

    def generate_health_report(self) -> Dict[str, Any]:
        critical = [a for a in self.alerts if a["severity"] == Severity.CRITICAL.value]
        warnings = [a for a in self.alerts if a["severity"] == Severity.WARNING.value]
        passed = len([t for t in self.synthetic_tests if t["passed"]])
        total = len(self.synthetic_tests)
        return {"timestamp": datetime.utcnow().isoformat(), "overall_status": "healthy" if not critical else "degraded", "metrics_sources": len(self.metrics), "active_alerts": {"critical": len(critical), "warning": len(warnings), "total": len(self.alerts)}, "synthetic_tests": {"total": total, "passed": passed, "failed": total - passed}, "dashboards": len(self.dashboards), "slo_trackers": len(self.slo_metrics)}

    def create_alert_rule(self, name: str, query: str, duration: str = "5m", severity: Severity = Severity.WARNING) -> Dict[str, Any]:
        rule = {"name": name, "query": query, "duration": duration, "severity": severity.value, "status": "active", "created_at": datetime.utcnow().isoformat()}
        logger.info("Alert rule created: %s (severity=%s)", name, severity.value)
        return rule


# ──────────────────────────────────────────────
# Incident Manager
# ──────────────────────────────────────────────

class IncidentManager:
    """Incident detection, response, and postmortem management."""

    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.oncall_schedule: List[Dict[str, Any]] = []
        self.runbooks: Dict[str, Dict[str, Any]] = {}
        self.postmortems: List[Dict[str, Any]] = []
        self.escalation_policies: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        logger.info("IncidentManager initialized")

    def create_incident(self, title: str, severity: Severity, description: str = "", assigned_to: Optional[str] = None, affected_services: Optional[List[str]] = None) -> Incident:
        iid = f"INC-{int(time.time()) % 100000:05d}"
        now = datetime.utcnow()
        incident = Incident(id=iid, title=title, severity=severity, status=IncidentStatus.OPEN, created_at=now, updated_at=now, assigned_to=assigned_to, description=description, timeline=[{"event": "incident_created", "timestamp": now.isoformat(), "actor": assigned_to or "system"}], affected_services=affected_services or [])
        with self._lock:
            self.incidents[iid] = incident
        logger.warning("Incident created: %s [%s] %s", iid, severity.value, title)
        return incident

    def update_incident(self, incident_id: str, status: Optional[IncidentStatus] = None, assigned_to: Optional[str] = None, note: Optional[str] = None) -> Incident:
        if incident_id not in self.incidents:
            raise ValueError(f"Incident {incident_id} not found")
        inc = self.incidents[incident_id]
        now = datetime.utcnow()
        if status:
            inc.status = status
            inc.timeline.append({"event": f"status_changed_to_{status.value}", "timestamp": now.isoformat()})
        if assigned_to:
            inc.assigned_to = assigned_to
            inc.timeline.append({"event": "assigned", "assigned_to": assigned_to, "timestamp": now.isoformat()})
        if note:
            inc.timeline.append({"event": "note_added", "note": note, "timestamp": now.isoformat()})
        inc.updated_at = now
        logger.info("Incident updated: %s -> %s", incident_id, inc.status.value)
        return inc

    def resolve_incident(self, incident_id: str, resolution: str, root_cause: Optional[str] = None) -> Incident:
        if incident_id not in self.incidents:
            raise ValueError(f"Incident {incident_id} not found")
        inc = self.incidents[incident_id]
        now = datetime.utcnow()
        inc.status = IncidentStatus.RESOLVED
        inc.resolution = resolution
        inc.root_cause = root_cause
        inc.updated_at = now
        inc.timeline.append({"event": "resolved", "resolution": resolution, "root_cause": root_cause, "timestamp": now.isoformat()})
        duration = (now - inc.created_at).total_seconds()
        logger.info("Incident resolved: %s (duration=%.0fs)", incident_id, duration)
        return inc

    def create_postmortem(self, incident_id: str, summary: str, timeline: List[Dict[str, Any]], root_cause: str, action_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        if incident_id not in self.incidents:
            raise ValueError(f"Incident {incident_id} not found")
        inc = self.incidents[incident_id]
        duration = (inc.updated_at - inc.created_at).total_seconds()
        postmortem = {"incident_id": incident_id, "title": inc.title, "severity": inc.severity.value, "duration_seconds": duration, "summary": summary, "timeline": timeline, "root_cause": root_cause, "action_items": action_items, "created_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.postmortems.append(postmortem)
        logger.info("Postmortem created for incident %s", incident_id)
        return postmortem

    def add_oncall_rotation(self, person: str, start: datetime, end: datetime) -> Dict[str, Any]:
        entry = {"person": person, "start": start.isoformat(), "end": end.isoformat(), "active": True}
        with self._lock:
            self.oncall_schedule.append(entry)
        return entry

    def get_current_oncall(self) -> Optional[Dict[str, Any]]:
        now = datetime.utcnow()
        for entry in self.oncall_schedule:
            start = datetime.fromisoformat(entry["start"])
            end = datetime.fromisoformat(entry["end"])
            if start <= now <= end and entry["active"]:
                return entry
        return None

    def add_runbook(self, name: str, title: str, steps: List[str], escalation: Optional[str] = None) -> Dict[str, Any]:
        runbook = {"name": name, "title": title, "steps": steps, "escalation": escalation, "created_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.runbooks[name] = runbook
        return runbook

    def create_escalation_policy(self, name: str, levels: List[Dict[str, Any]]) -> Dict[str, Any]:
        policy = {"name": name, "levels": levels, "created_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.escalation_policies[name] = policy
        return policy

    def get_incidents_by_severity(self, severity: Severity) -> List[Incident]:
        return [i for i in self.incidents.values() if i.severity == severity]

    def get_incident_summary(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        by_severity = defaultdict(int)
        for inc in self.incidents.values():
            by_status[inc.status.value] += 1
            by_severity[inc.severity.value] += 1
        return {"total": len(self.incidents), "by_status": dict(by_status), "by_severity": dict(by_severity), "postmortems": len(self.postmortems), "runbooks": len(self.runbooks)}


# ──────────────────────────────────────────────
# SRE Practices
# ──────────────────────────────────────────────

class SREPractices:
    """Site Reliability Engineering practices: SLI, SLO, Error Budgets."""

    def __init__(self):
        self.slis: Dict[str, SLIDefinition] = {}
        self.slos: Dict[str, SLODefinition] = {}
        self.error_budgets: Dict[str, Dict[str, Any]] = {}
        self.sli_measurements: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._lock = threading.Lock()
        logger.info("SREPractices initialized")

    def define_sli(self, name: str, description: str, metric_query: str, good_event: str, total_event: str, window_minutes: int = 60) -> SLIDefinition:
        sli = SLIDefinition(name=name, description=description, metric_query=metric_query, good_event=good_event, total_event=total_event, window_minutes=window_minutes)
        with self._lock:
            self.slis[name] = sli
        logger.info("SLI defined: %s", name)
        return sli

    def define_slo(self, name: str, target_percentage: float, sli_name: str, window_days: int = 30) -> SLODefinition:
        if sli_name not in self.slis:
            raise ValueError(f"SLI {sli_name} not found")
        slo = SLODefinition(name=name, target_percentage=target_percentage, window_days=window_days, sli=self.slis[sli_name], error_budget_remaining=100.0 - target_percentage)
        with self._lock:
            self.slos[name] = slo
            self.error_budgets[name] = {"total_budget": 100.0 - target_percentage, "consumed": 0.0, "remaining": 100.0 - target_percentage}
        logger.info("SLO defined: %s (target=%.2f%%)", name, target_percentage)
        return slo

    def record_sli_measurement(self, slo_name: str, good_count: int, total_count: int) -> Dict[str, Any]:
        if slo_name not in self.slos:
            raise ValueError(f"SLO {slo_name} not found")
        pct = (good_count / total_count * 100) if total_count > 0 else 100.0
        measurement = {"percentage": round(pct, 4), "good_count": good_count, "total_count": total_count, "timestamp": datetime.utcnow().isoformat()}
        with self._lock:
            self.sli_measurements[slo_name].append(measurement)
        slo = self.slos[slo_name]
        if pct < slo.target_percentage:
            violation = slo.target_percentage - pct
            budget = self.error_budgets[slo_name]
            budget["consumed"] = round(budget["consumed"] + violation, 4)
            budget["remaining"] = round(budget["total_budget"] - budget["consumed"], 4)
            slo.error_budget_remaining = budget["remaining"]
            logger.warning("SLO violation for %s: %.2f%% (target=%.2f%%)", slo_name, pct, slo.target_percentage)
        return measurement

    def calculate_burn_rate(self, slo_name: str, lookback_hours: int = 6) -> Dict[str, Any]:
        if slo_name not in self.slos:
            raise ValueError(f"SLO {slo_name} not found")
        slo = self.slos[slo_name]
        measurements = self.sli_measurements.get(slo_name, [])
        if not measurements:
            return {"slo_name": slo_name, "burn_rate": 1.0, "status": "no_data"}
        cutoff = datetime.utcnow() - timedelta(hours=lookback_hours)
        recent = [m for m in measurements if datetime.fromisoformat(m["timestamp"]) >= cutoff]
        if not recent:
            return {"slo_name": slo_name, "burn_rate": 1.0, "status": "no_recent_data"}
        avg_availability = sum(m["percentage"] for m in recent) / len(recent)
        allowed_error_rate = (100 - slo.target_percentage) / 100
        actual_error_rate = (100 - avg_availability) / 100
        burn_rate = actual_error_rate / allowed_error_rate if allowed_error_rate > 0 else 0.0
        return {"slo_name": slo_name, "burn_rate": round(burn_rate, 4), "avg_availability": round(avg_availability, 4), "target": slo.target_percentage, "lookback_hours": lookback_hours, "status": "critical" if burn_rate > 14.4 else "warning" if burn_rate > 1.0 else "ok"}

    def get_error_budget_status(self, slo_name: str) -> Dict[str, Any]:
        if slo_name not in self.error_budgets:
            raise ValueError(f"Error budget for {slo_name} not found")
        budget = self.error_budgets[slo_name]
        pct_remaining = (budget["remaining"] / budget["total_budget"] * 100) if budget["total_budget"] > 0 else 100.0
        return {"slo_name": slo_name, "total_budget_pct": budget["total_budget"], "consumed_pct": budget["consumed"], "remaining_pct": budget["remaining"], "percentage_remaining": round(pct_remaining, 2), "status": "healthy" if pct_remaining > 50 else "at_risk" if pct_remaining > 10 else "exhausted"}

    def get_slo_dashboard(self) -> List[SLOStatus]:
        dashboards = []
        for name, slo in self.slos.items():
            measurements = self.sli_measurements.get(name, [])
            current = measurements[-1]["percentage"] if measurements else 100.0
            burn = self.calculate_burn_rate(name)
            budget_info = self.get_error_budget_status(name)
            dashboards.append(SLOStatus(slo_name=name, current_value=current, target_value=slo.target_percentage, error_budget_total=budget_info["total_budget_pct"], error_budget_remaining=budget_info["remaining_pct"], status=budget_info["status"], burn_rate=burn["burn_rate"], breach_forecast_hours=self._forecast_breach(name)))
        return dashboards

    def _forecast_breach(self, slo_name: str) -> Optional[float]:
        measurements = self.sli_measurements.get(slo_name, [])
        if len(measurements) < 2 or slo_name not in self.error_budgets:
            return None
        slo = self.slos[slo_name]
        remaining = self.error_budgets[slo_name]["remaining"]
        recent = measurements[-10:]
        violations = sum(1 for m in recent if m["percentage"] < slo.target_percentage)
        if violations == 0:
            return None
        violation_rate = violations / len(recent)
        estimated_hours = remaining / (violation_rate * (100 - slo.target_percentage) / 100) if violation_rate > 0 else None
        return round(estimated_hours, 1) if estimated_hours else None


# ──────────────────────────────────────────────
# GitOps Manager
# ──────────────────────────────────────────────

class GitOpsManager:
    """GitOps workflow management with ArgoCD and Flux."""

    def __init__(self):
        self.applications: Dict[str, GitOpsApplication] = {}
        self.repositories: Dict[str, Dict[str, Any]] = {}
        self.sync_history: List[Dict[str, Any]] = []
        self.webhooks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        logger.info("GitOpsManager initialized")

    def register_repository(self, name: str, url: str, branch: str = "main", credentials_secret: Optional[str] = None) -> Dict[str, Any]:
        rid = hashlib.sha256(url.encode()).hexdigest()[:12]
        repo = {"id": rid, "name": name, "url": url, "branch": branch, "credentials_secret": credentials_secret, "status": "active", "registered_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.repositories[name] = repo
        logger.info("Repository registered: %s (%s)", name, url)
        return repo

    def create_application(self, name: str, repo_url: str, target_revision: str, target_namespace: str, path: str = ".", sync_policy: str = "auto", auto_prune: bool = True, self_heal: bool = True) -> GitOpsApplication:
        app = GitOpsApplication(name=name, repo_url=repo_url, target_revision=target_revision, target_namespace=target_namespace, sync_policy=sync_policy, auto_prune=auto_prune, self_heal=self_heal)
        with self._lock:
            self.applications[name] = app
        logger.info("GitOps application created: %s", name)
        return app

    def sync_application(self, name: str) -> Dict[str, Any]:
        if name not in self.applications:
            raise ValueError(f"Application {name} not found")
        app = self.applications[name]
        result = {"application": name, "repo": app.repo_url, "revision": app.target_revision, "namespace": app.target_namespace, "status": "synced", "synced_at": datetime.utcnow().isoformat(), "resources_synced": 5, "health_status": "healthy"}
        with self._lock:
            self.sync_history.append(result)
        logger.info("Application synced: %s", name)
        return result

    def add_webhook(self, name: str, url: str, secret: Optional[str] = None, events: Optional[List[str]] = None) -> Dict[str, Any]:
        wh = {"name": name, "url": url, "secret": secret or secrets.token_hex(32), "events": events or ["push", "pull_request"], "status": "active", "created_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.webhooks[name] = wh
        logger.info("Webhook registered: %s -> %s", name, url)
        return {"name": name, "url": url, "events": wh["events"], "status": "active"}

    def generate_argocd_application(self, app: GitOpsApplication) -> str:
        manifest = {"apiVersion": "argoproj.io/v1alpha1", "kind": "Application", "metadata": {"name": app.name, "namespace": "argocd"}, "spec": {"project": "default", "source": {"repoURL": app.repo_url, "targetRevision": app.target_revision, "path": "."}, "destination": {"server": "https://kubernetes.default.svc", "namespace": app.target_namespace}, "syncPolicy": {"automated": {"prune": app.auto_prune, "selfHeal": app.self_heal}, "syncOptions": ["CreateNamespace=true"]}}}
        return json.dumps(manifest, indent=2)

    def generate_flux_kustomization(self, name: str, repo_ref: str, path: str, namespace: str = "default", interval: str = "5m") -> str:
        manifest = {"apiVersion": "kustomize.toolkit.fluxcd.io/v1", "kind": "Kustomization", "metadata": {"name": name, "namespace": "flux-system"}, "spec": {"interval": interval, "path": path, "prune": True, "sourceRef": {"kind": "GitRepository", "name": repo_ref}, "targetNamespace": namespace}}
        return json.dumps(manifest, indent=2)

    def get_sync_status(self) -> Dict[str, Any]:
        synced = len([s for s in self.sync_history if s["status"] == "synced"])
        return {"total_applications": len(self.applications), "total_repositories": len(self.repositories), "total_syncs": len(self.sync_history), "synced": synced, "failed": len(self.sync_history) - synced, "webhooks": len(self.webhooks)}


# ──────────────────────────────────────────────
# Secret Manager
# ──────────────────────────────────────────────

class SecretManager:
    """Secret lifecycle management across multiple engines."""

    def __init__(self):
        self.secrets: Dict[str, SecretEntry] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.rotation_schedule: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        logger.info("SecretManager initialized")

    def create_secret(self, name: str, engine: SecretEngine, path: str, data: Dict[str, str], ttl_seconds: int = 3600, rotation_enabled: bool = False, rotation_interval_days: int = 90) -> SecretEntry:
        secret = SecretEntry(name=name, engine=engine, path=path, data=data.copy(), ttl_seconds=ttl_seconds, rotation_enabled=rotation_enabled, rotation_interval_days=rotation_interval_days)
        with self._lock:
            self.secrets[name] = secret
            if rotation_enabled:
                self.rotation_schedule[name] = {"interval_days": rotation_interval_days, "last_rotated": datetime.utcnow().isoformat(), "next_rotation": (datetime.utcnow() + timedelta(days=rotation_interval_days)).isoformat()}
            self._audit("create", name, f"Secret created via {engine.value}")
        logger.info("Secret created: %s (engine=%s)", name, engine.value)
        return secret

    def get_secret(self, name: str) -> Dict[str, str]:
        if name not in self.secrets:
            raise ValueError(f"Secret {name} not found")
        self._audit("access", name, "Secret retrieved")
        return self.secrets[name].data

    def update_secret(self, name: str, data: Dict[str, str]) -> SecretEntry:
        if name not in self.secrets:
            raise ValueError(f"Secret {name} not found")
        self.secrets[name].data.update(data)
        self._audit("update", name, f"Updated keys: {list(data.keys())}")
        logger.info("Secret updated: %s", name)
        return self.secrets[name]

    def delete_secret(self, name: str) -> bool:
        if name not in self.secrets:
            raise ValueError(f"Secret {name} not found")
        del self.secrets[name]
        self._audit("delete", name, "Secret deleted")
        logger.warning("Secret deleted: %s", name)
        return True

    def rotate_secret(self, name: str) -> Dict[str, Any]:
        if name not in self.secrets:
            raise ValueError(f"Secret {name} not found")
        secret = self.secrets[name]
        for key in secret.data:
            secret.data[key] = secrets.token_hex(32)
        if name in self.rotation_schedule:
            self.rotation_schedule[name]["last_rotated"] = datetime.utcnow().isoformat()
            self.rotation_schedule[name]["next_rotation"] = (datetime.utcnow() + timedelta(days=secret.rotation_interval_days)).isoformat()
        self._audit("rotate", name, "Secret rotated")
        logger.info("Secret rotated: %s", name)
        return {"name": name, "rotated_at": datetime.utcnow().isoformat(), "keys_rotated": len(secret.data)}

    def generate_kubernetes_secret(self, name: str, namespace: str = "default", data: Optional[Dict[str, str]] = None) -> str:
        import base64
        b64_data = {k: base64.b64encode(v.encode()).decode() for k, v in (data or {}).items()}
        manifest = {"apiVersion": "v1", "kind": "Secret", "metadata": {"name": name, "namespace": namespace}, "type": "Opaque", "data": b64_data}
        return json.dumps(manifest, indent=2)

    def generate_vault_policy(self, name: str, paths: List[Dict[str, str]]) -> str:
        policy_rules = [f'path "{p.get("path", "*")}" {{ capabilities = [{", ".join(f\'"{c}"\' for c in p.get("capabilities", ["read"]))}] }}' for p in paths]
        return f'path "secret/data/{name}" {{\n  capabilities = ["read", "list"]\n}}\n\n' + "\n\n".join(policy_rules)

    def _audit(self, action: str, secret_name: str, details: str) -> None:
        self.audit_log.append({"action": action, "secret": secret_name, "details": details, "timestamp": datetime.utcnow().isoformat()})

    def get_audit_log(self, secret_name: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        logs = [l for l in self.audit_log if not secret_name or l["secret"] == secret_name]
        return logs[-limit:]


# ──────────────────────────────────────────────
# Configuration Management
# ──────────────────────────────────────────────

class ConfigurationManagement:
    """Centralized configuration and feature flag management."""

    def __init__(self):
        self.configs: Dict[str, ConfigItem] = {}
        self.feature_flags: Dict[str, Dict[str, Any]] = {}
        self.environments: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        logger.info("ConfigurationManagement initialized")

    def set_config(self, key: str, value: Any, namespace: str = "default", encrypted: bool = False, tags: Optional[Dict[str, str]] = None) -> ConfigItem:
        full_key = f"{namespace}/{key}"
        existing = self.configs.get(full_key)
        version = (existing.version + 1) if existing else 1
        item = ConfigItem(key=full_key, value=value, namespace=namespace, encrypted=encrypted, version=version, tags=tags or {})
        with self._lock:
            self.configs[full_key] = item
        logger.info("Config set: %s (v%d)", full_key, version)
        return item

    def get_config(self, key: str, namespace: str = "default", default: Any = None) -> Any:
        item = self.configs.get(f"{namespace}/{key}")
        return item.value if item else default

    def delete_config(self, key: str, namespace: str = "default") -> bool:
        full_key = f"{namespace}/{key}"
        if full_key not in self.configs:
            return False
        del self.configs[full_key]
        logger.info("Config deleted: %s", full_key)
        return True

    def list_configs(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        items = list(self.configs.values())
        if namespace:
            items = [i for i in items if i.namespace == namespace]
        return [{"key": i.key, "namespace": i.namespace, "version": i.version, "encrypted": i.encrypted, "tags": i.tags} for i in items]

    def set_feature_flag(self, name: str, enabled: bool, rollout_percentage: float = 100.0, allowed_environments: Optional[List[str]] = None, description: str = "") -> Dict[str, Any]:
        flag = {"name": name, "enabled": enabled, "rollout_percentage": rollout_percentage, "allowed_environments": allowed_environments or ["dev", "staging", "prod"], "description": description, "created_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.feature_flags[name] = flag
        logger.info("Feature flag %s: enabled=%s (%.0f%%)", name, enabled, rollout_percentage)
        return flag

    def evaluate_feature_flag(self, name: str, environment: str, user_id: Optional[str] = None) -> bool:
        if name not in self.feature_flags:
            return False
        flag = self.feature_flags[name]
        if not flag["enabled"] or environment not in flag["allowed_environments"]:
            return False
        if flag["rollout_percentage"] < 100.0 and user_id:
            hash_val = int(hashlib.md5(f"{name}:{user_id}".encode()).hexdigest(), 16) % 100
            return hash_val < flag["rollout_percentage"]
        return True

    def create_environment_config(self, environment: str, configs: Dict[str, Any]) -> Dict[str, Any]:
        env_config = {"environment": environment, "configs": configs, "created_at": datetime.utcnow().isoformat()}
        with self._lock:
            self.environments[environment] = env_config
        logger.info("Environment config created: %s (%d keys)", environment, len(configs))
        return env_config

    def diff_configs(self, env_a: str, env_b: str) -> Dict[str, Any]:
        a = self.environments.get(env_a, {}).get("configs", {})
        b = self.environments.get(env_b, {}).get("configs", {})
        return {"environment_a": env_a, "environment_b": env_b, "only_in_a": {k: v for k, v in a.items() if k not in b}, "only_in_b": {k: v for k, v in b.items() if k not in a}, "different": {k: {"a": a[k], "b": b[k]} for k in a if k in b and a[k] != b[k]}}

    def export_config_map(self, namespace: str = "default") -> str:
        configs = {i.key.split("/", 1)[1]: i.value for i in self.configs.values() if i.namespace == namespace}
        return json.dumps(configs, indent=2, default=str)


# ──────────────────────────────────────────────
# Main DevOps Agent
# ──────────────────────────────────────────────

class DevOpsAgent:
    """Main DevOps Agent orchestrating all subsystems."""

    def __init__(self, default_provider: CloudProvider = CloudProvider.AWS):
        self.infrastructure = InfrastructureAutomation(default_provider)
        self.container = ContainerOrchestration()
        self.monitoring = MonitoringManager()
        self.incidents = IncidentManager()
        self.sre = SREPractices()
        self.gitops = GitOpsManager()
        self.secrets = SecretManager()
        self.config = ConfigurationManagement()
        logger.info("DevOpsAgent initialized with provider=%s", default_provider.value)

    def deploy_service(self, service: str, version: str, environment: str, replicas: int = 3, strategy: str = "ROLLING", cluster: str = "default", namespace: str = "default") -> Dict[str, Any]:
        env = Environment(environment)
        strat = DeploymentStrategy[strategy]
        config = DeploymentConfig(service_name=service, version=version, environment=env, strategy=strat, replica_count=replicas, namespace=namespace)
        k8s_result = self.container.create_deployment(config, cluster)
        svc_result = self.container.create_service(service, {"app": service}, namespace=namespace)
        ingress = self.container.create_ingress(f"{service}-ingress", f"{service}.{environment}.example.com", "/", service, namespace=namespace)
        return {"deployment": k8s_result, "service": svc_result, "ingress": ingress, "environment": environment, "cluster": cluster}

    def setup_monitoring(self, service: str) -> Dict[str, Any]:
        self.monitoring.set_threshold(f"{service}_cpu_usage", warning=70, critical=90)
        self.monitoring.set_threshold(f"{service}_memory_usage", warning=80, critical=95)
        self.monitoring.set_threshold(f"{service}_response_time_ms", warning=500, critical=1000)
        self.monitoring.set_threshold(f"{service}_error_rate", warning=1.0, critical=5.0)
        dashboard = self.monitoring.create_dashboard(f"{service}-overview", [{"title": "CPU", "type": "graph"}, {"title": "Memory", "type": "graph"}, {"title": "Latency", "type": "graph"}, {"title": "Errors", "type": "stat"}])
        self.sre.define_sli(f"{service}_availability", "Request success rate", f"sum(rate(http_requests_total{{service=\"{service}\",code!=\"500\"}}[5m]))", "success", "all")
        self.sre.define_slo(f"{service}_availability_slo", 99.9, f"{service}_availability")
        return {"service": service, "thresholds": 4, "dashboard": dashboard["name"], "slo": f"{service}_availability_slo"}

    def create_pipeline(self, name: str, stages: List[Dict[str, Any]], environment: str = "dev") -> Dict[str, Any]:
        pipeline = PipelineConfig(name=name, stages=stages, environment=Environment(environment))
        pipeline.validate()
        return {"pipeline": pipeline.name, "stages": len(pipeline.stages), "environment": pipeline.environment.value, "status": "created"}

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "infrastructure": self.infrastructure.get_state(),
            "containers": {"deployments": len(self.container.deployments), "services": len(self.container.services), "clusters": len(self.container.clusters)},
            "monitoring": self.monitoring.generate_health_report(),
            "incidents": self.incidents.get_incident_summary(),
            "gitops": self.gitops.get_sync_status(),
            "secrets": {"total": len(self.secrets.secrets)},
            "slo_dashboard": [{"name": s.slo_name, "current": s.current_value, "target": s.target_value, "status": s.status} for s in self.sre.get_slo_dashboard()]
        }


def main():
    print("\n" + "=" * 70)
    print("  DevOps Agent - Enterprise-Grade Infrastructure Automation")
    print("=" * 70 + "\n")
    agent = DevOpsAgent(CloudProvider.AWS)
    pipeline = agent.create_pipeline("my-app-pipeline", [
        {"name": "Checkout", "type": "checkout"},
        {"name": "Build", "type": "build", "command": "npm run build"},
        {"name": "Test", "type": "test", "framework": "jest"},
        {"name": "Security Scan", "type": "security_scan"},
        {"name": "Docker Build", "type": "docker"},
        {"name": "Deploy to Staging", "type": "deploy", "environment": "staging"},
        {"name": "Deploy to Production", "type": "deploy", "environment": "production"}
    ], "production")
    print(f"Pipeline Created: {json.dumps(pipeline, indent=2)}")
    deployment = agent.deploy_service("my-service", "v1.0.0", "staging", replicas=3, strategy="CANARY")
    print(f"Deployment created: {deployment['deployment']['deployment_id']}")
    monitoring = agent.setup_monitoring("my-service")
    print(f"Monitoring setup: {json.dumps(monitoring, indent=2)}")
    status = agent.get_system_status()
    print(f"System Status: {json.dumps(status, indent=2, default=str)[:300]}...")


if __name__ == "__main__":
    main()
