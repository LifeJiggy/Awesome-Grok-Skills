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

---

## Advanced Configuration

### Custom Scoring Matrices

```python
from sequence_alignment import ScoringMatrix, MatrixBuilder

# Create custom scoring matrix from count data
builder = MatrixBuilder()
blosum_custom = builder.build_from_counts(
    count_file="substitution_counts.txt",
    gap_open=-11,
    gap_extend=-1,
    name="CUSTOM_BLOSUM",
)

# Create PAM matrix with custom evolutionary distance
pam250 = builder.pam_matrix(distance=250)
pam120 = builder.pam_matrix(distance=120)

# Use substitution frequency matrix
sfm = builder.substitution_frequency_matrix(
    alignments="training_alignments.a2m",
    output_matrix="SFM.txt",
)
```

### Advanced Gap Penalty Models

```python
from sequence_alignment import PairwiseAligner, GapPenalty

# Affine gap penalty (standard)
aligner = PairwiseAligner(
    gap_penalty=GapPenalty.affine(open=-10, extend=-1),
)

# Convex gap penalty (gaps become less costly as they grow)
aligner_convex = PairwiseAligner(
    gap_penalty=GapPenalty.convex(
        open=-12,
        extension_cost=lambda length: -1 * (1 - 0.5 * (length - 1) / 10),
    ),
)

# Position-specific gap penalties
aligner_positional = PairwiseAligner(
    gap_penalty=GapPenalty.position_specific(
        penalties={
            "loop_region": {"open": -5, "extend": -0.5},
            "helix_region": {"open": -15, "extend": -2},
            "sheet_region": {"open": -15, "extend": -2},
        },
    ),
)

# Free end-gap penalty (glocal alignment)
aligner_free = PairwiseAligner(
    gap_penalty=GapPenalty.free_endgap(
        query_endgap="free",
        target_endgap="free",
        internal_open=-10,
        internal_extend=-1,
    ),
)
```

### HMM-Based Profile Alignment

```python
from sequence_alignment import HMMAligner, ProfileHMM

# Build profile HMM from MSA
hmm_builder = ProfileHMM()
hmm = hmm_builder.build_from_msa(
    msa_file="training alignment.a2m",
    name="kinase_family",
)

# Search for matches
hits = hmm.search(
    database="proteins.fasta",
    e_value_threshold=0.001,
)

# Add sequence to profile using HMM
aligner = HMMAligner(hmm=hmm)
aligned = aligner.add_sequence("new_protein.fasta")
print(f"Alignment score: {aligned.score:.2f}")
print(f"E-value: {aligned.e_value:.2e}")

# Build HMM from multiple sequence alignment with secondary structure
hmm = hmm_builder.build_from_msa(
    msa_file="alignment.a2m",
    secondary_structure="ss_annotation.txt",
)
```

### Consistency-Based Alignment (T-Coffee Style)

```python
from sequence_alignment import ConsistencyAligner

aligner = ConsistencyAligner(
    method="t_coffee",
    pairwise_aligner="smith_waterman",
    scoring_matrix=ScoringMatrix.blosum62(),
    consistency_rounds=2,
    library_size=1000,
)

# Progressive alignment with consistency scoring
msa = aligner.align([
    "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
    "MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFLGFPTTKTYFPHFDLSH",
    "MVLSAADKNNVKGIFTKIAGHAEEYGAETLERMFTTYPPTKTYFPHFDLSH",
    "MVHWTAEEKQLITGLWGKVNVAECGAEALARLLIVYPWTQRFFASFGNLSS",
])

print(f"Alignment score: {msa.score:.2f}")
print(f"Consistency score: {msa.consistency_score:.3f}")
```

## Architecture Patterns

