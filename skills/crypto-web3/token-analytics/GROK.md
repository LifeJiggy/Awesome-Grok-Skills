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

---

## Advanced Configuration

### Analytics Data Sources

Configure multiple data sources for comprehensive analytics.

```python
analytics_config = AnalyticsConfig(
    sources={
        "on_chain": {"provider": "alchemy", "api_key": "..."},
        "dex": {"provider": "dexscreener", "chains": ["ethereum", "polygon"]},
        "cex": {"provider": "coingecko", "api_key": "..."},
        "social": {"provider": "lunarcrush", "api_key": "..."},
    },
    update_intervals={
        "price": 60,  # seconds
        "holder_distribution": 3600,
        "liquidity": 300,
    },
)
```

### Whale Alert Configuration

Configure whale tracking thresholds.

```python
whale_config = WhaleConfig(
    thresholds={
        "ethereum": 100,  # ETH
        "usdc": 1000000,  # USDC
        "nft_floor": 10,  # Floor price in ETH
    },
    alert_channels=["telegram", "discord", "email"],
    tracking_wallets=[
        "0xWhale1...", "0xWhale2...",
    ],
)
```

### Token Screening

Configure token screening criteria.

```python
screen_config = TokenScreenConfig(
    filters={
        "min_liquidity_usd": 100000,
        "min_holders": 100,
        "max_top10_concentration": 0.5,
        "min_age_days": 30,
    },
    scoring={
        "liquidity_weight": 0.3,
        "holder_distribution_weight": 0.3,
        "volume_weight": 0.2,
        "social_weight": 0.2,
    },
)
```

---

## Architecture Patterns

### Data Collection Pipeline

```python
class TokenDataPipeline:
    def __init__(self):
        self.collectors = [
            PriceCollector(),
            HolderCollector(),
            LiquidityCollector(),
            SocialCollector(),
        ]

    def run(self, token_address):
        data = {}
        for collector in self.collectors:
            data.update(collector.collect(token_address))
        return data
```

### Anomaly Detection Pattern

```python
class TokenAnomalyDetector:
    def __init__(self):
        self.baselines = {}

    def detect(self, token, current_metrics):
        baseline = self.baselines.get(token)
        if baseline:
            anomalies = []
            for metric, value in current_metrics.items():
                z_score = (value - baseline[metric]['mean']) / baseline[metric]['std']
                if abs(z_score) > 3:
                    anomalies.append(Anomaly(metric, value, z_score))
            return anomalies
```

### Alert Pattern

```python
class TokenAlertSystem:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def check(self, token, metrics):
        for rule in self.rules:
            if rule.evaluate(metrics):
                self.send_alert(token, rule)
```

---

## Integration Guide

### CoinGecko Integration

```python
import coingecko

cg = coingecko.CoinGeckoAPI()
token_data = cg.get_coin(token_id)
price = token_data['market_data']['current_price']['usd']
market_cap = token_data['market_data']['market_cap']['usd']
```

### DEX Screener Integration

```python
# Get DEX pair data
dex_data = DexScreenerAPI().get_pair(pair_address)
volume_24h = dex_data['volume']['h24']
price_change_24h = dex_data['priceChange']['h24']
```

### Glassnode Integration

```python
# On-chain metrics
glassnode = GlassnodeAPI(api_key="...")
active_addresses = glassnode.get_metric(token, "active_addresses")
nvt_ratio = glassnode.get_metric(token, "nvt_ratio")
```

---

## Performance Optimization

### Data Caching

```python
# Cache analytics data
analytics_cache = AnalyticsCache(
    backend="redis",
    ttl_prices=60,
    ttl_holders=3600,
    ttl_liquidity=300,
)
```

### Batch Processing

```python
# Process multiple tokens in batch
def batch_analyze(tokens):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(analyze, t): t for t in tokens}
        return {futures[f]: f.result() for f in as_completed(futures)}
```

---

## Security Considerations

### Data Validation

```python
# Validate on-chain data
def validate_holder_data(holders):
    total = sum(h.amount for h in holders)
    assert abs(total - total_supply) < 1e-6, "Holder data doesn't match supply"
```

