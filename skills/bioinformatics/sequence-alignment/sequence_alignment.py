"""
Sequence Alignment Module
Needleman-Wunsch, Smith-Waterman, multiple alignment, BLAST-like search, and distance matrices.
"""

from __future__ import annotations

import logging
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AlignMode(Enum):
    GLOBAL = "global"
    LOCAL = "local"
    SEMI_GLOBAL = "semi_global"


class SequenceType(Enum):
    DNA = "dna"
    RNA = "rna"
    PROTEIN = "protein"


# ---------------------------------------------------------------------------
# Scoring Matrices
# ---------------------------------------------------------------------------

@dataclass
class ScoringMatrix:
    """A substitution scoring matrix."""
    name: str
    scores: Dict[Tuple[str, str], int] = field(default_factory=dict)

    def score(self, a: str, b: str) -> int:
        key1 = (a.upper(), b.upper())
        key2 = (b.upper(), a.upper())
        if key1 in self.scores:
            return self.scores[key1]
        if key2 in self.scores:
            return self.scores[key2]
        if a.upper() == b.upper():
            return 1
        return -1

    @classmethod
    def blosum62(cls) -> ScoringMatrix:
        matrix = cls(name="BLOSUM62")
        data = {
            "A": {"A": 4, "R": -1, "N": -2, "D": -2, "C": 0, "Q": -1, "E": -1, "G": 0, "H": -2, "I": -1,
                  "L": -1, "K": -1, "M": -1, "F": -2, "P": -1, "S": 1, "T": 0, "W": -3, "Y": -2, "V": 0},
            "R": {"R": 5, "N": 0, "D": -2, "E": -1, "C": -3, "Q": 1, "E": 0, "G": -2, "H": 0, "I": -3,
                  "L": -2, "K": 2, "M": -1, "F": -3, "P": -2, "S": -1, "T": -1, "W": -3, "Y": -2, "V": -3},
            "N": {"N": 6, "D": 1, "C": -2, "Q": 0, "E": 0, "G": 0, "H": -2, "I": -3, "L": -3, "K": 0,
                  "M": -2, "F": -3, "P": -2, "S": 1, "T": 0, "W": -4, "Y": -2, "V": -3},
            "D": {"D": 6, "C": -2, "Q": 0, "E": 2, "G": -1, "H": -1, "I": -3, "L": -4, "K": -1, "M": -3,
                  "F": -3, "P": -1, "S": 0, "T": -1, "W": -4, "Y": -3, "V": -3},
        }
        for aa1, row in data.items():
            for aa2, score in row.items():
                matrix.scores[(aa1, aa2)] = score
                matrix.scores[(aa2, aa1)] = score
        return matrix

    @classmethod
    def blosum45(cls) -> ScoringMatrix:
        matrix = cls(name="BLOSUM45")
        data = {
            "A": {"A": 5, "R": -2, "N": -2, "D": -1, "C": -1, "Q": -1, "E": -1, "G": 0, "H": -2, "I": -1,
                  "L": -1, "K": -1, "M": -1, "F": -2, "P": -1, "S": 1, "T": 0, "W": -3, "Y": -2, "V": 0},
        }
        for aa1, row in data.items():
            for aa2, score in row.items():
                matrix.scores[(aa1, aa2)] = score
                matrix.scores[(aa2, aa1)] = score
        return matrix

    @classmethod
    def nucleotide(cls) -> ScoringMatrix:
        matrix = cls(name="nucleotide")
        for nt in "ACGTUacgtu":
            for nt2 in "ACGTUacgtu":
                if nt.upper() == nt2.upper():
                    matrix.scores[(nt, nt2)] = 2
                else:
                    matrix.scores[(nt, nt2)] = -1
        return matrix

    @classmethod
    def simple(cls, match: int = 1, mismatch: int = -1) -> ScoringMatrix:
        matrix = cls(name="simple")
        for c in "ACGTUacgtuWYSMKHBDRVN":
            for c2 in "ACGTUacgtuWYSMKHBDRVN":
                matrix.scores[(c, c2)] = match if c.upper() == c2.upper() else mismatch
        return matrix


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class AlignmentResult:
    """Result of a pairwise alignment."""
    score: float
    aligned_query: str
    aligned_target: str
    alignment_string: str
    query_start: int = 0
    query_end: int = 0
    target_start: int = 0
    target_end: int = 0
    identity: int = 0
    similarity: int = 0
    gaps: int = 0
    length: int = 0

    @property
    def identity_pct(self) -> float:
        return self.identity / max(self.length, 1) * 100

    @property
    def similarity_pct(self) -> float:
        return self.similarity / max(self.length, 1) * 100

    @property
    def gap_pct(self) -> float:
        return self.gaps / max(self.length, 1) * 100


