# Reverse Engineering Agent — System Architecture

## 1. Executive Summary

The Reverse Engineering Agent is a comprehensive binary analysis platform providing binary file analysis, disassembly, decompilation, malware analysis, encryption detection, and network signature generation. It is designed for security researchers, malware analysts, and reverse engineers.

---

## 2. Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Component Deep Dives](#3-component-deep-dives)
4. [Data Flow Diagrams](#4-data-flow-diagrams)
5. [Design Patterns](#5-design-patterns)
6. [Tech Stack](#6-tech-stack)
7. [Security Considerations](#7-security-considerations)
8. [Scalability & Performance](#8-scalability--performance)
9. [Integration Points](#9-integration-points)
10. [Data Models](#10-data-models)
11. [Extension Points](#11-extension-points)
12. [Glossary](#12-glossary)
13. [Appendix: Design Decisions](#13-appendix-design-decisions)

---

## 3. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    REVERSE ENGINEERING AGENT                              │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │  BinaryAnalyzer   │  │DisassemblerEngine│  │MalwareAnalysisEngine │  │
│  │                   │  │                   │  │                      │  │
│  │ • File parsing    │  │ • Instruction     │  │ • Sample analysis    │  │
│  │ • Section layout  │  │   decoding        │  │ • Behavior detection │  │
│  │ • Import/Export   │  │ • Function ID     │  │ • IOC extraction     │  │
│  │ • String extract  │  │ • CFG building    │  │ • YARA generation    │  │
│  │ • Protections     │  │ • Decompilation   │  │ • Network signatures │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘  │
│                                                                          │
│  ┌──────────────────┐                                                   │
│  │EncryptionAnalyzer │                                                   │
│  │                   │                                                   │
│  │ • Algorithm ID    │                                                   │
│  │ • Entropy analysis│                                                   │
│  │ • Base64 decode   │                                                   │
│  │ • Encoding ID     │                                                   │
│  └──────────────────┘                                                   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              ReverseEngineeringDashboard (Orchestrator)           │   │
│  │  • Full binary analysis  • Malware analysis  • Binary comparison │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Deep Dives

### 4.1 BinaryAnalyzer

Binary file analysis with section layout, imports, exports, strings, and protection identification.

**Responsibilities:**
- Parse binary file headers and identify file type
- Map memory sections (.text, .data, .rodata, .bss, etc.)
- Extract and categorize imported functions
- Extract strings with type classification (ASCII, URL, path, config, debug)
- Identify binary protections (ASLR, NX, Canary, RELRO, PIE, Fortify)

**Binary Analysis Pipeline:**
```
Raw Binary ──→ Parse Header ──→ Map Sections ──→ Extract Imports ──→ Export Results
                    │                │                │
                    ▼                ▼                ▼
               Identify        Classify        Categorize
               Format          Permissions     by Function
                               (R/W/X)         Type
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `analyze_file(file_path)` | Perform full binary analysis |
| `extract_strings(file_path, min_length)` | Extract strings from binary |
| `identify_protections(binary_path)` | Identify security protections |
| `analyze_imports(binary_path)` | Analyze imported functions by category |

---

### 4.2 DisassemblerEngine

Disassembly, function identification, control flow graph construction, and decompilation.

**Responsibilities:**
- Decode machine instructions to assembly mnemonics
- Identify function boundaries and signatures
- Build control flow graphs (CFG) from basic blocks
- Generate pseudo-code decompilation
- Classify instructions by category (data transfer, arithmetic, control flow, etc.)

**Disassembly Pipeline:**
```
Code Bytes ──→ Decode Instructions ──→ Identify Functions ──→ Build CFG ──→ Decompile
                    │                       │                    │
                    ▼                       ▼                    ▼
              Classify                Entry/Exit           Nodes/Edges
              Categories              Detection            Loop Detection
```

**Instruction Categories:**
```
┌─────────────────┬──────────────────────────────────────────┐
│ Category        │ Instructions                             │
├─────────────────┼──────────────────────────────────────────┤
│ data_transfer   │ mov, push, pop, lea, xchg               │
│ arithmetic      │ add, sub, mul, div, inc, dec, cmp        │
│ logical         │ and, or, xor, not, shl, shr              │
│ control_flow    │ call, ret, jmp, je, jne, jg, jl          │
│ stack           │ push, pop, enter, leave                  │
│ string          │ movsb, movsw, cmpsb, scasb               │
│ nop             │ nop, int3                                │
└─────────────────┴──────────────────────────────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `disassemble(code_bytes, start_address, architecture)` | Decode instructions |
| `identify_functions(instructions)` | Find function boundaries |
| `build_control_flow_graph(start_address, instructions)` | Construct CFG |
| `decompile_function(address)` | Generate pseudo-code |

---

### 4.3 MalwareAnalysisEngine

Malware sample analysis with behavior detection, IOC extraction, and signature generation.

**Responsibilities:**
- Analyze malware samples for behaviors and indicators
- Extract IOCs (file hashes, domains, IPs, URLs)
- Generate YARA rules for detection
- Create network detection signatures (Snort/Suricata)
- Classify threat level and detection rate

**Malware Analysis Pipeline:**
```
Sample ──→ Static Analysis ──→ Dynamic Analysis ──→ IOC Extraction ──→ Signature Generation
              │                      │                    │                    │
              ▼                      ▼                    ▼                    ▼
         Strings, imports      File/registry/        Hash, domain,      YARA rules,
         Entropy check         network activity     IP extraction      Snort rules
```

**Behavior Categories:**
```
┌─────────────────────┬──────────────────────────────────────┐
│ Behavior            │ Indicators                           │
├─────────────────────┼──────────────────────────────────────┤
│ Persistence         │ Registry keys, startup entries       │
│ Privilege Escalation│ UAC bypass, token manipulation      │
│ Defense Evasion     │ Packing, obfuscation, anti-debug     │
│ Credential Access   │ Keylogging, credential dumping       │
│ Discovery           │ System/network enumeration           │
│ Lateral Movement    │ SMB, RDP, PsExec usage              │
│ Collection          │ Screenshot, keylogging, data staging │
│ C2 Communication    │ HTTP/DNS/IRC beacons                │
│ Exfiltration        │ Data upload, DNS tunneling          │
│ Impact              │ Ransomware, data destruction         │
└─────────────────────┴──────────────────────────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `analyze_sample(sample_path, sample_data)` | Full malware analysis |
| `extract_yara_rules(sample_analysis)` | Generate YARA detection rules |
| `generate_network_signatures(analysis)` | Create Snort/Suricata rules |

---

### 4.4 EncryptionAnalyzer

Encryption and encoding identification with entropy analysis and decoding.

**Responsibilities:**
- Identify encryption algorithms used in binaries
- Calculate Shannon entropy to detect encrypted/compressed data
- Decode Base64 encoded strings
- Identify encoding schemes (Base64, Hex, URL encoding, etc.)

**Entropy Analysis:**
```
Entropy Range    │ Classification
─────────────────┼───────────────────────────────
0.0 - 4.0       │ Low entropy (code, text)
4.0 - 6.0       │ Medium entropy (compressed)
6.0 - 7.5       │ High entropy (compressed/encoded)
7.5 - 8.0       │ Very high (likely encrypted)
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `identify_encryption(data)` | Detect encryption type and entropy |
| `decode_base64_strings(data)` | Decode Base64 encoded strings |
| `identify_encoding(data)` | Identify encoding scheme |

---

## 5. Data Flow Diagrams

### 5.1 Full Binary Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FULL BINARY ANALYSIS PIPELINE                         │
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  Binary   │    │ Binary   │    │Disassem- │    │ Malware  │          │
│  │  Input    │───▶│ Analyzer │───▶│ bler     │───▶│ Analyzer │          │
│  │          │    │          │    │ Engine   │    │          │          │
│  │ • File   │    │ • Parse  │    │ • Decode │    │ • Sample │          │
│  │ • Bytes  │    │ • Layout │    │ • Funcs  │    │ • Behave │          │
│  │          │    │ • Imports│    │ • CFG    │    │ • IOCs   │          │
│  │          │    │ • Strings│    │ • Decomp │    │ • YARA   │          │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │
│       │               │               │               │                  │
│       └───────────────┴───────────────┴───────────────┘                  │
│                              │                                           │
│                              ▼                                           │
│                    ┌──────────────────┐                                  │
│                    │    Dashboard     │                                  │
│                    │                  │                                  │
│                    │ • File info      │                                  │
│                    │ • Protections    │                                  │
│                    │ • Strings        │                                  │
│                    │ • Imports        │                                  │
│                    │ • Functions      │                                  │
│                    │ • CFG            │                                  │
│                    │ • Decompiled     │                                  │
│                    │ • YARA rules     │                                  │
│                    └──────────────────┘                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Malware Analysis Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  MALWARE ANALYSIS FLOW                           │
│                                                                  │
│  Sample ──→ Static ──→ Dynamic ──→ IOC ──→ Signature            │
│              │            │           │         │                │
│              ▼            ▼           ▼         ▼                │
│          Strings       Behavior    Extract   Generate            │
│          Imports       Tracking    Hashes    YARA/Snort          │
│          Entropy       File ops    Domains                       │
│          Sections      Registry    IPs                           │
│                        Network     URLs                          │
│                        Processes                                 │
│                                                                  │
│  Output:                                                         │
│    • Threat level (low/medium/high/critical)                     │
│    • Detection rate                                              │
│    • IOC list (MD5, SHA256, domains, IPs)                       │
│    • YARA rules                                                  │
│    • Network signatures                                          │
│    • Behavioral summary                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Control Flow Graph Construction

```
┌─────────────────────────────────────────────────────────────┐
│                  CFG CONSTRUCTION                             │
│                                                              │
│  Instructions ──→ Basic Block Detection ──→ Edge Detection  │
│                        │                        │           │
│                        ▼                        ▼           │
│                   Split at:                Connect:         │
│                   • Branches               • Fall-through   │
│                   • Calls                  • Conditional    │
│                   • Returns                • Unconditional  │
│                        │                        │           │
│                        └────────┬───────────────┘           │
│                                 │                            │
│                                 ▼                            │
│                        ┌──────────────┐                     │
│                        │   CFG Graph  │                     │
│                        │              │                     │
│                        │  Nodes:      │                     │
│                        │   - Entry    │                     │
│                        │   - Then     │                     │
│                        │   - Else     │                     │
│                        │   - Exit     │                     │
│                        │              │                     │
│                        │  Edges:      │                     │
│                        │   - Cond     │                     │
│                        │   - Uncond   │                     │
│                        │   - Fallthru │                     │
│                        └──────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Facade** | Unified interface via Dashboard | ReverseEngineeringDashboard |
| **Strategy** | Multiple analysis approaches | BinaryAnalyzer, MalwareAnalysisEngine |
| **Factory** | Instruction creation from bytes | DisassemblerEngine |
| **Builder** | CFG construction from instructions | DisassemblerEngine |
| **Template Method** | Analysis pipeline stages | MalwareAnalysisEngine |
| **Decorator** | Entropy analysis wraps raw data | EncryptionAnalyzer |
| **Composite** | Dashboard composes all analyzers | ReverseEngineeringDashboard |

---

## 7. Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Structures | dataclasses, Enum, Dict, List |
| Binary Parsing | struct module (implied) |
| Base64 | base64 module |
| Math | math (log2 for entropy) |
| Date/Time | datetime |
| Logging | Python logging |
| Optional | capstone (disassembly), yara-python, pefile, lief |

---

## 8. Security Considerations

- **Sandboxed Execution**: Malware analysis should occur in isolated environments
- **No Live Execution**: Sample analysis is static-only in this agent
- **Input Validation**: File paths and binary data validated before processing
- **Resource Limits**: String extraction and disassembly bounded by file size
- **Entropy Thresholds**: Configurable thresholds for encrypted data detection
- **Signature Safety**: Generated YARA/Snort rules should be reviewed before deployment

---

## 9. Scalability & Performance

| Operation | Target | Notes |
|-----------|--------|-------|
| Binary parse | < 100ms | Header + sections + imports |
| String extraction | < 50ms | Linear scan with min length filter |
| Protection ID | < 10ms | Header flag checks |
| Import analysis | < 20ms | Categorization of import list |
| Disassembly | < 200ms | 4KB code block |
| Function identification | < 100ms | Pattern-based |
| CFG construction | < 150ms | Basic block detection + edges |
| Decompilation | < 100ms | Pseudo-code generation |
| Malware analysis | < 500ms | Static analysis only |
| YARA rule generation | < 10ms | Template-based |
| Full analysis | < 1s | All components combined |

---

## 10. Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION ARCHITECTURE                       │
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  File System │ ◀─────▶ │  Binary      │                      │
│  │  (Input)     │  read   │  Analyzer    │                      │
│  └──────────────┘         └──────────────┘                      │
│         │                       │                                │
│         │                       │                                │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  YARA        │ ◀─────▶ │  Malware     │                      │
│  │  Rules       │  output │  Analyzer    │                      │
│  │  Repository  │         │              │                      │
│  └──────────────┘         └──────────────┘                      │
│         │                       │                                │
│         │                       │                                │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  SIEM/IDS    │ ◀───── │  Network     │                      │
│  │  (Snort)     │  rules  │  Signatures  │                      │
│  └──────────────┘         └──────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. Data Models

### Core Entities

```
┌─────────────────┐     ┌─────────────────┐
│   BinaryInfo    │     │  FunctionInfo   │
│                 │     │                 │
│ • file_path     │     │ • name          │
│ • file_type     │     │ • address       │
│ • architecture  │     │ • size          │
│ • endianness    │     │ • instructions  │
│ • entry_point   │     │ • locals_size   │
│ • image_base    │     │ • arguments     │
│ • sections      │     └─────────────────┘
│ • imports       │
│ • exports       │     ┌─────────────────┐
└─────────────────┘     │  Instruction    │
                        │                 │
                        │ • address       │
                        │ • raw_bytes     │
                        │ • mnemonic      │
                        │ • operands      │
                        │ • category      │
                        └─────────────────┘

┌─────────────────┐     ┌─────────────────┐
│ MalwareAnalysis │     │EncryptionAnalysis│
│                 │     │                 │
│ • sample_path   │     │ • encryption    │
│ • file_size     │     │   _type         │
│ • threat_level  │     │ • key_size      │
│ • behaviors     │     │ • entropy       │
│ • iocs          │     │ • iv_present    │
│ • network_ind.  │     │ • likely_       │
│ • static        │     │   encrypted     │
│ • dynamic       │     └─────────────────┘
└─────────────────┘
```

---

## 12. Extension Points

1. **Custom File Formats**: Extend FileType for new binary formats (ELF, PE, Mach-O, .NET, Java)
2. **Additional Architectures**: Add ARM, MIPS, RISC-V support to DisassemblerEngine
3. **Dynamic Analysis**: Integrate sandbox for runtime behavior monitoring
4. **Custom YARA Templates**: User-defined YARA rule generation templates
5. **Binary Diffing**: Enhanced binary comparison with patch analysis
6. **Symbol Resolution**: DB integration for function name resolution
7. **Emulation**: CPU emulation for shellcode analysis
8. **Network PCAP Analysis**: Integrate packet capture analysis

---

## 13. Glossary

| Term | Definition |
|------|-----------|
| CFG | Control Flow Graph — graph of basic blocks and edges |
| IOC | Indicator of Compromise — artifact indicating malicious activity |
| YARA | Pattern matching tool for malware classification |
| ASLR | Address Space Layout Randomization |
| NX | No-eXecute bit — prevents code execution in data pages |
| Canary | Stack canary — stack buffer overflow protection |
| RELRO | Relocation Read-Only — GOT protection |
| PIE | Position Independent Executable |
| JA3 | TLS client fingerprinting |
| Entropy | Measure of randomness in data (0-8 scale) |
| PE | Portable Executable — Windows binary format |
| ELF | Executable and Linkable Format — Linux binary format |

---

## 14. Appendix: Design Decisions

| Decision | Rationale |
|----------|-----------|
| Static-only analysis | Safety — no risk of malware execution |
| Sequential function IDs | Simple, human-readable |
| Pseudo-code decompilation | Readable output without full decompiler |
| Entropy-based encryption detection | Fast, reliable heuristic |
| Template-based YARA generation | Consistent, reviewable output |
| In-memory analysis | Simplicity; disk persistence optional |
| Categorized imports | Enables quick risk assessment |
| CFG with basic blocks | Industry standard for binary analysis |
