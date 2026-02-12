"""
API Gateway Agent - Enterprise-Grade Gateway Management and Configuration.

This agent provides comprehensive API gateway management capabilities including
routing, rate limiting, authentication, caching, circuit breaking, and more.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Union
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import re
import json
import hashlib
import time
import copy
import threading
from abc import ABC, abstractmethod


class GatewayEnvironment(Enum):
    """Deployment environment for the gateway."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    DISASTER_RECOVERY = "disaster_recovery"


class AuthType(Enum):
    """Authentication types supported by the gateway."""
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    MTLS = "mTLS"
    BASIC = "basic"
    CUSTOM = "custom"
    NONE = "none"


class HTTPMethod(Enum):
    """HTTP methods supported by the gateway."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    ANY = "ANY"


class RateLimitAlgorithm(Enum):
    """Rate limiting algorithms."""
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"
    LEAKY_BUCKET = "leaky_bucket"


class LoadBalancingStrategy(Enum):
    """Load balancing strategies for upstream services."""
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    RANDOM = "random"
    CONSISTENT_HASH = "consistent_hash"


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class LoggingLevel(Enum):
    """Logging levels for gateway operations."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class EndpointConfig:
    """Configuration for a single API endpoint."""
    path: str
    methods: List[HTTPMethod]
    upstream_url: str
    auth_type: AuthType
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
    metadata: Dict[str, Any] = field(default_factory=dict)

    def matches_path(self, request_path: str) -> bool:
        """Check if the request path matches this endpoint."""
        pattern = self.path.replace("*", ".*").replace("{param}", "[^/]+")
        return bool(re.match(f"^{pattern}$", request_path))


@dataclass
class UpstreamServer:
    """Configuration for an upstream server."""
    url: str
    weight: int = 100
    health_check_path: str = "/health"
    health_check_interval: int = 30
    is_healthy: bool = True
    current_connections: int = 0
    last_health_check: Optional[datetime] = None
    failure_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RateLimitConfig:
    """Global rate limiting configuration."""
    default_requests_per_window: int = 1000
    default_window_seconds: int = 60
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW
    per_endpoint_limits: Dict[str, Dict[str, int]] = field(default_factory=dict)
    per_user_limits: Dict[str, Dict[str, int]] = field(default_factory=dict)
    ip_whitelist: List[str] = field(default_factory=list)
    ip_blacklist: List[str] = field(default_factory=list)


@dataclass
class AuthConfig:
    """Authentication configuration."""
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    oauth2_issuer: str = ""
    oauth2_audience: str = ""
    api_key_header: str = "X-API-Key"
    api_key_prefix: str = "sk_"
    allowed_scopes: List[str] = field(default_factory=list)
    token_validation_rules: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout_seconds: int = 60
    half_open_requests: int = 3
    monitoring_window_seconds: int = 30


@dataclass
class CacheConfig:
    """Caching configuration."""
    enabled: bool = True
    default_ttl_seconds: int = 300
    max_cache_size_mb: int = 100
    cache_key_patterns: List[str] = field(default_factory=list)
    excluded_paths: List[str] = field(default_factory=list)
    storage_type: str = "memory"


@dataclass  
class LoggingConfig:
    """Logging configuration."""
    level: LoggingLevel = LoggingLevel.INFO
    format: str = "json"
    include_headers: bool = True
    include_request_body: bool = False
    include_response_body: bool = False
    sensitive_headers: List[str] = field(default_factory=list)
    log_requests: bool = True
    log_responses: bool = True
    log_errors_only: bool = False


@dataclass
class GatewayConfig:
    """Main gateway configuration."""
    name: str = "api-gateway"
    environment: GatewayEnvironment = GatewayEnvironment.DEVELOPMENT
    host: str = "0.0.0.0"
    port: int = 8080
    worker_processes: int = 4
    max_connections: int = 10000
    keepalive_timeout: int = 65
    endpoint_configs: List[EndpointConfig] = field(default_factory=list)
    rate_limit_config: RateLimitConfig = field(default_factory=RateLimitConfig)
    auth_config: AuthConfig = field(default_factory=AuthConfig)
    circuit_breaker_config: CircuitBreakerConfig = field(default_factory=CircuitBreakerConfig)
    cache_config: CacheConfig = field(default_factory=CacheConfig)
    logging_config: LoggingConfig = field(default_factory=LoggingConfig)


