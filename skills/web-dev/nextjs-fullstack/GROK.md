---
name: "nextjs-fullstack"
category: "web-dev"
version: "1.0.0"
tags: ["web-dev", "nextjs", "fullstack", "app-router", "react"]
---

# Next.js Full-Stack Development

## Overview

Next.js App Router represents the evolution of React full-stack development, introducing a file-system based routing convention that unifies server and client rendering strategies under a single mental model. The App Router (introduced in Next.js 13, stable in 14+) replaces the legacy Pages Router with a layout-first architecture where `layout.js`, `page.js`, `loading.js`, and `error.js` compose a nested routing tree. Each segment in the file system maps to a URL path, and the component hierarchy is derived from the folder nesting Ã¢â‚¬â€ eliminating manual route configuration entirely.

Server Components are the default rendering strategy in the App Router. Every component in `app/` runs on the server unless explicitly marked with `'use client'`. This means data fetching happens at the component level without `useEffect`, `getServerSideProps`, or client-side state management. The server can directly query databases, call internal APIs, read the filesystem, and stream HTML to the browser while the client hydrates progressively. Client Components handle interactivity Ã¢â‚¬â€ event handlers, browser APIs, state, and effects Ã¢â‚¬â€ and are serialized across the server-client boundary as React Server Component payloads.

The full-stack capability extends to API routes colocated with pages, middleware that runs at the edge before routing, image optimization via the `next/image` component, font optimization with `next/font`, and metadata generation through the Metadata API. Server Actions (available since Next.js 14) enable form submissions and mutations directly from Server Components without creating separate API endpoints, completing the full-stack loop where the same codebase handles rendering, data, and mutations.

## Core Capabilities

- **File-system routing with layouts** Ã¢â‚¬â€ Nested folders define URL segments; shared layouts persist across navigations without remounting
- **Server/Client Component boundaries** Ã¢â‚¬â€ Default server rendering with explicit `'use client'` for interactive islands
- **Multi-strategy data fetching** Ã¢â‚¬â€ SSR (request-time), SSG (build-time), ISR (revalidated), and Streaming (chunked HTML)
- **Server Actions** Ã¢â‚¬â€ Form mutations directly from Server Components without API route boilerplate
- **Middleware** Ã¢â‚¬â€ Edge-compatible request/response interception for auth, redirects, rewrites, and geo-routing
- **Image and font optimization** Ã¢â‚¬â€ Automatic WebP/AVIF conversion, lazy loading, layout shift prevention, and font self-hosting
- **Metadata API** Ã¢â‚¬â€ SEO, Open Graph, JSON-LD, and sitemap generation through structured exports
- **Parallel and intercepting routes** Ã¢â‚¬â€ Modal overlays, shared layouts across route groups, and route interception for UX patterns

## Usage Examples

### Basic App Router Page with Server Component Data Fetching

```python
# nextjs_fullstack.py Ã¢â‚¬â€ conceptual example of App Router page structure
from nextjs_fullstack import AppRouter, PageConfig, ServerComponent

router = AppRouter()

# Define a page that fetches data server-side at request time
@router.page("/dashboard")
class DashboardPage(ServerComponent):
    """Server Component Ã¢â‚¬â€ runs on the server, no client JS shipped."""

    config = PageConfig(
        dynamic="force-dynamic",  # SSR on every request
        revalidate=0,
    )

    async def render(self, params: dict) -> str:
        # Direct database query Ã¢â‚¬â€ no API layer needed
        user = await self.db.users.find_unique(where={"id": params["userId"]})
        metrics = await self.fetch_metrics(user.org_id)

        return self.html(
            template="dashboard.html",
            context={"user": user, "metrics": metrics},
        )
```

### Static Generation with ISR Revalidation

```python
from nextjs_fullstack import ISRPage, RevalidationStrategy

class ProductPage(ISRPage):
    """Static generation with Incremental Static Regeneration."""

    config = ISRPage.config(
        revalidate=3600,  # Revalidate every hour
        tags=["products"],  # On-demand revalidation tag
    )

    async def generate_static_params(self) -> list[dict]:
        products = await self.db.products.find_many()
        return [{"slug": p.slug} for p in products]

    async def render(self, params: dict) -> str:
        product = await self.db.products.find_unique(
            where={"slug": params["slug"]}
        )
        return self.html("product.html", {"product": product})
```

