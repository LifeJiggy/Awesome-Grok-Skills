# Research Agent Architecture

## Overview

The Research Agent provides a comprehensive framework for conducting academic and industry research, including literature review, experiment design, statistical analysis, and academic writing. It follows established research methodologies and supports multiple citation styles.

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       Research Agent (Orchestrator)                       │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Research    │  │  Literature  │  │  Experiment  │  │ Statistical │  │
│  │  Indexer     │  │  Analyzer    │  │  Designer    │  │  Analyzer   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
│         │                 │                 │                │          │
│         ▼                 ▼                 ▼                ▼          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Research Synthesizer                         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│  │  │   Citation   │  │  Knowledge   │  │  Academic Writer     │  │   │
│  │  │   Manager    │  │    Graph     │  │                      │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Output Layer                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│  │  │   Research   │  │   Academic   │  │   Knowledge          │  │   │
│  │  │   Reports    │  │   Papers     │  │   Graphs             │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
                          ┌─────────────────┐
                          │ Research Question│
                          │  Formulation     │
                          └────────┬────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │   Phase 1: Literature Review  │
                    │  ┌────────┐  ┌────────────┐  │
                    │  │ Source  │  │  Indexing  │  │
                    │  │ Search  │  │ & Search   │  │
                    │  └───┬────┘  └─────┬──────┘  │
                    │      │             │          │
                    │      └──────┬──────┘          │
                    │             │                  │
                    │             ▼                  │
                    │  ┌────────────────────┐       │
                    │  │  Thematic Analysis │       │
                    │  └─────────┬──────────┘       │
                    └────────────┼──────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────────┐
                    │    Phase 2: Methodology       │
                    │  ┌──────────────────────┐    │
                    │  │  Hypothesis           │    │
                    │  │  Formulation          │    │
                    │  └─────────┬────────────┘    │
                    │            │                  │
                    │            ▼                  │
                    │  ┌──────────────────────┐    │
                    │  │  Experiment Design    │    │
                    │  │  & Sample Size Calc   │    │
                    │  └─────────┬────────────┘    │
                    └────────────┼──────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────────┐
                    │   Phase 3: Data Analysis      │
                    │  ┌──────┐ ┌──────┐ ┌──────┐  │
                    │  │Desc. │ │Infer-│ │Effect│  │
                    │  │Stats │ │ential│ │Size  │  │
                    │  └──┬───┘ └──┬───┘ └──┬───┘  │
                    │     │        │        │       │
                    │     └────────┼────────┘       │
                    │              │                 │
                    │              ▼                 │
                    │  ┌──────────────────────┐    │
                    │  │  Synthesis &          │    │
                    │  │  Interpretation       │    │
                    │  └──────────────────────┘    │
                    └──────────────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────────┐
                    │      Phase 4: Writing         │
                    │  ┌──────────────────────────┐ │
                    │  │  Paper/Report Generation  │ │
                    │  │  Citation Formatting      │ │
                    │  │  Knowledge Graph Update   │ │
                    │  └──────────────────────────┘ │
                    └──────────────────────────────┘
