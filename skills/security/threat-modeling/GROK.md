---
name: "threat-modeling"
category: "security"
version: "2.0.0"
tags: ["security", "threat-modeling", "STRIDE", "DREAD", "PASTA", "attack-surface", "attack-trees", "risk-assessment"]
---

# Threat Modeling

## Overview

Threat modeling is a structured, proactive approach to identifying, quantifying, and mitigating security risks before code is deployed or systems are compromised. It answers four fundamental questions: What are we building? What can go wrong? What are we going to do about it? Did we do a good job? This module implements the major threat modeling frameworks — STRIDE, DREAD, PASTA, LINDDUN, and attack tree analysis — as systematic, repeatable processes that can be automated and integrated into development workflows.

Threat modeling is most effective early in the SDLC when architectural changes are cheap, but it remains valuable at any stage for identifying gaps that automated scanning cannot find. Unlike vulnerability scanning (which discovers known weaknesses in implemented code), threat modeling discovers design-level flaws that entire categories of testing miss. A system can pass every SAST/DAST scan and still have a critical design flaw that allows privilege escalation — threat modeling catches these architectural gaps.

This module provides tooling for data flow diagram (DFD) decomposition, STRIDE threat classification, DREAD/CVSS risk scoring, attack tree construction, PASTA threat analysis, attack surface quantification, and mitigation mapping. It bridges the gap between theoretical threat modeling frameworks and practical, automatable workflows. Every identified threat maps to specific mitigations: architectural changes, secure coding practices, monitoring, or documented risk acceptance. The module is designed for collaborative use — developers, architects, security engineers, and operations staff all see different threat surfaces, and the tooling supports multi-stakeholder threat modeling sessions.

## Core Capabilities

1. **Data Flow Diagram (DFD) Decomposition** — Model systems as processes, data stores, external entities, trust boundaries, and data flows. Identify every point where data crosses a security boundary. Automatic generation of DFDs from infrastructure-as-code (Terraform, CloudFormation) and architecture diagrams.

2. **STRIDE Threat Classification** — Systematically classify threats into six categories: Spoofing (identity), Tampering (integrity), Repudiation (non-repudiation), Information Disclosure (confidentiality), Denial of Service (availability), Elevation of Privilege (authorization). Each category maps to specific mitigations and testing patterns.

3. **Risk Scoring (DREAD / CVSS)** — Quantify threat severity using Damage, Reproducibility, Exploitability, Affected Users, Discoverability (DREAD) or Common Vulnerability Scoring System (CVSS) v3.1 for consistent prioritization across teams and time.

4. **PASTA Threat Analysis** — Process for Attack Simulation and Threat Analysis — a seven-stage risk-centric methodology that models the attacker's perspective, identifies attack patterns, and maps vulnerabilities to business impact.

5. **Attack Tree Analysis** — Model adversary goals as hierarchical tree structures with AND/OR nodes. Identify cheapest attack paths, compute composite risk scores, and determine the minimum-cost attack that achieves the attacker's objective.

6. **LINDDUN Privacy Threat Modeling** — Privacy-specific threat modeling covering Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, and Non-compliance with respect to privacy regulations.

7. **Attack Surface Quantification** — Measure and track the total exposed entry points, protocol count, authentication mechanisms, data sensitivity levels, and trust boundary crossings across the system. Track changes over time.

8. **Mitigation Mapping & Tracking** — Link each identified threat to specific controls: architectural changes, secure coding practices, monitoring/alerting, or documented risk acceptance with justification and expiration dates.

9. **Threat Intelligence Integration** — Correlate identified threats with MITRE ATT&CK techniques, known CVEs, and industry-specific threat actor TTPs to prioritize based on real-world attack likelihood.

10. **Living Threat Model Management** — Version-controlled threat models that evolve with the system. Track threat lifecycle from identification through mitigation to closure, with automated triggers for re-evaluation on architecture changes.

## Usage Examples

### STRIDE Threat Analysis

```python
from threat_modeling import STRIDEAnalyzer, TrustBoundary, SystemComponent

# Define system components with trust levels
components = [
    SystemComponent("WebApp", type="process", trust_level="semi-trusted",
                    data_classes=["pii", "session_tokens"]),
    SystemComponent("APIGateway", type="process", trust_level="trusted",
                    data_classes=["auth_tokens", "request_logs"]),
    SystemComponent("Database", type="datastore", trust_level="internal",
                    data_classes=["pii", "credentials", "financial"]),
    SystemComponent("UserBrowser", type="external_entity", trust_level="untrusted"),
    SystemComponent("ThirdPartyAPI", type="external_entity", trust_level="untrusted",
                    data_classes=["webhooks"]),
    SystemComponent("MessageQueue", type="datastore", trust_level="internal",
                    data_classes=["event_payloads"]),
]

# Define trust boundaries where data crosses security levels
boundaries = [
    TrustBoundary("Internet", components=["UserBrowser", "WebApp"],
                  controls=["TLS 1.3", "WAF", "Rate Limiting"]),
    TrustBoundary("DMZ", components=["WebApp", "APIGateway"],
                  controls=["mTLS", "API Key Validation"]),
    TrustBoundary("Internal", components=["APIGateway", "Database"],
                  controls=["Network Policy", "IAM Auth"]),
    TrustBoundary("External Integration", components=["APIGateway", "ThirdPartyAPI"],
                  controls=["OAuth 2.0", "IP Allowlist"]),
]

analyzer = STRIDEAnalyzer(components, boundaries)
threats = analyzer.analyze()

# Generate report with mitigation mapping
for threat in threats:
    print(f"[{threat.category}] {threat.description}")
    print(f"  Component:  {threat.component}")
    print(f"  Boundary:   {threat.boundary_crossed}")
    print(f"  Severity:   {threat.severity}")
    print(f"  Mitigation: {threat.recommended_mitigation}")
    print()
```

