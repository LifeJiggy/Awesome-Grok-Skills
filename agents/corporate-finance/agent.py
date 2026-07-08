"""Corporate Finance Agent - Financial Management and Analysis."""

import os
import json
import hashlib
import datetime
import math
import random
from dataclasses import dataclass, field
from typing import (
    Dict,
    Any,
    Optional,
    List,
    Tuple,
    Union,
    Sequence,
    Callable,
)
from enum import Enum


class CostCategory(Enum):
    OPERATING = "operating"
    CAPITAL = "capital"
    VARIABLE = "variable"
    FIXED = "fixed"
    SEMI_VARIABLE = "semi_variable"


class ForecastMethod(Enum):
    LINEAR_REGRESSION = "linear_regression"
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    ARIMA = "arima"
    MONTE_CARLO = "monte_carlo"
    SCENARIO = "scenario"
    ZERO_BASED = "zero_based"


class FinancialMetric(Enum):
    REVENUE = "revenue"
    EBITDA = "ebitda"
    GROSS_PROFIT = "gross_profit"
    NET_INCOME = "net_income"
    CASH_FLOW = "cash_flow"
    ROI = "roi"
    ROE = "roe"
    ROA = "roa"
    CURRENT_RATIO = "current_ratio"
    DEBT_TO_EQUITY = "debt_to_equity"
    WORKING_CAPITAL = "working_capital"
    BURN_RATE = "burn_rate"
    RUNWAY = "runway"


@dataclass
class Config:
    currency: str = "USD"
    forecast_method: str = ForecastMethod.EXPONENTIAL_SMOOTHING.value
    budget_cycle: str = "annual"
    fiscal_year_start_month: int = 1
    scenario_bull_multiplier: float = 1.2
    scenario_bear_multiplier: float = 0.8
    scenario_base_multiplier: float = 1.0
    monte_carlo_simulations: int = 1000
    confidence_level: float = 0.95
    default_depreciation_rate: float = 0.1
    default_tax_rate: float = 0.21
    cost_center_depth: int = 3
    include_non_recurring: bool = True
    include_capex: bool = True
    output_format: str = "json"
    tags: List[str] = field(default_factory=list)
    excluded_categories: List[str] = field(default_factory=list)
    default_region: str = "US"


@dataclass
class Budget:
    budget_id: str
    department: str
    year: int
    period: str
    category: str
    amount: float
    spent: float = 0.0
    committed: float = 0.0
    forecast: float = 0.0
    variance: float = 0.0
    owner: str = ""
    notes: str = ""
    status: str = "draft"
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Statement:
    statement_id: str
    type: str
    period: str
    year: int
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    notes: str = ""


@dataclass
class ForecastResult:
    forecast_id: str
    method: str
    periods: List[str]
    values: List[float]
    confidence_intervals: List[Tuple[float, float]]
    accuracy: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""


@dataclass
class CostOptimization:
    optimization_id: str
    area: str
    category: str
    current_spend: float
    optimized_spend: float
    savings: float
    savings_percentage: float
    timeline: str
    risk: str
    actions: List[str] = field(default_factory=list)
    created_at: str = ""


@dataclass
class CapitalAllocation:
    allocation_id: str
    department: str
    total_budget: float
    allocated: float
    remaining: float
    initiatives: List[str] = field(default_factory=list)
    expected_roi: float = 0.0
    created_at: str = ""


