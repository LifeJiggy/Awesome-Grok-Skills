"""
NFT Development Module
ERC-721/1155 implementation, metadata generation, lazy minting, auctions, and royalties.
"""

from __future__ import annotations

import hashlib
import json
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TokenStandard(Enum):
    ERC721 = "ERC-721"
    ERC1155 = "ERC-1155"


class AuctionType(Enum):
    ENGLISH = "english"
    DUTCH = "dutch"
    SEALED_BID = "sealed_bid"


class AuctionStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ENDED = "ended"
    SETTLED = "settled"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class NFTAttribute:
    """NFT trait/attribute."""
    trait_type: str
    value: str
    display_type: Optional[str] = None
    max_value: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {"trait_type": self.trait_type, "value": self.value}
        if self.display_type:
            d["display_type"] = self.display_type
        if self.max_value is not None:
            d["max_value"] = self.max_value
        return d


@dataclass
class NFTMetadata:
    """NFT metadata (ERC-721 Metadata standard)."""
    name: str
    description: str
    image: str
    attributes: List[NFTAttribute] = field(default_factory=list)
    external_url: str = ""
    animation_url: str = ""
    background_color: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_json(self, indent: int = 2) -> str:
        d: Dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "attributes": [a.to_dict() for a in self.attributes],
        }
        if self.external_url:
            d["external_url"] = self.external_url
        if self.animation_url:
            d["animation_url"] = self.animation_url
        if self.background_color:
            d["background_color"] = self.background_color
        if self.properties:
            d["properties"] = self.properties
        return json.dumps(d, indent=indent)

    @property
    def hash(self) -> str:
        return hashlib.sha256(self.to_json().encode()).hexdigest()[:16]


@dataclass
class LazyMintVoucher:
    """Voucher for lazy minting."""
    token_id: int
    metadata_uri: str
    min_price: float
    signer: str
    signature: str = ""
    expiration: Optional[datetime] = None
    max_per_wallet: int = 0

    @property
    def is_expired(self) -> bool:
        if self.expiration is None:
            return False
        return datetime.now(timezone.utc) > self.expiration


@dataclass
class Auction:
    """NFT auction."""
    auction_id: str
    token_id: int
    collection: str
    seller: str
    auction_type: AuctionType
    start_price: float
    reserve_price: float
    current_bid: float = 0.0
    current_bidder: str = ""
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    duration_hours: float = 24
    status: AuctionStatus = AuctionStatus.PENDING
    bids: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def end_time(self) -> datetime:
        return self.start_time + timedelta(hours=self.duration_hours)

    @property
    def time_remaining_hours(self) -> float:
        remaining = (self.end_time - datetime.now(timezone.utc)).total_seconds() / 3600
        return max(0, remaining)

    @property
    def reserve_met(self) -> bool:
        return self.current_bid >= self.reserve_price


@dataclass
class Bid:
    """Auction bid."""
    auction_id: str
    bidder: str
    amount: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sealed: bool = False


@dataclass
class RoyaltySplit:
    """Royalty payment split."""
    address: str
    bps: int
    share_pct: float = 0.0


@dataclass
class MerkleAllowlist:
    """Merkle tree allowlist data."""
    root: str
    entries: Dict[str, int] = field(default_factory=dict)
    tree: List[str] = field(default_factory=list)

    def get_proof(self, address: str) -> List[str]:
        idx = list(self.entries.keys()).index(address) if address in self.entries else -1
        if idx < 0:
            return []
        proof: List[str] = []
        level = list(self.entries.keys())
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                if i + 1 < len(level):
                    combined = hashlib.sha256(
                        (level[i] + level[i + 1]).encode()
                    ).hexdigest()
                    next_level.append(combined)
                    if i == idx or i + 1 == idx:
                        other = level[i + 1] if i == idx else level[i]
                        proof.append(other)
                else:
                    next_level.append(level[i])
            level = next_level
            idx = idx // 2
        return proof


# ---------------------------------------------------------------------------
# NFT Collection
# ---------------------------------------------------------------------------

