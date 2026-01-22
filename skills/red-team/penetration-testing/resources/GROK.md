# Penetration Testing Agent

## Overview

The **Penetration Testing Agent** provides comprehensive security assessment capabilities including network reconnaissance, vulnerability scanning, exploitation, and reporting. This agent helps identify security weaknesses before malicious actors can exploit them.

## Core Capabilities

### 1. Network Reconnaissance
Discover and map network infrastructure:
- **Port Scanning**: Identify open ports and services
- **Service Detection**: Version and technology fingerprinting
- **OS Detection**: Operating system identification
- **Subnet Discovery**: Host discovery across network ranges
- **DNS Enumeration**: Subdomain and record discovery
- **Network Mapping**: Visual topology creation

### 2. Web Application Testing
Identify web application vulnerabilities:
- **SQL Injection**: Detect and exploit SQL injection flaws
- **Cross-Site Scripting**: Reflected, stored, and DOM XSS
- **Directory Traversal**: Path traversal vulnerabilities
- **Security Header Analysis**: Missing security headers
- **Authentication Testing**: Weak authentication mechanisms
- **Session Management**: Cookie and session flaws

### 3. Exploitation
Validate vulnerabilities with controlled exploitation:
- **Reverse Shell Generation**: Various shell types and encodings
- **Payload Development**: Metasploit and custom payloads
- **Privilege Escalation**: Local exploit execution
- **Data Exfiltration**: Controlled data access demonstration
- **Lateral Movement**: Pivot to additional systems

### 4. Credential Attacks
Test password and authentication strength:
- **Dictionary Attacks**: Wordlist-based password testing
- **Brute Force**: Targeted credential guessing
- **Hash Cracking**: Password hash recovery
- **Credential stuffing**: Stolen credential testing
- **Default Password Check**: Common default credentials

### 5. Reporting
Generate comprehensive security reports:
- **Executive Summaries**: Management-focused overviews
- **Technical Findings**: Detailed vulnerability descriptions
- **Risk Ratings**: CVSS scoring and severity levels
- **Remediation Guidance**: Specific fix recommendations
- **Compliance Mapping**: Industry standard alignment

## Usage Examples

### Network Scanning

```python
from penetration_testing import NetworkScanner

scanner = NetworkScanner()
ports = scanner.port_scan("192.168.1.100", ports=[22, 80, 443, 8080])
print(f"Open ports: {[p['port'] for p in ports['open_ports']]}")

services = scanner.service_detection("192.168.1.100", port=80)
print(f"Service: {services['service']} {services['version']}")

hosts = scanner.subnet_discovery("192.168.1.0/24")
print(f"Live hosts: {hosts['live_count']}")
```

### Web Vulnerability Scanning

```python
from penetration_testing import WebVulnerabilityScanner

scanner = WebVulnerabilityScanner()
sqli = scanner.scan_sql_injection(
    "http://example.com/product?id=1"
)
print(f"SQL Injection found: {sqli['vulnerable']}")

xss = scanner.scan_xss("http://example.com/search")
print(f"XSS vulnerabilities: {len(xss['vulnerabilities'])}")

headers = scanner.scan_security_headers("https://example.com")
for finding in headers['findings']:
    print(f"{finding['header']}: {finding['status']}")
```

### Exploitation

```python
from penetration_testing import ExploitationFramework

exploit = ExploitationFramework()
shell = exploit.generate_reverse_shell(
    target_ip="10.10.10.5",
    target_port=4444,
    shell_type="bash"
)
print(f"Payload: {shell['payload']}")

msf = exploit.generate_msf_payload(
    payload_type="reverse_tcp",
    format_type="python"
)
print(f"MSF payload generated: {msf['payload_type']}")
```

### Credential Attacks

```python
from penetration_testing import CredentialAttacker

attacker = CredentialAttacker()
ssh = attacker.brute_force_ssh(
    target="192.168.1.100",
    username="admin"
)
print(f"SSH attack completed: {ssh['password_found']}")

crack = attacker.hash_cracking(
    hash_type="MD5",
    hash_value="5d41402abc4b2a76b9719d911017c592"
)
print(f"Cracked password: {crack['plaintext']}")
```

### Report Generation

```python
from penetration_testing import ReportGenerator, Severity, Vulnerability

report_gen = ReportGenerator()
summary = report_gen.create_executive_summary(
    target="192.168.1.100",
    scope=["192.168.1.0/24"],
    findings=[]
)
print(summary)
```

