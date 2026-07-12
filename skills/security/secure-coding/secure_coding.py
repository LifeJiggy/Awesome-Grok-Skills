"""
Secure Coding Framework
=======================

Provides input validation, parameterized query building, password hashing,
CSP generation, and common secure coding utilities. Designed to prevent OWASP
Top 10 vulnerability classes at the source-code level.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import secrets
import string
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EncodingContext(Enum):
    HTML = "html"
    JAVASCRIPT = "javascript"
    URL = "url"
    CSS = "css"
    SQL = "sql"
    XML = "xml"
    JSON = "json"


class ValidationStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    PARTIAL = "partial"


class PasswordAlgorithm(Enum):
    ARGON2ID = "argon2id"
    BCRYPT = "bcrypt"
    PBKDF2 = "pbkdf2_sha256"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ValidationRule:
    """Single field validation rule."""
    field: str
    type: type = str
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    pattern: Optional[str] = None
    nullable: bool = False
    allowed_values: Optional[list[Any]] = None
    custom_validator: Optional[Callable[[Any], bool]] = None


@dataclass
class ValidationResult:
    """Result of input validation."""
    status: ValidationStatus
    sanitized_data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.status == ValidationStatus.VALID


@dataclass
class HashResult:
    """Result of a password hashing operation."""
    hash: str
    algorithm: str
    salt: str
    iterations: int = 0
    memory_cost: int = 0


@dataclass
class CSPDirective:
    """A single Content Security Policy directive."""
    name: str
    sources: list[str] = field(default_factory=list)


@dataclass
class SQLQuery:
    """Parameterized SQL query representation."""
    template: str
    params: list[Any] = field(default_factory=list)
    param_style: str = "placeholder"


# ---------------------------------------------------------------------------
# Input Validation
# ---------------------------------------------------------------------------

class InputValidator:
    """Validates and sanitizes untrusted input against a set of rules."""

    def __init__(self, rules: list[ValidationRule]) -> None:
        self._rules = {r.field: r for r in rules}
        self._compiled_patterns: dict[str, re.Pattern[str]] = {}
        for rule in rules:
            if rule.pattern:
                self._compiled_patterns[rule.field] = re.compile(rule.pattern)

    def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Validate input data against all configured rules."""
        errors: list[str] = []
        sanitized: dict[str, Any] = {}

        for field_name, rule in self._rules.items():
            value = data.get(field_name)

            # Handle missing / nullable
            if value is None:
                if rule.nullable:
                    sanitized[field_name] = None
                    continue
                errors.append(f"Field '{field_name}' is required")
                continue

            # Type check
            if not isinstance(value, rule.type):
                errors.append(
                    f"Field '{field_name}' must be of type {rule.type.__name__}, "
                    f"got {type(value).__name__}"
                )
                continue

            # String constraints
            if rule.type is str:
                value = self._sanitize_string(value, rule, errors)
                if field_name in self._compiled_patterns:
                    if not self._compiled_patterns[field_name].match(value):
                        errors.append(f"Field '{field_name}' does not match pattern")
                        continue

            # Numeric constraints
            if rule.type in (int, float):
                if rule.min_value is not None and value < rule.min_value:
                    errors.append(
                        f"Field '{field_name}' must be >= {rule.min_value}"
                    )
                    continue
                if rule.max_value is not None and value > rule.max_value:
                    errors.append(
                        f"Field '{field_name}' must be <= {rule.max_value}"
                    )
                    continue

            # Allowed values
            if rule.allowed_values and value not in rule.allowed_values:
                errors.append(
                    f"Field '{field_name}' must be one of {rule.allowed_values}"
                )
                continue

            # Custom validator
            if rule.custom_validator and not rule.custom_validator(value):
                errors.append(f"Field '{field_name}' failed custom validation")
                continue

            sanitized[field_name] = value

        status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        return ValidationResult(status=status, sanitized_data=sanitized, errors=errors)

    def _sanitize_string(self, value: str, rule: ValidationRule,
                         errors: list[str]) -> str:
        value = value.strip()
        if rule.min_length is not None and len(value) < rule.min_length:
            errors.append(
                f"Field '{rule.field}' must have length >= {rule.min_length}"
            )
        if rule.max_length is not None and len(value) > rule.max_length:
            value = value[:rule.max_length]
            # Don't error — truncate silently or add warning
        # Strip null bytes and control characters
        value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", value)
        return value


# ---------------------------------------------------------------------------
# Output Encoding
# ---------------------------------------------------------------------------

