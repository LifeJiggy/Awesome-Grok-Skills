"""E-Commerce Agent — Full-stack platform management.

Covers product catalogs, shopping carts, order processing, payment handling,
inventory management, dynamic pricing, fraud detection, and customer
relationship management for modern e-commerce operations.
"""

import logging
import hashlib
import uuid
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Union
from uuid import uuid4

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ProductStatus(Enum):
    """Product lifecycle states."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"
    PREORDER = "preorder"
    COMING_SOON = "coming_soon"


class OrderStatus(Enum):
    """Order processing states."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    REFUNDED = "refunded"
    ON_HOLD = "on_hold"
    FAILED = "failed"


class PaymentStatus(Enum):
    """Payment processing states."""
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    SETTLED = "settled"
    DECLINED = "declined"
    REFUNDED = "refunded"
    CHARGEBACK = "chargeback"
    VOIDED = "voided"


class PaymentMethod(Enum):
    """Supported payment methods."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"
    BUY_NOW_PAY_LATER = "bnpl"
    STORE_CREDIT = "store_credit"
    GIFT_CARD = "gift_card"


class ShippingMethod(Enum):
    """Shipping options."""
    STANDARD = "standard"
    EXPEDITED = "expedited"
    OVERNIGHT = "overnight"
    SAME_DAY = "same_day"
    PICKUP = "pickup"
    FREE_SHIPPING = "free_shipping"


class DiscountType(Enum):
    """Discount calculation types."""
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    FREE_SHIPPING = "free_shipping"
    BUY_X_GET_Y = "bogo"
    TIERED = "tiered"


class CustomerSegment(Enum):
    """Customer segmentation categories."""
    NEW = "new"
    RETURNING = "returning"
    VIP = "vip"
    AT_RISK = "at_risk"
    DORMANT = "dormant"
    LOYAL = "loyal"
    WHOLESALE = "wholesale"
    EMPLOYEE = "employee"


class FraudRiskLevel(Enum):
    """Transaction risk assessment levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InventoryMovement(Enum):
    """Types of inventory adjustments."""
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"
    DAMAGE = "damage"
    THEFT = "theft"
    RESERVATION = "reservation"
    RELEASE = "release"


class TaxType(Enum):
    """Tax calculation types."""
    SALES_TAX = "sales_tax"
    VAT = "vat"
    GST = "gst"
    EXCISE = "excise"
    IMPORT_DUTY = "import_duty"
    WITHHOLDING = "withholding"


class CouponType(Enum):
    """Coupon and promotion types."""
    PERCENTAGE_OFF = "percentage_off"
    FIXED_OFF = "fixed_off"
    FREE_SHIPPING = "free_shipping"
    BOGO = "bogo"
    GIFT_WITH_PURCHASE = "gwp"
    TIERED_DISCOUNT = "tiered"
    LOYALTY_POINTS = "loyalty_points"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Money:
    """Monetary value with currency."""
    amount: float = 0.0
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: float) -> "Money":
        return Money(self.amount * factor, self.currency)

    def __repr__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"

    def is_positive(self) -> bool:
        return self.amount > 0

    def is_zero(self) -> bool:
        return abs(self.amount) < 0.001

    def to_cents(self) -> int:
        return int(round(self.amount * 100))


@dataclass
class Address:
    """Shipping or billing address."""
    address_id: str = field(default_factory=lambda: str(uuid4()))
    line1: str = ""
    line2: str = ""
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = "US"
    phone: str = ""
    is_default: bool = False

    def to_dict(self) -> Dict[str, str]:
        return {
            "line1": self.line1,
            "line2": self.line2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "phone": self.phone,
        }

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.line1:
            errors.append("Address line 1 is required")
        if not self.city:
            errors.append("City is required")
        if not self.postal_code:
            errors.append("Postal code is required")
        if not self.country:
            errors.append("Country is required")
        return errors


@dataclass
class ProductVariant:
    """A variant of a product (size, color, etc.)."""
    variant_id: str = field(default_factory=lambda: str(uuid4()))
    sku: str = ""
    name: str = ""
    attributes: Dict[str, str] = field(default_factory=dict)
    price: float = 0.0
    compare_at_price: Optional[float] = None
    weight: float = 0.0
    weight_unit: str = "lb"
    barcode: Optional[str] = None
    image_url: Optional[str] = None
    stock_quantity: int = 0
    is_active: bool = True

    @property
    def is_on_sale(self) -> bool:
        return (
            self.compare_at_price is not None
            and self.compare_at_price > self.price
        )

    @property
    def discount_percent(self) -> float:
        if not self.is_on_sale or not self.compare_at_price:
            return 0.0
        return (1 - self.price / self.compare_at_price) * 100

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.sku:
            errors.append("SKU is required")
        if self.price < 0:
            errors.append("Price cannot be negative")
        if self.stock_quantity < 0:
            errors.append("Stock quantity cannot be negative")
        return errors


