# E-Commerce Agent

Full-stack e-commerce platform management covering product catalogs, shopping
carts, order processing, payment handling, inventory tracking, dynamic pricing,
fraud detection, tax calculation, and customer management.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The E-Commerce Agent provides a complete, modular platform for managing online
retail operations. It handles everything from product listing through order
fulfillment, with built-in fraud detection, dynamic pricing, and accurate tax
calculation.

Each sub-engine (Catalog, Cart, Order, Pricing, Inventory, Fraud, Tax) operates
independently while being orchestrated by a top-level agent that provides a
unified checkout flow and store dashboard.

### Key Benefits

- **Zero Dependencies**: Pure Python stdlib, no external packages required
- **Modular Design**: Use only the components you need
- **Type-Safe**: Full type hints on all public methods
- **Extensible**: Easy to add custom fraud rules, pricing strategies, etc.
- **Auditable**: Complete trail of all financial transactions

### Use Cases

| Use Case | Description |
|----------|-------------|
| Product Catalog | CRUD operations, variants, search, bulk updates |
| Shopping Cart | Create, manage, calculate totals, apply coupons |
| Order Processing | Full lifecycle from pending to delivered |
| Inventory Management | Stock tracking, reservations, alerts |
| Fraud Detection | Rule-based scoring, velocity checks |
| Tax Calculation | Multi-jurisdiction rates, category handling |
| Customer Management | Profiles, segments, loyalty programs |

---

## Features

### Product Catalog
- Full CRUD operations for products and variants
- Multi-attribute variant management (size, color, material)
- Advanced search with text, category, price, and tag filters
- Bulk status updates
- Catalog statistics and reporting
- SKU management with barcode support
- Image URL tracking per product

### Shopping Cart
- Cart creation for authenticated and guest users
- Add, remove, update quantity operations
- Coupon code validation and application
- Tax and shipping calculation
- Cart expiry management
- Multi-currency support
- Saved cart functionality

### Order Management
- Complete order lifecycle (pending → delivered)
- Payment status tracking
- Fulfillment queue management
- Tracking number integration
- Order cancellation and refund processing
- Order history and search
- Export capabilities

### Dynamic Pricing
- Percentage and fixed discounts
- Buy-one-get-one (BOGO) promotions
- Tiered discount structures
- Bundle pricing
- Coupon validation with usage limits
- Time-limited promotions
- Customer-segment pricing

### Inventory Management
- Real-time stock tracking
- Stock reservation during checkout
- Movement history logging
- Low-stock and out-of-stock alerts
- Reorder point management
- Multi-warehouse support
- Batch inventory operations

### Fraud Detection
- Rule-based risk scoring
- Transaction velocity monitoring
- Address mismatch detection
- Configurable risk thresholds
- Assessment history and statistics
- Device fingerprinting
- Geolocation analysis

### Tax Calculation
- Multi-jurisdiction tax rates
- Category-specific tax handling
- Compound tax support
- Tax breakdown reporting
- Tax-inclusive pricing
- Exemption handling
- Audit-ready tax reports

### Customer Management
- Customer profiles with segmentation
- Loyalty points tracking
- Purchase history
- Wishlist management
- Address book
- Communication preferences
- GDPR compliance tools

---

## Architecture

### Component Diagram

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
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Inventory │ │  Fraud     │ │  Tax       │ │  Customer  │           │
│  │  Manager   │ │  Detector  │ │  Engine    │ │  Store     │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

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
```

### Order Lifecycle

```
  PENDING → CONFIRMED → PROCESSING → SHIPPED → DELIVERED
       │         │            │
       │         │            └──► CANCELLED
       │         └──► REVIEW → CONFIRMED/CANCELLED
       └──► CANCELLED
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed component diagrams,
data flows, and design patterns.

---

## Quick Start

```python
from agents.ecommerce.agent import (
    EcommerceAgent, Product, Address, PaymentMethod, ShippingMethod,
)

agent = EcommerceAgent()

# Add a product
product = Product(name="T-Shirt", category="Apparel", price=29.99)
pid = agent.catalog.add_product(product)
agent.inventory.adjust_stock(pid, 100)

# Create cart and add item
cart = agent.cart_manager.create_cart(user_id="user_001")
agent.cart_manager.add_item(cart.cart_id, pid, quantity=2)

# Checkout
result = agent.checkout(
    cart_id=cart.cart_id,
    customer_id="user_001",
    shipping_address=Address(line1="123 Main St", city="Portland", state="OR", postal_code="97201", country="US"),
    payment_method=PaymentMethod.CREDIT_CARD,
)
print(f"Order: {result['order_id']}, Total: ${result['total']:.2f}")
```

---

## Installation

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -r requirements.txt
python agents/ecommerce/agent.py
```

### Requirements

- Python 3.10+
- No external dependencies (stdlib only)

### Platform Support

- Windows 10+
- macOS 10.15+
- Linux (Ubuntu 18.04+, Debian 9+)

---

## Usage

### Running the Demo

```bash
python agents/ecommerce/agent.py
```

Demonstrates product creation, inventory management, cart operations,
discount application, checkout, and dashboard generation.

### Programmatic Usage

```python
from agents.ecommerce.agent import EcommerceAgent

