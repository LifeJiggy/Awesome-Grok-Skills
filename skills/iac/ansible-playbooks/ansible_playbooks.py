"""
Ansible Playbooks Module
Configuration management and automation with Ansible
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TaskModule(Enum):
    APT = "apt"
    YUM = "yum"
    DNF = "dnf"
    SERVICE = "service"
    SYSTEMD = "systemd"
    COPY = "copy"
    TEMPLATE = "template"
    FILE = "file"
    LINEINFILE = "lineinfile"
    SHELL = "shell"
    COMMAND = "command"
    USER = "user"
    GROUP = "group"
    CRON = "cron"
    DEBUG = "debug"
    SET_FACT = "set_fact"
    ASSERT = "assert"
    URI = "uri"
    WAIT_FOR = "wait_for"
    INCLUDE_TASKS = "include_tasks"
    IMPORT_TASKS = "import_tasks"
    IMPORT_ROLE = "import_role"
    INCLUDE_ROLE = "include_role"


class VariableScope(Enum):
    GLOBAL = "global"
    GROUP = "group"
    HOST = "host"
    PLAY = "play"
    TASK = "task"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    CHANGED = "changed"
    OK = "ok"
    FAILED = "failed"
    SKIPPED = "skipped"
    UNREACHABLE = "unreachable"


class PlayStrategy(Enum):
    LINEAR = "linear"
    FREE = "free"
    DEBUG = "debug"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """Ansible task definition."""
    name: str
    module: str
    args: Dict[str, Any] = field(default_factory=dict)
    register: Optional[str] = None
    when: Optional[str] = None
    loop: Optional[List[Any]] = None
    notify: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    ignore_errors: bool = False
    become: bool = False
    become_user: Optional[str] = None
    retries: int = 0
    delay: int = 0
    until: Optional[str] = None
    changed_when: Optional[str] = None
    failed_when: Optional[str] = None
    environment: Dict[str, str] = field(default_factory=dict)
    delegate_to: Optional[str] = None
    run_once: bool = False

    def to_dict(self) -> Dict[str, Any]:
        task_dict: Dict[str, Any] = {"name": self.name}
        task_dict[self.module] = self.args
        if self.register:
            task_dict["register"] = self.register
        if self.when:
            task_dict["when"] = self.when
        if self.loop:
            task_dict["loop"] = self.loop
        if self.notify:
            task_dict["notify"] = self.notify
        if self.tags:
            task_dict["tags"] = self.tags
        if self.ignore_errors:
            task_dict["ignore_errors"] = True
        if self.become:
            task_dict["become"] = True
        if self.become_user:
            task_dict["become_user"] = self.become_user
        if self.retries > 0:
            task_dict["retries"] = self.retries
            task_dict["delay"] = self.delay
        if self.changed_when:
            task_dict["changed_when"] = self.changed_when
        if self.failed_when:
            task_dict["failed_when"] = self.failed_when
        if self.environment:
            task_dict["environment"] = self.environment
        if self.delegate_to:
            task_dict["delegate_to"] = self.delegate_to
        if self.run_once:
            task_dict["run_once"] = True
        return task_dict


@dataclass
class Handler:
    """Ansible handler definition."""
    name: str
    module: str
    args: Dict[str, Any] = field(default_factory=dict)
    listen: Optional[str] = None
    become: bool = False
    become_user: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        handler_dict: Dict[str, Any] = {"name": self.name}
        handler_dict[self.module] = self.args
        if self.listen:
            handler_dict["listen"] = self.listen
        if self.become:
            handler_dict["become"] = True
        return handler_dict


@dataclass
class RoleTask:
    """Task within a role."""
    name: str
    module: str
    args: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    when: Optional[str] = None
    become: bool = False


@dataclass
class Host:
    """Ansible inventory host."""
    name: str
    ansible_host: Optional[str] = None
    ansible_user: Optional[str] = None
    ansible_port: Optional[int] = None
    ansible_ssh_private_key_file: Optional[str] = None
    ansible_python_interpreter: Optional[str] = None
    vars: Dict[str, Any] = field(default_factory=dict)

    @property
    def host_vars(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.ansible_host:
            result["ansible_host"] = self.ansible_host
        if self.ansible_user:
            result["ansible_user"] = self.ansible_user
        if self.ansible_port:
            result["ansible_port"] = self.ansible_port
        if self.ansible_ssh_private_key_file:
            result["ansible_ssh_private_key_file"] = self.ansible_ssh_private_key_file
        result.update(self.vars)
        return result


@dataclass
class Group:
    """Ansible inventory group."""
    name: str
    hosts: List[str] = field(default_factory=list)
    vars: Dict[str, Any] = field(default_factory=dict)
    children: List[str] = field(default_factory=list)


@dataclass
class PlayResult:
    """Result of a playbook execution."""
    play_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    play_name: str = ""
    status: str = "success"
    task_results: List[Dict[str, Any]] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    hosts_reached: int = 0
    hosts_failed: int = 0
    hosts_unreachable: int = 0
    changed: int = 0
    ok: int = 0
    failures: int = 0
    skips: int = 0
    duration_seconds: float = 0.0

    @property
    def success(self) -> bool:
        return self.failures == 0 and self.hosts_failed == 0

    def to_summary(self) -> Dict[str, Any]:
        return {
            "play": self.play_name,
            "status": self.status,
            "hosts_reached": self.hosts_reached,
            "hosts_failed": self.hosts_failed,
            "changed": self.changed,
            "ok": self.ok,
            "failures": self.failures,
            "skips": self.skips,
            "duration": f"{self.duration_seconds:.1f}s",
        }


@dataclass
class PlayStats:
    """Statistics from playbook execution."""
    plays: List[PlayResult] = field(default_factory=list)
    total_duration_seconds: float = 0.0
    total_hosts: int = 0
    total_tasks: int = 0

    @property
    def overall_success(self) -> bool:
        return all(p.success for p in self.plays)


# ---------------------------------------------------------------------------
# Playbook Generator
# ---------------------------------------------------------------------------

class PlaybookGenerator:
    """Generates Ansible playbook YAML structures."""

    def __init__(
        self,
        name: str = "playbook",
        hosts: str = "all",
        become: bool = False,
        strategy: PlayStrategy = PlayStrategy.LINEAR,
        gather_facts: bool = True,
    ) -> None:
        self.name = name
        self.hosts = hosts
        self.become = become
        self.strategy = strategy
        self.gather_facts = gather_facts
        self._tasks: List[Task] = []
        self._handlers: List[Handler] = []
        self._vars: Dict[str, Any] = {}
        self._pre_tasks: List[Task] = []
        self._post_tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def add_handler(self, handler: Handler) -> None:
        self._handlers.append(handler)

    def add_pre_task(self, task: Task) -> None:
        self._pre_tasks.append(task)

    def add_post_task(self, task: Task) -> None:
        self._post_tasks.append(task)

    def set_variable(self, key: str, value: Any) -> None:
        self._vars[key] = value

    def generate(self) -> str:
        play: Dict[str, Any] = {
            "name": self.name,
            "hosts": self.hosts,
            "gather_facts": self.gather_facts,
            "strategy": self.strategy.value,
        }

        if self.become:
            play["become"] = True

        if self._vars:
            play["vars"] = self._vars

        if self._pre_tasks:
            play["pre_tasks"] = [t.to_dict() for t in self._pre_tasks]

        play["tasks"] = [t.to_dict() for t in self._tasks]

        if self._post_tasks:
            play["post_tasks"] = [t.to_dict() for t in self._post_tasks]

        if self._handlers:
            play["handlers"] = [h.to_dict() for h in self._handlers]

        return json.dumps([play], indent=2)


# ---------------------------------------------------------------------------
# Role Generator
# ---------------------------------------------------------------------------

class RoleGenerator:
    """Generates Ansible role structures."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self._tasks: List[RoleTask] = []
        self._handlers: List[Dict[str, Any]] = []
        self._defaults: Dict[str, Any] = {}
        self._vars: Dict[str, Any] = {}
        self._files: List[str] = []
        self._templates: List[str] = []
        self._meta: Dict[str, Any] = {"role_name": name, "description": description}

    def add_task(self, task: RoleTask) -> None:
        self._tasks.append(task)

    def add_handler(self, name: str, module: str, args: Dict[str, Any]) -> None:
        self._handlers.append({"name": name, module: args})

    def set_default(self, key: str, value: Any) -> None:
        self._defaults[key] = value

    def add_dependency(self, role_name: str) -> None:
        dependencies = self._meta.get("dependencies", [])
        dependencies.append(role_name)
        self._meta["dependencies"] = dependencies

    def generate(self) -> Dict[str, Any]:
        return {
            "meta": self._meta,
            "defaults": self._defaults,
            "vars": self._vars,
            "tasks": [
                {"name": t.name, t.module: t.args}
                for t in self._tasks
            ],
            "handlers": self._handlers,
            "files": self._files,
            "templates": self._templates,
        }


