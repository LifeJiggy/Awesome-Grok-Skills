---
name: "secure-coding"
category: "security"
version: "2.0.0"
tags: ["security", "secure-coding", "owasp", "injection", "input-validation", "cryptography", "defense-in-depth"]
---

# Secure Coding

## Overview

Secure coding is the discipline of writing software that is resilient against exploitation by design, embedding security into every line of code rather than bolting it on after deployment. This module provides a comprehensive toolkit for defensive programming: input validation and sanitization, context-aware output encoding, cryptographic operations, authentication and session management, safe error handling, memory-safe patterns, and supply-chain integrity. Every technique maps directly to OWASP Top 10, SANS Top 25, and CWE classifications, giving developers a systematic way to eliminate entire vulnerability classes at the source level.

The core philosophy is "eliminate, don't detect." While DAST and SAST tools find vulnerabilities at runtime or post-commit, secure coding prevents those vulnerabilities from existing in the first place. This is achieved through a layered defense-in-depth approach: input validation at the boundary, parameterized queries against injection, output encoding against XSS, authenticated encryption for confidentiality and integrity, and least-privilege execution for blast-radius containment. Each layer independently stops an attack vector, so compromising one layer does not yield system compromise.

This module is designed for practical integration into development workflows. Every example uses real-world patterns: Flask/Django request validation, SQLAlchemy parameterized queries, bcrypt/Argon2id password hashing, JWT token lifecycle management, CSP header generation, and dependency vulnerability scanning in CI. The module bridges the gap between abstract security guidance and implementable code, providing developers with copy-paste-ready patterns that enforce security by default. Secure coding is the foundation upon which threat models, architecture, and compliance controls depend.

## Core Capabilities

1. **Input Validation & Sanitization** — Validate all untrusted input at system boundaries using allowlists, type checking, length constraints, and format verification. Reject rather than sanitize malformed data. Support for nested object validation, array bounds checking, and custom format validators.

2. **Context-Aware Output Encoding** — Apply encoding that matches the output context: HTML entity encoding, JavaScript string encoding, URL percent-encoding, CSS value encoding, and XML CDATA wrapping. Use parameterized queries for all database interactions to eliminate SQL injection.

3. **Cryptographic Operations** — Authenticated encryption (AES-256-GCM, ChaCha20-Poly1305), secure key derivation (Argon2id, scrypt, PBKDF2), TLS 1.3 configuration, digital signature verification, and random number generation using cryptographic CSPRNGs.

4. **Authentication & Session Management** — Secure password storage with Argon2id or bcrypt, MFA enrollment and verification flows, session token generation using CSPRNGs, cookie security flags (Secure, HttpOnly, SameSite), and session fixation prevention.

5. **Error Handling & Information Disclosure Prevention** — Structured error handling that returns generic messages to users while logging detailed diagnostics server-side. Prevent stack traces, database errors, internal paths, and configuration details from leaking in responses.

6. **Memory Safety & Safe Deserialization** — Prevention of buffer overflows, use-after-free, and format string vulnerabilities. Safe deserialization using schema validation (JSON Schema, Pydantic) instead of arbitrary object instantiation. Elimination of `eval()`, `exec()`, and dynamic code execution patterns.

7. **Dependency & Supply-Chain Security** — Software composition analysis (SCA), lock file pinning, vulnerability scanning (pip-audit, npm audit, trivy), SBOM generation, and provenance verification to prevent supply-chain attacks.

8. **Secure Configuration & Secrets Management** — Environment variable handling, secrets rotation, configuration file protection, and avoidance of hardcoded credentials in source code.

9. **Code Review & Static Analysis Integration** — Integration with bandit, semgrep, CodeQL, and custom rules for automated security review in CI/CD pipelines.

10. **Security Logging & Audit Trail** — Structured security event logging with field-level redaction of sensitive data, audit trail generation, and correlation with SIEM systems.

## Usage Examples

### Input Validation Framework

```python
from secure_coding import InputValidator, ValidationRule, ValidationError

# Define validation rules for a user registration endpoint
rules = [
    ValidationRule(field="username", type=str, min_length=3, max_length=32,
                   pattern=r"^[a-zA-Z0-9_-]+$"),
    ValidationRule(field="email", type=str, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
    ValidationRule(field="password", type=str, min_length=12, max_length=128,
                   require_uppercase=True, require_digit=True, require_special=True),
    ValidationRule(field="age", type=int, min_value=0, max_value=150),
    ValidationRule(field="bio", type=str, max_length=500, nullable=True),
    ValidationRule(field="website", type=str, pattern=r"^https://[a-zA-Z0-9.-]+(/.*)?$",
                   nullable=True),
]

validator = InputValidator(rules)

# Validate incoming request data
try:
    clean_data = validator.validate({
        "username": "alice_42",
        "email": "alice@example.com",
        "password": "S3cure!Passw0rd",
        "age": 28,
        "bio": "Security researcher",
        "website": "https://alice.dev"
    })
except ValidationError as e:
    print(f"Validation failed: {e.errors}")
    # Returns: ['Field age must be <= 150', 'Pattern mismatch for email']
```

### Parameterized Database Query

