# Security Monitoring Agent

## Overview

The **Security Monitoring Agent** provides comprehensive security operations capabilities including log collection, SIEM correlation, alert management, threat intelligence integration, and incident response coordination. This agent enables organizations to detect, investigate, and respond to security threats in real-time.

## Core Capabilities

### 1. Log Collection
Gather and normalize security logs:
- **Syslog Collection**: Unix/Linux system logs
- **Windows Events**: Security and system logs
- **Cloud Trails**: AWS CloudTrail, Azure Activity
- **Firewall Logs**: Network security appliances
- **Application Logs**: Web servers, databases
- **Custom Sources**: API and file-based inputs

### 2. SIEM Correlation
Analyze and correlate security events:
- **Event Correlation**: Find related events
- **Anomaly Detection**: Identify unusual patterns
- **Behavioral Baselines**: Establish normal behavior
- **Rule-based Detection**: Pattern matching
- **Machine Learning**: Advanced threat detection

### 3. Alert Management
Manage security alerts lifecycle:
- **Alert Creation**: Generate from correlations
- **Triage**: Prioritize and assign
- **Investigation**: Track analysis progress
- **Escalation**: Define escalation paths
- **SLA Tracking**: Monitor response times

### 4. Threat Intelligence
Integrate external threat data:
- **IP Reputation**: Check IP against feeds
- **Domain Analysis**: Domain lookups
- **File Hash Analysis**: Hash reputation
- **IOC Matching**: Indicators of compromise
- **Feed Integration**: Multiple intelligence sources

### 5. Incident Response
Coordinate incident handling:
- **Incident Creation**: Open from alerts
- **Timeline Tracking**: Document actions
- **Evidence Collection**: Track artifacts
- **Report Generation**: Closure documentation
- **Lessons Learned**: Improvement tracking

## Usage Examples

### Log Collection

```python
from security_monitoring import LogCollector

collector = LogCollector()
syslog = collector.collect_syslog(
    "Jan 15 10:30:45 server sshd[1234]: Accepted publickey for admin",
    "sshd"
)
print(f"Message: {syslog['normalized']['message']}")

windows = collector.collect_windows_event(
    {'IpAddress': '192.168.1.100'},
    event_code=4625
)
print(f"Event: {windows['event_type']}")

cloud = collector.collect_cloud_trail({
    'eventName': 'CreateUser',
    'eventSource': 'iam.amazonaws.com',
    'eventTime': '2024-01-15T10:30:00Z'
})
print(f"AWS Event: {cloud['event_name']}")
```

### Event Correlation

```python
from security_monitoring import SIEMAnalyzer, SecurityEvent, AlertSeverity

siem = SIEMAnalyzer()

rule = siem.add_correlation_rule(
    name="Failed Login Spike",
    conditions=[{'event_type': 'authentication', 'result': 'failed'}],
    time_window=300
)
print(f"Rule added: {rule['name']}")

events = [
    SecurityEvent(
        id="EVT-001", timestamp=datetime.now(), source=LogSource.APPLICATION,
        event_type="authentication", severity=AlertSeverity.MEDIUM,
        source_ip="10.10.10.50", destination_ip="192.168.1.10",
        user="admin", description="Failed login attempt", raw_log={}, indicators=[], correlated=False
    )
]

alerts = siem.correlate_events(events)
print(f"Alerts generated: {len(alerts)}")

baseline = siem.create_behavior_baseline(events, days=30)
print(f"Users in baseline: {baseline['unique_users']}")
```

### Alert Management

```python
from security_monitoring import AlertManager, AlertSeverity, AlertStatus

alerts = AlertManager()
alert = alerts.create_alert(
    title="Potential Brute Force Attack",
    severity=AlertSeverity.HIGH,
    description="Multiple failed login attempts detected",
    affected_assets=["192.168.1.100"]
)
print(f"Alert created: {alert.id}")

result = alerts.triage_alert(alert.id, "analyst@company.com", "Confirmed suspicious activity")
print(f"Triage result: {result['status']}")

escalation = alerts.get_escalation_path(alert)
for level in escalation:
    print(f"Level {level['level']}: {level['team']} - {level['max_response_minutes']} minutes")
```

