from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class ThreatSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ThreatCategory(Enum):
    SPOOFING = "spoofing"
    TAMPERING = "tampering"
    REPUDIATION = "repudiation"
    INFORMATION_DISCLOSURE = "information_disclosure"
    DENIAL_OF_SERVICE = "denial_of_service"
    ELEVATION_OF_PRIVILEGE = "elevation_of_privilege"


class AssetType(Enum):
    DATA = "data"
    PROCESS = "process"
    EXTERNAL_ENTITY = "external_entity"
    TRUST_BOUNDARY = "trust_boundary"


@dataclass
class Asset:
    id: str
    name: str
    type: AssetType
    description: str
    confidentiality: str
    integrity: str
    availability: str
    value: int
    owner: str


@dataclass
class Threat:
    id: str
    name: str
    category: ThreatCategory
    severity: ThreatSeverity
    description: str
    affected_assets: List[str]
    attack_vector: str
    likelihood: str
    impact: str
    mitigation: str
    residual_risk: str


@dataclass
class DiagramElement:
    id: str
    type: str
    name: str
    description: str
    properties: Dict
    trust_level: str
    incoming_flows: List[str]
    outgoing_flows: List[str]


class STRIDEAnalyzer:
    """STRIDE threat analysis"""
    
    def __init__(self):
        self.threats = []
    
    def analyze_spoofing(self,
                         element: DiagramElement) -> List[Threat]:
        """Analyze spoofing threats"""
        threats = []
        
        if element.type in ["user", "process", "external_entity"]:
            threats.append(Threat(
                id=f"SPOOF-{len(self.threats)+1:03d}",
                name=f"User spoofing for {element.name}",
                category=ThreatCategory.SPOOFING,
                severity=ThreatSeverity.HIGH,
                description=f"An attacker could impersonate {element.name}",
                affected_assets=[element.id],
                attack_vector="Network, credential theft",
                likelihood="Medium",
                impact="High",
                mitigation="Implement strong authentication, MFA",
                residual_risk="Medium"
            ))
        
        return threats
    
    def analyze_tampering(self,
                          element: DiagramElement) -> List[Threat]:
        """Analyze tampering threats"""
        threats = []
        
        if element.type in ["process", "data_store"]:
            threats.append(Threat(
                id=f"TAMP-{len(self.threats)+1:03d}",
                name=f"Data tampering for {element.name}",
                category=ThreatCategory.TAMPERING,
                severity=ThreatSeverity.HIGH,
                description=f"Data in {element.name} could be modified unauthorizedly",
                affected_assets=[element.id],
                attack_vector="Network, direct access",
                likelihood="Medium",
                impact="High",
                mitigation="Implement integrity checks, digital signatures",
                residual_risk="Low"
            ))
        
        return threats
    
    def analyze_repudiation(self,
                            element: DiagramElement) -> List[Threat]:
        """Analyze repudiation threats"""
        threats = []
        
        if element.type in ["process"]:
            threats.append(Threat(
                id=f"REPUD-{len(self.threats)+1:03d}",
                name=f"Repudiation for {element.name}",
                category=ThreatCategory.REPUDIATION,
                severity=ThreatSeverity.MEDIUM,
                description=f"Actions in {element.name} could be denied by user",
                affected_assets=[element.id],
                attack_vector="Log manipulation",
                likelihood="Low",
                impact="Medium",
                mitigation="Implement audit logging, non-repudiation",
                residual_risk="Low"
            ))
        
        return threats
    
    def analyze_information_disclosure(self,
                                       element: DiagramElement) -> List[Threat]:
        """Analyze information disclosure threats"""
        threats = []
        
        if element.type in ["data_store", "process"]:
            if element.properties.get("confidentiality") == "high":
                threats.append(Threat(
                    id=f"INFO-{len(self.threats)+1:03d}",
                    name=f"Information disclosure for {element.name}",
                    category=ThreatCategory.INFORMATION_DISCLOSURE,
                    severity=ThreatSeverity.CRITICAL,
                    description=f"Confidential data in {element.name} could be exposed",
                    affected_assets=[element.id],
                    attack_vector="Network, database access",
                    likelihood="Medium",
                impact="Critical",
                    mitigation="Encrypt data, implement access controls",
                    residual_risk="Medium"
                ))
        
        return threats
    
    def analyze_dos(self,
                    element: DiagramElement) -> List[Threat]:
        """Analyze denial of service threats"""
        threats = []
        
        if element.type in ["process", "data_store"]:
            threats.append(Threat(
                id=f"DOS-{len(self.threats)+1:03d}",
                name=f"Denial of service for {element.name}",
                category=ThreatCategory.DENIAL_OF_SERVICE,
                severity=ThreatSeverity.HIGH,
                description=f"{element.name} could be made unavailable",
                affected_assets=[element.id],
                attack_vector="Network, resource exhaustion",
                likelihood="Medium",
                impact="High",
                mitigation="Implement rate limiting, redundancy",
                residual_risk="Medium"
            ))
        
        return threats
    
    def analyze_elevation_of_privilege(self,
                                        element: DiagramElement) -> List[Threat]:
        """Analyze elevation of privilege threats"""
        threats = []
        
        if element.type == "process":
            threats.append(Threat(
                id=f"EOP-{len(self.threats)+1:03d}",
                name=f"Elevation of privilege in {element.name}",
                category=ThreatCategory.ELEVATION_OF_PRIVILEGE,
                severity=ThreatSeverity.CRITICAL,
                description=f"Attacker could gain elevated privileges in {element.name}",
                affected_assets=[element.id],
                attack_vector="Input validation, authentication bypass",
                likelihood="Low",
                impact="Critical",
                mitigation="Implement least privilege, input validation",
                residual_risk="Low"
            ))
        
        return threats
    
    def analyze_element(self, element: DiagramElement) -> List[Threat]:
        """Perform complete STRIDE analysis on element"""
        all_threats = []
        all_threats.extend(self.analyze_spoofing(element))
        all_threats.extend(self.analyze_tampering(element))
        all_threats.extend(self.analyze_repudiation(element))
        all_threats.extend(self.analyze_information_disclosure(element))
        all_threats.extend(self.analyze_dos(element))
        all_threats.extend(self.analyze_elevation_of_privilege(element))
        return all_threats


