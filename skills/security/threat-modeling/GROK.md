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
