"""
Red Team Operations Framework
A comprehensive framework for conducting full-spectrum adversary simulations
and security assessments.
"""

import asyncio
import logging
import hashlib
import json
import random
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from abc import ABC, abstractmethod
import ipaddress
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CampaignPhase(Enum):
    """Phases of red team operations."""
    PLANNING = "planning"
    RECONNAISSANCE = "reconnaissance"
    WEAPONIZATION = "weaponization"
    DELIVERY = "delivery"
    EXPLOITATION = "exploitation"
    INSTALLATION = "installation"
    COMMAND_AND_CONTROL = "command_and_control"
    ACTIONS_ON_OBJECTIVES = "actions_on_objectives"
    CLEANUP = "cleanup"
    REPORTING = "reporting"


class CampaignStatus(Enum):
    """Status of red team campaigns."""
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ThreatActor(Enum):
    """Known threat actor groups."""
    APT28 = "apt28"
    APT29 = "apt29"
    APT41 = "apt41"
    LAZARUS = "lazarus"
    FIN7 = "fin7"
    COBALT_GROUP = "cobalt_group"
    CUSTOM = "custom"


class ObjectiveType(Enum):
    """Types of red team objectives."""
    DATA_EXFILTRATION = "data_exfiltration"
    CREDENTIAL_HARVEST = "credential_harvest"
    PERSISTENCE = "persistence"
    LATERAL_MOVEMENT = "lateral_movement"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DISRUPTION = "disruption"
    INTELLIGENCE_GATHERING = "intelligence_gathering"


class DetectionEvent(Enum):
    """Types of detection events."""
    NETWORK_ALERT = "network_alert"
    HOST_ALERT = "host_alert"
    USER_REPORT = "user_report"
    LOG_ANALYSIS = "log_analysis"
    BEHAVIORAL_ANALYSIS = "behavioral_analysis"
    THREAT_INTEL = "threat_intel"


@dataclass
class EngagementTarget:
    """Represents an engagement target."""
    organization: str
    domain: str
    ip_ranges: List[str]
    critical_assets: List[str]
    excluded_systems: List[str] = field(default_factory=list)
    contact_information: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate target after initialization."""
        if not self.organization:
            raise ValueError("Organization name cannot be empty")
        if not self.domain:
            raise ValueError("Domain cannot be empty")


@dataclass
class CampaignConfig:
    """Configuration for red team campaign."""
    campaign_type: ThreatActor
    duration_days: int = 30
    team_size: int = 5
    infrastructure: List[Dict[str, str]] = field(default_factory=list)
    rules_of_engagement: Dict[str, Any] = field(default_factory=dict)
    objectives: List[ObjectiveType] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    
    @property
    def end_time(self) -> datetime:
        """Calculate campaign end time."""
        return self.start_time + timedelta(days=self.duration_days)


@dataclass
class CampaignResult:
    """Results from a red team campaign."""
    campaign_id: str
    campaign_type: ThreatActor
    start_time: datetime
    end_time: Optional[datetime] = None
    status: CampaignStatus = CampaignStatus.PLANNED
    objectives_achieved: int = 0
    total_objectives: int = 0
    detection_events: int = 0
    time_to_detection: Optional[timedelta] = None
    time_to_response: Optional[timedelta] = None
    findings: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def objectives_achievement_rate(self) -> float:
        """Calculate objectives achievement rate."""
        if self.total_objectives == 0:
            return 0.0
        return (self.objectives_achieved / self.total_objectives) * 100
    
    @property
    def detection_rate(self) -> float:
        """Calculate detection rate."""
        if self.total_objectives == 0:
            return 0.0
        return (self.detection_events / self.total_objectives) * 100


@dataclass
class TTP:
    """MITRE ATT&CK Technique, Tactic, and Procedure."""
    technique_id: str
    technique_name: str
    tactic: str
    description: str
    data_sources: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)
    detection: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert TTP to dictionary."""
        return {
            "technique_id": self.technique_id,
            "technique_name": self.technique_name,
            "tactic": self.tactic,
            "description": self.description,
            "data_sources": self.data_sources,
            "mitigations": self.mitigations,
            "detection": self.detection
        }


