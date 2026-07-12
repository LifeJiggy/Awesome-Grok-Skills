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
