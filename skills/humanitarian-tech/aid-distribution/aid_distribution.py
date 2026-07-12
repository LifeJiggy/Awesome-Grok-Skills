"""
Aid Distribution Module
Part of the humanitarian-tech skill domain

Comprehensive aid distribution system covering beneficiary registration,
voucher systems, and supply chain tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import hashlib
import json
import random
import uuid


# =============================================================================
# Enums
# =============================================================================

class BeneficiaryStatus(Enum):
    """Beneficiary registration status."""
    PENDING = "pending"
    REGISTERED = "registered"
    VERIFIED = "verified"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
    DECEASED = "deceased"


class VulnerabilityLevel(Enum):
    """Beneficiary vulnerability levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NeedCategory(Enum):
    """Categories of humanitarian needs."""
    FOOD = "food"
    WATER = "water"
    SHELTER = "shelter"
    HEALTH = "health"
    EDUCATION = "education"
    WASH = "wash"
    PROTECTION = "protection"
    LIVELIHOOD = "livelihood"
    NFIS = "non_food_items"


class VoucherType(Enum):
    """Types of vouchers."""
    FOOD = "food"
    CASH = "cash"
    MULTI_PURPOSE = "multi_purpose"
    SHELTER = "shelter"
    HEALTH = "health"
    EDUCATION = "education"
    WASH = "wash"


class VoucherStatus(Enum):
    """Voucher lifecycle status."""
    CREATED = "created"
    ISSUED = "issued"
    REDEEMED = "redeemed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    LOST = "lost"


class ShipmentStatus(Enum):
    """Supply chain shipment status."""
    PLANNED = "planned"
    DISPATCHED = "dispatched"
    IN_TRANSIT = "in_transit"
    AT_CHECKPOINT = "at_checkpoint"
    DELAYED = "delayed"
    ARRIVED = "arrived"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class WarehouseZone(Enum):
    """Warehouse storage zones."""
    GENERAL = "general"
    COLD_CHAIN = "cold_chain"
    HAZARDOUS = "hazardous"
    HIGH_VALUE = "high_value"
    RECEIVING = "receiving"
    DISPATCH = "dispatch"


class DistributionStatus(Enum):
    """Distribution event status."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIAL = "partial"
    CANCELLED = "cancelled"
    POST_MONITORING = "post_monitoring"


class ItemType(Enum):
    """Types of aid items."""
    RICE = "rice"
    WHEAT = "wheat"
    FLOUR = "flour"
    OIL = "oil"
    SUGAR = "sugar"
    SALT = "salt"
    BEANS = "beans"
    LENTILS = "lentils"
    CANNED_FOOD = "canned_food"
    HIGH_ENERGY_BISCUIT = "high_energy_biscuit"
    WATER_PURIFICATION = "water_purification"
    BLANKET = "blanket"
    TENT = "tent"
    HYGIENE_KIT = "hygiene_kit"
    MEDICAL_KIT = "medical_kit"
    COT = "cot"
    KITCHEN_SET = "kitchen_set"
    SOLAR_LAMP = "solar_lamp"


class DeliveryMethod(Enum):
    """Methods of aid delivery."""
    CENTRALIZED_DISTRIBUTION = "centralized_distribution"
    DOOR_TO_DOOR = "door_to_door"
    VOUCHER_REDEMPTION = "voucher_redemption"
    MOBILE_MONEY = "mobile_money"
    BANK_TRANSFER = "bank_transfer"
    CASH_FOR_WORK = "cash_for_work"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class Beneficiary:
    """Registered beneficiary record."""
    beneficiary_id: str
    household_size: int
    head_of_household_name: str
    location: str
    registration_date: datetime
    status: BeneficiaryStatus = BeneficiaryStatus.REGISTERED
    vulnerability_level: VulnerabilityLevel = VulnerabilityLevel.MEDIUM
    needs: List[NeedCategory] = field(default_factory=list)
    contact_phone: Optional[str] = None
    id_document_type: str = ""
    id_document_number: str = ""
    vulnerability_score: float = 0.5
    total aid_received: float = 0.0
    distribution_history: List[str] = field(default_factory=list)
    household_members: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.status == BeneficiaryStatus.ACTIVE

    def per_capita_entitlement(self, base_amount: float) -> float:
        """Calculate per capita entitlement."""
        return base_amount * self.household_size

    def to_dict(self) -> Dict[str, Any]:
        return {
            "beneficiary_id": self.beneficiary_id,
            "household_size": self.household_size,
            "head_of_household_name": self.head_of_household_name,
            "location": self.location,
            "status": self.status.value,
            "vulnerability_level": self.vulnerability_level.value,
            "vulnerability_score": self.vulnerability_score,
            "needs": [n.value for n in self.needs],
            "total_aid_received": self.total_aid_received,
            "distribution_count": len(self.distribution_history)
        }


@dataclass
class Voucher:
    """Aid voucher record."""
    voucher_id: str
    beneficiary_id: str
    voucher_type: VoucherType
    value: float
    currency: str
    issued_date: datetime
    expiry_date: datetime
    status: VoucherStatus = VoucherStatus.CREATED
    redemption_date: Optional[datetime] = None
    merchant_id: Optional[str] = None
    items_entitled: List[Dict[str, Any]] = field(default_factory=list)
    pin_hash: Optional[str] = None
    qr_code: str = ""
    redemption_location: Optional[str] = None

    def is_valid(self) -> bool:
        """Check if voucher is valid for redemption."""
        return (self.status == VoucherStatus.ISSUED and
                datetime.now() <= self.expiry_date)

    def remaining_value(self) -> float:
        """Calculate remaining voucher value."""
        if self.status == VoucherStatus.REDEEMED:
            return 0.0
        return self.value

    def days_until_expiry(self) -> int:
        """Calculate days until voucher expires."""
        delta = self.expiry_date - datetime.now()
        return max(0, delta.days)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "voucher_id": self.voucher_id,
            "beneficiary_id": self.beneficiary_id,
            "voucher_type": self.voucher_type.value,
            "value": self.value,
            "currency": self.currency,
            "status": self.status.value,
            "issued_date": self.issued_date.isoformat(),
            "expiry_date": self.expiry_date.isoformat(),
            "remaining_value": self.remaining_value(),
            "days_until_expiry": self.days_until_expiry(),
            "redemption_location": self.redemption_location
        }


@dataclass
class Shipment:
    """Supply chain shipment record."""
    shipment_id: str
    origin: str
    destination: str
    items: List[Dict[str, Any]]
    dispatch_date: Optional[datetime] = None
    estimated_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: ShipmentStatus = ShipmentStatus.PLANNED
    carrier: str = ""
    vehicle_id: str = ""
    tracking_events: List[Dict[str, Any]] = field(default_factory=list)
    temperature_log: List[Dict[str, Any]] = field(default_factory=list)
    condition_notes: str = ""

    @property
    def total_quantity(self) -> float:
        return sum(item.get("quantity", 0) for item in self.items)

    def add_tracking_event(self, location: str, status: str, notes: str = "") -> None:
        """Add a tracking event to the shipment."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "location": location,
            "status": status,
            "notes": notes
        }
        self.tracking_events.append(event)
        self.status = ShipmentStatus(status) if status in [s.value for s in ShipmentStatus] else self.status

    def transit_time_hours(self) -> Optional[float]:
        """Calculate transit time in hours."""
        if self.dispatch_date and self.actual_arrival:
            return (self.actual_arrival - self.dispatch_date).total_seconds() / 3600
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "shipment_id": self.shipment_id,
            "origin": self.origin,
            "destination": self.destination,
            "items": self.items,
            "total_quantity": self.total_quantity,
            "status": self.status.value,
            "dispatch_date": self.dispatch_date.isoformat() if self.dispatch_date else None,
            "estimated_arrival": self.estimated_arrival.isoformat() if self.estimated_arrival else None,
            "tracking_events": len(self.tracking_events),
            "carrier": self.carrier
        }