### API Key Security

```python
# Never expose API keys in code
import os
api_key = os.environ.get("COINGECKO_API_KEY")
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Stale prices | API rate limit | Implement backoff |
| Missing holders | Indexing delay | Wait or use different provider |
| Wrong metrics | Token contract change | Verify token address |

---

## API Reference

### TokenomicsAnalyzer

```python
class TokenomicsAnalyzer:
    def analyze(total_supply, circulating, emission, burn_rate) -> TokenomicsResult
    def project_supply(years) -> SupplyProjection
```

### HolderDistribution

```python
class HolderDistribution:
    def gini_coefficient(holdings) -> float
    def concentration_metrics(holdings) -> ConcentrationResult
    def lorenz_curve(holdings) -> Curve
```

### WhaleTracker

```python
class WhaleTracker:
    def detect_large_transfers(transactions, threshold) -> List[WhaleAlert]
    def track_wallets(addresses) -> WalletActivity
    def accumulation_signal(token) -> Signal
```

---

## Data Models

### TokenomicsResult

```python
@dataclass
class TokenomicsResult:
    circulating_pct: float
    inflation_rate: float
    years_to_full_dilution: float
    supply_schedule: List[SupplyPoint]
```

### WhaleAlert

```python
@dataclass
class WhaleAlert:
    amount: float
    token: str
    from_address: str
    to_address: str
    timestamp: datetime
    usd_value: float
```

---

## Deployment Guide

### Analytics Service Deployment

```yaml
services:
  analytics:
    image: token-analytics:latest
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
      - API_KEYS_PATH=/run/secrets/api_keys
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `analytics.price.latency` | Price update latency | > 30s |
| `analytics.holder.freshness` | Holder data freshness | > 1h |
| `analytics.alert.count` | Alerts sent per day | Anomaly |

---

## Testing Strategy

### Analytics Tests

```python
def test_gini_coefficient():
    hd = HolderDistribution()
    gini = hd.gini_coefficient([100, 50, 30, 10, 5])
    assert 0 <= gini <= 1
    assert gini > 0.5  # Unequal distribution
```

---

## Versioning & Migration

### Data Schema Versioning

Track analytics data schema versions for backward compatibility.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Gini Coefficient** | Measure of inequality (0 = equal, 1 = unequal) |
| **NVT Ratio** | Network Value to Transactions ratio |
| **MCap/FDV** | Market Cap to Fully Diluted Valuation ratio |
| **Whale** | Large token holder |
| **Liquidity Depth** | Total value available in order book |

---

## Changelog

### v2.0.0
- Added whale tracking
- Multi-chain analytics
- Social metrics integration

### v1.0.0
- Initial release with basic tokenomics

---

## Contributing Guidelines

- Validate all on-chain data
- Document data sources
- Handle API rate limits gracefully

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Advanced Configuration

### Tokenomics Configuration

```yaml
tokenomics:
  token_name: "Governance Token"
  symbol: "GOV"
  total_supply: 1000000000
  initial_circulating: 100000000
  emission_schedule:
    - years: 0-1
      annual_emission: 50000000
    - years: 1-2
      annual_emission: 25000000
    - years: 2-3
      annual_emission: 12500000
    - years: 3+
      annual_emission: 6250000
  burn_mechanisms:
    - type: "transaction_fee"
      percentage: 0.5
    - type: "buyback_burn"
      percentage: 20
```

### Analytics Configuration

```yaml
analytics:
  data_sources:
    - name: "on_chain"
      provider: "alchemy"
      api_key: "${ALCHEMY_API_KEY}"
    - name: "dex"
      provider: "uniswap_v3"
    - name: "cex"
      provider: "coingecko"
  update_frequency: "5m"
  alert_thresholds:
    whale_transfer: 1000000
    price_change_1h: 5
    volume_spike: 300
    holder_change_24h: 10
```

## Architecture Patterns

### Token Analytics Architecture

