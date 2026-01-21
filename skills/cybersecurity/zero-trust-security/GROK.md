---
name: "Zero-Trust Security"
version: "1.0.0"
description: "Enterprise zero-trust security architecture with Grok's physics-based threat modeling"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["security", "zero-trust", "cybersecurity", "threat-modeling"]
category: "cybersecurity"
personality: "security-architect"
use_cases: ["identity-security", "network-security", "threat-detection", "compliance"]
---

# Zero-Trust Security 🛡️

> Build unbreakable security with Grok's physics-based threat modeling and continuous verification

## 🎯 Why This Matters for Grok

Grok's analytical precision and security-first mindset create perfect cybersecurity:

- **Physics-Based Threat Modeling** ⚛️: Model threats with scientific rigor
- **Zero-Trust Architecture** 🔐: Never trust, always verify
- **Real-time Threat Detection** 📡: Instant anomaly identification
- **Defense in Depth** 🏰: Layered security approach

## 🛠️ Core Capabilities

### 1. Identity Security
```yaml
identity:
  mfa: ["fido2", "passkeys", "biometric"]
  sso: ["saml", "oauth", "oidc"]
  iam: ["rbac", "abac", "pbac"]
  privileged: ["pam", "just-in-time", "zero-standing"]
```

### 2. Network Security
```yaml
network:
  microsegmentation: "software-defined"
  sdp: "zero-trust-network"
  encryption: ["tls13", "wireguard", "post-quantum"]
  monitoring: "real-time-ids"
```

### 3. Threat Detection
```yaml
detection:
  siem: ["splunk", "elastic", "chronicle"]
  edr: ["crowdstrike", "microsoft-defender"]
  xdr: "unified-platform"
  soar: "automated-response"
```

## 🧠 Advanced Threat Modeling

### Physics-Based Threat Analysis
```python
import numpy as np
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

class ThreatLevel(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1

@dataclass
class ThreatVector:
    name: str
    attack_surface: float  # 0-1 scale
    likelihood: float  # 0-1 scale
    impact: float  # 0-1 scale
    complexity: float  # 0-1 scale (higher = more complex for attacker)
    discoverability: float  # 0-1 scale (higher = more discoverable)

class PhysicsBasedThreatModel:
    def __init__(self):
        self.attack_graph = AttackGraph()
        self.vulnerability_db = VulnerabilityDatabase()
        self.asset_inventory = AssetInventory()
        
    def calculate_threat_risk(self, threat: ThreatVector) -> Dict:
        """Calculate risk using physics-inspired probability model"""
        
        # Risk = Threat × Vulnerability × Impact
        # Modeled as interacting particles in potential field
        
        vulnerability = self.assess_vulnerability(threat)
        
        # Energy barrier model (attacker needs to overcome barriers)
        energy_barrier = self.calculate_energy_barrier(threat)
        attacker_capability = np.random.normal(0.7, 0.2)  # Assumed attacker capability
        
        # Probability of successful attack (Boltzmann distribution)
        temperature = 1.0  # System "temperature"
        p_success = np.exp(-energy_barrier / temperature) * attacker_capability * vulnerability
        
        # Risk score (0-100)
        risk_score = (
            p_success * 100 * 
            (1 + threat.impact) / 2 *
            threat.attack_surface
        )
        
        return {
            'threat_name': threat.name,
            'risk_score': min(100, risk_score),
            'threat_level': self.risk_to_level(risk_score),
            'p_success': p_success,
            'energy_barrier': energy_barrier,
            'recommended_mitigations': self.suggest_mitigations(threat),
            'detection_difficulty': 1 - threat.discoverability,
            'time_to_compromise': self.estimate_time_to_compromise(threat)
        }
    
    def calculate_energy_barrier(self, threat: ThreatVector) -> float:
        """Calculate energy barrier for attack (physics-inspired)"""
        
        # Multiple barriers representing security controls
        barriers = []
        
        # Network segmentation barrier
        barriers.append(0.2 * self.assess_network_segmentation())
        
        # Authentication barrier
        barriers.append(0.3 * self.assess_authentication_strength())
        
        # Encryption barrier
        barriers.append(0.25 * self.assess_encryption_strength())
        
        # Monitoring barrier
        barriers.append(0.15 * self.assess_detection_capability())
        
        # Anomaly barrier
        barriers.append(0.1 * self.assess_anomaly_detection())
        
        # Total energy barrier
        total_barrier = sum(barriers)
        
        # Adjust for attack complexity
        adjusted_barrier = total_barrier * (1 + threat.complexity)
        
        return adjusted_barrier
    
    def build_attack_graph(self, target_system):
        """Build attack graph for comprehensive threat analysis"""
        
        # Node types: assets, vulnerabilities, controls
        # Edges: attack paths
        
        graph = {
            'nodes': [],
            'edges': [],
            'attack_paths': []
        }
        
        # Add initial access nodes
        initial_access = self.vulnerability_db.find_initial_access()
        graph['nodes'].extend(initial_access)
        
        # Build attack paths using graph traversal
        for node in initial_access:
            paths = self.graph_traverse(
                node, 
                target_system, 
                max_depth=5,
                cost_function=self.attack_cost_function
            )
            graph['attack_paths'].extend(paths)
        
        # Calculate critical attack paths
        critical_paths = self.identify_critical_paths(graph['attack_paths'])
        
        return {
            'graph': graph,
            'critical_paths': critical_paths,
            'attack_surface_score': self.calculate_attack_surface(graph),
            'recommendations': self.recommend_controls(critical_paths)
        }
    
    def simulate_attack_scenarios(self, threat_vectors: List[ThreatVector]):
        """Monte Carlo simulation of attack scenarios"""
        
        n_simulations = 10000
        successful_attacks = 0
        attack_durations = []
        compromised_assets = []
        
        for _ in range(n_simulations):
            # Simulate each attack vector
            for threat in threat_vectors:
                risk = self.calculate_threat_risk(threat)
                
                # Monte Carlo outcome
                if np.random.random() < risk['p_success']:
                    successful_attacks += 1
                    
                    # Simulate attack duration (log-normal distribution)
                    duration = np.random.lognormal(
                        mean=np.log(60),  # 60 minutes median
                        sigma=1.0
                    )
                    attack_durations.append(duration)
                    
                    # Track compromised assets
                    compromised = self.simulate_lateral_movement(threat)
                    compromised_assets.extend(compromised)
        
        return {
            'success_rate': successful_attacks / (n_simulations * len(threat_vectors)),
            'avg_attack_duration_minutes': np.mean(attack_durations),
            'median_attack_duration_minutes': np.median(attack_durations),
            'most_compromised_assets': self.count_compromised_assets(compromised_assets),
            'attack_timeline': self.generate_attack_timeline(attack_durations),
            'security_gaps': self.identify_security_gaps(threat_vectors)
        }
```

