---
name: "robotics-vision"
category: "robotics"
version: "2.0.0"
tags: ["robotics", "computer-vision", "perception", "object-detection", "visual-odometry", "depth-estimation", "visual-slam"]
---

# Robotics Vision

## Overview

The Robotics Vision module provides computer vision infrastructure tailored for robotic perception pipelines. It covers camera calibration and undistortion, image preprocessing, feature detection and matching, object detection and tracking, visual odometry, stereo depth estimation, and visual SLAM. Designed for real-time operation on embedded platforms and GPU-accelerated workstations, the module emphasizes low-latency processing, robust feature extraction under varying lighting, and modular pipeline composition.

Robotics vision differs from general computer vision in its tight coupling with the robot's state estimation and control loops. Every perception module must output results within a strict time budget, and failures must be handled gracefully so the robot can fall back to alternative sensors or safe behaviors. The module is built around a pipeline abstraction that connects processing stages, measures latency at each stage, and provides deterministic fallback behavior when a stage exceeds its time budget.

The module supports both monocular and stereo camera configurations, RGB-D sensors, and event cameras. It is designed to integrate seamlessly with the navigation and autonomous-systems modules, providing object detections for world modeling, visual odometry for localization, and depth maps for obstacle avoidance. All components are GPU-accelerated where available and fall back to optimized CPU implementations on embedded platforms.

## Core Capabilities

- **Camera Calibration** — intrinsic and extrinsic calibration, lens undistortion, stereo rectification. Supports checkerboard, circle grid, and ArUco calibration patterns with automatic corner detection.
- **Image Preprocessing** — adaptive histogram equalization (CLAHE), denoising, ROI extraction, color space conversion. Pipeline stages are composable and auto-measure latency.
- **Feature Detection and Matching** — ORB, SIFT, SURF features with brute-force and FLANN matchers. Includes ratio test, cross-check, and RANSAC-based geometric verification.
- **Object Detection** — YOLO-style single-shot detection, contour-based detection, template matching. Supports custom-trained models via ONNX and TensorRT.
- **Object Tracking** — Kalman-filter-based multi-object tracking, IoU association, track lifecycle management. Handles occlusion, identity switches, and track fragmentation.
- **Visual Odometry** — frame-to-frame pose estimation from monocular or stereo camera sequences. Includes motion estimation, outlier rejection, and scale recovery.
- **Stereo Depth** — block matching, semi-global block matching, disparity-to-depth conversion. Configurable disparity range and post-filtering for noise reduction.
- **Color and Shape Segmentation** — HSV color filtering, contour extraction, geometric shape classification. Useful for simple pick-and-place targeting without deep learning.
- **Visual SLAM** — ORB-SLAM-style feature-based SLAM with loop closure detection and pose graph optimization. Fuses with IMU data for robust tracking.
- **Pipeline Composition** — connectable processing stages with automatic latency measurement and timeout enforcement. Stages can be hot-swapped at runtime.

## Usage Examples

### Camera Calibration and Undistortion

```python
from robotics_vision import CameraCalibrator, CalibrationConfig

config = CalibrationConfig(
    board_size=(9, 6),
    square_size_mm=25.0,
    image_size=(1920, 1080),
)

calibrator = CameraCalibrator(config)
for image in calibration_images:
    calibrator.add_image(image)

result = calibrator.calibrate()
print(f"RMS reprojection error: {result.rms_error:.4f}")
print(f"Intrinsic matrix:\n{result.camera_matrix}")

undistorted = calibrator.undistort(raw_image)
```

### Object Detection Pipeline

```python
from robotics_vision import ObjectDetector, DetectionConfig, DetectionFilter

detector = ObjectDetector(
    config=DetectionConfig(
        confidence_threshold=0.6,
        nms_threshold=0.4,
        input_size=(416, 416),
    ),
    filter=DetectionFilter(
        min_area=500,
        max_area=50000,
        class_whitelist=["person", "car", "box"],
    ),
)

detections = detector.detect(frame)
for det in detections:
    print(f"Class: {det.class_name}, Confidence: {det.confidence:.2f}, "
          f"BBox: {det.bounding_box}")
```

### Multi-Object Tracking

```python
from robotics_vision import MultiObjectTracker, TrackConfig

tracker = MultiObjectTracker(config=TrackConfig(
    max_age=30,
    min_hits=3,
    distance_threshold=80.0,
))

for frame in video_stream:
    detections = detector.detect(frame)
    tracks = tracker.update(detections)
    active = [t for t in tracks if t.is_confirmed]
    print(f"Frame: {frame.id}, Active tracks: {len(active)}")
```

### Visual Odometry

```python
from robotics_vision import VisualOdometry, OdometryConfig

vo = VisualOdometry(config=OdometryConfig(
    feature_type="orb",
    max_features=2000,
    match_ratio_test=0.75,
    ransac_threshold=5.0,
))

prev_frame = None
for frame in camera_stream:
    if prev_frame is not None:
        delta_pose = vo.estimate(prev_frame, frame)
        print(f"Translation: {delta_pose.translation}, Rotation: {delta_pose.rotation_euler}")
    prev_frame = frame
```

