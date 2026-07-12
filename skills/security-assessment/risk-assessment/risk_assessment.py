"""
Risk Assessment Module

Provides FAIR quantitative analysis, qualitative risk matrices,
business impact analysis, and Monte Carlo simulation for security risk management.
"""

from __future__ import annotations

import math
import random
import logging
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, Callable
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ──────────────────────────── Enums ────────────────────────────

class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NEGLIGIBLE = "NEGLIGIBLE"


class RiskTreatment(str, Enum):
    ACCEPT = "accept"
    MITIGATE = "mitigate"
    TRANSFER = "transfer"
    AVOID = "avoid"


class RiskStatus(str, Enum):
    IDENTIFIED = "identified"
    ANALYZING = "analyzing"
    TREATING = "treating"
    MONITORING = "monitoring"
    CLOSED = "closed"


class LossType(str, Enum):
    PRODUCTIVITY = "productivity"
    RESPONSE = "response"
    REPLACEMENT = "replacement"
    FINES_JUDGMENTS = "fines_judgments"
    COMPETITIVE_ADVANTAGE = "competitive_advantage"
    REPUTATION = "reputation"


class ThreatType(str, Enum):
    RANSOMWARE = "ransomware"
    DATA_BREACH = "data_breach"
    DDOS = "ddos"
    INSIDER_THREAT = "insider_threat"
    SUPPLY_CHAIN = "supply_chain"
    PHISHING = "phishing"
    ZERO_DAY = "zero_day"


# ──────────────────────────── Dataclasses ─────────────────────

@dataclass
class RiskScenario:
    id: str
    title: str
    description: str
    threat_type: ThreatType
    affected_assets: list[str]
    likelihood: int = 1
    impact: int = 1
    treatment: RiskTreatment = RiskTreatment.ACCEPT
    status: RiskStatus = RiskStatus.IDENTIFIED
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    target_date: Optional[datetime] = None
    residual_likelihood: int = 0
    residual_impact: int = 0

    @property
    def risk_score(self) -> int:
        return self.likelihood * self.impact

    @property
    def residual_score(self) -> int:
        return self.residual_likelihood * self.residual_impact

    @property
    def risk_level(self) -> RiskLevel:
        score = self.risk_score
        if score >= 20:
            return RiskLevel.CRITICAL
        elif score >= 12:
            return RiskLevel.HIGH
        elif score >= 6:
            return RiskLevel.MEDIUM
        elif score >= 1:
            return RiskLevel.LOW
        return RiskLevel.NEGLIGIBLE


@dataclass
class FAIRScenario:
    name: str
    threat_event_frequency: float
    vulnerability_rate: float
    loss_magnitude_min: float
    loss_magnitude_max: float
    ale: float = 0.0
    percentile_50: float = 0.0
    percentile_95: float = 0.0
    percentile_99: float = 0.0
    risk_rating: str = "unknown"
    confidence: float = 0.95


@dataclass
class MonteCarloResult:
    mean: float = 0.0
    median: float = 0.0
    std_dev: float = 0.0
    var_95: float = 0.0
    var_99: float = 0.0
    min_loss: float = 0.0
    max_loss: float = 0.0
    iterations: int = 0
    samples: list[float] = field(default_factory=list)

    def exceedance_probability(self, threshold: float) -> float:
        if not self.samples:
            return 0.0
        above = sum(1 for s in self.samples if s > threshold)
        return above / len(self.samples)


@dataclass
class BusinessImpact:
    threat: str
    revenue_loss: float = 0.0
    regulatory_fine: float = 0.0
    reputational_cost: float = 0.0
    recovery_cost: float = 0.0
    total_impact: float = 0.0
    recovery_hours: int = 0

    def __post_init__(self):
        self.total_impact = (self.revenue_loss + self.regulatory_fine
                             + self.reputational_cost + self.recovery_cost)


@dataclass
class RiskMatrixEntry:
    id: str
    title: str
    likelihood: int
    impact: int
    risk_level: RiskLevel
    exceeds_appetite: bool = False


@dataclass
class SimulationScenario:
    name: str
    frequency_dist: str
    frequency_params: dict
    magnitude_dist: str
    magnitude_params: dict


# ──────────────────────────── Helper Classes ──────────────────

