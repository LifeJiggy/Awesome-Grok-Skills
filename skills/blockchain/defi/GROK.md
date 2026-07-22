---
name: "defi"
category: "blockchain"
version: "2.0.0"
tags: ["blockchain", "defi", "automated-market-maker", "yield-farming", "liquidity-pools"]
---

# DeFi (Decentralized Finance)

## Overview

The DeFi module provides comprehensive tools for interacting with decentralized finance protocols on Ethereum and EVM-compatible chains. It covers Automated Market Maker (AMM) operations, liquidity pool management, yield farming strategies, flash loan mechanics, lending/borrowing protocol integration, and stablecoin mechanics. The module includes price oracle interfaces, impermanent loss calculators, gas estimation, and MEV (Maximal Extractable Value) protection strategies.

This skill is essential for DeFi developers building protocol integrations, quantitative traders optimizing yield strategies, security auditors analyzing DeFi protocols, and researchers studying on-chain economic mechanisms.

## Core Capabilities

- **AMM Operations**: Uniswap V2/V3 swap calculations, price impact estimation, slippage protection, multi-hop routing
- **Liquidity Management**: Add/remove liquidity, concentrated liquidity positions (V3), impermanent loss calculation
- **Yield Farming**: APY/APR calculation, reward token distribution, compounding frequency optimization, strategy comparison
- **Flash Loans**: Atomic transaction design, flash loan attack patterns, flash loan-powered arbitrage
- **Lending/Borrowing**: Collateralization ratios, liquidation thresholds, health factor calculation, interest rate models
- **Price Oracles**: TWAP (Time-Weighted Average Price) calculation, oracle manipulation detection, multi-oracle aggregation
- **Gas Optimization**: Transaction batching, calldata compression, gas price estimation, EIP-1559 fee calculation
- **MEV Protection**: Private mempool submission, sandwich attack detection, frontrunning protection

## Usage Examples

```python
from defi import (
    AMMRouter,
    LiquidityPool,
    YieldCalculator,
    FlashLoanExecutor,
    LendingProtocol,
    ImpermanentLossCalc,
)

# --- AMM Swap Calculation ---
router = AMMRouter(protocol="uniswap_v2")
quote = router.get_swap_quote(
    token_in="WETH",
    token_out="USDC",
    amount_in=1.0,
    fee_tier=0.003,
)
print(f"Expected output: {quote.amount_out:.2f} USDC")
print(f"Price impact: {quote.price_impact:.2%}")
print(f"Minimum received: {quote.minimum_out:.2f} USDC")

# --- Multi-hop Routing ---
route = router.find_best_route(
    token_in="DAI",
    token_out="WBTC",
    amount_in=10000,
    max_hops=3,
)
print(f"Route: {' -> '.join(route.path)}")
print(f"Output: {route.amount_out:.6f} WBTC")
print(f"Gas estimate: {route.gas_estimate:,}")

# --- Liquidity Pool Analysis ---
pool = LiquidityPool(
    address="0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
    protocol="uniswap_v2",
)
info = pool.get_pool_info()
print(f"Token0: {info.token0_symbol} (reserves: {info.reserve0:,.0f})")
print(f"Token1: {info.token1_symbol} (reserves: {info.reserve1:,.0f})")
print(f"LP total supply: {info.lp_supply:,.0f}")
print(f"Pool fee: {info.fee_tier:.1%}")

# --- Impermanent Loss Calculation ---
il_calc = ImpermanentLossCalc()
il = il_calc.calculate(
    entry_price_ratio=1.0,
    current_price_ratio=2.0,
    fee_apy=0.30,
    days_in_pool=365,
)
print(f"Impermanent loss: {il.il_pct:.2%}")
print(f"Fees earned: {il.fees_earned:.2%}")
print(f"Net P&L: {il.net_return:.2%}")

# --- Yield Farming ---
calculator = YieldCalculator()
strategies = [
    {"name": "Uniswap V3 ETH/USDC", "tvl": 500_000_000, "apr": 0.25, "risk": "medium"},
    {"name": "Aave V3 USDC", "tvl": 2_000_000_000, "apr": 0.04, "risk": "low"},
    {"name": "Curve 3pool", "tvl": 800_000_000, "apr": 0.08, "risk": "low"},
]
for strat in strategies:
    apy = calculator.compound_apy(strat["apr"], compound_freq=365)
    risk_adj = calculator.risk_adjusted_return(apy, strat["risk"])
    print(f"{strat['name']}: APY={apy:.1%}, Risk-adj={risk_adj:.1%}")

# --- Flash Loan ---
executor = FlashLoanExecutor(provider="aave_v3")
plan = executor.create_flash_loan(
    asset="USDC",
    amount=1_000_000,
    actions=[
        {"type": "swap", "dex": "uniswap", "token_in": "USDC", "token_out": "DAI"},
        {"type": "swap", "dex": "curve", "token_in": "DAI", "token_out": "USDC"},
    ],
)
print(f"Flash loan amount: {plan.amount:,.0f} {plan.asset}")
print(f"Projected profit: {projected_profit:.2f} USDC")
print(f"Gas cost: {plan.gas_cost:.2f} USDC")

# --- Lending Protocol ---
lending = LendingProtocol(protocol="aave_v3")
health = lending.calculate_health_factor(
    collateral=[{"asset": "WETH", "amount": 10, "price": 3000}],
    borrow=[{"asset": "USDC", "amount": 15000}],
)
print(f"Health factor: {health.health_factor:.2f}")
print(f"Liquidation threshold: {health.liquidation_threshold}")
print(f"Max borrow: {health.max_borrow:,.0f} USDC")
```

