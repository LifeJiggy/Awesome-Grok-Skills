# Compliance Audit Agent — Architecture

## 1. Overview

The Compliance Audit Agent is a comprehensive regulatory compliance and audit management system designed to manage the full compliance lifecycle from framework selection through assessment, audit execution, risk management, evidence collection, and remediation tracking. It supports SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001, CCPA, and custom frameworks with built-in control libraries and cross-framework mapping.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE AUDIT AGENT v2.0                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                      COMPLIANCE LAYER                             │  │
│  │  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────────────┐  │  │
│  │  │Framework │ │   Risk       │ │Remediation│ │   Evidence     │  │  │
│  │  │ Manager  │ │  Assessment  │ │ Tracker   │ │   Manager      │  │  │
│  │  └────┬─────┘ └──────┬───────┘ └────┬─────┘ └───────┬────────┘  │  │
│  │       │              │              │               │             │  │
│  │  ┌────┴─────┐ ┌──────┴───────┐ ┌────┴─────┐ ┌──────┴────────┐  │  │
│  │  │  Audit   │ │   Policy     │ │ Finding  │ │ Dashboard     │  │  │
│  │  │ Manager  │ │   Manager    │ │ Manager  │ │ Generator     │  │  │
│  │  └──────────┘ └──────────────┘ └──────────┘ └───────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│  ┌─────────────────────────────────┴──────────────────────────────────┐  │
│  │                         DATA LAYER                                 │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │  │
│  │  │Controls  │ │  Risks   │ │Evidence  │ │Policies  │            │  │
│  │  │& Findings│ │ Register │ │  Store   │ │          │            │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

## 2. System Components

### 2.1 Compliance Framework Manager
- Maintains control libraries for SOC2, GDPR, HIPAA, PCI DSS, ISO 27001
- Cross-framework control mapping
- Framework-specific requirement tracking
- Control status management (not assessed → compliant/non-compliant)

### 2.2 Risk Assessment Engine
- Threat-vulnerability-impact risk modeling
- Likelihood × Impact scoring with automatic severity classification
- Residual risk tracking after mitigation
- Risk register with trend analysis
- Risk level classification (negligible → critical)

### 2.3 Remediation Tracker
- Finding lifecycle management (open → in_progress → verified → closed)
- Deadline tracking with overdue detection
- Assignment management with owner accountability
- Progress reporting with completion rates
- Status history logging

### 2.4 Evidence Manager
- Multi-type evidence collection (documents, screenshots, logs, configs)
- SHA-256 integrity hashing
- Control and finding association
- Verification workflow (collect → verify → archive)
- Evidence statistics and coverage tracking

### 2.5 Policy Manager
- Policy lifecycle management (draft → review → approved → active)
- Review scheduling with next-review dates
- Framework alignment tracking
- Template library for common policy categories
- Training and acknowledgment requirements

### 2.6 Audit Manager
- Audit lifecycle (planned → in_progress → fieldwork → reporting → complete)
- Scope definition with system/department inclusion/exclusion
- Finding aggregation per audit
- Compliance rate calculation
- Evidence collection tracking

### 2.7 Dashboard Generator
- Unified compliance status view
- Risk summary with level distribution
- Remediation progress with completion rates
- Evidence collection statistics
- Policy lifecycle status

## 3. Data Flow

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│Framework│───>│  Assess  │───>│  Audit   │───>│  Report  │
│Selection│    │Compliance│    │ Execute  │    │ Generate │
└─────────┘    └────┬─────┘    └────┬─────┘    └──────────┘
                    │               │
                    v               v
             ┌──────────┐    ┌──────────┐
             │   Risk   │    │ Evidence │
             │Assessment│    │Collection│
             └────┬─────┘    └────┬─────┘
                  │               │
                  v               v
             ┌──────────────────────────┐
             │    Remediation Plan      │
             │  (Findings → Actions)    │
             └──────────────┬───────────┘
                            │
                            v
             ┌──────────────────────────┐
             │   Verification &         │
             │   Continuous Compliance  │
             └──────────────────────────┘
