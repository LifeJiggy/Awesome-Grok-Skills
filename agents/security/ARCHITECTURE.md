# Security Agent Architecture

## 1. Overview

The Security Agent implements a defense-in-depth architecture for enterprise security operations. It orchestrates five core subsystems—vulnerability scanning, threat modeling, compliance auditing, incident response, and penetration testing—behind a unified `SecurityAgent` facade. This design enables organizations to maintain a holistic security posture while keeping each subsystem independently testable and extensible.

The architecture follows the principle of separation of concerns: each subsystem owns its domain logic, data models, and state management. The facade layer coordinates cross-cutting concerns like dashboard aggregation, unified scoring, and correlation of findings across subsystems. This separation ensures that changes to one subsystem (e.g., adding a new compliance framework) do not ripple into others.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SecurityAgent (Facade)                            │
├─────────────┬─────────────┬─────────────┬──────────────┬────────────────────┤
│ Vulnerability│  Threat     │ Compliance  │  Incident    │  Penetration       │
│ Scanner     │  Modeler    │  Auditor    │  Responder   │  Tester            │
├─────────────┼─────────────┼─────────────┼──────────────┼────────────────────┤
│ SAST Engine │ STRIDE      │ SOC2        │ Playbooks    │ Network Scan       │
│ Secrets     │ Attack Tree │ ISO27001    │ Timeline     │ Web Scan           │
│ SCA         │ Trust Zone  │ PCI DSS     │ IOC Tracking │ Scope Management   │
│ Container   │ Data Flow   │ HIPAA       │ MTTR Calc    │ Finding Reports    │
│             │             │ NIST        │              │                    │
│             │             │ GDPR        │              │                    │
└─────────────┴─────────────┴─────────────┴──────────────┴────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Shared Models    │
                    │ Vulnerability      │
                    │ Incident           │
                    │ ComplianceControl  │
                    │ PentestFinding     │
                    │ ScanResult         │
                    └───────────────────┘
```

## 2. Component Descriptions

### 2.1 VulnerabilityScanner

Multi-engine static analysis scanner with pluggable detection backends. The scanner orchestrates multiple detection engines in parallel, aggregates results, deduplicates findings, and calculates an overall security score. Each engine operates independently, allowing for selective scanning based on the target codebase and risk profile.

The engine registry pattern allows new scan types to be added without modifying the scanner core. Each engine implements a common interface: it receives source code and language, returns a list of findings. The aggregator normalizes these findings into a unified format, assigns confidence scores based on detection heuristics, and produces a severity-weighted security score.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      VulnerabilityScanner                                │
├──────────────────────────────────────────────────────────────────────────┤
│  Engine Registry (Dict[ScanType, Callable])                              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │    SAST    │ │  Secrets   │ │    SCA     │ │ Container  │           │
│  │  (Static   │ │  (Regex    │ │ (Version   │ │ (YAML/     │           │
│  │   Analysis)│ │   Match)   │ │  Match)    │ │  Docker)   │           │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘           │
│        │              │              │              │                    │
│  ┌─────┴──────────────┴──────────────┴──────────────┴──────┐            │
│  │                  Finding Aggregator                      │            │
│  │  - Deduplication by (file, line, type)                  │            │
│  │  - Confidence scoring (0.0 - 1.0)                       │            │
│  │  - Severity classification (CRITICAL → INFO)             │            │
│  │  - CWE mapping                                          │            │
│  └──────────────────────────────────────────────────────────┘            │
│                                                                          │
│  CVE Database (Dict[str, Dict])                                          │
│  - vulnerability_id → {severity, cwe, description, references}          │
│  - Populated from NVD feed or custom entries                            │
│                                                                          │
│  Scan History (List[Dict])                                               │
│  - timestamp, language, findings_count, security_score                   │
│                                                                          │
│  Statistics Calculator                                                   │
│  - Severity distribution, type distribution, trend analysis             │
└──────────────────────────────────────────────────────────────────────────┘
```