### Stereo Depth Estimation

```python
from robotics_vision import StereoDepthEstimator, StereoConfig

stereo = StereoDepthEstimator(config=StereoConfig(
    num_disparities=64,
    block_size=15,
    uniqueness_ratio=10,
    speckle_window=100,
    baseline_mm=120.0,
    focal_length_px=640.0,
))

depth_map = stereo.compute_disparity(left_image, right_image)
point_cloud = stereo.disparity_to_point_cloud(depth_map)
```

### Visual SLAM Pipeline

```python
from robotics_vision import VisualSLAM, SLAMConfig

slam = VisualSLAM(config=SLAMConfig(
    num_features=2000,
    scale_factor=1.2,
    pyramid_levels=8,
    loop_closure_enabled=True,
    imu_fusion=True,
))

for frame in camera_stream:
    result = slam.process_frame(frame)
    if result.tracking_state == "OK":
        print(f"Pose: {result.pose}, Map points: {result.num_map_points}")
    if result.loop_closure_detected:
        print(f"Loop closed! Pose correction: {result.correction}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Camera Driver Layer                    │
│  (USB, GigE, CSI, ROS topics, RTSP streams)             │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Calibration & Undistortion              │
│  (intrinsic correction, stereo rectification)           │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Preprocessing Pipeline                  │
│  (CLAHE, denoise, resize, color convert, ROI crop)      │
└──────────┬───────────┬───────────────┬─────────────────┘
           │           │               │
┌──────────▼──┐ ┌──────▼──────┐ ┌──────▼──────────┐
│  Detection  │ │  Features   │ │  Stereo Depth   │
│  (YOLO/etc) │ │ (ORB/SIFT)  │ │  (SGBM/disparity)│
└──────┬──────┘ └──────┬──────┘ └──────┬──────────┘
       │               │               │
┌──────▼───────────────▼───────────────▼─────────────────┐
│              Tracking / Odometry / SLAM                  │
│  (multi-object tracks, visual odometry, pose graph)     │
└──────────────────────┬──────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  Output to Nav  │
              │  / World Model  │
              └─────────────────┘
```

The pipeline processes each frame through a chain of stages. Each stage declares its latency budget and the pipeline enforces it — if a stage exceeds its budget, the pipeline returns the last valid result and logs the timeout. This ensures the vision system never blocks the robot's control loop.

## Best Practices

1. **Calibrate once, verify often.** Camera intrinsics change with temperature and vibration. Store calibration results and re-verify periodically during long deployments. A calibration drift of even 1-2 pixels can cause significant depth errors in stereo.
2. **Use adaptive preprocessing.** Lighting conditions in the field vary dramatically. Adaptive histogram equalization (CLAHE) and auto-exposure compensation prevent feature detection failures. Tune clip limits for your environment.
3. **Budget your processing time.** A vision pipeline running at 30 FPS has 33 ms per frame. Profile each stage and set hard timeouts. If a stage exceeds its budget, skip it and use the last known result rather than blocking.
4. **Prefer feature-based methods over pixel-wise methods for odometry.** Feature-based visual odometry is more robust to illumination changes and provides sparse but reliable pose estimates. Dense methods are more accurate but too slow for real-time use on embedded platforms.
5. **Use Kalman filters for tracking.** Raw detections flicker and miss frames. A Kalman filter smooths tracks, predicts positions through occlusions, and maintains object identity across frames. Tune the process noise to match real-world motion dynamics.
6. **Validate detections against geometric constraints.** A car cannot appear at 50 meters in one frame and 5 meters in the next. Apply sanity checks on size, velocity, and position continuity. Reject detections that violate physical constraints.
7. **Handle camera failures gracefully.** If the vision pipeline fails to produce results within the time budget, the robot must have a fallback — IMU dead-reckoning, previous trajectory extrapolation, or a safe stop. Never let a vision failure cascade into loss of control.
8. **Store raw calibration data.** Never discard the images used for calibration. They are invaluable for re-calibration, troubleshooting, and verifying intrinsics on different hardware. Store them alongside the calibration parameters.
9. **Use GPU acceleration when available.** YOLO and other CNN-based detectors run 10-50x faster on GPU. On embedded platforms, use TensorRT or OpenVINO for optimized inference. Fall back to CPU-only methods when GPU is unavailable.
10. **Test under target lighting conditions.** Vision algorithms that work in a well-lit lab often fail in direct sunlight, shadows, or low light. Test your pipeline in the actual deployment environment before field use.

## Performance Considerations

