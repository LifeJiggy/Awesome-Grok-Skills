"""
edge_runtime.py — Edge Runtime & Serverless Functions library.

Provides abstractions for:
- Edge function lifecycle and request handling
- Geo-based routing and personalization
- Middleware chains with JWT verification
- WebSocket management with Durable Objects
- KV storage operations (get, put, list, delete)
- Scheduled/cron job execution
- HTML rewriting at the edge
- Rate limiting with token buckets
- Edge-compatible database connections

Designed for Cloudflare Workers, Vercel Edge, Deno Deploy, and Netlify Edge.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Union,
    runtime_checkable,
)
from urllib.parse import urlparse, parse_qs


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class HttpMethod(Enum):
    """HTTP methods supported at the edge."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    WebSocket = "WebSocket"


class EdgeRuntime(Enum):
    """Supported edge runtimes."""
    CLOUDFLARE_WORKERS = "cloudflare-workers"
    VERCEL_EDGE = "vercel-edge"
    DENO_DEPLOY = "deno-deploy"
    NETLIFY_EDGE = "netlify-edge"
    AWS_LAMBDA_EDGE = "aws-lambda-edge"


class CacheStrategy(Enum):
    """Edge caching strategies."""
    NO_CACHE = "no-cache"
    FORCE_CACHE = "force-cache"
    REVALIDATE = "revalidate"
    STALE_WHILE_REVALIDATE = "stale-while-revalidate"


class KVConsistency(Enum):
    """KV storage consistency models."""
    EVENTUAL = "eventual"   # Cloudflare KV — eventual consistency
    STRONG = "strong"       # Durable Objects / Deno KV — strong consistency


class WebSocketState(Enum):
    """WebSocket connection states."""
    CONNECTING = 0
    OPEN = 1
    CLOSING = 2
    CLOSED = 3


class DurableObjectState(Enum):
    """Durable Object lifecycle states."""
    CREATED = "created"
    ACTIVE = "active"
    IDLE = "idle"
    TERMINATED = "terminated"


class CronFrequency(Enum):
    """Predefined cron frequencies."""
    MINUTE = "* * * * *"
    HOURLY = "0 * * * *"
    EVERY_6H = "0 */6 * * *"
    DAILY = "0 0 * * *"
    WEEKLY = "0 0 * * 0"
    MONTHLY = "0 0 1 * *"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GeoContext:
    """Geographic context from the edge."""
    country: str | None = None
    region: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    continent: str | None = None
    postal_code: str | None = None
    metro_code: str | None = None

    @property
    def is_eu(self) -> bool:
        eu_countries = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
        return self.country in eu_countries if self.country else False


@dataclass
class EdgeRequest:
    """Edge-compatible request object."""
    url: str
    method: str = "GET"
    headers: dict[str, str] = field(default_factory=dict)
    cookies: dict[str, str] = field(default_factory=dict)
    body: Any = None
    geo: GeoContext = field(default_factory=GeoContext)
    cf: dict[str, Any] = field(default_factory=dict)  # Cloudflare-specific
    ip: str | None = None

    @property
    def origin(self) -> str:
        parsed = urlparse(self.url)
        return f"{parsed.scheme}://{parsed.netloc}"

    @property
    def pathname(self) -> str:
        return urlparse(self.url).path

    @property
    def query(self) -> dict[str, str]:
        parsed = urlparse(self.url)
        return {k: v[0] for k, v in parse_qs(parsed.query).items()}

    @property
    def search(self) -> str:
        return urlparse(self.url).query

    async def json(self) -> dict[str, Any]:
        """Parse request body as JSON."""
        if isinstance(self.body, str):
            return json.loads(self.body)
        if isinstance(self.body, dict):
            return self.body
        return {}


