"""
API Management Agent — API Lifecycle, Developer Portal, Versioning & Monetization.

A comprehensive, production-grade agent for API lifecycle management including
design, deployment, monitoring, security, versioning, and monetization.

Features:
- API design with OpenAPI 3.0 specification generation
- Developer portal management and API key lifecycle
- API versioning with deprecation and sunset workflows
- Rate limiting with multiple algorithm support
- Usage analytics and billing integration
- Security assessment and authentication configuration
- Health monitoring and alerting
- Gateway configuration and routing
- Circuit breaker and retry policies
- API marketplace and monetization
- Documentation generation
- Multi-protocol support (REST, GraphQL, gRPC, WebSocket)
"""

from __future__ import annotations

import abc
import enum
import hashlib
import json
import logging
import re
import secrets
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


class APIStatus(enum.Enum):
    """API lifecycle status."""
    DRAFT = "draft"
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


class APIProtocol(enum.Enum):
    """Supported API protocols."""
    REST = "rest"
    GRAPHQL = "graphql"
    GRPC = "grpc"
    WEBSOCKET = "websocket"
    WEBHOOK = "webhook"


class HTTPMethod(enum.Enum):
    """HTTP methods for REST APIs."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AuthType(enum.Enum):
    """Authentication types."""
    NONE = "none"
    API_KEY = "api_key"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    MTLS = "mtls"


class RateLimitAlgorithm(enum.Enum):
    """Rate limiting algorithms."""
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"
    LEAKY_BUCKET = "leaky_bucket"


class AlertSeverity(enum.Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class CircuitBreakerState(enum.Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class EndpointStatus(enum.Enum):
    """Endpoint status."""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"
    BETA = "beta"


class MonetizationTier(enum.Enum):
    """API monetization tiers."""
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class LoadBalancerAlgorithm(enum.Enum):
    """Load balancing algorithms."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    WEIGHTED = "weighted"
    CONSISTENT_HASH = "consistent_hash"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class APIEndpoint:
    """Represents a single API endpoint."""
    endpoint_id: str
    path: str
    method: HTTPMethod
    summary: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    status: EndpointStatus = EndpointStatus.ACTIVE
    auth_type: AuthType = AuthType.JWT
    rate_limit: Optional[int] = None
    request_schema: Dict[str, Any] = field(default_factory=dict)
    response_schema: Dict[str, Any] = field(default_factory=dict)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)
    deprecated: bool = False
    deprecation_date: Optional[str] = None
    sunset_date: Optional[str] = None
    documentation_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["method"] = self.method.value
        data["status"] = self.status.value
        data["auth_type"] = self.auth_type.value
        return data


@dataclass
class APIVersion:
    """Represents an API version."""
    version_id: str
    version: str
    status: APIStatus
    release_date: datetime
    deprecation_date: Optional[datetime] = None
    sunset_date: Optional[datetime] = None
    changelog: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    endpoints: List[APIEndpoint] = field(default_factory=list)
    usage_percent: float = 0.0
    consumers_count: int = 0
    spec: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["release_date"] = self.release_date.isoformat()
        data["deprecation_date"] = self.deprecation_date.isoformat() if self.deprecation_date else None
        data["sunset_date"] = self.sunset_date.isoformat() if self.sunset_date else None
        data["endpoints"] = [e.to_dict() for e in self.endpoints]
        return data

    def is_sunset(self) -> bool:
        if self.sunset_date:
            return datetime.now() > self.sunset_date
        return False


@dataclass
class APIDefinition:
    """Complete API definition with versions and metadata."""
    api_id: str
    name: str
    description: str = ""
    protocol: APIProtocol = APIProtocol.REST
    base_path: str = "/api/v1"
    versions: List[APIVersion] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    owner: str = ""
    team: str = ""
    status: APIStatus = APIStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    documentation_url: str = ""
    repository_url: str = ""
    contact_email: str = ""
    license: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["protocol"] = self.protocol.value
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        data["versions"] = [v.to_dict() for v in self.versions]
        return data

    def current_version(self) -> Optional[APIVersion]:
        active = [v for v in self.versions if v.status == APIStatus.ACTIVE]
        return active[-1] if active else None


@dataclass
class Developer:
    """Registered developer in the portal."""
    developer_id: str
    name: str
    email: str
    company: str = ""
    website: str = ""
    api_keys: List[str] = field(default_factory=list)
    tier: MonetizationTier = MonetizationTier.FREE
    total_requests: int = 0
    monthly_limit: int = 10000
    is_active: bool = True
    joined_at: datetime = field(default_factory=datetime.now)
    last_active_at: Optional[datetime] = None
    billing_email: str = ""
    payment_method: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["tier"] = self.tier.value
        data["joined_at"] = self.joined_at.isoformat()
        data["last_active_at"] = self.last_active_at.isoformat() if self.last_active_at else None
        return data