### Middleware for Auth and Geo-Routing

```python
from nextjs_fullstack import Middleware, Request, Response, NextResponse

class AuthMiddleware(Middleware):
    PROTECTED_PATHS = ["/dashboard", "/settings", "/api/private"]
    PUBLIC_PATHS = ["/", "/login", "/register", "/api/auth"]

    async def handle(self, request: Request) -> Response:
        token = request.cookies.get("session_token")

        if request.path in self.PROTECTED_PATHS:
            if not token:
                return NextResponse.redirect("/login")
            try:
                session = await self.verify_session(token)
                request.headers["x-user-id"] = str(session.user_id)
            except InvalidSessionError:
                return NextResponse.redirect("/login")

        # Geo-based routing
        country = request.geo.get("country", "US")
        if country == "EU":
            request.headers["x-locale"] = "de-DE"
        elif country == "JP":
            request.headers["x-locale"] = "ja-JP"
        else:
            request.headers["x-locale"] = "en-US"

        return NextResponse.next()
```

### Server Actions for Mutations

```python
from nextjs_fullstack import ServerAction, useFormStatus, useTransition

class CreatePostAction(ServerAction):
    """Server Action Ã¢â‚¬â€ called from a form in a Server Component."""

    async def execute(self, form_data: dict, user: AuthenticatedUser):
        title = form_data["title"]
        body = form_data["body"]

        if len(title) < 3:
            return {"error": "Title must be at least 3 characters"}

        post = await self.db.posts.create({
            "title": title,
            "body": body,
            "author_id": user.id,
        })

        # Revalidate cached pages showing posts
        self.revalidate_tag("posts")

        return {"success": True, "post_id": post.id}
```

### Parallel Routes for Modal Patterns

```python
from nextjs_fullstack import ParallelRoute, InterceptingRoute

# app/dashboard/@modal/(..)photo/[id]/page.tsx pattern
@router.parallel_route("modal")
class ModalSlot(InterceptingRoute):
    """Intercepting route Ã¢â‚¬â€ renders as modal over parent layout."""

    async def render(self, params: dict) -> str:
        photo = await self.db.photos.find_unique(where={"id": params["id"]})
        return self.html("modal-photo.html", {"photo": photo})

    def fallback(self) -> str:
        return ""  # Empty when not intercepted
```

## Best Practices

1. **Default to Server Components** Ã¢â‚¬â€ Only add `'use client'` when the component needs event handlers, browser APIs, or React hooks like `useState`/`useEffect`. Every client component adds JavaScript to the bundle.

2. **Colocate data fetching with components** Ã¢â‚¬â€ Fetch data in the component that renders it, not in a parent. This enables independent loading states via `loading.js` and streaming.

3. **Use `loading.js` for streaming** Ã¢â‚¬â€ Create a `loading.js` file in any route segment to show instant loading UI while the server component streams data.

4. **Cache aggressively, revalidate intentionally** Ã¢â‚¬â€ Default fetch requests in Server Components are cached. Use `cache: 'no-store'` for truly dynamic data and `revalidate` for time-based staleness.

5. **Keep Server Actions near their usage** Ã¢â‚¬â€ Define Server Actions in the same file or adjacent to the form that calls them. This keeps the mutation logic co-located with the UI.

6. **Use parallel routes for modals** Ã¢â‚¬â€ Avoid query-parameter-based modal state. Parallel routes (`@slot`) let the URL reflect modal content while preserving the underlying page.

7. **Optimize images with `next/image`** Ã¢â‚¬â€ Always use the Image component for external images. It handles lazy loading, responsive sizing, and format optimization automatically.

8. **Leverage metadata exports** Ã¢â‚¬â€ Export a `metadata` object or `generateMetadata` function from each page for SEO. Avoid duplicating metadata across layouts; let children merge via the Metadata API.

## Rendering Strategies Explained

### Server-Side Rendering (SSR)

SSR generates HTML on every request. Use this when the page content depends on request-time data (user session, headers, cookies). In the App Router, SSR is the default for dynamic components. Set `export const dynamic = 'force-dynamic'` or use `cookies()`/`headers()` in the component to opt into SSR. The trade-off is higher server load but always-fresh content.

