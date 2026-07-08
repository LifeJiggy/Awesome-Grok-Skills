# Operations Agent

> AI-powered business operations and process optimization for modern teams

The Operations Agent is a comprehensive, production-ready Python agent designed to manage, monitor, and optimize business operations. It provides process automation, KPI tracking, workflow execution, analytics, and external system integration out of the box.

## 📁 Project Structure

```
agents/
└── operations/
    ├── agent.py              # Core implementation (~1000 lines)
    ├── GROK.md               # Agent capabilities and usage guide
    ├── ARCHITECTURE.md       # System architecture and design decisions
    ├── README.md             # This file - quick start and overview
    └── tests/                # (Optional) Test files
        ├── test_agent.py
        └── test_optimizer.py
```

## 🚀 Quick Start

Get up and running in under 2 minutes.

### Prerequisites

- Python 3.9 or higher
- No external dependencies required (uses standard library)

### Installation

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd Awesome-Grok-Skills/agents/operations

# Verify Python version
python --version  # Should be 3.9+
```

### Basic Usage

```python
from agent import OperationsManager

# Initialize the operations manager
ops = OperationsManager()

# Define a business process
ops.define_process(
    name="Customer Onboarding",
    steps=["Verify Account", "Send Welcome Email", "Assign Support Agent"],
    owner="Customer Success",
    description="Standard new customer onboarding workflow",
    estimated_duration_minutes=60
)

# Set a KPI target
ops.set_kpi(
    name="Onboarding Time",
    target=45,
    unit="minutes",
    threshold_warning=60.0,
    threshold_critical=90.0
)

# Record a KPI measurement
ops.record_kpi("Onboarding Time", 38)

# View the dashboard
dashboard = ops.get_operations_dashboard()
print(dashboard)
```

### Run the Agent Directly

```bash
python agent.py
```

Expected output:
```
Bottlenecks: [
  {
    "step": "Paperwork",
    "duration": 120,
    "percentage": 48.0,
    "recommendation": "Consider optimizing Paperwork or parallelizing tasks"
  }
]
Automation candidates: ['Paperwork']
Dashboard: {
  "total_processes": 2,
  "active_processes": 0,
  "total_kpis": 2,
  "kpis_in_critical_state": 0,
  ...
}
```

### Interactive CLI

```bash
python -c "from agent import OperationsManager, OperationsCLI; ops = OperationsManager(); cli = OperationsCLI(ops); cli.run()"
```

Available commands:
- `dashboard` - View operations summary
- `kpi` - Record a KPI measurement
- `process` - Define a new process
- `workflow` - Create a new workflow
- `export` - Export state to JSON
- `exit` - Exit the CLI

## 📖 Documentation

### Core Files

| File | Lines | Description |
|------|-------|-------------|
| `agent.py` | ~1000 | Full implementation of the Operations Agent |
| `GROK.md` | ~1000 | Agent capabilities, API docs, usage patterns, best practices |
| `ARCHITECTURE.md` | ~1000 | System architecture, data flow, security, deployment |
| `README.md` | ~1000 | This file - quick start, overview, and navigation |

### Navigation Guide

```
README.md (You are here)
    │
    ├── Quick Start → Run the examples above
    ├── Installation → Set up your environment
    ├── Usage Patterns → Common use cases and code snippets
    ├── API Reference → Detailed method documentation
    ├── Testing → How to run and write tests
    ├── Troubleshooting → Common issues and solutions
    └── Contributing → How to contribute
```

## 💡 Usage Patterns

### Pattern 1: Process Definition & Management

```python
from agent import OperationsManager, ProcessStatus

ops = OperationsManager()

# Define a process with detailed steps
deployment_process = ops.define_process(
    name="Software Deployment",
    steps=[
        "Run Tests",
        "Build Artifact",
        "Deploy to Staging",
        "Smoke Tests",
        "Deploy to Production",
        "Monitor"
    ],
    owner="DevOps Team",
    description="Production deployment workflow",
    estimated_duration_minutes=120
)

# Update process status
ops.update_process_status("Software Deployment", ProcessStatus.ACTIVE)

# Estimate efficiency after execution
ops.estimate_process_efficiency(
    name="Software Deployment",
    actual_duration_minutes=90,
    planned_duration_minutes=120
)
# Returns: {"efficiency": 133.33, "variance": 30.0, ...}
```

### Pattern 2: KPI Monitoring & Alerting

```python
from agent import OperationsManager

ops = OperationsManager()

# Define multiple KPIs with thresholds
kpis = [
    ("Order Fulfillment Time", 24, "hours", 20.0, 30.0),
    ("Customer Satisfaction", 4.5, "score", 3.5, 2.5),
    ("Resource Utilization", 85.0, "%", 70.0, 60.0),
    ("Error Rate", 0.5, "%", 1.0, 2.0)
]

for name, target, unit, warn, crit in kpis:
    ops.set_kpi(name, target, unit, threshold_warning=warn, threshold_critical=crit)

