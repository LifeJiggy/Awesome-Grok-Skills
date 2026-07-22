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

## Disassembly Deep Dive

### Capstone Integration and Configuration

Capstone is the foundational disassembly engine used across this module. It provides multi-architecture support with a clean Python binding.

```python
from capstone import Cs, CS_ARCH_X86, CS_ARCH_ARM, CS_MODE_64, CS_MODE_32, CS_OPT_DETAIL
import struct

class DisassemblyEngine:
    """Multi-architecture disassembly using Capstone with detailed output."""

    ARCH_MAP = {
        'x86_32': (CS_ARCH_X86, CS_MODE_32),
        'x86_64': (CS_ARCH_X86, CS_MODE_64),
        'arm': (CS_ARCH_ARM, CS_MODE_ARM),
        'arm_thumb': (CS_ARCH_ARM, CS_MODE_THUMB),
        'arm64': (CS_ARCH_ARM64, 0),
        'mips': (CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN),
        'mips_be': (CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_BIG_ENDIAN),
    }

    def __init__(self, arch='x86_64'):
        arch_info = self.ARCH_MAP.get(arch, (CS_ARCH_X86, CS_MODE_64))
        self.cs = Cs(arch_info[0], arch_info[1])
        self.cs.detail = True

    def disassemble(self, code_bytes, base_address=0x0):
        """Disassemble bytes into detailed instruction objects."""
        instructions = []
        for insn in self.cs.disasm(code_bytes, base_address):
            detail = insn.detail
            # Extract operands with their types and register/memory details
            operands = []
            for op in detail.regs_access()[0] if hasattr(detail, 'regs_access') else []:
                operands.append({'type': 'reg', 'value': op})

            instructions.append({
                'address': insn.address,
                'size': insn.size,
                'mnemonic': insn.mnemonic,
                'op_str': insn.op_str,
                'bytes': insn.bytes.hex(),
                'groups': [self.cs.group_name(g) for g in detail.groups],
                'regs_read': [self.cs.reg_name(r) for r in detail.regs_read],
                'regs_written': [self.cs.reg_name(r) for r in detail.regs_write],
                'operands_count': len(detail.operands) if detail.operands else 0,
            })
        return instructions

    def find_function_prologue(self, code_bytes, base_address=0x0):
        """Detect common function prologues across architectures."""
        prologues = {
            'push rbp; mov rbp, rsp': b'\x55\x48\x89\xe5',
            'push ebp; mov ebp, esp': b'\x55\x89\xe5',
            'sub rsp, N': b'\x48\x83\xec',
            'xor ebp, ebp': b'\x31\xed',
        }
        results = []
        for name, pattern in prologues.items():
            offset = code_bytes.find(pattern)
            if offset != -1:
                results.append({
                    'prologue': name,
                    'offset': base_address + offset,
                    'context': code_bytes[max(0, offset-4):offset+16].hex(),
                })
        return results
```

### Radare2 Scripting for Binary Exploration

Radare2 provides a comprehensive reverse engineering framework with a scripting API for automation.

```python
import r2pipe
import json

class Radare2Analyzer:
    """Automated binary analysis using Radare2."""

    def __init__(self, binary_path):
        self.r2 = r2pipe.open(binary_path, flags=['-2'])
        self.r2.cmd('aaa')  # Full analysis

    def get_functions(self):
        """List all detected functions with metadata."""
        funcs = json.loads(self.r2.cmd('aflj'))
        return [{
            'name': f.get('name', 'unknown'),
            'offset': f['offset'],
            'size': f['size'],
            'nbbs': f.get('nbbs', 0),  # number of basic blocks
            'cc': f.get('cc', 0),       # cyclomatic complexity
            'callrefs': f.get('callrefs', []),
            'datarefs': f.get('datarefs', []),
        } for f in funcs]

    def decompile_function(self, address):
        """Decompile a specific function to pseudocode."""
        self.r2.cmd(f's {address:#x}')
        pseudocode = self.r2.cmd('pdg')  # Requires r2ghidra
        return pseudocode

    def get_xrefs(self, address):
        """Get all cross-references to an address."""
        xrefs = json.loads(self.r2.cmd(f'axtj @ {address:#x}}))
        return xrefs

    def analyze_imports(self):
        """Extract and categorize import table entries."""
        imports = json.loads(self.r2.cmd('iij'))
        categories = {
            'network': ['socket', 'connect', 'bind', 'listen', 'accept',
                       'send', 'recv', 'sendto', 'recvfrom', 'gethostbyname',
                       'inet_addr', 'WSAStartup'],
            'file_io': ['open', 'read', 'write', 'close', 'fopen', 'fread',
                       'fwrite', 'fclose', 'CreateFile', 'ReadFile', 'WriteFile'],
            'process': ['fork', 'exec', 'system', 'popen', 'CreateProcess',
                       'ShellExecute', 'WinExec'],
            'memory': ['malloc', 'calloc', 'realloc', 'free', 'VirtualAlloc',
                      'VirtualProtect', 'HeapAlloc'],
            'crypto': ['AES', 'DES', 'RSA', 'MD5', 'SHA', 'CryptEncrypt',
                      'CryptDecrypt', 'BCryptEncrypt'],
            'registry': ['RegOpenKey', 'RegQueryValue', 'RegSetValue',
                        'RegCreateKey', 'RegDeleteKey'],
        }

        categorized = {cat: [] for cat in categories}
        uncategorized = []

        for imp in imports:
            name = imp.get('name', '')
            found = False
            for cat, keywords in categories.items():
                if any(kw.lower() in name.lower() for kw in keywords):
                    categorized[cat].append(imp)
                    found = True
                    break
            if not found:
                uncategorized.append(imp)

        return {
            'categorized': categorized,
            'uncategorized': uncategorized,
            'total': len(imports),
        }

    def extract_strings_with_context(self, min_length=6):
        """Extract strings with their code references."""
        strings = json.loads(self.r2.cmd('izj'))
        results = []
        for s in strings:
            if len(s.get('string', '')) >= min_length:
                # Find code references to this string
                refs = json.loads(
                    self.r2.cmd(f'axtj @ {s["vaddr"]:#x}'))
                results.append({
                    'string': s['string'],
                    'address': s['vaddr'],
                    'size': s['size'],
                    'type': s.get('type', 'ascii'),
                    'references': refs,
                })
        return results

    def detect_anti_analysis(self):
        """Detect common anti-analysis and anti-debugging techniques."""
        suspicious_functions = []
        funcs = self.get_functions()

        anti_debug_patterns = [
            'IsDebuggerPresent', 'CheckRemoteDebuggerPresent',
            'NtQueryInformationProcess', 'OutputDebugString',
            'GetTickCount', 'QueryPerformanceCounter',
            'rdtsc', 'cpuid', 'int 2d', 'int 3',
        ]

        for func in funcs:
            disasm = self.r2.cmd(f'pd 50 @ {func["offset"]:#x}')
            for pattern in anti_debug_patterns:
                if pattern in disasm:
                    suspicious_functions.append({
                        'function': func['name'],
                        'address': func['offset'],
                        'technique': pattern,
                        'category': 'anti-debug',
                    })

        return suspicious_functions

    def close(self):
        self.r2.quit()
```

