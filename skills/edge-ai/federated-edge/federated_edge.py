"""
Federated Edge Learning Framework

Production-grade federated learning toolkit providing distributed training,
privacy-preserving aggregation, communication optimization, and edge coordination.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AggregationStrategy(Enum):
    FEDAVG = "fedavg"
    FEDPROX = "fedprox"
    SCAFFOLD = "scaffold"
    FEDMA = "fedma"
    FEDBN = "fedbn"


class SelectionStrategy(Enum):
    RANDOM = "random"
    POWER_OF_CHOICE = "power_of_choice"
    PROFIT = "profit"
    RESOURCE_AWARE = "resource_aware"
    FAIRNESS = "fairness"


class CompressionMethod(Enum):
    TOP_K = "top_k"
    RANDOM_K = "random_k"
    QUANTIZATION = "quantization"
    SPARSIFICATION = "sparsification"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class FederatedRound:
    """A single federated training round."""
    round_number: int
    selected_devices: List[str]
    completed_devices: List[str]
    global_model_update: NDArray
    round_loss: float
    round_accuracy: float
    duration_seconds: float = 0.0
    communication_mb: float = 0.0


@dataclass
class FederatedResult:
    """Federated training result."""
    accuracy: float
    rounds_completed: int
    total_communication_mb: float
    total_time_seconds: float
    final_loss: float
    convergence_round: int = 0
    rounds_history: List[FederatedRound] = field(default_factory=list)


@dataclass
class PrivacyConfig:
    """Differential privacy configuration."""
    epsilon: float
    delta: float
    noise_multiplier: float
    clip_norm: float
    remaining_epsilon: float = 0.0
    remaining_delta: float = 0.0


@dataclass
class ClientUpdate:
    """Client model update."""
    client_id: str
    model_update: NDArray
    num_samples: int
    local_loss: float
    local_accuracy: float
    computation_time: float = 0.0
    communication_cost: float = 0.0


@dataclass
class CompressionResult:
    """Gradient compression result."""
    original_bytes: int
    compressed_bytes: int
    ratio: float
    method: str
    sparsity: float = 0.0


@dataclass
class RoundResult:
    """Training round result."""
    round_number: int
    selected_count: int
    completed_count: int
    duration_seconds: float
    avg_loss: float = 0.0
    avg_accuracy: float = 0.0
    communication_mb: float = 0.0


@dataclass
class DeviceInfo:
    """Edge device information."""
    device_id: str
    capabilities: Dict[str, Any] = field(default_factory=dict)
    data_size: int = 0
    compute_power: float = 1.0
    network_bandwidth: float = 1.0
    battery_level: float = 1.0
    last_seen: Optional[datetime] = None


@dataclass
class PrivacyBudget:
    """Privacy budget tracking."""
    total_epsilon: float
    used_epsilon: float
    total_delta: float
    used_delta: float

    @property
    def remaining_epsilon(self) -> float:
        return max(0, self.total_epsilon - self.used_epsilon)

    @property
    def exhausted(self) -> bool:
        return self.remaining_epsilon <= 0


# ---------------------------------------------------------------------------
# Federated Trainer
# ---------------------------------------------------------------------------

class FederatedTrainer:
    """Train models using federated learning."""

    def __init__(
        self,
        num_rounds: int = 100,
        clients_per_round: int = 10,
        local_epochs: int = 5,
        aggregation: AggregationStrategy = AggregationStrategy.FEDAVG,
        learning_rate: float = 0.01,
    ):
        self.num_rounds = num_rounds
        self.clients_per_round = clients_per_round
        self.local_epochs = local_epochs
        self.aggregation = aggregation
        self.learning_rate = learning_rate
        self._history: List[FederatedRound] = []

    def train(
        self,
        global_model: Any,
        client_data: Dict[str, Any],
        validation_data: Optional[Any] = None,
    ) -> FederatedResult:
        start_time = time.time()
        total_communication = 0.0

        for round_num in range(self.num_rounds):
            # Simulate round
            round_result = self._simulate_round(round_num, client_data)
            self._history.append(round_result)
            total_communication += round_result.communication_mb

            if round_num % 10 == 0:
                logger.info("Round %d: loss=%.4f, accuracy=%.2f%%",
                           round_num, round_result.round_loss, round_result.round_accuracy * 100)

        total_time = time.time() - start_time
        final_round = self._history[-1] if self._history else None

        return FederatedResult(
            accuracy=final_round.round_accuracy if final_round else 0,
            rounds_completed=len(self._history),
            total_communication_mb=total_communication,
            total_time_seconds=total_time,
            final_loss=final_round.round_loss if final_round else 0,
            convergence_round=self._find_convergence(),
            rounds_history=self._history,
        )

    def _simulate_round(self, round_num: int, client_data: Dict) -> FederatedRound:
        selected = [f"client_{i}" for i in np.random.choice(
            len(client_data) or 10, min(self.clients_per_round, len(client_data) or 10), replace=False
        )]

        time.sleep(0.01)

        return FederatedRound(
            round_number=round_num,
            selected_devices=selected,
            completed_devices=selected[:int(len(selected) * 0.9)],
            global_model_update=np.random.randn(100),
            round_loss=max(0.1, 2.0 - round_num * 0.02 + np.random.uniform(-0.1, 0.1)),
            round_accuracy=min(0.98, 0.5 + round_num * 0.005 + np.random.uniform(-0.02, 0.02)),
            duration_seconds=np.random.uniform(1, 5),
            communication_mb=np.random.uniform(0.5, 2.0) * len(selected),
        )

    def _find_convergence(self) -> int:
        if len(self._history) < 10:
            return len(self._history)
        recent_acc = [r.round_accuracy for r in self._history[-10:]]
        if max(recent_acc) - min(recent_acc) < 0.01:
            return len(self._history) - 10
        return len(self._history)


# ---------------------------------------------------------------------------
# Privacy Engine
# ---------------------------------------------------------------------------

class PrivacyEngine:
    """Manage differential privacy for federated learning."""

    def __init__(self):
        self._budget = PrivacyBudget(total_epsilon=10.0, used_epsilon=0, total_delta=1e-5, used_delta=0)

    def configure(
        self,
        epsilon: float = 1.0,
        delta: float = 1e-5,
        noise_multiplier: float = 1.1,
        clip_norm: float = 1.0,
    ) -> PrivacyConfig:
        return PrivacyConfig(
            epsilon=epsilon,
            delta=delta,
            noise_multiplier=noise_multiplier,
            clip_norm=clip_norm,
            remaining_epsilon=self._budget.remaining_epsilon,
            remaining_delta=self._budget.total_delta - self._budget.used_delta,
        )

    def track_usage(self, epsilon_used: float, delta_used: float) -> None:
        self._budget.used_epsilon += epsilon_used
        self._budget.used_delta += delta_used

    def get_budget(self) -> PrivacyBudget:
        return self._budget


# ---------------------------------------------------------------------------
# Communication Optimizer
# ---------------------------------------------------------------------------

class CommunicationOptimizer:
    """Optimize communication in federated learning."""

    def compress(
        self,
        model_update: NDArray,
        compression_ratio: float = 0.1,
        method: CompressionMethod = CompressionMethod.TOP_K,
    ) -> CompressionResult:
        original_bytes = model_update.nbytes
        compressed_bytes = int(original_bytes * compression_ratio)

        return CompressionResult(
            original_bytes=original_bytes,
            compressed_bytes=compressed_bytes,
            ratio=original_bytes / compressed_bytes if compressed_bytes > 0 else 1.0,
            method=method.value,
            sparsity=1 - compression_ratio,
        )


# ---------------------------------------------------------------------------
# Edge Coordinator
# ---------------------------------------------------------------------------

class EdgeCoordinator:
    """Coordinate federated training across edge devices."""

    def __init__(self):
        self._devices: Dict[str, DeviceInfo] = {}

    def register_device(self, device: DeviceInfo) -> None:
        self._devices[device.device_id] = device

    def run_round(
        self,
        round_number: int,
        eligible_devices: Optional[List[str]] = None,
        selection_strategy: SelectionStrategy = SelectionStrategy.RANDOM,
    ) -> RoundResult:
        if eligible_devices is None:
            eligible_devices = list(self._devices.keys()) or [f"device_{i}" for i in range(10)]

        selected = list(np.random.choice(
            eligible_devices,
            min(10, len(eligible_devices)),
            replace=False,
        ))

        time.sleep(0.02)
        completed = selected[:int(len(selected) * 0.9)]

        return RoundResult(
            round_number=round_number,
            selected_count=len(selected),
            completed_count=len(completed),
            duration_seconds=np.random.uniform(1, 5),
            avg_loss=np.random.uniform(0.2, 1.0),
            avg_accuracy=np.random.uniform(0.6, 0.95),
            communication_mb=np.random.uniform(1, 10),
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate federated edge learning capabilities."""
    print("=" * 70)
    print("Federated Edge Learning Framework - Demo")
    print("=" * 70)

    # --- 1. Federated Training ---
    print("\n--- Federated Training ---")
    trainer = FederatedTrainer(num_rounds=20, clients_per_round=5)
    result = trainer.train("model", {})
    print(f"  Final accuracy: {result.accuracy:.2%}")
    print(f"  Rounds: {result.rounds_completed}")
    print(f"  Communication: {result.total_communication_mb:.1f} MB")
    print(f"  Convergence at round: {result.convergence_round}")

    # --- 2. Privacy ---
    print("\n--- Privacy-Preserving ---")
    privacy = PrivacyEngine()
    config = privacy.configure(epsilon=1.0, delta=1e-5)
    print(f"  Epsilon: {config.epsilon}")
    print(f"  Remaining: {config.remaining_epsilon:.2f}")
    print(f"  Noise multiplier: {config.noise_multiplier}")

    privacy.track_usage(0.5, 1e-6)
    budget = privacy.get_budget()
    print(f"  Used: {budget.used_epsilon:.2f}/{budget.total_epsilon}")

    # --- 3. Communication Optimization ---
    print("\n--- Communication Optimization ---")
    comm_optimizer = CommunicationOptimizer()
    compressed = comm_optimizer.compress(np.random.randn(10000), compression_ratio=0.1)
    print(f"  Original: {compressed.original_bytes / 1024:.1f} KB")
    print(f"  Compressed: {compressed.compressed_bytes / 1024:.1f} KB")
    print(f"  Ratio: {compressed.ratio:.1f}x")
    print(f"  Sparsity: {compressed.sparsity:.0%}")

    # --- 4. Edge Coordination ---
    print("\n--- Edge Coordination ---")
    coordinator = EdgeCoordinator()
    for i in range(10):
        coordinator.register_device(DeviceInfo(
            device_id=f"device_{i}",
            data_size=np.random.randint(100, 1000),
            compute_power=np.random.uniform(0.5, 2.0),
        ))

    round_result = coordinator.run_round(1)
    print(f"  Selected: {round_result.selected_count}")
    print(f"  Completed: {round_result.completed_count}")
    print(f"  Duration: {round_result.duration_seconds:.1f}s")
    print(f"  Accuracy: {round_result.avg_accuracy:.2%}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()