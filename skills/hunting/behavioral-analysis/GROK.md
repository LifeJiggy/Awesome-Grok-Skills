---
name: "behavioral-analysis"
category: "hunting"
version: "2.0.0"
tags: ["hunting", "behavioral", "anomaly-detection", "profiling", "baselines"]
description: "Behavioral pattern analysis for threat detection and anomaly identification"
---

# Behavioral Analysis

## Overview

The Behavioral Analysis module provides advanced techniques for detecting threats through the analysis of behavioral patterns rather than static indicators. It focuses on identifying deviations from established baselines, detecting anomalous user and system behaviors, and profiling adversary tactics, techniques, and procedures (TTPs) through observed activity. This module is critical for detecting zero-day attacks, insider threats, and advanced persistent threats that evade signature-based detection.

## Core Capabilities

- **Baseline Establishment**: Create behavioral baselines for users, systems, and network segments
- **Anomaly Detection**: Identify deviations from baselines using statistical and ML-based methods
- **User and Entity Behavior Analytics (UEBA)**: Profile normal user behavior and detect anomalies
- **Process Behavioral Analysis**: Monitor and analyze process execution patterns
- **Network Traffic Analysis**: Detect anomalous network flows, DNS queries, and connections
- **File System Behavioral Monitoring**: Track file access patterns, modifications, and deletions
- **Temporal Pattern Analysis**: Identify time-based behavioral anomalies
- **Behavioral Correlation**: Link related anomalous activities across multiple data sources

## Usage Examples

### Baseline Creation and Monitoring

```python
from behavioral_analysis import BehavioralEngine, BaselineType, DataCollector

engine = BehavioralEngine(window_days=30, sensitivity=0.8)

# Collect behavioral data
collector = DataCollector(sources=["process_logs", "network_flows", "auth_logs"])
data = collector.collect(hours=24)

# Create baselines
engine.create_baseline(
    entity_id="user-jsmith",
    baseline_type=BaselineType.USER_LOGIN,
    data=data.login_events
)

engine.create_baseline(
    entity_id="server-web-01",
    baseline_type=BaselineType.PROCESS_EXECUTION,
    data=data.process_events
)

# Detect anomalies
anomalies = engine.detect_anomalies(data)
for anomaly in anomalies:
    print(f"Anomaly detected: {anomaly.description}")
    print(f"  Entity: {anomaly.entity_id}")
    print(f"  Severity: {anomaly.severity}")
    print(f"  Confidence: {anomaly.confidence}%")
```

### User Behavior Profiling

```python
from behavioral_analysis import UserProfiler, BehaviorDimension

profiler = UserProfiler(learning_period_days=90)

# Build user profile
profile = profiler.build_profile(
    user_id="jsmith",
    dimensions=[
        BehaviorDimension.LOGIN_TIMES,
        BehaviorDimension.ACCESS_PATTERNS,
        BehaviorDimension.DATA_TRANSFER,
        BehaviorDimension.APPLICATION_USAGE,
    ]
)

print(f"User profile for {profile.user_id}:")
print(f"  Typical login window: {profile.typical_login_start} - {profile.typical_login_end}")
print(f"  Average session duration: {profile.avg_session_hours:.1f} hours")
print(f"  Most accessed resources: {profile.top_resources[:5]}")
print(f"  Anomaly score baseline: {profile.baseline_anomaly_score:.2f}")

# Score current activity
current_score = profiler.score_activity(
    user_id="jsmith",
    activity={
        "login_time": "03:45",  # Unusual time
        "source_ip": "198.51.100.99",  # New location
        "accessed_files": ["confidential_report.pdf"],
    }
)
print(f"  Current anomaly score: {current_score:.2f} (baseline: {profile.baseline_anomaly_score:.2f})")
```

### Process Behavior Analysis

```python
from behavioral_analysis import ProcessAnalyzer, ProcessBehavior

analyzer = ProcessAnalyzer()

# Analyze process behavior
behavior = analyzer.analyze(
    process_name="powershell.exe",
    command_line="powershell.exe -enc SQBmACgA...",
    parent_process="winword.exe",
    pid=4532,
)

print(f"Process Analysis:")
print(f"  Risk Score: {behavior.risk_score}")
print(f"  Indicators: {behavior.indicators}")
print(f"  Recommended Action: {behavior.recommended_action}")

if behavior.risk_score > 80:
    print("  HIGH RISK: Possible exploitation detected")
    analyzer.trigger_alert(behavior, priority="critical")
```

### Network Behavior Analysis

```python
from behavioral_analysis import NetworkBehaviorAnalyzer, Flow特征

analyzer = NetworkBehaviorAnalyzer()

# Analyze network flow
flow特征 = analyzer.analyze_flow(
    src_ip="10.0.1.100",
    dst_ip="198.51.100.42",
    dst_port=443,
    protocol="tcp",
    bytes_sent=1024,
    bytes_received=1048576,
    duration_seconds=300,
)

print(f"Network Flow Analysis:")
print(f"  Risk Level: {flow特征.risk_level}")
print(f"  Anomaly Indicators: {flow特征.anomaly_indicators}")
print(f"  Baseline Deviation: {flow特征.baseline_deviation:.2f}σ")
```

## Best Practices

- **Establish Strong Baselines**: Collect at least 30 days of data before establishing baselines
- **Adjust Sensitivity Gradually**: Start with lower sensitivity and increase based on false positive rates
- **Correlate Multiple Dimensions**: Combine user, process, network, and file system behaviors for better accuracy
- **Consider Context**: Account for legitimate anomalies (maintenance windows, remote work, etc.)
- **Regular Baseline Updates**: Refresh baselines periodically to account for legitimate changes
- **Layer with Other Detection**: Use behavioral analysis alongside signature and rule-based detection
- **Tune for Your Environment**: Customize thresholds and parameters for your organization's normal behavior
- **Document Behavioral Patterns**: Maintain documentation of expected behavioral patterns for different roles

## Advanced Analysis Workflows

### Multi-Dimensional Behavioral Correlation Engine