@dataclass
class EdgeResponse:
    """Edge-compatible response object."""
    status: int = 200
    headers: dict[str, str] = field(default_factory=dict)
    body: str | bytes | None = None

    @classmethod
    def json(cls, data: Any, status: int = 200, headers: dict[str, str] | None = None) -> EdgeResponse:
        """Create a JSON response."""
        resp_headers = {"Content-Type": "application/json"}
        if headers:
            resp_headers.update(headers)
        return cls(status=status, headers=resp_headers, body=json.dumps(data, default=str))

    @classmethod
    def redirect(cls, url: str, status: int = 302, headers: dict[str, str] | None = None) -> EdgeResponse:
        """Create a redirect response."""
        resp_headers = {"Location": url}
        if headers:
            resp_headers.update(headers)
        return cls(status=status, headers=resp_headers)

    @classmethod
    def html(cls, content: str, status: int = 200, headers: dict[str, str] | None = None) -> EdgeResponse:
        """Create an HTML response."""
        resp_headers = {"Content-Type": "text/html;charset=utf-8"}
        if headers:
            resp_headers.update(headers)
        return cls(status=status, headers=resp_headers, body=content)

    @classmethod
    def webSocket(cls, client: Any) -> EdgeResponse:
        """Create a WebSocket upgrade response."""
        return cls(status=101, headers={"Upgrade": "websocket"}, body=client)


@dataclass(frozen=True)
class ScheduledEvent:
    """Event for scheduled/cron triggers."""
    cron: str
    scheduled_time: int  # Unix timestamp in milliseconds
    event_id: str = ""

    def __post_init__(self) -> None:
        if not self.event_id:
            object.__setattr__(self, "event_id", str(uuid.uuid4()))


@dataclass(frozen=True)
class KVListOptions:
    """Options for KV list operations."""
    prefix: str = ""
    limit: int = 100
    cursor: str | None = None


@dataclass
class KVListResult:
    """Result from a KV list operation."""
    keys: list[KVKey] = field(default_factory=list)
    list_complete: bool = True
    cache_status: str | None = None

    @dataclass
    class KVKey:
        name: str
        expiration: int | None = None
        metadata: dict[str, Any] | None = None


@dataclass
class WebSocketMessage:
    """A WebSocket message."""
    data: str | bytes
    is_binary: bool = False
    timestamp: float = field(default_factory=time.time)


@dataclass
class DurableObjectInfo:
    """Information about a Durable Object instance."""
    id: str
    name: str | None = None
    class_name: str = ""
    state: DurableObjectState = DurableObjectState.ACTIVE
    created_at: float = field(default_factory=time.time)


@dataclass
class EdgeFunctionConfig:
    """Configuration for an edge function."""
    name: str = "edge-function"
    runtime: EdgeRuntime = EdgeRuntime.CLOUDFLARE_WORKERS
    routes: list[str] = field(default_factory=lambda: ["/*"])
    cache_strategy: CacheStrategy = CacheStrategy.NO_CACHE
    max_cpu_ms: int = 50  # Cloudflare Workers limit
    max_memory_mb: int = 128
    max_subrequests: int = 50
    cron: str | None = None
    kv_namespaces: list[str] = field(default_factory=list)
    durable_objects: list[str] = field(default_factory=list)
    env_vars: dict[str, str] = field(default_factory=dict)


@dataclass
class RateLimitConfig:
    """Configuration for edge rate limiting."""
    max_requests: int = 100
    window_seconds: int = 60
    key_prefix: str = "rl"
    skip_paths: list[str] = field(default_factory=list)
    skip_headers: dict[str, str] = field(default_factory=dict)


@dataclass
class EdgeMetrics:
    """Metrics collected during edge function execution."""
    request_count: int = 0
    error_count: int = 0
    total_cpu_ms: float = 0
    avg_cpu_ms: float = 0
    subrequest_count: int = 0
    kv_reads: int = 0
    kv_writes: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

    def record_request(self, cpu_ms: float) -> None:
        self.request_count += 1
        self.total_cpu_ms += cpu_ms
        self.avg_cpu_ms = self.total_cpu_ms / self.request_count


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class EdgeRuntimeError(Exception):
    """Base error for edge runtime operations."""
    pass


