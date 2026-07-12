"""
Quantum Networking Module
==========================

Protocols and infrastructure for entanglement distribution, quantum teleportation,
quantum repeaters, purification, and multi-node quantum network simulation.

Author: Quantum Skill Module
Version: 1.0.0
"""

from __future__ import annotations

import enum
import heapq
import logging
import math
import secrets
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProtocolType(enum.Enum):
    """Quantum networking protocol types."""
    TELEPORTATION = "teleportation"
    SUPERDENSE_CODING = "superdense_coding"
    ENTANGLEMENT_DISTRIBUTION = "entanglement_distribution"
    QKD_RELAY = "qkd_relay"


class PurificationMethod(enum.Enum):
    """Entanglement purification protocol variants."""
    DEJMPS = "DEJMPS"
    BBPSSW = "BBPSSW"
    RECURRENCE = "recurrence"


class MemoryStatus(enum.Enum):
    """Quantum memory slot status."""
    EMPTY = "empty"
    OCCUPIED = "occupied"
    DECAYED = "decayed"
    RESERVED = "reserved"


class NetworkNodeType(enum.Enum):
    """Types of network nodes."""
    ENDPOINT = "endpoint"
    REPEATER = "repeater"
    SWITCH = "switch"
    SOURCE = "entanglement_source"


class LinkStatus(enum.Enum):
    """Quantum link operational status."""
    ACTIVE = "active"
    DEGRADED = "degraded"
    DOWN = "down"
    CALIBRATING = "calibrating"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class QuantumState:
    """Simple qubit state representation."""
    alpha: complex = 1.0
    beta: complex = 0.0

    @classmethod
    def from_bloch(cls, theta: float, phi: float) -> QuantumState:
        return cls(
            alpha=complex(math.cos(theta / 2)),
            beta=complex(math.exp(1j * phi) * math.sin(theta / 2)),
        )

    @classmethod
    def computational(cls, bit: int) -> QuantumState:
        if bit == 0:
            return cls(alpha=1.0, beta=0.0)
        return cls(alpha=0.0, beta=1.0)

    def fidelity_to(self, other: QuantumState) -> float:
        overlap = abs(self.alpha * other.alpha + self.beta * other.beta) ** 2
        return float(overlap)

    def is_normalized(self) -> bool:
        return abs(abs(self.alpha) ** 2 + abs(self.beta) ** 2 - 1.0) < 1e-6


@dataclass
class BellPair:
    """Shared Bell pair between two nodes."""
    fidelity: float = 1.0
    source_node: Optional[str] = None
    target_node: Optional[str] = None
    creation_time: float = 0.0
    coherence_time: float = 10.0

    @property
    def is_usable(self) -> bool:
        return self.fidelity > 0.5

    def degrade(self, dt: float, dephasing_rate: float = 0.01) -> BellPair:
        decay = math.exp(-dephasing_rate * dt)
        return BellPair(
            fidelity=0.5 + (self.fidelity - 0.5) * decay,
            source_node=self.source_node,
            target_node=self.target_node,
            creation_time=self.creation_time + dt,
            coherence_time=self.coherence_time,
        )


@dataclass
class TeleportationResult:
    """Result of a quantum teleportation protocol."""
    fidelity: float
    bell_pair_consumed: bool = True
    classical_bits: int = 2
    success: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PurificationResult:
    """Result of entanglement purification."""
    input_fidelity: float
    output_fidelity: float
    pairs_consumed: int
    pairs_output: int
    rounds: int
    method: PurificationMethod = PurificationMethod.DEJMPS


@dataclass
class RepeaterSegment:
    """Single segment of a quantum repeater chain."""
    length_km: float
    loss_per_km: float = 0.2
    noise_rate: float = 0.01
    memory_coherence_time: float = 10.0

    @property
    def total_loss(self) -> float:
        return 1.0 - math.exp(-self.loss_per_km * self.length_km)

    @property
    def channel_fidelity(self) -> float:
        return 1.0 - self.noise_rate * self.length_km / 100.0