- **Frame rate**: Target 30 FPS for real-time tracking, 15 FPS minimum for visual odometry. Profile the full pipeline and identify bottlenecks. Common culprits: image resize, NMS in detection, and feature matching.
- **GPU memory**: YOLO models consume 200-500 MB of GPU memory. On platforms with shared GPU/CPU memory, this competes with other modules. Use model quantization (INT8) to reduce memory footprint.
- **Stereo matching cost**: SGBM with 128 disparities on a 1280x720 image takes 10-30 ms on GPU, 100-300 ms on CPU. Reduce resolution or disparity range for embedded platforms.
- **Feature extraction**: ORB extracts 2000 features in 5-10 ms. SIFT is 5-10x slower but more distinctive. Use ORB for real-time applications and SIFT for offline processing.
- **Latency measurement**: Instrument every pipeline stage with high-resolution timers. Log the 95th and 99th percentile latencies, not just the average. Occasional spikes cause missed deadlines.
- **Memory bandwidth**: Image processing is memory-bandwidth-bound. Use contiguous memory buffers, avoid unnecessary copies, and process ROIs in-place when possible.

## Security Considerations

- **Camera access control**: Unauthorized camera access can leak sensitive visual data. Implement authentication on camera streams and encrypt video feeds in transit.
- **Model integrity**: Object detection models can be adversarially perturbed. Validate model checksums before loading and monitor for adversarial inputs that cause misclassification.
- **Data privacy**: Vision systems may capture faces, license plates, or other PII. Implement on-device blurring or redaction for privacy compliance (GDPR, CCPA).
- **Secure model distribution**: When updating detection models over-the-air, verify signatures and use encrypted channels. A tampered model can cause the robot to misidentify obstacles.
- **Anti-spoofing**: Visual markers and fiducials can be spoofed with printed images. Use depth verification or temporal consistency checks to detect spoofed markers.
- **Storage encryption**: Vision logs may contain sensitive imagery. Encrypt stored video data and implement retention policies.

## Related Modules

- **autonomous-systems** — World modeling and path planning that consume vision pipeline outputs
- **navigation** — Visual SLAM integration with IMU and wheel odometry for localization
- **manipulation** — Visual servoing for grasp alignment and pick-and-place operations
- **swarm-robotics** — Shared visual maps for cooperative perception among multiple robots

## Advanced Configuration

### Camera Calibration Profiles

```yaml
calibration:
  profile: "industrial_robot_arm"
  board_type: checkerboard
  board_size: [9, 6]
  square_size_mm: 25.0
  image_count: 30
  min_images: 15
  rms_threshold: 0.5
  distortion_model: radial_tangential
  output_format: opencv_yaml
```

### Object Detection Model Configuration

```yaml
detection:
  model: yolov8n
  input_size: [416, 416]
  confidence_threshold: 0.6
  nms_threshold: 0.4
  device: cuda:0
  half_precision: true
  class_whitelist: ["person", "car", "box", "forklift"]
  custom_model_path: null
  batch_size: 4
```

### Visual SLAM Configuration

```yaml
slam:
  feature_type: orb
  num_features: 2000
  scale_factor: 1.2
  pyramid_levels: 8
  fast_threshold: 20
  matcher: brute_force_hamming
  loop_closure: true
  loop_closure_threshold: 0.75
  imu_fusion: true
  map_save_path: "./maps/"
  keyframe_distance_m: 0.1
  min_inlier_count: 50
```

## Architecture Patterns

### Pipeline Composition Pattern

Each vision pipeline stage is a composable unit with declared latency budgets:

```
CameraDriver → Calibration → Preprocessing → [Detection | Features | Depth] → Tracking/SLAM → Output

Pipeline Stage Interface:
  input: Image/DataFrame
  output: ProcessedResult
  latency_budget_ms: float
  fallback: ResultType  # last valid result on timeout
  on_timeout: enum      # SKIP, USE_LAST, ABORT
```

### Producer-Consumer Pattern for Real-Time Vision

```
Camera Thread (Producer):
  └─ Acquire frame from hardware buffer
  └─ Enqueue to frame ring buffer (lock-free)
  └─ Signal processing thread

Processing Thread (Consumer):
  └─ Dequeue frame from ring buffer
  └─ Run pipeline stages sequentially
  └─ Enqueue results to output buffer
  └─ Update tracking state

Visualization Thread:
  └─ Dequeue results for display
  └─ Render overlay (detections, tracks, depth)
  └─ Non-blocking display refresh
```

### Kalman Filter Tracking Pattern

```
Prediction Step:
  x̂ = F * x̂ + B * u     (state prediction)
  P = F * P * F' + Q     (covariance prediction)

Update Step:
  K = P * H' * (H * P * H' + R)⁻¹  (Kalman gain)
  x̂ = x̂ + K * (z - H * x̂)         (state update)
  P = (I - K * H) * P                (covariance update)

Association (Hungarian Algorithm):
  └─ Compute cost matrix (detection-to-track distance)
  └─ Solve assignment (min-cost matching)
  └─ Gate matches by Mahalanobis distance threshold
  └─ Create new tracks for unmatched detections
  └─ Age out tracks below hit threshold
```

## Integration Guide

### Sensor Fusion with Navigation Module

```python
# Fuse visual odometry with IMU and wheel odometry
from robotics_vision import VisualOdometry
from navigation import EKFFusion

vo = VisualOdometry(config=OdometryConfig(feature_type="orb"))
fusion = EKFFusion()

for imu, wheel, camera_frame in sensor_stream:
    vo_delta = vo.estimate(prev_frame, camera_frame)
    fused_pose = fusion.update(imu, wheel, visual_odometry=vo_delta)
    prev_frame = camera_frame
```

