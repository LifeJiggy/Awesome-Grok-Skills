---
name: clinical-data
category: health-tech
version: 1.0.0
tags:
  - clinical-trials
  - redcap
  - cdisc
  - data-validation
  - adverse-events
  - regulatory
difficulty: advanced
estimated_time: 100 minutes
prerequisites:
  - python-programming
  - biostatistics-basics
  - regulatory-knowledge
---

# Clinical Data Management

Clinical data management (CDM) encompasses the collection, cleaning, validation, and reporting of data from clinical trials. Key standards include CDISC (SDTM, ADaM, ODM), REDCap for data capture, and ICH-GCP for quality assurance.

## Core Concepts

### Clinical Trials
Multi-phase research studies evaluating safety and efficacy of interventions. Data flows from site-level collection through EDC systems to central databases, undergoing validation and query management at each stage.

### REDCap
Research Electronic Data Capture — a secure, web-based platform designed to support data capture for research studies. Features: branching logic, validation, audit trails, de-identification, API access, and multi-site coordination.

### CDISC Standards
- **SDTM** (Study Data Tabulation Model): Raw collected data organized into standard domains
- **ADaM** (Analysis Data Model): Analysis-ready datasets derived from SDTM
- **ODM** (Operational Data Model): Exchange format for clinical data and metadata
- **Define-XML**: Metadata describing datasets, variables, and controlled terminology

### Data Validation
Systematic quality assurance processes: edit checks, range validation, cross-field logic, missing data detection, protocol deviation identification, and medical coding (MedDRA, WHO Drug).

### Adverse Events
Systematic collection, grading (CTCAE v5.0), causality assessment, and regulatory reporting (IND safety reports, SUSARs) of adverse experiences during clinical trials.

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│              Clinical Data Management Pipeline             │
├──────────────┬──────────────────┬─────────────────────────┤
│  Collection  │   Processing     │   Reporting             │
│              │                  │                         │
│ • EDC/REDCap │ • Edit Checks   │ • SDTM Datasets         │
│ • ePRO       │ • Query Mgmt    │ • ADaM Tables           │
│ • Lab Data   │ • Coding        │ • CSR Tables            │
│ • IVRS/IWRS  │ • Derivations   │ • DSMB Reports          │
│ • eSource    │ • Audit Trail   │ • Regulatory Submissions│
└──────────────┴──────────────────┴─────────────────────────┘
```

## CDISC Domains

| Domain | Description | Key Variables |
|--------|-------------|---------------|
| DM | Demographics | USUBJID, AGE, SEX, RACE |
| AE | Adverse Events | AETERM, AESEV, AEREL, AESTDTC |
| CM | Concomitant Medications | CMTRT, CMDOSE, CMROUTE |
| LB | Laboratory Results | LBTEST, LBORRES, LBORRESU |
| VS | Vital Signs | VSTEST, VSORRES, VSORRESU |
| EX | Exposure (Drugs) | EXTRT, EXDOSE, EXDUR |
| QS | Questionnaires | QSTEST, QSORRES |
| AE | Adverse Events | AETERM, AESEV, AESER |
| MH | Medical History | MHTERM, MHSTDTC |

## CTCAE Grading

| Grade | Description |
|-------|-------------|
| 1 | Mild — asymptomatic or mild symptoms |
| 2 | Moderate — minimal, local, noninvasive intervention |
| 3 | Severe — medically significant, hospitalization |
| 4 | Life-threatening — urgent intervention indicated |
| 5 | Death related to AE |

## Common Pitfalls

1. **Protocol deviations**: Inclusion/exclusion criteria not properly checked
2. **Query cascades**: One data issue triggering dozens of follow-up queries
3. **Coding delays**: MedDRA/WHODrug coding backlog affecting data lock timelines
4. **Missing data patterns**: Systematic missingness biasing efficacy analyses
5. **Audit trail gaps**: Changes made outside the EDC system
6. **CDISC non-compliance**: Late-stage SDTM mapping failures delaying submissions

## References

- ICH E6(R2) Good Clinical Practice
- CDISC SDTM v3.4: https://www.cdisc.org/standards
- REDCap: https://projectredcap.org
- CTCAE v5.0: https://ctep.cancer.gov/protocoldevelopment/electronic_applications/ctc.htm
- MedDRA: https://www.meddra.org

## Advanced Configuration

### REDCap Configuration
```javascript
// Advanced REDCap configuration
const redcapConfig = {
  baseUrl: 'https://redcap.example.com',
  token: process.env.REDCAP_API_TOKEN,
  projectIds: ['123', '456', '789'],
  validation: {
    strictMode: false,
    allowMissingData: true,
    requireDateFormats: true,
  },
  export: {
    format: 'json',
    includeMetadata: true,
    includeSurveyFields: true,
    combineCheckboxes: true,
  },
  queries: {
    autoGenerate: true,
    requireResponse: true,
    escalationDays: 7,
    maxQueriesPerField: 3,
  },
  audit: {
    enabled: true,
    logAllChanges: true,
    retainDays: 365,
  },
};
```

### CDISC Configuration
```javascript
// CDISC standards configuration
const cdiscConfig = {
  sdtm: {
    version: '3.4',
    domains: ['DM', 'AE', 'CM', 'LB', 'VS', 'EX', 'QS', 'MH'],
    controlledTerminology: {
      meddra: '26.0',
      whodrug: '2023-06',
    },
    validation: {
      enabled: true,
      strictMode: false,
      allowCustomDomains: true,
    },
  },
  adam: {
    version: '1.1',
    datasets: ['ADSL', 'ADAE', 'ADLB', 'ADCM'],
    analysisPopulations: ['ITT', 'mITT', 'PP', 'Safety'],
  },
  odm: {
    version: '1.3.2',
    includeAuditTrail: true,
    includeMedia: true,
    exportFormat: 'xml',
  },
};
```

### Data Validation Configuration
```javascript
// Data validation configuration
const validationConfig = {
  editChecks: {
    enabled: true,
    severity: ['error', 'warning', 'info'],
    autoResolve: false,
    requireComment: true,
  },
  rangeChecks: {
    enabled: true,
    useStudyReferenceRanges: true,
    allowOverride: true,
  },
  crossFieldChecks: {
    enabled: true,
    rules: [
      { name: 'AE dates', check: 'AESTDTC <= AEENDTC' },
      { name: 'Age consistency', check: 'AGE == calculate_age(BRTHDTC)' },
    ],
  },
  missingData: {
    enabled: true,
    criticalFields: ['USUBJID', 'ARM', 'RANDDT'],
    reportMissing: true,
  },
};
```

## Architecture Patterns

### Clinical Data Architecture
```javascript
// Clinical data architecture
class ClinicalDataArchitect {
  constructor() {
    this.collection = new DataCollection();
    this.processing = new DataProcessing();
    this.reporting = new DataReporting();
  }

