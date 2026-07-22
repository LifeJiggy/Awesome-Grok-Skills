---
name: ehr-integration
category: health-tech
version: 1.0.0
tags:
  - fhir
  - hl7
  - interoperability
  - ehr
  - health-it
  - smart-on-fhir
  - patient-data
difficulty: advanced
estimated_time: 100 minutes
prerequisites:
  - python-programming
  - rest-api-basics
  - healthcare-data-standards
---

# EHR Integration

Electronic Health Record (EHR) integration enables the seamless exchange of patient data between clinical systems using standardized protocols. HL7 FHIR (Fast Healthcare Interoperability Resources) is the dominant modern standard, with SMART on FHIR providing an app-level authorization framework.

## Core Concepts

### HL7 FHIR
FHIR defines resources (Patient, Observation, Condition, MedicationRequest) as JSON or XML bundles with RESTful CRUD operations. Resources reference each other via canonical URLs and support search, validation, and versioning.

### SMART on FHIR
An OAuth 2.0-based authorization framework that lets third-party apps securely access EHR data. Launch modes: EHR-launch (initiated from within the EHR) and standalone-launch (independent app startup).

### Interoperability Levels
1. **Foundational**: Network connectivity, security
2. **Structural**: Standardized message formats (HL7 v2, FHIR)
3. **Semantic**: Shared vocabulary (SNOMED CT, LOINC, RxNorm)
4. **Organizational**: Governance, trust agreements, policies

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  EHR Integration Architecture            │
├────────────────┬────────────────┬───────────────────────┤
│   Client Apps  │  API Gateway   │   EHR Systems         │
│                │                │                       │
│ • SMART Apps   │ • FHIR Server  │ • Epic                │
│ • Dashboards   │ • Auth (OAuth) │ • Cerner              │
│ • Mobile Apps  │ • Rate Limiter │ • Allscripts          │
│ • Lab Systems  │ • Validator    │ • MEDITECH            │
└────────────────┴────────────────┴───────────────────────┘
```

## Key FHIR Resources

| Resource | Purpose | Example Use |
|----------|---------|-------------|
| Patient | Demographics & identifiers | Patient demographics lookup |
| Observation | Vital signs, lab results | Blood pressure trends |
| Condition | Diagnoses | Problem list management |
| MedicationRequest | Prescriptions | e-Prescribing |
| Encounter | Visits and admissions | Visit history |
| DiagnosticReport | Radiology/pathology | Imaging results |
| AllergyIntolerance | Allergies | Drug allergy checks |
| Procedure | Clinical procedures | Surgical history |

## SMART on FHIR Scopes

| Scope | Access Level | Use Case |
|-------|-------------|----------|
| `patient/*.read` | Read all patient data | Full clinical viewer |
| `patient/Observation.read` | Read observations only | Vitals dashboard |
| `user/Patient.read` | User-level patient access | Provider tools |
| `launch` | EHR launch context | In-context app launch |
| `online_access` | Maintain session | Long-running analyses |

## Common Pitfalls

1. **Pagination**: FHIR pages may contain 10 results; always handle `next` links
2. **Versioning**: Resource versions change — use `If-None-Match` headers
3. **Terminology binding**: Different systems code the same concept differently
4. **Bulk data**: Large datasets require FHIR Bulk Data Access ($export)
5. **Consent**: Patient consent restrictions may limit data availability
6. **Edge servers**: EHR sandbox ≠ production; test against both

## Data Standards

| Standard | Purpose | Maintainer |
|----------|---------|------------|
| SNOMED CT | Clinical terminology | SNOMED International |
| LOINC | Lab observations | Regenstrief Institute |
| RxNorm | Medications | NLM |
| ICD-10-CM | Diagnoses | WHO/CMS |
| CPT | Procedures | AMA |
| UCUM | Units of measure | Regenstrief Institute |

## References

- HL7 FHIR Specification: https://www.hl7.org/fhir/
- SMART on FHIR: https://www.smart-on-fhir.org/
- ONC Interoperability Standards: https://www.healthit.gov/topic/standards
- US Core Implementation Guide: http://hl7.org/fhir/us/core/

## Advanced Configuration

### FHIR Server Configuration
```javascript
// Advanced FHIR server configuration
const fhirConfig = {
  baseUrl: 'https://fhir.example.com',
  version: '4.0.1',
  auth: {
    type: 'oauth2',
    clientId: process.env.FHIR_CLIENT_ID,
    clientSecret: process.env.FHIR_CLIENT_SECRET,
    tokenUrl: 'https://auth.example.com/token',
    scopes: ['patient/*.read', 'user/*.read'],
  },
  pagination: {
    defaultPageSize: 20,
    maxPageSize: 100,
    includeTotal: true,
  },
  validation: {
    enabled: true,
    strictMode: false,
    profile: 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient',
  },
  caching: {
    enabled: true,
    ttl: 300000, // 5 minutes
    maxSize: 1000,
  },
  retry: {
    maxAttempts: 3,
    initialDelay: 1000,
    maxDelay: 5000,
    backoff: 'exponential',
  },
};
```

### SMART on FHIR Configuration
```javascript
// SMART on FHIR configuration
const smartConfig = {
  clientId: process.env.SMART_CLIENT_ID,
  redirectUri: process.env.SMART_REDIRECT_URI,
  scope: 'launch patient/Patient.read patient/Observation.read',
  iss: process.env.SMART_ISS,
  state: generateRandomState(),
  nonce: generateRandomNonce(),
  launchContext: {
    patient: true,
    encounter: true,
    location: true,
  },
  tokenStorage: {
    type: 'sessionStorage',
    ttl: 3600000, // 1 hour
  },
};
```

### Interoperability Configuration
```javascript
// Interoperability configuration
const interoperabilityConfig = {
  terminology: {
    primary: 'SNOMED CT',
    supported: ['SNOMED CT', 'LOINC', 'RxNorm', 'ICD-10-CM'],
    validation: {
      strict: false,
      fallback: true,
    },
  },
  messaging: {
    format: 'FHIR',
    version: '4.0.1',
    compression: 'gzip',
    encryption: 'TLS 1.3',
  },
  security: {
    authentication: 'OAuth2',
    authorization: 'SMART',
    encryption: 'AES-256',
    auditLogging: true,
  },
};
```

## Architecture Patterns

### FHIR Integration Architecture
```javascript
// FHIR integration architecture
class FHIRIntegrationArchitect {
  constructor(config) {
    this.config = config;
    this.client = new FHIRClient(config.baseUrl);
    this.cache = new FHIRCache(config.cache);
    this.validator = new FHIRValidator(config.validation);
  }

  async initialize() {
    // Validate server capabilities
    await this.validateServer();
    
    // Load SMART configuration
    await this.loadSMARTConfig();
    
    // Initialize cache
    await this.initializeCache();
    
    return this;
  }

  async validateServer() {
    const capabilities = await this.client.getCapabilities();
    
    if (!this.validateCapabilities(capabilities)) {
      throw new Error('Server capabilities do not meet requirements');
    }
    
    return capabilities;
  }

  async loadSMARTConfig() {
    const smartConfig = await this.client.getSMARTConfig();
    this.config.smart = smartConfig;
    return smartConfig;
  }

  async initializeCache() {
    await this.cache.initialize();
    return this.cache;
  }
}
```

### Patient Data Architecture
```javascript
// Patient data architecture
class PatientDataArchitecture {
  constructor() {
    this.repositories = new Map();
    this.services = new Map();
    this.mappers = new Map();
  }

  async getPatient(patientId) {
    // Check repository
    const patient = await this.repositories.get('patient').get(patientId);
    if (patient) {
      return patient;
    }

    // Fetch from FHIR server
    const fhirPatient = await this.fetchFHIRPatient(patientId);
    
    // Map to internal model
    const mappedPatient = this.mapToInternalModel(fhirPatient);
    
    // Cache result
    await this.repositories.get('patient').set(patientId, mappedPatient);
    
    return mappedPatient;
  }

  async fetchFHIRPatient(patientId) {
    const response = await fetch(`${this.config.fhirBaseUrl}/Patient/${patientId}`, {
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Accept': 'application/fhir+json',
      },
    });
    
    return response.json();
  }

  mapToInternalModel(fhirPatient) {
    const mapper = this.mappers.get('patient');
    return mapper.map(fhirPatient);
  }
}
```

### Clinical Data Architecture
```javascript
// Clinical data architecture
class ClinicalDataArchitecture {
  constructor() {
    this.observationService = new ObservationService();
    this.conditionService = new ConditionService();
    this.medicationService = new MedicationService();
  }

  async getPatientSummary(patientId) {
    const [observations, conditions, medications] = await Promise.all([
      this.observationService.getByPatient(patientId),
      this.conditionService.getByPatient(patientId),
      this.medicationService.getByPatient(patientId),
    ]);

    return {
      patientId,
      observations: this.summarizeObservations(observations),
      conditions: this.summarizeConditions(conditions),
      medications: this.summarizeMedications(medications),
      lastUpdated: new Date(),
    };
  }

  summarizeObservations(observations) {
    return observations.map(obs => ({
      code: obs.code.coding[0]?.code,
      display: obs.code.coding[0]?.display,
      value: obs.valueQuantity?.value,
      unit: obs.valueQuantity?.unit,
      effectiveDateTime: obs.effectiveDateTime,
    }));
  }

  summarizeConditions(conditions) {
    return conditions.map(cond => ({
      code: cond.code.coding[0]?.code,
      display: cond.code.coding[0]?.display,
      clinicalStatus: cond.clinicalStatus?.coding[0]?.code,
      onsetDateTime: cond.onsetDateTime,
    }));
  }

  summarizeMedications(medications) {
    return medications.map(med => ({
      code: med.medicationCodeableConcept?.coding[0]?.code,
      display: med.medicationCodeableConcept?.coding[0]?.display,
      status: med.status,
      authoredOn: med.authoredOn,
    }));
  }
}
```

## Integration Guide

### FHIR Client Integration
```javascript
// FHIR client integration
const FHIRClient = require('fhir-kit-client');

class EHRIntegration {
  constructor(config) {
    this.client = new FHIRClient({
      baseUrl: config.fhirBaseUrl,
      customHeaders: {
        'Authorization': `Bearer ${config.accessToken}`,
        'Accept': 'application/fhir+json',
      },
    });
  }

  async getPatient(patientId) {
    return this.client.read({
      resourceType: 'Patient',
      id: patientId,
    });
  }

  async searchPatients(params) {
    return this.client.search({
      resourceType: 'Patient',
      params: {
        family: params.lastName,
        given: params.firstName,
        birthdate: params.birthDate,
      },
    });
  }

  async getObservations(patientId) {
    return this.client.search({
      resourceType: 'Observation',
      params: {
        patient: patientId,
        _sort: '-date',
        _count: 100,
      },
    });
  }

  async createObservation(observation) {
    return this.client.create({
      resourceType: 'Observation',
      resource: observation,
    });
  }
}
```

### SMART on FHIR Launch Integration
```javascript
// SMART on FHIR launch integration
class SMARTLaunch {
  constructor(config) {
    this.config = config;
    this.tokenStorage = new TokenStorage();
  }

  async launchFromEHR() {
    // Get launch parameters
    const launchParams = this.getLaunchParams();
    
    // Get authorization endpoint
    const authEndpoint = await this.getAuthorizationEndpoint(launchParams.iss);
    
    // Redirect to authorization
    const authUrl = this.buildAuthorizationUrl(authEndpoint, launchParams);
    window.location.href = authUrl;
  }

  async launchStandalone() {
    // Build authorization URL for standalone launch
    const authUrl = this.buildAuthorizationUrl(
      this.config.authorizationEndpoint,
      {
        client_id: this.config.clientId,
        redirect_uri: this.config.redirectUri,
        scope: this.config.scope,
        state: this.config.state,
      }
    );
    
    window.location.href = authUrl;
  }

  async handleCallback() {
    // Get authorization code
    const code = this.getAuthorizationCode();
    
    // Exchange code for token
    const token = await this.exchangeCodeForToken(code);
    
    // Store token
    await this.tokenStorage.store(token);
    
    // Get launch context
    const launchContext = await this.getLaunchContext(token);
    
    return { token, launchContext };
  }

  buildAuthorizationUrl(endpoint, params) {
    const url = new URL(endpoint);
    
    for (const [key, value] of Object.entries(params)) {
      url.searchParams.append(key, value);
    }
    
    return url.toString();
  }
}
```

### Bulk Data Access Integration
```javascript
// Bulk data access integration
class BulkDataAccess {
  constructor(config) {
    this.config = config;
    this.client = new FHIRClient(config.fhirBaseUrl);
  }

  async initiateExport(patientId) {
    const response = await fetch(`${this.config.fhirBaseUrl}/Patient/${patientId}/$export`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${this.config.accessToken}`,
        'Accept': 'application/fhir+json',
        'Prefer': 'respond-async',
      },
    });

    if (response.status === 202) {
      const contentLocation = response.headers.get('Content-Location');
      return { status: 'pending', contentLocation };
    }

    return response.json();
  }

  async checkExportStatus(contentLocation) {
    const response = await fetch(contentLocation, {
      headers: {
        'Authorization': `Bearer ${this.config.accessToken}`,
      },
    });

    if (response.status === 200) {
      return { status: 'complete', data: await response.json() };
    }

    if (response.status === 202) {
      return { status: 'pending' };
    }

    throw new Error('Export failed');
  }

  async downloadExportFile(fileUrl) {
    const response = await fetch(fileUrl, {
      headers: {
        'Authorization': `Bearer ${this.config.accessToken}`,
      },
    });

    return response.json();
  }
}
```

## Performance Optimization

### Query Optimization
```javascript
// FHIR query optimization
class FHIROptimizer {
  constructor(client) {
    this.client = client;
    this.cache = new FHIRCache();
  }

  async optimizeQuery(query) {
    // Analyze query
    const analysis = this.analyzeQuery(query);
    
    // Optimize based on analysis
    const optimized = this.optimizeExecution(analysis);
    
    return optimized;
  }

  analyzeQuery(query) {
    return {
      resourceType: query.resourceType,
      params: query.params,
      complexity: this.calculateComplexity(query),
      estimatedCost: this.estimateCost(query),
    };
  }

  optimizeExecution(analysis) {
    const optimizations = [];
    
    // Add _count parameter for large result sets
    if (!analysis.params._count) {
      optimizations.push({ key: '_count', value: '100' });
    }
    
    // Add _sort parameter for predictable ordering
    if (!analysis.params._sort) {
      optimizations.push({ key: '_sort', value: '-_lastUpdated' });
    }
    
    // Add _elements parameter to reduce payload
    if (analysis.resourceType === 'Patient') {
      optimizations.push({ key: '_elements', value: 'name,birthDate,gender' });
    }
    
    return {
      ...analysis,
      optimizations,
    };
  }
}
```

### Caching Strategy
```javascript
// FHIR caching strategy
class FHIRCacheStrategy {
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

  async invalidateByPattern(pattern) {
    // Invalidate matching keys
    await this.l1Cache.deleteByPattern(pattern);
    await this.l2Cache.deleteByPattern(pattern);
  }
}
```

### Connection Pooling
```javascript
// FHIR connection pooling
class FHIRConnectionPool {
  constructor(config) {
    this.config = config;
    this.connections = new Map();
    this.maxConnections = config.maxConnections || 10;
  }

  async getConnection() {
    // Find available connection
    for (const [id, connection] of this.connections) {
      if (connection.available) {
        connection.available = false;
        return connection;
      }
    }

    // Create new connection if under limit
    if (this.connections.size < this.maxConnections) {
      return this.createConnection();
    }

    // Wait for available connection
    return this.waitForConnection();
  }

  async releaseConnection(connection) {
    connection.available = true;
    connection.lastUsed = Date.now();
  }

  createConnection() {
    const id = generateId();
    const connection = {
      id,
      client: new FHIRClient(this.config),
      available: false,
      createdAt: Date.now(),
      lastUsed: Date.now(),
    };

    this.connections.set(id, connection);
    return connection;
  }

  async waitForConnection() {
    return new Promise((resolve) => {
      const check = () => {
        for (const [id, connection] of this.connections) {
          if (connection.available) {
            connection.available = false;
            resolve(connection);
            return;
          }
        }
        setTimeout(check, 100);
      };
      check();
    });
  }
}
```

## Security Considerations

### Authentication
```javascript
// FHIR authentication
class FHIRAuth {
  constructor(config) {
    this.config = config;
    this.tokenManager = new TokenManager(config);
  }

  async authenticate(request) {
    const token = this.extractToken(request);
    if (!token) {
      throw new AuthenticationError('No token provided');
    }

    const validatedToken = await this.validateToken(token);
    if (!validatedToken) {
      throw new AuthenticationError('Invalid token');
    }

    return validatedToken;
  }

  extractToken(request) {
    const authHeader = request.headers.authorization;
    if (authHeader?.startsWith('Bearer ')) {
      return authHeader.slice(7);
    }
    return null;
  }

  async validateToken(token) {
    try {
      const decoded = await this.verifyToken(token);
      return decoded;
    } catch (error) {
      return null;
    }
  }

  async verifyToken(token) {
    // Verify token signature
    const decoded = jwt.verify(token, this.config.secret);
    
    // Check expiration
    if (decoded.exp < Date.now() / 1000) {
      throw new Error('Token expired');
    }
    
    // Check audience
    if (decoded.aud !== this.config.audience) {
      throw new Error('Invalid audience');
    }
    
    return decoded;
  }
}
```

### Authorization
```javascript
// FHIR authorization
class FHIRAuthorization {
  constructor(config) {
    this.config = config;
    this.policies = new Map();
  }

  async authorize(user, resource, operation) {
    const policy = this.getPolicy(resource, operation);
    if (!policy) {
      return true; // No policy = allow
    }

    return policy(user, resource);
  }

  getPolicy(resource, operation) {
    const key = `${resource}:${operation}`;
    return this.policies.get(key);
  }

  registerPolicy(resource, operation, policyFn) {
    const key = `${resource}:${operation}`;
    this.policies.set(key, policyFn);
  }

  // Example policies
  setupPolicies() {
    // Patient read policy
    this.registerPolicy('Patient', 'read', (user, patient) => {
      // Users can only read their own patient record
      return user.patientId === patient.id;
    });

    // Observation read policy
    this.registerPolicy('Observation', 'read', (user, observation) => {
      // Providers can read observations for their patients
      return user.role === 'provider' && 
             user.patientIds.includes(observation.subject.reference.split('/')[1]);
    });
  }
}
```

### Audit Logging
```javascript
// FHIR audit logging
class FHIRAuditLogger {
  constructor(config) {
    this.config = config;
    this.auditSink = config.auditSink;
  }

  async logAccess(user, resource, operation, result) {
    const auditEvent = {
      resourceType: 'AuditEvent',
      type: {
        system: 'http://dicom.nema.org/resources/ontology/DCM',
        code: operation === 'read' ? '110110' : '110111',
        display: operation === 'read' ? 'Patient Record' : 'Patient Record Modification',
      },
      actor: {
        who: {
          reference: `Practitioner/${user.id}`,
        },
      },
      entity: [
        {
          what: {
            reference: `${resource.resourceType}/${resource.id}`,
          },
          type: {
            system: 'http://terminology.hl7.org/CodeSystem/audit-entity-type',
            code: '2', // System
            display: 'System',
          },
        },
      ],
      outcome: result.success ? '0' : '8', // 0 = Success, 8 = Error
      outcomeDesc: result.success ? 'Success' : result.error,
      recorded: new Date().toISOString(),
    };

    await this.auditSink.log(auditEvent);
  }
}
```

## Troubleshooting Guide

### Common Issues

#### Connection Problems
```javascript
// Debugging FHIR connection issues
class FHIRConnectionDebugger {
  constructor() {
    this.logs = [];
  }

  async debugConnection(fhirBaseUrl, token) {
    const debugInfo = {
      timestamp: new Date(),
      fhirBaseUrl,
      hasToken: !!token,
    };

    try {
      // Test base URL
      const response = await fetch(fhirBaseUrl, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/fhir+json',
        },
      });

      debugInfo.status = response.status;
      debugInfo.headers = Object.fromEntries(response.headers.entries());

      // Test capabilities
      const capabilities = await fetch(`${fhirBaseUrl}/metadata`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/fhir+json',
        },
      });

      debugInfo.capabilitiesStatus = capabilities.status;
      debugInfo.capabilities = await capabilities.json();

      this.log('Connection debug', debugInfo);
      return debugInfo;
    } catch (error) {
      debugInfo.error = error.message;
      this.log('Connection debug failed', debugInfo);
      throw error;
    }
  }

  log(message, data) {
    this.logs.push({
      message,
      data,
      timestamp: new Date(),
    });
  }
}
```

#### Data Validation Errors
```javascript
// Debugging FHIR data validation
class FHIRValidationDebugger {
  constructor() {
    this.validationErrors = [];
  }

  async debugValidation(resource, profile) {
    const debugInfo = {
      timestamp: new Date(),
      resourceType: resource.resourceType,
      profile,
    };

    try {
      // Validate resource
      const validation = await this.validateResource(resource, profile);
      
      debugInfo.isValid = validation.isValid;
      debugInfo.errors = validation.errors;
      debugInfo.warnings = validation.warnings;

      this.log('Validation debug', debugInfo);
      return debugInfo;
    } catch (error) {
      debugInfo.error = error.message;
      this.log('Validation debug failed', debugInfo);
      throw error;
    }
  }

  async validateResource(resource, profile) {
    // Implement validation logic
    return {
      isValid: true,
      errors: [],
      warnings: [],
    };
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

### Performance Debugging
```javascript
// Performance debugging for FHIR
class FHIRPerformanceDebugger {
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

### FHIR API
```graphql
# FHIR API types
type FHIRConfig {
  baseUrl: String!
  version: String!
  auth: FHIRAuthConfig!
  pagination: PaginationConfig!
  validation: ValidationConfig!
}

type FHIRAuthConfig {
  type: String!
  clientId: String!
  clientSecret: String
  tokenUrl: String!
  scopes: [String!]!
}

type PaginationConfig {
  defaultPageSize: Int!
  maxPageSize: Int!
  includeTotal: Boolean!
}

type ValidationConfig {
  enabled: Boolean!
  strictMode: Boolean!
  profile: String
}

# FHIR operations
type Query {
  fhirPatient(id: ID!): FHIRPatient
  fhirPatients(params: FHIRSearchParams): FHIRPatientConnection!
  fhirObservations(patientId: ID!, params: FHIRSearchParams): FHIRObservationConnection!
  fhirConditions(patientId: ID!, params: FHIRSearchParams): FHIRConditionConnection!
}

type Mutation {
  createFHIRResource(input: CreateFHIRResourceInput!): FHIRResource!
  updateFHIRResource(id: ID!, input: UpdateFHIRResourceInput!): FHIRResource!
  deleteFHIRResource(id: ID!): Boolean!
}
```

### SMART on FHIR API
```javascript
// SMART on FHIR API interface
class SMARTAPI {
  constructor(config) {
    this.config = config;
    this.auth = new SMARTAuth(config);
    this.client = new FHIRClient(config.fhirBaseUrl);
  }

  async launch() {
    // Determine launch type
    const isEHRLaunch = this.isEHRLaunch();
    
    if (isEHRLaunch) {
      return this.launchFromEHR();
    } else {
      return this.launchStandalone();
    }
  }

  async getPatientContext() {
    const token = await this.auth.getToken();
    const patientId = token.patient;
    
    if (!patientId) {
      return null;
    }

    const patient = await this.client.read({
      resourceType: 'Patient',
      id: patientId,
    });

    return {
      patientId,
      patient,
      encounterId: token.encounter,
    };
  }

  async getScopes() {
    const token = await this.auth.getToken();
    return token.scope.split(' ');
  }
}
```

## Data Models

### FHIR Resource Data Model
```javascript
// Data model for FHIR resources
class FHIRResourceModel {
  constructor() {
    this.resources = new Map();
    this.versions = new Map();
  }

  createResource(resourceType, data) {
    const resource = {
      id: generateId(),
      resourceType,
      ...data,
      meta: {
        versionId: '1',
        lastUpdated: new Date().toISOString(),
      },
    };

    this.resources.set(resource.id, resource);
    this.versions.set(resource.id, [resource]);
    
    return resource;
  }

  updateResource(id, data) {
    const resource = this.resources.get(id);
    if (!resource) {
      return null;
    }

    const updatedResource = {
      ...resource,
      ...data,
      meta: {
        ...resource.meta,
        versionId: String(parseInt(resource.meta.versionId) + 1),
        lastUpdated: new Date().toISOString(),
      },
    };

    this.resources.set(id, updatedResource);
    
    // Add to versions
    const versions = this.versions.get(id) || [];
    versions.push(updatedResource);
    this.versions.set(id, versions);
    
    return updatedResource;
  }

  deleteResource(id) {
    return this.resources.delete(id);
  }

  getResource(id) {
    return this.resources.get(id);
  }

  getVersions(id) {
    return this.versions.get(id) || [];
  }
}
```

### Patient Data Model
```javascript
// Data model for patient data
class PatientDataModel {
  constructor() {
    this.patients = new Map();
    this.observations = new Map();
    this.conditions = new Map();
    this.medications = new Map();
  }

  createPatient(data) {
    const patient = {
      id: generateId(),
      resourceType: 'Patient',
      ...data,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.patients.set(patient.id, patient);
    return patient;
  }

  addObservation(patientId, observation) {
    const key = `${patientId}:${observation.id}`;
    this.observations.set(key, {
      patientId,
      ...observation,
      createdAt: new Date(),
    });
  }

  addCondition(patientId, condition) {
    const key = `${patientId}:${condition.id}`;
    this.conditions.set(key, {
      patientId,
      ...condition,
      createdAt: new Date(),
    });
  }

  addMedication(patientId, medication) {
    const key = `${patientId}:${medication.id}`;
    this.medications.set(key, {
      patientId,
      ...medication,
      createdAt: new Date(),
    });
  }

  getPatientObservations(patientId) {
    return Array.from(this.observations.values())
      .filter(obs => obs.patientId === patientId);
  }

  getPatientConditions(patientId) {
    return Array.from(this.conditions.values())
      .filter(cond => cond.patientId === patientId);
  }

  getPatientMedications(patientId) {
    return Array.from(this.medications.values())
      .filter(med => med.patientId === patientId);
  }
}
```

## Deployment Guide

### Docker Deployment
```dockerfile
# Dockerfile for EHR integration service
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV FHIR_BASE_URL=https://fhir.example.com
ENV FHIR_CLIENT_ID=your-client-id
ENV FHIR_CLIENT_SECRET=your-client-secret

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["node", "server.js"]
```

### Kubernetes Deployment
```yaml
# kubernetes/ehr-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ehr-integration
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ehr-integration
  template:
    metadata:
      labels:
        app: ehr-integration
    spec:
      containers:
      - name: ehr
        image: ehr-integration:latest
        ports:
        - containerPort: 3000
        env:
        - name: FHIR_BASE_URL
          valueFrom:
            configMapKeyRef:
              name: ehr-config
              key: fhir-base-url
        - name: FHIR_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: ehr-secrets
              key: fhir-client-id
        - name: FHIR_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: ehr-secrets
              key: fhir-client-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ehr-integration
spec:
  selector:
    app: ehr-integration
  ports:
  - name: http
    port: 3000
    targetPort: 3000
  type: ClusterIP
```

## Monitoring & Observability

### Metrics Collection
```javascript
// FHIR metrics collection
const promClient = require('prom-client');

const fhirMetrics = {
  requests: new promClient.Counter({
    name: 'fhir_requests_total',
    help: 'Total FHIR requests',
    labelNames: ['resource_type', 'operation', 'status'],
  }),

  latency: new promClient.Histogram({
    name: 'fhir_request_duration_seconds',
    help: 'FHIR request latency',
    labelNames: ['resource_type', 'operation'],
    buckets: [0.1, 0.5, 1, 5, 10, 30],
  }),

  errors: new promClient.Counter({
    name: 'fhir_errors_total',
    help: 'Total FHIR errors',
    labelNames: ['resource_type', 'error_code'],
  }),

  validation: new promClient.Counter({
    name: 'fhir_validation_total',
    help: 'FHIR validation attempts',
    labelNames: ['resource_type', 'valid'],
  }),
};
```

### Logging Configuration
```javascript
// Structured logging for FHIR
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'ehr-integration' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'ehr.log' }),
  ],
});

// FHIR request logging
const fhirRequestLogger = {
  logRequest(resourceType, operation, params) {
    logger.info('FHIR request', {
      resourceType,
      operation,
      params,
      timestamp: new Date().toISOString(),
    });
  },

  logResponse(resourceType, operation, duration, status) {
    logger.info('FHIR response', {
      resourceType,
      operation,
      duration,
      status,
      timestamp: new Date().toISOString(),
    });
  },

  logError(resourceType, operation, error) {
    logger.error('FHIR error', {
      resourceType,
      operation,
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString(),
    });
  },
};
```

## Testing Strategy

### Unit Testing
```javascript
// Unit tests for FHIR integration
describe('FHIR Integration', () => {
  let fhirClient;

  beforeEach(() => {
    fhirClient = new FHIRClient({
      baseUrl: 'https://fhir.example.com',
      accessToken: 'test-token',
    });
  });

  test('fetches patient by id', async () => {
    const patient = await fhirClient.getPatient('123');
    expect(patient).toBeDefined();
    expect(patient.resourceType).toBe('Patient');
  });

  test('searches patients', async () => {
    const patients = await fhirClient.searchPatients({
      lastName: 'Doe',
      firstName: 'John',
    });
    expect(patients).toBeDefined();
    expect(Array.isArray(patients.entry)).toBe(true);
  });

  test('fetches observations', async () => {
    const observations = await fhirClient.getObservations('123');
    expect(observations).toBeDefined();
    expect(Array.isArray(observations.entry)).toBe(true);
  });
});
```

### Integration Testing
```javascript
// Integration tests for EHR integration
describe('EHR Integration', () => {
  test('performs SMART on FHIR launch', async () => {
    const smart = new SMARTLaunch({
      clientId: 'test-client',
      redirectUri: 'http://localhost:3000/callback',
      scope: 'launch patient/Patient.read',
    });

    const result = await smart.launchStandalone();
    expect(result).toBeDefined();
  });

  test('gets patient context', async () => {
    const smart = new SMARTAPI({
      fhirBaseUrl: 'https://fhir.example.com',
      clientId: 'test-client',
    });

    const context = await smart.getPatientContext();
    expect(context).toBeDefined();
    expect(context.patientId).toBeDefined();
  });
});
```

## Versioning & Migration

### FHIR Versioning
```javascript
// FHIR versioning strategy
class FHIRVersionManager {
  constructor() {
    this.versions = new Map();
    this.migrations = new Map();
  }

  registerVersion(version, config) {
    this.versions.set(version, {
      config,
      registeredAt: new Date(),
      status: 'active',
    });
  }

  migrateResource(resource, fromVersion, toVersion) {
    const migration = this.migrations.get(`${fromVersion}:${toVersion}`);
    if (!migration) {
      throw new Error(`No migration from ${fromVersion} to ${toVersion}`);
    }

    return migration(resource);
  }

  getActiveVersions() {
    return Array.from(this.versions.entries())
      .filter(([_, info]) => info.status === 'active')
      .map(([version, _]) => version);
  }
}
```

### Migration Strategies
```javascript
// Migration strategy for FHIR resources
class FHIRMigrationStrategy {
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
      addedResources: [],
      removedResources: [],
      modifiedResources: [],
      addedFields: [],
      removedFields: [],
    };
  }

  generateMigrationSteps(changes) {
    const steps = [];
    
    // Handle added resources
    for (const resource of changes.addedResources) {
      steps.push({
        type: 'add_resource',
        resource,
        action: 'add',
      });
    }
    
    // Handle removed resources
    for (const resource of changes.removedResources) {
      steps.push({
        type: 'remove_resource',
        resource,
        action: 'remove',
      });
    }
    
    return steps;
  }
}
```

## Glossary

### FHIR Terms

- **Resource**: A discrete data element in FHIR (e.g., Patient, Observation)
- **Bundle**: A collection of resources
- **Reference**: A link from one resource to another
- **Profile**: A set of constraints on a resource
- **Terminology**: Standardized codes and values
- **Operation**: A predefined action on a resource
- **Capability Statement**: Describes what a FHIR server supports
- **Search Parameter**: Defines how to search for resources

### SMART on FHIR Terms

- **Launch**: Starting a SMART app
- **EHR Launch**: Launching from within an EHR system
- **Standalone Launch**: Launching independently
- **Scope**: Permission to access specific data
- **Token**: Authorization credential
- **Patient Context**: The patient whose data is being accessed
- **Encounter Context**: The current clinical encounter
- **Launch Context**: Additional context provided during launch

### Interoperability Terms

- **HL7**: Health Level Seven International
- **FHIR**: Fast Healthcare Interoperability Resources
- **SMART**: Substitutable Medical Applications, Reusable Technologies
- **ONC**: Office of the National Coordinator for Health IT
- **USCDI**: United States Core Data for Interoperability
- **CDS**: Clinical Decision Support
- **CQM**: Clinical Quality Measures
- **eCR**: Electronic Case Reporting

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
- HL7 FHIR overview
- SMART on FHIR
- Interoperability levels
- Common pitfalls

## Contributing Guidelines

### Development Setup
1. Clone the repository
2. Install dependencies: `npm install`
3. Set up development environment
4. Run tests: `npm test`
5. Start development server: `npm run dev`

### Code Standards
- Follow FHIR specification
- Use TypeScript for new implementations
- Write comprehensive tests
- Update documentation for changes

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Run FHIR validation
4. Update documentation
5. Submit pull request with description
6. Address review feedback

## License

MIT License

Copyright (c) 2024 EHR Integration Team

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