# ---------------------------------------------------------------------------
# Inventory Manager
# ---------------------------------------------------------------------------

class InventoryManager:
    """Manages Ansible inventory."""

    def __init__(self) -> None:
        self._hosts: Dict[str, Host] = {}
        self._groups: Dict[str, Group] = {}

    def add_host(self, host: Host) -> None:
        self._hosts[host.name] = host

    def add_group(self, group: Group) -> None:
        self._groups[group.name] = group

    def add_host_to_group(self, group_name: str, host_name: str) -> None:
        group = self._groups.get(group_name)
        if group and host_name not in group.hosts:
            group.hosts.append(host_name)

    def generate(self) -> str:
        inventory: Dict[str, Any] = {"all": {"children": {}}}

        # Ungrouped hosts
        ungrouped = []
        grouped_hosts = set()
        for group in self._groups.values():
            grouped_hosts.update(group.hosts)

        for host_name, host in self._hosts.items():
            if host_name not in grouped_hosts:
                ungrouped.append(host_name)

        if ungrouped:
            hosts_dict = {}
            for h_name in ungrouped:
                host = self._hosts[h_name]
                hosts_dict[h_name] = host.host_vars
            inventory["all"]["children"]["ungrouped"] = {"hosts": hosts_dict}

        # Groups
        for group_name, group in self._groups.items():
            group_data: Dict[str, Any] = {}
            if group.hosts:
                hosts_dict = {}
                for h_name in group.hosts:
                    host = self._hosts.get(h_name)
                    if host:
                        hosts_dict[h_name] = host.host_vars
                group_data["hosts"] = hosts_dict
            if group.vars:
                group_data["vars"] = group.vars
            if group.children:
                group_data["children"] = {c: {} for c in group.children}
            inventory["all"]["children"][group_name] = group_data

        return json.dumps(inventory, indent=2)

    def get_host_vars(self, host_name: str) -> Dict[str, Any]:
        host = self._hosts.get(host_name)
        if host is None:
            return {}
        return host.host_vars