class EdgeTimeoutError(EdgeRuntimeError):
    """Function execution exceeded CPU time limit."""
    def __init__(self, cpu_ms: int, limit_ms: int):
        self.cpu_ms = cpu_ms
        self.limit_ms = limit_ms
        super().__init__(f"CPU time {cpu_ms}ms exceeded limit of {limit_ms}ms")


class KVError(EdgeRuntimeError):
    """KV storage operation failed."""
    pass


class WebSocketError(EdgeRuntimeError):
    """WebSocket operation failed."""
    pass


class DurableObjectError(EdgeRuntimeError):
    """Durable Object operation failed."""
    pass


class JWTError(EdgeRuntimeError):
    """JWT verification failed."""
    pass


class RateLimitExceededError(EdgeRuntimeError):
    """Rate limit exceeded."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after}s")


# ---------------------------------------------------------------------------
# KV Storage
# ---------------------------------------------------------------------------

class KVNamespace:
    """Simulated KV storage namespace."""

    def __init__(self, name: str, consistency: KVConsistency = KVConsistency.EVENTUAL) -> None:
        self.name = name
        self.consistency = consistency
        self._store: dict[str, dict[str, Any]] = {}
        self._reads = 0
        self._writes = 0

    async def get(self, key: str, type: str = "text") -> Any:
        """Read a value from KV."""
        self._reads += 1
        entry = self._store.get(key)
        if entry is None:
            return None

        # Check expiration
        if entry.get("expires_at") and time.time() > entry["expires_at"]:
            del self._store[key]
            return None

        value = entry["value"]
        if type == "json" and isinstance(value, str):
            return json.loads(value)
        return value

    async def put(
        self, key: str, value: Any,
        expiration_ttl: int | None = None,
        expiration: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Write a value to KV."""
        self._writes += 1
        entry: dict[str, Any] = {"value": value}
        if expiration_ttl:
            entry["expires_at"] = time.time() + expiration_ttl
        elif expiration:
            entry["expires_at"] = expiration
        if metadata:
            entry["metadata"] = metadata
        self._store[key] = entry

    async def delete(self, key: str) -> None:
        """Delete a value from KV."""
        self._store.pop(key, None)

    async def list(self, options: KVListOptions | None = None) -> KVListResult:
        """List keys in the KV namespace."""
        options = options or KVListOptions()
        keys = []
        for key in sorted(self._store.keys()):
            if options.prefix and not key.startswith(options.prefix):
                continue
            entry = self._store[key]
            keys.append(KVListResult.KVKey(
                name=key,
                expiration=entry.get("expires_at"),
                metadata=entry.get("metadata"),
            ))
            if len(keys) >= options.limit:
                break
        return KVListResult(keys=keys, list_complete=len(keys) < options.limit)

    def get_stats(self) -> dict[str, int]:
        return {"reads": self._reads, "writes": self._writes, "entries": len(self._store)}


# ---------------------------------------------------------------------------
# WebSocket Manager
# ---------------------------------------------------------------------------

