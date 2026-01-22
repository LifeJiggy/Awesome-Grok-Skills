# Threat Modeling Agent

## Overview

The **Threat Modeling Agent** provides comprehensive threat analysis capabilities using methodologies like STRIDE and attack trees. This agent helps organizations identify, analyze, and mitigate security threats during system design and development.

## Core Capabilities

### 1. STRIDE Analysis
Perform systematic threat identification:
- **Spoofing**: Identity impersonation threats
- **Tampering**: Data or code modification threats
- **Repudiation**: Denial of actions
- **Information Disclosure**: Data exposure threats
- **Denial of Service**: Availability disruption
- **Elevation of Privilege**: Unauthorized access gains

### 2. Data Flow Diagramming
Create and analyze system diagrams:
- **External Entities**: Users, external systems
- **Processes**: Application logic and services
- **Data Stores**: Databases, file systems
- **Trust Boundaries**: Security perimeters
- **Data Flows**: Information movement

### 3. Risk Calculation
Quantify and prioritize threats:
- **Likelihood Assessment**: Probability of exploitation
- **Impact Analysis**: Business and technical impact
- **Risk Scoring**: Quantitative risk values
- **Prioritization**: Ranked mitigation order
- **Residual Risk**: Risk after controls

### 4. Attack Trees
Model attacker scenarios:
- **Attack Goals**: Attacker objectives
- **Attack Paths**: Sequence of steps
- **Cost/Benefit Analysis**: Attacker perspective
- **Mitigation Points**: Defense opportunities
- **Scenario Planning**: What-if analysis

### 5. Reporting
Generate comprehensive reports:
- **Executive Summaries**: Management overviews
- **Detailed Findings**: Technical analysis
- **Recommendations**: Action items
- **Compliance Mapping**: Standards alignment
- **Visual Diagrams**: Architecture diagrams

## Usage Examples

### STRIDE Analysis

```python
from threat_modeling import STRIDEAnalyzer, DiagramElement

stride = STRIDEAnalyzer()
element = DiagramElement(
    id="auth-001",
    type="process",
    name="User Authentication",
    description="Handles user login",
    properties={"confidentiality": "high"},
    trust_level="internal",
    incoming_flows=[],
    outgoing_flows=[]
)
threats = stride.analyze_element(element)
for threat in threats:
    print(f"{threat.severity.value}: {threat.name}")
    print(f"  Mitigation: {threat.mitigation}")
```

### Data Flow Diagram

```python
from threat_modeling import DataFlowDiagrammer

dfd = DataFlowDiagrammer()

user = dfd.add_external_entity("User", "End user application")
web = dfd.add_process("Web Server", "dmz")
api = dfd.add_process("API Service", "internal")
db = dfd.add_data_store("User Database", "high")
boundary = dfd.add_trust_boundary("DMZ Boundary")

dfd.add_data_flow(user, web, "HTTP requests", "HTTPS")
dfd.add_data_flow(web, api, "API calls", "HTTPS")
dfd.add_data_flow(api, db, "Queries", "TLS")

diagram = dfd.generate_diagram_description()
print(f"Elements: {diagram['elements']}, Flows: {diagram['flows']}")
```

### Risk Prioritization

```python
from threat_modeling import RiskCalculator

risk = RiskCalculator()
prioritized = risk.prioritize_threats(
    threats,
    existing_controls={'SPOOF-001': ['MFA']}
)
for p in prioritized:
    print(f"Priority {p['risk_level']}: {p['threat_name']}")
    print(f"  Risk Score: {p['risk_score']}/9")
```

### Attack Tree

```python
from threat_modeling import AttackTreeGenerator

tree = AttackTreeGenerator()
attack = tree.create_attack_tree(
    goal="Steal user credentials",
    attacker_profile="opportunistic"
)
print(f"Attack Goal: {attack['goal']}")
print(f"Easiest Path: {attack['easiest_path']}")
print(f"Total Attack Paths: {attack['total_paths']}")
```

### Report Generation

```python
from threat_modeling import ThreatReportGenerator

report = ThreatReportGenerator()
summary = report.generate_executive_summary(
    project_name="E-Commerce Platform",
    threats=threats,
    scope="Full application stack"
)
print(summary)

detailed = report.generate_detailed_report(
    project_name="E-Commerce Platform",
    diagram=diagram,
    threats=threats,
    mitigations=["Implement MFA", "Encrypt data at rest"]
)
print(f"Total threats: {detailed['threat_summary']['total_threats']}")
```

## Threat Modeling Methodologies

### STRIDE Threat Categories

| Category | Threat Type | Example | Mitigation |
|----------|-------------|---------|------------|
| **S**poofing | Identity spoofing | Fake user login | Strong authentication |
| **T**ampering | Data tampering | Modify transaction | Digital signatures |
| **R**epudiation | Action denial | "I didn't send that" | Audit logging |
| **I**nformation Disclosure | Data leak | Expose user data | Encryption |
| **D**enial of Service | Service disruption | DDoS attack | Rate limiting |
| **E**levation of Privilege | Unauthorized access | Admin takeover | Least privilege |

### Risk Matrix

| Likelihood / Impact | Low | Medium | High | Critical |
|---------------------|-----|--------|------|----------|
| High | Medium | High | Critical | Critical |
| Medium | Low | Medium | High | Critical |
| Low | Low | Low | Medium | High |

### DFD Elements

| Element Type | Symbol | Trust Level | Examples |
|--------------|--------|-------------|----------|
| External Entity | Circle | Untrusted | Users, Partner systems |
| Process | Circle | Varies | Web server, API, Service |
| Data Store | Open rectangle | Internal | Database, File storage |
| Trust Boundary | Dashed line | Boundary | DMZ, VPC, Firewall |