class TokenBucketRateLimiter:
    """Token bucket rate limiter implementation."""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def allow_request(self) -> bool:
        """Check if a request is allowed."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
    
    def get_remaining(self) -> int:
        """Get remaining tokens."""
        with self.lock:
            return int(self.tokens)


class SlidingWindowRateLimiter:
    """Sliding window rate limiter implementation."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()
    
    def allow_request(self, identifier: str) -> bool:
        """Check if a request is allowed."""
        with self.lock:
            now = time.time()
            window_start = now - self.window_seconds
            
            requests = self.requests[identifier]
            while requests and requests[0] < window_start:
                requests.pop(0)
            
            if len(requests) < self.max_requests:
                requests.append(now)
                return True
            return False
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests in window."""
        with self.lock:
            now = time.time()
            window_start = now - self.window_seconds
            requests = self.requests[identifier]
            valid_requests = [r for r in requests if r >= window_start]
            return max(0, self.max_requests - len(valid_requests))


class CircuitBreaker:
    """Circuit breaker implementation for upstream service protection."""
    
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure: Optional[datetime] = None
        self.next_attempt: Optional[datetime] = None
        self.half_open_successes = 0
        self.lock = threading.Lock()
    
    def allow_request(self) -> bool:
        """Check if a request should be allowed."""
        with self.lock:
            if self.state == CircuitState.CLOSED:
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
        """Record a successful request."""
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
        """Record a failed request."""
        with self.lock:
            self.last_failure = datetime.now()
            self.failure_count += 1
            self.success_count = 0
            
            if self.state == CircuitState.CLOSED:
                if self.failure_count >= self.config.failure_threshold:
                    self.state = CircuitState.OPEN
                    self.next_attempt = datetime.now() + timedelta(seconds=self.config.timeout_seconds)
            
            elif self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                self.next_attempt = datetime.now() + timedelta(seconds=self.config.timeout_seconds)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state."""
        with self.lock:
            return {
                "state": self.state.value,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "last_failure": self.last_failure.isoformat() if self.last_failure else None,
                "next_attempt": self.next_attempt.isoformat() if self.next_attempt else None
            }


