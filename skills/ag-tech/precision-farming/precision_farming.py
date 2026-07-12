"""
Precision Farming Module — Variable-rate prescriptions, yield mapping, zone management,
and geospatial analysis for site-specific crop management.
"""

from __future__ import annotations

import csv
import json
import math
import os
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CropType(Enum):
    CORN = "corn"
    SOYBEANS = "soybeans"
    WHEAT = "wheat"
    COTTON = "cotton"
    RICE = "rice"
    SORGHUM = "sorghum"
    BARLEY = "barley"
    SUNFLOWER = "sunflower"


class NutrientType(Enum):
    NITROGEN = "nitrogen"
    PHOSPHORUS = "phosphorus"
    POTASSIUM = "potassium"
    SULFUR = "sulfur"
    LIME = "lime"


class ZoneMethod(Enum):
    KMEANS = "kmeans"
    SOIL_EC = "soil_ec"
    YIELD_HISTORY = "yield_history"
    MANUAL = "manual"


class PrescriptionFormat(Enum):
    SHAPEFILE = "shapefile"
    ISO_XML = "iso_xml"
    GEOJSON = "geojson"
    JOHN_DEERE = "john_deere"
    CLIMATE_FV = "climate_fieldview"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SoilSample:
    """A single soil sample with location and test results."""
    sample_id: str
    latitude: float
    longitude: float
    depth_inches: float
    nitrogen_ppm: float
    phosphorus_ppm: float
    potassium_ppm: float
    ph: float
    organic_matter_pct: float
    cec: float
    zinc_ppm: float = 0.0
    manganese_ppm: float = 0.0
    iron_ppm: float = 0.0
    copper_ppm: float = 0.0
    boron_ppm: float = 0.0
    sulfur_ppm: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "lat": self.latitude,
            "lon": self.longitude,
            "nitrogen": self.nitrogen_ppm,
            "phosphorus": self.phosphorus_ppm,
            "potassium": self.potassium_ppm,
            "ph": self.ph,
            "organic_matter": self.organic_matter_pct,
            "cec": self.cec,
        }


@dataclass
class SoilDataProvider:
    """Provider for soil sample data with statistical analysis."""
    samples: List[SoilSample] = field(default_factory=list)

    @classmethod
    def from_csv(cls, filepath: str) -> SoilDataProvider:
        """Load soil samples from a CSV file."""
        provider = cls()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sample = SoilSample(
                        sample_id=row.get("sample_id", f"S{len(provider.samples)}"),
                        latitude=float(row.get("latitude", 0)),
                        longitude=float(row.get("longitude", 0)),
                        depth_inches=float(row.get("depth", 8)),
                        nitrogen_ppm=float(row.get("nitrogen", 0)),
                        phosphorus_ppm=float(row.get("phosphorus", 0)),
                        potassium_ppm=float(row.get("potassium", 0)),
                        ph=float(row.get("ph", 7.0)),
                        organic_matter_pct=float(row.get("organic_matter", 3.0)),
                        cec=float(row.get("cec", 15.0)),
                    )
                    provider.samples.append(sample)
        except FileNotFoundError:
            pass
        return provider

    @classmethod
    def from_dicts(cls, data: List[Dict[str, Any]]) -> SoilDataProvider:
        provider = cls()
        for d in data:
            provider.samples.append(SoilSample(
                sample_id=d.get("sample_id", ""),
                latitude=d.get("latitude", 0.0),
                longitude=d.get("longitude", 0.0),
                depth_inches=d.get("depth", 8.0),
                nitrogen_ppm=d.get("nitrogen", 0.0),
                phosphorus_ppm=d.get("phosphorus", 0.0),
                potassium_ppm=d.get("potassium", 0.0),
                ph=d.get("ph", 7.0),
                organic_matter_pct=d.get("organic_matter", 3.0),
                cec=d.get("cec", 15.0),
            ))
        return provider

    @property
    def n_range(self) -> Tuple[float, float]:
        vals = [s.nitrogen_ppm for s in self.samples]
        return (min(vals), max(vals)) if vals else (0, 0)

    @property
    def p_range(self) -> Tuple[float, float]:
        vals = [s.phosphorus_ppm for s in self.samples]
        return (min(vals), max(vals)) if vals else (0, 0)

    @property
    def ph_range(self) -> Tuple[float, float]:
        vals = [s.ph for s in self.samples]
        return (min(vals), max(vals)) if vals else (0, 0)

    def get_feature_matrix(self, features: List[str]) -> List[List[float]]:
        """Extract a feature matrix from samples for clustering."""
        matrix = []
        for sample in self.samples:
            row = []
            for feat in features:
                if feat == "nitrogen":
                    row.append(sample.nitrogen_ppm)
                elif feat == "phosphorus":
                    row.append(sample.phosphorus_ppm)
                elif feat == "potassium":
                    row.append(sample.potassium_ppm)
                elif feat == "ph":
                    row.append(sample.ph)
                elif feat == "organic_matter":
                    row.append(sample.organic_matter_pct)
                elif feat == "cec":
                    row.append(sample.cec)
                else:
                    row.append(0.0)
            matrix.append(row)
        return matrix


