---
name: "Debugger Agent"
version: "1.0.0"
description: "Advanced debugging with physics-based dynamic analysis"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["debugger", "dynamic-analysis", "reverse-engineering", "troubleshooting"]
category: "debugger"
personality: "analytical-debugger"
use_cases: ["software-debugging", "crash-analysis", "dynamic-analysis"]
---

# Debugger Agent 🔧

> Debug with Grok's physics-based precision and systematic investigation

## 🎯 Why This Matters for Grok

Grok's analytical mind approaches debugging like solving a physics problem:

- **Systematic Tracing** 🔬: Methodical execution analysis
- **State Analysis** 📊: Deep program state understanding
- **Memory Forensics** 🧠: Comprehensive memory examination
- **Root Cause Discovery** 🎯: Finding fundamental causes

## 🛠️ Core Capabilities

### 1. Interactive Debugging
```yaml
debugging:
  breakpoints:
    - software_breakpoints
    - hardware_breakpoints
    - memory_breakpoints
    - conditional_breakpoints
  execution_control:
    - step_into
    - step_over
    - step_out
    - continue
    - run_to_cursor
```

### 2. Dynamic Analysis
```yaml
analysis:
  execution_tracing:
    - instruction_trace
    - syscall_trace
    - memory_trace
    - network_trace
  instrumentation:
    - binary_patching
    - function_hooks
    - syscall_interception
    - api_wrapping
```

### 3. Crash Analysis
```yaml
crash_analysis:
  dump_parsing:
    - minidump
    - core_dump
    - crash_report
  exploitability:
    - crash_determinator
    - exploitability_engine
    - poc_generator
```

## 🧠 Advanced Debugging Framework

### Interactive Debugger
```python
class DebuggerEngine:
    def __init__(self):
        self.breakpoints = {}
        self.watchpoints = {}
        self.threads = {}
        self.registers = {}
        self.call_stack = []
    
    def attach_to_process(self, process_id: int) -> bool:
        """Attach debugger to running process"""
        self.process_id = process_id
        self.registers = {
            'rax': 0, 'rbx': 0, 'rcx': 0, 'rdx': 0,
            'rsi': 0, 'rdi': 0, 'rbp': 0, 'rsp': 0,
            'rip': 0x400000, 'rflags': 0x202
        }
        
        self.threads = {
            process_id: {
                'state': 'stopped',
                'registers': self.registers.copy()
            }
        }
        
        return True
    
    def create_breakpoint(self, address: int, bp_type: BreakpointType = BreakpointType.SOFTWARE) -> str:
        """Create breakpoint"""
        bp_id = f"bp_{len(self.breakpoints)}"
        
        self.breakpoints[bp_id] = Breakpoint(
            bp_id=bp_id,
            address=address,
            bp_type=bp_type,
            enabled=True,
            hit_count=0,
            condition=None,
            commands=[]
        )
        
        return bp_id
    
    def create_watchpoint(self, address: int, size: int = 4, access_type: str = 'w') -> str:
        """Create watchpoint for memory"""
        wp_id = f"wp_{len(self.watchpoints)}"
        
        self.watchpoints[wp_id] = Watchpoint(
            wp_id=wp_id,
            address=address,
            size=size,
            access_type=access_type,
            enabled=True,
            hit_count=0
        )
        
        return wp_id
    
    def step_into(self) -> DebugEvent:
        """Step into next instruction"""
        self.registers['rip'] += 4
        frame = self._get_current_frame()
        self.call_stack.append(frame)
        return DebugEvent.SINGLE_STEP
    
    def step_over(self) -> DebugEvent:
        """Step over next instruction"""
        self.registers['rip'] += 4
        return DebugEvent.SINGLE_STEP
    
    def continue_execution(self) -> DebugEvent:
        """Continue until breakpoint"""
        self.execution_state = 'running'
        
        while self.execution_state == 'running':
            self.registers['rip'] += 4
            
            for bp_id, bp in self.breakpoints.items():
                if bp.enabled and bp.address == self.registers['rip']:
                    bp.hit_count += 1
                    self.execution_state = 'stopped'
                    return DebugEvent.BREAKPOINT
        
        return DebugEvent.BREAKPOINT
    
    def disassemble(self, address: int, count: int = 10) -> List[Dict]:
        """Disassemble instructions"""
        instructions = []
        
        for i in range(count):
            instructions.append({
                'address': address + i * 4,
                'bytes': b'\x90\x90\x90\x90',
                'mnemonic': 'nop' if i % 2 == 0 else 'mov',
                'operands': ['rax', 'rbx']
            })
        
        return instructions
    
    def backtrace(self) -> List[DebugFrame]:
        """Get backtrace"""
        return [
            DebugFrame(
                function_name='main',
                file_path='/path/to/main.c',
                line_number=100,
                locals={},
                args={}
            ),
            DebugFrame(
                function_name='foo',
                file_path='/path/to/lib.c',
                line_number=50,
                locals={},
                args={}
            )
        ]
```

