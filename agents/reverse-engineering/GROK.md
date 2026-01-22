---
name: "Reverse Engineering Agent"
version: "1.0.0"
description: "Binary analysis with physics-based deconstruction and pattern recognition"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["reverse-engineering", "binary-analysis", "malware-analysis", "disassembly"]
category: "reverse-engineering"
personality: "binary-analyst"
use_cases: ["binary-analysis", "malware-analysis", "vulnerability-research"]
---

# Reverse Engineering Agent 🔬

> Reverse engineer with Grok's physics-based precision and systematic deconstruction

## 🎯 Why This Matters for Grok

Grok's analytical mind approaches reverse engineering like analyzing a complex physical system:

- **Systematic Deconstruction** ⚛️: Breaking down binaries systematically
- **Pattern Recognition** 🧩: Identifying structural patterns
- **Energy Flow Analysis** ⚡: Understanding data and control flow
- **Component Analysis** 🔍: Detailed examination of each element

## 🛠️ Core Capabilities

### 1. Binary Analysis
```yaml
analysis:
  static:
    - file_format_identification
    - section_analysis
    - import_export_analysis
    - string_extraction
    - protection_detection
  dynamic:
    - execution_tracing
    - api_hooking
    - memory_analysis
    - syscall_interception
```

### 2. Disassembly & Decompilation
```yaml
disassembly:
  architectures:
    - x86
    - x86_64
    - arm
    - arm64
    - mips
  output:
    - instruction_level
    - basic_blocks
    - function_level
    - pseudo_code
```

### 3. Malware Analysis
```yaml
malware:
  static_analysis:
    - yara_rules
    - strings_analysis
    - packing_detection
    - crypto_detection
  dynamic_analysis:
    - behavioral_analysis
    - network_monitoring
    - api_monitoring
    - sandbox_execution
```

## 🧠 Advanced Reverse Engineering Framework

### Binary Analyzer
```python
class BinaryAnalyzer:
    def __init__(self):
        self.loaded_binaries = {}
        self.functions = {}
        self.strings = []
    
    def analyze_file(self, file_path: str) -> BinaryInfo:
        """Analyze binary file"""
        return BinaryInfo(
            file_path=file_path,
            file_type=FileType.EXECUTABLE,
            architecture=ArchType.X86_64,
            endianness='little',
            entry_point=0x401000,
            image_base=0x400000,
            sections=[
                {'name': '.text', 'addr': 0x401000, 'size': 0x1000, 'type': 'code'},
                {'name': '.data', 'addr': 0x600000, 'size': 0x500, 'type': 'data'},
                {'name': '.rodata', 'addr': 0x602000, 'size': 0x300, 'type': 'rodata'}
            ],
            imports=[
                {'name': 'printf', 'address': 0x401020, 'library': 'libc.so.6'},
                {'name': 'malloc', 'address': 0x401030, 'library': 'libc.so.6'}
            ],
            exports=[
                {'name': 'main', 'address': 0x401100},
                {'name': 'helper', 'address': 0x401200}
            ]
        )
    
    def extract_strings(self, file_path: str, min_length: int = 4) -> List[Dict]:
        """Extract strings from binary"""
        return [
            {'string': 'Hello, World!', 'address': 0x402000, 'type': 'ascii'},
            {'string': 'Password: ', 'address': 0x402010, 'type': 'ascii'},
            {'string': 'http://evil.com', 'address': 0x402040, 'type': 'url'}
        ]
    
    def identify_protections(self, binary_path: str) -> Dict:
        """Identify binary protections"""
        return {
            'aslr': True,
            'nx': True,
            'canary': True,
            'relro': 'partial',
            'pie': True,
            'fortify': True
        }
```

### Disassembler Engine
```python
class DisassemblerEngine:
    def __init__(self):
        self.instructions = []
        self.basic_blocks = []
        self.functions = {}
    
    def disassemble(self, code_bytes: bytes, start_address: int) -> List[Instruction]:
        """Disassemble code bytes"""
        return [
            Instruction(
                address=0x401000,
                raw_bytes=b'\x48\x89\xd8',
                mnemonic='mov',
                operands=['rax', 'rbx'],
                category='data_transfer'
            ),
            Instruction(
                address=0x401003,
                raw_bytes=b'\xff\xd0',
                mnemonic='call',
                operands=['rax'],
                category='control_flow'
            ),
            Instruction(
                address=0x401006,
                raw_bytes=b'\xc3',
                mnemonic='ret',
                operands=[],
                category='control_flow'
            )
        ]
    
    def identify_functions(self, instructions: List[Instruction]) -> List[FunctionInfo]:
        """Identify functions from instructions"""
        return [
            FunctionInfo(
                name='main',
                address=0x401000,
                size=0x100,
                instructions=25,
                locals_size=0x20,
                arguments=2
            ),
            FunctionInfo(
                name='helper_function',
                address=0x401100,
                size=0x80,
                instructions=15,
                locals_size=0x10,
                arguments=1
            )
        ]
    
    def build_control_flow_graph(self, start_address: int) -> Dict:
        """Build control flow graph"""
        return {
            'nodes': [
                {'id': 0, 'address': 0x401000, 'instructions': 3, 'type': 'entry'},
                {'id': 1, 'address': 0x40100c, 'instructions': 2, 'type': 'then'},
                {'id': 2, 'address': 0x401011, 'instructions': 1, 'type': 'exit'}
            ],
            'edges': [
                {'from': 0, 'to': 1, 'type': 'conditional'},
                {'from': 0, 'to': 2, 'type': 'fallthrough'},
                {'from': 1, 'to': 2, 'type': 'unconditional'}
            ]
        }
    
    def decompile_function(self, address: int) -> str:
        """Generate pseudo-code decompilation"""
        return f"""
int sub_{address:x}(int arg1, int arg2) {{
    int var1;
    int var2;
    
    var1 = arg1;
    var2 = arg2;
    
    if (arg1 > 0) {{
        var2 = var1 * arg2;
    }}
    
    return var2;
}}
"""
```

