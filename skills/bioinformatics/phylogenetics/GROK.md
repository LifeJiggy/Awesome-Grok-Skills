---
name: "phylogenetics"
category: "bioinformatics"
version: "2.0.0"
tags: ["bioinformatics", "phylogenetics", "tree-building", "evolutionary-analysis", "molecular-evolution"]
---

# Phylogenetics

## Overview

The Phylogenetics module provides tools for constructing, analyzing, and visualizing evolutionary trees from molecular sequence data. It supports distance-based methods (Neighbor-Joining, UPGMA), maximum-parsimony, and maximum-likelihood tree inference. The module includes bootstrap support estimation, tree topology comparison, molecular clock analysis, ancestral state reconstruction, and divergence time estimation.

This skill is used by evolutionary biologists, population geneticists, microbiologists studying pathogen evolution, and bioinformaticians performing comparative genomics across species or within populations.

## Core Capabilities

- **Tree Construction**: Neighbor-Joining (NJ), UPGMA, maximum parsimony, and maximum likelihood (simplified)
- **Distance Models**: Jukes-Cantor, Kimura 2-parameter, p-distance, Poisson correction for nucleotide substitution
- **Bootstrap Analysis**: Non-parametric bootstrap for branch support estimation (100-1000 replicates)
- **Tree Comparison**: Robinson-Foulds distance, symmetric difference, subtree pruning and regrafting (SPR) moves
- **Ancestral State Reconstruction**: Maximum parsimony and maximum likelihood reconstruction of ancestral sequences
- **Molecular Clock**: Strict and relaxed clock models for divergence time estimation
- **Selection Analysis**: dN/dS (Ka/Ks) ratio calculation for coding sequences, site-model tests for positive selection
- **Tree Formats**: Newick parser and writer, Nexus format support, JSON tree representation
- **Divergence Time**: Ultrametric tree generation from dated tips or calibration points

## Usage Examples

```python
from phylogenetics import (
    TreeBuilder,
    DistanceModel,
    PhylogeneticTree,
    SelectionAnalyzer,
    AncestralReconstructor,
)

# --- Distance Matrix from Alignment ---
sequences = {
    "Human":     "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "Chimpanzee": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "Gorilla":   "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "Orangutan": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "Mouse":     "MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFLGFPTTKTYFPHFDLSH",
}

builder = TreeBuilder(model=DistanceModel.JUKES_CANTOR)

# --- Neighbor-Joining Tree ---
nj_tree = builder.neighbor_joining(sequences)
print("Newick:", nj_tree.to_newick())
print(f"Leaf count: {nj_tree.leaf_count}")
print(f"Internal nodes: {nj_tree.internal_node_count}")

# --- Bootstrap Support ---
bootstrap_tree = builder.bootstrap(
    sequences,
    method="nj",
    replicates=100,
    seed=42,
)
for node in bootstrap_tree.internal_nodes:
    print(f"  Branch {node.label}: support={node.bootstrap_value}%")

# --- UPGMA Tree ---
upgma_tree = builder.upgma(sequences)
print("UPGMA Newick:", upgma_tree.to_newick())

# --- Tree Comparison ---
rf_distance = nj_tree.robinson_foulds(upgma_tree)
print(f"Robinson-Foulds distance: {rf_distance}")

# --- Selection Analysis (dN/dS) ---
analyzer = SelectionAnalyzer()
result = analyzer.calculate_kaks(
    query="ATGAAACTGGTGGCGCTG",
    reference="ATGAAACTGGTGGCGCTG",
)
print(f"Ka/Ks ratio: {result.kaks_ratio:.4f}")
print(f"Ka: {result.ka:.4f}  Ks: {result.ks:.4f}")
print(f"Selection: {result.interpretation}")

# --- Ancestral Reconstruction ---
reconstructor = AncestralReconstructor()
ancestral = reconstruct(sequences, nj_tree)
print(f"Root sequence: {ancestral.root_sequence}")
for node_label, seq in ancestral.node_sequences.items():
    print(f"  {node_label}: {seq[:30]}...")
```

