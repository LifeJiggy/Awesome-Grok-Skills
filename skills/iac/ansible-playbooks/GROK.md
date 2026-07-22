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

---

## Advanced Configuration

### Ansible Vault Integration

```yaml
# encrypted_vars.yml
ansible_become_pass: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  66386134646432616264353531396437356130323465336431383936613333
  64333164376535626534333139353638643832363331653936633361653066
```

### Complex Conditionals

```yaml
- name: Install based on OS
  ansible.builtin.package:
    name: "{{ item }}"
    state: present
  loop: "{{ packages }}"
  when:
    - ansible_os_family == "Debian"
    - ansible_distribution_major_version | int >= 10
    - deploy_environment == "production"
```

### Custom Callback Plugins

```python
# callback_plugins/custom_logger.py
class CallbackModule:
    def v2_runner_on_ok(self, result):
        print(f"Task {result._task.get_name()} completed on {result._host.name}")

    def v2_runner_on_failed(self, result, ignore_errors=False):
        print(f"Task FAILED on {result._host.name}: {result._result.get('msg')}")
```

### Inventory Plugins

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - eu-west-1
filters:
  tag:Environment: production
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.availability_zone
    prefix: az
```

### Jinja2 Advanced Templates

```jinja2
{# templates/nginx.conf.j2 #}
{% for server in upstream_servers %}
server {{ server.host }}:{{ server.port }} weight={{ server.weight | default(1) }};
{% endfor %}

{% if ssl_enabled %}
listen 443 ssl;
ssl_certificate /etc/ssl/{{ ssl_cert_name }}.pem;
{% endif %}
```

### Role Dependencies

```yaml
# roles/webserver/meta/main.yml
dependencies:
  - role: common
  - role: firewall
    vars:
      firewall_allowed_ports:
        - 80
        - 443
  - role: monitoring
    when: enable_monitoring | default(false)
```

### Custom Modules

```python
# library/custom_package.py
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', choices=['present', 'absent']),
        ),
    )
    # Module logic here
    module.exit_json(changed=False, msg="Success")

if __name__ == '__main__':
    main()
```

## Architecture Patterns

### Layered Architecture

```
playbooks/
├── site.yml              # Master playbook
├── webservers.yml        # Web server role
├── dbservers.yml         # Database role
├── monitoring.yml        # Monitoring role
└── roles/
    ├── common/           # Base configuration
    ├── webserver/        # Web server configuration
    ├── database/         # Database configuration
    └── monitoring/       # Monitoring setup
```

### Environment-Based Structure

```
environments/
├── development/
│   ├── group_vars/
│   │   └── all.yml
│   └── host_vars/
├── staging/
│   ├── group_vars/
│   └── host_vars/
└── production/
    ├── group_vars/
    └── host_vars/
```

### Microservices Playbook Pattern

```yaml
# microservices.yml
- name: Deploy microservices
  hosts: "{{ target_service }}"
  roles:
    - common
    - docker
    - "{{ service_role }}"
    - monitoring
  vars:
    service_port: "{{ lookup('env', 'SERVICE_PORT') }}"
```

### Blue-Green Deployment Pattern

```yaml
# blue-green.yml
- name: Deploy to green
  hosts: green
  roles:
    - deploy
    - verify

- name: Switch traffic
  hosts: loadbalancer
  tasks:
    - name: Update upstream
      template:
        src: upstream.conf.j2
        dest: /etc/nginx/conf.d/upstream.conf
      notify: Reload nginx
```

### Rolling Update Pattern

```yaml
# rolling_update.yml
- name: Rolling update
  hosts: webservers
  serial: 1
  max_fail_percentage: 10
  roles:
    - deploy
    - verify
```

## Integration Guide

### CI/CD Integration

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - deploy

ansible-lint:
  stage: lint
  image: cytopia/ansible-lint
  script:
    - ansible-lint playbooks/

ansible-test:
  stage: test
  image: cytopia/ansible
  script:
    - ansible-playbook --check playbooks/site.yml

ansible-deploy:
  stage: deploy
  script:
    - ansible-playbook playbooks/site.yml
  only:
    - main
```

### Terraform Integration

```yaml
- name: Configure Terraform-managed infrastructure
  hosts: "{{ groups['terraform_managed'] }}"
  tasks:
    - name: Get Terraform outputs
      delegate_to: localhost
      shell: terraform output -json
      register: tf_output

    - name: Apply configuration
      template:
        src: app.conf.j2
        dest: /etc/app/config.conf
```

### Docker Integration

