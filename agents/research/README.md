# Research Agent

A comprehensive research operations framework for literature review, experiment design, statistical analysis, and academic writing. Supports multiple citation styles and methodologies.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Research Agent provides a complete research operations framework that follows established academic methodologies. It covers the entire research lifecycle from question formulation through publication-ready writing.

### Key Capabilities

- **Research Question Formulation**: Structured question development with sub-questions and keywords
- **Literature Review**: Source indexing, thematic analysis, gap identification, contradiction detection
- **Experiment Design**: Hypothesis formulation, sample size calculation, methodology selection
- **Data Analysis**: Descriptive and inferential statistics, effect sizes, assumption checking
- **Citation Management**: APA, MLA, IEEE, Harvard, Chicago, Vancouver formats
- **Academic Writing**: Abstract, methodology, results, discussion generation
- **Knowledge Graph**: Concept mapping, relationship discovery, path finding

### Use Cases

- Academic literature reviews
- Systematic reviews and meta-analyses
- Experimental research design
- Data analysis and statistical testing
- Thesis and dissertation writing
- Grant proposal preparation
- Conference paper preparation
- Research project management

## Features

### Source Management

| Feature | Description |
|---------|-------------|
| Multi-type Indexing | Journals, conferences, books, theses, patents |
| Full-text Search | TF-IDF weighted keyword search |
| Author Search | Find sources by author name |
| Year Range Search | Filter by publication date |
| Citation Network | Track citation relationships |
| Relevance Ranking | Score and rank search results |

### Analysis Tools

| Feature | Description |
|---------|-------------|
| Theme Extraction | Identify recurring themes across sources |
| Gap Detection | Find under-researched areas |
| Contradiction Detection | Identify conflicting findings |
| Trend Analysis | Track publication and citation trends |
| Methodology Analysis | Categorize research approaches |

### Statistical Testing

| Test | Use Case |
|------|----------|
| t-test | Compare 2 group means |
| ANOVA | Compare 3+ group means |
| Chi-square | Test categorical associations |
| Correlation | Measure variable relationships |
| Regression | Predict outcomes |
| Mann-Whitney | Non-parametric 2-group comparison |
| Kruskal-Wallis | Non-parametric 3+ group comparison |

### Citation Styles

| Style | Field | In-Text Format |
|-------|-------|----------------|
| APA | Social Sciences | (Author, Year) |
| MLA | Humanities | (Author Page) |
| IEEE | Engineering | [Number] |
| Chicago | History | Footnotes |
| Harvard | General | (Author Year) |
| Vancouver | Medicine | [Number] |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Research Agent                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Indexer  │  │ Analyzer │  │Designer  │  │Statistics│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Synthesizer│ │Citations │  │  Writer  │  │  Graph   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/awesome-grok-skills/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

### Basic Usage

```python
from agents.research.agent import ResearchAgent
from agents.research.agent import Source, SourceType, CitationStyle

# Initialize the agent
agent = ResearchAgent()

# Add research question
agent.add_research_question(
    "What are the challenges in AI alignment?",
    keywords=["AI", "alignment", "safety"]
)

# Add sources
source = Source(
    id="src_001",
    title="AI Safety Challenges",
    authors=["Smith, J."],
    source_type=SourceType.JOURNAL_ARTICLE,
    publication_date=datetime(2024, 1, 15),
    abstract="This paper examines...",
    keywords=["AI", "safety"],
)
agent.indexer.add_source(source)

# Conduct literature review
review = agent.literature_review("AI alignment")

# Generate report
report = agent.generate_report("AI Alignment Review")

# Format citations
citation = agent.citation_manager.format_citation(source, CitationStyle.APA)
```

### Run the Agent

```bash
python agents/research/agent.py
```

## Usage

### Literature Review

