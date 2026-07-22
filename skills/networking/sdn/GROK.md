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

## Advanced Configuration

### SDN Controller Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `openflow_version` | 1.3 | 1.0 - 1.5 | OpenFlow protocol version |
| `max_flow_rules` | 10000 | 1000 - 100000 | Maximum flow table entries |
| `controller_threads` | 4 | 1 - 32 | Controller processing threads |
| `topology_poll_interval` | 10s | 1 - 60s | Topology discovery interval |
| `flow_idle_timeout` | 300s | 30 - 3600s | Idle flow removal timeout |
| `packet_in_rate_limit` | 1000 | 100 - 10000 | Packet-in messages per second |

### Advanced SDN Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
from collections import defaultdict
import json
import hashlib
import time

class OpenFlowVersion(Enum):
    OF_10 = "1.0"
    OF_13 = "1.3"
    OF_15 = "1.5"

class ControllerMode(Enum):
    CENTRALIZED = "centralized"
    DISTRIBUTED = "distributed"
    HIERARCHICAL = "hierarchical"

@dataclass
class SdnConfig:
    controller_mode: ControllerMode = ControllerMode.CENTRALIZED
    openflow_version: OpenFlowVersion = OpenFlowVersion.OF_13
    max_flow_rules: int = 10000
    controller_threads: int = 4
    topology_poll_interval: int = 10
    flow_idle_timeout: int = 300
    packet_in_rate_limit: int = 1000
    enable_ssl: bool = True
    enable_auth: bool = True
    log_level: str = "INFO"

class OpenFlowController:
    def __init__(self, config: SdnConfig = None):
        self.config = config or SdnConfig()
        self._switches: Dict[str, dict] = {}
        self._flow_tables: Dict[str, List[dict]] = {}
        self._topology: Dict[str, List[Tuple[str, int, int]]] = defaultdict(list)
        self._packet_count = 0
        self._last_packet_time = time.time()

    def register_switch(self, dpid: str, datapath_id: int, features: dict):
        self._switches[dpid] = {
            "datapath_id": datapath_id,
            "features": features,
            "connected_at": time.time(),
            "flow_count": 0,
        }
        self._flow_tables[dpid] = []

    def install_flow(self, dpid: str, match: dict, actions: List[dict],
                     priority: int = 300, idle_timeout: int = None,
                     hard_timeout: int = None) -> str:
        if len(self._flow_tables.get(dpid, [])) >= self.config.max_flow_rules:
            raise RuntimeError(f"Flow table full for switch {dpid}")
        flow = {
            "cookie": hashlib.md5(json.dumps(match, sort_keys=True).encode()).hexdigest()[:8],
            "priority": priority,
            "match": match,
            "actions": actions,
            "idle_timeout": idle_timeout or self.config.flow_idle_timeout,
            "hard_timeout": hard_timeout or 0,
            "created_at": time.time(),
            "packet_count": 0,
            "byte_count": 0,
        }
        self._flow_tables.setdefault(dpid, []).append(flow)
        self._switches[dpid]["flow_count"] = len(self._flow_tables[dpid])
        return flow["cookie"]

    def remove_flow(self, dpid: str, cookie: str):
        if dpid in self._flow_tables:
            self._flow_tables[dpid] = [f for f in self._flow_tables[dpid] if f["cookie"] != cookie]
            self._switches[dpid]["flow_count"] = len(self._flow_tables[dpid])

    def add_link(self, src_dpid: str, src_port: int, dst_dpid: str, dst_port: int,
                 bandwidth_mbps: float = 1000.0, latency_ms: float = 1.0):
        self._topology[src_dpid].append((dst_dpid, src_port, dst_port))
        self._topology[dst_dpid].append((src_dpid, dst_port, src_port))

    def shortest_path(self, src: str, dst: str) -> Optional[List[str]]:
        if src == dst:
            return [src]
        visited: Set[str] = {src}
        queue = [(src, [src])]
        while queue:
            current, path = queue.pop(0)
            for neighbor, _, _ in self._topology.get(current, []):
                if neighbor == dst:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def install_path_flow(self, src: str, dst: str, src_port: int = 1,
                          dst_port: int = 1) -> bool:
        path = self.shortest_path(src, dst)
        if not path:
            return False
        for i in range(len(path) - 1):
            self.install_flow(
                path[i],
                match={"in_port": src_port},
                actions=[{"type": "output", "port": dst_port}],
                priority=500,
            )
        return True

    def block_ip(self, dpid: str, src_ip: str, dst_ip: str = None) -> str:
        match = {"src_ip": src_ip}
        if dst_ip:
            match["dst_ip"] = dst_ip
        return self.install_flow(dpid, match, [{"type": "drop"}], priority=1000)

    def get_switch_stats(self, dpid: str) -> dict:
        switch = self._switches.get(dpid, {})
        flows = self._flow_tables.get(dpid, [])
        return {
            "dpid": dpid,
            "datapath_id": switch.get("datapath_id"),
            "connected_at": switch.get("connected_at"),
            "flow_count": len(flows),
            "high_priority_flows": sum(1 for f in flows if f["priority"] >= 500),
        }

    def get_topology_summary(self) -> dict:
        total_links = sum(len(links) for links in self._topology.values())
        return {
            "switches": len(self._switches),
            "links": total_links // 2,
            "total_flows": sum(len(flows) for flows in self._flow_tables.values()),
        }

    def handle_packet_in(self, dpid: str, in_port: int, packet_data: bytes) -> dict:
        self._packet_count += 1
        now = time.time()
        if now - self._last_packet_time > 1:
            rate = self._packet_count / (now - self._last_packet_time)
            if rate > self.config.packet_in_rate_limit:
                return {"action": "drop", "reason": "rate_limit"}
            self._packet_count = 0
            self._last_packet_time = now
        return {"action": "flood"}
