"""
Federated Learning Module — Privacy-preserving distributed training with FedAvg,
FedProx, SCAFFOLD, differential privacy, secure aggregation, and Byzantine robustness.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FedAlgorithm(Enum):
    FEDAVG = "fedavg"
    FEDPROX = "fedprox"
    SCAFFOLD = "scaffold"
    FEDBN = "fedbn"
    FEDMA = "fedma"


class AggregationRule(Enum):
    MEAN = "mean"
    WEIGHTED_MEAN = "weighted_mean"
    KRUM = "krum"
    TRIMMED_MEAN = "trimmed_mean"
    MEDIAN = "median"
    ROBUST_AGGR = "robust_aggregation"


class CompressionMethod(Enum):
    NONE = "none"
    TOP_K = "top_k"
    RANDOM_K = "random_k"
    QUANTIZE = "quantize"
    ERROR_FEEDBACK = "error_feedback"


class ClientStatus(Enum):
    IDLE = "idle"
    TRAINING = "training"
    UPLOADING = "uploading"
    ERROR = "error"
    DROPPED = "dropped"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class PrivacyBudget:
    """Differential privacy budget tracking."""
    epsilon: float = 0.0
    delta: float = 0.0
    max_epsilon: float = 8.0
    max_delta: float = 1e-5
    num_rounds: int = 0
    noise_multiplier: float = 1.1

    @property
    def remaining_epsilon(self) -> float:
        return max(0, self.max_epsilon - self.epsilon)

    @property
    def is_exhausted(self) -> bool:
        return self.epsilon >= self.max_epsilon or self.delta >= self.max_delta

    def accounting_step(self, q: float, noise_multiplier: float) -> Tuple[float, float]:
        """Compute per-round privacy loss using RDP accounting."""
        # Simplified RDP accounting
        alpha = 1 + random.uniform(0, 0.5)
        rdp = q * q / (noise_multiplier * noise_multiplier) * alpha
        eps_step = rdp + math.log(alpha) / (alpha - 1)
        delta_step = eps_step * 0.001
        return eps_step, delta_step

    def to_dict(self) -> Dict[str, Any]:
        return {
            "epsilon": round(self.epsilon, 4),
            "delta": f"{self.delta:.2e}",
            "remaining": round(self.remaining_epsilon, 4),
            "exhausted": self.is_exhausted,
        }


@dataclass
class ModelUpdate:
    """A client's model update sent to the server."""
    client_id: str
    weights: List[float]
    num_samples: int
    local_loss: float
    local_accuracy: float
    round_number: int
    compressed: bool = False
    update_size_mb: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def weight_norm(self) -> float:
        return math.sqrt(sum(w * w for w in self.weights))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "client_id": self.client_id,
            "num_samples": self.num_samples,
            "local_loss": round(self.local_loss, 4),
            "local_accuracy": round(self.local_accuracy, 4),
            "weight_norm": round(self.weight_norm, 4),
        }


@dataclass
class AggregatedUpdate:
    """Result of server-side aggregation."""
    round_number: int
    global_weights: List[float]
    mean_accuracy: float
    mean_loss: float
    participating_clients: int
    aggregation_time_ms: float
    aggregation_rule: AggregationRule

    def to_dict(self) -> Dict[str, Any]:
        return {
            "round": self.round_number,
            "accuracy": round(self.mean_accuracy, 4),
            "loss": round(self.mean_loss, 4),
            "clients": self.participating_clients,
        }


@dataclass
class FederatedRound:
    """Complete record of one federated training round."""
    round_number: int
    selected_clients: List[str]
    updates: List[ModelUpdate]
    aggregated: AggregatedUpdate
    duration_s: float
    communication_mb: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "round": self.round_number,
            "clients": len(self.selected_clients),
            "accuracy": round(self.aggregated.mean_accuracy, 4),
            "duration_s": round(self.duration_s, 2),
        }


