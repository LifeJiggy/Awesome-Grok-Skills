# Security Testing

## Overview

Security Testing identifies vulnerabilities and weaknesses in software systems before attackers can exploit them. This skill encompasses static and dynamic analysis tools, penetration testing methodologies, OWASP testing frameworks, and compliance verification. Security testing integrates throughout the development lifecycle from code review to production monitoring, protecting both systems and user data from malicious actors.

## Core Capabilities

DAST (Dynamic Application Security Testing) tools like OWASP ZAP and Burp Suite analyze running applications for vulnerabilities through automated scanning and manual testing. SAST (Static Application Security Testing) examines source code without execution, identifying potential security flaws early in development. SCA (Software Composition Analysis) scans dependencies for known vulnerabilities and license compliance issues.

Penetration testing methodologies follow frameworks like OWASP Testing Guide and PTES to systematically identify exploitable vulnerabilities. API security testing validates authentication, authorization, input validation, and business logic controls. Compliance checking verifies adherence to standards like PCI-DSS, HIPAA, and SOC2 requirements.

## Usage Examples

```python
from security_testing import SecurityTesting

security = SecurityTesting()

security.configure_owasp_zap(api_key="zap_api_key")

security.configure_burp_suite(project_file="/projects/app.burp")

security.configure_snyk(
    api_token="snyk_token",
    organization="my-org"
)

security.create_owasp_top10_test(category="A03")

api_test = security.create_api_security_test(
    api_spec="/openapi.yaml",
    endpoints=["GET /users", "POST /orders"]
)

security.configure_dast_pipeline(ci_cd_platform="github")

results = security.run_vulnerability_scan(
    target="https://api.example.com",
    scanner="zap",
    scan_type="full"
)

compliance = security.run_compliance_check(standard="PCI-DSS")
```

## Best Practices

Integrate security testing early in the development lifecycle using shift-left approaches. Combine automated scanning with manual testing for comprehensive coverage. Prioritize findings based on actual risk considering exploitability and business impact. Maintain updated vulnerability databases to detect the latest known vulnerabilities.

Set up automated security scanning in CI/CD pipelines with clear pass/fail criteria. Document all findings with remediation guidance and track resolution through completion. Conduct regular penetration tests by qualified security professionals. Maintain separate environments for security testing to avoid affecting production systems.

## Related Skills

- Vulnerability Assessment (vulnerability identification)
- Penetration Testing (exploitation testing)
- Secure Coding (prevention practices)
- Security Monitoring (ongoing security operations)

## Use Cases

Web application security testing identifies OWASP Top 10 vulnerabilities before production deployment. API security testing validates authentication flows and input validation across service boundaries. Mobile app security testing examines data storage, communication security, and platform-specific vulnerabilities. Compliance verification ensures organizations meet regulatory security requirements for handling sensitive data.

## Advanced Configuration

### OWASP ZAP Advanced Configuration

```python
from security_testing import OWASPZAPConfig, ScanPolicy

# Advanced ZAP configuration
zap_config = OWASPZAPConfig(
    api_key="your_api_key",
    proxy_host="localhost",
    proxy_port=8080,
    scan_policy=ScanPolicy(
        name="comprehensive",
        thresholds={
            "sql_injection": "medium",
            "xss": "medium",
            "csrf": "low",
            "directory_listing": "low",
        },
        strength="high",
        alert_threshold="medium",
    ),
    spider_config={
        "max_depth": 10,
        "max_children": 10,
        "recurse": True,
        "subtree_only": False,
    },
    active_scan_config={
        "max_scan_duration_minutes": 60,
        "thread_per_host": 5,
        "handleAntiCSRF": True,
    },
)

security = SecurityTesting(zap_config=zap_config)
```

### Burp Suite Advanced Configuration

```python
from security_testing import BurpSuiteConfig, ScanConfig

# Advanced Burp Suite configuration
burp_config = BurpSuiteConfig(
    project_file="/projects/app.burp",
    scan_config=ScanConfig(
        scan_type="deep",
        audit_items=["active", "passive"],
        insertion_points=["all"],
        platform_authentication=None,
        rate_limit_delay_ms=1000,
        max_requests_per_second=100,
    ),
    intruder_config={
        "payload_type": "recursive grep",
        "grep_match": "error",
        "extraction_regex": "token=(.+)",
    },
    repeater_config={
        "follow_redirects": True,
        "process_cookies": True,
    },
)

security = SecurityTesting(burp_config=burp_config)
```

### SAST Configuration