## Best Practices

- Use Neighbor-Joining for quick exploratory trees; use maximum likelihood for publication-quality phylogenies
- Always report bootstrap support values — branches with <70% support should be considered unreliable
- Use appropriate substitution models: JC69 for closely related sequences, K2P for moderate divergence
- Remove gap-only columns from alignments before tree building
- Check for and remove saturation in third codon positions for deep phylogenies
- Use likelihood ratio tests to compare substitution models (e.g., GTR+Gamma vs JC69)
- Root trees with an appropriate outgroup when possible
- For molecular clock analysis, use non-degenerate sites only
- Report both unrooted and rooted topologies when outgroup selection is ambiguous
- For selection analysis, use coding sequences only and ensure correct reading frame alignment

## Related Modules

- **sequence-alignment**: Input alignment generation for phylogenetic analysis
- **genomic-analysis**: SNP-based phylogenetics from whole-genome data
- **protein-structure**: Structural evolution and conserved structural motifs
- **drug-discovery**: Target family evolution for drug resistance analysis

---

## Advanced Configuration

### Maximum Likelihood Tree Inference

```python
from phylogenetics import MLTreeBuilder, SubstitutionModel

builder = MLTreeBuilder(
    model=SubstitutionModel.GTR_GAMMA,
    gamma_categories=4,
    invariant_sites=True,
    starting_trees=5,
    SPR_moves=5,
    nni_rounds=3,
)

# Build ML tree from alignment
tree = builder.build(
    alignment="alignment.phy",
    bootstrap=1000,
    threads=8,
    output_prefix="ml_tree",
)

print(f"Log-likelihood: {tree.log_likelihood:.2f}")
print(f"AIC: {tree.aic:.2f}")
print(f"BIC: {tree.bic:.2f}")

# Model selection
best_model = builder.select_model(
    alignment="alignment.phy",
    candidates=[
        SubstitutionModel.JC69,
        SubstitutionModel.K80,
        SubstitutionModel.HKY85,
        SubstitutionModel.GTR,
        SubstitutionModel.GTR_GAMMA,
    ],
    criterion="bic",
)
print(f"Best model: {best_model.name}")
print(f"BIC: {best_model.bic:.2f}")
```

### Coalescent-Based Species Tree

```python
from phylogenetics import CoalescentBuilder

coalescent = CoalescentBuilder(
    method="astral",  # or "MP-EST", "StarBEAST"
    weight_by_sequence_length=True,
)

# Build species tree from gene trees
gene_trees = [
    "gene1.nwk", "gene2.nwk", "gene3.nwk",
    "gene4.nwk", "gene5.nwk",
]

species_tree = coalescent.build(
    gene_trees=gene_trees,
    output="species_tree.nwk",
)

# Support via local posterior probability
for node in species_tree.internal_nodes:
    print(f"  {node.label}: LPP={node.local_posterior_probability:.3f}")
```

### Bayesian Phylogenetics

```python
from phylogenetics import BayesianTreeBuilder

bayesian = BayesianTreeBuilder(
    model="GTR+G+I",
    prior={
        "clock_rate": {"dist": "lognormal", "mean": 0.01, "sigma": 1.0},
        "tree_prior": "birth-death",
        "alpha_prior": {"dist": "exponential", "rate": 2.0},
    },
    mcmc={
        "generations": 10_000_000,
        "sample_every": 1000,
        "burnin": 2_500_000,
        "chains": 4,
    },
)

# Run MCMC
result = bayesian.run(
    alignment="alignment.nex",
    output_prefix="beast_run",
)

# Summarize posterior
summary = result.summarize(
    credible_interval=0.95,
    max_clade_credibility=True,
)

print(f"Posterior mean log-likelihood: {summary.mean_log_likelihood:.2f}")
print(f"ESS (effective sample size): {summary.min_ess}")
```

