"""
Wallet Integration Module
Connection, SIWE auth, transaction building, chains, and security.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class WalletType(Enum):
    METAMASK = "metamask"
    WALLETCONNECT = "walletconnect"
    COINBASE = "coinbase"
    PHANTOM = "phantom"
    RAINBOW = "rainbow"
    LEDGER = "ledger"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class WalletConnection:
    """Wallet connection result."""
    address: str
    chain_id: int
    wallet_type: str
    balance_eth: float = 0.0
    connected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_hardware: bool = False


@dataclass
class Transaction:
    """Built transaction."""
    from_address: str
    to_address: str
    value: float
    chain_id: int
    gas_estimate: int = 21000
    gas_price_gwei: float = 20.0
    nonce: int = 0
    data: str = "0x"
    tx_hash: str = ""

    @property
    def max_fee_eth(self) -> float:
        return self.gas_estimate * self.gas_price_gwei / 1e9


@dataclass
class SIWEMessage:
    """Sign-In with Ethereum message."""
    address: str
    domain: str
    uri: str
    chain_id: int
    statement: str
    nonce: str = ""
    issued_at: str = ""

    def to_message(self) -> str:
        return (
            f"{self.domain} wants you to sign in with your Ethereum account:\n"
            f"{self.address}\n\n"
            f"{self.statement}\n\n"
            f"URI: {self.uri}\n"
            f"Chain ID: {self.chain_id}\n"
            f"Nonce: {self.nonce}\n"
            f"Issued At: {self.issued_at}"
        )


@dataclass
class ChainInfo:
    """Blockchain chain information."""
    chain_id: int
    name: str
    rpc_url: str
    explorer_url: str
    native_currency: str = "ETH"
    is_testnet: bool = False


@dataclass
class AddressRisk:
    """Address risk assessment."""
    address: str
    risk_level: RiskLevel
    is_contract: bool = False
    is_known_scammer: bool = False
    has_high_tx_volume: bool = False
    risk_factors: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Wallet Connector
# ---------------------------------------------------------------------------

class WalletConnector:
    """Connect and manage wallets."""

    def __init__(self):
        self._connections: Dict[str, WalletConnection] = {}

    def connect(
        self,
        wallet_type: str = "metamask",
        chain_id: int = 1,
    ) -> WalletConnection:
        address = f"0x{secrets.token_hex(20)}"
        connection = WalletConnection(
            address=address,
            chain_id=chain_id,
            wallet_type=wallet_type,
            balance_eth=round(secrets.randbelow(10000) / 1000, 4),
        )
        self._connections[address] = connection
        return connection

    def get_connection(self, address: str) -> Optional[WalletConnection]:
        return self._connections.get(address)

    def disconnect(self, address: str) -> bool:
        if address in self._connections:
            del self._connections[address]
            return True
        return False

    def get_balance(self, address: str) -> float:
        conn = self._connections.get(address)
        return conn.balance_eth if conn else 0.0


# ---------------------------------------------------------------------------
# Transaction Builder
# ---------------------------------------------------------------------------

class TransactionBuilder:
    """Build and manage transactions."""

    def __init__(self, chain_id: int = 1):
        self.chain_id = chain_id
        self._nonce: Dict[str, int] = {}

    def build_transfer(
        self,
        from_address: str,
        to_address: str,
        value_eth: float,
        gas_price_gwei: float = 20.0,
        nonce: Optional[int] = None,
    ) -> Transaction:
        if nonce is None:
            nonce = self._nonce.get(from_address, 0)
            self._nonce[from_address] = nonce + 1
        tx_hash = f"0x{secrets.token_hex(32)}"
        return Transaction(
            from_address=from_address,
            to_address=to_address,
            value=value_eth,
            chain_id=self.chain_id,
            gas_estimate=21000,
            gas_price_gwei=gas_price_gwei,
            nonce=nonce,
            tx_hash=tx_hash,
        )

    def build_contract_call(
        self,
        from_address: str,
        to_address: str,
        data: str,
        value_eth: float = 0,
        gas_limit: int = 100000,
        gas_price_gwei: float = 20.0,
    ) -> Transaction:
        nonce = self._nonce.get(from_address, 0)
        self._nonce[from_address] = nonce + 1
        return Transaction(
            from_address=from_address,
            to_address=to_address,
            value=value_eth,
            chain_id=self.chain_id,
            gas_estimate=gas_limit,
            gas_price_gwei=gas_price_gwei,
            nonce=nonce,
            data=data,
            tx_hash=f"0x{secrets.token_hex(32)}",
        )

    def estimate_gas(
        self, from_addr: str, to_addr: str, value: float, data: str = "0x"
    ) -> int:
        if data == "0x" or not data:
            return 21000
        return 100000 + len(data) * 16


# ---------------------------------------------------------------------------
# SIWE Authentication
# ---------------------------------------------------------------------------

class SIWEAuth:
    """Sign-In with Ethereum authentication."""

    def __init__(self):
        self._nonces: Dict[str, str] = {}

    def create_message(
        self,
        address: str,
        domain: str,
        uri: str,
        chain_id: int = 1,
        statement: str = "Sign in to access your account",
    ) -> str:
        nonce = secrets.token_hex(16)
        self._nonces[address] = nonce
        msg = SIWEMessage(
            address=address,
            domain=domain,
            uri=uri,
            chain_id=chain_id,
            statement=statement,
            nonce=nonce,
            issued_at=datetime.now(timezone.utc).isoformat(),
        )
        return msg.to_message()

    def verify_nonce(self, address: str, nonce: str) -> bool:
        return self._nonces.get(address) == nonce


# ---------------------------------------------------------------------------
# Chain Manager
# ---------------------------------------------------------------------------

class ChainManager:
    """Manage blockchain networks."""

    SUPPORTED_CHAINS = [
        ChainInfo(1, "Ethereum", "https://rpc.ankr.com/eth", "https://etherscan.io"),
        ChainInfo(137, "Polygon", "https://rpc.ankr.com/polygon", "https://polygonscan.com"),
        ChainInfo(42161, "Arbitrum", "https://rpc.ankr.com/arbitrum", "https://arbiscan.io"),
        ChainInfo(10, "Optimism", "https://rpc.ankr.com/optimism", "https://optimistic.etherscan.io"),
        ChainInfo(8453, "Base", "https://mainnet.base.org", "https://basescan.org"),
        ChainInfo(56, "BNB Chain", "https://rpc.ankr.com/bsc", "https://bscscan.com"),
    ]

    def get_supported_chains(self) -> List[Dict[str, Any]]:
        return [
            {"chain_id": c.chain_id, "name": c.name, "currency": c.native_currency}
            for c in self.SUPPORTED_CHAINS
        ]

    def switch_chain(self, chain_id: int) -> Optional[Dict[str, Any]]:
        chain = next((c for c in self.SUPPORTED_CHAINS if c.chain_id == chain_id), None)
        if chain:
            return {"chain_id": chain.chain_id, "name": chain.name, "rpc": chain.rpc_url}
        return None

    def get_chain_info(self, chain_id: int) -> Optional[ChainInfo]:
        return next((c for c in self.SUPPORTED_CHAINS if c.chain_id == chain_id), None)


# ---------------------------------------------------------------------------
# Security Checker
# ---------------------------------------------------------------------------

class SecurityChecker:
    """Check address and transaction security."""

    KNOWN_CONTRACTS = {"0x1234", "0xabcd"}

    def check_address(self, address: str) -> AddressRisk:
        is_contract = address.lower() in self.KNOWN_CONTRACTS
        risk_factors: List[str] = []
        if is_contract:
            risk_factors.append("Contract address")
        risk_level = RiskLevel.LOW
        if len(risk_factors) > 2:
            risk_level = RiskLevel.HIGH
        elif len(risk_factors) > 0:
            risk_level = RiskLevel.MEDIUM
        return AddressRisk(
            address=address,
            risk_level=risk_level,
            is_contract=is_contract,
            risk_factors=risk_factors,
        )

    def simulate_transaction(self, tx: Transaction) -> Dict[str, Any]:
        return {
            "success": True,
            "gas_used": tx.gas_estimate,
            "value": tx.value,
            "to": tx.to_address,
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Wallet Integration Demo")
    print("=" * 60)

    print("\n[1] Wallet Connection")
    connector = WalletConnector()
    wallet = connector.connect("metamask", 1)
    print(f"  Address: {wallet.address}")
    print(f"  Chain: {wallet.chain_id}")
    print(f"  Balance: {wallet.balance_eth} ETH")

    print("\n[2] Transaction Building")
    builder = TransactionBuilder(1)
    tx = builder.build_transfer(wallet.address, "0xABCD", 0.1, 20, 0)
    print(f"  Tx hash: {tx.tx_hash[:20]}...")
    print(f"  Gas estimate: {tx.gas_estimate}")
    print(f"  Max fee: {tx.max_fee_eth:.6f} ETH")

    print("\n[3] SIWE Authentication")
    siwe = SIWEAuth()
    message = siwe.create_message(wallet.address, "app.example.com", "https://app.example.com", 1)
    print(f"  Message:\n{message[:200]}...")

    print("\n[4] Chain Management")
    chains = ChainManager()
    supported = chains.get_supported_chains()
    print(f"  Supported: {len(supported)} chains")
    chain = chains.switch_chain(137)
    print(f"  Switched to: {chain['name']}")

    print("\n[5] Security Check")
    security = SecurityChecker()
    risk = security.check_address(wallet.address)
    print(f"  Risk: {risk.risk_level.value}")
    print(f"  Factors: {risk.risk_factors}")
    sim = security.simulate_transaction(tx)
    print(f"  Simulation: {sim}")

    print("\n" + "=" * 60)
    print("  Wallet integration demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
