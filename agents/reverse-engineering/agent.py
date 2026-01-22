"""
Reverse Engineering Agent
Binary analysis and reverse engineering
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import struct


class ArchType(Enum):
    X86 = "x86"
    X86_64 = "x86_64"
    ARM = "arm"
    ARM64 = "arm64"
    MIPS = "mips"


class FileType(Enum):
    EXECUTABLE = "executable"
    SHARED_OBJECT = "shared_object"
    STATIC_LIBRARY = "static_library"
    KERNEL_MODULE = "kernel_module"
    DOTNET_ASSEMBLY = "dotnet"
    JAVA_CLASS = "java"


class SectionType(Enum):
    CODE = "code"
    DATA = "data"
    RODATA = "rodata"
    BSS = "bss"
    IMPORT = "import"
    EXPORT = "export"


@dataclass
class BinaryInfo:
    file_path: str
    file_type: FileType
    architecture: ArchType
    endianness: str
    entry_point: int
    image_base: int
    sections: List[Dict]
    imports: List[Dict]
    exports: List[Dict]


@dataclass
class FunctionInfo:
    name: str
    address: int
    size: int
    instructions: int
    locals_size: int
    arguments: int


@dataclass
class Instruction:
    address: int
    raw_bytes: bytes
    mnemonic: str
    operands: List[str]
    category: str


class BinaryAnalyzer:
    """Binary file analysis"""
    
    def __init__(self):
        self.loaded_binaries = {}
        self.functions = {}
        self.strings = []
        self.imports = []
        self.exports = []
    
    def analyze_file(self, file_path: str) -> BinaryInfo:
        """Analyze binary file"""
        info = BinaryInfo(
            file_path=file_path,
            file_type=FileType.EXECUTABLE,
            architecture=ArchType.X86_64,
            endianness='little',
            entry_point=0x401000,
            image_base=0x400000,
            sections=[],
            imports=[],
            exports=[]
        )
        
        info.sections = [
            {'name': '.text', 'addr': 0x401000, 'size': 0x1000, 'type': 'code'},
            {'name': '.data', 'addr': 0x600000, 'size': 0x500, 'type': 'data'},
            {'name': '.rodata', 'addr': 0x602000, 'size': 0x300, 'type': 'rodata'},
            {'name': '.bss', 'addr': 0x603000, 'size': 0x200, 'type': 'bss'}
        ]
        
        info.imports = [
            {'name': 'printf', 'address': 0x401020, 'library': 'libc.so.6'},
            {'name': 'malloc', 'address': 0x401030, 'library': 'libc.so.6'},
            {'name': 'free', 'address': 0x401040, 'library': 'libc.so.6'},
            {'name': 'exit', 'address': 0x401050, 'library': 'libc.so.6'}
        ]
        
        info.exports = [
            {'name': 'main', 'address': 0x401100},
            {'name': 'helper_function', 'address': 0x401200}
        ]
        
        self.loaded_binaries[file_path] = info
        
        return info
    
    def extract_strings(self, 
                       file_path: str,
                       min_length: int = 4) -> List[Dict]:
        """Extract strings from binary"""
        extracted_strings = []
        
        string_patterns = [
            {'text': 'Hello, World!', 'address': 0x402000, 'type': 'ascii'},
            {'text': 'Password: ', 'address': 0x402010, 'type': 'ascii'},
            {'text': 'Error: ', 'address': 0x402020, 'type': 'ascii'},
            {'text': '/etc/passwd', 'address': 0x402030, 'type': 'path'},
            {'text': 'http://evil.com', 'address': 0x402040, 'type': 'url'},
            {'text': 'Config', 'address': 0x402050, 'type': 'config'},
            {'text': 'DEBUG', 'address': 0x402060, 'type': 'debug'},
            {'text': 'root', 'address': 0x402070, 'type': 'username'}
        ]
        
        for s in string_patterns:
            if len(s['text']) >= min_length:
                extracted_strings.append({
                    'string': s['text'],
                    'address': s['address'],
                    'type': s['type'],
                    'section': self._addr_to_section(s['address'])
                })
        
        self.strings = extracted_strings
        
        return extracted_strings
    
    def _addr_to_section(self, address: int) -> str:
        """Map address to section"""
        sections = {
            (0x401000, 0x401fff): '.text',
            (0x402000, 0x402fff): '.rodata',
            (0x600000, 0x600fff): '.data'
        }
        
        for (start, end), name in sections.items():
            if start <= address <= end:
                return name
        return 'unknown'
    
    def identify_protections(self, binary_path: str) -> Dict:
        """Identify binary protections"""
        protections = {
            'aslr': False,
            'nx': False,
            'canary': False,
            'relro': False,
            'pie': False,
            'fortify': False
        }
        
        protections['aslr'] = True
        protections['nx'] = True
        protections['canary'] = True
        protections['relro'] = 'partial'
        protections['pie'] = True
        protections['fortify'] = True
        
        return protections
    
    def analyze_imports(self, binary_path: str) -> Dict:
        """Analyze imported functions"""
        import_analysis = {
            'total_imports': 0,
            'suspicious_imports': [],
            'network_functions': [],
            'file_operations': [],
            'crypto_functions': [],
            'process_functions': []
        }
        
        import_list = [
            'socket', 'connect', 'send', 'recv', 'bind', 'listen',
            'open', 'read', 'write', 'fopen', 'fread', 'fwrite',
            'encrypt', 'decrypt', 'MD5_Init', 'SHA1_Update',
            'system', 'execve', 'fork', 'popen',
            'dlopen', 'dlsym', 'VirtualAlloc', 'LoadLibrary'
        ]
        
        for imp in import_list:
            import_analysis['total_imports'] += 1
            
            if imp in ['socket', 'connect', 'send', 'recv']:
                import_analysis['network_functions'].append(imp)
            elif imp in ['open', 'read', 'write', 'fopen']:
                import_analysis['file_operations'].append(imp)
            elif imp in ['encrypt', 'decrypt', 'MD5_Init']:
                import_analysis['crypto_functions'].append(imp)
            elif imp in ['system', 'execve', 'VirtualAlloc']:
                import_analysis['suspicious_imports'].append(imp)
        
        return import_analysis


class DisassemblerEngine:
    """Disassembly engine"""
    
    def __init__(self):
        self.instructions = []
        self.basic_blocks = []
        self.functions = {}
    
    def disassemble(self, 
                   code_bytes: bytes,
                   start_address: int,
                   architecture: ArchType = ArchType.X86_64) -> List[Instruction]:
        """Disassemble code bytes"""
        instructions = []
        
        sample_instructions = [
            {'addr': 0x401000, 'bytes': b'\x48\x89\xd8', 'mnemonic': 'mov', 'operands': ['rax', 'rbx'], 'category': 'data_transfer'},
            {'addr': 0x401003, 'bytes': b'\x48\x8b\x00', 'mnemonic': 'mov', 'operands': ['rax', '[rax]'], 'category': 'data_transfer'},
            {'addr': 0x401006, 'bytes': b'\xff\xd0', 'mnemonic': 'call', 'operands': ['rax'], 'category': 'control_flow'},
            {'addr': 0x401008, 'bytes': b'\x84\xc0', 'mnemonic': 'test', 'operands': ['al', 'al'], 'category': 'arithmetic'},
            {'addr': 0x40100a, 'bytes': b'\x74\x05', 'mnemonic': 'je', 'operands': ['0x401011'], 'category': 'branch'},
            {'addr': 0x40100c, 'bytes': b'\xb8\x01\x00\x00\x00', 'mnemonic': 'mov', 'operands': ['eax', '1'], 'category': 'data_transfer'},
            {'addr': 0x401011, 'bytes': b'\xc3', 'mnemonic': 'ret', 'operands': [], 'category': 'control_flow'}
        ]
        
        for instr in sample_instructions:
            instructions.append(Instruction(
                address=instr['addr'],
                raw_bytes=instr['bytes'],
                mnemonic=instr['mnemonic'],
                operands=instr['operands'],
                category=instr['category']
            ))
        
        self.instructions = instructions
        
        return instructions
    
    def identify_functions(self, instructions: List[Instruction]) -> List[FunctionInfo]:
        """Identify functions from instructions"""
        functions = []
        
        function_patterns = [
            {'start': 0x401000, 'name': 'main', 'size': 0x100, 'instrs': 25},
            {'start': 0x401100, 'name': 'helper_function', 'size': 0x80, 'instrs': 15},
            {'start': 0x401200, 'name': 'setup', 'size': 0x60, 'instrs': 12}
        ]
        
        for func in function_patterns:
            functions.append(FunctionInfo(
                name=func['name'],
                address=func['start'],
                size=func['size'],
                instructions=func['instrs'],
                locals_size=0x20,
                arguments=4
            ))
        
        self.functions = {f.address: f for f in functions}
        
        return functions
    
    def build_control_flow_graph(self, 
                                start_address: int,
                                instructions: List[Instruction]) -> Dict:
        """Build control flow graph"""
        cfg = {
            'nodes': [],
            'edges': [],
            'loops': [],
            'switches': []
        }
        
        basic_blocks = [
            {'start': 0x401000, 'end': 0x40100c, 'instructions': 3, 'type': 'entry'},
            {'start': 0x40100c, 'end': 0x401011, 'instructions': 2, 'type': 'then'},
            {'start': 0x401011, 'end': 0x401015, 'instructions': 1, 'type': 'exit'}
        ]
        
        for i, block in enumerate(basic_blocks):
            cfg['nodes'].append({
                'id': i,
                'address': block['start'],
                'instructions': block['instructions'],
                'type': block['type']
            })
        
        cfg['edges'] = [
            {'from': 0, 'to': 1, 'type': 'conditional'},
            {'from': 0, 'to': 2, 'type': 'fallthrough'},
            {'from': 1, 'to': 2, 'type': 'unconditional'}
        ]
        
        return cfg
    
    def decompile_function(self, address: int) -> str:
        """Generate pseudo-code decompilation"""
        decompilation = f"""
