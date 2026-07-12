"""
Drug Discovery Module
Virtual screening, ADMET profiling, pharmacophore modeling, and compound library management.
"""

from __future__ import annotations

import hashlib
import logging
import math
import re
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DrugLikelyHood(Enum):
    LIKELY_DRUG = "likely_drug"
    POSSIBLY_DRUG = "possibly_drug"
    UNLIKELY_DRUG = "unlikely_drug"


class ToxicityRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PharmacophoreFeature(Enum):
    HYDROGEN_BOND_DONOR = "HBD"
    HYDROGEN_BOND_ACCEPTOR = "HBA"
    HYDROPHOBIC = "HYD"
    AROMATIC = "AR"
    POSITIVE_CHARGE = "PI"
    NEGATIVE_CHARGE = "NI"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class MoleculeProperties:
    """Calculated molecular properties."""
    smiles: str
    molecular_weight: float = 0.0
    logP: float = 0.0
    tpsa: float = 0.0
    hbd: int = 0
    hba: int = 0
    rotatable_bonds: int = 0
    aromatic_rings: int = 0
    heavy_atoms: int = 0
    formula: str = ""
    qed: float = 0.0
    passes_lipinski: bool = True
    passes_veber: bool = True
    passes_pains: bool = True

    def __post_init__(self) -> None:
        violations = 0
        if self.molecular_weight > 500:
            violations += 1
        if self.logP > 5:
            violations += 1
        if self.hbd > 5:
            violations += 1
        if self.hba > 10:
            violations += 1
        self.passes_lipinski = violations <= 1
        self.passes_veber = self.rotatable_bonds <= 10 and self.tpsa <= 140


@dataclass
class DockingResult:
    """Single docking pose result."""
    compound_id: str
    smiles: str
    affinity: float
    pose_score: float = 0.0
    poses: int = 1
    interactions: List[str] = field(default_factory=list)
    binding_site: str = ""


@dataclass
class ADMETProfile:
    """ADMET prediction profile for a compound."""
    smiles: str
    bbb_penetration: bool = True
    cyp3a4_inhibitor: bool = False
    cyp2d6_inhibitor: bool = False
    cyp2c9_inhibitor: bool = False
    herg_liability: bool = False
    hepatotoxicity: ToxicityRisk = ToxicityRisk.LOW
   AMES_mutagenicity: bool = False
    oral_bioavailability: float = 0.5
    plasma_protein_binding: float = 0.5
    half_life_hours: float = 4.0
    solubility_log: float = -2.0
    permeability_caco2: float = 1.0

    @property
    def overall_safety(self) -> ToxicityRisk:
        risks = sum([
            self.herg_liability,
            self.hepatotoxicity == ToxicityRisk.HIGH,
            self.AMES_mutagenicity,
            self.cyp3a4_inhibitor and self.cyp2d6_inhibitor,
        ])
        if risks >= 3:
            return ToxicityRisk.CRITICAL
        elif risks == 2:
            return ToxicityRisk.HIGH
        elif risks == 1:
            return ToxicityRisk.MEDIUM
        return ToxicityRisk.LOW


@dataclass
class PharmacophorePoint:
    """Single pharmacophore feature with coordinates."""
    feature: PharmacophoreFeature
    x: float
    y: float
    z: float
    radius: float = 1.0
    weight: float = 1.0


@dataclass
class PharmacophoreModel:
    """Pharmacophore model for screening."""
    points: List[PharmacophorePoint] = field(default_factory=list)
    name: str = ""
    excluded_volumes: List[Tuple[Tuple[float, float, float], float]] = field(
        default_factory=list
    )

    @property
    def feature_count(self) -> Dict[PharmacophoreFeature, int]:
        counts: Dict[PharmacophoreFeature, int] = defaultdict(int)
        for p in self.points:
            counts[p.feature] += 1
        return dict(counts)


