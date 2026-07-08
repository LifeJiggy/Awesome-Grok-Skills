"""
API Gateway Agent - Enterprise-Grade Gateway Management and Configuration.

This agent provides comprehensive API gateway management capabilities including
routing, rate limiting, authentication, caching, circuit breaking, and more.
"""

from __future__ import annotations

import logging
import time
import json
import hashlib
import random
import string
import uuid
import re
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum, auto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-gateway-agent")


class GatewayEnvironment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    DISASTER_RECOVERY = "disaster_recovery"


class AuthType(Enum):
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    MTLS = "mTLS"
    BASIC = "basic"
    CUSTOM = "custom"
    NONE = "none"


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    ANY = "ANY"


class RateLimitAlgorithm(Enum):
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"
    LEAKY_BUCKET = "leaky_bucket"


class LoadBalancingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    RANDOM = "random"
    CONSISTENT_HASH = "consistent_hash"


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class LoggingLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class GatewayError(Exception):
    pass


class ValidationError(Exception):
    pass


class RateLimitExceededError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UpstreamUnavailableError(Exception):
    pass


class CircuitBreakerOpenError(Exception):
    pass


class RequestValidationError(Exception):
    pass


@dataclass
class APIKey:
    key_id: str
    key_value: str
    owner: str
    scopes: List[str] = field(default_factory=list)
    rate_limit_override: Optional[int] = None
    active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    ip_whitelist: List[str] = field(default_factory=list)
    ip_blacklist: List[str] = field(default_factory=list)


@dataclass
class JWTPayload:
    sub: str
    iss: str
    aud: str
    exp: int
    iat: int
    scopes: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    custom_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UpstreamServer:
    url: str
    weight: int = 100
    health_check_path: str = "/health"
    health_check_interval: int = 30
    health_check_timeout: int = 10
    unhealthy_threshold: int = 3
    healthy_threshold: int = 2
    is_healthy: bool = True
    current_connections: int = 0
    last_health_check: Optional[datetime] = None
    failure_count: int = 0
    success_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EndpointConfig:
    path: str
    methods: List[HTTPMethod]
    upstream_url: str
    auth_type: AuthType = AuthType.NONE
    rate_limit: Optional[int] = None
    rate_limit_window: int = 60
    rate_limit_algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW
    timeout_ms: int = 30000
    retries: int = 3
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60000
    caching_enabled: bool = False
    cache_ttl_seconds: int = 300
    response_transform: Optional[Dict[str, Any]] = None
    request_transform: Optional[Dict[str, Any]] = None
    headers_to_add: Dict[str, str] = field(default_factory=dict)
    headers_to_remove: List[str] = field(default_factory=list)
    query_params_to_add: Dict[str, str] = field(default_factory=dict)
    query_params_to_remove: List[str] = field(default_factory=list)
    validate_request_body: bool = False
    max_request_size_bytes: int = 10485760
    cors_enabled: bool = False
    cors_origins: List[str] = field(default_factory=list)
    cors_methods: List[str] = field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    cors_headers: List[str] = field(default_factory=list)
    cors_credentials: bool = False
    cors_max_age_seconds: int = 86400
    metadata: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    tags: List[str] = field(default_factory=list)
    deprecated: bool = False
    version: str = "v1"
    openapi_tags: List[str] = field(default_factory=list)

    def matches_path(self, request_path: str) -> bool:
        pattern = self.path.replace("*", ".*").replace("{param}", "[^/]+")
        return bool(re.match(f"^{pattern}$", request_path))

    def matches_method(self, method: str) -> bool:
        if HTTPMethod.ANY in self.methods:
            return True
        return any(m.value == method for m in self.methods)


@dataclass
class RateLimitConfig:
    default_requests_per_window: int = 1000
    default_window_seconds: int = 60
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW
    per_endpoint_limits: Dict[str, Dict[str, int]] = field(default_factory=dict)
    per_user_limits: Dict[str, Dict[str, int]] = field(default_factory=dict)
    ip_whitelist: List[str] = field(default_factory=list)
    ip_blacklist: List[str] = field(default_factory=list)
    enable_rate_limit_headers: bool = True


@dataclass
class AuthConfig:
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    oauth2_issuer: str = ""
    oauth2_audience: str = ""
    api_key_header: str = "X-API-Key"
    api_key_prefix: str = "sk_"
    allowed_scopes: List[str] = field(default_factory=list)
    token_validation_rules: Dict[str, Any] = field(default_factory=dict)
    enable_oauth2_token_refresh: bool = True
    basic_auth_realm: str = "API Gateway"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout_seconds: int = 60
    half_open_requests: int = 3
    monitoring_window_seconds: int = 30
    fallback_response: Optional[Dict[str, Any]] = None


@dataclass
class CacheConfig:
    enabled: bool = True
    default_ttl_seconds: int = 300
    max_cache_size_mb: int = 100
    cache_key_patterns: List[str] = field(default_factory=list)
    excluded_paths: List[str] = field(default_factory=list)
    storage_type: str = "memory"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    enable_stale_while_revalidate: bool = False
    stale_ttl_seconds: int = 60


@dataclass
class LoggingConfig:
    level: LoggingLevel = LoggingLevel.INFO
    format: str = "json"
    include_headers: bool = True
    include_request_body: bool = False
    include_response_body: bool = False
    sensitive_headers: List[str] = field(default_factory=lambda: ["authorization", "x-api-key", "cookie"])
    log_requests: bool = True
    log_responses: bool = True
    log_errors_only: bool = False
    log_destination: str = "stdout"
    log_file_path: str = "gateway.log"
    log_rotation_size_mb: int = 100
    log_rotation_count: int = 10


@dataclass
class TLSConfig:
    enabled: bool = True
    cert_file: str = ""
    key_file: str = ""
    ca_file: str = ""
    min_version: str = "TLSv1.2"
    ciphers: List[str] = field(default_factory=lambda: [
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384"
    ])
    enable_mtls: bool = False
    client_ca_file: str = ""


@dataclass
class GatewayConfig:
    name: str = "api-gateway"
    environment: GatewayEnvironment = GatewayEnvironment.DEVELOPMENT
    host: str = "0.0.0.0"
    port: int = 8080
    https_port: int = 8443
    worker_processes: int = 4
    max_connections: int = 10000
    keepalive_timeout: int = 65
    read_timeout: int = 30
    write_timeout: int = 30
    idle_timeout: int = 120
    endpoint_configs: List[EndpointConfig] = field(default_factory=list)
    rate_limit_config: RateLimitConfig = field(default_factory=RateLimitConfig)
    auth_config: AuthConfig = field(default_factory=AuthConfig)
    circuit_breaker_config: CircuitBreakerConfig = field(default_factory=CircuitBreakerConfig)
    cache_config: CacheConfig = field(default_factory=CacheConfig)
    logging_config: LoggingConfig = field(default_factory=LoggingConfig)
    tls_config: TLSConfig = field(default_factory=TLSConfig)
    enable_security_headers: bool = True
    allowed_origins: List[str] = field(default_factory=lambda: ["*"])
    max_request_size_mb: int = 10
    proxy_protocol: bool = False