```
┌─────────────────────────────────────────────────────────┐
│              Sequence Alignment Architecture             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Input Layer                          │  │
│  │  FASTA │ Raw strings │ GenBank │ UniProt          │  │
│  └────────────────────┬─────────────────────────────┘  │
│                       │                                 │
│  ┌────────────────────▼─────────────────────────────┐  │
│  │           Sequence Processing                     │  │
│  │  - Parse & validate                              │  │
│  │  - Remove gaps / mask low-complexity              │  │
│  │  - Translate nucleotide → protein                 │  │
│  └────────────────────┬─────────────────────────────┘  │
│                       │                                 │
│         ┌─────────────┼─────────────┐                  │
│         │             │             │                  │
│  ┌──────▼──────┐ ┌───▼────┐ ┌─────▼─────┐            │
│  │  Pairwise   │ │  MSA   │ │ Database  │            │
│  │  Alignment  │ │ Engine │ │  Search   │            │
│  │  ┌────────┐ │ │        │ │           │            │
│  │  │ Needle-│ │ │Progr.  │ │ Seed &    │            │
│  │  │ man-   │ │ │Consist.│ │ Extend    │            │
│  │  │ Wunsch │ │ │Iterate │ │ Heuristic │            │
│  │  ├────────┤ │ │Profile │ │           │            │
│  │  │ Smith- │ │ │  HMM   │ │           │            │
│  │  │Waterman│ │ │        │ │           │            │
│  │  └────────┘ │ └───┬────┘ └─────┬─────┘            │
│  └──────┬──────┘     │            │                  │
│         │            │            │                  │
│  ┌──────▼────────────▼────────────▼──────┐           │
│  │          Alignment Result              │           │
│  │  - Score / E-value                    │           │
│  │  - Aligned sequences with gaps        │           │
│  │  - Statistics (identity, similarity)  │           │
│  └───────────────┬───────────────────────┘           │
│                  │                                    │
│         ┌────────┼────────┐                          │
│         │        │        │                          │
│  ┌──────▼──┐ ┌──▼───┐ ┌──▼──────────┐              │
│  │Phylo-   │ │Motif │ │ Structural  │              │
│  │genetics │ │Discov│ │ Modeling    │              │
│  └─────────┘ └──────┘ └─────────────┘              │
└─────────────────────────────────────────────────────┘
```

```
BLAST-like Search Heuristic:

    Query Sequence
         │
    ┌────▼────────────┐
    │ Seed Generation │
    │ k-mer words     │
    │ (k=2-15)        │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Hit Table Lookup │
    │ Exact word matches│
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Ungapped Extension│
    │ Extend matches    │
    │ Score drops below │
    │ threshold → stop  │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Gapped Extension │
    │ Add gaps to find │
    │ optimal alignment│
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Score Evaluation │
    │ Compute E-value  │
    │ from score dist. │
    └────┬────────────┘
         │
    ┌────▼────────────┐
    │ Statistical Test │
    │ E-value < 0.01   │
    │ → Report hit     │
    └─────────────────┘
```

## Integration Guide

### FASTA Format Support

```python
from sequence_alignment import FASTAParser

parser = FASTAParser()

# Parse single sequence
seq = parser.parse_file("sequence.fasta")
print(f"ID: {seq.id}")
print(f"Description: {seq.description}")
print(f"Length: {len(seq.sequence)}")
print(f"Sequence: {seq.sequence[:50]}...")

# Parse multiple sequences
sequences = parser.parse_file("multi_sequences.fasta")
print(f"Parsed {len(sequences)} sequences")

# Parse from string
seq = parser.parse_string(">test_seq\\nMKTLLIAAALLVA")
```

### GenBank Integration

```python
from sequence_alignment import GenBankFetcher

fetcher = GenBankFetcher()

# Fetch sequence by accession
record = fetcher.fetch("NM_001256799.3")
print(f"Organism: {record.organism}")
print(f"Gene: {record.gene}")
print(f"Sequence length: {len(record.sequence)}")

# Fetch coding sequence
cds = fetcher.fetch_cds("NM_001256799.3")
print(f"CDS length: {len(cds.sequence)} bp")
print(f"Protein: {cds.protein_sequence[:50]}...")
```

### BLAST Database Creation

```python
from sequence_alignment import BLASTDBManager

db_manager = BLASTDBManager()

# Create BLAST database from FASTA
db_manager.makeblastdb(
    input_fasta="proteins.fasta",
    db_type="prot",  # "prot" or "nucl"
    db_name="custom_proteins",
    title="Custom Protein Database",
    parse_seqids=True,
)

# Search against custom database
from sequence_alignment import DatabaseSearcher
searcher = DatabaseSearcher(
    database="custom_proteins",
    program="blastp",
    e_value_threshold=0.001,
)

hits = searcher.search("query.fasta")
for hit in hits[:10]:
    print(f"  {hit.subject_id}: e_value={hit.e_value:.2e}, identity={hit.identity_pct:.1f}%")
```

## Performance Optimization

### Parallel Alignment