```python
from security_testing import SASTConfig, RuleSet

# Advanced SAST configuration
sast_config = SASTConfig(
    tool="semgrep",
    rulesets=[
        RuleSet("p/owasp-top-ten"),
        RuleSet("p/security-audit"),
        RuleSet("p/r2c-ci"),
        RuleSet("custom/company-rules"),
    ],
    severity_threshold="warning",
    auto_fix=True,
    ignore_patterns=["test/", "vendor/", "node_modules/"],
    file_extensions=[".py", ".js", ".ts", ".java", ".go"],
)

security = SecurityTesting(sast_config=sast_config)
```

### SCA Configuration

```python
from security_testing import SCAConfig, VulnerabilityPolicy

# Advanced SCA configuration
sca_config = SCAConfig(
    tool="snyk",
    api_token="your_token",
    organization="your-org",
    vulnerability_policy=VulnerabilityPolicy(
        auto_fix=False,
        severity_threshold="high",
        ignore_vulnerabilities=[],
        license_policy=["MIT", "Apache-2.0", "BSD-3-Clause"],
    ),
    dependency_files=["package.json", "requirements.txt", "go.mod"],
    deep_scan=True,
)

security = SecurityTesting(sca_config=sca_config)
```

## Architecture Patterns

### Security Testing Pipeline Pattern

```python
from security_testing import SecurityPipeline, PipelineStage

pipeline = SecurityPipeline(stages=[
    PipelineStage(
        name="sast",
        type="static",
        tool="semgrep",
        config=sast_config,
        blocking=True,
    ),
    PipelineStage(
        name="sca",
        type="composition",
        tool="snyk",
        config=sca_config,
        blocking=True,
    ),
    PipelineStage(
        name="dast",
        type="dynamic",
        tool="zap",
        config=zap_config,
        blocking=False,
    ),
    PipelineStage(
        name="secrets",
        type="secrets",
        tool="gitleaks",
        blocking=True,
    ),
    PipelineStage(
        name="compliance",
        type="compliance",
        standard="OWASP",
        blocking=False,
    ),
])

# Execute security pipeline
results = pipeline.execute()
print(f"Critical findings: {results.critical_count}")
print(f"High findings: {results.high_count}")
```

### Vulnerability Management Pattern

```python
from security_testing import VulnerabilityManager, Vulnerability

manager = VulnerabilityManager(
    deduplication=True,
    correlation=True,
    risk_scoring=True,
    auto_triage=True,
)

# Add findings
for finding in scan_results:
    vulnerability = Vulnerability(
        title=finding["title"],
        severity=finding["severity"],
        cvss_score=finding["cvss"],
        cve_id=finding.get("cve"),
        affected_component=finding["component"],
        remediation=finding["remediation"],
    )
    manager.add_vulnerability(vulnerability)

# Get prioritized list
prioritized = manager.get_prioritized_vulnerabilities()
print(f"Total vulnerabilities: {len(prioritized)}")
print(f"Critical: {manager.count_by_severity('critical')}")
print(f"High: {manager.count_by_severity('high')}")
```

### Compliance Verification Pattern

```python
from security_testing import ComplianceChecker, ComplianceStandard

checker = ComplianceChecker(
    standards=[
        ComplianceStandard("OWASP Top 10", version="2021"),
        ComplianceStandard("PCI-DSS", version="4.0"),
        ComplianceStandard("HIPAA", version="2023"),
        ComplianceStandard("SOC2", version="2"),
    ],
    auto_remediate=False,
    evidence_collection=True,
)

# Run compliance check
results = checker.check(application="my-app")

for standard in results.standards:
    print(f"{standard.name}: {standard.compliance_rate:.1%}")
    if standard.non_compliant_items:
        print(f"  Non-compliant items: {len(standard.non_compliant_items)}")
```

## Integration Guide

### CI/CD Integration

```python
from security_testing import CICDIntegration, PipelineConfig

# GitHub Actions integration
github_config = PipelineConfig(
    provider="github_actions",
    workflow_file="security_scan.yml",
    trigger_events=["push", "pull_request", "schedule"],
    schedule="0 6 * * 1",  # Weekly on Monday at 6 AM
    environment_variables={
        "ZAP_API_KEY": "${{ secrets.ZAP_API_KEY }}",
        "SNYK_TOKEN": "${{ secrets.SNYK_TOKEN }}",
    },
    quality_gates={
        "critical": 0,
        "high": 5,
        "medium": 20,
    },
)

cicd = CICDIntegration(config=github_config)
cicd.setup()
```

### Jira Integration

