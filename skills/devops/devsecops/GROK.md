---
name: devsecops
category: devops
version: 1.0.0
tags: [devops, devsecops, security, scanning, compliance, supply-chain]
---

# DevSecOps

## Overview

DevSecOps integrates security practices into every phase of the software development lifecycle, shifting security left so that vulnerabilities are caught early, remediated quickly, and prevented from reaching production. This module provides a comprehensive toolkit for embedding security into CI/CD pipelines, managing secrets, scanning for vulnerabilities (SAST, DAST, SCA, container scanning), enforcing compliance policies, and monitoring supply chain security.

The module implements a defense-in-depth approach: pre-commit hooks catch secrets and vulnerable dependencies, CI pipeline stages run SAST and container scans, DAST runs against staging environments, and production monitoring detects runtime vulnerabilities. Every scan result feeds into a centralized security dashboard with remediation guidance, SLA tracking, and integration with issue trackers.

Supply chain security is a first-class concern: the module monitors dependency updates, detects dependency confusion attacks, verifies artifact signatures (Sigstore/Cosign), and generates SBOMs (Software Bill of Materials) for compliance. Container image scanning includes vulnerability assessment, misconfiguration detection, and compliance checking against CIS benchmarks. The module integrates with major security tools (Snyk, Trivy, Checkmarx, SonarQube, OWASP ZAP) through a unified interface.

## Core Capabilities

- SAST (Static Application Security Testing) with language-specific analyzers
- DAST (Dynamic Application Security Testing) against running applications
- SCA (Software Composition Analysis) for dependency vulnerabilities
- Container image scanning with vulnerability and misconfiguration detection
- Secret detection in source code, configs, and commit history
- SBOM generation and supply chain monitoring
- Compliance policy enforcement (SOC2, HIPAA, PCI DSS, GDPR)
- Security gate integration in CI/CD pipelines
- Vulnerability management with SLA tracking and remediation guidance
- Artifact signing and verification (Sigstore/Cosign)

## Usage Examples

### Secret Detection

```python
from devsecops import SecretScanner

scanner = SecretScanner()

# Scan a repository
findings = scanner.scan_directory("/path/to/repo")
for finding in findings:
    print(f"[{finding.severity}] {finding.secret_type}: {finding.file}:{finding.line}")
    print(f"  Pattern: {finding.pattern_name}")
    print(f"  Suggestion: {finding.remediation}")
```

### SAST Scanning

```python
from devsecops import SASTScanner

sast = SASTScanner(language="python", rules="owasp-top10")
results = sast.scan("/path/to/source")
print(f"Vulnerabilities: {results.total}")
for vuln in results.vulnerabilities:
    print(f"  [{vuln.severity}] {vuln.cwe}: {vuln.description}")
    print(f"  File: {vuln.file}:{vuln.line}")
    print(f"  Fix: {vuln.fix_suggestion}")
```

### Container Scanning

```python
from devsecops import ContainerScanner

scanner = ContainerScanner()
results = scanner.scan_image("myapp:v2.1.0")
print(f"Vulnerabilities: {results.total}")
print(f"  Critical: {results.critical}")
print(f"  High: {results.high}")
print(f"  Medium: {results.medium}")
print(f"  Low: {results.low}")

for vuln in results.vulnerabilities:
    print(f"  {vuln.cve}: {vuln.package} {vuln.installed_version} -> {vuln.fixed_version}")
```

### SCA for Dependencies

```python
from devsecops import SCAScanner

sca = SCAScanner()
results = sca.scan("/path/to/project")
print(f"Dependencies: {results.total_dependencies}")
print(f"Vulnerable: {results.vulnerable_count}")
print(f"Outdated: {results.outdated_count}")

for vuln in results.vulnerabilities:
    print(f"  {vuln.package}: {vuln.vulnerability_id} ({vuln.severity})")
    print(f"    Installed: {vuln.installed_version}")
    print(f"    Fixed: {vuln.fixed_version}")
    print(f"    Upgrade: {vuln.upgrade_path}")
```

