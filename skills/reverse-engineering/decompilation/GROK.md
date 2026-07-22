---
name: "decompilation"
category: "reverse-engineering"
version: "1.0.0"
tags: ["reverse-engineering", "decompilation", "ghidra", "hex-rays", "ret-decompiler"]
---

# Decompilation — Reverse Engineering Module

## Overview

Decompilation is the process of translating compiled binary code back into higher-level source code representations. Unlike disassembly, which produces assembly language, decompilation recovers structure — functions, control flow, data types, and variable names — making the binary's logic comprehensible to human analysts.

This module provides a framework for programmatic decompilation using multiple decompiler backends: Ghidra headless mode, RetDec, and native Python-based decompilation heuristics. It produces structured decompilation output (C-like pseudocode) that can be searched, annotated, and cross-referenced for vulnerability research, malware analysis, and code audit workflows.

Decompilation is fundamentally imprecise — source-level constructs like variable names, comments, and type information are largely lost during compilation. The decompiler must infer these through analysis of data flow, control flow, and calling conventions. Different decompilers produce different output for the same binary due to differing heuristics and inference strategies. This module supports multiple backends precisely so analysts can cross-validate findings across decompilers.

Key capabilities include: function-level decompilation with pseudocode output, type recovery and propagation, cross-reference analysis, string and constant extraction, data structure reconstruction, and decompilation diff between binary versions. The module produces both human-readable output and structured JSON for programmatic consumption.

## Core Capabilities

### 1. Multi-Backend Decompilation
Leverage multiple decompilation engines: Ghidra headless for production-grade decompilation with type recovery, RetDec for open-source architecture-agnostic decompilation, and native Python heuristics for quick function-level analysis. Each backend produces C-like pseudocode with varying levels of detail and accuracy.

### 2. Function-Level Decompilation
Decompile individual functions by address, name, or offset. Extract the decompiled pseudocode along with metadata: local variables, parameters, call targets, and referenced strings. This targeted approach is ideal for focused vulnerability analysis and code review.

### 3. Type Recovery and Inference
Recover data types from binary code: parameter types via calling convention analysis, local variable types via data flow analysis, struct definitions via memory access patterns, and enum values via constant propagation. Type information significantly improves decompilation output readability.

### 4. Cross-Reference Analysis
Map relationships between code and data: find all callers of a function, all functions called by a function, all references to a global variable, and all cross-references to a string. Cross-references are essential for understanding data flow and control flow across the binary.

### 5. Data Structure Reconstruction
Infer data structures from how they are accessed in code: field offsets, array indexing patterns, pointer chains, and vtable layouts. Reconstructing struct definitions transforms raw pointer arithmetic into readable field accesses.

### 6. Decompilation Diffing
Compare decompiled output between two versions of a binary (or two different binaries) to identify: modified functions, new or removed functions, changed logic, and patched vulnerabilities. This is essential for patch analysis and regression identification.

### 7. String and Constant Extraction with Context
Extract strings and constants from decompiled code with full context: which function references them, at what offset, and how they are used. This contextual information is more valuable than raw string extraction because it reveals the string's purpose.

### 8. Batch Decompilation and Indexing
Decompile entire binaries or large function sets in batch, building a searchable index of all decompiled functions, strings, types, and cross-references. This index enables fast grep-style searching across the entire decompiled codebase.

## Usage Examples

### Ghidra Headless Decompilation

```python
from decompilation_engine import GhidraDecompiler, DecompilationResult

decompiler = GhidraDecompiler(ghidra_install="/opt/ghidra")
result = decompiler.decompile_function(
    binary_path="/path/to/target.exe",
    address=0x00401000,
)

print(f"Function: {result.function_name}")
print(f"Address: 0x{result.address:08x}")
print(f"Parameters: {result.parameters}")
print(f"Local variables: {result.local_variables}")
print(f"\nDecompiled code:\n{result.pseudocode}")
```

### RetDec Decompilation

```python
from decompilation_engine import RetDecDecompiler

decompiler = RetDecDecompiler()
result = decompiler.decompile(
    binary_path="/path/to/sample",
    target_arch="x86-64",
    target_os="linux",
)

for func in result.functions[:5]:
    print(f"\n{'='*60}")
    print(f"Function: {func.function_name} @ 0x{func.address:08x}")
    print(f"Signature: {func.signature}")
    print(f"Lines of code: {len(func.pseudocode.splitlines())}")
    print(f"\n{func.pseudocode[:500]}...")
```

### Type Recovery and Struct Reconstruction

```python
from decompilation_engine import TypeRecoveryEngine

engine = TypeRecoveryEngine()
recovered = engine.analyze(
    binary_path="/path/to/target",
    function_address=0x00401000,
)

print("Recovered types:")
for param in recovered.parameter_types:
    print(f"  {param.name}: {param.type_name} ({param.size} bytes)")

print("\nRecovered structs:")
for struct in recovered.struct_definitions:
    print(f"  struct {struct.name} {{")
    for field in struct.fields:
        print(f"    {field.type_name} {field.name}; // offset {field.offset}")
    print(f"  }};")

print("\nRecovered enums:")
for enum in recovered.enum_definitions:
    print(f"  enum {enum.name} {{")
    for value in enum.values:
        print(f"    {value.name} = {value.value},")
    print(f"  }};")
```

### Cross-Reference Analysis

```python
from decompilation_engine import CrossReferenceAnalyzer

analyzer = CrossReferenceAnalyzer()
xrefs = analyzer.analyze("/path/to/target")

# Find all callers of a function
callers = xrefs.get_callers("validate_input")
print(f"Functions calling validate_input: {len(callers)}")
for caller in callers:
    print(f"  {caller.caller_name} @ 0x{caller.caller_address:08x}")

# Find all references to a string
refs = xrefs.get_string_references("SELECT * FROM users")
print(f"\nCode referencing 'SELECT * FROM users': {len(refs)}")
for ref in refs:
    print(f"  {ref.function_name} @ 0x{ref.address:08x}")
```

