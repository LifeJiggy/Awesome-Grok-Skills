---
name: "server-components"
category: "web-dev"
version: "1.0.0"
tags: ["web-dev", "react", "server-components", "streaming", "ssr"]
---

# React Server Components Architecture

## Overview

React Server Components (RSC) represent a fundamental shift in how React applications render — moving the default execution environment from the browser to the server. Unlike traditional client-side React where the entire component tree ships as JavaScript and hydrates on the client, Server Components execute exclusively on the server during the request lifecycle. They can directly access databases, filesystems, environment variables, and internal services without exposing them to the client bundle. The server renders them into a serialized format (the RSC wire format), which the client receives and integrates into its component tree without additional JavaScript.

The key architectural distinction is between Server Components and Client Components. Server Components (the default) run only on the server — they cannot use `useState`, `useEffect`, event handlers, or browser APIs. Client Components (marked with `'use client'`) execute on both server (for initial SSR) and client (for hydration and interactivity). The boundary between them is explicit and affects the bundle: anything imported by a Client Component and used in its render must be serializable. Server Components can pass serializable props to Client Components and render them as children, creating a hybrid model where data-heavy, read-only parts of the UI are zero-JS while interactive islands remain fully hydrated.

Streaming is the rendering strategy that makes Server Components feel fast. Instead of waiting for the entire page to be ready, the server sends an initial shell (the parts that don't depend on slow data) immediately, then streams additional HTML as Suspense boundaries resolve. Each `<Suspense>` wrapper defines a fallback that's shown while the enclosed content loads. When the async data arrives, the server sends a delta update that replaces the fallback with real content. This creates the perception of instant page loads with progressive enhancement.

The React Server Component protocol defines the wire format between server and client: a stream of typed records representing component references, HTML strings, client module references, and Suspense promises. This protocol is framework-agnostic — Next.js, Remix, and other frameworks implement it differently, but the underlying model is the same. Components on the server produce RSC payloads; the client reconciles them into the React tree, preserving state across navigations and streaming updates.

## Core Capabilities

- **Server-only component execution** — Components run on the server with direct access to databases, APIs, and filesystem without client-side exposure
- **Streaming SSR with Suspense** — Progressive HTML delivery with streaming fallbacks for async data dependencies
- **Zero-bundle-size server components** — Server Components ship no JavaScript to the client, reducing bundle size dramatically
- **Client component interop** — Explicit boundary between server and client with serializable prop passing
- **Progressive rendering** — Initial shell streams immediately, then Suspense boundaries fill in as data resolves
- **Component-level caching** — Per-component cache with `React.cache()` for deduplicating async work within a request
- **Partial hydration** — Only Client Components hydrate on the client; Server Components remain server-rendered
- **`use server` directive** — Server-side functions callable from Client Components without creating API routes

## Usage Examples

### Basic Server Component with Data Fetching

```python
from server_components import ServerComponent, ComponentConfig

class UserDashboard(ServerComponent):
    """Server Component — runs only on the server, ships zero JS."""

    config = ComponentConfig(type="server")

    async def render(self, props: dict) -> str:
        # Direct database access — no API layer needed
        user = await self.db.users.find_unique(where={"id": props["userId"]})
        posts = await self.db.posts.find_many(
            where={"author_id": user.id},
            order={"created_at": "desc"},
            limit=10,
        )

        return self.html(
            "<div>",
            f"<h1>Welcome, {user.name}</h1>",
            "<ul>",
            *[f"<li>{post.title}</li>" for post in posts],
            "</ul>",
            "</div>",
        )
```

### Client Component with Interactivity

```python
from server_components import ClientComponent, ComponentConfig, useState, useEffect

class LikeButton(ClientComponent):
    """Client Component — hydrates on the client, has interactivity."""

    config = ComponentConfig(type="client", ssr=True)

    def render(self, props: dict) -> str:
        post_id = props["post_id"]
        initial_count = props.get("initial_count", 0)

        # useState and useEffect are available in Client Components
        state = self.use_state("count", initial_count)
        state = self.use_state("liked", False)

        def handle_click():
            new_count = state["count"] + (1 if not state["liked"] else -1)
            self.set_state({"count": new_count, "liked": not state["liked"]})

        return self.html(
            f'<button onclick="{handle_click}" class="like-btn">',
            f'{"♥" if state["liked"] else "♡"} {state["count"]}',
            '</button>',
        )
```

### Streaming with Suspense Boundaries

```python
from server_components import StreamingRenderer, SuspenseBoundary, AsyncComponent

class StreamingPage(ServerComponent):
    """Page with streaming Suspense boundaries for progressive loading."""

    config = ComponentConfig(type="server", streaming=True)

    async def render(self, props: dict) -> str:
        renderer = StreamingRenderer()

        # This renders immediately (no async dependency)
        shell = """
        <html>
        <body>
            <h1>Dashboard</h1>
            <nav>Navigation renders instantly</nav>
        """

        # This streams in when data resolves
        renderer.add_boundary(
            SuspenseBoundary(
                fallback="<p>Loading metrics...</p>",
                component=MetricsPanel,
                props={"org_id": props["org_id"]},
            )
        )

        # This streams independently
        renderer.add_boundary(
            SuspenseBoundary(
                fallback="<p>Loading activity feed...</p>",
                component=ActivityFeed,
                props={"user_id": props["user_id"]},
            )
        )

        shell += renderer.render()
        shell += "</body></html>"
        return shell


class MetricsPanel(ServerComponent):
    async def render(self, props: dict) -> str:
        # Slow database query — this streams independently
        metrics = await self.db.query("SELECT ...")
        return f'<div class="metrics">{metrics.to_html()}</div>'


class ActivityFeed(ServerComponent):
    async def render(self, props: dict) -> str:
        activities = await self.db.activities.find_many(limit=20)
        return f'<div class="feed">{activities.to_html()}</div>'
```

### Server Action for Mutations

```python
from server_components import ServerAction, useTransition

class DeletePostButton(ClientComponent):
    """Client Component that calls a Server Action."""

    def render(self, props: dict) -> str:
        post_id = props["post_id"]
        transition = self.use_transition()

        async def handle_delete():
            await delete_post_action(post_id)
            # Router refresh to update the UI
            self.router.refresh()

        return self.html(
            f'<button onclick="{handle_delete}" disabled={transition["pending"]}>',
            "Delete" if not transition["pending"] else "Deleting...",
            '</button>',
        )


# Server-side action
@ServerAction
async def delete_post_action(post_id: str) -> None:
    """Runs on the server — called from Client Component."""
    await db.posts.delete(where={"id": post_id})
    revalidate_tag("posts")
```

### Component-Level Caching

```python
from server_components import cache, ServerComponent

class CachedUserProfile(ServerComponent):
    """Demonstrates React.cache() for request-level deduplication."""

    async def render(self, props: dict) -> str:
        # This call is cached within the current request
        user = await self.get_user_cached(props["user_id"])
        return f"<div>{user.name}</div>"

    @cache
    async def get_user_cached(self, user_id: str):
        """Deduplicated — only one DB call even if multiple components request the same user."""
        return await self.db.users.find_unique(where={"id": user_id})
```

### Parallel Routes with Server Components

```python
from server_components import ParallelRoute

class DashboardLayout(ServerComponent):
    """Layout with parallel route slots rendered as Server Components."""

    async def render(self, props: dict) -> str:
        # Each slot is a separate Server Component tree
        return self.html(
            '<div class="layout">',
            '<aside>{sidebar}</aside>',
            '<main>{children}</main>',
            '<aside>{notifications}</aside>',
            '</div>',
        )


class SidebarSlot(ServerComponent):
    async def render(self, props: dict) -> str:
        nav_items = await self.db.navigation.find_many()
        return '<nav>' + ''.join(f'<a href="{i.url}">{i.label}</a>' for i in nav_items) + '</nav>'
```

## Best Practices

1. **Default to Server Components** — Only add `'use client'` when you need event handlers, browser APIs, or hooks like `useState`/`useEffect`. Every Client Component adds JavaScript to the bundle.

2. **Push Client Components to the leaves** — Keep your component tree as server-rendered as possible. Only the interactive leaf nodes (buttons, forms, inputs) should be Client Components.

3. **Pass serializable data across the boundary** — Server Components can only pass serializable props to Client Components: strings, numbers, plain objects, arrays. Functions, class instances, and Promises cannot cross the boundary.

4. **Use Suspense for streaming** — Wrap async Server Components in `<Suspense>` with meaningful fallbacks. This enables streaming and prevents slow data from blocking the entire page.

5. **Deduplicate with `React.cache()`** — When multiple components need the same data, use `React.cache()` to ensure only one fetch happens per request. This prevents N+1 query patterns.

6. **Leverage `use server` for mutations** — Use Server Actions instead of API routes for simple mutations. They colocate the mutation logic with the component and handle form submissions without client-side fetch calls.

7. **Avoid client-side state for server data** — Don't fetch data in `useEffect` and store it in `useState` when the same data is available as a Server Component prop. Server Components can always have fresher data.

8. **Test the RSC payload** — Verify your Server Components produce valid RSC wire format. Frameworks provide `renderToString` or `renderToReadableStream` for this. Check that client boundaries are correctly placed.

## Related Modules

- **nextjs-fullstack** — Next.js App Router integration with Server Components
- **edge-runtime** — Deploying Server Components at the edge
- **tailwind-shadcn** — UI components that work across server and client boundaries
- **supabase-auth** — Auth state management across server and client components

---

## Advanced Configuration

### RSC Payload Configuration

```python
from server_components import RSCConfig

config = RSCConfig(
    stream_enabled=True,
    suspense_boundaries="auto",
    cache_strategy="request",
    max_stream_depth=10,
    enable_partial_hydration=True,
)
```

### Component Cache Strategy

```python
from server_components import CacheStrategy

cache = CacheStrategy(
    dedup_enabled=True,
    cache_scope="request",  # request | session | global
    ttl_seconds=300,
    stale_while_revalidate=True,
)
```

## Architecture Patterns

### Server/Client Boundary

```
Server Components (zero JS)
    │
    │ Props (serializable only)
    ▼
Client Components (hydrated)
    │
    │ Event handlers, state
    ▼
Browser
```

### Streaming with Suspense

```
Initial Shell (immediate)
    │
    ├── Suspense Boundary 1 → Fallback → Resolved Content
    │
    ├── Suspense Boundary 2 → Fallback → Resolved Content
    │
    └── Suspense Boundary 3 → Fallback → Resolved Content
```

## Integration Guide

### Database Integration

```python
from server_components import ServerComponent, db

class UserList(ServerComponent):
    async def render(self, props):
        users = await db.user.find_many(order={"name": "asc"})
        return self.html("<ul>", *[f"<li>{u.name}</li>" for u in users], "</ul>")
```

### Client Component Interop

```python
from server_components import ClientComponent, useState

class Counter(ClientComponent):
    def render(self, props):
        count = self.use_state("count", props.get("initial", 0))
        return self.html(
            f'<button onClick=lambda: self.set_state("count", {count} + 1)>',
            f'Count: {count}',
            '</button>',
        )
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| React.cache() dedup | Single DB call per request |
| Streaming Suspense | Immediate shell, progressive content |
| Partial hydration | Only interactive parts ship JS |
| Component-level caching | Skip re-render for unchanged data |

## Security Considerations

- **No secrets in Server Components**: They run on server only
- **Serializable boundary**: Functions don't cross server/client
- **Server Action validation**: Always validate form data server-side
- **CSRF protection**: Server Actions include CSRF tokens

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Hydration error | Server/client render mismatch | Use useEffect for client state |
| Function passed to client | Non-serializable prop | Use Server Action instead |
| Streaming not working | Missing Suspense boundary | Wrap async component in Suspense |
| Cache not deduplicating | Different cache keys | Use React.cache() for same fetch |

## API Reference

### ServerComponent

```python
class ServerComponent:
    async def render(self, props: dict) -> str
    def html(self, *parts) -> str
```

### ClientComponent

```python
class ClientComponent:
    def render(self, props: dict) -> str
    def use_state(self, key: str, initial: any) -> any
    def use_effect(self, fn: callable, deps: list) -> None
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class ComponentConfig:
    type: str  # "server" | "client"
    ssr: bool = True
    streaming: bool = False

@dataclass
class RSCPayload:
    type: str
    id: str
    children: list
```

## Deployment Guide

### Installation

```bash
npx create-next-app@latest my-app --app
# Server Components are default in App Router
```

## Monitoring & Observability

```python
from server_components import MetricsCollector

collector = MetricsCollector()
collector.histogram("rsc.render.duration_ms", duration, tags={"component": name})
collector.counter("rsc.cache.hit", count)
collector.counter("rsc.cache.miss", count)
```

## Testing Strategy

```python
import pytest
from server_components import ServerComponent

def test_server_component():
    class TestComponent(ServerComponent):
        async def render(self, props):
            return self.html("<div>Hello</div>")
    component = TestComponent()
    result = asyncio.run(component.render({}))
    assert "Hello" in result
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 18.0 | Server Components introduced | Add 'use client' to interactive components |
| 19.0 | Actions stable | Use Server Actions for mutations |

## Glossary

| Term | Definition |
|------|-----------|
| **RSC** | React Server Components |
| **RSC Payload** | Serialized wire format between server and client |
| **Hydration** | Client-side event attachment to server HTML |
| **Suspense** | React boundary for async loading states |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with Server/Client Component model
- Streaming SSR with Suspense
- React.cache() for deduplication
- Server Actions

## Contributing Guidelines

```bash
git clone https://github.com/example/server-components.git
npm install
npm test
```

## Advanced Patterns

### Parallel Data Fetching with Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { RevenueChart } from './revenue-chart'
import { RecentSales } from './recent-sales'
import { StatsCards } from './stats-cards'

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      {/* Parallel data fetching — each component fetches independently */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Suspense fallback={<StatsCardSkeleton />}>
          <StatsCards />
        </Suspense>
      </div>

      <div className="grid gap-4 md:grid-cols-7">
        <div className="col-span-4">
          <Suspense fallback={<ChartSkeleton />}>
            <RevenueChart />
          </Suspense>
        </div>
        <div className="col-span-3">
          <Suspense fallback={<SalesSkeleton />}>
            <RecentSales />
          </Suspense>
        </div>
      </div>
    </div>
  )
}
```

### Server Component with Error Boundary

```tsx
// app/dashboard/error.tsx
'use client'

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="rounded-lg border border-destructive/50 p-6">
      <h2 className="text-lg font-semibold text-destructive">
        Something went wrong
      </h2>
      <p className="mt-2 text-sm text-muted-foreground">
        {error.message}
      </p>
      <button
        onClick={() => reset()}
        className="mt-4 rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground"
      >
        Try again
      </button>
    </div>
  )
}
```

### Server Action with Revalidation

```tsx
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({ data: { title, content } })

  // Revalidate the blog listing page
  revalidatePath('/blog')
  // Redirect after mutation
  redirect('/blog')
}