### Static Site Generation (SSG)

SSG generates HTML at build time. Pages with no dynamic data are automatically static. For pages with known dynamic segments, export a `generateStaticParams()` function that returns all possible parameter combinations. The HTML is generated once and served from CDN Ã¢â‚¬â€ fastest possible TTFB. Use SSG for marketing pages, documentation, and blog posts.

### Incremental Static Regeneration (ISR)

ISR extends SSG by revalidating static pages after a time interval or on-demand. Set `revalidate: 3600` to revalidate every hour, or use `revalidateTag('posts')` to trigger on-demand revalidation from Server Actions or API routes. ISR combines SSG performance with SSR freshness Ã¢â‚¬â€ the stale page serves immediately while a background regeneration creates the updated version.

### Streaming SSR

Streaming sends HTML in chunks as Server Components resolve. Wrap slow data-fetching components in `<Suspense fallback={<Loading />}>` to stream the shell immediately. Each Suspense boundary resolves independently, creating a progressive loading experience. This is the default rendering strategy in the App Router when components have async dependencies.

## File Structure Reference

```
app/
  layout.js          # Root layout (wraps all pages)
  page.js            # Root page (/)
  loading.js         # Loading UI for root segment
  error.js           # Error boundary for root segment
  not-found.js       # 404 page
  dashboard/
    layout.js        # Dashboard layout (nested)
    page.js          # /dashboard
    loading.js       # Loading UI for /dashboard
    error.js         # Error boundary for /dashboard
    settings/
      page.js        # /dashboard/settings
  api/
    users/
      route.js       # GET/POST /api/users
      [id]/
        route.js     # GET/PUT/DELETE /api/users/:id
  @modal/
    (..)photo/
      [id]/
        page.js      # Intercepting route for /photo/:id
```

## Related Modules

- **server-components** Ã¢â‚¬â€ Deep dive into React Server Components architecture and streaming
- **tailwind-shadcn** Ã¢â‚¬â€ UI component patterns for Next.js applications
- **supabase-auth** Ã¢â‚¬â€ Authentication integration with Next.js middleware and server actions
- **edge-runtime** Ã¢â‚¬â€ Edge function deployment for Next.js middleware and API routes

---

## Advanced Configuration

### Custom Server Configuration

```python
from nextjs_fullstack import CustomServerConfig

config = CustomServerConfig(
    port=3000,
    hostname="0.0.0.0",
    compress=True,
    http2=True,
    keep_alive_timeout=65000,
    headers_timeout=60000,
    experimental=["turbopack", "reactCompiler"],
)
```

### Next.config.js Advanced

```python
from nextjs_fullstack import NextConfig

next_config = NextConfig(
    react_strict_mode=True,
    images={
        "remote_patterns": [{"protocol": "https", "hostname": "**.example.com"}],
        "formats": ["image/avif", "image/webp"],
    },
    rewrites={"beforeFiles": [("/api/legacy/:path*", "/api/v1/:path*")]},
    headers=[{"source": "/api/:path*", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"}]}],
)
```

## Architecture Patterns

### App Router Data Flow

```
Browser Request
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Edge         Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Middleware (auth, geo, redirects)
Ã¢â€â€š Middleware   Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Route        Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Layout + Page + Loading + Error
Ã¢â€â€š Resolution   Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Server       Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Data fetching, rendering
Ã¢â€â€š Components   Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Streaming    Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Progressive HTML delivery
Ã¢â€â€š SSR          Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Client       Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Hydration, interactivity
Ã¢â€â€š Hydration    Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

### Server Action Flow

```
Form Submit (Client)
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Server Action Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Validates input, executes mutation
Ã¢â€â€š (RPC)        Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Database     Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Direct query or ORM
Ã¢â€â€š Mutation     Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Revalidation Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Revalidate tags or paths
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š UI Update    Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Server sends updated HTML
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

## Integration Guide

### Supabase Integration

```python
from nextjs_fullstack import SupabaseIntegration

supabase = SupabaseIntegration(
    url="https://your-project.supabase.co",
    anon_key="your-anon-key",
)

# In Server Component
async def get_user_data():
    client = supabase.create_client()
    user = await client.auth.get_user()
    data = await client.from_("profiles").select("*").eq("id", user.id).execute()
    return data
```

### Vercel Deployment

