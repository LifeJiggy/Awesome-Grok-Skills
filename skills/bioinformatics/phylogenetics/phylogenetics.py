"""
Phylogenetics Module
Tree construction, distance models, bootstrap analysis, selection analysis, and ancestral reconstruction.
"""

from __future__ import annotations

import hashlib
import math
import random
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

class DistanceModel(Enum):
    P_DISTANCE = "p_distance"
    JUKES_CANTOR = "jukes_cantor"
    KIMURA_2P = "kimura_2p"
    POISSON = "poisson"


class TreeMethod(Enum):
    NJ = "neighbor_joining"
    UPGMA = "upgma"
    MP = "maximum_parsimony"
    ML = "maximum_likelihood"


class SelectionType(Enum):
    POSITIVE = "positive_selection"
    NEUTRAL = "neutral"
    PURIFYING = "purifying_selection"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TreeNode:
    """Node in a phylogenetic tree."""
    label: str = ""
    branch_length: float = 0.0
    children: List[TreeNode] = field(default_factory=list)
    is_leaf: bool = True
    bootstrap_value: float = 0.0
    depth: int = 0

    def add_child(self, child: TreeNode) -> None:
        child.depth = self.depth + 1
        self.children.append(child)
        self.is_leaf = False

    @property
    def leaf_count(self) -> int:
        if self.is_leaf:
            return 1
        return sum(c.leaf_count for c in self.children)


@dataclass
class PhylogeneticTree:
    """Complete phylogenetic tree."""
    root: TreeNode = field(default_factory=TreeNode)
    name: str = ""
    method: TreeMethod = TreeMethod.NJ
    distance_model: DistanceModel = DistanceModel.JUKES_CANTOR
    bootstrap_replicates: int = 0

    @property
    def leaf_count(self) -> int:
        return self.root.leaf_count

    @property
    def internal_node_count(self) -> int:
        return self._count_internal(self.root)

    @property
    def leaves(self) -> List[str]:
        result: List[str] = []
        self._collect_leaves(self.root, result)
        return result

    @property
    def internal_nodes(self) -> List[TreeNode]:
        result: List[TreeNode] = []
        self._collect_internal(self.root, result)
        return result

    @property
    def total_branch_length(self) -> float:
        return self._sum_branches(self.root)

    def to_newick(self) -> str:
        """Convert tree to Newick format."""
        return self._node_newick(self.root) + ";"

    def robinson_foulds(self, other: PhylogeneticTree) -> int:
        """Calculate Robinson-Foulds symmetric distance."""
        sp1 = self._split_set(self.root)
        sp2 = other._split_set(other.root)
        return len(sp1.symmetric_difference(sp2))

    def get_distance(self, taxon1: str, taxon2: str) -> Optional[float]:
        """Get pairwise distance between two taxa."""
        path1 = self._path_to_leaf(self.root, taxon1, [])
        path2 = self._path_to_leaf(self.root, taxon2, [])
        if path1 is None or path2 is None:
            return None
        lca = self._find_lca(path1, path2)
        if lca is None:
            return None
        d1 = self._path_length(lca, taxon1)
        d2 = self._path_length(lca, taxon2)
        return d1 + d2

    def prune(self, taxon: str) -> PhylogeneticTree:
        """Remove a taxon and collapse the resulting degree-2 node."""
        new_root = self._prune_recursive(self.root, taxon)
        return PhylogeneticTree(root=new_root, method=self.method)

    def _node_newick(self, node: TreeNode) -> str:
        if node.is_leaf:
            return f"{node.label}:{node.branch_length:.4f}"
        children = ",".join(self._node_newick(c) for c in node.children)
        bl = f":{node.branch_length:.4f}" if node.branch_length > 0 else ""
        return f"({children}){bl}"

    def _count_internal(self, node: TreeNode) -> int:
        if node.is_leaf:
            return 0
        return 1 + sum(self._count_internal(c) for c in node.children)

    def _collect_leaves(self, node: TreeNode, result: List[str]) -> None:
        if node.is_leaf:
            result.append(node.label)
        else:
            for c in node.children:
                self._collect_leaves(c, result)

    def _collect_internal(self, node: TreeNode, result: List[TreeNode]) -> None:
        if not node.is_leaf:
            result.append(node)
            for c in node.children:
                self._collect_internal(c, result)

    def _sum_branches(self, node: TreeNode) -> float:
        total = node.branch_length
        for c in node.children:
            total += self._sum_branches(c)
        return total

    def _split_set(self, node: TreeNode) -> Set[frozenset]:
        splits: Set[frozenset] = set()
        if node.is_leaf:
            return splits
        for c in node.children:
            leaves = set()
            self._collect_leaves_set(c, leaves)
            if leaves and leaves != set(self.leaves):
                splits.add(frozenset(leaves))
        for c in node.children:
            splits.update(self._split_set(c))
        return splits

    def _collect_leaves_set(self, node: TreeNode, result: Set[str]) -> None:
        if node.is_leaf:
            result.add(node.label)
        else:
            for c in node.children:
                self._collect_leaves_set(c, result)

    def _path_to_leaf(
        self, node: TreeNode, target: str, path: List[TreeNode]
    ) -> Optional[List[TreeNode]]:
        if node.is_leaf:
            return path if node.label == target else None
        for c in node.children:
            result = self._path_to_leaf(c, target, path + [node])
            if result is not None:
                return result
        return None

    def _find_lca(
        self, path1: List[TreeNode], path2: List[TreeNode]
    ) -> Optional[TreeNode]:
        set2 = set(id(n) for n in path2)
        lca = None
        for node in path1:
            if id(node) in set2:
                lca = node
        return lca

    def _path_length(self, start: TreeNode, target: str) -> float:
        if start.is_leaf:
            return 0.0 if start.label == target else float("inf")
        for c in start.children:
            if c.is_leaf and c.label == target:
                return c.branch_length
            sub = self._path_length(c, target)
            if sub < float("inf"):
                return c.branch_length + sub
        return float("inf")

    def _prune_recursive(self, node: TreeNode, taxon: str) -> TreeNode:
        if node.is_leaf:
            return TreeNode(
                label=node.label,
                branch_length=node.branch_length,
            )
        new_children = []
        for c in node.children:
            if c.is_leaf and c.label == taxon:
                continue
            if not c.is_leaf:
                new_children.append(self._prune_recursive(c, taxon))
            else:
                new_children.append(
                    TreeNode(label=c.label, branch_length=c.branch_length)
                )
        if len(new_children) == 1:
            child = new_children[0]
            child.branch_length += node.branch_length
            return child
        new_node = TreeNode(
            label=node.label,
            branch_length=node.branch_length,
            is_leaf=False,
        )
        new_node.children = new_children
        return new_node