```

### Flow Table Manager

```python
class FlowTableManager:
    def __init__(self, max_entries: int = 10000):
        self.max_entries = max_entries
        self._tables: Dict[str, List[dict]] = {}

    def add_flow(self, dpid: str, flow: dict) -> bool:
        if len(self._tables.get(dpid, [])) >= self.max_entries:
            return False
        self._tables.setdefault(dpid, []).append(flow)
        return True

    def remove_flows_by_match(self, dpid: str, match_criteria: dict) -> int:
        if dpid not in self._tables:
            return 0
        original_count = len(self._tables[dpid])
        self._tables[dpid] = [
            f for f in self._tables[dpid]
            if not all(f.get("match", {}).get(k) == v for k, v in match_criteria.items())
        ]
        return original_count - len(self._tables[dpid])

    def get_table_stats(self, dpid: str) -> dict:
        flows = self._tables.get(dpid, [])
        return {
            "total_entries": len(flows),
            "capacity": self.max_entries,
            "utilization": len(flows) / self.max_entries if self.max_entries > 0 else 0,
            "priority_distribution": self._priority_distribution(flows),
        }

    def _priority_distribution(self, flows: List[dict]) -> Dict[str, int]:
        dist = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for f in flows:
            p = f.get("priority", 0)
            if p < 200:
                dist["low"] += 1
            elif p < 400:
                dist["medium"] += 1
            elif p < 800:
                dist["high"] += 1
            else:
                dist["critical"] += 1
        return dist

    def export_json(self) -> str:
        return json.dumps(self._tables, indent=2)
