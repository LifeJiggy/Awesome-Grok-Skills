---
name: "fact-checking"
category: "journalism-tech"
version: "2.0.0"
tags: ["journalism", "fact-checking", "verification", "credibility", "misinformation"]
description: "Automated fact-checking and claim verification tools for journalism"
---

# Fact-Checking

## Overview

The Fact-Checking module provides tools for verifying claims, checking sources, and identifying misinformation. It supports claim extraction, source verification, cross-referencing with authoritative databases, credibility scoring, and generating fact-check reports. The module enables journalists to verify information quickly and accurately.

## Core Capabilities

- **Claim Extraction**: Identify checkable claims from text
- **Source Verification**: Validate source credibility and authority
- **Cross-Reference**: Check claims against authoritative databases
- **Credibility Scoring**: Rate source and claim credibility
- **Misinformation Detection**: Identify common misinformation patterns
- **Fact-Check Reports**: Generate structured fact-check reports
- **Image Verification**: Reverse image search and manipulation detection
- **URL Verification**: Check URL reputation and safety

## Usage Examples

### Claim Verification

```python
from fact_checking import FactChecker, Claim

checker = FactChecker()

# Verify a claim
claim = Claim(
    text="The city budget increased by 45% over the past 5 years",
    source="city_council_report",
    date="2024-01-15",
)

result = checker.verify_claim(claim)
print(f"Claim Verification:")
print(f"  Verdict: {result.verdict}")
print(f"  Confidence: {result.confidence:.1%}")
print(f"  Sources Checked: {result.sources_checked}")
print(f"  Supporting Evidence: {len(result.supporting_evidence)}")
print(f"  Contradicting Evidence: {len(result.contradicting_evidence)}")
```

### Source Credibility

```python
from fact_checking import SourceEvaluator, Source

evaluator = SourceEvaluator()

# Evaluate source credibility
source = Source(
    name="City Budget Office",
    url="https://city.gov/budget",
    type="government",
    domain_authority=85,
)

credibility = evaluator.evaluate(source)
print(f"Source Credibility:")
print(f"  Score: {credibility.score:.1%}")
print(f"  Reliability: {credibility.reliability}")
print(f"  Bias Rating: {credibility.bias_rating}")
print(f"  Transparency: {credibility.transparency_score:.1%}")
```

### Misinformation Detection

```python
from fact_checking import MisinformationDetector

detector = MisinformationDetector()

# Analyze text for misinformation patterns
analysis = detector.analyze(
    text="Scientists confirm that 5G towers cause health problems",
    context="news_article",
)

print(f"Misinformation Analysis:")
print(f"  Risk Level: {analysis.risk_level}")
print(f"  Patterns Detected: {analysis.patterns}")
print(f"  Red Flags: {analysis.red_flags}")
print(f"  Recommendation: {analysis.recommendation}")
```

### Fact-Check Report

```python
from fact_checking import ReportGenerator, FactCheckReport

generator = ReportGenerator()

# Generate fact-check report
report = generator.generate(
    claim="Budget increased 45%",
    verdict="TRUE",
    sources=[
        {"name": "Budget Report 2019", "content": "Total: $100M"},
        {"name": "Budget Report 2024", "content": "Total: $145M"},
    ],
    explanation="Budget data confirms 45% increase from $100M to $145M",
)

print(f"Fact-Check Report:")
print(f"  Claim: {report.claim}")
print(f"  Verdict: {report.verdict}")
print(f"  Published: {report.publication_date}")
```

## Best Practices

- **Multiple Sources**: Verify claims with multiple independent sources
- **Primary Sources**: Prefer primary sources over secondary reports
- **Context Matters**: Consider full context of claims
- **Transparency**: Document verification methodology
- **Fairness**: Present findings fairly and completely
- **Timeliness**: Note when information was last verified
- **Corrections**: Have a clear correction policy
- **Avoid Amplification**: Don't amplify misinformation while debunking

## Related Modules

- **investigative-tools**: Tools for investigative reporting
- **data-journalism**: Data analysis for verification
- **content-management**: Publishing fact-check reports