```yaml
- name: Deploy to Docker hosts
  hosts: docker_hosts
  roles:
    - docker
  tasks:
    - name: Pull latest image
      docker_image:
        name: "{{ app_image }}"
        tag: "{{ app_tag }}"
        state: present

    - name: Start container
      docker_container:
        name: "{{ app_name }}"
        image: "{{ app_image }}:{{ app_tag }}"
        state: started
```

### Kubernetes Integration

```yaml
- name: Deploy to Kubernetes
  hosts: localhost
  tasks:
    - name: Apply manifests
      kubernetes.core.k8s:
        state: present
        src: "{{ item }}"
      loop:
        - manifests/deployment.yml
        - manifests/service.yml
        - manifests/ingress.yml
```

### Monitoring Stack Integration

```yaml
- name: Configure monitoring
  hosts: monitoring
  roles:
    - prometheus
    - grafana
    - alertmanager
  vars:
    alertmanager_slack_webhook: "{{ vault_slack_webhook }}"
```

## Performance Optimization

### Parallel Execution

```bash
# Run with increased parallelism
ansible-playbook site.yml -f 50

# Fork limit per host group
ansible-playbook site.yml -f 20 --limit webservers
```

### Async Tasks

```yaml
- name: Long running task
  ansible.builtin.command: /opt/scripts/long_task.sh
  async: 3600
  poll: 0
  register: async_result

- name: Wait for completion
  async_status:
    jid: "{{ async_result.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 60
  delay: 60
```

### Fact Caching

```ini
# ansible.cfg
[defaults]
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts_cache
fact_caching_timeout = 3600
```

### Strategy Optimization

```yaml
- name: Optimized playbook
  hosts: all
  strategy: free  # Or 'linear' for sequential
  serial: "30%"
  gather_facts: false  # Disable if not needed
```

### Connection Optimization

```ini
# ansible.cfg
[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
control_path_dir = /tmp/.ansible/cp
```

### Module Caching

```ini
[defaults]
gathering = smart
fact_caching = redis
fact_caching_timeout = 86400
```

## Security Considerations

### Ansible Vault for Secrets

```bash
# Create encrypted file
ansible-vault create secrets.yml

# Encrypt existing file
ansible-vault encrypt vars/secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# Run with vault password
ansible-playbook site.yml --ask-vault-pass
```

### SSH Security

```yaml
# Disable password authentication
- name: Harden SSH
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "{{ item.regexp }}"
    line: "{{ item.line }}"
  loop:
    - { regexp: '^#?PasswordAuthentication', line: 'PasswordAuthentication no' }
    - { regexp: '^#?PermitRootLogin', line: 'PermitRootLogin no' }
    - { regexp: '^#?Protocol', line: 'Protocol 2' }
  notify: Restart sshd
```

### Privilege Escalation Controls

```yaml
- name: Run with become
  hosts: all
  become: true
  become_method: sudo
  become_user: root
  vars:
    ansible_become_pass: "{{ vault_sudo_password }}"
```

### Inventory Security

```ini
# Ensure inventory is not world-readable
[defaults]
inventory_permissions = 0o600
```

### Network Security

```yaml
- name: Configure firewall
  ansible.builtin.ufw:
    rule: allow
    port: "{{ item }}"
    proto: tcp
  loop:
    - "22"
    - "80"
    - "443"
```

### Secrets Rotation

```yaml
- name: Rotate database password
  community.mysql.mysql_user:
    name: app_user
    password: "{{ new_db_password }}"
    login_password: "{{ old_db_password }}"
    state: present
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| SSH connection refused | Firewall blocking port 22 | Check firewall rules |
| Permission denied | Wrong become credentials | Verify sudo password |
| Module not found | Missing collection | `ansible-galaxy collection install <name>` |
| Variable undefined | Precedence issue | Check variable scope and precedence |
| Task timeout | Slow network or service | Increase timeout or check connectivity |
| Handler not triggered | Notify name mismatch | Verify handler name matches notify |
| Connection timeout | SSH keepalive issue | Set `ssh_args` in config |

### Debug Mode

```bash
# Increase verbosity
ansible-playbook site.yml -vvv

# Debug specific task
ansible-playbook site.yml -vvvv --step

# Check mode (dry run)
ansible-playbook site.yml --check
```

### Connection Debugging

```bash
# Test connectivity
ansible all -m ping

# Gather facts
ansible all -m setup

# Check SSH
ansible all -m shell -a "echo hello" --timeout 10
```

### Variable Debugging

```yaml
- name: Debug variables
  ansible.builtin.debug:
    var: hostvars[inventory_hostname]
    verbosity: 1
