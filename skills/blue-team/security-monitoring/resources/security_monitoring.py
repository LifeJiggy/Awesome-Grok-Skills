from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json


class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class LogSource(Enum):
    FIREWALL = "firewall"
    IDS_IPS = "ids_ips"
    ENDPOINT = "endpoint"
    APPLICATION = "application"
    NETWORK = "network"
    CLOUD = "cloud"
    AUTHENTICATION = "authentication"


@dataclass
class SecurityEvent:
    id: str
    timestamp: datetime
    source: LogSource
    event_type: str
    severity: AlertSeverity
    source_ip: Optional[str]
    destination_ip: Optional[str]
    user: Optional[str]
    description: str
    raw_log: Dict
    indicators: List[str]
    correlated: bool


@dataclass
class Alert:
    id: str
    title: str
    severity: AlertSeverity
    status: AlertStatus
    created_at: datetime
    events: List[str]
    affected_assets: List[str]
    description: str
    investigation_notes: List[str]
    remediation: str
    assigned_to: Optional[str]
    resolved_at: Optional[datetime]


class LogCollector:
    """Collect and normalize security logs"""
    
    def __init__(self):
        self.log_buffer = []
        self.sources = {}
    
    def collect_syslog(self, log_line: str, source: str = "unknown") -> Dict:
        """Parse and normalize syslog entry"""
        return {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'format': 'syslog',
            'raw': log_line,
            'normalized': {
                'facility': 'local0',
                'severity': 'INFO',
                'hostname': 'server01',
                'process': 'sshd',
                'message': 'Accepted publickey for user'
            }
        }
    
    def collect_windows_event(self,
                             event_data: Dict,
                             event_code: int) -> Dict:
        """Parse Windows event log"""
        event_mapping = {
            4624: {'type': 'Authentication', 'description': 'Successful logon'},
            4625: {'type': 'Authentication', 'description': 'Failed logon'},
            4688: {'type': 'Process', 'description': 'New process created'},
            4698: {'type': 'Scheduled Task', 'description': 'Scheduled task created'},
            4104: {'type': 'PowerShell', 'description': 'Script block logging'}
        }
        return {
            'timestamp': datetime.now().isoformat(),
            'source': 'windows',
            'event_code': event_code,
            'event_type': event_mapping.get(event_code, {}).get('type', 'Unknown'),
            'description': event_mapping.get(event_code, {}).get('description', 'N/A'),
            'data': event_data
        }
    
    def collect_cloud_trail(self, event: Dict) -> Dict:
        """Parse AWS CloudTrail event"""
        return {
            'timestamp': event.get('eventTime'),
            'source': 'aws',
            'event_name': event.get('eventName'),
            'event_source': event.get('eventSource'),
            'aws_region': event.get('awsRegion'),
            'source_ip': event.get('sourceIPAddress'),
            'user_agent': event.get('userAgent'),
            'user_identity': event.get('userIdentity', {}),
            'request_parameters': event.get('requestParameters'),
            'response_elements': event.get('responseElements')
        }
    
    def collect_firewall_log(self,
                            log_entry: Dict) -> Dict:
        """Parse firewall log entry"""
        return {
            'timestamp': log_entry.get('timestamp'),
            'source': 'firewall',
            'action': log_entry.get('action'),
            'source_ip': log_entry.get('src_ip'),
            'destination_ip': log_entry.get('dst_ip'),
            'source_port': log_entry.get('src_port'),
            'destination_port': log_entry.get('dst_port'),
            'protocol': log_entry.get('protocol'),
            'bytes_sent': log_entry.get('bytes_sent'),
            'bytes_received': log_entry.get('bytes_rcvd'),
            'packets': log_entry.get('packets')
        }
    
    def normalize_event(self, raw_event: Dict, source_type: LogSource) -> SecurityEvent:
        """Normalize event to standard format"""
        return SecurityEvent(
            id=f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hash(raw_event) % 1000:03d}",
            timestamp=datetime.now(),
            source=source_type,
            event_type=raw_event.get('type', 'unknown'),
            severity=self._calculate_severity(raw_event),
            source_ip=raw_event.get('source_ip'),
            destination_ip=raw_event.get('destination_ip'),
            user=raw_event.get('user'),
            description=raw_event.get('description', ''),
            raw_log=raw_event,
            indicators=self._extract_indicators(raw_event),
            correlated=False
        )
    
    def _calculate_severity(self, event: Dict) -> AlertSeverity:
        """Calculate event severity"""
        event_type = event.get('type', '').lower()
        if 'failed' in event_type or 'unauthorized' in event_type:
            return AlertSeverity.MEDIUM
        elif 'malware' in event_type or 'ransomware' in event_type:
            return AlertSeverity.CRITICAL
        elif 'brute' in event_type or 'attack' in event_type:
            return AlertSeverity.HIGH
        return AlertSeverity.INFO
    
    def _extract_indicators(self, event: Dict) -> List[str]:
        """Extract IOCs from event"""
        indicators = []
        if 'ip' in event.get('source_ip', ''):
            indicators.append(f"IP: {event['source_ip']}")
        if 'domain' in event.get('description', '').lower():
            indicators.append("Domain mentioned")
        if 'hash' in event:
            indicators.append(f"Hash: {event['hash']}")
        return indicators