### Binary Format Parsing with LIEF

LIEF provides format-agnostic binary parsing with structured access to ELF, PE, and Mach-O formats.

```python
import lief

class FormatParser:
    """Parse ELF, PE, and Mach-O binaries using LIEF."""

    def __init__(self, binary_path):
        self.binary = lief.parse(binary_path)
        self.format_type = self._detect_format()

    def _detect_format(self):
        if isinstance(self.binary, lief.ELF.Binary):
            return 'ELF'
        elif isinstance(self.binary, lief.PE.Binary):
            return 'PE'
        elif isinstance(self.binary, lief.MachO.Binary):
            return 'MachO'
        return 'UNKNOWN'

    def get_sections(self):
        """Extract section information with permissions and entropy."""
        sections = []
        for section in self.binary.sections:
            content = bytes(section.content)
            entropy = self._calculate_entropy(content)
            sections.append({
                'name': section.name,
                'virtual_address': section.virtual_address,
                'virtual_size': section.virtual_size,
                'offset': section.offset,
                'size': section.size,
                'entropy': entropy,
                'flags': str(section.flags),
                'type': str(section.type),
                'is_executable': bool(section.flags & 0x4),
                'is_writable': bool(section.flags & 0x2),
                'is_readable': bool(section.flags & 0x4),
            })
        return sections

    def get_dynamic_symbols(self):
        """Extract dynamic symbol table entries."""
        symbols = []
        for sym in self.binary.dynamic_symbols:
            symbols.append({
                'name': sym.name,
                'value': sym.value,
                'size': sym.size,
                'binding': str(sym.binding),
                'type': str(sym.type),
                'shndx': sym.shndx,
            })
        return symbols

    def get_relocations(self):
        """Extract relocation entries."""
        relocs = []
        for reloc in self.binary.relocations:
            relocs.append({
                'type': str(reloc.type),
                'address': reloc.address,
                'symbol': reloc.symbol.name if reloc.symbol else None,
                'addend': reloc.addend if hasattr(reloc, 'addend') else None,
            })
        return relocs

    def get_imported_functions(self):
        """Extract imported functions with library information."""
        imports = []
        for entry in self.binary.imported_functions:
            imports.append({
                'name': entry.name if hasattr(entry, 'name') else str(entry),
                'library': entry.library.name if hasattr(entry, 'library') else 'unknown',
                'ordinal': entry.ordinal if hasattr(entry, 'ordinal') else None,
            })
        return imports

    def get_exported_functions(self):
        """Extract exported functions."""
        exports = []
        for entry in self.binary.exported_functions:
            exports.append({
                'name': entry.name if hasattr(entry, 'name') else str(entry),
                'address': entry.address if hasattr(entry, 'address') else None,
                'ordinal': entry.ordinal if hasattr(entry, 'ordinal') else None,
            })
        return exports

    @staticmethod
    def _calculate_entropy(data):
        import math
        if not data:
            return 0.0
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
        entropy = 0.0
        for count in byte_counts:
            if count > 0:
                probability = count / len(data)
                entropy -= probability * math.log2(probability)
        return entropy
```

### Symbol Resolution and Demangling

Recovering meaningful symbols from stripped or partially stripped binaries requires multiple techniques.

```python
import subprocess
import re
import json

class SymbolResolver:
    """Resolve and demangle binary symbols."""

    def __init__(self, binary_path):
        self.binary_path = binary_path
        self.symbols = {}
        self.demangled = {}

    def extract_symbols(self):
        """Extract symbols from ELF/PE using readelf/objdump."""
        try:
            result = subprocess.run(
                ['readelf', '-sW', self.binary_path],
                capture_output=True, text=True, timeout=30
            )
            for line in result.stdout.splitlines():
                match = re.match(
                    r'\s*(\d+):\s+([0-9a-f]+)\s+(\d+)\s+(\w+)\s+'
                    r'(\w+)\s+(\w+)\s+(\w+)\s+(.*)', line
                )
                if match:
                    self.symbols[match.group(2)] = {
                        'index': int(match.group(1)),
                        'value': int(match.group(2), 16),
                        'size': int(match.group(3)),
                        'type': match.group(4),
                        'bind': match.group(5),
                        'vis': match.group(6),
                        'ndx': match.group(7),
                        'name': match.group(8).strip(),
                    }
        except FileNotFoundError:
            # Fallback: use LIEF or pefile
            pass
        return self.symbols

    def demangle_cxx(self, mangled_name):
        """Demangle C++ mangled symbol names."""
        try:
            result = subprocess.run(
                ['c++filt', mangled_name],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except FileNotFoundError:
            return mangled_name

    def demangle_all(self):
        """Demangle all C++ symbols in the symbol table."""
        for addr, sym in self.symbols.items():
            if sym['name'].startswith('_Z'):
                self.demangled[addr] = self.demangle_cxx(sym['name'])
            else:
                self.demangled[addr] = sym['name']
        return self.demangled

    def resolve_address(self, address):
        """Resolve an address to the closest known symbol."""
        best_match = None
        best_offset = float('inf')
        for addr_str, sym in self.symbols.items():
            sym_addr = int(addr_str, 16)
            offset = address - sym_addr
            if 0 <= offset < best_offset:
                best_offset = offset
                best_match = sym
        if best_match:
            return {
                'symbol': best_match['name'],
                'offset': best_offset,
                'function_start': int(
                    [a for a, s in self.symbols.items()
                     if s is == best_match][0], 16),
                'demangled': self.demangle_cxx(best_match['name']),
            }
        return None

    def find_functions_by_pattern(self, pattern):
        """Find symbols matching a regex pattern."""
        matches = []
        regex = re.compile(pattern, re.IGNORECASE)
        for addr, sym in self.symbols.items():
            if regex.search(sym['name']):
                matches.append({
                    'address': int(addr, 16),
                    'name': sym['name'],
                    'size': sym['size'],
                    'demangled': self.demangle_cxx(sym['name']),
                })
        return sorted(matches, key=lambda x: x['address'])
```