```python
from secure_coding import SecureQueryBuilder

# Never use string formatting for SQL — use parameterized queries
query_builder = SecureQueryBuilder(db_connection)

# UNSAFE (never do this — SQL injection vulnerability):
# cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
# cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)

# SAFE (parameterized — user input is never interpolated into SQL):
user_id = request.args.get("id")
result = query_builder.execute(
    "SELECT id, name, email FROM users WHERE id = %s AND active = %s",
    params=[user_id, True]
)

# SAFE with ORM (SQLAlchemy uses parameters under the hood):
user = session.query(User).filter(User.id == user_id, User.active == True).first()

# SAFE with dynamic conditions (parameterized WHERE construction):
filters = []
params = []
if request.args.get("email"):
    filters.append("email = %s")
    params.append(request.args["email"])
if request.args.get("role"):
    filters.append("role = %s")
    params.append(request.args["role"])
where_clause = " AND ".join(filters) if filters else "1=1"
result = query_builder.execute(
    f"SELECT * FROM users WHERE {where_clause}",
    params=params
)
```

### Secure Password Hashing

```python
from secure_coding import PasswordManager

pwd_manager = PasswordManager(algorithm="argon2id")

# Hash a password during registration
# Argon2id uses memory-hard computation to resist GPU/ASIC attacks
stored_hash = pwd_manager.hash("user_password_123!")
# Output: $argon2id$v=19$m=65536,t=3,p=4$salt$hash

# Verify during login (constant-time comparison to prevent timing attacks)
is_valid = pwd_manager.verify("user_password_123!", stored_hash)

# Check if hash needs rehashing (algorithm upgrade or parameter increase)
if pwd_manager.needs_rehash(stored_hash):
    new_hash = pwd_manager.hash("user_password_123!")
    # Update in database — next login will use stronger parameters

# Rate-limit password attempts per account
if pwd_manager.too_many_failed_attempts(user_id):
    raise AccountLockedError("Account locked after 5 failed attempts")
```

### Content Security Policy Generator

```python
from secure_coding import CSPBuilder

csp = CSPBuilder()
csp.add_directive("default-src", ["'self'"])
csp.add_directive("script-src", ["'self'", "cdn.example.com", "'nonce-abc123'"])
csp.add_directive("style-src", ["'self'", "'nonce-abc123'"])
csp.add_directive("img-src", ["'self'", "data:", "https:"])
csp.add_directive("connect-src", ["'self'", "api.example.com"])
csp.add_directive("font-src", ["'self'", "fonts.gstatic.com"])
csp.add_directive("frame-ancestors", ["'none'"])
csp.add_directive("base-uri", ["'self'"])
csp.add_directive("form-action", ["'self'"])

header = csp.build()
# Returns: "default-src 'self'; script-src 'self' cdn.example.com 'nonce-abc123'; ..."

# Generate report-only policy for testing before enforcement
report_only = csp.build(enforce=False, report_uri="/csp-report")
```

### Secure Request Handler with Defense-in-Depth

```python
from secure_coding import SecureHandler, RateLimiter, AuditLogger

handler = SecureHandler()
rate_limiter = RateLimiter(redis_client, max_requests=100, window_seconds=60)
audit = AuditLogger(structured=True, redact_fields=["password", "token", "ssn"])

@handler.route("/api/users", methods=["POST"])
@rate_limiter.limit
def create_user():
    # Layer 1: Rate limiting
    # Layer 2: Input validation (rejects invalid payloads)
    data = handler.validate_request(request.json, schema=UserCreateSchema)

    # Layer 3: Authentication check
    current_user = handler.require_auth(request, required_role="admin")

    # Layer 4: Authorization (RBAC)
    handler.require_permission(current_user, "users:create")

    # Layer 5: Parameterized query (no SQL injection)
    existing = db.query("SELECT id FROM users WHERE email = %s", [data.email])
    if existing:
        raise ConflictError("Email already registered")

    # Layer 6: Secure password handling (Argon2id)
    hashed = PasswordManager().hash(data.password)

    # Layer 7: Audit logging (no secrets in logs)
    audit.log("user_created", user=current_user.id, email=data.email)

    # Layer 8: Return generic success (no internal details leaked)
    return jsonify({"status": "created", "user_id": new_user.id}), 201
```

### Dependency Vulnerability Scanning

```python
from secure_coding import DependencyScanner, VulnerabilityPolicy

scanner = DependencyScanner(
    lock_files=["requirements.lock", "package-lock.json"],
    policy=VulnerabilityPolicy(
        block_on=["critical", "high"],
        warn_on=["medium"],
        ignore_known_fp=True
    )
)

# Scan all dependencies
results = scanner.scan()

for vuln in results.vulnerabilities:
    print(f"{vuln.package}@{vuln.installed_version}: {vuln.cve_id}")
    print(f"  Severity: {vuln.severity}")
    print(f"  Fixed in: {vuln.fixed_version or 'no fix yet'}")
    print(f"  EPSS: {vuln.epss_probability:.1%}")

# Generate SBOM for audit trail
sbom = scanner.generate_sbom(format="cyclonedx")
print(f"SBOM generated: {len(sbom.components)} components")
```

## Architecture

