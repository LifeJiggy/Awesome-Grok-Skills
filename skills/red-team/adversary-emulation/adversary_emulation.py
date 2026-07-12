"""
Adversary Emulation Framework
A comprehensive framework for simulating real-world threat actors
and their tactics, techniques, and procedures (TTPs).
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
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdversaryGroup(Enum):
    """Known adversary groups."""
    APT28 = "apt28"
    APT29 = "apt29"
    APT41 = "apt41"
    LAZARUS = "lazarus"
    FIN7 = "fin7"
    COBALT_GROUP = "cobalt_group"
    TURLA = "turla"
    FANCY_BEAR = "fancy_bear"
    COZY_BEAR = "cozy_bear"
    CUSTOM = "custom"


class Tactic(Enum):
    """MITRE ATT&CK tactics."""
    RECONNAISSANCE = "reconnaissance"
    RESOURCE_DEVELOPMENT = "resource-development"
    INITIAL_ACCESS = "initial-access"
    EXECUTION = "execution"
    PERSISTENCE = "persistence"
    PRIVILEGE_ESCALATION = "privilege-escalation"
    DEFENSE_EVASION = "defense-evasion"
    CREDENTIAL_ACCESS = "credential-access"
    DISCOVERY = "discovery"
    LATERAL_MOVEMENT = "lateral-movement"
    COLLECTION = "collection"
    COMMAND_AND_CONTROL = "command-and-control"
    EXFILTRATION = "exfiltration"
    IMPACT = "impact"


class DetectionConfidence(Enum):
    """Confidence in detection capabilities."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class EmulationPhase(Enum):
    """Phases of adversary emulation."""
    PLANNING = "planning"
    INTELLIGENCE_GATHERING = "intelligence-gathering"
    INFRASTRUCTURE_SETUP = "infrastructure-setup"
    WEAPONIZATION = "weaponization"
    DELIVERY = "delivery"
    EXPLOITATION = "exploitation"
    INSTALLATION = "installation"
    COMMAND_AND_CONTROL = "command-and-control"
    ACTIONS_ON_OBJECTIVES = "actions-on-objectives"
    CLEANUP = "cleanup"


