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

---

## Advanced Configuration

### AMM Configuration

Configure AMM parameters for different pool types.

```python
amm_config = AMMConfig(
    pool_types={
        "volatile": {"fee": 0.003, "curve": "constant_product"},
        "stable": {"fee": 0.0004, "curve": "stable_swap", "amplification": 100},
        "concentrated": {"fee_tiers": [0.0001, 0.0005, 0.003, 0.01]},
    },
    default_slippage=0.005,
    max_slippage=0.05,
)
```

### Lending Protocol Configuration

Configure lending parameters.

```python
lending_config = LendingConfig(
    collateral_factors={"ETH": 0.75, "WBTC": 0.70, "USDC": 0.85},
    liquidation_bonus=0.05,
    reserve_factor=0.10,
    interest_rate_model={
        "base_rate": 0.02,
        "slope1": 0.04,
        "slope2": 0.75,
        "optimal_utilization": 0.80,
    },
)
```

### Yield Farming Configuration

Configure yield farming parameters.

```python
yield_config = YieldConfig(
    reward_tokens=["GOV", "COMP"],
    emission_rate_per_block=0.1,
    lock_period_days=7,
    boost_multiplier=2.0,
)
```

---

## Architecture Patterns

### AMM Pool Pattern

```python
class AMMPool:
    def __init__(self, token_a, token_b, fee=0.003):
        self.reserve_a = 0
        self.reserve_b = 0
        self.fee = fee

    def swap(self, input_token, input_amount):
        if input_token == "A":
            output_amount = self.calculate_output(input_amount, self.reserve_a, self.reserve_b)
            self.reserve_a += input_amount
            self.reserve_b -= output_amount
        return output_amount

    def add_liquidity(self, amount_a, amount_b):
        self.reserve_a += amount_a
        self.reserve_b += amount_b
        return self.calculate_lp_tokens(amount_a, amount_b)
```

### Flash Loan Pattern

```python
class FlashLoanProtocol:
    def flash_loan(self, token, amount, callback):
        # Transfer tokens to borrower
        self.transfer(token, borrower, amount)

        # Execute callback
        result = callback(amount)

        # Verify repayment with fee
        fee = amount * self.fee_rate
        assert self.balance(token) >= amount + fee

        return result
```

### Liquidation Bot Pattern

```python
class LiquidationBot:
    def monitor_positions(self):
        while True:
            positions = self.get_liquidatable_positions()
            for position in positions:
                self.execute_liquidation(position)
            time.sleep(1)

    def execute_liquidation(self, position):
        profit = self.calculate_profit(position)
        if profit > self.min_profit:
            self.liquidate(position)
```

---

## Integration Guide

### Web3.py Integration

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/..."))

# Interact with AMM
amm_contract = w3.eth.contract(address=amm_address, abi=amm_abi)
tx = amm_contract.functions.swap(
    token_in,
    amount_in,
    min_amount_out,
).build_transaction({...})
```

### Ethers.js Integration

```javascript
const { ethers } = require('ethers');

const provider = new ethers.providers.JsonRpcProvider("https://mainnet.infura.io/v3/...");
const amm = new ethers.Contract(ammAddress, ammAbi, signer);

const tx = await amm.swap(tokenIn, amountIn, minAmountOut);
await tx.wait();
```

---

## Performance Optimization

### Gas Optimization

```python
# Batch multiple operations
class BatchRouter:
    def multi_hop_swap(self, path, amount_in, min_amount_out):
        # Single transaction for multi-hop
        return self.router.functions.multicall(
            path, amount_in, min_amount_out
        ).transact()
```

### Quoting Optimization

```python
# Cache quotes for frequent pairs
quote_cache = QuoteCache(
    ttl_seconds=5,
    max_entries=100,
)
```

---

## Security Considerations

### Slippage Protection

```python
# Always set slippage tolerance
min_amount_out = calculate_output(amount_in) * (1 - slippage_tolerance)
```

### Reentrancy Protection

```python
# Use checks-effects-interactions pattern
def withdraw(token, amount):
    balances[msg.sender] -= amount  # Effect before interaction
    token.transfer(msg.sender, amount)  # Interaction
