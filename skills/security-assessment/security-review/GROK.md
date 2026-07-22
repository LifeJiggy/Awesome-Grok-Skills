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

## Detailed STRIDE Threat Modeling

### STRIDE Analysis Framework

```python
from security_assessment.security_review import STRIDEAnalyzer

analyzer = STRIDEAnalyzer()

# Define system components for threat modeling
components = analyzer.define_system(
    name="E-Commerce Platform",
    components=[
        {
            "id": "web-frontend",
            "type": "web_application",
            "description": "React SPA serving product catalog and checkout",
            "technologies": ["React", "Node.js", "CDN"],
            "data_processed": ["PII", "payment_data", "session_tokens"],
            "trust_level": "untrusted"
        },
        {
            "id": "api-gateway",
            "type": "api",
            "description": "REST API gateway handling authentication and routing",
            "technologies": ["Kong", "OAuth2", "JWT"],
            "data_processed": ["authentication_tokens", "user_data", "order_data"],
            "trust_level": "semi_trusted"
        },
        {
            "id": "payment-service",
            "type": "microservice",
            "description": "Payment processing service with Stripe integration",
            "technologies": ["Python", "FastAPI", "Stripe API"],
            "data_processed": ["payment_info", "billing_address", "transaction_history"],
            "trust_level": "trusted"
        },
        {
            "id": "user-database",
            "type": "database",
            "description": "PostgreSQL database storing user accounts and orders",
            "technologies": ["PostgreSQL", "pgBouncer"],
            "data_processed": ["credentials", "PII", "order_history"],
            "trust_level": "trusted"
        },
        {
            "id": "message-queue",
            "type": "messaging",
            "description": "RabbitMQ for async order processing",
            "technologies": ["RabbitMQ", "AMQP"],
            "data_processed": ["order_events", "notification_events"],
            "trust_level": "semi_trusted"
        }
    ],
    trust_boundaries=[
        {"id": "internet", "components": ["web-frontend"], "level": "untrusted"},
        {"id": "dmz", "components": ["api-gateway"], "level": "semi_trusted"},
        {"id": "internal", "components": ["payment-service", "user-database", "message-queue"], "level": "trusted"}
    ],
    data_flows=[
        {"from": "web-frontend", "to": "api-gateway", "protocol": "HTTPS", "data": "API requests"},
        {"from": "api-gateway", "to": "payment-service", "protocol": "gRPC", "data": "payment requests"},
        {"from": "payment-service", "to": "user-database", "protocol": "PostgreSQL", "data": "order data"},
        {"from": "payment-service", "to": "message-queue", "protocol": "AMQP", "data": "order events"}
    ]
)

# Run STRIDE analysis
threats = analyzer.analyze(components)

print(f"Threats identified: {len(threats)}")
for threat in threats:
    print(f"\n[{threat.stride_category}] {threat.title}")
    print(f"  Component: {threat.target_component}")
    print(f"  Data flow: {threat.data_flow or 'N/A'}")
    print(f"  Risk rating: {threat.risk_rating}")
    print(f"  Likelihood: {threat.likelihood}")
    print(f"  Impact: {threat.impact}")
    print(f"  Mitigation: {threat.mitigation}")
    print(f"  Attack tree: {threat.attack_tree_id}")
```

### Spoofing Threat Analysis

```python
from security_assessment.security_review import SpoofingAnalyzer

spoofing = SpoofingAnalyzer()

# Analyze authentication mechanisms
auth_analysis = spoofing.analyze_authentication(
    components=[
        {
            "id": "login-endpoint",
            "auth_type": "username_password",
            "mfa_enabled": True,
            "mfa_type": "totp",
            "session_management": "jwt",
            "token_expiry": 3600
        },
        {
            "id": "api-auth",
            "auth_type": "oauth2",
            "flow": "authorization_code",
            "pkce_enabled": True,
            "token_validation": "signature"
        }
    ]
)

print("Authentication Threat Analysis:")
for component in auth_analysis.components:
    print(f"\n  {component.id}:")
    for threat in component.threats:
        print(f"    [{threat.severity}] {threat.title}")
        print(f"      Attack: {threat.attack_description}")
        print(f"      Mitigation: {threat.mitigation}")

# Analyze session management
session_analysis = spoofing.analyze_session_management(
    session_config={
        "token_type": "jwt",
        "algorithm": "RS256",
        "expiry_seconds": 3600,
        "refresh_token_enabled": True,
        "session_fixation_protection": True,
        "cookie_flags": {"httponly": True, "secure": True, "samesite": "strict"}
    }
)

print(f"\nSession Security Assessment:")
for finding in session_analysis.findings:
    print(f"  [{finding.severity}] {finding.title}")
    print(f"    Issue: {finding.description}")
    print(f"    Fix: {finding.recommendation}")
```

