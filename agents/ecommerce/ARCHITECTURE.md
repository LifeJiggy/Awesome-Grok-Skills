# E-Commerce Agent — System Architecture

## Overview

The E-Commerce Agent is a modular, service-oriented platform for managing
online retail operations. It covers the complete commerce lifecycle: product
catalog management, shopping cart operations, order processing, payment handling,
inventory tracking, dynamic pricing, fraud detection, tax calculation, and
customer relationship management.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       EcommerceAgent                                     │
│                   (Top-level Orchestrator)                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────────────┐ │
│  │  Product      │  │  Shopping Cart │  │  Order                       │ │
│  │  Catalog      │  │  Manager       │  │  Manager                     │ │
│  │              │  │                │  │                              │ │
│  │  - Products  │  │  - Add/Remove  │  │  - Create orders             │ │
│  │  - Variants  │  │  - Calculate   │  │  - Status tracking           │ │
│  │  - Search    │  │  - Coupons     │  │  - Fulfillment queue         │ │
│  └──────┬───────┘  └───────┬────────┘  └──────────────┬───────────────┘ │
│         │                  │                           │                  │
│  ┌──────┴───────┐  ┌──────┴────────┐  ┌──────────────┴───────────────┐ │
│  │  Pricing      │  │  Inventory   │  │  Fraud                       │ │
│  │  Engine       │  │  Manager     │  │  Detector                     │ │
│  │              │  │              │  │                              │ │
│  │  - Discounts │  │  - Stock     │  │  - Risk scoring               │ │
│  │  - Bundles   │  │  - Reservatn │  │  - Rule engine                │ │
│  │  - Tiered    │  │  - Alerts    │  │  - Assessment history         │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                     Tax Engine                                       │ │
│  │  - Multi-jurisdiction support                                        │ │
│  │  - Category-specific rates                                           │ │
│  │  - Compound tax handling                                             │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                     Customer Store                                   │ │
│  │  - Profiles, addresses, loyalty points                              │ │
│  │  - Order history, segmentation                                       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dives

### 1. ProductCatalog

**Purpose**: Manages the full product catalog — creation, updates, search,
filtering, and organization by category and tags.

```
┌─────────────────────────────────────────┐
│          ProductCatalog                  │
├─────────────────────────────────────────┤
│  _products: Dict[str, Product]          │
│  _categories: Dict[str, List[str]]      │
│  _tags_index: Dict[str, List[str]]      │
├─────────────────────────────────────────┤
│  add_product()          → str           │
│  update_product()       → Product       │
│  get_product()          → Product       │
│  delete_product()       → bool          │
│  search_products()      → List[Product] │
│  get_categories()       → Dict          │
│  bulk_update_status()   → int           │
│  get_catalog_stats()    → Dict          │
└─────────────────────────────────────────┘
```

**Search Pipeline**:
```
Input: query, category, price range, tags, status
  ↓
Filter by query (name, description, category, tags)
  ↓
Filter by category
  ↓
Filter by price range
  ↓
Filter by tags
  ↓
Filter by status
  ↓
Filter by stock (optional)
  ↓
Sort by (name, price, created, stock)
  ↓
Apply offset/limit
  ↓
Return List[Product]
```

**Product Variant Model**:
```
Product
  ├── Variant A (SKU-001, Blue, Size M)
  ├── Variant B (SKU-002, Blue, Size L)
  └── Variant C (SKU-003, Red, Size M)
```

### 2. ShoppingCartManager

**Purpose**: Manages shopping cart lifecycle — creation, item management,
totals calculation, and coupon application.

```
┌──────────────────────────────────────────┐
│         ShoppingCartManager              │
├──────────────────────────────────────────┤
│  _carts: Dict[str, ShoppingCart]         │
│  _catalog: ProductCatalog                │
├──────────────────────────────────────────┤
│  create_cart()           → ShoppingCart  │
│  get_cart()              → ShoppingCart  │
│  add_item()              → Dict          │
│  remove_item()           → Dict          │
│  update_quantity()       → Dict          │
│  calculate_total()       → Dict[float]   │
│  clear_cart()            → bool          │
└──────────────────────────────────────────┘
```

