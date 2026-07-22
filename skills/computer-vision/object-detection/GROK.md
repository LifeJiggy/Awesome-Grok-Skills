---
name: "object-detection"
category: "computer-vision"
version: "2.0.0"
tags: ["computer-vision", "object-detection", "YOLO", "R-CNN", "detection"]
---

# Object Detection

## Overview

The Object Detection module provides tools for detecting and localizing objects in images and video. It covers classical detection methods (Haar cascades, HOG+SVM), deep learning detectors (YOLO, SSD, Faster R-CNN, EfficientDet), anchor-free methods (CenterNet, FCOS), and transformer-based detectors (DETR). The module includes model selection guidance, training pipelines, post-processing (NMS), and deployment optimization.

This skill is essential for computer vision engineers building detection systems for autonomous vehicles, surveillance, manufacturing QA, retail analytics, and medical imaging.

## Core Capabilities

- **Classical Detectors**: Haar cascades, HOG+SVM, template matching, and sliding window approaches
- **One-Stage Detectors**: YOLOv5/v8, SSD, RetinaNet, and EfficientDet for real-time detection
- **Two-Stage Detectors**: Faster R-CNN, Mask R-CNN, and Cascade R-CNN for high-accuracy detection
- **Anchor-Free Detectors**: CenterNet, FCOS, CornerNet, and PointPillars for 3D detection
- **Transformer Detectors**: DETR, Deformable DETR, and DINO for end-to-end detection
- **Post-Processing**: Non-Maximum Suppression (NMS), Soft-NMS, confidence thresholding
- **Training**: Data augmentation, transfer learning, anchor optimization, and loss functions
- **Deployment**: TensorRT, ONNX, CoreML, and quantization for edge deployment

## Usage Examples

```python
from object_detection import (
    DetectorFactory,
    NMSProcessor,
    AnchorOptimizer,
    TrainingPipeline,
    DeploymentOptimizer,
)

# --- Create Detector ---
factory = DetectorFactory()
detector = factory.create(
    model="yolov8",
    num_classes=80,
    input_size=640,
    confidence_threshold=0.5,
)

# --- Run Detection ---
results = detector.detect(image)
for det in results.detections:
    print(f"  {det.class_name}: {det.confidence:.2f}")
    print(f"    BBox: [{det.x1:.0f}, {det.y1:.0f}, {det.x2:.0f}, {det.y2:.0f}]")

# --- NMS ---
nms = NMSProcessor(iou_threshold=0.5)
filtered = nms.process(results.detections)
print(f"After NMS: {len(filtered)} detections")

# --- Anchor Optimization ---
optimizer = AnchorOptimizer()
anchors = optimizer.optimize(
    dataset="coco",
    input_size=640,
    num_anchors_per_level=3,
)
print(f"Optimized anchors: {len(anchors)} anchors across {len(set(a.level for a in anchors))} levels")

# --- Training Pipeline ---
pipeline = TrainingPipeline()
config = pipeline.create_config(
    model="yolov8",
    dataset="custom_dataset",
    epochs=100,
    batch_size=16,
    lr0=0.01,
    augmentations=["mosaic", "mixup", "hsv"],
)
print(f"Training config: {config.epochs} epochs, batch {config.batch_size}")

# --- Deployment ---
deployer = DeploymentOptimizer()
optimized = deployer.optimize(
    model_path="best.pt",
    target="tensorrt",
    precision="fp16",
    input_shape=(1, 3, 640, 640),
)
print(f"Optimized model: {optimized.output_path}")
print(f"Speed improvement: {optimized.speedup:.1f}x")
```

## Best Practices

- Use YOLOv8 for real-time applications requiring >30 FPS on edge devices
- Use Faster R-CNN or DETR when accuracy is more important than speed
- Apply mosaic augmentation for small object detection improvement
- Use anchor-free methods when object aspect ratios vary significantly
- Always evaluate with mAP@0.5:0.95 (COCO metric), not just mAP@0.5
- Balance dataset classes — use oversampling or class weights for imbalanced data
- Apply test-time augmentation (TTA) for production accuracy improvement
- Use ONNX export for cross-platform deployment compatibility
- Quantize to INT8 for edge deployment with <1% mAP loss typically
- Monitor for class imbalance — models learn majority classes better

