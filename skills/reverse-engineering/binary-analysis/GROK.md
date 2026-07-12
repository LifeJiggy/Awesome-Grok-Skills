---
name: "binary-analysis"
category: "reverse-engineering"
version: "1.0.0"
tags: ["reverse-engineering", "binary-analysis", "elf", "pe", "disassembly"]
---

# Binary Analysis — Reverse Engineering Module

## Overview

Binary analysis is the foundation of reverse engineering — the discipline of understanding compiled executables without access to source code. This module provides systematic techniques for dissecting ELF (Linux), PE (Windows), and Mach-O (macOS) binaries to extract their structure, behavior, and embedded secrets.

Binary analysis spans multiple layers: static analysis (examining the file without execution), dynamic analysis (observing runtime behavior through debugging and tracing), and hybrid approaches that combine both. The goal is to answer questions like: What does this binary do? What libraries does it depend on? Where are its entry points? What data does it reference? Are there hidden strings, configuration, or anti-analysis measures?

This module integrates with industry-standard tools (Radare2, Ghidra headless, Capstone, LIEF, pefile) and provides Python-native analysis pipelines that can be scripted, automated, and integrated into CI/CD or threat intelligence workflows. Whether you are a security researcher analyzing malware, a developer debugging a crash, a CTF player solving a challenge, or an auditor performing a code review on a closed-source component, this module gives you the tools and methodology to work with binaries effectively.

Key architectural decisions in this module emphasize reproducibility, structured output (JSON/dict-based results), and composability — every analysis function returns typed results that can be fed into downstream pipelines or reports.

## Core Capabilities

### 1. File Format Parsing
Detect and parse binary file formats — ELF headers, PE optional headers, section tables, import/export tables, debug symbols, and overlay data. Extract metadata such as compiler, architecture, linked libraries, and compilation timestamps.

### 2. Disassembly and Disassembly Flow
Disassemble code sections using Capstone or Radare2 backends. Reconstruct control flow graphs, identify function boundaries, detect syscall wrappers, and trace execution paths through indirect calls and jumps.

### 3. String and Data Extraction
Extract ASCII, Unicode, and encoded strings from binaries. Identify base64 blobs, XOR-encoded payloads, embedded file magic bytes (PE, ZIP, ELF headers inside the binary), and structured configuration data.

### 4. Import/Export Analysis
Map the binary's external dependencies through its Import Address Table (IAT) or GOT. Identify API usage patterns indicative of specific behaviors (network communication, file I/O, cryptographic operations, anti-debugging checks).

### 5. Entropy and Packing Detection
Calculate Shannon entropy across binary regions to identify packed, encrypted, or compressed sections. Detect common packers (UPX, Themida, VMProtect) and distinguish between compressed data and encrypted payloads.

### 6. Symbol and Debug Information
Parse DWARF debug info, PDB data (via `pdb` or `lief`), and COFF symbol tables to recover function names, source file references, and type information when available.

### 7. Binary Diffing
Compare two versions of a binary (or a binary against a known-good baseline) to identify changed functions, new imports, or patched vulnerabilities using techniques like hash-based function matching and structural diffing.

### 8. YARA and Signature Matching
Apply YARA rules against binary sections, memory-mapped regions, or extracted strings to classify samples, detect known malware families, or flag suspicious API combinations.

## Usage Examples

### Detecting Binary Format and Extracting Headers

```python
from binary_analysis_engine import BinaryAnalyzer, BinaryFormat

analyzer = BinaryAnalyzer()
result = analyzer.load("/path/to/suspicious.exe")

if result.format == BinaryFormat.PE:
    print(f"Architecture: {result.architecture}")
    print(f"Entry point: 0x{result.entry_point:x}")
    print(f"Sections:")
    for section in result.sections:
        print(f"  {section.name}: VA=0x{section.virtual_address:x} "
              f"Size=0x{section.virtual_size:x} Entropy={section.entropy:.2f}")
    print(f"Imports: {[imp.dll for imp in result.imports]}")
```

### Extracting Strings with Encoding Detection