# ---------------------------------------------------------------------------
# Distance Calculator
# ---------------------------------------------------------------------------

class DistanceCalculator:
    """Calculate evolutionary distances between sequences."""

    def __init__(self, model: DistanceModel = DistanceModel.JUKES_CANTOR):
        self.model = model

    def distance(self, seq1: str, seq2: str) -> float:
        s1, s2 = seq1.upper(), seq2.upper()
        length = min(len(s1), len(s2))
        if length == 0:
            return 0.0
        matches = sum(1 for i in range(length) if s1[i] == s2[i])
        p = 1.0 - matches / length
        if self.model == DistanceModel.P_DISTANCE:
            return p
        elif self.model == DistanceModel.JUKES_CANTOR:
            if p >= 0.75:
                return 3.0
            return -0.75 * math.log(1 - 4.0 / 3.0 * p)
        elif self.model == DistanceModel.KIMURA_2P:
            transitions = self._count_transitions(s1[:length], s2[:length])
            transversions = length - matches - transitions
            p = transitions / max(length, 1)
            q = transversions / max(length, 1)
            if 1 - 2 * p - q <= 0 or 1 - 2 * q <= 0:
                return 3.0
            return -0.5 * math.log(1 - 2 * p - q) - 0.25 * math.log(1 - 2 * q)
        elif self.model == DistanceModel.POISSON:
            if p >= 1.0:
                return 10.0
            return -math.log(1 - p)
        return p

    def matrix(
        self, seq_dict: Dict[str, str]
    ) -> Tuple[List[str], List[List[float]]]:
        """Compute full pairwise distance matrix."""
        names = list(seq_dict.keys())
        n = len(names)
        mat = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d = self.distance(seq_dict[names[i]], seq_dict[names[j]])
                mat[i][j] = d
                mat[j][i] = d
        return names, mat

    def _count_transitions(self, s1: str, s2: str) -> int:
        transitions = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}
        count = 0
        for a, b in zip(s1, s2):
            if (a, b) in transitions:
                count += 1
        return count


