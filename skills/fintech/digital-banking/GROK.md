---
name: "digital-banking"
category: "fintech"
version: "2.0.0"
tags: ["fintech", "digital-banking", "neobank", "core-banking", "open-banking"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["python", "banking-fundamentals", "api-design"]
---

# Digital Banking Platform

## Overview

Digital banking technology encompasses the full stack of software systems powering modern banking services: core banking ledgers, account management, payment processing, lending engines, KYC/AML compliance, and customer-facing mobile/web applications. This module provides a comprehensive framework for building and operating digital banking platforms—from neobank greenfield deployments to legacy core banking modernization via API-first architectures.

The system addresses the critical requirements of modern banking: real-time transaction processing with sub-second latency, event-sourced ledgers for audit compliance, Open Banking API standards (PSD2, FDX), embedded finance integration, multi-currency support, and regulatory reporting across jurisdictions. It covers both B2C retail banking and B2B banking-as-a-service (BaaS) platforms.

## Core Capabilities

- **Core Banking Ledger**: Double-entry bookkeeping with event sourcing, ACID transactions, and multi-currency support across checking, savings, and investment accounts
- **Account Lifecycle Management**: Customer onboarding, account opening, KYC verification, account maintenance, and closure workflows
- **Transaction Processing**: Real-time transaction authorization, settlement, reconciliation, and posting with fraud screening at each stage
- **Lending Engine**: Credit scoring, loan origination, disbursement, amortization scheduling, collections management, and credit line management
- **Open Banking APIs**: PSD2/FDX-compliant REST APIs for third-party provider integration, account aggregation, and payment initiation
- **KYC/AML Compliance**: Identity verification, document scanning, sanctions screening, PEP checks, and transaction monitoring for suspicious activity
- **Multi-Currency Support**: Real-time FX conversion, multi-currency wallets, correspondent banking routing, and SWIFT gpi integration
- **Card Management**: Virtual and physical card issuance, tokenization, real-time spend controls, and merchant category restrictions
- **Interest Calculation**: Configurable interest accrual for deposits and loans with compound interest, tiered rates, and promotional periods
- **Regulatory Reporting**: Automated generation of regulatory reports (CCAR, Basel III, local central bank requirements)

## Usage Examples

### Account Management

```python
from fintech.digital_banking import CoreBankingSystem, AccountType, Currency

bank = CoreBankingSystem(
    name="NeoBank Pro",
    supported_currencies=[Currency.USD, Currency.EUR, Currency.GBP],
    ledger_type="event_sourced",
)

# Open a new customer account
account = bank.create_account(
    customer_id="CUST-001",
    account_type=AccountType.CHECKING,
    currency=Currency.USD,
    initial_deposit=1000.00,
    overdraft_limit=500.00,
)

print(f"Account: {account.account_number}")
print(f"Balance: ${account.balance:.2f}")

# Process a deposit
bank.post_transaction(
    account_id=account.account_id,
    amount=2500.00,
    transaction_type="credit",
    description="Payroll deposit",
    reference="PAY-2026-07-01",
)

# Process a withdrawal
bank.post_transaction(
    account_id=account.account_id,
    amount=150.00,
    transaction_type="debit",
    description="ATM withdrawal",
    reference="ATM-4521",
)
```

### Lending & Loan Origination

```python
from fintech.digital_banking import LendingEngine, LoanProduct

lending = LendingEngine(
    scoring_model="gradient_boosting",
    auto_decision_threshold=0.7,
)

# Define loan product
product = lending.create_product(
    name="Personal Loan",
    min_amount=1000,
    max_amount=50000,
    term_months=[12, 24, 36, 48, 60],
    interest_rate_range=(5.99, 24.99),
    origination_fee_pct=0.01,
)

# Originate a loan
loan = lending.originate(
    customer_id="CUST-001",
    product_id=product.product_id,
    amount=15000,
    term_months=36,
    credit_score=720,
    annual_income=75000,
)

print(f"Loan: {loan.loan_id}")
print(f"Approved: {loan.approved}")
print(f"Interest rate: {loan.interest_rate:.2f}%")
print(f"Monthly payment: ${loan.monthly_payment:.2f}")
print(f"Total cost: ${loan.total_cost:.2f}")
```

### Open Banking API

```python
from fintech.digital_banking import OpenBankingAPI, ConsentType

api = OpenBankingAPI(
    version="v3.1",
    compliance_framework="PSD2",
)

# Register a third-party provider
tpd = api.register_tpp(
    name="FinAggregator Ltd",
    redirect_uris=["https://finagg.com/callback"],
    consent_types=[ConsentType.ACCOUNT_READ, ConsentType.PAYMENT_INIT],
)

# Create customer consent
consent = api.create_consent(
    tpp_id=tpd.tpp_id,
    customer_id="CUST-001",
    scope=["accounts", "transactions", "balances"],
    validity_days=90,
)

# Retrieve account data via Open Banking API
accounts = api.get_accounts(consent_id=consent.consent_id)
transactions = api.get_transactions(
    consent_id=consent.consent_id,
    account_id=accounts[0].account_id,
    from_date="2026-06-01",
    to_date="2026-06-30",
)
```

### KYC Verification

```python
from fintech.digital_banking import KYCService, DocumentType

kyc = KYCService(
    verification_providers=["jumio", "onfido"],
    sanctions_lists=["OFAC", "EU_SANCTIONS", "UN"],
)

# Run KYC check
result = kyc.verify(
    customer_id="CUST-001",
    documents=[
        {"type": DocumentType.PASSPORT, "file": "passport_scan.jpg"},
        {"type": DocumentType.PROOF_OF_ADDRESS, "file": "utility_bill.pdf"},
    ],
    liveness_check=True,
    address_verification=True,
)

print(f"KYC Status: {result.status}")
print(f"Risk Level: {result.risk_level}")
print(f"Checks: {result.checks_passed}/{result.checks_total}")
for flag in result.flags:
    print(f"  FLAG: {flag}")
```

## Architecture

```
Customer Channels
├── Mobile App (iOS/Android)
├── Web Application
├── Open Banking APIs (PSD2/FDX)
└── Banking-as-a-Service APIs
         │
         ▼
┌─────────────────────┐
│  API Gateway         │──→ Rate limiting, auth, routing
│  (Kong / AWS GW)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Core Banking        │──→ Account mgmt, transactions, ledger
│  (Event-Sourced)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Services Layer      │──→ Lending, cards, FX, compliance
│  (Microservices)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Ledger Store        │──→ PostgreSQL + event store
│  (Immutable Log)     │
└─────────────────────┘
```

## Best Practices

- Use event sourcing for the core ledger to ensure complete audit trails and enable point-in-time reconstruction
- Implement idempotency keys on all payment endpoints to prevent duplicate transactions from network retries
- Design for real-time authorization (sub-100ms) with async settlement to decouple customer experience from back-office processing
- Apply defense-in-depth for fraud: screen at account opening, transaction authorization, and post-authorization monitoring
- Maintain separate read and write models (CQRS) for the ledger to scale query patterns independently from transaction throughput
- Store sensitive data (PAN, SSN) using format-preserving encryption with HSM-backed key management
- Test interest calculations against known amortization schedules to prevent rounding errors at scale
- Implement circuit breakers on external integrations (FX feeds, sanctions lists) to prevent cascade failures
- Keep regulatory reporting logic isolated from business logic to simplify audit and compliance changes
- Log all state transitions in the account lifecycle with immutable audit entries for regulatory examination readiness

## Related Modules

- `fintech/payment-systems` - Payment rails and processing infrastructure
- `fintech/risk-engine` - Credit scoring and fraud detection models
- `fintech/compliance-automation` - Automated KYC/AML and regulatory reporting
- `fintech/blockchain-finance` - DLT-based settlement and tokenized assets

## Advanced Configuration

### Ledger Configuration

```yaml
ledger:
  type: "event_sourced"
  storage:
    engine: "postgresql"
    host: "ledger-db.internal"
    port: 5432
    database: "banking_ledger"
    pool_size: 50
    connection_timeout_ms: 5000
  event_store:
    stream_prefix: "account-"
    snapshot_interval: 1000
    retention_days: 2555  # 7 years regulatory requirement
  partitioning:
    strategy: "account_hash"
    partitions: 64
    rebalance_interval_hours: 24
```

### Multi-Region Deployment

```yaml
deployment:
  primary_region: "us-east-1"
  disaster_recovery:
    enabled: true
    regions: ["us-west-2", "eu-west-1"]
    rpo_seconds: 30  # Recovery Point Objective
    rto_seconds: 300  # Recovery Time Objective
    replication:
      mode: "synchronous_within_region"
      cross_region: "asynchronous"
  load_balancing:
    algorithm: "least_connections"
    health_check_interval_seconds: 10
    circuit_breaker:
      failure_threshold: 5
      recovery_timeout_seconds: 30
```

### Security Configuration

```yaml
security:
  encryption:
    at_rest:
      algorithm: "AES-256-GCM"
      key_management: "aws_kms"
      rotation_days: 90
    in_transit:
      tls_version: "1.3"
      cipher_suites: ["TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"]
  authentication:
    mfa_required: true
    session_timeout_minutes: 15
    max_failed_attempts: 5
    lockout_duration_minutes: 30
  audit:
    enabled: true
    retention_years: 7
    tamper_evident: true
    hash_algorithm: "SHA-256"
```

## Architecture Patterns

### Event Sourcing Pattern

The core ledger implements event sourcing where every state change is captured as an immutable event:

```python
class EventSourcedAccount:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = Decimal('0.00')
        self.events = []
    
    def apply_event(self, event: AccountEvent):
        if event.type == EventType.CREDIT:
            self.balance += event.amount
        elif event.type == EventType.DEBIT:
            if self.balance < event.amount:
                raise InsufficientFundsError()
            self.balance -= event.amount
        
        event.sequence_number = len(self.events) + 1
        event.timestamp = datetime.utcnow()
        self.events.append(event)
    
    def get_state_at(self, timestamp: datetime) -> 'AccountState':
        """Reconstruct account state at any point in time"""
        state = AccountState()
        for event in self.events:
            if event.timestamp <= timestamp:
                state.apply(event)
        return state
```

### CQRS Implementation

Separate read and write models for optimal performance:

```python
# Write Model - Optimized for transaction throughput
class LedgerWriteModel:
    async def post_transaction(self, transaction: Transaction):
        async with self.db.transaction():
            # Write to event store
            await self.event_store.append(
                stream=f"account-{transaction.account_id}",
                events=[transaction.to_event()]
            )
            # Update projection asynchronously
            await self.projection_writer.schedule_update(
                account_id=transaction.account_id
            )

# Read Model - Optimized for query performance
class LedgerReadModel:
    async def get_account_summary(self, account_id: str) -> AccountSummary:
        return await self.read_db.execute("""
            SELECT account_id, balance, currency, last_activity
            FROM account_summaries
            WHERE account_id = $1
        """, account_id)
```

### Saga Pattern for Complex Transactions

Coordinate multi-step operations with compensating transactions:

```python
class TransferSaga:
    def __init__(self, source_account: str, target_account: str, amount: Decimal):
        self.steps = [
            SagaStep("debit_source", self.debit_source, self.compensate_debit),
            SagaStep("credit_target", self.credit_target, self.compensate_credit),
            SagaStep("notify_parties", self.notify_parties, None),
        ]
    
    async def execute(self):
        completed_steps = []
        try:
            for step in self.steps:
                await step.execute()
                completed_steps.append(step)
        except Exception as e:
            # Compensate in reverse order
            for step in reversed(completed_steps):
                if step.compensate:
                    await step.compensate()
            raise SagaFailedError(f"Transfer failed: {e}")
```

### Circuit Breaker Pattern

Protect against cascade failures in external integrations:

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "closed"
        self.last_failure_time = None
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half_open"
            else:
                raise CircuitOpenError("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "half_open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

## Integration Guide

### Core Banking System Integration

```python
# Initialize the core banking system
from fintech.digital_banking import CoreBankingSystem, IntegrationConfig

config = IntegrationConfig(
    ledger_endpoint="https://ledger.internal:8443",
    auth_endpoint="https://auth.internal:8443",
    compliance_endpoint="https://compliance.internal:8443",
    timeout_seconds=30,
    retry_attempts=3,
    circuit_breaker_enabled=True,
)

bank = CoreBankingSystem(config=config)

# Register webhook for real-time events
bank.register_webhook(
    url="https://your-app.com/webhooks/banking",
    events=["transaction.completed", "account.updated", "compliance.alert"],
    secret="webhook_secret_key",
    retry_policy={"max_attempts": 5, "backoff_seconds": [1, 2, 4, 8, 16]},
)
```

### Open Banking PSD2 Integration

```python
from fintech.digital_banking import PSD2Compliance, ASPSPConnector

# Configure with your ASPSP (Account Servicing Payment Service Provider)
aspsp = ASPSPConnector(
    bank_id="your-bank-id",
    api_version="v3.1",
    transport_cert_path="/path/to/transport.pem",
    signing_key_path="/path/to/signing.key",
    sandbox_mode=False,
)

# Implement consent management
consent_manager = PSD2Compliance(
    aspsp=aspsp,
    max_consents_per_tpp=1000,
    consent_expiry_days=90,
    require_reauth_for_sca=True,
)
```

### Payment Gateway Integration

```python
from fintech.digital_banking import PaymentGateway, PaymentMethod

gateway = PaymentGateway(
    supported_methods=[
        PaymentMethod.ACH,
        PaymentMethod.WIRE,
        PaymentMethod.SEPA,
        PaymentMethod.FASTER_PAYMENTS,
    ],
    settlement_currency="USD",
    reconciliation_schedule="daily",
)

# Process a payment
payment = await gateway.process_payment(
    source_account="ACC-001",
    destination_account="EXT-002",
    amount=Decimal("1500.00"),
    currency="USD",
    payment_method=PaymentMethod.WIRE,
    reference="INV-2026-07-001",
    idempotency_key="unique-payment-id-123",
)
```

## Performance Optimization

### Database Optimization

```sql
-- Partition tables by date range for efficient queries
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    account_id UUID NOT NULL,
    amount DECIMAL(19,4) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

-- Create partitions for each month
CREATE TABLE transactions_2026_07 PARTITION OF transactions
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

-- Optimize common queries with covering indexes
CREATE INDEX idx_transactions_account_date 
ON transactions (account_id, created_at DESC) 
INCLUDE (amount, currency, type);
```

### Caching Strategy

```python
class AccountCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_balance(self, account_id: str) -> Optional[Decimal]:
        cache_key = f"balance:{account_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return Decimal(cached)
        
        # Cache miss - fetch from database
        balance = await self.fetch_from_db(account_id)
        await self.redis.setex(cache_key, self.default_ttl, str(balance))
        return balance
    
    async def invalidate(self, account_id: str):
        """Invalidate cache on transaction"""
        await self.redis.delete(f"balance:{account_id}")
```

### Connection Pool Tuning

```python
# Optimal connection pool configuration
pool_config = {
    "min_size": 10,
    "max_size": 100,
    "max_inactive_connection_lifetime": 300,
    "command_timeout": 30,
    "statement_cache_size": 1000,
    "enable_hierarchical_subscriptions": True,
}

# Monitor pool utilization
async def monitor_pool(pool):
    while True:
        stats = pool.get_stats()
        metrics.gauge("db_pool_active", stats.active_connections)
        metrics.gauge("db_pool_idle", stats.idle_connections)
        metrics.gauge("db_pool_waiting", stats.waiting_requests)
        await asyncio.sleep(10)
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class DataEncryption:
    def __init__(self, master_key: bytes):
        self.master_key = master_key
    
    def encrypt_sensitive_field(self, data: str, context: str) -> str:
        """Encrypt sensitive data with context-aware key derivation"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=context.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        f = Fernet(key)
        return f.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_field(self, encrypted: str, context: str) -> str:
        """Decrypt sensitive data"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=context.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        f = Fernet(key)
        return f.decrypt(encrypted.encode()).decode()
```

### Fraud Detection Integration

```python
class FraudDetection:
    def __init__(self, risk_engine):
        self.risk_engine = risk_engine
        self.rules = self.load_fraud_rules()
    
    async def screen_transaction(self, transaction: Transaction) -> RiskAssessment:
        # Run through rule engine
        rule_results = await self.evaluate_rules(transaction)
        
        # ML-based scoring
        ml_score = await self.risk_engine.score_transaction({
            "amount": float(transaction.amount),
            "merchant_category": transaction.mcc,
            "time_of_day": transaction.timestamp.hour,
            "location": transaction.location,
            "velocity": await self.get_velocity(transaction.account_id),
        })
        
        # Combine scores
        combined_score = self.combine_scores(rule_results, ml_score)
        
        return RiskAssessment(
            score=combined_score,
            action=self.determine_action(combined_score),
            flags=rule_results.flags,
            ml_features=ml_score.feature_importance,
        )
```

### Audit Trail

```python
class AuditLogger:
    def __init__(self, immutable_store):
        self.store = immutable_store
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "actor": event.actor,
            "action": event.action,
            "resource": event.resource,
            "details": event.details,
            "ip_address": event.ip_address,
            "user_agent": event.user_agent,
            "previous_hash": await self.get_previous_hash(),
        }
        
        # Create tamper-evident hash
        audit_entry["hash"] = self.compute_hash(audit_entry)
        
        # Store in append-only log
        await self.store.append(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: Transaction latency spikes**
```bash
# Check connection pool utilization
curl -s http://localhost:9090/metrics | grep db_pool

# Monitor slow queries
psql -c "SELECT * FROM pg_stat_activity WHERE state = 'active' AND query_start < now() - interval '1 second';"
```

**Issue: Event store lag**
```bash
# Check event store consumer lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group ledger-consumer

# Monitor event processing rate
curl -s http://localhost:9090/metrics | grep event_processing_rate
```

**Issue: Reconciliation mismatches**
```python
# Run reconciliation diagnostic
async def diagnose_mismatch(account_id: str, date: str):
    ledger_balance = await get_ledger_balance(account_id, date)
    system_balance = await get_system_balance(account_id, date)
    
    if ledger_balance != system_balance:
        # Find divergent transactions
        transactions = await get_transactions(account_id, date)
        for tx in transactions:
            if not await is_posted_to_ledger(tx.id):
                print(f"Unposted transaction: {tx.id}")
```

### Performance Diagnostics

```python
class PerformanceDiagnostics:
    async def analyze_slow_transaction(self, transaction_id: str):
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

### Core Banking API

```python
class CoreBankingAPI:
    """REST API endpoints for core banking operations"""
    
    POST /api/v1/accounts
    GET /api/v1/accounts/{account_id}
    PATCH /api/v1/accounts/{account_id}
    DELETE /api/v1/accounts/{account_id}
    
    POST /api/v1/transactions
    GET /api/v1/transactions/{transaction_id}
    GET /api/v1/accounts/{account_id}/transactions
    
    POST /api/v1/transfers
    GET /api/v1/transfers/{transfer_id}
    
    POST /api/v1/payments
    GET /api/v1/payments/{payment_id}
```

### Request/Response Schemas

```python
# Account creation request
class CreateAccountRequest:
    customer_id: str
    account_type: AccountType
    currency: str
    initial_deposit: Optional[Decimal] = None
    overdraft_limit: Optional[Decimal] = None
    metadata: Optional[Dict[str, Any]] = None

# Account response
class AccountResponse:
    account_id: str
    account_number: str
    account_type: AccountType
    currency: str
    balance: Decimal
    available_balance: Decimal
    status: AccountStatus
    created_at: datetime
    updated_at: datetime
```

## Data Models

### Account Model

```python
class Account:
    account_id: UUID
    customer_id: UUID
    account_number: str  # Masked for display
    account_type: AccountType
    currency: str
    balance: Decimal
    available_balance: Decimal
    overdraft_limit: Decimal
    status: AccountStatus
    opened_at: datetime
    closed_at: Optional[datetime]
    metadata: Dict[str, Any]
    
    # Relationships
    customer: Customer
    transactions: List[Transaction]
    beneficiaries: List[Beneficiary]
```

### Transaction Model

```python
class Transaction:
    transaction_id: UUID
    account_id: UUID
    type: TransactionType
    amount: Decimal
    currency: str
    balance_after: Decimal
    description: str
    reference: str
    status: TransactionStatus
    created_at: datetime
    posted_at: Optional[datetime]
    settled_at: Optional[datetime]
    
    # Fraud screening results
    risk_score: Optional[float]
    risk_flags: List[str]
    
    # External references
    external_id: Optional[str]
    batch_id: Optional[str]
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: core-banking-service
  namespace: fintech-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: core-banking
  template:
    metadata:
      labels:
        app: core-banking
    spec:
      containers:
      - name: banking
        image: your-registry/core-banking:2.0.0
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

# Transaction metrics
transaction_counter = Counter(
    'banking_transactions_total',
    'Total transactions processed',
    ['type', 'currency', 'status']
)

transaction_duration = Histogram(
    'banking_transaction_duration_seconds',
    'Transaction processing duration',
    ['type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

# Account metrics
account_balance = Gauge(
    'banking_account_balance',
    'Current account balance',
    ['account_type', 'currency']
)

# System metrics
event_store_lag = Gauge(
    'banking_event_store_lag_seconds',
    'Event store consumer lag'
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Digital Banking Platform",
    "panels": [
      {
        "title": "Transaction Throughput",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(banking_transactions_total[5m])",
            "legendFormat": "{{type}} - {{currency}}"
          }
        ]
      },
      {
        "title": "Transaction Latency",
        "type": "heatmap",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(banking_transaction_duration_seconds_bucket[5m]))",
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
- name: banking_alerts
  rules:
  - alert: HighTransactionLatency
    expr: histogram_quantile(0.95, rate(banking_transaction_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Transaction latency exceeds 1 second"
      
  - alert: EventStoreLag
    expr: banking_event_store_lag_seconds > 60
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Event store lag exceeds 60 seconds"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestAccountOperations:
    def test_create_account(self, bank_system):
        account = bank_system.create_account(
            customer_id="CUST-001",
            account_type=AccountType.CHECKING,
            currency="USD",
        )
        assert account.balance == Decimal('0.00')
        assert account.status == AccountStatus.ACTIVE
    
    def test_credit_transaction(self, bank_system):
        account = bank_system.create_account(
            customer_id="CUST-001",
            account_type=AccountType.CHECKING,
            currency="USD",
        )
        
        bank_system.post_transaction(
            account_id=account.account_id,
            amount=Decimal('100.00'),
            transaction_type="credit",
        )
        
        updated = bank_system.get_account(account.account_id)
        assert updated.balance == Decimal('100.00')
    
    def test_insufficient_funds(self, bank_system):
        account = bank_system.create_account(
            customer_id="CUST-001",
            account_type=AccountType.CHECKING,
            currency="USD",
        )
        
        with pytest.raises(InsufficientFundsError):
            bank_system.post_transaction(
                account_id=account.account_id,
                amount=Decimal('100.00'),
                transaction_type="debit",
            )
```

### Integration Tests

```python
class TestPaymentIntegration:
    async def test_end_to_end_payment(self, payment_gateway):
        # Create test accounts
        source = await create_test_account(balance=1000)
        destination = await create_test_account(balance=0)
        
        # Process payment
        payment = await payment_gateway.process_payment(
            source_account=source.account_id,
            destination_account=destination.account_id,
            amount=Decimal("100.00"),
            currency="USD",
            idempotency_key="test-payment-001",
        )
        
        assert payment.status == PaymentStatus.COMPLETED
        
        # Verify balances
        source_updated = await get_account(source.account_id)
        destination_updated = await get_account(destination.account_id)
        
        assert source_updated.balance == Decimal("900.00")
        assert destination_updated.balance == Decimal("100.00")
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class BankingUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_balance(self):
        self.client.get(f"/api/v1/accounts/{self.account_id}/balance")
    
    @task(1)
    def transfer_money(self):
        self.client.post("/api/v1/transfers", json={
            "source_account": self.account_id,
            "destination_account": "DEST-001",
            "amount": "10.00",
            "currency": "USD",
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/accounts", methods=["GET"])
@app.route("/api/v2/accounts", methods=["GET"])
async def get_accounts():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await get_accounts_v2()
    return await get_accounts_v1()
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

- **ACID**: Atomicity, Consistency, Isolation, Durability - properties of database transactions
- **AML**: Anti-Money Laundering - regulations to prevent money laundering
- **ASPSP**: Account Servicing Payment Service Provider - bank that holds customer accounts
- **BaaS**: Banking as a Service - providing banking functionality via APIs
- **CQRS**: Command Query Responsibility Segregation - separating read/write models
- **FDX**: Financial Data Exchange - standard for sharing financial data
- **KYC**: Know Your Customer - verification of customer identity
- **PSD2**: Payment Services Directive 2 - EU regulation for payment services
- **SAGA**: Pattern for managing distributed transactions with compensation
- **TPP**: Third Party Provider - authorized to access bank data via APIs

## Changelog

### Version 2.0.0 (2026-07-01)
- Added multi-currency support with real-time FX
- Implemented event sourcing for core ledger
- Added Open Banking PSD2/FDX compliance
- Enhanced fraud detection with ML models

### Version 1.5.0 (2026-01-15)
- Added lending engine
- Implemented card management
- Enhanced KYC integration

### Version 1.0.0 (2025-06-01)
- Initial release
- Core banking ledger
- Account management
- Basic transaction processing

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def process_transaction(
    account_id: str,
    amount: Decimal,
    transaction_type: str,
) -> Transaction:
    """Process a banking transaction.
    
    Args:
        account_id: The account identifier.
        amount: Transaction amount.
        transaction_type: Type of transaction (credit/debit).
    
    Returns:
        The processed transaction.
    
    Raises:
        InsufficientFundsError: If debit exceeds available balance.
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

Copyright (c) 2026 Digital Banking Platform

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