**Scan engines:**
- **SAST**: Pattern-based detection for injection, XSS, SSRF, command injection, path traversal. Uses regex patterns compiled from OWASP guidelines. Each pattern maps to a CWE identifier for standardized classification.
- **Secrets**: Regex-based credential detection (API keys, tokens, passwords, cloud keys). Supports AWS, GCP, Azure, GitHub, Slack, Stripe, and custom patterns. False positive suppression via entropy checks and allowlist filtering.
- **SCA**: Dependency version vulnerability matching. Parses package manifests, resolves dependency trees, and cross-references against CVE databases.
- **Container**: Dockerfile/YAML security posture analysis. Checks for privileged containers, exposed ports, missing health checks, running as root, and image provenance.

**SAST Detection Patterns:**
```
┌──────────────────────────────────────────────────────────────────────────┐
│  Pattern Category     │  Regex Example                    │  CWE        │
├───────────────────────┼───────────────────────────────────┼─────────────┤
│  SQL Injection        │  query.*\+.*request|execute.*%s   │  CWE-89     │
│  Command Injection    │  os\.system\(|subprocess\.call    │  CWE-78     │
│  XSS                  │  innerHTML.*\+|document\.write    │  CWE-79     │
│  SSRF                 │  requests\.get\(.*input|urlopen   │  CWE-918    │
│  Path Traversal       │  open\(.*\+.*\.\./|os\.path\.join│  CWE-22     │
│  Hardcoded Secret     │  password\s*=\s*["'].*["']       │  CWE-798    │
│  Eval/Exec            │  eval\(|exec\(|compile\(|__import│  CWE-95     │
│  Weak Crypto          │  md5\(|sha1\(|DES                 │  CWE-327    │
│  Insecure Deser       │  pickle\.load|yaml\.load          │  CWE-502    │
│  Open Redirect        │  redirect\(.*input|Location.*input│  CWE-601    │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.2 ThreatModeler

STRIDE-based threat modeling with attack tree construction. The threat modeler maintains a registry of system components, data flows, and trust zones. It generates threats by applying STRIDE categories to each component-flow intersection and builds attack trees that visualize potential attack paths.

The STRIDE methodology systematically covers six threat categories. For each registered component, the modeler evaluates which STRIDE threats apply based on the component type (service, storage, user, external) and the data flows crossing trust boundaries. The resulting threat catalog provides a comprehensive security view of the system architecture.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ThreatModeler                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Components Registry (Dict[str, Component])                                │
│  ┌──────────────────┬──────────────────┬──────────────────┐                │
│  │  API Gateway     │  Database        │  User Browser    │                │
│  │  type: service   │  type: storage   │  type: user      │                │
│  │  trust: external │  trust: trusted  │  trust: external │                │
│  └──────────────────┴──────────────────┴──────────────────┘                │
│                                                                             │
│  Data Flow Graph (List[DataFlow])                                          │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  User → HTTPS → API Gateway → SQL → Database            │              │
│  │  User → HTTPS → CDN → HTTP → Origin Server              │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                             │
│  Trust Zone Definitions (Dict[str, TrustZone])                             │
│  - internet, dmz, internal, management, partner                            │
│                                                                             │
│  STRIDE Threat Generator                                                   │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  For each (component, flow) pair:                        │              │
│  │    Evaluate S/T/R/I/D/E applicability                    │              │
│  │    Generate threat with mitigations                      │              │
│  │    Map to MITRE ATT&CK technique IDs                    │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                             │
│  Attack Tree Builder                                                       │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  Target Node (root)                                      │              │
│  │  ├── Attack Path 1 (AND/OR gates)                        │              │
│  │  │   ├── Prerequisite 1                                  │              │
│  │  │   └── Prerequisite 2                                  │              │
│  │  └── Attack Path 2                                       │              │
│  │      └── Prerequisite 3                                  │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                             │
│  Threat Summary Aggregator                                                 │
│  - Total threats, severity distribution, mitigation coverage               │
│  - Per-component threat counts, per-STRIDE category breakdown              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**STRIDE categories:**
| Category | Description | Typical Mitigation | MITRE ATT&CK Mapping |
|----------|-------------|-------------------|----------------------|
| Spoofing | Identity impersonation | mTLS, certificate pinning | T1556, T1557 |
| Tampering | Data modification | HMAC, digital signatures | T1565, T1560 |
| Repudiation | Action denial | Audit logging | T1070, T1562 |
| Info Disclosure | Data exposure | Encryption, RBAC | T1005, T1039 |
| DoS | Availability disruption | Rate limiting, CDN | T1498, T1499 |
| EoP | Privilege escalation | Least privilege, RBAC | T1068, T1078 |

**Attack Tree Notation:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│  Attack Tree: Compromise Production Database                            │
│                                                                         │
│  Root: [AND] Steal customer data                                        │
│  ├── [OR] Direct access to database                                     │
│  │   ├── [AND] SQL injection via API                                    │
│  │   │   ├── Find injectable endpoint                                   │
│  │   │   └── Bypass WAF rules                                           │
│  │   └── [AND] Compromise database credentials                          │
│  │       ├── Extract from config file                                   │
│  │       └── Crack weak password                                        │
│  ├── [OR] Indirect access via application                               │
│  │   ├── [AND] SSRF from application server                             │
│  │   │   └── Access metadata service for IAM role                       │
│  │   └── [AND] Deserialization vulnerability                            │
│  │       └── Execute OS command on DB host                              │
│  └── [AND] Backup compromise                                            │
│      ├── Access S3 bucket with backups                                  │
│      └── Decrypt backup files                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 ComplianceAuditor

Multi-framework compliance assessment engine. The auditor maintains a registry of compliance frameworks, each defined as a set of controls with evaluation criteria. It assesses compliance by comparing evidence against control requirements, calculates scores, and generates detailed reports.

The framework registry pattern allows new compliance standards to be added declaratively. Each framework defines its controls, their descriptions, and evaluation methods. The evidence evaluator accepts a dictionary mapping control IDs to boolean or numeric evidence values, enabling both binary compliance checks and nuanced scoring.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      ComplianceAuditor                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  Framework Registry (Dict[ComplianceFramework, Dict])                       │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐                  │
│  │  SOC2    │ ISO27001 │ PCI_DSS  │  HIPAA   │   NIST   │                  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘                  │
│  ┌──────────┬──────────┐                                                    │
│  │   GDPR   │   CCPA   │                                                    │
│  └──────────┴──────────┘                                                    │
│                                                                              │
│  Evidence Evaluator                                                         │
│  - Boolean controls: implemented (True) / not (False)                       │
│  - Numeric controls: partial implementation (0.0 - 1.0)                     │
│  - Weighted scoring per control category                                    │
│                                                                              │
│  Score Calculator                                                           │
│  - Category scores: sum(implemented) / total controls × 100                 │
│  - Overall score: weighted average of category scores                       │
│  - Grade: A (90+), B (80+), C (70+), D (60+), F (<60)                      │
│                                                                              │
│  Report Generator                                                           │
│  - Executive summary with overall score and grade                           │
│  - Category breakdown with per-control details                              │
│  - Gap analysis: missing controls prioritized by risk                       │
│  - Remediation roadmap with effort estimates                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Compliance Framework Structure:**
```
ComplianceFramework.SOC2:
├── Trust Service Criteria
│   ├── CC1 (Control Environment)
│   │   ├── CC1.1: Integrity and ethical values
│   │   ├── CC1.2: Board independence
│   │   ├── CC1.3: Organizational structure
│   │   ├── CC1.4: Competence commitment
│   │   └── CC1.5: Accountability
│   ├── CC2 (Communication)
│   ├── CC3 (Risk Assessment)
│   ├── CC4 (Monitoring)
│   ├── CC5 (Control Activities)
│   ├── CC6 (Logical and Physical Access)
│   ├── CC7 (System Operations)
│   ├── CC8 (Change Management)
│   └── CC9 (Risk Mitigation)
└── Scoring
    ├── Implemented = True → control_score = 1.0
    ├── Implemented = False → control_score = 0.0
    └── Partial = 0.0-1.0 → control_score = partial_value
