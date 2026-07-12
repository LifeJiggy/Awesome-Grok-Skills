"""
Threat Intelligence Module
Comprehensive CTI collection, analysis, and dissemination framework
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class IndicatorType(Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DOMAIN = "domain"
    URL = "url"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    EMAIL = "email"
    CVE = "cve"
    FILE_NAME = "file_name"
    REGISTRY_KEY = "registry_key"
    MUTEX = "mutex"
    USER_AGENT = "user_agent"


class TLPLevel(Enum):
    CLEAR = "clear"
    GREEN = "green"
    AMBER = "amber"
    AMBER_STRICT = "amber+strict"
    RED = "red"


class ConfidenceLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class SeverityLevel(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatActorType(Enum):
    ADVERSARY = "adversary"
    INSIDER = "insider"
    COMPETITOR = "competitor"
    HACKTIVIST = "hacktivist"
    STATE_SPONSORED = "state-sponsored"
    ORGANIZED_CRIME = "organized-crime"


class Motivation(Enum):
    ESPIONAGE = "espionage"
    FINANCIAL = "financial"
    DESTRUCTION = "destruction"
    DISRUPTION = "disruption"
    HACKTIVISM = "hacktivism"
    IDEOLOGY = "ideology"
    UNKNOWN = "unknown"


class Sophistication(Enum):
    NONE = "none"
    MINIMAL = "minimal"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    INNOVATOR = "innovator"
    STRATEGIC = "strategic"


class IntelSourceReliability(Enum):
    A_RELIABLE = "A"
    B_USUALLY_RELIABLE = "B"
    C_FAIRLY_RELIABLE = "C"
    D_NOT_USUALLY_RELIABLE = "D"
    E_UNRELIABLE = "E"
    F_CANNOT_BE_JUDGED = "F"


class ReportFormat(Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    JSON = "json"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class IntelSource:
    """Represents a threat intelligence feed or source."""
    name: str
    url: str
    api_key: Optional[str] = None
    reliability: IntelSourceReliability = IntelSourceReliability.C_FAIRLY_RELIABLE
    enabled: bool = True
    last_polled: Optional[datetime] = None
    poll_interval_minutes: int = 60
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_stale(self, max_age_hours: int = 24) -> bool:
        if self.last_polled is None:
            return True
        return (datetime.utcnow() - self.last_polled) > timedelta(hours=max_age_hours)

    def mark_polled(self) -> None:
        self.last_polled = datetime.utcnow()


@dataclass
class Indicator:
    """Represents a single indicator of compromise."""
    id: str
    indicator_type: IndicatorType
    value: str
    tlp: TLPLevel = TLPLevel.AMBER
    confidence: int = 50
    source: str = "unknown"
    tags: List[str] = field(default_factory=list)
    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)
    expiration: Optional[datetime] = None
    threat_actors: List[str] = field(default_factory=list)
    mitre_techniques: List[str] = field(default_factory=list)
    campaigns: List[str] = field(default_factory=list)
    sightings: int = 1
    false_positive_rate: float = 0.0
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        if self.expiration is None:
            return False
        return datetime.utcnow() > self.expiration

    @property
    def confidence_level(self) -> ConfidenceLevel:
        if self.confidence >= 90:
            return ConfidenceLevel.VERY_HIGH
        elif self.confidence >= 75:
            return ConfidenceLevel.HIGH
        elif self.confidence >= 50:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    @property
    def is_actionable(self) -> bool:
        return not self.is_expired and self.confidence >= 50 and self.false_positive_rate < 0.3

    def fingerprint(self) -> str:
        raw = f"{self.indicator_type.value}:{self.value.lower().strip()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_stix(self) -> Dict[str, Any]:
        stix_type_map = {
            IndicatorType.IPV4: ("ipv4-addr", "value"),
            IndicatorType.DOMAIN: ("domain-name", "value"),
            IndicatorType.URL: ("url", "value"),
            IndicatorType.MD5: ("file", "hashes.MD5"),
            IndicatorType.SHA1: ("file", "hashes.SHA-1"),
            IndicatorType.SHA256: ("file", "hashes.SHA-256"),
            IndicatorType.EMAIL: ("email-addr", "value"),
        }
        stix_obj, property_name = stix_type_map.get(
            self.indicator_type,
            ("indicator", "pattern")
        )
        return {
            "type": "indicator",
            "spec_version": "2.1",
            "id": f"indicator--{self.id}",
            "created": self.first_seen.isoformat(),
            "modified": self.last_seen.isoformat(),
            "name": f"{self.indicator_type.value}: {self.value}",
            "pattern": f"[{stix_obj}:{property_name} = '{self.value}']",
            "pattern_type": "stix",
            "valid_from": self.first_seen.isoformat(),
            "confidence": self.confidence,
            "labels": self.tags,
        }


@dataclass
class ThreatActor:
    """Represents a threat actor or group."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    aliases: List[str] = field(default_factory=list)
    actor_type: ThreatActorType = ThreatActorType.ADVERSARY
    motivation: Motivation = Motivation.UNKNOWN
    sophistication: Sophistication = Sophistication.INTERMEDIATE
    targeting: List[str] = field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    country: Optional[str] = None
    description: str = ""
    tools: List[str] = field(default_factory=list)
    campaigns: List[str] = field(default_factory=list)
    mitre_techniques: List[str] = field(default_factory=list)
    known_infrastructure: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def matches_alias(self, query: str) -> bool:
        query_lower = query.lower()
        return (
            query_lower == self.name.lower()
            or any(query_lower == alias.lower() for alias in self.aliases)
        )

    def to_stix_bundle(self) -> Dict[str, Any]:
        return {
            "type": "bundle",
            "id": f"bundle--{uuid.uuid4()}",
            "objects": [
                {
                    "type": "threat-actor",
                    "spec_version": "2.1",
                    "id": f"threat-actor--{self.id}",
                    "created": (self.first_seen or datetime.utcnow()).isoformat(),
                    "modified": (self.last_seen or datetime.utcnow()).isoformat(),
                    "name": self.name,
                    "aliases": self.aliases,
                    "threat_actor_types": [self.actor_type.value],
                    "sophistication": self.sophistication.value,
                    "primary_motivation": self.motivation.value,
                    "goals": self.targeting,
                }
            ],
        }