@dataclass
class Finding:
    """Red team finding."""
    id: str
    title: str
    description: str
    severity: str
    cvss_score: float
    ttps: List[TTP] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    remediation: str = ""
    business_impact: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert finding to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "cvss_score": self.cvss_score,
            "ttps": [ttp.to_dict() for ttp in self.ttps],
            "evidence": self.evidence,
            "remediation": self.remediation,
            "business_impact": self.business_impact
        }


class TTPMapper:
    """Map MITRE ATT&CK techniques to adversary behavior."""
    
    def __init__(self):
        self.technique_database = self._load_technique_database()
    
    def _load_technique_database(self) -> Dict[str, TTP]:
        """Load MITRE ATT&CK technique database."""
        techniques = {
            "T1566": TTP(
                technique_id="T1566",
                technique_name="Phishing",
                tactic="initial-access",
                description="Adversaries may send phishing messages to gain access to victim systems.",
                data_sources=["Email gateway logs", "User reports"],
                mitigations=["User training", "Email filtering"],
                detection="Monitor email gateway logs for suspicious attachments or links."
            ),
            "T1059": TTP(
                technique_id="T1059",
                technique_name="Command and Scripting Interpreter",
                tactic="execution",
                description="Adversaries may abuse command and script interpreters to execute commands and scripts.",
                data_sources=["Process creation logs", "Command-line auditing"],
                mitigations=["Application whitelisting", "Execution prevention"],
                detection="Monitor process creation and command-line arguments."
            ),
            "T1078": TTP(
                technique_id="T1078",
                technique_name="Valid Accounts",
                tactic="persistence",
                description="Adversaries may obtain and abuse credentials of existing accounts.",
                data_sources=["Authentication logs", "Account usage patterns"],
                mitigations=["Multi-factor authentication", "Privileged account management"],
                detection="Monitor for unusual account usage patterns."
            ),
            "T1021": TTP(
                technique_id="T1021",
                technique_name="Remote Services",
                tactic="lateral-movement",
                description="Adversaries may use valid accounts to log into a service for remote access.",
                data_sources=["Network connection logs", "Service access logs"],
                mitigations=["Network segmentation", "Remote access policies"],
                detection="Monitor for unusual remote service access patterns."
            ),
            "T1048": TTP(
                technique_id="T1048",
                technique_name="Exfiltration Over Alternative Protocol",
                tactic="exfiltration",
                description="Adversaries may steal data by exfiltrating it over a different protocol.",
                data_sources=["Network flow data", "DNS query logs"],
                mitigations=["Network monitoring", "Data loss prevention"],
                detection="Monitor for unusual outbound network traffic."
            )
        }
        return techniques
    
    def map_techniques(
        self,
        adversary: str,
        target_environment: str,
        capabilities: List[str] = None
    ) -> List[TTP]:
        """Map techniques to adversary behavior."""
        if capabilities is None:
            capabilities = []
        
        # Filter techniques based on capabilities
        mapped_techniques = []
        
        for technique_id, technique in self.technique_database.items():
            # Simple mapping logic
            if "phishing" in capabilities and technique.tactic == "initial-access":
                mapped_techniques.append(technique)
            elif "execution" in capabilities and technique.tactic == "execution":
                mapped_techniques.append(technique)
            elif "persistence" in capabilities and technique.tactic == "persistence":
                mapped_techniques.append(technique)
            elif "lateral_movement" in capabilities and technique.tactic == "lateral-movement":
                mapped_techniques.append(technique)
            elif "exfiltration" in capabilities and technique.tactic == "exfiltration":
                mapped_techniques.append(technique)
        
        # If no specific capabilities, return all techniques
        if not capabilities:
            mapped_techniques = list(self.technique_database.values())
        
        return mapped_techniques


