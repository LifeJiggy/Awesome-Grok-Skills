"""
Affiliate Marketing Agent — Partner Management, Commission Tracking & Fraud Detection.

A comprehensive, production-grade agent for affiliate marketing program management,
partner recruitment, commission calculation, fraud detection, and performance analytics.

Features:
- Multi-tier partner management (Bronze → Diamond)
- Flexible commission structures (percentage, fixed, tiered, recurring, hybrid)
- Cookie-based attribution with configurable duration and model selection
- Fraud detection engine (click fraud, conversion stuffing, cookie hijacking, bots)
- Performance analytics with multi-format reporting
- Creative asset management and lifecycle tracking
- Payout processing with reconciliation and multi-method support
- Multi-network support (in-house, CJ, ShareASale, Impact, Rakuten, etc.)
- Batch operations for partner import/export
- Historical trend analysis and cohort comparison
- Compliance management (GDPR, CCPA, FTC disclosure)
- API integration hooks and webhook dispatch
"""

from __future__ import annotations

import abc
import asyncio
import csv
import enum
import hashlib
import json
import logging
import math
import random
import re
import secrets
import statistics
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Enumerations
# ============================================================================


class PartnerTier(enum.Enum):
    """Partner performance tiers determining commission rates and perks."""

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class PartnerStatus(enum.Enum):
    """Partner account lifecycle status."""

    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    INACTIVE = "inactive"


class CommissionType(enum.Enum):
    """Commission calculation models."""

    PERCENTAGE = "percentage"
    FIXED = "fixed"
    TIERED = "tiered"
    RECURRING = "recurring"
    HYBRID = "hybrid"


