# Network Operations (NetOps) Agent

Network monitoring, configuration management, troubleshooting, security analysis, and capacity planning.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The NetOps Agent provides complete network infrastructure management covering device monitoring, configuration management with rollback, security analysis, traffic optimization, diagnostics, and capacity planning with forecasting.

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| Network Monitor | Device status, interfaces, health |
| Configuration Manager | Validate, approve, apply, rollback |
| Security Manager | Firewall rules, threat analysis |
| Traffic Manager | Routing, QoS, bandwidth tracking |
| Diagnostic Runner | Ping, traceroute, DNS, port checks |
| Capacity Planner | Forecasting, bottleneck detection |

---

## Features

### Device Monitoring
- Support for 7 device types (router, switch, firewall, LB, AP, server, optical)
- Interface tracking with speed and utilization
- Health percentage calculation
- Device status lifecycle (online, offline, degraded, maintenance)

### Configuration Management
- 5-state lifecycle: draft → validated → approved → applied → rolled_back
- Automatic backup on apply
- Config comparison with diff output
- Rollback capability

### Security Analysis
- Firewall rule management (permit/deny)
- Security event logging with threat classification
- 7 threat types (port scan, brute force, malware, DDoS, intrusion, data exfil, phishing)
- Threat summary by type and severity

### Traffic Management
- Static route management
- QoS policy creation and application
- Bandwidth utilization tracking
- Trend analysis with avg/max/min

### Diagnostics
- 5 test types: ping, traceroute, bandwidth, DNS lookup, port check
- Full diagnostics suite (all tests against one target)
- Latency and packet loss measurement
- Results history

### Capacity Planning
- CPU, memory, bandwidth metric tracking
- Linear regression forecasting (30d, 90d, 180d)
- Bottleneck detection (>80% projected)
- Actionable recommendations

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│             NetOpsAgent (Facade)                 │
├─────────────────────────────────────────────────┤
│  NetworkMonitor    │  ConfigurationManager      │
│  SecurityManager   │  TrafficManager            │
│  DiagnosticRunner  │  CapacityPlanner           │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
pip install awesome-grok-skills
```

### Minimal Example

```python
from agents.netops.agent import NetOpsAgent, DeviceType, DeviceStatus

agent = NetOpsAgent()

# Add device
device = agent.monitor.add_device("Router1", DeviceType.ROUTER, "10.0.0.1")
agent.monitor.update_device_status(device.device_id, DeviceStatus.ONLINE)

# Check health
health = agent.monitor.get_network_health()
print(f"Health: {health['health_percent']}%")
```

---

## Usage

### Running the Agent

```bash
python agents/netops/agent.py
```

### Programmatic Access

```python
from agents.netops.agent import NetOpsAgent

agent = NetOpsAgent()

# Each component works independently
agent.monitor.add_device("Switch1", DeviceType.SWITCH, "10.0.1.1")
agent.security.add_firewall_rule("Allow SSH", "permit", Protocol.TCP, port="22")
agent.traffic.add_route("10.0.0.0/8", "10.0.0.1", "eth0")
agent.diagnostics.ping("10.0.0.1")
agent.capacity.record_metrics("dev_1", cpu=50, memory=60, bandwidth=70)
```

---

## API Reference

### NetOpsAgent

| Method | Description |
|--------|-------------|
| `full_network_audit(devices)` | Complete network audit |

### NetworkMonitor

| Method | Description |
|--------|-------------|
| `add_device(name, type, ip, vendor, model)` | Add device |
| `update_device_status(device_id, status)` | Update status |
| `add_interface(device_id, name, ip, speed)` | Add interface |
| `record_interface_stats(device_id, iface, in, out)` | Record stats |
| `get_network_health()` | Get health summary |
| `list_devices(type, status)` | List devices |

### ConfigurationManager

| Method | Description |
|--------|-------------|
| `create_config(device_id, changes, by)` | Create config |
| `validate_config(change_id)` | Validate |
| `approve_config(change_id)` | Approve |
| `apply_config(change_id)` | Apply |
| `rollback_config(change_id)` | Rollback |
| `backup_config(device_id)` | Backup |
| `compare_configs(device_id, a, b)` | Compare |

### SecurityManager

| Method | Description |
|--------|-------------|
| `add_firewall_rule(name, action, proto, src, dst, port)` | Add rule |
| `enable_rule(rule_id)` | Enable rule |
| `disable_rule(rule_id)` | Disable rule |
| `log_security_event(threat, src, dst, severity, msg)` | Log event |
| `get_threat_summary(hours)` | Get summary |
| `analyze_firewall()` | Analyze rules |

### TrafficManager

| Method | Description |
|--------|-------------|
| `add_route(dest, gateway, iface, metric)` | Add route |
| `optimize_routes()` | Get optimizations |
| `create_qos_policy(name, bandwidth, classes)` | Create QoS |
| `apply_qos_policy(policy_id)` | Apply QoS |
| `record_bandwidth(iface, utilization)` | Record bandwidth |
| `get_bandwidth_trend(iface, hours)` | Get trend |

### DiagnosticRunner

| Method | Description |
|--------|-------------|
| `ping(target, count)` | Ping test |
| `traceroute(target, max_hops)` | Traceroute |
| `bandwidth_test(target)` | Bandwidth test |
| `dns_lookup(hostname)` | DNS lookup |
| `port_check(target, port)` | Port check |
| `run_full_diagnostics(target)` | All tests |

### CapacityPlanner

| Method | Description |
|--------|-------------|
| `record_metrics(device_id, cpu, mem, bw)` | Record metrics |
| `forecast(device_id, resource)` | Generate forecast |

---

## Examples

### Full Network Audit

```python
agent = NetOpsAgent()