**Cart Calculation Flow**:
```
Cart Items
  ↓
Sum line totals (price × quantity)
  ↓
Apply coupon discount
  ↓
Calculate tax (jurisdiction-based)
  ↓
Calculate shipping (method-based)
  ↓
Return: subtotal, tax, shipping, discount, total
```

### 3. OrderManager

**Purpose**: Order creation, payment tracking, status management, fulfillment
queue, and refund processing.

```
┌──────────────────────────────────────────┐
│          OrderManager                    │
├──────────────────────────────────────────┤
│  _orders: Dict[str, Order]               │
│  _user_orders: Dict[str, List[str]]      │
│  _fulfillment_queue: List[str]           │
├──────────────────────────────────────────┤
│  create_order()            → Order       │
│  update_order_status()     → bool        │
│  update_payment_status()   → bool        │
│  add_tracking_number()     → bool        │
│  cancel_order()            → Dict        │
│  refund_order()            → Dict        │
│  get_user_orders()         → List[Order] │
│  get_orders_by_status()    → List[Order] │
│  get_fulfillment_queue()   → List[Dict]  │
│  get_order_stats()         → Dict        │
└──────────────────────────────────────────┘
```

**Order Lifecycle**:
```
PENDING → CONFIRMED → PROCESSING → SHIPPED → DELIVERED
   │          │            │           │
   └──────────┴────────────┴───────────┘
              ↓ (at any paid state)
           CANCELLED
              ↓
           REFUNDED
```

### 4. PricingEngine

**Purpose**: Discount creation, coupon validation, bundle pricing, tiered
discounts, and promotional offer management.

```
┌──────────────────────────────────────────┐
│          PricingEngine                   │
├──────────────────────────────────────────┤
│  _discounts: Dict[str, Discount]         │
│  _pricing_rules: List[Dict]              │
├──────────────────────────────────────────┤
│  create_discount()        → Discount     │
│  apply_discount()         → Dict         │
│  validate_coupon()        → Dict         │
│  calculate_bundle_price() → Dict         │
│  calculate_tiered_discount() → float     │
│  get_discount_stats()     → Dict         │
└──────────────────────────────────────────┘
```

**Discount Types**:
| Type | Calculation | Example |
|------|------------|---------|
| Percentage | subtotal × (value/100) | 20% off $100 = $20 discount |
| Fixed | Direct deduction | $15 off $100 = $15 discount |
| Free Shipping | Set shipping to $0 | Free shipping on orders > $50 |
| BOGO | Buy X get Y free | Buy 2 get 1 free |
| Tiered | Different rates at thresholds | 10% off $50+, 20% off $100+ |

### 5. InventoryManager

**Purpose**: Stock tracking, reservations, movement history, low-stock alerts,
and reorder management.

```
┌──────────────────────────────────────────┐
│         InventoryManager                 │
├──────────────────────────────────────────┤
│  _inventory: Dict[str, Dict]             │
│  _movements: List[Dict]                  │
│  _alerts: List[Dict]                     │
├──────────────────────────────────────────┤
│  adjust_stock()            → Dict        │
│  reserve_stock()           → bool        │
│  release_reservation()     → bool        │
│  get_stock_status()        → Dict        │
│  get_low_stock_items()     → List[Dict]  │
│  get_movement_history()    → List[Dict]  │
│  generate_report()         → Dict        │
└──────────────────────────────────────────┘
```

**Inventory Movement Types**:
| Movement | Direction | Trigger |
|----------|-----------|---------|
| Purchase | + | Supplier delivery |
| Sale | - | Order confirmed |
| Return | + | Customer return |
| Adjustment | +/- | Manual correction |
| Transfer | +/- | Warehouse move |
| Damage | - | Damaged goods |
| Reservation | - | Cart/checkout hold |
| Release | + | Cart abandoned |