class AdversaryEmulator:
    """Emulate adversary behavior."""
    
    def __init__(self, threat_actor: ThreatActor, mitre_attack_mapping: bool = True):
        self.threat_actor = threat_actor
        self.mitre_attack_mapping = mitre_attack_mapping
        self.ttp_mapper = TTPMapper()
        self.execution_results = []
    
    def execute_technique(self, technique: TTP) -> Dict[str, Any]:
        """Execute a specific technique."""
        logger.info(f"Executing technique: {technique.technique_id} - {technique.technique_name}")
        
        # Simulate technique execution
        result = {
            "technique_id": technique.technique_id,
            "technique_name": technique.technique_name,
            "success": random.random() > 0.3,
            "detected": random.random() > 0.7,
            "timestamp": datetime.now(),
            "details": {
                "target": "example.com",
                "method": technique.tactic,
                "outcome": "success" if random.random() > 0.3 else "failure"
            }
        }
        
        self.execution_results.append(result)
        return result
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of execution results."""
        total_techniques = len(self.execution_results)
        successful = sum(1 for r in self.execution_results if r["success"])
        detected = sum(1 for r in self.execution_results if r["detected"])
        
        return {
            "threat_actor": self.threat_actor.value,
            "total_techniques": total_techniques,
            "successful_techniques": successful,
            "detected_techniques": detected,
            "success_rate": (successful / total_techniques * 100) if total_techniques > 0 else 0,
            "detection_rate": (detected / total_techniques * 100) if total_techniques > 0 else 0
        }


class IncidentResponseTest:
    """Test incident response capabilities."""
    
    def __init__(self, name: str, test_scenarios: List[str] = None):
        self.name = name
        self.test_scenarios = test_scenarios or []
        self.results = []
    
    def execute_scenario(self, scenario: str) -> Dict[str, Any]:
        """Execute a test scenario."""
        logger.info(f"Executing scenario: {scenario}")
        
        # Simulate scenario execution
        result = {
            "scenario": scenario,
            "success": random.random() > 0.4,
            "time_to_detection": random.randint(5, 120),
            "response_effectiveness": random.randint(60, 100),
            "timestamp": datetime.now()
        }
        
        self.results.append(result)
        return result
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get summary of test results."""
        total_scenarios = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        avg_detection_time = sum(r["time_to_detection"] for r in self.results) / total_scenarios if total_scenarios > 0 else 0
        avg_response_effectiveness = sum(r["response_effectiveness"] for r in self.results) / total_scenarios if total_scenarios > 0 else 0
        
        return {
            "total_scenarios": total_scenarios,
            "successful_scenarios": successful,
            "average_detection_time": avg_detection_time,
            "average_response_effectiveness": avg_response_effectiveness
        }


class DetectionValidation:
    """Validate detection capabilities."""
    
    def __init__(self, scenario: str, time_to_detection: int, response_effectiveness: int):
        self.scenario = scenario
        self.time_to_detection = time_to_detection
        self.response_effectiveness = response_effectiveness
    
    def get_detection_score(self) -> float:
        """Calculate detection score."""
        # Weighted score based on detection time and response effectiveness
        time_score = max(0, 100 - (self.time_to_detection / 2))
        response_score = self.response_effectiveness
        
        return (time_score * 0.6) + (response_score * 0.4)
    
    def get_recommendations(self) -> List[str]:
        """Get improvement recommendations."""
        recommendations = []
        
        if self.time_to_detection > 60:
            recommendations.append("Improve detection capabilities to reduce time to detection")
        
        if self.response_effectiveness < 80:
            recommendations.append("Enhance incident response procedures and training")
        
        if not recommendations:
            recommendations.append("Maintain current detection and response capabilities")
        
        return recommendations


