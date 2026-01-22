# DevSecOps

## Overview

DevSecOps integrates security practices into the DevOps process, embedding security throughout the development lifecycle rather than treating it as a separate phase. This skill covers security automation in CI/CD pipelines, shift-left security testing, compliance as code, and security monitoring. DevSecOps aims to make security everyone's responsibility while maintaining development velocity.

## Core Capabilities

SAST tools analyze source code for vulnerabilities during development. DAST tools test running applications for security weaknesses. SCA tools scan dependencies for known vulnerabilities. Container security scanning ensures images are free from vulnerabilities.

Infrastructure as Code security validates cloud configurations against policies. Secret scanning detects exposed credentials in code repositories. Compliance automation checks for regulatory requirements automatically. Security metrics track vulnerability detection and remediation performance.

## Usage Examples

```python
from devsecops import DevSecOps

pipeline = DevSecOps()

pipeline.create_pipeline(name="Secure CI/CD")

stage = pipeline.add_stage(name="Build", stage_type="build")

sast_scan = pipeline.add_sast_scan(
    stage="Build",
    tool="sonarqube",
    rules_profile="Security Hotspots"
)

dast_scan = pipeline.add_dast_scan(
    stage="Security",
    tool="owasp_zap",
    target_url="https://staging.example.com"
)

sca_scan = pipeline.add_sca_scan(
    stage="Dependencies",
    tool="snyk",
    severity_threshold="medium"
)

container_scan = pipeline.add_container_scan(
    stage="Build",
    tool="trivy",
    fail_on_critical=True
)

infra_scan = pipeline.add_infra_scan(
    stage="Infrastructure",
    tool="checkov",
    policy_pack="aws-cis"
)

secret_scan = pipeline.add_secret_scan(
    stage="Commit",
    tool="gitleaks"
)

policy_gate = pipeline.configure_policy_gate(
    gate_name="Security Gate",
    conditions=[
        {"metric": "vulnerability_count", "threshold": 0, "severities": ["critical", "high"]},
        {"metric": "secret_count", "threshold": 0}
    ],
    action="fail"
)

compliance = pipeline.create_compliance_check(
    standard="SOC2",
    controls=["CC6.1", "CC6.6", "CC7.2"]
)

metrics = pipeline.configure_shift_left_metrics()

chatbot = pipeline.create_security_chatbot(
    name="SecurityBot",
    platform="slack",
    responders=["security-team", "dev-team"]
)

approval = pipeline.add_approval_gate(
    stage="Production",
    approvers=["security-approver"],
    timeout_hours=48
)

feedback = pipeline.configure_security_feedback(
    channel="#security-reports",
    report_format="html"
)

triage = pipeline.create_vulnerability_triage(
    workflow="automated",
    slas=[
        {"severity": "critical", "hours": 4},
        {"severity": "high", "hours": 24},
        {"severity": "medium", "hours": 72},
        {"severity": "low", "hours": 720}
    ]
)

dashboard = pipeline.create_security_metrics_dashboard(
    panels=[
        {"name": "Vulnerability Trend", "query": "trend(vulnerabilities)"},
        {"name": "MTTD", "query": "avg(mttd_hours)"},
        {"name": "MTTR", "query": "avg(mttr_hours)"}
    ]
)

pen_test = pipeline.configure_pen_test_schedule(
    frequency="quarterly",
    scope="full"
)
```

## Best Practices

Shift security left to catch issues early when they're cheaper to fix. Automate security testing in CI/CD to ensure consistent coverage. Define clear security gates with pass/fail criteria. Prioritize vulnerabilities based on severity and exploitability.

Integrate security feedback into development workflows. Track and report security metrics to demonstrate improvement. Train developers on secure coding practices. Balance security controls with development velocity.

## Related Skills

- CI/CD Pipelines (automation)
- Security Testing (testing practices)
- Cloud Security (cloud-specific security)
- Site Reliability Engineering (operations)

## Use Cases

Enterprise DevSecOps implements comprehensive security across large codebases. Startup DevSecOps enables security without slowing development velocity. Regulated industry DevSecOps automates compliance checks. Cloud-native DevSecOps secures containerized and serverless applications.