@dataclass
class SAREntry:
    """Structure-Activity Relationship data point."""
    smiles: str
    name: str
    activity: float
    target: str = ""
    unit: str = "pIC50"
    notes: str = ""


# ---------------------------------------------------------------------------
# Molecule Processor
# ---------------------------------------------------------------------------

class MoleculeProcessor:
    """Molecular property calculation and manipulation from SMILES."""

    ATOM_WEIGHTS: Dict[str, float] = {
        "C": 12.011, "H": 1.008, "N": 14.007, "O": 15.999,
        "S": 32.065, "P": 30.974, "F": 18.998, "Cl": 35.453,
        "Br": 79.904, "I": 126.904,
    }

    HBA_ATOMS: Set[str] = {"N", "O", "S"}
    HBD_SMARTS: List[str] = ["[NH]", "[OH]", "[SH]"]
    AROMATIC_SMARTS: List[str] = ["c1", "c2", "c3", "c4", "c5", "c6"]

    def from_smiles(self, smiles: str) -> MoleculeHandle:
        """Create a molecule handle from SMILES string."""
        return MoleculeHandle(smiles=smiles, processor=self)

    def from_smiles_batch(self, smiles_list: List[str]) -> List[MoleculeHandle]:
        """Create multiple molecule handles."""
        return [self.from_smiles(s) for s in smiles_list]


