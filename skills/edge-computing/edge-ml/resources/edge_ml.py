from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import random
import time
import json


class ModelType(Enum):
    CNN = "cnn"
    TRANSFORMER = "transformer"
    LSTM = "lstm"
    RESNET = "resnet"
    YOLO = "yolo"
    BERT = "bert"


class DeploymentTarget(Enum):
    EDGE_DEVICE = "edge_device"
    GATEWAY = "gateway"
    CLOUD = "cloud"
    HYBRID = "hybrid"


@dataclass
class EdgeModel:
    model_id: str
    name: str
    model_type: ModelType
    input_shape: List[int]
    output_shape: List[int]
    parameters: int
    accuracy: float
    latency_ms: float
    memory_mb: float
    quantized: bool = False
    optimization: str = "none"


@dataclass
class InferenceRequest:
    request_id: str
    model_id: str
    input_data: Any
    timestamp: float
    priority: int = 0
    metadata: Dict[str, Any] = None


@dataclass
class EdgeNode:
    node_id: str
    device_type: str
    capabilities: List[str]
    available_memory: float
    cpu_cores: int
    gpu_available: bool
    power_mode: str = "balanced"
    is_online: bool = True


class EdgeMLManager:
    def __init__(self, edge_id: str):
        self.edge_id = edge_id
        self.models: Dict[str, EdgeModel] = {}
        self.inference_history: List[Dict] = []
        self.edge_nodes: Dict[str, EdgeNode] = {}
        self.model_versions: Dict[str, List[str]] = {}
        self._initialize_models()
        self._initialize_nodes()

    def _initialize_models(self):
        self.models = {
            "object-detector": EdgeModel(
                model_id="object-detector",
                name="YOLOv8n",
                model_type=ModelType.YOLO,
                input_shape=[1, 640, 640, 3],
                output_shape=[1, 8400, 85],
                parameters=3700000,
                accuracy=0.872,
                latency_ms=12.5,
                memory_mb=14.5,
                quantized=True,
                optimization="tensorrt"
            ),
            "image-classifier": EdgeModel(
                model_id="image-classifier",
                name="MobileNetV3",
                model_type=ModelType.CNN,
                input_shape=[1, 224, 224, 3],
                output_shape=[1, 1000],
                parameters=5500000,
                accuracy=0.914,
                latency_ms=5.2,
                memory_mb=21.0,
                quantized=True,
                optimization="tflite"
            ),
            "pose-estimator": EdgeModel(
                model_id="pose-estimator",
                name="MoveNet Lightning",
                model_type=ModelType.CNN,
                input_shape=[1, 192, 192, 3],
                output_shape=[1, 17, 3],
                parameters=2800000,
                accuracy=0.896,
                latency_ms=4.8,
                memory_mb=11.0,
                quantized=True,
                optimization="tflite"
            ),
            "keyword-spotter": EdgeModel(
                model_id="keyword-spotter",
                name="Depthwise Separable CNN",
                model_type=ModelType.CNN,
                input_shape=[1, 16000],
                output_shape=[1, 2],
                parameters=95000,
                accuracy=0.952,
                latency_ms=15.0,
                memory_mb=1.5,
                quantized=True,
                optimization="tflite"
            ),
            "anomaly-detector": EdgeModel(
                model_id="anomaly-detector",
                name="Autoencoder",
                model_type=ModelType.LSTM,
                input_shape=[1, 50, 10],
                output_shape=[1, 50, 10],
                parameters=125000,
                accuracy=0.889,
                latency_ms=8.3,
                memory_mb=5.2,
                quantized=False,
                optimization="onnx"
            )
        }
        self.model_versions = {
            "object-detector": ["v1.0", "v1.1", "v1.2"],
            "image-classifier": ["v2.0", "v2.1"],
            "pose-estimator": ["v1.0"]
        }

    def _initialize_nodes(self):
        self.edge_nodes = {
            "node-gateway-1": EdgeNode(
                node_id="node-gateway-1",
                device_type="NVIDIA Jetson AGX Orin",
                capabilities=["gpu", "tensorrt", "cuda"],
                available_memory=32.0,
                cpu_cores=12,
                gpu_available=True,
                power_mode="maxn"
            ),
            "node-camera-1": EdgeNode(
                node_id="node-camera-1",
                device_type="NVIDIA Jetson Nano",
                capabilities=["gpu", "tflite"],
                available_memory=4.0,
                cpu_cores=4,
                gpu_available=True,
                power_mode="10w"
            ),
            "node-camera-2": EdgeNode(
                node_id="node-camera-2",
                device_type="Google Coral TPU",
                capabilities=["tpu", "edgetpu"],
                available_memory=2.0,
                cpu_cores=4,
                gpu_available=False,
                power_mode="default"
            )
        }

    def run_inference(self, model_id: str, input_data: Any, 
                     target_node: str = None) -> Dict:
        if model_id not in self.models:
            return {"error": "Model not found"}
        model = self.models[model_id]
        node = target_node if target_node and target_node in self.edge_nodes else None
        if not node:
            node = self._select_best_node(model_id)
        start_time = time.time()
        result = {
            "model_id": model_id,
            "model_name": model.name,
            "node_id": node,
            "inference_time_ms": model.latency_ms + random.uniform(-1, 1),
            "output_shape": model.output_shape,
            "timestamp": start_time
        }
        self.inference_history.append({
            **result,
            "input_size": len(str(input_data)) if input_data else 0
        })
        return result

    def _select_best_node(self, model_id: str) -> str:
        if model_id not in self.models:
            return list(self.edge_nodes.keys())[0]
        model = self.models[model_id]
        suitable = [
            n for n in self.edge_nodes.values()
            if n.is_online and 
            (model.gpu_available and n.gpu_available or not model.gpu_available)
        ]
        if suitable:
            return min(suitable, key=lambda n: n.available_memory).node_id
        return list(self.edge_nodes.keys())[0]

    def deploy_model(self, model: EdgeModel, target_node: str) -> Dict:
        if target_node not in self.edge_nodes:
            return {"error": "Node not found"}
        self.models[model.model_id] = model
        if model.model_id not in self.model_versions:
            self.model_versions[model.model_id] = []
        self.model_versions[model.model_id].append(f"v{len(self.model_versions[model.model_id]) + 1}")
        return {
            "status": "deployed",
            "model_id": model.model_id,
            "node_id": target_node,
            "version": self.model_versions[model.model_id][-1]
        }

    def quantize_model(self, model_id: str, precision: str = "int8") -> Dict:
        if model_id not in self.models:
            return {"error": "Model not found"}
        model = self.models[model_id]
        size_reduction = 0.25 if precision == "int8" else 0.5
        return {
            "model_id": model_id,
            "original_size_mb": model.memory_mb,
            "quantized_size_mb": model.memory_mb * size_reduction,
            "precision": precision,
            "accuracy_impact": random.uniform(-0.02, 0.01),
            "speedup": random.uniform(1.5, 2.5)
        }

    def prune_model(self, model_id: str, sparsity: float = 0.3) -> Dict:
        if model_id not in self.models:
            return {"error": "Model not found"}
        model = self.models[model_id]
        return {
            "model_id": model_id,
            "original_parameters": model.parameters,
            "pruned_parameters": int(model.parameters * (1 - sparsity)),
            "sparsity": sparsity,
            "accuracy_impact": random.uniform(-0.03, 0.0),
            "speedup": random.uniform(1.2, 1.8)
        }

    def benchmark_model(self, model_id: str, node_id: str = None) -> Dict:
        if model_id not in self.models:
            return {"error": "Model not found"}
        model = self.models[model_id]
        node = node_id or self._select_best_node(model_id)
        return {
            "model_id": model_id,
            "node_id": node,
            "latency_ms": model.latency_ms,
            "throughput_fps": 1000 / model.latency_ms if model.latency_ms > 0 else 0,
            "memory_mb": model.memory_mb,
            "accuracy": model.accuracy,
            "power_watts": random.uniform(1.5, 5.0) if node and self.edge_nodes.get(node) else None
        }

    def federated_learning_round(self, model_id: str, client_nodes: List[str]) -> Dict:
        if model_id not in self.models:
            return {"error": "Model not found"}
        updates = []
        for node_id in client_nodes:
            updates.append({
                "node_id": node_id,
                "samples_processed": random.randint(100, 1000),
                "learning_rate": 0.01,
                "gradients_norm": random.uniform(0.1, 1.0)
            })
        return {
            "model_id": model_id,
            "round": len(self.model_versions.get(model_id, [])),
            "participating_nodes": len(updates),
            "total_samples": sum(u["samples_processed"] for u in updates),
            "aggregated_update": random.uniform(-0.01, 0.01)
        }

    def get_model_list(self) -> List[Dict]:
        return [
            {
                "model_id": mid,
                "name": m.name,
                "type": m.model_type.value,
                "accuracy": m.accuracy,
                "latency_ms": m.latency_ms,
                "memory_mb": m.memory_mb,
                "quantized": m.quantized
            }
            for mid, m in self.models.items()
        ]

    def get_node_status(self) -> Dict:
        return {
            "total_nodes": len(self.edge_nodes),
            "online_nodes": sum(1 for n in self.edge_nodes.values() if n.is_online),
            "nodes": {
                nid: {
                    "device_type": n.device_type,
                    "memory_available": n.available_memory,
                    "cpu_cores": n.cpu_cores,
                    "gpu_available": n.gpu_available,
                    "power_mode": n.power_mode
                }
                for nid, n in self.edge_nodes.items()
            }
        }

    def get_edge_status(self) -> Dict:
        return {
            "edge_id": self.edge_id,
            "models_deployed": len(self.models),
            "inference_requests": len(self.inference_history),
            "nodes": self.get_node_status()
        }


class OnDeviceTraining:
    def __init__(self):
        self.training_history: List[Dict] = []

    def incremental_train(self, model_id: str, new_data: Any, epochs: int = 5) -> Dict:
        training_time = epochs * random.uniform(10, 30)
        result = {
            "model_id": model_id,
            "epochs": epochs,
            "training_time_seconds": training_time,
            "accuracy_before": random.uniform(0.85, 0.90),
            "accuracy_after": random.uniform(0.88, 0.93),
            "samples_used": random.randint(100, 1000)
        }
        self.training_history.append(result)
        return result

    def adaptive_learning_rate(self, epoch: int, base_lr: float = 0.01) -> float:
        return base_lr * (0.1 ** (epoch // 10))

    def memory_efficient_optimizer(self, model_size: int) -> Dict:
        return {
            "optimizer": "Adafactor",
            "memory_savings": "40%",
            "gradient_accumulation_steps": max(1, model_size // 1000000)
        }
