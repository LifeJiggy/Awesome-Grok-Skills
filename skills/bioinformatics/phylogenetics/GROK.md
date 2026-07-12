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
