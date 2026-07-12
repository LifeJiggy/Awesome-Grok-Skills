"""
Consensus Mechanisms Module
PoW, PoS, BFT simulation, finality analysis, and security modeling.
"""

from __future__ import annotations

import hashlib
import logging
import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ConsensusType(Enum):
    POW = "proof_of_work"
    POS = "proof_of_stake"
    BFT = "byzantine_fault_tolerant"
    DPoS = "delegated_proof_of_stake"
    DAG = "directed_acyclic_graph"


class FinalityType(Enum):
    PROBABILISTIC = "probabilistic"
    ABSOLUTE = "absolute"
    DETERMINISTIC = "deterministic"


class ValidatorStatus(Enum):
    ACTIVE = "active"
    EXITING = "exiting"
    SLASHED = "slashed"
    INACTIVE = "inactive"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class PoWStats:
    """Proof of Work simulation statistics."""
    blocks: int = 0
    avg_block_time: float = 0.0
    difficulty_change: float = 0.0
    energy_kwh: float = 0.0
    attack_cost_usd: float = 0.0
    hash_rate_ehs: float = 0.0
    total_hashes: int = 0


@dataclass
class Validator:
    """PoS validator."""
    index: int
    pubkey: str
    stake: float
    status: ValidatorStatus = ValidatorStatus.ACTIVE
    balance: float = 0.0
    rewards_earned: float = 0.0
    slashing_events: int = 0

    @property
    def effective_balance(self) -> float:
        return min(self.stake, 32.0)


@dataclass
class EpochStats:
    """PoS epoch statistics."""
    epoch: int = 0
    attestations: int = 0
    justified: bool = False
    finalized: bool = False
    rewards_distributed: float = 0.0
    slashing_events: int = 0
    active_validators: int = 0
    participation_rate: float = 0.0


@dataclass
class BFTResult:
    """BFT consensus result."""
    consensus_reached: bool = False
    rounds: int = 0
    message_count: int = 0
    latency_ms: float = 0.0
    faulty_detected: int = 0
    leader: int = 0


@dataclass
class FinalityAnalysis:
    """Finality analysis result."""
    finality_type: FinalityType = FinalityType.PROBABILISTIC
    time_to_finality: float = 0.0
    confirmations_needed: int = 0
    max_reorg_depth: int = 0
    security_threshold: float = 0.0
    confidence: float = 0.0


@dataclass
class AttackCost:
    """51% attack cost estimation."""
    hardware_cost: float = 0.0
    electricity_cost: float = 0.0
    total_cost: float = 0.0
    daily_revenue: float = 0.0
    profitable: bool = False
    attack_duration_hours: float = 1.0


@dataclass
class StakingEconomics:
    """Staking economics result."""
    validator_apr: float = 0.0
    delegator_apr: float = 0.0
    min_profitable_stake: float = 0.0
    annual_rewards: float = 0.0
    network_inflation: float = 0.0


@dataclass
class DagTransaction:
    """DAG (IOTA-style) transaction."""
    tx_id: str
    tip1: str
    tip2: str
    weight: float = 1.0
    cumulative_weight: float = 0.0
    confirmed: bool = False


# ---------------------------------------------------------------------------
# PoW Simulator
# ---------------------------------------------------------------------------

