---
name: "supabase-auth"
category: "web-dev"
version: "1.0.0"
tags: ["web-dev", "supabase", "auth", "authentication", "rls"]
---

# Supabase Authentication & Authorization

## Overview

Supabase Auth provides a complete authentication and authorization layer built on PostgreSQL's Row-Level Security (RLS), offering a unified identity system that works across client and server environments. Unlike standalone auth services that store sessions in external databases, Supabase Auth integrates directly with PostgreSQL, meaning your authorization policies are enforced at the database level — every query is automatically scoped to the authenticated user's permissions without application-level checks.

The authentication system supports multiple identity providers: email/password, magic links, social OAuth (Google, GitHub, Discord, Twitter, etc.), phone/SMS OTP, and passkeys (WebAuthn). Sessions are managed via JWTs containing the user's ID, role, and app metadata, which Supabase's PostgREST layer uses to set the `auth.uid()` and `auth.role()` PostgreSQL functions on every request. This means RLS policies can reference the authenticated user directly: `CREATE POLICY "Users can read own data" ON items USING (auth.uid() = user_id)`.

Row-Level Security is the cornerstone of Supabase's authorization model. When RLS is enabled on a table, every SELECT, INSERT, UPDATE, and DELETE operation is filtered through policy expressions. Policies can be additive (multiple policies are OR'd) or require specific conditions. Combined with Supabase's `service_role` key (which bypasses RLS) for server-side operations, this creates a clean security boundary: client-side queries are always user-scoped, while server-side operations can access the full dataset when needed.

Real-time subscriptions in Supabase are also governed by RLS — a user can only subscribe to changes on rows they can read. Edge Functions (Deno-based) can verify JWTs, call Supabase's admin API, and interact with the database using service-role or user-scoped clients. The entire stack — from the JavaScript client to the PostgREST API to the PostgreSQL database — enforces a single, consistent authorization model.

## Core Capabilities

- **Multi-provider authentication** — Email/password, magic links, OAuth (40+ providers), phone OTP, and passkeys
- **Row-Level Security policies** — Database-level authorization enforced on every query without application code
- **JWT-based session management** — Stateless tokens with automatic refresh, configurable expiry, and role-based claims
- **Multi-factor authentication (MFA)** — TOTP authenticator apps, SMS backup codes, and enforced MFA per user
- **Role-based access control (RBAC)** — Custom claims in JWT, PostgreSQL roles, and policy-based role switching
- **Real-time auth state** — Client-side auth state listener with `onAuthStateChange` for reactive UI updates
- **Edge Function auth middleware** — JWT verification and user context injection in Deno Edge Functions
- **Server-side session handling** — Cookie-based sessions with SSR frameworks (Next.js, Nuxt, etc.)

## Usage Examples

### Supabase Client Initialization and Basic Auth

```python
from supabase_auth import SupabaseClient, AuthConfig

# Initialize the client with project credentials
client = SupabaseClient(
    url="https://your-project.supabase.co",
    anon_key="your-anon-key",
    service_role_key="your-service-role-key",  # Server-side only
)

# Email/password sign-up
result = await client.auth.sign_up(
    email="user@example.com",
    password="secure-password-123",
    options={"data": {"full_name": "Jane Doe"}}
)
print(result.user.id, result.session.access_token)
```

### Row-Level Security Policy Setup

```python
from supabase_auth import RLSPolicy, PolicyAction, PolicyDefinition

# Define RLS policies for a "posts" table
read_policy = RLSPolicy(
    name="Users can read published posts",
    action=PolicyAction.SELECT,
    table="posts",
    definition=PolicyDefinition(
        using="status = 'published' OR auth.uid() = author_id",
    ),
)

insert_policy = RLSPolicy(
    name="Authenticated users can create posts",
    action=PolicyAction.INSERT,
    table="posts",
    definition=PolicyDefinition(
        check="auth.uid() = author_id",
    ),
)

# Apply policies to the database
await client.apply_rls_policies([read_policy, insert_policy])
```

### OAuth Provider Configuration

```python
from supabase_auth import OAuthProvider, OAuthConfig

# Configure GitHub OAuth
github_config = OAuthConfig(
    provider=OAuthProvider.GITHUB,
    client_id="your-github-client-id",
    client_secret="your-github-client-secret",
    redirect_url="http://localhost:3000/auth/callback",
    scopes=["user:email", "read:user"],
)

# Configure Google OAuth
google_config = OAuthConfig(
    provider=OAuthProvider.GOOGLE,
    client_id="your-google-client-id",
    client_secret="your-google-client-secret",
    redirect_url="http://localhost:3000/auth/callback",
    scopes=["openid", "email", "profile"],
)

# Register providers
await client.auth.admin.create_oauth_provider(github_config)
await client.auth.admin.create_oauth_provider(google_config)
```

### Multi-Factor Authentication