@dataclass
class Technique:
    """MITRE ATT&CK technique."""
    technique_id: str
    technique_name: str
    tactic: Tactic
    description: str
    data_sources: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)
    detection: str = ""
    platforms: List[str] = field(default_factory=list)
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert technique to dictionary."""
        return {
            "technique_id": self.technique_id,
            "technique_name": self.technique_name,
            "tactic": self.tactic.value,
            "description": self.description,
            "data_sources": self.data_sources,
            "mitigations": self.mitigations,
            "detection": self.detection,
            "platforms": self.platforms,
            "version": self.version
        }


@dataclass
class AdversaryProfile:
    """Adversary group profile."""
    name: str
    description: str
    origin_country: str = ""
    motivation: str = ""
    target_sectors: List[str] = field(default_factory=list)
    ttps: List[Technique] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    infrastructure: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "origin_country": self.origin_country,
            "motivation": self.motivation,
            "target_sectors": self.target_sectors,
            "ttps_count": len(self.ttps),
            "tools": self.tools,
            "infrastructure": self.infrastructure,
            "aliases": self.aliases
        }


@dataclass
class EmulationCampaign:
    """Adversary emulation campaign."""
    campaign_id: str
    adversary: AdversaryGroup
    objectives: List[str]
    start_time: datetime
    end_time: Optional[datetime] = None
    team_size: int = 3
    infrastructure: List[Dict[str, str]] = field(default_factory=list)
    rules_of_engagement: Dict[str, Any] = field(default_factory=dict)
    status: str = "planned"
    
    @property
    def duration_days(self) -> int:
        """Calculate campaign duration."""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).days
        return 0


@dataclass
class EmulationResult:
    """Results from adversary emulation."""
    campaign_id: str
    adversary: AdversaryGroup
    techniques_executed: int = 0
    techniques_detected: int = 0
    detection_rate: float = 0.0
    mean_time_to_detection: float = 0.0
    mean_time_to_response: float = 0.0
    objectives_achieved: int = 0
    total_objectives: int = 0
    findings: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def objectives_achievement_rate(self) -> float:
        """Calculate objectives achievement rate."""
        if self.total_objectives == 0:
            return 0.0
        return (self.objectives_achieved / self.total_objectives) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "campaign_id": self.campaign_id,
            "adversary": self.adversary.value,
            "techniques_executed": self.techniques_executed,
            "techniques_detected": self.techniques_detected,
            "detection_rate": self.detection_rate,
            "mean_time_to_detection": self.mean_time_to_detection,
            "mean_time_to_response": self.mean_time_to_response,
            "objectives_achieved": self.objectives_achieved,
            "total_objectives": self.total_objectives,
            "objectives_achievement_rate": self.objectives_achievement_rate
        }


@dataclass
class DetectionAlert:
    """Security detection alert."""
    alert_id: str
    technique: Technique
    timestamp: datetime
    source: str
    confidence: DetectionConfidence
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            "alert_id": self.alert_id,
            "technique_id": self.technique.technique_id,
            "technique_name": self.technique.technique_name,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "confidence": self.confidence.value,
            "details": self.details
        }


class TechniqueLibrary:
    """Library of MITRE ATT&CK techniques."""
    
    def __init__(self):
        self.techniques = self._load_technique_library()
    
    def _load_technique_library(self) -> Dict[str, Technique]:
        """Load technique library."""
        techniques = {
            "T1566": Technique(
                technique_id="T1566",
                technique_name="Phishing",
                tactic=Tactic.INITIAL_ACCESS,
                description="Adversaries may send phishing messages to gain access to victim systems.",
                data_sources=["Email gateway logs", "User reports"],
                mitigations=["User training", "Email filtering"],
                detection="Monitor email gateway logs for suspicious attachments or links.",
                platforms=["Windows", "Linux", "macOS"]
            ),
            "T1059": Technique(
                technique_id="T1059",
                technique_name="Command and Scripting Interpreter",
                tactic=Tactic.EXECUTION,
                description="Adversaries may abuse command and script interpreters to execute commands and scripts.",
                data_sources=["Process creation logs", "Command-line auditing"],
                mitigations=["Application whitelisting", "Execution prevention"],
                detection="Monitor process creation and command-line arguments.",
                platforms=["Windows", "Linux", "macOS"]
            ),
            "T1078": Technique(
                technique_id="T1078",
                technique_name="Valid Accounts",
                tactic=Tactic.PERSISTENCE,
                description="Adversaries may obtain and abuse credentials of existing accounts.",
                data_sources=["Authentication logs", "Account usage patterns"],
                mitigations=["Multi-factor authentication", "Privileged account management"],
                detection="Monitor for unusual account usage patterns.",
                platforms=["Windows", "Linux", "macOS"]
            ),
            "T1021": Technique(
                technique_id="T1021",
                technique_name="Remote Services",
                tactic=Tactic.LATERAL_MOVEMENT,
                description="Adversaries may use valid accounts to log into a service for remote access.",
                data_sources=["Network connection logs", "Service access logs"],
                mitigations=["Network segmentation", "Remote access policies"],
                detection="Monitor for unusual remote service access patterns.",
                platforms=["Windows", "Linux", "macOS"]
            ),
            "T1048": Technique(
                technique_id="T1048",
                technique_name="Exfiltration Over Alternative Protocol",
                tactic=Tactic.EXFILTRATION,
                description="Adversaries may steal data by exfiltrating it over a different protocol.",
                data_sources=["Network flow data", "DNS query logs"],
                mitigations=["Network monitoring", "Data loss prevention"],
                detection="Monitor for unusual outbound network traffic.",
                platforms=["Windows", "Linux", "macOS"]
            ),
            "T1053": Technique(
                technique_id="T1053",
                technique_name="Scheduled Task/Job",
                tactic=Tactic.EXECUTION,
                description="Adversaries may abuse task scheduling functionality to facilitate execution.",
                data_sources=["Scheduled task logs", "Process creation logs"],
                mitigations=["Audit scheduled task creation", "Restrict access to scheduling tools"],
                detection="Monitor scheduled task creation and modification.",
                platforms=["Windows", "Linux", "macOS"]
            )
        }
        return techniques
    
    def get_techniques(
        self,
        adversary: str,
        categories: List[str] = None
    ) -> List[Technique]:
        """Get techniques for specific adversary."""
        if categories is None:
            categories = []
        
        # Filter techniques by categories
        filtered_techniques = []
        
        for technique in self.techniques.values():
            if not categories or technique.tactic.value in categories:
                filtered_techniques.append(technique)
        
        return filtered_techniques
    
    def get_technique_by_id(self, technique_id: str) -> Optional[Technique]:
        """Get technique by ID."""
        return self.techniques.get(technique_id)


class TTPImplementer:
    """Implement adversary TTPs."""
    
    def __init__(self):
        self.implementations = {}
        self.execution_results = []
    
    def implement_technique(self, technique: Technique) -> 'TechniqueImplementation':
        """Implement a specific technique."""
        logger.info(f"Implementing technique: {technique.technique_id} - {technique.technique_name}")
        
        implementation = TechniqueImplementation(
            technique=technique,
            implementation_date=datetime.now(),
            status="implemented"
        )
        
        self.implementations[technique.technique_id] = implementation
        return implementation
    
    def get_implementation(self, technique_id: str) -> Optional['TechniqueImplementation']:
        """Get implementation by technique ID."""
        return self.implementations.get(technique_id)
    
    def execute_all(self) -> List[Dict[str, Any]]:
        """Execute all implementations."""
        results = []
        
        for technique_id, implementation in self.implementations.items():
            result = implementation.execute()
            results.append(result)
            self.execution_results.append(result)
        
        return results
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        total_implementations = len(self.implementations)
        successful = sum(1 for r in self.execution_results if r.get("success", False))
        detected = sum(1 for r in self.execution_results if r.get("detected", False))
        
        return {
            "total_implementations": total_implementations,
            "successful_implementations": successful,
            "detected_implementations": detected,
            "success_rate": (successful / total_implementations * 100) if total_implementations > 0 else 0,
            "detection_rate": (detected / total_implementations * 100) if total_implementations > 0 else 0
        }


class TechniqueImplementation:
    """Implementation of a specific technique."""
    
    def __init__(self, technique: Technique, implementation_date: datetime, status: str):
        self.technique = technique
        self.implementation_date = implementation_date
        self.status = status
        self.execution_history = []
    
    def test(self) -> Dict[str, Any]:
        """Test technique implementation."""
        logger.info(f"Testing implementation: {self.technique.technique_id}")
        
        # Simulate testing
        result = {
            "technique_id": self.technique.technique_id,
            "success": random.random() > 0.3,
            "detected": random.random() > 0.7,
            "timestamp": datetime.now(),
            "details": {
                "method": self.technique.tactic.value,
                "outcome": "success" if random.random() > 0.3 else "failure"
            }
        }
        
        self.execution_history.append(result)
        return result
    
    def execute(self) -> Dict[str, Any]:
        """Execute technique implementation."""
        return self.test()


class AdversaryEmulator:
    """Main adversary emulation engine."""
    
    def __init__(
        self,
        threat_actor: AdversaryGroup,
        mitre_attack_mapping: bool = True,
        fidelity_level: str = "medium"
    ):
        self.threat_actor = threat_actor
        self.mitre_attack_mapping = mitre_attack_mapping
        self.fidelity_level = fidelity_level
        self.ttp_implementer = TTPImplementer()
        self.technique_library = TechniqueLibrary()
        self.execution_results = []
        self.campaign = None
    
    def configure(self, campaign: EmulationCampaign) -> None:
        """Configure emulator with campaign settings."""
        self.campaign = campaign
        logger.info(f"Configured emulator for {self.threat_actor.value} campaign")
    
    def execute(self) -> EmulationResult:
        """Execute adversary emulation."""
        logger.info(f"Executing adversary emulation: {self.threat_actor.value}")
        
        # Execute TTPs
        results = self.ttp_implementer.execute_all()
        self.execution_results = results
        
        # Analyze results
        analysis = self.analyze_results()
        
        return analysis
    
    def analyze_results(self) -> EmulationResult:
        """Analyze emulation results."""
        total_techniques = len(self.execution_results)
        detected = sum(1 for r in self.execution_results if r.get("detected", False))
        
        # Calculate mean time to detection (simulated)
        mttd = random.uniform(5, 60) if detected > 0 else 0
        mttr = random.uniform(10, 120) if detected > 0 else 0
        
        result = EmulationResult(
            campaign_id=self.campaign.campaign_id if self.campaign else "unknown",
            adversary=self.threat_actor,
            techniques_executed=total_techniques,
            techniques_detected=detected,
            detection_rate=(detected / total_techniques * 100) if total_techniques > 0 else 0,
            mean_time_to_detection=mttd,
            mean_time_to_response=mttr,
            objectives_achieved=random.randint(1, 3),
            total_objectives=3,
            findings=self._generate_findings()
        )
        
        return result
    
    def _generate_findings(self) -> List[Dict[str, Any]]:
        """Generate findings from emulation."""
        findings = []
        
        # Simulate findings generation
        finding_templates = [
            {
                "title": "Weak Credential Management",
                "description": "Default or weak credentials found on critical systems",
                "severity": "high",
                "cvss_score": 7.5
            },
            {
                "title": "Insufficient Network Segmentation",
                "description": "Lateral movement possible between network segments",
                "severity": "medium",
                "cvss_score": 5.3
            },
            {
                "title": "Inadequate Logging and Monitoring",
                "description": "Insufficient logging for detecting adversary activities",
                "severity": "medium",
                "cvss_score": 5.0
            }
        ]
        
        for i, template in enumerate(finding_templates):
            finding = {
                "id": f"finding_{i+1}",
                "title": template["title"],
                "description": template["description"],
                "severity": template["severity"],
                "cvss_score": template["cvss_score"],
                "evidence": [f"Adversary technique {random.choice(['T1566', 'T1059', 'T1078'])} executed successfully"],
                "remediation": f"Implement controls to address {template['title'].lower()}"
            }
            findings.append(finding)
        
        return findings
    
    def execute_technique(self, technique: Technique) -> Dict[str, Any]:
        """Execute a specific technique."""
        implementation = self.ttp_implementer.implement_technique(technique)
        return implementation.execute()


class DetectionValidator:
    """Validate detection capabilities."""
    
    def __init__(
        self,
        adversary: AdversaryGroup,
        validation_scope: List[str] = None
    ):
        self.adversary = adversary
        self.validation_scope = validation_scope or ["network_detection", "host_detection"]
        self.alerts = []
        self.validation_results = []
    
    def validate(self) -> List[DetectionAlert]:
        """Validate detection capabilities."""
        logger.info(f"Validating detection for {self.adversary.value}")
        
        # Simulate validation
        alerts = [
            DetectionAlert(
                alert_id=f"alert_{i}",
                technique=Technique(
                    technique_id=f"T{1000+i}",
                    technique_name=f"Technique {i}",
                    tactic=Tactic.EXECUTION,
                    description=f"Test technique {i}"
                ),
                timestamp=datetime.now() - timedelta(minutes=random.randint(1, 60)),
                source=random.choice(["siem", "edr", "network_ids"]),
                confidence=random.choice(list(DetectionConfidence)),
                details={"test": True}
            )
            for i in range(5)
        ]
        
        self.alerts = alerts
        return alerts
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        total_alerts = len(self.alerts)
        true_positives = sum(1 for a in self.alerts if a.confidence in [DetectionConfidence.HIGH, DetectionConfidence.MEDIUM])
        
        return {
            "total_alerts": total_alerts,
            "true_positives": true_positives,
            "false_positives": total_alerts - true_positives,
            "detection_coverage": (true_positives / total_alerts * 100) if total_alerts > 0 else 0,
            "mean_confidence": sum(1 if a.confidence == DetectionConfidence.HIGH else 0.5 if a.confidence == DetectionConfidence.MEDIUM else 0 for a in self.alerts) / total_alerts if total_alerts > 0 else 0
        }


class AlertAnalyzer:
    """Analyze security alerts."""
    
    def __init__(self):
        self.alerts = []
    
    def analyze_alerts(
        self,
        time_range: str = "campaign_duration",
        alert_sources: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze alerts from specified sources."""
        if alert_sources is None:
            alert_sources = ["siem", "edr", "network_ids"]
        
        logger.info(f"Analyzing alerts from {alert_sources}")
        
        # Simulate alert analysis
        analysis = {
            "time_range": time_range,
            "alert_sources": alert_sources,
            "total_alerts": random.randint(50, 200),
            "true_positives": random.randint(20, 80),
            "false_positives": random.randint(10, 50),
            "mean_response_time": random.uniform(5, 30),
            "coverage_percentage": random.uniform(60, 95)
        }
        
        return analysis