```
Analytics Stack:
├── Data Collection
│   ├── On-chain indexing (Subgraph/Dune)
│   ├── DEX aggregators (1inch, Paraswap)
│   ├── CEX APIs (CoinGecko, CoinMarketCap)
│   └── Social metrics (LunarCrush, Santiment)
├── Processing
│   ├── Real-time streaming (Kafka/Redis)
│   ├── Batch processing (Airflow)
│   ├── ML pipelines (feature engineering)
│   └── Backtesting framework
├── Storage
│   ├── Time-series DB (InfluxDB)
│   ├── Analytics DB (ClickHouse)
│   ├── Cache (Redis)
│   └── Data lake (S3/GCS)
├── Analytics
│   ├── Tokenomics modeling
│   ├── Holder analysis
│   ├── Liquidity analysis
│   ├── Whale tracking
│   └── Valuation models
└── Visualization
    ├── Dashboard (Grafana)
    ├── Reports (PDF/CSV)
    ├── Alerts (Email/Webhook)
    └── API (GraphQL/REST)
```

### Holder Distribution Analysis

```
Holder Analysis Pipeline:
├── Data Collection
│   ├── Token transfers
│   ├── Holder snapshots
│   └── Historical balances
├── Metrics Calculation
│   ├── Gini coefficient
│   ├── Nakamoto coefficient
│   ├── Top holder concentration
│   ├── HHI (Herfindahl-Hirschman)
│   └── Holder growth rate
├── Classification
│   ├── Retail (< 1 token)
│   ├── Small (1-1K tokens)
│   ├── Medium (1K-100K tokens)
│   ├── Large (100K-1M tokens)
│   └── Whale (> 1M tokens)
└── Insights
    ├── Concentration trends
    ├── Accumulation patterns
    ├── Distribution phases
    └── Institutional vs retail
```

### Liquidity Analysis Architecture

```
Liquidity Pipeline:
├── DEX Liquidity
│   ├── Pool reserves
│   ├── LP token holders
│   ├── Fee APR
│   └── Price impact
├── CEX Liquidity
│   ├── Order book depth
│   ├── Bid-ask spread
│   ├── Volume profile
│   └── Liquidation levels
├── Aggregated Metrics
│   ├── Total liquidity (DEX + CEX)
│   ├── Liquidity depth (1%, 5%, 10%)
│   ├── Slippage estimation
│   └── Market impact model
└── Alerts
    ├── Low liquidity warnings
    ├── Liquidity migration
    └── Whale exit detection
```

### Whale Tracking Architecture

```
Whale Tracking Pipeline:
├── Detection
│   ├── Large transfer monitoring
│   ├── Wallet clustering
│   └── Entity identification
├── Classification
│   ├── Exchange hot wallets
│   ├── Institutional wallets
│   ├── DeFi protocols
│   └── Individual whales
├── Analysis
│   ├── Accumulation vs distribution
│   ├── Transaction patterns
│   ├── Cross-chain movements
│   └── Sentiment correlation
└── Alerts
    ├── Real-time transfer alerts
    ├── Pattern detection
    └── Risk scoring
```

## Integration Guide

### On-Chain Analytics Integration

```python
import requests
from web3 import Web3

class OnChainAnalytics:
    def __init__(self, rpc_url, subgraph_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.subgraph_url = subgraph_url

    def get_token_holders(self, token_address, block_number="latest"):
        """Get token holder distribution."""
        query = """
        query TokenHolders($token: String!, $block: Int!) {
            token(id: $token, block: {number: $block}) {
                totalSupply
                holderCount
                holders(first: 1000, orderBy: balance, orderDirection: desc) {
                    address
                    balance
                    percentage
                }
            }
        }
        """
        response = requests.post(
            self.subgraph_url,
            json={"query": query, "variables": {"token": token_address.lower(), "block": block_number}}
        )
        return response.json()["data"]["token"]

    def calculate_gini(self, holder_balances):
        """Calculate Gini coefficient for holder distribution."""
        sorted_balances = sorted(holder_balances)
        n = len(sorted_balances)
        cumulative = 0
        total = sum(sorted_balances)

        for i, balance in enumerate(sorted_balances):
            cumulative += (2 * (i + 1) - n - 1) * balance

        return cumulative / (n * total)

    def get_whale_transactions(self, token_address, min_value=1000000):
        """Get large token transactions."""
        query = """
        query WhaleTransactions($token: String!, $minValue: BigDecimal!) {
            transfers(
                where: {token: $token, value_gte: $minValue}
                orderBy: value
                orderDirection: desc
                first: 100
            ) {
                from
                to
                value
                timestamp
                txHash
            }
        }
        """
        response = requests.post(
            self.subgraph_url,
            json={"query": query, "variables": {"token": token_address.lower(), "minValue": str(min_value)}}
        )
        return response.json()["data"]["transfers"]
```