### Haplotype Network Construction

```python
from phylogenetics import HaplotypeNetwork

network = HaplotypeNetwork(
    method="median_joining",
    max_connections=3,
    treat_indels_as_missing=False,
)

# Build haplotype network from sequences
haplotype_net = network.build(
    sequences=sequences,
    distances="hamming",
)

# Export for visualization
haplotype_net.to_graphml("haplotype_network.graphml")
haplotype_net.to_popart_nex("haplotype_network.nex")

print(f"Haplotypes: {haplotype_net.haplotype_count}")
print(f"Private mutations: {haplotype_net.private_mutations}")
```

## Architecture Patterns

```
┌──────────────────────────────────────────────────────────┐
│               Phylogenetic Analysis Pipeline              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐   │
│  │  Input   │───▶│ Alignment│───▶│ Gap Removal /    │   │
│  │  Seqs    │    │ (MSA)    │    │ Trimming         │   │
│  └──────────┘    └──────────┘    └────────┬─────────┘   │
│                                           │             │
│  ┌────────────────────────────────────────┼─────────┐   │
│  │                                        │         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌▼────────┐│   │
│  │  │ Distance     │  │ Maximum      │  │ Bayesian││   │
│  │  │ Methods      │  │ Likelihood   │  │ MCMC    ││   │
│  │  │ ┌──────────┐ │  │ ┌──────────┐ │  │         ││   │
│  │  │ │ NJ       │ │  │ │ GTR+Γ    │ │  │         ││   │
│  │  │ ├──────────┤ │  │ │ HKY85    │ │  │         ││   │
│  │  │ │ UPGMA    │ │  │ │ JC69     │ │  │         ││   │
│  │  │ └──────────┘ │  │ └──────────┘ │  │         ││   │
│  │  └──────┬───────┘  └──────┬───────┘  └────┬────┘│   │
│  │         │                 │                │     │   │
│  └─────────┼─────────────────┼────────────────┼─────┘   │
│            │                 │                │          │
│  ┌─────────▼─────────────────▼────────────────▼─────┐   │
│  │              Unrooted Tree                        │   │
│  └──────────────────┬───────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐   │
│  │              Rooting (outgroup / midpoint)        │   │
│  └──────────────────┬───────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐   │
│  │              Support Assessment                   │   │
│  │  Bootstrap / Posterior Probability / SH-aLRT      │   │
│  └──────────────────┬───────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐   │
│  │              Analysis                             │   │
│  │  Divergence Time │ Ancestral State │ Selection   │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

```
Bootstrap Analysis Flow:

    Input Alignment (N sequences × M sites)
         │
    ┌────▼─────────────────────┐
    │ Resample M columns with  │
    │ replacement (N × M)      │
    └────┬─────────────────────┘
         │
    ┌────▼────────────────────┐
    │ Build tree from          │
    │ resampled alignment      │
    │ (replicate tree)         │
    └────┬────────────────────┘
         │
    ┌────▼────────────────────┐
    │ Record topology and      │
    │ branch lengths            │
    └────┬────────────────────┘
         │
         │  Repeat B times (B=100-1000)
         │
    ┌────▼────────────────────┐
    │ Count frequency of each  │
    │ bipartition across B      │
    │ replicate trees           │
    └────┬────────────────────┘
         │
    ┌────▼────────────────────┐
    │ Bootstrap support =       │
    │ frequency( bipartition )  │
    │ reported as percentage    │
    └─────────────────────────┘

    Branch support interpretation:
    ┌──────────────────────────────┐
    │  95-100%: Strong support    │
    │  80-94%:  Moderate support  │
    │  70-79%:  Weak support      │
    │  <70%:    Unreliable        │
    └──────────────────────────────┘
```

## Integration Guide

### Newick Format I/O

```python
from phylogenetics import NewickIO