class DataFlowDiagrammer:
    """Create and analyze data flow diagrams"""
    
    def __init__(self):
        self.elements = []
        self.flows = []
    
    def add_external_entity(self,
                            name: str,
                            description: str = "") -> str:
        """Add external entity to diagram"""
        element = DiagramElement(
            id=f"EE-{len(self.elements)+1:03d}",
            type="external_entity",
            name=name,
            description=description,
            properties={},
            trust_level="external",
            incoming_flows=[],
            outgoing_flows=[]
        )
        self.elements.append(element)
        return element.id
    
    def add_process(self,
                    name: str,
                    trust_level: str = "internal",
                    properties: Dict = None) -> str:
        """Add process to diagram"""
        element = DiagramElement(
            id=f"PROC-{len(self.elements)+1:03d}",
            type="process",
            name=name,
            description="",
            properties=properties or {},
            trust_level=trust_level,
            incoming_flows=[],
            outgoing_flows=[]
        )
        self.elements.append(element)
        return element.id
    
    def add_data_store(self,
                       name: str,
                       confidentiality: str = "medium") -> str:
        """Add data store to diagram"""
        element = DiagramElement(
            id=f"DS-{len(self.elements)+1:03d}",
            type="data_store",
            name=name,
            description="",
            properties={"confidentiality": confidentiality},
            trust_level="internal",
            incoming_flows=[],
            outgoing_flows=[]
        )
        self.elements.append(element)
        return element.id
    
    def add_trust_boundary(self, name: str) -> str:
        """Add trust boundary to diagram"""
        element = DiagramElement(
            id=f"TB-{len(self.elements)+1:03d}",
            type="trust_boundary",
            name=name,
            description="Boundary between trust zones",
            properties={},
            trust_level="boundary",
            incoming_flows=[],
            outgoing_flows=[]
        )
        self.elements.append(element)
        return element.id
    
    def add_data_flow(self,
                      from_id: str,
                      to_id: str,
                      data_type: str,
                      protocol: str = "HTTPS"):
        """Add data flow between elements"""
        flow = {
            'from': from_id,
            'to': to_id,
            'data_type': data_type,
            'protocol': protocol,
            'encrypted': protocol in ["HTTPS", "TLS", "SSH"]
        }
        self.flows.append(flow)
        
        for elem in self.elements:
            if elem.id == from_id:
                elem.outgoing_flows.append(to_id)
            if elem.id == to_id:
                elem.incoming_flows.append(from_id)
    
    def generate_diagram_description(self) -> Dict:
        """Generate text description of diagram"""
        return {
            'elements': len(self.elements),
            'flows': len(self.flows),
            'external_entities': [e for e in self.elements if e.type == "external_entity"],
            'processes': [e for e in self.elements if e.type == "process"],
            'data_stores': [e for e in self.elements if e.type == "data_store"],
            'trust_boundaries': [e for e in self.elements if e.type == "trust_boundary"],
            'data_flows': self.flows
        }