# Record measurements
ops.record_kpi("Order Fulfillment Time", 18.5)
ops.record_kpi("Customer Satisfaction", 4.6)
ops.record_kpi("Resource Utilization", 78.0)  # Triggers warning alert

# Get trend analysis
trend = ops.get_kpi_trend("Order Fulfillment Time", days=30)
print(trend)
# {
#   "kpi": "Order Fulfillment Time",
#   "period_days": 30,
#   "average": 22.5,
#   "min": 18.0,
#   "max": 28.0,
#   "trend": "improving",
#   "data_points": 30
# }
```

### Pattern 3: Workflow Automation

```python
from agent import OperationsManager

ops = OperationsManager()

# Define a workflow
workflow = ops.create_workflow(
    name="Incident Response",
    trigger="incident.created",
    description="Automated incident response workflow",
    actions=[
        {
            "action_id": "notify-oncall",
            "action_type": "notification",
            "parameters": {"channel": "oncall", "priority": "high"},
            "timeout_seconds": 10,
            "retry_count": 3,
            "on_failure": "continue"
        },
        {
            "action_id": "page-team",
            "action_type": "pagerduty",
            "parameters": {"severity": "high"},
            "timeout_seconds": 30,
            "retry_count": 2,
            "on_failure": "stop"
        },
        {
            "action_id": "create-ticket",
            "action_type": "jira",
            "parameters": {"project": "OPS", "priority": "highest"},
            "timeout_seconds": 15,
            "retry_count": 3,
            "on_failure": "continue"
        }
    ]
)

# Execute the workflow
result = ops.execute_workflow("Incident Response", input_payload={"incident_id": "INC-001"})
print(result["overall_status"])  # "success" or "partial_failure"
```

### Pattern 4: Analytics & Reporting

```python
from agent import OperationsManager
from datetime import datetime

ops = OperationsManager()

# Generate a compliance report
compliance_report = ops.generate_compliance_report(
    process_name="Software Deployment",
    standards=["SOC2", "ISO9001"],
    author="compliance_team"
)

# Access report details
print(compliance_report["report_id"])
print(compliance_report["data"]["compliance"])

# List all reports
reports = ops.analytics.list_reports(process_name="Software Deployment")
for report in reports:
    print(f"{report.report_id}: {report.generated_at.isoformat()}")
```

### Pattern 5: Integration Management

```python
from agent import OperationsManager

ops = OperationsManager()

# Register external integrations
ops.register_integration(
    name="warehouse_api",
    config={
        "endpoint": "https://warehouse.internal/v1",
        "auth": {"type": "bearer", "token_ref": "secret://warehouse/api_token"}
    },
    connection_type="api"
)

ops.register_integration(
    name="slack_notifications",
    config={"webhook_url": "https://hooks.slack.com/services/..."},
    connection_type="webhook"
)

# Test connections
ops.integrations.test_connection("warehouse_api")

# Send data to an integration
ops.integrations.send_data(
    integration_name="warehouse_api",
    payload={"order_id": "ORD-123", "items": [...], "priority": "rush"}
)

# List all integrations with status
integrations = ops.integrations.list_integrations()
for integration in integrations:
    print(f"{integration['name']}: connected={integration['connected']}")
```

### Pattern 6: State Persistence

```python
from agent import OperationsManager

ops = OperationsManager()
# ... perform operations ...

# Export state for backup
export_result = ops.export_state("./operational_state_backup.json")
print(f"Exported {export_result['size_bytes']} bytes to {export_result['filepath']}")

# Later, restore state
ops.import_state("./operational_state_backup.json")
# Processes, KPIs, and workflows are restored
```

### Pattern 7: Process Optimization

```python
from agent import ProcessOptimizer

# Analyze existing process for bottlenecks
process_steps = [
    {"name": "Request Review", "estimated_duration_minutes": 15, "manual_review_required": False, "repeatable": True},
    {"name": "Manager Approval", "estimated_duration_minutes": 45, "manual_review_required": True, "repeatable": False},
    {"name": "System Update", "estimated_duration_minutes": 10, "manual_review_required": False, "repeatable": True},
    {"name": "Notification", "estimated_duration_minutes": 5, "manual_review_required": False, "repeatable": True}
]

# Identify bottlenecks
bottlenecks = ProcessOptimizer.calculate_bottlenecks(process_steps)
print("Bottlenecks:", bottlenecks)
# Manager Approval takes 60% of total time - candidate for optimization

# Get automation suggestions
automation_candidates = ProcessOptimizer.suggest_automation(process_steps)
print("Automate these steps:", automation_candidates)
# System Update and Notification are good automation candidates
```

## 🔧 Configuration

### Environment Variables

Set these environment variables to customize agent behavior:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `OPS_STORAGE_PATH` | Persist state to this file path | None (in-memory) | `./ops_state.json` |
| `OPS_NOTIFICATION_CHANNEL` | Default channel for alerts | `operations` | `ops-team` |
| `OPS_ALERT_EMAIL_RECIPIENT` | Email recipient for critical alerts | None | `ops@example.com` |
| `OPS_WORKFLOW_TIMEOUT` | Default action timeout (seconds) | `30` | `60` |
| `OPS_KPI_CRITICAL_THRESHOLD` | Critical threshold multiplier | `0.5` | `0.4` |
| `OPS_KPI_WARNING_THRESHOLD` | Warning threshold multiplier | `0.7` | `0.6` |

### YAML Configuration

Create a `config/operations.yaml` file for comprehensive configuration:

```yaml
# config/operations.yaml
storage:
  filepath: ./data/operations_state.json
  auto_save: true
  save_frequency: minutes