```

### Oracle Manipulation Prevention

```python
# Use TWAP oracles instead of spot prices
class TWAPOracle:
    def get_price(self, token):
        prices = self.get_recent_prices(token, periods=30)
        return sum(prices) / len(prices)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Slippage error | Price moved too much | Increase slippage tolerance |
| Transaction reverted | Insufficient gas | Increase gas limit |
| Liquidation failed | Position not liquidatable | Check health factor |
| Low yield | High gas costs | Batch operations |

---

## API Reference

### AMMCalculator

```python
class AMMCalculator:
    def calculate_swap(amount_in, input_token) -> SwapResult
    def calculate_lp_tokens(amount_a, amount_b) -> float
    def calculate_price_impact(amount_in, input_token) -> float
    def get_pool_state() -> PoolState
```

### LendingModel

```python
class LendingModel:
    def health_factor() -> float
    def liquidation_price() -> float
    def borrow_apr() -> float
    def supply_apr() -> float
    def calculate_liquidation_profit(debt, collateral) -> float
```

---

## Data Models

### SwapResult

```python
@dataclass
class SwapResult:
    output_amount: float
    price_impact: float
    fee: float
    route: List[str]
    gas_estimate: int
```

### PoolState

```python
@dataclass
class PoolState:
    reserve_a: float
    reserve_b: float
    total_supply: float
    fee: float
    k: float
```

---

## Deployment Guide

### Smart Contract Deployment

```bash
# Deploy AMM Pool
forge create --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  src/AMMPool.sol:AMMPool \
  --constructor-args $TOKEN_A $TOKEN_B 30
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `amm.tvl` | Total value locked | < $1M |
| `amm.daily.volume` | Daily trading volume | Anomaly |
| `lending.utilization.rate` | Borrow utilization | > 90% |
| `liquidation.count` | Liquidation events | Spike |

---

## Testing Strategy

### Smart Contract Tests

```python
def test_swap():
    pool = AMMPool(token_a, token_b, fee=0.003)
    pool.add_liquidity(1000, 1000000)
    output = pool.swap("A", 10)
    assert output > 0
    assert pool.reserve_a == 1010