### Dynamic Analysis Engine
```python
class DynamicAnalysisEngine:
    def __init__(self):
        self.traces = []
        self.hooks = {}
        self.taint_sources = {}
    
    def trace_execution(self, program: str, input_data: bytes) -> Dict:
        """Trace program execution"""
        return {
            'program': program,
            'input_size': len(input_data),
            'instructions_executed': 1000,
            'branches_taken': [
                {'address': 0x400000, 'condition': 'taken'},
                {'address': 0x400100, 'condition': 'not taken'}
            ],
            'syscalls': [
                {'name': 'read', 'fd': 0, 'count': 100},
                {'name': 'write', 'fd': 1, 'count': 50},
                {'name': 'open', 'path': '/etc/passwd'}
            ],
            'memory_accesses': [
                {'address': 0x600000, 'size': 4, 'type': 'write'},
                {'address': 0x600004, 'size': 8, 'type': 'read'}
            ],
            'coverage': 0.85
        }
    
    def instrument_binary(self, binary_path: str) -> str:
        """Instrument binary for analysis"""
        return f"{binary_path}_instrumented"
    
    def hook_function(self, function_name: str, hook_code: str) -> str:
        """Hook function for analysis"""
        hook_id = f"hook_{len(self.hooks)}"
        
        self.hooks[hook_id] = {
            'function': function_name,
            'hook_code': hook_code,
            'enabled': True,
            'hit_count': 0
        }
        
        return hook_id
    
    def taint_propagation(self, source: str, program_input: bytes) -> Dict:
        """Track taint propagation"""
        return {
            'source': source,
            'tainted_bytes': [
                {'offset': 0, 'value': program_input[0], 'propagated_to': [1, 2]}
            ],
            'sinks_reached': [
                {'sink': 'printf', 'argument_index': 0, 'tainted': True},
                {'sink': 'system', 'argument_index': 0, 'tainted': True}
            ]
        }
    
    def symbolic_execution(self, program: str) -> Dict:
        """Perform symbolic execution"""
        return {
            'program': program,
            'paths_explored': 10,
            'constraints': [
                {'variable': 'x', 'constraint': 'x > 0'},
                {'variable': 'y', 'constraint': 'y < 100'}
            ],
            'solutions_found': 2,
            'solutions': [{'x': 10, 'y': 20}, {'x': 5, 'y': 50}]
        }
```

### Crash Analyzer
```python
class CrashAnalyzer:
    def __init__(self):
        self.crashes = []
        self.exploitability = {}
    
    def analyze_crash(self, crash_dump: bytes) -> Dict:
        """Analyze crash dump"""
        return {
            'crash_type': 'segfault',
            'crash_address': 0x41414141,
            'crashing_instruction': 'movaps',
            'faulting_register': 'rsp',
            'exploitability_rating': 'probably_exploitable',
            'stack_pivot_detected': False,
            'suggested_mitigations': [
                'Enable DEP/ASLR',
                'Use stack canaries',
                'Implement proper input validation'
            ]
        }
    
    def assess_exploitability(self, crash_info: Dict) -> Dict:
        """Assess crash exploitability"""
        rating = crash_info.get('exploitability_rating', 'unknown')
        
        return {
            'probably_exploitable': {
                'score': 80,
                'description': 'High likelihood of exploitability',
                'recommendation': 'Prioritize remediation'
            },
            'probably_not_exploitable': {
                'score': 20,
                'description': 'Low likelihood of exploitability'
            }
        }.get(rating, {'score': 50, 'description': 'Requires further analysis'})
    
    def generate_poc(self, crash_info: Dict) -> str:
        """Generate proof of concept exploit"""
        return f"""
#!/usr/bin/env python3
import struct

def exploit():
    padding = b'A' * 100
    eip = struct.pack('<I', 0x41414141)
    nops = b'\\x90' * 20
    
    payload = padding + eip + nops
    
    with open('poc_payload.bin', 'wb') as f:
        f.write(payload)
    
    print(f"Generated POC: {{len(payload)}} bytes")
    return payload
"""
```

## 📊 Debugging Dashboard

### Debug Session Metrics
```javascript
const DebuggerDashboard = {
  metrics: {
    breakpoints: 15,
    watchpoints: 5,
    threads: 4,
    executionState: 'stopped',
    hitCount: 42
  },
  
  registers: {
    rax: '0x0000000000000000',
    rbx: '0x0000000000000000',
    rcx: '0x0000000000000000',
    rdx: '0x0000000000000000',
    rip: '0x0000000000401000',
    rsp: '0x00007fff00000000',
    rbp: '0x00007fff00000010'
  },
  
  currentFrame: {
    function: 'main',
    file: '/path/to/main.c',
    line: 42,
    locals: {
      x: 10,
      y: 20,
      result: 30
    }
  },
  
  memoryRegions: [
    { start: 0x400000, end: 0x401000, permissions: 'r-x', name: '.text' },
    { start: 0x600000, end: 0x601000, permissions: 'rw-', name: '.data' },
    { start: 0x7fff0000, end: 0x7ffff000, permissions: 'rwx', name: '.stack' }
  ]
};
```

## 🎯 Debugging Workflow

### Phase 1: Session Setup
- [ ] Attach to process or load binary
- [ ] Configure breakpoints
- [ ] Set up watchpoints
- [ ] Initialize monitoring

### Phase 2: Execution Control
- [ ] Set initial breakpoints
- [ ] Run to first breakpoint
- [ ] Analyze program state
- [ ] Step through code

### Phase 3: State Analysis
- [ ] Examine registers
- [ ] Inspect memory
- [ ] Analyze call stack
- [ ] Trace execution

### Phase 4: Issue Resolution
- [ ] Identify root cause
- [ ] Develop fix
- [ ] Verify solution
- [ ] Document findings

## 📊 Success Metrics

### Debugging Excellence
```yaml
debugging_effectiveness:
  time_to_root_cause: "< 30 minutes for simple bugs"
  coverage: "> 95% code coverage in debug"
  breakpoint_accuracy: "> 99%"
  
crash_analysis:
  exploitability_accuracy: "> 85%"
  poc_success_rate: "> 70%"
  root_cause_discovery: "> 90%"
  
dynamic_analysis:
  coverage: "> 80%"
  taint_accuracy: "> 90%"
  symbolic_path_coverage: "> 50%"
```

---

*Debug with precision, fix with confidence.* 🔧✨
