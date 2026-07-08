# Network Operations (NetOps) Agent

Network monitoring, configuration management, troubleshooting, security analysis, and capacity planning.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
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

### System Requirements

- Python 3.10 or higher
- 256 MB RAM minimum
- 50 MB disk space
- Network access for device communication (optional)

---

## Features

### Device Monitoring
- Support for 7 device types (router, switch, firewall, LB, AP, server, optical)
- Interface tracking with speed and utilization
- Health percentage calculation
- Device status lifecycle (online, offline, degraded, maintenance)
- Vendor and model tracking
- SNMP collection support

### Configuration Management
- 5-state lifecycle: draft → validated → approved → applied → rolled_back
- Automatic backup on apply
- Config comparison with diff output
- Rollback capability
- Audit trail for all changes
- Maintenance window support

### Security Analysis
- Firewall rule management (permit/deny)
- Security event logging with threat classification
- 7 threat types (port scan, brute force, malware, DDoS, intrusion, data exfil, phishing)
- Threat summary by type and severity
- Rule analysis and recommendations
- Access control enforcement

### Traffic Management
- Static route management
- QoS policy creation and application
- Bandwidth utilization tracking
- Trend analysis with avg/max/min
- Route optimization suggestions
- Priority class configuration

### Diagnostics
- 5 test types: ping, traceroute, bandwidth, DNS lookup, port check
- Full diagnostics suite (all tests against one target)
- Latency and packet loss measurement
- Results history
- Parallel test execution

### Capacity Planning
- CPU, memory, bandwidth metric tracking
- Linear regression forecasting (30d, 90d, 180d)
- Bottleneck detection (>80% projected)
- Actionable recommendations
- Trend visualization

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│             NetOpsAgent (Facade)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │NetworkMonitor  │  │ConfigManager   │  │SecurityManager │    │
│  │                │  │                │  │                │    │
│  │ Devices        │  │ Lifecycle      │  │ Firewall       │    │
│  │ Interfaces     │  │ Validation     │  │ Rules          │    │
│  │ Health         │  │ Rollback       │  │ Threats        │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │TrafficManager  │  │DiagnosticRunner│  │CapacityPlanner │    │
│  │                │  │                │  │                │    │
│  │ Routes         │  │ Ping           │  │ Forecast       │    │
│  │ QoS            │  │ Traceroute     │  │ Bottleneck     │    │
│  │ Bandwidth      │  │ DNS/Port       │  │ Upgrade        │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
Network Request
     │
     ▼
NetOpsAgent (facade)
     │
     ├──→ NetworkMonitor.add_device()
     │         │
     │         ▼
     │    Device registered
     │
     ├──→ NetworkMonitor.update_device_status()
     │         │
     │         ▼
     │    Status updated
     │
     ├──→ ConfigurationManager.create_config()
     │         │
     │         ▼
     │    Config (DRAFT)
     │
     ├──→ ConfigurationManager.apply_config()
     │         │
     │         ▼
     │    Config (APPLIED)
     │
     ├──→ SecurityManager.add_firewall_rule()
     │         │
     │         ▼
     │    Rule active
     │
     ├──→ DiagnosticRunner.run_full_diagnostics()
     │         │
     │         ▼
     │    Results
     │
     └──→ CapacityPlanner.forecast()
               │
               ▼
          Forecast
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

### 60-Second Setup

```python
from agents.netops.agent import NetOpsAgent, DeviceType, DeviceStatus

agent = NetOpsAgent()

# Add devices
agent.monitor.add_device("Router", DeviceType.ROUTER, "10.0.0.1")
agent.monitor.add_device("Switch", DeviceType.SWITCH, "10.0.1.1")

# Check health
health = agent.monitor.get_network_health()
print(f"Network: {health['health_percent']}% healthy")
```

---

## Installation

### From PyPI

```bash
pip install awesome-grok-skills
```

### From Source

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Requirements