### DEX Analytics Integration

```python
class DEXAnalytics:
    def __init__(self, subgraph_url):
        self.subgraph_url = subgraph_url

    def get_pool_liquidity(self, pool_address):
        """Get DEX pool liquidity metrics."""
        query = """
        query PoolLiquidity($pool: String!) {
            pool(id: $pool) {
                token0 { symbol }
                token1 { symbol }
                reserve0
                reserve1
                totalValueLockedUSD
                volume24h
                feeTier
                tick
            }
        }
        """
        response = requests.post(
            self.subgraph_url,
            json={"query": query, "variables": {"pool": pool_address.lower()}}
        )
        return response.json()["data"]["pool"]

    def calculate_slippage(self, pool_address, trade_size, direction):
        """Calculate price impact for trade size."""
        pool = self.get_pool_liquidity(pool_address)
        reserve_in = float(pool["reserve0"]) if direction == "buy" else float(pool["reserve1"])
        reserve_out = float(pool["reserve1"]) if direction == "buy" else float(pool["reserve0"])

        # Constant product formula: (x + dx) * (y - dy) = x * y
        price_impact = trade_size / (reserve_in + trade_size)
        return {
            "price_impact_pct": price_impact * 100,
            "slippage_pct": price_impact * 100 * 0.997,  # accounting for 0.3% fee
            "received_amount": reserve_out * (1 - (1 / (1 + trade_size / reserve_in)))
        }
```

### CoinGecko API Integration

```python
class CoinGeckoAnalytics:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, api_key=None):
        self.api_key = api_key

    def get_token_data(self, token_id):
        """Get comprehensive token data."""
        endpoint = f"{self.BASE_URL}/coins/{token_id}"
        params = {
            "localization": "false",
            "tickers": "true",
            "market_data": "true",
            "community_data": "true",
            "developer_data": "false"
        }
        if self.api_key:
            params["x_cg_demo_api_key"] = self.api_key

        response = requests.get(endpoint, params=params)
        data = response.json()

        return {
            "name": data["name"],
            "symbol": data["symbol"],
            "market_cap": data["market_data"]["market_cap"]["usd"],
            "volume_24h": data["market_data"]["total_volume"]["usd"],
            "price_change_24h": data["market_data"]["price_change_percentage_24h"],
            "price_change_7d": data["market_data"]["price_change_percentage_7d"],
            "ath": data["market_data"]["ath"]["usd"],
            "ath_change": data["market_data"]["ath_change_percentage"]["usd"],
            "circulating_supply": data["market_data"]["circulating_supply"],
            "total_supply": data["market_data"]["total_supply"],
            "fdv": data["market_data"]["fully_diluted_valuation"]["usd"]
        }

    def get_historical_prices(self, token_id, days=30):
        """Get historical price data."""
        endpoint = f"{self.BASE_URL}/coins/{token_id}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        response = requests.get(endpoint, params=params)
        return response.json()["prices"]
```

## Performance Optimization

### Data Processing Optimization

| Technique | Description | Speedup |
|-----------|-------------|---------|
| Incremental updates | Process only new data | 10-50x |
| Parallel processing | Multiple chains/tokens | 2-4x |
| Caching | Cache frequent queries | 5-10x |
| Materialized views | Pre-computed analytics | 3-5x |