@dataclass
class RepeaterResult:
    """Result of repeater-based entanglement distribution."""
    fidelity: float
    total_distance_km: float
    key_rate: float
    num_swaps: int
    purification_rounds: int
    success_probability: float


@dataclass
class DistributionResult:
    """End-to-end entanglement distribution result."""
    fidelity: float
    latency: float
    success_probability: float
    path: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NetworkNode:
    """Quantum network node."""
    node_id: str
    node_type: NetworkNodeType = NetworkNodeType.ENDPOINT
    memory_size: int = 10
    neighbors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.node_id:
            self.node_id = f"node_{id(self)}"


@dataclass
class QuantumLink:
    """Quantum link between two nodes."""
    node_a: NetworkNode
    node_b: NetworkNode
    fidelity: float = 0.9
    generation_rate: float = 1000.0
    status: LinkStatus = LinkStatus.ACTIVE
    distance_km: float = 10.0

    @property
    def loss_probability(self) -> float:
        return 1.0 - self.fidelity


@dataclass
class QuantumMemory:
    """Quantum memory with coherence and storage properties."""
    num_slots: int = 10
    coherence_time: float = 5.0
    storage_fidelity: float = 0.99
    readout_fidelity: float = 0.98
    _slots: dict[int, tuple[QuantumState, float, MemoryStatus]] = field(
        default_factory=dict, repr=False
    )

    def __post_init__(self) -> None:
        self._slots = {}

    @property
    def occupancy(self) -> int:
        return sum(1 for _, _, s in self._slots.values() if s == MemoryStatus.OCCUPIED)

    @property
    def available(self) -> int:
        return self.num_slots - self.occupancy

    def store(self, state: QuantumState) -> int:
        for slot in range(self.num_slots):
            if slot not in self._slots or self._slots[slot][2] == MemoryStatus.EMPTY:
                import time
                self._slots[slot] = (state, time.time(), MemoryStatus.OCCUPIED)
                return slot
        raise MemoryError("No available memory slots")

    def retrieve(self, slot: int, current_time: Optional[float] = None) -> QuantumState:
        if slot not in self._slots:
            raise KeyError(f"Slot {slot} not found")
        state, store_time, status = self._slots[slot]
        if status != MemoryStatus.OCCUPIED:
            raise ValueError(f"Slot {slot} is {status.value}")
        if current_time is None:
            import time
            current_time = time.time()
        elapsed = current_time - store_time
        decay = math.exp(-elapsed / self.coherence_time)
        fidelity = self.storage_fidelity * decay * self.readout_fidelity
        degraded = QuantumState(
            alpha=state.alpha * math.sqrt(fidelity),
            beta=state.beta * math.sqrt(fidelity),
        )
        self._slots[slot] = (state, store_time, MemoryStatus.EMPTY)
        return degraded

    def decay_check(self, current_time: Optional[float] = None) -> list[int]:
        if current_time is None:
            import time
            current_time = time.time()
        decayed: list[int] = []
        for slot, (state, store_time, status) in list(self._slots.items()):
            if status == MemoryStatus.OCCUPIED:
                elapsed = current_time - store_time
                if elapsed > self.coherence_time * 3:
                    self._slots[slot] = (state, store_time, MemoryStatus.DECAYED)
                    decayed.append(slot)
        return decayed


@dataclass
class PathResult:
    """Best path found by router."""
    nodes: list[str]
    fidelity: float
    latency: float
    total_distance_km: float


# ---------------------------------------------------------------------------
# Quantum Teleporter
# ---------------------------------------------------------------------------

class QuantumTeleporter:
    """Quantum state teleportation using Bell pairs."""

    def __init__(self, bell_pair: BellPair) -> None:
        self.bell_pair = bell_pair

    def teleport(self, state: QuantumState) -> TeleportationResult:
        if not self.bell_pair.is_usable:
            return TeleportationResult(
                fidelity=0.0, bell_pair_consumed=False, success=False
            )

        fidelity = self.bell_pair.fidelity * state.fidelity_to(state)

        return TeleportationResult(
            fidelity=min(fidelity, 1.0),
            bell_pair_consumed=True,
            classical_bits=2,
            success=True,
        )