```
Python >= 3.10
No external dependencies (stdlib only)
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

### CLI Usage

```bash
# List all devices
python agents/netops/agent.py --list-devices

# Check network health
python agents/netops/agent.py --health

# Run diagnostics
python agents/netops/agent.py --diagnose 10.0.0.1
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
| `record_interface_stats(device_id, iface, in_octets, out_octets)` | Record stats |
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
| `log_security_event(threat, src, dst, severity, msg, blocked)` | Log event |
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
    {"setting": "vlan", "old_value": "10", "new_value": "20"},
    {"setting": "mtu", "old_value": "1500", "new_value": "9000"},
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

### Diagnostics Suite

```python
agent = NetOpsAgent()

# Individual tests
ping = agent.diagnostics.ping("10.0.0.1", count=5)
print(f"Ping: {ping['avg_latency_ms']}ms, Loss: {ping['packet_loss']}%")

dns = agent.diagnostics.dns_lookup("example.com")
print(f"DNS: {dns['ip_addresses']}")

port = agent.diagnostics.port_check("10.0.0.1", 443)
print(f"Port 443: {'Open' if port['open'] else 'Closed'}")

# Full diagnostics
results = agent.diagnostics.run_full_diagnostics("10.0.0.1")
print(f"Tests: {results['tests_passed']}/{results['tests_run']} passed")
```

### QoS Configuration

```python
agent = NetOpsAgent()

policy = agent.traffic.create_qos_policy(
    name="Production QoS",
    total_bandwidth_mbps=10000,
    classes=[
        {"name": "voice", "priority": "highest", "bandwidth_percent": 20},
        {"name": "video", "priority": "high", "bandwidth_percent": 30},
        {"name": "business", "priority": "medium", "bandwidth_percent": 30},
        {"name": "best_effort", "priority": "low", "bandwidth_percent": 15},
        {"name": "scavenger", "priority": "lowest", "bandwidth_percent": 5},
    ]
)
agent.traffic.apply_qos_policy(policy.policy_id)
print(f"QoS applied: {policy.name}")
```

---

## Configuration

### Device Types

| Type | Typical Use | Management Port |
|------|------------|-----------------|
| ROUTER | Layer 3 routing, WAN connectivity | 22 (SSH), 161 (SNMP) |
| SWITCH | Layer 2 switching, LAN distribution | 22 (SSH), 161 (SNMP) |
| FIREWALL | Security policy enforcement | 443 (HTTPS), 161 (SNMP) |
| LOAD_BALANCER | Traffic distribution | 443 (HTTPS), 161 (SNMP) |
| ACCESS_POINT | Wireless connectivity | 443 (HTTPS) |
| SERVER | Compute and application hosting | 22 (SSH), 3389 (RDP) |

### Threat Severity

| Level | Response Time | Example |
|-------|--------------|---------|
| CRITICAL | Immediate investigation | Active intrusion, DDoS |
| HIGH | Investigate within 1 hour | Brute force, port scan |
| MEDIUM | Investigate within 4 hours | Failed auth attempts |
| LOW | Investigate within 24 hours | Configuration change |
| INFO | Log and monitor | Routine event |

### QoS Priority Classes

| Class | Priority | Typical Traffic | Bandwidth % |
|-------|----------|----------------|-------------|
| VOICE | Highest | VoIP, real-time audio | 15-25% |
| VIDEO | High | Video conferencing, streaming | 20-30% |
| CRITICAL | Medium-High | Database, ERP | 15-25% |
| BUSINESS | Medium | Email, web apps | 15-25% |
| BEST_EFFORT | Low | General internet | 10-20% |
| SCAVENGER | Lowest | Updates, backups | 5-10% |

### Config Lifecycle States

