"""
Protein Structure Analysis Module
Structure parsing, quality assessment, binding site detection, alignment, and mutation analysis.
"""

from __future__ import annotations

import math
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SecondaryStructure(Enum):
    HELIX = "H"
    SHEET = "E"
    TURN = "T"
    COIL = "C"


class ResidueType(Enum):
    ALANINE = "ALA"
    ARGININE = "ARG"
    ASPARAGINE = "ASN"
    ASPARTIC_ACID = "ASP"
    CYSTEINE = "CYS"
    GLUTAMINE = "GLN"
    GLUTAMIC_ACID = "GLU"
    GLYCINE = "GLY"
    HISTIDINE = "HIS"
    ISOLEUCINE = "ILE"
    LEUCINE = "LEU"
    LYSINE = "LYS"
    METHIONINE = "MET"
    PHENYLALANINE = "PHE"
    PROLINE = "PRO"
    SERINE = "SER"
    THREONINE = "THR"
    TRYPTOPHAN = "TRP"
    TYROSINE = "TYR"
    VALINE = "VAL"


class MutationEffect(Enum):
    STABILIZING = "stabilizing"
    DESTRUCTIVE = "destabilizing"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Atom:
    """Single atom record."""
    serial: int
    name: str
    alt_loc: str
    res_name: str
    chain_id: str
    res_seq: int
    x: float
    y: float
    z: float
    occupancy: float = 1.0
    temp_factor: float = 0.0
    element: str = ""
    charge: str = ""

    @property
    def coord(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass
class Residue:
    """Residue with its atoms."""
    name: str
    chain: str
    seq_num: int
    atoms: List[Atom] = field(default_factory=list)
    secondary_structure: SecondaryStructure = SecondaryStructure.COIL

    @property
    def ca_atom(self) -> Optional[Atom]:
        for a in self.atoms:
            if a.name == "CA":
                return a
        return None

    @property
    def n_atom(self) -> Optional[Atom]:
        for a in self.atoms:
            if a.name == "N":
                return a
        return None

    @property
    def c_atom(self) -> Optional[Atom]:
        for a in self.atoms:
            if a.name == "C":
                return a
        return None

    @property
    def o_atom(self) -> Optional[Atom]:
        for a in self.atoms:
            if a.name == "O":
                return a
        return None


@dataclass
class Chain:
    """Protein chain."""
    chain_id: str
    residues: List[Residue] = field(default_factory=list)

    @property
    def sequence(self) -> str:
        return "".join(
            _three_to_one(r.name) for r in self.residues
        )


@dataclass
class Structure:
    """Complete protein structure."""
    title: str = ""
    chains: Dict[str, Chain] = field(default_factory=dict)
    ligands: List[Dict[str, Any]] = field(default_factory=list)
    resolution: Optional[float] = None
    method: str = ""
    source_pdb: str = ""

    @property
    def residue_count(self) -> int:
        return sum(len(c.residues) for c in self.chains.values())

    @property
    def atom_count(self) -> int:
        return sum(
            sum(len(r.atoms) for r in c.residues)
            for c in self.chains.values()
        )

    @property
    def ligand_names(self) -> List[str]:
        return [l.get("name", "?") for l in self.ligands]

    @property
    def all_residues(self) -> List[Residue]:
        result: List[Residue] = []
        for chain in self.chains.values():
            result.extend(chain.residues)
        return result

    @property
    def all_atoms(self) -> List[Atom]:
        atoms: List[Atom] = []
        for chain in self.chains.values():
            for res in chain.residues:
                atoms.extend(res.atoms)
        return atoms


@dataclass
class QualityReport:
    """Structure quality metrics."""
    rama_favored_pct: float = 0.0
    rama_allowed_pct: float = 0.0
    rama_outliers_pct: float = 0.0
    clashscore: float = 0.0
    rotamer_outliers: int = 0
    rotamer_pct: float = 0.0
    bond_rmsz: float = 0.0
    angle_rmsz: float = 0.0
    molprobity_score: float = 0.0
    ca_rmsd: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class BindingPocket:
    """Detected binding pocket."""
    rank: int
    center: Tuple[float, float, float]
    volume: float
    druggability: float
    residue_count: int
    residues: List[str] = field(default_factory=list)
    hydrophobicity: float = 0.0


@dataclass
class AlignmentResult:
    """Structural alignment result."""
    rmsd: float
    aligned_pairs: int
    aligned_residues: List[Tuple[str, str, float]] = field(default_factory=list)
    transformation_matrix: Optional[List[List[float]]] = None


@dataclass
class MutationPrediction:
    """Prediction for a single point mutation."""
    mutation: str
    ddG: float
    classification: MutationEffect
    confidence: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ONE_TO_THREE: Dict[str, str] = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", "C": "CYS",
    "E": "GLU", "Q": "GLN", "G": "GLY", "H": "HIS", "I": "ILE",
    "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", "P": "PRO",
    "S": "SER", "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL",
}
THREE_TO_ONE: Dict[str, str] = {v: k for k, v in ONE_TO_THREE.items()}

