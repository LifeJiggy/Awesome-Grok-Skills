---
name: "protein-structure"
category: "bioinformatics"
version: "2.0.0"
tags: ["bioinformatics", "protein-structure", "PDB", "fold-prediction", "molecular-dynamics"]
---

# Protein Structure Analysis

## Overview

The Protein Structure Analysis module provides comprehensive tools for protein 3D structure prediction, manipulation, visualization data generation, and analysis. It supports AlphaFold2/ColabFold predicted structures, experimental PDB files, and molecular dynamics trajectories. The module covers structure quality assessment, secondary structure assignment, solvent-accessible surface area (SASA) calculation, hydrogen bond network analysis, binding pocket detection, and structure-based virtual screening preparation.

This skill is essential for structural biologists, computational chemists, and bioinformaticians working on drug design, protein engineering, and structural genomics projects.

## Core Capabilities

- **Structure Parsing**: Read and manipulate PDB, mmCIF, PDBQT, and AlphaFold JSON formats with full atom-level access
- **Structure Quality Assessment**: Ramachandran plot analysis, clashscore calculation, Rotamer outliers, MolProbity-style validation
- **Secondary Structure Assignment**: DSSP-style assignment of helices, sheets, turns, and loops from atomic coordinates
- **Surface Analysis**: Solvent-accessible surface area (SASA) calculation using the Shrake-Rupley algorithm, electrostatic surface potential
- **Binding Site Detection**: FPocket and geometric approaches for identifying ligand-binding cavities and allosteric sites
- **Structure Alignment**: Structural superposition using Kabsch and iterative closest point (ICP) algorithms, RMSD calculation
- **Homology Modeling**: Template-based structure prediction using sequence-structure alignment
- **Molecular Dynamics Prep**: Topology generation, solvation, ionization, and energy minimization setup for GROMACS/OpenMM
- **Mutation Impact Analysis**: Stability prediction (ΔΔG) for point mutations using FoldX and empirical force fields

## Usage Examples

```python
from protein_structure import (
    StructureParser,
    QualityAssessor,
    BindingSiteDetector,
    StructureAligner,
    MutationAnalyzer,
)

# --- Parse and Inspect Structure ---
parser = StructureParser("7bqc.pdb")
structure = parser.parse()
print(f"Chains: {list(structure.chains)}")
print(f"Residues: {structure.residue_count}")
print(f"Atoms: {structure.atom_count}")
print(f"Ligands: {structure.ligand_names}")

# --- Quality Assessment ---
assessor = QualityAssessor(structure)
quality = assessor.comprehensive_report()
print(f"Ramachandran favored: {quality.rama_favored_pct:.1f}%")
print(f"Clashscore: {quality.clashscore}")
print(f"Rotamer outliers: {quality.rotamer_outliers}")
print(f"MolProbity score: {quality.molprobity_score:.2f}")
if quality.molprobity_score > 2.0:
    print("WARNING: Structure quality is below threshold")

# --- Binding Site Detection ---
detector = BindingSiteDetector(structure, min_volume=150)
pockets = detector.detect()
for pocket in pockets[:3]:
    print(
        f"Pocket {pocket.rank}: vol={pocket.volume:.0f} A^3, "
        f"druggability={pocket.druggability:.2f}, "
        f"residues={pocket.residue_count}"
    )

# --- Structural Alignment ---
aligner = StructureAligner()
mobile = StructureParser("mutant.pdb").parse()
alignment = aligner.align(
    reference=structure,
    mobile=mobile,
    chains="A",
)
print(f"RMSD: {alignment.rmsd:.2f} A")
print(f"Aligned residues: {alignment.aligned_pairs}")

# --- Mutation Impact ---
analyzer = MutationAnalyzer(structure)
mutations = [
    ("A42T", "stability"),
    ("L110P", "stability"),
    ("G200D", "binding_affinity"),
]
for mut, analysis_type in mutations:
    result = analyzer.predict(mut, analysis_type=analysis_type)
    print(
        f"{mut}: ddG={result.ddG:+.2f} kcal/mol, "
        f"effect={result.classification}"
    )
```

## Best Practices

