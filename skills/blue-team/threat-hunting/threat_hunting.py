"""
Threat Hunting Module
Hypothesis-driven hunting, MITRE ATT&CK mapping, IOB development, and hunt query library.
"""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class HuntPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Tactic(Enum):
    RECONNAISSANCE = "TA0043"
    RESOURCE_DEV = "TA0042"
    INITIAL_ACCESS = "TA0001"
    EXECUTION = "TA0002"
    PERSISTENCE = "TA0003"
    PRIV_ESCALATION = "TA0004"
    DEFENSE_EVASION = "TA0005"
    CREDENTIAL_ACCESS = "TA0006"
    DISCOVERY = "TA0007"
    LATERAL_MOVEMENT = "TA0008"
    COLLECTION = "TA0009"
    EXFILTRATION = "TA0010"
    COMMAND_CONTROL = "TA0011"
    IMPACT = "TA0040"


class IOBCategory(Enum):
    NETWORK = "network_behavior"
    PROCESS = "process_behavior"
    FILE = "file_system_behavior"
    REGISTRY = "registry_behavior"
    AUTH = "authentication_behavior"
    CLOUD = "cloud_behavior"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class HuntHypothesis:
    """Threat hunt hypothesis."""
    hypothesis_id: str
    description: str
    threat_actor: str
    technique_id: str
    technique_name: str
    rationale: str
    data_sources: List[str] = field(default_factory=list)
    priority: HuntPriority = HuntPriority.MEDIUM
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "proposed"
    mitre_tactic: str = ""

    @property
    def age_days(self) -> float:
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() / 86400


@dataclass
class HuntQuery:
    """Hunt query for a specific platform."""
    technique_id: str
    platform: str
    query_type: str
    query: str
    description: str = ""
    data_source: str = ""


@dataclass
class IOBIndicator:
    """Indicator of Behavior."""
    indicator_id: str
    behavior_category: IOBCategory
    description: str
    technique_id: str
    confidence: float = 0.5
    data_source: str = ""
    query: str = ""


@dataclass
class HuntOperation:
    """Hunt operation."""
    hunt_id: str
    name: str
    hypothesis: HuntHypothesis
    scope: List[str] = field(default_factory=list)
    start_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    duration_days: int = 7
    status: str = "planning"
    findings: List[str] = field(default_factory=list)
    queries_executed: int = 0
    data_volume_gb: float = 0.0


@dataclass
class CoverageAnalysis:
    """ATT&CK coverage analysis."""
    total_techniques: int = 0
    covered_techniques: int = 0
    coverage_pct: float = 0.0
    gaps: List[str] = field(default_factory=list)
    covered: List[str] = field(default_factory=list)


@dataclass
class HuntReport:
    """Hunt operation report."""
    hunt_id: str
    sections: List[Dict[str, str]] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    true_positives: int = 0
    false_positives: int = 0
    recommendations: List[str] = field(default_factory=list)
    new_detections: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# MITRE ATT&CK Database
# ---------------------------------------------------------------------------

MITRE_TECHNIQUES = {
    "T1059.001": {"name": "PowerShell", "tactic": "execution", "platforms": ["Windows"]},
    "T1059.003": {"name": "Windows Command Shell", "tactic": "execution", "platforms": ["Windows"]},
    "T1053.005": {"name": "Scheduled Task", "tactic": "persistence", "platforms": ["Windows"]},
    "T1021.002": {"name": "SMB/Windows Admin Shares", "tactic": "lateral_movement", "platforms": ["Windows"]},
    "T1547.001": {"name": "Registry Run Keys", "tactic": "persistence", "platforms": ["Windows"]},
    "T1003.001": {"name": "LSASS Memory", "tactic": "credential_access", "platforms": ["Windows"]},
    "T1071.001": {"name": "Web Protocols", "tactic": "command_control", "platforms": ["Linux", "Windows"]},
    "T1048": {"name": "Exfiltration Over Alternative Protocol", "tactic": "exfiltration", "platforms": ["Linux", "Windows"]},
    "T1078": {"name": "Valid Accounts", "tactic": "persistence", "platforms": ["Linux", "Windows"]},
    "T1486": {"name": "Data Encrypted for Impact", "tactic": "impact", "platforms": ["Linux", "Windows"]},
}