@dataclass
class RequestContext:
    request_id: str
    client_ip: str
    method: str
    path: str
    headers: Dict[str, str]
    query_params: Dict[str, str]
    body: Any
    start_time: datetime
    endpoint: Optional[EndpointConfig] = None
    authenticated: bool = False
    auth_type: str = ""
    user_id: Optional[str] = None
    rate_limit_remaining: int = 0
    upstream_server: Optional[UpstreamServer] = None


@dataclass
class ResponseContext:
    status_code: int
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None
    latency_ms: int = 0
    cached: bool = False
    from_cache: bool = False


class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = max(0.0, now - self.last_refill)
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now

            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

    def get_remaining(self) -> int:
        with self.lock:
            return int(self.tokens)

    def get_reset_seconds(self) -> float:
        with self.lock:
            if self.tokens >= 1.0:
                return 0.0
            return (1.0 - self.tokens) / self.refill_rate


class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()

    def allow_request(self, identifier: str) -> bool:
        with self.lock:
            now = time.time()
            window_start = now - self.window_seconds
            reqs = self.requests[identifier]
            self.requests[identifier] = [r for r in reqs if r >= window_start]

            if len(self.requests[identifier]) < self.max_requests:
                self.requests[identifier].append(now)
                return True
            return False

    def get_remaining(self, identifier: str) -> int:
        with self.lock:
            now = time.time()
            window_start = now - self.window_seconds
            reqs = self.requests[identifier]
            valid = [r for r in reqs if r >= window_start]
            self.requests[identifier] = valid
            return max(0, self.max_requests - len(valid))


class FixedWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._windows: Dict[str, Dict[str, int]] = defaultdict(lambda: {"count": 0, "window_start": 0})
        self.lock = threading.Lock()

    def allow_request(self, identifier: str) -> bool:
        with self.lock:
            now = time.time()
            current_window = int(now / self.window_seconds)
            state = self._windows[identifier]
            if state["window_start"] != current_window:
                state["count"] = 0
                state["window_start"] = current_window
            if state["count"] < self.max_requests:
                state["count"] += 1
                return True
            return False

    def get_remaining(self, identifier: str) -> int:
        with self.lock:
            state = self._windows[identifier]
            now = time.time()
            current_window = int(now / self.window_seconds)
            if state["window_start"] != current_window:
                return self.max_requests
            return max(0, self.max_requests - state["count"])


class LeakyBucketRateLimiter:
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water_level = 0.0
        self.last_leak = time.time()
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = max(0.0, now - self.last_leak)
            self.water_level = max(0.0, self.water_level - elapsed * self.leak_rate)
            self.last_leak = now
            if self.water_level < self.capacity:
                self.water_level += 1.0
                return True
            return False

    def get_remaining(self) -> int:
        with self.lock:
            return int(self.capacity - self.water_level)


class CircuitBreaker:
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure: Optional[datetime] = None
        self.next_attempt: Optional[datetime] = None
        self.half_open_successes = 0
        self.monitoring_window: List[datetime] = []
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            if self.state == CircuitState.CLOSED:
                self._cleanup_old_entries()
                return True

            if self.state == CircuitState.OPEN:
                if datetime.now() >= self.next_attempt:
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_successes = 0
                    return True
                return False

            if self.state == CircuitState.HALF_OPEN:
                return self.half_open_successes < self.config.half_open_requests
            return False

    def record_success(self):
        with self.lock:
            if self.state == CircuitState.CLOSED:
                self.failure_count = 0
            elif self.state == CircuitState.HALF_OPEN:
                self.half_open_successes += 1
                if self.half_open_successes >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0

    def record_failure(self):
        with self.lock:
            self.last_failure = datetime.now()
            self.monitoring_window.append(self.last_failure)
            self.failure_count += 1
            self.success_count = 0
            self._cleanup_old_entries()

            if self.state == CircuitState.CLOSED:
                if self.failure_count >= self.config.failure_threshold:
                    self.state = CircuitState.OPEN
                    self.next_attempt = datetime.now() + timedelta(seconds=self.config.timeout_seconds)
            elif self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                self.next_attempt = datetime.now() + timedelta(seconds=self.config.timeout_seconds)

    def _cleanup_old_entries(self):
        cutoff = datetime.now() - timedelta(seconds=self.config.monitoring_window_seconds)
        self.monitoring_window = [t for t in self.monitoring_window if t >= cutoff]
        self.failure_count = len(self.monitoring_window)

    def get_state(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "state": self.state.value,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "last_failure": self.last_failure.isoformat() if self.last_failure else None,
                "next_attempt": self.next_attempt.isoformat() if self.next_attempt else None,
                "half_open_successes": self.half_open_successes
            }


class InMemoryCache:
    def __init__(self, max_size_mb: int, default_ttl_seconds: int):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}
        self.current_size_bytes = 0
        self.lock = threading.Lock()
        self.stats = {"hits": 0, "misses": 0, "evictions": 0}

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            entry = self._store.get(key)
            if not entry:
                self.stats["misses"] += 1
                return None
            if datetime.now() >= entry["expires_at"]:
                self._remove(key)
                self.stats["misses"] += 1
                return None
            self.stats["hits"] += 1
            return entry["value"]

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds or self.default_ttl
        size = len(json.dumps(value, default=str).encode("utf-8"))
        with self.lock:
            if key in self._store:
                self.current_size_bytes -= self._store[key]["size"]
            elif self.current_size_bytes + size > self.max_size_bytes:
                self._evict(size)
            self._store[key] = {
                "value": value,
                "expires_at": datetime.now() + timedelta(seconds=ttl),
                "size": size,
                "created_at": datetime.now()
            }
            self.current_size_bytes += size

    def _remove(self, key: str):
        entry = self._store.pop(key, None)
        if entry:
            self.current_size_bytes -= entry["size"]

    def _evict(self, needed_bytes: int):
        keys_by_priority = sorted(
            self._store.keys(),
            key=lambda k: self._store[k]["created_at"]
        )
        freed = 0
        for key in keys_by_priority:
            freed += self._store[key]["size"]
            self._remove(key)
            self.stats["evictions"] += 1
            if freed >= needed_bytes:
                break

    def invalidate(self, pattern: str):
        regex = re.compile(pattern.replace("*", ".*"))
        with self.lock:
            to_remove = [k for k in self._store if regex.match(k)]
            for key in to_remove:
                self._remove(key)

    def clear(self):
        with self.lock:
            self._store.clear()
            self.current_size_bytes = 0

    def get_stats(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "size_bytes": self.current_size_bytes,
                "size_mb": round(self.current_size_bytes / (1024 * 1024), 2),
                "max_size_mb": self.max_size_bytes / (1024 * 1024),
                "key_count": len(self._store),
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "evictions": self.stats["evictions"],
                "hit_rate": round(self.stats["hits"] / max(1, self.stats["hits"] + self.stats["misses"]), 4)
            }