class OutputEncoder:
    """Context-aware output encoding to prevent injection."""

    _HTML_ESCAPE = str.maketrans({
        "&": "&amp;", "<": "&lt;", ">": "&gt;",
        '"': "&quot;", "'": "&#x27;", "/": "&#x2F;",
    })

    @staticmethod
    def encode(value: str, context: EncodingContext) -> str:
        match context:
            case EncodingContext.HTML:
                return value.translate(OutputEncoder._HTML_ESCAPE)
            case EncodingContext.JAVASCRIPT:
                return value.replace("\\", "\\\\").replace("'", "\\'") \
                    .replace('"', '\\"').replace("\n", "\\n") \
                    .replace("\r", "\\r").replace("<", "\\x3c") \
                    .replace(">", "\\x3e")
            case EncodingContext.URL:
                import urllib.parse
                return urllib.parse.quote(value, safe="")
            case EncodingContext.CSS:
                return re.sub(r"[^a-zA-Z0-9_-]", "", value)
            case EncodingContext.XML:
                return value.replace("&", "&amp;").replace("<", "&lt;") \
                    .replace(">", "&gt;").replace('"', "&quot;")
            case EncodingContext.JSON:
                import json
                return json.dumps(value)
            case _:
                return value


# ---------------------------------------------------------------------------
# Parameterized Queries
# ---------------------------------------------------------------------------

class SecureQueryBuilder:
    """Builds parameterized SQL queries to prevent injection."""

    def __init__(self, connection: Any = None) -> None:
        self._connection = connection
        self._query_log: list[SQLQuery] = []

    def build(self, template: str, params: list[Any]) -> SQLQuery:
        """Build a parameterized query (does not execute)."""
        query = SQLQuery(template=template, params=params)
        self._query_log.append(query)
        return query

    def execute(self, template: str, params: list[Any]) -> Any:
        """Build and execute a parameterized query."""
        query = self.build(template, params)
        if self._connection is None:
            return {"status": "simulated", "query": query.template,
                    "params_count": len(query.params)}
        cursor = self._connection.cursor()
        cursor.execute(query.template, query.params)
        return cursor.fetchall()

    def get_query_log(self) -> list[SQLQuery]:
        return list(self._query_log)


# ---------------------------------------------------------------------------
# Password Hashing
# ---------------------------------------------------------------------------

class PasswordManager:
    """Secure password hashing and verification."""

    def __init__(self, algorithm: PasswordAlgorithm | str = PasswordAlgorithm.BCRYPT,
                 iterations: int = 100_000) -> None:
        if isinstance(algorithm, str):
            algorithm = PasswordAlgorithm(algorithm)
        self.algorithm = algorithm
        self.iterations = iterations

    def hash(self, password: str) -> HashResult:
        """Hash a password with the configured algorithm."""
        salt = secrets.token_hex(16)
        if self.algorithm == PasswordAlgorithm.PBKDF2:
            dk = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt.encode(), self.iterations
            )
            return HashResult(
                hash=dk.hex(), algorithm="pbkdf2_sha256",
                salt=salt, iterations=self.iterations
            )
        # Simple HMAC-based hash for demo (real usage: argon2-cffi / bcrypt lib)
        dk = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), self.iterations
        )
        return HashResult(
            hash=dk.hex(), algorithm=self.algorithm.value,
            salt=salt, iterations=self.iterations
        )

    def verify(self, password: str, stored: HashResult) -> bool:
        """Verify a password against a stored hash."""
        recomputed = self.hash(password)
        return hmac.compare_digest(recomputed.hash, stored.hash)

    def needs_rehash(self, stored: HashResult, min_iterations: int = 100_000) -> bool:
        """Check if a stored hash should be rehashed."""
        if stored.iterations < min_iterations:
            return True
        if stored.algorithm != self.algorithm.value:
            return True
        return False


# ---------------------------------------------------------------------------
# CSP Builder
# ---------------------------------------------------------------------------

class CSPBuilder:
    """Build Content Security Policy headers."""

    def __init__(self) -> None:
        self._directives: dict[str, list[str]] = {}

    def add_directive(self, name: str, sources: list[str]) -> None:
        if name in self._directives:
            self._directives[name].extend(sources)
        else:
            self._directives[name] = list(sources)

    def build(self) -> str:
        parts = []
        for name, sources in self._directives.items():
            parts.append(f"{name} {' '.join(sources)}")
        return "; ".join(parts)

    def build_report_only(self) -> tuple[str, str]:
        """Return (header-name, header-value) for CSP-Report-Only."""
        return ("Content-Security-Policy-Report-Only", self.build())


# ---------------------------------------------------------------------------
# Security Scanner (lightweight)
# ---------------------------------------------------------------------------

