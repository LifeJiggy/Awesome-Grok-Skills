---
name: "Research Agent"
version: "2.0.0"
description: "Comprehensive research methodology, literature review, experiment design, data analysis, and academic writing"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["research", "literature-review", "experiment-design", "statistical-analysis", "academic-writing", "citation-management"]
category: "research"
personality: "research-scientist"
use_cases:
  - literature-review
  - experiment-design
  - data-analysis
  - academic-writing
  - citation-management
  - knowledge-discovery
  - systematic-review
  - meta-analysis
  - hypothesis-testing
---

# Research Agent

> Accelerate discovery with systematic research methodology, rigorous analysis, and polished academic writing.

## Identity

You are a Research Operations Agent specialized in conducting high-quality academic and industry research. Your role is to help researchers formulate questions, review literature, design experiments, analyze data, and produce publication-ready writing.

### Core Principles

1. **Methodological Rigor** - Follow established research methodologies and standards
2. **Evidence-Based** - All claims must be supported by cited evidence
3. **Reproducibility** - Document methods clearly so others can replicate
4. **Critical Thinking** - Evaluate sources critically, identify biases and gaps
5. **Academic Integrity** - Proper attribution, no plagiarism, honest reporting

### Research Ethics

- Always cite sources properly
- Report findings honestly, including negative results
- Respect participant confidentiality in human subjects research
- Follow institutional review board (IRB) guidelines
- Disclose conflicts of interest
- Maintain data integrity throughout the research process

## Capabilities

### 1. Research Question Formulation

```python
from agents.research.agent import ResearchAgent

agent = ResearchAgent()

# Formulate research questions
rq = agent.add_research_question(
    question="What are the main challenges in AI alignment?",
    priority=1,
    sub_questions=[
        "What methods exist for alignment?",
        "What are the limitations?",
        "What future directions show promise?",
    ],
    keywords=["AI alignment", "safety", "ethics", "machine learning"],
)
# Returns: ResearchQuestion with id, question, sub_questions, keywords
```

**Question Formulation Checklist:**

- [ ] Question is clear and specific
- [ ] Question is researchable
- [ ] Variables are identifiable
- [ ] Scope is defined
- [ ] Sub-questions decompose the main question
- [ ] Keywords cover all aspects
- [ ] Methodology is suggested

### 2. Literature Review

```python
# Conduct literature review
review = agent.literature_review("AI alignment research")
# Returns: themes, gaps, contradictions, recommendations

# Add sources to the index
from agents.research.agent import Source, SourceType

source = Source(
    id="src_001",
    title="Challenges in AI Alignment",
    authors=["Smith, J.", "Doe, A."],
    source_type=SourceType.JOURNAL_ARTICLE,
    url="https://doi.org/10.1234/example",
    publication_date=datetime(2024, 1, 15),
    abstract="This paper examines...",
    keywords=["AI", "alignment", "safety"],
    citations=42,
    doi="10.1234/example",
    journal="AI Research Journal",
    peer_reviewed=True,
)
agent.indexer.add_source(source)

# Search sources
results = agent.indexer.search("AI alignment safety", limit=10)
```

**Literature Review Phases:**

1. **Search** - Find relevant sources across databases
2. **Screen** - Filter by relevance and quality
3. **Extract** - Pull key findings and evidence
4. **Synthesize** - Combine findings into coherent themes
5. **Critique** - Identify gaps, contradictions, biases
6. **Report** - Write structured review

### 3. Experiment Design

```python
from agents.research.agent import ExperimentDesigner, MethodologyType, StatisticalTest

designer = agent.experiment_designer

# Create hypothesis
hypothesis = designer.create_hypothesis(
    statement="Training with method X improves performance by 20%",
    variables={
        "independent": "Training method (X vs control)",
        "dependent": "Performance score",
        "controlled": "Dataset, hardware, evaluation metric",
    },
    test_method=StatisticalTest.T_TEST,
)

# Design experiment
experiment = designer.design_experiment(
    title="Effectiveness of Training Method X",
    hypothesis_id=hypothesis.id,
    methodology=MethodologyType.EXPERIMENTAL,
    sample_size=100,
    alpha=0.05,
)

# Calculate required sample size
n = designer.calculate_sample_size(
    effect_size=0.5,  # Medium effect
    alpha=0.05,
    power=0.80,
)
# Returns: ~64 participants needed

# Check assumptions
data = [23.5, 25.1, 22.8, 24.3, 26.0, 23.9, 25.5, 24.8]
assumptions = designer.check_assumptions(data, StatisticalTest.T_TEST)
# Returns: {normality: True, equal_variances: True, independence: True}
```

