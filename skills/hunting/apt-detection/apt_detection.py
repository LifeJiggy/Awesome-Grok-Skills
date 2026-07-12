"""
APT Detection Module
Advanced persistent threat detection, tracking, and attribution framework
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class KillChainPhase(Enum):
    RECONNAISSANCE = "reconnaissance"
    WEAPONIZATION = "weaponization"
    DELIVERY = "delivery"
    EXPLOITATION = "exploitation"
    INSTALLATION = "installation"
    COMMAND_AND_CONTROL = "command_and_control"
    ACTIONS_ON_OBJECTIVES = "actions_on_objectives"


class DetectionSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatActorType(Enum):
    STATE_SPONSORED = "state-sponsored"
    ORGANIZED_CRIME = "organized-crime"
    HACKTIVIST = "hacktivist"
    INSIDER = "insider"
    UNKNOWN = "unknown"


class PersistenceType(Enum):
    REGISTRY = "registry"
    SCHEDULED_TASK = "scheduled_task"
    WMI_SUBSCRIPTION = "wmi_subscription"
    SERVICE = "service"
    STARTUP_FOLDER = "startup_folder"
    DLL_HIJACKING = "dll_hijacking"
    BITS_JOB = "bits_job"
    COM_OBJECT = "com_object"


class LateralMovementTechnique(Enum):
    PS_EXEC = "psexec"
    WMI = "wmi"
    RDP = "rdp"
    SMB = "smb"
    WINRM = "winrm"
    SSH = "ssh"
    PASS_THE_HASH = "pass_the_hash"
    GOLDEN_TICKET = "golden_ticket"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class DetectionRule:
    """Rule for detecting APT activities."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    severity: DetectionSeverity = DetectionSeverity.MEDIUM
    mitre_id: str = ""
    kill_chain_phase: KillChainPhase = KillChainPhase.ACTIONS_ON_OBJECTIVES
    pattern: str = ""
    conditions: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    confidence_threshold: int = 70
    false_positive_exceptions: List[str] = field(default_factory=list)


@dataclass
class ThreatActorProfile:
    """Known threat actor profile."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    aliases: List[str] = field(default_factory=list)
    actor_type: ThreatActorType = ThreatActorType.UNKNOWN
    primary_mitres: List[str] = field(default_factory=list)
    preferred_c2: List[str] = field(default_factory=list)
    targeting: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    description: str = ""
    confidence_factors: Dict[str, float] = field(default_factory=dict)

    def matches_alias(self, query: str) -> bool:
        query_lower = query.lower()
        return (
            query_lower == self.name.lower()
            or any(query_lower == a.lower() for a in self.aliases)
        )


@dataclass
class SecurityEvent:
    """A single security event."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source_system: str = ""
    event_type: str = ""
    user_account: str = ""
    source_ip: str = ""
    destination_ip: str = ""
    process_name: str = ""
    command_line: str = ""
    hash_value: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Detection:
    """A detected APT activity."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    rule_name: str = ""
    rule_id: str = ""
    severity: DetectionSeverity = DetectionSeverity.MEDIUM
    kill_chain_phase: KillChainPhase = KillChainPhase.ACTIONS_ON_OBJECTIVES
    confidence: int = 70
    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)
    affected_systems: List[str] = field(default_factory=list)
    affected_users: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)
    mitre_techniques: List[str] = field(default_factory=list)
    events: List[SecurityEvent] = field(default_factory=list)
    description: str = ""
    recommended_actions: List[str] = field(default_factory=list)


@dataclass
class AttributionResult:
    """Result of threat actor attribution."""
    top_matches: List[Tuple[ThreatActorProfile, int]] = field(default_factory=list)
    observed_techniques: List[str] = field(default_factory=list)
    observed_tools: List[str] = field(default_factory=list)
    confidence_breakdown: Dict[str, Dict[str, float]] = field(default_factory=dict)
    attribution_time_ms: int = 0

    def best_match(self) -> Optional[Tuple[ThreatActorProfile, int]]:
        if self.top_matches:
            return self.top_matches[0]
        return None


@dataclass
class LateralMovementPath:
    """A detected lateral movement path."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    hops: List[str] = field(default_factory=list)
    user_account: str = ""
    techniques: List[LateralMovementTechnique] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: datetime = field(default_factory=datetime.utcnow)
    risk_score: int = 0
    events: List[SecurityEvent] = field(default_factory=list)

    @property
    def duration(self) -> timedelta:
        return self.end_time - self.start_time

    @property
    def hop_count(self) -> int:
        return len(self.hops)