@dataclass
class MSA:
    """Multiple Sequence Alignment result."""
    sequences: Dict[str, str] = field(default_factory=dict)
    names: List[str] = field(default_factory=list)
    alignment_length: int = 0
    score: float = 0.0

    @property
    def consensus(self) -> str:
        if not self.sequences:
            return ""
        length = self.alignment_length or max(len(s) for s in self.sequences.values())
        consensus = []
        for i in range(length):
            counts: Dict[str, int] = defaultdict(int)
            for seq in self.sequences.values():
                if i < len(seq) and seq[i] != "-":
                    counts[seq[i]] += 1
            if counts:
                best = max(counts, key=counts.get)
                total = sum(counts.values())
                if counts[best] / total >= 0.5:
                    consensus.append(best.lower())
                else:
                    consensus.append(best)
            else:
                consensus.append("-")
        return "".join(consensus)

    @property
    def conservation_scores(self) -> List[float]:
        if not self.sequences:
            return []
        length = self.alignment_length or max(len(s) for s in self.sequences.values())
        scores = []
        for i in range(length):
            residues = [
                seq[i] for seq in self.sequences.values()
                if i < len(seq) and seq[i] != "-"
            ]
            if not residues:
                scores.append(0.0)
                continue
            counts: Dict[str, int] = defaultdict(int)
            for r in residues:
                counts[r] += 1
            max_count = max(counts.values())
            scores.append(max_count / len(residues))
        return scores


@dataclass
class SearchHit:
    """Database search hit."""
    subject_id: str
    score: float
    e_value: float
    identity_pct: float
    query_start: int
    query_end: int
    subject_start: int
    subject_end: int
    aligned_query: str = ""
    aligned_subject: str = ""


@dataclass
class TracebackEntry:
    """DP traceback pointer."""
    row: int
    col: int
    score: float
    source: str = ""  # "diag", "up", "left", "none"


# ---------------------------------------------------------------------------
# Pairwise Aligner
# ---------------------------------------------------------------------------