### Function Signature Analysis

```python
from decompilation_engine import SignatureAnalyzer

analyzer = SignatureAnalyzer()
signatures = analyzer.extract_signatures("/path/to/target")

print(f"Detected {len(signatures)} function signatures:\n")
for sig in signatures[:10]:
    print(f"  {sig.return_type} {sig.function_name}({', '.join(sig.parameters)})")
    print(f"    Address: 0x{sig.address:08x}")
    print(f"    Calling convention: {sig.calling_convention}")
    print(f"    Stack frame size: {sig.stack_frame_size} bytes")
```

### Decompilation Diff

```python
from decompilation_engine import DecompilationDiffer

differ = DecompilationDiffer()
diff = differ.diff(
    old_binary="/path/to/vulnerable.so",
    new_binary="/path/to/patched.so",
)

print(f"Modified functions: {len(diff.modified)}")
print(f"Added functions: {len(diff.added)}")
print(f"Removed functions: {len(diff.removed)}")

for mod in diff.modified:
    print(f"\n  {mod.function_name}:")
    print(f"    Old signature: {mod.old_signature}")
    print(f"    New signature: {mod.new_signature}")
    if mod.logic_changes:
        print(f"    Logic changes:")
        for change in mod.logic_changes:
            print(f"      {change}")
```

### Batch Decompilation with Search

```python
from decompilation_engine import BatchDecompiler, DecompilationIndex

batch = BatchDecompiler(max_workers=4)
index = batch.decompile_and_index("/path/to/binary.exe")

# Search for SQL injection patterns
results = index.search(r"SELECT.*\+.*input")
print(f"Potential SQL injection points: {len(results)}")
for r in results:
    print(f"  {r.function_name} @ 0x{r.address:08x}")
    print(f"  Match: {r.matched_text[:80]}")

# Search for hardcoded credentials
results = index.search(r"password.*=.*\"[^\"]+\"")
print(f"\nHardcoded credentials: {len(results)}")
for r in results:
    print(f"  {r.function_name}: {r.matched_text}")
```

### Vulnerability Pattern Detection

```python
from decompilation_engine import VulnerabilityDetector

detector = VulnerabilityDetector()
findings = detector.scan("/path/to/target")

print(f"Potential vulnerabilities: {len(findings)}")
for finding in findings:
    print(f"\n  [{finding.severity}] {finding.vuln_type}")
    print(f"  Function: {finding.function_name}")
    print(f"  Address: 0x{finding.address:08x}")
    print(f"  Description: {finding.description}")
    print(f"  Code:\n{finding.code_snippet}")
```

### Exported Function Table

```python
from decompilation_engine import ExportAnalyzer

analyzer = ExportAnalyzer()
exports = analyzer.analyze("/path/to/library.dll")

print(f"Exported functions: {len(exports)}")
for exp in exports:
    print(f"  {exp.ordinal:4d} | 0x{exp.address:08x} | {exp.name}")
    if exp.is_forwarded:
        print(f"         -> Forwarded to: {exp.forward_target}")
```

### Pseudocode Annotation

```python
from decompilation_engine import AnnotationEngine

annotator = AnnotationEngine()
annotated = annotator.annotate(
    binary_path="/path/to/target",
    address=0x00401000,
    annotations={
        0x00401020: "Input validation check",
        0x00401045: "Buffer overflow here - no bounds check",
        0x00401060: "Cryptographic operation",
    }
)

print("Annotated pseudocode:")
print(annotated)
```

## Best Practices

### 1. Start with High-Confidence Functions
Begin analysis with well-known functions: `main()`, exported functions, functions with clear string references, and library function wrappers. These have the highest decompilation accuracy and provide entry points for deeper analysis.

### 2. Cross-Validate with Multiple Decompilers
Different decompilers use different heuristics and produce different output. When you find something important, verify it across at least two decompilers (e.g., Ghidra and RetDec). Discrepancies may reveal decompiler limitations or, more interestingly, intentional obfuscation.

### 3. Understand Decompiler Limitations
Decompilers struggle with: optimized code (inlined functions, register allocation), self-modifying code, hand-written assembly, obfuscated code, and unusual calling conventions. Recognize these situations and fall back to manual disassembly when decompilation produces nonsensical output.

### 4. Annotate Your Findings
Decompilation output is generated code — it lacks the context that makes source code meaningful. Add comments, rename variables, and document your understanding as you analyze. Many decompilation tools (Ghidra, IDA) support user annotations that persist across sessions.

### 5. Preserve Function Boundaries
Decompiler accuracy depends on correct function boundary detection. If the decompiler misidentifies function boundaries (e.g., treats data as code or vice versa), manually define correct boundaries before decompilation. This is especially important for binaries without symbol information.

### 6. Use Type Information Strategically
Manually defining types (structs, enums, typedefs) before decompilation dramatically improves output quality. If you identify a data structure through manual analysis, define it in the decompiler's type system and re-decompile affected functions.

### 7. Analyze Control Flow Before Data Flow
Understanding the program's control flow (if/else branches, loops, switch statements) provides context for data flow analysis. Start by mapping the function's control flow graph, then trace data through the identified paths.

### 8. Document Uncertainty
Decompilation involves inference. When the decompiler produces a result you're uncertain about, mark it as uncertain in your notes. Distinguish between what the decompiler definitively shows and what requires human interpretation.

## Related Modules

| Module | Relationship |
|--------|-------------|
| `binary-analysis` | Decompilation requires binary analysis for format parsing and function boundary detection |
| `malware-analysis` | Decompiled code reveals malware logic, algorithms, and C2 protocol implementations |
| `protocol-analysis` | Protocol implementations in binaries are best understood through decompilation of network handlers |
| `firmware-analysis` | Firmware contains compiled code that decompilation recovers for analysis |

