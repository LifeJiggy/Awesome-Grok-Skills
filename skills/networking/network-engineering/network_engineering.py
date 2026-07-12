"""
Network Engineering Module
Part of the networking skill domain.

Network engineering utilities: subnet calculation, VLAN management, firewall rules,
DNS zone management, VPN configuration, and network monitoring.
"""

from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ANY = "any"


class FirewallAction(Enum):
    ALLOW = "ACCEPT"
    DENY = "DROP"
    REJECT = "REJECT"


class NatType(Enum):
    SNAT = "SNAT"
    DNAT = "DNAT"
    MASQUERADE = "MASQUERADE"


class VpnType(Enum):
    WIREGUARD = "wireguard"
    OPENVPN = "openvpn"
    IPSec = "ipsec"


@dataclass
class FirewallRule:
    name: str
    action: FirewallAction
    protocol: Protocol
    source: str
    destination: str
    ports: List[int] = field(default_factory=list)
    direction: str = "inbound"
    enabled: bool = True
    logging: bool = False
    priority: int = 100

    def to_iptables(self) -> str:
        chain = "INPUT" if self.direction == "inbound" else "OUTPUT"
        proto = f"-p {self.protocol.value}" if self.protocol != Protocol.ANY else ""
        ports = f"--dport {','.join(map(str, self.ports))}" if self.ports else ""
        log_flag = "-j LOG --log-prefix 'RULE_DROP: '" if self.logging else ""
        return (f"iptables -A {chain} -s {self.source} -d {self.destination} "
                f"{proto} {ports} -j {self.action.value}" +
                (f" {log_flag}" if self.logging else ""))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name, "action": self.action.value,
            "protocol": self.protocol.value, "source": self.source,
            "destination": self.destination, "ports": self.ports,
            "direction": self.direction, "enabled": self.enabled,
        }


@dataclass
class NatRule:
    name: str
    nat_type: NatType
    protocol: Protocol
    source: str = ""
    destination: str = ""
    original_port: int = 0
    translated_port: int = 0
    translated_ip: str = ""

    def to_iptables(self) -> str:
        proto = f"-p {self.protocol.value}"
        src = f"-s {self.source}" if self.source else ""
        dst = f"-d {self.destination}" if self.destination else ""
        sport = f"--sport {self.original_port}" if self.original_port else ""
        dport = f"--dport {self.translated_port}" if self.translated_port else ""
        target = f"--to {self.translated_ip}:{self.original_port}" if self.translated_ip else ""
        return f"iptables -t nat -A PREROUTING {src} {dst} {proto} {sport} {dport} -j {self.nat_type.value} {target}"


class SubnetCalculator:
    def __init__(self, network: str):
        self.network = ipaddress.ip_network(network, strict=False)

    @property
    def cidr(self) -> str:
        return f"{self.network.network_address}/{self.network.prefixlen}"

    @property
    def total_hosts(self) -> int:
        return self.network.num_addresses - 2

    @property
    def first_host(self) -> str:
        return str(self.network.network_address + 1)

    @property
    def last_host(self) -> str:
        return str(self.network.broadcast_address - 1)

    @property
    def broadcast(self) -> str:
        return str(self.network.broadcast_address)

    @property
    def netmask(self) -> str:
        return str(self.network.netmask)

    def subnet(self, new_prefix: int) -> List[str]:
        return [str(s) for s in self.network.subnets(new_prefix=new_prefix)]

    def supernet(self, target_prefix: int) -> str:
        return str(self.network.supernet(new_prefix=target_prefix))

    def contains(self, ip: str) -> bool:
        return ipaddress.ip_address(ip) in self.network

    def summarize(self) -> Dict[str, Any]:
        return {
            "network": self.cidr,
            "netmask": self.netmask,
            "broadcast": self.broadcast,
            "first_host": self.first_host,
            "last_host": self.last_host,
            "total_hosts": self.total_hosts,
            "prefix_length": self.network.prefixlen,
        }

    @staticmethod
    def vlsm(network: str, subnets: List[int]) -> List[Dict[str, Any]]:
        net = ipaddress.ip_network(network, strict=False)
        current_ip = int(net.network_address)
        results = []

        for size in sorted(subnets, reverse=True):
            needed = size + 2
            prefix = 32
            while (1 << (32 - prefix)) < needed:
                prefix -= 1
            subnet = ipaddress.ip_network(f"{ipaddress.ip_address(current_ip)}/{prefix}", strict=False)
            results.append({
                "network": str(subnet),
                "hosts": subnet.num_addresses - 2,
                "first_host": str(subnet.network_address + 1),
                "last_host": str(subnet.broadcast_address - 1),
            })
            current_ip = int(subnet.broadcast_address) + 1

        return results