The secure coding module follows a layered defense-in-depth architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    External Input                       │
│    (HTTP requests, CLI args, file uploads, APIs)        │
└──────────────────────┬──────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │ Input Validation │  ← Allowlist-based, type-checked
              │   & Sanitization │  ← Reject malformed data early
              └────────┬────────┘
                       │
           ┌───────────▼───────────┐
           │  Authentication &      │  ← Argon2id/bcrypt, MFA
           │  Authorization Check   │  ← RBAC/ABAC enforcement
           └───────────┬───────────┘
                       │
          ┌────────────▼────────────┐
          │   Business Logic Layer  │  ← Parameterized queries
          │   (Secure Coding)       │  ← No eval/exec, safe deser
          └────────────┬────────────┘
                       │
         ┌─────────────▼─────────────┐
         │  Output Encoding Layer    │  ← Context-aware encoding
         │  (XSS Prevention)         │  ← CSP headers, escaping
         └─────────────┬─────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   Error Handling Layer      │  ← Generic user messages
        │   & Security Logging        │  ← Structured audit logs
        └──────────────┬──────────────┘
                       │
          ┌────────────▼────────────┐
          │  Cryptographic Layer    │  ← AES-GCM, TLS 1.3
          │  (Confidentiality &     │  ← Key management, rotation
          │   Integrity)            │
          └────────────┬────────────┘
                       │
    ┌──────────────────▼──────────────────┐
    │  Dependency & Supply-Chain Layer    │  ← SCA scanning, SBOM
    │  (External Component Security)      │  ← Provenance verification
    └─────────────────────────────────────┘
```

Each layer is independent — if an attacker bypasses input validation, parameterized queries still prevent SQL injection. If output encoding is missed, CSP headers still block script execution. This redundancy is intentional and essential.

## Best Practices

1. **Never trust user input** — Treat all data from HTTP requests, command-line arguments, file uploads, environment variables, and external APIs as untrusted. Validate at every boundary using allowlists rather than blocklists.

2. **Use parameterized queries everywhere** — No exceptions for "quick queries," internal tools, or debug code. ORM query builders are acceptable only when they use parameterized queries internally. String interpolation in SQL is always a vulnerability.

3. **Apply defense in depth** — Layer multiple independent controls: input validation + output encoding + parameterized queries + least privilege + monitoring. Each layer independently stops attacks.

4. **Fail securely** — Default deny on all authorization checks. When validation fails, return generic error messages to users and log detailed diagnostics server-side. Never expose stack traces, database errors, or internal paths.

5. **Use established libraries** — Don't roll your own cryptography, authentication, or session management. Use vetted, actively maintained libraries with strong community review (cryptography, argon2-cffi, PyJWT, etc.).

6. **Keep dependencies updated** — Run `pip-audit`, `npm audit`, or `trivy` in CI. Pin transitive dependencies in lock files. Monitor CVE databases and automated alerts (Dependabot, Renovate).

7. **Apply least privilege at every layer** — Database accounts, file system permissions, API tokens, container capabilities, and IAM roles should have only the minimum permissions needed for their function.

8. **Never log secrets or PII** — Redact tokens, passwords, API keys, SSNs, and other sensitive data from all log outputs. Use structured logging with field-level redaction rules.

9. **Use type hints and static analysis** — Enable mypy strict mode, use `bandit` for Python security linting, `semgrep` for pattern-based vulnerability detection, and `CodeQL` for deep semantic analysis.

10. **Review code for security** — Include security-focused review in every PR checklist. Specifically check for injection vectors, SSRF paths, path traversal, authentication bypass, and authorization gaps. Use automated security review tools alongside human review.

## Performance Considerations

- **Argon2id memory cost**: Default 64MB memory, 3 iterations, 4 parallelism. Tune based on server resources — higher memory costs increase resistance to GPU attacks but increase login latency.
- **Parameterized queries**: Negligible overhead vs string formatting. Modern database drivers cache parameterized query plans, so there is no performance penalty for using parameters.
- **Output encoding**: HTML entity encoding adds ~5% overhead for response size. CSP headers are small (<1KB) and cached by browsers.
- **SCA scanning**: Full dependency scans take 5-30 seconds depending on lock file size. Run in CI parallel with tests, not as a blocking step.
- **Rate limiting**: Redis-backed rate limiters add <1ms latency per request. In-memory rate limiters are faster but don't work across instances.
- **TLS termination**: TLS 1.3 handshakes are 1-RTT (0-RTT with resumption). Offload to a reverse proxy (nginx, Cloudflare) for production workloads.

## Security Considerations

- **Timing attacks**: Use constant-time comparison for password verification, token comparison, and HMAC validation. Python's `hmac.compare_digest()` provides this.
- **Unicode normalization**: Apply NFKC normalization before validation to prevent bypass via Unicode homoglyphs (e.g., fullwidth characters, confusables).
- **Injection beyond SQL**: Command injection (shell=True), LDAP injection, NoSQL injection, XPath injection, and template injection are all real threats. Parameterize all query interfaces, not just SQL.
- **Deserialization attacks**: Never use `pickle.loads()`, `yaml.load()` without SafeLoader, or `eval()` on untrusted data. Use JSON Schema validation for all deserialized input.
- **Key management**: Never commit secrets to version control. Use environment variables, vault systems, or cloud KMS. Rotate keys on a schedule and on compromise detection.
- **CSRF protection**: Use synchronized token patterns or SameSite cookies for all state-changing requests. GET requests should never cause side effects.
- **Clickjacking**: Set X-Frame-Options: DENY or use CSP frame-ancestors 'none' on pages that should not be embedded.
- **Open redirect**: Validate redirect URLs against an allowlist of trusted domains. Never redirect to user-supplied URLs without validation.

## Related Modules

- **threat-modeling** — Identify what needs to be protected before writing secure code
- **vulnerability-management** — Track and remediate discovered vulnerabilities
- **security-architecture** — Design system-level security controls
- **compliance** — Map secure coding practices to regulatory requirements (PCI DSS 6.5, OWASP ASVS)
- **hunt-xss** — Practical XSS testing patterns that validate output encoding effectiveness
- **hunt-sqli** — SQL injection testing that validates parameterized query implementations
- **web2-vuln-classes** — Complete reference for web vulnerability classes and mitigations

## References

- OWASP Top 10 (2021): https://owasp.org/www-project-top-ten/
- OWASP Application Security Verification Standard (ASVS): https://owasp.org/www-project-application-security-verification-standard/
- SANS Top 25 Most Dangerous Software Weaknesses: https://sans.org/top25
- CWE/SANS Top 25: https://cwe.mitre.org/top25/
- NIST Secure Software Development Framework (SSDF): https://csrc.nist.gov/publications/detail/sp/800-218/final
- CERT C Coding Standard (Memory Safety): https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard
- Python Security Best Practices: https://python-security.readthedocs.io/
- Node.js Security Checklist: https://blog.risingstack.com/node-js-security-checklist/
- Argon2 Password Hashing: https://argon2.online/
- Bandit Python Security Linter: https://bandit.readthedocs.io/
- Semgrep Rules Registry: https://semgrep.dev/rules

---

## OWASP Top 10 Prevention Patterns

### A01: Broken Access Control Prevention

```python
from secure_coding import AccessControlEnforcer, Permission, ResourceScope

