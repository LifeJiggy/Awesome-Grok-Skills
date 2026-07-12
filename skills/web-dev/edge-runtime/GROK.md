---
name: "edge-runtime"
category: "web-dev"
version: "1.0.0"
tags: ["web-dev", "edge", "cloudflare-workers", "serverless", "runtime"]
---

# Edge Runtime & Serverless Functions

## Overview

Edge computing brings code execution closer to users by running functions at network edge locations worldwide — typically within 50ms of any user, compared to 100-300ms for traditional serverless regions. The Edge Runtime (based on Web Standards: `Request`, `Response`, `URL`, `fetch`, `crypto`, `TextEncoder`) provides a lightweight, sandboxed JavaScript/TypeScript environment that boots in under 5ms, compared to 50-200ms for Node.js serverless functions. This makes edge functions ideal for latency-sensitive operations: auth checks, A/B testing, geo-routing, header manipulation, and edge-side rendering.

Major platforms implement the Edge Runtime differently: Cloudflare Workers use V8 isolates with the Workerd runtime (not Node.js), Vercel Edge Functions run on the same V8-based runtime integrated with their CDN, Deno Deploy uses V8 on their global network, and Netlify Edge Functions combine Deno with their CDN layer. Despite different implementations, they share the Web Standard APIs — making code largely portable. The key constraint is the absence of Node.js-specific APIs: no `fs`, no `child_process`, no `Buffer` (use `Uint8Array` instead), no Node.js crypto (use Web Crypto API), and limited npm package compatibility.

WebSocket support at the edge has become a critical capability. Cloudflare Durable Objects provide stateful WebSocket connections with persistent storage, enabling real-time applications like chat, collaborative editing, and live dashboards without a traditional backend. Vercel's Fluid Functions and Deno's native WebSocket support offer similar capabilities with different trade-offs.

Edge middleware sits between the CDN and the origin server, intercepting requests before they reach the application. In Next.js, middleware runs on the Edge Runtime and can modify headers, rewrite URLs, redirect, and even generate responses entirely — all without hitting the origin. Combined with KV storage (Cloudflare KV, Vercel KV, Deno KV) for fast key-value access at the edge, edge functions can maintain session state, cache API responses, and implement rate limiting without a database round-trip.

## Core Capabilities

- **Low-latency execution** — V8 isolate boot in <5ms, Web Standard APIs, no Node.js overhead
- **Geo-based routing** — Route users to different content based on country, region, language, or device
- **Edge middleware** — Intercept and modify requests before they reach the origin
- **WebSocket at the edge** — Real-time bidirectional communication with Durable Objects for state
- **KV storage** — Global key-value storage with eventual consistency (<5ms reads at the edge)
- **Edge-side rendering** — Render pages at the edge for dynamic, personalized content
- **Cron jobs at the edge** — Scheduled tasks running on global infrastructure
- **Edge-compatible database connections** — Neon, PlanetScale, Turso, and Supabase with connection pooling

## Usage Examples

### Edge Function with Geo-Routing

```python
from edge_runtime import EdgeFunction, Request, Response, GeoContext

class GeoRouter(EdgeFunction):
    """Route users based on their geographic location."""

    async def handle(self, request: Request) -> Response:
        geo = request.geo
        country = geo.country or "US"
        language = geo.language or "en"

        # Route to region-specific content
        routes = {
            "US": "/en-us/dashboard",
            "GB": "/en-gb/dashboard",
            "DE": "/de-de/dashboard",
            "JP": "/ja-jp/dashboard",
            "CN": "/zh-cn/dashboard",
        }

        target = routes.get(country, f"/{language}/dashboard")

        return Response.redirect(
            url=f"{request.origin}{target}",
            status=302,
            headers={"Vary": "Accept-Language, CF-IPCountry"},
        )
```

### Edge Middleware for Auth

