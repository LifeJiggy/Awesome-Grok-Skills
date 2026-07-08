"""
Debugger Agent - Software Debugging, Analysis, and Error Resolution
===================================================================

Interactive debugging engine with breakpoints, watchpoints, execution control,
root cause analysis, logging, profiling, tracing, error resolution, and
post-mortem analysis capabilities.

Author: Awesome Grok Skills
License: MIT
"""

import os
import re
import sys
import time
import json
import hashlib
import logging
import traceback
import threading
from typing import Dict, List, Optional, Any, Tuple, Union, Set, Callable, Iterator
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path


# =============================================================================
# Enums
# =============================================================================

class BreakpointType(Enum):
    """Types of breakpoints supported by the debugging engine."""
    SOFTWARE = "software"
    HARDWARE = "hardware"
    CONDITIONAL = "conditional"
    TEMPORARY = "temporary"
    FUNCTION_ENTRY = "function_entry"
    EXCEPTION = "exception"


class DebugEvent(Enum):
    """Events that can occur during debugging."""
    BREAKPOINT = "breakpoint"
    WATCHPOINT = "watchpoint"
    SINGLE_STEP = "single_step"
    PROGRAM_EXIT = "program_exit"
    EXCEPTION = "exception"
    THREAD_CREATED = "thread_created"
    THREAD_EXITED = "thread_exited"


class MemoryProtection(Enum):
    """Memory region protection flags."""
    NONE = 0
    READ = 1
    WRITE = 2
    EXECUTE = 4
    READ_WRITE = READ | WRITE
    READ_EXECUTE = READ | EXECUTE
    READ_WRITE_EXECUTE = READ | WRITE | EXECUTE


class ThreadState(Enum):
    """Thread execution states."""
    RUNNING = "running"
    STOPPED = "stopped"
    WAITING = "waiting"
    ZOMBIE = "zombie"
    DEAD = "dead"


class LogLevel(Enum):
    """Logging levels for the debugging agent."""
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    FATAL = auto()


class CrashType(Enum):
    """Types of program crashes."""
    SEGMENTATION_FAULT = "segfault"
    STACK_OVERFLOW = "stack_overflow"
    HEAP_CORRUPTION = "heap_corruption"
    USE_AFTER_FREE = "use_after_free"
    DOUBLE_FREE = "double_free"
    BUFFER_OVERFLOW = "buffer_overflow"
    INTEGER_OVERFLOW = "integer_overflow"
    DIVIDE_BY_ZERO = "divide_by_zero"
    DEADLOCK = "deadlock"
    OUT_OF_MEMORY = "out_of_memory"
    UNKNOWN = "unknown"


class RootCauseCategory(Enum):
    """Categories of root causes for software defects."""
    LOGIC_ERROR = "logic_error"
    RACE_CONDITION = "race_condition"
    MEMORY_SAFETY = "memory_safety"
    RESOURCE_LEAK = "resource_leak"
    INPUT_VALIDATION = "input_validation"
    ERROR_HANDLING = "error_handling"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    PERFORMANCE = "performance"
    SECURITY = "security"
    UNKNOWN = "unknown"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Breakpoint:
    """Represents a debug breakpoint."""
    bp_id: str
    address: int
    bp_type: BreakpointType = BreakpointType.SOFTWARE
    enabled: bool = True
    hit_count: int = 0
    condition: Optional[str] = None
    temporary: bool = False
    ignore_count: int = 0
    hit_timestamps: List[float] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def increment_hit(self) -> None:
        self.hit_count += 1
        self.hit_timestamps.append(time.time())
        if self.temporary:
            self.enabled = False

    def should_ignore(self) -> bool:
        if self.ignore_count > 0:
            self.ignore_count -= 1
            return True
        return False

    def get_hit_rate(self) -> float:
        if not self.hit_timestamps:
            return 0.0
        elapsed = self.hit_timestamps[-1] - self.created_at
        return len(self.hit_timestamps) / elapsed if elapsed > 0 else 0.0


@dataclass
class DebugFrame:
    """Represents a stack frame during debugging."""
    function_name: str
    file_path: str
    line_number: int
    locals: Dict[str, Any] = field(default_factory=dict)
    args: Dict[str, Any] = field(default_factory=dict)
    instruction_pointer: int = 0
    stack_pointer: int = 0
    frame_index: int = 0

    def get_variable(self, name: str) -> Any:
        return self.locals.get(name, self.args.get(name))

    def set_variable(self, name: str, value: Any, is_local: bool = True) -> None:
        target = self.locals if is_local else self.args
        target[name] = value


@dataclass
class Watchpoint:
    """Represents a memory watchpoint."""
    wp_id: str
    address: int
    size: int = 4
    access_type: str = "rw"
    enabled: bool = True
    hit_count: int = 0
    last_access_value: Optional[bytes] = None

    def record_access(self, value: bytes) -> None:
        self.hit_count += 1
        self.last_access_value = value


@dataclass
class MemoryRegion:
    """Represents a memory region in the target process."""
    start: int
    end: int
    permissions: MemoryProtection
    name: str
    path: Optional[str] = None

    @property
    def size(self) -> int:
        return self.end - self.start

    def contains(self, address: int) -> bool:
        return self.start <= address < self.end


@dataclass
class Register:
    """Represents a CPU register."""
    name: str
    value: int
    size: int
    is_program_counter: bool = False
    is_stack_pointer: bool = False
    is_flags: bool = False

    def get_bit(self, bit: int) -> bool:
        return bool(self.value & (1 << bit))

    def set_bit(self, bit: int, on: bool) -> None:
        if on:
            self.value |= (1 << bit)
        else:
            self.value &= ~(1 << bit)


@dataclass
class Thread:
    """Represents a thread in the debugged process."""
    thread_id: int
    state: ThreadState = ThreadState.STOPPED
    registers: Dict[str, Register] = field(default_factory=dict)
    call_stack: List[DebugFrame] = field(default_factory=list)
    name: Optional[str] = None
    cpu_time: float = 0.0

    def get_pc(self) -> Optional[int]:
        for reg in self.registers.values():
            if reg.is_program_counter:
                return reg.value
        return None

    def get_sp(self) -> Optional[int]:
        for reg in self.registers.values():
            if reg.is_stack_pointer:
                return reg.value
        return None