### Control Flow Analysis Techniques

Advanced control flow graph construction and analysis for complex binaries.

```python
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional

@dataclass
class BasicBlock:
    """Represents a single basic block in a control flow graph."""
    address: int
    size: int
    instructions: List[dict] = field(default_factory=list)
    successors: List[int] = field(default_factory=list)
    predecessors: List[int] = field(default_factory=list)
    is_entry: bool = False
    is_exit: bool = False

@dataclass
class ControlFlowGraph:
    """Complete control flow graph for a function."""
    entry_address: int
    blocks: Dict[int, BasicBlock] = field(default_factory=dict)
    edges: List[tuple] = field(default_factory=list)

class CFGBuilder:
    """Build and analyze control flow graphs from disassembly."""

    def __init__(self, disasm_engine):
        self.disasm = disasm_engine

    def build_cfg(self, code_bytes, base_address=0x0):
        """Build a CFG from raw code bytes."""
        instructions = self.disasm.disassemble(code_bytes, base_address)
        blocks = self._partition_into_blocks(instructions)

        # Build edges
        edges = []
        for addr, block in blocks.items():
            if block.instructions:
                last_insn = block.instructions[-1]
                mnemonic = last_insn['mnemonic']

                if mnemonic in ('ret', 'retn'):
                    block.is_exit = True
                elif mnemonic.startswith('j') or mnemonic.startswith('b'):
                    # Conditional or unconditional branch
                    target = self._parse_branch_target(last_insn)
                    if target and target in blocks:
                        block.successors.append(target)
                        blocks[target].predecessors.append(addr)
                        edges.append((addr, target, 'branch'))

                    # For conditional branches, fall-through is also a successor
                    if not mnemonic.startswith('jmp'):
                        fall_through = addr + last_insn['size']
                        if fall_through in blocks:
                            block.successors.append(fall_through)
                            blocks[fall_through].predecessors.append(addr)
                            edges.append((addr, fall_through, 'fallthrough'))
                elif mnemonic.startswith('call'):
                    # Call instructions — fall-through successor
                    fall_through = addr + last_insn['size']
                    if fall_through in blocks:
                        block.successors.append(fall_through)
                        blocks[fall_through].predecessors.append(addr)
                        edges.append((addr, fall_through, 'call'))
                else:
                    # Sequential flow
                    fall_through = addr + last_insn['size']
                    if fall_through in blocks:
                        block.successors.append(fall_through)
                        blocks[fall_through].predecessors.append(addr)
                        edges.append((addr, fall_through, 'sequential'))

        # Mark entry block
        if blocks:
            first_addr = min(blocks.keys())
            blocks[first_addr].is_entry = True

        return ControlFlowGraph(
            entry_address=base_address,
            blocks=blocks,
            edges=edges,
        )

    def _partition_into_blocks(self, instructions):
        """Partition instructions into basic blocks at control flow boundaries."""
        blocks = {}
        current_block = []

        for insn in instructions:
            mnemonic = insn['mnemonic']

            # Start new block after branches and calls
            if current_block and (
                mnemonic.startswith('j') or
                mnemonic.startswith('b') or
                mnemonic in ('ret', 'retn', 'bl') or
                current_block[-1]['mnemonic'].startswith('j') or
                current_block[-1]['mnemonic'] in ('ret', 'retn')
            ):
                block_addr = current_block[0]['address']
                blocks[block_addr] = BasicBlock(
                    address=block_addr,
                    size=sum(i['size'] for i in current_block),
                    instructions=current_block,
                )
                current_block = []

            current_block.append(insn)

        # Final block
        if current_block:
            block_addr = current_block[0]['address']
            blocks[block_addr] = BasicBlock(
                address=block_addr,
                size=sum(i['size'] for i in current_block),
                instructions=current_block,
            )

        return blocks

    def _parse_branch_target(self, instruction):
        """Parse the target address from a branch instruction."""
        op_str = instruction['op_str'].strip()
        # Direct numeric address
        if op_str.startswith('0x'):
            return int(op_str, 16)
        if op_str.startswith('#'):
            return int(op_str[1:], 16)
        # Try parsing as integer
        try:
            return int(op_str)
        except ValueError:
            return None

    def calculate_complexity(self, cfg):
        """Calculate cyclomatic complexity of a function's CFG."""
        V = len(cfg.blocks)     # vertices (basic blocks)
        E = len(cfg.edges)      # edges
        P = 1                    # connected components (one function)
        return E - V + 2 * P

    def find_dominators(self, cfg):
        """Compute dominator tree for a CFG."""
        if not cfg.blocks:
            return {}

        entry = min(cfg.blocks.keys())
        dominators = {addr: set(cfg.blocks.keys()) for addr in cfg.blocks}
        dominators[entry] = {entry}

        changed = True
        while changed:
            changed = False
            for addr, block in cfg.blocks.items():
                if addr == entry:
                    continue
                # Intersect dominators of all predecessors
                if block.predecessors:
                    new_dom = set.intersection(
                        *[dominators[p] for p in block.predecessors
                          if p in dominators])
                    new_dom = new_dom | {addr}
                    if new_dom != dominators[addr]:
                        dominators[addr] = new_dom
                        changed = True

        return dominators

    def find_loops(self, cfg):
        """Detect loops (back edges) in the CFG."""
        loops = []
        for src, dst, edge_type in cfg.edges:
            # A back edge creates a loop
            if self._is_dominator(dst, src, cfg):
                loops.append({
                    'header': dst,
                    'back_edge_src': src,
                    'type': 'natural loop' if edge_type == 'branch' else 'irreducible',
                })
        return loops

    def _is_dominator(self, dom_candidate, node, cfg):
        """Check if dom_candidate dominates node."""
        if dom_candidate == node:
            return True
        visited = set()
        stack = [node]
        while stack:
            current = stack.pop()
            if current == dom_candidate:
                return True
            if current in visited:
                continue
            visited.add(current)
            if current in cfg.blocks:
                stack.extend(cfg.blocks[current].predecessors)
        return False
```

