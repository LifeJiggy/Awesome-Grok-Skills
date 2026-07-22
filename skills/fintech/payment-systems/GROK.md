---
name: "payment-systems"
category: "fintech"
version: "2.0.0"
tags: ["fintech", "payment-systems", "payments", "card-processing", "real-time-payments"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["python", "payment-processing-fundamentals"]
---

# Payment Systems

## Overview

Payment systems technology encompasses the infrastructure, protocols, and software that enable the transfer of money between parties—covering card networks, real-time payment rails, bank transfers, digital wallets, and emerging payment methods. This module provides a comprehensive framework for building payment processing systems that handle authorization, capture, settlement, reconciliation, and refund workflows across multiple payment methods and geographies.

The system addresses the critical requirements of modern payment processing: PCI-DSS compliance, tokenization of sensitive card data, 3D Secure 2.0 authentication, real-time fraud screening, multi-currency processing with dynamic currency conversion, payment orchestration across multiple acquirers, and regulatory compliance across jurisdictions (PSD2 SCA in Europe, PCI in all markets).

## Core Capabilities

- **Card Processing**: Authorization, capture, settlement, and refund processing for Visa, Mastercard, Amex, and Discover with EMV chip and contactless support
- **Tokenization Service**: PCI-compliant card tokenization with network tokenization (Visa/MC tokens) and vault management for recurring payments
- **3D Secure Authentication**: 3DS2 frictionless and challenge flow implementation for Strong Customer Authentication (SCA) compliance
- **Real-Time Payments**: Integration with instant payment rails (FedNow, RTP, UPI, PIX, SEPA Instant) for sub-second domestic transfers
- **Payment Orchestration**: Smart routing across multiple acquirers for optimal authorization rates, cost optimization, and failover handling
- **Fraud Screening**: Real-time transaction risk scoring using ML models with device fingerprinting, behavioral biometrics, and velocity checks
- **Multi-Currency Processing**: Dynamic currency conversion, multi-currency settlement, and FX rate management for cross-border payments
- **Subscription Billing**: Recurring payment management with retry logic, dunning campaigns, and subscription lifecycle management
- **Payment Reconciliation**: Automated matching of processor settlements with internal ledger entries and bank statements
- **Dispute Management**: Chargeback representment workflow, evidence collection, and win-rate optimization

## Usage Examples

### Card Payment Processing

```python
from fintech.payment_systems import PaymentProcessor, PaymentMethod, PaymentStatus

processor = PaymentProcessor(
    acquirers=["stripe", "adyen"],
    default_acquirer="stripe",
    pci_level="pci_dss_1",
)

# Authorize a card payment
auth = processor.authorize(
    amount=99.99,
    currency="USD",
    payment_method=PaymentMethod.CARD,
    card_token="tok_visa_4242",
    merchant_id="MERCHANT-001",
    metadata={"order_id": "ORD-12345"},
    three_ds=True,
)

print(f"Auth ID: {auth.authorization_id}")
print(f"Status: {auth.status.value}")
print(f"Risk Score: {auth.risk_score:.2f}")
if auth.requires_3ds:
    print(f"3DS URL: {auth.three_ds_url}")

# Capture authorized payment
if auth.status == PaymentStatus.AUTHORIZED:
    capture = processor.capture(
        authorization_id=auth.authorization_id,
        amount=99.99,
    )
    print(f"Capture: {capture.capture_id}")
```

### Tokenization & Vault

```python
from fintech.payment_systems import TokenizationService, TokenScope

tokens = TokenizationService(
    provider="stripe",
    network_tokenization=True,
    encryption_key_id="key_2026_v1",
)

# Tokenize a card
token = tokens.tokenize(
    card_number="4242424242424242",
    exp_month=12, exp_year=2028,
    cardholder_name="Jane Smith",
    scope=TokenScope.MERCHANT_VAULT,
)

print(f"Token: {token.token}")
print(f"Network Token: {token.network_token}")
print(f"Card Brand: {token.card_brand}")
print(f"Last 4: {token.last_four}")

# Use token for payment
payment = tokens.charge_token(
    token=token.token,
    amount=49.99,
    currency="USD",
)
```

### Subscription Billing

```python
from fintech.payment_systems import SubscriptionBilling, BillingInterval

billing = SubscriptionBilling(
    retry_policy="smart",
    max_retries=3,
    dunning_enabled=True,
)

# Create subscription
subscription = billing.create_subscription(
    customer_id="CUST-001",
    plan_id="plan_pro_monthly",
    payment_token="tok_visa_4242",
    billing_interval=BillingInterval.MONTHLY,
    trial_days=14,
)

print(f"Subscription: {subscription.subscription_id}")
print(f"Next billing: {subscription.next_billing_date}")
print(f"Amount: ${subscription.amount:.2f}/{subscription.interval.value}")

# Process renewal
renewal = billing.process_renewal(subscription.subscription_id)
print(f"Renewal status: {renewal.status}")
```

### Payment Reconciliation

```python
from fintech.payment_systems import ReconciliationEngine

recon = ReconciliationEngine(
    tolerance_cents=1,
    auto_match=True,
)

# Reconcile settlements with ledger
result = recon.reconcile(
    settlement_file="stripe_settlement_20260701.csv",
    ledger_entries="ledger_entries_20260701.json",
    bank_statement="bank_stmt_20260701.csv",
)

print(f"Matched: {result.matched_count}")
print(f"Unmatched settlements: {result.unmatched_settlements}")
print(f"Unmatched ledger: {result.unmatched_ledger}")
print(f"Discrepancies: ${result.total_discrepancy:.2f}")
```

## Architecture

```
Payment Methods
├── Card Networks (Visa, MC, Amex)
├── Real-Time Rails (FedNow, RTP, UPI)
├── Digital Wallets (Apple Pay, Google Pay)
├── Bank Transfers (ACH, SEPA, BACS)
└── Buy Now Pay Later (Affirm, Klarna)
         │
         ▼
┌─────────────────────┐
│  Payment Gateway     │──→ Auth, encryption, routing
│  (PCI-DSS L1)       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Orchestration       │──→ Smart routing, failover, optimization
│  (Multi-acquirer)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Processing Layer    │──→ Auth, capture, settlement, refunds
│  (Event-sourced)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Reconciliation      │──→ Settlement matching, dispute mgmt
│  + Ledger            │
└─────────────────────┘
```

## Best Practices

- Never store raw card numbers; use tokenization at the earliest possible point in the payment flow
- Implement idempotency keys on all payment endpoints to prevent duplicate charges from network retries
- Use network tokenization (Visa/MC tokens) instead of gateway tokens for higher authorization rates and reduced PCI scope
- Build acquirer failover logic: if primary acquirer declines due to technical issues, retry on secondary within 200ms
- Monitor authorization rates by card type, issuer country, and BIN to identify optimization opportunities
- Implement 3DS2 with proper exemptions (low-value, trusted merchant, recurring) to minimize friction while maintaining SCA compliance
- Reconcile daily: match processor settlements, bank deposits, and internal ledger entries before T+1
- Set up velocity checks to prevent card testing attacks (multiple small authorizations followed by large charge)
- Maintain detailed audit logs of all payment state transitions for PCI compliance and dispute evidence
- Test payment flows with sandbox/test cards covering all edge cases: insufficient funds, expired cards, lost/stolen, 3DS challenges

## Related Modules

- `fintech/digital-banking` - Account and ledger infrastructure for payment settlement
- `fintech/risk-engine` - ML fraud detection models for payment screening
- `fintech/compliance-automation` - PCI-DSS and PSD2 compliance automation
- `fintech/blockchain-finance` - DLT-based payment settlement rails

## Advanced Configuration

### Acquirer Configuration

```yaml
acquirers:
  stripe:
    api_key: "${STRIPE_API_KEY}"
    webhook_secret: "${STRIPE_WEBHOOK_SECRET}"
    enabled: true
    priority: 1
    supported_methods: ["card", "wallet"]
    currencies: ["USD", "EUR", "GBP"]
    fee_structure:
      percentage: 2.9
      fixed_cents: 30
    
  adyen:
    api_key: "${ADYEN_API_KEY}"
    merchant_account: "${ADYEN_MERCHANT_ACCOUNT}"
    enabled: true
    priority: 2
    supported_methods: ["card", "wallet", "bank_transfer"]
    currencies: ["USD", "EUR", "GBP", "JPY"]
    fee_structure:
      percentage: 2.5
      fixed_cents: 25
```

### 3D Secure Configuration

```yaml
three_ds:
  enabled: true
  version: "2.2"
  directory_server: "production"
  ACS:
    timeout_seconds: 30
    max_retries: 2
  exemptions:
    low_value:
      enabled: true
      threshold_eur: 30
    trusted_merchant:
      enabled: true
      max_trust_score: 80
    recurring:
      enabled: true
      merchant_threshold: 100
  frictionless:
    enabled: true
    risk_threshold: 80
```

### Fraud Detection Rules

```yaml
fraud_rules:
  velocity_checks:
    max_transactions_per_hour: 10
    max_amount_per_day: 10000
    max_failed_attempts: 5
    
  geo_velocity:
    max_distance_km: 500
    max_time_between_hours: 1
    
  device_fingerprint:
    enabled: true
    trusted_devices_count: 5
    new_device_threshold: 0.7
    
  ml_model:
    enabled: true
    model_path: "/models/fraud_detection_v2.pkl"
    threshold: 0.8
    features:
      - transaction_amount
      - merchant_category
      - time_of_day
      - device_type
      - location
```

## Architecture Patterns

### Payment State Machine

```python
class PaymentStateMachine:
    def __init__(self):
        self.states = {
            "created": ["authorizing", "failed"],
            "authorizing": ["authorized", "declined", "failed"],
            "authorized": ["capturing", "voided"],
            "capturing": ["captured", "capture_failed"],
            "captured": ["settling", "refunding"],
            "settling": ["settled", "settlement_failed"],
            "settled": ["refunding"],
            "refunding": ["refunded", "refund_failed"],
        }
    
    def transition(self, current_state: str, event: str) -> str:
        if current_state not in self.states:
            raise InvalidStateError(f"Invalid state: {current_state}")
        
        if event not in self.states[current_state]:
            raise InvalidTransitionError(
                f"Cannot transition from {current_state} via {event}"
            )
        
        return event
```

### Event Sourcing for Payments

```python
class PaymentEventStore:
    def __init__(self, db):
        self.db = db
    
    async def append_event(self, payment_id: str, event: PaymentEvent):
        await self.db.execute("""
            INSERT INTO payment_events (payment_id, event_type, payload, created_at)
            VALUES ($1, $2, $3, $4)
        """, payment_id, event.type, event.to_json(), datetime.utcnow())
    
    async def get_events(self, payment_id: str) -> List[PaymentEvent]:
        rows = await self.db.fetch("""
            SELECT event_type, payload, created_at
            FROM payment_events
            WHERE payment_id = $1
            ORDER BY created_at ASC
        """, payment_id)
        
        return [PaymentEvent.from_json(row) for row in rows]
    
    async def rebuild_state(self, payment_id: str) -> PaymentState:
        events = await self.get_events(payment_id)
        state = PaymentState()
        for event in events:
            state.apply(event)
        return state
```

### Idempotency Pattern

```python
class IdempotencyManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 86400  # 24 hours
    
    async def check_idempotency(self, key: str) -> Optional[Dict]:
        """Check if request was already processed"""
        cached = await self.redis.get(f"idempotency:{key}")
        if cached:
            return json.loads(cached)
        return None
    
    async def store_result(self, key: str, result: Dict):
        """Store result for idempotent retrieval"""
        await self.redis.setex(
            f"idempotency:{key}",
            self.ttl,
            json.dumps(result)
        )
```

### Circuit Breaker for Acquirers

```python
class AcquirerCircuitBreaker:
    def __init__(self, acquirer_name: str):
        self.acquirer = acquirer_name
        self.failure_count = 0
        self.failure_threshold = 5
        self.recovery_timeout = 30
        self.state = "closed"
        self.last_failure = None
    
    async def execute_with_protection(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure > self.recovery_timeout:
                self.state = "half_open"
            else:
                raise CircuitOpenError(f"Circuit open for {self.acquirer}")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "half_open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

## Integration Guide

### Stripe Integration

```python
import stripe
from fintech.payment_systems import PaymentGateway

class StripeGateway(PaymentGateway):
    def __init__(self, api_key: str):
        stripe.api_key = api_key
    
    async def authorize(self, payment_data: PaymentData) -> AuthorizationResult:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(payment_data.amount * 100),
                currency=payment_data.currency,
                payment_method=payment_data.payment_method_id,
                capture_method="manual",
                confirm=True,
                metadata=payment_data.metadata,
            )
            
            return AuthorizationResult(
                authorization_id=intent.id,
                status=self.map_status(intent.status),
                risk_score=self.calculate_risk_score(intent),
                requires_3ds=self.check_3ds_required(intent),
            )
        except stripe.error.CardError as e:
            return AuthorizationResult(
                status=PaymentStatus.DECLINED,
                error_code=e.code,
                error_message=str(e),
            )
