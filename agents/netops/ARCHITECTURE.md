# NetOps Agent Architecture

## Overview

The NetOps Agent provides comprehensive network operations management covering device monitoring, configuration management, security analysis, traffic optimization, diagnostics, and capacity planning. The architecture follows a modular design where each subsystem operates independently with clean interfaces, coordinated through the top-level facade.

The system is designed for network engineers, infrastructure teams, and DevOps professionals who need full visibility and control over network infrastructure. It supports multiple device types (routers, switches, firewalls, load balancers, access points, servers) and provides unified management across all of them.

---

## System Context

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Network Infrastructure                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Routers  │  │ Switches │  │ Firewalls│  │   Load   │  │  Access  ││
│  │ (Cisco,  │  │ (Juniper,│  │ (Palo    │  │ Balancers│  │  Points  ││
│  │  Arista) │  │  Cisco)  │  │  Alto)   │  │ (F5, HA) │  │ (Meraki) ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘│
│       │             │             │             │             │        │
│  ┌────▼─────────────▼─────────────▼─────────────▼─────────────▼────┐  │
│  │                    SNMP / API Collection                          │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │  │
│  │  │   SNMP     │ │  NETCONF   │ │   REST     │ │   gNMI     │  │  │
│  │  │   Polling  │ │   Config   │ │   APIs     │ │   Streaming│  │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘  │  │
│  └─────────────────────────┬──────────────────────────────────────┘  │
│                            │                                           │
│  ┌─────────────────────────▼──────────────────────────────────────┐  │
│  │                   NetOps Agent Core                             │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │  │
│  │  │   Network    │  │    Config    │  │   Security   │         │  │
│  │  │   Monitor    │  │   Manager    │  │   Manager    │         │  │
│  │  │              │  │              │  │              │         │  │
│  │  │  Devices     │  │  Lifecycle   │  │  Firewall    │         │  │
│  │  │  Interfaces  │  │  Validation  │  │  Rules       │         │  │
│  │  │  Health      │  │  Rollback    │  │  Threats     │         │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │  │
│  │  │   Traffic    │  │  Diagnostic  │  │   Capacity   │         │  │
│  │  │   Manager    │  │   Runner     │  │   Planner    │         │  │
│  │  │              │  │              │  │              │         │  │
│  │  │  Routes      │  │  Ping        │  │  Forecast    │         │  │
│  │  │  QoS         │  │  Traceroute  │  │  Bottleneck  │         │  │
│  │  │  Bandwidth   │  │  DNS/Port    │  │  Upgrade     │         │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                            │                                           │
│  ┌─────────────────────────▼──────────────────────────────────────┐  │
│  │                        Data Layer                                │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐               │  │
│  │  │   Device   │  │   Config   │  │  Security  │               │  │
│  │  │  Registry  │  │   History  │  │   Events   │               │  │
│  │  │            │  │            │  │            │               │  │
│  │  │  metadata  │  │  versions  │  │  logs      │               │  │
│  │  │  status    │  │  backups   │  │  alerts    │               │  │
│  │  └────────────┘  └────────────┘  └────────────┘               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐               │  │
│  │  │  Traffic   │  │Diagnostic  │  │  Capacity  │               │  │
│  │  │   Data     │  │  Results   │  │  History   │               │  │
│  │  └────────────┘  └────────────┘  └────────────┘               │  │
│  └────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Network Monitor

**Purpose**: Track device status, interfaces, and health across the infrastructure.

