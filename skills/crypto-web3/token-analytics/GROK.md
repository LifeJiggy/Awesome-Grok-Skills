---
name: "token-analytics"
category: "crypto-web3"
version: "2.0.0"
tags: ["crypto-web3", "token", "analytics", "metrics", "market-data"]
---

# Token Analytics

## Overview

The Token Analytics module provides tools for analyzing token economics, on-chain metrics, market dynamics, and token holder distribution. It covers tokenomics modeling, holder concentration analysis, liquidity analysis, whale tracking, and token valuation frameworks.

This skill is essential for crypto analysts, DeFi researchers, and token project teams monitoring and evaluating token performance.

## Core Capabilities

- **Tokenomics Modeling**: Supply schedules, emission curves, burn mechanisms, and inflation analysis
- **Holder Distribution**: Gini coefficient, concentration metrics, and whale identification
- **Liquidity Analysis**: DEX liquidity depth, CEX order book analysis, and slippage estimation
- **Market Metrics**: Market cap, fully diluted valuation, volume analysis, and volatility
- **Whale Tracking**: Large transaction monitoring, accumulation/distribution detection
- **On-Chain Metrics**: Active addresses, transaction count, network value, and NVT ratio
- **Token Valuation**: Discounted cash flow for protocols, comparables analysis, and Metcalfe's law

## Usage Examples

```python
from token_analytics import (
    TokenomicsAnalyzer,
    HolderDistribution,
    LiquidityAnalyzer,
    MarketMetrics,
    WhaleTracker,
)

# --- Tokenomics Analysis ---
analyzer = TokenomicsAnalyzer()
analysis = analyzer.analyze(
    total_supply=1_000_000_000,
    circulating_supply=500_000_000,
    annual_emission=50_000_000,
    burn_rate=0.02,
)
print(f"Circulating: {analysis.circulating_pct:.1%}")
print(f"Inflation rate: {analysis.inflation_rate:.2%}")
print(f"Years to full dilution: {analysis.years_to_full_dilution:.1f}")

# --- Holder Distribution ---
holders = HolderDistribution()
gini = holders.gini_coefficient([100, 50, 30, 10, 5, 3, 2])
print(f"Gini coefficient: {gini:.3f}")
concentration = holders.concentration_metrics([1000, 500, 200, 100, 50])
print(f"Top 1 holders: {concentration.top1_pct:.1%}")
print(f"Top 10 holders: {concentration.top10_pct:.1%}")

# --- Liquidity Analysis ---
liquidity = LiquidityAnalyzer()
depth = liquidity.analyze_depth(
    bids=[(1.0, 10000), (0.99, 15000), (0.98, 20000)],
    asks=[(1.01, 8000), (1.02, 12000), (1.03, 18000)],
)
print(f"Bid depth: ${depth.bid_depth_usd:,.0f}")
print(f"Spread: {depth.spread_pct:.3%}")

# --- Market Metrics ---
metrics = MarketMetrics()
mcap = metrics.calculate_mcap(
    price=2.5,
    circulating_supply=500_000_000,
    total_supply=1_000_000_000,
)
print(f"Market cap: ${mcap.market_cap:,.0f}")
print(f"FDV: ${mcap.fully_diluted_valuation:,.0f}")
print(f"Mcap/FDV ratio: {mcap.mcap_fdv_ratio:.2%}")

# --- Whale Tracking ---
tracker = WhaleTracker()
alerts = tracker.detect_large_transfers(
    transactions=[{"amount": 5000000, "token": "USDC", "from": "0x1234", "to": "0xABCD"}],
    threshold=1000000,
)
for alert in alerts:
    print(f"Whale alert: {alert['amount']:,} {alert['token']}")
```

## Best Practices

- Use Gini coefficient for objective holder concentration measurement
- Track MCap/FDV ratio — low ratio means high future dilution risk
- Monitor whale wallets for accumulation before price moves
- Use NVT ratio (Network Value to Transactions) for valuation context
- Analyze liquidity depth across multiple DEXs for true market depth
- Consider token unlock schedules when evaluating supply dynamics
- Use on-chain metrics for fundamental analysis beyond price charts
- Track active addresses as a proxy for network adoption
- Compare token metrics against similar projects for relative valuation
- Monitor burn rates and buybacks for deflationary token models

## Related Modules

- **defi-patterns**: DeFi protocol token economics
- **nft-marketplace**: NFT marketplace token integration
- **wallet-integration**: Wallet-based token analytics
- **dao-governance**: Token governance mechanics
