---
name: "authentication"
category: "api-gateway"
version: "2.0.0"
tags: ["authentication", "oauth2", "jwt", "api-keys", "mtls", "sso", "identity"]
---

# Gateway Authentication

## Overview

Gateway-level authentication and authorization framework for API gateways supporting OAuth 2.0 (all grant types), API key validation, JWT verification, mTLS client certificates, HMAC request signing, and SSO integration. This module provides centralized authentication middleware that validates credentials before requests reach backend services, with token introspection, JWKS caching, session management, and multi-tenant authentication support.

## Core Capabilities

- **OAuth 2.0 Gateway**: Validate access tokens via introspection, JWT verification, and token exchange
- **API Key Management**: Validate, rotate, and revoke API keys with scope-based access control
- **JWT Verification**: JWKS-based signature verification with key rotation and caching
- **mTLS Support**: Client certificate validation against trusted CA bundles
- **HMAC Signing**: Request signature validation for webhook and inter-service authentication
- **Token Introspection**: RFC 7662 token introspection with caching
- **SSO Integration**: SAML, OIDC, and LDAP integration for enterprise SSO
- **Multi-Tenant**: Tenant-aware authentication with per-tenant identity providers

## Usage

```python
from authentication import (
    AuthMiddleware, OAuth2Config, APIKeyStore, JWTVerifier, MTLSConfig
)

# Configure OAuth 2.0
oauth = OAuth2Config(
    issuer="https://auth.example.com",
    audience="https://api.example.com",
    jwks_uri="https://auth.example.com/.well-known/jwks.json",
    introspection_endpoint="https://auth.example.com/introspect",
    scopes_supported=["read", "write", "admin"],
)

# API key store
api_keys = APIKeyStore()
api_keys.add_key(
    key_id="ak_live_abc123",
    name="Production App",
    scopes=["read", "write"],
    rate_limit=1000,
    expires_at="2025-12-31T23:59:59Z",
)

# JWT verifier
jwt_verifier = JWTVerifier(oauth)

# MTLS config
mtls = MTLSConfig(
    client_ca_bundle="/etc/ssl/client-ca.pem",
    verify_client_cert=True,
    allowed_cn_patterns=["*.internal.example.com"],
)

# Create middleware
auth = AuthMiddleware(
    oauth_config=oauth,
    api_key_store=api_keys,
    jwt_verifier=jwt_verifier,
    mtls_config=mtls,
    routes={
        "/api/public/*": {"auth": False},
        "/api/admin/*": {"required_scopes": ["admin"]},
        "/api/users/*": {"required_scopes": ["read"]},
    },
)

# Authenticate request
result = auth.authenticate(
    path="/api/users/123",
    headers={"Authorization": "Bearer eyJhbGciOi..."},
    method="GET",
)
print(f"Authenticated: {result.authenticated}")
print(f"User: {result.user_id}")
print(f"Scopes: {result.scopes}")
print(f"Method: {result.auth_method}")
```

## Best Practices

- Always validate JWT signatures against the issuer's JWKS endpoint — never skip verification
- Use short-lived access tokens (15 minutes) with refresh token rotation
- Implement token introspection caching (5-10 minutes) to reduce latency
- Apply different authentication levels per route — public endpoints need no auth
- Use API keys only for server-to-server communication, not for end-user authentication
- Implement mTLS for service-to-service communication in zero-trust architectures
- Monitor authentication failures for brute-force and credential stuffing attacks
- Cache JWKS keys with appropriate TTL (1 hour) and handle key rotation gracefully
- Use HMAC signing for webhook endpoints to prevent request forgery
- Implement graceful degradation — if identity provider is down, fail closed (deny)

## Related Modules

- **api-security** — Security middleware and OWASP protections
- **api-gateway** → **api-management** — Gateway configuration with auth plugins
- **api-gateway** → **rate-limiting** — Rate limiting tied to authenticated consumers
- **zero-trust** → **identity-verification** — Zero-trust identity verification
- **api-gateway** → **caching** — Token and JWKS caching strategies