# ---------------------------------------------------------------------------
# Tree Builder
# ---------------------------------------------------------------------------

class TreeBuilder:
    """Construct phylogenetic trees from sequence data."""

    def __init__(
        self,
        model: DistanceModel = DistanceModel.JUKES_CANTOR,
        seed: Optional[int] = None,
    ):
        self.model = model
        self.calculator = DistanceCalculator(model)
        self.seed = seed
        self._rng = random.Random(seed)

    def neighbor_joining(self, sequences: Dict[str, str]) -> PhylogeneticTree:
        """Build Neighbor-Joining tree."""
        names, dist_mat = self.calculator.matrix(sequences)
        n = len(names)
        nodes = {
            name: TreeNode(label=name, is_leaf=True) for name in names
        }
        active = list(range(n))
        dist = [row[:] for row in dist_mat]
        while len(active) > 2:
            m = len(active)
            r = sum(dist[i][j] for i in active for j in active if i != j) / max(m * (m - 1), 1)
            min_val = float("inf")
            pair = (active[0], active[1])
            for idx_i in range(len(active)):
                for idx_j in range(idx_i + 1, len(active)):
                    i, j = active[idx_i], active[idx_j]
                    val = dist[i][j] - (r[i] if isinstance(r, list) else r) - (r[j] if isinstance(r, list) else r)
                    if val < min_val:
                        min_val = val
                        pair = (i, j)
            i, j = pair
            new_label = f"({names[i]},{names[j]})"
            new_node = TreeNode(label=new_label, is_leaf=False)
            new_node.add_child(nodes[names[i]])
            new_node.add_child(nodes[names[j]])
            bl_i = max(dist[i][j] / 2 + r / 2 if isinstance(r, float) else dist[i][j] / 2, 0.001)
            bl_j = max(dist[i][j] - bl_i, 0.001)
            nodes[names[i]].branch_length = bl_i
            nodes[names[j]].branch_length = bl_j
            nodes[new_label] = new_node
            # Update distance matrix
            new_idx = len(dist)
            dist.append([0.0] * (new_idx + 1))
            for row in dist:
                row.append(0.0)
            for k in active:
                if k != i and k != j:
                    d_k_new = max((dist[i][k] + dist[j][k] - dist[i][j]) / 2, 0.001)
                    dist[new_idx][k] = d_k_new
                    dist[k][new_idx] = d_k_new
            active.remove(i)
            active.remove(j)
            active.append(new_idx)
            names.append(new_label)

        root = TreeNode(label="root", is_leaf=False)
        if len(active) == 2:
            root.add_child(nodes[names[active[0]]])
            root.add_child(nodes[names[active[1]]])
            bl = max(dist[active[0]][active[1]] / 2, 0.001)
            nodes[names[active[0]]].branch_length = bl
            nodes[names[active[1]]].branch_length = bl
        return PhylogeneticTree(root=root, method=TreeMethod.NJ, distance_model=self.model)

    def upgma(self, sequences: Dict[str, str]) -> PhylogeneticTree:
        """Build UPGMA tree."""
        names, dist_mat = self.calculator.matrix(sequences)
        n = len(names)
        nodes = {
            name: TreeNode(label=name, is_leaf=True) for name in names
        }
        sizes = {name: 1 for name in names}
        active = list(range(n))
        dist = [row[:] for row in dist_mat]
        heights: Dict[str, float] = {name: 0.0 for name in names}

        while len(active) > 1:
            min_val = float("inf")
            pair = (active[0], active[1])
            for idx_i in range(len(active)):
                for idx_j in range(idx_i + 1, len(active)):
                    i, j = active[idx_i], active[idx_j]
                    if dist[i][j] < min_val:
                        min_val = dist[i][j]
                        pair = (i, j)
            i, j = pair
            new_height = min_val / 2
            new_label = f"({names[i]},{names[j]})"
            new_node = TreeNode(label=new_label, is_leaf=False)
            new_node.add_child(nodes[names[i]])
            new_node.add_child(nodes[names[j]])
            bl_i = max(new_height - heights.get(names[i], 0), 0.001)
            bl_j = max(new_height - heights.get(names[j], 0), 0.001)
            nodes[names[i]].branch_length = bl_i
            nodes[names[j]].branch_length = bl_j
            nodes[new_label] = new_node
            heights[new_label] = new_height
            new_idx = len(dist)
            dist.append([0.0] * (new_idx + 1))
            for row in dist:
                row.append(0.0)
            si = sizes[names[i]]
            sj = sizes[names[j]]
            for k in active:
                if k != i and k != j:
                    d_new = (dist[i][k] * si + dist[j][k] * sj) / (si + sj)
                    dist[new_idx][k] = d_new
                    dist[k][new_idx] = d_new
            sizes[new_label] = si + sj
            active.remove(i)
            active.remove(j)
            active.append(new_idx)
            names.append(new_label)

        root = nodes[names[active[0]]] if active else TreeNode(label="root")
        return PhylogeneticTree(root=root, method=TreeMethod.UPGMA, distance_model=self.model)

    def bootstrap(
        self,
        sequences: Dict[str, str],
        method: str = "nj",
        replicates: int = 100,
        seed: int = 42,
    ) -> PhylogeneticTree:
        """Bootstrap analysis for branch support."""
        rng = random.Random(seed)
        seq_list = list(sequences.values())
        names_list = list(sequences.keys())
        seq_len = len(seq_list[0])
        support: Dict[str, List[int]] = defaultdict(list)
        actual_tree = (
            self.neighbor_joining(sequences) if method == "nj"
            else self.upgma(sequences)
        )
        for rep in range(replicates):
            sites = [rng.randint(0, seq_len - 1) for _ in range(seq_len)]
            resampled = {
                name: "".join(seq[s] for s in sites)
                for name, seq in sequences.items()
            }
            rep_tree = (
                self.neighbor_joining(resampled) if method == "nj"
                else self.upgma(resampled)
            )
            for leaf_set in self._all_bipartitions(rep_tree.root):
                key = frozenset(leaf_set)
                support[str(sorted(key))].append(1)
        for node in actual_tree.internal_nodes:
            leaves = set()
            self._collect_leaves(node, leaves)
            key = str(sorted(leaves))
            count = sum(support.get(key, [0]))
            node.bootstrap_value = count / max(replicates, 1) * 100
        actual_tree.bootstrap_replicates = replicates
        return actual_tree

    def _all_bipartitions(self, node: TreeNode) -> List[Set[str]]:
        if node.is_leaf:
            return []
        result = []
        for c in node.children:
            leaves = set()
            self._collect_leaves(c, leaves)
            result.append(leaves)
        for c in node.children:
            result.extend(self._all_bipartitions(c))
        return result

    def _collect_leaves(self, node: TreeNode, result: Set[str]) -> None:
        if node.is_leaf:
            result.add(node.label)
        else:
            for c in node.children:
                self._collect_leaves(c, result)


