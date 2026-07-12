"""
Threat Intelligence Module
IOC management, actor profiling, ATT&CK mapping, and detection rules.
"""

from __future__ import annotations

import hashlib
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

class IOCType(Enum):
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH_MD5 = "file_hash_md5"
    FILE_HASH_SHA1 = "file_hash_sha1"
    FILE_HASH_SHA256 = "file_hash_sha256"
    EMAIL = "email"
    CVE = "cve"


class TLP(Enum):
    WHITE = "white"
    GREEN = "green"
    AMBER = "amber"
    RED = "red"


class SourceReliability(Enum):
    A = "A_completely_reliable"
    B = "B_usually_reliable"
    C = "C_fairly_reliable"
    D = "D_not_usually_reliable"
    E = "E_unreliable"
    F = "F_reliability_unknown"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class IOC:
    """Indicator of Compromise."""
    indicator: str
    ioc_type: IOCType
    confidence: int
    source: str
    tlp: TLP = TLP.AMBER
    tags: List[str] = field(default_factory=list)
    first_seen: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expiry: str = ""
    enrichment: Dict[str, Any] = field(default_factory=dict)
    related_actors: List[str] = field(default_factory=list)


@dataclass
class ThreatActor:
    """Threat actor profile."""
    name: str
    aliases: List[str]
    attribution: str
    target_sectors: List[str]
    ttps: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    infrastructure: List[str] = field(default_factory=list)
    description: str = ""
    motivation: str = ""
    sophistication: str = "advanced"


@dataclass
class ATTCKTechnique:
    """MITRE ATT&CK technique."""
    technique_id: str
    technique_name: str
    tactic: str
    description: str = ""
    detection: str = ""
    mitigation: str = ""


@dataclass
class DiamondModelResult:
    """Diamond model analysis result."""
    adversary: str
    capability: str
    infrastructure: str
    victim: str
    relationships: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class DetectionRule:
    """Detection rule (Sigma/YARA)."""
    rule_name: str
    rule_type: str
    severity: str
    description: str
    detection_query: str = ""
    false_positives: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)


@dataclass
class IntelFeed:
    """Threat intelligence feed."""
    name: str
    source: str
    format: str
    ioc_count: int = 0
    last_updated: str = ""
    reliability: SourceReliability = SourceReliability.B


# ---------------------------------------------------------------------------
# IOC Manager
# ---------------------------------------------------------------------------

class IOCManager:
    """Manage indicators of compromise."""

    def __init__(self):
        self._iocs: Dict[str, IOC] = {}

    def create_ioc(
        self,
        indicator: str,
        ioc_type: str,
        confidence: int = 50,
        source: str = "",
        tags: Optional[List[str]] = None,
        tlp: str = "amber",
    ) -> IOC:
        ioc = IOC(
            indicator=indicator,
            ioc_type=IOCType(ioc_type),
            confidence=confidence,
            source=source,
            tlp=TLP(tlp),
            tags=tags or [],
            enrichment=self._auto_enrich(indicator, ioc_type),
        )
        self._iocs[indicator] = ioc
        return ioc

    def lookup(self, indicator: str) -> Optional[IOC]:
        return self._iocs.get(indicator)

    def search_by_tag(self, tag: str) -> List[IOC]:
        return [ioc for ioc in self._iocs.values() if tag in ioc.tags]

    def deduplicate(self) -> int:
        before = len(self._iocs)
        seen: Dict[str, str] = {}
        to_remove: List[str] = []
        for indicator, ioc in self._iocs.items():
            h = hashlib.md5(f"{ioc.indicator}:{ioc.ioc_type.value}".encode()).hexdigest()
            if h in seen:
                to_remove.append(indicator)
            else:
                seen[h] = indicator
        for k in to_remove:
            del self._iocs[k]
        return before - len(self._iocs)

    def get_expired(self, days: int = 90) -> List[IOC]:
        return list(self._iocs.values())

    def _auto_enrich(self, indicator: str, ioc_type: str) -> Dict[str, Any]:
        return {"country": "US", "asn": "AS1234", "reputation": "neutral"}


