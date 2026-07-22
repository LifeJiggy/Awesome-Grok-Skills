---
name: "drug-discovery"
category: "bioinformatics"
version: "2.0.0"
tags: ["bioinformatics", "drug-discovery", "virtual-screening", "ADMET", "pharmacophore"]
---

# Drug Discovery

## Overview

The Drug Discovery module provides a computational toolkit for the early stages of pharmaceutical research, covering target identification, virtual screening, lead optimization, and ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) profiling. It integrates molecular docking, pharmacophore modeling, QSAR (Quantitative Structure-Activity Relationship), molecular property calculation, and compound library management.

This module is designed for computational chemists, medicinal chemists, and bioinformaticians working on drug design projects. It supports both structure-based drug design (SBDD) using protein crystal structures and ligand-based approaches when only known active compounds are available.

## Core Capabilities

- **Molecular Property Calculation**: Lipinski's Rule of Five, TPSA, rotatable bonds, molecular weight, LogP, and drug-likeness scoring
- **Virtual Screening**: High-throughput docking using AutoDock Vina, Glide-score approximations, and pharmacophore-based filtering
- **Pharmacophore Modeling**: 3D pharmacophore generation from active compounds, feature-based screening (H-bond donor/acceptor, hydrophobic, aromatic, charge)
- **QSAR Modeling**: Machine-learning-based activity prediction from molecular fingerprints (Morgan, MACCS, topological)
- **ADMET Prediction**: Blood-brain barrier penetration, CYP450 inhibition, hERG liability, hepatotoxicity, and metabolic stability
- **Compound Library Management**: ChEMBL/PubChem API integration, SMILES/InChI parsing, RDKit molecular objects, duplicate detection by Tanimoto similarity
- **Lead Optimization**: Scaffold hopping suggestions, bioisostere replacement, and R-group enumeration
- **SAR Analysis**: Structure-Activity Relationship tables, matched molecular pair analysis

## Usage Examples

```python
from drug_discovery import (
    MoleculeProcessor,
    VirtualScreener,
    ADMETPredictor,
    CompoundLibrary,
    PharmacophoreModeler,
)

# --- Molecular Property Calculation ---
processor = MoleculeProcessor()
mol = processor.from_smiles("CC(=O)Oc1ccccc1C(=O)O")  # Aspirin
props = mol.calculate_properties()
print(f"MW: {props.molecular_weight:.1f}")
print(f"LogP: {props.logP:.2f}")
print(f"TPSA: {props.tpsa:.1f} A^2")
print(f"HBD: {props.hbd}  HBA: {props.hba}")
print(f"Drug-like (Lipinski): {props.passes_lipinski}")
print(f"QED score: {props.qed:.3f}")

# --- Virtual Screening ---
screener = VirtualScreener(
    protein_pdb="7bqc.pdb",
    grid_center=(12.5, 34.2, -8.1),
    grid_size=(20, 20, 20),
)
results = screener.dock_library(
    library="approved_drugs.sdf",
    top_n=50,
)
for hit in results[:5]:
    print(
        f"{hit.compound_id}: affinity={hit.affinity:.1f} kcal/mol, "
        f"pose_score={hit.pose_score:.2f}"
    )

# --- ADMET Profiling ---
admet = ADMETPredictor()
for hit in results[:10]:
    profile = admet.predict(hit.smiles)
    print(
        f"{hit.compound_id}: BBB={profile.bbb_penetration}, "
        f"CYP3A4={profile.cyp3a4_inhibitor}, "
        f"hERG={profile.herg_liability}, "
        f"hepato={profile.hepatotoxicity}"
    )

# --- Pharmacophore Modeling ---
modeler = PharmacophoreModeler()
pharmacophore = modeler.generate_from_actives(
    smiles_list=["CC(=O)Oc1ccccc1C(=O)O", "c1ccc(cc1)C(=O)O"],
    activity_threshold=7.0,
)
screen_hits = modeler.screen_library(
    pharmacophore=pharmacophore,
    library="chembl_compounds.smi",
    tolerance=1.5,
)

# --- Compound Library ---
library = CompoundLibrary("my_library.sdf")
library.add_from_smiles("CC(=O)Oc1ccccc1C(=O)O", name="Aspirin")
library.deduplicate(threshold=0.85)
print(f"Library size after dedup: {len(library)}")
library.export("cleaned_library.sdf")
```