```

## Component Details

### 1. Research Indexer

```
┌─────────────────────────────────────────────────┐
│           Research Indexer                       │
├─────────────────────────────────────────────────┤
│                                                  │
│  Indexing Strategies                            │
│  ├── Keyword Index (full-text)                  │
│  ├── Author Index                               │
│  ├── Year Index                                 │
│  ├── Source Type Index                          │
│  ├── Citation Network                           │
│  └── DOI/ISBN Lookup                            │
│                                                  │
│  Search Capabilities                            │
│  ├── Keyword Search (TF-IDF scoring)           │
│  ├── Author Search                              │
│  ├── Year Range Search                          │
│  ├── Source Type Filter                         │
│  ├── Relevance Ranking                          │
│  └── Combined Queries                           │
│                                                  │
│  Source Types Supported                          │
│  ├── Academic (Journal, Conference, Thesis)     │
│  ├── Industry (White Paper, Tech Report)        │
│  ├── Government                                 │
│  ├── Preprints                                  │
│  ├── Patents                                    │
│  └── Datasets                                   │
└─────────────────────────────────────────────────┘
```

**Indexing Structure:**

```python
# Multi-level index
index = {
    "keyword_token": [source_id_1, source_id_2, ...],
    ...
}
author_index = {
    "author_name": {source_id_1, source_id_2, ...},
    ...
}
year_index = {
    2024: {source_id_1, source_id_2, ...},
    ...
}
```

### 2. Literature Analyzer

```
┌─────────────────────────────────────────────────┐
│         Literature Analyzer                      │
├─────────────────────────────────────────────────┤
│                                                  │
│  Theme Extraction                               │
│  ├── Keyword-based classification               │
│  ├── Topic modeling (LDA-ready)                 │
│  ├── Concept clustering                         │
│  └── Cross-cutting theme identification         │
│                                                  │
│  Trend Analysis                                 │
│  ├── Publication timeline                       │
│  ├── Citation trends                            │
│  ├── Methodology evolution                      │
│  └── Geographic distribution                    │
│                                                  │
│  Gap Analysis                                   │
│  ├── Coverage gaps (sub-questions)              │
│  ├── Methodology gaps                           │
│  ├── Temporal gaps                              │
│  └── Population gaps                            │
│                                                  │
│  Contradiction Detection                        │
│  ├── Text similarity analysis                   │
│  ├── Finding comparison                         │
│  ├── Evidence strength comparison               │
│  └── Resolution suggestions                     │
└─────────────────────────────────────────────────┘
```

### 3. Experiment Designer

```
┌─────────────────────────────────────────────────┐
│         Experiment Designer                      │
├─────────────────────────────────────────────────┤
│                                                  │
│  Hypothesis Management                          │
│  ├── Null hypothesis formulation                │
│  ├── Alternative hypothesis formulation         │
│  ├── Directional hypotheses                     │
│  └── Variable operationalization                │
│                                                  │
│  Methodology Selection                          │
│  ├── Quantitative (experiments, surveys)        │
│  ├── Qualitative (case studies, ethnography)    │
│  ├── Mixed Methods                              │
│  ├── Meta-analysis                              │
│  └── Systematic Review                          │
│                                                  │
│  Sample Size Calculation                        │
│  ├── Power analysis                             │
│  ├── Effect size estimation                     │
│  ├── Alpha/beta parameters                      │
│  └── Attrition adjustment                       │
│                                                  │
│  Assumption Checking                            │
│  ├── Normality (Shapiro-Wilk ready)            │
│  ├── Homogeneity of variance                    │
│  ├── Independence                               │
│  └── Linearity                                  │
└─────────────────────────────────────────────────┘
```

### 4. Statistical Analyzer

```
┌─────────────────────────────────────────────────┐
│         Statistical Analyzer                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  Descriptive Statistics                         │
│  ├── Central tendency (mean, median, mode)      │
│  ├── Dispersion (SD, variance, IQR, range)     │
│  ├── Distribution shape (skewness, kurtosis)    │
│  └── Percentiles                                │
│                                                  │
│  Inferential Statistics                         │
│  ├── t-tests (independent, paired)             │
│  ├── ANOVA (one-way, factorial)                │
│  ├── Chi-square tests                           │
│  ├── Correlation (Pearson, Spearman)            │
│  ├── Regression (linear, logistic)              │
│  ├── Non-parametric (Mann-Whitney, Kruskal-Wall)│
│  └── Bayesian methods (MCMC-ready)             │
│                                                  │
│  Effect Size Measures                           │
│  ├── Cohen's d                                  │
│  ├── Eta-squared                                │
│  ├── Odds ratio                                 │
│  └── Confidence intervals                       │
│                                                  │
│  Assumption Validation                          │
│  ├── Normality tests                            │
│  ├── Homoscedasticity                           │
│  ├── Multicollinearity                          │
│  └── Outlier detection                          │
└─────────────────────────────────────────────────┘
```

### 5. Research Synthesizer

```
┌─────────────────────────────────────────────────┐
│         Research Synthesizer                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  Evidence Hierarchy                             │
│  ├── Strong (meta-analysis, RCTs)              │
│  ├── Moderate (cohort, case-control)            │
│  ├── Weak (cross-sectional, case reports)       │
│  ├── Anecdotal                                  │
│  ├── Conflicting                                │
│  └── Insufficient                               │
│                                                  │
│  Synthesis Methods                              │
│  ├── Narrative synthesis                        │
│  ├── Thematic synthesis                         │
│  ├── Framework synthesis                        │
│  ├── Meta-ethnography                           │
│  └── Vote counting                              │
│                                                  │
│  Output Generation                              │
│  ├── Answer summaries per research question     │
│  ├── Confidence levels                          │
│  ├── Evidence gaps                              │
│  ├── Key findings extraction                    │
│  └── Contradiction identification               │
└─────────────────────────────────────────────────┘
```

### 6. Citation Manager

```
┌─────────────────────────────────────────────────┐
│         Citation Manager                         │
├─────────────────────────────────────────────────┤
│                                                  │
│  Supported Styles                               │
│  ├── APA (7th edition)                          │
│  ├── MLA (9th edition)                          │
│  ├── Chicago (17th edition)                     │
│  ├── IEEE                                        │
│  ├── Harvard                                     │
│  ├── Vancouver                                   │
│  ├── ACS                                         │
│  ├── AMA                                         │
│  └── Turabian                                    │
│                                                  │
│  Citation Types                                 │
│  ├── In-text citations                          │
│  ├── Bibliography/Reference list                │
│  ├── Footnotes                                   │
│  └── Endnotes                                    │
│                                                  │
│  Source Types Handled                            │
│  ├── Journal articles                           │
│  ├── Conference papers                          │
│  ├── Books and book chapters                    │
│  ├── Theses/Dissertations                       │
│  ├── Websites and online sources                │
│  ├── Government documents                       │
│  └── Patents                                     │
└─────────────────────────────────────────────────┘
```

### 7. Knowledge Graph

```
┌─────────────────────────────────────────────────┐
│         Knowledge Graph                          │
├─────────────────────────────────────────────────┤
│                                                  │
│  Node Types                                     │
│  ├── Concepts                                   │
│  ├── Entities                                   │
│  ├── Findings                                   │
│  ├── Methodologies                              │
│  ├── Theories                                   │
│  └── Variables                                  │
│                                                  │
│  Edge Types (Relationships)                     │
│  ├── supports                                   │
│  ├── contradicts                                │
│  ├── extends                                    │
│  ├── uses                                       │
│  ├── part_of                                    │
│  ├── causes                                     │
│  └── correlates_with                            │
│                                                  │
│  Query Operations                               │
│  ├── Path finding (DFS/BFS)                    │
│  ├── Subgraph extraction                        │
│  ├── Connected components                       │
│  ├── Centrality analysis                        │
│  └── Cluster detection                          │
└─────────────────────────────────────────────────┘
```

### 8. Academic Writer

```
┌─────────────────────────────────────────────────┐
│         Academic Writer                          │
├─────────────────────────────────────────────────┤
│                                                  │
│  Paper Sections                                 │
│  ├── Abstract                                   │
│  ├── Introduction                               │
│  ├── Literature Review                          │
│  ├── Methodology                                │
│  ├── Results                                    │
│  ├── Discussion                                 │
│  ├── Conclusion                                 │
│  └── References                                 │
│                                                  │
│  Writing Formats                                │
│  ├── APA Paper Format                          │
│  ├── IEEE Paper Format                         │
│  ├── LaTeX                                      │
│  ├── Markdown                                   │
│  └── HTML                                       │
│                                                  │
│  Output Types                                   │
│  ├── Research Papers                            │
│  ├── Literature Reviews                         │
│  ├── Technical Reports                          │
│  ├── Executive Summaries                        │
│  └── Conference Abstracts                       │
└─────────────────────────────────────────────────┘
```

## Design Patterns

### 1. Facade Pattern
The `ResearchAgent` class provides a simplified interface to the complex subsystem:

```python
# Simple interface through the facade
agent = ResearchAgent()
review = agent.literature_review("AI safety")
paper = agent.write_paper("Title", ["Author"])
```

### 2. Strategy Pattern
Statistical analysis uses strategy pattern for interchangeable tests:

```python
result = analyzer.analyze(group1, group2, StatisticalTest.T_TEST)
result = analyzer.analyze(group1, group2, StatisticalTest.CORRELATION)
```

### 3. Builder Pattern
Academic papers are built incrementally:

```python
paper = agent.write_paper("Title", ["Author"])
paper.introduction = agent.academic_writer.write_introduction(...)
paper.methodology = agent.academic_writer.write_methodology(...)
paper.results = agent.academic_writer.write_results(...)
```

### 4. Observer Pattern
Knowledge graph notifies when new connections are discovered.

### 5. Composite Pattern
Research findings can be composed into themes, then into narratives.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Type System | Dataclasses + Enums |
| Statistics | Built-in `statistics` module |
| Text Processing | String operations (regex-ready) |
| Graph Operations | Custom BFS/DFS implementation |
| Date/Time | `datetime` module |
| Unique IDs | `uuid4` |
| Logging | Python `logging` module |
| Serialization | JSON-compatible structures |

## Data Models

### Source

```python
@dataclass
class Source:
    id: str                    # Unique identifier
    title: str                 # Source title
    authors: List[str]         # Author names
    source_type: SourceType    # Type of source
    url: str                   # URL or DOI link
    publication_date: datetime # When published
    abstract: str              # Abstract/summary
    keywords: List[str]        # Indexing keywords
    citations: int             # Citation count
    relevance_score: float     # Search relevance
    doi: Optional[str]         # Digital Object Identifier
    journal: Optional[str]     # Journal name
    peer_reviewed: bool        # Peer review status
