---
name: "Reverse Engineering"
version: "2.0.0"
description: "Comprehensive reverse engineering toolkit with binary analysis, disassembly, protocol reverse engineering, API discovery, and malware analysis for security research and debugging"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["debugger", "reverse-engineering", "binary-analysis", "disassembly", "protocol-analysis", "security"]
category: "debugger"
personality: "reverse-engineer"
use_cases: ["binary analysis", "disassembly", "protocol reverse engineering", "API discovery", "malware analysis"]
---

# Reverse Engineering

> Production-grade reverse engineering framework providing binary analysis, disassembly, protocol reverse engineering, API discovery, and malware analysis for security research and debugging.

## Overview

The Reverse Engineering module provides tools for analyzing software without source code access. It implements binary analysis with architecture detection, disassembly and decompilation, protocol reverse engineering through traffic analysis, API endpoint discovery from compiled binaries, obfuscation detection, and malware analysis with indicator extraction. Every analysis produces structured reports with actionable findings.

## Core Capabilities

### 1. Binary Analysis
- File format detection (PE, ELF, Mach-O)
- Architecture detection (x86, ARM, MIPS)
- Entropy analysis for packed/encrypted sections
- Import/export table analysis
- Section header analysis

### 2. Disassembly and Decompilation
- Multi-architecture disassembly
- Control flow graph generation
- Function identification and labeling
- String extraction
- Constant propagation

### 3. Protocol Reverse Engineering
- Network protocol analysis
- Message format detection
- Encryption identification
- API endpoint discovery
- Authentication mechanism analysis

### 4. API Discovery
- REST API endpoint extraction from binaries
- GraphQL schema discovery
- gRPC service extraction
- WebSocket endpoint identification
- API version detection

### 5. Obfuscation Detection
- String obfuscation detection
- Control flow obfuscation
- Packing detection
- Anti-analysis technique identification
- Deobfuscation strategies

### 6. Malware Analysis
- Indicator of Compromise (IOC) extraction
- Behavioral analysis
- Network communication analysis
- Persistence mechanism detection
- Evasion technique identification

## Usage Examples

### Binary Analysis

```python
from reverse_engineering import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Analyze a binary file
analysis = analyzer.analyze("/path/to/binary")
print(f"Format: {analysis.format}")
print(f"Architecture: {analysis.architecture}")
print(f"Entrypoint: {analysis.entrypoint}")
print(f"Sections: {len(analysis.sections)}")

for section in analysis.sections:
    print(f"  {section.name}: {section.size_bytes} bytes, entropy={section.entropy:.2f}")
    if section.entropy > 7.0:
        print(f"    ⚠ High entropy — may be packed/encrypted")
```

### Protocol Reverse Engineering

```python
from reverse_engineering import ProtocolAnalyzer

analyzer = ProtocolAnalyzer()

# Analyze captured traffic
protocol = analyzer.analyze_traffic(packets)
print(f"Detected protocol: {protocol.name}")
print(f"Message types: {protocol.message_types}")
print(f"Encryption: {protocol.encryption_type}")
print(f"Authentication: {protocol.auth_mechanism}")

print("Message format:")
for msg_type, fields in protocol.message_formats.items():
    print(f"  {msg_type}:")
    for field in fields:
        print(f"    {field.name}: {field.type} ({field.size} bytes)")
```

### API Discovery

```python
from reverse_engineering import APIDiscovery

discovery = APIDiscovery()

# Extract APIs from binary
apis = discovery.extract_from_binary("/path/to/server")
print(f"REST endpoints: {len(apis.rest_endpoints)}")
print(f"GraphQL schemas: {len(apis.graphql_schemas)}")
print(f"gRPC services: {len(apis.grpc_services)}")

for endpoint in apis.rest_endpoints[:10]:
    print(f"  {endpoint.method} {endpoint.path}")
    print(f"    Parameters: {endpoint.parameters}")
    print(f"    Auth: {endpoint.auth_required}")
```

