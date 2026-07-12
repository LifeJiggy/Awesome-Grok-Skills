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