### Attack Tree Construction and Analysis

```python
from threat_modeling import AttackTree, AttackNode, GoalNode

tree = AttackTree(root=GoalNode(
    goal="Exfiltrate customer PII from production database",
    attacker="External ( financially motivated)",
    children=[
        AttackNode(method="SQL Injection on search endpoint",
                   cost="low", success_probability=0.6,
                   detection_probability=0.3,
                   children=[
                       AttackNode(method="Bypass WAF via double-encoding", cost="medium",
                                  success_probability=0.7),
                       AttackNode(method="Use UNION-based extraction", cost="low",
                                  success_probability=0.8),
                       AttackNode(method="Time-based blind extraction", cost="low",
                                  success_probability=0.5),
                   ]),
        AttackNode(method="Compromise admin credentials",
                   cost="medium", success_probability=0.3,
                   detection_probability=0.5,
                   children=[
                       AttackNode(method="Credential stuffing with leaked lists", cost="low",
                                  success_probability=0.4),
                       AttackNode(method="Phishing campaign targeting admins", cost="medium",
                                  success_probability=0.3),
                       AttackNode(method="MFA bypass via SIM swapping", cost="high",
                                  success_probability=0.2),
                   ]),
        AttackNode(method="SSRF via webhook integration",
                   cost="low", success_probability=0.4,
                   detection_probability=0.2,
                   children=[
                       AttackNode(method="Access cloud metadata service", cost="low",
                                  success_probability=0.7),
                       AttackNode(method="Pivot to internal database", cost="medium",
                                  success_probability=0.3),
                   ]),
        AttackNode(method="Supply chain compromise via dependency",
                   cost="high", success_probability=0.1,
                   detection_probability=0.1),
    ]
))

# Find cheapest attack path (lowest cost that achieves the goal)
cheapest = tree.cheapest_path()
print(f"Cheapest attack path: {cheapest}")
print(f"  Cost: {cheapest.total_cost}")
print(f"  Success probability: {cheapest.composite_probability:.1%}")
print(f"  Risk score: {cheapest.risk_score}")

# Find path with highest success probability
most_reliable = tree.most_reliable_path()
print(f"\nMost reliable path: {most_reliable}")
print(f"  Success probability: {most_reliable.composite_probability:.1%}")

# Find path least likely to be detected
stealthiest = tree.stealthiest_path()
print(f"\nStealthiest path: {stealthiest}")
print(f"  Detection probability: {stealthiest.composite_detection:.1%}")
```

### DREAD Risk Scoring with Aggregation

```python
from threat_modeling import DREADScorer, Threat, RiskMatrix

# Define threats identified during modeling session
threats = [
    Threat(name="SQL Injection in login", component="AuthService",
           category="Elevation of Privilege"),
    Threat(name="Stored XSS in user profile", component="ProfilePage",
           category="Tampering"),
    Threat(name="SSRF via webhook callback", component="Integrations",
           category="Information Disclosure"),
    Threat(name="Session fixation after login", component="SessionManager",
           category="Spoofing"),
    Threat(name="Unrestricted file upload", component="FileService",
           category="Elevation of Privilege"),
]

scorer = DREADScorer()

# Score each threat (1-10 scale for each DREAD factor)
scores = {
    "SQL Injection in login": {"damage": 10, "reproducibility": 8,
                               "exploitability": 7, "affected_users": 10,
                               "discoverability": 6},
    "Stored XSS in user profile": {"damage": 6, "reproducibility": 9,
                                   "exploitability": 8, "affected_users": 7,
                                   "discoverability": 7},
    "SSRF via webhook callback": {"damage": 8, "reproducibility": 6,
                                  "exploitability": 5, "affected_users": 5,
                                  "discoverability": 4},
    "Session fixation after login": {"damage": 7, "reproducibility": 8,
                                     "exploitability": 6, "affected_users": 9,
                                     "discoverability": 5},
    "Unrestricted file upload": {"damage": 9, "reproducibility": 9,
                                 "exploitability": 7, "affected_users": 8,
                                 "discoverability": 8},
}

# Generate risk matrix
risk_matrix = RiskMatrix()

for threat in threats:
    result = scorer.score(threat.name, scores[threat.name])
    risk_matrix.add(threat, result)
    print(f"{threat.name}: DREAD = {result.average:.1f} ({result.risk_level})")
    print(f"  Component: {threat.component}")
    print(f"  Category:  {threat.category}")
    print()

# Print prioritized risk summary
print("=== Risk Matrix Summary ===")
print(risk_matrix.summary())
print(f"\nCritical: {risk_matrix.count_by_level('critical')}")
print(f"High:     {risk_matrix.count_by_level('high')}")
print(f"Medium:   {risk_matrix.count_by_level('medium')}")
print(f"Low:      {risk_matrix.count_by_level('low')}")
```

### PASTA Threat Analysis

```python
from threat_modeling import PASTAAnalyzer, BusinessContext, TechnicalModel

# Stage 1: Define business context
business = BusinessContext(
    application="E-Commerce Platform",
    business_objectives=["Revenue generation", "Customer trust", "Regulatory compliance"],
    data_sensitivity={
        "payment_cards": "critical",
        "customer_pii": "high",
        "browsing_history": "medium",
        "public_catalog": "low"
    },
    regulatory_requirements=["PCI DSS", "GDPR", "CCPA"]
)

# Stage 2: Define technical model
tech_model = TechnicalModel(
    components=["WebApp", "API", "PaymentGateway", "Database", "CDN"],
    protocols=["HTTPS", "gRPC", "PostgreSQL"],
    trust_boundaries=["Internet/DMZ", "DMZ/Internal", "Internal/Payment"]
)

# Stage 3-7: Run PASTA analysis
analyzer = PASTAAnalyzer(business, tech_model)
results = analyzer.analyze()

# Get attack scenarios with business impact
for scenario in results.attack_scenarios:
    print(f"Attack: {scenario.attack_name}")
    print(f"  STRIDE: {scenario.stride_category}")
    print(f"  Business Impact: {scenario.business_impact}")
    print(f"  Exploitability: {scenario.exploitability}")
    print(f"  Risk: {scenario.risk_score}")
    print(f"  Mitigation: {scenario.mitigation}")
    print()
```

