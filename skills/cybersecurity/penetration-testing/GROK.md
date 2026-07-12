---
name: "penetration-testing"
category: "cybersecurity"
version: "2.0.0"
tags: ["cybersecurity", "pentesting", "red-team", "exploitation", "vulnerability"]
---

# Penetration Testing

## Overview

The Penetration Testing module provides structured methodologies and tools for authorized security testing of systems, networks, and applications. It covers reconnaissance, vulnerability scanning, exploitation, privilege escalation, lateral movement, and reporting following industry-standard frameworks (OWASP, PTES, NIST).

This skill is essential for penetration testers, red team operators, and security consultants conducting authorized security assessments.

## Core Capabilities

- **Reconnaissance**: Passive and active information gathering, OSINT, and attack surface mapping
- **Scanning**: Port scanning, service enumeration, vulnerability scanning, and technology fingerprinting
- **Exploitation**: Vulnerability exploitation, proof-of-concept development, and exploit chaining
- **Privilege Escalation**: Linux/Windows privilege escalation techniques and misconfigurations
- **Lateral Movement**: Network pivoting, credential reuse, and active directory attacks
- **Post-Exploitation**: Data exfiltration, persistence mechanisms, and evidence collection
- **Web Application Testing**: OWASP Top 10 testing, API security, and authentication bypass
- **Reporting**: Finding documentation, risk ratings, and remediation recommendations

## Usage Examples

```python
from penetration_testing import (
    ReconEngine,
    VulnScanner,
    ExploitFramework,
    PrivEscDetector,
    ReportGenerator,
)

# --- Reconnaissance ---
recon = ReconEngine()
results = recon.passive_recon(target="example.com")
print(f"Subdomains found: {len(results.subdomains)}")
print(f"IP addresses: {results.ip_addresses}")
print(f"Email addresses: {len(results.emails)}")

# --- Scanning ---
scanner = VulnScanner()
scan_results = scanner.scan(
    target="192.168.1.0/24",
    scan_type="service",
    ports="1-65535",
)
print(f"Hosts up: {scan_results.hosts_up}")
print(f"Open ports: {len(scan_results.open_ports)}")
print(f"Vulnerabilities: {len(scan_results.vulnerabilities)}")

# --- Exploitation ---
exploit = ExploitFramework()
result = exploit.run_exploit(
    target="192.168.1.10",
    exploit="ms17_010",
    payload="reverse_shell",
    lhost="192.168.1.5",
    lport=4444,
)
print(f"Exploit success: {result.success}")
print(f"Shell obtained: {result.shell_type}")

# --- Privilege Escalation ---
privesc = PrivEscDetector()
vulns = privesc.check_linux(
    os_info="Ubuntu 20.04",
    kernel_version="5.4.0-42",
    suid_binaries=["/usr/bin/find", "/usr/bin/vim"],
    sudo_permissions="ALL",
)
for v in vulns:
    print(f"  [{v.severity}] {v.technique}")

# --- Report ---
reporter = ReportGenerator()
report = reporter.generate(
    findings=vulns,
    scope="192.168.1.0/24",
    methodology="OWASP Testing Guide",
    executive_summary="Critical vulnerabilities found in web application",
)
print(f"Report: {report.title}")
print(f"Findings: {report.total_findings}")
```

## Best Practices

- Always obtain written authorization before testing — never test without permission
- Define clear scope boundaries and rules of engagement before starting
- Document everything — evidence collection is critical for report credibility
- Use non-destructive techniques first — escalate carefully with client approval
- Test in production-like environments when possible for realistic results
- Validate all findings manually before reporting — false positives waste client time
- Provide actionable remediation steps, not just vulnerability descriptions
- Follow responsible disclosure timelines for any discovered vulnerabilities
- Use isolated test environments for exploit development and validation
- Maintain chain of custody for all evidence collected during testing

## Related Modules

- **security-audit**: Systematic security auditing methodology
- **threat-intelligence**: Threat data for targeted testing
- **incident-response**: Post-compromise investigation techniques
- **digital-forensics**: Evidence analysis after exploitation
