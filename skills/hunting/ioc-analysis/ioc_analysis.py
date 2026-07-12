"""
IOC Analysis Module
Advanced indicator of compromise analysis, correlation, and lifecycle management
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
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


class EnrichmentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"


class LifecycleState(Enum):
    NEW = "new"
    ACTIVE = "active"
    AGING = "aging"
    EXPIRED = "expired"
    RETIRED = "retired"
    ARCHIVED = "archived"


class TimeWindow(Enum):
    HOURS_1 = 1
    HOURS_6 = 6
    HOURS_24 = 24
    DAYS_7 = 7
    DAYS_30 = 30
    DAYS_90 = 90


class CorrelationType(Enum):
    SHARED_INFRASTRUCTURE = "shared_infrastructure"
    TEMPORAL_PROXIMITY = "temporal_proximity"
    BEHAVIORAL_SIMILARITY = "behavioral_similarity"
    GEOGRAPHIC_PROXIMITY = "geographic_proximity"
    ASN_OVERLAP = "asn_overlap"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class EnrichmentResult:
    """Result from a single enrichment source."""
    source: str
    status: EnrichmentStatus
    data: Dict[str, Any] = field(default_factory=dict)
    queried_at: datetime = field(default_factory=datetime.utcnow)
    response_time_ms: int = 0
    error: Optional[str] = None

    @property
    def is_successful(self) -> bool:
        return self.status == EnrichmentStatus.COMPLETED


@dataclass
class GeoLocation:
    """Geographic location information."""
    country: str = ""
    country_code: str = ""
    region: str = ""
    city: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    postal_code: str = ""


@dataclass
class ASNInfo:
    """Autonomous System Number information."""
    asn: int = 0
    name: str = ""
    organization: str = ""
    isp: str = ""
    country: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result for an indicator."""
    indicator_id: str
    value: str
    indicator_type: IndicatorType
    confidence_score: int = 0
    false_positive_rate: float = 0.0
    enrichment_count: int = 0
    enrichment_results: List[EnrichmentResult] = field(default_factory=list)
    threat_actors: List[str] = field(default_factory=list)
    campaigns: List[str] = field(default_factory=list)
    geo_location: Optional[GeoLocation] = None
    asn_info: Optional[ASNInfo] = None
    tags: List[str] = field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    analysis_time_ms: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "indicator_id": self.indicator_id,
            "value": self.value,
            "type": self.indicator_type.value,
            "confidence": self.confidence_score,
            "false_positive_rate": self.false_positive_rate,
            "enrichment_sources": self.enrichment_count,
            "threat_actors": self.threat_actors,
            "campaigns": self.campaigns,
            "geo": {
                "country": self.geo_location.country_code if self.geo_location else None,
                "city": self.geo_location.city if self.geo_location else None,
            },
            "asn": self.asn_info.asn if self.asn_info else None,
            "tags": self.tags,
        }