enforcer = AccessControlEnforcer()

# Object-level authorization (prevents IDOR)
# UNSAFE pattern - never check only resource type, check ownership
# @app.get("/api/orders/<order_id>")
# def get_order(order_id):
#     return db.query(Order).filter(Order.id == order_id).first()  # ANY user can see ANY order

# SAFE pattern - always include user context
@app.get("/api/orders/<order_id>")
@enforcer.authorize
def get_order(order_id):
    current_user = get_current_user(request)
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id  # Ownership check
    ).first()
    if not order:
        return jsonify({"error": "Not found"}), 404
    return jsonify(order.to_dict())

# Function-level authorization decorator
@enforcer.require_permissions("orders:read")
def get_order(order_id):
    pass

# Resource-level RBAC with conditions
permissions = [
    Permission(
        resource="orders",
        actions=["read", "write"],
        conditions={
            "owner_only": True,  # Users can only access their own orders
            "admin_override": True  # Admins can access all orders
        }
    ),
    Permission(
        resource="reports",
        actions=["read"],
        conditions={
            "department": "finance",  # Only finance department
            "clearance_level_min": 3  # Minimum clearance level
        }
    ),
]

# Path traversal prevention
from secure_coding import SecureFilePath

secure_path = SecureFilePath(base_dir="/uploads", allowed_extensions=["pdf", "png", "jpg"])

# UNSAFE:
# @app.get("/files/<filename>")
# def get_file(filename):
#     return send_file(f"/uploads/{filename}")  # Path traversal: /../../../etc/passwd

# SAFE:
@app.get("/files/<filename>")
def get_file(filename):
    safe_path = secure_path.resolve(filename)
    if safe_path is None:
        return jsonify({"error": "Invalid filename"}), 400
    return send_file(safe_path)
```

### A03: Injection Prevention

```python
from secure_coding import SQLInjectionPrevention, CommandInjectionPrevention, LDAPInjectionPrevention

# SQL Injection prevention - multiple layers
sql_guard = SQLInjectionPrevention()

# Layer 1: Parameterized queries (primary defense)
# UNSAFE: cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# SAFE:
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))

# Layer 2: Input validation (defense in depth)
from secure_coding import InputValidator
name_validator = InputValidator(
    field="name",
    type=str,
    pattern=r"^[a-zA-Z0-9_]{3,50}$",
    reject_special_chars=True
)
clean_name = name_validator.validate(raw_name)

# Layer 3: Stored procedure (additional defense)
cursor.callproc("get_user_by_name", (clean_name,))

# Command injection prevention
cmd_guard = CommandInjectionPrevention()

# UNSAFE:
# import subprocess
# subprocess.run(f"ping {host}", shell=True)  # Command injection: ; rm -rf /

# SAFE:
import shlex
import subprocess

# Option 1: Use shlex.quote for shell commands
safe_host = shlex.quote(host)
subprocess.run(f"ping {safe_host}", shell=True)

# Option 2: Avoid shell=True entirely
subprocess.run(["ping", host])  # No shell interpretation

# Option 3: Use a dedicated library
import socket
ip = socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]

# LDAP injection prevention
ldap_guard = LDAPInjectionPrevention()

# UNSAFE:
# conn.search("dc=example,dc=com", f"(uid={user_input})")

# SAFE:
import ldap3
# Escape special characters in LDAP input
safe_input = ldap3.utils.conv.escape_filter_chars(user_input)
conn.search("dc=example,dc=com", f"(uid={safe_input})")
```

### A05: Security Misconfiguration Prevention

```python
from secure_coding import SecurityHeaders, TLSConfig, ErrorHandling

# Security headers middleware
headers = SecurityHeaders()

