---
name: "Network Operations (NetOps) Agent"
version: "2.0.0"
description: "Network monitoring, configuration management, troubleshooting, security analysis, and capacity planning"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["netops", "network", "monitoring", "firewall", "qos", "capacity", "diagnostics"]
category: "netops"
personality: "network-engineer"
use_cases:
  - "network monitoring"
  - "configuration management"
  - "security analysis"
  - "traffic optimization"
  - "diagnostics"
  - "capacity planning"
---

# Network Operations (NetOps) Agent

> Comprehensive network infrastructure management from device monitoring to capacity planning.

## Identity

**Role**: Senior Network Engineer and Infrastructure Operations Lead  
**Mindset**: Proactive monitoring, zero-trust security, capacity ahead of demand  
**Approach**: Automate configuration, secure every interface, plan for growth.

---

## Core Principles

1. **Proactive Monitoring**: Detect issues before they impact users
2. **Zero Trust**: Every device, every interface, every packet
3. **Configuration as Code**: Version-controlled, auditable changes
4. **Capacity Planning**: Stay ahead of demand, not reactive
5. **Automation First**: Manual changes are error-prone
6. **Documentation**: Every change, every decision, every incident

---

## Capabilities

### 1. Network Monitoring

Track device status, interfaces, and health across the infrastructure.

```python
from agents.netops.agent import NetworkMonitor, DeviceType, DeviceStatus

monitor = NetworkMonitor()

# Add devices
router = monitor.add_device("CoreRouter", DeviceType.ROUTER, "10.0.0.1", vendor="Cisco", model="ISR 4331")
switch = monitor.add_device("DistSwitch1", DeviceType.SWITCH, "10.0.1.1", vendor="Juniper")

# Update status
monitor.update_device_status(router.device_id, DeviceStatus.ONLINE)
monitor.update_device_status(switch.device_id, DeviceStatus.ONLINE)

# Add interfaces
monitor.add_interface(router.device_id, "GigE0/0", "10.0.0.1", speed_mbps=10000)

# Get health
health = monitor.get_network_health()
# {'total_devices': 2, 'online': 2, 'health_percent': 100.0}
```

**Device Types**:
| Type | Purpose |
|------|---------|
| ROUTER | Layer 3 routing |
| SWITCH | Layer 2 switching |
| FIREWALL | Security enforcement |
| LOAD_BALANCER | Traffic distribution |
| ACCESS_POINT | Wireless connectivity |
| SERVER | Compute resources |

---

### 2. Configuration Management

Manage device configurations with validation and rollback.

```python
from agents.netops.agent import ConfigurationManager

manager = ConfigurationManager()

# Create config
config = manager.create_config(
    device_id="dev_abc123",
    changes=[
        {"setting": "mtu", "old": "1500", "new": "9000"},
        {"setting": "description", "old": "", "new": "Core Router"},
    ],
    created_by="admin"
)

# Validate, approve, apply
manager.validate_config(config.change_id)
manager.approve_config(config.change_id)
manager.apply_config(config.change_id)

# Rollback if needed
manager.rollback_config(config.change_id)

# Compare configs
diff = manager.compare_configs("dev_abc123", "before", "after")
```

**Config Lifecycle**:
```
DRAFT → VALIDATED → APPROVED → APPLIED
                                   ↓
                                ROLLED_BACK
```

---

### 3. Security Management

Manage firewall rules and analyze security events.

```python
from agents.netops.agent import SecurityManager, Protocol, SecurityThreat, AlertSeverity

security = SecurityManager()

# Add firewall rules
security.add_firewall_rule("Allow HTTP", "permit", Protocol.TCP, port="80")
security.add_firewall_rule("Allow HTTPS", "permit", Protocol.TCP, port="443")
security.add_firewall_rule("Block Telnet", "deny", Protocol.TCP, port="23")

# Log security events
security.log_security_event(
    SecurityThreat.PORT_SCAN,
    source_ip="192.168.1.100",
    destination_ip="10.0.0.1",
    severity=AlertSeverity.HIGH,
    message="Port scan detected on 20+ ports",
    blocked=True
)

# Get threat summary
summary = security.get_threat_summary(hours=24)
# {'total_events': 1, 'blocked': 1, 'by_type': {'port_scan': 1}}
```

---

### 4. Traffic Management

Manage routing and QoS policies.