```

---

## Versioning & Migration

### Protocol Versioning

Follow semantic versioning for smart contracts.

---

## Advanced Configuration (Extended)

### AMM Configuration (Extended)

Configure advanced AMM parameters.

```python
advanced_amm_config = AdvancedAMMConfig(
    fee_tiers={
        "low_volatility": [0.0001, 0.0005],
        "normal": [0.003],
        "high_volatility": [0.01],
    },
    tick_spacing={
        "low": 1,
        "medium": 10,
        "high": 60,
    },
    price_oracle={
        "type": "twap",
        "period_seconds": 1800,
        "min_periods": 2,
    },
)
```

### Lending Protocol Configuration (Extended)

Configure advanced lending parameters.

```python
advanced_lending_config = AdvancedLendingConfig(
    interest_rate_model={
        "type": "jump_rate",
        "base_rate": 0.02,
        "slope1": 0.04,
        "slope2": 0.75,
        "optimal_utilization": 0.80,
    },
    liquidation_parameters={
        "liquidation_threshold": 0.80,
        "liquidation_bonus": 0.05,
        "close_factor": 0.5,
        "min_liquidation_amount": 100,
    },
    collateral_parameters={
        "ETH": {"ltv": 0.75, "liquidation_threshold": 0.80},
        "WBTC": {"ltv": 0.70, "liquidation_threshold": 0.75},
        "USDC": {"ltv": 0.85, "liquidation_threshold": 0.90},
    },
)
```

### Yield Farming Configuration (Extended)

Configure advanced yield farming parameters.

```python
advanced_yield_config = AdvancedYieldConfig(
    staking_pools={
        "ETH": {"lock_period_days": 0, "boost_multiplier": 1.0},
        "GOV_TOKEN": {"lock_period_days": 30, "boost_multiplier": 2.0},
        "LP_TOKEN": {"lock_period_days": 7, "boost_multiplier": 1.5},
    },
    emission_schedule={
        "type": "halving",
        "initial_rate": 100,
        "halving_interval_days": 90,
        "minimum_rate": 1,
    },
    reward_distribution={
        "type": "pro_rata",
        "distribution_frequency": "block",
    },
)
```

---

## Architecture Patterns (Extended)

### AMM Pool Pattern (Extended)

```python
class AdvancedAMMPool:
    def __init__(self, token_a, token_b, fee=0.003):
        self.reserve_a = 0
        self.reserve_b = 0
        self.fee = fee
        self.fee_protocol = 0.1  # 10% to protocol
        self.price_oracle = PriceOracle()
        self.liquidity_positions = {}

    def swap(self, input_token, input_amount, min_output):
        # Calculate output with fee
        fee_amount = input_amount * self.fee
        net_input = input_amount - fee_amount
        
        if input_token == "A":
            output_amount = (net_input * self.reserve_b) / (self.reserve_a + net_input)
        else:
            output_amount = (net_input * self.reserve_a) / (self.reserve_b + net_input)
        
        # Price impact check
        price_impact = abs(output_amount / self.get_mid_price() - input_amount) / input_amount
        if price_impact > 0.05:  # 5% max price impact
            raise PriceImpactTooHigh(f"Price impact: {price_impact:.2%}")
        
        # Update reserves
        if input_token == "A":
            self.reserve_a += input_amount
            self.reserve_b -= output_amount
        else:
            self.reserve_b += input_amount
            self.reserve_a -= output_amount
        
        # Update oracle
        self.price_oracle.update(self.get_mid_price())
        
        return output_amount

    def add_liquidity(self, amount_a, amount_b, provider):
        # Calculate LP tokens
        lp_tokens = min(
            amount_a * self.total_supply / self.reserve_a,
            amount_b * self.total_supply / self.reserve_b,
        )
        
        # Update reserves
        self.reserve_a += amount_a
        self.reserve_b += amount_b
        self.total_supply += lp_tokens
        
        # Record position
        self.liquidity_positions[provider] = {
            'lp_tokens': lp_tokens,
            'share': lp_tokens / self.total_supply,
        }
        
        return lp_tokens

    def remove_liquidity(self, provider, lp_tokens):
        share = lp_tokens / self.total_supply
        amount_a = self.reserve_a * share
        amount_b = self.reserve_b * share
        
        # Update reserves
        self.reserve_a -= amount_a
        self.reserve_b -= amount_b
        self.total_supply -= lp_tokens
        
        # Remove position
        del self.liquidity_positions[provider]
        
        return amount_a, amount_b
```

### Flash Loan Pattern (Extended)

```python
class AdvancedFlashLoanProtocol:
    def __init__(self):
        self.fee_rate = 0.0009  # 0.09%
        self.min_flash_amount = 1000

    def flash_loan(self, token, amount, borrower, callback):
        # Validate
        if amount < self.min_flash_amount:
            raise FlashLoanTooSmall(f"Minimum: {self.min_flash_amount}")
        
        # Calculate fee
        fee = int(amount * self.fee_rate)
        
        # Transfer tokens to borrower
        self.transfer(token, borrower, amount)
        
        # Execute callback
        try:
            success = callback(amount, fee)
            if not success:
                raise FlashLoanCallbackFailed()
        except Exception as e:
            # Revert transfer
            self.transfer(token, borrower, -amount)
            raise
        
        # Verify repayment
        balance = self.balance(token, borrower)
        required = amount + fee
        if balance < required:
            raise InsufficientRepayment(f"Need {required}, have {balance}")
        
        # Collect fee
        self.transfer(token, borrower, -fee)
        
        return True

    def arbitrage_flash_loan(self, token_a, token_b, amount_a, dex_a, dex_b):
        """Execute arbitrage using flash loan."""
        def arbitrage_callback(borrowed_amount, fee):
            # Buy on dex_a
            amount_b = dex_a.swap(token_a, token_b, borrowed_amount)
            # Sell on dex_b
            amount_a_back = dex_b.swap(token_b, token_a, amount_b)
            # Repay
            return amount_a_back >= borrowed_amount + fee
        
        return self.flash_loan(token_a, amount_a, self.address, arbitrage_callback)
