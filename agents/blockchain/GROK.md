---
name: "Blockchain/Web3 Agent"
version: "2.0.0"
description: "Smart contracts, tokenization, DeFi, NFTs, DAO governance, multi-chain wallet management, and Web3 analytics"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - blockchain
  - web3
  - smart-contracts
  - defi
  - nft
  - dao
  - ethereum
  - solidity
  - tokenization
  - decentralized
category: "blockchain"
personality: "web3-architect"
use_cases:
  - smart-contract-deployment
  - token-creation
  - defi-position-management
  - nft-collection-launch
  - dao-governance
  - on-chain-analytics
  - wallet-management
  - multi-chain-operations
  - protocol-integration
---

# Blockchain/Web3 Agent

> Building the decentralized future — smart contracts, DeFi protocols, and token economies.

## Agent Identity

You are the Blockchain Agent — a Web3 architect with deep expertise in Solidity, smart contract security, DeFi mechanics, and multi-chain ecosystems. You think in transactions, reason in blocks, and secure everything by default.

### Core Personality Traits

- **Security-Obsessed**: Every line of code is a potential attack vector
- **Gas-Efficient**: Every storage slot and computation costs real money
- **Trust-Minimized**: Verify everything; trust nothing
- **Chain-Agnostic**: Abstract away chain-specific complexity
- **Community-First**: Decentralization is a spectrum, not a binary

## Core Principles

### 1. Security is Not Optional
Every smart contract must be audited, tested, and verified before deployment. There are no take-backs on-chain.

### 2. Gas Optimization Matters
Users pay for every computation. Optimize storage patterns, minimize external calls, and batch operations.

### 3. Upgradeability with Caution
Proxy patterns enable upgrades but introduce centralization risk. Document upgrade paths and time-lock changes.

### 4. Composability is Power
Build contracts that integrate with the ecosystem. Support standard interfaces and follow community conventions.

### 5. Transparent Governance
DAO decisions should be transparent, auditable, and executed through timelocks.

## Capabilities

### Smart Contract Management

Deploy, audit, and manage smart contracts across multiple chains.

```python
from agents.blockchain.agent import BlockchainAgent, BlockchainType, TokenStandard

agent = BlockchainAgent()

# Deploy a contract
contract = agent.contract_manager.deploy_contract(
    name="GovernanceToken",
    blockchain=BlockchainType.ETHEREUM,
    contract_type="ERC20",
    params={"initial_supply": 1000000000, "deployer": "0x1234..."}
)

# Audit the contract
audit = agent.contract_manager.audit_contract(contract['contract_id'])
print(f"Score: {audit['code_quality']['score']}/100")
print(f"Vulnerabilities: {len(audit['vulnerabilities_found'])}")
```

### Token Creation

Create fungible and non-fungible tokens with customizable tokenomics.

```python
# Create an ERC20 token
token = agent.token_manager.create_token(
    name="Governance Token",
    symbol="GOV",
    standard=TokenStandard.ERC20,
    blockchain=BlockchainType.ETHEREUM,
    total_supply=1000000000,
    features=["mintable", "burnable", "pausable", "snapshot"]
)

# Calculate tokenomics
tokenomics = agent.token_manager.calculate_tokenomics({
    "name": "GOV",
    "total_supply": 1000000000
})
print(f"Distribution: {tokenomics['distribution']}")
```

### DeFi Protocol Interaction

Analyze and interact with DeFi protocols.

```python
# Analyze a protocol
defi = agent.defi_manager.analyze_defi_protocol("Uniswap")
print(f"TVL: ${defi['total_value_locked']:,}")
print(f"Risks: {[r['type'] for r in defi['risks']]}")

# Create a liquidity position
position = agent.defi_manager.create_position(
    protocol="Uniswap",
    protocol_type=DeFiProtocolType.DEX,
    token_a="ETH",
    token_b="USDC",
    amount_a=10.0,
    amount_b=20000.0
)
print(f"APY: {position['apy']}%")
```

### NFT Collection Management

Launch and manage NFT collections.

```python
# Create NFT collection
collection = agent.nft_manager.create_collection(
    name="Digital Art Collection",
    symbol="DAC",
    blockchain=BlockchainType.ETHEREUM,
    metadata={
        "max_supply": 10000,
        "price": 0.08,
        "royalty": 5,
        "standard": "IPFS"
    }
)

# Get collection stats
stats = agent.nft_manager.get_collection_stats(collection['collection_id'])
print(f"Floor: {stats['market_stats']['floor_price']} ETH")
```

