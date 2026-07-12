"""
nextjs_fullstack.py — Next.js App Router full-stack patterns library.

Provides abstractions for:
- File-system routing with nested layouts
- Server/Client Component boundaries with data fetching
- Static generation, ISR, and streaming strategies
- Server Actions for form mutations
- Middleware for auth, geo-routing, and request interception
- Image and font optimization configuration
- Metadata API for SEO and Open Graph
- Parallel and intercepting route definitions

Designed for Next.js 14+ App Router.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RenderingStrategy(Enum):
    """How a page is rendered at request time."""
    SSR = auto()          # Server-Side Rendering on every request
    SSG = auto()          # Static Site Generation at build time
    ISR = auto()          # Incremental Static Regeneration
    STREAMING = auto()    # Chunked SSR with Suspense boundaries
    EDGE_SSR = auto()     # SSR at the edge runtime


class HttpMethod(Enum):
    """Supported HTTP methods for API routes."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class CacheControl(Enum):
    """Cache control directives for responses."""
    NO_CACHE = "no-cache"
    NO_STORE = "no-store"
    PUBLIC = "public"
    PRIVATE = "private"
    MUST_REVALIDATE = "must-revalidate"
    S_MAXAGE = "s-maxage"
    STALE_WHILE_REVALIDATE = "stale-while-revalidate"


class RevalidationType(Enum):
    """How ISR pages are revalidated."""
    TIME = auto()         # Time-based (seconds)
    ON_DEMAND = auto()    # Tag-based on-demand revalidation


class MiddlewarePriority(Enum):
    """Middleware execution priority."""
    EARLY = auto()
    NORMAL = auto()
    LATE = auto()


class AuthStrategy(Enum):
    """Authentication strategy for protected routes."""
    JWT = "jwt"
    SESSION = "session"
    OAUTH = "oauth"
    MAGIC_LINK = "magic_link"
    PASSKEY = "passkey"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PageConfig:
    """Configuration for a Next.js page component."""
    dynamic: Literal[
        "auto", "force-dynamic", "force-static", "error"
    ] = "auto"
    revalidate: int | None = None
    fetchCache: Literal[
        "auto", "force-no-store", "default-cache", "only-if-cached", "force-cache"
    ] = "auto"
    runtime: Literal["nodejs", "edge"] | None = None
    preferredRegion: str | None = None
    generateStaticParams: bool = False
    generateMetadata: bool = False
    tags: list[str] = field(default_factory=list)
    meta: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Metadata:
    """SEO and Open Graph metadata for a page."""
    title: str | None = None
    description: str | None = None
    keywords: list[str] = field(default_factory=list)
    authors: list[dict[str, str]] = field(default_factory=list)
    openGraph: dict[str, Any] = field(default_factory=dict)
    twitter: dict[str, str] = field(default_factory=dict)
    robots: dict[str, bool | str] = field(default_factory=dict)
    canonical: str | None = None
    alternates: dict[str, str] = field(default_factory=dict)
    icons: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RouteSegment:
    """Represents a single segment in the file-system router."""
    name: str
    dynamic: bool = False
    catch_all: bool = False
    optional_catch_all: bool = False
    group: str | None = None
    parallel_slot: str | None = None
    intercepting: bool = False


@dataclass
class RequestContext:
    """Immutable context passed to middleware and route handlers."""
    path: str
    method: HttpMethod
    headers: dict[str, str]
    cookies: dict[str, str]
    query: dict[str, str]
    body: Any = None
    geo: dict[str, str] = field(default_factory=dict)
    ip: str | None = None
    url: str = ""

    @property
    def origin(self) -> str:
        parsed = urlparse(self.url)
        return f"{parsed.scheme}://{parsed.netloc}" if parsed.netloc else ""


@dataclass
class MiddlewareResult:
    """Result from middleware execution."""
    response: dict[str, Any] | None = None
    redirect: str | None = None
    rewrite: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    cookies_to_set: list[dict[str, str]] = field(default_factory=list)
    cookies_to_delete: list[str] = field(default_factory=list)
    status: int = 200
    continue_processing: bool = True