```

**Supported frameworks and their control counts:**
| Framework | Controls | Categories | Scoring Method |
|-----------|----------|------------|----------------|
| SOC2 | 64 | 9 Trust Service Criteria | Boolean + weighted |
| ISO27001 | 114 | 14 Annex A domains | Boolean + categorical |
| PCI DSS | 281 | 12 Requirements | Boolean per sub-requirement |
| HIPAA | 46 | 6 Safeguard categories | Boolean + weight |
| NIST CSF | 108 | 5 Functions | Tier-based maturity |
| GDPR | 99 | 11 Chapters | Boolean + article-level |
| CCPA | 23 | 7 Categories | Boolean + consumer rights |

### 2.4 IncidentResponder

Automated incident lifecycle management. The responder manages the full incident lifecycle from detection through closure, with playbook-driven workflows, timeline tracking, containment actions, and metrics calculation.

The playbook engine provides predefined response procedures for common incident types. Each playbook defines phases, actions, responsible roles, and escalation triggers. The timeline tracker maintains a chronological log of all actions taken during an incident, enabling post-incident analysis and MTTR calculation.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      IncidentResponder                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  Playbook Engine                                                            │
│  ┌─────────────────┬─────────────────┬─────────────────┐                    │
│  │  Data Breach    │  Ransomware     │  Phishing       │                    │
│  │  ┌───────────┐  │  ┌───────────┐  │  ┌───────────┐  │                    │
│  │  │ Detect    │  │  │ Contain   │  │  │ Verify    │  │                    │
│  │  │ Contain   │  │  │ Isolate   │  │  │ Report    │  │                    │
│  │  │ Eradicate │  │  │ Negotiate │  │  │ Block     │  │                    │
│  │  │ Recover   │  │  │ Restore   │  │  │ Educate   │  │                    │
│  │  │ Notify    │  │  │ Notify    │  │  │ Notify    │  │                    │
│  │  └───────────┘  │  └───────────┘  │  └───────────┘  │                    │
│  └─────────────────┴─────────────────┴─────────────────┘                    │
│                                                                              │
│  Incident Store (Dict[str, Incident])                                       │
│  - Key: incident_id (INC-YYYYMMDD-NNNN)                                     │
│  - Value: full incident record with all fields                              │
│                                                                              │
│  Timeline Tracker                                                           │
│  - Each entry: timestamp, action, user, notes                               │
│  - Enables MTTR calculation and post-mortem analysis                        │
│                                                                              │
│  IOC Registry                                                               │
│  - Indicators of Compromise linked to incidents                             │
│  - Types: IP, domain, hash, email, URL                                      │
│  - TTL and confidence scoring                                               │
│                                                                              │
│  MTTR Calculator                                                            │
│  - Mean Time to Respond: detection → first action                           │
│  - Mean Time to Contain: detection → containment                            │
│  - Mean Time to Resolve: detection → resolution                             │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Incident lifecycle:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   OPEN ──► TRIAGED ──► INVESTIGATING ──► CONTAINED ──► ERADICATED          │
│     │                       │                              │                │
│     │                       │                              │                │
│     │                       ▼                              ▼                │
│     │              ESCALATED (if needed)           RECOVERED ──► CLOSED    │
│     │                                                                      │
│     └──────► CLOSED (false positive / duplicate)                           │
│                                                                             │
│  Status Transitions:                                                        │
│  - OPEN → TRIAGED: Initial assessment complete                             │
│  - TRIAGED → INVESTIGATING: Root cause analysis begins                     │
│  - INVESTIGATING → CONTAINED: Threat isolated                              │
│  - CONTAINED → ERADICATED: Threat removed                                  │
│  - ERADICATED → RECOVERED: Systems restored                                │
│  - RECOVERED → CLOSED: Post-incident review complete                       │
│  - Any → ESCALATED: Requires higher-level response                         │
│  - Any → CLOSED: False positive or duplicate                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**MTTR Calculation:**
```
MTTR = Σ(resolution_time - detection_time) / total_incidents