- Always validate structure quality before using it for modeling or drug design
- Remove crystallographic water molecules unless studying ordered water-mediated contacts
- Add hydrogen atoms explicitly for molecular dynamics and docking simulations
- Use multiple templates for homology modeling when available to improve accuracy
- Check for crystal packing artifacts in biological assembly assignments
- Use CHARMM36 or AMBER ff19SB force fields for protein molecular dynamics
- Validate Ramachandran statistics — structures with <95% favored regions need manual inspection
- Use pLDDT scores from AlphaFold to weight structural confidence in hybrid models
- For binding site analysis, compare geometric and energy-based methods for robustness
- Store structure comparisons with sequence identity and coverage metrics

## Related Modules

- **genomic-analysis**: Variant-to-structure mapping for missense mutations
- **drug-discovery**: Virtual screening and lead optimization workflows
- **sequence-alignment**: Sequence-level homology for template selection
- **phylogenetics**: Evolutionary conservation mapping onto structures

---

## Advanced Configuration

### AlphaFold Integration

```python
from protein_structure import AlphaFoldManager

af_manager = AlphaFoldManager(
    cache_dir="/data/alphafold_cache",
    api_key_env="ALPHAFOLD_API_KEY",
)

# Fetch structure by UniProt ID
structure = af_manager.fetch("P00533")  # EGFR

# Check confidence distribution
conf = structure.plddt_summary()
print(f"High confidence (>90): {conf.high_pct:.1f}%")
print(f"Medium confidence (70-90): {conf.medium_pct:.1f}%")
print(f"Low confidence (<70): {conf.low_pct:.1f}%")

# Filter low-confidence regions for modeling
confident_structure = af_manager.filter_confidence(
    structure,
    min_plddt=70,
    include_flanking=5,
)
```

### Molecular Dynamics Setup

```python
from protein_structure import MDSimulator

sim = MDSimulator(
    force_field="charmm36",
    water_model="tip3p",
    integrator="langevin",
)

# Full MD setup pipeline
system = sim.prepare(
    structure="protein.pdb",
    box_type="dodecahedron",
    box_padding=1.2,  # nm from solute
    ionic_strength=0.15,  # M NaCl
    neutralize=True,
)

# Energy minimization
system.minimize(
    max_iterations=50000,
    force_tolerance=1000,  # kJ/mol/nm
    step_size=0.01,  # nm
)

# Equilibration (NVT then NPT)
system.equilibrate_nvt(
    temperature=310,  # K (body temperature)
    coupling_time=0.1,  # ps
    duration=100,  # ps
)
system.equilibrate_npt(
    temperature=310,
    pressure=1.0,  # bar
    coupling_time=0.1,
    duration=500,  # ps
)

# Production run
system.production(
    duration=100,  # ns
    timestep=0.002,  # ps (2 fs)
    save_interval=10,  # ps
    output_dir="/data/md_runs/run_001",
)
```

### Homology Modeling

```python
from protein_structure import HomologyModeler

modeler = HomologyModeler(
    target_sequence="MKTLLIAA...",
    template_pdb="1abc",
    modeling_tool="modeller",
)

# Build model from single template
model = modeler.build_model(
    alignment="target_template.aln",
    num_models=5,
    assess_method="DOPE",
)

# Select best model
best = model.select_best(criterion="dope_score")
print(f"DOPE score: {best.dope_score:.2f}")

# Refine with energy minimization
refined = modeler.refine(
    model=best,
    minimization_steps=1000,
    solvent="explicit",
)
```

## Architecture Patterns