## Decompiler Output Analysis

### Understanding Decompiler Artifacts

Different decompilers produce varying output for the same binary. Understanding these differences is crucial for accurate analysis.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re

@dataclass
class DecompilerOutput:
    """Structured representation of decompiled code."""
    function_name: str
    address: int
    pseudocode: str
    decompiler: str  # 'ghidra', 'retdec', 'hexrays'
    confidence: float
    warnings: List[str] = field(default_factory=list)
    inferred_types: Dict[str, str] = field(default_factory=dict)
    call_targets: List[str] = field(default_factory=list)
    strings_referenced: List[str] = field(default_factory=list)

class DecompilerOutputAnalyzer:
    """Analyze and compare decompiler outputs."""

    # Common decompiler artifacts
    ARTIFACT_PATTERNS = {
        'ghidra': {
            'unhandled': re.compile(r'UNHANDLED|<UNRESOLVED|???'),
            'stack_var': re.compile(r'local_[0-9a-f]+'),
            'thunk': re.compile(r' thunk '),
            'datatype': re.compile(r'(undefined|int|uint|char|byte|long|ulong|float|double|void)\s'),
        },
        'retdec': {
            'unhandled': re.compile(r'UNHANDLED|unknown|unk_'),
            'stack_var': re.compile(r'stack_[0-9a-f]+'),
            'thunk': re.compile(r' th_'),
            'datatype': re.compile(r'(int|uint8_t|uint16_t|uint32_t|uint64_t|char|void)\s'),
        },
        'hexrays': {
            'unhandled': re.compile(r'v[0-9]+|a[0-9]+'),
            'stack_var': re.compile(r'[sv]\d+'),
            'thunk': re.compile(r'j_'),
            'datatype': re.compile(r'(int|__int64|__int32|__int16|__int8|void|char)\s'),
        },
    }

    def __init__(self):
        self.outputs: List[DecompilerOutput] = []

    def add_output(self, output: DecompilerOutput):
        """Add a decompiler output for analysis."""
        self.outputs.append(output)

    def detect_artifacts(self, output: DecompilerOutput) -> Dict[str, List[str]]:
        """Detect common decompiler artifacts in output."""
        artifacts = {}
        patterns = self.ARTIFACT_PATTERNS.get(output.decompiler, {})

        for artifact_type, pattern in patterns.items():
            matches = pattern.findall(output.pseudocode)
            if matches:
                artifacts[artifact_type] = list(set(matches))

        return artifacts

    def compare_outputs(self, output_a: DecompilerOutput,
                        output_b: DecompilerOutput) -> dict:
        """Compare outputs from two different decompilers."""
        comparison = {
            'function_a': output_a.function_name,
            'function_b': output_b.function_name,
            'decompiler_a': output_a.decompiler,
            'decompiler_b': output_b.decompiler,
        }

        # Compare function signatures
        sig_a = self._extract_signature(output_a.pseudocode)
        sig_b = self._extract_signature(output_b.pseudocode)
        comparison['signatures_match'] = sig_a == sig_b
        comparison['signature_a'] = sig_a
        comparison['signature_b'] = sig_b

        # Compare call targets
        calls_a = set(self._extract_calls(output_a.pseudocode))
        calls_b = set(self._extract_calls(output_b.pseudocode))
        comparison['calls_in_common'] = list(calls_a & calls_b)
        comparison['calls_only_in_a'] = list(calls_a - calls_b)
        comparison['calls_only_in_b'] = list(calls_b - calls_a)

        # Compare string references
        strings_a = set(self._extract_strings(output_a.pseudocode))
        strings_b = set(self._extract_strings(output_b.pseudocode))
        comparison['strings_in_common'] = list(strings_a & strings_b)
        comparison['strings_only_in_a'] = list(strings_a - strings_b)
        comparison['strings_only_in_b'] = list(strings_b - strings_a)

        # Compare structural complexity
        comparison['complexity_a'] = self._calculate_complexity(output_a.pseudocode)
        comparison['complexity_b'] = self._calculate_complexity(output_b.pseudocode)

        return comparison

    def _extract_signature(self, pseudocode: str) -> str:
        """Extract the function signature from pseudocode."""
        lines = pseudocode.strip().splitlines()
        if lines:
            # First line is typically the signature
            return lines[0].strip()
        return ''

    def _extract_calls(self, pseudocode: str) -> List[str]:
        """Extract function call targets from pseudocode."""
        call_pattern = re.compile(r'(\w+)\s*\(')
        # Filter out common keywords and operators
        keywords = {'if', 'while', 'for', 'switch', 'return', 'sizeof',
                    'sizeof', 'typeof', 'true', 'false', 'NULL', 'null',
                    'int', 'char', 'void', 'long', 'unsigned', 'signed'}
        calls = []
        for match in call_pattern.finditer(pseudocode):
            name = match.group(1)
            if name not in keywords and not name.startswith('_'):
                calls.append(name)
        return list(set(calls))

    def _extract_strings(self, pseudocode: str) -> List[str]:
        """Extract string literals from pseudocode."""
        string_pattern = re.compile(r'"([^"\\]|\\.)*"')
        return [m.group() for m in string_pattern.finditer(pseudocode)]

    def _calculate_complexity(self, pseudocode: str) -> dict:
        """Calculate various complexity metrics."""
        lines = pseudocode.splitlines()

        # Count control flow constructs
        if_count = sum(1 for l in lines if re.search(r'\bif\s*\(', l))
        while_count = sum(1 for l in lines if re.search(r'\bwhile\s*\(', l))
        for_count = sum(1 for l in lines if re.search(r'\bfor\s*\(', l))
        switch_count = sum(1 for l in lines if re.search(r'\bswitch\s*\(', l))
        case_count = sum(1 for l in lines if re.search(r'\bcase\s+', l))
        return_count = sum(1 for l in lines if re.search(r'\breturn\b', l))
        goto_count = sum(1 for l in lines if re.search(r'\bgoto\s+', l))

        # Cyclomatic complexity
        cyclomatic = if_count + while_count + for_count + switch_count + 1

        return {
            'total_lines': len(lines),
            'if_statements': if_count,
            'while_loops': while_count,
            'for_loops': for_count,
            'switch_statements': switch_count,
            'case_labels': case_count,
            'return_statements': return_count,
            'goto_statements': goto_count,
            'cyclomatic_complexity': cyclomatic,
            'nesting_depth': self._max_nesting_depth(lines),
        }

    def _max_nesting_depth(self, lines: List[str]) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0
        current_depth = 0

        for line in lines:
            stripped = line.strip()
            # Count opening braces
            current_depth += stripped.count('{') - stripped.count('}')
            max_depth = max(max_depth, current_depth)

        return max(max_depth, 0)

    def detect_vulnerabilities(self, output: DecompilerOutput) -> List[dict]:
        """Detect vulnerability patterns in decompiled code."""
        findings = []
        pseudocode = output.pseudocode

        # Buffer overflow patterns
        overflow_patterns = [
            (re.compile(r'strcpy\s*\([^,]+,\s*(\w+)'), 'strcpy buffer overflow'),
            (re.compile(r'strcat\s*\([^,]+,\s*(\w+)'), 'strcat buffer overflow'),
            (re.compile(r'sprintf\s*\([^,]+,\s*"[^"]*%s'), 'sprintf format string'),
            (re.compile(r'gets\s*\('), 'gets always overflow'),
            (re.compile(r'scanf\s*\([^"]*%s'), 'scanf format string overflow'),
            (re.compile(r'memcpy\s*\([^,]+,[^,]+,.*\b(len|size|length)\b'),
             'memcpy with variable length'),
        ]

        for pattern, description in overflow_patterns:
            if pattern.search(pseudocode):
                findings.append({
                    'type': 'buffer_overflow',
                    'severity': 'high',
                    'description': description,
                    'function': output.function_name,
                })

        # Use-after-free patterns
        uaf_pattern = re.compile(
            r'free\s*\((\w+)\).*?\1\b.*?(?:->|\*)',
            re.DOTALL
        )
        if uaf_pattern.search(pseudocode):
            findings.append({
                'type': 'use_after_free',
                'severity': 'high',
                'function': output.function_name,
            })

        # Format string vulnerability
        format_pattern = re.compile(
            r'printf\s*\(\s*(\w+)\s*\)',
            re.IGNORECASE
        )
        if format_pattern.search(pseudocode):
            findings.append({
                'type': 'format_string',
                'severity': 'high',
                'function': output.function_name,
            })

        # SQL injection patterns
        sql_pattern = re.compile(
            r'(?:SELECT|INSERT|UPDATE|DELETE).*["\'].*\+.*\w+',
            re.IGNORECASE
        )
        if sql_pattern.search(pseudocode):
            findings.append({
                'type': 'sql_injection',
                'severity': 'high',
                'function': output.function_name,
            })

        # Command injection
        cmd_pattern = re.compile(
            r'(?:system|popen|exec[vl]?)\s*\(\s*.*\+',
            re.IGNORECASE
        )
        if cmd_pattern.search(pseudocode):
            findings.append({
                'type': 'command_injection',
                'severity': 'critical',
                'function': output.function_name,
            })

        return findings
