---
name: "security-monitoring"
category: "blue-team"
version: "2.0.0"
tags: ["blue-team", "SIEM", "monitoring", "detection", "alerting"]
---

# Security Monitoring

## Overview

The Security Monitoring module provides comprehensive tools for building, operating, and optimizing security monitoring infrastructure. It covers SIEM (Security Information and Event Management) integration, log aggregation, correlation rule development, alert triage, dashboard creation, and metrics reporting. The module supports integration with major SIEM platforms (Splunk, Elastic SIEM, Microsoft Sentinel, IBM QRadar) and cloud-native monitoring services.

This skill is essential for SOC analysts, security engineers, and blue team operators responsible for detecting and responding to security threats in real-time.

## Core Capabilities

- **Log Collection & Parsing**: Syslog, Windows Event Logs, cloud audit logs, application logs with structured parsing
- **Correlation Rules**: Sigma rule authoring, SPL queries (Splunk), KQL queries (Sentinel), EQL queries (Elastic)
- **Alert Management**: Alert creation, deduplication, enrichment, severity scoring, and escalation workflows
- **Dashboard Creation**: Real-time security dashboards, KPI tracking, trend visualization
- **Threat Intelligence Integration**: IOC matching, threat feed aggregation, reputation scoring
- **Network Monitoring**: NetFlow analysis, DNS monitoring, HTTP proxy log analysis, lateral movement detection
- **Endpoint Monitoring**: EDR integration, process creation monitoring, file integrity monitoring
- **Anomaly Detection**: Baseline behavior modeling, statistical anomaly detection, ML-based threat detection

## Usage Examples

```python
from security_monitoring import (
    LogParser,
    CorrelationEngine,
    AlertManager,
    DashboardBuilder,
    SIEMConnector,
)

# --- Log Parsing ---
parser = LogParser()
syslog_entry = parser.parse_syslog(
    "Jul  6 12:34:56 server1 sshd[12345]: Failed password for root from 192.168.1.100 port 22 ssh2"
)
print(f"Host: {syslog_entry.host}")
print(f"Service: {syslog_entry.service}")
print(f"Message: {syslog_entry.message}")
print(f"Source IP: {syslog_entry.extracted_fields.get('src_ip')}")

# --- Correlation Rules ---
engine = CorrelationEngine()
engine.add_sigma_rule({
    "title": "Brute Force SSH",
    "status": "experimental",
    "logsource": {"service": "sshd"},
    "detection": {
        "selection": {"message": "Failed password"},
        "condition": "selection | count() by src_ip > 10 within 5m",
    },
    "level": "high",
})
alerts = engine.evaluate(logs)
print(f"Correlation alerts: {len(alerts)}")

# --- Alert Management ---
alert_mgr = AlertManager()
alert = alert_mgr.create_alert(
    rule_name="SSH Brute Force",
    severity="high",
    source_ip="192.168.1.100",
    details={"attempts": 15, "target_user": "root"},
)
print(f"Alert ID: {alert.alert_id}")
print(f"Status: {alert.status}")

# --- SIEM Connector ---
splunk = SIEMConnector(platform="splunk")
splunk.connect(host="splunk.internal", port="8089")
results = splunk.query(
    'index=network sourcetype=firewall action=blocked | top src_ip | head 10'
)
print(f"Query results: {len(results)} entries")

# --- Dashboard ---
dashboard = DashboardBuilder("SOC Overview")
dashboard.add_panel(
    title="Alerts by Severity",
    type="pie_chart",
    query="index=alerts | stats count by severity",
)
dashboard.add_panel(
    title="Top Source IPs",
    type="bar_chart",
    query="index=alerts | top src_ip limit=20",
)
print(f"Dashboard panels: {len(dashboard.panels)}")
```

## Best Practices