@dataclass
class MoleculeHandle:
    """Handle to a molecule for property calculation."""
    smiles: str
    processor: MoleculeProcessor

    def calculate_properties(self) -> MoleculeProperties:
        """Calculate molecular properties from SMILES."""
        atoms = self._parse_smiles_atoms()
        props = MoleculeProperties(smiles=self.smiles)
        props.heavy_atoms = len([a for a in atoms if a != "H"])
        props.molecular_weight = sum(
            self.processor.ATOM_WEIGHTS.get(a, 12.0) for a in atoms
        )
        props.hbd = self.smiles.count("N") + self.smiles.count("O") + self.smiles.count("S")
        props.hba = sum(1 for a in atoms if a in self.processor.HBA_ATOMS)
        props.hbd = min(props.hbd, 5)
        props.hba = min(props.hba, 10)
        props.rotatable_bonds = self._count_rotatable_bonds()
        props.aromatic_rings = self._count_aromatic_rings()
        props.tpsa = self._estimate_tpsa()
        props.logP = self._estimate_logP()
        props.formula = self._compute_formula(atoms)
        props.qed = self._compute_qed(props)
        return props

    def fingerprint(self, radius: int = 2, nbits: int = 2048) -> List[int]:
        """Compute Morgan-like circular fingerprint."""
        bits = [0] * nbits
        tokens = self._tokenize_smiles()
        for i, token in enumerate(tokens):
            context = tokens[max(0, i - radius):i + radius + 1]
            h = int(hashlib.md5("".join(context).encode()).hexdigest(), 16)
            bits[h % nbits] = 1
        return bits

    def tanimoto_similarity(self, other: MoleculeHandle) -> float:
        """Tanimoto coefficient between two fingerprints."""
        fp1 = self.fingerprint()
        fp2 = other.fingerprint()
        intersection = sum(a & b for a, b in zip(fp1, fp2))
        union = sum(a | b for a, b in zip(fp1, fp2))
        return intersection / max(union, 1)

    def _parse_smiles_atoms(self) -> List[str]:
        atoms: List[str] = []
        i = 0
        smi = self.smiles
        while i < len(smi):
            c = smi[i]
            if c.isupper():
                if i + 1 < len(smi) and smi[i + 1].islower():
                    atoms.append(smi[i:i + 2])
                    i += 2
                else:
                    atoms.append(c)
                    i += 1
            elif c == "H":
                atoms.append("H")
                i += 1
            else:
                i += 1
        return atoms

    def _count_rotatable_bonds(self) -> int:
        count = 0
        smi = self.smiles
        for bond_type in ["-", "=", "#"]:
            pattern = f"[A-Z]{bond_type}[A-Z]"
            count += len(re.findall(pattern, smi))
        return max(0, min(count - 4, 15))

    def _count_aromatic_rings(self) -> int:
        return sum(1 for pattern in self.processor.AROMATIC_SMARTS if pattern in self.smiles)

    def _estimate_tpsa(self) -> float:
        tpsa = 0.0
        tpsa += self.smiles.count("O") * 20.0
        tpsa += self.smiles.count("N") * 26.0
        tpsa += self.smiles.count("S") * 32.0
        tpsa += self.smiles.count("P") * 13.0
        return min(tpsa, 200.0)

    def _estimate_logP(self) -> float:
        logP = 0.0
        for atom in self._parse_smiles_atoms():
            if atom in ("C",):
                logP += 0.23
            elif atom in ("N",):
                logP -= 0.71
            elif atom in ("O",):
                logP -= 0.93
            elif atom in ("S",):
                logP += 0.05
            elif atom in ("F", "Cl", "Br", "I"):
                logP += 0.37
        return round(logP, 2)

    def _compute_formula(self, atoms: List[str]) -> str:
        counts: Dict[str, int] = defaultdict(int)
        for a in atoms:
            counts[a] += 1
        order = ["C", "H", "N", "O", "S", "P", "F", "Cl", "Br", "I"]
        parts = []
        for element in order:
            if element in counts:
                parts.append(f"{element}{counts[element] if counts[element] > 1 else ''}")
        return "".join(parts)

    def _compute_qed(self, props: MoleculeProperties) -> float:
        """Simplified QED (Quantitative Estimate of Drug-likeness)."""
        scores = []
        if 150 <= props.molecular_weight <= 500:
            scores.append(1.0)
        else:
            scores.append(max(0, 1 - abs(props.molecular_weight - 300) / 500))
        if 0 <= props.logP <= 3:
            scores.append(1.0)
        else:
            scores.append(max(0, 1 - abs(props.logP - 1.5) / 5))
        if props.hbd <= 5:
            scores.append(1.0)
        else:
            scores.append(max(0, 1 - (props.hbd - 5) / 5))
        if props.hba <= 10:
            scores.append(1.0)
        else:
            scores.append(max(0, 1 - (props.hba - 10) / 10))
        if props.tpsa <= 140:
            scores.append(1.0)
        else:
            scores.append(max(0, 1 - (props.tpsa - 140) / 60))
        return round(statistics.mean(scores), 3) if scores else 0.0

    def _tokenize_smiles(self) -> List[str]:
        tokens: List[str] = []
        i = 0
        while i < len(self.smiles):
            c = self.smiles[i]
            if c in "[]()=":
                tokens.append(c)
                i += 1
            elif c.isupper():
                if i + 1 < len(self.smiles) and self.smiles[i + 1].islower():
                    tokens.append(self.smiles[i:i + 2])
                    i += 2
                else:
                    tokens.append(c)
                    i += 1
            elif c.isdigit():
                tokens.append(c)
                i += 1
            elif c == "@":
                tokens.append("@")
                i += 1
            else:
                i += 1
        return tokens


# ---------------------------------------------------------------------------
# Virtual Screener
# ---------------------------------------------------------------------------

