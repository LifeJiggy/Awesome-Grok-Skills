# NLP Agent

## Overview

The **NLP Agent** provides comprehensive natural language processing capabilities including text preprocessing, classification, named entity recognition, sentiment analysis, and text generation. This agent enables machines to understand, interpret, and generate human language.

## Core Capabilities

### 1. Text Preprocessing
Clean and prepare text data:
- **Tokenization**: Word and sentence splitting
- **Normalization**: Lowercase, stemming, lemmatization
- **Stopword Removal**: Filter common words
- **N-gram Generation**: Create n-gram features
- **Vectorization**: TF-IDF, word embeddings

### 2. Text Classification
Categorize text content:
- **Binary Classification**: Yes/no categories
- **Multi-Class**: Multiple categories
- **Multi-Label**: Multiple labels per text
- **Sentiment Analysis**: Positive/negative/neutral
- **Topic Classification**: Subject categorization

### 3. Named Entity Recognition
Identify entities in text:
- **Entity Types**: Person, Location, Organization
- **Entity Linking**: Link to knowledge bases
- **Relation Extraction**: Entity relationships
- **Temporal Entities**: Dates and times
- **Numerical Entities**: Money, quantities

### 4. Sentiment Analysis
Understand emotional content:
- **Polarity Detection**: Positive/negative/neutral
- **Emotion Detection**: Joy, anger, sadness, etc.
- **Aspect-Based**: Sentiment per aspect
- **Sarcasm Detection**: Irony identification
- **Intensity Scoring**: Strength of sentiment

### 5. Text Generation
Create human-like text:
- **Text Completion**: Autocomplete
- **Summarization**: Condense content
- **Translation**: Multi-language support
- **Question Answering**: Generate responses
- **Creative Writing**: Stories, poems

### 6. Topic Modeling
Discover document themes:
- **LDA**: Latent Dirichlet Allocation
- **Keyword Extraction**: Important terms
- **Document Clustering**: Group similar documents
- **Topic Tracking**: Over time analysis

## Usage Examples

### Text Preprocessing

```python
from nlp import TextPreprocessor

preprocessor = TextPreprocessor()
text = "Hello, world! How are you today?"
tokens = preprocessor.tokenize(text)
print(f"Tokens: {tokens}")

cleaned = preprocessor.clean_text(text, ['lowercase', 'remove_punctuation'])
print(f"Cleaned: {cleaned}")

no_stopwords = preprocessor.remove_stopwords(tokens)
print(f"Without stopwords: {no_stopwords}")

ngrams = preprocessor.create_ngrams(tokens, 2)
print(f"Bigrams: {ngrams}")

vector = preprocessor.vectorize([text], method="tfidf")
print(f"Vector shape: {vector['shape']}")
```

### Text Classification

```python
from nlp import TextClassifier

classifier = TextClassifier()
result = classifier.classify_text(
    "Great product, highly recommend!",
    model="bert"
)
print(f"Classification: {result['top_class']} ({result['confidence']:.2%})")

multi = classifier.multi_label_classification(
    "Technology article about AI",
    labels=['technology', 'science', 'sports']
)
print(f"Labels: {multi['selected_labels']}")
```

### Named Entity Recognition

```python
from nlp import NamedEntityRecognizer

ner = NamedEntityRecognizer()
entities = ner.extract_entities(
    "John Smith works at Google in New York."
)
for e in entities:
    print(f"{e['text']} ({e['type']})")

linking = ner.entity_linking("John Smith")
print(f"Wikidata: {linking['wikidata_id']}")

relations = ner.relation_extraction("John works at Google.")
print(f"Relations: {len(relations)}")
```

### Sentiment Analysis

```python
from nlp import SentimentAnalyzer

sentiment = SentimentAnalyzer()
analysis = sentiment.analyze_sentiment(
    "I love this product! It's amazing!",
    model="roberta"
)
print(f"Sentiment: {analysis['sentiment']} ({analysis['confidence']:.2%})")

emotions = sentiment.analyze_emotions("I'm so excited about this!")
print(f"Dominant: {emotions['dominant_emotion']}")
```

### Text Generation

```python
from nlp import TextGenerator

generator = TextGenerator()
generated = generator.generate_text(
    "The future of AI is",
    max_length=100,
    model="gpt"
)
print(f"Generated: {generated['generated_text'][:100]}...")

summary = generator.summarize_text(
    "Long document text...",
    max_length=50,
    method="extractive"
)
print(f"Summary: {summary['summary']}")

answer = generator.answer_question(
    question="What is machine learning?",
    context="Machine learning is a subset of AI..."
)
print(f"Answer: {answer['answer']}")
```

## NLP Pipeline

```
┌─────────────────────────────────────────────────────────┐
│              NLP Pipeline                               │
├─────────────────────────────────────────────────────────┤
│  1. Text Input → 2. Preprocessing                      │
│         │                          │                    │
│  6. Output ← 5. Post-Processing ← 4. Model Inference   │
│         │                          │                    │
│         └────────── 3. Feature Extraction ─────────────┘
└─────────────────────────────────────────────────────────┘
```

## NLP Models

### Transformer Models

| Model | Parameters | Languages | Use Case |
|-------|------------|-----------|----------|
| BERT | 110M | 104 | General NLP |
| GPT-3 | 175B | English | Text generation |
| T5 | 11B | Multilingual | Seq2Seq |
| XLM-R | 1.5B | 100 | Cross-lingual |

### Specialized Models
- **RoBERTa**: Optimized BERT
- **ALBERT**: Lightweight BERT
- **DistilBERT**: Compressed BERT
- **BART**: Sequence-to-sequence

## Text Analysis Techniques

### Statistical Methods
- **TF-IDF**: Term frequency-inverse document frequency
- **Word Embeddings**: Word2Vec, GloVe
- **Topic Models**: LDA, NMF
- **Document Similarity**: Cosine similarity

### Deep Learning Methods
- **RNN/LSTM**: Sequential modeling
- **Attention**: Focus on important parts
- **Transformers**: Self-attention architecture
- **BERT/GPT**: Pre-trained language models

## Evaluation Metrics

### Classification Metrics
| Metric | Description | Formula |
|--------|-------------|---------|
| Accuracy | Overall correctness | (TP+TN)/Total |
| Precision | Predicted positives | TP/(TP+FP) |
| Recall | Actual positives | TP/(TP+FN) |
| F1 | Harmonic mean | 2PR/(P+R) |

### Generation Metrics
| Metric | Description |
|--------|-------------|
| BLEU | N-gram overlap |
| ROUGE | Recall-oriented |
| METEOR | Semantic matching |
| Perplexity | Language model quality |

## Applications

### 1. Customer Service
- Chatbots and virtual assistants
- Sentiment analysis for feedback
- Ticket classification
- Response generation

### 2. Content Analysis
- Topic extraction
- Document summarization
- Trend analysis
- Content recommendation

### 3. Healthcare
- Clinical note analysis
- Medical entity extraction
- Patient feedback analysis
- Research paper mining

### 4. Legal Tech
- Document classification
- Contract analysis
- Case law search
- Legal document summarization

### 5. Social Media
- Trend detection
- Sentiment tracking
- Influencer identification
- Content moderation

## Tools and Libraries

### Python Libraries
- **NLTK**: Classic NLP tools
- **spaCy**: Industrial-strength NLP
- **Transformers**: Hugging Face models
- **Gensim**: Topic modeling

### APIs and Services
- **OpenAI API**: GPT models
- **Google NLP**: Cloud NLP
- **AWS Comprehend**: Managed NLP
- **Azure Text Analytics**: Cognitive services

## Best Practices

1. **Data Quality**: Clean, diverse training data
2. **Preprocessing**: Consistent text normalization
3. **Model Selection**: Task-appropriate models
4. **Evaluation**: Human evaluation when possible
5. **Bias Awareness**: Monitor for biases
6. **Continuous Learning**: Update models

## Related Skills

- [Machine Learning](../machine-learning/model-development/README.md) - ML fundamentals
- [Data Science](../data-science/statistical-analysis/README.md) - Data analysis
- [Text Analytics](../analytics/text-analytics/README.md) - Text mining

---

**File Path**: `skills/nlp/text-processing/resources/nlp.py`