### Attack Surface Report

```python
from threat_modeling import AttackSurfaceAnalyzer, AssetInventory

inventory = AssetInventory()
inventory.add_asset("web-prod-01", type="server", os="Ubuntu 22.04",
                    public_facing=True, data_classification="high")
inventory.add_asset("db-prod-01", type="database", os="Ubuntu 22.04",
                    public_facing=False, data_classification="critical")
inventory.add_asset("api-gateway", type="load-balancer", os="AL2023",
                    public_facing=True, data_classification="medium")

analyzer = AttackSurfaceAnalyzer(inventory)
surface = analyzer.analyze()

print(f"Total exposed endpoints: {surface.endpoint_count}")
print(f"Authentication mechanisms: {surface.auth_mechanisms}")
print(f"Protocols in use: {surface.protocols}")
print(f"Trust boundary crossings: {surface.trust_boundary_count}")
print(f"Data sensitivity score: {surface.sensitivity_score}/10")

# Track surface changes over time
previous_surface = analyzer.load_snapshot("2024-01-01")
changes = analyzer.diff(previous_surface)
print(f"\nNew endpoints since last review: {len(changes.new_endpoints)}")
print(f"Removed endpoints: {len(changes.removed_endpoints)}")
print(f"Changed configurations: {len(changes.config_changes)}")
```

## Architecture

The threat modeling module follows a four-phase iterative architecture:

```
┌──────────────────────────────────────────────────────────┐
│                  Phase 1: DECOMPOSE                       │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Data Flow    │  │  Asset       │  │  Trust        │  │
│  │  Diagrams     │  │  Inventory   │  │  Boundaries   │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘  │
│         └──────────────────┼──────────────────┘          │
│                            │                             │
└────────────────────────────┼─────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────┐
│                  Phase 2: IDENTIFY                        │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  STRIDE  │  │  PASTA   │  │  Attack  │  │  LINDDUN │ │
│  │  Analysis│  │  Analysis│  │  Trees   │  │  Privacy │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       └──────────────┼────────────┼──────────────┘       │
│                      │            │                      │
└──────────────────────┼────────────┼──────────────────────┘
                       │            │
┌──────────────────────▼────────────▼──────────────────────┐
│                  Phase 3: EVALUATE                        │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  DREAD /     │  │  Risk        │  │  MITRE ATT&CK │  │
│  │  CVSS Scoring│  │  Matrix      │  │  Mapping      │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘  │
│         └──────────────────┼──────────────────┘          │
│                            │                             │
└────────────────────────────┼─────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────┐
│                  Phase 4: ADDRESS                         │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Mitigation  │  │  Risk        │  │  Living       │  │
│  │  Mapping     │  │  Acceptance  │  │  Threat Model │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Model early and often** — Perform threat modeling during design, not after implementation. Revisit the threat model whenever architecture changes. A threat model created after deployment is an audit artifact, not a security tool.

2. **Decompose the system completely** — Missed components are missed threats. Include all external services, shared libraries, infrastructure components, third-party APIs, and CDNs. If it touches data, it's in scope.

3. **Use multiple frameworks** — STRIDE catches design flaws, attack trees catch adversary strategy, DREAD catches prioritization gaps, PASTA catches business impact misalignment. No single framework catches everything.

4. **Include the whole team** — Developers, architects, security engineers, QA, and operations staff all see different threat surfaces. Facilitate collaborative sessions rather than security-team-only analysis.

5. **Document assumptions explicitly** — Record trust boundaries, data classification levels, security requirements, and architectural assumptions. Undocumented assumptions are the most common source of missed threats.

6. **Map every threat to a mitigation** — Every identified threat must have a response: mitigate with a specific control, transfer via insurance, accept with documented justification and expiration, or avoid by removing the feature.

7. **Quantify risk consistently** — Use DREAD, CVSS, or FAIR to assign numeric scores. Without quantification, teams argue about severity instead of addressing it. Consistent scoring enables data-driven prioritization.

8. **Maintain a living threat model** — Threat models should be version-controlled, updated with each sprint, and re-evaluated when new features add attack surface. A stale threat model is worse than no threat model — it creates false confidence.

9. **Validate threat models with testing** — Use the threat model to drive security testing. Each identified threat should have a corresponding test case. If you can't test for a threat, you can't verify the mitigation works.

10. **Track threats across the full lifecycle** — From identification through implementation of controls to verification and closure. Threats that are "mitigated" but never verified are not truly mitigated.

## Performance Considerations

- **STRIDE analysis**: Manual STRIDE analysis takes 2-4 hours per system component. Automated STRIDE analysis reduces this to minutes but requires accurate DFD input.
- **Attack tree computation**: Composite risk scoring on large attack trees (>100 nodes) takes seconds. Tree construction and review is the time bottleneck, not computation.
- **DREAD scoring**: Scoring is inherently manual and subjective (5-15 minutes per threat). Use calibration exercises to improve consistency across reviewers.
- **PASTA analysis**: Full seven-stage PASTA analysis takes 1-2 days per application. Use abbreviated PASTA for lower-risk systems.
- **Attack surface scanning**: Automated attack surface analysis completes in minutes for most applications. Manual verification of findings takes additional time.
- **Threat intelligence correlation**: MITRE ATT&CK mapping is fast (<1 second per threat) but requires up-to-date technique databases.

## Security Considerations

- **Avoid security theater**: Threat modeling is not a compliance checkbox. It must be performed by people who understand the system and the threat landscape. Automated tools assist but cannot replace human judgment.
- **Don't miss the supply chain**: Third-party libraries, containers, cloud services, and CI/CD pipelines are all part of the threat surface. Include them in your DFD.
- **Consider insider threats**: STRIDE and attack trees typically model external attackers. Don't forget malicious insiders, compromised credentials, and social engineering.
- **Account for deployment context**: The same application has different threat profiles in development, staging, and production. Model each environment separately.
- **Privacy threats are distinct**: Use LINDDUN or similar privacy-specific framework alongside STRIDE. Privacy violations can occur without security breaches (e.g., authorized data aggregation).

## Related Modules

- **secure-coding** — Implement the mitigations identified in threat models
- **security-architecture** — Design systems with threat model outputs as architectural requirements
- **vulnerability-management** — Verify that identified threats are actually mitigated through scanning
- **compliance** — Demonstrate threat modeling to auditors (SOC 2, ISO 27001, PCI DSS)
- **hunt-ato** — Account takeover threat modeling with real attack patterns
- **hunt-ssrf** — SSRF threat modeling with bypass techniques
- **offensive-osint** — Reconnaissance data that feeds threat model attacker profiles

## References

- Microsoft Threat Modeling Tool: https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool
- OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling
- STRIDE威胁模型: https://en.wikipedia.org/wiki/STRIDE_(security)
- PASTA Threat Modeling: https://www.toreon.com/pasta-process-for-attack-simulation-and-threat-analysis/
- LINDDUN Privacy Threat Modeling: https://www.privacyengineering.eu/linddun/
- MITRE ATT&CK Framework: https://attack.mitre.org/
- NIST SP 800-30 (Risk Assessment): https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final
- Threat Modeling: Designing for Security (Adam Shostack): https://threatmodelingbook.com/
- DREAD Risk Rating: https://en.wikipedia.org/wiki/DREAD_(rating_system)
- CVSS v3.1 Specification: https://www.first.org/cvss/v3.1/specification-document

---

## STRIDE Threat Classification Deep Dive

### Spoofing Threat Analysis

```python
from threat_modeling import SpoofingAnalyzer, AuthenticationFlow