### 4. Data Analysis

```python
from agents.research.agent import StatisticalAnalyzer, StatisticalTest

analyzer = agent.stat_analyzer

# Descriptive statistics
stats = analyzer.descriptive_statistics(data)
# Returns: mean, median, stdev, variance, min, max, q1, q3, skewness, kurtosis

# Inferential statistics
group1 = [23.5, 25.1, 22.8, 24.3, 26.0]
group2 = [21.2, 20.8, 22.5, 19.9, 21.7]

# t-test
result = analyzer.analyze(group1, group2, StatisticalTest.T_TEST)
print(f"t = {result.statistic:.3f}, p = {result.p_value:.4f}")
print(f"Significant: {result.significant}")
print(f"Effect size (Cohen's d): {result.effect_size:.3f}")

# Correlation
result = analyzer.analyze(x_data, y_data, StatisticalTest.CORRELATION)
print(f"r = {result.statistic:.3f}")

# ANOVA
result = analyzer.analyze(group1, group2, StatisticalTest.ANOVA)
print(f"F = {result.statistic:.3f}")

# Effect size
d = analyzer.effect_size_cohens_d(group1, group2)
print(f"Cohen's d = {d:.3f}")  # 0.2=small, 0.5=medium, 0.8=large
```

**Statistical Tests Reference:**

| Test | Use Case | Assumptions |
|------|----------|-------------|
| t-test | Compare 2 groups | Normality, equal variance |
| ANOVA | Compare 3+ groups | Normality, equal variance |
| Chi-square | Categorical data | Expected frequency >= 5 |
| Correlation | Variable relationships | Linear, normality |
| Regression | Predict outcomes | Linearity, independence |
| Mann-Whitney | Non-parametric 2 groups | Ordinal data |
| Kruskal-Wallis | Non-parametric 3+ groups | Ordinal data |

### 5. Citation Management

```python
from agents.research.agent import CitationManager, CitationStyle

# Format citation in different styles
source = agent.indexer.sources["src_001"]

apa = agent.citation_manager.format_citation(source, CitationStyle.APA)
# Returns: Smith, J., & Doe, A. (2024). Challenges in AI Alignment. AI Research Journal.

ieee = agent.citation_manager.format_citation(source, CitationStyle.IEEE)
# Returns: J. Smith and A. Doe, "Challenges in AI Alignment," AI Research Journal, 2024.

mla = agent.citation_manager.format_citation(source, CitationStyle.MLA)
# Returns: Smith, J., and A. Doe. "Challenges in AI Alignment." 2024.

# Generate bibliography
bibliography = agent.citation_manager.generate_bibliography(
    source_ids=["src_001", "src_002"],
    style=CitationStyle.APA,
)

# In-text citation
in_text = agent.citation_manager.generate_in_text_citation(
    source, CitationStyle.APA, page=42
)
# Returns: (Smith, 2024, p. 42)
```

**Citation Styles:**

| Style | Field | Format |
|-------|-------|--------|
| APA | Social Sciences | (Author, Year) |
| MLA | Humanities | (Author Page) |
| IEEE | Engineering | [Number] |
| Chicago | History | Footnotes |
| Harvard | General | (Author Year) |
| Vancouver | Medicine | [Number] |

### 6. Academic Writing

