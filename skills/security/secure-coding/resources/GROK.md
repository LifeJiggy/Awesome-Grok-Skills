# Secure Coding Agent

## Overview

The **Secure Coding Agent** provides comprehensive tools for writing secure code, including static analysis, secure pattern generation, input validation, and cryptographic operations. This agent helps developers write code that is resilient to security vulnerabilities from the start.

## Core Capabilities

### 1. Static Analysis
Analyze code for security vulnerabilities:
- **Pattern Detection**: Find dangerous patterns
- **Language Support**: Python, JavaScript, Java, etc.
- **Vulnerability Classification**: Categorize by type and severity
- **Remediation Guidance**: Suggest fixes
- **CI/CD Integration**: Automated scanning

### 2. Secure Pattern Generation
Generate secure code patterns:
- **Password Handling**: Secure hashing with bcrypt/argon2
- **Token Generation**: Cryptographically secure tokens
- **SQL Queries**: Parameterized query builders
- **Security Headers**: HTTP security headers
- **Authentication**: Secure session management

### 3. Input Validation
Validate and sanitize user input:
- **Email Validation**: Format and sanitization
- **Filename Validation**: Path traversal prevention
- **SQL Injection Detection**: Malicious pattern detection
- **HTML Sanitization**: XSS prevention
- **Numeric Range Validation**: Bounds checking

### 4. Cryptography
Secure cryptographic operations:
- **Hashing**: SHA-256, bcrypt, argon2
- **Encryption**: AES-256-GCM, ChaCha20
- **Key Generation**: Secure random keys
- **Digital Signatures**: RSA, ECDSA, Ed25519
- **Token Generation**: Secure random tokens

### 5. Security Headers
Generate HTTP security headers:
- **HSTS**: Force HTTPS connections
- **CSP**: Content Security Policy
- **X-Frame-Options**: Clickjacking protection
- **X-Content-Type**: MIME type sniffing prevention
- **CORS**: Cross-origin resource sharing

## Usage Examples

### Code Analysis

```python
from secure_coding import CodeAnalyzer

analyzer = CodeAnalyzer()
code = "exec(user_input)"
findings = analyzer.analyze_code(code)
for finding in findings:
    print(f"{finding.severity.value}: {finding.description}")
    print(f"  Remediation: {finding.remediation}")
```

### Password Hashing

```python
from secure_coding import SecureCodeGenerator

generator = SecureCodeGenerator()
hashed = generator.generate_password_hash("mypassword", algorithm="bcrypt")
print(f"Algorithm: {hashed['algorithm']}")
print(f"Hash length: {len(hashed['hash'])}")

token = generator.generate_secure_token(32)
print(f"Secure token: {token['token'][:20]}...")
```

### Input Validation

```python
from secure_coding import InputValidator

validator = InputValidator()

email = validator.validate_email("user@example.com")
print(f"Email valid: {email['valid']}")

filename = validator.validate_filename("../../../etc/passwd")
print(f"Filename valid: {filename['valid']}")
print(f"Sanitized: {filename['sanitized']}")

sql = validator.validate_sql_input("' OR 1=1--")
print(f"SQL injection: {sql['is_malicious']}")
```

### Cryptography

```python
from secure_coding import CryptographyManager

crypto = CryptographyManager()

hashed = crypto.hash_data("sensitive data", algorithm="sha256")
print(f"SHA-256: {hashed['hash'][:20]}...")

key = crypto.generate_key("aes-256-gcm")
print(f"Key length: {key['key_length']} bits")

encrypted = crypto.encrypt_data("secret message", key['key'])
print(f"Encrypted (first 20 chars): {encrypted['ciphertext'][:20]}...")
```

### Security Headers

```python
from secure_coding import SecurityHeaderGenerator

headers = SecurityHeaderGenerator()

security = headers.generate_security_headers()
for name, value in security.items():
    print(f"{name}: {value[:50]}...")

cors = headers.generate_cors_policy(
    allowed_origins=["https://example.com"],
    methods=["GET", "POST"]
)
print(f"CORS Origin: {cors['Access-Control-Allow-Origin']}")
```

## Secure Coding Principles

### OWASP Top 10 (2021)

| Rank | Vulnerability | Prevention |
|------|---------------|------------|
| A01:2021 | Broken Access Control | Implement proper authorization |
| A02:2021 | Cryptographic Failures | Use strong cryptography |
| A03:2021 | Injection | Input validation, parameterized queries |
| A04:2021 | Insecure Design | Security by design |
| A05:2021 | Security Misconfiguration | Hardened configurations |
| A06:2021 | Vulnerable Components | Keep dependencies updated |
| A07:2021 | Authentication Failures | Strong authentication |
| A08:2021 | Data Integrity Failures | Digital signatures, checksums |
| A09:2021 | Logging Failures | Comprehensive logging |
| A10:2021 | SSRF | Network segmentation |

### Secure Development Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│              Secure Development Lifecycle                │
├─────────────────────────────────────────────────────────┤
│  1. Design → 2. Develop → 3. Test → 4. Deploy → 5. Maintain
│       │           │           │            │            │
│  Threat      Secure      SAST/DAST   Hardening    Patching
│  Modeling    Guidelines  Testing     Configuration Updates
└─────────────────────────────────────────────────────────┘
```

## Language-Specific Guidance

### Python Security

| Issue | CWE | Safe Alternative |
|-------|-----|------------------|
| pickle.load | CWE-502 | json.loads() |
| eval() | CWE-78 | ast.literal_eval() |
| exec() | CWE-78 | subprocess with list |
| YAML load | CWE-91 | yaml.safe_load() |
| MD5 | CWE-328 | hashlib.sha256() |

### JavaScript Security

| Issue | CWE | Safe Alternative |
|-------|-----|------------------|
| innerHTML | CWE-79 | textContent |
| eval() | CWE-78 | JSON.parse() |
| Buffer() | CWE-787 | Buffer.from() |
| crypto.random() | CWE-338 | crypto.randomBytes() |

### Common Vulnerabilities

#### SQL Injection

```python
# UNSAFE
query = "SELECT * FROM users WHERE id = " + user_id