KNOWN_ACTORS = {
    "APT29": {
        "aliases": ["Cozy Bear", "The Dukes"],
        "techniques": ["T1059.001", "T1053.005", "T1071.001", "T1078"],
        "ttps": ["Supply chain compromise", "Steganography", "Password spraying"],
    },
    "APT28": {
        "aliases": ["Fancy Bear", "Sofacy"],
        "techniques": ["T1059.001", "T1053.005", "T1021.002", "T1003.001"],
        "ttps": ["Credential harvesting", "Spear phishing", "Zero-day exploitation"],
    },
    "Lazarus Group": {
        "aliases": ["HIDDEN COBRA"],
        "techniques": ["T1059.001", "T1547.001", "T1071.001", "T1486"],
        "ttps": ["Supply chain attacks", "Ransomware", "Cryptocurrency theft"],
    },
}


# ---------------------------------------------------------------------------
# Hypothesis Engine
# ---------------------------------------------------------------------------

class HypothesisEngine:
    """Develop and manage hunt hypotheses."""

    def create_hypothesis(
        self,
        threat_actor: str,
        technique: str,
        rationale: str,
        data_sources: Optional[List[str]] = None,
        priority: str = "medium",
    ) -> HuntHypothesis:
        tech_id = technique.split(" - ")[0] if " - " in technique else technique
        tech_info = MITRE_TECHNIQUES.get(tech_id, {"name": technique, "tactic": "unknown"})
        return HuntHypothesis(
            hypothesis_id=f"HYP-{secrets.token_hex(4).upper()}",
            description=f"Hunt for {threat_actor} using {tech_info.get('name', technique)}",
            threat_actor=threat_actor,
            technique_id=tech_id,
            technique_name=tech_info.get("name", technique),
            rationale=rationale,
            data_sources=data_sources or [],
            priority=HuntPriority(priority),
            mitre_tactic=tech_info.get("tactic", ""),
        )

    def from_threat_intel(self, report: str) -> List[HuntHypothesis]:
        hypotheses: List[HuntHypothesis] = []
        for actor, info in KNOWN_ACTORS.items():
            if actor.lower() in report.lower():
                for tech_id in info["techniques"][:2]:
                    tech = MITRE_TECHNIQUES.get(tech_id, {"name": tech_id, "tactic": "unknown"})
                    hypotheses.append(self.create_hypothesis(
                        threat_actor=actor,
                        technique=tech_id,
                        rationale=f"CTI report mentions {actor} activity",
                        data_sources=["process_creation", "network_connection"],
                    ))
        return hypotheses


# ---------------------------------------------------------------------------
# MITRE Mapper
# ---------------------------------------------------------------------------

class MITREMapper:
    """Map detections to MITRE ATT&CK and analyze coverage."""

    def analyze_coverage(
        self,
        existing_rules: List[str],
        target_techniques: Optional[List[str]] = None,
    ) -> CoverageAnalysis:
        target = target_techniques or list(MITRE_TECHNIQUES.keys())
        covered = [t for t in target if t in existing_rules or t in [r.split(".")[0] for r in existing_rules]]
        gaps = [t for t in target if t not in covered]
        return CoverageAnalysis(
            total_techniques=len(target),
            covered_techniques=len(covered),
            coverage_pct=len(covered) / max(len(target), 1) * 100,
            gaps=gaps,
            covered=covered,
        )

    def get_techniques_for_tactic(self, tactic: str) -> List[Dict[str, str]]:
        return [
            {"id": tid, "name": info["name"]}
            for tid, info in MITRE_TECHNIQUES.items()
            if info["tactic"] == tactic
        ]

    def map_actor_techniques(self, actor: str) -> List[Dict[str, str]]:
        actor_info = KNOWN_ACTORS.get(actor, {})
        techniques = actor_info.get("techniques", [])
        return [
            {"id": tid, "name": MITRE_TECHNIQUES.get(tid, {}).get("name", tid)}
            for tid in techniques
        ]


