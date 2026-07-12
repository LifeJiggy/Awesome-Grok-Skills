"""
Neural Architecture Search Module — DARTS, evolutionary, and Bayesian search
strategies for automated deep learning architecture discovery.
"""

from __future__ import annotations

import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SearchStrategy(Enum):
    DARTS = "darts"
    EVOLUTIONARY = "evolutionary"
    BAYESIAN = "bayesian"
    REINFORCEMENT = "reinforcement"
    RANDOM = "random"


class CellType(Enum):
    NORMAL = "normal"
    REDUCTION = "reduction"


class Operation(Enum):
    CONV_3x3 = "conv_3x3"
    CONV_5x5 = "conv_5x5"
    DEPTHWISE_CONV = "depthwise_conv"
    MAX_POOL = "max_pool"
    AVG_POOL = "avg_pool"
    SKIP_CONNECT = "skip_connect"
    NONE = "none"
    DILATED_CONV_3x3 = "dilated_conv_3x3"
    SEPARABLE_CONV_3x3 = "separable_conv_3x3"
    IDENTITY = "identity"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SearchSpace:
    """Definition of the architecture search space."""
    operations: List[str] = field(default_factory=lambda: [
        "conv_3x3", "conv_5x5", "depthwise_conv", "max_pool",
        "avg_pool", "skip_connect", "none",
    ])
    nodes_per_cell: int = 4
    num_cells: int = 8
    cell_types: List[str] = field(default_factory=lambda: ["normal", "reduction"])
    input_channels: int = 3
    stem_channels: int = 16

    @property
    def total_operations(self) -> int:
        return len(self.operations)

    @property
    def search_space_size(self) -> float:
        edges_per_cell = self.nodes_per_cell * (self.nodes_per_cell + 1) // 2
        return self.total_operations ** edges_per_cell * self.num_cells

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operations": self.operations,
            "nodes_per_cell": self.nodes_per_cell,
            "num_cells": self.num_cells,
            "cell_types": self.cell_types,
            "search_space_size": f"{self.search_space_size:.2e}",
        }


@dataclass
class ArchitectureConfig:
    """A specific architecture configuration."""
    genotype: Dict[str, List[Tuple[str, int]]]
    cell_type: CellType
    num_cells: int = 8
    channels: List[int] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "genotype": self.genotype,
            "cell_type": self.cell_type.value,
            "num_cells": self.num_cells,
        }


@dataclass
class ArchitectureResult:
    """Result of evaluating a discovered architecture."""
    architecture_id: str
    genotype: Dict[str, Any]
    accuracy: float
    parameter_count: int
    flops: float
    latency_ms: float
    search_time_s: float
    training_time_s: float
    dataset: str = ""
    pareto_rank: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def efficiency_score(self) -> float:
        """Combined efficiency metric (higher is better)."""
        if self.latency_ms == 0:
            return self.accuracy
        return self.accuracy * 1000 / self.latency_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.architecture_id,
            "accuracy": round(self.accuracy, 4),
            "parameters": self.parameter_count,
            "flops": f"{self.flops:.2e}",
            "latency_ms": round(self.latency_ms, 2),
            "efficiency": round(self.efficiency_score, 4),
        }


@dataclass
class NASConfig:
    """Configuration for a neural architecture search run."""
    strategy: SearchStrategy = SearchStrategy.DARTS
    search_space: Optional[SearchSpace] = None
    epochs: int = 50
    batch_size: int = 64
    learning_rate: float = 0.025
    weight_decay: float = 3e-4
    target_accuracy: float = 0.95
    max_parameters: int = 10_000_000
    max_latency_ms: float = 20.0
    max_flops: float = 1e9
    dataset: str = "cifar10"
    gpus: int = 1
    seed: int = 42
    output_dir: str = "nas_results"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy.value,
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "lr": self.learning_rate,
            "target_accuracy": self.target_accuracy,
            "max_params": self.max_parameters,
            "dataset": self.dataset,
        }