```python
from behavioral_analysis import CorrelationEngine, CorrelationDimension, TemporalWindow

engine = CorrelationEngine(
    dimensions=[
        CorrelationDimension.AUTHENTICATION,
        CorrelationDimension.NETWORK,
        CorrelationDimension.PROCESS,
        CorrelationDimension.FILE_SYSTEM,
        CorrelationDimension.REGISTRY,
    ],
    temporal_window=TemporalWindow(minutes=15),
    min_correlation_score=0.65
)

# Ingest events from multiple sources
engine.ingest_events(auth_events)
engine.ingest_events(netflow_events)
engine.ingest_events(sysmon_events)
engine.ingest_events(firewall_events)

# Run correlation analysis
clusters = engine.correlate()

for cluster in clusters:
    print(f"\nCorrelation Cluster ID: {cluster.cluster_id}")
    print(f"  Event Count: {len(cluster.events)}")
    print(f"  Dimensions Hit: {[d.value for d in cluster.dimensions]}")
    print(f"  Time Span: {cluster.start_time} -> {cluster.end_time}")
    print(f"  Risk Score: {cluster.risk_score:.2f}")
    print(f"  MITRE Mapping: {[t.technique_id for t in cluster.mitre_techniques]}")

    for event in cluster.events:
        print(f"    [{event.timestamp}] {event.source}: {event.description}")
```

### Graph-Based Behavioral Modeling

```python
from behavioral_analysis import BehavioralGraph, Node, Edge, GraphAlgorithm

graph = BehavioralGraph()

# Build behavioral graph from observed activity
nodes = [
    Node(id="user-1", type="user", attributes={"department": "finance", "clearance": "secret"}),
    Node(id="host-a", type="host", attributes={"os": "windows-11", "role": "workstation"}),
    Node(id="host-b", type="host", attributes={"os": "windows-server-2022", "role": "file-server"}),
    Node(id="share-conf", type="resource", attributes={"path": "\\\\fileserver\\confidential", "classification": "secret"}),
    Node(id="process-ps", type="process", attributes={"name": "powershell.exe", "cmdline": "-enc ..."}),
    Node(id="ip-external", type="network", attributes={"ip": "203.0.113.50", "geo": "RU"}),
]

edges = [
    Edge(src="user-1", dst="host-a", type="authenticates", weight=1.0),
    Edge(src="host-a", dst="host-b", type="accesses_share", weight=0.8),
    Edge(src="host-b", dst="share-conf", type="reads_file", weight=0.9),
    Edge(src="user-1", dst="process-ps", type="launches", weight=0.3),
    Edge(src="process-ps", dst="ip-external", type="connects_to", weight=0.1),
]

for node in nodes:
    graph.add_node(node)
for edge in edges:
    graph.add_edge(edge)

# Detect anomalous paths using graph algorithms
anomalous_paths = graph.detect_anomalous_paths(
    algorithm=GraphAlgorithm.SHORTEST_PATH_DEVIATION,
    baseline_paths=graph.load_baseline_paths(),
    threshold_sigma=3.0
)

for path in anomalous_paths:
    print(f"Anomalous path detected: {' -> '.join(path.node_ids)}")
    print(f"  Deviation score: {path.deviation_score:.2f}σ")
    print(f"  Normal frequency: {path.baseline_frequency:.4f}")
    print(f"  Observed frequency: {path.observed_frequency:.4f}")
```

### Insider Threat Detection Pipeline

```python
from behavioral_analysis import InsiderThreatDetector, RiskIndicator, ThreatLevel

detector = InsiderThreatDetector(
    risk_weights={
        RiskIndicator.DATA_EXFILTRATION: 0.35,
        RiskIndicator.UNUSUAL_ACCESS: 0.25,
        RiskIndicator.AFTER_HOURS_ACTIVITY: 0.15,
        RiskIndicator.PRIVILEGE_ESCALATION: 0.15,
        RiskIndicator.DEFENSE_EVASION: 0.10,
    },
    scoring_window_days=30,
    alert_threshold=0.70
)

# Ingest user activity logs
detector.ingest_user_activity(
    user_id="jsmith",
    activities=[
        {"type": "file_access", "resource": "\\\\fileserver\\hr_records", "time": "02:15", "bytes": 52428800},
        {"type": "usb_connect", "device": "SanDisk_Ultra", "time": "02:20", "bytes": 52428800},
        {"type": "email_send", "to": "external@gmail.com", "time": "02:25", "attachment_size": 48000000},
        {"type": "process_launch", "program": "rar.exe", "cmdline": "a -hp password archive.rar ."},
        {"type": "browser_visit", "url": "mega.nz/upload", "time": "02:30"},
    ]
)

# Run risk assessment
assessment = detector.assess_user("jsmith")

print(f"User: {assessment.user_id}")
print(f"Overall Risk Score: {assessment.risk_score:.2f}")
print(f"Threat Level: {assessment.threat_level.value}")
print(f"Confidence: {assessment.confidence:.1%}")
print(f"\nTriggered Risk Indicators:")
for indicator in assessment.triggered_indicators:
    print(f"  - {indicator.name}: weight={indicator.weight:.2f}, "
          f"events={indicator.event_count}, score={indicator.score:.2f}")
    print(f"    Evidence: {indicator.evidence[:3]}")
```

## Detection Techniques

### Statistical Anomaly Detection Methods

```python
from behavioral_analysis import StatisticalDetector, DistributionModel

detector = StatisticalDetector(
    models=[
        DistributionModel.Z_SCORE,
        DistributionModel.MODIFIED_Z_SCORE,
        DistributionModel.IQR,
        DistributionModel.EWMA,
        DistributionModel.GAUSSIAN_MIXTURE,
    ],
    min_samples=100,
    confidence_level=0.95
)

# Define metrics to monitor
metrics = {
    "login_count_per_day": {"data": login_counts, "model": DistributionModel.EWMA, "ewma_alpha": 0.3},
    "bytes_transferred": {"data": byte_counts, "model": DistributionModel.IQR, "iqr_multiplier": 1.5},
    "failed_auth_rate": {"data": failed_auth_rates, "model": DistributionModel.GAUSSIAN_MIXTURE, "n_components": 3},
    "process_count": {"data": process_counts, "model": DistributionModel.MODIFIED_Z_SCORE, "threshold": 3.5},
}

results = detector.analyze_metrics(metrics)

for metric_name, result in results.items():
    print(f"\nMetric: {metric_name}")
    print(f"  Model: {result.model_used.value}")
    print(f"  Mean: {result.mean:.2f}, StdDev: {result.stddev:.2f}")
    print(f"  Anomalies: {result.anomaly_count}/{result.total_samples}")
    print(f"  Current Value: {result.current_value:.2f}")
    print(f"  Score: {result.anomaly_score:.2f}")
    if result.anomalies:
        for a in result.anomalies[:3]:
            print(f"    Anomaly at {a.timestamp}: value={a.value:.2f}, "
                  f"deviation={a.deviation_sigma:.2f}σ")
```