### 6. FraudDetector

**Purpose**: Transaction risk assessment using rule-based scoring with
configurable thresholds and custom rules.

```
┌──────────────────────────────────────────┐
│          FraudDetector                   │
├──────────────────────────────────────────┤
│  _rules: List[Dict]                      │
│  _assessments: List[FraudAssessment]     │
├──────────────────────────────────────────┤
│  add_rule()               → None         │
│  assess_transaction()     → FraudAssess  │
│  get_assessment_stats()   → Dict         │
└──────────────────────────────────────────┘
```

**Risk Scoring Matrix**:
| Signal | Score | Threshold |
|--------|-------|-----------|
| High-risk country | +30 | Country in watchlist |
| High-value transaction | +20 | Amount > $500 |
| High velocity | +25 | > 5 orders/hour |
| First-time customer | +15 | 0 prior orders |
| Address mismatch | +20 | Billing ≠ shipping |

**Action Thresholds**:
| Risk Score | Level | Action |
|-----------|-------|--------|
| 0-29 | LOW | Approve |
| 30-49 | MEDIUM | Additional verification |
| 50-69 | HIGH | Manual review |
| 70+ | CRITICAL | Block |

### 7. TaxEngine

**Purpose**: Multi-jurisdiction tax calculation with support for different tax
types, categories, and compound rates.

```
┌──────────────────────────────────────────┐
│            TaxEngine                     │
├──────────────────────────────────────────┤
│  _tax_rates: Dict[str, TaxRate]          │
├──────────────────────────────────────────┤
│  add_tax_rate()            → None        │
│  calculate_tax()           → Dict        │
└──────────────────────────────────────────┘
```

**Tax Resolution**:
```
Amount + Jurisdiction + Category
  ↓
Filter applicable TaxRate entries
  ↓
Calculate per-rate tax
  ↓
Sum total tax
  ↓
Return: total_tax, effective_rate, breakdown
```

---

## Data Flow Diagrams

### Checkout Flow

```
Customer clicks "Checkout"
     │
     ▼
┌─────────────────────────────────────┐
│  EcommerceAgent.checkout()          │
└────────────┬────────────────────────┘
             │
     ┌───────┼───────────────┐
     ▼       ▼               ▼
  Validate  Apply Coupon   Calculate
  Cart      (if present)   Tax + Shipping
     │       │               │
     └───────┼───────────────┘
             ▼
      Create Order
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  Reserve  Fraud      Charge
  Stock    Assessment Payment
     │       │           │
     └───────┼───────────┘
             ▼
      Fraud Check
             │
     ┌───────┴───────┐
     ▼               ▼
   PASS            FAIL
     │               │
  Confirm         Block
  Order           Order
     │               │
     ▼               ▼
  Return         Return
  Order ID       Error
```

### Product Search Flow

```
Search Query
     │
     ▼
┌──────────────────────────────────┐
│  ProductCatalog.search_products()│
└────────────┬─────────────────────┘
             │
     ┌───────┼──────────────────────────┐
     ▼       ▼         ▼               ▼
  Text    Category  Price Range     Tag
  Match   Filter    Filter          Filter
     │       │         │               │
     └───────┼─────────┴───────────────┘
             ▼
      Status Filter
             │
             ▼
      Stock Filter
             │
             ▼
        Sort + Paginate
             │
             ▼
      Return Products
```

### Inventory Adjustment Flow

```
Inventory Event
     │
     ▼
┌──────────────────────────────────┐
│  InventoryManager.adjust_stock() │
└────────────┬─────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  Update   Record      Check
  Quantity Movement    Thresholds
     │       │           │
     └───────┼───────────┘
             ▼
      Low Stock?
             │
     ┌───────┴───────┐
     ▼               ▼
    YES             NO
     │               │
  Generate        Done
  Alert
```