### Data Structure Recovery from Binary

Inferring data structures by analyzing how memory is accessed in disassembled code.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class FieldInfo:
    """Represents an inferred field within a data structure."""
    name: str
    offset: int
    size: int
    inferred_type: str
    access_patterns: List[str] = field(default_factory=list)

@dataclass
class RecoveredStruct:
    """A data structure inferred from binary code analysis."""
    name: str
    size: int
    fields: List[FieldInfo] = field(default_factory=list)
    confidence: float = 0.0
    access_count: int = 0

class DataStructureRecovery:
    """Infer data structures from memory access patterns."""

    def __init__(self):
        self.structs: Dict[str, RecoveredStruct] = {}
        self.access_patterns: Dict[str, List[dict]] = {}

    def analyze_memory_accesses(self, instructions, base_address=0x0):
        """Analyze memory access patterns to infer struct layouts."""
        for insn in instructions:
            # Look for base + offset patterns (struct field access)
            op_str = insn.get('op_str', '')
            # x86: [reg + 0xNN] or [reg + offset]
            import re
            match = re.search(r'\[(\w+)\s*\+\s*(0x[0-9a-f]+|\d+)\]', op_str)
            if match:
                base_reg = match.group(1)
                offset = int(match.group(2), 0)
                size = self._infer_access_size(insn)

                if base_reg not in self.access_patterns:
                    self.access_patterns[base_reg] = []
                self.access_patterns[base_reg].append({
                    'offset': offset,
                    'size': size,
                    'mnemonic': insn['mnemonic'],
                    'address': insn['address'],
                    'access_type': self._classify_access(insn['mnemonic']),
                })

    def _infer_access_size(self, instruction):
        """Infer the size of a memory access from the instruction."""
        mnemonic = instruction['mnemonic']
        size_map = {
            'movzx': 1, 'movsx': 1, 'movb': 1,
            'movw': 2, 'movzx': 2,
            'movl': 4, 'mov': 4, 'cmpl': 4, 'addl': 4,
            'movq': 8, 'mov': 8,
        }
        return size_map.get(mnemonic, 4)

    def _classify_access(self, mnemonic):
        """Classify whether an access is a read or write."""
        write_mnemonics = {'mov', 'movb', 'movw', 'movl', 'movq',
                          'stosb', 'stosw', 'stosd', 'stosq',
                          'push', 'movups', 'movaps'}
        if mnemonic in write_mnemonics:
            return 'write'
        return 'read'

    def recover_structures(self):
        """Recover struct definitions from accumulated access patterns."""
        for reg, accesses in self.access_patterns.items():
            if len(accesses) < 3:
                continue

            # Group accesses by offset
            offset_map = {}
            for acc in accesses:
                offset = acc['offset']
                if offset not in offset_map:
                    offset_map[offset] = {
                        'reads': 0, 'writes': 0,
                        'sizes': set(), 'examples': [],
                    }
                if acc['access_type'] == 'read':
                    offset_map[offset]['reads'] += 1
                else:
                    offset_map[offset]['writes'] += 1
                offset_map[offset]['sizes'].add(acc['size'])
                offset_map[offset]['examples'].append(acc)

            # Determine most likely size for each field
            fields = []
            for offset in sorted(offset_map.keys()):
                info = offset_map[offset]
                most_likely_size = max(info['sizes'],
                                       key=lambda s: sum(
                                           1 for x in info['sizes'] if x == s))

                field_type = {
                    1: 'uint8_t', 2: 'uint16_t',
                    4: 'uint32_t', 8: 'uint64_t',
                }.get(most_likely_size, f'unknown_{most_likely_size}d')

                fields.append(FieldInfo(
                    name=f'field_{offset:x}',
                    offset=offset,
                    size=most_likely_size,
                    inferred_type=field_type,
                    access_patterns=[e['mnemonic'] for e in info['examples'][:5]],
                ))

            max_offset = max(f.offset + f.size for f in fields) if fields else 0
            self.structs[reg] = RecoveredStruct(
                name=f'struct_{reg}',
                size=max_offset,
                fields=fields,
                confidence=min(1.0, len(accesses) / 20.0),
                access_count=len(accesses),
            )

        return self.structs

    def generate_c_struct(self, struct_name):
        """Generate a C struct definition from recovered structure."""
        if struct_name not in self.structs:
            return None

        struct = self.structs[struct_name]
        lines = [f'typedef struct {struct.name} {{']

        current_offset = 0
        for field in sorted(struct.fields, key=lambda f: f.offset):
            # Add padding if needed
            if field.offset > current_offset:
                padding_size = field.offset - current_offset
                lines.append(f'    uint8_t _pad{current_offset:x}[{padding_size}];')
            lines.append(f'    {field.inferred_type} {field.name};'
                        f' // offset 0x{field.offset:x}, size {field.size}')
            current_offset = field.offset + field.size

        lines.append(f'}} {struct.name};')
        return '\n'.join(lines)