```python
from sequence_alignment import ParallelAligner

parallel = ParallelAligner(n_workers=16)

# Parallel pairwise alignments
pairs = [("seq1", "seqA"), ("seq2", "seqB"), ("seq3", "seqC")]
results = parallel.align_pairs(
    pairs=pairs,
    method="smith_waterman",
    scoring_matrix=ScoringMatrix.blosum62(),
)

# Parallel database search
hits = parallel.search_database(
    queries=["query1.fasta", "query2.fasta"],
    database="large_proteins.fasta",
    program="blastp",
)
```

### Index-Based Searching

```python
from sequence_alignment import SequenceIndex

# Build k-mer index for fast exact matching
index = SequenceIndex(k=6)
index.build("proteins.fasta")

# Fast exact subsequence search
results = index.exact_search("MVLSPADK", max_hits=100)
print(f"Found {len(results)} exact matches")

# Approximate search with up to 2 mismatches
results = index.approximate_search(
    query="MVLSPADK",
    max_mismatches=2,
    max_hits=50,
)
```

### Memory-Efficient Alignment

```python
from sequence_alignment import StreamingAligner

# Align large sequences without loading all into memory
aligner = StreamingAligner(
    method="smith_waterman",
    chunk_size=10000,
    overlap=500,
)

# Stream alignment of very long sequences
result = aligner.align(
    query="long_sequence.fasta",
    target="reference.fasta",
    output="alignment_result.a2m",
)

# Progressive alignment with disk-based intermediate storage
from sequence_alignment import ProgressiveAlignerDisk

aligner = ProgressiveAlignerDisk(
    temp_dir="/scratch/msa_temp",
    max_memory_gb=8,
)
msa = aligner.align("large_dataset.fasta")
```

## Security Considerations

### Sequence Data Security

- Never log raw sequences in pipeline output files — use sequence IDs only
- Encrypt proprietary sequences and alignments at rest
- Validate input sequences before alignment — malformed input can cause buffer overflows
- Use secure channels for remote database searches
- Implement access controls on proprietary sequence databases
- Audit all sequence database access operations
- Use anonymized sequence IDs in shared alignment results
- Implement data retention policies for alignment outputs

### Input Validation

```python
from sequence_alignment import InputValidator

validator = InputValidator(
    max_sequence_length=1_000_000,
    max_sequence_count=10_000,
    allowed_alphabets=["protein", "nucleotide"],
    reject_invalid_characters=True,
)

# Validate before alignment
is_valid, errors = validator.validate("input.fasta")
if not is_valid:
    for error in errors:
        print(f"Validation error: {error}")
```

### Secure Database Operations

```python
from sequence_alignment import SecureBLASTDB

secure_db = SecureBLASTDB(
    encryption_key="/secure/keys/db.key",
    audit_log="/var/log/blast_audit.log",
)

# Encrypted database creation
secure_db.makeblastdb(
    input_fasta="proprietary_proteins.fasta",
    db_name="encrypted_proteins",
    encrypt=True,
)

# Search with access logging
results = secure_db.search(
    query="query.fasta",
    user="researcher_jdoe",
    project="PRJ_2024_001",
)
```

## Troubleshooting Guide

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| Needleman-Wunsch produces too many gaps | Gap penalties too low | Increase gap_open to -12 to -15 for proteins |
| Smith-Waterman returns empty alignment | Query and target share no similarity | Lower threshold or check input sequences |
| MSA has very low conservation | Sequences are too divergent | Use BLOSUM45; check if sequences are homologous |
| BLAST search returns no hits | E-value threshold too strict | Increase e_value_threshold to 0.01 or 0.1 |
| Pairwise distance matrix has negative values | Substitution model mismatch | Use p-distance for divergent sequences |
| MSA is extremely slow | Too many sequences | Pre-filter by length; use representative sequences |
| Custom scoring matrix produces odd scores | Matrix not normalized | Verify substitution counts are from aligned pairs |
| Profile HMM search has high false positives | HMM is overfitted | Reduce consensus threshold; increase training data |
| Nucleotide alignment has frameshifts | Input contains sequencing errors | Consider translated alignment (tblastx) |
| E-values differ between runs | Database size changed | E-values depend on database size — report size |
| Alignment output is truncated | Terminal width limit | Use `--full` output flag or redirect to file |
| Gaps appear at biologically impossible positions | Gap penalties inappropriate for region | Use position-specific gap penalties |