### CI/CD Pipeline Integration

```python
from devsecops import SecurityGate

gate = SecurityGate(
    fail_on=["critical", "high"],
    warn_on=["medium"],
    max_vulnerabilities=0,
    required_scans=["sast", "sca", "container"],
)

# Run in CI pipeline
result = gate.evaluate(scan_results)
if result.passed:
    print("Security gate passed")
else:
    print(f"Security gate failed: {result.failures}")
```

### SBOM Generation

```python
from devsecops import SBOMGenerator

generator = SBOMGenerator(format="spdx-json")
sbom = generator.generate("/path/to/project")
generator.write(sbom, "sbom.spdx.json")

# Upload to dependency tracking
generator.upload_to_defectdojo(sbom, "https://defectdojo.example.com")
```

## Advanced Configuration

### Custom Scan Rules

```python
from devsecops import CustomRule

rule = CustomRule(
    id="CUSTOM-001",
    name="Hardcoded API Key Pattern",
    pattern=r"(?:api[_-]?key|apikey)\s*[=:]\s*['\"]([a-zA-Z0-9]{32,})['\"]",
    severity="high",
    cwe="CWE-798",
    remediation="Use environment variables or secrets manager",
)
scanner.add_custom_rule(rule)
```

### Compliance Policy

```python
from devsecops import CompliancePolicy

policy = CompliancePolicy(
    name="SOC2-Controls",
    rules=[
        {"type": "no_critical_vulns", "max": 0},
        {"type": "no_hardcoded_secrets", "max": 0},
        {"type": "container_base_image", "allowed": ["ubuntu:22.04", "python:3.11-slim"]},
        {"type": "dependency_license", "blocked": ["GPL-3.0", "AGPL-3.0"]},
        {"type": "sbom_required", "format": "spdx-json"},
    ],
)
results = policy.evaluate(project_path="/path/to/project")
```

## Architecture Patterns

### Shift-Left Security Pipeline

```
Pre-Commit → CI Build → Staging DAST → Production Monitoring
    │              │              │               │
    ├── Secret     ├── SAST       ├── DAST        ├── RASP
    │   Detection  ├── SCA        ├── API Scan    ├── WAF
    ├── Lint       ├── Container  ├── Auth Test   ├── SIEM
    │   Security   │   Scan       └── Perf Test   └── Threat
    └── License    └── SBOM                       Intelligence
        Check         Generation
```

### Vulnerability Lifecycle

```
Detection → Triage → Assignment → Remediation → Verification → Closure
```

## Integration Guide

### GitHub Actions

```yaml
# .github/workflows/security.yml
name: Security Scanning

on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run SAST
        uses: github/codeql-action/analyze@v2

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Scan container
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:latest
          severity: CRITICAL,HIGH
```

### Snyk Integration

```python
from devsecops import SnykIntegration

snyk = SnykIntegration(api_token="your-token")
results = snyk.test_project("my-org/my-project")
snyk.monitor_project("my-org/my-project")
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Incremental scanning | Scan only changed files |
| Parallel scan execution | 5x faster pipeline |
| Vulnerability caching | Skip known results |
| Baseline comparison | Only report new findings |
| Async upload | Non-blocking SBOM submission |

## Security Considerations

- **Scan tool integrity**: Verify scanner checksums before execution
- **Credential management**: Use CI/CD secrets, not hardcoded tokens
- **Scanner permissions**: Least-privilege for scan agents
- **Result storage**: Encrypt vulnerability data at rest
- **Access control**: Restrict who can view/modify scan results

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| False positive in SAST | Tainted data flow not tracked | Add sanitizer annotations |
| Container scan timeout | Large image | Scan only production layers |
| SBOM generation slow | Too many dependencies | Use cached dependency tree |
| Gate fails on medium | Policy too strict | Adjust fail_on thresholds |
| Secret detection noisy | Test fixtures flagged | Add patterns to ignore list |

## API Reference

### SecretScanner

```python
class SecretScanner:
    def __init__(self, rules: list = None, ignore_patterns: list = None)
    def scan_directory(self, path: str) -> list[SecretFinding]
    def scan_file(self, path: str) -> list[SecretFinding]
    def scan_diff(self, diff: str) -> list[SecretFinding]