@dataclass
class Campaign:
    """Represents a threat campaign."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    objective: str = ""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    targets: List[str] = field(default_factory=list)
    attack_patterns: List[Dict[str, str]] = field(default_factory=list)
    threat_actors: List[str] = field(default_factory=list)
    indicators: List[str] = field(default_factory=list)
    description: str = ""

    @property
    def is_active(self) -> bool:
        if self.end_date:
            return self.end_date > datetime.utcnow()
        return True

    @property
    def duration_days(self) -> Optional[int]:
        if self.start_date is None:
            return None
        end = self.end_date or datetime.utcnow()
        return (end - self.start_date).days


@dataclass
class IntelReport:
    """Structured intelligence report."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    classification: str = "TLP:GREEN"
    executive_summary: str = ""
    sections: List[Dict[str, Any]] = field(default_factory=list)
    indicators: List[Indicator] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.utcnow)
    authors: List[str] = field(default_factory=list)
    distribution: List[str] = field(default_factory=list)

    def add_section(self, heading: str, content: str, severity: SeverityLevel = SeverityLevel.INFO) -> None:
        self.sections.append({
            "heading": heading,
            "content": content,
            "severity": severity.value,
        })

    def render_markdown(self) -> str:
        lines = [
            f"# {self.title}",
            f"\n**Classification:** {self.classification}",
            f"**Date:** {self.created.strftime('%Y-%m-%d')}",
            f"**Authors:** {', '.join(self.authors)}",
            f"\n## Executive Summary\n\n{self.executive_summary}",
        ]
        for section in self.sections:
            lines.append(f"\n## {section['heading']}\n\n{section['content']}")
        if self.indicators:
            lines.append("\n## Indicators of Compromise\n")
            lines.append("| Type | Value | Confidence | TLP |")
            lines.append("|------|-------|------------|-----|")
            for ind in self.indicators:
                lines.append(f"| {ind.indicator_type.value} | `{ind.value}` | {ind.confidence}% | {ind.tlp.value} |")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "classification": self.classification,
            "executive_summary": self.executive_summary,
            "sections": self.sections,
            "indicator_count": len(self.indicators),
            "created": self.created.isoformat(),
            "authors": self.authors,
        }