## Best Practices

- Always set slippage tolerance to 0.5-1% for normal swaps; increase to 3-5% for volatile pairs
- Use multi-hop routing through intermediate pools to reduce price impact on large trades
- Calculate impermanent loss before providing liquidity — compare against simply holding
- Monitor health factor continuously; keep it above 1.5 for safety margin against liquidation
- Use flash loans for capital-efficient strategies but account for 0.09% Aave flash loan fee
- Prefer concentrated liquidity (V3) for known price ranges; use full-range (V2) for passive strategies
- Check pool depth before trading — pools with TVL < $100K have significant MEV risk
- Use EIP-1559 transaction types for predictable gas pricing on Ethereum mainnet
- Validate price oracle freshness — stale oracle prices are the most common DeFi exploit vector
- Test all DeFi interactions on testnets (Sepolia, Goerli) before mainnet deployment

## Related Modules

- **smart-contract-development**: Solidity smart contract development for DeFi protocols
- **smart-contracts**: Security auditing of DeFi smart contracts
- **nft-development**: NFT marketplace integration with DeFi composability
- **consensus-mechanisms**: Underlying blockchain consensus for DeFi transactions

## Advanced Configuration

### DEX Router Configuration

```python
from defi import RouterConfig

config = RouterConfig(
    protocols=["uniswap_v2", "uniswap_v3", "sushiswap", "curve"],
    max_hops=4,
    max_splits=3,
    gas_price_gwei=30,
    slippage_tolerance=0.005,
    deadline_seconds=1800,
    use_mempool_protection=True,
    private_relay="flashbots",
)
```

### Oracle Configuration

```python
from defi import OracleConfig

oracle_config = OracleConfig(
    primary="chainlink",
    fallback="uniswap_v3_twap",
    staleness_threshold_seconds=3600,
    deviation_threshold_pct=0.05,
    heartbeat_seconds=1800,
    min_price_sources=3,
)
```

### Yield Strategy Configuration

```python
from defi import YieldConfig

yield_config = YieldConfig(
    min_apy=0.02,
    max_risk="medium",
    min_tvl=1_000_000,
    auto_compound=True,
    compound_frequency_hours=24,
    gas_budget_usd=50,
    rebalance_threshold=0.02,
)
```

## Architecture Patterns

### AMM Liquidity Architecture

```
Liquidity Provider Flow:
├── Deposit Assets
│   ├── Single-sided (stable pools)
│   └── Double-sided (volatile pairs)
├── Receive LP Tokens
│   ├── ERC-20 LP token
│   └── NFT position (V3 concentrated)
├── Earn Fees
│   ├── Trading fees (0.01%-1%)
│   └── Reward tokens (incentive programs)
└── Withdraw Liquidity
    ├── Pro-rata share of pool
    └── Impermanent loss realization
```

### Lending Protocol Architecture

```
Lending Pool:
├── Deposit Side
│   ├── aToken (interest-bearing)
│   ├── Variable rate model
│   └── Utilization-based pricing
├── Borrow Side
│   ├── Collateral requirement
│   ├── Liquidation threshold
│   └── Health factor monitoring
├── Interest Rate Model
│   ├── Base rate
│   ├── Slope1 (below optimal utilization)
│   └── Slope2 (above optimal utilization)
└── Risk Management
    ├── Oracles (Chainlink, Uniswap TWAP)
    ├── Asset risk parameters
    └── Protocol-level insurance
```