# ---------------------------------------------------------------------------
# Threat Actor Profiler
# ---------------------------------------------------------------------------

class ThreatActorProfiler:
    """Profile threat actors."""

    ACTORS = {
        "APT29": ThreatActor(
            name="APT29",
            aliases=["Cozy Bear", "The Dukes", "NOBELIUM"],
            attribution="Russia (SVR)",
            target_sectors=["government", "technology", "think_tanks"],
            ttps=["T1059.001", "T1053.005", "T1071.001", "T1078"],
            tools=["Cobalt Strike", "WellMess", "WellMail", "SolarMarker"],
            motivation="espionage",
            sophistication="advanced",
        ),
        "APT28": ThreatActor(
            name="APT28",
            aliases=["Fancy Bear", "Sofacy", "Pawn Storm"],
            attribution="Russia (GRU)",
            target_sectors=["government", "military", "media"],
            ttps=["T1566.001", "T1059.001", "T1055", "T1003.001"],
            tools=["X-Agent", "X-Tunnel", "Zebrocy", "Cobalt Strike"],
            motivation="espionage",
            sophistication="advanced",
        ),
        "Lazarus Group": ThreatActor(
            name="Lazarus Group",
            aliases=["HIDDEN COBRA", "Zinc"],
            attribution="North Korea (RGB)",
            target_sectors=["finance", "technology", "cryptocurrency"],
            ttps=["T1566.001", "T1059.001", "T1486", "T1547.001"],
            tools=["FALLCHILL", "Manuscrypt", "Hoaxcalls"],
            motivation="financial",
            sophistication="advanced",
        ),
    }

    def profile(self, actor_name: str) -> ThreatActor:
        return self.ACTORS.get(actor_name, ThreatActor(
            name=actor_name, aliases=[], attribution="Unknown",
            target_sectors=["unknown"],
        ))

    def list_actors(self) -> List[str]:
        return list(self.ACTORS.keys())


# ---------------------------------------------------------------------------
# ATT&CK Mapper
# ---------------------------------------------------------------------------

class ATTCKMapper:
    """Map observations to MITRE ATT&CK."""

    BEHAVIOR_MAP = {
        "powershell": ATTCKTechnique("T1059.001", "PowerShell", "execution", "Suspicious PowerShell execution", "Monitor PowerShell script block logging"),
        "scheduled task": ATTCKTechnique("T1053.005", "Scheduled Task", "persistence", "Scheduled task creation", "Monitor Windows Event ID 4698"),
        "smb": ATTCKTechnique("T1021.002", "SMB/Windows Admin Shares", "lateral_movement", "SMB lateral movement", "Monitor SMB connections"),
        "credential dump": ATTCKTechnique("T1003.001", "LSASS Memory", "credential_access", "LSASS credential dumping", "Monitor for LSASS access"),
        "registry": ATTCKTechnique("T1547.001", "Registry Run Keys", "persistence", "Registry persistence", "Monitor registry modifications"),
        "dns": ATTCKTechnique("T1071.004", "DNS", "command_control", "DNS C2 communication", "Monitor DNS query patterns"),
        "phishing": ATTCKTechnique("T1566.001", "Spearphishing Link", "initial_access", "Phishing emails", "Email gateway filtering"),
        "lateral movement": ATTCKTechnique("T1021.002", "SMB", "lateral_movement", "Network lateral movement", "Monitor east-west traffic"),
    }

    def map_observations(self, observations: List[str]) -> List[ATTCKTechnique]:
        techniques: List[ATTCKTechnique] = []
        seen: set = set()
        for obs in observations:
            obs_lower = obs.lower()
            for keyword, technique in self.BEHAVIOR_MAP.items():
                if keyword in obs_lower and technique.technique_id not in seen:
                    techniques.append(technique)
                    seen.add(technique.technique_id)
        return techniques


# ---------------------------------------------------------------------------
# Intel Analyzer
# ---------------------------------------------------------------------------

