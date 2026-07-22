---
name: "supabase-auth"
category: "web-dev"
version: "1.0.0"
tags: ["web-dev", "supabase", "auth", "authentication", "rls"]
---

# Supabase Authentication & Authorization

## Overview

Supabase Auth provides a complete authentication and authorization layer built on PostgreSQL's Row-Level Security (RLS), offering a unified identity system that works across client and server environments. Unlike standalone auth services that store sessions in external databases, Supabase Auth integrates directly with PostgreSQL, meaning your authorization policies are enforced at the database level Ã¢â‚¬â€ every query is automatically scoped to the authenticated user's permissions without application-level checks.

The authentication system supports multiple identity providers: email/password, magic links, social OAuth (Google, GitHub, Discord, Twitter, etc.), phone/SMS OTP, and passkeys (WebAuthn). Sessions are managed via JWTs containing the user's ID, role, and app metadata, which Supabase's PostgREST layer uses to set the `auth.uid()` and `auth.role()` PostgreSQL functions on every request. This means RLS policies can reference the authenticated user directly: `CREATE POLICY "Users can read own data" ON items USING (auth.uid() = user_id)`.

Row-Level Security is the cornerstone of Supabase's authorization model. When RLS is enabled on a table, every SELECT, INSERT, UPDATE, and DELETE operation is filtered through policy expressions. Policies can be additive (multiple policies are OR'd) or require specific conditions. Combined with Supabase's `service_role` key (which bypasses RLS) for server-side operations, this creates a clean security boundary: client-side queries are always user-scoped, while server-side operations can access the full dataset when needed.

Real-time subscriptions in Supabase are also governed by RLS Ã¢â‚¬â€ a user can only subscribe to changes on rows they can read. Edge Functions (Deno-based) can verify JWTs, call Supabase's admin API, and interact with the database using service-role or user-scoped clients. The entire stack Ã¢â‚¬â€ from the JavaScript client to the PostgREST API to the PostgreSQL database Ã¢â‚¬â€ enforces a single, consistent authorization model.

## Core Capabilities

- **Multi-provider authentication** Ã¢â‚¬â€ Email/password, magic links, OAuth (40+ providers), phone OTP, and passkeys
- **Row-Level Security policies** Ã¢â‚¬â€ Database-level authorization enforced on every query without application code
- **JWT-based session management** Ã¢â‚¬â€ Stateless tokens with automatic refresh, configurable expiry, and role-based claims
- **Multi-factor authentication (MFA)** Ã¢â‚¬â€ TOTP authenticator apps, SMS backup codes, and enforced MFA per user
- **Role-based access control (RBAC)** Ã¢â‚¬â€ Custom claims in JWT, PostgreSQL roles, and policy-based role switching
- **Real-time auth state** Ã¢â‚¬â€ Client-side auth state listener with `onAuthStateChange` for reactive UI updates
- **Edge Function auth middleware** Ã¢â‚¬â€ JWT verification and user context injection in Deno Edge Functions
- **Server-side session handling** Ã¢â‚¬â€ Cookie-based sessions with SSR frameworks (Next.js, Nuxt, etc.)

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

1. **Always use RLS** Ã¢â‚¬â€ Never rely solely on application-level checks. Enable RLS on every table and write policies for all operations. The `service_role` key should only be used in trusted server environments.

2. **Never expose service_role key client-side** Ã¢â‚¬â€ The service_role key bypasses RLS. Only use it in server-side code, Edge Functions with verified JWTs, or database migrations.

3. **Use short-lived JWTs with refresh tokens** Ã¢â‚¬â€ Set access token expiry to 1 hour (default) and refresh token expiry to 7 days. Use cookie-based sessions for SSR frameworks to avoid token exposure in client JavaScript.

4. **Implement MFA for sensitive accounts** Ã¢â‚¬â€ Enforce TOTP-based MFA for admin users and offer it for all users. Use `amr` (Authentication Methods References) claims to check if MFA was used in the current session.

5. **Scope policies with `auth.uid()`** Ã¢â‚¬â€ Reference the authenticated user in RLS policies using `auth.uid() = user_id` rather than passing user IDs from the client. This prevents horizontal privilege escalation.