# ---------------------------------------------------------------------------
# Purification Protocol
# ---------------------------------------------------------------------------

class PurificationProtocol:
    """Entanglement purification protocols (DEJMPS, BBPSSW)."""

    def __init__(
        self,
        method: PurificationMethod = PurificationMethod.DEJMPS,
        input_fidelity: float = 0.85,
        num_rounds: int = 1,
    ) -> None:
        self.method = method
        self.input_fidelity = input_fidelity
        self.num_rounds = num_rounds

    def purify(self) -> PurificationResult:
        fidelity = self.input_fidelity
        total_consumed = 0
        total_output = 1

        for round_num in range(self.num_rounds):
            if self.method == PurificationMethod.DEJMPS:
                fidelity = self._dejmps_step(fidelity)
                consumed = 2
                output = 1
            elif self.method == PurificationMethod.BBPSSW:
                fidelity = self._bbpssw_step(fidelity)
                consumed = 3
                output = 1
            else:
                fidelity = self._recurrence_step(fidelity)
                consumed = 2
                output = 1

            total_consumed += consumed
            total_output = output
            fidelity = min(fidelity, 0.9999)

        return PurificationResult(
            input_fidelity=self.input_fidelity,
            output_fidelity=fidelity,
            pairs_consumed=total_consumed,
            pairs_output=total_output,
            rounds=self.num_rounds,
            method=self.method,
        )

    def _dejmps_step(self, F: float) -> float:
        """DEJMPS single-round fidelity update."""
        F_new = (F ** 2 + (1 - F) ** 2 / 9) / (F ** 2 + 2 * F * (1 - F) / 3 + 5 * (1 - F) ** 2 / 9)
        return F_new

    def _bbpssw_step(self, F: float) -> float:
        """BBPSSW single-round fidelity update."""
        E = 1 - F
        F_new = (F ** 2 + E ** 2 / 9) / (F ** 2 + 2 * F * E / 3 + 5 * E ** 2 / 9)
        return F_new

    def _recurrence_step(self, F: float) -> float:
        """Recurrence purification step."""
        E = 1 - F
        p_success = F ** 2 + E ** 2 / 9
        F_new = (F ** 2 + E ** 2 / 9) / p_success if p_success > 0 else 0.5
        return F_new


# ---------------------------------------------------------------------------
# Quantum Repeater
# ---------------------------------------------------------------------------

class QuantumRepeater:
    """Multi-segment quantum repeater chain."""

    def __init__(
        self,
        segments: list[RepeaterSegment],
        memory_coherence_time: float = 10.0,
        purification_rounds: int = 2,
        swap_success_probability: float = 0.5,
    ) -> None:
        self.segments = segments
        self.memory_coherence_time = memory_coherence_time
        self.purification_rounds = purification_rounds
        self.swap_success_prob = swap_success_probability

    def distribute(
        self,
        source_fidelity: float = 0.99,
        time_budget: float = 5.0,
    ) -> RepeaterResult:
        fidelity = source_fidelity
        total_distance = sum(s.length_km for s in self.segments)
        num_swaps = len(self.segments) - 1

        for seg in self.segments:
            fidelity *= seg.channel_fidelity
            fidelity *= (1 - seg.total_loss)

        purifier = PurificationProtocol(
            method=PurificationMethod.DEJMPS,
            input_fidelity=fidelity,
            num_rounds=self.purification_rounds,
        )
        pur_result = purifier.purify()
        fidelity = pur_result.output_fidelity

        success_prob = self.swap_success_prob ** num_swaps
        latency = total_distance / 300000.0  # speed of light in fiber

        key_rate = 0.0
        if fidelity > 0.5:
            h = -fidelity * math.log2(fidelity) - (1 - fidelity) * math.log2(max(1 - fidelity, 1e-15))
            key_rate = max(0, (1 - 2 * h)) * 1000

        return RepeaterResult(
            fidelity=fidelity,
            total_distance_km=total_distance,
            key_rate=key_rate,
            num_swaps=num_swaps,
            purification_rounds=self.purification_rounds,
            success_probability=success_prob,
        )