```
┌───────────────────────────────────────────────────────────────────────┐
│                        Network Monitor                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ add_device(name, type, ip, vendor, model) → NetworkDevice       │  │
│  │ update_device_status(device_id, status) → NetworkDevice         │  │
│  │ add_interface(device_id, name, ip, speed_mbps) → Interface      │  │
│  │ record_interface_stats(device_id, iface, in_octets, out_octets) │  │
│  │ get_network_health() → HealthSummary                            │  │
│  │ list_devices(type, status) → List[NetworkDevice]                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Device Types:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ ROUTER       │ Layer 3 routing, WAN connectivity               │  │
│  │ SWITCH       │ Layer 2 switching, LAN distribution             │  │
│  │ FIREWALL     │ Security policy enforcement                     │  │
│  │ LOAD_BALANCER│ Traffic distribution                            │  │
│  │ ACCESS_POINT │ Wireless connectivity                           │  │
│  │ SERVER       │ Compute and application hosting                 │  │
│  │ OPTICAL      │ Fiber optic transport                           │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Device Status:                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ ONLINE      │ Device reachable, all services operational       │  │
│  │ OFFLINE     │ Device unreachable                               │  │
│  │ DEGRADED    │ Device reachable but some services degraded      │  │
│  │ MAINTENANCE │ Device in planned maintenance window             │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Health Calculation:                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ health_percent = online_devices / total_devices * 100          │  │
│  │                                                                 │  │
│  │ Example:                                                        │  │
│  │ 9 online + 1 offline = 90% health                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Internal State:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ _devices: Dict[str, NetworkDevice]                              │  │
│  │ _interfaces: Dict[str, Dict[str, Interface]]                    │  │
│  │   (device_id → interface_name → Interface)                      │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
```
Add Device:
  Input → Validate IP → Create Device Object → Store → Return

Update Status:
  Device ID → Load Device → Update Status → Store → Return

Add Interface:
  Device ID → Validate Exists → Create Interface → Store → Return

Get Health:
  Load All Devices → Count Online → Calculate % → Return
```

---

### 2. Configuration Manager

**Purpose**: Manage device configurations with validation and rollback.

```
┌───────────────────────────────────────────────────────────────────────┐
│                     Configuration Manager                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Config Lifecycle:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  DRAFT ──→ VALIDATED ──→ APPROVED ──→ APPLIED                  │  │
│  │                                        │                        │  │
│  │                                        ▼                        │  │
│  │                                    ROLLED_BACK                  │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Operations:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ create_config → validate → approve → apply                      │  │
│  │ backup_config → compare_configs → rollback                      │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Backup Strategy:                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ apply_config → save to backup store                             │  │
│  │ backup contains: change_id, changes, timestamp                  │  │
│  │ retention: 90 days                                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ create_config(device_id, changes, created_by) → ConfigChange    │  │
│  │ validate_config(change_id) → ConfigChange                       │  │
│  │ approve_config(change_id) → ConfigChange                        │  │
│  │ apply_config(change_id) → ConfigChange                          │  │
│  │ rollback_config(change_id) → ConfigChange                       │  │
│  │ backup_config(device_id) → Backup                               │  │
│  │ compare_configs(device_id, config_a, config_b) → Diff           │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Config Validation Rules**:
```
1. All changes must have setting, old_value, new_value
2. Device must exist
3. No duplicate settings in single change
4. Backup must exist before apply
5. Validation must pass before approval
6. Approval required before apply
```

---

### 3. Security Manager

**Purpose**: Manage firewall rules and analyze security events.