result = agent.full_network_audit([
    {"name": "CoreRouter", "type": "router", "ip": "10.0.0.1", "vendor": "Cisco"},
    {"name": "DistSwitch", "type": "switch", "ip": "10.0.1.1", "vendor": "Juniper"},
    {"name": "Firewall", "type": "firewall", "ip": "10.0.0.254", "vendor": "Palo Alto"},
])
print(f"Health: {result['health']['health_percent']}%")
```

### Configuration Workflow

```python
agent = NetOpsAgent()

device = agent.monitor.add_device("Switch1", DeviceType.SWITCH, "10.0.1.1")
config = agent.config.create_config(device.device_id, [
    {"setting": "vlan", "old": "10", "new": "20"},
    {"setting": "mtu", "old": "1500", "new": "9000"},
], created_by="netadmin")

agent.config.validate_config(config.change_id)
agent.config.approve_config(config.change_id)
agent.config.apply_config(config.change_id)
print(f"Config applied: {config.change_id}")
```

### Security Monitoring

```python
agent = NetOpsAgent()

agent.security.add_firewall_rule("Allow HTTP", "permit", Protocol.TCP, port="80")
agent.security.add_firewall_rule("Allow HTTPS", "permit", Protocol.TCP, port="443")
agent.security.add_firewall_rule("Block Telnet", "deny", Protocol.TCP, port="23")

agent.security.log_security_event(SecurityThreat.BRUTE_FORCE, "192.168.1.50", "10.0.0.1", AlertSeverity.HIGH, "50 failed SSH attempts")
agent.security.log_security_event(SecurityThreat.PORT_SCAN, "10.10.10.10", "10.0.0.0/8", AlertSeverity.MEDIUM, "SYN scan detected")

summary = agent.security.get_threat_summary(hours=24)
print(f"Threats: {summary['total_events']}, Blocked: {summary['blocked']}")
```

### Capacity Forecasting

```python
agent = NetOpsAgent()

# Simulate growing utilization
for cpu, mem, bw in [(50, 55, 60), (55, 58, 65), (60, 62, 70), (65, 66, 75), (70, 70, 80)]:
    agent.capacity.record_metrics("router_1", cpu=cpu, memory=mem, bandwidth=bw)

forecast = agent.capacity.forecast("router_1", "bandwidth")
print(f"Current: {forecast.current_utilization}%")
print(f"90-day: {forecast.projected_90d}%")
print(f"Bottleneck: {forecast.bottleneck}")
print(f"Action: {forecast.recommendation}")
```

---

## Configuration

### Device Types

| Type | Typical Use |
|------|------------|
| ROUTER | Layer 3 routing, WAN connectivity |
| SWITCH | Layer 2 switching, LAN distribution |
| FIREWALL | Security policy enforcement |
| LOAD_BALANCER | Traffic distribution |
| ACCESS_POINT | Wireless connectivity |
| SERVER | Compute and application hosting |

### Threat Severity

| Level | Response |
|-------|----------|
| CRITICAL | Immediate investigation |
| HIGH | Investigate within 1 hour |
| MEDIUM | Investigate within 4 hours |
| LOW | Investigate within 24 hours |
| INFO | Log and monitor |

### QoS Priority Classes

| Class | Priority | Typical Traffic |
|-------|----------|----------------|
| VOICE | Highest | VoIP, real-time audio |
| VIDEO | High | Video conferencing, streaming |
| CRITICAL | Medium-High | Database, ERP |
| BUSINESS | Medium | Email, web apps |
| BEST_EFFORT | Low | General internet |
| SCAVENGER | Lowest | Updates, backups |

---

## Best Practices

### Monitoring
- Monitor all critical infrastructure devices
- Set appropriate polling intervals
- Configure meaningful alert thresholds
- Maintain device inventory accuracy

### Configuration
- Always validate before applying
- Take backups before changes
- Use maintenance windows for production
- Document all changes with tickets

### Security
- Review firewall rules quarterly
- Remove unused rules
- Enable logging on all deny rules
- Monitor for brute force and scans
- Implement least-privilege access

### Traffic
- Classify traffic by business importance
- Reserve bandwidth for critical applications
- Monitor for anomalies and spikes
- Review routing tables regularly

### Diagnostics
- Run baseline diagnostics during normal operations
- Compare against baseline during issues
- Document diagnostic results
- Use full diagnostics for comprehensive checks

### Capacity
- Collect metrics regularly (daily minimum)
- Review forecasts monthly
- Plan upgrades before bottleneck
- Maintain 20% headroom on critical links

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Device shows offline | Network/power issue | Check physical, ping management IP |
| High latency | Congestion | Check QoS, review bandwidth |
| Config apply fails | Validation error | Review diff, fix syntax |
| Security event flood | Misconfigured rule | Review rule, adjust threshold |
| Bandwidth spike | DDoS or legitimate surge | Check traffic classes, trace source |
| Forecast bottleneck | Growth exceeding plan | Initiate upgrade process |
| DNS slow | Server overload | Check DNS server health, add redundancy |
| Route flapping | Link instability | Check physical, adjust metrics |

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.
