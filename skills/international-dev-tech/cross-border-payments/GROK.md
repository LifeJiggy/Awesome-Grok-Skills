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

---

## Advanced Configuration

### Multi-Currency Configuration

```python
currency_config = {
    "supported_currencies": ["USD", "EUR", "GBP", "JPY", "CNY", "INR", "BRL"],
    "default_currency": "USD",
    "decimal_precision": {"JPY": 0, "USD": 2, "EUR": 2},
    "currency_symbols": {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"},
    "auto_detect_currency": True,
}
```

### Payment Method Configuration

```python
payment_methods = {
    "cards": {
        "visa": {"enabled": True, "countries": "all"},
        "mastercard": {"enabled": True, "countries": "all"},
        "amex": {"enabled": True, "countries": ["US", "CA", "GB"]},
    },
    "bank_transfers": {
        "swift": {"enabled": True, "countries": "all"},
        "sepa": {"enabled": True, "countries": ["EU", "EEA"]},
        "ach": {"enabled": True, "countries": ["US"]},
    },
    "local_methods": {
        "ideal": {"enabled": True, "countries": ["NL"]},
        "boleto": {"enabled": True, "countries": ["BR"]},
        "alipay": {"enabled": True, "countries": ["CN"]},
    },
}
```

### FX Rate Configuration

```python
fx_config = {
    "rate_providers": ["xe", "oanda", "ecb"],
    "markup_pips": 50,
    "spread_percentage": 0.5,
    "rate_refresh_seconds": 30,
    "locked_rate_duration_seconds": 300,
    "fallback_rate_source": "ecb",
}
```

### Settlement Configuration

```python
settlement_config = {
    "settlement_currencies": ["USD", "EUR"],
    "netting_enabled": True,
    "netting_frequency": "daily",
    "settlement_cycle": "T+2",
    "instant_settlement_enabled": False,
    "reconciliation_tolerance": 0.01,
}
```

### Compliance Configuration

```python
compliance_config = {
    "sanctions_screening": {"provider": "dow_jones", "enabled": True},
    "aml_checks": {"enabled": True, "threshold": 10000},
    "kyb_required": True,
    "transaction_monitoring": {"enabled": True, "real_time": True},
    "regulatory_reporting": {"enabled": True, "frequency": "daily"},
}
```

## Architecture Patterns

### Payment Processing Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Payment    │────▶│  Compliance  │────▶│  FX         │
│  Intake     │     │  Screening   │     │  Conversion │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Auth   │           │  Settle   │         │  Reconcile│
                    │         │           │           │         │           │
                    └─────────┘           └───────────┘         └───────────┘
```

### Multi-Currency Settlement

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Transaction│────▶│  Currency    │────▶│  Netting    │
│  Pool       │     │  Aggregation │     │  Engine     │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  USD    │           │  EUR      │         │  Other    │
                    │  Net    │           │  Net      │         │  Currencies│
                    └─────────┘           └───────────┘         └───────────┘
```

### Fraud Detection Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Transaction│────▶│  Velocity    │────▶│  Risk       │
│  Request    │     │  Check       │     │  Scoring    │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Approve│           │  Review   │         │  Decline  │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### Payment Gateway Integration

```python
def process_payment_with_gateway(payment_request):
    gateway = payment_gateways[payment_request.method]
    result = gateway.charge(
        amount=payment_request.amount,
        currency=payment_request.currency,
        token=payment_request.token,
        metadata=payment_request.metadata,
    )
    return {"transaction_id": result.id, "status": result.status}
```

### Banking Integration

```python
def initiate_bank_transfer(transfer_details):
    bank = banking_providers[transfer_details.bank_code]
    result = bank.initiate_transfer(
        amount=transfer_details.amount,
        currency=transfer_details.currency,
        beneficiary_iban=transfer_details.iban,
        reference=transfer_details.reference,
    )
    return {"transfer_id": result.id, "status": result.status}
```

### Compliance System Integration