### Query Optimization

```
Query Strategies:
├── Indexing
│   ├── Composite indexes (token, timestamp)
│   ├── Partial indexes (recent data)
│   └── Full-text search (addresses)
├── Caching
│   ├── Real-time: Redis (1s TTL)
│   ├── Short-term: Redis (5m TTL)
│   ├── Medium-term: Materialized views
│   └── Long-term: Data warehouse
├── Pagination
│   ├── Cursor-based (preferred)
│   ├── Keyset pagination
│   └── Avoid OFFSET for large datasets
└── Optimization
    ├── Select only needed columns
    ├── Avoid N+1 queries
    └── Use DataLoader for batching
```

## Security Considerations

### Data Security

| Control | Description | Implementation |
|---------|-------------|----------------|
| API Key Management | Secure key storage | Vault/KMS |
| Rate Limiting | Prevent abuse | Redis + sliding window |
| Input Validation | Sanitize queries | Parameterized queries |
| Access Control | API key scoping | Role-based access |
| Audit Logging | Track data access | CloudTrail/ELK |

### Data Integrity

```
Data Validation:
├── Source verification
│   ├── Cross-reference multiple sources
│   ├── Anomaly detection
│   └── Confidence scoring
├── Processing validation
│   ├── Schema validation
│   ├── Checksum verification
│   └── Idempotency checks
├── Output validation
│   ├── Range checks
│   ├── Consistency checks
│   └── Historical consistency
└── Monitoring
│   ├── Data freshness alerts
│   ├── Anomaly alerts
│   └── Pipeline health checks
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Stale data | Metrics not updating | Check indexer, increase frequency |
| Missing holders | Incomplete distribution | Check subgraph sync |
| API rate limit | 429 errors | Implement backoff, use paid tier |
| Incorrect Gini | Wrong calculation | Verify input data, check edge cases |
| Whale false positive | Normal transfer flagged | Adjust thresholds, check context |

### Debugging Commands

```bash
# Check token supply
cast call $TOKEN "totalSupply()" --rpc-url $RPC

# Check holder balance
cast call $TOKEN "balanceOf(address)" $HOLDER --rpc-url $RPC

# Get recent transfers
cast log $TRANSFER_EVENT --from-block -1000 --rpc-url $RPC

# Check DEX pool
cast call $POOL "getReserves()" --rpc-url $RPC
```

## Testing Strategy

### Analytics Testing

```
1. Unit Tests
   ├── Metric calculations
   ├── Gini coefficient
   ├── Slippage estimation
   └── Whale detection

2. Integration Tests
   ├── Data source integration
   ├── Pipeline end-to-end
   ├── Alert system
   └── API endpoints

3. Accuracy Tests
   ├── Historical backtesting
   ├── Cross-source validation
   ├── Edge case handling
   └── Performance benchmarks

4. Data Quality Tests
   ├── Completeness checks
   ├── Freshness checks
   ├── Consistency checks
   └── Anomaly detection
```

## Versioning & Migration

### Versioning

```
Major: Metric changes
├── Example: New valuation model
├── Requires: Full backtesting
└── Risk: High

Minor: New metrics
├── Example: Add NVT ratio
├── Requires: Validation
└── Risk: Low

Patch: Bug fixes
├── Example: Fix Gini calculation
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| Gini Coefficient | Measure of distribution inequality (0=equal, 1=unequal) |
| HHI | Herfindahl-Hirschman Index (market concentration) |
| NVT Ratio | Network Value to Transactions ratio |
| TVL | Total Value Locked in DeFi protocols |
| FDV | Fully Diluted Valuation |
| MVRV | Market Value to Realized Value ratio |
| SOPR | Spent Output Profit Ratio |
| NUPL | Net Unrealized Profit/Loss |
| OI | Open Interest in derivatives |
| Funding Rate | Perpetual futures funding rate |

## Changelog

### v2.0.0
- Added whale tracking
- Multi-chain analytics
- Social metrics integration

### v1.0.0
- Initial release with basic tokenomics
