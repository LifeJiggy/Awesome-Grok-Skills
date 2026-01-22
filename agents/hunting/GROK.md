---
name: "Threat Hunting Agent"
version: "1.0.0"
description: "Proactive threat hunting and adversary detection with Grok's analytical precision"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["hunting", "threat-intelligence", "adversary", "detection"]
category: "hunting"
personality: "threat-hunter"
use_cases: ["apt-detection", "threat-intelligence", "adversary-tracking"]
---

# Threat Hunting Agent 🎯

> Hunt down threats with Grok's physics-based analytical precision and systematic investigation

## 🎯 Why This Matters for Grok

Grok's analytical mind approaches threat hunting like solving a complex physics problem:

- **Systematic Investigation** 🔬: Methodical hypothesis-driven hunting
- **Pattern Recognition** 🧩: Identifying subtle attack patterns
- **Predictive Modeling** 📊: Anticipating adversary movements
- **Deep Forensics** 🔍: Comprehensive digital forensics

## 🛠️ Core Capabilities

### 1. Threat Intelligence
```yaml
intelligence:
  ioc_collection:
    - domains
    - ip_addresses
    - file_hashes
    - urls
    - email_addresses
  enrichment:
    - threat_actor_mapping
    - campaign_correlation
    - ttp_analysis
```

### 2. Active Hunting
```yaml
hunting:
  hypothesis_driven:
    - lateral_movement
    - persistence
    - data_exfiltration
    - command_control
  analytics:
    - anomaly_detection
    - behavioral_analysis
    - correlation_rules
```

### 3. Adversary Tracking
```yaml
tracking:
  actors:
    - apt_groups
    - criminal_organizations
    - hacktivists
  campaigns:
    - attribution
    - infrastructure
    - tactics_techniques
```

## 🧠 Advanced Hunting Framework

### Threat Intelligence Engine
```python
class ThreatIntelligenceEngine:
    def __init__(self):
        self.ioc_database = {}
        self.threat_actors = {}
        self.campaigns = {}
        self.ttps_matrix = {}
    
    def collect_iocs(self, source: str, iocs: List[Dict]) -> List[ThreatIndicator]:
        """Collect indicators of compromise"""
        for ioc in iocs:
            self.ioc_database[ioc['value']] = ThreatIndicator(
                ioc_type=ioc.get('type'),
                value=ioc['value'],
                severity=ThreatSeverity(ioc['severity']),
                source=source,
                first_seen=datetime.fromisoformat(ioc.get('first_seen')),
                tags=ioc.get('tags', [])
            )
        
        return list(self.ioc_database.values())
    
    def enrich_threat_data(self, threat_data: Dict) -> Dict:
        """Enrich threat data with intelligence"""
        enriched = threat_data.copy()
        
        enriched['matched_iocs'] = [
            self.ioc_database[ioc] 
            for ioc in threat_data.get('indicators', [])
            if ioc in self.ioc_database
        ]
        
        enriched['risk_score'] = self.calculate_risk_score(threat_data)
        enriched['threat_actor'] = self.identify_threat_actor(threat_data)
        enriched['ttps'] = self.map_attack_ttps(threat_data)
        
        return enriched
    
    def calculate_risk_score(self, threat_data: Dict) -> float:
        """Calculate risk score using physics-inspired model"""
        base_score = 0
        
        for ioc in threat_data.get('indicators', []):
            if ioc in self.ioc_database:
                base_score += self.ioc_database[ioc].severity.value * 20
        
        if 'severity' in threat_data:
            base_score += threat_data['severity'] * 10
        
        return min(100, base_score)
```

