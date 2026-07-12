---
name: "api-security"
category: "api"
version: "2.0.0"
tags: ["api", "security", "authentication", "authorization", "oauth", "jwt", "rate-limiting", "owasp"]
---

# API Security

## Overview

Comprehensive API security framework covering authentication (OAuth 2.0, API keys, JWT, mTLS), authorization (RBAC, ABAC, scoped permissions), input validation, rate limiting, CORS, CSRF, injection prevention, and security headers. This module implements OWASP API Security Top 10 protections, provides security middleware for common frameworks, and offers automated security testing tools for identifying vulnerabilities in API endpoints.

## Core Capabilities

- **Authentication**: OAuth 2.0 (authorization code, client credentials, PKCE), API key management, JWT validation, and mTLS client certificates
- **Authorization**: Role-based access control (RBAC), attribute-based access control (ABAC), resource-level permissions, and API scope management
- **Input Validation**: Request schema validation, type coercion prevention, SQL injection detection, XSS filtering, and file upload validation
- **Rate Limiting**: Per-user, per-endpoint, and global rate limits with sliding window, token bucket, and leaky bucket algorithms
- **Security Headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, and CORS policy configuration
- **OWASP API Top 10**: Protections against BOLA, broken authentication, excessive data exposure, lack of rate limiting, and mass assignment
- **Security Testing**: Automated scanning for common API vulnerabilities with severity scoring
- **Audit Logging**: Complete API access logs with user, endpoint, timestamp, and response code

## Usage

```python
from api_security import (
    SecurityMiddleware, OAuthConfig, JWTValidator, RateLimiter, RBACPolicy
)

# Configure OAuth 2.0
oauth = OAuthConfig(
    issuer="https://auth.example.com",
    audience="https://api.example.com",
    scopes=["read:users", "write:users", "admin"],
    token_endpoint="https://auth.example.com/token",
    jwks_uri="https://auth.example.com/.well-known/jwks.json",
)

# JWT validation
validator = JWTValidator(oauth)
token = "eyJhbGciOiJSUzI1NiIs..."
result = validator.validate(token)
print(f"Valid: {result.valid}")
print(f"Scopes: {result.scopes}")
print(f"Expires: {result.expires_at}")

# Rate limiting
limiter = RateLimiter(
    default_limit=100,
    window_seconds=60,
    strategy="sliding_window",
)
limiter.add_limit("POST /api/users", limit=10, window=60)
limiter.add_limit("GET /api/search", limit=30, window=60)

# RBAC policy
rbac = RBACPolicy()
rbac.add_role("admin", permissions=["*"])
rbac.add_role("user", permissions=["read:own", "write:own"])
rbac.add_role("viewer", permissions=["read:all"])
rbac.add_assignment("user-123", "admin")

# Check authorization
authorized = rbac.check("user-123", "write:users")
print(f"Authorized: {authorized}")
```

## Best Practices

- Always use HTTPS — never transmit credentials over plaintext HTTP
- Implement OAuth 2.0 with PKCE for public clients (mobile, SPA)
- Use short-lived JWTs (15 minutes) with refresh token rotation
- Validate JWT signatures against the issuer's JWKS endpoint
- Apply rate limiting at every API endpoint — different limits for different operations
- Validate all input against a schema — never trust client data
- Use parameterized queries to prevent SQL injection
- Implement CORS with explicit origin allowlists — never use wildcard with credentials
- Log all authentication failures and rate limit violations for security monitoring
- Rotate API keys regularly and provide key revocation endpoints
- Use mTLS for service-to-service communication in microservice architectures
- Implement request signing (HMAC) for webhook endpoints

## Related Modules

- **api-design** — Secure API design patterns
- **api-versioning** — Version-aware security policy management
- **api-gateway** → **authentication** — Gateway-level authentication
- **api-gateway** → **rate-limiting** — Distributed rate limiting
- **zero-trust** → **security-framework** — Zero-trust principles for API security
