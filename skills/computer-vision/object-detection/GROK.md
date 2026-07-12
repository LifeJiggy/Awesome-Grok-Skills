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