```

### ContainerScanner

```python
class ContainerScanner:
    def __init__(self, severities: list = None)
    def scan_image(self, image: str) -> ScanResults
    def scan_dockerfile(self, path: str) -> DockerfileResults
    def scan_compose(self, path: str) -> ComposeResults
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class Vulnerability:
    id: str
    severity: Severity
    description: str
    file: str
    line: int
    fix_suggestion: str

@dataclass
class ScanResults:
    total: int
    critical: int
    high: int
    medium: int
    low: int
    vulnerabilities: list[Vulnerability]
```

## Deployment Guide

### Installation

```bash
pip install devsecops
# With all scanners
pip install devsecops[all]
```

### Pipeline Setup

1. Add secret scanning to pre-commit hooks
2. Add SAST/SCA to CI pipeline
3. Add container scanning to build pipeline
4. Add DAST to staging deployment
5. Configure security gate thresholds
6. Set up vulnerability dashboard

## Monitoring & Observability

```python
from devsecops import MetricsCollector

collector = MetricsCollector()
collector.counter("security.vulnerabilities.total", count, tags={"severity": sev, "type": vtype})
collector.gauge("security.gate.pass_rate", rate)
collector.counter("security.secrets.detected", count, tags={"type": secret_type})
collector.histogram("security.scan.duration_seconds", duration)
```

## Testing Strategy

```python
import pytest
from devsecops import SecretScanner

def test_secret_detection():
    scanner = SecretScanner()
    findings = scanner.scan_file("test_secret.py")
    assert len(findings) > 0
    assert findings[0].secret_type == "AWS Access Key"
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added SBOM generation | Enable SBOM in pipeline |
| 2.0.0 | New scan engine | Update scanner configs |

## Glossary

| Term | Definition |
|------|-----------|
| **SAST** | Static Application Security Testing |
| **DAST** | Dynamic Application Security Testing |
| **SCA** | Software Composition Analysis |
| **SBOM** | Software Bill of Materials |
| **CWE** | Common Weakness Enumeration |
| **CVE** | Common Vulnerabilities and Exposures |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with SAST, DAST, SCA scanning
- Secret detection and container scanning
- CI/CD security gate integration
- SBOM generation and compliance checking

## Contributing Guidelines

```bash
git clone https://github.com/example/devsecops.git
pip install -e ".[dev]"
pytest tests/
```

## Advanced Security Scanning

### Runtime Application Self-Protection (RASP)

```python
from devsecops import RASPMonitor

rasp = RASPMonitor(
    service="api-gateway",
    rules=[
        {"type": "sql_injection", "action": "block", "severity": "critical"},
        {"type": "xss_attempt", "action": "alert", "severity": "high"},
        {"type": "path_traversal", "action": "block", "severity": "critical"},
        {"type": "command_injection", "action": "block", "severity": "critical"},
    ],
    logging_enabled=True,
)

# Attach to application
rasp.instrument(app)

# Query attack attempts
attacks = rasp.get_recent_attacks(window_minutes=60)
print(f"Blocked: {attacks.blocked_count}")
print(f"Alerted: {alerts.alerted_count}")
print(f"Top attack type: {attacks.most_common_type}")
```

### Supply Chain Security Monitoring

```python
from devsecops import SupplyChainMonitor

monitor = SupplyChainMonitor(
    project="my-org/my-project",
    registries=["npm", "pypi", "docker-hub"],
)

# Monitor for dependency confusion
confusion = monitor.check_dependency_confusion()
for risk in confusion.risks:
    print(f"  Package: {risk.package_name}")
    print(f"  Internal: {risk.internal_registry}")
    print(f"  Public: {risk.public_registry}")
    print(f"  Risk: {risk.severity}")

# Monitor for typosquatting
typosquats = monitor.check_typosquatting()
for typosquat in typosquats:
    print(f"  Suspicious: {typosquat.name} (similarity: {typosquat.similarity:.2%})")

# Verify artifact signatures
signatures = monitor.verify_signatures("myapp:v2.1.0")
print(f"Signed: {signatures.is_signed}")
print(f"Signer: {signatures.signer}")
print(f"Trusted: {signatures.is_trusted}")
```