- Implement defense-in-depth: combine network, endpoint, and application monitoring
- Use Sigma rules for vendor-agnostic detection logic, then convert to platform-specific queries
- Tune alert thresholds regularly to reduce false positive fatigue
- Enrich alerts with threat intelligence (GeoIP, reputation, WHOIS) automatically
- Maintain baseline behavior profiles for anomaly detection; review monthly
- Ensure log retention meets compliance requirements (PCI-DSS: 1 year, HIPAA: 6 years)
- Use correlation windows of 5-15 minutes for brute force detection
- Implement automated playbooks for high-confidence alerts to reduce response time
- Monitor for log gaps — a missing log source is a detection blind spot
- Regularly test detection rules against MITRE ATT&CK techniques

## Related Modules

- **soc-operations**: SOC workflow and incident handling
- **incident-response**: Response procedures triggered by monitoring alerts
- **threat-hunting**: Proactive threat detection beyond automated monitoring
- **digital-forensics**: Post-incident investigation from collected logs

## Advanced Configuration

### SIEM Platform Configuration

```yaml
# Splunk configuration
splunk:
  hec_url: "https://splunk.internal:8088"
  hec_token: "${SPLUNK_HEC_TOKEN}"
  index: "security"
  sourcetype: "json"
  batch_size: 1000
  flush_interval_ms: 5000

# Elastic SIEM configuration
elastic:
  hosts: ["https://elastic.internal:9200"]
  username: "${ELASTIC_USER}"
  password: "${ELASTIC_PASS}"
  index_pattern: "security-*"
  ilm_policy: "security-policy"
  template_name: "security-template"
```

### Correlation Rule Configuration

```yaml
# Sigma rule configuration
sigma:
  pipelines:
    - id: splunk_pipeline
      output: splunk
      config: splunk_config.yml
    - id: elastic_pipeline
      output: elastic
      config: elastic_config.yml
  backends:
    - type: splunk
      url: https://splunk.internal:8089
    - type: elasticsearch
      url: https://elastic.internal:9200
```

### Alert Tuning Configuration

```yaml
alert_tuning:
  thresholds:
    ssh_brute_force:
      count: 10
      window_minutes: 5
      severity: high
    failed_login:
      count: 5
      window_minutes: 10
      severity: medium
    port_scan:
      unique_ports: 20
      window_minutes: 5
      severity: high
  suppression:
    enabled: true
    rules:
      - rule: "duplicate_alert"
        suppress_fields: ["src_ip", "rule_name"]
        suppress_duration_minutes: 30
```

## Architecture Patterns

### Security Monitoring Architecture

```
Data Sources:
├── Network
│   ├── Firewall logs
│   ├── IDS/IPS alerts
│   ├── NetFlow data
│   ├── DNS logs
│   └── Proxy logs
├── Endpoint
│   ├── EDR telemetry
│   ├── Windows Event Logs
│   ├── Sysmon logs
│   └── File integrity monitoring
├── Application
│   ├── Web server logs
│   ├── Application logs
│   ├── Database audit logs
│   └── API access logs
├── Identity
│   ├── Active Directory logs
│   ├── SSO/IAM logs
│   └── VPN logs
└── Cloud
    ├── CloudTrail/Activity Log
    ├── VPC Flow Logs
    └── S3 access logs

Collection Layer:
├── Log Collectors (Fluentd, Logstash)
├── API Pollers
├── Agent-based (OSSEC, Wazuh)
└── Network TAPs

Processing Layer:
├── Normalization
├── Enrichment (GeoIP, Threat Intel)
├── Deduplication
└── Correlation Engine

Storage Layer:
├── Hot (7 days, SSD)
├── Warm (30 days, HDD)
├── Cold (1 year, Archive)
└── Frozen (7+ years, Glacier)

Analysis Layer:
├── Real-time correlation
├── Historical queries
├── ML anomaly detection
└── Threat hunting

Visualization Layer:
├── Dashboards
├── Alerts
├── Reports
└── Executive views
```

### Alert Processing Pipeline

```
Raw Events → Normalization → Enrichment → Correlation → Alert → Triage → Response
    │              │              │              │          │         │         │
    └── Parse      └── Standardize └── Add context └── Pattern └── Create └── Analyst └── Action
```

## Integration Guide

### Splunk Integration