### Threat Intelligence

```python
from security_monitoring import ThreatIntelligence

intel = ThreatIntelligence()

ip = intel.lookup_ip("185.220.101.46")
print(f"IP Reputation: {ip['reputation']}")
print(f"Threat Type: {ip['threat_type']}")
print(f"Sources: {', '.join(ip['sources'])}")

domain = intel.lookup_domain("malicious-domain.com")
print(f"Domain Status: {domain['reputation']}")

hash_info = intel.lookup_hash("e3b0c44298fc1c149afbf4c8996fb924")
print(f"Detection: {hash_info['detection_name']}")
```

### Incident Response

```python
from security_monitoring import IncidentResponse, AlertSeverity

incident = IncidentResponse()

inc = incident.create_incident(
    title="Suspected Data Breach",
    severity=AlertSeverity.CRITICAL,
    description="Customer data accessed from unusual location"
)
print(f"Incident created: {inc['id']}")

incident.add_incident_action(inc['id'], "Isolated affected systems", "analyst")
incident.add_incident_action(inc['id'], "Collected memory dumps", "forensics")

report = incident.generate_incident_report(inc['id'])
print(f"Duration: {report['duration']}")
print(f"Root Cause: {report['root_cause']}")
```

## Security Operations Center (SOC) Framework

### SOC Maturity Levels

| Level | Description | Key Capabilities |
|-------|-------------|------------------|
| Level 1 | Reactive | Basic monitoring, manual processes |
| Level 2 | Proactive | Alert correlation, defined processes |
| Level 3 | Advanced | Automated detection, threat intelligence |
| Level 4 | Managed | Predictive analysis, Red Team integration |
| Level 5 | Optimizing | AI-driven, self-healing systems |

### Alert Severity Levels

| Severity | Response Time | Examples |
|----------|---------------|----------|
| Critical | 15 minutes | Active breach, ransomware |
| High | 1 hour | Exploitation attempt, data exfiltration |
| Medium | 4 hours | Vulnerability scan, suspicious activity |
| Low | 24 hours | Policy violation, minor anomalies |

### NIST Incident Response Phases

```
┌─────────────────────────────────────────────────────────┐
│              Incident Response Lifecycle                 │
├─────────────────────────────────────────────────────────┤
│  1. Preparation → 2. Detection → 3. Analysis            │
│         │              │              │                  │
│  6. Recovery ← 5. Containment ← 4. Investigation        │
│         │              │              │                  │
│         └──────────────┴──────────────┘
└─────────────────────────────────────────────────────────┘
```

## Detection Rules

### Network-Based Detection

| Rule | Description | Severity |
|------|-------------|----------|
| BRUTE_FORCE_SSH | >5 failed SSH logins in 5 min | High |
| PORT_SCAN | >10 ports scanned in 1 min | Medium |
| C2_COMMUNICATION | Known C2 protocol detected | Critical |
| DATA_EXFIL | Large outbound transfer | Critical |
| DNS_TUNNELING | Abnormal DNS traffic | High |

### Endpoint-Based Detection

| Rule | Description | Severity |
|------|-------------|----------|
| MALWARE_DETECTED | Known malware signature | Critical |
| SUSPICIOUS_PROCESS | Abnormal process behavior | High |
| PRIVILEGE_ESCALATION | Attempted privilege elevation | Critical |
| PERSISTENCE_MOD | New startup item or service | High |
| CREDENTIAL_DUMP | LSASS access attempt | Critical |

### Cloud-Based Detection

| Rule | Description | Severity |
|------|-------------|----------|
| IAM_POLICY_CHANGE | Sensitive IAM policy modified | High |
| NEW_USER_CREATED | New privileged user created | Critical |
| UNUSUAL_API_CALL | API call from new location | Medium |
| S3_PUBLIC | Bucket made publicly accessible | High |
| CRYPTOMINING | Cryptocurrency mining activity | High |