@dataclass
class Product:
    """A product in the catalog."""
    product_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    slug: str = ""
    description: str = ""
    short_description: str = ""
    category: str = ""
    subcategory: str = ""
    tags: List[str] = field(default_factory=list)
    brand: str = ""
    variants: List[ProductVariant] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    status: ProductStatus = ProductStatus.DRAFT
    price: float = 0.0
    compare_at_price: Optional[float] = None
    cost: float = 0.0
    weight: float = 0.0
    weight_unit: str = "lb"
    requires_shipping: bool = True
    is_taxable: bool = True
    seo_title: str = ""
    seo_description: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def is_active(self) -> bool:
        return self.status == ProductStatus.ACTIVE

    @property
    def primary_image(self) -> Optional[str]:
        return self.images[0] if self.images else None

    @property
    def min_price(self) -> float:
        if self.variants:
            return min(v.price for v in self.variants if v.is_active)
        return self.price

    @property
    def max_price(self) -> float:
        if self.variants:
            return max(v.price for v in self.variants if v.is_active)
        return self.price

    @property
    def total_stock(self) -> int:
        if self.variants:
            return sum(v.stock_quantity for v in self.variants)
        return 0

    @property
    def is_in_stock(self) -> bool:
        return self.total_stock > 0

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.name:
            errors.append("Product name is required")
        if not self.slug:
            self.slug = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
        if self.price < 0:
            errors.append("Price cannot be negative")
        for variant in self.variants:
            for err in variant.validate():
                errors.append(f"Variant '{variant.name}': {err}")
        return errors


@dataclass
class CartItem:
    """An item in a shopping cart."""
    item_id: str = field(default_factory=lambda: str(uuid4()))
    product_id: str = ""
    variant_id: Optional[str] = None
    quantity: int = 1
    price: float = 0.0
    name: str = ""
    image_url: Optional[str] = None
    added_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def line_total(self) -> float:
        return self.price * self.quantity

    def validate(self, available_stock: int = 999999) -> List[str]:
        errors: List[str] = []
        if self.quantity <= 0:
            errors.append("Quantity must be positive")
        if self.quantity > available_stock:
            errors.append(f"Only {available_stock} available in stock")
        return errors


@dataclass
class ShoppingCart:
    """A customer shopping cart."""
    cart_id: str = field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    items: List[CartItem] = field(default_factory=list)
    coupon_codes: List[str] = field(default_factory=list)
    shipping_address: Optional[Address] = None
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0

    def get_item(self, product_id: str, variant_id: Optional[str] = None) -> Optional[CartItem]:
        for item in self.items:
            if item.product_id == product_id:
                if variant_id is None or item.variant_id == variant_id:
                    return item
        return None


@dataclass
class Discount:
    """A discount or coupon."""
    discount_id: str = field(default_factory=lambda: str(uuid4()))
    code: str = ""
    name: str = ""
    description: str = ""
    discount_type: DiscountType = DiscountType.PERCENTAGE
    value: float = 0.0
    min_order_amount: float = 0.0
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    usage_count: int = 0
    per_user_limit: Optional[int] = None
    applies_to: str = "all"
    category: Optional[str] = None
    product_ids: List[str] = field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    stackable: bool = False

    @property
    def is_valid(self) -> bool:
        if not self.is_active:
            return False
        now = datetime.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
        return True

    def calculate_discount(self, subtotal: float) -> float:
        if not self.is_valid:
            return 0.0
        if subtotal < self.min_order_amount:
            return 0.0
        if self.discount_type == DiscountType.PERCENTAGE:
            discount = subtotal * (self.value / 100)
        elif self.discount_type == DiscountType.FIXED:
            discount = self.value
        elif self.discount_type == DiscountType.FREE_SHIPPING:
            return 0.0
        else:
            discount = 0.0
        if self.max_discount_amount:
            discount = min(discount, self.max_discount_amount)
        return round(discount, 2)


@dataclass
class Order:
    """A customer order."""
    order_id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    items: List[CartItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_method: Optional[PaymentMethod] = None
    shipping_address: Optional[Address] = None
    billing_address: Optional[Address] = None
    shipping_method: ShippingMethod = ShippingMethod.STANDARD
    subtotal: float = 0.0
    discount_amount: float = 0.0
    shipping_cost: float = 0.0
    tax_amount: float = 0.0
    total: float = 0.0
    currency: str = "USD"
    notes: str = ""
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def is_paid(self) -> bool:
        return self.payment_status in (
            PaymentStatus.AUTHORIZED,
            PaymentStatus.CAPTURED,
            PaymentStatus.SETTLED,
        )

    @property
    def is_shipped(self) -> bool:
        return self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED)

    @property
    def can_cancel(self) -> bool:
        return self.status in (OrderStatus.PENDING, OrderStatus.CONFIRMED)

    @property
    def can_refund(self) -> bool:
        return self.payment_status in (
            PaymentStatus.CAPTURED,
            PaymentStatus.SETTLED,
        )

    def calculate_totals(
        self,
        tax_rate: float = 0.0,
        shipping_cost: float = 0.0,
        discount_amount: float = 0.0,
    ) -> None:
        self.subtotal = sum(item.line_total for item in self.items)
        self.discount_amount = discount_amount
        self.shipping_cost = shipping_cost
        taxable = max(self.subtotal - discount_amount, 0)
        self.tax_amount = round(taxable * tax_rate, 2)
        self.total = round(
            self.subtotal - discount_amount + shipping_cost + self.tax_amount,
            2,
        )


