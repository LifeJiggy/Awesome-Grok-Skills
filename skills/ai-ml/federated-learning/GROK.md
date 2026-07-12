---
name: "federated-learning"
category: "ai-ml"
version: "2.0.0"
tags: ["ai-ml", "federated-learning", "privacy", "distributed", "differential-privacy", "secure-aggregation"]
---

# Federated Learning

## Overview

Privacy-preserving federated learning framework for training machine learning models across decentralized data sources without sharing raw data. This module implements FedAvg, FedProx, Scaffold, and personalized federated learning algorithms with built-in differential privacy, secure aggregation, communication compression, and heterogeneous device management. Supports cross-silo (enterprise) and cross-device (mobile/IoT) federated learning topologies with Byzantine-robust aggregation and non-IID data handling.

## Core Capabilities

- **Federated Averaging (FedAvg)**: Standard federated averaging with configurable local epochs and learning rate schedules
- **FedProx**: Proximal term regularization for handling heterogeneous data distributions across clients
- **SCAFFOLD**: Variance-reduced federated learning with client control variates
- **Differential Privacy**: (ε, δ)-differential privacy with per-round and cumulative privacy accounting
- **Secure Aggregation**: Cryptographic secure aggregation preventing server from seeing individual client updates
- **Communication Compression**: Gradient compression via top-k sparsification, quantization, and error feedback
- **Byzantine Robustness**: Robust aggregation rules (Krum, trimmed mean, median) for hostile client detection
- **Personalization**: Per-client model personalization via meta-learning, local fine-tuning, and mixture-of-experts

## Usage

```python
from federated_learning import (
    FederatedServer, FederatedClient, FedAlgorithm, PrivacyBudget
)

# Configure federated learning server
server = FederatedServer(
    algorithm=FedAlgorithm.FEDAVG,
    global_model="resnet50",
    num_rounds=100,
    clients_per_round=10,
    min_clients=5,
    rounds_before_exit=10,
)

# Configure privacy
server.configure_privacy(
    epsilon=8.0,
    delta=1e-5,
    max_grad_norm=1.0,
    noise_multiplier=1.1,
)

# Add clients
for i in range(50):
    server.add_client(
        client_id=f"client_{i}",
        data_samples=1000 + i * 100,
        compute_power="medium",
        connection_type="wifi",
    )

# Run federated training
result = server.train()
print(f"Global accuracy: {result.final_accuracy:.4f}")
print(f"Communication rounds: {result.total_rounds}")
print(f"Privacy spent: ε={result.privacy_spent.epsilon:.2f}, δ={result.privacy_spent.delta:.2e}")
print(f"Total communication: {result.total_communication_mb:.1f} MB")
```

```python
# Federated client
client = FederatedClient(
    client_id="client_0",
    local_data="data/client_0/",
    local_epochs=5,
    learning_rate=0.01,
    batch_size=32,
)
client.train_local(global_model)
update = client.get_update()
print(f"Local accuracy: {update.local_accuracy:.4f}")
print(f"Update size: {update.update_size_mb:.2f} MB")
```

## Best Practices

- Use FedProx or SCAFFOLD when data is non-IID across clients — FedAvg struggles with heterogeneous data
- Set differential privacy budget (ε) before training starts — privacy loss is cumulative across rounds
- Use secure aggregation when client updates could reveal sensitive information about local data
- Compress gradients for cross-device FL where bandwidth is limited (top-k sparsification works well)
- Monitor for Byzantine clients using Krum or trimmed mean aggregation in open federation settings
- Start with 10-20% of clients per round to balance communication cost and convergence speed
- Use learning rate warmup for the first 5-10 rounds to stabilize early training
- Implement early stopping based on validation accuracy on a small shared held-out dataset
- Log per-client metrics to detect free-riders and stragglers in the federation
- Use FedBN (federated batch normalization) when local batch statistics vary significantly across clients

## Related Modules

- **model-optimization** — Compress federated updates for efficient communication
- **model-deployment** — Deploy federated models to edge devices
- **ai-ml** → **neural-architecture-search** — Federated NAS for privacy-preserving architecture search
- **api-security** — Secure communication channels for federated coordination
- **zero-trust** → **security-framework** — Zero-trust principles for federated infrastructure