```
┌─────────────────────────────────────────────────────┐
│            Protein Structure Analysis Pipeline       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │  Input    │───▶│  Parse   │───▶│  Validate    │  │
│  │  PDB/CIF  │    │  Structure│    │  Quality     │  │
│  └──────────┘    └──────────┘    └──────┬───────┘  │
│                                         │           │
│                              ┌──────────┼──────────┐│
│                              │          │          ││
│                     ┌────────▼───┐ ┌────▼────┐ ┌──▼──────────┐│
│                     │ Secondary  │ │ Surface │ │ Binding     ││
│                     │ Structure  │ │ Analysis│ │ Site Detect ││
│                     │ (DSSP)     │ │ (SASA)  │ │ (FPocket)   ││
│                     └────────┬───┘ └────┬────┘ └──┬──────────┘│
│                              │          │          │           │
│                     ┌────────▼──────────▼──────────▼──────┐  │
│                     │       Structure Properties           │  │
│                     └────────┬──────────┬──────────┬──────┘  │
│                              │          │          │         │
│                    ┌─────────▼──┐ ┌─────▼─────┐ ┌─▼────────┐│
│                    │ Alignment  │ │ Mutation  │ │ MD Prep   ││
│                    │ (Kabsch)   │ │ Analysis  │ │ (GROMACS) ││
│                    └────────────┘ └───────────┘ └──────────┘│
│                                                     │       │
│  ┌──────────────────────────────────────────────┐   │       │
│  │               Output Formats                 │   │       │
│  │  PDB │ mmCIF │ SDF │ PyMOL scripts │ HTML   │   │       │
│  └──────────────────────────────────────────────┘   │       │
└─────────────────────────────────────────────────────────────┘
```

```
Structure Quality Assessment Pipeline:

    Input PDB/CIF
         │
    ┌────▼────────────────────┐
    │ Parse & Clean Structure │
    │  - Remove alt confs     │
    │  - Add hydrogens        │
    │  - Assign bonds         │
    └────┬────────────────────┘
         │
    ┌────▼──────────────┐
    │ Geometry Checks   │
    │  - Bond lengths   │
    │  - Bond angles    │
    │  - Torsion angles │
    │  - Clashscore     │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │ Ramachandran      │
    │  - Favored: >98%  │
    │  - Outliers: <0.5%│
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │ Rotamer Analysis  │
    │  - Favored: >95%  │
    │  - Outliers: <1%  │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │ MolProbity Score  │
    │  - Composite: <2.0│
    │  - Clashes: <10   │
    └────┬──────────────┘
         │
    ┌────▼────┐
    │ PASS /  │
    │ WARN /  │
    │ FAIL    │
    └─────────┘
```

## Integration Guide

### PyMOL Visualization Export

```python
from protein_structure import PyMOLExporter

exporter = PyMOLExporter()

# Generate PyMOL script for structure visualization
script = exporter.generate_script(
    structure="protein.pdb",
    highlights=[
        {"residues": ["A:42", "A:110"], "color": "red", "label": "mutant sites"},
        {"residues": ["A:200"], "color": "yellow", "label": "binding site"},
    ],
    surface={"show": True, "type": "electrostatic", "range": [-5, 5]},
    output="visualization.pml",
)

# Generate interactive HTML viewer
exporter.to_html(
    structure="protein.pdb",
    style="cartoon",
    coloring="chain",
    output="viewer.html",
)
```

### PyRosetta Integration

```python
from protein_structure import RosettaInterface

rosetta = RosettaInterface(
    rosetta_database="/opt/rosetta/database",
    executable="/opt/rosetta/bin/rosetta_scripts",
)

# Fast relax
relaxed = rosetta.fast_relax(
    structure="input.pdb",
    score_function="ref2015",
    num_cycles=5,
    output="relaxed.pdb",
)

# Interface energy calculation
interface = rosetta_interface.calc_interface_energy(
    complex_pdb="complex.pdb",
    chainA="A",
    chainB="B",
    score_function="ref2015",
)
print(f"Interface energy: {interface.total_energy:.1f} REU")
```

### ChimeraX Session Export

```python
from protein_structure import ChimeraXExporter

cx = ChimeraXExporter()

cx.create_session(
    structures=["protein.pdb", "ligand.sdf"],
    alignments=[("protein.pdb", "alphafold_model.pdb")],
    color_schemes={
        "protein": "chain",
        "ligand": "element",
    },
    output="session.cxs",
)
```

## Performance Optimization

### Structure Parsing Optimization

