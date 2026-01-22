"""
Hunting Agent
Threat hunting and adversary detection
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import re


class ThreatSeverity(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


@dataclass
class ThreatIndicator:
    ioc_type: str
    value: str
    severity: ThreatSeverity
    source: str
    first_seen: datetime
    last_seen: datetime
    tags: List[str]


class ThreatIntelligenceEngine:
    """Threat intelligence collection and analysis"""
    
    def __init__(self):
        self.ioc_database = {}
        self.threat_actors = {}
        self.campaigns = {}
        self.ttps_matrix = {}
    
    def collect_iocs(self, 
                    source: str,
                    iocs: List[Dict]) -> List[ThreatIndicator]:
        """Collect indicators of compromise"""
        indicators = []
        
        for ioc in iocs:
            indicator = ThreatIndicator(
                ioc_type=ioc.get('type', 'domain'),
                value=ioc.get('value', ''),
                severity=ThreatSeverity(ioc.get('severity', 3)),
                source=source,
                first_seen=datetime.fromisoformat(ioc.get('first_seen', datetime.now().isoformat())),
                last_seen=datetime.fromisoformat(ioc.get('last_seen', datetime.now().isoformat())),
                tags=ioc.get('tags', [])
            )
            indicators.append(indicator)
            self.ioc_database[indicator.value] = indicator
        
        return indicators
    
    def enrich_threat_data(self, threat_data: Dict) -> Dict:
        """Enrich threat data with intelligence"""
        enriched = threat_data.copy()
        
        if 'indicators' in threat_data:
            enriched['matched_iocs'] = []
            for ioc in threat_data['indicators']:
                if ioc in self.ioc_database:
                    enriched['matched_iocs'].append(self.ioc_database[ioc])
        
        enriched['risk_score'] = self.calculate_risk_score(threat_data)
        enriched['threat_actor'] = self.identify_threat_actor(threat_data)
        enriched['campaign'] = self.link_to_campaign(threat_data)
        
        return enriched
    
    def calculate_risk_score(self, threat_data: Dict) -> float:
        """Calculate risk score based on IOCs and context"""
        base_score = 0
        
        if 'indicators' in threat_data:
            for ioc in threat_data['indicators']:
                if ioc in self.ioc_database:
                    base_score += self.ioc_database[ioc].severity.value * 20
        
        if 'severity' in threat_data:
            base_score += threat_data['severity'] * 10
        
        return min(100, base_score)
    
    def identify_threat_actor(self, threat_data: Dict) -> Optional[str]:
        """Identify associated threat actor"""
        for actor, data in self.threat_actors.items():
            if any(ioc in data.get('iocs', []) for ioc in threat_data.get('indicators', [])):
                return actor
        return None
    
    def link_to_campaign(self, threat_data: Dict) -> Optional[str]:
        """Link to known campaign"""
        for campaign, data in self.campaigns.items():
            if any(ioc in data.get('iocs', []) for ioc in threat_data.get('indicators', [])):
                return campaign
        return None


class ThreatHuntingEngine:
    """Active threat hunting engine"""
    
    def __init__(self):
        self.hypotheses = []
        self.hunts = {}
        self.findings = []
        self.analytics_rules = []
    
    def create_hypothesis(self, 
                         hypothesis: str,
                         category: str,
                         severity: ThreatSeverity) -> str:
        """Create threat hunting hypothesis"""
        hunt_id = f"hunt_{int(datetime.now().timestamp())}"
        
        self.hypotheses.append({
            'id': hunt_id,
            'hypothesis': hypothesis,
            'category': category,
            'severity': severity,
            'status': 'active',
            'created_at': datetime.now(),
            'findings': []
        })
        
        return hunt_id
    
    def execute_hunt(self, hunt_id: str, data_sources: List[str]) -> Dict:
        """Execute threat hunt"""
        if hunt_id not in self.hypotheses:
            raise ValueError(f"Hunt {hunt_id} not found")
        
        hunt = next(h for h in self.hypotheses if h['id'] == hunt_id)
        
        results = {
            'hunt_id': hunt_id,
            'hypothesis': hunt['hypothesis'],
            'data_sources': data_sources,
            'queries_executed': [],
            'results_analyzed': [],
            'findings': []
        }
        
        for source in data_sources:
            queries = self.generate_queries(hunt, source)
            results['queries_executed'].extend(queries)
            
            for query in queries:
                query_results = self.execute_query(source, query)
                results['results_analyzed'].extend(query_results)
        
        hunt['findings'] = results['findings']
        self.hunts[hunt_id] = results
        
        return results
    
    def generate_queries(self, hunt: Dict, data_source: str) -> List[str]:
        """Generate hunt queries based on hypothesis"""
        queries = []
        
        if 'lateral movement' in hunt['hypothesis'].lower():
            queries.extend([
                f"SELECT * FROM {data_source} WHERE event_type = 'network_connect' AND destination_port IN (445, 3389)",
                f"SELECT * FROM {data_source} WHERE process_name LIKE '%psexec%' OR process_name LIKE '%wmiexec%'"
            ])
        
        if 'persistence' in hunt['hypothesis'].lower():
            queries.extend([
                f"SELECT * FROM {data_source} WHERE registry_key LIKE '%Run%' OR registry_key LIKE '%Startup%'",
                f"SELECT * FROM {data_source} WHERE scheduled_task_name IS NOT NULL"
            ])
        
        if 'data exfiltration' in hunt['hypothesis'].lower():
            queries.extend([
                f"SELECT * FROM {data_source} WHERE bytes_sent > 100000000 AND protocol IN ('http', 'https', 'dns')",
                f"SELECT * FROM {data_source} WHERE unusual_destination_ip = true"
            ])
        
        return queries
    
    def execute_query(self, data_source: str, query: str) -> List[Dict]:
        """Execute hunt query"""
        return [
            {'timestamp': datetime.now(), 'source': data_source, 'matched': True}
        ]
    
    def add_analytics_rule(self, 
                          rule_name: str,
                          query: str,
                          severity: ThreatSeverity):
        """Add analytics rule for detection"""
        self.analytics_rules.append({
            'name': rule_name,
            'query': query,
            'severity': severity,
            'enabled': True,
            'created_at': datetime.now()
        })
    
    def run_analytics(self, telemetry: List[Dict]) -> List[Dict]:
        """Run analytics rules against telemetry"""
        alerts = []
        
        for rule in self.analytics_rules:
            if not rule['enabled']:
                continue
            
            for event in telemetry:
                if self.match_rule(event, rule):
                    alerts.append({
                        'rule_name': rule['name'],
                        'severity': rule['severity'],
                        'event': event,
                        'timestamp': datetime.now()
                    })
        
        return alerts
    
    def match_rule(self, event: Dict, rule: Dict) -> bool:
        """Match event against rule"""
        return rule['query'].lower() in str(event).lower()


class AdversaryTrackingEngine:
    """Track and monitor adversary activities"""
    
    def __init__(self):
        self.tracked_actors = {}
        self.activity_timelines = {}
        self.target_profiles = {}
    
    def add_adversary(self, 
                     actor_name: str,
                     aliases: List[str],
                     target_sectors: List[str],
                     ttps: List[str]):
        """Add tracked adversary"""
        self.tracked_actors[actor_name] = {
            'aliases': aliases,
            'target_sectors': target_sectors,
            'ttps': ttps,
            'first_observed': datetime.now(),
            'last_activity': None,
            'activity_count': 0
        }
    
    def record_activity(self, 
                       actor_name: str,
                       activity: Dict):
        """Record adversary activity"""
        if actor_name not in self.tracked_actors:
            return
        
        if actor_name not in self.activity_timelines:
            self.activity_timelines[actor_name] = []
        
        self.activity_timelines[actor_name].append({
            'timestamp': datetime.now(),
            'activity': activity
        })
        
        self.tracked_actors[actor_name]['last_activity'] = datetime.now()
        self.tracked_actors[actor_name]['activity_count'] += 1
    
    def get_actor_summary(self, actor_name: str) -> Dict:
        """Get adversary summary"""
        if actor_name not in self.tracked_actors:
            return {'error': 'Actor not found'}
        
        actor = self.tracked_actors[actor_name]
        timeline = self.activity_timelines.get(actor_name, [])
        
        return {
            'name': actor_name,
            'aliases': actor['aliases'],
            'target_sectors': actor['target_sectors'],
            'ttps': actor['ttps'],
            'first_observed': actor['first_observed'],
            'last_activity': actor['last_activity'],
            'activity_count': actor['activity_count'],
            'recent_activity': timeline[-10:] if timeline else [],
            'risk_assessment': self.assess_actor_risk(actor)
        }
    
    def assess_actor_risk(self, actor: Dict) -> Dict:
        """Assess adversary risk level"""
        recent_activity = actor.get('activity_count', 0)
        
        risk_level = 'low'
        if recent_activity > 50:
            risk_level = 'critical'
        elif recent_activity > 20:
            risk_level = 'high'
        elif recent_activity > 5:
            risk_level = 'medium'
        
        return {
            'level': risk_level,
            'activity_score': min(100, recent_activity * 2),
            'recommendation': f"Increase monitoring for {actor['target_sectors']}"
        }


class HuntingDashboard:
    """Threat hunting dashboard"""
    
    def __init__(self):
        self.threat_intel = ThreatIntelligenceEngine()
        self.hunting = ThreatHuntingEngine()
        self.adversary = AdversaryTrackingEngine()
    
    def hunt_for_apt_activity(self, network_telemetry: List[Dict]) -> Dict:
        """Hunt for APT-like activity"""
        results = {
            'suspicious_activities': [],
            'potential_compromised': [],
            'recommended_actions': []
        }
        
        apt_indicators = [
            'powershell.*-enc',
            'certutil.*-decode',
            'schtasks.*/create.*powershell',
            'reg.*add.*run',
            'wmic.*process.*call.*create'
        ]
        
        for event in network_telemetry:
            for indicator in apt_indicators:
                if re.search(indicator, str(event), re.IGNORECASE):
                    results['suspicious_activities'].append({
                        'event': event,
                        'matched_indicator': indicator
                    })
        
        lateral_movement = self.detect_lateral_movement(network_telemetry)
        results['potential_compromised'].extend(lateral_movement)
        
        if results['suspicious_activities']:
            results['recommended_actions'].extend([
                'Isolate affected endpoints',
                'Preserve forensic evidence',
                'Enable enhanced logging',
                'Review access controls'
            ])
        
        return results
    
    def detect_lateral_movement(self, telemetry: List[Dict]) -> List[Dict]:
        """Detect potential lateral movement"""
        compromised = []
        
        internal_connections = [e for e in telemetry if self.is_internal_ip(e.get('destination_ip', ''))]
        
        connection_patterns = {}
        for conn in internal_connections:
            src = conn.get('source_ip', '')
            if src not in connection_patterns:
                connection_patterns[src] = []
            connection_patterns[src].append(conn)
        
        for src, connections in connection_patterns.items():
            if len(connections) > 10:
                compromised.append({
                    'source_ip': src,
                    'connection_count': len(connections),
                    'reason': 'Excessive internal connections'
                })
        
        return compromised
    
    def is_internal_ip(self, ip: str) -> bool:
        """Check if IP is internal"""
        internal_ranges = ['10.', '172.16.', '192.168.', '127.']
        return any(ip.startswith(r) for r in internal_ranges)


if __name__ == "__main__":
    hunting = HuntingDashboard()
    
    telemetry = [
        {'source_ip': '192.168.1.100', 'destination_ip': '192.168.1.50', 'process': 'psexec.exe'},
        {'source_ip': '192.168.1.100', 'destination_ip': '192.168.1.51', 'process': 'psexec.exe'},
        {'command_line': 'powershell -enc SQBFAFgAIAAoAE4AZQB3AC0A'}
    ]
    
    results = hunting.hunt_for_apt_activity(telemetry)
    
    print(f"Suspicious activities: {len(results['suspicious_activities'])}")
    print(f"Potential compromised: {len(results['potential_compromised'])}")
    print(f"Recommended actions: {results['recommended_actions']}")