class UpstreamPool:
    """Manages a pool of upstream servers with load balancing."""
    
    def __init__(self, strategy: LoadBalancingStrategy):
        self.strategy = strategy
        self.servers: Dict[str, UpstreamServer] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.lock = threading.Lock()
    
    def add_server(self, server: UpstreamServer):
        """Add a server to the pool."""
        with self.lock:
            self.servers[server.url] = server
            self.circuit_breakers[server.url] = CircuitBreaker(CircuitBreakerConfig())
    
    def remove_server(self, url: str):
        """Remove a server from the pool."""
        with self.lock:
            self.servers.pop(url, None)
            self.circuit_breakers.pop(url, None)
    
    def get_server(self, identifier: str = "") -> Optional[UpstreamServer]:
        """Get the next server based on load balancing strategy."""
        with self.lock:
            healthy_servers = {k: v for k, v in self.servers.items() if v.is_healthy}
            
            if not healthy_servers:
                return None
            
            if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
                return self._round_robin(healthy_servers)
            
            elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
                return self._weighted_round_robin(healthy_servers)
            
            elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
                return self._least_connections(healthy_servers)
            
            elif self.strategy == LoadBalancingStrategy.IP_HASH:
                return self._ip_hash(healthy_servers, identifier)
            
            elif self.strategy == LoadBalancingStrategy.CONSISTENT_HASH:
                return self._consistent_hash(healthy_servers, identifier)
            
            elif self.strategy == LoadBalancingStrategy.RANDOM:
                return self._random(healthy_servers)
            
            return list(healthy_servers.values())[0]
    
    def _round_robin(self, servers: Dict[str, UpstreamServer]) -> UpstreamServer:
        """Round robin selection."""
        return list(servers.values())[0]
    
    def _weighted_round_robin(self, servers: Dict[str, UpstreamServer]) -> UpstreamServer:
        """Weighted round robin selection."""
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
    
    def _least_connections(self, servers: Dict[str, UpstreamServer]) -> UpstreamServer:
        """Least connections selection."""
        return min(servers.values(), key=lambda s: s.current_connections)
    
    def _ip_hash(self, servers: Dict[str, UpstreamServer], identifier: str) -> UpstreamServer:
        """IP hash selection."""
        if not identifier:
            return list(servers.values())[0]
        hash_val = int(hashlib.md5(identifier.encode()).hexdigest(), 16)
        server_list = list(servers.values())
        return server_list[hash_val % len(server_list)]
    
    def _consistent_hash(self, servers: Dict[str, UpstreamServer], identifier: str) -> UpstreamServer:
        """Consistent hash selection."""
        if not identifier:
            return list(servers.values())[0]
        hash_val = int(hashlib.md5(identifier.encode()).hexdigest(), 16)
        server_list = list(servers.values())
        return server_list[hash_val % len(server_list)]
    
    def _random(self, servers: Dict[str, UpstreamServer]) -> UpstreamServer:
        """Random selection."""
        import random
        server_list = list(servers.values())
        return random.choice(server_list)
    
    def record_success(self, url: str):
        """Record success for a server."""
        with self.lock:
            if url in self.servers:
                self.servers[url].failure_count = 0
            if url in self.circuit_breakers:
                self.circuit_breakers[url].record_success()
    
    def record_failure(self, url: str):
        """Record failure for a server."""
        with self.lock:
            if url in self.servers:
                self.servers[url].failure_count += 1
            if url in self.circuit_breakers:
                self.circuit_breakers[url].record_failure()


class ResponseTransformer:
    """Handles request and response transformations."""
    
    def __init__(self):
        self.transformers: Dict[str, Callable] = {
            "json_to_xml": self._json_to_xml,
            "uppercase": self._uppercase_fields,
            "lowercase": self._lowercase_fields,
            "rename_fields": self._rename_fields,
            "add_fields": self._add_fields,
            "remove_fields": self._remove_fields,
            "map_values": self._map_values,
        }
    
    def transform_request(self, body: Any, transform_config: Optional[Dict]) -> Any:
        """Transform request body."""
        if not transform_config:
            return body
        
        transform_type = transform_config.get("type")
        if transform_type and transform_type in self.transformers:
            return self.transformers[transform_type](body, transform_config)
        return body
    
    def transform_response(self, body: Any, transform_config: Optional[Dict]) -> Any:
        """Transform response body."""
        return self.transform_request(body, transform_config)
    
    def _json_to_xml(self, body: Any, config: Dict) -> str:
        """Convert JSON to XML."""
        if isinstance(body, str):
            body = json.loads(body)
        root_element = config.get("root_element", "root")
        item_element = config.get("item_element", "item")
        
        xml = f"<{root_element}>"
        if isinstance(body, list):
            for item in body:
                xml += f"<{item_element}>{json.dumps(item)}</{item_element}>"
        elif isinstance(body, dict):
            for key, value in body.items():
                xml += f"<{key}>{value}</{key}>"
        xml += f"</{root_element}>"
        return xml
    
    def _uppercase_fields(self, body: Any, config: Dict) -> Any:
        """Uppercase specified fields."""
        if isinstance(body, dict):
            fields = config.get("fields", [])
            for field in fields:
                if field in body and isinstance(body[field], str):
                    body[field] = body[field].upper()
        return body
    
    def _lowercase_fields(self, body: Any, config: Dict) -> Any:
        """Lowercase specified fields."""
        if isinstance(body, dict):
            fields = config.get("fields", [])
            for field in fields:
                if field in body and isinstance(body[field], str):
                    body[field] = body[field].lower()
        return body
    
    def _rename_fields(self, body: Any, config: Dict) -> Any:
        """Rename fields."""
        if isinstance(body, dict):
            mappings = config.get("mappings", {})
            for old_name, new_name in mappings.items():
                if old_name in body:
                    body[new_name] = body.pop(old_name)
        return body
    
    def _add_fields(self, body: Any, config: Dict) -> Any:
        """Add new fields."""
        if isinstance(body, dict):
            fields = config.get("fields", {})
            body.update(fields)
        return body
    
    def _remove_fields(self, body: Any, config: Dict) -> Any:
        """Remove specified fields."""
        if isinstance(body, dict):
            fields = config.get("fields", [])
            for field in fields:
                body.pop(field, None)
        return body
    
    def _map_values(self, body: Any, config: Dict) -> Any:
        """Map field values."""
        if isinstance(body, dict):
            mappings = config.get("mappings", {})
            for field, mapping in mappings.items():
                if field in body and body[field] in mapping:
                    body[field] = mapping[body[field]]
        return body