# ---------------------------------------------------------------------------
# Selection Analyzer
# ---------------------------------------------------------------------------

@dataclass
class KaKsResult:
    """dN/dS analysis result."""
    ka: float
    ks: float
    kaks_ratio: float
    interpretation: SelectionType
    p_value: float = 1.0
    sites_tested: int = 0
    positive_sites: int = 0


class SelectionAnalyzer:
    """Calculate dN/dS (Ka/Ks) ratios for coding sequences."""

    CODON_TABLE: Dict[str, str] = {
        "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
        "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
        "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
        "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
        "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
        "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
        "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
        "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
    }

    SYNONYMOUS = {
        "F": [("TTT", "TTC")], "L": [("CTT", "CTC", "CTA", "CTG", "TTA", "TTG")],
        "I": [("ATT", "ATC", "ATA")], "V": [("GTT", "GTC", "GTA", "GTG")],
        "S": [("TCT", "TCC", "TCA", "TCG", "AGT", "AGC")],
        "P": [("CCT", "CCC", "CCA", "CCG")], "T": [("ACT", "ACC", "ACA", "ACG")],
        "A": [("GCT", "GCC", "GCA", "GCG")], "Y": [("TAT", "TAC")],
        "H": [("CAT", "CAC")], "Q": [("CAA", "CAG")],
        "N": [("AAT", "AAC")], "D": [("GAT", "GAC")],
        "E": [("GAA", "GAG")], "C": [("TGT", "TGC")],
        "W": [("TGG",)], "R": [("CGT", "CGC", "CGA", "CGG", "AGA", "AGG")],
        "G": [("GGT", "GGC", "GGA", "GGG")], "M": [("ATG",)],
        "K": [("AAA", "AAG")], "*": [("TAA", "TAG", "TGA")],
    }

    def calculate_kaks(
        self, query: str, reference: str
    ) -> KaKsResult:
        q = query.upper().replace("U", "T")
        r = reference.upper().replace("U", "T")
        n_sites = min(len(q), len(r)) // 3
        synonymous_diffs = 0
        nonsynonymous_diffs = 0
        total_synonymous = 0
        total_nonsynonymous = 0
        positive_sites = 0

        for i in range(n_sites):
            codon_q = q[i * 3:i * 3 + 3]
            codon_r = r[i * 3:i * 3 + 3]
            if len(codon_q) < 3 or len(codon_r) < 3:
                continue
            aa_q = self.CODON_TABLE.get(codon_q, "X")
            aa_r = self.CODON_TABLE.get(codon_r, "X")
            total_nonsynonymous += 2.0
            total_synonymous += 1.0
            if codon_q != codon_r:
                if aa_q == aa_r:
                    synonymous_diffs += 1
                else:
                    nonsynonymous_diffs += 1
                    positive_sites += 1

        ka = nonsynonymous_diffs / max(total_nonsynonymous, 1)
        ks = synonymous_diffs / max(total_synonymous, 1)
        kaks = ka / max(ks, 0.0001)
        if kaks > 1.0:
            interpretation = SelectionType.POSITIVE
        elif kaks < 0.5:
            interpretation = SelectionType.PURIFYING
        else:
            interpretation = SelectionType.NEUTRAL

        return KaKsResult(
            ka=round(ka, 4),
            ks=round(ks, 4),
            kaks_ratio=round(kaks, 4),
            interpretation=interpretation,
            sites_tested=n_sites,
            positive_sites=positive_sites,
        )