Where:
  detection_time  = incident.created_at
  resolution_time = incident.timeline[-1].timestamp (when status = RECOVERED/CLOSED)
  
Example:
  Incident 1: detected 10:00, resolved 14:00 → 4 hours
  Incident 2: detected 11:00, resolved 15:30 → 4.5 hours
  MTTR = (4 + 4.5) / 2 = 4.25 hours
```

### 2.5 PenetrationTester

Penetration test orchestration and reporting. The tester manages test scope, executes network and web application scans, records findings, and generates comprehensive reports.

The scope manager enforces testing boundaries, ensuring that only authorized targets are tested. It tracks scope definitions, validates scan targets against scope, and prevents out-of-scope activity. Findings are recorded with proof-of-concept details, impact assessments, and remediation recommendations.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      PenetrationTester                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  Scope Manager                                                              │
│  ┌──────────────────────────────────────────────────────────┐               │
│  │  Scopes (Dict[str, PentestScope])                        │               │
│  │  - target: URL or IP range                               │               │
│  │  - scope_type: blackbox / greybox / whitebox             │               │
│  │  - objectives: list of goals                             │               │
│  │  - constraints: boundaries and rules                     │               │
│  │  - exclusions: targets to avoid                          │               │
│  └──────────────────────────────────────────────────────────┘               │
│                                                                              │
│  ┌──────────────────┬──────────────────┐                                    │
│  │  Network Scan    │  Web Scan        │                                    │
│  │  ┌────────────┐  │  ┌────────────┐  │                                    │
│  │  │ Port Scan  │  │  │ Spider     │  │                                    │
│  │  │ Service    │  │  │ Fuzz       │  │                                    │
│  │  │ OS Detect  │  │  │ Auth Test  │  │                                    │
│  │  │ Vuln Check │  │  │ Injection  │  │                                    │
│  │  └────────────┘  │  │ XSS Test   │  │                                    │
│  │                   │  └────────────┘  │                                    │
│  └──────────────────┴──────────────────┘                                    │
│                                                                              │
│  Finding Store (List[PentestFinding])                                        │
│  - Each finding: title, severity, description, proof, impact, remediation   │
│  - Linked to scope and test type                                            │
│                                                                              │
│  Report Generator                                                           │
│  - Executive summary                                                        │
│  - Methodology description                                                  │
│  - Findings by severity                                                     │
│  - Remediation roadmap                                                      │
│  - Appendices (raw data, tools used)                                        │
│                                                                              │
│  Scope Registry                                                             │
│  - Active scopes, completed scopes, findings per scope                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Penetration Test Phases:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 1: Reconnaissance                                                    │
│  - Passive: DNS, WHOIS, certificate transparency, job postings             │
│  - Active: Port scanning, service enumeration, technology fingerprinting    │
│                                                                             │
│  Phase 2: Scanning                                                          │
│  - Network: Open ports, running services, OS detection                     │
│  - Web: Spidering, directory enumeration, parameter discovery              │
│  - Vulnerability: CVE matching, misconfiguration detection                 │
│                                                                             │
│  Phase 3: Exploitation                                                      │
│  - Verify identified vulnerabilities                                       │
│  - Chain vulnerabilities for greater impact                                │
│  - Document proof-of-concept for each finding                              │
│                                                                             │
│  Phase 4: Post-Exploitation                                                 │
│  - Assess impact of successful exploitation                                │
│  - Determine data access and exfiltration paths                            │
│  - Identify lateral movement opportunities                                 │
│                                                                             │
│  Phase 5: Reporting                                                         │
│  - Executive summary for leadership                                        │
│  - Technical findings with remediation                                     │
│  - Risk assessment and prioritization                                      │
│  - Timeline and methodology documentation                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3. Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Security Agent Data Flow                            │
│                                                                             │
│  Source Code / Config / Network                                             │
│         │                                                                   │
│         ▼                                                                   │
│  ┌───────────────────┐                                                      │
│  │ Vulnerability     │──── Findings ────┐                                  │
│  │ Scanner           │                  │                                  │
│  │ (SAST+Secrets+SCA)│                  │                                  │
│  └───────────────────┘                  │                                  │
│                                          │                                  │
│  ┌───────────────────┐                  │                                  │
│  │ Threat Modeler    │──── Threats ────┤                                  │
│  │ (STRIDE+Attack    │                  │                                  │
│  │  Trees)           │                  │                                  │
│  └───────────────────┘                  ▼                                  │
│                                    ┌─────────┐                             │
│  ┌───────────────────┐            │Security │                             │
│  │ Compliance Auditor│── Controls─►│  Agent  │──── Dashboard              │
│  │ (SOC2, ISO, PCI)  │            │(Facade) │                             │
│  └───────────────────┘            └─────────┘                             │
│                                    │       │                               │
│  ┌───────────────────┐            │       │                               │
│  │ Incident Responder│── Incidents┘       │                               │
│  │ (Playbooks,       │                    │                               │
│  │  Timeline)        │                    │                               │
│  └───────────────────┘                    │                               │
│                                           │                               │
│  ┌───────────────────┐                    │                               │
│  │ Penetration Tester│──── Findings ──────┘                               │
│  │ (Scope, Scan,     │                                                    │
│  │  Reports)         │                                                    │
│  └───────────────────┘                                                    │
│                                                                             │
│  Output: Unified Security Dashboard                                        │
│  - Vulnerability statistics and trends                                     │
│  - Threat model summary                                                    │
│  - Compliance scores by framework                                          │
│  - Active incidents and MTTR metrics                                       │
│  - Pentest findings and risk exposure                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4. Design Patterns

| Pattern | Application | Implementation Detail |
|---------|-------------|----------------------|
| **Facade** | `SecurityAgent` provides unified API over five subsystems | Single entry point, delegates to subsystems, aggregates results |
| **Strategy** | Scan engines registered as pluggable callbacks | `Dict[ScanType, Callable]` with engine registration at init |
| **Observer** | Incident timeline tracks all state transitions | Each status change appends timestamped entry |
| **Template Method** | Playbooks define phase-action templates | Phases are steps; actions are customizable per playbook |
| **Registry** | Compliance frameworks stored in class-level dict | `FRAMEWORKS` dict maps framework enum to control definitions |
| **Dataclass DTOs** | `Vulnerability`, `Incident`, `PentestFinding` as value objects | Immutable data transfer, clear field definitions |
| **Chain of Responsibility** | Escalation rules evaluated in sequence | Rules checked in priority order, first match triggers action |
| **Composite** | Scan results compose multiple engine outputs | Aggregate findings from all engines into unified result |
| **State Machine** | Incident lifecycle follows defined transitions | Valid transitions enforced, invalid transitions rejected |

## 5. Data Models

### Core Entities

```python
@dataclass
class Vulnerability:
    id: str                    # Unique identifier (VULN-XXXXXXXX)
    name: str                  # Human-readable name
    type: VulnerabilityType    # OWASP category
    severity: ThreatLevel      # CRITICAL=5, HIGH=4, MEDIUM=3, LOW=2, INFO=1
    cvss_score: float          # 0.0 - 10.0 (Common Vulnerability Scoring System)
    cwe_id: Optional[str]      # CWE reference (e.g., CWE-89)
    status: FindingStatus      # OPEN → IN_PROGRESS → RESOLVED/ACCEPTED/FALSE_POSITIVE
    confidence: float          # 0.0 - 1.0 detection confidence
    file_path: Optional[str]   # Source file location
    line_number: Optional[int] # Line number in source
    description: str           # Detailed description
    recommendation: str        # Remediation guidance
    references: List[str]      # CVE, CWE, OWASP links
