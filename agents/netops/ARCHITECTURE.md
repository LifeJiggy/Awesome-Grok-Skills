# NetOps Agent Architecture

## Overview

The NetOps Agent provides comprehensive network operations management covering device monitoring, configuration management, security analysis, traffic optimization, diagnostics, and capacity planning. The architecture follows a modular design where each subsystem operates independently with clean interfaces, coordinated through the top-level facade.

---

## System Context

```
┌──────────────────────────────────────────────────────────────────┐
│                       Network Infrastructure                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Routers  │ │ Switches │ │Firewalls │ │  Servers │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       │            │            │            │                    │
│  ┌────▼────────────▼────────────▼────────────▼─────┐            │
│  │              SNMP / API Collection               │            │
│  └──────────────────┬──────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │             NetOps Agent Core                    │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │ Network  │ │  Config  │ │ Security │        │            │
│  │  │ Monitor  │ │ Manager  │ │ Manager  │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │ Traffic  │ │Diagnostic│ │ Capacity │        │            │
│  │  │ Manager  │ │ Runner   │ │ Planner  │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  └─────────────────────────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │              Data Layer                          │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │ Device   │ │  Config  │ │ Security │        │            │
│  │  │ Registry │ │ History  │ │ Events   │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  └─────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Network Monitor

**Purpose**: Track device status, interfaces, and health.

```
┌─────────────────────────────────────────────┐
│           Network Monitor                   │
├─────────────────────────────────────────────┤
│  add_device(name, type, ip)                 │
│  update_device_status(device_id, status)    │
│  add_interface(device_id, name, ip, speed)  │
│  record_interface_stats(device_id, iface)   │
│  get_network_health()                       │
│  list_devices(type, status)                 │
├─────────────────────────────────────────────┤
│  Device Types:                              │
│  ROUTER | SWITCH | FIREWALL | LB | AP       │
│  SERVER | OPTICAL                           │
│                                             │
│  Status:                                    │
│  ONLINE | OFFLINE | DEGRADED | MAINTENANCE  │
└─────────────────────────────────────────────┘
```

**Health Calculation**:
```
health_percent = online_devices / total_devices * 100
```

---

### 2. Configuration Manager

**Purpose**: Manage device configurations with validation and rollback.

```
┌──────────────────────────────────────────────────────────┐
│              Configuration Manager                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Config Lifecycle:                                       │
│  DRAFT → VALIDATED → APPROVED → APPLIED                  │
│                                         ↓                │
│                                      ROLLED_BACK         │
│                                                          │
│  Operations:                                             │
│  create_config → validate → approve → apply              │
│  backup_config → compare_configs → rollback              │
└──────────────────────────────────────────────────────────┘
```

**Backup Strategy**:
```
apply_config → save to backup store
backup contains: change_id, changes, timestamp
retention: 90 days
```

---

### 3. Security Manager

**Purpose**: Manage firewall rules and analyze security events.

```
┌──────────────────────────────────────────────────────────┐
│               Security Manager                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Firewall Rules:                                         │
│  ┌──────────┐ action + protocol + src + dst + port       │
│  │ permit/  │                                            │
│  │ deny     │                                            │
│  └──────────┘                                            │
│                                                          │
│  Threat Types:                                           │
│  PORT_SCAN | BRUTE_FORCE | MALWARE | DDoS                │
│  INTRUSION | DATA_EXFIL | PHISHING                       │
│                                                          │
│  Summary: events by type, by severity, blocked count     │
└──────────────────────────────────────────────────────────┘
```

---

### 4. Traffic Manager

**Purpose**: Manage routing and QoS policies.

```
┌─────────────────────────────────────────────┐
│           Traffic Manager                   │
├─────────────────────────────────────────────┤
│  Routes:                                    │
│  destination + gateway + interface + metric │
│                                             │
│  QoS Classes:                               │
│  VOICE → VIDEO → CRITICAL → BUSINESS →      │
│  BEST_EFFORT → SCAVENGER                    │
│                                             │
│  Bandwidth Tracking:                        │
│  interface → utilization history            │
│  trend analysis with avg/max/min            │
└─────────────────────────────────────────────┘
```

---

### 5. Diagnostic Runner

**Purpose**: Run network connectivity and performance tests.

```
Available Tests:
┌──────────┬────────────────────────────────────┐
│ PING     │ ICMP reachability + latency         │
│ TRACEROUTE│ Hop-by-hop path analysis           │
│ BANDWIDTH│ Download/upload speed test          │
│ DNS      │ Name resolution + TTL               │
│ PORT     │ TCP port open/closed check          │
└──────────┴────────────────────────────────────┘

Full Diagnostics = all tests against single target
```

---

### 6. Capacity Planner

**Purpose**: Forecast resource utilization and identify bottlenecks.

```
┌──────────────────────────────────────────────────────────┐
│              Capacity Planner                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Metrics Tracked:                                        │
│  cpu_utilization | memory_utilization | bandwidth        │
│                                                          │
│  Forecasting: Linear regression on historical data       │
│  projections: 30d, 90d, 180d                             │
│                                                          │
│  Bottleneck Detection:                                   │
│  projected_90d > 80% → bottleneck = True                 │
│                                                          │
│  Recommendations:                                        │
│  > 90% → Critical upgrade                               │
│  > 80% → Warning, plan upgrade                           │
│  < 80% → No action needed                               │
└──────────────────────────────────────────────────────────┘
```

---

## Data Flow: Network Audit

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Discover │───→│ Monitor  │───→│ Analyze  │───→│ Report   │
│ Devices  │    │  Health  │    │ Security │    │ Findings │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Design Patterns

| Pattern | Where | Purpose |
|---------|-------|---------|
| Repository | Device/Config stores | Data access abstraction |
| State Machine | Config lifecycle | Validated transitions |
| Strategy | QoS classes | Pluggable traffic policies |
| Facade | NetOpsAgent | Unified interface |
| Observer | Security events | Event-driven alerting |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Data Classes | dataclasses, typing |
| Enums | enum.Enum |
| Math | math (regression) |
| Logging | logging |
| ID Generation | uuid |
| Date/Time | datetime, timedelta |

---

## Scalability

| Dimension | Approach |
|-----------|---------|
| Device Volume | Hash-based device lookup |
| Config History | Append-only with retention |
| Security Events | Time-windowed queries |
| Bandwidth Data | Rolling window storage |
| Forecasting | On-demand computation |

---

## Security

| Concern | Approach |
|---------|----------|
| Config Access | Role-based approval workflow |
| Firewall Rules | Audit trail for all changes |
| Security Events | Encrypted storage |
| Device Credentials | Environment variables |
| API Access | Authentication required |

---

## Error Handling

```
NetOpsError (base)
├── DeviceNotFoundError
├── ConfigError
└── DiagnosticError
```

Config operations require validated → approved → applied sequence. Diagnostic tests return success/failure status. Security events are logged regardless of processing outcome.