### Infrastructure as Code Security

```python
from devsecops import IaCScanner

iac = IaCScanner()

# Scan Terraform
tf_results = iac.scan_terraform("/path/to/terraform")
for finding in tf_results.findings:
    print(f"  [{finding.severity}] {finding.resource}: {finding.description}")
    print(f"    Rule: {finding.rule_id}")
    print(f"    Fix: {finding.fix_suggestion}")

# Scan Kubernetes manifests
k8s_results = iac.scan_kubernetes("/path/to/k8s/manifests")
for finding in k8s_results.findings:
    print(f"  [{finding.severity}] {finding.resource}: {finding.description}")

# Scan Helm charts
helm_results = iac.scan_helm("/path/to/helm/chart")
for finding in helm_results.findings:
    print(f"  [{finding.severity}] {finding.template}: {finding.description}")
```

### Security Policy Enforcement

```python
from devsecops import PolicyEngine

engine = PolicyEngine()

# Define OPA-like policies
engine.add_policy(
    name="no-privileged-containers",
    description="Containers must not run as privileged",
    check=lambda resource: resource.get("security_context", {}).get("privileged", False) == False,
    severity="critical",
    remediation="Remove privileged: true from securityContext",
)

engine.add_policy(
    name="image-scan-required",
    description="All images must be scanned before deployment",
    check=lambda resource: resource.get("scan_status") == "passed",
    severity="high",
    remediation="Run container scan before deployment",
)

# Evaluate against resources
results = engine.evaluate(k8s_resources)
print(f"Passed: {results.passed_count}")
print(f"Failed: {results.failed_count}")
print(f"Blocked: {results.blocked_count}")
```

### Security Gate CI/CD Integration

```python
from devsecops import SecurityGateV2

gate = SecurityGateV2(
    rules=[
        {"scan": "sast", "max_critical": 0, "max_high": 0},
        {"scan": "sca", "max_critical": 0, "max_high": 5},
        {"scan": "container", "max_critical": 0, "max_high": 3},
        {"scan": "secrets", "max_total": 0},
        {"scan": "iac", "max_critical": 0, "max_high": 2},
    ],
    exemptions_file=".security-exemptions.json",
    notify=["slack-security", "jira-security"],
)

# Run in pipeline
result = gate.evaluate(scan_results)
if not result.passed:
    for failure in result.failures:
        print(f"  FAIL: {failure.rule} — {failure.message}")
```

### Vulnerability Prioritization

```python
from devsecops import VulnerabilityPrioritizer

prioritizer = VulnerabilityPrioritizer(
    exploitability_weight=0.4,
    severity_weight=0.3,
    exposure_weight=0.2,
    age_weight=0.1,
)

# Prioritize vulnerabilities
prioritized = prioritizer.prioritize(vulnerabilities)
for i, vuln in enumerate(prioritized[:10], 1):
    print(f"  {i}. [{vuln.priority_score:.2f}] {vuln.id} ({vuln.severity})")
    print(f"     Exploitable: {vuln.is_exploitable}")
    print(f"     Exposed: {vuln.is_exposed}")
    print(f"     Age: {vuln.age_days} days")
```

### Security Metrics Dashboard

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Critical vulns | 0 | 0 | Passing |
| High vulns | < 5 | 3 | Passing |
| Mean time to fix (critical) | < 24h | 18h | Passing |
| Mean time to fix (high) | < 7d | 5d | Passing |
| Secret scan pass rate | 100% | 98% | Warning |
| SBOM coverage | 100% | 85% | Warning |
| Container scan coverage | 100% | 100% | Passing |
| Security gate pass rate | > 95% | 97% | Passing |

### Threat Modeling Integration