```

### Function Boundary Detection

Accurate function boundary detection is critical for decompilation quality.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import struct

@dataclass
class FunctionBoundary:
    """Detected function boundary."""
    start_address: int
    end_address: int
    name: str
    confidence: float
    detection_method: str  # 'symbol', 'prologue', 'call_ref', 'return_scan'
    prologue_pattern: Optional[str] = None

class FunctionBoundaryDetector:
    """Detect function boundaries in disassembled code."""

    # Common function prologues (x86-64)
    PROLOGUES_64BIT = [
        (b'\x55\x48\x89\xe5', 'push rbp; mov rbp, rsp', 0.95),
        (b'\x48\x89\xe5', 'mov rbp, rsp', 0.85),
        (b'\x48\x83\xec', 'sub rsp, imm8', 0.80),
        (b'\x31\xed', 'xor ebp, ebp', 0.75),
        (b'\x41\x57\x41\x56\x41\x55\x41\x54', 'push r15-r12', 0.85),
        (b'\x53\x57\x56', 'push rbx; push rdi; push rsi', 0.70),
    ]

    # Common function prologues (x86-32)
    PROLOGUES_32BIT = [
        (b'\x55\x89\xe5', 'push ebp; mov ebp, esp', 0.95),
        (b'\x89\xe5', 'mov ebp, esp', 0.85),
        (b'\x83\xec', 'sub esp, imm8', 0.80),
        (b'\x53\x56\x57', 'push ebx; push esi; push edi', 0.70),
    ]

    # Common function prologues (ARM)
    PROLOGUES_ARM = [
        (b'\xf0\x4f\x2d\xe9', 'push {r4-r11, lr}', 0.90),
        (b'\x00\x48\x2d\xe9', 'push {fp, lr}', 0.85),
        (b'\x04\xe0\x2d\xe5', 'push {lr}', 0.75),
    ]

    # Common return instructions
    RETURNS = {
        'x86_64': [b'\xc3', b'\xc2', b'\xcb'],
        'x86_32': [b'\xc3', b'\xc2', b'\xcb'],
        'arm': [b'\x1e\xff\x2f\xe1'],  # bx lr
        'arm64': [b'\xc0\x03\x5f\xd6'],  # ret
    }

    def __init__(self, architecture='x86_64'):
        self.architecture = architecture
        self.functions: List[FunctionBoundary] = []

    def detect_from_symbols(self, symbols: List[dict]) -> List[FunctionBoundary]:
        """Use symbol information to establish function boundaries."""
        boundaries = []
        for sym in symbols:
            if sym.get('type') == 'STT_FUNC' or sym.get('size', 0) > 0:
                boundaries.append(FunctionBoundary(
                    start_address=sym['address'],
                    end_address=sym['address'] + sym.get('size', 0),
                    name=sym.get('name', f'func_{sym["address"]:x}'),
                    confidence=0.95,
                    detection_method='symbol',
                ))
        self.functions.extend(boundaries)
        return boundaries

    def detect_from_prologues(self, code_bytes: bytes,
                               base_address: int = 0) -> List[FunctionBoundary]:
        """Detect functions by scanning for prologue patterns."""
        boundaries = []
        prologues = (self.PROLOGUES_64BIT if self.architecture == 'x86_64'
                    else self.PROLOGUES_32BIT if self.architecture == 'x86_32'
                    else self.PROLOGUES_ARM)

        for pattern, name, confidence in prologues:
            offset = 0
            while True:
                pos = code_bytes.find(pattern, offset)
                if pos == -1:
                    break

                func_addr = base_address + pos
                # Check if already detected
                if not any(f.start_address == func_addr for f in boundaries):
                    boundaries.append(FunctionBoundary(
                        start_address=func_addr,
                        end_address=0,  # Will be resolved later
                        name=f'func_{func_addr:x}',
                        confidence=confidence,
                        detection_method='prologue',
                        prologue_pattern=name,
                    ))
                offset = pos + len(pattern)

        self.functions.extend(boundaries)
        return boundaries

    def detect_from_call_references(self, code_bytes: bytes,
                                     call_targets: Set[int],
                                     base_address: int = 0) -> List[FunctionBoundary]:
        """Detect functions from call instruction targets."""
        boundaries = []
        for target in call_targets:
            if not any(f.start_address == target for f in self.functions):
                boundaries.append(FunctionBoundary(
                    start_address=target,
                    end_address=0,
                    name=f'func_{target:x}',
                    confidence=0.70,
                    detection_method='call_ref',
                ))
        self.functions.extend(boundaries)
        return boundaries

    def resolve_end_addresses(self, code_bytes: bytes, base_address: int = 0):
        """Resolve function end addresses by finding return instructions."""
        returns = self.RETURNS.get(self.architecture, [b'\xc3'])

        for func in self.functions:
            if func.end_address != 0:
                continue

            # Search forward from function start for return instruction
            start_offset = func.start_address - base_address
            min_end = start_offset + 4  # Minimum function size

            # Search in reasonable range (up to 10KB)
            search_range = min(start_offset + 10240, len(code_bytes))
            for offset in range(start_offset + 4, search_range):
                for ret_pattern in returns:
                    if code_bytes[offset:offset+len(ret_pattern)] == ret_pattern:
                        func.end_address = base_address + offset + len(ret_pattern)
                        break
                if func.end_address != 0:
                    break

            # If no return found, set a default
            if func.end_address == 0:
                func.end_address = func.start_address + 256  # Default size

    def merge_overlapping(self):
        """Merge overlapping function boundaries."""
        if not self.functions:
            return

        # Sort by start address
        self.functions.sort(key=lambda f: f.start_address)

        merged = [self.functions[0]]
        for func in self.functions[1:]:
            last = merged[-1]
            if func.start_address < last.end_address:
                # Overlapping — keep the one with higher confidence
                if func.confidence > last.confidence:
                    merged[-1] = func
                # Extend end address if needed
                if func.end_address > last.end_address:
                    merged[-1].end_address = func.end_address
            else:
                merged.append(func)

        self.functions = merged

    def generate_function_map(self) -> str:
        """Generate a text-based function map."""
        lines = []
        for func in sorted(self.functions, key=lambda f: f.start_address):
            size = func.end_address - func.start_address
            lines.append(
                f"0x{func.start_address:08x}-0x{func.end_address:08x} "
                f"({size:5d} bytes) [{func.confidence:.0%}] "
                f"{func.name}"
            )
        return '\n'.join(lines)
```