agent = EcommerceAgent()

# Check agent status
print(agent.get_status())

# Get store dashboard
dashboard = agent.get_store_dashboard()
print(f"Products: {dashboard['catalog']['total_products']}")
print(f"Revenue: ${dashboard['orders']['total_revenue']:,.2f}")
```

### Using Individual Components

```python
from agents.ecommerce.agent import ProductCatalog, InventoryManager

# Use catalog independently
catalog = ProductCatalog()
product_id = catalog.add_product(product)

# Use inventory independently
inventory = InventoryManager()
inventory.adjust_stock(product_id, 100)
status = inventory.get_stock_status(product_id)
```

---

## API Reference

### EcommerceAgent (Top-Level)

| Method | Description | Returns |
|--------|-------------|---------|
| `checkout(...)` | Full checkout flow | `Dict` |
| `get_store_dashboard()` | Store metrics | `Dict` |
| `add_customer(customer)` | Register customer | `str` |
| `get_customer(id)` | Get customer | `Customer` |
| `get_status()` | Agent status | `Dict` |

### ProductCatalog

| Method | Description | Returns |
|--------|-------------|---------|
| `add_product(product)` | Add product | `str` |
| `update_product(id, updates)` | Update product | `Product` |
| `get_product(id)` | Get product | `Product` |
| `delete_product(id)` | Delete product | `bool` |
| `search_products(...)` | Search | `List[Product]` |
| `get_categories()` | Category counts | `Dict` |
| `bulk_update_status(ids, status)` | Bulk update | `int` |
| `get_catalog_stats()` | Stats | `Dict` |

### ShoppingCartManager

| Method | Description | Returns |
|--------|-------------|---------|
| `create_cart(user_id, session_id)` | Create cart | `ShoppingCart` |
| `get_cart(id)` | Get cart | `ShoppingCart` |
| `add_item(cart_id, product_id, qty)` | Add item | `Dict` |
| `remove_item(cart_id, product_id)` | Remove item | `Dict` |
| `update_quantity(cart_id, product_id, qty)` | Update qty | `Dict` |
| `calculate_total(cart_id, tax, shipping)` | Calculate | `Dict` |
| `clear_cart(cart_id)` | Clear cart | `bool` |

### OrderManager

| Method | Description | Returns |
|--------|-------------|---------|
| `create_order(...)` | Create order | `Order` |
| `update_order_status(id, status)` | Update status | `bool` |
| `update_payment_status(id, status)` | Update payment | `bool` |
| `add_tracking_number(id, tracking)` | Add tracking | `bool` |
| `cancel_order(id)` | Cancel order | `Dict` |
| `refund_order(id, amount)` | Refund | `Dict` |
| `get_user_orders(user_id)` | User orders | `List[Order]` |
| `get_fulfillment_queue()` | Queue | `List[Dict]` |
| `get_order_stats()` | Stats | `Dict` |

### PricingEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `create_discount(code, name, type, value, ...)` | Create | `Discount` |
| `apply_discount(id, subtotal)` | Apply | `Dict` |
| `validate_coupon(code)` | Validate | `Dict` |
| `calculate_bundle_price(items, discount)` | Bundle | `Dict` |
| `calculate_tiered_discount(amount, tiers)` | Tiered | `float` |
| `get_discount_stats()` | Stats | `Dict` |

### InventoryManager

| Method | Description | Returns |
|--------|-------------|---------|
| `adjust_stock(id, qty, type, reason)` | Adjust | `Dict` |
| `reserve_stock(id, qty)` | Reserve | `bool` |
| `release_reservation(id, qty)` | Release | `bool` |
| `get_stock_status(id)` | Status | `Dict` |
| `get_low_stock_items()` | Low stock | `List[Dict]` |
| `get_movement_history(id, limit)` | History | `List[Dict]` |
| `generate_report()` | Report | `Dict` |

### FraudDetector

| Method | Description | Returns |
|--------|-------------|---------|
| `add_rule(name, check_fn, weight)` | Add rule | `None` |
| `assess_transaction(txn, customer)` | Assess | `FraudAssessment` |
| `get_assessment_stats()` | Stats | `Dict` |

### TaxEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `add_tax_rate(tax_rate)` | Add rate | `None` |
| `calculate_tax(amount, state, city, country)` | Calculate | `Dict` |

---

## Examples

### Example 1: Product with Variants

```python
from agents.ecommerce.agent import Product, ProductVariant

product = Product(
    name="Running Shoes",
    category="Footwear",
    price=129.99,
    variants=[
        ProductVariant(
            sku="RS-BLK-10",
            name="Black Size 10",
            attributes={"color": "Black", "size": "10"},
            price=129.99,
            stock_quantity=25,
        ),
        ProductVariant(
            sku="RS-WHT-10",
            name="White Size 10",
            attributes={"color": "White", "size": "10"},
            price=129.99,
            stock_quantity=15,
        ),
    ],
)
pid = agent.catalog.add_product(product)
```

### Example 2: Bulk Order Processing

```python
for order_data in bulk_orders:
    order = agent.order_manager.create_order(
        user_id=order_data["user_id"],
        items=[CartItem(**item) for item in order_data["items"]],
        shipping_address=Address(**order_data["address"]),
        payment_method=PaymentMethod.CREDIT_CARD,
    )
    agent.order_manager.update_order_status(order.order_id, OrderStatus.PROCESSING)