```

### Task Failure Analysis

```yaml
- name: Handle errors
  block:
    - name: Risky task
      ansible.builtin.command: /opt/risky.sh
  rescue:
    - name: Handle failure
      ansible.builtin.debug:
        msg: "Task failed, running recovery"
  always:
    - name: Cleanup
      ansible.builtin.file:
        path: /tmp/work
        state: absent
```

## API Reference

### PlaybookGenerator

```python
class PlaybookGenerator:
    def __init__(self, name: str, hosts: str, become: bool = False):
        """Initialize playbook generator."""

    def add_task(self, task: Task) -> None:
        """Add task to playbook."""

    def add_handler(self, handler: Handler) -> None:
        """Add handler to playbook."""

    def add_role(self, role: str, vars: dict = None) -> None:
        """Add role to playbook."""

    def generate(self) -> str:
        """Generate YAML playbook string."""
```

### Task

```python
@dataclass
class Task:
    name: str
    module: str
    args: Dict[str, Any]
    when: str = None
    notify: str = None
    become: bool = False
    tags: List[str] = None
    loop: List[Any] = None
```

### RoleGenerator

```python
class RoleGenerator:
    def __init__(self, name: str, description: str = ""):
        """Initialize role generator."""

    def add_task(self, task: RoleTask) -> None:
        """Add task to role."""

    def add_handler(self, handler: Handler) -> None:
        """Add handler to role."""

    def add_template(self, name: str, content: str) -> None:
        """Add template to role."""

    def generate(self) -> Dict[str, Any]:
        """Generate role directory structure."""
```

### InventoryManager

```python
class InventoryManager:
    def __init__(self):
        """Initialize inventory manager."""

    def add_host(self, host: Host) -> None:
        """Add host to inventory."""

    def add_group(self, group: Group) -> None:
        """Add group to inventory."""

    def generate(self) -> str:
        """Generate inventory YAML."""
```

### VariableManager

```python
class VariableManager:
    def __init__(self):
        """Initialize variable manager."""

    def add_variable(self, name: str, value: Any, scope: VariableScope,
                     host: str = None, group: str = None) -> None:
        """Add variable with scope."""

    def resolve(self, host: str) -> Dict[str, Any]:
        """Resolve all variables for a host."""
```

## Data Models

### Playbook

```python
@dataclass
class Playbook:
    name: str
    hosts: str
    become: bool
    tasks: List[Task]
    handlers: List[Handler]
    roles: List[Role]
    vars: Dict[str, Any]
    pre_tasks: List[Task] = None
    post_tasks: List[Task] = None
```

### Task

```python
@dataclass
class Task:
    name: str
    module: str
    args: Dict[str, Any]
    when: str = None
    notify: str = None
    become: bool = False
    become_user: str = None
    tags: List[str] = None
    loop: List[Any] = None
    register: str = None
    retries: int = None
    delay: int = None
    timeout: int = None
```

### Handler

```python
@dataclass
class Handler:
    name: str
    module: str
    args: Dict[str, Any]
    listen: str = None
    tags: List[str] = None
```

### Host

```python
@dataclass
class Host:
    name: str
    ansible_host: str = None
    ansible_user: str = None
    ansible_ssh_private_key_file: str = None
    ansible_port: int = None
    vars: Dict[str, Any] = None
```

### Group

```python
@dataclass
class Group:
    name: str
    hosts: List[str]
    vars: Dict[str, Any] = None
    children: List[str] = None
```

### Inventory

```python
@dataclass
class Inventory:
    hosts: List[Host]
    groups: List[Group]
    group_vars: Dict[str, Dict] = None
    host_vars: Dict[str, Dict] = None
```

### VariableScope

```python
class VariableScope(Enum):
    GLOBAL = "global"
    GROUP = "group"
    HOST = "host"
    PLAY = "play"
    TASK = "task"
```

## Deployment Guide

### Environment Promotion

```yaml
# promote.yml
- name: Promote from staging to production
  hosts: localhost
  vars:
    promote_from: staging
    promote_to: production
  tasks:
    - name: Run production playbook
      ansible.builtin.include_playbook: site.yml
      vars:
        target_env: "{{ promote_to }}"
```

### Rolling Deployment

```bash
# Deploy to 25% at a time
ansible-playbook deploy.yml -e "batch_size=25%"

# Deploy to specific subset
ansible-playbook deploy.yml --limit "webservers[0:2]"
```

### Health Check Integration

```yaml
- name: Post-deploy health check
  ansible.builtin.uri:
    url: "http://{{ ansible_host }}:{{ app_port }}/health"
    status_code: 200
  retries: 10
  delay: 5