class RedTeamCampaign:
    """Red team campaign management."""
    
    def __init__(
        self,
        name: str,
        target_organization: str,
        threat_actor: ThreatActor = ThreatActor.CUSTOM,
        objectives: List[ObjectiveType] = None
    ):
        self.name = name
        self.target_organization = target_organization
        self.threat_actor = threat_actor
        self.objectives = objectives or []
        self.config = None
        self.status = CampaignStatus.PLANNED
        self.findings = []
        self.start_time = None
        self.end_time = None
    
    def configure(self, **kwargs) -> None:
        """Configure campaign settings."""
        self.config = CampaignConfig(
            campaign_type=self.threat_actor,
            **kwargs
        )
        logger.info(f"Configured red team campaign: {self.name}")
    
    def execute(self) -> str:
        """Execute red team campaign."""
        if not self.config:
            raise ValueError("Campaign not configured")
        
        self.status = CampaignStatus.ACTIVE
        self.start_time = datetime.now()
        campaign_id = hashlib.md5(self.name.encode()).hexdigest()[:8]
        
        logger.info(f"Executing red team campaign: {self.name} (ID: {campaign_id})")
        
        # Simulate campaign execution
        self._execute_phases()
        
        self.status = CampaignStatus.COMPLETED
        self.end_time = datetime.now()
        
        return campaign_id
    
    def _execute_phases(self) -> None:
        """Execute campaign phases."""
        phases = [
            CampaignPhase.RECONNAISSANCE,
            CampaignPhase.WEAPONIZATION,
            CampaignPhase.DELIVERY,
            CampaignPhase.EXPLOITATION,
            CampaignPhase.INSTALLATION,
            CampaignPhase.COMMAND_AND_CONTROL,
            CampaignPhase.ACTIONS_ON_OBJECTIVES,
            CampaignPhase.CLEANUP
        ]
        
        for phase in phases:
            logger.info(f"Executing phase: {phase.value}")
            # Simulate phase execution
            phase_findings = self._simulate_phase_execution(phase)
            self.findings.extend(phase_findings)
    
    def _simulate_phase_execution(self, phase: CampaignPhase) -> List[Finding]:
        """Simulate phase execution and generate findings."""
        findings = []
        
        if phase == CampaignPhase.EXPLOITATION:
            # Simulate exploitation finding
            finding = Finding(
                id=f"finding_{len(self.findings) + 1}",
                title="Remote Code Execution Vulnerability",
                description="Critical vulnerability allows remote code execution",
                severity="critical",
                cvss_score=9.8,
                ttps=[
                    TTP(
                        technique_id="T1190",
                        technique_name="Exploit Public-Facing Application",
                        tactic="initial-access",
                        description="Adversary exploited public-facing application"
                    )
                ],
                evidence=["Exploit code executed successfully", "Shell access obtained"],
                remediation="Patch vulnerable application immediately",
                business_impact="Complete system compromise possible"
            )
            findings.append(finding)
        
        elif phase == CampaignPhase.ACTIONS_ON_OBJECTIVES:
            # Simulate data exfiltration finding
            finding = Finding(
                id=f"finding_{len(self.findings) + 1}",
                title="Data Exfiltration via DNS",
                description="Sensitive data exfiltrated using DNS tunneling",
                severity="high",
                cvss_score=7.5,
                ttps=[
                    TTP(
                        technique_id="T1048",
                        technique_name="Exfiltration Over Alternative Protocol",
                        tactic="exfiltration",
                        description="Data exfiltrated over DNS protocol"
                    )
                ],
                evidence=["DNS queries to external server", "Encoded data in DNS requests"],
                remediation="Implement DNS monitoring and blocking",
                business_impact="Confidential data exposure"
            )
            findings.append(finding)
        
        return findings
    
    def add_finding(self, finding: Finding) -> None:
        """Add a finding to the campaign."""
        self.findings.append(finding)
    
    def get_results(self) -> Dict[str, Any]:
        """Get campaign results."""
        return {
            "campaign_id": self.name,
            "threat_actor": self.threat_actor.value,
            "status": self.status.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "findings": [f.to_dict() for f in self.findings],
            "total_findings": len(self.findings),
            "critical_findings": sum(1 for f in self.findings if f.severity == "critical"),
            "high_findings": sum(1 for f in self.findings if f.severity == "high")
        }