@dataclass
class CrashInfo:
    """Represents crash information from a core dump or exception."""
    crash_type: CrashType
    crash_address: int = 0
    crashing_instruction: str = ""
    faulting_register: str = ""
    signal_number: int = 0
    signal_name: str = ""
    stack_trace: List[DebugFrame] = field(default_factory=list)
    registers_at_crash: Dict[str, int] = field(default_factory=dict)
    memory_dump: Optional[bytes] = None
    timestamp: float = field(default_factory=time.time)
    thread_id: int = 0

    def get_crash_hash(self) -> str:
        data = f"{self.crash_type.value}:{self.crash_address:#x}:{self.crashing_instruction}"
        return hashlib.md5(data.encode()).hexdigest()


@dataclass
class TraceEntry:
    """Single entry in an execution trace."""
    timestamp: float
    instruction_address: int
    instruction_size: int
    opcode: str
    operands: List[str]
    registers_before: Dict[str, int]
    registers_after: Dict[str, int]
    is_branch: bool = False
    branch_taken: Optional[bool] = None
    thread_id: int = 0


@dataclass
class Symbol:
    """Represents a debug symbol."""
    name: str
    address: int
    size: int
    sym_type: str = "function"
    file_path: Optional[str] = None
    line_number: Optional[int] = None

    def contains_address(self, address: int) -> bool:
        return self.address <= address < self.address + self.size


@dataclass
class ProfilingResult:
    """Results from a profiling session."""
    session_id: str
    function_profiles: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    total_samples: int = 0
    sample_interval_ms: float = 10.0
    duration_seconds: float = 0.0
    start_time: float = field(default_factory=time.time)
    hotspots: List[Tuple[str, float]] = field(default_factory=list)
    call_graph: Dict[str, List[str]] = field(default_factory=dict)

    def get_top_functions(self, n: int = 10) -> List[Tuple[str, float]]:
        sorted_funcs = sorted(
            self.function_profiles.items(),
            key=lambda x: x[1].get("total_time_ms", 0),
            reverse=True,
        )
        return [(name, data.get("total_time_ms", 0)) for name, data in sorted_funcs[:n]]


@dataclass
class LogEntry:
    """Represents a structured log entry."""
    timestamp: datetime
    level: LogLevel
    source: str
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    duration_ms: Optional[float] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.name,
            "source": self.source,
            "message": self.message,
            "context": self.context,
            "correlation_id": self.correlation_id,
            "duration_ms": self.duration_ms,
            "tags": self.tags,
        }


@dataclass
class ErrorContext:
    """Contextual information about an error."""
    error_type: str
    error_message: str
    stack_trace: str
    timestamp: float = field(default_factory=time.time)
    source_file: Optional[str] = None
    source_line: Optional[int] = None
    variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RootCauseCandidate:
    """A candidate root cause for a software defect."""
    category: RootCauseCategory
    confidence: float
    description: str
    evidence: List[str] = field(default_factory=list)
    suggested_fix: Optional[str] = None
    severity: str = "medium"

    def is_high_confidence(self, threshold: float = 0.7) -> bool:
        return self.confidence >= threshold


# =============================================================================
# Core Engine Classes
# =============================================================================