```

```python
@dataclass
class Incident:
    id: str                              # Format: INC-YYYYMMDD-NNNN
    title: str                           # Short description
    severity: Severity                   # CRITICAL, HIGH, MEDIUM, LOW
    status: IncidentStatus               # Lifecycle state
    description: str                     # Detailed incident description
    affected_systems: List[str]          # Systems impacted
    timeline: List[Dict]                 # Chronological action log
    containment_actions: List[str]       # Actions taken to contain
    assigned_to: Optional[str]           # Assigned responder
    created_at: datetime                 # Detection timestamp
    updated_at: datetime                 # Last update timestamp
    resolved_at: Optional[datetime]      # Resolution timestamp
    iocs: List[Dict]                     # Indicators of compromise
```

```python
@dataclass
class PentestFinding:
    id: str                              # Unique identifier (PF-XXXXXXXX)
    title: str                           # Finding title
    severity: ThreatLevel                # CVSS-based severity
    description: str                     # Detailed description
    proof: str                           # Proof-of-concept
    impact: str                          # Business impact
    remediation: str                     # Remediation steps
    scope_id: str                        # Associated scope
    test_type: str                       # Network, web, social, etc.
    cvss_vector: Optional[str]           # CVSS vector string
    cwe_id: Optional[str]                # CWE reference
    created_at: datetime                 # Discovery timestamp