  async processData(studyId) {
    // Collect data from sources
    const rawData = await this.collection.collect(studyId);
    
    // Process and validate
    const processedData = await this.processing.process(rawData);
    
    // Generate reports
    const reports = await this.reporting.generate(processedData);
    
    return {
      rawData,
      processedData,
      reports,
    };
  }

  async validateData(data, studyId) {
    const validationRules = await this.getValidationRules(studyId);
    const results = [];
    
    for (const rule of validationRules) {
      const result = await this.applyRule(rule, data);
      results.push(result);
    }
    
    return results;
  }
}
```

### Data Collection Architecture
```javascript
// Data collection architecture
class DataCollection {
  constructor() {
    this.sources = new Map();
    this.transformers = new Map();
  }

  async collect(studyId) {
    const sources = this.getSources(studyId);
    const collectedData = [];
    
    for (const source of sources) {
      const data = await source.collect();
      const transformed = await this.transform(source.type, data);
      collectedData.push(...transformed);
    }
    
    return collectedData;
  }

  getSources(studyId) {
    return Array.from(this.sources.values())
      .filter(source => source.studyId === studyId);
  }

  async transform(sourceType, data) {
    const transformer = this.transformers.get(sourceType);
    if (!transformer) {
      return data;
    }
    
    return transformer.transform(data);
  }
}
```

### Data Processing Architecture
```javascript
// Data processing architecture
class DataProcessing {
  constructor() {
    this.validators = new Map();
    this.coders = new Map();
    this.derivers = new Map();
  }

  async process(data) {
    // Validate data
    const validatedData = await this.validate(data);
    
    // Code medical terms
    const codedData = await this.code(validatedData);
    
    // Derive variables
    const derivedData = await this.derive(codedData);
    
    return derivedData;
  }

  async validate(data) {
    const validationResults = [];
    
    for (const validator of this.validators.values()) {
      const result = await validator.validate(data);
      validationResults.push(result);
    }
    
    return {
      data,
      validationResults,
      isValid: validationResults.every(r => r.isValid),
    };
  }

  async code(data) {
    const codedData = { ...data };
    
    for (const coder of this.coders.values()) {
      codedData.results = await coder.code(codedData.results);
    }
    
    return codedData;
  }