### Type Recovery Engine

Advanced type inference from decompiled code and binary analysis.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
import re

@dataclass
class RecoveredType:
    """A type recovered from binary analysis."""
    name: str
    kind: str  # 'primitive', 'struct', 'enum', 'pointer', 'array', 'function'
    size: int
    base_type: Optional[str] = None
    fields: List[Dict] = field(default_factory=list)
    values: List[Dict] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class FunctionPrototype:
    """Recovered function prototype."""
    name: str
    return_type: str
    parameters: List[Dict]
    calling_convention: str
    confidence: float

class TypeRecoveryEngine:
    """Recover types from binary code through multiple analysis passes."""

    def __init__(self):
        self.types: Dict[str, RecoveredType] = {}
        self.prototypes: Dict[str, FunctionPrototype] = {}
        self.type_usage: Dict[str, List[str]] = {}

    def recover_from_disassembly(self, instructions: List[dict]):
        """Recover types from instruction patterns."""
        for insn in instructions:
            mnemonic = insn.get('mnemonic', '')
            op_str = insn.get('op_str', '')

            # Detect size from move instructions
            size_hints = self._extract_size_hints(mnemonic, op_str)
            for reg, size in size_hints.items():
                self._update_type_hint(reg, size)

            # Detect struct access patterns
            struct_access = self._detect_struct_access(op_str)
            if struct_access:
                base_reg, offset = struct_access
                self._update_struct_field(base_reg, offset, size_hints.get(base_reg, 4))

    def _extract_size_hints(self, mnemonic: str, op_str: str) -> Dict[str, int]:
        """Extract size hints from instruction mnemonic and operands."""
        hints = {}

        # x86 size suffixes
        size_map = {
            'movb': 1, 'movw': 2, 'movl': 4, 'movq': 8,
            'movzx': 4, 'movsx': 4,
            'addb': 1, 'addw': 2, 'addl': 4, 'addq': 8,
            'cmpb': 1, 'cmpw': 2, 'cmpl': 4, 'cmpq': 8,
        }

        for suffix, size in size_map.items():
            if mnemonic == suffix or mnemonic.startswith(suffix):
                # Extract register operand
                regs = re.findall(r'\b(\w+)\b', op_str)
                for reg in regs:
                    hints[reg] = size
                break

        return hints

    def _detect_struct_access(self, op_str: str) -> Optional[tuple]:
        """Detect struct field access pattern [reg + offset]."""
        match = re.search(r'\[(\w+)\s*\+\s*(0x[0-9a-f]+|\d+)\]', op_str)
        if match:
            reg = match.group(1)
            offset = int(match.group(2), 0)
            return (reg, offset)
        return None

    def _update_type_hint(self, reg: str, size: int):
        """Update type hint for a register."""
        type_name = {
            1: 'uint8_t', 2: 'uint16_t',
            4: 'uint32_t', 8: 'uint64_t',
        }.get(size, 'unknown')

        if reg not in self.types:
            self.types[reg] = RecoveredType(
                name=reg, kind='primitive', size=size,
                confidence=0.5
            )

    def _update_struct_field(self, base_reg: str, offset: int, field_size: int):
        """Update struct type with a discovered field."""
        struct_name = f'struct_{base_reg}'
        if struct_name not in self.types:
            self.types[struct_name] = RecoveredType(
                name=struct_name, kind='struct', size=offset + field_size,
                confidence=0.3
            )

        struct = self.types[struct_name]
        # Check if field already exists
        existing = [f for f in struct.fields if f['offset'] == offset]
        if not existing:
            field_type = {
                1: 'uint8_t', 2: 'uint16_t',
                4: 'uint32_t', 8: 'uint64_t',
            }.get(field_size, f'unknown_{field_size}')
            struct.fields.append({
                'offset': offset,
                'type': field_type,
                'size': field_size,
                'name': f'field_{offset:x}',
            })
            struct.confidence = min(1.0, struct.confidence + 0.1)

    def recover_from_calling_convention(self, function_calls: List[dict]):
        """Infer parameter types from calling convention patterns."""
        # x86-64 System V ABI
        arg_registers = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']

        for call in function_calls:
            func_name = call.get('target', '')
            arg_values = call.get('arguments', {})

            if func_name not in self.prototypes:
                self.prototypes[func_name] = FunctionPrototype(
                    name=func_name,
                    return_type='void',
                    parameters=[],
                    calling_convention='system_v',
                    confidence=0.4,
                )

            proto = self.prototypes[func_name]
            for i, reg in enumerate(arg_registers):
                if reg in arg_values:
                    value = arg_values[reg]
                    param_type = self._infer_type_from_value(value)
                    while len(proto.parameters) <= i:
                        proto.parameters.append({'type': 'unknown', 'name': f'arg{i}'})
                    proto.parameters[i]['type'] = param_type
                    proto.confidence = min(1.0, proto.confidence + 0.05)

    def _infer_type_from_value(self, value) -> str:
        """Infer type from a constant value."""
        if isinstance(value, int):
            if 0 <= value <= 0xFF:
                return 'uint8_t'
            elif 0 <= value <= 0xFFFF:
                return 'uint16_t'
            elif 0 <= value <= 0xFFFFFFFF:
                return 'uint32_t'
            elif value > 0xFFFFFFFF:
                return 'uint64_t'
        elif isinstance(value, str):
            if value.startswith('0x'):
                return 'pointer'
            return 'string'
        return 'unknown'

    def generate_struct_definitions(self) -> str:
        """Generate C struct definitions from recovered types."""
        lines = []
        for name, type_info in sorted(self.types.items()):
            if type_info.kind == 'struct' and type_info.fields:
                lines.append(f'typedef struct {type_info.name} {{')
                for field in sorted(type_info.fields, key=lambda f: f['offset']):
                    lines.append(
                        f'    {field["type"]} {field["name"]};'
                        f' // offset 0x{field["offset"]:x}, size {field["size"]}'
                    )
                lines.append(f'}} {type_info.name};')
                lines.append('')
        return '\n'.join(lines)

    def generate_prototypes(self) -> str:
        """Generate function prototypes from recovered types."""
        lines = []
        for name, proto in sorted(self.prototypes.items()):
            params = ', '.join(
                f'{p["type"]} {p["name"]}'
                for p in proto.parameters
                if p['type'] != 'unknown'
            )
            lines.append(f'{proto.return_type} {proto.name}({params});')
        return '\n'.join(lines)