# Generate comprehensive security headers
header_config = headers.generate(
    content_security_policy="default-src 'self'; script-src 'self' 'nonce-{random}'; style-src 'self' 'nonce-{random}'",
    strict_transport_security="max-age=63072000; includeSubDomains; preload",
    x_content_type_options="nosniff",
    x_frame_options="DENY",
    x_xss_protection="0",  # Deprecated, rely on CSP instead
    referrer_policy="strict-origin-when-cross-origin",
    permissions_policy="camera=(), microphone=(), geolocation=()",
    cross_origin_opener_policy="same-origin",
    cross_origin_resource_policy="same-origin",
    cross_origin_embedder_policy="require-corp",
)

# TLS configuration hardened for production
tls = TLSConfig()
tls_config = tls.configure(
    min_version="TLSv1.2",
    preferred_version="TLSv1.3",
    ciphers=[
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384",
    ],
    disable_compression=True,
    session_tickets=False,  # Disable for perfect forward secrecy
    ocsp_stapling=True,
    hsts_max_age=63072000,
)

# Secure error handling
error_handler = SecurityHeaders()

@app.errorhandler(404)
def not_found(error):
    # SAFE: Generic error message, detailed logging server-side
    logger.warning(f"404: {request.remote_addr} {request.path}")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    # SAFE: Never expose stack traces to clients
    logger.error(f"500: {traceback.format_exc()}")
    return jsonify({"error": "Internal server error"}), 500
```

### A08: Software and Data Integrity Failures Prevention

```python
from secure_coding import IntegrityVerifier, DependencyVerifier

verifier = IntegrityVerifier()

# Verify file integrity before processing
def upload_file(file):
    # Calculate SHA-256 hash before processing
    file_hash = verifier.hash_file(file, algorithm="sha256")
    
    # Verify against known hash (if provided)
    if expected_hash:
        if not verifier.verify_hash(file_hash, expected_hash):
            return jsonify({"error": "File integrity check failed"}), 400
    
    # Store hash with file metadata
    save_file_with_hash(file, file_hash)

# Dependency integrity verification
dep_verifier = DependencyVerifier()

# Verify lock file integrity
integrity = dep_verifier.verify_lock_file(
    lock_file="package-lock.json",
    check_integrity=True,  # Verify package hashes
    check_signatures=True,  # Verify npm package signatures
)

if not integrity.valid:
    for violation in integrity.violations:
        print(f"Integrity violation: {violation.package}")
        print(f"  Expected: {violation.expected_hash}")
        print(f"  Actual: {violation.actual_hash}")

# CI/CD pipeline integrity
from secure_coding import CIPipelineSecurity

pipeline_security = CIPipelineSecurity()

# Verify build artifact integrity
artifact = pipeline_security.verify_artifact(
    artifact_path="./dist/app.tar.gz",
    signature_file="./dist/app.tar.gz.sig",
    public_key="vault://signing-key",
    expected_hash="sha256:abc123..."
)
print(f"Artifact verified: {artifact.verified}")
print(f"Signer: {artifact.signer}")
print(f"Timestamp: {artifact.timestamp}")
```

## Secure API Design Patterns

### API Authentication and Rate Limiting

```python
from secure_coding import APISecurity, OAuth2Validator, RateLimiter

api_security = APISecurity()

# OAuth 2.0 token validation
@app.before_request
def validate_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401
    
    claims = api_security.validate_oauth_token(
        token=token,
        expected_issuer="https://auth.example.com",
        expected_audience="api.example.com",
        required_scopes=["read:users", "write:users"],
        clock_skew_seconds=30
    )
    
    if not claims.valid:
        return jsonify({"error": "Invalid token", "detail": claims.error}), 401
    
    request.current_user = claims.subject
    request.token_scopes = claims.scopes

# API key authentication with rotation
api_key_store = APISecurity()

def authenticate_api_key():
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "Missing API key"}), 401
    
    # Constant-time comparison to prevent timing attacks
    key_info = api_key_store.validate_api_key(
        key=api_key,
        key_type="production",
        required_permissions=["data:read"],
        rate_limit_tier="standard"
    )
    
    if not key_info.valid:
        return jsonify({"error": "Invalid API key"}), 401
    
    request.api_client = key_info.client_id

# Rate limiting per API key
rate_limiter = RateLimiter(
    backend="redis",
    tiers={
        "free": {"requests": 100, "window": 3600},
        "standard": {"requests": 1000, "window": 3600},
        "premium": {"requests": 10000, "window": 3600},
    }
)

@app.after_request
def add_rate_limit_headers(response):
    tier = getattr(request, "rate_limit_tier", "free")
    limit = rate_limiter.get_limit(tier)
    remaining = rate_limiter.get_remaining(request.api_key)
    
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 3600)
    
    return response
```

### Secure API Response Design

```python
from secure_coding import SecureResponseBuilder, FieldFilter

builder = SecureResponseBuilder()

# Filter sensitive fields from API responses
response_filter = FieldFilter(
    remove_fields=["password_hash", "ssn", "api_key", "secret"],
    mask_fields={"email": "email_mask", "phone": "phone_mask"},
    redact_patterns=[r"\b\d{4}-\d{4}-\d{4}-\d{4}\b"],  # Credit card numbers
)

