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

---

## Advanced Configuration

### Reference Genome Management

```python
from genomic_analysis import ReferenceManager

# Local reference cache with symbolic links to save disk
ref_mgr = ReferenceManager(cache_dir="/data/references")
ref_mgr.add(
    name="hg38",
    fasta="/data/references/hg38.fa",
    bwt_index="/data/references/hg38.fa.bwt",
    dict_index="/data/references/hg38.dict",
)
ref_mgr.add_alias("GRCh38", "hg38")
ref_mgr.add_alias("hs38", "hg38")

# Retrieve reference by any alias
fasta, indices = ref_mgr.resolve("GRCh38")
```

### Multi-Sample Joint Calling

```python
from genomic_analysis import JointCaller

joint = JointCaller(
    reference="hg38",
    gatk_path="/opt/gatk/gatk",
    scatter_count=50,
)

# GenomicsDBImport for cohort
import_genome = joint.import_gvcfs(
    gvcf_list="cohort_gvcfs.list",
    intervals="wgs.targets.bed",
    output_db="cohort_db",
)

# GenotypeGVCFs for joint calls
joint.genotype(
    database=import_genome,
    output="cohort.joint.vcf.gz",
    annotation_groups=["StandardAnnotation", "AS_StandardAnnotation"],
)

# VQSR or hard filtering
if joint.sample_count >= 30:
    joint.vqsr(
        vcf="cohort.joint.vcf.gz",
        mode="SNP",
        resources={
            "dbsnp": "dbsnp.vcf.gz",
            "hapmap": "hapmap.vcf.gz",
            "omni": "1000G_omni.vcf.gz",
            "mills": "Mills_and_1000G_gold_standard.vcf.gz",
        },
    )
else:
    joint.hard_filter(
        vcf="cohort.joint.vcf.gz",
        filters={
            "SNP": "QD<2.0 || FS>60.0 || MQ<40.0 || MQRankSum<-12.5 || ReadPosRankSum<-8.0",
            "INDEL": "QD<2.0 || FS>200.0 || ReadPosRankSum<-20.0",
        },
    )
```

### Somatic Variant Calling (Tumor-Normal Pairs)

```python
from genomic_analysis import SomaticCaller

somatic = SomaticCaller(
    reference="hg38",
    gatk_path="/opt/gatk/gatk",
    panel_of_normals="pon.vcf.gz",
    known_sites=["dbsnp.vcf.gz", "cosmic.vcf.gz"],
)

# Mutect2 somatic calling
calls = somatic.mutect2(
    tumor_bam="tumor.dedup.bam",
    normal_bam="normal.dedup.bam",
    output="somatic.vcf.gz",
    intervals="exome.targets.bed",
    f1r2_tar="f1r2.tar.gz",
)

# Learn read orientation model and filter
somatic.learn_read_orientation(f1r2="f1r2.tar.gz")
somatic.filter_mutect(calls, output="somatic.filtered.vcf.gz")

# Funcotator annotation
somatic.funcotate(
    vcf="somatic.filtered.vcf.gz",
    output="somatic.funcotated.vcf.gz",
    reference="hg38",
    funcotator_data_sources="/data/funcotator_data",
)
```

### Pipeline Configuration File

```yaml
# pipeline_config.yaml
pipeline:
  name: "germline_wgs"
  version: "3.2.1"
  reference: "hg38"

qc:
  adapter_trim: true
  min_quality: 20
  min_read_length: 50
  duplication_flag: true

alignment:
  tool: "bwa-mem2"
  threads: 32
  sort_memory: "16G"
  mark_duplicates: true
  bqsr: true

variant_calling:
  tool: "haplotype_caller"
  mode: "germline"
  emit_ref_confidence: "GVCF"
  gvcf_gq_bands:
    - "[0,30)"
    - "[30,40)"
    - "[40,50)"
    - "[50,60)"
    - "[60,70)"
    - "[70,80)"
    - "[80,90)"
    - "[90,100)"

annotation:
  tool: "vep"
  plugins:
    - "CADD"
    - "SpliceAI"
    - "dbNSFP"
    - "AlphaMissense"
  cache_dir: "~/.vep/cache"

output:
  format: "vcf.gz"
  index: "tbi"
  report: "html"
```

## Architecture Patterns

