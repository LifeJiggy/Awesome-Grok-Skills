---
name: network-engineering
category: networking
version: 2.0.0
tags: [networking, network-engineering, routing, switching, protocols]
---

# Network Engineering

## Overview

Network engineering toolkit covering routing protocols, subnetting, VLAN configuration, NAT/PAT, VPN setup, network monitoring, and infrastructure automation. This skill provides practical implementations for network design, IP addressing schemes, protocol analysis, and automated network configuration management.

## Core Capabilities

- **IP Addressing**: CIDR notation, subnet calculation, VLSM, IPv4/IPv6 planning
- **Routing**: Static routes, OSPF, BGP concepts, routing table management
- **VLAN Configuration**: Tagged/untagged ports, inter-VLAN routing, trunking
- **NAT/PAT**: Source NAT, destination NAT, port forwarding rules
- **VPN**: WireGuard, IPSec, OpenVPN configuration generation
- **Network Monitoring**: Bandwidth analysis, latency measurement, packet capture
- **DNS Management**: Zone files, record types, split-horizon DNS
- **Infrastructure Automation**: Ansible playbook generation, network config templating

## Usage Examples

```python
import ipaddress
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ANY = "any"

@dataclass
class FirewallRule:
    name: str
    action: str  # allow, deny
    protocol: Protocol
    source: str
    destination: str
    ports: List[int] = field(default_factory=list)
    direction: str = "inbound"
    enabled: bool = True

    def toiptables(self) -> str:
        chain = "INPUT" if self.direction == "inbound" else "OUTPUT"
        proto = f"-p {self.protocol.value}" if self.protocol != Protocol.ANY else ""
        ports = f"--dport {self.ports[0]}" if self.ports else ""
        return f"iptables -A {chain} -s {self.source} -d {self.destination} {proto} {ports} -j {self.action.upper()}"

class SubnetCalculator:
    def __init__(self, network: str):
        self.network = ipaddress.ip_network(network, strict=False)

    def get_hosts(self) -> int:
        return self.network.num_addresses - 2

    def get_subnets(self, prefix_length: int) -> List[str]:
        return [str(s) for s in self.network.subnets(new_prefix=prefix_length)]

    def get_first_host(self) -> str:
        return str(self.network.network_address + 1)

    def get_last_host(self) -> str:
        return str(self.network.broadcast_address - 1)

    def get_cidr(self) -> str:
        return f"{self.network.network_address}/{self.network.prefixlen}"

    def supernet(self, prefix_length: int) -> str:
        return str(self.network.supernet(new_prefix=prefix_length))

class NetworkMonitor:
    def __init__(self):
        self._metrics: Dict[str, List[float]] = {}

    def record_latency(self, host: str, latency_ms: float):
        if host not in self._metrics:
            self._metrics[host] = []
        self._metrics[host].append(latency_ms)
        if len(self._metrics[host]) > 1000:
            self._metrics[host] = self._metrics[host][-1000:]

    def get_stats(self, host: str) -> Dict:
        if host not in self._metrics or not self._metrics[host]:
            return {"host": host, "samples": 0}
        data = self._metrics[host]
        return {
            "host": host,
            "samples": len(data),
            "avg_ms": sum(data) / len(data),
            "min_ms": min(data),
            "max_ms": max(data),
            "jitter_ms": max(data) - min(data),
        }

class DNSZoneManager:
    def __init__(self, domain: str, ttl: int = 3600):
        self.domain = domain
        self.ttl = ttl
        self.records: List[Dict] = []

    def add_a_record(self, name: str, ip: str, ttl: Optional[int] = None):
        self.records.append({"type": "A", "name": f"{name}.{self.domain}", "ip": ip, "ttl": ttl or self.ttl})

    def add_cname(self, name: str, target: str, ttl: Optional[int] = None):
        self.records.append({"type": "CNAME", "name": f"{name}.{self.domain}", "target": target, "ttl": ttl or self.ttl})

    def add_mx(self, name: str, mail_server: str, priority: int = 10, ttl: Optional[int] = None):
        self.records.append({"type": "MX", "name": self.domain, "mail_server": mail_server, "priority": priority, "ttl": ttl or self.ttl})

    def generate_zone_file(self) -> str:
        lines = [f"; Zone file for {self.domain}", f"$TTL {self.ttl}", f"@ IN SOA ns1.{self.domain}. admin.{self.domain}. ("]
        lines.append("    2024010101 ; Serial")
        lines.append("    3600       ; Refresh")
        lines.append("    900        ; Retry")
        lines.append("    604800     ; Expire")
        lines.append("    86400      ; Minimum TTL")
        lines.append(")")
        for rec in self.records:
            if rec["type"] == "A":
                lines.append(f'{rec["name"]} IN A {rec["ip"]}')
            elif rec["type"] == "CNAME":
                lines.append(f'{rec["name"]} IN CNAME {rec["target"]}')
            elif rec["type"] == "MX":
                lines.append(f'{rec["name"]} IN MX {rec["priority"]} {rec["mail_server"]}')
        return "\n".join(lines)
```

