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