```

### Adyen Integration

```python
from adyen import AdyenAPI

class AdyenGateway(PaymentGateway):
    def __init__(self, api_key: str, merchant_account: str):
        self.adyen = AdyenAPI(api_key)
        self.merchant_account = merchant_account
    
    async def authorize(self, payment_data: PaymentData) -> AuthorizationResult:
        request = {
            "merchantAccount": self.merchant_account,
            "amount": {
                "value": int(payment_data.amount * 100),
                "currency": payment_data.currency,
            },
            "reference": payment_data.reference,
            "paymentMethod": payment_data.payment_method,
            "returnUrl": payment_data.return_url,
        }
        
        response = self.adyen.payments(request)
        return self.map_response(response)
```

### Webhook Handling

```python
from fastapi import FastAPI, Request
import stripe

app = FastAPI()

@app.post("/webhooks/stripe")
async def handle_stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event["type"] == "payment_intent.succeeded":
        await handle_payment_success(event["data"]["object"])
    elif event["type"] == "payment_intent.payment_failed":
        await handle_payment_failure(event["data"]["object"])
    
    return {"status": "success"}
```

## Performance Optimization

### Connection Pooling

```python
import asyncpg
from contextlib import asynccontextmanager

class PaymentDatabasePool:
    def __init__(self):
        self.pool = None
    
    async def initialize(self, dsn: str, min_size: int = 10, max_size: int = 50):
        self.pool = await asyncpg.create_pool(
            dsn=dsn,
            min_size=min_size,
            max_size=max_size,
            max_inactive_connection_lifetime=300,
            command_timeout=30,
        )
    
    @asynccontextmanager
    async def acquire(self):
        async with self.pool.acquire() as conn:
            yield conn
