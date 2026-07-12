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
