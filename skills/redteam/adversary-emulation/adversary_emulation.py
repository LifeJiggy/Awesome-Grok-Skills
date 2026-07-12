"""
Adversary Emulation Framework Module

Provides structured methodology and tooling for mapping, implementing,
and testing against specific threat actor tactics, techniques, and
procedures (TTPs). Bridges threat intelligence and offensive operations.

This module is for authorized security testing and threat-informed defense validation only.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EmulationStatus(Enum):
    """Status of an adversary emulation."""
    PLANNING = auto()
    INFRASTRUCTURE = auto()
    EXECUTING = auto()
    VALIDATING = auto()
    COMPLETED = auto()


class TTPStatus(Enum):
    """Status of a TTP execution."""
    PENDING = auto()
    EXECUTING = auto()
    SUCCESS = auto()
    FAILED = auto()
    DETECTED = auto()
    SKIPPED = auto()


class Motivation(Enum):
    """Threat actor motivations."""
    ESPIONAGE = "espionage"
    FINANCIAL = "financial"
    SABOTAGE = "sabotage"
    HACKTIVISM = "hacktivism"
    CYBERCRIME = "cybercrime"
    STATE_SPONSORED = "state-sponsored"


class Sophistication(Enum):
    """Threat actor sophistication levels."""
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    INNOVATOR = "innovator"
    STRATEGIC = "strategic"


class TacticCategory(Enum):
    """MITRE ATT&CK tactic categories."""
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


class DetectionCoverage(Enum):
    """Detection coverage levels."""
    NONE = "none"
    PARTIAL = "partial"
    MODERATE = "moderate"
    GOOD = "good"
    EXCELLENT = "excellent"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class TTP:
    """MITRE ATT&CK technique, tactic, and procedure."""
    technique_id: str
    name: str
    description: str = ""
    tactic: TacticCategory = TacticCategory.EXECUTION
    tools: list[str] = field(default_factory=list)
    detection: str = ""
    sub_techniques: list[str] = field(default_factory=list)
    data_sources: list[str] = field(default_factory=list)

    @property
    def base_technique(self) -> str:
        """Get base technique ID without sub-technique."""
        return self.technique_id.split(".")[0]


@dataclass
class ThreatActor:
    """Known threat actor definition."""
    name: str
    aliases: list[str] = field(default_factory=list)
    motivation: Motivation = Motivation.ESPIONAGE
    sophistication: Sophistication = Sophistication.ADVANCED
    country: str = ""
    associated_groups: list[str] = field(default_factory=list)
    targeted_sectors: list[str] = field(default_factory=list)
    active_since: str = ""
    tools: list[str] = field(default_factory=list)
    infrastructure: list[str] = field(default_factory=list)


@dataclass
class AdversaryProfile:
    """Complete adversary profile for emulation."""
    threat_actor: ThreatActor
    ttps: list[TTP] = field(default_factory=list)
    emulation_scope: str = "external_network"
    target_environment: str = "enterprise_windows"
    skill_level_required: str = "advanced"
    estimated_duration_weeks: int = 8
    team_size: int = 3

    def get_ttps_by_tactic(self) -> dict[TacticCategory, list[TTP]]:
        """Group TTPs by tactic."""
        result: dict[TacticCategory, list[TTP]] = {}
        for ttp in self.ttps:
            if ttp.tactic not in result:
                result[ttp.tactic] = []
            result[ttp.tactic].append(ttp)
        return result

    def get_tactic_coverage(self) -> dict[str, int]:
        """Get count of TTPs per tactic."""
        coverage: dict[str, int] = {}
        for ttp in self.ttps:
            key = ttp.tactic.value
            coverage[key] = coverage.get(key, 0) + 1
        return coverage


@dataclass
class TechniqueExecution:
    """Result of executing a single technique."""
    technique_id: str
    technique_name: str
    success: bool
    detected: bool = False
    detection_time_seconds: Optional[int] = None
    implementation: dict[str, Any] = field(default_factory=dict)
    evidence_path: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    execution_id: str = field(default_factory=lambda: f"EXEC-{uuid.uuid4().hex[:6].upper()}")


@dataclass
class DetectionTest:
    """Test for validating detection capabilities."""
    technique: str
    name: str
    expected_detection: str = ""
    test_method: str = ""
    validation_criteria: list[str] = field(default_factory=list)
    result: Optional[TechniqueExecution] = None
    detected: bool = False


@dataclass
class DetectionGap:
    """Identified detection gap."""
    technique: str
    coverage_level: DetectionCoverage = DetectionCoverage.NONE
    description: str = ""
    remediation: str = ""
    priority: str = "high"


@dataclass
class TTPCoverageStats:
    """TTP coverage statistics."""
    total_ttps: int = 0
    executed_ttps: int = 0
    successful_ttps: int = 0
    detected_ttps: int = 0

    @property
    def execution_rate(self) -> float:
        return (self.executed_ttps / max(self.total_ttps, 1)) * 100

    @property
    def detection_rate(self) -> float:
        return (self.detected_ttps / max(self.executed_ttps, 1)) * 100


@dataclass
class TacticStats:
    """Statistics for a single tactic."""
    total: int = 0
    executed: int = 0
    detected: int = 0


# ---------------------------------------------------------------------------
# Core Engine Classes
# ---------------------------------------------------------------------------

class AdversaryEmulationEngine:
    """Main engine for adversary emulation operations."""

    def __init__(self, profile: AdversaryProfile):
        self.profile = profile
        self.status: EmulationStatus = EmulationStatus.PLANNING
        self.execution_results: list[TechniqueExecution] = []
        self.detection_tests: list[DetectionTest] = []
        self.detection_gaps: list[DetectionGap] = []

    def configure(self, detection_validation: bool = True,
                  opsec_level: str = "high",
                  auto_adapt: bool = True) -> None:
        """Configure the emulation engine."""
        self._config = {
            "detection_validation": detection_validation,
            "opsec_level": opsec_level,
            "auto_adapt": auto_adapt,
        }
        self.status = EmulationStatus.PLANNING

    def validate_profile(self) -> dict[str, Any]:
        """Validate the adversary profile."""
        return {
            "threat_actor": self.profile.threat_actor.name,
            "total_ttps": len(self.profile.ttps),
            "tactic_coverage": self.profile.get_tactic_coverage(),
            "scope": self.profile.emulation_scope,
            "environment": self.profile.target_environment,
            "estimated_duration_weeks": self.profile.estimated_duration_weeks,
        }

    def execute_technique(self, technique_id: str,
                          implementation: dict[str, Any] | None = None,
                          opsec: bool = True,
                          validate_detection: bool = True) -> TechniqueExecution:
        """Execute a single technique."""
        ttp = next(
            (t for t in self.profile.ttps if t.technique_id == technique_id),
            None,
        )
        if not ttp:
            return TechniqueExecution(
                technique_id=technique_id,
                technique_name="Unknown",
                success=False,
                error=f"Technique {technique_id} not in profile",
            )

        import random
        success = random.random() > 0.25
        detected = random.random() > 0.7 if validate_detection else False

        result = TechniqueExecution(
            technique_id=technique_id,
            technique_name=ttp.name,
            success=success,
            detected=detected,
            detection_time_seconds=random.randint(10, 86400) if detected else None,
            implementation=implementation or {},
        )
        self.execution_results.append(result)
        return result

    def get_coverage_stats(self) -> TTPCoverageStats:
        """Get TTP coverage statistics."""
        stats = TTPCoverageStats(total_ttps=len(self.profile.ttps))
        for result in self.execution_results:
            stats.executed_ttps += 1
            if result.success:
                stats.successful_ttps += 1
            if result.detected:
                stats.detected_ttps += 1
        return stats

    def get_tactic_breakdown(self) -> dict[str, TacticStats]:
        """Get breakdown by tactic."""
        breakdown: dict[str, TacticStats] = {}
        for ttp in self.profile.ttps:
            tactic = ttp.tactic.value
            if tactic not in breakdown:
                breakdown[tactic] = TacticStats()
            breakdown[tactic].total += 1

        for result in self.execution_results:
            ttp = next(
                (t for t in self.profile.ttps if t.technique_id == result.technique_id),
                None,
            )
            if ttp:
                tactic = ttp.tactic.value
                if tactic in breakdown:
                    breakdown[tactic].executed += 1
                    if result.detected:
                        breakdown[tactic].detected += 1
        return breakdown

    def get_status(self) -> dict[str, Any]:
        """Get current emulation status."""
        stats = self.get_coverage_stats()
        return {
            "profile": self.profile.threat_actor.name,
            "status": self.status.name,
            "total_ttps": stats.total_ttps,
            "executed": stats.executed_ttps,
            "successful": stats.successful_ttps,
            "detected": stats.detected_ttps,
            "detection_rate": f"{stats.detection_rate:.1f}%",
        }


class TTPChainExecutor:
    """Executes a chain of TTPs in sequence."""

    def __init__(self, engine: AdversaryEmulationEngine):
        self.engine = engine
        self.chain: list[dict[str, Any]] = []

    def define_chain(self, techniques: list[dict[str, Any]]) -> None:
        """Define the TTP execution chain."""
        self.chain = techniques

    def execute_chain(self, auto_adapt: bool = True,
                      max_retries: int = 3) -> list[TechniqueExecution]:
        """Execute the full TTP chain."""
        results = []
        for step in self.chain:
            technique_id = step.get("id", "")
            result = self.engine.execute_technique(
                technique_id=technique_id,
                implementation=step.get("implementation", {}),
                opsec=step.get("opsec", True),
                validate_detection=step.get("validate_detection", True),
            )
            results.append(result)
            if not result.success and not auto_adapt:
                break
        return results


class DetectionValidator:
    """Validates detection capabilities against TTPs."""

    def __init__(self, engine: AdversaryEmulationEngine):
        self.engine = engine
        self.tests: list[DetectionTest] = []

    def add_test(self, technique: str, name: str,
                 test_method: str = "",
                 validation_criteria: list[str] | None = None) -> DetectionTest:
        """Add a detection test."""
        test = DetectionTest(
            technique=technique,
            name=name,
            test_method=test_method,
            validation_criteria=validation_criteria or [],
        )
        self.tests.append(test)
        return test

    def run_tests(self) -> list[DetectionTest]:
        """Run all detection tests."""
        for test in self.tests:
            result = self.engine.execute_technique(
                technique_id=test.technique,
                validate_detection=True,
            )
            test.result = result
            test.detected = result.detected
        return self.tests

    def analyze_gaps(self) -> list[DetectionGap]:
        """Analyze detection gaps from test results."""
        gaps = []
        for test in self.tests:
            if not test.detected:
                gap = DetectionGap(
                    technique=test.technique,
                    coverage_level=DetectionCoverage.NONE,
                    description=f"Detection failed for {test.name}",
                    remediation=f"Implement detection for {test.technique}",
                    priority="high",
                )
                gaps.append(gap)
                self.engine.detection_gaps.append(gap)
        return gaps


class EmulationReport:
    """Generates adversary emulation reports."""

    def __init__(self, engine: AdversaryEmulationEngine):
        self.engine = engine

    def generate_executive_summary(self) -> str:
        """Generate executive summary."""
        stats = self.engine.get_coverage_stats()
        return (
            f"Adversary emulation of {self.engine.profile.threat_actor.name} "
            f"executed {stats.executed_ttps}/{stats.total_ttps} techniques "
            f"with {stats.detection_rate:.1f}% detection rate."
        )

    def generate_ttp_matrix(self) -> dict[str, list[dict[str, str]]]:
        """Generate MITRE ATT&CK TTP matrix."""
        matrix: dict[str, list[dict[str, str]]] = {}
        for ttp in self.engine.profile.ttps:
            tactic = ttp.tactic.value
            if tactic not in matrix:
                matrix[tactic] = []
            result = next(
                (r for r in self.engine.execution_results if r.technique_id == ttp.technique_id),
                None,
            )
            matrix[tactic].append({
                "technique": ttp.technique_id,
                "name": ttp.name,
                "executed": "yes" if result else "no",
                "detected": "yes" if result and result.detected else "no",
            })
        return matrix

    def generate_detection_analysis(self) -> dict[str, Any]:
        """Generate detection analysis."""
        stats = self.engine.get_coverage_stats()
        gaps = self.engine.detection_gaps
        return {
            "total_techniques": stats.total_ttps,
            "executed": stats.executed_ttps,
            "detected": stats.detected_ttps,
            "detection_rate": f"{stats.detection_rate:.1f}%",
            "gaps_count": len(gaps),
            "gap_techniques": [g.technique for g in gaps],
        }

    def generate_full_report(self) -> str:
        """Generate complete emulation report."""
        lines = [
            "# Adversary Emulation Report",
            f"## Threat Actor: {self.engine.profile.threat_actor.name}",
            f"**Motivation:** {self.engine.profile.threat_actor.motivation.value}",
            f"**Sophistication:** {self.engine.profile.threat_actor.sophistication.value}",
            f"**Country:** {self.engine.profile.threat_actor.country}",
            "",
            "## Executive Summary",
            self.generate_executive_summary(),
            "",
        ]

        # TTP matrix
        matrix = self.generate_ttp_matrix()
        lines.extend(["## MITRE ATT&CK Matrix", ""])
        for tactic, techniques in matrix.items():
            lines.append(f"### {tactic}")
            for t in techniques:
                status = "✓" if t["executed"] == "yes" else "✗"
                detected = " [DETECTED]" if t["detected"] == "yes" else ""
                lines.append(f"- {status} {t['technique']}: {t['name']}{detected}")
            lines.append("")

        # Detection analysis
        analysis = self.generate_detection_analysis()
        lines.extend([
            "## Detection Analysis",
            f"- Detection Rate: {analysis['detection_rate']}",
            f"- Gaps: {analysis['gaps_count']}",
            "",
        ])

        if self.engine.detection_gaps:
            lines.extend(["## Detection Gaps", ""])
            for gap in self.engine.detection_gaps:
                lines.extend([
                    f"### {gap.technique}",
                    f"- Coverage: {gap.coverage_level.value}",
                    f"- Description: {gap.description}",
                    f"- Remediation: {gap.remediation}",
                    "",
                ])

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Pre-built adversary profiles
# ---------------------------------------------------------------------------

def create_apt29_profile() -> AdversaryProfile:
    """Create a pre-built APT29 (Cozy Bear) emulation profile."""
    actor = ThreatActor(
        name="APT29 (Cozy Bear)",
        aliases=["The Dukes", "CozyDuke", "NOBELIUM"],
        motivation=Motivation.ESPIONAGE,
        sophistication=Sophistication.EXPERT,
        country="Russia",
        targeted_sectors=["government", "technology", "healthcare"],
        active_since="2008",
        tools=["wellmess", "wellmail", "crutch", "lazagne", "certutil"],
    )
    ttps = [
        TTP("T1566.001", "Spearphishing Attachment", tactic=TacticCategory.INITIAL_ACCESS,
            tools=["macro_documents"], detection="email_gateway"),
        TTP("T1059.001", "PowerShell", tactic=TacticCategory.EXECUTION,
            tools=["powershell_encoded"], detection="script_block_logging"),
        TTP("T1053.005", "Scheduled Task", tactic=TacticCategory.PERSISTENCE,
            tools=["schtasks"], detection="task_creation_events"),
        TTP("T1003.002", "Security Account Manager", tactic=TacticCategory.CREDENTIAL_ACCESS,
            tools=["reg_save", "secretsdump"], detection="reg_access_monitoring"),
        TTP("T1021.002", "SMB/Windows Admin Shares", tactic=TacticCategory.LATERAL_MOVEMENT,
            tools=["psexec", "wmiexec"], detection="network_logon_events"),
        TTP("T1041", "Exfiltration Over C2", tactic=TacticCategory.EXFILTRATION,
            tools=["https_c2"], detection="network_traffic_analysis"),
    ]
    return AdversaryProfile(threat_actor=actor, ttps=ttps)


def create_lazarus_profile() -> AdversaryProfile:
    """Create a pre-built Lazarus Group emulation profile."""
    actor = ThreatActor(
        name="Lazarus Group",
        aliases=["HIDDEN COBRA", "Zinc", "Labyrinth Chollima"],
        motivation=Motivation.FINANCIAL,
        sophistication=Sophistication.EXPERT,
        country="North Korea",
        targeted_sectors=["finance", "cryptocurrency", "technology"],
        tools=["applejeus", "fallchill", "electricfish"],
    )
    ttps = [
        TTP("T1566.001", "Spearphishing Attachment", tactic=TacticCategory.INITIAL_ACCESS,
            tools=["macro_documents"], detection="email_gateway"),
        TTP("T1204.002", "User Execution: Malicious File", tactic=TacticCategory.EXECUTION,
            tools=["lnk_files"], detection="file_execution_monitoring"),
        TTP("T1059.001", "PowerShell", tactic=TacticCategory.EXECUTION,
            tools=["powershell_encoded"], detection="script_block_logging"),
        TTP("T1547.001", "Registry Run Keys", tactic=TacticCategory.PERSISTENCE,
            tools=["reg_add"], detection="registry_modification"),
        TTP("T1003.001", "LSASS Memory", tactic=TacticCategory.CREDENTIAL_ACCESS,
            tools=["mimikatz", "procdump"], detection="lsass_access_monitoring"),
        TTP("T1048", "Exfiltration Over Alternative Protocol", tactic=TacticCategory.EXFILTRATION,
            tools=["dns_tunneling"], detection="dns_query_monitoring"),
    ]
    return AdversaryProfile(threat_actor=actor, ttps=ttps)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def map_technique_to_tactic(technique_id: str) -> TacticCategory:
    """Map a technique ID to its tactic category."""
    mapping = {
        "T1566": TacticCategory.INITIAL_ACCESS,
        "T1204": TacticCategory.EXECUTION,
        "T1059": TacticCategory.EXECUTION,
        "T1053": TacticCategory.PERSISTENCE,
        "T1547": TacticCategory.PERSISTENCE,
        "T1003": TacticCategory.CREDENTIAL_ACCESS,
        "T1021": TacticCategory.LATERAL_MOVEMENT,
        "T1041": TacticCategory.EXFILTRATION,
        "T1048": TacticCategory.EXFILTRATION,
        "T1572": TacticCategory.COMMAND_AND_CONTROL,
    }
    prefix = technique_id.split(".")[0]
    return mapping.get(prefix, TacticCategory.EXECUTION)


def calculate_detection_score(results: list[TechniqueExecution]) -> float:
    """Calculate overall detection score from results."""
    if not results:
        return 0.0
    detected = sum(1 for r in results if r.detected)
    return (detected / len(results)) * 100


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the adversary emulation framework."""
    print("=" * 60)
    print("  Adversary Emulation Framework - Demo")
    print("=" * 60)

    # Create APT29 profile
    profile = create_apt29_profile()
    print(f"\nProfile: {profile.threat_actor.name}")
    print(f"Motivation: {profile.threat_actor.motivation.value}")
    print(f"Sophistication: {profile.threat_actor.sophistication.value}")
    print(f"Total TTPs: {len(profile.ttps)}")
    print(f"Tactic coverage: {profile.get_tactic_coverage()}")

    # Initialize engine
    engine = AdversaryEmulationEngine(profile)
    engine.configure(detection_validation=True, opsec_level="high")

    # Validate profile
    validation = engine.validate_profile()
    print(f"\nValidation: {json.dumps(validation, indent=2)}")

    # Execute techniques
    print("\nExecuting techniques...")
    for ttp in profile.ttps:
        result = engine.execute_technique(
            technique_id=ttp.technique_id,
            implementation={"method": "automated"},
            validate_detection=True,
        )
        status = "SUCCESS" if result.success else "FAILED"
        detected = "DETECTED" if result.detected else "UNDETECTED"
        print(f"  {ttp.technique_id} ({ttp.name}): {status} - {detected}")

    # Coverage stats
    stats = engine.get_coverage_stats()
    print(f"\nCoverage: {stats.executed_ttps}/{stats.total_ttps} executed")
    print(f"Detection rate: {stats.detection_rate:.1f}%")

    # Tactic breakdown
    breakdown = engine.get_tactic_breakdown()
    print("\nTactic breakdown:")
    for tactic, stats in breakdown.items():
        print(f"  {tactic}: {stats.executed}/{stats.total} executed, {stats.detected} detected")

    # Detection validation
    validator = DetectionValidator(engine)
    validator.add_test("T1003.001", "LSASS Dump Detection",
                       test_method="mimikatz", validation_criteria=["alert_generated"])
    validator.add_test("T1053.005", "Scheduled Task Detection",
                       test_method="schtasks", validation_criteria=["task_logged"])
    test_results = validator.run_tests()
    gaps = validator.analyze_gaps()
    print(f"\nDetection tests: {len(test_results)}")
    print(f"Detected: {sum(1 for t in test_results if t.detected)}")
    print(f"Gaps: {len(gaps)}")

    # Generate report
    report = EmulationReport(engine)
    print(f"\n{report.generate_executive_summary()}")

    ttp_matrix = report.generate_ttp_matrix()
    print(f"\nTTP Matrix tactics: {list(ttp_matrix.keys())}")

    detection_analysis = report.generate_detection_analysis()
    print(f"\nDetection analysis: {json.dumps(detection_analysis, indent=2)}")

    # Full report
    full_report = report.generate_full_report()
    print(f"\n{'='*40}")
    print("Full report preview (first 30 lines):")
    print("=" * 40)
    for line in full_report.split("\n")[:30]:
        print(line)

    # Status
    status = engine.get_status()
    print(f"\nEngine status: {json.dumps(status, indent=2)}")

    # Demo Lazarus profile
    lazarus = create_lazarus_profile()
    print(f"\nLazarus profile: {lazarus.threat_actor.name}")
    print(f"  TTPs: {len(lazarus.ttps)}")
    print(f"  Sectors: {lazarus.threat_actor.targeted_sectors}")


if __name__ == "__main__":
    main()