# ---------------------------------------------------------------------------
# Hunt Query Library
# ---------------------------------------------------------------------------

class HuntQueryLibrary:
    """Library of hunt queries for MITRE techniques."""

    QUERIES: Dict[str, Dict[str, str]] = {
        "T1059.001": {
            "splunk_process": 'index=windows EventCode=4688 | search New_Process_Name="*powershell*" | stats count by Computer, New_Process_Name, Creator_Process_Name',
            "splunk_script": 'index=windows sourcetype="WinEventLog:Microsoft-Windows-PowerShell/Operational" | stats count by Computer, ScriptBlockText',
            "elastic": 'event.code:4688 and process.name:powershell.exe | stats count by host, process.name, process.parent.name',
        },
        "T1053.005": {
            "splunk_process": 'index=windows EventCode=4698 | stats count by Computer, TaskName',
            "elastic": 'event.code:4698 | stats count by host, winlog.event_data.TaskName',
        },
        "T1003.001": {
            "splunk_process": 'index=windows EventCode=10 | search TargetImage="*lsass*" | stats count by Computer, SourceImage',
            "elastic": 'event.code:10 and winlog.event_data.TargetImage:*lsass* | stats count by host, winlog.event_data.SourceImage',
        },
    }

    def get_query(
        self,
        technique: str,
        platform: str = "splunk",
        data_source: str = "process_creation",
    ) -> str:
        key = f"{platform}_{data_source}"
        queries = self.queries.get(technique, {})
        return queries.get(key, queries.get(f"{platform}_process", f"-- No query for {technique} on {platform} --"))

    def list_techniques(self) -> List[str]:
        return list(self.QUERIES.keys())


# ---------------------------------------------------------------------------
# IOB Builder
# ---------------------------------------------------------------------------

class IOBBuilder:
    """Build Indicators of Behavior from threat intelligence."""

    def build_from_actor(self, actor: str) -> List[IOBIndicator]:
        actor_info = KNOWN_ACTORS.get(actor, {})
        indicators: List[IOBIndicator] = []
        for tech_id in actor_info.get("techniques", []):
            tech = MITRE_TECHNIQUES.get(tech_id, {"name": tech_id, "tactic": "unknown"})
            category = self._tactic_to_category(tech.get("tactic", ""))
            indicators.append(IOBIndicator(
                indicator_id=f"IOB-{secrets.token_hex(4).upper()}",
                behavior_category=category,
                description=f"{actor} uses {tech.get('name', tech_id)} for {tech.get('tactic', 'unknown')}",
                technique_id=tech_id,
                confidence=0.7,
                data_source="process_creation",
            ))
        return indicators

    def _tactic_to_category(self, tactic: str) -> IOBCategory:
        mapping = {
            "execution": IOBCategory.PROCESS,
            "persistence": IOBCategory.REGISTRY,
            "credential_access": IOBCategory.PROCESS,
            "lateral_movement": IOBCategory.NETWORK,
            "command_control": IOBCategory.NETWORK,
            "exfiltration": IOBCategory.NETWORK,
        }
        return mapping.get(tactic, IOBCategory.PROCESS)


# ---------------------------------------------------------------------------
# Hunt Planner
# ---------------------------------------------------------------------------