@dataclass
class Warehouse:
    """Warehouse facility record."""
    warehouse_id: str
    name: str
    location: str
    capacity: float  # in metric tons
    current_inventory: float = 0.0
    zones: Dict[WarehouseZone, float] = field(default_factory=dict)
    manager: str = ""
    contact_phone: str = ""
    operational_since: Optional[date] = None
    temperature_controlled: bool = False
    security_level: str = "standard"

    @property
    def utilization_rate(self) -> float:
        if self.capacity == 0:
            return 0.0
        return self.current_inventory / self.capacity

    @property
    def available_capacity(self) -> float:
        return max(0, self.capacity - self.current_inventory)

    def add_inventory(self, quantity: float, zone: WarehouseZone = WarehouseZone.GENERAL) -> bool:
        """Add inventory to warehouse."""
        if self.current_inventory + quantity > self.capacity:
            return False
        self.current_inventory += quantity
        self.zones[zone] = self.zones.get(zone, 0) + quantity
        return True

    def remove_inventory(self, quantity: float, zone: WarehouseZone = WarehouseZone.GENERAL) -> bool:
        """Remove inventory from warehouse."""
        if quantity > self.current_inventory:
            return False
        if zone in self.zones and self.zones[zone] < quantity:
            return False
        self.current_inventory -= quantity
        if zone in self.zones:
            self.zones[zone] -= quantity
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "warehouse_id": self.warehouse_id,
            "name": self.name,
            "location": self.location,
            "capacity": self.capacity,
            "current_inventory": self.current_inventory,
            "available_capacity": self.available_capacity,
            "utilization_rate": self.utilization_rate,
            "zones": {z.value: v for z, v in self.zones.items()},
            "temperature_controlled": self.temperature_controlled
        }


@dataclass
class DistributionSite:
    """Distribution site record."""
    site_id: str
    name: str
    location: str
    capacity: int  # beneficiaries per day
    planned_date: Optional[datetime] = None
    status: DistributionStatus = DistributionStatus.PLANNED
    items_available: List[Dict[str, Any]] = field(default_factory=list)
    queue_count: int = 0
    served_count: int = 0
    staff_assigned: List[str] = field(default_factory=list)
    setup_checklist: Dict[str, bool] = field(default_factory=dict)
    feedback_collected: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def completion_rate(self) -> float:
        if self.capacity == 0:
            return 0.0
        return self.served_count / self.capacity

    @property
    def remaining_capacity(self) -> int:
        return max(0, self.capacity - self.served_count)

    def serve_beneficiary(self, count: int = 1) -> bool:
        """Record beneficiary service."""
        if self.served_count + count > self.capacity:
            return False
        self.served_count += count
        if self.served_count >= self.capacity:
            self.status = DistributionStatus.COMPLETED
        return True

    def collect_feedback(self, beneficiary_id: str, rating: int, comments: str = "") -> None:
        """Collect beneficiary feedback."""
        feedback = {
            "beneficiary_id": beneficiary_id,
            "rating": rating,
            "comments": comments,
            "timestamp": datetime.now().isoformat()
        }
        self.feedback_collected.append(feedback)

    def average_rating(self) -> float:
        """Calculate average feedback rating."""
        if not self.feedback_collected:
            return 0.0
        return sum(f["rating"] for f in self.feedback_collected) / len(self.feedback_collected)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site_id": self.site_id,
            "name": self.name,
            "location": self.location,
            "capacity": self.capacity,
            "served_count": self.served_count,
            "remaining_capacity": self.remaining_capacity,
            "completion_rate": self.completion_rate,
            "status": self.status.value,
            "queue_count": self.queue_count,
            "average_rating": self.average_rating(),
            "feedback_count": len(self.feedback_collected)
        }