  async derive(data) {
    const derivedData = { ...data };
    
    for (const deriver of this.derivers.values()) {
      derivedData.derived = await deriver.derive(derivedData);
    }
    
    return derivedData;
  }
}
```

## Integration Guide

### REDCap Integration
```javascript
// REDCap integration
class REDCapIntegration {
  constructor(config) {
    this.config = config;
    this.client = new REDCapClient(config);
  }

  async exportData(projectId, params = {}) {
    const response = await this.client.post('/api/', {
      token: this.config.token,
      content: 'record',
      format: this.config.export.format,
      type: 'flat',
      csvDelimeter: ',',
      exportSurveyFields: this.config.export.includeSurveyFields,
      exportCheckboxLabels: this.config.export.combineCheckboxes,
      ...params,
    });

    return JSON.parse(response);
  }

  async importData(projectId, data) {
    const response = await this.client.post('/api/', {
      token: this.config.token,
      content: 'record',
      format: 'json',
      type: 'flat',
      data: JSON.stringify(data),
      overwriteBehavior: 'overwrite',
      forceAutoNumber: 'false',
    });

    return response;
  }

  async getMetadata(projectId) {
    const response = await this.client.post('/api/', {
      token: this.config.token,
      content: 'metadata',
      format: 'json',
      exportSurveyFields: 'true',
    });

    return JSON.parse(response);
  }

  async getEvents(projectId) {
    const response = await this.client.post('/api/', {
      token: this.config.token,
      content: 'event',
      format: 'json',
    });

    return JSON.parse(response);
  }
}
```

### CDISC Integration
```javascript
// CDISC integration
class CDISCIntegration {
  constructor(config) {
    this.config = config;
    this.sdtmMapper = new SDTMMapper(config.sdtm);
    this.adamMapper = new ADaMMapper(config.adam);
  }

  async generateSDTM(studyData) {
    const sdtmData = {};
    
    for (const domain of this.config.sdtm.domains) {
      const domainData = await this.sdtmMapper.map(studyData, domain);
      sdtmData[domain] = domainData;
    }
    
    return sdtmData;
  }

  async generateADaM(sdtmData) {
    const adamData = {};
    
    for (const dataset of this.config.adam.datasets) {
      const datasetData = await this.adamMapper.map(sdtmData, dataset);
      adamData[dataset] = datasetData;
    }
    
    return adamData;
  }

  async validateCDISC(data, standard) {
    const validator = this.getValidator(standard);
    return validator.validate(data);
  }

  getValidator(standard) {
    switch (standard) {
      case 'SDTM':
        return new SDTMValidator(this.config.sdtm);
      case 'ADaM':
        return new ADaMValidator(this.config.adam);
      default:
        throw new Error(`Unknown standard: ${standard}`);
    }
  }
}
```

### Data Export Integration
```javascript
// Data export integration
class DataExportIntegration {
  constructor(config) {
    this.config = config;
    this.exporters = new Map();
  }

  async exportData(data, format, options = {}) {
    const exporter = this.exporters.get(format);
    if (!exporter) {
      throw new Error(`Unsupported format: ${format}`);
    }

    return exporter.export(data, options);
  }

  registerExporter(format, exporter) {
    this.exporters.set(format, exporter);
  }
}

// Example exporters
class CSVExporter {
  export(data, options) {
    const { delimiter = ',', includeHeaders = true } = options;
    
    const headers = Object.keys(data[0]);
    const rows = data.map(row => 
      headers.map(header => row[header]).join(delimiter)
    );
    
    if (includeHeaders) {
      rows.unshift(headers.join(delimiter));
    }
    
    return rows.join('\n');
  }
}

class JSONExporter {
  export(data, options) {
    const { pretty = false } = options;
    return pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
  }
}
```

## Performance Optimization

### Query Optimization
```javascript
// Clinical data query optimization
class ClinicalDataOptimizer {
  constructor() {
    this.queryCache = new QueryCache();
    this.indexManager = new IndexManager();
  }

  async optimizeQuery(query) {
    const cacheKey = this.generateCacheKey(query);
    
    // Check cache
    const cached = await this.queryCache.get(cacheKey);
    if (cached) {
      return cached;
    }

    // Optimize query
    const optimized = this.optimizeExecution(query);
    
    // Cache result
    await this.queryCache.set(cacheKey, optimized);
    
    return optimized;
  }

