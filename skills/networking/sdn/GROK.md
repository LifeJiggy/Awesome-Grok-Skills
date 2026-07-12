---
name: sdn
category: networking
version: 2.0.0
tags: [networking, sdn, openflow, controllers, network-virtualization]
---

# Software-Defined Networking (SDN)

## Overview

Software-Defined Networking toolkit covering SDN architecture, OpenFlow protocol implementation, network controller management, flow table programming, and network virtualization. This skill provides SDN controller configurations, flow rule management, network topology discovery, and programmable data plane concepts for modern network infrastructure.

## Core Capabilities

- **SDN Architecture**: Control plane / data plane separation, controller southbound/northbound APIs
- **OpenFlow**: Flow table entries, match fields, action sets, group tables, meter tables
- **Controller Management**: ONOS, OpenDaylight, Floodlight configuration and management
- **Flow Programming**: Add/delete/modify flow rules with match criteria and actions
- **Topology Discovery**: LLDP-based discovery, shortest path computation, link-state management
- **Network Slicing**: Virtual network isolation with overlapping physical infrastructure
- **Load Balancing**: SDN-based dynamic load distribution across paths
- **Policy Enforcement**: ACL-based traffic filtering and QoS enforcement

## Usage Examples

```python
import json
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
from collections import defaultdict

class FlowAction(Enum):
    FORWARD = "forward"
    DROP = "drop"
    CONTROLLER = "controller"
    SET_VLAN = "set_vlan"
    STRIP_VLAN = "strip_vlan"
    SET_QOS = "set_qos"

class FlowPriority(Enum):
    LOW = 100
    NORMAL = 300
    HIGH = 500
    CRITICAL = 1000

@dataclass
class FlowEntry:
    cookie: int = 0
    priority: int = 300
    match: Dict = field(default_factory=dict)
    actions: List[Dict] = field(default_factory=list)
    idle_timeout: int = 300
    hard_timeout: int = 0
    table_id: int = 0

    def to_openflow(self) -> Dict:
        return {
            "cookie": self.cookie,
            "priority": self.priority,
            "match": self.match,
            "actions": self.actions,
            "idle_timeout": self.idle_timeout,
            "hard_timeout": self.hard_timeout,
            "table_id": self.table_id,
        }

    @property
    def flow_id(self) -> str:
        match_str = json.dumps(self.match, sort_keys=True)
        return hashlib.md5(match_str.encode()).hexdigest()[:12]

@dataclass
class Switch:
    dpid: str
    name: str
    ports: List[Dict] = field(default_factory=list)
    is_connected: bool = True
    controller_ip: str = ""

@dataclass
class Link:
    src_switch: str
    src_port: int
    dst_switch: str
    dst_port: int
    bandwidth_mbps: float = 1000.0
    latency_ms: float = 1.0
    is_up: bool = True

class FlowTableManager:
    def __init__(self):
        self._tables: Dict[str, List[FlowEntry]] = {}

    def add_flow(self, dpid: str, flow: FlowEntry) -> str:
        if dpid not in self._tables:
            self._tables[dpid] = []
        self._tables[dpid].append(flow)
        return flow.flow_id

    def remove_flow(self, dpid: str, flow_id: str):
        if dpid in self._tables:
            self._tables[dpid] = [f for f in self._tables[dpid] if f.flow_id != flow_id]

    def get_flows(self, dpid: str) -> List[FlowEntry]:
        return self._tables.get(dpid, [])

    def clear_flows(self, dpid: str):
        self._tables[dpid] = []

    def match_flows(self, dpid: str, match_criteria: Dict) -> List[FlowEntry]:
        flows = self._tables.get(dpid, [])
        matches = []
        for flow in flows:
            if all(flow.match.get(k) == v for k, v in match_criteria.items()):
                matches.append(flow)
        return sorted(matches, key=lambda f: f.priority, reverse=True)

    def to_json(self) -> str:
        result = {}
        for dpid, flows in self._tables.items():
            result[dpid] = [f.to_openflow() for f in flows]
        return json.dumps(result, indent=2)

class TopologyManager:
    def __init__(self):
        self._switches: Dict[str, Switch] = {}
        self._links: List[Link] = []
        self._adjacency: Dict[str, List[Tuple[str, int, int]]] = defaultdict(list)

    def add_switch(self, switch: Switch):
        self._switches[switch.dpid] = switch

    def add_link(self, link: Link):
        self._links.append(link)
        self._adjacency[link.src_switch].append((link.dst_switch, link.src_port, link.dst_port))
        self._adjacency[link.dst_switch].append((link.dst_switch, link.src_port, link.src_port))

    def shortest_path(self, src: str, dst: str) -> Optional[List[str]]:
        if src == dst:
            return [src]
        visited: Set[str] = {src}
        queue = [(src, [src])]
        while queue:
            current, path = queue.pop(0)
            for neighbor, _, _ in self._adjacency.get(current, []):
                if neighbor == dst:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def get_all_paths(self, src: str, dst: str, max_paths: int = 5) -> List[List[str]]:
        paths: List[List[str]] = []
        self._dfs_paths(src, dst, [src], set(), paths, max_paths)
        return paths

    def _dfs_paths(self, current: str, dst: str, path: List[str],
                   visited: Set[str], all_paths: List, limit: int):
        if len(all_paths) >= limit:
            return
        if current == dst and len(path) > 1:
            all_paths.append(list(path))
            return
        for neighbor, _, _ in self._adjacency.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                self._dfs_paths(neighbor, dst, path, visited, all_paths, limit)
                path.pop()
                visited.discard(neighbor)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "switches": len(self._switches),
            "links": len(self._links),
            "active_links": sum(1 for l in self._links if l.is_up),
            "total_bandwidth": sum(l.bandwidth_mbps for l in self._links if l.is_up),
        }

class SdnController:
    def __init__(self, name: str, ip: str = "0.0.0.0", port: int = 6633):
        self.name = name
        self.ip = ip
        self.port = port
        self.flow_table = FlowTableManager()
        self.topology = TopologyManager()
        self._connected_switches: Dict[str, Switch] = {}

    def connect_switch(self, switch: Switch):
        self._connected_switches[switch.dpid] = switch
        self.topology.add_switch(switch)

    def install_flow(self, dpid: str, match: Dict, actions: List[Dict],
                     priority: int = 300) -> str:
        flow = FlowEntry(match=match, actions=actions, priority=priority)
        return self.flow_table.add_flow(dpid, flow)

    def install_shortest_path(self, src_dpid: str, dst_dpid: str, src_port: int = 1, dst_port: int = 1) -> bool:
        path = self.topology.shortest_path(src_dpid, dst_dpid)
        if not path:
            return False
        for i in range(len(path) - 1):
            self.install_flow(path[i], {"in_port": src_port}, [{"type": "output", "port": dst_port}], priority=500)
        return True

    def block_traffic(self, dpid: str, src_ip: str, dst_ip: str) -> str:
        return self.install_flow(dpid, {"src_ip": src_ip, "dst_ip": dst_ip}, [{"type": "drop"}], priority=1000)

    def get_status(self) -> Dict[str, Any]:
        return {
            "controller": self.name,
            "ip": self.ip,
            "port": self.port,
            "connected_switches": len(self._connected_switches),
            "topology": self.topology.get_summary(),
        }
```

## Best Practices

- Use OpenFlow priority levels to prevent rule conflicts and ensure correct matching
- Implement flow timeout policies to prevent table overflow in large networks
- Use topology discovery for real-time path computation and failover
- Separate production traffic flows from management flows with different priorities
- Monitor flow table sizes across switches to prevent TCAM exhaustion
- Use group tables for multicast and load-balanced forwarding
- Implement SDN controller redundancy for high availability
- Use network slicing to isolate tenant traffic in multi-tenant environments
- Regularly audit flow rules to remove stale entries
- Use southbound APIs (OpenFlow, NETCONF) and northbound APIs (REST) consistently

## Related Modules

- `network-engineering` - Traditional network infrastructure
- `load-balancing` - Traffic distribution algorithms
- `dns-management` - DNS infrastructure management
- `traffic-analysis` - Network traffic analysis