### Obfuscation Detection

```python
from reverse_engineering import ObfuscationDetector

detector = ObfuscationDetector()

# Detect obfuscation techniques
detection = detector.detect("/path/to/binary")
print(f"Obfuscation score: {detection.score}/10")
print(f"Techniques detected:")
for technique in detection.techniques:
    print(f"  {technique.name}: {technique.description}")
    print(f"    Confidence: {technique.confidence:.1%}")
    print(f"    Mitigation: {technique.mitigation}")
```

## Best Practices

### Binary Analysis
- Always analyze in a sandboxed environment
- Use multiple analysis tools for cross-validation
- Check for anti-analysis techniques before deep analysis
- Preserve original binaries with checksums

### Protocol Reverse Engineering
- Capture traffic from multiple sessions
- Look for patterns in message structures
- Identify encryption before attempting decryption
- Document protocol state machines

### API Discovery
- Combine static and dynamic analysis
- Test discovered endpoints in a safe environment
- Check for version differences
- Verify authentication requirements

### Malware Analysis
- Never execute malware on production systems
- Use network isolation for behavioral analysis
- Extract IOCs before full analysis
- Document all findings with evidence

## Related Modules

- **crash-analysis**: Binary crash analysis and debugging
- **network-debugging**: Network traffic analysis
- **dynamic-analysis**: Runtime behavior analysis
- **security-hardening**: Security configuration analysis

---

## Advanced Configuration

### Advanced Binary Analysis

```python
from reverse_engineering import BinaryAnalyzer, AnalysisConfig

analyzer = BinaryAnalyzer(
    config=AnalysisConfig(
        deep_analysis=True,
        check_packing=True,
        check_obfuscation=True,
        extract_strings=True,
        min_string_length=4,
        analyze_imports=True,
        analyze_exports=True,
        calculate_entropy=True,
    ),
)

# Comprehensive binary analysis
analysis = analyzer.analyze_comprehensive("/path/to/binary")
print(f"Format: {analysis.format}")
print(f"Architecture: {analysis.architecture}")
print(f"Compiler: {analysis.compiler}")
print(f"Packers detected: {analysis.packers}")
print(f"Obfuscation score: {analysis.obfuscation_score}/10")

print("\nSections:")
for section in analysis.sections:
    print(f"  {section.name}: {section.size_bytes} bytes, entropy={section.entropy:.2f}")
    if section.entropy > 7.0:
        print(f"    High entropy - may be packed/encrypted")

print("\nImports:")
for imp in analysis.imports[:20]:
    print(f"  {imp.library}: {imp.name}")
```

### Advanced Protocol Reverse Engineering

```python
from reverse_engineering import ProtocolAnalyzer, ProtocolConfig

analyzer = ProtocolAnalyzer(
    config=ProtocolConfig(
        detect_encryption=True,
        identify_message_types=True,
        analyze_state_machine=True,
        extract_api_endpoints=True,
        detect_authentication=True,
    ),
)

# Analyze protocol from traffic
protocol = analyzer.analyze_traffic(
    packets,
    output_format="protobuf",
    generate_client=True,
    generate_server=True,
)

print(f"Protocol: {protocol.name}")
print(f"Message types: {len(protocol.message_types)}")
print(f"Encryption: {protocol.encryption_type}")
print(f"Authentication: {protocol.auth_mechanism}")

print("\nMessage formats:")
for msg_type, fields in protocol.message_formats.items():
    print(f"  {msg_type}:")
    for field in fields:
        print(f"    {field.name}: {field.type} ({field.size} bytes)")

# Generate protocol documentation
protocol.generate_documentation("protocol_doc.md")
```

### Advanced API Discovery