class RiskCalculator:
    """Calculate and prioritize risks"""
    
    def calculate_risk(self,
                       threat: Threat,
                       existing_controls: List[str] = None) -> Dict:
        """Calculate risk score for threat"""
        likelihood_scores = {"High": 3, "Medium": 2, "Low": 1}
        impact_scores = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        
        likelihood = likelihood_scores.get(threat.likelihood, 2)
        impact = impact_scores.get(threat.impact, 2)
        risk_score = likelihood * impact
        
        severity_mapping = {
            (4, 4): ThreatSeverity.CRITICAL,
            (3, 4): ThreatSeverity.CRITICAL,
            (4, 3): ThreatSeverity.CRITICAL,
            (3, 3): ThreatSeverity.HIGH,
            (2, 4): ThreatSeverity.HIGH,
            (3, 2): ThreatSeverity.MEDIUM,
            (2, 3): ThreatSeverity.MEDIUM,
            (4, 1): ThreatSeverity.MEDIUM,
            (1, 4): ThreatSeverity.MEDIUM,
            (2, 2): ThreatSeverity.LOW,
            (1, 3): ThreatSeverity.LOW,
            (3, 1): ThreatSeverity.LOW,
            (1, 2): ThreatSeverity.LOW,
            (2, 1): ThreatSeverity.LOW,
            (1, 1): ThreatSeverity.LOW
        }
        
        calculated_severity = severity_mapping.get((likelihood, impact), ThreatSeverity.MEDIUM)
        
        return {
            'threat_id': threat.id,
            'risk_score': risk_score,
            'risk_level': 'Critical' if risk_score >= 9 else 'High' if risk_score >= 6 else 'Medium' if risk_score >= 3 else 'Low',
            'calculated_severity': calculated_severity.value,
            'likelihood_score': likelihood,
            'impact_score': impact,
            'mitigation_effectiveness': 'High' if existing_controls else 'None',
            'residual_risk': 'Low' if existing_controls else 'Same as inherent'
        }
    
    def prioritize_threats(self,
                           threats: List[Threat],
                           existing_controls: Dict = None) -> List[Dict]:
        """Prioritize threats by risk"""
        risk_list = []
        for threat in threats:
            controls = existing_controls.get(threat.id, []) if existing_controls else []
            risk = self.calculate_risk(threat, controls)
            risk['threat_name'] = threat.name
            risk['category'] = threat.category.value
            risk_list.append(risk)
        
        return sorted(risk_list, key=lambda x: x['risk_score'], reverse=True)
    
    def calculate_mitigation_cost(self,
                                  threat: Threat,
                                  mitigation_type: str) -> Dict:
        """Estimate cost of mitigation"""
        cost_estimates = {
            'technical_control': {'low': '$5K-25K', 'medium': '$25K-100K', 'high': '$100K+'},
            'process_change': {'low': '$1K-10K', 'medium': '$10K-50K', 'high': '$50K+'},
            'training': {'low': '$1K-5K', 'medium': '$5K-20K', 'high': '$20K+'}
        }
        
        return {
            'mitigation_type': mitigation_type,
            'estimated_cost': cost_estimates.get(mitigation_type, {}).get('medium', 'Unknown'),
            'implementation_time': '1-3 months',
            'effectiveness': 'High',
            'trade_offs': ['May impact user experience', 'Requires ongoing maintenance']
        }


