"""
NFT Marketplace Module
Listing, auction, order matching, royalties, and collection analytics.
"""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ListingType(Enum):
    FIXED_PRICE = "fixed_price"
    ENGLISH_AUCTION = "english_auction"
    DUTCH_AUCTION = "dutch_auction"
    SEALED_BID = "sealed_bid"


class OrderStatus(Enum):
    ACTIVE = "active"
    SOLD = "sold"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Listing:
    """NFT listing."""
    listing_id: str
    collection: str
    token_id: int
    seller: str
    price_eth: float
    listing_type: ListingType
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    status: OrderStatus = OrderStatus.ACTIVE


@dataclass
class Auction:
    """NFT auction."""
    auction_id: str
    collection: str
    token_id: int
    seller: str
    starting_price: float
    reserve_price: float
    current_bid: float = 0.0
    current_bidder: str = ""
    num_bids: int = 0
    end_time: Optional[datetime] = None
    reserve_met: bool = False

    @property
    def time_remaining_hours(self) -> float:
        if self.end_time is None:
            return 0
        return max(0, (self.end_time - datetime.now(timezone.utc)).total_seconds() / 3600)


@dataclass
class Bid:
    """Auction bid."""
    bid_id: str
    auction_id: str
    bidder: str
    amount: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Trade:
    """Executed trade."""
    trade_id: str
    collection: str
    token_id: int
    seller: str
    buyer: str
    price_eth: float
    royalty_eth: float = 0.0
    fee_eth: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RoyaltyInfo:
    """Royalty calculation result."""
    creator_share: float
    seller_share: float
    marketplace_fee: float
    total: float


@dataclass
class CollectionStats:
    """Collection statistics."""
    collection: str
    floor_price: float = 0.0
    volume_24h: float = 0.0
    volume_7d: float = 0.0
    unique_holders: int = 0
    total_supply: int = 0
    listed_count: int = 0
    avg_sale_price: float = 0.0


# ---------------------------------------------------------------------------
# Listing Manager
# ---------------------------------------------------------------------------

class ListingManager:
    """Manage NFT listings."""

    def __init__(self, marketplace_fee_bps: int = 250):
        self._listings: Dict[str, Listing] = {}
        self.marketplace_fee_bps = marketplace_fee_bps

    def create_fixed_price(
        self,
        collection: str,
        token_id: int,
        price_eth: float,
        seller: str,
        duration_hours: float = 72,
    ) -> Listing:
        listing_id = f"LST-{secrets.token_hex(4).upper()}"
        listing = Listing(
            listing_id=listing_id,
            collection=collection,
            token_id=token_id,
            seller=seller,
            price_eth=price_eth,
            listing_type=ListingType.FIXED_PRICE,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=duration_hours),
        )
        self._listings[listing_id] = listing
        return listing

    def cancel_listing(self, listing_id: str) -> bool:
        listing = self._listings.get(listing_id)
        if listing and listing.status == OrderStatus.ACTIVE:
            listing.status = OrderStatus.CANCELLED
            return True
        return False

    def get_active_listings(self) -> List[Listing]:
        return [l for l in self._listings.values() if l.status == OrderStatus.ACTIVE]

    def get_listings_by_collection(self, collection: str) -> List[Listing]:
        return [l for l in self._listings.values() if l.collection == collection]


# ---------------------------------------------------------------------------
# Auction Engine
# ---------------------------------------------------------------------------

class AuctionEngine:
    """Manage NFT auctions."""

    def __init__(self):
        self._auctions: Dict[str, Auction] = {}
        self._bids: Dict[str, List[Bid]] = {}

    def create_english_auction(
        self,
        collection: str,
        token_id: int,
        starting_price: float,
        reserve_price: float,
        seller: str = "",
        duration_hours: float = 24,
    ) -> Auction:
        auction_id = f"AUC-{secrets.token_hex(4).upper()}"
        auction = Auction(
            auction_id=auction_id,
            collection=collection,
            token_id=token_id,
            seller=seller,
            starting_price=starting_price,
            reserve_price=reserve_price,
            end_time=datetime.now(timezone.utc) + timedelta(hours=duration_hours),
        )
        self._auctions[auction_id] = auction
        self._bids[auction_id] = []
        return auction

    def place_bid(self, auction_id: str, bidder: str, amount: float) -> Optional[Bid]:
        auction = self._auctions.get(auction_id)
        if not auction:
            return None
        if amount <= auction.current_bid:
            return None
        bid = Bid(
            bid_id=f"BID-{secrets.token_hex(4).upper()}",
            auction_id=auction_id,
            bidder=bidder,
            amount=amount,
        )
        self._bids[auction_id].append(bid)
        auction.current_bid = amount
        auction.current_bidder = bidder
        auction.num_bids += 1
        auction.reserve_met = amount >= auction.reserve_price
        return bid

    def check_reserve(self, auction_id: str) -> bool:
        auction = self._auctions.get(auction_id)
        return auction.reserve_met if auction else False

    def get_auction(self, auction_id: str) -> Optional[Auction]:
        return self._auctions.get(auction_id)