```python
from security_monitoring import SplunkConnector

splunk = SplunkConnector(
    host="splunk.internal",
    port=8089,
    token="${SPLUNK_HEC_TOKEN}",
    verify_ssl=True,
)

# Execute SPL query
results = splunk.query(
    'index=network sourcetype=firewall action=blocked | stats count by src_ip | sort -count | head 20'
)
for row in results:
    print(f"{row['src_ip']}: {row['count']} blocked connections")

# Send events to Splunk
splunk.send_event(
    index="security",
    source="firewall",
    event={"src_ip": "10.0.0.1", "action": "blocked", "port": 443},
)
```

### Elastic SIEM Integration

```python
from security_monitoring import ElasticConnector

elastic = ElasticConnector(
    hosts=["https://elastic.internal:9200"],
    username="${ELASTIC_USER}",
    password="${ELASTIC_PASS}",
)

# Execute KQL query
results = elastic.query_kql(
    index="security-*",
    query='event.kind: "alert" and event.severity: 3',
    size=50,
)
print(f"Alerts found: {results.total}")

# Create detection rule
elastic.create_rule(
    name="SSH Brute Force",
    query='event.dataset: "auth.ssh" and event.outcome: "failure"',
    severity="high",
    interval="5m",
)
```

### Sigma Rule Deployment

```python
from security_monitoring import SigmaDeployment

deployer = SigmaDeployment()
deployer.deploy_rules(
    rule_directory="./sigma_rules",
    targets=["splunk", "elastic", "sentinel"],
    config_path="./sigma_config.yml",
)
```

## Performance Optimization

### Query Optimization

| Technique | Description | Impact |
|-----------|-------------|--------|
| Index filtering | Restrict time range | 10-100x faster |
| Field selection | Return only needed fields | 2-5x faster |
| Pre-aggregation | Summary tables | 50-100x faster |
| Parallel execution | Multi-threaded queries | 2-4x faster |
| Cache warming | Pre-load hot data | 5-10x faster |

### Log Volume Management

```
Strategy:
├── Filtering at source (reduce noise)
│   ├── Drop verbose debug logs
│   ├── Sample high-volume events
│   └── Aggregate similar events
├── Tiered storage
│   ├── Hot: 7 days SSD
│   ├── Warm: 30 days HDD
│   ├── Cold: 1 year archive
│   └── Frozen: 7+ years compliance
└── Compression
    ├── Zstandard for hot/warm
    ├── gzip for cold
    └── Raw for frozen
```

### Dashboard Performance

```python
from security_monitoring import DashboardOptimizer

optimizer = DashboardOptimizer()
optimizer.optimize(
    dashboard_id="soc-overview",
    techniques=[
        "reduce_time_range",
        "add_field_selection",
        "enable_caching",
        "precompute_summaries",
    ],
)
print(f"Load time: {optimizer.original_load_time}s → {optimizer.optimized_load_time}s")
```

## Security Considerations

### Monitoring Infrastructure Security

| Component | Risk | Mitigation |
|-----------|------|------------|
| SIEM Server | Privileged access | MFA, least privilege, audit logs |
| Log Sources | Log tampering | Signed logs, tamper detection |
| API Access | Credential theft | API keys with expiry, IP allowlist |
| Dashboards | Information disclosure | Role-based access control |
| Correlation Rules | Rule bypass | Version control, change management |

### Data Protection

```
Sensitive Data Handling:
├── PII in logs → Mask/hash before storage
├── Credentials → Never log; use vault references
├── Financial data → Encrypt at rest and in transit
├── Health data → HIPAA compliance requirements
└── Card data → PCI-DSS masking requirements
```

### Access Control Matrix