```

### ResearchFinding

```python
@dataclass
class ResearchFinding:
    source_id: str                    # Source reference
    finding: str                      # Finding description
    evidence_strength: EvidenceStrength  # Evidence level
    page_number: Optional[int]        # Page reference
    quote: Optional[str]              # Direct quote
    themes: List[str]                 # Associated themes
    methodology_used: MethodologyType  # Research method
    sample_size: Optional[int]        # Study sample size
```

### Experiment

```python
@dataclass
class Experiment:
    id: str                           # Experiment ID
    title: str                        # Experiment title
    hypothesis_id: str                # Linked hypothesis
    methodology: MethodologyType      # Research method
    variables: Dict[str, List[str]]   # IV/DV definitions
    sample_size: int                  # Planned sample
    control_group: bool               # Has control
    randomization: bool               # Random assignment
    alpha: float                      # Significance level
    power_analysis: float             # Statistical power
```

## Security Considerations

### Data Integrity
- Source metadata validated on ingestion
- Citation counts tracked for accuracy
- Version control for research documents

### Intellectual Property
- Proper attribution for all sources
- Citation style compliance
- Plagiarism prevention via proper referencing

### Privacy
- No PII stored in research indices
- Anonymous data handling for surveys
- IRB compliance tracking for experiments

## Scalability

### Horizontal Scaling
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Indexer 1   │  │  Indexer 2   │  │  Indexer N   │
│  (Partition A)│  │ (Partition B)│  │ (Partition N)│
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────────────────────────────────────────┐
│              Query Aggregation Layer             │
└─────────────────────────────────────────────────┘
```