@dataclass
class AidItem:
    """Individual aid item record."""
    item_id: str
    item_type: ItemType
    description: str
    quantity: float
    unit: str
    weight_kg: float = 0.0
    volume_m3: float = 0.0
    expiry_date: Optional[date] = None
    batch_number: str = ""
    manufacturer: str = ""
    cost_per_unit: float = 0.0
    storage_requirements: str = ""

    def is_expired(self) -> bool:
        """Check if item is expired."""
        if self.expiry_date is None:
            return False
        return date.today() > self.expiry_date

    def days_until_expiry(self) -> Optional[int]:
        """Calculate days until expiry."""
        if self.expiry_date is None:
            return None
        return max(0, (self.expiry_date - date.today()).days)

    def total_value(self) -> float:
        """Calculate total value of items."""
        return self.quantity * self.cost_per_unit

    def total_weight(self) -> float:
        """Calculate total weight."""
        return self.quantity * self.weight_kg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "item_type": self.item_type.value,
            "description": self.description,
            "quantity": self.quantity,
            "unit": self.unit,
            "total_weight_kg": self.total_weight(),
            "total_value": self.total_value(),
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "batch_number": self.batch_number
        }


# =============================================================================
# Core Systems
# =============================================================================

class BeneficiaryRegistry:
    """Beneficiary registration and management system."""

    def __init__(self, database: str = "aid_db"):
        self.database = database
        self.beneficiaries: Dict[str, Beneficiary] = {}
        self.household_index: Dict[str, List[str]] = {}  # location -> [beneficiary_ids]
        self.deduplication_index: Dict[str, str] = {}  # id_hash -> beneficiary_id
        self.registration_counter = 0

    def _generate_beneficiary_id(self) -> str:
        """Generate unique beneficiary ID."""
        self.registration_counter += 1
        return f"BEN-{datetime.now().year}-{self.registration_counter:06d}"

    def register_beneficiary(self, household_size: int, head_of_household_name: str,
                             location: str, needs: List[NeedCategory],
                             vulnerability_score: float = 0.5,
                             contact_phone: Optional[str] = None,
                             id_document_type: str = "",
                             id_document_number: str = "",
                             household_members: Optional[List[Dict[str, Any]]] = None) -> Beneficiary:
        """Register a new beneficiary."""
        # Deduplication check
        id_hash = hashlib.sha256(f"{id_document_number}:{head_of_household_name}".encode()).hexdigest()[:16]
        if id_hash in self.deduplication_index:
            existing_id = self.deduplication_index[id_hash]
            return self.beneficiaries[existing_id]

        beneficiary_id = self._generate_beneficiary_id()

        # Determine vulnerability level
        if vulnerability_score >= 0.8:
            vuln_level = VulnerabilityLevel.CRITICAL
        elif vulnerability_score >= 0.6:
            vuln_level = VulnerabilityLevel.HIGH
        elif vulnerability_score >= 0.4:
            vuln_level = VulnerabilityLevel.MEDIUM
        else:
            vuln_level = VulnerabilityLevel.LOW

        beneficiary = Beneficiary(
            beneficiary_id=beneficiary_id,
            household_size=household_size,
            head_of_household_name=head_of_household_name,
            location=location,
            registration_date=datetime.now(),
            status=BeneficiaryStatus.REGISTERED,
            vulnerability_level=vuln_level,
            needs=needs,
            contact_phone=contact_phone,
            id_document_type=id_document_type,
            id_document_number=id_document_number,
            vulnerability_score=vulnerability_score,
            household_members=household_members or []
        )

        self.beneficiaries[beneficiary_id] = beneficiary
        if location not in self.household_index:
            self.household_index[location] = []
        self.household_index[location].append(beneficiary_id)
        self.deduplication_index[id_hash] = beneficiary_id

        return beneficiary

    def verify_beneficiary(self, beneficiary_id: str) -> bool:
        """Verify a beneficiary registration."""
        if beneficiary_id in self.beneficiaries:
            self.beneficiaries[beneficiary_id].status = BeneficiaryStatus.VERIFIED
            return True
        return False

    def activate_beneficiary(self, beneficiary_id: str) -> bool:
        """Activate a beneficiary for aid distribution."""
        if beneficiary_id in self.beneficiaries:
            self.beneficiaries[beneficiary_id].status = BeneficiaryStatus.ACTIVE
            return True
        return False

    def suspend_beneficiary(self, beneficiary_id: str, reason: str) -> bool:
        """Suspend a beneficiary."""
        if beneficiary_id in self.beneficiaries:
            self.beneficiaries[beneficiary_id].status = BeneficiaryStatus.SUSPENDED
            self.beneficiaries[beneficiary_id].metadata["suspension_reason"] = reason
            return True
        return False

    def get_beneficiaries_by_location(self, location: str) -> List[Beneficiary]:
        """Get all beneficiaries in a location."""
        ids = self.household_index.get(location, [])
        return [self.beneficiaries[bid] for bid in ids if bid in self.beneficiaries]

    def get_beneficiaries_by_vulnerability(self, min_level: VulnerabilityLevel) -> List[Beneficiary]:
        """Get beneficiaries by minimum vulnerability level."""
        level_order = [VulnerabilityLevel.LOW, VulnerabilityLevel.MEDIUM,
                       VulnerabilityLevel.HIGH, VulnerabilityLevel.CRITICAL]
        min_idx = level_order.index(min_level)
        return [b for b in self.beneficiaries.values()
                if level_order.index(b.vulnerability_level) >= min_idx]

    def calculate_total_entitlement(self, beneficiary_id: str,
                                    entitlement_rules: Dict[str, float]) -> float:
        """Calculate total entitlement for a beneficiary."""
        beneficiary = self.beneficiaries.get(beneficiary_id)
        if not beneficiary:
            return 0.0

        base = entitlement_rules.get("base_amount", 50.0)
        per_capita = entitlement_rules.get("per_capita", 25.0)
        vulnerability_multiplier = 1 + (beneficiary.vulnerability_score * 0.5)

        total = (base + per_capita * beneficiary.household_size) * vulnerability_multiplier
        return round(total, 2)

    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_status = {}
        by_vulnerability = {}
        by_location = {}

        for b in self.beneficiaries.values():
            by_status[b.status.value] = by_status.get(b.status.value, 0) + 1
            by_vulnerability[b.vulnerability_level.value] = by_vulnerability.get(b.vulnerability_level.value, 0) + 1
            by_location[b.location] = by_location.get(b.location, 0) + 1

        total_household_size = sum(b.household_size for b in self.beneficiaries.values())

        return {
            "total_beneficiaries": len(self.beneficiaries),
            "total_household_members": total_household_size,
            "by_status": by_status,
            "by_vulnerability": by_vulnerability,
            "by_location": by_location,
            "average_vulnerability_score": sum(b.vulnerability_score for b in self.beneficiaries.values()) / max(len(self.beneficiaries), 1)
        }


