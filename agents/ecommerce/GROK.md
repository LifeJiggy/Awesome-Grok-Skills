---
name: "E-Commerce Agent"
version: "2.0.0"
description: "Full-stack e-commerce platform management covering product catalogs, shopping carts, order processing, payment handling, inventory, dynamic pricing, fraud detection, tax calculation, and customer management"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["e-commerce", "shopping-cart", "orders", "inventory", "pricing", "payments", "fraud-detection", "tax", "retail", "product-catalog"]
category: "business"
personality: "efficiency-expert"
use_cases:
  - "product catalog management"
  - "shopping cart operations"
  - "order lifecycle management"
  - "dynamic pricing and discounts"
  - "inventory tracking and alerts"
  - "fraud risk assessment"
  - "multi-jurisdiction tax calculation"
  - "customer relationship management"
  - "store performance dashboards"
---

# E-Commerce Agent

> End-to-end e-commerce platform management — from product listing to delivery.

## Table of Contents

- [Agent Identity](#agent-identity)
- [Core Principles](#core-principles)
- [System Architecture](#system-architecture)
- [Capabilities](#capabilities)
- [Data Models](#data-models)
- [Method Signatures](#method-signatures)
- [Operational Guidelines](#operational-guidelines)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Scalability](#scalability)
- [Design Patterns](#design-patterns)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [Integration Points](#integration-points)
- [Examples](#examples)
- [Best Practices](#best-practices)

---

## Agent Identity

The E-Commerce Agent is an efficiency expert that manages the complete retail
lifecycle. It optimizes conversions, reduces operational overhead, prevents fraud,
and ensures accurate financial operations across the entire commerce stack.

**Core Personality**: Precision-focused, customer-centric, data-driven.
Every recommendation optimizes for conversion, margin, and customer satisfaction.

### Agent Capabilities Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                    ECOMMERCE AGENT CAPABILITIES                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Product     │  │  Shopping   │  │  Order      │             │
│  │  Catalog     │  │  Cart       │  │  Manager    │             │
│  │  ────────    │  │  ────────   │  │  ────────   │             │
│  │  • CRUD      │  │  • Add/Rem  │  │  • Create   │             │
│  │  • Search    │  │  • Calculate│  │  • Track    │             │
│  │  • Variants  │  │  • Coupons  │  │  • Fulfill  │             │
│  │  • Bulk ops  │  │  • Expiry   │  │  • Refund   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Pricing    │  │  Inventory  │  │  Fraud      │             │
│  │  Engine     │  │  Manager    │  │  Detector   │             │
│  │  ────────   │  │  ────────   │  │  ────────   │             │
│  │  • Discounts│  │  • Track    │  │  • Score    │             │
│  │  • Bundles  │  │  • Reserve  │  │  • Rules    │             │
│  │  • Tiers    │  │  • Alerts   │  │  • Block    │             │
│  │  • BOGO     │  │  • Reorder  │  │  • Review   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐                               │
│  │  Tax Engine │  │  Customer   │                               │
│  │  ────────   │  │  Store      │                               │
│  │  • Rates    │  │  ────────   │                               │
│  │  • Calculate│  │  • Profiles │                               │
│  │  • Multi-jur│  │  • Segments │                               │
│  │  • Reports  │  │  • Loyalty  │                               │
│  └─────────────┘  └─────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Principles

1. **Conversion Optimization**: Every friction point is an opportunity.
2. **Inventory Accuracy**: Stock numbers must be exact, always.
3. **Financial Integrity**: Payments, taxes, and discounts must be precise.
4. **Fraud Prevention**: Catch fraud before it costs money.
5. **Customer Trust**: Fast checkout, accurate orders, easy returns.

---

## System Architecture

### High-Level Component Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ECOMMERCE AGENT                                   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      UNIFIED CHECKOUT FLOW                        │   │
│  │  Cart → Validate → Tax → Fraud Check → Payment → Order → Ship   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Product   │ │  Shopping  │ │  Order     │ │  Pricing   │           │
│  │  Catalog   │ │  Cart Mgr  │ │  Manager   │ │  Engine    │           │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘           │
│        │              │              │              │                    │
│  ┌─────┴──────┐ ┌─────┴──────┐ ┌─────┴──────┐ ┌─────┴──────┐           │
│  │  Inventory │ │  Fraud     │ │  Tax       │ │  Customer  │           │
│  │  Manager   │ │  Detector  │ │  Engine    │ │  Store     │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    DATA LAYER (In-Memory + Optional DB)           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
  Customer Journey:
  ════════════════

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Browse   │ ─► │ Add to   │ ─► │ Checkout │ ─► │ Payment  │
  │ Products │    │ Cart     │    │          │    │          │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
       ▼               ▼               ▼               ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Search   │    │ Calculate│    │ Fraud    │    │ Process  │
  │ Filter   │    │ Totals   │    │ Check    │    │ Payment  │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                              │
                                              ▼
                                       ┌──────────┐    ┌──────────┐
                                       │ Create   │ ─► │ Ship     │
                                       │ Order    │    │ Track    │
                                       └──────────┘    └──────────┘
```

### Order Lifecycle State Machine

```
                    ┌─────────┐
                    │ PENDING │
                    └────┬────┘
                         │
              ┌──────────┴──────────┐
              │  Fraud Check Pass?  │
              └──────────┬──────────┘
                    Yes  │  No
              ┌──────────┴──────────┐
              ▼                     ▼
        ┌──────────┐          ┌──────────┐
        │CONFIRMED │          │ REVIEW   │
        └────┬─────┘          └────┬─────┘
             │                     │
             ▼                     │
        ┌──────────┐               │
        │PROCESSING│◄──────────────┘
        └────┬─────┘  (approved)
             │
             ▼
        ┌──────────┐
        │ SHIPPED  │
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │DELIVERED │
        └──────────┘

  Cancelation: PENDING/CONFIRMED → CANCELLED
  Refund: SHIPPED/DELIVERED → REFUNDED
```

---

## Capabilities

### 1. Product Catalog Management

```python
from agents.ecommerce.agent import (
    EcommerceAgent, Product, ProductVariant, ProductStatus,
)

agent = EcommerceAgent()

product = Product(
    name="Wireless Headphones",
    description="Premium noise-cancelling headphones with 30hr battery",
    category="Electronics",
    subcategory="Audio",
    price=299.99,
    cost=120.00,
    tags=["wireless", "noise-cancelling", "premium"],
    variants=[
        ProductVariant(sku="WH-BLK-M", name="Black", attributes={"color": "Black"}, price=299.99, stock_quantity=50),
        ProductVariant(sku="WH-WHT-M", name="White", attributes={"color": "White"}, price=299.99, stock_quantity=30),
    ],
)
pid = agent.catalog.add_product(product)

# Search products
results = agent.catalog.search_products(
    query="headphones",
    category="Electronics",
    min_price=100,
    max_price=500,
    in_stock_only=True,
)

# Get catalog stats
stats = agent.catalog.get_catalog_stats()
# {"total_products": 1247, "active_products": 1100, "out_of_stock": 23, ...}
```

### 2. Shopping Cart Operations

```python
cart = agent.cart_manager.create_cart(user_id="user_123")

agent.cart_manager.add_item(cart.cart_id, pid, quantity=1)
agent.cart_manager.add_item(cart.cart_id, pid2, quantity=2)

# Calculate totals
totals = agent.cart_manager.calculate_total(
    cart.cart_id,
    tax_rate=0.08,
    shipping_cost=5.99,
)
# {"subtotal": 899.97, "tax": 72.00, "shipping": 5.99, "total": 977.96}

# Update quantity
agent.cart_manager.update_quantity(cart.cart_id, pid, quantity=3)

# Remove item
agent.cart_manager.remove_item(cart.cart_id, pid2)
```

### 3. Order Management

```python
from agents.ecommerce.agent import Address, PaymentMethod, ShippingMethod

order = agent.order_manager.create_order(
    user_id="user_123",
    items=cart.items,
    shipping_address=Address(
        line1="123 Main St",
        city="Springfield",
        state="IL",
        postal_code="62701",
        country="US",
    ),
    payment_method=PaymentMethod.CREDIT_CARD,
    shipping_method=ShippingMethod.EXPEDITED,
    tax_rate=0.08,
    shipping_cost=12.99,
)

# Update status
agent.order_manager.update_order_status(order.order_id, OrderStatus.PROCESSING)
agent.order_manager.add_tracking_number(order.order_id, "1Z999AA10123456784")

# Get user orders
orders = agent.order_manager.get_user_orders("user_123")

# Order stats
stats = agent.order_manager.get_order_stats()
# {"total_orders": 1547, "total_revenue": 234567.89, "average_order_value": 151.63}
```

### 4. Dynamic Pricing and Discounts

```python
from agents.ecommerce.agent import DiscountType

# Create discount
discount = agent.pricing.create_discount(
    code="SUMMER20",
    name="Summer Sale 20%",
    discount_type=DiscountType.PERCENTAGE,
    value=20,
    min_order_amount=50,
    usage_limit=1000,
    start_date=datetime(2025, 6, 1),
    end_date=datetime(2025, 8, 31),
)

# Apply discount
result = agent.pricing.apply_discount(discount.discount_id, subtotal=200)
# {"discount_amount": 40.0, "code": "SUMMER20"}

# Bundle pricing
bundle = agent.pricing.calculate_bundle_price(
    items=[{"price": 299.99, "quantity": 1}, {"price": 49.99, "quantity": 2}],
    bundle_discount_percent=15,
)
# {"original_total": 399.97, "bundle_discount": 60.00, "bundle_price": 339.97}

# Tiered discount
tiered = agent.pricing.calculate_tiered_discount(
    amount=150,
    tiers=[(50, 5), (100, 10), (200, 20)],
)
# 15.0 (10% tier)
```

### 5. Inventory Management

```python
from agents.ecommerce.agent import InventoryMovement

# Adjust stock
agent.inventory.adjust_stock(
    pid, 100, InventoryMovement.PURCHASE, "Initial stock from supplier"
)

# Reserve for order
agent.inventory.reserve_stock(pid, 5)

# Get status
status = agent.inventory.get_stock_status(pid)
# {"quantity": 100, "reserved": 5, "available": 95, "low_stock": False}

# Low stock alert
low_items = agent.inventory.get_low_stock_items()

# Full report
report = agent.inventory.generate_report()
# {"total_products": 500, "low_stock_count": 23, "out_of_stock_count": 5}
```

### 6. Fraud Detection

```python
assessment = agent.fraud_detector.assess_transaction(
    {
        "id": "txn_001",
        "amount": 750.00,
        "country": "US",
        "velocity": 2,
    },
    customer=customer,
)
# FraudAssessment(risk_level=LOW, risk_score=20, recommended_action="approve")

# Add custom rule
agent.fraud_detector.add_rule(
    name="high_amount_check",
    check_fn=lambda t: 30 if t.get("amount", 0) > 1000 else 0,
    weight=1.5,
)

# Stats
stats = agent.fraud_detector.get_assessment_stats()
```

### 7. Tax Calculation

```python
from agents.ecommerce.agent import TaxRate, TaxType

agent.tax_engine.add_tax_rate(TaxRate(
    name="IL Sales Tax",
    rate_type=TaxType.SALES_TAX,
    rate=0.0625,
    country="US",
    state="IL",
))

tax = agent.tax_engine.calculate_tax(amount=100, state="IL", country="US")
# {"subtotal": 100, "total_tax": 6.25, "effective_rate": 0.0625}
```

### 8. Full Checkout Flow

```python
result = agent.checkout(
    cart_id=cart.cart_id,
    customer_id=customer.customer_id,
    shipping_address=Address(line1="123 Main St", city="Springfield", state="IL", postal_code="62701", country="US"),
    payment_method=PaymentMethod.CREDIT_CARD,
    shipping_method=ShippingMethod.STANDARD,
    coupon_code="SUMMER20",
)
# {"order_id": "order_xxx", "total": 247.99, "fraud_risk": "low", "estimated_delivery": "5-7 business days"}
```

---

## Data Models

### Product Model

```python
@dataclass
class Product:
    product_id: str              # Unique identifier
    name: str                    # Product name
    slug: str                    # URL-friendly name
    description: str             # Product description
    category: str                # Primary category
    subcategory: str             # Subcategory
    price: float                 # Selling price
    cost: float                  # Cost price (for margin)
    status: ProductStatus        # DRAFT, ACTIVE, ARCHIVED
    tags: List[str]              # Searchable tags
    images: List[str]            # Image URLs
    variants: List[ProductVariant]  # SKU variants
    created_at: datetime         # Creation timestamp
    updated_at: datetime         # Last update timestamp
```

### ProductVariant Model

```python
@dataclass
class ProductVariant:
    variant_id: str              # Unique identifier
    sku: str                     # Stock Keeping Unit
    name: str                    # Variant name
    attributes: Dict[str, str]   # {color: "Red", size: "XL"}
    price: float                 # Variant price
    cost: float                  # Variant cost
    stock_quantity: int           # Current stock
    barcode: str                 # UPC/EAN barcode
```

### ShoppingCart Model

```python
@dataclass
class ShoppingCart:
    cart_id: str                 # Unique identifier
    user_id: Optional[str]       # Associated user
    session_id: Optional[str]    # Guest session
    items: List[CartItem]        # Cart contents
    coupons: List[str]           # Applied coupon codes
    shipping_address: Optional[Address]
    created_at: datetime
    updated_at: datetime
    expires_at: datetime         # Cart expiry
```

### Order Model

```python
@dataclass
class Order:
    order_id: str                # Unique identifier
    user_id: str                 # Customer ID
    items: List[OrderItem]       # Ordered items
    status: OrderStatus          # PENDING → DELIVERED
    payment_status: PaymentStatus
    payment_method: PaymentMethod
    shipping_method: ShippingMethod
    shipping_address: Address
    billing_address: Optional[Address]
    subtotal: float
    tax: float
    shipping_cost: float
    discount_amount: float
    total: float
    tracking_number: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### Customer Model

```python
@dataclass
class Customer:
    customer_id: str             # Unique identifier
    email: str                   # Email address
    name: str                    # Full name
    phone: Optional[str]         # Phone number
    segment: CustomerSegment     # VIP, REGULAR, NEW
    loyalty_points: int          # Loyalty program points
    total_orders: int            # Lifetime order count
    total_spent: float           # Lifetime spend
    created_at: datetime
```

### FraudAssessment Model

```python
@dataclass
class FraudAssessment:
    assessment_id: str           # Unique identifier
    transaction_id: str          # Transaction reference
    risk_level: RiskLevel        # LOW, MEDIUM, HIGH, CRITICAL
    risk_score: float            # 0-100
    flags: List[str]             # Triggered fraud flags
    recommended_action: str      # approve, review, block
    created_at: datetime
```

### Data Model Relationships

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Product    │ 1───∞ │   Variant    │       │   Category   │
│              │       │              │       │              │
│ product_id   │       │ variant_id   │       │ category_id  │
│ name         │       │ sku          │       │ name         │
│ category_id ─┼──────►│ price        │       │ parent_id    │
│ price        │       │ stock_qty    │       └──────────────┘
└──────┬───────┘       └──────────────┘
       │
       │ 1───∞
       ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  CartItem    │ ∞───1 │  ShoppingCart│ 1───∞ │    Order     │
│              │       │              │       │              │
│ cart_id     ─┼──────►│ cart_id      │       │ order_id     │
│ product_id   │       │ user_id      │       │ user_id      │
│ quantity     │       │ items        │       │ status       │
│ price        │       │ total        │       │ total        │
└──────────────┘       └──────────────┘       └──────┬───────┘
                                                      │
                                                      │ 1───∞
                                                      ▼
                                               ┌──────────────┐
                                               │  OrderItem   │
                                               │              │
                                               │ order_id     │
                                               │ product_id   │
                                               │ quantity     │
                                               │ price        │
                                               └──────────────┘
```

---

## Method Signatures

### EcommerceAgent (Top-Level)

```python
def checkout(
    self,
    cart_id: str,
    customer_id: str,
    shipping_address: Address,
    payment_method: PaymentMethod,
    shipping_method: ShippingMethod = ShippingMethod.STANDARD,
    coupon_code: Optional[str] = None,
) -> Dict[str, Any]

def get_store_dashboard(self) -> Dict[str, Any]

def add_customer(self, customer: Customer) -> str

def get_customer(self, customer_id: str) -> Optional[Customer]

def get_status(self) -> Dict[str, Any]
```

### ProductCatalog

```python
def add_product(self, product: Product) -> str

def update_product(
    self,
    product_id: str,
    updates: Dict[str, Any]
) -> Optional[Product]

def get_product(self, product_id: str) -> Optional[Product]

def delete_product(self, product_id: str) -> bool

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
) -> List[Product]

def get_categories(self) -> Dict[str, int]

def bulk_update_status(
    self,
    product_ids: List[str],
    new_status: ProductStatus
) -> int

def get_catalog_stats(self) -> Dict[str, Any]
```

### ShoppingCartManager

```python
def create_cart(
    self,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
) -> ShoppingCart

def get_cart(self, cart_id: str) -> Optional[ShoppingCart]

def add_item(
    self,
    cart_id: str,
    product_id: str,
    quantity: int = 1,
    variant_id: Optional[str] = None,
) -> Dict[str, Any]

def remove_item(
    self,
    cart_id: str,
    product_id: str,
    variant_id: Optional[str] = None,
) -> Dict[str, Any]

def update_quantity(
    self,
    cart_id: str,
    product_id: str,
    quantity: int,
    variant_id: Optional[str] = None,
) -> Dict[str, Any]

def calculate_total(
    self,
    cart_id: str,
    tax_rate: float = 0.0,
    shipping_cost: float = 0.0,
    discount_amount: float = 0.0,
) -> Dict[str, float]

def clear_cart(self, cart_id: str) -> bool
```

### OrderManager

```python
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
) -> Order

def update_order_status(self, order_id: str, status: OrderStatus) -> bool

def update_payment_status(self, order_id: str, payment_status: PaymentStatus) -> bool

def add_tracking_number(self, order_id: str, tracking_number: str) -> bool

def cancel_order(self, order_id: str) -> Dict[str, Any]

def refund_order(self, order_id: str, amount: Optional[float] = None) -> Dict[str, Any]

def get_order(self, order_id: str) -> Optional[Order]

def get_user_orders(self, user_id: str) -> List[Order]

def get_orders_by_status(self, status: OrderStatus) -> List[Order]

def get_fulfillment_queue(self) -> List[Dict[str, Any]]

def get_order_stats(self) -> Dict[str, Any]
```

### PricingEngine

```python
def create_discount(
    self,
    code: str,
    name: str,
    discount_type: DiscountType,
    value: float,
    min_order_amount: float = 0,
    usage_limit: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Discount

def apply_discount(self, discount_id: str, subtotal: float) -> Dict[str, float]

def validate_coupon(self, code: str) -> Dict[str, Any]

def calculate_bundle_price(
    self,
    items: List[Dict[str, Any]],
    bundle_discount_percent: float = 10.0,
) -> Dict[str, float]

def calculate_tiered_discount(
    self,
    amount: float,
    tiers: List[Tuple[float, float]],
) -> float

def get_discount_stats(self) -> Dict[str, Any]
```

### InventoryManager

```python
def adjust_stock(
    self,
    product_id: str,
    quantity_change: int,
    movement_type: InventoryMovement = InventoryMovement.ADJUSTMENT,
    reason: str = "",
    reference_id: Optional[str] = None,
) -> Dict[str, Any]

def reserve_stock(self, product_id: str, quantity: int) -> bool

def release_reservation(self, product_id: str, quantity: int) -> bool

def get_stock_status(self, product_id: str) -> Dict[str, Any]

def get_low_stock_items(self) -> List[Dict[str, Any]]

def get_movement_history(
    self,
    product_id: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]

def generate_report(self) -> Dict[str, Any]
```

### FraudDetector

```python
def add_rule(
    self,
    name: str,
    check_fn: Callable[[Dict], float],
    weight: float = 1.0,
) -> None

def assess_transaction(
    self,
    transaction: Dict[str, Any],
    customer: Optional[Customer] = None,
) -> FraudAssessment

def get_assessment_stats(self) -> Dict[str, Any]
```

### TaxEngine

```python
def add_tax_rate(self, tax_rate: TaxRate) -> None

def calculate_tax(
    self,
    amount: float,
    state: Optional[str] = None,
    city: Optional[str] = None,
    country: str = "US",
) -> Dict[str, float]
```

---

## Operational Guidelines

### Product Listing Checklist

1. Complete product name and description
2. Set accurate pricing (including cost for margin tracking)
3. Add high-quality images
4. Create all variants with SKUs
5. Set SEO metadata (title, description)
6. Configure stock quantities
7. Assign categories and tags
8. Validate with `product.validate()`

### Order Processing Rules

- Auto-confirm orders only if fraud risk is LOW
- Hold orders with MEDIUM+ fraud risk for review
- Send tracking number within 24h of shipping
- Allow cancellation only for PENDING/CONFIRMED orders
- Process refunds within 5-7 business days

### Inventory Best Practices

- Set low_stock_threshold per product based on sales velocity
- Use reorder_point to trigger automatic reorder alerts
- Reserve stock during checkout to prevent overselling
- Release reservations after 30 minutes of cart inactivity
- Audit inventory monthly with physical counts

### Fraud Prevention Rules

- Block transactions with risk_score >= 70
- Hold for manual review at risk_score 50-69
- Require additional verification at risk_score 30-49
- Monitor velocity: flag > 5 orders/hour per customer
- Cross-reference billing/shipping address mismatch

---

## Configuration

### Agent Configuration

```yaml
ecommerce_agent:
  catalog:
    max_products: 1000000
    default_currency: USD
    search_index: elasticsearch
    image_upload_max_mb: 10

  cart:
    cart_expiry_hours: 24
    max_items_per_cart: 100
    allow_guest_checkout: true
    reservation_timeout_minutes: 30

  orders:
    cancellation_window_hours: 24
    return_window_days: 30
    auto_confirm_threshold: "low"
    tracking_update_hours: 24

  inventory:
    low_stock_threshold: 10
    reorder_point: 20
    reservation_timeout_minutes: 30
    enable_negative_stock: false

  fraud:
    high_risk_countries: ["XX", "YY"]
    velocity_threshold: 5
    block_threshold: 70
    review_threshold: 50
    enable_device_fingerprinting: true

  tax:
    auto_calculate: true
    fallback_rate: 0.0
    tax_inclusive_pricing: false

  shipping:
    free_shipping_threshold: 50
    rates:
      standard: 5.99
      expedited: 12.99
      overnight: 24.99
```

### Environment Variables

```bash
# Payment Processing
STRIPE_API_KEY=sk_test_...
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...

# Shipping
SHIPSTATION_API_KEY=...
SHIPSTATION_API_SECRET=...

# Tax
AVALARA_API_KEY=...
AVALARA_COMPANY_CODE=...

# Analytics
SEGMENT_WRITE_KEY=...
GOOGLE_ANALYTICS_ID=...

# Email
SENDGRID_API_KEY=...
FROM_EMAIL=noreply@yourstore.com
```

---

## Security Considerations

### Payment Security

- Never store raw credit card numbers
- Use tokenization via payment processor (Stripe, PayPal)
- Implement PCI DSS compliance for card handling
- Validate all payment amounts server-side
- Use HTTPS for all payment endpoints

### Data Protection

- Encrypt sensitive customer data at rest
- Implement proper authentication for admin endpoints
- Use rate limiting on checkout endpoints
- Validate all input to prevent injection attacks
- Log all financial transactions for audit

### Fraud Prevention

- Implement velocity checks (orders per hour/IP)
- Use device fingerprinting for risk assessment
- Cross-reference with known fraud databases
- Implement address verification (AVS)
- Use CVV verification for card transactions

### API Security

- Use API keys for external integrations
- Implement request signing for webhooks
- Validate webhook signatures before processing
- Use IP whitelisting for admin APIs
- Implement proper CORS policies

---

## Scalability

### Current Design Limits

| Component | Limit | Notes |
|-----------|-------|-------|
| Products | ~100,000 | In-memory storage |
| Orders | ~50,000 | Per session |
| Cart items | 100 | Per cart |
| Concurrent users | ~100 | Single process |

### Scaling Strategies

```
┌─────────────────────────────────────────────────────────────┐
│                    SCALING PATHWAY                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Phase 1: In-Memory (Current)                                │
│  ├── Single process, stdlib only                             │
│  └── Suitable for < 1000 products                            │
│                                                               │
│  Phase 2: Database Backend                                   │
│  ├── PostgreSQL/MySQL for persistence                        │
│  ├── Redis for cart sessions                                 │
│  └── Suitable for < 100K products                            │
│                                                               │
│  Phase 3: Distributed                                        │
│  ├── Microservices per component                             │
│  ├── Message queues (RabbitMQ/Kafka)                         │
│  ├── CDN for product images                                  │
│  └── Suitable for 100K+ products                             │
│                                                               │
│  Phase 4: Global Scale                                       │
│  ├── Multi-region deployment                                 │
│  ├── Edge caching                                            │
│  ├── Database sharding                                       │
│  └── Suitable for 1M+ products                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Performance Benchmarks

| Operation | Current | With DB | With Cache |
|-----------|---------|---------|------------|
| Product search (1K products) | ~5ms | ~20ms | ~2ms |
| Cart calculation | ~1ms | ~5ms | ~1ms |
| Order creation | ~2ms | ~15ms | ~10ms |
| Fraud assessment | ~3ms | ~10ms | ~5ms |
| Tax calculation | ~1ms | ~5ms | ~1ms |

---

## Design Patterns

### Strategy Pattern

Different pricing strategies, fraud rules, and tax calculations are interchangeable:

```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, cart: ShoppingCart) -> float:
        pass

class PercentageDiscount(PricingStrategy):
    def calculate(self, cart: ShoppingCart) -> float:
        return cart.subtotal * self.percent

class FixedDiscount(PricingStrategy):
    def calculate(self, cart: ShoppingCart) -> float:
        return min(self.amount, cart.subtotal)
```

### State Pattern

Order status transitions follow a state machine:

```python
class OrderState(ABC):
    @abstractmethod
    def next(self, order: Order) -> 'OrderState':
        pass

class PendingState(OrderState):
    def next(self, order: Order) -> OrderState:
        if order.fraud_risk == "low":
            return ConfirmedState()
        return ReviewState()
```

### Observer Pattern

Inventory changes trigger notifications:

```python
class InventoryObserver(ABC):
    @abstractmethod
    def on_stock_changed(self, product_id: str, new_quantity: int):
        pass

class LowStockAlert(InventoryObserver):
    def on_stock_changed(self, product_id: str, new_quantity: int):
        if new_quantity < self.threshold:
            self.send_alert(product_id, new_quantity)
```

### Factory Pattern

Order creation with different configurations:

```python
class OrderFactory:
    @staticmethod
    def create_standard_order(cart, address) -> Order:
        return Order(items=cart.items, shipping=ShippingMethod.STANDARD, ...)

    @staticmethod
    def create_express_order(cart, address) -> Order:
        return Order(items=cart.items, shipping=ShippingMethod.EXPEDITED, ...)
```

---

## Checklists

### Pre-Launch Checklist

- [ ] All products validated and active
- [ ] Tax rates configured for all jurisdictions
- [ ] Shipping rates defined per method
- [ ] Payment processing tested end-to-end
- [ ] Fraud rules tested with sample transactions
- [ ] Discount codes tested with edge cases
- [ ] Order confirmation emails configured
- [ ] Return/refund policy documented
- [ ] Dashboard monitoring enabled
- [ ] Load testing completed

### Product Listing Checklist

- [ ] Product name is clear and descriptive
- [ ] Description includes key features and benefits
- [ ] Price is accurate (including cost for margin)
- [ ] All variants have unique SKUs
- [ ] Images are high-quality and properly sized
- [ ] Categories and tags are assigned
- [ ] SEO metadata is set
- [ ] Stock quantities are accurate

### Order Processing Checklist

- [ ] Fraud check completed
- [ ] Payment authorized
- [ ] Inventory reserved
- [ ] Tax calculated correctly
- [ ] Shipping cost applied
- [ ] Discount applied (if applicable)
- [ ] Confirmation email sent
- [ ] Order status updated

---

## Troubleshooting

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Product not in search results | Status is DRAFT | Set status to ACTIVE |
| Cart total is 0 | Empty cart | Add items before calculating |
| Order won't cancel | Already SHIPPED | Only PENDING/CONFIRMED can cancel |
| Discount not applying | Below minimum order | Check min_order_amount |
| Stock shows negative | Overselling | Implement stock reservation |
| Fraud score too high | Multiple flags | Review individual flag weights |
| Tax calculation returns 0 | No matching tax rates | Add tax rates for jurisdiction |
| Payment fails | Invalid card | Validate card details |
| Shipping cost wrong | Missing address | Ensure shipping address is complete |
| Refund not processing | Already refunded | Check refund status |

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed error info
result = agent.checkout(...)
if "error" in result:
    print(f"Error: {result['error']}")
    print(f"Details: {result.get('details', {})}")
```

---

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| Stripe | REST API | Payment processing |
| PayPal | REST API | Payment processing |
| ShipStation | REST API | Fulfillment & tracking |
| Avalara | REST API | Automated tax calculation |
| Elasticsearch | REST API | Product search at scale |
| SendGrid | REST API | Order confirmation emails |
| Segment | REST API | Customer analytics |
| Google Analytics | GA4 | E-commerce tracking |
| CloudFlare | CDN | Image delivery |
| Redis | Protocol | Session/cart caching |

---

## Examples

### Example 1: Complete E-Commerce Flow

```python
from agents.ecommerce.agent import *

# Initialize agent
agent = EcommerceAgent()

# 1. Create products
product = Product(
    name="Wireless Mouse",
    category="Electronics",
    price=49.99,
    cost=20.00,
)
pid = agent.catalog.add_product(product)

# 2. Add inventory
agent.inventory.adjust_stock(pid, 100, InventoryMovement.PURCHASE)

# 3. Customer creates cart
cart = agent.cart_manager.create_cart(user_id="user_001")
agent.cart_manager.add_item(cart.cart_id, pid, quantity=2)

# 4. Apply discount
agent.pricing.create_discount(
    code="SAVE10",
    name="10% Off",
    discount_type=DiscountType.PERCENTAGE,
    value=10,
)

# 5. Checkout
result = agent.checkout(
    cart_id=cart.cart_id,
    customer_id="user_001",
    shipping_address=Address(line1="123 Main St", city="Portland", state="OR", postal_code="97201", country="US"),
    payment_method=PaymentMethod.CREDIT_CARD,
    coupon_code="SAVE10",
)

print(f"Order: {result['order_id']}, Total: ${result['total']:.2f}")
```

### Example 2: Inventory Monitoring

```python
# Check inventory health
report = agent.inventory.generate_report()

if report["out_of_stock_count"] > 0:
    print(f"WARNING: {report['out_of_stock_count']} products out of stock!")

for item in agent.inventory.get_low_stock_items():
    print(f"Low stock: {item['product_id']} ({item['available']} remaining)")

# Auto-reorder logic
for item in report["low_stock_items"]:
    if item["available"] <= item["reorder_point"]:
        trigger_reorder(item["product_id"], item["reorder_quantity"])
```

### Example 3: Fraud Analysis

```python
# Analyze suspicious transaction
assessment = agent.fraud_detector.assess_transaction(
    {
        "id": "txn_suspicious",
        "amount": 2500.00,
        "country": "NG",
        "velocity": 8,
        "ip_country": "US",
    }
)

if assessment.risk_level in ("HIGH", "CRITICAL"):
    print(f"BLOCKED: Risk score {assessment.risk_score}")
    print(f"Flags: {assessment.flags}")
    # Hold for manual review
    hold_for_review(assessment)
```

---

## Best Practices

1. **Always validate products** before publishing to catch missing SKUs or negative prices.
2. **Reserve stock during checkout** to prevent overselling on high-demand items.
3. **Set fraud thresholds** appropriately for your industry — too strict loses sales, too loose invites fraud.
4. **Configure tax rates** for every jurisdiction you ship to before going live.
5. **Monitor low-stock alerts** daily to maintain healthy inventory levels.
6. **Use bundle pricing** for complementary products to increase AOV.
7. **Log all inventory movements** for audit trail and discrepancy investigation.
8. **Test checkout flow** end-to-end before every major sale event.
9. **Implement idempotency keys** for payment processing to prevent double charges.
10. **Use webhooks** for real-time order status updates from shipping providers.

---

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[README.md](./README.md) for quick start and API reference.