class IntelAnalyzer:
    """Analyze threat intelligence."""

    def diamond_model(
        self,
        adversary: str = "",
        capability: str = "",
        infrastructure: str = "",
        victim: str = "",
    ) -> DiamondModelResult:
        relationships = []
        if adversary and capability:
            relationships.append({"type": "uses", "from": adversary, "to": capability})
        if adversary and infrastructure:
            relationships.append({"type": "redirects_to", "from": adversary, "to": infrastructure})
        if adversary and victim:
            relationships.append({"type": "targets", "from": adversary, "to": victim})
        if capability and victim:
            relationships.append({"type": "compromises", "from": capability, "to": victim})
        return DiamondModelResult(
            adversary=adversary, capability=capability,
            infrastructure=infrastructure, victim=victim,
            relationships=relationships,
        )

    def kill_chain_mapping(self, techniques: List[ATTCKTechnique]) -> Dict[str, List[str]]:
        chain: Dict[str, List[str]] = {}
        for t in techniques:
            chain.setdefault(t.tactic, []).append(t.technique_id)
        return chain


# ---------------------------------------------------------------------------
# Detection Rule Generator
# ---------------------------------------------------------------------------

class DetectionRuleGenerator:
    """Generate detection rules from intelligence."""

    def generate_sigma(
        self,
        technique: str,
        description: str,
        logsource: str = "windows",
        severity: str = "medium",
    ) -> DetectionRule:
        detection = f"title: {description}\nlogsource:\n  category: {logsource}\ndetection:\n  selection:\n    EventID: 4688\n  condition: selection"
        return DetectionRule(
            rule_name=f"det_{technique.replace('.', '_')}",
            rule_type="sigma",
            severity=severity,
            description=description,
            detection_query=detection,
            false_positives=["legitimate_admin_activity"],
        )

    def generate_yara(
        self,
        malware_name: str,
        strings: Optional[List[str]] = None,
    ) -> DetectionRule:
        strings = strings or [f"string s1 = \"{malware_name}\""]
        rule = f"rule {malware_name} {{\n  strings:\n    {chr(10).join(strings)}\n  condition:\n    any of them\n}}"
        return DetectionRule(
            rule_name=f"yar_{malware_name}",
            rule_type="yara",
            severity="high",
            description=f"Detect {malware_name} malware",
            detection_query=rule,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Threat Intelligence Demo")
    print("=" * 60)

    print("\n[1] IOC Management")
    ioc_mgr = IOCManager()
    ioc = ioc_mgr.create_ioc("185.220.101.34", "ip_address", 85, "internal", ["c2", "apt29"])
    print(f"  IOC: {ioc.indicator}")
    print(f"  Confidence: {ioc.confidence}%")
    print(f"  Enrichment: {ioc.enrichment}")

    print("\n[2] Threat Actor Profiling")
    profiler = ThreatActorProfiler()
    actor = profiler.profile("APT29")
    print(f"  Name: {actor.name}")
    print(f"  Aliases: {actor.aliases}")
    print(f"  Attribution: {actor.attribution}")
    print(f"  Sectors: {actor.target_sectors}")

    print("\n[3] ATT&CK Mapping")
    mapper = ATTCKMapper()
    techniques = mapper.map_observations(["PowerShell execution", "Scheduled task creation", "SMB lateral movement"])
    for t in techniques:
        print(f"  {t.technique_id}: {t.technique_name} ({t.tactic})")

    print("\n[4] Diamond Model")
    analyzer = IntelAnalyzer()
    diamond = analyzer.diamond_model("APT29", "Cobalt Strike", "185.220.101.34", "government")
    print(f"  Relationships: {len(diamond.relationships)}")
    for r in diamond.relationships:
        print(f"    {r['from']} -> {r['to']} ({r['type']})")

    print("\n[5] Detection Rules")
    rule_gen = DetectionRuleGenerator()
    sigma = rule_gen.generate_sigma("T1059.001", "Suspicious PowerShell")
    print(f"  Sigma: {sigma.rule_name}")
    yara = rule_gen.generate_yara("Emotet", ['s1 = "Emotet"'])
    print(f"  YARA: {yara.rule_name}")

    print("\n" + "=" * 60)
    print("  Threat intelligence demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