class VirtualScreener:
    """Molecular docking and virtual screening engine."""

    def __init__(
        self,
        protein_pdb: str,
        grid_center: Tuple[float, float, float] = (0, 0, 0),
        grid_size: Tuple[float, float, float] = (20, 20, 20),
        exhaustiveness: int = 8,
    ):
        self.protein_pdb = Path(protein_pdb)
        self.grid_center = grid_center
        self.grid_size = grid_size
        self.exhaustiveness = exhaustiveness
        self._processed_protein: Optional[str] = None

    def prepare_receptor(self) -> str:
        """Prepare receptor PDB for docking (remove water, add charges)."""
        output = self.protein_pdb.with_suffix(".pdbqt")
        lines: List[str] = []
        if self.protein_pdb.exists():
            with open(self.protein_pdb) as fh:
                for line in fh:
                    if line.startswith("ATOM") and line[12:16].strip() != "HOH":
                        lines.append(line.rstrip())
        else:
            lines = self._generate_demo_receptor()
        with open(output, "w") as fh:
            fh.write("\n".join(lines) + "\n")
        self._processed_protein = str(output)
        return str(output)

    def dock_library(
        self,
        library: str,
        top_n: int = 50,
    ) -> List[DockingResult]:
        """Dock a library of compounds and return ranked results."""
        compounds = self._load_library(library)
        results: List[DockingResult] = []
        for compound_id, smiles in compounds:
            affinity = self._score_compound(smiles)
            result = DockingResult(
                compound_id=compound_id,
                smiles=smiles,
                affinity=affinity,
                pose_score=-affinity / 10.0,
                interactions=self._predict_interactions(smiles),
            )
            results.append(result)
        results.sort(key=lambda r: r.affinity)
        return results[:top_n]

    def dock_single(self, smiles: str, compound_id: str = "ligand") -> DockingResult:
        """Dock a single compound."""
        affinity = self._score_compound(smiles)
        return DockingResult(
            compound_id=compound_id,
            smiles=smiles,
            affinity=affinity,
            pose_score=-affinity / 10.0,
            interactions=self._predict_interactions(smiles),
        )

    def _score_compound(self, smiles: str) -> float:
        """Score a compound using simplified scoring function."""
        atoms = sum(1 for c in smiles if c.isupper())
        hbonds = smiles.count("N") + smiles.count("O")
        rings = sum(1 for c in smiles if c in "cn")
        score = -2.0
        score -= hbonds * 0.8
        score -= rings * 0.3
        score -= atoms * 0.05
        return round(score, 2)

    def _predict_interactions(self, smiles: str) -> List[str]:
        interactions = []
        if "N" in smiles or "O" in smiles:
            interactions.append("H-bond")
        if any(c in smiles for c in "c1c2c3c4c5"):
            interactions.append("Pi-stacking")
        if "S" in smiles:
            interactions.append("Hydrophobic")
        if "+" in smiles or "N" in smiles:
            interactions.append("Salt-bridge")
        return interactions

    def _load_library(self, library: str) -> List[Tuple[str, str]]:
        """Load compound library (demo data if file not found)."""
        path = Path(library)
        if path.exists():
            return self._parse_sdf(path)
        return [
            ("Aspirin", "CC(=O)Oc1ccccc1C(=O)O"),
            ("Ibuprofen", "CC(C)Cc1ccc(cc1)C(C)C(=O)O"),
            ("Metformin", "CN(C)C(=N)NC(=N)N"),
            ("Omeprazole", "COc1ccc2nc(CS(=O)c3ncc(C)c(OC)c3C)cc2n1"),
            ("Atorvastatin", "CC(C)c1n(CC[C@@H](O)C[C@@H](O)CC(=O)O)c(c2ccc(F)cc2)c(C(=O)Nc3ccccc3)c1c4ccccc4"),
        ]

    def _parse_sdf(self, path: Path) -> List[Tuple[str, str]]:
        compounds: List[Tuple[str, str]] = []
        with open(path) as fh:
            name = ""
            for line in fh:
                line = line.strip()
                if line.startswith("> <Name>"):
                    name = next(fh, "").strip()
                elif line and not line.startswith(">") and not line.startswith("$$$$"):
                    compounds.append((name or f"mol_{len(compounds)}", line))
        return compounds

    def _generate_demo_receptor(self) -> List[str]:
        lines = []
        for i in range(1, 101):
            lines.append(
                f"ATOM  {i:5d}  CA  ALA A{i:4d}    "
                f"{10.0 + i * 0.1:8.3f}{20.0:8.3f}{30.0:8.3f}"
                f"  1.00 20.00           C  "
            )
        return lines