### Machine Learning-Based Behavioral Classification

```python
from behavioral_analysis import MLClassifier, FeatureExtractor, ModelConfig

# Feature engineering from raw events
extractor = FeatureExtractor(
    feature_sets=[
        "temporal_features",    # time-of-day, day-of-week, session duration
        "volume_features",      # bytes in/out, file count, process count
        "entropy_features",     # command-line entropy, filename entropy
        "graph_features",       # centrality, connectivity, path length
        "sequence_features",    # n-gram patterns, Markov transitions
    ],
    window_size_hours=1,
    aggregation_methods=["count", "sum", "mean", "stddev", "max", "min"]
)

# Configure the ML model
config = ModelConfig(
    algorithm="gradient_boosting",
    hyperparameters={
        "n_estimators": 500,
        "max_depth": 8,
        "learning_rate": 0.05,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 3,
    },
    cross_validation_folds=5,
    test_size=0.2,
    random_state=42
)

classifier = MLClassifier(config=config, feature_extractor=extractor)

# Train the model
features, labels = extractor.extract_labeled_data(
    normal_events=normal_event_store,
    confirmed_malicious_events=malicious_event_store
)

training_result = classifier.train(features, labels)
print(f"Model Training Results:")
print(f"  Accuracy: {training_result.accuracy:.4f}")
print(f"  Precision: {training_result.precision:.4f}")
print(f"  Recall: {training_result.recall:.4f}")
print(f"  F1 Score: {training_result.f1_score:.4f}")
print(f"  AUC-ROC: {training_result.auc_roc:.4f}")

# Classify new events
predictions = classifier.predict_batch(new_events)
for pred in predictions:
    if pred.probability > 0.8:
        print(f"  ALERT: {pred.event_id} classified as {pred.label} "
              f"(confidence: {pred.probability:.2%})")
```

### Temporal Pattern Mining

```python
from behavioral_analysis import TemporalMiner, PatternType, SequenceMiner

miner = TemporalMiner(
    min_support=0.01,
    min_confidence=0.7,
    max_gap_seconds=3600,
    pattern_types=[
        PatternType.SEQUENTIAL,
        PatternType.PERIODIC,
        PatternType.BURST,
        PatternType.FREQUENCY_SHIFT,
    ]
)

# Mine temporal patterns from event sequences
patterns = miner.mine(
    event_sequences=user_event_sequences,
    time_granularity="minute"
)

for pattern in patterns:
    print(f"\nTemporal Pattern: {pattern.pattern_id}")
    print(f"  Type: {pattern.pattern_type.value}")
    print(f"  Support: {pattern.support:.4f}")
    print(f"  Confidence: {pattern.confidence:.4f}")
    print(f"  Events: {' -> '.join([e.event_type for e in pattern.sequence])}")
    print(f"  Avg Interval: {pattern.avg_interval_seconds:.0f}s")
    print(f"  Users exhibiting: {pattern.user_count}")

# Detect deviations from mined patterns
deviations = miner.detect_deviations(
    current_sequences=current_event_sequences,
    mined_patterns=patterns,
    deviation_threshold=2.0
)

for dev in deviations:
    print(f"\n  DEVIATION: User {dev.user_id}")
    print(f"    Expected: {dev.expected_pattern}")
    print(f"    Observed: {dev.observed_sequence}")
    print(f"    Deviation Score: {dev.score:.2f}")
```

## Real-World Investigation Scenarios

### Scenario 1: Compromised Workstation Lateral Movement

```python
from behavioral_analysis import InvestigationCase, InvestigationStep, Evidence

case = InvestigationCase(
    case_id="IR-2024-089",
    title="Suspected Lateral Movement from Workstation WS-FIN-042",
    analyst="jdoe",
    severity="high"
)

# Step 1: Baseline deviation analysis
step1 = InvestigationStep(
    name="Baseline Deviation Check",
    description="Compare WS-FIN-042 activity against its behavioral baseline"
)

baseline = step1.run_baseline_comparison(
    entity_id="ws-fin-042",
    metrics=[
        "process_creation_count",
        "network_connection_count",
        "authentication_events",
        "file_modification_count",
        "registry_modification_count",
    ],
    comparison_window="last_4_hours"
)

print("Baseline Deviation Report for WS-FIN-042:")
for metric in baseline.metrics:
    flag = " *** ANOMALY ***" if metric.is_anomaly else ""
    print(f"  {metric.name}: current={metric.current_value:.1f}, "
          f"baseline_mean={metric.baseline_mean:.1f}, "
          f"deviation={metric.deviation_sigma:.2f}σ{flag}")

# Step 2: Process tree analysis
step2 = InvestigationStep(
    name="Process Tree Reconstruction",
    description="Reconstruct process creation tree to identify suspicious chains"
)

process_tree = step2.build_process_tree(
    host="ws-fin-042",
    time_range=("2024-01-15T08:00:00Z", "2024-01-15T12:00:00Z"),
    include_command_line=True
)

print("\nProcess Tree (highlighting suspicious chains):")
for node in process_tree.traverse():
    risk_marker = "[RISK]" if node.risk_score > 70 else ""
    print(f"  {'  ' * node.depth}{node.process_name} (PID {node.pid}) {risk_marker}")
    if node.command_line:
        print(f"  {'  ' * (node.depth + 1)}CMD: {node.command_line[:120]}")
    if node.risk_score > 70:
        print(f"  {'  ' * (node.depth + 1)}Risk: {node.risk_score:.1f}, "
              f"Indicators: {node.indicators}")

# Step 3: Network connection analysis
step3 = InvestigationStep(
    name="Network Connection Analysis",
    description="Identify anomalous network connections from the compromised host"
)

connections = step3.analyze_connections(
    host="ws-fin-042",
    time_range=("2024-01-15T08:00:00Z", "2024-01-15T12:00:00Z"),
    flags=["new_dst_ip", "new_dst_port", "high_volume", "unusual_protocol"]
)

print("\nAnomalous Network Connections:")
for conn in connections:
    print(f"  {conn.timestamp}: {conn.src_ip}:{conn.src_port} -> "
          f"{conn.dst_ip}:{conn.dst_port} ({conn.protocol})")
    print(f"    Bytes: {conn.bytes_sent}B sent, {conn.bytes_received}B recv")
    print(f"    Flags: {conn.anomaly_flags}")
    print(f"    Geo: {conn.dst_geo}, ASN: {conn.dst_asn}")

# Step 4: Evidence packaging
evidence = Evidence(
    case_id="IR-2024-089",
    items=[
        {"type": "process_tree", "data": process_tree.serialize()},
        {"type": "network_connections", "data": [c.serialize() for c in connections]},
        {"type": "baseline_report", "data": baseline.serialize()},
    ],
    collected_by="jdoe",
    collection_timestamp="2024-01-15T13:00:00Z"
)
evidence.package(output_path="/evidence/IR-2024-089/behavioral-analysis/")
print(f"\nEvidence packaged at: {evidence.output_path}")
print(f"Evidence hash: {evidence.sha256}")
```