### YOLO Detection to World Model Pipeline

```python
# Convert 2D detections to 3D world model entries
from robotics_vision import ObjectDetector, DetectionTo3D

detector = ObjectDetector(config=DetectionConfig(model="yolov8n"))
to_3d = DetectionTo3D(stereo_baseline_mm=120.0, focal_length_px=640.0)

for left_frame, right_frame in stereo_stream:
    detections = detector.detect(left_frame)
    depth_map = stereo.compute_disparity(left_frame, right_frame)
    objects_3d = to_3d.convert(detections, depth_map)
    world_model.update_objects(objects_3d)
```

### Event Camera Integration

```python
from robotics_vision import EventCameraDriver, EventProcessor

driver = EventCameraDriver(device="/dev/event0", resolution=(640, 480))
processor = EventProcessor(
    method="time_surface",
    accumulation_window_ms=50,
    noise_filter_threshold=1
)

for events in driver.stream():
    time_surface = processor.process(events)
    features = processor.extract_features(time_surface)
```

## Performance Optimization

### GPU Utilization Strategy

| Component | GPU Memory | Speedup vs CPU | Recommended |
|-----------|-----------|----------------|-------------|
| YOLOv8n detection | 200 MB | 15-30x | Yes |
| YOLOv8x detection | 500 MB | 10-20x | Yes (if available) |
| ORB feature extraction | 50 MB | 3-5x | Optional |
| SGBM stereo | 100 MB | 5-10x | Yes for real-time |
| Optical flow | 80 MB | 8-15x | Optional |

### Latency Optimization Checklist

1. **Reduce input resolution**: Process at 640x480 for detection, full resolution only for features
2. **Use TensorRT/ONNX**: Convert PyTorch models to optimized inference format
3. **Enable FP16**: Half-precision inference on GPU with minimal accuracy loss
4. **Pipeline parallelism**: Run detection on GPU while preprocessing next frame on CPU
5. **Zero-copy buffers**: Use shared memory for camera-to-GPU frame transfer
6. **Skip frames**: Process every Nth frame for non-critical pipelines; interpolate between results

### Memory Management

- **Ring buffer size**: Allocate 2-3x the pipeline latency in frame buffers to absorb jitter
- **Feature cache**: LRU cache of 50-100 frames of extracted features for loop closure
- **Model caching**: Keep detection and SLAM models in GPU memory for the session lifetime
- **Image pre-allocation**: Pre-allocate output arrays for undistortion, resize, and color conversion

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| High reprojection error | Calibration drift | Re-calibrate; check for thermal effects |
| Lost tracking in SLAM | Insufficient features | Increase ORB features; add texture-rich areas |
| Detection false positives | Low confidence threshold | Raise confidence threshold; retrain model |
| Stereo depth holes | Textureless surfaces | Add structured light or switch to ToF camera |
| Frame drops | Pipeline exceeds budget | Profile stages; reduce resolution or skip frames |
| Color shift after calibration | Wrong distortion model | Verify distortion model matches lens type |
| Loop closure false positives | Low feature distinctiveness | Increase descriptor size; use SIFT for offline |

### Diagnostic Commands

```bash
# Check camera calibration quality
python -m robotics_vision.calibration_check --images ./calibration_images/

# Test detection pipeline latency
python -m robotics_vision.bench_detection --model yolov8n --input test_video.mp4

# Verify stereo calibration
python -m robotics_vision.stereo_check --left left.yml --right right.yml

# Profile full pipeline
python -m robotics_vision.profiler --pipeline full --duration 30
```

## API Reference

### Core Classes

| Class | Description |
|-------|-------------|
| `CameraCalibrator` | Intrinsic/extrinsic calibration with automatic corner detection |
| `ObjectDetector` | YOLO-style single-shot detection with filtering |
| `MultiObjectTracker` | Kalman-filter-based multi-object tracking |
| `VisualOdometry` | Frame-to-frame pose estimation |
| `StereoDepthEstimator` | Block/semi-global matching disparity computation |
| `VisualSLAM` | ORB-based SLAM with loop closure |
| `PipelineComposer` | Composable pipeline stage manager with timeout enforcement |

### Key Enums

| Enum | Values |
|------|--------|
| `FeatureType` | ORB, SIFT, SURF, AKAZE |
| `DetectionBackend` | OPENCV, TENSORRT, ONNX, CPU |
| `TrackingState` | OK, LOST, NOT_INITIALIZED |
| `LoopClosureResult` | DETECTED, CANDIDATE, REJECTED |

## Data Models

### Detection

```
Detection:
  bbox: (x, y, w, h)    # bounding box in pixels
  class_name: str         # class label
  confidence: float       # 0.0-1.0
  class_id: int           # numeric class ID
  frame_id: int           # source frame
```

### Track