## Best Practices

- Use VLSM for efficient IP address allocation across subnets
- Document all network changes with timestamps and justification
- Implement network monitoring with latency, bandwidth, and error metrics
- Use firewall rules with explicit deny-all default policies
- Maintain configuration backups before any network change
- Use split-horizon DNS for internal vs. external resolution
- Implement redundant paths for critical network infrastructure
- Use BGP for multi-homing and ISP failover in production networks
- Regularly audit firewall rules for unused or overly permissive entries
- Automate network configuration with Ansible or Terraform for consistency

## Related Modules

- `load-balancing` - Traffic distribution across backends
- `dns-management` - DNS infrastructure and resolution
- `sdn` - Software-defined networking
- `traffic-analysis` - Network traffic analysis and optimization

## Advanced Configuration

### Network Device Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `mtu_size` | 1500 | 576 - 9000 | Maximum Transmission Unit |
| `vlan_id` | 1 | 1 - 4094 | VLAN identifier |
| `ospf_area` | 0 | 0 - 65535 | OSPF area ID |
| `bgp_asn` | 65000 | 1 - 4294967295 | BGP Autonomous System Number |
| `stp_priority` | 32768 | 0 - 61440 | Spanning Tree Priority |
| `acl_max_entries` | 100 | 10 - 1000 | Maximum ACL entries |

### Advanced Network Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import ipaddress

class RoutingProtocol(Enum):
    STATIC = "static"
    OSPF = "ospf"
    BGP = "bgp"
    RIP = "rip"
    EIGRP = "eigrp"

@dataclass
class NetworkConfig:
    hostname: str = "router"
    routing_protocol: RoutingProtocol = RoutingProtocol.STATIC
    ospf_area: int = 0
    bgp_asn: int = 65000
    enable_ip_routing: bool = True
    enable_cdp: bool = True
    enable_ssh: bool = True
    enable_https: bool = True
    syslog_server: str = ""
    ntp_server: str = ""
    snmp_community: str = "public"

class RouterConfig:
    def __init__(self, config: NetworkConfig = None):
        self.config = config or NetworkConfig()
        self._interfaces: Dict[str, dict] = {}
        self._routes: List[dict] = []
        self._acls: Dict[str, List[dict]] = {}

    def configure_interface(self, name: str, ip: str, mask: str,
                           description: str = "", vlan: int = None):
        self._interfaces[name] = {
            "ip": ip, "mask": mask, "description": description,
            "vlan": vlan, "status": "up",
        }

    def add_static_route(self, destination: str, gateway: str, metric: int = 1):
        self._routes.append({
            "type": "static", "destination": destination,
            "gateway": gateway, "metric": metric,
        })

    def add_ospf_network(self, network: str, area: int = 0):
        self._routes.append({
            "type": "ospf", "network": network, "area": area,
        })

    def add_acl_entry(self, acl_name: str, action: str, source: str,
                     destination: str, protocol: str = "ip"):
        if acl_name not in self._acls:
            self._acls[acl_name] = []
        self._acls[acl_name].append({
            "action": action, "source": source,
            "destination": destination, "protocol": protocol,
        })

    def generate_config(self) -> str:
        lines = [f"hostname {self.config.hostname}"]
        if self.config.enable_ip_routing:
            lines.append("ip routing")
        if self.config.enable_ssh:
            lines.append("ip ssh version 2")
        for name, iface in self._interfaces.items():
            lines.append(f"interface {name}")
            if iface.get("description"):
                lines.append(f"  description {iface['description']}")
            lines.append(f"  ip address {iface['ip']} {iface['mask']}")
            if iface.get("vlan"):
                lines.append(f"  switchport access vlan {iface['vlan']}")
            lines.append("  no shutdown")
        for route in self._routes:
            if route["type"] == "static":
                lines.append(f"ip route {route['destination']} {route['gateway']} {route['metric']}")
        for acl_name, entries in self._acls.items():
            for i, entry in enumerate(entries, 1):
                lines.append(f"access-list {acl_name} {entry['action']} {entry['source']} {entry['destination']}")
        return "\n".join(lines)

