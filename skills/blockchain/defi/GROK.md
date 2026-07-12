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