```
┌─────────────────────────────────────────────────────────┐
│                 Genomic Analysis Pipeline                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │  FASTQ   │───▶│   QC     │───▶│  Trimming /      │  │
│  │  Reads   │    │  Report  │    │  Filtering       │  │
│  └──────────┘    └──────────┘    └────────┬─────────┘  │
│                                           │             │
│                                    ┌──────▼──────┐     │
│                                    │  Alignment  │     │
│                                    │  (BWA-MEM2) │     │
│                                    └──────┬──────┘     │
│                                           │             │
│                              ┌────────────┼───────────┐│
│                              │            │           ││
│                        ┌─────▼─────┐ ┌───▼───┐ ┌────▼┐│
│                        │ Sort +    │ │ BQSR  │ │ Mark ││
│                        │ Index     │ │       │ │ Dup  ││
│                        └─────┬─────┘ └───┬───┘ └──┬──┘│
│                              │           │        │   ││
│                        ┌─────▼───────────▼────────▼──┐│
│                        │     Processed BAM/CRAM      ││
│                        └─────┬───────────┬────────┬──┘│
│                              │           │        │   ││
│                    ┌─────────▼───┐ ┌─────▼────┐ ┌─▼──┐│
│                    │ Germline    │ │ Somatic  │ │ SV ││
│                    │ Calling     │ │ Calling  │ │Det.││
│                    │ (Haplotype) │ │ (Mutect2)│ │    ││
│                    └──────┬──────┘ └────┬─────┘ └┬───┘│
│                           │            │         │    ││
│                    ┌──────▼────────────▼─────────▼──┐│
│                    │        Merged VCF               ││
│                    └──────┬─────────────────────────┘│
│                           │                          │
│                    ┌──────▼──────┐                    │
│                    │ Annotation  │                    │
│                    │ (VEP/ANNOVAR)│                   │
│                    └──────┬──────┘                    │
│                           │                          │
│                    ┌──────▼──────┐                    │
│                    │   Report    │                    │
│                    │  (HTML/PDF) │                    │
│                    └─────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

```
Variant Calling Decision Tree:

    Sample Size < 30 exomes?
         │
    ┌────┴────┐
    │  YES    │  NO
    │         │
    ▼         ▼
Hard Filter  VQSR
    │         │
    │    ┌────┴────┐
    │    │ SNP VQSR│──▶ Tranche 99.5% ──▶ SNP Filter
    │    └────┬────┘
    │         │
    │    ┌────┴────┐
    │    │Indel VQSR│──▶ Tranche 99.0% ──▶ Indel Filter
    │    └─────────┘
    │
    ▼
Filter expression string
QD<2.0 || FS>60.0 || MQ<40.0
```

## Integration Guide

### External Tool Integration

```python
from genomic_analysis import PipelineRunner

runner = PipelineRunner(
    conda_env="ngs_pipeline",
    container="docker://broadinstitute/gatk:4.6.1.0",
    scheduler="slurm",
)

# Define pipeline stages with dependencies
runner.add_stage("qc", tool="fastqc", threads=8, memory="16G")
runner.add_stage("trim", tool="fastp", threads=4, depends=["qc"])
runner.add_stage("align", tool="bwa-mem2", threads=32, depends=["trim"])
runner.add_stage("sort", tool="samtools", depends=["align"])
runner.add_stage("dedup", tool="gatk MarkDuplicates", depends=["sort"])
runner.add_stage("bqsr", tool="gatk BaseRecalibrator", depends=["dedup"])
runner.add_stage("call", tool="gatk HaplotypeCaller", depends=["bqsr"])
runner.add_stage("annotate", tool="vep", depends=["call"])

# Execute with dependency resolution
runner.execute(samples="samples.tsv", dry_run=False)
```

### Cloud Storage Integration

```python
from genomic_analysis import CloudStorage

cloud = CloudStorage(provider="gcs", bucket="my-project-data")

# Upload local BAM to cloud with index
cloud.upload("sample1.dedup.bam", prefix="runs/2024-01/")
cloud.upload("sample1.dedup.bam.bai", prefix="runs/2024-01/")

# Stream reads from cloud for alignment (no local download needed)
aligner = ReadAligner(reference="gs://refs/hg38.fa")
bam = aligner.align(
    r1="gs://reads/sample_R1.fq.gz",
    r2="gs://reads/sample_R2.fq.gz",
    output="gs://runs/2024-01/sample1.bam",
)
```

### REST API Integration

```python
from genomic_analysis import VariantAPI