```

### Example 3: Custom Fraud Rules

```python
# High-value international transaction
agent.fraud_detector.add_rule(
    name="international_high_value",
    check_fn=lambda t: 40 if t.get("country") != "US" and t.get("amount", 0) > 500 else 0,
    weight=2.0,
)

# Velocity check
agent.fraud_detector.add_rule(
    name="velocity_check",
    check_fn=lambda t: 30 if t.get("velocity", 0) > 5 else 0,
    weight=1.5,
)

assessment = agent.fraud_detector.assess_transaction({
    "amount": 750, "country": "GB", "velocity": 1
})
```

### Example 4: Inventory Monitoring

```python
report = agent.inventory.generate_report()

if report["out_of_stock_count"] > 0:
    print(f"WARNING: {report['out_of_stock_count']} products out of stock!")

for item in report["low_stock_items"]:
    print(f"Low stock: {item['product_id']} ({item['available']} remaining)")
```

### Example 5: Discount Campaign

```python
# Create tiered discount campaign
agent.pricing.create_discount(
    code="BLACKFRI2025",
    name="Black Friday 2025",
    discount_type=DiscountType.PERCENTAGE,
    value=25,
    min_order_amount=100,
    usage_limit=10000,
    start_date=datetime(2025, 11, 28),
    end_date=datetime(2025, 11, 30),
)

# Validate and apply
validation = agent.pricing.validate_coupon("BLACKFRI2025")
if validation["valid"]:
    result = agent.pricing.apply_discount(validation["discount_id"], subtotal=250)
    print(f"Discount: ${result['discount_amount']:.2f}")
```

---

## Configuration

### Agent Configuration (YAML)

```yaml
ecommerce_agent:
  catalog:
    max_products: 1000000
    default_currency: USD

  cart:
    cart_expiry_hours: 24
    max_items_per_cart: 100
    allow_guest_checkout: true

  orders:
    cancellation_window_hours: 24
    return_window_days: 30

  inventory:
    low_stock_threshold: 10
    reorder_point: 20
    reservation_timeout_minutes: 30

  fraud:
    high_risk_countries: ["XX", "YY"]
    velocity_threshold: 5
    block_threshold: 70

  shipping:
    free_shipping_threshold: 50
    rates:
      standard: 5.99
      expedited: 12.99
      overnight: 24.99
```

### Environment Variables

```bash
# Payment
STRIPE_API_KEY=sk_test_...
PAYPAL_CLIENT_ID=...

# Shipping
SHIPSTATION_API_KEY=...

# Tax
AVALARA_API_KEY=...

# Analytics
SEGMENT_WRITE_KEY=...
```

---

## Best Practices

1. **Always validate products** before publishing to catch missing SKUs or
   negative prices.
2. **Reserve stock during checkout** to prevent overselling on high-demand items.
3. **Set fraud thresholds** appropriately for your industry — too strict loses
   sales, too loose invites fraud.
4. **Configure tax rates** for every jurisdiction you ship to before going live.
5. **Monitor low-stock alerts** daily to maintain healthy inventory levels.
6. **Use bundle pricing** for complementary products to increase AOV.
7. **Log all inventory movements** for audit trail and discrepancy investigation.
8. **Test checkout flow** end-to-end before every major sale event.
9. **Implement idempotency keys** for payment processing.
10. **Use webhooks** for real-time order status updates.

### Security Best Practices

- Never store raw credit card numbers
- Use tokenization via payment processor
- Implement PCI DSS compliance
- Validate all payment amounts server-side
- Use HTTPS for all payment endpoints

### Performance Best Practices

- Cache product search results
- Use database indexing for product queries
- Implement pagination for large catalogs
- Use async processing for order emails
- Optimize inventory queries with batch operations

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Product not searchable | Status is DRAFT | Set status to ACTIVE |
| Cart total shows $0 | No items in cart | Add items first |
| Order can't be cancelled | Status is SHIPPED | Only PENDING/CONFIRMED can cancel |
| Discount code rejected | Below minimum order | Check min_order_amount |
| Stock goes negative | Race condition | Implement stock reservation |
| Fraud score always high | Thresholds too aggressive | Adjust rule weights |
| Tax returns $0 | No matching rates | Add rates for that jurisdiction |
| Payment fails | Invalid card | Validate card details server-side |
| Shipping cost wrong | Missing address | Ensure full shipping address |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed error info
result = agent.checkout(...)
if "error" in result:
    print(f"Error: {result['error']}")
    print(f"Details: {result.get('details', {})}")
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Full type hints on all public methods
- Docstrings for all classes and public methods
- Zero external dependencies (stdlib only)
- Follow existing naming conventions
- Write tests for new functionality
- Update documentation for API changes

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[GROK.md](./GROK.md) for agent identity and operational guidelines.