```python
from reverse_engineering import APIDiscovery, DiscoveryConfig

discovery = APIDiscovery(
    config=DiscoveryConfig(
        extract_from_binary=True,
        extract_from_config=True,
        extract_from_strings=True,
        detect_versioning=True,
        analyze_auth=True,
        generate_openapi=True,
    ),
)

# Extract APIs from multiple sources
apis = discovery.extract_comprehensive(
    binary="/path/to/server",
    config_files=["/path/to/config.yaml"],
    documentation=["/path/to/docs"],
)

print(f"REST endpoints: {len(apis.rest_endpoints)}")
print(f"GraphQL schemas: {len(apis.graphql_schemas)}")
print(f"gRPC services: {len(apis.grpc_services)}")
print(f"WebSocket endpoints: {len(apis.websocket_endpoints)}")

for endpoint in apis.rest_endpoints[:10]:
    print(f"\n  {endpoint.method} {endpoint.path}")
    print(f"    Parameters: {endpoint.parameters}")
    print(f"    Auth: {endpoint.auth_required}")
    print(f"    Rate limit: {endpoint.rate_limit}")

# Generate OpenAPI spec
discovery.generate_openapi(apis, "openapi.yaml")
```

### Advanced Malware Analysis

```python
from reverse_engineering import MalwareAnalyzer, AnalysisConfig

analyzer = MalwareAnalyzer(
    config=AnalysisConfig(
        sandbox_execution=True,
        network_capture=True,
        behavioral_analysis=True,
        extract_indicators=True,
        detect_evasion=True,
    ),
)

# Analyze malware sample
analysis = analyzer.analyze_comprehensive("/path/to/malware.exe")
print(f"Malware type: {analysis.malware_type}")
print(f"Risk score: {analysis.risk_score}/10")
print(f"Family: {analysis.family}")

print("\nIndicators of Compromise (IOCs):")
for ioc in analysis.iocs:
    print(f"  {ioc.type}: {ioc.value} (confidence: {ioc.confidence:.1%})")

print("\nBehavior:")
for behavior in analysis.behaviors:
    print(f"  {behavior.category}: {behavior.description}")
    print(f"    Technique: {behavior.technique}")
    print(f"    Evidence: {behavior.evidence}")

print("\nNetwork activity:")
for conn in analysis.network_connections:
    print(f"  {conn.protocol} {conn.dst_ip}:{conn.dst_port}")
    print(f"    C2 server: {conn.is_c2}")
```

## Architecture Patterns

### Reverse Engineering Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Reverse Engineering Architecture               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Static Analysis Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Binary     │  │  Disassembly│  │  Decompila-  │ │   │
│  │  │  Parsing    │  │  Engine     │  │  tion        │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Dynamic Analysis Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Debugger   │  │  Emulator   │  │  Sandboxed  │ │   │
│  │  │  Integration│  │             │  │  Execution  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Analysis Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Pattern    │  │  Protocol   │  │  Behavior   │ │   │
│  │  │  Matching   │  │  Analysis   │  │  Analysis   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Malware Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Malware Analysis Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│  1. Sample Acquisition                                     │
│     └─► Safe download, hash verification                    │
│  2. Static Analysis                                        │
│     └─► Binary parsing, string extraction, YARA rules       │
│  3. Dynamic Analysis                                        │
│     └─► Sandboxed execution, behavior monitoring            │
│  4. Network Analysis                                        │
│     └─► Traffic capture, C2 detection                       │
│  5. Indicator Extraction                                    │
│     └─► IOCs, TTPs, behavioral patterns                     │
│  6. Classification                                          │
│     └─► Malware family, risk scoring                        │
│  7. Reporting                                                │
│     └─► Structured report, recommendations                  │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with CI/CD
from reverse_engineering import BinaryAnalyzer, APIDiscovery

def security_scan(binary_path: str):
    analyzer = BinaryAnalyzer()
    analysis = analyzer.analyze(binary_path)
    
    # Check for security issues
    issues = []
    if analysis.has_nx:
        issues.append("NX bit not enabled")
    if analysis.has_aslr:
        issues.append("ASLR not enabled")
    if analysis.has_stack_canary:
        issues.append("Stack canary not present")
    
    return {
        "binary": binary_path,
        "security_score": analysis.security_score,
        "issues": issues,
    }