api = VariantAPI(base_url="https://api.variantregistry.org/v2")

# Submit VCF for annotation
job = api.submit_annotation(
    vcf_url="gs://runs/2024-01/cohort.vcf.gz",
    reference="hg38",
    annotations=["clinvar", "gnomad", "dbsnp"],
)

# Poll for completion
import time
while not job.is_complete:
    time.sleep(30)
    job.refresh()

# Download annotated results
api.download(job.id, "annotated_results.vcf.gz")
```

## Performance Optimization

### Parallelization Strategies

```python
from genomic_analysis import Parallelizer

parallel = Parallelizer(scheduler="slurm", nodes=4, cpus_per_node=32)

# Scatter-gather pattern for variant calling
parallel.scatter_gather(
    tool="gatk HaplotypeCaller",
    intervals="wgs.targets.bed",
    scatter_count=100,
    input_files=["sample1.bam"],
    output_pattern="sample1.g.vcf.gz",
    merge_tool="gatk CombineGVCFs",
)

# Parallel multi-sample processing
parallel.map_over_samples(
    pipeline="full_pipeline",
    sample_sheet="samples.csv",
    max_concurrent=8,
)
```

### Memory and Disk Optimization

```python
from genomic_analysis import ResourceOptimizer

optimizer = ResourceOptimizer()

# Estimate memory requirements
estimates = optimizer.estimate(
    tool="haplotype_caller",
    input_size_gb=120,
    reference_size_gb=3.2,
    sample_count=1,
)
print(f"Recommended memory: {estimates.memory_gb} GB")
print(f"Recommended disk: {estimates.disk_gb} GB")
print(f"Estimated runtime: {estimates.runtime_hours:.1f} hours")

# Optimize disk usage during pipeline
optimizer.enable_streaming_mode(
    temp_dir="/scratch",
    max_temp_gb=500,
    cleanup_on_success=True,
    keep_on_failure=True,
)
```

### Reference Caching

```python
from genomic_analysis import ReferenceCache

cache = ReferenceCache(
    cache_dir="/data/references",
    max_size_gb=50,
    eviction_policy="lru",
)

# Pre-fetch and index references
cache.prefetch("hg38", sources=[
    "https://s3.amazonaws.com/broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.gz",
])

# Shared index pool across pipelines
cache.register_shared_indices(
    bwt_index="/data/references/hg38.fa.bwt",
    dict_index="/data/references/hg38.dict",
    fai_index="/data/references/hg38.fa.fai",
)
```

## Security Considerations

### Data Privacy (HIPAA/GDPR Compliance)

- Never log raw read data, variant calls, or sample identifiers in pipeline logs
- Encrypt all intermediate and output files at rest using AES-256
- Use secure transfer protocols (HTTPS, SFTP) for data movement
- Implement access controls on variant databases — not all users need access to raw variants
- Anonymize sample IDs in reports before sharing externally
- Audit all data access and pipeline execution events
- Retain chain-of-custody documentation for clinical sequencing data
- Implement data retention policies aligned with institutional requirements

### Secure Pipeline Execution

```python
from genomic_analysis import SecurePipeline

secure = SecurePipeline(
    encryption_key_file="/secure/keys/pipeline.key",
    audit_log="/var/log/ngs_audit.log",
    max_permission_level="clinical",
)