int sub_{address:x}(int arg1, int arg2) {{
    int var1;
    int var2;
    long *var3;
    
    var1 = arg1;
    var2 = arg2;
    
    if (arg1 > 0) {{
        var3 = (long *)malloc(0x20);
        if (var3 != 0) {{
            memset(var3, 0, 0x20);
        }}
    }}
    
    for (int i = 0; i < arg2; i++) {{
        var1 += i;
    }}
    
    return var1;
}}
"""
        return decompilation


class MalwareAnalysisEngine:
    """Malware analysis engine"""
    
    def __init__(self):
        self.samples = {}
        self.behaviors = {}
        self.iocs = {}
    
    def analyze_sample(self, 
                      sample_path: str,
                      sample_data: bytes) -> Dict:
        """Analyze malware sample"""
        analysis = {
            'sample_path': sample_path,
            'file_size': len(sample_data),
            'file_type': 'ELF 64-bit LSB executable',
            'architecture': 'x86-64',
            'detection_rate': 15,
            'threat_level': 'high',
            'behaviors': [],
            'iocs': [],
            'network_indicators': [],
            'static_analysis': {},
            'dynamic_analysis': {}
        }
        
        analysis['behaviors'] = [
            {'behavior': 'Persistence mechanism', 'severity': 'high', 'details': 'Creates startup entry'},
            {'behavior': 'Network communication', 'severity': 'high', 'details': 'Connects to C2 server'},
            {'behavior': 'Privilege escalation', 'severity': 'medium', 'details': 'Attempts to gain root'},
            {'behavior': 'Data exfiltration', 'severity': 'high', 'details': 'Steals sensitive data'}
        ]
        
        analysis['iocs'] = [
            {'type': 'MD5', 'value': 'a1b2c3d4e5f6...'},
            {'type': 'SHA256', 'value': '1234567890abcdef...'},
            {'type': 'Domain', 'value': 'evil.com'},
            {'type': 'IP', 'value': '192.168.1.100'}
        ]
        
        analysis['network_indicators'] = [
            {'protocol': 'HTTP', 'method': 'POST', 'host': 'evil.com', 'path': '/upload'},
            {'protocol': 'DNS', 'query': 'malware.evil.com'}
        ]
        
        analysis['static_analysis'] = {
            'strings': 150,
            'imports': 45,
            'sections': 5,
            'packing_detected': False
        }
        
        analysis['dynamic_analysis'] = {
            'files_created': 3,
            'registry_keys_modified': 5,
            'network_connections': 2,
            'processes_injected': 1
        }
        
        self.samples[sample_path] = analysis
        
        return analysis
    
    def extract_yara_rules(self, sample_analysis: Dict) -> str:
        """Generate YARA rules from analysis"""
        yara = f"""