```
┌───────────────────────────────────────────────────────────────────────┐
│                       Security Manager                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Firewall Rules:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ action + protocol + source_ip + destination_ip + port           │  │
│  │                                                                 │  │
│  │ Actions: permit | deny                                          │  │
│  │ Protocols: TCP | UDP | ICMP | ANY                               │  │
│  │                                                                 │  │
│  │ Rule Evaluation:                                                │  │
│  │ First matching rule wins                                        │  │
│  │ Default: deny all                                               │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Threat Types:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ PORT_SCAN     │ Sequential port probing                        │  │
│  │ BRUTE_FORCE   │ Multiple failed auth attempts                  │  │
│  │ MALWARE       │ Known malware signatures                      │  │
│  │ DDOS          │ Distributed denial of service                  │  │
│  │ INTRUSION     │ Unauthorized access attempt                    │  │
│  │ DATA_EXFIL    │ Unusual data egress                            │  │
│  │ PHISHING      │ Social engineering attempts                    │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Threat Scoring:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ events_by_type, events_by_severity, blocked_count               │  │
│  │                                                                 │  │
│  │ Severity: CRITICAL > HIGH > MEDIUM > LOW > INFO                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ add_firewall_rule(name, action, protocol, src, dst, port)       │  │
│  │ enable_rule(rule_id) → FirewallRule                             │  │
│  │ disable_rule(rule_id) → FirewallRule                            │  │
│  │ log_security_event(threat, src, dst, severity, msg, blocked)    │  │
│  │ get_threat_summary(hours) → ThreatSummary                       │  │
│  │ analyze_firewall() → FirewallAnalysis                           │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

---

### 4. Traffic Manager

**Purpose**: Manage routing and QoS policies.

```
┌───────────────────────────────────────────────────────────────────────┐
│                       Traffic Manager                                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Routes:                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ destination + gateway + interface + metric                       │  │
│  │                                                                 │  │
│  │ Lower metric = higher priority                                  │  │
│  │ Example:                                                        │  │
│  │ 10.0.0.0/8 → 10.0.0.1 → eth0 (metric 100)                    │  │
│  │ 10.0.0.0/8 → 10.0.0.2 → eth1 (metric 200) [backup]           │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  QoS Classes:                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ VOICE        → Highest priority (VoIP, real-time)              │  │
│  │ VIDEO        → High priority (conferencing, streaming)         │  │
│  │ CRITICAL     → Medium-High (database, ERP)                     │  │
│  │ BUSINESS     → Medium (email, web apps)                        │  │
│  │ BEST_EFFORT  → Low (general internet)                          │  │
│  │ SCAVENGER    → Lowest (updates, backups)                       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Bandwidth Tracking:                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ interface → utilization history                                 │  │
│  │ trend analysis with avg/max/min                                 │  │
│  │                                                                 │  │
│  │ Example:                                                        │  │
│  │ eth0: avg=65%, max=82%, min=45%                                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ add_route(destination, gateway, interface, metric)               │  │
│  │ optimize_routes() → List[RouteOptimization]                     │  │
│  │ create_qos_policy(name, total_bandwidth, classes) → QoSPolicy   │  │
│  │ apply_qos_policy(policy_id) → QoSPolicy                         │  │
│  │ record_bandwidth(interface, utilization_percent)                 │  │
│  │ get_bandwidth_trend(interface, hours) → BandwidthTrend          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

---

### 5. Diagnostic Runner

**Purpose**: Run network connectivity and performance tests.