analyzer = SpoofingAnalyzer()

# Analyze authentication flow for spoofing vectors
auth_flow = AuthenticationFlow(
    components=["Client", "LoadBalancer", "AuthService", "SessionStore", "Database"],
    protocols=["HTTPS", "JWT", "Redis"],
    authentication_methods=["password", "mfa", "sso"],
)

spoofing_vectors = analyzer.analyze(auth_flow)

for vector in spoofing_vectors:
    print(f"[Spoofing] {vector.description}")
    print(f"  Target: {vector.target_component}")
    print(f"  Method: {vector.attack_method}")
    print(f"  Likelihood: {vector.likelihood}/10")
    print(f"  Impact: {vector.impact}/10")
    print(f"  Mitigation: {vector.mitigation}")
    print()

# Example spoofing threats identified
example_threats = [
    {
        "description": "JWT token forgery using weak signing key",
        "target": "AuthService",
        "method": "Attacker forges JWT with admin claims using known weak HMAC key",
        "likelihood": 6,
        "impact": 10,
        "mitigation": "Use RS256 asymmetric signing, rotate keys regularly, validate all claims",
        "test_case": "Attempt JWT forgery with common weak secrets",
    },
    {
        "description": "Session fixation via cookie manipulation",
        "target": "SessionStore",
        "method": "Attacker sets victim's session cookie before authentication",
        "likelihood": 5,
        "impact": 8,
        "mitigation": "Regenerate session ID on authentication, use Secure/HttpOnly/SameSite flags",
        "test_case": "Attempt to set session cookie before login and verify regeneration",
    },
    {
        "description": "DNS spoofing to redirect API calls",
        "target": "Client",
        "method": "Attacker poisons DNS cache to redirect API calls to malicious server",
        "likelihood": 3,
        "impact": 9,
        "mitigation": "Certificate pinning, DNSSEC, validate server certificate in client",
        "test_case": "Test certificate validation in client applications",
    },
]
```

### Tampering Threat Analysis

```python
from threat_modeling import TamperingAnalyzer, DataFlow

analyzer = TamperingAnalyzer()

# Analyze data flow for tampering vectors
data_flows = [
    DataFlow(
        name="User Profile Update",
        source="Client",
        destination="Database",
        intermediate=["APIGateway", "AuthService", "Application"],
        data_class="pii",
        protocol="HTTPS",
        storage_encryption="AES-256-GCM",
    ),
    DataFlow(
        name="Payment Processing",
        source="Client",
        destination="PaymentGateway",
        intermediate=["APIGateway", "PaymentService"],
        data_class="pci",
        protocol="TLS 1.3",
        storage_encryption="AES-256-GCM",
    ),
    DataFlow(
        name="Log Shipping",
        source="Application",
        destination="ELK",
        intermediate=["LogAgent", "Kafka"],
        data_class="internal",
        protocol="mTLS",
        storage_encryption=None,
    ),
]

for flow in data_flows:
    tampering_vectors = analyzer.analyze_flow(flow)
    
    print(f"=== Tampering Analysis: {flow.name} ===")
    for vector in tampering_vectors:
        print(f"  [{vector.category}] {vector.description}")
        print(f"    Target: {vector.target}")
        print(f"    Method: {vector.method}")
        print(f"    Mitigation: {vector.mitigation}")
    print()