export async function deletePost(id: string) {
  await db.post.delete({ where: { id } })

  // Revalidate specific paths
  revalidatePath('/blog')
  revalidatePath(`/blog/${id}`)
}
```

### Streaming with Generators

```tsx
// app/api/progress/route.ts
export async function GET() {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i <= 100; i += 10) {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify({ progress: i })}\n\n`)
        )
        await new Promise(r => setTimeout(r, 500))
      }
      controller.close()
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    }
  })
}
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Server vs Client Component Decision Guide

| Use Server Component | Use Client Component |
|---------------------|---------------------|
| Data fetching | useState, useEffect |
| Database queries | Event handlers |
| File system access | Browser APIs |
| Sensitive data | Interactive UI |
| Heavy computation | Third-party client libs |
| SEO content | Drag and drop |
| Layouts | Media playback |

### Serializable Props Reference

| Serializable | Not Serializable |
|-------------|-----------------|
| Strings, numbers | Functions |
| Plain objects | Class instances |
| Arrays | Promises |
| Dates | Symbols |
| null, undefined | Maps, Sets |
| Blobs | DOM nodes |

### React.cache() Reference

```typescript
// Deduplicate within a request
const getUser = React.cache(async (id: string) => {
  return await db.users.findUnique({ where: { id } })
})