## Attack Tree Construction

### Building Attack Trees

```python
from security_assessment.security_review import AttackTreeBuilder

builder = AttackTreeBuilder()

# Build attack tree for account takeover
ato_tree = builder.build_tree(
    goal="Compromise user account",
    methods=[
        {
            "id": "m1",
            "name": "Credential Stuffing",
            "preconditions": ["valid_email", "weak_password"],
            "steps": [
                "Obtain credential list from breach database",
                "Automate login attempts with credential pairs",
                "Bypass rate limiting (IP rotation, distributed)",
                "Access account with valid credentials"
            ],
            "detection_difficulty": "low",
            "cost": "low",
            "success_probability": 0.15
        },
        {
            "id": "m2",
            "name": "Session Hijacking",
            "preconditions": ["active_session", "xss_vulnerability"],
            "steps": [
                "Discover reflected XSS in application",
                "Craft payload to exfiltrate session cookie",
                "Deliver payload via phishing or stored XSS",
                "Use stolen session token to access account"
            ],
            "detection_difficulty": "medium",
            "cost": "medium",
            "success_probability": 0.25
        },
        {
            "id": "m3",
            "name": "Password Reset Abuse",
            "preconditions": ["valid_email", "weak_reset_token"],
            "steps": [
                "Initiate password reset for target account",
                "Intercept or predict reset token",
                "Use token to set new password",
                "Access account with new credentials"
            ],
            "detection_difficulty": "medium",
            "cost": "low",
            "success_probability": 0.30
        }
    ],
    attack_paths=[
        {"path": ["m1"], "probability": 0.15, "impact": "high"},
        {"path": ["m2"], "probability": 0.25, "impact": "high"},
        {"path": ["m3"], "probability": 0.30, "impact": "high"},
        {"path": ["m1", "m2"], "probability": 0.04, "impact": "critical"}
    ]
)

print("Attack Tree Analysis:")
print(f"Goal: {ato_tree.goal}")
print(f"Total attack methods: {len(ato_tree.methods)}")
print(f"Overall success probability: {ato_tree.overall_probability:.1%}")

for method in ato_tree.methods:
    print(f"\n  Method: {method.name}")
    print(f"    Probability: {method.success_probability:.0%}")
    print(f"    Cost: {method.cost}")
    print(f"    Detection difficulty: {method.detection_difficulty}")
    for step in method.steps:
        print(f"      → {step}")

for path in ato_tree.attack_paths:
    print(f"\n  Attack Path: {' → '.join(path['path'])}")
    print(f"    Combined probability: {path['probability']:.1%}")
    print(f"    Impact: {path['impact']}")
```

## Code Review Checklists

### Python Security Review Checklist

```python
from security_assessment.security_review import CodeReviewChecklist

checklist = CodeReviewChecklist(language="python")

# Define review checklist items
python_checklist = checklist.get_items(categories=[
    "input_validation",
    "authentication",
    "authorization",
    "cryptography",
    "error_handling",
    "logging",
    "serialization",
    "dependencies"
])

for category, items in python_checklist.items():
    print(f"\n## {category.replace('_', ' ').title()}")
    for item in items:
        print(f"  [ ] {item.description}")
        print(f"      Risk: {item.risk}")
        print(f"      Check: {item.verification_method}")
        if item.example_bad:
            print(f"      Bad:  {item.example_bad}")
        if item.example_good:
            print(f"      Good: {item.example_good}")
```

### JavaScript/Node.js Security Review Checklist