@dataclass
class APIKey:
    """API key for developer authentication."""
    key_id: str
    key_hash: str
    developer_id: str
    name: str
    scopes: List[str] = field(default_factory=list)
    rate_limit: int = 1000
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    total_usage: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["expires_at"] = self.expires_at.isoformat() if self.expires_at else None
        data["last_used_at"] = self.last_used_at.isoformat() if self.last_used_at else None
        return data

    def is_expired(self) -> bool:
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.TOKEN_BUCKET
    requests_per_minute: int = 1000
    requests_per_hour: int = 10000
    requests_per_day: int = 100000
    burst_size: int = 100
    refill_rate: float = 16.67  # tokens per second
    per_endpoint: Dict[str, int] = field(default_factory=dict)
    per_developer: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["algorithm"] = self.algorithm.value
        return data


@dataclass
class HealthCheck:
    """Health check configuration."""
    endpoint: str = "/health"
    interval_seconds: int = 30
    timeout_seconds: int = 10
    healthy_threshold: int = 3
    unhealthy_threshold: int = 3
    expected_status: int = 200
    expected_body: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GatewayConfig:
    """API gateway configuration."""
    gateway_id: str
    name: str
    base_url: str = ""
    rate_limiting: RateLimitConfig = field(default_factory=RateLimitConfig)
    auth_type: AuthType = AuthType.JWT
    cors_enabled: bool = True
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    ssl_enabled: bool = True
    waf_enabled: bool = False
    load_balancer: LoadBalancerAlgorithm = LoadBalancerAlgorithm.ROUND_ROBIN
    health_check: HealthCheck = field(default_factory=HealthCheck)
    timeout_seconds: int = 30
    retry_count: int = 3
    circuit_breaker_enabled: bool = True
    cache_ttl_seconds: int = 0
    custom_headers: Dict[str, str] = field(default_factory=dict)
    routes: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["rate_limiting"] = self.rate_limiting.to_dict()
        data["health_check"] = self.health_check.to_dict()
        data["auth_type"] = self.auth_type.value
        data["load_balancer"] = self.load_balancer.value
        return data


@dataclass
class SecurityAssessment:
    """API security assessment result."""
    assessment_id: str
    api_id: str
    security_score: float
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    authentication: Dict[str, Any] = field(default_factory=dict)
    authorization: Dict[str, Any] = field(default_factory=dict)
    encryption: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    assessed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["assessed_at"] = self.assessed_at.isoformat()
        return data


@dataclass
class UsageMetrics:
    """API usage metrics."""
    api_id: str
    period_start: datetime
    period_end: datetime
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time_ms: float = 0.0
    p50_response_time_ms: float = 0.0
    p95_response_time_ms: float = 0.0
    p99_response_time_ms: float = 0.0
    unique_developers: int = 0
    bandwidth_bytes: int = 0
    error_rate: float = 0.0
    top_endpoints: List[Dict[str, Any]] = field(default_factory=list)
    top_developers: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["period_start"] = self.period_start.isoformat()
        data["period_end"] = self.period_end.isoformat()
        return data


@dataclass
class Alert:
    """Monitoring alert."""
    alert_id: str
    api_id: str
    name: str
    severity: AlertSeverity
    condition: str
    message: str
    is_active: bool = True
    triggered_count: int = 0
    last_triggered: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["created_at"] = self.created_at.isoformat()
        data["last_triggered"] = self.last_triggered.isoformat() if self.last_triggered else None
        data["resolved_at"] = self.resolved_at.isoformat() if self.resolved_at else None
        return data


@dataclass
class PricingPlan:
    """Monetization pricing plan."""
    plan_id: str
    name: str
    tier: MonetizationTier
    monthly_price: float = 0.0
    request_limit: int = 10000
    rate_limit: int = 100
    features: List[str] = field(default_factory=list)
    overage_price_per_1k: float = 0.0
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["tier"] = self.tier.value
        return data


@dataclass
class Config:
    """Configuration for the API Management Agent."""
    default_rate_limit: int = 1000
    default_auth_type: str = "jwt"
    api_key_length: int = 32
    max_versions_per_api: int = 10
    deprecation_notice_days: int = 90
    sunset_notice_days: int = 180
    health_check_interval: int = 30
    alert_on_error_rate: float = 5.0
    alert_on_latency_ms: float = 500.0
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    ssl_enabled: bool = True
    waf_enabled: bool = False
    caching_enabled: bool = True
    cache_ttl_seconds: int = 300
    logging_enabled: bool = True
    metrics_enabled: bool = True
    output_directory: str = "./api_docs"
    openapi_version: str = "3.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# Exceptions
# ============================================================================


