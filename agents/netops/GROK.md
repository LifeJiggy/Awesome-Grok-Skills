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
  - "firewall management"
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
7. **Least Privilege**: Minimal access required for operations
8. **Defense in Depth**: Multiple security layers

---

## Capabilities

### 1. Network Monitoring

Track device status, interfaces, and health across the infrastructure.

```python
from agents.netops.agent import NetworkMonitor, DeviceType, DeviceStatus

monitor = NetworkMonitor()

# Add devices
router = monitor.add_device(
    "CoreRouter",
    DeviceType.ROUTER,
    "10.0.0.1",
    vendor="Cisco",
    model="ISR 4331"
)
# Returns: NetworkDevice(device_id="dev_abc123", name="CoreRouter", ...)

switch = monitor.add_device(
    "DistSwitch1",
    DeviceType.SWITCH,
    "10.0.1.1",
    vendor="Juniper",
    model="EX4300"
)

firewall = monitor.add_device(
    "FW01",
    DeviceType.FIREWALL,
    "10.0.0.254",
    vendor="Palo Alto",
    model="PA-3260"
)

# Update status
monitor.update_device_status(router.device_id, DeviceStatus.ONLINE)
monitor.update_device_status(switch.device_id, DeviceStatus.ONLINE)
monitor.update_device_status(firewall.device_id, DeviceStatus.ONLINE)

# Add interfaces
monitor.add_interface(router.device_id, "GigE0/0", "10.0.0.1", speed_mbps=10000)
monitor.add_interface(router.device_id, "GigE0/1", "10.0.0.2", speed_mbps=10000)
monitor.add_interface(switch.device_id, "GigE0/1", "10.0.1.1", speed_mbps=1000)

# Record interface stats
monitor.record_interface_stats(router.device_id, "GigE0/0", in_octets=1500000, out_octets=2300000)

# Get network health
health = monitor.get_network_health()
# {
#   'total_devices': 3,
#   'online': 3,
#   'offline': 0,
#   'degraded': 0,
#   'health_percent': 100.0
# }

# List devices
routers = monitor.list_devices(device_type=DeviceType.ROUTER)
online_devices = monitor.list_devices(status=DeviceStatus.ONLINE)
```

**Device Types**:
| Type | Purpose | Example Vendors |
|------|---------|-----------------|
| ROUTER | Layer 3 routing, WAN | Cisco, Juniper, Arista |
| SWITCH | Layer 2 switching, LAN | Cisco, Juniper, HPE |
| FIREWALL | Security enforcement | Palo Alto, Fortinet, Cisco |
| LOAD_BALANCER | Traffic distribution | F5, HAProxy, Citrix |
| ACCESS_POINT | Wireless connectivity | Meraki, Aruba, Ubiquiti |
| SERVER | Compute resources | Dell, HPE, Lenovo |
| OPTICAL | Fiber transport | Ciena, Infinera |

---

### 2. Configuration Management

Manage device configurations with validation and rollback.