@dataclass
class ManagementZone:
    """A variable-rate management zone."""
    id: int
    area_acres: float
    avg_n: float
    avg_p: float
    avg_k: float
    avg_ph: float
    avg_om: float
    sample_count: int
    recommended_rate: float = 0.0
    color: str = "#000000"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.id,
            "area_acres": round(self.area_acres, 2),
            "avg_n": round(self.avg_n, 1),
            "avg_p": round(self.avg_p, 1),
            "avg_k": round(self.avg_k, 1),
            "avg_ph": round(self.avg_ph, 2),
            "recommended_rate": round(self.recommended_rate, 1),
        }


@dataclass
class PrescriptionPoint:
    """A point in a variable-rate prescription map."""
    latitude: float
    longitude: float
    rate: float
    zone_id: int
    product: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lat": self.latitude,
            "lon": self.longitude,
            "rate": round(self.rate, 2),
            "zone_id": self.zone_id,
        }


@dataclass
class Prescription:
    """A variable-rate application prescription."""
    crop: CropType
    nutrient: NutrientType
    points: List[PrescriptionPoint] = field(default_factory=list)
    unit: str = "lb/ac"
    product_name: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def total_area_acres(self) -> float:
        return len(self.points) * 0.1  # simplified: 0.1 acre per point

    @property
    def avg_rate(self) -> float:
        if not self.points:
            return 0.0
        return sum(p.rate for p in self.points) / len(self.points)

    @property
    def min_rate(self) -> float:
        return min(p.rate for p in self.points) if self.points else 0.0

    @property
    def max_rate(self) -> float:
        return max(p.rate for p in self.points) if self.points else 0.0

    @property
    def total_cost(self) -> float:
        total_lbs = sum(p.rate * 0.1 for p in self.points)
        return total_lbs * 0.55  # simplified cost per lb

    @property
    def projected_revenue(self) -> float:
        return self.total_area_acres * 180 * 4.50  # simplified

    def export_shapefile(self, path: str) -> None:
        """Export prescription as a shapefile (simplified JSON representation)."""
        data = {
            "type": "PrescriptionMap",
            "crop": self.crop.value,
            "nutrient": self.nutrient.value,
            "unit": self.unit,
            "points": [p.to_dict() for p in self.points],
            "summary": {
                "total_area": self.total_area_acres,
                "avg_rate": self.avg_rate,
                "min_rate": self.min_rate,
                "max_rate": self.max_rate,
            },
        }
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

    def export_iso_xml(self, path: str) -> None:
        """Export prescription as ISO-XML format (simplified)."""
        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_parts.append('<ISO11783_TaskData>')
        xml_parts.append(f'  <Part>{self.product_name}</Part>')
        xml_parts.append(f'  <Unit>{self.unit}</Unit>')
        for pt in self.points:
            xml_parts.append(
                f'  <TreatmentZone><Lat>{pt.latitude}</Lat>'
                f'<Lon>{pt.longitude}</Lon>'
                f'<Rate>{pt.rate}</Rate></TreatmentZone>'
            )
        xml_parts.append('</ISO11783_TaskData>')
        Path(path).write_text("\n".join(xml_parts), encoding="utf-8")

    def export_geojson(self, path: str) -> None:
        """Export prescription as GeoJSON."""
        features = []
        for pt in self.points:
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [pt.longitude, pt.latitude]},
                "properties": {"rate": pt.rate, "zone_id": pt.zone_id, "unit": self.unit},
            })
        geojson = {"type": "FeatureCollection", "features": features}
        Path(path).write_text(json.dumps(geojson, indent=2), encoding="utf-8")