```

### Liquidation Bot Pattern (Extended)

```python
class AdvancedLiquidationBot:
    def __init__(self):
        self.min_profit_threshold = 50  # USD
        self.gas_price_limit = 100  # gwei
        self.position_cache = {}

    def monitor_positions(self):
        while True:
            positions = self.get_all_positions()
            for position in positions:
                health_factor = self.calculate_health_factor(position)
                if health_factor < 1.0:
                    self.queue_liquidation(position)
            time.sleep(1)

    def calculate_health_factor(self, position):
        collateral_value = position.collateral * self.get_price(position.collateral_token)
        debt_value = position.debt * self.get_price(position.debt_token)
        return (collateral_value * position.liquidation_threshold) / debt_value

    def execute_liquidation(self, position):
        # Calculate profit
        collateral_to_seize = position.debt * position.liquidation_bonus
        profit = (collateral_to_seize * self.get_price(position.collateral_token) -
                  position.debt * self.get_price(position.debt_token) -
                  self.estimate_gas_cost())
        
        if profit < self.min_profit_threshold:
            return None
        
        # Execute liquidation
        tx = self.build_liquidation_tx(position, collateral_to_seize)
        return self.send_tx(tx)
```

---

## Integration Guide (Extended)

### Web3.py Integration (Extended)

```python
from web3 import Web3
from eth_account import Account

class DeFiIntegration:
    def __init__(self, rpc_url, private_key):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        
    def swap_tokens(self, router_address, token_in, token_out, amount_in, min_amount_out):
        router = self.w3.eth.contract(
            address=router_address,
            abi=ROUTER_ABI
        )
        
        # Approve token
        token_contract = self.w3.eth.contract(
            address=token_in,
            abi=ERC20_ABI
        )
        token_contract.functions.approve(
            router_address, amount_in
        ).transact({'from': self.account.address})
        
        # Execute swap
        tx = router.functions.swapExactTokensForTokens(
            amount_in,
            min_amount_out,
            [token_in, token_out],
            self.account.address,
            int(time.time()) + 300
        ).build_transaction({
            'from': self.account.address,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })
        
        signed_tx = self.account.sign_transaction(tx)
        return self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
```

### Ethers.js Integration (Extended)

```javascript
const { ethers } = require('ethers');

class DeFiClient {
    constructor(rpcUrl, privateKey) {
        this.provider = new ethers.providers.JsonRpcProvider(rpcUrl);
        this.wallet = new ethers.Wallet(privateKey, this.provider);
    }