```python
from security_testing import JiraIntegration, JiraConfig

jira_config = JiraConfig(
    server="https://company.atlassian.net",
    project_key="SECURITY",
    issue_type="Security Bug",
    auto_create_issues=True,
    link_to_scan_results=True,
    transition_on_fix="Ready for Retest",
)

jira = JiraIntegration(config=jira_config)

# Create Jira issue from vulnerability
for vuln in results.critical_vulnerabilities:
    issue = jira.create_issue(
        summary=f"Critical: {vuln.title}",
        description=vuln.description,
        priority="Critical",
        labels=["security", "auto-scan"],
        custom_fields={
            "cvss_score": vuln.cvss_score,
            "cve_id": vuln.cve_id,
        },
    )
    print(f"Created issue: {issue.key}")
```

### Slack Integration

```python
from security_testing import SlackIntegration, SlackConfig

slack_config = SlackConfig(
    webhook_url="https://hooks.slack.com/services/...",
    channel="#security-alerts",
    mention_on_critical=["@security-team"],
    include_remediation=True,
    summary_on_complete=True,
)

slack = SlackIntegration(config=slack_config)
slack.notify_results(results)
```

## Performance Optimization

### Parallel Scanning

```python
from security_testing import ParallelScanner

scanner = ParallelScanner(
    max_workers=5,
    scan_types=["sast", "sca", "secrets"],
    resource_monitoring=True,
)

# Run scans in parallel
results = scanner.scan(
    source_code="/app/src",
    dependencies="/app/requirements.txt",
    secrets="/app/.env",
)

print(f"Total scan time: {results.total_time_seconds:.1f}s")
print(f"SAST time: {results.sast_time_seconds:.1f}s")
print(f"SCA time: {results.sca_time_seconds:.1f}s")
```

### Incremental Scanning

```python
from security_testing import IncrementalScanner

incremental = IncrementalScanner(
    baseline_scan="last_successful",
    change_detection=True,
    file_hash_tracking=True,
)

# Only scan changed files
results = incremental.scan(
    git_diff="HEAD~1",
    source_code="/app/src",
)

print(f"Files scanned: {results.files_scanned}")
print(f"Files skipped: {results.files_skipped}")
print(f"Time saved: {results.time_saved_seconds:.1f}s")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. False Positives

**Symptom**: High number of false positive findings

**Solution**:
```python
# Tune scan policies
scan_policy.alert_threshold = "high"

# Add suppressions
security.add_suppression(
    rule_id="sql-injection",
    file_pattern="test/*",
    reason="Test data only",
)

# Verify manually
for finding in results.findings:
    if security.verify_finding(finding):
        confirmed.append(finding)
```

#### 2. Scan Time Too Long

**Symptom**: Security scans take too long

**Solution**:
```python
# Use incremental scanning
incremental = IncrementalScanner(baseline_scan="last_successful")

# Reduce scan scope
scan_policy.strength = "medium"

# Parallelize
scanner = ParallelScanner(max_workers=5)
```

#### 3. Missing Vulnerabilities

**Symptom**: Vulnerabilities found in production not caught by scans

**Solution**:
```python
# Add custom rules
security.add_custom_rule(
    name="custom_sql_injection",
    pattern=r"execute\(.*\+.*\)",
    severity="high",
    description="Potential SQL injection",
)

# Increase scan coverage
scan_policy.insertion_points = ["all"]
scan_policy.strength = "high"
```

## API Reference

### Core Classes

#### `SecurityTesting`
```python
class SecurityTesting:
    def __init__(self, zap_config: Optional[OWASPZAPConfig] = None, burp_config: Optional[BurpSuiteConfig] = None) -> None: ...
    def configure_owasp_zap(self, api_key: str) -> None: ...
    def configure_burp_suite(self, project_file: str) -> None: ...
    def configure_snyk(self, api_token: str, organization: str) -> None: ...
    def create_owasp_top10_test(self, category: str) -> Test: ...
    def create_api_security_test(self, api_spec: str, endpoints: List[str]) -> Test: ...
    def run_vulnerability_scan(self, target: str, scanner: str, scan_type: str) -> ScanResults: ...
    def run_compliance_check(self, standard: str) -> ComplianceResults: ...
```

## Data Models

### Scan Results Schema

```json
{
  "scan_id": "uuid-v4",
  "timestamp": "2024-01-15T10:30:00Z",
  "target": "https://api.example.com",
  "scanner": "zap",
  "scan_type": "full",
  "duration_seconds": 1200,
  "findings": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 10,
    "informational": 15
  },
  "vulnerabilities": [
    {
      "title": "SQL Injection",
      "severity": "critical",
      "cvss_score": 9.8,
      "cve_id": "CVE-2024-0001",
      "affected_component": "/api/users",
      "remediation": "Use parameterized queries"
    }
  ]
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM owasp/zap2docker-stable:latest