class HuntPlanner:
    """Plan and manage hunt operations."""

    def __init__(self):
        self._hunts: Dict[str, HuntOperation] = {}

    def create_hunt(
        self,
        name: str,
        hypothesis: HuntHypothesis,
        scope: Optional[List[str]] = None,
        duration_days: int = 7,
    ) -> HuntOperation:
        hunt = HuntOperation(
            hunt_id=f"HUNT-{secrets.token_hex(4).upper()}",
            name=name,
            hypothesis=hypothesis,
            scope=scope or ["endpoints"],
            duration_days=duration_days,
            status="active",
        )
        self._hunts[hunt.hunt_id] = hunt
        return hunt

    def add_finding(self, hunt_id: str, finding: str) -> None:
        hunt = self._hunts.get(hunt_id)
        if hunt:
            hunt.findings.append(finding)

    def get_hunt(self, hunt_id: str) -> Optional[HuntOperation]:
        return self._hunts.get(hunt_id)

    def get_active_hunts(self) -> List[HuntOperation]:
        return [h for h in self._hunts.values() if h.status == "active"]


# ---------------------------------------------------------------------------
# Hunt Reporter
# ---------------------------------------------------------------------------

class HuntReporter:
    """Generate hunt operation reports."""

    def generate_report(
        self,
        hunt: HuntOperation,
        findings: Optional[List[str]] = None,
        true_positives: int = 0,
        false_positives: int = 0,
    ) -> HuntReport:
        report = HuntReport(
            hunt_id=hunt.hunt_id,
            findings=findings or hunt.findings,
            true_positives=true_positives,
            false_positives=false_positives,
        )
        report.sections = [
            {"title": "Executive Summary", "content": f"Hunt: {hunt.name}"},
            {"title": "Hypothesis", "content": hunt.hypothesis.description},
            {"title": "Methodology", "content": f"Scope: {', '.join(hunt.scope)}"},
            {"title": "Findings", "content": f"{len(report.findings)} findings"},
            {"title": "Detections", "content": f"TP: {true_positives}, FP: {false_positives}"},
        ]
        report.recommendations = [
            "Create automated detection for confirmed findings",
            "Update hunt hypothesis based on results",
            "Expand data collection if gaps identified",
        ]
        return report


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Threat Hunting Demo")
    print("=" * 60)

    engine = HypothesisEngine()
    hypothesis = engine.create_hypothesis(
        threat_actor="APT29",
        technique="T1059.001 - PowerShell",
        rationale="CTI indicates APT29 PowerShell usage",
        data_sources=["process_creation", "script_block_logging"],
    )
    print(f"\nHypothesis: {hypothesis.description}")
    print(f"Technique: {hypothesis.technique_id}")

    print("\n[1] MITRE Coverage")
    mapper = MITREMapper()
    coverage = mapper.analyze_coverage(
        existing_rules=["T1059.001", "T1053.005"],
        target_techniques=["T1059.001", "T1053.005", "T1021.002", "T1547.001", "T1003.001"],
    )
    print(f"  Coverage: {coverage.coverage_pct:.0f}%")
    print(f"  Gaps: {coverage.gaps}")

    print("\n[2] Hunt Queries")
    lib = HuntQueryLibrary()
    query = lib.get_query("T1059.001", "splunk", "process_creation")
    print(f"  Query: {query[:80]}...")

    print("\n[3] IOB Building")
    iob = IOBBuilder()
    indicators = iob.build_from_actor("APT29")
    for ind in indicators[:3]:
        print(f"  {ind.behavior_category.value}: {ind.description[:60]}")

    print("\n[4] Hunt Operations")
    planner = HuntPlanner()
    hunt = planner.create_hunt("APT29 PowerShell Hunt", hypothesis, ["endpoints", "network"])
    planner.add_finding(hunt.hunt_id, "Suspicious encoded PowerShell on WS-003")
    print(f"  Hunt: {hunt.hunt_id}")

    print("\n[5] Hunt Report")
    reporter = HuntReporter()
    report = reporter.generate_report(hunt, true_positives=1, false_positives=2)
    print(f"  Sections: {len(report.sections)}")
    print(f"  Findings: {report.findings}")

    print("\n" + "=" * 60)
    print("  Threat hunting demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