```python
from protein_structure import StructureParser

# Fast parsing for large structures (>100K atoms)
parser = StructureParser(
    "huge_complex.pdb",
    parse_mode="fast",           # Skip hydrogen and water
    load_alt_conformations=False,
    load_insertions=False,
    lazy_atom_loading=True,      # Load atoms on demand
)
structure = parser.parse()

# Batch parsing for MD trajectories
from protein_structure import TrajectoryParser

traj = TrajectoryParser(
    topology="system.pdb",
    trajectory=["frame_001.xtc", "frame_002.xtc"],
    stride=10,  # Read every 10th frame
    selection="protein and not name H*",
)
for frame in traj:
    rmsd = frame.rmsd(reference)
```

### Caching Strategies

```python
from protein_structure import StructureCache

cache = StructureCache(
    cache_dir="/data/structure_cache",
    max_size_gb=100,
    eviction_policy="lru",
)

# Cache parsed structures
structure = cache.get_or_compute(
    key="P00533_alpha_fold",
    compute_fn=lambda: AlphaFoldManager().fetch("P00533"),
)

# Cache alignment results
alignment = cache.get_or_compute(
    key=f"align_{hash(ref)}_{hash(mobile)}",
    compute_fn=lambda: aligner.align(ref, mobile),
)
```

### GPU-Accelerated Computing

```python
from protein_structure import GPUAccelerated

gpu = GPUAccelerated(device_id=0)

# GPU-accelerated SASA calculation
sasa = gpu.calculate_sasa(
    structure="protein.pdb",
    probe_radius=1.4,
    n_points=100,
)

# GPU-accelerated distance matrix
distance_matrix = gpu.distance_matrix(
    structure="complex.pdb",
    selection="chain A and chain B",
)
```

## Security Considerations

### Structural Data Handling

- PDB files from untrusted sources may contain malicious metadata — sanitize before processing
- Never execute scripts embedded in mmCIF or PDB header fields
- Validate file formats before parsing — malformed files can cause buffer overflows
- Limit file size inputs to prevent denial-of-service through extremely large structures
- Verify MD5 checksums when downloading structures from RCSB PDB
- Be cautious with automated structure downloads — rate-limit requests to public databases
- Store proprietary drug target structures in encrypted storage
- Audit access to proprietary structural data containing competitive intelligence

### Computational Resource Security

```python
from protein_structure import ResourceLimiter

limiter = ResourceLimiter(
    max_memory_gb=32,
    max_cpu_hours=24,
    max_gpu_hours=8,
    timeout_seconds=86400,
)

# Run with resource limits
result = limiter.run_with_limits(
    function=expensive_calculation,
    args=(structure,),
    timeout=3600,
    memory_limit="8G",
)
```

### Intellectual Property Protection

- Never upload proprietary protein structures to public databases without authorization
- Use local BLAST databases for proprietary sequence searches
- Encrypt structure files containing unpublished drug targets
- Implement access controls on structural databases containing proprietary data
- Log all access to proprietary structural information
- Use secure deletion for temporary structure files containing sensitive data

## Troubleshooting Guide

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| PDB parsing error "alternate conformations" | Multiple conformations in file | Set `alt_loc='A'` or `alt_loc='first'` in parser |
| Ramachandran shows >10% outliers | Structure not energy-minimized | Run energy minimization or use REFMAC5 refinement |
| Binding site detection returns no pockets | Protein is too small or too regular | Lower `min_volume` parameter; try geometric method |
| SASA calculation is extremely slow | Very large structure with many atoms | Use selection to compute SASA for specific chains only |
| Structure alignment RMSD is >10 A | Structures are not homologous | Check sequence identity first; use fragment alignment |
| Molecular dynamics crashes at start | Clashing atoms or missing atoms | Run energy minimization first; check for missing residues |
| AlphaFold pLDDT is all low | No homologs in sequence database | Try ColabFold with genetic databases; check sequence length |
| PDB file won't load in PyMOL | Format errors or missing chains | Validate PDB format with `pdb4amber`; try mmCIF instead |
| Homology model has poor DOPE score | Template is low quality | Try different template; use multiple templates |
| MD trajectory alignment drifts | Reference frame not set | Align to initial frame or representative structure |
| Mutation analysis returns NaN | Residue not in structure | Verify residue number and chain; check for missing residues |
| Electrostatic surface looks wrong | Dielectric constant incorrect | Use Poisson-Boltzmann solver; verify charge assignments |