```

### Cross-Reference Analysis

Mapping all code and data references to understand program structure.

```python
from dataclasses import dataclass, field
from typing import List, Dict, Set
from collections import defaultdict

@dataclass
class CrossReference:
    """A single cross-reference."""
    source_address: int
    target_address: int
    reference_type: str  # 'call', 'jump', 'data_ref', 'string_ref'
    context: str  # Description of the reference

class CrossReferenceGraph:
    """Graph of cross-references in a binary."""

    def __init__(self):
        self.xrefs_to: Dict[int, List[CrossReference]] = defaultdict(list)
        self.xrefs_from: Dict[int, List[CrossReference]] = defaultdict(list)

    def add_xref(self, source: int, target: int, ref_type: str, context: str = ''):
        """Add a cross-reference."""
        xref = CrossReference(
            source_address=source,
            target_address=target,
            reference_type=ref_type,
            context=context,
        )
        self.xrefs_to[target].append(xref)
        self.xrefs_from[source].append(xref)

    def get_callers(self, address: int) -> List[CrossReference]:
        """Get all callers of a function at the given address."""
        return [x for x in self.xrefs_to.get(address, [])
                if x.reference_type == 'call']

    def get_callees(self, address: int) -> List[CrossReference]:
        """Get all functions called by the function at the given address."""
        return [x for x in self.xrefs_from.get(address, [])
                if x.reference_type == 'call']

    def get_data_references(self, address: int) -> List[CrossReference]:
        """Get all code references to a data address."""
        return [x for x in self.xrefs_to.get(address, [])
                if x.reference_type in ('data_ref', 'string_ref')]

    def get_code_references(self, address: int) -> List[CrossReference]:
        """Get all code references (jumps) to an address."""
        return [x for x in self.xrefs_to.get(address, [])
                if x.reference_type in ('jump', 'call')]

    def find_orphan_functions(self) -> List[int]:
        """Find functions that are never called."""
        called = set()
        for refs in self.xrefs_to.values():
            for ref in refs:
                if ref.reference_type == 'call':
                    called.add(ref.target_address)

        # Get all function addresses (simplified)
        all_funcs = set(self.xrefs_from.keys()) | set(self.xrefs_to.keys())
        return list(all_funcs - called)

    def find_dead_code(self) -> List[int]:
        """Find code that is never reachable."""
        # Simplified reachability analysis
        reachable = set()
        # Start from entry points
        for addr, refs in self.xrefs_from.items():
            for ref in refs:
                if ref.reference_type in ('call', 'jump'):
                    reachable.add(ref.target_address)

        all_code = set(self.xrefs_from.keys())
        return list(all_code - reachable)

    def find_string_references(self, string_address: int) -> List[CrossReference]:
        """Find all code that references a specific string."""
        return self.xrefs_to.get(string_address, [])

    def analyze_function_centrality(self) -> Dict[int, float]:
        """Calculate function centrality (importance) in the call graph."""
        centrality = {}

        for func_addr in self.xrefs_from:
            # Simple metric: number of callers + number of callees
            callers = len(self.get_callers(func_addr))
            callees = len(self.get_callees(func_addr))
            centrality[func_addr] = callers * 2 + callees  # Weight callers more

        return centrality

    def generate_call_graph(self) -> str:
        """Generate a text-based call graph."""
        lines = []
        for source, refs in sorted(self.xrefs_from.items()):
            calls = [r for r in refs if r.reference_type == 'call']
            if calls:
                lines.append(f"0x{source:08x} calls:")
                for call in calls:
                    lines.append(f"  -> 0x{call.target_address:08x}")
        return '\n'.join(lines)