```
Track:
  track_id: int           # unique track identifier
  state: TrackingState
  bbox: (x, y, w, h)     # predicted bounding box
  velocity: (vx, vy)      # estimated velocity (px/s)
  age_frames: int         # total frames tracked
  hits: int               # successful update count
  misses: int             # missed detection count
  is_confirmed: bool      # meets min_hits threshold
```

### CameraIntrinsics

```
CameraIntrinsics:
  camera_matrix: 3x3 array
  distortion_coeffs: (k1, k2, p1, p2, k3)
  image_size: (width, height)
  rms_error: float
  focal_length_px: float
  principal_point: (cx, cy)
```

## Deployment Guide

### Edge Deployment (Jetson Orin)

```bash
# Install TensorRT models
python -m robotics_vision.export_model --model yolov8n --format engine --device jetson

# Run with GPU acceleration
python -m robotics_vision.pipeline --device cuda:0 --backend tensorrt --resolution 640x480
```

### Cloud Deployment (GPU Server)

```bash
# Multi-camera pipeline
python -m robotics_vision.multi_camera_server \
  --cameras 4 \
  --model yolov8n \
  --gpus 2 \
  --port 8080
```

### Camera Hardware Selection Guide

| Use Case | Recommended Camera | Resolution | Frame Rate |
|----------|-------------------|------------|------------|
| Indoor navigation | Intel RealSense D435 | 1280x720 | 30 fps |
| Outdoor mapping | FLIR Blackfly S | 2048x1536 | 60 fps |
| High-speed tracking | FLIR Oryx | 2448x2048 | 120 fps |
| Event-based | Prophesee EVK4 | 1280x720 | 1 Mfps |
| Stereo depth | ZED 2i | 2208x1242 | 15 fps |

## Monitoring & Observability

### Pipeline Health Metrics

| Metric | Description | Alert |
|--------|-------------|-------|
| `pipeline_fps` | Frames processed per second | < 15 fps |
| `detection_latency_ms` | Detection stage latency | > 30 ms |
| `tracking_id_switches` | Track identity changes | > 5 per minute |
| `slam_tracking_state` | SLAM tracker state | != OK |
| `loop_closures_total` | Loop closure count | Sudden spike |
| `stereo_depth_coverage` | % of valid depth pixels | < 70% |

### Prometheus Integration

```python
from prometheus_client import Counter, Histogram, Gauge

detected_objects = Counter('vision_detected_total', 'Objects detected', ['class'])
detection_latency = Histogram('vision_detection_latency_seconds', 'Detection latency')
active_tracks = Gauge('vision_active_tracks', 'Number of active tracks')
slam_pose = Gauge('vision_slam_pose', 'SLAM pose estimate', ['axis'])
```

## Testing Strategy

### Unit Tests

- Camera calibration: verify RMS error < 0.5 pixels with synthetic data
- Detection: verify mAP > 0.5 on test dataset with known ground truth
- Tracking: verify identity preservation across 100-frame sequences
- Depth: verify disparity error < 2 pixels on calibrated stereo pairs

### Integration Tests

- Full pipeline latency test: verify < 33 ms (30 fps) on target hardware
- SLAM drift test: verify < 1% drift over 100 m traversal
- Detection-to-tracking: verify track continuity through partial occlusions

### Regression Tests

- Calibration stability: verify intrinsics don't change > 0.1% over 1-hour session
- Detection consistency: verify same detections on same frames across runs
- Memory leak test: verify stable memory usage over 24-hour continuous operation

## Versioning & Migration

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-01-15 | YOLOv8 support, visual SLAM, GPU acceleration |
| 1.5.0 | 2023-09-01 | Multi-object tracking, stereo depth improvements |
| 1.0.0 | 2023-03-15 | Initial release: detection, features, basic odometry |

## Glossary

| Term | Definition |
|------|-----------|
| **ORB** | Oriented FAST and Rotated BRIEF — fast binary feature descriptor |
| **SIFT** | Scale-Invariant Feature Transform — robust feature descriptor |
| **SLAM** | Simultaneous Localization and Mapping |
| **CLAHE** | Contrast Limited Adaptive Histogram Equalization |
| **NMS** | Non-Maximum Suppression — removes overlapping detection boxes |
| **RANSAC** | Random Sample Consensus — robust model fitting with outlier rejection |
| **SGBM** | Semi-Global Block Matching — stereo depth algorithm |
| **FLANN** | Fast Library for Approximate Nearest Neighbors — feature matching |

## Changelog

### 2.0.0 — 2024-01-15

- **Added**: YOLOv8 single-shot detection with TensorRT backend
- **Added**: ORB-SLAM-style visual SLAM with loop closure
- **Added**: GPU acceleration for detection, stereo, and feature extraction
- **Improved**: Multi-object tracking with Kalman filter and Hungarian matching
- **Improved**: Stereo depth quality by 30% with SGBM tuning
- **Fixed**: Camera calibration stability under thermal drift

## Contributing Guidelines

