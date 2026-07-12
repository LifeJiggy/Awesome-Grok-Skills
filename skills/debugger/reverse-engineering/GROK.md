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