@dataclass
class YieldStatistics:
    """Statistical summary of yield data."""
    mean: float
    median: float
    std_dev: float
    cv: float
    min_yield: float
    max_yield: float
    total_bushels: float
    total_acres: float
    percentile_5: float
    percentile_95: float


@dataclass
class YieldDataPoint:
    """A single yield data point from a yield monitor."""
    latitude: float
    longitude: float
    yield_bu_ac: float
    moisture_pct: float
    timestamp: str = ""
    field_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lat": self.latitude,
            "lon": self.longitude,
            "yield": round(self.yield_bu_ac, 1),
            "moisture": round(self.moisture_pct, 1),
        }


# ---------------------------------------------------------------------------
# Zone Manager
# ---------------------------------------------------------------------------

class ZoneManager:
    """Creates and manages variable-rate management zones."""

    def __init__(self, soil_data: SoilDataProvider):
        self.soil_data = soil_data

    def create_zones(
        self,
        num_zones: int = 5,
        method: ZoneMethod = ZoneMethod.KMEANS,
        features: Optional[List[str]] = None,
    ) -> List[ManagementZone]:
        """Create management zones using the specified method."""
        if not self.soil_data.samples:
            return []

        features = features or ["nitrogen", "phosphorus", "ph", "organic_matter"]
        matrix = self.soil_data.get_feature_matrix(features)

        if method == ZoneMethod.KMEANS:
            assignments = self._kmeans(matrix, num_zones)
        elif method == ZoneMethod.YIELD_HISTORY:
            assignments = self._by_yield_threshold(matrix, num_zones)
        else:
            assignments = [i % num_zones for i in range(len(matrix))]

        zones = self._build_zones(assignments, num_zones)
        return zones

    def _kmeans(self, data: List[List[float]], k: int) -> List[int]:
        """Simplified k-means clustering."""
        if not data:
            return []
        n_features = len(data[0])
        centroids = [list(row) for row in data[:k]]

        for _ in range(10):
            assignments = []
            for point in data:
                distances = [
                    sum((p - c) ** 2 for p, c in zip(point, centroid)) ** 0.5
                    for centroid in centroids
                ]
                assignments.append(distances.index(min(distances)))

            for j in range(k):
                members = [data[i] for i in range(len(data)) if assignments[i] == j]
                if members:
                    centroids[j] = [
                        sum(m[f] for m in members) / len(members)
                        for f in range(n_features)
                    ]

        return assignments

    def _by_yield_threshold(self, data: List[List[float]], k: int) -> List[int]:
        """Create zones based on yield thresholds."""
        assignments = []
        for point in data:
            avg = sum(point) / len(point) if point else 0
            zone = min(int(avg / (max(1, max(max(p) for p in data) / k))), k - 1)
            assignments.append(zone)
        return assignments

    def _build_zones(
        self, assignments: List[int], num_zones: int
    ) -> List[ManagementZone]:
        """Build ManagementZone objects from cluster assignments."""
        zones = []
        for z in range(num_zones):
            indices = [i for i, a in enumerate(assignments) if a == z]
            if not indices:
                continue
            samples = [self.soil_data.samples[i] for i in indices if i < len(self.soil_data.samples)]
            if not samples:
                continue
            zone = ManagementZone(
                id=z + 1,
                area_acres=len(samples) * 2.5,
                avg_n=sum(s.nitrogen_ppm for s in samples) / len(samples),
                avg_p=sum(s.phosphorus_ppm for s in samples) / len(samples),
                avg_k=sum(s.potassium_ppm for s in samples) / len(samples),
                avg_ph=sum(s.ph for s in samples) / len(samples),
                avg_om=sum(s.organic_matter_pct for s in samples) / len(samples),
                sample_count=len(samples),
            )
            zones.append(zone)
        return zones


