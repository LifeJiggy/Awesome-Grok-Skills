"""
Green IT Module
IT infrastructure sustainability audits, data center PUE optimization,
e-waste tracking, hardware lifecycle management, and carbon footprint reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta, timezone
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums & Constants
# ---------------------------------------------------------------------------

class DeviceStatus(Enum):
    """Lifecycle status of an IT asset."""
    PROCUREMENT = "procurement"
    INVENTORY = "inventory"
    DEPLOYED = "deployed"
    ACTIVE = "active"
    IDLE = "idle"
    DECOMMISSIONED = "decommissioned"
    PENDING_DISPOSITION = "pending_disposition"
    REFURBISHED = "refurbished"
    RECYCLED = "recycled"
    DISPOSED = "disposed"
    DONATED = "donated"


class DispositionMethod(Enum):
    """How decommissioned equipment is handled."""
    CERTIFIED_RECYCLER = "certified_recycler"
    REFURBISHMENT = "refurbishment"
    DONATION = "donation"
    TRADE_IN = "trade_in"
    MANUFACTURER_TAKEBACK = "manufacturer_takeback"
    HAZARDOUS_DISPOSAL = "hazardous_disposal"
    ASSET_RECOVERY = "asset_recovery"


class EPEATRating(Enum):
    """EPEAT environmental performance tiers."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


class EnergyStarStatus(Enum):
    """Energy Star compliance status."""
    CERTIFIED = "certified"
    PENDING = "pending"
    NOT_CERTIFIED = "not_certified"
    EXEMPT = "exempt"