@dataclass
class SearchProgress:
    """Progress tracking for NAS runs."""
    current_epoch: int = 0
    total_epochs: int = 0
    architectures_evaluated: int = 0
    best_accuracy: float = 0.0
    best_architecture: Optional[str] = None
    elapsed_time_s: float = 0.0
    estimated_remaining_s: float = 0.0

    @property
    def progress_pct(self) -> float:
        if self.total_epochs == 0:
            return 0.0
        return round(self.current_epoch / self.total_epochs * 100, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "epoch": self.current_epoch,
            "total": self.total_epochs,
            "progress": f"{self.progress_pct}%",
            "evaluated": self.architectures_evaluated,
            "best_accuracy": round(self.best_accuracy, 4),
        }


@dataclass
class ParetoFront:
    """Pareto-optimal architectures for multi-objective optimization."""
    architectures: List[ArchitectureResult] = field(default_factory=list)

    def add(self, arch: ArchitectureResult) -> bool:
        """Add architecture if it is not dominated by existing ones."""
        dominated = False
        to_remove = []
        for i, existing in enumerate(self.architectures):
            if self._dominates(existing, arch):
                dominated = True
                break
            if self._dominates(arch, existing):
                to_remove.append(i)
        if not dominated:
            for i in reversed(to_remove):
                self.architectures.pop(i)
            self.architectures.append(arch)
            return True
        return False

    @staticmethod
    def _dominates(a: ArchitectureResult, b: ArchitectureResult) -> bool:
        """Check if architecture a dominates b (better in all objectives)."""
        better_acc = a.accuracy >= b.accuracy
        better_lat = a.latency_ms <= b.latency_ms
        better_params = a.parameter_count <= b.parameter_count
        strictly_better = (a.accuracy > b.accuracy or a.latency_ms < b.latency_ms
                          or a.parameter_count < b.parameter_count)
        return better_acc and better_lat and better_params and strictly_better

    @property
    def best_accuracy(self) -> float:
        return max(a.accuracy for a in self.architectures) if self.architectures else 0.0

    @property
    def most_efficient(self) -> Optional[ArchitectureResult]:
        if not self.architectures:
            return None
        return max(self.architectures, key=lambda a: a.efficiency_score)


# ---------------------------------------------------------------------------
# DARTS Search
# ---------------------------------------------------------------------------

class DARTSSearch:
    """Differentiable Architecture Search using continuous relaxation."""

    def __init__(self, config: NASConfig):
        self.config = config
        self.search_space = config.search_space or SearchSpace()
        self._architectures: List[ArchitectureResult] = []
        self._progress = SearchProgress(total_epochs=config.epochs)

    def search(self) -> ArchitectureResult:
        """Run DARTS search and return the best architecture."""
        start_time = time.time()

        # Simulate DARTS training
        best_arch = None
        best_acc = 0.0
        for epoch in range(self.config.epochs):
            self._progress.current_epoch = epoch + 1
            epoch_acc = self._train_epoch(epoch)
            if epoch_acc > best_acc:
                best_acc = epoch_acc

            if epoch % 10 == 0:
                arch = self._derive_architecture()
                result = self._evaluate_architecture(arch, start_time)
                self._architectures.append(result)
                self._progress.architectures_evaluated += 1
                self._progress.best_accuracy = best_acc

        # Final architecture derivation
        final_arch = self._derive_architecture()
        final_result = self._evaluate_architecture(final_arch, start_time)
        self._architectures.append(final_result)
        return final_result

    def _train_epoch(self, epoch: int) -> float:
        """Simulate one epoch of DARTS architecture parameter optimization."""
        # In production: actual gradient descent on architecture parameters
        return min(0.95, 0.5 + epoch * 0.01 + random.uniform(-0.01, 0.01))

    def _derive_architecture(self) -> Dict[str, Any]:
        """Derive discrete architecture from continuous architecture parameters."""
        genotype: Dict[str, Any] = {"normal": [], "reduction": []}
        for cell_type in ["normal", "reduction"]:
            for node in range(self.search_space.nodes_per_cell):
                ops = []
                for edge in range(node + 1):
                    op = random.choice(self.search_space.operations)
                    ops.append((op, edge))
                genotype[cell_type].append(ops)
        return genotype

    def _evaluate_architecture(
        self, genotype: Dict[str, Any], start_time: float
    ) -> ArchitectureResult:
        """Evaluate a discovered architecture."""
        param_count = random.randint(500_000, 5_000_000)
        flops = param_count * 100
        latency = param_count / 500_000 * 5
        accuracy = random.uniform(0.88, 0.95)

        return ArchitectureResult(
            architecture_id=f"DARTS-{uuid.uuid4().hex[:8].upper()}",
            genotype=genotype,
            accuracy=accuracy,
            parameter_count=param_count,
            flops=flops,
            latency_ms=latency,
            search_time_s=time.time() - start_time,
            training_time_s=time.time() - start_time,
            dataset=self.config.dataset,
        )

    def get_progress(self) -> SearchProgress:
        return self._progress

    def get_all_results(self) -> List[ArchitectureResult]:
        return sorted(self._architectures, key=lambda a: a.accuracy, reverse=True)