notifications:
  default_channel: operations
  email_enabled: true
  email_smtp: smtp://localhost:25
  slack_webhook: https://hooks.slack.com/services/...

integrations:
  warehouse:
    type: api
    endpoint: https://warehouse.internal/v1
    auth:
      type: bearer
      token_ref: secret://warehouse/api_token
    timeout: 30
    retries: 3

  erp:
    type: database
    connection_string: secret://erp/connection_string
    pool_size: 10

kpis:
  order_fulfillment_time:
    target: 24
    unit: hours
    measurement_frequency: hourly
    thresholds:
      warning: 20
      critical: 30

workflows:
  new_order:
    trigger: order.created
    enabled: true
    actions:
      - type: reserve_inventory
        timeout: 10
        retries: 3
```

Load configuration:
```python
import yaml
from agent import OperationsManager

with open("config/operations.yaml") as f:
    config = yaml.safe_load(f)

ops = OperationsManager(storage_path=config["storage"]["filepath"])
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=agent --cov-report=html

# Run specific test file
python -m pytest tests/test_agent.py -v

# Run specific test
python -m pytest tests/test_agent.py::test_kpi_threshold_calculation -v
```

### Writing Tests

```python
# tests/test_agent.py
import pytest
from agent import OperationsManager, KPI, KPIThreshold, ProcessStatus

@pytest.fixture
def manager():
    return OperationsManager()

def test_process_creation(manager):
    result = manager.define_process(
        name="Test Process",
        steps=["Step 1", "Step 2"],
        owner="Test Team"
    )
    assert result["name"] == "Test Process"
    assert result["total_steps"] == 2
    assert result["owner"] == "Test Team"

def test_kpi_status_calculation():
    kpi = KPI(name="Test", target=100, unit="units", current=30)
    assert kpi.calculate_status() == KPIThreshold.CRITICAL

    kpi.current = 60
    assert kpi.calculate_status() == KPIThreshold.WARNING

    kpi.current = 100
    assert kpi.calculate_status() == KPIThreshold.EXCELLENT

def test_workflow_execution(manager):
    workflow = manager.create_workflow(
        name="Test Workflow",
        trigger="test.trigger",
        actions=[
            {"action_id": "a1", "action_type": "test", "parameters": {}}
        ]
    )
    result = manager.execute_workflow("Test Workflow")
    assert result["overall_status"] == "success"
```

### Test Coverage

```bash
# Generate coverage report
python -m pytest tests/ --cov=agent --cov-report=term-missing
```

## 🔍 Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| `KeyError: Process not found` | Accessing undefined process | Verify process name; list with `ops.processes.keys()` |
| `KeyError: KPI not found` | Recording undefined KPI | Define KPI first with `set_kpi()` |
| `ValueError: Workflow disabled` | Cannot execute disabled workflow | Set `workflow.enabled = True` or recreate |
| `ConnectionError: No active connection` | Sending data to unregistered integration | Call `test_connection()` after `register_integration()` |
| `FileNotFoundError` on import | State file missing | Ensure filepath is correct; use `export_state()` first |
| Empty dashboard | No processes or KPIs defined | Define at least one process and one KPI |

### Debug Mode

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

ops = OperationsManager()
# Debug output will show method calls and state changes
```

### Health Check

```python
def health_check(ops: OperationsManager) -> Dict[str, str]:
    checks = {}
    checks["processes"] = f"{len(ops.processes)} defined"
    checks["kpis"] = f"{len(ops.kpis)} tracked"
    checks["workflows"] = f"{len(ops.workflows)} registered"
    checks["analytics"] = f"{len(ops.analytics.reports)} reports generated"
    checks["integrations"] = f"{len(ops.integrations.integrations)} registered"
    return checks

print(health_check(ops))
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Write** tests for your changes
4. **Ensure** tests pass (`python -m pytest tests/`)
5. **Commit** with descriptive message (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run linter (if configured)
flake8 agent.py
black agent.py
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙋 Support

- **Documentation**: See `GROK.md` and `ARCHITECTURE.md` for detailed docs
- **Issues**: Report bugs via [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: Join community discussions for best practices

---

## 🗺️ Quick Navigation

| Need | Go To |
|------|-------|
| Understand the system | `ARCHITECTURE.md` |
| Learn agent capabilities | `GROK.md` |
| Quick start and examples | This file (`README.md`) |
| Full implementation code | `agent.py` |
| Set up environment | Prerequisites section above |
| Run tests | Testing section above |
| Configure the agent | Configuration section above |

---

*Last updated: 2026-06-04*
*Maintained by: Awesome Grok Skills Community*