## Best Practices

- Always apply drug-likeness filters (Lipinski, Veber, PAINS) before docking to reduce false positives
- Use multiple scoring functions for consensus docking to improve hit rates
- Validate ADMET predictions with experimental data when available
- Apply PAINS (Pan-Assay Interference Compounds) filtering to remove assay artifacts
- Consider multiple protein conformations (ensemble docking) for flexible targets
- Use Morgan fingerprints (radius=2, 2048 bits) for general-purpose similarity searching
- Set appropriate grid size — too small misses key interactions, too large increases noise
- Include water molecules in binding sites when they mediate key hydrogen bonds
- Report confidence intervals for QSAR predictions, not just point estimates
- For lead optimization, balance potency with ADMET properties — optimize multi-parameter

## Related Modules

- **protein-structure**: Target preparation for structure-based drug design
- **genomic-analysis**: Pharmacogenomic variant interpretation
- **sequence-alignment**: Target homology identification for template-based docking
- **phylogenetics**: Evolutionary analysis of drug target families

---

## Advanced Configuration

### Multi-Objective Lead Optimization

```python
from drug_discovery import LeadOptimizer

optimizer = LeadOptimizer(
    objectives=[
        {"property": "binding_affinity", "direction": "minimize", "weight": 1.0},
        {"property": "molecular_weight", "direction": "minimize", "weight": 0.3},
        {"property": "logP", "direction": "target", "target": 2.5, "weight": 0.5},
        {"property": "tpsa", "direction": "maximize", "weight": 0.2},
    ],
    constraints=[
        {"property": "hbd", "max": 3},
        {"property": "hba", "max": 7},
        {"property": "rotatable_bonds", "max": 8},
    ],
    algorithm="nsga2",
    population_size=200,
    generations=50,
)

# Optimize from starting compound
results = optimizer.optimize(
    starting_smiles="CC(=O)Oc1ccccc1C(=O)O",
    scaffold_hopping=True,
    bioisostere_replacement=True,
    r_group_enumeration=True,
)

# Pareto-optimal compounds
for compound in results.pareto_front:
    print(
        f"SMILES: {compound.smiles}\n"
        f"  Affinity: {compound.binding_affinity:.1f} kcal/mol\n"
        f"  QED: {compound.qed:.3f}\n"
        f"  SA score: {compound.synthetic_accessibility:.2f}\n"
    )
```

### QSAR Model Training

```python
from drug_discovery import QSARTrainer, QSARModel

trainer = QSARTrainer(
    task="regression",
    fingerprint_type="morgan",
    fingerprint_radius=2,
    n_bits=2048,
)

# Train from activity data
model = trainer.train(
    training_data="activity_data.csv",
    smiles_column="smiles",
    activity_column="pIC50",
    method="random_forest",
    cv_folds=5,
    feature_scaling="standard",
)

print(f"R² (train): {model.r2_train:.3f}")
print(f"R² (CV): {model.r2_cv:.3f}")
print(f"RMSE (CV): {model.rmse_cv:.3f}")
print(f"MAE (CV): {model.mae_cv:.3f}")

# Feature importance
importance = model.feature_importance(top_n=20)
for feat, score in importance:
    print(f"  Bit {feat}: importance={score:.4f}")

# Predict on new compounds
predictions = model.predict(
    compounds=["c1ccc(NC(=O)c2ccncc2)cc1", "CC(=O)Nc1ccc(O)cc1"],
)
for pred in predictions:
    print(f"  {pred.smiles}: pIC50={pred.prediction:.2f} ± {pred.uncertainty:.2f}")
```