```

### Information Disclosure Threat Analysis

```python
from threat_modeling import InfoDisclosureAnalyzer, SensitiveDataMap

analyzer = InfoDisclosureAnalyzer()

# Map sensitive data flows
data_map = SensitiveDataMap(
    data_types=[
        {"name": "password_hash", "classification": "secret", "regulation": "SOC2,PCI-DSS"},
        {"name": "email", "classification": "pii", "regulation": "GDPR,CCPA"},
        {"name": "ssn", "classification": "pii", "regulation": "HIPAA,GDPR"},
        {"name": "api_key", "classification": "secret", "regulation": "SOC2"},
        {"name": "session_token", "classification": "secret", "regulation": "SOC2"},
        {"name": "error_message", "classification": "internal", "regulation": "SOC2"},
        {"name": "stack_trace", "classification": "internal", "regulation": "SOC2"},
    ]
)

disclosure_vectors = analyzer.analyze(data_map)

for vector in disclosure_vectors:
    print(f"[Info Disclosure] {vector.description}")
    print(f"  Data at Risk: {vector.data_type}")
    print(f"  Exposure Point: {vector.exposure_point}")
    print(f"  Disclosure Method: {vector.method}")
    print(f"  Risk Level: {vector.risk_level}")
    print(f"  Mitigation: {vector.mitigation}")
    print()
```

## DREAD Risk Scoring with Calibrated Examples

### DREAD Score Interpretation

```python
from threat_modeling import DREADScorer, DREADFactor

scorer = DREADScorer()

# DREAD factor definitions and scoring guidance
factor_guide = {
    DREADFactor.DAMAGE: {
        "1": "Minimal impact, no data loss",
        "3": "Minor impact, limited data exposure",
        "5": "Moderate impact, some sensitive data exposed",
        "7": "Significant impact, major data breach possible",
        "9": "Severe impact, full system compromise",
        "10": "Catastrophic impact, complete business disruption",
    },
    DREADFactor.REPRODUCIBILITY: {
        "1": "Nearly impossible to reproduce",
        "3": "Difficult to reproduce, race condition",
        "5": "Moderate difficulty, requires specific configuration",
        "7": "Easy to reproduce, common misconfiguration",
        "9": "Very easy, single request exploitation",
        "10": "Trivial, automated exploitation",
    },
    DREADFactor.EXPLOITABILITY: {
        "1": "Extremely difficult, requires advanced skills",
        "3": "Difficult, requires custom exploit development",
        "5": "Moderate, requires some technical skill",
        "7": "Easy, public exploit available",
        "9": "Very easy, point-and-click tools available",
        "10": "Trivial, no tools required",
    },
    DREADFactor.AFFECTED_USERS: {
        "1": "Single user affected",
        "3": "Small group of users (<100)",
        "5": "Moderate number of users (100-1000)",
        "7": "Large number of users (1000-10000)",
        "9": "Most users affected (10000+)",
        "10": "All users affected",
    },
    DREADFactor.DISCOVERABILITY: {
        "1": "Extremely difficult to discover",
        "3": "Difficult, requires source code access",
        "5": "Moderate, requires some reconnaissance",
        "7": "Easy, publicly visible in normal usage",
        "9": "Very easy, obvious in error messages",
        "10": "Trivial, first thing an attacker finds",
    },
}

# Score a threat with calibrated factors
threat_scores = [
    {
        "threat": "SQL Injection in login form",
        "factors": {"damage": 9, "reproducibility": 8, "exploitability": 7, "affected_users": 10, "discoverability": 8},
        "expected_risk": "critical",
    },
    {
        "threat": "XSS in user profile bio",
        "factors": {"damage": 5, "reproducibility": 9, "exploitability": 8, "affected_users": 6, "discoverability": 7},
        "expected_risk": "high",
    },
    {
        "threat": "Information disclosure in debug endpoint",
        "factors": {"damage": 4, "reproducibility": 10, "exploitability": 9, "affected_users": 3, "discoverability": 5},
        "expected_risk": "medium",
    },
    {
        "threat": "Race condition in payment processing",
        "factors": {"damage": 8, "reproducibility": 3, "exploitability": 2, "affected_users": 1, "discoverability": 2},
        "expected_risk": "medium",
    },
]

for item in threat_scores:
    result = scorer.score(item["threat"], item["factors"])
    match = "PASS" if result.risk_level == item["expected_risk"] else "MISMATCH"
    print(f"[{match}] {item['threat']}")
    print(f"  DREAD: {result.average:.1f} | Risk: {result.risk_level} | Expected: {item['expected_risk']}")
    print()
```

## Attack Tree Analysis with Quantitative Methods

### Risk Quantification Using Attack Trees

```python
from threat_modeling import AttackTreeQuantifier, RiskMetric

quantifier = AttackTreeQuantifier()