```

### Network Slicing

```python
class NetworkSlice:
    def __init__(self, slice_id: str, name: str):
        self.slice_id = slice_id
        self.name = name
        self._switches: Set[str] = set()
        self._flows: List[dict] = []
        self._bandwidth_mbps: float = 0
        self._sla: dict = {}

    def add_switch(self, dpid: str):
        self._switches.add(dpid)

    def add_flow(self, flow: dict):
        flow["slice_id"] = self.slice_id
        self._flows.append(flow)

    def set_sla(self, max_latency_ms: float, min_bandwidth_mbps: float,
                max_packet_loss: float):
        self._sla = {
            "max_latency_ms": max_latency_ms,
            "min_bandwidth_mbps": min_bandwidth_mbps,
            "max_packet_loss": max_packet_loss,
        }

    def get_info(self) -> dict:
        return {
            "slice_id": self.slice_id,
            "name": self.name,
            "switches": len(self._switches),
            "flows": len(self._flows),
            "sla": self._sla,
        }

class NetworkSlicingManager:
    def __init__(self):
        self._slices: Dict[str, NetworkSlice] = {}

    def create_slice(self, slice_id: str, name: str) -> NetworkSlice:
        slice_obj = NetworkSlice(slice_id, name)
        self._slices[slice_id] = slice_obj
        return slice_obj

    def delete_slice(self, slice_id: str):
        self._slices.pop(slice_id, None)

    def get_slice(self, slice_id: str) -> Optional[NetworkSlice]:
        return self._slices.get(slice_id)

    def list_slices(self) -> List[dict]:
        return [s.get_info() for s in self._slices.values()]

    def allocate_bandwidth(self, slice_id: str, bandwidth_mbps: float):
        if slice_id in self._slices:
            self._slices[slice_id]._bandwidth_mbps = bandwidth_mbps
```

## Architecture Patterns

### SDN Architecture Layers

```
┌─────────────────────────────────────────────────┐
│              Application Layer                    │
│    (Network apps, policy engines, monitoring)     │
└──────────────────────┬──────────────────────────┘
                       │ Northbound API (REST)
┌──────────────────────┴──────────────────────────┐
│              Control Layer                        │
│    (Controller, topology, routing logic)           │
└──────────────────────┬──────────────────────────┘
                       │ Southbound API (OpenFlow)
┌──────────────────────┴──────────────────────────┐
│              Infrastructure Layer                 │
│    (Switches, routers, physical network)          │
└─────────────────────────────────────────────────┘
```

### Distributed Controller Architecture

```python
class DistributedController:
    def __init__(self, controller_id: str, peers: List[str] = None):
        self.controller_id = controller_id
        self.peers = peers or []
        self._state: Dict[str, any] = {}
        self._flow_sync_queue: List[dict] = []

    def sync_state(self, state: dict):
        self._state.update(state)

    def replicate_flow(self, flow: dict, target_controllers: List[str]):
        self._flow_sync_queue.append({
            "flow": flow,
            "targets": target_controllers,
            "timestamp": time.time(),
        })

    def get_sync_status(self) -> dict:
        return {
            "controller_id": self.controller_id,
            "peers": len(self.peers),
            "pending_sync": len(self._flow_sync_queue),
            "state_entries": len(self._state),
        }
```

### Policy Engine

```python
class PolicyEngine:
    def __init__(self):
        self._policies: List[dict] = []

    def add_policy(self, name: str, priority: int, conditions: dict, actions: List[dict]):
        self._policies.append({
            "name": name,
            "priority": priority,
            "conditions": conditions,
            "actions": actions,
            "enabled": True,
        })
        self._policies.sort(key=lambda p: p["priority"], reverse=True)

    def evaluate(self, packet_metadata: dict) -> Optional[List[dict]]:
        for policy in self._policies:
            if not policy["enabled"]:
                continue
            if self._matches(policy["conditions"], packet_metadata):
                return policy["actions"]
        return None

    def _matches(self, conditions: dict, metadata: dict) -> bool:
        return all(metadata.get(k) == v for k, v in conditions.items())

    def list_policies(self) -> List[dict]:
        return [p for p in self._policies if p["enabled"]]
