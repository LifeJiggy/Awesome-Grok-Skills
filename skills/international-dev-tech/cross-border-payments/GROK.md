---
name: "cross-border-payments"
category: "international-dev-tech"
version: "2.0.0"
tags: ["payments", "cross-border", "fintech", "currency", "compliance"]
description: "Cross-border payment processing with multi-currency and regulatory compliance"
---

# Cross-Border Payments

## Overview

The Cross-Border Payments module handles international payment processing, currency conversion, settlement, and compliance with cross-border financial regulations. It supports multiple payment methods (cards, bank transfers, digital wallets), real-time FX rates, regulatory screening, and multi-currency settlement with reconciliation.

## Core Capabilities

- **Multi-Currency Processing**: Support for 150+ currencies with real-time FX rates
- **Payment Methods**: Cards, SWIFT, SEPA, local payment methods (iDEAL, Boleto, etc.)
- **FX Rate Management**: Real-time and locked-in exchange rates with spread management
- **Regulatory Screening**: Sanctions screening, AML checks, and compliance validation
- **Settlement**: Multi-currency settlement with netting and reconciliation
- **Fee Calculation**: Configurable fee structures by corridor, method, and volume
- **Fraud Prevention**: Cross-border fraud detection and risk scoring
- **Reporting**: Transaction reporting for regulatory and reconciliation purposes

## Usage Examples

### Payment Processing

```python
from cross_border_payments import PaymentProcessor, PaymentRequest

processor = PaymentProcessor(
    merchant_id="MERCHANT-001",
    supported_currencies=["USD", "EUR", "GBP", "JPY"],
)

# Process cross-border payment
payment = PaymentRequest(
    amount=1500.00,
    source_currency="USD",
    destination_currency="EUR",
    source_country="US",
    destination_country="DE",
    payment_method="card",
    card_number="4111111111111111",
    recipient={"name": "Hans Mueller", "iban": "DE89370400440532013000"},
)

result = processor.process_payment(payment)
print(f"Payment Result:")
print(f"  Transaction ID: {result.transaction_id}")
print(f"  Status: {result.status}")
print(f"  Source Amount: {result.source_amount} {result.source_currency}")
print(f"  Destination Amount: {result.destination_amount} {result.destination_currency}")
print(f"  Exchange Rate: {result.exchange_rate}")
print(f"  Fees: {result.total_fees} {result.source_currency}")
```

### FX Rate Management

```python
from cross_border_payments import FXRateManager, RateQuote

fx_manager = FXRateManager(
    markup_pips=50,  # 5 pip markup
    spread_percentage=0.5,
)

# Get rate quote
quote = fx_manager.get_quote(
    source_currency="USD",
    destination_currency="EUR",
    amount=10000.00,
)

print(f"FX Quote:")
print(f"  Rate: {quote.rate}")
print(f"  Markup: {quote.markup}")
print(f"  Valid Until: {quote.valid_until}")
print(f"  Source Amount: {quote.source_amount} {quote.source_currency}")
print(f"  Destination Amount: {quote.destination_amount} {quote.destination_currency}")
```

### Regulatory Screening

```python
from cross_border_payments import ComplianceScreening, ScreeningRequest

screener = ComplianceScreening()

# Screen transaction
screening = screener.screen_transaction(
    ScreeningRequest(
        transaction_id="TXN-001",
        source_name="John Smith",
        source_country="US",
        destination_name="Hans Mueller",
        destination_country="DE",
        amount=1500.00,
        currency="USD",
    )
)

print(f"Screening Result:")
print(f"  Status: {screening.status}")
print(f"  Sanctions Check: {screening.sanctions_result}")
print(f"  PEP Check: {screening.pep_result}")
print(f"  Risk Score: {screening.risk_score}")
print(f"  Flags: {screening.flags}")
```

### Fee Calculation

```python
from cross_border_payments import FeeCalculator

calculator = FeeCalculator(
    fee_rules=[
        {"corridor": "US-EU", "method": "card", "percentage": 2.9, "fixed": 0.30},
        {"corridor": "US-EU", "method": "bank_transfer", "percentage": 1.0, "fixed": 5.00},
        {"corridor": "US-APAC", "method": "card", "percentage": 3.2, "fixed": 0.30},
    ]
)

fees = calculator.calculate(
    source_country="US",
    destination_country="DE",
    payment_method="card",
    amount=1500.00,
)
print(f"Fees: ${fees:.2f}")
```

## Best Practices

- **Rate Transparency**: Always show customers the rate and fees before confirmation
- **Regulatory Compliance**: Comply with AML/KYC regulations in all jurisdictions
- **Settlement Speed**: Optimize settlement times for competitive advantage
- **FX Risk Management**: Hedge currency exposure for large volumes
- **Fraud Prevention**: Implement cross-border-specific fraud rules
- **Reconciliation**: Automate reconciliation for all currency pairs
- **PCI Compliance**: Maintain PCI DSS compliance for card processing
- **Local Payment Methods**: Support preferred local payment methods in each market

## Related Modules

- **global-compliance**: Regulatory compliance across jurisdictions
- **localization-systems**: Locale-specific payment page localization
- **fraud-detection**: Fraud prevention for cross-border transactions
