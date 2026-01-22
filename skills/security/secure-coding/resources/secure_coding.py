from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import re
import hashlib
import secrets


class VulnerabilityType(Enum):
    INJECTION = "injection"
    XSS = "cross_site_scripting"
    CSRF = "cross_site_request_forgery"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    CRYPTOGRAPHY = "cryptography"
    SENSITIVE_DATA = "sensitive_data"
    MISCONFIGURATION = "misconfiguration"
    INPUT_VALIDATION = "input_validation"
    ERROR_HANDLING = "error_handling"


class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityFinding:
    id: str
    type: VulnerabilityType
    severity: SecurityLevel
    file: str
    line: int
    function: str
    description: str
    remediation: str
    references: List[str]


class CodeAnalyzer:
    """Static application security testing"""
    
    def __init__(self):
        self.findings = []
    
    def analyze_code(self, code: str, language: str = "python") -> List[SecurityFinding]:
        """Analyze code for security vulnerabilities"""
        findings = []
        
        injection_patterns = [
            (r'exec\s*\(', 'Command Injection', SecurityLevel.CRITICAL),
            (r'eval\s*\(', 'Code Injection', SecurityLevel.CRITICAL),
            (r'os\.system\s*\(', 'Command Injection', SecurityLevel.HIGH),
            (r'subprocess.*shell\s*=\s*True', 'Shell Injection', SecurityLevel.HIGH),
            (r'format\s*\(.*%', 'Format String Vulnerability', SecurityLevel.MEDIUM),
        ]
        
        for pattern, vuln_type, severity in injection_patterns:
            if re.search(pattern, code):
                findings.append(SecurityFinding(
                    id=f"SC-{len(findings)+1:04d}",
                    type=VulnerabilityType.INJECTION,
                    severity=severity,
                    file="analyzed_code.py",
                    line=1,
                    function="main",
                    description=f"Potential {vuln_type} vulnerability detected",
                    remediation=f"Review use of pattern and implement safe alternatives",
                    references=["CWE-78", "OWASP-A03:2021"]
                ))
        
        crypto_patterns = [
            (r'md5', 'Weak Cryptographic Hash', SecurityLevel.HIGH),
            (r'sha1', 'Weak Cryptographic Hash', SecurityLevel.MEDIUM),
            (r'DES\.new', 'Weak Encryption Algorithm', SecurityLevel.HIGH),
            (r'Random\.new', 'Insecure Random Number Generator', SecurityLevel.MEDIUM),
        ]
        
        for pattern, vuln_type, severity in crypto_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                findings.append(SecurityFinding(
                    id=f"SC-{len(findings)+1:04d}",
                    type=VulnerabilityType.CRYPTOGRAPHY,
                    severity=severity,
                    file="analyzed_code.py",
                    line=1,
                    function="main",
                    description=f"{vuln_type} vulnerability detected",
                    remediation="Use SHA-256+ or bcrypt for hashing, AES-256 for encryption",
                    references=["CWE-327", "OWASP-A02:2021"]
                ))
        
        auth_patterns = [
            (r'password\s*=\s*[\'"].*[\'"]', 'Hardcoded Credential', SecurityLevel.CRITICAL),
            (r'api_key\s*=\s*[\'"].*[\'"]', 'Hardcoded API Key', SecurityLevel.CRITICAL),
            (r'secret_key\s*=\s*[\'"].*[\'"]', 'Hardcoded Secret', SecurityLevel.CRITICAL),
        ]
        
        for pattern, vuln_type, severity in auth_patterns:
            if re.search(pattern, code):
                findings.append(SecurityFinding(
                    id=f"SC-{len(findings)+1:04d}",
                    type=VulnerabilityType.SENSITIVE_DATA,
                    severity=severity,
                    file="analyzed_code.py",
                    line=1,
                    function="main",
                    description=f"Hardcoded {vuln_type} detected",
                    remediation="Use environment variables or secure secret management",
                    references=["CWE-259", "CWE-798"]
                ))
        
        return findings
    
    def analyze_python_security(self, code: str) -> List[SecurityFinding]:
        """Python-specific security analysis"""
        findings = []
        
        pickle_patterns = [
            (r'pickle\.load', 'Insecure Deserialization', SecurityLevel.CRITICAL),
            (r'cPickle\.load', 'Insecure Deserialization', SecurityLevel.CRITICAL),
        ]
        
        for pattern, desc, severity in pickle_patterns:
            if re.search(pattern, code):
                findings.append(SecurityFinding(
                    id=f"PY-{len(findings)+1:04d}",
                    type=VulnerabilityType.INJECTION,
                    severity=severity,
                    file="analyzed.py",
                    line=1,
                    function="main",
                    description=desc,
                    remediation="Use JSON instead of pickle, or validate input",
                    references=["CWE-502", "OWASP-A08:2021"]
                ))
        
        yaml_patterns = [
            (r'yaml\.load\s*\([^)]*\)', 'Unsafe YAML Parsing', SecurityLevel.HIGH),
        ]
        
        for pattern, desc, severity in yaml_patterns:
            if re.search(pattern, code):
                findings.append(SecurityFinding(
                    id=f"PY-{len(findings)+1:04d}",
                    type=VulnerabilityType.INJECTION,
                    severity=severity,
                    file="analyzed.py",
                    line=1,
                    function="main",
                    description=desc,
                    remediation="Use yaml.safe_load() instead",
                    references=["CWE-91"]
                ))
        
        return findings
    
    def analyze_javascript_security(self, code: str) -> List[SecurityFinding]:
        """JavaScript-specific security analysis"""
        findings = []
        
        xss_patterns = [
            (r'innerHTML\s*=', 'DOM XSS via innerHTML', SecurityLevel.HIGH),
            (r'document\.write', 'Potential XSS via document.write', SecurityLevel.MEDIUM),
            (r'eval\s*\(.*innerHTML', 'XSS via eval', SecurityLevel.CRITICAL),
        ]
        
        for pattern, desc, severity in xss_patterns:
            if re.search(pattern, code):
                findings.append(SecurityFinding(
                    id=f"JS-{len(findings)+1:04d}",
                    type=VulnerabilityType.XSS,
                    severity=severity,
                    file="analyzed.js",
                    line=1,
                    function="main",
                    description=desc,
                    remediation="Use textContent instead of innerHTML, sanitize input",
                    references=["CWE-79", "OWASP-A03:2021"]
                ))
        
        return findings