```python
from devsecops import ThreatModeler

modeler = ThreatModeler(project="payment-service")

# Generate threat model
threats = modeler.analyze(
    components=["api", "database", "payment-gateway", "cache"],
    data_flows=[
        {"from": "user", "to": "api", "protocol": "HTTPS"},
        {"from": "api", "to": "database", "protocol": "TCP"},
        {"from": "api", "to": "payment-gateway", "protocol": "HTTPS"},
    ],
)

for threat in threats:
    print(f"  [{threat.risk_level}] {threat.description}")
    print(f"    STRIDE: {threat.stride_category}")
    print(f"    Mitigation: {threat.mitigation}")
```

### DAST Scanning (Advanced)

```python
from devsecops import DASTScanner

dast = DASTScanner(
    target_url="https://staging.example.com",
    auth_config={
        "type": "form",
        "login_url": "/login",
        "username_field": "email",
        "password_field": "password",
        "credentials": ("test@example.com", "password123"),
    },
    scan_policy="owasp-top10",
    max_depth=5,
    timeout_s=600,
)

results = dast.scan()
print(f"URLs tested: {results.urls_tested}")
print(f"Vulnerabilities: {results.total}")
for vuln in results.vulnerabilities:
    print(f"  [{vuln.severity}] {vuln.type}: {vuln.url}")
    print(f"    Parameter: {vuln.parameter}")
    print(f"    Evidence: {vuln.evidence[:100]}")
```

### License Compliance Scanning

```python
from devsecops import LicenseScanner

scanner = LicenseScanner(
    allowed_licenses=["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"],
    blocked_licenses=["GPL-3.0", "AGPL-3.0", "SSPL-1.0"],
    warn_licenses=["LGPL-2.1", "MPL-2.0"],
)

results = scanner.scan("/path/to/project")
print(f"Total dependencies: {results.total}")
print(f"Allowed: {results.allowed_count}")
print(f"Blocked: {results.blocked_count}")
print(f"Warn: {results.warn_count}")

for dep in results.blocked:
    print(f"  BLOCKED: {dep.name} — {dep.license} (replace or remove)")
```

### License Compliance Scanning

```python
from devsecops import LicenseScanner

scanner = LicenseScanner(
    allowed_licenses=["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"],
    blocked_licenses=["GPL-3.0", "AGPL-3.0", "SSPL-1.0"],
    warn_licenses=["LGPL-2.1", "MPL-2.0"],
)

results = scanner.scan("/path/to/project")
print(f"Total dependencies: {results.total}")
print(f"Allowed: {results.allowed_count}")
print(f"Blocked: {results.blocked_count}")
print(f"Warn: {results.warn_count}")

for dep in results.blocked:
    print(f"  BLOCKED: {dep.name} — {dep.license} (replace or remove)")
```

### Security Scanner Comparison Matrix

| Tool | Type | Languages | Speed | False Positive Rate |
|------|------|-----------|-------|---------------------|
| Trivy | Container/SCA | Multi | Fast | Low |
| Semgrep | SAST | 20+ | Fast | Medium |
| Bandit | SAST | Python | Fast | Medium |
| OWASP ZAP | DAST | Any | Slow | Low |
| Snyk | SCA | Multi | Medium | Low |
| Checkmarx | SAST/DAST | Multi | Slow | Low |
| Grype | Container | Multi | Fast | Low |

### Security Debt Tracking

```python
from devsecops import SecurityDebtTracker

tracker = SecurityDebtTracker(project="my-app")

# Add debt items
tracker.add(
    vulnerability_id="CVE-2024-1234",
    severity="high",
    age_days=45,
    assigned_team="backend",
    remediation_effort="2h",
    risk_acceptance=None,
)

# Generate debt report
report = tracker.report()
print(f"Total debt items: {report.total_items}")
print(f"Critical debt: {report.critical_count}")
print(f"Oldest item: {report.oldest_age_days} days")
print(f"Teams with most debt:")
for team in report.team_breakdown:
    print(f"  {team.name}: {team.count} items ({team.avg_age_days:.0f} days avg)")
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