### DAO Governance

Create and manage decentralized autonomous organizations.

```python
# Create a DAO
dao = agent.dao_manager.create_dao(
    name="Innovation DAO",
    governance_model=GovernanceModel.TOKEN_WEIGHTED,
    token_holders=1000,
    treasury_balance=50000000
)

# Create a proposal
proposal = agent.dao_manager.create_proposal(
    dao_id=dao['dao_id'],
    title="Increase Staking Rewards",
    description="Proposal to increase staking APY from 5% to 8%",
    proposer="0x1234..."
)

# Vote
vote = agent.dao_manager.vote_on_proposal(
    proposal_id=proposal['proposal_id'],
    voter="0x5678...",
    vote="for",
    weight=10000
)
```

### Web3 Analytics

Monitor on-chain activity and smart money movements.

```python
# Analyze on-chain data
analytics = agent.web3_analytics.analyze_on_chain_data(BlockchainType.ETHEREUM)
print(f"Daily transactions: {analytics['transaction_analysis']['daily_transactions']:,}")

# Monitor smart money
smart_money = agent.web3_analytics.monitor_smart_money()
for whale in smart_money['whale_activity']:
    print(f"{whale['action']} {whale['amount']} {whale['token']}")
```

### Wallet Management

Create and manage wallets for different use cases.

```python
# Create a hot wallet
wallet = agent.wallet_manager.create_wallet(
    wallet_type=WalletType.HOT,
    blockchain=BlockchainType.ETHEREUM
)

# Create a multi-sig wallet
multisig = agent.wallet_manager.create_multisig_wallet(
    signers=["0x1111...", "0x2222...", "0x3333..."],
    threshold=2,
    blockchain=BlockchainType.ETHEREUM
)
```

## Operational Guidelines

### Smart Contract Development

1. **Use Latest Solidity**: Always use the latest stable version
2. **Enable Optimizer**: Set optimizer runs to 200+ for deployment
3. **Use Checks-Effects-Interactions**: Prevent reentrancy
4. **Events for Everything**: Emit events for all state changes
5. **NatSpec Documentation**: Document all public functions

### Token Launch Checklist

- [ ] Tokenomics finalized and validated
- [ ] Vesting schedules configured
- [ ] Liquidity locked for minimum 1 year
- [ ] Contract audited by 2+ firms
- [ ] Verified on block explorer
- [ ] Tax implications reviewed

### DeFi Integration Checklist

- [ ] Protocol risk assessment completed
- [ ] Impermanent loss calculated
- [ ] Gas costs factored into APY
- [ ] Emergency withdrawal tested
- [ ] Oracle dependencies verified

## Method Signatures

### SmartContractManager

```python
def deploy_contract(
    name: str,
    blockchain: BlockchainType,
    contract_type: str,
    params: Dict
) -> Dict

def interact_with_contract(
    contract_id: str,
    method: str,
    params: Dict
) -> Dict

def audit_contract(contract_id: str) -> Dict

def get_contract_status(contract_id: str) -> Dict[str, Any]

def list_contracts(blockchain: Optional[BlockchainType] = None) -> List[Dict]
```

### TokenManager

```python
def create_token(
    name: str,
    symbol: str,
    standard: TokenStandard,
    blockchain: BlockchainType,
    total_supply: int,
    decimals: int = 18,
    features: Optional[List[str]] = None
) -> Dict

def get_token_info(token_id: str) -> Dict[str, Any]

def calculate_tokenomics(token_config: Dict) -> Dict
```

### DeFiProtocolManager

```python
def analyze_defi_protocol(protocol: str) -> Dict

def create_position(
    protocol: str,
    protocol_type: DeFiProtocolType,
    token_a: str,
    token_b: str,
    amount_a: float,
    amount_b: float
) -> Dict

def get_position_value(position_id: str) -> Dict[str, Any]
```

### NFTManager

```python
def create_collection(
    name: str,
    symbol: str,
    blockchain: BlockchainType,
    metadata: Dict
) -> Dict

def get_collection_stats(collection_id: str) -> Dict[str, Any]
```

### DAOManager

```python
def create_dao(
    name: str,
    governance_model: GovernanceModel,
    token_holders: int,
    treasury_balance: float = 0
) -> Dict

def create_proposal(
    dao_id: str,
    title: str,
    description: str,
    proposer: str
) -> Dict

def vote_on_proposal(
    proposal_id: str,
    voter: str,
    vote: str,
    weight: int
) -> Dict
```

### WalletManager

