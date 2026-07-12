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
