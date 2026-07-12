---
name: "ansible-playbooks"
category: "iac"
version: "2.0.0"
tags: ["iac", "ansible", "configuration-management", "playbooks", "automation"]
description: "Ansible playbook creation, management, and execution for configuration automation"
---

# Ansible Playbooks

## Overview

The Ansible Playbooks module provides comprehensive automation for configuration management, application deployment, and infrastructure orchestration using Ansible. It enables the creation, management, and execution of playbooks, roles, and inventory configurations across heterogeneous environments. The module supports idempotent operations, role-based organization, variable management, and integration with CI/CD pipelines.

## Core Capabilities

- **Playbook Generation**: Create structured playbooks with tasks, handlers, and roles
- **Role Management**: Organize automation into reusable, shareable roles
- **Inventory Management**: Dynamic and static inventory with host grouping and variable assignment
- **Variable Management**: Hierarchical variable precedence with vault integration
- **Task Orchestration**: Sequential, parallel, and conditional task execution
- **Handler System**: Event-driven tasks triggered by notify directives
- **Template Engine**: Jinja2 template rendering for configuration files
- **Module Library**: Access to 3000+ Ansible modules for system management

## Usage Examples

### Playbook Creation

```python
from ansible_playbooks import PlaybookGenerator, Task, Handler

generator = PlaybookGenerator(
    name="web-server-setup",
    hosts="webservers",
    become=True,
)

# Add tasks
generator.add_task(Task(
    name="Install nginx",
    module="apt",
    args={"name": "nginx", "state": "present", "update_cache": True},
))

generator.add_task(Task(
    name="Deploy nginx config",
    module="template",
    args={
        "src": "templates/nginx.conf.j2",
        "dest": "/etc/nginx/nginx.conf",
        "owner": "root",
        "mode": "0644",
    },
    notify="Restart nginx",
))

generator.add_task(Task(
    name="Ensure nginx is running",
    module="service",
    args={"name": "nginx", "state": "started", "enabled": True},
))

# Add handlers
generator.add_handler(Handler(
    name="Restart nginx",
    module="service",
    args={"name": "nginx", "state": "restarted"},
))

# Generate playbook
playbook = generator.generate()
print(playbook)
```

### Role Creation

```python
from ansible_playbooks import RoleGenerator, RoleTask

role_gen = RoleGenerator(
    name="common",
    description="Common server configuration",
)

# Add tasks
role_gen.add_task(RoleTask(
    name="Update apt cache",
    module="apt",
    args={"update_cache": True, "cache_valid_time": 3600},
))

role_gen.add_task(RoleTask(
    name="Install base packages",
    module="apt",
    args={
        "name": ["vim", "curl", "wget", "htop", "net-tools"],
        "state": "present",
    },
))

role_gen.add_task(RoleTask(
    name="Configure timezone",
    module="timezone",
    args={"name": "UTC"},
))

# Generate role structure
role_structure = role_gen.generate()
print(f"Role structure: {list(role_structure.keys())}")
```

### Inventory Management

```python
from ansible_playbooks import InventoryManager, Host, Group

inventory = InventoryManager()

# Add hosts
inventory.add_host(Host(
    name="web-01",
    ansible_host="10.0.1.10",
    ansible_user="deploy",
    ansible_ssh_private_key_file="~/.ssh/id_rsa",
))

# Add groups
inventory.add_group(Group(
    name="webservers",
    hosts=["web-01", "web-02"],
    vars={"http_port": 80, "https_port": 443},
))

inventory.add_group(Group(
    name="dbservers",
    hosts=["db-01", "db-02"],
    vars={"mysql_port": 3306},
))

# Generate inventory
inv_yaml = inventory.generate()
print(inv_yaml)
```

### Variable Management

```python
from ansible_playbooks import VariableManager, VariableScope

var_manager = VariableManager()

# Add global variables
var_manager.add_variable("app_name", "myapp", scope=VariableScope.GLOBAL)
var_manager.add_variable("app_version", "2.1.0", scope=VariableScope.GLOBAL)

# Add group variables
var_manager.add_variable("http_port", 80, scope=VariableScope.GROUP, group="webservers")
var_manager.add_variable("mysql_port", 3306, scope=VariableScope.GROUP, group="dbservers")

# Add host variables
var_manager.add_variable("ansible_host", "10.0.1.10", scope=VariableScope.HOST, host="web-01")

# Resolve variables with precedence
resolved = var_manager.resolve("web-01")
print(f"Variables for web-01: {resolved}")
```

## Best Practices

- **Idempotency**: Design tasks to be idempotent; running them multiple times should produce the same result
- **Role Organization**: Use roles to organize related tasks, handlers, and templates
- **Variable Precedence**: Understand and document variable precedence to avoid surprises
- **Vault for Secrets**: Use Ansible Vault for sensitive data; never commit plaintext secrets
- **Tags for Selective Execution**: Use tags to enable partial playbook execution
- **Handler Efficiency**: Use handlers for service restarts to avoid unnecessary restarts
- **Testing**: Test playbooks in development before applying to production
- **Documentation**: Document playbook purpose, variables, and expected outcomes

## Related Modules

- **terraform-cloudformation**: Infrastructure provisioning for Ansible to configure
- **cloud-deployment**: Deployment orchestration combining IaC and configuration management
- **drift-detection**: Verify configuration state after Ansible execution