# ---------------------------------------------------------------------------
# Quantum Network
# ---------------------------------------------------------------------------

class QuantumNetwork:
    """Multi-node quantum network for entanglement distribution."""

    def __init__(
        self,
        nodes: list[NetworkNode],
        links: list[QuantumLink],
    ) -> None:
        self.nodes = {n.node_id: n for n in nodes}
        self.links = links
        self._adjacency: dict[str, list[QuantumLink]] = {}
        for link in links:
            self._adjacency.setdefault(link.node_a.node_id, []).append(link)
            self._adjacency.setdefault(link.node_b.node_id, []).append(link)

    def distribute_entanglement(
        self,
        source: NetworkNode,
        target: NetworkNode,
        target_fidelity: float = 0.9,
        time_budget: float = 1.0,
    ) -> DistributionResult:
        path = self._find_path(source.node_id, target.node_id)
        if not path:
            return DistributionResult(fidelity=0.0, latency=float("inf"), success_probability=0.0)

        fidelity = 1.0
        for i in range(len(path) - 1):
            link = self._get_link(path[i], path[i + 1])
            if link:
                fidelity *= link.fidelity

        num_hops = len(path) - 1
        success_prob = 0.9 ** num_hops
        latency = num_hops * 0.001

        return DistributionResult(
            fidelity=fidelity,
            latency=latency,
            success_probability=success_prob,
            path=path,
        )

    def _find_path(self, source: str, target: str) -> list[str]:
        visited: set[str] = set()
        queue: list[tuple[float, list[str]]] = [(0.0, [source])]

        while queue:
            cost, path = heapq.heappop(queue)
            current = path[-1]
            if current == target:
                return path
            if current in visited:
                continue
            visited.add(current)

            for link in self._adjacency.get(current, []):
                neighbor = link.node_b.node_id if link.node_a.node_id == current else link.node_a.node_id
                if neighbor not in visited:
                    new_cost = cost + (1.0 - link.fidelity)
                    heapq.heappush(queue, (new_cost, path + [neighbor]))

        return []

    def _get_link(self, node_a: str, node_b: str) -> Optional[QuantumLink]:
        for link in self.links:
            if (link.node_a.node_id == node_a and link.node_b.node_id == node_b):
                return link
            if (link.node_a.node_id == node_b and link.node_b.node_id == node_a):
                return link
        return None


# ---------------------------------------------------------------------------
# Quantum Router
# ---------------------------------------------------------------------------