1. Follow PEP 8 with type hints on all public APIs
2. Run `pytest tests/ --cov=robotics_vision --cov-report=html` before submitting PRs
3. Target coverage: 80%+ for all modules
4. All performance-sensitive code must include benchmarks
5. New detection models require accuracy evaluation on standardized test set

## License

Apache License, Version 2.0. Copyright 2024 Robotics Vision Contributors.

## References

- Hartley, R. & Zisserman, A. (2004). *Multiple View Geometry in Computer Vision*, 2nd Edition. Cambridge University Press.
- Scaramuzza, D. & Fraundorfer, F. (2011). Visual odometry [Tutorial]. *IEEE Robotics & Automation Magazine*, 18(4), 80-92.
- Mur-Artal, R., Montiel, J. M. M., & Tardos, J. D. (2015). ORB-SLAM: A versatile and accurate monocular SLAM system. *IEEE Transactions on Robotics*, 31(5), 1147-1163.
- Redmon, J. & Farhadi, A. (2018). YOLOv3: An incremental improvement. *arXiv preprint arXiv:1804.02767*.
- Bradski, G. (2000). The OpenCV Library. *Dr. Dobb's Journal of Software Tools*.
- Lavalle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.
- OpenCV Stereo Vision Tutorial: https://docs.opencv.org/4.x/dd/d52/tutorial_js_depth.html
- ORB-SLAM3 GitHub Repository: https://github.com/UZ-SLAMLab/ORB_SLAM3

## Depth Estimation Algorithms

### Monocular Depth Estimation with MiDaS

Monocular depth estimation predicts relative depth from a single RGB image using a trained neural network. The MiDaS architecture uses multi-scale feature fusion for robust depth prediction.

```python
import torch
from robotics_vision import DepthEstimator, DepthConfig

class MiDaSDepthEstimator:
    def __init__(self, config):
        self.config = config
        self.model = torch.hub.load("intel-isl/MiDaS", config.model_type)
        self.model.eval()
        self.transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform
    
    def estimate(self, image):
        input_batch = self.transform(image)
        
        with torch.no_grad():
            prediction = self.model(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=image.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        
        depth_map = prediction.cpu().numpy()
        
        # Convert relative depth to metric depth using scale and shift
        if self.config.metric_scale is not None:
            depth_map = depth_map * self.config.metric_scale + self.config.metric_shift
        
        return depth_map
    
    def estimate_with_confidence(self, image):
        depth_map = self.estimate(image)
        
        # Multi-scale ensemble for uncertainty estimation
        scales = [0.8, 1.0, 1.2]
        predictions = []
        for scale in scales:
            scaled_input = torch.nn.functional.interpolate(
                self.transform(image).unsqueeze(0),
                scale_factor=scale,
                mode="bilinear"
            )
            with torch.no_grad():
                pred = self.model(scaled_input)
                pred = torch.nn.functional.interpolate(
                    pred.unsqueeze(1),
                    size=image.shape[:2],
                    mode="bicubic"
                ).squeeze()
                predictions.append(pred.cpu().numpy())
        
        mean_depth = np.mean(predictions, axis=0)
        std_depth = np.std(predictions, axis=0)
        
        return mean_depth, std_depth
```

### Stereo Depth Estimation — SGBM Optimization

```python
import cv2
import numpy as np

class OptimizedSGBM:
    def __init__(self, config):
        self.config = config
        self.stereo = cv2.StereoSGBM_create(
            minDisparity=config.min_disparity,
            numDisparities=config.num_disparities,
            blockSize=config.block_size,
            P1=8 * 3 * config.block_size**2,
            P2=32 * 3 * config.block_size**2,
            disp12MaxDiff=config.disp12_max_diff,
            uniquenessRatio=config.uniqueness_ratio,
            speckleWindowSize=config.speckle_window_size,
            speckleRange=config.speckle_range,
            preFilterCap=config.pre_filter_cap,
            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY,
        )
        self.wls_filter = cv2.ximgproc.createDisparityWLSFilter(self.stereo)
        self.right_matcher = cv2.ximgproc.createRightMatcher(self.stereo)
    
    def compute(self, left_gray, right_gray):
        left_disp = self.stereo.compute(left_gray, right_gray)
        right_disp = self.right_matcher.compute(right_gray, left_gray)
        
        filtered_disp = self.wls_filter.filter(left_disp, left_gray, disparity_map_right=right_disp)
        
        depth_map = np.zeros_like(filtered_disp, dtype=np.float32)
        valid = filtered_disp > 0
        depth_map[valid] = (self.config.focal_length_px * self.config.baseline_mm) / filtered_disp[valid]
        
        return depth_map, filtered_disp
```

### RGB-D Depth Processing