class PoWSimulator:
    """Proof of Work mining simulation."""

    def __init__(
        self,
        block_time_target: float = 12.0,
        hash_rate: float = 1e18,
        difficulty: float = 1e15,
        block_reward: float = 6.25,
        energy_per_hash_j: float = 1e-13,
        electricity_cost_kwh: float = 0.05,
    ):
        self.block_time_target = block_time_target
        self.hash_rate = hash_rate
        self.difficulty = difficulty
        self.block_reward = block_reward
        self.energy_per_hash_j = energy_per_hash_j
        self.electricity_cost_kwh = electricity_cost_kwh

    def simulate(self, blocks: int = 100, seed: int = 42) -> PoWStats:
        rng = random.Random(seed)
        total_time = 0.0
        total_energy = 0.0
        total_hashes = 0
        block_times: List[float] = []
        current_diff = self.difficulty

        for _ in range(blocks):
            expected_hashes = current_diff * 2**32
            time_seconds = expected_hashes / max(self.hash_rate, 1)
            block_times.append(time_seconds)
            total_time += time_seconds
            hashes = int(expected_hashes * rng.uniform(0.5, 1.5))
            total_hashes += hashes
            energy_j = hashes * self.energy_per_hash_j
            total_energy += energy_j
            if (_ + 1) % 2016 == 0:
                actual_time = sum(block_times[-2016:])
                target_time = 2016 * self.block_time_target
                ratio = target_time / max(actual_time, 1)
                current_diff *= min(max(ratio, 0.25), 4.0)

        avg_bt = total_time / max(blocks, 1)
        energy_kwh = total_energy / 3.6e6
        cost_per_block = energy_kwh / max(blocks, 1) * self.electricity_cost_kwh
        attack_cost = self._estimate_attack_cost()

        return PoWStats(
            blocks=blocks,
            avg_block_time=avg_bt,
            difficulty_change=(current_diff - self.difficulty) / max(self.difficulty, 1),
            energy_kwh=energy_kwh,
            attack_cost_usd=attack_cost,
            hash_rate_ehs=self.hash_rate / 1e18,
            total_hashes=total_hashes,
        )

    def mine_block(self, nonce_start: int = 0, max_attempts: int = 10_000_000) -> Optional[Dict[str, Any]]:
        target = 2**256 // max(int(self.difficulty), 1)
        for nonce in range(nonce_start, nonce_start + max_attempts):
            block_hash = hashlib.sha256(f"block_{nonce}".encode()).hexdigest()
            hash_int = int(block_hash, 16)
            if hash_int < target:
                return {
                    "nonce": nonce,
                    "hash": block_hash,
                    "difficulty": self.difficulty,
                    "attempts": nonce - nonce_start + 1,
                }
        return None

    def _estimate_attack_cost(self) -> float:
        hash_rate_needed = self.hash_rate * 1.01
        hardware_cost = hash_rate_needed / 1e12 * 20_000
        hourly_energy = hash_rate_needed * self.energy_per_hash_j * 3600 / 3.6e6
        hourly_cost = hourly_energy * self.electricity_cost_kwh
        return hardware_cost + hourly_cost * 24


# ---------------------------------------------------------------------------
# PoS Simulator
# ---------------------------------------------------------------------------

class PoSSimulator:
    """Proof of Stake simulation."""

    def __init__(
        self,
        total_staked: float = 32_000_000,
        validator_count: int = 1_000_000,
        min_stake: float = 32.0,
        slashing_penalty: float = 0.01,
        base_reward_rate: float = 0.04,
    ):
        self.total_staked = total_staked
        self.validator_count = validator_count
        self.min_stake = min_stake
        self.slashing_penalty = slashing_penalty
        self.base_reward_rate = base_reward_rate
        self._epoch = 0
        self._validators = self._init_validators()

    def _init_validators(self) -> List[Validator]:
        rng = random.Random(42)
        validators: List[Validator] = []
        for i in range(self.validator_count):
            stake = max(self.min_stake, rng.gauss(self.min_stake * 2, self.min_stake))
            validators.append(Validator(
                index=i,
                pubkey=f"0x{i:040x}",
                stake=stake,
                balance=stake,
            ))
        return validators

    def simulate_epoch(self, epoch: Optional[int] = None) -> EpochStats:
        self._epoch = epoch if epoch is not None else self._epoch + 1
        active = [v for v in self._validators if v.status == ValidatorStatus.ACTIVE]
        total_active = len(active)
        participating = int(total_active * random.uniform(0.95, 1.0))
        attestation_reward = self.base_reward_rate / 365 / 225 * self.min_stake
        total_rewards = 0.0
        slashing = 0
        for v in active[:participating]:
            v.rewards_earned += attestation_reward
            v.balance += attestation_reward
            total_rewards += attestation_reward
        if random.random() < 0.001:
            slashed = random.choice(active)
            slashed.status = ValidatorStatus.SLASHED
            slashed.balance *= (1 - self.slashing_penalty)
            slashing += 1

        justified = participating / max(total_active, 1) >= 2 / 3
        finalized = justified and participating / max(total_active, 1) >= 0.9

        return EpochStats(
            epoch=self._epoch,
            attestations=participating,
            justified=justified,
            finalized=finalized,
            rewards_distributed=round(total_rewards, 4),
            slashing_events=slashing,
            active_validators=total_active,
            participation_rate=participating / max(total_active, 1),
        )

    def calculate_staking_economics(
        self,
        eth_price: float = 3000.0,
        network_reward_rate: float = 0.04,
    ) -> StakingEconomics:
        annual_rewards_per_validator = self.min_stake * network_reward_rate
        validator_apr = network_reward_rate
        delegator_apr = network_reward_rate * 0.9
        min_profitable = 32.0 * eth_price
        annual_usd = annual_rewards_per_validator * eth_price
        inflation = network_reward_rate * self.total_staked / (self.total_staked * 0.7)
        return StakingEconomics(
            validator_apr=validator_apr,
            delegator_apr=delegator_apr,
            min_profitable_stake=min_profitable,
            annual_rewards=round(annual_usd, 2),
            network_inflation=round(inflation, 4),
        )

    def calculate_slashing_loss(self, slash_count: int = 1) -> float:
        total_slash = 0.0
        for _ in range(slash_count):
            total_slash += self.min_stake * self.slashing_penalty
        return total_slash