class AuditSeverity(Enum):
    """Severity of findings in an IT sustainability audit."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class PUEMeasurement:
    """A single PUE measurement with breakdown."""
    timestamp: datetime
    total_power_kw: float
    it_equipment_power_kw: float
    cooling_power_kw: float
    lighting_power_kw: float
    other_power_kw: float

    @property
    def pue(self) -> float:
        if self.it_equipment_power_kw <= 0:
            return float("inf")
        return self.total_power_kw / self.it_equipment_power_kw

    @property
    def overhead_power_kw(self) -> float:
        return self.total_power_kw - self.it_equipment_power_kw

    @property
    def cooling_percentage(self) -> float:
        if self.total_power_kw <= 0:
            return 0.0
        return self.cooling_power_kw / self.total_power_kw * 100


@dataclass
class PUEAuditResult:
    """Results of a PUE optimization audit."""
    current_pue: float
    target_pue: float
    wasted_power_kw: float
    annual_excess_cost_usd: float
    annual_excess_carbon_kg: float
    recommendations: list[str]
    free_cooling_hours_per_year: int = 0
    hot_cold_aisle_compliant: bool = False


@dataclass
class EWasteAsset:
    """An IT asset tracked through its lifecycle."""
    asset_tag: str
    device_type: str
    manufacturer: str
    model: str
    serial_number: str = ""
    purchase_date: str = ""
    purchase_cost_usd: float = 0.0
    weight_kg: float = 0.0
    hazardous_materials: list[str] = field(default_factory=list)
    status: DeviceStatus = DeviceStatus.PROCUREMENT
    deployment_date: Optional[str] = None
    decommission_date: Optional[str] = None
    expected_lifespan_years: int = 5
    current_location: str = "data-center"
    disposal_method: Optional[DispositionMethod] = None
    recycler: Optional[str] = None
    recovery_percent: float = 0.0

    @property
    def age_years(self) -> float:
        if not self.purchase_date:
            return 0.0
        purchase = datetime.strptime(self.purchase_date, "%Y-%m-%d")
        return (datetime.now() - purchase).days / 365.25

    @property
    def is_end_of_life(self) -> bool:
        return self.age_years >= self.expected_lifespan_years

    @property
    def has_hazardous_materials(self) -> bool:
        return len(self.hazardous_materials) > 0

    @property
    def recyclable_weight_kg(self) -> float:
        if self.has_hazardous_materials:
            return self.weight_kg * 0.7  # 30% hazardous fraction
        return self.weight_kg * 0.95


@dataclass
class DeviceDisposition:
    """Disposition record for a decommissioned device."""
    asset_tag: str
    method: DispositionMethod
    recycler: str
    date: str
    weight_kg: float
    recovered_weight_kg: float
    hazardous_weight_kg: float
    certificate_number: str = ""
    notes: str = ""


@dataclass
class CarbonFootprintResult:
    """Calculated IT carbon footprint."""
    scope2_kgCO2: float
    embodied_kgCO2: float
    scope3_kgCO2: float
    total_kgCO2: float
    breakdown: dict[str, float] = field(default_factory=dict)

    @property
    def total_tonnesCO2(self) -> float:
        return self.total_kgCO2 / 1000.0

    @property
    def per_server_kgCO2(self) -> float:
        return self.total_kgCO2  # Caller divides by server count


@dataclass
class ProcurementScore:
    """Green procurement score for a hardware product."""
    name: str
    epeat_score: float
    energy_star_score: float
    recycled_content_score: float
    packaging_score: float
    total_score: float
    rating: str

    def __post_init__(self):
        if self.total_score >= 80:
            self.rating = "Excellent"
        elif self.total_score >= 60:
            self.rating = "Good"
        elif self.total_score >= 40:
            self.rating = "Fair"
        else:
            self.rating = "Poor"


@dataclass
class AuditFinding:
    """A finding from an IT sustainability audit."""
    category: str
    severity: AuditSeverity
    title: str
    description: str
    recommendation: str
    estimated_savings_kwh: float = 0.0
    estimated_savings_usd: float = 0.0


# ---------------------------------------------------------------------------
# Data Center Auditor
# ---------------------------------------------------------------------------

class DataCenterAuditor:
    """
    Audits data center power usage, cooling efficiency, and environmental impact.
    Produces PUE measurements, identifies optimization opportunities, and tracks
    improvement over time.
    """

    # Industry benchmarks by climate zone
    PUE_TARGETS = {
        "cold": 1.10,    # Nordic, Canada
        "temperate": 1.25,  # Central US, Western Europe
        "warm": 1.40,    # Southern US, Mediterranean
        "tropical": 1.60,  # Southeast Asia, equatorial
    }

    def __init__(self, name: str, climate_zone: str = "temperate"):
        self.name = name
        self.climate_zone = climate_zone
        self._measurements: list[PUEMeasurement] = []
        self._target_pue = self.PUE_TARGETS.get(climate_zone, 1.25)

    def record_measurement(
        self,
        total_power_kw: float,
        it_equipment_power_kw: float,
        cooling_power_kw: float,
        lighting_power_kw: float = 5.0,
        other_power_kw: float = 10.0
    ) -> PUEMeasurement:
        """Record a power measurement with component breakdown."""
        if it_equipment_power_kw <= 0:
            raise ValueError("IT equipment power must be positive")
        if total_power_kw < it_equipment_power_kw:
            raise ValueError("Total power cannot be less than IT equipment power")

        measurement = PUEMeasurement(
            timestamp=datetime.now(timezone.utc),
            total_power_kw=total_power_kw,
            it_equipment_power_kw=it_equipment_power_kw,
            cooling_power_kw=cooling_power_kw,
            lighting_power_kw=lighting_power_kw,
            other_power_kw=other_power_kw
        )
        self._measurements.append(measurement)
        return measurement

    def calculate_pue(self) -> PUEAuditResult:
        """Calculate PUE and generate audit recommendations."""
        if not self._measurements:
            raise ValueError("No measurements recorded")

        latest = self._measurements[-1]
        pue = latest.pue
        wasted = latest.overhead_power_kw

        # Annualize
        annual_hours = 8760
        electricity_rate = 0.10  # $/kWh
        excess_kwh = wasted * annual_hours
        annual_cost = excess_kwh * electricity_rate
        carbon = excess_kwh * 0.4  # 400g CO2/kWh average

        recommendations = []
        if latest.cooling_percentage > 40:
            recommendations.append(
                "Cooling exceeds 40% of total power. Consider free cooling, "
                "hot/cold aisle containment, or liquid cooling."
            )
        if pue > self._target_pue:
            recommendations.append(
                f"Current PUE ({pue:.2f}) exceeds target ({self._target_pue:.2f})."
            )
        if pue > 1.5:
            recommendations.append(
                "PUE > 1.5 indicates severe inefficiency. Prioritize airflow management "
                "and check for recirculation hotspots."
            )
        if latest.lighting_power_kw > 20:
            recommendations.append(
                "Lighting power is high. Consider LED replacement and motion-sensor controls."
            )

        return PUEAuditResult(
            current_pue=round(pue, 3),
            target_pue=self._target_pue,
            wasted_power_kw=round(wasted, 2),
            annual_excess_cost_usd=round(annual_cost, 2),
            annual_excess_carbon_kg=round(carbon, 1),
            recommendations=recommendations
        )

    def trend_analysis(self) -> dict:
        """Analyze PUE trend across recorded measurements."""
        if len(self._measurements) < 2:
            return {"trend": "insufficient_data", "measurements": len(self._measurements)}

        pue_values = [m.pue for m in self._measurements]
        first_half = sum(pue_values[:len(pue_values)//2]) / (len(pue_values)//2)
        second_half = sum(pue_values[len(pue_values)//2:]) / (len(pue_values) - len(pue_values)//2)

        trend = "improving" if second_half < first_half else "degrading" if second_half > first_half else "stable"
        return {
            "trend": trend,
            "first_half_avg_pue": round(first_half, 3),
            "second_half_avg_pue": round(second_half, 3),
            "change_percent": round((second_half - first_half) / first_half * 100, 2),
            "measurements": len(self._measurements)
        }

    def zombie_server_estimate(self, total_servers: int, utilization_threshold: float = 0.05) -> dict:
        """Estimate zombie (idle) server count based on utilization patterns."""
        # Industry data: 15-30% of servers in typical DC are zombies
        zombie_percent = 0.22  # Conservative estimate
        zombie_count = int(total_servers * zombie_percent)
        power_per_server = 250  # Watts average
        zombie_power_kw = zombie_count * power_per_server / 1000
        annual_kwh = zombie_power_kw * 8760

        return {
            "total_servers": total_servers,
            "estimated_zombies": zombie_count,
            "zombie_power_kw": round(zombie_power_kw, 1),
            "annual_waste_kwh": round(annual_kwh, 0),
            "annual_waste_usd": round(annual_kwh * 0.10, 2),
            "recommendation": f"Decommission ~{zombie_count} idle servers to save "
                              f"${annual_kwh * 0.10:,.0f}/year"
        }


# ---------------------------------------------------------------------------
# E-Waste Tracker
# ---------------------------------------------------------------------------

class EWasteTracker:
    """
    Tracks IT equipment through its full lifecycle from procurement to
    responsible end-of-life disposition with chain-of-custody documentation.
    """

    def __init__(self):
        self._assets: dict[str, EWasteAsset] = {}
        self._dispositions: list[DeviceDisposition] = []

    def register_device(
        self,
        asset_tag: str,
        device_type: str,
        manufacturer: str,
        model: str,
        serial_number: str = "",
        purchase_date: str = "",
        weight_kg: float = 0.0,
        hazardous_materials: list[str] | None = None,
        purchase_cost_usd: float = 0.0
    ) -> EWasteAsset:
        """Register a new IT asset for lifecycle tracking."""
        if asset_tag in self._assets:
            raise ValueError(f"Asset {asset_tag} already registered")

        asset = EWasteAsset(
            asset_tag=asset_tag,
            device_type=device_type,
            manufacturer=manufacturer,
            model=model,
            serial_number=serial_number,
            purchase_date=purchase_date,
            weight_kg=weight_kg,
            hazardous_materials=hazardous_materials or [],
            purchase_cost_usd=purchase_cost_usd,
            status=DeviceStatus.INVENTORY
        )
        self._assets[asset_tag] = asset
        return asset

    def update_status(self, asset_tag: str, status: str, reason: str = "") -> None:
        """Update the lifecycle status of an asset."""
        if asset_tag not in self._assets:
            raise KeyError(f"Asset {asset_tag} not found")

        asset = self._assets[asset_tag]
        new_status = DeviceStatus(status)
        asset.status = new_status

        if new_status == DeviceStatus.DEPLOYED:
            asset.deployment_date = date.today().isoformat()
        elif new_status == DeviceStatus.DECOMMISSIONED:
            asset.decommission_date = date.today().isoformat()

    def schedule_disposition(
        self,
        asset_tag: str,
        method: str,
        recycler: str,
        expected_recovery_percent: float = 85.0
    ) -> DeviceDisposition:
        """Schedule end-of-life disposition for a device."""
        if asset_tag not in self._assets:
            raise KeyError(f"Asset {asset_tag} not found")

        asset = self._assets[asset_tag]
        asset.status = DeviceStatus.PENDING_DISPOSITION
        asset.disposal_method = DispositionMethod(method)
        asset.recycler = recycler
        asset.recovery_percent = expected_recovery_percent

        disposition = DeviceDisposition(
            asset_tag=asset_tag,
            method=DispositionMethod(method),
            recycler=recycler,
            date=date.today().isoformat(),
            weight_kg=asset.weight_kg,
            recovered_weight_kg=round(asset.weight_kg * expected_recovery_percent / 100, 2),
            hazardous_weight_kg=sum(
                asset.weight_kg * 0.05 for _ in asset.hazardous_materials
            )
        )
        self._dispositions.append(disposition)
        self.update_status(asset_tag, "recycled")
        return disposition

    def fleet_summary(self) -> dict:
        """Generate fleet-level summary statistics."""
        total_weight = sum(a.weight_kg for a in self._assets.values())
        eol_count = sum(1 for a in self._assets.values() if a.is_end_of_life)
        deployed = sum(1 for a in self._assets.values() if a.status == DeviceStatus.ACTIVE)
        hazardous = [a for a in self._assets.values() if a.has_hazardous_materials]
        total_recovered = sum(d.recovered_weight_kg for d in self._dispositions)

        return {
            "total_assets": len(self._assets),
            "deployed": deployed,
            "end_of_life": eol_count,
            "total_weight_kg": round(total_weight, 1),
            "hazardous_count": len(hazardous),
            "total_dispositions": len(self._dispositions),
            "total_recovered_kg": round(total_recovered, 1),
            "recovery_rate_percent": round(
                total_recovered / max(total_weight, 1) * 100, 1
            )
        }

    def get_asset(self, asset_tag: str) -> EWasteAsset:
        """Retrieve an asset by its tag."""
        if asset_tag not in self._assets:
            raise KeyError(f"Asset {asset_tag} not found")
        return self._assets[asset_tag]


# ---------------------------------------------------------------------------
# Carbon Footprint Calculator
# ---------------------------------------------------------------------------

class CarbonFootprintCalculator:
    """
    Calculates IT department carbon footprint across Scope 2 (electricity),
    embodied carbon, and Scope 3 (supply chain) categories.
    """

    def __init__(self):
        self._energy_sources: list[dict] = []
        self._equipment: list[dict] = []
        self._scope3_categories: list[dict] = []

    def add_energy_source(
        self,
        name: str,
        annual_kwh: float,
        grid_carbon_intensity: float = 400.0,
        pue: float = 1.2
    ) -> None:
        """Add an electricity source with its carbon intensity."""
        self._energy_sources.append({
            "name": name,
            "annual_kwh": annual_kwh,
            "grid_carbon_intensity": grid_carbon_intensity,
            "pue": pue
        })

    def add_equipment_embodied(
        self,
        category: str,
        count: int,
        embodied_carbon_kg: float,
        expected_lifespan_years: float = 5.0,
        current_age_years: float = 2.5
    ) -> None:
        """Add equipment with embodied carbon information."""
        self._equipment.append({
            "category": category,
            "count": count,
            "embodied_carbon_kg": embodied_carbon_kg,
            "expected_lifespan_years": expected_lifespan_years,
            "current_age_years": current_age_years
        })

    def add_scope3(
        self,
        category: str,
        annual_cost_usd: float,
        emission_factor_kg_per_usd: float = 0.1
    ) -> None:
        """Add a Scope 3 emission source."""
        self._scope3_categories.append({
            "category": category,
            "annual_cost_usd": annual_cost_usd,
            "emission_factor_kg_per_usd": emission_factor_kg_per_usd
        })

    def compute(self) -> CarbonFootprintResult:
        """Compute total carbon footprint with category breakdown."""
        breakdown = {}

        # Scope 2: Electricity
        scope2 = 0.0
        for source in self._energy_sources:
            facility_kwh = source["annual_kwh"] * source["pue"]
            source_carbon = facility_kwh * source["grid_carbon_intensity"] / 1000.0
            scope2 += source_carbon
            breakdown[f"electricity_{source['name']}"] = round(source_carbon, 1)

        # Embodied carbon (amortized)
        embodied = 0.0
        for equip in self._equipment:
            total_embodied = equip["count"] * equip["embodied_carbon_kg"]
            amortization = equip["current_age_years"] / equip["expected_lifespan_years"]
            amortized = total_embodied * min(amortization, 1.0)
            embodied += amortized
            breakdown[f"embodied_{equip['category']}"] = round(amortized, 1)

        # Scope 3: Supply chain
        scope3 = 0.0
        for cat in self._scope3_categories:
            cat_carbon = cat["annual_cost_usd"] * cat["emission_factor_kg_per_usd"]
            scope3 += cat_carbon
            breakdown[f"scope3_{cat['category']}"] = round(cat_carbon, 1)

        total = scope2 + embodied + scope3

        return CarbonFootprintResult(
            scope2_kgCO2=round(scope2, 1),
            embodied_kgCO2=round(embodied, 1),
            scope3_kgCO2=round(scope3, 1),
            total_kgCO2=round(total, 1),
            breakdown=breakdown
        )


# ---------------------------------------------------------------------------
# Green Procurement Scorer
# ---------------------------------------------------------------------------

class GreenProcurementScorer:
    """
    Scores hardware products against environmental procurement criteria
    including EPEAT, Energy Star, recycled content, and packaging.
    """

    # Scoring weights
    WEIGHTS = {
        "epeat": 35.0,
        "energy_star": 20.0,
        "recycled_content": 25.0,
        "packaging": 10.0,
        "other": 10.0
    }

    EPEAT_SCORES = {
        "gold": 100.0,
        "silver": 65.0,
        "bronze": 35.0,
        "none": 0.0
    }

    def score_products(self, products: list[dict]) -> list[ProcurementScore]:
        """Score a list of products and return ranked results."""
        scores = []
        for product in products:
            epeat = self.EPEAT_SCORES.get(product.get("epeat", "none"), 0.0)
            energy_star = 100.0 if product.get("energy_star", False) else 0.0
            recycled = min(100.0, product.get("recycled_content", 0) * 2.86)
            packaging = 100.0 if product.get("packaging_recyclable", False) else 30.0
            other = product.get("additional_score", 50.0)

            total = (
                epeat * self.WEIGHTS["epeat"] / 100 +
                energy_star * self.WEIGHTS["energy_star"] / 100 +
                recycled * self.WEIGHTS["recycled_content"] / 100 +
                packaging * self.WEIGHTS["packaging"] / 100 +
                other * self.WEIGHTS["other"] / 100
            )

            scores.append(ProcurementScore(
                name=product.get("name", "Unknown"),
                epeat_score=round(epeat * self.WEIGHTS["epeat"] / 100, 1),
                energy_star_score=round(energy_star * self.WEIGHTS["energy_star"] / 100, 1),
                recycled_content_score=round(recycled * self.WEIGHTS["recycled_content"] / 100, 1),
                packaging_score=round(packaging * self.WEIGHTS["packaging"] / 100, 1),
                total_score=round(total, 1),
                rating=""
            ))
        return sorted(scores, key=lambda s: s.total_score, reverse=True)

    def recommend(self, scores: list[ProcurementScore], budget_usd: float = 0.0) -> dict:
        """Provide a procurement recommendation based on scores."""
        if not scores:
            return {"recommendation": "No products to evaluate"}

        best = scores[0]
        return {
            "recommended_product": best.name,
            "score": best.total_score,
            "rating": best.rating,
            "rationale": f"Highest green procurement score ({best.total_score}/100) "
                         f"with {best.rating} rating across all environmental criteria."
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    """Demonstrate Green IT capabilities."""
    print("=" * 60)
    print("Green IT Module Demo")
    print("=" * 60)

    # 1. Data Center PUE Audit
    print("\n--- Data Center PUE Audit ---")
    auditor = DataCenterAuditor(name="DC-East", climate_zone="temperate")
    for _ in range(5):
        import random
        auditor.record_measurement(
            total_power_kw=500 + random.uniform(-20, 20),
            it_equipment_power_kw=320 + random.uniform(-10, 10),
            cooling_power_kw=120 + random.uniform(-5, 5),
            lighting_power_kw=10,
            other_power_kw=50
        )
    result = auditor.calculate_pue()
    print(f"  Current PUE: {result.current_pue}")
    print(f"  Target PUE: {result.target_pue}")
    print(f"  Wasted power: {result.wasted_power_kw:.1f} kW")
    print(f"  Annual excess cost: ${result.annual_excess_cost_usd:,.0f}")
    print(f"  Annual excess carbon: {result.annual_excess_carbon_kg:.0f} kg CO2")
    for rec in result.recommendations[:2]:
        print(f"  > {rec}")

    # 2. E-Waste Tracking
    print("\n--- E-Waste Tracking ---")
    tracker = EWasteTracker()
    devices = [
        ("SRV-001", "server", "Dell", "PowerEdge R750", 28.5, ["lead_solder"]),
        ("SRV-002", "server", "Dell", "PowerEdge R750", 28.5, []),
        ("SW-001", "switch", "Cisco", "C9300", 5.2, []),
        ("LAP-001", "laptop", "Lenovo", "ThinkPad T14", 1.4, []),
    ]
    for tag, dtype, mfr, model, weight, hazards in devices:
        tracker.register_device(
            asset_tag=tag, device_type=dtype, manufacturer=mfr,
            model=model, weight_kg=weight, hazardous_materials=hazards,
            purchase_date="2022-06-15", purchase_cost_usd=3000 if dtype == "server" else 500
        )
        tracker.update_status(tag, "deployed")

    tracker.update_status("SRV-001", "decommissioned")
    tracker.schedule_disposition("SRV-001", method="certified_recycler", recycler="Dell Reconnect")
    summary = tracker.fleet_summary()
    print(f"  Total assets: {summary['total_assets']}")
    print(f"  Deployed: {summary['deployed']}")
    print(f"  End of life: {summary['end_of_life']}")
    print(f"  Total weight: {summary['total_weight_kg']:.1f} kg")
    print(f"  Recovery rate: {summary['recovery_rate_percent']:.1f}%")

    # 3. Carbon Footprint
    print("\n--- IT Carbon Footprint ---")
    calc = CarbonFootprintCalculator()
    calc.add_energy_source("DC-East", 4_380_000, 350.0, 1.35)
    calc.add_equipment_embodied("servers", 120, 850.0, 5.0, 2.5)
    calc.add_scope3("cloud_services", 250_000, 0.12)
    calc.add_scope3("software_licenses", 80_000, 0.08)
    fp = calc.compute()
    print(f"  Scope 2: {fp.scope2_kgCO2:,.0f} kg CO2eq")
    print(f"  Embodied: {fp.embodied_kgCO2:,.0f} kg CO2eq")
    print(f"  Scope 3: {fp.scope3_kgCO2:,.0f} kg CO2eq")
    print(f"  Total: {fp.total_kgCO2:,.0f} kg CO2eq ({fp.total_tonnesCO2:.1f} tonnes)")

    # 4. Green Procurement
    print("\n--- Green Procurement Scoring ---")
    scorer = GreenProcurementScorer()
    products = [
        {"name": "Dell PowerEdge R760", "epeat": "gold", "energy_star": True,
         "recycled_content": 35, "packaging_recyclable": True},
        {"name": "HPE ProLiant DL380", "epeat": "silver", "energy_star": True,
         "recycled_content": 20, "packaging_recyclable": True},
        {"name": "Lenovo ThinkSystem SR650", "epeat": "bronze", "energy_star": False,
         "recycled_content": 15, "packaging_recyclable": False},
    ]
    scores = scorer.score_products(products)
    for s in scores:
        print(f"  {s.name}: {s.total_score:.1f}/100 ({s.rating})")
    rec = scorer.recommend(scores)
    print(f"  Recommendation: {rec['recommended_product']} — {rec['rationale']}")

    print("\n" + "=" * 60)
    print("Demo complete.")


if __name__ == "__main__":
    main()