6. **Use server-side auth for SSR frameworks** Ã¢â‚¬â€ In Next.js, always verify the session server-side in `getServerSideProps` or middleware. Don't rely on client-side `getUser()` for protected pages.

7. **Audit auth events** Ã¢â‚¬â€ Log sign-in attempts, sign-ups, MFA challenges, and password resets. Supabase provides `auth.admin.list_users()` and `auth.admin.get_user()` for user management.

8. **Rotate secrets regularly** Ã¢â‚¬â€ Rotate JWT signing keys, API keys, and OAuth client secrets on a schedule. Supabase supports multiple active JWT secrets during rotation.

## Related Modules

- **nextjs-fullstack** Ã¢â‚¬â€ Integrating Supabase Auth with Next.js middleware and server actions
- **edge-runtime** Ã¢â‚¬â€ Deploying Supabase Edge Functions with auth middleware
- **server-components** Ã¢â‚¬â€ Using Supabase auth state in React Server Components
- **tailwind-shadcn** Ã¢â‚¬â€ UI patterns for auth forms and login pages

---

## Advanced Configuration

### Custom JWT Claims

```python
from supabase_auth import JWTClaimsConfig

claims_config = JWTClaimsConfig(
    custom_claims={
        "role": "app_metadata.role",
        "permissions": "app_metadata.permissions",
        "org_id": "app_metadata.org_id",
    },
    token_lifetime_seconds=3600,
    refresh_token_lifetime_seconds=604800,
)
```

### RLS Policy Templates

```python
from supabase_auth import RLSTemplate

templates = RLSTemplate(
    owner_policy="auth.uid() = user_id",
    org_policy="auth.uid() IN (SELECT user_id FROM org_members WHERE org_id = org_id)",
    admin_policy="auth.jwt()->>'role' = 'admin'",
    public_read_policy="status = 'published'",
)
```

## Architecture Patterns

### Auth Flow Architecture

```
Client Request
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Middleware    Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ JWT verification, session refresh
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Server       Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Session validation, user context
Ã¢â€â€š Component    Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š PostgREST    Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Sets auth.uid() from JWT
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š RLS Policy   Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Filters rows based on auth.uid()
Ã¢â€â€š Evaluation   Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Database     Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Returns only authorized rows
Ã¢â€â€š Query        Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

## Integration Guide

### Next.js Middleware Integration

```python
from supabase_auth import SupabaseMiddleware

middleware = SupabaseMiddleware(
    supabase_url="https://your-project.supabase.co",
    anon_key="your-anon-key",
    protected_paths=["/dashboard", "/settings"],
    public_paths=["/", "/login"],
)
```

### Edge Function Integration

```python
from supabase_auth import EdgeFunctionAuth

auth = EdgeFunctionAuth(jwt_secret="your-jwt-secret")

async def handler(request):
    user = await auth.verify_request(request)
    if not user:
        return {"status": 401, "error": "Unauthorized"}
    return {"status": 200, "user_id": user.id}
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| JWT caching | Skip repeated verification |
| RLS policy caching | Faster query planning |
| Session refresh batching | Reduce refresh storms |
| Connection pooling | Handle auth spikes |

## Security Considerations

- **Never expose service_role key**: Use only server-side
- **Short-lived JWTs**: 1-hour access tokens
- **Refresh token rotation**: Detect token theft
- **MFA enforcement**: Require for admin users
- **RLS on every table**: Defense in depth

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 on valid request | JWT expired | Implement token refresh |
| RLS blocks legitimate access | Policy missing | Add permissive policy |
| Session not persisting | Cookie not set | Configure cookie options |
| OAuth callback fails | Redirect URL mismatch | Update provider config |

## API Reference

### SupabaseClient

```python
class SupabaseClient:
    def __init__(self, url: str, anon_key: str, service_role_key: str = None)
    async def sign_up(self, email: str, password: str, options: dict = None) -> AuthResult
    async def sign_in(self, email: str, password: str) -> AuthResult
    async def sign_out(self) -> None
    async def get_user(self) -> User
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    role: str
    app_metadata: dict
    user_metadata: dict

@dataclass
class Session:
    access_token: str
    refresh_token: str
    expires_at: int
    user: User
```