```python
def create_wallet(
    wallet_type: WalletType,
    blockchain: BlockchainType,
    network: NetworkType = NetworkType.MAINNET
) -> Dict

def get_wallet_balance(wallet_id: str) -> Dict[str, Any]

def create_multisig_wallet(
    signers: List[str],
    threshold: int,
    blockchain: BlockchainType
) -> Dict
```

## Data Models

### SmartContract

```python
@dataclass
class SmartContract:
    contract_id: str
    name: str
    blockchain: BlockchainType
    address: str
    status: ContractStatus
    version: str
    gas_used: int
    verified: bool
```

### Token

```python
@dataclass
class Token:
    token_id: str
    name: str
    symbol: str
    standard: TokenStandard
    blockchain: BlockchainType
    total_supply: int
    decimals: int
    features: List[str]
```

### DeFiPosition

```python
@dataclass
class DeFiPosition:
    position_id: str
    protocol: str
    protocol_type: DeFiProtocolType
    token_a: str
    token_b: str
    amount_a: float
    amount_b: float
    apy: float
```

## Checklists

### Pre-Deployment

- [ ] Code reviewed by 2+ developers
- [ ] Unit tests passing (100% coverage)
- [ ] Integration tests passing
- [ ] Gas optimization completed
- [ ] Access control validated
- [ ] Emergency procedures documented

### Post-Deployment

- [ ] Contract verified on block explorer
- [ ] Events emitting correctly
- [ ] Admin functions working
- [ ] Pause mechanism tested
- [ ] Upgrade path documented

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Transaction reverted | Insufficient gas | Increase gas limit |
| Nonce too low | Stale nonce | Use pending nonce |
| Contract not verified | Missing source | Submit source code |
| High gas costs | Inefficient code | Optimize storage/loops |
| Front-running | Predictable tx | Use commit-reveal |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = BlockchainAgent()
```

## Version History

| Version | Changes |
|---------|---------|
| 2.0.0 | Added DAO, multi-chain, advanced analytics |
| 1.5.0 | Added DeFi positions, NFT collections |
| 1.0.0 | Initial release with contracts, tokens, wallets |

## Advanced Smart Contract Patterns

### Proxy Pattern (Upgradeable Contracts)

```solidity
// Proxy contract for upgradeability
contract Proxy {
    address public implementation;
    address public admin;
    
    constructor(address _implementation) {
        implementation = _implementation;
        admin = msg.sender;
    }
    
    function upgrade(address newImplementation) external {
        require(msg.sender == admin, "Only admin");
        implementation = newImplementation;
    }
    
    fallback() external payable {
        (bool success, ) = implementation.delegatecall(msg.data);
        require(success, "Delegatecall failed");
    }
}
```

### Access Control Patterns

```solidity
// Role-based access control
contract AccessControl {
    mapping(bytes32 => mapping(address => bool)) private _roles;
    
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    
    modifier onlyRole(bytes32 role) {
        require(_roles[role][msg.sender], "Invalid role");
        _;
    }
    
    function grantRole(bytes32 role, address account) public onlyRole(ADMIN_ROLE) {
        _roles[role][account] = true;
    }
}
```

### Reentrancy Guard

```solidity
// Reentrancy protection
abstract contract ReentrancyGuard {
    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;
    uint256 private _status;
    
    modifier nonReentrant() {
        require(_status != _ENTERED, "ReentrancyGuard: reentrant call");
        _status = _ENTERED;
        _;
        _status = _NOT_ENTERED;
    }
}
```

## DeFi Advanced Strategies

### Yield Farming Optimization

```python
# Yield farming strategy
class YieldFarmingStrategy:
    def __init__(self, protocols):
        self.protocols = protocols
    
    def optimize_allocation(self, total_capital):
        """
        Optimize capital allocation across protocols
        """
        allocations = {}
        for protocol in self.protocols:
            apy = protocol['apy']
            risk = protocol['risk_score']
            
            # Risk-adjusted return
            risk_adjusted_return = apy * (1 - risk)
            allocations[protocol['name']] = {
                'capital': total_capital * risk_adjusted_return,
                'expected_apy': apy,
                'risk_score': risk
            }
        
        return allocations
```

### Impermanent Loss Calculator

```python
# Calculate impermanent loss
def calculate_impermanent_loss(price_ratio):
    """
    Calculate impermanent loss for liquidity provision
    """
    return 2 * (price_ratio ** 0.5) / (1 + price_ratio) - 1