```

### Caching Strategy

```python
import redis.asyncio as redis
from functools import wraps

class PaymentCache:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
    
    async def cache_payment(self, payment_id: str, payment_data: dict, ttl: int = 300):
        await self.redis.setex(
            f"payment:{payment_id}",
            ttl,
            json.dumps(payment_data)
        )
    
    async def get_payment(self, payment_id: str) -> Optional[dict]:
        data = await self.redis.get(f"payment:{payment_id}")
        if data:
            return json.loads(data)
        return None
    
    async def invalidate_payment(self, payment_id: str):
        await self.redis.delete(f"payment:{payment_id}")

def cache_result(ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = await payment_cache.get_payment(cache_key)
            if cached:
                return cached
            result = await func(*args, **kwargs)
            await payment_cache.cache_payment(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
```

### Batch Processing

```python
class PaymentBatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self.queue = asyncio.Queue()
    
    async def add_payment(self, payment: Payment):
        await self.queue.put(payment)
    
    async def process_batches(self):
        while True:
            batch = []
            for _ in range(self.batch_size):
                try:
                    payment = await asyncio.wait_for(
                        self.queue.get(), timeout=1.0
                    )
                    batch.append(payment)
                except asyncio.TimeoutError:
                    break
            
            if batch:
                await self.process_batch(batch)
    
    async def process_batch(self, batch: List[Payment]):
        async with db_pool.acquire() as conn:
            async with conn.transaction():
                for payment in batch:
                    await self.process_single_payment(conn, payment)
```

## Security Considerations

### PCI-DSS Compliance

```python
class PCIDSSCompliance:
    def __init__(self):
        self.encryption_key_id = "pci_key_2026"
    
    def encrypt_card_data(self, card_number: str) -> str:
        """Encrypt card data using AES-256-GCM"""
        from cryptography.fernet import Fernet
        
        key = self.get_encryption_key()
        f = Fernet(key)
        return f.encrypt(card_number.encode()).decode()
    
    def tokenize_card(self, card_number: str) -> str:
        """Replace card number with token"""
        token = f"tok_{uuid.uuid4().hex[:16]}"
        # Store mapping in secure vault
        self.store_token_mapping(token, card_number)
        return token
    
    def mask_card_number(self, card_number: str) -> str:
        """Mask card number for display"""
        return f"****-****-****-{card_number[-4:]}"
```

### Fraud Prevention

```python
class FraudPrevention:
    def __init__(self):
        self.velocity_checker = VelocityChecker()
        self.geo_checker = GeoVelocityChecker()
        self.device_checker = DeviceFingerprintChecker()
    
    async def screen_transaction(self, transaction: Transaction) -> RiskAssessment:
        checks = await asyncio.gather(
            self.velocity_checker.check(transaction),
            self.geo_checker.check(transaction),
            self.device_checker.check(transaction),
        )
        
        risk_score = self.calculate_composite_score(checks)
        
        return RiskAssessment(
            score=risk_score,
            action=self.determine_action(risk_score),
            flags=self.collect_flags(checks),
        )
```

### Secure Key Management

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class KeyManager:
    def __init__(self, master_key: str):
        self.master_key = master_key
    
    def derive_key(self, purpose: str, length: int = 32) -> bytes:
        """Derive purpose-specific key from master key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=purpose.encode(),
            iterations=100000,
        )
        return kdf.derive(self.master_key.encode())
```

## Troubleshooting Guide

### Common Issues

**Issue: Payment authorization failures**
```bash
# Check acquirer connectivity
curl -I https://api.stripe.com/v1/health

# Verify API keys
stripe api_keys list

# Check webhook logs
tail -f /var/log/payment-webhooks.log | grep -i error
```

**Issue: 3DS authentication timeouts**
```python
# Increase timeout for 3DS
three_ds_config = {
    "timeout_seconds": 45,
    "max_retries": 2,
    "retry_delay_seconds": 5,
}

# Monitor 3DS completion rates
metrics.gauge("3ds_completion_rate", 
    successful_3ds / total_3ds_attempts * 100)
```

**Issue: Settlement reconciliation mismatches**
```python
async def diagnose_settlement_mismatch(date: str):
    settlements = await get_settlements(date)
    ledger_entries = await get_ledger_entries(date)
    
    for settlement in settlements:
        matching_ledger = find_matching_entry(settlement, ledger_entries)
        if not matching_ledger:
            print(f"Missing ledger entry for: {settlement.id}")
        elif settlement.amount != matching_ledger.amount:
            print(f"Amount mismatch: {settlement.id}")
            print(f"  Settlement: {settlement.amount}")
            print(f"  Ledger: {matching_ledger.amount}")
```

### Performance Diagnostics

```python
class PaymentDiagnostics:
    async def analyze_transaction(self, transaction_id: str):
        trace = await self.get_transaction_trace(transaction_id)
        
        print(f"Transaction {transaction_id}:")
        print(f"  Total time: {trace.total_duration_ms}ms")
        print(f"  Breakdown:")
        for step in trace.steps:
            print(f"    {step.name}: {step.duration_ms}ms")
            if step.duration_ms > 100:
                print(f"      WARNING: Step exceeds 100ms threshold")
                print(f"      Details: {step.details}")
```

## API Reference

### Payment API Endpoints

```python
# Payment processing endpoints
POST /api/v1/payments/authorize
POST /api/v1/payments/capture
POST /api/v1/payments/void
POST /api/v1/payments/refund

# Token management endpoints
POST /api/v1/tokens
GET /api/v1/tokens/{token_id}
DELETE /api/v1/tokens/{token_id}

# Subscription endpoints
POST /api/v1/subscriptions
GET /api/v1/subscriptions/{subscription_id}
PATCH /api/v1/subscriptions/{subscription_id}
DELETE /api/v1/subscriptions/{subscription_id}

# Reconciliation endpoints
POST /api/v1/reconciliation/run
GET /api/v1/reconciliation/{reconciliation_id}
```

### Request/Response Schemas

```python
# Authorization request
class AuthorizationRequest:
    amount: Decimal
    currency: str
    payment_method_id: str
    merchant_id: str
    metadata: Optional[Dict[str, Any]] = None
    idempotency_key: str
    three_ds: bool = True

# Authorization response
class AuthorizationResponse:
    authorization_id: str
    status: PaymentStatus
    risk_score: float
    requires_3ds: bool
    three_ds_url: Optional[str]
    acquirer_reference: Optional[str]
```

## Data Models

### Payment Model

```python
class Payment:
    payment_id: UUID
    merchant_id: UUID
    amount: Decimal
    currency: str
    status: PaymentStatus
    payment_method: PaymentMethod
    authorization_id: Optional[str]
    capture_id: Optional[str]
    refund_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    
    # Fraud screening
    risk_score: Optional[float]
    risk_flags: List[str]
    
    # 3DS data
    three_ds_authenticated: bool
    three_ds_version: Optional[str]
```

### Transaction Model

```python
class Transaction:
    transaction_id: UUID
    payment_id: UUID
    type: TransactionType  # authorization, capture, refund, void
    amount: Decimal
    currency: str
    status: TransactionStatus
    acquirer: str
    acquirer_reference: str
    created_at: datetime
    processed_at: Optional[datetime]
    
    # Fee breakdown
    interchange_fee: Decimal
    acquirer_fee: Decimal
    network_fee: Decimal
    total_fee: Decimal
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: payments-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
    spec:
      containers:
      - name: payment
        image: your-registry/payment-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Payment metrics
payment_counter = Counter(
    'payments_total',
    'Total payments processed',
    ['status', 'currency', 'acquirer']
)

payment_duration = Histogram(
    'payment_duration_seconds',
    'Payment processing duration',
    ['operation'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

# Fraud metrics
fraud_score_histogram = Histogram(
    'fraud_score_distribution',
    'Distribution of fraud scores',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# 3DS metrics
three_ds_success_counter = Counter(
    'three_ds_success_total',
    '3DS authentication successes'
)

three_ds_failure_counter = Counter(
    'three_ds_failure_total',
    '3DS authentication failures'
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Payment Processing",
    "panels": [
      {
        "title": "Payment Throughput",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(payments_total[5m])",
            "legendFormat": "{{status}} - {{currency}}"
          }
        ]
      },
      {
        "title": "Payment Latency",
        "type": "heatmap",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(payment_duration_seconds_bucket[5m]))",
            "legendFormat": "P95"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: payment_alerts
  rules:
  - alert: HighPaymentDeclineRate
    expr: rate(payments_total{status="declined"}[5m]) / rate(payments_total[5m]) > 0.1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Payment decline rate exceeds 10%"
      
  - alert: PaymentProcessingLatency
    expr: histogram_quantile(0.95, rate(payment_duration_seconds_bucket[5m])) > 2
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Payment processing latency exceeds 2 seconds"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestPaymentProcessing:
    def test_authorize_payment(self, payment_processor):
        auth = payment_processor.authorize(
            amount=Decimal("100.00"),
            currency="USD",
            payment_method_id="pm_test_visa",
            merchant_id="MERCHANT-001",
        )
        assert auth.status == PaymentStatus.AUTHORIZED
        assert auth.authorization_id is not None
    
    def test_capture_payment(self, payment_processor):
        auth = payment_processor.authorize(
            amount=Decimal("100.00"),
            currency="USD",
            payment_method_id="pm_test_visa",
            merchant_id="MERCHANT-001",
        )
        
        capture = payment_processor.capture(
            authorization_id=auth.authorization_id,
            amount=Decimal("100.00"),
        )
        assert capture.status == PaymentStatus.CAPTURED
    
    def test_declined_payment(self, payment_processor):
        auth = payment_processor.authorize(
            amount=Decimal("100.00"),
            currency="USD",
            payment_method_id="pm_test_decline",
            merchant_id="MERCHANT-001",
        )
        assert auth.status == PaymentStatus.DECLINED
```

### Integration Tests

```python
class TestEndToEndPayment:
    async def test_full_payment_flow(self, payment_gateway):
        # Authorize
        auth = await payment_gateway.authorize(
            amount=Decimal("50.00"),
            currency="USD",
            payment_method_id="pm_test_visa",
            merchant_id="MERCHANT-001",
        )
        assert auth.status == PaymentStatus.AUTHORIZED
        
        # Capture
        capture = await payment_gateway.capture(
            authorization_id=auth.authorization_id,
            amount=Decimal("50.00"),
        )
        assert capture.status == PaymentStatus.CAPTURED
        
        # Refund
        refund = await payment_gateway.refund(
            capture_id=capture.capture_id,
            amount=Decimal("25.00"),
        )
        assert refund.status == PaymentStatus.REFUNDED
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class PaymentUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def authorize_payment(self):
        self.client.post("/api/v1/payments/authorize", json={
            "amount": "100.00",
            "currency": "USD",
            "payment_method_id": "pm_test_visa",
            "merchant_id": "MERCHANT-001",
        })
    
    @task(1)
    def capture_payment(self):
        self.client.post(f"/api/v1/payments/{self.payment_id}/capture")
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/payments", methods=["POST"])
@app.route("/api/v2/payments", methods=["POST"])
async def process_payment():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await process_payment_v2()
    return await process_payment_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **3DS**: 3D Secure - authentication protocol for online card payments
- **Acquirer**: Financial institution that processes credit/debit card payments
- **Authorization**: Approval of a transaction by the card issuer
- **Capture**: Process of collecting funds from an authorized transaction
- **Chargeback**: Dispute initiated by cardholder against a merchant
- **Interchange Fee**: Fee paid between banks for the acceptance of card-based transactions
- **Merchant**: Business that accepts card payments
- **PCI-DSS**: Payment Card Industry Data Security Standard
- **Settlement**: Process of transferring funds between acquirer and issuer
- **Tokenization**: Replacement of sensitive card data with non-sensitive tokens

## Changelog

### Version 2.0.0 (2026-07-01)
- Added multi-acquirer orchestration
- Implemented network tokenization
- Enhanced fraud detection with ML
- Added 3DS2 support

### Version 1.5.0 (2026-01-15)
- Added subscription billing
- Implemented payment reconciliation
- Enhanced dispute management

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic card processing
- Tokenization service

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def process_payment(
    amount: Decimal,
    currency: str,
    payment_method_id: str,
) -> Payment:
    """Process a payment transaction.
    
    Args:
        amount: Payment amount.
        currency: ISO currency code.
        payment_method_id: Tokenized payment method.
    
    Returns:
        The processed payment.
    
    Raises:
        PaymentError: If payment processing fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Payment Systems Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
