"""Crypto/Web3 Agent - Blockchain and Web3 Development Platform.

Comprehensive framework for blockchain operations, smart contract management,
wallet integration, DeFi protocol interaction, NFT operations, and
decentralized storage management.

Features:
- Multi-chain wallet management (Ethereum, BSC, Polygon, Solana, Bitcoin)
- Smart contract compilation, deployment, and interaction
- DeFi protocol integration (AMM, lending, staking, yield farming)
- NFT minting, marketplace operations, and royalty management
- IPFS and decentralized storage operations
- Transaction monitoring and gas optimization
- Multi-chain bridge operations
- DAO governance and voting
- Token analysis and portfolio tracking
- Yield optimization and MEV protection
- Multi-signature wallet support
- Contract audit helpers
"""

import asyncio
import hashlib
import json
import logging
import math
import os
import random
import struct
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import (
    Any, Callable, Coroutine, Dict, List, Optional, Set, Tuple, Union,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("crypto_web3_agent")

# =============================================================================
# ENUMS
# =============================================================================

class Blockchain(Enum):
    ETHEREUM = "ethereum"
    BITCOIN = "bitcoin"
    BSC = "bsc"
    POLYGON = "polygon"
    SOLANA = "solana"
    AVALANCHE = "avalanche"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"

class TokenType(Enum):
    NATIVE = auto()
    ERC20 = auto()
    ERC721 = auto()
    ERC1155 = auto()
    SPL = auto()
    BRC20 = auto()

class TransactionStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    FAILED = auto()
    DROPPED = auto()
    UNKNOWN = auto()

class ContractType(Enum):
    ERC20 = auto()
    ERC721 = auto()
    ERC1155 = auto()
    DEFI_AMM = auto()
    DEFI_LENDING = auto()
    DEFI_STAKING = auto()
    DAO_GOVERNANCE = auto()
    CUSTOM = auto()

class NetworkType(Enum):
    MAINNET = auto()
    TESTNET = auto()
    LOCAL = auto()

class StorageType(Enum):
    IPFS = auto()
    ARWEAVE = auto()
    FILECOIN = auto()
    PINATA = auto()
    NFT_STORAGE = auto()

class DeFiProtocol(Enum):
    UNISWAP = auto()
    PANCAKESWAP = auto()
    AAVE = auto()
    COMPOUND = auto()
    LIDO = auto()
    CURVE = auto()
    SUSHISWAP = auto()
    CUSTOM = auto()

class NFTStandard(Enum):
    ERC721 = auto()
    ERC1155 = auto()
    METAPLEX = auto()
    CUSTOM = auto()

class ProposalStatus(Enum):
    PENDING = auto()
    ACTIVE = auto()
    SUCCEEDED = auto()
    DEFEATED = auto()
    QUEUED = auto()
    EXECUTED = auto()
    CANCELED = auto()

class YieldStrategy(Enum):
    LIQUIDITY_PROVIDING = auto()
    STAKING = auto()
    LENDING = auto()
    YIELD_FARMING = auto()
    SINGLE_SIDED = auto()
    CONCENTRATED_LIQUIDITY = auto()
    RESTAKING = auto()
    VAULT = auto()

class RiskLevel(Enum):
    VERY_LOW = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    VERY_HIGH = auto()
    DEGEN = auto()

class AuditStatus(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    PASSED = auto()
    FAILED = auto()
    FINDINGS = auto()
    REMEDIATED = auto()

class SignatureType(Enum):
    EOA = auto()
    EIP712 = auto()
    MULTISIG = auto()
    ERC4337 = auto()
    EIP2930 = auto()
    EIP1559 = auto()

class MEVProtectionMode(Enum):
    NONE = auto()
    PRIVATE_MEMPOOL = auto()
    FLASHBOTS = auto()
    MEV_BLOCKER = auto()
    BATCH_AUCTION = auto()

# =============================================================================
# CONSTANTS
# =============================================================================

CHAIN_CONFIGS: Dict[Blockchain, Dict[str, Any]] = {
    Blockchain.ETHEREUM: {
        "chain_id": 1, "rpc_url": "https://mainnet.infura.io/v3/",
        "native_currency": "ETH", "decimals": 18,
        "block_time": 12, "explorer": "https://etherscan.io",
    },
    Blockchain.BSC: {
        "chain_id": 56, "rpc_url": "https://bsc-dataseed.binance.org",
        "native_currency": "BNB", "decimals": 18,
        "block_time": 3, "explorer": "https://bscscan.com",
    },
    Blockchain.POLYGON: {
        "chain_id": 137, "rpc_url": "https://polygon-rpc.com",
        "native_currency": "MATIC", "decimals": 18,
        "block_time": 2, "explorer": "https://polygonscan.com",
    },
    Blockchain.SOLANA: {
        "chain_id": 0, "rpc_url": "https://api.mainnet-beta.solana.com",
        "native_currency": "SOL", "decimals": 9,
        "block_time": 0.4, "explorer": "https://solscan.io",
    },
    Blockchain.AVALANCHE: {
        "chain_id": 43114, "rpc_url": "https://api.avax.network/ext/bc/C/rpc",
        "native_currency": "AVAX", "decimals": 18,
        "block_time": 2, "explorer": "https://snowtrace.io",
    },
    Blockchain.ARBITRUM: {
        "chain_id": 42161, "rpc_url": "https://arb1.arbitrum.io/rpc",
        "native_currency": "ETH", "decimals": 18,
        "block_time": 0.25, "explorer": "https://arbiscan.io",
    },
    Blockchain.OPTIMISM: {
        "chain_id": 10, "rpc_url": "https://mainnet.optimism.io",
        "native_currency": "ETH", "decimals": 18,
        "block_time": 2, "explorer": "https://optimistic.etherscan.io",
    },
    Blockchain.BASE: {
        "chain_id": 8453, "rpc_url": "https://mainnet.base.org",
        "native_currency": "ETH", "decimals": 18,
        "block_time": 2, "explorer": "https://basescan.org",
    },
}

GAS_LIMITS: Dict[str, int] = {
    "transfer_eth": 21000,
    "transfer_erc20": 65000,
    "swap": 150000,
    "mint_nft": 200000,
    "deploy_contract": 3000000,
    "approve": 46000,
    "stake": 100000,
    "unstake": 80000,
    "claim_rewards": 120000,
    "vote": 150000,
    "batch_transfer": 80000,
    "set_approval_for_all": 46000,
    "multisig_submit": 200000,
    "multisig_execute": 150000,
}

ERC20_ABI = [
    {"type": "function", "name": "balanceOf", "inputs": [{"name": "account", "type": "address"}],
     "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view"},
    {"type": "function", "name": "transfer", "inputs": [
        {"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}],
     "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable"},
    {"type": "function", "name": "approve", "inputs": [
        {"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],
     "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable"},
    {"type": "function", "name": "allowance", "inputs": [
        {"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}],
     "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view"},
    {"type": "function", "name": "totalSupply", "inputs": [],
     "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view"},
    {"type": "function", "name": "decimals", "inputs": [],
     "outputs": [{"name": "", "type": "uint8"}], "stateMutability": "view"},
    {"type": "function", "name": "symbol", "inputs": [],
     "outputs": [{"name": "", "type": "string"}], "stateMutability": "view"},
]

ERC721_ABI = [
    {"type": "function", "name": "balanceOf", "inputs": [{"name": "owner", "type": "address"}],
     "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view"},
    {"type": "function", "name": "ownerOf", "inputs": [{"name": "tokenId", "type": "uint256"}],
     "outputs": [{"name": "", "type": "address"}], "stateMutability": "view"},
    {"type": "function", "name": "safeTransferFrom", "inputs": [
        {"name": "from", "type": "address"}, {"name": "to", "type": "address"},
        {"name": "tokenId", "type": "uint256"}],
     "outputs": [], "stateMutability": "nonpayable"},
    {"type": "function", "name": "tokenURI", "inputs": [{"name": "tokenId", "type": "uint256"}],
     "outputs": [{"name": "", "type": "string"}], "stateMutability": "view"},
]

UNISWAP_ROUTER_ABI = [
    {"type": "function", "name": "swapExactTokensForTokens", "inputs": [
        {"name": "amountIn", "type": "uint256"},
        {"name": "amountOutMin", "type": "uint256"},
        {"name": "path", "type": "address[]"},
        {"name": "to", "type": "address"},
        {"name": "deadline", "type": "uint256"}],
     "outputs": [{"name": "amounts", "type": "uint256[]"}], "stateMutability": "nonpayable"},
    {"type": "function", "name": "addLiquidity", "inputs": [
        {"name": "tokenA", "type": "address"}, {"name": "tokenB", "type": "address"},
        {"name": "amountADesired", "type": "uint256"}, {"name": "amountBDesired", "type": "uint256"},
        {"name": "amountAMin", "type": "uint256"}, {"name": "amountBMin", "type": "uint256"},
        {"name": "to", "type": "address"}, {"name": "deadline", "type": "uint256"}],
     "outputs": [
         {"name": "amountA", "type": "uint256"}, {"name": "amountB", "type": "uint256"},
         {"name": "liquidity", "type": "uint256"}], "stateMutability": "nonpayable"},
]

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class WalletInfo:
    address: str
    chain: Blockchain
    name: str
    balance: float = 0.0
    tokens: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    nonce: int = 0

@dataclass
class TokenInfo:
    address: str
    name: str
    symbol: str
    decimals: int
    chain: Blockchain
    token_type: TokenType = TokenType.ERC20
    total_supply: float = 0.0
    verified: bool = False

@dataclass
class TransactionRecord:
    tx_hash: str
    from_address: str
    to_address: str
    value: float
    chain: Blockchain
    token_symbol: str = "ETH"
    status: TransactionStatus = TransactionStatus.PENDING
    gas_used: int = 0
    gas_price: float = 0.0
    nonce: int = 0
    block_number: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)
    method_name: Optional[str] = None
    contract_address: Optional[str] = None

@dataclass
class ContractInfo:
    address: str
    name: str
    chain: Blockchain
    contract_type: ContractType
    abi: List[Dict[str, Any]] = field(default_factory=list)
    bytecode: str = ""
    deployer: str = ""
    deployed_at: datetime = field(default_factory=datetime.now)
    verified: bool = False
    source_code: str = ""
    compiler_version: str = ""

@dataclass
class NFTInfo:
    token_id: int
    contract_address: str
    chain: Blockchain
    owner: str
    name: str = ""
    description: str = ""
    image_url: str = ""
    metadata_uri: str = ""
    token_standard: NFTStandard = NFTStandard.ERC721
    royalty_percent: float = 0.0
    last_sale_price: float = 0.0
    attributes: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class DeFiPosition:
    protocol: DeFiProtocol
    pool_address: str
    chain: Blockchain
    user_address: str
    token_a: str
    token_b: str
    amount_a: float = 0.0
    amount_b: float = 0.0
    lp_tokens: float = 0.0
    value_usd: float = 0.0
    apr: float = 0.0
    rewards: float = 0.0

@dataclass
class StakingPosition:
    validator: str
    chain: Blockchain
    staker: str
    amount: float
    rewards: float = 0.0
    apr: float = 0.0
    lock_period_days: int = 0
    staked_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

@dataclass
class ProposalInfo:
    proposal_id: int
    chain: Blockchain
    governor_address: str
    proposer: str
    title: str
    description: str = ""
    status: ProposalStatus = ProposalStatus.PENDING
    votes_for: float = 0.0
    votes_against: float = 0.0
    votes_abstain: float = 0.0
    start_block: int = 0
    end_block: int = 0
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class GasEstimate:
    chain: Blockchain
    method_name: str
    gas_limit: int
    gas_price_gwei: float
    max_fee_per_gas: float = 0.0
    max_priority_fee: float = 0.0
    estimated_cost_native: float = 0.0
    estimated_cost_usd: float = 0.0

@dataclass
class StorageMetadata:
    cid: str
    name: str
    size_bytes: int
    storage_type: StorageType
    pinned: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    gateway_url: str = ""
    pinata_url: str = ""

@dataclass
class BridgeConfig:
    source_chain: Blockchain
    dest_chain: Blockchain
    token_address: str
    bridge_address: str
    fee_percent: float = 0.1
    min_amount: float = 0.0
    max_amount: float = float("inf")
    estimated_time_seconds: int = 300

@dataclass
class PriceQuote:
    token_in: str
    token_out: str
    amount_in: float
    amount_out: float
    price_impact: float
    route: List[str]
    gas_estimate: float
    pool_addresses: List[str]

@dataclass
class YieldPosition:
    strategy: YieldStrategy
    protocol: DeFiProtocol
    chain: Blockchain
    user_address: str
    token: str
    amount: float = 0.0
    apy: float = 0.0
    value_usd: float = 0.0
    risk_level: RiskLevel = RiskLevel.MEDIUM
    auto_compound: bool = False
    lock_end: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class AuditReport:
    contract_address: str
    chain: Blockchain
    auditor: str
    status: AuditStatus = AuditStatus.NOT_STARTED
    findings_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    informational_count: int = 0
    recommendations: List[str] = field(default_factory=list)
    completed_at: Optional[datetime] = None
    report_url: str = ""

@dataclass
class MultiSigTransaction:
    tx_id: str
    contract_address: str
    chain: Blockchain
    proposer: str
    destination: str
    value: float
    data: str = ""
    executed: bool = False
    confirmations: List[str] = field(default_factory=list)
    required_signatures: int = 2
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None

@dataclass
class MEVBundle:
    bundle_id: str
    transactions: List[Dict[str, Any]]
    chain: Blockchain
    target_block: int
    protection_mode: MEVProtectionMode = MEVProtectionMode.PRIVATE_MEMPOOL
    status: str = "pending"
    submitted_at: datetime = field(default_factory=datetime.now)
    included_in_block: Optional[int] = None
    profit_usd: float = 0.0

@dataclass
class PortfolioSnapshot:
    timestamp: datetime
    total_value_usd: float
    chain_values: Dict[str, float] = field(default_factory=dict)
    token_allocations: Dict[str, float] = field(default_factory=dict)
    defi_positions_count: int = 0
    nft_count: int = 0
    staking_value_usd: float = 0.0
    pending_rewards_usd: float = 0.0

# =============================================================================
# EXCEPTIONS
# =============================================================================

class Web3AgentError(Exception):
    pass

class WalletError(Web3AgentError):
    pass

class TransactionError(Web3AgentError):
    pass

class ContractError(Web3AgentError):
    pass

class InsufficientFundsError(Web3AgentError):
    pass

class NetworkError(Web3AgentError):
    pass

class IPFSError(Web3AgentError):
    pass

class DeFiError(Web3AgentError):
    pass

class BridgeError(Web3AgentError):
    pass

class MEVProtectionError(Web3AgentError):
    pass

class MultiSigError(Web3AgentError):
    pass

class AuditError(Web3AgentError):
    pass

# =============================================================================
# WALLET MANAGER
# =============================================================================

class WalletManager:
    def __init__(self):
        self._wallets: Dict[str, WalletInfo] = {}
        self._transactions: List[TransactionRecord] = []
        self._balances: Dict[str, float] = {}
        self._token_balances: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._approvals: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self._lock = threading.Lock()

    def create_wallet(self, chain: Blockchain, name: Optional[str] = None,
                      private_key: Optional[str] = None) -> WalletInfo:
        address = "0x" + hashlib.md5(f"{chain.value}_{time.time()}".encode()).hexdigest()[:40]
        wallet = WalletInfo(address=address, chain=chain, name=name or f"Wallet_{len(self._wallets)+1}")
        with self._lock:
            self._wallets[address] = wallet
            self._balances[address] = 0.0
        logger.info("Created wallet %s on %s", address[:10], chain.value)
        return wallet

    def import_wallet(self, address: str, chain: Blockchain, name: str = "Imported") -> WalletInfo:
        with self._lock:
            if address in self._wallets:
                return self._wallets[address]
        wallet = WalletInfo(address=address, chain=chain, name=name)
        with self._lock:
            self._wallets[address] = wallet
        logger.info("Imported wallet %s on %s", address[:10], chain.value)
        return wallet

    def get_wallet(self, address: str) -> Optional[WalletInfo]:
        with self._lock:
            return self._wallets.get(address)

    def get_balance(self, address: str) -> Dict[str, Any]:
        with self._lock:
            wallet = self._wallets.get(address)
        if not wallet:
            return {"error": "Wallet not found"}
        return {
            "address": address, "chain": wallet.chain.value,
            "native_balance": self._balances.get(address, 0.0),
            "tokens": self._token_balances.get(address, {}),
        }

    def set_balance(self, address: str, balance: float) -> None:
        with self._lock:
            self._balances[address] = balance

    def set_token_balance(self, address: str, token_symbol: str, amount: float) -> None:
        with self._lock:
            self._token_balances[address][token_symbol] = amount

    def transfer(self, from_address: str, to_address: str, amount: float,
                 token_symbol: str = "ETH", chain: Blockchain = Blockchain.ETHEREUM) -> TransactionRecord:
        with self._lock:
            if from_address not in self._wallets:
                raise WalletError(f"Sender wallet {from_address} not found")
            if token_symbol == "ETH":
                if self._balances.get(from_address, 0) < amount:
                    raise InsufficientFundsError(f"Insufficient {token_symbol} balance")
                self._balances[from_address] -= amount
                self._balances[to_address] = self._balances.get(to_address, 0) + amount
            else:
                current = self._token_balances[from_address].get(token_symbol, 0)
                if current < amount:
                    raise InsufficientFundsError(f"Insufficient {token_symbol} balance")
                self._token_balances[from_address][token_symbol] = current - amount
                self._token_balances[to_address][token_symbol] = (
                    self._token_balances[to_address].get(token_symbol, 0) + amount
                )
        tx_hash = "0x" + hashlib.sha256(f"{from_address}_{to_address}_{time.time()}".encode()).hexdigest()[:64]
        record = TransactionRecord(
            tx_hash=tx_hash, from_address=from_address, to_address=to_address,
            value=amount, chain=chain, token_symbol=token_symbol,
            status=TransactionStatus.CONFIRMED, gas_used=21000, gas_price=20.0,
        )
        with self._lock:
            self._transactions.append(record)
        logger.info("Transfer %s: %s %s from %s to %s", tx_hash[:10], amount, token_symbol, from_address[:10], to_address[:10])
        return record

    def batch_transfer(self, from_address: str, transfers: List[Tuple[str, float, str]],
                       chain: Blockchain = Blockchain.ETHEREUM) -> List[TransactionRecord]:
        results = []
        for to_address, amount, token in transfers:
            tx = self.transfer(from_address, to_address, amount, token, chain)
            results.append(tx)
        return results

    def set_approval(self, owner: str, spender: str, token_symbol: str, amount: float) -> bool:
        with self._lock:
            self._approvals[owner][f"{spender}_{token_symbol}"] = amount
        logger.info("Approval set: %s -> %s for %s (%.4f)", owner[:10], spender[:10], token_symbol, amount)
        return True

    def get_approval(self, owner: str, spender: str, token_symbol: str) -> float:
        with self._lock:
            return self._approvals[owner].get(f"{spender}_{token_symbol}", 0.0)

    def get_transaction_history(self, address: str, limit: int = 50) -> List[TransactionRecord]:
        with self._lock:
            txs = [t for t in self._transactions if t.from_address == address or t.to_address == address]
        return txs[-limit:]

    def get_all_wallets(self, chain: Optional[Blockchain] = None) -> List[WalletInfo]:
        with self._lock:
            wallets = list(self._wallets.values())
        if chain:
            wallets = [w for w in wallets if w.chain == chain]
        return wallets

    def get_total_value(self, prices: Dict[str, float]) -> float:
        total = 0.0
        with self._lock:
            for address, balance in self._balances.items():
                wallet = self._wallets.get(address)
                if wallet:
                    symbol = CHAIN_CONFIGS.get(wallet.chain, {}).get("native_currency", "ETH")
                    total += balance * prices.get(symbol, 0.0)
                for token, amount in self._token_balances.get(address, {}).items():
                    total += amount * prices.get(token, 0.0)
        return total

    def get_chain_balances(self, chain: Blockchain) -> Dict[str, float]:
        with self._lock:
            result = {}
            for address, wallet in self._wallets.items():
                if wallet.chain == chain:
                    result[address] = self._balances.get(address, 0.0)
            return result

# =============================================================================
# SMART CONTRACT MANAGER
# =============================================================================

class SmartContractManager:
    def __init__(self):
        self._contracts: Dict[str, ContractInfo] = {}
        self._deployments: List[Dict[str, Any]] = []
        self._abi_registry: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = threading.Lock()

    def compile_contract(self, source_code: str, contract_name: str,
                         compiler_version: str = "0.8.19") -> Dict[str, Any]:
        bytecode = "0x608060405234801561001057600080fd5b50"
        abi = [{"type": "constructor", "inputs": []}]
        with self._lock:
            self._abi_registry[contract_name] = abi
        return {"bytecode": bytecode, "abi": abi, "contract_name": contract_name,
                "compiler_version": compiler_version}

    def deploy(self, bytecode: str, abi: List[Dict[str, Any]], chain: Blockchain,
               deployer: str, contract_name: str = "Unnamed",
               constructor_args: Optional[List[Any]] = None,
               gas_limit: int = 3000000) -> ContractInfo:
        address = "0x" + hashlib.sha256(f"{deployer}_{time.time()}".encode()).hexdigest()[:40]
        contract = ContractInfo(
            address=address, name=contract_name, chain=chain,
            contract_type=ContractType.CUSTOM, abi=abi, bytecode=bytecode,
            deployer=deployer, source_code="", compiler_version="0.8.19",
        )
        tx_hash = "0x" + hashlib.sha256(f"deploy_{address}".encode()).hexdigest()[:64]
        with self._lock:
            self._contracts[address] = contract
            self._deployments.append({
                "tx_hash": tx_hash, "contract_address": address,
                "chain": chain.value, "deployer": deployer,
                "timestamp": datetime.now().isoformat(),
            })
        logger.info("Deployed contract %s at %s on %s", contract_name, address[:10], chain.value)
        return contract

    def deploy_erc20(self, name: str, symbol: str, decimals: int, total_supply: float,
                     chain: Blockchain, deployer: str) -> ContractInfo:
        return self.deploy(
            bytecode="0x608060405234801561001057600080fd5b50", abi=ERC20_ABI,
            chain=chain, deployer=deployer, contract_name=f"{name} ({symbol})",
        )

    def deploy_erc721(self, name: str, symbol: str, base_uri: str,
                      chain: Blockchain, deployer: str) -> ContractInfo:
        return self.deploy(
            bytecode="0x608060405234801561001057600080fd5b50", abi=ERC721_ABI,
            chain=chain, deployer=deployer, contract_name=f"NFT: {name} ({symbol})",
        )

    def get_contract(self, address: str) -> Optional[ContractInfo]:
        with self._lock:
            return self._contracts.get(address)

    def get_all_contracts(self, chain: Optional[Blockchain] = None) -> List[ContractInfo]:
        with self._lock:
            contracts = list(self._contracts.values())
        if chain:
            contracts = [c for c in contracts if c.chain == chain]
        return contracts

    def verify_contract(self, address: str, source_code: str) -> bool:
        with self._lock:
            if address in self._contracts:
                self._contracts[address].verified = True
                self._contracts[address].source_code = source_code
                logger.info("Contract %s verified", address[:10])
                return True
        return False

    def encode_function_call(self, function_name: str, params: List[Any]) -> str:
        func_id = hashlib.sha256(function_name.encode()).hexdigest()[:8]
        return f"0x{func_id}"

    def decode_event(self, event_data: str, abi: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"event": "Transfer", "decoded": True, "raw": event_data}

    def estimate_deployment_gas(self, contract_type: ContractType) -> int:
        estimates = {
            ContractType.ERC20: 1500000, ContractType.ERC721: 2500000,
            ContractType.ERC1155: 3000000, ContractType.DEFI_AMM: 4000000,
            ContractType.DEFI_LENDING: 5000000, ContractType.DAO_GOVERNANCE: 6000000,
            ContractType.CUSTOM: 3000000,
        }
        return estimates.get(contract_type, 3000000)

    def get_deployment_history(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._deployments)

    def get_verified_contracts(self) -> List[ContractInfo]:
        with self._lock:
            return [c for c in self._contracts.values() if c.verified]

    def register_abi(self, name: str, abi: List[Dict[str, Any]]) -> None:
        with self._lock:
            self._abi_registry[name] = abi
        logger.info("Registered ABI: %s", name)

    def get_abi(self, name: str) -> Optional[List[Dict[str, Any]]]:
        with self._lock:
            return self._abi_registry.get(name)

# =============================================================================
# DEFI MANAGER
# =============================================================================

class DeFiManager:
    def __init__(self, wallet_manager: WalletManager):
        self._wallet_manager = wallet_manager
        self._positions: Dict[str, DeFiPosition] = {}
        self._staking: Dict[str, StakingPosition] = {}
        self._swap_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def get_swap_quote(self, token_in: str, token_out: str, amount_in: float,
                       chain: Blockchain = Blockchain.ETHEREUM,
                       slippage_percent: float = 0.5) -> PriceQuote:
        price_impact = min(amount_in * 0.0001, 5.0)
        amount_out = amount_in * random.uniform(0.98, 1.02)
        min_out = amount_out * (1 - slippage_percent / 100)
        return PriceQuote(
            token_in=token_in, token_out=token_out, amount_in=amount_in,
            amount_out=amount_out, price_impact=price_impact,
            route=[token_in, token_out], gas_estimate=150000,
            pool_addresses=["0x" + hashlib.md5(f"{token_in}_{token_out}".encode()).hexdigest()[:40]],
        )

    def execute_swap(self, user_address: str, token_in: str, token_out: str,
                     amount_in: float, min_amount_out: float,
                     chain: Blockchain = Blockchain.ETHEREUM) -> TransactionRecord:
        quote = self.get_swap_quote(token_in, token_out, amount_in, chain)
        tx = self._wallet_manager.transfer(
            user_address, "0x" + "0" * 40, 0.0, token_in, chain,
        )
        tx.method_name = "swap"
        swap_record = {
            "token_in": token_in, "token_out": token_out,
            "amount_in": amount_in, "amount_out": quote.amount_out,
            "price_impact": quote.price_impact, "chain": chain.value,
            "timestamp": datetime.now().isoformat(),
        }
        with self._lock:
            self._swap_history.append(swap_record)
        logger.info("Swap executed: %s %s -> %s %s", amount_in, token_in, quote.amount_out, token_out)
        return tx

    def add_liquidity(self, user_address: str, token_a: str, token_b: str,
                      amount_a: float, amount_b: float,
                      chain: Blockchain = Blockchain.ETHEREUM) -> DeFiPosition:
        position_id = f"{user_address}_{token_a}_{token_b}_{chain.value}"
        position = DeFiPosition(
            protocol=DeFiProtocol.UNISWAP, pool_address="0x" + hashlib.md5(position_id.encode()).hexdigest()[:40],
            chain=chain, user_address=user_address, token_a=token_a, token_b=token_b,
            amount_a=amount_a, amount_b=amount_b, lp_tokens=amount_a * 0.5,
            value_usd=(amount_a + amount_b) * 1500, apr=random.uniform(5.0, 50.0),
        )
        with self._lock:
            self._positions[position_id] = position
        logger.info("Liquidity added: %s/%s on %s", token_a, token_b, chain.value)
        return position

    def remove_liquidity(self, user_address: str, token_a: str, token_b: str,
                         chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        position_id = f"{user_address}_{token_a}_{token_b}_{chain.value}"
        with self._lock:
            position = self._positions.pop(position_id, None)
        if not position:
            return {"error": "Position not found"}
        return {
            "amount_a": position.amount_a, "amount_b": position.amount_b,
            "lp_tokens_burned": position.lp_tokens, "chain": chain.value,
        }

    def get_positions(self, user_address: str) -> List[DeFiPosition]:
        with self._lock:
            return [p for p in self._positions.values() if p.user_address == user_address]

    def stake(self, user_address: str, validator: str, amount: float,
              chain: Blockchain = Blockchain.ETHEREUM, lock_days: int = 0) -> StakingPosition:
        position_id = f"{user_address}_{validator}_{chain.value}"
        position = StakingPosition(
            validator=validator, chain=chain, staker=user_address,
            amount=amount, apr=random.uniform(3.0, 15.0),
            lock_period_days=lock_days,
        )
        with self._lock:
            self._staking[position_id] = position
        logger.info("Staked %s on %s (validator: %s)", amount, chain.value, validator[:10])
        return position

    def unstake(self, user_address: str, validator: str,
                chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        position_id = f"{user_address}_{validator}_{chain.value}"
        with self._lock:
            position = self._staking.pop(position_id, None)
        if not position:
            return {"error": "Staking position not found"}
        return {"amount": position.amount, "rewards": position.rewards, "chain": chain.value}

    def get_staking_positions(self, user_address: str) -> List[StakingPosition]:
        with self._lock:
            return [s for s in self._staking.values() if s.staker == user_address]

    def get_swap_history(self, user_address: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            history = list(self._swap_history)
        return history[-limit:]

    def calculate_impermanent_loss(self, price_change_percent: float) -> float:
        ratio = 1 + price_change_percent / 100
        return 2 * (ratio ** 0.5) / (1 + ratio) - 1

    def estimate_lp_value(self, amount_a: float, amount_b: float,
                          price_a: float, price_b: float) -> float:
        return amount_a * price_a + amount_b * price_b

# =============================================================================
# NFT MANAGER
# =============================================================================

class NFTManager:
    def __init__(self, wallet_manager: WalletManager, contract_manager: SmartContractManager):
        self._wallet_manager = wallet_manager
        self._contract_manager = contract_manager
        self._nfts: Dict[str, NFTInfo] = {}
        self._listings: List[Dict[str, Any]] = []
        self._sales: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def mint_nft(self, contract_address: str, chain: Blockchain, recipient: str,
                 name: str, description: str, image_url: str,
                 metadata_uri: str, royalty_percent: float = 5.0,
                 attributes: Optional[List[Dict[str, Any]]] = None) -> NFTInfo:
        token_id = random.randint(1, 2**32)
        nft = NFTInfo(
            token_id=token_id, contract_address=contract_address, chain=chain,
            owner=recipient, name=name, description=description,
            image_url=image_url, metadata_uri=metadata_uri,
            royalty_percent=royalty_percent, attributes=attributes or [],
        )
        with self._lock:
            key = f"{contract_address}_{token_id}"
            self._nfts[key] = nft
        logger.info("Minted NFT #%d at %s for %s", token_id, contract_address[:10], recipient[:10])
        return nft

    def transfer_nft(self, contract_address: str, token_id: int, from_address: str,
                     to_address: str, chain: Blockchain) -> TransactionRecord:
        key = f"{contract_address}_{token_id}"
        with self._lock:
            nft = self._nfts.get(key)
            if nft:
                nft.owner = to_address
        tx = self._wallet_manager.transfer(from_address, to_address, 0.0, "NFT", chain)
        tx.method_name = "safeTransferFrom"
        tx.contract_address = contract_address
        logger.info("NFT #%d transferred from %s to %s", token_id, from_address[:10], to_address[:10])
        return tx

    def list_nft(self, contract_address: str, token_id: int, seller: str,
                 price: float, currency: str = "ETH", chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        listing = {
            "contract_address": contract_address, "token_id": token_id,
            "seller": seller, "price": price, "currency": currency,
            "chain": chain.value, "listed_at": datetime.now().isoformat(),
            "status": "active",
        }
        with self._lock:
            self._listings.append(listing)
        logger.info("NFT #%d listed for %s %s", token_id, price, currency)
        return listing

    def buy_nft(self, contract_address: str, token_id: int, buyer: str,
                chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        key = f"{contract_address}_{token_id}"
        with self._lock:
            listing = None
            for l in self._listings:
                if l["contract_address"] == contract_address and l["token_id"] == token_id and l["status"] == "active":
                    listing = l
                    break
            if not listing:
                return {"error": "NFT not listed"}
            nft = self._nfts.get(key)
            if nft:
                nft.owner = buyer
                nft.last_sale_price = listing["price"]
            listing["status"] = "sold"
            sale = {**listing, "buyer": buyer, "sold_at": datetime.now().isoformat()}
            self._sales.append(sale)
        logger.info("NFT #%d bought by %s for %s %s", token_id, buyer[:10], listing["price"], listing["currency"])
        return sale

    def get_nft(self, contract_address: str, token_id: int) -> Optional[NFTInfo]:
        with self._lock:
            return self._nfts.get(f"{contract_address}_{token_id}")

    def get_collection(self, contract_address: str) -> List[NFTInfo]:
        with self._lock:
            return [n for k, n in self._nfts.items() if k.startswith(contract_address)]

    def get_owner_nfts(self, owner_address: str) -> List[NFTInfo]:
        with self._lock:
            return [n for n in self._nfts.values() if n.owner == owner_address]

    def get_listings(self, chain: Optional[Blockchain] = None) -> List[Dict[str, Any]]:
        with self._lock:
            listings = [l for l in self._listings if l["status"] == "active"]
        if chain:
            listings = [l for l in listings if l["chain"] == chain.value]
        return listings

    def get_sales_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._sales)[-limit:]

    def create_collection(self, name: str, symbol: str, chain: Blockchain,
                          deployer: str, max_supply: int, base_price: float) -> ContractInfo:
        contract = self._contract_manager.deploy_erc721(name, symbol, f"ipfs://collection/{name}/", chain, deployer)
        logger.info("Created NFT collection: %s (%s) on %s", name, symbol, chain.value)
        return contract

    def set_royalty(self, contract_address: str, royalty_percent: float) -> bool:
        with self._lock:
            for nft in self._nfts.values():
                if nft.contract_address == contract_address:
                    nft.royalty_percent = royalty_percent
        return True

# =============================================================================
# STORAGE MANAGER
# =============================================================================

class StorageManager:
    def __init__(self):
        self._stored_files: Dict[str, StorageMetadata] = {}
        self._pin_queue: deque = deque()
        self._lock = threading.Lock()

    def upload_to_ipfs(self, data: bytes, name: str, pin: bool = True) -> StorageMetadata:
        cid = "Qm" + hashlib.sha256(data).hexdigest()[:44]
        metadata = StorageMetadata(
            cid=cid, name=name, size_bytes=len(data),
            storage_type=StorageType.IPFS, pinned=pin,
            gateway_url=f"https://ipfs.io/ipfs/{cid}",
        )
        with self._lock:
            self._stored_files[cid] = metadata
        logger.info("Uploaded to IPFS: %s (CID: %s)", name, cid[:12])
        return metadata

    def upload_to_arweave(self, data: bytes, name: str) -> StorageMetadata:
        tx_id = hashlib.sha256(data).hexdigest()[:64]
        metadata = StorageMetadata(
            cid=tx_id, name=name, size_bytes=len(data),
            storage_type=StorageType.ARWEAVE, pinned=True,
            gateway_url=f"https://arweave.net/{tx_id}",
        )
        with self._lock:
            self._stored_files[tx_id] = metadata
        logger.info("Uploaded to Arweave: %s (TX: %s)", name, tx_id[:12])
        return metadata

    def pin_to_pinata(self, cid: str, name: str) -> StorageMetadata:
        metadata = StorageMetadata(
            cid=cid, name=name, size_bytes=0,
            storage_type=StorageType.PINATA, pinned=True,
            pinata_url=f"https://gateway.pinata.cloud/ipfs/{cid}",
        )
        with self._lock:
            self._stored_files[cid] = metadata
        logger.info("Pinned to Pinata: %s (CID: %s)", name, cid[:12])
        return metadata

    def store_nft_metadata(self, name: str, description: str, image_url: str,
                           attributes: List[Dict[str, Any]]) -> StorageMetadata:
        metadata_json = json.dumps({
            "name": name, "description": description,
            "image": image_url, "attributes": attributes,
        }, indent=2)
        return self.upload_to_ipfs(metadata_json.encode(), f"{name}_metadata.json")

    def get_file(self, cid: str) -> Optional[StorageMetadata]:
        with self._lock:
            return self._stored_files.get(cid)

    def list_files(self, storage_type: Optional[StorageType] = None) -> List[StorageMetadata]:
        with self._lock:
            files = list(self._stored_files.values())
        if storage_type:
            files = [f for f in files if f.storage_type == storage_type]
        return files

    def unpin(self, cid: str) -> bool:
        with self._lock:
            if cid in self._stored_files:
                self._stored_files[cid].pinned = False
                return True
        return False

    def get_storage_stats(self) -> Dict[str, Any]:
        with self._lock:
            total_files = len(self._stored_files)
            total_size = sum(f.size_bytes for f in self._stored_files.values())
            by_type = defaultdict(int)
            for f in self._stored_files.values():
                by_type[f.storage_type.name] += 1
        return {"total_files": total_files, "total_size_bytes": total_size,
                "by_type": dict(by_type), "pinned_count": sum(1 for f in self._stored_files.values() if f.pinned)}

# =============================================================================
# GAS OPTIMIZER
# =============================================================================

class GasOptimizer:
    def __init__(self):
        self._gas_history: Dict[Blockchain, deque] = defaultdict(lambda: deque(maxlen=100))
        self._lock = threading.Lock()

    def record_gas_price(self, chain: Blockchain, gas_price_gwei: float) -> None:
        with self._lock:
            self._gas_history[chain].append({
                "gas_price": gas_price_gwei, "timestamp": datetime.now().isoformat(),
            })

    def get_gas_estimate(self, chain: Blockchain, method_name: str) -> GasEstimate:
        gas_limit = GAS_LIMITS.get(method_name, 100000)
        history = list(self._gas_history.get(chain, []))
        if history:
            avg_price = sum(h["gas_price"] for h in history[-20:]) / min(20, len(history))
        else:
            avg_price = 20.0
        config = CHAIN_CONFIGS.get(chain, {})
        native = config.get("native_currency", "ETH")
        cost_native = (gas_limit * avg_price) / 1e9
        return GasEstimate(
            chain=chain, method_name=method_name, gas_limit=gas_limit,
            gas_price_gwei=avg_price, max_fee_per_gas=avg_price * 1.2,
            max_priority_fee=avg_price * 0.1, estimated_cost_native=cost_native,
        )

    def suggest_gas_price(self, chain: Blockchain) -> Dict[str, float]:
        history = list(self._gas_history.get(chain, []))
        if not history:
            return {"slow": 10.0, "standard": 20.0, "fast": 30.0}
        prices = [h["gas_price"] for h in history[-50:]]
        prices.sort()
        n = len(prices)
        return {
            "slow": prices[n // 4] if n > 4 else prices[0],
            "standard": prices[n // 2] if n > 1 else prices[0],
            "fast": prices[3 * n // 4] if n > 4 else prices[-1],
        }

    def estimate_swap_cost(self, chain: Blockchain, amount_usd: float) -> Dict[str, Any]:
        estimate = self.get_gas_estimate(chain, "swap")
        return {
            "gas_limit": estimate.gas_limit,
            "gas_price_gwei": estimate.gas_price_gwei,
            "estimated_cost_native": estimate.estimated_cost_native,
            "cost_as_percent_of_trade": (estimate.estimated_cost_native * 2000 / amount_usd * 100) if amount_usd > 0 else 0,
        }

    def get_optimal_timing(self, chain: Blockchain) -> Dict[str, Any]:
        history = list(self._gas_history.get(chain, []))
        if len(history) < 10:
            return {"recommendation": "unknown", "reason": "insufficient data"}
        recent = [h["gas_price"] for h in history[-10:]]
        avg = sum(recent) / len(recent)
        current = recent[-1]
        if current < avg * 0.8:
            return {"recommendation": "now", "reason": "gas price below average"}
        if current > avg * 1.2:
            return {"recommendation": "wait", "reason": "gas price above average"}
        return {"recommendation": "ok", "reason": "gas price near average"}

# =============================================================================
# BRIDGE MANAGER
# =============================================================================

class BridgeManager:
    def __init__(self, wallet_manager: WalletManager):
        self._wallet_manager = wallet_manager
        self._bridges: List[BridgeConfig] = []
        self._bridge_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def register_bridge(self, config: BridgeConfig) -> None:
        with self._lock:
            self._bridges.append(config)
        logger.info("Registered bridge: %s -> %s", config.source_chain.value, config.dest_chain.value)

    def get_available_bridges(self, source_chain: Blockchain,
                              dest_chain: Blockchain) -> List[BridgeConfig]:
        with self._lock:
            return [b for b in self._bridges
                    if b.source_chain == source_chain and b.dest_chain == dest_chain]

    def estimate_bridge(self, source_chain: Blockchain, dest_chain: Blockchain,
                        token_address: str, amount: float) -> Dict[str, Any]:
        bridges = self.get_available_bridges(source_chain, dest_chain)
        if not bridges:
            return {"error": "No bridge found"}
        bridge = bridges[0]
        fee = amount * bridge.fee_percent / 100
        return {
            "amount_in": amount, "amount_out": amount - fee,
            "fee": fee, "fee_percent": bridge.fee_percent,
            "estimated_time_seconds": bridge.estimated_time_seconds,
            "source_chain": source_chain.value, "dest_chain": dest_chain.value,
        }

    def execute_bridge(self, user_address: str, source_chain: Blockchain,
                       dest_chain: Blockchain, token_address: str,
                       amount: float) -> Dict[str, Any]:
        estimate = self.estimate_bridge(source_chain, dest_chain, token_address, amount)
        if "error" in estimate:
            return estimate
        bridge_id = str(uuid.uuid4())[:8]
        record = {
            "bridge_id": bridge_id, "user": user_address,
            "source_chain": source_chain.value, "dest_chain": dest_chain.value,
            "amount": amount, "fee": estimate["fee"],
            "amount_out": estimate["amount_out"],
            "status": "pending", "created_at": datetime.now().isoformat(),
        }
        with self._lock:
            self._bridge_history.append(record)
        logger.info("Bridge initiated: %s %s from %s to %s", amount, token_address[:10], source_chain.value, dest_chain.value)
        return record

    def get_bridge_history(self, user_address: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            history = list(self._bridge_history)
        if user_address:
            history = [h for h in history if h["user"] == user_address]
        return history

# =============================================================================
# DAO MANAGER
# =============================================================================

class DAOManager:
    def __init__(self):
        self._proposals: Dict[int, ProposalInfo] = {}
        self._votes: Dict[int, Dict[str, str]] = defaultdict(dict)
        self._lock = threading.Lock()
        self._next_id = 1

    def create_proposal(self, chain: Blockchain, governor_address: str, proposer: str,
                        title: str, description: str = "",
                        start_block: int = 0, end_block: int = 100) -> ProposalInfo:
        proposal_id = self._next_id
        self._next_id += 1
        proposal = ProposalInfo(
            proposal_id=proposal_id, chain=chain, governor_address=governor_address,
            proposer=proposer, title=title, description=description,
            status=ProposalStatus.ACTIVE, start_block=start_block, end_block=end_block,
        )
        with self._lock:
            self._proposals[proposal_id] = proposal
        logger.info("Proposal #%d created: %s", proposal_id, title)
        return proposal

    def cast_vote(self, proposal_id: int, voter: str, support: str,
                  weight: float = 1.0) -> Dict[str, Any]:
        with self._lock:
            proposal = self._proposals.get(proposal_id)
            if not proposal:
                return {"error": "Proposal not found"}
            if voter in self._votes[proposal_id]:
                return {"error": "Already voted"}
            self._votes[proposal_id][voter] = support
            if support == "for":
                proposal.votes_for += weight
            elif support == "against":
                proposal.votes_against += weight
            elif support == "abstain":
                proposal.votes_abstain += weight
        logger.info("Vote cast on proposal #%d by %s: %s", proposal_id, voter[:10], support)
        return {"proposal_id": proposal_id, "voter": voter, "support": support, "weight": weight}

    def get_proposal(self, proposal_id: int) -> Optional[ProposalInfo]:
        with self._lock:
            return self._proposals.get(proposal_id)

    def get_active_proposals(self, chain: Optional[Blockchain] = None) -> List[ProposalInfo]:
        with self._lock:
            proposals = [p for p in self._proposals.values()
                         if p.status in (ProposalStatus.ACTIVE, ProposalStatus.PENDING)]
        if chain:
            proposals = [p for p in proposals if p.chain == chain]
        return proposals

    def get_vote_results(self, proposal_id: int) -> Dict[str, Any]:
        with self._lock:
            proposal = self._proposals.get(proposal_id)
            votes = dict(self._votes.get(proposal_id, {}))
        if not proposal:
            return {"error": "Proposal not found"}
        total = proposal.votes_for + proposal.votes_against + proposal.votes_abstain
        return {
            "proposal_id": proposal_id, "title": proposal.title,
            "votes_for": proposal.votes_for, "votes_against": proposal.votes_against,
            "votes_abstain": proposal.votes_abstain, "total_votes": total,
            "quorum_reached": total > 0, "voter_count": len(votes),
        }

    def execute_proposal(self, proposal_id: int) -> Dict[str, Any]:
        with self._lock:
            proposal = self._proposals.get(proposal_id)
            if not proposal:
                return {"error": "Proposal not found"}
            proposal.status = ProposalStatus.EXECUTED
        logger.info("Proposal #%d executed", proposal_id)
        return {"proposal_id": proposal_id, "status": "executed"}

    def cancel_proposal(self, proposal_id: int, canceller: str) -> Dict[str, Any]:
        with self._lock:
            proposal = self._proposals.get(proposal_id)
            if not proposal:
                return {"error": "Proposal not found"}
            proposal.status = ProposalStatus.CANCELED
        logger.info("Proposal #%d canceled by %s", proposal_id, canceller[:10])
        return {"proposal_id": proposal_id, "status": "canceled"}

# =============================================================================
# TOKEN ANALYZER
# =============================================================================

class TokenAnalyzer:
    def __init__(self):
        self._token_cache: Dict[str, TokenInfo] = {}
        self._price_cache: Dict[str, float] = {}
        self._lock = threading.Lock()

    def analyze_token(self, address: str, chain: Blockchain) -> Dict[str, Any]:
        with self._lock:
            token = self._token_cache.get(f"{address}_{chain.value}")
        if not token:
            return {"error": "Token not found in cache"}
        price = self._price_cache.get(token.symbol, 0.0)
        return {
            "address": token.address, "name": token.name, "symbol": token.symbol,
            "decimals": token.decimals, "chain": chain.value,
            "total_supply": token.total_supply, "price_usd": price,
            "market_cap": token.total_supply * price if token.total_supply > 0 else 0,
            "verified": token.verified,
        }

    def register_token(self, token: TokenInfo) -> None:
        key = f"{token.address}_{token.chain.value}"
        with self._lock:
            self._token_cache[key] = token
        logger.info("Registered token: %s (%s) on %s", token.name, token.symbol, token.chain.value)

    def set_price(self, symbol: str, price_usd: float) -> None:
        with self._lock:
            self._price_cache[symbol] = price_usd

    def get_price(self, symbol: str) -> float:
        with self._lock:
            return self._price_cache.get(symbol, 0.0)

    def get_tokens_by_chain(self, chain: Blockchain) -> List[TokenInfo]:
        with self._lock:
            return [t for t in self._token_cache.values() if t.chain == chain]

    def calculate_token_metrics(self, symbol: str, holdings: float) -> Dict[str, Any]:
        price = self.get_price(symbol)
        return {
            "symbol": symbol, "holdings": holdings,
            "value_usd": holdings * price, "price_usd": price,
        }

# =============================================================================
# PORTFOLIO TRACKER
# =============================================================================

class PortfolioTracker:
    def __init__(self, wallet_manager: WalletManager):
        self._wallet_manager = wallet_manager
        self._snapshots: List[PortfolioSnapshot] = []
        self._lock = threading.Lock()

    def take_snapshot(self, prices: Dict[str, float]) -> PortfolioSnapshot:
        wallets = self._wallet_manager.get_all_wallets()
        total_value = 0.0
        chain_values: Dict[str, float] = defaultdict(float)
        token_allocations: Dict[str, float] = defaultdict(float)
        for wallet in wallets:
            balance = self._wallet_manager.get_balance(wallet.address)
            if "error" in balance:
                continue
            native = balance.get("native_balance", 0.0)
            currency = CHAIN_CONFIGS.get(wallet.chain, {}).get("native_currency", "ETH")
            native_usd = native * prices.get(currency, 0.0)
            total_value += native_usd
            chain_values[wallet.chain.value] += native_usd
            token_allocations[currency] += native_usd
            for token_symbol, amount in balance.get("tokens", {}).items():
                token_usd = amount * prices.get(token_symbol, 0.0)
                total_value += token_usd
                token_allocations[token_symbol] += token_usd
        snapshot = PortfolioSnapshot(
            timestamp=datetime.now(), total_value_usd=total_value,
            chain_values=dict(chain_values), token_allocations=dict(token_allocations),
        )
        with self._lock:
            self._snapshots.append(snapshot)
        logger.info("Portfolio snapshot: $%.2f across %d chains", total_value, len(chain_values))
        return snapshot

    def get_latest_snapshot(self) -> Optional[PortfolioSnapshot]:
        with self._lock:
            return self._snapshots[-1] if self._snapshots else None

    def get_value_change(self, hours: int = 24) -> Dict[str, Any]:
        with self._lock:
            if len(self._snapshots) < 2:
                return {"change_usd": 0.0, "change_percent": 0.0}
            latest = self._snapshots[-1]
            cutoff = latest.timestamp - timedelta(hours=hours)
            older = None
            for s in reversed(self._snapshots):
                if s.timestamp <= cutoff:
                    older = s
                    break
            if not older:
                older = self._snapshots[0]
        change_usd = latest.total_value_usd - older.total_value_usd
        change_pct = (change_usd / older.total_value_usd * 100) if older.total_value_usd > 0 else 0
        return {"change_usd": change_usd, "change_percent": change_pct, "hours": hours}

    def get_allocation_breakdown(self) -> Dict[str, Any]:
        snapshot = self.get_latest_snapshot()
        if not snapshot:
            return {"allocations": {}, "total_usd": 0.0}
        total = snapshot.total_value_usd
        allocations = {}
        for symbol, value in snapshot.token_allocations.items():
            allocations[symbol] = {"value_usd": value, "percent": (value / total * 100) if total > 0 else 0}
        return {"allocations": allocations, "total_usd": total}

# =============================================================================
# YIELD OPTIMIZER
# =============================================================================

class YieldOptimizer:
    def __init__(self):
        self._positions: Dict[str, YieldPosition] = {}
        self._yield_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def add_position(self, user_address: str, strategy: YieldStrategy,
                     protocol: DeFiProtocol, chain: Blockchain, token: str,
                     amount: float, apy: float) -> YieldPosition:
        position_id = f"{user_address}_{token}_{chain.value}_{strategy.value}"
        risk_map = {
            YieldStrategy.STAKING: RiskLevel.LOW,
            YieldStrategy.LENDING: RiskLevel.LOW,
            YieldStrategy.SINGLE_SIDED: RiskLevel.LOW,
            YieldStrategy.LIQUIDITY_PROVIDING: RiskLevel.MEDIUM,
            YieldStrategy.YIELD_FARMING: RiskLevel.HIGH,
            YieldStrategy.CONCENTRATED_LIQUIDITY: RiskLevel.HIGH,
            YieldStrategy.RESTAKING: RiskLevel.MEDIUM,
            YieldStrategy.VAULT: RiskLevel.MEDIUM,
        }
        position = YieldPosition(
            strategy=strategy, protocol=protocol, chain=chain,
            user_address=user_address, token=token, amount=amount,
            apy=apy, risk_level=risk_map.get(strategy, RiskLevel.MEDIUM),
        )
        with self._lock:
            self._positions[position_id] = position
        logger.info("Yield position added: %s %s on %s (APY: %.1f%%)", amount, token, chain.value, apy)
        return position

    def get_user_positions(self, user_address: str) -> List[YieldPosition]:
        with self._lock:
            return [p for p in self._positions.values() if p.user_address == user_address]

    def calculate_optimal_allocation(self, user_address: str,
                                     risk_tolerance: RiskLevel) -> Dict[str, Any]:
        positions = self.get_user_positions(user_address)
        if not positions:
            return {"allocations": [], "total_apy": 0.0}
        risk_order = list(RiskLevel)
        max_risk_idx = risk_order.index(risk_tolerance)
        suitable = [p for p in positions if risk_order.index(p.risk_level) <= max_risk_idx]
        if not suitable:
            return {"allocations": [], "total_apy": 0.0}
        total_amount = sum(p.amount for p in suitable)
        allocations = []
        for p in suitable:
            allocations.append({
                "token": p.token, "chain": p.chain.value,
                "amount": p.amount, "percent": (p.amount / total_amount * 100) if total_amount > 0 else 0,
                "apy": p.apy, "strategy": p.strategy.name,
            })
        weighted_apy = sum(p.apy * p.amount for p in suitable) / total_amount if total_amount > 0 else 0
        return {"allocations": allocations, "total_apy": weighted_apy, "total_amount": total_amount}

    def estimate_daily_yield(self, user_address: str) -> Dict[str, Any]:
        positions = self.get_user_positions(user_address)
        total_daily = 0.0
        by_token: Dict[str, float] = defaultdict(float)
        for p in positions:
            daily = p.amount * (p.apy / 100 / 365)
            total_daily += daily
            by_token[p.token] += daily
        return {"total_daily_yield": total_daily, "by_token": dict(by_token)}

# =============================================================================
# MEV PROTECTOR
# =============================================================================

class MEVProtector:
    def __init__(self):
        self._bundles: Dict[str, MEVBundle] = {}
        self._bundle_history: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def create_bundle(self, chain: Blockchain, transactions: List[Dict[str, Any]],
                      target_block: int, mode: MEVProtectionMode = MEVProtectionMode.PRIVATE_MEMPOOL) -> MEVBundle:
        bundle_id = str(uuid.uuid4())[:8]
        bundle = MEVBundle(
            bundle_id=bundle_id, transactions=transactions,
            chain=chain, target_block=target_block,
            protection_mode=mode,
        )
        with self._lock:
            self._bundles[bundle_id] = bundle
        logger.info("MEV bundle created: %s (mode: %s)", bundle_id, mode.name)
        return bundle

    def submit_bundle(self, bundle_id: str) -> Dict[str, Any]:
        with self._lock:
            bundle = self._bundles.get(bundle_id)
            if not bundle:
                return {"error": "Bundle not found"}
            bundle.status = "submitted"
        logger.info("MEV bundle submitted: %s", bundle_id)
        return {"bundle_id": bundle_id, "status": "submitted", "mode": bundle.protection_mode.name}

    def get_bundle(self, bundle_id: str) -> Optional[MEVBundle]:
        with self._lock:
            return self._bundles.get(bundle_id)

    def get_pending_bundles(self, chain: Optional[Blockchain] = None) -> List[MEVBundle]:
        with self._lock:
            bundles = [b for b in self._bundles.values() if b.status in ("pending", "submitted")]
        if chain:
            bundles = [b for b in bundles if b.chain == chain]
        return bundles

    def estimate_mev_savings(self, transaction_value_usd: float) -> Dict[str, Any]:
        baseline_loss = transaction_value_usd * 0.005
        protected_loss = transaction_value_usd * 0.0001
        savings = baseline_loss - protected_loss
        return {
            "baseline_mev_loss_usd": baseline_loss,
            "protected_mev_loss_usd": protected_loss,
            "savings_usd": savings,
            "savings_percent": (savings / baseline_loss * 100) if baseline_loss > 0 else 0,
        }

# =============================================================================
# MULTI-SIG WALLET
# =============================================================================

class MultiSigWallet:
    def __init__(self):
        self._wallets: Dict[str, Dict[str, Any]] = {}
        self._transactions: Dict[str, List[MultiSigTransaction]] = defaultdict(list)
        self._lock = threading.Lock()

    def create_multisig(self, chain: Blockchain, owners: List[str],
                        required_signatures: int, name: str = "") -> Dict[str, Any]:
        multisig_id = str(uuid.uuid4())[:8]
        address = "0x" + hashlib.sha256(f"multisig_{multisig_id}".encode()).hexdigest()[:40]
        config = {
            "id": multisig_id, "address": address, "chain": chain.value,
            "owners": owners, "required_signatures": required_signatures,
            "name": name or f"Multisig-{multisig_id}", "created_at": datetime.now().isoformat(),
        }
        with self._lock:
            self._wallets[multisig_id] = config
        logger.info("Created multisig %s with %d owners (require %d signatures)", multisig_id, len(owners), required_signatures)
        return config

    def submit_transaction(self, multisig_id: str, proposer: str,
                           destination: str, value: float, data: str = "") -> Optional[MultiSigTransaction]:
        with self._lock:
            config = self._wallets.get(multisig_id)
            if not config:
                return None
            tx_id = str(uuid.uuid4())[:8]
            tx = MultiSigTransaction(
                tx_id=tx_id, contract_address=config["address"],
                chain=Blockchain(config["chain"]), proposer=proposer,
                destination=destination, value=value, data=data,
                required_signatures=config["required_signatures"],
                confirmations=[proposer],
            )
            self._transactions[multisig_id].append(tx)
        logger.info("Multisig tx %s submitted by %s", tx_id, proposer[:10])
        return tx

    def confirm_transaction(self, multisig_id: str, tx_id: str, signer: str) -> Dict[str, Any]:
        with self._lock:
            txs = self._transactions.get(multisig_id, [])
            tx = None
            for t in txs:
                if t.tx_id == tx_id:
                    tx = t
                    break
            if not tx:
                return {"error": "Transaction not found"}
            if signer in tx.confirmations:
                return {"error": "Already confirmed"}
            config = self._wallets.get(multisig_id)
            if signer not in (config or {}).get("owners", []):
                return {"error": "Signer not an owner"}
            tx.confirmations.append(signer)
            sufficient = len(tx.confirmations) >= tx.required_signatures
        logger.info("Multisig tx %s confirmed by %s (%d/%d)", tx_id, signer[:10], len(tx.confirmations), tx.required_signatures)
        return {"tx_id": tx_id, "confirmations": len(tx.confirmations), "required": tx.required_signatures, "sufficient": sufficient}

    def get_pending_transactions(self, multisig_id: str) -> List[MultiSigTransaction]:
        with self._lock:
            return [t for t in self._transactions.get(multisig_id, []) if not t.executed]

    def get_multisig(self, multisig_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._wallets.get(multisig_id)

# =============================================================================
# CONTRACT AUDIT HELPER
# =============================================================================

class ContractAuditHelper:
    def __init__(self):
        self._reports: Dict[str, AuditReport] = {}
        self._lock = threading.Lock()

    def start_audit(self, contract_address: str, chain: Blockchain, auditor: str) -> AuditReport:
        report = AuditReport(
            contract_address=contract_address, chain=chain,
            auditor=auditor, status=AuditStatus.IN_PROGRESS,
        )
        with self._lock:
            self._reports[f"{contract_address}_{chain.value}"] = report
        logger.info("Audit started for %s on %s by %s", contract_address[:10], chain.value, auditor)
        return report

    def add_finding(self, contract_address: str, chain: Blockchain,
                    severity: str, description: str) -> bool:
        key = f"{contract_address}_{chain.value}"
        with self._lock:
            report = self._reports.get(key)
            if not report:
                return False
            report.findings_count += 1
            if severity == "critical":
                report.critical_count += 1
            elif severity == "high":
                report.high_count += 1
            elif severity == "medium":
                report.medium_count += 1
            elif severity == "low":
                report.low_count += 1
            else:
                report.informational_count += 1
            report.recommendations.append(f"[{severity.upper()}] {description}")
        return True

    def complete_audit(self, contract_address: str, chain: Blockchain,
                       status: AuditStatus = AuditStatus.PASSED) -> Optional[AuditReport]:
        key = f"{contract_address}_{chain.value}"
        with self._lock:
            report = self._reports.get(key)
            if not report:
                return None
            report.status = status
            report.completed_at = datetime.now()
        logger.info("Audit completed for %s: %s (findings: %d)", contract_address[:10], status.name, report.findings_count)
        return report

    def get_report(self, contract_address: str, chain: Blockchain) -> Optional[AuditReport]:
        key = f"{contract_address}_{chain.value}"
        with self._lock:
            return self._reports.get(key)

    def get_all_reports(self, status_filter: Optional[AuditStatus] = None) -> List[AuditReport]:
        with self._lock:
            reports = list(self._reports.values())
        if status_filter:
            reports = [r for r in reports if r.status == status_filter]
        return reports

    def get_risk_summary(self, contract_address: str, chain: Blockchain) -> Dict[str, Any]:
        report = self.get_report(contract_address, chain)
        if not report:
            return {"error": "Report not found"}
        return {
            "total_findings": report.findings_count,
            "critical": report.critical_count,
            "high": report.high_count,
            "medium": report.medium_count,
            "low": report.low_count,
            "informational": report.informational_count,
            "status": report.status.name,
            "risk_score": report.critical_count * 10 + report.high_count * 5 + report.medium_count * 2 + report.low_count * 1,
        }

# =============================================================================
# CONFIG
# =============================================================================

class Config:
    def __init__(self, default_chain: Blockchain = Blockchain.ETHEREUM,
                 network_type: NetworkType = NetworkType.MAINNET,
                 gas_limit_buffer: float = 1.2, slippage_tolerance: float = 0.5,
                 ipfs_gateway: str = "https://ipfs.io", pinata_api_key: str = "",
                 rpc_urls: Optional[Dict[Blockchain, str]] = None):
        self.default_chain = default_chain
        self.network_type = network_type
        self.gas_limit_buffer = gas_limit_buffer
        self.slippage_tolerance = slippage_tolerance
        self.ipfs_gateway = ipfs_gateway
        self.pinata_api_key = pinata_api_key
        self.rpc_urls = rpc_urls or {}

# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class CryptoWeb3Agent:
    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._wallet_manager = WalletManager()
        self._contract_manager = SmartContractManager()
        self._defi_manager = DeFiManager(self._wallet_manager)
        self._nft_manager = NFTManager(self._wallet_manager, self._contract_manager)
        self._storage_manager = StorageManager()
        self._gas_optimizer = GasOptimizer()
        self._bridge_manager = BridgeManager(self._wallet_manager)
        self._dao_manager = DAOManager()
        self._token_analyzer = TokenAnalyzer()
        self._portfolio_tracker = PortfolioTracker(self._wallet_manager)
        self._yield_optimizer = YieldOptimizer()
        self._mev_protector = MEVProtector()
        self._multisig = MultiSigWallet()
        self._audit_helper = ContractAuditHelper()
        self._running = False
        self._lock = threading.Lock()

    def initialize(self) -> Dict[str, Any]:
        logger.info("Initializing CryptoWeb3Agent")
        self._running = True
        return {"status": "initialized", "default_chain": self._config.default_chain.value,
                "network": self._config.network_type.name}

    def shutdown(self) -> Dict[str, Any]:
        self._running = False
        logger.info("CryptoWeb3Agent shutdown complete")
        return {"status": "shutdown"}

    def create_wallet(self, chain: Blockchain, name: Optional[str] = None) -> Dict[str, Any]:
        wallet = self._wallet_manager.create_wallet(chain, name)
        return {"address": wallet.address, "chain": wallet.chain.value, "name": wallet.name}

    def get_wallet_balance(self, address: str) -> Dict[str, Any]:
        return self._wallet_manager.get_balance(address)

    def transfer(self, from_address: str, to_address: str, amount: float,
                 token: str = "ETH", chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        tx = self._wallet_manager.transfer(from_address, to_address, amount, token, chain)
        return {"tx_hash": tx.tx_hash, "status": tx.status.name, "value": tx.value}

    def get_transaction_history(self, address: str, limit: int = 50) -> List[Dict[str, Any]]:
        txs = self._wallet_manager.get_transaction_history(address, limit)
        return [{"tx_hash": t.tx_hash, "from": t.from_address, "to": t.to_address,
                 "value": t.value, "status": t.status.name, "chain": t.chain.value}
                for t in txs]

    def deploy_contract(self, source_code: str, name: str, chain: Blockchain,
                        deployer: str, contract_type: ContractType = ContractType.CUSTOM) -> Dict[str, Any]:
        compiled = self._contract_manager.compile_contract(source_code, name)
        contract = self._contract_manager.deploy(
            compiled["bytecode"], compiled["abi"], chain, deployer, name,
        )
        return {"address": contract.address, "chain": chain.value, "name": name, "deployer": deployer}

    def deploy_erc20(self, name: str, symbol: str, chain: Blockchain,
                     deployer: str, total_supply: float = 1000000) -> Dict[str, Any]:
        contract = self._contract_manager.deploy_erc20(name, symbol, 18, total_supply, chain, deployer)
        return {"address": contract.address, "chain": chain.value, "name": name, "symbol": symbol}

    def deploy_erc721(self, name: str, symbol: str, chain: Blockchain, deployer: str) -> Dict[str, Any]:
        contract = self._contract_manager.deploy_erc721(name, symbol, f"ipfs://{name}/", chain, deployer)
        return {"address": contract.address, "chain": chain.value, "name": name, "symbol": symbol}

    def get_swap_quote(self, token_in: str, token_out: str, amount: float,
                       chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        quote = self._defi_manager.get_swap_quote(token_in, token_out, amount, chain)
        return {"token_in": quote.token_in, "token_out": quote.token_out,
                "amount_in": quote.amount_in, "amount_out": quote.amount_out,
                "price_impact": quote.price_impact, "gas_estimate": quote.gas_estimate}

    def execute_swap(self, user: str, token_in: str, token_out: str, amount: float,
                     chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        tx = self._defi_manager.execute_swap(user, token_in, token_out, amount, 0, chain)
        return {"tx_hash": tx.tx_hash, "status": tx.status.name}

    def add_liquidity(self, user: str, token_a: str, token_b: str,
                      amount_a: float, amount_b: float,
                      chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        pos = self._defi_manager.add_liquidity(user, token_a, token_b, amount_a, amount_b, chain)
        return {"token_a": pos.token_a, "token_b": pos.token_b,
                "amount_a": pos.amount_a, "amount_b": pos.amount_b, "apr": pos.apr}

    def stake(self, user: str, validator: str, amount: float,
              chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        pos = self._defi_manager.stake(user, validator, amount, chain)
        return {"validator": pos.validator, "amount": pos.amount, "apr": pos.apr}

    def mint_nft(self, contract: str, chain: Blockchain, recipient: str,
                 name: str, image_url: str, description: str = "",
                 royalty: float = 5.0) -> Dict[str, Any]:
        nft = self._nft_manager.mint_nft(contract, chain, recipient, name, description, image_url, "", royalty)
        return {"token_id": nft.token_id, "owner": nft.owner, "name": nft.name}

    def list_nft(self, contract: str, token_id: int, seller: str, price: float,
                 chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        return self._nft_manager.list_nft(contract, token_id, seller, price, chain=chain)

    def buy_nft(self, contract: str, token_id: int, buyer: str,
                chain: Blockchain = Blockchain.ETHEREUM) -> Dict[str, Any]:
        return self._nft_manager.buy_nft(contract, token_id, buyer, chain)

    def store_on_ipfs(self, data: bytes, name: str) -> Dict[str, Any]:
        meta = self._storage_manager.upload_to_ipfs(data, name)
        return {"cid": meta.cid, "gateway_url": meta.gateway_url, "size": meta.size_bytes}

    def store_nft_metadata(self, name: str, description: str, image_url: str,
                           attributes: List[Dict[str, Any]]) -> Dict[str, Any]:
        meta = self._storage_manager.store_nft_metadata(name, description, image_url, attributes)
        return {"cid": meta.cid, "gateway_url": meta.gateway_url}

    def get_gas_estimate(self, chain: Blockchain, method: str) -> Dict[str, Any]:
        est = self._gas_optimizer.get_gas_estimate(chain, method)
        return {"gas_limit": est.gas_limit, "gas_price_gwei": est.gas_price_gwei,
                "estimated_cost": est.estimated_cost_native}

    def suggest_gas_price(self, chain: Blockchain) -> Dict[str, float]:
        return self._gas_optimizer.suggest_gas_price(chain)

    def bridge_tokens(self, user: str, source: Blockchain, dest: Blockchain,
                      token: str, amount: float) -> Dict[str, Any]:
        return self._bridge_manager.execute_bridge(user, source, dest, token, amount)

    def create_proposal(self, chain: Blockchain, governor: str, proposer: str,
                        title: str, description: str = "") -> Dict[str, Any]:
        proposal = self._dao_manager.create_proposal(chain, governor, proposer, title, description)
        return {"proposal_id": proposal.proposal_id, "title": proposal.title, "status": proposal.status.name}

    def cast_vote(self, proposal_id: int, voter: str, support: str, weight: float = 1.0) -> Dict[str, Any]:
        return self._dao_manager.cast_vote(proposal_id, voter, support, weight)

    def get_proposal_results(self, proposal_id: int) -> Dict[str, Any]:
        return self._dao_manager.get_vote_results(proposal_id)

    def get_status(self) -> Dict[str, Any]:
        wallets = self._wallet_manager.get_all_wallets()
        contracts = self._contract_manager.get_all_contracts()
        return {
            "agent": "CryptoWeb3Agent", "running": self._running,
            "wallets_count": len(wallets), "contracts_count": len(contracts),
            "default_chain": self._config.default_chain.value,
            "network": self._config.network_type.name,
        }

    def get_full_report(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(), "status": self.get_status(),
            "storage_stats": self._storage_manager.get_storage_stats(),
            "deployment_history": self._contract_manager.get_deployment_history(),
        }

# =============================================================================
# ASYNC WRAPPER
# =============================================================================

class AsyncCryptoWeb3Agent:
    def __init__(self, config: Optional[Config] = None):
        self._agent = CryptoWeb3Agent(config)

    async def initialize(self) -> Dict[str, Any]:
        return self._agent.initialize()

    async def shutdown(self) -> Dict[str, Any]:
        return self._agent.shutdown()

    async def create_wallet(self, chain: Blockchain, name: Optional[str] = None) -> Dict[str, Any]:
        return self._agent.create_wallet(chain, name)

    async def get_full_report(self) -> Dict[str, Any]:
        return self._agent.get_full_report()

# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    print("=" * 60)
    print("  Crypto/Web3 Agent - Comprehensive Demo")
    print("=" * 60)
    agent = CryptoWeb3Agent(Config(default_chain=Blockchain.ETHEREUM))
    agent.initialize()
    wallet_a = agent.create_wallet(Blockchain.ETHEREUM, "Alice")
    wallet_b = agent.create_wallet(Blockchain.ETHEREUM, "Bob")
    agent._wallet_manager.set_balance(wallet_a["address"], 10.0)
    agent._wallet_manager.set_balance(wallet_b["address"], 5.0)
    print(f"\nWallets: {wallet_a['address'][:12]}... ({wallet_a['name']}), {wallet_b['address'][:12]}... ({wallet_b['name']})")
    tx = agent.transfer(wallet_a["address"], wallet_b["address"], 1.0, "ETH")
    print(f"Transfer: {tx['tx_hash'][:16]}... | Status: {tx['status']}")
    contract = agent.deploy_erc20("MyToken", "MTK", Blockchain.ETHEREUM, wallet_a["address"])
    print(f"Deployed ERC20: {contract['address'][:12]}... ({contract['name']})")
    nft_contract = agent.deploy_erc721("ArtCollection", "ART", Blockchain.ETHEREUM, wallet_a["address"])
    nft = agent.mint_nft(nft_contract["address"], Blockchain.ETHEREUM, wallet_b["address"], "Cool Art", "ipfs://art.png")
    print(f"Minted NFT: #{nft['token_id']} owned by {nft['owner'][:12]}...")
    quote = agent.get_swap_quote("ETH", "USDC", 1.0)
    print(f"Swap Quote: {quote['amount_in']} ETH -> {quote['amount_out']:.2f} USDC")
    gas = agent.get_gas_estimate(Blockchain.ETHEREUM, "swap")
    print(f"Gas Estimate: {gas['gas_limit']} gas @ {gas['gas_price_gwei']:.1f} gwei")
    proposal = agent.create_proposal(Blockchain.ETHEREUM, "0x" + "1"*40, wallet_a["address"], "Increase LP Rewards")
    vote = agent.cast_vote(proposal["proposal_id"], wallet_b["address"], "for")
    results = agent.get_proposal_results(proposal["proposal_id"])
    print(f"Proposal #{proposal['proposal_id']}: {results['votes_for']} for, {results['votes_against']} against")
    report = agent.get_full_report()
    print(f"\nReport: {report['status']['wallets_count']} wallets, {report['status']['contracts_count']} contracts")
    agent.shutdown()
    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