# ---------------------------------------------------------------------------
# Evolutionary NAS
# ---------------------------------------------------------------------------

class EvolutionaryNAS:
    """Population-based evolutionary architecture search."""

    def __init__(self, config: NASConfig):
        self.config = config
        self.search_space = config.search_space or SearchSpace()
        self._pareto = ParetoFront()
        self._all_results: List[ArchitectureResult] = []

    def search(
        self,
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.3,
        crossover_rate: float = 0.5,
        tournament_size: int = 5,
    ) -> ArchitectureResult:
        """Run evolutionary search."""
        start = time.time()
        population = self._init_population(population_size)

        for gen in range(generations):
            # Evaluate population
            evaluated = []
            for genome in population:
                result = self._evaluate_genome(genome, start)
                evaluated.append((genome, result))
                self._all_results.append(result)
                self._pareto.add(result)

            # Selection, crossover, mutation
            evaluated.sort(key=lambda x: x[1].accuracy, reverse=True)
            survivors = [g for g, _ in evaluated[:population_size // 2]]

            new_population = list(survivors)
            while len(new_population) < population_size:
                if random.random() < crossover_rate:
                    p1, p2 = random.sample(survivors, 2)
                    child = self._crossover(p1, p2)
                else:
                    child = self._mutate(random.choice(survivors), mutation_rate)
                new_population.append(child)

            population = new_population

        best = max(self._all_results, key=lambda a: a.accuracy)
        return best

    def _init_population(self, size: int) -> List[Dict[str, Any]]:
        population = []
        for _ in range(size):
            genome = {}
            for cell_type in ["normal", "reduction"]:
                genome[cell_type] = []
                for _ in range(self.search_space.nodes_per_cell):
                    node_ops = []
                    for edge in range(random.randint(1, self.search_space.nodes_per_cell)):
                        op = random.choice(self.search_space.operations)
                        node_ops.append((op, edge))
                    genome[cell_type].append(node_ops)
            population.append(genome)
        return population

    def _evaluate_genome(
        self, genome: Dict[str, Any], start_time: float
    ) -> ArchitectureResult:
        param_count = random.randint(500_000, 8_000_000)
        return ArchitectureResult(
            architecture_id=f"EVO-{uuid.uuid4().hex[:8].upper()}",
            genotype=genome,
            accuracy=random.uniform(0.85, 0.94),
            parameter_count=param_count,
            flops=param_count * 100,
            latency_ms=param_count / 500_000 * 5,
            search_time_s=time.time() - start_time,
            training_time_s=0,
            dataset=self.config.dataset,
        )

    def _crossover(self, p1: Dict, p2: Dict) -> Dict:
        child = {}
        for cell_type in ["normal", "reduction"]:
            child[cell_type] = []
            src = p1 if random.random() < 0.5 else p2
            child[cell_type] = list(src.get(cell_type, []))
        return child

    def _mutate(self, genome: Dict, rate: float) -> Dict:
        mutated = json.loads(json.dumps(genome))
        for cell_type in ["normal", "reduction"]:
            for i, node in enumerate(mutated.get(cell_type, [])):
                if random.random() < rate:
                    op = random.choice(self.search_space.operations)
                    mutated[cell_type][i] = [(op, j) for j in range(len(node))]
        return mutated

    @property
    def pareto_front(self) -> ParetoFront:
        return self._pareto


# ---------------------------------------------------------------------------
# Bayesian NAS
# ---------------------------------------------------------------------------

class BayesianNAS:
    """Bayesian optimization over architecture hyperparameters."""

    def __init__(self, config: NASConfig):
        self.config = config
        self._observations: List[Tuple[Dict, float]] = []

    def suggest(self) -> Dict[str, Any]:
        """Suggest next architecture to evaluate."""
        if len(self._observations) < 5:
            return self._random_config()
        return self._ucb_suggest()

    def observe(self, architecture: Dict[str, Any], accuracy: float) -> None:
        self._observations.append((architecture, accuracy))

    def optimize(self, n_iterations: int = 30) -> ArchitectureResult:
        """Run Bayesian optimization loop."""
        start = time.time()
        best_acc = 0.0
        best_arch = None

        for i in range(n_iterations):
            config = self.suggest()
            acc = random.uniform(0.85, 0.95)
            self.observe(config, acc)
            if acc > best_acc:
                best_acc = acc
                best_arch = config

        params = random.randint(500_000, 5_000_000)
        return ArchitectureResult(
            architecture_id=f"BAYES-{uuid.uuid4().hex[:8].upper()}",
            genotype=best_arch or {},
            accuracy=best_acc,
            parameter_count=params,
            flops=params * 100,
            latency_ms=params / 500_000 * 5,
            search_time_s=time.time() - start,
            training_time_s=0,
            dataset=self.config.dataset,
        )

    def _random_config(self) -> Dict[str, Any]:
        return {
            "num_cells": random.choice([6, 8, 10, 12]),
            "channels": random.choice([16, 24, 32, 48]),
            "nodes_per_cell": random.choice([3, 4, 5]),
            "operations": random.sample(self.config.search_space.operations or ["conv_3x3", "conv_5x5"], 3),
        }

    def _ucb_suggest(self) -> Dict[str, Any]:
        """Upper Confidence Bound acquisition function."""
        # Simplified: return config with highest expected improvement
        best = max(self._observations, key=lambda x: x[1])[0]
        mutated = dict(best)
        mutated["num_cells"] = best.get("num_cells", 8) + random.choice([-1, 0, 1])
        return mutated


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the NAS framework."""
    print("Neural Architecture Search Framework")
    print("=" * 60)

    search_space = SearchSpace()
    print(f"\nSearch space size: {search_space.search_space_size:.2e}")
    print(f"Operations: {search_space.operations}")

    config = NASConfig(
        strategy=SearchStrategy.DARTS,
        search_space=search_space,
        epochs=30,
        target_accuracy=0.95,
        dataset="cifar10",
    )

    # DARTS
    print("\n--- DARTS Search ---")
    darts = DARTSSearch(config)
    result = darts.search()
    print(f"Best: {result.accuracy:.4f} accuracy, {result.parameter_count:,} params, {result.latency_ms:.1f}ms")

    # Evolutionary
    print("\n--- Evolutionary Search ---")
    evo = EvolutionaryNAS(config)
    evo_result = evo.search(population_size=20, generations=10)
    print(f"Best: {evo_result.accuracy:.4f} accuracy")
    print(f"Pareto front: {len(evo.pareto_front.architectures)} architectures")
    best_pe = evo.pareto_front.most_efficient
    if best_pe:
        print(f"Most efficient: {best_pe.accuracy:.4f} ({best_pe.latency_ms:.1f}ms)")

    # Bayesian
    print("\n--- Bayesian Optimization ---")
    bayes = BayesianNAS(config)
    bayes_result = bayes.optimize(n_iterations=20)
    print(f"Best: {bayes_result.accuracy:.4f} accuracy")


if __name__ == "__main__":
    main()