# SAFE: Filter before returning to client
@app.get("/api/users/<user_id>")
def get_user(user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({"error": "Not found"}), 404
    
    # Filter sensitive fields
    safe_response = response_filter.apply(user.to_dict())
    return jsonify(safe_response)

# Safe pagination with no data leakage
@app.get("/api/users")
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)  # Cap at 100
    
    users = db.query(User).offset((page - 1) * per_page).limit(per_page).all()
    total = db.query(User).count()
    
    # SAFE: Never expose total count that reveals data volume to attackers
    # Use safe response that masks exact counts for unprivileged users
    return builder.paginate(
        items=[response_filter.apply(u.to_dict()) for u in users],
        page=page,
        per_page=per_page,
        total=total,
        expose_total=get_current_user(request).has_permission("users:list:count")
    )
```

## Input Validation Deep Dive

### Schema Validation with Pydantic

```python
from pydantic import BaseModel, Field, validator, constr
from typing import Optional, List
from secure_coding import StrictPydanticConfig

class UserRegistration(BaseModel):
    """Strict schema validation for user registration"""
    
    username: constr(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr  # Pydantic validates email format
    password: constr(min_length=12, max_length=128)
    age: int = Field(ge=0, le=150)
    bio: Optional[constr(max_length=500)] = None
    website: Optional[HttpUrl] = None
    roles: List[str] = Field(default=["user"], max_items=5)
    
    @validator("password")
    def validate_password_strength(cls, v):
        """Enforce password complexity"""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letters")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digits")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain special characters")
        return v
    
    @validator("roles")
    def validate_roles(cls, v):
        """Whitelist allowed roles"""
        allowed_roles = {"user", "admin", "moderator"}
        for role in v:
            if role not in allowed_roles:
                raise ValueError(f"Invalid role: {role}")
        return v

    class Config:
        config = StrictPydanticConfig  # Reject extra fields

# Usage
try:
    user_data = UserRegistration(**request.json)
except ValidationError as e:
    return jsonify({"error": "Validation failed", "details": e.errors()}), 400
```

### File Upload Validation

```python
from secure_coding import SecureFileUpload, FileValidator

upload_handler = SecureFileUpload(
    max_size_mb=10,
    allowed_types=["image/jpeg", "image/png", "image/gif", "application/pdf"],
    max_files=5,
    quarantine_dir="/tmp/quarantine",
)

@app.route("/upload", methods=["POST"])
def upload_file():
    files = request.files.getlist("files")
    
    for file in files:
        # Layer 1: MIME type validation
        mime_type = upload_handler.detect_mime_type(file)
        if mime_type not in upload_handler.allowed_types:
            return jsonify({"error": f"File type {mime_type} not allowed"}), 400
        
        # Layer 2: Magic bytes validation (prevents MIME type spoofing)
        if not upload_handler.verify_magic_bytes(file, mime_type):
            return jsonify({"error": "File content does not match declared type"}), 400
        
        # Layer 3: File size check
        if file.content_length > upload_handler.max_size_bytes:
            return jsonify({"error": "File too large"}), 400
        
        # Layer 4: Filename sanitization
        safe_filename = upload_handler.sanitize_filename(file.filename)
        
        # Layer 5: Content scanning (clamav, trivy)
        scan_result = upload_handler.scan_content(file)
        if scan_result.threat_detected:
            logger.warning(f"Malicious upload blocked: {scan_result.threat}")
            return jsonify({"error": "File rejected"}), 400
        
        # Layer 6: Save with random name (prevent path traversal in filename)
        saved_path = upload_handler.save(
            file=file,
            filename=safe_filename,
            storage="/uploads",
            use_uuid_name=True  # Generate UUID-based filename
        )
        
        return jsonify({
            "status": "uploaded",
            "filename": safe_filename,
            "stored_path": saved_path,
            "size": file.content_length,
            "type": mime_type,
        }), 201
```

## Cryptographic Operations

### Encryption at Rest

```python
from secure_coding import EncryptionManager, KeyManager
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key_manager = KeyManager(backend="aws_kms")

# Encrypt sensitive data before storage
def encrypt_pii(plaintext: str, context: dict) -> dict:
    """Encrypt PII with authenticated encryption"""
    # Get encryption key from KMS
    key_id = "alias/customer-data"
    key = key_manager.get_key(key_id)
    
    # Generate random nonce
    nonce = os.urandom(12)  # 96-bit nonce for AES-GCM
    
    # Additional authenticated data (AAD) for context binding
    aad = json.dumps(context).encode()
    
    # Encrypt with AES-256-GCM (authenticated encryption)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), aad)
    
    return {
        "ciphertext": ciphertext.hex(),
        "nonce": nonce.hex(),
        "key_id": key_id,
        "algorithm": "AES-256-GCM",
        "aad_context": context,
    }

# Decrypt PII
def decrypt_pii(encrypted_data: dict) -> str:
    """Decrypt PII with authentication verification"""
    key = key_manager.get_key(encrypted_data["key_id"])
    
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(
        bytes.fromhex(encrypted_data["nonce"]),
        bytes.fromhex(encrypted_data["ciphertext"]),
        json.dumps(encrypted_data["aad_context"]).encode()
    )
    
    return plaintext.decode()

