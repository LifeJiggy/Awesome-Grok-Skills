"""
Digital Banking Pipeline
FinTech and payment processing systems
"""

import hashlib
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"


class TransactionStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"


@dataclass
class Account:
    account_id: str
    holder_name: str
    balance: float
    account_type: str
    currency: str = "USD"
    overdraft_limit: float = 0.0


@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    transaction_type: TransactionType
    amount: float
    currency: str
    status: TransactionStatus
    timestamp: datetime
    description: str = ""
    merchant_id: Optional[str] = None


class AccountService:
    """Core banking account management"""
    
    def __init__(self):
        self.accounts = {}
        self.transactions = []
    
    def create_account(self, holder_name: str, 
                      account_type: str,
                      currency: str = "USD") -> Account:
        """Create new account"""
        account_id = f"ACC{hashlib.md5(str(time.time()).encode()).hexdigest()[:8].upper()}"
        account = Account(
            account_id=account_id,
            holder_name=holder_name,
            balance=0.0,
            account_type=account_type,
            currency=currency
        )
        self.accounts[account_id] = account
        return account
    
    def get_balance(self, account_id: str) -> float:
        """Get account balance"""
        return self.accounts.get(account_id, Account("", "", 0, "")).balance
    
    def deposit(self, account_id: str, amount: float, 
               description: str = "") -> Transaction:
        """Deposit funds"""
        if account_id not in self.accounts:
            raise ValueError("Account not found")
        
        self.accounts[account_id].balance += amount
        
        transaction = Transaction(
            transaction_id=f"TX{time.time_ns()}",
            account_id=account_id,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            currency=self.accounts[account_id].currency,
            status=TransactionStatus.COMPLETED,
            timestamp=datetime.now(),
            description=description
        )
        self.transactions.append(transaction)
        return transaction
    
    def transfer(self, from_id: str, to_id: str, 
                amount: float) -> Tuple[Transaction, Transaction]:
        """Transfer between accounts"""
        if from_id not in self.accounts or to_id not in self.accounts:
            raise ValueError("Account not found")
        
        if self.accounts[from_id].balance + self.accounts[from_id].overdraft_limit < amount:
            raise ValueError("Insufficient funds")
        
        self.accounts[from_id].balance -= amount
        self.accounts[to_id].balance += amount
        
        debit = Transaction(
            transaction_id=f"TX{time.time_ns()}",
            account_id=from_id,
            transaction_type=TransactionType.TRANSFER,
            amount=-amount,
            currency=self.accounts[from_id].currency,
            status=TransactionStatus.COMPLETED,
            timestamp=datetime.now(),
            description=f"Transfer to {to_id}"
        )
        
        credit = Transaction(
            transaction_id=f"TX{time.time_ns()}",
            account_id=to_id,
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
            currency=self.accounts[to_id].currency,
            status=TransactionStatus.COMPLETED,
            timestamp=datetime.now(),
            description=f"Transfer from {from_id}"
        )
        
        self.transactions.extend([debit, credit])
        return debit, credit


class PaymentProcessor:
    """Payment processing gateway"""
    
    def __init__(self):
        self.merchant_ids = {}
        self.payments = []
    
    def process_payment(self,
                       merchant_id: str,
                       card_token: str,
                       amount: float,
                       currency: str = "USD") -> Dict:
        """Process payment transaction"""
        if not self._validate_card(card_token):
            return {"status": "failed", "reason": "Invalid card"}
        
        if not self._check_fraud(merchant_id, amount):
            return {"status": "failed", "reason": "Fraud detected"}
        
        transaction_id = f"PAY{time.time_ns()}"
        
        self.payments.append({
            "transaction_id": transaction_id,
            "merchant_id": merchant_id,
            "amount": amount,
            "currency": currency,
            "status": "completed",
            "timestamp": datetime.now()
        })
        
        return {
            "transaction_id": transaction_id,
            "status": "completed",
            "amount": amount,
            "currency": currency
        }
    
    def _validate_card(self, card_token: str) -> bool:
        """Validate card token"""
        return len(card_token) == 16
    
    def _check_fraud(self, merchant_id: str, amount: float) -> bool:
        """Basic fraud check"""
        return amount < 10000


class LoanCalculator:
    """Loan and credit calculations"""
    
    def calculate_payment(self,
                         principal: float,
                         annual_rate: float,
                         term_months: int) -> float:
        """Calculate monthly loan payment"""
        monthly_rate = annual_rate / 12
        return principal * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
    
    def calculate_amortization(self,
                              principal: float,
                              annual_rate: float,
                              term_months: int) -> List[Dict]:
        """Generate amortization schedule"""
        monthly_payment = self.calculate_payment(principal, annual_rate, term_months)
        schedule = []
        balance = principal
        
        for month in range(1, term_months + 1):
            interest_payment = balance * annual_rate / 12
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            
            schedule.append({
                "month": month,
                "payment": monthly_payment,
                "principal": principal_payment,
                "interest": interest_payment,
                "balance": max(0, balance)
            })
        
        return schedule
    
    def calculate_credit_score_impact(self,
                                     payment_history: List[bool],
                                     utilization: float,
                                     credit_history_months: int) -> int:
        """Estimate credit score impact"""
        base_score = 650
        
        payment_impact = sum(1 for p in payment_history if p) * 5
        utilization_impact = (1 - utilization) * 100
        history_impact = min(credit_history_months / 10, 50)
        
        return min(850, max(300, int(base_score + payment_impact + utilization_impact + history_impact)))


if __name__ == "__main__":
    account_service = AccountService()
    payment_processor = PaymentProcessor()
    loan_calculator = LoanCalculator()
    
    account = account_service.create_account("John Doe", "checking")
    account_service.deposit(account.account_id, 1000, "Initial deposit")
    
    payment = payment_processor.process_payment(
        "merchant_123",
        "4111111111111111",
        99.99
    )
    
    loan_payment = loan_calculator.calculate_payment(10000, 0.05, 36)
    amortization = loan_calculator.calculate_amortization(10000, 0.05, 36)
    
    print(f"Account: {account.account_id}")
    print(f"Balance: ${account_service.get_balance(account.account_id):.2f}")
    print(f"Payment status: {payment['status']}")
    print(f"Monthly loan payment: ${loan_payment:.2f}")
    print(f"Amortization schedule: {len(amortization)} months")