class VlanManager:
    def __init__(self):
        self._vlans: Dict[int, Dict[str, Any]] = {}
        self._ports: Dict[str, Dict[str, Any]] = {}

    def create_vlan(self, vlan_id: int, name: str, subnet: Optional[str] = None):
        self._vlans[vlan_id] = {"name": name, "subnet": subnet, "ports": []}

    def assign_port(self, port: str, vlan_id: int, tagged: bool = False):
        if vlan_id not in self._vlans:
            raise ValueError(f"VLAN {vlan_id} does not exist")
        self._ports[port] = {"vlan_id": vlan_id, "tagged": tagged}
        self._vlans[vlan_id]["ports"].append(port)

    def get_vlan_config(self) -> str:
        lines = ["! VLAN Configuration"]
        for vid, vinfo in self._vlans.items():
            lines.append(f"vlan {vid}")
            lines.append(f" name {vinfo['name']}")
        lines.append("")
        lines.append("! Port Assignments")
        for port, pinfo in self._ports.items():
            mode = "trunk" if pinfo["tagged"] else "access"
            lines.append(f"interface {port}")
            lines.append(f" switchport mode {mode}")
            if not pinfo["tagged"]:
                lines.append(f" switchport access vlan {pinfo['vlan_id']}")
            else:
                lines.append(f" switchport trunk allowed vlan {pinfo['vlan_id']}")
        return "\n".join(lines)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "vlans": {vid: {"name": v["name"], "subnet": v["subnet"], "port_count": len(v["ports"])}
                      for vid, v in self._vlans.items()},
            "total_ports": len(self._ports),
        }


class DnsZoneManager:
    def __init__(self, domain: str, ttl: int = 3600):
        self.domain = domain
        self.ttl = ttl
        self.records: List[Dict[str, Any]] = []

    def add_a(self, name: str, ip: str, ttl: Optional[int] = None):
        fqdn = f"{name}.{self.domain}" if name != "@" else self.domain
        self.records.append({"type": "A", "name": fqdn, "ip": ip, "ttl": ttl or self.ttl})

    def add_aaaa(self, name: str, ipv6: str, ttl: Optional[int] = None):
        fqdn = f"{name}.{self.domain}" if name != "@" else self.domain
        self.records.append({"type": "AAAA", "name": fqdn, "ipv6": ipv6, "ttl": ttl or self.ttl})

    def add_cname(self, name: str, target: str, ttl: Optional[int] = None):
        fqdn = f"{name}.{self.domain}"
        self.records.append({"type": "CNAME", "name": fqdn, "target": target, "ttl": ttl or self.ttl})

    def add_mx(self, mail_server: str, priority: int = 10, ttl: Optional[int] = None):
        self.records.append({"type": "MX", "name": self.domain, "mail_server": mail_server, "priority": priority, "ttl": ttl or self.ttl})

    def add_txt(self, name: str, value: str, ttl: Optional[int] = None):
        fqdn = f"{name}.{self.domain}" if name != "@" else self.domain
        self.records.append({"type": "TXT", "name": fqdn, "value": value, "ttl": ttl or self.ttl})

    def generate_zone_file(self) -> str:
        lines = [
            f"; Zone file for {self.domain}",
            f"$TTL {self.ttl}",
            f"@ IN SOA ns1.{self.domain}. admin.{self.domain}. (",
            "    2024010101 ; Serial",
            "    3600       ; Refresh",
            "    900        ; Retry",
            "    604800     ; Expire",
            "    86400      ; Minimum TTL",
            ")",
            "",
        ]
        for rec in self.records:
            if rec["type"] == "A":
                lines.append(f'{rec["name"]} IN A {rec["ip"]}')
            elif rec["type"] == "AAAA":
                lines.append(f'{rec["name"]} IN AAAA {rec["ipv6"]}')
            elif rec["type"] == "CNAME":
                lines.append(f'{rec["name"]} IN CNAME {rec["target"]}')
            elif rec["type"] == "MX":
                lines.append(f'{rec["name"]} IN MX {rec["priority"]} {rec["mail_server"]}')
            elif rec["type"] == "TXT":
                lines.append(f'{rec["name"]} IN TXT "{rec["value"]}"')
        return "\n".join(lines)