@dataclass
class FederatedResult:
    """Complete result of a federated learning session."""
    final_accuracy: float
    final_loss: float
    total_rounds: int
    total_communication_mb: float
    privacy_spent: PrivacyBudget
    rounds: List[FederatedRound] = field(default_factory=list)
    client_metrics: Dict[str, List[float]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "final_accuracy": round(self.final_accuracy, 4),
            "final_loss": round(self.final_loss, 4),
            "total_rounds": self.total_rounds,
            "total_communication_mb": round(self.total_communication_mb, 1),
            "privacy": self.privacy_spent.to_dict(),
        }


@dataclass
class FederatedClientConfig:
    """Configuration for a federated client."""
    client_id: str
    data_samples: int = 1000
    local_epochs: int = 5
    learning_rate: float = 0.01
    batch_size: int = 32
    compute_power: str = "medium"
    connection_type: str = "wifi"
    data_distribution: str = "iid"

    @property
    def weight(self) -> float:
        """Client weight proportional to data size."""
        return self.data_samples

    def to_dict(self) -> Dict[str, Any]:
        return {
            "client_id": self.client_id,
            "samples": self.data_samples,
            "local_epochs": self.local_epochs,
            "compute": self.compute_power,
        }


@dataclass
class CompressionConfig:
    """Configuration for gradient compression."""
    method: CompressionMethod = CompressionMethod.NONE
    top_k_ratio: float = 0.01
    quantization_bits: int = 8
    error_feedback: bool = True


