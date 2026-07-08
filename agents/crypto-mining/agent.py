"""Crypto Mining Agent - Cryptocurrency Mining Operations Platform.

Comprehensive framework for mining operations including pool management,
hardware monitoring, profitability analysis, and multi-algorithm optimization.

Features:
- Multi-algorithm mining (SHA-256, Ethash, Scrypt, RandomX, KawPow)
- ASIC and GPU rig management with hot-swap capability
- Real-time hash rate tracking and anomaly detection
- Dynamic profitability calculator with difficulty adjustment
- Energy consumption tracking and efficiency optimization
- Temperature monitoring with automatic throttling
- Pool switching with latency-based and composite strategies
- Mining economics with ROI and break-even analysis
"""

import asyncio
import hashlib
import hmac
import json
import logging
import math
import os
import random
import statistics
import struct
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import (
    Any, Callable, Coroutine, Dict, List, Optional, Set, Tuple, Union,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("crypto_mining_agent")

# =============================================================================
# ENUMS
# =============================================================================

class AlgorithmType(Enum):
    SHA256 = auto()
    ETHASH = auto()
    SCRYPT = auto()
    RANDOMX = auto()
    KAWPOW = auto()
    EQUIHASH = auto()
    CRYPTONIGHT = auto()
    BLAKE2S = auto()
    LYRA2REV2 = auto()
    X11 = auto()

class HardwareType(Enum):
    ASIC = auto()
    GPU_NVIDIA = auto()
    GPU_AMD = auto()
    CPU = auto()
    FPGA = auto()

class PoolStatus(Enum):
    ONLINE = auto()
    DEGRADED = auto()
    OFFLINE = auto()
    MAINTENANCE = auto()
    HIGH_LATENCY = auto()

class RigStatus(Enum):
    ONLINE = auto()
    MINING = auto()
    IDLE = auto()
    THROTTLED = auto()
    ERROR = auto()
    OFFLINE = auto()
    MAINTENANCE = auto()

class RewardType(Enum):
    PPS = auto()
    PPLNS = auto()
    PROP = auto()
    SOLO = auto()
    PPS_PLUS = auto()

class TemperatureUnit(Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"

class EnergyUnit(Enum):
    WATT = "W"
    KILOWATT = "kW"
    MEGAWATT = "MW"
    JOULES = "J"
    KWH = "kWh"

class HashRateUnit(Enum):
    HPS = "H/s"
    KHPS = "kH/s"
    MHPS = "MH/s"
    GHPS = "GH/s"
    THPS = "TH/s"
    PHPS = "PH/s"
    EHPS = "EH/s"

# =============================================================================
# CONSTANTS
# =============================================================================

NETWORK_DIFFICULTY: Dict[str, float] = {
    "bitcoin": 83_000_000_000_000, "litecoin": 800_000_000,
    "bitcoin_cash": 600_000_000, "dogecoin": 450_000_000,
    "monero": 380_000_000_000, "ravencoin": 15_000_000,
    "ethereum_classic": 18_000_000_000_000, "firo": 200_000, "flux": 500_000,
}

BLOCK_REWARDS: Dict[str, float] = {
    "bitcoin": 3.125, "litecoin": 6.25, "bitcoin_cash": 3.125,
    "dogecoin": 10000, "monero": 0.6, "ravencoin": 2500,
    "ethereum_classic": 2.56, "firo": 6.25, "flux": 3.75,
}

ALGORITHM_COINS: Dict[AlgorithmType, List[str]] = {
    AlgorithmType.SHA256: ["bitcoin", "bitcoin_cash", "dogecoin"],
    AlgorithmType.ETHASH: ["ethereum_classic", "flux"],
    AlgorithmType.SCRYPT: ["litecoin", "dogecoin"],
    AlgorithmType.RANDOMX: ["monero"],
    AlgorithmType.KAWPOW: ["ravencoin"],
    AlgorithmType.EQUIHASH: ["zcoin", "bitcoin_gold"],
    AlgorithmType.CRYPTONIGHT: ["monero", "grin"],
    AlgorithmType.BLAKE2S: ["sia", "decred"],
    AlgorithmType.LYRA2REV2: ["verge", "monacoin"],
    AlgorithmType.X11: ["dash", "smartcash"],
}

HARDWARE_HASH_RATES: Dict[str, Dict[str, Any]] = {
    "bitmain_s19": {"algorithm": AlgorithmType.SHA256, "hash_rate": 110.0, "power": 3250},
    "bitmain_s21": {"algorithm": AlgorithmType.SHA256, "hash_rate": 200.0, "power": 3500},
    "antminer_l7": {"algorithm": AlgorithmType.SCRYPT, "hash_rate": 9.16, "power": 3425},
    "nvidia_rtx_4090": {"algorithm": AlgorithmType.KAWPOW, "hash_rate": 120.0, "power": 450},
    "nvidia_rtx_3080": {"algorithm": AlgorithmType.KAWPOW, "hash_rate": 65.0, "power": 320},
    "amd_rx_6800_xt": {"algorithm": AlgorithmType.KAWPOW, "hash_rate": 64.0, "power": 300},
    "amd_rx_7900_xtx": {"algorithm": AlgorithmType.KAWPOW, "hash_rate": 110.0, "power": 355},
}

TEMPERATURE_THRESHOLDS: Dict[HardwareType, Tuple[float, float, float]] = {
    HardwareType.ASIC: (40.0, 70.0, 90.0),
    HardwareType.GPU_NVIDIA: (30.0, 75.0, 95.0),
    HardwareType.GPU_AMD: (30.0, 75.0, 95.0),
    HardwareType.CPU: (30.0, 80.0, 100.0),
    HardwareType.FPGA: (20.0, 60.0, 85.0),
}

BLOCK_TIMES: Dict[str, float] = {
    "bitcoin": 600.0, "litecoin": 150.0, "bitcoin_cash": 600.0,
    "dogecoin": 60.0, "monero": 120.0, "ravencoin": 60.0,
    "ethereum_classic": 13.0, "firo": 240.0, "flux": 120.0,
}

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class HashRateSample:
    timestamp: datetime = field(default_factory=datetime.now)
    value: float = 0.0
    unit: HashRateUnit = HashRateUnit.HPS
    rig_id: Optional[str] = None
    algorithm: Optional[AlgorithmType] = None
    difficulty: float = 0.0
    valid: bool = True

@dataclass
class TemperatureReading:
    sensor_id: str
    value: float
    unit: TemperatureUnit = TemperatureUnit.CELSIUS
    timestamp: datetime = field(default_factory=datetime.now)
    component: str = "unknown"
    warning: bool = False
    critical: bool = False

@dataclass
class EnergyReading:
    rig_id: str
    power_draw: float
    unit: EnergyUnit = EnergyUnit.WATT
    timestamp: datetime = field(default_factory=datetime.now)
    efficiency: float = 0.0
    cost_per_kwh: float = 0.12
    daily_cost: float = 0.0
    monthly_cost: float = 0.0

@dataclass
class PoolEndpoint:
    url: str
    port: int
    protocol: str = "stratum+tcp"
    priority: int = 1
    region: str = "unknown"
    latency_ms: float = 0.0
    active: bool = True
    fee: float = 1.0
    payout_threshold: float = 0.01

@dataclass
class MiningReward:
    block_height: int
    coin: str
    amount: float
    timestamp: datetime = field(default_factory=datetime.now)
    pool_fee: float = 0.0
    payout_txid: Optional[str] = None
    confirmed: bool = False
    confirmations: int = 0

@dataclass
class ProfitabilityMetrics:
    coin: str
    algorithm: AlgorithmType
    hash_rate: float
    power_consumption: float
    electricity_cost_per_kwh: float
    network_difficulty: float
    block_reward: float
    daily_revenue: float
    daily_cost: float
    daily_profit: float
    monthly_profit: float
    yearly_profit: float
    roi_days: float
    break_even_price: float
    efficiency_j_per_gh: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class RigHardware:
    rig_id: str
    hardware_type: HardwareType
    model: str
    algorithm: AlgorithmType
    hash_rate: float
    power_consumption: float
    unit_cost: float
    age_days: int = 0
    warranty_expiry_days: int = 365
    serial_number: Optional[str] = None
    firmware_version: Optional[str] = None

@dataclass
class RigState:
    rig_id: str
    status: RigStatus
    current_hash_rate: float
    target_hash_rate: float
    accepted_shares: int = 0
    rejected_shares: int = 0
    stale_shares: int = 0
    uptime_seconds: int = 0
    temperature: float = 0.0
    fan_speed_percent: float = 0.0
    last_share_time: Optional[datetime] = None
    error_message: Optional[str] = None

@dataclass
class PoolConfig:
    pool_name: str
    coin: str
    algorithm: AlgorithmType
    endpoints: List[PoolEndpoint]
    reward_type: RewardType
    fee_percentage: float = 1.0
    payout_threshold: float = 0.01
    default: bool = False
    min_payout: float = 0.001
    url: str = ""
    worker_name: str = ""
    password: str = "x"

@dataclass
class ShareSubmission:
    share_id: str
    rig_id: str
    pool_name: str
    difficulty: float
    timestamp: datetime = field(default_factory=datetime.now)
    valid: bool = True
    block_candidate: bool = False
    latency_ms: float = 0.0

# =============================================================================
# EXCEPTIONS
# =============================================================================

class CryptoMiningError(Exception):
    pass

class HardwareError(CryptoMiningError):
    pass

class PoolError(CryptoMiningError):
    pass

class ProfitabilityError(CryptoMiningError):
    pass

class TemperatureError(HardwareError):
    pass

class HashRateError(CryptoMiningError):
    pass

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def convert_hash_rate(value: float, from_unit: HashRateUnit, to_unit: HashRateUnit) -> float:
    unit_exponents = {
        HashRateUnit.HPS: 0, HashRateUnit.KHPS: 3, HashRateUnit.MHPS: 6,
        HashRateUnit.GHPS: 9, HashRateUnit.THPS: 12, HashRateUnit.PHPS: 15,
        HashRateUnit.EHPS: 18,
    }
    exponent_diff = unit_exponents[to_unit] - unit_exponents[from_unit]
    return value * (10 ** exponent_diff)

def convert_temperature(value: float, from_unit: TemperatureUnit, to_unit: TemperatureUnit) -> float:
    if from_unit == to_unit:
        return value
    if from_unit == TemperatureUnit.CELSIUS:
        celsius = value
    elif from_unit == TemperatureUnit.FAHRENHEIT:
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15
    if to_unit == TemperatureUnit.CELSIUS:
        return celsius
    if to_unit == TemperatureUnit.FAHRENHEIT:
        return celsius * 9 / 5 + 32
    return celsius + 273.15

def calculate_network_hash_rate(difficulty: float, algorithm: AlgorithmType,
                                 block_time_seconds: float = 600.0) -> float:
    hashes_per_block = difficulty * 2**32
    return hashes_per_block / block_time_seconds

def calculate_miner_reward(hash_rate: float, network_hash_rate: float,
                           block_reward: float, block_time_seconds: float = 600.0) -> float:
    if network_hash_rate <= 0:
        return 0.0
    probability = hash_rate / network_hash_rate
    return (probability * block_reward) / block_time_seconds

def generate_worker_name(prefix: str = "worker") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def calculate_pool_fee(amount: float, fee_percentage: float) -> Tuple[float, float]:
    fee = amount * (fee_percentage / 100.0)
    return amount - fee, fee

def estimate_mining_duration(hash_rate: float, difficulty: float,
                             algorithm: AlgorithmType, block_time: float = 600.0) -> float:
    network_hash_rate = calculate_network_hash_rate(difficulty, algorithm, block_time)
    if network_hash_rate <= 0 or hash_rate <= 0:
        return float("inf")
    return 1.0 / (hash_rate / network_hash_rate)

def infer_algorithm(coin: str) -> AlgorithmType:
    coin_lower = coin.lower().replace("-", "").replace("_", "")
    for algorithm, coins in ALGORITHM_COINS.items():
        if any(c.lower().replace("-", "").replace("_", "") == coin_lower for c in coins):
            return algorithm
    return AlgorithmType.SHA256

# =============================================================================
# TEMPERATURE MONITOR
# =============================================================================

class TemperatureMonitor:
    def __init__(self, hardware_type: HardwareType = HardwareType.ASIC,
                 unit: TemperatureUnit = TemperatureUnit.CELSIUS):
        self._hardware_type = hardware_type
        self._unit = unit
        self._sensors: Dict[str, TemperatureReading] = {}
        self._history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._alerts: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        thresholds = TEMPERATURE_THRESHOLDS.get(hardware_type, (30.0, 70.0, 90.0))
        self._warning_threshold = thresholds[1]
        self._critical_threshold = thresholds[2]

    def add_sensor(self, sensor_id: str, component: str = "unknown") -> None:
        with self._lock:
            self._sensors[sensor_id] = TemperatureReading(
                sensor_id=sensor_id, value=0.0, unit=self._unit, component=component,
            )

    def update_reading(self, sensor_id: str, value: float,
                       unit: Optional[TemperatureUnit] = None) -> TemperatureReading:
        with self._lock:
            if sensor_id not in self._sensors:
                self.add_sensor(sensor_id)
            reading = TemperatureReading(
                sensor_id=sensor_id, value=value, unit=unit or self._unit,
                component=self._sensors[sensor_id].component,
            )
            reading.warning = value >= self._warning_threshold
            reading.critical = value >= self._critical_threshold
            self._sensors[sensor_id] = reading
            self._history[sensor_id].append(reading)
            if reading.critical:
                self._alerts.append({
                    "sensor": sensor_id, "value": value,
                    "threshold": self._critical_threshold,
                    "timestamp": datetime.now().isoformat(), "severity": "critical",
                })
            return reading

    def get_reading(self, sensor_id: str) -> Optional[TemperatureReading]:
        with self._lock:
            return self._sensors.get(sensor_id)

    def get_all_readings(self) -> Dict[str, TemperatureReading]:
        with self._lock:
            return dict(self._sensors)

    def get_history(self, sensor_id: str, limit: int = 100) -> List[TemperatureReading]:
        with self._lock:
            return list(self._history.get(sensor_id, []))[-limit:]

    def get_alerts(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            alerts = list(self._alerts)
        if severity:
            alerts = [a for a in alerts if a.get("severity") == severity]
        return alerts

    def get_average_temperature(self) -> float:
        with self._lock:
            values = [r.value for r in self._sensors.values() if r.value > 0]
        return statistics.mean(values) if values else 0.0

    def get_max_temperature(self) -> float:
        with self._lock:
            values = [r.value for r in self._sensors.values()]
        return max(values) if values else 0.0

    def is_safe(self) -> bool:
        with self._lock:
            return not any(r.critical for r in self._sensors.values())

    def clear_alerts(self) -> None:
        with self._lock:
            self._alerts.clear()

    def set_thresholds(self, warning: float, critical: float) -> None:
        with self._lock:
            self._warning_threshold = warning
            self._critical_threshold = critical

# =============================================================================
# HARDWARE MONITOR
# =============================================================================

class HardwareMonitor:
    def __init__(self, poll_interval_seconds: float = 5.0):
        self._poll_interval = poll_interval_seconds
        self._rigs: Dict[str, RigState] = {}
        self._temp_monitors: Dict[str, TemperatureMonitor] = {}
        self._energy_readings: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._hash_rate_samples: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._running = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._callbacks: List[Callable[[str, RigState], None]] = []

    def register_rig(self, rig: RigHardware) -> RigState:
        state = RigState(
            rig_id=rig.rig_id, status=RigStatus.OFFLINE,
            current_hash_rate=0.0, target_hash_rate=rig.hash_rate,
        )
        with self._lock:
            self._rigs[rig.rig_id] = state
            self._temp_monitors[rig.rig_id] = TemperatureMonitor(hardware_type=rig.hardware_type)
        logger.info("Registered rig %s (%s)", rig.rig_id, rig.model)
        return state

    def unregister_rig(self, rig_id: str) -> None:
        with self._lock:
            self._rigs.pop(rig_id, None)
            self._temp_monitors.pop(rig_id, None)

    def start_monitoring(self) -> None:
        if self._running:
            return
        self._running = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("Hardware monitoring started")

    def stop_monitoring(self) -> None:
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)
        logger.info("Hardware monitoring stopped")

    def _monitor_loop(self) -> None:
        while self._running:
            try:
                self._collect_metrics()
            except Exception as e:
                logger.error("Monitoring error: %s", e)
            time.sleep(self._poll_interval)

    def _collect_metrics(self) -> None:
        with self._lock:
            rig_ids = list(self._rigs.keys())
        for rig_id in rig_ids:
            self._simulate_rig_metrics(rig_id)

    def _simulate_rig_metrics(self, rig_id: str) -> None:
        state = self._rigs.get(rig_id)
        if not state or state.status != RigStatus.MINING:
            return
        temp_monitor = self._temp_monitors.get(rig_id)
        if not temp_monitor:
            return
        core_temp = 55.0 + random.uniform(-5.0, 15.0)
        vr_temp = 65.0 + random.uniform(-3.0, 10.0)
        temp_monitor.update_reading("core", core_temp)
        temp_monitor.update_reading("vrm", vr_temp)
        variance = random.uniform(-0.02, 0.02)
        state.current_hash_rate = max(0, state.target_hash_rate * (1 + variance))
        state.temperature = temp_monitor.get_average_temperature()
        state.accepted_shares += random.randint(0, 3)
        state.rejected_shares += random.randint(0, 1)
        state.stale_shares += random.randint(0, 1)
        state.uptime_seconds += int(self._poll_interval)
        if state.temperature > 85.0:
            state.status = RigStatus.THROTTLED
            state.fan_speed_percent = min(100.0, state.fan_speed_percent + 5.0)
        for callback in self._callbacks:
            try:
                callback(rig_id, state)
            except Exception as e:
                logger.error("Callback error for %s: %s", rig_id, e)

    def register_callback(self, callback: Callable[[str, RigState], None]) -> None:
        self._callbacks.append(callback)

    def get_rig_state(self, rig_id: str) -> Optional[RigState]:
        with self._lock:
            return self._rigs.get(rig_id)

    def get_all_states(self) -> Dict[str, RigState]:
        with self._lock:
            return dict(self._rigs)

    def update_rig_status(self, rig_id: str, status: RigStatus) -> None:
        with self._lock:
            if rig_id in self._rigs:
                self._rigs[rig_id].status = status

    def record_hash_rate(self, rig_id: str, value: float, unit: HashRateUnit = HashRateUnit.THPS) -> None:
        with self._lock:
            self._hash_rate_samples[rig_id].append(HashRateSample(value=value, unit=unit, rig_id=rig_id))

    def get_hash_rate_history(self, rig_id: str, limit: int = 100) -> List[HashRateSample]:
        with self._lock:
            return list(self._hash_rate_samples.get(rig_id, []))[-limit:]

    def record_energy(self, reading: EnergyReading) -> None:
        with self._lock:
            self._energy_readings[reading.rig_id].append(reading)

    def get_energy_history(self, rig_id: str, limit: int = 100) -> List[EnergyReading]:
        with self._lock:
            return list(self._energy_readings.get(rig_id, []))[-limit:]

    def get_total_power_draw(self) -> float:
        total = 0.0
        with self._lock:
            for readings in self._energy_readings.values():
                if readings:
                    total += readings[-1].power_draw
        return total

    def get_health_report(self) -> Dict[str, Any]:
        report = {
            "timestamp": datetime.now().isoformat(), "rigs": {},
            "total_power_w": self.get_total_power_draw(), "alerts": [],
        }
        with self._lock:
            for rig_id, state in self._rigs.items():
                temp_mon = self._temp_monitors.get(rig_id)
                alerts = temp_mon.get_alerts() if temp_mon else []
                report["rigs"][rig_id] = {
                    "status": state.status.name, "hash_rate": state.current_hash_rate,
                    "temperature": state.temperature, "uptime_seconds": state.uptime_seconds,
                    "accepted_shares": state.accepted_shares,
                    "rejected_shares": state.rejected_shares,
                    "stale_shares": state.stale_shares, "alerts_count": len(alerts),
                }
                report["alerts"].extend([{"rig_id": rig_id, **a} for a in alerts])
        return report

# =============================================================================
# HASH RATE TRACKER
# =============================================================================

class HashRateTracker:
    def __init__(self, window_size: int = 100, alert_threshold_percent: float = 10.0):
        self._window_size = window_size
        self._alert_threshold = alert_threshold_percent
        self._samples: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self._baselines: Dict[str, float] = {}
        self._anomalies: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def set_baseline(self, rig_id: str, baseline_hash_rate: float) -> None:
        with self._lock:
            self._baselines[rig_id] = baseline_hash_rate

    def record_sample(self, rig_id: str, value: float, unit: HashRateUnit = HashRateUnit.HPS,
                      algorithm: Optional[AlgorithmType] = None, difficulty: float = 0.0) -> HashRateSample:
        sample = HashRateSample(value=value, unit=unit, rig_id=rig_id, algorithm=algorithm, difficulty=difficulty)
        with self._lock:
            self._samples[rig_id].append(sample)
            if rig_id in self._baselines:
                baseline = self._baselines[rig_id]
                if baseline > 0:
                    drop_percent = ((baseline - value) / baseline) * 100
                    if drop_percent > self._alert_threshold:
                        self._anomalies.append({
                            "rig_id": rig_id, "baseline": baseline, "current": value,
                            "drop_percent": drop_percent, "timestamp": datetime.now().isoformat(),
                        })
                        logger.warning("Hash rate anomaly for %s: %.1f%% drop", rig_id, drop_percent)
        return sample

    def get_samples(self, rig_id: str, limit: Optional[int] = None) -> List[HashRateSample]:
        with self._lock:
            samples = list(self._samples.get(rig_id, []))
        return samples[-limit:] if limit else samples

    def get_average(self, rig_id: str, last_n: Optional[int] = None) -> float:
        samples = self.get_samples(rig_id, last_n)
        return statistics.mean([s.value for s in samples]) if samples else 0.0

    def get_stddev(self, rig_id: str, last_n: Optional[int] = None) -> float:
        samples = self.get_samples(rig_id, last_n)
        if len(samples) < 2:
            return 0.0
        return statistics.stdev([s.value for s in samples])

    def get_efficiency_trend(self, rig_id: str, last_n: int = 50) -> float:
        samples = self.get_samples(rig_id, last_n)
        if len(samples) < 2:
            return 0.0
        values = [s.value for s in samples]
        n = len(values)
        mean_x = sum(range(n)) / n
        mean_y = sum(values) / n
        numerator = sum((i - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((i - mean_x) ** 2 for i in range(n))
        return numerator / denominator if denominator != 0 else 0.0

    def get_anomalies(self, rig_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            anomalies = list(self._anomalies)
        if rig_id:
            anomalies = [a for a in anomalies if a.get("rig_id") == rig_id]
        return anomalies

    def clear_history(self, rig_id: Optional[str] = None) -> None:
        with self._lock:
            if rig_id:
                self._samples.pop(rig_id, None)
                self._baselines.pop(rig_id, None)
            else:
                self._samples.clear()
                self._baselines.clear()
                self._anomalies.clear()

# =============================================================================
# PROFITABILITY CALCULATOR
# =============================================================================

class ProfitabilityCalculator:
    def __init__(self, electricity_cost_per_kwh: float = 0.12, pool_fee_percentage: float = 1.0):
        self._electricity_cost = electricity_cost_per_kwh
        self._pool_fee = pool_fee_percentage
        self._coin_prices: Dict[str, float] = {}
        self._network_difficulties: Dict[str, float] = {}
        self._block_rewards: Dict[str, float] = {}
        self._historical_prices: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._lock = threading.Lock()

    def update_coin_price(self, coin: str, price: float) -> None:
        with self._lock:
            self._coin_prices[coin] = price
            self._historical_prices[coin].append({"timestamp": datetime.now().isoformat(), "price": price})

    def update_network_difficulty(self, coin: str, difficulty: float) -> None:
        with self._lock:
            self._network_difficulties[coin] = difficulty

    def update_block_reward(self, coin: str, reward: float) -> None:
        with self._lock:
            self._block_rewards[coin] = reward

    def calculate_profitability(self, coin: str, hash_rate: float, power_consumption: float,
                                algorithm: Optional[AlgorithmType] = None,
                                electricity_cost: Optional[float] = None,
                                pool_fee: Optional[float] = None) -> ProfitabilityMetrics:
        algorithm = algorithm or infer_algorithm(coin)
        electricity_cost = electricity_cost if electricity_cost is not None else self._electricity_cost
        pool_fee = pool_fee if pool_fee is not None else self._pool_fee
        with self._lock:
            coin_price = self._coin_prices.get(coin, 0.0)
            difficulty = self._network_difficulties.get(coin, NETWORK_DIFFICULTY.get(coin, 0.0))
            block_reward = self._block_rewards.get(coin, BLOCK_REWARDS.get(coin, 0.0))
        block_time = BLOCK_TIMES.get(coin, 600.0)
        if difficulty <= 0:
            difficulty = NETWORK_DIFFICULTY.get(coin, 1.0)
        network_hash_rate = calculate_network_hash_rate(difficulty, algorithm, block_time)
        daily_hash_seconds = hash_rate * 86400
        expected_daily_coins = (
            (daily_hash_seconds / network_hash_rate) * block_reward if network_hash_rate > 0 else 0.0
        )
        daily_revenue = expected_daily_coins * coin_price
        net_revenue = daily_revenue * (1 - pool_fee / 100.0)
        daily_energy_kwh = (power_consumption / 1000) * 24
        daily_cost = daily_energy_kwh * electricity_cost
        daily_profit = net_revenue - daily_cost
        monthly_profit = daily_profit * 30
        yearly_profit = daily_profit * 365
        roi_days = 0.0 if daily_profit > 0 else float("inf")
        break_even_price = (
            (daily_energy_kwh * electricity_cost) / expected_daily_coins
            if expected_daily_coins > 0 else float("inf")
        )
        efficiency = (power_consumption / hash_rate) if hash_rate > 0 else 0.0
        return ProfitabilityMetrics(
            coin=coin, algorithm=algorithm, hash_rate=hash_rate,
            power_consumption=power_consumption, electricity_cost_per_kwh=electricity_cost,
            network_difficulty=difficulty, block_reward=block_reward,
            daily_revenue=net_revenue, daily_cost=daily_cost, daily_profit=daily_profit,
            monthly_profit=monthly_profit, yearly_profit=yearly_profit, roi_days=roi_days,
            break_even_price=break_even_price, efficiency_j_per_gh=efficiency,
        )

    def compare_coins(self, hash_rate: float, power_consumption: float,
                      coins: Optional[List[str]] = None) -> List[ProfitabilityMetrics]:
        coins = coins or list(NETWORK_DIFFICULTY.keys())
        results = []
        for coin in coins:
            try:
                metrics = self.calculate_profitability(coin, hash_rate, power_consumption)
                results.append(metrics)
            except Exception as e:
                logger.error("Error calculating %s: %s", coin, e)
        results.sort(key=lambda m: m.daily_profit, reverse=True)
        return results

    def get_most_profitable(self, hash_rate: float, power_consumption: float,
                            coins: Optional[List[str]] = None) -> Optional[ProfitabilityMetrics]:
        results = self.compare_coins(hash_rate, power_consumption, coins)
        return results[0] if results else None

    def get_price_volatility(self, coin: str, last_n: int = 100) -> float:
        with self._lock:
            history = list(self._historical_prices.get(coin, []))[-last_n:]
        if len(history) < 2:
            return 0.0
        prices = [h["price"] for h in history]
        returns = [(prices[i] - prices[i - 1]) / prices[i - 1]
                   for i in range(1, len(prices)) if prices[i - 1] > 0]
        return statistics.stdev(returns) if returns else 0.0

    def get_profitability_report(self, operations: List[Dict[str, Any]]) -> Dict[str, Any]:
        metrics_list = []
        for op in operations:
            metrics_list.append(self.calculate_profitability(
                coin=op.get("coin", "bitcoin"), hash_rate=op.get("hash_rate", 0.0),
                power_consumption=op.get("power_consumption", 0.0),
            ))
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_daily_profit": sum(m.daily_profit for m in metrics_list),
                "total_monthly_profit": sum(m.monthly_profit for m in metrics_list),
                "total_power_w": sum(m.power_consumption for m in metrics_list),
                "operations_count": len(metrics_list),
                "profitable_count": sum(1 for m in metrics_list if m.daily_profit > 0),
            },
            "operations": [{
                "coin": m.coin, "algorithm": m.algorithm.name,
                "daily_profit": m.daily_profit, "monthly_profit": m.monthly_profit,
            } for m in metrics_list],
        }

# =============================================================================
# POOL MANAGEMENT
# =============================================================================

class MiningPoolManager:
    def __init__(self):
        self._pools: Dict[str, PoolConfig] = {}
        self._pool_states: Dict[str, Dict[str, Any]] = {}
        self._active_pool: Optional[str] = None
        self._fallback_pools: List[str] = []
        self._latency_tracker: Dict[str, deque] = defaultdict(lambda: deque(maxlen=50))
        self._share_submissions: Dict[str, List[ShareSubmission]] = defaultdict(list)
        self._rewards: Dict[str, List[MiningReward]] = defaultdict(list)
        self._lock = threading.Lock()

    def register_pool(self, config: PoolConfig) -> None:
        with self._lock:
            self._pools[config.pool_name] = config
            self._pool_states[config.pool_name] = {
                "status": PoolStatus.OFFLINE, "workers": 0, "hash_rate": 0.0,
                "last_block": None, "connected_since": None,
                "shares_accepted": 0, "shares_rejected": 0,
            }
            if config.default:
                self._active_pool = config.pool_name
        logger.info("Registered pool: %s (%s)", config.pool_name, config.coin)

    def unregister_pool(self, pool_name: str) -> None:
        with self._lock:
            self._pools.pop(pool_name, None)
            self._pool_states.pop(pool_name, None)
            if self._active_pool == pool_name:
                self._active_pool = None

    def connect_to_pool(self, pool_name: str, worker_name: str, password: str = "x") -> bool:
        if pool_name not in self._pools:
            logger.error("Pool %s not found", pool_name)
            return False
        with self._lock:
            self._pool_states[pool_name]["status"] = PoolStatus.ONLINE
            self._pool_states[pool_name]["connected_since"] = datetime.now().isoformat()
        logger.info("Connected to pool: %s", pool_name)
        return True

    def disconnect_pool(self, pool_name: str) -> None:
        with self._lock:
            if pool_name in self._pool_states:
                self._pool_states[pool_name]["status"] = PoolStatus.OFFLINE
                self._pool_states[pool_name]["connected_since"] = None
        logger.info("Disconnected from pool: %s", pool_name)

    def set_active_pool(self, pool_name: str) -> bool:
        with self._lock:
            if pool_name not in self._pools:
                return False
            self._active_pool = pool_name
            self._fallback_pools = [p for p in self._pools if p != pool_name]
        logger.info("Active pool set to: %s", pool_name)
        return True

    def get_active_pool(self) -> Optional[str]:
        with self._lock:
            return self._active_pool

    def record_latency(self, pool_name: str, latency_ms: float) -> None:
        with self._lock:
            self._latency_tracker[pool_name].append(latency_ms)
            if pool_name in self._pool_states:
                avg = statistics.mean(list(self._latency_tracker[pool_name]))
                self._pool_states[pool_name]["avg_latency_ms"] = avg
                if avg > 500:
                    self._pool_states[pool_name]["status"] = PoolStatus.HIGH_LATENCY

    def get_average_latency(self, pool_name: str) -> float:
        with self._lock:
            samples = list(self._latency_tracker.get(pool_name, []))
        return statistics.mean(samples) if samples else 0.0

    def record_share(self, pool_name: str, rig_id: str, difficulty: float,
                     valid: bool = True, block_candidate: bool = False,
                     latency_ms: float = 0.0) -> ShareSubmission:
        submission = ShareSubmission(
            share_id=str(uuid.uuid4()), rig_id=rig_id, pool_name=pool_name,
            difficulty=difficulty, valid=valid, block_candidate=block_candidate, latency_ms=latency_ms,
        )
        with self._lock:
            self._share_submissions[pool_name].append(submission)
            if pool_name in self._pool_states:
                if valid:
                    self._pool_states[pool_name]["shares_accepted"] += 1
                else:
                    self._pool_states[pool_name]["shares_rejected"] += 1
        return submission

    def record_reward(self, reward: MiningReward) -> None:
        with self._lock:
            self._rewards[reward.coin].append(reward)

    def get_pool_stats(self, pool_name: str) -> Dict[str, Any]:
        with self._lock:
            return dict(self._pool_states.get(pool_name, {}))

    def get_all_pool_stats(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return {k: dict(v) for k, v in self._pool_states.items()}

    def get_best_pool(self, algorithm: AlgorithmType) -> Optional[str]:
        candidates = []
        with self._lock:
            for name, config in self._pools.items():
                if config.algorithm != algorithm:
                    continue
                state = self._pool_states.get(name, {})
                if state.get("status") == PoolStatus.OFFLINE:
                    continue
                avg_latency = self.get_average_latency(name)
                score = avg_latency + (config.fee_percentage * 10)
                candidates.append((name, score))
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[1])
        return candidates[0][0]

    def get_pool_health(self) -> Dict[str, str]:
        with self._lock:
            return {name: state.get("status", PoolStatus.OFFLINE).name
                    for name, state in self._pool_states.items()}

    def update_pool_status(self, pool_name: str, status: PoolStatus) -> None:
        with self._lock:
            if pool_name in self._pool_states:
                self._pool_states[pool_name]["status"] = status

    def get_total_revenue(self, coin: str) -> float:
        with self._lock:
            return sum(r.amount for r in self._rewards.get(coin, []))

# =============================================================================
# POOL SWITCHING STRATEGIES
# =============================================================================

class PoolSwitchingStrategy(ABC):
    @abstractmethod
    def should_switch(self, current_pool: Optional[str], available_pools: List[str],
                      metrics: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        pass

class LatencyBasedSwitching(PoolSwitchingStrategy):
    def __init__(self, max_latency_ms: float = 200.0, min_switch_interval: float = 300.0):
        self._max_latency = max_latency_ms
        self._min_interval = min_switch_interval
        self._last_switch: Dict[str, float] = {}
        self._lock = threading.Lock()

    def should_switch(self, current_pool, available_pools, metrics):
        with self._lock:
            now = time.time()
            if current_pool and current_pool in self._last_switch:
                if now - self._last_switch[current_pool] < self._min_interval:
                    return False, None
            latency_data = metrics.get("pool_latencies", {})
            best_pool, best_latency = current_pool, float("inf")
            for pool in available_pools:
                latency = latency_data.get(pool, float("inf"))
                if latency < best_latency:
                    best_latency = latency
                    best_pool = pool
            if best_latency > self._max_latency and best_pool != current_pool and best_pool:
                self._last_switch[best_pool] = now
                return True, best_pool
            return False, None

class ProfitabilityBasedSwitching(PoolSwitchingStrategy):
    def __init__(self, min_profit_delta: float = 0.05, min_switch_interval: float = 600.0):
        self._min_delta = min_profit_delta
        self._min_interval = min_switch_interval
        self._last_switch: Dict[str, float] = {}
        self._lock = threading.Lock()

    def should_switch(self, current_pool, available_pools, metrics):
        with self._lock:
            now = time.time()
            if current_pool and current_pool in self._last_switch:
                if now - self._last_switch[current_pool] < self._min_interval:
                    return False, None
            profitability = metrics.get("pool_profitability", {})
            if not profitability:
                return False, None
            current_profit = profitability.get(current_pool, 0.0)
            best_pool, best_profit = current_pool, current_profit
            for pool, profit in profitability.items():
                if profit > best_profit:
                    best_profit = profit
                    best_pool = pool
            if best_pool != current_pool:
                delta = (best_profit - current_profit) / current_profit if current_profit > 0 else 1.0
                if delta >= self._min_delta:
                    self._last_switch[best_pool] = now
                    return True, best_pool
            return False, None

class CompositeSwitchingStrategy(PoolSwitchingStrategy):
    def __init__(self, strategies: Optional[List[PoolSwitchingStrategy]] = None,
                 weights: Optional[List[float]] = None):
        self._strategies = strategies or []
        self._weights = weights or [1.0] * len(self._strategies)

    def should_switch(self, current_pool, available_pools, metrics):
        switch_votes: Dict[str, int] = defaultdict(int)
        for strategy, weight in zip(self._strategies, self._weights):
            try:
                should, target = strategy.should_switch(current_pool, available_pools, metrics)
                if should and target:
                    switch_votes[target] += weight
            except Exception as e:
                logger.error("Strategy error: %s", e)
        if not switch_votes:
            return False, None
        best_pool = max(switch_votes, key=switch_votes.get)
        return True, best_pool

class PoolSwitchingEngine:
    def __init__(self, strategy: Optional[PoolSwitchingStrategy] = None):
        self._strategy = strategy or LatencyBasedSwitching()
        self._available_pools: List[str] = []
        self._metrics_buffer: deque = deque(maxlen=100)
        self._lock = threading.Lock()
        self._switch_history: List[Dict[str, Any]] = []

    def set_strategy(self, strategy: PoolSwitchingStrategy) -> None:
        with self._lock:
            self._strategy = strategy

    def record_metrics(self, metrics: Dict[str, Any]) -> None:
        with self._lock:
            self._metrics_buffer.append({"timestamp": datetime.now().isoformat(), **metrics})

    def evaluate_switch(self, current_pool: Optional[str]) -> Tuple[bool, Optional[str]]:
        with self._lock:
            metrics = dict(self._metrics_buffer[-1]) if self._metrics_buffer else {}
            available = list(self._available_pools)
        should_switch, target = self._strategy.should_switch(current_pool, available, metrics)
        if should_switch and target:
            with self._lock:
                self._switch_history.append({
                    "from": current_pool, "to": target,
                    "timestamp": datetime.now().isoformat(), "reason": "strategy_decision",
                })
        return should_switch, target

    def get_switch_history(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._switch_history)

# =============================================================================
# REWARD ANALYZER
# =============================================================================

class RewardAnalyzer:
    def __init__(self):
        self._rewards: List[MiningReward] = []
        self._payout_history: Dict[str, List[float]] = defaultdict(list)
        self._expected_rewards: Dict[str, float] = {}
        self._lock = threading.Lock()

    def add_reward(self, reward: MiningReward) -> None:
        with self._lock:
            self._rewards.append(reward)
            self._payout_history[reward.coin].append(reward.amount)

    def add_expected_reward(self, coin: str, expected_daily: float) -> None:
        with self._lock:
            self._expected_rewards[coin] = expected_daily

    def get_total_rewards(self, coin: Optional[str] = None) -> List[MiningReward]:
        with self._lock:
            rewards = list(self._rewards)
        return [r for r in rewards if r.coin == coin] if coin else rewards

    def get_total_revenue(self, coin: Optional[str] = None) -> float:
        return sum(r.amount for r in self.get_total_rewards(coin))

    def get_average_payout(self, coin: str) -> float:
        with self._lock:
            payouts = self._payout_history.get(coin, [])
        return statistics.mean(payouts) if payouts else 0.0

    def get_payout_variance(self, coin: str) -> float:
        with self._lock:
            payouts = self._payout_history.get(coin, [])
        return statistics.variance(payouts) if len(payouts) >= 2 else 0.0

    def get_reward_frequency(self, coin: str, hours: int = 24) -> int:
        cutoff = datetime.now() - timedelta(hours=hours)
        with self._lock:
            return sum(1 for r in self._rewards if r.coin == coin and r.timestamp >= cutoff)

    def get_fee_efficiency(self, coin: str) -> float:
        with self._lock:
            coin_rewards = [r for r in self._rewards if r.coin == coin]
        if not coin_rewards:
            return 0.0
        gross = sum(r.amount + r.pool_fee for r in coin_rewards)
        net = sum(r.amount for r in coin_rewards)
        return net / gross if gross > 0 else 0.0

    def get_reward_distribution_report(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {"timestamp": datetime.now().isoformat(), "coins": {}, "total_revenue": 0.0}
        with self._lock:
            coin_rewards: Dict[str, List[MiningReward]] = defaultdict(list)
            for r in self._rewards:
                coin_rewards[r.coin].append(r)
            for coin, rewards in coin_rewards.items():
                total = sum(r.amount for r in rewards)
                fees = sum(r.pool_fee for r in rewards)
                report["coins"][coin] = {
                    "count": len(rewards), "total_revenue": total, "total_fees": fees,
                    "avg_reward": total / len(rewards) if rewards else 0.0,
                }
                report["total_revenue"] += total
        return report

# =============================================================================
# ENERGY TRACKER
# =============================================================================

class EnergyConsumptionTracker:
    def __init__(self, cost_per_kwh: float = 0.12):
        self._cost_per_kwh = cost_per_kwh
        self._readings: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._daily_totals: Dict[str, Dict[str, float]] = defaultdict(lambda: {"total_kwh": 0.0, "cost": 0.0})
        self._optimization_targets: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._carbon_factor = 0.475

    def record_reading(self, reading: EnergyReading) -> None:
        with self._lock:
            self._readings[reading.rig_id].append(reading)
            date_key = reading.timestamp.strftime("%Y-%m-%d")
            kwh = reading.power_draw * (1 / 1000) * (1 / 3600)
            self._daily_totals[reading.rig_id][date_key] += kwh

    def set_optimization_target(self, rig_id: str, target_kwh_per_day: float) -> None:
        with self._lock:
            self._optimization_targets[rig_id] = target_kwh_per_day

    def get_daily_consumption(self, rig_id: str, date: Optional[datetime] = None) -> float:
        date = date or datetime.now()
        with self._lock:
            return self._daily_totals.get(rig_id, {}).get(date.strftime("%Y-%m-%d"), 0.0)

    def get_total_daily_consumption(self) -> float:
        total = 0.0
        today = datetime.now().strftime("%Y-%m-%d")
        with self._lock:
            for rig_totals in self._daily_totals.values():
                total += rig_totals.get(today, 0.0)
        return total

    def get_total_monthly_cost(self) -> float:
        return self.get_total_daily_consumption() * 30 * self._cost_per_kwh

    def get_efficiency_rating(self, rig_id: str) -> str:
        readings = self.get_readings(rig_id, limit=10)
        if not readings:
            return "unknown"
        avg_power = statistics.mean([r.power_draw for r in readings])
        target = self._optimization_targets.get(rig_id)
        if target and avg_power > target * 1.2:
            return "poor"
        if target and avg_power > target:
            return "fair"
        return "good"

    def get_carbon_footprint(self, kwh: float) -> float:
        return kwh * self._carbon_factor

    def get_optimization_suggestions(self, rig_id: str) -> List[str]:
        suggestions = []
        readings = self.get_readings(rig_id, limit=20)
        if not readings:
            return suggestions
        avg_power = statistics.mean([r.power_draw for r in readings])
        target = self._optimization_targets.get(rig_id)
        if target and avg_power > target:
            suggestions.append(f"Reduce power target from {avg_power:.0f}W to {target:.0f}W")
        if target and avg_power < target * 0.8:
            suggestions.append("Consider increasing power limit for better hash rate")
        return suggestions

    def get_readings(self, rig_id: str, limit: int = 100) -> List[EnergyReading]:
        with self._lock:
            return list(self._readings.get(rig_id, []))[-limit:]

    def get_energy_report(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(), "cost_per_kwh": self._cost_per_kwh,
            "total_monthly_cost_estimate": self.get_total_monthly_cost(),
            "daily_consumption_kwh": self.get_total_daily_consumption(), "rigs": {},
        }
        with self._lock:
            for rig_id, readings in self._readings.items():
                if readings:
                    latest = readings[-1]
                    report["rigs"][rig_id] = {
                        "current_power_w": latest.power_draw, "efficiency": latest.efficiency,
                        "rating": self.get_efficiency_rating(rig_id),
                    }
        report["carbon_footprint_kg_monthly"] = self.get_carbon_footprint(report["daily_consumption_kwh"] * 30)
        return report

# =============================================================================
# RIG MANAGER
# =============================================================================

class MiningRigManager:
    def __init__(self):
        self._rigs: Dict[str, RigHardware] = {}
        self._rig_states: Dict[str, RigState] = {}
        self._lock = threading.Lock()
        self._maintenance_schedule: Dict[str, datetime] = {}

    def add_rig(self, hardware: RigHardware) -> None:
        with self._lock:
            self._rigs[hardware.rig_id] = hardware
            self._rig_states[hardware.rig_id] = RigState(
                rig_id=hardware.rig_id, status=RigStatus.OFFLINE,
                current_hash_rate=0.0, target_hash_rate=hardware.hash_rate,
            )
        logger.info("Added rig %s (%s)", hardware.rig_id, hardware.model)

    def remove_rig(self, rig_id: str) -> None:
        with self._lock:
            self._rigs.pop(rig_id, None)
            self._rig_states.pop(rig_id, None)
            self._maintenance_schedule.pop(rig_id, None)

    def get_rig(self, rig_id: str) -> Optional[RigHardware]:
        with self._lock:
            return self._rigs.get(rig_id)

    def start_rig(self, rig_id: str) -> bool:
        with self._lock:
            if rig_id not in self._rigs:
                return False
            self._rig_states[rig_id].status = RigStatus.MINING
            self._rig_states[rig_id].uptime_seconds = 0
        logger.info("Started rig %s", rig_id)
        return True

    def stop_rig(self, rig_id: str) -> bool:
        with self._lock:
            if rig_id not in self._rigs:
                return False
            self._rig_states[rig_id].status = RigStatus.IDLE
        logger.info("Stopped rig %s", rig_id)
        return True

    def restart_rig(self, rig_id: str) -> bool:
        self.stop_rig(rig_id)
        time.sleep(2)
        return self.start_rig(rig_id)

    def set_rig_power_limit(self, rig_id: str, power_limit_w: float) -> bool:
        with self._lock:
            if rig_id not in self._rigs:
                return False
            hardware = self._rigs[rig_id]
            self._rig_states[rig_id].target_hash_rate = (
                hardware.hash_rate * (power_limit_w / hardware.power_consumption)
            )
        return True

    def get_fleet_summary(self) -> Dict[str, Any]:
        with self._lock:
            total_hash_rate = sum(hw.hash_rate for hw in self._rigs.values())
            total_power = sum(hw.power_consumption for hw in self._rigs.values())
            active = sum(1 for s in self._rig_states.values() if s.status == RigStatus.MINING)
            by_algorithm: Dict[str, int] = defaultdict(int)
            by_hardware: Dict[str, int] = defaultdict(int)
            for hw in self._rigs.values():
                by_algorithm[hw.algorithm.name] += 1
                by_hardware[hw.hardware_type.name] += 1
        return {
            "total_rigs": len(self._rigs), "active_rigs": active,
            "total_hash_rate_th_s": total_hash_rate, "total_power_w": total_power,
            "by_algorithm": dict(by_algorithm), "by_hardware_type": dict(by_hardware),
        }

    def get_rig_health_score(self, rig_id: str) -> float:
        with self._lock:
            state = self._rig_states.get(rig_id)
            hardware = self._rigs.get(rig_id)
        if not state or not hardware:
            return 0.0
        score = 1.0
        if state.status != RigStatus.MINING:
            score -= 0.3
        if state.rejected_shares > 0:
            ratio = state.rejected_shares / max(1, state.accepted_shares + state.rejected_shares)
            score -= ratio * 0.3
        if state.current_hash_rate > 0 and hardware.hash_rate > 0:
            hr_ratio = state.current_hash_rate / hardware.hash_rate
            if hr_ratio < 0.9:
                score -= (0.9 - hr_ratio) * 0.4
        if state.temperature > 80:
            score -= 0.2
        return max(0.0, min(1.0, score))

    def schedule_maintenance(self, rig_id: str, date: datetime) -> bool:
        with self._lock:
            if rig_id not in self._rigs:
                return False
            self._maintenance_schedule[rig_id] = date
        return True

# =============================================================================
# ALGORITHM SELECTOR
# =============================================================================

class AlgorithmSelector:
    def __init__(self):
        self._profiles: Dict[AlgorithmType, Dict[str, Any]] = {
            AlgorithmType.SHA256: {
                "name": "SHA-256", "memory_intensive": False, "asic_optimized": True,
                "gpu_feasible": True, "coins": ["bitcoin", "bitcoin_cash", "dogecoin"],
                "asic_advantage": 10000,
            },
            AlgorithmType.ETHASH: {
                "name": "Ethash", "memory_intensive": True, "asic_optimized": False,
                "gpu_feasible": True, "coins": ["ethereum_classic", "flux"],
                "asic_advantage": 1,
            },
            AlgorithmType.SCRYPT: {
                "name": "Scrypt", "memory_intensive": True, "asic_optimized": True,
                "gpu_feasible": True, "coins": ["litecoin", "dogecoin"],
                "asic_advantage": 1000,
            },
            AlgorithmType.RANDOMX: {
                "name": "RandomX", "memory_intensive": True, "asic_optimized": False,
                "gpu_feasible": False, "coins": ["monero"], "asic_advantage": 1,
            },
            AlgorithmType.KAWPOW: {
                "name": "KawPow", "memory_intensive": True, "asic_optimized": False,
                "gpu_feasible": True, "coins": ["ravencoin"], "asic_advantage": 1,
            },
        }

    def select_algorithm(self, hardware_type: HardwareType, available_memory_gb: float,
                         power_budget_w: float) -> AlgorithmType:
        candidates = []
        for algo, profile in self._profiles.items():
            if hardware_type == HardwareType.ASIC and not profile["asic_optimized"]:
                continue
            if hardware_type in (HardwareType.GPU_NVIDIA, HardwareType.GPU_AMD) and not profile["gpu_feasible"]:
                continue
            if profile["memory_intensive"] and available_memory_gb < 4:
                continue
            candidates.append((algo, profile["asic_advantage"]))
        if not candidates:
            return AlgorithmType.SHA256
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

    def get_compatible_algorithms(self, hardware_type: HardwareType) -> List[AlgorithmType]:
        compatible = []
        for algo, profile in self._profiles.items():
            if hardware_type == HardwareType.ASIC and profile["asic_optimized"]:
                compatible.append(algo)
            elif hardware_type in (HardwareType.GPU_NVIDIA, HardwareType.GPU_AMD) and profile["gpu_feasible"]:
                compatible.append(algo)
            elif hardware_type == HardwareType.CPU:
                compatible.append(algo)
        return compatible

    def get_algorithm_profile(self, algorithm: AlgorithmType) -> Dict[str, Any]:
        return dict(self._profiles.get(algorithm, {}))

    def estimate_hash_rate(self, algorithm: AlgorithmType, hardware_type: HardwareType,
                           hardware_model: str) -> float:
        lookup_key = hardware_model.lower().replace(" ", "_")
        hw_data = HARDWARE_HASH_RATES.get(lookup_key)
        if hw_data and hw_data["algorithm"] == algorithm:
            return hw_data["hash_rate"]
        defaults = {
            HardwareType.ASIC: {AlgorithmType.SHA256: 100.0, AlgorithmType.SCRYPT: 5.0},
            HardwareType.GPU_NVIDIA: {AlgorithmType.KAWPOW: 80.0, AlgorithmType.ETHASH: 60.0},
            HardwareType.GPU_AMD: {AlgorithmType.KAWPOW: 70.0, AlgorithmType.ETHASH: 55.0},
        }
        return defaults.get(hardware_type, {}).get(algorithm, 0.0)

# =============================================================================
# MINING OPTIMIZER
# =============================================================================

class MiningOptimizer:
    def __init__(self, profitability_calculator: Optional[ProfitabilityCalculator] = None,
                 hardware_monitor: Optional[HardwareMonitor] = None):
        self._profitability = profitability_calculator or ProfitabilityCalculator()
        self._hardware_monitor = hardware_monitor or HardwareMonitor()
        self._optimization_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def optimize_fleet(self, rig_ids: List[str]) -> Dict[str, Any]:
        results = {"timestamp": datetime.now().isoformat(), "rigs": {}, "fleet_actions": []}
        for rig_id in rig_ids:
            rig_result = self._optimize_single_rig(rig_id)
            results["rigs"][rig_id] = rig_result
            if rig_result.get("action_required"):
                results["fleet_actions"].append({"rig_id": rig_id, "action": rig_result["action_required"]})
        return results

    def _optimize_single_rig(self, rig_id: str) -> Dict[str, Any]:
        state = self._hardware_monitor.get_rig_state(rig_id)
        if not state:
            return {"error": "rig_not_found"}
        result = {
            "rig_id": rig_id, "current_hash_rate": state.current_hash_rate,
            "target_hash_rate": state.target_hash_rate, "status": state.status.name,
            "temperature": state.temperature, "action_required": None, "suggestions": [],
        }
        if state.temperature > 85:
            result["action_required"] = "reduce_power"
            result["suggestions"].append(f"High temperature ({state.temperature:.1f}C)")
        elif state.temperature < 50 and state.status == RigStatus.MINING:
            result["suggestions"].append("Low temperature: consider increasing power limit")
        if state.current_hash_rate < state.target_hash_rate * 0.9:
            result["action_required"] = "check_hardware"
        return result

    def optimize_power_allocation(self, rig_ids: List[str], total_power_budget_w: float) -> Dict[str, float]:
        rigs_data = []
        for rig_id in rig_ids:
            state = self._hardware_monitor.get_rig_state(rig_id)
            if state:
                efficiency = state.current_hash_rate / max(1, state.temperature)
                rigs_data.append({"rig_id": rig_id, "current_power": state.temperature * 10, "efficiency": efficiency})
        rigs_data.sort(key=lambda r: r["efficiency"], reverse=True)
        allocation: Dict[str, float] = {}
        remaining = total_power_budget_w
        for rig in rigs_data:
            allocated = min(rig["current_power"], remaining)
            allocation[rig["rig_id"]] = allocated
            remaining -= allocated
        return allocation

    def record_optimization(self, optimization_type: str, details: Dict[str, Any]) -> None:
        with self._lock:
            self._optimization_history.append({
                "type": optimization_type, "timestamp": datetime.now().isoformat(), **details,
            })

# =============================================================================
# MINING ECONOMICS
# =============================================================================

class MiningEconomics:
    def __init__(self, initial_investment: float = 0.0, electricity_cost_per_kwh: float = 0.12):
        self._initial_investment = initial_investment
        self._electricity_cost = electricity_cost_per_kwh
        self._hardware_costs: Dict[str, float] = {}
        self._operational_costs: Dict[str, deque] = defaultdict(lambda: deque(maxlen=365))
        self._revenue_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=365))
        self._lock = threading.Lock()

    def set_initial_investment(self, amount: float) -> None:
        with self._lock:
            self._initial_investment = amount

    def add_hardware_cost(self, rig_id: str, cost: float) -> None:
        with self._lock:
            self._hardware_costs[rig_id] = cost
            self._initial_investment += cost

    def record_operational_cost(self, rig_id: str, cost: float, date: Optional[datetime] = None) -> None:
        with self._lock:
            self._operational_costs[rig_id].append({"date": (date or datetime.now()).isoformat(), "cost": cost})

    def record_revenue(self, rig_id: str, revenue: float, date: Optional[datetime] = None) -> None:
        with self._lock:
            self._revenue_history[rig_id].append({"date": (date or datetime.now()).isoformat(), "revenue": revenue})

    def calculate_roi(self, total_revenue: float, period_days: int = 30) -> Dict[str, float]:
        with self._lock:
            costs = self._initial_investment
            for c_list in self._operational_costs.values():
                for c in list(c_list)[-period_days:]:
                    costs += c.get("cost", 0.0)
        net = total_revenue - costs
        return {
            "total_revenue": total_revenue, "total_costs": costs, "net_profit": net,
            "roi_percent": (net / costs * 100) if costs > 0 else 0.0, "period_days": period_days,
        }

    def calculate_break_even(self, monthly_revenue: float, monthly_costs: float) -> int:
        if monthly_revenue <= monthly_costs:
            return -1
        net_monthly = monthly_revenue - monthly_costs
        remaining = self._initial_investment
        months = 0
        while remaining > 0 and months < 1200:
            remaining -= net_monthly
            months += 1
        return months

    def get_cashflow_projection(self, monthly_revenue: float, monthly_costs: float,
                                months: int = 12) -> List[Dict[str, float]]:
        projection = []
        cumulative = -self._initial_investment
        for m in range(1, months + 1):
            cumulative += monthly_revenue - monthly_costs
            projection.append({
                "month": m, "revenue": monthly_revenue, "costs": monthly_costs,
                "net": monthly_revenue - monthly_costs, "cumulative": cumulative,
            })
        return projection

    def get_risk_analysis(self, volatility: float, hash_rate_growth: float = 0.0,
                          difficulty_growth: float = 0.0) -> Dict[str, Any]:
        base_risk = volatility * 100
        if difficulty_growth > 0.1:
            base_risk += 15
        if hash_rate_growth > 0.2:
            base_risk += 10
        risk_level = "low"
        if base_risk > 60:
            risk_level = "high"
        elif base_risk > 30:
            risk_level = "medium"
        return {"risk_score": base_risk, "risk_level": risk_level, "volatility_impact": volatility * 100}

    def get_economics_summary(self) -> Dict[str, Any]:
        with self._lock:
            total_revenue = sum(sum(r.get("revenue", 0.0) for r in list(revs)[-30:])
                               for revs in self._revenue_history.values())
            total_costs = self._initial_investment + sum(
                sum(c.get("cost", 0.0) for c in list(costs)[-30:])
                for costs in self._operational_costs.values()
            )
        net = total_revenue - total_costs
        return {
            "initial_investment": self._initial_investment,
            "total_revenue_30d": total_revenue, "total_costs_30d": total_costs,
            "net_profit_30d": net,
            "roi_30d_percent": (net / total_costs * 100) if total_costs > 0 else 0.0,
        }

# =============================================================================
# CONFIG
# =============================================================================

class Config:
    def __init__(self, electricity_cost_per_kwh: float = 0.12, default_algorithm: AlgorithmType = AlgorithmType.SHA256,
                 temperature_unit: TemperatureUnit = TemperatureUnit.CELSIUS, hash_rate_unit: HashRateUnit = HashRateUnit.THPS,
                 monitor_poll_interval: float = 5.0, auto_switch_pools: bool = True,
                 max_temperature: float = 85.0, power_budget_w: float = 5000.0):
        self.electricity_cost_per_kwh = electricity_cost_per_kwh
        self.default_algorithm = default_algorithm
        self.temperature_unit = temperature_unit
        self.hash_rate_unit = hash_rate_unit
        self.monitor_poll_interval = monitor_poll_interval
        self.auto_switch_pools = auto_switch_pools
        self.max_temperature = max_temperature
        self.power_budget_w = power_budget_w

# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class CryptoMiningAgent:
    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._rigs: List[RigHardware] = []
        self._pool_manager = MiningPoolManager()
        self._profitability = ProfitabilityCalculator(
            electricity_cost_per_kwh=self._config.electricity_cost_per_kwh,
        )
        self._hardware_monitor = HardwareMonitor(poll_interval_seconds=self._config.monitor_poll_interval)
        self._hash_rate_tracker = HashRateTracker()
        self._reward_analyzer = RewardAnalyzer()
        self._energy_tracker = EnergyConsumptionTracker(cost_per_kwh=self._config.electricity_cost_per_kwh)
        self._rig_manager = MiningRigManager()
        self._algorithm_selector = AlgorithmSelector()
        self._optimizer = MiningOptimizer(
            profitability_calculator=self._profitability, hardware_monitor=self._hardware_monitor,
        )
        self._pool_switcher = PoolSwitchingEngine(strategy=LatencyBasedSwitching())
        self._economics = MiningEconomics(electricity_cost_per_kwh=self._config.electricity_cost_per_kwh)
        self._running = False
        self._lock = threading.Lock()

    def initialize(self) -> Dict[str, Any]:
        logger.info("Initializing CryptoMiningAgent")
        self._hardware_monitor.start_monitoring()
        self._running = True
        return {"status": "initialized", "rigs_registered": len(self._rigs), "config": {
            "electricity_cost_per_kwh": self._config.electricity_cost_per_kwh,
            "max_temperature": self._config.max_temperature,
            "power_budget_w": self._config.power_budget_w,
        }}

    def shutdown(self) -> Dict[str, Any]:
        self._running = False
        self._hardware_monitor.stop_monitoring()
        logger.info("CryptoMiningAgent shutdown complete")
        return {"status": "shutdown"}

    def register_pool(self, pool_name: str, coin: str, algorithm: AlgorithmType,
                      endpoints: List[PoolEndpoint], reward_type: RewardType = RewardType.PPS,
                      fee_percentage: float = 1.0, default: bool = False) -> Dict[str, Any]:
        config = PoolConfig(pool_name=pool_name, coin=coin, algorithm=algorithm,
                            endpoints=endpoints, reward_type=reward_type,
                            fee_percentage=fee_percentage, default=default)
        self._pool_manager.register_pool(config)
        return {"status": "registered", "pool": pool_name}

    def connect_pool(self, pool_name: str, worker_name: str, password: str = "x") -> Dict[str, Any]:
        success = self._pool_manager.connect_to_pool(pool_name, worker_name, password)
        return {"status": "connected" if success else "failed", "pool": pool_name}

    def disconnect_pool(self, pool_name: str) -> Dict[str, Any]:
        self._pool_manager.disconnect_pool(pool_name)
        return {"status": "disconnected", "pool": pool_name}

    def get_active_pool(self) -> Optional[str]:
        return self._pool_manager.get_active_pool()

    def set_active_pool(self, pool_name: str) -> Dict[str, Any]:
        success = self._pool_manager.set_active_pool(pool_name)
        return {"status": "success" if success else "failed", "pool": pool_name}

    def get_pool_stats(self, pool_name: str) -> Dict[str, Any]:
        return self._pool_manager.get_pool_stats(pool_name)

    def get_pool_health(self) -> Dict[str, str]:
        return self._pool_manager.get_pool_health()

    def register_rig(self, rig_id: str, model: str, hardware_type: HardwareType,
                     algorithm: AlgorithmType, hash_rate: float, power_consumption: float,
                     unit_cost: float = 0.0) -> Dict[str, Any]:
        hardware = RigHardware(rig_id=rig_id, hardware_type=hardware_type, model=model,
                               algorithm=algorithm, hash_rate=hash_rate,
                               power_consumption=power_consumption, unit_cost=unit_cost)
        self._rigs.append(hardware)
        self._rig_manager.add_rig(hardware)
        self._hardware_monitor.register_rig(hardware)
        self._hash_rate_tracker.set_baseline(rig_id, hash_rate)
        return {"status": "registered", "rig_id": rig_id, "model": model, "hash_rate": hash_rate}

    def start_rig(self, rig_id: str) -> Dict[str, Any]:
        success = self._rig_manager.start_rig(rig_id)
        self._hardware_monitor.update_rig_status(rig_id, RigStatus.MINING if success else RigStatus.ERROR)
        return {"status": "started" if success else "failed", "rig_id": rig_id}

    def stop_rig(self, rig_id: str) -> Dict[str, Any]:
        success = self._rig_manager.stop_rig(rig_id)
        self._hardware_monitor.update_rig_status(rig_id, RigStatus.IDLE if success else RigStatus.ERROR)
        return {"status": "stopped" if success else "failed", "rig_id": rig_id}

    def restart_rig(self, rig_id: str) -> Dict[str, Any]:
        success = self._rig_manager.restart_rig(rig_id)
        return {"status": "restarted" if success else "failed", "rig_id": rig_id}

    def remove_rig(self, rig_id: str) -> Dict[str, Any]:
        self._rig_manager.remove_rig(rig_id)
        self._hardware_monitor.unregister_rig(rig_id)
        self._rigs = [r for r in self._rigs if r.rig_id != rig_id]
        return {"status": "removed", "rig_id": rig_id}

    def get_rig_status(self, rig_id: str) -> Dict[str, Any]:
        state = self._hardware_monitor.get_rig_state(rig_id)
        if not state:
            return {"error": "rig_not_found"}
        health = self._rig_manager.get_rig_health_score(rig_id)
        return {
            "rig_id": rig_id, "status": state.status.name,
            "hash_rate": state.current_hash_rate, "target_hash_rate": state.target_hash_rate,
            "temperature": state.temperature, "uptime_seconds": state.uptime_seconds,
            "accepted_shares": state.accepted_shares, "rejected_shares": state.rejected_shares,
            "health_score": health,
        }

    def get_fleet_status(self) -> Dict[str, Any]:
        return self._rig_manager.get_fleet_summary()

    def analyze_profitability(self, coin: str, hash_rate: Optional[float] = None,
                              power_consumption: Optional[float] = None,
                              algorithm: Optional[AlgorithmType] = None) -> Dict[str, Any]:
        hash_rate = hash_rate or 100.0
        power_consumption = power_consumption or 3000.0
        metrics = self._profitability.calculate_profitability(coin, hash_rate, power_consumption, algorithm)
        return {
            "coin": metrics.coin, "algorithm": metrics.algorithm.name,
            "daily_revenue": metrics.daily_revenue, "daily_cost": metrics.daily_cost,
            "daily_profit": metrics.daily_profit, "monthly_profit": metrics.monthly_profit,
            "yearly_profit": metrics.yearly_profit, "break_even_price": metrics.break_even_price,
        }

    def compare_profitability(self, hash_rate: float, power_consumption: float,
                              coins: Optional[List[str]] = None) -> Dict[str, Any]:
        results = self._profitability.compare_coins(hash_rate, power_consumption, coins)
        return {
            "comparisons": [{"coin": r.coin, "algorithm": r.algorithm.name,
                             "daily_profit": r.daily_profit, "monthly_profit": r.monthly_profit}
                            for r in results],
            "most_profitable": results[0].coin if results else None,
        }

    def update_coin_price(self, coin: str, price: float) -> Dict[str, Any]:
        self._profitability.update_coin_price(coin, price)
        return {"status": "updated", "coin": coin, "price": price}

    def update_network_difficulty(self, coin: str, difficulty: float) -> Dict[str, Any]:
        self._profitability.update_network_difficulty(coin, difficulty)
        return {"status": "updated", "coin": coin, "difficulty": difficulty}

    def get_temperature_readings(self, rig_id: str) -> Dict[str, Any]:
        monitor = self._hardware_monitor._temp_monitors.get(rig_id)
        if not monitor:
            return {"error": "rig_not_found"}
        readings = monitor.get_all_readings()
        return {
            "rig_id": rig_id,
            "readings": {sid: {"value": r.value, "component": r.component,
                               "warning": r.warning, "critical": r.critical}
                         for sid, r in readings.items()},
            "average": monitor.get_average_temperature(),
            "max": monitor.get_max_temperature(), "safe": monitor.is_safe(),
        }

    def get_hardware_health_report(self) -> Dict[str, Any]:
        return self._hardware_monitor.get_health_report()

    def record_hash_rate(self, rig_id: str, value: float,
                         unit: HashRateUnit = HashRateUnit.THPS) -> Dict[str, Any]:
        sample = self._hash_rate_tracker.record_sample(rig_id, value, unit)
        return {"status": "recorded", "rig_id": rig_id, "value": sample.value, "unit": sample.unit.name}

    def get_hash_rate_history(self, rig_id: str, limit: int = 100) -> Dict[str, Any]:
        samples = self._hash_rate_tracker.get_samples(rig_id, limit)
        return {
            "rig_id": rig_id,
            "samples": [{"timestamp": s.timestamp.isoformat(), "value": s.value,
                         "unit": s.unit.name, "valid": s.valid} for s in samples],
            "average": self._hash_rate_tracker.get_average(rig_id),
            "stddev": self._hash_rate_tracker.get_stddev(rig_id),
        }

    def record_energy_reading(self, rig_id: str, power_draw: float, efficiency: float = 0.0,
                              cost_per_kwh: Optional[float] = None) -> Dict[str, Any]:
        reading = EnergyReading(rig_id=rig_id, power_draw=power_draw, efficiency=efficiency,
                                cost_per_kwh=cost_per_kwh or self._config.electricity_cost_per_kwh)
        reading.daily_cost = (power_draw / 1000) * 24 * reading.cost_per_kwh
        reading.monthly_cost = reading.daily_cost * 30
        self._energy_tracker.record_reading(reading)
        self._hardware_monitor.record_energy(reading)
        return {"status": "recorded", "rig_id": rig_id, "power_w": power_draw,
                "daily_cost": reading.daily_cost, "monthly_cost": reading.monthly_cost}

    def get_energy_report(self) -> Dict[str, Any]:
        return self._energy_tracker.get_energy_report()

    def record_reward(self, coin: str, amount: float, pool_fee: float = 0.0,
                      block_height: Optional[int] = None) -> Dict[str, Any]:
        reward = MiningReward(block_height=block_height or 0, coin=coin, amount=amount, pool_fee=pool_fee)
        self._reward_analyzer.add_reward(reward)
        self._pool_manager.record_reward(reward)
        return {"status": "recorded", "coin": coin, "amount": amount, "pool_fee": pool_fee}

    def get_reward_analysis(self, coin: str) -> Dict[str, Any]:
        return {
            "coin": coin, "total_revenue": self._reward_analyzer.get_total_revenue(coin),
            "average_payout": self._reward_analyzer.get_average_payout(coin),
            "fee_efficiency": self._reward_analyzer.get_fee_efficiency(coin),
        }

    def get_reward_distribution_report(self) -> Dict[str, Any]:
        return self._reward_analyzer.get_reward_distribution_report()

    def evaluate_pool_switch(self) -> Dict[str, Any]:
        current = self.get_active_pool()
        available = list(self._pool_manager._pools.keys())
        should_switch, target = self._pool_switcher.evaluate_switch(current)
        return {"should_switch": should_switch, "current_pool": current,
                "target_pool": target, "available_pools": available}

    def optimize_fleet(self, rig_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        if rig_ids is None:
            rig_ids = [r.rig_id for r in self._rigs]
        return self._optimizer.optimize_fleet(rig_ids)

    def optimize_power_allocation(self, rig_ids: List[str], total_power_budget_w: float) -> Dict[str, Any]:
        allocation = self._optimizer.optimize_power_allocation(rig_ids, total_power_budget_w)
        return {"allocation": allocation, "total_allocated_w": sum(allocation.values()),
                "budget_w": total_power_budget_w}

    def select_algorithm(self, hardware_type: HardwareType, available_memory_gb: float,
                         power_budget_w: float) -> Dict[str, Any]:
        algo = self._algorithm_selector.select_algorithm(hardware_type, available_memory_gb, power_budget_w)
        profile = self._algorithm_selector.get_algorithm_profile(algo)
        return {"algorithm": algo.name, "profile": profile, "coins": profile.get("coins", [])}

    def get_compatible_algorithms(self, hardware_type: HardwareType) -> List[str]:
        return [a.name for a in self._algorithm_selector.get_compatible_algorithms(hardware_type)]

    def get_mining_economics(self) -> Dict[str, Any]:
        return self._economics.get_economics_summary()

    def calculate_roi(self, total_revenue: float, period_days: int = 30) -> Dict[str, Any]:
        return self._economics.calculate_roi(total_revenue, period_days)

    def calculate_break_even(self, monthly_revenue: float, monthly_costs: float) -> Dict[str, Any]:
        months = self._economics.calculate_break_even(monthly_revenue, monthly_costs)
        return {"break_even_months": months if months > 0 else None, "monthly_revenue": monthly_revenue,
                "monthly_costs": monthly_costs, "net_monthly": monthly_revenue - monthly_costs}

    def get_cashflow_projection(self, monthly_revenue: float, monthly_costs: float,
                                months: int = 12) -> Dict[str, Any]:
        projection = self._economics.get_cashflow_projection(monthly_revenue, monthly_costs, months)
        return {"projection_months": months, "data": projection,
                "final_cumulative": projection[-1]["cumulative"] if projection else 0.0}

    def get_status(self) -> Dict[str, Any]:
        fleet = self.get_fleet_status()
        return {
            "agent": "CryptoMiningAgent", "running": self._running,
            "rigs_count": fleet.get("total_rigs", 0), "active_rigs": fleet.get("active_rigs", 0),
            "total_hash_rate_th_s": fleet.get("total_hash_rate_th_s", 0.0),
            "total_power_w": fleet.get("total_power_w", 0.0),
            "active_pool": self.get_active_pool(), "pool_health": self.get_pool_health(),
        }

    def get_full_report(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(), "agent_status": self.get_status(),
            "hardware_health": self.get_hardware_health_report(),
            "economics": self.get_mining_economics(),
            "energy": self.get_energy_report(),
        }

# =============================================================================
# ASYNC WRAPPER
# =============================================================================

class AsyncCryptoMiningAgent:
    def __init__(self, config: Optional[Config] = None):
        self._agent = CryptoMiningAgent(config)

    async def initialize(self) -> Dict[str, Any]:
        return self._agent.initialize()

    async def shutdown(self) -> Dict[str, Any]:
        return self._agent.shutdown()

    async def analyze_profitability(self, coin: str, hash_rate: float = 100.0,
                                    power: float = 3000.0) -> Dict[str, Any]:
        return self._agent.analyze_profitability(coin, hash_rate, power)

    async def get_full_report(self) -> Dict[str, Any]:
        return self._agent.get_full_report()

# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    print("=" * 60)
    print("  Crypto Mining Agent - Comprehensive Demo")
    print("=" * 60)
    config = Config(electricity_cost_per_kwh=0.12, max_temperature=85.0, power_budget_w=5000.0)
    agent = CryptoMiningAgent(config)
    init_result = agent.initialize()
    print(f"Initialized: {init_result['status']}")
    rigs = [
        ("asic_001", "Bitmain S19", HardwareType.ASIC, AlgorithmType.SHA256, 110.0, 3250.0, 3000.0),
        ("asic_002", "Bitmain S21", HardwareType.ASIC, AlgorithmType.SHA256, 200.0, 3500.0, 5000.0),
        ("gpu_001", "NVIDIA RTX 4090", HardwareType.GPU_NVIDIA, AlgorithmType.KAWPOW, 120.0, 450.0, 1500.0),
        ("gpu_002", "AMD RX 7900 XTX", HardwareType.GPU_AMD, AlgorithmType.KAWPOW, 110.0, 355.0, 1000.0),
    ]
    for rig_id, model, hw_type, algo, hr, power, cost in rigs:
        agent.register_rig(rig_id, model, hw_type, algo, hr, power, cost)
        agent.start_rig(rig_id)
    pools = [
        ("f2pool", "bitcoin", AlgorithmType.SHA256,
         [PoolEndpoint(url="stratum+tcp://btc.f2pool.com", port=3333)], RewardType.PPS, 1.5),
        ("slushpool", "bitcoin", AlgorithmType.SHA256,
         [PoolEndpoint(url="stratum+tcp://stratum.slushpool.com", port=3333)], RewardType.PPS, 2.0),
        ("woolypooly", "ravencoin", AlgorithmType.KAWPOW,
         [PoolEndpoint(url="stratum+tcp://rvn.woolypooly.com", port=5555)], RewardType.PPLNS, 0.9),
    ]
    for name, coin, algo, endpoints, reward_type, fee in pools:
        agent.register_pool(name, coin, algo, endpoints, reward_type, fee, default=(name == "f2pool"))
    for coin in ["bitcoin", "litecoin", "ravencoin"]:
        analysis = agent.analyze_profitability(coin)
        print(f"{coin:15s}: Daily Profit: ${analysis['daily_profit']:8.2f} | Monthly: ${analysis['monthly_profit']:9.2f}")
    fleet = agent.get_fleet_status()
    print(f"\nFleet: {fleet['total_rigs']} rigs | {fleet['total_hash_rate_th_s']:.2f} TH/s | {fleet['total_power_w']:.0f}W")
    opt = agent.optimize_fleet([r[0] for r in rigs])
    print(f"Optimization actions: {len(opt.get('fleet_actions', []))}")
    econ = agent.get_mining_economics()
    print(f"Economics: ROI={econ.get('roi_30d_percent', 0):.2f}% | Net 30d=${econ.get('net_profit_30d', 0):.2f}")
    agent.shutdown()
    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