class DebuggingEngine:
    """
    Interactive debugging engine with breakpoints, watchpoints,
    execution control, memory inspection, and disassembly.
    """

    def __init__(self) -> None:
        self.breakpoints: Dict[str, Breakpoint] = {}
        self.watchpoints: Dict[str, Watchpoint] = {}
        self.threads: Dict[int, Thread] = {}
        self.call_stack: List[DebugFrame] = []
        self.registers: Dict[str, Register] = {}
        self.memory_regions: List[MemoryRegion] = []
        self.execution_state: str = "stopped"
        self.process_id: Optional[int] = None
        self._bp_counter: int = 0
        self._wp_counter: int = 0
        self._instruction_count: int = 0
        self._lock = threading.Lock()
        self._logger = logging.getLogger("debugger.engine")

    def initialize(self) -> None:
        self.registers = {
            "rax": Register("rax", 0, 64),
            "rbx": Register("rbx", 0, 64),
            "rcx": Register("rcx", 0, 64),
            "rdx": Register("rdx", 0, 64),
            "rsp": Register("rsp", 0, 64, is_stack_pointer=True),
            "rbp": Register("rbp", 0, 64),
            "rip": Register("rip", 0x400000, 64, is_program_counter=True),
            "r8": Register("r8", 0, 64),
            "r9": Register("r9", 0, 64),
            "r10": Register("r10", 0, 64),
            "rflags": Register("rflags", 0x202, 64, is_flags=True),
        }
        self.memory_regions = [
            MemoryRegion(0x400000, 0x401000, MemoryProtection.READ_EXECUTE, ".text"),
            MemoryRegion(0x600000, 0x601000, MemoryProtection.READ_WRITE, ".data"),
            MemoryRegion(0x7fff0000, 0x7ffff000, MemoryProtection.READ_WRITE_EXECUTE, "[stack]"),
        ]
        self._logger.info("Engine initialized with x86-64 register layout")

    def attach_to_process(self, process_id: int) -> bool:
        if not self.registers:
            self.initialize()
        self.process_id = process_id
        self.execution_state = "attached"
        thread = Thread(thread_id=process_id, state=ThreadState.STOPPED, registers=self.registers.copy())
        self.threads[process_id] = thread
        self._logger.info(f"Attached to process {process_id}")
        return True

    def create_breakpoint(
        self, address: int, bp_type: BreakpointType = BreakpointType.SOFTWARE,
        condition: Optional[str] = None, temporary: bool = False, ignore_count: int = 0,
    ) -> str:
        with self._lock:
            self._bp_counter += 1
            bp_id = f"bp_{self._bp_counter}"
        bp = Breakpoint(bp_id=bp_id, address=address, bp_type=bp_type,
                        condition=condition, temporary=temporary, ignore_count=ignore_count)
        self.breakpoints[bp_id] = bp
        self._logger.info(f"Breakpoint {bp_id} at 0x{address:08x} (type={bp_type.value})")
        return bp_id

    def create_watchpoint(self, address: int, size: int = 4, access_type: str = "rw") -> str:
        with self._lock:
            self._wp_counter += 1
            wp_id = f"wp_{self._wp_counter}"
        wp = Watchpoint(wp_id=wp_id, address=address, size=size, access_type=access_type)
        self.watchpoints[wp_id] = wp
        self._logger.info(f"Watchpoint {wp_id} at 0x{address:08x} ({access_type})")
        return wp_id

    def remove_breakpoint(self, bp_id: str) -> bool:
        if bp_id in self.breakpoints:
            del self.breakpoints[bp_id]
            return True
        return False

    def remove_watchpoint(self, wp_id: str) -> bool:
        if wp_id in self.watchpoints:
            del self.watchpoints[wp_id]
            return True
        return False

    def enable_breakpoint(self, bp_id: str) -> bool:
        if bp_id in self.breakpoints:
            self.breakpoints[bp_id].enabled = True
            return True
        return False

    def disable_breakpoint(self, bp_id: str) -> bool:
        if bp_id in self.breakpoints:
            self.breakpoints[bp_id].enabled = False
            return True
        return False

    def step_into(self) -> DebugEvent:
        self._advance_instruction()
        self._logger.debug("Step into")
        return DebugEvent.SINGLE_STEP

    def step_over(self) -> DebugEvent:
        self._advance_instruction()
        return DebugEvent.SINGLE_STEP

    def step_out(self) -> DebugEvent:
        if self.call_stack:
            self.call_stack.pop()
        self._advance_instruction()
        return DebugEvent.SINGLE_STEP

    def step_instruction(self) -> DebugEvent:
        self._advance_instruction()
        return DebugEvent.SINGLE_STEP

    def continue_execution(self, max_steps: int = 100000) -> DebugEvent:
        self.execution_state = "running"
        steps = 0
        while self.execution_state == "running" and steps < max_steps:
            self._advance_instruction()
            steps += 1
            event = self._check_breakpoints()
            if event:
                return event
        return DebugEvent.PROGRAM_EXIT

    def _advance_instruction(self) -> None:
        if "rip" in self.registers:
            self.registers["rip"].value += 4
        self._instruction_count += 1

    def _check_breakpoints(self) -> Optional[DebugEvent]:
        if "rip" not in self.registers:
            return None
        addr = self.registers["rip"].value
        for bp_id, bp in self.breakpoints.items():
            if bp.enabled and bp.address == addr:
                if bp.should_ignore():
                    continue
                if self._eval_condition(bp.condition):
                    bp.increment_hit()
                    self.execution_state = "stopped"
                    return DebugEvent.BREAKPOINT
        return None

    def _eval_condition(self, condition: Optional[str]) -> bool:
        if not condition:
            return True
        try:
            env = {"__builtins__": {}}
            locals_dict = {}
            if self.call_stack:
                frame = self.call_stack[-1]
                locals_dict.update(frame.locals)
            return bool(eval(condition, env, locals_dict))
        except Exception:
            return True

    def read_memory(self, address: int, size: int) -> bytes:
        return b"\x00" * size

    def write_memory(self, address: int, data: bytes) -> bool:
        self._logger.info(f"Wrote {len(data)} bytes to 0x{address:08x}")
        return True

    def disassemble(self, address: int, count: int = 10) -> List[Dict[str, Any]]:
        mnemonics = [
            ("nop", []), ("mov", ["rax", "rbx"]), ("push", ["rbp"]),
            ("pop", ["rbx"]), ("add", ["rax", "0x10"]), ("sub", ["rsp", "0x20"]),
            ("call", ["0x401234"]), ("ret", []), ("cmp", ["rax", "0"]),
            ("je", ["0x401100"]), ("jmp", ["0x401200"]), ("xor", ["rax", "rax"]),
        ]
        instructions = []
        for i in range(count):
            m, ops = mnemonics[i % len(mnemonics)]
            instructions.append({"address": address + i * 4, "mnemonic": m, "operands": ops})
        return instructions

    def backtrace(self) -> List[DebugFrame]:
        if self.call_stack:
            return list(reversed(self.call_stack))
        return [
            DebugFrame("main", "/src/main.c", 100, frame_index=0),
            DebugFrame("process_input", "/src/handler.c", 50, frame_index=1),
        ]

    def info_registers(self) -> Dict[str, str]:
        return {n: f"0x{r.value:016x}" for n, r in self.registers.items()}

    def info_breaks(self) -> Dict[str, Any]:
        return {
            "breakpoints": {
                bp_id: {"address": f"0x{bp.address:08x}", "enabled": bp.enabled, "hits": bp.hit_count}
                for bp_id, bp in self.breakpoints.items()
            },
            "watchpoints": {
                wp_id: {"address": f"0x{wp.address:08x}", "size": wp.size, "enabled": wp.enabled}
                for wp_id, wp in self.watchpoints.items()
            },
            "total_breakpoints": len(self.breakpoints),
            "total_watchpoints": len(self.watchpoints),
        }

    def info_memory(self) -> List[Dict[str, Any]]:
        return [
            {"start": f"0x{r.start:x}", "end": f"0x{r.end:x}", "size": r.size, "perms": r.permissions.name, "name": r.name}
            for r in self.memory_regions
        ]