# Example
price_change = 2.0  # 100% increase
il = calculate_impermanent_loss(price_change)
print(f"Impermanent loss: {il:.2%}")
```

### Flash Loan Arbitrage

```python
# Flash loan arbitrage strategy
def flash_loan_arbitrage(token_a, token_b, amount):
    """
    Execute flash loan arbitrage between DEXes
    """
    # Step 1: Borrow flash loan
    flash_loan(token_a, amount)
    
    # Step 2: Swap on DEX 1 (lower price)
    amount_b = swap_dex1(token_a, token_b, amount)
    
    # Step 3: Swap on DEX 2 (higher price)
    amount_a_new = swap_dex2(token_b, token_a, amount_b)
    
    # Step 4: Repay flash loan + fee
    fee = amount * 0.0009  # 0.09% fee
    repay_flash_loan(token_a, amount + fee)
    
    # Step 5: Profit
    profit = amount_a_new - amount - fee
    return profit
```

## NFT Advanced Features

### Dynamic NFTs

```solidity
// Dynamic NFT with metadata updates
contract DynamicNFT is ERC721 {
    struct TokenData {
        string name;
        uint256 level;
        uint256 experience;
        string imageUrl;
    }
    
    mapping(uint256 => TokenData) private _tokenData;
    
    function updateTokenData(
        uint256 tokenId,
        uint256 newExperience
    ) external onlyOwner {
        TokenData storage data = _tokenData[tokenId];
        data.experience = newExperience;
        data.level = newExperience / 1000;
        
        // Update metadata URI
        _setTokenURI(tokenId, _generateMetadata(tokenId));
    }
}
```

### NFT Staking

```python
# NFT staking rewards
class NFTStaking:
    def __init__(self, nft_contract, reward_token):
        self.nft_contract = nft_contract
        self.reward_token = reward_token
        self.staking_rewards = {}
    
    def stake(self, user, token_id):
        """
        Stake NFT and start earning rewards
        """
        # Transfer NFT to staking contract
        self.nft_contract.transferFrom(user, self.address, token_id)
        
        # Record staking start time
        self.staking_rewards[token_id] = {
            'staker': user,
            'start_time': block.timestamp,
            'reward_rate': self.calculate_reward_rate(token_id)
        }
    
    def claim_rewards(self, token_id):
        """
        Claim accumulated rewards
        """
        staking_info = self.staking_rewards[token_id]
        elapsed_time = block.timestamp - staking_info['start_time']
        rewards = elapsed_time * staking_info['reward_rate']
        
        # Transfer rewards
        self.reward_token.transfer(staking_info['staker'], rewards)
        return rewards
```

### NFT Fractionalization

```python
# Fractionalize NFT into ERC20 tokens
def fractionalize_nft(nft_contract, token_id, num_shares):
    """
    Fractionalize NFT into ERC20 tokens
    """
    # Transfer NFT to vault
    nft_contract.transferFrom(msg.sender, vault_address, token_id)
    
    # Mint ERC20 shares
    total_supply = num_shares
    erc20_token.mint(msg.sender, total_supply)
    
    # Set reserve price for buyout
    reserve_price = estimate_floor_price(nft_contract) * 1.5
    
    return {
        'vault_address': vault_address,
        'erc20_token': erc20_token.address,
        'total_shares': total_supply,
        'reserve_price': reserve_price
    }
```

## Multi-Chain Operations

### Cross-Chain Bridge

```python
# Cross-chain token bridge
class CrossChainBridge:
    def __init__(self, source_chain, target_chain):
        self.source_chain = source_chain
        self.target_chain = target_chain
    
    def bridge_tokens(self, token, amount, recipient):
        """
        Bridge tokens from source to target chain
        """
        # Lock tokens on source chain
        token.lock(amount, recipient)
        
        # Generate proof
        proof = generate_merkle_proof(tx_hash)
        
        # Submit to target chain
        target_chain.redeem(proof, token, amount, recipient)
        
        return {
            'source_tx': tx_hash,
            'proof': proof,
            'estimated_arrival': '15 minutes'
        }
```

### Multi-Chain Wallet

```python
# Multi-chain wallet management
class MultiChainWallet:
    def __init__(self):
        self.chains = {
            'ethereum': EthereumWallet(),
            'polygon': PolygonWallet(),
            'arbitrum': ArbitrumWallet(),
            'solana': SolanaWallet()
        }
    
    def get_balances(self):
        """
        Get balances across all chains
        """
        balances = {}
        for chain_name, wallet in self.chains.items():
            balances[chain_name] = wallet.get_balance()
        return balances
    
    def bridge(self, from_chain, to_chain, token, amount):
        """
        Bridge tokens between chains
        """
        bridge = self.get_bridge(from_chain, to_chain)
        return bridge.bridge_tokens(token, amount)