class WebSocketManager:
    """Manages WebSocket connections at the edge."""

    def __init__(self) -> None:
        self._connections: dict[str, list[dict[str, Any]]] = {}

    def accept(self, ws_id: str) -> None:
        """Accept a WebSocket connection."""
        if ws_id not in self._connections:
            self._connections[ws_id] = []
        self._connections[ws_id].append({
            "state": WebSocketState.OPEN,
            "created_at": time.time(),
            "messages": [],
        })

    def send(self, ws_id: str, data: str | bytes) -> bool:
        """Send a message to a WebSocket connection."""
        if ws_id not in self._connections or not self._connections[ws_id]:
            return False
        conn = self._connections[ws_id][-1]
        if conn["state"] != WebSocketState.OPEN:
            return False
        conn["messages"].append(WebSocketMessage(data=data))
        return True

    def broadcast(self, data: str | bytes, room: str | None = None) -> int:
        """Broadcast a message to all connected clients."""
        sent = 0
        for ws_id, conns in self._connections.items():
            for conn in conns:
                if conn["state"] == WebSocketState.OPEN:
                    conn["messages"].append(WebSocketMessage(data=data))
                    sent += 1
        return sent

    def close(self, ws_id: str) -> None:
        """Close a WebSocket connection."""
        if ws_id in self._connections:
            for conn in self._connections[ws_id]:
                conn["state"] = WebSocketState.CLOSED

    @property
    def active_connections(self) -> int:
        count = 0
        for conns in self._connections.values():
            for conn in conns:
                if conn["state"] == WebSocketState.OPEN:
                    count += 1
        return count


# ---------------------------------------------------------------------------
# Durable Object
# ---------------------------------------------------------------------------

class DurableObject:
    """Base class for Durable Objects with state and WebSocket support."""

    def __init__(self, state: DurableObjectInfo, env: dict[str, Any]) -> None:
        self.state = state
        self.env = env
        self.ws_manager = WebSocketManager()
        self._storage: dict[str, Any] = {}

    async def fetch(self, request: EdgeRequest) -> EdgeResponse:
        """Handle a request to this Durable Object."""
        if request.pathname.endswith("/ws"):
            return await self.handle_websocket(request)
        return EdgeResponse.json({"id": self.state.id, "state": self.state.state.value})

    async def handle_websocket(self, request: EdgeRequest) -> EdgeResponse:
        """Handle a WebSocket upgrade."""
        ws_id = str(uuid.uuid4())
        self.ws_manager.accept(ws_id)
        return EdgeResponse(status=101, headers={"Upgrade": "websocket"})

    async def alarm(self) -> None:
        """Handle a Durable Object alarm (scheduled wake-up)."""
        pass

    async def storage_get(self, key: str) -> Any:
        return self._storage.get(key)

    async def storage_put(self, key: str, value: Any) -> None:
        self._storage[key] = value

    async def storage_delete(self, key: str) -> None:
        self._storage.pop(key, None)


# ---------------------------------------------------------------------------
# HTML Rewriter
# ---------------------------------------------------------------------------

class HTMLRewriterElement:
    """Represents an element being transformed by HTMLRewriter."""

    def __init__(self, tag: str, attributes: dict[str, str]) -> None:
        self.tag = tag
        self.attributes = dict(attributes)
        self._inner_content: str | None = None
        self._inner_html: str | None = None
        self._remove: bool = False

    def setInnerContent(self, content: str) -> None:
        self._inner_content = content

    def setInnerHTML(self, html: str) -> None:
        self._inner_html = html

    def remove(self) -> None:
        self._remove = True

    def setAttribute(self, name: str, value: str) -> None:
        self.attributes[name] = value

    def removeAttribute(self, name: str) -> None:
        self.attributes.pop(name, None)