newick = NewickIO()

# Parse Newick tree
tree = newick.read("tree.nwk")
print(f"Leaves: {tree.leaf_count}")
print(f"Internal nodes: {tree.internal_node_count}")

# Write Newick tree
newick.write(tree, "output.nwk", branch_lengths=True, internal_labels=True)

# Parse from string
tree = newick.from_string("((A:0.1,B:0.2):0.3,(C:0.4,D:0.5):0.6);")
```

### Nexus Format Support

```python
from phylogenetics import NexusIO

nexus = NexusIO()

# Parse Nexus file (with alignment and tree)
data = nexus.read("analysis.nex")
print(f"Taxa: {data.taxa}")
print(f"Characters: {data.characters}")
print(f"Trees: {len(data.trees)}")

# Write Nexus file
nexus.write(
    alignment=msa,
    trees=[tree1, tree2],
    output="combined.nex",
)
```

### JSON Tree Exchange

```python
from phylogenetics import JSONTreeIO

json_io = JSONTreeIO()

# Convert tree to JSON for web visualization
tree_json = json_io.to_json(tree)
print(tree_json)

# Parse JSON tree
tree = json_io.from_json(tree_json)

# Export for D3.js visualization
d3_data = json_io.to_d3_format(tree)
with open("tree_d3.json", "w") as f:
    json.dump(d3_data, f)
```

### Tree Visualization

```python
from phylogenetics import TreeVisualizer

viz = TreeVisualizer()

# Generate publication-quality tree image
viz.to_png(
    tree="species_tree.nwk",
    output="tree.png",
    format="png",
    dpi=300,
    layout="rectangular",
    branch_scale=1000,
    show_support=True,
    show_branch_lengths=True,
    taxa_font_size=10,
)

# Generate SVG for editing
viz.to_svg(tree="species_tree.nwk", output="tree.svg")

# Generate ASCII tree for terminal
ascii_tree = viz.to_ascii(tree, show_support=True, show_lengths=True)
print(ascii_tree)
```

## Performance Optimization

### Parallel Tree Building

```python
from phylogenetics import ParallelTreeBuilder

parallel = ParallelTreeBuilder(n_workers=16)

# Parallel bootstrap
bootstrap_trees = parallel.bootstrap(
    alignment="large_alignment.phy",
    method="ml",
    replicates=1000,
    model="GTR+G",
    threads_per_worker=4,
)

# Parallel MCMC chains
mcmc_results = parallel.run_mcmc(
    alignment="large_alignment.nex",
    chains=4,
    generations=10_000_000,
    threads_per_chain=4,
)
```

### Large Dataset Handling

```python
from phylogenetics import LargeDatasetTreeBuilder

builder = LargeDatasetTreeBuilder(
    strategy="divide_and_conquer",  # or "shortcut", "recursive"
    subset_size=50,
    overlap=10,
    merge_method="taxon插入",
)

# Build tree for thousands of sequences
tree = builder.build(
    alignment="huge_alignment.phy",
    method="nj",
    model="k2p",
    output="large_tree.nwk",
)
```

### Memory-Efficient Tree Storage

```python
from phylogenetics import CompactTree

# Compress tree for memory efficiency
compact = CompactTree(tree, compression="cladewise")
print(f"Memory: {compact.memory_bytes / 1024:.1f} KB (vs {tree.memory_bytes / 1024:.1f} KB original)")

# Load tree lazily (load nodes on demand)
lazy_tree = CompactTree.from_file("huge_tree.nwk", lazy=True)
root = lazy_tree.root
```

## Security Considerations

### Phylogenetic Data Security

- Never log raw sequences or alignment data in pipeline logs — use taxon names only
- Encrypt proprietary phylogenetic trees and alignments at rest
- Implement access controls on phylogenetic databases containing sensitive data
- Audit all tree building and analysis operations
- Use anonymized taxon names in shared results
- Secure backup of phylogenetic analysis data
- Implement data retention policies for phylogenetic results
- Use secure channels for remote tree building services

### Input Validation

```python
from phylogenetics import InputValidator