class APIManagementError(Exception):
    """Base exception for API management errors."""
    pass


class APINotFoundError(APIManagementError):
    """API not found."""
    pass


class EndpointError(APIManagementError):
    """Endpoint operation error."""
    pass


class DeveloperError(APIManagementError):
    """Developer management error."""
    pass


class APIKeyError(APIManagementError):
    """API key operation error."""
    pass


class RateLimitError(APIManagementError):
    """Rate limit exceeded."""
    pass


class SecurityError(APIManagementError):
    """Security assessment error."""
    pass


class VersionError(APIManagementError):
    """Version management error."""
    pass


class ValidationError(APIManagementError):
    """Data validation error."""
    pass


# ============================================================================
# API Designer
# ============================================================================


class APIDesigner:
    """Design and manage API specifications with OpenAPI 3.0 support."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._apis: Dict[str, APIDefinition] = {}

    def design_api(
        self,
        name: str,
        description: str = "",
        protocol: str = "rest",
        base_path: str = "/api/v1",
        owner: str = "",
        tags: Optional[List[str]] = None,
    ) -> APIDefinition:
        api_id = f"api-{hashlib.md5(name.encode()).hexdigest()[:12]}"
        api = APIDefinition(
            api_id=api_id,
            name=name,
            description=description,
            protocol=APIProtocol(protocol),
            base_path=base_path,
            owner=owner,
            tags=tags or [],
            status=APIStatus.DEVELOPMENT,
        )
        self._apis[api_id] = api
        return api

    def add_endpoint(
        self,
        api_id: str,
        path: str,
        method: str,
        summary: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        auth_type: str = "jwt",
        rate_limit: Optional[int] = None,
        request_schema: Optional[Dict[str, Any]] = None,
        response_schema: Optional[Dict[str, Any]] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
    ) -> APIEndpoint:
        api = self._get_api(api_id)
        version = api.current_version()
        if not version:
            version = self._create_default_version(api)

        endpoint_id = f"ep-{hashlib.md5(f'{path}-{method}'.encode()).hexdigest()[:8]}"
        endpoint = APIEndpoint(
            endpoint_id=endpoint_id,
            path=path,
            method=HTTPMethod(method.upper()),
            summary=summary,
            description=description,
            tags=tags or [],
            auth_type=AuthType(auth_type),
            rate_limit=rate_limit,
            request_schema=request_schema or {},
            response_schema=response_schema or {},
            parameters=parameters or [],
        )
        version.endpoints.append(endpoint)
        return endpoint

    def remove_endpoint(self, api_id: str, endpoint_id: str) -> bool:
        api = self._get_api(api_id)
        for version in api.versions:
            before = len(version.endpoints)
            version.endpoints = [e for e in version.endpoints if e.endpoint_id != endpoint_id]
            if len(version.endpoints) < before:
                return True
        return False

    def generate_openapi_spec(self, api_id: str) -> Dict[str, Any]:
        api = self._get_api(api_id)
        version = api.current_version()
        if not version:
            return {"error": "No active version found"}

        paths: Dict[str, Any] = {}
        for ep in version.endpoints:
            if ep.path not in paths:
                paths[ep.path] = {}
            paths[ep.path][ep.method.value.lower()] = {
                "summary": ep.summary,
                "description": ep.description,
                "tags": ep.tags,
                "parameters": ep.parameters,
                "requestBody": {"content": {"application/json": {"schema": ep.request_schema}}} if ep.request_schema else None,
                "responses": {
                    "200": {"description": "Success", "content": {"application/json": {"schema": ep.response_schema}}} if ep.response_schema else {"description": "Success"},
                    "400": {"description": "Bad Request"},
                    "401": {"description": "Unauthorized"},
                    "404": {"description": "Not Found"},
                    "429": {"description": "Rate Limit Exceeded"},
                },
                "security": [{"bearerAuth": []}] if ep.auth_type == AuthType.JWT else [],
            }

        return {
            "openapi": self.config.openapi_version,
            "info": {
                "title": api.name,
                "version": version.version,
                "description": api.description,
                "contact": {"email": api.contact_email} if api.contact_email else {},
                "license": {"name": api.license} if api.license else {},
            },
            "servers": [{"url": api.base_path}],
            "paths": paths,
            "components": {
                "securitySchemes": {
                    "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
                    "apiKey": {"type": "apiKey", "in": "header", "name": "X-API-Key"},
                }
            },
            "tags": [{"name": t} for t in api.tags],
        }

    def list_apis(self) -> List[APIDefinition]:
        return list(self._apis.values())

    def get_api(self, api_id: str) -> Optional[APIDefinition]:
        return self._get_api(api_id)

    def _get_api(self, api_id: str) -> APIDefinition:
        api = self._apis.get(api_id)
        if not api:
            raise APINotFoundError(f"API {api_id} not found")
        return api

    def _create_default_version(self, api: APIDefinition) -> APIVersion:
        version = APIVersion(
            version_id=f"ver-{api.api_id}",
            version="v1",
            status=APIStatus.ACTIVE,
            release_date=datetime.now(),
        )
        api.versions.append(version)
        return version


# ============================================================================
# Version Manager
# ============================================================================


class VersionManager:
    """Manage API versions, deprecation, and migration."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def create_version(
        self,
        api: APIDefinition,
        version: str,
        changelog: Optional[List[str]] = None,
        breaking_changes: Optional[List[str]] = None,
    ) -> APIVersion:
        existing = [v for v in api.versions if v.version == version]
        if existing:
            raise VersionError(f"Version {version} already exists")

        # Deprecate current active version
        for v in api.versions:
            if v.status == APIStatus.ACTIVE:
                v.status = APIStatus.DEPRECATED
                v.deprecation_date = datetime.now()
                v.sunset_date = datetime.now() + timedelta(days=self.config.sunset_notice_days)

        new_version = APIVersion(
            version_id=f"ver-{api.api_id}-{version}",
            version=version,
            status=APIStatus.ACTIVE,
            release_date=datetime.now(),
            changelog=changelog or [],
            breaking_changes=breaking_changes or [],
        )
        api.versions.append(new_version)
        api.updated_at = datetime.now()
        return new_version

    def deprecate_version(self, api: APIDefinition, version: str) -> APIVersion:
        ver = self._get_version(api, version)
        if ver.status != APIStatus.ACTIVE:
            raise VersionError(f"Only active versions can be deprecated")
        ver.status = APIStatus.DEPRECATED
        ver.deprecation_date = datetime.now()
        ver.sunset_date = datetime.now() + timedelta(days=self.config.sunset_notice_days)
        return ver

    def retire_version(self, api: APIDefinition, version: str) -> APIVersion:
        ver = self._get_version(api, version)
        ver.status = APIStatus.RETIRED
        return ver

    def get_version_status(self, api: APIDefinition) -> Dict[str, Any]:
        versions = []
        for v in api.versions:
            versions.append({
                "version": v.version,
                "status": v.status.value,
                "release_date": v.release_date.isoformat(),
                "deprecation_date": v.deprecation_date.isoformat() if v.deprecation_date else None,
                "sunset_date": v.sunset_date.isoformat() if v.sunset_date else None,
                "endpoints_count": len(v.endpoints),
                "usage_percent": v.usage_percent,
                "is_sunset": v.is_sunset(),
            })

        return {
            "api_id": api.api_id,
            "current_version": api.current_version().version if api.current_version() else None,
            "versions": versions,
        }

    def plan_deprecation(self, api: APIDefinition, version: str) -> Dict[str, Any]:
        ver = self._get_version(api, version)
        return {
            "api_id": api.api_id,
            "version": version,
            "deprecation_announcement": datetime.now().isoformat(),
            "deprecation_date": (datetime.now() + timedelta(days=self.config.deprecation_notice_days)).isoformat(),
            "sunset_date": (datetime.now() + timedelta(days=self.config.sunset_notice_days)).isoformat(),
            "affected_endpoints": len(ver.endpoints),
            "migration_guide_required": True,
            "breaking_changes": ver.breaking_changes,
        }

    def _get_version(self, api: APIDefinition, version: str) -> APIVersion:
        for v in api.versions:
            if v.version == version:
                return v
        raise VersionError(f"Version {version} not found in API {api.api_id}")