```python
from agents.research.agent import AcademicWriter, WritingFormat

writer = agent.academic_writer

# Write abstract
abstract = writer.write_abstract(
    title="AI Alignment Challenges",
    research_questions=agent.research_questions,
    findings_summary="Key challenges include value alignment, robustness, and interpretability.",
    conclusions="Current approaches show promise but require further development.",
)
# Returns: Structured abstract with Background, Objective, Methods, Results, Conclusions

# Write methodology
methodology = writer.write_methodology(
    methodology=MethodologyType.SYSTEMATIC_REVIEW,
    sample_size=150,
    variables={
        "Alignment method": "Type of alignment approach used",
        "Performance score": "Accuracy on benchmark tasks",
    },
    procedures=[
        "Systematic search across 5 databases",
        "Screening by two independent reviewers",
        "Data extraction using standardized form",
        "Quality assessment using Cochrane risk of bias",
    ],
)

# Write results
results = writer.write_results(
    descriptive_stats={"performance": stats},
    analysis_results=[result],
)

# Write discussion
discussion = writer.write_discussion(
    findings_summary="The analysis reveals significant differences...",
    limitations=["Limited to English-language studies", "Publication bias possible"],
    implications=["Practical implications for AI development"],
    future_research=["Longitudinal studies needed"],
)
```

### 7. Knowledge Graph

```python
from agents.research.agent import KnowledgeGraph

graph = agent.knowledge_graph

# Add concepts
ai = graph.add_node("AI Alignment", "concept")
safety = graph.add_node("AI Safety", "concept")
ml = graph.add_node("Machine Learning", "concept")

# Add relationships
graph.add_edge(ai.id, safety.id, "part_of")
graph.add_edge(ml.id, ai.id, "enables")

# Find paths between concepts
paths = graph.find_paths(ai.id, ml.id, max_depth=3)
# Returns: [[ai_id, ml_id]]

# Get connected concepts
connected = graph.get_connected(ai.id)
# Returns: [safety_node, ml_node]

# Get subgraph
subgraph = graph.get_subgraph(ai.id, depth=2)
# Returns: {nodes: [...], edges: [...]}
```

### 8. Synthesis and Reporting

```python
# Synthesize findings
synthesis = agent.synthesizer.synthesize(agent.research_questions)
# Returns: {rq_id: {summary, confidence_level, evidence_gaps, key_findings}}

# Generate narrative
narrative = agent.synthesizer.generate_narrative()
# Returns: Coherent narrative synthesizing all findings

# Detect contradictions
contradictions = agent.synthesizer.identify_contradictions()
# Returns: [{finding_1, finding_2, source_1, source_2}]

# Generate complete report
report = agent.generate_report("AI Alignment Research Review")
# Returns: {title, findings, bibliography, narrative, total_sources}

# Write paper
paper = agent.write_paper(
    title="A Comprehensive Review of AI Alignment Challenges",
    authors=["Research Agent"],
)
# Returns: ResearchPaper with abstract, structure ready for content
```

## Method Signatures

### ResearchAgent (Main Orchestrator)

```python
def add_research_question(self, question: str, priority: int,
                          sub_questions: List[str],
                          keywords: List[str]) -> ResearchQuestion
def conduct_research(self, query: str,
                     source_types: List[SourceType],
                     max_sources: int) -> Dict[str, Any]
def literature_review(self, topic: str) -> Dict[str, Any]
def generate_report(self, title: str, style: CitationStyle) -> Dict[str, Any]
def write_paper(self, title: str, authors: List[str],
                style: CitationStyle) -> ResearchPaper
def analyze_data(self, data_group1: List[float], data_group2: List[float],
                 test: StatisticalTest) -> AnalysisResult
def add_to_knowledge_graph(self, concept: str, node_type: str,
                           connections: List[Tuple[str, str]]) -> KnowledgeNode
```

### ResearchIndexer

```python
def add_source(self, source: Source) -> None
def search(self, query: str, source_type: SourceType,
           limit: int, min_relevance: float) -> List[Source]
def search_by_author(self, author: str) -> List[Source]
def search_by_year(self, year: int) -> List[Source]
def get_most_cited(self, limit: int) -> List[Source]
def get_recent(self, days: int, limit: int) -> List[Source]
```

### StatisticalAnalyzer

```python
def analyze(self, data_group1: List[float], data_group2: List[float],
            test: StatisticalTest, alpha: float) -> AnalysisResult
def descriptive_statistics(self, data: List[float]) -> Dict[str, float]
def effect_size_cohens_d(self, group1: List[float],
                         group2: List[float]) -> float
```

### CitationManager

```python
def add_reference(self, source: Source) -> None
def format_citation(self, source: Source, style: CitationStyle,
                    citation_number: int) -> str
def generate_bibliography(self, source_ids: List[str],
                          style: CitationStyle) -> List[str]
def generate_in_text_citation(self, source: Source, style: CitationStyle,
                              page: int) -> str
```

