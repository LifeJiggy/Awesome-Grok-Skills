"""
SDN (Software-Defined Networking) Module
Part of the networking skill domain.

SDN architecture, OpenFlow flow management, topology discovery,
network virtualization, and controller management.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class FlowAction(Enum):
    FORWARD = "forward"
    DROP = "drop"
    CONTROLLER = "controller"
    SET_VLAN = "set_vlan"
    STRIP_VLAN = "strip_vlan"
    SET_METADATA = "set_metadata"
    RESUBMIT = "resubmit"


class FlowPriority(Enum):
    LOW = 100
    NORMAL = 300
    HIGH = 500
    CRITICAL = 1000


@dataclass
class FlowEntry:
    cookie: int = 0
    priority: int = 300
    match: Dict[str, Any] = field(default_factory=dict)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    idle_timeout: int = 300
    hard_timeout: int = 0
    table_id: int = 0

    @property
    def flow_id(self) -> str:
        match_str = json.dumps(self.match, sort_keys=True)
        return hashlib.md5(match_str.encode()).hexdigest()[:12]

    def to_openflow(self) -> Dict[str, Any]:
        return {
            "cookie": self.cookie,
            "priority": self.priority,
            "match": self.match,
            "actions": self.actions,
            "idle_timeout": self.idle_timeout,
            "hard_timeout": self.hard_timeout,
            "table_id": self.table_id,
        }

    def matches_packet(self, packet: Dict[str, Any]) -> bool:
        return all(self.match.get(k) == v for k, v in packet.items())


@dataclass
class Switch:
    dpid: str
    name: str
    ports: List[Dict[str, Any]] = field(default_factory=list)
    is_connected: bool = True
    controller_ip: str = ""
    openflow_version: str = "1.3"


@dataclass
class Link:
    src_switch: str
    src_port: int
    dst_switch: str
    dst_port: int
    bandwidth_mbps: float = 1000.0
    latency_ms: float = 1.0
    is_up: bool = True


@dataclass
class NetworkSlice:
    slice_id: str
    name: str
    vlan_id: int = 0
    bandwidth_mbps: float = 100.0
    switches: List[str] = field(default_factory=list)
    flows: List[FlowEntry] = field(default_factory=list)


class FlowTableManager:
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self._tables: Dict[str, List[FlowEntry]] = {}

    def add_flow(self, dpid: str, flow: FlowEntry) -> str:
        if dpid not in self._tables:
            self._tables[dpid] = []
        if len(self._tables[dpid]) >= self.max_entries:
            self._evict_flows(dpid)
        self._tables[dpid].append(flow)
        self._tables[dpid].sort(key=lambda f: f.priority, reverse=True)
        return flow.flow_id

    def remove_flow(self, dpid: str, flow_id: str) -> bool:
        if dpid in self._tables:
            before = len(self._tables[dpid])
            self._tables[dpid] = [f for f in self._tables[dpid] if f.flow_id != flow_id]
            return len(self._tables[dpid]) < before
        return False

    def get_flows(self, dpid: str) -> List[FlowEntry]:
        return list(self._tables.get(dpid, []))

    def clear_flows(self, dpid: str):
        self._tables[dpid] = []

    def match_packet(self, dpid: str, packet: Dict[str, Any]) -> Optional[FlowEntry]:
        for flow in self._tables.get(dpid, []):
            if flow.matches_packet(packet):
                return flow
        return None

    def _evict_flows(self, dpid: str):
        if dpid in self._tables and len(self._tables[dpid]) > 0:
            self._tables[dpid].pop()

    def get_stats(self) -> Dict[str, Any]:
        return {
            dpid: {"total_flows": len(flows), "max_entries": self.max_entries}
            for dpid, flows in self._tables.items()
        }


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
        self._adjacency[link.dst_switch].append((link.src_switch, link.dst_port, link.src_port))

    def remove_link(self, src: str, dst: str):
        self._links = [l for l in self._links
                       if not ((l.src_switch == src and l.dst_switch == dst) or
                               (l.src_switch == dst and l.dst_switch == src))]
        self._adjacency[src] = [(d, sp, dp) for d, sp, dp in self._adjacency[src] if d != dst]
        self._adjacency[dst] = [(d, sp, dp) for d, sp, dp in self._adjacency[dst] if d != src]

    def shortest_path(self, src: str, dst: str) -> Optional[List[str]]:
        if src == dst:
            return [src]
        visited: Set[str] = {src}
        queue: List[Tuple[str, List[str]]] = [(src, [src])]
        while queue:
            current, path = queue.pop(0)
            for neighbor, _, _ in self._adjacency.get(current, []):
                if neighbor == dst:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def k_shortest_paths(self, src: str, dst: str, k: int = 3) -> List[List[str]]:
        paths: List[List[str]] = []
        self._dfs(src, dst, [src], set(), paths, k)
        return paths

    def _dfs(self, current: str, dst: str, path: List[str],
             visited: Set[str], results: List, limit: int):
        if len(results) >= limit:
            return
        if current == dst and len(path) > 1:
            results.append(list(path))
            return
        for neighbor, _, _ in self._adjacency.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                self._dfs(neighbor, dst, path, visited, results, limit)
                path.pop()
                visited.discard(neighbor)

    def get_switches(self) -> List[Switch]:
        return list(self._switches.values())

    def get_links(self) -> List[Link]:
        return list(self._links)

    def summary(self) -> Dict[str, Any]:
        return {
            "switches": len(self._switches),
            "links": len(self._links),
            "active_links": sum(1 for l in self._links if l.is_up),
            "total_bandwidth_mbps": sum(l.bandwidth_mbps for l in self._links if l.is_up),
        }


class NetworkSliceManager:
    def __init__(self):
        self._slices: Dict[str, NetworkSlice] = {}

    def create_slice(self, slice_id: str, name: str, vlan_id: int = 0) -> NetworkSlice:
        s = NetworkSlice(slice_id=slice_id, name=name, vlan_id=vlan_id)
        self._slices[slice_id] = s
        return s

    def add_switch_to_slice(self, slice_id: str, dpid: str):
        if slice_id in self._slices:
            self._slices[slice_id].switches.append(dpid)

    def add_flow_to_slice(self, slice_id: str, flow: FlowEntry):
        if slice_id in self._slices:
            self._slices[slice_id].flows.append(flow)

    def get_slice_flows(self, slice_id: str) -> List[FlowEntry]:
        return self._slices.get(slice_id, NetworkSlice("", "")).flows

    def list_slices(self) -> List[Dict[str, Any]]:
        return [
            {"id": s.slice_id, "name": s.name, "vlan": s.vlan_id,
             "switches": len(s.switches), "flows": len(s.flows)}
            for s in self._slices.values()
        ]


class SdnController:
    def __init__(self, name: str, ip: str = "0.0.0.0", port: int = 6633):
        self.name = name
        self.ip = ip
        self.port = port
        self.flow_table = FlowTableManager()
        self.topology = TopologyManager()
        self.slice_manager = NetworkSliceManager()
        self._switches: Dict[str, Switch] = {}

    def connect_switch(self, switch: Switch):
        self._switches[switch.dpid] = switch
        self.topology.add_switch(switch)

    def install_flow(self, dpid: str, match: Dict, actions: List[Dict],
                     priority: int = 300) -> str:
        flow = FlowEntry(match=match, actions=actions, priority=priority)
        return self.flow_table.add_flow(dpid, flow)

    def install_path_flows(self, src: str, dst: str) -> bool:
        path = self.topology.shortest_path(src, dst)
        if not path:
            return False
        for i in range(len(path) - 1):
            self.install_flow(
                path[i],
                match={"eth_dst": dst},
                actions=[{"type": "output", "port": 1}],
                priority=500,
            )
        return True

    def block_ip(self, dpid: str, src_ip: str) -> str:
        return self.install_flow(dpid, {"src_ip": src_ip}, [{"type": "drop"}], priority=1000)

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "ip": self.ip,
            "port": self.port,
            "switches": len(self._switches),
            "topology": self.topology.summary(),
            "slices": self.slice_manager.list_slices(),
            "flow_stats": self.flow_table.get_stats(),
        }


def main():
    print("=== SDN Module ===")

    controller = SdnController("main-controller", "192.168.1.100")

    print("\n=== Switches ===")
    for i in range(1, 5):
        sw = Switch(dpid=f"00:00:00:00:00:0{i}", name=f"Switch{i}")
        controller.connect_switch(sw)
        print(f"  Connected {sw.name} ({sw.dpid})")

    print("\n=== Links ===")
    links = [
        ("00:00:00:00:00:01", 1, "00:00:00:00:00:02", 1),
        ("00:00:00:00:00:02", 2, "00:00:00:00:00:03", 1),
        ("00:00:00:00:00:01", 2, "00:00:00:00:00:04", 1),
        ("00:00:00:00:00:03", 2, "00:00:00:00:00:04", 2),
    ]
    for src, sp, dst, dp in links:
        controller.topology.add_link(Link(src, sp, dst, dp))
        print(f"  Link: {src}:{sp} <-> {dst}:{dp}")

    print("\n=== Shortest Path ===")
    path = controller.topology.shortest_path("00:00:00:00:00:01", "00:00:00:00:00:03")
    print(f"  Path: {' -> '.join(path) if path else 'No path'}")

    k_paths = controller.topology.k_shortest_paths("00:00:00:00:00:01", "00:00:00:00:00:03")
    for i, p in enumerate(k_paths):
        print(f"  Path {i+1}: {' -> '.join(p)}")

    print("\n=== Flow Rules ===")
    fid1 = controller.install_flow("00:00:00:00:00:01", {"src_ip": "10.0.0.1"}, [{"type": "output", "port": 1}], 500)
    fid2 = controller.block_ip("00:00:00:00:00:01", "192.168.1.100")
    print(f"  Installed flow: {fid1}")
    print(f"  Block rule: {fid2}")

    flows = controller.flow_table.get_flows("00:00:00:00:00:01")
    print(f"  Total flows on Switch1: {len(flows)}")

    print("\n=== Network Slicing ===")
    s1 = controller.slice_manager.create_slice("slice-tenant-a", "Tenant A", vlan_id=100)
    controller.slice_manager.add_switch_to_slice("slice-tenant-a", "00:00:00:00:00:01")
    controller.slice_manager.add_flow_to_slice("slice-tenant-a",
        FlowEntry(match={"vlan_id": 100}, actions=[{"type": "output", "port": 1}]))
    print(f"  Slices: {controller.slice_manager.list_slices()}")

    print("\n=== Status ===")
    status = controller.get_status()
    print(f"  Controller: {status['name']}")
    print(f"  Switches: {status['switches']}")
    print(f"  Topology: {status['topology']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