### Combinatorial Library Design

```python
from drug_discovery import CombinatorialDesigner

designer = CombinatorialDesigner(
    scaffolds=["c1ccc2[nH]ccc2c1", "c1ccc2ncncc2c1"],
    r_groups={
        "position_1": ["F", "Cl", "CH3", "OCH3", "CF3"],
        "position_2": ["NH2", "OH", "SH", "N(CH3)2"],
        "position_3": ["C(=O)NH2", "SO2NH2", "CN", "C#N"],
    },
)

# Generate enumerated library
library = designer.enumerate(
    max_compounds=10000,
    apply_filters={
        "lipinski": True,
        "pains": True,
        "veber": True,
        "mw_max": 500,
    },
)

print(f"Enumerated: {library.total_generated}")
print(f"After filtering: {library.filtered_count}")
library.export("combinatorial_library.smi")
```

## Architecture Patterns

```
┌──────────────────────────────────────────────────────────┐
│                 Drug Discovery Pipeline                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐   │
│  │  Target  │───▶│  Prepare │───▶│  Binding Site    │   │
│  │  PDB/CIF │    │  Structure│   │  Detection       │   │
│  └──────────┘    └──────────┘    └────────┬─────────┘   │
│                                           │             │
│  ┌──────────┐    ┌──────────┐    ┌────────▼─────────┐   │
│  │ Compound │───▶│ Filter   │───▶│  Pharmacophore   │   │
│  │ Library  │    │ (Lipinski│    │  Generation      │   │
│  └──────────┘    │  PAINS)  │    └────────┬─────────┘   │
│                  └──────────┘             │             │
│                                  ┌────────▼─────────┐   │
│                                  │ Virtual Screening │   │
│                                  │ (Docking + Score) │   │
│                                  └────────┬─────────┘   │
│                                           │             │
│                                  ┌────────▼─────────┐   │
│                                  │  ADMET Profiling  │   │
│                                  └────────┬─────────┘   │
│                                           │             │
│                              ┌────────────┼────────────┐│
│                              │            │            ││
│                    ┌─────────▼──┐ ┌───────▼─────┐ ┌───▼────────┐│
│                    │  QSAR      │ │  Lead       │ │  SAR       ││
│                    │  Prediction│ │  Optimization│ │  Analysis  ││
│                    └────────────┘ └─────────────┘ └────────────┘│
│                                                          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                 Output: Hit List / Lead Compounds     │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

```
ADMET Prediction Pipeline:

    Input SMILES
         │
    ┌────▼────────────────┐
    │ Lipinski Rule of 5  │
    │  MW ≤ 500           │
    │  LogP ≤ 5           │
    │  HBD ≤ 5            │
    │  HBA ≤ 10           │
    └────┬────────────────┘
         │ PASS / FAIL
    ┌────▼────────────────┐
    │ Veber Rules         │
    │  TPSA ≤ 140 A²     │
    │  RotBonds ≤ 10      │
    └────┬────────────────┘
         │
    ┌────▼────────────────┐
    │ PAINS Filter        │
    │  Remove assay       │
    │  interference hits  │
    └────┬────────────────┘
         │
    ┌────▼────────────────┐
    │ ADMET Properties    │
    │  - BBB penetration  │
    │  - CYP450 inhib.    │
    │  - hERG liability   │
    │  - Hepatotoxicity   │
    │  - Metabolic stab.  │
    │  - Oral bioavail.   │
    └────┬────────────────┘
         │
    ┌────▼────────────────┐
    │ Composite Score     │
    │  Weighted ADMET     │
    │  profile ranking    │
    └─────────────────────┘
```

## Integration Guide

### ChEMBL Database Integration

```python
from drug_discovery import ChEMBLClient

client = ChEMBLClient(api_key="your_api_key")

# Search for compounds with activity against target
compounds = client.search_activities(
    target_chembl_id="CHEMBL220",
    activity_types=["IC50", "Ki", "Kd"],
    min_confidence=8,
    max_records=500,
)