```

### Rollback Procedures

```yaml
# rollback.yml
- name: Rollback deployment
  hosts: "{{ target_hosts }}"
  tasks:
    - name: Restore previous version
      ansible.builtin.package:
        name: "{{ app_name }}"
        state: "{{ previous_version }}"

    - name: Restart service
      ansible.builtin.service:
        name: "{{ app_name }}"
        state: restarted
```

## Monitoring & Observability

### Ansible Callback Plugin for Monitoring

```python
# callback_plugins/metrics.py
import time

class CallbackModule:
    def __init__(self):
        self.start_time = None
        self.task_times = []

    def v2_playbook_on_start(self, playbook):
        self.start_time = time.time()

    def v2_runner_on_ok(self, result):
        elapsed = time.time() - self.start_time
        self.task_times.append({
            'task': result._task.get_name(),
            'host': result._host.name,
            'elapsed': elapsed,
        })
```

### Logging Configuration

```ini
# ansible.cfg
[defaults]
log_path = /var/log/ansible/playbook.log
callback_whitelist = timer, profile_tasks
```

### Metrics Collection

```yaml
- name: Collect deployment metrics
  ansible.builtin.uri:
    url: "https://metrics.internal/api/v1/deploy"
    method: POST
    body:
      environment: "{{ deploy_env }}"
      version: "{{ app_version }}"
      timestamp: "{{ ansible_date_time.iso8601 }}"
      status: "success"
    body_format: json
```

### Alert Integration

```yaml
- name: Send alert on failure
  ansible.builtin.uri:
    url: "https://hooks.slack.com/xxx"
    method: POST
    body:
      text: "Deployment FAILED on {{ inventory_hostname }}"
    body_format: json
  when: deployment_failed | default(false)
```

## Testing Strategy

### Molecule Testing

```yaml
# molecule/default/molecule.yml
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: geerlingguy/docker-debian12-ansible
    command: ""
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:rw
    privileged: true
provisioner:
  name: ansible
verifier:
  name: ansible
```

### Test Playbooks

```yaml
# test.yml
- name: Test role
  hosts: localhost
  roles:
    - my_role
  post_tasks:
    - name: Verify nginx is running
      ansible.builtin.service:
        name: nginx
        state: started
      register: nginx_status

    - name: Assert nginx is running
      ansible.builtin.assert:
        that:
          - nginx_status.status.ActiveState == "active"
```

### Idempotency Testing

```bash
# Run twice and check for changes
ansible-playbook site.yml --check
ansible-playbook site.yml --check  # Second run should show no changes
```

### Lint Testing

```yaml
# .ansible-lint
exclude_paths:
  - .git/
  - molecule/
rules:
  enable:
    - yaml[line-length]
  disable:
    - name[missing]
```

## Versioning & Migration

### Role Versioning

```yaml
# roles/myrole/meta/main.yml
galaxy_info:
  role_name: myrole
  version: "2.1.0"
  min_ansible_version: "2.14"
```

### Collection Versioning

```yaml
# galaxy.yml
namespace: myorg
name: mycollection
version: 1.2.3
dependencies:
  - community.general: ">=6.0.0"
```

### Migration Strategy

```python
migration_steps = {
    "1.x_to_2.x": [
        "Update variable names",
        "Replace deprecated modules",
        "Update role dependencies",
    ],
    "2.x_to_3.x": [
        "Migrate to collections",
        "Update inventory plugins",
        "Replace lookup plugins",
    ],
}
```

## Glossary

| Term | Definition |
|------|------------|
| **Playbook** | YAML file defining automation tasks |
| **Role** | Reusable collection of tasks, handlers, and templates |
| **Task** | Single unit of automation |
| **Handler** | Task triggered by notify directive |
| **Module** | Unit of code that manages system resources |
| **Inventory** | List of hosts to manage |
| **Group** | Collection of hosts with shared variables |
| **Vault** | Ansible's encrypted data storage |
| **Galaxy** | Ansible's package repository |
| **Facts** | System information gathered from hosts |
| **Variables** | Dynamic values used in playbooks |
| **Idempotency** | Running same playbook produces same result |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with collection support |
| 1.5.0 | 2024-11-01 | Added custom module support |
| 1.4.0 | 2024-09-15 | Molecule testing integration |
| 1.3.0 | 2024-07-20 | Vault improvements |
| 1.2.0 | 2024-05-10 | Inventory plugin support |
| 1.1.0 | 2024-03-01 | Performance optimizations |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow Ansible coding standards
2. Write Molecule tests for new roles
3. Use ansible-lint before submitting
4. Document all variables and defaults
5. Include examples in role documentation
6. Test with multiple Ansible versions
7. Update changelog for new features

## License

MIT License. See LICENSE file for full terms.