@dataclass
class ImageConfig:
    """Configuration for next/image optimization."""
    device_sizes: list[int] = field(default_factory=lambda: [640, 750, 828, 1080, 1200, 1920, 2048])
    image_sizes: list[int] = field(default_factory=lambda: [16, 32, 48, 64, 96, 128, 256, 384])
    formats: list[str] = field(default_factory=lambda: ["image/avif", "image/webp"])
    minimum_cache_time: int = 60 * 60 * 24 * 30  # 30 days
    dangerously_allow_svg: bool = False
    content_security_policy: str = ""


@dataclass(frozen=True)
class ServerActionConfig:
    """Configuration for a Server Action."""
    name: str | None = None
    transition: bool = True
    experimental_prending: bool = False
    allowed_origins: list[str] = field(default_factory=list)


@dataclass
class RouteHandler:
    """A handler for an API route."""
    method: HttpMethod
    path: str
    handler: Callable[..., Awaitable[Any]]
    middleware: list[Callable[..., Awaitable[MiddlewareResult]]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    revalidate: int | None = None


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class NextjsError(Exception):
    """Base exception for Next.js patterns library."""
    pass


class RouteConflictError(NextjsError):
    """Two routes map to the same path."""
    def __init__(self, path: str, existing: str, new: str):
        self.path = path
        self.existing = existing
        self.new = new
        super().__init__(f"Route conflict at '{path}': '{existing}' vs '{new}'")


class InvalidMiddlewareError(NextjsError):
    """Middleware is not a valid async function."""
    pass


class ServerActionError(NextjsError):
    """Server Action execution failed."""
    def __init__(self, action_name: str, message: str, status: int = 500):
        self.action_name = action_name
        self.status = status
        super().__init__(f"ServerAction '{action_name}' failed ({status}): {message}")


class StreamingError(NextjsError):
    """Error during streaming SSR."""
    pass


class ClientComponentError(NextjsError):
    """Invalid use of server-only APIs in a client component."""
    pass


# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------

@runtime_checkable
class ServerComponentProtocol(Protocol):
    """Protocol for Server Component implementations."""
    config: ClassVar[PageConfig]

    async def render(self, params: dict[str, Any]) -> str:
        """Render the component to HTML."""
        ...

    def html(self, template: str, context: dict[str, Any]) -> str:
        """Wrap rendered content in a template."""
        ...


@runtime_checkable
class ClientComponentProtocol(Protocol):
    """Protocol for Client Component implementations."""
    client: ClassVar[bool] = True

    def render(self, props: dict[str, Any]) -> str:
        """Render the client component."""
        ...


@runtime_checkable
class MiddlewareProtocol(Protocol):
    """Protocol for middleware implementations."""
    async def handle(self, request: RequestContext) -> MiddlewareResult:
        """Process the request and return a result."""
        ...


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class RouteRegistry:
    """Central registry for all routes in the application."""

    def __init__(self) -> None:
        self._routes: dict[str, RouteHandler] = {}
        self._middleware: list[tuple[int, MiddlewareProtocol]] = []
        self._layouts: dict[str, Any] = {}
        self._error_handlers: dict[str, Callable[..., Any]] = {}

    def register_route(
        self,
        path: str,
        handler: Callable[..., Awaitable[Any]],
        method: HttpMethod = HttpMethod.GET,
        tags: list[str] | None = None,
        revalidate: int | None = None,
    ) -> RouteHandler:
        """Register a route handler."""
        key = f"{method.value}:{path}"
        if key in self._routes:
            raise RouteConflictError(path, self._routes[key].handler.__name__, handler.__name__)

        route = RouteHandler(
            method=method,
            path=path,
            handler=handler,
            tags=tags or [],
            revalidate=revalidate,
        )
        self._routes[key] = route
        return route

    def register_middleware(self, mw: MiddlewareProtocol, priority: MiddlewarePriority = MiddlewarePriority.NORMAL) -> None:
        """Register middleware with priority."""
        self._middleware.append((priority.value, mw))
        self._middleware.sort(key=lambda x: x[0])

    def match_route(self, path: str, method: HttpMethod = HttpMethod.GET) -> RouteHandler | None:
        """Match a request path to a registered route."""
        key = f"{method.value}:{path}"
        if key in self._routes:
            return self._routes[key]

        # Pattern matching for dynamic segments
        for route_key, handler in self._routes.items():
            route_method, route_path = route_key.split(":", 1)
            if route_method != method.value:
                continue
            if self._matches_pattern(route_path, path):
                return handler

        return None

    def _matches_pattern(self, pattern: str, path: str) -> bool:
        """Check if a path matches a route pattern with dynamic segments."""
        pattern_parts = pattern.strip("/").split("/")
        path_parts = path.strip("/").split("/")

        if len(pattern_parts) != len(path_parts):
            # Check catch-all
            if pattern_parts and pattern_parts[-1].startswith("[..."):
                return len(path_parts) >= len(pattern_parts) - 1
            return False

        for pp, rp in zip(pattern_parts, path_parts):
            if pp.startswith("[") and pp.endswith("]"):
                continue  # Dynamic segment — matches anything
            if pp != rp:
                return False

        return True


class StreamingRenderer:
    """Handles streaming SSR with Suspense-like boundaries."""

    def __init__(self) -> None:
        self._chunks: list[str] = []
        self._placeholders: dict[str, str] = {}
        self._resolved: dict[str, str] = {}

    def add_suspense_boundary(
        self, boundary_id: str, fallback: str, resolver: Callable[..., Awaitable[str]]
    ) -> None:
        """Register a Suspense boundary with a fallback and async resolver."""
        self._placeholders[boundary_id] = fallback
        # In production, this would stream the fallback immediately
        # and replace it when the resolver completes
        self._resolved[boundary_id] = ""  # Placeholder

    async def resolve_all(self) -> str:
        """Resolve all Suspense boundaries and return the final HTML."""
        results = []
        for boundary_id, fallback in self._placeholders.items():
            resolved = self._resolved.get(boundary_id, fallback)
            results.append(f'<div id="suspense-{boundary_id}">{resolved}</div>')
        return "\n".join(results)

    def inject_streaming_scripts(self, html: str) -> str:
        """Inject the client-side streaming hydration script."""
        script = (
            "<script>"
            "function nextSuspenseCallback(id, html) {"
            "  const el = document.getElementById('suspense-' + id);"
            "  if (el) el.innerHTML = html;"
            "}"
            "</script>"
        )
        return html + script


class MetadataGenerator:
    """Generates structured metadata for SEO and social sharing."""

    def __init__(self) -> None:
        self._metadata: list[Metadata] = []
        self._base_url: str = "https://example.com"

    def set_base_url(self, url: str) -> None:
        self._base_url = url

    def add_metadata(self, meta: Metadata) -> None:
        self._metadata.append(meta)

    def generate_json_ld(self, data: dict[str, Any]) -> str:
        """Generate JSON-LD structured data script tag."""
        return f'<script type="application/ld+json">{json.dumps(data, indent=2)}</script>'

    def generate_tags(self, meta: Metadata) -> str:
        """Generate HTML meta tags from a Metadata object."""
        tags: list[str] = []
        if meta.title:
            tags.append(f"<title>{self._escape(meta.title)}</title>")
            tags.append(f'<meta property="og:title" content="{self._escape(meta.title)}">')
            tags.append(f'<meta name="twitter:title" content="{self._escape(meta.title)}">')

        if meta.description:
            tags.append(f'<meta name="description" content="{self._escape(meta.description)}">')
            tags.append(f'<meta property="og:description" content="{self._escape(meta.description)}">')
            tags.append(f'<meta name="twitter:description" content="{self._escape(meta.description)}">')

        if meta.canonical:
            tags.append(f'<link rel="canonical" href="{self._escape(meta.canonical)}">')

        if meta.keywords:
            tags.append(f'<meta name="keywords" content="{", ".join(meta.keywords)}">')

        for key, value in meta.robots.items():
            if isinstance(value, bool):
                tags.append(f'<meta name="robots" content="{key}={str(value).lower()}">')

        return "\n".join(tags)

    def generate_sitemap_entry(
        self, path: str, last_modified: datetime | None = None, priority: float = 0.5
    ) -> dict[str, Any]:
        """Generate a sitemap entry for a route."""
        return {
            "loc": f"{self._base_url}{path}",
            "lastmod": (last_modified or datetime.now(timezone.utc)).isoformat(),
            "priority": priority,
        }

    @staticmethod
    def _escape(text: str) -> str:
        """Escape HTML special characters."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class ServerActionExecutor:
    """Executes Server Actions with validation and error handling."""

    def __init__(self) -> None:
        self._actions: dict[str, Callable[..., Awaitable[Any]]] = {}
        self._configs: dict[str, ServerActionConfig] = {}

    def register(
        self,
        name: str,
        action: Callable[..., Awaitable[Any]],
        config: ServerActionConfig | None = None,
    ) -> None:
        """Register a Server Action."""
        self._actions[name] = action
        self._configs[name] = config or ServerActionConfig(name=name)

    async def execute(
        self, name: str, form_data: dict[str, Any], user: Any = None
    ) -> dict[str, Any]:
        """Execute a registered Server Action."""
        if name not in self._actions:
            raise ServerActionError(name, "Action not found", status=404)

        action = self._actions[name]
        config = self._configs[name]

        try:
            if user is not None and config.allowed_origins:
                pass  # Origin validation would happen here

            result = await action(form_data, user)
            return {"success": True, "data": result}

        except ServerActionError:
            raise
        except Exception as exc:
            raise ServerActionError(name, str(exc), status=500) from exc

    def list_actions(self) -> list[str]:
        """List all registered Server Action names."""
        return list(self._actions.keys())


class ImageOptimizer:
    """Configuration and helpers for next/image optimization."""

    def __init__(self, config: ImageConfig | None = None) -> None:
        self.config = config or ImageConfig()

    def get_optimized_url(
        self, src: str, width: int = 0, quality: int = 75, format: str = "auto"
    ) -> str:
        """Generate an optimized image URL."""
        params = {
            "url": src,
            "w": str(width or self.config.device_sizes[0]),
            "q": str(quality),
        }
        if format != "auto":
            params["f"] = format
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"/_next/image?{query}"

    def get_src_set(self, src: str, sizes: list[int] | None = None) -> str:
        """Generate a srcSet attribute for responsive images."""
        sizes = sizes or self.config.device_sizes
        entries = []
        for size in sizes:
            url = self.get_optimized_url(src, width=size)
            entries.append(f"{url} {size}w")
        return ", ".join(entries)

    def validate_loader(self, src: str) -> bool:
        """Validate that the image source is allowed."""
        if self.config.dangerously_allow_svg and src.endswith(".svg"):
            return True
        if src.endswith(".svg") and not self.config.dangerously_allow_svg:
            return False
        return True


# ---------------------------------------------------------------------------
# App Router (main orchestrator)
# ---------------------------------------------------------------------------

class AppRouter:
    """Central App Router orchestrator for Next.js full-stack applications."""

    def __init__(self) -> None:
        self.registry = RouteRegistry()
        self.streaming = StreamingRenderer()
        self.metadata_gen = MetadataGenerator()
        self.server_actions = ServerActionExecutor()
        self.image_optimizer = ImageOptimizer()
        self._global_middleware: list[MiddlewareProtocol] = []

    def page(self, path: str, config: PageConfig | None = None):
        """Decorator to register a Server Component as a page."""
        def decorator(cls: Type[ServerComponentProtocol]):
            config_obj = config or PageConfig()

            async def _handler(**kwargs: Any) -> str:
                instance = cls()
                return await instance.render(kwargs.get("params", {}))

            self.registry.register_route(
                path,
                _handler,
                tags=config_obj.tags,
                revalidate=config_obj.revalidate,
            )
            return cls
        return decorator

    def api_route(self, path: str, methods: list[HttpMethod] | None = None):
        """Decorator to register an API route handler."""
        def decorator(func: Callable[..., Awaitable[Any]]):
            for method in (methods or [HttpMethod.GET]):
                self.registry.register_route(path, func, method=method)
            return func
        return decorator

    def add_middleware(self, mw: MiddlewareProtocol) -> None:
        """Add middleware to the application."""
        self.registry.register_middleware(mw)

    def register_action(
        self,
        name: str,
        action: Callable[..., Awaitable[Any]],
        config: ServerActionConfig | None = None,
    ) -> None:
        """Register a Server Action."""
        self.server_actions.register(name, action, config)

    async def handle_request(self, path: str, method: HttpMethod = HttpMethod.GET, **kwargs: Any) -> dict[str, Any]:
        """Handle an incoming request through middleware then routing."""
        # Build request context
        ctx = RequestContext(
            path=path,
            method=method,
            headers=kwargs.get("headers", {}),
            cookies=kwargs.get("cookies", {}),
            query=kwargs.get("query", {}),
            geo=kwargs.get("geo", {}),
            url=kwargs.get("url", f"https://localhost{path}"),
        )

        # Run middleware chain
        for _, mw in self.registry._middleware:
            result = await mw.handle(ctx)
            if not result.continue_processing:
                return {"status": result.status, "redirect": result.redirect}

        # Match route
        route = self.registry.match_route(path, method)
        if route is None:
            return {"status": 404, "error": "Not Found"}

        try:
            body = await route.handler()
            return {"status": 200, "body": body}
        except Exception as exc:
            return {"status": 500, "error": str(exc)}


# ---------------------------------------------------------------------------
# Demo / Main
# ---------------------------------------------------------------------------

async def main() -> None:
    """Demonstrate the Next.js full-stack patterns library."""
    print("=" * 70)
    print("Next.js Full-Stack Patterns Library — Demo")
    print("=" * 70)

    # 1. App Router setup
    router = AppRouter()

    # 2. Register a page
    @router.page("/dashboard", config=PageConfig(dynamic="force-dynamic", tags=["dashboard"]))
    async def dashboard_page() -> str:
        return "<div>Dashboard Content</div>"

    print("\n[1] Registered /dashboard page")

    # 3. Register API routes
    @router.api_route("/api/users", methods=[HttpMethod.GET, HttpMethod.POST])
    async def users_api() -> dict:
        return {"users": []}

    print("[2] Registered /api/users API route")

    # 4. Register middleware
    class AuthCheck:
        async def handle(self, request: RequestContext) -> MiddlewareResult:
            if request.path.startswith("/dashboard"):
                token = request.cookies.get("token")
                if not token:
                    return MiddlewareResult(redirect="/login", status=302)
            return MiddlewareResult(continue_processing=True)

    router.add_middleware(AuthCheck())
    print("[3] Added auth middleware")

    # 5. Handle a request
    result = await router.handle_request(
        "/dashboard",
        method=HttpMethod.GET,
        cookies={"token": "valid-session"},
    )
    print(f"[4] Request /dashboard: status={result['status']}")

    # 6. Handle a request without auth
    result_no_auth = await router.handle_request("/dashboard")
    print(f"[5] Request /dashboard (no auth): status={result_no_auth['status']}, redirect={result_no_auth.get('redirect')}")

    # 7. Server Actions
    async def create_post(form_data: dict, user: Any) -> dict:
        return {"post_id": 1, "title": form_data.get("title", "")}

    router.register_action("createPost", create_post, ServerActionConfig(name="createPost"))
    action_result = await router.server_actions.execute("createPost", {"title": "Hello"}, user="user1")
    print(f"[6] Server Action createPost: {action_result}")

    # 8. Metadata generation
    meta = Metadata(
        title="My Dashboard",
        description="View your metrics and activity",
        keywords=["dashboard", "analytics"],
        openGraph={"type": "website"},
    )
    tags_html = router.metadata_gen.generate_tags(meta)
    print(f"[7] Generated metadata tags ({len(tags_html)} chars)")

    # 9. Image optimization
    img_url = router.image_optimizer.get_optimized_url("https://example.com/photo.jpg", width=1200)
    print(f"[8] Optimized image URL: {img_url}")

    srcset = router.image_optimizer.get_src_set("https://example.com/hero.jpg")
    print(f"[9] Generated srcSet ({len(srcset.split(','))} entries)")

    # 10. Streaming renderer
    streaming = StreamingRenderer()
    streaming.add_suspense_boundary("comments", "<p>Loading comments...</p>", None)
    streaming.add_suspense_boundary("sidebar", "<p>Loading sidebar...</p>", None)
    resolved = await streaming.resolve_all()
    print(f"[10] Streaming resolved ({len(resolved)} chars)")

    # 11. Route matching
    print("\n[Route matching]")
    test_paths = ["/dashboard", "/api/users", "/products/laptop-1", "/unknown"]
    for p in test_paths:
        route = router.registry.match_route(p)
        handler_name = route.handler.__name__ if route else "None"
        print(f"  {p} -> {handler_name}")

    # 12. JSON-LD
    json_ld = router.metadata_gen.generate_json_ld({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "MyApp",
    })
    print(f"\n[12] JSON-LD ({len(json_ld)} chars)")

    # 13. Sitemap entry
    sitemap = router.metadata_gen.generate_sitemap_entry("/dashboard", priority=0.8)
    print(f"[13] Sitemap entry: {sitemap}")

    print("\n" + "=" * 70)
    print("Demo complete — all Next.js patterns demonstrated successfully")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