class UpstreamPool:
    def __init__(self, strategy: LoadBalancingStrategy):
        self.strategy = strategy
        self.servers: Dict[str, UpstreamServer] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.lock = threading.Lock()
        self._round_robin_index = 0

    def add_server(self, server: UpstreamServer):
        with self.lock:
            self.servers[server.url] = server
            self.circuit_breakers[server.url] = CircuitBreaker(CircuitBreakerConfig())

    def remove_server(self, url: str):
        with self.lock:
            self.servers.pop(url, None)
            self.circuit_breakers.pop(url, None)

    def get_server(self, identifier: str = "") -> Optional[UpstreamServer]:
        with self.lock:
            healthy = {k: v for k, v in self.servers.items() if v.is_healthy}
            if not healthy:
                return None
            if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
                return self._round_robin(healthy)
            if self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
                return self._weighted_round_robin(healthy)
            if self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
                return min(healthy.values(), key=lambda s: s.current_connections)
            if self.strategy == LoadBalancingStrategy.IP_HASH:
                return self._ip_hash(healthy, identifier)
            if self.strategy == LoadBalancingStrategy.CONSISTENT_HASH:
                return self._consistent_hash(healthy, identifier)
            if self.strategy == LoadBalancingStrategy.RANDOM:
                return random.choice(list(healthy.values()))
            return list(healthy.values())[0]

    def _round_robin(self, servers: Dict[str, UpstreamServer]) -> UpstreamServer:
        values = list(servers.values())
        server = values[self._round_robin_index % len(values)]
        self._round_robin_index += 1
        return server

    def _weighted_round_robin(self, servers: Dict[str, UpstreamServer]) -> UpstreamServer:
        server_list = list(servers.values())
        total_weight = sum(s.weight for s in server_list)
        if total_weight == 0:
            return server_list[0]
        random_weight = hash(str(time.time())) % total_weight
        current_weight = 0
        for server in server_list:
            current_weight += server.weight
            if current_weight >= random_weight:
                return server
        return server_list[-1]

    def _ip_hash(self, servers: Dict[str, UpstreamServer], identifier: str) -> UpstreamServer:
        if not identifier:
            return list(servers.values())[0]
        hash_val = int(hashlib.md5(identifier.encode()).hexdigest(), 16)
        server_list = list(servers.values())
        return server_list[hash_val % len(server_list)]

    def _consistent_hash(self, servers: Dict[str, UpstreamServer], identifier: str) -> UpstreamServer:
        if not identifier:
            return list(servers.values())[0]
        hash_val = int(hashlib.md5(identifier.encode()).hexdigest(), 16)
        server_list = list(servers.values())
        return server_list[hash_val % len(server_list)]

    def record_success(self, url: str):
        with self.lock:
            if url in self.servers:
                self.servers[url].success_count += 1
                self.servers[url].failure_count = 0
            if url in self.circuit_breakers:
                self.circuit_breakers[url].record_success()

    def record_failure(self, url: str):
        with self.lock:
            if url in self.servers:
                self.servers[url].failure_count += 1
            if url in self.circuit_breakers:
                self.circuit_breakers[url].record_failure()

    def get_circuit_breaker_state(self, url: str) -> Dict[str, Any]:
        with self.lock:
            cb = self.circuit_breakers.get(url)
            return cb.get_state() if cb else {"state": "unknown"}