```python
class RGBDDepthProcessor:
    def __init__(self, config):
        self.config = config
        self.invalid_value = 0
        self.depth_scale = config.depth_scale  # e.g., 0.001 for mm to m
    
    def process(self, depth_image, rgb_image):
        # Scale to metric
        depth_m = depth_image.astype(np.float32) * self.depth_scale
        
        # Remove invalid pixels
        valid_mask = (depth_m > self.config.min_depth) & (depth_m < self.config.max_depth)
        depth_m[~valid_mask] = self.invalid_value
        
        # Temporal smoothing
        if hasattr(self, 'prev_depth'):
            alpha = self.config.temporal_alpha
            depth_m = alpha * depth_m + (1 - alpha) * self.prev_depth
        self.prev_depth = depth_m.copy()
        
        # Hole filling via inpainting
        depth_filled = self.fill_holes(depth_m, valid_mask)
        
        # Generate point cloud
        points = self.depth_to_pointcloud(depth_filled, rgb_image)
        
        return {
            'depth': depth_filled,
            'valid_mask': valid_mask,
            'point_cloud': points,
        }
    
    def fill_holes(self, depth, valid_mask):
        depth_uint16 = (depth * 1000).astype(np.uint16)
        depth_uint16[~valid_mask] = 0
        
        filled = cv2.inpaint(depth_uint16, (~valid_mask).astype(np.uint8), 
                             self.config.inpaint_radius, cv2.INPAINT_NS)
        
        return filled.astype(np.float32) / 1000.0
```

## 6D Pose Estimation

### Feature-Based 6D Pose Estimation

Estimates the full 6-DOF pose (position + orientation) of a known object from a single image.

```python
import numpy as np
from robotics_vision import FeatureDetector, PnPResolver

class FeatureBased6DPose:
    def __init__(self, config):
        self.detector = FeatureDetector(type=config.feature_type, max_features=config.max_features)
        self.pnp = PnPResolver(method=config.pnp_method)
        self.matcher = FeatureMatcher(ratio_test=config.ratio_test)
        
        # Load object 3D model points and descriptors
        self.model_points = None
        self.model_descriptors = None
    
    def load_model(self, model_path):
        mesh = self.load_mesh(model_path)
        self.model_points = mesh.vertices
        self.model_descriptors = self.detector.describe_reference(model_path)
    
    def estimate(self, image, camera_matrix, dist_coeffs):
        # Detect features
        keypoints, descriptors = self.detector.detect_and_compute(image)
        
        # Match against model
        matches = self.matcher.match(descriptors, self.model_descriptors)
        
        if len(matches) < 6:
            return None
        
        # Get 3D-2D correspondences
        obj_points = []
        img_points = []
        for match in matches:
            obj_points.append(self.model_points[match.train_idx])
            img_points.append(keypoints[match.query_idx].pt)
        
        obj_points = np.array(obj_points, dtype=np.float32)
        img_points = np.array(img_points, dtype=np.float32)
        
        # Solve PnP
        success, rvec, tvec, inliers = self.pnp.solve(
            obj_points, img_points, camera_matrix, dist_coeffs
        )
        
        if not success:
            return None
        
        # Refine with inliers
        if len(inliers) > 6:
            success, rvec, tvec = self.pnp.refine(
                obj_points[inliers], img_points[inliers], 
                camera_matrix, dist_coeffs, rvec, tvec
            )
        
        rotation_matrix, _ = cv2.Rodrigues(rvec)
        
        return Pose6D(
            position=tvec.flatten(),
            rotation=rotation_matrix,
            rvec=rvec,
            tvec=tvec,
            num_inliers=len(inliers),
            inlier_ratio=len(inliers) / len(matches),
        )

class Deep6DPose:
    def __init__(self, config):
        self.model = self.load_model(config.model_path)
        self.refiner = PoseRefineriterations=config.refinement_iterations)
    
    def estimate(self, image, object_id):
        # Direct regression of pose
        pose_pred, confidence = self.model.predict(image)
        
        if confidence < self.config.confidence_threshold:
            return None
        
        # Refine with iterative optimization
        refined_pose = self.refiner.refine(
            image, pose_pred, self.config.learning_rate, self.config.refinement_iterations
        )
        
        return Pose6D(
            position=refined_pose[:3, 3],
            rotation=refined_pose[:3, :3],
            confidence=confidence,
        )
```

## Point Cloud Processing

### Point Cloud Filtering and Segmentation