validator = InputValidator(
    max_taxa=10000,
    max_alignment_length=10_000_000,
    allowed_gap_proportion=0.5,
    min_sequence_count=3,
)

# Validate before tree building
is_valid, errors = validator.validate_alignment("alignment.phy")
if not is_valid:
    for error in errors:
        print(f"Validation error: {error}")
```

### Secure Analysis Environment

```python
from phylogenetics import SecureAnalysis

secure = SecureAnalysis(
    temp_dir="/secure/tmp",
    encryption_key="/secure/keys/analysis.key",
    audit_log="/var/log/phylo_audit.log",
)

# Run tree building with secure temporary storage
result = secure.run_tree_building(
    alignment="sensitive_alignment.phy",
    method="ml",
    user="researcher_jdoe",
    project="PRJ_2024_001",
)
```

## Troubleshooting Guide

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| NJ tree has negative branch lengths | Distance matrix not ultrametric | Use NJ with positive branch enforcement; try UPGMA |
| ML tree fails to converge | Poor starting tree or model misspecification | Use multiple starting trees; check model adequacy |
| Bootstrap values all below 50% | Sequences are too divergent or alignment is poor | Use BLOSUM45 matrix; check alignment quality |
| UPGMA produces unexpected topology | Assumption of equal rates violated | Use NJ instead of UPGMA; check for rate heterogeneity |
| Ancestral reconstruction has many ambiguous sites | Deep divergence or long branches | Use ML reconstruction with model; increase alignment depth |
| MCMC chain has low ESS | Chain too short or poor mixing | Increase generations; check for multimodality |
| Tree comparison shows large RF distance | Topologies are very different | Check for long-branch attraction; try different methods |
| dN/dS calculation gives NaN | No synonymous substitutions | Use pair of more divergent sequences; check codon alignment |
| Newick parsing fails on large trees | Memory or format issues | Use streaming parser; verify Newick syntax |
| Molecular clock test rejects clock | Rate heterogeneity across lineages | Use relaxed clock model; check for outlier lineages |
| Haplotype network is unconnected | Too many unique haplotypes | Increase max_connections; use median-joining with gapped sites |
| Tree rooting looks wrong | Incorrect outgroup | Verify outgroup identity; try midpoint rooting |

## API Reference

### TreeBuilder

```python
class TreeBuilder:
    def __init__(
        self,
        model: DistanceModel = DistanceModel.JUKES_CANTOR,
        gap_action: str = "exclude",
    ): ...

    def neighbor_joining(
        self,
        sequences: Dict[str, str],
        positive_branches: bool = True,
    ) -> PhylogeneticTree:
        """Build Neighbor-Joining tree."""

    def upgma(
        self,
        sequences: Dict[str, str],
    ) -> PhylogeneticTree:
        """Build UPGMA tree."""

    def bootstrap(
        self,
        sequences: Dict[str, str],
        method: str = "nj",
        replicates: int = 100,
        seed: int = None,
    ) -> PhylogeneticTree:
        """Build tree with bootstrap support."""

    def distance_matrix(
        self,
        sequences: Dict[str, str],
    ) -> DistanceMatrix:
        """Compute pairwise distance matrix."""