```

### Binary Patching and Modification

Techniques for modifying binary code for vulnerability research and authorized testing.

```python
import struct
import hashlib
from pathlib import Path

class BinaryPatcher:
    """Patch binary code and data for authorized security testing."""

    def __init__(self, binary_path):
        self.binary_path = binary_path
        self.original_data = Path(binary_path).read_bytes()
        self.patches = []

    def calculate_hashes(self):
        """Calculate cryptographic hashes of the original binary."""
        return {
            'md5': hashlib.md5(self.original_data).hexdigest(),
            'sha1': hashlib.sha1(self.original_data).hexdigest(),
            'sha256': hashlib.sha256(self.original_data).hexdigest(),
        }

    def patch_byte(self, offset, new_byte):
        """Patch a single byte at the given offset."""
        if offset >= len(self.original_data):
            raise ValueError(f"Offset 0x{offset:x} exceeds file size")
        old_byte = self.original_data[offset]
        self.patches.append({
            'offset': offset,
            'old': old_byte,
            'new': new_byte,
        })
        # Apply to a mutable copy
        if not hasattr(self, '_patched_data'):
            self._patched_data = bytearray(self.original_data)
        self._patched_data[offset] = new_byte

    def patch_bytes(self, offset, new_bytes):
        """Patch multiple bytes starting at offset."""
        for i, byte in enumerate(new_bytes):
            self.patch_byte(offset + i, byte)

    def nop_sled(self, offset, length):
        """Replace instructions with NOP sled."""
        # x86 NOP = 0x90
        self.patch_bytes(offset, b'\x90' * length)

    def replace_call(self, call_address, new_target):
        """Replace a call instruction target."""
        # x86 relative call: E8 XX XX XX XX
        # E8 is opcode for near call
        relative_offset = new_target - (call_address + 5)
        self.patch_byte(call_address, 0xE8)
        self.patch_bytes(call_address + 1,
                        struct.pack('<i', relative_offset))

    def apply_patches(self, output_path):
        """Apply all patches and write to output file."""
        if not hasattr(self, '_patched_data'):
            return False

        output = Path(output_path)
        output.write_bytes(bytes(self._patched_data))
        return True

    def generate_patch_report(self):
        """Generate a detailed report of all patches applied."""
        report = {
            'original_hashes': self.calculate_hashes(),
            'total_patches': len(self.patches),
            'patches': [],
        }

        modified_data = self._patched_data if hasattr(self, '_patched_data') \
                       else self.original_data
        report['patched_hashes'] = {
            'md5': hashlib.md5(bytes(modified_data)).hexdigest(),
            'sha1': hashlib.sha1(bytes(modified_data)).hexdigest(),
            'sha256': hashlib.sha256(bytes(modified_data)).hexdigest(),
        }

        for patch in self.patches:
            report['patches'].append({
                'offset': f"0x{patch['offset']:08x}",
                'original': f"0x{patch['old']:02x}",
                'patched': f"0x{patch['new']:02x}",
            })

        return report
```

### ELF Binary Analysis Specifics

Deep analysis of ELF format internals for Linux binary analysis.

```python
import struct
from pathlib import Path