class HTMLRewriter:
    """HTML Rewriter for streaming transformations at the edge."""

    def __init__(self) -> None:
        self._handlers: dict[str, dict[str, Callable]] = {}
        self._results: list[str] = []

    def on(self, selector: str, handlers: dict[str, Callable]) -> HTMLRewriter:
        """Register handlers for a CSS selector."""
        self._handlers[selector] = handlers
        return self

    def transform(self, response: EdgeResponse) -> EdgeResponse:
        """Apply transformations to an HTML response."""
        if not response.body or not isinstance(response.body, str):
            return response

        html = response.body

        # Simple element replacement (simulation)
        for selector, handlers in self._handlers.items():
            tag = selector.lstrip(".#")
            pattern = re.compile(
                rf'<{tag}([^>]*)>(.*?)</{tag}>',
                re.DOTALL,
            )

            def replace_match(match: re.Match, _handlers: dict = handlers) -> str:
                attrs_str = match.group(1)
                content = match.group(2)
                el = HTMLRewriterElement(tag, self._parse_attrs(attrs_str))

                if "element" in _handlers:
                    _handlers["element"](el)

                if el._remove:
                    return ""
                if el._inner_content is not None:
                    return f'<{tag}{self._attrs_str(el.attributes)}>{el._inner_content}</{tag}>'
                return match.group(0)

            html = pattern.sub(replace_match, html)

        return EdgeResponse(
            status=response.status,
            headers=response.headers,
            body=html,
        )

    def _parse_attrs(self, attrs_str: str) -> dict[str, str]:
        """Parse HTML attributes from a string."""
        attrs = {}
        for match in re.finditer(r'(\w[\w-]*)="([^"]*)"', attrs_str):
            attrs[match.group(1)] = match.group(2)
        return attrs

    def _attrs_str(self, attrs: dict[str, str]) -> str:
        """Build an attributes string."""
        if not attrs:
            return ""
        parts = [f' {k}="{v}"' for k, v in attrs.items()]
        return "".join(parts)


# ---------------------------------------------------------------------------
# Edge Function (base)
# ---------------------------------------------------------------------------

class EdgeFunction:
    """Base class for edge functions."""

    config: ClassVar[EdgeFunctionConfig] = EdgeFunctionConfig()

    def __init__(self, env: dict[str, Any] | None = None) -> None:
        self.env = env or {}
        self.metrics = EdgeMetrics()

    async def handle(self, request: EdgeRequest) -> EdgeResponse:
        """Override this to handle requests."""
        return EdgeResponse.json({"message": "Edge function"}, status=200)

    async def scheduled(self, event: ScheduledEvent) -> None:
        """Override this for scheduled/cron triggers."""
        pass

    async def fetch_with_cache(
        self, url: str, cache_strategy: CacheStrategy = CacheStrategy.NO_CACHE, ttl: int = 60
    ) -> dict:
        """Fetch with edge caching."""
        self.metrics.subrequest_count += 1
        # Simulated fetch
        return {"url": url, "cached": cache_strategy != CacheStrategy.NO_CACHE}


class EdgeMiddleware:
    """Base class for edge middleware."""

    async def handle(self, request: EdgeRequest, next: Callable) -> EdgeResponse:
        """Process the request and call next."""
        return await next(request)


# ---------------------------------------------------------------------------
# JWT Verifier (Edge)
# ---------------------------------------------------------------------------

class EdgeJWTVerifier:
    """Lightweight JWT verification for edge functions."""

    def __init__(self, secret: str, audience: str = "authenticated") -> None:
        self.secret = secret
        self.audience = audience

    async def verify(self, token: str) -> dict[str, Any]:
        """Verify a JWT token (simplified HMAC verification)."""
        import base64 as b64

        parts = token.split(".")
        if len(parts) != 3:
            raise JWTError("Invalid token format")

        header_b64, payload_b64, sig_b64 = parts

        # Verify signature
        import hmac as hmac_mod
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac_mod.new(self.secret.encode(), signing_input, hashlib.sha256).digest()

        # Pad and decode
        padding = 4 - len(sig_b64) % 4
        if padding != 4:
            sig_b64 += "=" * padding
        actual_sig = b64.urlsafe_b64decode(sig_b64)

        if not hmac_mod.compare_digest(expected_sig, actual_sig):
            raise JWTError("Invalid signature")

        # Decode payload
        padding2 = 4 - len(payload_b64) % 4
        if padding2 != 4:
            payload_b64 += "=" * padding2
        payload = json.loads(b64.urlsafe_b64decode(payload_b64))

        # Check expiry
        if payload.get("exp", 0) < time.time():
            raise JWTError("Token expired")

        return payload


# ---------------------------------------------------------------------------
# Rate Limiter
# ---------------------------------------------------------------------------