class VoucherManagementSystem:
    """Digital and paper voucher management system."""

    def __init__(self, digital_enabled: bool = True, default_currency: str = "USD"):
        self.digital_enabled = digital_enabled
        self.default_currency = default_currency
        self.vouchers: Dict[str, Voucher] = {}
        self.merchants: Dict[str, Dict[str, Any]] = {}
        self.redemption_log: List[Dict[str, Any]] = []
        self.voucher_counter = 0

    def register_merchant(self, merchant_id: str, name: str,
                          location: str, accepted_types: List[VoucherType]) -> Dict[str, Any]:
        """Register a merchant for voucher redemption."""
        merchant = {
            "merchant_id": merchant_id,
            "name": name,
            "location": location,
            "accepted_types": [vt.value for vt in accepted_types],
            "total_redemptions": 0,
            "total_value_redeemed": 0.0,
            "status": "active"
        }
        self.merchants[merchant_id] = merchant
        return merchant

    def issue_voucher(self, beneficiary_id: str, voucher_type: VoucherType,
                      value: float, valid_days: int = 30,
                      currency: Optional[str] = None,
                      items_entitled: Optional[List[Dict[str, Any]]] = None) -> Voucher:
        """Issue a new voucher to a beneficiary."""
        self.voucher_counter += 1
        voucher_id = f"VCH-{datetime.now().strftime('%Y%m')}-{self.voucher_counter:06d}"

        voucher = Voucher(
            voucher_id=voucher_id,
            beneficiary_id=beneficiary_id,
            voucher_type=voucher_type,
            value=value,
            currency=currency or self.default_currency,
            issued_date=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=valid_days),
            status=VoucherStatus.ISSUED,
            items_entitled=items_entitled or [],
            qr_code=f"QR-{uuid.uuid4().hex[:16].upper()}"
        )

        self.vouchers[voucher_id] = voucher
        return voucher

    def redeem_voucher(self, voucher_id: str, merchant_id: str,
                       pin: Optional[str] = None) -> Dict[str, Any]:
        """Process voucher redemption."""
        voucher = self.vouchers.get(voucher_id)
        if not voucher:
            return {"success": False, "error": "Voucher not found"}

        if not voucher.is_valid():
            return {"success": False, "error": f"Voucher not valid (status: {voucher.status.value})"}

        merchant = self.merchants.get(merchant_id)
        if not merchant:
            return {"success": False, "error": "Merchant not found"}

        if merchant["status"] != "active":
            return {"success": False, "error": "Merchant not active"}

        # Process redemption
        voucher.status = VoucherStatus.REDEEMED
        voucher.redemption_date = datetime.now()
        voucher.merchant_id = merchant_id
        voucher.redemption_location = merchant["location"]

        merchant["total_redemptions"] += 1
        merchant["total_value_redeemed"] += voucher.value

        redemption_record = {
            "voucher_id": voucher_id,
            "beneficiary_id": voucher.beneficiary_id,
            "merchant_id": merchant_id,
            "value": voucher.value,
            "currency": voucher.currency,
            "redeemed_at": datetime.now().isoformat(),
            "voucher_type": voucher.voucher_type.value
        }
        self.redemption_log.append(redemption_record)

        return {"success": True, "redemption": redemption_record}

    def cancel_voucher(self, voucher_id: str, reason: str) -> bool:
        """Cancel a voucher."""
        if voucher_id in self.vouchers:
            voucher = self.vouchers[voucher_id]
            if voucher.status in (VoucherStatus.CREATED, VoucherStatus.ISSUED):
                voucher.status = VoucherStatus.CANCELLED
                voucher.metadata = {"cancellation_reason": reason}
                return True
        return False

    def report_lost_voucher(self, voucher_id: str) -> bool:
        """Report a voucher as lost."""
        if voucher_id in self.vouchers:
            voucher = self.vouchers[voucher_id]
            if voucher.status == VoucherStatus.ISSUED:
                voucher.status = VoucherStatus.LOST
                return True
        return False

    def get_vouchers_by_beneficiary(self, beneficiary_id: str) -> List[Voucher]:
        """Get all vouchers for a beneficiary."""
        return [v for v in self.vouchers.values() if v.beneficiary_id == beneficiary_id]

    def get_active_vouchers(self) -> List[Voucher]:
        """Get all active (issued) vouchers."""
        return [v for v in self.vouchers.values() if v.status == VoucherStatus.ISSUED]

    def get_statistics(self) -> Dict[str, Any]:
        """Get voucher system statistics."""
        by_status = {}
        by_type = {}
        total_value = 0.0
        total_redeemed_value = 0.0

        for v in self.vouchers.values():
            by_status[v.status.value] = by_status.get(v.status.value, 0) + 1
            by_type[v.voucher_type.value] = by_type.get(v.voucher_type.value, 0) + 1
            total_value += v.value
            if v.status == VoucherStatus.REDEEMED:
                total_redeemed_value += v.value

        return {
            "total_vouchers": len(self.vouchers),
            "by_status": by_status,
            "by_type": by_type,
            "total_value_issued": total_value,
            "total_value_redeemed": total_redeemed_value,
            "redemption_rate": total_redeemed_value / max(total_value, 1),
            "active_merchants": sum(1 for m in self.merchants.values() if m["status"] == "active")
        }