## API Reference

### StructureParser

```python
class StructureParser:
    """Parse protein structure files."""

    def __init__(
        self,
        filepath: str,
        format: str = "auto",
        alt_loc: str = "first",
        model_id: int = 0,
    ): ...

    def parse(self) -> Structure:
        """Parse and return Structure object."""

    def parse_selection(self, selection: str) -> Structure:
        """Parse atoms matching selection string."""

class Structure:
    chains: Dict[str, Chain]
    residue_count: int
    atom_count: int
    ligand_names: List[str]
    title: str
    resolution: float
    method: str

    def select(self, selection: str) -> "Structure":
        """Select atoms by selection string."""

    def to_pdb(self, filepath: str) -> None:
        """Write structure to PDB file."""

    def to_mmcif(self, filepath: str) -> None:
        """Write structure to mmCIF file."""
```

### QualityAssessor

```python
class QualityAssessor:
    def __init__(self, structure: Structure): ...

    def comprehensive_report(self) -> QualityReport:
        """Run all quality checks and return report."""

    def ramachandran(self) -> RamachandranReport:
        """Ramachandran plot analysis."""

    def clashscore(self) -> float:
        """Calculate clashscore (clashes per 1000 atoms)."""

    def rotamer_analysis(self) -> RotamerReport:
        """Rotamer outlier analysis."""

class QualityReport:
    rama_favored_pct: float
    rama_allowed_pct: float
    rama_outlier_pct: float
    clashscore: float
    rotamer_outliers: int
    molprobity_score: float
    ca_rmsd: float  # C-alpha RMSD from ideal geometry
```

### BindingSiteDetector

```python
class BindingSiteDetector:
    def __init__(
        self,
        structure: Structure,
        min_volume: float = 100,
        max_volume: float = 5000,
        min_spheres: int = 5,
    ): ...

    def detect(self) -> List[BindingPocket]:
        """Detect binding pockets."""

    def druggability(self, pocket: BindingPocket) -> float:
        """Estimate druggability of a pocket (0-1)."""

class BindingPocket:
    rank: int
    volume: float       # cubic Angstroms
    druggability: float  # 0-1 score
    center: Tuple[float, float, float]
    residue_count: int
    residues: List[str]
    score: float
```

### MutationAnalyzer

```python
class MutationAnalyzer:
    def __init__(self, structure: Structure): ...

    def predict(
        self,
        mutation: str,
        analysis_type: str = "stability",
    ) -> MutationResult:
        """Predict mutation impact."""

    def batch_predict(
        self,
        mutations: List[str],
        analysis_type: str = "stability",
    ) -> List[MutationResult]:
        """Predict impact for multiple mutations."""

class MutationResult:
    mutation: str
    ddG: float           # kcal/mol (negative = stabilizing)
    classification: str  # stabilizing, neutral, destabilizing
    confidence: float
    details: Dict[str, float]
```

## Data Models

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from enum import Enum

class ResidueType(Enum):
    ALA = "ALA"; ARG = "ARG"; ASN = "ASN"; ASP = "ASP"
    CYS = "CYS"; GLU = "GLU"; GLN = "GLN"; GLY = "GLY"
    HIS = "HIS"; ILE = "ILE"; LEU = "LEU"; LYS = "LYS"
    MET = "MET"; PHE = "PHE"; PRO = "PRO"; SER = "SER"
    THR = "THR"; TRP = "TRP"; TYR = "TYR"; VAL = "VAL"

class SecondaryStructure(Enum):
    HELIX = "H"
    SHEET = "E"
    TURN = "T"
    COIL = "C"

@dataclass
class Atom:
    serial: int
    name: str
    alt_loc: str
    residue_name: str
    chain_id: str
    residue_seq: int
    x: float
    y: float
    z: float
    occupancy: float
    temperature_factor: float
    element: str
    charge: str = ""
    is_hetero: bool = False

@dataclass
class Residue:
    name: str
    sequence_number: int
    chain_id: str
    atoms: List[Atom]
    secondary_structure: SecondaryStructure = SecondaryStructure.COIL
    phi: float = 0.0
    psi: float = 0.0