## API Reference

### PairwiseAligner

```python
class PairwiseAligner:
    def __init__(
        self,
        scoring_matrix: ScoringMatrix = None,
        gap_open: int = -10,
        gap_extend: int = -1,
        gap_penalty: GapPenalty = None,
    ): ...

    def global_align(
        self,
        query: str,
        target: str,
        free_endgap: bool = False,
    ) -> AlignmentResult:
        """Perform global (Needleman-Wunsch) alignment."""

    def local_align(
        self,
        query: str,
        target: str,
    ) -> LocalAlignmentResult:
        """Perform local (Smith-Waterman) alignment."""

    def semi_global_align(
        self,
        query: str,
        target: str,
    ) -> AlignmentResult:
        """Perform semi-global (glocal) alignment."""

class AlignmentResult:
    score: float
    aligned_query: str
    aligned_target: str
    alignment_string: str
    identity: int
    identity_pct: float
    similarity_pct: float
    gaps: int
    gap_openings: int
    query_start: int
    query_end: int
    target_start: int
    target_end: int

class LocalAlignmentResult(AlignmentResult):
    query_start: int
    query_end: int
    target_start: int
    target_end: int
```

### MultipleAligner

```python
class MultipleAligner:
    def __init__(
        self,
        method: str = "progressive",
        scoring_matrix: ScoringMatrix = None,
        gap_open: int = -10,
        gap_extend: int = -1,
        iteration_rounds: int = 2,
    ): ...

    def align(
        self,
        sequences: List[str],
        sequence_ids: List[str] = None,
    ) -> MSA:
        """Perform multiple sequence alignment."""

    def distance_matrix(
        self,
        sequences: Dict[str, str],
        model: str = "identity",
    ) -> Dict[str, Dict[str, float]]:
        """Compute pairwise distance matrix from sequences."""

class MSA:
    sequences: Dict[str, str]
    alignment_length: int
    num_sequences: int
    score: float
    consensus: str
    conservation_scores: List[float]
    gap_columns: List[int]
    identity_matrix: Dict[str, Dict[str, float]]

    def gap_free_columns(self) -> int:
        """Count columns without gaps."""

    def column_conservation(self, column: int) -> float:
        """Compute conservation score for a column (0-1)."""

    def to_fasta(self, filepath: str = None) -> str:
        """Export MSA to FASTA format."""

    def to_stockholm(self, filepath: str = None) -> str:
        """Export MSA to Stockholm format."""

    def to_a2m(self, filepath: str = None) -> str:
        """Export MSA to A2M format."""
```

### DatabaseSearcher

```python
class DatabaseSearcher:
    def __init__(
        self,
        scoring_matrix: ScoringMatrix = None,
        word_size: int = 3,
        e_value_threshold: float = 0.01,
        max_hits: int = 500,
        gap_open: int = -10,
        gap_extend: int = -1,
    ): ...

    def search(
        self,
        query: str,
        database: List[str] = None,
        database_path: str = None,
        program: str = "auto",
    ) -> List[SearchHit]:
        """Search database with query sequence."""

class SearchHit:
    query_id: str
    subject_id: str
    score: float
    bit_score: float
    e_value: float
    identity: int
    identity_pct: float
    similarity_pct: float
    gaps: int
    query_start: int
    query_end: int
    subject_start: int
    subject_end: int
    aligned_query: str
    aligned_subject: str
    coverage_pct: float
```

### ScoringMatrix

```python
class ScoringMatrix:
    @staticmethod
    def blosum45() -> "ScoringMatrix": ...
    @staticmethod
    def blosum62() -> "ScoringMatrix": ...
    @staticmethod
    def blosum80() -> "ScoringMatrix": ...
    @staticmethod
    def pam250() -> "ScoringMatrix": ...
    @staticmethod
    def pam120() -> "ScoringMatrix": ...
    @staticmethod
    def nucleotide(match: int = 1, mismatch: int = -2) -> "ScoringMatrix": ...

    def score(self, a: str, b: str) -> int:
        """Score substitution of residue a with b."""

    def from_file(self, filepath: str) -> "ScoringMatrix":
        """Load custom matrix from file."""
```

## Data Models

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

