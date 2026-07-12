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