class VlanManager:
    def __init__(self):
        self._vlans: Dict[int, dict] = {}
        self._ports: Dict[str, dict] = {}

    def create_vlan(self, vlan_id: int, name: str):
        self._vlans[vlan_id] = {"name": name, "ports": []}

    def assign_port(self, port: str, vlan_id: int, mode: str = "access"):
        self._ports[port] = {"vlan_id": vlan_id, "mode": mode}
        if vlan_id in self._vlans:
            self._vlans[vlan_id]["ports"].append(port)

    def get_vlan_summary(self) -> Dict[int, dict]:
        return {vid: {"name": v["name"], "port_count": len(v["ports"])}
                for vid, v in self._vlans.items()}

class IpSubnetCalculator:
    def __init__(self, network: str):
        self.network = ipaddress.ip_network(network, strict=False)

    def get_subnets(self, prefix_length: int) -> List[str]:
        return [str(s) for s in self.network.subnets(new_prefix=prefix_length)]

    def get_host_range(self) -> Tuple[str, str]:
        hosts = list(self.network.hosts())
        return (str(hosts[0]), str(hosts[-1])) if hosts else ("", "")

    def get_cidr(self) -> str:
        return f"{self.network.network_address}/{self.network.prefixlen}"

    def get_wildcard_mask(self) -> str:
        netmask = self.network.netmask
        wildcard = ipaddress.IPv4Address(int(netmask) ^ 0xFFFFFFFF)
        return str(wildcard)

    def summarize_routes(self, subnets: List[str]) -> List[str]:
        networks = [ipaddress.ip_network(s, strict=False) for s in subnets]
        summarized = ipaddress.summarize_address_range(
            min(n.network_address for n in networks),
            max(n.broadcast_address for n in networks)
        )
        return [str(s) for s in summarized]
```

### VPN Configuration

```python
class WireGuardConfig:
    def __init__(self, interface_name: str = "wg0"):
        self.interface_name = interface_name
        self._peers: List[dict] = []

    def set_interface(self, private_key: str, address: str, listen_port: int = 51820):
        self.interface = {
            "private_key": private_key,
            "address": address,
            "listen_port": listen_port,
        }

    def add_peer(self, public_key: str, allowed_ips: List[str],
                 endpoint: str = "", keepalive: int = 25):
        self._peers.append({
            "public_key": public_key,
            "allowed_ips": allowed_ips,
            "endpoint": endpoint,
            "persistent_keepalive": keepalive,
        })

    def generate_config(self) -> str:
        lines = [f"[Interface]", f"PrivateKey = {self.interface['private_key']}",
                 f"Address = {self.interface['address']}",
                 f"ListenPort = {self.interface['listen_port']}"]
        for peer in self._peers:
            lines.append("")
            lines.append("[Peer]")
            lines.append(f"PublicKey = {peer['public_key']}")
            lines.append(f"AllowedIPs = {', '.join(peer['allowed_ips'])}")
            if peer['endpoint']:
                lines.append(f"Endpoint = {peer['endpoint']}")
            lines.append(f"PersistentKeepalive = {peer['persistent_keepalive']}")
        return "\n".join(lines)