    async swapTokens(routerAddress, tokenIn, tokenOut, amountIn, minAmountOut) {
        const router = new ethers.Contract(routerAddress, ROUTER_ABI, this.wallet);
        
        // Approve
        const token = new ethers.Contract(tokenIn, ERC20_ABI, this.wallet);
        await token.approve(routerAddress, amountIn);
        
        // Swap
        const tx = await router.swapExactTokensForTokens(
            amountIn,
            minAmountOut,
            [tokenIn, tokenOut],
            this.wallet.address,
            Math.floor(Date.now() / 1000) + 300
        );
        
        return await tx.wait();
    }
}
```

---

## Performance Optimization (Extended)

### Gas Optimization (Extended)

```python
class GasOptimizer:
    def optimize_transaction(self, tx):
        # Estimate gas
        gas_estimate = self.w3.eth.estimate_gas(tx)
        
        # Add buffer
        tx['gas'] = int(gas_estimate * 1.2)
        
        # Optimize gas price
        current_gas_price = self.w3.eth.gas_price
        tx['gasPrice'] = int(current_gas_price * 1.1)
        
        return tx

    def batch_transactions(self, transactions):
        # Use multicall for batch operations
        multicall = self.w3.eth.contract(
            address=MULTICALL_ADDRESS,
            abi=MULTICALL_ABI
        )
        
        calls = []
        for tx in transactions:
            calls.append((tx['to'], tx['data']))
        
        return multicall.functions.aggregate(calls).call()
```

### Quoting Optimization (Extended)

```python
class QuoteOptimizer:
    def __init__(self):
        self.quote_cache = {}
        self.cache_ttl = 5  # seconds

    def get_best_quote(self, token_in, token_out, amount, dexes):
        quotes = []
        for dex in dexes:
            quote = self.get_quote(dex, token_in, token_out, amount)
            if quote:
                quotes.append(quote)
        
        if not quotes:
            raise NoQuoteAvailable()
        
        return max(quotes, key=lambda q: q.output_amount)

    def get_quote(self, dex, token_in, token_out, amount):
        cache_key = f"{dex.address}:{token_in}:{token_out}:{amount}"
        cached = self.quote_cache.get(cache_key)
        
        if cached and time.time() - cached['timestamp'] < self.cache_ttl:
            return cached['quote']
        
        quote = dex.get_quote(token_in, token_out, amount)
        self.quote_cache[cache_key] = {
            'quote': quote,
            'timestamp': time.time(),
        }
        
        return quote
```

---

## Security Considerations (Extended)

### Slippage Protection (Extended)

```python
class SlippageProtector:
    def __init__(self):
        self.default_slippage = 0.005  # 0.5%
        self.max_slippage = 0.05  # 5%

    def calculate_min_output(self, expected_output, slippage=None):
        if slippage is None:
            slippage = self.default_slippage
        
        min_output = expected_output * (1 - slippage)
        return int(min_output)

    def check_price_impact(self, input_amount, output_amount, reserve_in, reserve_out):
        mid_price = reserve_out / reserve_in
        execution_price = output_amount / input_amount
        price_impact = abs(execution_price - mid_price) / mid_price
        
        if price_impact > 0.05:
            raise PriceImpactTooHigh(f"Price impact: {price_impact:.2%}")
        
        return price_impact
```

### Reentrancy Protection (Extended)

```python
class ReentrancyGuard:
    def __init__(self):
        self.locked = False

    def __enter__(self):
        if self.locked:
            raise ReentrancyDetected()
        self.locked = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.locked = False
        return False

# Usage
guard = ReentrancyGuard()
with guard:
    # Execute transaction
    pass
```

### Oracle Manipulation Prevention (Extended)

```python
class TWAPOracle:
    def __init__(self):
        self.price_accumulator = 0
        self.last_block = 0
        self.period = 10  # blocks

    def update(self, price):
        if self.last_block == 0:
            self.price_accumulator = price
        else:
            blocks_elapsed = self.w3.eth.block_number - self.last_block
            self.price_accumulator += price * blocks_elapsed
        self.last_block = self.w3.eth.block_number

    def get_price(self):
        blocks_elapsed = self.w3.eth.block_number - self.last_block
        if blocks_elapsed == 0:
            return self.price_accumulator / self.period
        return self.price_accumulator / (self.period + blocks_elapsed)

    def is_manipulated(self, current_price, threshold=0.1):
        twap = self.get_price()
        deviation = abs(current_price - twap) / twap
        return deviation > threshold