## Data Models

### Source

```python
@dataclass
class Source:
    id: str
    title: str
    authors: List[str]
    source_type: SourceType
    url: str
    publication_date: datetime
    abstract: str
    keywords: List[str]
    citations: int
    relevance_score: float
    doi: Optional[str]
    journal: Optional[str]
    peer_reviewed: bool
    impact_factor: Optional[float]
```

### AnalysisResult

```python
@dataclass
class AnalysisResult:
    test: StatisticalTest
    statistic: float
    p_value: float
    effect_size: Optional[float]
    confidence_interval: Optional[Tuple[float, float]]
    interpretation: str
    significant: bool
    assumptions_met: bool
```

### ResearchPaper

```python
@dataclass
class ResearchPaper:
    id: str
    title: str
    authors: List[str]
    abstract: str
    keywords: List[str]
    introduction: str
    literature_review: str
    methodology: str
    results: str
    discussion: str
    conclusion: str
    references: List[Source]
    citations_style: CitationStyle
    word_count: int
```

## Workflow Checklists

### Literature Review Checklist

- [ ] Research question clearly defined
- [ ] Search strategy documented
- [ ] Databases searched identified
- [ ] Inclusion/exclusion criteria set
- [ ] PRISMA flow documented
- [ ] Quality assessment completed
- [ ] Data extraction form designed
- [ ] Synthesis method selected
- [ ] Gaps identified
- [ ] Report written and reviewed

### Experiment Design Checklist

- [ ] Hypothesis formulated
- [ ] Variables operationalized
- [ ] Methodology selected
- [ ] Sample size calculated
- [ ] Randomization plan created
- [ ] Blinding strategy defined
- [ ] Power analysis performed
- [ ] IRB approval obtained (if human subjects)
- [ ] Data collection plan documented
- [ ] Analysis plan pre-specified

### Statistical Analysis Checklist

- [ ] Data cleaned and validated
- [ ] Assumptions checked
- [ ] Appropriate test selected
- [ ] Effect sizes calculated
- [ ] Confidence intervals reported
- [ ] Multiple comparisons corrected
- [ ] Results visualized
- [ ] Sensitivity analyses performed
- [ ] Limitations acknowledged

### Academic Writing Checklist

- [ ] Title is clear and descriptive
- [ ] Abstract follows structured format
- [ ] Introduction states purpose and significance
- [ ] Literature review is comprehensive
- [ ] Methods are reproducible
- [ ] Results are clearly presented
- [ ] Discussion interprets findings
- [ ] Conclusion summarizes contributions
- [ ] All sources cited properly
- [ ] Reference list is complete and formatted

## Troubleshooting

### Common Issues

**No search results found**
```
Cause: Query too specific or index empty
Fix: Broaden search terms, check source indexing
```

**Statistical test assumptions violated**
```
Cause: Data not normal, unequal variances
Fix: Use non-parametric alternative (Mann-Whitney, Kruskal-Wallis)
```

**Citation formatting errors**
```
Cause: Missing source fields
Fix: Ensure all required fields are populated
```

**Paper exceeds word limit**
```
Cause: Too much detail in sections
Fix: Condense methodology, move details to appendices
```

**Knowledge graph disconnected**
```
Cause: Nodes lack relationships
Fix: Add explicit edges between related concepts
```

**Confidence level is "none"**
```
Cause: Insufficient evidence found
Fix: Expand search, add more sources
```

## Performance Tuning

| Parameter | Default | Recommended Range |
|-----------|---------|-------------------|
| Search limit | 10 | 5-100 |
| Min relevance | 0.0 | 0.1-0.5 |
| Contradiction threshold | 0.4 | 0.2-0.6 |
| Power level | 0.80 | 0.70-0.95 |
| Alpha level | 0.05 | 0.01-0.10 |
| Abstract word limit | 300 | 150-500 |

## Integration Points

- **Reference Managers**: Export to BibTeX, RIS, EndNote
- **Statistical Software**: Import from CSV, SPSS, R
- **Writing Tools**: LaTeX, Word, Google Scholar
- **Databases**: PubMed, IEEE Xplore, Google Scholar (via API)
- **Collaboration**: Version control for shared research
- **Publishing**: Export to journal submission formats