## Deployment Guide

### Installation

```bash
pip install supabase-auth
```

### Environment Setup

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Monitoring & Observability

```python
from supabase_auth import MetricsCollector

collector = MetricsCollector()
collector.counter("auth.signin.total", count, tags={"method": method, "status": status})
collector.counter("auth.signup.total", count, tags={"status": status})
collector.histogram("auth.jwt.verify_ms", duration)
collector.counter("auth.mfa.challenge_total", count, tags={"method": method})
```

## Testing Strategy

```python
import pytest
from supabase_auth import SupabaseClient

@pytest.fixture
def client():
    return SupabaseClient(url="http://localhost:54321", anon_key="test-key")

async def test_sign_up(client):
    result = await client.sign_up(email="test@example.com", password="password123")
    assert result.user is not None
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added passkey support | Enable WebAuthn |
| 2.0.0 | New RLS policy format | Migrate policies |

## Glossary

| Term | Definition |
|------|-----------|
| **RLS** | Row-Level Security |
| **JWT** | JSON Web Token |
| **OAuth** | Open Authorization protocol |
| **MFA** | Multi-Factor Authentication |
| **PostgREST** | RESTful API for PostgreSQL |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with email/password and OAuth
- RLS policy management
- MFA support
- Edge Function auth middleware

## Contributing Guidelines

```bash
git clone https://github.com/example/supabase-auth.git
pip install -e ".[dev]"
pytest tests/
```

## Advanced Authentication Patterns

### Multi-Factor Authentication Setup

```typescript
import { supabase } from './client'

async function signInWithMFA(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })
  if (error) throw error

  // Check if MFA is enrolled
  const { data: factors } = await supabase.auth.mfa.listFactors()
  if (factors?.totp.length === 0) {
    // No MFA enrolled Ã¢â‚¬â€ redirect to setup
    return { requiresSetup: true }
  }

  // Challenge the first TOTP factor
  const factorId = factors.totp[0].id
  const { data: challenge, error: challengeError } =
    await supabase.auth.mfa.challenge({ factorId })
  if (challengeError) throw challengeError

  return { requiresChallenge: true, challengeId: challenge.id, factorId }
}

async function verifyMFA(code: string, factorId: string, challengeId: string) {
  const { data, error } = await supabase.auth.mfa.verify({
    factorId,
    challengeId,
    code,
  })
  if (error) throw error
  return data.session
}
```

### Row-Level Security with Auth Context

```sql
-- Policy: Users can only read their own data
CREATE POLICY "Users read own data"
  ON documents
  FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Team members can read team documents
CREATE POLICY "Team members read team docs"
  ON documents
  FOR SELECT
  USING (
    team_id IN (
      SELECT team_id FROM team_members
      WHERE user_id = auth.uid()
    )
  );

-- Policy: Only admins can delete
CREATE POLICY "Admins can delete"
  ON documents
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM team_members
      WHERE user_id = auth.uid()
      AND role = 'admin'
    )
  );
```

### Session Refresh Strategy

```typescript
import { supabase } from './client'

// Proactive session refresh before expiry
async function maintainSession() {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) return

  const expiresAt = session.expires_at * 1000
  const now = Date.now()
  const timeUntilExpiry = expiresAt - now

  // Refresh if less than 5 minutes until expiry
  if (timeUntilExpiry < 5 * 60 * 1000) {
    const { error } = await supabase.auth.refreshSession()
    if (error) {
      // Session refresh failed Ã¢â‚¬â€ user needs to re-authenticate
      await supabase.auth.signOut()
      window.location.href = '/login'
    }
  }
}

