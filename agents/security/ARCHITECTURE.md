# Security Agent Architecture

## 1. Overview

The Security Agent implements a defense-in-depth architecture for enterprise security operations. It orchestrates five core subsystems—vulnerability scanning, threat modeling, compliance auditing, incident response, and penetration testing—behind a unified `SecurityAgent` facade.

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

Multi-engine static analysis scanner with pluggable detection backends.

```
┌──────────────────────────────────────────┐
│          VulnerabilityScanner            │
├──────────────────────────────────────────┤
│  Engine Registry (Dict[ScanType, Fn])   │
│  ┌────────┐ ┌────────┐ ┌────────┐      │
│  │  SAST  │ │ Secrets│ │  SCA   │      │
│  └────┬───┘ └────┬───┘ └────┬───┘      │
│       │          │          │            │
│  ┌────┴──────────┴──────────┴────┐      │
│  │      Finding Aggregator       │      │
│  └───────────────────────────────┘      │
│  CVE Database (Dict[str, Dict])         │
│  Scan History (List[Dict])              │
│  Statistics Calculator                  │
└──────────────────────────────────────────┘
```

**Scan engines:**
- **SAST**: Pattern-based detection for injection, XSS, SSRF, command injection, path traversal
- **Secrets**: Regex-based credential detection (API keys, tokens, passwords, cloud keys)
- **SCA**: Dependency version vulnerability matching
- **Container**: Dockerfile/YAML security posture analysis

### 2.2 ThreatModeler

STRIDE-based threat modeling with attack tree construction.

```
┌─────────────────────────────────────────────┐
│             ThreatModeler                   │
├─────────────────────────────────────────────┤
│  Components Registry                        │
│  Data Flow Graph                            │
│  Trust Zone Definitions                     │
│  STRIDE Threat Generator                    │
│  Attack Tree Builder                        │
│  Threat Summary Aggregator                  │
└─────────────────────────────────────────────┘
```

**STRIDE categories:**
| Category | Description | Typical Mitigation |
|----------|-------------|-------------------|
| Spoofing | Identity impersonation | mTLS, certificate pinning |
| Tampering | Data modification | HMAC, digital signatures |
| Repudiation | Action denial | Audit logging |
| Info Disclosure | Data exposure | Encryption, RBAC |
| DoS | Availability disruption | Rate limiting, CDN |
| EoP | Privilege escalation | Least privilege, RBAC |

### 2.3 ComplianceAuditor

Multi-framework compliance assessment engine.

```
┌──────────────────────────────────────────────┐
│            ComplianceAuditor                 │
├──────────────────────────────────────────────┤
│  Framework Registry                          │
│  ┌──────┬──────────┬────────┬──────┐        │
│  │ SOC2 │ ISO27001 │ PCI_DSS│ NIST │        │
│  └──────┴──────────┴────────┴──────┘        │
│  ┌──────┬──────────┐                         │
│  │ HIPAA│   GDPR   │                         │
│  └──────┴──────────┘                         │
│  Evidence Evaluator                          │
│  Score Calculator                            │
│  Report Generator                            │
└──────────────────────────────────────────────┘
```

### 2.4 IncidentResponder

Automated incident lifecycle management.

```
┌──────────────────────────────────────────────┐
│          IncidentResponder                   │
├──────────────────────────────────────────────┤
│  Playbook Engine                             │
│  ┌─────────────┬────────────┬──────────┐    │
│  │ Data Breach │ Ransomware │ Phishing │    │
│  └─────────────┴────────────┴──────────┘    │
│  Incident Store (List[Incident])             │
│  Timeline Tracker                            │
│  IOC Registry                                │
│  MTTR Calculator                             │
└──────────────────────────────────────────────┘
```

**Incident lifecycle:**
```
OPEN → TRIAGED → INVESTIGATING → CONTAINED → ERADICATED → RECOVERED → CLOSED
```

### 2.5 PenetrationTester

Penetration test orchestration and reporting.

```
┌──────────────────────────────────────────────┐
│          PenetrationTester                   │
├──────────────────────────────────────────────┤
│  Scope Manager                               │
│  ┌──────────────┬──────────────┐             │
│  │ Network Scan │  Web Scan    │             │
│  └──────────────┴──────────────┘             │
│  Finding Store (List[PentestFinding])         │
│  Report Generator                            │
│  Scope Registry                              │
└──────────────────────────────────────────────┘
```