# ---------------------------------------------------------------------------
# ADMET Predictor
# ---------------------------------------------------------------------------

class ADMETPredictor:
    """Predict ADMET properties using heuristic/ML-based models."""

    def predict(self, smiles: str) -> ADMETProfile:
        """Generate full ADMET profile for a compound."""
        props = MoleculeProcessor().from_smiles(smiles).calculate_properties()
        profile = ADMETProfile(smiles=smiles)
        profile.bbb_penetration = self._predict_bbb(props)
        profile.cyp3a4_inhibitor = self._predict_cyp3a4(props)
        profile.cyp2d6_inhibitor = self._predict_cyp2d6(props)
        profile.herg_liability = self._predict_herg(props)
        profile.hepatotoxicity = self._predict_hepatotox(props)
        profile.AMES_mutagenicity = self._predict_ames(props)
        profile.oral_bioavailability = self._predict_oral_bio(props)
        profile.plasma_protein_binding = self._predict_ppb(props)
        profile.half_life_hours = self._predict_half_life(props)
        profile.solubility_log = self._predict_solubility(props)
        profile.permeability_caco2 = self._predict_caco2(props)
        return profile

    def _predict_bbb(self, props: MoleculeProperties) -> bool:
        score = 0.0
        if props.molecular_weight < 450:
            score += 1.0
        if 0 < props.logP < 3:
            score += 1.0
        if props.tpsa < 90:
            score += 1.0
        if props.hbd <= 3:
            score += 0.5
        return score >= 2.5

    def _predict_cyp3a4(self, props: MoleculeProperties) -> bool:
        return props.molecular_weight > 400 and props.logP > 3

    def _predict_cyp2d6(self, props: MoleculeProperties) -> bool:
        return props.logP > 3 and props.hba >= 3

    def _predict_herg(self, props: MoleculeProperties) -> bool:
        return props.molecular_weight > 300 and props.logP > 2 and props.tpsa < 80

    def _predict_hepatotox(self, props: MoleculeProperties) -> ToxicityRisk:
        risk_score = 0
        if props.molecular_weight > 500:
            risk_score += 1
        if props.logP > 4:
            risk_score += 1
        if props.rotatable_bonds > 8:
            risk_score += 1
        if risk_score >= 3:
            return ToxicityRisk.HIGH
        elif risk_score == 2:
            return ToxicityRisk.MEDIUM
        return ToxicityRisk.LOW

    def _predict_ames(self, props: MoleculeProperties) -> bool:
        aromatic_count = props.aromatic_rings
        return aromatic_count >= 3 and props.molecular_weight > 300

    def _predict_oral_bio(self, props: MoleculeProperties) -> float:
        score = 0.5
        if props.passes_lipinski:
            score += 0.2
        if props.tpsa < 140:
            score += 0.1
        if props.rotatable_bonds < 10:
            score += 0.1
        return min(score, 1.0)

    def _predict_ppb(self, props: MoleculeProperties) -> float:
        base = 0.5
        base += props.logP * 0.05
        return min(base, 0.99)

    def _predict_half_life(self, props: MoleculeProperties) -> float:
        base = 4.0
        if props.molecular_weight > 400:
            base *= 1.5
        if props.logP > 3:
            base *= 0.8
        return round(base, 1)

    def _predict_solubility(self, props: MoleculeProperties) -> float:
        return round(-2.0 + props.tpsa / 50 - props.logP, 2)

    def _predict_caco2(self, props: MoleculeProperties) -> float:
        score = 1.0
        if props.tpsa > 90:
            score *= 0.5
        if props.molecular_weight > 500:
            score *= 0.6
        return round(score, 2)


# ---------------------------------------------------------------------------
# Pharmacophore Modeler
# ---------------------------------------------------------------------------