# Run with access controls
secure.execute(
    pipeline="germline_wgs",
    sample_sheet="samples.csv",
    user="analyst_jdoe",
    project="PRJ_2024_001",
    approval_token="APPROVED_BY_PI_20240115",
)
```

### Credential and Secret Management

- Store API keys, cloud credentials, and database passwords in a secrets manager (HashiCorp Vault, AWS Secrets Manager)
- Never hardcode credentials in pipeline scripts or configuration files
- Use service accounts with minimal required permissions for cloud operations
- Rotate credentials on a regular schedule (90 days maximum)
- Use temporary credentials (STS tokens) for short-lived pipeline jobs
- Audit credential usage and alert on anomalous access patterns

## Troubleshooting Guide

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| BWA index fails with OOM | Reference genome too large for available memory | Use `bwa-mem2 index` with `--threads 8` and 64GB RAM; or split reference into contigs |
| HaplotypeCaller crashes on chrM | Mitochondrial genome has different properties | Call chrM separately with `-L chrM` and relaxed parameters |
| VQSR fails to converge | Insufficient training sites or samples | Use hard filtering with < 30 exomes; increase `--max-gaussians` for larger datasets |
| BAM index mismatch error | BAM and BAI files are out of sync | Re-index with `samtools index -c` or regenerate BAI after re-sort |
| Variant call count differs between callers | Different statistical models and thresholds | Use consensus calling (intersection of 2+ callers) for clinical reporting |
| GATK Queue/Spark throws Java errors | Java version incompatibility | Use GATK 4.x bundled Java; check `java -version` matches GATK requirements |
| VEP annotation is slow | Large VCF and remote cache | Use local VEP cache with `--offline` flag; increase `--fork` for parallelism |
| Coverage is uneven in targeted regions | Poor capture efficiency or PCR bias | Check library complexity metrics; increase on-target enrichment stringency |
| Structural variant calls have low sensitivity | Insufficient read depth or paired-end info | Use SV-caller ensemble (Manta + Delly + GRIDSS); ensure proper insert size |
| Pipeline fails at merge step | GVCF blocks don't overlap | Ensure consistent intervals across all samples; use `CombineGVCFs` not `MergeVCFs` |
| Out-of-memory during sorting | SAMTOOLS_SORT memory limit too low | Set `-m 8G` for `samtools sort`; use `--threads` to reduce per-thread memory |
| Tabix index creation fails | File not bgzipped | Use `bgzip` not `gzip`; ensure `.gz` extension for tabix compatibility |

## API Reference

### QualityControl

```python
class QualityControl:
    """Performs FASTQ quality control and trimming."""

    def __init__(
        self,
        fastq_r1: str,
        fastq_r2: str = None,
        adapter_sequence: str = "AGATCGGAAGAGC",
        minimum_length: int = 36,
        threads: int = 4,
    ): ...

    def run(self) -> QCReport:
        """Execute QC analysis and return report."""

    def trim_quality(
        self,
        min_quality: int = 20,
        min_length: int = 50,
        sliding_window: tuple = (4, 15),
    ) -> str:
        """Trim low-quality bases; returns path to trimmed FASTQ."""

    def gc_content_plot(self, output: str = None) -> str:
        """Generate GC content distribution plot."""

    def adapter_content_plot(self, output: str = None) -> str:
        """Generate adapter content plot."""

class QCReport:
    mean_q30: float          # Percentage of bases >= Q30
    adapter_pct: float       # Adapter contamination percentage
    gc_mean: float           # Mean GC content
    duplication_rate: float  # Duplication rate estimate
    total_reads: int         # Total read count
    passed_reads: int        # Reads passing QC
```

### ReadAligner

```python
class ReadAligner:
    def __init__(
        self,
        reference: str,
        threads: int = 8,
        read_group: str = None,
        algorithm: str = "mem",
    ): ...

    def index_reference(self) -> None:
        """Build BWA-MEM2 index for reference genome."""

    def align(
        self,
        r1: str,
        r2: str = None,
        output: str = "aligned.bam",
        read_groups: dict = None,
    ) -> str:
        """Align reads and return output BAM path."""

    def sort(
        self,
        bam: str,
        memory: str = "4G",
        order: str = "coordinate",
    ) -> str:
        """Sort BAM file."""

    def mark_duplicates(
        self,
        bam: str,
        output: str = None,
        metrics_file: str = None,
    ) -> str:
        """Mark or remove duplicate reads."""

    def recalibrate(
        self,
        bam: str,
        known_sites: list,
        output: str = None,
    ) -> str:
        """Base Quality Score Recalibration (BQSR)."""
```

### VariantCaller

```python
class VariantCaller:
    def __init__(
        self,
        reference: str,
        mode: str = "germline",
        gatk_path: str = "gatk",
    ): ...

    def haplotype_caller(
        self,
        bam: str,
        intervals: str = None,
        output: str = "output.vcf.gz",
        emit_ref_confidence: str = "NONE",
        pcr_mode: str = "conservative",
    ) -> str:
        """Run GATK HaplotypeCaller."""

    def mutect2(
        self,
        tumor_bam: str,
        normal_bam: str = None,
        output: str = "somatic.vcf.gz",
        panel_of_normals: str = None,
    ) -> str:
        """Run Mutect2 somatic caller."""

    def joint_genotype(
        self,
        gvcf_list: str,
        output: str = "joint.vcf.gz",
        database: str = None,
    ) -> str:
        """Joint genotyping across samples."""

    def select_variants(
        self,
        vcf: str,
        variant_type: str = "SNP",
        output: str = None,
    ) -> str:
        """Select SNPs or Indels from VCF."""