```

### PhylogeneticTree

```python
class PhylogeneticTree:
    root: TreeNode
    leaf_count: int
    internal_node_count: int
    total_branch_length: float

    def to_newick(self) -> str:
        """Export to Newick format."""

    def to_nexus(self) -> str:
        """Export to Nexus format."""

    def to_json(self) -> str:
        """Export to JSON format."""

    def robinson_foulds(self, other: "PhylogeneticTree") -> int:
        """Compute Robinson-Foulds distance."""

    def symmetric_difference(self, other: "PhylogeneticTree") -> int:
        """Compute symmetric difference."""

    def spr_distance(self, other: "PhylogeneticTree") -> int:
        """Estimate SPR distance."""

    def root_with_outgroup(self, outgroup: List[str]) -> "PhylogeneticTree":
        """Root tree with specified outgroup taxa."""

    def midpoint_root(self) -> "PhylogeneticTree":
        """Root tree at midpoint of longest path."""

    def ultrametric(self) -> "PhylogeneticTree":
        """Convert to ultrametric tree (all tips equidistant from root)."""

class TreeNode:
    label: str
    branch_length: float
    children: List["TreeNode"]
    is_leaf: bool
    bootstrap_value: float
    depth: float
```

### DistanceModel

```python
class DistanceModel:
    JUKES_CANTOR = "jc69"
    KIMURA_2PARAMETER = "k2p"
    P_DISTANCE = "p"
    POISSON_CORRECTION = "pc"
    TN93 = "tn93"
    GTR = "gtr"

    @staticmethod
    def from_name(name: str) -> "DistanceModel": ...

    def compute_distance(
        self,
        seq1: str,
        seq2: str,
        alphabet: str = "nucleotide",
    ) -> float:
        """Compute evolutionary distance between two sequences."""
```

### SelectionAnalyzer

```python
class SelectionAnalyzer:
    def calculate_kaks(
        self,
        query: str,
        reference: str,
        method: str = "codeml",
    ) -> KaKsResult:
        """Calculate dN/dS ratio for coding sequences."""

    def site_model_test(
        self,
        alignment: str,
        tree: PhylogeneticTree,
    ) -> SiteModelResult:
        """Test for positive selection using site models."""

    def branch_model_test(
        self,
        alignment: str,
        tree: PhylogeneticTree,
        foreground_branches: List[str],
    ) -> BranchModelResult:
        """Test for positive selection on specific branches."""

class KaKsResult:
    ka: float          # dN (nonsynonymous substitutions per site)
    ks: float          # dS (synonymous substitutions per site)
    kaks_ratio: float  # dN/dS ratio
    interpretation: str  # positive, purifying, neutral
    p_value: float
    confidence_interval: Tuple[float, float]
```

### AncestralReconstructor

```python
class AncestralReconstructor:
    def __init__(self, method: str = "parsimony"): ...

    def reconstruct(
        self,
        sequences: Dict[str, str],
        tree: PhylogeneticTree,
    ) -> AncestralResult:
        """Reconstruct ancestral sequences."""

class AncestralResult:
    root_sequence: str
    node_sequences: Dict[str, str]
    confidence_scores: Dict[str, Dict[str, float]]  # node → base → probability
    changes: List[Tuple[str, str, str, str]]  # (node, parent, from_base, to_base)