  optimizeExecution(query) {
    // Add indexes
    const indexes = this.indexManager.getIndexes(query.table);
    
    // Optimize joins
    const optimizedJoins = this.optimizeJoins(query.joins);
    
    // Add limit if not present
    const optimizedQuery = {
      ...query,
      joins: optimizedJoins,
      limit: query.limit || 1000,
    };
    
    return optimizedQuery;
  }
}
```

### Caching Strategy
```javascript
// Clinical data caching strategy
class ClinicalDataCache {
  constructor(config) {
    this.config = config;
    this.l1Cache = new L1Cache({ maxSize: 1000, ttl: 60000 });
    this.l2Cache = new L2Cache({ maxSize: 10000, ttl: 300000 });
  }

  async get(key) {
    // Check L1 cache
    let value = await this.l1Cache.get(key);
    if (value) {
      return value;
    }

    // Check L2 cache
    value = await this.l2Cache.get(key);
    if (value) {
      // Promote to L1
      await this.l1Cache.set(key, value);
      return value;
    }

    return null;
  }

  async set(key, value, ttl) {
    // Set in both caches
    await this.l1Cache.set(key, value, ttl);
    await this.l2Cache.set(key, value, ttl);
  }

  async invalidate(key) {
    // Invalidate from both caches
    await this.l1Cache.delete(key);
    await this.l2Cache.delete(key);
  }

  async invalidateByStudy(studyId) {
    // Invalidate all data for a study
    const pattern = `study:${studyId}:*`;
    await this.l1Cache.deleteByPattern(pattern);
    await this.l2Cache.deleteByPattern(pattern);
  }
}
```

### Batch Processing
```javascript
// Batch processing for clinical data
class BatchProcessor {
  constructor(config) {
    this.config = config;
    this.batchSize = config.batchSize || 1000;
  }

  async processBatch(data, processor) {
    const batches = this.createBatches(data);
    const results = [];
    
    for (const batch of batches) {
      const batchResult = await processor(batch);
      results.push(...batchResult);
    }
    
    return results;
  }

  createBatches(data) {
    const batches = [];
    
    for (let i = 0; i < data.length; i += this.batchSize) {
      batches.push(data.slice(i, i + this.batchSize));
    }
    
    return batches;
  }

  async processInParallel(data, processor, concurrency = 5) {
    const batches = this.createBatches(data);
    const results = [];
    
    // Process batches in parallel
    const promises = batches.map(batch => processor(batch));
    const batchResults = await Promise.all(promises);
    
    return batchResults.flat();
  }
}
```

## Security Considerations

### Data Security
```javascript
// Clinical data security
class ClinicalDataSecurity {
  constructor(config) {
    this.config = config;
    this.encryption = new EncryptionService(config.encryption);
    this.auditLogger = new AuditLogger(config.audit);
  }

  async secureData(data) {
    // Encrypt sensitive fields
    const encryptedData = await this.encryptSensitiveFields(data);
    
    // Log access
    await this.auditLogger.logAccess({
      action: 'secure',
      dataType: 'clinical',
      timestamp: new Date(),
    });
    
    return encryptedData;
  }

  async encryptSensitiveFields(data) {
    const sensitiveFields = ['USUBJID', 'SUBJINIT', 'BRTHDTC'];
    const encryptedData = { ...data };
    
    for (const field of sensitiveFields) {
      if (encryptedData[field]) {
        encryptedData[field] = await this.encryption.encrypt(encryptedData[field]);
      }
    }
    
    return encryptedData;
  }

  async accessControl(user, data, action) {
    const allowed = await this.checkPermission(user, data, action);
    
    if (!allowed) {
      await this.auditLogger.logUnauthorizedAccess({
        user,
        action,
        dataType: 'clinical',
        timestamp: new Date(),
      });
      
      throw new Error('Unauthorized access');
    }
    
    return true;
  }
}
```

### Audit Logging
```javascript
// Clinical data audit logging
class ClinicalAuditLogger {
  constructor(config) {
    this.config = config;
    this.auditSink = config.auditSink;
  }

  async logAccess(event) {
    const auditEvent = {
      eventType: 'access',
      timestamp: new Date().toISOString(),
      user: event.user,
      action: event.action,
      dataType: event.dataType,
      recordId: event.recordId,
      details: event.details,
    };

    await this.auditSink.log(auditEvent);
  }

  async logChange(event) {
    const auditEvent = {
      eventType: 'change',
      timestamp: new Date().toISOString(),
      user: event.user,
      action: event.action,
      dataType: event.dataType,
      recordId: event.recordId,
      oldValue: event.oldValue,
      newValue: event.newValue,
      reason: event.reason,
    };

    await this.auditSink.log(auditEvent);
  }