```python
from edge_runtime import EdgeMiddleware, Request, Response, NextFunction

class AuthMiddleware(EdgeMiddleware):
    """Verify JWT at the edge before routing to origin."""

    PROTECTED_PATHS = ["/dashboard", "/settings", "/api/private"]
    PUBLIC_PATHS = ["/", "/login", "/register", "/api/auth/*"]

    async def handle(self, request: Request, next: NextFunction) -> Response:
        path = request.url.pathname

        # Skip public paths
        if any(path.startswith(p.rstrip("*")) for p in self.PUBLIC_PATHS):
            return await next(request)

        # Check protected paths
        if any(path.startswith(p) for p in self.PROTECTED_PATHS):
            token = request.cookies.get("session")

            if not token:
                return Response.redirect(f"{request.origin}/login?redirect={path}")

            try:
                payload = await self.verify_jwt(token)
                # Inject user info into headers for the origin
                request.headers["x-user-id"] = payload["sub"]
                request.headers["x-user-role"] = payload.get("role", "user")
            except JWTError:
                return Response.redirect(f"{request.origin}/login?expired=true")

        return await next(request)
```

### WebSocket with Durable Objects

```python
from edge_runtime import EdgeFunction, DurableObject, WebSocketPair

class ChatRoom(DurableObject):
    """Durable Object managing WebSocket connections for a chat room."""

    def __init__(self, state, env) -> None:
        self.state = state
        self.env = env
        self.connections: list[WebSocket] = []

    async def fetch(self, request: Request) -> Response:
        if request.url.endswith("/ws"):
            return self.handle_websocket(request)
        return Response.json({"connections": len(self.connections)})

    def handle_websocket(self, request: Request) -> Response:
        pair = WebSocketPair()
        server, client = pair.server, pair.client

        self.connections.append(server)
        server.accept()

        server.addEventListener("message", self.on_message)
        server.addEventListener("close", self.on_close)

        return Response.webSocket(client)

    def on_message(self, event) -> None:
        data = event.data
        # Broadcast to all connected clients
        for conn in self.connections:
            try:
                conn.send(data)
            except Exception:
                pass

    def on_close(self, event) -> None:
        self.connections = [c for c in self.connections if c.readyState != 3]
```

### KV Storage Operations

```python
from edge_runtime import EdgeFunction, KVNamespace

class KVHandler(EdgeFunction):
    """Read and write to KV storage at the edge."""

    def __init__(self, env: dict) -> None:
        self.kv: KVNamespace = env["CACHE_KV"]

    async def handle(self, request: Request) -> Response:
        if request.method == "GET":
            key = request.query.get("key")
            value = await self.kv.get(key)
            if value is None:
                return Response.json({"error": "Not found"}, status=404)
            return Response.json({"key": key, "value": value})

        elif request.method == "PUT":
            body = await request.json()
            key = body["key"]
            value = body["value"]
            ttl = body.get("ttl", 3600)  # 1 hour default
            await self.kv.put(key, value, expiration_ttl=ttl)
            return Response.json({"stored": True, "key": key, "ttl": ttl})

        elif request.method == "DELETE":
            key = request.query.get("key")
            await self.kv.delete(key)
            return Response.json({"deleted": True, "key": key})

        return Response.json({"error": "Method not allowed"}, status=405)
```

### Cron Job at the Edge

```python
from edge_runtime import EdgeFunction, ScheduledEvent

class ScheduledTask(EdgeFunction):
    """Run scheduled tasks at the edge."""

    async def scheduled(self, event: ScheduledEvent) -> None:
        cron = event.cron  # e.g., "0 */6 * * *"
        timestamp = event.scheduled_time

        if cron == "0 */6 * * *":
            # Every 6 hours: clean up expired sessions
            await self.cleanup_expired_sessions()

        elif cron == "0 0 * * *":
            # Daily: generate analytics report
            await self.generate_daily_report()

    async def cleanup_expired_sessions(self) -> None:
        kv = self.env["SESSIONS_KV"]
        # List and delete expired entries
        keys = await kv.list(prefix="session:")
        deleted = 0
        for key in keys.keys:
            value = await kv.get(key.name)
            if value and self.is_expired(value):
                await kv.delete(key.name)
                deleted += 1
        print(f"Cleaned up {deleted} expired sessions")

    def is_expired(self, session_data: str) -> bool:
        import json, time
        data = json.loads(session_data)
        return data.get("expires_at", 0) < time.time()

    async def generate_daily_report(self) -> None:
        print("Generating daily analytics report...")
```

### Edge-Side Rendering

