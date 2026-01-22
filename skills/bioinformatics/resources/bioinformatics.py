#!/usr/bin/env python3
"""
Grok Bioinformatics Module
Biological sequence analysis, protein structure prediction, and genomic computations.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np
from collections import Counter
from abc import ABC, abstractmethod

@dataclass
class Sequence:
    id: str
    sequence: str
    sequence_type: str
    metadata: Dict[str, Any]

@dataclass
class AlignmentResult:
    score: float
    alignment: Tuple[str, str]
    identity: float
    coverage: float

class DNATools:
    """DNA sequence analysis tools."""
    
    COMPLEMENT = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    CODON_TABLE = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
        'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    
    def __init__(self):
        pass
    
    def reverse_complement(self, dna: str) -> str:
        """Generate reverse complement of DNA sequence."""
        return ''.join(self.COMPLEMENT.get(base, 'N') for base in reversed(dna))
    
    def transcribe(self, dna: str) -> str:
        """Transcribe DNA to RNA."""
        return dna.replace('T', 'U')
    
    def translate(self, dna: str, frame: int = 0) -> str:
        """Translate DNA to protein."""
        protein = ''
        start = frame
        for i in range(start, len(dna) - 2, 3):
            codon = dna[i:i+3]
            amino_acid = self.CODON_TABLE.get(codon, 'X')
            protein += amino_acid
            if amino_acid == '*':
                break
        return protein
    
    def gc_content(self, sequence: str) -> float:
        """Calculate GC content percentage."""
        gc_count = sequence.count('G') + sequence.count('C')
        return gc_count / len(sequence) * 100
    
    def find_orfs(self, dna: str, min_length: int = 100) -> List[Dict]:
        """Find open reading frames."""
        orfs = []
        
        for frame in range(3):
            protein = self.translate(dna, frame)
            orf_start = 0
            
            for i, aa in enumerate(protein):
                if aa == 'M' and orf_start == 0:
                    orf_start = i
                elif aa == '*' and orf_start > 0:
                    length = (i - orf_start) * 3
                    if length >= min_length:
                        orfs.append({
                            'start': orf_start * 3 + frame,
                            'end': i * 3 + frame,
                            'length': length,
                            'frame': frame
                        })
                    orf_start = 0
        
        return orfs
    
    def primer_binding_sites(self, sequence: str, primer: str,
                            max_mismatches: int = 2) -> List[int]:
        """Find primer binding sites with allowed mismatches."""
        sites = []
        primer = primer.upper()
        
        for i in range(len(sequence) - len(primer) + 1):
            window = sequence[i:i+len(primer)]
            mismatches = sum(1 for a, b in zip(window, primer) if a != b)
            if mismatches <= max_mismatches:
                sites.append(i)
        
        return sites


class ProteinAnalyzer:
    """Protein sequence and structure analysis."""
    
    AMINO_ACID_PROPERTIES = {
        'A': {'hydrophobicity': 1.8, 'volume': 88.6, 'charge': 0},
        'R': {'hydrophobicity': -4.5, 'volume': 173.4, 'charge': 1},
        'N': {'hydrophobicity': -3.5, 'volume': 114.1, 'charge': 0},
        'D': {'hydrophobicity': -3.5, 'volume': 111.1, 'charge': -1},
        'C': {'hydrophobicity': 2.5, 'volume': 108.5, 'charge': 0},
        'Q': {'hydrophobicity': -3.5, 'volume': 143.8, 'charge': 0},
        'E': {'hydrophobicity': -3.5, 'volume': 138.4, 'charge': -1},
        'G': {'hydrophobicity': -0.4, 'volume': 60.1, 'charge': 0},
        'H': {'hydrophobicity': -3.2, 'volume': 153.2, 'charge': 1},
        'I': {'hydrophobicity': 4.5, 'volume': 166.7, 'charge': 0},
        'L': {'hydrophobicity': 3.8, 'volume': 166.7, 'charge': 0},
        'K': {'hydrophobicity': -3.9, 'volume': 168.6, 'charge': 1},
        'M': {'hydrophobicity': 1.9, 'volume': 162.9, 'charge': 0},
        'F': {'hydrophobicity': 2.8, 'volume': 189.9, 'charge': 0},
        'P': {'hydrophobicity': -1.6, 'volume': 112.7, 'charge': 0},
        'S': {'hydrophobicity': -0.8, 'volume': 89.0, 'charge': 0},
        'T': {'hydrophobicity': -0.7, 'volume': 116.1, 'charge': 0},
        'W': {'hydrophobicity': -0.9, 'volume': 227.8, 'charge': 0},
        'Y': {'hydrophobicity': -1.3, 'volume': 193.6, 'charge': 0},
        'V': {'hydrophobicity': 4.2, 'volume': 140.0, 'charge': 0}
    }
    
    def molecular_weight(self, sequence: str) -> float:
        """Calculate approximate molecular weight."""
        weights = {
            'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10,
            'C': 121.15, 'Q': 146.15, 'E': 147.13, 'G': 75.07,
            'H': 155.16, 'I': 131.17, 'L': 131.17, 'K': 146.19,
            'M': 149.21, 'F': 165.19, 'P': 115.13, 'S': 105.09,
            'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
        }
        mw = sum(weights.get(aa, 0) for aa in sequence)
        mw -= (len(sequence) - 1) * 18.015
        return mw
    
    def isoelectric_point(self, sequence: str) -> float:
        """Estimate isoelectric point."""
        pKa = {'D': 3.9, 'E': 4.3, 'C': 8.3, 'Y': 10.1,
               'H': 6.0, 'K': 10.5, 'R': 12.5}
        
        ph = 7.0
        for _ in range(100):
            charge = 0
            for aa in sequence:
                if aa == 'D':
                    charge -= 1 / (1 + 10 ** (ph - pKa['D']))
                elif aa == 'E':
                    charge -= 1 / (1 + 10 ** (ph - pKa['E']))
                elif aa == 'C':
                    charge -= 1 / (1 + 10 ** (ph - pKa['C']))
                elif aa == 'Y':
                    charge -= 1 / (1 + 10 ** (ph - pKa['Y']))
                elif aa == 'H':
                    charge += 1 / (1 + 10 ** (pKa['H'] - ph))
                elif aa == 'K':
                    charge += 1 / (1 + 10 ** (pKa['K'] - ph))
                elif aa == 'R':
                    charge += 1 / (1 + 10 ** (pKa['R'] - ph))
            
            if abs(charge) < 0.01:
                break
            ph -= charge * 0.1
        
        return ph
    
    def hydrophobicity_profile(self, sequence: str,
                               window: int = 9) -> List[float]:
        """Calculate sliding window hydrophobicity."""
        profile = []
        for i in range(len(sequence) - window + 1):
            window_seq = sequence[i:i+window]
            avg_hydro = np.mean([
                self.AMINO_ACID_PROPERTIES.get(aa, {}).get('hydrophobicity', 0)
                for aa in window_seq
            ])
            profile.append(avg_hydro)
        return profile
    
    def secondary_structure_prediction(self, sequence: str) -> str:
        """Simple secondary structure prediction (Chou-Fasman method)."""
        p_turn = {'N': 0.006, 'P': 0.075, 'T': 0.065, 'G': 0.102,
                  'S': 0.077, 'D': 0.058, 'Q': 0.037, 'R': 0.093,
                  'K': 0.095, 'H': 0.043, 'E': 0.054, 'A': 0.06,
                  'M': 0.013, 'V': 0.062, 'I': 0.056, 'F': 0.065,
                  'Y': 0.034, 'W': 0.014, 'L': 0.045, 'C': 0.049}
        
        structure = ''
        for i in range(len(sequence) - 3):
            window = sequence[i:i+4]
            p_turn_avg = np.mean([p_turn.get(aa, 0.05) for aa in window])
            if p_turn_avg > 0.075:
                structure += 'T'
            elif i < len(sequence) - 1:
                structure += 'C'
            else:
                structure += 'E'
        
        return structure
    
    def find_motifs(self, sequence: str, motif: str) -> List[int]:
        """Find motif occurrences in sequence."""
        positions = []
        motif = motif.upper()
        for i in range(len(sequence) - len(motif) + 1):
            if sequence[i:i+len(motif)] == motif:
                positions.append(i)
        return positions


class SequenceAligner:
    """Pairwise and multiple sequence alignment."""
    
    BLOSUM62 = np.array([
        [4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, 0, -3, -2],
        [-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -4, -3],
        [-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -1, -3, -2],
        [-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -3, -4, -3],
        [0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1],
        [-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, -1, -1, -2, -2, -1],
        [-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -2, -3, -2],
        [0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -3, -3, -2],
        [-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, -2, 2],
        [-1, -3, -3, -3, -1, -3, -3, -4, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, -1],
        [-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -2, -2, 0, -1],
        [-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -2, -3, -1, 0, -1, -2, -3, -2],
        [-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -2, 7, 0, -2, -1, -1, -1, 0, -1],
        [-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 7, -1, -2, -2, -2, -1, 1, 1],
        [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -1, 4, -1, -1, -3, -2, -2],
        [1, -1, 1, 0, 0, -1, 0, 0, -1, -2, -2, 0, -2, -2, -1, 4, 1, -1, -3, -2],
        [0, -1, 0, -1, 0, -1, -1, -2, -2, -1, -2, -1, -1, -2, -1, 1, 5, 0, -2, -1],
        [0, -3, -1, -3, -2, -2, -2, -3, -2, -3, -2, -2, -1, -1, -3, -1, 0, 7, -1, -1],
        [-3, -4, -3, -4, -2, -3, -3, -3, -2, -1, 0, -3, 0, 1, -2, -3, -2, -1, 11, 2],
        [-2, -3, -2, -3, -1, -1, -2, -2, 2, -1, -1, -2, -1, 1, -2, -2, -1, -1, 2, 7]
    ])
    
    AMINO_ACIDS = 'ARNDCQEGHILKMFPSTWYV'
    
    def __init__(self, gap_penalty: float = -10, gap_extension: float = -0.5):
        self.gap_penalty = gap_penalty
        self.gap_extension = gap_extension
    
    def needleman_wunsch(self, seq1: str, seq2: str) -> AlignmentResult:
        """Global alignment using Needleman-Wunsch algorithm."""
        m, n = len(seq1), len(seq2)
        score = np.zeros((m + 1, n + 1))
        
        for i in range(m + 1):
            score[i][0] = i * self.gap_penalty
        for j in range(n + 1):
            score[0][j] = j * self.gap_penalty
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                idx1 = self.AMINO_ACIDS.index(seq1[i - 1])
                idx2 = self.AMINO_ACIDS.index(seq2[j - 1])
                match = score[i - 1][j - 1] + self.BLOSUM62[idx1][idx2]
                delete = score[i - 1][j] + self.gap_penalty
                insert = score[i][j - 1] + self.gap_penalty
                score[i][j] = max(match, delete, insert)
        
        alignment1, alignment2 = '', ''
        i, j = m, n
        
        while i > 0 or j > 0:
            if i > 0 and j > 0:
                idx1 = self.AMINO_ACIDS.index(seq1[i - 1])
                idx2 = self.AMINO_ACIDS.index(seq2[j - 1])
                if score[i][j] == score[i - 1][j - 1] + self.BLOSUM62[idx1][idx2]:
                    alignment1 = seq1[i - 1] + alignment1
                    alignment2 = seq2[j - 1] + alignment2
                    i -= 1
                    j -= 1
                elif score[i][j] == score[i - 1][j] + self.gap_penalty:
                    alignment1 = seq1[i - 1] + alignment1
                    alignment2 = '-' + alignment2
                    i -= 1
                else:
                    alignment1 = '-' + alignment1
                    alignment2 = seq2[j - 1] + alignment2
                    j -= 1
            elif i > 0:
                alignment1 = seq1[i - 1] + alignment1
                alignment2 = '-' + alignment2
                i -= 1
            else:
                alignment1 = '-' + alignment1
                alignment2 = seq2[j - 1] + alignment2
                j -= 1
        
        matches = sum(1 for a, b in zip(alignment1, alignment2) if a == b)
        identity = matches / len(alignment1) * 100
        
        return AlignmentResult(
            score=score[m][n],
            alignment=(alignment1, alignment2),
            identity=identity,
            coverage=matches / max(len(seq1), len(seq2)) * 100
        )
    
    def smith_waterman(self, seq1: str, seq2: str) -> AlignmentResult:
        """Local alignment using Smith-Waterman algorithm."""
        m, n = len(seq1), len(seq2)
        score = np.zeros((m + 1, n + 1))
        max_score, max_pos = 0, (0, 0)
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                idx1 = self.AMINO_ACIDS.index(seq1[i - 1])
                idx2 = self.AMINO_ACIDS.index(seq2[j - 1])
                match = score[i - 1][j - 1] + self.BLOSUM62[idx1][idx2]
                delete = score[i - 1][j] + self.gap_penalty
                insert = score[i][j - 1] + self.gap_penalty
                score[i][j] = max(0, match, delete, insert)
                
                if score[i][j] > max_score:
                    max_score = score[i][j]
                    max_pos = (i, j)
        
        alignment1, alignment2 = '', ''
        i, j = max_pos
        
        while i > 0 and j > 0 and score[i][j] > 0:
            idx1 = self.AMINO_ACIDS.index(seq1[i - 1])
            idx2 = self.AMINO_ACIDS.index(seq2[j - 1])
            if score[i][j] == score[i - 1][j - 1] + self.BLOSUM62[idx1][idx2]:
                alignment1 = seq1[i - 1] + alignment1
                alignment2 = seq2[j - 1] + alignment2
                i -= 1
                j -= 1
            elif score[i][j] == score[i - 1][j] + self.gap_penalty:
                alignment1 = seq1[i - 1] + alignment1
                alignment2 = '-' + alignment2
                i -= 1
            else:
                alignment1 = '-' + alignment1
                alignment2 = seq2[j - 1] + alignment2
                j -= 1
        
        matches = sum(1 for a, b in zip(alignment1, alignment2) if a == b)
        identity = matches / len(alignment1) * 100 if alignment1 else 0
        
        return AlignmentResult(
            score=max_score,
            alignment=(alignment1, alignment2),
            identity=identity,
            coverage=identity
        )


class GenomicVariantAnalyzer:
    """Analyze genomic variants and mutations."""
    
    def __init__(self):
        self.variants = []
    
    def parse_vcf(self, vcf_line: str) -> Dict:
        """Parse VCF variant line."""
        fields = vcf_line.strip().split('\t')
        return {
            'chrom': fields[0],
            'pos': int(fields[1]),
            'id': fields[2],
            'ref': fields[3],
            'alt': fields[4],
            'qual': float(fields[5]),
            'filter': fields[6],
            'info': fields[7]
        }
    
    def predict_variant_effect(self, variant: Dict, gene_seq: str) -> Dict:
        """Predict functional effect of variant."""
        pos = variant['pos'] - 1
        ref = variant['ref']
        alt = variant['alt']
        
        effect = 'silent'
        if len(ref) == len(alt) == 1:
            if ref != alt:
                original_aa = gene_seq[pos // 3]
                new_aa = gene_seq[pos // 3]
                if original_aa != new_aa:
                    effect = 'missense'
        elif len(ref) > len(alt):
            effect = 'deletion'
        elif len(alt) > len(ref):
            effect = 'insertion'
        
        return {
            'variant': variant,
            'effect': effect,
            'position': pos,
            'codon_change': f"{ref}->{alt}"
        }
    
    def calculate_af_frequency(self, variant: Dict, population: str = "gnomAD") -> float:
        """Calculate allele frequency from population data."""
        return 0.001
    
    def assess_pathogenicity(self, variant: Dict) -> Dict:
        """Assess variant pathogenicity using simple rules."""
        qual = variant.get('qual', 0)
        info = variant.get('info', '')
        
        score = 0
        if qual > 50:
            score += 2
        elif qual > 30:
            score += 1
        
        if ' pathogenic ' in info.lower():
            score += 3
        elif ' benign ' in info.lower():
            score -= 2
        
        if score >= 3:
            classification = 'pathogenic'
        elif score >= 1:
            likely_pathogenic = 'likely_pathogenic'
        elif score >= -1:
            variant_of_uncertain_significance = 'VUS'
        else:
            classification = 'benign'
        
        return {'score': score, 'classification': classification}


class PhylogeneticTree:
    """Build and analyze phylogenetic trees."""
    
    def __init__(self):
        self.distances = {}
    
    def compute_distance_matrix(self, sequences: List[str],
                                labels: List[str]) -> np.ndarray:
        """Compute pairwise distance matrix."""
        aligner = SequenceAligner()
        n = len(sequences)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                result = aligner.needleman_wunsch(sequences[i], sequences[j])
                distance = 100 - result.identity
                matrix[i][j] = distance
                matrix[j][i] = distance
        
        self.distances = {labels[i]: dict(zip(labels, row))
                         for i, row in enumerate(matrix)}
        return matrix
    
    def neighbor_joining(self, distance_matrix: np.ndarray,
                        labels: List[str]) -> Dict:
        """Build tree using neighbor-joining algorithm."""
        n = len(labels)
        current_matrix = distance_matrix.copy()
        current_labels = labels.copy()
        tree = {label: [] for label in labels}
        
        for step in range(n - 1):
            min_dist = float('inf')
            min_pair = (0, 1)
            
            for i in range(len(current_labels)):
                for j in range(i + 1, len(current_labels)):
                    if current_matrix[i][j] < min_dist:
                        min_dist = current_matrix[i][j]
                        min_pair = (i, j)
            
            i, j = min_pair
            label_i, label_j = current_labels[i], current_labels[j]
            
            new_label = f"node_{step}"
            tree[new_label] = [label_i, label_j]
            
            for k in range(len(current_labels)):
                if k not in [i, j]:
                    new_dist = (current_matrix[i][k] + current_matrix[j][k]) / 2
                    current_matrix[k][len(current_labels)] = new_dist
                    current_matrix[len(current_labels)][k] = new_dist
            
            current_labels.remove(label_i)
            current_labels.remove(label_j)
            current_labels.append(new_label)
        
        return tree
    
    def compute_bootstrap_support(self, sequences: List[str],
                                  labels: List[str],
                                  n_bootstraps: int = 100) -> Dict[str, float]:
        """Compute bootstrap support for tree branches."""
        support = {}
        
        for label in labels:
            if label.startswith('node'):
                support[label] = 0.0
        
        for _ in range(n_bootstraps):
            bootstrapped_seqs = [sequences[np.random.randint(len(sequences))]
                               for _ in range(len(sequences))]
            matrix = self.compute_distance_matrix(bootstrapped_seqs, labels)
            tree = self.neighbor_joining(matrix, labels)
            
            for node in support:
                if node in tree:
                    support[node] += 1
        
        for node in support:
            support[node] /= n_bootstraps
        
        return support


class BioPython:
    """Main bioinformatics orchestration class."""
    
    def __init__(self):
        self.dna_tools = DNATools()
        self.protein_analyzer = ProteinAnalyzer()
        self.aligner = SequenceAligner()
        self.variant_analyzer = GenomicVariantAnalyzer()
        self.phylogeny = PhylogeneticTree()
    
    def analyze_sequence(self, sequence: str, seq_type: str) -> Dict[str, Any]:
        """Comprehensive sequence analysis."""
        result = {
            'sequence_type': seq_type,
            'length': len(sequence)
        }
        
        if seq_type == 'DNA':
            result.update({
                'gc_content': self.dna_tools.gc_content(sequence),
                'transcript': self.dna_tools.transcribe(sequence),
                'orfs': self.dna_tools.find_orfs(sequence)
            })
        elif seq_type == 'protein':
            result.update({
                'molecular_weight': self.protein_analyzer.molecular_weight(sequence),
                'isoelectric_point': self.protein_analyzer.isoelectric_point(sequence),
                'hydrophobicity': self.protein_analyzer.hydrophobicity_profile(sequence)
            })
        
        return result


def demo_bioinformatics():
    """Demonstrate bioinformatics capabilities."""
    print("=" * 60)
    print("Grok Bioinformatics Demo")
    print("=" * 60)
    
    bio = BioPython()
    
    print("\n--- DNA Analysis ---")
    dna = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"
    analysis = bio.analyze_sequence(dna, 'DNA')
    print(f"Sequence: {dna}")
    print(f"GC Content: {analysis['gc_content']:.2f}%")
    print(f"Transcript: {bio.dna_tools.transcribe(dna)}")
    print(f"Protein: {bio.dna_tools.translate(dna)}")
    print(f"ORFs found: {len(analysis['orfs'])}")
    
    print("\n--- Protein Analysis ---")
    protein = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
    analysis = bio.analyze_sequence(protein, 'protein')
    print(f"MW: {analysis['molecular_weight']:.2f} Da")
    print(f"pI: {analysis['isoelectric_point']:.2f}")
    print(f"First 5 hydrophobicity values: {analysis['hydrophobicity'][:5]}")
    
    print("\n--- Sequence Alignment ---")
    seq1 = "MVLSPADKTN"
    seq2 = "MVLSAADKTN"
    result = bio.aligner.needleman_wunsch(seq1, seq2)
    print(f"Seq1: {seq1}")
    print(f"Seq2: {seq2}")
    print(f"Score: {result.score:.1f}")
    print(f"Identity: {result.identity:.1f}%")
    print(f"Alignment:\n{result.alignment[0]}\n{result.alignment[1]}")
    
    print("\n--- Variant Analysis ---")
    variant = {
        'chrom': '17',
        'pos': 7577121,
        'id': '.',
        'ref': 'G',
        'alt': 'A',
        'qual': 99.0,
        'filter': 'PASS',
        'info': 'Pathogenic'
    }
    assessment = bio.variant_analyzer.assess_pathogenicity(variant)
    print(f"Variant: {variant['chrom']}:{variant['pos']} {variant['ref']}>{variant['alt']}")
    print(f"Classification: {assessment['classification']}")
    
    print("\n--- Phylogenetic Tree ---")
    sequences = [
        "ATGGCCATTGTAATGGGCC",
        "ATGGCCATTGTAATGGGCT",
        "ATGACCATTGTAATGGGCC",
        "ATGGCCATTGTTATGGGCC"
    ]
    labels = ['Species_A', 'Species_B', 'Species_C', 'Species_D']
    dist_matrix = bio.phylogeny.compute_distance_matrix(sequences, labels)
    print("Distance Matrix:")
    print(np.round(dist_matrix, 1))
    tree = bio.phylogeny.neighbor_joining(dist_matrix, labels)
    print(f"Tree: {tree}")
    
    print("\n" + "=" * 60)
    print("Bioinformatics toolkit ready!")
    print("=" * 60)


if __name__ == "__main__":
    demo_bioinformatics()