## Related Modules

- **image-processing**: Pre-processing and augmentation for detection
- **face-recognition**: Face-specific detection and recognition
- **ocr**: Text detection in images
- **video-analysis**: Frame-by-frame detection in video streams

## Advanced Configuration

### Model Configuration

```yaml
detection:
  model: "yolov8"
  input_size: 640
  confidence_threshold: 0.5
  nms_threshold: 0.45
  num_classes: 80
  device: "cuda:0"
  half_precision: true
  batch_size: 16
```

### Training Configuration

```yaml
training:
  epochs: 100
  batch_size: 16
  learning_rate: 0.01
  optimizer: "SGD"
  momentum: 0.937
  weight_decay: 0.0005
  lr0: 0.01
  lrf: 0.01
  warmup_epochs: 3
  warmup_momentum: 0.8
  warmup_bias_lr: 0.1
  augmentations:
    - "mosaic"
    - "mixup"
    - "hsv"
    - "flip"
    - "scale"
```

### Deployment Configuration

```yaml
deployment:
  target: "tensorrt"
  precision: "fp16"
  max_batch_size: 16
  workspace_size_gb: 4
  enable_dynamic_shapes: false
  input_shape: [1, 3, 640, 640]
```

## Architecture Patterns

### Detection Architecture Comparison

```
One-Stage Detectors:
├── YOLO Series (YOLOv5, v8)
│   ├── Single pass detection
│   ├── Real-time capable
│   └── Good for edge deployment
├── SSD
│   ├── Multi-scale feature maps
│   ├── Anchor-based
│   └── Moderate accuracy
└── RetinaNet
    ├── Focal loss
    ├── Better class imbalance
    └── Higher accuracy than SSD

Two-Stage Detectors:
├── Faster R-CNN
│   ├── Region proposal network
│   ├── High accuracy
│   └── Slower inference
├── Mask R-CNN
│   ├── Instance segmentation
│   ├── Pixel-level masks
│   └── Higher compute cost
└── Cascade R-CNN
    ├── Multi-stage refinement
    ├── Best accuracy
    └── Slowest inference

Anchor-Free Detectors:
├── CenterNet
│   ├── Keypoint-based
│   ├── Simple design
│   └── Fast inference
├── FCOS
│   ├── Fully convolutional
│   ├── No anchor tuning
│   └── Good generalization
└── CornerNet
    ├── Corner detection
    ├── Bottom-up grouping
    └── Novel approach

Transformer Detectors:
├── DETR
│   ├── End-to-end detection
│   ├── Set prediction
│   └── No NMS needed
├── Deformable DETR
│   ├── Deformable attention
│   ├── Faster convergence
│   └── Better small objects
└── DINO
    ├── Contrastive learning
    ├── State-of-the-art
    └── Higher compute cost
```

### NMS (Non-Maximum Suppression)

```
NMS Process:
├── 1. Sort detections by confidence
├── 2. Select highest confidence detection
├── 3. Remove all IoU > threshold
├── 4. Repeat until no detections remain
└── Output: Filtered detections

NMS Variants:
├── Standard NMS
├── Soft-NMS (score decay)
├── DIoU-NMS
└── CIoU-NMS
```

## Integration Guide

### YOLOv8 Integration

```python
from ultralytics import YOLO

# Load model
model = YOLO('yolov8n.pt')

# Run detection
results = model('image.jpg')

# Process results
for r in results:
    boxes = r.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        conf = box.conf[0]
        cls = box.cls[0]
        print(f"Class: {model.names[int(cls)]}, Conf: {conf:.2f}")
```

### ONNX Runtime Integration