```python
from binary_analysis_engine import StringExtractor, StringEncoding

extractor = StringExtractor(min_length=4)
strings = extractor.extract("/path/to/binary")

for s in strings:
    if s.encoding == StringEncoding.BASE64:
        decoded = s.decode_base64()
        print(f"[BASE64] {s.text[:40]}... -> {decoded[:100]}")
    elif s.encoding == StringEncoding.XOR_ENCODED:
        print(f"[XOR?] {s.text[:60]} (entropy={s.entropy:.2f})")
    elif s.is_printable:
        print(f"[ASCII] {s.text}")
```

### Entropy-Based Packing Detection

```python
from binary_analysis_engine import EntropyAnalyzer, SectionType

analyzer = EntropyAnalyzer()
sections = analyzer.analyze("/path/to/binary")

packed_indicators = []
for section in sections:
    if section.entropy > 7.5:
        packed_indicators.append(
            f"Section '{section.name}' has entropy {section.entropy:.2f} "
            f"(likely packed/encrypted)"
        )

if packed_indicators:
    print("WARNING: Possible packing detected:")
    for indicator in packed_indicators:
        print(f"  - {indicator}")
```

### Control Flow Graph Extraction

```python
from binary_analysis_engine import CFGExtractor, CFGNode

cfg = CFGExtractor(backend="capstone")
graph = cfg.build("/path/to/binary", function_address=0x401000)

print(f"Function has {len(graph.nodes)} basic blocks")
print(f"Edges: {len(graph.edges)}")

for node in graph.nodes:
    print(f"\nBlock at 0x{node.address:x} ({len(node.instructions)} instructions):")
    for insn in node.instructions:
        print(f"  0x{insn.address:x}: {insn.mnemonic} {insn.op_str}")
```

### Import Analysis for Capability Mapping

```python
from binary_analysis_engine import ImportAnalyzer, CapabilityFlag

analyzer = ImportAnalyzer()
imports = analyzer.analyze("/path/to/binary")
capabilities = analyzer.infer_capabilities(imports)

flag_names = {
    CapabilityFlag.NETWORK: "Network Communication",
    CapabilityFlag.CRYPTO: "Cryptographic Operations",
    CapabilityFlag.FILE_IO: "File System Access",
    CapabilityFlag.REGISTRY: "Registry Manipulation",
    CapabilityFlag.PROCESS_CREATE: "Process Injection",
    CapabilityFlag.ANTI_DEBUG: "Anti-Debugging",
}

print("Detected capabilities:")
for cap in capabilities:
    print(f"  [+] {flag_names.get(cap, cap.name)}")
    for imp in capabilities[cap]:
        print(f"      -> {imp.name} ({imp.dll})")
```

### Binary Diffing Between Versions

```python
from binary_analysis_engine import BinaryDiffer

differ = BinaryDiffer()
diff = differ.diff("/path/to/old_version.exe", "/path/to/new_version.exe")

print(f"Modified functions: {len(diff.modified)}")
print(f"Added functions: {len(diff.added)}")
print(f"Removed functions: {len(diff.removed)}")

for func in diff.modified:
    print(f"\n  {func.name} ({func.change_type}):")
    for change in func.changes:
        print(f"    {change.description}")
```

### YARA Rule Matching on Binary Sections

```python
from binary_analysis_engine import YaraScanner

scanner = YaraScanner(rules_dir="/path/to/rules")
results = scanner.scan("/path/to/suspicious.exe")

for match in results:
    print(f"Rule: {match.rule_name} (namespace: {match.namespace})")
    print(f"  Tags: {match.tags}")
    print(f"  Matches in:")
    for offset, data in match.matched_strings:
        print(f"    0x{offset:x}: {data[:80]}")
```

### Automated Binary Triage Report

```python
from binary_analysis_engine import TriageEngine, TriageReport

engine = TriageEngine()
report = engine.triage("/path/to/sample.bin")

print(TriageReport.format_text(report))
# Output includes:
# - File metadata (format, arch, size, hashes)
# - Section overview with entropy
# - Import summary grouped by category
# - Extracted strings (interesting subset)
# - Packer detection results
# - YARA matches
# - Risk score and indicators
```

## Best Practices