```

### VariantAnnotator

```python
class VariantAnnotator:
    def __init__(
        self,
        vcf: str,
        reference: str = "hg38",
        cache_dir: str = "~/.vep/cache",
        plugins: list = None,
    ): ...

    def annotate(self, output: str = None) -> str:
        """Annotate VCF using VEP; returns output path."""

    def summary_report(self) -> AnnotationSummary:
        """Generate summary statistics of annotated variants."""

    def filter_by_consequence(
        self,
        consequences: list,
        output: str = None,
    ) -> str:
        """Filter variants by consequence type."""

    def export_to_table(self, output: str = None) -> str:
        """Export annotated VCF to tabular format."""
```

## Data Models

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

@dataclass
class FASTQRead:
    """Single FASTQ read."""
    name: str
    sequence: str
    quality: str
    is_paired: bool = False
    read_number: int = 1

@dataclass
class QCReport:
    """Quality control report output."""
    total_reads: int
    passed_reads: int
    failed_reads: int
    mean_quality: float
    mean_q30: float
    gc_mean: float
    gc_std: float
    duplication_rate: float
    adapter_pct: float
    per_base_quality: List[Tuple[int, float]]  # (position, quality)
    per_base_gc: List[Tuple[int, float]]       # (position, gc_pct)

@dataclass
class AlignedRead:
    """Single aligned read."""
    query_name: str
    reference_name: str
    position: int
    mapping_quality: int
    cigar: str
    sequence: str
    quality: str
    is_reverse: bool
    is_duplicate: bool
    is_secondary: bool
    mate_reference_name: str
    mate_position: int
    insert_size: int

@dataclass
class Variant:
    """Single variant call."""
    chromosome: str
    position: int
    reference: str
    alternate: str
    quality: float
    filter_status: str
    genotype: str
    depth: int
    allele_frequency: float
    annotations: Dict[str, str] = field(default_factory=dict)

@dataclass
class StructuralVariant:
    """Structural variant call."""
    chromosome: str
    start: int
    end: int
    sv_type: str  # DEL, DUP, INV, BND
    size: int
    confidence: str  # HIGH, MEDIUM, LOW
    genotypes: Dict[str, str] = field(default_factory=dict)

@dataclass
class CoverageReport:
    """Coverage analysis results."""
    mean_depth: float
    median_depth: float
    min_depth: int
    max_depth: int
    on_target_rate: float
    uniformity: float
    target_size: int
    regions_below_20x: int
    regions_below_100x: int

@dataclass
class AnnotationSummary:
    """Variant annotation summary."""
    total: int
    missense: int
    synonymous: int
    nonsense: int
    frameshift: int
    splice_site: int
    intronic: int
    intergenic: int
    pathogenic: int
    likely_pathogenic: int
    uncertain: int
    benign: int

@dataclass
class PipelineRun:
    """Pipeline execution record."""
    run_id: str
    pipeline_name: str
    pipeline_version: str
    start_time: str
    end_time: str
    status: str  # running, completed, failed
    samples: List[str]
    parameters: Dict[str, str]
    output_files: Dict[str, str]
```

## Deployment Guide

### Local Installation

```bash
# Install from pip
pip install genomic-analysis[all]

# Install with specific extras
pip install genomic-analysis[gatk,bwa,vep]

# Install from source
git clone https://github.com/example/genomic-analysis.git
cd genomic-analysis
pip install -e ".[dev,test]"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    samtools \
    bwa \
    tabix \
    bgzip \
    && rm -rf /var/lib/apt/lists/*

# Install GATK
RUN wget -q https://github.com/broadinstitute/gatk/releases/download/4.6.1.0/gatk-4.6.1.0.zip \
    && unzip gatk-4.6.1.0.zip -d /opt/ \
    && ln -s /opt/gatk-4.6.1.0/gatk /usr/local/bin/gatk

# Install Python package
RUN pip install genomic-analysis[all]

# Default entrypoint
ENTRYPOINT ["genomic-pipeline"]
```