```python
import onnxruntime as ort
import numpy as np

# Load model
session = ort.InferenceSession('model.onnx')

# Prepare input
input_data = preprocess('image.jpg')
input_name = session.get_inputs()[0].name

# Run inference
outputs = session.run(None, {input_name: input_data})

# Process outputs
detections = postprocess(outputs)
```

### TensorRT Integration

```python
import tensorrt as trt
import pycuda.driver as cuda

# Load engine
logger = trt.Logger(trt.Logger.WARNING)
with open('model.trt', 'rb') as f:
    runtime = trt.Runtime(logger)
    engine = runtime.deserialize_cuda_engine(f.read())

# Create context
context = engine.create_execution_context()
```

## Performance Optimization

### Inference Speed

| Model | FPS (GPU) | FPS (CPU) | mAP@0.5 | mAP@0.5:0.95 |
|-------|-----------|-----------|---------|---------------|
| YOLOv8n | 300+ | 30 | 52.0 | 37.3 |
| YOLOv8s | 200+ | 20 | 61.0 | 44.9 |
| YOLOv8m | 100+ | 10 | 65.0 | 50.2 |
| YOLOv8l | 60+ | 5 | 68.0 | 52.9 |
| YOLOv8x | 30+ | 2 | 69.0 | 53.9 |

### Optimization Techniques

```
Optimization Pipeline:
├── Model Optimization
│   ├── Pruning (remove redundant weights)
│   ├── Quantization (FP32 → INT8)
│   ├── Knowledge distillation
│   └── Architecture search
├── Inference Optimization
│   ├── TensorRT (NVIDIA)
│   ├── ONNX Runtime
│   ├── OpenVINO (Intel)
│   └── CoreML (Apple)
├── Deployment Optimization
│   ├── Dynamic batching
│   ├── Model ensemble
│   ├── Multi-GPU inference
│   └── Edge deployment
└── Post-Processing Optimization
    ├── Efficient NMS
    ├── Batch NMS
    └── Parallel processing
```

### Quantization

```python
# INT8 quantization
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.export(format='onnx', int8=True, data='coco.yaml')
```

## Security Considerations

### Model Security

| Threat | Description | Mitigation |
|--------|-------------|------------|
| Model Theft | Unauthorized model access | Model encryption |
| Adversarial Attacks | Input manipulation | Adversarial training |
| Data Poisoning | Training data corruption | Data validation |
| Model Inversion | Extract training data | Differential privacy |
| Backdoor Attacks | Hidden triggers | Model auditing |

### Adversarial Robustness

```
Defense Strategies:
├── Adversarial training
├── Input validation
├── Ensemble methods
├── Certified robustness
└── Anomaly detection
```

## Troubleshooting Guide

### Common Detection Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Low mAP | Poor accuracy | Increase training data, adjust anchors |
| False Positives | Detecting background | Increase confidence threshold |
| Missed Detections | Missing objects | Lower confidence threshold |
| Slow Inference | Low FPS | Use smaller model, optimize |
| Memory Error | OOM during inference | Reduce batch size |

### Training Debugging

```
Issue: Model not converging
1. Check learning rate
2. Verify data loading
3. Check loss functions
4. Verify label format
5. Monitor validation metrics

Issue: Overfitting
1. Add data augmentation
2. Use regularization
3. Reduce model complexity
4. Get more training data
5. Use early stopping
```

### Inference Debugging

```python
# Check model input
print(f"Input shape: {model.input_shape}")
print(f"Input type: {model.input_type}")

# Check output
results = model('image.jpg')
print(f"Output shapes: {[r.shape for r in results]}")

# Profile inference
import time
start = time.time()
for _ in range(100):
    model('image.jpg')
print(f"Avg inference: {(time.time() - start) / 100 * 1000:.1f}ms")
```

## API Reference

### DetectorFactory

```python
class DetectorFactory:
    def create(
        model: str,
        num_classes: int,
        input_size: int,
        confidence_threshold: float,
    ) -> Detector:
        """Create detection model."""
```