@dataclass
class Chain:
    chain_id: str
    residues: List[Residue]
    sequence: str = ""
    organism: str = ""

@dataclass
class Structure:
    title: str
    chains: Dict[str, Chain]
    atoms: List[Atom]
    resolution: float = 0.0
    method: str = ""
    date: str = ""
    plddt_scores: Dict[int, float] = field(default_factory=dict)

    @property
    def residue_count(self) -> int:
        return sum(len(c.residues) for c in self.chains.values())

    @property
    def atom_count(self) -> int:
        return len(self.atoms)

    @property
    def ligand_names(self) -> List[str]:
        return list(set(a.residue_name for a in self.atoms if a.is_hetero))

@dataclass
class RamachandranRegion:
    favored_pct: float
    allowed_pct: float
    outlier_pct: float
    outliers: List[Tuple[int, str, float, float]]  # (res_num, res_name, phi, psi)

@dataclass
class AlignmentResult:
    rmsd: float
    aligned_pairs: int
    transformation_matrix: List[List[float]]
    mobile_alignment: Structure
    aligned_residues: List[Tuple[str, int, str, int]]

@dataclass
class MolecularDynamicsSetup:
    topology_file: str
    coordinates_file: str
    force_field: str
    water_model: str
    box_type: str
    box_dimensions: Tuple[float, float, float]
    ion_concentration: float
    temperature: float
    timestep: float
```

## Deployment Guide

### Installation

```bash
# Install from PyPI
pip install protein-structure[all]

# Install with specific backends
pip install protein-structure[openmm,gromacs,foldx]

# Install from source
git clone https://github.com/example/protein-structure.git
cd protein-structure
pip install -e ".[dev,test]"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install OpenMM
RUN conda install -c conda-forge openmm=8.0

# Install DSSP
RUN conda install -c conda-forge dssp

# Install Python package
RUN pip install protein-structure[openmm]