@dataclass
class Customer:
    """Customer profile."""
    customer_id: str = field(default_factory=lambda: str(uuid4()))
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    addresses: List[Address] = field(default_factory=list)
    segment: CustomerSegment = CustomerSegment.NEW
    total_orders: int = 0
    total_spent: float = 0.0
    loyalty_points: int = 0
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_order_at: Optional[datetime] = None
    is_active: bool = True

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def average_order_value(self) -> float:
        return self.total_spent / self.total_orders if self.total_orders else 0

    def add_order(self, amount: float) -> None:
        self.total_orders += 1
        self.total_spent += amount
        self.last_order_at = datetime.now()
        self.loyalty_points += int(amount)

    def get_default_address(self) -> Optional[Address]:
        for addr in self.addresses:
            if addr.is_default:
                return addr
        return self.addresses[0] if self.addresses else None


@dataclass
class FraudAssessment:
    """Fraud detection result."""
    assessment_id: str = field(default_factory=lambda: str(uuid4()))
    transaction_id: str = ""
    risk_level: FraudRiskLevel = FraudRiskLevel.LOW
    risk_score: float = 0.0
    flags: List[str] = field(default_factory=list)
    recommended_action: str = "approve"
    assessed_at: datetime = field(default_factory=datetime.now)


@dataclass
class TaxRate:
    """Tax rate configuration."""
    rate_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    rate_type: TaxType = TaxType.SALES_TAX
    rate: float = 0.0
    country: str = ""
    state: str = ""
    city: str = ""
    postal_code: str = ""
    product_category: Optional[str] = None
    is_compound: bool = False

    def calculate_tax(self, amount: float) -> float:
        return round(amount * self.rate, 2)


# ---------------------------------------------------------------------------
# Core Engine Classes
# ---------------------------------------------------------------------------

class ProductCatalog:
    """Product catalog management — search, filter, and organize products."""

    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}
        self._categories: Dict[str, List[str]] = {}
        self._tags_index: Dict[str, List[str]] = {}
        logger.info("ProductCatalog initialized")

    def add_product(self, product: Product) -> str:
        errors = product.validate()
        if errors:
            raise ValueError(f"Product validation failed: {errors}")
        self._products[product.product_id] = product
        if product.category:
            self._categories.setdefault(product.category, []).append(product.product_id)
        for tag in product.tags:
            self._tags_index.setdefault(tag, []).append(product.product_id)
        logger.info("Product added: %s (%s)", product.name, product.product_id)
        return product.product_id

    def update_product(self, product_id: str, updates: Dict[str, Any]) -> Optional[Product]:
        product = self._products.get(product_id)
        if not product:
            return None
        for key, value in updates.items():
            if hasattr(product, key):
                setattr(product, key, value)
        product.updated_at = datetime.now()
        return product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def delete_product(self, product_id: str) -> bool:
        if product_id not in self._products:
            return False
        del self._products[product_id]
        return True

    def search_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        tags: Optional[List[str]] = None,
        status: Optional[ProductStatus] = None,
        in_stock_only: bool = False,
        sort_by: str = "name",
        limit: int = 50,
        offset: int = 0,
    ) -> List[Product]:
        results = list(self._products.values())
        if query:
            q = query.lower()
            results = [
                p for p in results
                if q in p.name.lower()
                or q in p.description.lower()
                or q in p.category.lower()
                or any(q in t.lower() for t in p.tags)
            ]
        if category:
            results = [p for p in results if p.category == category]
        if min_price is not None:
            results = [p for p in results if p.price >= min_price]
        if max_price is not None:
            results = [p for p in results if p.price <= max_price]
        if tags:
            results = [
                p for p in results if any(t in p.tags for t in tags)
            ]
        if status:
            results = [p for p in results if p.status == status]
        if in_stock_only:
            results = [p for p in results if p.is_in_stock]
        sort_keys = {
            "name": lambda p: p.name.lower(),
            "price": lambda p: p.price,
            "created": lambda p: p.created_at,
            "stock": lambda p: p.total_stock,
        }
        if sort_by in sort_keys:
            results.sort(key=sort_keys[sort_by])
        return results[offset: offset + limit]

    def get_categories(self) -> Dict[str, int]:
        return {
            cat: len(product_ids)
            for cat, product_ids in self._categories.items()
        }

    def get_products_by_category(self, category: str) -> List[Product]:
        product_ids = self._categories.get(category, [])
        return [self._products[pid] for pid in product_ids if pid in self._products]

    def bulk_update_status(
        self, product_ids: List[str], new_status: ProductStatus
    ) -> int:
        count = 0
        for pid in product_ids:
            if pid in self._products:
                self._products[pid].status = new_status
                self._products[pid].updated_at = datetime.now()
                count += 1
        return count

    def get_catalog_stats(self) -> Dict[str, Any]:
        products = list(self._products.values())
        active = [p for p in products if p.status == ProductStatus.ACTIVE]
        out_of_stock = [p for p in products if not p.is_in_stock]
        total_value = sum(p.price * p.total_stock for p in products)
        return {
            "total_products": len(products),
            "active_products": len(active),
            "out_of_stock": len(out_of_stock),
            "categories": len(self._categories),
            "total_inventory_value": round(total_value, 2),
        }