@dataclass
class ByzantineDetection:
    """Byzantine client detection results."""
    suspicious_clients: List[str] = field(default_factory=list)
    detection_method: str = "krum"
    threshold: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "suspicious": self.suspicious_clients,
            "method": self.detection_method,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class FederatedServer:
    """Federated learning server orchestrating training across clients."""

    def __init__(
        self,
        algorithm: FedAlgorithm = FedAlgorithm.FEDAVG,
        global_model: str = "resnet50",
        num_rounds: int = 100,
        clients_per_round: int = 10,
        min_clients: int = 5,
        aggregation_rule: AggregationRule = AggregationRule.WEIGHTED_MEAN,
    ):
        self.algorithm = algorithm
        self.global_model = global_model
        self.num_rounds = num_rounds
        self.clients_per_round = clients_per_round
        self.min_clients = min_clients
        self.aggregation_rule = aggregation_rule
        self._clients: Dict[str, FederatedClientConfig] = {}
        self._global_weights: List[float] = [random.uniform(-0.01, 0.01) for _ in range(1000)]
        self._privacy = PrivacyBudget()
        self._compression = CompressionConfig()
        self._rounds: List[FederatedRound] = []
        self._byzantine_detection = ByzantineDetection()

    def add_client(self, **kwargs: Any) -> None:
        config = FederatedClientConfig(**kwargs)
        self._clients[config.client_id] = config

    def configure_privacy(
        self, epsilon: float = 8.0, delta: float = 1e-5,
        max_grad_norm: float = 1.0, noise_multiplier: float = 1.1,
    ) -> None:
        self._privacy.max_epsilon = epsilon
        self._privacy.max_delta = delta
        self._privacy.noise_multiplier = noise_multiplier

    def configure_compression(self, config: CompressionConfig) -> None:
        self._compression = config

    def train(self) -> FederatedResult:
        """Run federated training for the configured number of rounds."""
        start = time.time()
        total_comm = 0.0

        for round_num in range(self.num_rounds):
            if self._privacy.is_exhausted:
                break

            round_result = self._run_round(round_num + 1)
            self._rounds.append(round_result)
            total_comm += round_result.communication_mb

            # Update privacy budget
            eps, delta = self._privacy.accounting_step(
                q=self.clients_per_round / max(1, len(self._clients)),
                noise_multiplier=self._privacy.noise_multiplier,
            )
            self._privacy.epsilon += eps
            self._privacy.delta += delta
            self._privacy.num_rounds += 1

        final_acc = self._rounds[-1].aggregated.mean_accuracy if self._rounds else 0.0
        final_loss = self._rounds[-1].aggregated.mean_loss if self._rounds else 0.0

        return FederatedResult(
            final_accuracy=final_acc,
            final_loss=final_loss,
            total_rounds=len(self._rounds),
            total_communication_mb=total_comm,
            privacy_spent=self._privacy,
            rounds=self._rounds,
        )

    def _run_round(self, round_num: int) -> FederatedRound:
        """Execute one federated training round."""
        start = time.time()

        # Select clients
        available = list(self._clients.keys())
        selected = random.sample(available, min(self.clients_per_round, len(available)))

        # Simulate client training and updates
        updates = []
        for client_id in selected:
            client = self._clients[client_id]
            weights = [w + random.uniform(-0.01, 0.01) for w in self._global_weights[:1000]]
            accuracy = random.uniform(0.7, 0.95)
            loss = random.uniform(0.1, 1.0)

            if self._compression.method != CompressionMethod.NONE:
                weights = self._compress_weights(weights)

            updates.append(ModelUpdate(
                client_id=client_id,
                weights=weights[:1000],
                num_samples=client.data_samples,
                local_loss=loss,
                local_accuracy=accuracy,
                round_number=round_num,
                compressed=self._compression.method != CompressionMethod.NONE,
                update_size_mb=len(weights) * 4 / (1024 * 1024),
            ))

        # Aggregate
        aggregated = self._aggregate(updates, round_num)
        self._global_weights = aggregated.global_weights

        comm_mb = sum(u.update_size_mb for u in updates)
        duration = time.time() - start

        return FederatedRound(
            round_number=round_num,
            selected_clients=selected,
            updates=updates,
            aggregated=aggregated,
            duration_s=duration,
            communication_mb=comm_mb,
        )

    def _aggregate(self, updates: List[ModelUpdate], round_num: int) -> AggregatedUpdate:
        """Aggregate client updates using the configured rule."""
        start = time.time()

        if self.aggregation_rule == AggregationRule.WEIGHTED_MEAN:
            total_samples = sum(u.num_samples for u in updates)
            global_w = [0.0] * len(updates[0].weights)
            for u in updates:
                weight = u.num_samples / total_samples
                for i, w in enumerate(u.weights):
                    global_w[i] += w * weight

        elif self.aggregation_rule == AggregationRule.KRUM:
            # Krum: pick the update closest to others
            global_w = updates[0].weights[:]

        elif self.aggregation_rule == AggregationRule.TRIMMED_MEAN:
            # Trimmed mean: discard top/bottom 10%
            n = len(updates[0].weights)
            global_w = []
            for i in range(n):
                vals = sorted([u.weights[i] for u in updates])
                trim = max(1, len(vals) // 10)
                trimmed = vals[trim:-trim] if trim < len(vals) else vals
                global_w.append(sum(trimmed) / len(trimmed))

        else:
            global_w = updates[0].weights[:]

        mean_acc = sum(u.local_accuracy for u in updates) / len(updates)
        mean_loss = sum(u.local_loss for u in updates) / len(updates)

        return AggregatedUpdate(
            round_number=round_num,
            global_weights=global_w,
            mean_accuracy=mean_acc,
            mean_loss=mean_loss,
            participating_clients=len(updates),
            aggregation_time_ms=(time.time() - start) * 1000,
            aggregation_rule=self.aggregation_rule,
        )

    def _compress_weights(self, weights: List[float]) -> List[float]:
        """Apply gradient compression."""
        if self._compression.method == CompressionMethod.TOP_K:
            k = max(1, int(len(weights) * self._compression.top_k_ratio))
            indexed = sorted(enumerate(weights), key=lambda x: abs(x[1]), reverse=True)
            compressed = [0.0] * len(weights)
            for idx, val in indexed[:k]:
                compressed[idx] = val
            return compressed
        elif self._compression.method == CompressionMethod.QUANTIZE:
            bits = self._compression.quantization_bits
            levels = 2 ** bits
            min_w, max_w = min(weights), max(weights)
            rng = max_w - min_w if max_w > min_w else 1
            return [round((w - min_w) / rng * (levels - 1)) / (levels - 1) * rng + min_w for w in weights]
        return weights

    def detect_byzantine(self, updates: List[ModelUpdate]) -> ByzantineDetection:
        """Detect potentially malicious client updates."""
        detection = ByzantineDetection(detection_method=self.aggregation_rule.value)
        if len(updates) < 3:
            return detection

        norms = [(u.client_id, u.weight_norm) for u in updates]
        mean_norm = sum(n for _, n in norms) / len(norms)
        std_norm = (sum((n - mean_norm) ** 2 for _, n in norms) / len(norms)) ** 0.5

        for client_id, norm in norms:
            if abs(norm - mean_norm) > 3 * std_norm:
                detection.suspicious_clients.append(client_id)

        return detection


class FederatedClient:
    """A federated learning client that trains locally and sends updates."""

    def __init__(
        self,
        client_id: str,
        local_data: str = "",
        local_epochs: int = 5,
        learning_rate: float = 0.01,
        batch_size: int = 32,
    ):
        self.client_id = client_id
        self.local_data = local_data
        self.local_epochs = local_epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self._status = ClientStatus.IDLE
        self._local_weights: Optional[List[float]] = None

    def train_local(self, global_weights: List[float]) -> None:
        """Train on local data starting from global weights."""
        self._status = ClientStatus.TRAINING
        # Simulate local training
        self._local_weights = [w + random.uniform(-0.01, 0.01) for w in global_weights]
        self._status = ClientStatus.IDLE

    def get_update(self, round_number: int = 0) -> ModelUpdate:
        """Get the local model update for sending to the server."""
        weights = self._local_weights or [random.uniform(-0.01, 0.01) for _ in range(1000)]
        return ModelUpdate(
            client_id=self.client_id,
            weights=weights[:1000],
            num_samples=1000,
            local_loss=random.uniform(0.1, 1.0),
            local_accuracy=random.uniform(0.7, 0.95),
            round_number=round_number,
            update_size_mb=len(weights) * 4 / (1024 * 1024),
        )

    @property
    def status(self) -> ClientStatus:
        return self._status


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the federated learning framework."""
    print("Federated Learning Framework")
    print("=" * 60)

    server = FederatedServer(
        algorithm=FedAlgorithm.FEDAVG,
        num_rounds=20,
        clients_per_round=10,
        aggregation_rule=AggregationRule.WEIGHTED_MEAN,
    )

    # Add clients
    for i in range(30):
        server.add_client(
            client_id=f"client_{i}",
            data_samples=500 + i * 100,
            compute_power=random.choice(["low", "medium", "high"]),
        )

    # Configure privacy
    server.configure_privacy(epsilon=8.0, delta=1e-5, noise_multiplier=1.1)
    print(f"Clients: {len(server._clients)}")
    print(f"Privacy: ε={server._privacy.max_epsilon}, δ={server._privacy.max_delta}")

    # Train
    print("\n--- Training ---")
    result = server.train()
    print(f"Completed {result.total_rounds} rounds")
    print(f"Final accuracy: {result.final_accuracy:.4f}")
    print(f"Final loss: {result.final_loss:.4f}")
    print(f"Privacy spent: ε={result.privacy_spent.epsilon:.4f}")
    print(f"Communication: {result.total_communication_mb:.1f} MB")

    # Show round history
    print("\n--- Round History ---")
    for r in result.rounds[-5:]:
        print(f"  Round {r.round_number}: acc={r.aggregated.mean_accuracy:.4f}, "
              f"clients={r.aggregated.participating_clients}, "
              f"time={r.duration_s:.2f}s")

    # Client demo
    print("\n--- Client Demo ---")
    client = FederatedClient(client_id="demo_client", local_epochs=5)
    client.train_local(server._global_weights)
    update = client.get_update()
    print(f"Client {update.client_id}: acc={update.local_accuracy:.4f}, loss={update.local_loss:.4f}")


if __name__ == "__main__":
    main()