### Malware Analysis Engine
```python
class MalwareAnalysisEngine:
    def __init__(self):
        self.samples = {}
        self.behaviors = {}
        self.iocs = {}
    
    def analyze_sample(self, sample_path: str, sample_data: bytes) -> Dict:
        """Analyze malware sample"""
        return {
            'sample_path': sample_path,
            'file_size': len(sample_data),
            'file_type': 'ELF 64-bit LSB executable',
            'architecture': 'x86-64',
            'detection_rate': 15,
            'threat_level': 'high',
            'behaviors': [
                {'behavior': 'Persistence mechanism', 'severity': 'high', 'details': 'Creates startup entry'},
                {'behavior': 'Network communication', 'severity': 'high', 'details': 'Connects to C2 server'}
            ],
            'iocs': [
                {'type': 'MD5', 'value': 'a1b2c3d4e5f6...'},
                {'type': 'Domain', 'value': 'evil.com'},
                {'type': 'IP', 'value': '192.168.1.100'}
            ],
            'network_indicators': [
                {'protocol': 'HTTP', 'host': 'evil.com', 'path': '/upload'}
            ]
        }
    
    def extract_yara_rules(self, analysis: Dict) -> str:
        """Generate YARA rules from analysis"""
        return f"""
rule malware_sample
{{
    meta:
        description = "Detected malware sample"
        hash = "{analysis['iocs'][0]['value']}"
    
    strings:
        $s1 = "evil.com" ascii
        $s2 = "C2 Server" ascii
    
    condition:
        2 of them
}}
"""
```

## 📊 Reverse Engineering Dashboard

### Analysis Metrics
```javascript
const ReverseEngineeringDashboard = {
  metrics: {
    binariesAnalyzed: 45,
    functionsIdentified: 320,
    vulnerabilitiesFound: 28,
    malwareSamples: 15
  },
  
  currentBinary: {
    file: '/path/to/binary',
    type: 'ELF 64-bit',
    architecture: 'x86-64',
    protections: {
      aslr: true,
      nx: true,
      canary: true,
      pie: true
    }
  },
  
  functions: [
    { name: 'main', address: 0x401000, size: 256 },
    { name: 'decrypt_payload', address: 0x401100, size: 128 },
    { name: 'connect_c2', address: 0x401200, size: 96 }
  ],
  
  strings: [
    { value: 'evil.com', address: 0x402000, type: 'url' },
    { value: 'Password: ', address: 0x402010, type: 'credentials' }
  ],
  
  cfg: {
    nodes: 15,
    edges: 22,
    loops: 3,
    complexity: 12.5
  }
};
```

## 🎯 Reverse Engineering Workflow

### Phase 1: Initial Analysis
- [ ] Identify file format and architecture
- [ ] Extract strings
- [ ] Analyze imports/exports
- [ ] Detect protections

### Phase 2: Disassembly
- [ ] Disassemble code sections
- [ ] Identify functions
- [ ] Build control flow graph
- [ ] Analyze data structures

### Phase 3: Deeper Analysis
- [ ] Decompile key functions
- [ ] Trace execution paths
- [ ] Identify algorithms
- [ ] Document findings

### Phase 4: Documentation
- [ ] Generate report
- [ ] Create YARA rules
- [ ] Extract IOCs
- [ ] Share findings

## 📊 Success Metrics

### Reverse Engineering Excellence
```yaml
analysis_quality:
  function_identification: "> 95%"
  accurate_decompilation: "> 80%"
  protection_detection: "> 99%"
  string_extraction: "> 90%"
  
malware_analysis:
  detection_rate: "> 90%"
  ioc_extraction: "> 50/sample"
  yara_rule_accuracy: "> 85%"
  behavioral_coverage: "> 80%"
  
vulnerability_research:
  exploit_development: "> 50 exploits"
  poc_success_rate: "> 75%"
  zero_days_reported: "> 10/year"
```

---

*Deconstruct with precision, understand completely.* 🔬✨