@dataclass
class PollConfig:
    """Configuration for feed polling."""
    interval_minutes: int = 60
    full_sync: bool = False
    timeout_seconds: int = 30
    retry_count: int = 3
    filters: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Indicator Factory
# ---------------------------------------------------------------------------

class IndicatorFactory:
    """Factory for creating and validating indicators."""

    IP_REGEX = re.compile(
        r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
    )
    DOMAIN_REGEX = re.compile(
        r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    )
    MD5_REGEX = re.compile(r"^[a-fA-F0-9]{32}$")
    SHA1_REGEX = re.compile(r"^[a-fA-F0-9]{40}$")
    SHA256_REGEX = re.compile(r"^[a-fA-F0-9]{64}$")
    CVE_REGEX = re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE)
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

    VALIDATORS: Dict[IndicatorType, Any] = {
        IndicatorType.IPV4: IP_REGEX,
        IndicatorType.DOMAIN: DOMAIN_REGEX,
        IndicatorType.MD5: MD5_REGEX,
        IndicatorType.SHA1: SHA1_REGEX,
        IndicatorType.SHA256: SHA256_REGEX,
        IndicatorType.CVE: CVE_REGEX,
        IndicatorType.EMAIL: EMAIL_REGEX,
    }

    def detect_type(self, value: str) -> IndicatorType:
        value = value.strip()
        if self.IP_REGEX.match(value):
            return IndicatorType.IPV4
        if self.SHA256_REGEX.match(value):
            return IndicatorType.SHA256
        if self.SHA1_REGEX.match(value):
            return IndicatorType.SHA1
        if self.MD5_REGEX.match(value):
            return IndicatorType.MD5
        if self.CVE_REGEX.match(value):
            return IndicatorType.CVE
        if self.EMAIL_REGEX.match(value):
            return IndicatorType.EMAIL
        if value.startswith("http://") or value.startswith("https://"):
            return IndicatorType.URL
        if self.DOMAIN_REGEX.match(value):
            return IndicatorType.DOMAIN
        raise ValueError(f"Unable to auto-detect indicator type for: {value}")

    def validate(self, indicator_type: IndicatorType, value: str) -> bool:
        validator = self.VALIDATORS.get(indicator_type)
        if validator is None:
            return True
        return bool(validator.match(value.strip()))

    def create_indicator(
        self,
        indicator_type: str,
        value: str,
        tlp: str = "amber",
        confidence: int = 50,
        source: str = "manual",
        tags: Optional[List[str]] = None,
        description: str = "",
        expiration_days: Optional[int] = None,
    ) -> Indicator:
        itype = IndicatorType(indicator_type)
        if not self.validate(itype, value):
            raise ValueError(f"Invalid value '{value}' for indicator type '{indicator_type}'")

        expiration = None
        if expiration_days:
            expiration = datetime.utcnow() + timedelta(days=expiration_days)

        return Indicator(
            id=str(uuid.uuid4()),
            indicator_type=itype,
            value=value.strip(),
            tlp=TLPLevel(tlp),
            confidence=min(max(confidence, 0), 100),
            source=source,
            tags=tags or [],
            description=description,
            expiration=expiration,
        )

    def create_from_batch(self, raw_values: List[str], source: str = "batch") -> List[Indicator]:
        indicators = []
        for raw in raw_values:
            try:
                itype = self.detect_type(raw)
                ind = self.create_indicator(
                    indicator_type=itype.value,
                    value=raw,
                    source=source,
                )
                indicators.append(ind)
            except ValueError as e:
                logger.warning("Skipping invalid indicator %s: %s", raw, e)
        return indicators


# ---------------------------------------------------------------------------
# Indicator Repository
# ---------------------------------------------------------------------------