## 3. Data Flow

```
Source Code / Config
        │
        ▼
┌───────────────────┐
│ Vulnerability     │──── Findings ────┐
│ Scanner           │                  │
└───────────────────┘                  │
                                       │
┌───────────────────┐                  ▼
│ Threat Modeler    │──── Threats ──► SecurityAgent ──► Dashboard
│                   │                  ▲
└───────────────────┘                  │
                                       │
┌───────────────────┐                  │
│ Compliance Auditor│──── Controls ────┘
│                   │
└───────────────────┘

┌───────────────────┐
│ Incident Responder│──── Incidents ──► SecurityAgent ──► Dashboard
└───────────────────┘

┌───────────────────┐
│ Penetration Tester│──── Findings ───► SecurityAgent ──► Dashboard
└───────────────────┘
```

## 4. Design Patterns

| Pattern | Application |
|---------|-------------|
| **Facade** | `SecurityAgent` provides unified API over five subsystems |
| **Strategy** | Scan engines registered as pluggable callbacks |
| **Observer** | Incident timeline tracks all state transitions |
| **Template Method** | Playbooks define phase-action templates |
| **Registry** | Compliance frameworks stored in class-level dict |
| **Dataclass DTOs** | `Vulnerability`, `Incident`, `PentestFinding` as value objects |

## 5. Data Models

### Core Entities

```python
@dataclass
class Vulnerability:
    id: str                    # Unique identifier
    name: str                  # Human-readable name
    type: VulnerabilityType    # OWASP category
    severity: ThreatLevel      # CRITICAL/HIGH/MEDIUM/LOW/INFO
    cvss_score: float          # 0.0 - 10.0
    cwe_id: Optional[str]      # CWE reference
    status: FindingStatus      # OPEN → RESOLVED lifecycle
    confidence: float          # 0.0 - 1.0 detection confidence
```

### Relationship Diagram

```
Vulnerability 1──* SecurityFinding
Incident       1──* TimelineEntry
ComplianceFramework 1──* ComplianceControl
PentestScope   1──* PentestFinding
ScanResult     1──* Vulnerability
```

## 6. Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | dataclasses, Enum, typing |
| Logging | Python logging module |
| Hashing | hashlib, secrets |
| Pattern Matching | re (regex) |
| Data Format | JSON-compatible dicts |
| ID Generation | uuid4, secrets.randbelow |

## 7. Security Considerations

- **Input Validation**: All scan inputs are treated as untrusted text
- **No Arbitrary Execution**: `eval()`/`exec()` are detected, never called
- **Secret Handling**: Secrets scanner does not log or persist found credentials
- **Audit Trail**: All incident actions are timestamped and attributed
- **Least Privilege**: Scanner operates in read-only mode on source code

## 8. Scalability

| Dimension | Strategy |
|-----------|----------|
| Scan Volume | Pluggable engine registry allows horizontal engine addition |
| Framework Growth | New compliance frameworks added to `FRAMEWORKS` dict |
| Playbook Expansion | JSON-driven playbook definitions |
| Finding Volume | Findings stored in lists; aggregate via statistics methods |
| Concurrent Scans | Thread-safe by design (no shared mutable state between scans) |

## 9. Extension Points

1. **New Scan Engine**: Implement `_scan_<name>` method and register in `_register_engines()`
2. **New Compliance Framework**: Add entry to `ComplianceAuditor.FRAMEWORKS`
3. **New Playbook**: Add entry to `IncidentResponder._load_playbooks()`
4. **Custom Severity Weights**: Override `calculate_security_score()` weights dict
5. **New MITRE Mappings**: Extend `ThreatModeler.generate_stride_threats()` templates

## 10. Performance Characteristics

| Metric | Target |
|--------|--------|
| Single-file SAST scan | < 500ms |
| Full security analysis | < 2s |
| Compliance assessment | < 100ms |
| Incident creation | < 50ms |
| Dashboard generation | < 200ms |
| Memory per 1000 findings | < 50MB |