### Scenario 2: Data Exfiltration Detection

```python
from behavioral_analysis import ExfiltrationDetector, DataFlowAnalyzer

detector = ExfiltrationDetector(
    detection_methods=["volume_baseline", "protocol_anomaly", "temporal_anomaly", "content_pattern"],
    sensitivity="high"
)

# Analyze outbound data flows
flows = DataFlowAnalyzer().analyze(
    host="db-server-01",
    time_range=("2024-01-15T00:00:00Z", "2024-01-15T23:59:59Z"),
    protocols=["tcp", "udp", "icmp", "dns"]
)

exfil_indicators = detector.detect(flows)

print("Data Exfiltration Analysis Report:")
print(f"  Total outbound flows analyzed: {len(flows)}")
print(f"  Exfiltration indicators detected: {len(exfil_indicators)}")

for indicator in exfil_indicators:
    print(f"\n  Indicator: {indicator.type}")
    print(f"    Severity: {indicator.severity}")
    print(f"    Confidence: {indicator.confidence:.1%}")
    print(f"    Evidence:")
    for ev in indicator.evidence:
        print(f"      - {ev}")
    print(f"    MITRE Technique: {indicator.mitre_technique}")

# Generate IOCs from confirmed exfiltration
iocs = detector.generate_iocs(exfil_indicators, min_confidence=0.8)
print(f"\nGenerated IOCs from exfiltration analysis: {len(iocs)}")
for ioc in iocs:
    print(f"  {ioc.type}: {ioc.value} (confidence: {ioc.confidence:.1%})")
```

## Configuration Reference

### BehavioralEngine Configuration Schema

```yaml
behavioral_engine:
  general:
    window_days: 30
    sensitivity: 0.8
    min_samples: 100
    evaluation_interval_minutes: 15
    max_events_per_entity: 1000000

  baselines:
    login_pattern:
      type: "temporal_distribution"
      dimensions: ["hour_of_day", "day_of_week", "source_ip"]
      update_frequency: "weekly"
      min_sessions: 20

    process_execution:
      type: "frequency_distribution"
      dimensions: ["process_name", "parent_process", "command_line"]
      update_frequency: "daily"
      min_executions: 50

    network_traffic:
      type: "volume_baseline"
      dimensions: ["dst_ip", "dst_port", "protocol", "time_of_day"]
      update_frequency: "daily"
      min_flows: 100

    file_access:
      type: "pattern_baseline"
      dimensions: ["path", "access_type", "time_of_day", "file_type"]
      update_frequency: "weekly"
      min_accesses: 30

  detection:
    statistical:
      z_score_threshold: 3.0
      modified_z_score_threshold: 3.5
      iqr_multiplier: 1.5
      ewma_alpha: 0.3
      ewma_threshold_sigma: 2.5

    ml_classification:
      model_path: "models/behavioral_classifier.pkl"
      retrain_frequency: "monthly"
      min_training_samples: 10000
      feature_importance_threshold: 0.01

    temporal_mining:
      min_support: 0.01
      min_confidence: 0.7
      max_gap_seconds: 3600
      max_pattern_length: 10

  alerting:
    severity_thresholds:
      critical: 0.90
      high: 0.75
      medium: 0.50
      low: 0.25

    notification_channels:
      - type: "siem"
        endpoint: "https://siem.example.com/api/alerts"
      - type: "email"
        recipients: ["soc@example.com"]
        severity_filter: ["critical", "high"]
      - type: "slack"
        webhook: "https://hooks.slack.com/services/xxx"
        channel: "#security-alerts"

  tuning:
    false_positive_suppression:
      enabled: true
      auto_suppress_threshold: 5
      suppression_window_days: 30
    baseline_adjustment:
      auto_adjust: true
      adjustment_factor: 0.1
      max_adjustment_per_cycle: 0.05
```

## Database Schema for Behavioral Data

### Entity and Baseline Storage