# SAFE - Parameterized query
query = "SELECT * FROM users WHERE id = :id"
params = {'id': user_id}
```

#### Cross-Site Scripting (XSS)

```python
# UNSAFE
element.innerHTML = user_input

# SAFE - Sanitize and escape
element.textContent = user_input

# Or use a sanitizer library
from django.utils.html import escape
safe_html = escape(user_input)
```

#### Insecure Deserialization

```python
# UNSAFE
import pickle
data = pickle.loads(untrusted_data)

# SAFE
import json
data = json.loads(untrusted_data)
```

## Cryptography Best Practices

### Password Storage

| Algorithm | Recommended | Reason |
|-----------|-------------|--------|
| bcrypt | YES | Adaptive cost, widely supported |
| argon2 | YES | Winner of Password Hashing Competition |
| scrypt | YES | Memory-hard function |
| PBKDF2 | OK | Lower computational cost |
| MD5 | NO | Too fast, no salt |
| SHA-256 | NO | Not designed for passwords |

### Encryption

| Algorithm | Status | Use Case |
|-----------|--------|----------|
| AES-256-GCM | RECOMMENDED | Symmetric encryption |
| ChaCha20-Poly1305 | RECOMMENDED | Mobile, low-power |
| RSA-2048+ | RECOMMENDED | Asymmetric encryption |
| ECDSA-P256 | RECOMMENDED | Digital signatures |
| 3DES | DEPRECATED | Legacy only |
| RC4 | BANNED | Insecure |

### Key Management

1. **Never hardcode keys**: Use environment variables or secrets manager
2. **Use key rotation**: Regularly rotate encryption keys
3. **Separate keys**: Different keys for different purposes
4. **Secure storage**: Use HSM or secure vault
5. **Key derivation**: Derive keys from master key

## Input Validation Strategies

### Whitelist Validation

```python
def validate_action(action):
    allowed = ['create', 'read', 'update', 'delete']
    if action not in allowed:
        raise ValueError(f"Invalid action: {action}")
    return action
```

### Sanitization

```python
import re

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

def sanitize_sql(input):
    return input.replace("'", "''")
```

### Type Checking

```python
def process_id(user_id: int) -> int:
    if not isinstance(user_id, int):
        raise TypeError("user_id must be an integer")
    if user_id < 1 or user_id > 1000000:
        raise ValueError("user_id out of range")
    return user_id
```

## Security Headers Reference

| Header | Purpose | Example Value |
|--------|---------|---------------|
| HSTS | Force HTTPS | `max-age=31536000; includeSubDomains` |
| CSP | Content restrictions | `default-src 'self'` |
| X-Frame-Options | Clickjacking | `SAMEORIGIN` |
| X-Content-Type | MIME sniffing | `nosniff` |
| Referrer-Policy | Referrer info | `strict-origin-when-cross-origin` |
| Permissions-Policy | Feature access | `geolocation=()` |

## Security Tools Integration

### SAST Tools

| Tool | Language | Best For |
|------|----------|----------|
| Bandit | Python | Quick Python scans |
| Semgrep | Multi | Custom rules |
| SonarQube | Multi | Comprehensive analysis |
| Checkmarx | Multi | Enterprise scanning |

### Dependency Scanning

| Tool | Purpose |
|------|---------|
| Snyk | Dependency vulnerabilities |
| npm audit | Node.js packages |
| pip-audit | Python packages |
| Dependabot | Automated updates |

## Secure Coding Checklist

### Development Phase

- [ ] Use parameterized queries
- [ ] Validate all input
- [ ] Encode output for context
- [ ] Use cryptographic hashing for passwords
- [ ] Implement proper authentication
- [ ] Use HTTPS everywhere
- [ ] Keep dependencies updated
- [ ] Follow principle of least privilege

### Code Review Checklist

- [ ] No hardcoded credentials
- [ ] No use of dangerous functions (eval, exec)
- [ ] No insecure deserialization
- [ ] Proper error handling (no stack traces)
- [ ] Secure cryptographic implementations
- [ ] Proper access controls
- [ ] Sensitive data encrypted at rest
- [ ] Logging of security events

### Deployment Checklist

- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Debug mode disabled
- [ ] Error messages sanitized
- [ ] HTTPS enforced
- [ ] Security monitoring enabled
- [ ] Backup and recovery tested

## Best Practices

1. **Shift Left**: Address security early in development
2. **Defense in Depth**: Multiple security layers
3. **Least Privilege**: Minimum necessary permissions
4. **Fail Secure**: Default to secure behavior
5. **Keep it Simple**: Complex code has more vulnerabilities
6. **Defense in Depth**: Don't rely on single controls
7. **Use Established Libraries**: Don't roll your own crypto

## Related Skills

- [Vulnerability Assessment](./../security-assessment/vulnerability-assessment/resources/GROK.md) - Finding vulnerabilities
- [Penetration Testing](./../red-team/penetration-testing/resources/GROK.md) - Testing security
- [Threat Modeling](./../threat-modeling/resources/GROK.md) - Proactive security design
- [Security Monitoring](./../blue-team/security-monitoring/resources/GROK.md) - Detecting issues

---

**File Path**: `skills/security/secure-coding/resources/secure_coding.py`