class SupplyChainTracker:
    """Supply chain tracking and logistics management."""

    def __init__(self, tracking_provider: str = "standard"):
        self.tracking_provider = tracking_provider
        self.shipments: Dict[str, Shipment] = {}
        self.warehouses: Dict[str, Warehouse] = {}
        self.inventory: Dict[str, List[AidItem]] = {}  # warehouse_id -> [items]
        self.shipment_counter = 0

    def create_warehouse(self, name: str, location: str, capacity: float,
                         temperature_controlled: bool = False) -> Warehouse:
        """Create a new warehouse."""
        warehouse_id = f"WH-{uuid.uuid4().hex[:8].upper()}"
        warehouse = Warehouse(
            warehouse_id=warehouse_id,
            name=name,
            location=location,
            capacity=capacity,
            temperature_controlled=temperature_controlled,
            operational_since=date.today()
        )
        self.warehouses[warehouse_id] = warehouse
        self.inventory[warehouse_id] = []
        return warehouse

    def receive_inventory(self, warehouse_id: str, items: List[AidItem]) -> Dict[str, Any]:
        """Receive inventory at a warehouse."""
        warehouse = self.warehouses.get(warehouse_id)
        if not warehouse:
            return {"success": False, "error": "Warehouse not found"}

        total_weight = sum(item.total_weight() for item in items)
        if total_weight > warehouse.available_capacity:
            return {"success": False, "error": "Insufficient warehouse capacity"}

        for item in items:
            warehouse.add_inventory(item.total_weight(), WarehouseZone.GENERAL)
            if warehouse_id not in self.inventory:
                self.inventory[warehouse_id] = []
            self.inventory[warehouse_id].append(item)

        return {
            "success": True,
            "warehouse_id": warehouse_id,
            "items_received": len(items),
            "total_weight_kg": total_weight,
            "new_utilization": warehouse.utilization_rate
        }

    def create_shipment(self, origin: str, destination: str,
                        items: List[Dict[str, Any]], carrier: str = "",
                        estimated_days: int = 3) -> Shipment:
        """Create a new shipment."""
        self.shipment_counter += 1
        shipment_id = f"SHP-{datetime.now().strftime('%Y%m')}-{self.shipment_counter:04d}"

        shipment = Shipment(
            shipment_id=shipment_id,
            origin=origin,
            destination=destination,
            items=items,
            carrier=carrier,
            estimated_arrival=datetime.now() + timedelta(days=estimated_days)
        )
        self.shipments[shipment_id] = shipment
        return shipment

    def dispatch_shipment(self, shipment_id: str) -> bool:
        """Mark a shipment as dispatched."""
        if shipment_id in self.shipments:
            shipment = self.shipments[shipment_id]
            if shipment.status == ShipmentStatus.PLANNED:
                shipment.status = ShipmentStatus.DISPATCHED
                shipment.dispatch_date = datetime.now()
                shipment.add_tracking_event(shipment.origin, "dispatched", "Shipment left origin")
                return True
        return False

    def update_shipment_location(self, shipment_id: str, location: str,
                                 notes: str = "") -> bool:
        """Update shipment location."""
        if shipment_id in self.shipments:
            shipment = self.shipments[shipment_id]
            if shipment.status in (ShipmentStatus.DISPATCHED, ShipmentStatus.IN_TRANSIT, ShipmentStatus.AT_CHECKPOINT):
                shipment.status = ShipmentStatus.IN_TRANSIT
                shipment.add_tracking_event(location, "in_transit", notes)
                return True
        return False

    def confirm_delivery(self, shipment_id: str, received_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Confirm shipment delivery."""
        shipment = self.shipments.get(shipment_id)
        if not shipment:
            return {"success": False, "error": "Shipment not found"}

        shipment.status = ShipmentStatus.DELIVERED
        shipment.actual_arrival = datetime.now()
        shipment.add_tracking_event(shipment.destination, "delivered", "Shipment received")

        # Calculate discrepancies
        planned_quantity = sum(item.get("quantity", 0) for item in shipment.items)
        received_quantity = sum(item.get("quantity", 0) for item in received_items)
        discrepancy = planned_quantity - received_quantity

        return {
            "success": True,
            "shipment_id": shipment_id,
            "planned_quantity": planned_quantity,
            "received_quantity": received_quantity,
            "discrepancy": discrepancy,
            "transit_time_hours": shipment.transit_time_hours()
        }

    def get_shipment_tracking(self, shipment_id: str) -> List[Dict[str, Any]]:
        """Get tracking history for a shipment."""
        shipment = self.shipments.get(shipment_id)
        if not shipment:
            return []
        return shipment.tracking_events

    def get_warehouse_inventory(self, warehouse_id: str) -> List[AidItem]:
        """Get inventory items at a warehouse."""
        return self.inventory.get(warehouse_id, [])

    def get_statistics(self) -> Dict[str, Any]:
        """Get supply chain statistics."""
        by_status = {}
        total_shipments = len(self.shipments)
        for s in self.shipments.values():
            by_status[s.status.value] = by_status.get(s.status.value, 0) + 1

        warehouse_stats = {}
        for wh in self.warehouses.values():
            warehouse_stats[wh.warehouse_id] = {
                "name": wh.name,
                "utilization": wh.utilization_rate,
                "capacity": wh.capacity
            }

        return {
            "total_shipments": total_shipments,
            "by_status": by_status,
            "total_warehouses": len(self.warehouses),
            "warehouse_stats": warehouse_stats,
            "total_inventory_items": sum(len(items) for items in self.inventory.values())
        }


class DistributionManager:
    """Distribution site management and monitoring."""

    def __init__(self, distribution_type: str = "mixed"):
        self.distribution_type = distribution_type
        self.sites: Dict[str, DistributionSite] = {}
        self.distributions: List[Dict[str, Any]] = []
        self.site_counter = 0

    def create_distribution_site(self, name: str, location: str,
                                 capacity: int, planned_date: Optional[datetime] = None) -> DistributionSite:
        """Create a new distribution site."""
        self.site_counter += 1
        site_id = f"SITE-{self.site_counter:03d}"

        site = DistributionSite(
            site_id=site_id,
            name=name,
            location=location,
            capacity=capacity,
            planned_date=planned_date,
            setup_checklist={
                "shelter_set_up": False,
                "queues_marked": False,
                "staff_trained": False,
                "items_staged": False,
                "registration_complete": False,
                "safety_measures": False
            }
        )
        self.sites[site_id] = site
        return site

    def setup_distribution_site(self, site_id: str, checklist_items: Dict[str, bool]) -> bool:
        """Update distribution site setup checklist."""
        if site_id in self.sites:
            site = self.sites[site_id]
            site.setup_checklist.update(checklist_items)
            return True
        return False

    def assign_staff(self, site_id: str, staff_ids: List[str]) -> bool:
        """Assign staff to a distribution site."""
        if site_id in self.sites:
            self.sites[site_id].staff_assigned.extend(staff_ids)
            return True
        return False

    def stage_items(self, site_id: str, items: List[Dict[str, Any]]) -> bool:
        """Stage items for distribution."""
        if site_id in self.sites:
            self.sites[site_id].items_available = items
            return True
        return False

    def start_distribution(self, site_id: str) -> bool:
        """Start distribution at a site."""
        if site_id in self.sites:
            site = self.sites[site_id]
            # Check if setup is complete
            if all(site.setup_checklist.values()):
                site.status = DistributionStatus.IN_PROGRESS
                return True
        return False

    def serve_beneficiary(self, site_id: str, beneficiary_id: str,
                          items_received: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Record beneficiary service at distribution."""
        site = self.sites.get(site_id)
        if not site:
            return {"success": False, "error": "Site not found"}

        if site.status != DistributionStatus.IN_PROGRESS:
            return {"success": False, "error": "Distribution not in progress"}

        if not site.serve_beneficiary():
            return {"success": False, "error": "Site at capacity"}

        record = {
            "distribution_id": f"DIST-{uuid.uuid4().hex[:8].upper()}",
            "site_id": site_id,
            "beneficiary_id": beneficiary_id,
            "items_received": items_received,
            "timestamp": datetime.now().isoformat()
        }
        self.distributions.append(record)

        return {"success": True, "record": record}

    def complete_distribution(self, site_id: str) -> Dict[str, Any]:
        """Complete distribution at a site."""
        site = self.sites.get(site_id)
        if not site:
            return {"success": False, "error": "Site not found"}

        site.status = DistributionStatus.COMPLETED
        site_distributions = [d for d in self.distributions if d["site_id"] == site_id]

        return {
            "success": True,
            "site_id": site_id,
            "total_served": site.served_count,
            "completion_rate": site.completion_rate,
            "total_distributions": len(site_distributions)
        }

    def collect_feedback(self, site_id: str, beneficiary_id: str,
                         rating: int, comments: str = "") -> bool:
        """Collect beneficiary feedback."""
        if site_id in self.sites:
            self.sites[site_id].collect_feedback(beneficiary_id, rating, comments)
            return True
        return False

    def get_site_status(self, site_id: str) -> Optional[Dict[str, Any]]:
        """Get distribution site status."""
        if site_id in self.sites:
            return self.sites[site_id].to_dict()
        return None

    def get_all_sites_status(self) -> List[Dict[str, Any]]:
        """Get status of all distribution sites."""
        return [site.to_dict() for site in self.sites.values()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get distribution statistics."""
        by_status = {}
        total_served = 0
        total_capacity = 0

        for site in self.sites.values():
            by_status[site.status.value] = by_status.get(site.status.value, 0) + 1
            total_served += site.served_count
            total_capacity += site.capacity

        return {
            "total_sites": len(self.sites),
            "by_status": by_status,
            "total_beneficiaries_served": total_served,
            "total_capacity": total_capacity,
            "overall_completion_rate": total_served / max(total_capacity, 1),
            "total_distributions": len(self.distributions)
        }


# =============================================================================
# Main Demo Function
# =============================================================================

def main() -> None:
    """Demonstrate the aid distribution system capabilities."""
    print("=" * 70)
    print("  AID DISTRIBUTION SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # --- Beneficiary Registration ---
    print("\n[1] BENEFICIARY REGISTRATION")
    print("-" * 40)
    registry = BeneficiaryRegistry(database="demo_aid_db")

    beneficiaries_data = [
        {"household_size": 5, "name": "Amina Hassan", "location": "Zone_A",
         "needs": [NeedCategory.FOOD, NeedCategory.WATER, NeedCategory.SHELTER],
         "vulnerability_score": 0.85, "phone": "+254-700-123456"},
        {"household_size": 3, "name": "Jean Baptiste", "location": "Zone_A",
         "needs": [NeedCategory.FOOD, NeedCategory.HEALTH],
         "vulnerability_score": 0.65},
        {"household_size": 7, "name": "Fatima Al-Said", "location": "Zone_B",
         "needs": [NeedCategory.FOOD, NeedCategory.WATER, NeedCategory.WASH, NeedCategory.HEALTH],
         "vulnerability_score": 0.92, "phone": "+254-700-789012"},
        {"household_size": 2, "name": "Li Wei", "location": "Zone_B",
         "needs": [NeedCategory.FOOD, NeedCategory.EDUCATION],
         "vulnerability_score": 0.45},
        {"household_size": 4, "name": "Maria Santos", "location": "Zone_C",
         "needs": [NeedCategory.FOOD, NeedCategory.WATER, NeedCategory.SHELTER, NeedCategory.LIVELIHOOD],
         "vulnerability_score": 0.78},
    ]

    registered = []
    for data in beneficiaries_data:
        beneficiary = registry.register_beneficiary(
            household_size=data["household_size"],
            head_of_household_name=data["name"],
            location=data["location"],
            needs=data["needs"],
            vulnerability_score=data["vulnerability_score"],
            contact_phone=data.get("phone"),
            id_document_type="national_id",
            id_document_number=f"ID-{random.randint(100000, 999999)}"
        )
        registry.verify_beneficiary(beneficiary.beneficiary_id)
        registry.activate_beneficiary(beneficiary.beneficiary_id)
        registered.append(beneficiary)
        print(f"  Registered: {beneficiary.head_of_household_name} (ID: {beneficiary.beneficiary_id})")
        print(f"    Household: {beneficiary.household_size}, Vulnerability: {beneficiary.vulnerability_level.value}")

    stats = registry.get_statistics()
    print(f"\n  Registration Statistics:")
    print(f"    Total beneficiaries: {stats['total_beneficiaries']}")
    print(f"    Total household members: {stats['total_household_members']}")
    print(f"    By vulnerability: {stats['by_vulnerability']}")

    # --- Voucher System ---
    print("\n\n[2] VOUCHER SYSTEM")
    print("-" * 40)
    voucher_system = VoucherManagementSystem(digital_enabled=True)

    # Register merchants
    merchants = [
        ("MERC-001", "Food Store Alpha", "Zone_A", [VoucherType.FOOD, VoucherType.MULTI_PURPOSE]),
        ("MERC-002", "Pharmacy Beta", "Zone_B", [VoucherType.HEALTH]),
        ("MERC-003", "General Shop Gamma", "Zone_C", [VoucherType.MULTI_PURPOSE, VoucherType.CASH]),
    ]
    for mid, name, loc, types in merchants:
        voucher_system.register_merchant(mid, name, loc, types)
        print(f"  Registered merchant: {name} ({', '.join([t.value for t in types])})")

    # Issue vouchers
    print("\n  Issuing vouchers...")
    vouchers = []
    for beneficiary in registered:
        voucher = voucher_system.issue_voucher(
            beneficiary_id=beneficiary.beneficiary_id,
            voucher_type=VoucherType.MULTI_PURPOSE,
            value=beneficiary.household_size * 30,  # $30 per person
            valid_days=30
        )
        vouchers.append(voucher)
        print(f"    {beneficiary.head_of_household_name}: ${voucher.value:.2f} (expires in {voucher.days_until_expiry()} days)")

    # Redeem some vouchers
    print("\n  Processing redemptions...")
    for i, voucher in enumerate(vouchers[:3]):
        merchant_id = merchants[i % len(merchants)][0]
        result = voucher_system.redeem_voucher(voucher.voucher_id, merchant_id)
        if result["success"]:
            print(f"    Voucher {voucher.voucher_id}: ${voucher.value:.2f} redeemed at {merchant_id}")

    v_stats = voucher_system.get_statistics()
    print(f"\n  Voucher Statistics:")
    print(f"    Total vouchers: {v_stats['total_vouchers']}")
    print(f"    Redemption rate: {v_stats['redemption_rate']:.1%}")
    print(f"    Total value redeemed: ${v_stats['total_value_redeemed']:.2f}")

    # --- Supply Chain Tracking ---
    print("\n\n[3] SUPPLY CHAIN TRACKING")
    print("-" * 40)
    supply_chain = SupplyChainTracker(tracking_provider="blockchain")

    # Create warehouses
    wh1 = supply_chain.create_warehouse("Regional Hub", "Nairobi", 5000, temperature_controlled=True)
    wh2 = supply_chain.create_warehouse("Field Warehouse", "Dadaab", 2000)
    print(f"  Created warehouse: {wh1.name} (capacity: {wh1.capacity}MT)")
    print(f"  Created warehouse: {wh2.name} (capacity: {wh2.capacity}MT)")

    # Receive inventory
    items = [
        AidItem(f"ITEM-{uuid.uuid4().hex[:6].upper()}", ItemType.RICE, "Fortified Rice", 500, "kg",
                weight_kg=1.0, expiry_date=date(2025, 6, 30), batch_number="BATCH-001", cost_per_unit=0.80),
        AidItem(f"ITEM-{uuid.uuid4().hex[:6].upper()}", ItemType.OIL, "Vegetable Oil", 200, "liters",
                weight_kg=0.92, expiry_date=date(2025, 3, 31), batch_number="BATCH-002", cost_per_unit=1.50),
        AidItem(f"ITEM-{uuid.uuid4().hex[:6].upper()}", ItemType.HYGIENE_KIT, "Standard Hygiene Kit", 100, "units",
                weight_kg=2.5, batch_number="BATCH-003", cost_per_unit=15.00),
    ]
    receive_result = supply_chain.receive_inventory(wh1.warehouse_id, items)
    print(f"\n  Received inventory at {wh1.name}: {receive_result['items_received']} items ({receive_result['total_weight_kg']:.1f} kg)")

    # Create and track shipment
    shipment = supply_chain.create_shipment(
        origin=wh1.warehouse_id,
        destination=wh2.warehouse_id,
        items=[{"item_type": "rice", "quantity": 200, "unit": "kg"},
               {"item_type": "oil", "quantity": 50, "unit": "liters"}],
        carrier="Logistics Co.",
        estimated_days=2
    )
    print(f"\n  Created shipment: {shipment.shipment_id}")

    supply_chain.dispatch_shipment(shipment.shipment_id)
    print(f"  Dispatched: {shipment.shipment_id}")

    supply_chain.update_shipment_location(shipment.shipment_id, "Transit Point Alpha", "On schedule")
    supply_chain.update_shipment_location(shipment.shipment_id, "Transit Point Beta", "Arriving soon")

    delivery = supply_chain.confirm_delivery(shipment.shipment_id, shipment.items)
    print(f"  Delivered: {shipment.shipment_id} (transit time: {delivery['transit_time_hours']:.1f} hours)")

    sc_stats = supply_chain.get_statistics()
    print(f"\n  Supply Chain Statistics:")
    print(f"    Total shipments: {sc_stats['total_shipments']}")
    print(f"    Warehouses: {sc_stats['total_warehouses']}")
    print(f"    By status: {sc_stats['by_status']}")

    # --- Distribution Management ---
    print("\n\n[4] DISTRIBUTION MANAGEMENT")
    print("-" * 40)
    distributor = DistributionManager(distribution_type="mixed")

    # Create distribution sites
    sites = [
        ("Distribution Center A", "Zone_A", 200),
        ("Distribution Center B", "Zone_B", 150),
        ("Mobile Distribution Unit", "Zone_C", 75),
    ]
    for name, loc, capacity in sites:
        site = distributor.create_distribution_site(name, loc, capacity)
        print(f"  Created site: {site.name} (capacity: {site.capacity})")

        # Setup site
        distributor.setup_distribution_site(site.site_id, {
            "shelter_set_up": True,
            "queues_marked": True,
            "staff_trained": True,
            "items_staged": True,
            "registration_complete": True,
            "safety_measures": True
        })

        # Assign staff
        distributor.assign_staff(site.site_id, [f"STAFF-{i}" for i in range(1, 4)])

        # Stage items
        distributor.stage_items(site.site_id, [
            {"item_type": "rice", "quantity": 100, "unit": "kg"},
            {"item_type": "oil", "quantity": 30, "unit": "liters"},
            {"item_type": "hygiene_kit", "quantity": 50, "unit": "units"},
        ])

        # Start distribution
        distributor.start_distribution(site.site_id)
        print(f"    Started distribution at {site.name}")

    # Serve beneficiaries
    print("\n  Serving beneficiaries...")
    for site_id, site in distributor.sites.items():
        site_beneficiaries = [b for b in registered if b.location == site.location.replace("Distribution Center ", "").replace("Mobile Distribution Unit", "Zone_C")]
        for beneficiary in site_beneficiaries[:2]:
            result = distributor.serve_beneficiary(site_id, beneficiary.beneficiary_id, [
                {"item_type": "rice", "quantity": beneficiary.household_size * 5, "unit": "kg"},
                {"item_type": "oil", "quantity": beneficiary.household_size * 1, "unit": "liters"},
            ])
            if result["success"]:
                print(f"    Served {beneficiary.head_of_household_name} at {site.name}")

        # Collect feedback
        distributor.collect_feedback(site_id, "BEN-001", 5, "Good service, short wait time")
        distributor.collect_feedback(site_id, "BEN-002", 4, "Efficient process")

    # Complete distributions
    print("\n  Completing distributions...")
    for site_id, site in distributor.sites.items():
        result = distributor.complete_distribution(site_id)
        if result["success"]:
            print(f"    {site.name}: {result['total_beneficiaries_served']} served ({result['completion_rate']:.1%})")

    dist_stats = distributor.get_statistics()
    print(f"\n  Distribution Statistics:")
    print(f"    Total sites: {dist_stats['total_sites']}")
    print(f"    Total served: {dist_stats['total_beneficiaries_served']}")
    print(f"    Overall completion rate: {dist_stats['overall_completion_rate']:.1%}")

    # --- Summary ---
    print("\n\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n  Components demonstrated:")
    print("    1. Beneficiary Registration - registration, verification, activation")
    print("    2. Voucher System - issuance, redemption, merchant management")
    print("    3. Supply Chain Tracking - warehouses, shipments, delivery confirmation")
    print("    4. Distribution Management - site setup, service, feedback collection")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()