# Key rotation support
def rotate_encryption_key(old_key_id: str, new_key_id: str):
    """Rotate encryption key for all records using old key"""
    records = db.query(EncryptedData).filter(EncryptedData.key_id == old_key_id)
    
    old_key = key_manager.get_key(old_key_id)
    new_key = key_manager.get_key(new_key_id)
    
    for record in records:
        # Decrypt with old key
        aesgcm_old = AESGCM(old_key)
        plaintext = aesgcm_old.decrypt(
            bytes.fromhex(record.nonce),
            bytes.fromhex(record.ciphertext),
            record.aad
        )
        
        # Re-encrypt with new key
        nonce = os.urandom(12)
        aesgcm_new = AESGCM(new_key)
        new_ciphertext = aesgcm_new.encrypt(nonce, plaintext, record.aad)
        
        # Update record
        record.ciphertext = new_ciphertext.hex()
        record.nonce = nonce.hex()
        record.key_id = new_key_id
        db.commit()
```

### Secure Token Generation

```python
from secure_coding import TokenGenerator, SecureRandom

# Generate cryptographically secure tokens
token_gen = TokenGenerator()

# API key generation
api_key = token_gen.generate_api_key(
    prefix="sk_live_",  # Identifyable prefix
    length=48,  # 48 bytes = 384 bits of entropy
    format="hex"
)
print(f"API Key: {api_key}")

# Session token generation
session_token = token_gen.generate_session_token(
    length=64,  # 64 bytes = 512 bits
    format="url_safe"  # URL-safe base64
)

# CSRF token generation
csrf_token = token_gen.generate_csrf_token(
    user_session=session_id,
    secret_key=app.config["SECRET_KEY"]
)

# Secure random number generation
secure_random = SecureRandom()
random_int = secure_random.randint(1, 1000000)
random_bytes = secure_random.bytes(32)
random_string = secure_random.alphanumeric(16)

# Token with expiration
signed_token = token_gen.generate_signed_token(
    payload={"user_id": user.id, "role": user.role},
    secret=app.config["JWT_SECRET"],
    algorithm="HS256",
    expires_in_hours=1,
    issuer="auth.example.com",
    audience="api.example.com"
)
```

## Secure Deserialization

### Safe JSON Processing

```python
from secure_coding import SafeDeserializer, DeserializationPolicy

deserializer = SafeDeserializer(
    policy=DeserializationPolicy(
        max_depth=5,           # Prevent deeply nested bombs
        max_items=10000,       # Limit array sizes
        max_string_length=10000,  # Limit string lengths
        disallow_special_types=True,  # Reject __proto__, __class__, etc
    )
)

# Safe JSON deserialization
def process_request_body():
    raw_data = request.get_data(as_text=True)
    
    try:
        data = deserializer.safe_loads(
            raw_data,
            schema=expected_schema,  # Validate against expected schema
            strict=True,  # Reject extra fields
        )
    except DeserializationError as e:
        return jsonify({"error": "Invalid request body", "detail": str(e)}), 400
    
    return data

# Safe YAML deserialization
from secure_coding import SafeYAML

yaml_data = SafeYAML.safe_load(yaml_string)
# Never use: yaml.load(yaml_string)  # Arbitrary code execution

# Safe pickle deserialization (avoid if possible)
from secure_coding import SafePickle

# Only deserialize from trusted sources
trusted_data = SafePickle.loads(
    pickle_bytes,
    allowed_classes=["dict", "list", "str", "int", "float"],
    max_size_bytes=1024 * 1024  # 1MB limit
)
```

## Security Logging and Audit Trail

```python
from secure_coding import SecurityLogger, AuditTrail, LogField

logger = SecurityLogger(
    backend="structured_json",
    output="/var/log/app/security.log",
    redact_fields=[
        LogField("password", replace="[REDACTED]"),
        LogField("token", replace="[REDACTED]"),
        LogField("api_key", replace="[REDACTED]"),
        LogField("ssn", pattern=r"\d{3}-\d{2}-\d{4}", replace="XXX-XX-[REDACTED]"),
        LogField("email", transform="mask"),  # alice@example.com -> a***@example.com
        LogField("ip", transform="hash"),  # Hash IPs for privacy
    ],
    include_request_id=True,
    include_timestamp=True,
    include_user_agent=True,
)

# Security event logging
def log_auth_event(event_type, user_id=None, success=True, details=None):
    logger.log(
        event_type=event_type,
        user_id=user_id,
        success=success,
        source_ip=request.remote_addr,
        user_agent=request.user_agent.string,
        request_id=request.id,
        details=details or {},
        severity="INFO" if success else "WARNING"
    )

# Usage
log_auth_event("login_attempt", user_id="user-123", success=True)
log_auth_event("login_attempt", user_id=None, success=False, 
               details={"reason": "invalid_password", "email": "attacker@evil.com"})
log_auth_event("password_change", user_id="user-123", success=True)
log_auth_event("mfa_bypass_attempt", user_id="user-123", success=False,
               details={"method": "recovery_code", "code_used": "XXXX-XXXX"})

# Audit trail for sensitive operations
audit = AuditTrail(
    storage="immutable_log",
    retention_days=2555,  # 7 years
    tamper_evident=True  # Hash chain for integrity
)

audit.record(
    action="data_export",
    actor="user-123",
    resource="/api/users/export",
    result="success",
    fields_exported=["name", "email", "phone"],
    record_count=1500,
    justification="Annual compliance audit",
    approver="security-team"
)
```

## Secure Configuration Management

### Secrets Detection in Code

```python
from secure_coding import SecretsDetector, SecretPattern

