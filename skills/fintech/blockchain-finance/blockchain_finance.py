"""
Blockchain Finance Module
Part of the fintech skill domain

Provides token issuance, AMM operations, DeFi lending, yield optimization,
institutional custody, and regulatory compliance for blockchain-based finance.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import hashlib


class TokenType(Enum):
    ERC20 = "erc20"
    ERC721 = "erc721"
    ERC1155 = "erc1155"
    SPL = "spl"


class Network(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    BASE = "base"
    SOLANA = "solana"


class WalletTier(Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class TransactionStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    BRIDGING = "bridging"


@dataclass
class ComplianceConfig:
    kyc_required: bool = True
    transfer_restricted: bool = False
    max_holders: int = 10000
    jurisdiction_allowlist: List[str] = field(default_factory=list)


@dataclass
class TokenDeployment:
    contract_address: str
    deployment_tx: str
    network: str
    explorer_url: str
    name: str
    symbol: str
    total_supply: float
    token_type: TokenType


@dataclass
class LiquidityPosition:
    position_id: str
    pool_address: str
    token_a: str
    token_b: str
    fee_tier: float
    price_lower: float
    price_upper: float
    liquidity: float
    amount_a: float
    amount_b: float
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ImpermanentLoss:
    percentage: float
    usd_value: float
    hold_value: float
    lp_value: float


@dataclass
class SupplyResult:
    tx_hash: str
    asset: str
    amount: float
    apy: float
    wallet: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class BorrowResult:
    tx_hash: str
    asset: str
    amount: float
    collateral_asset: str
    collateral_amount: float
    health_factor: float
    liquidation_price: float
    interest_rate: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class YieldAllocation:
    protocol: str
    percentage: float
    apy: float
    risk_score: float
    asset: str
    tvl: float


@dataclass
class YieldStrategy:
    allocations: List[YieldAllocation]
    expected_apy: float
    estimated_gas_usd: float
    rebalance_frequency_days: int
    risk_score: float


@dataclass
class WalletAddress:
    address: str
    tier: WalletTier
    network: str
    balance: float = 0.0
    last_active: str = ""


class TokenIssuer:
    """Token deployment and compliance management."""

    def __init__(self, network: str = "ethereum", compliance: Optional[ComplianceConfig] = None):
        self.network = network
        self.compliance = compliance or ComplianceConfig()
        self._tokens: Dict[str, TokenDeployment] = {}

    def deploy(
        self, name: str, symbol: str, total_supply: float,
        token_type: TokenType = TokenType.ERC20,
        decimals: int = 18, base_uri: str = "",
    ) -> TokenDeployment:
        addr = f"0x{hashlib.sha256(f'{name}{symbol}{datetime.now().isoformat()}'.encode()).hexdigest()[:40]}"
        tx = f"0x{hashlib.sha256(b'deploy').hexdigest()[:64]}"

        deployment = TokenDeployment(
            contract_address=addr, deployment_tx=tx,
            network=self.network,
            explorer_url=f"https://{self.network}.etherscan.io/token/{addr}",
            name=name, symbol=symbol, total_supply=total_supply,
            token_type=token_type,
        )
        self._tokens[addr] = deployment
        return deployment

    def get_token(self, address: str) -> Optional[TokenDeployment]:
        return self._tokens.get(address)


class AMMManager:
    """Automated Market Maker liquidity management."""

    def __init__(self, protocol: str = "uniswap_v3", rpc_url: str = ""):
        self.protocol = protocol
        self.rpc_url = rpc_url
        self._positions: Dict[str, LiquidityPosition] = {}

    def create_position(
        self, token_a: str, token_b: str, fee_tier: float,
        price_range: Tuple[float, float],
        amount_a: float, amount_b: float,
    ) -> LiquidityPosition:
        pos_id = f"LP-{uuid.uuid4().hex[:10].upper()}"
        position = LiquidityPosition(
            position_id=pos_id,
            pool_address=f"0x{hashlib.sha256(f'{token_a}{token_b}'.encode()).hexdigest()[:40]}",
            token_a=token_a, token_b=token_b, fee_tier=fee_tier,
            price_lower=price_range[0], price_range=price_range[1],
            liquidity=amount_a * amount_b,
            amount_a=amount_a, amount_b=amount_b,
        )
        self._positions[pos_id] = position
        return position

    def calculate_impermanent_loss(self, position: LiquidityPosition) -> ImpermanentLoss:
        price_ratio = position.price_upper / position.price_lower
        il_pct = 2 * (price_ratio ** 0.5 / (1 + price_ratio)) - 1
        hold_value = position.amount_a * position.price_lower + position.amount_b * position.price_upper
        lp_value = hold_value * (1 + il_pct)
        return ImpermanentLoss(
            percentage=abs(il_pct),
            usd_value=abs(hold_value - lp_value),
            hold_value=hold_value,
            lp_value=lp_value,
        )

    def get_position(self, position_id: str) -> Optional[LiquidityPosition]:
        return self._positions.get(position_id)


class LendingProtocol:
    """DeFi lending and borrowing operations."""

    def __init__(self, protocol: str = "aave_v3", risk_model: str = "conservative"):
        self.protocol = protocol
        self.risk_model = risk_model

    def supply(self, asset: str, amount: float, wallet: str) -> SupplyResult:
        return SupplyResult(
            tx_hash=f"0x{hashlib.sha256(f'supply{amount}'.encode()).hexdigest()[:64]}",
            asset=asset, amount=amount, apy=0.045, wallet=wallet,
        )

    def borrow(
        self, asset: str, amount: float,
        collateral_asset: str, collateral_amount: float,
    ) -> BorrowResult:
        health = collateral_amount * 0.5 / (amount * 2000) if amount > 0 else 0
        return BorrowResult(
            tx_hash=f"0x{hashlib.sha256(f'borrow{amount}'.encode()).hexdigest()[:64]}",
            asset=asset, amount=amount,
            collateral_asset=collateral_asset,
            collateral_amount=collateral_amount,
            health_factor=round(max(health, 1.0), 2),
            liquidation_price=round(2000 * health * 0.8, 2),
            interest_rate=0.035,
        )

    def get_health_factor(self, wallet: str) -> float:
        return 1.85


class YieldOptimizer:
    """Cross-protocol yield optimization."""

    def __init__(self, risk_tolerance: str = "moderate",
                 max_gas_price_gwei: float = 50,
                 rebalance_threshold_pct: float = 0.5):
        self.risk_tolerance = risk_tolerance
        self.max_gas = max_gas_price_gwei
        self.rebalance_threshold = rebalance_threshold_pct

    def optimize(
        self, capital: float,
        preferred_assets: Optional[List[str]] = None,
        exclude_protocols: Optional[List[str]] = None,
    ) -> YieldStrategy:
        assets = preferred_assets or ["USDC"]
        allocations = [
            YieldAllocation("Aave V3", 0.35, 0.045, 0.15, "USDC", 8_500_000_000),
            YieldAllocation("Compound V3", 0.25, 0.042, 0.12, "USDC", 3_200_000_000),
            YieldAllocation("Maker DSR", 0.20, 0.050, 0.10, "DAI", 5_100_000_000),
            YieldAllocation("Ethena sUSDe", 0.20, 0.150, 0.35, "USDe", 2_800_000_000),
        ]
        expected_apy = sum(a.percentage * a.apy for a in allocations)
        risk_score = sum(a.percentage * a.risk_score for a in allocations)
        return YieldStrategy(
            allocations=allocations,
            expected_apy=round(expected_apy, 4),
            estimated_gas_usd=12.50,
            rebalance_frequency_days=7,
            risk_score=round(risk_score, 2),
        )


class InstitutionalCustody:
    """Multi-signature wallet management for institutional custody."""

    def __init__(self, required_signers: int = 3, total_signers: int = 5):
        self.required = required_signers
        self.total = total_signers
        self._wallets: Dict[str, WalletAddress] = {}

    def create_wallet(self, tier: WalletTier, network: str = "ethereum") -> WalletAddress:
        addr = f"0x{hashlib.sha256(f'{tier.value}{network}'.encode()).hexdigest()[:40]}"
        wallet = WalletAddress(address=addr, tier=tier, network=network)
        self._wallets[addr] = wallet
        return wallet

    def get_wallets(self, tier: Optional[WalletTier] = None) -> List[WalletAddress]:
        wallets = list(self._wallets.values())
        if tier:
            wallets = [w for w in wallets if w.tier == tier]
        return wallets


def main():
    print("=" * 60)
    print("  Blockchain Finance Demo")
    print("=" * 60)

    # Token issuance
    print("\n--- Token Issuance ---")
    issuer = TokenIssuer(network="ethereum", compliance=ComplianceConfig(kyc_required=True))
    token = issuer.deploy("Real Estate Fund", "REFT", 1_000_000)
    print(f"  Address: {token.contract_address[:20]}...")
    print(f"  Explorer: {token.explorer_url[:50]}...")

    # AMM
    print("\n--- AMM Liquidity ---")
    amm = AMMManager()
    pos = amm.create_position("USDC", "WETH", 0.003, (1800, 2500), 50000, 27.78)
    il = amm.calculate_impermanent_loss(pos)
    print(f"  Position: {pos.position_id}")
    print(f"  Impermanent Loss: {il.percentage:.2%} (${il.usd_value:.2f})")

    # Lending
    print("\n--- DeFi Lending ---")
    lending = LendingProtocol("aave_v3")
    supply = lending.supply("USDC", 100_000, "0x1234...5678")
    borrow = lending.borrow("WETH", 20, "USDC", 100_000)
    print(f"  Supply: {supply.asset} ${supply.amount:,.0f} at {supply.apy:.1%} APY")
    print(f"  Borrow: {borrow.asset} {borrow.amount} @ Health Factor: {borrow.health_factor}")

    # Yield
    print("\n--- Yield Optimization ---")
    optimizer = YieldOptimizer(risk_tolerance="moderate")
    strategy = optimizer.optimize(100_000)
    print(f"  Expected APY: {strategy.expected_apy:.2%}")
    for a in strategy.allocations:
        print(f"    {a.protocol}: {a.percentage:.0%} @ {a.apy:.1%} APY")

    # Custody
    print("\n--- Institutional Custody ---")
    custody = InstitutionalCustody(required_signers=3, total_signers=5)
    hot = custody.create_wallet(WalletTier.HOT)
    cold = custody.create_wallet(WalletTier.COLD)
    print(f"  Hot wallet: {hot.address[:20]}...")
    print(f"  Cold wallet: {cold.address[:20]}...")
    print(f"  Signers required: {custody.required}/{custody.total}")


if __name__ == "__main__":
    main()
