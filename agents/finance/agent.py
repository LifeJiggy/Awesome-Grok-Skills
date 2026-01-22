"""
Finance Agent
Financial analysis and operations automation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    INVESTMENT = "investment"


@dataclass
class FinancialRecord:
    record_id: str
    date: datetime
    type: TransactionType
    category: str
    amount: float
    description: str
    account: str


class BudgetTracker:
    """Personal/corporate budget tracking"""
    
    def __init__(self):
        self.accounts = {}
        self.transactions = []
        self.budgets = {}
    
    def add_account(self, name: str, account_type: str, balance: float = 0):
        """Add financial account"""
        self.accounts[name] = {
            "type": account_type,
            "balance": balance,
            "transactions": []
        }
    
    def record_transaction(self, 
                          record: FinancialRecord):
        """Record financial transaction"""
        self.transactions.append(record)
        
        if record.account in self.accounts:
            if record.type in [TransactionType.INCOME, TransactionType.INVESTMENT]:
                self.accounts[record.account]["balance"] += record.amount
            else:
                self.accounts[record.account]["balance"] -= record.amount
            
            self.accounts[record.account]["transactions"].append(record.record_id)
    
    def create_budget(self,
                     category: str,
                     amount: float,
                     period: str = "monthly"):
        """Create budget"""
        self.budgets[category] = {
            "amount": amount,
            "spent": 0,
            "period": period,
            "created_at": datetime.now()
        }
    
    def get_budget_status(self, category: str = None) -> Dict:
        """Get budget status"""
        if category:
            if category not in self.budgets:
                return {}
            budget = self.budgets[category]
            return {
                "category": category,
                "budget": budget["amount"],
                "spent": budget["spent"],
                "remaining": budget["amount"] - budget["spent"],
                "percent_used": (budget["spent"] / budget["amount"] * 100) if budget["amount"] > 0 else 0
            }
        
        return {
            cat: self.get_budget_status(cat) 
            for cat in self.budgets
        }
    
    def generate_report(self, 
                       start_date: datetime,
                       end_date: datetime) -> Dict:
        """Generate financial report"""
        filtered = [t for t in self.transactions 
                   if start_date <= t.date <= end_date]
        
        income = sum(t.amount for t in filtered if t.type == TransactionType.INCOME)
        expenses = sum(t.amount for t in filtered if t.type == TransactionType.EXPENSE)
        
        by_category = {}
        for t in filtered:
            if t.type == TransactionType.EXPENSE:
                by_category[t.category] = by_category.get(t.category, 0) + t.amount
        
        return {
            "period": {"start": start_date, "end": end_date},
            "total_income": income,
            "total_expenses": expenses,
            "net_income": income - expenses,
            "expenses_by_category": by_category,
            "transaction_count": len(filtered)
        }


class InvestmentAnalyzer:
    """Investment analysis utilities"""
    
    def __init__(self):
        self.portfolio = {}
        self.historical_data = {}
    
    def add_position(self, 
                    symbol: str,
                    shares: float,
                    purchase_price: float,
                    purchase_date: datetime):
        """Add investment position"""
        self.portfolio[symbol] = {
            "shares": shares,
            "purchase_price": purchase_price,
            "purchase_date": purchase_date,
            "current_price": purchase_price
        }
    
    def update_price(self, symbol: str, price: float):
        """Update current price"""
        if symbol in self.portfolio:
            self.portfolio[symbol]["current_price"] = price
    
    def get_portfolio_value(self) -> Dict:
        """Calculate portfolio value"""
        total_value = 0
        total_cost = 0
        
        for symbol, position in self.portfolio.items():
            value = position["shares"] * position["current_price"]
            cost = position["shares"] * position["purchase_price"]
            total_value += value
            total_cost += cost
            
            position["market_value"] = value
            position["gain_loss"] = value - cost
            position["gain_loss_percent"] = ((value - cost) / cost * 100) if cost > 0 else 0
        
        return {
            "total_value": total_value,
            "total_cost": total_cost,
            "total_gain_loss": total_value - total_cost,
            "total_gain_loss_percent": ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            "positions": self.portfolio
        }
    
    def calculate_returns(self, 
                         symbol: str = None,
                         period: str = "ytd") -> Dict:
        """Calculate investment returns"""
        if symbol:
            if symbol not in self.portfolio:
                return {}
            position = self.portfolio[symbol]
            return {
                "symbol": symbol,
                "total_return": position["gain_loss"],
                "total_return_percent": position["gain_loss_percent"],
                "current_value": position["market_value"]
            }
        
        portfolio = self.get_portfolio_value()
        return {
            "total_return": portfolio["total_gain_loss"],
            "total_return_percent": portfolio["total_gain_loss_percent"]
        }


class InvoiceGenerator:
    """Invoice generation"""
    
    def __init__(self):
        self.templates = {}
        self.invoices = {}
    
    def create_invoice(self,
                      invoice_number: str,
                      customer: Dict,
                      items: List[Dict],
                      due_date: datetime = None) -> Dict:
        """Create invoice"""
        subtotal = sum(item["quantity"] * item["unit_price"] for item in items)
        tax = subtotal * 0.1  # 10% tax
        total = subtotal + tax
        
        invoice = {
            "invoice_number": invoice_number,
            "customer": customer,
            "items": items,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "due_date": due_date or (datetime.now() + timedelta(days=30)),
            "status": "draft",
            "created_at": datetime.now()
        }
        
        self.invoices[invoice_number] = invoice
        return invoice
    
    def send_invoice(self, invoice_number: str) -> bool:
        """Send invoice to customer"""
        if invoice_number not in self.invoices:
            return False
        
        self.invoices[invoice_number]["status"] = "sent"
        return True
    
    def get_overdue_invoices(self) -> List[Dict]:
        """Get overdue invoices"""
        now = datetime.now()
        return [
            inv for inv in self.invoices.values()
            if inv["status"] in ["sent", "overdue"] and inv["due_date"] < now
        ]


class FinancialForecaster:
    """Financial forecasting"""
    
    def __init__(self):
        self.models = {}
    
    def forecast_cashflow(self,
                         historical_data: List[Dict],
                         periods: int = 12,
                         method: str = "moving_average") -> Dict:
        """Forecast cash flow"""
        values = [d.get("cash_flow", 0) for d in historical_data]
        
        if method == "moving_average":
            window = min(3, len(values))
            forecast = []
            for _ in range(periods):
                if len(values) >= window:
                    avg = sum(values[-window:]) / window
                else:
                    avg = sum(values) / len(values) if values else 0
                forecast.append(avg)
                values.append(avg)
        
        elif method == "linear_regression":
            n = len(values)
            x = list(range(n))
            x_mean = sum(x) / n
            y_mean = sum(values) / n
            
            numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, values))
            denominator = sum((xi - x_mean)**2 for xi in x)
            
            slope = numerator / denominator if denominator != 0 else 0
            intercept = y_mean - slope * x_mean
            
            forecast = [intercept + slope * (n + i) for i in range(periods)]
        
        else:
            forecast = [values[-1]] * periods
        
        return {
            "forecast": forecast,
            "method": method,
            "periods": periods,
            "confidence_interval": self._calculate_confidence(values, forecast)
        }
    
    def _calculate_confidence(self, historical: List[float], forecast: List[float]) -> Dict:
        """Calculate forecast confidence intervals"""
        return {"lower": [f * 0.9 for f in forecast], "upper": [f * 1.1 for f in forecast]}
    
    def calculate_breakeven(self,
                           fixed_costs: float,
                           variable_cost_per_unit: float,
                           price_per_unit: float) -> Dict:
        """Calculate breakeven point"""
        contribution_margin = price_per_unit - variable_cost_per_unit
        
        if contribution_margin <= 0:
            return {"error": "No profit potential"}
        
        breakeven_units = fixed_costs / contribution_margin
        breakeven_revenue = breakeven_units * price_per_unit
        
        return {
            "breakeven_units": breakeven_units,
            "breakeven_revenue": breakeven_revenue,
            "contribution_margin": contribution_margin,
            "margin_percent": (contribution_margin / price_per_unit * 100) if price_per_unit > 0 else 0
        }


if __name__ == "__main__":
    budget = BudgetTracker()
    investment = InvestmentAnalyzer()
    invoice = InvoiceGenerator()
    forecast = FinancialForecaster()
    
    budget.add_account("Checking", "bank", 5000)
    budget.add_account("Savings", "bank", 10000)
    
    budget.record_transaction(FinancialRecord(
        "tx1", datetime.now(), TransactionType.INCOME,
        "Salary", 5000, "Monthly salary", "Checking"
    ))
    
    budget.create_budget("Groceries", 500)
    budget.create_budget("Entertainment", 200)
    
    budget_status = budget.get_budget_status()
    
    investment.add_position("AAPL", 10, 150, datetime.now() - timedelta(days=30))
    investment.update_price("AAPL", 175)
    portfolio = investment.get_portfolio_value()
    
    inv = invoice.create_invoice(
        "INV-001",
        {"name": "Acme Corp", "email": "billing@acme.com"},
        [{"description": "Service", "quantity": 10, "unit_price": 100}]
    )
    
    historical = [{"cash_flow": 10000}, {"cash_flow": 12000}, {"cash_flow": 11000}]
    cashflow_forecast = forecast.forecast_cashflow(historical, periods=6)
    breakeven = forecast.calculate_breakeven(50000, 20, 50)
    
    print(f"Budget status: {list(budget_status.keys())}")
    print(f"Portfolio value: ${portfolio['total_value']:.2f}")
    print(f"Invoice total: ${inv['total']:.2f}")
    print(f"Cashflow forecast: {len(cashflow_forecast['forecast'])} periods")
    print(f"Breakeven units: {breakeven['breakeven_units']:.0f}")