class ShoppingCartManager:
    """Shopping cart operations — add, remove, calculate totals."""

    def __init__(self, catalog: ProductCatalog) -> None:
        self._carts: Dict[str, ShoppingCart] = {}
        self._catalog = catalog
        logger.info("ShoppingCartManager initialized")

    def create_cart(
        self, user_id: Optional[str] = None, session_id: Optional[str] = None
    ) -> ShoppingCart:
        cart = ShoppingCart(user_id=user_id, session_id=session_id)
        self._carts[cart.cart_id] = cart
        return cart

    def get_cart(self, cart_id: str) -> Optional[ShoppingCart]:
        return self._carts.get(cart_id)

    def add_item(
        self,
        cart_id: str,
        product_id: str,
        quantity: int = 1,
        variant_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        cart = self._carts.get(cart_id)
        if not cart:
            return {"error": "Cart not found"}
        product = self._catalog.get_product(product_id)
        if not product:
            return {"error": "Product not found"}
        if not product.is_in_stock:
            return {"error": "Product is out of stock"}
        existing = cart.get_item(product_id, variant_id)
        price = product.price
        if variant_id:
            variant = next(
                (v for v in product.variants if v.variant_id == variant_id),
                None,
            )
            if variant:
                price = variant.price
        if existing:
            existing.quantity += quantity
        else:
            item = CartItem(
                product_id=product_id,
                variant_id=variant_id,
                quantity=quantity,
                price=price,
                name=product.name,
                image_url=product.primary_image,
            )
            cart.items.append(item)
        cart.updated_at = datetime.now()
        return {"status": "added", "item_count": cart.item_count}

    def remove_item(
        self, cart_id: str, product_id: str, variant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        cart = self._carts.get(cart_id)
        if not cart:
            return {"error": "Cart not found"}
        cart.items = [
            item for item in cart.items
            if not (item.product_id == product_id and item.variant_id == variant_id)
        ]
        cart.updated_at = datetime.now()
        return {"status": "removed", "item_count": cart.item_count}

    def update_quantity(
        self, cart_id: str, product_id: str, quantity: int, variant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        cart = self._carts.get(cart_id)
        if not cart:
            return {"error": "Cart not found"}
        item = cart.get_item(product_id, variant_id)
        if not item:
            return {"error": "Item not in cart"}
        if quantity <= 0:
            return self.remove_item(cart_id, product_id, variant_id)
        item.quantity = quantity
        cart.updated_at = datetime.now()
        return {"status": "updated", "quantity": quantity}

    def calculate_total(
        self,
        cart_id: str,
        tax_rate: float = 0.0,
        shipping_cost: float = 0.0,
        discount_amount: float = 0.0,
    ) -> Dict[str, float]:
        cart = self._carts.get(cart_id)
        if not cart:
            return {"error": "Cart not found"}
        subtotal = sum(item.line_total for item in cart.items)
        tax = round(subtotal * tax_rate, 2)
        total = round(subtotal + tax + shipping_cost - discount_amount, 2)
        return {
            "subtotal": round(subtotal, 2),
            "tax": tax,
            "shipping": shipping_cost,
            "discount": discount_amount,
            "total": max(total, 0),
            "item_count": cart.item_count,
        }

    def clear_cart(self, cart_id: str) -> bool:
        cart = self._carts.get(cart_id)
        if not cart:
            return False
        cart.items.clear()
        cart.coupon_codes.clear()
        cart.updated_at = datetime.now()
        return True


class OrderManager:
    """Order creation, processing, status updates, and fulfillment."""

    def __init__(self) -> None:
        self._orders: Dict[str, Order] = {}
        self._user_orders: Dict[str, List[str]] = {}
        self._fulfillment_queue: List[str] = []
        logger.info("OrderManager initialized")

    def create_order(
        self,
        user_id: str,
        items: List[CartItem],
        shipping_address: Address,
        billing_address: Optional[Address] = None,
        payment_method: Optional[PaymentMethod] = None,
        shipping_method: ShippingMethod = ShippingMethod.STANDARD,
        tax_rate: float = 0.0,
        shipping_cost: float = 0.0,
        discount_amount: float = 0.0,
    ) -> Order:
        order = Order(
            user_id=user_id,
            items=list(items),
            shipping_address=shipping_address,
            billing_address=billing_address or shipping_address,
            payment_method=payment_method,
            shipping_method=shipping_method,
        )
        order.calculate_totals(tax_rate, shipping_cost, discount_amount)
        self._orders[order.order_id] = order
        self._user_orders.setdefault(user_id, []).append(order.order_id)
        self._fulfillment_queue.append(order.order_id)
        logger.info("Order created: %s (total: %.2f)", order.order_id, order.total)
        return order

    def update_order_status(self, order_id: str, status: OrderStatus) -> bool:
        order = self._orders.get(order_id)
        if not order:
            return False
        order.status = status
        order.updated_at = datetime.now()
        if status == OrderStatus.SHIPPED:
            order.shipped_at = datetime.now()
        elif status == OrderStatus.DELIVERED:
            order.delivered_at = datetime.now()
        return True

    def update_payment_status(
        self, order_id: str, payment_status: PaymentStatus
    ) -> bool:
        order = self._orders.get(order_id)
        if not order:
            return False
        order.payment_status = payment_status
        order.updated_at = datetime.now()
        return True

    def add_tracking_number(self, order_id: str, tracking_number: str) -> bool:
        order = self._orders.get(order_id)
        if not order:
            return False
        order.tracking_number = tracking_number
        order.updated_at = datetime.now()
        return True

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        order = self._orders.get(order_id)
        if not order:
            return {"error": "Order not found"}
        if not order.can_cancel:
            return {"error": f"Cannot cancel order in {order.status.value} status"}
        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.now()
        return {"status": "cancelled", "order_id": order_id}

    def refund_order(self, order_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        order = self._orders.get(order_id)
        if not order:
            return {"error": "Order not found"}
        if not order.can_refund:
            return {"error": "Order cannot be refunded"}
        refund_amount = amount or order.total
        order.payment_status = PaymentStatus.REFUNDED
        order.status = OrderStatus.REFUNDED
        order.updated_at = datetime.now()
        return {
            "status": "refunded",
            "order_id": order_id,
            "amount": refund_amount,
        }

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def get_user_orders(self, user_id: str) -> List[Order]:
        order_ids = self._user_orders.get(user_id, [])
        return [self._orders[oid] for oid in order_ids if oid in self._orders]

    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        return [
            o for o in self._orders.values() if o.status == status
        ]

    def get_fulfillment_queue(self) -> List[Dict[str, Any]]:
        return [
            {
                "order_id": oid,
                "status": self._orders[oid].status.value,
                "items": len(self._orders[oid].items),
                "total": self._orders[oid].total,
                "created_at": self._orders[oid].created_at.isoformat(),
            }
            for oid in self._fulfillment_queue
            if oid in self._orders
            and self._orders[oid].status
            in (OrderStatus.CONFIRMED, OrderStatus.PROCESSING)
        ]

    def get_order_stats(self) -> Dict[str, Any]:
        orders = list(self._orders.values())
        return {
            "total_orders": len(orders),
            "pending": len([o for o in orders if o.status == OrderStatus.PENDING]),
            "processing": len([o for o in orders if o.status == OrderStatus.PROCESSING]),
            "shipped": len([o for o in orders if o.status == OrderStatus.SHIPPED]),
            "delivered": len([o for o in orders if o.status == OrderStatus.DELIVERED]),
            "cancelled": len([o for o in orders if o.status == OrderStatus.CANCELLED]),
            "total_revenue": sum(o.total for o in orders if o.is_paid),
            "average_order_value": (
                sum(o.total for o in orders if o.is_paid)
                / max(len([o for o in orders if o.is_paid]), 1)
            ),
        }


class PricingEngine:
    """Dynamic pricing, discounts, coupons, and bundle pricing."""

    def __init__(self) -> None:
        self._discounts: Dict[str, Discount] = {}
        self._pricing_rules: List[Dict[str, Any]] = []
        logger.info("PricingEngine initialized")

    def create_discount(
        self,
        code: str,
        name: str,
        discount_type: DiscountType,
        value: float,
        min_order_amount: float = 0.0,
        usage_limit: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Discount:
        discount = Discount(
            code=code.upper(),
            name=name,
            discount_type=discount_type,
            value=value,
            min_order_amount=min_order_amount,
            usage_limit=usage_limit,
            start_date=start_date,
            end_date=end_date,
        )
        self._discounts[discount.discount_id] = discount
        return discount

    def apply_discount(
        self, discount_id: str, subtotal: float
    ) -> Dict[str, float]:
        discount = self._discounts.get(discount_id)
        if not discount:
            return {"error": "Discount not found", "discount_amount": 0}
        discount_amount = discount.calculate_discount(subtotal)
        return {"discount_amount": discount_amount, "code": discount.code}

    def validate_coupon(self, code: str) -> Dict[str, Any]:
        for discount in self._discounts.values():
            if discount.code == code.upper():
                return {
                    "valid": discount.is_valid,
                    "type": discount.discount_type.value,
                    "value": discount.value,
                    "min_order": discount.min_order_amount,
                }
        return {"valid": False, "error": "Coupon not found"}

    def calculate_bundle_price(
        self, items: List[Dict[str, Any]], bundle_discount_percent: float = 10.0
    ) -> Dict[str, float]:
        subtotal = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
        bundle_discount = subtotal * (bundle_discount_percent / 100)
        return {
            "original_total": round(subtotal, 2),
            "bundle_discount": round(bundle_discount, 2),
            "bundle_price": round(subtotal - bundle_discount, 2),
        }

    def calculate_tiered_discount(
        self, amount: float, tiers: List[Tuple[float, float]]
    ) -> float:
        for threshold, discount_pct in sorted(tiers, key=lambda t: t[0], reverse=True):
            if amount >= threshold:
                return round(amount * (discount_pct / 100), 2)
        return 0.0

    def get_discount_stats(self) -> Dict[str, Any]:
        discounts = list(self._discounts.values())
        return {
            "total_discounts": len(discounts),
            "active_discounts": len([d for d in discounts if d.is_valid]),
            "total_usage": sum(d.usage_count for d in discounts),
        }


class InventoryManager:
    """Inventory tracking, reservations, and low-stock alerts."""

    def __init__(self) -> None:
        self._inventory: Dict[str, Dict[str, Any]] = {}
        self._movements: List[Dict[str, Any]] = []
        self._alerts: List[Dict[str, Any]] = []
        logger.info("InventoryManager initialized")

    def adjust_stock(
        self,
        product_id: str,
        quantity_change: int,
        movement_type: InventoryMovement = InventoryMovement.ADJUSTMENT,
        reason: str = "",
        reference_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if product_id not in self._inventory:
            self._inventory[product_id] = {
                "quantity": 0,
                "reserved": 0,
                "low_stock_threshold": 10,
                "reorder_point": 20,
                "reorder_quantity": 50,
            }
        inv = self._inventory[product_id]
        old_quantity = inv["quantity"]
        inv["quantity"] += quantity_change
        movement = {
            "product_id": product_id,
            "movement_type": movement_type.value,
            "quantity_change": quantity_change,
            "old_quantity": old_quantity,
            "new_quantity": inv["quantity"],
            "reason": reason,
            "reference_id": reference_id,
            "timestamp": datetime.now().isoformat(),
        }
        self._movements.append(movement)
        if inv["quantity"] <= inv["low_stock_threshold"]:
            self._alerts.append({
                "type": "low_stock",
                "product_id": product_id,
                "current_quantity": inv["quantity"],
                "threshold": inv["low_stock_threshold"],
                "timestamp": datetime.now().isoformat(),
            })
        return {"new_quantity": inv["quantity"], "movement": movement}

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        if product_id not in self._inventory:
            return False
        inv = self._inventory[product_id]
        available = inv["quantity"] - inv["reserved"]
        if available < quantity:
            return False
        inv["reserved"] += quantity
        self._movements.append({
            "product_id": product_id,
            "movement_type": InventoryMovement.RESERVATION.value,
            "quantity_change": -quantity,
            "timestamp": datetime.now().isoformat(),
        })
        return True

    def release_reservation(self, product_id: str, quantity: int) -> bool:
        if product_id not in self._inventory:
            return False
        inv = self._inventory[product_id]
        inv["reserved"] = max(0, inv["reserved"] - quantity)
        return True

    def get_stock_status(self, product_id: str) -> Dict[str, Any]:
        if product_id not in self._inventory:
            return {"error": "Product not in inventory"}
        inv = self._inventory[product_id]
        available = inv["quantity"] - inv["reserved"]
        return {
            "product_id": product_id,
            "quantity": inv["quantity"],
            "reserved": inv["reserved"],
            "available": available,
            "low_stock": available <= inv["low_stock_threshold"],
            "out_of_stock": available <= 0,
            "needs_reorder": available <= inv["reorder_point"],
        }

    def get_low_stock_items(self) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for pid, inv in self._inventory.items():
            available = inv["quantity"] - inv["reserved"]
            if available <= inv["low_stock_threshold"]:
                result.append({
                    "product_id": pid,
                    "available": available,
                    "threshold": inv["low_stock_threshold"],
                })
        return result

    def get_movement_history(
        self, product_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        movements = self._movements
        if product_id:
            movements = [m for m in movements if m["product_id"] == product_id]
        return movements[-limit:]

    def generate_report(self) -> Dict[str, Any]:
        products = list(self._inventory.values())
        low_stock = [
            pid for pid, inv in self._inventory.items()
            if (inv["quantity"] - inv["reserved"]) <= inv["low_stock_threshold"]
        ]
        out_of_stock = [
            pid for pid, inv in self._inventory.items()
            if (inv["quantity"] - inv["reserved"]) <= 0
        ]
        return {
            "total_products": len(self._inventory),
            "low_stock_count": len(low_stock),
            "out_of_stock_count": len(out_of_stock),
            "total_quantity": sum(inv["quantity"] for inv in products),
            "total_reserved": sum(inv["reserved"] for inv in products),
            "low_stock_items": low_stock[:20],
            "out_of_stock_items": out_of_stock[:20],
            "total_movements": len(self._movements),
        }


class FraudDetector:
    """Transaction fraud detection and risk assessment."""

    def __init__(self) -> None:
        self._rules: List[Dict[str, Any]] = []
        self._assessments: List[FraudAssessment] = []
        self._high_risk_countries = {"XX", "YY"}
        self._velocity_threshold = 5
        logger.info("FraudDetector initialized")

    def add_rule(
        self, name: str, check_fn: Callable[[Dict[str, Any]], float], weight: float = 1.0
    ) -> None:
        self._rules.append({"name": name, "check_fn": check_fn, "weight": weight})

    def assess_transaction(
        self, transaction: Dict[str, Any], customer: Optional[Customer] = None
    ) -> FraudAssessment:
        risk_score = 0.0
        flags: List[str] = []
        if transaction.get("country") in self._high_risk_countries:
            risk_score += 30
            flags.append("high_risk_country")
        if transaction.get("amount", 0) > 500:
            risk_score += 20
            flags.append("high_value_transaction")
        if transaction.get("velocity", 0) > self._velocity_threshold:
            risk_score += 25
            flags.append("high_velocity")
        if customer and customer.total_orders == 0:
            risk_score += 15
            flags.append("first_time_customer")
        if transaction.get("mismatched_address", False):
            risk_score += 20
            flags.append("address_mismatch")
        for rule in self._rules:
            try:
                rule_score = rule["check_fn"](transaction)
                risk_score += rule_score * rule["weight"]
            except Exception:
                pass
        if risk_score >= 70:
            level = FraudRiskLevel.CRITICAL
            action = "block"
        elif risk_score >= 50:
            level = FraudRiskLevel.HIGH
            action = "manual_review"
        elif risk_score >= 30:
            level = FraudRiskLevel.MEDIUM
            action = "additional_verification"
        else:
            level = FraudRiskLevel.LOW
            action = "approve"
        assessment = FraudAssessment(
            transaction_id=transaction.get("id", ""),
            risk_level=level,
            risk_score=min(risk_score, 100),
            flags=flags,
            recommended_action=action,
        )
        self._assessments.append(assessment)
        return assessment

    def get_assessment_stats(self) -> Dict[str, Any]:
        assessments = self._assessments
        return {
            "total_assessments": len(assessments),
            "approved": len([a for a in assessments if a.recommended_action == "approve"]),
            "blocked": len([a for a in assessments if a.recommended_action == "block"]),
            "manual_review": len([a for a in assessments if a.recommended_action == "manual_review"]),
            "average_risk_score": (
                sum(a.risk_score for a in assessments) / len(assessments)
                if assessments else 0
            ),
        }


class TaxEngine:
    """Tax calculation and management."""

    def __init__(self) -> None:
        self._tax_rates: Dict[str, TaxRate] = {}
        logger.info("TaxEngine initialized")

    def add_tax_rate(self, tax_rate: TaxRate) -> None:
        self._tax_rates[tax_rate.rate_id] = tax_rate

    def calculate_tax(
        self,
        amount: float,
        state: str = "",
        city: str = "",
        country: str = "US",
        product_category: Optional[str] = None,
    ) -> Dict[str, Any]:
        applicable_rates: List[TaxRate] = []
        for tr in self._tax_rates.values():
            if tr.country and tr.country != country:
                continue
            if tr.state and tr.state != state:
                continue
            if tr.city and tr.city != city:
                continue
            if tr.product_category and tr.product_category != product_category:
                continue
            applicable_rates.append(tr)
        total_tax = 0.0
        breakdown: List[Dict[str, Any]] = []
        for tr in applicable_rates:
            tax = tr.calculate_tax(amount)
            total_tax += tax
            breakdown.append({
                "name": tr.name,
                "rate": tr.rate,
                "amount": tax,
            })
        return {
            "subtotal": amount,
            "total_tax": round(total_tax, 2),
            "effective_rate": round(total_tax / amount, 4) if amount else 0,
            "breakdown": breakdown,
        }


# ---------------------------------------------------------------------------
# Main Agent Orchestrator
# ---------------------------------------------------------------------------

class EcommerceAgent:
    """Top-level orchestrator for all e-commerce operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._catalog = ProductCatalog()
        self._cart_manager = ShoppingCartManager(self._catalog)
        self._order_manager = OrderManager()
        self._pricing = PricingEngine()
        self._inventory = InventoryManager()
        self._fraud = FraudDetector()
        self._tax = TaxEngine()
        self._customers: Dict[str, Customer] = {}
        logger.info("EcommerceAgent initialized")

    @property
    def catalog(self) -> ProductCatalog:
        return self._catalog

    @property
    def cart_manager(self) -> ShoppingCartManager:
        return self._cart_manager

    @property
    def order_manager(self) -> OrderManager:
        return self._order_manager

    @property
    def pricing(self) -> PricingEngine:
        return self._pricing

    @property
    def inventory(self) -> InventoryManager:
        return self._inventory

    @property
    def fraud_detector(self) -> FraudDetector:
        return self._fraud

    @property
    def tax_engine(self) -> TaxEngine:
        return self._tax

    def add_customer(self, customer: Customer) -> str:
        self._customers[customer.customer_id] = customer
        return customer.customer_id

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        return self._customers.get(customer_id)

    def checkout(
        self,
        cart_id: str,
        customer_id: str,
        shipping_address: Address,
        payment_method: PaymentMethod,
        shipping_method: ShippingMethod = ShippingMethod.STANDARD,
        coupon_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        cart = self._cart_manager.get_cart(cart_id)
        if not cart or cart.is_empty:
            return {"error": "Cart is empty or not found"}
        customer = self._customers.get(customer_id)
        discount_amount = 0.0
        if coupon_code:
            validation = self._pricing.validate_coupon(coupon_code)
            if validation.get("valid"):
                totals = self._cart_manager.calculate_total(cart_id)
                result = self._pricing.apply_discount(
                    self._find_discount_id(coupon_code), totals["subtotal"]
                )
                discount_amount = result.get("discount_amount", 0)
        tax_result = self._tax.calculate_tax(
            sum(item.line_total for item in cart.items),
            state=shipping_address.state,
            country=shipping_address.country,
        )
        shipping_cost = self._calculate_shipping(shipping_method, cart)
        order = self._order_manager.create_order(
            user_id=customer_id,
            items=cart.items,
            shipping_address=shipping_address,
            payment_method=payment_method,
            shipping_method=shipping_method,
            tax_rate=tax_result["effective_rate"],
            shipping_cost=shipping_cost,
            discount_amount=discount_amount,
        )
        for item in cart.items:
            self._inventory.adjust_stock(
                item.product_id,
                -item.quantity,
                InventoryMovement.SALE,
                reason=f"Order {order.order_id}",
                reference_id=order.order_id,
            )
        fraud_assessment = self._fraud.assess_transaction(
            {"id": order.order_id, "amount": order.total, "country": shipping_address.country},
            customer,
        )
        if fraud_assessment.recommended_action == "block":
            self._order_manager.cancel_order(order.order_id)
            return {
                "error": "Transaction blocked by fraud detection",
                "risk_score": fraud_assessment.risk_score,
                "flags": fraud_assessment.flags,
            }
        if customer:
            customer.add_order(order.total)
        self._cart_manager.clear_cart(cart_id)
        return {
            "order_id": order.order_id,
            "total": order.total,
            "payment_status": order.payment_status.value,
            "fraud_risk": fraud_assessment.risk_level.value,
            "estimated_delivery": self._estimate_delivery(shipping_method),
        }

    def get_store_dashboard(self) -> Dict[str, Any]:
        catalog_stats = self._catalog.get_catalog_stats()
        order_stats = self._order_manager.get_order_stats()
        inventory_report = self._inventory.generate_report()
        fraud_stats = self._fraud.get_assessment_stats()
        return {
            "catalog": catalog_stats,
            "orders": order_stats,
            "inventory": inventory_report,
            "fraud": fraud_stats,
            "customers": {
                "total": len(self._customers),
                "total_revenue": sum(c.total_spent for c in self._customers.values()),
            },
            "generated_at": datetime.now().isoformat(),
        }

    def _find_discount_id(self, code: str) -> Optional[str]:
        for did, d in self._pricing._discounts.items():
            if d.code == code.upper():
                return did
        return None

    def _calculate_shipping(
        self, method: ShippingMethod, cart: ShoppingCart
    ) -> float:
        shipping_rates = {
            ShippingMethod.STANDARD: 5.99,
            ShippingMethod.EXPEDITED: 12.99,
            ShippingMethod.OVERNIGHT: 24.99,
            ShippingMethod.SAME_DAY: 34.99,
            ShippingMethod.FREE_SHIPPING: 0.0,
            ShippingMethod.PICKUP: 0.0,
        }
        base = shipping_rates.get(method, 5.99)
        return base if cart.item_count > 0 else 0.0

    def _estimate_delivery(self, method: ShippingMethod) -> str:
        estimates = {
            ShippingMethod.STANDARD: "5-7 business days",
            ShippingMethod.EXPEDITED: "2-3 business days",
            ShippingMethod.OVERNIGHT: "Next business day",
            ShippingMethod.SAME_DAY: "Same day",
            ShippingMethod.PICKUP: "Ready for pickup",
            ShippingMethod.FREE_SHIPPING: "5-7 business days",
        }
        return estimates.get(method, "5-7 business days")

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "EcommerceAgent",
            "products": len(self._catalog._products),
            "orders": len(self._order_manager._orders),
            "customers": len(self._customers),
            "active_discounts": len([
                d for d in self._pricing._discounts.values() if d.is_valid
            ]),
        }


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    print("=== E-Commerce Agent Demo ===")
    agent = EcommerceAgent()

    product = Product(
        name="Wireless Headphones",
        description="Premium noise-cancelling wireless headphones",
        category="Electronics",
        price=299.99,
        cost=120.00,
        tags=["audio", "wireless", "premium"],
    )
    pid = agent.catalog.add_product(product)
    print(f"Product added: {pid}")

    agent.inventory.adjust_stock(pid, 100, InventoryMovement.PURCHASE, "Initial stock")

    cart = agent.cart_manager.create_cart(user_id="user_001")
    agent.cart_manager.add_item(cart.cart_id, pid, quantity=2)

    totals = agent.cart_manager.calculate_total(cart.cart_id, tax_rate=0.08)
    print(f"Cart total: ${totals['total']:.2f}")

    discount = agent.pricing.create_discount(
        code="SAVE20", name="20% Off", discount_type=DiscountType.PERCENTAGE,
        value=20, min_order_amount=100,
    )
    discount_result = agent.pricing.apply_discount(discount.discount_id, totals["subtotal"])
    print(f"Discount: ${discount_result['discount_amount']:.2f}")

    customer = Customer(email="test@example.com", first_name="John", last_name="Doe")
    agent.add_customer(customer)

    addr = Address(line1="123 Main St", city="Springfield", state="IL", postal_code="62701", country="US")
    order_result = agent.checkout(
        cart_id=cart.cart_id,
        customer_id=customer.customer_id,
        shipping_address=addr,
        payment_method=PaymentMethod.CREDIT_CARD,
        coupon_code="SAVE20",
    )
    print(f"Order: {order_result.get('order_id', 'N/A')}")

    dashboard = agent.get_store_dashboard()
    print(f"Dashboard — Products: {dashboard['catalog']['total_products']}, "
          f"Orders: {dashboard['orders']['total_orders']}")

    stock = agent.inventory.get_stock_status(pid)
    print(f"Stock remaining: {stock.get('available', 0)}")

    status = agent.get_status()
    print(f"Agent status: {status}")


if __name__ == "__main__":
    main()
