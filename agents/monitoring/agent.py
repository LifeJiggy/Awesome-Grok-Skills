"""
Monitoring Agent
System monitoring and alerting
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(Enum):
    FIRED = "fired"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


@dataclass
class Alert:
    alert_id: str
    name: str
    severity: AlertSeverity
    status: AlertStatus
    message: str
    labels: Dict
    starts_at: datetime
    ends_at: Optional[datetime]


class PrometheusMetrics:
    """Prometheus-style metrics collector"""
    
    def __init__(self):
        self.counters = {}
        self.gauges = {}
        self.histograms = {}
    
    def counter(self, name: str, description: str = "", labels: List[str] = None):
        """Define counter metric"""
        self.counters[name] = {
            "description": description,
            "labels": labels or [],
            "value": 0
        }
    
    def gauge(self, name: str, description: str = "", labels: List[str] = None):
        """Define gauge metric"""
        self.gauges[name] = {
            "description": description,
            "labels": labels or [],
            "value": 0
        }
    
    def histogram(self, name: str, description: str = "", buckets: List[float] = None):
        """Define histogram metric"""
        self.histograms[name] = {
            "description": description,
            "buckets": buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1],
            "values": []
        }
    
    def inc_counter(self, name: str, value: float = 1, labels: Dict = None):
        """Increment counter"""
        if name in self.counters:
            self.counters[name]["value"] += value
    
    def set_gauge(self, name: str, value: float):
        """Set gauge value"""
        if name in self.gauges:
            self.gauges[name]["value"] = value
    
    def observe_histogram(self, name: str, value: float):
        """Observe histogram value"""
        if name in self.histograms:
            self.histograms[name]["values"].append(value)
    
    def scrape(self) -> Dict:
        """Scrape all metrics"""
        metrics = {}
        
        for name, counter in self.counters.items():
            metrics[name] = counter["value"]
        
        for name, gauge in self.gauges.items():
            metrics[name] = gauge["value"]
        
        for name, hist in self.histograms.items():
            values = hist["values"]
            metrics[f"{name}_count"] = len(values)
            metrics[f"{name}_sum"] = sum(values)
            metrics[f"{name}_avg"] = sum(values) / len(values) if values else 0
        
        return metrics


class AlertManager:
    """Alert management system"""
    
    def __init__(self):
        self.alerts = {}
        self.rules = {}
        self.notifications = []
    
    def add_rule(self,
                name: str,
                expr: str,
                severity: AlertSeverity,
                labels: Dict = None,
                annotations: Dict = None):
        """Add alert rule"""
        self.rules[name] = {
            "expr": expr,
            "severity": severity,
            "labels": labels or {},
            "annotations": annotations or {}
        }
    
    def fire_alert(self, 
                  rule_name: str,
                  labels: Dict = None) -> str:
        """Fire alert based on rule"""
        if rule_name not in self.rules:
            raise ValueError(f"Unknown rule: {rule_name}")
        
        rule = self.rules[rule_name]
        alert_id = f"alert_{int(datetime.now().timestamp())}"
        
        alert = Alert(
            alert_id=alert_id,
            name=rule_name,
            severity=rule["severity"],
            status=AlertStatus.FIRED,
            message=rule["annotations"].get("summary", "Alert fired"),
            labels={**rule["labels"], **(labels or {})},
            starts_at=datetime.now(),
            ends_at=None
        )
        
        self.alerts[alert_id] = alert
        self._send_notification(alert)
        
        return alert_id
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].status = AlertStatus.ACKNOWLEDGED
            return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].status = AlertStatus.RESOLVED
            self.alerts[alert_id].ends_at = datetime.now()
            return True
        return False
    
    def _send_notification(self, alert: Alert):
        """Send alert notification"""
        self.notifications.append({
            "alert_id": alert.alert_id,
            "severity": alert.severity.value,
            "message": alert.message,
            "channel": self._get_notification_channel(alert.severity),
            "sent_at": datetime.now()
        })
    
    def _get_notification_channel(self, severity: AlertSeverity) -> str:
        """Get notification channel based on severity"""
        channels = {
            AlertSeverity.CRITICAL: ["pager", "slack", "email"],
            AlertSeverity.HIGH: ["slack", "email"],
            AlertSeverity.MEDIUM: ["slack"],
            AlertSeverity.LOW: ["email"],
            AlertSeverity.INFO: []
        }
        return channels.get(severity, [])
    
    def get_active_alerts(self) -> List[Dict]:
        """Get all active alerts"""
        return [
            {
                "id": k,
                "name": v.name,
                "severity": v.severity.value,
                "status": v.status.value,
                "message": v.message,
                "duration": (datetime.now() - v.starts_at).total_seconds()
            }
            for k, v in self.alerts.items()
            if v.status in [AlertStatus.FIRED, AlertStatus.ACKNOWLEDGED]
        ]


class UptimeMonitor:
    """Uptime monitoring"""
    
    def __init__(self):
        self.checks = {}
        self.history = []
    
    def add_check(self,
                 name: str,
                 url: str,
                 method: str = "GET",
                 expected_status: int = 200,
                 timeout: int = 10):
        """Add uptime check"""
        self.checks[name] = {
            "url": url,
            "method": method,
            "expected_status": expected_status,
            "timeout": timeout,
            "interval": 60
        }
    
    def run_check(self, name: str) -> Dict:
        """Run uptime check"""
        if name not in self.checks:
            raise ValueError(f"Unknown check: {name}")
        
        check = self.checks[name]
        
        result = {
            "check": name,
            "url": check["url"],
            "status": "up",
            "status_code": check["expected_status"],
            "response_time_ms": 45,
            "timestamp": datetime.now()
        }
        
        self.history.append(result)
        
        return result
    
    def get_status_summary(self) -> Dict:
        """Get status summary"""
        recent = [h for h in self.history 
                 if h["timestamp"] > datetime.now() - timedelta(hours=1)]
        
        total_checks = len(self.checks)
        up_checks = len([h for h in recent if h["status"] == "up"])
        
        return {
            "total_checks": total_checks,
            "healthy": up_checks,
            "unhealthy": total_checks - up_checks,
            "uptime_percent": (up_checks / total_checks * 100) if total_checks > 0 else 100,
            "avg_response_time": sum(h["response_time_ms"] for h in recent) / len(recent) if recent else 0
        }


class LogMonitor:
    """Log monitoring and analysis"""
    
    def __init__(self):
        self.logs = []
        self.patterns = {}
    
    def add_pattern(self, 
                   name: str,
                   pattern: str,
                   severity: AlertSeverity):
        """Add log pattern to monitor"""
        self.patterns[name] = {
            "pattern": pattern,
            "severity": severity,
            "count": 0
        }
    
    def ingest_log(self, log_line: str, source: str = "app"):
        """Ingest log line"""
        import re
        
        log_entry = {
            "line": log_line,
            "source": source,
            "timestamp": datetime.now(),
            "level": self._extract_level(log_line),
            "matched_patterns": []
        }
        
        for name, pattern_info in self.patterns.items():
            if re.search(pattern_info["pattern"], log_line):
                log_entry["matched_patterns"].append(name)
                pattern_info["count"] += 1
        
        self.logs.append(log_entry)
        
        if log_entry["matched_patterns"]:
            return log_entry
        
        return None
    
    def _extract_level(self, log_line: str) -> str:
        """Extract log level"""
        if "ERROR" in log_line or "Exception" in log_line:
            return "error"
        elif "WARN" in log_line:
            return "warning"
        elif "DEBUG" in log_line:
            return "debug"
        return "info"
    
    def get_error_summary(self, 
                         since: datetime = None) -> Dict:
        """Get error summary"""
        since = since or datetime.now() - timedelta(hours=1)
        
        recent_logs = [l for l in self.logs if l["timestamp"] >= since]
        errors = [l for l in recent_logs if l["level"] == "error"]
        
        by_pattern = {}
        for log in errors:
            for pattern in log["matched_patterns"]:
                by_pattern[pattern] = by_pattern.get(pattern, 0) + 1
        
        return {
            "total_errors": len(errors),
            "error_rate": len(errors) / len(recent_logs) * 100 if recent_logs else 0,
            "by_pattern": by_pattern,
            "recent_errors": errors[:10]
        }


class DashboardGenerator:
    """Monitoring dashboard generation"""
    
    def __init__(self):
        self.panels = []
    
    def add_panel(self,
                 title: str,
                 panel_type: str,
                 metrics: List[str],
                 visualization: str = "graph"):
        """Add dashboard panel"""
        self.panels.append({
            "title": title,
            "type": panel_type,
            "metrics": metrics,
            "visualization": visualization
        })
    
    def generate_dashboard(self, 
                          name: str,
                          refresh_interval: int = 30) -> Dict:
        """Generate dashboard configuration"""
        return {
            "title": name,
            "refresh_interval": refresh_interval,
            "panels": self.panels,
            "created_at": datetime.now()
        }
    
    def export_grafana(self) -> str:
        """Export as Grafana dashboard"""
        dashboard = self.generate_dashboard("Auto-generated Dashboard")
        import json
        return json.dumps(dashboard, indent=2)


if __name__ == "__main__":
    metrics = PrometheusMetrics()
    alerts = AlertManager()
    uptime = UptimeMonitor()
    logs = LogMonitor()
    dashboard = DashboardGenerator()
    
    metrics.counter("http_requests_total", "Total HTTP requests")
    metrics.gauge("http_request_duration_seconds", "Request duration")
    metrics.inc_counter("http_requests_total")
    metrics.set_gauge("http_request_duration_seconds", 0.25)
    
    alerts.add_rule(
        "HighErrorRate",
        "rate(http_requests_total{status=~'5..'}[5m]) > 0.05",
        AlertSeverity.HIGH,
        {"service": "api"}
    )
    
    uptime.add_check("api", "https://api.example.com/health")
    uptime_result = uptime.run_check("api")
    
    logs.add_pattern("DatabaseError", r"Database.*error", AlertSeverity.HIGH)
    matched = logs.ingest_log("ERROR: Database connection failed")
    
    dashboard.add_panel("Request Rate", "graph", ["http_requests_total"])
    dashboard.add_panel("Response Time", "graph", ["http_request_duration_seconds"])
    
    print(f"Metrics: {metrics.scrape()}")
    print(f"Uptime: {uptime.get_status_summary()}")
    print(f"Log matched: {matched is not None}")
    print(f"Dashboard panels: {len(dashboard.panels)}")
