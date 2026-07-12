"""
Cross-Border Payments Module
International payment processing with multi-currency support
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class PaymentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    ON_HOLD = "on_hold"

class PaymentMethod(Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    SWIFT = "swift"
    SEPA = "sepa"
    IDEAL = "ideal"
    BOLETO = "bolet to"
    ALIPAY = "alipay"
    WECHAT = "wechat"

class ScreeningStatus(Enum):
    CLEARED = "cleared"
    FLAGGED = "flagged"
    BLOCKED = "blocked"
    PENDING = "pending"

@dataclass
class PaymentRequest:
    amount: float = 0.0
    source_currency: str = "USD"
    destination_currency: str = "EUR"
    source_country: str = "US"
    destination_country: str = "DE"
    payment_method: str = "card"
    card_number: str = ""
    recipient: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaymentResult:
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    status: PaymentStatus = PaymentStatus.PENDING
    source_amount: float = 0.0
    source_currency: str = "USD"
    destination_amount: float = 0.0
    destination_currency: str = "EUR"
    exchange_rate: float = 1.0
    total_fees: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class FXQuote:
    source_currency: str = ""
    destination_currency: str = ""
    rate: float = 1.0
    markup: float = 0.0
    source_amount: float = 0.0
    destination_amount: float = 0.0
    valid_until: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=5))
    quote_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])

@dataclass
class ScreeningRequest:
    transaction_id: str = ""
    source_name: str = ""
    source_country: str = ""
    destination_name: str = ""
    destination_country: str = ""
    amount: float = 0.0
    currency: str = "USD"

@dataclass
class ScreeningResult:
    transaction_id: str = ""
    status: ScreeningStatus = ScreeningStatus.CLEARED
    sanctions_result: str = "clear"
    pep_result: str = "clear"
    risk_score: float = 0.1
    flags: List[str] = field(default_factory=list)
    screened_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class FeeRule:
    corridor: str = ""
    method: str = ""
    percentage: float = 0.0
    fixed: float = 0.0

class PaymentProcessor:
    def __init__(self, merchant_id: str = "", supported_currencies: Optional[List[str]] = None) -> None:
        self.merchant_id = merchant_id
        self.supported_currencies = supported_currencies or ["USD", "EUR", "GBP"]
        self._transactions: List[PaymentResult] = []
        self._fx_rates: Dict[str, float] = {"USD_EUR": 0.92, "USD_GBP": 0.79, "USD_JPY": 149.5, "EUR_GBP": 0.86}

    def process_payment(self, request: PaymentRequest) -> PaymentResult:
        rate = self._get_rate(request.source_currency, request.destination_currency)
        fees = self._calculate_fees(request.amount, request.payment_method)
        dest_amount = (request.amount - fees) * rate

        result = PaymentResult(
            status=PaymentStatus.COMPLETED,
            source_amount=request.amount,
            source_currency=request.source_currency,
            destination_amount=dest_amount,
            destination_currency=request.destination_currency,
            exchange_rate=rate,
            total_fees=fees,
        )
        self._transactions.append(result)
        return result

    def _get_rate(self, source: str, dest: str) -> float:
        key = f"{source}_{dest}"
        if key in self._fx_rates:
            return self._fx_rates[key]
        return 1.0

    def _calculate_fees(self, amount: float, method: str) -> float:
        if method == "card":
            return amount * 0.029 + 0.30
        return amount * 0.01 + 5.00

    def get_transactions(self) -> List[PaymentResult]:
        return self._transactions

class FXRateManager:
    def __init__(self, markup_pips: int = 50, spread_percentage: float = 0.5) -> None:
        self.markup_pips = markup_pips
        self.spread_percentage = spread_percentage
        self._base_rates: Dict[str, float] = {"USD_EUR": 0.92, "USD_GBP": 0.79, "EUR_GBP": 0.86, "USD_JPY": 149.5}

    def get_quote(self, source_currency: str, destination_currency: str, amount: float) -> FXQuote:
        key = f"{source_currency}_{destination_currency}"
        base_rate = self._base_rates.get(key, 1.0)
        markup = self.markup_pips / 10000
        adjusted_rate = base_rate * (1 + markup)
        dest_amount = amount * adjusted_rate

        return FXQuote(
            source_currency=source_currency,
            destination_currency=destination_currency,
            rate=adjusted_rate,
            markup=markup,
            source_amount=amount,
            destination_amount=dest_amount,
        )

class ComplianceScreening:
    def __init__(self) -> None:
        self._sanctioned_countries = {"KP", "IR", "SY", "CU"}

    def screen_transaction(self, request: ScreeningRequest) -> ScreeningResult:
        flags = []
        risk_score = 0.1

        if request.source_country in self._sanctioned_countries or request.destination_country in self._sanctioned_countries:
            return ScreeningResult(transaction_id=request.transaction_id, status=ScreeningStatus.BLOCKED, sanctions_result="match", risk_score=1.0, flags=["sanctioned_country"])

        if request.amount > 10000:
            flags.append("high_value")
            risk_score += 0.2

        if request.source_country != request.destination_country:
            flags.append("cross_border")
            risk_score += 0.1

        status = ScreeningStatus.FLAGGED if risk_score > 0.5 else ScreeningStatus.CLEARED
        return ScreeningResult(transaction_id=request.transaction_id, status=status, risk_score=min(1.0, risk_score), flags=flags)

class FeeCalculator:
    def __init__(self, fee_rules: Optional[List[Dict[str, Any]]] = None) -> None:
        self._rules = [FeeRule(corridor=r.get("corridor", ""), method=r.get("method", ""), percentage=r.get("percentage", 0), fixed=r.get("fixed", 0)) for r in (fee_rules or [])]

    def calculate(self, source_country: str, destination_country: str, payment_method: str, amount: float) -> float:
        corridor = f"{source_country}-{destination_country}"
        for rule in self._rules:
            if rule.corridor == corridor and rule.method == payment_method:
                return amount * (rule.percentage / 100) + rule.fixed
        return amount * 0.03 + 0.30

def main() -> None:
    print("=" * 60)
    print("  Cross-Border Payments Module — Demo")
    print("=" * 60)

    processor = PaymentProcessor(merchant_id="M-001", supported_currencies=["USD", "EUR", "GBP"])
    payment = PaymentRequest(amount=1500.00, source_currency="USD", destination_currency="EUR", source_country="US", destination_country="DE", recipient={"name": "Hans Mueller"})
    result = processor.process_payment(payment)
    print(f"\n[+] Payment: {result.transaction_id}")
    print(f"    Status: {result.status.value}")
    print(f"    Source: {result.source_amount} {result.source_currency}")
    print(f"    Destination: {result.destination_amount:.2f} {result.destination_currency}")
    print(f"    Rate: {result.exchange_rate}")
    print(f"    Fees: {result.total_fees:.2f}")

    fx = FXRateManager()
    quote = fx.get_quote("USD", "GBP", 10000)
    print(f"\n[+] FX Quote: 1 USD = {quote.rate:.4f} GBP")

    screener = ComplianceScreening()
    screening = screener.screen_transaction(ScreeningRequest(transaction_id="T-001", source_name="John", source_country="US", destination_name="Hans", destination_country="DE", amount=1500))
    print(f"\n[+] Screening: {screening.status.value} (risk: {screening.risk_score})")

    calc = FeeCalculator([{"corridor": "US-DE", "method": "card", "percentage": 2.9, "fixed": 0.30}])
    fees = calc.calculate("US", "DE", "card", 1500)
    print(f"\n[+] Fees: ${fees:.2f}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