class IndicatorRepository:
    """In-memory indicator store with deduplication and search."""

    def __init__(self) -> None:
        self._indicators: Dict[str, Indicator] = {}
        self._fingerprints: Set[str] = set()

    def add(self, indicator: Indicator) -> bool:
        fp = indicator.fingerprint()
        if fp in self._fingerprints:
            existing = self._indicators.get(fp)
            if existing:
                existing.sightings += 1
                existing.last_seen = datetime.utcnow()
                existing.confidence = min(existing.confidence + 5, 100)
            return False
        self._indicators[fp] = indicator
        self._fingerprints.add(fp)
        return True

    def get(self, fingerprint: str) -> Optional[Indicator]:
        return self._indicators.get(fingerprint)

    def search_by_type(self, indicator_type: IndicatorType) -> List[Indicator]:
        return [i for i in self._indicators.values() if i.indicator_type == indicator_type]

    def search_by_tag(self, tag: str) -> List[Indicator]:
        tag_lower = tag.lower()
        return [i for i in self._indicators.values() if tag_lower in [t.lower() for t in i.tags]]

    def search_by_source(self, source: str) -> List[Indicator]:
        return [i for i in self._indicators.values() if i.source == source]

    def get_expired(self) -> List[Indicator]:
        return [i for i in self._indicators.values() if i.is_expired]

    def get_actionable(self) -> List[Indicator]:
        return [i for i in self._indicators.values() if i.is_actionable]

    def remove_expired(self) -> int:
        expired = self.get_expired()
        for ind in expired:
            fp = ind.fingerprint()
            self._indicators.pop(fp, None)
            self._fingerprints.discard(fp)
        return len(expired)

    def stats(self) -> Dict[str, Any]:
        total = len(self._indicators)
        type_counts = {}
        for ind in self._indicators.values():
            type_counts[ind.indicator_type.value] = type_counts.get(ind.indicator_type.value, 0) + 1
        return {
            "total": total,
            "by_type": type_counts,
            "expired": len(self.get_expired()),
            "actionable": len(self.get_actionable()),
        }


# ---------------------------------------------------------------------------
# Threat Intelligence Engine
# ---------------------------------------------------------------------------