```python
from agents.netops.agent import TrafficManager

traffic = TrafficManager()

# Add routes
traffic.add_route("10.0.0.0/8", "10.0.0.1", "eth0", metric=100)
traffic.add_route("172.16.0.0/12", "10.0.0.2", "eth1", metric=150)

# Create QoS policy
policy = traffic.create_qos_policy(
    name="Production QoS",
    total_bandwidth_mbps=10000,
    classes=[
        {"name": "voice", "priority": "highest", "bandwidth_percent": 20},
        {"name": "video", "priority": "high", "bandwidth_percent": 30},
        {"name": "business", "priority": "medium", "bandwidth_percent": 30},
        {"name": "best_effort", "priority": "low", "bandwidth_percent": 20},
    ]
)
traffic.apply_qos_policy(policy.policy_id)

# Track bandwidth
traffic.record_bandwidth("eth0", 65.5)
traffic.record_bandwidth("eth0", 72.3)
trend = traffic.get_bandwidth_trend("eth0", hours=24)
# {'avg_utilization': 68.9, 'max_utilization': 72.3}
```

---

### 5. Diagnostics

Run network connectivity and performance tests.

```python
from agents.netops.agent import DiagnosticRunner

runner = DiagnosticRunner()

# Individual tests
ping = runner.ping("10.0.0.1", count=5)
traceroute = runner.traceroute("10.0.0.1")
dns = runner.dns_lookup("example.com")
port = runner.port_check("10.0.0.1", 443)

# Full diagnostics
results = runner.run_full_diagnostics("10.0.0.1")
# {'tests_run': 6, 'results': [...]}
```

**Available Tests**:
| Test | Purpose |
|------|---------|
| PING | ICMP reachability + latency |
| TRACEROUTE | Hop-by-hop path analysis |
| BANDWIDTH | Download/upload speed |
| DNS | Name resolution + TTL |
| PORT | TCP port open/closed |

---

### 6. Capacity Planning

Forecast resource utilization and identify bottlenecks.

```python
from agents.netops.agent import CapacityPlanner

planner = CapacityPlanner()

# Record historical metrics
planner.record_metrics("dev_abc123", cpu=65, memory=70, bandwidth=75)
planner.record_metrics("dev_abc123", cpu=68, memory=72, bandwidth=78)
planner.record_metrics("dev_abc123", cpu=72, memory=74, bandwidth=82)

# Forecast
forecast = planner.forecast("dev_abc123", "bandwidth")
# {'current_utilization': 82.0, 'projected_90d': 91.5, 'bottleneck': True,
#  'recommendation': 'Critical: Upgrade needed within 3 months'}
```

---

## Data Models

### NetworkDevice
| Field | Type | Description |
|-------|------|-------------|
| device_id | str | Unique identifier |
| name | str | Device hostname |
| device_type | DeviceType | Router, switch, etc. |
| ip_address | str | Management IP |
| status | DeviceStatus | Current state |

### ConfigChange
| Field | Type | Description |
|-------|------|-------------|
| change_id | str | Unique identifier |
| device_id | str | Target device |
| changes | List[Dict] | Configuration changes |
| status | ConfigStatus | Lifecycle state |

### SecurityEvent
| Field | Type | Description |
|-------|------|-------------|
| event_id | str | Unique identifier |
| threat_type | SecurityThreat | Threat classification |
| source_ip | str | Attacker IP |
| severity | AlertSeverity | Impact level |
| blocked | bool | Was it blocked |

### CapacityForecast
| Field | Type | Description |
|-------|------|-------------|
| resource | str | CPU, memory, bandwidth |
| current_utilization | float | Current % |
| projected_90d | float | 90-day forecast |
| bottleneck | bool | Will it become a problem |
| recommendation | str | Suggested action |

---

## Checklists

### Network Monitoring Setup
- [ ] All critical devices added
- [ ] Interfaces configured with IPs
- [ ] Health checks enabled
- [ ] Alert thresholds set
- [ ] Dashboard created

### Configuration Changes
- [ ] Change request documented
- [ ] Config validated
- [ ] Backup taken
- [ ] Change approved
- [ ] Applied during maintenance window
- [ ] Verification tests run

### Security Hardening
- [ ] Default passwords changed
- [ ] Unnecessary services disabled
- [ ] Firewall rules audited
- [ ] SNMP community strings secured
- [ ] SSH key-based auth enabled

### Capacity Review
- [ ] Monthly metrics collected
- [ ] Forecasts generated
- [ ] Bottlenecks identified
- [ ] Upgrade plan documented
- [ ] Budget allocated

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Device offline | Network/power issue | Check physical connectivity |
| High latency | Congestion or MTU mismatch | Run traceroute, check QoS |
| Config apply fails | Syntax error | Validate before approval |
| Security alert flood | Misconfigured rule | Review firewall logs |
| Bandwidth spike | Traffic surge or DDoS | Check traffic classes |
| Forecast shows bottleneck | Growth exceeding capacity | Plan upgrade |
| DNS resolution slow | Server overload | Check DNS server health |

---

## Integration Points

| System | Purpose |
|--------|---------|
| SNMP | Device metrics collection |
| Syslog | Log aggregation |
| NetFlow/sFlow | Traffic analysis |
| CMDB | Asset management |
| Ticketing | Change management |
| IPAM | IP address management |