class QuantumRouter:
    """Fidelity-aware routing for quantum networks."""

    def __init__(self, topology: NetworkTopology) -> None:
        self.topology = topology

    def find_best_path(
        self,
        source: str,
        target: str,
        min_fidelity: float = 0.0,
    ) -> PathResult:
        all_paths = self._enumerate_paths(source, target)
        if not all_paths:
            return PathResult([], 0.0, float("inf"), 0.0)

        best_path: Optional[list[str]] = None
        best_fidelity = 0.0
        best_latency = float("inf")

        for path in all_paths:
            fidelity = self._path_fidelity(path)
            latency = self._path_latency(path)
            distance = self._path_distance(path)

            if fidelity >= min_fidelity and fidelity > best_fidelity:
                best_path = path
                best_fidelity = fidelity
                best_latency = latency

        if best_path is None:
            return PathResult([], 0.0, float("inf"), 0.0)

        return PathResult(
            nodes=best_path,
            fidelity=best_fidelity,
            latency=best_latency,
            total_distance_km=self._path_distance(best_path),
        )

    def _enumerate_paths(
        self, source: str, target: str, max_depth: int = 10
    ) -> list[list[str]]:
        paths: list[list[str]] = []
        self._dfs(source, target, [], set(), paths, max_depth)
        return paths

    def _dfs(
        self,
        current: str,
        target: str,
        path: list[str],
        visited: set[str],
        all_paths: list[list[str]],
        max_depth: int,
    ) -> None:
        if len(path) > max_depth:
            return
        if current == target:
            all_paths.append(path + [current])
            return
        visited.add(current)
        for neighbor in self.topology.neighbors(current):
            if neighbor not in visited:
                self._dfs(neighbor, target, path + [current], visited.copy(), all_paths, max_depth)

    def _path_fidelity(self, path: list[str]) -> float:
        fidelity = 1.0
        for i in range(len(path) - 1):
            link = self.topology.get_link(path[i], path[i + 1])
            if link:
                fidelity *= link.fidelity
            else:
                return 0.0
        return fidelity

    def _path_latency(self, path: list[str]) -> float:
        latency = 0.0
        for i in range(len(path) - 1):
            link = self.topology.get_link(path[i], path[i + 1])
            if link:
                latency += link.latency
        return latency

    def _path_distance(self, path: list[str]) -> float:
        dist = 0.0
        for i in range(len(path) - 1):
            link = self.topology.get_link(path[i], path[i + 1])
            if link:
                dist += link.distance_km
        return dist


# ---------------------------------------------------------------------------
# Network Topology
# ---------------------------------------------------------------------------

@dataclass
class TopologyLink:
    """Link in the network topology graph."""
    node_a: str
    node_b: str
    fidelity: float
    latency: float
    distance_km: float = 10.0


class NetworkTopology:
    """Graph-based network topology for routing."""

    def __init__(self) -> None:
        self._nodes: set[str] = set()
        self._links: list[TopologyLink] = []
        self._adj: dict[str, list[str]] = {}

    def add_node(self, node_id: str) -> None:
        self._nodes.add(node_id)

    def add_link(
        self,
        node_a: str,
        node_b: str,
        fidelity: float = 0.9,
        latency: float = 0.001,
        distance_km: float = 10.0,
    ) -> None:
        self._links.append(TopologyLink(node_a, node_b, fidelity, latency, distance_km))
        self._adj.setdefault(node_a, []).append(node_b)
        self._adj.setdefault(node_b, []).append(node_a)

    def neighbors(self, node_id: str) -> list[str]:
        return self._adj.get(node_id, [])

    def get_link(self, node_a: str, node_b: str) -> Optional[TopologyLink]:
        for link in self._links:
            if (link.node_a == node_a and link.node_b == node_b) or \
               (link.node_a == node_b and link.node_b == node_a):
                return link
        return None

    @property
    def num_nodes(self) -> int:
        return len(self._nodes)

    @property
    def num_links(self) -> int:
        return len(self._links)


# ---------------------------------------------------------------------------
# Entanglement Scheduling
# ---------------------------------------------------------------------------

class EntanglementScheduler:
    """Schedule entanglement generation across network links."""

    def __init__(self, network: QuantumNetwork, time_bins: int = 100) -> None:
        self.network = network
        self.time_bins = time_bins
        self._schedule: dict[int, list[tuple[str, str]]] = {}

    def generate_schedule(self) -> dict[int, list[tuple[str, str]]]:
        self._schedule = {t: [] for t in range(self.time_bins)}
        for link in self.network.links:
            rate = link.generation_rate
            interval = max(1, int(self.time_bins / (rate / 100)))
            for t in range(0, self.time_bins, interval):
                self._schedule[t].append((link.node_a.node_id, link.node_b.node_id))
        return self._schedule

    def get_active_links(self, time_bin: int) -> list[tuple[str, str]]:
        return self._schedule.get(time_bin, [])

    def utilization(self) -> float:
        total = sum(len(links) for links in self._schedule.values())
        max_possible = self.time_bins * len(self.network.links)
        return total / max(1, max_possible)


# ---------------------------------------------------------------------------
# Network Tomography
# ---------------------------------------------------------------------------