```python
from agents.research.agent import ResearchAgent, Source, SourceType

agent = ResearchAgent()

# Add sources to the index
for src_data in sources:
    source = Source(**src_data)
    agent.indexer.add_source(source)

# Search for sources
results = agent.indexer.search("machine learning safety", limit=20)

# Conduct full literature review
review = agent.literature_review("AI safety research")
print(f"Themes: {review['key_themes']}")
print(f"Gaps: {review['critical_analysis']['gaps']}")
print(f"Recommendations: {review['recommendations']}")
```

### Experiment Design

```python
from agents.research.agent import ExperimentDesigner, MethodologyType, StatisticalTest

designer = agent.experiment_designer

# Create hypothesis
hypothesis = designer.create_hypothesis(
    "Method X improves accuracy by 20%",
    variables={"IV": "Method", "DV": "Accuracy"},
    test_method=StatisticalTest.T_TEST,
)

# Calculate sample size
n = designer.calculate_sample_size(effect_size=0.5, alpha=0.05, power=0.80)
print(f"Required sample: {n}")

# Design experiment
experiment = designer.design_experiment(
    "Effectiveness Study",
    hypothesis.id,
    MethodologyType.EXPERIMENTAL,
    sample_size=n,
)
```

### Statistical Analysis

```python
from agents.research.agent import StatisticalAnalyzer, StatisticalTest

analyzer = agent.stat_analyzer

# Descriptive statistics
data = [23.5, 25.1, 22.8, 24.3, 26.0, 23.9, 25.5]
stats = analyzer.descriptive_statistics(data)
print(f"Mean: {stats['mean']:.2f}")
print(f"SD: {stats['stdev']:.2f}")

# t-test
group1 = [23.5, 25.1, 22.8, 24.3, 26.0]
group2 = [21.2, 20.8, 22.5, 19.9, 21.7]
result = analyzer.analyze(group1, group2, StatisticalTest.T_TEST)
print(f"t = {result.statistic:.3f}, p = {result.p_value:.4f}")
print(f"Significant: {result.significant}")
print(f"Cohen's d: {result.effect_size:.3f}")

# Correlation
r_result = analyzer.analyze(x_data, y_data, StatisticalTest.CORRELATION)
print(f"r = {r_result.statistic:.3f}")
```

### Citation Management

```python
from agents.research.agent import CitationStyle

# Format single citation
apa = agent.citation_manager.format_citation(source, CitationStyle.APA)
ieee = agent.citation_manager.format_citation(source, CitationStyle.IEEE)
mla = agent.citation_manager.format_citation(source, CitationStyle.MLA)

# Generate bibliography
bib = agent.citation_manager.generate_bibliography(
    ["src_001", "src_002"],
    CitationStyle.APA,
)

# In-text citation
in_text = agent.citation_manager.generate_in_text_citation(
    source, CitationStyle.APA, page=42
)
```

### Academic Writing

```python
# Write abstract
abstract = agent.academic_writer.write_abstract(
    "AI Alignment Challenges",
    agent.research_questions,
    "Key challenges include value alignment and robustness.",
    "Current approaches show promise.",
)

# Write methodology
methodology = agent.academic_writer.write_methodology(
    MethodologyType.SYSTEMATIC_REVIEW,
    sample_size=150,
    variables={"method": "Alignment approach", "score": "Performance"},
    procedures=["Search databases", "Screen articles", "Extract data"],
)

# Write results
results = agent.academic_writer.write_results(
    descriptive_stats={"performance": stats},
    analysis_results=[result],
)
```

### Knowledge Graph

```python
# Add concepts and relationships
ai = agent.add_to_knowledge_graph("AI Alignment", "concept")
safety = agent.add_to_knowledge_graph("AI Safety", "concept")
agent.knowledge_graph.add_edge(ai.id, safety.id, "part_of")

# Find connections
paths = agent.knowledge_graph.find_paths(ai.id, safety.id)
connected = agent.knowledge_graph.get_connected(ai.id)
subgraph = agent.knowledge_graph.get_subgraph(ai.id, depth=2)
```

## API Reference

### ResearchAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_research_question()` | question, priority, sub_questions, keywords | ResearchQuestion | Add research question |
| `conduct_research()` | query, source_types, max_sources | Dict | Search and analyze sources |
| `literature_review()` | topic | Dict | Full literature review |
| `generate_report()` | title, style | Dict | Generate research report |
| `write_paper()` | title, authors, style | ResearchPaper | Create paper structure |
| `analyze_data()` | data1, data2, test | AnalysisResult | Statistical analysis |
| `add_to_knowledge_graph()` | concept, type, connections | KnowledgeNode | Add to knowledge graph |

### ResearchIndexer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_source()` | source | None | Add source to index |
| `search()` | query, source_type, limit, min_relevance | List[Source] | Search sources |
| `search_by_author()` | author | List[Source] | Search by author |
| `search_by_year()` | year | List[Source] | Search by year |
| `get_most_cited()` | limit | List[Source] | Most cited sources |
| `get_recent()` | days, limit | List[Source] | Recently published |

### StatisticalAnalyzer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `analyze()` | data1, data2, test, alpha | AnalysisResult | Run statistical test |
| `descriptive_statistics()` | data | Dict[str, float] | Calculate descriptive stats |
| `effect_size_cohens_d()` | group1, group2 | float | Calculate Cohen's d |

### CitationManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_reference()` | source | None | Add to reference library |
| `format_citation()` | source, style, num | str | Format citation |
| `generate_bibliography()` | source_ids, style | List[str] | Generate bibliography |
| `generate_in_text_citation()` | source, style, page | str | In-text citation |

## Examples

### Complete Literature Review

```python
from agents.research.agent import ResearchAgent, Source, SourceType, CitationStyle
from datetime import datetime

agent = ResearchAgent()

# Add research question
agent.add_research_question(
    "How effective is reinforcement learning for robotics?",
    keywords=["reinforcement learning", "robotics", "control"],
)

# Add sources
sources = [
    Source(
        id="src_001",
        title="Deep RL for Robotic Control",
        authors=["Zhang, L.", "Wang, M."],
        source_type=SourceType.JOURNAL_ARTICLE,
        publication_date=datetime(2024, 3, 1),
        abstract="We present a deep RL approach for robotic manipulation...",
        keywords=["deep learning", "reinforcement learning", "robotics"],
        citations=85,
        journal="Robotics and Autonomous Systems",
    ),
    # ... more sources
]

for source in sources:
    agent.indexer.add_source(source)

# Conduct review
review = agent.literature_review("reinforcement learning robotics")

# Generate report
report = agent.generate_report("RL for Robotics Review", CitationStyle.APA)

# Write paper
paper = agent.write_paper(
    "Reinforcement Learning in Robotics: A Comprehensive Review",
    ["Author Name"],
)

print(f"Review complete: {len(report['bibliography'])} references")
```

### Data Analysis Pipeline

```python
from agents.research.agent import StatisticalAnalyzer, StatisticalTest

analyzer = StatisticalAnalyzer()

# Generate sample data
control = [22.1, 23.5, 21.8, 24.2, 22.9, 23.1, 21.5, 24.8, 22.3, 23.7]
treatment = [25.3, 26.1, 24.8, 27.2, 25.9, 26.5, 24.3, 27.8, 25.1, 26.9]

# Descriptive statistics
desc_control = analyzer.descriptive_statistics(control)
desc_treatment = analyzer.descriptive_statistics(treatment)

print("Control group:")
print(f"  Mean = {desc_control['mean']:.2f}, SD = {desc_control['stdev']:.2f}")
print("Treatment group:")
print(f"  Mean = {desc_treatment['mean']:.2f}, SD = {desc_treatment['stdev']:.2f}")

# t-test
t_result = analyzer.analyze(control, treatment, StatisticalTest.T_TEST)
print(f"\nt-test: t({len(control)+len(treatment)-2}) = {t_result.statistic:.3f}")
print(f"p = {t_result.p_value:.4f}")
print(f"Significant: {t_result.significant}")

# Effect size
d = analyzer.effect_size_cohens_d(control, treatment)
print(f"Cohen's d = {d:.3f}")

# Correlation
import random
x = [random.uniform(0, 10) for _ in range(50)]
y = [xi * 2 + random.uniform(-1, 1) for xi in x]
r_result = analyzer.analyze(x, y, StatisticalTest.CORRELATION)
print(f"\nCorrelation: r = {r_result.statistic:.3f}, p = {r_result.p_value:.4f}")
```