```python
from agents.netops.agent import ConfigurationManager

manager = ConfigurationManager()

# Create config change
config = manager.create_config(
    device_id="dev_abc123",
    changes=[
        {"setting": "mtu", "old_value": "1500", "new_value": "9000"},
        {"setting": "description", "old_value": "", "new_value": "Core Router"},
        {"setting": "snmp_community", "old_value": "public", "new_value": "secure_string"}
    ],
    created_by="netadmin"
)
# Returns: ConfigChange(change_id="chg_xyz789", status=DRAFT, ...)

# Validate configuration
manager.validate_config(config.change_id)
# Status: DRAFT → VALIDATED

# Approve configuration
manager.approve_config(config.change_id)
# Status: VALIDATED → APPROVED

# Apply configuration
manager.apply_config(config.change_id)
# Status: APPROVED → APPLIED
# Backup automatically created

# Rollback if needed
manager.rollback_config(config.change_id)
# Status: APPLIED → ROLLED_BACK
# Previous config restored

# Compare configs
diff = manager.compare_configs("dev_abc123", "before", "after")
# {
#   'device_id': 'dev_abc123',
#   'changes': [
#     {'setting': 'mtu', 'old': '1500', 'new': '9000'},
#     {'setting': 'description', 'old': '', 'new': 'Core Router'}
#   ]
# }

# Backup current config
backup = manager.backup_config("dev_abc123")
# Returns backup ID for future rollback
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
security.add_firewall_rule("Allow SSH", "permit", Protocol.TCP, port="22", source_ip="10.0.0.0/8")
security.add_firewall_rule("Block Telnet", "deny", Protocol.TCP, port="23")
security.add_firewall_rule("Block FTP", "deny", Protocol.TCP, port="21")

# Enable/disable rules
security.enable_rule(rule_id)
security.disable_rule(rule_id)

# Log security events
security.log_security_event(
    SecurityThreat.PORT_SCAN,
    source_ip="192.168.1.100",
    destination_ip="10.0.0.1",
    severity=AlertSeverity.HIGH,
    message="Port scan detected on 20+ ports",
    blocked=True
)

security.log_security_event(
    SecurityThreat.BRUTE_FORCE,
    source_ip="192.168.1.50",
    destination_ip="10.0.0.1",
    severity=AlertSeverity.CRITICAL,
    message="50 failed SSH attempts in 5 minutes",
    blocked=True
)

# Get threat summary
summary = security.get_threat_summary(hours=24)
# {
#   'total_events': 2,
#   'blocked': 2,
#   'by_type': {
#     'port_scan': 1,
#     'brute_force': 1
#   },
#   'by_severity': {
#     'HIGH': 1,
#     'CRITICAL': 1
#   }
# }

# Analyze firewall rules
analysis = security.analyze_firewall()
# {
#   'total_rules': 5,
#   'enabled': 5,
#   'disabled': 0,
#   'permit_rules': 3,
#   'deny_rules': 2,
#   'recommendations': ['Consider adding rate limiting for SSH']
# }
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
traffic.add_route("192.168.0.0/16", "10.0.0.3", "eth2", metric=200)

# Optimize routes
optimizations = traffic.optimize_routes()
# [
#   {'route': '192.168.0.0/16', 'suggestion': 'Reduce metric to 150 for faster failover'},
#   {'route': '172.16.0.0/12', 'suggestion': 'Consider load balancing across eth1 and eth2'}
# ]

# Create QoS policy
policy = traffic.create_qos_policy(
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

# Apply QoS policy
traffic.apply_qos_policy(policy.policy_id)

# Track bandwidth
traffic.record_bandwidth("eth0", 65.5)
traffic.record_bandwidth("eth0", 72.3)
traffic.record_bandwidth("eth0", 58.9)

# Get bandwidth trend
trend = traffic.get_bandwidth_trend("eth0", hours=24)
# {
#   'interface': 'eth0',
#   'hours': 24,
#   'avg_utilization': 65.6,
#   'max_utilization': 72.3,
#   'min_utilization': 58.9,
#   'data_points': 3
# }
```

---

### 5. Diagnostics

Run network connectivity and performance tests.

```python
from agents.netops.agent import DiagnosticRunner

runner = DiagnosticRunner()

# Individual tests
ping = runner.ping("10.0.0.1", count=5)
# {
#   'target': '10.0.0.1',
#   'packets_sent': 5,
#   'packets_received': 5,
#   'packet_loss': 0.0,
#   'avg_latency_ms': 1.2,
#   'min_latency_ms': 0.8,
#   'max_latency_ms': 1.8,
#   'reachable': True
# }

traceroute = runner.traceroute("10.0.0.1", max_hops=15)
# {
#   'target': '10.0.0.1',
#   'hops': [
#     {'hop': 1, 'ip': '10.0.0.1', 'latency_ms': 1.2},
#   ],
#   'total_hops': 1
# }

dns = runner.dns_lookup("example.com")
# {
#   'hostname': 'example.com',
#   'ip_addresses': ['93.184.216.34'],
#   'ttl': 3600,
#   'resolve_time_ms': 15
# }

port = runner.port_check("10.0.0.1", 443)
# {
#   'target': '10.0.0.1',
#   'port': 443,
#   'open': True,
#   'response_time_ms': 2
# }

# Full diagnostics against single target
results = runner.run_full_diagnostics("10.0.0.1")
# {
#   'target': '10.0.0.1',
#   'tests_run': 5,
#   'tests_passed': 5,
#   'results': {
#     'ping': {...},
#     'traceroute': {...},
#     'dns': {...},
#     'port_80': {...},
#     'port_443': {...}
#   }
# }
```