class SIEMAnalyzer:
    """Security Information and Event Management"""
    
    def __init__(self):
        self.correlation_rules = []
        self.alerts = []
    
    def add_correlation_rule(self,
                            name: str,
                            conditions: List[Dict],
                            time_window: int = 300) -> Dict:
        """Add correlation rule"""
        rule = {
            'name': name,
            'conditions': conditions,
            'time_window_seconds': time_window,
            'enabled': True
        }
        self.correlation_rules.append(rule)
        return rule
    
    def correlate_events(self,
                        events: List[SecurityEvent],
                        rules: List[Dict] = None) -> List[Alert]:
        """Correlate events into alerts"""
        alerts = []
        
        brute_force = [e for e in events if 'failed' in e.description.lower()]
        if len(brute_force) >= 5:
            alert = Alert(
                id=f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                title="Potential Brute Force Attack Detected",
                severity=AlertSeverity.HIGH,
                status=AlertStatus.NEW,
                created_at=datetime.now(),
                events=[e.id for e in brute_force],
                affected_assets=[e.destination_ip for e in brute_force if e.destination_ip],
                description=f"Detected {len(brute_force)} failed login attempts",
                investigation_notes=[],
                remediation="Block source IP, reset affected accounts",
                assigned_to=None,
                resolved_at=None
            )
            alerts.append(alert)
        
        data_exfiltration = [e for e in events if 'large' in e.description.lower() and 'upload' in e.description.lower()]
        if len(data_exfiltration) > 0:
            alert = Alert(
                id=f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                title="Potential Data Exfiltration Detected",
                severity=AlertSeverity.CRITICAL,
                status=AlertStatus.NEW,
                created_at=datetime.now(),
                events=[e.id for e in data_exfiltration],
                affected_assets=[e.source_ip for e in data_exfiltration if e.source_ip],
                description=f"Detected large data upload events",
                investigation_notes=[],
                remediation="Investigate source, block transfer if unauthorized",
                assigned_to=None,
                resolved_at=None
            )
            alerts.append(alert)
        
        return alerts
    
    def detect_anomalies(self,
                        events: List[SecurityEvent],
                        baseline: Dict = None) -> List[Dict]:
        """Detect anomalous behavior"""
        anomalies = []
        
        hourly_volume = {}
        for event in events:
            hour = event.timestamp.hour
            hourly_volume[hour] = hourly_volume.get(hour, 0) + 1
        
        if baseline:
            for hour, count in hourly_volume.items():
                expected = baseline.get('hourly', {}).get(str(hour), count)
                if count > expected * 3:
                    anomalies.append({
                        'type': 'volume_spike',
                        'hour': hour,
                        'actual': count,
                        'expected': expected,
                        'deviation': f"{(count/expected - 1) * 100:.0f}%"
                    })
        
        return anomalies
    
    def create_behavior_baseline(self,
                                 events: List[SecurityEvent],
                                 days: int = 30) -> Dict:
        """Create behavioral baseline"""
        hourly_pattern = {}
        for event in events:
            hour = event.timestamp.hour
            hourly_pattern[hour] = hourly_pattern.get(hour, 0) + 1
        
        user_patterns = {}
        for event in events:
            if event.user:
                if event.user not in user_patterns:
                    user_patterns[event.user] = {'events': 0, 'ips': set()}
                user_patterns[event.user]['events'] += 1
                if event.source_ip:
                    user_patterns[event.user]['ips'].add(event.source_ip)
        
        return {
            'period_days': days,
            'hourly_pattern': hourly_pattern,
            'unique_users': len(user_patterns),
            'user_patterns': {k: {'events': v['events'], 'unique_ips': len(v['ips'])} for k, v in user_patterns.items()}
        }