class ELFAnalyzer:
    """Low-level ELF format analysis without external dependencies."""

    ELF_MAGIC = b'\x7fELF'

    # ELF class constants
    ELFCLASS32 = 1
    ELFCLASS64 = 2

    # EI_DATA values
    ELFDATA2LSB = 1  # Little-endian
    ELFDATA2MSB = 2  # Big-endian

    # e_type values
    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4

    # e_machine values
    EM_386 = 3
    EM_X86_64 = 62
    EM_ARM = 40
    EM_AARCH64 = 183
    EM_MIPS = 8
    EM_PPC = 20
    EM_RISCV = 243

    def __init__(self, binary_path):
        self.data = Path(binary_path).read_bytes()
        self.header = self._parse_ehdr()
        self.sections = self._parse_sections()
        self.segments = self._parse_segments()

    def _parse_ehdr(self):
        """Parse the ELF header."""
        if self.data[:4] != self.ELF_MAGIC:
            raise ValueError("Not a valid ELF file")

        ei_class = self.data[4]
        ei_data = self.data[5]

        if ei_class == self.ELFCLASS64:
            return self._parse_ehdr64(ei_data)
        elif ei_class == self.ELFCLASS32:
            return self._parse_ehdr32(ei_data)
        raise ValueError(f"Unsupported ELF class: {ei_class}")

    def _parse_ehdr64(self, ei_data):
        fmt = '<' if ei_data == self.ELFDATA2LSB else '>'
        header = struct.unpack_from(f'{fmt}16sHHIQQQIHHHHHH', self.data, 0)
        return {
            'class': 'ELF64',
            'endian': 'little' if ei_data == self.ELFDATA2LSB else 'big',
            'ei_osabi': self.data[7],
            'type': header[1],
            'machine': header[2],
            'version': header[3],
            'entry': header[4],
            'phoff': header[5],
            'shoff': header[6],
            'flags': header[7],
            'ehsize': header[8],
            'phentsize': header[9],
            'phnum': header[10],
            'shentsize': header[11],
            'shnum': header[12],
            'shstrndx': header[13],
        }

    def _parse_ehdr32(self, ei_data):
        fmt = '<' if ei_data == self.ELFDATA2LSB else '>'
        header = struct.unpack_from(f'{fmt}16sHHIIIIIIHHHHHH', self.data, 0)
        return {
            'class': 'ELF32',
            'endian': 'little' if ei_data == self.ELFDATA2LSB else 'big',
            'type': header[1],
            'machine': header[2],
            'version': header[3],
            'entry': header[4],
            'phoff': header[5],
            'shoff': header[6],
            'flags': header[7],
            'ehsize': header[8],
            'phentsize': header[9],
            'phnum': header[10],
            'shentsize': header[11],
            'shnum': header[12],
            'shstrndx': header[13],
        }

    def _parse_sections(self):
        """Parse section headers."""
        sections = []
        shoff = self.header['shoff']
        shnum = self.header['shnum']
        shentsize = self.header['shentsize']

        for i in range(shnum):
            offset = shoff + i * shentsize
            if self.header['class'] == 'ELF64':
                fmt = '<' if self.header['endian'] == 'little' else '>'
                sh = struct.unpack_from(f'{fmt}IIQQQQIIQQ', self.data, offset)
                sections.append({
                    'name_idx': sh[0],
                    'type': sh[1],
                    'flags': sh[2],
                    'addr': sh[3],
                    'offset': sh[4],
                    'size': sh[5],
                    'link': sh[6],
                    'info': sh[7],
                    'addralign': sh[8],
                    'entsize': sh[9],
                })
        return sections

    def _parse_segments(self):
        """Parse program headers (segments)."""
        segments = []
        phoff = self.header['phoff']
        phnum = self.header['phnum']
        phentsize = self.header['phentsize']

        for i in range(phnum):
            offset = phoff + i * phentsize
            if self.header['class'] == 'ELF64':
                fmt = '<' if self.header['endian'] == 'little' else '>'
                ph = struct.unpack_from(f'{fmt}IIQQQQQQ', self.data, offset)
                segments.append({
                    'type': ph[0],
                    'flags': ph[1],
                    'offset': ph[2],
                    'vaddr': ph[3],
                    'paddr': ph[4],
                    'filesz': ph[5],
                    'memsz': ph[6],
                    'align': ph[7],
                })
        return segments

    def get_section_name(self, section):
        """Resolve section name from string table."""
        shstrndx = self.header['shstrndx']
        if shstrndx >= len(self.sections):
            return f'unknown_{section["name_idx"]}'
        strtab = self.sections[shstrndx]
        strtab_offset = strtab['offset'] + section['name_idx']
        name_end = self.data.index(b'\x00', strtab_offset)
        return self.data[strtab_offset:name_end].decode('ascii', errors='replace')

    def analyze_protections(self):
        """Analyze binary protections (NX, PIE, stack canary, RELRO)."""
        protections = {
            'NX': False,       # No-Execute (DEP)
            'PIE': False,      # Position-Independent Executable
            'RELRO': 'none',   # RELRO: partial, full, or none
            'StackCanary': False,
            'FORTIFY': False,
        }

        # Check for PT_GNU_STACK (NX)
        for seg in self.segments:
            if seg['type'] == 0x6474e551:  # PT_GNU_STACK
                protections['NX'] = not bool(seg['flags'] & 0x1)

        # Check for PT_INTERP position (PIE detection)
        for seg in self.segments:
            if seg['type'] == 3:  # PT_INTERP
                if seg['vaddr'] > 0x100000:
                    protections['PIE'] = True

        # RELRO detection via segment types
        has_gnu_relro = False
        has_gnu_dynamic = False
        for seg in self.segments:
            if seg['type'] == 0x6474e552:  # PT_GNU_RELRO
                has_gnu_relro = True
            if seg['type'] == 0x6474e550:  # PT_GNU_DYNAMIC
                has_gnu_dynamic = True
        if has_gnu_relro and has_gnu_dynamic:
            protections['RELRO'] = 'full'
        elif has_gnu_relro:
            protections['RELRO'] = 'partial'

        return protections
```

### PE Binary Analysis Specifics

Windows PE format analysis for reverse engineering Windows executables.

```python
import struct
from pathlib import Path

