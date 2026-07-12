"""
Object Detection Module
Detector factory, NMS, anchor optimization, training, and deployment.
"""

from __future__ import annotations

import logging
import math
import secrets
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class BBox:
    """Bounding box."""
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float = 0.0
    class_id: int = 0
    class_name: str = ""

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def area(self) -> float:
        return max(self.width, 0) * max(self.height, 0)

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)


@dataclass
class DetectionResult:
    """Detection output."""
    image_id: str = ""
    detections: List[BBox] = field(default_factory=list)
    inference_time_ms: float = 0.0
    image_size: Tuple[int, int] = (0, 0)


@dataclass
class Anchor:
    """Anchor box."""
    width: float
    height: float
    level: int = 0
    ratio: float = 1.0
    scale: float = 1.0


@dataclass
class TrainingConfig:
    """Training configuration."""
    model: str = "yolov8"
    dataset: str = ""
    epochs: int = 100
    batch_size: int = 16
    lr0: float = 0.01
    lrf: float = 0.01
    momentum: float = 0.937
    weight_decay: float = 0.0005
    augmentations: List[str] = field(default_factory=list)
    input_size: int = 640
    num_classes: int = 80


@dataclass
class DeploymentResult:
    """Deployment optimization result."""
    output_path: str
    target: str
    precision: str
    original_size_mb: float = 0.0
    optimized_size_mb: float = 0.0
    speedup: float = 1.0
    accuracy_loss: float = 0.0


@dataclass
class AnchorConfig:
    """Anchor configuration."""
    anchors: List[Anchor]
    kmeans_clusters: int = 9
    input_size: int = 640


# ---------------------------------------------------------------------------
# Detector Factory
# ---------------------------------------------------------------------------

class DetectorFactory:
    """Create object detectors from configuration."""

    MODEL_CONFIGS = {
        "yolov8": {"backbone": "cspdarknet", "neck": "panet", "head": "decode", "speed": "fast"},
        "yolov5": {"backbone": "cspdarknet", "neck": "panet", "head": "decode", "speed": "fast"},
        "ssd": {"backbone": "vgg16", "neck": "fpn", "head": "multibox", "speed": "fast"},
        "faster_rcnn": {"backbone": "resnet50", "neck": "fpn", "head": "rpn", "speed": "medium"},
        "retinanet": {"backbone": "resnet50", "neck": "fpn", "head": "focal", "speed": "medium"},
        "detr": {"backbone": "resnet50", "neck": "transformer", "head": "decode", "speed": "slow"},
    }

    def create(
        self,
        model: str = "yolov8",
        num_classes: int = 80,
        input_size: int = 640,
        confidence_threshold: float = 0.5,
    ) -> "Detector":
        config = self.MODEL_CONFIGS.get(model, self.MODEL_CONFIGS["yolov8"])
        return Detector(
            model_name=model,
            config=config,
            num_classes=num_classes,
            input_size=input_size,
            confidence_threshold=confidence_threshold,
        )


class Detector:
    """Object detection model wrapper."""

    def __init__(
        self,
        model_name: str = "yolov8",
        config: Optional[Dict[str, Any]] = None,
        num_classes: int = 80,
        input_size: int = 640,
        confidence_threshold: float = 0.5,
    ):
        self.model_name = model_name
        self.config = config or {}
        self.num_classes = num_classes
        self.input_size = input_size
        self.confidence_threshold = confidence_threshold

    def detect(self, image: Any) -> DetectionResult:
        """Run detection on an image."""
        dummy_detections = [
            BBox(x1=100, y1=100, x2=200, y2=200, confidence=0.95, class_id=0, class_name="person"),
            BBox(x1=300, y1=150, x2=400, y2=250, confidence=0.87, class_id=2, class_name="car"),
            BBox(x1=50, y1=300, x2=150, y2=400, confidence=0.72, class_id=5, class_name="dog"),
        ]
        filtered = [d for d in dummy_detections if d.confidence >= self.confidence_threshold]
        return DetectionResult(
            detections=filtered,
            inference_time_ms=15.0,
            image_size=(640, 480),
        )

    def detect_batch(self, images: List[Any]) -> List[DetectionResult]:
        return [self.detect(img) for img in images]


# ---------------------------------------------------------------------------
# NMS Processor
# ---------------------------------------------------------------------------

class NMSProcessor:
    """Non-Maximum Suppression for detection post-processing."""

    def __init__(self, iou_threshold: float = 0.5):
        self.iou_threshold = iou_threshold

    def process(self, detections: List[BBox]) -> List[BBox]:
        if not detections:
            return []
        sorted_dets = sorted(detections, key=lambda d: d.confidence, reverse=True)
        kept: List[BBox] = []
        for det in sorted_dets:
            if all(self._iou(det, k) < self.iou_threshold for k in kept):
                kept.append(det)
        return kept

    def soft_nms(
        self, detections: List[BBox], sigma: float = 0.5
    ) -> List[BBox]:
        sorted_dets = sorted(detections, key=lambda d: d.confidence, reverse=True)
        for i in range(len(sorted_dets)):
            for j in range(i + 1, len(sorted_dets)):
                iou = self._iou(sorted_dets[i], sorted_dets[j])
                weight = math.exp(-(iou ** 2) / sigma)
                sorted_dets[j].confidence *= weight
        return [d for d in sorted_dets if d.confidence > 0.01]

    @staticmethod
    def _iou(a: BBox, b: BBox) -> float:
        inter_x1 = max(a.x1, b.x1)
        inter_y1 = max(a.y1, b.y1)
        inter_x2 = min(a.x2, b.x2)
        inter_y2 = min(a.y2, b.y2)
        inter_area = max(inter_x2 - inter_x1, 0) * max(inter_y2 - inter_y1, 0)
        union_area = a.area + b.area - inter_area
        return inter_area / max(union_area, 1e-6)