@dataclass
class Sequence:
    id: str
    description: str
    sequence: str
    alphabet: str  # "protein", "dna", "rna"

    @property
    def length(self) -> int:
        return len(self.sequence)

    @property
    def gc_content(self) -> float:
        gc = sum(1 for c in self.sequence if c in "GC")
        return gc / len(self.sequence) if self.sequence else 0

@dataclass
class AlignmentResult:
    score: float
    aligned_query: str
    aligned_target: str
    alignment_string: str
    identity: int
    identity_pct: float
    similarity_pct: float
    gaps: int
    gap_openings: int
    query_start: int
    query_end: int
    target_start: int
    target_end: int
    query_id: str = ""
    target_id: str = ""

@dataclass
class LocalAlignmentResult(AlignmentResult):
    pass

@dataclass
class MSA:
    sequences: Dict[str, str]
    alignment_length: int
    num_sequences: int
    score: float
    consensus: str
    conservation_scores: List[float]
    gap_columns: List[int]

@dataclass
class SearchHit:
    query_id: str
    subject_id: str
    score: float
    bit_score: float
    e_value: float
    identity: int
    identity_pct: float
    similarity_pct: float
    gaps: int
    query_start: int
    query_end: int
    subject_start: int
    subject_end: int
    aligned_query: str
    aligned_subject: str
    coverage_pct: float

@dataclass
class DistanceMatrix:
    sequences: List[str]
    matrix: List[List[float]]

    def get_distance(self, seq1: str, seq2: str) -> float:
        """Get distance between two sequences."""

@dataclass
class AlignmentStatistics:
    total_columns: int
    gap_free_columns: int
    percent_identity: float
    percent_similarity: float
    percent_gaps: float
    conserved_columns: int
    variable_columns: int
    parsimony_informative_sites: int
    singletons: int
    total_sites: int

@dataclass
class ProfileHMM:
    name: str
    length: int
    alphabet: str
    match_states: List[Dict[str, float]]
    insert_states: List[Dict[str, float]]
    delete_states: List[Dict[str, float]]
    transition_probs: Dict[str, Dict[str, float]]
```

## Deployment Guide

### Installation

```bash
# Install from PyPI
pip install sequence-alignment[all]

# Install with specific backends
pip install sequence-alignment[blast,hs-blast]