### Detector

```python
class Detector:
    def detect(
        image: np.ndarray,
        confidence_threshold: float = None,
    ) -> DetectionResult:
        """Run detection on image."""
    
    def detect_batch(
        images: list[np.ndarray],
    ) -> list[DetectionResult]:
        """Run batch detection."""
```

### NMSProcessor

```python
class NMSProcessor:
    def process(
        detections: list[Detection],
        iou_threshold: float,
    ) -> list[Detection]:
        """Apply Non-Maximum Suppression."""
```

## Data Models

### Detection

```
Detection:
  bbox: tuple           # (x1, y1, x2, y2)
  confidence: float
  class_id: int
  class_name: str
  area: float
  center: tuple         # (cx, cy)
```

### DetectionResult

```
DetectionResult:
  detections: list[Detection]
  image_shape: tuple
  inference_time_ms: float
  model_name: str
  num_detections: int
```

### TrainingConfig

```
TrainingConfig:
  model: str
  dataset: str
  epochs: int
  batch_size: int
  learning_rate: float
  augmentations: list[str]
  optimizer: str
  pretrained: bool
```

## Deployment Guide

### Model Deployment

```
1. Export Model
   ├── YOLO to ONNX
   ├── ONNX to TensorRT
   └── TensorRT to engine

2. Optimize
   ├── Quantization (INT8)
   ├── Pruning
   └── Layer fusion

3. Deploy
   ├── Docker container
   ├── Kubernetes service
   ├── Edge device
   └── Cloud endpoint

4. Monitor
   ├── Latency tracking
   ├── Throughput monitoring
   └── Accuracy drift detection
```

## Monitoring & Observability

### Detection Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Inference Latency | <50ms | Per-image inference time |
| Throughput | >30 FPS | Images per second |
| mAP@0.5 | >0.5 | Detection accuracy |
| Memory Usage | <4GB | GPU memory usage |
| GPU Utilization | >70% | GPU usage |

## Testing Strategy

### Detection Testing

```
1. Unit Tests
   ├── Model loading
   ├── Preprocessing
   ├── Postprocessing
   └── NMS logic

2. Integration Tests
   ├── End-to-end detection
   ├── Batch processing
   ├── Video processing
   └── API endpoints

3. Accuracy Tests
   ├── COCO benchmark
   ├── Custom dataset
   ├── Edge cases
   └── Robustness tests
```

## Versioning & Migration

### Model Versioning

```
Major: Architecture change
├── Example: YOLOv5 → YOLOv8
├── Requires: Full retraining
└── Risk: High

Minor: Weight update
├── Example: Fine-tuned weights
├── Requires: Validation testing
└── Risk: Low

Patch: Config changes
├── Example: Threshold adjustment
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| Anchor | Pre-defined box templates for detection |
| BBox | Bounding box around detected object |
| CNN | Convolutional Neural Network |
| FP | False Positive |
| IoU | Intersection over Union |
| mAP | Mean Average Precision |
| NMS | Non-Maximum Suppression |
| ONNX | Open Neural Network Exchange |
| RPN | Region Proposal Network |
| TensorRT | NVIDIA inference optimizer |
| YOLO | You Only Look Once |

## Changelog

### 2.0.0 (2024-12-01)
- Added YOLOv8 support
- Added TensorRT optimization
- Improved NMS performance
- Added INT8 quantization

### 1.2.0 (2024-08-15)
- Added transformer detectors
- Added anchor-free methods
- Improved training pipeline

### 1.1.0 (2024-05-20)
- Added YOLOv5
- Added Faster R-CNN
- Improved deployment

### 1.0.0 (2024-02-01)
- Initial release with basic detection
- SSD support
- Simple deployment

## Contributing Guidelines

### Adding New Models

1. Implement model architecture
2. Add training pipeline
3. Include benchmarks
4. Document performance
5. Submit PR with results

## License

MIT License

Copyright (c) 2024 Object Detection Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