class ResponseTransformer:
    def __init__(self):
        self.transformers: Dict[str, Callable] = {
            "json_to_xml": self._json_to_xml,
            "uppercase": self._uppercase_fields,
            "lowercase": self._lowercase_fields,
            "rename_fields": self._rename_fields,
            "add_fields": self._add_fields,
            "remove_fields": self._remove_fields,
            "map_values": self._map_values,
            "xml_to_json": self._xml_to_json,
            "base64_encode": self._base64_encode,
            "base64_decode": self._base64_decode,
            "mask_fields": self._mask_fields,
            "trim_fields": self._trim_fields,
        }

    def transform(self, body: Any, transform_config: Optional[Dict]) -> Any:
        if not transform_config:
            return body
        transform_type = transform_config.get("type")
        if transform_type and transform_type in self.transformers:
            return self.transformers[transform_type](body, transform_config)
        return body

    def _json_to_xml(self, body: Any, config: Dict) -> str:
        if isinstance(body, str):
            body = json.loads(body)
        root = config.get("root_element", "root")
        item = config.get("item_element", "item")
        xml = f"<{root}>"
        if isinstance(body, list):
            for entry in body:
                xml += f"<{item}>{json.dumps(entry)}</{item}>"
        elif isinstance(body, dict):
            for key, value in body.items():
                xml += f"<{key}>{value}</{key}>"
        xml += f"</{root}>"
        return xml

    def _xml_to_json(self, body: Any, config: Dict) -> Dict:
        if isinstance(body, dict):
            return body
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(body)
            result = {}
            for child in root:
                result[child.tag] = child.text
            return result
        except Exception:
            return {"raw_xml": str(body)}

    def _uppercase_fields(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            for field in config.get("fields", []):
                if field in body and isinstance(body[field], str):
                    body[field] = body[field].upper()
        return body

    def _lowercase_fields(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            for field in config.get("fields", []):
                if field in body and isinstance(body[field], str):
                    body[field] = body[field].lower()
        return body

    def _rename_fields(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            mappings = config.get("mappings", {})
            for old_name, new_name in mappings.items():
                if old_name in body:
                    body[new_name] = body.pop(old_name)
        return body

    def _add_fields(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            body.update(config.get("fields", {}))
        return body

    def _remove_fields(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            for field in config.get("fields", []):
                body.pop(field, None)
        return body

    def _map_values(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            for field, mapping in config.get("mappings", {}).items():
                if field in body and body[field] in mapping:
                    body[field] = mapping[body[field]]
        return body

    def _base64_encode(self, body: Any, config: Dict) -> str:
        import base64
        return base64.b64encode(json.dumps(body).encode()).decode()

    def _base64_decode(self, body: Any, config: Dict) -> Any:
        import base64
        return json.loads(base64.b64decode(body).decode())

    def _mask_fields(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            for field in config.get("fields", []):
                if field in body:
                    body[field] = "*" * len(str(body[field]))
        return body

    def _trim_fields(self, body: Any, config: Dict) -> Any:
        if isinstance(body, dict):
            for field in config.get("fields", []):
                if field in body and isinstance(body[field], str):
                    body[field] = body[field].strip()
        return body


class RequestValidator:
    def __init__(self):
        self.max_request_size = 10 * 1024 * 1024
        self.allowed_content_types = [
            "application/json",
            "application/xml",
            "multipart/form-data",
            "application/x-www-form-urlencoded",
            "text/plain",
            "text/html",
            "application/octet-stream",
        ]
        self.ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    def validate(self, method: str, path: str, headers: Dict, body: Any, endpoint: EndpointConfig) -> Dict[str, Any]:
        errors = []
        warnings = []

        if not self._validate_method(method, endpoint.methods):
            errors.append(f"Method {method} not allowed for {path}")

        content_length = headers.get("content-length", 0)
        try:
            length = int(content_length) if content_length else 0
        except (ValueError, TypeError):
            length = 0

        if length > endpoint.max_request_size_bytes:
            errors.append(f"Request body size {length} exceeds maximum {endpoint.max_request_size_bytes} bytes")

        if endpoint.validate_request_body:
            body_errors = self._validate_body(headers.get("content-type"), body)
            errors.extend(body_errors)

        if endpoint.cors_enabled:
            origin = headers.get("origin", "")
            if origin and endpoint.cors_origins and "*" not in endpoint.cors_origins and origin not in endpoint.cors_origins:
                errors.append(f"CORS origin {origin} not allowed")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def _validate_method(self, method: str, allowed: List[HTTPMethod]) -> bool:
        if HTTPMethod.ANY in allowed:
            return True
        return any(m.value == method for m in allowed)

    def _validate_body(self, content_type: Optional[str], body: Any) -> List[str]:
        errors = []
        if not content_type:
            errors.append("Content-Type header is required")
        elif content_type not in self.allowed_content_types:
            errors.append(f"Unsupported Content-Type: {content_type}")
        return errors

    def validate_ip(self, ip: str) -> bool:
        return bool(self.ip_pattern.match(ip))


class GatewayAnalytics:
    def __init__(self):
        self.total_requests = 0
        self.total_errors = 0
        self.total_latency_ms = 0
        self.requests_by_endpoint: Dict[str, int] = defaultdict(int)
        self.requests_by_status: Dict[int, int] = defaultdict(int)
        self.requests_by_auth_type: Dict[str, int] = defaultdict(int)
        self.errors_by_type: Dict[str, int] = defaultdict(int)
        self.rate_limit_hits = 0
        self.circuit_breaker_trips = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.auth_failures = 0
        self.request_sizes_bytes = 0
        self.response_sizes_bytes = 0
        self.start_time = datetime.now()
        self.lock = threading.Lock()
        self.recent_requests: List[Dict[str, Any]] = []
        self.max_recent = 1000

    def record_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        latency_ms: int,
        auth_type: str,
        cached: bool = False,
        request_size_bytes: int = 0,
        response_size_bytes: int = 0,
        error_type: Optional[str] = None,
    ):
        with self.lock:
            self.total_requests += 1
            self.total_latency_ms += latency_ms
            self.requests_by_endpoint[f"{method} {endpoint}"] += 1
            self.requests_by_status[status_code] += 1
            self.requests_by_auth_type[auth_type] += 1
            self.request_sizes_bytes += request_size_bytes
            self.response_sizes_bytes += response_size_bytes
            if cached:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
            if status_code >= 400:
                self.total_errors += 1
                if error_type:
                    self.errors_by_type[error_type] += 1
            self.recent_requests.append({
                "method": method, "endpoint": endpoint, "status": status_code,
                "latency_ms": latency_ms, "timestamp": datetime.now().isoformat()
            })
            if len(self.recent_requests) > self.max_recent:
                self.recent_requests = self.recent_requests[-self.max_recent:]

    def record_rate_limit_hit(self):
        with self.lock:
            self.rate_limit_hits += 1

    def record_circuit_breaker_trip(self):
        with self.lock:
            self.circuit_breaker_trips += 1

    def record_auth_failure(self):
        with self.lock:
            self.auth_failures += 1

    def get_summary(self) -> Dict[str, Any]:
        with self.lock:
            uptime = (datetime.now() - self.start_time).total_seconds()
            total = max(1, self.total_requests)
            return {
                "summary": {
                    "total_requests": self.total_requests,
                    "total_errors": self.total_errors,
                    "error_rate": round(self.total_errors / total * 100, 2),
                    "average_latency_ms": round(self.total_latency_ms / total, 2),
                    "requests_per_second": round(self.total_requests / max(1, uptime), 2),
                    "uptime_seconds": round(uptime, 2),
                    "rate_limit_hits": self.rate_limit_hits,
                    "circuit_breaker_trips": self.circuit_breaker_trips,
                    "auth_failures": self.auth_failures,
                    "cache_hits": self.cache_hits,
                    "cache_misses": self.cache_misses,
                    "cache_hit_rate": round(self.cache_hits / max(1, self.cache_hits + self.cache_misses) * 100, 2),
                },
                "by_endpoint": dict(self.requests_by_endpoint),
                "by_status": dict(self.requests_by_status),
                "by_auth_type": dict(self.requests_by_auth_type),
                "by_error_type": dict(self.errors_by_type),
            }

    def get_report(self, period: str = "hour") -> Dict[str, Any]:
        summary = self.get_summary()
        return {"period": period, "generated_at": datetime.now().isoformat(), **summary}


class Plugin(ABC):
    @abstractmethod
    def on_request(self, request: RequestContext) -> RequestContext:
        pass

    @abstractmethod
    def on_response(self, request: RequestContext, response: ResponseContext) -> ResponseContext:
        pass

    @abstractmethod
    def on_error(self, request: RequestContext, error: Exception) -> ResponseContext:
        pass


class PluginManager:
    def __init__(self):
        self.plugins: List[Plugin] = []
        self.enabled = True

    def register_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)

    def unregister_plugin(self, plugin_class: type):
        self.plugins = [p for p in self.plugins if not isinstance(p, plugin_class)]

    def on_request(self, request: RequestContext) -> RequestContext:
        if not self.enabled:
            return request
        for plugin in self.plugins:
            request = plugin.on_request(request)
        return request

    def on_response(self, request: RequestContext, response: ResponseContext) -> ResponseContext:
        if not self.enabled:
            return response
        for plugin in self.plugins:
            response = plugin.on_response(request, response)
        return response

    def on_error(self, request: RequestContext, error: Exception) -> ResponseContext:
        for plugin in self.plugins:
            response = plugin.on_error(request, error)
        return ResponseContext(status_code=500, body={"error": str(error)})


class RateLimitMiddleware:
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.limiters: Dict[str, Union[TokenBucketRateLimiter, SlidingWindowRateLimiter, FixedWindowRateLimiter, LeakyBucketRateLimiter]] = {}
        self.lock = threading.Lock()

    def allow_request(self, identifier: str, endpoint: str = "") -> Dict[str, Any]:
        with self.lock:
            if any(identifier.startswith(ip) for ip in self.config.ip_whitelist):
                return {"allowed": True, "reason": "whitelisted", "remaining": float("inf")}
            if any(identifier.startswith(ip) for ip in self.config.ip_blacklist):
                return {"allowed": False, "reason": "blacklisted", "remaining": 0}

            endpoint_cfg = self.config.per_endpoint_limits.get(endpoint, {})
            user_cfg = self.config.per_user_limits.get(identifier, {})
            max_req = endpoint_cfg.get("requests", user_cfg.get("requests", self.config.default_requests_per_window))
            window = endpoint_cfg.get("window", user_cfg.get("window", self.config.default_window_seconds))

            limiter_key = f"{endpoint}:{identifier}:{max_req}:{window}"
            if limiter_key not in self.limiters:
                alg = self.config.algorithm
                if alg == RateLimitAlgorithm.TOKEN_BUCKET:
                    self.limiters[limiter_key] = TokenBucketRateLimiter(max_req, max_req / window)
                elif alg == RateLimitAlgorithm.SLIDING_WINDOW:
                    self.limiters[limiter_key] = SlidingWindowRateLimiter(max_req, window)
                elif alg == RateLimitAlgorithm.FIXED_WINDOW:
                    self.limiters[limiter_key] = FixedWindowRateLimiter(max_req, window)
                elif alg == RateLimitAlgorithm.LEAKY_BUCKET:
                    self.limiters[limiter_key] = LeakyBucketRateLimiter(max_req, max_req / window)

            limiter = self.limiters[limiter_key]
            allowed = limiter.allow_request()
            result = {
                "allowed": allowed,
                "reason": "rate_limited" if not allowed else "allowed",
                "remaining": limiter.get_remaining(),
                "limit": max_req,
                "window_seconds": window,
            }
            if not allowed and isinstance(limiter, TokenBucketRateLimiter):
                result["retry_after"] = round(limiter.get_reset_seconds(), 2)
            return result


class AuthMiddleware:
    def __init__(self, config: AuthConfig):
        self.config = config
        self.api_keys: Dict[str, APIKey] = {}

    def register_api_key(self, api_key: APIKey):
        self.api_keys[api_key.key_value] = api_key

    def revoke_api_key(self, key_value: str):
        self.api_keys.pop(key_value, None)

    def authenticate(self, request: RequestContext) -> Dict[str, Any]:
        auth_type = request.endpoint.auth_type if request.endpoint else AuthType.NONE

        if auth_type == AuthType.NONE:
            return {"authenticated": True, "user_id": "anonymous", "scopes": []}

        if auth_type == AuthType.API_KEY:
            return self._authenticate_api_key(request)
        if auth_type == AuthType.JWT:
            return self._authenticate_jwt(request)
        if auth_type == AuthType.BASIC:
            return self._authenticate_basic(request)
        if auth_type == AuthType.OAUTH2:
            return self._authenticate_oauth2(request)

        return {"authenticated": False, "error": "unsupported_auth_type"}

    def _authenticate_api_key(self, request: RequestContext) -> Dict[str, Any]:
        key_value = request.headers.get(self.config.api_key_header, "")
        if not key_value.startswith(self.config.api_key_prefix):
            return {"authenticated": False, "error": "invalid_api_key_format"}
        key = self.api_keys.get(key_value)
        if not key:
            return {"authenticated": False, "error": "api_key_not_found"}
        if not key.active:
            return {"authenticated": False, "error": "api_key_revoked"}
        if key.expires_at and datetime.now() >= key.expires_at:
            return {"authenticated": False, "error": "api_key_expired"}
        if key.ip_blacklist and request.client_ip in key.ip_blacklist:
            return {"authenticated": False, "error": "ip_blacklisted"}
        key.last_used = datetime.now()
        return {"authenticated": True, "user_id": key.owner, "scopes": key.scopes}

    def _authenticate_jwt(self, request: RequestContext) -> Dict[str, Any]:
        token = request.headers.get("authorization", "")
        if not token.startswith("Bearer "):
            return {"authenticated": False, "error": "missing_bearer_token"}
        token = token[7:]
        try:
            parts = token.split(".")
            if len(parts) < 2:
                return {"authenticated": False, "error": "invalid_token_format"}
            payload_b64 = parts[1] + "=" * (4 - len(parts[1]) % 4)
            import base64
            payload = json.loads(base64.b64decode(payload_b64).decode())
            exp = payload.get("exp", 0)
            if datetime.now().timestamp() > exp:
                return {"authenticated": False, "error": "token_expired"}
            return {
                "authenticated": True,
                "user_id": payload.get("sub", ""),
                "scopes": payload.get("scopes", []),
                "roles": payload.get("roles", []),
                "claims": payload
            }
        except Exception:
            return {"authenticated": False, "error": "token_validation_failed"}

    def _authenticate_basic(self, request: RequestContext) -> Dict[str, Any]:
        import base64
        auth = request.headers.get("authorization", "")
        if not auth.startswith("Basic "):
            return {"authenticated": False, "error": "missing_basic_auth"}
        try:
            decoded = base64.b64decode(auth[6:]).decode()
            username, password = decoded.split(":", 1)
            if username == "admin" and password == "admin":
                return {"authenticated": True, "user_id": username, "scopes": ["admin"]}
        except Exception:
            pass
        return {"authenticated": False, "error": "invalid_credentials"}

    def _authenticate_oauth2(self, request: RequestContext) -> Dict[str, Any]:
        token = request.headers.get("authorization", "")
        if not token.startswith("Bearer "):
            return {"authenticated": False, "error": "missing_oauth2_token"}
        return {"authenticated": True, "user_id": "oauth2_user", "scopes": ["read"]}


class APIGatewayAgent:
    """Enterprise-Grade API Gateway Agent."""

    def __init__(self, config: Optional[GatewayConfig] = None):
        self._config = config or GatewayConfig()
        self._endpoints: Dict[str, EndpointConfig] = {}
        self._upstream_pools: Dict[str, UpstreamPool] = {}
        self._rate_limit_middleware = RateLimitMiddleware(self._config.rate_limit_config)
        self._auth_middleware = AuthMiddleware(self._config.auth_config)
        self._response_transformer = ResponseTransformer()
        self._request_validator = RequestValidator()
        self._analytics = GatewayAnalytics()
        self._plugin_manager = PluginManager()
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._cache = InMemoryCache(
            max_size_mb=self._config.cache_config.max_cache_size_mb,
            default_ttl_seconds=self._config.cache_config.default_ttl_seconds,
        )
        self._request_id_counter = 0
        self._request_id_lock = threading.Lock()
        self._started = False

    def _generate_request_id(self) -> str:
        with self._request_id_lock:
            self._request_id_counter += 1
            return f"req-{uuid.uuid4().hex[:8]}-{self._request_id_counter}"

    def configure_gateway(self, config: GatewayConfig) -> Dict[str, Any]:
        self._config = config
        self._rate_limit_middleware = RateLimitMiddleware(config.rate_limit_config)
        self._auth_middleware = AuthMiddleware(config.auth_config)
        self._cache = InMemoryCache(
            max_size_mb=config.cache_config.max_cache_size_mb,
            default_ttl_seconds=config.cache_config.default_ttl_seconds,
        )
        for endpoint in config.endpoint_configs:
            self.register_endpoint(endpoint)
        return {"status": "configured", "name": config.name, "environment": config.environment.value,
                "endpoints_registered": len(self._endpoints)}

    def register_endpoint(self, endpoint: EndpointConfig) -> Dict[str, Any]:
        self._endpoints[endpoint.path] = endpoint
        pool = UpstreamPool(LoadBalancingStrategy.ROUND_ROBIN)
        self._upstream_pools[endpoint.path] = pool
        return {"status": "registered", "path": endpoint.path,
                "methods": [m.value for m in endpoint.methods],
                "upstream_url": endpoint.upstream_url, "auth_type": endpoint.auth_type.value}

    def add_upstream_server(self, endpoint_path: str, server: UpstreamServer) -> Dict[str, Any]:
        if endpoint_path not in self._upstream_pools:
            return {"status": "error", "message": f"Endpoint {endpoint_path} not found"}
        self._upstream_pools[endpoint_path].add_server(server)
        return {"status": "added", "endpoint": endpoint_path, "server_url": server.url, "weight": server.weight}

    def register_api_key(self, owner: str, scopes: List[str], rate_limit_override: Optional[int] = None,
                        expires_in_days: Optional[int] = None) -> APIKey:
        key_value = f"{self._config.auth_config.api_key_prefix}{uuid.uuid4().hex}"
        key = APIKey(
            key_id=self._generate_request_id(),
            key_value=key_value,
            owner=owner,
            scopes=scopes,
            rate_limit_override=rate_limit_override,
            expires_at=datetime.now() + timedelta(days=expires_in_days) if expires_in_days else None
        )
        self._auth_middleware.register_api_key(key)
        logger.info(f"Registered API key for {owner}")
        return key

    def configure_rate_limit(self, endpoint: str, requests_per_minute: int,
                             algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW) -> Dict[str, Any]:
        if endpoint in self._endpoints:
            self._endpoints[endpoint].rate_limit = requests_per_minute
            self._endpoints[endpoint].rate_limit_algorithm = algorithm
        return {"status": "configured", "endpoint": endpoint, "requests_per_minute": requests_per_minute,
                "algorithm": algorithm.value}

    def configure_auth(self, endpoint: str, auth_type: AuthType, **kwargs) -> Dict[str, Any]:
        if endpoint in self._endpoints:
            self._endpoints[endpoint].auth_type = auth_type
        return {"status": "configured", "endpoint": endpoint, "auth_type": auth_type.value}

    def add_route(self, path: str, methods: List[str], upstream_url: str,
                  auth_type: str = "none", rate_limit: int = 1000) -> Dict[str, Any]:
        endpoint = EndpointConfig(
            path=path,
            methods=[HTTPMethod(m) for m in methods],
            upstream_url=upstream_url,
            auth_type=AuthType(auth_type),
            rate_limit=rate_limit
        )
        return self.register_endpoint(endpoint)

    def create_upstream_pool(self, name: str, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN) -> Dict[str, Any]:
        self._upstream_pools[name] = UpstreamPool(strategy)
        return {"status": "created", "pool_name": name, "strategy": strategy.value}

    def register_plugin(self, plugin: Plugin) -> Dict[str, Any]:
        self._plugin_manager.register_plugin(plugin)
        return {"status": "registered", "plugin_type": type(plugin).__name__}

    def get_analytics(self, period: str = "hour") -> Dict[str, Any]:
        return self._analytics.get_report(period)

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "APIGatewayAgent",
            "name": self._config.name,
            "environment": self._config.environment.value,
            "status": "running" if self._started else "stopped",
            "endpoints_count": len(self._endpoints),
            "upstream_pools_count": len(self._upstream_pools),
            "plugins_count": len(self._plugin_manager.plugins),
            "cache_stats": self._cache.get_stats(),
            "analytics": self._analytics.get_summary()["summary"],
        }

    def get_statistics(self) -> Dict[str, Any]:
        stats = {
            "gateway": {"name": self._config.name, "environment": self._config.environment.value, "status": "running" if self._started else "stopped"},
            "endpoints": {},
            "upstream_pools": {},
            "circuit_breakers": {},
            "analytics": self._analytics.get_summary(),
            "cache": self._cache.get_stats(),
        }
        for path, ep in self._endpoints.items():
            stats["endpoints"][path] = {
                "methods": [m.value for m in ep.methods],
                "upstream_url": ep.upstream_url,
                "auth_type": ep.auth_type.value,
                "rate_limit": ep.rate_limit,
                "caching": ep.caching_enabled,
                "circuit_breaker": {"threshold": ep.circuit_breaker_threshold, "timeout": ep.circuit_breaker_timeout},
            }
        for name, pool in self._upstream_pools.items():
            stats["upstream_pools"][name] = {
                "strategy": pool.strategy.value,
                "servers_count": len(pool.servers),
                "servers": [{"url": s.url, "healthy": s.is_healthy, "weight": s.weight} for s in pool.servers.values()]
            }
        for url, pool in self._upstream_pools.items():
            for server_url, cb in pool.circuit_breakers.items():
                stats["circuit_breakers"][server_url] = cb.get_state()
        return stats

    def export_config(self) -> Dict[str, Any]:
        return {
            "config": {
                "name": self._config.name,
                "environment": self._config.environment.value,
                "host": self._config.host,
                "port": self._config.port,
                "endpoints": [
                    {
                        "path": ep.path,
                        "methods": [m.value for m in ep.methods],
                        "upstream_url": ep.upstream_url,
                        "auth_type": ep.auth_type.value,
                        "rate_limit": ep.rate_limit,
                        "timeout_ms": ep.timeout_ms,
                        "version": ep.version,
                        "cors_enabled": ep.cors_enabled,
                    }
                    for ep in self._endpoints.values()
                ],
            }
        }

    def import_config(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        endpoints = config_dict.get("config", {}).get("endpoints", [])
        imported = 0
        for ep_data in endpoints:
            try:
                ep = EndpointConfig(
                    path=ep_data["path"],
                    methods=[HTTPMethod(m) for m in ep_data["methods"]],
                    upstream_url=ep_data["upstream_url"],
                    auth_type=AuthType(ep_data.get("auth_type", "none")),
                    rate_limit=ep_data.get("rate_limit"),
                    timeout_ms=ep_data.get("timeout_ms", 30000),
                    version=ep_data.get("version", "v1"),
                )
                self.register_endpoint(ep)
                imported += 1
            except Exception as e:
                logger.error(f"Failed to import endpoint {ep_data}: {e}")
        return {"status": "imported", "endpoints_imported": imported}

    def validate_endpoint(self, method: str, path: str, headers: Dict, body: Any) -> Dict[str, Any]:
        endpoint = None
        for ep_path, ep_config in self._endpoints.items():
            if ep_config.matches_path(path):
                endpoint = ep_config
                break

        if not endpoint:
            return {"valid": False, "errors": [f"No endpoint found for {path}"], "status_code": 404}

        validation = self._request_validator.validate(method, path, headers, body, endpoint)
        return {**validation, "status_code": 400 if not validation["valid"] else 200}

    def health_check(self) -> Dict[str, Any]:
        healthy_upstreams = sum(
            1 for pool in self._upstream_pools.values()
            for server in pool.servers.values()
            if server.is_healthy
        )
        total_upstreams = sum(len(p.servers) for p in self._upstream_pools.values())

        return {
            "status": "healthy" if total_upstreams == 0 or healthy_upstreams > 0 else "degraded",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "endpoints": {"registered": len(self._endpoints), "healthy": "all"},
                "upstream_services": {"healthy": healthy_upstreams, "total": total_upstreams},
                "cache": self._cache.get_stats(),
                "rate_limiting": {"status": "active", "limiters": len(self._rate_limit_middleware.limiters)},
                "authentication": {"status": "active", "registered_keys": len(self._auth_middleware.api_keys)},
                "circuit_breakers": {"active": sum(len(p.circuit_breakers) for p in self._upstream_pools.values())},
                "analytics": {"status": "connected", "requests_logged": self._analytics.total_requests},
            }
        }

    def invalidate_cache(self, pattern: str) -> Dict[str, Any]:
        self._cache.invalidate(pattern)
        return {"status": "invalidated", "pattern": pattern}

    def clear_cache(self) -> Dict[str, Any]:
        self._cache.clear()
        return {"status": "cleared"}

    def get_cache_stats(self) -> Dict[str, Any]:
        return self._cache.get_stats()

    def update_upstream_health(self, upstream_url: str, is_healthy: bool) -> Dict[str, Any]:
        for pool in self._upstream_pools.values():
            if upstream_url in pool.servers:
                pool.servers[upstream_url].is_healthy = is_healthy
                pool.servers[upstream_url].last_health_check = datetime.now()
                return {"status": "updated", "server": upstream_url, "healthy": is_healthy}
        return {"status": "not_found", "server": upstream_url}

    def simulate_request(self, method: str, path: str, headers: Optional[Dict] = None,
                         body: Any = None, client_ip: str = "127.0.0.1") -> Dict[str, Any]:
        start = time.time()
        request_id = self._generate_request_id()
        headers = headers or {}

        endpoint = None
        for ep_path, ep_config in self._endpoints.items():
            if ep_config.matches_path(path):
                if ep_config.matches_method(method):
                    endpoint = ep_config
                    break

        if not endpoint:
            latency = int((time.time() - start) * 1000)
            self._analytics.record_request(path, method, 404, latency, "none", error_type="not_found")
            return {"request_id": request_id, "status": 404, "error": "Not Found", "latency_ms": latency}

        req_ctx = RequestContext(
            request_id=request_id, client_ip=client_ip, method=method, path=path,
            headers=headers, query_params={}, body=body, start_time=datetime.now(), endpoint=endpoint
        )

        req_ctx = self._plugin_manager.on_request(req_ctx)

        validation = self._request_validator.validate(method, path, headers, body, endpoint)
        if not validation["valid"]:
            latency = int((time.time() - start) * 1000)
            self._analytics.record_request(path, method, 400, latency, endpoint.auth_type.value, error_type="validation_error")
            return {"request_id": request_id, "status": 400, "errors": validation["errors"], "latency_ms": latency}

        if endpoint.auth_type != AuthType.NONE:
            auth_result = self._auth_middleware.authenticate(req_ctx)
            if not auth_result.get("authenticated"):
                latency = int((time.time() - start) * 1000)
                self._analytics.record_auth_failure()
                self._analytics.record_request(path, method, 401, latency, endpoint.auth_type.value, error_type="auth_failure")
                return {"request_id": request_id, "status": 401, "error": auth_result.get("error", "Unauthorized"), "latency_ms": latency}
            req_ctx.authenticated = True
            req_ctx.user_id = auth_result.get("user_id")

        rate_limit_result = self._rate_limit_middleware.allow_request(req_ctx.client_ip, path)
        if not rate_limit_result["allowed"]:
            latency = int((time.time() - start) * 1000)
            self._analytics.record_rate_limit_hit()
            self._analytics.record_request(path, method, 429, latency, endpoint.auth_type.value, error_type="rate_limit")
            return {
                "request_id": request_id, "status": 429, "error": "Rate limit exceeded",
                "latency_ms": latency, "retry_after": rate_limit_result.get("retry_after", endpoint.rate_limit_window)
            }

        upstream_pool = self._upstream_pools.get(path)
        upstream_server = upstream_pool.get_server(req_ctx.client_ip) if upstream_pool else None
        if not upstream_server:
            latency = int((time.time() - start) * 1000)
            self._analytics.record_request(path, method, 503, latency, endpoint.auth_type.value, error_type="no_upstream")
            return {"request_id": request_id, "status": 503, "error": "Service Unavailable", "latency_ms": latency}

        req_ctx.upstream_server = upstream_server
        upstream_pool.record_success(upstream_server.url) if random.random() > 0.1 else upstream_pool.record_failure(upstream_server.url)
        upstream_server.current_connections += 1

        try:
            if endpoint.caching_enabled and method == "GET":
                cache_key = f"{method}:{path}:{hashlib.sha256(str(body).encode()).hexdigest()}"
                cached_response = self._cache.get(cache_key)
                if cached_response:
                    latency = int((time.time() - start) * 1000)
                    self._analytics.record_request(path, method, cached_response.get("status_code", 200),
                                                   latency, endpoint.auth_type.value, cached=True)
                    response = ResponseContext(**cached_response, from_cache=True, cached=True, latency_ms=latency)
                    response.headers["X-Cache"] = "HIT"
                    response.headers["X-Cache-Key"] = cache_key[:16]
                    return response.to_dict() if hasattr(response, 'to_dict') else {
                        "request_id": request_id, "status": response.status_code, "body": response.body,
                        "headers": response.headers, "latency_ms": latency, "cached": True,
                    }

            response_status = 200 if method in ["GET", "HEAD", "OPTIONS"] else 201
            response_body = {"message": f"{method} {path} succeeded via {upstream_server.url}",
                             "upstream": upstream_server.url, "user_id": req_ctx.user_id}

            if endpoint.response_transform:
                response_body = self._response_transformer.transform(response_body, endpoint.response_transform)

            latency = int((time.time() - start) * 1000)
            self._analytics.record_request(path, method, response_status, latency, endpoint.auth_type.value)

            if endpoint.caching_enabled and method == "GET":
                self._cache.set(cache_key, {"status_code": response_status, "body": response_body, "headers": {}}, ttl_seconds=endpoint.cache_ttl_seconds)

            return {
                "request_id": request_id, "status": response_status, "body": response_body,
                "latency_ms": latency, "upstream": upstream_server.url, "cached": False,
                "headers": {"X-Cache": "MISS", "X-Request-ID": request_id}
            }
        finally:
            upstream_server.current_connections = max(0, upstream_server.current_connections - 1)

    def start(self) -> Dict[str, Any]:
        self._started = True
        logger.info(f"API Gateway {self._config.name} started on {self._config.host}:{self._config.port}")
        return {"status": "started", "name": self._config.name, "timestamp": datetime.now().isoformat()}

    def stop(self) -> Dict[str, Any]:
        self._started = False
        logger.info(f"API Gateway {self._config.name} stopped")
        return {"status": "stopped", "name": self._config.name, "timestamp": datetime.now().isoformat()}


def main():
    print("\n" + "=" * 60)
    print("  API Gateway Agent")
    print("  Enterprise-Grade Gateway Management")
    print("=" * 60 + "\n")

    gateway = APIGatewayAgent()

    config = GatewayConfig(
        name="production-gateway",
        environment=GatewayEnvironment.PRODUCTION,
        host="0.0.0.0",
        port=8080,
        endpoint_configs=[
            EndpointConfig(
                path="/api/v1/users", methods=[HTTPMethod.GET, HTTPMethod.POST],
                upstream_url="http://user-service:8080", auth_type=AuthType.JWT,
                rate_limit=100, rate_limit_window=60, caching_enabled=True, cache_ttl_seconds=300,
                cors_enabled=True, cors_origins=["https://app.example.com", "https://admin.example.com"],
                description="User management endpoints", version="v1", tags=["users", "core"]
            ),
            EndpointConfig(
                path="/api/v1/orders", methods=[HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT],
                upstream_url="http://order-service:8080", auth_type=AuthType.JWT,
                rate_limit=50, rate_limit_window=60, timeout_ms=10000, retries=3,
                caching_enabled=False, cors_enabled=True,
                description="Order processing endpoints", version="v1", tags=["orders", "core"]
            ),
            EndpointConfig(
                path="/api/public/health", methods=[HTTPMethod.GET],
                upstream_url="http://internal:8080/health", auth_type=AuthType.NONE,
                rate_limit=1000, caching_enabled=True, cache_ttl_seconds=10,
                description="Public health check", version="v1", tags=["health", "public"]
            ),
        ],
        rate_limit_config=RateLimitConfig(default_requests_per_window=1000, default_window_seconds=60,
                                          ip_whitelist=["10.0.0.0/8", "192.168.1.0/24"], ip_blacklist=["192.168.1.100"]),
        auth_config=AuthConfig(jwt_secret="my-super-secret-key", jwt_expiry_hours=24, allowed_scopes=["read", "write", "admin"]),
        circuit_breaker_config=CircuitBreakerConfig(failure_threshold=5, success_threshold=2, timeout_seconds=60),
        cache_config=CacheConfig(enabled=True, default_ttl_seconds=300, max_cache_size_mb=100, storage_type="memory"),
        logging_config=LoggingConfig(level=LoggingLevel.INFO, format="json", include_headers=True, log_requests=True),
        tls_config=TLSConfig(enabled=True, min_version="TLSv1.2", enable_mtls=False),
    )
    gateway.configure_gateway(config)

    keys = []
    for user in ["alice", "bob", "charlie"]:
        key = gateway.register_api_key(owner=user, scopes=["read", "write"], rate_limit_override=500)
        keys.append(key.key_value)
        print(f"Registered API key: {key.key_value[:20]}... ({key.owner})")

    gateway.start()
    print(f"\nGateway {config.name} started on {config.host}:{config.port}")
    print(f"Environment: {config.environment.value}")
    print(f"Registered endpoints: {len(config.endpoint_configs)}")

    print("\n" + "=" * 60)
    print("Simulated Requests:")
    print("=" * 60)

    test_paths = [
        ("GET", "/api/v1/users", {"authorization": "Bearer eyJzdWIiOiJhbGljZSJ9.signature", "x-api-key": keys[0]}),
        ("GET", "/api/v1/users", {"authorization": "Bearer eyJzdWIiOiJib2IifQ.signature", "x-api-key": keys[1]}),
        ("POST", "/api/v1/orders", {"authorization": f"Bearer eyJzdWIiOiJjaGFybGllJ30.signature", "x-api-key": keys[2]},
         '{"product_id": 123, "quantity": 2}'),
        ("GET", "/api/public/health", {}),
        ("GET", "/api/v1/unknown", {"authorization": "Bearer eyJzdWIiOiJhbGljZSJ9.signature"}),
    ]

    for req in test_paths:
        if len(req) == 4:
            method, path, headers, body = req
        else:
            method, path, headers = req
            body = None
        result = gateway.simulate_request(method, path, headers=headers, body=body)
        print(f"\n  {method} {path}")
        print(f"    Status: {result['status']}")
        print(f"    Latency: {result.get('latency_ms', 0)}ms")
        print(f"    Upstream: {result.get('upstream', 'N/A')}")
        print(f"    Cached: {result.get('cached', False)}")
        if result.get("error"):
            print(f"    Error: {result['error']}")

    pool = gateway._upstream_pools.get("/api/v1/users")
    if pool:
        unhealthy = [url for url, server in pool.servers.items() if not server.is_healthy]
        gateway.update_upstream_health(list(pool.servers.keys())[0], False)
        healthy_update = gateway.update_upstream_health(list(pool.servers.keys())[0], True)
        print(f"\nUpstream health updated: {healthy_update}")

    print("\n" + "=" * 60)
    print("Gateway Status:")
    status = gateway.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    cache_stats = gateway.get_cache_stats()
    print(f"\nCache: {cache_stats['size_mb']}MB | keys: {cache_stats['key_count']} | hit_rate: {cache_stats['hit_rate']}")

    analytics = gateway.get_analytics()
    print(f"\nAnalytics: {analytics['summary']['total_requests']} requests | {analytics['summary']['error_rate']}% error rate")

    exported = gateway.export_config()
    print(f"\nExported config: {json.dumps(exported, indent=2)[:500]}...")

    imported = gateway.import_config(exported)
    print(f"\nImport result: {imported}")

    print("\n" + "=" * 60)
    print("Demo completed.")


if __name__ == "__main__":
    main()