```
┌───────────────────────────────────────────────────────────────────────┐
│                       Diagnostic Runner                                │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Available Tests:                                                     │
│  ┌────────────────┬──────────────────────────────────────────────┐   │
│  │ PING           │ ICMP reachability + latency measurement      │   │
│  │ TRACEROUTE     │ Hop-by-hop path analysis                     │   │
│  │ BANDWIDTH      │ Download/upload speed test                   │   │
│  │ DNS            │ Name resolution + TTL lookup                 │   │
│  │ PORT           │ TCP port open/closed check                   │   │
│  └────────────────┴──────────────────────────────────────────────┘   │
│                                                                       │
│  Full Diagnostics:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ All tests against a single target                               │  │
│  │ Returns comprehensive connectivity report                       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ ping(target, count) → PingResult                                │  │
│  │ traceroute(target, max_hops) → TracerouteResult                 │  │
│  │ bandwidth_test(target) → BandwidthResult                        │  │
│  │ dns_lookup(hostname) → DNSResult                                │  │
│  │ port_check(target, port) → PortResult                           │  │
│  │ run_full_diagnostics(target) → DiagnosticReport                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

---

### 6. Capacity Planner

**Purpose**: Forecast resource utilization and identify bottlenecks.

```
┌───────────────────────────────────────────────────────────────────────┐
│                       Capacity Planner                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Metrics Tracked:                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ cpu_utilization    │ CPU usage percentage                       │  │
│  │ memory_utilization │ RAM usage percentage                       │  │
│  │ bandwidth          │ Network utilization percentage             │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Forecasting:                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Linear regression on historical data                            │  │
│  │ projections: 30d, 90d, 180d                                     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Bottleneck Detection:                                                │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ projected_90d > 80% → bottleneck = True                        │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Recommendations:                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ > 90% → Critical upgrade (immediate action)                    │  │
│  │ > 80% → Warning, plan upgrade (within 3 months)                │  │
│  │ < 80% → No action needed (monitor monthly)                     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ record_metrics(device_id, cpu, memory, bandwidth)               │  │
│  │ forecast(device_id, resource) → CapacityForecast                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Forecasting Algorithm**:
```python
def forecast(device_id, resource):
    history = get_metrics_history(device_id, resource)
    if len(history) < 3:
        return CapacityForecast(error="Insufficient data")

    # Linear regression
    x = list(range(len(history)))
    y = [m.value for m in history]

    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)

    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(len(x)))

    slope = numerator / denominator if denominator != 0 else 0
    intercept = y_mean - slope * x_mean

    # Project 90 days forward
    projected_90d = slope * (len(x) + 90) + intercept
    bottleneck = projected_90d > 80

    # Generate recommendation
    if projected_90d > 90:
        recommendation = "Critical: Upgrade needed within 1 month"
    elif projected_90d > 80:
        recommendation = "Warning: Plan upgrade within 3 months"
    else:
        recommendation = "No action needed"

    return CapacityForecast(
        resource=resource,
        current_utilization=history[-1].value,
        projected_90d=projected_90d,
        bottleneck=bottleneck,
        recommendation=recommendation
    )
```

---

## Data Flow: Network Audit

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Discover   │───→│   Monitor    │───→│   Analyze    │───→│   Report     │
│   Devices    │    │   Health     │    │   Security   │    │   Findings   │
│              │    │              │    │              │    │              │
│ - add devices│    │ - status     │    │ - threats    │    │ - health %   │
│ - interfaces │    │ - health     │    │ - firewall   │    │ - threats    │
│ - vendor     │    │ - uptime     │    │ - events     │    │ - capacity   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

**Complete Network Audit Workflow**:
```python
agent = NetOpsAgent()

# 1. Discover devices
router = agent.monitor.add_device("CoreRouter", DeviceType.ROUTER, "10.0.0.1", vendor="Cisco")
switch = agent.monitor.add_device("DistSwitch", DeviceType.SWITCH, "10.0.1.1", vendor="Juniper")
firewall = agent.monitor.add_device("FW01", DeviceType.FIREWALL, "10.0.0.254", vendor="Palo Alto")

# 2. Update status
agent.monitor.update_device_status(router.device_id, DeviceStatus.ONLINE)
agent.monitor.update_device_status(switch.device_id, DeviceStatus.ONLINE)
agent.monitor.update_device_status(firewall.device_id, DeviceStatus.ONLINE)

# 3. Add interfaces
agent.monitor.add_interface(router.device_id, "GigE0/0", "10.0.0.1", speed_mbps=10000)
agent.monitor.add_interface(switch.device_id, "GigE0/1", "10.0.1.1", speed_mbps=1000)

# 4. Configure security
agent.security.add_firewall_rule("Allow HTTP", "permit", Protocol.TCP, port="80")
agent.security.add_firewall_rule("Allow HTTPS", "permit", Protocol.TCP, port="443")
agent.security.add_firewall_rule("Block Telnet", "deny", Protocol.TCP, port="23")

# 5. Set up traffic
agent.traffic.add_route("10.0.0.0/8", "10.0.0.1", "eth0", metric=100)

# 6. Run diagnostics
results = agent.diagnostics.run_full_diagnostics("10.0.0.1")

# 7. Plan capacity
agent.capacity.record_metrics(router.device_id, cpu=65, memory=70, bandwidth=75)
forecast = agent.capacity.forecast(router.device_id, "bandwidth")

# 8. Get health summary
health = agent.monitor.get_network_health()
print(f"Network Health: {health['health_percent']}%")
```

