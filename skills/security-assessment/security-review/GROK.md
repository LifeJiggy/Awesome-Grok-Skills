---
name: "security-review"
category: "security-assessment"
version: "2.0.0"
tags: ["security-assessment", "security-review", "code-review", "architecture-review", "threat-modeling"]
---

# Security Review Module

## Overview

The Security Review module provides systematic evaluation of application security posture through architecture review, code-level security analysis, threat modeling, and control assessment. It combines automated static analysis with expert-guided review workflows to identify design flaws, insecure coding patterns, missing controls, and architectural weaknesses before they reach production. This module bridges the gap between automated scanning and manual expert review.

Designed for security architects, developers, and security champions, the module provides structured review workflows that ensure comprehensive coverage of high-risk code paths while minimizing review fatigue. It integrates with development workflows through IDE plugins, CI/CD pipelines, and pull request automation, enabling security review as part of the normal development process rather than a separate activity.

The module's threat modeling engine generates attack trees and threat catalogs that provide developers with actionable context about why certain code patterns are dangerous. This educational approach improves code quality over time as developers internalize security thinking through repeated exposure to threat models and review findings.

## Core Capabilities

1. **Architecture Security Review** — Evaluate system architecture against security principles (defense-in-depth, least privilege, secure defaults). Identify single points of failure, trust boundary violations, and insecure data flows with visual diagrams.

2. **Threat Modeling** — Structured threat modeling using STRIDE, PASTA, and Attack Tree methodologies. Generate threat catalogs with attack trees, mitigations, and risk ratings for each threat scenario.

3. **Code Security Review** — Guided code review workflows for high-risk code paths: authentication, authorization, cryptography, input handling, serialization, and API endpoints with pattern matching.

4. **Control Effectiveness Assessment** — Evaluate security controls against design requirements. Identify control gaps, bypasses, and design weaknesses with evidence-based validation.

5. **Secure Design Patterns** — Validate implementation against secure design patterns for authentication, session management, encryption, error handling, and logging with compliance mapping.

6. **Security Debt Tracking** — Track technical security debt with risk-based prioritization, remediation assignments, and trend metrics with historical comparison.

7. **Threat Intelligence Integration** — Correlate identified threats with current threat intelligence feeds and known attack patterns for context-aware prioritization.

8. **Developer Feedback Loop** — Provide contextual security feedback during code review with educational explanations and secure code alternatives.

## Usage Examples

### Architecture Security Review

```python
from security_assessment.security_review import ArchitectureReviewer

reviewer = ArchitectureReviewer()
architecture = reviewer.load_architecture(
    diagrams=["./docs/architecture.drawio"],
    data_flows=["./docs/data-flow.md"],
    deployment=["./docs/deployment.yaml"]
)

findings = reviewer.review(
    principles=["least_privilege", "defense_in_depth", "secure_defaults"],
    trust_boundaries=True,
    data_classification=True
)

for finding in findings:
    print(f"[{finding.severity}] {finding.category}: {finding.title}")
    print(f"  Component: {finding.component}")
    print(f"  Issue: {finding.description}")
    print(f"  Recommendation: {finding.recommendation}")
```

### STRIDE Threat Modeling

```python
from security_assessment.security_review import ThreatModeler

modeler = ThreatModeler(methodology="STRIDE")
model = modeler.build_model(
    components=system_components,
    data_flows=data_flows,
    trust_boundaries=trust_zones
)

threats = modeler.identify_threats(
    categories=["spoofing", "tampering", "repudiation",
                 "information_disclosure", "denial_of_service",
                 "elevation_of_privilege"]
)

for threat in threats:
    print(f"[{threat.stride_category}] {threat.title}")
    print(f"  Target: {threat.target_component}")
    print(f"  Risk: {threat.risk_rating}")
    print(f"  Mitigation: {threat.mitigation}")
    print(f"  Attack tree: {threat.attack_tree_id}")
```

### Code Security Review