### Multi-Style Citations

```python
from agents.research.agent import CitationManager, CitationStyle, Source, SourceType

manager = CitationManager()

source = Source(
    id="ref_001",
    title="The Art of Research",
    authors=["Smith, J.", "Doe, A.", "Brown, B."],
    source_type=SourceType.BOOK,
    publication_date=datetime(2024, 6, 1),
    publisher="Academic Press",
    isbn="978-0-123456-78-9",
)

# Different citation styles
styles = [CitationStyle.APA, CitationStyle.MLA, CitationStyle.IEEE,
          CitationStyle.HARVARD, CitationStyle.CHICAGO, CitationStyle.VANCOUVER]

for style in styles:
    citation = manager.format_citation(source, style)
    print(f"{style.value.upper()}: {citation}")
```

## Configuration

### Research Settings

```yaml
research_agent:
  indexer:
    max_sources: 10000
    min_relevance_score: 0.1
    
  analyzer:
    contradiction_threshold: 0.4
    gap_detection_depth: 3
    
  experiment:
    default_alpha: 0.05
    default_power: 0.80
    min_sample_size: 30
    
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
```

## Best Practices

### Literature Review

1. **Define Clear Search Strategy** - Document databases, search terms, and filters
2. **Use Inclusion/Exclusion Criteria** - Be systematic about what to include
3. **Screen by Title, Then Abstract, Then Full Text** - Progressive screening
4. **Extract Data Systematically** - Use standardized forms
5. **Assess Quality** - Use established quality assessment tools
6. **Document Everything** - Follow PRISMA guidelines

### Experiment Design

1. **Pre-register Your Study** - Specify hypotheses and analysis plan beforehand
2. **Calculate Sample Size** - Use power analysis to determine required N
3. **Randomize Properly** - Use appropriate randomization methods
4. **Control Confounds** - Identify and control confounding variables
5. **Plan for Attrition** - Expect and account for dropouts
6. **Use Blinding** - Single or double-blind when possible

### Statistical Analysis

1. **Check Assumptions First** - Verify test assumptions before applying
2. **Report Effect Sizes** - p-values alone are insufficient
3. **Use Confidence Intervals** - More informative than p-values alone
4. **Correct for Multiple Comparisons** - Bonferroni, FDR, etc.
5. **Visualize Your Data** - Plots reveal patterns numbers miss
6. **Report Completely** - Include null results and failed analyses

### Academic Writing

1. **Write the Abstract Last** - Summarize after completing the paper
2. **Lead with Contributions** - State what's new in the introduction
3. **Be Concise** - Every word should earn its place
4. **Use Active Voice** - Clearer and more direct
5. **Cite as You Write** - Don't leave citations for later
6. **Revise Multiple Times** - First drafts are never final

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No search results | Query too specific | Broaden search terms |
| Assumptions violated | Non-normal data | Use non-parametric tests |
| Citation errors | Missing fields | Ensure all required fields present |
| Paper too long | Too much detail | Move details to appendices |
| Graph disconnected | Missing edges | Add explicit relationships |
| Confidence "none" | No evidence found | Expand source collection |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Files

- `agent.py` - Main implementation with all components
- `ARCHITECTURE.md` - System architecture and design patterns
- `GROK.md` - Agent instructions, capabilities, and workflows
- `README.md` - This file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see [LICENSE](../../LICENSE) for details.