class SecureCodeGenerator:
    """Generate secure code patterns"""
    
    def generate_password_hash(self,
                               password: str,
                               algorithm: str = "bcrypt") -> Dict:
        """Generate secure password hash"""
        if algorithm == "bcrypt":
            import bcrypt
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode(), salt)
            return {
                'algorithm': 'bcrypt',
                'hash': hashed.decode(),
                'salt': salt.decode()[:29],
                'rounds': 12
            }
        elif algorithm == "argon2":
            return {
                'algorithm': 'argon2',
                'hash': 'argon2_hash_placeholder',
                'memory_cost': 65536,
                'time_cost': 3,
                'parallelism': 2
            }
        else:
            import hashlib
            salt = secrets.token_hex(16)
            hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return {
                'algorithm': 'pbkdf2_sha256',
                'hash': hashed.hex(),
                'salt': salt,
                'iterations': 100000
            }
    
    def generate_secure_token(self, length: int = 32) -> Dict:
        """Generate cryptographically secure token"""
        token = secrets.token_urlsafe(length)
        return {
            'token': token,
            'length': len(token),
            'entropy': length * 8,
            'algorithm': 'secrets.token_urlsafe'
        }
    
    def generate_sql_query(self,
                           table: str,
                           columns: List[str],
                           conditions: Dict[str, Any]) -> str:
        """Generate parameterized SQL query"""
        column_list = ', '.join(columns)
        condition_list = ' AND '.join(f"{k} = :{k}" for k in conditions.keys())
        query = f"SELECT {column_list} FROM {table} WHERE {condition_list}"
        return query
    
    def generate_csp_header(self,
                            sources: Dict[str, List[str]]) -> str:
        """Generate Content Security Policy header"""
        csp_parts = []
        for directive, source_list in sources.items():
            if source_list:
                csp_parts.append(f"{directive} {' '.join(source_list)}")
        return '; '.join(csp_parts)


class InputValidator:
    """Secure input validation utilities"""
    
    def __init__(self):
        self.validation_rules = {}
    
    def validate_email(self, email: str) -> Dict:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(pattern, email))
        return {
            'input': email,
            'valid': is_valid,
            'sanitized': email.lower().strip() if is_valid else None
        }
    
    def validate_filename(self, filename: str) -> Dict:
        """Validate filename for security"""
        dangerous_patterns = ['../', '..\\', '/etc/passwd', 'CON', 'PRN', 'AUX']
        has_dangerous = any(p in filename for p in dangerous_patterns)
        
        allowed_chars = re.compile(r'^[a-zA-Z0-9._-]+$')
        valid_chars = bool(allowed_chars.match(filename))
        
        sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        
        return {
            'input': filename,
            'valid': not has_dangerous and valid_chars,
            'sanitized': sanitized,
            'warnings': ['Contains dangerous path' if has_dangerous else None]
        }
    
    def validate_sql_input(self, user_input: str) -> Dict:
        """Detect potential SQL injection"""
        sql_patterns = [
            r"(\%27)|(\')|(--)|(\%23)|(#)",
            r"(\%3D)|(=)[^\n]*((\%27)|(\')|(--)|(\%3B)|(;))",
            r"\w*(\%27)|(\')|((\%6F)|(o)|(\%4F))((\%72)|(r)|(\%52))",
            r"((\%27)|(\')|)union",
            r"exec(\s|\+)+(s|x)p\w+",
        ]
        
        is_malicious = any(re.search(p, user_input, re.IGNORECASE) for p in sql_patterns)
        
        sanitized = user_input.replace("'", "''")
        
        return {
            'input': user_input,
            'is_malicious': is_malicious,
            'sanitized': sanitized,
            'recommendation': 'Use parameterized queries instead'
        }
    
    def sanitize_html(self, user_input: str) -> str:
        """Sanitize HTML to prevent XSS"""
        import html
        escaped = html.escape(user_input)
        return escaped
    
    def validate_numeric_range(self,
                               value: int,
                               min_val: int = 0,
                               max_val: int = 1000000) -> Dict:
        """Validate numeric input is within range"""
        is_valid = min_val <= value <= max_val
        return {
            'input': value,
            'valid': is_valid,
            'sanitized': max(min_val, min(value, max_val)) if is_valid else None
        }


