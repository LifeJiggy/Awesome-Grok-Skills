# Reverse Engineering Agent

> Binary analysis, disassembly, decompilation, malware analysis, and encryption detection platform.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Reverse Engineering Agent is a comprehensive binary analysis platform that provides binary file analysis (parsing, section layout, imports/exports, strings, protections), disassembly with function identification and control flow graph construction, pseudo-code decompilation, malware analysis with IOC extraction and YARA rule generation, encryption and encoding detection, and binary comparison. It is designed for security researchers, malware analysts, and reverse engineers.

### Design Principles

- **Static-Only Analysis**: No live execution — safe for malware analysis
- **Comprehensive Reporting**: Full analysis results in a single view
- **Extensible Architecture**: Plugin points for new file formats and architectures
- **Signature Generation**: Auto-generate YARA and Snort rules from analysis

---

## Features

| Feature | Description |
|---------|-------------|
| **Binary File Analysis** | Parse headers, map sections, extract imports/exports |
| **String Extraction** | Extract strings with type classification (URL, path, config, etc.) |
| **Protection Identification** | Detect ASLR, NX, Canary, RELRO, PIE, Fortify |
| **Import Analysis** | Categorize imports by function type (network, file, crypto, suspicious) |
| **Disassembly** | Decode x86/x86_64 instructions with category classification |
| **Function Identification** | Detect function boundaries and signatures |
| **CFG Construction** | Build control flow graphs from basic blocks |
| **Decompilation** | Generate pseudo-code from assembly |
| **Malware Analysis** | Analyze samples for behaviors, IOCs, and threat level |
| **YARA Rule Generation** | Auto-generate YARA rules from malware analysis |
| **Network Signatures** | Generate Snort/Suricata rules for C2 detection |
| **Encryption Detection** | Identify encryption algorithms and entropy |
| **Base64 Decoding** | Decode and validate Base64 encoded strings |
| **Binary Comparison** | Compare two binaries for similarities and differences |

---

## Quick Start

### Installation

```bash
# No external dependencies required
python agents/reverse-engineering/agent.py
```

### Basic Usage

```python
from agents.reverse_engineering.agent import ReverseEngineeringDashboard

dashboard = ReverseEngineeringDashboard()
results = dashboard.analyze_binary("/path/to/binary")
```

### First Binary Analysis

```python
from agents.reverse_engineering.agent import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Analyze a binary file
info = analyzer.analyze_file("/path/to/binary")
print(f"Architecture: {info.architecture}")
print(f"Entry Point: 0x{info.entry_point:x}")
print(f"Sections: {len(info.sections)}")
print(f"Imports: {len(info.imports)}")
print(f"Exports: {len(info.exports)}")

# Extract strings
strings = analyzer.extract_strings("/path/to/binary", min_length=6)
for s in strings:
    print(f"  [{s['type']}] 0x{s['address']:x}: {s['string']}")

# Identify protections
protections = analyzer.identify_protections("/path/to/binary")
print(f"Protections: {protections}")
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  ReverseEngineeringDashboard                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  BinaryAnalyzer   │  │DisassemblerEngine│  │MalwareEngine  │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌──────────────────┐                                            │
│  │EncryptionAnalyzer│                                            │
│  └──────────────────┘                                            │
└─────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system architecture.

---

## Usage

### Binary Analysis

```python
from agents.reverse_engineering.agent import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Full analysis
info = analyzer.analyze_file("/path/to/binary")

# Extract strings
strings = analyzer.extract_strings("/path/to/binary", min_length=4)

# Identify protections
protections = analyzer.identify_protections("/path/to/binary")

# Analyze imports
imports = analyzer.analyze_imports("/path/to/binary")
print(f"Suspicious: {imports['suspicious_imports']}")
print(f"Network: {imports['network_functions']}")
print(f"Crypto: {imports['crypto_functions']}")
```

### Disassembly

```python
from agents.reverse_engineering.agent import DisassemblerEngine, ArchType

engine = DisassemblerEngine()

# Disassemble code bytes
code = b'\x48\x89\xd8\x48\x8b\x00\xff\xd0\x84\xc0\x74\x05\xb8\x01\x00\x00\x00\xc3'
instructions = engine.disassemble(code, 0x401000, ArchType.X86_64)

for instr in instructions:
    print(f"0x{instr.address:x}: {instr.mnemonic} {', '.join(instr.operands)}")

# Identify functions
functions = engine.identify_functions(instructions)
for func in functions:
    print(f"{func.name}: 0x{func.address:x} ({func.size} bytes, {func.instructions} instructions)")

# Build CFG
cfg = engine.build_control_flow_graph(0x401000, instructions)
print(f"Nodes: {len(cfg['nodes'])}, Edges: {len(cfg['edges'])}")

# Decompile
decompilation = engine.decompile_function(0x401000)
print(decompilation)
```

### Malware Analysis

```python
from agents.reverse_engineering.agent import MalwareAnalysisEngine

malware = MalwareAnalysisEngine()

with open("/path/to/sample", "rb") as f:
    sample_data = f.read()

# Analyze sample
analysis = malware.analyze_sample("/path/to/sample", sample_data)
print(f"Threat Level: {analysis['threat_level']}")
print(f"Behaviors: {len(analysis['behaviors'])}")
print(f"IOCs: {len(analysis['iocs'])}")

# Generate YARA rules
yara = malware.extract_yara_rules(analysis)
print(yara)

# Generate network signatures
sigs = malware.generate_network_signatures(analysis)
for sig in sigs:
    print(f"  {sig['rule']}")