---

## Design Patterns

### Service Locator Pattern
The `EcommerceAgent` orchestrator acts as a service locator — all sub-engines
are accessible via properties, providing a single entry point while maintaining
separation of concerns.

### Money Value Object
The `Money` dataclass encapsulates monetary values with currency, preventing
accidental mixing of currencies and providing arithmetic operations.

### Specification Pattern
Product search uses a chain of filter specifications — each filter independently
narrows the result set, making it easy to add new filter dimensions.

### Observer Pattern (Alerts)
The InventoryManager generates alerts when thresholds are breached. These alerts
can be consumed by notification services, dashboards, or automated reorder
systems.

### Strategy Pattern (Pricing)
Different discount types (percentage, fixed, BOGO, tiered) implement the same
`calculate_discount()` interface, allowing the PricingEngine to apply any
discount type without conditional branching.

---

## Data Model Relationships

```
Customer ──────────┐
  │                 │
  ├── Address (1:N) │
  │                 │
  └── Order (1:N) ──┤
                     │
Order ──────────────┤
  │                 │
  ├── CartItem (N:1)│
  ├── Address (N:1) │
  └── Payment       │
                     │
Product ─────────────┤
  │                 │
  ├── Variant (1:N) │
  └── Category (N:1)│
                     │
Discount ────────────┘
  │
  └── Applied to Order/Cart
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | dataclasses + Enum |
| Validation | Custom validate() methods |
| Logging | stdlib logging |
| Storage | In-memory dicts (pluggable) |
| Serialization | dataclass → dict (JSON-serializable) |
| Testing | pytest + hypothesis |
| Payment | Stripe/PayPal adapters (pluggable) |
| Tax | Avalara/TaxJar adapters (pluggable) |

---

## Security Considerations

1. **PCI Compliance**: Payment card data must never be stored in plain text.
   Use tokenization via payment processor APIs.
2. **Fraud Prevention**: The FraudDetector provides real-time risk assessment.
   High-risk transactions are held for manual review.
3. **Data Encryption**: Customer PII (email, phone, addresses) must be encrypted
   at rest and in transit.
4. **Access Control**: Order modifications require authentication. Admin operations
   (bulk status changes, refunds) require authorization.
5. **Audit Trail**: All inventory movements and order status changes are logged
   with timestamps and references.
6. **Input Validation**: All user inputs are validated before processing to
   prevent injection attacks.

---

## Scalability Considerations

| Dimension | Current | Target |
|-----------|---------|--------|
| Products | 10,000 | 1,000,000+ |
| Orders/day | 100 | 100,000+ |
| Concurrent carts | 1,000 | 100,000+ |
| Inventory SKUs | 10,000 | 500,000+ |
| Customers | 10,000 | 10,000,000+ |

**Scaling Strategy**:
- Move from in-memory to PostgreSQL/Redis for persistent storage.
- Use Elasticsearch for product search at scale.
- Shard order processing by customer_id or region.
- Implement event sourcing for inventory movements.
- Use message queues (RabbitMQ/Kafka) for async order processing.

---

## Extension Points

1. **Payment Gateways**: Add new `PaymentMethod` values and implement adapter
   classes for each gateway (Stripe, PayPal, Square, etc.).
2. **Tax Providers**: Integrate Avalara, TaxJar, or Vertex for automated
   tax calculation.
3. **Fulfillment Services**: Connect ShipStation, EasyPost, or custom
   warehouse management systems.
4. **Fraud Rules**: Add custom rule functions via `FraudDetector.add_rule()`.
5. **Product Attributes**: Extend the `attributes` dict on Product for
   arbitrary product metadata.

---

## Configuration

```yaml
ecommerce_agent:
  catalog:
    max_products: 1000000
    search_index_enabled: true
    default_currency: USD

  cart:
    cart_expiry_hours: 24
    max_items_per_cart: 100
    allow_guest_checkout: true

  orders:
    auto_confirm: false
    cancellation_window_hours: 24
    return_window_days: 30

  pricing:
    max_discounts_per_order: 3
    allow_stackable_coupons: false
    min_order_for_coupon: 0

  inventory:
    low_stock_threshold: 10
    reorder_point: 20
    reservation_timeout_minutes: 30

  fraud:
    high_risk_countries: ["XX", "YY"]
    velocity_threshold: 5
    high_value_threshold: 500
    block_threshold: 70

  tax:
    default_country: US
    tax_calculation_service: internal  # or avalara, taxjar

  shipping:
    free_shipping_threshold: 50
    default_method: standard
    rates:
      standard: 5.99
      expedited: 12.99
      overnight: 24.99