class AdversaryProfileManager:
    """Manage adversary profiles."""
    
    def __init__(self):
        self.profiles = {}
        self.builtin_profiles = self._load_builtin_profiles()
    
    def _load_builtin_profiles(self) -> Dict[str, AdversaryProfile]:
        """Load built-in adversary profiles."""
        profiles = {
            "apt28": AdversaryProfile(
                name="APT28",
                description="Russian military intelligence cyber espionage group",
                origin_country="Russia",
                motivation="Espionage, information theft",
                target_sectors=["government", "military", "media"],
                tools=["X-Agent", "X-Tunnel", "Zebrocy"],
                infrastructure=["bulletproof_hosting", "domain_fronting"],
                aliases=["Fancy Bear", "Pawn Storm", "Sofacy"]
            ),
            "apt29": AdversaryProfile(
                name="APT29",
                description="Russian intelligence cyber espionage group",
                origin_country="Russia",
                motivation="Espionage, information theft",
                target_sectors=["government", "think_tanks", "technology"],
                tools=["WellMess", "WellMail", "Cobalt Strike"],
                infrastructure=["compromised_websites", "cloud_services"],
                aliases=["Cozy Bear", "The Dukes"]
            )
        }
        return profiles
    
    def register_profile(self, profile: AdversaryProfile) -> None:
        """Register a new adversary profile."""
        self.profiles[profile.name.lower()] = profile
        logger.info(f"Registered adversary profile: {profile.name}")
    
    def get_profile(self, adversary_name: str) -> Optional[AdversaryProfile]:
        """Get adversary profile by name."""
        # Check built-in profiles first
        if adversary_name.lower() in self.builtin_profiles:
            return self.builtin_profiles[adversary_name.lower()]
        
        # Check custom profiles
        return self.profiles.get(adversary_name.lower())
    
    def list_profiles(self) -> List[str]:
        """List all available profiles."""
        profiles = list(self.builtin_profiles.keys())
        profiles.extend(self.profiles.keys())
        return profiles


