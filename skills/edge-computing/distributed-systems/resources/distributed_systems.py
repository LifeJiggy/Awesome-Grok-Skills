"""
Distributed Systems Pipeline
Edge computing and distributed architecture patterns
"""

import hashlib
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ConsistencyLevel(Enum):
    STRONG = "strong"
    EVENTUAL = "eventual"
    CAUSAL = "causal"


@dataclass
class Node:
    node_id: str
    region: str
    capacity: float
    current_load: float = 0.0
    
    def is_healthy(self) -> bool:
        return self.current_load < self.capacity * 0.9
    
    def latency_to(self, other: "Node") -> float:
        """Estimate latency to another node"""
        latencies = {
            ("us-east", "us-west"): 80,
            ("us-east", "eu-west"): 100,
            ("us-east", "ap-southeast"): 180,
            ("us-west", "eu-west"): 160,
            ("us-west", "ap-southeast"): 120,
            ("eu-west", "ap-southeast"): 220
        }
        return latencies.get((self.region, other.region), 200)


class DistributedCache:
    """Distributed caching with consistent hashing"""
    
    def __init__(self, nodes: List[Node], replication_factor: int = 3):
        self.nodes = nodes
        self.replication_factor = replication_factor
        self.ring = {}
        self._build_ring()
    
    def _build_ring(self):
        """Build consistent hashing ring"""
        for node in self.nodes:
            for i in range(100):
                hash_key = f"{node.node_id}:{i}"
                position = int(hashlib.md5(hash_key.encode()).hexdigest(), 16)
                self.ring[position] = node
    
    def _find_node(self, key: str) -> Node:
        """Find node responsible for key"""
        key_hash = int(hashlib.md5(key.encode()).hexdigest(), 16)
        positions = sorted(self.ring.keys())
        
        for pos in positions:
            if pos >= key_hash:
                return self.ring[pos]
        
        return self.ring[positions[0]]
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        node = self._find_node(key)
        return getattr(node, f"cache_{key}", None)
    
    def set(self, key: str, value: str):
        """Set value in cache with replication"""
        primary = self._find_node(key)
        setattr(primary, f"cache_{key}", value)
        
        replicas = self._get_replicas(primary)
        for replica in replicas:
            setattr(replica, f"cache_{key}", value)
    
    def _get_replicas(self, primary: Node) -> List[Node]:
        """Get replica nodes"""
        replicas = []
        positions = sorted(self.ring.keys())
        primary_pos = [p for p, n in self.ring.items() if n == primary][0]
        idx = positions.index(primary_pos)
        
        for i in range(1, self.replication_factor):
            replica_pos = positions[(idx + i) % len(positions)]
            replicas.append(self.ring[replica_pos])
        
        return replicas


class LoadBalancer:
    """Global load balancing with latency-based routing"""
    
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
    
    def route_request(self, client_region: str, 
                     service: str) -> Tuple[Node, float]:
        """Route request to optimal node"""
        candidates = [n for n in self.nodes if n.is_healthy()]
        
        if not candidates:
            return self.nodes[0], 500
        
        best_node = None
        best_latency = float('inf')
        
        for node in candidates:
            latency = node.latency_to(Node("client", client_region, 100))
            if latency < best_latency:
                best_latency = latency
                best_node = node
        
        return best_node, best_latency
    
    def health_check(self) -> Dict:
        """Check health of all nodes"""
        return {
            node.node_id: {
                "healthy": node.is_healthy(),
                "load": node.current_load / node.capacity
            }
            for node in self.nodes
        }


class ConsistencyManager:
    """Manage consistency in distributed systems"""
    
    def __init__(self):
        self.vector_clocks = {}
        self.pending_writes = []
    
    def write(self, key: str, value: str, node_id: str):
        """Write with vector clock"""
        if key not in self.vector_clocks:
            self.vector_clocks[key] = {}
        
        self.vector_clocks[key][node_id] = self.vector_clocks[key].get(node_id, 0) + 1
        
        self.pending_writes.append({
            "key": key,
            "value": value,
            "vector_clock": self.vector_clocks[key].copy()
        })
    
    def check_causal(self, key: str, vector_clock: Dict) -> bool:
        """Check if write respects causal consistency"""
        if key not in self.vector_clocks:
            return True
        
        for node, timestamp in vector_clock.items():
            local_timestamp = self.vector_clocks[key].get(node, 0)
            if local_timestamp > timestamp:
                return False
        
        return True
    
    def resolve_conflict(self, key: str, writes: List[Dict]) -> str:
        """Resolve conflicting writes using last-write-wins"""
        if not writes:
            return ""
        
        return max(writes, key=lambda w: max(w["vector_clock"].values()))["value"]


class CircuitBreaker:
    """Circuit breaker for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, 
                 recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure = None
        self.state = "closed"
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker"""
        if self.state == "open":
            if time.time() - self.last_failure > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = "closed"
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"


if __name__ == "__main__":
    nodes = [
        Node("node-1", "us-east", 100),
        Node("node-2", "us-west", 100),
        Node("node-3", "eu-west", 100)
    ]
    
    cache = DistributedCache(nodes, replication_factor=2)
    lb = LoadBalancer(nodes)
    consistency = ConsistencyManager()
    breaker = CircuitBreaker()
    
    cache.set("user:123", "John")
    node, latency = lb.route_request("us-east", "api")
    consistency.write("user:123", "John", "node-1")
    
    print(f"Cache node: {cache._find_node('user:123').node_id}")
    print(f"Routing latency: {latency}ms")
    print(f"Circuit state: {breaker.state}")