```

### NAT Configuration

```python
class NatManager:
    def __init__(self):
        self._nat_rules: List[dict] = []

    def add_source_nat(self, internal_net: str, translated_ip: str):
        self._nat_rules.append({
            "type": "source", "internal": internal_net,
            "translated": translated_ip,
        })

    def add_destination_nat(self, external_ip: str, internal_ip: str, port: int):
        self._nat_rules.append({
            "type": "destination", "external": external_ip,
            "internal": internal_ip, "port": port,
        })

    def add_port_forward(self, external_port: int, internal_ip: str, internal_port: int):
        self._nat_rules.append({
            "type": "port_forward", "external_port": external_port,
            "internal_ip": internal_ip, "internal_port": internal_port,
        })

    def generate_iptables(self) -> str:
        lines = ["# NAT Rules"]
        for rule in self._nat_rules:
            if rule["type"] == "source":
                lines.append(f"iptables -t nat -A POSTROUTING -s {rule['internal']} -o eth0 -j MASQUERADE")
            elif rule["type"] == "destination":
                lines.append(f"iptables -t nat -A PREROUTING -d {rule['external']} -p tcp --dport {rule['port']} -j DNAT --to-destination {rule['internal']}:{rule['port']}")
            elif rule["type"] == "port_forward":
                lines.append(f"iptables -t nat -A PREROUTING -p tcp --dport {rule['external_port']} -j DNAT --to-destination {rule['internal_ip']}:{rule['internal_port']}")
        return "\n".join(lines)
```

## Architecture Patterns

### Hierarchical Network Design

```
┌─────────────────────────────────────────────┐
│                 Core Layer                   │
│         (High-speed routing, redundancy)     │
└──────────────────┬──────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───┴───┐     ┌───┴───┐     ┌───┴───┐
│Dist-1 │     │Dist-2 │     │Dist-3 │
│Layer  │     │Layer  │     │Layer  │
└───┬───┘     └───┬───┘     └───┬───┘
    │              │              │
┌───┴───┐     ┌───┴───┐     ┌───┴───┐
│Access │     │Access │     │Access │
│Layer  │     │Layer  │     │Layer  │
└───────┘     └───────┘     └───────┘
```

### Network Segmentation

```python
class NetworkSegmentation:
    def __init__(self):
        self._segments: Dict[str, dict] = {}

    def create_segment(self, name: str, cidr: str, vlan_id: int):
        self._segments[name] = {
            "cidr": cidr, "vlan_id": vlan_id,
            "hosts": [], "gateway": None,
        }

    def assign_host(self, segment: str, host_ip: str):
        if segment in self._segments:
            self._segments[segment]["hosts"].append(host_ip)

    def set_gateway(self, segment: str, gateway_ip: str):
        if segment in self._segments:
            self._segments[segment]["gateway"] = gateway_ip

    def get_segment_info(self, name: str) -> dict:
        return self._segments.get(name, {})

    def list_segments(self) -> List[dict]:
        return [{"name": k, **v} for k, v in self._segments.items()]
```

### Firewall Rule Management

```python
class FirewallRuleManager:
    def __init__(self):
        self._rules: List[dict] = []

    def add_rule(self, name: str, action: str, protocol: str,
                source: str, destination: str, ports: List[int] = None,
                direction: str = "inbound"):
        self._rules.append({
            "name": name, "action": action, "protocol": protocol,
            "source": source, "destination": destination,
            "ports": ports or [], "direction": direction, "enabled": True,
        })

    def remove_rule(self, name: str):
        self._rules = [r for r in self._rules if r["name"] != name]

    def disable_rule(self, name: str):
        for rule in self._rules:
            if rule["name"] == name:
                rule["enabled"] = False

    def generate_iptables(self) -> str:
        lines = ["# Firewall Rules"]
        for rule in self._rules:
            if not rule["enabled"]:
                continue
            chain = "INPUT" if rule["direction"] == "inbound" else "OUTPUT"
            proto = f"-p {rule['protocol']}" if rule["protocol"] != "any" else ""
            ports = f"--dport {','.join(map(str, rule['ports']))}" if rule["ports"] else ""
            lines.append(f"iptables -A {chain} -s {rule['source']} -d {rule['destination']} {proto} {ports} -j {rule['action'].upper()}")
        return "\n".join(lines)

    def get_rules(self) -> List[dict]:
        return [r for r in self._rules if r["enabled"]]