```

### 3.1 Detailed Compliance Lifecycle

1. **Framework Selection**: Choose applicable compliance framework(s)
2. **Gap Assessment**: Evaluate current controls against framework requirements
3. **Risk Identification**: Identify and assess compliance risks
4. **Audit Planning**: Define scope, team, timeline for formal audit
5. **Evidence Collection**: Gather evidence for each control
6. **Finding Documentation**: Record non-compliance issues with severity
7. **Remediation Planning**: Assign owners and deadlines for findings
8. **Remediation Execution**: Track progress on corrective actions
9. **Verification**: Verify remediation effectiveness
10. **Reporting**: Generate compliance dashboard and audit reports
11. **Continuous Monitoring**: Ongoing compliance checks and reviews

## 4. Design Patterns

### 4.1 Strategy Pattern
Risk scoring uses interchangeable calculation strategies based on framework-specific severity models (CVSS for vulnerabilities, custom for operational risks).

### 4.2 Repository Pattern
`EvidenceManager` acts as a repository for evidence artifacts, providing CRUD operations with query capabilities (by control, finding, type).

### 4.3 State Machine Pattern
Findings follow a defined state machine: OPEN → IN_PROGRESS → BLOCKED → PENDING_VERIFICATION → VERIFIED → CLOSED. Invalid transitions are rejected.

### 4.4 Template Method Pattern
Framework assessment follows a template: load controls → evaluate each → aggregate score → identify gaps → generate recommendations. Framework-specific logic fills in the details.

### 4.5 Composite Pattern
Audits are composed of scopes, controls, findings, and evidence — each independently manageable but aggregating into the audit record.

### 4.6 Chain of Responsibility
Compliance assessment chains through controls: each control is evaluated, gaps are accumulated, and the aggregate determines overall compliance status.

## 5. Component Deep Dive

### 5.1 Compliance Assessment Flow

```
┌─────────────────────────────────────────────────────────┐
│              Compliance Assessment Flow                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Input: Framework + Control Scores                      │
│         {CC1.1: 0.9, CC6.1: 0.3, ...}                  │
│                    │                                    │
│                    v                                    │
│  ┌─────────────────────────────┐                       │
│  │ Load Framework Controls     │                       │
│  │ SOC2: 16 controls           │                       │
│  │ GDPR: 12 controls           │                       │
│  │ HIPAA: 11 controls          │                       │
│  │ PCI: 12 controls            │                       │
│  └──────────────┬──────────────┘                       │
│                 │                                      │
│                 v                                      │
│  ┌─────────────────────────────┐                       │
│  │ Classify Each Control       │                       │
│  │ Score ≥ 0.8 → Compliant     │                       │
│  │ Score ≥ 0.5 → Partial       │                       │
│  │ Score < 0.5 → Non-compliant │                       │
│  └──────────────┬──────────────┘                       │
│                 │                                      │
│                 v                                      │
│  ┌─────────────────────────────┐                       │
│  │ Calculate Rates             │                       │
│  │ Compliance = Compliant/Total│                       │
│  │ Partial   = Partial/Total   │                       │
│  └──────────────┬──────────────┘                       │
│                 │                                      │
│                 v                                      │
│  ┌─────────────────────────────┐                       │
│  │ Determine Status            │                       │
│  │ ≥ 90% → COMPLIANT           │                       │
│  │ ≥ 70% → PARTIALLY_COMPLIANT │                       │
│  │ < 70% → NON_COMPLIANT       │                       │
│  └──────────────┬──────────────┘                       │
│                 │                                      │
│                 v                                      │
│  Output: {status, rate, gaps[], recommendations[]}    │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Risk Assessment Model