# ---------------------------------------------------------------------------
# Variable Manager
# ---------------------------------------------------------------------------

class VariableManager:
    """Manages Ansible variables with precedence."""

    def __init__(self) -> None:
        self._variables: Dict[str, Dict[str, Any]] = {}
        self._scopes: Dict[str, VariableScope] = {}

    def add_variable(self, key: str, value: Any, scope: VariableScope, host: Optional[str] = None, group: Optional[str] = None) -> None:
        scope_key = self._make_scope_key(scope, host, group)
        if scope_key not in self._variables:
            self._variables[scope_key] = {}
        self._variables[scope_key][key] = value

    def _make_scope_key(self, scope: VariableScope, host: Optional[str], group: Optional[str]) -> str:
        if scope == VariableScope.HOST and host:
            return f"host:{host}"
        elif scope == VariableScope.GROUP and group:
            return f"group:{group}"
        return scope.value

    def resolve(self, host_name: str) -> Dict[str, Any]:
        result: Dict[str, Any] = {}

        # Precedence: global < group < host
        for scope_key in ["global", "play", f"group:webservers", f"group:dbservers", f"host:{host_name}"]:
            scope_vars = self._variables.get(scope_key, {})
            result.update(scope_vars)

        return result


# ---------------------------------------------------------------------------
# Playbook Runner (Simulated)
# ---------------------------------------------------------------------------

class PlaybookRunner:
    """Simulates playbook execution for testing."""

    def __init__(self, check_mode: bool = False, diff: bool = False) -> None:
        self.check_mode = check_mode
        self.diff = diff
        self._execution_log: List[Dict[str, Any]] = []

    def run(self, playbook: str, inventory: str, limit: Optional[str] = None) -> PlayResult:
        result = PlayResult(
            play_name="playbook-run",
            hosts_reached=10,
            changed=3,
            ok=7,
            duration_seconds=12.5,
        )
        self._execution_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "playbook": playbook[:50],
            "limit": limit,
            "check_mode": self.check_mode,
        })
        return result

    def get_execution_log(self) -> List[Dict[str, Any]]:
        return self._execution_log


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Ansible Playbooks module."""
    print("=" * 60)
    print("  Ansible Playbooks Module — Demo")
    print("=" * 60)

    # Playbook generation
    gen = PlaybookGenerator(name="web-server-setup", hosts="webservers", become=True)
    gen.add_task(Task(name="Install nginx", module="apt", args={"name": "nginx", "state": "present"}))
    gen.add_task(Task(name="Start nginx", module="service", args={"name": "nginx", "state": "started"}, notify="Restart nginx"))
    gen.add_handler(Handler(name="Restart nginx", module="service", args={"name": "nginx", "state": "restarted"}))
    playbook = gen.generate()
    print(f"\n[+] Playbook Generated ({len(playbook)} chars):")
    print(playbook[:200] + "...")

    # Role generation
    role = RoleGenerator(name="common", description="Base server config")
    role.add_task(RoleTask(name="Install packages", module="apt", args={"name": ["vim", "curl"], "state": "present"}))
    role.set_default("http_port", 80)
    role_structure = role.generate()
    print(f"\n[+] Role Structure: {list(role_structure.keys())}")

    # Inventory
    inventory = InventoryManager()
    inventory.add_host(Host(name="web-01", ansible_host="10.0.1.10", ansible_user="deploy"))
    inventory.add_host(Host(name="web-02", ansible_host="10.0.1.11", ansible_user="deploy"))
    inventory.add_group(Group(name="webservers", hosts=["web-01", "web-02"], vars={"http_port": 80}))
    inv_yaml = inventory.generate()
    print(f"\n[+] Inventory ({len(inv_yaml)} chars):")
    print(inv_yaml[:200] + "...")

    # Variables
    var_mgr = VariableManager()
    var_mgr.add_variable("app_name", "myapp", scope=VariableScope.GLOBAL)
    var_mgr.add_variable("http_port", 80, scope=VariableScope.GROUP, group="webservers")
    resolved = var_mgr.resolve("web-01")
    print(f"\n[+] Resolved Variables for web-01: {resolved}")

    # Runner
    runner = PlaybookRunner(check_mode=True)
    result = runner.run(playbook, inv_yaml)
    print(f"\n[+] Execution Result: {result.to_summary()}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