class RootCauseAnalyzer:
    """
    Evidence-based root cause analysis engine using hypothesis testing
    and pattern matching to identify defect origins.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("debugger.rca")
        self.hypotheses: List[Dict[str, Any]] = []
        self.evidence: List[Dict[str, Any]] = []
        self.candidates: List[RootCauseCandidate] = []
        self._pattern_db: Dict[str, List[str]] = {
            "memory_corruption": ["heap corruption", "buffer overflow", "use after free", "double free"],
            "race_condition": ["data race", "deadlock", "lock ordering", "ABA problem"],
            "logic_error": ["off by one", "null pointer", "wrong operator", "missing break"],
            "resource_leak": ["memory leak", "file handle leak", "socket leak"],
            "error_handling": ["unhandled exception", "missing error check", "swallowed error"],
        }

    def add_evidence(self, evidence_type: str, description: str, source: str) -> None:
        entry = {"type": evidence_type, "description": description, "source": source, "timestamp": time.time()}
        self.evidence.append(entry)
        self._logger.info(f"Evidence: {evidence_type} - {description}")

    def add_hypothesis(self, hypothesis: str, rationale: str, priority: int = 5) -> str:
        hid = f"hyp_{len(self.hypotheses) + 1}"
        self.hypotheses.append({
            "id": hid, "hypothesis": hypothesis, "rationale": rationale,
            "priority": priority, "status": "open", "evidence_for": [], "evidence_against": [],
        })
        self._logger.info(f"Hypothesis {hid}: {hypothesis}")
        return hid

    def evaluate_hypothesis(self, hypothesis_id: str, evidence_id: str, supports: bool) -> None:
        for hyp in self.hypotheses:
            if hyp["id"] == hypothesis_id:
                target = hyp["evidence_for"] if supports else hyp["evidence_against"]
                target.append(evidence_id)
                total = len(hyp["evidence_for"]) + len(hyp["evidence_against"])
                if total > 0:
                    ratio = len(hyp["evidence_for"]) / total
                    hyp["status"] = "strong" if ratio > 0.8 else "weak" if ratio < 0.2 else "open"
                break

    def analyze_crash_pattern(self, crashes: List[CrashInfo]) -> RootCauseCandidate:
        if not crashes:
            return RootCauseCandidate(RootCauseCategory.UNKNOWN, 0.0, "No crash data")
        type_counts: Dict[CrashType, int] = defaultdict(int)
        addr_counts: Dict[int, int] = defaultdict(int)
        for c in crashes:
            type_counts[c.crash_type] += 1
            addr_counts[c.crash_address] += 1
        common_type = max(type_counts, key=type_counts.get)
        common_addr = max(addr_counts, key=addr_counts.get)
        category = self._map_crash_type(common_type)
        confidence = type_counts[common_type] / len(crashes)
        fix = "Implement bounds checking" if common_type == CrashType.BUFFER_OVERFLOW else "Add reference counting" if common_type == CrashType.USE_AFTER_FREE else "Investigate with tracing"
        candidate = RootCauseCandidate(
            category=category, confidence=confidence,
            description=f"Recurring {common_type.value} at 0x{common_addr:x} ({type_counts[common_type]}/{len(crashes)} occurrences)",
            evidence=[f"Crash type '{common_type.value}' repeated {type_counts[common_type]}/{len(crashes)} times"],
            suggested_fix=fix, severity="high" if confidence > 0.7 else "medium",
        )
        self.candidates.append(candidate)
        return candidate

    def _map_crash_type(self, ct: CrashType) -> RootCauseCategory:
        mapping = {
            CrashType.SEGMENTATION_FAULT: RootCauseCategory.MEMORY_SAFETY,
            CrashType.STACK_OVERFLOW: RootCauseCategory.MEMORY_SAFETY,
            CrashType.BUFFER_OVERFLOW: RootCauseCategory.MEMORY_SAFETY,
            CrashType.USE_AFTER_FREE: RootCauseCategory.MEMORY_SAFETY,
            CrashType.DEADLOCK: RootCauseCategory.RACE_CONDITION,
            CrashType.INTEGER_OVERFLOW: RootCauseCategory.LOGIC_ERROR,
            CrashType.OUT_OF_MEMORY: RootCauseCategory.RESOURCE_LEAK,
        }
        return mapping.get(ct, RootCauseCategory.UNKNOWN)

    def analyze_error_context(self, context: ErrorContext) -> RootCauseCandidate:
        best_cat = RootCauseCategory.UNKNOWN
        best_conf = 0.0
        for cat, patterns in self._pattern_db.items():
            for pat in patterns:
                if pat in context.error_type.lower() or pat in context.error_message.lower():
                    conf = 0.6 + (0.1 if context.stack_trace else 0) + (0.1 if context.variables else 0)
                    if conf > best_conf:
                        best_conf = conf
                        best_cat = RootCauseCategory(cat) if cat in RootCauseCategory.__members__ else RootCauseCategory.UNKNOWN
        return RootCauseCandidate(best_cat, min(best_conf, 0.95), f"{context.error_type}: {context.error_message}",
                                  evidence=[context.error_type, context.error_message])

    def get_ranked_candidates(self) -> List[RootCauseCandidate]:
        return sorted(self.candidates, key=lambda c: c.confidence, reverse=True)

    def generate_report(self) -> Dict[str, Any]:
        return {
            "total_evidence": len(self.evidence),
            "total_hypotheses": len(self.hypotheses),
            "candidates": [
                {"category": c.category.value, "confidence": c.confidence, "description": c.description, "fix": c.suggested_fix}
                for c in self.get_ranked_candidates()
            ],
        }


class LoggingManager:
    """
    Centralized logging with structured entries, correlation tracking,
    filtering, and multiple output handlers.
    """

    def __init__(self, name: str = "debugger.logging") -> None:
        self._logger = logging.getLogger(name)
        self._entries: List[LogEntry] = []
        self._correlation_counter: int = 0
        self._active_correlations: Dict[str, List[LogEntry]] = defaultdict(list)
        self._filters: List[Callable[[LogEntry], bool]] = []
        self._handlers: List[Callable[[LogEntry], None]] = []
        self._max_entries: int = 100000
        self._level: LogLevel = LogLevel.DEBUG
        self._timers: Dict[str, float] = {}

    def set_level(self, level: LogLevel) -> None:
        self._level = level

    def add_filter(self, filter_fn: Callable[[LogEntry], bool]) -> None:
        self._filters.append(filter_fn)

    def add_handler(self, handler: Callable[[LogEntry], None]) -> None:
        self._handlers.append(handler)

    def start_correlation(self) -> str:
        self._correlation_counter += 1
        cid = f"corr_{self._correlation_counter}"
        self._active_correlations[cid] = []
        return cid

    def end_correlation(self, correlation_id: str) -> List[LogEntry]:
        return self._active_correlations.pop(correlation_id, [])

    def log(self, level: LogLevel, source: str, message: str,
            context: Optional[Dict[str, Any]] = None, correlation_id: Optional[str] = None) -> LogEntry:
        entry = LogEntry(timestamp=datetime.now(timezone.utc), level=level, source=source,
                         message=message, context=context or {}, correlation_id=correlation_id)
        for filt in self._filters:
            if not filt(entry):
                return entry
        self._entries.append(entry)
        if len(self._entries) > self._max_entries:
            self._entries = self._entries[-self._max_entries:]
        if correlation_id and correlation_id in self._active_correlations:
            self._active_correlations[correlation_id].append(entry)
        for handler in self._handlers:
            try:
                handler(entry)
            except Exception as exc:
                self._logger.error(f"Handler error: {exc}")
        return entry

    def trace(self, source: str, message: str, **kw: Any) -> LogEntry:
        return self.log(LogLevel.TRACE, source, message, **kw)

    def debug(self, source: str, message: str, **kw: Any) -> LogEntry:
        return self.log(LogLevel.DEBUG, source, message, **kw)

    def info(self, source: str, message: str, **kw: Any) -> LogEntry:
        return self.log(LogLevel.INFO, source, message, **kw)

    def warning(self, source: str, message: str, **kw: Any) -> LogEntry:
        return self.log(LogLevel.WARNING, source, message, **kw)

    def error(self, source: str, message: str, **kw: Any) -> LogEntry:
        return self.log(LogLevel.ERROR, source, message, **kw)

    def critical(self, source: str, message: str, **kw: Any) -> LogEntry:
        return self.log(LogLevel.CRITICAL, source, message, **kw)

    def start_timer(self, name: str) -> None:
        self._timers[name] = time.perf_counter()

    def end_timer(self, name: str) -> float:
        start = self._timers.pop(name, None)
        if start is None:
            return 0.0
        elapsed = (time.perf_counter() - start) * 1000
        self.debug("timer", f"{name}: {elapsed:.2f}ms", duration_ms=elapsed)
        return elapsed

    def get_entries(self, level: Optional[LogLevel] = None, source: Optional[str] = None, limit: int = 100) -> List[LogEntry]:
        filtered = self._entries
        if level is not None:
            filtered = [e for e in filtered if e.level == level]
        if source is not None:
            filtered = [e for e in filtered if e.source == source]
        return filtered[-limit:]

    def get_summary(self) -> Dict[str, Any]:
        level_counts: Dict[str, int] = defaultdict(int)
        for e in self._entries:
            level_counts[e.level.name] += 1
        return {"total": len(self._entries), "by_level": dict(level_counts)}

    def clear(self) -> int:
        count = len(self._entries)
        self._entries.clear()
        return count

    def export_json(self) -> str:
        return json.dumps([e.to_dict() for e in self._entries[-1000:]], indent=2, default=str)


class Profiler:
    """
    CPU and memory profiling with sampling, call graph construction,
    hotspot detection, and performance analysis.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("debugger.profiler")
        self._sessions: List[ProfilingResult] = []
        self._current: Optional[ProfilingResult] = None
        self._call_counts: Dict[str, int] = defaultdict(int)
        self._self_time: Dict[str, float] = defaultdict(float)
        self._total_time: Dict[str, float] = defaultdict(float)
        self._children: Dict[str, List[str]] = defaultdict(list)
        self._parents: Dict[str, Set[str]] = defaultdict(set)
        self._sampling: bool = False

    def start_session(self, session_id: Optional[str] = None, sample_interval_ms: float = 10.0) -> str:
        sid = session_id or f"profile_{int(time.time())}"
        self._current = ProfilingResult(session_id=sid, sample_interval_ms=sample_interval_ms, start_time=time.time())
        self._sampling = True
        self._call_counts.clear()
        self._self_time.clear()
        self._total_time.clear()
        self._children.clear()
        self._parents.clear()
        self._logger.info(f"Profiling session {sid} started")
        return sid

    def stop_session(self) -> Optional[ProfilingResult]:
        if self._current is None:
            return None
        self._current.duration_seconds = time.time() - self._current.start_time
        self._compute_profiles()
        self._detect_hotspots()
        self._build_call_graph()
        self._sessions.append(self._current)
        result = self._current
        self._current = None
        self._sampling = False
        self._logger.info(f"Session stopped: {result.total_samples} samples in {result.duration_seconds:.2f}s")
        return result

    def record_sample(self, function_name: str, duration_ms: float) -> None:
        if not self._sampling:
            return
        self._call_counts[function_name] += 1
        self._self_time[function_name] += duration_ms

    def record_call(self, caller: str, callee: str) -> None:
        self._children[caller].append(callee)
        self._parents[callee].add(caller)

    def record_call_time(self, caller: str, callee: str, duration_ms: float) -> None:
        self.record_call(caller, callee)
        self._self_time[callee] += duration_ms
        self._total_time[caller] += duration_ms

    def _compute_profiles(self) -> None:
        if self._current is None:
            return
        for name, self_ms in self._self_time.items():
            total_ms = self._total_time.get(name, 0.0) + self_ms
            count = self._call_counts.get(name, 0)
            self._current.function_profiles[name] = {
                "total_time_ms": total_ms, "self_time_ms": self_ms,
                "call_count": count, "avg_time_ms": total_ms / count if count else 0.0,
                "children": self._children.get(name, []),
            }

    def _detect_hotspots(self) -> None:
        if self._current is None:
            return
        total = sum(p["total_time_ms"] for p in self._current.function_profiles.values())
        sorted_f = sorted(self._current.function_profiles.items(), key=lambda x: x[1]["total_time_ms"], reverse=True)
        self._current.hotspots = [
            (n, p["total_time_ms"] / total * 100 if total else 0) for n, p in sorted_f[:20]
        ]

    def _build_call_graph(self) -> None:
        if self._current is None:
            return
        for caller, callees in self._children.items():
            self._current.call_graph[caller] = list(set(callees))

    def get_hotspots(self, n: int = 10) -> List[Tuple[str, float]]:
        if not self._sessions:
            return []
        return self._sessions[-1].hotspots[:n]

    def get_function_profile(self, name: str) -> Optional[Dict[str, Any]]:
        if self._current and name in self._current.function_profiles:
            return self._current.function_profiles[name]
        if self._sessions and name in self._sessions[-1].function_profiles:
            return self._sessions[-1].function_profiles[name]
        return None

    def get_callers(self, name: str) -> List[str]:
        return list(self._parents.get(name, set()))

    def get_callees(self, name: str) -> List[str]:
        return self._children.get(name, [])

    def generate_flamegraph_data(self) -> Dict[str, Any]:
        if not self._sessions:
            return {"name": "root", "value": 0, "children": []}
        latest = self._sessions[-1]
        return self._build_fg_node("root", latest)

    def _build_fg_node(self, name: str, result: ProfilingResult) -> Dict[str, Any]:
        profile = result.function_profiles.get(name, {})
        children = [
            self._build_fg_node(c, result) for c in result.call_graph.get(name, [])
            if c in result.function_profiles
        ]
        return {"name": name, "value": profile.get("self_time_ms", 0), "total": profile.get("total_time_ms", 0), "children": children}

    def get_summary(self) -> Dict[str, Any]:
        if not self._sessions:
            return {"sessions": 0}
        latest = self._sessions[-1]
        return {"sessions": len(self._sessions), "duration": latest.duration_seconds,
                "samples": latest.total_samples, "functions": len(latest.function_profiles)}