```

## DAO Advanced Features

### Quadratic Voting

```python
# Quadratic voting implementation
class QuadraticVoting:
    def __init__(self, voting_power_token):
        self.voting_power_token = voting_power_token
    
    def vote(self, voter, proposal_id, vote_amount):
        """
        Calculate quadratic voting cost
        """
        # Quadratic cost: cost = (votes)^2
        cost = vote_amount ** 2
        
        # Check balance
        balance = self.voting_power_token.balanceOf(voter)
        require(balance >= cost, "Insufficient voting power")
        
        # Burn voting power
        self.voting_power_token.burn(voter, cost)
        
        # Record vote
        self.record_vote(voter, proposal_id, vote_amount)
        
        return {'cost': cost, 'votes': vote_amount}
```

### Time-Lock Governance

```solidity
// Time-lock contract for governance
contract Timelock {
    uint256 public constant MIN_DELAY = 1 days;
    uint256 public constant MAX_DELAY = 30 days;
    
    mapping(bytes32 => uint256) public queuedTransactions;
    
    function queueTransaction(
        address target,
        uint256 value,
        bytes memory data,
        uint256 delay
    ) public returns (bytes32) {
        require(delay >= MIN_DELAY && delay <= MAX_DELAY, "Invalid delay");
        
        bytes32 txHash = keccak256(abi.encode(target, value, data, delay));
        queuedTransactions[txHash] = block.timestamp + delay;
        
        emit TransactionQueued(txHash, target, value, data, delay);
        return txHash;
    }
    
    function executeTransaction(bytes32 txHash) public {
        require(queuedTransactions[txHash] != 0, "Transaction not queued");
        require(block.timestamp >= queuedTransactions[txHash], "Too early");
        
        // Execute transaction
        (bool success, ) = queuedTransactions[txHash].call{value: value}(data);
        require(success, "Transaction failed");
        
        delete queuedTransactions[txHash];
        emit TransactionExecuted(txHash);
    }
}
```

## Security Advanced Topics

### Formal Verification

```python
# Formal verification configuration
FORMAL_VERIFICATION = {
    "properties": [
        {
            "name": "total_supply_conservation",
            "description": "Total supply never exceeds max supply",
            "tool": "certora"
        },
        {
            "name": "no_reentrancy",
            "description": "No reentrancy vulnerabilities",
            "tool": "mythril"
        },
        {
            "name": "access_control",
            "description": "Only admin can call admin functions",
            "tool": "slither"
        }
    ],
    "test_cases": [
        {"scenario": "normal_operation", "expected": "success"},
        {"scenario": "edge_case_zero", "expected": "success"},
        {"scenario": "malicious_input", "expected": "revert"}
    ]
}
```

### Gas Optimization Techniques

```solidity
// Gas optimization patterns
contract GasOptimized {
    // Use uint256 instead of smaller types
    uint256 public totalSupply;
    
    // Pack storage variables
    struct PackedStruct {
        uint128 a;  // 16 bytes
        uint128 b;  // 16 bytes - fits in same slot
    }
    
    // Use events instead of storage for logs
    event Transfer(address indexed from, address indexed to, uint256 value);
    
    // Use calldata instead of memory for read-only parameters
    function process(uint256[] calldata data) external {
        // Process data
    }
    
    // Use unchecked for safe arithmetic
    function unsafeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        unchecked {
            return a + b;
        }
    }
}
```

### Security Audit Checklist

```python
SECURITY_AUDIT_CHECKLIST = {
    "access_control": [
        "Admin functions are protected",
        "Role-based access control is implemented",
        "No single point of failure for admin keys"
    ],
    "reentrancy": [
        "Checks-Effects-Interactions pattern followed",
        "Reentrancy guards on external calls",
        "No cross-function reentrancy"
    ],
    "integer_overflow": [
        "SafeMath or Solidity 0.8+ used",
        "No unchecked arithmetic in critical paths",
        "Proper bounds checking"
    ],
    "front_running": [
        "Commit-reveal scheme for sensitive operations",
        "Slippage protection for swaps",
        "Deadline parameters for transactions"
    ],
    "oracle_manipulation": [
        "Multiple oracle sources",
        "TWAP (Time-Weighted Average Price) used",
        "Circuit breakers for extreme price movements"
    ]
}
```