```

## Integration Guide

### REST API Integration

```python
class SdnRestApi:
    def __init__(self, controller_host: str = "localhost", port: int = 8080):
        self.base_url = f"http://{controller_host}:{port}"

    def get_switches(self) -> List[dict]:
        return []  # HTTP GET /switches

    def install_flow(self, dpid: str, flow: dict) -> dict:
        return {}  # HTTP POST /switches/{dpid}/flows

    def get_topology(self) -> dict:
        return {}  # HTTP GET /topology

    def add_host(self, mac: str, ip: str, dpid: str, port: int):
        pass  # HTTP POST /hosts
```

### OpenStack Neutron Integration

```python
class OpenStackIntegration:
    def __init__(self, controller_url: str):
        self.controller_url = controller_url
        self._networks: Dict[str, dict] = {}
        self._ports: Dict[str, dict] = {}

    def create_network(self, name: str, tenant_id: str) -> str:
        import uuid
        network_id = str(uuid.uuid4())
        self._networks[network_id] = {
            "name": name, "tenant_id": tenant_id,
            "status": "ACTIVE", "admin_state_up": True,
        }
        return network_id

    def create_port(self, network_id: str, tenant_id: str) -> str:
        import uuid
        port_id = str(uuid.uuid4())
        self._ports[port_id] = {
            "network_id": network_id, "tenant_id": tenant_id,
            "status": "ACTIVE", "admin_state_up": True,
        }
        return port_id
```

## Performance Optimization

### Flow Table Optimization

| Strategy | Benefit | Tradeoff |
|----------|---------|----------|
| Aggregate flows | Fewer table entries | Less granular control |
| Priority ordering | Faster matching | Complex management |
| Hard timeouts | Auto cleanup | May remove active flows |
| Cookie-based management | Easy bulk operations | Extra metadata storage |
| Pipeline tables | Modular processing | Increased complexity |

### Controller Performance

```python
class ControllerPerformanceMonitor:
    def __init__(self):
        self._metrics: Dict[str, list] = defaultdict(list)

    def record_event(self, event_type: str, duration_ms: float):
        self._metrics[event_type].append(duration_ms)
        if len(self._metrics[event_type]) > 10000:
            self._metrics[event_type] = self._metrics[event_type][-10000:]

    def get_stats(self, event_type: str) -> dict:
        times = self._metrics.get(event_type, [])
        if not times:
            return {"count": 0}
        return {
            "count": len(times),
            "avg_ms": sum(times) / len(times),
            "p95_ms": sorted(times)[int(len(times) * 0.95)],
            "max_ms": max(times),
        }
```

## Security Considerations

### Flow Table Security

```python
class FlowSecurityManager:
    def __init__(self):
        self._audit_log: List[dict] = []

    def validate_flow(self, flow: dict) -> bool:
        actions = flow.get("actions", [])
        for action in actions:
            if action.get("type") == "controller" and flow.get("priority", 0) < 100:
                self._log_audit("suspicious_flow", flow)
                return False
        return True

    def detect_anomaly(self, flows: List[dict]) -> List[dict]:
        anomalies = []
        priority_counts = defaultdict(int)
        for f in flows:
            priority_counts[f.get("priority", 0)] += 1
        for priority, count in priority_counts.items():
            if count > 1000:
                anomalies.append({"type": "high_flow_count", "priority": priority, "count": count})
        return anomalies

    def _log_audit(self, event_type: str, details: dict):
        self._audit_log.append({
            "event": event_type,
            "details": details,
            "timestamp": time.time(),
        })