```javascript
// security-review-checklist.js
const checklist = {
  authentication: [
    {
      id: "AUTH-001",
      description: "Verify JWT tokens use strong algorithms (RS256/ES256, not HS256)",
      risk: "critical",
      pattern: /algorithm.*HS256|verify.*algorithm/,
      remediation: "Use RS256 or ES256 with proper key management"
    },
    {
      id: "AUTH-002",
      description: "Check for hardcoded secrets in source code",
      risk: "critical",
      pattern: /password\s*=\s*['"][^'"]+['"]|secret\s*=\s*['"][^'"]+['"]/,
      remediation: "Use environment variables or secret management"
    },
    {
      id: "AUTH-003",
      description: "Verify session cookies have secure flags",
      risk: "high",
      pattern: /cookie.*httpOnly|cookie.*secure|cookie.*sameSite/,
      remediation: "Set httpOnly, secure, and sameSite flags on cookies"
    }
  ],
  input_validation: [
    {
      id: "INPUT-001",
      description: "Check for SQL injection vulnerabilities",
      risk: "critical",
      pattern: /query\(`[^`]*\$\{|query\('[^']*'\s*\+/,
      remediation: "Use parameterized queries or ORM"
    },
    {
      id: "INPUT-002",
      description: "Check for command injection",
      risk: "critical",
      pattern: /exec\(|spawn\([^)]*\+/,
      remediation: "Use spawn with array arguments, avoid shell=true"
    },
    {
      id: "INPUT-003",
      description: "Check for path traversal",
      risk: "high",
      pattern: /readFile\([^)]*\+|path\.join\([^)]*\+/,
      remediation: "Validate and sanitize file paths, use allowlists"
    }
  ],
  serialization: [
    {
      id: "SER-001",
      description: "Check for prototype pollution",
      risk: "critical",
      pattern: /Object\.assign\(|\.\.\.req\.body|\$\.extend\(/,
      remediation: "Sanitize input objects, use Object.create(null) for maps"
    },
    {
      id: "SER-002",
      description: "Check for unsafe deserialization",
      risk: "critical",
      pattern: /JSON\.parse\([^)]*req|eval\([^)]*JSON/,
      remediation: "Validate deserialized data against schema"
    }
  ]
};
```

## Secure Design Patterns

### Authentication Design Patterns

```python
from security_assessment.security_review import SecureDesignPatterns

patterns = SecureDesignPatterns()

# Validate authentication implementation
auth_validation = patterns.validate_authentication(
    implementation={
        "password_hashing": {
            "algorithm": "argon2id",
            "memory_cost": 65536,
            "time_cost": 3,
            "parallelism": 4,
            "salt_length": 16
        },
        "mfa": {
            "enabled": True,
            "methods": ["totp", "webauthn"],
            "backup_codes": True,
            "enforcement_policy": "all_admin_users"
        },
        "session_management": {
            "token_type": "jwt",
            "algorithm": "RS256",
            "expiry_seconds": 3600,
            "refresh_token_expiry": 86400,
            "concurrent_sessions_allowed": 5
        },
        "account_lockout": {
            "enabled": True,
            "max_attempts": 5,
            "lockout_duration_seconds": 900,
            "reset_counter_after": 1800
        }
    }
)

print("Authentication Design Validation:")
for check in auth_validation.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"  [{status}] {check.name}: {check.description}")
    if not check.passed:
        print(f"    Issue: {check.issue}")
        print(f"    Fix: {check.recommendation}")
```

### Authorization Design Patterns

```python
from security_assessment.security_review import AuthorizationPatterns

authz = AuthorizationPatterns()

# Validate RBAC implementation
rbac_validation = authz.validate_rbac(
    roles_definition={
        "admin": {
            "permissions": ["*"],
            "constraints": ["ip_whitelist", "mfa_required"]
        },
        "editor": {
            "permissions": ["read:*", "write:own", "delete:own"],
            "constraints": ["mfa_required"]
        },
        "viewer": {
            "permissions": ["read:public", "read:own"],
            "constraints": []
        }
    },
    enforcement_points=[
        "api_gateway",
        "service_layer",
        "data_layer"
    ]
)

print("RBAC Validation:")
for check in rbac_validation.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"  [{status}] {check.name}")
    if not check.passed:
        print(f"    Issue: {check.issue}")

# Validate ABAC implementation
abac_validation = authz.validate_abac(
    policy_engine="opa",
    policies=[
        {
            "name": "data-access-policy",
            "description": "Control access to data based on classification",
            "rules": [
                "allow if subjectClearance >= resourceClassification",
                "deny if subject.dept != resource.ownerDept and resource.classification >= 'confidential'"
            ]
        }
    ]
)

print("\nABAC Validation:")
for check in abac_validation.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"  [{status}] {check.name}")
```

## Threat Intelligence Integration

### Mapping Threats to MITRE ATT&CK

```python
from security_assessment.security_review import ThreatIntelMapper

mapper = ThreatIntelMapper()

# Map identified threats to ATT&CK
attack_mapping = mapper.map_to_attack(
    threats=identified_threats,
    include_sub_techniques=True,
    confidence_threshold=0.7
)

print("MITRE ATT&CK Mapping:")
for threat in attack_mapping.threats:
    print(f"\n  {threat.title}")
    print(f"    ATT&CK Technique: {threat.technique_id} — {threat.technique_name}")
    print(f"    Tactic: {threat.tactic}")
    print(f"    Confidence: {threat.confidence:.0%}")
    print(f"    Detection: {threat.detection_guidance}")
    print(f"    Mitigation: {threat.mitigation_id}")

# Get detection recommendations
detection_recs = mapper.get_detection_recommendations(
    techniques=attack_mapping.techniques,
    data_sources=["network_traffic", "process_creation", "file_modification", "authentication_logs"]
)

print("\nDetection Recommendations:")
for rec in detection_recs:
    print(f"\n  Technique: {rec.technique}")
    print(f"    Data source: {rec.data_source}")
    print(f"    Detection rule: {rec.rule_description}")
    print(f"    Query: {rec.query}")
    print(f"    False positive rate: {rec.fp_rate}")
```

## Developer Feedback Loop

### Automated Security Feedback

```python
from security_assessment.security_review import DeveloperFeedback

feedback = DeveloperFeedback(
    repository="acme-corp/ecommerce-api",
    branch="feature/checkout"
)

# Analyze pull request for security issues
pr_analysis = feedback.analyze_pr(
    pr_number=1234,
    files_changed=["src/api/checkout.py", "src/services/payment.py"],
    review_focus=["injection", "auth", "crypto", "secrets"]
)

print(f"PR Security Analysis: #{pr_analysis.pr_number}")
print(f"  Files reviewed: {pr_analysis.files_reviewed}")
print(f"  Security issues found: {pr_analysis.issue_count}")

for issue in pr_analysis.issues:
    print(f"\n  [{issue.severity}] {issue.title}")
    print(f"    File: {issue.file}:{issue.line}")
    print(f"    Rule: {issue.rule_id}")
    print(f"    Issue: {issue.description}")
    print(f"    Suggestion: {issue.suggestion}")
    if issue.secure_example:
        print(f"    Secure code:")
        for line in issue.secure_example.split('\n'):
            print(f"      {line}")

# Generate educational feedback
education = feedback.generate_educational_feedback(
    issues=pr_analysis.issues,
    developer_experience="mid-level",
    format="inline_comment"
)

for comment in education.comments:
    print(f"\n  Comment on {comment.file}:{comment.line}:")
    print(f"    {comment.text}")
```

## Testing Examples

### Unit Tests for Threat Modeling

```python
import pytest
from security_assessment.security_review import STRIDEAnalyzer, ThreatModeler

class TestSTRIDEAnalyzer:
    def setup_method(self):
        self.analyzer = STRIDEAnalyzer()

    def test_spoofing_detection(self):
        component = {
            "id": "auth-service",
            "type": "authentication",
            "mfa_enabled": False,
            "session_fixation_protection": False
        }
        threats = self.analyzer.analyze_component(component)
        spoofing_threats = [t for t in threats if t.category == "spoofing"]
        assert len(spoofing_threats) > 0

    def test_tampering_detection(self):
        component = {
            "id": "api-endpoint",
            "type": "api",
            "input_validation": False,
            "parameterized_queries": False
        }
        threats = self.analyzer.analyze_component(component)
        tampering_threats = [t for t in threats if t.category == "tampering"]
        assert len(tampering_threats) > 0

    def test_information_disclosure_detection(self):
        component = {
            "id": "error-handler",
            "type": "error_handling",
            "stack_traces_enabled": True,
            "debug_mode": True
        }
        threats = self.analyzer.analyze_component(component)
        disclosure_threats = [t for t in threats if t.category == "information_disclosure"]
        assert len(disclosure_threats) > 0

    def test_elevation_of_privilege_detection(self):
        component = {
            "id": "admin-panel",
            "type": "web_application",
            "rbac_enabled": False,
            "authorization_checked": False
        }
        threats = self.analyzer.analyze_component(component)
        eop_threats = [t for t in threats if t.category == "elevation_of_privilege"]
        assert len(eop_threats) > 0

class TestAttackTree:
    def setup_method(self):
        self.builder = AttackTreeBuilder()

    def test_attack_probability_calculation(self):
        tree = self.builder.build_tree(
            goal="Data breach",
            methods=[
                {"id": "m1", "probability": 0.3},
                {"id": "m2", "probability": 0.2}
            ],
            attack_paths=[
                {"path": ["m1"], "probability": 0.3},
                {"path": ["m2"], "probability": 0.2},
                {"path": ["m1", "m2"], "probability": 0.06}
            ]
        )
        assert tree.overall_probability > 0
        assert tree.overall_probability <= 1.0

    def test_mitigation_impact(self):
        tree = self.builder.build_tree(
            goal="Account takeover",
            methods=[{"id": "m1", "probability": 0.5}]
        )
        mitigated = tree.apply_mitigation(
            method_id="m1",
            effectiveness=0.9
        )
        assert mitigated.methods[0].probability == 0.05
```

## References

- OWASP Application Security Verification Standard (ASVS)
- Microsoft Threat Modeling Tool Documentation
- STRIDE Threat Model — Microsoft Security Development Lifecycle
- PASTA — Process for Attack Simulation and Threat Analysis
- CWE — Common Weakness Enumeration
- NIST SP 800-53 Rev 5 — Security and Privacy Controls
- BSIMM — Building Security In Maturity Model
- SANS Secure Coding Principles