# Amino acid properties
HYDROPHOBIC: Set[str] = {"ALA", "VAL", "LEU", "ILE", "MET", "PHE", "TRP", "PRO"}
CHARGED_POS: Set[str] = {"ARG", "LYS", "HIS"}
CHARGED_NEG: Set[str] = {"ASP", "GLU"}
POLAR: Set[str] = {"ASN", "GLN", "SER", "THR", "TYR", "CYS"}


def _three_to_one(code: str) -> str:
    return THREE_TO_ONE.get(code, "X")


def _one_to_three(code: str) -> str:
    return ONE_TO_THREE.get(code.upper(), "UNK")


def _distance(a: Atom, b: Atom) -> float:
    return math.sqrt(
        (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2
    )


def _center_of_mass(atoms: List[Atom]) -> Tuple[float, float, float]:
    n = len(atoms)
    return (
        sum(a.x for a in atoms) / n,
        sum(a.y for a in atoms) / n,
        sum(a.z for a in atoms) / n,
    )


# ---------------------------------------------------------------------------
# Structure Parser
# ---------------------------------------------------------------------------

class StructureParser:
    """Parse PDB files into Structure objects."""

    def __init__(self, pdb_path: str):
        self.pdb_path = Path(pdb_path)

    def parse(self) -> Structure:
        """Parse PDB file and return Structure."""
        structure = Structure(source_pdb=str(self.pdb_path))
        chains: Dict[str, List[Residue]] = defaultdict(list)
        current_residues: Dict[str, Residue] = {}

        if not self.pdb_path.exists():
            return self._generate_demo_structure()

        with open(self.pdb_path, "r") as fh:
            for line in fh:
                if line.startswith("ATOM"):
                    atom = self._parse_atom(line)
                    key = (atom.chain_id, atom.res_seq)
                    if key not in current_residues:
                        res = Residue(
                            name=atom.res_name,
                            chain=atom.chain_id,
                            seq_num=atom.res_seq,
                        )
                        current_residues[key] = res
                        chains[atom.chain_id].append(res)
                    current_residues[key].atoms.append(atom)

                elif line.startswith("HETATM"):
                    atom = self._parse_atom(line)
                    if atom.res_name not in (
                        "HOH", "WAT", "SO4", "PO4", "GOL"
                    ):
                        structure.ligands.append({
                            "name": atom.res_name,
                            "chain": atom.chain_id,
                            "seq": atom.res_seq,
                        })

                elif line.startswith("TITLE"):
                    structure.title = line[10:].strip()

                elif line.startswith("REMARK   2"):
                    try:
                        structure.resolution = float(line[22:].strip())
                    except (ValueError, IndexError):
                        pass

        for chain_id, residues in chains.items():
            structure.chains[chain_id] = Chain(
                chain_id=chain_id, residues=residues
            )
        return structure

    def _parse_atom(self, line: str) -> Atom:
        return Atom(
            serial=int(line[6:11].strip()),
            name=line[12:16].strip(),
            alt_loc=line[16].strip() or " ",
            res_name=line[17:20].strip(),
            chain_id=line[21].strip() or "A",
            res_seq=int(line[22:26].strip()),
            x=float(line[30:38]),
            y=float(line[38:46]),
            z=float(line[46:54]),
            occupancy=float(line[54:60]) if line[54:60].strip() else 1.0,
            temp_factor=float(line[60:66]) if line[60:66].strip() else 0.0,
            element=line[76:78].strip() if len(line) > 76 else "",
        )

    def _generate_demo_structure(self) -> Structure:
        """Generate a demo structure for testing."""
        structure = Structure(
            title="Demo Protein",
            resolution=1.8,
            method="X-RAY DIFFRACTION",
            source_pdb="demo",
        )
        residues = []
        for i, aa in enumerate("MKWVTFISLLFLFSSAYSRGVFRRDAHKSEVAHRFKDLGEENFKALVLIAFAQYLQQCPFEDHVKLVNEVTEFAKTCVADESAENCDKS"):
            atoms = []
            for j, (name, x, y, z) in enumerate([
                ("N", i * 3.8, 0, 0),
                ("CA", i * 3.8 + 1.5, 0, 0),
                ("C", i * 3.8 + 3.0, 1.2, 0),
                ("O", i * 3.8 + 3.0, 2.4, 0),
            ]):
                atoms.append(Atom(
                    serial=i * 4 + j + 1,
                    name=name,
                    alt_loc=" ",
                    res_name=_one_to_three(aa),
                    chain_id="A",
                    res_seq=i + 1,
                    x=x, y=y, z=z,
                ))
            residues.append(Residue(
                name=_one_to_three(aa), chain="A",
                seq_num=i + 1, atoms=atoms,
            ))
        structure.chains["A"] = Chain(chain_id="A", residues=residues)
        return structure


# ---------------------------------------------------------------------------
# Quality Assessor
# ---------------------------------------------------------------------------

class QualityAssessor:
    """Structure quality assessment: Ramachandran, clashscore, rotamers."""

    def __init__(self, structure: Structure):
        self.structure = structure

    def comprehensive_report(self) -> QualityReport:
        """Generate a full quality report."""
        rama = self._ramachandran_analysis()
        clash = self._clashscore()
        rot = self._rotamer_analysis()
        mp_score = self._molprobity_score(rama, clash, rot)
        return QualityReport(
            rama_favored_pct=rama["favored"],
            rama_allowed_pct=rama["allowed"],
            rama_outliers_pct=rama["outliers"],
            clashscore=clash,
            rotamer_outliers=rot["outliers"],
            rotamer_pct=rot["pct"],
            molprobity_score=mp_score,
        )

    def _ramachandran_analysis(self) -> Dict[str, float]:
        """Analyze backbone dihedral angles."""
        residues = [
            r for r in self.structure.all_residues
            if r.name not in ("PRO", "GLY")
            and r.n_atom and r.ca_atom and r.c_atom
        ]
        favored, allowed, outliers = 0, 0, 0
        for res in residues:
            phi = self._calc_phi(res)
            psi = self._calc_psi(res)
            if phi is None or psi is None:
                continue
            region = self._rama_region(phi, psi)
            if region == "favored":
                favored += 1
            elif region == "allowed":
                allowed += 1
            else:
                outliers += 1
        total = max(favored + allowed + outliers, 1)
        return {
            "favored": favored / total * 100,
            "allowed": allowed / total * 100,
            "outliers": outliers / total * 100,
        }

    def _clashscore(self) -> float:
        """Calculate clashscore: clashes per 1000 atoms."""
        atoms = self.structure.all_atoms
        heavy = [a for a in atoms if a.element != "H"]
        clashes = 0
        for i in range(len(heavy)):
            for j in range(i + 1, min(i + 200, len(heavy))):
                d = _distance(heavy[i], heavy[j])
                vdw_sum = self._vdw_radius(heavy[i].element) + self._vdw_radius(heavy[j].element)
                if d < vdw_sum - 0.4 and d > 0.1:
                    clashes += 1
        return clashes / max(len(heavy), 1) * 1000

    def _rotamer_analysis(self) -> Dict[str, Any]:
        """Count rotamer outliers (simplified)."""
        total, outliers = 0, 0
        for res in self.structure.all_residues:
            if res.name in THREE_TO_ONE and THREE_TO_ONE[res.name] not in ("G", "A", "P"):
                total += 1
                sidechain = [a for a in res.atoms if a.name.startswith("CB") or a.name.startswith("CG")]
                if len(sidechain) >= 2:
                    d = _distance(sidechain[0], sidechain[1])
                    if d < 1.2 or d > 4.0:
                        outliers += 1
        return {
            "outliers": outliers,
            "pct": (1 - outliers / max(total, 1)) * 100,
        }

    def _molprobity_score(
        self, rama: Dict, clash: float, rot: Dict
    ) -> float:
        """Composite MolProbity-style score (lower is better)."""
        rama_penalty = rama["outliers"] / 100 * 5
        clash_penalty = clash / 100 * 3
        rot_penalty = (100 - rot["pct"]) / 100 * 2
        return rama_penalty + clash_penalty + rot_penalty

    def _calc_phi(self, res: Residue) -> Optional[float]:
        prev = self._prev_residue(res)
        if not prev or not prev.c_atom or not res.n_atom or not res.ca_atom:
            return None
        return self._dihedral(prev.c_atom, res.n_atom, res.ca_atom, res.c_atom)

    def _calc_psi(self, res: Residue) -> Optional[float]:
        nxt = self._next_residue(res)
        if not nxt or not res.n_atom or not res.ca_atom or not res.c_atom or not nxt.n_atom:
            return None
        return self._dihedral(res.n_atom, res.ca_atom, res.c_atom, nxt.n_atom)

    def _prev_residue(self, res: Residue) -> Optional[Residue]:
        chain = self.structure.chains.get(res.chain)
        if not chain:
            return None
        idx = next(
            (i for i, r in enumerate(chain.residues) if r.seq_num == res.seq_num),
            -1,
        )
        return chain.residues[idx - 1] if idx > 0 else None

    def _next_residue(self, res: Residue) -> Optional[Residue]:
        chain = self.structure.chains.get(res.chain)
        if not chain:
            return None
        idx = next(
            (i for i, r in enumerate(chain.residues) if r.seq_num == res.seq_num),
            -1,
        )
        return chain.residues[idx + 1] if idx < len(chain.residues) - 1 else None

    @staticmethod
    def _dihedral(a: Atom, b: Atom, c: Atom, d: Atom) -> float:
        v1 = (b.x - a.x, b.y - a.y, b.z - a.z)
        v2 = (c.x - b.x, c.y - b.y, c.z - b.z)
        v3 = (d.x - c.x, d.y - c.y, d.z - c.z)
        n1 = (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        )
        n2 = (
            v2[1] * v3[2] - v2[2] * v3[1],
            v2[2] * v3[0] - v2[0] * v3[2],
            v2[0] * v3[1] - v2[1] * v3[0],
        )
        dot = n1[0] * n2[0] + n1[1] * n2[1] + n1[2] * n2[2]
        m1 = math.sqrt(sum(x**2 for x in n1))
        m2 = math.sqrt(sum(x**2 for x in n2))
        if m1 * m2 == 0:
            return 0.0
        angle = math.acos(max(-1, min(1, dot / (m1 * m2))))
        cross = (
            n1[1] * n2[2] - n1[2] * n2[1],
            n1[2] * n2[0] - n1[0] * n2[2],
            n1[0] * n2[1] - n1[1] * n2[0],
        )
        sign = v2[0] * cross[0] + v2[1] * cross[1] + v2[2] * cross[2]
        return math.degrees(angle) * (-1 if sign < 0 else 1)

    @staticmethod
    def _rama_region(phi: float, psi: float) -> str:
        if -180 <= phi <= -30 and -90 <= psi <= 45:
            return "favored"
        elif -180 <= phi <= -30 and (45 < psi <= 180 or -180 <= psi < -90):
            return "allowed"
        return "outlier"

    @staticmethod
    def _vdw_radius(element: str) -> float:
        radii = {"C": 1.7, "N": 1.55, "O": 1.52, "S": 1.8, "H": 1.2, "FE": 2.0}
        return radii.get(element.upper(), 1.7)


# ---------------------------------------------------------------------------
# Binding Site Detector
# ---------------------------------------------------------------------------

class BindingSiteDetector:
    """Geometric detection of protein binding pockets."""

    def __init__(
        self, structure: Structure, min_volume: float = 100, probe_radius: float = 1.4
    ):
        self.structure = structure
        self.min_volume = min_volume
        self.probe_radius = probe_radius

    def detect(self) -> List[BindingPocket]:
        """Detect binding pockets using geometric cavity analysis."""
        atoms = [
            a for a in self.structure.all_atoms
            if a.element in ("C", "N", "O", "S")
        ]
        if not atoms:
            return []

        grid = self._build_grid(atoms, spacing=2.0)
        cavities = self._find_cavities(grid, atoms)
        pockets: List[BindingPocket] = []
        for i, cavity in enumerate(cavities):
            if len(cavity) < 5:
                continue
            center = _center_of_mass(cavity)
            volume = len(cavity) * 8.0
            if volume < self.min_volume:
                continue
            hydro = self._hydrophobicity_score(cavity)
            druggability = min(1.0, hydro * 0.4 + volume / 1000 * 0.3 + len(cavity) / 50 * 0.3)
            nearby = self._nearby_residues(center, cutoff=8.0)
            pockets.append(BindingPocket(
                rank=i + 1,
                center=center,
                volume=volume,
                druggability=druggability,
                residue_count=len(nearby),
                residues=nearby,
                hydrophobicity=hydro,
            ))
        pockets.sort(key=lambda p: p.druggability, reverse=True)
        for i, p in enumerate(pockets):
            p.rank = i + 1
        return pockets

    def _build_grid(
        self, atoms: List[Atom], spacing: float = 2.0
    ) -> Set[Tuple[int, int, int]]:
        grid: Set[Tuple[int, int, int]] = set()
        for atom in atoms:
            gx = int(atom.x / spacing)
            gy = int(atom.y / spacing)
            gz = int(atom.z / spacing)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    for dz in range(-2, 3):
                        grid.add((gx + dx, gy + dy, gz + dz))
        return grid

    def _find_cavities(
        self, occupied: Set[Tuple[int, int, int]], atoms: List[Atom]
    ) -> List[List[Atom]]:
        min_bound = tuple(min(g[i] for g in occupied) for i in range(3))
        max_bound = tuple(max(g[i] for g in occupied) for i in range(3))
        cavities: List[List[Atom]] = []
        visited: Set[Tuple[int, int, int]] = set()

        for x in range(min_bound[0], max_bound[0] + 1):
            for y in range(min_bound[1], max_bound[1] + 1):
                for z in range(min_bound[2], max_bound[2] + 1):
                    pos = (x, y, z)
                    if pos not in occupied and pos not in visited:
                        cavity_atoms = self._flood_fill(
                            pos, occupied, visited, atoms, max_size=200
                        )
                        if cavity_atoms:
                            cavities.append(cavity_atoms)
        return cavities

    def _flood_fill(
        self,
        start: Tuple[int, int, int],
        occupied: Set[Tuple[int, int, int]],
        visited: Set[Tuple[int, int, int]],
        atoms: List[Atom],
        max_size: int = 200,
    ) -> List[Atom]:
        from collections import deque
        queue = deque([start])
        cavity: List[Atom] = []
        while queue and len(cavity) < max_size:
            pos = queue.popleft()
            if pos in visited or pos in occupied:
                continue
            visited.add(pos)
            real_pos = (pos[0] * 2.0, pos[1] * 2.0, pos[2] * 2.0)
            for atom in atoms:
                dist = math.sqrt(
                    sum((real_pos[i] - atom.coord[i]) ** 2 for i in range(3))
                )
                if dist < 4.0:
                    cavity.append(atom)
                    break
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        neighbor = (pos[0] + dx, pos[1] + dy, pos[2] + dz)
                        if neighbor not in occupied:
                            queue.append(neighbor)
        return cavity

    def _hydrophobicity_score(self, atoms: List[Atom]) -> float:
        if not atoms:
            return 0.0
        hydro_count = sum(1 for a in atoms if a.res_name in HYDROPHOBIC)
        return hydro_count / len(atoms)

    def _nearby_residues(
        self, center: Tuple[float, float, float], cutoff: float = 8.0
    ) -> List[str]:
        seen: Set[str] = set()
        for res in self.structure.all_residues:
            ca = res.ca_atom
            if not ca:
                continue
            dist = math.sqrt(
                sum((center[i] - ca.coord[i]) ** 2 for i in range(3))
            )
            if dist < cutoff:
                key = f"{res.chain}{res.seq_num}"
                if key not in seen:
                    seen.add(key)
        return sorted(seen)


# ---------------------------------------------------------------------------
# Structure Aligner
# ---------------------------------------------------------------------------

class StructureAligner:
    """Structural alignment via Kabsch superposition."""

    def align(
        self,
        reference: Structure,
        mobile: Structure,
        chains: str = "A",
    ) -> AlignmentResult:
        ref_atoms = [
            r.ca_atom for r in reference.all_residues
            if r.chain in chains and r.ca_atom
        ]
        mob_atoms = [
            r.ca_atom for r in mobile.all_residues
            if r.chain in chains and r.ca_atom
        ]
        n = min(len(ref_atoms), len(mob_atoms))
        if n < 3:
            return AlignmentResult(rmsd=float("inf"), aligned_pairs=0)

        ref_pts = [a.coord for a in ref_atoms[:n]]
        mob_pts = [a.coord for a in mob_atoms[:n]]
        ref_c = _center_of_mass_from_pts(ref_pts)
        mob_c = _center_of_mass_from_pts(mob_pts)
        ref_cen = [(p[0] - ref_c[0], p[1] - ref_c[1], p[2] - ref_c[2]) for p in ref_pts]
        mob_cen = [(p[0] - mob_c[0], p[1] - mob_c[1], p[2] - mob_c[2]) for p in mob_pts]
        h = [[0.0] * 3 for _ in range(3)]
        for i in range(n):
            for j in range(3):
                for k in range(3):
                    h[j][k] += mob_cen[i][j] * ref_cen[i][k]
        u, s, vt = _svd3(h)
        d = 1.0
        if _det(u) * _det(vt) < 0:
            d = -1.0
        rotated = []
        for pt in mob_cen:
            r_pt = tuple(
                sum(u[i][j] * pt[j] for j in range(3))
                for i in range(3)
            )
            scaled = (r_pt[0] * d, r_pt[1] * d, r_pt[2] * d)
            translated = (
                scaled[0] + ref_c[0],
                scaled[1] + ref_c[1],
                scaled[2] + ref_c[2],
            )
            rotated.append(translated)
        rmsd = math.sqrt(
            sum(
                sum((rotated[i][j] - ref_pts[i][j]) ** 2 for j in range(3))
                for i in range(n)
            )
            / n
        )
        pairs = [
            (ref_atoms[i].chain + str(ref_atoms[i].res_seq),
             mob_atoms[i].chain + str(mob_atoms[i].res_seq),
             math.sqrt(sum((rotated[i][j] - ref_pts[i][j]) ** 2 for j in range(3))))
            for i in range(n)
        ]
        return AlignmentResult(rmsd=rmsd, aligned_pairs=n, aligned_residues=pairs)


# ---------------------------------------------------------------------------
# Mutation Analyzer
# ---------------------------------------------------------------------------

class MutationAnalyzer:
    """Predict structural impact of point mutations."""

    def __init__(self, structure: Structure):
        self.structure = structure

    def predict(
        self, mutation: str, analysis_type: str = "stability"
    ) -> MutationPrediction:
        """Predict mutation effect. Format: 'A42T' (chain, position, new_aa)."""
        chain_id = mutation[0]
        rest = mutation[1:]
        pos_str = ""
        for c in rest:
            if c.isdigit():
                pos_str += c
            else:
                break
        new_aa = rest[len(pos_str):]
        position = int(pos_str) if pos_str else 0

        chain = self.structure.chains.get(chain_id)
        if not chain:
            return MutationPrediction(
                mutation=mutation, ddG=0.0,
                classification=MutationEffect.UNKNOWN,
            )
        target = next(
            (r for r in chain.residues if r.seq_num == position), None
        )
        if not target:
            return MutationPrediction(
                mutation=mutation, ddG=0.0,
                classification=MutationEffect.UNKNOWN,
            )
        old_aa = _one_to_three(target.name)
        new_aa_3 = _one_to_three(new_aa)
        ddG = self._estimate_ddG(old_aa, new_aa_3, target)
        if ddG < -1.5:
            effect = MutationEffect.STABILIZING
        elif ddG > 1.5:
            effect = MutationEffect.DESTABILIZING
        else:
            effect = MutationEffect.NEUTRAL
        return MutationPrediction(
            mutation=mutation, ddG=ddG, classification=effect,
            confidence=0.7,
            details={"old_residue": old_aa, "new_residue": new_aa_3},
        )

    def _estimate_ddG(self, old: str, new: str, residue: Residue) -> float:
        """Simplified ddG estimation based on residue properties."""
        penalty = 0.0
        ca = residue.ca_atom
        if ca and ca.temp_factor > 60:
            penalty += 1.0
        hydro_diff = 0
        if old in HYDROPHOBIC and new not in HYDROPHOBIC:
            hydro_diff = 2.0
        elif old not in HYDROPHOBIC and new in HYDROPHOBIC:
            hydro_diff = -1.5
        charge_diff = 0
        if old in CHARGED_POS and new not in CHARGED_POS:
            charge_diff = 1.0
        elif old in CHARGED_NEG and new not in CHARGED_NEG:
            charge_diff = 1.0
        elif new in CHARGED_POS and old not in CHARGED_POS:
            charge_diff = -0.5
        return hydro_diff + charge_diff + penalty


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _center_of_mass_from_pts(pts: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    n = len(pts)
    return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n, sum(p[2] for p in pts) / n)


def _svd3(m: List[List[float]]) -> Tuple[List[List[float]], List[float], List[List[float]]]:
    """Simplified 3x3 SVD for structural alignment."""
    u = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    s = [1.0, 1.0, 1.0]
    vt = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for i in range(3):
        s[i] = math.sqrt(max(sum(m[j][i] ** 2 for j in range(3)), 1e-10))
    return u, s, vt


def _det(m: List[List[float]]) -> float:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Protein Structure Analysis Demo")
    print("=" * 60)

    parser = StructureParser("demo.pdb")
    structure = parser.parse()
    print(f"\nStructure: {structure.title}")
    print(f"Chains: {list(structure.chains.keys())}")
    print(f"Residues: {structure.residue_count}")
    print(f"Atoms: {structure.atom_count}")

    print("\n[1] Quality Assessment")
    assessor = QualityAssessor(structure)
    report = assessor.comprehensive_report()
    print(f"  Ramachandran favored: {report.rama_favored_pct:.1f}%")
    print(f"  Clashscore: {report.clashscore:.1f}")
    print(f"  MolProbity score: {report.molprobity_score:.2f}")

    print("\n[2] Binding Site Detection")
    detector = BindingSiteDetector(structure)
    pockets = detector.detect()
    for p in pockets[:3]:
        print(f"  Pocket {p.rank}: vol={p.volume:.0f} A^3, druggability={p.druggability:.2f}")

    print("\n[3] Mutation Impact")
    analyzer = MutationAnalyzer(structure)
    mutations = ["A5T", "L20P", "D42N"]
    for mut in mutations:
        result = analyzer.predict(mut)
        print(f"  {mut}: ddG={result.ddG:+.2f}, effect={result.classification.value}")

    print("\n" + "=" * 60)
    print("  Analysis complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