## Threat Intelligence Sources

### Open Source Feeds

| Feed | Type | Update Frequency |
|------|------|------------------|
| AlienVault OTX | IP, Domain, Hash | Hourly |
| VirusTotal | File, URL, IP | Real-time |
| AbuseIPDB | IP | Hourly |
| ThreatFox | IOC Database | Daily |
| MISP | Community IOCs | Varies |

### Commercial Feeds

| Provider | Coverage | Integration |
|----------|----------|-------------|
| Recorded Future | Enterprise | API |
| CrowdStrike | Endpoint | Falcon API |
| Mandiant | APT Groups | Advantage |
| Palo Alto | WildFire | AutoFocus |

## Metrics and KPIs

### Detection Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| MTTD | < 24 hours | Mean time to detect |
| MTTI | < 1 hour | Mean time to investigate |
| MTTR | < 4 hours | Mean time to respond |
| False Positive Rate | < 10% | Invalid alerts |
| Alert Coverage | > 95% | Log sources monitored |

### Operational Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Analyst Utilization | < 80% | Alert processing capacity |
| Escalation Rate | < 20% | Alerts escalated to L2+ |
| Closure Rate | > 95% | Alerts resolved within SLA |
| Threat Hunt Frequency | Weekly | Proactive hunting |

## SIEM Architecture

### Log Flow

```
Data Sources → Collectors → Processors → Storage → Analytics → Alerts
                                    ↓
                            Long-term Storage
                                    ↓
                            Reporting & Forensics
```

### Correlation Techniques

1. **Sequential Correlation**: Event A followed by Event B
2. **Threshold Correlation**: Count exceeds threshold
3. **Pattern Correlation**: Specific sequence of events
4. **Statistical Correlation**: Statistical anomaly detection
5. **ML-based Correlation**: Machine learning patterns

## Incident Types

### Classification

| Category | Description | Example |
|----------|-------------|---------|
| Malware | Malicious software infection | Ransomware outbreak |
| Phishing | Social engineering attack | Credential theft |
| DDoS | Service disruption | Network flooding |
| Data Breach | Unauthorized data access | Customer data exfil |
| Insider Threat | Internal actor misuse | Data theft |
| Vulnerability | Exploitable weakness | SQL injection |

### Severity Assessment

| Factor | Weight | Considerations |
|--------|--------|----------------|
| Data Sensitivity | 40% | PII, financial, health data |
| Impact Scope | 30% | Systems, users affected |
| Attacker Capability | 20% | Sophistication, persistence |
| Recovery Complexity | 10% | Time to restore |

## Best Practices

### Monitoring

1. **Comprehensive Coverage**: Log all critical systems
2. **Centralized Collection**: Aggregate in SIEM
3. **Real-time Processing**: Minimize detection delay
4. **Baseline Development**: Understand normal behavior
5. **Regular Tuning**: Reduce false positives

### Alert Management

1. **Clear Triage Process**: Defined workflows
2. **Proper Escalation**: Defined paths and SLAs
3. **Documentation**: Track all actions
4. **Post-Incident Review**: Continuous improvement
5. **Automation**: Automate repetitive tasks

### Incident Response

1. **Preparedness**: Documented playbooks
2. **Trained Team**: Regular exercises
3. **Clear Communication**: Stakeholder updates
4. **Evidence Preservation**: Chain of custody
5. **Lessons Learned**: After-action reviews

## Related Skills

- [Vulnerability Assessment](./../security-assessment/vulnerability-assessment/resources/GROK.md) - Finding vulnerabilities
- [Penetration Testing](./../red-team/penetration-testing/resources/GROK.md) - Testing security
- [Threat Modeling](./../security/threat-modeling/resources/GROK.md) - Proactive identification
- [Secure Coding](./../security/secure-coding/resources/GROK.md) - Prevention through development

---

**File Path**: `skills/blue-team/security-monitoring/resources/security_monitoring.py`