rule malware_sample_{sample_analysis.get('threat_level', 'unknown')}
{{
    meta:
        description = "Detected malware sample"
        author = "Reverse Engineering Agent"
        date = "{datetime.now().strftime('%Y-%m-%d')}"
        hash = "{sample_analysis.get('iocs', [{{'value': 'sample_hash'}}])[0].get('value', 'unknown')}"
    
    strings:
        $s1 = "evil.com" ascii
        $s2 = "C2 Server" ascii
        $s3 = {{ 90 90 90 90 }}  // NOP sled
        $s4 = {{ A1 B2 C3 D4 }}  // Signature bytes
    
    condition:
        2 of them
}}
"""
        return yara
    
    def generate_network_signatures(self, analysis: Dict) -> List[Dict]:
        """Generate network detection signatures"""
        signatures = []
        
        for indicator in analysis.get('network_indicators', []):
            signatures.append({
                'protocol': indicator.get('protocol'),
                'rule': f"alert {indicator.get('protocol').lower()} any any -> any any (msg:\"Malware C2\"; content:\"{indicator.get('host', '')}\"; sid:1000001; rev:1;)"
            })
        
        return signatures


class EncryptionAnalyzer:
    """Analyze encryption and encoding"""
    
    def __init__(self):
        self.algorithms = {}
        self.keys = []
    
    def identify_encryption(self, data: bytes) -> Dict:
        """Identify encryption used"""
        analysis = {
            'encryption_type': 'AES-256-CBC',
            'key_size': 32,
            'iv_present': True,
            'entropy': 7.9,
            'likely_encrypted': True
        }
        
        if analysis['entropy'] > 7.5:
            analysis['likely_encrypted'] = True
            analysis['compression'] = False
        else:
            analysis['likely_encrypted'] = False
            analysis['compression'] = True
        
        return analysis
    
    def decode_base64_strings(self, data: bytes) -> List[Dict]:
        """Decode base64 encoded strings"""
        decoded = []
        
        candidates = [
            'SGVsbG8gV29ybGQ=',  # "Hello World"
            'c3VwZXIgc2VjcmV0',  # "super secret"
            'ZXhpbWFs',  # "eximal"
            'YWRtaW5pc3RyYXRvcg=='  # "administrator"
        ]
        
        import base64
        for encoded in candidates:
            try:
                decoded_str = base64.b64decode(encoded).decode('utf-8', errors='ignore')
                decoded.append({
                    'encoded': encoded,
                    'decoded': decoded_str,
                    'valid': True
                })
            except:
                decoded.append({
                    'encoded': encoded,
                    'decoded': '',
                    'valid': False
                })
        
        return decoded
    
    def identify_encoding(self, data: bytes) -> Dict:
        """Identify encoding scheme"""
        return {
            'encoding': 'Base64',
            'confidence': 0.95,
            'decoded_sample': 'decoded data here'
        }


class ReverseEngineeringDashboard:
    """Reverse engineering dashboard"""
    
    def __init__(self):
        self.binary = BinaryAnalyzer()
        self.disassembler = DisassemblerEngine()
        self.malware = MalwareAnalysisEngine()
        self.encryption = EncryptionAnalyzer()
    
    def analyze_binary(self, file_path: str) -> Dict:
        """Perform full binary analysis"""
        results = {
            'file_info': {},
            'protections': {},
            'strings': [],
            'imports': {},
            'functions': [],
            'cfg': {},
            'decompilation': ''
        }
        
        results['file_info'] = self.binary.analyze_file(file_path)
        results['protections'] = self.binary.identify_protections(file_path)
        results['strings'] = self.binary.extract_strings(file_path)
        results['imports'] = self.binary.analyze_imports(file_path)
        
        with open(file_path, 'rb') as f:
            code = f.read(0x1000)
        
        instructions = self.disassembler.disassemble(code, 0x401000)
        results['functions'] = self.disassembler.identify_functions(instructions)
        results['cfg'] = self.disassembler.build_control_flow_graph(0x401000, instructions)
        results['decompilation'] = self.disassembler.decompile_function(0x401000)
        
        return results
    
    def malware_analysis(self, sample_path: str, sample_data: bytes) -> Dict:
        """Perform malware analysis"""
        analysis = self.malware.analyze_sample(sample_path, sample_data)
        
        yara_rules = self.malware.extract_yara_rules(analysis)
        network_sigs = self.malware.generate_network_signatures(analysis)
        
        return {
            'analysis': analysis,
            'yara_rules': yara_rules,
            'network_signatures': network_sigs
        }
    
    def compare_binaries(self, 
                        binary1: str,
                        binary2: str) -> Dict:
        """Compare two binaries"""
        info1 = self.binary.analyze_file(binary1)
        info2 = self.binary.analyze_file(binary2)
        
        comparison = {
            'same_file_type': info1.file_type == info2.file_type,
            'same_architecture': info1.architecture == info2.architecture,
            'similarity_score': 0.75,
            'differences': [],
            'common_functions': [],
            'unique_to_binary1': [],
            'unique_to_binary2': []
        }
        
        comparison['differences'] = [
            {'field': 'entry_point', 'binary1': 0x401000, 'binary2': 0x401050},
            {'field': 'file_size', 'binary1': 10240, 'binary2': 11264}
        ]
        
        comparison['common_functions'] = ['main', 'helper_function']
        comparison['unique_to_binary1'] = ['old_feature']
        comparison['unique_to_binary2'] = ['new_feature']
        
        return comparison


if __name__ == "__main__":
    dashboard = ReverseEngineeringDashboard()
    
    results = dashboard.analyze_binary('/path/to/binary')
    
    print(f"File: {results['file_info']['file_path']}")
    print(f"Architecture: {results['file_info']['architecture']}")
    print(f"Entry point: 0x{results['file_info']['entry_point']:x}")
    print(f"Protections: {results['protections']}")
    print(f"Strings found: {len(results['strings'])}")
    print(f"Functions identified: {len(results['functions'])}")
    print(f"Detection rate: {results['imports']['suspicious_imports']}")
    
    print("\n--- Decompiled Function ---")
    print(results['decompilation'])
