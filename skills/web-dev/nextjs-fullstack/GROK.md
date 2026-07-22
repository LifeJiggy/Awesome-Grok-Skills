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
    │
    ▼
┌──────────────┐
│ Edge         │── Middleware (auth, geo, redirects)
│ Middleware   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Route        │── Layout + Page + Loading + Error
│ Resolution   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Server       │── Data fetching, rendering
│ Components   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Streaming    │── Progressive HTML delivery
│ SSR          │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Client       │── Hydration, interactivity
│ Hydration    │
└──────────────┘
```

### Server Action Flow

```
Form Submit (Client)
    │
    ▼
┌──────────────┐
│ Server Action │── Validates input, executes mutation
│ (RPC)        │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Database     │── Direct query or ORM
│ Mutation     │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Revalidation │── Revalidate tags or paths
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ UI Update    │── Server sends updated HTML
└──────────────┘
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
├── layout.js              # Root layout
├── page.js                # Home page
├── loading.js             # Root loading
├── error.js               # Root error
├── not-found.js           # 404 page
├── globals.css            # Global styles
├── dashboard/
│   ├── layout.js          # Dashboard layout
│   ├── page.js            # /dashboard
│   ├── loading.js         # Dashboard loading
│   ├── error.js           # Dashboard error
│   └── settings/
│       └── page.js        # /dashboard/settings
├── api/
│   └── users/
│       ├── route.js       # GET/POST /api/users
│       └── [id]/
│           └── route.js   # GET/PUT/DELETE /api/users/:id
├── @modal/
│   └── (..)photo/
│       └── [id]/
│           └── page.js    # Intercepting route
└── (marketing)/
    ├── layout.js          # Marketing layout group
    └── about/
        └── page.js        # /about
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