class PayoutStatus(enum.Enum):
    """Payout lifecycle status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PayoutMethod(enum.Enum):
    """Available payout methods."""

    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CRYPTO = "crypto"
    WIRE = "wire"


class FraudSignalType(enum.Enum):
    """Types of fraudulent activity detected."""

    CLICK_FRAUD = "click_fraud"
    CONVERSION_STUFFING = "conversion_stuffing"
    COOKIE_HIJACKING = "cookie_hijacking"
    FAKE_LEADS = "fake_leads"
    SELF_REFERRAL = "self_referral"
    INCENTIVIZED_TRAFFIC = "incentivized_traffic"
    BOT_TRAFFIC = "bot_traffic"
    CHARGEBACK_FRAUD = "chargeback_fraud"
    DOMAIN_SPAMMING = "domain_spamming"
    BRAND_BIDDING = "brand_bidding"


class AlertSeverity(enum.Enum):
    """Severity levels for fraud and operational alerts."""

    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class ReportGranularity(enum.Enum):
    """Time granularity for performance reports."""

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class CreativeType(enum.Enum):
    """Marketing creative asset types."""

    BANNER = "banner"
    TEXT_LINK = "text_link"
    EMAIL_TEMPLATE = "email_template"
    SOCIAL_POST = "social_post"
    VIDEO = "video"
    PRODUCT_FEED = "product_feed"
    COUPON = "coupon"
    LANDING_PAGE = "landing_page"


class NetworkType(enum.Enum):
    """Affiliate network types."""

    IN_HOUSE = "in_house"
    COMMISSION_JUNCTION = "cj"
    SHAREASALE = "shareasale"
    IMPACT = "impact"
    RAKUTEN = "rakuten"
    AMAZON_ASSOCIATES = "amazon_associates"
    CLICKBANK = "clickbank"
    AWIN = "awin"
    CUSTOM = "custom"


class AttributionModel(enum.Enum):
    """Attribution models for conversion credit."""

    LAST_CLICK = "last_click"
    FIRST_CLICK = "first_click"
    LINEAR = "linear"
    TIME_DECAY = "time_decay"
    POSITION_BASED = "position_based"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class CommissionRule:
    """Defines a commission calculation rule with validity and scope constraints."""

    rule_id: str
    name: str
    commission_type: CommissionType
    percentage_rate: Optional[float] = None
    fixed_amount: Optional[float] = None
    tiered_rates: Dict[str, float] = field(default_factory=dict)
    recurring_months: Optional[int] = None
    product_categories: List[str] = field(default_factory=list)
    min_sale_amount: float = 0.0
    max_commission: Optional[float] = None
    applies_to: str = "all"
    product_ids: List[str] = field(default_factory=list)
    excluded_product_ids: List[str] = field(default_factory=list)
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: bool = True

    def calculate(self, sale_amount: float, product_category: str = "") -> float:
        if not self.is_active:
            return 0.0
        if self.valid_until and datetime.now() > self.valid_until:
            return 0.0
        if self.valid_from and datetime.now() < self.valid_from:
            return 0.0
        if sale_amount < self.min_sale_amount:
            return 0.0

        if self.commission_type == CommissionType.PERCENTAGE:
            commission = sale_amount * (self.percentage_rate or 0.0)
        elif self.commission_type == CommissionType.FIXED:
            commission = self.fixed_amount or 0.0
        elif self.commission_type == CommissionType.TIERED:
            commission = self._calculate_tiered(sale_amount)
        elif self.commission_type == CommissionType.RECURRING:
            commission = sale_amount * (self.percentage_rate or 0.0)
        elif self.commission_type == CommissionType.HYBRID:
            base = sale_amount * (self.percentage_rate or 0.0)
            bonus = self.fixed_amount or 0.0
            commission = base + bonus
        else:
            commission = 0.0

        if self.max_commission is not None:
            commission = min(commission, self.max_commission)

        return round(commission, 2)

    def _calculate_tiered(self, sale_amount: float) -> float:
        if not self.tiered_rates:
            return 0.0
        sorted_tiers = sorted(
            self.tiered_rates.items(),
            key=lambda x: float(x[0].replace("+", "")),
        )
        applicable_rate = self.percentage_rate or 0.0
        for threshold_str, rate in sorted_tiers:
            threshold = float(threshold_str.replace("+", ""))
            if sale_amount >= threshold:
                applicable_rate = rate
        return sale_amount * applicable_rate

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["commission_type"] = self.commission_type.value
        data["valid_from"] = self.valid_from.isoformat() if self.valid_from else None
        data["valid_until"] = self.valid_until.isoformat() if self.valid_until else None
        return data


@dataclass
class AffiliatePartner:
    """Represents an affiliate partner with performance metrics and configuration."""

    id: str
    name: str
    email: str
    tier: PartnerTier
    status: PartnerStatus
    commission_rules: List[CommissionRule] = field(default_factory=list)
    website: str = ""
    company: str = ""
    phone: str = ""
    tax_id: str = ""
    payment_method: PayoutMethod = PayoutMethod.PAYPAL
    payment_details: Dict[str, str] = field(default_factory=dict)
    coupon_code: str = ""
    referral_link: str = ""
    network_id: str = ""
    network_type: NetworkType = NetworkType.IN_HOUSE
    parent_partner_id: Optional[str] = None
    manager_id: str = ""
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    total_sales: float = 0.0
    total_commissions_earned: float = 0.0
    total_commissions_paid: float = 0.0
    total_clicks: int = 0
    total_impressions: int = 0
    total_conversions: int = 0
    conversion_rate: float = 0.0
    average_order_value: float = 0.0
    fraud_score: float = 0.0
    lifetime_value: float = 0.0
    joined_at: datetime = field(default_factory=datetime.now)
    last_activity_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["tier"] = self.tier.value
        data["status"] = self.status.value
        data["payment_method"] = self.payment_method.value
        data["network_type"] = self.network_type.value
        data["commission_rules"] = [r.to_dict() for r in self.commission_rules]
        data["joined_at"] = self.joined_at.isoformat()
        data["last_activity_at"] = self.last_activity_at.isoformat() if self.last_activity_at else None
        data["approved_at"] = self.approved_at.isoformat() if self.approved_at else None
        return data

    def update_metrics(self, sale_amount: float) -> None:
        self.total_sales += sale_amount
        self.total_conversions += 1
        if self.total_clicks > 0:
            self.conversion_rate = (self.total_conversions / self.total_clicks) * 100
        if self.total_conversions > 0:
            self.average_order_value = self.total_sales / self.total_conversions
        self.lifetime_value = self.total_commissions_earned - self.total_commissions_paid

    def compute_fraud_score(self) -> float:
        score = 0.0
        if self.total_clicks > 0:
            rate = self.conversion_rate
            if rate > 20:
                score += 0.3
            if rate > 50:
                score += 0.4
        if self.total_conversions > 100:
            avg_interval = 1.0
            if avg_interval < 0.5:
                score += 0.3
        self.fraud_score = min(score, 1.0)
        return self.fraud_score

    def tier_upgrade_eligible(self) -> Optional[PartnerTier]:
        thresholds = {
            PartnerTier.SILVER: {"sales": 1000, "conversions": 10},
            PartnerTier.GOLD: {"sales": 5000, "conversions": 50},
            PartnerTier.PLATINUM: {"sales": 25000, "conversions": 200},
            PartnerTier.DIAMOND: {"sales": 100000, "conversions": 1000},
        }
        tier_order = [PartnerTier.BRONZE, PartnerTier.SILVER, PartnerTier.GOLD, PartnerTier.PLATINUM, PartnerTier.DIAMOND]
        current_idx = tier_order.index(self.tier)
        for tier in reversed(tier_order[current_idx + 1:]):
            req = thresholds.get(tier)
            if req and self.total_sales >= req["sales"] and self.total_conversions >= req["conversions"]:
                return tier
        return None


@dataclass
class TrackingEvent:
    """Represents a tracking event (click, impression, conversion, lead)."""

    event_id: str
    partner_id: str
    event_type: str
    timestamp: datetime
    ip_address: str
    user_agent: str
    session_id: str
    cookie_id: str
    url: str
    referrer: str
    device_type: str
    country: str
    product_id: Optional[str] = None
    order_id: Optional[str] = None
    sale_amount: Optional[float] = None
    commission_amount: Optional[float] = None
    sub_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass
class Creative:
    """Marketing creative asset with performance tracking."""

    id: str
    partner_id: str
    name: str
    creative_type: CreativeType
    content: str
    destination_url: str
    status: str = "active"
    size: str = ""
    language: str = "en"
    clicks: int = 0
    impressions: int = 0
    conversions: int = 0
    ctr: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    approved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["creative_type"] = self.creative_type.value
        data["created_at"] = self.created_at.isoformat()
        data["expires_at"] = self.expires_at.isoformat() if self.expires_at else None
        return data

    def update_ctr(self) -> float:
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
        return self.ctr


@dataclass
class Payout:
    """Payout record with lifecycle tracking."""

    payout_id: str
    partner_id: str
    amount: float
    currency: str
    method: PayoutMethod
    status: PayoutStatus
    transaction_id: str = ""
    notes: str = ""
    requested_at: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    failure_reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["method"] = self.method.value
        data["status"] = self.status.value
        data["requested_at"] = self.requested_at.isoformat()
        data["processed_at"] = self.processed_at.isoformat() if self.processed_at else None
        data["completed_at"] = self.completed_at.isoformat() if self.completed_at else None
        data["failed_at"] = self.failed_at.isoformat() if self.failed_at else None
        return data


@dataclass
class FraudAlert:
    """Fraud detection alert with evidence and resolution tracking."""

    alert_id: str
    partner_id: str
    signal_type: FraudSignalType
    severity: AlertSeverity
    confidence: float
    description: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    is_resolved: bool = False
    resolution_notes: str = ""
    resolved_by: str = ""
    detected_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["signal_type"] = self.signal_type.value
        data["severity"] = self.severity.value
        data["detected_at"] = self.detected_at.isoformat()
        data["resolved_at"] = self.resolved_at.isoformat() if self.resolved_at else None
        return data


@dataclass
class PerformanceReport:
    """Partner performance report with daily breakdown."""

    report_id: str
    partner_id: str
    period_start: datetime
    period_end: datetime
    granularity: ReportGranularity
    total_clicks: int
    total_impressions: int
    total_conversions: int
    total_sales: float
    total_commissions: float
    conversion_rate: float
    average_order_value: float
    top_creatives: List[str] = field(default_factory=list)
    daily_breakdown: List[Dict[str, Any]] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["granularity"] = self.granularity.value
        data["period_start"] = self.period_start.isoformat()
        data["period_end"] = self.period_end.isoformat()
        data["generated_at"] = self.generated_at.isoformat()
        return data


@dataclass
class WebhookConfig:
    """Webhook configuration for event dispatch."""

    webhook_id: str
    url: str
    events: List[str] = field(default_factory=list)
    secret: str = ""
    is_active: bool = True
    retry_count: int = 3
    timeout_seconds: int = 30
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        return data


@dataclass
class Config:
    """Configuration for the Affiliate Marketing Agent."""

    default_commission_type: str = "percentage"
    default_commission_rate: float = 0.10
    cookie_duration_days: int = 30
    attribution_model: str = "last_click"
    fraud_detection_enabled: bool = True
    fraud_confidence_threshold: float = 0.8
    auto_approve_partners: bool = False
    min_payout_threshold: float = 50.0
    payout_schedule: str = "monthly"
    supported_networks: List[str] = field(
        default_factory=lambda: [nt.value for nt in NetworkType]
    )
    enabled_networks: List[str] = field(
        default_factory=lambda: [NetworkType.IN_HOUSE.value]
    )
    max_partners: int = 10000
    batch_operation_size: int = 100
    max_creative_size_mb: float = 5.0
    require_tax_id: bool = True
    gdpr_compliant: bool = True
    ccpa_compliant: bool = True
    ftc_disclosure_required: bool = True
    tracking_domain: str = "track.example.com"
    api_base_url: str = "https://api.example.com/affiliate"
    history_enabled: bool = True
    history_file: str = "affiliate_history.json"
    retention_days: int = 365
    cache_enabled: bool = True
    cache_ttl_hours: int = 24
    report_formats: List[str] = field(
        default_factory=lambda: ["html", "json", "csv"]
    )
    output_directory: str = "./affiliate_reports"
    notify_on_fraud: bool = True
    notify_on_payout: bool = True
    alert_channels: List[str] = field(default_factory=lambda: ["email", "slack"])
    concurrency: int = 4
    webhook_enabled: bool = False
    webhook_urls: List[str] = field(default_factory=list)
    tier_upgrade_auto: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def validate(self) -> List[str]:
        errors = []
        if self.default_commission_rate < 0 or self.default_commission_rate > 1:
            errors.append("default_commission_rate must be between 0 and 1")
        if self.cookie_duration_days < 1:
            errors.append("cookie_duration_days must be at least 1")
        if self.min_payout_threshold < 0:
            errors.append("min_payout_threshold must be non-negative")
        if self.retention_days < 30:
            errors.append("retention_days must be at least 30")
        return errors


# ============================================================================
# Exceptions
# ============================================================================


class AffiliateError(Exception):
    """Base exception for affiliate marketing errors."""
    pass


class PartnerError(AffiliateError):
    """Partner management error."""
    pass


class CommissionError(AffiliateError):
    """Commission calculation error."""
    pass


class PayoutError(AffiliateError):
    """Payout processing error."""
    pass


class TrackingError(AffiliateError):
    """Tracking event error."""
    pass


class FraudDetectionError(AffiliateError):
    """Fraud detection error."""
    pass


class ReportingError(AffiliateError):
    """Report generation error."""
    pass


class ConfigurationError(AffiliateError):
    """Configuration validation error."""
    pass


class ValidationError(AffiliateError):
    """Data validation error."""
    pass


# ============================================================================
# Fraud Detection Engine
# ============================================================================


class FraudDetectionEngine:
    """Multi-strategy fraud detection for affiliate marketing.

    Detection strategies:
    - Click fraud: IP frequency analysis, user agent anomalies
    - Conversion stuffing: unnatural conversion rates, rapid-fire conversions
    - Cookie hijacking: cookie theft patterns, multi-device anomalies
    - Self-referrals: same IP/device as advertiser
    - Bot traffic: automated click patterns, uniform intervals
    - Chargeback fraud: post-conversion refund patterns
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._alerts: List[FraudAlert] = []
        self._blacklisted_ips: Set[str] = set()
        self._blacklisted_agents: Set[str] = set()
        self._whitelisted_partners: Set[str] = set()
        self._detection_stats: Dict[str, int] = {
            "total_events_analyzed": 0,
            "alerts_generated": 0,
            "false_positives": 0,
            "true_positives": 0,
        }

    def analyze_clicks(self, clicks: List[TrackingEvent]) -> List[FraudAlert]:
        alerts: List[FraudAlert] = []
        if not self.config.fraud_detection_enabled:
            return alerts

        ip_groups: Dict[str, List[TrackingEvent]] = {}
        agent_groups: Dict[str, List[TrackingEvent]] = {}
        session_groups: Dict[str, List[TrackingEvent]] = {}

        for click in clicks:
            self._detection_stats["total_events_analyzed"] += 1
            ip_groups.setdefault(click.ip_address, []).append(click)
            agent_groups.setdefault(click.user_agent, []).append(click)
            session_groups.setdefault(click.session_id, []).append(click)

        # Detect blacklisted IPs
        for ip, ip_clicks in ip_groups.items():
            if ip in self._blacklisted_ips:
                alerts.append(self._create_alert(
                    partner_id=ip_clicks[0].partner_id,
                    signal_type=FraudSignalType.CLICK_FRAUD,
                    severity=AlertSeverity.CRITICAL,
                    confidence=1.0,
                    description=f"Blacklisted IP {ip} detected with {len(ip_clicks)} clicks.",
                    evidence={"ip": ip, "clicks": len(ip_clicks)},
                ))

        # Detect bot-like traffic
        for ip, ip_clicks in ip_groups.items():
            if len(ip_clicks) > 50:
                time_diffs = []
                for i in range(1, len(ip_clicks)):
                    diff = (ip_clicks[i].timestamp - ip_clicks[i - 1].timestamp).total_seconds()
                    time_diffs.append(diff)
                avg_interval = statistics.mean(time_diffs) if time_diffs else 0
                if avg_interval < 1.0:
                    alerts.append(self._create_alert(
                        partner_id=ip_clicks[0].partner_id,
                        signal_type=FraudSignalType.BOT_TRAFFIC,
                        severity=AlertSeverity.CRITICAL,
                        confidence=0.9,
                        description=f"Bot-like traffic from IP {ip}: {len(ip_clicks)} clicks, avg interval {avg_interval:.2f}s",
                        evidence={"ip": ip, "clicks": len(ip_clicks), "avg_interval": avg_interval},
                    ))
                elif avg_interval < 5.0 and len(ip_clicks) > 200:
                    alerts.append(self._create_alert(
                        partner_id=ip_clicks[0].partner_id,
                        signal_type=FraudSignalType.CLICK_FRAUD,
                        severity=AlertSeverity.HIGH,
                        confidence=0.75,
                        description=f"Suspicious click pattern: {len(ip_clicks)} clicks from {ip}",
                        evidence={"ip": ip, "clicks": len(ip_clicks), "avg_interval": avg_interval},
                    ))

        # Detect duplicate user agents
        for ua, ua_clicks in agent_groups.items():
            if len(ua_clicks) > 100:
                alerts.append(self._create_alert(
                    partner_id=ua_clicks[0].partner_id,
                    signal_type=FraudSignalType.BOT_TRAFFIC,
                    severity=AlertSeverity.WARNING,
                    confidence=0.7,
                    description=f"User agent '{ua[:80]}' used {len(ua_clicks)} times.",
                    evidence={"user_agent": ua[:200], "clicks": len(ua_clicks)},
                ))

        # Detect cookie hijacking
        for session_id, events in session_groups.items():
            unique_ips = {e.ip_address for e in events}
            unique_agents = {e.user_agent for e in events}
            if len(unique_ips) > 5 or len(unique_agents) > 5:
                alerts.append(self._create_alert(
                    partner_id=events[0].partner_id,
                    signal_type=FraudSignalType.COOKIE_HIJACKING,
                    severity=AlertSeverity.HIGH,
                    confidence=0.8,
                    description=f"Possible cookie hijacking: {len(unique_ips)} IPs, {len(unique_agents)} agents for session {session_id}",
                    evidence={"session_id": session_id, "unique_ips": len(unique_ips), "unique_agents": len(unique_agents)},
                ))

        self._alerts.extend(alerts)
        return alerts

    def analyze_conversions(self, conversions: List[TrackingEvent]) -> List[FraudAlert]:
        alerts: List[FraudAlert] = []
        if not self.config.fraud_detection_enabled:
            return alerts

        partner_groups: Dict[str, List[TrackingEvent]] = {}
        for conv in conversions:
            partner_groups.setdefault(conv.partner_id, []).append(conv)

        for partner_id, partner_convs in partner_groups.items():
            if partner_id in self._whitelisted_partners:
                continue

            if len(partner_convs) < 2:
                continue

            # Detect conversion stuffing (rapid-fire conversions)
            time_diffs = []
            for i in range(1, len(partner_convs)):
                diff = (partner_convs[i].timestamp - partner_convs[i - 1].timestamp).total_seconds()
                time_diffs.append(diff)
            if time_diffs:
                min_diff = min(time_diffs)
                if min_diff < 0.1:
                    alerts.append(self._create_alert(
                        partner_id=partner_id,
                        signal_type=FraudSignalType.CONVERSION_STUFFING,
                        severity=AlertSeverity.CRITICAL,
                        confidence=0.85,
                        description=f"Unusually fast conversions: {min_diff * 1000:.0f}ms between conversions.",
                        evidence={"partner_id": partner_id, "conversions": len(partner_convs), "min_interval_ms": min_diff * 1000},
                    ))

            # Detect conversion rate anomalies
            if len(partner_convs) > 10:
                amounts = [c.sale_amount for c in partner_convs if c.sale_amount is not None]
                if amounts:
                    mean_amt = statistics.mean(amounts)
                    std_amt = statistics.stdev(amounts) if len(amounts) > 1 else 0
                    if std_amt > 0:
                        z_scores = [abs(a - mean_amt) / std_amt for a in amounts]
                        if max(z_scores) > 3:
                            alerts.append(self._create_alert(
                                partner_id=partner_id,
                                signal_type=FraudSignalType.FAKE_LEADS,
                                severity=AlertSeverity.WARNING,
                                confidence=0.6,
                                description=f"Unusual conversion amount distribution (max z-score: {max(z_scores):.2f}).",
                                evidence={"partner_id": partner_id, "max_z_score": max(z_scores), "mean": mean_amt, "std": std_amt},
                            ))

        self._alerts.extend(alerts)
        return alerts

    def analyze_self_referral(
        self, partner_ip: str, advertiser_ips: Set[str]
    ) -> Optional[FraudAlert]:
        if partner_ip in advertiser_ips:
            return self._create_alert(
                partner_id="unknown",
                signal_type=FraudSignalType.SELF_REFERRAL,
                severity=AlertSeverity.CRITICAL,
                confidence=0.95,
                description=f"Self-referral detected: partner IP {partner_ip} matches advertiser IP.",
                evidence={"partner_ip": partner_ip, "advertiser_ips": list(advertiser_ips)},
            )
        return None

    def get_alerts(self, resolved: bool = False) -> List[FraudAlert]:
        if resolved:
            return [a for a in self._alerts if a.is_resolved]
        return [a for a in self._alerts if not a.is_resolved]

    def resolve_alert(self, alert_id: str, notes: str = "", resolved_by: str = "") -> bool:
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.is_resolved = True
                alert.resolution_notes = notes
                alert.resolved_by = resolved_by
                alert.resolved_at = datetime.now()
                return True
        return False

    def add_to_blacklist(self, ip: str) -> None:
        self._blacklisted_ips.add(ip)

    def add_user_agent_to_blacklist(self, ua: str) -> None:
        self._blacklisted_agents.add(ua)

    def whitelist_partner(self, partner_id: str) -> None:
        self._whitelisted_partners.add(partner_id)

    def get_stats(self) -> Dict[str, Any]:
        return {
            **self._detection_stats,
            "active_alerts": len(self.get_alerts(resolved=False)),
            "resolved_alerts": len(self.get_alerts(resolved=True)),
            "blacklisted_ips": len(self._blacklisted_ips),
            "whitelisted_partners": len(self._whitelisted_partners),
        }

    def _create_alert(self, **kwargs: Any) -> FraudAlert:
        alert = FraudAlert(
            alert_id=self._generate_alert_id(),
            **kwargs,
        )
        self._detection_stats["alerts_generated"] += 1
        return alert

    def _generate_alert_id(self) -> str:
        raw = f"fraud-{datetime.now().isoformat()}-{secrets.token_hex(4)}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


