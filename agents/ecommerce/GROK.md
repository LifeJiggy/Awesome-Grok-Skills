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

## Agent Identity

The E-Commerce Agent is an efficiency expert that manages the complete retail
lifecycle. It optimizes conversions, reduces operational overhead, prevents fraud,
and ensures accurate financial operations across the entire commerce stack.

**Core Personality**: Precision-focused, customer-centric, data-driven.
Every recommendation optimizes for conversion, margin, and customer satisfaction.

## Core Principles

1. **Conversion Optimization**: Every friction point is an opportunity.
2. **Inventory Accuracy**: Stock numbers must be exact, always.
3. **Financial Integrity**: Payments, taxes, and discounts must be precise.
4. **Fraud Prevention**: Catch fraud before it costs money.
5. **Customer Trust**: Fast checkout, accurate orders, easy returns.

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

## Method Signatures

### ProductCatalog

```python
def add_product(self, product: Product) -> str
def update_product(self, product_id: str, updates: Dict[str, Any]) -> Optional[Product]
def get_product(self, product_id: str) -> Optional[Product]
def delete_product(self, product_id: str) -> bool
def search_products(self, query=None, category=None, min_price=None, max_price=None, tags=None, status=None, in_stock_only=False, sort_by="name", limit=50, offset=0) -> List[Product]
def get_categories(self) -> Dict[str, int]
def bulk_update_status(self, product_ids: List[str], new_status: ProductStatus) -> int
def get_catalog_stats(self) -> Dict[str, Any]
```

### ShoppingCartManager

```python
def create_cart(self, user_id=None, session_id=None) -> ShoppingCart
def get_cart(self, cart_id: str) -> Optional[ShoppingCart]
def add_item(self, cart_id, product_id, quantity=1, variant_id=None) -> Dict[str, Any]
def remove_item(self, cart_id, product_id, variant_id=None) -> Dict[str, Any]
def update_quantity(self, cart_id, product_id, quantity, variant_id=None) -> Dict[str, Any]
def calculate_total(self, cart_id, tax_rate=0.0, shipping_cost=0.0, discount_amount=0.0) -> Dict[str, float]
def clear_cart(self, cart_id: str) -> bool
```

### OrderManager

```python
def create_order(self, user_id, items, shipping_address, billing_address=None, payment_method=None, shipping_method=ShippingMethod.STANDARD, tax_rate=0.0, shipping_cost=0.0, discount_amount=0.0) -> Order
def update_order_status(self, order_id: str, status: OrderStatus) -> bool
def update_payment_status(self, order_id: str, payment_status: PaymentStatus) -> bool
def add_tracking_number(self, order_id: str, tracking_number: str) -> bool
def cancel_order(self, order_id: str) -> Dict[str, Any]
def refund_order(self, order_id: str, amount=None) -> Dict[str, Any]
def get_order(self, order_id: str) -> Optional[Order]
def get_user_orders(self, user_id: str) -> List[Order]
def get_orders_by_status(self, status: OrderStatus) -> List[Order]
def get_fulfillment_queue(self) -> List[Dict[str, Any]]
def get_order_stats(self) -> Dict[str, Any]
```

### PricingEngine

```python
def create_discount(self, code, name, discount_type, value, min_order_amount=0, usage_limit=None, start_date=None, end_date=None) -> Discount
def apply_discount(self, discount_id: str, subtotal: float) -> Dict[str, float]
def validate_coupon(self, code: str) -> Dict[str, Any]
def calculate_bundle_price(self, items: List[Dict], bundle_discount_percent=10.0) -> Dict[str, float]
def calculate_tiered_discount(self, amount: float, tiers: List[Tuple[float, float]]) -> float
def get_discount_stats(self) -> Dict[str, Any]
```

### InventoryManager

```python
def adjust_stock(self, product_id, quantity_change, movement_type=InventoryMovement.ADJUSTMENT, reason="", reference_id=None) -> Dict[str, Any]
def reserve_stock(self, product_id: str, quantity: int) -> bool
def release_reservation(self, product_id: str, quantity: int) -> bool
def get_stock_status(self, product_id: str) -> Dict[str, Any]
def get_low_stock_items(self) -> List[Dict[str, Any]]
def get_movement_history(self, product_id=None, limit=100) -> List[Dict[str, Any]]
def generate_report(self) -> Dict[str, Any]
```

---

## Data Models Reference

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| Product | Catalog item | id, name, slug, price, variants, images, status |
| ProductVariant | SKU variant | sku, attributes, price, stock, barcode |
| ShoppingCart | Cart session | id, items, coupons, shipping_address |
| CartItem | Cart line item | product_id, variant_id, quantity, price |
| Order | Purchase order | id, items, status, payment, shipping, totals |
| Customer | Buyer profile | id, email, name, segment, loyalty_points |
| Discount | Coupon/promo | code, type, value, limits, validity |
| FraudAssessment | Risk result | risk_level, risk_score, flags, action |
| TaxRate | Tax config | rate, jurisdiction, type |
| Address | Location | line1, city, state, postal_code, country |

---

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Product not in search results | Status is DRAFT | Set status to ACTIVE |
| Cart total is 0 | Empty cart | Add items before calculating |
| Order won't cancel | Already SHIPPED | Only PENDING/CONFIRMED can cancel |
| Discount not applying | Below minimum order | Check min_order_amount |
| Stock shows negative | Overselling | Implement stock reservation |
| Fraud score too high | Multiple flags | Review individual flag weights |
| Tax calculation returns 0 | No matching tax rates | Add tax rates for jurisdiction |

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

---

## Checklist

- [ ] Products validated before publishing
- [ ] All variants have unique SKUs
- [ ] Stock quantities set for all active products
- [ ] Tax rates configured for all jurisdictions
- [ ] Shipping rates defined per method
- [ ] Fraud rules tested with sample transactions
- [ ] Discount codes tested with edge cases
- [ ] Order confirmation emails configured
- [ ] Return/refund policy documented
- [ ] Dashboard monitoring enabled