# ---------------------------------------------------------------------------
# Order Matcher
# ---------------------------------------------------------------------------

class OrderMatcher:
    """Match and execute trades."""

    def __init__(self, fee_bps: int = 250):
        self._trades: List[Trade] = []
        self.fee_bps = fee_bps

    def execute_trade(
        self,
        listing_id: str = "",
        buyer: str = "",
        price_eth: float = 0,
        max_slippage: float = 0.01,
    ) -> Trade:
        trade = Trade(
            trade_id=f"TRD-{secrets.token_hex(4).upper()}",
            collection="0x0000",
            token_id=0,
            seller="0x0000",
            buyer=buyer,
            price_eth=price_eth,
            fee_eth=price_eth * self.fee_bps / 10000,
        )
        self._trades.append(trade)
        return trade

    def get_recent_trades(self, limit: int = 10) -> List[Trade]:
        return self._trades[-limit:]


# ---------------------------------------------------------------------------
# Royalty Calculator
# ---------------------------------------------------------------------------

class RoyaltyCalculator:
    """Calculate marketplace royalties."""

    def calculate(
        self,
        sale_price_eth: float,
        royalty_bps: int = 500,
        seller_share_bps: int = 9500,
        marketplace_fee_bps: int = 250,
    ) -> RoyaltyInfo:
        royalty = sale_price_eth * royalty_bps / 10000
        marketplace_fee = sale_price_eth * marketplace_fee_bps / 10000
        seller_share = sale_price_eth - royalty - marketplace_fee
        return RoyaltyInfo(
            creator_share=round(royalty, 6),
            seller_share=round(seller_share, 6),
            marketplace_fee=round(marketplace_fee, 6),
            total=round(sale_price_eth, 6),
        )


# ---------------------------------------------------------------------------
# Collection Analytics
# ---------------------------------------------------------------------------

class CollectionAnalytics:
    """NFT collection analytics."""

    def __init__(self, collection: str):
        self.collection = collection

    def get_stats(self) -> CollectionStats:
        return CollectionStats(
            collection=self.collection,
            floor_price=0.5,
            volume_24h=125.3,
            volume_7d=890.2,
            unique_holders=1250,
            total_supply=5000,
            listed_count=350,
            avg_sale_price=1.2,
        )

    def get_sales_history(self, days: int = 30) -> List[Dict[str, Any]]:
        return [
            {"date": f"2024-01-{d:02d}", "volume": 50 + d * 2, "sales": 10 + d}
            for d in range(1, min(days + 1, 31))
        ]


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  NFT Marketplace Demo")
    print("=" * 60)

    print("\n[1] Fixed Price Listing")
    mgr = ListingManager()
    listing = mgr.create_fixed_price("0x1234", 42, 1.5, "0xABCD", 72)
    print(f"  ID: {listing.listing_id}")
    print(f"  Price: {listing.price_eth} ETH")
    print(f"  Expires: {listing.expires_at}")

    print("\n[2] English Auction")
    engine = AuctionEngine()
    auction = engine.create_english_auction("0x1234", 42, 0.1, 2.0)
    bid = engine.place_bid(auction.auction_id, "0xBidder", 1.0)
    print(f"  Auction: {auction.auction_id}")
    print(f"  Bid: {bid.amount} ETH")
    print(f"  Reserve met: {engine.check_reserve(auction.auction_id)}")

    print("\n[3] Order Matching")
    matcher = OrderMatcher()
    trade = matcher.execute_trade(buyer="0xBuyer", price_eth=1.5)
    print(f"  Trade: {trade.trade_id}")
    print(f"  Fee: {trade.fee_eth:.4f} ETH")

    print("\n[4] Royalty Calculation")
    royalty_calc = RoyaltyCalculator()
    royalty = royalty_calc.calculate(10.0, 500, 9250, 250)
    print(f"  Creator: {royalty.creator_share} ETH")
    print(f"  Seller: {royalty.seller_share} ETH")
    print(f"  Marketplace: {royalty.marketplace_fee} ETH")

    print("\n[5] Collection Analytics")
    analytics = CollectionAnalytics("0x1234")
    stats = analytics.get_stats()
    print(f"  Floor: {stats.floor_price} ETH")
    print(f"  Volume (24h): {stats.volume_24h} ETH")
    print(f"  Holders: {stats.unique_holders}")
    print(f"  Listed: {stats.listed_count}")

    print("\n" + "=" * 60)
    print("  NFT marketplace demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