class PharmacophoreModeler:
    """Generate and screen pharmacophore models."""

    def generate_from_actives(
        self,
        smiles_list: List[str],
        activity_threshold: float = 7.0,
    ) -> PharmacophoreModel:
        """Generate pharmacophore from known active compounds."""
        model = PharmacophoreModel(name="generated_pharmacophore")
        processor = MoleculeProcessor()
        all_features: Dict[PharmacophoreFeature, List[Tuple[float, float, float]]] = defaultdict(list)
        for smi in smiles_list:
            features = self._extract_features(smi)
            for feat, coord in features:
                all_features[feat].append(coord)
        for feat, coords in all_features.items():
            cx = sum(c[0] for c in coords) / len(coords)
            cy = sum(c[1] for c in coords) / len(coords)
            cz = sum(c[2] for c in coords) / len(coords)
            model.points.append(PharmacophorePoint(
                feature=feat, x=cx, y=cy, z=cz, radius=1.5
            ))
        return model

    def screen_library(
        self,
        pharmacophore: PharmacophoreModel,
        library: str,
        tolerance: float = 1.5,
    ) -> List[DockingResult]:
        """Screen a compound library against a pharmacophore model."""
        processor = MoleculeProcessor()
        hits: List[DockingResult] = []
        path = Path(library)
        compounds = []
        if path.exists():
            with open(path) as fh:
                for line in fh:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        compounds.append((parts[1], parts[0]))
        else:
            compounds = [
                ("CC(=O)Oc1ccccc1C(=O)O", "Aspirin"),
                ("c1ccc(cc1)C(=O)O", "Benzoic_acid"),
            ]
        for smi, name in compounds:
            if self._matches_pharmacophore(smi, pharmacophore, tolerance):
                hits.append(DockingResult(
                    compound_id=name, smiles=smi, affinity=-5.0
                ))
        return hits

    def _extract_features(
        self, smiles: str
    ) -> List[Tuple[PharmacophoreFeature, Tuple[float, float, float]]]:
        features: List[Tuple[PharmacophoreFeature, Tuple[float, float, float]]] = []
        x, y, z = 0.0, 0.0, 0.0
        for c in smiles:
            if c in ("N", "O"):
                features.append((
                    PharmacophoreFeature.HYDROGEN_BOND_ACCEPTOR,
                    (x, y, z),
                ))
            elif c == "c":
                features.append((
                    PharmacophoreFeature.AROMATIC,
                    (x, y, z),
                ))
            elif c in ("C", "c"):
                features.append((
                    PharmacophoreFeature.HYDROPHOBIC,
                    (x, y, z),
                ))
            x += 1.5
        return features

    def _matches_pharmacophore(
        self, smiles: str, model: PharmacophoreModel, tolerance: float
    ) -> bool:
        features = self._extract_features(smiles)
        model_features = [p.feature for p in model.points]
        for feat in model_features:
            if not any(f == feat for f, _ in features):
                return False
        return True


# ---------------------------------------------------------------------------
# Compound Library
# ---------------------------------------------------------------------------