```

## Integration Guide

### Ansible Integration

```python
class AnsiblePlaybookGenerator:
    def __init__(self):
        self._tasks: List[dict] = []

    def add_task(self, name: str, module: str, params: dict):
        self._tasks.append({"name": name, module: params})

    def generate_playbook(self, hosts: str = "all") -> str:
        import yaml
        playbook = [{
            "hosts": hosts,
            "tasks": self._tasks,
        }]
        return yaml.dump(playbook, default_flow_style=False)

    def add_interface_config(self, device: str, interface: str, ip: str, mask: str):
        self.add_task(
            f"Configure {interface} on {device}",
            "cisco.ios.ios_interfaces",
            {"config": [{"name": interface, "ipv4": [{"address": f"{ip} {mask}"}]}]}
        )
```

### Terraform Integration

```python
class TerraformConfigGenerator:
    def __init__(self):
        self._resources: List[dict] = []

    def add_aws_vpc(self, name: str, cidr: str):
        self._resources.append({
            "type": "aws_vpc",
            "name": name,
            "config": {"cidr_block": cidr},
        })

    def add_aws_subnet(self, name: str, vpc_ref: str, cidr: str, az: str):
        self._resources.append({
            "type": "aws_subnet",
            "name": name,
            "config": {"vpc_id": f"${{aws_vpc.{vpc_ref}.id}}", "cidr_block": cidr, "availability_zone": az},
        })

    def generate_tf(self) -> str:
        lines = []
        for res in self._resources:
            lines.append(f'resource "{res["type"]}" "{res["name"]}" {{')
            for key, value in res["config"].items():
                lines.append(f'  {key} = "{value}"')
            lines.append("}")
            lines.append("")
        return "\n".join(lines)
```

## Performance Optimization

### Network Performance Metrics

| Metric | Target | Strategy |
|--------|--------|----------|
| Latency (LAN) | < 1ms | Switch fabric optimization |
| Latency (WAN) | < 50ms | CDN, edge computing |
| Throughput | Line rate | Jumbo frames, RSS |
| Packet loss | < 0.01% | QoS, buffer management |
| Convergence time | < 1s | Fast failover protocols |
| CPU utilization | < 50% | Hardware offloading |

### QoS Configuration

```python
class QosManager:
    def __init__(self):
        self._classes: Dict[str, dict] = {}

    def define_class(self, name: str, bandwidth_percent: float,
                     priority: int = 0, queue_size: int = 64):
        self._classes[name] = {
            "bandwidth": bandwidth_percent,
            "priority": priority,
            "queue_size": queue_size,
        }

    def assign_traffic(self, class_name: str, match_criteria: dict):
        if class_name in self._classes:
            self._classes[class_name]["match"] = match_criteria

    def generate_config(self) -> str:
        lines = ["# QoS Configuration"]
        for name, cls in self._classes.items():
            lines.append(f"class-map {name}")
            lines.append(f"  match {cls.get('match', {})}")
            lines.append(f"policy-map {name}")
            lines.append(f"  class {name}")
            lines.append(f"    bandwidth {cls['bandwidth']}%")
        return "\n".join(lines)
```

## Security Considerations

### Network Security Hardening

```python
class SecurityHardening:
    def __init__(self):
        self._hardening_rules: List[dict] = []

    def disable_unused_services(self, services: List[str]):
        for service in services:
            self._hardening_rules.append({
                "rule": f"no {service}",
                "description": f"Disable {service}",
            })

    def enable_ssh_security(self, key_only: bool = True, port: int = 22):
        self._hardening_rules.append({
            "rule": f"ip ssh version 2",
            "description": "Enable SSH v2",
        })
        if key_only:
            self._hardening_rules.append({
                "rule": "ip ssh authentication-retries 3",
                "description": "Limit SSH retries",
            })

    def enable_acls(self):
        self._hardening_rules.append({
            "rule": "access-list 100 deny ip any any log",
            "description": "Deny and log all traffic",
        })

    def generate_hardening_config(self) -> str:
        lines = ["# Security Hardening"]
        for rule in self._hardening_rules:
            lines.append(f"! {rule['description']}")
            lines.append(rule["rule"])
        return "\n".join(lines)