class ProfileBuilder:
    """Build custom adversary profiles."""
    
    def build_profile(
        self,
        name: str,
        description: str,
        ttps: List[str] = None,
        tools: List[str] = None,
        infrastructure: List[str] = None,
        **kwargs
    ) -> AdversaryProfile:
        """Build custom adversary profile."""
        if ttps is None:
            ttps = []
        if tools is None:
            tools = []
        if infrastructure is None:
            infrastructure = []
        
        # Convert technique IDs to Technique objects
        technique_library = TechniqueLibrary()
        techniques = []
        for ttp_id in ttps:
            technique = technique_library.get_technique_by_id(ttp_id)
            if technique:
                techniques.append(technique)
        
        profile = AdversaryProfile(
            name=name,
            description=description,
            ttps=techniques,
            tools=tools,
            infrastructure=infrastructure,
            **kwargs
        )
        
        return profile


class CampaignPlanner:
    """Plan adversary emulation campaigns."""
    
    def create_campaign(
        self,
        adversary: str,
        objectives: List[str] = None,
        duration_days: int = 14,
        team_size: int = 3,
        **kwargs
    ) -> EmulationCampaign:
        """Create emulation campaign."""
        if objectives is None:
            objectives = []
        
        campaign_id = hashlib.md5(f"{adversary}_{datetime.now()}".encode()).hexdigest()[:8]
        
        campaign = EmulationCampaign(
            campaign_id=campaign_id,
            adversary=AdversaryGroup(adversary) if adversary in [a.value for a in AdversaryGroup] else AdversaryGroup.CUSTOM,
            objectives=objectives,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(days=duration_days),
            team_size=team_size,
            **kwargs
        )
        
        logger.info(f"Created campaign: {campaign_id} for {adversary}")
        return campaign


