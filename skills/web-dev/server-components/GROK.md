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