```python
from security_assessment.security_review import CodeReviewer

reviewer = CodeReviewer(
    languages=["python", "javascript"],
    review_focus=["auth", "crypto", "input_validation", "serialization"]
)

code_findings = reviewer.review_paths(
    paths=["./src/auth/", "./src/api/", "./lib/crypto/"],
    severity=["critical", "high", "medium"]
)

for finding in code_findings:
    print(f"[{finding.severity}] {finding.rule_id}: {finding.title}")
    print(f"  File: {finding.file}:{finding.line}")
    print(f"  Pattern: {finding.pattern}")
    print(f"  Fix: {finding.remediation}")
    print(f"  CWE: {finding.cwe_id}")
```

### Threat Model for API

```python
from security_assessment.security_review import APIThreatModeler

api_modeler = APIThreatModeler(
    openapi_spec="./api/openapi.yaml",
    auth_schemes=["oauth2", "api_key"]
)

api_threats = api_modeler.analyze(
    endpoints=["/api/v2/users", "/api/v2/payments", "/api/v2/admin"],
    data_classes=["PII", "financial", "internal"]
)

for endpoint in api_threats.endpoints:
    print(f"\nEndpoint: {endpoint.method} {endpoint.path}")
    for threat in endpoint.threats:
        print(f"  [{threat.risk}] {threat.title}")
        print(f"    Attack: {threat.attack_vector}")
        print(f"    Mitigation: {endpoint.get_mitigation(threat)}")
```

### Control Assessment

```python
from security_assessment.security_review import ControlAssessor

assessor = ControlAssessor()
controls = assessor.assess_controls(
    categories=["access_control", "cryptography", "input_validation",
                  "logging", "error_handling", "session_management"],
    implementation_evidence=control_evidence,
    requirements=security_requirements
)

print(f"Control Assessment Summary:")
print(f"  Total controls assessed: {controls.total}")
print(f"  Effective: {controls.effective}")
print(f"  Partially effective: {controls.partial}")
print(f"  Ineffective: {controls.ineffective}")
print(f"  Not implemented: {controls.missing}")

for gap in controls.gaps:
    print(f"\n  GAP: {gap.control} — {gap.description}")
    print(f"  Risk: {gap.risk}")
    print(f"  Remediation: {gap.recommendation}")
```

### Security Debt Tracking

```python
from security_assessment.security_review import SecurityDebtTracker

tracker = SecurityDebtTracker()
tracker.load_baseline("./baseline.json")

debt = tracker.calculate_debt(
    codebase_path="./src/",
    findings=all_findings,
    exclude_false_positives=True
)

print(f"Security Debt Summary:")
print(f"  Total debt items: {debt.total_items}")
print(f"  Critical debt: {debt.critical}")
print(f"  Estimated remediation effort: {debt.estimated_hours}h")
print(f"  Debt trend: {debt.trend} (vs last quarter)")
```

## Architecture

```
┌────────────────────────────────────────────────────┐
│              Security Review Module                 │
├──────────────┬──────────────┬──────────────────────┤
│ Architecture │   Threat     │   Code               │
│ Review       │  Modeling    │  Review              │
├──────────────┼──────────────┼──────────────────────┤
│ Principles   │ STRIDE       │ Pattern Matching     │
│ Trust Zones  │ Attack Trees │ Secure Coding        │
│ Data Flows   │ PASTA        │ CWE Mapping          │
│ SPOF Detect  │ Risk Rating  │ Remediation Guide    │
├──────────────┴──────────────┴──────────────────────┤
│         Control Assessment & Debt Tracking          │
├────────────────────────────────────────────────────┤
│  Threat Intel  │  Developer   │  Reporting          │
│  Integration   │  Feedback    │  Dashboard          │
└────────────────────────────────────────────────────┘
```

The module operates on three parallel review tracks: architecture, threat modeling, and code review. Each track produces findings that feed into a unified assessment, with control effectiveness assessment validating that security controls address identified threats. The debt tracking system maintains historical context for trend analysis.

