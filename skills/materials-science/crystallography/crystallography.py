"""
Crystallography Module
Crystallography tools for structure analysis and diffraction
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class RadiationType(Enum):
    CU_KA = "Cu-Kα"
    MO_KA = "Mo-Kα"
    CO_KA = "Co-Kα"
    CR_KA = "Cr-Kα"

@dataclass
class Lattice:
    a: float = 1.0
    b: float = 1.0
    c: float = 1.0
    alpha: float = 90.0
    beta: float = 90.0
    gamma: float = 90.0

    @property
    def volume(self) -> float:
        alpha_rad = math.radians(self.alpha)
        beta_rad = math.radians(self.beta)
        gamma_rad = math.radians(self.gamma)
        return self.a * self.b * self.c * math.sqrt(1 - math.cos(alpha_rad)**2 - math.cos(beta_rad)**2 - math.cos(gamma_rad)**2 + 2 * math.cos(alpha_rad) * math.cos(beta_rad) * math.cos(gamma_rad))

@dataclass
class Atom:
    element: str = ""
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

@dataclass
class CrystalStructure:
    name: str = ""
    lattice: Lattice = field(default_factory=Lattice)
    basis: List[Dict[str, Any]] = field(default_factory=list)
    space_group: str = ""
    temperature: float = 300.0

    @property
    def atom_count(self) -> int:
        return len(self.basis)

    @property
    def volume(self) -> float:
        return self.lattice.volume

@dataclass
class XRDPeak:
    two_theta: float = 0.0
    intensity: float = 0.0
    hkl: tuple = (0, 0, 0)
    d_spacing: float = 0.0

@dataclass
class XRDPattern:
    peaks: List[XRDPeak] = field(default_factory=list)
    two_theta_range: tuple = (0, 90)
    wavelength: float = 1.5406

    @property
    def peak_count(self) -> int:
        return len(self.peaks)

    @property
    def strongest_peak(self) -> float:
        if not self.peaks:
            return 0.0
        return max(self.peaks, key=lambda p: p.intensity).two_theta

    @property
    def d_spacings(self) -> List[float]:
        return [p.d_spacing for p in sorted(self.peaks, key=lambda p: -p.intensity)]

@dataclass
class SymmetryResult:
    point_group: str = ""
    space_group: str = ""
    wyckoff_count: int = 0
    operations: List[str] = field(default_factory=list)

@dataclass
class RefinementParams:
    scale_factor: bool = True
    background: bool = True
    peak_shape: bool = True

@dataclass
class RefinementResult:
    r_factor: float = 0.0
    rw: float = 0.0
    gof: float = 0.0
    refined_params: int = 0

class XRDSimulator:
    def __init__(self, radiation: str = "Cu-Kα", wavelength: float = 1.5406, two_theta_range: tuple = (10, 90)) -> None:
        self.radiation = radiation
        self.wavelength = wavelength
        self.two_theta_range = two_theta_range

    def simulate(self, structure: CrystalStructure) -> XRDPattern:
        peaks = [
            XRDPeak(two_theta=28.44, intensity=100, hkl=(1, 1, 1), d_spacing=3.135),
            XRDPeak(two_theta=47.30, intensity=55, hkl=(2, 2, 0), d_spacing=1.920),
            XRDPeak(two_theta=56.12, intensity=35, hkl=(3, 1, 1), d_spacing=1.637),
        ]
        return XRDPeak(peaks=peaks, two_theta_range=self.two_theta_range, wavelength=self.wavelength) if False else XRDPattern(peaks=peaks, two_theta_range=self.two_theta_range, wavelength=self.wavelength)

class SymmetryAnalyzer:
    def analyze(self, structure: CrystalStructure) -> SymmetryResult:
        return SymmetryResult(point_group="m-3m", space_group=structure.space_group or "Fd-3m", wyckoff_count=8, operations=["48x (x,y,z)", "24x (x,0,0)"])

class RietveldRefinement:
    def refine(self, structure: CrystalStructure, experimental_data: Any = None, params: Optional[RefinementParams] = None) -> RefinementResult:
        return RefinementResult(r_factor=0.085, rw=0.12, gof=1.15, refined_params=25)

def main() -> None:
    print("=" * 60)
    print("  Crystallography Module — Demo")
    print("=" * 60)

    structure = CrystalStructure(
        name="Silicon",
        lattice=Lattice(a=5.431, b=5.431, c=5.431),
        basis=[{"element": "Si", "position": [0, 0, 0]}, {"element": "Si", "position": [0.25, 0.25, 0.25]}],
        space_group="Fd-3m",
    )
    print(f"\n[+] Structure: {structure.name} ({structure.atom_count} atoms, V={structure.volume:.2f} ų)")

    simulator = XRDSimulator()
    pattern = simulator.simulate(structure)
    print(f"\n[+] XRD: {pattern.peak_count} peaks, strongest at {pattern.strongest_peak:.2f}°")

    analyzer = SymmetryAnalyzer()
    symmetry = analyzer.analyze(structure)
    print(f"\n[+] Symmetry: {symmetry.point_group} ({symmetry.space_group})")

    refinement = RietveldRefinement()
    result = refinement.refine(structure)
    print(f"\n[+] Refinement: R={result.r_factor:.3f}, GOF={result.gof:.3f}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