ENTRYPOINT ["protein-analyzer"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: protein-analysis
spec:
  replicas: 3
  selector:
    matchLabels:
      app: protein-analysis
  template:
    metadata:
      labels:
        app: protein-analysis
    spec:
      containers:
      - name: analysis
        image: protein-structure:2.0.0
        resources:
          requests:
            memory: "8Gi"
            cpu: "4"
          limits:
            memory: "32Gi"
            cpu: "8"
            nvidia.com/gpu: "1"
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: structure-data-pvc
```

## Monitoring and Observability

### Quality Metrics

```python
from protein_structure import StructureMonitor

monitor = StructureMonitor(metrics_backend="statsd")

# Track structure processing metrics
monitor.gauge("structure.atom_count", structure.atom_count)
monitor.gauge("quality.molprobity", quality.molprobity_score)
monitor.gauge("quality.clashscore", quality.clashscore)
monitor.gauge("quality.rama_favored", quality.rama_favored_pct)

# Track analysis throughput
monitor.increment("structures.parsed", tags=["format:pdb"])
monitor.timing("analysis.quality_assessment", elapsed_ms)
```

### Pipeline Monitoring

- Track structure parsing success/failure rates
- Monitor quality assessment scores across datasets
- Alert on structures with quality scores below thresholds
- Track memory usage during large structure processing
- Monitor cache hit rates for repeated structure lookups
- Report on alignment convergence and RMSD distributions
- Track mutation analysis completion rates

## Testing Strategy

### Unit Tests

```python
import pytest
from protein_structure import StructureParser, QualityAssessor

def test_parse_pdb():
    parser = StructureParser("test_data/1crn.pdb")
    structure = parser.parse()
    assert structure.atom_count > 0
    assert len(structure.chains) == 1

def test_quality_assessment():
    structure = StructureParser("test_data/1crn.pdb").parse()
    assessor = QualityAssessor(structure)
    report = assessor.comprehensive_report()
    assert report.rama_favored_pct > 95
    assert report.clashscore < 10

def test_binding_site_detection():
    structure = StructureParser("test_data/1hsg.pdb").parse()
    detector = BindingSiteDetector(structure, min_volume=100)
    pockets = detector.detect()
    assert len(pockets) > 0
    assert pockets[0].volume > 100
```

### Integration Tests

```python
@pytest.mark.integration
def test_mutation_analysis_pipeline():
    structure = StructureParser("test_data/kinase.pdb").parse()
    analyzer = MutationAnalyzer(structure)
    result = analyzer.predict("L858R", analysis_type="stability")
    assert result.ddG is not None
    assert result.classification in ["stabilizing", "neutral", "destabilizing"]

@pytest.mark.integration
def test_md_setup():
    from protein_structure import MDSimulator
    sim = MDSimulator(force_field="charmm36")
    system = sim.prepare(structure="test_data/protein.pdb", box_padding=1.0)
    assert system.topology_file.exists()
    assert system.coordinates_file.exists()
```

## Versioning and Migration

### Semantic Versioning

- **Major** (X.0.0): Breaking API changes, new format support dropping old versions
- **Minor** (0.X.0): New analysis methods, new tool integrations, backward-compatible
- **Patch** (0.0.X): Bug fixes, improved accuracy, documentation updates

### Migration Guide (v1.x → v2.0)

```python
# v1.x (deprecated)
from protein_structure.v1 import PDBParser
parser = PDBParser("structure.pdb")

# v2.0 (current)
from protein_structure import StructureParser
parser = StructureParser("structure.pdb")
structure = parser.parse()
```

### Compatibility Matrix

| Version | OpenMM | GROMACS | FoldX | AlphaFold |
|---------|--------|---------|-------|-----------|
| 2.0.x   | 8.0+   | 2023+   | 6+    | 2.3+      |
| 1.5.x   | 7.7+   | 2020+   | 5+    | 2.0+      |
| 1.0.x   | 7.5+   | 2019+   | 5+    | N/A       |

## Glossary

| Term | Definition |
|------|-----------|
| **RMSD** | Root Mean Square Deviation — average distance between superimposed atoms |
| **SASA** | Solvent-Accessible Surface Area — surface area accessible to solvent probe |
| **pLDDT** | predicted Local Distance Difference Test — AlphaFold per-residue confidence |
| **DSSP** | Dictionary of Secondary Structure of proteins — standard SS assignment |
| **FoldX** | Protein design and analysis suite for predicting mutation effects |
| **FPocket** | Geometric pocket detection algorithm based on Voronoi tessellation |
| **CHARMM** | Chemistry at Harvard Macromolecular Mechanics — molecular dynamics force field |
| **AMBER** | Assisted Model Building with Energy Refinement — MD force field |
| **DOPE** | Discrete Optimized Protein Energy — model quality assessment score |
| **Kabsch** | Algorithm for optimal superposition of two sets of structures |
| **ICP** | Iterative Closest Point — algorithm for aligning point clouds |
| **PDB** | Protein Data Bank — repository for 3D structural data |
| **mmCIF** | macromolecular Crystallographic Information File — modern PDB format |
| **PDBQT** | PDB format with partial charges — used for molecular docking |

## Changelog

### v2.0.0 (2024-06-15)
- Added AlphaFold structure integration and confidence filtering
- Added molecular dynamics setup for GROMACS and OpenMM
- Added GPU-accelerated SASA and distance calculations
- Added ChimeraX session export
- Improved binding site detection accuracy

### v1.5.0 (2024-01-10)
- Added PyMOL script generation
- Added PyRosetta interface
- Added structural alignment with ICP algorithm
- Improved mutation impact prediction accuracy

### v1.0.0 (2023-09-01)
- Initial release with PDB/CIF parsing
- Quality assessment (Ramachandran, clashscore, rotamers)
- Binding site detection (FPocket)
- Mutation analysis (FoldX interface)

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Write tests for all new functionality
3. Run the full test suite: `pytest tests/ -v --cov=protein_structure`
4. Update documentation for API changes
5. Follow PEP 8 and type hint conventions
6. Add changelog entries for user-facing changes
7. Submit a pull request with clear description

### Development Setup

```bash
git clone https://github.com/example/protein-structure.git
cd protein-structure
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Protein Structure Analysis Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