# ---------------------------------------------------------------------------
# BFT Simulator
# ---------------------------------------------------------------------------

class BFTSimulator:
    """Byzantine Fault Tolerant consensus simulation."""

    def __init__(
        self,
        validators: int = 100,
        faulty_nodes: int = 33,
        view_change_timeout: float = 5.0,
        message_delay_ms: float = 50.0,
    ):
        self.total_validators = validators
        self.faulty_nodes = min(faulty_nodes, (validators - 1) // 3)
        self.max_faulty = (validators - 1) // 3
        self.view_change_timeout = view_change_timeout
        self.message_delay_ms = message_delay_ms

    def simulate_consensus(
        self,
        proposal: str,
        view: int = 0,
        seed: int = 42,
    ) -> BFTResult:
        rng = random.Random(seed)
        rounds = 0
        total_messages = 0
        faulty_detected = 0

        for attempt in range(10):
            rounds = attempt + 1
            leader = (view + attempt) % self.total_validators
            pre_prepare = 1
            prepare_messages = 0
            commit_messages = 0

            for v in range(self.total_validators):
                if rng.random() < 0.02 and v < self.faulty_nodes:
                    faulty_detected += 1
                    continue
                prepare_messages += 1

            for v in range(self.total_validators):
                if rng.random() < 0.02 and v < self.faulty_nodes:
                    continue
                commit_messages += 1

            total_messages += pre_prepare + prepare_messages + commit_messages
            honest_prepares = prepare_messages
            if honest_prepares >= 2 * self.max_faulty + 1:
                honest_commits = commit_messages
                if honest_commits >= 2 * self.max_faulty + 1:
                    latency = rounds * (self.message_delay_ms * 3 + self.view_change_timeout * 1000)
                    return BFTResult(
                        consensus_reached=True,
                        rounds=rounds,
                        message_count=total_messages,
                        latency_ms=latency,
                        faulty_detected=faulty_detected,
                        leader=leader,
                    )
        latency = rounds * (self.message_delay_ms * 3 + self.view_change_timeout * 1000)
        return BFTResult(
            consensus_reached=False,
            rounds=rounds,
            message_count=total_messages,
            latency_ms=latency,
            faulty_detected=faulty_detected,
        )

    def message_complexity(self) -> Dict[str, int]:
        n = self.total_validators
        return {
            "pre_prepare": 1,
            "prepare": n * (n - 1),
            "commit": n * (n - 1),
            "total": 1 + 2 * n * (n - 1),
        }

    def max_throughput(
        self, block_size_bytes: int, network_bandwidth_mbps: float = 100
    ) -> float:
        msgs = self.message_complexity()
        total_bytes = msgs["total"] * block_size_bytes
        bandwidth_bytes_s = network_bandwidth_mbps * 1e6 / 8
        return bandwidth_bytes_s / max(total_bytes, 1)


# ---------------------------------------------------------------------------
# Finality Analyzer
# ---------------------------------------------------------------------------

class FinalityAnalyzer:
    """Analyze finality properties of consensus mechanisms."""

    def __init__(
        self,
        consensus_type: str = "pos",
        validator_set_size: int = 1_000_000,
        stake_distribution: str = "normal",
        network_latency_ms: float = 100.0,
    ):
        self.consensus_type = consensus_type
        self.validator_set_size = validator_set_size
        self.stake_distribution = stake_distribution
        self.network_latency_ms = network_latency_ms

    def analyze(self, security_level: float = 0.99) -> FinalityAnalysis:
        if self.consensus_type in ("bft", "tendermint"):
            return FinalityAnalysis(
                finality_type=FinalityType.ABSOLUTE,
                time_to_finality=6.0,
                confirmations_needed=1,
                max_reorg_depth=0,
                security_threshold=0.67,
                confidence=security_level,
            )
        elif self.consensus_type == "pos":
            return FinalityAnalysis(
                finality_type=FinalityType.DETERMINISTIC,
                time_to_finality=768.0,
                confirmations_needed=2,
                max_reorg_depth=3,
                security_threshold=0.33,
                confidence=security_level,
            )
        else:
            confirmations = self._poisson_confirmations(security_level)
            time = confirmations * 600
            return FinalityAnalysis(
                finality_type=FinalityType.PROBABILISTIC,
                time_to_finality=time,
                confirmations_needed=confirmations,
                max_reorg_depth=confirmations,
                security_threshold=0.5,
                confidence=security_level,
            )

    def _poisson_confirmations(self, confidence: float) -> int:
        lam = 1.0 / 6
        for k in range(1, 100):
            prob = sum(math.exp(-lam) * lam**i / math.factorial(i) for i in range(k))
            if prob >= confidence:
                return k
        return 60


# ---------------------------------------------------------------------------
# Security Modeler
# ---------------------------------------------------------------------------

class SecurityModeler:
    """Model consensus security properties."""

    def estimate_51_percent_attack(
        self,
        network_hash_rate: float,
        hardware_cost_per_th: float = 50.0,
        electricity_cost_kwh: float = 0.05,
        block_reward: float = 6.25,
        btc_price: float = 50000.0,
        attack_duration_hours: float = 1.0,
    ) -> AttackCost:
        hash_rate_th = network_hash_rate / 1e12
        hardware = hash_rate_th * hardware_cost_per_th * 1.01
        power_mw = network_hash_rate * 1e12 * 1e-13 * 1.01 / 1e6
        energy_kwh = power_mw * 1000 * attack_duration_hours
        electricity = energy_kwh * electricity_cost_kwh
        blocks_per_hour = 3600 / 600
        daily_blocks = blocks_per_hour * 24
        daily_revenue = daily_blocks * block_reward * btc_price
        total = hardware + electricity
        profitable = daily_revenue > total
        return AttackCost(
            hardware_cost=round(hardware, 2),
            electricity_cost=round(electricity, 2),
            total_cost=round(total, 2),
            daily_revenue=round(daily_revenue, 2),
            profitable=profitable,
            attack_duration_hours=attack_duration_hours,
        )

    def nothing_at_stake_risk(
        self,
        validator_count: int,
        chain_count: int = 3,
    ) -> float:
        return min(chain_count * 0.1, 0.9)

    def long_range_attack_resistance(
        self,
        checkpoint_interval: int = 256,
        finality_depth: int = 100,
        stake_required_pct: float = 0.33,
    ) -> Dict[str, Any]:
        return {
            "checkpoint_interval": checkpoint_interval,
            "finality_depth": finality_depth,
            "stake_required": stake_required_pct,
            "resistant": stake_required_pct >= 0.33 and finality_depth <= checkpoint_interval,
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Consensus Mechanisms Demo")
    print("=" * 60)

    print("\n[1] PoW Simulation")
    pow = PoWSimulator(block_time_target=12, hash_rate=1e18, difficulty=1e15)
    stats = pow.simulate(blocks=50)
    print(f"  Avg block time: {stats.avg_block_time:.1f}s")
    print(f"  Energy: {stats.energy_kwh:.2f} kWh")
    print(f"  51% cost: ${stats.attack_cost_usd:,.0f}")

    print("\n[2] PoS Simulation")
    pos = PoSSimulator(total_staked=32_000_000, validator_count=1000000)
    epoch = pos.simulate_epoch()
    print(f"  Epoch {epoch.epoch}: {epoch.attestations} attestations")
    print(f"  Finalized: {epoch.finalized}")
    print(f"  Rewards: {epoch.rewards_distributed:.4f} ETH")

    print("\n[3] BFT Simulation")
    bft = BFTSimulator(validators=100, faulty_nodes=33)
    result = bft.simulate_consensus("Block #12345")
    print(f"  Consensus: {result.consensus_reached}")
    print(f"  Rounds: {result.rounds}  Messages: {result.message_count}")
    print(f"  Max faulty: {bft.max_faulty}/{bft.total_validators}")

    print("\n[4] Finality Analysis")
    fa = FinalityAnalyzer(consensus_type="pos")
    analysis = fa.analyze()
    print(f"  Type: {analysis.finality_type.value}")
    print(f"  Time to finality: {analysis.time_to_finality:.0f}s")

    print("\n[5] Security Modeler")
    sm = SecurityModeler()
    attack = sm.estimate_51_percent_attack(
        network_hash_rate=1e18, block_reward=6.25, btc_price=50000
    )
    print(f"  Hardware: ${attack.hardware_cost:,.0f}")
    print(f"  Electricity: ${attack.electricity_cost:,.0f}")
    print(f"  Total: ${attack.total_cost:,.0f}")

    print("\n[6] Staking Economics")
    econ = pos.calculate_staking_economics(eth_price=3000)
    print(f"  Validator APR: {econ.validator_apr:.2%}")
    print(f"  Min stake: ${econ.min_profitable_stake:,.0f}")

    print("\n" + "=" * 60)
    print("  Consensus mechanisms demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