```yaml
# vercel.json
{
  "framework": "nextjs",
  "buildCommand": "next build",
  "outputDirectory": ".next",
  "regions": ["iad1", "sfo1", "cdg1"]
}
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Turbopack dev server | 10x faster HMR |
| React Compiler | Automatic memoization |
| Image priority hints | Preload above-fold images |
| Dynamic imports | Code-split by route |
| ISR with tags | On-demand revalidation |

## Security Considerations

- **Server Actions**: Always validate input server-side
- **Middleware auth**: Never trust client-side auth alone
- **CSP headers**: Set Content-Security-Policy in middleware
- **Rate limiting**: Protect API routes and Server Actions
- **Environment variables**: Use NEXT_PUBLIC_ prefix carefully

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Hydration mismatch | Server/client render difference | Use useEffect for client-only state |
| Slow page load | Missing loading.js | Add loading.js per route segment |
| 404 on dynamic routes | Missing generateStaticParams | Export generateStaticParams |
| Middleware too slow | Heavy computation at edge | Move logic to API route |
| Image optimization error | Remote image not configured | Add hostname to images.remote_patterns |

## API Reference

### AppRouter

```python
class AppRouter:
    def page(self, path: str) -> decorator
    def layout(self, path: str) -> decorator
    def error(self, path: str) -> decorator
```

### ServerAction

```python
class ServerAction:
    async def execute(self, form_data: dict, user: AuthenticatedUser) -> dict
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class PageConfig:
    dynamic: str
    revalidate: int
    fetchCache: str
    runtime: str

@dataclass
class RouteParams:
    params: dict
    search_params: dict
```

## Deployment Guide

### Installation

```bash
npx create-next-app@latest my-app
cd my-app
npm install
npm run dev
```

### Production Deployment

```bash
npm run build
npm run start
# Or deploy to Vercel
vercel --prod
```

## Monitoring & Observability

```python
from nextjs_fullstack import MetricsCollector

collector = MetricsCollector()
collector.histogram("nextjs.render.duration_ms", duration, tags={"route": route})
collector.counter("nextjs.server_action.total", count, tags={"action": action})
collector.gauge("nextjs.isr.revalidation_count", count)
```

## Testing Strategy

```python
import pytest
from nextjs_fullstack import AppRouter

def test_page_render():
    router = AppRouter()
    # Test server component rendering
    result = router.render("/dashboard")
    assert "dashboard" in result
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 13.0 | App Router introduced | Migrate from Pages Router |
| 14.0 | Server Actions stable | Replace API routes for mutations |
| 15.0 | React Compiler | Remove manual memoization |

## Glossary

| Term | Definition |
|------|-----------|
| **ISR** | Incremental Static Regeneration |
| **RSC** | React Server Components |
| **SSR** | Server-Side Rendering |
| **SSG** | Static Site Generation |
| **Streaming** | Progressive HTML delivery via Suspense |

## Changelog

### Version 14.0.0 (2024-01-15)
- Server Actions stable
- Improved streaming SSR
- Parallel routes for modals
- Enhanced metadata API

## Contributing Guidelines

```bash
git clone https://github.com/example/nextjs-fullstack.git
npm install
npm run dev
npm test
```

## Advanced Patterns

### Streaming Suspense with Loading States

```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-8 bg-muted rounded w-1/3" />
      <div className="grid grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-32 bg-muted rounded-lg" />
        ))}
      </div>
    </div>
  )
}
```

### Server Action with Optimistic Updates