```sql
-- Behavioral entities (users, hosts, processes)
CREATE TABLE behavioral_entities (
    entity_id       VARCHAR(128) PRIMARY KEY,
    entity_type     ENUM('user', 'host', 'process', 'network', 'file') NOT NULL,
    display_name    VARCHAR(256),
    department      VARCHAR(128),
    role            VARCHAR(128),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active       BOOLEAN DEFAULT TRUE,
    INDEX idx_entity_type (entity_type),
    INDEX idx_department (department)
);

-- Baseline records
CREATE TABLE behavioral_baselines (
    baseline_id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    entity_id           VARCHAR(128) NOT NULL,
    metric_name         VARCHAR(128) NOT NULL,
    baseline_type       VARCHAR(64) NOT NULL,
    mean_value          DOUBLE,
    stddev_value        DOUBLE,
    median_value        DOUBLE,
    p95_value           DOUBLE,
    p99_value           DOUBLE,
    sample_count        INT,
    observation_start   TIMESTAMP,
    observation_end     TIMESTAMP,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES behavioral_entities(entity_id),
    UNIQUE KEY uk_entity_metric (entity_id, metric_name),
    INDEX idx_metric_name (metric_name)
);

-- Anomaly detections
CREATE TABLE behavioral_anomalies (
    anomaly_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    entity_id           VARCHAR(128) NOT NULL,
    metric_name         VARCHAR(128) NOT NULL,
    anomaly_score       DOUBLE NOT NULL,
    deviation_sigma     DOUBLE,
    observed_value      DOUBLE,
    baseline_value      DOUBLE,
    detection_method    VARCHAR(64),
    severity            ENUM('info', 'low', 'medium', 'high', 'critical') NOT NULL,
    detected_at         TIMESTAMP NOT NULL,
    acknowledged        BOOLEAN DEFAULT FALSE,
    acknowledged_by     VARCHAR(128),
    acknowledged_at     TIMESTAMP,
    false_positive      BOOLEAN DEFAULT FALSE,
    investigation_id    VARCHAR(64),
    evidence_json       JSON,
    FOREIGN KEY (entity_id) REFERENCES behavioral_entities(entity_id),
    INDEX idx_severity (severity),
    INDEX idx_detected_at (detected_at),
    INDEX idx_entity_detected (entity_id, detected_at)
);

-- Correlation clusters
CREATE TABLE correlation_clusters (
    cluster_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    cluster_uid         VARCHAR(64) UNIQUE NOT NULL,
    risk_score          DOUBLE NOT NULL,
    event_count         INT NOT NULL,
    dimension_count     INT NOT NULL,
    start_time          TIMESTAMP NOT NULL,
    end_time            TIMESTAMP NOT NULL,
    mitre_techniques    JSON,
    status              ENUM('new', 'investigating', 'confirmed', 'false_positive', 'resolved') DEFAULT 'new',
    assigned_to         VARCHAR(128),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_risk_score (risk_score DESC),
    INDEX idx_status (status),
    INDEX idx_time_range (start_time, end_time)
);

-- Cluster events mapping
CREATE TABLE cluster_events (
    cluster_id      BIGINT NOT NULL,
    event_id        VARCHAR(128) NOT NULL,
    event_source    VARCHAR(64),
    event_timestamp TIMESTAMP,
    relevance_score DOUBLE,
    PRIMARY KEY (cluster_id, event_id),
    FOREIGN KEY (cluster_id) REFERENCES correlation_clusters(cluster_id)
);

-- Behavioral rules
CREATE TABLE behavioral_rules (
    rule_id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    rule_name       VARCHAR(256) NOT NULL,
    rule_description TEXT,
    rule_type       ENUM('threshold', 'statistical', 'ml', 'temporal', 'graph') NOT NULL,
    entity_scope    VARCHAR(128),
    conditions      JSON NOT NULL,
    severity        ENUM('info', 'low', 'medium', 'high', 'critical') NOT NULL,
    enabled         BOOLEAN DEFAULT TRUE,
    created_by      VARCHAR(128),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rule_type (rule_type),
    INDEX idx_enabled (enabled)
);
```

## Integration Patterns

### SIEM Integration (Splunk, Elastic, QRadar)

```python
from behavioral_analysis import SIEMIntegration, SIEMType, AlertFormat

# Splunk integration
splunk = SIEMIntegration(
    siem_type=SIEMType.SPLUNK,
    host="splunk.example.com",
    port=8089,
    token="your-splunk-token",
    index="behavioral_analysis",
    sourcetype="behavioral:anomaly"
)

# Configure alert forwarding
splunk.configure_alert_forwarding(
    min_severity="medium",
    batch_size=100,
    flush_interval_seconds=30,
    include_evidence=True,
    field_mappings={
        "entity_id": "user",
        "anomaly_score": "risk_score",
        "detection_method": "technique",
        "evidence_json": "evidence",
    }
)

# Elastic Security integration
elastic = SIEMIntegration(
    siem_type=SIEMType.ELASTIC,
    hosts=["https://elastic.example.com:9200"],
    api_key="your-elastic-key",
    index_pattern="behavioral-analysis-*",
    ilm_policy="behavioral-analysis-policy"
)

# Push detections to Elastic
detection_rules = elastic.create_detection_rules(
    anomalies=recent_anomalies,
    rule_template={
        "type": "threshold",
        "language": "kuery",
        "risk_score_mapping": [{"field": "anomaly_score"}],
        "severity_mapping": [{"field": "severity"}],
        "timeline_template_id": "behavioral-analysis-timeline",
    }
)
print(f"Created {len(detection_rules)} detection rules in Elastic Security")
```

### SOAR Platform Integration

```python
from behavioral_analysis import SOARIntegration, PlaybookTrigger, Action

soar = SOARIntegration(
    platform="Cortex XSOAR",
    base_url="https://soar.example.com",
    api_key="your-soar-key"
)

# Define automated response playbooks
playbook_high_risk = soar.create_playbook(
    name="Behavioral Anomaly - High Risk",
    trigger=PlaybookTrigger(
        condition="anomaly_score >= 0.75 AND severity IN ('high', 'critical')",
        source="behavioral_analysis"
    ),
    actions=[
        Action(
            type="enrich_user",
            parameters={"user_id": "{{entity_id}}", "enrichment_sources": ["ad", "hr_system"]}
        ),
        Action(
            type="check_user_risk_history",
            parameters={"user_id": "{{entity_id}}", "lookback_days": 90}
        ),
        Action(
            type="conditional",
            condition="{{user_risk_history}} >= 3",
            then_actions=[
                Action(type="create_ticket", parameters={
                    "title": "High Risk Behavioral Anomaly - {{entity_id}}",
                    "severity": "P2",
                    "assignee": "soc_l2_team"
                }),
                Action(type="isolate_host", parameters={"host": "{{source_host}}"}),
                Action(type="disable_user", parameters={"user_id": "{{entity_id}}", "temporary": True}),
            ],
            else_actions=[
                Action(type="create_ticket", parameters={
                    "title": "Behavioral Anomaly - {{entity_id}}",
                    "severity": "P3",
                    "assignee": "soc_l1_team"
                }),
            ]
        ),
    ]
)

# Register webhook for real-time anomaly alerts
soar.register_webhook(
    name="behavioral-anomaly-ingest",
    endpoint="/api/behavioral/anomalies",
    playbook_id=playbook_high_risk.id,
    auth_method="bearer_token"
)
```