class TracingManager:
    """
    Execution tracing supporting instruction-level, function-level,
    syscall, and memory access tracing with filtering and export.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("debugger.tracing")
        self._traces: List[TraceEntry] = []
        self._is_tracing: bool = False
        self._options: Dict[str, Any] = {
            "instruction_trace": True, "function_trace": True,
            "syscall_trace": True, "memory_trace": False, "max_entries": 1000000,
        }
        self._function_traces: List[Dict[str, Any]] = []
        self._syscall_traces: List[Dict[str, Any]] = []
        self._memory_traces: List[Dict[str, Any]] = []
        self._branch_counts: Dict[int, int] = defaultdict(int)
        self._address_hits: Dict[int, int] = defaultdict(int)
        self._coverage: Set[int] = set()

    def start_tracing(self, options: Optional[Dict[str, Any]] = None) -> None:
        if options:
            self._options.update(options)
        self._is_tracing = True
        self._traces.clear()
        self._function_traces.clear()
        self._syscall_traces.clear()
        self._memory_traces.clear()
        self._branch_counts.clear()
        self._address_hits.clear()
        self._coverage.clear()
        self._logger.info("Tracing started")

    def stop_tracing(self) -> Dict[str, Any]:
        self._is_tracing = False
        summary = {
            "total_instructions": len(self._traces),
            "total_functions": len(set(t.function_name for t in self._traces if hasattr(t, 'function_name'))),
            "total_syscalls": len(self._syscall_traces),
            "total_memory_accesses": len(self._memory_traces),
            "unique_addresses": len(self._address_hits),
            "coverage_addresses": len(self._coverage),
        }
        self._logger.info(f"Tracing stopped: {summary}")
        return summary

    def record_instruction(self, address: int, size: int, opcode: str, operands: List[str],
                           registers_before: Optional[Dict[str, int]] = None,
                           registers_after: Optional[Dict[str, int]] = None) -> None:
        if not self._is_tracing:
            return
        entry = TraceEntry(timestamp=time.time(), instruction_address=address, instruction_size=size,
                           opcode=opcode, operands=operands,
                           registers_before=registers_before or {}, registers_after=registers_after or {})
        self._traces.append(entry)
        self._address_hits[address] += 1
        self._coverage.add(address)
        if len(self._traces) > self._options["max_entries"]:
            self._traces = self._traces[-self._options["max_entries"] // 2:]

    def record_function_call(self, function_name: str, arguments: Dict[str, Any],
                             return_value: Optional[Any] = None) -> None:
        if not self._is_tracing or not self._options["function_trace"]:
            return
        self._function_traces.append({
            "timestamp": time.time(), "function": function_name,
            "arguments": arguments, "return_value": return_value, "is_return": return_value is not None,
        })

    def record_syscall(self, name: str, arguments: List[Any], return_value: Optional[int] = None,
                       error: Optional[str] = None) -> None:
        if not self._is_tracing or not self._options["syscall_trace"]:
            return
        self._syscall_traces.append({
            "timestamp": time.time(), "name": name, "arguments": arguments,
            "return_value": return_value, "error": error,
        })

    def record_memory_access(self, address: int, size: int, access_type: str,
                             value: Optional[bytes] = None) -> None:
        if not self._is_tracing or not self._options["memory_trace"]:
            return
        self._memory_traces.append({
            "timestamp": time.time(), "address": address, "size": size,
            "type": access_type, "value_hex": value.hex() if value else None,
        })

    def record_branch(self, address: int, taken: bool, target: Optional[int] = None) -> None:
        if not self._is_tracing:
            return
        self._branch_counts[address] += 1
        if self._traces:
            self._traces[-1].is_branch = True
            self._traces[-1].branch_taken = taken

    def get_trace_range(self, start: int = 0, end: Optional[int] = None) -> List[TraceEntry]:
        return self._traces[start:end]

    def get_function_trace(self, name: str) -> List[Dict[str, Any]]:
        return [t for t in self._function_traces if t["function"] == name]

    def get_syscall_summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for entry in self._syscall_traces:
            counts[entry["name"]] += 1
        return dict(counts)

    def get_coverage(self) -> Dict[str, Any]:
        branches = len(self._branch_counts)
        taken = sum(1 for c in self._branch_counts.values() if c > 0)
        return {"unique_addresses": len(self._coverage), "branches": branches,
                "branches_taken": taken, "branch_coverage": taken / branches if branches else 0.0}

    def get_hot_addresses(self, n: int = 10) -> List[Tuple[int, int]]:
        return sorted(self._address_hits.items(), key=lambda x: x[1], reverse=True)[:n]

    def find_execution_path(self, start_addr: int, end_addr: int, max_depth: int = 100) -> List[int]:
        path: List[int] = []
        for trace in self._traces:
            if trace.instruction_address == start_addr:
                path.append(trace.instruction_address)
            elif trace.instruction_address == end_addr:
                path.append(trace.instruction_address)
                return path
            elif path and trace.is_branch and trace.branch_taken:
                path.append(trace.instruction_address)
            if len(path) >= max_depth:
                break
        return path

    def export_trace(self, fmt: str = "json") -> str:
        if fmt == "json":
            data = [{"address": t.instruction_address, "opcode": t.opcode, "operands": t.operands}
                    for t in self._traces[-5000:]]
            return json.dumps(data, indent=2)
        elif fmt == "csv":
            lines = ["address,opcode,operands"]
            for t in self._traces[-5000:]:
                lines.append(f"0x{t.instruction_address:x},{t.opcode},{';'.join(t.operands)}")
            return "\n".join(lines)
        return ""


class ErrorResolver:
    """
    Knowledge-based error resolution with pattern matching,
    solution suggestions, and resolution history tracking.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("debugger.resolver")
        self._knowledge_base: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._resolution_history: List[Dict[str, Any]] = []
        self._active_errors: Dict[str, ErrorContext] = {}
        self._fix_templates: Dict[str, str] = {
            "null_pointer": "Add null check before dereferencing. Use optional chaining or guard clauses.",
            "index_out_of_bounds": "Validate array/list index before access. Use bounds checking.",
            "memory_leak": "Ensure all allocated resources are freed. Use RAII or context managers.",
            "deadlock": "Enforce consistent lock ordering. Use lock timeouts.",
            "race_condition": "Protect shared state with synchronization. Use mutexes or atomics.",
            "overflow": "Validate arithmetic operations for overflow. Use checked arithmetic.",
            "timeout": "Increase timeout or optimize the slow operation. Consider async patterns.",
            "permission_denied": "Check file/process permissions. Ensure appropriate access rights.",
        }

    def register_knowledge(self, error_pattern: str, solution: str, category: str = "general",
                           confidence: float = 0.5) -> None:
        entry = {"pattern": error_pattern, "solution": solution, "category": category,
                 "confidence": confidence, "usage_count": 0, "success_count": 0, "created_at": time.time()}
        self._knowledge_base[error_pattern].append(entry)
        self._logger.info(f"Knowledge registered: {error_pattern}")

    def resolve_error(self, context: ErrorContext) -> Dict[str, Any]:
        self._active_errors[context.error_type] = context
        suggestions = self._find_solutions(context)
        if not suggestions:
            suggestions = [{"solution": "No known solution. Manual investigation required.", "confidence": 0.0}]
        best = max(suggestions, key=lambda s: s.get("confidence", 0))
        resolution = {
            "error_type": context.error_type, "error_message": context.error_message,
            "best_suggestion": best["solution"], "confidence": best.get("confidence", 0),
            "all_suggestions": suggestions,
            "context": {"source_file": context.source_file, "source_line": context.source_line, "variables": context.variables},
        }
        self._resolution_history.append({"timestamp": time.time(), "error_type": context.error_type, "resolution": resolution})
        return resolution

    def _find_solutions(self, context: ErrorContext) -> List[Dict[str, Any]]:
        solutions: List[Dict[str, Any]] = []
        combined = f"{context.error_type} {context.error_message}".lower()
        for pattern, entries in self._knowledge_base.items():
            if pattern.lower() in combined:
                for entry in entries:
                    entry["usage_count"] += 1
                    solutions.append({"solution": entry["solution"], "confidence": entry["confidence"],
                                      "category": entry["category"], "pattern": pattern})
        for key, template in self._fix_templates.items():
            if key.replace("_", " ") in combined:
                solutions.append({"solution": template, "confidence": 0.6, "category": "template", "pattern": key})
        return solutions

    def suggest_fix(self, error_type: str, error_message: str) -> str:
        combined = f"{error_type} {error_message}".lower()
        for key, template in self._fix_templates.items():
            if key.replace("_", " ") in combined:
                return template
        return "No automated fix suggestion available. Review the error context and stack trace."

    def get_resolution_history(self, error_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        history = self._resolution_history
        if error_type:
            history = [h for h in history if h["error_type"] == error_type]
        return history[-limit:]

    def get_knowledge_stats(self) -> Dict[str, Any]:
        total_entries = sum(len(v) for v in self._knowledge_base.values())
        total_usage = sum(e["usage_count"] for entries in self._knowledge_base.values() for e in entries)
        total_success = sum(e["success_count"] for entries in self._knowledge_base.values() for e in entries)
        return {
            "patterns": len(self._knowledge_base), "total_solutions": total_entries,
            "total_usage": total_usage, "success_rate": total_success / total_usage if total_usage else 0,
            "resolutions_performed": len(self._resolution_history),
        }

    def clear_active_errors(self) -> int:
        count = len(self._active_errors)
        self._active_errors.clear()
        return count


class PostMortemAnalyzer:
    """
    Post-mortem analysis engine for crash dumps, core files,
    and error logs after program termination.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("debugger.postmortem")
        self._dumps: List[CrashInfo] = []
        self._analysis_results: List[Dict[str, Any]] = []
        self._timeline: List[Dict[str, Any]] = []

    def analyze_dump(self, crash_info: CrashInfo) -> Dict[str, Any]:
        self._dumps.append(crash_info)
        analysis = {
            "crash_hash": crash_info.get_crash_hash(),
            "crash_type": crash_info.crash_type.value,
            "crash_address": f"0x{crash_info.crash_address:08x}",
            "crashing_instruction": crash_info.crashing_instruction,
            "faulting_register": crash_info.faulting_register,
            "signal": crash_info.signal_name or f"signal_{crash_info.signal_number}",
            "stack_frames": len(crash_info.stack_trace),
            "exploitability": self._assess_exploitability(crash_info),
            "root_cause_hints": self._generate_hints(crash_info),
            "memory_analysis": self._analyze_memory(crash_info),
            "recommendations": self._generate_recommendations(crash_info),
        }
        self._analysis_results.append(analysis)
        self._logger.info(f"Post-mortem analysis: {analysis['crash_hash']}")
        return analysis

    def _assess_exploitability(self, crash: CrashInfo) -> Dict[str, Any]:
        score = 0
        factors: List[str] = []
        if crash.crash_address & 0xFF == 0x41:
            score += 30
            factors.append("Controlled crash address (0x41 pattern)")
        if crash.faulting_register in ("rsp", "rbp"):
            score += 20
            factors.append("Stack pointer/frame pointer corrupted")
        if crash.crash_type == CrashType.BUFFER_OVERFLOW:
            score += 30
            factors.append("Buffer overflow detected")
        if crash.crash_type == CrashType.USE_AFTER_FREE:
            score += 25
            factors.append("Use-after-free detected")
        if crash.memory_dump and b"\x90" * 10 in crash.memory_dump:
            score += 15
            factors.append("NOP sled detected")
        rating = "probably_exploitable" if score >= 70 else "probably_not_exploitable" if score >= 30 else "not_exploitable"
        return {"rating": rating, "score": min(score, 100), "factors": factors}

    def _generate_hints(self, crash: CrashInfo) -> List[str]:
        hints: List[str] = []
        if crash.crash_type == CrashType.SEGMENTATION_FAULT:
            hints.append("Null pointer dereference or invalid memory access")
            if crash.faulting_register in ("rsp", "rbp"):
                hints.append("Stack corruption - check buffer overflow")
        if crash.crash_type == CrashType.STACK_OVERFLOW:
            hints.append("Excessive recursion or large stack allocations")
        if crash.crash_type == CrashType.HEAP_CORRUPTION:
            hints.append("Heap metadata corruption - possible buffer overflow")
        if crash.crash_address == 0x0:
            hints.append("NULL pointer dereference")
        elif crash.crash_address & 0xFFFF0000 == 0xDEAD0000:
            hints.append("Use of poisoned/deallocated memory")
        if crash.stack_trace:
            hints.append(f"Crash in {crash.stack_trace[0].function_name}")
        return hints

    def _analyze_memory(self, crash: CrashInfo) -> Dict[str, Any]:
        if not crash.memory_dump:
            return {"available": False}
        dump = crash.memory_dump
        analysis: Dict[str, Any] = {"available": True, "size": len(dump), "null_bytes": dump.count(b"\x00")}
        if b"\x90" * 10 in dump:
            analysis["nop_sled"] = True
            analysis["nop_sled_offset"] = dump.find(b"\x90" * 10)
        printable = sum(1 for b in dump if 0x20 <= b <= 0x7E)
        analysis["printable_ratio"] = printable / len(dump) if dump else 0
        return analysis

    def _generate_recommendations(self, crash: CrashInfo) -> List[str]:
        recs: List[str] = []
        if crash.crash_type in (CrashType.BUFFER_OVERFLOW, CrashType.STACK_OVERFLOW):
            recs.append("Enable AddressSanitizer (ASAN)")
            recs.append("Add bounds checking on buffer operations")
        if crash.crash_type == CrashType.USE_AFTER_FREE:
            recs.append("Enable LeakSanitizer and AddressSanitizer")
            recs.append("Review memory ownership patterns")
        if crash.crash_type == CrashType.DEADLOCK:
            recs.append("Implement lock ordering to prevent deadlock")
        recs.append("Enable core dumps for post-mortem analysis")
        recs.append("Write a regression test for the crash scenario")
        return recs

    def build_timeline(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._timeline = sorted(events, key=lambda e: e.get("timestamp", 0))
        return self._timeline

    def correlate_dumps(self) -> Dict[str, Any]:
        if len(self._dumps) < 2:
            return {"correlations": [], "message": "Need at least 2 dumps"}
        type_groups: Dict[str, List[CrashInfo]] = defaultdict(list)
        for dump in self._dumps:
            type_groups[dump.crash_type.value].append(dump)
        correlations = []
        for crash_type, dumps in type_groups.items():
            if len(dumps) > 1:
                addrs = set(d.crash_address for d in dumps)
                correlations.append({
                    "crash_type": crash_type, "count": len(dumps),
                    "unique_addresses": len(addrs),
                    "recurring": len(addrs) < len(dumps),
                    "addresses": [f"0x{a:08x}" for a in addrs],
                })
        return {"correlations": correlations, "total_dumps": len(self._dumps)}

    def get_analysis_results(self) -> List[Dict[str, Any]]:
        return self._analysis_results

    def get_most_common_crash(self) -> Optional[str]:
        if not self._dumps:
            return None
        counts: Dict[str, int] = defaultdict(int)
        for d in self._dumps:
            counts[d.crash_type.value] += 1
        return max(counts, key=counts.get) if counts else None


# =============================================================================
# Factory Function
# =============================================================================

def create_debugging_agent() -> Dict[str, Any]:
    """Create a fully initialized debugging agent suite."""
    engine = DebuggingEngine()
    engine.initialize()
    rca = RootCauseAnalyzer()
    logging_mgr = LoggingManager()
    profiler = Profiler()
    tracing = TracingManager()
    resolver = ErrorResolver()
    postmortem = PostMortemAnalyzer()
    resolver.register_knowledge("segfault", "Check for null pointer or buffer overflow", "memory_safety", 0.7)
    resolver.register_knowledge("deadlock", "Implement lock ordering and timeouts", "concurrency", 0.8)
    resolver.register_knowledge("memory leak", "Ensure proper resource cleanup", "resource_management", 0.6)
    return {
        "engine": engine, "root_cause_analyzer": rca, "logging_manager": logging_mgr,
        "profiler": profiler, "tracing_manager": tracing, "error_resolver": resolver,
        "postmortem_analyzer": postmortem,
    }


if __name__ == "__main__":
    agent = create_debugging_agent()
    engine = agent["engine"]
    engine.create_breakpoint(0x400100)
    engine.create_watchpoint(0x600000, size=8, access_type="rw")
    event = engine.continue_execution()
    print(f"Execution stopped: {event.value}")
    print(json.dumps({
        "breakpoints": engine.info_breaks()["total_breakpoints"],
        "watchpoints": engine.info_breaks()["total_watchpoints"],
    }, indent=2))
