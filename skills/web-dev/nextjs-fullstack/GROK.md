---
name: "nextjs-fullstack"
category: "web-dev"
version: "1.0.0"
tags: ["web-dev", "nextjs", "fullstack", "app-router", "react"]
---

# Next.js Full-Stack Development

## Overview

Next.js App Router represents the evolution of React full-stack development, introducing a file-system based routing convention that unifies server and client rendering strategies under a single mental model. The App Router (introduced in Next.js 13, stable in 14+) replaces the legacy Pages Router with a layout-first architecture where `layout.js`, `page.js`, `loading.js`, and `error.js` compose a nested routing tree. Each segment in the file system maps to a URL path, and the component hierarchy is derived from the folder nesting — eliminating manual route configuration entirely.

Server Components are the default rendering strategy in the App Router. Every component in `app/` runs on the server unless explicitly marked with `'use client'`. This means data fetching happens at the component level without `useEffect`, `getServerSideProps`, or client-side state management. The server can directly query databases, call internal APIs, read the filesystem, and stream HTML to the browser while the client hydrates progressively. Client Components handle interactivity — event handlers, browser APIs, state, and effects — and are serialized across the server-client boundary as React Server Component payloads.

The full-stack capability extends to API routes colocated with pages, middleware that runs at the edge before routing, image optimization via the `next/image` component, font optimization with `next/font`, and metadata generation through the Metadata API. Server Actions (available since Next.js 14) enable form submissions and mutations directly from Server Components without creating separate API endpoints, completing the full-stack loop where the same codebase handles rendering, data, and mutations.

## Core Capabilities

- **File-system routing with layouts** — Nested folders define URL segments; shared layouts persist across navigations without remounting
- **Server/Client Component boundaries** — Default server rendering with explicit `'use client'` for interactive islands
- **Multi-strategy data fetching** — SSR (request-time), SSG (build-time), ISR (revalidated), and Streaming (chunked HTML)
- **Server Actions** — Form mutations directly from Server Components without API route boilerplate
- **Middleware** — Edge-compatible request/response interception for auth, redirects, rewrites, and geo-routing
- **Image and font optimization** — Automatic WebP/AVIF conversion, lazy loading, layout shift prevention, and font self-hosting
- **Metadata API** — SEO, Open Graph, JSON-LD, and sitemap generation through structured exports
- **Parallel and intercepting routes** — Modal overlays, shared layouts across route groups, and route interception for UX patterns

## Usage Examples

### Basic App Router Page with Server Component Data Fetching

```python
# nextjs_fullstack.py — conceptual example of App Router page structure
from nextjs_fullstack import AppRouter, PageConfig, ServerComponent

router = AppRouter()

# Define a page that fetches data server-side at request time
@router.page("/dashboard")
class DashboardPage(ServerComponent):
    """Server Component — runs on the server, no client JS shipped."""

    config = PageConfig(
        dynamic="force-dynamic",  # SSR on every request
        revalidate=0,
    )

    async def render(self, params: dict) -> str:
        # Direct database query — no API layer needed
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
    """Server Action — called from a form in a Server Component."""

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
    """Intercepting route — renders as modal over parent layout."""

    async def render(self, params: dict) -> str:
        photo = await self.db.photos.find_unique(where={"id": params["id"]})
        return self.html("modal-photo.html", {"photo": photo})

    def fallback(self) -> str:
        return ""  # Empty when not intercepted
```

## Best Practices

1. **Default to Server Components** — Only add `'use client'` when the component needs event handlers, browser APIs, or React hooks like `useState`/`useEffect`. Every client component adds JavaScript to the bundle.

2. **Colocate data fetching with components** — Fetch data in the component that renders it, not in a parent. This enables independent loading states via `loading.js` and streaming.

3. **Use `loading.js` for streaming** — Create a `loading.js` file in any route segment to show instant loading UI while the server component streams data.

4. **Cache aggressively, revalidate intentionally** — Default fetch requests in Server Components are cached. Use `cache: 'no-store'` for truly dynamic data and `revalidate` for time-based staleness.

5. **Keep Server Actions near their usage** — Define Server Actions in the same file or adjacent to the form that calls them. This keeps the mutation logic co-located with the UI.

6. **Use parallel routes for modals** — Avoid query-parameter-based modal state. Parallel routes (`@slot`) let the URL reflect modal content while preserving the underlying page.

7. **Optimize images with `next/image`** — Always use the Image component for external images. It handles lazy loading, responsive sizing, and format optimization automatically.

8. **Leverage metadata exports** — Export a `metadata` object or `generateMetadata` function from each page for SEO. Avoid duplicating metadata across layouts; let children merge via the Metadata API.

## Rendering Strategies Explained

### Server-Side Rendering (SSR)

SSR generates HTML on every request. Use this when the page content depends on request-time data (user session, headers, cookies). In the App Router, SSR is the default for dynamic components. Set `export const dynamic = 'force-dynamic'` or use `cookies()`/`headers()` in the component to opt into SSR. The trade-off is higher server load but always-fresh content.

### Static Site Generation (SSG)

SSG generates HTML at build time. Pages with no dynamic data are automatically static. For pages with known dynamic segments, export a `generateStaticParams()` function that returns all possible parameter combinations. The HTML is generated once and served from CDN — fastest possible TTFB. Use SSG for marketing pages, documentation, and blog posts.

### Incremental Static Regeneration (ISR)

ISR extends SSG by revalidating static pages after a time interval or on-demand. Set `revalidate: 3600` to revalidate every hour, or use `revalidateTag('posts')` to trigger on-demand revalidation from Server Actions or API routes. ISR combines SSG performance with SSR freshness — the stale page serves immediately while a background regeneration creates the updated version.

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

- **server-components** — Deep dive into React Server Components architecture and streaming
- **tailwind-shadcn** — UI component patterns for Next.js applications
- **supabase-auth** — Authentication integration with Next.js middleware and server actions
- **edge-runtime** — Edge function deployment for Next.js middleware and API routes