class CryptographyManager:
    """Secure cryptographic operations"""
    
    def __init__(self):
        self.algorithms = {
            'hash': ['sha256', 'sha384', 'sha512', 'bcrypt', 'argon2'],
            'encryption': ['aes-256-gcm', 'chacha20-poly1305'],
            'signing': ['rsa-2048', 'ecdsa-p256', 'ed25519']
        }
    
    def hash_data(self,
                  data: str,
                  algorithm: str = "sha256") -> Dict:
        """Hash data using secure algorithm"""
        import hashlib
        if algorithm.startswith('sha'):
            hasher = hashlib.new(algorithm)
            hasher.update(data.encode())
            return {
                'algorithm': algorithm,
                'hash': hasher.hexdigest(),
                'length': len(hasher.hexdigest())
            }
        elif algorithm == 'bcrypt':
            import bcrypt
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(data.encode(), salt)
            return {
                'algorithm': 'bcrypt',
                'hash': hashed.decode(),
                'rounds': 12
            }
        return {}
    
    def encrypt_data(self,
                     plaintext: str,
                     key: str,
                     algorithm: str = "aes-256-gcm") -> Dict:
        """Encrypt data using secure algorithm"""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        import os
        
        if algorithm == "aes-256-gcm":
            key_bytes = key[:32].encode()[:32]
            aesgcm = AESGCM(key_bytes)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
            return {
                'algorithm': 'AES-256-GCM',
                'ciphertext': ciphertext.hex(),
                'nonce': nonce.hex(),
                'tag': ciphertext[-16:].hex()
            }
        return {}
    
    def decrypt_data(self,
                     ciphertext: str,
                     key: str,
                     nonce: str,
                     algorithm: str = "aes-256-gcm") -> Dict:
        """Decrypt data"""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        
        if algorithm == "aes-256-gcm":
            key_bytes = key[:32].encode()[:32]
            aesgcm = AESGCM(key_bytes)
            full_ct = bytes.fromhex(ciphertext)
            full_ct += bytes.fromhex(nonce) 
            plaintext = aesgcm.decrypt(bytes.fromhex(nonce), full_ct, None)
            return {
                'algorithm': 'AES-256-GCM',
                'plaintext': plaintext.decode()
            }
        return {}
    
    def generate_key(self,
                     algorithm: str = "aes-256-gcm") -> Dict:
        """Generate cryptographic key"""
        import os
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa, ec
        from cryptography.hazmat.backends import default_backend
        
        if algorithm == "aes-256-gcm":
            key = os.urandom(32)
            return {
                'algorithm': 'AES-256-GCM',
                'key': key.hex(),
                'key_length': 256
            }
        elif algorithm.startswith('rsa'):
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            return {
                'algorithm': 'RSA-2048',
                'private_key': private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8
                ).decode(),
                'key_size': 2048
            }
        return {}


class SecurityHeaderGenerator:
    """Generate security HTTP headers"""
    
    def generate_security_headers(self) -> Dict:
        """Generate comprehensive security headers"""
        return {
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-XSS-Protection': '1; mode=block',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
            'Cache-Control': 'no-store, no-cache, must-revalidate, private',
            'Pragma': 'no-cache'
        }
    
    def generate_cors_policy(self,
                            allowed_origins: List[str],
                            methods: List[str] = None,
                            headers: List[str] = None) -> Dict:
        """Generate CORS policy"""
        if methods is None:
            methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        if headers is None:
            headers = ['Content-Type', 'Authorization', 'X-Requested-With']
        
        return {
            'Access-Control-Allow-Origin': ', '.join(allowed_origins),
            'Access-Control-Allow-Methods': ', '.join(methods),
            'Access-Control-Allow-Headers': ', '.join(headers),
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '86400'
        }


if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    findings = analyzer.analyze_code("exec(user_input)")
    print(f"Findings: {len(findings)}")
    
    generator = SecureCodeGenerator()
    hashed = generator.generate_password_hash("mypassword", "bcrypt")
    print(f"Hash algorithm: {hashed['algorithm']}")
    
    validator = InputValidator()
    email = validator.validate_email("test@example.com")
    print(f"Email valid: {email['valid']}")
    
    crypto = CryptographyManager()
    key = crypto.generate_key("aes-256-gcm")
    print(f"Key generated: {key['key_length']} bits")
    
    headers = SecurityHeaderGenerator()
    security = headers.generate_security_headers()
    print(f"Security headers: {len(security)} defined")