```
┌─────────────────────────────────────────────────────┐
│              Risk Assessment Matrix                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Risk Score = Likelihood × Impact                   │
│                                                     │
│  ┌───────────────────────────────────────────┐      │
│  │  Impact →                                 │      │
│  │  0.0  0.2  0.4  0.6  0.8  1.0            │      │
│  │ ┌────┬────┬────┬────┬────┬────┐           │      │
│  │ │ NE │ NE │ LO │ LO │ ME │ ME │  0.2      │      │
│  │ ├────┼────┼────┼────┼────┼────┤           │      │
│  │ │ NE │ LO │ LO │ ME │ ME │ HI │  0.4      │      │
│  │ ├────┼────┼────┼────┼────┼────┤           │      │
│  │ │ LO │ LO │ ME │ ME │ HI │ HI │  0.6  L   │      │
│  │ ├────┼────┼────┼────┼────┼────┤  i        │      │
│  │ │ LO │ ME │ ME │ HI │ HI │ CR │  0.8  k   │      │
│  │ ├────┼────┼────┼────┼────┼────┤  e        │      │
│  │ │ ME │ ME │ HI │ HI │ CR │ CR │  1.0  l   │      │
│  │ └────┴────┴────┴────┴────┴────┘           │      │
│  └───────────────────────────────────────────┘      │
│                                                     │
│  NE = Negligible  ME = Medium  CR = Critical        │
│  LO = Low         HI = High                         │
│                                                     │
│  Residual Risk = Risk after existing controls       │
└─────────────────────────────────────────────────────┘
```

### 5.3 Finding Lifecycle State Machine

```
┌──────────────────────────────────────────────────────────┐
│                 Finding State Machine                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────┐   assign   ┌────────────┐                   │
│  │  OPEN  │──────────>│ IN_PROGRESS │                   │
│  └────────┘            └─────┬──────┘                   │
│       │                      │                          │
│       │ blocked              │ complete                 │
│       v                      v                          │
│  ┌─────────┐          ┌──────────────────┐              │
│  │ BLOCKED │          │PENDING_VERIFICA- │              │
│  └────┬────┘          │     TION         │              │
│       │               └────────┬─────────┘              │
│       │ unblocked              │ verified               │
│       │                        v                        │
│       └──────────────>  ┌──────────┐                    │
│                         │ VERIFIED │                     │
│                         └────┬─────┘                     │
│                              │ close                     │
│                              v                           │
│                         ┌────────┐                       │
│                         │ CLOSED │                       │
│                         └────────┘                       │
│                                                          │
│  Alternative: ACCEPTED_RISK (from any non-closed state) │
└──────────────────────────────────────────────────────────┘
```

## 6. Framework Control Libraries

### 6.1 SOC 2 Trust Service Criteria

| Category | Controls | Focus Area |
|----------|----------|------------|
| CC1 - Control Environment | CC1.1, CC1.2 | Integrity, ethics, oversight |
| CC2 - Communication | CC2.1 | Information quality, internal communication |
| CC3 - Risk Assessment | CC3.1 | Objective setting, risk identification |
| CC4 - Monitoring | CC4.1 | Ongoing evaluations, deficiency remediation |
| CC5 - Control Activities | CC5.1 | Policy deployment, technology controls |
| CC6 - Logical Access | CC6.1-CC6.3 | Access management, user lifecycle |
| CC7 - System Operations | CC7.1-CC7.2 | Vulnerability management, incident detection |
| CC8 - Change Management | CC8.1 | Change authorization, testing, approval |
| CC9 - Risk Mitigation | CC9.1 | Risk identification, mitigation activities |
| A1 - Availability | A1.1 | Capacity management, disaster recovery |
| PI - Processing Integrity | PI1.1 | Data quality, error handling |
| PR - Privacy | PR1.1 | Data protection, consent management |

### 6.2 GDPR Articles

| Article | Focus Area |
|---------|-----------|
| Art.5 | Processing principles (lawfulness, fairness, transparency) |
| Art.6 | Lawful basis for processing |
| Art.12 | Transparent communication |
| Art.15-17 | Data subject rights (access, portability, erasure) |
| Art.25 | Data protection by design and by default |
| Art.30 | Records of processing activities |
| Art.32 | Security of processing |
| Art.33-34 | Breach notification (72 hours) |
| Art.35 | Data Protection Impact Assessment |
| Art.37 | Data Protection Officer designation |
| Art.44-49 | International data transfers |

### 6.3 HIPAA Safeguards

| Category | Requirements |
|----------|-------------|
| Administrative | Security management, workforce security, training |
| Physical | Facility access, workstation use, device controls |
| Technical | Access control, audit controls, integrity, authentication, transmission security |