**Available Tests**:
| Test | Purpose | Output |
|------|---------|--------|
| PING | ICMP reachability + latency | Packet loss, avg/min/max latency |
| TRACEROUTE | Hop-by-hop path analysis | Hop list with latencies |
| BANDWIDTH | Download/upload speed | Throughput in Mbps |
| DNS | Name resolution + TTL | IP addresses, TTL |
| PORT | TCP port open/closed | Open/closed status |

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
planner.record_metrics("dev_abc123", cpu=75, memory=76, bandwidth=85)
planner.record_metrics("dev_abc123", cpu=78, memory=78, bandwidth=88)

# Generate forecast
forecast = planner.forecast("dev_abc123", "bandwidth")
# {
#   'device_id': 'dev_abc123',
#   'resource': 'bandwidth',
#   'current_utilization': 88.0,
#   'projected_30d': 91.2,
#   'projected_90d': 97.5,
#   'projected_180d': 107.0,
#   'bottleneck': True,
#   'recommendation': 'Critical: Upgrade needed within 1 month'
# }

# Forecast CPU
cpu_forecast = planner.forecast("dev_abc123", "cpu")
# {
#   'current_utilization': 78.0,
#   'projected_90d': 89.5,
#   'bottleneck': True,
#   'recommendation': 'Warning: Plan upgrade within 3 months'
# }

# Forecast memory
mem_forecast = planner.forecast("dev_abc123", "memory")
# {
#   'current_utilization': 78.0,
#   'projected_90d': 86.5,
#   'bottleneck': True,
#   'recommendation': 'Warning: Plan upgrade within 3 months'
# }
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
| vendor | str | Device vendor |
| model | str | Device model |
| status | DeviceStatus | Current state |
| created_at | datetime | Registration time |

### Interface
| Field | Type | Description |
|-------|------|-------------|
| interface_id | str | Unique identifier |
| device_id | str | Parent device |
| name | str | Interface name (e.g., GigE0/0) |
| ip_address | str | Interface IP |
| speed_mbps | int | Interface speed |
| status | str | up/down |

### ConfigChange
| Field | Type | Description |
|-------|------|-------------|
| change_id | str | Unique identifier |
| device_id | str | Target device |
| changes | List[Dict] | Configuration changes |
| status | ConfigStatus | Lifecycle state |
| created_by | str | Author |
| created_at | datetime | Creation time |

### FirewallRule
| Field | Type | Description |
|-------|------|-------------|
| rule_id | str | Unique identifier |
| name | str | Rule name |
| action | str | permit/deny |
| protocol | Protocol | TCP/UDP/ICMP/ANY |
| source_ip | str | Source IP/CIDR |
| destination_ip | str | Destination IP/CIDR |
| port | str | Port number |
| enabled | bool | Is rule active |

### SecurityEvent
| Field | Type | Description |
|-------|------|-------------|
| event_id | str | Unique identifier |
| threat_type | SecurityThreat | Threat classification |
| source_ip | str | Attacker IP |
| destination_ip | str | Target IP |
| severity | AlertSeverity | Impact level |
| message | str | Description |
| blocked | bool | Was it blocked |
| timestamp | datetime | Event time |

### CapacityForecast
| Field | Type | Description |
|-------|------|-------------|
| device_id | str | Device identifier |
| resource | str | CPU, memory, bandwidth |
| current_utilization | float | Current % |
| projected_30d | float | 30-day forecast |
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
- [ ] Device inventory documented
- [ ] SNMP credentials secured
- [ ] Backup power verified

### Configuration Changes
- [ ] Change request documented
- [ ] Config validated
- [ ] Backup taken
- [ ] Change approved
- [ ] Applied during maintenance window
- [ ] Verification tests run
- [ ] Rollback plan ready
- [ ] Changes documented

### Security Hardening
- [ ] Default passwords changed
- [ ] Unnecessary services disabled
- [ ] Firewall rules audited
- [ ] SNMP community strings secured
- [ ] SSH key-based auth enabled
- [ ] Access lists reviewed
- [ ] Logging enabled
- [ ] Intrusion detection active