class NetworkTomography:
    """Estimate link fidelities from measurement statistics."""

    def __init__(self, network: QuantumNetwork) -> None:
        self.network = network
        self._measurements: dict[str, list[int]] = {}

    def record_measurement(self, link_id: str, success: bool) -> None:
        self._measurements.setdefault(link_id, []).append(1 if success else 0)

    def estimate_fidelity(self, link_id: str) -> float:
        if link_id not in self._measurements or not self._measurements[link_id]:
            return 0.5
        data = self._measurements[link_id]
        success_rate = sum(data) / len(data)
        return 0.5 + success_rate * 0.5

    def estimate_all(self) -> dict[str, float]:
        results: dict[str, float] = {}
        for link in self.network.links:
            link_id = f"{link.node_a.node_id}-{link.node_b.node_id}"
            results[link_id] = self.estimate_fidelity(link_id)
        return results


# ---------------------------------------------------------------------------
# QKD Network
# ---------------------------------------------------------------------------

class QKDNetwork:
    """Multi-node quantum key distribution network with key relay."""

    def __init__(self, network: QuantumNetwork) -> None:
        self.network = network
        self._key_registry: dict[str, bytes] = {}

    def establish_key(
        self,
        source: NetworkNode,
        target: NetworkNode,
        key_length: int = 256,
    ) -> bytes:
        path_result = self.network.distribute_entanglement(source, target)
        if path_result.fidelity < 0.5:
            raise ValueError("Entanglement fidelity too low for key generation")

        key = secrets.token_bytes(key_length // 8)
        pair_key = f"{source.node_id}-{target.node_id}"
        self._key_registry[pair_key] = key
        return key

    def relay_key(
        self,
        intermediate_node: NetworkNode,
        source_key: bytes,
        target_key: bytes,
    ) -> bytes:
        xored = bytes(a ^ b for a, b in zip(source_key, target_key))
        return xored

    def get_stored_key(self, node_a: str, node_b: str) -> Optional[bytes]:
        return self._key_registry.get(f"{node_a}-{node_b}")


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate quantum networking module capabilities."""
    print("=" * 60)
    print("  Quantum Networking Module — Demo")
    print("=" * 60)

    # 1. Quantum Teleportation
    print("\n--- 1. Quantum Teleportation ---")
    bell = BellPair(fidelity=0.95)
    teleporter = QuantumTeleporter(bell_pair=bell)
    state = QuantumState.from_bloch(theta=0.5, phi=0.3)
    t_result = teleporter.teleport(state)
    print(f"Teleportation fidelity: {t_result.fidelity:.4f}")
    print(f"Bell pair consumed: {t_result.bell_pair_consumed}")
    print(f"Classical bits: {t_result.classical_bits}")

    # 2. Entanglement Purification
    print("\n--- 2. Entanglement Purification (DEJMPS) ---")
    purifier = PurificationProtocol(
        method=PurificationMethod.DEJMPS,
        input_fidelity=0.80,
        num_rounds=3,
    )
    pur_result = purifier.purify()
    print(f"Input fidelity: {pur_result.input_fidelity:.4f}")
    print(f"Output fidelity: {pur_result.output_fidelity:.4f}")
    print(f"Pairs consumed: {pur_result.pairs_consumed}")

    # 3. Quantum Repeater
    print("\n--- 3. Quantum Repeater Chain (3 segments) ---")
    segments = [
        RepeaterSegment(length_km=50, loss_per_km=0.2, noise_rate=0.01),
        RepeaterSegment(length_km=50, loss_per_km=0.2, noise_rate=0.01),
        RepeaterSegment(length_km=50, loss_per_km=0.2, noise_rate=0.01),
    ]
    repeater = QuantumRepeater(
        segments=segments,
        memory_coherence_time=10.0,
        purification_rounds=2,
        swap_success_probability=0.6,
    )
    rep_result = repeater.distribute(source_fidelity=0.99, time_budget=5.0)
    print(f"Output fidelity: {rep_result.fidelity:.4f}")
    print(f"Total distance: {rep_result.total_distance_km} km")
    print(f"Key rate: {rep_result.key_rate:.1f} bits/s")
    print(f"Success probability: {rep_result.success_probability:.4f}")

    # 4. Quantum Network Distribution
    print("\n--- 4. Quantum Network (5 nodes) ---")
    nodes = [NetworkNode(node_id=f"N{i}", memory_size=10) for i in range(5)]
    links = [
        QuantumLink(nodes[i], nodes[i + 1], fidelity=0.9, generation_rate=1000)
        for i in range(4)
    ]
    qnet = QuantumNetwork(nodes=nodes, links=links)
    dist = qnet.distribute_entanglement(nodes[0], nodes[4], target_fidelity=0.85)
    print(f"Path: {' -> '.join(dist.path)}")
    print(f"Fidelity: {dist.fidelity:.4f}")
    print(f"Latency: {dist.latency:.4f} s")
    print(f"Success prob: {dist.success_probability:.4f}")

    # 5. Quantum Memory
    print("\n--- 5. Quantum Memory ---")
    mem = QuantumMemory(num_slots=5, coherence_time=5.0, storage_fidelity=0.99)
    slot0 = mem.store(QuantumState.computational(0))
    slot1 = mem.store(QuantumState.from_bloch(1.0, 0.5))
    print(f"Slots in use: {mem.occupancy}/{mem.num_slots}")
    retrieved = mem.retrieve(slot0)
    print(f"Retrieved fidelity: {retrieved.fidelity_to(QuantumState.computational(0)):.4f}")

    # 6. Network Routing
    print("\n--- 6. Network Routing ---")
    topo = NetworkTopology()
    for n in ["A", "B", "C", "D", "E"]:
        topo.add_node(n)
    topo.add_link("A", "B", fidelity=0.95, latency=0.001, distance_km=10)
    topo.add_link("B", "C", fidelity=0.90, latency=0.001, distance_km=15)
    topo.add_link("A", "C", fidelity=0.70, latency=0.002, distance_km=20)
    topo.add_link("C", "D", fidelity=0.92, latency=0.001, distance_km=12)
    topo.add_link("D", "E", fidelity=0.88, latency=0.001, distance_km=10)
    topo.add_link("B", "D", fidelity=0.75, latency=0.002, distance_km=18)

    router = QuantumRouter(topo)
    path_result = router.find_best_path("A", "E", min_fidelity=0.7)
    print(f"Best path: {' -> '.join(path_result.nodes)}")
    print(f"Fidelity: {path_result.fidelity:.4f}")
    print(f"Latency: {path_result.latency:.4f} s")
    print(f"Distance: {path_result.total_distance_km} km")

    # 7. Entanglement Scheduling
    print("\n--- 7. Entanglement Scheduling ---")
    scheduler = EntanglementScheduler(qnet, time_bins=10)
    sched = scheduler.generate_schedule()
    utilization = scheduler.utilization()
    active_at_0 = scheduler.get_active_links(0)
    print(f"Time bins: {len(sched)}")
    print(f"Active links at t=0: {active_at_0}")
    print(f"Link utilization: {utilization:.2%}")

    # 8. QKD Network
    print("\n--- 8. QKD Key Relay ---")
    qkd = QKDNetwork(qnet)
    key = qkd.establish_key(nodes[0], nodes[4], key_length=128)
    print(f"Established key: {key.hex()[:32]}...")
    print(f"Key length: {len(key) * 8} bits")

    # 9. Network Tomography
    print("\n--- 9. Network Tomography ---")
    tomography = NetworkTomography(qnet)
    for _ in range(100):
        for link in qnet.links:
            link_id = f"{link.node_a.node_id}-{link.node_b.node_id}"
            tomography.record_measurement(link_id, secrets.randbelow(100) < link.fidelity * 100)
    estimates = tomography.estimate_all()
    for link_id, fid in estimates.items():
        print(f"  {link_id}: {fid:.4f}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