### MEV Protection Architecture

```
Transaction Submission:
├── Public Mempool (default, MEV vulnerable)
├── Flashbots Protect (private relay)
├── MEV-Share (MEV redistribution)
└── Private Transaction Pools
    ├── MEV Blocker (by MEV Blocker)
    └── Custom relayer networks
```

## Integration Guide

### Chainlink Oracle Integration

```python
from defi import ChainlinkOracle

oracle = ChainlinkOracle(
    feed_addresses={
        "ETH/USD": "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
        "BTC/USD": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",
        "USDC/USD": "0x8fFfF89722629B0a406A44d55B91C2f0E729c5ab",
    },
    staleness_threshold=3600,
)

price = oracle.get_price("ETH/USD")
print(f"ETH/USD: ${price.price:.2f}")
print(f"Updated: {price.updated_seconds_ago}s ago")
print(f"Decimals: {price.decimals}")
```

### Uniswap V3 Position Management

```python
from defi import V3PositionManager

manager = V3PositionManager(
    nft_manager="0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
)

position = manager.create_position(
    token0="WETH",
    token1="USDC",
    fee=3000,
    tick_lower=-887220,   # Price lower bound
    tick_upper=887220,    # Price upper bound
    amount0=10,
    amount1=30000,
)
print(f"Position NFT: {position.token_id}")
print(f"Liquidity: {position.liquidity}")
print(f"Fee APR: {position.estimated_fee_apr:.1%}")
```

### Flash Loan Integration

```python
from defi import FlashLoanProvider

aave = FlashLoanProvider(
    protocol="aave_v3",
    pool_address="0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
)

tx = aave.execute_flash_loan(
    assets=["USDC"],
    amounts=[1_000_000],
    actions=[
        {"dex": "uniswap", "token_in": "USDC", "token_out": "DAI"},
        {"dex": "curve", "token_in": "DAI", "token_out": "USDC"},
    ],
)
print(f"Flash loan profit: {tx.profit:.2f} USDC")
print(f"Gas cost: {tx.gas_cost:.2f} USDC")
print(f"Net profit: {tx.net_profit:.2f} USDC")
```

## Performance Optimization

### Gas Optimization Strategies

| Strategy | Description | Savings |
|----------|-------------|---------|
| Batch operations | Combine multiple swaps in one tx | 40-60% |
| Calldata compression | Pack route data efficiently | 10-20% |
| Flashbots bundles | Avoid failed tx gas waste | 100% failed tx |
| Route optimization | Fewer hops = less gas | 20-30% per hop |
| Optimal split routing | Split large trades across pools | Variable |

### RPC Optimization

```python
from defi import OptimizedProvider

provider = OptimizedProvider(
    primary="https://eth-mainnet.g.alchemy.com/v2/KEY",
    fallbacks=[
        "https://eth-mainnet.infura.io/v3/KEY",
        "https://rpc.ankr.com/eth",
    ],
    cache_ttl_seconds=5,
    batch_requests=True,
    max_retries=3,
)
```

### Price Impact Optimization

```python
from defi import PriceImpactAnalyzer

analyzer = PriceImpactAnalyzer()
optimal_route = analyzer.find_optimal_route(
    token_in="USDC",
    token_out="WETH",
    amount_in=500_000,
    max_price_impact=0.01,
    pools=["uniswap_v3_0.05", "uniswap_v3_0.3", "sushiswap"],
)
print(f"Route: {optimal_route.path}")
print(f"Output: {optimal_route.amount_out:.4f} WETH")
print(f"Price impact: {optimal_route.price_impact:.4%}")
print(f"Gas: {optimal_route.gas_estimate:,}")
```

## Security Considerations

### Common DeFi Attack Vectors

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Flash Loan Exploit | Borrow huge capital to manipulate price | Time-weighted operations |
| Oracle Manipulation | Feed stale or manipulated prices | Multi-oracle with TWAP |
| Sandwich Attack | Front-run and back-run trades | Flashbots, private pools |
| Governance Attack | Flash loan voting | Time-weighted voting |
| Reentrancy | Recursive callback exploitation | CEI pattern, ReentrancyGuard |
| Price Manipulation | Move pool price via large trade | Oracles, circuit breakers |
| Rug Pull | Remove liquidity suddenly | Timelock, LP locking |

### Security Checklist

- [ ] Oracle freshness validated (staleness threshold)
- [ ] Price deviation checks in place
- [ ] Slippage protection on all swaps
- [ ] Health factor monitoring for lending
- [ ] Liquidation incentive properly calibrated
- [ ] Flash loan fee accounted for in profitability
- [ ] MEV protection enabled for user-facing txs
- [ ] Emergency pause functionality available
- [ ] Multi-sig for protocol admin functions
- [ ] Timelock on governance changes

## Troubleshooting Guide

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| INSUFFICIENT_OUTPUT_AMOUNT | Slippage too low | Increase slippage tolerance |
| STALE_PRICE_FEED | Oracle too old | Check oracle heartbeat |
| HEALTH_FACTOR_LOW | Collateral value dropped | Add more collateral |
| INSUFFICIENT_LIQUIDITY | Pool too shallow | Use deeper pool |
| EXPIRED_DEADLINE | Transaction took too long | Increase deadline |
| GAS_ESTIMATE_EXCEEDED | Network congestion | Increase gas limit |

### Debugging Failed Swaps

```bash
# Simulate swap
cast call 0xRouter "swapExactTokensForTokens(
  uint256 amountIn,
  uint256 amountOutMin,
  address[] path,
  address to,
  uint256 deadline
)" 1000000000000000000 900000000000000000 "[0xWETH,0xUSDC]" 0xRecipient $(($(date +%s)+1800)) --rpc-url $ETH_RPC_URL

# Check pool reserves
cast call 0xPool "getReserves()" --rpc-url $ETH_RPC_URL

# Check token balances
cast call 0xToken "balanceOf(address)" 0xPool --rpc-url $ETH_RPC_URL
```

### Slippage Troubleshooting

```
1. Check current pool reserves
2. Calculate expected output vs actual
3. Factor in price impact of your trade size
4. Account for pending transactions in mempool
5. Set slippage = price_impact + buffer (0.1-0.5%)
```

## API Reference

### AMMRouter

```python
class AMMRouter:
    def get_swap_quote(
        token_in: str,
        token_out: str,
        amount_in: float,
        fee_tier: float = 0.003,
    ) -> SwapQuote:
        """Get a quote for a token swap."""
    
    def find_best_route(
        token_in: str,
        token_out: str,
        amount_in: float,
        max_hops: int = 3,
    ) -> Route:
        """Find optimal routing across pools."""
    
    def execute_swap(
        route: Route,
        slippage_tolerance: float = 0.005,
        deadline_seconds: int = 1800,
    ) -> SwapResult:
        """Execute a swap transaction."""
```

### LiquidityPool

```python
class LiquidityPool:
    def get_pool_info(self) -> PoolInfo:
        """Get pool reserves, supply, and fee info."""
    
    def add_liquidity(
        amount0: float,
        amount1: float,
        slippage: float = 0.005,
    ) -> LPResult:
        """Add liquidity to pool."""
    
    def remove_liquidity(
        lp_amount: float,
        slippage: float = 0.005,
    ) -> RemovalResult:
        """Remove liquidity from pool."""
```

### YieldCalculator

```python
class YieldCalculator:
    def compound_apy(
        apr: float,
        compound_freq: int = 365,
    ) -> float:
        """Calculate compounded APY from APR."""
    
    def risk_adjusted_return(
        apy: float,
        risk_level: str,
    ) -> float:
        """Calculate risk-adjusted return."""
```

## Data Models

### SwapQuote

```
SwapQuote:
  token_in: str
  token_out: str
  amount_in: float
  amount_out: float
  minimum_out: float
  price_impact: float
  route: list[str]
  fee: float
  gas_estimate: int
  gas_cost_usd: float
```

### PoolInfo

```
PoolInfo:
  address: str
  protocol: str
  token0: str
  token0_symbol: str
  token1: str
  token1_symbol: str
  reserve0: float
  reserve1: float
  lp_supply: float
  fee_tier: float
  tvl_usd: float
  volume_24h: float
```

### LiquidityPosition

```
LiquidityPosition:
  pool_address: str
  lp_tokens: float
  share_of_pool: float
  value0: float
  value1: float
  entry_price_ratio: float
  current_price_ratio: float
  fees_earned: float
  impermanent_loss: float
```

## Deployment Guide

### DEX Integration Deployment

```
1. Configure RPC providers (Alchemy/Infura)
2. Set up wallet with sufficient gas (ETH)
3. Configure slippage and gas parameters
4. Test on Sepolia testnet
5. Deploy to mainnet with small amounts
6. Verify profitability calculations
7. Monitor for MEV attacks
8. Scale to production amounts
```

### Liquidity Provision Deployment

```
1. Analyze pool fee vs volume
2. Calculate expected APR and IL
3. Determine optimal price range (V3)
4. Deposit liquidity
5. Monitor position health
6. Set up fee collection strategy
7. Rebalance when price moves out of range
```

## Monitoring & Observability

### Key DeFi Metrics

| Metric | Description | Alert |
|--------|-------------|-------|
| TVL | Total value locked in protocol | >10% change |
| Volume | 24h trading volume | <50% baseline |
| Fee Revenue | Daily fee collection | >50% drop |
| Oracle Deviation | Price feed variance | >5% deviation |
| Liquidation Volume | Liquidation events | >$1M in 1hr |
| Governance Activity | Proposal submissions | Any admin action |

### Position Monitoring

```python
from defi import PositionMonitor

monitor = PositionMonitor(
    addresses=["0xMyAddress"],
    pools=["0xPool1", "0xPool2"],
    alert_conditions={
        "il_threshold": 0.05,
        "health_factor": 1.2,
        "price_range_exit": True,
    },
)
monitor.start()
```

## Testing Strategy

### Test Categories

```
1. Unit Tests
   ├── Swap quote calculation
   ├── Price impact calculation
   ├── Liquidity math
   └── Fee calculations

2. Integration Tests
   ├── Multi-hop routing
   ├── Flash loan execution
   ├── Oracle integration
   └── Liquidation mechanics

3. Fork Tests
   ├── Mainnet fork simulation
   ├── Historical trade replay
   └── Edge case reproduction

4. Property-Based Tests
   ├── Constant product invariant (x*y=k)
   ├── Conservation of value
   └── No free money (arbitrage bounded)
```

### Fork Testing

```bash
# Test against mainnet state
forge test --fork-url $ETH_RPC_URL --fork-block-number 18000000 -vvv

# Test specific pool interaction
cast call 0xPool "token0()" --fork-url $ETH_RPC_URL
```

## Versioning & Migration

### Protocol Versioning

```
Major: Breaking changes to interfaces or economics
Minor: New features, new pool types, new assets
Patch: Bug fixes, gas optimizations, parameter tuning
```

### Migration Checklist

- [ ] New contract addresses documented
- [ ] Old positions withdrawable
- [ ] New pool parameters configured
- [ ] Oracle feeds updated
- [ ] Frontend updated
- [ ] Monitoring alerts updated
- [ ] Emergency pause tested

## Glossary

| Term | Definition |
|------|-----------|
| AMM | Automated Market Maker — decentralized exchange using math formulas |
| APR | Annual Percentage Rate — simple interest rate |
| APY | Annual Percentage Yield — compounded interest rate |
| Flash Loan | Uncollateralized loan that must be repaid in same transaction |
| Impermanent Loss | Value loss from providing liquidity vs holding |
| Liquidity Pool | Smart contract holding token pairs for trading |
| MEV | Maximal Extractable Value — profit from transaction ordering |
| Slippage | Difference between expected and actual trade price |
| TVL | Total Value Locked — total assets in a protocol |
| TWAP | Time-Weighted Average Price — averaged price over time |
| IL | Impermanent Loss |

## Changelog

### 2.0.0 (2024-12-01)
- Added multi-DEX routing optimizer
- Added MEV protection integration (Flashbots)
- Added concentrated liquidity (V3) support
- Improved gas estimation accuracy

### 1.2.0 (2024-08-15)
- Added flash loan profitability calculator
- Added impermanent loss calculator
- Improved oracle integration

### 1.1.0 (2024-05-20)
- Added lending protocol integration
- Added yield farming calculator
- Added price impact estimation

### 1.0.0 (2024-02-01)
- Initial release with basic swap routing
- Uniswap V2 pool support
- Basic liquidity management

## Contributing Guidelines

### Adding New DEX Support

1. Implement the `DEXAdapter` interface
2. Add pool discovery and quote logic
3. Write unit tests with mock data
4. Add fork tests against mainnet
5. Submit PR with gas benchmarks

### Code Quality

- All functions must have type hints
- Unit test coverage >90%
- Gas benchmarks for all swap paths
- Documentation for new integrations

## License

MIT License

Copyright (c) 2024 DeFi Module Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