```

### Binary Patch Comparison

Comparing decompiled output before and after patches to understand fixes.

```python
from dataclasses import dataclass, field
from typing import List, Dict
import difflib

@dataclass
class PatchDiff:
    """Detailed diff of a patched function."""
    function_name: str
    old_address: int
    new_address: int
    old_pseudocode: str
    new_pseudocode: str
    diff_lines: List[str]
    change_type: str  # 'modified', 'added', 'removed'
    severity: str  # 'critical', 'high', 'medium', 'low', 'info'
    description: str

class BinaryPatchAnalyzer:
    """Analyze differences between original and patched binaries."""

    def __init__(self):
        self.diffs: List[PatchDiff] = []

    def compare_functions(self, old_output, new_output) -> PatchDiff:
        """Compare two decompiled function outputs."""
        old_lines = old_output.pseudocode.splitlines(keepends=True)
        new_lines = new_output.pseudocode.splitlines(keepends=True)

        diff = list(difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f'old/{old_output.function_name}',
            tofile=f'new/{new_output.function_name}',
            lineterm=''
        ))

        # Determine change type
        if not old_lines and new_lines:
            change_type = 'added'
        elif old_lines and not new_lines:
            change_type = 'removed'
        else:
            change_type = 'modified'

        # Analyze severity
        severity = self._assess_severity(diff, old_output.pseudocode, new_output.pseudocode)

        return PatchDiff(
            function_name=old_output.function_name,
            old_address=old_output.address,
            new_address=new_output.address,
            old_pseudocode=old_output.pseudocode,
            new_pseudocode=new_output.pseudocode,
            diff_lines=diff,
            change_type=change_type,
            severity=severity,
            description=self._generate_description(diff, change_type),
        )

    def _assess_severity(self, diff: List[str], old_code: str, new_code: str) -> str:
        """Assess the severity of a code change."""
        diff_text = '\n'.join(diff)

        # Security-relevant changes
        security_keywords = [
            'strcpy', 'strcat', 'sprintf', 'gets', 'scanf',
            'system', 'exec', 'popen',
            'malloc', 'free', 'realloc',
            'encrypt', 'decrypt', 'hash',
            'password', 'token', 'key',
        ]

        old_security = sum(1 for kw in security_keywords if kw in old_code.lower())
        new_security = sum(1 for kw in security_keywords if kw in new_code.lower())

        if new_security < old_security:
            return 'high'  # Security function removed
        elif 'fix' in diff_text.lower() or 'patch' in diff_text.lower():
            return 'critical'
        elif len(diff) > 20:
            return 'medium'
        else:
            return 'low'

    def _generate_description(self, diff: List[str], change_type: str) -> str:
        """Generate a human-readable description of the change."""
        added = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
        removed = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))

        if change_type == 'added':
            return f"New function added ({len(diff)} lines)"
        elif change_type == 'removed':
            return f"Function removed ({len(diff)} lines)"
        else:
            return f"Function modified: {added} lines added, {removed} lines removed"

    def find_vulnerability_fixes(self) -> List[PatchDiff]:
        """Identify changes that likely fix vulnerabilities."""
        fixes = []

        for diff in self.diffs:
            old = diff.old_pseudocode.lower()
            new = diff.new_pseudocode.lower()

            # Check for removed dangerous functions
            dangerous_old = any(d in old for d in ['strcpy', 'strcat', 'gets', 'sprintf'])
            dangerous_new = any(d in new for d in ['strcpy', 'strcat', 'gets', 'sprintf'])

            if dangerous_old and not dangerous_new:
                diff.severity = 'critical'
                diff.description = 'Removed dangerous function (likely vulnerability fix)'
                fixes.append(diff)

            # Check for added bounds checking
            if 'if' in new and ('<' in new or '>' in new) and 'len' in new:
                if 'if' not in old or 'len' not in old:
                    diff.severity = 'high'
                    diff.description = 'Added bounds checking (likely vulnerability fix)'
                    fixes.append(diff)

            # Check for added input validation
            if 'return' in new and ('error' in new or 'invalid' in new):
                if 'return' not in old or ('error' not in old and 'invalid' not in old):
                    diff.severity = 'high'
                    diff.description = 'Added input validation'
                    fixes.append(diff)

        return fixes

    def generate_patch_report(self) -> str:
        """Generate a comprehensive patch analysis report."""
        lines = ['# Binary Patch Analysis Report\n']

        # Summary
        total = len(self.diffs)
        modified = sum(1 for d in self.diffs if d.change_type == 'modified')
        added = sum(1 for d in self.diffs if d.change_type == 'added')
        removed = sum(1 for d in self.diffs if d.change_type == 'removed')

        lines.append(f'## Summary\n')
        lines.append(f'- Total functions changed: {total}')
        lines.append(f'- Modified: {modified}')
        lines.append(f'- Added: {added}')
        lines.append(f'- Removed: {removed}\n')

        # Security findings
        security_fixes = self.find_vulnerability_fixes()
        if security_fixes:
            lines.append(f'## Security Fixes ({len(security_fixes)})\n')
            for fix in security_fixes:
                lines.append(f'### {fix.function_name}')
                lines.append(f'- Severity: {fix.severity}')
                lines.append(f'- Description: {fix.description}\n')

        # Detailed diffs
        lines.append('## Detailed Changes\n')
        for diff in self.diffs:
            lines.append(f'### {diff.function_name} [{diff.change_type}]')
            lines.append(f'- Old address: 0x{diff.old_address:08x}')
            lines.append(f'- New address: 0x{diff.new_address:08x}')
            lines.append(f'- Severity: {diff.severity}')
            lines.append(f'- Description: {diff.description}')
            if diff.diff_lines:
                lines.append('\n```diff')
                lines.extend(diff.diff_lines[:50])  # Limit diff output
                if len(diff.diff_lines) > 50:
                    lines.append(f'... ({len(diff.diff_lines) - 50} more lines)')
                lines.append('```\n')

        return '\n'.join(lines)