@dataclass
class LateralMovementMap:
    """Map of all detected lateral movement."""
    paths: List[LateralMovementPath] = field(default_factory=list)
    systems_involved: Set[str] = field(default_factory=set)
    users_involved: Set[str] = field(default_factory=set)


@dataclass
class LateralMovementAnomaly:
    """An anomalous lateral movement pattern."""
    description: str = ""
    source_system: str = ""
    dest_system: str = ""
    user_account: str = ""
    technique: LateralMovementTechnique = LateralMovementTechnique.PS_EXEC
    risk_score: int = 0
    detected_at: datetime = field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Kill Chain Mapper
# ---------------------------------------------------------------------------

class KillChainMapper:
    """Maps MITRE techniques to kill chain phases."""

    TECHNIQUE_PHASE_MAP: Dict[str, KillChainPhase] = {
        "T1595": KillChainPhase.RECONNAISSANCE,
        "T1592": KillChainPhase.RECONNAISSANCE,
        "T1589": KillChainPhase.RECONNAISSANCE,
        "T1583": KillChainPhase.WEAPONIZATION,
        "T1584": KillChainPhase.WEAPONIZATION,
        "T1587": KillChainPhase.WEAPONIZATION,
        "T1566": KillChainPhase.DELIVERY,
        "T1204": KillChainPhase.DELIVERY,
        "T1195": KillChainPhase.DELIVERY,
        "T1203": KillChainPhase.EXPLOITATION,
        "T1189": KillChainPhase.EXPLOITATION,
        "T1190": KillChainPhase.EXPLOITATION,
        "T1059": KillChainPhase.INSTALLATION,
        "T1053": KillChainPhase.INSTALLATION,
        "T1547": KillChainPhase.INSTALLATION,
        "T1543": KillChainPhase.INSTALLATION,
        "T1071": KillChainPhase.COMMAND_AND_CONTROL,
        "T1105": KillChainPhase.COMMAND_AND_CONTROL,
        "T1573": KillChainPhase.COMMAND_AND_CONTROL,
        "T1572": KillChainPhase.COMMAND_AND_CONTROL,
        "T1041": KillChainPhase.ACTIONS_ON_OBJECTIVES,
        "T1048": KillChainPhase.ACTIONS_ON_OBJECTIVES,
        "T1003": KillChainPhase.ACTIONS_ON_OBJECTIVES,
        "T1005": KillChainPhase.ACTIONS_ON_OBJECTIVES,
        "T1021": KillChainPhase.ACTIONS_ON_OBJECTIVES,
    }

    def map_technique(self, technique_id: str) -> KillChainPhase:
        prefix = technique_id.split(".")[0]
        return self.TECHNIQUE_PHASE_MAP.get(prefix, KillChainPhase.ACTIONS_ON_OBJECTIVES)

    def get_techniques_for_phase(self, phase: KillChainPhase) -> List[str]:
        return [tid for tid, p in self.TECHNIQUE_PHASE_MAP.items() if p == phase]


# ---------------------------------------------------------------------------
# APT Detector
# ---------------------------------------------------------------------------