### REST API Endpoint for Real-Time Scoring

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from behavioral_analysis import BehavioralEngine, ScoreRequest, ScoreResponse

app = FastAPI(title="Behavioral Analysis API", version="2.0.0")
engine = BehavioralEngine.load("production_model")

@app.post("/api/v2/score", response_model=ScoreResponse)
async def score_activity(request: ScoreRequest):
    """Score a single activity against behavioral baselines."""
    try:
        result = engine.score_activity(
            entity_id=request.entity_id,
            activity=request.activity,
            dimensions=request.dimensions
        )
        return ScoreResponse(
            entity_id=request.entity_id,
            anomaly_score=result.anomaly_score,
            risk_level=result.risk_level,
            triggered_rules=result.triggered_rules,
            baseline_deviations=result.baseline_deviations,
            recommended_actions=result.recommended_actions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/batch-score")
async def batch_score(activities: list[ScoreRequest]):
    """Score multiple activities in batch."""
    results = engine.batch_score(activities)
    return {
        "total": len(results),
        "anomalies_detected": sum(1 for r in results if r.anomaly_score > 0.5),
        "results": results
    }

@app.get("/api/v2/baselines/{entity_id}")
async def get_baselines(entity_id: str):
    """Retrieve behavioral baselines for an entity."""
    baselines = engine.get_baselines(entity_id)
    if not baselines:
        raise HTTPException(status_code=404, detail="No baselines found")
    return {"entity_id": entity_id, "baselines": baselines}

@app.get("/api/v2/anomalies")
async def list_anomalies(
    severity: str = None,
    entity_id: str = None,
    since_hours: int = 24,
    limit: int = 100
):
    """List detected anomalies with optional filters."""
    anomalies = engine.query_anomalies(
        severity=severity,
        entity_id=entity_id,
        since_hours=since_hours,
        limit=limit
    )
    return {"count": len(anomalies), "anomalies": anomalies}
```

## Performance Tuning Guide

### Throughput Optimization

```python
from behavioral_analysis import PerformanceConfig, ParallelEngine

config = PerformanceConfig(
    # Parallelism settings
    max_worker_threads=8,
    batch_size=10000,
    queue_size=100000,

    # Caching
    enable_baseline_cache=True,
    baseline_cache_ttl_seconds=300,
    baseline_cache_max_entries=50000,

    # I/O optimization
    use_async_io=True,
    connection_pool_size=20,
    read_timeout_seconds=30,

    # Memory management
    max_memory_mb=4096,
    event_buffer_size=500000,
    garbage_collection_threshold=100000,

    # Database
    db_batch_insert_size=5000,
    db_connection_pool_size=10,
    db_query_timeout_seconds=30
)

engine = ParallelEngine(config=config)

# Benchmark throughput
benchmark = engine.benchmark(
    event_count=1000000,
    concurrent_users=100,
    duration_seconds=60
)

print(f"Performance Benchmark Results:")
print(f"  Events/second: {benchmark.events_per_second:.0f}")
print(f"  Latency P50: {benchmark.latency_p50_ms:.1f}ms")
print(f"  Latency P95: {benchmark.latency_p95_ms:.1f}ms")
print(f"  Latency P99: {benchmark.latency_p99_ms:.1f}ms")
print(f"  Memory usage: {benchmark.memory_mb:.1f}MB")
print(f"  CPU utilization: {benchmark.cpu_percent:.1f}%")
print(f"  Anomalies detected: {benchmark.anomalies_detected}")
```

### Memory-Efficient Large-Scale Processing

```python
from behavioral_analysis import StreamingProcessor, ChunkIterator

processor = StreamingProcessor(
    chunk_size=50000,
    max_concurrent_chunks=4,
    spill_to_disk=True,
    spill_directory="/tmp/behavioral_spill"
)

# Process large event stream without loading all into memory
async def process_large_dataset(file_path: str):
    chunk_iter = ChunkIterator(file_path, chunk_size=50000)

    total_processed = 0
    total_anomalies = 0

    async for chunk in chunk_iter:
        results = await processor.process_chunk(chunk)
        total_processed += len(chunk.events)
        total_anomalies += len(results.anomalies)

        # Write results incrementally
        await results.write_to_output(f"output_batch_{total_processed}.jsonl")

        if total_processed % 500000 == 0:
            print(f"  Progress: {total_processed:,} events processed, "
                  f"{total_anomalies:,} anomalies found")

    print(f"\nFinal: {total_processed:,} events, {total_anomalies:,} anomalies")
    return total_anomalies
```

### Baseline Refresh Optimization

```python
from behavioral_analysis import BaselineRefreshScheduler, RefreshStrategy

scheduler = BaselineRefreshScheduler(
    strategy=RefreshStrategy.INCREMENTAL,
    refresh_config={
        "user_login": {"frequency": "daily", "lookback_days": 30, "min_samples": 20},
        "process_exec": {"frequency": "daily", "lookback_days": 14, "min_samples": 50},
        "network_flow": {"frequency": "hourly", "lookback_days": 7, "min_samples": 100},
        "file_access": {"frequency": "weekly", "lookback_days": 60, "min_samples": 30},
    },
    max_concurrent_refreshes=4,
    priority_entities=["domain_admins", "service_accounts", "critical_servers"]
)

# Run scheduled refresh
refresh_result = scheduler.run_refresh()
print(f"Baseline Refresh Summary:")
print(f"  Entities refreshed: {refresh_result.entities_refreshed}")
print(f"  Baselines updated: {refresh_result.baselines_updated}")
print(f"  Duration: {refresh_result.duration_seconds:.1f}s")
print(f"  Errors: {refresh_result.error_count}")
for error in refresh_result.errors:
    print(f"    - {error.entity_id}: {error.message}")
```

## Architecture

```
+================================================================+
|                    BEHAVIORAL ANALYSIS ARCHITECTURE              |
+================================================================+

+-------------------+     +-------------------+     +-------------------+
|   DATA SOURCES    |     |   DATA SOURCES    |     |   DATA SOURCES    |
|  +-------------+  |     |  +-------------+  |     |  +-------------+  |
|  | Auth Logs   |--+--+  |  | Sysmon      |--+--+  |  | NetFlow     |--+--+
|  +-------------+  |  |  |  +-------------+  |  |  |  +-------------+  |  |
|  +-------------+  |  |  |  +-------------+  |  |  |  +-------------+  |  |
|  | EDR Agent   |--+  |  |  | WMI Logs    |--+  |  |  | Firewall    |--+  |
|  +-------------+  |  |  |  +-------------+  |  |  |  +-------------+  |  |
|  +-------------+  |  |  |  +-------------+  |  |  |  +-------------+  |  |
|  | File Audit  |--+  |  |  | DNS Logs    |--+  |  |  | Proxy Logs  |--+  |
|  +-------------+  |  |  |  +-------------+  |  |  |  +-------------+  |  |
+-------------------+  |  +-------------------+  |  +-------------------+  |
                        |                        |                         |
                        v                        v                         v
              +----------------------------------------------+
              |            EVENT NORMALIZATION LAYER          |
              |  +----------------------------------------+  |
              |  | Parser | Normalizer | Timestamp Sync   |  |
              |  +----------------------------------------+  |
              +----------------------------------------------+
                                    |
                                    v
              +----------------------------------------------+
              |            BEHAVIORAL ENGINE CORE            |
              |                                              |
              |  +------------+  +------------+  +--------+ |
              |  | Baseline   |  | Anomaly    |  | ML     | |
              |  | Manager    |  | Detector   |  | Class. | |
              |  +------------+  +------------+  +--------+ |
              |  +------------+  +------------+  +--------+ |
              |  | Temporal   |  | Graph      |  | Correl. | |
              |  | Miner      |  | Analyzer   |  | Engine | |
              |  +------------+  +------------+  +--------+ |
              +----------------------------------------------+
                    |                    |                    |
                    v                    v                    v
         +-------------+     +------------------+    +---------------+
         |  Statistical |     |  ML Classification|   |  Temporal     |
         |  Analysis    |     |  & Prediction     |   |  Pattern      |
         |  + Z-Score   |     |  + GBT Model      |   |  Mining       |
         |  + IQR       |     |  + Anomaly Forest |   |  + Sequences  |
         |  + EWMA      |     |  + Deep Learning  |   |  + Periodicity|
         +-------------+     +------------------+    +---------------+
                    |                    |                    |
                    v                    v                    v
              +----------------------------------------------+
              |           CORRELATION & SCORING               |
              |  +----------------------------------------+  |
              |  | Multi-Dimension Correlation Engine      |  |
              |  | Risk Scoring | MITRE Mapping | Alerts  |  |
              |  +----------------------------------------+  |
              +----------------------------------------------+
                                    |
                    +---------------+---------------+
                    |               |               |
                    v               v               v
            +-----------+  +-------------+  +------------+
            | SIEM      |  | SOAR        |  | Dashboard  |
            | Integration|  | Integration |  | & Reports  |
            +-----------+  +-------------+  +------------+
```

## Testing and Validation

### Unit Testing Behavioral Rules

```python
import pytest
from behavioral_analysis import BehavioralEngine, Anomaly, Baseline

class TestBehavioralEngine:
    def setup_method(self):
        self.engine = BehavioralEngine(window_days=30, sensitivity=0.8)

    def test_baseline_creation(self):
        """Test that baselines are created correctly from sample data."""
        data = [10, 12, 11, 13, 10, 12, 14, 11, 12, 13] * 10
        baseline = self.engine.create_baseline(
            entity_id="test-user",
            metric_name="login_count",
            data=data
        )
        assert baseline.mean_value == pytest.approx(12.0, abs=0.5)
        assert baseline.sample_count == 100
        assert baseline.stddev_value > 0

    def test_anomaly_detection_normal(self):
        """Normal activity should not trigger anomalies."""
        baseline = Baseline(mean_value=12.0, stddev_value=1.5)
        result = self.engine.score_observation(
            baseline=baseline,
            observed_value=13.0
        )
        assert result.anomaly_score < 0.5
        assert result.is_anomaly is False

    def test_anomaly_detection_spike(self):
        """Spike activity should trigger anomaly."""
        baseline = Baseline(mean_value=12.0, stddev_value=1.5)
        result = self.engine.score_observation(
            baseline=baseline,
            observed_value=25.0
        )
        assert result.anomaly_score > 0.8
        assert result.is_anomaly is True
        assert result.deviation_sigma > 5.0

    def test_anomaly_detection_drop(self):
        """Significant drop should trigger anomaly."""
        baseline = Baseline(mean_value=100.0, stddev_value=10.0)
        result = self.engine.score_observation(
            baseline=baseline,
            observed_value=10.0
        )
        assert result.anomaly_score > 0.7
        assert result.is_anomaly is True

    def test_temporal_pattern_detection(self):
        """Test detection of temporal pattern deviation."""
        normal_hours = list(range(8, 18)) * 30  # 9am-5pm
        patterns = self.engine.mine_temporal_patterns(normal_hours)
        assert len(patterns) > 0

        # Activity at 3am should be anomalous
        result = self.engine.score_temporal_observation(
            patterns=patterns,
            observed_hour=3
        )
        assert result.anomaly_score > 0.7

    def test_multi_dimension_correlation(self):
        """Test correlation across multiple behavioral dimensions."""
        events = [
            {"dimension": "auth", "entity": "user-1", "anomaly": True, "score": 0.9},
            {"dimension": "network", "entity": "user-1", "anomaly": True, "score": 0.8},
            {"dimension": "process", "entity": "user-1", "anomaly": True, "score": 0.7},
        ]
        correlation = self.engine.correlate_dimensions(events)
        assert correlation.cluster_risk_score > 0.8
        assert len(correlation.mitre_techniques) > 0

    def test_false_positive_suppression(self):
        """Test that known false positives are suppressed."""
        self.engine.add_false_positive_pattern(
            entity_id="backup-server",
            metric_name="network_volume",
            reason="scheduled_backup"
        )
        baseline = Baseline(mean_value=500.0, stddev_value=50.0)
        result = self.engine.score_observation(
            baseline=baseline,
            observed_value=800.0,
            entity_id="backup-server",
            metric_name="network_volume"
        )
        assert result.false_positive_suppressed is True
```

### Integration Testing

```python
import pytest
from behavioral_analysis import BehavioralEngine, SIEMIntegration

class TestSIEMIntegration:
    @pytest.fixture
    def engine(self):
        return BehavioralEngine.load_test_config()

    @pytest.fixture
    def splunk_mock(self, mocker):
        mock = mocker.patch("behavioral_analysis.splunk.SplunkClient")
        mock.return_value.submit_event.return_value = {"status": "ok"}
        return mock

    def test_alert_forwarding(self, engine, splunk_mock):
        """Test that alerts are forwarded to Splunk correctly."""
        # Create a high-severity anomaly
        anomaly = engine.create_test_anomaly(severity="high", score=0.95)

        # Forward to SIEM
        siem = SIEMIntegration(siem_type="splunk", client=splunk_mock)
        result = siem.forward_alert(anomaly)

        assert result.status == "delivered"
        splunk_mock.return_value.submit_event.assert_called_once()

    def test_batch_forwarding(self, engine, splunk_mock):
        """Test batch alert forwarding with batching enabled."""
        anomalies = [engine.create_test_anomaly(severity="medium", score=0.6) for _ in range(150)]

        siem = SIEMIntegration(
            siem_type="splunk",
            client=splunk_mock,
            batch_size=100,
            flush_interval_seconds=5
        )

        for anomaly in anomalies:
            siem.forward_alert(anomaly)

        siem.flush()
        assert splunk_mock.return_value.submit_event.call_count == 2  # 100 + 50
```

### Performance Benchmarking

```python
from behavioral_analysis import BehavioralEngine, BenchmarkSuite

def test_throughput_benchmark():
    """Verify engine meets minimum throughput requirements."""
    engine = BehavioralEngine(window_days=30, sensitivity=0.8)
    benchmark = BenchmarkSuite(engine)

    results = benchmark.run_throughput_test(
        event_count=100000,
        concurrent_threads=4,
        timeout_seconds=60
    )

    assert results.events_per_second > 5000, \
        f"Throughput {results.events_per_second} below minimum 5000 eps"
    assert results.latency_p99_ms < 100, \
        f"P99 latency {results.latency_p99_ms}ms exceeds 100ms threshold"
    assert results.error_rate < 0.001, \
        f"Error rate {results.error_rate} exceeds 0.1% threshold"

def test_memory_usage_benchmark():
    """Verify engine stays within memory limits."""
    engine = BehavioralEngine(window_days=30, sensitivity=0.8)
    benchmark = BenchmarkSuite(engine)

    results = benchmark.run_memory_test(
        event_count=500000,
        max_memory_mb=2048
    )

    assert results.peak_memory_mb < 2048, \
        f"Peak memory {results.peak_memory_mb}MB exceeds 2GB limit"
    assert results.memory_leak_detected is False, "Memory leak detected during test"
```

## Reporting Templates

### Anomaly Investigation Report

```python
from behavioral_analysis import ReportGenerator, ReportTemplate, ReportSection

generator = ReportGenerator(template=ReportTemplate.INVESTIGATION_REPORT)

report = generator.generate(
    case_id="IR-2024-089",
    title="Behavioral Anomaly Investigation Report",
    sections=[
        ReportSection(
            heading="Executive Summary",
            content=("""
                On 2024-01-15, behavioral analysis detected anomalous activity from user
                jsmith (Department: Finance) involving unauthorized access to sensitive file
                shares and data exfiltration indicators. The anomaly score of 0.94 significantly
                exceeded the baseline threshold of 0.50. Investigation confirmed the account
                was compromised via credential stuffing.
            """)
        ),
        ReportSection(
            heading="Anomaly Details",
            template="anomaly_detail_table",
            data={
                "entity": "jsmith",
                "anomaly_score": 0.94,
                "severity": "critical",
                "detection_time": "2024-01-15T02:15:00Z",
                "dimensions_triggered": ["authentication", "file_access", "network"],
                "mitre_techniques": ["T1078", "T1083", "T1041"],
            }
        ),
        ReportSection(
            heading="Timeline of Events",
            template="timeline_table",
            events=[
                {"time": "02:15", "event": "Unusual login from 198.51.100.42", "risk": "high"},
                {"time": "02:18", "event": "Access to \\\\fileserver\\confidential", "risk": "high"},
                {"time": "02:22", "event": "File compression with rar.exe", "risk": "high"},
                {"time": "02:25", "event": "Outbound connection to mega.nz", "risk": "critical"},
                {"time": "02:30", "event": "52MB data transfer completed", "risk": "critical"},
            ]
        ),
        ReportSection(
            heading="Recommendations",
            content=("""
                1. Immediately disable jsmith account pending investigation
                2. Force password reset for all accounts in Finance department
                3. Review and restrict access to \\\\fileserver\\confidential
                4. Implement geographic-based login restrictions
                5. Deploy DLP rules for large outbound transfers to cloud storage
                6. Enable MFA for all Finance department users
            """)
        ),
    ]
)

report.export("IR-2024-089_behavioral_report.pdf")
report.export("IR-2024-089_behavioral_report.html")
print(f"Report generated: {report.output_path}")
```

## Related Modules

- **threat-intelligence**: Threat intelligence for context enrichment
- **ioc-analysis**: Indicator analysis for behavioral correlation
- **apt-detection**: Advanced persistent threat detection using behavioral patterns