| Role | Read Logs | Create Rules | Manage Alerts | Delete Data |
|------|-----------|-------------|---------------|-------------|
| Analyst L1 | Yes (assigned) | No | Acknowledge | No |
| Analyst L2 | Yes (all) | Yes | Yes | No |
| Analyst L3 | Yes (all) | Yes | Yes | Archive only |
| Admin | Yes (all) | Yes | Yes | Yes (with approval) |

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Log Gaps | Missing events in time range | Check collector health, network |
| High Latency | Slow query results | Optimize queries, add indexes |
| Alert Storm | Too many alerts firing | Tune thresholds, add suppression |
| Data Loss | Events not appearing | Check retention policy, disk space |
| Correlation Failures | Rules not matching | Verify field mapping, test regex |

### Debugging Correlation Rules

```bash
# Test Sigma rule against sample data
sigma check sigma_rules/brute_force.yml
sigma convert -t splunk sigma_rules/brute_force.yml

# Validate Splunk SPL
splunk search 'index=security | head 10' -auth admin:password

# Test Elastic query
curl -X GET "https://elastic:9200/security-*/_search" \
  -H "Content-Type: application/json" \
  -d '{"query": {"match_all": {}}}'
```

### Log Source Health Check

```python
from security_monitoring import LogSourceHealth

health = LogSourceHealth()
for source in health.check_all():
    status = "OK" if source.healthy else "DEGRADED"
    gap = source.last_event_gap_minutes
    print(f"[{status}] {source.name}: {gap:.0f}min since last event")
```

## API Reference

### LogParser

```python
class LogParser:
    def parse_syslog(message: str) -> SyslogEntry:
        """Parse syslog message into structured fields."""
    
    def parse_windows_event(xml: str) -> WindowsEvent:
        """Parse Windows Event Log XML."""
    
    def parse_json(message: str) -> dict:
        """Parse JSON-structured log."""
    
    def normalize(source_type: str, raw: str) -> NormalizedEvent:
        """Normalize event to standard schema."""

class SyslogEntry:
    timestamp: datetime
    host: str
    service: str
    pid: int
    message: str
    extracted_fields: dict
```

### CorrelationEngine

```python
class CorrelationEngine:
    def add_sigma_rule(rule: dict) -> None:
        """Add Sigma correlation rule."""
    
    def add_spl_query(name: str, query: str) -> None:
        """Add Splunk SPL detection rule."""
    
    def add_kql_query(name: str, query: str) -> None:
        """Add Elastic KQL detection rule."""
    
    def evaluate(events: list[dict]) -> list[Alert]:
        """Evaluate rules against event stream."""
```

### AlertManager

```python
class AlertManager:
    def create_alert(
        rule_name: str,
        severity: str,
        source_ip: str,
        details: dict,
    ) -> Alert:
        """Create new security alert."""
    
    def deduplicate(alert: Alert) -> bool:
        """Check if alert is duplicate."""
    
    def enrich(alert: Alert) -> Alert:
        """Enrich alert with threat intel."""
    
    def escalate(alert: Alert, escalation_path: str) -> None:
        """Escalate alert to appropriate team."""

class Alert:
    alert_id: str
    rule_name: str
    severity: str
    status: str
    source_ip: str
    created_at: datetime
    updated_at: datetime
    details: dict
    enrichment: dict
```

## Data Models

### NormalizedEvent

```
NormalizedEvent:
  timestamp: datetime
  source: str
  source_type: str
  event_type: str
  severity: str
  src_ip: str
  dst_ip: str
  src_port: int
  dst_port: int
  protocol: str
  user: str
  action: str
  outcome: str
  raw_message: str
  fields: dict
```

### DetectionRule

```
DetectionRule:
  rule_id: str
  name: str
  description: str
  severity: str
  mitre_technique: str
  query: str
  query_language: str
  enabled: bool
  false_positive_rate: float
  last_triggered: datetime
  trigger_count: int
```

### LogSource

```
LogSource:
  source_id: str
  name: str
  type: str
  enabled: bool
  last_event_time: datetime
  events_per_second: float
  health_status: str
  error_count: int
  retention_days: int
```

## Deployment Guide

### SIEM Deployment Steps

