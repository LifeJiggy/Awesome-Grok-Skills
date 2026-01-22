"""
Neural Architecture Search (NAS) Pipeline
Production-ready NAS implementation with PyTorch
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import random


class SearchStrategy(Enum):
    RANDOM = "random"
    BAYESIAN = "bayesian"
    EVOLUTIONARY = "evolutionary"
    DIFFERENTIABLE = "differentiable"


@dataclass
class ArchitectureConfig:
    """Neural architecture configuration"""
    input_channels: int = 3
    num_classes: int = 10
    layers: List[Dict] = None
    use_skip_connections: bool = True
    attention_mechanism: bool = False
    
    def __post_init__(self):
        if self.layers is None:
            self.layers = [
                {"type": "conv", "filters": 32, "kernel": 3, "stride": 1},
                {"type": "pool", "pool_type": "max", "kernel": 2, "stride": 2},
                {"type": "conv", "filters": 64, "kernel": 3, "stride": 1},
                {"type": "pool", "pool_type": "max", "kernel": 2, "stride": 2},
                {"type": "flatten"},
                {"type": "dense", "units": 128, "activation": "relu"},
                {"type": "dense", "units": self.num_classes, "activation": "softmax"}
            ]


class NASSearchSpace:
    """Search space definition for neural architectures"""
    
    def __init__(self):
        self.search_space = {
            "num_blocks": (3, 12),
            "filters_base": (16, 64),
            "filters_multiplier": (1.0, 2.0),
            "kernel_sizes": [3, 5, 7],
            "activation_fn": ["relu", "swish", "mish"],
            "use_se": [True, False],
            "use_skip": [True, False],
            "dropout_rate": (0.0, 0.5),
            "optimizer": ["adam", "sgd", "radam"],
            "learning_rate": (1e-5, 1e-2),
            "batch_size": [32, 64, 128, 256]
        }
    
    def sample(self, strategy: SearchStrategy = SearchStrategy.RANDOM) -> ArchitectureConfig:
        """Sample architecture from search space"""
        num_blocks = random.randint(*self.search_space["num_blocks"])
        filters_base = random.randint(*self.search_space["filters_base"])
        
        layers = []
        current_filters = filters_base
        
        for i in range(num_blocks):
            layer = {
                "type": random.choice(["conv", "depthwise_separable"]),
                "filters": int(current_filters),
                "kernel": random.choice(self.search_space["kernel_sizes"]),
                "stride": 1 if i == 0 else random.choice([1, 2]),
                "activation": random.choice(self.search_space["activation_fn"]),
                "use_bn": True,
                "use_dropout": random.random() < 0.3,
                "dropout_rate": random.uniform(*self.search_space["dropout_rate"])
            }
            layers.append(layer)
            current_filters *= random.uniform(*self.search_space["filters_multiplier"])
        
        return ArchitectureConfig(
            layers=layers,
            use_skip_connections=random.choice(self.search_space["use_skip"]),
            attention_mechanism=random.choice(self.search_space["use_se"])
        )


class ArchitectureEvaluator:
    """Evaluate neural architecture performance"""
    
    def __init__(self, device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.evaluation_history = []
    
    def build_model(self, config: ArchitectureConfig) -> nn.Module:
        """Build PyTorch model from configuration"""
        layers = []
        in_channels = config.input_channels
        
        for layer_config in config.layers:
            layer_type = layer_config["type"]
            
            if layer_type == "conv":
                layers.append(nn.Conv2d(
                    in_channels,
                    layer_config["filters"],
                    kernel_size=layer_config["kernel"],
                    stride=layer_config.get("stride", 1),
                    padding=layer_config["kernel"] // 2
                ))
                if layer_config.get("use_bn", True):
                    layers.append(nn.BatchNorm2d(layer_config["filters"]))
                layers.append(self._get_activation(layer_config["activation"]))
                in_channels = layer_config["filters"]
            
            elif layer_type == "pool":
                pool_type = layer_config.get("pool_type", "max")
                if pool_type == "max":
                    layers.append(nn.MaxPool2d(
                        kernel_size=layer_config["kernel"],
                        stride=layer_config.get("stride", 2)
                    ))
                else:
                    layers.append(nn.AvgPool2d(
                        kernel_size=layer_config["kernel"],
                        stride=layer_config.get("stride", 2)
                    ))
            
            elif layer_type == "dense":
                layers.append(nn.Linear(in_channels, layer_config["units"]))
                layers.append(self._get_activation(layer_config["activation"]))
                in_channels = layer_config["units"]
                if layer_config.get("use_dropout"):
                    layers.append(nn.Dropout(layer_config.get("dropout_rate", 0.3)))
            
            elif layer_type == "flatten":
                layers.append(nn.Flatten())
                in_channels = in_channels * 7 * 7
        
        return nn.Sequential(*layers)
    
    def _get_activation(self, name: str) -> nn.Module:
        """Get activation function by name"""
        activations = {
            "relu": nn.ReLU(),
            "swish": nn.SiLU(),
            "mish": nn.Mish(),
            "gelu": nn.GELU()
        }
        return activations.get(name, nn.ReLU())
    
    def evaluate(self, config: ArchitectureConfig, 
                 train_loader: DataLoader,
                 val_loader: DataLoader,
                 epochs: int = 10) -> Dict:
        """Evaluate architecture performance"""
        model = self.build_model(config).to(self.device)
        
        optimizer = optim.Adam(model.parameters(), lr=1e-3)
        criterion = nn.CrossEntropyLoss()
        
        best_acc = 0.0
        for epoch in range(epochs):
            model.train()
            for batch in train_loader:
                inputs, targets = batch
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
            
            model.eval()
            correct, total = 0, 0
            with torch.no_grad():
                for batch in val_loader:
                    inputs, targets = batch
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    outputs = model(inputs)
                    _, predicted = torch.max(outputs.data, 1)
                    total += targets.size(0)
                    correct += (predicted == targets).sum().item()
            
            accuracy = correct / total
            best_acc = max(best_acc, accuracy)
        
        result = {
            "accuracy": best_acc,
            "params": sum(p.numel() for p in model.parameters()),
            "config": config.__dict__
        }
        self.evaluation_history.append(result)
        return result


class NASPipeline:
    """End-to-end NAS pipeline"""
    
    def __init__(self, search_strategy: SearchStrategy = SearchStrategy.RANDOM):
        self.search_space = NASSearchSpace()
        self.evaluator = ArchitectureEvaluator()
        self.strategy = search_strategy
        self.best_architecture = None
        self.best_accuracy = 0.0
    
    def run(self, train_loader, val_loader, num_samples: int = 20, epochs: int = 10):
        """Run NAS search"""
        results = []
        
        for i in range(num_samples):
            config = self.search_space.sample(self.strategy)
            result = self.evaluator.evaluate(config, train_loader, val_loader, epochs)
            results.append(result)
            
            if result["accuracy"] > self.best_accuracy:
                self.best_accuracy = result["accuracy"]
                self.best_architecture = config
            
            print(f"Sample {i+1}/{num_samples}: Accuracy={result['accuracy']:.4f}, "
                  f"Params={result['params']:,}")
        
        return results


if __name__ == "__main__":
    from torchvision import datasets, transforms
    
    transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(32, padding=4),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    train_dataset = datasets.CIFAR10(root='./data', train=True, 
                                     download=True, transform=transform)
    val_dataset = datasets.CIFAR10(root='./data', train=False, 
                                   transform=transforms.Compose([
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                   ]))
    
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False)
    
    pipeline = NASPipeline(SearchStrategy.RANDOM)
    results = pipeline.run(train_loader, val_loader, num_samples=10, epochs=5)
    
    print(f"\nBest Architecture: {pipeline.best_architecture}")
    print(f"Best Accuracy: {pipeline.best_accuracy:.4f}")