```

### AAA Configuration

```python
class AaaConfig:
    def __init__(self):
        self._servers: List[dict] = []

    def add_radius_server(self, ip: str, key: str, port: int = 1812):
        self._servers.append({
            "type": "radius", "ip": ip, "key": key, "port": port,
        })

    def add_tacacs_server(self, ip: str, key: str, port: int = 49):
        self._servers.append({
            "type": "tacacs", "ip": ip, "key": key, "port": port,
        })

    def generate_config(self) -> str:
        lines = ["# AAA Configuration"]
        for server in self._servers:
            if server["type"] == "radius":
                lines.append(f"radius-server host {server['ip']} auth-port {server['port']} key {server['key']}")
            elif server["type"] == "tacacs":
                lines.append(f"tacacs-server host {server['ip']} port {server['port']} key {server['key']}")
        lines.append("aaa new-model")
        lines.append("aaa authentication login default group radius local")
        return "\n".join(lines)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| No connectivity | Can't reach remote host | Check interface status, routing table |
| Intermittent drops | Packet loss | Check cables, duplex mismatch, buffers |
| Slow performance | High latency | Check MTU, QoS, interface errors |
| VLAN not working | Cross-VLAN routing fails | Verify trunking, inter-VLAN routing |
| DHCP failure | No IP assigned | Check DHCP server, relay agent |
| DNS resolution fail | Can't resolve names | Check DNS server config, connectivity |
| OSPF not forming | Neighbor not established | Verify area, hello/dead timers, auth |
| BGP not peering | Session inactive | Check ASN, neighbor IP, filters |

### Network Diagnostics

```python
class NetworkDiagnostics:
    def __init__(self):
        self._results: Dict[str, dict] = {}

    def ping_test(self, target: str, count: int = 10) -> dict:
        import subprocess
        try:
            result = subprocess.run(
                ["ping", "-n", str(count), target],
                capture_output=True, text=True, timeout=count * 2
            )
            return {"success": result.returncode == 0, "output": result.stdout}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def traceroute(self, target: str, max_hops: int = 30) -> dict:
        import subprocess
        try:
            result = subprocess.run(
                ["tracert", "-d", "-h", str(max_hops), target],
                capture_output=True, text=True, timeout=60
            )
            return {"success": result.returncode == 0, "hops": result.stdout}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def port_check(self, host: str, port: int, timeout: float = 5.0) -> dict:
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return {"open": result == 0, "port": port}
        except Exception as e:
            return {"open": False, "error": str(e)}

    def dns_lookup(self, hostname: str) -> dict:
        import socket
        try:
            ip = socket.gethostbyname(hostname)
            return {"hostname": hostname, "ip": ip}
        except Exception as e:
            return {"hostname": hostname, "error": str(e)}
```

## API Reference

### Core Classes

| Class | Constructor | Key Methods |
|-------|-------------|-------------|
| `SubnetCalculator(network)` | `str` | `get_hosts()`, `get_subnets()`, `get_first_host()`, `get_last_host()` |
| `NetworkMonitor()` | none | `record_latency()`, `get_stats()` |
| `DNSZoneManager(domain, ttl)` | `str, int` | `add_a_record()`, `add_cname()`, `add_mx()`, `generate_zone_file()` |
| `FirewallRuleManager()` | none | `add_rule()`, `remove_rule()`, `generate_iptables()` |
| `VlanManager()` | none | `create_vlan()`, `assign_port()`, `get_vlan_summary()` |
| `RouterConfig(config)` | `NetworkConfig` | `configure_interface()`, `add_static_route()`, `generate_config()` |
| `WireGuardConfig(name)` | `str` | `set_interface()`, `add_peer()`, `generate_config()` |
| `NatManager()` | none | `add_source_nat()`, `add_destination_nat()`, `generate_iptables()` |
| `QosManager()` | none | `define_class()`, `assign_traffic()`, `generate_config()` |
| `NetworkDiagnostics()` | none | `ping_test()`, `traceroute()`, `port_check()`, `dns_lookup()` |