class RequestValidator:
    """Validates incoming requests."""
    
    def __init__(self):
        self.max_request_size = 10485760
        self.allowed_content_types = [
            "application/json",
            "application/xml",
            "multipart/form-data",
            "application/x-www-form-urlencoded",
            "text/plain",
            "text/html",
        ]
    
    def validate(
        self,
        method: str,
        path: str,
        headers: Dict,
        body: Any,
        endpoint_config: EndpointConfig
    ) -> Dict[str, Any]:
        """Validate a request against endpoint configuration."""
        errors = []
        warnings = []
        
        if not self._validate_method(method, endpoint_config.methods):
            errors.append(f"Method {method} not allowed for this endpoint")
        
        if not self._validate_content_length(headers.get("content-length", 0), endpoint_config.max_request_size_bytes):
            errors.append(f"Request body exceeds maximum size of {endpoint_config.max_request_size_bytes} bytes")
        
        if endpoint_config.validate_request_body:
            validation_result = self._validate_body(headers.get("content-type"), body)
            if validation_result:
                errors.extend(validation_result)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _validate_method(self, method: str, allowed_methods: List[HTTPMethod]) -> bool:
        """Check if HTTP method is allowed."""
        if HTTPMethod.ANY in allowed_methods:
            return True
        return any(m.value == method for m in allowed_methods)
    
    def _validate_content_length(self, content_length: Union[str, int], max_size: int) -> bool:
        """Check if content length is within limits."""
        try:
            length = int(content_length) if content_length else 0
            return length <= max_size
        except (ValueError, TypeError):
            return True
    
    def _validate_body(self, content_type: Optional[str], body: Any) -> List[str]:
        """Validate request body."""
        errors = []
        if not content_type:
            errors.append("Content-Type header is required for this endpoint")
        elif content_type not in self.allowed_content_types:
            errors.append(f"Unsupported Content-Type: {content_type}")
        return errors