### Kubernetes Deployment

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ngs-pipeline-run
spec:
  template:
    spec:
      containers:
      - name: pipeline
        image: genomic-analysis:2.0.0
        command: ["genomic-pipeline", "run", "--config", "/config/pipeline.yaml"]
        resources:
          requests:
            memory: "32Gi"
            cpu: "8"
          limits:
            memory: "64Gi"
            cpu: "16"
        volumeMounts:
        - name: data-volume
          mountPath: /data
        - name: config-volume
          mountPath: /config
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: ngs-data-pvc
      - name: config-volume
        configMap:
          name: pipeline-config
      restartPolicy: Never
```

### Conda Environment

```yaml
# environment.yaml
name: genomic-analysis
channels:
  - bioconda
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - bwa-mem2=2.2.1
  - samtools=1.20
  - gatk4=4.6.1.0
  - fastqc=0.12.1
  - fastp=0.23.4
  - tabix=1.20
  - bgzip=1.20
  - ensembl-vep=112
  - pip:
    - genomic-analysis==2.0.0
```

## Monitoring and Observability

### Pipeline Metrics

```python
from genomic_analysis import PipelineMonitor

monitor = PipelineMonitor(
    metrics_backend="prometheus",
    push_gateway="http://prometheus:9091",
)

# Track key metrics
monitor.track("qc_pass_rate", report.passed_reads / report.total_reads)
monitor.track("alignment_rate", aligned_reads / total_reads)
monitor.track("on_target_rate", on_target / total_reads)
monitor.track("variant_count", len(variants))
monitor.track("pipeline_duration_seconds", elapsed)

# Alert on quality thresholds
monitor.set_alert(
    metric="qc_pass_rate",
    threshold=0.70,
    operator="lt",
    message="QC pass rate below 70% — check input quality",
)
```

### Log Management

```python
import logging
from genomic_analysis import StructuredLogger

logger = StructuredLogger(
    name="ngs_pipeline",
    level=logging.INFO,
    json_format=True,
    output="/var/log/ngs/pipeline.jsonl",
)

logger.info("Pipeline started", extra={
    "run_id": "run_2024_001",
    "sample_count": 24,
    "reference": "hg38",
    "pipeline_version": "3.2.1",
})

logger.warning("Low coverage detected", extra={
    "sample": "sample_015",
    "mean_depth": 18.5,
    "threshold": 20.0,
})
```

### Quality Dashboards

- Monitor per-sample QC metrics across all runs
- Track alignment rate trends over time
- Visualize variant call rate distributions
- Alert on pipeline failures and resource exhaustion
- Track tool version drift across pipeline runs
- Report on storage consumption and cleanup efficiency
- Monitor cluster utilization for batch scheduling

## Testing Strategy

### Unit Tests

```python
import pytest
from genomic_analysis import VariantCaller, Variant

def test_variant_caller_germline(tmp_path):
    caller = VariantCaller(reference="hg38.fa", mode="germline")
    vcf = caller.haplotype_caller(
        bam="test_data/sample.bam",
        intervals="test_data/test.bed",
        output=str(tmp_path / "test.vcf.gz"),
    )
    assert vcf.exists()

def test_variant_filtering():
    variants = [
        Variant("chr1", 100, "A", "G", 100.0, "PASS", "0/1", 30, 0.5),
        Variant("chr1", 200, "C", "T", 10.0, "LowQual", "0/1", 5, 0.2),
    ]
    filtered = [v for v in variants if v.filter_status == "PASS"]
    assert len(filtered) == 1

def test_qc_report_parsing():
    report = QCReport.from_fastqc("test_data/fastqc_report.zip")
    assert report.mean_q30 > 0
    assert report.total_reads > 0
```

### Integration Tests

```python
@pytest.mark.integration
def test_full_pipeline(tmp_path):
    """End-to-end test from FASTQ to annotated VCF."""
    runner = PipelineRunner(config="test_pipeline.yaml")
    result = runner.execute(
        samples="test_data/samples_small.csv",
        output_dir=str(tmp_path),
    )
    assert result.status == "completed"
    assert (tmp_path / "annotated.vcf.gz").exists()
    assert (tmp_path / "qc_report.html").exists()

@pytest.mark.integration
def test_reference_indexing():
    ref = ReferenceManager(cache_dir="/tmp/test_refs")
    ref.add("test_ref", fasta="test_data/test_ref.fa")
    ref.index("test_ref")
    assert ref.is_indexed("test_ref")