class NFTCollection:
    """Manage an NFT collection."""

    def __init__(
        self,
        name: str,
        symbol: str,
        base_uri: str = "",
        max_supply: int = 10000,
        royalty_bps: int = 500,
        standard: TokenStandard = TokenStandard.ERC721,
    ):
        self.name = name
        self.symbol = symbol
        self.base_uri = base_uri
        self.max_supply = max_supply
        self.royalty_bps = royalty_bps
        self.standard = standard
        self.address = f"0x{secrets.token_hex(20)}"
        self._minted: Set[int] = set()
        self._owners: Dict[int, str] = {}
        self._balances: Dict[str, int] = {}

    @property
    def royalty_pct(self) -> float:
        return self.royalty_bps / 100

    @property
    def total_minted(self) -> int:
        return len(self._minted)

    @property
    def total_supply(self) -> int:
        return self.total_minted

    @property
    def remaining(self) -> int:
        return self.max_supply - self.total_minted

    def mint(self, token_id: int, to: str) -> bool:
        if token_id in self._minted or self.total_minted >= self.max_supply:
            return False
        self._minted.add(token_id)
        self._owners[token_id] = to
        self._balances[to] = self._balances.get(to, 0) + 1
        return True

    def mint_batch(
        self, token_ids: List[int], to: str
    ) -> int:
        count = 0
        for tid in token_ids:
            if self.mint(tid, to):
                count += 1
        return count

    def owner_of(self, token_id: int) -> Optional[str]:
        return self._owners.get(token_id)

    def balance_of(self, owner: str) -> int:
        return self._balances.get(owner, 0)

    def token_uri(self, token_id: int) -> str:
        return f"{self.base_uri}{token_id}.json"

    def create_merkle_allowlist(
        self, addresses: List[str], max_per_wallet: int = 1
    ) -> MerkleAllowlist:
        entries = {addr.lower(): max_per_wallet for addr in addresses}
        leaves = [hashlib.sha256(addr.encode()).hexdigest() for addr in entries]
        root = hashlib.sha256("".join(sorted(leaves)).encode()).hexdigest()
        return MerkleAllowlist(root=root, entries=entries, tree=leaves)

    def transfer(self, token_id: int, from_addr: str, to_addr: str) -> bool:
        if self._owners.get(token_id) != from_addr:
            return False
        self._owners[token_id] = to_addr
        self._balances[from_addr] = max(self._balances.get(from_addr, 0) - 1, 0)
        self._balances[to_addr] = self._balances.get(to_addr, 0) + 1
        return True

    def get_collection_stats(self) -> Dict[str, Any]:
        unique_holders = len(set(self._owners.values()))
        return {
            "name": self.name,
            "symbol": self.symbol,
            "standard": self.standard.value,
            "total_supply": self.total_supply,
            "max_supply": self.max_supply,
            "unique_holders": unique_holders,
            "royalty_pct": self.royalty_pct,
        }


# ---------------------------------------------------------------------------
# Metadata Generator
# ---------------------------------------------------------------------------

class MetadataGenerator:
    """Generate and validate NFT metadata."""

    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_ATTRIBUTES = 100
    SUPPORTED_IMAGE_FORMATS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}

    def __init__(self, collection: Optional[NFTCollection] = None):
        self.collection = collection

    def create_metadata(
        self,
        name: str,
        description: str,
        image: str,
        attributes: Optional[List[Dict[str, str]]] = None,
        external_url: str = "",
        animation_url: str = "",
        properties: Optional[Dict[str, Any]] = None,
    ) -> NFTMetadata:
        attrs = [
            NFTAttribute(trait_type=a["trait_type"], value=a["value"])
            for a in (attributes or [])
        ]
        return NFTMetadata(
            name=name,
            description=description,
            image=image,
            attributes=attrs,
            external_url=external_url,
            animation_url=animation_url,
            properties=properties or {},
        )

    def validate_metadata(self, metadata: NFTMetadata) -> bool:
        errors = self.get_validation_errors(metadata)
        return len(errors) == 0

    def get_validation_errors(self, metadata: NFTMetadata) -> List[str]:
        errors: List[str] = []
        if not metadata.name:
            errors.append("Name is required")
        elif len(metadata.name) > self.MAX_NAME_LENGTH:
            errors.append(f"Name exceeds {self.MAX_NAME_LENGTH} characters")
        if not metadata.description:
            errors.append("Description is required")
        elif len(metadata.description) > self.MAX_DESCRIPTION_LENGTH:
            errors.append(f"Description exceeds {self.MAX_DESCRIPTION_LENGTH} characters")
        if not metadata.image:
            errors.append("Image URL is required")
        if len(metadata.attributes) > self.MAX_ATTRIBUTES:
            errors.append(f"Too many attributes (max {self.MAX_ATTRIBUTES})")
        return errors

    def generate_token_uri(self, metadata: NFTMetadata) -> str:
        return f"data:application/json;base64,{self._to_base64(metadata.to_json())}"

    def batch_generate(
        self, base_name: str, count: int, trait_pool: Dict[str, List[str]]
    ) -> List[NFTMetadata]:
        results: List[NFTMetadata] = []
        for i in range(count):
            attrs = []
            for trait_type, values in trait_pool.items():
                value = values[i % len(values)]
                attrs.append({"trait_type": trait_type, "value": value})
            meta = self.create_metadata(
                name=f"{base_name} #{i + 1}",
                description=f"Unique {base_name} from the collection",
                image=f"ipfs://QmImageCID/{i + 1}.png",
                attributes=attrs,
            )
            results.append(meta)
        return results

    @staticmethod
    def _to_base64(s: str) -> str:
        import base64
        return base64.b64encode(s.encode()).decode()