```python
def screen_transaction(transaction):
    sanctions_result = sanctions_api.screen(
        name=transaction.beneficiary_name,
        country=transaction.beneficiary_country,
    )
    aml_result = aml_api.check(transaction)
    return {"sanctions": sanctions_result, "aml": aml_result}
```

### FX Provider Integration

```python
def get_fx_rate(source_currency, target_currency, amount):
    rate = fx_providers["primary"].get_rate(
        source=source_currency,
        target=target_currency,
        amount=amount,
    )
    return {"rate": rate.mid, "markup": rate.markup, "valid_until": rate.valid_until}
```

## Performance Optimization

### Transaction Processing Optimization

```python
processing_config = {
    "batch_size": 100,
    "parallel_workers": 8,
    "async_processing": True,
    "queue_enabled": True,
    "timeout_seconds": 30,
}
```

### Caching Strategy

```python
cache_config = {
    "fx_rates_ttl": 30,
    "currency_config_ttl": 3600,
    "payment_methods_ttl": 3600,
    "cache_backend": "redis",
}
```

### Database Optimization

```python
db_config = {
    "indexing": ["transaction_id", "status", "created_at"],
    "partitioning": "by_month",
    "connection_pool_size": 50,
    "read_replicas": 3,
    "query_timeout": 10,
}
```

### API Optimization

```python
api_config = {
    "response_timeout": 10,
    "retry_count": 3,
    "circuit_breaker": True,
    "rate_limiting": 1000,
    "connection_pool_size": 100,
}
```

## Security Considerations

### PCI DSS Compliance

```python
pci_config = {
    "level": "PCI DSS Level 1",
    "tokenization": True,
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "access_logging": True,
    "vulnerability_scanning": True,
}
```

### Fraud Prevention

```python
fraud_config = {
    "velocity_checks": {
        "max_transactions_per_hour": 10,
        "max_amount_per_day": 50000,
    },
    "risk_scoring": {"enabled": True, "threshold": 0.8},
    "3d_secure": {"enabled": True, "threshold": 100},
    "address_verification": True,
}
```

### Data Protection

```python
data_protection = {
    "pci_data_encrypted": True,
    "pii_masking": True,
    "data_masking_fields": ["card_number", "cvv", "account_number"],
    "access_logging": True,
    "audit_trail_retention": 2555,
}
```

### API Security

```python
api_security = {
    "api_key_required": True,
    "mutual_tls": True,
    "rate_limiting": 1000,
    "ip_whitelist": ["10.0.0.0/8"],
    "webhook_signature_verification": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Payment declined | Insufficient funds | Check balance |
| FX rate expired | Quote validity exceeded | Request new quote |
| Settlement delay | Banking hours | Check settlement cycle |
| Compliance block | Sanctions match | Manual review required |
| Reconciliation mismatch | Timing difference | Check transaction status |
| Card tokenization failed | Invalid card data | Verify card details |

### Debug Commands

```bash
# Check transaction status
payments-cli status --transaction-id TXN-001

# View FX rates
payments-cli fx-rates --source USD --target EUR

# Test compliance screening
payments-cli screen --name "John Smith" --country US

# Verify settlement
payments-cli settlement --date 2024-01-15
```

## API Reference

### PaymentProcessor

```python
class PaymentProcessor:
    def __init__(self, merchant_id: str, supported_currencies: List[str]):
        """Initialize payment processor."""

    def process_payment(self, request: PaymentRequest) -> PaymentResult:
        """Process cross-border payment."""

    def get_transaction(self, transaction_id: str) -> Transaction:
        """Get transaction details."""

    def refund_transaction(self, transaction_id: str, amount: float) -> RefundResult:
        """Process refund."""
```

### PaymentRequest

```python
@dataclass
class PaymentRequest:
    amount: float
    source_currency: str
    destination_currency: str
    source_country: str
    destination_country: str
    payment_method: str
    card_number: str = None
    recipient: Dict[str, Any] = None
```

### PaymentResult

```python
@dataclass
class PaymentResult:
    transaction_id: str
    status: str
    source_amount: float
    source_currency: str
    destination_amount: float
    destination_currency: str
    exchange_rate: float
    total_fees: float