class CampaignManager:
    """Manage multiple red team campaigns."""
    
    def __init__(self):
        self.campaigns = {}
        self.results = {}
    
    def execute_campaign(self, campaign: RedTeamCampaign) -> str:
        """Execute a campaign and return its ID."""
        campaign_id = campaign.execute()
        self.campaigns[campaign_id] = campaign
        self.results[campaign_id] = campaign.get_results()
        return campaign_id
    
    def is_complete(self, campaign_id: str) -> bool:
        """Check if campaign is complete."""
        if campaign_id not in self.campaigns:
            return False
        return self.campaigns[campaign_id].status == CampaignStatus.COMPLETED
    
    def get_status(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign status."""
        if campaign_id not in self.campaigns:
            return {}
        
        campaign = self.campaigns[campaign_id]
        return {
            "campaign_id": campaign_id,
            "status": campaign.status.value,
            "current_phase": "reporting" if campaign.status == CampaignStatus.COMPLETED else "active",
            "objectives_completed": len(campaign.findings),
            "total_objectives": len(campaign.objectives),
            "detection_events": sum(1 for f in campaign.findings if f.severity in ["high", "critical"])
        }
    
    def get_results(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign results."""
        return self.results.get(campaign_id, {})
    
    def list_campaigns(self) -> List[str]:
        """List all campaigns."""
        return list(self.campaigns.keys())
    
    def get_overall_statistics(self) -> Dict[str, Any]:
        """Get overall statistics across all campaigns."""
        total_campaigns = len(self.campaigns)
        total_findings = sum(r.get("total_findings", 0) for r in self.results.values())
        critical_findings = sum(r.get("critical_findings", 0) for r in self.results.values())
        
        return {
            "total_campaigns": total_campaigns,
            "total_findings": total_findings,
            "critical_findings": critical_findings,
            "average_findings_per_campaign": total_findings / total_campaigns if total_campaigns > 0 else 0
        }


class CampaignReport:
    """Generate red team campaign reports."""
    
    def __init__(
        self,
        campaign_id: str,
        report_type: str = "comprehensive",
        include_technical_details: bool = True,
        include_recommendations: bool = True
    ):
        self.campaign_id = campaign_id
        self.report_type = report_type
        self.include_technical_details = include_technical_details
        self.include_recommendations = include_recommendations
        self.content = self._generate_content()
    
    def _generate_content(self) -> Dict[str, Any]:
        """Generate report content."""
        return {
            "executive_summary": "This report summarizes the results of red team operations.",
            "key_findings": [
                "Critical vulnerability identified in public-facing application",
                "Data exfiltration via DNS tunneling detected",
                "Weak credential management practices"
            ],
            "recommendations": [
                "Implement immediate patching for critical vulnerabilities",
                "Deploy DNS monitoring and blocking capabilities",
                "Enhance credential management and rotation policies"
            ] if self.include_recommendations else [],
            "technical_details": {
                "attack_vectors": ["phishing", "web exploitation", "lateral movement"],
                "tools_used": ["custom exploit", "c2 framework", "credential harvester"],
                "infrastructure": ["cloud c2 server", "phishing infrastructure"]
            } if self.include_technical_details else {},
            "appendices": []
        }
    
    def get_key_metrics(self) -> Dict[str, Any]:
        """Get key metrics for the report."""
        return {
            "objectives_achieved": 3,
            "total_objectives": 5,
            "mean_time_to_detection": "2.5 hours",
            "mean_time_to_response": "4.2 hours",
            "detection_rate": "60%",
            "overall_risk_rating": "high"
        }
    
    def export_to_pdf(self, filename: str) -> None:
        """Export report to PDF."""
        logger.info(f"Exporting report to PDF: {filename}")
        # Simulate PDF export
    
    def export_to_json(self, filename: str) -> None:
        """Export report to JSON."""
        logger.info(f"Exporting report to JSON: {filename}")
        # Simulate JSON export


class ExecutiveSummary:
    """Generate executive summary for red team engagements."""
    
    def __init__(
        self,
        campaign_results: Dict[str, Any],
        key_findings: List[str],
        risk_assessment: Dict[str, Any]
    ):
        self.campaign_results = campaign_results
        self.key_findings = key_findings
        self.risk_assessment = risk_assessment
        self.content = self._generate_content()
    
    def _generate_content(self) -> Dict[str, Any]:
        """Generate executive summary content."""
        return {
            "engagement_overview": "Red team engagement conducted to assess security posture.",
            "key_findings": self.key_findings,
            "risk_assessment": self.risk_assessment,
            "business_impact": "Potential impact on business operations and data security.",
            "recommendations": [
                "Prioritize critical vulnerability remediation",
                "Enhance security monitoring capabilities",
                "Improve incident response procedures"
            ],
            "conclusion": "The organization has areas for improvement in security controls."
        }
    
    def export_to_pdf(self, filename: str) -> None:
        """Export executive summary to PDF."""
        logger.info(f"Exporting executive summary to PDF: {filename}")
        # Simulate PDF export


async def main():
    """Main demonstration function."""
    print("=" * 60)
    print("Red Team Operations Framework Demonstration")
    print("=" * 60)
    
    # Create engagement target
    target = EngagementTarget(
        organization="Example Corporation",
        domain="example.com",
        ip_ranges=["192.168.0.0/16", "10.0.0.0/8"],
        critical_assets=["web application", "database servers", "file shares"],
        excluded_systems=["production databases", "backup systems"],
        contact_information={
            "security_team": "security@example.com",
            "emergency": "emergency@example.com"
        }
    )
    
    print(f"Target Organization: {target.organization}")
    print(f"Domain: {target.domain}")
    print(f"Critical Assets: {target.critical_assets}")
    
    # Demo 1: Red Team Campaign
    print("\n" + "=" * 60)
    print("Demo 1: Red Team Campaign")
    print("=" * 60)
    
    # Create red team campaign
    campaign = RedTeamCampaign(
        name="APT28 Emulation Campaign",
        target_organization=target.organization,
        threat_actor=ThreatActor.APT28,
        objectives=[
            ObjectiveType.DATA_EXFILTRATION,
            ObjectiveType.CREDENTIAL_HARVEST,
            ObjectiveType.PERSISTENCE
        ]
    )
    
    # Configure campaign
    campaign.configure(
        duration_days=30,
        team_size=5,
        infrastructure=[
            {"type": "c2_server", "location": "cloud"},
            {"type": "phishing_server", "location": "cloud"},
            {"type": "exfil_server", "location": "bulletproof"}
        ],
        rules_of_engagement={
            "no_destructive_actions": True,
            "business_hours_only": False,
            "emergency_contact": "security@example.com"
        }
    )
    
    # Execute campaign
    campaign_manager = CampaignManager()
    campaign_id = campaign_manager.execute_campaign(campaign)
    print(f"Campaign ID: {campaign_id}")
    
    # Get campaign status
    status = campaign_manager.get_status(campaign_id)
    print(f"Phase: {status['current_phase']}")
    print(f"Objectives completed: {status['objectives_completed']}/{status['total_objectives']}")
    print(f"Detection events: {status['detection_events']}")
    
    # Demo 2: Adversary Emulation
    print("\n" + "=" * 60)
    print("Demo 2: Adversary Emulation")
    print("=" * 60)
    
    # Initialize adversary emulator
    emulator = AdversaryEmulator(
        threat_actor=ThreatActor.APT29,
        mitre_attack_mapping=True
    )
    
    # Map TTPs
    ttp_mapper = TTPMapper()
    techniques = ttp_mapper.map_techniques(
        adversary="APT29",
        target_environment="cloud",
        capabilities=["phishing", "execution", "persistence", "exfiltration"]
    )
    
    print(f"Mapped {len(techniques)} techniques")
    
    # Execute techniques
    for technique in techniques[:3]:  # Execute first 3 techniques
        result = emulator.execute_technique(technique)
        print(f"Technique: {result['technique_id']} - {result['technique_name']}")
        print(f"  Success: {result['success']}")
        print(f"  Detected: {result['detected']}")
    
    # Get execution summary
    execution_summary = emulator.get_execution_summary()
    print(f"\nExecution Summary:")
    print(f"  Total techniques: {execution_summary['total_techniques']}")
    print(f"  Success rate: {execution_summary['success_rate']:.1f}%")
    print(f"  Detection rate: {execution_summary['detection_rate']:.1f}%")
    
    # Demo 3: Incident Response Testing
    print("\n" + "=" * 60)
    print("Demo 3: Incident Response Testing")
    print("=" * 60)
    
    # Initialize IR test
    ir_test = IncidentResponseTest(
        name="Incident Response Validation",
        test_scenarios=["credential_theft", "data_exfiltration", "ransomware_deployment"]
    )
    
    # Execute scenarios
    for scenario in ir_test.test_scenarios:
        result = ir_test.execute_scenario(scenario)
        print(f"Scenario: {result['scenario']}")
        print(f"  Success: {result['success']}")
        print(f"  Time to detection: {result['time_to_detection']} minutes")
        print(f"  Response effectiveness: {result['response_effectiveness']}%")
    
    # Get results summary
    ir_summary = ir_test.get_results_summary()
    print(f"\nIR Test Summary:")
    print(f"  Total scenarios: {ir_summary['total_scenarios']}")
    print(f"  Average detection time: {ir_summary['average_detection_time']:.1f} minutes")
    print(f"  Average response effectiveness: {ir_summary['average_response_effectiveness']:.1f}%")
    
    # Demo 4: Campaign Reporting
    print("\n" + "=" * 60)
    print("Demo 4: Campaign Reporting")
    print("=" * 60)
    
    # Generate campaign report
    report = CampaignReport(
        campaign_id=campaign_id,
        report_type="comprehensive",
        include_technical_details=True,
        include_recommendations=True
    )
    
    # Get key metrics
    metrics = report.get_key_metrics()
    print(f"Report Metrics:")
    print(f"  Objectives achieved: {metrics['objectives_achieved']}/{metrics['total_objectives']}")
    print(f"  Mean time to detection: {metrics['mean_time_to_detection']}")
    print(f"  Mean time to response: {metrics['mean_time_to_response']}")
    print(f"  Overall risk rating: {metrics['overall_risk_rating']}")
    
    # Generate executive summary
    exec_summary = ExecutiveSummary(
        campaign_results=campaign_manager.get_results(campaign_id),
        key_findings=report.content["key_findings"],
        risk_assessment={"overall_risk": "high", "critical_issues": 2}
    )
    
    print(f"\nExecutive Summary:")
    print(f"  Engagement overview: {exec_summary.content['engagement_overview']}")
    print(f"  Key findings: {len(exec_summary.content['key_findings'])}")
    print(f"  Recommendations: {len(exec_summary.content['recommendations'])}")
    
    # Get overall statistics
    overall_stats = campaign_manager.get_overall_statistics()
    print(f"\nOverall Statistics:")
    print(f"  Total campaigns: {overall_stats['total_campaigns']}")
    print(f"  Total findings: {overall_stats['total_findings']}")
    print(f"  Critical findings: {overall_stats['critical_findings']}")
    
    print("\n" + "=" * 60)
    print("Demonstration completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())