```

---

## Performance Benchmarks

| Operation | Latency (p99) | Throughput |
|-----------|---------------|------------|
| Product search | < 50ms | 10K queries/s |
| Cart add/remove | < 10ms | 50K ops/s |
| Order creation | < 100ms | 1K orders/s |
| Inventory check | < 5ms | 100K/s |
| Fraud assessment | < 20ms | 5K/s |
| Tax calculation | < 15ms | 10K/s |

---

## Testing Strategy

| Test Type | Coverage Target | Tools |
|-----------|----------------|-------|
| Unit tests | 90%+ | pytest |
| Integration tests | Key flows | pytest + fixtures |
| Load tests | Throughput | locust |
| Property tests | Data invariants | hypothesis |
| Contract tests | API boundaries | schemathesis |
| E2E tests | Full checkout | playwright |

### Unit Test Examples

```python
# Product Catalog Tests
def test_add_product():
    catalog = ProductCatalog()
    product = Product(name="Test", price=9.99)
    pid = catalog.add_product(product)
    assert catalog.get_product(pid) is not None

def test_search_products():
    catalog = ProductCatalog()
    catalog.add_product(Product(name="Widget", category="Tools"))
    results = catalog.search_products(query="Widget")
    assert len(results) == 1

# Inventory Tests
def test_reserve_stock():
    inventory = InventoryManager()
    inventory.adjust_stock("P1", 100)
    assert inventory.reserve_stock("P1", 10)
    status = inventory.get_stock_status("P1")
    assert status["reserved"] == 10
    assert status["available"] == 90

# Fraud Detection Tests
def test_fraud_scoring():
    detector = FraudDetector()
    detector.add_rule("high_amount", lambda t: 50 if t.get("amount", 0) > 1000 else 0)
    assessment = detector.assess_transaction({"amount": 1500})
    assert assessment.risk_score > 0
```

### Integration Test Examples

```python
def test_checkout_flow():
    agent = EcommerceAgent()
    
    # Setup
    pid = agent.catalog.add_product(Product(name="Test", price=29.99))
    agent.inventory.adjust_stock(pid, 100)
    
    # Cart
    cart = agent.cart_manager.create_cart(user_id="user_001")
    agent.cart_manager.add_item(cart.cart_id, pid, quantity=2)
    
    # Checkout
    result = agent.checkout(
        cart_id=cart.cart_id,
        customer_id="user_001",
        shipping_address=Address(line1="123 Main St", city="Portland", state="OR", postal_code="97201", country="US"),
        payment_method=PaymentMethod.CREDIT_CARD,
    )
    
    assert "order_id" in result
    assert result["total"] > 0
    
    # Verify inventory
    status = agent.inventory.get_stock_status(pid)
    assert status["quantity"] == 98