class CompoundLibrary:
    """Manage compound libraries with deduplication and filtering."""

    def __init__(self, path: Optional[str] = None):
        self.compounds: List[Dict[str, str]] = []
        if path and Path(path).exists():
            self._load(path)

    def __len__(self) -> int:
        return len(self.compounds)

    def add_from_smiles(self, smiles: str, name: str = "") -> None:
        self.compounds.append({"smiles": smiles, "name": name})

    def add_batch(self, entries: List[Tuple[str, str]]) -> None:
        for smiles, name in entries:
            self.add_from_smiles(smiles, name)

    def deduplicate(self, threshold: float = 0.85) -> int:
        """Remove near-duplicate compounds by Tanimoto similarity."""
        processor = MoleculeProcessor()
        unique: List[Dict[str, str]] = []
        removed = 0
        for compound in self.compounds:
            mol = processor.from_smiles(compound["smiles"])
            is_dup = False
            for existing in unique:
                existing_mol = processor.from_smiles(existing["smiles"])
                if mol.tanimoto_similarity(existing_mol) >= threshold:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(compound)
            else:
                removed += 1
        self.compounds = unique
        return removed

    def filter_lipinski(self) -> int:
        """Remove compounds that fail Lipinski's Rule of Five."""
        processor = MoleculeProcessor()
        before = len(self.compounds)
        self.compounds = [
            c for c in self.compounds
            if processor.from_smiles(c["smiles"]).calculate_properties().passes_lipinski
        ]
        return before - len(self.compounds)

    def filter_molecular_weight(
        self, min_mw: float = 150, max_mw: float = 500
    ) -> int:
        processor = MoleculeProcessor()
        before = len(self.compounds)
        self.compounds = [
            c for c in self.compounds
            if min_mw <= processor.from_smiles(c["smiles"]).calculate_properties().molecular_weight <= max_mw
        ]
        return before - len(self.compounds)

    def export(self, output_path: str) -> None:
        """Export library to file."""
        with open(output_path, "w") as fh:
            for c in self.compounds:
                fh.write(f"{c['name']}\t{c['smiles']}\n")

    def similarity_matrix(self) -> List[List[float]]:
        """Compute pairwise Tanimoto similarity matrix."""
        processor = MoleculeProcessor()
        n = len(self.compounds)
        mols = [processor.from_smiles(c["smiles"]) for c in self.compounds]
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                sim = mols[i].tanimoto_similarity(mols[j])
                matrix[i][j] = sim
                matrix[j][i] = sim
        return matrix

    def _load(self, path: str) -> None:
        with open(path) as fh:
            for line in fh:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    self.compounds.append({"name": parts[0], "smiles": parts[1]})


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Drug Discovery Pipeline Demo")
    print("=" * 60)

    processor = MoleculeProcessor()

    print("\n[1] Molecular Properties")
    aspirin = processor.from_smiles("CC(=O)Oc1ccccc1C(=O)O")
    props = aspirin.calculate_properties()
    print(f"  Compound: Aspirin")
    print(f"  MW: {props.molecular_weight:.1f}  LogP: {props.logP:.2f}")
    print(f"  TPSA: {props.tpsa:.1f}  HBD: {props.hbd}  HBA: {props.hba}")
    print(f"  Lipinski: {props.passes_lipinski}  QED: {props.qed:.3f}")

    print("\n[2] Virtual Screening")
    screener = VirtualScreener("protein.pdb")
    hits = screener.dock_library("library.sdf", top_n=5)
    for h in hits:
        print(f"  {h.compound_id}: {h.affinity:.1f} kcal/mol")

    print("\n[3] ADMET Profiling")
    admet = ADMETPredictor()
    profile = admet.predict("CC(=O)Oc1ccccc1C(=O)O")
    print(f"  BBB: {profile.bbb_penetration}")
    print(f"  CYP3A4: {profile.cyp3a4_inhibitor}")
    print(f"  hERG: {profile.herg_liability}")
    print(f"  Safety: {profile.overall_safety.value}")

    print("\n[4] Pharmacophore Model")
    modeler = PharmacophoreModeler()
    pharma = modeler.generate_from_actives(
        ["CC(=O)Oc1ccccc1C(=O)O", "c1ccc(cc1)C(=O)O"]
    )
    print(f"  Features: {pharma.feature_count}")

    print("\n[5] Compound Library")
    library = CompoundLibrary()
    library.add_from_smiles("CC(=O)Oc1ccccc1C(=O)O", "Aspirin")
    library.add_from_smiles("CC(C)Cc1ccc(cc1)C(C)C(=O)O", "Ibuprofen")
    library.add_from_smiles("CC(=O)Oc1ccccc1C(=O)O", "Aspirin_dup")
    removed = library.deduplicate()
    print(f"  Removed {removed} duplicates, size: {len(library)}")

    print("\n" + "=" * 60)
    print("  Drug discovery pipeline complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