// Multiple components call getUser(123)
// Only one database query is made
async function Profile({ userId }) {
  const user = await getUser(userId)
  return <h1>{user.name}</h1>
}

async function Stats({ userId }) {
  const user = await getUser(userId)
  return <p>{user.email}</p>
}
```

### use() Hook Reference

```typescript
// Read promises and context in render
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise)
  return comments.map(c => <p key={c.id}>{c.text}</p>)
}

// Read context
function Theme() {
  const theme = use(ThemeContext)
  return <div className={theme}>...</div>
}
```

### Streaming Patterns

```typescript
// Suspense boundary with fallback
<Suspense fallback={<Skeleton />}>
  <SlowComponent />
</Suspense>

// Multiple independent Suspense boundaries
<Suspense fallback={<NavSkeleton />}>
  <Navigation />
</Suspense>
<Suspense fallback={<ContentSkeleton />}>
  <Content />
</Suspense>
<Suspense fallback={<SidebarSkeleton />}>
  <Sidebar />
</Suspense>
```

### Server Action Patterns

```typescript
// With revalidation
async function createPost(formData: FormData) {
  'use server'
  await db.posts.create({ data: { title: formData.get('title') } })
  revalidatePath('/posts')
}

// With redirect
async function login(formData: FormData) {
  'use server'
  const user = await authenticate(formData)
  if (user) redirect('/dashboard')
}

// With error handling
async function riskyAction() {
  'use server'
  try {
    await doSomethingRisky()
    return { success: true }
  } catch (e) {
    return { error: e.message }
  }
}
```