class AlertManager:
    """Manage security alerts"""
    
    def __init__(self):
        self.alert_queue = []
    
    def create_alert(self,
                     title: str,
                     severity: AlertSeverity,
                     description: str,
                     affected_assets: List[str] = None) -> Alert:
        """Create new alert"""
        alert = Alert(
            id=f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            title=title,
            severity=severity,
            status=AlertStatus.NEW,
            created_at=datetime.now(),
            events=[],
            affected_assets=affected_assets or [],
            description=description,
            investigation_notes=[],
            remediation="Investigate and remediate",
            assigned_to=None,
            resolved_at=None
        )
        self.alert_queue.append(alert)
        return alert
    
    def triage_alert(self,
                    alert_id: str,
                    analyst: str,
                    decision: str) -> Dict:
        """Triage and assign alert"""
        for alert in self.alert_queue:
            if alert.id == alert_id:
                alert.status = AlertStatus.INVESTIGATING
                alert.assigned_to = analyst
                alert.investigation_notes.append(f"[{datetime.now().isoformat()}] Triage by {analyst}: {decision}")
                return {'status': 'updated', 'alert': alert.id}
        return {'status': 'not_found'}
    
    def update_alert(self,
                    alert_id: str,
                    status: AlertStatus,
                    notes: str = None) -> Alert:
        """Update alert status"""
        for alert in self.alert_queue:
            if alert.id == alert_id:
                alert.status = status
                if notes:
                    alert.investigation_notes.append(f"[{datetime.now().isoformat()}] {notes}")
                if status == AlertStatus.RESOLVED:
                    alert.resolved_at = datetime.now()
                return alert
        return None
    
    def get_escalation_path(self, alert: Alert) -> List[Dict]:
        """Get escalation path for alert"""
        escalation = [
            {'level': 1, 'team': 'L1 Security Analyst', 'time': '15 minutes'},
            {'level': 2, 'team': 'L2 Security Analyst', 'time': '1 hour'},
            {'level': 3, 'team': 'Security Manager', 'time': '4 hours'},
            {'level': 4, 'team': 'CISO', 'time': '24 hours'}
        ]
        
        severity_times = {
            AlertSeverity.CRITICAL: [15, 60, 240, 1440],
            AlertSeverity.HIGH: [30, 120, 480, 2880],
            AlertSeverity.MEDIUM: [60, 240, 1440, 5760],
            AlertSeverity.LOW: [120, 480, 2880, 10080]
        }
        
        times = severity_times.get(alert.severity, severity_times[AlertSeverity.MEDIUM])
        
        return [
            {**escalation[i], 'max_response_minutes': times[i]}
            for i in range(len(escalation))
        ]
    
    def generate_sla_report(self,
                            start_date: datetime,
                            end_date: datetime) -> Dict:
        """Generate SLA compliance report"""
        alerts = [a for a in self.alert_queue if start_date <= a.created_at <= end_date]
        
        resolved = [a for a in alerts if a.status == AlertStatus.RESOLVED]
        breached = []
        
        for alert in resolved:
            if alert.resolved_at:
                resolution_time = (alert.resolved_at - alert.created_at).total_seconds() / 60
                max_time = {'critical': 60, 'high': 240, 'medium': 480, 'low': 1440}
                if resolution_time > max_time.get(alert.severity.value, 480):
                    breached.append(alert.id)
        
        return {
            'period': f"{start_date.date()} to {end_date.date()}",
            'total_alerts': len(alerts),
            'resolved': len(resolved),
            'breached': len(breached),
            'resolution_rate': f"{(len(resolved)/len(alerts)*100):.1f}%" if alerts else "N/A",
            'sla_compliance': f"{((len(resolved)-len(breached))/len(resolved)*100):.1f}%" if resolved else "N/A"
        }


class ThreatIntelligence:
    """Threat intelligence integration"""
    
    def __init__(self):
        self.feeds = []
        self.ioc_database = {}
    
    def add_threat_feed(self,
                       feed_name: str,
                       feed_type: str,
                       update_frequency: str = "hourly") -> Dict:
        """Add threat intelligence feed"""
        feed = {
            'name': feed_name,
            'type': feed_type,
            'update_frequency': update_frequency,
            'last_updated': datetime.now().isoformat(),
            'records': 0
        }
        self.feeds.append(feed)
        return feed
    
    def lookup_ip(self, ip: str) -> Dict:
        """Look up IP in threat intelligence"""
        return {
            'ip': ip,
            'reputation': 'malicious',
            'threat_type': 'C2 Server',
            'first_seen': '2024-01-01',
            'last_seen': '2024-01-15',
            'sources': ['AlienVault', 'VirusTotal', 'ThreatFox'],
            'campaigns': ['APT29', 'TrickBot'],
            'tags': ['c2', 'malware', 'botnet']
        }
    
    def lookup_domain(self, domain: str) -> Dict:
        """Look up domain in threat intelligence"""
        return {
            'domain': domain,
            'reputation': 'suspicious',
            'registration_date': '2024-01-01',
            'registrar': 'NameSilo',
            'dns_records': {
                'A': ['192.168.1.1'],
                'NS': ['ns1.malicious.com']
            },
            'threat_indicators': ['dns_tunneling', 'fast_flux'],
            'associated_ips': ['192.168.1.1', '192.168.1.2']
        }
    
    def lookup_hash(self, file_hash: str) -> Dict:
        """Look up file hash in threat intelligence"""
        return {
            'hash': file_hash,
            'md5': 'd41d8cd98f00b204e9800998ecf8427e',
            'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            'reputation': 'malicious',
            'detection_name': 'Trojan.GenericKD.46789',
            'first_submission': '2024-01-01',
            'file_type': 'PE32 executable',
            'file_size': 24576,
            'threat_type': 'Trojan',
            'analysis': {
                'sandbox': 'MalwareBazaar',
                'behavior': ['Creates hidden directory', 'Modifies registry', 'Connects to C2']
            }
        }
    
    def check_iocs(self, event: SecurityEvent) -> List[Dict]:
        """Check event against IOCs"""
        matches = []
        
        if event.source_ip:
            ip_info = self.lookup_ip(event.source_ip)
            if ip_info['reputation'] == 'malicious':
                matches.append({'type': 'ip', 'value': event.source_ip, 'info': ip_info})
        
        return matches