class EdgeRateLimiter:
    """Token bucket rate limiter for edge functions."""

    def __init__(self, config: RateLimitConfig, kv: KVNamespace) -> None:
        self.config = config
        self.kv = kv

    async def check(self, request: EdgeRequest) -> tuple[bool, dict[str, str]]:
        """Check if the request is within rate limits. Returns (allowed, headers)."""
        # Skip certain paths
        for path in self.config.skip_paths:
            if request.pathname.startswith(path):
                return True, {}

        client_ip = request.ip or request.headers.get("cf-connecting-ip", "unknown")
        key = f"{self.config.key_prefix}:{client_ip}"

        data = await self.kv.get(key, type="json")
        now = int(time.time())

        if data is None or now - data.get("window_start", 0) > self.config.window_seconds:
            data = {"count": 1, "window_start": now}
        else:
            data["count"] += 1

        remaining_ttl = max(1, self.config.window_seconds - (now - data["window_start"]))
        await self.kv.put(key, json.dumps(data), expiration_ttl=remaining_ttl)

        headers = {
            "X-RateLimit-Limit": str(self.config.max_requests),
            "X-RateLimit-Remaining": str(max(0, self.config.max_requests - data["count"])),
            "X-RateLimit-Reset": str(data["window_start"] + self.config.window_seconds),
        }

        if data["count"] > self.config.max_requests:
            headers["Retry-After"] = str(remaining_ttl)
            return False, headers

        return True, headers


# ---------------------------------------------------------------------------
# Edge Router
# ---------------------------------------------------------------------------

class EdgeRouter:
    """Route requests to edge functions based on patterns."""

    def __init__(self) -> None:
        self._routes: list[tuple[str, EdgeFunction]] = []
        self._middleware: list[EdgeMiddleware] = []

    def add_route(self, pattern: str, handler: EdgeFunction) -> None:
        """Add a route pattern and handler."""
        self._routes.append((pattern, handler))

    def add_middleware(self, middleware: EdgeMiddleware) -> None:
        """Add middleware to the chain."""
        self._middleware.append(middleware)

    def match(self, path: str) -> EdgeFunction | None:
        """Match a path to a handler."""
        for pattern, handler in self._routes:
            if self._match_pattern(pattern, path):
                return handler
        return None

    def _match_pattern(self, pattern: str, path: str) -> bool:
        """Match a route pattern (supports * wildcards)."""
        if pattern == "/*":
            return True
        if "*" in pattern:
            prefix = pattern.rstrip("*")
            return path.startswith(prefix)
        return path == pattern

    async def handle(self, request: EdgeRequest) -> EdgeResponse:
        """Handle a request through middleware then routing."""
        handler = self.match(request.pathname)
        if handler is None:
            return EdgeResponse.json({"error": "Not found"}, status=404)

        # Build middleware chain
        async def run_middleware(idx: int, req: EdgeRequest) -> EdgeResponse:
            if idx >= len(self._middleware):
                return await handler.handle(req)
            return await self._middleware[idx].handle(req, lambda r: run_middleware(idx + 1, r))

        return await run_middleware(0, request)


# ---------------------------------------------------------------------------
# Cron Manager
# ---------------------------------------------------------------------------

class CronManager:
    """Manage scheduled/cron tasks at the edge."""

    def __init__(self) -> None:
        self._tasks: list[tuple[str, Callable[..., Awaitable[None]]]] = []

    def register(self, cron: str, handler: Callable[..., Awaitable[None]]) -> None:
        """Register a cron task."""
        self._tasks.append((cron, handler))

    async def run_due(self) -> list[str]:
        """Run any tasks that are due (simplified — checks minute alignment)."""
        now = datetime.now(timezone.utc)
        results = []
        for cron_expr, handler in self._tasks:
            if self._is_due(cron_expr, now):
                try:
                    event = ScheduledEvent(cron=cron_expr, scheduled_time=int(time.time() * 1000))
                    await handler(event)
                    results.append(cron_expr)
                except Exception as exc:
                    results.append(f"{cron_expr}: ERROR {exc}")
        return results

    def _is_due(self, cron: str, now: datetime) -> bool:
        """Check if a cron expression is due at the current time (simplified)."""
        parts = cron.split()
        if len(parts) != 5:
            return False
        minute, hour, day, month, dow = parts
        if minute != "*" and int(minute) != now.minute:
            return False
        if hour != "*" and int(hour) != now.hour:
            return False
        return True