---

## Design Patterns

| Pattern | Where | Purpose |
|---------|-------|---------|
| Repository | Device/Config stores | Data access abstraction |
| State Machine | Config lifecycle | Validated transitions |
| Strategy | QoS classes | Pluggable traffic policies |
| Facade | NetOpsAgent | Unified interface to subsystems |
| Observer | Security events | Event-driven alerting |
| Factory Method | Device creation | Platform-specific handlers |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Data Classes | dataclasses, typing | Structured data models |
| Enums | enum.Enum | Type-safe constants |
| Math | math (regression) | Forecasting calculations |
| Logging | logging | Audit trail |
| ID Generation | uuid4 | Unique identifiers |
| Date/Time | datetime, timedelta | Time-based operations |

---

## Scalability

| Dimension | Approach | Threshold |
|-----------|---------|-----------|
| Device Volume | Hash-based device lookup | 10K devices |
| Config History | Append-only with retention | 100K changes |
| Security Events | Time-windowed queries | 1M events/day |
| Bandwidth Data | Rolling window storage | 100K data points |
| Forecasting | On-demand computation | 1K forecasts/day |
| Interfaces | Per-device indexed lookup | 100K interfaces |

**Performance Optimizations**:
1. **Hash Indexing**: O(1) device lookup by ID
2. **Lazy SWOT**: Security analysis computed on-demand
3. **Batch Diagnostics**: Tests run in parallel
4. **Incremental Bandwidth**: Stats updated incrementally
5. **Forecast Caching**: Results cached by device + resource

---

## Security

| Concern | Approach | Implementation |
|---------|----------|----------------|
| Config Access | Role-based approval workflow | RBAC |
| Firewall Rules | Audit trail for all changes | Immutable logs |
| Security Events | Encrypted storage | AES-256 |
| Device Credentials | Environment variables | No hardcoded keys |
| API Access | Authentication required | API keys, OAuth |
| Config Backup | Encrypted at rest | AES-256 |
| Diagnostic Results | Access-controlled | Permission checks |

---

## Error Handling

```
NetOpsError (base)
├── DeviceNotFoundError
│   └── Raised when device_id not found
├── ConfigError
│   ├── InvalidConfigError
│   │   └── Raised when config validation fails
│   ├── ConfigNotApprovedError
│   │   └── Raised when config not approved before apply
│   └── RollbackError
│       └── Raised when rollback fails
├── DiagnosticError
│   ├── HostUnreachableError
│   │   └── Raised when target unreachable
│   └── PortClosedError
│       └── Raised when port closed (expected for some tests)
├── SecurityError
│   └── RuleConflictError
│       └── Raised when firewall rules conflict
└── CapacityError
    └── InsufficientDataError
        └── Raised when < 3 data points for forecasting
```

**Error Handling Strategy**:
- All public methods validate inputs before execution
- Config operations require validated → approved → applied sequence
- Diagnostic tests return success/failure status (don't raise)
- Security events are logged regardless of processing outcome
- Capacity forecasts gracefully handle insufficient data

---

## Testing Strategy

| Component | Approach | Coverage Target |
|-----------|---------|-----------------|
| Network Monitor | Device CRUD, health calc | 95% |
| Configuration Manager | Lifecycle transitions, rollback | 100% transitions |
| Security Manager | Rule management, threat logging | 90% |
| Traffic Manager | Route and QoS operations | 90% |
| Diagnostic Runner | Test execution, result accuracy | 95% |
| Capacity Planner | Forecast accuracy, bottleneck detection | 90% |

**Test Categories**:
1. **Unit Tests**: Individual method correctness
2. **Integration Tests**: Component interaction verification
3. **State Tests**: Config lifecycle transition validation
4. **Network Tests**: Simulated device responses
5. **Performance Tests**: Large-scale device management