class NetworkMonitor:
    def __init__(self):
        self._latencies: Dict[str, List[float]] = {}
        self._bandwidth: Dict[str, List[Tuple[float, float]]] = {}

    def record_latency(self, host: str, latency_ms: float):
        if host not in self._latencies:
            self._latencies[host] = []
        self._latencies[host].append(latency_ms)
        if len(self._latencies[host]) > 10000:
            self._latencies[host] = self._latencies[host][-10000:]

    def record_bandwidth(self, host: str, upload_mbps: float, download_mbps: float):
        if host not in self._bandwidth:
            self._bandwidth[host] = []
        self._bandwidth[host].append((upload_mbps, download_mbps))
        if len(self._bandwidth[host]) > 1000:
            self._bandwidth[host] = self._bandwidth[host][-1000:]

    def get_latency_stats(self, host: str) -> Dict[str, Any]:
        data = self._latencies.get(host, [])
        if not data:
            return {"host": host, "samples": 0}
        return {
            "host": host,
            "samples": len(data),
            "avg_ms": round(sum(data) / len(data), 2),
            "min_ms": round(min(data), 2),
            "max_ms": round(max(data), 2),
            "p95_ms": round(sorted(data)[int(len(data) * 0.95)], 2),
            "jitter_ms": round(max(data) - min(data), 2),
        }

    def get_bandwidth_stats(self, host: str) -> Dict[str, Any]:
        data = self._bandwidth.get(host, [])
        if not data:
            return {"host": host, "samples": 0}
        uploads = [d[0] for d in data]
        downloads = [d[1] for d in data]
        return {
            "host": host,
            "samples": len(data),
            "avg_upload_mbps": round(sum(uploads) / len(uploads), 2),
            "avg_download_mbps": round(sum(downloads) / len(downloads), 2),
            "max_upload_mbps": round(max(uploads), 2),
            "max_download_mbps": round(max(downloads), 2),
        }

    def get_all_stats(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for host in set(list(self._latencies.keys()) + list(self._bandwidth.keys())):
            result[host] = {
                "latency": self.get_latency_stats(host),
                "bandwidth": self.get_bandwidth_stats(host),
            }
        return result


class FirewallManager:
    def __init__(self):
        self._rules: List[FirewallRule] = []
        self._nat_rules: List[NatRule] = []

    def add_rule(self, rule: FirewallRule):
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority)

    def add_nat_rule(self, rule: NatRule):
        self._nat_rules.append(rule)

    def remove_rule(self, name: str):
        self._rules = [r for r in self._rules if r.name != name]

    def generate_iptables_script(self) -> str:
        lines = ["#!/bin/bash", "# Auto-generated iptables rules", "iptables -F", "iptables -X", ""]
        lines.append("# NAT Rules")
        for rule in self._nat_rules:
            lines.append(rule.to_iptables())
        lines.append("")
        lines.append("# Firewall Rules")
        for rule in self._rules:
            if rule.enabled:
                lines.append(f"# {rule.name}")
                lines.append(rule.to_iptables())
        lines.append("")
        lines.append("iptables -P INPUT DROP")
        lines.append("iptables -P FORWARD DROP")
        lines.append("iptables -P OUTPUT ACCEPT")
        return "\n".join(lines)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_rules": len(self._rules),
            "enabled_rules": sum(1 for r in self._rules if r.enabled),
            "nat_rules": len(self._nat_rules),
            "rules": [r.to_dict() for r in self._rules],
        }


def main():
    print("=== Network Engineering Module ===")

    print("\n=== Subnet Calculation ===")
    calc = SubnetCalculator("192.168.1.0/24")
    summary = calc.summarize()
    for k, v in summary.items():
        print(f"  {k}: {v}")

    subnets = calc.subnet(26)
    print(f"  /26 subnets: {subnets[:4]}...")

    print("\n=== VLSM ===")
    vlsm_results = SubnetCalculator.vlsm("10.0.0.0/24", [60, 30, 14, 6])
    for s in vlsm_results:
        print(f"  {s['network']} ({s['hosts']} hosts)")

    print("\n=== VLAN Configuration ===")
    vlan_mgr = VlanManager()
    vlan_mgr.create_vlan(10, "Management", "10.10.0.0/24")
    vlan_mgr.create_vlan(20, "Production", "10.20.0.0/24")
    vlan_mgr.assign_port("Gi0/1", 10, tagged=False)
    vlan_mgr.assign_port("Gi0/2", 20, tagged=False)
    vlan_mgr.assign_port("Gi0/24", 10, tagged=True)
    print(vlan_mgr.get_vlan_config())

    print("\n=== DNS Zone ===")
    dns = DnsZoneManager("example.com")
    dns.add_a("@", "93.184.216.34")
    dns.add_a("www", "93.184.216.34")
    dns.add_cname("api", "lb.example.com")
    dns.add_mx("mx1.example.com", priority=10)
    dns.add_txt("@", "v=spf1 include:_spf.example.com ~all")
    print(dns.generate_zone_file())

    print("\n=== Firewall Rules ===")
    fw = FirewallManager()
    fw.add_rule(FirewallRule("allow-ssh", FirewallAction.ALLOW, Protocol.TCP, "0.0.0.0/0", "10.0.0.1", [22]))
    fw.add_rule(FirewallRule("allow-http", FirewallAction.ALLOW, Protocol.TCP, "0.0.0.0/0", "10.0.0.1", [80, 443]))
    fw.add_rule(FirewallRule("deny-all", FirewallAction.DENY, Protocol.ANY, "0.0.0.0/0", "0.0.0.0/0", priority=999))
    print(fw.generate_iptables_script())

    print("\n=== Network Monitor ===")
    import random
    monitor = NetworkMonitor()
    for _ in range(100):
        monitor.record_latency("10.0.1.1", random.uniform(5, 50))
        monitor.record_bandwidth("10.0.1.1", random.uniform(10, 100), random.uniform(50, 500))
    print(json.dumps(monitor.get_latency_stats("10.0.1.1"), indent=2))

    print("\nDone.")


if __name__ == "__main__":
    main()