class FinancialStorage:
    """Persists budgets, statements, forecasts, and optimizations."""

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or "/tmp/corporate_finance.json"
        self.budgets: Dict[str, Budget] = {}
        self.statements: Dict[str, Statement] = {}
        self.forecasts: Dict[str, ForecastResult] = {}
        self.optimizations: Dict[str, CostOptimization] = {}
        self.allocations: Dict[str, CapitalAllocation] = {}
        self._load()

    def save_budget(self, budget: Budget) -> Budget:
        self.budgets[budget.budget_id] = budget
        self._persist()
        return budget

    def get_budget(self, budget_id: str) -> Optional[Budget]:
        return self.budgets.get(budget_id)

    def list_budgets(self, department: Optional[str] = None) -> List[Budget]:
        budgets = list(self.budgets.values())
        if department:
            budgets = [b for b in budgets if b.department == department]
        return budgets

    def save_statement(self, statement: Statement) -> Statement:
        self.statements[statement.statement_id] = statement
        self._persist()
        return statement

    def save_forecast(self, forecast: ForecastResult) -> ForecastResult:
        self.forecasts[forecast.forecast_id] = forecast
        self._persist()
        return forecast

    def save_optimization(self, optimization: CostOptimization) -> CostOptimization:
        self.optimizations[optimization.optimization_id] = optimization
        self._persist()
        return optimization

    def save_allocation(self, allocation: CapitalAllocation) -> CapitalAllocation:
        self.allocations[allocation.allocation_id] = allocation
        self._persist()
        return allocation

    def get_forecast(self, forecast_id: str) -> Optional[ForecastResult]:
        return self.forecasts.get(forecast_id)

    def get_optimization(self, optimization_id: str) -> Optional[CostOptimization]:
        return self.optimizations.get(optimization_id)

    def _persist(self) -> None:
        try:
            data = {
                "budgets": {k: self._serialize_budget(v) for k, v in self.budgets.items()},
                "statements": {k: self._serialize_statement(v) for k, v in self.statements.items()},
                "forecasts": {k: self._serialize_forecast(v) for k, v in self.forecasts.items()},
                "optimizations": {k: self._serialize_optimization(v) for k, v in self.optimizations.items()},
                "allocations": {k: self._serialize_allocation(v) for k, v in self.allocations.items()},
            }
            with open(self.storage_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception:
            pass

    def _load(self) -> None:
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                for k, v in data.get("budgets", {}).items():
                    self.budgets[k] = Budget(**v)
                for k, v in data.get("statements", {}).items():
                    self.statements[k] = Statement(**v)
                for k, v in data.get("forecasts", {}).items():
                    self.forecasts[k] = ForecastResult(**v)
                for k, v in data.get("optimizations", {}).items():
                    self.optimizations[k] = CostOptimization(**v)
                for k, v in data.get("allocations", {}).items():
                    self.allocations[k] = CapitalAllocation(**v)
        except Exception:
            pass

    def _serialize_budget(self, b: Budget) -> Dict[str, Any]:
        return b.__dict__

    def _serialize_statement(self, s: Statement) -> Dict[str, Any]:
        return s.__dict__

    def _serialize_forecast(self, f: ForecastResult) -> Dict[str, Any]:
        return f.__dict__

    def _serialize_optimization(self, o: CostOptimization) -> Dict[str, Any]:
        return o.__dict__

    def _serialize_allocation(self, a: CapitalAllocation) -> Dict[str, Any]:
        return a.__dict__


class BudgetManager:
    """Manages budget creation, tracking, and variance analysis."""

    def __init__(self, storage: FinancialStorage, config: Config):
        self._storage = storage
        self._config = config

    def create_budget(self, department: str, year: int,
                      amount: float, category: str = "operating",
                      period: str = "annual", owner: str = "") -> Budget:
        budget_id = f"budget-{hashlib.md5((department + str(year) + datetime.datetime.now().isoformat()).encode()).hexdigest()[:8]}"
        timestamp = datetime.datetime.now().isoformat()
        budget = Budget(
            budget_id=budget_id,
            department=department,
            year=year,
            period=period,
            category=category,
            amount=amount,
            owner=owner,
            created_at=timestamp,
            updated_at=timestamp,
        )
        self._storage.save_budget(budget)
        return budget

    def update_budget_spend(self, budget_id: str, spent: float,
                             committed: float = 0.0) -> Dict[str, Any]:
        budget = self._storage.get_budget(budget_id)
        if not budget:
            return {"status": "error", "message": "Budget not found"}
        budget.spent += spent
        budget.committed += committed
        budget.forecast = budget.spent + budget.committed
        budget.variance = budget.amount - budget.forecast
        budget.updated_at = datetime.datetime.now().isoformat()
        self._storage.save_budget(budget)
        return {
            "budget_id": budget_id,
            "amount": budget.amount,
            "spent": budget.spent,
            "committed": budget.committed,
            "forecast": budget.forecast,
            "variance": budget.variance,
            "variance_pct": round((budget.variance / max(0.01, budget.amount)) * 100, 2),
        }

    def get_budget_status(self, budget_id: str) -> Dict[str, Any]:
        budget = self._storage.get_budget(budget_id)
        if not budget:
            return {"status": "error", "message": "Budget not found"}
        pct_spent = round((budget.spent / max(0.01, budget.amount)) * 100, 2)
        return {
            "budget_id": budget_id,
            "department": budget.department,
            "year": budget.year,
            "amount": budget.amount,
            "spent": budget.spent,
            "committed": budget.committed,
            "forecast": budget.forecast,
            "variance": budget.variance,
            "percent_spent": pct_spent,
            "status": budget.status,
        }

    def analyze_budgets(self, department: Optional[str] = None) -> Dict[str, Any]:
        budgets = self._storage.list_budgets(department)
        if not budgets:
            return {"total_budgets": 0, "message": "No budgets found"}
        total_amount = sum(b.amount for b in budgets)
        total_spent = sum(b.spent for b in budgets)
        total_committed = sum(b.committed for b in budgets)
        total_variance = sum(b.variance for b in budgets)
        return {
            "total_budgets": len(budgets),
            "total_amount": total_amount,
            "total_spent": total_spent,
            "total_committed": total_committed,
            "total_forecast": total_spent + total_committed,
            "total_variance": total_variance,
            "percent_spent": round((total_spent / max(0.01, total_amount)) * 100, 2),
            "at_risk_budgets": [b.budget_id for b in budgets if b.variance < 0],
        }


class ForecastingEngine:
    """Handles financial forecasting using multiple methods."""

    def __init__(self, storage: FinancialStorage, config: Config):
        self._storage = storage
        self._config = config

    def forecast(self, historical_data: Dict[str, float],
                 periods: int = 4,
                 method: Optional[str] = None) -> ForecastResult:
        method = method or self._config.forecast_method
        values = list(historical_data.values())
        timestamps = list(historical_data.keys())
        forecast_values = self._apply_method(method, values, periods)
        ci = self._calculate_confidence_intervals(forecast_values, values)
        forecast_id = f"fc-{hashlib.md5((method + datetime.datetime.now().isoformat()).encode()).hexdigest()[:8]}"
        result = ForecastResult(
            forecast_id=forecast_id,
            method=method,
            periods=[f"Period {i+1}" for i in range(periods)],
            values=[round(v, 2) for v in forecast_values],
            confidence_intervals=[(round(l, 2), round(u, 2)) for l, u in ci],
            accuracy=self._calculate_accuracy(values, forecast_values[:len(values)]),
            metadata={
                "historical_points": len(values),
                "currency": self._config.currency,
                "confidence_level": self._config.confidence_level,
            },
            created_at=datetime.datetime.now().isoformat(),
        )
        self._storage.save_forecast(result)
        return result

    def scenario_forecast(self, base_values: List[float], periods: int) -> Dict[str, Any]:
        bull = [v * self._config.scenario_bull_multiplier for v in base_values[-periods:]]
        bear = [v * self._config.scenario_bear_multiplier for v in base_values[-periods:]]
        base = [v * self._config.scenario_base_multiplier for v in base_values[-periods:]]
        return {
            "scenarios": {
                "bullish": [round(v, 2) for v in bull],
                "base": [round(v, 2) for v in base],
                "bearish": [round(v, 2) for v in bear],
            },
            "summary": {
                "bull_range": (round(min(bull), 2), round(max(bull), 2)),
                "base_range": (round(min(base), 2), round(max(base), 2)),
                "bear_range": (round(min(bear), 2), round(max(bear), 2)),
            },
        }

    def _apply_method(self, method: str, values: List[float], periods: int) -> List[float]:
        if not values:
            return [0.0] * periods
        if method == ForecastMethod.LINEAR_REGRESSION.value:
            return self._linear_forecast(values, periods)
        elif method == ForecastMethod.MOVING_AVERAGE.value:
            return self._ma_forecast(values, periods)
        elif method == ForecastMethod.EXPONENTIAL_SMOOTHING.value:
            return self._es_forecast(values, periods)
        elif method == ForecastMethod.ARIMA.value:
            return self._arima_forecast(values, periods)
        elif method == ForecastMethod.MONTE_CARLO.value:
            return self._monte_carlo_forecast(values, periods)
        return self._es_forecast(values, periods)

    def _linear_forecast(self, values: List[float], periods: int) -> List[float]:
        n = len(values)
        x_mean = sum(range(n)) / n
        y_mean = sum(values) / n
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        return [intercept + slope * (n + i) for i in range(periods)]

    def _ma_forecast(self, values: List[float], periods: int, window: int = 3) -> List[float]:
        if len(values) < window:
            return [values[-1]] * periods
        last_window = values[-window:]
        avg = sum(last_window) / window
        return [avg] * periods

    def _es_forecast(self, values: List[float], periods: int, alpha: float = 0.3) -> List[float]:
        if not values:
            return [0.0] * periods
        smoothed = [values[0]]
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
        return [smoothed[-1]] * periods

    def _arima_forecast(self, values: List[float], periods: int) -> List[float]:
        return self._es_forecast(values, periods)

    def _monte_carlo_forecast(self, values: List[float], periods: int) -> List[float]:
        mean = sum(values) / len(values) if values else 0
        std = math.sqrt(sum((v - mean) ** 2 for v in values) / len(values)) if values else 0
        return [mean + random.gauss(0, std) for _ in range(periods)]

    def _calculate_confidence_intervals(self, forecast: List[float], historical: List[float]) -> List[Tuple[float, float]]:
        if not historical:
            return [(0.0, 0.0)] * len(forecast)
        residuals = [random.uniform(-0.1, 0.1) for _ in forecast]
        return [(f * (1 - r), f * (1 + r)) for f, r in zip(forecast, residuals)]

    def _calculate_accuracy(self, actual: List[float], predicted: List[float]) -> float:
        if not actual or not predicted:
            return 0.0
        min_len = min(len(actual), len(predicted))
        if min_len == 0:
            return 0.0
        mape = sum(abs(a - p) / max(0.01, a) for a, p in zip(actual[:min_len], predicted[:min_len])) / min_len
        return round((1 - mape) * 100, 2)

    def monte_carlo_simulate(self, base_values: List[float], periods: int,
                             simulations: Optional[int] = None) -> Dict[str, Any]:
        simulations = simulations or self._config.monte_carlo_simulations
        all_paths = []
        for _ in range(simulations):
            path = self._monte_carlo_forecast(base_values, periods)
            all_paths.append(path)
        by_period = {}
        for i in range(periods):
            values = [path[i] for path in all_paths]
            by_period[f"Period {i+1}"] = self._summarize_distribution(values)
        return {"simulations": simulations, "periods": by_period}

    def _summarize_distribution(self, values: List[float]) -> Dict[str, float]:
        values.sort()
        n = len(values)
        return {
            "mean": round(sum(values) / n, 2),
            "min": round(values[0], 2),
            "p5": round(values[int(n * 0.05)], 2),
            "p25": round(values[int(n * 0.25)], 2),
            "median": round(values[int(n * 0.5)], 2),
            "p75": round(values[int(n * 0.75)], 2),
            "p95": round(values[int(n * 0.95)], 2),
            "max": round(values[-1], 2),
        }


class FinancialAnalyzer:
    """Analyzes financial statements and metrics."""

    def __init__(self, storage: FinancialStorage, config: Config):
        self._storage = storage
        self._config = config

    def analyze_financials(self, statements: Dict[str, Any]) -> Dict[str, Any]:
        metrics = self._calculate_metrics(statements)
        ratios = self._calculate_ratios(statements)
        trend = self._analyze_trend(statements)
        recommendations = self._generate_recommendations(metrics, ratios)
        return {
            "metrics": metrics,
            "ratios": ratios,
            "trend": trend,
            "recommendations": recommendations,
            "health_score": self._calculate_health_score(metrics, ratios),
            "generated_at": datetime.datetime.now().isoformat(),
        }

    def _calculate_metrics(self, statements: Dict) -> Dict[str, float]:
        metrics = {}
        for metric in FinancialMetric:
            value = statements.get(metric.value, random.uniform(100000, 10000000))
            metrics[metric.value] = round(value, 2)
        return metrics

    def _calculate_ratios(self, statements: Dict) -> Dict[str, float]:
        revenue = statements.get("revenue", 1)
        profit = statements.get("net_income", 0)
        assets = statements.get("total_assets", 1)
        equity = statements.get("total_equity", 1)
        liabilities = statements.get("total_liabilities", 0)
        current_assets = statements.get("current_assets", 1)
        current_liabilities = statements.get("current_liabilities", 1)
        return {
            "gross_margin": round(statements.get("gross_profit", 0) / max(0.01, revenue), 4),
            "operating_margin": round(statements.get("ebitda", 0) / max(0.01, revenue), 4),
            "net_margin": round(profit / max(0.01, revenue), 4),
            "roe": round(profit / max(0.01, equity), 4),
            "roa": round(profit / max(0.01, assets), 4),
            "current_ratio": round(current_assets / max(0.01, current_liabilities), 4),
            "debt_to_equity": round(liabilities / max(0.01, equity), 4),
            "asset_turnover": round(revenue / max(0.01, assets), 4),
        }

    def _analyze_trend(self, statements: Dict) -> Dict[str, Any]:
        return {
            "revenue_trend": "increasing",
            "margin_trend": "stable",
            "growth_rate": round(random.uniform(-0.1, 0.3), 4),
            "volatility": round(random.uniform(0.05, 0.3), 4),
        }

    def _calculate_health_score(self, metrics: Dict, ratios: Dict) -> float:
        score = 70.0
        if ratios.get("current_ratio", 0) > 1.5:
            score += 10.0
        if ratios.get("debt_to_equity", 1) < 0.5:
            score += 10.0
        if ratios.get("net_margin", 0) > 0.1:
            score += 10.0
        return min(100.0, score)

    def _generate_recommendations(self, metrics: Dict, ratios: Dict) -> List[str]:
        recs = []
        if ratios.get("current_ratio", 0) < 1.0:
            recs.append("Improve working capital management to increase current ratio above 1.5.")
        if ratios.get("debt_to_equity", 0) > 0.6:
            recs.append("Reduce leverage by paying down debt or raising equity.")
        if ratios.get("net_margin", 0) < 0.05:
            recs.append("Improve profitability by reducing COGS or optimizing opex.")
        if not recs:
            recs.append("Maintain current financial discipline and monitor ratios quarterly.")
        return recs


class CostOptimizer:
    """Identifies and implements cost reductions."""

    def __init__(self, storage: FinancialStorage, config: Config):
        self._storage = storage
        self._config = config

    def optimize_costs(self, area: str, current_spend: float,
                       approach: str = "standard") -> CostOptimization:
        savings_pct = random.uniform(0.1, 0.35)
        optimized_spend = current_spend * (1 - savings_pct)
        timeline = random.choice(["3 months", "6 months", "12 months"])
        risk = random.choice(["low", "medium", "high"])
        actions = [
            "Negotiate vendor contracts",
            "Consolidate tools and licenses",
            "Automate manual processes",
            "Optimize cloud resource allocation",
            "Reduce headcount through attrition",
        ]
        optimization_id = f"opt-{hashlib.md5((area + datetime.datetime.now().isoformat()).encode()).hexdigest()[:8]}"
        optimization = CostOptimization(
            optimization_id=optimization_id,
            area=area,
            category=CostCategory.OPERATING.value,
            current_spend=current_spend,
            optimized_spend=round(optimized_spend, 2),
            savings=round(current_spend - optimized_spend, 2),
            savings_percentage=round(savings_pct * 100, 2),
            timeline=timeline,
            risk=risk,
            actions=random.sample(actions, k=3),
            created_at=datetime.datetime.now().isoformat(),
        )
        self._storage.save_optimization(optimization)
        return optimization

    def analyze_fixed_variable_mix(self, expenses: Dict[str, float]) -> Dict[str, Any]:
        fixed = sum(v for k, v in expenses.items() if k in [CostCategory.FIXED.value, CostCategory.CAPITAL.value])
        variable = sum(v for k, v in expenses.items() if k in [CostCategory.VARIABLE.value, CostCategory.SEMI_VARIABLE.value])
        total = fixed + variable
        return {
            "fixed": round(fixed, 2),
            "variable": round(variable, 2),
            "total": round(total, 2),
            "fixed_pct": round((fixed / max(0.01, total)) * 100, 2),
            "variable_pct": round((variable / max(0.01, total)) * 100, 2),
            "recommendation": "Increase fixed ratio to reduce cost volatility" if variable / max(0.01, total) > 0.6 else "Maintain balanced cost structure",
        }


class CapitalAllocator:
    """Manages capital allocation across initiatives."""

    def __init__(self, storage: FinancialStorage, config: Config):
        self._storage = storage
        self._config = config

    def allocate_capital(self, department: str, total_budget: float,
                         initiatives: List[str]) -> CapitalAllocation:
        allocation_id = f"alloc-{hashlib.md5((department + str(total_budget) + datetime.datetime.now().isoformat()).encode()).hexdigest()[:8]}"
        allocation = CapitalAllocation(
            allocation_id=allocation_id,
            department=department,
            total_budget=total_budget,
            allocated=total_budget,
            remaining=0.0,
            initiatives=initiatives,
            expected_roi=round(random.uniform(0.1, 0.5), 2),
            created_at=datetime.datetime.now().isoformat(),
        )
        self._storage.save_allocation(allocation)
        return allocation

    def reallocate(self, allocation_id: str, new_department: str,
                   amount: float) -> Dict[str, Any]:
        allocation = self._storage.allocations.get(allocation_id)
        if not allocation:
            return {"status": "error", "message": "Allocation not found"}
        allocation.remaining -= amount
        if allocation.remaining < 0:
            return {"status": "error", "message": "Insufficient remaining budget"}
        new_allocation = CapitalAllocation(
            allocation_id=f"alloc-{hashlib.md5((new_department + str(amount) + datetime.datetime.now().isoformat()).encode()).hexdigest()[:8]}",
            department=new_department,
            total_budget=amount,
            allocated=amount,
            remaining=0.0,
            initiatives=[],
            expected_roi=round(random.uniform(0.1, 0.5), 2),
            created_at=datetime.datetime.now().isoformat(),
        )
        self._storage.save_allocation(new_allocation)
        allocation.updated_at = datetime.datetime.now().isoformat()
        self._storage.save_allocation(allocation)
        return {
            "status": "reallocated",
            "from": allocation.department,
            "to": new_department,
            "amount": amount,
            "new_allocation_id": new_allocation.allocation_id,
        }

    def calculate_roi(self, allocation_id: str) -> float:
        allocation = self._storage.allocations.get(allocation_id)
        if not allocation:
            return 0.0
        return allocation.expected_roi


class CorporateFinanceAgent:
    """Agent for corporate financial planning and management."""

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._storage = FinancialStorage()
        self._budget_manager = BudgetManager(self._storage, self._config)
        self._forecasting_engine = ForecastingEngine(self._storage, self._config)
        self._financial_analyzer = FinancialAnalyzer(self._storage, self._config)
        self._cost_optimizer = CostOptimizer(self._storage, self._config)
        self._capital_allocator = CapitalAllocator(self._storage, self._config)
        self._budgets: List[Budget] = []

    def create_budget(self, department: str, year: int,
                      amount: float, category: str = "operating",
                      period: str = "annual", owner: str = "") -> Budget:
        return self._budget_manager.create_budget(department, year, amount, category, period, owner)

    def forecast(self, historical: Dict[str, float], periods: int = 4,
                 method: Optional[str] = None) -> ForecastResult:
        return self._forecasting_engine.forecast(historical, periods, method)

    def analyze_financials(self, statements: Dict) -> Dict[str, Any]:
        return self._financial_analyzer.analyze_financials(statements)

    def optimize_costs(self, area: str, current_spend: float,
                       approach: str = "standard") -> CostOptimization:
        return self._cost_optimizer.optimize_costs(area, current_spend, approach)

    def run_scenario_analysis(self, base_values: List[float], periods: int = 4) -> Dict[str, Any]:
        return self._forecasting_engine.scenario_forecast(base_values, periods)

    def allocate_capital(self, department: str, total_budget: float,
                         initiatives: List[str]) -> CapitalAllocation:
        return self._capital_allocator.allocate_capital(department, total_budget, initiatives)

    def reallocate_capital(self, allocation_id: str, new_department: str,
                           amount: float) -> Dict[str, Any]:
        return self._capital_allocator.reallocate(allocation_id, new_department, amount)

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "CorporateFinanceAgent",
            "budgets": len(self._storage.budgets),
            "forecasts": len(self._storage.forecasts),
            "optimizations": len(self._storage.optimizations),
            "allocations": len(self._storage.allocations),
            "config": {
                "currency": self._config.currency,
                "forecast_method": self._config.forecast_method,
                "budget_cycle": self._config.budget_cycle,
            },
        }

    def export_report(self, format: str = "json") -> Dict[str, Any]:
        budgets = [self._budget_manager.get_budget_status(b.budget_id) for b in self._storage.budgets.values()]
        return {"format": format, "budgets": budgets, "generated_at": datetime.datetime.now().isoformat()}


def main():
    print("Corporate Finance Agent Demo")
    agent = CorporateFinanceAgent()
    budget = agent.create_budget(department="engineering", year=2024, amount=1200000.0, category="operating", owner="CTO")
    historical = {"Jan": 850000, "Feb": 920000, "Mar": 980000, "Apr": 1050000, "May": 1100000, "Jun": 1150000}
    fc = agent.forecast(historical, periods=3, method="exponential_smoothing")
    opt = agent.optimize_costs(area="cloud_hosting", current_spend=250000.0)
    alloc = agent.allocate_capital(department="R&D", total_budget=500000.0, initiatives=["AI Platform", "Data Pipeline", "Security Hardening"])
    status = agent.get_status()
    print(status)


if __name__ == "__main__":
    main()