```

### Encryption Analysis

```python
from agents.reverse_engineering.agent import EncryptionAnalyzer

crypto = EncryptionAnalyzer()

# Identify encryption
data = b'\x00\x00\x00\x00' * 1024  # Sample data
analysis = crypto.identify_encryption(data)
print(f"Entropy: {analysis['entropy']}")
print(f"Likely encrypted: {analysis['likely_encrypted']}")

# Decode Base64
decoded = crypto.decode_base64_strings(data)
for d in decoded:
    print(f"  {d['encoded']} -> {d['decoded']}")
```

### Full Dashboard Analysis

```python
from agents.reverse_engineering.agent import ReverseEngineeringDashboard

dashboard = ReverseEngineeringDashboard()

# Complete binary analysis
results = dashboard.analyze_binary("/path/to/binary")
print(f"File: {results['file_info'].file_path}")
print(f"Arch: {results['file_info'].architecture}")
print(f"Entry: 0x{results['file_info'].entry_point:x}")
print(f"Strings: {len(results['strings'])}")
print(f"Functions: {len(results['functions'])}")
print(f"Decompilation:\n{results['decompilation']}")

# Malware analysis
malware_results = dashboard.malware_analysis("/path/to/sample", sample_data)
print(f"YARA Rules:\n{malware_results['yara_rules']}")

# Binary comparison
comparison = dashboard.compare_binaries("/path/to/binary1", "/path/to/binary2")
print(f"Similarity: {comparison['similarity_score']:.0%}")
```

---

## API Reference

| Class | Description |
|-------|-------------|
| `BinaryAnalyzer` | Binary file parsing, section mapping, strings, protections |
| `DisassemblerEngine` | Instruction decoding, function ID, CFG, decompilation |
| `MalwareAnalysisEngine` | Malware analysis, IOC extraction, YARA/Snort generation |
| `EncryptionAnalyzer` | Encryption detection, entropy analysis, Base64 decoding |
| `ReverseEngineeringDashboard` | Orchestrator combining all analyzers |

### Enums

| Enum | Values |
|------|--------|
| `ArchType` | X86, X86_64, ARM, ARM64, MIPS |
| `FileType` | EXECUTABLE, SHARED_OBJECT, STATIC_LIBRARY, KERNEL_MODULE, DOTNET_ASSEMBLY, JAVA_CLASS |
| `SectionType` | CODE, DATA, RODATA, BSS, IMPORT, EXPORT |

### Data Models

| Model | Key Fields |
|-------|------------|
| `BinaryInfo` | file_path, file_type, architecture, entry_point, sections, imports, exports |
| `FunctionInfo` | name, address, size, instructions, locals_size, arguments |
| `Instruction` | address, raw_bytes, mnemonic, operands, category |

---

## Examples

### Complete Malware Analysis Workflow

```python
from agents.reverse_engineering.agent import ReverseEngineeringDashboard

dashboard = ReverseEngineeringDashboard()

# 1. Analyze binary
results = dashboard.analyze_binary("/path/to/suspicious.exe")

# 2. Check protections
if not results['protections'].get('aslr'):
    print("WARNING: No ASLR — easier to exploit")

# 3. Check for suspicious imports
suspicious = results['imports']['suspicious_imports']
if suspicious:
    print(f"Suspicious imports: {suspicious}")

# 4. Analyze as malware
with open("/path/to/suspicious.exe", "rb") as f:
    data = f.read()

malware_results = dashboard.malware_analysis("/path/to/suspicious.exe", data)

# 5. Get IOCs
for ioc in malware_results['analysis']['iocs']:
    print(f"IOC: {ioc['type']} = {ioc['value']}")

# 6. Deploy detection
print(malware_results['yara_rules'])
```

### Binary Diffing

```python
from agents.reverse_engineering.agent import ReverseEngineeringDashboard

dashboard = ReverseEngineeringDashboard()

# Compare two versions of a binary
comparison = dashboard.compare_binaries("v1.0.exe", "v2.0.exe")

if comparison['same_architecture']:
    print("Same architecture — direct comparison valid")

print(f"Similarity: {comparison['similarity_score']:.0%}")
print(f"Common functions: {comparison['common_functions']}")
print(f"New in v2.0: {comparison['unique_to_binary2']}")
```

---

## Configuration

The agent uses default configuration suitable for most use cases. Key configurable parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Min string length | 4 | Minimum characters for string extraction |
| Architecture | X86_64 | Default disassembly architecture |
| Endianness | little | Default byte order |
| Entry point | 0x401000 | Default entry point address |
| Image base | 0x400000 | Default image base |

---

## Best Practices

### Binary Analysis
1. Always check protections before exploitation testing
2. Review import categories for risk assessment
3. Extract strings early — they often reveal functionality
4. Compare binaries to detect changes between versions

### Malware Analysis
1. **Never execute** malware samples — static analysis only
2. Generate YARA rules for future detection
3. Extract all IOCs for threat intelligence
4. Review behavioral analysis for kill chain mapping

### Disassembly
1. Start from the entry point and follow call graph
2. Identify key functions before deep analysis
3. Use CFG to understand control flow
4. Cross-reference function calls for data flow

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Binary parse fails | Check file format — may not be supported |
| No strings found | Lower min_length parameter |
| Disassembly looks wrong | Verify architecture and endianness |
| High entropy on all data | Binary may be packed — check for packing indicators |
| YARA rules too broad | Add more specific string patterns |

---

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation (all classes and logic) |
| `ARCHITECTURE.md` | System architecture with diagrams |
| `README.md` | This file — overview and quick start |

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

*Analyze binaries, detect malware, generate signatures with precision.*