```

### Flash Loan Attack Prevention

```python
class FlashLoanProtector:
    def __init__(self):
        self.same_block_threshold = 1

    def check_flash_loan_attack(self, tx_block, prev_block, actions):
        if tx_block - prev_block < self.same_block_threshold:
            if self.suspicious_actions(actions):
                raise FlashLoanAttackDetected()

    def suspicious_actions(self, actions):
        # Check for flash loan patterns
        return (
            len(actions) >= 3 and
            actions[0]['type'] == 'borrow' and
            actions[-1]['type'] == 'repay'
        )
```

---

## Troubleshooting Guide (Extended)

### Common Issues (Extended)

| Symptom | Cause | Solution |
|---------|-------|----------|
| Slippage error | Price moved too much | Increase slippage tolerance |
| Transaction reverted | Insufficient gas | Increase gas limit |
| Liquidation failed | Position not liquidatable | Check health factor |
| Low yield | High gas costs | Batch operations |
| Oracle stale | Oracle not updated | Use TWAP oracle |
| Sandwich attack | MEV extraction | Use private mempool |

### Debug Mode (Extended)

```python
class DeFiDebugger:
    def debug_swap(self, token_in, token_out, amount):
        print(f"Swap: {amount} {token_in} -> {token_out}")
        
        # Check reserves
        reserve_in = self.pool.get_reserve(token_in)
        reserve_out = self.pool.get_reserve(token_out)
        print(f"Reserves: {reserve_in} {token_in}, {reserve_out} {token_out}")
        
        # Calculate output
        expected_output = self.calculate_output(amount, reserve_in, reserve_out)
        print(f"Expected output: {expected_output}")
        
        # Check price impact
        price_impact = self.calculate_price_impact(amount, reserve_in, reserve_out)
        print(f"Price impact: {price_impact:.2%}")
        
        # Check gas
        gas_estimate = self.estimate_gas(token_in, token_out, amount)
        print(f"Gas estimate: {gas_estimate}")
```

---

## API Reference (Extended)

### AMMCalculator (Extended)

```python
class AMMCalculator:
    def calculate_swap(amount_in, input_token) -> SwapResult
    def calculate_lp_tokens(amount_a, amount_b) -> float
    def calculate_price_impact(amount_in, input_token) -> float
    def get_pool_state() -> PoolState
    def calculate_impermanent_loss(price_change) -> float
    def get_optimal_range(tick_lower, tick_upper) -> RangeResult
```

### LendingModel (Extended)

```python
class LendingModel:
    def health_factor() -> float
    def liquidation_price() -> float
    def borrow_apr() -> float
    def supply_apr() -> float
    def calculate_liquidation_profit(debt, collateral) -> float
    def get_utilization_rate() -> float
    def get_available_liquidity() -> float
```

---

## Data Models (Extended)

### SwapResult (Extended)

```python
@dataclass
class SwapResult:
    output_amount: float
    price_impact: float
    fee: float
    route: List[str]
    gas_estimate: int
    min_output: float
    execution_price: float
    mid_price: float
```

### PoolState (Extended)

```python
@dataclass
class PoolState:
    reserve_a: float
    reserve_b: float
    total_supply: float
    fee: float
    k: float
    price: float
    tvl: float
    volume_24h: float
    apr: float
```

### LiquidationResult

```python
@dataclass
class LiquidationResult:
    success: bool
    collateral_seized: float
    debt_repaid: float
    profit: float
    gas_used: int
    tx_hash: str
```

---

## Deployment Guide (Extended)

### Smart Contract Deployment (Extended)

```bash
# Deploy AMM Pool
forge create --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  src/AMMPool.sol:AMMPool \
  --constructor-args $TOKEN_A $TOKEN_B 30

# Deploy with verification
forge verify-contract $CONTRACT_ADDRESS src/AMMPool.sol:AMMPool \
  --chain-id 1 \
  --etherscan-api-key $ETHERSCAN_KEY