# API discovery for documentation
def discover_apis(binary_path: str):
    discovery = APIDiscovery()
    apis = discovery.extract_from_binary(binary_path)
    return discovery.generate_openapi(apis)
```

### Prometheus Integration

```python
from prometheus_client import Counter, Gauge

BINARY_ANALYSIS = Counter('binary_analysis_total', 'Binary analyses', ['result'])
SECURITY_SCORE = Gauge('binary_security_score', 'Security score', ['binary'])

class REMetrics:
    def __init__(self, analyzer: BinaryAnalyzer):
        self.analyzer = analyzer
    
    def record_analysis(self, binary: str, result: str):
        BINARY_ANALYSIS.labels(result=result).inc()
        
        analysis = self.analyzer.analyze(binary)
        SECURITY_SCORE.labels(binary=binary).set(analysis.security_score)
```

## Performance Optimization

### Analysis Performance

| Technique | Time | Accuracy | Use Case |
|-----------|------|----------|----------|
| String extraction | Fast | Low | Quick triage |
| Import analysis | Fast | Medium | Functionality mapping |
| Disassembly | Slow | High | Deep analysis |
| Decompilation | Very Slow | High | Code understanding |
| Dynamic analysis | Slow | High | Behavior analysis |

### Optimized Analysis

```python
from reverse_engineering import OptimizedAnalyzer

analyzer = OptimizedAnalyzer()

# Configure for speed
analyzer.configure(
    quick_scan=True,
    skip_decompilation=True,
    parallel_analysis=True,
    max_workers=4,
    cache_results=True,
)

# Quick scan
result = analyzer.quick_scan("/path/to/binary")
print(f"Quick scan: {result.security_score}/10")
print(f"Suspicious: {result.is_suspicious}")
```

## Security Considerations

### Safe Analysis Environment

```python
from reverse_engineering import SandboxConfig

sandbox = SandboxConfig(
    # Network isolation
    network_isolation=True,
    allowed_hosts=[],
    
    # File system isolation
    read_only_filesystem=True,
    temp_directory="/tmp/sandbox",
    
    # Resource limits
    max_memory_mb=512,
    max_cpu_seconds=60,
    max_disk_mb=100,
    
    # Monitoring
    monitor_syscalls=True,
    monitor_network=True,
    monitor_file_access=True,
)

# Analyze in sandbox
with analyzer.sandbox(sandbox) as env:
    result = env.analyze("/path/to/malware.exe")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Analysis timeout | Long-running analysis | Increase timeout, use quick scan |
| Memory exhaustion | OOM during analysis | Limit analysis depth, use sampling |
| False positives | Incorrect classification | Tune detection rules, verify manually |
| Anti-analysis | Sample detects analysis | Use anti-evasion techniques |
| Packed binaries | Cannot analyze | Unpack first, use dynamic analysis |

### Diagnostic Queries

```python
# Check analysis status
from reverse_engineering import AnalysisStatus

status = AnalysisStatus()
check = status.check()
print(f"Analysis engine: {check.engine_status}")
print(f"Rules version: {check.rules_version}")
print(f"Database version: {check.database_version}")
```

## API Reference

### BinaryAnalyzer

```python
class BinaryAnalyzer:
    def __init__(self, config: AnalysisConfig = None)
    def analyze(self, binary_path: str) -> BinaryAnalysis
    def analyze_comprehensive(self, binary_path: str) -> ComprehensiveAnalysis
    def extract_strings(self, binary_path: str, min_length: int = 4) -> list[str]
    def calculate_entropy(self, binary_path: str) -> float
    def check_packing(self, binary_path: str) -> PackerResult
```

### ProtocolAnalyzer

