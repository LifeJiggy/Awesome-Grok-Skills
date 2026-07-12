---
name: "defi-patterns"
category: "crypto-web3"
version: "2.0.0"
tags: ["crypto-web3", "defi", "patterns", "amm", "yield", "lending"]
---

# DeFi Patterns

## Overview

The DeFi Patterns module provides comprehensive reference material for common decentralized finance patterns, including Automated Market Makers (AMMs), lending protocols, yield farming, flash loans, and stablecoin mechanics. It covers pattern implementations, economic modeling, security considerations, and composability patterns.

This skill is essential for DeFi protocol developers, smart contract auditors, and Web3 architects building financial infrastructure on blockchain.

## Core Capabilities

- **AMM Patterns**: Constant product (x*y=k), concentrated liquidity, stable swap curves (Curve-style)
- **Lending**: Over-collateralized lending, interest rate models, liquidation mechanics
- **Yield**: Liquidity mining, staking rewards, auto-compounding vaults
- **Flash Loans**: Atomic arbitrage, liquidation bots, and collateral swap patterns
- **Stablecoins**: Algorithmic stablecoins, CDP (Collateralized Debt Position), and reserve-backed
- **Governance**: Token-weighted voting, quadratic voting, and delegation patterns
- **Composability**: Protocol stacking, money legos, and cross-protocol interactions

## Usage Examples

```python
from defi_patterns import (
    AMMCalculator,
    LendingModel,
    YieldCalculator,
    FlashLoanSimulator,
    StablecoinModel,
)

# --- AMM Calculator ---
amm = AMMCalculator(reserve_a=1000, reserve_b=2_000_000)
output = amm.calculate_swap(input_amount=10, input_token="A")
print(f"Swap: {input_amount} A -> {output.output_amount:.2f} B")
print(f"Price impact: {output.price_impact:.2%}")
print(f"Fee: {output.fee:.4f}")

# --- Stable Swap ---
stable = StableSwapCalculator(
    balances=[1_000_000, 1_000_000, 1_000_000],
    amplification=100,
)
output = stable.swap(input_index=0, output_index=1, amount=10_000)
print(f"Stable swap: {output.output_amount:.2f}")

# --- Lending ---
lending = LendingModel(
    collateral=10,  # ETH
    collateral_price=3000,
    borrow_amount=15_000,  # USDC
)
health = lending.health_factor()
print(f"Health factor: {health:.2f}")
print(f"Liquidation price: ${lending.liquidation_price:.0f}")

# --- Yield ---
yield_calc = YieldCalculator()
apy = yield_calc.calculate_apy(
    reward_per_day=100,
    token_price=5,
    staked_value=100_000,
)
print(f"APY: {apy:.1%}")

# --- Flash Loan ---
flash = FlashLoanSimulator()
profit = flash.simulate_arbitrage(
    flash_amount=1_000_000,
    buy_price=0.999,
    sell_price=1.001,
    gas_cost_usd=10,
)
print(f"Flash loan profit: ${profit:.2f}")
```

## Best Practices

- Use constant product AMM (x*y=k) for volatile pairs; Curve-style for stable pairs
- Set liquidation threshold at 75-80% LTV for safety margin
- Always simulate flash loan transactions before executing on-chain
- Implement slippage protection on all swaps (0.5-1% for normal, 3-5% for volatile)
- Use time-weighted average prices (TWAP) for oracle-dependent protocols
- Test economic models with extreme scenarios (10x price swing, 0 liquidity)
- Implement circuit breakers for unusual protocol behavior
- Audit all token transfer logic for reentrancy vulnerabilities
- Use OpenZeppelin's ERC-4626 for vault standardization
- Document all economic assumptions and risk parameters

## Related Modules

- **nft-marketplace**: NFT trading patterns
- **token-analytics**: Token analysis and metrics
- **wallet-integration**: Wallet connection patterns
- **dao-governance**: DAO governance mechanisms