### Threat Hunting Engine
```python
class ThreatHuntingEngine:
    def __init__(self):
        self.hypotheses = []
        self.hunts = {}
        self.findings = []
        self.analytics_rules = []
    
    def create_hypothesis(self, hypothesis: str, category: str) -> str:
        """Create threat hunting hypothesis"""
        hunt_id = f"hunt_{int(datetime.now().timestamp())}"
        
        self.hypotheses.append({
            'id': hunt_id,
            'hypothesis': hypothesis,
            'category': category,
            'status': 'active',
            'created_at': datetime.now(),
            'findings': []
        })
        
        return hunt_id
    
    def execute_hunt(self, hunt_id: str, data_sources: List[str]) -> Dict:
        """Execute threat hunt with hypothesis testing"""
        hunt = next(h for h in self.hypotheses if h['id'] == hunt_id)
        
        results = {
            'hunt_id': hunt_id,
            'hypothesis': hunt['hypothesis'],
            'data_sources': data_sources,
            'queries_executed': [],
            'findings': []
        }
        
        for source in data_sources:
            queries = self.generate_queries(hunt, source)
            results['queries_executed'].extend(queries)
            
            for query in queries:
                query_results = self.execute_query(source, query)
                results['findings'].extend(query_results)
        
        hunt['findings'] = results['findings']
        
        return results
    
    def generate_queries(self, hunt: Dict, data_source: str) -> List[str]:
        """Generate hunt queries based on hypothesis"""
        queries = []
        hyp = hunt['hypothesis'].lower()
        
        if 'lateral movement' in hyp:
            queries.extend([
                f"SELECT * FROM {data_source} WHERE event_type = 'network_connect' AND destination_port IN (445, 3389)",
                f"SELECT * FROM {data_source} WHERE process_name LIKE '%psexec%'"
            ])
        
        if 'persistence' in hyp:
            queries.extend([
                f"SELECT * FROM {data_source} WHERE registry_key LIKE '%Run%'",
                f"SELECT * FROM {data_source} WHERE scheduled_task_name IS NOT NULL"
            ])
        
        if 'data exfiltration' in hyp:
            queries.extend([
                f"SELECT * FROM {data_source} WHERE bytes_sent > 100000000",
                f"SELECT * FROM {data_source} WHERE unusual_destination_ip = true"
            ])
        
        return queries
```

### Adversary Tracking Engine
```python
class AdversaryTrackingEngine:
    def __init__(self):
        self.tracked_actors = {}
        self.activity_timelines = {}
        self.ttps_matrix = {}
    
    def add_adversary(self, actor_name: str, aliases: List[str], ttps: List[str]):
        """Add tracked adversary"""
        self.tracked_actors[actor_name] = {
            'aliases': aliases,
            'ttps': ttps,
            'first_observed': datetime.now(),
            'last_activity': None,
            'activity_count': 0,
            'target_sectors': []
        }
    
    def record_activity(self, actor_name: str, activity: Dict):
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
        """Get adversary profile"""
        if actor_name not in self.tracked_actors:
            return {'error': 'Actor not found'}
        
        actor = self.tracked_actors[actor_name]
        timeline = self.activity_timelines.get(actor_name, [])
        
        return {
            'name': actor_name,
            'aliases': actor['aliases'],
            'ttps': actor['ttps'],
            'first_observed': actor['first_observed'],
            'last_activity': actor['last_activity'],
            'activity_count': actor['activity_count'],
            'risk_level': self.assess_risk(actor),
            'recent_activity': timeline[-10:]
        }
```

## 📊 Hunting Dashboard

### Real-time Hunting Metrics
```javascript
const HuntingDashboard = {
  metrics: {
    activeHunts: 5,
    hypothesesTested: 23,
    findings: {
      critical: 3,
      high: 8,
      medium: 15,
      low: 25
    },
    timeToDetect: {
      average: 4.2, // hours
      median: 2.5
    },
    coverage: {
      endpoints: 98,
      network: 95,
      cloud: 85
    }
  },
  
  trackedActors: [
    { name: 'APT29', alias: 'Cozy Bear', ttps: 12, activity: 'high' },
    { name: 'APT41', alias: 'Winnti', ttps: 15, activity: 'medium' },
    { name: 'LAPSUS$', alias: 'DEV-0537', ttps: 8, activity: 'high' }
  ],
  
  generateAlerts: function() {
    const alerts = [];
    
    if (this.metrics.findings.critical > 0) {
      alerts.push({
        type: 'critical',
        message: `${this.metrics.findings.critical} critical hunting findings`,
        action: 'investigate_findings'
      });
    }
    
    return alerts;
  }
};
```

## 🎯 Hunting Workflow

### Phase 1: Intelligence Preparation
- [ ] Collect threat intelligence feeds
- [ ] Map adversary TTPs
- [ ] Identify potential targets
- [ ] Develop hypotheses

### Phase 2: Active Hunting
- [ ] Execute hypothesis-driven hunts
- [ ] Run analytics rules
- [ ] Correlate events
- [ ] Document findings

### Phase 3: Analysis & Response
- [ ] Analyze collected data
- [ ] Attribute to adversary
- [ ] Develop indicators
- [ ] Initiate response

## 📊 Success Metrics

### Hunting Excellence
```yaml
hunting_effectiveness:
  hypothesis_success_rate: "> 30%"
  time_to_detect: "< 4 hours"
  false_positive_rate: "< 10%"
  adversary_coverage: "> 80% of tracked actors"
  
operational_efficiency:
  hunts_per_week: 10+
  findings_per_hunt: 2+
  investigations_started: "> 5/month"
  
threat_intelligence:
  ioc_coverage: "> 1000 IOCs"
  actor_tracking: "> 20 actors"
  campaign_attribution: "> 90% accuracy"
```

---

*Hunt with precision, detect with certainty.* 🎯✨
