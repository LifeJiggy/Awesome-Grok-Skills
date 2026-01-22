from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
import time


class NodeType(Enum):
    CLOUD = "cloud"
    FOG = "fog"
    EDGE = "edge"
    IOT_GATEWAY = "iot_gateway"
    MICRO_EDGE = "micro_edge"


class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class FogNode:
    node_id: str
    node_type: NodeType
    location: Tuple[float, float]
    resources: Dict[str, float]
    connected_devices: List[str] = field(default_factory=list)
    status: str = "active"
    last_heartbeat: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FogTask:
    task_id: str
    task_type: str
    data_size: float
    computation_req: float
    latency_req: float
    priority: TaskPriority
    source_node: str
    created_at: float = field(default_factory=time.time)


@dataclass
class ServicePlacement:
    service_id: str
    node_id: str
    replicas: int
    resource_allocation: Dict[str, float]


class FogComputingOrchestrator:
    def __init__(self, fog_domain: str):
        self.fog_domain = fog_domain
        self.nodes: Dict[str, FogNode] = {}
        self.tasks: List[FogTask] = []
        self.service_placements: Dict[str, ServicePlacement] = {}
        self.task_queue: List[FogTask] = []
        self.network_links: Dict[str, Dict] = {}
        self._initialize_topology()
        self._initialize_services()

    def _initialize_topology(self):
        self.nodes = {
            "cloud-region-1": FogNode(
                node_id="cloud-region-1",
                node_type=NodeType.CLOUD,
                location=(40.7128, -74.0060),
                resources={"compute": 1000, "storage": 10000, "bandwidth": 1000},
                status="active"
            ),
            "fog-cluster-1": FogNode(
                node_id="fog-cluster-1",
                node_type=NodeType.FOG,
                location=(40.7200, -74.0100),
                resources={"compute": 100, "storage": 500, "bandwidth": 100},
                connected_devices=["edge-1", "edge-2", "edge-3"],
                status="active"
            ),
            "fog-cluster-2": FogNode(
                node_id="fog-cluster-2",
                node_type=NodeType.FOG,
                location=(40.7050, -74.0150),
                resources={"compute": 80, "storage": 400, "bandwidth": 80},
                connected_devices=["edge-4", "edge-5"],
                status="active"
            ),
            "edge-1": FogNode(
                node_id="edge-1",
                node_type=NodeType.EDGE,
                location=(40.7180, -74.0080),
                resources={"compute": 10, "storage": 50, "bandwidth": 10},
                status="active"
            ),
            "edge-2": FogNode(
                node_id="edge-2",
                node_type=NodeType.EDGE,
                location=(40.7220, -74.0120),
                resources={"compute": 8, "storage": 40, "bandwidth": 8},
                status="active"
            )
        }
        self.network_links = {
            "edge-1-fog-1": {"latency_ms": 2, "bandwidth_mbps": 100},
            "edge-2-fog-1": {"latency_ms": 3, "bandwidth_mbps": 80},
            "fog-1-cloud": {"latency_ms": 15, "bandwidth_mbps": 500},
            "fog-2-cloud": {"latency_ms": 20, "bandwidth_mbps": 400}
        }

    def _initialize_services(self):
        self.service_placements = {
            "video-analysis": ServicePlacement(
                service_id="video-analysis",
                node_id="fog-cluster-1",
                replicas=2,
                resource_allocation={"compute": 20, "storage": 100}
            ),
            "device-management": ServicePlacement(
                service_id="device-management",
                node_id="fog-cluster-2",
                replicas=1,
                resource_allocation={"compute": 5, "storage": 20}
            )
        }

    def add_node(self, node: FogNode) -> bool:
        if node.node_id in self.nodes:
            return False
        self.nodes[node.node_id] = node
        return True

    def submit_task(self, task: FogTask) -> Dict:
        self.tasks.append(task)
        self.task_queue.append(task)
        placement = self._offload_task(task)
        return {"task_id": task.task_id, "assigned_node": placement["node_id"]}

    def _offload_task(self, task: FogTask) -> Dict:
        candidates = self._find_suitable_nodes(task)
        if not candidates:
            return {"node_id": "cloud-region-1", "reason": "fallback"}
        best = min(candidates, key=lambda n: n.get("cost", float('inf')))
        return {"node_id": best["node_id"], "cost": best.get("cost", 0)}

    def _find_suitable_nodes(self, task: FogTask) -> List[Dict]:
        candidates = []
        for node_id, node in self.nodes.items():
            if node.status != "active":
                continue
            if (node.resources.get("compute", 0) >= task.computation_req and
                node.resources.get("bandwidth", 0) >= task.data_size * 0.1):
                latency = self._estimate_latency(task.source_node, node_id)
                if latency <= task.latency_req:
                    cost = self._calculate_cost(node, task)
                    candidates.append({"node_id": node_id, "cost": cost, "latency": latency})
        return candidates

    def _estimate_latency(self, source: str, destination: str) -> float:
        if source == destination:
            return 1.0
        direct_link = f"{source[:8]}-{destination[:8]}" if len(source) > 8 and len(destination) > 8 else None
        if direct_link and direct_link in self.network_links:
            return self.network_links[direct_link]["latency_ms"]
        return random.uniform(5, 30)

    def _calculate_cost(self, node: FogNode, task: FogTask) -> float:
        compute_cost = task.computation_req * 0.01
        storage_cost = task.data_size * 0.001
        priority_multiplier = 1.0 / task.priority.value
        return (compute_cost + storage_cost) * priority_multiplier

    def deploy_service(self, service_id: str, node_id: str, replicas: int = 1,
                       resources: Dict[str, float] = None) -> Dict:
        if node_id not in self.nodes:
            return {"error": "Node not found"}
        placement = ServicePlacement(
            service_id=service_id,
            node_id=node_id,
            replicas=replicas,
            resource_allocation=resources or {"compute": 10, "storage": 50}
        )
        self.service_placements[service_id] = placement
        return {"status": "deployed", "service_id": service_id, "node_id": node_id}

    def scale_service(self, service_id: str, target_replicas: int) -> Dict:
        if service_id not in self.service_placements:
            return {"error": "Service not found"}
        self.service_placements[service_id].replicas = target_replicas
        return {"service_id": service_id, "new_replicas": target_replicas}

    def get_service_status(self) -> Dict:
        services = {}
        for service_id, placement in self.service_placements.items():
            services[service_id] = {
                "node_id": placement.node_id,
                "replicas": placement.replicas,
                "resources": placement.resource_allocation
            }
        return services

    def route_request(self, request: Dict) -> Dict:
        source = request.get("source", "unknown")
        service = request.get("service", "unknown")
        if service in self.service_placements:
            node_id = self.service_placements[service].node_id
            latency = self._estimate_latency(source, node_id)
            return {"routed_to": node_id, "estimated_latency_ms": latency}
        return {"routed_to": "cloud-region-1", "fallback": True}

    def get_network_topology(self) -> Dict:
        return {
            "nodes": {
                nid: {
                    "type": n.node_type.value,
                    "location": n.location,
                    "resources": n.resources,
                    "status": n.status
                }
                for nid, n in self.nodes.items()
            },
            "links": self.network_links
        }

    def optimize_placement(self, objective: str = "latency") -> Dict:
        if objective == "latency":
            for service_id, placement in self.service_placements.items():
                best_node = self._find_lowest_latency_node(placement.service_id)
                if best_node != placement.node_id:
                    placement.node_id = best_node
        return {"optimized": True, "objective": objective}

    def _find_lowest_latency_node(self, service_id: str) -> str:
        return "fog-cluster-1"

    def get_fog_status(self) -> Dict:
        active_nodes = sum(1 for n in self.nodes.values() if n.status == "active")
        total_compute = sum(n.resources.get("compute", 0) for n in self.nodes.values())
        return {
            "domain": self.fog_domain,
            "nodes": {
                "total": len(self.nodes),
                "active": active_nodes
            },
            "resources": {
                "total_compute": total_compute,
                "total_storage": sum(n.resources.get("storage", 0) for n in self.nodes.values())
            },
            "services": len(self.service_placements),
            "pending_tasks": len(self.task_queue)
        }

    def simulate_workload(self, duration: int = 60) -> Dict:
        start_time = time.time()
        tasks_completed = 0
        tasks_failed = 0
        while time.time() - start_time < duration:
            task = FogTask(
                task_id=f"task-{int(time.time())}",
                task_type=random.choice(["inference", "analytics", "storage"]),
                data_size=random.uniform(0.1, 10.0),
                computation_req=random.uniform(1, 50),
                latency_req=random.uniform(10, 100),
                priority=random.choice(list(TaskPriority)),
                source_node=random.choice(["edge-1", "edge-2"])
            )
            result = self.submit_task(task)
            if result.get("assigned_node"):
                tasks_completed += 1
            else:
                tasks_failed += 1
            time.sleep(0.1)
        return {
            "duration_seconds": duration,
            "tasks_completed": tasks_completed,
            "tasks_failed": tasks_failed,
            "throughput": tasks_completed / duration
        }


class ServiceMeshManager:
    def __init__(self):
        self.services: Dict[str, Dict] = {}
        self.routes: List[Dict] = []
        self.circuit_breakers: Dict[str, Dict] = {}

    def register_service(self, service_id: str, node_id: str, port: int):
        self.services[service_id] = {
            "node_id": node_id,
            "port": port,
            "status": "healthy",
            "last_heartbeat": time.time()
        }

    def add_route(self, service_id: str, destination: str, weight: int = 100):
        self.routes.append({
            "source": service_id,
            "destination": destination,
            "weight": weight
        })

    def enable_circuit_breaker(self, service_id: str, threshold: int = 5, timeout: float = 30.0):
        self.circuit_breakers[service_id] = {
            "threshold": threshold,
            "timeout": timeout,
            "state": "closed"
        }