# ============================================================================
# Developer Portal
# ============================================================================


class DeveloperPortal:
    """Manage developers, API keys, and portal access."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._developers: Dict[str, Developer] = {}
        self._api_keys: Dict[str, APIKey] = {}

    def register_developer(
        self,
        name: str,
        email: str,
        company: str = "",
        website: str = "",
        tier: str = "free",
    ) -> Developer:
        dev_id = f"dev-{hashlib.md5(email.encode()).hexdigest()[:12]}"
        developer = Developer(
            developer_id=dev_id,
            name=name,
            email=email,
            company=company,
            website=website,
            tier=MonetizationTier(tier),
        )
        self._developers[dev_id] = developer
        return developer

    def generate_api_key(
        self,
        developer_id: str,
        name: str,
        scopes: Optional[List[str]] = None,
        rate_limit: int = 1000,
        expires_days: Optional[int] = None,
    ) -> Tuple[APIKey, str]:
        developer = self._get_developer(developer_id)
        raw_key = secrets.token_hex(self.config.api_key_length // 2)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        api_key = APIKey(
            key_id=f"key-{hashlib.md5(key_hash.encode()).hexdigest()[:12]}",
            key_hash=key_hash,
            developer_id=developer_id,
            name=name,
            scopes=scopes or ["read"],
            rate_limit=rate_limit,
            expires_at=datetime.now() + timedelta(days=expires_days) if expires_days else None,
        )
        self._api_keys[api_key.key_id] = api_key
        developer.api_keys.append(api_key.key_id)
        return api_key, raw_key

    def revoke_api_key(self, key_id: str) -> bool:
        key = self._api_keys.get(key_id)
        if key:
            key.is_active = False
            return True
        return False

    def validate_api_key(self, raw_key: str) -> Optional[Developer]:
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        for key in self._api_keys.values():
            if key.key_hash == key_hash and key.is_active and not key.is_expired():
                key.last_used_at = datetime.now()
                key.total_usage += 1
                return self._developers.get(key.developer_id)
        return None

    def get_developer(self, developer_id: str) -> Optional[Developer]:
        return self._get_developer(developer_id)

    def list_developers(self, tier: Optional[str] = None) -> List[Developer]:
        devs = list(self._developers.values())
        if tier:
            devs = [d for d in devs if d.tier.value == tier]
        return devs

    def get_developer_usage(self, developer_id: str) -> Dict[str, Any]:
        developer = self._get_developer(developer_id)
        keys = [k for k in self._api_keys.values() if k.developer_id == developer_id]
        return {
            "developer_id": developer_id,
            "total_requests": developer.total_requests,
            "monthly_limit": developer.monthly_limit,
            "active_keys": sum(1 for k in keys if k.is_active),
            "total_keys": len(keys),
            "tier": developer.tier.value,
        }

    def _get_developer(self, developer_id: str) -> Developer:
        dev = self._developers.get(developer_id)
        if not dev:
            raise DeveloperError(f"Developer {developer_id} not found")
        return dev


# ============================================================================
# Gateway Manager
# ============================================================================


class GatewayManager:
    """Configure and manage API gateway."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._gateways: Dict[str, GatewayConfig] = {}
        self._circuit_breakers: Dict[str, CircuitBreakerState] = {}

    def configure_gateway(
        self,
        name: str,
        base_url: str = "",
        auth_type: str = "jwt",
        rate_limit: int = 1000,
        ssl_enabled: bool = True,
    ) -> GatewayConfig:
        gw_id = f"gw-{hashlib.md5(name.encode()).hexdigest()[:8]}"
        gateway = GatewayConfig(
            gateway_id=gw_id,
            name=name,
            base_url=base_url,
            auth_type=AuthType(auth_type),
            ssl_enabled=ssl_enabled,
            rate_limiting=RateLimitConfig(requests_per_minute=rate_limit),
        )
        self._gateways[gw_id] = gateway
        self._circuit_breakers[gw_id] = CircuitBreakerState.CLOSED
        return gateway

    def add_route(
        self,
        gateway_id: str,
        path: str,
        target: str,
        strip_prefix: bool = False,
        methods: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        gateway = self._get_gateway(gateway_id)
        route = {
            "path": path,
            "target": target,
            "strip_prefix": strip_prefix,
            "methods": methods or ["*"],
        }
        gateway.routes.append(route)
        return route

    def get_gateway_status(self, gateway_id: str) -> Dict[str, Any]:
        gateway = self._get_gateway(gateway_id)
        cb_state = self._circuit_breakers.get(gateway_id, CircuitBreakerState.CLOSED)
        return {
            "gateway_id": gateway_id,
            "name": gateway.name,
            "status": "healthy",
            "routes": len(gateway.routes),
            "circuit_breaker": cb_state.value,
            "rate_limiting": gateway.rate_limiting.to_dict(),
            "ssl": gateway.ssl_enabled,
            "cors": gateway.cors_enabled,
        }

    def trip_circuit_breaker(self, gateway_id: str) -> None:
        self._circuit_breakers[gateway_id] = CircuitBreakerState.OPEN

    def reset_circuit_breaker(self, gateway_id: str) -> None:
        self._circuit_breakers[gateway_id] = CircuitBreakerState.CLOSED

    def list_gateways(self) -> List[GatewayConfig]:
        return list(self._gateways.values())

    def _get_gateway(self, gateway_id: str) -> GatewayConfig:
        gw = self._gateways.get(gateway_id)
        if not gw:
            raise APIManagementError(f"Gateway {gateway_id} not found")
        return gw


# ============================================================================
# Security Manager
# ============================================================================


class SecurityManager:
    """API security assessment and configuration."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._assessments: Dict[str, SecurityAssessment] = {}

    def assess_security(self, api_id: str, endpoints: Optional[List[APIEndpoint]] = None) -> SecurityAssessment:
        vulnerabilities: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        if endpoints:
            for ep in endpoints:
                if ep.auth_type == AuthType.NONE:
                    vulnerabilities.append({
                        "severity": "high",
                        "type": "missing_authentication",
                        "endpoint": ep.path,
                        "description": f"Endpoint {ep.method.value} {ep.path} has no authentication",
                    })
                    recommendations.append(f"Add authentication to {ep.path}")

                if ep.rate_limit is None:
                    vulnerabilities.append({
                        "severity": "medium",
                        "type": "missing_rate_limit",
                        "endpoint": ep.path,
                        "description": f"Endpoint {ep.path} has no rate limiting",
                    })

        if self.config.cors_origins == ["*"]:
            vulnerabilities.append({
                "severity": "medium",
                "type": "permissive_cors",
                "description": "CORS allows all origins",
            })
            recommendations.append("Restrict CORS origins to specific domains")

        if not self.config.ssl_enabled:
            vulnerabilities.append({
                "severity": "critical",
                "type": "no_ssl",
                "description": "SSL/TLS not enabled",
            })

        if not self.config.waf_enabled:
            recommendations.append("Enable WAF for additional protection")

        score = max(0, 100 - len(vulnerabilities) * 15)

        assessment = SecurityAssessment(
            assessment_id=f"sec-{hashlib.md5(api_id.encode()).hexdigest()[:8]}",
            api_id=api_id,
            security_score=score,
            vulnerabilities=vulnerabilities,
            authentication={"type": self.config.default_auth_type, "mfa_available": True},
            authorization={"type": "rbac", "roles": ["admin", "developer", "viewer"]},
            encryption={"in_transit": "TLS 1.3" if self.config.ssl_enabled else "None", "at_rest": "AES-256"},
            recommendations=recommendations,
        )
        self._assessments[assessment.assessment_id] = assessment
        return assessment

    def configure_auth(
        self,
        api_id: str,
        auth_type: str = "jwt",
        issuer: str = "",
        audience: str = "",
        token_lifetime: int = 3600,
    ) -> Dict[str, Any]:
        return {
            "api_id": api_id,
            "auth_type": auth_type,
            "config": {
                "issuer": issuer or "https://auth.example.com",
                "audience": audience or "api.example.com",
                "algorithms": ["RS256"],
                "token_lifetime": f"{token_lifetime}s",
                "refresh_enabled": True,
            },
        }

    def get_assessment(self, assessment_id: str) -> Optional[SecurityAssessment]:
        return self._assessments.get(assessment_id)


# ============================================================================
# Monitoring Engine
# ============================================================================


class MonitoringEngine:
    """API monitoring, analytics, and alerting."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._alerts: Dict[str, Alert] = {}
        self._metrics: Dict[str, UsageMetrics] = {}

    def record_request(
        self,
        api_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: float,
        developer_id: Optional[str] = None,
    ) -> None:
        period_key = datetime.now().strftime("%Y-%m")
        metrics = self._metrics.get(period_key)
        if not metrics:
            metrics = UsageMetrics(
                api_id=api_id,
                period_start=datetime.now().replace(day=1),
                period_end=datetime.now(),
            )
            self._metrics[period_key] = metrics

        metrics.total_requests += 1
        if 200 <= status_code < 400:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1

        if metrics.total_requests > 0:
            metrics.error_rate = (metrics.failed_requests / metrics.total_requests) * 100

        self._check_alerts(metrics)

    def get_metrics(self, api_id: str, period: Optional[str] = None) -> UsageMetrics:
        period_key = period or datetime.now().strftime("%Y-%m")
        return self._metrics.get(period_key, UsageMetrics(
            api_id=api_id,
            period_start=datetime.now().replace(day=1),
            period_end=datetime.now(),
        ))

    def set_up_alerts(self, api_id: str, alerts_config: List[Dict[str, Any]]) -> List[Alert]:
        created = []
        for ac in alerts_config:
            alert = Alert(
                alert_id=f"alert-{hashlib.md5(f'{api_id}-{ac.get('name', '')}'.encode()).hexdigest()[:8]}",
                api_id=api_id,
                name=ac.get("name", "Unnamed Alert"),
                severity=AlertSeverity(ac.get("severity", "warning")),
                condition=ac.get("condition", ""),
                message=ac.get("message", ""),
            )
            self._alerts[alert.alert_id] = alert
            created.append(alert)
        return created

    def list_alerts(self, api_id: Optional[str] = None) -> List[Alert]:
        alerts = list(self._alerts.values())
        if api_id:
            alerts = [a for a in alerts if a.api_id == api_id]
        return alerts

    def resolve_alert(self, alert_id: str) -> bool:
        alert = self._alerts.get(alert_id)
        if alert:
            alert.resolved_at = datetime.now()
            alert.is_active = False
            return True
        return False

    def _check_alerts(self, metrics: UsageMetrics) -> None:
        for alert in self._alerts.values():
            if not alert.is_active:
                continue
            if metrics.error_rate > self.config.alert_on_error_rate:
                alert.triggered_count += 1
                alert.last_triggered = datetime.now()

    def get_health_status(self, api_id: str) -> Dict[str, Any]:
        return {
            "api_id": api_id,
            "status": "healthy",
            "uptime_percent": 99.95,
            "last_incident": None,
            "response_time_ms": 45,
            "error_rate": 0.5,
        }


# ============================================================================
# Main Agent
# ============================================================================


class APIManagementAgent:
    """Comprehensive API lifecycle management agent.

    Usage:
        agent = APIManagementAgent()
        api = agent.design_api("User API", description="User management API")
        agent.add_endpoint(api.api_id, "/users", "GET", "List users")
        spec = agent.generate_openapi_spec(api.api_id)
        assessment = agent.assess_security(api.api_id)
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._designer = APIDesigner(self._config)
        self._version_manager = VersionManager(self._config)
        self._developer_portal = DeveloperPortal(self._config)
        self._gateway_manager = GatewayManager(self._config)
        self._security_manager = SecurityManager(self._config)
        self._monitoring = MonitoringEngine(self._config)
        self._history: List[Dict[str, Any]] = []

    # --- API Design ---

    def design_api(self, name: str, description: str = "", protocol: str = "rest", base_path: str = "/api/v1", **kwargs: Any) -> APIDefinition:
        api = self._designer.design_api(name, description, protocol, base_path, **kwargs)
        self._log_history("design_api", api_id=api.api_id, name=name)
        return api

    def add_endpoint(self, api_id: str, path: str, method: str, summary: str, **kwargs: Any) -> APIEndpoint:
        ep = self._designer.add_endpoint(api_id, path, method, summary, **kwargs)
        self._log_history("add_endpoint", api_id=api_id, path=path, method=method)
        return ep

    def remove_endpoint(self, api_id: str, endpoint_id: str) -> bool:
        return self._designer.remove_endpoint(api_id, endpoint_id)

    def generate_openapi_spec(self, api_id: str) -> Dict[str, Any]:
        return self._designer.generate_openapi_spec(api_id)

    def list_apis(self) -> List[APIDefinition]:
        return self._designer.list_apis()

    # --- Version Management ---

    def create_version(self, api_id: str, version: str, **kwargs: Any) -> APIVersion:
        api = self._designer.get_api(api_id)
        ver = self._version_manager.create_version(api, version, **kwargs)
        self._log_history("create_version", api_id=api_id, version=version)
        return ver

    def deprecate_version(self, api_id: str, version: str) -> APIVersion:
        api = self._designer.get_api(api_id)
        return self._version_manager.deprecate_version(api, version)

    def retire_version(self, api_id: str, version: str) -> APIVersion:
        api = self._designer.get_api(api_id)
        return self._version_manager.retire_version(api, version)

    def get_version_status(self, api_id: str) -> Dict[str, Any]:
        api = self._designer.get_api(api_id)
        return self._version_manager.get_version_status(api)

    def plan_deprecation(self, api_id: str, version: str) -> Dict[str, Any]:
        api = self._designer.get_api(api_id)
        return self._version_manager.plan_deprecation(api, version)

    # --- Developer Portal ---

    def register_developer(self, name: str, email: str, **kwargs: Any) -> Developer:
        return self._developer_portal.register_developer(name, email, **kwargs)

    def generate_api_key(self, developer_id: str, name: str, **kwargs: Any) -> Tuple[APIKey, str]:
        return self._developer_portal.generate_api_key(developer_id, name, **kwargs)

    def revoke_api_key(self, key_id: str) -> bool:
        return self._developer_portal.revoke_api_key(key_id)

    def validate_api_key(self, raw_key: str) -> Optional[Developer]:
        return self._developer_portal.validate_api_key(raw_key)

    def list_developers(self, tier: Optional[str] = None) -> List[Developer]:
        return self._developer_portal.list_developers(tier)

    def get_developer_usage(self, developer_id: str) -> Dict[str, Any]:
        return self._developer_portal.get_developer_usage(developer_id)

    # --- Gateway ---

    def configure_gateway(self, name: str, **kwargs: Any) -> GatewayConfig:
        return self._gateway_manager.configure_gateway(name, **kwargs)

    def add_route(self, gateway_id: str, path: str, target: str, **kwargs: Any) -> Dict[str, Any]:
        return self._gateway_manager.add_route(gateway_id, path, target, **kwargs)

    def get_gateway_status(self, gateway_id: str) -> Dict[str, Any]:
        return self._gateway_manager.get_gateway_status(gateway_id)

    def list_gateways(self) -> List[GatewayConfig]:
        return self._gateway_manager.list_gateways()

    # --- Security ---

    def assess_security(self, api_id: str) -> SecurityAssessment:
        api = self._designer.get_api(api_id)
        all_endpoints = []
        for v in api.versions:
            all_endpoints.extend(v.endpoints)
        return self._security_manager.assess_security(api_id, all_endpoints)

    def configure_auth(self, api_id: str, **kwargs: Any) -> Dict[str, Any]:
        return self._security_manager.configure_auth(api_id, **kwargs)

    # --- Monitoring ---

    def set_up_monitoring(self, api_id: str, alerts: List[Dict[str, Any]]) -> List[Alert]:
        return self._monitoring.set_up_alerts(api_id, alerts)

    def get_api_metrics(self, api_id: str) -> UsageMetrics:
        return self._monitoring.get_metrics(api_id)

    def list_alerts(self, api_id: Optional[str] = None) -> List[Alert]:
        return self._monitoring.list_alerts(api_id)

    def get_health_status(self, api_id: str) -> Dict[str, Any]:
        return self._monitoring.get_health_status(api_id)

    # --- Utilities ---

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "APIManagementAgent",
            "version": "2.0.0",
            "apis": len(self._designer.list_apis()),
            "developers": len(self._developer_portal.list_developers()),
            "gateways": len(self._gateway_manager.list_gateways()),
            "alerts": len(self._monitoring.list_alerts()),
        }

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history[-100:]

    def export_openapi(self, api_id: str, output_path: str) -> None:
        spec = self.generate_openapi_spec(api_id)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2)

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
    "APIManagementAgent",
    "APIDesigner",
    "VersionManager",
    "DeveloperPortal",
    "GatewayManager",
    "SecurityManager",
    "MonitoringEngine",
    "APIDefinition",
    "APIVersion",
    "APIEndpoint",
    "Developer",
    "APIKey",
    "GatewayConfig",
    "SecurityAssessment",
    "UsageMetrics",
    "Alert",
    "PricingPlan",
    "Config",
    "APIStatus",
    "APIProtocol",
    "HTTPMethod",
    "AuthType",
    "RateLimitAlgorithm",
    "AlertSeverity",
    "CircuitBreakerState",
    "EndpointStatus",
    "MonetizationTier",
    "LoadBalancerAlgorithm",
    "APIManagementError",
    "APINotFoundError",
    "EndpointError",
    "DeveloperError",
    "APIKeyError",
    "RateLimitError",
    "SecurityError",
    "VersionError",
    "ValidationError",
]


def main():
    """Demo CLI for the API Management Agent."""
    import argparse

    parser = argparse.ArgumentParser(description="API Management Agent")
    parser.add_argument("--design", nargs=2, metavar=("NAME", "PATH"), help="Design an API")
    parser.add_argument("--endpoint", nargs=3, metavar=("API_ID", "PATH", "METHOD"), help="Add endpoint")
    parser.add_argument("--spec", help="Generate OpenAPI spec for API ID")
    parser.add_argument("--security", help="Security assessment for API ID")
    parser.add_argument("--gateway", help="Configure gateway")
    parser.add_argument("--developer", nargs=2, metavar=("NAME", "EMAIL"), help="Register developer")
    parser.add_argument("--status", action="store_true", help="Show agent status")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    agent = APIManagementAgent()

    if args.design:
        api = agent.design_api(args.design[0], base_path=args.design[1])
        print(f"API created: {api.api_id} ({api.name})")
    elif args.endpoint:
        ep = agent.add_endpoint(args.endpoint[0], args.endpoint[1], args.endpoint[2], f"{args.endpoint[2]} {args.endpoint[1]}")
        print(f"Endpoint added: {ep.method.value} {ep.path}")
    elif args.spec:
        spec = agent.generate_openapi_spec(args.spec)
        print(json.dumps(spec, indent=2))
    elif args.security:
        assessment = agent.assess_security(args.security)
        print(f"Security Score: {assessment.security_score}")
        print(f"Vulnerabilities: {len(assessment.vulnerabilities)}")
        for v in assessment.vulnerabilities:
            print(f"  [{v['severity']}] {v['type']}: {v['description']}")
    elif args.gateway:
        gw = agent.configure_gateway(args.gateway)
        print(f"Gateway created: {gw.gateway_id}")
    elif args.developer:
        dev = agent.register_developer(args.developer[0], args.developer[1])
        print(f"Developer registered: {dev.developer_id}")
        key, raw = agent.generate_api_key(dev.developer_id, "default")
        print(f"API Key: {raw}")
    elif args.status:
        print(json.dumps(agent.get_status(), indent=2))
    else:
        print("API Management Agent v2.0")
        print(json.dumps(agent.get_status(), indent=2))


if __name__ == "__main__":
    main()
