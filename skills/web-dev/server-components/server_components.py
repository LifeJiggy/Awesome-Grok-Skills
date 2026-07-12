"""
server_components.py — React Server Components architecture library.

Provides abstractions for:
- Server Component and Client Component definitions
- Streaming SSR with Suspense boundaries
- RSC wire format serialization
- Component-level caching with React.cache()
- Server Actions with use server directive
- Progressive rendering with streaming
- Partial hydration management
- Client component interop boundaries

Designed for React 18+ with Server Components support.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
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
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ComponentType(Enum):
    """Server or Client component type."""
    SERVER = "server"
    CLIENT = "client"
    SHARED = "shared"  # Can run on either side


class RenderPhase(Enum):
    """Rendering pipeline phases."""
    SERIALIZE = "serialize"
    STREAM = "stream"
    HYDRATE = "hydrate"
    MOUNT = "mount"
    UPDATE = "update"
    UNMOUNT = "unmount"


class SuspenseStatus(Enum):
    """Status of a Suspense boundary."""
    PENDING = "pending"
    RESOLVED = "resolved"
    ERRORED = "errored"


class RSCRecordType(Enum):
    """RSC wire format record types."""
    COMPONENT = "C"
    CLIENT_REFERENCE = "D"
    SUSPENSE_BOUNDARY = "S"
    HTML_CHUNK = "H"
    FLUSH = "F"
    STRING = "T"
    ERROR = "E"
    FINISH = "."


class HydrationStatus(Enum):
    """Hydration lifecycle status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"


class CacheStrategy(Enum):
    """Component-level caching strategies."""
    NONE = "none"
    REQUEST = "request"        # Cache within a single request
    REVALIDATE = "revalidate"  # Time-based revalidation
    STATIC = "static"          # Never revalidate (build-time)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ComponentConfig:
    """Configuration for a React component."""
    type: ComponentType = ComponentType.SERVER
    ssr: bool = True
    streaming: bool = False
    cache_strategy: CacheStrategy = CacheStrategy.NONE
    cache_ttl: int = 0  # seconds, 0 = no cache
    tags: list[str] = field(default_factory=list)
    name: str | None = None

    @property
    def is_server(self) -> bool:
        return self.type == ComponentType.SERVER

    @property
    def is_client(self) -> bool:
        return self.type == ComponentType.CLIENT


@dataclass(frozen=True)
class SuspenseBoundary:
    """A Suspense boundary definition."""
    fallback: str
    component: type | None = None
    props: dict[str, Any] = field(default_factory=dict)
    name: str | None = None
    timeout_ms: int = 5000

    @property
    def boundary_id(self) -> str:
        return self.name or f"suspense-{uuid.uuid4().hex[:8]}"