```

### Multi-Chain Deployment

```python
class MultiChainDeployer:
    def __init__(self):
        self.chains = {
            1: {"name": "Ethereum", "rpc": "https://eth-mainnet.alchemyapi.io/v2/..."},
            137: {"name": "Polygon", "rpc": "https://polygon-rpc.com"},
            42161: {"name": "Arbitrum", "rpc": "https://arb1.arbitrum.io/rpc"},
        }

    def deploy_to_all(self, contract, constructor_args):
        results = {}
        for chain_id, config in self.chains.items():
            results[chain_id] = self.deploy(contract, constructor_args, config)
        return results
```

---

## Monitoring & Observability (Extended)

### Key Metrics (Extended)

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `amm.tvl` | Total value locked | < $1M |
| `amm.daily.volume` | Daily trading volume | Anomaly |
| `lending.utilization.rate` | Borrow utilization | > 90% |
| `liquidation.count` | Liquidation events | Spike |
| `oracle.price.deviation` | Price deviation | > 5% |
| `gas.price.gwei` | Gas price | > 100 gwei |

### Dashboard

```python
class DeFiDashboard:
    def get_metrics(self):
        return {
            'tvl': self.get_total_tvl(),
            'volume_24h': self.get_24h_volume(),
            'active_users': self.get_active_users(),
            'liquidations_24h': self.get_24h_liquidations(),
            'oracle_status': self.get_oracle_status(),
        }
```

---

## Testing Strategy (Extended)

### Smart Contract Tests (Extended)

```python
def test_swap():
    pool = AMMPool(token_a, token_b, fee=0.003)
    pool.add_liquidity(1000, 1000000)
    output = pool.swap("A", 10)
    assert output > 0
    assert pool.reserve_a == 1010

def test_liquidation():
    bot = LiquidationBot()
    profit = bot.calculate_liquidation_profit(debt=1000, collateral=1200)
    assert profit > 0

def test_flash_loan():
    protocol = FlashLoanProtocol()
    result = protocol.flash_loan(token, 1000000, callback)
    assert result.success
```

---

## Versioning & Migration (Extended)

### Protocol Versioning (Extended)

Follow semantic versioning for smart contracts.

```python
class ProtocolVersioner:
    def __init__(self):
        self.versions = {}

    def deploy_version(self, version, contract):
        self.versions[version] = {
            'address': contract.address,
            'deployed_at': time.time(),
        }

    def get_latest(self):
        return max(self.versions.keys())
```

### Migration Scripts

```python
def migrate_v1_to_v2():
    """Migrate from v1 to v2 protocol."""
    # Read v1 state
    v1_pool = AMMPoolV1(PoolAddress)
    state = v1_pool.get_state()
    
    # Deploy v2
    v2_pool = deploy_v2(state['token_a'], state['token_b'])
    
    # Migrate liquidity
    v1_pool.remove_all_liquidity()
    v2_pool.add_liquidity(state['reserve_a'], state['reserve_b'])
```

---

## Glossary (Extended)

| Term | Definition |
|------|-----------|
| **AMM** | Automated Market Maker |
| **TVL** | Total Value Locked |
| **APR/APY** | Annual Percentage Rate/Year |
| **Liquidation** | Forced closure of undercollateralized position |
| **Flash Loan** | Uncollateralized loan repaid in same transaction |
| **Impermanent Loss** | Loss from providing liquidity vs holding |
| **TWAP** | Time-Weighted Average Price |
| **MEV** | Maximal Extractable Value |
| **Slippage** | Price difference between quote and execution |
| **LTV** | Loan-to-Value ratio |

---

## Changelog

### v2.0.0
- Added concentrated liquidity
- Flash loan support
- Multi-chain routing

### v1.0.0
- Initial release with basic AMM

---

## Contributing Guidelines

- Audit all smart contracts before deployment
- Test with mainnet forking
- Document economic assumptions

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