# Define attack tree for data exfiltration
tree_data = {
    "goal": "Exfiltrate customer database",
    "children": [
        {
            "method": "SQL Injection",
            "type": "OR",
            "cost_usd": 0,
            "time_hours": 1,
            "success_probability": 0.6,
            "detection_probability": 0.3,
            "children": [
                {
                    "method": "Union-based extraction",
                    "cost_usd": 0,
                    "time_hours": 2,
                    "success_probability": 0.8,
                    "detection_probability": 0.2,
                    "children": [],
                },
                {
                    "method": "Time-based blind extraction",
                    "cost_usd": 0,
                    "time_hours": 8,
                    "success_probability": 0.5,
                    "detection_probability": 0.1,
                    "children": [],
                },
            ]
        },
        {
            "method": "Credential compromise",
            "type": "OR",
            "cost_usd": 500,
            "time_hours": 24,
            "success_probability": 0.3,
            "detection_probability": 0.5,
            "children": [
                {
                    "method": "Phishing admin credentials",
                    "cost_usd": 200,
                    "time_hours": 48,
                    "success_probability": 0.4,
                    "detection_probability": 0.6,
                    "children": [],
                },
                {
                    "method": "Credential stuffing",
                    "cost_usd": 100,
                    "time_hours": 4,
                    "success_probability": 0.3,
                    "detection_probability": 0.4,
                    "children": [],
                },
            ]
        },
        {
            "method": "SSRF via webhook",
            "type": "AND",
            "cost_usd": 0,
            "time_hours": 4,
            "success_probability": 0.7,
            "detection_probability": 0.2,
            "children": [
                {
                    "method": "Find SSRF vulnerability",
                    "cost_usd": 0,
                    "time_hours": 2,
                    "success_probability": 0.8,
                    "detection_probability": 0.1,
                    "children": [],
                },
                {
                    "method": "Access cloud metadata for credentials",
                    "cost_usd": 0,
                    "time_hours": 1,
                    "success_probability": 0.9,
                    "detection_probability": 0.1,
                    "children": [],
                },
            ]
        },
    ]
}

# Compute quantitative risk metrics
metrics = quantifier.analyze(tree_data)

print(f"=== Attack Tree Risk Analysis ===")
print(f"Goal: {metrics.goal}")
print(f"\nCheapest Path:")
print(f"  Method: {metrics.cheapest_path.method}")
print(f"  Cost: ${metrics.cheapest_path.total_cost}")
print(f"  Time: {metrics.cheapest_path.total_hours}h")
print(f"  Success: {metrics.cheapest_path.success_probability:.1%}")
print(f"  Detection: {metrics.cheapest_path.detection_probability:.1%}")
print(f"  Risk Score: {metrics.cheapest_path.risk_score:.2f}")

print(f"\nMost Likely Path:")
print(f"  Method: {metrics.most_likely_path.method}")
print(f"  Success: {metrics.most_likely_path.success_probability:.1%}")
print(f"  Risk Score: {metrics.most_likely_path.risk_score:.2f}")

print(f"\nStealthiest Path:")
print(f"  Method: {metrics.stealthiest_path.method}")
print(f"  Detection: {metrics.stealthiest_path.detection_probability:.1%}")
print(f"  Risk Score: {metrics.stealthiest_path.risk_score:.2f}")

print(f"\nOverall Risk:")
print(f"  Composite Score: {metrics.composite_risk_score:.2f}")
print(f"  Risk Level: {metrics.risk_level}")
print(f"  Recommended Priority: {metrics.recommended_priority}")
```

## MITRE ATT&CK Mapping

### Mapping Threats to ATT&CK Techniques

```python
from threat_modeling import ATTCKMapper, ThreatIntelCorrelation

mapper = ATTCKMapper()

# Map STRIDE threats to ATT&CK techniques
threats_with_attack = [
    {
        "stride_category": "Spoofing",
        "description": "Attacker impersonates legitimate user via stolen session token",
        "attck_techniques": [
            {"id": "T1078", "name": "Valid Accounts", "tactic": "Initial Access"},
            {"id": "T1539", "name": "Steal Web Session Cookie", "tactic": "Credential Access"},
        ],
        "likelihood": 7,
        "impact": 8,
    },
    {
        "stride_category": "Elevation of Privilege",
        "description": "Attacker exploits deserialization vulnerability to execute arbitrary code",
        "attck_techniques": [
            {"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution"},
            {"id": "T1203", "name": "Exploitation for Client Execution", "tactic": "Execution"},
        ],
        "likelihood": 5,
        "impact": 10,
    },
    {
        "stride_category": "Information Disclosure",
        "description": "Attacker exfiltrates data via DNS tunneling",
        "attck_techniques": [
            {"id": "T1048", "name": "Exfiltration Over Alternative Protocol", "tactic": "Exfiltration"},
            {"id": "T1071", "name": "Application Layer Protocol", "tactic": "Command and Control"},
        ],
        "likelihood": 3,
        "impact": 9,
    },
    {
        "stride_category": "Denial of Service",
        "description": "Attacker performs resource exhaustion via API abuse",
        "attck_techniques": [
            {"id": "T1499", "name": "Endpoint Denial of Service", "tactic": "Impact"},
            {"id": "T1498", "name": "Network Denial of Service", "tactic": "Impact"},
        ],
        "likelihood": 6,
        "impact": 6,
    },
]

# Correlate with threat intelligence
correlation = ATTCKMapper.correlate_threats(threats_with_attack)

for threat in correlation:
    print(f"[{threat['stride_category']}] {threat['description']}")
    for technique in threat['attck_techniques']:
        print(f"  ATT&CK: {technique['id']} - {technique['name']}")
        print(f"  Tactic: {technique['tactic']}")
        print(f"  Detection: {technique.get('detection_rules', 'Configure detection rule')}")
    print()
```

## PASTA Seven-Stage Analysis

### Full PASTA Implementation

```python
from threat_modeling import PASTAAnalyzer, BusinessContext, TechnicalModel, AttackModel

# Stage 1: Business Objectives
business = BusinessContext(
    application="Healthcare Patient Portal",
    business_objectives=[
        "Enable patients to access medical records",
        "Schedule appointments with providers",
        "Process prescription refill requests",
        "Maintain HIPAA compliance",
    ],
    data_sensitivity={
        "medical_records": "critical",
        "patient_pii": "critical",
        "insurance_info": "high",
        "appointment_data": "medium",
    },
    regulatory_requirements=["HIPAA", "HITECH", "State Privacy Laws"],
    financial_impact_per_breach=5000000,
    reputation_impact="severe",
)