@dataclass
class CorrelationGroup:
    """A group of correlated indicators."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    indicators: List[AnalysisResult] = field(default_factory=list)
    correlation_type: CorrelationType = CorrelationType.SHARED_INFRASTRUCTURE
    correlation_confidence: int = 0
    datasets: List[str] = field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    description: str = ""


@dataclass
class LifecycleStatus:
    """Status of an indicator in its lifecycle."""
    state: LifecycleState = LifecycleState.NEW
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    retired_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    notes: str = ""

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    @property
    def days_until_expiry(self) -> Optional[int]:
        if self.expires_at is None:
            return None
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)


@dataclass
class EnrichmentSource:
    """Configuration for an enrichment data source."""
    name: str
    api_key: Optional[str] = None
    base_url: str = ""
    rate_limit_per_minute: int = 60
    enabled: bool = True
    timeout_seconds: int = 30
    priority: int = 1  # Lower = higher priority


@dataclass
class LifecyclePolicy:
    """Policy governing indicator lifecycle management."""
    default_ttl_days: int = 90
    high_confidence_ttl_days: int = 180
    auto_retire: bool = True
    archive_after_days: int = 365
    max_sightings_before_escalate: int = 10
    min_confidence_to_activate: int = 30


# ---------------------------------------------------------------------------
# Enrichment Provider (Abstract)
# ---------------------------------------------------------------------------

class EnrichmentProvider(ABC):
    """Base class for enrichment providers."""

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def enrich(self, value: str, indicator_type: IndicatorType) -> EnrichmentResult:
        ...


class VirusTotalProvider(EnrichmentProvider):
    """Enrichment via VirusTotal API."""

    def name(self) -> str:
        return "virustotal"

    def enrich(self, value: str, indicator_type: IndicatorType) -> EnrichmentResult:
        # Placeholder for actual VT API integration
        data = {
            "detection_ratio": "0/70",
            "reputation": 0,
            "categories": [],
            "last_analysis_date": datetime.utcnow().isoformat(),
        }
        return EnrichmentResult(
            source=self.name(),
            status=EnrichmentStatus.COMPLETED,
            data=data,
            response_time_ms=245,
        )


class AbuseIPDBProvider(EnrichmentProvider):
    """Enrichment via AbuseIPDB API."""

    def name(self) -> str:
        return "abuseipdb"

    def enrich(self, value: str, indicator_type: IndicatorType) -> EnrichmentResult:
        data = {
            "abuse_confidence_score": 0,
            "total_reports": 0,
            "country_code": "US",
            "isp": "Example ISP",
            "usage_type": "Data Center/Web Hosting",
        }
        return EnrichmentResult(
            source=self.name(),
            status=EnrichmentStatus.COMPLETED,
            data=data,
            response_time_ms=180,
        )


class ShodanProvider(EnrichmentProvider):
    """Enrichment via Shodan API."""

    def name(self) -> str:
        return "shodan"

    def enrich(self, value: str, indicator_type: IndicatorType) -> EnrichmentResult:
        data = {
            "open_ports": [80, 443],
            "os": "Linux",
            "org": "Example Org",
            "vulns": [],
            "hostnames": [],
        }
        return EnrichmentResult(
            source=self.name(),
            status=EnrichmentStatus.COMPLETED,
            data=data,
            response_time_ms=320,
        )


# ---------------------------------------------------------------------------
# Indicator Validator
# ---------------------------------------------------------------------------

class IndicatorValidator:
    """Validate and detect indicator types."""

    PATTERNS: Dict[IndicatorType, re.Pattern] = {
        IndicatorType.IPV4: re.compile(
            r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
        ),
        IndicatorType.DOMAIN: re.compile(
            r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
        ),
        IndicatorType.MD5: re.compile(r"^[a-fA-F0-9]{32}$"),
        IndicatorType.SHA1: re.compile(r"^[a-fA-F0-9]{40}$"),
        IndicatorType.SHA256: re.compile(r"^[a-fA-F0-9]{64}$"),
        IndicatorType.CVE: re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE),
        IndicatorType.EMAIL: re.compile(
            r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        ),
    }

    def detect_type(self, value: str) -> IndicatorType:
        value = value.strip()
        for itype, pattern in self.PATTERNS.items():
            if pattern.match(value):
                return itype
        if value.startswith("http://") or value.startswith("https://"):
            return IndicatorType.URL
        raise ValueError(f"Unable to detect indicator type for: {value}")

    def validate(self, indicator_type: IndicatorType, value: str) -> bool:
        pattern = self.PATTERNS.get(indicator_type)
        if pattern is None:
            return True
        return bool(pattern.match(value.strip()))

    def fingerprint(self, indicator_type: IndicatorType, value: str) -> str:
        raw = f"{indicator_type.value}:{value.lower().strip()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# IOC Analyzer
# ---------------------------------------------------------------------------

class IOCAnalyzer:
    """Main analyzer for IOC enrichment and analysis."""

    def __init__(
        self,
        enrichment_sources: Optional[List[EnrichmentSource]] = None,
        confidence_threshold: int = 50,
        max_concurrent: int = 10,
    ) -> None:
        self.enrichment_sources = enrichment_sources or []
        self.confidence_threshold = confidence_threshold
        self.max_concurrent = max_concurrent
        self.validator = IndicatorValidator()
        self._providers: Dict[str, EnrichmentProvider] = {}
        self._cache: Dict[str, AnalysisResult] = {}
        self._register_default_providers()

    def _register_default_providers(self) -> None:
        self._providers["virustotal"] = VirusTotalProvider()
        self._providers["abuseipdb"] = AbuseIPDBProvider()
        self._providers["shodan"] = ShodanProvider()

    def register_provider(self, provider: EnrichmentProvider) -> None:
        self._providers[provider.name()] = provider

    def analyze(self, value: str, force_refresh: bool = False) -> AnalysisResult:
        indicator_type = self.validator.detect_type(value)
        fingerprint = self.validator.fingerprint(indicator_type, value)

        if not force_refresh and fingerprint in self._cache:
            logger.debug("Cache hit for indicator: %s", value)
            return self._cache[fingerprint]

        start_time = datetime.utcnow()

        result = AnalysisResult(
            indicator_id=fingerprint,
            value=value,
            indicator_type=indicator_type,
        )

        # Enrich from each source
        for source in self.enrichment_sources:
            provider = self._providers.get(source.name)
            if provider is None or not source.enabled:
                continue
            try:
                enrichment = provider.enrich(value, indicator_type)
                result.enrichment_results.append(enrichment)
                if enrichment.is_successful:
                    result.enrichment_count += 1
                    self._apply_enrichment_data(result, enrichment)
            except Exception as e:
                logger.warning("Enrichment failed for %s from %s: %s", value, source.name, e)
                result.enrichment_results.append(EnrichmentResult(
                    source=source.name,
                    status=EnrichmentStatus.FAILED,
                    error=str(e),
                ))

        # Calculate confidence
        result.confidence_score = self._calculate_confidence(result)
        result.false_positive_rate = self._estimate_false_positive(result)

        elapsed = (datetime.utcnow() - start_time).total_seconds() * 1000
        result.analysis_time_ms = int(elapsed)

        self._cache[fingerprint] = result
        return result

    def _apply_enrichment_data(self, result: AnalysisResult, enrichment: EnrichmentResult) -> None:
        data = enrichment.data
        if enrichment.source == "abuseipdb":
            score = data.get("abuse_confidence_score", 0)
            if score > 50:
                result.tags.append("abuse-reported")
            geo = GeoLocation(country_code=data.get("country_code", ""))
            result.geo_location = geo
            result.asn_info = ASNInfo(
                asn=0,
                isp=data.get("isp", ""),
                organization=data.get("org", ""),
            )
        elif enrichment.source == "virustotal":
            detection = data.get("detection_ratio", "0/0")
            if detection != "0/0":
                result.tags.append("vt-detected")
        elif enrichment.source == "shodan":
            ports = data.get("open_ports", [])
            if ports:
                result.tags.append(f"open-ports:{','.join(map(str, ports[:5]))}")

    def _calculate_confidence(self, result: AnalysisResult) -> int:
        base = 30
        enrichment_bonus = min(result.enrichment_count * 10, 30)
        tag_bonus = min(len(result.tags) * 5, 20)
        return min(base + enrichment_bonus + tag_bonus, 100)

    def _estimate_false_positive(self, result: AnalysisResult) -> float:
        fp_score = 0.2  # Base false positive rate
        if "abuse-reported" in result.tags:
            fp_score -= 0.1
        if result.enrichment_count >= 2:
            fp_score -= 0.05
        return max(0.0, min(1.0, fp_score))

    def analyze_batch(self, values: List[str]) -> List[AnalysisResult]:
        results = []
        for value in values:
            try:
                result = self.analyze(value)
                results.append(result)
            except ValueError as e:
                logger.warning("Skipping invalid indicator %s: %s", value, e)
        return results

    def get_cache_stats(self) -> Dict[str, Any]:
        return {
            "cached_indicators": len(self._cache),
            "enrichment_sources": len(self.enrichment_sources),
        }


# ---------------------------------------------------------------------------
# Correlation Engine
# ---------------------------------------------------------------------------

class CorrelationEngine:
    """Engine for correlating indicators across datasets."""

    def __init__(self, time_window: TimeWindow = TimeWindow.DAYS_30) -> None:
        self.time_window = time_window
        self._datasets: Dict[str, List[AnalysisResult]] = {}
        self._correlations: List[CorrelationGroup] = []

    def load_dataset(self, name: str, indicators: List[AnalysisResult]) -> None:
        self._datasets[name] = indicators
        logger.info("Loaded dataset '%s' with %d indicators", name, len(indicators))

    def find_overlaps(self) -> List[CorrelationGroup]:
        self._correlations.clear()
        self._find_shared_infrastructure()
        self._find_temporal_clusters()
        return self._correlations

    def _find_shared_infrastructure(self) -> None:
        all_indicators = []
        for dataset_name, indicators in self._datasets.items():
            for ind in indicators:
                all_indicators.append((dataset_name, ind))

        # Group by value for exact matches
        value_groups: Dict[str, List[Tuple[str, AnalysisResult]]] = defaultdict(list)
        for dataset_name, ind in all_indicators:
            value_groups[ind.value.lower()].append((dataset_name, ind))

        for value, group in value_groups.items():
            datasets = list(set(dn for dn, _ in group))
            if len(datasets) > 1:
                corr = CorrelationGroup(
                    indicators=[ind for _, ind in group],
                    correlation_type=CorrelationType.SHARED_INFRASTRUCTURE,
                    correlation_confidence=90,
                    datasets=datasets,
                    description=f"Shared indicator: {value}",
                )
                self._correlations.append(corr)

    def _find_temporal_clusters(self) -> None:
        all_with_dates = []
        for dataset_name, indicators in self._datasets.items():
            for ind in indicators:
                if ind.first_seen:
                    all_with_dates.append((dataset_name, ind))

        # Sort by first_seen
        all_with_dates.sort(key=lambda x: x[1].first_seen or datetime.min)

        window = timedelta(days=self.time_window.value)
        i = 0
        while i < len(all_with_dates):
            cluster = [all_with_dates[i]]
            j = i + 1
            while j < len(all_with_dates):
                if (all_with_dates[j][1].first_seen - all_with_dates[i][1].first_seen) <= window:
                    cluster.append(all_with_dates[j])
                j += 1

            if len(cluster) >= 3:
                datasets = list(set(dn for dn, _ in cluster))
                if len(datasets) > 1:
                    corr = CorrelationGroup(
                        indicators=[ind for _, ind in cluster],
                        correlation_type=CorrelationType.TEMPORAL_PROXIMITY,
                        correlation_confidence=70,
                        datasets=datasets,
                        first_seen=cluster[0][1].first_seen,
                        last_seen=cluster[-1][1].last_seen,
                        description=f"Temporal cluster of {len(cluster)} indicators",
                    )
                    self._correlations.append(corr)
            i += 1


# ---------------------------------------------------------------------------
# False Positive Scorer
# ---------------------------------------------------------------------------

class FalsePositiveScorer:
    """Heuristic false positive scoring for indicators."""

    def __init__(self) -> None:
        self._known_fp_indicators: Set[str] = set()
        self._weight_config = {
            "abuse_reports": 0.3,
            "detection_ratio": 0.25,
            "enrichment_count": 0.2,
            "sighting_count": 0.15,
            "age_factor": 0.1,
        }

    def score(self, analysis: AnalysisResult) -> float:
        fp_score = 0.0

        # Check against known FP list
        if analysis.value in self._known_fp_indicators:
            return 0.9

        # Abuse reports reduce FP likelihood
        if "abuse-reported" in analysis.tags:
            fp_score -= 0.2

        # Multiple enrichment confirmations reduce FP
        if analysis.enrichment_count >= 3:
            fp_score -= 0.15
        elif analysis.enrichment_count == 0:
            fp_score += 0.3

        # High confidence reduces FP
        if analysis.confidence_score >= 80:
            fp_score -= 0.1
        elif analysis.confidence_score < 30:
            fp_score += 0.2

        # Normalize to [0, 1]
        return max(0.0, min(1.0, 0.5 + fp_score))

    def add_known_false_positive(self, indicator_value: str) -> None:
        self._known_fp_indicators.add(indicator_value)

    def is_known_false_positive(self, indicator_value: str) -> bool:
        return indicator_value in self._known_fp_indicators


# ---------------------------------------------------------------------------
# Lifecycle Manager
# ---------------------------------------------------------------------------

class LifecycleManager:
    """Manages the lifecycle of indicators."""

    def __init__(self, policy: Optional[LifecyclePolicy] = None) -> None:
        self.policy = policy or LifecyclePolicy()
        self._statuses: Dict[str, LifecycleStatus] = {}

    def register(self, indicator_id: str, confidence: int = 50) -> LifecycleStatus:
        ttl_days = (
            self.policy.high_confidence_ttl_days
            if confidence >= 80
            else self.policy.default_ttl_days
        )
        status = LifecycleStatus(
            state=LifecycleState.NEW,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=ttl_days),
        )
        self._statuses[indicator_id] = status
        return status

    def get_status(self, indicator_id: str) -> Optional[LifecycleStatus]:
        return self._statuses.get(indicator_id)

    def activate(self, indicator_id: str) -> None:
        status = self._statuses.get(indicator_id)
        if status and status.state == LifecycleState.NEW:
            status.state = LifecycleState.ACTIVE
            status.last_updated = datetime.utcnow()

    def retire(self, indicator_id: str) -> None:
        status = self._statuses.get(indicator_id)
        if status:
            status.state = LifecycleState.RETIRED
            status.retired_at = datetime.utcnow()
            status.last_updated = datetime.utcnow()

    def archive(self, indicator_id: str) -> None:
        status = self._statuses.get(indicator_id)
        if status:
            status.state = LifecycleState.ARCHIVED
            status.archived_at = datetime.utcnow()
            status.last_updated = datetime.utcnow()

    def update_states(self) -> int:
        updated = 0
        now = datetime.utcnow()
        for indicator_id, status in self._statuses.items():
            if status.state in (LifecycleState.RETIRED, LifecycleState.ARCHIVED):
                continue
            if status.expires_at and now > status.expires_at:
                status.state = LifecycleState.EXPIRED
                status.last_updated = now
                updated += 1
            elif status.state == LifecycleState.ACTIVE and status.expires_at:
                remaining = (status.expires_at - now).days
                if remaining <= 30:
                    status.state = LifecycleState.AGING
                    status.last_updated = now
                    updated += 1
        return updated

    def purge_expired(self) -> int:
        expired_ids = [
            iid for iid, status in self._statuses.items()
            if status.state == LifecycleState.EXPIRED
        ]
        for iid in expired_ids:
            self.archive(iid)
        return len(expired_ids)

    def get_statistics(self) -> Dict[str, Any]:
        state_counts = defaultdict(int)
        for status in self._statuses.values():
            state_counts[status.state.value] += 1
        return {
            "total": len(self._statuses),
            "by_state": dict(state_counts),
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the IOC analysis module."""
    print("=" * 60)
    print("  IOC Analysis Module — Demo")
    print("=" * 60)

    # Initialize analyzer
    analyzer = IOCAnalyzer(
        enrichment_sources=[
            EnrichmentSource(name="virustotal", api_key="demo-vt-key"),
            EnrichmentSource(name="abuseipdb", api_key="demo-abuse-key"),
            EnrichmentSource(name="shodan", api_key="demo-shodan-key"),
        ]
    )

    # Analyze single indicator
    result = analyzer.analyze("198.51.100.42")
    print(f"\n[+] Single Indicator Analysis:")
    print(f"    Value: {result.value}")
    print(f"    Type: {result.indicator_type.value}")
    print(f"    Confidence: {result.confidence_score}%")
    print(f"    FP Rate: {result.false_positive_rate:.1%}")
    print(f"    Enrichment Sources: {result.enrichment_count}")
    print(f"    Tags: {result.tags}")
    print(f"    Analysis Time: {result.analysis_time_ms}ms")

    # Batch analysis
    batch_values = [
        "evil-c2.example.com",
        "https://malware.example.com/payload.exe",
        "d41d8cd98f00b204e9800998ecf8427e",
    ]
    batch_results = analyzer.analyze_batch(batch_values)
    print(f"\n[+] Batch Analysis: {len(batch_results)} indicators processed")

    # Correlation engine
    correlator = CorrelationEngine(time_window=TimeWindow.DAYS_30)
    correlator.load_dataset("dataset_a", [result])
    correlator.load_dataset("dataset_b", batch_results)
    overlaps = correlator.find_overlaps()
    print(f"\n[+] Correlation: found {len(overlaps)} groups")

    # False positive scorer
    fp_scorer = FalsePositiveScorer()
    fp_score = fp_scorer.score(result)
    print(f"\n[+] False Positive Score: {fp_score:.2f}")

    # Lifecycle manager
    lifecycle = LifecycleManager(
        policy=LifecyclePolicy(default_ttl_days=90, high_confidence_ttl_days=180)
    )
    lifecycle.register("ind-001", confidence=85)
    lifecycle.activate("ind-001")
    status = lifecycle.get_status("ind-001")
    print(f"\n[+] Lifecycle Status: {status.state.value if status else 'N/A'}")
    print(f"    Expires: {status.expires_at.strftime('%Y-%m-%d') if status else 'N/A'}")

    # Cache stats
    cache_stats = analyzer.get_cache_stats()
    print(f"\n[+] Cache Stats: {cache_stats}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