```python
from edge_runtime import EdgeFunction, HTMLRewriter

class EdgeRenderer(EdgeFunction):
    """Render dynamic content at the edge using HTML rewriting."""

    async def handle(self, request: Request) -> Response:
        # Fetch the static page from origin
        origin_response = await fetch(f"{request.origin}/page.html")

        # Create an HTML rewriter to inject dynamic content
        rewriter = HTMLRewriter()

        # Replace the title
        rewriter.on("title", {
            "element": lambda el: el.setInnerContent(f"Edge-Rendered: {request.query.get('title', 'Page')}")
        })

        # Inject a personalized greeting
        rewriter.on("#greeting", {
            "element": lambda el: el.setInnerContent(
                f"Hello, {request.headers.get('x-user-name', 'Guest')}!"
            )
        })

        # Add geo-specific content
        country = request.geo.get("country", "US")
        rewriter.on("#geo-content", {
            "element": lambda el: el.setInnerContent(
                f"Welcome from {country}!"
            )
        })

        return rewriter.transform(origin_response)
```

### Rate Limiting at the Edge

```python
from edge_runtime import EdgeFunction, Request, Response
import time

class RateLimiter(EdgeFunction):
    """Token bucket rate limiter using KV storage."""

    def __init__(self, env: dict) -> None:
        self.kv = env["RATE_LIMIT_KV"]
        self.max_requests = 100
        self.window_seconds = 60

    async def handle(self, request: Request) -> Response:
        client_ip = request.headers.get("cf-connecting-ip", "unknown")
        key = f"rl:{client_ip}"

        # Get current count from KV
        data = await self.kv.get(key, type="json")
        now = int(time.time())

        if data is None or now - data["window_start"] > self.window_seconds:
            # New window
            data = {"count": 1, "window_start": now}
        else:
            data["count"] += 1

        # Store with TTL
        remaining_ttl = max(1, self.window_seconds - (now - data["window_start"]))
        await self.kv.put(key, json.dumps(data), expiration_ttl=remaining_ttl)

        # Check rate limit
        if data["count"] > self.max_requests:
            return Response.json(
                {"error": "Rate limit exceeded"},
                status=429,
                headers={
                    "Retry-After": str(remaining_ttl),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                },
            )

        return Response(
            status=200,
            headers={
                "X-RateLimit-Limit": str(self.max_requests),
                "X-RateLimit-Remaining": str(self.max_requests - data["count"]),
            },
        )
```

## Best Practices

1. **Keep functions small and focused** — Edge functions should do one thing: auth check, geo-route, rewrite headers, or serve a response. Large functions increase cold start and hit size limits (1MB for Workers, 4MB for Vercel Edge).

2. **Use KV for reads, Durable Objects for writes** — KV is eventually consistent (writes may take up to 60s to propagate) but fast for reads. Durable Objects provide strong consistency for writes and WebSocket state.

3. **Minimize dependencies** — Edge runtimes don't support all npm packages. Use Web Standard APIs (`fetch`, `crypto`, `URL`, `TextEncoder`) instead of Node.js equivalents. Check compatibility before importing.

4. **Cache aggressively at the edge** — Use `Cache-Control` headers and the Edge Cache API. Edge cache hits are served without hitting your function, saving CPU and reducing latency.

5. **Handle errors gracefully** — Edge functions can fail due to CPU limits, memory limits, or network issues. Always wrap handlers in try/catch and return meaningful error responses. Don't let errors propagate to the origin.

6. **Use `Vary` headers correctly** — When serving different content based on geo, language, or device, set appropriate `Vary` headers to prevent cache poisoning. `Vary: CF-IPCountry` for geo-based responses.

7. **Test locally before deploying** — Use Miniflare (Cloudflare), Vercel CLI, or Deno's edge test runner to test edge functions locally. Edge runtimes have different behaviors than Node.js — test in the actual runtime.

8. **Monitor with analytics** — Edge platforms provide real-time analytics. Monitor invocation counts, CPU time, error rates, and subrequest counts to identify performance bottlenecks.

## Related Modules

- **nextjs-fullstack** — Next.js middleware running on the Edge Runtime
- **supabase-auth** — Edge Function auth middleware for JWT verification
- **server-components** — Server Components with edge rendering
- **tailwind-shadcn** — CSS-in-JS considerations for edge rendering