class PEAnalyzer:
    """PE format analysis for Windows binary reverse engineering."""

    # PE signature
    PE_MAGIC = b'MZ'

    # Machine types
    MACHINE_AMD64 = 0x8664
    MACHINE_I386 = 0x014c
    MACHINE_ARM64 = 0xAA64

    # Section flags
    IMAGE_SCN_CNT_CODE = 0x00000020
    IMAGE_SCN_CNT_INITIALIZED_DATA = 0x00000040
    IMAGE_SCN_MEM_EXECUTE = 0x20000000
    IMAGE_SCN_MEM_READ = 0x40000000
    IMAGE_SCN_MEM_WRITE = 0x80000000

    def __init__(self, pe_path):
        self.data = Path(pe_path).read_bytes()
        self.dos_header = self._parse_dos_header()
        self.pe_offset = self.dos_header['e_lfanew']
        self.signature = struct.unpack_from('<I', self.data, self.pe_offset)[0]
        self.coff_header = self._parse_coff_header()
        self.optional_header = self._parse_optional_header()
        self.sections = self._parse_section_table()

    def _parse_dos_header(self):
        """Parse the DOS MZ header."""
        return {
            'e_magic': struct.unpack_from('<H', self.data, 0)[0],
            'e_lfanew': struct.unpack_from('<I', self.data, 0x3C)[0],
        }

    def _parse_coff_header(self):
        """Parse the COFF file header."""
        offset = self.pe_offset + 4
        fields = struct.unpack_from('<HHIIIHH', self.data, offset)
        return {
            'machine': fields[0],
            'num_sections': fields[1],
            'time_date_stamp': fields[2],
            'pointer_to_symbol_table': fields[3],
            'num_symbols': fields[4],
            'size_optional_header': fields[5],
            'characteristics': fields[6],
        }

    def _parse_optional_header(self):
        """Parse the Optional Header (PE32 or PE32+)."""
        offset = self.pe_offset + 24
        magic = struct.unpack_from('<H', self.data, offset)[0]

        if magic == 0x20b:  # PE32+ (64-bit)
            fields = struct.unpack_from('<' + 'B' * 11 + 'I' * 10, self.data, offset + 2)
            return {
                'magic': magic,
                'class': 'PE32+',
                'address_of_entry_point': fields[10],
                'image_base': struct.unpack_from('<Q', self.data, offset + 24)[0],
                'section_alignment': fields[11],
                'file_alignment': fields[12],
                'subsystem': fields[18],
                'dll_characteristics': fields[20],
            }
        elif magic == 0x10b:  # PE32 (32-bit)
            fields = struct.unpack_from('<' + 'B' * 11 + 'I' * 10, self.data, offset + 2)
            return {
                'magic': magic,
                'class': 'PE32',
                'address_of_entry_point': fields[10],
                'image_base': struct.unpack_from('<I', self.data, offset + 28)[0],
                'section_alignment': fields[11],
                'file_alignment': fields[12],
                'subsystem': fields[18],
                'dll_characteristics': fields[20],
            }
        return {}

    def _parse_section_table(self):
        """Parse section headers."""
        sections = []
        offset = (self.pe_offset + 24 +
                  self.coff_header['size_optional_header'])

        for i in range(self.coff_header['num_sections']):
            name = self.data[offset:offset+8].rstrip(b'\x00').decode('ascii', errors='replace')
            fields = struct.unpack_from('<IIIIIIHHI', self.data, offset + 8)

            section = {
                'name': name,
                'virtual_size': fields[0],
                'virtual_address': fields[1],
                'size_of_raw_data': fields[2],
                'pointer_to_raw_data': fields[3],
                'pointer_to_relocations': fields[4],
                'pointer_to_linenumbers': fields[5],
                'num_relocations': fields[6],
                'num_linenumbers': fields[7],
                'characteristics': fields[8],
            }

            # Calculate entropy for the section
            raw_data = self.data[
                section['pointer_to_raw_data']:
                section['pointer_to_raw_data'] + section['size_of_raw_data']
            ]
            section['entropy'] = self._calculate_entropy(raw_data)

            sections.append(section)
            offset += 40  # Each section header is 40 bytes

        return sections

    @staticmethod
    def _calculate_entropy(data):
        import math
        if not data:
            return 0.0
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
        entropy = 0.0
        for count in byte_counts:
            if count > 0:
                p = count / len(data)
                entropy -= p * math.log2(p)
        return entropy

    def analyze_dll_characteristics(self):
        """Analyze DLL characteristics flags for security features."""
        flags = self.optional_header.get('dll_characteristics', 0)
        features = {
            'HighEntropyVA': bool(flags & 0x0020),
            'DynamicBase (ASLR)': bool(flags & 0x0040),
            'ForceIntegrityCheck': bool(flags & 0x0080),
            'NXCompat (DEP)': bool(flags & 0x0100),
            'NoIsolation': bool(flags & 0x0200),
            'NoSEH': bool(flags & 0x0400),
            'NoBind': bool(flags & 0x0800),
            'AppContainer': bool(flags & 0x1000),
            'ControlFlowGuard': bool(flags & 0x4000),
        }
        return features

    def extract_imports(self):
        """Extract import table entries."""
        imports = {}
        # Import Directory RVA is typically at index 1 of data directories
        # This is a simplified extraction; full implementation requires
        # walking the Import Directory Table
        import_dir_rva = self._get_data_directory_rva(1)
        if import_dir_rva:
            imports = self._walk_import_directory(import_dir_rva)
        return imports

    def _get_data_directory_rva(self, index):
        """Get RVA of a data directory entry."""
        offset = self.pe_offset + 24
        magic = struct.unpack_from('<H', self.data, offset)[0]
        if magic == 0x20b:  # PE32+
            dir_offset = offset + 112 + (index * 16)
        else:  # PE32
            dir_offset = offset + 96 + (index * 16)
        rva = struct.unpack_from('<I', self.data, dir_offset)[0]
        size = struct.unpack_from('<I', self.data, dir_offset + 4)[0]
        return rva if size > 0 else None

    def rva_to_offset(self, rva):
        """Convert RVA to file offset using section table."""
        for section in self.sections:
            start = section['virtual_address']
            end = start + section['virtual_size']
            if start <= rva < end:
                return section['pointer_to_raw_data'] + (rva - start)
        return None
```

## Advanced Analysis Patterns

### Pattern-Based Vulnerability Detection

Identifying common vulnerability patterns in disassembled code.

```python
import re

class VulnerabilityPatternMatcher:
    """Detect vulnerability patterns in disassembled code."""

    BUFFER_OVERFLOW_PATTERNS = [
        # strcpy(buf, input) - no bounds checking
        r'call\s+\w*strcpy',
        r'call\s+\w*strcat',
        r'call\s+\w*sprintf',
        # gets(buf) - always dangerous
        r'call\s+\w*gets\b',
        # scanf without width specifier
        r'call\s+\w*scanf.*%s',
    ]

    FORMAT_STRING_PATTERNS = [
        # printf(user_input) - format string vulnerability
        r'call\s+\w*printf.*\bsi\b',  # user-controlled format in rsi
        r'call\s+\w*fprintf.*\bsi\b',
    ]

    USE_AFTER_FREE_PATTERNS = [
        # free(ptr) followed by use of ptr
        r'call\s+\w*free.*',
        r'mov.*\[\w+\].*,\s*\w+',  # dereference after free
    ]

    INTEGER_OVERFLOW_PATTERNS = [
        # mul without overflow check
        r'\bmul\b',
        r'\bimul\b.*\[\w+\]',  # imul with memory operand
        # add without carry check
        r'\badd\b.*\beax\b',
    ]

    def __init__(self):
        self.compiled_patterns = {
            'buffer_overflow': [re.compile(p, re.IGNORECASE)
                              for p in self.BUFFER_OVERFLOW_PATTERNS],
            'format_string': [re.compile(p, re.IGNORECASE)
                             for p in self.FORMAT_STRING_PATTERNS],
            'use_after_free': [re.compile(p, re.IGNORECASE)
                              for p in self.USE_AFTER_FREE_PATTERNS],
            'integer_overflow': [re.compile(p, re.IGNORECASE)
                               for p in self.INTEGER_OVERFLOW_PATTERNS],
        }

    def scan_function(self, function_address, disassembly_text):
        """Scan a disassembled function for vulnerability patterns."""
        findings = []
        for vuln_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = list(pattern.finditer(disassembly_text))
                for match in matches:
                    findings.append({
                        'vulnerability_type': vuln_type,
                        'function_address': function_address,
                        'matched_text': match.group(),
                        'offset': match.start(),
                        'confidence': self._estimate_confidence(vuln_type),
                    })
        return findings

    def _estimate_confidence(self, vuln_type):
        confidence_map = {
            'buffer_overflow': 0.7,
            'format_string': 0.8,
            'use_after_free': 0.6,
            'integer_overflow': 0.5,
        }
        return confidence_map.get(vuln_type, 0.5)

    def scan_binary(self, disasm_engine, code_section):
        """Scan entire code section for vulnerabilities."""
        all_findings = []
        functions = disasm_engine.get_functions()

        for func in functions:
            disasm = disasm_engine.disassemble_function(func['address'])
            disasm_text = '\n'.join(
                f"0x{i['address']:x}: {i['mnemonic']} {i['op_str']}"
                for i in disasm
            )
            findings = self.scan_function(func['address'], disasm_text)
            all_findings.extend(findings)

        return all_findings
