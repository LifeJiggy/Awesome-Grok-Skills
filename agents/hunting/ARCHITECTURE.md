# Hunting Agent — System Architecture

## 1. Executive Summary

The Hunting Agent is a comprehensive threat hunting platform providing IOC management, hypothesis-driven hunting, log analysis, network forensics, detection engineering, alert management, and threat intelligence correlation. It is designed for security operations centers (SOC) and threat hunting teams.

---

## 2. Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Component Deep Dives](#3-component-deep-dives)
4. [Data Flow Diagrams](#4-data-flow-diagrams)
5. [MITRE ATT&CK Mapping](#5-mitre-attack-mapping)
6. [Detection Rule Lifecycle](#6-detection-rule-lifecycle)
7. [Design Patterns](#7-design-patterns)
8. [Tech Stack](#8-tech-stack)
9. [Security Considerations](#9-security-considerations)
10. [Scalability & Performance](#10-scalability--performance)
11. [Integration Points](#11-integration-points)
12. [Deployment Architecture](#12-deployment-architecture)
13. [Monitoring & Observability](#13-monitoring--observability)
14. [Data Models](#14-data-models)
15. [Disaster Recovery](#15-disaster-recovery)
16. [Extension Points](#16-extension-points)
17. [Glossary](#17-glossary)
18. [Appendix: Design Decisions](#18-appendix-design-decisions)

---

## 3. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         HUNTING AGENT                                     │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │    IOC       │  │     Log      │  │   Network    │  │ Detection  │  │
│  │   Manager    │  │   Analyzer   │  │   Analyzer   │  │   Engine   │  │
│  │              │  │              │  │              │  │            │  │
│  │ • Lifecycle  │  │ • Ingestion  │  │ • Flow analysis│ │ • Sigma    │  │
│  │ • STIX export│  │ • Anomaly    │  │ • JA3 finger- │  │   rules    │  │
│  │ • Correlation│  │   detection  │  │   printing    │  │ • Matching  │  │
│  │ • Search     │  │ • Volume     │  │ • Lateral    │  │ • Lifecycle │  │
│  │ • Statistics │  │   analysis   │  │   movement   │  │ • Tuning    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │    Hunt      │  │    Alert     │  │  Threat      │                  │
│  │ Orchestrator │  │   Manager    │  │   Intel      │                  │
│  │              │  │              │  │              │                  │
│  │ • Hypothesis │  │ • Triage     │  │ • Actor      │                  │
│  │ • Phases     │  │ • Assignment │  │   profiles   │                  │
│  │ • Reporting  │  │ • Resolution │  │ • IOC        │                  │
│  │ • MITRE map  │  │ • Metrics    │  │   correlation│                  │
│  │ • Analytics  │  │ • SLA track  │  │ • Tracking   │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │    Data Models (IOC, Hunt, LogEntry, Flow, Sigma, Alert, Actor)  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Deep Dives

### 4.1 IOC Manager

Indicator of Compromise lifecycle management with STIX export.

**Responsibilities:**
- Ingest and store IOCs of various types (IP, domain, URL, hash, email, mutex, registry, etc.)
- Track IOC lifecycle from creation through expiration
- Support false-positive marking and review workflows
- Export IOCs in STIX 2.1 format for interoperability
- Search and filter IOCs by type, threat level, tags, and time range
- Calculate IOC statistics for dashboarding

**Data Flow:**
```
External Feed / Analyst Input
         │
         ▼
┌─────────────────┐
│   IOC Manager    │
│                  │
│  ┌────────────┐  │
│  │  Ingest    │──┼──→ Validate → Normalize → Store
│  └────────────┘  │
│  ┌────────────┐  │
│  │  Search    │──┼──→ Filter → Rank → Return
│  └────────────┘  │
│  ┌────────────┐  │
│  │  Export    │──┼──→ STIX → JSON → Deliver
│  └────────────┘  │
│  ┌────────────┐  │
│  │  Stats     │──┼──→ Aggregate → Report
│  └────────────┘  │
└─────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `add_ioc(value, type, threat_level, confidence, source, tags)` | Register a new IOC |
| `search(query)` | Search IOCs by value or tag |
| `get_by_type(type)` | Filter IOCs by type |
| `get_active()` | Get all non-expired, active IOCs |
| `get_high_threat()` | Get HIGH and CRITICAL IOCs |
| `mark_false_positive(ioc_id)` | Mark IOC as false positive |
| `export_stix(ioc_ids)` | Export IOCs in STIX 2.1 format |
| `stats()` | Get IOC statistics by type and threat level |

---

### 4.2 Log Analyzer

Log ingestion, anomaly detection, and volume analysis.

**Responsibilities:**
- Ingest logs from multiple sources (firewall, IDS/IPS, proxy, DNS, endpoint, email, auth, cloud, application, database)
- Detect anomalies based on configurable rules
- Track volume by domain and source
- Maintain baseline statistics for anomaly threshold calculation
- Support time-based and pattern-based filtering

**Anomaly Detection Rules:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    Anomaly Detection Matrix                      │
├─────────────────────┬───────────────────────────────────────────┤
│ Anomaly Type        │ Detection Logic                           │
├─────────────────────┼───────────────────────────────────────────┤
│ VOLUME_SPIKE        │ bytes_sent > baseline × threshold        │
│ NEW_CONNECTION      │ First connection to destination           │
│ UNUSUAL_TIME        │ Connection outside business hours         │
│ UNUSUAL_PROTOCOL    │ Protocol not matching port standard       │
│ DATA_EXFIL          │ bytes_sent > 10MB threshold               │
│ LATERAL_MOVEMENT    │ Internal-to-internal unusual port/protocol│
│ PRIVILEGE_ESCALATION│ Auth event + privilege change pattern     │
│ C2_COMMUNICATION    │ Connection to known C2 port or IP         │
│ BRUTE_FORCE         │ > N auth failures in time window          │
│ DNS_TUNNEL          │ DNS query length > 50 characters          │
└─────────────────────┴───────────────────────────────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `add_log(entry)` | Ingest a log entry |
| `detect_anomalies()` | Run all anomaly detection rules |
| `get_connections_by_ip(ip)` | Get all connections for an IP |
| `get_volume_by_domain()` | Get data volume by domain |
| `get_unique_sources()` | Get unique source IPs |
| `summary()` | Get log analysis summary |

---

### 4.3 Network Analyzer

Flow analysis, JA3 fingerprinting, lateral movement detection.

**Responsibilities:**
- Ingest and analyze network flow data
- Detect anomalies in network traffic patterns
- Identify top talkers by bandwidth
- Track JA3 hashes for TLS fingerprinting
- Detect lateral movement between internal hosts
- Monitor encrypted traffic ratios

**Flow Analysis Pipeline:**
```
Raw Flow Data → Enrich → Classify → Analyze → Alert
     │              │         │         │        │
     ▼              ▼         ▼         ▼        ▼
  Parse         GeoIP     Direction  Anomaly  Generate
  Fields        Lookup    Label      Detection Alert
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `add_flow(flow)` | Add a network flow record |
| `detect_anomalies()` | Detect anomalous network flows |
| `get_top_talkers(n)` | Get top N talkers by bandwidth |
| `get_external_connections()` | Get all outbound connections |
| `get_ja3_duplicates()` | Find hosts with same JA3 hash |
| `stats()` | Get network flow statistics |

---

### 4.4 Detection Engine

Sigma rule management and log matching.

**Responsibilities:**
- Create and manage detection rules (Sigma format compatible)
- Match rules against log entries
- Track rule effectiveness (matches, false positives)
- Manage rule lifecycle from draft to deployment to retirement
- Support custom detection logic per rule

**Detection Rule Lifecycle:**
```
Draft → Tested → Deployed → Tuning → Retired
  │        │          │          │        │
  ▼        ▼          ▼          ▼        ▼
Review   Validation  Monitor  Adjust  Archive
         Results     Matches  Threshold
```

**Rule Evaluation Logic:**
```
┌─────────────────────────────────────────────────────────────┐
│                   Rule Evaluation Pipeline                    │
│                                                              │
│  Log Entry ──→ Parse Rule ──→ Match Conditions ──→ Result   │
│                    │                │                │       │
│                    ▼                ▼                ▼       │
│               Extract         Evaluate         Pass/Fail    │
│               Fields          Boolean          + Count      │
│                               Expression                    │
└─────────────────────────────────────────────────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `add_rule(title, logsource, detection_logic, severity)` | Create a detection rule |
| `match_logs(rule_id, logs)` | Match a rule against log entries |
| `get_deployed_rules()` | Get all deployed rules |
| `rules_stats()` | Get rule statistics |

---

### 4.5 Hunt Orchestrator

Hypothesis-driven hunting with phase tracking and reporting.

**Responsibilities:**
- Create and manage threat hunts
- Track hunt lifecycle through phases (Planning → Data Collection → Analysis → Investigation → Remediation → Reporting)
- Generate hunt reports with MITRE ATT&CK mapping
- Track confirmed vs. false-positive findings
- Support analyst assignment and collaboration

**Hunt Lifecycle:**
```
┌─────────┐     ┌───────────────┐     ┌──────────┐
│Planning │────▶│Data Collection│────▶│Analysis  │
└─────────┘     └───────────────┘     └────┬─────┘
                                           │
                      ┌────────────────────┘
                      ▼
              ┌──────────────┐     ┌──────────────┐
              │Investigation │────▶│ Remediation  │
              └──────────────┘     └──────┬───────┘
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │  Reporting   │
                                  └──────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `create_hunt(title, hypothesis, analyst, tactic, sources)` | Create a new threat hunt |
| `start_hunt(hunt_id)` | Begin a hunt |
| `complete_hunt(hunt_id, findings, confirmed)` | Complete a hunt with findings |
| `generate_report(hunt_id)` | Generate a hunt report |
| `get_active_hunts()` | Get all in-progress hunts |
| `hunt_stats()` | Get hunt statistics |

---

### 4.6 Alert Manager

Alert lifecycle management with assignment and resolution.

**Responsibilities:**
- Create alerts with severity classification
- Assign alerts to analysts for investigation
- Track alert resolution and false-positive rates
- Calculate alert metrics (time to resolution, SLA compliance)
- Support escalation workflows

**Alert Lifecycle:**
```
NEW ──→ INVESTIGATING ──→ ESCALATED ──→ RESOLVED
 │           │                              │
 │           └──→ FALSE_POSITIVE (terminal) │
 │                                          │
 └──→ RESOLVED (direct) ────────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `create_alert(title, severity, **kwargs)` | Create a new alert |
| `assign(alert_id, analyst)` | Assign alert to analyst |
| `resolve(alert_id, notes, false_positive)` | Resolve an alert |
| `get_open_alerts()` | Get all open alerts |
| `get_critical_alerts()` | Get all critical open alerts |
| `stats()` | Get alert statistics |

---

### 4.7 Threat Intel Correlator

Threat actor profiles and IOC correlation.

**Responsibilities:**
- Maintain threat actor profiles with techniques, tools, and IOCs
- Correlate IOCs across multiple actors
- Track active vs. dormant threat actors
- Map actors to MITRE ATT&CK techniques
- Support threat intelligence sharing

**Correlation Flow:**
```
IOC Set ──→ Compare ──→ Match ──→ Enrich ──→ Report
              │            │          │          │
              ▼            ▼          ▼          ▼
          Actor DB    Overlap     Actor      Correlation
          Lookup      Score       Details    Report
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `add_actor(name, **kwargs)` | Create a threat actor profile |
| `correlate_iocs(iocs)` | Find actors matching given IOCs |
| `get_active_actors()` | Get recently active actors |
| `get_by_sophistication(level)` | Filter actors by sophistication |

---

## 5. Data Flow Diagrams

### 5.1 End-to-End Hunting Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THREAT HUNTING PIPELINE                               │
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  Data    │    │  IOC     │    │  Log     │    │  Network │          │
│  │  Sources │───▶│  Manager │───▶│  Analyzer │───▶│  Analyzer │         │
│  │          │    │          │    │          │    │          │          │
│  │ • SIEM   │    │ • Track  │    │ • Detect │    │ • Flow   │          │
│  │ • Firewall│   │ • Search │    │ • Alert  │    │ • JA3    │          │
│  │ • Proxy  │    │ • Export │    │ • Volume │    │ • Lateral│          │
│  │ • Endpoint│   │          │    │          │    │          │          │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │
│       │               │               │               │                  │
│       └───────────────┴───────────────┴───────────────┘                  │
│                              │                                           │
│                              ▼                                           │
│                    ┌──────────────────┐                                  │
│                    │   Detection      │                                  │
│                    │   Engine         │                                  │
│                    │                  │                                  │
│                    │ • Sigma rules    │                                  │
│                    │ • Match logs     │                                  │
│                    │ • Track hits     │                                  │
│                    └────────┬─────────┘                                  │
│                             │                                            │
│              ┌──────────────┼──────────────┐                            │
│              ▼              ▼              ▼                            │
│    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                  │
│    │   Hunt       │ │   Alert      │ │  Threat      │                  │
│    │ Orchestrator │ │   Manager    │ │  Intel       │                  │
│    │              │ │              │ │              │                  │
│    │ • Hypothesis │ │ • Triage     │ │ • Correlate  │                  │
│    │ • Phases     │ │ • Assign     │ │ • Enrich     │                  │
│    │ • Report     │ │ • Resolve    │ │ • Track      │                  │
│    └──────────────┘ └──────────────┘ └──────────────┘                  │
│              │              │              │                            │
│              └──────────────┼──────────────┘                            │
│                             ▼                                            │
│                    ┌──────────────────┐                                  │
│                    │   Hunt Report    │                                  │
│                    │                  │                                  │
│                    │ • Executive      │                                  │
│                    │   summary        │                                  │
│                    │ • Findings       │                                  │
│                    │ • MITRE map      │                                  │
│                    │ • Recommendations│                                  │
│                    └──────────────────┘                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Alert Triage Flow

```
                    ┌──────────────────┐
                    │   New Alert      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Severity Check   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │   CRITICAL   │ │    HIGH      │ │  MEDIUM/LOW  │
     │              │ │              │ │              │
     │ Auto-assign  │ │ Queue for    │ │ Batch        │
     │ senior       │ │ review       │ │ processing   │
     │ analyst      │ │              │ │              │
     └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
            │                │                │
            ▼                ▼                ▼
     ┌──────────────────────────────────────────────┐
     │              Investigation                    │
     │                                               │
     │  • Review alert context                       │
     │  • Correlate with IOCs                        │
     │  • Check threat intelligence                  │
     │  • Map to MITRE ATT&CK                        │
     └──────────────────┬───────────────────────────┘
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
     ┌──────────────┐ ┌──────┐ ┌──────────────┐
     │  CONFIRMED   │ │FP    │ │  ESCALATED   │
     │  THREAT      │ │      │ │              │
     │              │ │      │ │              │
     │ Create hunt  │ │Close │ │ Notify mgmt  │
     │ Engage IR    │ │      │ │              │
     └──────────────┘ └──────┘ └──────────────┘
```

### 5.3 IOC Correlation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  IOC CORRELATION PIPELINE                     │
│                                                              │
│  Input IOCs ──→ Load Actor DB ──→ Compare ──→ Score ──→ Output│
│                                                              │
│  [IP, Domain,    [Actor A,        Set overlap   Match      │
│   Hash, etc]      Actor B,         computation   ranking    │
│                   Actor C]                                       │
│                                                              │
│  Score = (matched IOCs / total IOCs) × actor_confidence      │
│                                                              │
│  Results:                                                     │
│    Actor A: 3/5 IOCs matched → High confidence               │
│    Actor B: 1/5 IOCs matched → Low confidence                │
│    Actor C: 0/5 IOCs matched → No match                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. MITRE ATT&CK Mapping

```
Reconnaissance → Initial Access → Execution → Persistence
      ↓                                        ↓
Resource Development              Privilege Escalation
                                        ↓
                              Defense Evasion ← Credential Access
                                        ↓
                    Discovery → Lateral Movement → Collection
                                        ↓
                    C2 ←←←←←←←←←←←←←←←←←←←←← Exfiltration
                                        ↓
                                      Impact
```

**Tactic Coverage:**
| Tactic | Data Sources | Detection Methods |
|--------|-------------|-------------------|
| Reconnaissance | OSINT, DNS, Web logs | Port scan detection, web scraping patterns |
| Initial Access | Firewall, Proxy, Email | Phishing detection, exploit attempt signatures |
| Execution | Endpoint, Process logs | Script execution, WMI/PowerShell monitoring |
| Persistence | Registry, File system | Startup modification, scheduled task creation |
| Privilege Escalation | Auth logs, Process | Token manipulation, service creation |
| Defense Evasion | Endpoint, Log | Log clearing, binary padding detection |
| Credential Access | Auth logs, Memory | Brute force, credential dumping patterns |
| Discovery | Network, Endpoint | Network scanning, account enumeration |
| Lateral Movement | Network flows | SMB/RDP lateral, pass-the-hash detection |
| Collection | File system, Database | Data staging, screenshot capture |
| C2 | Network, DNS | C2 channel detection, DNS beaconing |
| Exfiltration | Network, Proxy | Data exfil volume, encryption detection |
| Impact | File system, Database | Ransomware, destructive activity |

---

## 7. Detection Rule Lifecycle

```
  Draft → Tested → Deployed → Tuning → Retired
```

**Effectiveness Score:** min(matches / 10, 1.0)

**Rule Lifecycle States:**
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  DRAFT   │───▶│ TESTED   │───▶│ DEPLOYED │───▶│ TUNING   │───▶│ RETIRED  │
│          │    │          │    │          │    │          │    │          │
│ Authoring│    │ Validate │    │ Active   │    │ Refining │    │ Archived │
│ Review   │    │ False +  │    │ Monitor  │    │ Threshold│    │ History  │
│ Approval │    │ True -   │    │ Alert    │    │ Update   │    │ kept     │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## 8. Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Repository** | IOC storage and retrieval | IOCManager |
| **Strategy** | Multiple anomaly detection algorithms | LogAnalyzer, NetworkAnalyzer |
| **Observer** | Alert notification on threshold breach | AlertManager |
| **State** | Alert lifecycle management | AlertManager |
| **Template Method** | Hunt phase progression | HuntOrchestrator |
| **Chain of Responsibility** | Rule evaluation pipeline | DetectionEngine |
| **Factory** | IOC creation from various sources | IOCManager |
| **Facade** | Unified interface to all components | HuntingAgent (orchestrator) |
| **Decorator** | Log enrichment pipeline | LogAnalyzer |
| **Composite** | Hunt report aggregation | HuntOrchestrator |

---

## 9. Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Structures | dataclasses, Enum, Dict, List |
| ID Generation | Sequential counters (IOC-00001, SIGMA-0001) |
| Logging | Python logging module |
| Hashing | hashlib (MD5, SHA1, SHA256) |
| Regex | re module for pattern matching |
| Statistics | statistics module for baseline calculation |
| Date/Time | datetime, timedelta |
| Serialization | JSON (STIX export) |
| Optional | SQLite, Redis, Elasticsearch |

---

## 10. Security Considerations

- **Input Validation**: All public methods validate inputs before processing
- **No External Calls**: All computation is local; no network calls during analysis
- **Audit Trail**: Full history of IOC changes, alert state transitions, and hunt activities
- **Access Control**: Method-level for sensitive operations (false positive marking, hunt completion)
- **Data Integrity**: Immutable log entries and flow records
- **IOC Confidence Scoring**: All IOCs carry confidence scores to prevent low-quality intelligence from polluting operations
- **STIX Compliance**: Export format follows STIX 2.1 specification for interoperability
- **False Positive Management**: Dedicated workflow to reduce alert fatigue

---

## 11. Scalability & Performance

| Dimension | Strategy |
|-----------|----------|
| IOC volume | Indexed by type, threat level, tags; in-memory Dict for O(1) lookup |
| Log volume | Time-bucketed processing; streaming anomaly detection |
| Flow volume | Batch processing with rolling windows |
| Rule evaluation | Pre-compiled rule logic; lazy evaluation |
| Alert volume | Severity-based prioritization; batch assignment |
| Hunt reports | Generated on-demand from hunt state |
| Actor correlation | Set-based overlap computation; caching |

**Performance Targets:**
| Operation | Target | Notes |
|-----------|--------|-------|
| IOC lookup | < 1ms | Dict-based O(1) |
| IOC search | < 10ms | Linear scan with string matching |
| Log anomaly detection | < 5ms per entry | Rule-based evaluation |
| Network flow analysis | < 10ms per flow | Threshold-based |
| Rule matching | < 2ms per log | Pre-compiled logic |
| Alert creation | < 1ms | Dict insertion |
| Hunt report generation | < 50ms | Template-based |
| Full status | < 100ms | All components aggregated |

---

## 12. Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION ARCHITECTURE                       │
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │   SIEM       │ ◀─────▶ │  Hunting     │                      │
│  │  (Splunk,    │  syslog │  Agent       │                      │
│  │   ELK, QRadar)│  API   │              │                      │
│  └──────────────┘         └──────────────┘                      │
│         │                       │                                │
│         │                       │                                │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  Threat      │ ◀─────▶ │  STIX/TAXII  │                      │
│  │  Intel       │  feeds  │  Export      │                      │
│  │  Platforms   │         │              │                      │
│  └──────────────┘         └──────────────┘                      │
│         │                       │                                │
│         │                       │                                │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  Ticketing   │ ◀─────▶ │  Alert       │                      │
│  │  System      │  webhook│  Manager     │                      │
│  │  (Jira, etc) │         │              │                      │
│  └──────────────┘         └──────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 13. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT TOPOLOGY                            │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Collector  │    │   Processing │    │   Storage    │      │
│  │   Nodes      │───▶│   Engine     │───▶│   Layer      │      │
│  │              │    │              │    │              │      │
│  │ • Log        │    │ • Anomaly    │    │ • IOC DB     │      │
│  │   collection │    │   detection  │    │ • Log store  │      │
│  │ • Flow       │    │ • Rule       │    │ • Alert      │      │
│  │   capture    │    │   matching   │    │   history    │      │
│  │ • Enrichment │    │ • Correlation│    │ • Hunt       │      │
│  │              │    │              │    │   records    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │                │
│         └───────────────────┴───────────────────┘                │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────┐                              │
│                    │   Dashboard  │                              │
│                    │   & API      │                              │
│                    └──────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 14. Monitoring & Observability

| Signal | Method | Threshold |
|--------|--------|-----------|
| Total IOCs | `ioc_mgr.stats()["total"]` | Alert if > 10,000 |
| Active IOCs | `ioc_mgr.stats()["active"]` | Alert if > 5,000 |
| High-threat IOCs | `len(ioc_mgr.get_high_threat())` | Alert if > 500 |
| Log anomaly rate | `flagged / total` | Alert if > 5% |
| Network flow anomalies | `len(net.detect_anomalies())` | Alert if > 100/hour |
| Open alerts | `alert_mgr.stats()["open"]` | Alert if > 50 |
| Critical alerts | `len(alert_mgr.get_critical_alerts())` | Alert if > 5 |
| Active hunts | `orch.get_active_hunts()` | Alert if > 10 |
| Detection rule matches | `detection.rules_stats()["total_matches"]` | Track trend |
| Threat actors active | `len(ti.get_active_actors())` | Track trend |

---

## 15. Data Models

### Core Entity Relationships

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│     IOC      │◀───▶│  ThreatHunt │◀───▶│  HuntReport │
│              │     │              │     │              │
│ • ioc_id     │     │ • hunt_id    │     │ • report_id  │
│ • value      │     │ • hypothesis │     │ • findings   │
│ • type       │     │ • phase      │     │ • iocs       │
│ • threat_lvl │     │ • status     │     │ • mitre_map  │
│ • confidence │     │ • findings   │     │ • recommendations│
│ • source     │     │ • mitre_tactic│    │              │
└──────┬──────┘     └──────────────┘     └──────────────┘
       │
       │              ┌─────────────┐
       └─────────────▶│    Alert    │
                      │              │
                      │ • alert_id   │
                      │ • severity   │
                      │ • status     │
                      │ • iocs       │
                      │ • mitre_tech │
                      └──────┬──────┘
                             │
                             ▼
                      ┌─────────────┐
                      │ThreatActor  │
                      │              │
                      │ • actor_id   │
                      │ • name       │
                      │ • techniques │
                      │ • iocs       │
                      │ • tools      │
                      └──────────────┘

┌─────────────┐     ┌─────────────┐
│  LogEntry   │     │ NetworkFlow │
│              │     │              │
│ • timestamp  │     │ • flow_id    │
│ • source     │     │ • src/dst    │
│ • src/dst IP │     │ • bytes      │
│ • port/proto │     │ • direction  │
│ • bytes      │     │ • ja3_hash   │
│ • anomalies  │     │ • anomalies  │
└──────────────┘     └──────────────┘

┌─────────────┐
│  SigmaRule  │
│              │
│ • rule_id    │
│ • title      │
│ • logsource  │
│ • detection  │
│ • severity   │
│ • matches    │
│ • status     │
└──────────────┘
```

---

## 16. Disaster Recovery

| Scenario | Recovery Strategy |
|----------|-------------------|
| IOC data loss | Re-import from STIX exports; external feed re-sync |
| Alert history loss | Reconstruct from hunt reports and log archives |
| Hunt report loss | Regenerate from hunt state and findings |
| Detection rule loss | Re-import from Sigma rule repository |
| Full system loss | Rebuild from external feeds, SIEM data, and rule repository |

---

## 17. Extension Points

1. **Custom IOC Types**: Extend IOCType enum for organization-specific indicators
2. **Custom Anomaly Rules**: Add detection logic to LogAnalyzer and NetworkAnalyzer
3. **External Feed Integration**: Plugin architecture for threat intel feeds (MISP, OTX, VirusTotal)
4. **Custom Sigma Rules**: User-defined detection rules with custom logic
5. **SIEM Integration**: Syslog, API, or webhook output for SIEM platforms
6. **Ticketing Integration**: Auto-create tickets in Jira/ServiceNow for critical alerts
7. **Dashboard Plugins**: Custom visualization components for hunt metrics
8. **ML-Based Detection**: Integrate machine learning models for anomaly detection

---

## 18. Glossary

| Term | Definition |
|------|-----------|
| IOC | Indicator of Compromise — artifact indicating a security breach |
| STIX | Structured Threat Information Expression — standard for threat intel |
| Sigma | Generic signature format for SIEM detection rules |
| JA3 | TLS client fingerprinting method |
| APT | Advanced Persistent Threat — sophisticated, prolonged attack |
| MITRE ATT&CK | Knowledge base of adversary tactics and techniques |
| SIEM | Security Information and Event Management |
| SOC | Security Operations Center |
| TTP | Tactics, Techniques, and Procedures |
| Dwell Time | Duration an attacker remains undetected in a network |
| Mean Time to Detect | Average time to identify a security incident |
| Mean Time to Respond | Average time to contain a security incident |

---

## 19. Appendix: Design Decisions

| Decision | Rationale |
|----------|-----------|
| Sequential IOC IDs | Human-readable, sortable; sufficient for single-instance deployment |
| In-memory storage | Simplicity; persistence layer optional for production |
| Boolean anomaly flags | Simple, fast evaluation; extensible via AnomalyType enum |
| STIX 2.1 export | Industry standard for threat intel sharing |
| Sigma-compatible rules | Interoperable with multiple SIEM platforms |
| MITRE ATT&CK mapping | Standard framework for adversary behavior classification |
| Severity as IntEnum | Enables numeric comparison and sorting |
| Phase-based hunt lifecycle | Enforces structured approach to threat hunting |
| False positive tracking | Essential for reducing alert fatigue over time |
| Configurable thresholds | Allows tuning for different environments and risk tolerances |