## Penetration Testing Methodology

```
┌─────────────────────────────────────────────────────────┐
│              Penetration Testing Phases                  │
├─────────────────────────────────────────────────────────┤
│  1. Reconnaissance → 2. Scanning → 3. Exploitation     │
│         │                  │              │              │
│  6. Reporting ← 5. Persist ← 4. Privilege Escalation   │
│         │                  │              │              │
│         └────────────── 7. Cleanup ─────────────────────┘
└─────────────────────────────────────────────────────────┘
```

## Testing Frameworks

### OWASP Testing Guide

| Category | Tests | Risk Level |
|----------|-------|------------|
| Information Gathering | 8 tests | Info |
| Configuration Testing | 8 tests | Medium |
| Identity Management | 7 tests | High |
| Authentication | 12 tests | Critical |
| Authorization | 10 tests | High |
| Session Management | 12 tests | High |
| Input Validation | 18 tests | Critical |
| Error Handling | 5 tests | Medium |
| Cryptography | 7 tests | Medium |

### PTES Phases

1. **Pre-Engagement Interactions**: Scoping and rules
2. **Intelligence Gathering**: Passive and active recon
3. **Threat Modeling**: Identify attack vectors
4. **Vulnerability Analysis**: Discover weaknesses
5. **Exploitation**: Validate vulnerabilities
6. **Post-Exploitation**: Maintain access
7. **Reporting**: Document findings

## Common Vulnerabilities

### OWASP Top 10 (2021)

| Rank | Vulnerability | Description |
|------|---------------|-------------|
| 1 | Broken Access Control | Authorization bypass |
| 2 | Cryptographic Failures | Weak encryption |
| 3 | Injection | SQL, Command, LDAP injection |
| 4 | Insecure Design | Missing controls |
| 5 | Security Misconfiguration | Default configs |
| 6 | Vulnerable Components | Outdated libraries |
| 7 | Authentication Failures | Weak passwords |
| 8 | Data Integrity Failures | Unvalidated data |
| 9 | Logging Failures | Missing monitoring |
| 10 | SSRF | Server-side request forgery |

## Tools and Frameworks

### Reconnaissance Tools

| Tool | Purpose | Example |
|------|---------|---------|
| Nmap | Port scanning | `nmap -sV -sC target` |
| Masscan | Fast scanning | `masscan -p0-65535 target` |
| Netcat | Banner grabbing | `nc -v target 22` |
| DNSRecon | DNS enumeration | `dnsrecon -d domain.com` |
| theHarvester | OSINT gathering | `theHarvester -d domain.com` |

### Exploitation Tools

| Tool | Purpose | Example |
|------|---------|---------|
| Metasploit | Exploitation framework | `msfconsole` |
| Burp Suite | Web testing | Intercept and modify |
| SQLMap | SQL injection | `sqlmap -u url` |
| John the Ripper | Password cracking | `john hash.txt` |
|Responder| LLMNR poisoning | `responder -I eth0` |

## Legal and Ethical Considerations

### Rules of Engagement

1. **Defined Scope**: Clearly document what's in scope
2. **Time Windows**: Specify testing hours
3. **Data Handling**: How to handle sensitive data
4. **Incident Response**: What to do if critical issues found
5. **Communication**: Regular status updates

### Responsible Disclosure

1. **Document Everything**: Record all findings
2. **Report Immediately**: Notify of critical issues
3. **Allow Remediation**: Give time to fix
4. **Coordinated Release**: Public disclosure timing
5. **Helpful Attitude**: Work with vendor to fix

## Best Practices

1. **Get Written Authorization**: Always have documented permission
2. **Define Scope Clearly**: Know what's authorized
3. **Minimize Impact**: Use least intrusive methods first
4. **Preserve Evidence**: Document for reporting
5. **Communicate Proactively**: Keep stakeholders informed
6. **Follow Up**: Verify fixes were implemented

## Related Skills

- [Vulnerability Assessment](./../vulnerability-assessment/resources/GROK.md) - Automated scanning
- [Blue Team Security](./../blue-team/security-monitoring/resources/GROK.md) - Defensive operations
- [Threat Modeling](./../threat-modeling/resources/GROK.md) - Proactive assessment
- [Secure Coding](./../secure-coding/resources/GROK.md) - Prevention through development

---

**File Path**: `skills/red-team/penetration-testing/resources/penetration_testing.py`