### Vertical Scaling
- Each component has independent state
- Analysis results cached for reuse
- Knowledge graph supports incremental updates

## Performance Characteristics

| Metric | Target |
|--------|--------|
| Source indexing | < 100ms per source |
| Search query | < 200ms |
| Theme extraction | < 500ms per 100 sources |
| Statistical analysis | < 1s per test |
| Citation formatting | < 50ms per citation |
| Paper generation | < 5s |

## Error Handling

```
┌─────────────────────────────────────────┐
│           Error Handling Flow            │
├─────────────────────────────────────────┤
│                                          │
│  Source Ingestion                        │
│  ├── Missing required fields → skip      │
│  ├── Duplicate source → update           │
│  └── Invalid format → log and continue   │
│                                          │
│  Search Operations                       │
│  ├── No results → return empty list      │
│  ├── Index corruption → rebuild          │
│  └── Query too broad → apply filters     │
│                                          │
│  Statistical Analysis                    │
│  ├── Insufficient data → report N/A      │
│  ├── Assumption violation → use non-param│
│  └── Division by zero → return 0         │
│                                          │
│  Citation Formatting                     │
│  ├── Missing fields → use placeholders   │
│  ├── Invalid style → fallback to APA     │
│  └── Special characters → escape         │
│                                          │
│  Paper Generation                        │
│  ├── Missing sections → generate stubs   │
│  ├── Word limit exceeded → truncate      │
│  └── Citation overflow → inline refs     │
└─────────────────────────────────────────┘

## Configuration

```yaml
research_agent:
  indexer:
    max_sources: 10000
    index_rebuild_interval: 3600  # seconds
    min_relevance_score: 0.1
    
  analyzer:
    theme_keywords: 50
    contradiction_threshold: 0.4
    gap_detection_depth: 3
    
  experiment:
    default_alpha: 0.05
    default_power: 0.80
    min_sample_size: 30
    max_sample_size: 10000
    
  statistics:
    significance_level: 0.05
    effect_size_threshold: 0.2
    confidence_level: 0.95
    
  citations:
    default_style: "apa"
    max_authors_display: 6
    et_al_threshold: 3
    
  writing:
    default_format: "markdown"
    abstract_word_limit: 300
    section_headers: true
```

## Extension Points

### Custom Source Types
```python
class CustomSourceType(Enum):
    PODCAST = "podcast"
    VIDEO_SERIES = "video_series"

# Extend indexer to handle new types
indexer.type_index[CustomSourceType.PODCAST] = set()
```

### Custom Statistical Tests
```python
class StatisticalAnalyzer:
    def custom_test(self, data1, data2):
        # Custom analysis logic
        return AnalysisResult(...)

    # Register in analyze dispatch
    analyze_dispatch[StatisticalTest.CUSTOM] = self.custom_test
```

### Custom Citation Styles
```python
class CitationManager:
    def _format_custom(self, source, num):
        return f"Custom format: {source.title}"

    # Register formatter
    style_formatters[CitationStyle.CUSTOM] = self._format_custom
```

### Custom Knowledge Graph Relationships
```python
# Add new relationship types
graph.add_edge(node1.id, node2.id, "novel_connection", weight=0.8)
```