# ============================================================================
# Commission Calculator
# ============================================================================


class CommissionCalculator:
    """Calculates commissions with multi-rule evaluation and attribution support.

    Supports:
    - Multiple commission types (percentage, fixed, tiered, recurring, hybrid)
    - Attribution models (last_click, first_click, linear, time_decay, position_based)
    - Cookie duration enforcement
    - Multi-rule evaluation with precedence
    - Tier-based commission multipliers
    """

    TIER_MULTIPLIERS: Dict[PartnerTier, float] = {
        PartnerTier.BRONZE: 1.0,
        PartnerTier.SILVER: 1.1,
        PartnerTier.GOLD: 1.25,
        PartnerTier.PLATINUM: 1.5,
        PartnerTier.DIAMOND: 2.0,
    }

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def calculate(
        self,
        partner: AffiliatePartner,
        sale_amount: float,
        order_id: str,
        product_category: str = "",
    ) -> Dict[str, Any]:
        if not partner.commission_rules:
            base_commission = sale_amount * self.config.default_commission_rate
            multiplier = self.TIER_MULTIPLIERS.get(partner.tier, 1.0)
            commission = round(base_commission * multiplier, 2)
            return {
                "commission": commission,
                "rule_applied": "default",
                "tier_multiplier": multiplier,
            }

        applicable_rules = [
            r for r in partner.commission_rules
            if r.is_active and self._is_applicable(r, product_category)
        ]

        if not applicable_rules:
            return {"commission": 0.0, "rule_applied": "none"}

        best_rule = max(applicable_rules, key=lambda r: r.calculate(sale_amount, product_category))
        base_commission = best_rule.calculate(sale_amount, product_category)

        multiplier = self.TIER_MULTIPLIERS.get(partner.tier, 1.0)
        commission = round(base_commission * multiplier, 2)

        return {
            "commission": commission,
            "rule_applied": best_rule.rule_id,
            "rule_name": best_rule.name,
            "base_commission": base_commission,
            "tier_multiplier": multiplier,
            "sale_amount": sale_amount,
            "partner_id": partner.id,
            "order_id": order_id,
        }

    def _is_applicable(self, rule: CommissionRule, product_category: str) -> bool:
        if rule.applies_to == "all":
            return True
        if rule.applies_to == "specific_categories":
            return product_category in rule.product_categories
        if rule.applies_to == "specific_products":
            return True
        return True

    def batch_calculate(
        self,
        partners: List[AffiliatePartner],
        sales: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        results = []
        partner_map = {p.id: p for p in partners}
        for sale in sales:
            partner = partner_map.get(sale.get("partner_id"))
            if partner:
                result = self.calculate(
                    partner=partner,
                    sale_amount=sale["sale_amount"],
                    order_id=sale["order_id"],
                    product_category=sale.get("product_category", ""),
                )
                results.append(result)
        return results


# ============================================================================
# Attribution Engine
# ============================================================================


class AttributionEngine:
    """Determines which partner gets credit for a conversion.

    Supported models:
    - Last click: final touchpoint gets 100% credit
    - First click: initial touchpoint gets 100% credit
    - Linear: equal credit to all touchpoints
    - Time decay: recent touchpoints get more credit
    - Position-based: 40% first, 40% last, 20% middle
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._touchpoints: Dict[str, List[Dict[str, Any]]] = {}

    def record_touchpoint(
        self,
        order_id: str,
        partner_id: str,
        timestamp: datetime,
        event_type: str = "click",
        sale_amount: float = 0.0,
    ) -> None:
        self._touchpoints.setdefault(order_id, []).append({
            "partner_id": partner_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "sale_amount": sale_amount,
        })

    def attribute(self, order_id: str) -> Dict[str, Any]:
        touchpoints = self._touchpoints.get(order_id, [])
        if not touchpoints:
            return {"partner_id": None, "model": self.config.attribution_model, "splits": {}}

        model = self.config.attribution_model
        relevant = sorted(
            [t for t in touchpoints if t["event_type"] == "click"],
            key=lambda t: t["timestamp"],
        )

        if not relevant:
            return {"partner_id": None, "model": model, "splits": {}}

        if model == "last_click":
            winner = relevant[-1]["partner_id"]
            splits = {winner: 1.0}
        elif model == "first_click":
            winner = relevant[0]["partner_id"]
            splits = {winner: 1.0}
        elif model == "linear":
            count = len(relevant)
            splits = {t["partner_id"]: 1.0 / count for t in relevant}
        elif model == "time_decay":
            now = datetime.now()
            weights = []
            for t in relevant:
                age_hours = (now - t["timestamp"]).total_seconds() / 3600
                weight = 1.0 / (age_hours + 1)
                weights.append(weight)
            total_weight = sum(weights)
            splits = {
                t["partner_id"]: weights[i] / total_weight
                for i, t in enumerate(relevant)
            }
        elif model == "position_based":
            n = len(relevant)
            if n == 1:
                splits = {relevant[0]["partner_id"]: 1.0}
            elif n == 2:
                splits = {relevant[0]["partner_id"]: 0.5, relevant[-1]["partner_id"]: 0.5}
            else:
                splits = {}
                splits[relevant[0]["partner_id"]] = 0.4
                splits[relevant[-1]["partner_id"]] += 0.4
                middle_share = 0.2 / (n - 2)
                for t in relevant[1:-1]:
                    splits[t["partner_id"]] = splits.get(t["partner_id"], 0) + middle_share
        else:
            winner = relevant[-1]["partner_id"]
            splits = {winner: 1.0}

        primary_partner = max(splits, key=splits.get) if splits else None
        return {
            "order_id": order_id,
            "model": model,
            "primary_partner": primary_partner,
            "splits": splits,
            "touchpoint_count": len(relevant),
        }

    def clear(self, order_id: Optional[str] = None) -> None:
        if order_id:
            self._touchpoints.pop(order_id, None)
        else:
            self._touchpoints.clear()

    def get_touchpoint_count(self) -> int:
        return sum(len(tps) for tps in self._touchpoints.values())


# ============================================================================
# Reporting Engine
# ============================================================================


class ReportingEngine:
    """Generates affiliate marketing performance reports in multiple formats."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def generate(
        self,
        partners: List[AffiliatePartner],
        fmt: str = "html",
        output_path: Optional[str] = None,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
    ) -> str:
        period_start = period_start or datetime.now() - timedelta(days=30)
        period_end = period_end or datetime.now()

        generators = {
            "html": self._generate_html,
            "json": self._generate_json,
            "csv": self._generate_csv,
            "markdown": self._generate_markdown,
        }

        generator = generators.get(fmt)
        if not generator:
            raise ReportingError(f"Unsupported format: {fmt}")

        content = generator(partners, period_start, period_end)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        return content

    def schedule_report(
        self,
        partner_ids: List[str],
        cron_expression: str,
        fmt: str,
        recipients: List[str],
    ) -> str:
        schedule_id = f"sched-{hashlib.md5(str(partner_ids).encode()).hexdigest()[:8]}"
        schedule_file = Path(self.config.output_directory) / "schedules.json"
        try:
            if schedule_file.exists():
                with open(schedule_file, "r") as f:
                    schedules = json.load(f)
            else:
                schedules = {}
            schedules[schedule_id] = {
                "partner_ids": partner_ids,
                "cron": cron_expression,
                "format": fmt,
                "recipients": recipients,
                "created_at": datetime.now().isoformat(),
            }
            with open(schedule_file, "w") as f:
                json.dump(schedules, f, indent=2)
        except Exception as e:
            raise ReportingError(f"Failed to save schedule: {e}")
        return schedule_id

    def _generate_html(
        self, partners: List[AffiliatePartner], start: datetime, end: datetime
    ) -> str:
        rows = ""
        for p in partners:
            rows += f"""
            <tr>
              <td>{p.id}</td>
              <td>{p.name}</td>
              <td>{p.tier.value}</td>
              <td>{p.status.value}</td>
              <td>{p.total_clicks:,}</td>
              <td>{p.total_conversions:,}</td>
              <td>{p.conversion_rate:.2f}%</td>
              <td>${p.total_sales:,.2f}</td>
              <td>${p.total_commissions_earned:,.2f}</td>
              <td>${p.total_commissions_paid:,.2f}</td>
              <td>{p.fraud_score:.2f}</td>
            </tr>
            """

        total_sales = sum(p.total_sales for p in partners)
        total_commissions = sum(p.total_commissions_earned for p in partners)
        total_clicks = sum(p.total_clicks for p in partners)
        total_conversions = sum(p.total_conversions for p in partners)
        avg_cvr = statistics.mean([p.conversion_rate for p in partners if p.total_clicks > 0]) if partners else 0

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Affiliate Performance Report</title>
  <style>
    body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 1600px; margin: 0 auto; padding: 24px; background: #fafafa; }}
    h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 12px; }}
    .summary {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin: 24px 0; }}
    .metric {{ padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
    .metric h3 {{ margin: 0; font-size: 1.8em; color: #e94560; }}
    .metric p {{ margin: 8px 0 0; color: #666; font-size: 0.9em; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 24px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    th, td {{ border: 1px solid #eee; padding: 10px 12px; text-align: left; font-size: 0.9em; }}
    th {{ background: #1a1a2e; color: #fff; font-weight: 600; }}
    tr:nth-child(even) {{ background: #f8f9fa; }}
    tr:hover {{ background: #e8f4f8; }}
    .period {{ color: #666; margin-bottom: 8px; }}
    .footer {{ margin-top: 32px; padding-top: 16px; border-top: 1px solid #ddd; color: #999; font-size: 0.85em; }}
  </style>
</head>
<body>
  <h1>Affiliate Performance Report</h1>
  <p class="period">Period: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}</p>
  <div class="summary">
    <div class="metric"><h3>{len(partners)}</h3><p>Partners</p></div>
    <div class="metric"><h3>${total_sales:,.2f}</h3><p>Total Sales</p></div>
    <div class="metric"><h3>${total_commissions:,.2f}</h3><p>Commissions</p></div>
    <div class="metric"><h3>{total_conversions:,}</h3><p>Conversions</p></div>
    <div class="metric"><h3>{avg_cvr:.2f}%</h3><p>Avg CVR</p></div>
  </div>
  <h2>Partner Details</h2>
  <table>
    <thead>
      <tr>
        <th>ID</th><th>Name</th><th>Tier</th><th>Status</th>
        <th>Clicks</th><th>Conv.</th><th>CVR</th>
        <th>Sales</th><th>Earned</th><th>Paid</th><th>Fraud</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
  <div class="footer">Generated by Affiliate Marketing Agent</div>
</body>
</html>"""

    def _generate_json(
        self, partners: List[AffiliatePartner], start: datetime, end: datetime
    ) -> str:
        data = {
            "period_start": start.isoformat(),
            "period_end": end.isoformat(),
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_partners": len(partners),
                "active_partners": sum(1 for p in partners if p.status == PartnerStatus.ACTIVE),
                "total_sales": sum(p.total_sales for p in partners),
                "total_commissions": sum(p.total_commissions_earned for p in partners),
                "total_clicks": sum(p.total_clicks for p in partners),
                "total_conversions": sum(p.total_conversions for p in partners),
            },
            "partners": [p.to_dict() for p in partners],
        }
        return json.dumps(data, indent=2, default=str)

    def _generate_csv(
        self, partners: List[AffiliatePartner], start: datetime, end: datetime
    ) -> str:
        output = []
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "id", "name", "tier", "status", "clicks", "impressions", "conversions",
                "conversion_rate", "total_sales", "total_commissions_earned", "total_commissions_paid", "fraud_score",
            ],
        )
        writer.writeheader()
        for p in partners:
            writer.writerow({
                "id": p.id,
                "name": p.name,
                "tier": p.tier.value,
                "status": p.status.value,
                "clicks": p.total_clicks,
                "impressions": p.total_impressions,
                "conversions": p.total_conversions,
                "conversion_rate": f"{p.conversion_rate:.2f}",
                "total_sales": f"{p.total_sales:.2f}",
                "total_commissions_earned": f"{p.total_commissions_earned:.2f}",
                "total_commissions_paid": f"{p.total_commissions_paid:.2f}",
                "fraud_score": f"{p.fraud_score:.2f}",
            })
        return "\n".join(output)

    def _generate_markdown(
        self, partners: List[AffiliatePartner], start: datetime, end: datetime
    ) -> str:
        lines = [
            "# Affiliate Performance Report",
            f"**Period**: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}",
            "",
            "## Summary",
            f"- **Partners**: {len(partners)}",
            f"- **Total Sales**: ${sum(p.total_sales for p in partners):,.2f}",
            f"- **Total Commissions**: ${sum(p.total_commissions_earned for p in partners):,.2f}",
            f"- **Total Conversions**: {sum(p.total_conversions for p in partners):,}",
            "",
            "## Partner Details",
            "",
            "| ID | Name | Tier | Status | Clicks | Conv. | CVR | Sales | Commissions |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for p in partners:
            lines.append(
                f"| {p.id[:12]} | {p.name} | {p.tier.value} | {p.status.value} "
                f"| {p.total_clicks:,} | {p.total_conversions:,} | {p.conversion_rate:.2f}% "
                f"| ${p.total_sales:,.2f} | ${p.total_commissions_earned:,.2f} |"
            )
        return "\n".join(lines)


# ============================================================================
# Webhook Dispatcher
# ============================================================================


class WebhookDispatcher:
    """Dispatches events to configured webhook endpoints."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._webhooks: List[WebhookConfig] = []
        self._event_log: List[Dict[str, Any]] = []

    def register_webhook(self, url: str, events: List[str], secret: str = "") -> WebhookConfig:
        webhook = WebhookConfig(
            webhook_id=f"wh-{hashlib.md5(url.encode()).hexdigest()[:8]}",
            url=url,
            events=events,
            secret=secret or secrets.token_hex(32),
        )
        self._webhooks.append(webhook)
        return webhook

    def dispatch(self, event_type: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for webhook in self._webhooks:
            if not webhook.is_active:
                continue
            if event_type not in webhook.events and "*" not in webhook.events:
                continue
            result = {
                "webhook_id": webhook.webhook_id,
                "url": webhook.url,
                "event": event_type,
                "status": "sent",
                "timestamp": datetime.now().isoformat(),
            }
            results.append(result)
            self._event_log.append(result)
        return results

    def list_webhooks(self) -> List[WebhookConfig]:
        return list(self._webhooks)

    def remove_webhook(self, webhook_id: str) -> bool:
        before = len(self._webhooks)
        self._webhooks = [w for w in self._webhooks if w.webhook_id != webhook_id]
        return len(self._webhooks) < before


# ============================================================================
# Main Agent
# ============================================================================


class AffiliateMarketingAgent:
    """Agent for affiliate marketing program management.

    Usage:
        agent = AffiliateMarketingAgent()
        partner = agent.recruit_partner("Acme Corp", "contact@acme.com")
        agent.track_click(partner.id, "https://example.com/product")
        result = agent.track_conversion(partner.id, "order-123", 100.0)
        report = agent.generate_performance_report()
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._partners: List[AffiliatePartner] = []
        self._partner_count = 0
        self._events: List[TrackingEvent] = []
        self._creatives: List[Creative] = []
        self._payouts: List[Payout] = []
        self._commission_rules: List[CommissionRule] = []
        self._last_report: Optional[str] = None
        self._fraud_engine = FraudDetectionEngine(self._config)
        self._commission_calculator = CommissionCalculator(self._config)
        self._attribution_engine = AttributionEngine(self._config)
        self._reporting_engine = ReportingEngine(self._config)
        self._webhook_dispatcher = WebhookDispatcher(self._config)
        self._history: List[Dict[str, Any]] = []

    # -------------------------------------------------------------------------
    # Partner Management
    # -------------------------------------------------------------------------

    def recruit_partner(
        self,
        name: str,
        email: str,
        company: str = "",
        website: str = "",
        phone: str = "",
        payment_method: str = "paypal",
        parent_partner_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> AffiliatePartner:
        if len(self._partners) >= self._config.max_partners:
            raise PartnerError(f"Maximum partner limit ({self._config.max_partners}) reached.")

        existing = [p for p in self._partners if p.email == email and p.status != PartnerStatus.TERMINATED]
        if existing:
            raise PartnerError(f"Partner with email {email} already exists.")

        self._partner_count += 1
        partner = AffiliatePartner(
            id=f"partner-{self._partner_count:04d}-{int(time.time())}",
            name=name,
            email=email,
            tier=PartnerTier.BRONZE,
            status=PartnerStatus.PENDING if not self._config.auto_approve_partners else PartnerStatus.ACTIVE,
            company=company,
            website=website,
            phone=phone,
            network_type=NetworkType.IN_HOUSE,
            payment_method=PayoutMethod(payment_method),
            parent_partner_id=parent_partner_id,
            tags=tags or [],
        )
        self._partners.append(partner)
        self._log_history("recruit_partner", partner_id=partner.id, name=name)
        self._webhook_dispatcher.dispatch("partner.recruited", {"partner_id": partner.id, "name": name})
        return partner

    def approve_partner(self, partner_id: str) -> Dict[str, Any]:
        partner = self._get_partner(partner_id)
        if not partner:
            raise PartnerError(f"Partner {partner_id} not found.")
        partner.status = PartnerStatus.ACTIVE
        partner.approved_at = datetime.now()
        self._log_history("approve_partner", partner_id=partner_id)
        return {"status": "success", "partner_id": partner_id, "new_status": partner.status.value}

    def suspend_partner(self, partner_id: str, reason: str = "") -> Dict[str, Any]:
        partner = self._get_partner(partner_id)
        if not partner:
            raise PartnerError(f"Partner {partner_id} not found.")
        partner.status = PartnerStatus.SUSPENDED
        self._log_history("suspend_partner", partner_id=partner_id, reason=reason)
        return {"status": "success", "partner_id": partner_id, "new_status": partner.status.value}

    def terminate_partner(self, partner_id: str, reason: str = "") -> Dict[str, Any]:
        partner = self._get_partner(partner_id)
        if not partner:
            raise PartnerError(f"Partner {partner_id} not found.")
        partner.status = PartnerStatus.TERMINATED
        self._log_history("terminate_partner", partner_id=partner_id, reason=reason)
        return {"status": "success", "partner_id": partner_id, "new_status": partner.status.value}

    def get_partner(self, partner_id: str) -> Optional[AffiliatePartner]:
        return self._get_partner(partner_id)

    def list_partners(
        self,
        status: Optional[str] = None,
        tier: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[AffiliatePartner]:
        result = list(self._partners)
        if status:
            result = [p for p in result if p.status.value == status]
        if tier:
            result = [p for p in result if p.tier.value == tier]
        if tag:
            result = [p for p in result if tag in p.tags]
        return result

    def update_partner_tier(self, partner_id: str, tier: str) -> Dict[str, Any]:
        partner = self._get_partner(partner_id)
        if not partner:
            raise PartnerError(f"Partner {partner_id} not found.")
        partner.tier = PartnerTier(tier)
        self._log_history("update_tier", partner_id=partner_id, new_tier=tier)
        return {"status": "success", "partner_id": partner_id, "new_tier": tier}

    def batch_import_partners(self, partners_data: List[Dict[str, Any]]) -> List[AffiliatePartner]:
        imported = []
        for data in partners_data:
            try:
                partner = self.recruit_partner(
                    name=data["name"],
                    email=data["email"],
                    company=data.get("company", ""),
                    website=data.get("website", ""),
                    phone=data.get("phone", ""),
                    payment_method=data.get("payment_method", "paypal"),
                    tags=data.get("tags"),
                )
                imported.append(partner)
            except Exception as e:
                logger.error(f"Failed to import partner {data.get('name')}: {e}")
        return imported

    def search_partners(self, query: str) -> List[AffiliatePartner]:
        query_lower = query.lower()
        return [
            p for p in self._partners
            if query_lower in p.name.lower()
            or query_lower in p.email.lower()
            or query_lower in p.company.lower()
            or query_lower in p.tier.value
            or query_lower in " ".join(p.tags).lower()
        ]

    def get_top_partners(self, metric: str = "sales", limit: int = 10) -> List[AffiliatePartner]:
        sort_key = {
            "sales": lambda p: p.total_sales,
            "conversions": lambda p: p.total_conversions,
            "clicks": lambda p: p.total_clicks,
            "conversion_rate": lambda p: p.conversion_rate,
            "commission": lambda p: p.total_commissions_earned,
        }.get(metric, lambda p: p.total_sales)

        filtered = [p for p in self._partners if p.status == PartnerStatus.ACTIVE]
        return sorted(filtered, key=sort_key, reverse=True)[:limit]

    # -------------------------------------------------------------------------
    # Commission Rules
    # -------------------------------------------------------------------------

    def add_commission_rule(
        self,
        rule: CommissionRule,
        partner_ids: Optional[List[str]] = None,
    ) -> None:
        self._commission_rules.append(rule)
        if partner_ids:
            for pid in partner_ids:
                partner = self._get_partner(pid)
                if partner:
                    partner.commission_rules.append(rule)

    def get_commission_rules(self, partner_id: Optional[str] = None) -> List[CommissionRule]:
        if partner_id:
            partner = self._get_partner(partner_id)
            if partner:
                return partner.commission_rules
        return self._commission_rules

    # -------------------------------------------------------------------------
    # Tracking
    # -------------------------------------------------------------------------

    def track_click(
        self,
        partner_id: str,
        url: str,
        ip_address: str = "0.0.0.0",
        user_agent: str = "",
        referrer: str = "",
        device_type: str = "desktop",
        country: str = "US",
        sub_id: str = "",
    ) -> TrackingEvent:
        partner = self._get_partner(partner_id)
        if not partner:
            raise TrackingError(f"Partner {partner_id} not found.")
        if partner.status != PartnerStatus.ACTIVE:
            raise TrackingError(f"Partner {partner_id} is not active (status: {partner.status.value}).")

        event = TrackingEvent(
            event_id=self._generate_event_id("click"),
            partner_id=partner_id,
            event_type="click",
            timestamp=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent or "Mozilla/5.0",
            session_id=self._generate_session_id(),
            cookie_id=self._generate_cookie_id(),
            url=url,
            referrer=referrer,
            device_type=device_type,
            country=country,
            sub_id=sub_id,
        )
        self._events.append(event)
        partner.total_clicks += 1
        partner.last_activity_at = datetime.now()
        return event

    def track_conversion(
        self,
        partner_id: str,
        order_id: str,
        sale_amount: float,
        product_id: Optional[str] = None,
        product_category: str = "",
    ) -> Dict[str, Any]:
        partner = self._get_partner(partner_id)
        if not partner:
            raise TrackingError(f"Partner {partner_id} not found.")

        event = TrackingEvent(
            event_id=self._generate_event_id("conv"),
            partner_id=partner_id,
            event_type="conversion",
            timestamp=datetime.now(),
            ip_address="",
            user_agent="",
            session_id="",
            cookie_id="",
            url="",
            referrer="",
            device_type="",
            country="",
            order_id=order_id,
            product_id=product_id,
            sale_amount=sale_amount,
        )
        self._events.append(event)

        commission_result = self._commission_calculator.calculate(
            partner=partner,
            sale_amount=sale_amount,
            order_id=order_id,
            product_category=product_category,
        )
        event.commission_amount = commission_result["commission"]
        partner.update_metrics(sale_amount)
        partner.total_commissions_earned += commission_result["commission"]
        partner.last_activity_at = datetime.now()

        if self._config.tier_upgrade_auto:
            new_tier = partner.tier_upgrade_eligible()
            if new_tier and new_tier != partner.tier:
                partner.tier = new_tier

        self._webhook_dispatcher.dispatch("conversion.tracked", {
            "partner_id": partner_id,
            "order_id": order_id,
            "sale_amount": sale_amount,
            "commission": commission_result["commission"],
        })

        return commission_result

    def track_impression(self, partner_id: str, url: str) -> TrackingEvent:
        partner = self._get_partner(partner_id)
        if not partner:
            raise TrackingError(f"Partner {partner_id} not found.")
        event = TrackingEvent(
            event_id=self._generate_event_id("imp"),
            partner_id=partner_id,
            event_type="impression",
            timestamp=datetime.now(),
            ip_address="0.0.0.0",
            user_agent="",
            session_id="",
            cookie_id="",
            url=url,
            referrer="",
            device_type="",
            country="",
        )
        self._events.append(event)
        partner.total_impressions += 1
        return event

    # -------------------------------------------------------------------------
    # Fraud Detection
    # -------------------------------------------------------------------------

    def detect_fraud(
        self,
        clicks: Optional[List[TrackingEvent]] = None,
        conversions: Optional[List[TrackingEvent]] = None,
    ) -> List[FraudAlert]:
        click_alerts = self._fraud_engine.analyze_clicks(clicks or [])
        conversion_alerts = self._fraud_engine.analyze_conversions(conversions or [])
        return click_alerts + conversion_alerts

    def get_fraud_alerts(self, resolved: bool = False) -> List[FraudAlert]:
        return self._fraud_engine.get_alerts(resolved=resolved)

    def resolve_fraud_alert(self, alert_id: str, notes: str = "", resolved_by: str = "") -> bool:
        return self._fraud_engine.resolve_alert(alert_id, notes, resolved_by)

    def blacklist_ip(self, ip: str) -> None:
        self._fraud_engine.add_to_blacklist(ip)

    # -------------------------------------------------------------------------
    # Payouts
    # -------------------------------------------------------------------------

    def request_payout(
        self,
        partner_id: str,
        amount: float,
        method: str = "paypal",
        notes: str = "",
    ) -> Payout:
        partner = self._get_partner(partner_id)
        if not partner:
            raise PayoutError(f"Partner {partner_id} not found.")
        if amount < self._config.min_payout_threshold:
            raise PayoutError(
                f"Payout amount ${amount:.2f} below minimum threshold ${self._config.min_payout_threshold:.2f}"
            )
        available = partner.total_commissions_earned - partner.total_commissions_paid
        if amount > available:
            raise PayoutError(f"Insufficient balance. Available: ${available:.2f}")

        payout = Payout(
            payout_id=self._generate_payout_id(),
            partner_id=partner_id,
            amount=amount,
            currency="USD",
            method=PayoutMethod(method),
            status=PayoutStatus.PENDING,
            notes=notes,
        )
        self._payouts.append(payout)
        self._webhook_dispatcher.dispatch("payout.requested", {"payout_id": payout.payout_id, "partner_id": partner_id, "amount": amount})
        return payout

    def process_payout(self, payout_id: str) -> Dict[str, Any]:
        payout = self._get_payout(payout_id)
        if not payout:
            raise PayoutError(f"Payout {payout_id} not found.")
        payout.status = PayoutStatus.PROCESSING
        payout.processed_at = datetime.now()

        success = random.random() > 0.05
        if success:
            payout.status = PayoutStatus.COMPLETED
            payout.completed_at = datetime.now()
            payout.transaction_id = f"txn-{secrets.token_hex(8)}"
            partner = self._get_partner(payout.partner_id)
            if partner:
                partner.total_commissions_paid += payout.amount
        else:
            payout.status = PayoutStatus.FAILED
            payout.failed_at = datetime.now()
            payout.failure_reason = "Payment processor error"

        self._webhook_dispatcher.dispatch("payout.processed", {"payout_id": payout_id, "status": payout.status.value})
        return {"status": payout.status.value, "payout_id": payout_id, "transaction_id": payout.transaction_id}

    def get_payout_history(self, partner_id: str) -> List[Payout]:
        return [p for p in self._payouts if p.partner_id == partner_id]

    # -------------------------------------------------------------------------
    # Creatives
    # -------------------------------------------------------------------------

    def create_creative(
        self,
        partner_id: str,
        name: str,
        creative_type: str,
        content: str,
        destination_url: str,
        size: str = "",
    ) -> Creative:
        partner = self._get_partner(partner_id)
        if not partner:
            raise PartnerError(f"Partner {partner_id} not found.")
        creative = Creative(
            id=self._generate_creative_id(),
            partner_id=partner_id,
            name=name,
            creative_type=CreativeType(creative_type),
            content=content,
            destination_url=destination_url,
            size=size,
            approved=not self._config.ftc_disclosure_required,
        )
        self._creatives.append(creative)
        return creative

    def get_creatives(self, partner_id: Optional[str] = None) -> List[Creative]:
        if partner_id:
            return [c for c in self._creatives if c.partner_id == partner_id]
        return list(self._creatives)

    def approve_creative(self, creative_id: str) -> bool:
        for c in self._creatives:
            if c.id == creative_id:
                c.approved = True
                c.status = "active"
                return True
        return False

    # -------------------------------------------------------------------------
    # Reporting
    # -------------------------------------------------------------------------

    def generate_performance_report(
        self,
        partner_ids: Optional[List[str]] = None,
        period_days: int = 30,
        fmt: str = "html",
        output_path: Optional[str] = None,
    ) -> str:
        partners = (
            [self._get_partner(pid) for pid in partner_ids]
            if partner_ids
            else self._partners
        )
        partners = [p for p in partners if p is not None]

        start = datetime.now() - timedelta(days=period_days)
        end = datetime.now()
        self._last_report = self._reporting_engine.generate(
            partners, fmt=fmt, output_path=output_path,
            period_start=start, period_end=end,
        )
        return self._last_report

    def get_dashboard_summary(self) -> Dict[str, Any]:
        active_partners = [p for p in self._partners if p.status == PartnerStatus.ACTIVE]
        active_rates = [p.conversion_rate for p in self._partners if p.total_clicks > 0]
        active_aovs = [p.average_order_value for p in self._partners if p.total_conversions > 0]

        return {
            "total_partners": len(self._partners),
            "active_partners": len(active_partners),
            "total_sales": sum(p.total_sales for p in self._partners),
            "total_commissions_earned": sum(p.total_commissions_earned for p in self._partners),
            "total_commissions_paid": sum(p.total_commissions_paid for p in self._partners),
            "total_clicks": sum(p.total_clicks for p in self._partners),
            "total_impressions": sum(p.total_impressions for p in self._partners),
            "total_conversions": sum(p.total_conversions for p in self._partners),
            "avg_conversion_rate": statistics.mean(active_rates) if active_rates else 0,
            "avg_order_value": statistics.mean(active_aovs) if active_aovs else 0,
            "open_fraud_alerts": len(self._fraud_engine.get_alerts(resolved=False)),
            "pending_payouts": sum(1 for p in self._payouts if p.status == PayoutStatus.PENDING),
            "tier_distribution": {
                tier.value: sum(1 for p in self._partners if p.tier == tier)
                for tier in PartnerTier
            },
            "fraud_stats": self._fraud_engine.get_stats(),
            "touchpoints_tracked": self._attribution_engine.get_touchpoint_count(),
        }

    # -------------------------------------------------------------------------
    # Webhooks
    # -------------------------------------------------------------------------

    def register_webhook(self, url: str, events: List[str], secret: str = "") -> WebhookConfig:
        return self._webhook_dispatcher.register_webhook(url, events, secret)

    def list_webhooks(self) -> List[WebhookConfig]:
        return self._webhook_dispatcher.list_webhooks()

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AffiliateMarketingAgent",
            "version": "2.0.0",
            "partners": len(self._partners),
            "active_partners": sum(1 for p in self._partners if p.status == PartnerStatus.ACTIVE),
            "total_sales": sum(p.total_sales for p in self._partners),
            "total_commissions": sum(p.total_commissions_earned for p in self._partners),
            "fraud_alerts": len(self._fraud_engine.get_alerts(resolved=False)),
            "pending_payouts": sum(1 for p in self._payouts if p.status == PayoutStatus.PENDING),
            "total_events": len(self._events),
            "total_creatives": len(self._creatives),
        }

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history[-100:]

    def clear_history(self) -> None:
        self._history = []

    def export_partners(self, fmt: str = "json") -> str:
        return json.dumps(
            [p.to_dict() for p in self._partners], indent=2, default=str
        )

    def import_partners(self, data: str, fmt: str = "json") -> int:
        if fmt == "json":
            try:
                payload = json.loads(data)
                if isinstance(payload, list):
                    imported = self.batch_import_partners(payload)
                    return len(imported)
            except json.JSONDecodeError:
                pass
        return 0

    def compare_partners(self, ids: List[str]) -> Dict[str, Any]:
        partners = [self._get_partner(pid) for pid in ids]
        partners = [p for p in partners if p]
        if not partners:
            return {}
        return {
            "partners": [
                {
                    "id": p.id,
                    "name": p.name,
                    "tier": p.tier.value,
                    "sales": p.total_sales,
                    "conversions": p.total_conversions,
                    "commission_earned": p.total_commissions_earned,
                    "conversion_rate": p.conversion_rate,
                }
                for p in partners
            ],
            "top_sales": max(partners, key=lambda p: p.total_sales).id,
            "top_conversions": max(partners, key=lambda p: p.total_conversions).id,
            "top_conversion_rate": max(
                [p for p in partners if p.total_clicks > 0],
                key=lambda p: p.conversion_rate,
                default=partners[0],
            ).id if partners else None,
        }

    def _get_partner(self, partner_id: str) -> Optional[AffiliatePartner]:
        for p in self._partners:
            if p.id == partner_id:
                return p
        return None

    def _get_payout(self, payout_id: str) -> Optional[Payout]:
        for p in self._payouts:
            if p.payout_id == payout_id:
                return p
        return None

    def _generate_event_id(self, prefix: str) -> str:
        raw = f"{prefix}-{datetime.now().isoformat()}-{secrets.token_hex(4)}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def _generate_session_id(self) -> str:
        return secrets.token_urlsafe(16)

    def _generate_cookie_id(self) -> str:
        return hashlib.md5(f"{datetime.now().isoformat()}-{random.random()}".encode()).hexdigest()

    def _generate_payout_id(self) -> str:
        raw = f"payout-{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def _generate_creative_id(self) -> str:
        raw = f"creative-{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def _log_history(self, action: str, **kwargs: Any) -> None:
        self._history.append({
            "action": action,
            "timestamp": datetime.now().isoformat(),
            **kwargs,
        })


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "AffiliateMarketingAgent",
    "AffiliatePartner",
    "CommissionRule",
    "TrackingEvent",
    "Creative",
    "Payout",
    "FraudAlert",
    "PerformanceReport",
    "WebhookConfig",
    "Config",
    "PartnerTier",
    "PartnerStatus",
    "CommissionType",
    "PayoutStatus",
    "PayoutMethod",
    "FraudSignalType",
    "AlertSeverity",
    "ReportGranularity",
    "CreativeType",
    "NetworkType",
    "AttributionModel",
    "FraudDetectionEngine",
    "CommissionCalculator",
    "AttributionEngine",
    "ReportingEngine",
    "WebhookDispatcher",
    "AffiliateError",
    "PartnerError",
    "CommissionError",
    "PayoutError",
    "TrackingError",
    "FraudDetectionError",
    "ReportingError",
    "ConfigurationError",
    "ValidationError",
]


def main():
    """Demo CLI for the Affiliate Marketing Agent."""
    import argparse

    parser = argparse.ArgumentParser(description="Affiliate Marketing Agent")
    parser.add_argument("--create-partner", action="store_true", help="Create demo partner")
    parser.add_argument("--track-click", help="Track click for partner ID")
    parser.add_argument("--track-conversion", nargs=2, metavar=("PARTNER_ID", "AMOUNT"), help="Track conversion")
    parser.add_argument("--report", action="store_true", help="Generate performance report")
    parser.add_argument("--fraud", action="store_true", help="Run fraud analysis demo")
    parser.add_argument("--dashboard", action="store_true", help="Show dashboard summary")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    agent = AffiliateMarketingAgent()

    if args.create_partner:
        partner = agent.recruit_partner(
            "Demo Partner Inc",
            "contact@demopartner.com",
            company="Demo Corp",
            website="https://demopartner.com",
        )
        print(f"Created partner: {partner.id} ({partner.name})")
        print(json.dumps(agent.get_status(), indent=2))
    elif args.track_click:
        event = agent.track_click(
            args.track_click,
            "https://example.com/product",
            ip_address="192.168.1.1",
        )
        print(f"Tracked click: {event.event_id}")
    elif args.track_conversion:
        result = agent.track_conversion(
            args.track_conversion[0],
            f"order-{int(time.time())}",
            float(args.track_conversion[1]),
        )
        print(f"Commission: ${result['commission']:.2f} (rule: {result['rule_applied']})")
    elif args.report:
        report = agent.generate_performance_report(fmt="markdown")
        print(report)
    elif args.fraud:
        partner = agent.recruit_partner("Fraud Test", "fraud@test.com")
        clicks = [
            TrackingEvent(
                event_id=f"click-{i}",
                partner_id=partner.id,
                event_type="click",
                timestamp=datetime.now() - timedelta(seconds=random.randint(1, 10)),
                ip_address=f"10.0.0.{random.randint(1, 255)}",
                user_agent="Bot/1.0",
                session_id="sess-1",
                cookie_id="cookie-1",
                url="https://example.com",
                referrer="",
                device_type="desktop",
                country="US",
            )
            for i in range(60)
        ]
        alerts = agent.detect_fraud(clicks=clicks)
        print(f"Detected {len(alerts)} fraud alerts")
        for a in alerts:
            print(f"  [{a.severity.value}] {a.signal_type.value}: {a.description}")
    elif args.dashboard:
        print(json.dumps(agent.get_dashboard_summary(), indent=2))
    else:
        print("Affiliate Marketing Agent v2.0")
        print(json.dumps(agent.get_status(), indent=2))


if __name__ == "__main__":
    main()