```tsx
'use client'

import { useOptimistic } from 'react'

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: string) => [
      ...state,
      { id: crypto.randomUUID(), text: newTodo, completed: false }
    ]
  )

  async function handleSubmit(formData: FormData) {
    const text = formData.get('text') as string
    addOptimisticTodo(text)
    await createTodo(formData)
  }

  return (
    <form action={handleSubmit}>
      <input name="text" />
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>
    </form>
  )
}
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Next.js File Convention Reference

| File | Purpose | Scope |
|------|---------|-------|
| `layout.js` | Shared UI for segment | Persists across navigations |
| `page.js` | Unique UI for segment | Renders at URL path |
| `loading.js` | Loading UI | Instant streaming fallback |
| `error.js` | Error boundary | Catches errors in segment |
| `not-found.js` | 404 UI | Handles not-found |
| `template.js` | Like layout, remounts | Animations per navigation |
| `default.js` | Parallel routes fallback | Used with @slots |
| `route.js` | API route handler | HTTP API endpoint |
| `middleware.js` | Request interception | Runs before routing |

### Rendering Strategy Decision Guide

| Strategy | When to Use | Pros | Cons |
|----------|------------|------|------|
| SSR | User-specific data | Fresh data every request | Higher server load |
| SSG | Static content | Fastest TTFB | Requires rebuild for updates |
| ISR | Semi-static content | SSG speed + freshness | Background regeneration |
| Streaming | Variable load times | Progressive loading | Complexity |
| Client | Interactive UI | Full interactivity | More JS shipped |

### Server Action Reference

```typescript
// Server Action with validation
'use server'

import { z } from 'zod'

const CreatePostSchema = z.object({
  title: z.string().min(3).max(100),
  body: z.string().min(10),
  tags: z.array(z.string()).optional(),
})

export async function createPost(formData: FormData) {
  const parsed = CreatePostSchema.safeParse({
    title: formData.get('title'),
    body: formData.get('body'),
    tags: formData.get('tags')?.split(','),
  })

  if (!parsed.success) {
    return { error: parsed.error.flatten() }
  }

  const post = await db.posts.create({ data: parsed.data })
  revalidateTag('posts')
  return { success: true, post }
}
```

### Middleware Reference

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Auth check
  const token = request.cookies.get('session')
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Geo-based routing
  const country = request.geo?.country || 'US'
  const response = NextResponse.next()
  response.headers.set('x-country', country)
  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

### Image Optimization Reference

| Component | Feature | Description |
|-----------|---------|-------------|
| `next/image` | Lazy loading | Load on viewport intersection |
| `next/image` | Responsive | srcset for different sizes |
| `next/image` | Format | Auto WebP/AVIF |
| `next/image` | Blur placeholder | BlurHash preview |
| `next/image` | Priority | Preload above-fold images |

### Metadata API Reference

```typescript
// Static metadata
export const metadata: Metadata = {
  title: 'My Page',
  description: 'Page description',
  openGraph: {
    title: 'My Page',
    description: 'Page description',
    images: ['/og-image.png'],
  },
}

// Dynamic metadata
export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await getProduct(params.id)
  return {
    title: product.name,
    description: product.description,
  }
}
```

### Caching Strategies

| Strategy | Configuration | Use Case |
|----------|--------------|----------|
| Default fetch | Cached automatically | Static-ish data |
| `cache: 'no-store'` | Never cached | Real-time data |
| `next: { revalidate: N }` | Time-based | Semi-dynamic |
| `tags: ['x']` | On-demand | Event-driven |
| `cache: 'force-cache'` | Always cached | Truly static |

### File Structure Reference

```
app/
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ layout.js              # Root layout
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ page.js                # Home page
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ loading.js             # Root loading
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ error.js               # Root error
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ not-found.js           # 404 page
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ globals.css            # Global styles
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ dashboard/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ layout.js          # Dashboard layout
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ page.js            # /dashboard
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ loading.js         # Dashboard loading
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ error.js           # Dashboard error
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ settings/
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ page.js        # /dashboard/settings
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ api/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ users/
Ã¢â€â€š       Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ route.js       # GET/POST /api/users
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ [id]/
Ã¢â€â€š           Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ route.js   # GET/PUT/DELETE /api/users/:id
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ @modal/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ (..)photo/
Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ [id]/
Ã¢â€â€š           Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ page.js    # Intercepting route
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ (marketing)/
    Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ layout.js          # Marketing layout group
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ about/
        Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ page.js        # /about
```

### Common Patterns Reference

| Pattern | Implementation | Use Case |
|---------|---------------|----------|
| Parallel routes | `@slot` folders | Modals, dashboards |
| Intercepting routes | `(..)` prefix | Photo viewers, drawers |
| Route groups | `(name)` folders | Layout variations |
| Dynamic routes | `[param]` folders | User profiles, products |
| Catch-all routes | `[...slug]` | CMS pages |
| Optional catch-all | `[[...slug]]` | Marketing + docs |
| Intercepting catch-all | `(..)[...slug]` | Modal + direct URL |


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