  async logExport(event) {
    const auditEvent = {
      eventType: 'export',
      timestamp: new Date().toISOString(),
      user: event.user,
      dataType: event.dataType,
      format: event.format,
      recordCount: event.recordCount,
      destination: event.destination,
    };

    await this.auditSink.log(auditEvent);
  }
}
```

### Access Control
```javascript
// Clinical data access control
class ClinicalAccessControl {
  constructor(config) {
    this.config = config;
    this.roles = new Map();
    this.permissions = new Map();
  }

  async checkPermission(user, resource, action) {
    const userRoles = await this.getUserRoles(user.id);
    const requiredPermission = `${resource}:${action}`;
    
    for (const role of userRoles) {
      const rolePermissions = this.permissions.get(role) || [];
      if (rolePermissions.includes(requiredPermission)) {
        return true;
      }
    }
    
    return false;
  }

  async getUserRoles(userId) {
    // Get user roles from database
    return ['data_manager']; // Example
  }

  setupRoles() {
    // Data Manager
    this.roles.set('data_manager', {
      name: 'Data Manager',
      permissions: [
        'clinical_data:read',
        'clinical_data:write',
        'clinical_data:export',
        'queries:manage',
      ],
    });

    // Study Coordinator
    this.roles.set('study_coordinator', {
      name: 'Study Coordinator',
      permissions: [
        'clinical_data:read',
        'queries:respond',
      ],
    });

    // Monitor
    this.roles.set('monitor', {
      name: 'Monitor',
      permissions: [
        'clinical_data:read',
        'queries:create',
      ],
    });
  }
}
```

## Troubleshooting Guide

### Common Issues

#### Data Validation Errors
```javascript
// Debugging data validation errors
class DataValidationDebugger {
  constructor() {
    this.validationErrors = [];
  }

  async debugValidation(data, rules) {
    const debugInfo = {
      timestamp: new Date(),
      recordCount: data.length,
      ruleCount: rules.length,
    };

    try {
      // Run validation
      const results = await this.runValidation(data, rules);
      
      debugInfo.errors = results.filter(r => r.severity === 'error');
      debugInfo.warnings = results.filter(r => r.severity === 'warning');
      debugInfo.passed = results.filter(r => r.isValid);

      this.log('Validation debug', debugInfo);
      return debugInfo;
    } catch (error) {
      debugInfo.error = error.message;
      this.log('Validation debug failed', debugInfo);
      throw error;
    }
  }

  async runValidation(data, rules) {
    const results = [];
    
    for (const rule of rules) {
      const result = await this.applyRule(rule, data);
      results.push(result);
    }
    
    return results;
  }

  log(message, data) {
    this.validationErrors.push({
      message,
      data,
      timestamp: new Date(),
    });
  }
}
```

#### CDISC Compliance Issues
```javascript
// Debugging CDISC compliance
class CDISCComplianceDebugger {
  constructor() {
    this.complianceIssues = [];
  }

  async debugCompliance(data, standard) {
    const debugInfo = {
      timestamp: new Date(),
      standard,
      recordCount: data.length,
    };

    try {
      // Check compliance
      const results = await this.checkCompliance(data, standard);
      
      debugInfo.compliant = results.compliant;
      debugInfo.violations = results.violations;
      debugInfo.warnings = results.warnings;

      this.log('Compliance debug', debugInfo);
      return debugInfo;
    } catch (error) {
      debugInfo.error = error.message;
      this.log('Compliance debug failed', debugInfo);
      throw error;
    }
  }

  async checkCompliance(data, standard) {
    // Implement compliance checking
    return {
      compliant: true,
      violations: [],
      warnings: [],
    };
  }

  log(message, data) {
    this.complianceIssues.push({
      message,
      data,
      timestamp: new Date(),
    });
  }
}
```

### Performance Debugging
```javascript
// Performance debugging for clinical data
class ClinicalDataPerformanceDebugger {
  constructor() {
    this.metrics = new Map();
  }

  async measureOperation(name, operation) {
    const start = Date.now();
    const result = await operation();
    const duration = Date.now() - start;

    this.recordMetric(name, duration);
    return result;
  }

  recordMetric(name, duration) {
    if (!this.metrics.has(name)) {
      this.metrics.set(name, {
        count: 0,
        totalDuration: 0,
        maxDuration: 0,
        minDuration: Infinity,
      });
    }

    const metric = this.metrics.get(name);
    metric.count++;
    metric.totalDuration += duration;
    metric.maxDuration = Math.max(metric.maxDuration, duration);
    metric.minDuration = Math.min(metric.minDuration, duration);
  }