async def main():
    """Main demonstration function."""
    print("=" * 60)
    print("Adversary Emulation Framework Demonstration")
    print("=" * 60)
    
    # Demo 1: Adversary Emulation
    print("\n" + "=" * 60)
    print("Demo 1: Adversary Emulation Campaign")
    print("=" * 60)
    
    # Create campaign planner
    campaign_planner = CampaignPlanner()
    
    # Create campaign
    campaign = campaign_planner.create_campaign(
        adversary="apt29",
        objectives=["credential_access", "lateral_movement", "data_exfiltration"],
        duration_days=14,
        team_size=3
    )
    
    print(f"Campaign ID: {campaign.campaign_id}")
    print(f"Adversary: {campaign.adversary.value}")
    print(f"Duration: {campaign.duration_days} days")
    print(f"Objectives: {campaign.objectives}")
    
    # Initialize emulator
    emulator = AdversaryEmulator(
        threat_actor=campaign.adversary,
        mitre_attack_mapping=True,
        fidelity_level="high"
    )
    
    # Configure emulator
    emulator.configure(campaign)
    
    # Get techniques for emulation
    technique_library = TechniqueLibrary()
    techniques = technique_library.get_techniques(
        adversary="apt29",
        categories=["initial_access", "execution", "persistence"]
    )
    
    print(f"\nLoaded {len(techniques)} techniques for emulation")
    
    # Implement techniques
    for technique in techniques:
        emulator.execute_technique(technique)
        print(f"  Implemented: {technique.technique_id} - {technique.technique_name}")
    
    # Execute emulation
    print("\nExecuting adversary emulation...")
    result = emulator.execute()
    
    # Display results
    print(f"\nEmulation Results:")
    print(f"  Techniques executed: {result.techniques_executed}")
    print(f"  Techniques detected: {result.techniques_detected}")
    print(f"  Detection rate: {result.detection_rate:.1f}%")
    print(f"  Mean time to detection: {result.mean_time_to_detection:.1f} minutes")
    print(f"  Mean time to response: {result.mean_time_to_response:.1f} minutes")
    print(f"  Objectives achieved: {result.objectives_achieved}/{result.total_objectives}")
    
    # Demo 2: Detection Validation
    print("\n" + "=" * 60)
    print("Demo 2: Detection Validation")
    print("=" * 60)
    
    # Initialize detection validator
    validator = DetectionValidator(
        adversary=campaign.adversary,
        validation_scope=["network_detection", "host_detection"]
    )
    
    # Execute validation
    alerts = validator.validate()
    print(f"Generated {len(alerts)} detection alerts")
    
    # Analyze alerts
    alert_analyzer = AlertAnalyzer()
    analysis = alert_analyzer.analyze_alerts(
        time_range="campaign_duration",
        alert_sources=["siem", "edr", "network_ids"]
    )
    
    print(f"\nAlert Analysis:")
    print(f"  Total alerts: {analysis['total_alerts']}")
    print(f"  True positives: {analysis['true_positives']}")
    print(f"  False positives: {analysis['false_positives']}")
    print(f"  Detection coverage: {analysis['coverage_percentage']:.1f}%")
    
    # Get validation summary
    validation_summary = validator.get_validation_summary()
    print(f"\nValidation Summary:")
    print(f"  Detection coverage: {validation_summary['detection_coverage']:.1f}%")
    print(f"  Mean confidence: {validation_summary['mean_confidence']:.2f}")
    
    # Demo 3: Adversary Profile Management
    print("\n" + "=" * 60)
    print("Demo 3: Adversary Profile Management")
    print("=" * 60)
    
    # Initialize profile manager
    profile_manager = AdversaryProfileManager()
    
    # List available profiles
    profiles = profile_manager.list_profiles()
    print(f"Available profiles: {profiles}")
    
    # Get specific profile
    apt29_profile = profile_manager.get_profile("apt29")
    if apt29_profile:
        print(f"\nAPT29 Profile:")
        print(f"  Name: {apt29_profile.name}")
        print(f"  Description: {apt29_profile.description}")
        print(f"  Origin: {apt29_profile.origin_country}")
        print(f"  Motivation: {apt29_profile.motivation}")
        print(f"  Target sectors: {apt29_profile.target_sectors}")
    
    # Build custom profile
    profile_builder = ProfileBuilder()
    custom_profile = profile_builder.build_profile(
        name="Custom APT Group",
        description="Custom adversary for organization-specific testing",
        ttps=["T1566", "T1059", "T1078"],
        tools=["custom_malware", "c2_framework"],
        infrastructure=["bulletproof_hosting", "domain_fronting"]
    )
    
    # Register custom profile
    profile_manager.register_profile(custom_profile)
    print(f"\nCustom profile registered: {custom_profile.name}")
    
    # Demo 4: TTP Implementation
    print("\n" + "=" * 60)
    print("Demo 4: TTP Implementation")
    print("=" * 60)
    
    # Initialize TTP implementer
    implementer = TTPImplementer()
    
    # Implement techniques
    for technique in techniques[:3]:  # Implement first 3 techniques
        implementation = implementer.implement_technique(technique)
        print(f"Implemented: {technique.technique_id} - {technique.technique_name}")
        
        # Test implementation
        test_result = implementation.test()
        print(f"  Test result: {'Success' if test_result['success'] else 'Failed'}")
        print(f"  Detected: {'Yes' if test_result['detected'] else 'No'}")
    
    # Get execution summary
    execution_summary = implementer.get_execution_summary()
    print(f"\nImplementation Summary:")
    print(f"  Total implementations: {execution_summary['total_implementations']}")
    print(f"  Success rate: {execution_summary['success_rate']:.1f}%")
    print(f"  Detection rate: {execution_summary['detection_rate']:.1f}%")
    
    print("\n" + "=" * 60)
    print("Demonstration completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())