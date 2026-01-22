# Agent Template

## Overview

Brief description of what this agent does and the problems it solves.

## Capabilities

- **Capability 1**: Description of first capability
- **Capability 2**: Description of second capability
- **Capability 3**: Description of third capability

## Personality

This agent has the following personality traits:
- **Trait 1**: Description
- **Trait 2**: Description

## Usage

### Basic Example

```python
from agents.$slug.agent import $ClassNameAgent

agent = $ClassNameAgent()
result = agent.execute(task="process", data={"input": "value"})
print(result)
```

### Advanced Example

```python
from agents.$slug.agent import $ClassNameAgent, Config

config = Config(
    api_key="your-api-key",
    timeout=60,
    retries=3
)

agent = $ClassNameAgent(config=config)
response = agent.chat("Your message here")
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | API key for external services | Yes |
| `MODEL` | Model to use | No (default: gpt-4) |
| `TEMPERATURE` | Response creativity | No (default: 0.7) |

### Config Class

```python
@dataclass
class Config:
    """Configuration for the agent."""
    api_key: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 60
```

## API Reference

### $ClassNameAgent

The main agent class.

#### `__init__(config: Optional[Config] = None)`

Initialize the agent.

**Parameters:**
- `config`: Optional configuration object

#### `execute(task: str, data: Dict[str, Any]) -> Dict[str, Any]`

Execute a task.

**Parameters:**
- `task`: Task name
- `data`: Task data

**Returns:** Task result

#### `chat(message: str) -> str`

Chat with the agent.

**Parameters:**
- `message`: User message

**Returns:** Agent response

#### `analyze(input_data: Any) -> AnalysisResult`

Analyze input data.

**Parameters:**
- `input_data`: Data to analyze

**Returns:** Analysis result

## Examples

### Example 1: Task Execution

```python
from agents.$slug.agent import $ClassNameAgent

agent = $ClassNameAgent()
result = agent.execute(
    task="analyze",
    data={"text": "Your text to analyze"}
)
print(result)
```

### Example 2: Conversation

```python
from agents.$slug.agent import $ClassNameAgent

agent = $ClassNameAgent()
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    response = agent.chat(user_input)
    print(f"Agent: {response}")
```

## Integration

This agent can be integrated with:

- **Skill Name**: For enhanced capabilities
- **Other Agent**: For multi-agent workflows

## Performance

| Operation | Latency | Throughput |
|-----------|---------|------------|
| Single request | ~100ms | 10 req/s |
| Batch processing | ~500ms | 2 batches/s |

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.

---

Generated on: $date