class APTDetector:
    """Main detector for APT activities."""

    def __init__(self, detection_rules: Optional[List[DetectionRule]] = None) -> None:
        self.detection_rules = detection_rules or []
        self._events: List[SecurityEvent] = []
        self._detections: List[Detection] = []
        self._kill_chain_mapper = KillChainMapper()
        self._rule_index: Dict[str, DetectionRule] = {r.name: r for r in self.detection_rules}

    def load_events(self, source: Any) -> List[SecurityEvent]:
        # In production, parse from file/API
        return []

    def add_event(self, event: SecurityEvent) -> None:
        self._events.append(event)

    def analyze(self, events: Optional[List[SecurityEvent]] = None) -> List[Detection]:
        if events is None:
            events = self._events

        detections = []
        for rule in self.detection_rules:
            if not rule.enabled:
                continue
            matched_events = self._match_rule(rule, events)
            if len(matched_events) >= 1:
                detection = self._create_detection(rule, matched_events)
                detections.append(detection)
                self._detections.append(detection)

        return detections

    def _match_rule(self, rule: DetectionRule, events: List[SecurityEvent]) -> List[SecurityEvent]:
        matched = []
        pattern = rule.pattern.lower()
        for event in events:
            event_str = f"{event.event_type} {event.process_name} {event.command_line}".lower()
            if pattern in event_str:
                matched.append(event)
            elif self._match_conditions(rule.conditions, event):
                matched.append(event)
        return matched

    def _match_conditions(self, conditions: Dict[str, Any], event: SecurityEvent) -> bool:
        for key, value in conditions.items():
            event_value = getattr(event, key, None) or event.metadata.get(key)
            if event_value is None:
                return False
            if isinstance(value, str) and value.lower() not in str(event_value).lower():
                return False
        return True

    def _create_detection(self, rule: DetectionRule, events: List[SecurityEvent]) -> Detection:
        affected_systems = list(set(e.source_system for e in events if e.source_system))
        affected_users = list(set(e.user_account for e in events if e.user_account))
        first_seen = min(e.timestamp for e in events) if events else datetime.utcnow()
        last_seen = max(e.timestamp for e in events) if events else datetime.utcnow()

        return Detection(
            rule_name=rule.name,
            rule_id=rule.id,
            severity=rule.severity,
            kill_chain_phase=rule.kill_chain_phase,
            confidence=min(70 + len(events) * 5, 100),
            first_seen=first_seen,
            last_seen=last_seen,
            affected_systems=affected_systems,
            affected_users=affected_users,
            mitre_techniques=[rule.mitre_id] if rule.mitre_id else [],
            events=events,
            description=f"Detected {rule.name} across {len(events)} events",
        )

    def get_detections_by_phase(self, phase: KillChainPhase) -> List[Detection]:
        return [d for d in self._detections if d.kill_chain_phase == phase]

    def get_kill_chain_summary(self) -> Dict[str, int]:
        summary = {}
        for phase in KillChainPhase:
            count = len(self.get_detections_by_phase(phase))
            if count > 0:
                summary[phase.value] = count
        return summary


# ---------------------------------------------------------------------------
# Attribution Engine
# ---------------------------------------------------------------------------

class AttributionEngine:
    """Engine for attributing activities to threat actors."""

    def __init__(self) -> None:
        self._actor_profiles: List[ThreatActorProfile] = []

    def load_actor_profile(self, profile: ThreatActorProfile) -> None:
        self._actor_profiles.append(profile)

    def attribute(
        self,
        observed_techniques: List[str],
        observed_tools: Optional[List[str]] = None,
        targeting_patterns: Optional[List[str]] = None,
    ) -> AttributionResult:
        observed_tools = observed_tools or []
        targeting_patterns = targeting_patterns or []

        scores: List[Tuple[ThreatActorProfile, int]] = []
        breakdown: Dict[str, Dict[str, float]] = {}

        for profile in self._actor_profiles:
            score, details = self._score_actor(profile, observed_techniques, observed_tools, targeting_patterns)
            if score > 0:
                scores.append((profile, score))
                breakdown[profile.name] = details

        scores.sort(key=lambda x: x[1], reverse=True)

        return AttributionResult(
            top_matches=scores,
            observed_techniques=observed_techniques,
            observed_tools=observed_tools,
            confidence_breakdown=breakdown,
        )

    def _score_actor(
        self,
        profile: ThreatActorProfile,
        techniques: List[str],
        tools: List[str],
        targeting: List[str],
    ) -> Tuple[int, Dict[str, float]]:
        details: Dict[str, float] = {}

        # Technique overlap
        technique_overlap = set(techniques) & set(profile.primary_mitres)
        technique_score = min(len(technique_overlap) / max(len(profile.primary_mitres), 1) * 40, 40)
        details["techniques"] = technique_score

        # Tool overlap
        tool_overlap = set(tools) & set(profile.tools)
        tool_score = min(len(tool_overlap) / max(len(profile.tools), 1) * 30, 30)
        details["tools"] = tool_score

        # Targeting overlap
        targeting_overlap = set(t.lower() for t in targeting) & set(t.lower() for t in profile.targeting)
        targeting_score = min(len(targeting_overlap) / max(len(profile.targeting), 1) * 30, 30)
        details["targeting"] = targeting_score

        total_score = int(technique_score + tool_score + targeting_score)
        return total_score, details