class IncidentResponse:
    """Incident response coordination"""
    
    def __init__(self):
        self.incidents = []
    
    def create_incident(self,
                        title: str,
                        severity: AlertSeverity,
                        description: str) -> Dict:
        """Create incident"""
        incident = {
            'id': f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'title': title,
            'severity': severity.value,
            'status': 'open',
            'created': datetime.now().isoformat(),
            'description': description,
            'timeline': [
                {'timestamp': datetime.now().isoformat(), 'action': 'Incident created', 'actor': 'System'}
            ],
            'actions_taken': [],
            'evidence_collected': [],
            'lessons_learned': []
        }
        self.incidents.append(incident)
        return incident
    
    def add_incident_action(self,
                           incident_id: str,
                           action: str,
                           actor: str) -> Dict:
        """Add action to incident"""
        for inc in self.incidents:
            if inc['id'] == incident_id:
                inc['timeline'].append({
                    'timestamp': datetime.now().isoformat(),
                    'action': action,
                    'actor': actor
                })
                inc['actions_taken'].append(action)
                return {'status': 'success'}
        return {'status': 'not_found'}
    
    def generate_incident_report(self,
                                 incident_id: str) -> Dict:
        """Generate incident closure report"""
        for inc in self.incidents:
            if inc['id'] == incident_id:
                return {
                    'incident_id': inc['id'],
                    'title': inc['title'],
                    'severity': inc['severity'],
                    'status': 'closed',
                    'duration': '4 hours',
                    'summary': f"Incident {inc['id']} was successfully resolved.",
                    'timeline': inc['timeline'],
                    'actions_taken': inc['actions_taken'],
                    'evidence_collected': inc['evidence_collected'],
                    'root_cause': 'Unauthenticated remote code execution vulnerability',
                    'remediation_steps': [
                        'Isolate affected systems',
                        'Apply security patch',
                        'Reset credentials',
                        'Verify integrity'
                    ],
                    'lessons_learned': inc['lessons_learned'],
                    'recommendations': [
                        'Implement patch management process',
                        'Enable MFA for all admin accounts',
                        'Review access controls weekly'
                    ]
                }
        return {'status': 'not_found'}


if __name__ == "__main__":
    collector = LogCollector()
    syslog = collector.collect_syslog("Jan 15 10:30:45 server sshd[1234]: Accepted publickey for user admin", "sshd")
    print(f"Syslog parsed: {syslog['normalized']['message']}")
    
    siem = SIEMAnalyzer()
    alerts = siem.correlate_events([])
    print(f"Alerts generated: {len(alerts)}")
    
    baseline = siem.create_behavior_baseline([])
    print(f"Baseline created for {baseline['unique_users']} users")
    
    alerts_mgmt = AlertManager()
    alert = alerts_mgmt.create_alert(
        title="Suspicious Login Activity",
        severity=AlertSeverity.HIGH,
        description="Multiple failed login attempts from unknown IP",
        affected_assets=["192.168.1.100"]
    )
    print(f"Alert created: {alert.id}")
    
    escalation = alerts_mgmt.get_escalation_path(alert)
    print(f"Escalation levels: {len(escalation)}")
    
    threat_intel = ThreatIntelligence()
    ip_info = threat_intel.lookup_ip("10.10.10.10")
    print(f"IP reputation: {ip_info['reputation']}")
    
    incident = IncidentResponse()
    inc = incident.create_incident(
        title="Data Breach Investigation",
        severity=AlertSeverity.CRITICAL,
        description="Potential unauthorized access to customer data"
    )
    print(f"Incident created: {inc['id']}")