class PairwiseAligner:
    """Needleman-Wunsch and Smith-Waterman pairwise alignment."""

    def __init__(
        self,
        scoring_matrix: Optional[ScoringMatrix] = None,
        gap_open: int = -10,
        gap_extend: int = -1,
    ):
        self.matrix = scoring_matrix or ScoringMatrix.blosum62()
        self.gap_open = gap_open
        self.gap_extend = gap_extend

    def global_align(
        self, query: str, target: str, mode: AlignMode = AlignMode.GLOBAL
    ) -> AlignmentResult:
        """Global alignment using Needleman-Wunsch with affine gaps."""
        q = " " + query.upper()
        t = " " + target.upper()
        n, m = len(q), len(t)

        # Three matrices: M (match), Ix (gap in query), Iy (gap in target)
        M = [[-float("inf")] * m for _ in range(n)]
        Ix = [[-float("inf")] * m for _ in range(n)]
        Iy = [[-float("inf")] * m for _ in range(n)]
        trace_M = [[None] * m for _ in range(n)]
        trace_Ix = [[None] * m for _ in range(n)]
        trace_Iy = [[None] * m for _ in range(n)]

        M[0][0] = 0
        for i in range(1, n):
            Ix[i][0] = self.gap_open + (i - 1) * self.gap_extend
        for j in range(1, m):
            Iy[0][j] = self.gap_open + (j - 1) * self.gap_extend

        for i in range(1, n):
            for j in range(1, m):
                # M[i][j]: best alignment ending with match/mismatch
                candidates = [
                    (M[i - 1][j - 1], "diag"),
                    (Ix[i - 1][j - 1], "diag"),
                    (Iy[i - 1][j - 1], "diag"),
                ]
                best_m, src_m = max(candidates, key=lambda x: x[0])
                M[i][j] = best_m + self.matrix.score(q[i], t[j])
                trace_M[i][j] = src_m

                # Ix[i][j]: gap in target (insertion in query)
                candidates_ix = [
                    (M[i - 1][j] + self.gap_open, "M"),
                    (Ix[i - 1][j] + self.gap_extend, "Ix"),
                ]
                best_ix, src_ix = max(candidates_ix, key=lambda x: x[0])
                Ix[i][j] = best_ix
                trace_Ix[i][j] = src_ix

                # Iy[i][j]: gap in query (insertion in target)
                candidates_iy = [
                    (M[i][j - 1] + self.gap_open, "M"),
                    (Iy[i][j - 1] + self.gap_extend, "Iy"),
                ]
                best_iy, src_iy = max(candidates_iy, key=lambda x: x[0])
                Iy[i][j] = best_iy
                trace_Iy[i][j] = src_iy

        # Traceback
        scores = [
            (M[n - 1][m - 1], "M"),
            (Ix[n - 1][m - 1], "Ix"),
            (Iy[n - 1][m - 1], "Iy"),
        ]
        best_score, best_matrix = max(scores, key=lambda x: x[0])
        aligned_q, aligned_t = self._traceback(
            q, t, M, Ix, Iy, trace_M, trace_Ix, trace_Iy,
            n - 1, m - 1, best_matrix,
        )
        return self._build_result(
            aligned_q, aligned_t, best_score, query, target
        )

    def local_align(
        self, query: str, target: str
    ) -> AlignmentResult:
        """Local alignment using Smith-Waterman."""
        q = " " + query.upper()
        t = " " + target.upper()
        n, m = len(q), len(t)
        dp = [[0] * m for _ in range(n)]
        trace = [[None] * m for _ in range(n)]
        max_score = 0
        max_pos = (0, 0)

        for i in range(1, n):
            for j in range(1, m):
                match = dp[i - 1][j - 1] + self.matrix.score(q[i], t[j])
                delete = dp[i - 1][j] + self.gap_extend
                insert = dp[i][j - 1] + self.gap_extend
                dp[i][j] = max(0, match, delete, insert)
                if dp[i][j] == match:
                    trace[i][j] = "diag"
                elif dp[i][j] == delete:
                    trace[i][j] = "up"
                elif dp[i][j] == insert:
                    trace[i][j] = "left"
                if dp[i][j] > max_score:
                    max_score = dp[i][j]
                    max_pos = (i, j)

        # Traceback from max position
        aligned_q, aligned_t = self._local_traceback(
            q, t, dp, trace, max_pos[0], max_pos[1]
        )
        result = self._build_result(
            aligned_q, aligned_t, max_score, query, target
        )
        # Adjust positions
        result.query_start = max_pos[0] - len(aligned_q.replace("-", ""))
        result.query_end = max_pos[0]
        result.target_start = max_pos[1] - len(aligned_t.replace("-", ""))
        result.target_end = max_pos[1]
        return result

    def _traceback(
        self, q, t, M, Ix, Iy, trace_M, trace_Ix, trace_Iy, i, j, current_matrix
    ) -> Tuple[str, str]:
        aq, at = [], []
        while i > 0 or j > 0:
            if current_matrix == "M":
                if trace_M[i][j] == "diag":
                    aq.append(q[i])
                    at.append(t[j])
                    i -= 1
                    j -= 1
                    current_matrix = "M"
                else:
                    current_matrix = trace_M[i][j]
            elif current_matrix == "Ix":
                aq.append(q[i])
                at.append("-")
                if trace_Ix[i][j] == "M":
                    current_matrix = "M"
                else:
                    i -= 1
                    current_matrix = "Ix"
                if i > 0:
                    i -= 0
            elif current_matrix == "Iy":
                aq.append("-")
                at.append(t[j])
                if trace_Iy[i][j] == "M":
                    current_matrix = "M"
                else:
                    j -= 1
                    current_matrix = "Iy"
            else:
                break
        return "".join(reversed(aq)), "".join(reversed(at))

    def _local_traceback(
        self, q, t, dp, trace, i, j
    ) -> Tuple[str, str]:
        aq, at = [], []
        while i > 0 and j > 0 and dp[i][j] > 0:
            if trace[i][j] == "diag":
                aq.append(q[i])
                at.append(t[j])
                i -= 1
                j -= 1
            elif trace[i][j] == "up":
                aq.append(q[i])
                at.append("-")
                i -= 1
            elif trace[i][j] == "left":
                aq.append("-")
                at.append(t[j])
                j -= 1
            else:
                break
        return "".join(reversed(aq)), "".join(reversed(at))

    def _build_result(
        self, aq: str, at: str, score: float, query: str, target: str
    ) -> AlignmentResult:
        match_str = []
        identity = similarity = gaps = 0
        for i in range(len(aq)):
            if aq[i] == "-":
                match_str.append(" ")
                gaps += 1
            elif at[i] == "-":
                match_str.append(" ")
                gaps += 1
            elif aq[i] == at[i]:
                match_str.append("|")
                identity += 1
                similarity += 1
            elif self.matrix.score(aq[i], at[i]) > 0:
                match_str.append(":")
                similarity += 1
            else:
                match_str.append(".")
        length = max(len(aq), 1)
        return AlignmentResult(
            score=score,
            aligned_query=aq,
            aligned_target=at,
            alignment_string="".join(match_str),
            identity=identity,
            similarity=similarity,
            gaps=gaps,
            length=length,
        )