### 1. Always Verify File Format First
Before any analysis, confirm the file is actually what it claims to be. Check magic bytes rather than relying on file extensions. A `.pdf` may actually be a PE executable; a `.jpg` may contain an embedded script.

### 2. Use Multiple Disassembly Backends
Capstone and Radare2 may produce different disassembly results due to differing heuristics for instruction boundary detection. Cross-validate critical findings across backends, especially when dealing with obfuscated or packed code.

### 3. Be Wary of Anti-Analysis Techniques
Sophisticated binaries employ anti-debugging (IsDebuggerPresent, timing checks), anti-VM (CPUID checks, registry lookups), and anti-disassembly (obfuscated jumps, garbage bytes). Always run analysis in instrumented environments (QEMU, sandboxed VMs) and account for these techniques when interpreting results.

### 4. Document Your Analysis Workflow
Binary analysis is iterative. Maintain notes on what you've examined, what hypotheses you've tested, and what you've ruled out. Use structured output formats (JSON, Markdown reports) so findings can be referenced later or shared with teammates.

### 5. Isolate Analysis Environments
Never analyze untrusted binaries on production systems. Use dedicated VMs, Docker containers with network isolation, or dedicated analysis platforms (Cuckoo Sandbox, CAPE) that provide safe execution environments with monitoring.

### 6. Preserve Evidence
Work on copies of binaries, never originals. Calculate and record cryptographic hashes (SHA-256, MD5) of all samples before analysis. Maintain a chain of custody if the analysis may be used in legal or incident response contexts.

### 7. Combine Static and Dynamic Analysis
Static analysis reveals structure and intent; dynamic analysis reveals actual behavior. Neither alone provides a complete picture. Use static findings to guide dynamic analysis (set breakpoints at interesting API calls), and use dynamic observations to resolve static ambiguities (indirect calls, computed addresses).