### Continuous Verification System
```python
class ContinuousVerification:
    def __init__(self):
        self.identity_provider = IdentityProvider()
        self.behavior_analyzer = BehaviorAnalyzer()
        self.risk_engine = RiskEngine()
        
    def verify_identity_continuous(self, user_context):
        """Continuous identity verification based on risk"""
        
        # Collect verification signals
        signals = {
            'mfa_present': self.check_mfa(user_context),
            'device_trust': self.assess_device_trust(user_context),
            'location_risk': self.assess_location_risk(user_context),
            'behavioral_anomaly': self.behavior_analyzer.detect_anomaly(user_context),
            'session_behavior': self.assess_session_behavior(user_context),
            'network_context': self.assess_network_context(user_context)
        }
        
        # Calculate risk score (physics-inspired, sum of forces)
        risk_forces = {
            'positive': signals['mfa_present'] * 0.2 + 
                       signals['device_trust'] * 0.15 +
                       signals['session_behavior'] * 0.15,
            
            'negative': (1 - signals['location_risk']) * 0.2 +
                       signals['behavioral_anomaly'] * 0.15 +
                       (1 - signals['network_context']) * 0.15
        }
        
        net_risk = sum(risk_forces['negative']) - sum(risk_forces['positive'])
        risk_score = (net_risk + 1) / 2 * 100  # Normalize to 0-100
        
        # Determine verification requirements
        verification_required = risk_score > 30
        
        # Adaptive authentication
        if verification_required:
            additional_verification = self.select_adaptive_verification(
                risk_score, 
                signals
            )
        else:
            additional_verification = []
        
        return {
            'risk_score': risk_score,
            'risk_level': self.classify_risk_level(risk_score),
            'signals': signals,
            'verification_required': verification_required,
            'additional_verification': additional_verification,
            'session_duration': self.calculate_session_duration(risk_score),
            'policy_decision': self.apply_zero_trust_policy(risk_score)
        }
    
    def detect_anomaly_behavior(self, user_behavior_history):
        """Physics-inspired behavioral anomaly detection"""
        
        # Model normal behavior as a potential well
        normal_behavior_center = self.calculate_behavioral_center(user_behavior_history)
        
        # Calculate deviation from normal (energy)
        deviations = []
        for behavior in user_behavior_history[-100:]:  # Recent behaviors
            deviation = np.linalg.norm(
                behavior - normal_behavior_center
            )
            deviations.append(deviation)
        
        # Statistical analysis of deviations
        mean_deviation = np.mean(deviations)
        std_deviation = np.std(deviations)
        
        # Anomaly detection using z-score
        z_scores = [
            (d - mean_deviation) / std_deviation 
            for d in deviations[-10:]  # Most recent
        ]
        
        # Physics-based: sudden changes indicate anomalies
        anomaly_score = max(z_scores) if max(z_scores) > 2.5 else 0
        
        return {
            'anomaly_detected': anomaly_score > 2.5,
            'anomaly_score': anomaly_score,
            'deviation_magnitude': max(deviations) if deviations else 0,
            'trend': self.calculate_deviation_trend(deviations),
            'recommendation': self.suggest_action(anomaly_score)
        }
```

## 📊 Security Operations Center

### Real-time Security Dashboard
```javascript
const SecurityDashboard = {
  threatMetrics: {
    identity: {
      mfa_adoption: 94.5,
      risk_based_auth: 87,
      privileged_access: 125,
      compromised_credentials: 3,
      avg_verification_time: 2.3
    },
    
    network: {
      microsegmentation: 92,
      encrypted_traffic: 99.2,
      sdp_coverage: 78,
      blocked_attacks: 15420,
      avg_response_time: 45
    },
    
    endpoint: {
      healthy_endpoints: 9842,
      vulnerable_systems: 23,
      edr_coverage: 98.5,
      avg_detection_time: 3.2,
      false_positive_rate: 0.03
    },
    
    cloud: {
      misconfigurations: 45,
      compliance_score: 96.8,
      iam_policies: 1234,
      exposed_secrets: 2,
      policy_violations: 156
    }
  },
  
  riskMetrics: {
    overall_risk_score: 24,
    critical_vulnerabilities: 5,
    attack_surface: 67,
    mean_time_to_detect: 4.2,
    mean_time_to_respond: 45,
    mean_time_to_remediate: 720
  },
  
  generateSecurityInsights: function() {
    const insights = [];
    
    // Critical vulnerabilities
    if (this.riskMetrics.critical_vulnerabilities > 0) {
      insights.push({
        type: 'vulnerability',
        level: 'critical',
        message: `${this.riskMetrics.critical_vulnerabilities} critical vulnerabilities require immediate attention`,
        recommendation: 'Apply emergency patches or implement compensating controls'
      });
    }
    
    // Identity risks
    if (this.threatMetrics.identity.compromised_credentials > 5) {
      insights.push({
        type: 'identity',
        level: 'high',
        message: `Compromised credential attempts: ${this.threatMetrics.identity.compromised_credentials}`,
        recommendation: 'Reset credentials, enable additional MFA factors'
      });
    }
    
    // Response time
    if (this.riskMetrics.mean_time_to_respond > 60) {
      insights.push({
        type: 'operations',
        level: 'warning',
        message: `Mean response time above target: ${this.riskMetrics.mean_time_to_respond} minutes`,
        recommendation: 'Automate SOC responses with SOAR playbooks'
      });
    }
    
    return insights;
  },
  
  predictBreachLikelihood: function() {
    // Physics-inspired breach probability model
    const vulnerabilityExposure = this.riskMetrics.critical_vulnerabilities * 0.15;
    const attackSurfaceExposure = this.riskMetrics.attack_surface * 0.1;
    const protectionEfficacy = (this.threatMetrics.network.microsegmentation + 
                               this.threatMetrics.endpoint.edr_coverage) / 200;
    
    const breachProbability = Math.min(1, 
      vulnerabilityExposure + attackSurfaceExposure - protectionEfficacy + 0.1
    );
    
    return {
      probability: breachProbability,
      risk_level: breachProbability > 0.3 ? 'high' : breachProbability > 0.1 ? 'medium' : 'low',
      contributing_factors: {
        vulnerabilities: vulnerabilityExposure,
        attack_surface: attackSurfaceExposure,
        protection_gap: protectionEfficacy
      },
      recommendations: this.generateRiskMitachProbability)
   igationPlan(bre };
  }
};
```

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Identity framework setup
- [ ] MFA deployment
- [ ] Basic monitoring
- [ ] Policy definitions

### Phase 2: Intelligence (Week 3-4)
- [ ] Zero-trust architecture
- [ ] Microsegmentation
- [ ] Advanced threat detection
- [ ] Automated response

### Phase 3: Production (Week 5-6)
- [ ] Continuous verification
- [ ] Threat intelligence integration
- [ ] Compliance automation
- [ ] Red team exercises

## 📊 Success Metrics

### Security Excellence
```yaml
identity_security:
  mfa_coverage: "> 99%"
  privileged_access_management: "100%"
  compromised_credentials_detected: "> 95%"
  identity_risk_score: "< 20"
  
network_security:
  microsegmentation: "> 95%"
  encrypted_traffic: "> 99%"
  attack_blocked: "> 99%"
  lateral_movement_prevented: "100%"
  
operational_excellence:
  mttd: "< 1 hour"
  mttr: "< 4 hours"
  false_positive_rate: "< 2%"
  automated_response: "> 80%"
  
compliance:
  audit_findings: "< 5/year"
  regulatory_compliance: "> 99%"
  policy_violations: "< 10/month"
```

---

*Build unbreakable security with physics-based threat modeling and zero-trust principles.* 🛡️✨