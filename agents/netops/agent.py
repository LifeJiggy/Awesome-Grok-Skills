"""
Network Operations (NetOps) Agent
Network monitoring, configuration management, troubleshooting, and capacity planning.
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class DeviceType(Enum):
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    ACCESS_POINT = "access_point"
    SERVER = "server"
    OPTICAL = "optical"


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    SNMP = "snmp"
    DNS = "dns"
    ICMP = "icmp"
    BGP = "bgp"
    OSPF = "ospf"


class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ConfigStatus(Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    APPROVED = "approved"
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"


class TrafficClass(Enum):
    VOICE = "voice"
    VIDEO = "video"
    CRITICAL = "critical"
    BUSINESS = "business"
    BEST_EFFORT = "best_effort"
    SCAVENGER = "scavenger"


class SecurityThreat(Enum):
    PORT_SCAN = "port_scan"
    BRUTE_FORCE = "brute_force"
    MALWARE = "malware"
    DDoS = "ddos"
    INTRUSION = "intrusion"
    DATA_EXFIL = "data_exfiltration"
    PHIISHING = "phishing"


class MaintenanceWindow(Enum):
    EMERGENCY = "emergency"
    SCHEDULED = "scheduled"
    PLANNED = "planned"


# ──────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────

@dataclass
class NetworkDevice:
    device_id: str = field(default_factory=lambda: f"dev_{str(uuid4())[:8]}")
    name: str = ""
    device_type: DeviceType = DeviceType.ROUTER
    ip_address: str = ""
    mac_address: str = ""
    status: DeviceStatus = DeviceStatus.UNKNOWN
    vendor: str = ""
    model: str = ""
    firmware_version: str = ""
    location: str = ""
    interfaces: List[Dict[str, Any]] = field(default_factory=list)
    last_seen: Optional[datetime] = None
    uptime_seconds: float = 0.0


@dataclass
class NetworkInterface:
    interface_id: str = field(default_factory=lambda: f"int_{str(uuid4())[:8]}")
    device_id: str = ""
    name: str = ""
    ip_address: str = ""
    mac_address: str = ""
    speed_mbps: float = 0.0
    status: str = "up"
    in_octets: int = 0
    out_octets: int = 0
    errors: int = 0
    drops: int = 0


@dataclass
class ConfigChange:
    change_id: str = field(default_factory=lambda: f"cfg_{str(uuid4())[:8]}")
    device_id: str = ""
    config_type: str = "running"
    changes: List[Dict[str, Any]] = field(default_factory=list)
    status: ConfigStatus = ConfigStatus.DRAFT
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    applied_at: Optional[datetime] = None
    rollback_available: bool = True


@dataclass
class FirewallRule:
    rule_id: str = field(default_factory=lambda: f"rule_{str(uuid4())[:8]}")
    name: str = ""
    action: str = "permit"
    protocol: Protocol = Protocol.TCP
    source: str = "any"
    destination: str = "any"
    port: str = "any"
    direction: str = "inbound"
    enabled: bool = True
    hit_count: int = 0


@dataclass
class QoSPolicy:
    policy_id: str = field(default_factory=lambda: f"qos_{str(uuid4())[:8]}")
    name: str = ""
    classes: List[Dict[str, Any]] = field(default_factory=list)
    total_bandwidth_mbps: float = 0.0
    status: str = "inactive"


@dataclass
class RouteEntry:
    route_id: str = field(default_factory=lambda: f"rt_{str(uuid4())[:8]}")
    destination: str = ""
    gateway: str = ""
    interface: str = ""
    metric: int = 0
    protocol: str = "static"
    ad_distance: int = 0
    is_active: bool = True


@dataclass
class SecurityEvent:
    event_id: str = field(default_factory=lambda: f"sec_{str(uuid4())[:8]}")
    threat_type: SecurityThreat = SecurityThreat.PORT_SCAN
    source_ip: str = ""
    destination_ip: str = ""
    severity: AlertSeverity = AlertSeverity.MEDIUM
    message: str = ""
    blocked: bool = False
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CapacityMetrics:
    metric_id: str = field(default_factory=lambda: f"cap_{str(uuid4())[:8]}")
    device_id: str = ""
    cpu_utilization: float = 0.0
    memory_utilization: float = 0.0
    bandwidth_utilization: float = 0.0
    connection_count: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DiagnosticResult:
    test_name: str = ""
    target: str = ""
    result: str = "success"
    latency_ms: float = 0.0
    packet_loss: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CapacityForecast:
    resource: str = ""
    current_utilization: float = 0.0
    projected_30d: float = 0.0
    projected_90d: float = 0.0
    projected_180d: float = 0.0
    bottleneck: bool = False
    recommendation: str = ""


# ──────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────

class NetOpsError(Exception):
    """Base NetOps error."""


class DeviceNotFoundError(NetOpsError):
    """Device not found."""


class ConfigError(NetOpsError):
    """Configuration error."""


class DiagnosticError(NetOpsError):
    """Diagnostic test failed."""


# ──────────────────────────────────────────────
# Network Monitor
# ──────────────────────────────────────────────

class NetworkMonitor:
    """Monitor network devices and interfaces."""

    def __init__(self) -> None:
        self._devices: Dict[str, NetworkDevice] = {}
        self._interfaces: Dict[str, List[NetworkInterface]] = {}
        self._capacity: Dict[str, List[CapacityMetrics]] = {}

    def add_device(
        self,
        name: str,
        device_type: DeviceType,
        ip_address: str,
        vendor: str = "",
        model: str = "",
        location: str = "",
    ) -> NetworkDevice:
        device = NetworkDevice(
            name=name,
            device_type=device_type,
            ip_address=ip_address,
            vendor=vendor,
            model=model,
            location=location,
            last_seen=datetime.now(),
        )
        self._devices[device.device_id] = device
        logger.info("Added device %s (%s) at %s", name, device_type.value, ip_address)
        return device

    def update_device_status(self, device_id: str, status: DeviceStatus) -> NetworkDevice:
        device = self._get_device(device_id)
        device.status = status
        device.last_seen = datetime.now()
        return device

    def add_interface(
        self,
        device_id: str,
        name: str,
        ip_address: str,
        speed_mbps: float,
        mac_address: str = "",
    ) -> NetworkInterface:
        self._get_device(device_id)
        interface = NetworkInterface(
            device_id=device_id,
            name=name,
            ip_address=ip_address,
            mac_address=mac_address,
            speed_mbps=speed_mbps,
        )
        self._interfaces.setdefault(device_id, []).append(interface)
        return interface

    def record_interface_stats(
        self, device_id: str, interface_name: str, in_octets: int, out_octets: int, errors: int = 0
    ) -> Optional[NetworkInterface]:
        interfaces = self._interfaces.get(device_id, [])
        for iface in interfaces:
            if iface.name == interface_name:
                iface.in_octets = in_octets
                iface.out_octets = out_octets
                iface.errors = errors
                return iface
        return None

    def get_network_health(self) -> Dict[str, Any]:
        devices = list(self._devices.values())
        total = len(devices)
        online = sum(1 for d in devices if d.status == DeviceStatus.ONLINE)
        offline = sum(1 for d in devices if d.status == DeviceStatus.OFFLINE)
        degraded = sum(1 for d in devices if d.status == DeviceStatus.DEGRADED)
        return {
            "total_devices": total,
            "online": online,
            "offline": offline,
            "degraded": degraded,
            "health_percent": round(online / total * 100, 2) if total > 0 else 100.0,
        }

    def get_device(self, device_id: str) -> NetworkDevice:
        return self._get_device(device_id)

    def list_devices(self, device_type: Optional[DeviceType] = None, status: Optional[DeviceStatus] = None) -> List[NetworkDevice]:
        devices = list(self._devices.values())
        if device_type:
            devices = [d for d in devices if d.device_type == device_type]
        if status:
            devices = [d for d in devices if d.status == status]
        return devices

    def _get_device(self, device_id: str) -> NetworkDevice:
        if device_id not in self._devices:
            raise DeviceNotFoundError(f"Device {device_id} not found")
        return self._devices[device_id]


# ──────────────────────────────────────────────
# Configuration Manager
# ──────────────────────────────────────────────

class ConfigurationManager:
    """Manage network device configurations."""

    def __init__(self) -> None:
        self._configs: Dict[str, ConfigChange] = {}
        self._backups: Dict[str, List[Dict[str, Any]]] = {}

    def create_config(
        self,
        device_id: str,
        changes: List[Dict[str, Any]],
        created_by: str = "admin",
    ) -> ConfigChange:
        config = ConfigChange(device_id=device_id, changes=changes, created_by=created_by)
        self._configs[config.change_id] = config
        return config

    def validate_config(self, change_id: str) -> ConfigChange:
        config = self._get_config(change_id)
        config.status = ConfigStatus.VALIDATED
        return config

    def approve_config(self, change_id: str) -> ConfigChange:
        config = self._get_config(change_id)
        if config.status != ConfigStatus.VALIDATED:
            raise ConfigError("Config must be validated before approval")
        config.status = ConfigStatus.APPROVED
        return config

    def apply_config(self, change_id: str) -> ConfigChange:
        config = self._get_config(change_id)
        if config.status != ConfigStatus.APPROVED:
            raise ConfigError("Config must be approved before application")
        config.status = ConfigStatus.APPLIED
        config.applied_at = datetime.now()
        self._backups.setdefault(config.device_id, []).append({
            "change_id": change_id,
            "changes": config.changes,
            "applied_at": datetime.now().isoformat(),
        })
        logger.info("Applied config %s to device %s", change_id, config.device_id)
        return config

    def rollback_config(self, change_id: str) -> ConfigChange:
        config = self._get_config(change_id)
        if not config.rollback_available:
            raise ConfigError("Rollback not available for this config")
        config.status = ConfigStatus.ROLLED_BACK
        return config

    def compare_configs(self, device_id: str, config_a: str, config_b: str) -> Dict[str, Any]:
        return {
            "device_id": device_id,
            "config_a": config_a,
            "config_b": config_b,
            "differences": [
                {"line": 1, "change": "interface description", "type": "modification"},
                {"line": 15, "change": "access-list entry", "type": "addition"},
            ],
            "risk_level": "low",
        }

    def backup_config(self, device_id: str) -> Dict[str, Any]:
        return {
            "device_id": device_id,
            "backup_time": datetime.now().isoformat(),
            "config_size": "45KB",
            "hash": f"sha256:{uuid4().hex[:16]}",
            "retention_days": 90,
            "status": "success",
        }

    def get_config(self, change_id: str) -> ConfigChange:
        return self._get_config(change_id)

    def list_configs(self, device_id: Optional[str] = None) -> List[ConfigChange]:
        configs = list(self._configs.values())
        if device_id:
            configs = [c for c in configs if c.device_id == device_id]
        return configs

    def _get_config(self, change_id: str) -> ConfigChange:
        if change_id not in self._configs:
            raise ConfigError(f"Config {change_id} not found")
        return self._configs[change_id]


# ──────────────────────────────────────────────
# Security Manager
# ──────────────────────────────────────────────

class SecurityManager:
    """Manage firewall rules and analyze security events."""

    def __init__(self) -> None:
        self._firewall_rules: Dict[str, FirewallRule] = {}
        self._security_events: List[SecurityEvent] = []

    def add_firewall_rule(
        self,
        name: str,
        action: str,
        protocol: Protocol,
        source: str = "any",
        destination: str = "any",
        port: str = "any",
        direction: str = "inbound",
    ) -> FirewallRule:
        rule = FirewallRule(
            name=name,
            action=action,
            protocol=protocol,
            source=source,
            destination=destination,
            port=port,
            direction=direction,
        )
        self._firewall_rules[rule.rule_id] = rule
        return rule

    def disable_rule(self, rule_id: str) -> FirewallRule:
        rule = self._get_rule(rule_id)
        rule.enabled = False
        return rule

    def enable_rule(self, rule_id: str) -> FirewallRule:
        rule = self._get_rule(rule_id)
        rule.enabled = True
        return rule

    def log_security_event(
        self,
        threat_type: SecurityThreat,
        source_ip: str,
        destination_ip: str,
        severity: AlertSeverity,
        message: str,
        blocked: bool = False,
    ) -> SecurityEvent:
        event = SecurityEvent(
            threat_type=threat_type,
            source_ip=source_ip,
            destination_ip=destination_ip,
            severity=severity,
            message=message,
            blocked=blocked,
        )
        self._security_events.append(event)
        logger.warning("Security event: %s from %s", threat_type.value, source_ip)
        return event

    def get_threat_summary(self, hours: int = 24) -> Dict[str, Any]:
        since = datetime.now() - timedelta(hours=hours)
        events = [e for e in self._security_events if e.timestamp >= since]
        by_type: Dict[str, int] = {}
        by_severity: Dict[str, int] = {}
        blocked_count = 0
        for e in events:
            by_type[e.threat_type.value] = by_type.get(e.threat_type.value, 0) + 1
            by_severity[e.severity.value] = by_severity.get(e.severity.value, 0) + 1
            if e.blocked:
                blocked_count += 1
        return {
            "total_events": len(events),
            "blocked": blocked_count,
            "by_type": by_type,
            "by_severity": by_severity,
        }

    def analyze_firewall(self) -> Dict[str, Any]:
        rules = list(self._firewall_rules.values())
        active = [r for r in rules if r.enabled]
        return {
            "total_rules": len(rules),
            "active_rules": len(active),
            "inactive_rules": len(rules) - len(active),
            "top_hit_rules": sorted(rules, key=lambda r: r.hit_count, reverse=True)[:5],
        }

    def get_rule(self, rule_id: str) -> FirewallRule:
        return self._get_rule(rule_id)

    def list_rules(self) -> List[FirewallRule]:
        return list(self._firewall_rules.values())

    def _get_rule(self, rule_id: str) -> FirewallRule:
        if rule_id not in self._firewall_rules:
            raise NetOpsError(f"Firewall rule {rule_id} not found")
        return self._firewall_rules[rule_id]


# ──────────────────────────────────────────────
# Traffic Manager
# ──────────────────────────────────────────────

class TrafficManager:
    """Manage network traffic, routing, and QoS."""

    def __init__(self) -> None:
        self._routes: Dict[str, RouteEntry] = {}
        self._qos_policies: Dict[str, QoSPolicy] = {}
        self._bandwidth_history: List[Dict[str, Any]] = []

    def add_route(
        self,
        destination: str,
        gateway: str,
        interface: str,
        metric: int = 100,
        protocol: str = "static",
    ) -> RouteEntry:
        route = RouteEntry(
            destination=destination,
            gateway=gateway,
            interface=interface,
            metric=metric,
            protocol=protocol,
        )
        self._routes[route.route_id] = route
        return route

    def optimize_routes(self) -> Dict[str, Any]:
        routes = list(self._routes.values())
        active = [r for r in routes if r.is_active]
        return {
            "total_routes": len(routes),
            "active_routes": len(active),
            "optimization_opportunities": [
                {"route": r.destination, "current_metric": r.metric, "suggestion": "Reduce hop count"}
                for r in active if r.metric > 200
            ],
        }

    def create_qos_policy(
        self,
        name: str,
        total_bandwidth_mbps: float,
        classes: List[Dict[str, Any]],
    ) -> QoSPolicy:
        policy = QoSPolicy(
            name=name,
            total_bandwidth_mbps=total_bandwidth_mbps,
            classes=classes,
            status="inactive",
        )
        self._qos_policies[policy.policy_id] = policy
        return policy

    def apply_qos_policy(self, policy_id: str) -> QoSPolicy:
        policy = self._get_qos(policy_id)
        policy.status = "active"
        return policy

    def record_bandwidth(self, interface: str, utilization_percent: float, timestamp: Optional[datetime] = None) -> None:
        self._bandwidth_history.append({
            "interface": interface,
            "utilization": utilization_percent,
            "timestamp": timestamp or datetime.now(),
        })

    def get_bandwidth_trend(self, interface: str, hours: int = 24) -> Dict[str, Any]:
        since = datetime.now() - timedelta(hours=hours)
        history = [
            h for h in self._bandwidth_history
            if h["interface"] == interface and h["timestamp"] >= since
        ]
        if not history:
            return {"interface": interface, "data_points": 0}
        values = [h["utilization"] for h in history]
        return {
            "interface": interface,
            "data_points": len(values),
            "avg_utilization": round(sum(values) / len(values), 2),
            "max_utilization": round(max(values), 2),
            "min_utilization": round(min(values), 2),
        }

    def list_routes(self) -> List[RouteEntry]:
        return list(self._routes.values())

    def list_qos_policies(self) -> List[QoSPolicy]:
        return list(self._qos_policies.values())

    def _get_qos(self, policy_id: str) -> QoSPolicy:
        if policy_id not in self._qos_policies:
            raise NetOpsError(f"QoS policy {policy_id} not found")
        return self._qos_policies[policy_id]


# ──────────────────────────────────────────────
# Diagnostic Runner
# ──────────────────────────────────────────────

class DiagnosticRunner:
    """Run network diagnostic tests."""

    def __init__(self) -> None:
        self._results: List[DiagnosticResult] = []

    def ping(self, target: str, count: int = 5) -> DiagnosticResult:
        result = DiagnosticResult(
            test_name="ping",
            target=target,
            result="success",
            latency_ms=2.5,
            packet_loss=0.0,
            details={"packets_sent": count, "packets_received": count},
        )
        self._results.append(result)
        return result

    def traceroute(self, target: str, max_hops: int = 30) -> DiagnosticResult:
        hops = [
            {"hop": 1, "ip": "10.0.0.1", "latency_ms": 1.0},
            {"hop": 2, "ip": "10.0.1.1", "latency_ms": 5.0},
            {"hop": 3, "ip": target, "latency_ms": 15.0},
        ]
        result = DiagnosticResult(
            test_name="traceroute",
            target=target,
            result="success",
            latency_ms=15.0,
            details={"hops": hops, "hop_count": len(hops)},
        )
        self._results.append(result)
        return result

    def bandwidth_test(self, target: str) -> DiagnosticResult:
        result = DiagnosticResult(
            test_name="bandwidth",
            target=target,
            result="success",
            details={"download_mbps": 950.0, "upload_mbps": 480.0},
        )
        self._results.append(result)
        return result

    def dns_lookup(self, hostname: str) -> DiagnosticResult:
        result = DiagnosticResult(
            test_name="dns_lookup",
            target=hostname,
            result="success",
            latency_ms=5.0,
            details={"resolved_ip": "93.184.216.34", "ttl": 300},
        )
        self._results.append(result)
        return result

    def port_check(self, target: str, port: int) -> DiagnosticResult:
        result = DiagnosticResult(
            test_name="port_check",
            target=f"{target}:{port}",
            result="success",
            details={"port": port, "state": "open", "service": "http"},
        )
        self._results.append(result)
        return result

    def run_full_diagnostics(self, target: str) -> Dict[str, Any]:
        self.ping(target)
        self.traceroute(target)
        self.dns_lookup(target)
        self.bandwidth_test(target)
        self.port_check(target, 80)
        self.port_check(target, 443)
        return {
            "target": target,
            "tests_run": 6,
            "results": [
                {"test": r.test_name, "result": r.result, "latency_ms": r.latency_ms}
                for r in self._results[-6:]
            ],
        }

    def get_results(self) -> List[DiagnosticResult]:
        return list(self._results)


# ──────────────────────────────────────────────
# Capacity Planner
# ──────────────────────────────────────────────

class CapacityPlanner:
    """Plan and forecast network capacity needs."""

    def __init__(self) -> None:
        self._metrics: Dict[str, List[CapacityMetrics]] = {}
        self._forecasts: Dict[str, CapacityForecast] = {}

    def record_metrics(self, device_id: str, cpu: float, memory: float, bandwidth: float, connections: int = 0) -> CapacityMetrics:
        metrics = CapacityMetrics(
            device_id=device_id,
            cpu_utilization=cpu,
            memory_utilization=memory,
            bandwidth_utilization=bandwidth,
            connection_count=connections,
        )
        self._metrics.setdefault(device_id, []).append(metrics)
        return metrics

    def forecast(self, device_id: str, resource: str = "bandwidth") -> CapacityForecast:
        history = self._metrics.get(device_id, [])
        if not history:
            return CapacityForecast(resource=resource, bottleneck=False, recommendation="Collect more data")
        values = []
        for m in history:
            if resource == "cpu":
                values.append(m.cpu_utilization)
            elif resource == "memory":
                values.append(m.memory_utilization)
            else:
                values.append(m.bandwidth_utilization)
        if not values:
            return CapacityForecast(resource=resource, bottleneck=False, recommendation="No data")
        current = values[-1]
        n = len(values)
        x_mean = sum(range(n)) / n
        y_mean = sum(values) / n
        num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        den = sum((i - x_mean) ** 2 for i in range(n))
        slope = num / den if den != 0 else 0
        intercept = y_mean - slope * x_mean
        proj_30 = min(100, slope * (n + 30) + intercept)
        proj_90 = min(100, slope * (n + 90) + intercept)
        proj_180 = min(100, slope * (n + 180) + intercept)
        bottleneck = proj_90 > 80
        recommendation = "No action needed"
        if proj_90 > 90:
            recommendation = "Critical: Upgrade needed within 3 months"
        elif proj_90 > 80:
            recommendation = "Warning: Plan capacity upgrade within 6 months"
        forecast = CapacityForecast(
            resource=resource,
            current_utilization=round(current, 2),
            projected_30d=round(proj_30, 2),
            projected_90d=round(proj_90, 2),
            projected_180d=round(proj_180, 2),
            bottleneck=bottleneck,
            recommendation=recommendation,
        )
        self._forecasts[f"{device_id}:{resource}"] = forecast
        return forecast

    def get_forecast(self, device_id: str, resource: str) -> Optional[CapacityForecast]:
        return self._forecasts.get(f"{device_id}:{resource}")

    def list_forecasts(self) -> List[CapacityForecast]:
        return list(self._forecasts.values())


# ──────────────────────────────────────────────
# NetOps Agent (orchestrator)
# ──────────────────────────────────────────────

class NetOpsAgent:
    """Top-level orchestrator for all network operations."""

    def __init__(self) -> None:
        self.monitor = NetworkMonitor()
        self.config = ConfigurationManager()
        self.security = SecurityManager()
        self.traffic = TrafficManager()
        self.diagnostics = DiagnosticRunner()
        self.capacity = CapacityPlanner()
        logger.info("NetOpsAgent initialized")

    def full_network_audit(self, devices: List[Dict[str, Any]]) -> Dict[str, Any]:
        for dev_data in devices:
            device = self.monitor.add_device(
                name=dev_data["name"],
                device_type=DeviceType(dev_data.get("type", "router")),
                ip_address=dev_data["ip"],
                vendor=dev_data.get("vendor", ""),
            )
            self.monitor.update_device_status(device.device_id, DeviceStatus.ONLINE)
        health = self.monitor.get_network_health()
        threats = self.security.get_threat_summary()
        routes = self.traffic.optimize_routes()
        return {
            "health": health,
            "threats": threats,
            "route_optimizations": len(routes["optimization_opportunities"]),
        }


# ──────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = NetOpsAgent()

    device = agent.monitor.add_device("CoreRouter", DeviceType.ROUTER, "10.0.0.1", "Cisco", "ISR 4331")
    agent.monitor.update_device_status(device.device_id, DeviceStatus.ONLINE)
    health = agent.monitor.get_network_health()
    print(f"Health: {health['health_percent']}% online")

    config = agent.config.create_config(device.device_id, [{"setting": "mtu", "value": "9000"}], "admin")
    agent.config.validate_config(config.change_id)
    agent.config.approve_config(config.change_id)
    agent.config.apply_config(config.change_id)
    print(f"Config {config.change_id} applied")

    agent.security.add_firewall_rule("Allow HTTP", "permit", Protocol.TCP, port="80")
    agent.security.add_firewall_rule("Allow HTTPS", "permit", Protocol.TCP, port="443")
    agent.security.log_security_event(SecurityThreat.PORT_SCAN, "192.168.1.100", "10.0.0.1", AlertSeverity.HIGH, "Port scan detected")
    threats = agent.security.get_threat_summary()
    print(f"Security events: {threats['total_events']}")

    agent.traffic.add_route("10.0.0.0/8", "10.0.0.1", "eth0", metric=100)
    agent.traffic.add_route("172.16.0.0/12", "10.0.0.2", "eth1", metric=150)
    optimizations = agent.traffic.optimize_routes()
    print(f"Route optimizations: {len(optimizations['optimization_opportunities'])}")

    result = agent.diagnostics.run_full_diagnostics("10.0.0.1")
    print(f"Diagnostics: {result['tests_run']} tests run")

    agent.capacity.record_metrics(device.device_id, cpu=65, memory=70, bandwidth=75)
    agent.capacity.record_metrics(device.device_id, cpu=70, memory=72, bandwidth=78)
    forecast = agent.capacity.forecast(device.device_id, "bandwidth")
    print(f"Bandwidth forecast: {forecast.projected_90d}%, bottleneck: {forecast.bottleneck}")