# ---------------------------------------------------------------------------
# Lazy Minter
# ---------------------------------------------------------------------------

class LazyMinter:
    """Gas-free lazy minting with EIP-712 style vouchers."""

    def __init__(self, collection: NFTCollection):
        self.collection = collection
        self._claimed: Set[int] = set()

    def create_voucher(
        self,
        token_id: int,
        metadata_uri: str,
        min_price: float = 0.0,
        signer: str = "0x0000000000000000000000000000000000000000",
        max_per_wallet: int = 0,
        expiration_hours: Optional[int] = None,
    ) -> LazyMintVoucher:
        expiration = None
        if expiration_hours:
            expiration = datetime.now(timezone.utc) + timedelta(hours=expiration_hours)
        message = f"{token_id}:{metadata_uri}:{min_price}:{signer}"
        signature = hashlib.sha256(message.encode()).hexdigest()[:64]
        return LazyMintVoucher(
            token_id=token_id,
            metadata_uri=metadata_uri,
            min_price=min_price,
            signer=signer,
            signature=signature,
            expiration=expiration,
            max_per_wallet=max_per_wallet,
        )

    def redeem_voucher(
        self, voucher: LazyMintVoucher, redeemer: str, price: float
    ) -> bool:
        if voucher.is_expired:
            logger.error("Voucher expired")
            return False
        if price < voucher.min_price:
            logger.error("Price below minimum")
            return False
        if voucher.token_id in self._claimed:
            logger.error("Token already claimed")
            return False
        self._claimed.add(voucher.token_id)
        return self.collection.mint(voucher.token_id, redeemer)


# ---------------------------------------------------------------------------
# Auction House
# ---------------------------------------------------------------------------