```python
from supabase_auth import MFAConfig, MFAFactor, TOTPEnrollment

# Enroll a user in TOTP MFA
enrollment = await client.auth.mfa.enroll(
    factor_type="totp",
    friendly_name="Authenticator App",
)
# enrollment contains a QR code URL and secret

# Verify a TOTP challenge
verified = await client.auth.mfa.verify(
    factor_id=enrollment.id,
    code="123456",
)

# Check if MFA is required for sensitive operations
async def require_mfa(user_id: str) -> bool:
    factors = await client.auth.mfa.list_factors(user_id)
    verified_factors = [f for f in factors if f.status == "verified"]
    return len(verified_factors) > 0
```

### JWT Token Verification in Edge Functions

```python
from supabase_auth import JWTVerifier, EdgeFunctionAuth

# Verify a JWT from an incoming request
verifier = JWTVerifier(
    secret="your-jwt-secret",
    audience="authenticated",
    issuer="https://your-project.supabase.co/auth/v1",
)

async def edge_function_handler(request: dict) -> dict:
    token = request["headers"].get("Authorization", "").replace("Bearer ", "")

    try:
        payload = await verifier.verify(token)
        user_id = payload["sub"]
        role = payload.get("role", "authenticated")
        return {"status": 200, "user_id": user_id, "role": role}
    except JWTVerificationError as e:
        return {"status": 401, "error": str(e)}
```

### Role-Based Access Control with Custom Claims

```python
from supabase_auth import RoleManager, CustomClaims

# Set custom claims for a user (stored in app_metadata)
await client.auth.admin.update_user(
    user_id="user-uuid-123",
    app_metadata={"role": "admin", "permissions": ["read", "write", "delete"]},
)

# Verify permissions in a policy or middleware
role_manager = RoleManager(client)
is_admin = await role_manager.has_role("user-uuid-123", "admin")
has_permission = await role_manager.has_permission("user-uuid-123", "write")
```

### Magic Link Authentication Flow

```python
from supabase_auth import MagicLinkConfig

# Send a magic link to the user
magic_config = MagicLinkConfig(
    email="user@example.com",
    redirect_to="http://localhost:3000/dashboard",
    should_create_user=True,  # Auto-create if user doesn't exist
)

result = await client.auth.sign_in_with_otp(
    email=magic_config.email,
    options={
        "emailRedirectTo": magic_config.redirect_to,
        "data": {"full_name": "Jane Doe"},
    },
)

# The user receives an email with a link that contains a token
# When they click it, they're redirected back with a session
```

### Session Management with Cookie Refresh

```python
from supabase_auth import SessionManager, CookieConfig

# Server-side session management (Next.js middleware pattern)
session_manager = SessionManager(
    client=client,
    cookie_config=CookieConfig(
        name="sb-auth-token",
        http_only=True,
        secure=True,
        same_site="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    ),
)

async def get_server_session(request_cookies: dict) -> dict | None:
    token = request_cookies.get("sb-auth-token")
    if not token:
        return None

    try:
        session = await session_manager.get_session(token)
        if session.is_expired():
            session = await session_manager.refresh_session(session.refresh_token)
        return session
    except SessionError:
        return None
```

## Best Practices

1. **Always use RLS** — Never rely solely on application-level checks. Enable RLS on every table and write policies for all operations. The `service_role` key should only be used in trusted server environments.

2. **Never expose service_role key client-side** — The service_role key bypasses RLS. Only use it in server-side code, Edge Functions with verified JWTs, or database migrations.

3. **Use short-lived JWTs with refresh tokens** — Set access token expiry to 1 hour (default) and refresh token expiry to 7 days. Use cookie-based sessions for SSR frameworks to avoid token exposure in client JavaScript.

4. **Implement MFA for sensitive accounts** — Enforce TOTP-based MFA for admin users and offer it for all users. Use `amr` (Authentication Methods References) claims to check if MFA was used in the current session.

5. **Scope policies with `auth.uid()`** — Reference the authenticated user in RLS policies using `auth.uid() = user_id` rather than passing user IDs from the client. This prevents horizontal privilege escalation.

6. **Use server-side auth for SSR frameworks** — In Next.js, always verify the session server-side in `getServerSideProps` or middleware. Don't rely on client-side `getUser()` for protected pages.

7. **Audit auth events** — Log sign-in attempts, sign-ups, MFA challenges, and password resets. Supabase provides `auth.admin.list_users()` and `auth.admin.get_user()` for user management.

8. **Rotate secrets regularly** — Rotate JWT signing keys, API keys, and OAuth client secrets on a schedule. Supabase supports multiple active JWT secrets during rotation.

## Related Modules

- **nextjs-fullstack** — Integrating Supabase Auth with Next.js middleware and server actions
- **edge-runtime** — Deploying Supabase Edge Functions with auth middleware
- **server-components** — Using Supabase auth state in React Server Components
- **tailwind-shadcn** — UI patterns for auth forms and login pages