```

## Data Models

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

@dataclass
class TreeNode:
    label: str = ""
    branch_length: float = 0.0
    children: List["TreeNode"] = field(default_factory=list)
    parent: Optional["TreeNode"] = None
    is_leaf: bool = True
    bootstrap_value: float = 0.0
    depth: float = 0.0

    @property
    def descendants(self) -> List["TreeNode"]:
        """Get all descendant nodes."""

    @property
    def leaves(self) -> List["TreeNode"]:
        """Get all leaf descendants."""

    def distance_to(self, other: "TreeNode") -> float:
        """Compute path distance to another node."""

@dataclass
class PhylogeneticTree:
    root: TreeNode
    leaf_count: int
    internal_node_count: int
    total_branch_length: float

    @property
    def internal_nodes(self) -> List[TreeNode]:
        """Get all internal nodes."""

    @property
    def leaves(self) -> List[TreeNode]:
        """Get all leaf nodes."""

    def to_newick(self) -> str: ...
    def to_nexus(self) -> str: ...
    def to_json(self) -> str: ...
    def robinson_foulds(self, other: "PhylogeneticTree") -> int: ...

@dataclass
class DistanceMatrix:
    taxa: List[str]
    matrix: List[List[float]]

    def get_distance(self, taxon1: str, taxon2: str) -> float: ...

@dataclass
class KaKsResult:
    ka: float
    ks: float
    kaks_ratio: float
    interpretation: str
    p_value: float
    confidence_interval: Tuple[float, float]
    synonymous_sites: float
    nonsynonymous_sites: float

@dataclass
class AncestralResult:
    root_sequence: str
    node_sequences: Dict[str, str]
    confidence_scores: Dict[str, Dict[str, float]]
    changes: List[Tuple[str, str, str, str]]

@dataclass
class MolecularClockResult:
    clock_model: str
    log_likelihood: float
    rate_estimate: float
    rate_variance: float
    clock_test_p_value: float
    root_to_tip_regression_r2: float

@dataclass
class DivergenceTimeResult:
    node_ages: Dict[str, float]
    calibration_points: Dict[str, Tuple[float, float]]
    confidence_intervals: Dict[str, Tuple[float, float]]
    substitution_rate: float
    clock_model: str
```

## Deployment Guide

### Installation

```bash
# Install from PyPI
pip install phylogenetics[all]

# Install with specific backends
pip install phylogenetics[fasttree,iqtree]

# Install from source
git clone https://github.com/example/phylogenetics.git
cd phylogenetics
pip install -e ".[dev,test]"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    iqtree \
    fasttree \
    mafft \
    && rm -rf /var/lib/apt/lists/*

RUN pip install phylogenetics[all]

ENTRYPOINT ["phylo-analysis"]
```

### Kubernetes Deployment

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: phylogenetic-analysis
spec:
  template:
    spec:
      containers:
      - name: phylo
        image: phylogenetics:2.0.0
        command: ["phylo-analysis", "run", "--config", "/config/phylo.yaml"]
        resources:
          requests:
            memory: "16Gi"
            cpu: "8"
          limits:
            memory: "64Gi"
            cpu: "16"
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: phylo-data-pvc
      restartPolicy: Never
```

## Monitoring and Observability

### Tree Building Metrics

```python
from phylogenetics import PhyloMonitor

monitor = PhyloMonitor(metrics_backend="prometheus")

# Track tree building metrics
monitor.counter("trees.built", count)
monitor.histogram("tree.leaf_count", leaf_counts)
monitor.histogram("tree.bootstrap_mean", bootstrap_means)
monitor.timing("tree.build_duration_ms", durations)
monitor.gauge("tree.rf_distance", rf_distances)
```

### Quality Dashboards

- Monitor tree building completion rates and error rates
- Track bootstrap support distributions across runs
- Visualize model selection results
- Alert on convergence failures in MCMC
- Monitor memory usage during large tree building
- Track Robinson-Foulds distances between methods
- Report on divergence time estimation confidence intervals

## Testing Strategy

### Unit Tests

```python
import pytest
from phylogenetics import TreeBuilder, DistanceModel, PhylogeneticTree

def test_neighbor_joining():
    builder = TreeBuilder(model=DistanceModel.JUKES_CANTOR)
    sequences = {
        "A": "ACGTACGTACGT",
        "B": "ACGTACGTACGA",
        "C": "ACGTACGTTCGT",
    }
    tree = builder.neighbor_joining(sequences)
    assert tree.leaf_count == 3
    assert tree.to_newick().count("(") > 0

def test_distance_model():
    model = DistanceModel.JUKES_CANTOR
    dist = model.compute_distance("ACGT", "ACGA")
    assert 0 <= dist <= 1

def test_newick_roundtrip():
    from phylogenetics import NewickIO
    original = "((A:0.1,B:0.2):0.3,(C:0.4,D:0.5):0.6);"
    tree = NewickIO().from_string(original)
    output = tree.to_newick()
    assert "A" in output
    assert "B" in output