```python
import numpy as np
from robotics_vision import PointCloud, VoxelGrid

class PointCloudProcessor:
    def __init__(self, config):
        self.config = config
        self.voxel_filter = VoxelGrid(voxel_size=config.voxel_size)
    
    def filter_and_segment(self, point_cloud):
        # Statistical outlier removal
        filtered = self.statistical_outlier_removal(
            point_cloud, 
            k_neighbors=self.config.outlier_k,
            std_ratio=self.config.outlier_std_ratio
        )
        
        # Voxel downsampling
        downsampled = self.voxel_filter.downsample(filtered)
        
        # RANSAC plane segmentation
        plane_model, inlier_mask = self.ransac_segmentation(
            downsampled, 
            distance_threshold=self.config.plane_distance_threshold,
            max_iterations=self.config.plansac_iterations
        )
        
        objects_cloud = downsampled[~inlier_mask]
        plane_cloud = downsampled[inlier_mask]
        
        # Euclidean clustering on objects
        clusters = self.euclidean_clustering(
            objects_cloud,
            tolerance=self.config.cluster_tolerance,
            min_size=self.config.cluster_min_size,
            max_size=self.config.cluster_max_size
        )
        
        return {
            'plane': plane_cloud,
            'plane_model': plane_model,
            'clusters': clusters,
        }
    
    def statistical_outlier_removal(self, points, k_neighbors=20, std_ratio=2.0):
        from scipy.spatial import cKDTree
        tree = cKDTree(points)
        distances, _ = tree.query(points, k=k_neighbors)
        mean_distances = np.mean(distances, axis=1)
        
        threshold = np.mean(mean_distances) + std_ratio * np.std(mean_distances)
        inliers = mean_distances < threshold
        
        return points[inliers]
    
    def euclidean_clustering(self, points, tolerance=0.02, min_size=50, max_size=10000):
        from scipy.spatial import cKDTree
        tree = cKDTree(points)
        
        visited = np.zeros(len(points), dtype=bool)
        clusters = []
        
        for i in range(len(points)):
            if visited[i]:
                continue
            
            cluster = [i]
            queue = [i]
            visited[i] = True
            
            while queue:
                current = queue.pop(0)
                neighbors = tree.query_ball_point(points[current], tolerance)
                
                for nb in neighbors:
                    if not visited[nb]:
                        visited[nb] = True
                        cluster.append(nb)
                        queue.append(nb)
            
            if min_size <= len(cluster) <= max_size:
                clusters.append(points[cluster])
        
        return clusters
```

### Point Cloud Registration (ICP)

```python
class PointCloudRegistration:
    def __init__(self, config):
        self.max_iterations = config.max_iterations
        self.tolerance = config.tolerance
        self.max_correspondence_distance = config.max_correspondence_distance
    
    def register_icp(self, source, target, initial_transform=np.eye(4)):
        transform = initial_transform.copy()
        
        for iteration in range(self.max_iterations):
            # Transform source
            source_h = np.hstack([source, np.ones((len(source), 1))])
            source_transformed = (transform @ source_h.T).T[:, :3]
            
            # Find correspondences
            tree = cKDTree(target)
            distances, indices = tree.query(source_transformed)
            
            # Filter by distance
            valid = distances < self.max_correspondence_distance
            source_valid = source_transformed[valid]
            target_valid = target[indices[valid]]
            
            if len(source_valid) < 3:
                break
            
            # Compute transformation
            R, t = self.rigid_transform_svd(source_valid, target_valid)
            
            # Update transform
            delta = np.eye(4)
            delta[:3, :3] = R
            delta[:3, 3] = t
            transform = delta @ transform
            
            # Check convergence
            if np.linalg.norm(t) < self.tolerance and np.abs(np.linalg.norm(R) - 1) < self.tolerance:
                break
        
        return transform
```

### Normal Estimation and Feature Extraction

```python
class PointCloudFeatures:
    def __init__(self, config):
        self.normal_radius = config.normal_radius
        self.fpfh_radius = config.fpfh_radius
    
    def compute_normals(self, points):
        tree = cKDTree(points)
        normals = np.zeros_like(points)
        
        for i, point in enumerate(points):
            neighbors_idx = tree.query_ball_point(point, self.normal_radius)
            if len(neighbors_idx) < 3:
                normals[i] = [0, 0, 1]
                continue
            
            neighbors = points[neighbors_idx]
            centroid = np.mean(neighbors, axis=0)
            cov = np.cov((neighbors - centroid).T)
            
            eigenvalues, eigenvectors = np.linalg.eigh(cov)
            normals[i] = eigenvectors[:, 0]  # smallest eigenvalue direction
        
        return normals
    
    def compute_fpfh(self, points, normals):
        tree = cKDTree(points)
        fpfh_features = []
        
        for i, point in enumerate(points):
            neighbors_idx = tree.query_ball_point(point, self.fpfh_radius)
            if len(neighbors_idx) < 3:
                fpfh_features.append(np.zeros(33))
                continue
            
            # Simplified FPFH computation
            spfh = self.compute_spfh(point, normals[i], points[neighbors_idx], normals[neighbors_idx])
            fpfh = self.weighted_spfh(point, spfh, neighbors_idx)
            fpfh_features.append(fpfh)
        
        return np.array(fpfh_features)
    
    def compute_spfh(self, point, normal, neighbors, neighbor_normals):
        hist = np.zeros(33)
        
        for nb, nb_normal in zip(neighbors, neighbor_normals):
            # Angular features
            diff = nb - point
            distance = np.linalg.norm(diff)
            
            alpha = np.arctan2(np.linalg.norm(np.cross(normal, diff)), np.dot(normal, diff))
            phi = np.arccos(np.dot(normal, nb_normal))
            theta = np.arctan2(np.linalg.norm(np.cross(normal, diff)), np.dot(normal, diff))
            
            # Bin into histogram
            hist[int(alpha / np.pi * 11)] += 1
            hist[11 + int(phi / (np.pi/2) * 11)] += 1
            hist[22 + int(theta / np.pi * 11)] += 1
        
        return hist
```