  getMetrics() {
    const result = {};
    for (const [name, metric] of this.metrics) {
      result[name] = {
        ...metric,
        averageDuration: metric.totalDuration / metric.count,
      };
    }
    return result;
  }
}
```

## API Reference

### REDCap API
```graphql
# REDCap API types
type REDCapConfig {
  baseUrl: String!
  token: String!
  projectIds: [String!]!
  validation: REDCapValidationConfig!
  export: REDCapExportConfig!
}

type REDCapValidationConfig {
  strictMode: Boolean!
  allowMissingData: Boolean!
  requireDateFormats: Boolean!
}

type REDCapExportConfig {
  format: String!
  includeMetadata: Boolean!
  includeSurveyFields: Boolean!
  combineCheckboxes: Boolean!
}

# REDCap operations
type Query {
  redcapRecords(projectId: ID!, params: REDCapExportParams): JSON
  redcapMetadata(projectId: ID!): JSON
  redcapEvents(projectId: ID!): JSON
}

type Mutation {
  importREDCapRecords(projectId: ID!, data: JSON!): REDCapImportResult!
  generateQueries(projectId: ID!, params: REDCapQueryParams): REDCapQueryResult!
}
```

### CDISC API
```javascript
// CDISC API interface
class CDiscAPI {
  constructor(config) {
    this.config = config;
    this.sdtmMapper = new SDTMMapper(config.sdtm);
    this.adamMapper = new ADaMMapper(config.adam);
  }

  async generateSDTM(studyId, data) {
    const sdtmData = {};
    
    for (const domain of this.config.sdtm.domains) {
      const domainData = await this.sdtmMapper.map(studyId, data, domain);
      sdtmData[domain] = domainData;
    }
    
    return sdtmData;
  }

  async generateADaM(studyId, sdtmData) {
    const adamData = {};
    
    for (const dataset of this.config.adam.datasets) {
      const datasetData = await this.adamMapper.map(studyId, sdtmData, dataset);
      adamData[dataset] = datasetData;
    }
    
    return adamData;
  }

  async validateCDISC(data, standard) {
    const validator = this.getValidator(standard);
    return validator.validate(data);
  }
}
```

## Data Models

### Clinical Data Model
```javascript
// Data model for clinical data
class ClinicalDataModel {
  constructor() {
    this.studies = new Map();
    this.subjects = new Map();
    this.visits = new Map();
    this.forms = new Map();
    this.fields = new Map();
  }