### 8. Understand the Target Platform
Binary analysis requires understanding the target platform's ABI, calling conventions, system call interface, and loader behavior. A function's first argument is in `rdi` on Linux x86-64 but in `rcx` on Windows x86-64. Syscalls are numbered differently across platforms. These details are essential for accurate analysis.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Binary Analysis Pipeline                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────────┐   │
│  │  Input    │───▶│  Format      │───▶│  Static Analysis    │   │
│  │  Binary   │    │  Detection   │    │  Engine             │   │
│  └──────────┘    └──────────────┘    └──────────┬──────────┘   │
│                                                  │               │
│                              ┌───────────────────┼────────┐     │
│                              ▼                   ▼        ▼     │
│                    ┌──────────────┐  ┌────────┐ ┌──────────┐   │
│                    │  Disassembly │  │ String │ │ Entropy  │   │
│                    │  Engine      │  │ Extract│ │ Analysis │   │
│                    └──────┬───────┘  └────┬───┘ └────┬─────┘   │
│                           │               │          │          │
│                           ▼               ▼          ▼          │
│                    ┌──────────────────────────────────────────┐ │
│                    │           Unified Result Schema           │ │
│                    │  (JSON/dict-based, typed output)          │ │
│                    └──────────────────┬───────────────────────┘ │
│                                       │                          │
│              ┌────────────────────────┼────────────────────┐    │
│              ▼                        ▼                    ▼    │
│  ┌───────────────────┐  ┌──────────────────┐  ┌────────────┐  │
│  │  YARA Scanner     │  │  CFG Builder     │  │  Report     │  │
│  │  (Signature Match)│  │  (Flow Graph)    │  │  Generator  │  │
│  └───────────────────┘  └──────────────────┘  └────────────┘  │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  Backend Adapters: Capstone │ Radare2 │ Ghidra │ LIEF │ pefile │
└─────────────────────────────────────────────────────────────────┘
```

The pipeline follows a layered architecture where format detection feeds into specialized analysis engines. Each engine produces typed results that flow into the Unified Result Schema, enabling composability with downstream tools. Backend adapters provide pluggable disassembly and parsing capabilities.

## Performance Considerations

### 1. Caching Parsed Results
Binary parsing is expensive for large files (500MB+). Cache parsed headers, section tables, and import/export data to disk using pickle or JSON serialization. Subsequent analyses of the same binary skip redundant parsing.

### 2. Parallel Section Processing
Large binaries may contain hundreds of sections. Process entropy calculation, string extraction, and disassembly in parallel using `concurrent.futures.ProcessPoolExecutor` to utilize multi-core CPUs effectively.

### 3. Lazy Disassembly
Disassemble only regions of interest rather than the entire binary. Use entry points, import thunks, and cross-references to identify code sections. Data sections (`.data`, `.rdata`) rarely benefit from disassembly.

### 4. Streaming String Extraction
For binaries larger than 100MB, use memory-mapped file I/O and streaming string extraction instead of loading the entire file into memory. Process strings in chunks to maintain constant memory usage.

### 5. Entropy Window Size Tuning
Shannon entropy calculation performance depends on window size. Use 256-byte windows for quick scanning, 4KB windows for section-level analysis, and 64KB windows for fine-grained packed region detection. Balance granularity against computation time.

### 6. YARA Rule Compilation
Compile YARA rules once and reuse the compiled object across multiple scans. Rule compilation is 10-100x slower than matching. Maintain a rule cache with version tracking for long-running analysis pipelines.

### 7. CFG Construction Limits
Control flow graph construction for functions with complex control flow (obfuscated binaries, compiler-generated switch tables) can be extremely time-consuming. Set maximum basic block limits and function depth thresholds to prevent analysis hangs.

## Security Considerations

### 1. Never Execute Untrusted Binaries
All static analysis should occur without executing the binary. If dynamic analysis is required, use isolated sandbox environments (Cuckoo, CAPE, QEMU VMs) with network isolation and snapshot capabilities.

### 2. Protect Analysis Infrastructure
Analysis VMs should be on isolated networks with no access to production systems. Use dedicated VLANs, disable shared folders, and configure firewall rules to prevent lateral movement if a sample escapes analysis.

### 3. Sanitize Extracted Strings
Extracted strings may contain exploit payloads, ANSI escape sequences, or terminal injection sequences. Display strings using safe formatters that strip control characters before rendering in terminals or reports.

### 4. Handle Sensitive Binaries Carefully
Binaries from incident response or legal cases require chain of custody documentation. Use write-protected storage, calculate hashes before/after analysis, and maintain audit logs of who accessed samples.

### 5. Validate Tool Outputs
Cross-validate critical findings across multiple tools. Disassembly errors, incorrect type interpretations, and false YARA matches are common. Never trust a single tool's output as ground truth.

### 6. Protect Extracted Secrets
Binaries may contain hardcoded credentials, API keys, or private keys. Handle these with the same care as live credentials — don't commit them to version control, don't display them in shared terminals, and securely delete temporary analysis artifacts.

## Related Modules

| Module | Relationship |
|--------|-------------|
| `decompilation` | Binary analysis feeds decompilation — understanding structure first enables better decompilation output |
| `malware-analysis` | Binary analysis techniques are foundational to malware reverse engineering |
| `firmware-analysis` | Firmware images contain binaries that require the same analysis techniques |
| `protocol-analysis` | Binary analysis reveals protocol implementations through network API usage |
| `web2-recon` | Binary analysis of client-side applications complements web application recon |

## References

- **Linux ELF Specification**: System V Application Binary Interface (ABI) — https://refspecs.linuxbase.org/elf/
- **Microsoft PE Format**: PE Format documentation — https://learn.microsoft.com/en-us/windows/win32/debug/pe-format
- **Capstone Disassembly Framework**: https://www.capstone-engine.org/
- **Radare2**: Advanced reverse engineering framework — https://rada.re/n/
- **LIEF Library**: Format-agnostic binary manipulation — https://lief.re/
- **Ghidra**: NSA's software reverse engineering framework — https://ghidra-sre.org/
- **Practical Binary Analysis**: Dennis Andriesse, No Starch Press
- **malware-analysis**: "Practical Malware Analysis" by Michael Sikorski and Andrew Honig
- **PE File Format Reference**: Microsoft official documentation
- **Binary Analysis with the Binary Analysis Toolkit**: https://bat.imirhill.org/