# Export to DataFrame
df = compounds.to_dataframe()
print(f"Found {len(df)} activity records for {df['compound_id'].nunique()} compounds")

# Get compound structures
structures = client.get_structures(
    compound_ids=df["compound_id"].unique().tolist(),
)
library = CompoundLibrary.from_chembl(structures, activities=df)
```

### PubChem Integration

```python
from drug_discovery import PubChemClient

pubchem = PubChemClient()

# Search by name
compound = pubchem.get_compound("aspirin")
print(f"CID: {compound.cid}")
print(f"SMILES: {compound.smiles}")
print(f"InChI: {compound.inchi}")

# Search by SMILES similarity
similar = pubchem.similarity_search(
    smiles="CC(=O)Oc1ccccc1C(=O)O",
    threshold=90,
    max_results=100,
)

# Get bioassay data
bioassays = pubchem.get_bioassays(cid=compound.cid, max_records=50)
for assay in bioassays:
    print(f"  Assay {assay.aid}: outcome={assay.outcome}, target={assay.target}")
```

### Docking Server Integration

```python
from drug_discovery import DockingServer

server = DockingServer(
    server_url="https://dock.example.org/api/v1",
    api_key="your_api_key",
)

# Submit docking job
job = server.submit_docking(
    protein_pdb_id="7BQC",
    ligand_smiles="CC(=O)Oc1ccccc1C(=O)O",
    grid_center=(12.5, 34.2, -8.1),
    grid_size=(20, 20, 20),
    exhaustiveness=32,
)

# Poll for completion
result = server.wait_for_completion(job.id, timeout=3600)

# Download results
poses = server.download_poses(job.id, format="sdf")
```

## Performance Optimization

### Virtual Screening Throughput

```python
from drug_discovery import ParallelScreener

screener = ParallelScreener(
    n_workers=32,
    gpu_ids=[0, 1, 2, 3],
    batch_size=1000,
)

# Screen large library in parallel
results = screener.screen(
    protein="target.pdb",
    library="millions_compounds.sdf",
    scoring_function="vina",
    top_n=100,
    progress_callback=lambda p: print(f"Progress: {p:.1f}%"),
)

# Expected throughput: ~10,000 compounds/minute on 4 GPUs
```

### Fingerprint Caching

```python
from drug_discovery import FingerprintCache

cache = FingerprintCache(
    cache_dir="/data/fp_cache",
    fingerprint_type="morgan",
    radius=2,
    n_bits=2048,
)

# Precompute fingerprints for library
cache.precompute(
    library="large_library.smi",
    batch_size=10000,
)

# Similarity search with cached fingerprints
results = cache.tanimoto_search(
    query_smiles="CC(=O)Oc1ccccc1C(=O)O",
    threshold=0.7,
    top_k=100,
)
```

### Batch Property Calculation

```python
from drug_discovery import BatchPropertyCalculator

calc = BatchPropertyCalculator(
    n_workers=16,
    chunk_size=5000,
)

# Calculate properties for large library
properties = calc.calculate(
    library="approved_drugs.smi",
    properties=[
        "molecular_weight", "logP", "tpsa", "hbd", "hba",
        "rotatable_bonds", "qed", "sa_score", "lipinski",
    ],
)

# Export to CSV
properties.to_csv("drug_properties.csv", index=False)
```

## Security Considerations

### Compound Data Security

- Encrypt proprietary compound libraries at rest using AES-256
- Use secure channels (HTTPS, TLS) for API communications with ChEMBL/PubChem
- Never log SMILES strings or compound identifiers in pipeline output files
- Implement access controls on virtual screening results containing proprietary data
- Audit all compound library access and screening operations
- Use anonymized compound IDs in shared results
- Implement data retention policies for screening results
- Secure backup of proprietary compound databases

### API Key Management

```python
from drug_discovery import SecureConfig

config = SecureConfig(
    secrets_backend="vault",
    vault_url="https://vault.internal:8200",
)

# Retrieve API keys from secrets manager
chembl_key = config.get_secret("chembl/api_key")
pubchem_key = config.get_secret("pubchem/api_key")
docking_key = config.get_secret("docking/api_key")

# Use in clients
client = ChEMBLClient(api_key=chembl_key)
```

### Intellectual Property Protection

- Never submit proprietary compounds to public databases without authorization
- Use local docking servers for proprietary target structures
- Implement watermarking on virtual screening results
- Restrict access to lead optimization data containing competitive intelligence
- Use secure deletion for temporary screening files
- Log all operations on proprietary compound data

## Troubleshooting Guide

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| Docking fails with "grid out of range" | Grid center outside protein bounds | Verify grid coordinates against PDB; increase grid size |
| Vina returns unrealistic binding scores | Flexible residues clash with ligand | Pre-minimize protein; check for structural conflicts |
| PAINS filter removes known actives | Compounds contain PAINS-like motifs | Review PAINS alerts; some are legitimate — use with caution |
| QSAR model has low R² | Insufficient training data or noisy labels | Collect more data; clean activity values; try different descriptors |
| ADMET predictions are all "pass" | Model is undertrained or features are wrong | Validate with known positives/negatives; check feature engineering |
| Pharmacophore screening returns no hits | Pharmacophore is too restrictive | Increase tolerance; relax feature constraints |
| Compound library dedup removes intended duplicates | Similarity threshold too high | Lower threshold; use structural key similarity instead of Tanimoto |
| Virtual screening is too slow | Large library, single-threaded | Enable parallelization; use GPU docking; pre-filter library |
| RDKit fails to parse SMILES | Invalid or unusual SMILES syntax | Use `Chem.MolFromSmiles` error handling; sanitize molecules |
| CYP450 prediction gives contradictory results | Different models for different CYPs | Check each CYP isoform separately; ensemble prediction |
| Lead optimization generates invalid molecules | R-group enumeration produces valence errors | Apply valence checks; use constrained enumeration |
| hERG prediction is unreliable | hERG models have high false positive rate | Use multiple models; validate with patch clamp data |

## API Reference

### MoleculeProcessor

```python
class MoleculeProcessor:
    """Process and analyze molecular structures."""

    def from_smiles(self, smiles: str) -> Molecule:
        """Create molecule from SMILES string."""

    def from_inchi(self, inchi: str) -> Molecule:
        """Create molecule from InChI string."""

    def from_sdf(self, filepath: str) -> List[Molecule]:
        """Load molecules from SDF file."""

    def from_mol2(self, filepath: str) -> Molecule:
        """Load molecule from MOL2 file."""

class Molecule:
    smiles: str
    inchi: str
    molecular_weight: float

    def calculate_properties(self) -> MolecularProperties:
        """Calculate comprehensive molecular properties."""

    def get_fingerprint(self, type: str = "morgan", radius: int = 2, n_bits: int = 2048):
        """Generate molecular fingerprint."""

    def substructure_search(self, pattern: str) -> bool:
        """Check if molecule contains substructure."""

    def to_3d(self, coords_only: bool = False) -> str:
        """Generate 3D coordinates (returns SDF block)."""
```

### VirtualScreener

```python
class VirtualScreener:
    def __init__(
        self,
        protein_pdb: str,
        grid_center: Tuple[float, float, float],
        grid_size: Tuple[float, float, float],
        exhaustiveness: int = 8,
        n_poses: int = 10,
    ): ...

    def dock_single(self, molecule: Molecule) -> DockingResult:
        """Dock a single molecule."""

    def dock_library(
        self,
        library: str,
        top_n: int = 100,
        output: str = None,
    ) -> List[DockingResult]:
        """Dock an entire library."""

    def ensemble_dock(
        self,
        protein_structures: List[str],
        library: str,
        top_n: int = 100,
    ) -> List[DockingResult]:
        """Dock against multiple protein conformations."""

class DockingResult:
    compound_id: str
    smiles: str
    affinity: float       # kcal/mol
    pose_score: float
    pose: Molecule
    interactions: List[ProteinLigandInteraction]
```

### ADMETPredictor

```python
class ADMETPredictor:
    def __init__(self, model_version: str = "latest"): ...

    def predict(self, smiles: str) -> ADMETProfile:
        """Predict all ADMET properties."""

    def predict_bbb(self, smiles: str) -> BBBPrediction:
        """Predict blood-brain barrier penetration."""

    def predict_cyp(self, smiles: str) -> CYPPrediction:
        """Predict CYP450 inhibition profile."""

    def predict_herg(self, smiles: str) -> float:
        """Predict hERG inhibition probability."""

    def predict_hepatotoxicity(self, smiles: str) -> float:
        """Predict hepatotoxicity probability."""

class ADMETProfile:
    bbb_penetration: str     # HIGH, MEDIUM, LOW
    cyp3a4_inhibitor: bool
    cyp2d6_inhibitor: bool
    cyp2c9_inhibitor: bool
    herg_liability: str      # HIGH, MEDIUM, LOW
    hepatotoxicity: bool
    oral_bioavailability: float
    metabolic_stability: float  # half-life in minutes
    plasma_protein_binding: float  # percentage
```

### CompoundLibrary

```python
class CompoundLibrary:
    def __init__(self, filepath: str = None): ...

    def add_from_smiles(self, smiles: str, name: str = None) -> None:
        """Add compound from SMILES."""

    def add_from_sdf(self, filepath: str) -> int:
        """Add compounds from SDF; returns count added."""

    def deduplicate(self, threshold: float = 0.85) -> int:
        """Remove duplicates; returns count removed."""

    def filter_lipinski(self) -> int:
        """Apply Lipinski Rule of Five filter."""

    def filter_pains(self) -> int:
        """Remove PAINS compounds."""

    def similarity_search(self, query: str, threshold: float = 0.7) -> List:
        """Search by Tanimoto similarity."""

    def export(self, filepath: str, format: str = "sdf") -> None:
        """Export library to file."""

    def __len__(self) -> int:
        """Return library size."""
```

## Data Models

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

@dataclass
class MolecularProperties:
    molecular_weight: float
    logP: float
    tpsa: float
    hbd: int
    hba: int
    rotatable_bonds: int
    aromatic_rings: int
    heavy_atom_count: int
    passes_lipinski: bool
    passes_veber: bool
    qed: float
    sa_score: float
    formula: str

@dataclass
class PharmacophoreFeature:
    feature_type: str  # HB_DONOR, HB_ACCEPTOR, HYDROPHOBIC, AROMATIC, POS_CHARGE, NEG_CHARGE
    x: float
    y: float
    z: float
    radius: float = 1.5

@dataclass
class Pharmacophore:
    features: List[PharmacophoreFeature]
    name: str = ""
    tolerance: float = 1.5
    activity_threshold: float = 0.0

@dataclass
class DockingResult:
    compound_id: str
    smiles: str
    affinity: float
    pose_score: float
    pose_coordinates: List[Tuple[float, float, float]]
    hydrogen_bonds: List[Tuple[str, str, float]]  # (protein_res, ligand_atom, distance)
    hydrophobic_contacts: List[Tuple[str, str]]
    interactions: List[Dict[str, str]]

@dataclass
class ADMETProfile:
    bbb_penetration: str
    cyp3a4_inhibitor: bool
    cyp2d6_inhibitor: bool
    cyp2c9_inhibitor: bool
    herg_liability: str
    hepatotoxicity: bool
    oral_bioavailability: float
    metabolic_stability: float
    plasma_protein_binding: float
    solubility: float  # mg/L

@dataclass
class SARRecord:
    compound_id: str
    smiles: str
    scaffold: str
    r_group_positions: Dict[str, str]
    activity: float
    activity_type: str  # IC50, Ki, Kd, EC50
    target: str

@dataclass
class QSARModel:
    model_type: str
    r2_train: float
    r2_cv: float
    rmse_cv: float
    mae_cv: float
    feature_names: List[str]
    feature_importance: Dict[str, float]
    training_size: int
    descriptor_set: str

@dataclass
class VirtualScreeningRun:
    run_id: str
    protein_pdb: str
    library_size: int
    compounds_screened: int
    top_hits: int
    scoring_function: str
    grid_center: Tuple[float, float, float]
    grid_size: Tuple[float, float, float]
    runtime_seconds: float
    results: List[DockingResult]
```

## Deployment Guide

### Installation

```bash
# Install from PyPI
pip install drug-discovery[all]

# Install with specific backends
pip install drug-discovery[docking,admet,qsar]

# Install from source
git clone https://github.com/example/drug-discovery.git
cd drug-discovery
pip install -e ".[dev,test]"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libboost-all-dev \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install AutoDock Vina
RUN pip install vina==1.2.3

# Install drug-discovery package
RUN pip install drug-discovery[all]

ENTRYPOINT ["drug-discover"]
```

### Kubernetes Deployment

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: virtual-screening
spec:
  template:
    spec:
      containers:
      - name: screener
        image: drug-discovery:2.0.0
        command: ["drug-discover", "screen", "--config", "/config/screening.yaml"]
        resources:
          requests:
            memory: "16Gi"
            cpu: "8"
          limits:
            memory: "64Gi"
            cpu: "16"
            nvidia.com/gpu: "4"
        volumeMounts:
        - name: library
          mountPath: /data/library
        - name: targets
          mountPath: /data/targets
      volumes:
      - name: library
        persistentVolumeClaim:
          claimName: compound-library-pvc
      - name: targets
        persistentVolumeClaim:
          claimName: target-structures-pvc
      restartPolicy: Never
```

## Monitoring and Observability

### Screening Metrics

```python
from drug_discovery import ScreeningMonitor

monitor = ScreeningMonitor(metrics_backend="prometheus")

# Track screening throughput
monitor.counter("compounds.screened", count)
monitor.histogram("docking.affinity", affinity)
monitor.gauge("screening.hit_rate", hits / total)
monitor.timing("docking.per_compound_ms", elapsed / total)

# Track ADMET profile distributions
monitor.histogram("admet.bbb_score", bbb_scores)
monitor.histogram("admet.herg_probability", herg_scores)
```

### Quality Dashboards

- Monitor virtual screening hit rates across targets
- Track ADMET property distributions for hit compounds
- Visualize QSAR model performance over time
- Alert on docking failures or anomalous binding scores
- Track compound library growth and diversity metrics
- Monitor API usage for ChEMBL/PubChem integrations
- Report on lead optimization progress and compound attrition

## Testing Strategy

### Unit Tests

```python
import pytest
from drug_discovery import MoleculeProcessor, VirtualScreener

def test_smiles_parsing():
    proc = MoleculeProcessor()
    mol = proc.from_smiles("CC(=O)Oc1ccccc1C(=O)O")
    assert mol.molecular_weight == pytest.approx(180.16, rel=1e-2)

def test_lipinski_filter():
    proc = MoleculeProcessor()
    mol = proc.from_smiles("CC(=O)Oc1ccccc1C(=O)O")
    props = mol.calculate_properties()
    assert props.passes_lipinski is True

def test_docking():
    screener = VirtualScreener(
        protein_pdb="test_data/test_target.pdb",
        grid_center=(0, 0, 0),
        grid_size=(20, 20, 20),
    )
    result = screener.dock_single(
        MoleculeProcessor().from_smiles("CC(=O)Oc1ccccc1C(=O)O")
    )
    assert result.affinity < 0
```

### Integration Tests

```python
@pytest.mark.integration
def test_screening_pipeline():
    screener = VirtualScreener(
        protein_pdb="test_data/kinase.pdb",
        grid_center=(10, 20, 30),
        grid_size=(25, 25, 25),
    )
    results = screener.dock_library(
        library="test_data/small_library.sdf",
        top_n=10,
    )
    assert len(results) == 10
    assert all(r.affinity < 0 for r in results)

@pytest.mark.integration
def test_admet_profiling():
    admet = ADMETPredictor()
    profile = admet.predict("CC(=O)Oc1ccccc1C(=O)O")
    assert profile.bbb_penetration in ["HIGH", "MEDIUM", "LOW"]
    assert 0 <= profile.oral_bioavailability <= 1
```

## Versioning and Migration

### Semantic Versioning

- **Major** (X.0.0): Breaking API changes, new docking engine support
- **Minor** (0.X.0): New ADMET models, new library formats, new QSAR methods
- **Patch** (0.0.X): Bug fixes, improved accuracy, documentation updates

### Migration Guide (v1.x → v2.0)

```python
# v1.x (deprecated)
from drug_discovery.v1 import Dock
dock = Dock(protein="target.pdb", library="compounds.sdf")

# v2.0 (current)
from drug_discovery import VirtualScreener
screener = VirtualScreener(protein_pdb="target.pdb", grid_center=(...), grid_size=(...))
results = screener.dock_library(library="compounds.sdf")
```

### Compatibility Matrix

| Version | Vina | RDKit | scikit-learn | DeepChem |
|---------|------|-------|-------------|----------|
| 2.0.x   | 1.2+ | 2023+ | 1.3+        | 2.7+     |
| 1.5.x   | 1.1+ | 2022+ | 1.2+        | 2.6+     |
| 1.0.x   | 1.0+ | 2021+ | 1.0+        | 2.5+     |

## Glossary

| Term | Definition |
|------|-----------|
| **ADMET** | Absorption, Distribution, Metabolism, Excretion, Toxicity — pharmacokinetic properties |
| **QSAR** | Quantitative Structure-Activity Relationship — mathematical model relating structure to activity |
| **PAINS** | Pan-Assay Interference Compounds — molecules that give false positives in biochemical assays |
| **Lipinski's Rule of Five** | Heuristic for oral bioavailability: MW≤500, LogP≤5, HBD≤5, HBA≤10 |
| **TPSA** | Topological Polar Surface Area — correlates with membrane permeability |
| **QED** | Quantitative Estimate of Drug-likeness — composite score 0-1 |
| **SA Score** | Synthetic Accessibility score — estimates ease of chemical synthesis |
| **Scaffold Hopping** | Replacing core structure while maintaining activity |
| **Bioisostere** | Chemical group with similar size, shape, and electronic properties |
| **Pharmacophore** | 3D arrangement of features necessary for molecular recognition |
| **Morgan Fingerprint** | Circular fingerprint based on atomic environments within radius |
| **Tanimoto Similarity** | Jaccard index for comparing molecular fingerprints |
| **IC50** | Half-maximal inhibitory concentration — potency measure |
| **pIC50** | -log10(IC50 in M) — logarithmic potency scale |
| **hERG** | Human Ether-à-go-go-Related Gene — cardiac potassium channel |

## Changelog

### v2.0.0 (2024-06-15)
- Added multi-objective lead optimization with NSGA-II
- Added GPU-accelerated virtual screening
- Added QSAR model training and validation
- Added combinatorial library design
- Improved ADMET prediction accuracy with ensemble models

### v1.5.0 (2024-01-10)
- Added ChEMBL and PubChem API integration
- Added pharmacophore generation and screening
- Added PAINS filtering
- Improved docking speed with parallelization

### v1.0.0 (2023-09-01)
- Initial release with molecular property calculation
- Virtual screening with AutoDock Vina
- ADMET prediction
- Compound library management

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Write tests for all new functionality
3. Run the full test suite: `pytest tests/ -v --cov=drug_discovery`
4. Update documentation for API changes
5. Follow PEP 8 style guidelines
6. Add changelog entries for user-facing changes
7. Submit a pull request with clear description

## License

MIT License

Copyright (c) 2024 Drug Discovery Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