```

### Binary Diffing with Hash-Based Comparison

Comparing two binary versions to identify changes, patches, and updates.

```python
import hashlib
from collections import OrderedDict

class BinaryDiffer:
    """Compare two binary executables at function and section levels."""

    def __init__(self):
        self.hash_cache = {}

    def compute_function_hashes(self, disasm_engine, binary_path):
        """Compute hash for each function in a binary."""
        functions = disasm_engine.get_functions(binary_path)
        hashes = {}

        for func in functions:
            code = disasm_engine.get_function_bytes(
                binary_path, func['offset'], func['size'])
            # Normalize the code (ignore addresses, just hash opcodes)
            normalized = self._normalize_code(code)
            func_hash = hashlib.sha256(normalized).hexdigest()
            hashes[func_hash] = {
                'name': func['name'],
                'address': func['offset'],
                'size': func['size'],
                'hash': func_hash,
            }

        return hashes

    def diff_binaries(self, old_disasm, new_disasm,
                      old_binary, new_binary):
        """Compare two binaries and report differences."""
        old_hashes = self.compute_function_hashes(old_disasm, old_binary)
        new_hashes = self.compute_function_hashes(new_disasm, new_binary)

        old_by_hash = {h: info for h, info in old_hashes.items()}
        new_by_hash = {h: info for h, info in new_hashes.items()}

        old_names = {info['name'] for info in old_hashes.values()}
        new_names = {info['name'] for info in new_hashes.values()}

        # Functions that exist in both but with different hashes = modified
        modified = []
        # Functions only in old = removed
        removed = []
        # Functions only in new = added
        added = []
        # Functions with same hash = unchanged
        unchanged = []

        for h, old_info in old_by_hash.items():
            if h in new_by_hash:
                unchanged.append(old_info)
            else:
                # Check by name
                name = old_info['name']
                matching_new = [info for info in new_by_hash.values()
                               if info['name'] == name]
                if matching_new:
                    modified.append({
                        'name': name,
                        'old': old_info,
                        'new': matching_new[0],
                    })
                else:
                    removed.append(old_info)

        for h, new_info in new_by_hash.items():
            if h not in old_by_hash:
                name = new_info['name']
                matching_old = [info for info in old_by_hash.values()
                               if info['name'] == name]
                if not matching_old:
                    added.append(new_info)

        return {
            'modified': modified,
            'added': added,
            'removed': removed,
            'unchanged': unchanged,
            'summary': {
                'total_old': len(old_hashes),
                'total_new': len(new_hashes),
                'modified': len(modified),
                'added': len(added),
                'removed': len(removed),
                'unchanged': len(unchanged),
            }
        }

    def _normalize_code(self, code_bytes):
        """Normalize code for comparison (remove address-dependent bytes)."""
        # Simple normalization: hash all bytes but mask address-dependent fields
        return code_bytes
```

### Export Table Analysis and DLL Functionality Mapping

Mapping exported DLL functions to their likely capabilities.

```python
class ExportAnalyzer:
    """Analyze DLL export tables to map functionality."""

    CAPABILITY_KEYWORDS = {
        'crypto': ['encrypt', 'decrypt', 'hash', 'sign', 'verify',
                   'aes', 'rsa', 'sha', 'md5', 'hmac', 'cipher'],
        'network': ['connect', 'send', 'recv', 'socket', 'bind',
                    'listen', 'accept', 'http', 'dns', 'ftp', 'smtp'],
        'file': ['read', 'write', 'open', 'close', 'create', 'delete',
                 'copy', 'move', 'find', 'enumerate'],
        'process': ['create', 'spawn', 'inject', 'terminate', 'enum',
                   'suspend', 'resume', 'thread'],
        'registry': ['reg', 'key', 'value', 'query', 'set', 'delete'],
        'memory': ['alloc', 'free', 'protect', 'map', 'commit'],
        'authentication': ['login', 'auth', 'token', 'credential',
                          'password', 'logon', 'session'],
    }

    def __init__(self, exports):
        self.exports = exports

    def categorize_exports(self):
        """Categorize exports by likely functionality."""
        categorized = {cat: [] for cat in self.CAPABILITY_KEYWORDS}

        for exp in self.exports:
            name_lower = exp['name'].lower()
            for category, keywords in self.CAPABILITY_KEYWORDS.items():
                if any(kw in name_lower for kw in keywords):
                    categorized[category].append(exp)
                    break

        return categorized

    def find_suspicious_exports(self):
        """Find exports that suggest suspicious functionality."""
        suspicious = []
        suspicious_keywords = [
            'inject', 'hook', 'detour', 'patch', 'bypass',
            'hide', 'stealth', 'rootkit', 'keylog', 'capture',
            'screenshot', 'webcam', 'microphone', 'clipboard',
            'password', 'credential', 'token', 'cookie',
        ]

        for exp in self.exports:
            name_lower = exp['name'].lower()
            for keyword in suspicious_keywords:
                if keyword in name_lower:
                    suspicious.append({
                        'export': exp,
                        'reason': f'Contains suspicious keyword: {keyword}',
                        'risk_level': 'high',
                    })
                    break

        return suspicious

    def detect_ordinals_only(self):
        """Find exports that are ordinal-only (no name)."""
        return [exp for exp in self.exports
                if not exp.get('name') or exp['name'].startswith('#')]
