# Crypto Mining Agent

A comprehensive cryptocurrency mining operations platform with multi-algorithm support, pool management, hardware monitoring, profitability analysis, and energy optimization.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Setup](#basic-setup)
  - [Pool Management](#pool-management)
  - [Rig Management](#rig-management)
  - [Profitability Analysis](#profitability-analysis)
  - [Hardware Monitoring](#hardware-monitoring)
  - [Energy Optimization](#energy-optimization)
  - [Algorithm Selection](#algorithm-selection)
  - [Mining Economics](#mining-economics)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Supported Algorithms](#supported-algorithms)
- [Hardware Compatibility](#hardware-compatibility)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Crypto Mining Agent provides a complete framework for managing cryptocurrency mining operations. It supports multiple mining algorithms (SHA-256, Ethash, Scrypt, RandomX, KawPow), various hardware types (ASIC, GPU, CPU, FPGA), and integrates with major mining pools for automated operations.

The agent is designed for both individual miners managing a few rigs and large-scale mining operations with hundreds of machines. It provides real-time monitoring, automatic optimization, and comprehensive economic analysis to maximize profitability.

## Features

### Core Capabilities
- **Multi-Algorithm Mining**: SHA-256, Ethash, Scrypt, RandomX, KawPow, EquiHash, CryptoNight, Blake2S, Lyra2REV2, X11
- **Hardware Support**: ASIC (Bitmain, Antminer), GPU (NVIDIA, AMD), CPU, FPGA
- **Pool Management**: Multi-pool support with automatic failover and latency-based switching
- **Real-Time Monitoring**: Temperature, hash rate, fan speed, share statistics
- **Profitability Analysis**: Multi-coin comparison with difficulty-adjusted calculations
- **Energy Optimization**: Power tracking, cost analysis, carbon footprint estimation
- **Mining Economics**: ROI calculation, break-even analysis, cash flow projection

### Advanced Features
- **Automatic Pool Switching**: Strategy-based pool selection (latency, profitability, composite)
- **Temperature Monitoring**: Multi-sensor tracking with automatic throttling
- **Anomaly Detection**: Hash rate deviation alerts with trend analysis
- **Health Scoring**: Comprehensive rig health assessment (0.0 to 1.0)
- **Reward Analysis**: Payout tracking, fee efficiency, and distribution reporting
- **Async Support**: Full asyncio wrapper for non-blocking operations

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    CryptoMiningAgent                          │
│  ┌────────────┐ ┌──────────────┐ ┌────────────────────────┐ │
│  │ Pool Mgr   │ │ Hardware Mon │ │ Profitability Calc     │ │
│  ├────────────┤ ├──────────────┤ ├────────────────────────┤ │
│  │ Switch Eng │ │ Temp Monitor │ │ Energy Tracker         │ │
│  ├────────────┤ ├──────────────┤ ├────────────────────────┤ │
│  │ Reward An  │ │ Hash Tracker │ │ Rig Manager            │ │
│  └────────────┘ └──────────────┘ └────────────────────────┘ │
│  ┌────────────┐ ┌──────────────┐ ┌────────────────────────┐ │
│  │ Algorithm  │ │ Optimizer    │ │ Economics              │ │
│  │ Selector   │ │              │ │                        │ │
│  └────────────┘ └──────────────┘ └────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.crypto_mining.agent import (
    CryptoMiningAgent, Config, HardwareType, AlgorithmType,
    PoolEndpoint, RewardType
)

# Initialize agent
config = Config(electricity_cost_per_kwh=0.12, power_budget_w=5000)
agent = CryptoMiningAgent(config)
agent.initialize()

# Register a mining rig
agent.register_rig(
    rig_id="asic_001",
    model="Bitmain S19",
    hardware_type=HardwareType.ASIC,
    algorithm=AlgorithmType.SHA256,
    hash_rate=110.0,
    power_consumption=3250,
    unit_cost=3000.0
)

# Register a pool
agent.register_pool(
    pool_name="f2pool",
    coin="bitcoin",
    algorithm=AlgorithmType.SHA256,
    endpoints=[PoolEndpoint(url="stratum+tcp://btc.f2pool.com", port=3333)],
    reward_type=RewardType.PPS,
    fee_percentage=1.5,
    default=True
)

# Start mining
agent.start_rig("asic_001")
agent.connect_pool("f2pool", "worker_001")

# Analyze profitability
result = agent.analyze_profitability("bitcoin", hash_rate=110.0, power_consumption=3250)
print(f"Daily Profit: ${result['daily_profit']:.2f}")

# Get full report
report = agent.get_full_report()
agent.shutdown()
```

## Installation

### From Source
```bash
git clone https://github.com/your-org/crypto-mining-agent.git
cd crypto-mining-agent
pip install -r requirements.txt
```

### Dependencies
```
Python 3.10+
No external dependencies required (stdlib only)
```

## Usage

### Basic Setup

```python
from agents.crypto_mining.agent import CryptoMiningAgent, Config

config = Config(
    electricity_cost_per_kwh=0.12,    # $/kWh
    max_temperature=85.0,             # °C
    power_budget_w=5000,              # Watts
    auto_switch_pools=True,
    monitor_poll_interval=5.0,        # seconds
)

agent = CryptoMiningAgent(config)
agent.initialize()
```

### Pool Management

```python
# Register multiple pools
agent.register_pool("f2pool", "bitcoin", AlgorithmType.SHA256,
    [PoolEndpoint("stratum+tcp://btc.f2pool.com", 3333)],
    RewardType.PPS, 1.5, default=True)

agent.register_pool("slushpool", "bitcoin", AlgorithmType.SHA256,
    [PoolEndpoint("stratum+tcp://stratum.slushpool.com", 3333)],
    RewardType.PPS, 2.0)

# Connect and manage
agent.connect_pool("f2pool", "worker_001")
agent.set_active_pool("slushpool")

# Monitor pool health
health = agent.get_pool_health()
# {"f2pool": "ONLINE", "slushpool": "ONLINE"}

# Evaluate automatic switching
switch = agent.evaluate_pool_switch()
```

### Rig Management

```python
# Register ASIC rigs
agent.register_rig("asic_001", "Bitmain S19", HardwareType.ASIC,
    AlgorithmType.SHA256, 110.0, 3250, 3000)

# Register GPU rigs
agent.register_rig("gpu_001", "NVIDIA RTX 4090", HardwareType.GPU_NVIDIA,
    AlgorithmType.KAWPOW, 120.0, 450, 1500)

# Control lifecycle
agent.start_rig("asic_001")
agent.stop_rig("gpu_001")
agent.restart_rig("asic_001")

# Monitor status
status = agent.get_rig_status("asic_001")
fleet = agent.get_fleet_status()
```

### Profitability Analysis

```python
# Single coin analysis
result = agent.analyze_profitability(
    coin="bitcoin",
    hash_rate=110.0,        # TH/s
    power_consumption=3250  # Watts
)
# {'daily_profit': 12.45, 'monthly_profit': 373.50, 'break_even_price': 42000}

# Multi-coin comparison
comparison = agent.compare_profitability(
    hash_rate=110.0,
    power_consumption=3250,
    coins=["bitcoin", "litecoin", "ravencoin"]
)
# Ranked by daily profit

# Update market data
agent.update_coin_price("bitcoin", 65000)
agent.update_network_difficulty("bitcoin", 83e12)
```

### Hardware Monitoring

```python
# Temperature readings
temps = agent.get_temperature_readings("asic_001")
# {'average': 62.5, 'max': 68.2, 'safe': True, 'readings': {...}}

# Comprehensive health report
health = agent.get_hardware_health_report()
# Per-rig: status, hash_rate, temperature, shares, alerts

# Hash rate tracking
agent.record_hash_rate("asic_001", 109.5, HashRateUnit.THPS)
history = agent.get_hash_rate_history("asic_001", limit=100)
```

### Energy Optimization

```python
# Record energy readings
agent.record_energy_reading("asic_001", power_draw=3250, efficiency=0.95)

# Get energy report
energy = agent.get_energy_report()
# {'total_monthly_cost_estimate': 2808.00, 'carbon_footprint_kg_monthly': 1134.0}

# Set optimization targets
agent._energy_tracker.set_optimization_target("asic_001", 75.0)  # kWh/day
```

### Algorithm Selection

```python
# Auto-select best algorithm
algo = agent.select_algorithm(
    hardware_type=HardwareType.GPU_NVIDIA,
    available_memory_gb=24,
    power_budget_w=450
)
# {'algorithm': 'KAWPOW', 'coins': ['ravencoin'], ...}

# Get compatible algorithms
algos = agent.get_compatible_algorithms(HardwareType.ASIC)
# ['SHA256', 'SCRYPT', 'EQUIHASH', 'BLAKE2S']
```

### Mining Economics

```python
# ROI calculation
roi = agent.calculate_roi(total_revenue=15000, period_days=30)
# {'roi_percent': 45.2, 'net_profit': 4520}

# Break-even analysis
be = agent.calculate_break_even(monthly_revenue=5000, monthly_costs=2000)
# {'break_even_months': 8, 'net_monthly': 3000}

# Cash flow projection
cf = agent.get_cashflow_projection(5000, 2000, months=12)
# List of monthly projections with cumulative values

# Risk analysis
risk = agent._economics.get_risk_analysis(volatility=0.15, difficulty_growth=0.05)
# {'risk_level': 'low', 'risk_score': 22.5}
```

## API Reference

### CryptoMiningAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `initialize()` | - | Dict | Start the agent and all subsystems |
| `shutdown()` | - | Dict | Gracefully stop all operations |
| `register_pool()` | pool_name, coin, algorithm, endpoints, reward_type, fee, default | Dict | Register a mining pool |
| `connect_pool()` | pool_name, worker_name, password | Dict | Connect to a pool |
| `register_rig()` | rig_id, model, hw_type, algorithm, hash_rate, power, cost | Dict | Register mining hardware |
| `start_rig()` | rig_id | Dict | Start mining on a rig |
| `stop_rig()` | rig_id | Dict | Stop mining on a rig |
| `analyze_profitability()` | coin, hash_rate, power, algorithm | Dict | Calculate mining profitability |
| `compare_profitability()` | hash_rate, power, coins | Dict | Compare profitability across coins |
| `get_temperature_readings()` | rig_id | Dict | Get temperature sensor data |
| `get_hardware_health_report()` | - | Dict | Comprehensive health report |
| `record_energy_reading()` | rig_id, power_draw, efficiency | Dict | Record energy consumption |
| `get_energy_report()` | - | Dict | Energy consumption report |
| `select_algorithm()` | hw_type, memory_gb, power_budget | Dict | Select optimal algorithm |
| `calculate_roi()` | revenue, period_days | Dict | Calculate return on investment |
| `calculate_break_even()` | monthly_revenue, monthly_costs | Dict | Break-even analysis |
| `optimize_fleet()` | rig_ids | Dict | Optimize entire fleet |
| `evaluate_pool_switch()` | - | Dict | Evaluate pool switching |
| `get_status()` | - | Dict | Overall agent status |
| `get_full_report()` | - | Dict | Comprehensive status report |

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `electricity_cost_per_kwh` | float | 0.12 | Electricity cost in $/kWh |
| `max_temperature` | float | 85.0 | Maximum temperature before throttle (°C) |
| `power_budget_w` | float | 5000.0 | Total power budget in Watts |
| `auto_switch_pools` | bool | True | Enable automatic pool switching |
| `monitor_poll_interval` | float | 5.0 | Hardware monitoring interval (seconds) |
| `default_algorithm` | AlgorithmType | SHA256 | Default mining algorithm |
| `temperature_unit` | TemperatureUnit | CELSIUS | Temperature display unit |
| `hash_rate_unit` | HashRateUnit | THPS | Hash rate display unit |

## Supported Algorithms

| Algorithm | Coins | Typical Hardware | Hash Rate Unit |
|-----------|-------|-----------------|----------------|
| SHA-256 | Bitcoin, Bitcoin Cash, Dogecoin | ASIC | TH/s |
| Ethash | Ethereum Classic, Flux | GPU | MH/s |
| Scrypt | Litecoin, Dogecoin | ASIC | MH/s |
| RandomX | Monero | CPU | kH/s |
| KawPow | Ravencoin | GPU | MH/s |
| EquiHash | Zcoin, Bitcoin Gold | ASIC/GPU | H/s |
| CryptoNight | Monero, Grin | CPU/GPU | kH/s |
| Blake2S | Sia, Decred | ASIC | GH/s |
| Lyra2REV2 | Verge, Monacoin | GPU | MH/s |
| X11 | Dash, SmartCash | GPU | MH/s |

## Hardware Compatibility

### ASIC Miners
| Model | Algorithm | Hash Rate | Power |
|-------|-----------|-----------|-------|
| Bitmain S19 | SHA-256 | 110 TH/s | 3250W |
| Bitmain S21 | SHA-256 | 200 TH/s | 3500W |
| Antminer L7 | Scrypt | 9.16 GH/s | 3425W |
| Antminer K7 | Ethash | 63.5 GH/s | 3000W |

### GPU Cards
| Model | Algorithm | Hash Rate | Power |
|-------|-----------|-----------|-------|
| NVIDIA RTX 4090 | KawPow | 120 MH/s | 450W |
| NVIDIA RTX 3080 | KawPow | 65 MH/s | 320W |
| AMD RX 6800 XT | KawPow | 64 MH/s | 300W |
| AMD RX 7900 XTX | KawPow | 110 MH/s | 355W |

## Best Practices

### Hardware Management
1. **Temperature Monitoring**: Always monitor both core and VRM temperatures
2. **Power Headroom**: Size power supplies with 20% headroom above rated draw
3. **Firmware Updates**: Keep ASIC firmware current for optimal performance
4. **Dust Management**: Clean filters and heatsinks regularly
5. **Redundancy**: Use multiple pools for failover

### Profitability Optimization
1. **Update Prices**: Refresh coin prices every 5-15 minutes
2. **Track Difficulty**: Monitor network difficulty changes daily
3. **Factor All Costs**: Include pool fees, hardware depreciation, cooling
4. **Compare Regularly**: Re-evaluate coin selection weekly
5. **Consider Variance**: PPLNS pools have higher variance than PPS

### Energy Efficiency
1. **Undervolt GPUs**: Better performance-per-watt at lower voltages
2. **Optimize Power Limits**: Find the efficiency sweet spot for each card
3. **Smart Scheduling**: Mine during off-peak electricity hours
4. **Monitor Power Factor**: Ensure efficient power delivery
5. **Track Carbon Footprint**: Use renewable energy when possible

### Pool Strategy
1. **Low Latency**: Choose pools with < 100ms latency
2. **Reasonable Fees**: PPS pools < 2%, PPLNS pools < 1%
3. **High Uptime**: Verify > 99.5% historical availability
4. **Payout Threshold**: Align with your mining scale
5. **Diversification**: Use 2-3 pools for redundancy

## Troubleshooting

### Common Issues

**Rig shows OFFLINE**
- Check network connectivity to pool endpoint
- Verify worker name and password
- Ensure firewall allows stratum protocol
- Check pool maintenance status

**Temperature too high**
- Increase fan speed
- Reduce power limit by 10-15%
- Check ambient temperature and airflow
- Clean dust from heatsinks
- Consider liquid cooling

**Low hash rate**
- Verify correct algorithm for hardware
- Check power limit settings
- Update firmware/drivers
- Monitor for thermal throttling
- Compare with reference rates

**High share rejection**
- Check difficulty setting
- Verify pool configuration
- Ensure stable network connection
- Check for hardware errors

**No rewards received**
- Verify pool statistics
- Check payout threshold
- Confirm payout address
- Review reward type (PPS vs PPLNS)

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Detailed logging shows:
# - Pool connection attempts
# - Share submissions
# - Temperature readings
# - Profitability calculations
# - Pool switching decisions
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
pip install -r requirements-dev.txt
python -m pytest tests/
python -m mypy agents/
python -m black agents/
```

### Code Style
- Follow PEP 8
- Use type hints for all public methods
- Write docstrings for all classes and public methods
- Keep methods under 50 lines
- Use dataclasses for data structures

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Bitcoin mining algorithm specifications
- OpenZimmer for hardware reference data
- Mining pool documentation from f2pool, slushpool, and woolypooly
- Community contributions and feedback