# ---------------------------------------------------------------------------
# Prescription Engine
# ---------------------------------------------------------------------------

class PrescriptionEngine:
    """Generates variable-rate application prescriptions."""

    # Yield response factors per bushel of corn
    N_FACTOR_LB_BU = 0.8  # 0.8 lb N per bu of corn yield goal
    P_FACTOR_LB_BU = 0.37
    K_FACTOR_LB_BU = 0.27

    def __init__(
        self,
        soil_data: SoilDataProvider,
        zones: List[ManagementZone],
    ):
        self.soil_data = soil_data
        self.zones = zones

    def generate_prescription(
        self,
        crop: CropType,
        nutrient: NutrientType,
        target_yield_bu_ac: float = 180,
        base_rate_lb_ac: float = 120,
        price_per_ton: float = 450.0,
        cost_per_lb_n: float = 0.55,
    ) -> Prescription:
        """Generate a variable-rate prescription based on zone data."""
        prescription = Prescription(
            crop=crop,
            nutrient=nutrient,
            product_name=f"{nutrient.value.title()} - {crop.value.title()}",
        )

        for zone in self.zones:
            zone_rate = self._calculate_zone_rate(
                zone, crop, nutrient, target_yield_bu_ac, base_rate_lb_ac
            )
            zone.recommended_rate = zone_rate
            num_points = max(1, int(zone.area_acres / 0.1))
            for _ in range(num_points):
                lat = 38.0 + random.uniform(-0.01, 0.01)
                lon = -98.0 + random.uniform(-0.01, 0.01)
                prescription.points.append(
                    PrescriptionPoint(
                        latitude=lat,
                        longitude=lon,
                        rate=zone_rate + random.uniform(-5, 5),
                        zone_id=zone.id,
                    )
                )

        return prescription

    def _calculate_zone_rate(
        self,
        zone: ManagementZone,
        crop: CropType,
        nutrient: NutrientType,
        target_yield: float,
        base_rate: float,
    ) -> float:
        """Calculate application rate for a specific zone."""
        if nutrient == NutrientType.NITROGEN:
            soil_credit = zone.avg_n * 0.5  # 50% credit for soil N
            crop_needs = target_yield * self.N_FACTOR_LB_BU
            rate = max(0, crop_needs - soil_credit)
        elif nutrient == NutrientType.PHOSPHORUS:
            soil_credit = zone.avg_p * 0.3
            crop_needs = target_yield * self.P_FACTOR_LB_BU
            rate = max(0, crop_needs - soil_credit)
        elif nutrient == NutrientType.POTASSIUM:
            soil_credit = zone.avg_k * 0.2
            crop_needs = target_yield * self.K_FACTOR_LB_BU
            rate = max(0, crop_needs - soil_credit)
        else:
            rate = base_rate

        return round(rate, 1)


# ---------------------------------------------------------------------------
# Yield Mapper
# ---------------------------------------------------------------------------