# ---------------------------------------------------------------------------
# Lateral Movement Analyzer
# ---------------------------------------------------------------------------

class LateralMovementAnalyzer:
    """Analyzes lateral movement patterns."""

    def __init__(self) -> None:
        self._auth_events: List[SecurityEvent] = []

    def analyze_auth_events(self, events: List[SecurityEvent]) -> LateralMovementMap:
        movement_map = LateralMovementMap()

        # Group events by user
        user_events: Dict[str, List[SecurityEvent]] = defaultdict(list)
        for event in events:
            if event.user_account:
                user_events[event.user_account].append(event)

        for user, user_evts in user_events.items():
            paths = self._build_movement_paths(user, user_evts)
            movement_map.paths.extend(paths)
            for path in paths:
                movement_map.systems_involved.update(path.hops)
                movement_map.users_involved.add(user)

        return movement_map

    def _build_movement_paths(self, user: str, events: List[SecurityEvent]) -> List[LateralMovementPath]:
        paths = []
        events.sort(key=lambda e: e.timestamp)

        current_path: List[str] = []
        path_events: List[SecurityEvent] = []
        current_hops: Set[str] = set()

        for event in events:
            src = event.source_system or event.source_ip
            dst = event.destination_ip or event.source_system

            if src and dst and src != dst:
                if src not in current_hops:
                    current_path.append(src)
                    current_hops.add(src)
                if dst not in current_hops:
                    current_path.append(dst)
                    current_hops.add(dst)
                path_events.append(event)

            if len(current_path) >= 3:
                techniques = self._detect_techniques(path_events)
                risk = self._calculate_risk(current_path, techniques)
                paths.append(LateralMovementPath(
                    hops=current_path.copy(),
                    user_account=user,
                    techniques=techniques,
                    start_time=path_events[0].timestamp,
                    end_time=path_events[-1].timestamp,
                    risk_score=risk,
                    events=path_events.copy(),
                ))
                current_path = []
                path_events = []
                current_hops.clear()

        return paths

    def _detect_techniques(self, events: List[SecurityEvent]) -> List[LateralMovementTechnique]:
        techniques = []
        for event in events:
            proc = event.process_name.lower()
            if "psexec" in proc or "svcctl" in event.command_line.lower():
                techniques.append(LateralMovementTechnique.PS_EXEC)
            elif "wmic" in proc or "wmiprvse" in proc:
                techniques.append(LateralMovementTechnique.WMI)
            elif "mstsc" in proc or "rdp" in event.command_line.lower():
                techniques.append(LateralMovementTechnique.RDP)
            elif "net" in proc and "use" in event.command_line.lower():
                techniques.append(LateralMovementTechnique.SMB)
        return list(set(techniques))

    def _calculate_risk(self, hops: List[str], techniques: List[LateralMovementTechnique]) -> int:
        risk = len(hops) * 10
        risk += len(techniques) * 15
        if LateralMovementTechnique.PASS_THE_HASH in techniques:
            risk += 30
        if LateralMovementTechnique.GOLDEN_TICKET in techniques:
            risk += 50
        return min(100, risk)

    def detect_anomalies(self, movement_map: LateralMovementMap) -> List[LateralMovementAnomaly]:
        anomalies = []
        for path in movement_map.paths:
            if path.risk_score > 70:
                anomalies.append(LateralMovementAnomaly(
                    description=f"High-risk lateral movement: {path.hop_count} hops via {', '.join(t.value for t in path.techniques)}",
                    source_system=path.hops[0] if path.hops else "",
                    dest_system=path.hops[-1] if path.hops else "",
                    user_account=path.user_account,
                    technique=path.techniques[0] if path.techniques else LateralMovementTechnique.PS_EXEC,
                    risk_score=path.risk_score,
                ))
            if path.duration < timedelta(minutes=5) and path.hop_count > 5:
                anomalies.append(LateralMovementAnomaly(
                    description=f"Rapid lateral movement: {path.hop_count} hops in {path.duration}",
                    source_system=path.hops[0] if path.hops else "",
                    dest_system=path.hops[-1] if path.hops else "",
                    user_account=path.user_account,
                    risk_score=path.risk_score,
                ))
        return anomalies


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the APT detection module."""
    print("=" * 60)
    print("  APT Detection Module — Demo")
    print("=" * 60)

    # Initialize detector
    detector = APTDetector(
        detection_rules=[
            DetectionRule(
                name="lateral_movement_psexec",
                severity=DetectionSeverity.HIGH,
                mitre_id="T1021.002",
                kill_chain_phase=KillChainPhase.ACTIONS_ON_OBJECTIVES,
                pattern="psexec",
            ),
            DetectionRule(
                name="credential_dumping",
                severity=DetectionSeverity.CRITICAL,
                mitre_id="T1003.001",
                kill_chain_phase=KillChainPhase.ACTIONS_ON_OBJECTIVES,
                pattern="lsass",
            ),
        ]
    )

    # Add sample events
    events = [
        SecurityEvent(
            source_system="web-server-01",
            event_type="process_execution",
            user_account="SYSTEM",
            process_name="psexec.exe",
            command_line="psexec \\\\dc-01 cmd.exe",
        ),
        SecurityEvent(
            source_system="dc-01",
            event_type="process_access",
            user_account="SYSTEM",
            process_name="procdump.exe",
            command_line="procdump -ma lsass.exe",
        ),
    ]
    for event in events:
        detector.add_event(event)

    # Analyze
    detections = detector.analyze()
    print(f"\n[+] Detections: {len(detections)}")
    for det in detections:
        print(f"    - {det.rule_name} ({det.severity.value})")
        print(f"      Kill Chain: {det.kill_chain_phase.value}")
        print(f"      Confidence: {det.confidence}%")

    # Kill chain summary
    summary = detector.get_kill_chain_summary()
    print(f"\n[+] Kill Chain Summary: {summary}")

    # Attribution
    attribution = AttributionEngine()
    attribution.load_actor_profile(ThreatActorProfile(
        name="APT29",
        aliases=["Cozy Bear"],
        primary_mitres=["T1195.002", "T1071.001", "T1059.001", "T1003.001"],
        tools=["WellMess", "SUNBURST"],
        targeting=["government", "technology"],
    ))

    result = attribution.attribute(
        observed_techniques=["T1003.001", "T1021.002"],
        observed_tools=["SUNBURST"],
    )
    print(f"\n[+] Attribution Results:")
    for actor, score in result.top_matches:
        print(f"    {actor.name}: {score}% confidence")

    # Lateral movement
    lm_analyzer = LateralMovementAnalyzer()
    lm_map = lm_analyzer.analyze_auth_events(events)
    print(f"\n[+] Lateral Movement:")
    print(f"    Paths: {len(lm_map.paths)}")
    print(f"    Systems: {lm_map.systems_involved}")

    anomalies = lm_analyzer.detect_anomalies(lm_map)
    print(f"    Anomalies: {len(anomalies)}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