### 6.4 PCI DSS Requirements

| Requirement | Focus Area |
|-------------|-----------|
| Req 1 | Firewall configuration |
| Req 2 | Default credentials eliminated |
| Req 3 | Stored data minimization |
| Req 4 | Encryption in transit |
| Req 5 | Anti-malware |
| Req 6 | Secure development |
| Req 7 | Need-to-know access |
| Req 8 | Unique identification |
| Req 9 | Physical access controls |
| Req 10 | Audit logging |
| Req 11 | Vulnerability testing |
| Req 12 | Security policies |

## 7. Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.10+ | Type safety, dataclass support |
| Data Models | dataclasses | Typed, serializable, composable |
| Hashing | hashlib.sha256 | Evidence integrity verification |
| Frameworks | Built-in libraries | SOC2, GDPR, HIPAA, PCI DSS |
| Search | In-memory dict | Fast control/evidence lookup |
| Serialization | to_dict methods | JSON-compatible output |

## 8. Security Considerations

### 8.1 Data Protection
- Compliance data may contain sensitive security information
- Evidence files tracked by hash for integrity
- Access to audit results restricted to authorized personnel
- No persistence of raw audit data without encryption

### 8.2 Evidence Integrity
- SHA-256 hashes computed on evidence collection
- Verification timestamps recorded
- Chain of custody maintained through collection history
- Tamper detection through hash comparison

### 8.3 Audit Trail
- All state changes logged with timestamps and actors
- Finding lifecycle fully traceable
- Policy review history maintained
- Risk assessment changes recorded

## 9. Scalability

### 9.1 Current Architecture
- In-memory storage limits to ~10 concurrent audits
- ~10,000 controls across all frameworks
- ~100,000 evidence items per audit
- Single-threaded execution

### 9.2 Scaling Strategies
- **Database backend**: PostgreSQL with proper schema for audit data
- **Document store**: MongoDB for evidence metadata and large documents
- **Search index**: Elasticsearch for control/evidence search
- **Async processing**: Background jobs for evidence verification
- **Multi-tenant**: Namespace isolation for multiple organizations

## 10. Integration Points

```
┌─────────────────┐     ┌──────────────────┐
│ Compliance      │────>│ GRC Platforms    │
│ Agent           │     │ (ServiceNow,     │
│                 │     │  Archer, OneTrust)│
└────────┬────────┘     └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Vulnerability    │
         │             │ Scanners        │
         │             │ (Qualys, Nessus) │
         │             └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ SIEM Systems     │
         │             │ (Splunk, ELK)    │
         │             └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Policy Engines   │
         │             │ (Open Policy     │
         │             │  Agent)          │
         │             └──────────────────┘
         │
         └────────────>┌──────────────────┐
                       │ Cloud Security   │
                       │ (AWS Config,     │
                       │  Azure Policy)   │
                       └──────────────────┘
```

## 11. Error Handling

| Error Type | Handling Strategy |
|-----------|-------------------|
| Unknown framework | Return available frameworks list |
| Invalid control ID | Return error with valid IDs |
| Invalid state transition | Reject with current state info |
| Duplicate evidence | Allow, flag as duplicate |
| Missing required fields | Return validation error with details |
| Remediation deadline past | Flag as overdue in reports |

## 12. Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Compliance assessment | < 500ms | Per framework |
| Risk calculation | < 20ms | Per risk item |
| Finding status update | < 30ms | State machine check |
| Evidence collection | < 100ms | With hash computation |
| Dashboard generation | < 1s | Full compliance view |
| Audit preparation | < 200ms | Scope + control mapping |

## 13. Testing Strategy

### Unit Tests
- Risk score calculation accuracy
- Finding state machine transitions
- Compliance rate calculation
- Evidence hash computation
- Control classification logic

### Integration Tests
- Full assessment → audit → remediation flow
- Multi-framework compliance evaluation
- Evidence collection and verification cycle
- Policy lifecycle management

### Acceptance Tests
- SOC 2 assessment produces expected control evaluations
- GDPR assessment covers all required articles
- HIPAA safeguard classification accuracy
- PCI DSS requirement mapping completeness