# Install from source
git clone https://github.com/example/sequence-alignment.git
cd sequence-alignment
pip install -e ".[dev,test]"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ncbi-blast+ \
    hmmer \
    && rm -rf /var/lib/apt/lists/*

RUN pip install sequence-alignment[all]

ENTRYPOINT ["seq-align"]
```

### Kubernetes Deployment

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: alignment-batch
spec:
  template:
    spec:
      containers:
      - name: aligner
        image: sequence-alignment:2.0.0
        command: ["seq-align", "batch", "--config", "/config/alignment.yaml"]
        resources:
          requests:
            memory: "8Gi"
            cpu: "4"
          limits:
            memory: "32Gi"
            cpu: "8"
        volumeMounts:
        - name: sequences
          mountPath: /data/sequences
      volumes:
      - name: sequences
        persistentVolumeClaim:
          claimName: sequence-data-pvc
      restartPolicy: Never
```

## Monitoring and Observability

### Alignment Metrics

```python
from sequence_alignment import AlignmentMonitor

monitor = AlignmentMonitor(metrics_backend="statsd")

# Track alignment statistics
monitor.counter("alignments.completed", count)
monitor.histogram("alignment.score", scores)
monitor.histogram("alignment.identity_pct", identity_pcts)
monitor.timing("alignment.duration_ms", elapsed)

# Track search statistics
monitor.gauge("search.hits_per_query", avg_hits)
monitor.histogram("search.e_values", e_values)
```

### Quality Dashboards

- Monitor alignment completion rates and error rates
- Track identity distribution across alignment runs
- Visualize E-value distributions for database searches
- Alert on anomalous alignment scores
- Monitor database search throughput
- Track memory usage during large MSA runs
- Report on sequence coverage statistics

## Testing Strategy

### Unit Tests

```python
import pytest
from sequence_alignment import PairwiseAligner, ScoringMatrix

def test_needleman_wunsch():
    aligner = PairwiseAligner(scoring_matrix=ScoringMatrix.blosum62())
    result = aligner.global_align("AGTACGCA", "TATGC")
    assert result.score > 0
    assert result.identity > 0

def test_smith_waterman():
    aligner = PairwiseAligner(scoring_matrix=ScoringMatrix.blosum62())
    result = aligner.local_align("HEAGAWGHEE", "PAWHEAE")
    assert result.score > 0
    assert result.identity > 0

def test_scoring_matrix():
    matrix = ScoringMatrix.blosum62()
    assert matrix.score("A", "A") > 0
    assert matrix.score("A", "D") < 0
```

### Integration Tests

```python
@pytest.mark.integration
def test_msa_pipeline():
    from sequence_alignment import MultipleAligner
    aligner = MultipleAligner(method="progressive")
    msa = aligner.align([
        "HEAGAWGHEE", "PAWHEAE", "HEAGAWGHEE", "PAWEAE"
    ])
    assert msa.num_sequences == 4
    assert msa.alignment_length > 0

@pytest.mark.integration
def test_database_search():
    from sequence_alignment import DatabaseSearcher
    searcher = DatabaseSearcher(e_value_threshold=0.01)
    hits = searcher.search(
        query="HEAGAWGHEE",
        database=["PAWHEAE", "HEAGAWGHEE"],
    )
    assert len(hits) > 0
```

## Versioning and Migration

### Semantic Versioning

- **Major** (X.0.0): Breaking API changes, new algorithm implementations
- **Minor** (0.X.0): New scoring matrices, new alignment methods, backward-compatible
- **Patch** (0.0.X): Bug fixes, performance improvements, documentation updates

### Migration Guide (v1.x → v2.0)

```python
# v1.x (deprecated)
from sequence_alignment.v1 import Align
result = Align.needleman_wunsch("seq1", "seq2")

# v2.0 (current)
from sequence_alignment import PairwiseAligner, ScoringMatrix
aligner = PairwiseAligner(scoring_matrix=ScoringMatrix.blosum62())
result = aligner.global_align("seq1", "seq2")
```

### Compatibility Matrix

| Version | BLAST+ | HMMER | MUSCLE | BioPython |
|---------|--------|-------|--------|-----------|
| 2.0.x   | 2.14+  | 3.3+  | 5.0+   | 1.82+     |
| 1.5.x   | 2.12+  | 3.3+  | 3.8+   | 1.79+     |
| 1.0.x   | 2.10+  | 3.2+  | 3.8+   | 1.78+     |

## Glossary

| Term | Definition |
|------|-----------|
| **Needleman-Wunsch** | Global alignment algorithm using dynamic programming |
| **Smith-Waterman** | Local alignment algorithm using dynamic programming |
| **BLOSUM** | BLOcks SUbstitution Matrix — protein substitution matrix from aligned blocks |
| **PAM** | Point Accepted Mutation — protein substitution matrix from evolutionary model |
| **E-value** | Expected number of hits with equal or better score by chance |
| **Bit score** | Normalized alignment score independent of database size |
| **MSA** | Multiple Sequence Alignment — alignment of three or more sequences |
| **HMM** | Hidden Markov Model — probabilistic model for sequence profiles |
| **k-mer** | Subsequence of length k used as seed in heuristic search |
| **Scoring matrix** | Matrix of substitution scores for alignment |
| **Gap penalty** | Cost subtracted for inserting gaps in alignment |
| **Identity** | Percentage of aligned positions with identical residues |
| **Similarity** | Percentage of aligned positions with similar residues |
| **Coverage** | Percentage of query aligned to subject |
| **A2M** | aligned FASTA format with uppercase=match, lowercase=insert, -=delete |

## Changelog

### v2.0.0 (2024-06-15)
- Added HMM-based profile alignment
- Added consistency-based MSA (T-Coffee style)
- Added custom scoring matrix builder
- Added parallel alignment engine
- Added streaming alignment for long sequences

### v1.5.0 (2024-01-10)
- Added free end-gap alignment
- Added position-specific gap penalties
- Added convex gap penalty model
- Improved MSA iterative refinement

### v1.0.0 (2023-09-01)
- Initial release with Needleman-Wunsch and Smith-Waterman
- BLOSUM/PAM scoring matrices
- Progressive MSA
- BLAST-like database search
- E-value and bit score calculation

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Write tests for all new functionality
3. Run the full test suite: `pytest tests/ -v --cov=sequence_alignment`
4. Update documentation for API changes
5. Follow PEP 8 style guidelines
6. Add changelog entries for user-facing changes
7. Submit a pull request with clear description

## License

MIT License

Copyright (c) 2024 Sequence Alignment Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
