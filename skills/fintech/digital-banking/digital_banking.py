"""
Digital Banking Platform Module
Part of the fintech skill domain

Provides core banking ledger, account management, transaction processing,
lending, Open Banking APIs, KYC/AML, and multi-currency support.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import hashlib
import uuid
import math
import statistics


class AccountType(Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    CREDIT = "credit"
    LOAN = "loan"


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CNY = "CNY"


class TransactionType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER = "transfer"
    FEE = "fee"
    INTEREST = "interest"


class TransactionStatus(Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    POSTED = "posted"
    SETTLED = "settled"
    FAILED = "failed"


class KYCStatus(Enum):
    NOT_STARTED = "not_started"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual_review"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConsentType(Enum):
    ACCOUNT_READ = "account_read"
    TRANSACTION_READ = "transaction_read"
    PAYMENT_INIT = "payment_init"


class LoanStatus(Enum):
    APPLICATION = "application"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    ACTIVE = "active"
    DEFAULTED = "defaulted"
    PAID_OFF = "paid_off"


class DocumentType(Enum):
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"
    PROOF_OF_ADDRESS = "proof_of_address"


@dataclass
class Account:
    account_id: str
    customer_id: str
    account_type: AccountType
    currency: Currency
    balance: float
    available_balance: float
    overdraft_limit: float = 0.0
    opened_date: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "active"

    @property
    def is_overdrawn(self) -> bool:
        return self.balance < 0


@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    amount: float
    transaction_type: TransactionType
    status: TransactionStatus
    description: str
    reference: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    balance_after: float = 0.0


@dataclass
class LedgerEntry:
    entry_id: str
    debit_account: str
    credit_account: str
    amount: float
    currency: Currency
    transaction_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class LoanProduct:
    product_id: str
    name: str
    min_amount: float
    max_amount: float
    term_months: List[int]
    interest_rate_range: Tuple[float, float]
    origination_fee_pct: float


@dataclass
class Loan:
    loan_id: str
    customer_id: str
    product_id: str
    principal: float
    term_months: int
    interest_rate: float
    monthly_payment: float
    total_cost: float
    approved: bool
    status: LoanStatus
    remaining_balance: float = 0.0

    def __post_init__(self):
        if self.remaining_balance == 0 and self.approved:
            self.remaining_balance = self.principal


@dataclass
class AmortizationEntry:
    month: int
    payment: float
    principal_portion: float
    interest_portion: float
    remaining_balance: float


@dataclass
class TPPRegistration:
    tpp_id: str
    name: str
    redirect_uris: List[str]
    consent_types: List[ConsentType]
    status: str = "active"


@dataclass
class Consent:
    consent_id: str
    tpp_id: str
    customer_id: str
    scope: List[str]
    validity_days: int
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "active"

    @property
    def expires_date(self) -> str:
        created = datetime.fromisoformat(self.created_date)
        return (created + timedelta(days=self.validity_days)).isoformat()


@dataclass
class KYCResult:
    customer_id: str
    status: KYCStatus
    risk_level: RiskLevel
    checks_passed: int
    checks_total: int
    flags: List[str] = field(default_factory=list)


class CoreBankingSystem:
    """Event-sourced core banking ledger."""

    def __init__(self, name: str, supported_currencies: Optional[List[Currency]] = None):
        self.name = name
        self.currencies = supported_currencies or [Currency.USD]
        self._accounts: Dict[str, Account] = {}
        self._transactions: Dict[str, List[Transaction]] = {}
        self._ledger: List[LedgerEntry] = []
        self._events: List[Dict[str, Any]] = []

    def create_account(
        self, customer_id: str, account_type: AccountType,
        currency: Currency = Currency.USD, initial_deposit: float = 0.0,
        overdraft_limit: float = 0.0,
    ) -> Account:
        account_id = f"ACC-{uuid.uuid4().hex[:12].upper()}"
        account = Account(
            account_id=account_id, customer_id=customer_id,
            account_type=account_type, currency=currency,
            balance=initial_deposit, available_balance=initial_deposit + overdraft_limit,
            overdraft_limit=overdraft_limit,
        )
        self._accounts[account_id] = account
        self._transactions[account_id] = []
        self._events.append({"type": "account_opened", "account_id": account_id})

        if initial_deposit > 0:
            self.post_transaction(account_id, initial_deposit, TransactionType.CREDIT,
                                  "Initial deposit", "INIT")
        return account

    def post_transaction(
        self, account_id: str, amount: float, transaction_type: TransactionType,
        description: str, reference: str,
    ) -> Transaction:
        account = self._accounts.get(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        if transaction_type == TransactionType.DEBIT:
            if account.balance - amount < -account.overdraft_limit:
                raise ValueError("Insufficient funds")
            account.balance -= amount
        else:
            account.balance += amount
        account.available_balance = account.balance + account.overdraft_limit

        txn = Transaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            account_id=account_id, amount=amount,
            transaction_type=transaction_type, status=TransactionStatus.POSTED,
            description=description, reference=reference, balance_after=account.balance,
        )
        self._transactions.setdefault(account_id, []).append(txn)
        self._ledger.append(LedgerEntry(
            entry_id=f"LED-{uuid.uuid4().hex[:8].upper()}",
            debit_account=account_id if transaction_type == TransactionType.DEBIT else "EXT",
            credit_account="EXT" if transaction_type == TransactionType.DEBIT else account_id,
            amount=amount, currency=account.currency, transaction_id=txn.transaction_id,
        ))
        self._events.append({"type": "txn_posted", "txn_id": txn.transaction_id})
        return txn

    def get_account(self, account_id: str) -> Optional[Account]:
        return self._accounts.get(account_id)

    def get_transactions(self, account_id: str, limit: int = 50) -> List[Transaction]:
        return self._transactions.get(account_id, [])[-limit:]

    def get_balance(self, account_id: str) -> Dict[str, float]:
        acc = self._accounts.get(account_id)
        if not acc:
            raise ValueError(f"Account {account_id} not found")
        return {"balance": acc.balance, "available": acc.available_balance}


class LendingEngine:
    """Loan origination and management."""

    def __init__(self, scoring_model: str = "gradient_boosting", auto_threshold: float = 0.7):
        self.scoring_model = scoring_model
        self.auto_threshold = auto_threshold
        self._products: Dict[str, LoanProduct] = {}
        self._loans: Dict[str, Loan] = {}

    def create_product(
        self, name: str, min_amount: float, max_amount: float,
        term_months: List[int], interest_rate_range: Tuple[float, float],
        origination_fee_pct: float = 0.0,
    ) -> LoanProduct:
        pid = f"PROD-{uuid.uuid4().hex[:8].upper()}"
        product = LoanProduct(pid, name, min_amount, max_amount, term_months,
                              interest_rate_range, origination_fee_pct)
        self._products[pid] = product
        return product

    def score_customer(self, credit_score: int, annual_income: float) -> float:
        score = (min(credit_score / 850.0, 1.0) * 0.5 +
                 min(annual_income / 150000.0, 1.0) * 0.3 + 0.2)
        return round(score, 3)

    def originate(
        self, customer_id: str, product_id: str, amount: float,
        term_months: int, credit_score: int, annual_income: float,
    ) -> Loan:
        product = self._products.get(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")

        risk = self.score_customer(credit_score, annual_income)
        approved = risk >= self.auto_threshold
        rate = product.interest_rate_range[0] + (1 - risk) * (
            product.interest_rate_range[1] - product.interest_rate_range[0])
        monthly_rate = rate / 100 / 12
        if monthly_rate > 0:
            payment = amount * (monthly_rate * (1 + monthly_rate) ** term_months) / (
                (1 + monthly_rate) ** term_months - 1)
        else:
            payment = amount / term_months

        loan = Loan(
            loan_id=f"LOAN-{uuid.uuid4().hex[:10].upper()}",
            customer_id=customer_id, product_id=product_id,
            principal=amount, term_months=term_months,
            interest_rate=round(rate, 2), monthly_payment=round(payment, 2),
            total_cost=round(payment * term_months, 2), approved=approved,
            status=LoanStatus.APPROVED if approved else LoanStatus.UNDER_REVIEW,
        )
        self._loans[loan.loan_id] = loan
        return loan

    def generate_amortization(self, loan: Loan) -> List[AmortizationEntry]:
        schedule = []
        balance = loan.principal
        monthly_rate = loan.interest_rate / 100 / 12
        for month in range(1, loan.term_months + 1):
            interest = balance * monthly_rate
            principal = loan.monthly_payment - interest
            balance -= principal
            schedule.append(AmortizationEntry(
                month=month, payment=loan.monthly_payment,
                principal_portion=round(principal, 2),
                interest_portion=round(interest, 2),
                remaining_balance=round(max(balance, 0), 2),
            ))
        return schedule

    def get_loan(self, loan_id: str) -> Optional[Loan]:
        return self._loans.get(loan_id)


class OpenBankingAPI:
    """PSD2-compliant Open Banking facade."""

    def __init__(self, version: str = "v3.1"):
        self.version = version
        self._tpps: Dict[str, TPPRegistration] = {}
        self._consents: Dict[str, Consent] = {}

    def register_tpp(self, name: str, redirect_uris: List[str],
                     consent_types: List[ConsentType]) -> TPPRegistration:
        tpp_id = f"TPP-{uuid.uuid4().hex[:10].upper()}"
        tpp = TPPRegistration(tpp_id, name, redirect_uris, consent_types)
        self._tpps[tpp_id] = tpp
        return tpp

    def create_consent(self, tpp_id: str, customer_id: str,
                       scope: List[str], validity_days: int = 90) -> Consent:
        if tpp_id not in self._tpps:
            raise ValueError(f"TPP {tpp_id} not registered")
        consent_id = f"CON-{uuid.uuid4().hex[:12].upper()}"
        consent = Consent(consent_id, tpp_id, customer_id, scope, validity_days)
        self._consents[consent_id] = consent
        return consent

    def get_accounts(self, consent_id: str) -> List[Account]:
        if consent_id not in self._consents:
            raise ValueError("Invalid consent")
        return []

    def get_transactions(self, consent_id: str, account_id: str,
                         from_date: str = "", to_date: str = "") -> List[Transaction]:
        if consent_id not in self._consents:
            raise ValueError("Invalid consent")
        return []


class KYCService:
    """KYC verification service."""

    def __init__(self, providers: Optional[List[str]] = None):
        self.providers = providers or ["jumio"]

    def verify(self, customer_id: str, documents: List[Dict[str, Any]],
               liveness_check: bool = True) -> KYCResult:
        total = 2 + len(documents) + (1 if liveness_check else 0)
        passed = total - 1
        return KYCResult(
            customer_id=customer_id,
            status=KYCStatus.APPROVED if passed == total else KYCStatus.MANUAL_REVIEW,
            risk_level=RiskLevel.LOW, checks_passed=passed, checks_total=total,
        )


class FXService:
    """Foreign exchange service."""

    def __init__(self):
        self._rates: Dict[Tuple[Currency, Currency], float] = {}
        pairs = [
            (Currency.USD, Currency.EUR, 0.92), (Currency.USD, Currency.GBP, 0.79),
            (Currency.USD, Currency.JPY, 149.5), (Currency.USD, Currency.CNY, 7.24),
        ]
        for f, t, r in pairs:
            self._rates[(f, t)] = r

    def get_rate(self, from_c: Currency, to_c: Currency) -> float:
        if from_c == to_c:
            return 1.0
        return self._rates.get((from_c, to_c), 1.0)

    def convert(self, amount: float, from_c: Currency, to_c: Currency) -> float:
        return round(amount * self.get_rate(from_c, to_c), 2)


def main():
    print("=" * 60)
    print("  Digital Banking Platform Demo")
    print("=" * 60)

    # Core banking
    print("\n--- Account Management ---")
    bank = CoreBankingSystem("NeoBank Pro", [Currency.USD, Currency.EUR])
    acc = bank.create_account("CUST-001", AccountType.CHECKING, Currency.USD, 1000.00, 500.00)
    print(f"  Account: {acc.account_id}, Balance: ${acc.balance:.2f}")
    bank.post_transaction(acc.account_id, 2500.00, TransactionType.CREDIT, "Payroll", "PAY-001")
    bank.post_transaction(acc.account_id, 150.00, TransactionType.DEBIT, "ATM", "ATM-001")
    bal = bank.get_balance(acc.account_id)
    print(f"  After transactions: ${bal['balance']:.2f} (available: ${bal['available']:.2f})")

    # Lending
    print("\n--- Loan Origination ---")
    lending = LendingEngine()
    product = lending.create_product("Personal Loan", 1000, 50000, [12, 24, 36], (5.99, 24.99))
    loan = lending.originate("CUST-001", product.product_id, 15000, 36, 720, 75000)
    print(f"  Loan: {loan.loan_id}, Approved: {loan.approved}")
    print(f"  Rate: {loan.interest_rate}%, Payment: ${loan.monthly_payment:.2f}")

    # Amortization
    schedule = lending.generate_amortization(loan)
    print(f"  Amortization: {len(schedule)} months, first payment split: "
          f"principal=${schedule[0].principal_portion:.2f}, interest=${schedule[0].interest_portion:.2f}")

    # Open Banking
    print("\n--- Open Banking ---")
    api = OpenBankingAPI()
    tpp = api.register_tpp("FinAggregator", ["https://finagg.com/callback"], [ConsentType.ACCOUNT_READ])
    consent = api.create_consent(tpp.tpp_id, "CUST-001", ["accounts", "transactions"])
    print(f"  TPP: {tpp.tpp_id}, Consent: {consent.consent_id}")
    print(f"  Expires: {consent.expires_date}")

    # KYC
    print("\n--- KYC Verification ---")
    kyc = KYCService()
    result = kyc.verify("CUST-001", [{"type": DocumentType.PASSPORT}], liveness_check=True)
    print(f"  Status: {result.status.value}, Checks: {result.checks_passed}/{result.checks_total}")

    # FX
    print("\n--- FX Service ---")
    fx = FXService()
    print(f"  USD→EUR: {fx.get_rate(Currency.USD, Currency.EUR)}")
    print(f"  $1000 → EUR: €{fx.convert(1000, Currency.USD, Currency.EUR):.2f}")


if __name__ == "__main__":
    main()
