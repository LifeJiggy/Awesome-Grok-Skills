# Crypto/Web3 Agent

A comprehensive blockchain and Web3 development platform with wallet management, smart contract deployment, DeFi protocol integration, NFT operations, IPFS storage, gas optimization, cross-chain bridges, DAO governance, token analysis, portfolio tracking, yield optimization, MEV protection, multi-signature wallets, and contract auditing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Wallet Management](#wallet-management)
  - [Smart Contracts](#smart-contracts)
  - [DeFi Operations](#defi-operations)
  - [NFT Management](#nft-management)
  - [IPFS Storage](#ipfs-storage)
  - [Gas Optimization](#gas-optimization)
  - [Cross-Chain Bridge](#cross-chain-bridge)
  - [DAO Governance](#dao-governance)
  - [Token Analysis](#token-analysis)
  - [Portfolio Tracking](#portfolio-tracking)
  - [Yield Optimization](#yield-optimization)
  - [MEV Protection](#mev-protection)
  - [Multi-Signature Wallet](#multi-signature-wallet)
  - [Contract Auditing](#contract-auditing)
- [API Reference](#api-reference)
- [Supported Chains](#supported-chains)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Crypto/Web3 Agent provides a unified interface for blockchain operations across multiple networks. It abstracts the complexity of interacting with different blockchains, protocols, and standards into a clean, Pythonic API.

Whether you're building DeFi applications, launching NFT collections, managing multi-chain portfolios, participating in DAO governance, optimizing yield strategies, protecting against MEV, or conducting security audits, this agent provides the tools and abstractions needed for efficient Web3 development.

## Features

### Core Capabilities
- **Multi-Chain Wallets**: Create and manage wallets on Ethereum, BSC, Polygon, Solana, Avalanche, Arbitrum, Optimism, and Base
- **Smart Contract Lifecycle**: Compile, deploy, verify, and interact with smart contracts
- **DeFi Integration**: Swap tokens, provide liquidity, stake, and farm yield
- **NFT Operations**: Mint, transfer, list, and trade NFTs with royalty support
- **Decentralized Storage**: Upload to IPFS, Arweave, and Pinata
- **Gas Optimization**: Real-time gas tracking, estimates, and timing recommendations
- **Cross-Chain Bridges**: Bridge tokens between supported networks
- **DAO Governance**: Create proposals, cast votes, and track governance

### Advanced Features
- **ABI Registry**: Automatic ABI management for contract interaction
- **Transaction History**: Complete ledger of all on-chain operations
- **Portfolio Tracking**: Multi-chain balance aggregation with snapshots
- **Price Impact Analysis**: DEX swap impact calculation
- **Impermanent Loss Calculator**: LP position risk assessment
- **Async Support**: Full asyncio wrapper for non-blocking operations
- **Token Analysis**: Token metrics, pricing, and market data
- **Yield Optimization**: Risk-based allocation and daily yield estimation
- **MEV Protection**: Flashbots and private mempool bundle submission
- **Multi-Signature Wallets**: N-of-M threshold signature wallets
- **Contract Auditing**: Audit workflow, findings tracking, and risk scoring

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       CryptoWeb3Agent                             │
│  ┌────────────┐ ┌──────────────┐ ┌────────────────────────────┐ │
│  │ Wallet Mgr │ │ Contract Mgr │ │ DeFi Manager               │ │
│  ├────────────┤ ├──────────────┤ ├────────────────────────────┤ │
│  │ NFT Mgr    │ │ Storage Mgr  │ │ Gas Optimizer              │ │
│  ├────────────┤ ├──────────────┤ ├────────────────────────────┤ │
│  │ Bridge Mgr │ │ DAO Manager  │ │ Multi-Chain Config         │ │
│  ├────────────┤ ├──────────────┤ ├────────────────────────────┤ │
│  │ Token      │ │ Portfolio    │ │ Yield Optimizer            │ │
│  │ Analyzer   │ │ Tracker      │ │                            │ │
│  ├────────────┤ ├──────────────┤ ├────────────────────────────┤ │
│  │ MEV        │ │ Multi-Sig    │ │ Contract Audit             │ │
│  │ Protector  │ │ Wallet       │ │ Helper                     │ │
│  └────────────┘ └──────────────┘ └────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.crypto_web3.agent import CryptoWeb3Agent, Config, Blockchain

# Initialize agent
agent = CryptoWeb3Agent(Config(default_chain=Blockchain.ETHEREUM))
agent.initialize()

# Create a wallet
wallet = agent.create_wallet(Blockchain.ETHEREUM, "My Wallet")
print(f"Address: {wallet['address']}")

# Get swap quote
quote = agent.get_swap_quote("ETH", "USDC", 1.0)
print(f"1 ETH = {quote['amount_out']:.2f} USDC")

# Deploy an ERC-20 token
token = agent.deploy_erc20("MyToken", "MTK", Blockchain.ETHEREUM, wallet["address"])
print(f"Token deployed at: {token['address']}")

# Get full report
report = agent.get_full_report()
agent.shutdown()
```

## Installation

### From Source
```bash
git clone https://github.com/your-org/crypto-web3-agent.git
cd crypto-web3-agent
pip install -r requirements.txt
```

### Dependencies
```
Python 3.10+
No external dependencies required (stdlib only)
```

## Usage

### Wallet Management

```python
from agents.crypto_web3.agent import CryptoWeb3Agent, Blockchain

agent = CryptoWeb3Agent()
agent.initialize()

# Create wallets on different chains
eth_wallet = agent.create_wallet(Blockchain.ETHEREUM, "ETH Wallet")
bsc_wallet = agent.create_wallet(Blockchain.BSC, "BSC Wallet")
polygon_wallet = agent.create_wallet(Blockchain.POLYGON, "Polygon Wallet")

# Import existing wallet
imported = agent._wallet_manager.import_wallet("0x1234...", Blockchain.ETHEREUM, "Imported")

# Check balances
balance = agent.get_wallet_balance(eth_wallet["address"])
# {'native_balance': 10.5, 'tokens': {'USDC': 1000, 'UNI': 50}}

# Transfer tokens
tx = agent.transfer(eth_wallet["address"], "0xRecipient...", 1.0, "ETH")
print(f"Tx: {tx['tx_hash'][:16]}... | Status: {tx['status']}")

# Batch transfers
txs = agent._wallet_manager.batch_transfer(
    eth_wallet["address"],
    [("0xAddr2...", 0.5, "ETH"), ("0xAddr3...", 100, "USDC")]
)

# Set token approvals
agent._wallet_manager.set_approval(
    eth_wallet["address"], "0xSpender...", "USDC", 1000.0
)

# Transaction history
history = agent.get_transaction_history(eth_wallet["address"], limit=20)
```

### Smart Contracts

```python
# Deploy ERC-20 token
token = agent.deploy_erc20(
    name="MyToken", symbol="MTK",
    chain=Blockchain.ETHEREUM, deployer=wallet["address"],
    total_supply=1000000
)
# {'address': '0x...', 'chain': 'ethereum', 'name': 'MyToken'}

# Deploy ERC-721 NFT collection
nft_collection = agent.deploy_erc721(
    name="ArtCollection", symbol="ART",
    chain=Blockchain.ETHEREUM, deployer=wallet["address"]
)

# Deploy custom contract
source_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
contract MyContract { ... }
"""
contract = agent.deploy_contract(source_code, "MyContract", Blockchain.ETHEREUM, wallet["address"])

# Verify contract
agent._contract_manager.verify_contract(contract["address"], source_code)

# Register and retrieve ABIs
agent._contract_manager.register_abi("MyProtocol", my_abi)
abi = agent._contract_manager.get_abi("MyProtocol")

# Get deployment history
history = agent._contract_manager.get_deployment_history()
```

### DeFi Operations

```python
# Get swap quote with price impact
quote = agent.get_swap_quote("ETH", "USDC", 1.0)
print(f"Amount Out: {quote['amount_out']:.2f} USDC")
print(f"Price Impact: {quote['price_impact']:.4f}%")
print(f"Gas Estimate: {quote['gas_estimate']}")

# Execute swap
tx = agent.execute_swap(wallet["address"], "ETH", "USDC", 1.0)

# Add liquidity to a pool
position = agent.add_liquidity(
    wallet["address"], "ETH", "USDC",
    amount_a=1.0, amount_b=1850.0
)
print(f"APR: {position['apr']:.1f}%")

# Remove liquidity
removed = agent._defi_manager.remove_liquidity(wallet["address"], "ETH", "USDC")

# Stake tokens
stake = agent.stake(wallet["address"], "0xValidator...", 32.0)
print(f"Staking APR: {stake['apr']:.1f}%")

# Calculate impermanent loss
il = agent._defi_manager.calculate_impermanent_loss(50.0)  # 50% price change
print(f"Impermanent Loss: {il:.4f}%")
```

### NFT Management

```python
# Mint NFT
nft = agent.mint_nft(
    contract_address=nft_collection["address"],
    chain=Blockchain.ETHEREUM,
    recipient=wallet["address"],
    name="Cool Art #1",
    image_url="ipfs://QmImage...",
    description="A beautiful piece of art",
    royalty=5.0
)
print(f"Minted NFT #{nft['token_id']}")

# List NFT for sale
agent.list_nft(
    nft_collection["address"], nft["token_id"],
    seller=wallet["address"], price=1.0
)

# Buy NFT
sale = agent.buy_nft(nft_collection["address"], nft["token_id"], buyer_address)

# Get collection
collection = agent._nft_manager.get_collection(nft_collection["address"])

# Get owner's NFTs
my_nfts = agent._nft_manager.get_owner_nfts(wallet["address"])

# Get sales history
sales = agent._nft_manager.get_sales_history()
```

### IPFS Storage

```python
# Upload file to IPFS
with open("image.png", "rb") as f:
    result = agent.store_on_ipfs(f.read(), "image.png")
print(f"IPFS CID: {result['cid']}")
print(f"Gateway: {result['gateway_url']}")

# Store NFT metadata
metadata = agent.store_nft_metadata(
    name="My NFT",
    description="NFT description",
    image_url="ipfs://QmImage...",
    attributes=[
        {"trait_type": "Color", "value": "Blue"},
        {"trait_type": "Rarity", "value": "Legendary"}
    ]
)
print(f"Metadata CID: {metadata['cid']}")

# Upload to Arweave (permanent storage)
arweave = agent._storage_manager.upload_to_arweave(b"important data", "document.pdf")

# Pin existing IPFS content
agent._storage_manager.pin_to_pinata("QmExistingCID", "pinned_file")

# Get storage stats
stats = agent._storage_manager.get_storage_stats()
```

### Gas Optimization

```python
# Get gas estimate for specific method
estimate = agent.get_gas_estimate(Blockchain.ETHEREUM, "swap")
print(f"Gas Limit: {estimate['gas_limit']}")
print(f"Gas Price: {estimate['gas_price_gwei']:.1f} gwei")
print(f"Cost: {estimate['estimated_cost']:.6f} ETH")

# Get pricing tiers (slow/standard/fast)
prices = agent.suggest_gas_price(Blockchain.ETHEREUM)
print(f"Slow: {prices['slow']:.1f} gwei")
print(f"Standard: {prices['standard']:.1f} gwei")
print(f"Fast: {prices['fast']:.1f} gwei")

# Estimate swap cost as percentage of trade
swap_cost = agent._gas_optimizer.estimate_swap_cost(Blockchain.ETHEREUM, 1000.0)
print(f"Gas cost: {swap_cost['cost_as_percent_of_trade']:.2f}% of trade")

# Get optimal timing recommendation
timing = agent._gas_optimizer.get_optimal_timing(Blockchain.ETHEREUM)
print(f"Recommendation: {timing['recommendation']} - {timing['reason']}")
```

### Cross-Chain Bridge

```python
# Register a bridge
from agents.crypto_web3.agent import BridgeConfig
agent._bridge_manager.register_bridge(BridgeConfig(
    source_chain=Blockchain.ETHEREUM,
    dest_chain=Blockchain.POLYGON,
    token_address="0x...",
    bridge_address="0x...",
    fee_percent=0.1,
    estimated_time_seconds=300
))

# Get available bridges
bridges = agent._bridge_manager.get_available_bridges(Blockchain.ETHEREUM, Blockchain.POLYGON)

# Estimate bridge cost
estimate = agent._bridge_manager.estimate_bridge(
    Blockchain.ETHEREUM, Blockchain.POLYGON, "ETH", 1.0
)
print(f"Amount Out: {estimate['amount_out']} | Fee: {estimate['fee']}")

# Execute bridge
result = agent.bridge_tokens(wallet["address"], Blockchain.ETHEREUM, Blockchain.POLYGON, "ETH", 1.0)
print(f"Bridge ID: {result['bridge_id']} | Status: {result['status']}")

# Check bridge history
history = agent._bridge_manager.get_bridge_history(wallet["address"])
```

### DAO Governance

```python
# Create proposal
proposal = agent.create_proposal(
    chain=Blockchain.ETHEREUM,
    governor="0xGovernor...",
    proposer=wallet["address"],
    title="Increase Staking Rewards",
    description="Proposal to increase staking APR from 4% to 6%"
)
print(f"Proposal #{proposal['proposal_id']}: {proposal['status']}")

# Cast votes
agent.cast_vote(proposal["proposal_id"], voter1, "for", weight=100.0)
agent.cast_vote(proposal["proposal_id"], voter2, "against", weight=50.0)
agent.cast_vote(proposal["proposal_id"], voter3, "abstain", weight=25.0)

# Get results
results = agent.get_proposal_results(proposal["proposal_id"])
print(f"For: {results['votes_for']} | Against: {results['votes_against']}")
print(f"Total Voters: {results['voter_count']}")

# Execute proposal
agent._dao_manager.execute_proposal(proposal["proposal_id"])

# Get active proposals
active = agent._dao_manager.get_active_proposals(Blockchain.ETHEREUM)
```

### Token Analysis

```python
from agents.crypto_web3.agent import TokenAnalyzer, TokenInfo, Blockchain

analyzer = TokenAnalyzer()

# Register tokens for tracking
analyzer.register_token(TokenInfo(
    address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    name="USD Coin", symbol="USDC", decimals=6,
    chain=Blockchain.ETHEREUM, total_supply=1e12, verified=True,
))

# Set and query prices
analyzer.set_price("USDC", 1.0)
analyzer.set_price("ETH", 3500.0)
price = analyzer.get_price("ETH")

# Analyze token
analysis = analyzer.analyze_token("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", Blockchain.ETHEREUM)
print(f"Market Cap: ${analysis['market_cap']:,.0f}")

# Get tokens by chain
eth_tokens = analyzer.get_tokens_by_chain(Blockchain.ETHEREUM)

# Calculate portfolio metrics
metrics = analyzer.calculate_token_metrics("ETH", 10.0)
print(f"Holdings Value: ${metrics['value_usd']:,.2f}")
```

### Portfolio Tracking

```python
from agents.crypto_web3.agent import PortfolioTracker

tracker = PortfolioTracker(agent._wallet_manager)

# Take snapshot with current prices
snapshot = tracker.take_snapshot({"ETH": 3500, "USDC": 1.0, "BTC": 65000})
print(f"Portfolio value: ${snapshot.total_value_usd:,.2f}")
print(f"Chain breakdown: {snapshot.chain_values}")

# Get value change over time
change = tracker.get_value_change(hours=24)
print(f"24h change: ${change['change_usd']:,.2f} ({change['change_percent']:.1f}%)")

# Get allocation breakdown
allocation = tracker.get_allocation_breakdown()
for symbol, data in allocation["allocations"].items():
    print(f"  {symbol}: ${data['value_usd']:,.2f} ({data['percent']:.1f}%)")
```

### Yield Optimization

```python
from agents.crypto_web3.agent import YieldOptimizer, YieldStrategy, DeFiProtocol, RiskLevel

optimizer = YieldOptimizer()

# Add yield positions
optimizer.add_position(user, YieldStrategy.STAKING, DeFiProtocol.LIDO,
                       Blockchain.ETHEREUM, "ETH", 32.0, 4.5)
optimizer.add_position(user, YieldStrategy.LENDING, DeFiProtocol.AAVE,
                       Blockchain.ETHEREUM, "USDC", 10000.0, 8.2)
optimizer.add_position(user, YieldStrategy.YIELD_FARMING, DeFiProtocol.UNISWAP,
                       Blockchain.ETHEREUM, "LP", 5000.0, 25.0)

# Calculate optimal allocation by risk tolerance
optimal = optimizer.calculate_optimal_allocation(user, RiskLevel.MEDIUM)
print(f"Weighted APY: {optimal['total_apy']:.1f}%")

# Estimate daily yield
daily = optimizer.estimate_daily_yield(user)
print(f"Daily yield: {daily['total_daily_yield']:.4f} tokens")
for token, amount in daily["by_token"].items():
    print(f"  {token}: {amount:.6f}")
```

### MEV Protection

```python
from agents.crypto_web3.agent import MEVProtector, MEVProtectionMode

protector = MEVProtector()

# Create protected bundle
bundle = protector.create_bundle(
    Blockchain.ETHEREUM,
    [{"to": "0xRouter...", "value": 0, "data": "0x..."}],
    target_block=current_block + 1,
    mode=MEVProtectionMode.FLASHBOTS,
)
print(f"Bundle ID: {bundle.bundle_id}")

# Submit bundle
result = protector.submit_bundle(bundle.bundle_id)
print(f"Submitted: {result['status']}")

# Estimate MEV savings
savings = protector.estimate_mev_savings(50000.0)
print(f"Protected savings: ${savings['savings_usd']:.2f}")
print(f"Savings percent: {savings['savings_percent']:.1f}%")

# Get pending bundles
pending = protector.get_pending_bundles(Blockchain.ETHEREUM)
```

### Multi-Signature Wallet

```python
from agents.crypto_web3.agent import MultiSigWallet

multisig = MultiSigWallet()

# Create 2-of-3 multisig
config = multisig.create_multisig(
    Blockchain.ETHEREUM,
    owners=[owner1, owner2, owner3],
    required_signatures=2,
    name="Treasury",
)
print(f"Multisig address: {config['address']}")

# Submit transaction
tx = multisig.submit_transaction(config["id"], owner1, destination, 5.0)
print(f"Tx ID: {tx.tx_id}")

# Confirm transaction
result = multisig.confirm_transaction(config["id"], tx.tx_id, owner2)
print(f"Confirmations: {result['confirmations']}/{result['required']}")
print(f"Sufficient: {result['sufficient']}")

# Get pending transactions
pending = multisig.get_pending_transactions(config["id"])
```

### Contract Auditing

```python
from agents.crypto_web3.agent import ContractAuditHelper, AuditStatus

auditor = ContractAuditHelper()

# Start audit
report = auditor.start_audit(contract_address, Blockchain.ETHEREUM, "SecurityInc")
print(f"Audit started: {report.status.name}")

# Add findings
auditor.add_finding(contract_address, Blockchain.ETHEREUM, "critical", "Reentrancy in withdraw()")
auditor.add_finding(contract_address, Blockchain.ETHEREUM, "high", "Unchecked low-level call")
auditor.add_finding(contract_address, Blockchain.ETHEREUM, "medium", "Centralized owner")
auditor.add_finding(contract_address, Blockchain.ETHEREUM, "low", "Missing event emission")

# Complete audit
completed = auditor.complete_audit(contract_address, Blockchain.ETHEREUM, AuditStatus.FINDINGS)
print(f"Status: {completed.status.name} | Findings: {completed.findings_count}")

# Get risk summary
risk = auditor.get_risk_summary(contract_address, Blockchain.ETHEREUM)
print(f"Risk score: {risk['risk_score']}")
print(f"Critical: {risk['critical']} | High: {risk['high']} | Medium: {risk['medium']}")
```

## API Reference

### CryptoWeb3Agent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `initialize()` | - | Dict | Start the agent |
| `shutdown()` | - | Dict | Stop the agent |
| `create_wallet()` | chain, name | Dict | Create a new wallet |
| `get_wallet_balance()` | address | Dict | Get wallet balances |
| `transfer()` | from, to, amount, token, chain | Dict | Transfer tokens |
| `deploy_contract()` | source, name, chain, deployer, type | Dict | Deploy contract |
| `deploy_erc20()` | name, symbol, chain, deployer, supply | Dict | Deploy ERC-20 |
| `deploy_erc721()` | name, symbol, chain, deployer | Dict | Deploy ERC-721 |
| `get_swap_quote()` | token_in, token_out, amount, chain | Dict | Get swap quote |
| `execute_swap()` | user, token_in, token_out, amount, chain | Dict | Execute swap |
| `add_liquidity()` | user, token_a, token_b, amount_a, amount_b | Dict | Add liquidity |
| `stake()` | user, validator, amount, chain | Dict | Stake tokens |
| `mint_nft()` | contract, chain, recipient, name, image | Dict | Mint NFT |
| `list_nft()` | contract, token_id, seller, price, chain | Dict | List NFT |
| `buy_nft()` | contract, token_id, buyer, chain | Dict | Buy NFT |
| `store_on_ipfs()` | data, name | Dict | Upload to IPFS |
| `store_nft_metadata()` | name, desc, image, attributes | Dict | Store metadata |
| `get_gas_estimate()` | chain, method | Dict | Estimate gas |
| `suggest_gas_price()` | chain | Dict | Get gas prices |
| `bridge_tokens()` | user, source, dest, token, amount | Dict | Bridge tokens |
| `create_proposal()` | chain, governor, proposer, title | Dict | Create proposal |
| `cast_vote()` | proposal_id, voter, support, weight | Dict | Cast vote |
| `get_proposal_results()` | proposal_id | Dict | Get results |
| `get_status()` | - | Dict | Agent status |
| `get_full_report()` | - | Dict | Full report |

## Supported Chains

| Chain | Chain ID | Native Currency | Block Time | Explorer |
|-------|----------|----------------|------------|----------|
| Ethereum | 1 | ETH | 12s | etherscan.io |
| BSC | 56 | BNB | 3s | bscscan.com |
| Polygon | 137 | MATIC | 2s | polygonscan.com |
| Solana | 0 | SOL | 0.4s | solscan.io |
| Avalanche | 43114 | AVAX | 2s | snowtrace.io |
| Arbitrum | 42161 | ETH | 0.25s | arbiscan.io |
| Optimism | 10 | ETH | 2s | optimistic.etherscan.io |
| Base | 8453 | ETH | 2s | basescan.org |

## Configuration

```yaml
agent:
  default_chain: ethereum
  network_type: mainnet
  gas_limit_buffer: 1.2
  slippage_tolerance: 0.5
  ipfs_gateway: "https://ipfs.io"
```

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_chain` | Blockchain | ETHEREUM | Default chain for operations |
| `network_type` | NetworkType | MAINNET | Network selection |
| `gas_limit_buffer` | float | 1.2 | Gas limit multiplier (20% buffer) |
| `slippage_tolerance` | float | 0.5 | Default slippage tolerance (%) |
| `ipfs_gateway` | str | "https://ipfs.io" | IPFS gateway URL |
| `pinata_api_key` | str | "" | Pinata API key for pinning |

## Best Practices

### Security
1. Never store private keys in code or logs
2. Validate all addresses before transactions
3. Use appropriate slippage tolerance
4. Verify contract addresses on block explorers
5. Test on testnets before mainnet deployment
6. Use MEV protection for large-value transactions
7. Implement multi-sig for treasury operations

### Gas Optimization
1. Batch operations when possible
2. Use Layer 2 for high-frequency operations
3. Monitor gas prices and set alerts
4. Optimize contract storage patterns
5. Use calldata instead of memory for read-only inputs
6. Time non-urgent transactions for low-gas periods

### DeFi Safety
1. Check price impact before large swaps
2. Understand impermanent loss risks
3. Diversify across protocols
4. Monitor APR changes regularly
5. Use stop-loss strategies
6. Prefer audited protocols with proven track records
7. Start with testnet before deploying capital

### NFT Best Practices
1. Store metadata on IPFS before minting
2. Set reasonable royalty percentages (2.5-10%)
3. Verify collection authenticity
4. Track sales for portfolio analytics
5. Consider gas costs for batch operations
6. Use permanent storage for critical metadata

### Yield Strategy
1. Match strategy to risk tolerance
2. Diversify across protocols and chains
3. Monitor APY changes daily
4. Account for gas costs in yield calculations
5. Consider lock periods before committing capital
6. Use auto-compounding for hands-off management

## Troubleshooting

### Common Issues

**Transaction stuck pending**
- Check gas price against network conditions
- Increase gas price by 20-30% and resubmit
- Use nonce management for replacements

**Swap failed**
- Increase slippage tolerance
- Reduce swap amount
- Check pool liquidity

**IPFS upload failed**
- Verify file size under limits
- Check API key validity
- Try alternative gateway

**NFT mint reverted**
- Verify contract is active
- Check mint limits and price
- Ensure sufficient balance

**Bridge delayed**
- Check status on explorer
- Verify minimum amounts
- Contact support if needed

**MEV bundle not included**
- Check target block is in the future
- Verify bundle format
- Ensure relay accessibility

**Multisig stuck**
- Verify all required signers confirmed
- Check signer is an owner
- Ensure sufficient execution gas

**Audit false positive**
- Review finding context
- Provide additional analysis
- Document as informational

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### Development Setup
```bash
pip install -r requirements-dev.txt
python -m pytest tests/
python -m mypy agents/
```

## Error Handling

The agent provides a comprehensive exception hierarchy for error handling:

```python
from agents.crypto_web3.agent import (
    Web3AgentError, WalletError, TransactionError,
    ContractError, InsufficientFundsError, NetworkError,
    IPFSError, DeFiError, BridgeError,
    MEVProtectionError, MultiSigError, AuditError,
)

try:
    tx = agent.transfer(from_addr, to_addr, amount)
except InsufficientFundsError as e:
    print(f"Not enough funds: {e}")
except WalletError as e:
    print(f"Wallet issue: {e}")
except TransactionError as e:
    print(f"Transaction failed: {e}")
except Web3AgentError as e:
    print(f"General error: {e}")
```

### Exception Hierarchy

```
Web3AgentError (base)
├── WalletError - Wallet not found, invalid address
├── TransactionError - Nonce conflict, revert
├── ContractError - ABI mismatch, not verified
├── InsufficientFundsError - Balance too low
├── NetworkError - RPC timeout, rate limit
├── IPFSError - Upload/pin failure
├── DeFiError - Slippage, pool issues
├── BridgeError - No route, fee issues
├── MEVProtectionError - Bundle rejected
├── MultiSigError - Threshold not met
└── AuditError - Invalid audit data
```

## Performance

### Operation Latency

| Operation | Target | Typical |
|-----------|--------|---------|
| Wallet creation | < 10ms | ~2ms |
| Balance query | < 50ms | ~15ms |
| Transaction submit | < 100ms | ~30ms |
| Swap quote | < 200ms | ~50ms |
| NFT mint | < 500ms | ~200ms |
| IPFS upload | < 2s | ~1s |
| Gas estimate | < 100ms | ~25ms |
| Portfolio snapshot | < 200ms | ~40ms |
| Yield optimization | < 300ms | ~60ms |

### Memory Usage

| Component | Per-Item | 100 Items |
|-----------|----------|-----------|
| WalletManager | ~200 bytes | ~20KB |
| ContractManager | ~1KB | ~100KB |
| DeFiManager | ~300 bytes | ~30KB |
| NFTManager | ~400 bytes | ~40KB |
| PortfolioTracker | ~500 bytes | ~50KB |

## Changelog

### v3.0.0
- Added TokenAnalyzer for token metrics and pricing
- Added PortfolioTracker with snapshot history
- Added YieldOptimizer with risk-based allocation
- Added MEVProtector for Flashbots/private mempool
- Added MultiSigWallet for threshold signatures
- Added ContractAuditHelper for security audits
- Expanded GasOptimizer with swap cost estimation
- Added batch transfer support to WalletManager
- Added token approval management
- Added chain-specific balance queries
- New enums: YieldStrategy, RiskLevel, AuditStatus, SignatureType, MEVProtectionMode
- New dataclasses: YieldPosition, AuditReport, MultiSigTransaction, MEVBundle, PortfolioSnapshot
- New exceptions: MEVProtectionError, MultiSigError, AuditError

### v2.0.0
- Added DeFi protocol integration
- Added NFT marketplace operations
- Added IPFS and Arweave storage
- Added cross-chain bridge support
- Added DAO governance
- Added gas optimization

### v1.0.0
- Initial release with wallet management
- Basic smart contract deployment
- Multi-chain support

## Examples

### Complete DeFi Workflow

```python
from agents.crypto_web3.agent import CryptoWeb3Agent, Config, Blockchain

agent = CryptoWeb3Agent(Config(default_chain=Blockchain.ETHEREUM))
agent.initialize()

# Setup
wallet = agent.create_wallet(Blockchain.ETHEREUM, "DeFi Wallet")
agent._wallet_manager.set_balance(wallet["address"], 10.0)

# Swap ETH for USDC
quote = agent.get_swap_quote("ETH", "USDC", 5.0)
print(f"Expected: {quote['amount_out']:.2f} USDC")

if quote["price_impact"] < 1.0:
    tx = agent.execute_swap(wallet["address"], "ETH", "USDC", 5.0)
    print(f"Swap executed: {tx['tx_hash'][:16]}...")

# Provide liquidity
pos = agent.add_liquidity(wallet["address"], "ETH", "USDC", 2.0, 3700.0)
print(f"LP APR: {pos['apr']:.1f}%")

# Stake
stake = agent.stake(wallet["address"], "0xLidoValidator...", 32.0)
print(f"Staking APR: {stake['apr']:.1f}%")

# Track portfolio
agent._portfolio_tracker.take_snapshot({"ETH": 3500, "USDC": 1.0})
report = agent.get_full_report()
```

### NFT Collection Launch

```python
agent = CryptoWeb3Agent(Config(default_chain=Blockchain.ETHEREUM))
agent.initialize()

deployer = agent.create_wallet(Blockchain.ETHEREUM, "NFT Deployer")
agent._wallet_manager.set_balance(deployer["address"], 50.0)

# Deploy collection
collection = agent.deploy_erc721("PixelPunks", "PP", Blockchain.ETHEREUM, deployer["address"])

# Store metadata and mint
for i in range(10):
    meta = agent.store_nft_metadata(
        f"Pixel Punk #{i}", f"Unique pixel art #{i}",
        "ipfs://QmImage...", [{"trait_type": "Rarity", "value": "Common"}]
    )
    nft = agent.mint_nft(
        collection["address"], Blockchain.ETHEREUM,
        deployer["address"], f"Pixel Punk #{i}",
        "ipfs://QmImage...", f"Description #{i}", 5.0
    )
    agent.list_nft(collection["address"], nft["token_id"], deployer["address"], 0.1)
    print(f"Minted and listed #{nft['token_id']}")
```

### Yield Farming Setup

```python
from agents.crypto_web3.agent import YieldOptimizer, YieldStrategy, DeFiProtocol, RiskLevel

agent = CryptoWeb3Agent()
agent.initialize()
wallet = agent.create_wallet(Blockchain.ETHEREUM, "Yield Farmer")

optimizer = YieldOptimizer()
user = wallet["address"]

# Diversify across strategies
optimizer.add_position(user, YieldStrategy.STAKING, DeFiProtocol.LIDO,
                       Blockchain.ETHEREUM, "ETH", 32.0, 4.5)
optimizer.add_position(user, YieldStrategy.LENDING, DeFiProtocol.AAVE,
                       Blockchain.ETHEREUM, "USDC", 10000.0, 8.2)
optimizer.add_position(user, YieldStrategy.YIELD_FARMING, DeFiProtocol.UNISWAP,
                       Blockchain.ETHEREUM, "LP", 5000.0, 25.0)

# Optimize
optimal = optimizer.calculate_optimal_allocation(user, RiskLevel.MEDIUM)
print(f"Optimal APY: {optimal['total_apy']:.1f}%")

daily = optimizer.estimate_daily_yield(user)
print(f"Daily yield: ${daily['total_daily_yield'] * 3500:.2f}")
```

## License

MIT License - see [LICENSE](LICENSE) for details.