```

### Controller Authentication

```python
class ControllerAuth:
    def __init__(self):
        self._authorized_switches: Dict[str, str] = {}  # dpid -> certificate
        self._auth_tokens: Dict[str, float] = {}

    def register_switch(self, dpid: str, certificate: str):
        self._authorized_switches[dpid] = certificate

    def authenticate(self, dpid: str, token: str) -> bool:
        if dpid not in self._authorized_switches:
            return False
        return token in self._auth_tokens

    def generate_token(self, dpid: str, valid_seconds: int = 3600) -> str:
        import uuid
        token = str(uuid.uuid4())
        self._auth_tokens[token] = time.time() + valid_seconds
        return token
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Switch disconnect | Controller loses switch | Check network connectivity, restart switch |
| Flow table overflow | New flows rejected | Remove unused flows, increase capacity |
| Packet-in flood | Controller overwhelmed | Rate limit packet-in, install proactive flows |
| Topology stale | Incorrect paths | Force topology poll, check LLDP |
| Flow conflict | Wrong behavior | Check priority ordering, verify match fields |
| Controller crash | Network partition | Deploy redundant controllers |
| SSL handshake fail | Switch can't connect | Verify certificates, check CA trust |
| Latency spike | Slow forwarding | Check controller load, optimize flows |

### Debugging

```python
def debug_sdn_controller(controller: OpenFlowController):
    print("=== SDN Controller Status ===")
    topo = controller.get_topology_summary()
    print(f"Switches: {topo['switches']}")
    print(f"Links: {topo['links']}")
    print(f"Total flows: {topo['total_flows']}")
    for dpid, switch in controller._switches.items():
        print(f"Switch {dpid}: {switch['flow_count']} flows")

def debug_flow_table(manager: FlowTableManager, dpid: str):
    stats = manager.get_table_stats(dpid)
    print(f"=== Flow Table {dpid} ===")
    print(f"Entries: {stats['total_entries']}/{stats['capacity']}")
    print(f"Utilization: {stats['utilization']:.1%}")
    print(f"Priority distribution: {stats['priority_distribution']}")
```

## API Reference

### Core Classes

| Class | Constructor | Key Methods |
|-------|-------------|-------------|
| `OpenFlowController(config)` | `SdnConfig` | `register_switch()`, `install_flow()`, `remove_flow()`, `shortest_path()` |
| `FlowTableManager(max_entries)` | `int` | `add_flow()`, `remove_flows_by_match()`, `get_table_stats()` |
| `NetworkSlice(id, name)` | `str, str` | `add_switch()`, `add_flow()`, `set_sla()` |
| `NetworkSlicingManager()` | none | `create_slice()`, `delete_slice()`, `list_slices()` |
| `PolicyEngine()` | none | `add_policy()`, `evaluate()`, `list_policies()` |
| `ControllerPerformanceMonitor()` | none | `record_event()`, `get_stats()` |
| `FlowSecurityManager()` | none | `validate_flow()`, `detect_anomaly()` |
| `ControllerAuth()` | none | `register_switch()`, `authenticate()`, `generate_token()` |

## Data Models

### Flow Entry Schema

```json
{
  "flow_entry": {
    "cookie": "string",
    "priority": "int",
    "match": {"in_port": "int", "src_mac": "string", "dst_ip": "string"},
    "actions": [{"type": "output", "port": "int"}],
    "idle_timeout": "int",
    "hard_timeout": "int",
    "packet_count": "int",
    "byte_count": "int"
  }
}
```

### Network Slice Schema

```json
{
  "network_slice": {
    "slice_id": "string",
    "name": "string",
    "switches": ["dpid1", "dpid2"],
    "flow_count": "int",
    "sla": {
      "max_latency_ms": "float",
      "min_bandwidth_mbps": "float",
      "max_packet_loss": "float"
    }
  }
}
```

## Deployment Guide

### ONOS Deployment

```yaml
version: '3.8'
services:
  onos:
    image: opennetworking/onos:latest
    ports:
      - "8181:8181"
      - "8101:8101"
      - "6633:6633"
    environment:
      - ONOS_APPS=org.onosproject.openflow,org.onosproject.fwd
    volumes:
      - onos.apache:/root/onos/apache-karaf-4.2.13/instances
```

### Mininet Setup