COPY security_testing/ /app/security_testing/
WORKDIR /app

ENV ZAP_API_KEY=your_api_key
ENV ZAP_PROXY_PORT=8080

EXPOSE 8080

CMD ["zap.sh", "-daemon", "-host", "0.0.0.0", "-port", "8080"]
```

## Monitoring & Observability

### Metrics Collection

```python
from security_testing import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("security_scan_duration", type="histogram")
collector.register_metric("security_vulnerabilities_critical", type="gauge")
collector.register_metric("security_vulnerabilities_high", type="gauge")
collector.register_metric("security_scan_success", type="gauge")

collector.observe("security_scan_duration", scan_duration_seconds)
collector.set("security_vulnerabilities_critical", results.critical_count)
collector.set("security_vulnerabilities_high", results.high_count)
collector.set("security_scan_success", 1 if results.success else 0)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from security_testing import SecurityTesting, OWASPZAPConfig

class TestSecurityTesting:
    def setup_method(self):
        self.config = OWASPZAPConfig(api_key="test_key")
        self.security = SecurityTesting(zap_config=self.config)
    
    def test_vulnerability_scan(self):
        results = self.security.run_vulnerability_scan(
            target="http://localhost:8080",
            scanner="zap",
            scan_type="quick",
        )
        assert results.scan_id is not None
    
    def test_compliance_check(self):
        results = self.security.run_compliance_check(standard="OWASP")
        assert results.standards is not None
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: SAST and SCA support
- **Added**: Compliance verification
- **Improved**: 3x faster scanning
- **Fixed**: False positive reduction

## Glossary

| Term | Definition |
|------|------------|
| **DAST** | Dynamic Application Security Testing |
| **SAST** | Static Application Security Testing |
| **SCA** | Software Composition Analysis |
| **OWASP** | Open Web Application Security Project |
| **CVSS** | Common Vulnerability Scoring System |
| **CVE** | Common Vulnerabilities and Exposures |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/security-testing.git
cd security-testing
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Security Testing Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Data Validation

### Scan Result Validation

```python
from security_testing import ScanResultValidator

validator = ScanResultValidator()

# Validate scan results
validator.validate_findings(scan_results)
validator.validate_severity(findings)
validator.validate_remediation(recommendations)
```

## Advanced Patterns

### API Security Testing

```python
from security_testing import APISecurityTester, APIConfig

api_config = APIConfig(
    base_url="https://api.example.com",
    spec_file="openapi.yaml",
    authentication={
        "type": "bearer",
        "token": "your_token",
    },
    endpoints=[
        {"method": "GET", "path": "/users"},
        {"method": "POST", "path": "/users"},
        {"method": "GET", "path": "/users/{id}"},
        {"method": "PUT", "path": "/users/{id}"},
        {"method": "DELETE", "path": "/users/{id}"},
    ],
)

api_tester = APISecurityTester(config=api_config)

# Run API security tests
results = api_tester.test()
print(f"Authentication tests: {results.auth_tests.pass_rate:.1%}")
print(f"Authorization tests: {results.authz_tests.pass_rate:.1%}")
print(f"Input validation tests: {results.validation_tests.pass_rate:.1%}")
```

### Container Security Scanning

```python
from security_testing import ContainerScanner, ContainerConfig

container_config = ContainerConfig(
    images=["myapp:latest", "myapp-db:latest"],
    registries=["gcr.io", "docker.io"],
    scan_options={
        "os_vulnerabilities": True,
        "app_vulnerabilities": True,
        "secrets": True,
        "malware": True,
        "compliance": ["CIS", "NIST"],
    },
)

container_scanner = ContainerScanner(config=container_config)

# Scan container images
results = container_scanner.scan()
for image, result in results.items():
    print(f"\nImage: {image}")
    print(f"  Vulnerabilities: {result.vulnerability_count}")
    print(f"  Critical: {result.critical_count}")
    print(f"  Secrets: {result.secret_count}")
```

### Infrastructure as Code Security

