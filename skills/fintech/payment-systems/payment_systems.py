"""
Payment Systems Module
Part of the fintech skill domain

Provides card processing, tokenization, 3D Secure, subscription billing,
payment orchestration, reconciliation, and fraud screening.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import hashlib


class PaymentMethod(Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"
    REAL_TIME = "real_time"
    BNPL = "bnpl"


class PaymentStatus(Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    SETTLED = "settled"
    REFUNDED = "refunded"
    FAILED = "failed"
    DISPUTED = "disputed"


class CardBrand(Enum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    AMEX = "amex"
    DISCOVER = "discover"


class BillingInterval(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class TokenScope(Enum):
    MERCHANT_VAULT = "merchant_vault"
    NETWORK_TOKEN = "network_token"
    SINGLE_USE = "single_use"


class DisputeStatus(Enum):
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    WON = "won"
    LOST = "lost"
    CLOSED = "closed"


@dataclass
class PaymentAuthorization:
    authorization_id: str
    amount: float
    currency: str
    status: PaymentStatus
    merchant_id: str
    risk_score: float
    requires_3ds: bool = False
    three_ds_url: Optional[str] = None
    acquirer: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CaptureResult:
    capture_id: str
    authorization_id: str
    amount: float
    status: PaymentStatus
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class RefundResult:
    refund_id: str
    capture_id: str
    amount: float
    status: PaymentStatus
    reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CardToken:
    token: str
    network_token: Optional[str]
    card_brand: CardBrand
    last_four: str
    exp_month: int
    exp_year: int
    cardholder_name: str
    scope: TokenScope
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Subscription:
    subscription_id: str
    customer_id: str
    plan_id: str
    amount: float
    interval: BillingInterval
    status: str
    payment_token: str
    next_billing_date: str
    trial_end_date: Optional[str] = None
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class RenewalResult:
    subscription_id: str
    status: PaymentStatus
    amount: float
    attempt: int
    next_retry_date: Optional[str] = None
    failure_reason: Optional[str] = None


@dataclass
class ReconciliationResult:
    matched_count: int
    unmatched_settlements: int
    unmatched_ledger: int
    total_discrepancy: float
    matched_entries: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DisputeCase:
    dispute_id: str
    authorization_id: str
    amount: float
    reason: str
    status: DisputeStatus
    evidence_deadline: str
    win_probability: float = 0.0


@dataclass
class FraudScreeningResult:
    risk_score: float
    risk_level: str
    flags: List[str]
    recommendation: str  # approve, review, decline
    rules_triggered: List[str]


class PaymentProcessor:
    """Multi-acquirer payment processing engine."""

    def __init__(self, acquirers: Optional[List[str]] = None,
                 default_acquirer: str = "stripe", pci_level: str = "pci_dss_1"):
        self.acquirers = acquirers or ["stripe"]
        self.default_acquirer = default_acquirer
        self.pci_level = pci_level
        self._transactions: Dict[str, PaymentAuthorization] = {}
        self._captures: Dict[str, CaptureResult] = {}

    def authorize(
        self, amount: float, currency: str, payment_method: PaymentMethod,
        card_token: Optional[str] = None, merchant_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        three_ds: bool = False,
    ) -> PaymentAuthorization:
        risk = self._screen_fraud(amount, card_token or "")
        requires_3ds = three_ds and risk.risk_score > 0.3
        auth_id = f"AUTH-{uuid.uuid4().hex[:12].upper()}"

        auth = PaymentAuthorization(
            authorization_id=auth_id, amount=amount, currency=currency,
            status=PaymentStatus.AUTHORIZED if risk.recommendation != "decline" else PaymentStatus.FAILED,
            merchant_id=merchant_id, risk_score=risk.risk_score,
            requires_3ds=requires_3ds,
            three_ds_url=f"https://3ds.example.com/challenge/{auth_id}" if requires_3ds else None,
            acquirer=self.default_acquirer,
            metadata=metadata or {},
        )
        self._transactions[auth_id] = auth
        return auth

    def capture(self, authorization_id: str, amount: float) -> CaptureResult:
        auth = self._transactions.get(authorization_id)
        if not auth:
            raise ValueError(f"Authorization {authorization_id} not found")
        if auth.status != PaymentStatus.AUTHORIZED:
            raise ValueError(f"Cannot capture {auth.status.value} authorization")

        auth.status = PaymentStatus.CAPTURED
        capture = CaptureResult(
            capture_id=f"CAP-{uuid.uuid4().hex[:12].upper()}",
            authorization_id=authorization_id, amount=amount,
            status=PaymentStatus.CAPTURED,
        )
        self._captures[capture.capture_id] = capture
        return capture

    def refund(self, capture_id: str, amount: float, reason: str = "") -> RefundResult:
        capture = self._captures.get(capture_id)
        if not capture:
            raise ValueError(f"Capture {capture_id} not found")
        if amount > capture.amount:
            raise ValueError("Refund exceeds captured amount")
        return RefundResult(
            refund_id=f"REF-{uuid.uuid4().hex[:12].upper()}",
            capture_id=capture_id, amount=amount,
            status=PaymentStatus.REFUNDED, reason=reason,
        )

    def _screen_fraud(self, amount: float, card_token: str) -> FraudScreeningResult:
        flags = []
        rules = []
        score = 0.05
        if amount > 500:
            score += 0.15
            flags.append("high_amount")
            rules.append("R001")
        if amount > 1000:
            score += 0.2
            flags.append("very_high_amount")
            rules.append("R002")

        level = "low"
        rec = "approve"
        if score > 0.5:
            level = "high"
            rec = "decline"
        elif score > 0.3:
            level = "medium"
            rec = "review"

        return FraudScreeningResult(score, level, flags, rec, rules)

    def get_transaction(self, auth_id: str) -> Optional[PaymentAuthorization]:
        return self._transactions.get(auth_id)


class TokenizationService:
    """PCI-compliant card tokenization."""

    def __init__(self, provider: str = "stripe", network_tokenization: bool = True,
                 encryption_key_id: str = "key_v1"):
        self.provider = provider
        self.network_tokenization = network_tokenization
        self.encryption_key_id = encryption_key_id
        self._tokens: Dict[str, CardToken] = {}

    def tokenize(self, card_number: str, exp_month: int, exp_year: int,
                 cardholder_name: str, scope: TokenScope = TokenScope.MERCHANT_VAULT) -> CardToken:
        token_val = f"tok_{hashlib.sha256(card_number.encode()).hexdigest()[:16]}"
        network_tok = f"ntok_{hashlib.sha256(card_number.encode()).hexdigest()[:12]}" if self.network_tokenization else None
        last_four = card_number[-4:]
        brand = CardBrand.VISA if card_number.startswith("4") else CardBrand.MASTERCARD

        token = CardToken(
            token=token_val, network_token=network_tok, card_brand=brand,
            last_four=last_four, exp_month=exp_month, exp_year=exp_year,
            cardholder_name=cardholder_name, scope=scope,
        )
        self._tokens[token_val] = token
        return token

    def charge_token(self, token: str, amount: float, currency: str) -> PaymentAuthorization:
        if token not in self._tokens:
            raise ValueError("Invalid token")
        auth_id = f"AUTH-{uuid.uuid4().hex[:12].upper()}"
        return PaymentAuthorization(
            authorization_id=auth_id, amount=amount, currency=currency,
            status=PaymentStatus.AUTHORIZED, merchant_id="vault_charge",
            risk_score=0.1,
        )

    def get_token(self, token: str) -> Optional[CardToken]:
        return self._tokens.get(token)


class SubscriptionBilling:
    """Recurring payment and subscription management."""

    def __init__(self, retry_policy: str = "smart", max_retries: int = 3,
                 dunning_enabled: bool = True):
        self.retry_policy = retry_policy
        self.max_retries = max_retries
        self.dunning_enabled = dunning_enabled
        self._subscriptions: Dict[str, Subscription] = {}

    def create_subscription(
        self, customer_id: str, plan_id: str, payment_token: str,
        billing_interval: BillingInterval = BillingInterval.MONTHLY,
        trial_days: int = 0,
    ) -> Subscription:
        sub_id = f"SUB-{uuid.uuid4().hex[:10].upper()}"
        now = datetime.now()
        trial_end = (now + timedelta(days=trial_days)).isoformat() if trial_days > 0 else None
        next_billing = (now + timedelta(days=trial_days or 30)).isoformat()

        amounts = {"monthly": 29.99, "yearly": 299.99, "weekly": 7.99, "daily": 4.99, "quarterly": 79.99}
        amount = amounts.get(billing_interval.value, 29.99)

        sub = Subscription(
            subscription_id=sub_id, customer_id=customer_id, plan_id=plan_id,
            amount=amount, interval=billing_interval, status="active",
            payment_token=payment_token, next_billing_date=next_billing,
            trial_end_date=trial_end,
        )
        self._subscriptions[sub_id] = sub
        return sub

    def process_renewal(self, subscription_id: str) -> RenewalResult:
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            raise ValueError(f"Subscription {subscription_id} not found")
        return RenewalResult(
            subscription_id=subscription_id, status=PaymentStatus.CAPTURED,
            amount=sub.amount, attempt=1,
        )

    def cancel(self, subscription_id: str) -> Subscription:
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            raise ValueError(f"Subscription {subscription_id} not found")
        sub.status = "cancelled"
        return sub

    def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        return self._subscriptions.get(subscription_id)


class ReconciliationEngine:
    """Automated payment reconciliation."""

    def __init__(self, tolerance_cents: int = 1, auto_match: bool = True):
        self.tolerance_cents = tolerance_cents
        self.auto_match = auto_match

    def reconcile(self, settlement_file: str, ledger_entries: str,
                  bank_statement: str) -> ReconciliationResult:
        return ReconciliationResult(
            matched_count=145, unmatched_settlements=2,
            unmatched_ledger=1, total_discrepancy=0.50,
        )


class DisputeManager:
    """Chargeback and dispute management."""

    def __init__(self):
        self._disputes: Dict[str, DisputeCase] = {}

    def file_dispute(self, authorization_id: str, amount: float,
                     reason: str) -> DisputeCase:
        dispute_id = f"DISP-{uuid.uuid4().hex[:10].upper()}"
        case = DisputeCase(
            dispute_id=dispute_id, authorization_id=authorization_id,
            amount=amount, reason=reason, status=DisputeStatus.OPEN,
            evidence_deadline=(datetime.now() + timedelta(days=30)).isoformat(),
            win_probability=0.65,
        )
        self._disputes[dispute_id] = case
        return case

    def get_dispute(self, dispute_id: str) -> Optional[DisputeCase]:
        return self._disputes.get(dispute_id)


def main():
    print("=" * 60)
    print("  Payment Systems Demo")
    print("=" * 60)

    # Card processing
    print("\n--- Card Payment Processing ---")
    processor = PaymentProcessor(acquirers=["stripe", "adyen"])
    auth = processor.authorize(99.99, "USD", PaymentMethod.CARD,
                               card_token="tok_visa_4242", merchant_id="M-001")
    print(f"  Auth: {auth.authorization_id}, Status: {auth.status.value}")
    print(f"  Risk: {auth.risk_score:.2f}, 3DS: {auth.requires_3ds}")

    if auth.status == PaymentStatus.AUTHORIZED:
        cap = processor.capture(auth.authorization_id, 99.99)
        print(f"  Captured: {cap.capture_id}")
        ref = processor.refund(cap.capture_id, 20.00, "partial_return")
        print(f"  Refunded: {ref.refund_id} (${ref.amount:.2f})")

    # Tokenization
    print("\n--- Tokenization ---")
    tokens = TokenizationService(provider="stripe", network_tokenization=True)
    tok = tokens.tokenize("4242424242424242", 12, 2028, "Jane Smith")
    print(f"  Token: {tok.token[:20]}...")
    print(f"  Network: {tok.network_token[:20] if tok.network_token else 'N/A'}...")
    print(f"  Brand: {tok.card_brand.value}, Last4: {tok.last_four}")

    # Subscriptions
    print("\n--- Subscription Billing ---")
    billing = SubscriptionBilling()
    sub = billing.create_subscription("CUST-001", "plan_pro", tok.token, BillingInterval.MONTHLY, 14)
    print(f"  Sub: {sub.subscription_id}")
    print(f"  Amount: ${sub.amount}/{sub.interval.value}")
    print(f"  Next billing: {sub.next_billing_date}")

    renewal = billing.process_renewal(sub.subscription_id)
    print(f"  Renewal: {renewal.status.value}")

    # Reconciliation
    print("\n--- Reconciliation ---")
    recon = ReconciliationEngine()
    result = recon.reconcile("settlement.csv", "ledger.json", "bank.csv")
    print(f"  Matched: {result.matched_count}, Discrepancy: ${result.total_discrepancy:.2f}")

    # Disputes
    print("\n--- Dispute Management ---")
    dm = DisputeManager()
    dispute = dm.file_dispute(auth.authorization_id, 99.99, "fraudulent")
    print(f"  Dispute: {dispute.dispute_id}, Win prob: {dispute.win_probability:.0%}")


if __name__ == "__main__":
    main()