```

### Integration Tests

```python
@pytest.mark.integration
def test_full_phylogenetic_pipeline():
    sequences = {
        "Human": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
        "Chimp": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
        "Gorilla": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
        "Mouse": "MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFLGFPTTKTYFPHFDLSH",
    }
    builder = TreeBuilder(model=DistanceModel.JUKES_CANTOR)
    tree = builder.neighbor_joining(sequences)
    bootstrap_tree = builder.bootstrap(sequences, replicates=100)

    # All internal nodes should have support values
    for node in bootstrap_tree.internal_nodes:
        assert 0 <= node.bootstrap_value <= 100
```

## Versioning and Migration

### Semantic Versioning

- **Major** (X.0.0): Breaking API changes, new tree inference methods
- **Minor** (0.X.0): New distance models, new analysis methods, backward-compatible
- **Patch** (0.0.X): Bug fixes, performance improvements, documentation updates

### Migration Guide (v1.x → v2.0)

```python
# v1.x (deprecated)
from phylogenetics.v1 import BuildTree
tree = BuildTree.nj(sequences)

# v2.0 (current)
from phylogenetics import TreeBuilder, DistanceModel
builder = TreeBuilder(model=DistanceModel.JUKES_CANTOR)
tree = builder.neighbor_joining(sequences)
```

### Compatibility Matrix

| Version | IQ-TREE | FastTree | RAxML | BEAST |
|---------|---------|----------|-------|-------|
| 2.0.x   | 2.2+    | 2.1+     | 8.2+  | 1.10+ |
| 1.5.x   | 2.1+    | 2.0+     | 8.1+  | 1.8+  |
| 1.0.x   | 2.0+    | 1.0+     | 8.0+  | 1.8+  |

## Glossary

| Term | Definition |
|------|-----------|
| **Neighbor-Joining** | Distance-based tree building method minimizing total branch length |
| **UPGMA** | Unweighted Pair Group Method with Arithmetic Mean — assumes ultrametric tree |
| **Maximum Likelihood** | Tree inference maximizing probability of observed data given model |
| **Maximum Parsimony** | Tree inference minimizing number of evolutionary changes |
| **Bootstrap** | Resampling method to estimate branch support confidence |
| **Robinson-Foulds** | Metric measuring topological distance between two trees |
| **SPR** | Subtree Pruning and Regrafting — tree rearrangement operation |
| **dN/dS** | Ratio of nonsynonymous to synonymous substitution rates |
| **JC69** | Jukes-Cantor 1969 — simplest nucleotide substitution model |
| **K2P** | Kimura 2-Parameter — model with transition/transversion bias |
| **GTR** | General Time Reversible — most parameterized nucleotide model |
| **Gamma distribution** | Models rate heterogeneity among sites |
| **Molecular clock** | Hypothesis of constant evolutionary rate across lineages |
| **Coalescent** | Theory describing gene genealogy going back in time |
| **Ultrametric** | Tree where all tips are equidistant from root |

## Changelog

### v2.0.0 (2024-06-15)
- Added maximum likelihood tree building
- Added Bayesian MCMC inference
- Added coalescent species tree methods
- Added model selection framework
- Added haplotype network construction

### v1.5.0 (2024-01-10)
- Added Nexus format support
- Added JSON tree export
- Added tree visualization
- Improved bootstrap implementation

### v1.0.0 (2023-09-01)
- Initial release with NJ and UPGMA
- Distance models (JC69, K2P, p-distance)
- Bootstrap support estimation
- Robinson-Foulds tree comparison
- Newick format I/O

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Write tests for all new functionality
3. Run the full test suite: `pytest tests/ -v --cov=phylogenetics`
4. Update documentation for API changes
5. Follow PEP 8 style guidelines
6. Add changelog entries for user-facing changes
7. Submit a pull request with clear description

## License

MIT License

Copyright (c) 2024 Phylogenetics Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