## Data Models

### Interface Schema

```json
{
  "interface": {
    "name": "string",
    "ip": "string",
    "mask": "string",
    "description": "string",
    "vlan": "int",
    "status": "up|down",
    "speed": "string",
    "duplex": "auto|full|half"
  }
}
```

### Route Schema

```json
{
  "route": {
    "type": "static|ospf|bgp|connected",
    "destination": "string",
    "gateway": "string",
    "metric": "int",
    "admin_distance": "int",
    "interface": "string"
  }
}
```

## Deployment Guide

### Ansible Role Structure

```
roles/
├── network_base/
│   ├── tasks/main.yml
│   ├── templates/ios_config.j2
│   └── defaults/main.yml
├── firewall/
│   ├── tasks/main.yml
│   └── templates/iptables.j2
└── vpn/
    ├── tasks/main.yml
    └── templates/wireguard.j2
```

### Docker Network Setup

```yaml
version: '3.8'
services:
  router:
    image: network-router:latest
    networks:
      - frontend
      - backend
    cap_add:
      - NET_ADMIN

networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.1.0/24
  backend:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 10.0.2.0/24
```

## Monitoring and Observability

### Network Metrics

```python
@dataclass
class NetworkMetrics:
    interfaces_up: int = 0
    interfaces_down: int = 0
    total_routes: int = 0
    avg_latency_ms: float = 0.0
    packet_loss_percent: float = 0.0
    bandwidth_utilization: float = 0.0

    def get_dashboard(self) -> dict:
        return {
            "interfaces": f"{self.interfaces_up} up / {self.interfaces_down} down",
            "routes": self.total_routes,
            "latency": f"{self.avg_latency_ms:.1f}ms",
            "packet_loss": f"{self.packet_loss_percent:.2%}",
            "bandwidth": f"{self.bandwidth_utilization:.1%}",
        }
```

## Testing Strategy

### Network Connectivity Tests

```python
class NetworkTestSuite:
    def __init__(self):
        self._tests: List[dict] = []

    def add_connectivity_test(self, source: str, destination: str):
        self._tests.append({"type": "connectivity", "source": source, "dest": destination})

    def add_latency_test(self, source: str, destination: str, threshold_ms: float = 100):
        self._tests.append({"type": "latency", "source": source, "dest": destination, "threshold": threshold_ms})

    def run_all(self) -> List[dict]:
        results = []
        diagnostics = NetworkDiagnostics()
        for test in self._tests:
            if test["type"] == "connectivity":
                result = diagnostics.ping_test(test["dest"])
                results.append({"test": test, "result": result})
            elif test["type"] == "latency":
                result = diagnostics.ping_test(test["dest"], count=5)
                results.append({"test": test, "result": result})
        return results
```

## Versioning and Migration

| Version | Changes |
|---------|---------|
| 2.0.0 | VPN config, NAT management, QoS, security hardening |
| 1.5.0 | VLAN management, subnet calculator |
| 1.0.0 | Initial release with basic routing and firewall |

## Glossary

| Term | Definition |
|------|-----------|
| **VLAN** | Virtual Local Area Network - logical network segmentation |
| **OSPF** | Open Shortest Path First - link-state routing protocol |
| **BGP** | Border Gateway Protocol - path-vector routing protocol |
| **NAT** | Network Address Translation - IP address mapping |
| **ACL** | Access Control List - traffic filtering rules |
| **MTU** | Maximum Transmission Unit - largest packet size |
| **QoS** | Quality of Service - traffic prioritization |
| **CIDR** | Classless Inter-Domain Routing - flexible IP allocation |
| **VLSM** | Variable Length Subnet Masking - efficient subnetting |
| **STP** | Spanning Tree Protocol - loop prevention |

## Changelog

- **2.0.0** - VPN, NAT, QoS, security hardening
- **1.5.0** - VLAN management, subnet calculator
- **1.2.0** - Added firewall rule management
- **1.1.0** - Enhanced monitoring capabilities
- **1.0.0** - Initial release

## Contributing Guidelines

1. Test configurations in lab environment first
2. Verify routing table consistency
3. Document all network changes
4. Follow security best practices

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