# ---------------------------------------------------------------------------
# Edge Database Connection
# ---------------------------------------------------------------------------

class EdgeDatabasePool:
    """Connection pool for edge-compatible databases (Neon, PlanetScale, Turso)."""

    def __init__(self, connection_string: str, max_connections: int = 5) -> None:
        self.connection_string = connection_string
        self.max_connections = max_connections
        self._pool: list[dict[str, Any]] = []
        self._queries = 0

    async def query(self, sql: str, params: list | None = None) -> list[dict]:
        """Execute a query (simulated)."""
        self._queries += 1
        # In production, this would use neon-serverless, @planetscale/database, or @libsql/client
        return [{"sql": sql, "params": params or [], "mock": True}]

    @property
    def stats(self) -> dict[str, int]:
        return {"queries": self._queries, "pool_size": len(self._pool)}


# ---------------------------------------------------------------------------
# Demo / Main
# ---------------------------------------------------------------------------

async def main() -> None:
    """Demonstrate the Edge Runtime library."""
    print("=" * 70)
    print("Edge Runtime & Serverless Functions — Demo")
    print("=" * 70)

    # 1. Edge request and response
    print("\n[1] Edge Request & Response")
    request = EdgeRequest(
        url="https://example.com/dashboard?tab=overview",
        method="GET",
        headers={"Authorization": "Bearer token123"},
        cookies={"session": "abc123"},
        geo=GeoContext(country="DE", city="Berlin", continent="EU"),
        ip="203.0.113.1",
    )
    print(f"    Origin: {request.origin}")
    print(f"    Pathname: {request.pathname}")
    print(f"    Query: {request.query}")
    print(f"    Geo: {request.geo.country}, {request.geo.city} (EU: {request.geo.is_eu})")

    response = EdgeResponse.json({"status": "ok"}, status=200, headers={"X-Custom": "value"})
    print(f"    Response: status={response.status}, headers={list(response.headers.keys())}")

    # 2. KV Storage
    print("\n[2] KV Storage")
    kv = KVNamespace("CACHE_KV")
    await kv.put("user:123", '{"name": "Alice"}', expiration_ttl=300)
    await kv.put("user:456", '{"name": "Bob"}')
    await kv.put("session:abc", "token-data")

    user = await kv.get("user:123", type="json")
    print(f"    Get user:123 = {user}")

    missing = await kv.get("nonexistent")
    print(f"    Get nonexistent = {missing}")

    keys = await kv.list(KVListOptions(prefix="user:"))
    print(f"    List 'user:*': {[k.name for k in keys.keys]}")

    await kv.delete("user:456")
    print(f"    After delete, stats: {kv.get_stats()}")

    # 3. WebSocket Manager
    print("\n[3] WebSocket Manager")
    ws = WebSocketManager()
    ws.accept("ws-1")
    ws.accept("ws-2")
    print(f"    Active connections: {ws.active_connections}")

    ws.send("ws-1", "Hello!")
    sent = ws.broadcast("Broadcast message")
    print(f"    Broadcast sent to: {sent}")

    ws.close("ws-1")
    print(f"    After close ws-1: {ws.active_connections} active")

    # 4. Durable Object
    print("\n[4] Durable Object")
    do_info = DurableObjectInfo(id="do-room-1", class_name="ChatRoom", state=DurableObjectState.ACTIVE)
    durable_obj = DurableObject(do_info, env={"KV": kv})
    resp = await durable_obj.fetch(EdgeRequest(url="https://do.room.com/info"))
    print(f"    DO response: {resp.body}")

    await durable_obj.storage_put("last_message", "Hello world!")
    msg = await durable_obj.storage_get("last_message")
    print(f"    Storage get: {msg}")

    # 5. HTML Rewriter
    print("\n[5] HTML Rewriter")
    rewriter = HTMLRewriter()
    rewriter.on("title", {"element": lambda el: el.setInnerContent("Edge-Rendered Page")})
    rewriter.on("h1", {"element": lambda el: el.setInnerContent("Welcome from the Edge!")})

    original_html = "<html><head><title>Original</title></head><body><h1>Original Title</h1></body></html>"
    response = EdgeResponse.html(original_html)
    transformed = rewriter.transform(response)
    print(f"    Original: {original_html[:60]}...")
    print(f"    Transformed: {transformed.body[:60]}...")

    # 6. Rate Limiter
    print("\n[6] Rate Limiter")
    rl_kv = KVNamespace("RATE_LIMIT_KV")
    limiter = EdgeRateLimiter(
        RateLimitConfig(max_requests=5, window_seconds=60), rl_kv,
    )
    for i in range(7):
        allowed, headers = await limiter.check(request)
        print(f"    Request {i+1}: allowed={allowed}, remaining={headers.get('X-RateLimit-Remaining', '?')}")

    # 7. JWT Verifier
    print("\n[7] JWT Verification")
    import base64 as b64
    # Create a test JWT
    header = b64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    payload_data = {"sub": "user-123", "exp": int(time.time()) + 3600, "role": "admin"}
    payload = b64.urlsafe_b64encode(json.dumps(payload_data).encode()).rstrip(b"=").decode()
    signing_input = f"{header}.{payload}".encode()
    sig = hmac.new(b"test-secret-key", signing_input, hashlib.sha256).digest()
    token = f"{header}.{payload}.{b64.urlsafe_b64encode(sig).rstrip(b'=').decode()}"

    verifier = EdgeJWTVerifier("test-secret-key")
    verified = await verifier.verify(token)
    print(f"    Verified: sub={verified['sub']}, role={verified['role']}")

    # 8. Edge Router
    print("\n[8] Edge Router")
    router = EdgeRouter()
    router.add_route("/api/*", EdgeFunction())
    router.add_route("/dashboard", EdgeFunction())

    test_paths = ["/api/users", "/dashboard", "/unknown"]
    for path in test_paths:
        handler = router.match(path)
        print(f"    {path} -> {'Matched' if handler else 'Not found'}")

    # 9. Cron Manager
    print("\n[9] Cron Manager")
    cron = CronManager()
    cron.register("0 */6 * * *", lambda e: print(f"  Running 6-hour task"))
    cron.register("0 0 * * *", lambda e: print(f"  Running daily task"))

    # Simulate running at 00:00
    results = await cron.run_due()
    print(f"    Due tasks: {results}")

    # 10. Edge Database
    print("\n[10] Edge Database Pool")
    db = EdgeDatabasePool("postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/db")
    result = await db.query("SELECT * FROM users WHERE id = $1", [123])
    print(f"    Query result: {result}")
    print(f"    Stats: {db.stats}")

    # 11. Edge Metrics
    print("\n[11] Edge Metrics")
    metrics = EdgeMetrics()
    metrics.record_request(12.5)
    metrics.record_request(8.3)
    metrics.record_request(15.1)
    metrics.kv_reads = 10
    metrics.cache_hits = 7
    print(f"    Requests: {metrics.request_count}, Avg CPU: {metrics.avg_cpu_ms:.1f}ms")
    print(f"    KV reads: {metrics.kv_reads}, Cache hits: {metrics.cache_hits}")

    print("\n" + "=" * 70)
    print("Demo complete — all Edge Runtime patterns demonstrated")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