```

### Performance Tests

```python
@pytest.mark.benchmark
def test_alignment_throughput(benchmark):
    aligner = ReadAligner(reference="hg38.fa", threads=16)
    result = benchmark(
        aligner.align,
        r1="test_data/1M_reads_R1.fq.gz",
        r2="test_data/1M_reads_R2.fq.gz",
        output="/tmp/bench.bam",
    )
    # Expect > 1M reads/minute alignment rate
    assert result.throughput_rpm > 1_000_000
```

## Versioning and Migration

### Semantic Versioning

- **Major** (X.0.0): Breaking changes to output formats, API signatures, or required tool versions
- **Minor** (0.X.0): New tools, new annotation sources, backward-compatible features
- **Patch** (0.0.X): Bug fixes, performance improvements, documentation updates

### Migration Guide (v1.x → v2.0)

```python
# v1.x (deprecated)
from genomic_analysis.v1 import Pipeline
pipeline = Pipeline(config="old_config.yaml")

# v2.0 (current)
from genomic_analysis import PipelineRunner
runner = PipelineRunner(config="new_config.yaml")
# Config schema changed: 'reference_genome' → 'reference'
# Config schema changed: 'call_variants' → 'variant_calling'
# VCF output now defaults to compressed format
```

### Tool Version Compatibility Matrix

| genomic-analysis | GATK  | BWA-MEM2 | samtools | VEP |
|-----------------|-------|----------|----------|-----|
| 2.0.x           | 4.6.x | 2.2.x   | 1.20+    | 112+|
| 1.5.x           | 4.5.x | 2.2.x   | 1.18+    | 110+|
| 1.0.x           | 4.2.x | 2.1.x   | 1.15+    | 105+|

## Glossary

| Term | Definition |
|------|-----------|
| **BAM** | Binary Alignment/Map — compressed binary form of SAM alignment data |
| **BQSR** | Base Quality Score Recalibration — corrects systematic errors in base quality scores |
| **CRAM** | Compressed Reference-oriented Alignment Map — more compressed than BAM, reference-dependent |
| **GVCF** | Genome VCF — includes confidence bands for non-variant sites, enabling joint calling |
| **HaplotypeCaller** | GATK tool that performs local reassembly and variant calling simultaneously |
| **Mutect2** | GATK somatic variant caller using Bayesian statistics and panel of normals |
| **VCF** | Variant Call Format — standard text format for storing gene sequence variations |
| **VQSR** | Variant Quality Score Recalibration — machine learning–based variant quality filtering |
| **MAF** | Minor Allele Frequency — frequency of the less common allele in a population |
| **pLDDT** | Predicted Local Distance Difference Test — AlphaFold per-residue confidence score |
| **CADD** | Combined Annotation Dependent Depletion — variant deleteriousness prediction |
| **SpliceAI** | Deep learning model for predicting splice-altering variants |
| **PAS** | Premature Termination Codon — variant introducing a stop codon in coding sequence |
| **SNV** | Single Nucleotide Variant — single base pair change |
| **Indel** | Insertion/Deletion — small insertion or deletion (typically 1-50 bp) |
| **SV** | Structural Variant — large genomic rearrangement (>50 bp) |

## Changelog

### v2.0.0 (2024-06-15)
- Added Mutect2 somatic calling pipeline
- Added VQSR support for cohorts ≥ 30 samples
- Added DeepVariant integration as alternative caller
- Added StructuredLogger and PipelineMonitor
- Added cloud storage integration (S3, GCS)
- Migrated to GATK 4.6.x

### v1.5.0 (2024-01-10)
- Added SpliceAI plugin for variant annotation
- Added alpha-missense annotation support
- Improved SV detection with GRIDSS integration
- Added Kubernetes deployment manifests

### v1.0.0 (2023-09-01)
- Initial release with QC, alignment, germline calling
- VEP and ANNOVAR annotation support
- HTML report generation
- Docker container support

## Contributing Guidelines

1. Fork the repository and create a feature branch from `main`
2. Write tests for all new functionality
3. Ensure all tests pass: `pytest tests/ -v --cov=genomic_analysis`
4. Update documentation for any API changes
5. Follow PEP 8 style guidelines
6. Add changelog entries for user-facing changes
7. Submit a pull request with a clear description of changes
8. Request review from at least one maintainer before merging

### Development Setup

```bash
git clone https://github.com/example/genomic-analysis.git
cd genomic-analysis
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Genomic Analysis Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