```python
class MininetTopology:
    def __init__(self):
        self._hosts: List[str] = []
        self._switches: List[str] = []
        self._links: List[Tuple[str, str]] = []

    def add_host(self, name: str):
        self._hosts.append(name)

    def add_switch(self, name: str):
        self._switches.append(name)

    def add_link(self, node1: str, node2: str):
        self._links.append((node1, node2))

    def generate_script(self) -> str:
        lines = ["from mininet.net import Mininet", "from mininet.topo import Topo"]
        lines.append("topo = Topo()")
        for h in self._hosts:
            lines.append(f"topo.addHost('{h}')")
        for s in self._switches:
            lines.append(f"topo.addSwitch('{s}')")
        for n1, n2 in self._links:
            lines.append(f"topo.addLink('{n1}', '{n2}')")
        lines.append("net = Mininet(topo=topo)")
        lines.append("net.start()")
        lines.append("net.interact()")
        return "\n".join(lines)
```

## Monitoring and Observability

### SDN Metrics

```python
@dataclass
class SdnMetrics:
    active_switches: int = 0
    total_flows: int = 0
    packets_per_second: float = 0.0
    controller_cpu_percent: float = 0.0
    topology_changes: int = 0
    flow_table_utilization: float = 0.0

    def get_dashboard(self) -> dict:
        return {
            "switches": self.active_switches,
            "flows": self.total_flows,
            "pps": f"{self.packets_per_second:.0f}",
            "cpu": f"{self.controller_cpu_percent:.1f}%",
            "topo_changes": self.topology_changes,
            "ft_util": f"{self.flow_table_utilization:.1%}",
        }
```

## Testing Strategy

### Flow Rule Tests

```python
class FlowRuleTest:
    def __init__(self, controller: OpenFlowController):
        self.controller = controller

    def test_install_and_match(self, dpid: str) -> bool:
        match = {"src_ip": "10.0.0.1"}
        actions = [{"type": "output", "port": 2}]
        cookie = self.controller.install_flow(dpid, match, actions)
        flows = self.controller._flow_tables.get(dpid, [])
        return any(f["cookie"] == cookie for f in flows)

    def test_priority_ordering(self, dpid: str) -> bool:
        self.controller.install_flow(dpid, {"src_ip": "10.0.0.1"}, [{"type": "drop"}], priority=100)
        self.controller.install_flow(dpid, {"src_ip": "10.0.0.1"}, [{"type": "output", "port": 1}], priority=500)
        flows = self.controller._flow_tables.get(dpid, [])
        high_p = [f for f in flows if f["priority"] >= 500]
        return len(high_p) > 0
```

## Versioning and Migration

| Version | Changes |
|---------|---------|
| 2.0.0 | Network slicing, policy engine, distributed controller |
| 1.5.0 | Flow table management, REST API |
| 1.0.0 | Initial release with basic OpenFlow support |

## Glossary

| Term | Definition |
|------|-----------|
| **OpenFlow** | Protocol for SDN controller-switch communication |
| **Flow Table** | Switch table mapping packets to actions |
| **Controller** | Central intelligence in SDN architecture |
| **Northbound API** | Interface between applications and controller |
| **Southbound API** | Interface between controller and switches |
| **Packet-in** | Message from switch to controller for unknown packets |
| **Network Slicing** | Virtual network isolation on shared infrastructure |
| **LLDP** | Link Layer Discovery Protocol for topology discovery |
| **TCAM** | Ternary Content-Addressable Memory for flow matching |
| **Pipeline** | Multi-table flow processing in OpenFlow 1.3+ |

## Changelog

- **2.0.0** - Network slicing, policy engine, distributed controller
- **1.5.0** - Flow table management, REST API
- **1.2.0** - Added topology management
- **1.1.0** - Enhanced flow matching
- **1.0.0** - Initial release

## Contributing Guidelines

1. Test flow rules in Mininet before deployment
2. Verify controller failover behavior
3. Benchmark flow table performance
4. Document API changes

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