### Capacity Review
- [ ] Monthly metrics collected
- [ ] Forecasts generated
- [ ] Bottlenecks identified
- [ ] Upgrade plan documented
- [ ] Budget allocated
- [ ] Vendor quotes obtained
- [ ] Implementation timeline set
- [ ] Stakeholders notified

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Device offline | Network/power issue | Check physical connectivity, ping management IP |
| High latency | Congestion or MTU mismatch | Run traceroute, check QoS, verify MTU |
| Config apply fails | Syntax error | Validate before approval, check diff |
| Security alert flood | Misconfigured rule | Review firewall logs, adjust thresholds |
| Bandwidth spike | Traffic surge or DDoS | Check traffic classes, trace source |
| Forecast shows bottleneck | Growth exceeding capacity | Plan upgrade, get budget approval |
| DNS resolution slow | Server overload | Check DNS server health, add redundancy |
| Route flapping | Link instability | Check physical, adjust metrics, enable dampening |
| QoS not working | Policy not applied | Verify policy application, check class maps |
| Config rollback fails | Backup corrupted | Restore from alternate backup |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = NetOpsAgent()
# Now all operations will log detailed debug information
```

---

## Integration Points

| System | Purpose |
|--------|---------|
| SNMP | Device metrics collection (v2c, v3) |
| Syslog | Log aggregation and analysis |
| NetFlow/sFlow | Traffic analysis and monitoring |
| CMDB | Asset management and inventory |
| Ticketing | Change management (Jira, ServiceNow) |
| IPAM | IP address management |
| NMS | Network management systems (Nagios, Zabbix) |
| SIEM | Security event correlation |

---

## Advanced Usage

### Bulk Device Discovery
```python
agent = NetOpsAgent()

devices = [
    {"name": "Router1", "type": "router", "ip": "10.0.0.1", "vendor": "Cisco"},
    {"name": "Switch1", "type": "switch", "ip": "10.0.1.1", "vendor": "Juniper"},
    {"name": "FW01", "type": "firewall", "ip": "10.0.0.254", "vendor": "Palo Alto"},
]

for device in devices:
    dev = agent.monitor.add_device(device["name"], device["type"], device["ip"], vendor=device["vendor"])
    agent.monitor.update_device_status(dev.device_id, DeviceStatus.ONLINE)

health = agent.monitor.get_network_health()
print(f"Discovered {health['total_devices']} devices, {health['health_percent']}% healthy")
```

### Security Audit
```python
agent = NetOpsAgent()

# Add rules
agent.security.add_firewall_rule("Allow HTTP", "permit", Protocol.TCP, port="80")
agent.security.add_firewall_rule("Allow HTTPS", "permit", Protocol.TCP, port="443")
agent.security.add_firewall_rule("Block Telnet", "deny", Protocol.TCP, port="23")

# Log events
agent.security.log_security_event(SecurityThreat.PORT_SCAN, "192.168.1.100", "10.0.0.0/8", AlertSeverity.HIGH, "SYN scan")

# Get summary
summary = agent.security.get_threat_summary(hours=24)
print(f"Threats: {summary['total_events']}, Blocked: {summary['blocked']}")

# Analyze rules
analysis = agent.security.analyze_firewall()
print(f"Rules: {analysis['total_rules']}, Recommendations: {analysis['recommendations']}")
```

### Complete Capacity Planning
```python
agent = NetOpsAgent()

# Simulate 6 months of growing utilization
for cpu, mem, bw in [(50, 55, 60), (55, 58, 65), (60, 62, 70), (65, 66, 75), (70, 70, 80), (75, 75, 85)]:
    agent.capacity.record_metrics("router_1", cpu=cpu, memory=mem, bandwidth=bw)

# Forecast all resources
for resource in ["cpu", "memory", "bandwidth"]:
    forecast = agent.capacity.forecast("router_1", resource)
    print(f"{resource}: {forecast.current_utilization}% → {forecast.projected_90d}% (90d)")
    print(f"  Bottleneck: {forecast.bottleneck}, Action: {forecast.recommendation}")
```