## Best Practices

1. **Threat Model Early** — Perform threat modeling during design phase when changes are cheap. Post-implementation threat modeling is 10x more expensive.

2. **Risk-Based Focus** — Focus deep review on high-risk components: authentication, authorization, cryptographic, data handling, and external interfaces.

3. **Checklist + Expert Judgment** — Use checklists for completeness but rely on expert judgment for context. Checklists miss design flaws.

4. **Peer Review** — Security reviews should involve multiple reviewers with different perspectives (developer, architect, security specialist).

5. **Architectural Decision Records** — Document security-relevant architectural decisions with rationale and tradeoffs for future reference.

6. **Threat Model Living Documents** — Update threat models when architecture changes. Stale threat models provide false confidence.

7. **Security Champions** — Embed security champions in development teams to catch issues during code review, not after.

8. **Metrics That Matter** — Track: findings per component, mean time to remediate, security debt ratio, findings by category, and review coverage.

9. **Continuous Improvement** — Review security findings quarterly to identify systemic issues and update review checklists accordingly.

## Performance Considerations

- Architecture review depends on diagram complexity; simplify diagrams for faster analysis.
- Threat modeling with STRIDE completes in 2-5 minutes for typical systems; PASTA analysis may take 10-20 minutes.
- Code review scales with codebase size; focus on high-risk paths rather than reviewing entire codebases.
- Control assessment requires evidence collection which may take 1-2 hours for comprehensive evaluation.
- Security debt tracking benefits from incremental updates rather than full recalculation each time.

## Security Considerations

- Security review findings may contain sensitive architectural details; restrict access to authorized personnel.
- Threat models reveal attack vectors; protect from external disclosure that could enable targeted attacks.
- Code review findings may expose insecure patterns; handle as sensitive vulnerability information.
- Control assessment evidence may contain configuration details; redact before sharing externally.
- Security debt metrics provide insight into security posture; protect from competitive intelligence gathering.

## Related Modules

- `vulnerability-assessment` — Technical vulnerability scanning to validate review findings with automated tools
- `risk-assessment` — Quantitative risk analysis for security review priorities and resource allocation
- `penetration-testing` — Adversarial validation of security review assumptions and attack path verification
- `compliance-audit` — Mapping review findings to compliance requirements and framework controls

## Configuration Reference

```yaml
# security_review_config.yaml
architecture_review:
  principles:
    - least_privilege
    - defense_in_depth
    - secure_defaults
    - separation_of_duties
  trust_boundaries: true
  data_classification: true

threat_modeling:
  methodology: STRIDE  # STRIDE | PASTA | Attack Trees
  categories:
    - spoofing
    - tampering
    - repudiation
    - information_disclosure
    - denial_of_service
    - elevation_of_privilege

code_review:
  languages: ["python", "javascript", "java"]
  focus_areas:
    - authentication
    - authorization
    - cryptography
    - input_validation
    - serialization

reporting:
  formats: ["html", "json", "pdf"]
  include_attack_trees: true
  include_remediation: true
  executive_summary: true
```

## Integration Guide

The module integrates with common development and security tools:

- **IDE Plugins** — Integrate with VS Code, IntelliJ for real-time security feedback during development.
- **CI/CD Integration** — Run security reviews on every pull request with automated gating.
- **Static Analysis Tools** — Import findings from SonarQube, Semgrep, Checkmarx for correlation.
- **Threat Intelligence** — Correlate threats with MITRE ATT&CK and current threat intelligence feeds.

## References

- OWASP Application Security Verification Standard (ASVS)
- Microsoft Threat Modeling Tool Documentation
- STRIDE Threat Model — Microsoft Security Development Lifecycle
- PASTA — Process for Attack Simulation and Threat Analysis
- CWE — Common Weakness Enumeration
- NIST SP 800-53 Rev 5 — Security and Privacy Controls
- BSIMM — Building Security In Maturity Model
- SANS Secure Coding Principles