// Check every minute
setInterval(maintainSession, 60 * 1000)
```

### Auth Middleware Pattern

```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    { cookies: { getAll: () => request.cookies.getAll() } }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Protected routes
  const protectedPaths = ['/dashboard', '/settings', '/admin']
  if (protectedPaths.some(p => request.nextUrl.pathname.startsWith(p))) {
    if (!user) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Role-based routes
  if (request.nextUrl.pathname.startsWith('/admin')) {
    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', user!.id)
      .single()

    if (profile?.role !== 'admin') {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*', '/admin/:path*']
}
```

### OAuth Provider Configuration Table

| Provider | Scopes | Profile Fields | Notes |
|----------|--------|----------------|-------|
| Google | email profile | email name picture | Most common |
| GitHub | read:user user:email | login email name avatar_url | Developer-focused |
| Discord | identify email | id username email avatar | Gaming/social apps |
| Twitter | tweet.read users.read | id name username | OAuth 2.0 only |
| Apple | name email | name email | Required for iOS apps |

### JWT Claims Reference

```typescript
// Accessing JWT claims in Supabase
const { data: { user } } = await supabase.auth.getUser()

// Standard claims
console.log(user?.id)                    // UUID
console.log(user?.email)                 // User email
console.log(user?.user_metadata)         // Custom user data
console.log(user?.app_metadata)          // App-level data

// Custom claims via edge functions
// Set in Supabase dashboard > Auth > JWT Templates
// {
//   "role": "{{ .user_metadata.role }}",
//   "plan": "{{ .app_metadata.plan }}",
//   "org_id": "{{ .user_metadata.org_id }}"
// }
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### OAuth Provider Reference

| Provider | Scopes | Notes |
|----------|--------|-------|
| Google | openid, email, profile | Most common |
| GitHub | user:email, read:user | Developer-focused |
| Discord | email, identify | Gaming/community |
| Twitter | email, users.read | Social |
| Apple | name, email | iOS apps required |
| Facebook | email, public_profile | Social |
| Azure AD | openid, email | Enterprise |

### RLS Policy Examples

```sql
-- Users can read their own data
CREATE POLICY "Users read own data" ON items
  FOR SELECT USING (auth.uid() = user_id);

-- Users can insert their own data
CREATE POLICY "Users insert own data" ON items
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Team members can read team data
CREATE POLICY "Team members read" ON items
  FOR SELECT USING (
    team_id IN (
      SELECT team_id FROM team_members WHERE user_id = auth.uid()
    )
  );

-- Admins can do everything
CREATE POLICY "Admins full access" ON items
  FOR ALL USING (
    auth.jwt()->>'role' = 'admin'
  );
```

### MFA Configuration Reference

| Method | Security | User Experience | Use Case |
|--------|----------|-----------------|----------|
| TOTP | High | Good | Standard MFA |
| SMS | Medium | Excellent | Fallback |
| Backup codes | High | Good | Recovery |
| WebAuthn | Very high | Excellent | High-security |

### Session Management Reference

| Parameter | Default | Recommended | Description |
|-----------|---------|-------------|-------------|
| Access token expiry | 3600s | 1800-3600s | Short-lived token |
| Refresh token expiry | 604800s | 604800s | 7 days |
| Token refresh interval | 300s | 300-600s | Auto-refresh |
| Session timeout | Ã¢â‚¬â€ | 86400s | Inactivity timeout |

### JWT Claims Reference

| Claim | Description | Example |
|-------|-------------|---------|
| `sub` | User ID | UUID |
| `email` | User email | user@example.com |
| `role` | User role | authenticated |
| `aud` | Audience | authenticated |
| `iss` | Issuer | https://project.supabase.co |
| `exp` | Expiration | Unix timestamp |
| `iat` | Issued at | Unix timestamp |
| `app_metadata` | App metadata | role, provider |
| `user_metadata` | User metadata | name, avatar |

### Auth Flow Reference

```
Email/Password Sign-Up:
1. User submits email + password
2. Supabase creates user in auth.users
3. Confirmation email sent
4. User clicks link Ã¢â€ â€™ email confirmed
5. Session created with JWT

OAuth Sign-In:
1. User clicks provider button
2. Redirect to provider OAuth screen
3. User authorizes app
4. Callback with authorization code
5. Supabase exchanges code for tokens
6. User profile created/updated
7. Session created with JWT

Magic Link:
1. User enters email
2. Supabase sends magic link email
3. User clicks link
4. Session created with JWT
5. Redirect to app
```


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