class YieldMapper:
    """Import, process, and analyze yield monitor data."""

    def import_yield_file(self, filepath: str) -> List[YieldDataPoint]:
        """Import yield data from CSV."""
        data = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    point = YieldDataPoint(
                        latitude=float(row.get("latitude", 0)),
                        longitude=float(row.get("longitude", 0)),
                        yield_bu_ac=float(row.get("yield", 0)),
                        moisture_pct=float(row.get("moisture", 15)),
                    )
                    data.append(point)
        except FileNotFoundError:
            pass
        return data

    def compute_statistics(self, data: List[YieldDataPoint]) -> YieldStatistics:
        """Compute statistical summary of yield data."""
        if not data:
            return YieldStatistics(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        yields = [d.yield_bu_ac for d in data]
        sorted_yields = sorted(yields)
        n = len(sorted_yields)
        mean = sum(yields) / n
        median = sorted_yields[n // 2]
        variance = sum((y - mean) ** 2 for y in yields) / n
        std_dev = variance ** 0.5
        cv = std_dev / mean if mean > 0 else 0

        return YieldStatistics(
            mean=round(mean, 1),
            median=round(median, 1),
            std_dev=round(std_dev, 1),
            cv=round(cv, 4),
            min_yield=round(min(yields), 1),
            max_yield=round(max(yields), 1),
            total_bushels=round(sum(yields) * 0.1, 0),
            total_acres=round(n * 0.1, 1),
            percentile_5=round(sorted_yields[int(n * 0.05)], 1) if n > 20 else round(min(yields), 1),
            percentile_95=round(sorted_yields[int(n * 0.95)], 1) if n > 20 else round(max(yields), 1),
        )

    def clean_yield_data(
        self,
        data: List[YieldDataPoint],
        min_yield: float = 0,
        max_yield: float = 500,
    ) -> List[YieldDataPoint]:
        """Remove outliers from yield data."""
        return [d for d in data if min_yield <= d.yield_bu_ac <= max_yield]


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the precision farming toolkit."""
    print("Precision Farming Toolkit")
    print("=" * 60)

    # Create sample soil data
    samples = []
    for i in range(50):
        samples.append({
            "sample_id": f"S{i+1:03d}",
            "latitude": 38.0 + random.uniform(-0.005, 0.005),
            "longitude": -98.0 + random.uniform(-0.005, 0.005),
            "nitrogen": random.uniform(20, 80),
            "phosphorus": random.uniform(15, 60),
            "potassium": random.uniform(100, 300),
            "ph": random.uniform(5.5, 7.5),
            "organic_matter": random.uniform(2.0, 5.0),
            "cec": random.uniform(10, 30),
        })

    soil = SoilDataProvider.from_dicts(samples)
    print(f"Loaded {len(soil.samples)} soil samples")
    print(f"N range: {soil.n_range[0]:.0f}-{soil.n_range[1]:.0f} ppm")
    print(f"pH range: {soil.ph_range[0]:.1f}-{soil.ph_range[1]:.1f}")

    # Create management zones
    zone_mgr = ZoneManager(soil_data=soil)
    zones = zone_mgr.create_zones(num_zones=4, features=["nitrogen", "phosphorus", "ph", "organic_matter"])
    print(f"\nCreated {len(zones)} management zones:")
    for z in zones:
        print(f"  Zone {z.id}: {z.area_acres:.1f}ac, N={z.avg_n:.0f}ppm, pH={z.avg_ph:.1f}")

    # Generate prescription
    engine = PrescriptionEngine(soil_data=soil, zones=zones)
    rx = engine.generate_prescription(
        crop=CropType.CORN,
        nutrient=NutrientType.NITROGEN,
        target_yield_bu_ac=180,
    )
    print(f"\nPrescription: {rx.total_area_acres:.1f} acres, avg {rx.avg_rate:.1f} lb/ac")
    print(f"  Min rate: {rx.min_rate:.1f}, Max rate: {rx.max_rate:.1f}")

    # Export
    rx.export_shapefile("rx_nitrogen.json")
    rx.export_geojson("rx_nitrogen.geojson")
    print("Exported: rx_nitrogen.json, rx_nitrogen.geojson")


if __name__ == "__main__":
    main()
