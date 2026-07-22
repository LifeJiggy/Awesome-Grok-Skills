---
name: "blockchain-finance"
category: "fintech"
version: "2.0.0"
tags: ["fintech", "blockchain", "defi", "tokenization", "smart-contracts", "web3"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["python", "blockchain-fundamentals", "cryptography"]
---

# Blockchain Finance

## Overview

Blockchain finance encompasses decentralized finance (DeFi), tokenized assets, smart contract-based financial instruments, and distributed ledger technology for institutional and retail financial services. This module provides tools for building on-chain financial products including token issuance, AMM (Automated Market Maker) operations, lending protocols, yield optimization, and institutional custody with regulatory compliance.

## Core Capabilities

- **Token Issuance**: ERC-20/721/1155 token deployment with compliance features (transfer restrictions, KYC-gated wallets, regulatory snapshots)
- **AMM Operations**: Liquidity pool creation, rebalancing strategies, impermanent loss calculation, and multi-hop swap routing
- **DeFi Lending**: Collateralized lending protocol management with liquidation monitoring, interest rate models, and utilization tracking
- **Yield Optimization**: Automated yield farming across protocols with risk-adjusted return calculations and gas optimization
- **Institutional Custody**: Multi-signature wallet management, HSM integration, cold/warm/hot wallet tiering with policy-based controls
- **Cross-Chain Bridge**: Multi-chain asset bridging with validation monitoring and liquidity tracking across L1/L2 networks
- **Smart Contract Audit Tools**: Automated vulnerability scanning, formal verification helpers, and gas optimization analysis
- **Regulatory Compliance**: On-chain KYC/AML integration, travel rule compliance, and audit trail for regulatory reporting

## Usage Examples

### Token Issuance

```python
from fintech.blockchain_finance import TokenIssuer, TokenType, ComplianceConfig

issuer = TokenIssuer(
    network="ethereum",
    compliance=ComplianceConfig(
        kyc_required=True,
        transfer_restricted=True,
        max_holders=10000,
        jurisdiction_allowlist=["US", "EU", "SG"],
    ),
)

# Issue a compliant security token
token = issuer.deploy(
    name="Real Estate Fund Token",
    symbol="REFT",
    total_supply=1_000_000,
    token_type=TokenType.ERC20,
    decimals=18,
    base_uri="https://api.reft.example.com/metadata/",
)

print(f"Token Address: {token.contract_address}")
print(f"Deployment Tx: {token.deployment_tx}")
print(f"Explorer: {token.explorer_url}")
```

### AMM Liquidity Management

```python
from fintech.blockchain_finance import AMMManager, PoolConfig

amm = AMMManager(
    protocol="uniswap_v3",
    rpc_url="https://eth-mainnet.alchemyapi.io/v2/KEY",
)

# Create concentrated liquidity position
position = amm.create_position(
    token_a="USDC",
    token_b="WETH",
    fee_tier=0.003,
    price_range=(1800, 2500),
    amount_a=50000,
    amount_b=27.78,
)

print(f"Position ID: {position.position_id}")
print(f"Liquidity: {position.liquidity}")
print(f"Range: ${position.price_lower} - ${position.price_upper}")

# Calculate impermanent loss
il = amm.calculate_impermanent_loss(position)
print(f"Impermanent Loss: {il.percentage:.2%}")
print(f"IL USD Value: ${il.usd_value:.2f}")
```

### DeFi Lending

```python
from fintech.blockchain_finance import LendingProtocol

lending = LendingProtocol(
    protocol="aave_v3",
    risk_model="conservative",
)

# Supply collateral and borrow
supply_tx = lending.supply(
    asset="USDC",
    amount=100_000,
    wallet="0x1234...5678",
)

borrow_tx = lending.borrow(
    asset="WETH",
    amount=20,
    collateral_asset="USDC",
    collateral_amount=100_000,
)

print(f"Supply TX: {supply_tx.tx_hash}")
print(f"Borrow TX: {borrow_tx.tx_hash}")
print(f"Health Factor: {borrow_tx.health_factor:.2f}")
print(f"Liquidation Price: ${borrow_tx.liquidation_price:.2f}")
```

### Yield Optimization

```python
from fintech.blockchain_finance import YieldOptimizer

optimizer = YieldOptimizer(
    risk_tolerance="moderate",
    max_gas_price_gwei=50,
    rebalance_threshold_pct=0.5,
)

# Optimize yield across protocols
strategy = optimizer.optimize(
    capital=100_000,
    preferred_assets=["USDC", "DAI", "USDT"],
    exclude_protocols=[],
)

print(f"Optimal Allocation:")
for alloc in strategy.allocations:
    print(f"  {alloc.protocol}: {alloc.percentage:.1%} "
          f"({alloc.apy:.2%} APY, risk={alloc.risk_score:.2f})")
print(f"Expected APY: {strategy.expected_apy:.2%}")
print(f"Gas Cost Estimate: {strategy.estimated_gas_usd:.2f}")
```

## Architecture

```
User Interface
├── Web DApp
├── Institutional Portal
├── API Gateway
└── Mobile Wallet
         │
         ▼
┌─────────────────────┐
│  Smart Contracts     │──→ On-chain logic (Solidity/Vyper)
│  (EVM / Solana)      │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ DeFi   │ │ Token  │──→ ERC-20/721/1155
│ Protocols│ │ Mgmt │
└────┬───┘ └────┬───┘
     │          │
     ▼          ▼
┌─────────────────────┐
│  Oracle Layer        │──→ Price feeds, events
│  (Chainlink/Pyth)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Compliance Layer    │──→ KYC, AML, travel rule
│  (On-chain + Off)    │
└─────────────────────┘
```

## Best Practices

- Always use audited smart contracts; never deploy custom contracts without professional security audit
- Implement time-locks on admin functions to give users time to react to governance changes
- Use multi-signature wallets for protocol treasury management (minimum 3-of-5 signers)
- Monitor liquidation thresholds in real-time and implement automatic deleveraging triggers
- Account for gas costs in yield calculations; a 20% APY with $50 gas per rebalance may not be profitable
- Implement circuit breakers on smart contracts to pause operations during suspected exploits
- Use price oracle redundancy (Chainlink + Pyth + TWAP) to prevent single-source manipulation
- Maintain off-chain compliance records even for on-chain transactions for regulatory examination
- Test all smart contract interactions on testnets before mainnet deployment
- Monitor contract upgrade proposals and maintain ability to exit before governance changes take effect

## Related Modules

- `fintech/digital-banking` - Fiat on/off ramp integration
- `fintech/payment-systems` - Traditional payment rails for settlement
- `fintech/risk-engine` - Risk assessment for DeFi positions
- `fintech/compliance-automation` - Regulatory compliance for token offerings

## Advanced Configuration

### Network Configuration

```yaml
networks:
  ethereum:
    rpc_url: "${ETH_RPC_URL}"
    chain_id: 1
    gas_limit: 3000000
    gas_price_strategy: "eip1559"
    max_fee_per_gas_gwei: 100
    max_priority_fee_per_gas_gwei: 2
    
  polygon:
    rpc_url: "${MATIC_RPC_URL}"
    chain_id: 137
    gas_limit: 5000000
    gas_price_gwei: 30
    
  arbitrum:
    rpc_url: "${ARB_RPC_URL}"
    chain_id: 42161
    gas_limit: 10000000
    l1_data_fee_buffer_pct: 20
```

### Smart Contract Configuration

```yaml
smart_contracts:
  uniswap_v3:
    router: "0xE592427A0AEce92De3Edee1F18E0157C05861564"
    factory: "0x1F98431c8aD98523631AE4a59f267346ea31F984"
    quoter: "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
    
  aave_v3:
    pool: "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
    oracle: "0x54586bE62E3c3580375aE3723C145253060Ca0C2"
    lending_pool: "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
    
  chainlink:
    eth_usd: "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
    btc_usd: "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"
    link_usd: "0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c"
```

### Compliance Configuration

```yaml
compliance:
  kyc:
    provider: "chainalysis"
    required_for:
      - token_purchase
      - token_transfer
      - liquidity_provision
    jurisdiction_rules:
      US:
        accredited_investor_required: true
        max_holding_period_days: 365
      EU:
        mifid_ii_classification: true
        prospectus_required_above_eur: 8000000
      SG:
        mas_license_required: true
        
  aml:
    screening_lists:
      - ofac_sdn
      - eu_sanctions
      - un_sanctions
    transaction_monitoring:
      enabled: true
      threshold_usd: 10000
      velocity_check: true
      
  travel_rule:
    enabled: true
    protocol: "trisa"
    threshold_usd: 3000
    required_fields:
      - originator_name
      - originator_address
      - beneficiary_name
      - beneficiary_address
```

## Architecture Patterns

### Event-Driven DeFi Architecture

```python
class DeFiEventProcessor:
    def __init__(self, web3_client, event_store):
        self.web3 = web3_client
        self.event_store = event_store
        self.handlers = {}
    
    def register_handler(self, event_type: str, handler: Callable):
        self.handlers[event_type] = handler
    
    async def process_events(self, from_block: int, to_block: int):
        events = await self.get_events(from_block, to_block)
        
        for event in events:
            handler = self.handlers.get(event['event'])
            if handler:
                await handler(event)
            
            await self.event_store.store(event)
    
    async def get_events(self, from_block: int, to_block: int):
        # Fetch events from all registered contracts
        all_events = []
        for contract in self.contracts:
            events = contract.events.get_logs(
                fromBlock=from_block,
                toBlock=to_block
            )
            all_events.extend(events)
        return sorted(all_events, key=lambda x: x['blockNumber'])
```

### Multi-Chain Orchestration

```python
class MultiChainOrchestrator:
    def __init__(self):
        self.chains = {}
        self.bridge_providers = {}
    
    async def bridge_asset(
        self,
        asset: str,
        amount: Decimal,
        source_chain: str,
        target_chain: str,
        wallet_address: str,
    ) -> BridgeResult:
        # Find optimal bridge route
        route = await self.find_optimal_route(
            asset, amount, source_chain, target_chain
        )
        
        # Execute bridge transaction
        tx_hash = await self.bridge_providers[route.provider].bridge(
            asset=asset,
            amount=amount,
            source_chain=source_chain,
            target_chain=target_chain,
            recipient=wallet_address,
        )
        
        # Monitor bridge status
        status = await self.monitor_bridge_status(tx_hash)
        
        return BridgeResult(
            tx_hash=tx_hash,
            status=status,
            estimated_arrival=route.estimated_time,
            fees=route.fees,
        )
```

### Smart Contract Interaction Pattern

```python
class SmartContractClient:
    def __init__(self, web3, contract_address, abi):
        self.web3 = web3
        self.contract = web3.eth.contract(address=contract_address, abi=abi)
    
    async def execute_transaction(
        self,
        function_name: str,
        args: tuple,
        value: int = 0,
        gas_limit: int = None,
    ) -> TransactionReceipt:
        # Build transaction
        func = getattr(self.contract.functions, function_name)(*args)
        
        tx = func.build_transaction({
            'from': self.wallet_address,
            'value': value,
            'gas': gas_limit or await func.estimate_gas(),
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.wallet_address),
        })
        
        # Sign and send
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for confirmation
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return receipt
```

### Oracle Integration Pattern

```python
class OracleAggregator:
    def __init__(self):
        self.oracles = {
            'chainlink': ChainlinkOracle(),
            'pyth': PythOracle(),
            'uniswap_twap': UniswapTWAPOracle(),
        }
        self.weights = {
            'chainlink': 0.5,
            'pyth': 0.3,
            'uniswap_twap': 0.2,
        }
    
    async def get_price(self, asset: str) -> PriceData:
        prices = {}
        
        for name, oracle in self.oracles.items():
            try:
                price = await oracle.get_price(asset)
                prices[name] = price
            except Exception as e:
                logger.warning(f"Oracle {name} failed: {e}")
        
        if not prices:
            raise OracleFailureError("All oracles failed")
        
        # Weighted average
        weighted_price = sum(
            prices[name] * self.weights[name]
            for name in prices
        ) / sum(self.weights[name] for name in prices)
        
        # Check for manipulation
        max_deviation = max(
            abs(prices[name] - weighted_price) / weighted_price
            for name in prices
        )
        
        if max_deviation > 0.05:  # 5% deviation threshold
            raise PriceManipulationError(
                f"Price deviation {max_deviation:.2%} exceeds threshold"
            )
        
        return PriceData(
            price=weighted_price,
            sources=prices,
            timestamp=datetime.utcnow(),
        )
```

## Integration Guide

### Web3.py Integration

```python
from web3 import Web3
from eth_account import Account

class BlockchainClient:
    def __init__(self, rpc_url: str, private_key: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        self.wallet_address = self.account.address
    
    async def get_balance(self, token_address: str = None) -> Decimal:
        if token_address:
            # ERC-20 token balance
            contract = self.w3.eth.contract(
                address=token_address,
                abi=ERC20_ABI
            )
            balance = contract.functions.balanceOf(
                self.wallet_address
            ).call()
            decimals = contract.functions.decimals().call()
            return Decimal(balance) / Decimal(10 ** decimals)
        else:
            # Native token balance
            balance = self.w3.eth.get_balance(self.wallet_address)
            return Decimal(balance) / Decimal(10 ** 18)
    
    async def send_transaction(
        self,
        to_address: str,
        value: Decimal,
        data: bytes = b'',
    ) -> str:
        tx = {
            'from': self.wallet_address,
            'to': to_address,
            'value': self.w3.to_wei(value, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.wallet_address),
            'data': data,
        }
        
        signed_tx = self.w3.eth.account.sign_transaction(
            tx, self.account.key
        )
        
        tx_hash = self.w3.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        
        return tx_hash.hex()
```

### Ethers.js Integration

```python
from web3 import Web3
import json

class EthersClient:
    def __init__(self, provider_url: str):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
    
    async def deploy_contract(
        self,
        abi: list,
        bytecode: str,
        constructor_args: tuple,
    ) -> str:
        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        tx = contract.constructor(*constructor_args).build_transaction({
            'from': self.wallet_address,
            'gas': 5000000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.wallet_address),
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(
            tx, self.private_key
        )
        
        tx_hash = self.w3.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.contractAddress
```

### DeFi Protocol Integration

```python
class UniswapV3Client:
    def __init__(self, w3: Web3, router_address: str):
        self.w3 = w3
        self.router = w3.eth.contract(
            address=router_address,
            abi=UNISWAP_V3_ROUTER_ABI
        )
    
    async def swap_exact_input(
        self,
        token_in: str,
        token_out: str,
        amount_in: Decimal,
        slippage_pct: float = 0.5,
        deadline_minutes: int = 20,
    ) -> SwapResult:
        # Get quote
        amount_out = await self.get_quote(
            token_in, token_out, amount_in
        )
        
        # Apply slippage
        min_amount_out = amount_out * (1 - slippage_pct / 100)
        
        # Build swap transaction
        deadline = int(time.time()) + (deadline_minutes * 60)
        
        tx = self.router.functions.exactInputSingle({
            'tokenIn': token_in,
            'tokenOut': token_out,
            'fee': 3000,  # 0.3% fee tier
            'recipient': self.wallet_address,
            'deadline': deadline,
            'amountIn': int(amount_in * 10 ** 18),
            'amountOutMinimum': int(min_amount_out * 10 ** 18),
            'sqrtPriceLimitX96': 0,
        }).build_transaction({
            'from': self.wallet_address,
            'value': 0,
            'gas': 300000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.wallet_address),
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(
            tx, self.private_key
        )
        
        tx_hash = self.w3.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return SwapResult(
            tx_hash=tx_hash.hex(),
            amount_in=amount_in,
            amount_out=amount_out,
            gas_used=receipt.gasUsed,
            status='success' if receipt.status == 1 else 'failed',
        )
```

## Performance Optimization

### Gas Optimization

```python
class GasOptimizer:
    def __init__(self, w3: Web3):
        self.w3 = w3
        self.gas_history = []
    
    async def optimize_gas_price(self) -> GasPrice:
        # Get current gas price
        current_gas = self.w3.eth.gas_price
        
        # Get historical gas prices
        recent_blocks = await self.get_recent_blocks(10)
        gas_prices = [block.gasUsed for block in recent_blocks]
        
        # Calculate optimal gas price
        avg_gas = sum(gas_prices) / len(gas_prices)
        
        if current_gas > avg_gas * 1.5:
            # Gas is high, suggest waiting
            return GasPrice(
                max_fee_per_gas=current_gas * 0.8,
                max_priority_fee_per_gas=current_gas * 0.1,
                wait_recommendation=True,
                estimated_wait_minutes=10,
            )
        else:
            # Gas is reasonable
            return GasPrice(
                max_fee_per_gas=current_gas,
                max_priority_fee_per_gas=current_gas * 0.1,
                wait_recommendation=False,
                estimated_wait_minutes=1,
            )
```

### Transaction Batching

```python
class TransactionBatcher:
    def __init__(self, max_batch_size: int = 10):
        self.max_batch_size = max_batch_size
        self.pending_txs = []
    
    async def add_transaction(self, tx: Transaction):
        self.pending_txs.append(tx)
        
        if len(self.pending_txs) >= self.max_batch_size:
            await self.execute_batch()
    
    async def execute_batch(self):
        if not self.pending_txs:
            return
        
        # Group by function type
        grouped = self.group_by_function(self.pending_txs)
        
        for func_name, txs in grouped.items():
            if func_name == 'transfer':
                await self.execute_multicall(txs)
            else:
                for tx in txs:
                    await self.execute_single(tx)
        
        self.pending_txs = []
```

### Caching Strategy

```python
class BlockchainCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_price(self, asset: str) -> Optional[Decimal]:
        cache_key = f"price:{asset}"
        cached = await self.redis.get(cache_key)
        if cached:
            return Decimal(cached)
        return None
    
    async def set_price(self, asset: str, price: Decimal):
        cache_key = f"price:{asset}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            str(price)
        )
    
    async def invalidate_price(self, asset: str):
        cache_key = f"price:{asset}"
        await self.redis.delete(cache_key)
```

## Security Considerations

### Private Key Management

```python
from cryptography.fernet import Fernet
from eth_account import Account

class SecureKeyManager:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_private_key(self, private_key: str) -> str:
        """Encrypt private key for secure storage"""
        return self.fernet.encrypt(private_key.encode()).decode()
    
    def decrypt_private_key(self, encrypted_key: str) -> str:
        """Decrypt private key for use"""
        return self.fernet.decrypt(encrypted_key.encode()).decode()
    
    def sign_transaction(self, tx: dict, encrypted_key: str) -> str:
        """Sign transaction with encrypted key"""
        private_key = self.decrypt_private_key(encrypted_key)
        signed = Account.sign_transaction(tx, private_key)
        return signed.rawTransaction.hex()
```

### Smart Contract Security

```python
class SmartContractAuditor:
    def __init__(self):
        self.vulnerability_patterns = self.load_patterns()
    
    async def audit_contract(self, contract_code: str) -> AuditReport:
        findings = []
        
        # Check for common vulnerabilities
        for pattern in self.vulnerability_patterns:
            matches = re.findall(pattern.regex, contract_code)
            if matches:
                findings.append(Finding(
                    severity=pattern.severity,
                    title=pattern.title,
                    description=pattern.description,
                    line_numbers=[m.start() for m in matches],
                    recommendation=pattern.recommendation,
                ))
        
        # Check for reentrancy
        if self.check_reentrancy(contract_code):
            findings.append(Finding(
                severity="HIGH",
                title="Reentrancy Vulnerability",
                description="External calls before state changes",
                recommendation="Use checks-effects-interactions pattern",
            ))
        
        # Check for integer overflow
        if self.check_integer_overflow(contract_code):
            findings.append(Finding(
                severity="HIGH",
                title="Integer Overflow",
                description="Potential arithmetic overflow",
                recommendation="Use SafeMath library or Solidity 0.8+",
            ))
        
        return AuditReport(
            findings=findings,
            risk_score=self.calculate_risk_score(findings),
        )
```

### Access Control

```python
class AccessControlManager:
    def __init__(self):
        self.roles = {}
        self.permissions = {}
    
    def grant_role(self, address: str, role: str):
        if address not in self.roles:
            self.roles[address] = set()
        self.roles[address].add(role)
    
    def revoke_role(self, address: str, role: str):
        if address in self.roles:
            self.roles[address].discard(role)
    
    def check_permission(self, address: str, permission: str) -> bool:
        if address not in self.roles:
            return False
        
        for role in self.roles[address]:
            if permission in self.permissions.get(role, []):
                return True
        
        return False
```

## Troubleshooting Guide

### Common Issues

**Issue: Transaction stuck pending**
```python
async def accelerate_transaction(tx_hash: str, gas_multiplier: float = 1.5):
    # Get current transaction
    tx = w3.eth.get_transaction(tx_hash)
    
    # Build replacement transaction
    replacement_tx = {
        'from': tx['from'],
        'to': tx['to'],
        'value': tx['value'],
        'gas': tx['gas'],
        'gasPrice': int(tx['gasPrice'] * gas_multiplier),
        'nonce': tx['nonce'],
        'data': tx['data'],
    }
    
    # Send replacement transaction
    signed = w3.eth.account.sign_transaction(replacement_tx, private_key)
    new_tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    
    return new_tx_hash
```

**Issue: Slippage exceeded**
```python
async def handle_slippage_error(swap_params: SwapParams):
    # Increase slippage tolerance
    new_slippage = min(swap_params.slippage * 1.5, 5.0)
    
    # Retry swap with higher slippage
    return await execute_swap(
        **swap_params,
        slippage=new_slippage,
    )
```

**Issue: Gas estimation failed**
```python
async def estimate_gas_safely(tx: dict) -> int:
    try:
        estimated = w3.eth.estimate_gas(tx)
        # Add 20% buffer
        return int(estimated * 1.2)
    except Exception as e:
        # Fallback to default gas limit
        logger.warning(f"Gas estimation failed: {e}")
        return 500000
```

### Performance Diagnostics

```python
class BlockchainDiagnostics:
    async def analyze_transaction(self, tx_hash: str):
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        
        print(f"Transaction {tx_hash}:")
        print(f"  Status: {'Success' if receipt.status == 1 else 'Failed'}")
        print(f"  Gas Used: {receipt.gasUsed}")
        print(f"  Block: {receipt.blockNumber}")
        print(f"  Confirmations: {w3.eth.block_number - receipt.blockNumber}")
        
        # Analyze gas usage
        if receipt.gasUsed > 200000:
            print(f"  WARNING: High gas usage")
            print(f"  Consider optimizing contract calls")
```

## API Reference

### Blockchain API Endpoints

```python
# Token operations
POST /api/v1/tokens/deploy
GET /api/v1/tokens/{token_address}
POST /api/v1/tokens/{token_address}/transfer
GET /api/v1/tokens/{token_address}/holders

# DeFi operations
POST /api/v1/defi/swap
POST /api/v1/defi/add-liquidity
POST /api/v1/defi/remove-liquidity
GET /api/v1/defi/positions/{position_id}

# Lending operations
POST /api/v1/lending/supply
POST /api/v1/lending/borrow
POST /api/v1/lending/repay
GET /api/v1/lending/positions/{position_id}
```

### Request/Response Schemas

```python
# Token deployment request
class DeployTokenRequest:
    name: str
    symbol: str
    total_supply: int
    decimals: int = 18
    network: str = "ethereum"
    compliance_config: Optional[ComplianceConfig] = None

# Token deployment response
class DeployTokenResponse:
    contract_address: str
    deployment_tx: str
    explorer_url: str
    gas_used: int
```

## Data Models

### Token Model

```python
class Token:
    contract_address: str
    name: str
    symbol: str
    decimals: int
    total_supply: Decimal
    network: str
    token_type: TokenType
    deployment_tx: str
    deployed_at: datetime
    
    # Compliance
    is_compliant: bool
    kyc_required: bool
    transfer_restricted: bool
    jurisdiction_allowlist: List[str]
```

### DeFi Position Model

```python
class DeFiPosition:
    position_id: str
    protocol: str
    position_type: PositionType  # liquidity, lending, borrowing
    assets: List[PositionAsset]
    value_usd: Decimal
    apy: Decimal
    risk_score: float
    health_factor: Optional[float]
    liquidation_price: Optional[float]
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Smart Contract Deployment

```bash
# Compile contracts
npx hardhat compile

# Run tests
npx hardhat test

# Deploy to testnet
npx hardhat run scripts/deploy.js --network goerli

# Deploy to mainnet
npx hardhat run scripts/deploy.js --network mainnet

# Verify contract
npx hardhat verify --network mainnet CONTRACT_ADDRESS
```

### Infrastructure Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  blockchain-service:
    image: your-registry/blockchain-service:2.0.0
    ports:
      - "8443:8443"
    environment:
      - ETH_RPC_URL=${ETH_RPC_URL}
      - PRIVATE_KEY_ENCRYPTED=${PRIVATE_KEY_ENCRYPTED}
    volumes:
      - ./config:/app/config
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Transaction metrics
transaction_counter = Counter(
    'blockchain_transactions_total',
    'Total blockchain transactions',
    ['network', 'status', 'type']
)

transaction_duration = Histogram(
    'blockchain_transaction_duration_seconds',
    'Transaction processing duration',
    ['network'],
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0]
)

# DeFi metrics
defi_position_value = Gauge(
    'defi_position_value_usd',
    'DeFi position value in USD',
    ['protocol', 'position_type']
)

# Gas metrics
gas_price = Gauge(
    'blockchain_gas_price_gwei',
    'Current gas price',
    ['network']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Blockchain Finance",
    "panels": [
      {
        "title": "Transaction Throughput",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(blockchain_transactions_total[5m])",
            "legendFormat": "{{network}} - {{status}}"
          }
        ]
      },
      {
        "title": "Gas Price",
        "type": "graph",
        "targets": [
          {
            "expr": "blockchain_gas_price_gwei",
            "legendFormat": "{{network}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: blockchain_alerts
  rules:
  - alert: HighGasPrice
    expr: blockchain_gas_price_gwei > 100
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Gas price exceeds 100 gwei"
      
  - alert: TransactionFailed
    expr: rate(blockchain_transactions_total{status="failed"}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Transaction failure rate exceeds 10%"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestTokenOperations:
    def test_deploy_token(self, blockchain_client):
        token = blockchain_client.deploy_token(
            name="Test Token",
            symbol="TEST",
            total_supply=1000000,
            decimals=18,
        )
        assert token.contract_address is not None
        assert token.total_supply == Decimal("1000000")
    
    def test_transfer_token(self, blockchain_client, deployed_token):
        tx_hash = blockchain_client.transfer_token(
            token_address=deployed_token.contract_address,
            to_address="0x1234...5678",
            amount=Decimal("100"),
        )
        assert tx_hash is not None
        
        # Verify balance
        balance = blockchain_client.get_token_balance(
            deployed_token.contract_address,
            "0x1234...5678",
        )
        assert balance == Decimal("100")
```

### Integration Tests

```python
class TestDeFiIntegration:
    async def test_swap_tokens(self, defi_client):
        # Get initial balances
        initial_usdc = await defi_client.get_balance("USDC")
        initial_weth = await defi_client.get_balance("WETH")
        
        # Execute swap
        result = await defi_client.swap(
            token_in="USDC",
            token_out="WETH",
            amount_in=Decimal("1000"),
            slippage=0.5,
        )
        
        assert result.status == "success"
        
        # Verify balances changed
        final_usdc = await defi_client.get_balance("USDC")
        final_weth = await defi_client.get_balance("WETH")
        
        assert final_usdc < initial_usdc
        assert final_weth > initial_weth
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class BlockchainUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_price(self):
        self.client.get("/api/v1/prices/ETH")
    
    @task(1)
    def swap_tokens(self):
        self.client.post("/api/v1/defi/swap", json={
            "token_in": "USDC",
            "token_out": "WETH",
            "amount": "1000",
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/tokens", methods=["POST"])
@app.route("/api/v2/tokens", methods=["POST"])
async def deploy_token():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await deploy_token_v2()
    return await deploy_token_v1()
```

### Smart Contract Migration

```python
class ContractMigrator:
    def __init__(self, old_address: str, new_address: str):
        self.old_address = old_address
        self.new_address = new_address
    
    async def migrate_data(self):
        # Read data from old contract
        data = await self.read_from_old_contract()
        
        # Write data to new contract
        await self.write_to_new_contract(data)
        
        # Update references
        await self.update_references()
```

## Glossary

- **AMM**: Automated Market Maker - decentralized exchange using algorithmic pricing
- **APY**: Annual Percentage Yield - annualized return on DeFi positions
- **DeFi**: Decentralized Finance - financial services built on blockchain
- **ERC-20**: Ethereum token standard for fungible tokens
- **ERC-721**: Ethereum token standard for non-fungible tokens (NFTs)
- **Gas**: Fee paid for blockchain transactions
- **Health Factor**: Metric indicating risk of liquidation in lending protocols
- **Impermanent Loss**: Loss in value of liquidity provision vs holding
- **Liquidity Pool**: Pool of tokens used for decentralized trading
- **Slippage**: Difference between expected and actual trade price
- **Smart Contract**: Self-executing contract with terms directly written into code
- **TWAP**: Time-Weighted Average Price - average price over time period

## Changelog

### Version 2.0.0 (2026-07-01)
- Added multi-chain support (Ethereum, Polygon, Arbitrum)
- Implemented institutional custody
- Enhanced DeFi protocol integrations
- Added smart contract audit tools

### Version 1.5.0 (2026-01-15)
- Added yield optimization
- Implemented cross-chain bridging
- Enhanced oracle integration

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic token issuance
- AMM operations

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def deploy_token(
    name: str,
    symbol: str,
    total_supply: int,
    network: str,
) -> Token:
    """Deploy a new token contract.
    
    Args:
        name: Token name.
        symbol: Token symbol.
        total_supply: Total supply.
        network: Target network.
    
    Returns:
        Deployed token information.
    
    Raises:
        DeploymentError: If deployment fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Blockchain Finance Platform

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