detector = SecretsDetector(
    patterns=[
        SecretPattern(name="AWS Access Key", regex=r"AKIA[0-9A-Z]{16}"),
        SecretPattern(name="AWS Secret Key", regex=r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}"),
        SecretPattern(name="GitHub Token", regex=r"ghp_[A-Za-z0-9]{36}"),
        SecretPattern(name="Stripe Key", regex=r"sk_live_[0-9a-zA-Z]{24,}"),
        SecretPattern(name="Private Key", regex=r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
        SecretPattern(name="Generic Secret", regex=r"(?i)(password|secret|api_key|apikey|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
        SecretPattern(name="Database URL", regex=r"(?i)(mysql|postgres|mongodb)://[^\s]+:[^\s]+@[^\s]+"),
    ],
    entropy_threshold=4.5  # Minimum Shannon entropy for high-entropy strings
)

# Scan codebase for secrets
results = detector.scan_directory(
    path="./src",
    exclude_patterns=["*.test.js", "*.spec.py", "node_modules/", "__pycache__/"],
    include_config_files=False  # Skip .env files (handled separately)
)

for secret in results.secrets:
    print(f"SECRET FOUND: {secret.pattern_name}")
    print(f"  File: {secret.file_path}:{secret.line_number}")
    print(f"  Severity: {secret.severity}")
    print(f"  Action: {secret.recommended_action}")
    print(f"  Redacted: {secret.redacted_preview}")
    print()

# Pre-commit hook integration
def pre_commit_secrets_check():
    """Run in CI/CD or pre-commit hook"""
    results = detector.scan_staged_files()
    if results.has_secrets:
        print(f"BLOCKED: {results.secrets_count} secrets found in staged files")
        for secret in results.secrets:
            print(f"  {secret.file_path}:{secret.line_number}: {secret.pattern_name}")
        return False
    return True
```

## Advanced Secure Coding Patterns

### Race Condition Prevention

```python
from secure_coding import AtomicOperation, DistributedLock

# Prevent race conditions in account balance operations
@AtomicOperation
def transfer_funds(from_account_id, to_account_id, amount):
    """Atomic transfer using database-level locking"""
    with db.session.begin():
        # SELECT FOR UPDATE prevents concurrent modification
        from_account = db.session.query(Account).with_for_update().filter(
            Account.id == from_account_id
        ).first()
        
        to_account = db.session.query(Account).with_for_update().filter(
            Account.id == to_account_id
        ).first()
        
        if from_account.balance < amount:
            raise InsufficientFundsError()
        
        from_account.balance -= amount
        to_account.balance += amount

# Distributed lock for cross-service operations
lock = DistributedLock(
    backend="redis",
    timeout_seconds=10,
    retry_count=3,
    retry_delay=0.1
)

@app.route("/api/coupons/redeem", methods=["POST"])
def redeem_coupon():
    coupon_code = request.json.get("coupon_code")
    user_id = request.current_user.id
    
    # Distributed lock prevents double-redemption
    with lock.acquire(f"coupon:{coupon_code}", owner=user_id):
        coupon = db.query(Coupon).filter(Coupon.code == coupon_code).first()
        if not coupon or coupon.used:
            return jsonify({"error": "Invalid coupon"}), 400
        
        coupon.used = True
        coupon.used_by = user_id
        coupon.used_at = datetime.utcnow()
        db.commit()
        
        return jsonify({"status": "redeemed", "discount": coupon.discount})
```

### Timing Attack Prevention

```python
import hmac
import hashlib
import secrets

def secure_compare(a: str, b: str) -> bool:
    """Constant-time string comparison to prevent timing attacks"""
    return hmac.compare_digest(a.encode(), b.encode())

def verify_token(provided_token: str, stored_token: str) -> bool:
    """Verify token with constant-time comparison"""
    return secure_compare(provided_token, stored_token)

def verify_hmac(message: str, provided_hmac: str, secret: bytes) -> bool:
    """Verify HMAC with constant-time comparison"""
    expected = hmac.new(secret, message.encode(), hashlib.sha256).hexdigest()
    return secure_compare(provided_hmac, expected)

# Password verification with constant-time comparison
def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password hash with constant-time comparison"""
    import argon2
    verifier = argon2.PasswordHasher()
    try:
        verifier.verify(stored_hash, password)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
    except argon2.exceptions.InvalidHashError:
        return False
```

### Secure File Operations

```python
from secure_coding import SecureFileOps
import tempfile
import os

file_ops = SecureFileOps()

# Secure temp file creation
def process_upload(file):
    # Create temp file with restrictive permissions
    with file_ops.secure_tempfile(suffix=".tmp") as tmp_path:
        file.save(tmp_path)
        
        # Process file
        result = process_file(tmp_path)
        
        # File is securely deleted when context exits
        # (overwrite before unlink)
    
    return result

# Secure file deletion
def delete_sensitive_file(path):
    """Securely delete file by overwriting before unlink"""
    file_ops.secure_delete(
        path=path,
        passes=3,  # Number of overwrite passes
        pattern="dod_5220_22_m"  # DoD 5220.22-M standard
    )

# Atomic file write (prevents partial writes on crash)
def save_config(config_data, config_path):
    """Atomically write config file"""
    file_ops.atomic_write(
        path=config_path,
        data=json.dumps(config_data, indent=2),
        backup=True,  # Keep backup of previous version
        mode=0o600,  # Owner read/write only
    )
```