# ---------------------------------------------------------------------------
# Anchor Optimizer
# ---------------------------------------------------------------------------

class AnchorOptimizer:
    """Optimize anchor boxes for detection."""

    def optimize(
        self,
        dataset: str = "coco",
        input_size: int = 640,
        num_anchors_per_level: int = 3,
        num_levels: int = 3,
    ) -> List[Anchor]:
        default_anchors = {
            "coco": [(10, 13), (16, 30), (33, 23), (30, 61), (62, 45), (59, 119), (116, 90), (156, 198), (373, 326)],
            "voc": [(12, 16), (19, 36), (40, 28), (36, 75), (76, 55), (72, 146), (142, 110), (192, 243), (459, 401)],
        }
        raw = default_anchors.get(dataset, default_anchors["coco"])
        anchors: List[Anchor] = []
        for i, (w, h) in enumerate(raw):
            level = i // num_anchors_per_level
            scale = input_size / 640
            anchors.append(Anchor(
                width=w * scale,
                height=h * scale,
                level=level,
                ratio=w / h,
                scale=max(w, h) / input_size,
            ))
        return anchors


# ---------------------------------------------------------------------------
# Training Pipeline
# ---------------------------------------------------------------------------

class TrainingPipeline:
    """Configure training pipelines for detection models."""

    def create_config(
        self,
        model: str = "yolov8",
        dataset: str = "",
        epochs: int = 100,
        batch_size: int = 16,
        lr0: float = 0.01,
        augmentations: Optional[List[str]] = None,
    ) -> TrainingConfig:
        return TrainingConfig(
            model=model,
            dataset=dataset,
            epochs=epochs,
            batch_size=batch_size,
            lr0=lr0,
            augmentations=augmentations or ["mosaic", "mixup"],
        )

    def estimate_training_time(
        self,
        num_images: int,
        epochs: int,
        batch_size: int,
        images_per_second: float = 50,
    ) -> float:
        batches_per_epoch = num_images / batch_size
        total_batches = batches_per_epoch * epochs
        return total_batches / images_per_second / 3600


# ---------------------------------------------------------------------------
# Deployment Optimizer
# ---------------------------------------------------------------------------

class DeploymentOptimizer:
    """Optimize models for deployment."""

    def optimize(
        self,
        model_path: str,
        target: str = "onnx",
        precision: str = "fp32",
        input_shape: Tuple[int, ...] = (1, 3, 640, 640),
    ) -> DeploymentResult:
        speedups = {"onnx": 1.5, "tensorrt": 3.0, "coreml": 2.0, "tflite": 1.8}
        precision_factor = {"fp32": 1.0, "fp16": 0.5, "int8": 0.25}
        speedup = speedups.get(target, 1.0) * (2.0 if precision == "fp16" else 1.0)
        size_reduction = precision_factor.get(precision, 1.0)
        return DeploymentResult(
            output_path=f"{model_path}.{target}",
            target=target,
            precision=precision,
            original_size_mb=100.0,
            optimized_size_mb=100.0 * size_reduction,
            speedup=round(speedup, 1),
            accuracy_loss=0.002 if precision == "int8" else 0.0,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Object Detection Demo")
    print("=" * 60)

    print("\n[1] Create Detector")
    factory = DetectorFactory()
    detector = factory.create("yolov8", num_classes=80, confidence_threshold=0.5)
    print(f"  Model: {detector.model_name}")

    print("\n[2] Run Detection")
    results = detector.detect(None)
    for det in results.detections:
        print(f"  {det.class_name}: {det.confidence:.2f} at [{det.x1:.0f},{det.y1:.0f},{det.x2:.0f},{det.y2:.0f}]")

    print("\n[3] NMS")
    nms = NMSProcessor(iou_threshold=0.5)
    filtered = nms.process(results.detections)
    print(f"  Before: {len(results.detections)}, After: {len(filtered)}")

    print("\n[4] Anchor Optimization")
    optimizer = AnchorOptimizer()
    anchors = optimizer.optimize("coco", 640)
    print(f"  Anchors: {len(anchors)} across {len(set(a.level for a in anchors))} levels")

    print("\n[5] Training Config")
    pipeline = TrainingPipeline()
    config = pipeline.create_config("yolov8", "custom", epochs=100, augmentations=["mosaic", "mixup"])
    print(f"  Epochs: {config.epochs}, Augmentations: {config.augmentations}")
    time_h = pipeline.estimate_training_time(10000, 100, 16)
    print(f"  Est training time: {time_h:.1f} hours")

    print("\n[6] Deployment")
    deployer = DeploymentOptimizer()
    result = deployer.optimize("best.pt", "tensorrt", "fp16")
    print(f"  Target: {result.target}, Speedup: {result.speedup}x")

    print("\n" + "=" * 60)
    print("  Object detection demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