  createStudy(data) {
    const study = {
      id: generateId(),
      ...data,
      status: 'active',
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.studies.set(study.id, study);
    return study;
  }

  createSubject(studyId, data) {
    const subject = {
      id: generateId(),
      studyId,
      ...data,
      status: 'enrolled',
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.subjects.set(subject.id, subject);
    return subject;
  }

  createVisit(subjectId, data) {
    const visit = {
      id: generateId(),
      subjectId,
      ...data,
      status: 'scheduled',
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.visits.set(visit.id, visit);
    return visit;
  }

  createForm(visitId, data) {
    const form = {
      id: generateId(),
      visitId,
      ...data,
      status: 'incomplete',
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.forms.set(form.id, form);
    return form;
  }

  createField(formId, data) {
    const field = {
      id: generateId(),
      formId,
      ...data,
      status: 'empty',
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.fields.set(field.id, field);
    return field;
  }
}
```

### SDTM Data Model
```javascript
// Data model for SDTM data
class SDTMDataModel {
  constructor() {
    this.domains = new Map();
    this.datasets = new Map();
    this.variables = new Map();
  }

  createDomain(name, definition) {
    const domain = {
      name,
      ...definition,
      createdAt: new Date(),
    };

    this.domains.set(name, domain);
    return domain;
  }

  createDataset(domainName, data) {
    const dataset = {
      id: generateId(),
      domainName,
      ...data,
      createdAt: new Date(),
    };

    this.datasets.set(dataset.id, dataset);
    return dataset;
  }

  createVariable(domainName, variableName, definition) {
    const key = `${domainName}:${variableName}`;
    const variable = {
      domainName,
      variableName,
      ...definition,
      createdAt: new Date(),
    };

    this.variables.set(key, variable);
    return variable;
  }

  getDomain(name) {
    return this.domains.get(name);
  }

  getDatasets(domainName) {
    return Array.from(this.datasets.values())
      .filter(dataset => dataset.domainName === domainName);
  }

  getVariables(domainName) {
    return Array.from(this.variables.values())
      .filter(variable => variable.domainName === domainName);
  }
}
```

## Deployment Guide

### Docker Deployment
```dockerfile
# Dockerfile for clinical data management
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV REDCAP_API_TOKEN=your-token
ENV REDCAP_BASE_URL=https://redcap.example.com

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "app.py"]
```

### Kubernetes Deployment
```yaml
# kubernetes/clinical-data-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clinical-data-manager
spec:
  replicas: 3
  selector:
    matchLabels:
      app: clinical-data-manager
  template:
    metadata:
      labels:
        app: clinical-data-manager
    spec:
      containers:
      - name: clinical-data
        image: clinical-data-manager:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDCAP_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: clinical-data-secrets
              key: redcap-api-token
        - name: REDCAP_BASE_URL
          valueFrom:
            configMapKeyRef:
              name: clinical-data-config
              key: redcap-base-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: clinical-data-manager
spec:
  selector:
    app: clinical-data-manager
  ports:
  - name: http
    port: 8000
    targetPort: 8000
  type: ClusterIP
```

## Monitoring & Observability

### Metrics Collection
```javascript
// Clinical data metrics
const promClient = require('prom-client');

const clinicalMetrics = {
  recordsProcessed: new promClient.Counter({
    name: 'clinical_records_processed_total',
    help: 'Total clinical records processed',
    labelNames: ['study', 'domain', 'status'],
  }),

  validationErrors: new promClient.Counter({
    name: 'clinical_validation_errors_total',
    help: 'Total validation errors',
    labelNames: ['study', 'domain', 'error_type'],
  }),

  queryGenerationTime: new promClient.Histogram({
    name: 'clinical_query_generation_seconds',
    help: 'Query generation time',
    labelNames: ['study'],
    buckets: [0.1, 0.5, 1, 5, 10, 30],
  }),

  dataExportSize: new promClient.Histogram({
    name: 'clinical_export_size_bytes',
    help: 'Data export size',
    labelNames: ['study', 'format'],
    buckets: [1000, 10000, 100000, 1000000, 10000000],
  }),
};
```

### Logging Configuration
```javascript
// Structured logging for clinical data
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'clinical-data-manager' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'clinical-data.log' }),
  ],
});

// Clinical data logging
const clinicalLogger = {
  logRecordProcessed(studyId, domain, recordId) {
    logger.info('Record processed', {
      studyId,
      domain,
      recordId,
      timestamp: new Date().toISOString(),
    });
  },

  logValidationError(studyId, domain, error) {
    logger.error('Validation error', {
      studyId,
      domain,
      error: error.message,
      timestamp: new Date().toISOString(),
    });
  },

  logDataExport(studyId, format, recordCount) {
    logger.info('Data exported', {
      studyId,
      format,
      recordCount,
      timestamp: new Date().toISOString(),
    });
  },
};
```

## Testing Strategy

### Unit Testing
```javascript
// Unit tests for clinical data
describe('Clinical Data Management', () => {
  let dataManager;

  beforeEach(() => {
    dataManager = new ClinicalDataManager();
  });

  test('validates clinical data', async () => {
    const data = {
      USUBJID: '001',
      AETERM: 'Headache',
      AESEV: 'MILD',
    };

    const result = await dataManager.validate(data);
    expect(result.isValid).toBe(true);
  });

  test('generates SDTM domains', async () => {
    const studyData = {
      subjects: [
        { id: '001', name: 'John Doe', age: 45 },
      ],
    };

    const sdtmData = await dataManager.generateSDTM(studyData);
    expect(sdtmData.DM).toBeDefined();
  });

  test('creates queries for missing data', async () => {
    const data = {
      USUBJID: '001',
      AETERM: null,
    };

    const queries = await dataManager.generateQueries(data);
    expect(queries.length).toBeGreaterThan(0);
  });
});
```

### Integration Testing
```javascript
// Integration tests for clinical data
describe('Clinical Data Integration', () => {
  test('exports data in CDISC format', async () => {
    const dataManager = new ClinicalDataManager();
    const studyData = await dataManager.getStudyData('123');
    
    const sdtmExport = await dataManager.exportSDTM(studyData);
    expect(sdtmExport).toBeDefined();
    expect(sdtmExport.DM).toBeDefined();
  });

  test('imports data from REDCap', async () => {
    const redcapIntegration = new REDCapIntegration({
      baseUrl: 'https://redcap.example.com',
      token: 'test-token',
    });

    const data = await redcapIntegration.exportData('123');
    expect(data).toBeDefined();
    expect(Array.isArray(data)).toBe(true);
  });
});
```

## Versioning & Migration

### Data Versioning
```javascript
// Clinical data versioning
class ClinicalDataVersioning {
  constructor() {
    this.versions = new Map();
    this.migrations = new Map();
  }