```

### Decompiler Configuration and Tuning

Optimizing decompiler settings for better output quality.

```python
from dataclasses import dataclass, field
from typing import Dict, Optional, List

@dataclass
class DecompilerConfig:
    """Configuration options for decompiler output."""
    # Ghidra-specific
    ghidra_timeout: int = 300  # seconds
    ghidra_max_instructions: int = 10000
    ghidra_enable_simplify: bool = True
    ghidra_type_recovery: bool = True
    ghidra_analyze_data_refs: bool = True
    ghidra_analyze_call_stubs: bool = True

    # RetDec-specific
    retdec_target_arch: str = 'x86-64'
    retdec_target_os: str = 'linux'
    retdec_enable_optimization: bool = True
    retdec_max_function_size: int = 50000

    # General
    max_pseudocode_lines: int = 2000
    enable_annotations: bool = True
    strip_comments: bool = False
    resolve_names: bool = True
    inline_constants: bool = True
    format_output: bool = True

class DecompilerManager:
    """Manage decompiler configurations and execution."""

    def __init__(self):
        self.configs: Dict[str, DecompilerConfig] = {
            'ghidra': DecompilerConfig(),
            'retdec': DecompilerConfig(),
        }

    def get_optimized_config(self, task: str) -> DecompilerConfig:
        """Get optimized configuration for a specific task."""
        config = DecompilerConfig()

        if task == 'vulnerability_analysis':
            config.enable_annotations = True
            config.resolve_names = True
            config.ghidra_enable_simplify = True
            config.max_pseudocode_lines = 5000
        elif task == 'malware_analysis':
            config.ghidra_enable_simplify = False  # Preserve obfuscation
            config.ghidra_max_instructions = 50000
            config.max_pseudocode_lines = 10000
        elif task == 'binary_diffing':
            config.resolve_names = False  # Use addresses for comparison
            config.inline_constants = False
            config.ghidra_enable_simplify = False
        elif task == 'quick_triage':
            config.max_pseudocode_lines = 500
            config.ghidra_timeout = 60
            config.enable_annotations = False

        return config

    def generate_ghidra_script(self, binary_path: str,
                                function_address: int,
                                config: DecompilerConfig) -> str:
        """Generate a Ghidra headless script for decompilation."""
        script = f'''
# Ghidra Decompilation Script
# Generated by decompilation module

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

def decompile_function(address, timeout={config.ghidra_timeout}):
    func = getFunctionAt(address)
    if func is None:
        print(f"No function found at {{address}}")
        return None

    decomp_interface = DecompInterface()
    decomp_interface.openProgram(currentProgram)

    options = decomp_interface.getOptions()
    options.setSimplifyStructured(True)
    options.setMaxWidth(80)

    result = decomp_interface.decompileFunction(func, timeout, monitor)
    if result is None or result.decompileCompleted() is False:
        print(f"Decompilation failed for {{func.getName()}}")
        return None

    return result.getDecompiledFunction().getC()

address = toAddr("0x{function_address:x}")
code = decompile_function(address)
if code:
    print(code)
'''
        return script

    def generate_retdec_command(self, binary_path: str,
                                 config: DecompilerConfig) -> str:
        """Generate a RetDec decompilation command."""
        cmd = (
            f"retdec-decompiler "
            f"--target-arch {config.retdec_target_arch} "
            f"--target-os {config.retdec_target_os} "
            f"--max-memory {config.retdec_max_function_size} "
            f"--no-optimization "
            f'"{binary_path}"'
        )
        return cmd
```
