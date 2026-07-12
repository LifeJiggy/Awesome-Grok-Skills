---
name: recruitment-ai
category: hr-tech
version: 1.0.0
tags:
  - recruitment
  - ai
  - resume-parsing
  - candidate-matching
  - interview-scheduling
  - bias-detection
  - nlp
  - hr-tech
difficulty: advanced
estimated_time: 60min
prerequisites:
  - python-3.11
  - pandas
  - scikit-learn
  - nltk
---

# Recruitment AI

## Purpose

End-to-end AI-driven recruitment pipeline covering resume parsing, candidate-job matching, interview scheduling optimization, and algorithmic bias detection. This skill builds production-grade recruitment automation with fairness auditing built in.

## Core Components

### 1. Resume Parsing Engine

- **Structured Extraction**: Parse PDF/DOCX resumes into normalized candidate profiles (skills, experience, education, certifications)
- **NLP Pipeline**: Tokenization, NER for skills/companies/degrees, experience duration extraction
- **Skill Taxonomy Mapping**: Map free-text skills to a canonical taxonomy using fuzzy matching and embedding similarity
- **Confidence Scoring**: Assign extraction confidence scores per field; flag low-confidence profiles for human review

### 2. Candidate-Job Matching

- **Multi-Signal Scoring**: Combine skill overlap, experience level, education fit, location compatibility, and salary alignment into a composite match score
- **Weighted Configuration**: Per-role weighting profiles (e.g., startup = skill > degree, enterprise = degree + certification)
- **Diversity-Aware Ranking**: Re-rank shortlists to ensure diverse slates without compromising minimum qualification thresholds
- **Explainability Layer**: Generate human-readable reasoning for each match score component

### 3. Interview Scheduling Optimizer

- **Constraint Satisfaction**: Solve scheduling as CSP — interviewer availability, candidate timezone, room/resource booking, buffer times
- **Cascade Scheduling**: Multi-round scheduling with dependency chains (phone screen -> technical -> onsite -> executive)
- **No-Show Prediction**: ML model predicting candidate interviewer no-shows to overbook strategically
- **Candidate Experience Scoring**: Rank schedule options by candidate convenience (fewer reschedules, preferred time slots)

### 4. Bias Detection & Fairness Audit

- **Statistical Parity**: Measure selection rate differences across protected groups (gender, ethnicity, age)
- **Disparate Impact Ratio**: Calculate 4/5ths rule compliance per hiring stage
- **Feature Attribution**: Identify which resume features (name, school prestige, gap periods) correlate with adverse outcomes
- **Mitigation Strategies**: Automated resume anonymization, structured interview scorecards, calibration workshops

## Data Models

```
CandidateProfile
  ├── skills: List[SkillMatch]
  ├── experience: List[WorkExperience]
  ├── education: List[Education]
  ├── certifications: List[str]
  └── metadata: CandidateMetadata

JobRequirement
  ├── required_skills: List[SkillRequirement]
  ├── preferred_skills: List[SkillRequirement]
  ├── experience_range: ExperienceRange
  ├── education_level: EducationLevel
  └── compensation: CompensationRange

MatchResult
  ├── candidate_id: str
  ├── job_id: str
  ├── composite_score: float
  ├── component_scores: Dict[str, float]
  ├── explanation: str
  └── flagged_bias_risks: List[BiasFlag]
```

## Implementation Patterns

### Skill Extraction Pipeline
```python
class SkillExtractor:
    def extract(self, resume_text: str) -> List[SkillMatch]:
        tokens = self.tokenize(resume_text)
        entities = self.ner_extract(tokens)
        skills = self.map_to_taxonomy(entities)
        return [SkillMatch(skill=s, confidence=c) for s, c in skills]
```

### Bias Audit Workflow
```python
class BiasAuditor:
    def audit(self, shortlist: List[MatchResult], demographics: Dict) -> AuditReport:
        rates = self.selection_rates(shortlist, demographics)
        disparate_impact = self.calculate_dir(rates)
        features = self.feature_attribution(shortlist, demographics)
        return AuditReport(rates, disparate_impact, features, self.recommendations(disparate_impact))
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_match_score` | 0.60 | Minimum composite score to advance |
| `diversity_rebalance_factor` | 0.15 | Max ranking adjustment for diversity |
| `anonymize_level` | `full` | `none`, `partial`, `full` resume anonymization |
| `bias_threshold` | 0.80 | Disparate impact ratio floor (4/5ths rule) |
| `max_schedule_rounds` | 5 | Maximum interview cascade depth |

## Integration Points

- **ATS Connectors**: Greenhouse, Lever, Workday, iCIMS via REST API
- **Calendar**: Google Calendar, Outlook via OAuth2
- **Assessment Platforms**: HackerRank, Codility, Criteria via webhook
- **Background Checks**: Checkr, Sterling integration hooks
- **Job Boards**: LinkedIn, Indeed, Glassdoor posting APIs

## Ethical Guidelines

1. Never use protected characteristics as input features for ranking
2. All bias audit results must be reviewed by a human before acting on recommendations
3. Candidates must be informed when AI is used in screening (transparency requirement)
4. Regular third-party audits recommended quarterly for high-volume hiring
5. Maintain human-in-the-loop for all hiring decisions above senior IC level

## Testing Strategy

- **Unit Tests**: Skill extraction accuracy, scoring calculation correctness, scheduling constraint satisfaction
- **Integration Tests**: End-to-end pipeline from resume input to shortlist output
- **Fairness Tests**: Synthetic candidate pools with controlled demographics to verify bias detection
- **Regression Tests**: Known-good match results preserved as golden snapshots