# Stage 2: Define Technical Scope
tech_model = TechnicalModel(
    components=[
        "PatientWebApp", "MobileApp", "APIGateway", "AuthService",
        "PatientService", "AppointmentService", "PrescriptionService",
        "Database", "MessageQueue", "EmailService", "CDN"
    ],
    protocols=["HTTPS", "gRPC", "PostgreSQL", "Redis", "SMTP"],
    trust_boundaries=[
        "Internet/DMZ", "DMZ/Application", "Application/Data",
        "Application/ThirdParty", "Internal/VPN"
    ],
    external_dependencies=[
        {"name": "Insurance Provider API", "trust": "low", "data_shared": ["patient_id", "insurance_info"]},
        {"name": "Pharmacy System", "trust": "medium", "data_shared": ["prescription_id", "medication"]},
        {"name": "Email Provider", "trust": "low", "data_shared": ["email", "appointment_reminder"]},
    ],
)

# Stages 3-7: Run PASTA
analyzer = PASTAAnalyzer(business, tech_model)
results = analyzer.run_full_analysis()

# Stage 3: Application decomposition
print("=== Stage 3: Application Decomposition ===")
for component in results.decomposition.components:
    print(f"  {component.name}: {component.type} (trust: {component.trust_level})")
    for flow in component.data_flows:
        print(f"    Flow: {flow.source} -> {flow.destination} ({flow.protocol})")

# Stage 4: Threat analysis
print("\n=== Stage 4: Threat Analysis ===")
for threat in results.threats:
    print(f"  [{threat.category}] {threat.description}")
    print(f"    STRIDE: {threat.stride_category}")
    print(f"    ATT&CK: {threat.attck_technique}")

# Stage 5: Vulnerability analysis
print("\n=== Stage 5: Vulnerability Analysis ===")
for vuln in results.vulnerabilities:
    print(f"  {vuln.cve or vuln CWE}: {vuln.description}")
    print(f"    Component: {vuln.component}")
    print(f"    Exploitability: {vuln.exploitability}")

# Stage 6: Attack modeling
print("\n=== Stage 6: Attack Modeling ===")
for attack in results.attack_models:
    print(f"  Attack: {attack.name}")
    print(f"    Pre-conditions: {attack.preconditions}")
    print(f"    Attack steps: {len(attack.steps)}")
    print(f"    Post-conditions: {attack.postconditions}")

# Stage 7: Risk & impact analysis
print("\n=== Stage 7: Risk & Impact Analysis ===")
for risk in results.risk_analysis:
    print(f"  Risk: {risk.description}")
    print(f"    Business Impact: ${risk.financial_impact:,.0f}")
    print(f"    Likelihood: {risk.likelihood}")
    print(f"    Mitigation: {risk.mitigation}")
```

## Privacy Threat Modeling with LINDDUN

### LINDDUN Privacy Analysis

```python
from threat_modeling import LINDDUNAnalyzer, PrivacyThreat, PersonalData

analyzer = LINDDUNAnalyzer()

# Define personal data flows
personal_data = [
    PersonalData(
        data_type="email",
        sensitivity="medium",
        purpose="account_communication",
        retention="account_lifetime",
        processors=["auth_service", "email_service"],
        cross_border=False,
    ),
    PersonalData(
        data_type="medical_records",
        sensitivity="critical",
        purpose="patient_care",
        retention="10_years",
        providers=["patient_service", "database"],
        cross_border=False,
    ),
    PersonalData(
        data_type="location_data",
        sensitivity="high",
        purpose="facility_finder",
        retention="30_days",
        providers=["mobile_app", "api_gateway"],
        cross_border=False,
    ),
]

# Run LINDDUN analysis
linddun_threats = analyzer.analyze(personal_data)

# L: Linkability
print("=== Linkability Threats ===")
for threat in linddun_threats.linkability:
    print(f"  {threat.description}")
    print(f"    Data: {threat.data_involved}")
    print(f"    Mitigation: {threat.mitigation}")

# I: Identifiability
print("\n=== Identifiability Threats ===")
for threat in linddun_threats.identifiability:
    print(f"  {threat.description}")
    print(f"    Data: {threat.data_involved}")
    print(f"    Mitigation: {threat.mitigation}")

# N: Non-repudiation
print("\n=== Non-repudiation Threats ===")
for threat in linddun_threats.non_repudiation:
    print(f"  {threat.description}")
    print(f"    Data: {threat.data_involved}")
    print(f"    Mitigation: {threat.mitigation}")

# D: Detectability
print("\n=== Detectability Threats ===")
for threat in linddun_threats.detectability:
    print(f"  {threat.description}")
    print(f"    Data: {threat.data_involved}")
    print(f"    Mitigation: {threat.mitigation}")

# D: Disclosure of information
print("\n=== Disclosure Threats ===")
for threat in linddun_threats.disclosure:
    print(f"  {threat.description}")
    print(f"    Data: {threat.data_involved}")
    print(f"    Mitigation: {threat.mitigation}")

# U: Unawareness
print("\n=== Unawareness Threats ===")
for threat in linddun_threats.unawareness:
    print(f"  {threat.description}")
    print(f"    Mitigation: {threat.mitigation}")

# N: Non-compliance
print("\n=== Non-compliance Threats ===")
for threat in linddun_threats.non_compliance:
    print(f"  {threat.description}")
    print(f"    Regulation: {threat.regulation}")
    print(f"    Mitigation: {threat.mitigation}")
```

## Threat Model Lifecycle Management

### Living Threat Model with Version Control

```python
from threat_modeling import LivingThreatModel, ThreatLifecycle, ReevaluationTrigger