```python
from security_testing import IaCScanner, IaCConfig

iac_config = IaCConfig(
    tools=["terraform", "cloudformation", "kubernetes"],
    scan_options={
        "misconfigurations": True,
        "security_baselines": True,
        "compliance": ["CIS", "NIST", "PCI-DSS"],
        "secrets": True,
        "drift_detection": True,
    },
)

iac_scanner = IaCScanner(config=iac_config)

# Scan IaC files
results = iac_scanner.scan(directory="infrastructure/")
print(f"Total issues: {results.issue_count}")
print(f"Critical: {results.critical_count}")
print(f"High: {results.high_count}")
```

### Dependency Vulnerability Scanning

```python
from security_testing import DependencyScanner, DependencyConfig

dep_config = DependencyConfig(
    ecosystems=["python", "javascript", "go", "java"],
    scan_options={
        "known_vulnerabilities": True,
        "license_compliance": True,
        "outdated_packages": True,
        "transitive_dependencies": True,
    },
    ignore_vulnerabilities=[],  # CVE IDs to ignore
)

dep_scanner = DependencyScanner(config=dep_config)

# Scan dependencies
results = dep_scanner.scan(directory="src/")
print(f"Total dependencies: {results.total_deps}")
print(f"Vulnerable: {results.vulnerable_deps}")
print(f"Outdated: {results.outdated_deps}")
```

### Secret Scanning

```python
from security_testing import SecretScanner, SecretConfig

secret_config = SecretConfig(
    patterns=[
        {"name": "AWS Key", "regex": "AKIA[0-9A-Z]{16}"},
        {"name": "API Key", "regex": "api[_-]?key[\"']?\\s*[:=]\\s*[\"']([^\"']+)[\"']"},
        {"name": "Password", "regex": "password[\"']?\\s*[:=]\\s*[\"']([^\"']+)[\"']"},
        {"name": "Private Key", "regex": "-----BEGIN (RSA |EC )?PRIVATE KEY-----"},
    ],
    scan_options={
        "git_history": True,
        "file_contents": True,
        "environment_variables": True,
        "configuration_files": True,
    },
)

secret_scanner = SecretScanner(config=secret_config)

# Scan for secrets
results = secret_scanner.scan(directory=".")
print(f"Secrets found: {results.secret_count}")
print(f"Files with secrets: {results.files_affected}")
```

### Network Security Testing

```python
from security_testing import NetworkScanner, NetworkConfig

network_config = NetworkConfig(
    targets=["192.168.1.0/24", "10.0.0.0/8"],
    scan_options={
        "port_scan": True,
        "service_detection": True,
        "os_detection": True,
        "vulnerability_scan": True,
        "ssl_tls_scan": True,
        "dns_enumeration": True,
    },
    exclude_hosts=["192.168.1.1"],  # Gateway
)

network_scanner = NetworkScanner(config=network_config)

# Scan network
results = network_scanner.scan()
print(f"Hosts discovered: {results.host_count}")
print(f"Open ports: {results.open_port_count}")
print(f"Services found: {results.service_count}")
print(f"Vulnerabilities: {results.vulnerability_count}")
```

### Social Engineering Testing

```python
from security_testing import SocialEngineeringTester, SocialConfig

social_config = SocialConfig(
    campaigns=[
        {
            "name": "Phishing Campaign",
            "type": "phishing",
            "templates": ["login_page", "password_reset", "invoice"],
            "target_groups": ["employees", "contractors"],
            "tracking": True,
        },
        {
            "name": "Vishing Campaign",
            "type": "vishing",
            "scripts": ["helpdesk", "executive"],
            "target_groups": ["helpdesk", "finance"],
        },
    ],
    ethics_approval=True,
    consent_obtained=True,
)

social_tester = SocialEngineeringTester(config=social_config)

# Run campaign
results = social_tester.run_campaign("phishing")
print(f"Emails sent: {results.emails_sent}")
print(f"Opened: {results.opened_count}")
print(f"Clicked: {results.clicked_count}")
print(f"Credentials submitted: {results.credentials_count}")
```

### Cloud Security Posture

```python
from security_testing import CloudPostureTester, CloudConfig

cloud_config = CloudConfig(
    providers=["aws", "azure", "gcp"],
    scan_options={
        "iam": True,
        "storage": True,
        "network": True,
        "compute": True,
        "database": True,
        "logging": True,
    },
    compliance_frameworks=["CIS", "PCI-DSS", "HIPAA"],
)

cloud_tester = CloudPostureTester(config=cloud_config)

# Test cloud security posture
results = cloud_tester.test()
for provider, result in results.items():
    print(f"\n{provider}:")
    print(f"  Score: {result.score:.1%}")
    print(f"  Issues: {result.issue_count}")
    print(f"  Compliance: {result.compliance_rate:.1%}")
```