class ThreatIntelEngine:
    """Main engine orchestrating CTI operations."""

    def __init__(
        self,
        feeds: Optional[List[IntelSource]] = None,
        confidence_threshold: int = 50,
        enable_enrichment: bool = True,
    ) -> None:
        self.feeds = feeds or []
        self.confidence_threshold = confidence_threshold
        self.enable_enrichment = enable_enrichment
        self.indicator_factory = IndicatorFactory()
        self.repository = IndicatorRepository()
        self._threat_actors: Dict[str, ThreatActor] = {}
        self._campaigns: Dict[str, Campaign] = {}
        self._reports: List[IntelReport] = []
        self._enrichment_callbacks: List[Callable[[Indicator], Optional[Dict[str, Any]]]] = []
        logger.info("ThreatIntelEngine initialized with %d feeds", len(self.feeds))

    def register_enrichment(self, callback: Callable[[Indicator], Optional[Dict[str, Any]]]) -> None:
        self._enrichment_callbacks.append(callback)

    def ingest_indicator(self, indicator: Indicator) -> bool:
        added = self.repository.add(indicator)
        if added:
            logger.info("Ingested new indicator: %s (%s)", indicator.value, indicator.indicator_type.value)
        else:
            logger.debug("Indicator already exists, updated sighting: %s", indicator.value)
        return added

    def ingest_batch(self, indicators: List[Indicator]) -> int:
        return sum(1 for ind in indicators if self.ingest_indicator(ind))

    def enrich_indicator(self, indicator: Indicator) -> Indicator:
        if not self.enable_enrichment:
            return indicator
        for callback in self._enrichment_callbacks:
            try:
                result = callback(indicator)
                if result:
                    indicator.metadata.update(result)
            except Exception as e:
                logger.warning("Enrichment callback failed: %s", e)
        return indicator

    def add_threat_actor(self, actor: ThreatActor) -> None:
        self._threat_actors[actor.id] = actor
        logger.info("Added threat actor: %s", actor.name)

    def find_threat_actor(self, query: str) -> List[ThreatActor]:
        return [a for a in self._threat_actors.values() if a.matches_alias(query)]

    def add_campaign(self, campaign: Campaign) -> None:
        self._campaigns[campaign.id] = campaign
        logger.info("Added campaign: %s", campaign.name)

    def create_report(
        self,
        title: str,
        classification: str = "TLP:GREEN",
        executive_summary: str = "",
    ) -> IntelReport:
        report = IntelReport(
            title=title,
            classification=classification,
            executive_summary=executive_summary,
        )
        self._reports.append(report)
        return report

    def get_recent_indicators(self, days: int = 30) -> List[Indicator]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [
            i for i in self.repository.get_actionable()
            if i.last_seen >= cutoff
        ]

    def get_stats(self) -> Dict[str, Any]:
        repo_stats = self.repository.stats()
        repo_stats["threat_actors"] = len(self._threat_actors)
        repo_stats["campaigns"] = len(self._campaigns)
        repo_stats["reports"] = len(self._reports)
        repo_stats["feeds"] = len(self.feeds)
        return repo_stats

    def export_all_stix(self) -> Dict[str, Any]:
        objects = []
        for ind in self.repository.get_actionable():
            objects.append(ind.to_stix())
        for actor in self._threat_actors.values():
            bundle = actor.to_stix_bundle()
            objects.extend(bundle.get("objects", []))
        return {
            "type": "bundle",
            "id": f"bundle--{uuid.uuid4()}",
            "objects": objects,
        }

    def purge_expired(self) -> int:
        count = self.repository.remove_expired()
        logger.info("Purged %d expired indicators", count)
        return count


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the threat intelligence module capabilities."""
    print("=" * 60)
    print("  Threat Intelligence Module — Demo")
    print("=" * 60)

    # Initialize engine
    engine = ThreatIntelEngine(
        feeds=[
            IntelSource(name="alienvault-otx", url="https://otx.alienvault.com"),
            IntelSource(name="abuse-ch", url="https://urlhaus-api.abuse.ch"),
        ],
        confidence_threshold=60,
    )

    # Create indicators
    factory = IndicatorFactory()
    indicators = factory.create_from_batch([
        "198.51.100.42",
        "evil-c2.example.com",
        "https://malware.example.com/payload.exe",
        "d41d8cd98f00b204e9800998ecf8427e",
        "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",
        "CVE-2024-12345",
    ])
    print(f"\n[+] Created {len(indicators)} indicators from batch")

    # Ingest into repository
    added = engine.ingest_batch(indicators)
    print(f"[+] Ingested {added} new indicators into repository")

    # Enrich an indicator
    enriched = engine.enrich_indicator(indicators[0])
    print(f"[+] Enriched indicator: {enriched.value} (confidence: {enriched.confidence}%)")

    # Add a threat actor
    actor = ThreatActor(
        name="APT29",
        aliases=["Cozy Bear", "The Dukes"],
        motivation=Motivation.ESPIONAGE,
        sophistication=Sophistication.ADVANCED,
        targeting=["government", "think-tanks"],
        country="RU",
        mitre_techniques=["T1195.002", "T1071.001", "T1059.001"],
    )
    engine.add_threat_actor(actor)
    print(f"[+] Added threat actor: {actor.name} ({', '.join(actor.aliases)})")

    # Find threat actor
    results = engine.find_threat_actor("Cozy Bear")
    print(f"[+] Search for 'Cozy Bear' found: {[a.name for a in results]}")

    # Create campaign
    campaign = Campaign(
        name="SolarWinds Supply Chain Attack",
        objective="Compromise software supply chain",
        targets=["us-government", "technology"],
        attack_patterns=[
            {"technique_id": "T1195.002", "name": "Supply Chain Compromise"},
        ],
    )
    engine.add_campaign(campaign)
    print(f"[+] Added campaign: {campaign.name}")

    # Create intelligence report
    report = engine.create_report(
        title="Q4 2024 Threat Landscape",
        classification="TLP:AMBER",
        executive_summary="Elevated ransomware and APT activity targeting critical infrastructure.",
    )
    report.add_section("Key Findings", "47 unique threat actor groups active.", SeverityLevel.HIGH)
    report.add_section("Recommendations", "Implement zero-trust architecture.", SeverityLevel.MEDIUM)
    print(f"[+] Created report: {report.title}")

    # Repository stats
    stats = engine.get_stats()
    print(f"\n[+] Engine Statistics:")
    print(f"    Total indicators: {stats['total']}")
    print(f"    Actionable: {stats['actionable']}")
    print(f"    Threat actors: {stats['threat_actors']}")
    print(f"    Campaigns: {stats['campaigns']}")
    print(f"    Reports: {stats['reports']}")

    # STIX export
    stix_bundle = engine.export_all_stix()
    print(f"[+] Exported STIX bundle with {len(stix_bundle['objects'])} objects")

    # Render report
    md = report.render_markdown()
    print(f"\n[+] Report rendered ({len(md)} chars, first 200 chars):")
    print(md[:200] + "...")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