```

### Performance Test Scenarios

| Scenario | Target | Description |
|----------|--------|-------------|
| Product search | < 10ms | Search 10K products |
| Cart calculation | < 5ms | Calculate totals with tax |
| Order creation | < 20ms | Create order with items |
| Fraud assessment | < 10ms | Evaluate transaction risk |
| Checkout flow | < 100ms | End-to-end checkout |

---

## Deployment Architecture

### Single-Instance Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVER                         │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  EcommerceAgent                        │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │ │
│  │  │ Catalog │ │  Cart   │ │  Order  │ │ Pricing │    │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │ │
│  │  │Inventory│ │  Fraud  │ │   Tax   │ │ Customer│    │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  DATA LAYER                            │ │
│  │  In-Memory │ Optional DB │ Cache (Redis)              │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Distributed Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                        LOAD BALANCER                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Server 1   │       │   Server 2   │       │   Server 3   │
│  Ecommerce   │       │  Ecommerce   │       │  Ecommerce   │
│    Agent     │       │    Agent     │       │    Agent     │
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Shared Database    │
                    │   (PostgreSQL)       │
                    └─────────────────────┘
```

---

## Security Architecture

### Authentication Flow

```
  Client Request
       │
       ▼
  ┌──────────────┐
  │   API Gateway │
  │  (Auth Check) │
  └──────┬───────┘
         │
    ┌────┴────┐
    │ Valid?  │
    └────┬────┘
    Yes  │  No
    │    │   │
    ▼    │   ▼
  Process│  401 Unauthorized
  Request│
```

### Data Encryption

| Data Type | Encryption | Storage |
|-----------|------------|---------|
| Payment tokens | AES-256 | Payment processor |
| Customer PII | AES-256 | Database |
| API keys | Hashed | Environment variables |
| Session data | TLS in transit | Redis/Memory |

### PCI DSS Compliance

- Never store raw card numbers
- Use tokenization via payment processor
- Validate CVV on every transaction
- Implement address verification (AVS)
- Use HTTPS for all endpoints

---

## Monitoring and Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Order success rate | Successful checkouts / attempts | < 95% |
| Average checkout time | Time from cart to order | > 5 seconds |
| Fraud block rate | Blocked transactions / total | > 5% |
| Inventory accuracy | Stock matches system | < 99% |
| API response time | 95th percentile | > 500ms |
| Error rate | Errors / total requests | > 1% |

### Logging Strategy

```python
# Structured logging example
import logging

logger = logging.getLogger("ecommerce")

# Order creation
logger.info("order_created", extra={
    "order_id": order.order_id,
    "user_id": order.user_id,
    "total": order.total,
    "items_count": len(order.items),
})

# Fraud detection
logger.warning("fraud_detected", extra={
    "transaction_id": txn.id,
    "risk_score": assessment.risk_score,
    "flags": assessment.flags,
})
```

### Health Check Endpoint

```python
def health_check():
    return {
        "status": "healthy",
        "components": {
            "catalog": check_catalog(),
            "inventory": check_inventory(),
            "orders": check_orders(),
            "fraud": check_fraud_detector(),
        },
        "timestamp": datetime.utcnow().isoformat(),
    }
```

---

## Data Retention Policy

| Data Type | Retention | Archive After |
|-----------|-----------|---------------|
| Product data | Indefinite | Never |
| Order data | 7 years | 1 year |
| Customer data | Until deletion request | 2 years |
| Fraud assessments | 2 years | 6 months |
| Audit logs | 3 years | 1 year |
| Cart data | 30 days | Immediate |

---

## Disaster Recovery

### Backup Strategy

| Data | Frequency | Method | Recovery Time |
|------|-----------|--------|---------------|
| Product catalog | Daily | Full dump | < 1 hour |
| Order database | Real-time | Replication | < 5 minutes |
| Customer data | Daily | Encrypted backup | < 2 hours |
| Configuration | On change | Version control | < 15 minutes |

### Recovery Procedures

1. **Data corruption**: Restore from last backup
2. **Service failure**: Restart and verify state
3. **Database failure**: Switch to replica
4. **Full outage**: Deploy to backup region

---

**See Also**: [GROK.md](./GROK.md) for agent identity and capabilities,
[README.md](./README.md) for quick start and API reference.