```

```python
@dataclass
class ComplianceControl:
    id: str                              # Control ID (e.g., CC1.1)
    name: str                            # Control name
    description: str                     # Control description
    framework: ComplianceFramework       # Parent framework
    category: str                        # Category within framework
    implemented: bool                    # Implementation status
    evidence: Optional[str]              # Evidence reference
    score: float                         # 0.0 - 1.0
    remediation: Optional[str]           # If not implemented
```

### Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Entity Relationships                                                      │
│                                                                             │
│  SecurityAgent 1──* Vulnerability                                           │
│  SecurityAgent 1──* Incident                                                │
│  SecurityAgent 1──* PentestFinding                                          │
│  SecurityAgent 1──* ComplianceControl                                       │
│                                                                             │
│  ScanResult 1──* Vulnerability                                              │
│  Vulnerability *──* SecurityFinding (cross-reference)                       │
│                                                                             │
│  Incident 1──* TimelineEntry                                                │
│  Incident 1──* ContainmentAction                                            │
│  Incident 1──* IOC                                                          │
│  Incident 1──0..1 Playbook                                                  │
│                                                                             │
│  ComplianceFramework 1──* ComplianceControl                                 │
│  ComplianceControl *──* Evidence                                            │
│                                                                             │
│  PentestScope 1──* PentestFinding                                           │
│  PentestScope 1──* ScanResult                                               │
│  PentestFinding 1──* Remediation                                             │
│                                                                             │
│  ThreatModel 1──* Threat                                                    │
│  Threat 1──* AttackPath                                                     │
│  Threat 1──* Mitigation                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6. Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Type System | dataclasses, Enum, typing | Type safety and documentation |
| Logging | Python logging module | Audit trail and debugging |
| Hashing | hashlib, secrets | Secure hash generation, token creation |
| Pattern Matching | re (regex) | SAST and secrets detection patterns |
| Data Format | JSON-compatible dicts | Serialization and API responses |
| ID Generation | uuid4, secrets.randbelow | Unique identifier creation |
| Date/Time | datetime, timedelta | Timestamps and duration calculations |
| Math | Standard library | Score calculations, statistics |
| File I/O | pathlib, json | Configuration and state persistence |
| Testing | unittest, pytest | Unit and integration tests |
| Documentation | Markdown | Architecture and API documentation |

## 7. Security Considerations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Security Principles for the Security Agent itself                         │
│                                                                             │
│  1. Input Validation                                                        │
│     - All scan inputs are treated as untrusted text                         │
│     - No arbitrary code execution (eval/exec detected, never called)       │
│     - Input sanitization before pattern matching                            │
│                                                                             │
│  2. Secret Handling                                                         │
│     - Secrets scanner does not log or persist found credentials            │
│     - Detected secrets are redacted in reports                              │
│     - No hardcoded credentials in agent code                                │
│                                                                             │
│  3. Audit Trail                                                             │
│     - All incident actions are timestamped and attributed                   │
│     - Timeline entries cannot be modified after creation                    │
│     - State transitions are logged with before/after values                 │
│                                                                             │
│  4. Least Privilege                                                         │
│     - Scanner operates in read-only mode on source code                     │
│     - Each subsystem only accesses its own data                             │
│     - No cross-subsystem data mutation                                      │
│                                                                             │
│  5. Data Protection                                                         │
│     - Vulnerability data encrypted at rest (production)                     │
│     - Incident data access-controlled by role                               │
│     - PII in reports redacted by default                                    │
│                                                                             │
│  6. Secure Defaults                                                         │
│     - Error states default to secure (deny, don't allow)                   │
│     - New controls marked as not-implemented until verified                 │
│     - Compliance scores start at 0 until evidence provided                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 8. Scalability

| Dimension | Strategy | Implementation |
|-----------|----------|----------------|
| Scan Volume | Pluggable engine registry | New engines added without modifying scanner core |
| Framework Growth | New compliance frameworks added to `FRAMEWORKS` dict | Declarative framework definition, zero code changes |
| Playbook Expansion | JSON-driven playbook definitions | Playbooks loaded from config, not hardcoded |
| Finding Volume | Findings stored in lists; aggregate via statistics | Statistics calculated on-demand, not pre-computed |
| Concurrent Scans | Thread-safe by design | No shared mutable state between scan instances |
| Incident Volume | In-memory store with optional persistence | Migrate to database for high-volume deployments |
| Report Generation | Lazy evaluation with caching | Reports generated on-demand, cached for repeated access |
| Multi-tenant | Tenant isolation via partition keys | Each tenant gets isolated data partitions |

## 9. Extension Points

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Extension Points                                                          │
│                                                                             │
│  1. New Scan Engine                                                         │
│     - Implement `_scan_<name>(code, language) -> List[Vulnerability]`      │
│     - Register in `_register_engines()` method                             │
│     - Add ScanType enum value                                               │
│                                                                             │
│  2. New Compliance Framework                                                │
│     - Add entry to `ComplianceAuditor.FRAMEWORKS` dict                    │
│     - Define controls with IDs, names, descriptions                        │
│     - Optionally add custom scoring logic                                   │
│                                                                             │
│  3. New Incident Playbook                                                   │
│     - Add entry to `IncidentResponder._load_playbooks()`                  │
│     - Define phases, actions, responsible roles                            │
│     - Add escalation triggers if needed                                     │
│                                                                             │
│  4. Custom Severity Weights                                                 │
│     - Override `calculate_security_score()` weights dict                   │
│     - Adjust CVSS score normalization                                       │
│     - Add custom severity categories                                        │
│                                                                             │
│  5. New MITRE Mappings                                                      │
│     - Extend `ThreatModeler.generate_stride_threats()` templates          │
│     - Add ATT&CK technique IDs to threat definitions                       │
│     - Map mitigations to ATT&CK countermeasures                            │
│                                                                             │
│  6. Custom Report Formats                                                   │
│     - Extend ReportGenerator with new format methods                        │
│     - Add PDF, HTML, or CSV export                                         │
│     - Customize report templates                                            │
│                                                                             │
│  7. Integration Hooks                                                       │
│     - Pre-scan hook for input validation                                    │
│     - Post-scan hook for finding enrichment                                 │
│     - On-incident hook for external notification                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 10. Performance Characteristics

| Metric | Target | Optimization |
|--------|--------|--------------|
| Single-file SAST scan | < 500ms | Pre-compiled regex patterns |
| Full security analysis | < 2s | Parallel engine execution |
| Compliance assessment | < 100ms | Cached framework definitions |
| Incident creation | < 50ms | In-memory state, lazy persistence |
| Dashboard generation | < 200ms | Cached aggregations |
| Memory per 1000 findings | < 50MB | Efficient dataclass storage |
| Threat model generation | < 150ms | Pre-built threat templates |
| Pentest report generation | < 300ms | Template-based rendering |

## Appendix A: Scoring Algorithm

```
Security Score Calculation:

1. Severity Weights:
   CRITICAL = 10 points
   HIGH     = 5 points
   MEDIUM   = 2 points
   LOW      = 1 point
   INFO     = 0 points

2. Raw Score = Σ(severity_weight × confidence) for all findings

3. Normalized Score:
   - Start at 100
   - Deduct raw_score (capped at 100)
   - Result: 0-100 scale

4. Grade Mapping:
   A: 90-100  (Excellent)
   B: 80-89   (Good)
   C: 70-79   (Fair)
   D: 60-69   (Poor)
   F: 0-59    (Critical)

5. Risk Level:
   - score >= 90: low risk
   - score >= 70: medium risk
   - score >= 50: high risk
   - score < 50:  critical risk
```

## Appendix B: Incident Response SLA

```
┌──────────────┬─────────────────┬───────────────────┬──────────────────┐
│  Severity    │  First Response  │  Containment      │  Resolution      │
├──────────────┼─────────────────┼───────────────────┼──────────────────┤
│  CRITICAL    │  15 minutes      │  1 hour           │  4 hours         │
│  HIGH        │  1 hour          │  4 hours          │  24 hours        │
│  MEDIUM      │  4 hours         │  24 hours         │  72 hours        │
│  LOW         │  24 hours        │  72 hours         │  1 week          │
└──────────────┴─────────────────┴───────────────────┴──────────────────┘

SLA Calculation:
  response_time = first_timeline_entry.timestamp - incident.created_at
  containment_time = CONTAINED_status.timestamp - incident.created_at
  resolution_time = CLOSED_status.timestamp - incident.created_at
  
  SLA Breach = actual_time > sla_target
```
