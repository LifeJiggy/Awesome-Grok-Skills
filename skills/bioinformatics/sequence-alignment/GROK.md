---
name: "sequence-alignment"
category: "bioinformatics"
version: "2.0.0"
tags: ["bioinformatics", "alignment", "BLAST", "Smith-Waterman", "Needleman-Wunsch", "MUSCLE"]
---

# Sequence Alignment

## Overview

The Sequence Alignment module provides implementations of classical and modern sequence alignment algorithms for DNA, RNA, and protein sequences. It covers global alignment (Needleman-Wunsch), local alignment (Smith-Waterman), multiple sequence alignment (MSA), profile-based alignment, and heuristic search methods (BLAST-like). The module supports custom scoring matrices, gap penalties, and extension penalties, and produces alignment objects suitable for downstream phylogenetic analysis, motif discovery, and structural modeling.

This skill is essential for bioinformaticians performing homology searches, constructing sequence alignments for tree building, identifying conserved domains, and comparing sequences across species or within protein families.

## Core Capabilities

- **Global Alignment**: Needleman-Wunsch algorithm with affine gap penalties for full-length sequence comparison
- **Local Alignment**: Smith-Waterman algorithm for finding highest-scoring local regions between sequences
- **Scoring Matrices**: BLOSUM45/62/80, PAM250 for proteins; simple match/mismatch for nucleotides; custom matrix support
- **Gap Penalties**: Linear, affine (gap open + gap extension), and free-endgap models
- **Multiple Sequence Alignment**: Progressive alignment (MUSCLE/Clustal-style), iterative refinement, consistency-based alignment (T-Coffee)
- **Profile Alignment**: HMM-based and profile-scoring alignment for adding sequences to an existing MSA
- **BLAST-like Search**: Seed-and-extend heuristic for fast database similarity searching
- **Alignment Statistics**: E-value calculation, bit scores, identity and similarity percentages, gap statistics
- **Pairwise Distance Matrix**: Convert alignments to evolutionary distance matrices for tree construction

## Usage Examples

```python
from sequence_alignment import (
    PairwiseAligner,
    MultipleAligner,
    ScoringMatrix,
    AlignmentResult,
    DatabaseSearcher,
)

# --- Global Alignment (Needleman-Wunsch) ---
aligner = PairwiseAligner(
    scoring_matrix=ScoringMatrix.blosum62(),
    gap_open=-10,
    gap_extend=-1,
)
result = aligner.global_align(
    query="HEAGAWGHEE",
    target="PAWHEAE",
)
print(f"Score: {result.score}")
print(f"Identity: {result.identity_pct:.1f}%")
print(f"Query:  {result.aligned_query}")
print(f"        {result.alignment_string}")
print(f"Target: {result.aligned_target}")

# --- Local Alignment (Smith-Waterman) ---
local = aligner.local_align(
    query="MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    target="MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFLGFPTTKTYFPHFDLSH",
)
print(f"Local score: {local.score}")
print(f"Query range: {local.query_start}-{local.query_end}")
print(f"Target range: {local.target_start}-{local.target_end}")

# --- Multiple Sequence Alignment ---
msa_aligner = MultipleAligner(
    method="progressive",
    scoring_matrix=ScoringMatrix.blosum62(),
)
msa = msa_aligner.align([
    "HEAGAWGHEE",
    "PAWHEAE",
    "HEAGAWGHEE",
    "PAWEAE",
])
for name, seq in msa.sequences.items():
    print(f"  {name}: {seq}")
print(f"  Consensus: {msa.consensus}")
print(f"  Conservation: {msa.conservation_scores}")

# --- Database Search (BLAST-like) ---
searcher = DatabaseSearcher(
    scoring_matrix=ScoringMatrix.blosum62(),
    word_size=3,
    e_value_threshold=0.01,
)
hits = searcher.search(
    query="HEAGAWGHEE",
    database=["PAWHEAE", "HEAGAWGHEE", "PAWEAE", "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"],
)
for hit in hits[:5]:
    print(f"  {hit.subject_id}: score={hit.score}, e_value={hit.e_value:.2e}, identity={hit.identity_pct:.1f}%")

# --- Pairwise Distance Matrix ---
sequences = {
    "Human": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "Gorilla": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "Mouse": "MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFLGFPTTKTYFPHFDLSH",
}
distances = msa_aligner.distance_matrix(sequences)
for sp1, row in distances.items():
    for sp2, dist in row.items():
        if sp1 < sp2:
            print(f"  {sp1} vs {sp2}: {dist:.4f}")
```

## Best Practices

- Use BLOSUM62 for general-purpose protein alignment; BLOSUM45 for distant homologs; BLOSUM80 for closely related sequences
- Set gap open penalty to -10 and gap extension to -1 for protein alignment (Henikoff & Henikoff)
- For nucleotide alignment, use match=+1, mismatch=-2 with gap open=-5, gap_extend=-2
- Always report E-values for database searches, not just raw scores — E-values are comparable across searches
- Use word_size=2 for protein and word_size=11 for nucleotide in BLAST-like searches
- For MSA, run 1-2 rounds of iterative refinement to improve accuracy
- Mask low-complexity regions before database searching to reduce false positive hits
- Use gap-free columns for phylogenetic analysis — columns with gaps introduce noise
- For closely related sequences (>95% identity), codon-based alignment is unnecessary
- Store alignment objects with sequence IDs, not just aligned strings, for traceability

## Related Modules

- **phylogenetics**: Build evolutionary trees from alignment output
- **genomic-analysis**: NGS read alignment and mapping
- **protein-structure**: Structure-level alignment for structural homology
- **drug-discovery**: Sequence-based target identification for drug design