```python
class ProtocolAnalyzer:
    def __init__(self, config: ProtocolConfig = None)
    def analyze_traffic(self, packets: list, **kwargs) -> Protocol
    def detect_protocol(self, packets: list) -> str
    def extract_message_formats(self, packets: list) -> dict
    def generate_client(self, protocol: Protocol, language: str = "python") -> str
    def generate_server(self, protocol: Protocol, language: str = "python") -> str
```

### APIDiscovery

```python
class APIDiscovery:
    def __init__(self, config: DiscoveryConfig = None)
    def extract_from_binary(self, binary_path: str) -> APIList
    def extract_from_config(self, config_path: str) -> APIList
    def extract_comprehensive(self, **kwargs) -> APIList
    def generate_openapi(self, apis: APIList, output_path: str)
    def generate_documentation(self, apis: APIList, output_path: str)
```

### MalwareAnalyzer

```python
class MalwareAnalyzer:
    def __init__(self, config: AnalysisConfig = None)
    def analyze(self, sample_path: str) -> MalwareAnalysis
    def analyze_comprehensive(self, sample_path: str) -> ComprehensiveAnalysis
    def extract_indicators(self, sample_path: str) -> list[IOC]
    def classify(self, sample_path: str) -> Classification
    def detect_evasion(self, sample_path: str) -> EvasionResult
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class BinaryFormat(Enum):
    PE = "pe"
    ELF = "elf"
    MACH_O = "mach_o"
    UNKNOWN = "unknown"

class Architecture(Enum):
    X86 = "x86"
    X86_64 = "x86_64"
    ARM = "arm"
    ARM64 = "arm64"
    MIPS = "mips"

@dataclass
class BinaryAnalysis:
    path: str
    format: BinaryFormat
    architecture: Architecture
    entrypoint: int
    sections: List['Section']
    imports: List['Import']
    exports: List['Export']
    strings: List[str]
    entropy: float
    security_score: float

@dataclass
class Section:
    name: str
    virtual_address: int
    size_bytes: int
    entropy: float
    characteristics: List[str]

@dataclass
class IOC:
    type: str
    value: str
    confidence: float
    context: str

@dataclass
class MalwareAnalysis:
    sample_path: str
    malware_type: str
    risk_score: float
    family: str
    iocs: List[IOC]
    behaviors: List['Behavior']
    network_connections: List['NetworkConnection']
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  reverse-engineering:
    image: reverse-engineering:latest
    volumes:
      - ./samples:/samples
      - ./output:/output
    environment:
      ANALYSIS_MODE: "safe"
      SANDBOX_ENABLED: "true"
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'
```

## Monitoring & Observability

### Metrics Collection

```python
from reverse_engineering import MetricsCollector

collector = MetricsCollector()

# Collect analysis metrics
collector.counter("re.analyses.total", count, tags={"result": result})
collector.histogram("re.analysis.duration.seconds", duration)
collector.gauge("re.security.score", score, tags=["binary": binary])
collector.counter("re.iocs.extracted", count, tags={"type": ioc_type})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from reverse_engineering import BinaryAnalyzer, APIDiscovery

@pytest.fixture
def analyzer():
    return BinaryAnalyzer()

def test_binary_analysis(analyzer):
    analysis = analyzer.analyze("test_binary")
    assert analysis.format in [BinaryFormat.PE, BinaryFormat.ELF]

def test_api_discovery():
    discovery = APIDiscovery()
    apis = discovery.extract_from_binary("test_server")
    assert len(apis.rest_endpoints) >= 0
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |
| Radare2 | 5.0 | 5.8+ |
| Ghidra | 10.0 | 11.0+ |

## Glossary

| Term | Definition |
|------|------------|
| **IOC** | Indicator of Compromise |
| **TTP** | Tactics, Techniques, and Procedures |
| **YARA** | Pattern matching tool for malware |
| **PE** | Portable Executable (Windows) |
| **ELF** | Executable and Linkable Format (Linux) |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added malware analysis
- New protocol reverse engineering
- Improved API discovery
- Added sandbox execution

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/reverse-engineering.git
cd reverse-engineering
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills