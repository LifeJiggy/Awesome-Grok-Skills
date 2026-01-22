# Synthetic Data Agent

## Overview

The **Synthetic Data Agent** provides comprehensive test data generation and data anonymization capabilities. This agent enables privacy-preserving data sharing, testing environments, and data augmentation without exposing real user information.

## Core Capabilities

### 1. Synthetic Data Generation
Generate realistic test data:
- **Schema-based Generation**: From defined schemas
- **Relational Data**: Multi-table datasets
- **Time Series**: Temporal data with trends
- **Structured Data**: JSON, CSV, database formats
- **Custom Generators**: Domain-specific data

### 2. Data Anonymization
Protect sensitive information:
- **PII Detection**: Auto-identify sensitive fields
- **Masking**: Partial data hiding
- **Pseudonymization**: Consistent fake values
- **Generalization**: Reduce precision
- **Perturbation**: Add controlled noise

### 3. Data Export
Export in multiple formats:
- **JSON**: Structured data exchange
- **CSV**: Tabular data
- **SQL**: Database inserts
- **Parquet**: Columnar storage
- **Avro**: Serialization format

### 4. Privacy Compliance
Meet regulatory requirements:
- **GDPR**: EU data protection
- **CCPA**: California privacy law
- **HIPAA**: Healthcare data protection
- **SOC 2**: Security compliance

## Usage Examples

### Generate Schema-based Data

```python
from synthetic_data import SyntheticDataGenerator, FieldConfig, DataType

generator = SyntheticDataGenerator()
schema = [
    FieldConfig('id', DataType.UUID),
    FieldConfig('name', DataType.NAME),
    FieldConfig('email', DataType.EMAIL),
    FieldConfig('age', DataType.NUMBER, min_value=18, max_value=99),
    FieldConfig('created_at', DataType.DATE)
]
generator.define_schema('users', schema)
records = generator.generate_batch('users', 10)
```

### Anonymize Sensitive Data

```python
from synthetic_data import DataAnonymizer

anonymizer = DataAnonymizer()
sensitive = {
    'name': 'John Doe',
    'email': 'john@real.com',
    'ssn': '123-45-6789'
}
anonymized = anonymizer.anonymize_record(sensitive)
print(anonymized)
```

### Generate Fake Identities

```python
identities = anonymizer.generate_fake_identities(10)
for identity in identities:
    print(f"ID: {identity['id']}, Name: {identity['fake_0_name']}")
```

## Data Types Supported

### Basic Types
- **UUID**: Unique identifiers
- **NAME**: Person names (first, last, full)
- **EMAIL**: Email addresses
- **PHONE**: Phone numbers
- **ADDRESS**: Structured addresses

### Numeric Types
- **NUMBER**: Integers and floats
- **BOOLEAN**: True/false values
- **CURRENCY**: Monetary values

### Temporal Types
- **DATE**: Calendar dates
- **DATETIME**: Timestamps
- **TIME**: Time of day

### Special Types
- **JSON**: Nested objects
- **ENUM**: Predefined options
- **CUSTOM**: Regex-based generation

## Anonymization Techniques

### Data Masking
```python
# Full masking
"john@example.com" → "***@***.com"

# Partial masking
"John Smith" → "J*** S****"
```

### Pseudonymization
```python
# Consistent mapping
"john@real.com" → "user8472@example.com"
"john@real.com" → "user8472@example.com"  # Same each time
```

### Generalization
```python
# Reduce precision
"42.5678" → "42.5"  # Round to 1 decimal
"2024-01-15" → "2024-01"  # Remove day
```

### Perturbation
```python
# Add noise
42.0 → 42.3 (±5% variation)
```

## Data Generation Strategies

### Realistic Distribution
- Match statistical properties
- Preserve correlations
- Maintain referential integrity

### Preserving Privacy
- k-anonymity (≥k records per group)
- l-diversity (≥l distinct values)
- Differential privacy (add noise)

### Scalability
- Streaming generation
- Parallel processing
- Incremental updates

## Use Cases

### 1. Development & Testing
- Seed development databases
- Create test fixtures
- Generate demo data

### 2. Data Sharing
- Share with external teams
- Publish for research
- Submit for audits

### 3. Machine Learning
- Augment training data
- Create balanced datasets
- Generate adversarial examples

### 4. Compliance
- Anonymize for GDPR
- Mask sensitive fields
- Generate audit trails

## Quality Metrics

### Realism
- **Statistical Similarity**: Distribution matching
- **Correlation Preservation**: Relationship maintenance
- **Domain Validity**: Valid format/values

### Privacy
- **Re-identification Risk**: Attack resistance
- **Information Loss**: Utility preservation
- **Disclosure Risk**: Data leak potential

### Performance
- **Generation Speed**: Records per second
- **Storage Efficiency**: Compression ratio
- **Export Speed**: Format conversion

## Tools Integration

### Python Libraries
- **Faker**: Fake data generation
- **Mimesis**: Synthetic data library
- **SDV**: Synthetic data vault

### Database Tools
- **Mockaroo**: Web-based generation
- **Datameer**: Enterprise synthesis
- **Mostly AI**: AI-powered synthesis

### Cloud Services
- **AWS SageMaker Canvas**: No-code ML
- **Google Synthetics**: Data synthesis
- **Azure Synapse**: Data generation

## Best Practices

1. **Understand Data**: Analyze original dataset
2. **Define Privacy Levels**: Classify sensitivity
3. **Validate Output**: Check data quality
4. **Document Process**: Maintain audit trail
5. **Iterate**: Refine based on feedback

## Related Skills

- [Data Engineering](../data-engineering/data-pipelines/README.md) - Data pipelines
- [Privacy Engineering](../privacy/data-protection/README.md) - Data protection
- [Database Administration](../database-admin/db-management/README.md) - Database management

---

**File Path**: `skills/synthetic-data/data-generation/resources/synthetic_data.py`