  createVersion(studyId, data) {
    const version = {
      id: generateId(),
      studyId,
      data,
      createdAt: new Date(),
      version: this.getNextVersion(studyId),
    };

    this.versions.set(version.id, version);
    return version;
  }

  getVersion(versionId) {
    return this.versions.get(versionId);
  }

  getVersions(studyId) {
    return Array.from(this.versions.values())
      .filter(version => version.studyId === studyId)
      .sort((a, b) => a.version - b.version);
  }

  migrateData(fromVersion, toVersion, migrationFn) {
    const migration = {
      id: generateId(),
      fromVersion,
      toVersion,
      migrate: migrationFn,
      createdAt: new Date(),
    };

    this.migrations.set(migration.id, migration);
    return migration;
  }
}
```

### Migration Strategies
```javascript
// Migration strategy for clinical data
class ClinicalDataMigration {
  constructor(config) {
    this.config = config;
    this.steps = [];
  }

  async migrate(fromVersion, toVersion) {
    // Analyze changes
    const changes = this.analyzeChanges(fromVersion, toVersion);
    
    // Generate migration steps
    this.steps = this.generateMigrationSteps(changes);
    
    // Execute migration
    for (const step of this.steps) {
      await this.executeStep(step);
    }
    
    return {
      success: true,
      steps: this.steps,
      duration: Date.now() - this.startTime,
    };
  }

  analyzeChanges(fromVersion, toVersion) {
    return {
      addedFields: [],
      removedFields: [],
      modifiedFields: [],
      addedDomains: [],
      removedDomains: [],
    };
  }

  generateMigrationSteps(changes) {
    const steps = [];
    
    // Handle added fields
    for (const field of changes.addedFields) {
      steps.push({
        type: 'add_field',
        field,
        action: 'add',
      });
    }
    
    // Handle removed fields
    for (const field of changes.removedFields) {
      steps.push({
        type: 'remove_field',
        field,
        action: 'remove',
      });
    }
    
    return steps;
  }
}
```

## Glossary

### Clinical Data Terms

- **Clinical Trial**: A research study conducted to evaluate a medical intervention
- **EDC**: Electronic Data Capture system
- **REDCap**: Research Electronic Data Capture
- **CDISC**: Clinical Data Interchange Standards Consortium
- **SDTM**: Study Data Tabulation Model
- **ADaM**: Analysis Data Model
- **ODM**: Operational Data Model
- **MedDRA**: Medical Dictionary for Regulatory Activities
- **WHO Drug**: World Health Organization Drug Dictionary
- **CTCAE**: Common Terminology Criteria for Adverse Events

### Regulatory Terms

- **ICH-GCP**: International Council for Harmonisation - Good Clinical Practice
- **FDA**: Food and Drug Administration
- **EMA**: European Medicines Agency
- **IND**: Investigational New Drug
- **NDA**: New Drug Application
- **CSR**: Clinical Study Report
- **DSMB**: Data Safety Monitoring Board
- **SUSAR**: Suspected Unexpected Serious Adverse Reaction

### Data Management Terms

- **Query**: A question about data quality or completeness
- **Edit Check**: A validation rule applied to data
- **Coding**: Mapping free text to standardized terminology
- **Derivation**: Creating new variables from existing data
- **Data Lock**: The point at which data can no longer be modified
- **Audit Trail**: A record of all changes made to data
- **De-identification**: Removing personally identifiable information
- **Source Data Verification**: Comparing EDC data to source documents

## Changelog

### Version 1.1.0 (2024-01-15)
- Added advanced configuration section
- Added architecture patterns
- Added integration guide
- Added performance optimization techniques
- Added security considerations
- Added troubleshooting guide

### Version 1.0.0 (2024-01-01)
- Initial release
- Clinical trials overview
- REDCap
- CDISC standards
- Data validation

## Contributing Guidelines

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up development environment
4. Run tests: `pytest`
5. Start development server: `python app.py`

### Code Standards
- Follow CDISC standards
- Use Python for new implementations
- Write comprehensive tests
- Update documentation for changes

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Run CDISC validation
4. Update documentation
5. Submit pull request with description
6. Address review feedback

## License

MIT License

Copyright (c) 2024 Clinical Data Management Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