## Threat Categories Deep Dive

### Spoofing Threats

**Common Attack Vectors:**
- Credential theft
- Session hijacking
- IP spoofing
- DNS spoofing
- Man-in-the-middle

**Mitigation Strategies:**
- Multi-factor authentication
- Certificate pinning
- Session tokens with short expiry
- Strong password policies
- Account lockout policies

### Tampering Threats

**Common Attack Vectors:**
- SQL injection
- Buffer overflow
- Parameter manipulation
- Race conditions
- Time-of-check to time-of-use

**Mitigation Strategies:**
- Input validation
- Parameterized queries
- Memory-safe languages
- File integrity monitoring
- Code signing

### Information Disclosure

**Common Attack Vectors:**
- Data breaches
- Side-channel attacks
- Error messages
- Logging sensitive data
- Insecure storage

**Mitigation Strategies:**
- Encryption at rest and in transit
- Data classification
- Secure key management
- Minimize logging of sensitive data
- Data masking

### Denial of Service

**Common Attack Vectors:**
- Volumetric attacks
- Protocol attacks
- Application layer attacks
- Resource exhaustion
- Amplification attacks

**Mitigation Strategies:**
- Rate limiting
- Load balancing
- CDN usage
- Traffic filtering
- Auto-scaling

## Attack Tree Components

### Structure

```
Goal: Compromise User Account
├── Method 1: Credential Theft
│   ├── Phishing
│   │   ├── Email phishing
│   │   └── Spear phishing
│   └── Keylogging
│       └── Malware-based
└── Method 2: Authentication Bypass
    ├── Brute force
    └── Session fixation
```

### Attack Cost Metrics

| Metric | Description | Values |
|--------|-------------|--------|
| Cost | Monetary cost to attacker | Low, Medium, High |
| Skill Required | Attacker expertise | Low, Medium, High |
| Detection | Likelihood of detection | Low, Medium, High |
| Success Rate | Probability of success | Percentage |

## Threat Modeling Process

```
┌─────────────────────────────────────────────────────────┐
│              Threat Modeling Process                     │
├─────────────────────────────────────────────────────────┤
│  1. Define Scope → 2. Create Model → 3. Identify Threats│
│         │                │                  │            │
│  6. Document ← 5. Mitigate ← 4. Analyze Risks          │
│         │                │                  │            │
│         └────────────────┴──────────────────┘
└─────────────────────────────────────────────────────────┘
```

### Step Details

1. **Define Scope**: What are we analyzing?
2. **Create Model**: Build DFD or other diagram
3. **Identify Threats**: Use STRIDE or other methodology
4. **Analyze Risks**: Calculate likelihood and impact
5. **Mitigate**: Design security controls
6. **Document**: Record findings and decisions

## Tools and Platforms

### Commercial Tools

| Tool | Strength | Best For |
|------|----------|----------|
| Microsoft TMT | Free, integrated | Microsoft ecosystems |
| OWASP Threat Dragon | Open source | Web applications |
| IriusRisk | Collaborative | Enterprise teams |
| SD Elements | Automated | Compliance-driven |

### Open Source Tools

| Tool | Purpose | Features |
|------|---------|----------|
| Threat Dragon | Diagram creation | STRIDE support |
| OWASP PyAttacks | Attack patterns | Attack trees |
| Maat | Analysis framework | Custom methodologies |

## Compliance Mapping

### NIST Cybersecurity Framework

| Function | Threat Model Activity |
|----------|----------------------|
| Identify | Asset inventory, risk assessment |
| Protect | Control design, secure architecture |
| Detect | Logging, monitoring points |
| Respond | Incident response planning |
| Recover | Resilience testing |

### ISO 27001 Controls

| Control | Threat Model Application |
|---------|-------------------------|
| A.14.1 | Security requirements analysis |
| A.14.2 | Secure development lifecycle |
| A.13.1 | Network security design |
| A.12.2 | Malware protection design |
| A.10.1 | Cryptographic controls design |

## Documentation Templates

### Threat Documentation

```
Threat ID: T-001
Name: SQL Injection in User Search
Category: Tampering
Severity: High
Description: Attacker can inject SQL commands...
Affected Component: search.php
Attack Vector: Network
Likelihood: Medium
Impact: High
Mitigation: Use parameterized queries
Status: Open
```

### Architecture Documentation

```
Component: User Authentication Service
Trust Level: Internal
Data Flows:
  - HTTPS from: Web Server
  - TLS to: User Database
Trust Boundaries Crossed: DMZ → Internal
Existing Controls: HTTPS, Rate Limiting
Associated Threats: SPOOF-001, TAMP-001, EOP-001
```

## Best Practices

1. **Start Early**: Model during design phase
2. **Iterate**: Update model with changes
3. **Automate**: Integrate into CI/CD
4. **Collaborate**: Include diverse perspectives
5. **Prioritize**: Focus on high-risk areas
6. **Document**: Maintain living documents
7. **Validate**: Test mitigations

## Related Skills

- [Vulnerability Assessment](./../security-assessment/vulnerability-assessment/resources/GROK.md) - Finding vulnerabilities
- [Penetration Testing](./../red-team/penetration-testing/resources/GROK.md) - Testing security
- [Secure Coding](./../secure-coding/resources/GROK.md) - Prevention through development
- [Security Monitoring](./../blue-team/security-monitoring/resources/GROK.md) - Detection capabilities

---

**File Path**: `skills/security/threat-modeling/resources/threat_modeling.py`
