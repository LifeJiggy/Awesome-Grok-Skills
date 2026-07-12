---
name: "genomic-analysis"
category: "bioinformatics"
version: "2.0.0"
tags: ["bioinformatics", "genomics", "NGS", "variant-calling", "alignment"]
---

# Genomic Analysis

## Overview

The Genomic Analysis module provides a comprehensive toolkit for Next-Generation Sequencing (NGS) data processing, variant calling, and genomic interpretation. It covers the full bioinformatics pipeline from raw FASTQ reads through aligned BAMs, called VCFs, and annotated variant reports. The module integrates with industry-standard tools (BWA, GATK, samtools) via Python wrappers and provides native implementations for common analytical tasks such as quality control, read alignment, variant discovery, and structural variant detection.

This skill is designed for bioinformaticians building production pipelines, researchers conducting genome-wide association studies (GWAS), and clinical genomics teams performing diagnostic variant interpretation.

## Core Capabilities

- **Quality Control**: FastQC-style per-base quality metrics, adapter contamination detection, GC bias analysis, and duplication rate estimation
- **Read Alignment**: BWA-MEM and Minimap2 wrappers for short-read and long-read alignment with reference genome indexing
- **Variant Calling**: GATK HaplotypeCaller and Mutect2 integration for germline and somatic SNV/Indel calling, plus DeepVariant neural-network-based calling
- **Structural Variant Detection**: Manta and Delly wrappers for large deletions, duplications, inversions, and translocations
- **Variant Annotation**: VEP (Variant Effect Predictor) and ANNOVAR integration for functional consequence prediction, population frequency lookup, and clinical significance classification
- **Coverage Analysis**: Targeted sequencing depth calculation, on-target rate metrics, and uniformity statistics
- **Phylogenetic Inference**: Neighbor-joining and maximum-likelihood tree construction from SNP alignment matrices
- **Reporting**: Automated multi-sample variant summary reports in HTML and PDF formats

## Usage Examples

```python
from genomic_analysis import (
    QualityControl,
    ReadAligner,
    VariantCaller,
    VariantAnnotator,
    CoverageAnalyzer,
)

# --- Quality Control Pipeline ---
qc = QualityControl(
    fastq_r1="sample_R1.fastq.gz",
    fastq_r2="sample_R2.fastq.gz",
    adapter_sequence="AGATCGGAAGAGC",
)
qc_report = qc.run()
print(f"Mean Q30: {qc_report.mean_q30:.1f}%")
print(f"Adapter contamination: {qc_report.adapter_pct:.2f}%")
if qc_report.mean_q30 < 80.0:
    qc.trim_quality(min_quality=20, min_length=50)
    qc_report = qc.run()

# --- Read Alignment ---
aligner = ReadAligner(
    reference="hg38.fa",
    threads=16,
    read_group="@RG\\tID:sample1\\tSM:sample1\\tPL:ILLUMINA",
)
aligner.index_reference()
bam_path = aligner.align(
    r1="sample_R1.trimmed.fq.gz",
    r2="sample_R2.trimmed.fq.gz",
    output="sample1.bam",
)
sorted_bam = aligner.sort(bam_path, memory="8G")
aligner.mark_duplicates(sorted_bam, output="sample1.dedup.bam")

# --- Variant Calling (Germline) ---
caller = VariantCaller(
    reference="hg38.fa",
    mode="germline",
    gatk_path="/opt/gatk/gatk",
)
vcf_path = caller.haplotype_caller(
    bam="sample1.dedup.bam",
    intervals="exome.targets.bed",
    output="sample1.g.vcf.gz",
    emit_ref_confidence="GVCF",
)

# --- Variant Annotation ---
annotator = VariantAnnotator(
    vcf="sample1.g.vcf.gz",
    cache_dir="~/.vep/cache",
    plugins=["CADD", "SpliceAI"],
)
annotated_vcf = annotator.annotate(output="sample1.annotated.vcf.gz")
summary = annotator.summary_report()
print(f"Total variants: {summary.total}")
print(f"Pathogenic: {summary.pathogenic}")
print(f"Likely pathogenic: {summary.likely_pathogenic}")
```

## Best Practices

- Always perform quality control before alignment — never skip QC even with trusted sequencing providers
- Use GATK Best Practices workflows for germline and somatic variant calling
- Index reference genomes with `samtools faidx` and `bwa index` before alignment runs
- Use `-L intervals.bed` for targeted sequencing to avoid wasted computation on off-target regions
- Apply hard filtering on VQSR-ineligible sample sizes (< 30 exomes or < 1 WGS)
- Validate called variants against orthogonal technologies (Sanger, qPCR) for clinical applications
- Store pipeline provenance with sample metadata, tool versions, and parameters for reproducibility
- Use cloud-native storage (S3, GCS) for large-scale cohort analyses to avoid I/O bottlenecks
- Compress all intermediate files with `bgzip` and index with `tabix` to save disk space
- Run structural variant calling in parallel with SNV/Indel calling to minimize wall-clock time

## Related Modules

- **sequence-alignment**: Advanced alignment algorithms and scoring matrices
- **protein-structure**: Structural interpretation of genomic variants
- **phylogenetics**: Evolutionary analysis from genomic data
- **drug-discovery**: Pharmacogenomic variant interpretation for drug response