class ThreatReportGenerator:
    """Generate threat model reports"""
    
    def __init__(self):
        self.templates = {}
    
    def generate_executive_summary(self,
                                   project_name: str,
                                   threats: List[Threat],
                                   scope: str) -> str:
        """Generate executive summary"""
        critical = sum(1 for t in threats if t.severity == ThreatSeverity.CRITICAL)
        high = sum(1 for t in threats if t.severity == ThreatSeverity.HIGH)
        medium = sum(1 for t in threats if t.severity == ThreatSeverity.MEDIUM)
        low = sum(1 for t in threats if t.severity == ThreatSeverity.LOW)
        
        return f"""
THREAT MODEL EXECUTIVE SUMMARY
==============================

Project: {project_name}
Assessment Date: {datetime.now().strftime('%Y-%m-%d')}
Scope: {scope}

OVERALL RISK ASSESSMENT
-----------------------
Critical: {critical} threats
High: {high} threats
Medium: {medium} threats
Low: {low} threats

KEY FINDINGS
------------
{critical + high} high-priority threats require immediate attention.
Primary risk categories: Authentication, Data Protection, Access Control.

RECOMMENDATIONS
---------------
1. Implement multi-factor authentication across all user-facing systems
2. Encrypt sensitive data at rest and in transit
3. Apply principle of least privilege to all processes
4. Implement comprehensive logging and monitoring
5. Conduct regular security reviews and updates
"""
    
    def generate_detailed_report(self,
                                 project_name: str,
                                 diagram: Dict,
                                 threats: List[Threat],
                                 mitigations: List[str]) -> Dict:
        """Generate detailed threat model report"""
        return {
            'report_id': f"TM-{datetime.now().strftime('%Y%m%d')}",
            'project': project_name,
            'generated': datetime.now().isoformat(),
            'scope': {
                'elements': diagram.get('elements', 0),
                'data_flows': diagram.get('flows', 0),
                'trust_boundaries': len([e for e in diagram.get('elements', []) if e.get('type') == 'trust_boundary'])
            },
            'threat_summary': {
                'total_threats': len(threats),
                'by_severity': {
                    'critical': sum(1 for t in threats if t.severity == ThreatSeverity.CRITICAL),
                    'high': sum(1 for t in threats if t.severity == ThreatSeverity.HIGH),
                    'medium': sum(1 for t in threats if t.severity == ThreatSeverity.MEDIUM),
                    'low': sum(1 for t in threats if t.severity == ThreatSeverity.LOW)
                },
                'by_category': {}
            },
            'threats': [
                {
                    'id': t.id,
                    'name': t.name,
                    'category': t.category.value,
                    'severity': t.severity.value,
                    'mitigation': t.mitigation,
                    'residual_risk': t.residual_risk
                }
                for t in threats
            ],
            'mitigations_planned': len(mitigations),
            'recommendations': mitigations
        }


class AttackTreeGenerator:
    """Generate attack trees for scenarios"""
    
    def __init__(self):
        self.attackers = {}
    
    def create_attack_tree(self,
                           goal: str,
                           attacker_profile: str = "opportunistic") -> Dict:
        """Create attack tree for common attack goal"""
        return {
            'goal': goal,
            'attacker_profile': attacker_profile,
            'attack_steps': [
                {
                    'step': 1,
                    'description': 'Gain initial access',
                    'methods': [
                        {'method': 'Phishing', 'cost': 'Low', 'success_rate': '15%'},
                        {'method': 'Credential theft', 'cost': 'Low', 'success_rate': '25%'},
                        {'method': 'Exploit vulnerability', 'cost': 'Medium', 'success_rate': '10%'}
                    ]
                },
                {
                    'step': 2,
                    'description': 'Establish persistence',
                    'methods': [
                        {'method': 'Create backdoor', 'cost': 'Low', 'success_rate': '90%'},
                        {'method': 'Modify startup', 'cost': 'Low', 'success_rate': '85%'}
                    ]
                },
                {
                    'step': 3,
                    'description': 'Escalate privileges',
                    'methods': [
                        {'method': 'Exploit local vuln', 'cost': 'Medium', 'success_rate': '30%'},
                        {'method': 'Credential harvesting', 'cost': 'Medium', 'success_rate': '40%'}
                    ]
                },
                {
                    'step': 4,
                    'description': 'Achieve objective',
                    'methods': [
                        {'method': 'Data exfiltration', 'cost': 'Low', 'success_rate': '70%'},
                        {'method': 'Service disruption', 'cost': 'Low', 'success_rate': '60%'}
                    ]
                }
            ],
            'total_paths': 12,
            'easiest_path': 'Phishing → Backdoor → Credential Harvesting → Data Exfiltration',
            'recommended_mitigations': [
                'Implement email filtering and user training',
                'Deploy EDR solutions',
                'Enable MFA for all accounts',
                'Monitor for anomalous behavior'
            ]
        }


if __name__ == "__main__":
    stride = STRIDEAnalyzer()
    threats = stride.analyze_element(DiagramElement(
        id="test-001",
        type="process",
        name="User Authentication",
        description="User login process",
        properties={"confidentiality": "high"},
        trust_level="internal",
        incoming_flows=[],
        outgoing_flows=[]
    ))
    print(f"STRIDE threats found: {len(threats)}")
    
    dfd = DataFlowDiagrammer()
    user = dfd.add_external_entity("User", "End user")
    auth = dfd.add_process("Authentication", "internal")
    db = dfd.add_data_store("User Database", "high")
    dfd.add_data_flow(user, auth, "credentials", "HTTPS")
    dfd.add_data_flow(auth, db, "query", "TLS")
    print(f"DFD elements: {len(dfd.elements)}, flows: {len(dfd.flows)}")
    
    risk = RiskCalculator()
    prioritized = risk.prioritize_threats(threats)
    print(f"Prioritized threats: {len(prioritized)}")
    
    report = ThreatReportGenerator()
    summary = report.generate_executive_summary("Test Project", threats, "Full System")
    print("Report generated successfully")