# ---------------------------------------------------------------------------
# Ancestral Reconstructor
# ---------------------------------------------------------------------------

@dataclass
class AncestralState:
    """Result of ancestral state reconstruction."""
    root_sequence: str = ""
    node_sequences: Dict[str, str] = field(default_factory=dict)
    confidence: Dict[str, Dict[str, float]] = field(default_factory=dict)


class AncestralReconstructor:
    """Reconstruct ancestral sequences using parsimony."""

    def reconstruct(
        self,
        sequences: Dict[str, str],
        tree: PhylogeneticTree,
    ) -> AncestralState:
        seq_len = max(len(s) for s in sequences.values())
        padded = {
            k: v.ljust(seq_len, "-") for k, v in sequences.items()
        }
        result = AncestralState()
        node_seqs: Dict[str, List[str]] = {}
        self._fitch_down(tree.root, padded, node_seqs)
        self._fitch_up(tree.root, node_seqs, {})
        for node_label, seq_chars in node_seqs.items():
            result.node_sequences[node_label] = "".join(seq_chars)
        if tree.root.label in result.node_sequences:
            result.root_sequence = result.node_sequences[tree.root.label]
        return result

    def _fitch_down(
        self,
        node: TreeNode,
        leaf_seqs: Dict[str, str],
        node_seqs: Dict[str, List[str]],
    ) -> List[Set[str]]:
        if node.is_leaf:
            seq = leaf_seqs.get(node.label, "")
            sets = [set([c]) for c in seq]
            node_seqs[node.label] = list(seq)
            return sets
        child_sets = []
        for c in node.children:
            child_sets.append(self._fitch_down(c, leaf_seqs, node_seqs))
        if not child_sets:
            return []
        seq_len = len(child_sets[0])
        node_sets: List[Set[str]] = []
        node_chars: List[str] = []
        for i in range(seq_len):
            union = set()
            intersection = None
            for cs in child_sets:
                if i < len(cs):
                    union |= cs[i]
                    if intersection is None:
                        intersection = set(cs[i])
                    else:
                        intersection &= cs[i]
            if intersection:
                node_sets.append(intersection)
                node_chars.append(min(intersection))
            else:
                node_sets.append(union)
                node_chars.append(min(union) if union else "?")
        node_seqs[node.label] = node_chars
        return node_sets

    def _fitch_up(
        self,
        node: TreeNode,
        node_seqs: Dict[str, List[str]],
        parent_seqs: Dict[str, str],
    ) -> None:
        if node.is_leaf:
            return
        parent_char = parent_seqs.get(node.label, "")
        if node.label in node_seqs and parent_char:
            for i in range(len(node_seqs[node.label])):
                if i < len(parent_char) and parent_char[i] != "?":
                    node_seqs[node.label][i] = parent_char[i]
        for c in node.children:
            self._fitch_up(c, node_seqs, {node.label: "".join(node_seqs.get(node.label, []))})


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Phylogenetics Demo")
    print("=" * 60)

    sequences = {
        "Human":     "ATGAAACTGGTGGCGCTG",
        "Chimp":     "ATGAAACTGGTGGCGCTG",
        "Gorilla":   "ATGAAACTGGTGGCGCTG",
        "Orangutan": "ATGAAACTGGTGGCGCTG",
        "Mouse":     "ATGAAACTGGTGGTGCTG",
    }

    print("\n[1] Distance Matrix (Kimura 2-parameter)")
    calc = DistanceCalculator(DistanceModel.KIMURA_2P)
    names, mat = calc.matrix(sequences)
    for i, n1 in enumerate(names):
        for j, n2 in enumerate(names):
            if i < j:
                print(f"  {n1} vs {n2}: {mat[i][j]:.4f}")

    print("\n[2] Neighbor-Joining Tree")
    builder = TreeBuilder(model=DistanceModel.JUKES_CANTOR, seed=42)
    nj = builder.neighbor_joining(sequences)
    print(f"  Newick: {nj.to_newick()}")
    print(f"  Leaves: {nj.leaf_count}  Internal: {nj.internal_node_count}")
    print(f"  Total branch length: {nj.total_branch_length:.4f}")

    print("\n[3] UPGMA Tree")
    upgma = builder.upgma(sequences)
    print(f"  Newick: {upgma.to_newick()}")

    print("\n[4] Robinson-Foulds Distance")
    rf = nj.robinson_foulds(upgma)
    print(f"  NJ vs UPGMA: {rf}")

    print("\n[5] Bootstrap Analysis (100 replicates)")
    boot_tree = builder.bootstrap(sequences, method="nj", replicates=100)
    for node in boot_tree.internal_nodes:
        print(f"  {node.label}: support={node.bootstrap_value:.0f}%")

    print("\n[6] Selection Analysis")
    analyzer = SelectionAnalyzer()
    result = analyzer.calculate_kaks(
        "ATGAAACTGGTGGCGCTG",
        "ATGAAACTGGTGGTGCTG",
    )
    print(f"  Ka: {result.ka:.4f}  Ks: {result.ks:.4f}")
    print(f"  Ka/Ks: {result.kaks_ratio:.4f} ({result.interpretation.value})")

    print("\n[7] Ancestral Reconstruction")
    reconstructor = AncestralReconstructor()
    ancestral = reconstructor.reconstruct(sequences, nj)
    print(f"  Root: {ancestral.root_sequence}")
    for label in list(ancestral.node_sequences.keys())[:3]:
        print(f"  {label}: {ancestral.node_sequences[label][:30]}...")

    print("\n" + "=" * 60)
    print("  Phylogenetics demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