```

### FXRateManager

```python
class FXRateManager:
    def __init__(self, markup_pips: int, spread_percentage: float):
        """Initialize FX rate manager."""

    def get_quote(self, source_currency: str, destination_currency: str, amount: float) -> RateQuote:
        """Get FX rate quote."""

    def lock_rate(self, quote_id: str) -> LockedRate:
        """Lock rate for transaction."""
```

### ComplianceScreening

```python
class ComplianceScreening:
    def __init__(self):
        """Initialize compliance screener."""

    def screen_transaction(self, request: ScreeningRequest) -> ScreeningResult:
        """Screen transaction for compliance."""

    def get_screening_history(self, transaction_id: str) -> List[ScreeningResult]:
        """Get screening history."""
```

## Data Models

### Transaction

```python
@dataclass
class Transaction:
    transaction_id: str
    status: str
    source_amount: float
    source_currency: str
    destination_amount: float
    destination_currency: str
    exchange_rate: float
    fees: List[Fee]
    created_at: datetime
    settled_at: datetime = None
```

### Fee

```python
@dataclass
class Fee:
    fee_type: str
    amount: float
    currency: str
    description: str
```

### RateQuote

```python
@dataclass
class RateQuote:
    quote_id: str
    rate: float
    markup: float
    source_amount: float
    destination_amount: float
    valid_until: datetime
```

### ScreeningResult

```python
@dataclass
class ScreeningResult:
    transaction_id: str
    status: str
    sanctions_result: str
    pep_result: str
    risk_score: float
    flags: List[str]
    screened_at: datetime
```

## Deployment Guide

### Initial Setup

```bash
# Initialize payment system
payments-cli init

# Configure payment providers
payments-cli configure --config config.yaml

# Test connectivity
payments-cli test-connectivity
```

### Production Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/payments-service.yaml

# Verify deployment
kubectl rollout status deployment/payments-service
```

## Monitoring & Observability

### Key Metrics

```python
metrics_config = {
    "transaction_count": "counter",
    "transaction_volume": "counter",
    "success_rate": "gauge",
    "average_processing_time": "histogram",
    "fx_rate_spread": "gauge",
    "settlement_delay": "histogram",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Cross-Border Payments Dashboard",
    "panels": [
        "transaction_volume",
        "success_rate",
        "fx_rate_trends",
        "settlement_status",
    ],
}
```

## Testing Strategy

### Unit Tests

```python
def test_payment_processing():
    processor = PaymentProcessor(merchant_id="test", supported_currencies=["USD", "EUR"])
    result = processor.process_payment(mock_payment)
    assert result.status in ["completed", "pending", "failed"]
```

### Integration Tests

```python
def test_full_payment_flow():
    payment = create_test_payment()
    result = processor.process_payment(payment)
    assert result.transaction_id is not None
    assert result.exchange_rate > 0
```

## Versioning & Migration

### API Versioning

```python
version_config = {
    "current_version": "v2",
    "supported_versions": ["v1", "v2"],
    "deprecation_policy": "6 months",
    "breaking_changes": "major",
}
```

## Glossary

| Term | Definition |
|------|------------|
| **FX** | Foreign Exchange |
| **SWIFT** | Society for Worldwide Interbank Financial Telecommunication |
| **SEPA** | Single Euro Payments Area |
| **AML** | Anti-Money Laundering |
| **KYC** | Know Your Customer |
| **KYB** | Know Your Business |
| **Settlement** | Final transfer of funds |
| **Netting** | Offsetting obligations to reduce transfers |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with multi-currency |
| 1.5.0 | 2024-11-01 | Added local payment methods |
| 1.4.0 | 2024-09-15 | Enhanced compliance screening |
| 1.3.0 | 2024-07-20 | Settlement improvements |
| 1.2.0 | 2024-05-10 | FX rate management |
| 1.1.0 | 2024-03-01 | Fraud prevention enhancements |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow PCI DSS requirements
2. Test with multiple currencies
3. Validate compliance rules
4. Document payment flows
5. Update FX rate logic

## License

MIT License. See LICENSE file for full terms.