| State | Description | Allowed Transitions |
|-------|-------------|---------------------|
| DRAFT | Created, not validated | VALIDATED, ARCHIVED |
| VALIDATED | Passed validation | APPROVED, DRAFT |
| APPROVED | Approved for apply | APPLIED, DRAFT |
| APPLIED | Applied to device | ROLLED_BACK |
| ROLLED_BACK | Reverted | (terminal) |

### Diagnostic Tests

| Test | Protocol | Port | Description |
|------|----------|------|-------------|
| PING | ICMP | - | Reachability + latency |
| TRACEROUTE | ICMP/TCP | - | Path analysis |
| BANDWIDTH | TCP | 80/443 | Speed test |
| DNS | UDP/TCP | 53 | Name resolution |
| PORT | TCP | Custom | Port status |

---

## Best Practices

### Monitoring
- Monitor all critical infrastructure devices
- Set appropriate polling intervals
- Configure meaningful alert thresholds
- Maintain device inventory accuracy
- Use SNMP v3 for security
- Monitor from multiple locations

### Configuration
- Always validate before applying
- Take backups before changes
- Use maintenance windows for production
- Document all changes with tickets
- Test changes in lab first
- Implement change approval workflow

### Security
- Review firewall rules quarterly
- Remove unused rules
- Enable logging on all deny rules
- Monitor for brute force and scans
- Implement least-privilege access
- Use jump hosts for admin access
- Enable SSH key-based authentication

### Traffic
- Classify traffic by business importance
- Reserve bandwidth for critical applications
- Monitor for anomalies and spikes
- Review routing tables regularly
- Implement route summarization
- Use BGP for multi-homed connections

### Diagnostics
- Run baseline diagnostics during normal operations
- Compare against baseline during issues
- Document diagnostic results
- Use full diagnostics for comprehensive checks
- Run from multiple source locations
- Save results for trend analysis

### Capacity
- Collect metrics regularly (daily minimum)
- Review forecasts monthly
- Plan upgrades before bottleneck
- Maintain 20% headroom on critical links
- Track growth trends quarterly
- Budget for capacity upgrades annually

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Device shows offline | Network/power issue | Check physical, ping management IP |
| High latency | Congestion | Check QoS, review bandwidth utilization |
| Config apply fails | Validation error | Review diff, fix syntax, re-validate |
| Security event flood | Misconfigured rule | Review rule, adjust threshold |
| Bandwidth spike | DDoS or legitimate surge | Check traffic classes, trace source |
| Forecast bottleneck | Growth exceeding plan | Initiate upgrade process |
| DNS slow | Server overload | Check DNS server health, add redundancy |
| Route flapping | Link instability | Check physical, adjust metrics, enable dampening |
| QoS not enforced | Policy misapplied | Verify policy, check class maps |
| Config rollback fails | Backup issue | Restore from alternate backup |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = NetOpsAgent()
# Now all operations will log detailed debug information
```

---

## FAQ

### Q: Can I use components independently?
A: Yes, each component (NetworkMonitor, ConfigurationManager, etc.) can be used standalone without the NetOpsAgent facade.

### Q: How many devices can I manage?
A: No hard limit. Performance tested with 10,000+ devices using hash-based indexing.

### Q: Can I rollback configurations?
A: Yes, every config apply creates an automatic backup. Use `rollback_config()` to revert.

### Q: How accurate are capacity forecasts?
A: Forecasts use linear regression and are most accurate with 5+ data points. Review quarterly.

### Q: Can I integrate with existing NMS?
A: Yes, the agent provides APIs that can be called from Nagios, Zabbix, or other NMS platforms.

### Q: How do I handle multi-vendor environments?
A: The agent is vendor-agnostic. Add devices with vendor metadata for tracking.

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/netops/
pytest --cov=agents.netops
```

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

## Support

- Documentation: [docs.example.com](https://docs.example.com)
- Issues: [GitHub Issues](https://github.com/awesome-grok-skills/awesome-grok-skills/issues)
- Discussions: [GitHub Discussions](https://github.com/awesome-grok-skills/awesome-grok-skills/discussions)