class MonteCarloSimulator:
    """Monte Carlo simulation engine for probabilistic risk analysis."""

    def __init__(self, iterations: int = 10000, seed: int | None = None):
        self.iterations = iterations
        self.scenarios: list[SimulationScenario] = []
        if seed is not None:
            random.seed(seed)

    def add_scenario(self, name: str, frequency_dist: str,
                     frequency_params: dict, magnitude_dist: str,
                     magnitude_params: dict) -> None:
        self.scenarios.append(SimulationScenario(
            name=name, frequency_dist=frequency_dist,
            frequency_params=frequency_params,
            magnitude_dist=magnitude_dist,
            magnitude_params=magnitude_params,
        ))

    def _sample_frequency(self, dist: str, params: dict) -> int:
        if dist == "poisson":
            lam = params.get("lambda", 1.0)
            return random.randint(0, max(int(lam * 3), 10))
        elif dist == "uniform":
            return random.randint(int(params.get("low", 1)),
                                  int(params.get("high", 10)))
        elif dist == "normal":
            mu = params.get("mu", 5)
            sigma = params.get("sigma", 1)
            return max(1, int(random.gauss(mu, sigma)))
        return 1

    def _sample_magnitude(self, dist: str, params: dict) -> float:
        if dist == "lognormal":
            mu = params.get("mu", 10)
            sigma = params.get("sigma", 1.5)
            return random.lognormvariate(mu, sigma)
        elif dist == "normal":
            mu = params.get("mu", 100000)
            sigma = params.get("sigma", 50000)
            return max(0, random.gauss(mu, sigma))
        elif dist == "uniform":
            low = params.get("low", 10000)
            high = params.get("high", 1000000)
            return random.uniform(low, high)
        return 0.0

    def run(self) -> MonteCarloResult:
        all_losses: list[float] = []
        for scenario in self.scenarios:
            for _ in range(self.iterations):
                freq = self._sample_frequency(scenario.frequency_dist,
                                              scenario.frequency_params)
                total = 0.0
                for _ in range(freq):
                    total += self._sample_magnitude(scenario.magnitude_dist,
                                                    scenario.magnitude_params)
                all_losses.append(total)

        all_losses.sort()
        n = len(all_losses)
        mean = sum(all_losses) / n if n else 0
        median = all_losses[n // 2] if n else 0
        var = sum((x - mean) ** 2 for x in all_losses) / n if n else 1
        std_dev = math.sqrt(var)

        return MonteCarloResult(
            mean=mean, median=median, std_dev=std_dev,
            var_95=all_losses[int(n * 0.95)] if n else 0,
            var_99=all_losses[int(n * 0.99)] if n else 0,
            min_loss=all_losses[0] if n else 0,
            max_loss=all_losses[-1] if n else 0,
            iterations=n, samples=all_losses,
        )


class BusinessImpactAnalyzer:
    """Map technical threats to business impact metrics."""

    def assess(self, threat: str, assets: list[str],
               factors: dict) -> BusinessImpact:
        revenue_per_hour = factors.get("revenue_per_hour", 0)
        regulatory_fine_max = factors.get("regulatory_fine_max", 0)
        customer_count = factors.get("customer_count", 0)
        reputation_days = factors.get("reputation_recovery_days", 30)

        base_hours = self._estimate_recovery_hours(threat)
        revenue_loss = revenue_per_hour * base_hours
        reg_fine = regulatory_fine_max * self._regulatory_probability(threat)
        rep_cost = customer_count * 0.5 * reputation_days
        recovery_cost = base_hours * 500

        return BusinessImpact(
            threat=threat, revenue_loss=revenue_loss,
            regulatory_fine=reg_fine, reputational_cost=rep_cost,
            recovery_cost=recovery_cost, recovery_hours=base_hours,
        )

    def _estimate_recovery_hours(self, threat: str) -> int:
        estimates = {
            "Ransomware": 72, "Data Breach": 48, "DDoS": 8,
            "Insider Threat": 96, "Supply Chain": 120,
        }
        return estimates.get(threat, 24)

    def _regulatory_probability(self, threat: str) -> float:
        probs = {
            "Ransomware": 0.3, "Data Breach": 0.7, "DDoS": 0.05,
            "Insider Threat": 0.4, "Supply Chain": 0.5,
        }
        return probs.get(threat, 0.2)


# ──────────────────────────── Main Engine ─────────────────────

class FAIRAnalyzer:
    """FAIR-based quantitative risk analysis engine."""

    def __init__(self, simulations: int = 10000, seed: int | None = None):
        self.simulations = simulations
        self.seed = seed
        self._scenarios: list[RiskScenario] = []
        self._is_configured = False
        if seed is not None:
            random.seed(seed)

    def configure(self, config: dict) -> None:
        self.simulations = config.get("simulations", self.simulations)
        self.seed = config.get("seed", self.seed)
        self._is_configured = True
        logger.info("FAIR Analyzer configured: %d simulations", self.simulations)

    def run(self) -> dict:
        if not self._is_configured:
            raise RuntimeError("Not configured. Call configure() first.")
        return {"status": "complete", "scenarios_analyzed": len(self._scenarios),
                "simulations": self.simulations}

    def validate(self) -> bool:
        return self._is_configured

    def get_status(self) -> dict:
        return {"configured": self._is_configured,
                "simulations": self.simulations,
                "scenarios": len(self._scenarios)}

    def model_scenario(self, threat_event_frequency: float,
                       vulnerability_rate: float,
                       loss_magnitude_min: float,
                       loss_magnitude_max: float,
                       confidence: float = 0.95) -> FAIRScenario:
        losses = []
        for _ in range(self.simulations):
            tef = random.gauss(threat_event_frequency,
                               threat_event_frequency * 0.1)
            vuln = min(max(vulnerability_rate + random.gauss(0, 0.05), 0), 1)
            lef = max(tef * vuln, 0)
            mag = random.uniform(loss_magnitude_min, loss_magnitude_max)
            losses.append(lef * mag)

        losses.sort()
        n = len(losses)
        ale = sum(losses) / n
        p50 = losses[int(n * 0.50)]
        p95 = losses[int(n * 0.95)]
        p99 = losses[int(n * 0.99)]

        if p95 > 1_000_000:
            rating = "Critical"
        elif p95 > 250_000:
            rating = "High"
        elif p95 > 50_000:
            rating = "Medium"
        else:
            rating = "Low"

        return FAIRScenario(
            name="FAIR Analysis", threat_event_frequency=threat_event_frequency,
            vulnerability_rate=vulnerability_rate,
            loss_magnitude_min=loss_magnitude_min,
            loss_magnitude_max=loss_magnitude_max,
            ale=ale, percentile_50=p50, percentile_95=p95,
            percentile_99=p99, risk_rating=rating, confidence=confidence,
        )


class RiskMatrix:
    """Qualitative risk matrix with configurable scales."""

    def __init__(self, likelihood_scale: int = 5, impact_scale: int = 5,
                 appetite: dict | None = None):
        self.likelihood_scale = likelihood_scale
        self.impact_scale = impact_scale
        self.appetite = appetite or {"high": 15, "medium": 8, "low": 3}
        self._entries: list[RiskMatrixEntry] = []

    def populate(self, risks: list[dict]) -> None:
        self._entries = []
        for r in risks:
            score = r["likelihood"] * r["impact"]
            level = (RiskLevel.CRITICAL if score >= 20 else
                     RiskLevel.HIGH if score >= 12 else
                     RiskLevel.MEDIUM if score >= 6 else
                     RiskLevel.LOW)
            exceeds = score >= self.appetite.get("high", 15)
            self._entries.append(RiskMatrixEntry(
                id=r["id"], title=r["title"],
                likelihood=r["likelihood"], impact=r["impact"],
                risk_level=level, exceeds_appetite=exceeds,
            ))

    def heatmap(self) -> str:
        grid = [["." for _ in range(self.impact_scale)]
                for _ in range(self.likelihood_scale)]
        for e in self._entries:
            row = e.likelihood - 1
            col = e.impact - 1
            if 0 <= row < self.likelihood_scale and 0 <= col < self.impact_scale:
                grid[row][col] = "X"
        lines = ["  Impact →"]
        for row_idx, row in enumerate(reversed(grid)):
            lk = self.likelihood_scale - row_idx
            lines.append(f"  L{lk}: {' '.join(row)}")
        return "\n".join(lines)

    def exceeds_appetite(self) -> list[RiskMatrixEntry]:
        return [e for e in self._entries if e.exceeds_appetite]


class RiskRegister:
    """Risk register with lifecycle management."""

    def __init__(self):
        self._risks: dict[str, RiskScenario] = {}
        self._is_configured = True

    def configure(self, config: dict = None) -> None:
        self._is_configured = True

    def run(self) -> dict:
        return {"status": "complete", "risks_tracked": len(self._risks)}

    def validate(self) -> bool:
        return self._is_configured

    def get_status(self) -> dict:
        return {"configured": True, "risks": len(self._risks)}

    def add_risk(self, id: str, title: str, category: str,
                 inherent_risk_score: int, owner: str = "",
                 treatment: str = "accept", controls: list[str] = None,
                 target_date: str = None) -> RiskScenario:
        likelihood = int(math.ceil(inherent_risk_score ** 0.5))
        impact = int(math.ceil(inherent_risk_score / max(likelihood, 1)))
        scenario = RiskScenario(
            id=id, title=title, description=f"{category}: {title}",
            threat_type=ThreatType.DATA_BREACH, affected_assets=[],
            likelihood=min(likelihood, 5), impact=min(impact, 5),
            treatment=RiskTreatment(treatment), owner=owner,
            target_date=datetime.fromisoformat(target_date) if target_date else None,
        )
        self._risks[id] = scenario
        return scenario

    def update_residual_risk(self, risk_id: str, score: int,
                             rationale: str = "") -> bool:
        if risk_id not in self._risks:
            return False
        r = self._risks[risk_id]
        r.residual_likelihood = int(math.ceil(score ** 0.5))
        r.residual_impact = int(math.ceil(score / max(r.residual_likelihood, 1)))
        return True

    def export_compliance_report(self, format: str = "iso27005") -> dict:
        return {
            "format": format,
            "risks": len(self._risks),
            "critical": sum(1 for r in self._risks.values()
                           if r.risk_level == RiskLevel.CRITICAL),
            "exported_at": datetime.utcnow().isoformat(),
        }


# ──────────────────────────── Demo ────────────────────────────

def main() -> None:
    print("=" * 60)
    print("  Risk Assessment Module — Demo")
    print("=" * 60)

    # FAIR Analysis
    print("\n[1] FAIR Quantitative Analysis:")
    fair = FAIRAnalyzer(simulations=1000, seed=42)
    fair.configure({"simulations": 1000})
    scenario = fair.model_scenario(
        threat_event_frequency=100, vulnerability_rate=0.3,
        loss_magnitude_min=50000, loss_magnitude_max=500000,
    )
    print(f"    Annual Loss Expectancy: ${scenario.ale:,.0f}")
    print(f"    95th percentile: ${scenario.percentile_95:,.0f}")
    print(f"    Risk rating: {scenario.risk_rating}")

    # Risk Matrix
    print("\n[2] Qualitative Risk Matrix:")
    matrix = RiskMatrix(likelihood_scale=5, impact_scale=5)
    risks = [
        {"id": "R001", "title": "SQLi on payment API", "likelihood": 4, "impact": 5},
        {"id": "R002", "title": "Missing MFA on admin", "likelihood": 2, "impact": 3},
        {"id": "R003", "title": "Unencrypted data", "likelihood": 3, "impact": 4},
    ]
    matrix.populate(risks)
    print(matrix.heatmap())
    print(f"    Risks above appetite: {len(matrix.exceeds_appetite())}")

    # Monte Carlo
    print("\n[3] Monte Carlo Simulation:")
    mc = MonteCarloSimulator(iterations=1000, seed=42)
    mc.add_scenario(
        name="Cloud Breach", frequency_dist="poisson",
        frequency_params={"lambda": 2.5}, magnitude_dist="lognormal",
        magnitude_params={"mu": 12, "sigma": 1.5},
    )
    mc_result = mc.run()
    print(f"    Expected Annual Loss: ${mc_result.mean:,.0f}")
    print(f"    Value at Risk (95%): ${mc_result.var_95:,.0f}")
    print(f"    P(> $1M): {mc_result.exceedance_probability(1_000_000):.1%}")

    # Business Impact
    print("\n[4] Business Impact Analysis:")
    bia = BusinessImpactAnalyzer()
    impact = bia.assess(
        threat="Ransomware",
        assets=["payment-system", "customer-db"],
        factors={"revenue_per_hour": 50000, "regulatory_fine_max": 2000000,
                 "customer_count": 100000, "reputation_recovery_days": 90},
    )
    print(f"    Total Impact: ${impact.total_impact:,.0f}")
    print(f"    Revenue Loss: ${impact.revenue_loss:,.0f}")
    print(f"    Recovery Time: {impact.recovery_hours}h")

    # Risk Register
    print("\n[5] Risk Register:")
    register = RiskRegister()
    register.add_risk(id="R001", title="SQLi on payment API",
                      category="AppSec", inherent_risk_score=20,
                      owner="security-team", treatment="mitigate",
                      controls=["WAF", "Parameterized queries"],
                      target_date="2026-08-01")
    register.update_residual_risk("R001", score=4)
    report = register.export_compliance_report()
    print(f"    Risks tracked: {report['risks']}")
    print(f"    Critical: {report['critical']}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