```
1. Planning
   ├── Define log sources and retention
   ├── Size infrastructure (CPU, RAM, storage)
   ├── Plan network architecture
   └── Define access controls

2. Installation
   ├── Deploy SIEM platform
   ├── Configure storage tiers
   ├── Set up collectors
   └── Enable SSL/TLS

3. Configuration
   ├── Import log sources
   ├── Create normalization rules
   ├── Deploy detection rules
   └── Set up dashboards

4. Validation
   ├── Test log ingestion
   ├── Verify correlation rules
   ├── Validate alert routing
   └── Confirm dashboard data

5. Go-Live
   ├── Enable monitoring
   ├── Train analysts
   ├── Document procedures
   └── Schedule reviews
```

## Monitoring & Observability

### SIEM Health Metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Ingestion Rate | >10K EPS | <5K EPS |
| Query Latency | <5s P95 | >15s P95 |
| Storage Used | <80% capacity | >85% capacity |
| Index Lag | <1 minute | >5 minutes |
| Rule Execution | <1s | >5s |
| Alert Queue | <100 pending | >500 pending |

### Monitoring Dashboards

```
SOC Overview Dashboard:
├── Alert volume by severity
├── Mean time to detect (MTTD)
├── Mean time to respond (MTTR)
├── Top alert types
├── Analyst workload
└── Trend lines (7d, 30d)

Infrastructure Dashboard:
├── Log ingestion rates
├── Storage utilization
├── Query performance
├── Collector health
├── Error rates
└── Capacity forecasting
```

## Testing Strategy

### Detection Testing

```
1. Rule Validation
   ├── Test against known-good data (FP check)
   ├── Test against known-bad data (TP check)
   ├── Performance testing (latency)
   └── Volume testing (scale)

2. Red Team Validation
   ├── Execute MITRE ATT&CK techniques
   ├── Verify detection triggers
   ├── Measure detection time
   └── Document coverage gaps

3. Regression Testing
   ├── Run rules against historical data
   ├── Compare alert volumes
   ├── Identify new false positives
   └── Verify no false negatives
```

## Versioning & Migration

### Rule Versioning

```
v2.0.0: Major rule updates (breaking changes in query syntax)
v1.x.0: New rules added
v1.0.x: Rule tuning and false positive fixes
```

### Migration Checklist

- [ ] Export existing rules
- [ ] Map fields to new schema
- [ ] Test rules in staging
- [ ] Validate alert routing
- [ ] Deploy to production
- [ ] Monitor for 48 hours
- [ ] Update documentation

## Glossary

| Term | Definition |
|------|-----------|
| EPS | Events Per Second — log ingestion rate |
| SIEM | Security Information and Event Management |
| SOC | Security Operations Center |
| Sigma | Vendor-agnostic detection rule format |
| MTTD | Mean Time to Detect |
| MTTR | Mean Time to Respond |
| FP Rate | False Positive Rate |
| ATT&CK | Adversarial Tactics, Techniques, and Common Knowledge |
| IOC | Indicator of Compromise |
| IOB | Indicator of Behavior |
| Correlation | Linking multiple events to detect complex attacks |

## Changelog

### 2.0.0 (2024-12-01)
- Added multi-SIEM support (Splunk, Elastic, Sentinel)
- Added Sigma rule pipeline
- Improved correlation engine performance
- Added ML-based anomaly detection

### 1.2.0 (2024-08-15)
- Added alert deduplication
- Added threat intelligence enrichment
- Improved dashboard builder

### 1.1.0 (2024-05-20)
- Added Windows Event Log parsing
- Added Sigma rule authoring
- Added SIEM health monitoring

### 1.0.0 (2024-02-01)
- Initial release with basic log parsing
- Splunk integration
- Simple correlation rules
- Basic dashboarding

## Contributing Guidelines

### Adding New Detection Rules

1. Create Sigma rule YAML
2. Add test cases (positive and negative)
3. Document MITRE ATT&CK mapping
4. Submit PR with false positive analysis
5. Include performance benchmarks

### Code Quality

- Type hints on all public functions
- Unit tests for parsers and normalizers
- Integration tests with mock SIEM
- Documentation for new connectors

## License

MIT License

Copyright (c) 2024 Security Monitoring Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