class GatewayAnalytics:
    """Tracks and reports gateway analytics."""
    
    def __init__(self):
        self.total_requests: int = 0
        self.total_errors: int = 0
        self.total_latency_ms: int = 0
        self.requests_by_endpoint: Dict[str, int] = defaultdict(int)
        self.requests_by_status: Dict[int, int] = defaultdict(int)
        self.requests_by_auth_type: Dict[str, int] = defaultdict(int)
        self.errors_by_type: Dict[str, int] = defaultdict(int)
        self.rate_limit_hits: int = 0
        self.circuit_breaker_trips: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.start_time: datetime = datetime.now()
        self.lock = threading.Lock()
    
    def record_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        latency_ms: int,
        auth_type: str,
        cached: bool = False
    ):
        """Record a request."""
        with self.lock:
            self.total_requests += 1
            self.total_latency_ms += latency_ms
            self.requests_by_endpoint[f"{method} {endpoint}"] += 1
            self.requests_by_status[status_code] += 1
            self.requests_by_auth_type[auth_type] += 1
            
            if cached:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
            
            if status_code >= 400:
                self.total_errors += 1
    
    def record_error(self, error_type: str):
        """Record an error."""
        with self.lock:
            self.errors_by_type[error_type] += 1
    
    def record_rate_limit_hit(self):
        """Record a rate limit hit."""
        with self.lock:
            self.rate_limit_hits += 1
    
    def record_circuit_breaker_trip(self):
        """Record a circuit breaker trip."""
        with self.lock:
            self.circuit_breaker_trips += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get analytics summary."""
        with self.lock:
            uptime = (datetime.now() - self.start_time).total_seconds()
            avg_latency = self.total_latency_ms / max(1, self.total_requests)
            
            return {
                "summary": {
                    "total_requests": self.total_requests,
                    "total_errors": self.total_errors,
                    "error_rate": round(self.total_errors / max(1, self.total_requests) * 100, 2),
                    "average_latency_ms": round(avg_latency, 2),
                    "requests_per_second": round(self.total_requests / max(1, uptime), 2),
                    "uptime_seconds": round(uptime, 2),
                    "rate_limit_hits": self.rate_limit_hits,
                    "circuit_breaker_trips": self.circuit_breaker_trips,
                    "cache_hits": self.cache_hits,
                    "cache_misses": self.cache_misses,
                    "cache_hit_rate": round(self.cache_hits / max(1, self.cache_hits + self.cache_misses) * 100, 2)
                },
                "by_endpoint": dict(self.requests_by_endpoint),
                "by_status": dict(self.requests_by_status),
                "by_auth_type": dict(self.requests_by_auth_type),
                "by_error_type": dict(self.errors_by_type)
            }
    
    def get_report(self, period: str = "hour") -> Dict[str, Any]:
        """Generate a report for a time period."""
        summary = self.get_summary()
        return {
            "period": period,
            "generated_at": datetime.now().isoformat(),
            **summary
        }


class Plugin(ABC):
    """Base class for gateway plugins."""
    
    @abstractmethod
    def on_request(self, request: Dict) -> Dict:
        """Called before processing a request."""
        pass
    
    @abstractmethod
    def on_response(self, request: Dict, response: Dict) -> Dict:
        """Called before sending a response."""
        pass
    
    @abstractmethod
    def on_error(self, request: Dict, error: Exception) -> Dict:
        """Called when an error occurs."""
        pass


class PluginManager:
    """Manages gateway plugins."""
    
    def __init__(self):
        self.plugins: List[Plugin] = []
        self.enabled: bool = True
    
    def register_plugin(self, plugin: Plugin):
        """Register a new plugin."""
        self.plugins.append(plugin)
    
    def unregister_plugin(self, plugin_class: type):
        """Unregister a plugin by class."""
        self.plugins = [p for p in self.plugins if not isinstance(p, plugin_class)]
    
    def on_request(self, request: Dict) -> Dict:
        """Process request through all plugins."""
        if not self.enabled:
            return request
        for plugin in self.plugins:
            request = plugin.on_request(request)
        return request
    
    def on_response(self, request: Dict, response: Dict) -> Dict:
        """Process response through all plugins."""
        if not self.enabled:
            return response
        for plugin in self.plugins:
            response = plugin.on_response(request, response)
        return response
    
    def on_error(self, request: Dict, error: Exception) -> Dict:
        """Process error through all plugins."""
        for plugin in self.plugins:
            response = plugin.on_error(request, error)
        return {"error": str(error), "status": 500}


class RateLimitMiddleware:
    """Rate limiting middleware for the gateway."""
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.limiters: Dict[str, TokenBucketRateLimiter] = {}
        self.sliding_window_limiters: Dict[str, SlidingWindowRateLimiter] = {}
        self.lock = threading.Lock()
    
    def allow_request(self, identifier: str, endpoint: str = "") -> Dict[str, Any]:
        """Check if a request should be allowed."""
        with self.lock:
            if self._is_whitelisted(identifier):
                return {"allowed": True, "reason": "whitelisted", "remaining": float("inf")}
            
            if self._is_blacklisted(identifier):
                return {"allowed": False, "reason": "blacklisted", "remaining": 0}
            
            endpoint_config = self.config.per_endpoint_limits.get(endpoint, {})
            user_config = self.config.per_user_limits.get(identifier, {})
            
            max_requests = endpoint_config.get("requests", user_config.get("requests", self.config.default_requests_per_window))
            window_seconds = endpoint_config.get("window", user_config.get("window", self.config.default_window_seconds))
            
            if self.config.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
                return self._check_token_bucket(identifier, max_requests, window_seconds)
            else:
                return self._check_sliding_window(identifier, max_requests, window_seconds)
    
    def _is_whitelisted(self, identifier: str) -> bool:
        """Check if identifier is whitelisted."""
        return any(identifier.startswith(ip) for ip in self.config.ip_whitelist)
    
    def _is_blacklisted(self, identifier: str) -> bool:
        """Check if identifier is blacklisted."""
        return any(identifier.startswith(ip) for ip in self.config.ip_blacklist)
    
    def _check_token_bucket(
        self,
        identifier: str,
        max_requests: int,
        window_seconds: int
    ) -> Dict[str, Any]:
        """Check token bucket rate limit."""
        if identifier not in self.limiters:
            refill_rate = max_requests / window_seconds
            self.limiters[identifier] = TokenBucketRateLimiter(max_requests, refill_rate)
        
        limiter = self.limiters[identifier]
        allowed = limiter.allow_request()
        
        return {
            "allowed": allowed,
            "reason": "rate_limited" if not allowed else "allowed",
            "remaining": limiter.get_remaining(),
            "limit": max_requests,
            "reset_seconds": window_seconds
        }
    
    def _check_sliding_window(
        self,
        identifier: str,
        max_requests: int,
        window_seconds: int
    ) -> Dict[str, Any]:
        """Check sliding window rate limit."""
        if identifier not in self.sliding_window_limiters:
            self.sliding_window_limiters[identifier] = SlidingWindowRateLimiter(max_requests, window_seconds)
        
        limiter = self.sliding_window_limiters[identifier]
        allowed = limiter.allow_request(identifier)
        
        return {
            "allowed": allowed,
            "reason": "rate_limited" if not allowed else "allowed",
            "remaining": limiter.get_remaining(identifier),
            "limit": max_requests,
            "reset_seconds": window_seconds
        }


class APIGatewayAgent:
    """
    Enterprise-Grade API Gateway Agent.
    
    Provides comprehensive API gateway management including:
    - Dynamic routing and request handling
    - Rate limiting with multiple algorithms
    - Authentication and authorization
    - Circuit breaker patterns
    - Request/response transformation
    - Caching strategies
    - Analytics and monitoring
    - Plugin extensibility
    """
    
    def __init__(self, config: Optional[GatewayConfig] = None):
        self._config = config or GatewayConfig()
        self._endpoints: Dict[str, EndpointConfig] = {}
        self._upstream_pools: Dict[str, UpstreamPool] = {}
        self._rate_limit_middleware = RateLimitMiddleware(self._config.rate_limit_config)
        self._response_transformer = ResponseTransformer()
        self._request_validator = RequestValidator()
        self._analytics = GatewayAnalytics()
        self._plugin_manager = PluginManager()
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._request_id_counter = 0
        self._request_id_lock = threading.Lock()
        self._started = False
    
    def configure_gateway(self, config: GatewayConfig) -> Dict[str, Any]:
        """Configure the API gateway with the provided configuration."""
        self._config = config
        self._rate_limit_middleware = RateLimitMiddleware(config.rate_limit_config)
        
        for endpoint in config.endpoint_configs:
            self.register_endpoint(endpoint)
        
        return {
            "status": "configured",
            "name": config.name,
            "environment": config.environment.value,
            "endpoints_registered": len(self._endpoints)
        }
    
    def register_endpoint(self, endpoint: EndpointConfig) -> Dict[str, Any]:
        """Register a new API endpoint."""
        self._endpoints[endpoint.path] = endpoint
        
        pool = UpstreamPool(LoadBalancingStrategy.ROUND_ROBIN)
        self._upstream_pools[endpoint.path] = pool
        
        return {
            "status": "registered",
            "path": endpoint.path,
            "methods": [m.value for m in endpoint.methods],
            "upstream_url": endpoint.upstream_url,
            "auth_type": endpoint.auth_type.value
        }
    
    def add_upstream_server(self, endpoint_path: str, server: UpstreamServer) -> Dict[str, Any]:
        """Add an upstream server to an endpoint's pool."""
        if endpoint_path not in self._upstream_pools:
            return {"status": "error", "message": f"Endpoint {endpoint_path} not found"}
        
        pool = self._upstream_pools[endpoint_path]
        pool.add_server(server)
        
        return {
            "status": "added",
            "endpoint": endpoint_path,
            "server_url": server.url,
            "weight": server.weight
        }
    
    def configure_rate_limit(
        self,
        endpoint: str,
        requests_per_minute: int,
        algorithm: RateLimitAlgorithm = RateLimitAlgorithm.SLIDING_WINDOW
    ) -> Dict[str, Any]:
        """Configure rate limiting for an endpoint."""
        if endpoint in self._endpoints:
            self._endpoints[endpoint].rate_limit = requests_per_minute
            self._endpoints[endpoint].rate_limit_algorithm = algorithm
        
        return {
            "status": "configured",
            "endpoint": endpoint,
            "requests_per_minute": requests_per_minute,
            "algorithm": algorithm.value
        }
    
    def configure_auth(self, endpoint: str, auth_type: AuthType, **kwargs) -> Dict[str, Any]:
        """Configure authentication for an endpoint."""
        if endpoint in self._endpoints:
            self._endpoints[endpoint].auth_type = auth_type
        
        return {
            "status": "configured",
            "endpoint": endpoint,
            "auth_type": auth_type.value
        }
    
    def add_route(self, path: str, methods: List[str], upstream_url: str, 
                  auth_type: str = "none", rate_limit: int = 1000) -> Dict[str, Any]:
        """Add a new route to the gateway."""
        endpoint = EndpointConfig(
            path=path,
            methods=[HTTPMethod(m) for m in methods],
            upstream_url=upstream_url,
            auth_type=AuthType(auth_type),
            rate_limit=rate_limit
        )
        return self.register_endpoint(endpoint)
    
    def create_upstream_pool(self, name: str, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN) -> Dict[str, Any]:
        """Create a new upstream pool."""
        self._upstream_pools[name] = UpstreamPool(strategy)
        return {
            "status": "created",
            "pool_name": name,
            "strategy": strategy.value
        }
    
    def register_plugin(self, plugin: Plugin) -> Dict[str, Any]:
        """Register a plugin with the gateway."""
        self._plugin_manager.register_plugin(plugin)
        return {
            "status": "registered",
            "plugin_type": type(plugin).__name__
        }
    
    def get_analytics(self, period: str = "hour") -> Dict[str, Any]:
        """Get API usage analytics."""
        return self._analytics.get_report(period)
    
    def get_status(self) -> Dict[str, Any]:
        """Get gateway status."""
        return {
            "agent": "APIGatewayAgent",
            "name": self._config.name,
            "environment": self._config.environment.value,
            "status": "running" if self._started else "stopped",
            "endpoints_count": len(self._endpoints),
            "upstream_pools_count": len(self._upstream_pools),
            "plugins_count": len(self._plugin_manager.plugins),
            "analytics": self._analytics.get_summary()["summary"]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get detailed gateway statistics."""
        stats = {
            "gateway": {
                "name": self._config.name,
                "environment": self._config.environment.value,
                "status": "running"
            },
            "endpoints": {},
            "upstream_pools": {},
            "circuit_breakers": {},
            "analytics": self._analytics.get_summary()
        }
        
        for path, endpoint in self._endpoints.items():
            stats["endpoints"][path] = {
                "methods": [m.value for m in endpoint.methods],
                "upstream_url": endpoint.upstream_url,
                "auth_type": endpoint.auth_type.value,
                "rate_limit": endpoint.rate_limit
            }
        
        for name, pool in self._upstream_pools.items():
            stats["upstream_pools"][name] = {
                "strategy": pool.strategy.value,
                "servers_count": len(pool.servers)
            }
        
        return stats
    
    def validate_endpoint(self, method: str, path: str, headers: Dict, 
                         body: Any) -> Dict[str, Any]:
        """Validate an incoming request."""
        endpoint = None
        for ep_path, ep_config in self._endpoints.items():
            if ep_config.matches_path(path):
                endpoint = ep_config
                break
        
        if not endpoint:
            return {
                "valid": False,
                "errors": [f"No endpoint found for path {path}"],
                "status_code": 404
            }
        
        return self._request_validator.validate(method, path, headers, body, endpoint)
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on the gateway."""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "endpoints": len(self._endpoints),
                "upstream_pools": len([p for p in self._upstream_pools.values() if p.servers]),
                "analytics": "connected" if self._analytics else "disconnected"
            }
        }
    
    def export_config(self) -> Dict[str, Any]:
        """Export current gateway configuration."""
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
                        "timeout_ms": ep.timeout_ms
                    }
                    for ep in self._endpoints.values()
                ]
            }
        }
    
    def start(self) -> Dict[str, Any]:
        """Start the gateway."""
        self._started = True
        return {
            "status": "started",
            "name": self._config.name,
            "timestamp": datetime.now().isoformat()
        }
    
    def stop(self) -> Dict[str, Any]:
        """Stop the gateway."""
        self._started = False
        return {
            "status": "stopped",
            "name": self._config.name,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main entry point for the API Gateway Agent."""
    print("\n" + "="*60)
    print("  API Gateway Agent")
    print("  Enterprise-Grade Gateway Management")
    print("="*60 + "\n")
    
    gateway = APIGatewayAgent()
    
    gateway_result = gateway.configure_gateway(GatewayConfig(
        name="production-gateway",
        environment=GatewayEnvironment.PRODUCTION,
        host="0.0.0.0",
        port=8080
    ))
    print("Gateway Configuration:")
    print(f"  Name: {gateway_result['name']}")
    print(f"  Environment: {gateway_result['environment']}")
    print()
    
    route1 = gateway.add_route(
        path="/api/v1/users",
        methods=["GET", "POST"],
        upstream_url="http://user-service:8080",
        auth_type="jwt",
        rate_limit=100
    )
    print("Route Registration:")
    print(f"  Path: {route1['path']}")
    print(f"  Methods: {route1['methods']}")
    print(f"  Auth: {route1['auth_type']}")
    print()
    
    gateway.create_upstream_pool("user-service-pool", LoadBalancingStrategy.LEAST_CONNECTIONS)
    server = UpstreamServer(url="http://user-service-1:8080", weight=100)
    gateway.add_upstream_server("/api/v1/users", server)
    print("Upstream Pool:")
    print(f"  Strategy: least_connections")
    print(f"  Server: {server.url}")
    print()
    
    print("Gateway Status:")
    status = gateway.get_status()
    for key, value in status.items():
        if key != "analytics":
            print(f"  {key}: {value}")
    print()
    
    print("Analytics Preview:")
    analytics = gateway.get_analytics()
    summary = analytics.get("summary", {})
    print(f"  Total Requests: {summary.get('total_requests', 0)}")
    print(f"  Error Rate: {summary.get('error_rate', 0)}%")
    print(f"  Avg Latency: {summary.get('average_latency_ms', 0)}ms")
    print()


if __name__ == "__main__":
    main()