@dataclass(frozen=True)
class RSCRecord:
    """A record in the RSC wire format."""
    type: RSCRecordType
    id: str
    data: Any = None
    children: list["RSCRecord"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HydrationState:
    """Tracks the hydration lifecycle of a component."""
    component_id: str
    status: HydrationStatus = HydrationStatus.NOT_STARTED
    started_at: int | None = None
    completed_at: int | None = None
    error: str | None = None

    @property
    def duration_ms(self) -> int | None:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None


@dataclass
class StreamingChunk:
    """A chunk of streamed HTML content."""
    id: str
    content: str
    boundary_id: str | None = None
    is_fallback: bool = False
    timestamp: float = field(default_factory=time.time)

    def to_rsc_record(self) -> RSCRecord:
        record_type = RSCRecordType.SUSPENSE_BOUNDARY if self.is_fallback else RSCRecordType.HTML_CHUNK
        return RSCRecord(type=record_type, id=self.id, data=self.content)


@dataclass
class CacheEntry:
    """A cached component render result."""
    component_id: str
    render_key: str
    result: str
    created_at: float = field(default_factory=time.time)
    ttl: int = 0  # seconds, 0 = never expires
    tags: list[str] = field(default_factory=list)

    @property
    def is_expired(self) -> bool:
        if self.ttl == 0:
            return False
        return time.time() > self.created_at + self.ttl


@dataclass
class ServerActionDescriptor:
    """Descriptor for a Server Action."""
    name: str
    function_id: str
    bound_args: list[Any] = field(default_factory=list)
    form_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class ComponentTree:
    """Represents a tree of components for rendering."""
    root: "BaseComponent"
    children: list["ComponentTree"] = field(default_factory=list)
    suspense_boundary: SuspenseBoundary | None = None
    is_client_boundary: bool = False


@dataclass
class RenderResult:
    """Result from rendering a component tree."""
    html: str
    rsc_payload: str
    component_count: int = 0
    client_component_count: int = 0
    server_component_count: int = 0
    streaming: bool = False
    cache_hits: int = 0
    cache_misses: int = 0
    render_time_ms: float = 0


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ServerComponentsError(Exception):
    """Base error for Server Components operations."""
    pass


class HydrationError(ServerComponentsError):
    """Client hydration failed."""
    def __init__(self, component_id: str, message: str):
        self.component_id = component_id
        super().__init__(f"Hydration error in {component_id}: {message}")


class SerializationError(ServerComponentsError):
    """Failed to serialize a value across server/client boundary."""
    def __init__(self, value: Any, reason: str):
        self.value = value
        super().__init__(f"Cannot serialize {type(value).__name__}: {reason}")


class SuspenseTimeoutError(ServerComponentsError):
    """A Suspense boundary timed out."""
    def __init__(self, boundary_id: str, timeout_ms: int):
        self.boundary_id = boundary_id
        self.timeout_ms = timeout_ms
        super().__init__(f"Suspense boundary '{boundary_id}' timed out after {timeout_ms}ms")


class StreamingError(ServerComponentsError):
    """Error during streaming SSR."""
    pass


class ServerActionError(ServerComponentsError):
    """Server Action execution failed."""
    def __init__(self, action_name: str, message: str, status: int = 500):
        self.action_name = action_name
        self.status = status
        super().__init__(f"ServerAction '{action_name}' failed ({status}): {message}")


# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------

@runtime_checkable
class RenderableProtocol(Protocol):
    """Protocol for components that can render."""
    async def render(self, props: dict[str, Any]) -> str: ...


@runtime_checkable
class CacheableProtocol(Protocol):
    """Protocol for components that support caching."""
    cache_config: ClassVar[ComponentConfig]
    async def render(self, props: dict[str, Any]) -> str: ...


# ---------------------------------------------------------------------------
# Base Component Classes
# ---------------------------------------------------------------------------

class BaseComponent:
    """Base class for all React components (Server and Client)."""

    config: ClassVar[ComponentConfig] = ComponentConfig()

    def __init__(self, props: dict[str, Any] | None = None) -> None:
        self.props = props or {}
        self._id = str(uuid.uuid4())
        self._hooks_state: dict[str, Any] = {}
        self._effect_queue: list[Callable[[], None]] = []

    @property
    def component_id(self) -> str:
        return self._id

    @property
    def component_name(self) -> str:
        return self.config.name or self.__class__.__name__

    def html(self, *parts: str) -> str:
        """Join HTML parts into a single string."""
        return "\n".join(parts)

    def escape(self, text: str) -> str:
        """Escape HTML special characters."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class ServerComponent(BaseComponent):
    """Server Component — runs only on the server, ships zero JS."""

    config: ClassVar[ComponentConfig] = ComponentConfig(type=ComponentType.SERVER)

    async def render(self, props: dict[str, Any]) -> str:
        """Override this method to define server-side rendering logic."""
        return self.html(f"<div>{self.component_name}</div>")

    async def fetch_data(self, query: str, params: dict | None = None) -> Any:
        """Simulate a database query (server-only)."""
        return {"query": query, "params": params or {}, "results": []}

    def create_cache_key(self, props: dict[str, Any]) -> str:
        """Generate a cache key from component props."""
        props_str = json.dumps(props, sort_keys=True, default=str)
        return hashlib.md5(f"{self.component_name}:{props_str}".encode()).hexdigest()


class ClientComponent(BaseComponent):
    """Client Component — hydrates on the client, has interactivity."""

    config: ClassVar[ComponentConfig] = ComponentConfig(type=ComponentType.CLIENT)

    def __init__(self, props: dict[str, Any] | None = None) -> None:
        super().__init__(props)
        self._state: dict[str, Any] = {}
        self._effects: list[Callable[[], None]] = []
        self._transitions: list[dict[str, Any]] = []

    def use_state(self, key: str, initial_value: Any) -> Any:
        """React-like useState hook."""
        if key not in self._state:
            self._state[key] = initial_value
        return self._state[key]

    def set_state(self, updates: dict[str, Any]) -> None:
        """React-like setState."""
        self._state.update(updates)

    def use_effect(self, effect_fn: Callable[[], None], deps: list | None = None) -> None:
        """React-like useEffect hook (simplified)."""
        self._effects.append(effect_fn)

    def use_transition(self) -> dict[str, Any]:
        """React-like useTransition hook."""
        return {"pending": False}

    def use_memo(self, fn: Callable[[], Any], deps: list) -> Any:
        """React-like useMemo hook."""
        return fn()

    def use_callback(self, fn: Callable, deps: list) -> Callable:
        """React-like useCallback hook."""
        return fn

    def render(self, props: dict[str, Any]) -> str:
        """Override this to define client-side rendering logic."""
        return self.html(f"<div class='client-component'>{self.component_name}</div>")


# ---------------------------------------------------------------------------
# Serialization (RSC Wire Format)
# ---------------------------------------------------------------------------

class RSCSerializer:
    """Serializes component trees into RSC wire format."""

    def serialize(self, component: BaseComponent, props: dict[str, Any] | None = None) -> str:
        """Serialize a component to RSC wire format."""
        records: list[str] = []

        record_type = RSCRecordType.CLIENT_REFERENCE if component.config.is_client else RSCRecordType.COMPONENT
        payload = {
            "name": component.component_name,
            "props": props or {},
            "type": record_type.value,
        }

        record = RSCRecord(
            type=record_type,
            id=component.component_id,
            data=payload,
        )

        records.append(self._format_record(record))
        return "".join(records)

    def _format_record(self, record: RSCRecord) -> str:
        """Format an RSC record as a line in the wire format."""
        data_str = json.dumps(record.data, default=str) if record.data else ""
        return f"{record.type.value}:{record.id}:{data_str}\n"

    def serialize_tree(self, tree: ComponentTree) -> str:
        """Serialize a full component tree."""
        parts = [self.serialize(tree.root)]
        for child in tree.children:
            parts.append(self.serialize_tree(child))
        return "".join(parts)


class RSCDeserializer:
    """Deserializes RSC wire format into component references."""

    def deserialize(self, payload: str) -> list[RSCRecord]:
        """Parse RSC wire format into records."""
        records = []
        for line in payload.strip().split("\n"):
            if not line:
                continue
            parts = line.split(":", 2)
            if len(parts) < 2:
                continue
            record_type = RSCRecordType(parts[0])
            record_id = parts[1]
            data = json.loads(parts[2]) if len(parts) > 2 and parts[2] else None
            records.append(RSCRecord(type=record_type, id=record_id, data=data))
        return records


# ---------------------------------------------------------------------------
# Streaming Renderer
# ---------------------------------------------------------------------------

class StreamingRenderer:
    """Manages streaming SSR with Suspense boundary resolution."""

    def __init__(self) -> None:
        self._chunks: list[StreamingChunk] = []
        self._boundaries: dict[str, SuspenseBoundary] = {}
        self._resolved: dict[str, str] = {}
        self._pending: set[str] = set()
        self._errors: dict[str, str] = {}

    def add_boundary(self, boundary: SuspenseBoundary) -> str:
        """Register a Suspense boundary and return its fallback HTML."""
        boundary_id = boundary.boundary_id
        self._boundaries[boundary_id] = boundary
        self._pending.add(boundary_id)

        chunk = StreamingChunk(
            id=f"chunk-{boundary_id}",
            content=boundary.fallback,
            boundary_id=boundary_id,
            is_fallback=True,
        )
        self._chunks.append(chunk)
        return boundary.fallback

    async def resolve_boundary(self, boundary_id: str, content: str) -> None:
        """Resolve a Suspense boundary with its final content."""
        if boundary_id not in self._boundaries:
            return
        self._resolved[boundary_id] = content
        self._pending.discard(boundary_id)

        chunk = StreamingChunk(
            id=f"resolved-{boundary_id}",
            content=content,
            boundary_id=boundary_id,
            is_fallback=False,
        )
        self._chunks.append(chunk)

    def error_boundary(self, boundary_id: str, error: str) -> None:
        """Mark a boundary as errored."""
        self._errors[boundary_id] = error
        self._pending.discard(boundary_id)

    async def resolve_all(self) -> str:
        """Resolve all boundaries and return complete HTML."""
        html_parts = []
        for chunk in self._chunks:
            if chunk.boundary_id and chunk.boundary_id in self._errors:
                html_parts.append(f'<div class="error-boundary">{self._errors[chunk.boundary_id]}</div>')
            elif chunk.boundary_id and chunk.boundary_id in self._resolved:
                html_parts.append(f'<div id="{chunk.boundary_id}">{self._resolved[chunk.boundary_id]}</div>')
            else:
                html_parts.append(chunk.content)
        return "\n".join(html_parts)

    @property
    def is_complete(self) -> bool:
        return len(self._pending) == 0

    @property
    def pending_count(self) -> int:
        return len(self._pending)

    def get_stream_script(self) -> str:
        """Generate client-side script for streaming updates."""
        return (
            "<script>"
            "(function(){"
            "const callbacks = {};"
            "window.__RSC_STREAM__ = {"
            "  onChunk: function(id, html) {"
            "    const el = document.getElementById(id);"
            "    if (el) el.innerHTML = html;"
            "    if (callbacks[id]) callbacks[id](html);"
            "  },"
            "  onReady: function(id, cb) { callbacks[id] = cb; }"
            "};"
            "})();"
            "</script>"
        )


# ---------------------------------------------------------------------------
# Component Cache
# ---------------------------------------------------------------------------

class ComponentCache:
    """Request-level and time-based component cache."""

    def __init__(self) -> None:
        self._cache: dict[str, CacheEntry] = {}
        self._request_cache: dict[str, str] = {}

    def get(self, key: str, is_request: bool = False) -> str | None:
        """Retrieve a cached render result."""
        if is_request:
            return self._request_cache.get(key)

        entry = self._cache.get(key)
        if entry and not entry.is_expired:
            return entry.result
        if entry and entry.is_expired:
            del self._cache[key]
        return None

    def set(self, key: str, result: str, ttl: int = 0, tags: list[str] | None = None, is_request: bool = False) -> None:
        """Cache a render result."""
        if is_request:
            self._request_cache[key] = result
            return

        self._cache[key] = CacheEntry(
            component_id=key,
            render_key=key,
            result=result,
            ttl=ttl,
            tags=tags or [],
        )

    def invalidate(self, tags: list[str] | None = None) -> int:
        """Invalidate cache entries, optionally by tags."""
        if not tags:
            count = len(self._cache)
            self._cache.clear()
            return count

        count = 0
        to_remove = []
        for key, entry in self._cache.items():
            if any(t in entry.tags for t in tags):
                to_remove.append(key)
        for key in to_remove:
            del self._cache[key]
            count += 1
        return count

    def clear_request_cache(self) -> None:
        """Clear the request-level cache (call at end of request)."""
        self._request_cache.clear()

    @property
    def stats(self) -> dict[str, int]:
        return {
            "entries": len(self._cache),
            "request_entries": len(self._request_cache),
            "total_size_bytes": sum(len(e.result) for e in self._cache.values()),
        }


# ---------------------------------------------------------------------------
# Hydration Manager
# ---------------------------------------------------------------------------

class HydrationManager:
    """Manages client-side hydration of Server Component output."""

    def __init__(self) -> None:
        self._states: dict[str, HydrationState] = {}
        self._client_components: dict[str, ClientComponent] = {}

    def register(self, component_id: str) -> None:
        """Register a component for hydration."""
        self._states[component_id] = HydrationState(component_id=component_id)

    def start_hydration(self, component_id: str) -> None:
        """Begin hydrating a component."""
        if component_id in self._states:
            state = self._states[component_id]
            self._states[component_id] = HydrationState(
                component_id=component_id,
                status=HydrationStatus.IN_PROGRESS,
                started_at=int(time.time() * 1000),
            )

    def complete_hydration(self, component_id: str) -> None:
        """Mark hydration as complete."""
        if component_id in self._states:
            state = self._states[component_id]
            self._states[component_id] = HydrationState(
                component_id=component_id,
                status=HydrationStatus.COMPLETE,
                started_at=state.started_at,
                completed_at=int(time.time() * 1000),
            )

    def fail_hydration(self, component_id: str, error: str) -> None:
        """Mark hydration as failed."""
        if component_id in self._states:
            state = self._states[component_id]
            self._states[component_id] = HydrationState(
                component_id=component_id,
                status=HydrationStatus.FAILED,
                started_at=state.started_at,
                error=error,
            )

    def get_stats(self) -> dict[str, Any]:
        """Get hydration statistics."""
        total = len(self._states)
        complete = sum(1 for s in self._states.values() if s.status == HydrationStatus.COMPLETE)
        failed = sum(1 for s in self._states.values() if s.status == HydrationStatus.FAILED)
        durations = [s.duration_ms for s in self._states.values() if s.duration_ms is not None]
        return {
            "total": total,
            "complete": complete,
            "failed": failed,
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
        }


# ---------------------------------------------------------------------------
# Server Action Manager
# ---------------------------------------------------------------------------

class ServerActionManager:
    """Manages Server Actions callable from Client Components."""

    def __init__(self) -> None:
        self._actions: dict[str, Callable[..., Awaitable[Any]]] = {}
        self._ids: dict[str, str] = {}

    def register(self, name: str, action: Callable[..., Awaitable[Any]]) -> str:
        """Register a Server Action and return its function ID."""
        function_id = hashlib.md5(name.encode()).hexdigest()[:12]
        self._actions[name] = action
        self._ids[name] = function_id
        return function_id

    async def execute(self, name: str, form_data: dict[str, Any] | None = None, bound_args: list | None = None) -> Any:
        """Execute a registered Server Action."""
        if name not in self._actions:
            raise ServerActionError(name, "Action not found", status=404)

        try:
            action = self._actions[name]
            result = await action(*(bound_args or []), **(form_data or {}))
            return result
        except ServerActionError:
            raise
        except Exception as exc:
            raise ServerActionError(name, str(exc), status=500) from exc

    def get_function_id(self, name: str) -> str | None:
        return self._ids.get(name)

    def list_actions(self) -> list[str]:
        return list(self._actions.keys())


# ---------------------------------------------------------------------------
# RSC Renderer (main orchestrator)
# ---------------------------------------------------------------------------

class RSCRenderer:
    """Main renderer orchestrating Server Components, streaming, and hydration."""

    def __init__(self) -> None:
        self.serializer = RSCSerializer()
        self.deserializer = RSCDeserializer()
        self.streaming = StreamingRenderer()
        self.cache = ComponentCache()
        self.hydration = HydrationManager()
        self.actions = ServerActionManager()
        self._component_count = 0
        self._client_count = 0
        self._server_count = 0

    async def render_component(
        self, component: BaseComponent, props: dict[str, Any] | None = None
    ) -> str:
        """Render a single component."""
        self._component_count += 1
        if component.config.is_client:
            self._client_count += 1
        else:
            self._server_count += 1

        # Check cache
        if component.config.cache_strategy != CacheStrategy.NONE:
            cache_key = component.create_cache_key(props or {})
            cached = self.cache.get(cache_key)
            if cached:
                return cached

        # Render
        if isinstance(component, ServerComponent):
            result = await component.render(props or {})
        else:
            result = component.render(props or {})

        # Cache result
        if component.config.cache_strategy == CacheStrategy.REVALIDATE:
            cache_key = component.create_cache_key(props or {})
            self.cache.set(cache_key, result, ttl=component.config.cache_ttl, tags=component.config.tags)

        return result

    async def render_tree(self, tree: ComponentTree) -> RenderResult:
        """Render a full component tree."""
        start_time = time.time()

        # Render root component
        root_html = await self.render_component(tree.root, tree.root.props)

        # Add Suspense boundaries
        if tree.suspense_boundary:
            self.streaming.add_boundary(tree.suspense_boundary)

        # Render children
        child_htmls = []
        for child in tree.children:
            child_result = await self.render_tree(child)
            child_htmls.append(child_result.html)

        html = root_html + "\n".join(child_htmls)
        rsc_payload = self.serializer.serialize_tree(tree)

        render_time = (time.time() - start_time) * 1000

        return RenderResult(
            html=html,
            rsc_payload=rsc_payload,
            component_count=self._component_count,
            client_component_count=self._client_count,
            server_component_count=self._server_count,
            streaming=self.streaming.pending_count > 0,
            cache_hits=0,
            cache_misses=0,
            render_time_ms=render_time,
        )

    async def render_page(self, components: list[tuple[BaseComponent, dict[str, Any]]]) -> RenderResult:
        """Render a full page with multiple components."""
        start_time = time.time()
        self._component_count = 0
        self._client_count = 0
        self._server_count = 0

        html_parts = []
        rsc_parts = []

        for component, props in components:
            html = await self.render_component(component, props)
            html_parts.append(html)
            rsc_parts.append(self.serializer.serialize(component, props))

            if component.config.is_client:
                self.hydration.register(component.component_id)
                self.hydration.start_hydration(component.component_id)
                self.hydration.complete_hydration(component.component_id)

        render_time = (time.time() - start_time) * 1000

        return RenderResult(
            html="\n".join(html_parts),
            rsc_payload="".join(rsc_parts),
            component_count=self._component_count,
            client_component_count=self._client_count,
            server_component_count=self._server_count,
            render_time_ms=render_time,
        )


# ---------------------------------------------------------------------------
# Demo / Main
# ---------------------------------------------------------------------------

async def main() -> None:
    """Demonstrate the Server Components architecture."""
    print("=" * 70)
    print("React Server Components Architecture — Demo")
    print("=" * 70)

    renderer = RSCRenderer()

    # 1. Server Component
    print("\n[1] Server Component")
    class WelcomeBanner(ServerComponent):
        config = ComponentConfig(type=ComponentType.SERVER, cache_strategy=CacheStrategy.REVALIDATE, cache_ttl=300)

        async def render(self, props: dict) -> str:
            return self.html(
                f'<div class="banner">',
                f'<h1>Welcome, {props.get("name", "Guest")}!</h1>',
                f'<p>Server-rendered at {datetime.now(timezone.utc).isoformat()}</p>',
                f'</div>',
            )

    banner = WelcomeBanner()
    result = await renderer.render_component(banner, {"name": "Alice"})
    print(f"    HTML: {result[:80]}...")

    # 2. Client Component
    print("\n[2] Client Component")
    class CounterButton(ClientComponent):
        config = ComponentConfig(type=ComponentType.CLIENT)

        def render(self, props: dict) -> str:
            count = self.use_state("count", 0)
            return self.html(
                f'<button class="counter">',
                f'Clicked {count} times',
                f'</button>',
            )

    counter = CounterButton({"initial": 0})
    html = counter.render({})
    print(f"    HTML: {html[:80]}...")

    # 3. Streaming renderer
    print("\n[3] Streaming Suspense")
    streaming = StreamingRenderer()
    streaming.add_boundary(SuspenseBoundary(fallback="<p>Loading...</p>", name="data-panel"))
    streaming.add_boundary(SuspenseBoundary(fallback="<p>Loading feed...</p>", name="activity-feed"))
    print(f"    Pending boundaries: {streaming.pending_count}")

    await streaming.resolve_boundary("data-panel", "<div>Data loaded!</div>")
    print(f"    After resolving 1: {streaming.pending_count} pending")

    await streaming.resolve_boundary("activity-feed", "<div>Feed loaded!</div>")
    print(f"    After resolving 2: {streaming.pending_count} pending")
    print(f"    Is complete: {streaming.is_complete}")

    final_html = await streaming.resolve_all()
    print(f"    Final HTML ({len(final_html)} chars)")

    # 4. Component cache
    print("\n[4] Component Cache")
    cache = ComponentCache()
    cache.set("user-123", "<div>User Alice</div>", ttl=300, tags=["users"])
    cache.set("post-456", "<div>Post title</div>", ttl=60, tags=["posts", "user-123"])

    hit = cache.get("user-123")
    print(f"    Cache hit: {hit}")
    miss = cache.get("nonexistent")
    print(f"    Cache miss: {miss}")
    invalidated = cache.invalidate(tags=["posts"])
    print(f"    Invalidated by 'posts' tag: {invalidated} entries")
    print(f"    Stats: {cache.stats}")

    # 5. Hydration manager
    print("\n[5] Hydration Manager")
    hydration = HydrationManager()
    hydration.register("comp-1")
    hydration.register("comp-2")
    hydration.start_hydration("comp-1")
    hydration.complete_hydration("comp-1")
    hydration.start_hydration("comp-2")
    hydration.fail_hydration("comp-2", "Mismatch in props")
    print(f"    Stats: {hydration.get_stats()}")

    # 6. Server Actions
    print("\n[6] Server Actions")
    actions = ServerActionManager()

    async def create_comment(body: str, post_id: str) -> dict:
        return {"id": str(uuid.uuid4()), "body": body, "post_id": post_id}

    actions.register("createComment", create_comment)
    result = await actions.execute("createComment", {"body": "Great post!", "post_id": "post-1"})
    print(f"    Action result: {result}")
    print(f"    Registered actions: {actions.list_actions()}")

    # 7. RSC Serialization
    print("\n[7] RSC Serialization")
    serializer = RSCSerializer()
    rsc_payload = serializer.serialize(banner, {"name": "Bob"})
    print(f"    RSC payload: {rsc_payload[:80]}...")

    deserializer = RSCDeserializer()
    records = deserializer.deserialize(rsc_payload)
    print(f"    Deserialized {len(records)} records")

    # 8. Full page render
    print("\n[8] Full Page Render")
    page_result = await renderer.render_page([
        (WelcomeBanner(), {"name": "Charlie"}),
        (CounterButton(), {}),
    ])
    print(f"    Components: {page_result.component_count} total ({page_result.server_component_count} server, {page_result.client_component_count} client)")
    print(f"    Render time: {page_result.render_time_ms:.2f}ms")
    print(f"    HTML length: {len(page_result.html)} chars")
    print(f"    RSC payload length: {len(page_result.rsc_payload)} chars")

    # 9. Streaming script
    print("\n[9] Streaming Client Script")
    script = streaming.get_stream_script()
    print(f"    Script ({len(script)} chars)")

    print("\n" + "=" * 70)
    print("Demo complete — all Server Components patterns demonstrated")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