class SecurityLinter:
    """Lightweight static analysis for common Python security issues."""

    _PATTERNS: list[tuple[str, str, Severity]] = [
        (r"eval\(", "Use of eval() detected", Severity.HIGH),
        (r"exec\(", "Use of exec() detected", Severity.CRITICAL),
        (r"__import__\(", "Dynamic import detected", Severity.MEDIUM),
        (r"subprocess\.call\(.*shell\s*=\s*True", "Shell injection risk", Severity.CRITICAL),
        (r"os\.system\(", "os.system() is unsafe", Severity.CRITICAL),
        (r"pickle\.load", "Insecure deserialization via pickle", Severity.HIGH),
        (r"yaml\.load\(", "Use yaml.safe_load() instead", Severity.HIGH),
        (r"md5\(", "Use SHA-256+ instead of MD5", Severity.MEDIUM),
        (r"random\.", "Use secrets module for crypto operations", Severity.MEDIUM),
    ]

    def scan_file(self, filepath: str) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for lineno, line in enumerate(f, start=1):
                    for pattern, message, severity in self._PATTERNS:
                        if re.search(pattern, line):
                            findings.append({
                                "file": filepath,
                                "line": lineno,
                                "message": message,
                                "severity": severity.value,
                                "code": line.strip(),
                            })
        except FileNotFoundError:
            findings.append({
                "file": filepath,
                "line": 0,
                "message": "File not found",
                "severity": "info",
            })
        return findings


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate all secure coding utilities."""
    print("=" * 60)
    print("  Secure Coding Framework Demo")
    print("=" * 60)

    # --- Input Validation ---
    print("\n--- Input Validation ---")
    rules = [
        ValidationRule(field="username", type=str, min_length=3, max_length=32,
                       pattern=r"^[a-zA-Z0-9_-]+$"),
        ValidationRule(field="email", type=str,
                       pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
        ValidationRule(field="age", type=int, min_value=0, max_value=150),
        ValidationRule(field="bio", type=str, max_length=200, nullable=True),
    ]
    validator = InputValidator(rules)

    good = validator.validate({
        "username": "alice_42", "email": "alice@example.com",
        "age": 28, "bio": "Researcher"
    })
    print(f"  Valid input:   is_valid={good.is_valid}, errors={good.errors}")

    bad = validator.validate({
        "username": "x", "email": "not-an-email",
        "age": 200, "bio": "x" * 300
    })
    print(f"  Invalid input: is_valid={bad.is_valid}, errors={bad.errors}")

    # --- Output Encoding ---
    print("\n--- Output Encoding ---")
    payload = '<script>alert("xss")</script>'
    for ctx in EncodingContext:
        encoded = OutputEncoder.encode(payload, ctx)
        print(f"  {ctx.value:12s}: {encoded[:60]}")

    # --- Parameterized Queries ---
    print("\n--- Parameterized Queries ---")
    qbuilder = SecureQueryBuilder()
    q = qbuilder.build("SELECT * FROM users WHERE id = %s AND active = %s",
                        params=[42, True])
    print(f"  Template: {q.template}")
    print(f"  Params:   {q.params}")
    result = qbuilder.execute("SELECT * FROM users WHERE id = %s", params=[42])
    print(f"  Execute:  {result}")

    # --- Password Hashing ---
    print("\n--- Password Hashing ---")
    pwd_mgr = PasswordManager(PasswordAlgorithm.BCRYPT, iterations=100_000)
    hashed = pwd_mgr.hash("my_secret_password")
    print(f"  Hash:     {hashed.hash[:40]}...")
    print(f"  Algo:     {hashed.algorithm}")
    valid = pwd_mgr.verify("my_secret_password", hashed)
    print(f"  Verify:   {valid}")
    print(f"  Rehash:   {pwd_mgr.needs_rehash(hashed)}")

    # --- CSP Builder ---
    print("\n--- CSP Builder ---")
    csp = CSPBuilder()
    csp.add_directive("default-src", ["'self'"])
    csp.add_directive("script-src", ["'self'", "cdn.example.com"])
    csp.add_directive("style-src", ["'self'", "'unsafe-inline'"])
    csp.add_directive("img-src", ["'self'", "data:", "https:"])
    csp.add_directive("frame-ancestors", ["'none'"])
    print(f"  Header: {csp.build()}")

    # --- Security Linter ---
    print("\n--- Security Linter ---")
    linter = SecurityLinter()
    findings = linter.scan_file(__file__)
    print(f"  Self-scan findings: {len(findings)}")
    for f in findings[:3]:
        print(f"    L{f['line']:3d}: [{f['severity']}] {f['message']}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