class AuctionHouse:
    """NFT auction management."""

    def __init__(self):
        self._auctions: Dict[str, Auction] = {}
        self._bids: Dict[str, List[Bid]] = {}

    def create_auction(
        self,
        token_id: int,
        collection: str,
        start_price: float,
        reserve_price: float,
        duration_hours: float = 24,
        seller: str = "",
        auction_type: AuctionType = AuctionType.ENGLISH,
    ) -> Auction:
        auction_id = f"auc_{secrets.token_hex(8)}"
        auction = Auction(
            auction_id=auction_id,
            token_id=token_id,
            collection=collection,
            seller=seller,
            auction_type=auction_type,
            start_price=start_price,
            reserve_price=reserve_price,
            duration_hours=duration_hours,
            status=AuctionStatus.ACTIVE,
        )
        self._auctions[auction_id] = auction
        self._bids[auction_id] = []
        return auction

    def place_bid(
        self, auction_id: str, bidder: str, amount: float
    ) -> Bid:
        auction = self._auctions.get(auction_id)
        if not auction or auction.status != AuctionStatus.ACTIVE:
            raise ValueError("Auction not active")
        if amount <= auction.current_bid:
            raise ValueError("Bid must be higher than current bid")
        bid = Bid(auction_id=auction_id, bidder=bidder, amount=amount)
        self._bids[auction_id].append(bid)
        auction.current_bid = amount
        auction.current_bidder = bidder
        auction.bids.append({
            "bidder": bidder,
            "amount": amount,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return bid

    def settle_auction(self, auction_id: str) -> Dict[str, Any]:
        auction = self._auctions.get(auction_id)
        if not auction:
            raise ValueError("Auction not found")
        auction.status = AuctionStatus.SETTLED
        return {
            "auction_id": auction_id,
            "winner": auction.current_bidder,
            "final_price": auction.current_bid,
            "reserve_met": auction.reserve_met,
            "total_bids": len(auction.bids),
        }

    def get_auction(self, auction_id: str) -> Optional[Auction]:
        return self._auctions.get(auction_id)

    def get_active_auctions(self) -> List[Auction]:
        return [
            a for a in self._auctions.values()
            if a.status == AuctionStatus.ACTIVE
        ]


# ---------------------------------------------------------------------------
# Royalty Manager
# ---------------------------------------------------------------------------

class RoyaltyManager:
    """Manage NFT royalty splits and payments."""

    def create_splits(
        self, total_royalty_bps: int, recipients: List[Dict[str, Any]]
    ) -> List[RoyaltySplit]:
        total_bps = sum(r["bps"] for r in recipients)
        if total_bps != total_royalty_bps:
            raise ValueError(
                f"Split total {total_bps} != royalty {total_royalty_bps}"
            )
        splits = []
        for r in recipients:
            splits.append(RoyaltySplit(
                address=r["address"],
                bps=r["bps"],
                share_pct=r["bps"] / total_royalty_bps * 100,
            ))
        return splits

    def calculate_payouts(
        self, sale_price: float, splits: List[RoyaltySplit]
    ) -> List[Dict[str, Any]]:
        payouts = []
        for split in splits:
            amount = sale_price * split.bps / 10000
            payouts.append({
                "address": split.address,
                "amount": round(amount, 6),
                "bps": split.bps,
            })
        return payouts

    def validate_splits(self, splits: List[RoyaltySplit]) -> bool:
        total = sum(s.bps for s in splits)
        return 0 < total <= 10000


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  NFT Development Module Demo")
    print("=" * 60)

    collection = NFTCollection(
        name="Pixel Punks",
        symbol="PUNK",
        base_uri="ipfs://QmTest/",
        max_supply=100,
        royalty_bps=500,
    )
    print(f"\nCollection: {collection.name} ({collection.symbol})")
    print(f"Max supply: {collection.max_supply}")
    print(f"Royalty: {collection.royalty_pct}%")
    print(f"Address: {collection.address}")

    print("\n[1] Minting")
    collection.mint_batch(range(1, 11), "0x1234...abcd")
    print(f"  Minted: {collection.total_minted} / {collection.max_supply}")
    print(f"  Owner of #1: {collection.owner_of(1)}")

    print("\n[2] Metadata Generation")
    gen = MetadataGenerator(collection)
    meta = gen.create_metadata(
        name="Pixel Punk #1",
        description="A unique pixel punk",
        attributes=[
            {"trait_type": "Background", "value": "Blue"},
            {"trait_type": "Eyes", "value": "Laser"},
        ],
    )
    print(f"  Valid: {gen.validate_metadata(meta)}")
    print(f"  Hash: {meta.hash}")

    print("\n[3] Lazy Minting")
    lazy = LazyMinter(collection)
    voucher = lazy.create_voucher(50, "ipfs://QmTest/50.json", min_price=0.01)
    print(f"  Voucher token: {voucher.token_id}")
    print(f"  Signature: {voucher.signature[:32]}...")

    print("\n[4] Auction")
    auction_house = AuctionHouse()
    auction = auction_house.create_auction(
        token_id=1, collection=collection.address,
        start_price=0.1, reserve_price=1.0,
    )
    bid = auction_house.place_bid(auction.auction_id, "0xBidder", 0.5)
    print(f"  Auction {auction.auction_id[:16]}...")
    print(f"  Current bid: {bid.amount} ETH")

    print("\n[5] Royalties")
    royalty_mgr = RoyaltyManager()
    splits = royalty_mgr.create_splits(500, [
        {"address": "0xArtist", "bps": 700},
        {"address": "0xPlatform", "bps": 200},
        {"address": "0xTreasury", "bps": 100},
    ])
    payouts = royalty_mgr.calculate_payouts(10.0, splits)
    for p in payouts:
        print(f"  {p['address']}: ${p['amount']:.2f}")

    print("\n[6] Allowlist")
    merkle = collection.create_merkle_allowlist(
        ["0xAddr1", "0xAddr2", "0xAddr3"], max_per_wallet=2
    )
    print(f"  Merkle root: {merkle.root[:32]}...")

    print("\n[7] Collection Stats")
    stats = collection.get_collection_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 60)
    print("  NFT development demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