# Create version-controlled threat model
model = LivingThreatModel(
    system_name="E-Commerce Platform",
    version="2.1.0",
    owner="security-team",
    review_cycle="quarterly",
    storage="git",  # Store in git for version history
    repo_path="security/threat-models/ecommerce",
)

# Track threat lifecycle
lifecycle = ThreatLifecycle(model)

# Add new threat
threat = lifecycle.add_threat(
    title="SSRF via webhook callback URL",
    category="Information Disclosure",
    component="WebhookService",
    stride="Information Disclosure",
    severity="high",
    description="Attacker can provide internal URLs as webhook callback, causing server to make requests to internal services",
    attacker_profile="External, low skill, financial motivation",
    preconditions=["Valid account", "Ability to create webhooks"],
    attack_vector="HTTP POST to /api/webhooks with internal URL as callback",
    impact=["Access to internal metadata service", "Pivot to internal services", "Potential RCE"],
    mitigations=[
        "URL allowlist for webhook callbacks",
        "Network segmentation to prevent SSRF",
        "Disable IMDSv1 on cloud instances",
    ],
    risk_acceptance=None,
    status="open",
)

# Track reevaluation triggers
triggers = [
    ReevaluationTrigger(
        trigger="architecture_change",
        description="WebhookService moved to new network segment",
        date="2024-03-15",
        changed_by="platform-team",
    ),
    ReevaluationTrigger(
        trigger="new_threat_intel",
        description="New SSRF bypass technique published for similar framework",
        date="2024-04-01",
        changed_by="threat-intel-team",
    ),
]

for trigger in triggers:
    lifecycle.handle_trigger(trigger)
    print(f"Trigger: {trigger.description}")
    print(f"  Action: Reevaluation completed")
    print(f"  New threats: {trigger.new_threats_found}")
    print(f"  Mitigations updated: {trigger.mitigations_updated}")
```

## Threat Modeling Automation in CI/CD

### Automated Threat Model Generation

```python
from threat_modeling import ThreatModelGenerator, InfrastructureParser

# Generate threat model from infrastructure-as-code
parser = InfrastructureParser(
    sources=[
        {"type": "terraform", "path": "./infrastructure/"},
        {"type": "kubernetes", "path": "./k8s/manifests/"},
        {"type": "docker_compose", "path": "./docker-compose.yml"},
    ]
)

# Parse infrastructure
infra_model = parser.parse()
print(f"Components discovered: {len(infra_model.components)}")
print(f"Data flows discovered: {len(infra_model.data_flows)}")
print(f"Trust boundaries discovered: {len(infra_model.trust_boundaries)}")

# Generate threat model automatically
generator = ThreatModelGenerator()
auto_model = generator.generate_from_infrastructure(
    infrastructure=infra_model,
    business_context={
        "application": "E-Commerce Platform",
        "data_classification": {"customer_data": "high", "product_catalog": "low"},
        "regulatory_requirements": ["PCI-DSS", "GDPR"],
    }
)

# Generate STRIDE threats for each component
for component in auto_model.components:
    threats = generator.generate_stride_threats(component)
    if threats:
        print(f"\n{component.name}: {len(threats)} threats identified")
        for threat in threats:
            print(f"  [{threat.category}] {threat.description}")
            print(f"    Severity: {threat.severity}")
            print(f"    Mitigation: {threat.mitigation}")

# Export for review
auto_model.export(
    format="markdown",
    output_path="./threat-models/auto-generated.md",
    include_diagrams=True,
    include_mitigations=True,
    include_risk_scores=True,
)
```

## Risk Assessment Frameworks

### FAIR (Factor Analysis of Information Risk)

```python
from threat_modeling import FAIRAssessment, RiskScenario

fair = FAIRAssessment()

# Define risk scenario
scenario = RiskScenario(
    threat_event="Data breach via SQL injection",
    loss_event_type="confidentiality",
    assets=["customer_database"],
    threat_agent="external_attacker",
    vulnerability="sql_injection_in_search",
)

# FAIR quantification factors
factors = {
    "threat_event_frequency": {
        "min": 1,
        "mode": 3,
        "max": 10,
        "confidence": "medium",
    },
    "vulnerability": {
        "min": 0.3,
        "mode": 0.6,
        "max": 0.9,
        "confidence": "high",
    },
    "loss_magnitude": {
        "primary": {
            "replacement_costs": {"min": 100000, "mode": 500000, "max": 2000000},
            "response_costs": {"min": 50000, "mode": 150000, "max": 500000},
            "fines_judgments": {"min": 0, "mode": 200000, "max": 1000000},
        },
        "secondary": {
            "competitive_advantage": {"min": 0, "mode": 100000, "max": 500000},
            "reputation": {"min": 100000, "mode": 500000, "max": 2000000},
        },
    },
}

# Run Monte Carlo simulation
result = fair.analyze(
    scenario=scenario,
    factors=factors,
    iterations=10000,
)

print(f"=== FAIR Risk Analysis ===")
print(f"Scenario: {scenario.threat_event}")
print(f"\nLoss Event Frequency:")
print(f"  Mean: {result.lef.mean:.1f}/year")
print(f"  95th percentile: {result.lef.percentile_95:.1f}/year")
print(f"\nLoss Magnitude:")
print(f"  Mean: ${result.lm.mean:,.0f}")
print(f"  95th percentile: ${result.lm.percentile_95:,.0f}")
print(f"\nAnnual Loss Expectancy:")
print(f"  Mean: ${result.ale.mean:,.0f}")
print(f"  95th percentile: ${result.ale.percentile_95:,.0f}")
print(f"\nRisk Level: {result.risk_level}")
print(f"Recommended investment in mitigation: ${result.recommended_mitigation_investment:,.0f}")
```