# ---------------------------------------------------------------------------
# Multiple Sequence Aligner
# ---------------------------------------------------------------------------

class MultipleAligner:
    """Progressive multiple sequence alignment."""

    def __init__(
        self,
        method: str = "progressive",
        scoring_matrix: Optional[ScoringMatrix] = None,
        gap_open: int = -10,
        gap_extend: int = -1,
    ):
        self.method = method
        self.gap_open = gap_open
        self.gap_extend = gap_extend
        self.matrix = scoring_matrix or ScoringMatrix.blosum62()
        self._pairwise = PairwiseAligner(self.matrix, gap_open, gap_extend)

    def align(self, sequences: List[str], names: Optional[List[str]] = None) -> MSA:
        """Progressive MSA: pairwise distance → guide tree → progressive alignment."""
        if names is None:
            names = [f"seq_{i}" for i in range(len(sequences))]
        seq_dict = dict(zip(names, sequences))

        if len(sequences) <= 2:
            result = self._pairwise.global_align(sequences[0], sequences[-1])
            return MSA(
                sequences={names[0]: result.aligned_query, names[1]: result.aligned_target},
                names=names,
                alignment_length=max(len(result.aligned_query), len(result.aligned_target)),
            )

        # Step 1: Distance matrix
        dist = self._distance_matrix(seq_dict)
        # Step 2: UPGMA guide tree
        tree = self._upgma(dist, names)
        # Step 3: Progressive alignment following tree
        aligned = self._progressive_align(seq_dict, tree)
        return MSA(
            sequences=aligned,
            names=list(aligned.keys()),
            alignment_length=max(len(s) for s in aligned.values()) if aligned else 0,
        )

    def distance_matrix(self, seq_dict: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """Compute pairwise distance matrix from sequence dictionary."""
        names = list(seq_dict.keys())
        dist: Dict[str, Dict[str, float]] = {n: {} for n in names}
        for i, n1 in enumerate(names):
            for j, n2 in enumerate(names):
                if i == j:
                    dist[n1][n2] = 0.0
                elif j > i:
                    d = self._sequence_distance(seq_dict[n1], seq_dict[n2])
                    dist[n1][n2] = d
                    dist[n2][n1] = d
                else:
                    dist[n1][n2] = dist.get(n2, {}).get(n1, 0.0)
        return dist

    def _sequence_distance(self, s1: str, s2: str) -> float:
        result = self._pairwise.global_align(s1, s2)
        return 1.0 - result.identity_pct / 100.0

    def _distance_matrix(self, seq_dict: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        names = list(seq_dict.keys())
        dist: Dict[str, Dict[str, float]] = {n: {} for n in names}
        for i, n1 in enumerate(names):
            for j, n2 in enumerate(names):
                if i == j:
                    dist[n1][n2] = 0.0
                elif j > i:
                    d = self._sequence_distance(seq_dict[n1], seq_dict[n2])
                    dist[n1][n2] = d
                    dist[n2][n1] = d
                else:
                    dist[n1][n2] = dist.get(n2, {}).get(n1, 0.0)
        return dist

    def _upgma(
        self, dist: Dict[str, Dict[str, float]], names: List[str]
    ) -> Dict[str, Any]:
        """Simple UPGMA guide tree construction."""
        clusters = {n: {"name": n, "children": [], "size": 1} for n in names}
        remaining = list(names)
        d = dict(dist)

        while len(remaining) > 1:
            min_d = float("inf")
            pair = (remaining[0], remaining[1])
            for i, c1 in enumerate(remaining):
                for c2 in remaining[i + 1:]:
                    val = d.get(c1, {}).get(c2, d.get(c2, {}).get(c1, float("inf")))
                    if val < min_d:
                        min_d = val
                        pair = (c1, c2)
            c1, c2 = pair
            new_name = f"({c1},{c2})"
            new_cluster = {
                "name": new_name,
                "children": [clusters[c1], clusters[c2]],
                "size": clusters[c1]["size"] + clusters[c2]["size"],
            }
            clusters[new_name] = new_cluster
            d[new_name] = {}
            for c in remaining:
                if c not in (c1, c2):
                    d_val = (
                        d[c1].get(c, 0) * clusters[c1]["size"]
                        + d[c2].get(c, 0) * clusters[c2]["size"]
                    ) / (clusters[c1]["size"] + clusters[c2]["size"])
                    d[new_name][c] = d_val
                    d[c][new_name] = d_val
            remaining.remove(c1)
            remaining.remove(c2)
            remaining.append(new_name)

        return clusters.get(remaining[0], {"name": remaining[0], "children": []})

    def _progressive_align(
        self, seq_dict: Dict[str, str], tree: Dict[str, Any]
    ) -> Dict[str, str]:
        """Recursively align sequences following the guide tree."""
        if "children" not in tree or not tree["children"]:
            name = tree["name"]
            return {name: seq_dict.get(name, "")}
        left = self._progressive_align(seq_dict, tree["children"][0])
        right = self._progressive_align(seq_dict, tree["children"][1])
        merged: Dict[str, str] = {}
        left_seqs = list(left.values())
        right_seqs = list(right.values())
        if left_seqs and right_seqs:
            result = self._pairwise.global_align(left_seqs[0], right_seqs[0])
            merged.update({k: result.aligned_query for k in left})
            merged.update({k: result.aligned_target for k in right})
        else:
            merged.update(left)
            merged.update(right)
        return merged


# ---------------------------------------------------------------------------
# Database Searcher
# ---------------------------------------------------------------------------

class DatabaseSearcher:
    """BLAST-like seed-and-extend database search."""

    def __init__(
        self,
        scoring_matrix: Optional[ScoringMatrix] = None,
        word_size: int = 3,
        e_value_threshold: float = 0.01,
        gap_open: int = -10,
        gap_extend: int = -1,
    ):
        self.matrix = scoring_matrix or ScoringMatrix.blosum62()
        self.word_size = word_size
        self.e_value_threshold = e_value_threshold
        self.gap_open = gap_open
        self.gap_extend = gap_extend
        self._aligner = PairwiseAligner(self.matrix, gap_open, gap_extend)

    def search(
        self, query: str, database: List[str], ids: Optional[List[str]] = None
    ) -> List[SearchHit]:
        """Search query against a list of database sequences."""
        if ids is None:
            ids = [f"seq_{i}" for i in range(len(database))]
        hits: List[SearchHit] = []
        query_upper = query.upper()
        query_words = self._extract_words(query_upper)
        db_size = len(database)
        for idx, seq in enumerate(database):
            seq_upper = seq.upper()
            seq_words = self._extract_words(seq_upper)
            seeds = query_words & seq_words
            if not seeds:
                continue
            result = self._aligner.global_align(query_upper, seq_upper)
            if result.score <= 0:
                continue
            e_value = self._calc_e_value(result.score, len(query_upper), len(seq_upper), db_size)
            if e_value > self.e_value_threshold:
                continue
            hits.append(SearchHit(
                subject_id=ids[idx],
                score=result.score,
                e_value=e_value,
                identity_pct=result.identity_pct,
                query_start=0,
                query_end=len(query_upper),
                subject_start=0,
                subject_end=len(seq_upper),
                aligned_query=result.aligned_query,
                aligned_subject=result.aligned_target,
            ))
        hits.sort(key=lambda h: h.e_value)
        return hits

    def _extract_words(self, seq: str) -> Set[str]:
        words: Set[str] = set()
        for i in range(len(seq) - self.word_size + 1):
            words.add(seq[i:i + self.word_size])
        return words

    def _calc_e_value(
        self, score: float, query_len: int, db_seq_len: int, db_size: int
    ) -> float:
        """Simplified E-value calculation."""
        k = 0.041
        lam = 0.267
        eff_db = db_size
        m = query_len
        n = db_seq_len
        return k * m * n * math.exp(-lam * score) / eff_db


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Sequence Alignment Demo")
    print("=" * 60)

    aligner = PairwiseAligner(ScoringMatrix.blosum62())

    print("\n[1] Global Alignment (Needleman-Wunsch)")
    result = aligner.global_align("HEAGAWGHEE", "PAWHEAE")
    print(f"  Score: {result.score}")
    print(f"  Identity: {result.identity_pct:.1f}%")
    print(f"  Query:    {result.aligned_query}")
    print(f"            {result.alignment_string}")
    print(f"  Target:   {result.aligned_target}")

    print("\n[2] Local Alignment (Smith-Waterman)")
    local = aligner.local_align(
        "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
        "MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFLGFPTTKTYFPHFDLSH",
    )
    print(f"  Score: {local.score}")
    print(f"  Identity: {local.identity_pct:.1f}%")

    print("\n[3] Multiple Sequence Alignment")
    msa_aligner = MultipleAligner(scoring_matrix=ScoringMatrix.blosum62())
    msa = msa_aligner.align([
        "HEAGAWGHEE", "PAWHEAE", "HEAGAWGHEE", "PAWEAE"
    ])
    for name, seq in msa.sequences.items():
        print(f"  {name}: {seq}")
    print(f"  Consensus: {msa.consensus}")

    print("\n[4] Database Search")
    searcher = DatabaseSearcher(word_size=3)
    hits = searcher.search(
        "HEAGAWGHEE",
        ["PAWHEAE", "HEAGAWGHEE", "PAWEAE"],
        ids=["hit1", "hit2", "hit3"],
    )
    for hit in hits:
        print(f"  {hit.subject_id}: score={hit.score}, e={hit.e_value:.2e}")

    print("\n[5] Distance Matrix")
    seqs = {
        "Human": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
        "Gorilla": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH",
        "Mouse": "MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFLGFPTTKTYFPHFDLSH",
    }
    dm = msa_aligner.distance_matrix(seqs)
    for sp1 in seqs:
        for sp2 in seqs:
            if sp1 < sp2:
                print(f"  {sp1} vs {sp2}: {dm[sp1][sp2]:.4f}")

    print("\n" + "=" * 60)
    print("  Alignment demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
