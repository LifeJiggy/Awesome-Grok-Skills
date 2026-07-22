---
name: "video-analysis"
category: "computer-vision"
version: "2.0.0"
tags: ["computer-vision", "video-analysis", "action-recognition", "tracking", "video-processing"]
---

# Video Analysis

## Overview

The Video Analysis module provides comprehensive tools for processing, analyzing, and extracting insights from video data. It covers video I/O, frame extraction, object tracking, action recognition, video summarization, anomaly detection, and video understanding. The module integrates temporal models, multi-object tracking, and video-specific pre/post-processing.

This skill is essential for video analytics engineers, surveillance system developers, sports analysts, and teams building real-time video understanding systems.

## Core Capabilities

- **Video I/O**: Frame extraction, video encoding/decoding, streaming, and format conversion
- **Object Tracking**: DeepSORT, ByteTrack, and FairMOT for multi-object tracking across frames
- **Action Recognition**: Temporal modeling with SlowFast, TimeSformer, and video transformers
- **Video Summarization**: Key frame selection, highlight detection, and story generation
- **Anomaly Detection**: Temporal anomaly detection for surveillance and manufacturing quality
- **Scene Understanding**: Scene classification, change detection, and temporal segmentation
- **Pose Estimation**: Video pose estimation, action pose sequences, and motion analysis
- **Real-Time Processing**: GPU-accelerated pipelines, frame batching, and streaming inference

## Usage Examples

```python
from video_analysis import (
    VideoProcessor,
    ObjectTracker,
    ActionRecognizer,
    VideoSummarizer,
    AnomalyDetector,
)

# --- Video Processing ---
processor = VideoProcessor()
frames = processor.extract_frames("video.mp4", fps=1)
print(f"Extracted {len(frames)} frames")

info = processor.get_video_info("video.mp4")
print(f"Duration: {info.duration_seconds:.1f}s")
print(f"Resolution: {info.width}x{info.height}")
print(f"FPS: {info.fps}")

# --- Object Tracking ---
tracker = ObjectTracker(model="bytetrack")
tracks = tracker.track(video_path="surveillance.mp4")
for track in tracks[:5]:
    print(f"  ID={track.track_id}: {track.class_name} ({track.frames_tracked} frames)")

# --- Action Recognition ---
recognizer = ActionRecognizer(model="slowfast_r101")
actions = recognizer.recognize(video_path="sports.mp4")
for action in actions:
    print(f"  {action.label}: {action.confidence:.2f} ({action.start_time:.1f}s-{action.end_time:.1f}s)")

# --- Video Summarization ---
summarizer = VideoSummarizer()
summary = summarizer.summarize("long_video.mp4", target_duration_seconds=30)
print(f"Summary: {len(summary.keyframes)} keyframes")
print(f"Highlights: {len(summary.highlights)} scenes")

# --- Anomaly Detection ---
anomaly_detector = AnomalyDetector()
anomalies = anomaly_detector.detect("cctv_footage.mp4")
for anomaly in anomalies:
    print(f"  Anomaly at {anomaly.timestamp:.1f}s: {anomaly.type} (score: {anomaly.score:.2f})")
```

## Best Practices

- Extract frames at the minimum FPS needed for your task — 1 FPS for surveillance, 15-30 FPS for action recognition
- Use ByteTrack for real-time tracking — it's faster than DeepSORT with comparable accuracy
- Apply temporal smoothing for track IDs to reduce identity switches
- Use keyframe extraction to reduce processing load for long videos
- Implement frame skipping for real-time applications to maintain FPS targets
- Use GPU batching for action recognition to maximize throughput
- Store tracking results as CSV/JSON for downstream analysis
- Apply scene change detection before expensive per-frame analysis
- Use video codecs (H.265/HEVC) for storage-efficient archival
- Implement progress callbacks for long video processing to track completion

## Related Modules

- **image-processing**: Per-frame image processing within videos
- **object-detection**: Frame-by-frame detection for tracking initialization
- **face-recognition**: Face tracking and recognition in video streams
- **ocr**: Text extraction from video frames

## Architecture Patterns

### Video Processing Pipeline

```
Video Input → Frame Extraction → Processing → Analysis → Output

Frame Extraction:
├── Decode video stream
├── Extract frames at target FPS
├── Keyframe selection
├── Scene change detection
└── Frame buffering

Processing:
├── Preprocessing (resize, normalize)
├── Object detection per frame
├── Feature extraction
├── Temporal aggregation
└── Batch GPU processing

Analysis:
├── Object tracking
├── Action recognition
├── Anomaly detection
├── Scene classification
└── Event detection

Output:
├── Video annotations
├── Tracking CSV/JSON
├── Summary statistics
├── Alert notifications
└── Annotated video
```

### Multi-Object Tracking Architecture

```
Detection → Association → Track Management → Output

Detection:
├── YOLO/Faster R-CNN per frame
├── Confidence filtering
├── NMS (Non-Maximum Suppression)
└── Feature extraction (ReID)

Association:
├── IoU matching
├── Hungarian algorithm
├── Appearance similarity (cosine)
└── Motion prediction (Kalman)

Track Management:
├── Track creation (new detection)
├── Track update (matched detection)
├── Track prediction (unmatched frame)
├── Track deletion (lost threshold)
└── Track ID assignment

Output:
├── Track history (bbox, timestamp)
├── Track statistics (duration, speed)
├── Identity assignment
└──行为 patterns
```

### Action Recognition Pipeline

```
Video → Temporal Sampling → Feature Extraction → Classification → Actions

Temporal Sampling:
├── Uniform sampling (N frames)
├── Dense sampling (all frames)
├── Keyframe sampling (scene changes)
└── Strided sampling (every K frames)

Feature Extraction:
├── 3D CNN (SlowFast, R(2+1)D)
├── Video Transformer (TimeSformer, ViViT)
├── 2D CNN + temporal pooling
└── Pretrained backbone (ResNet, EfficientNet)

Classification:
├── Single-label (softmax)
├── Multi-label (sigmoid)
├── Temporal localization (start/end)
└── Confidence scoring
```

### Video Anomaly Detection Architecture

```
Normal Pattern Learning → Anomaly Scoring → Alert Generation

Normal Pattern Learning:
├── Autoencoder reconstruction
├── Predictive modeling (future frame prediction)
├── Clustering of normal patterns
└── Memory bank of normal features

Anomaly Scoring:
├── Reconstruction error
├── Prediction error
├── Feature distribution distance
└── Temporal inconsistency

Alert Generation:
├── Threshold-based alerts
├── Adaptive thresholds (seasonal)
├── Severity classification
└── Notification routing
```

## Model Selection Guide

### Detection Model for Video

| Model | FPS (GPU) | mAP | Best For |
|-------|-----------|-----|----------|
| YOLOv8n | 300+ | 37.3 | Real-time tracking |
| YOLOv8s | 200+ | 44.9 | Balanced |
| YOLOv8m | 100+ | 50.2 | High accuracy |
| YOLOv8x | 30+ | 53.9 | Maximum accuracy |
| RT-DETR | 150+ | 53.0 | End-to-end |

### Tracking Model Comparison

| Tracker | FPS | MOTA | IDF1 | Best For |
|---------|-----|------|------|----------|
| ByteTrack | 30+ | 78.2 | 79.1 | Speed |
| DeepSORT | 15 | 75.4 | 77.5 | Appearance |
| BoT-SORT | 25 | 80.1 | 81.3 | Balanced |
| FairMOT | 20 | 74.9 | 72.8 | Joint detection |
| QD-3DT | 10 | 82.3 | 84.1 | 3D tracking |

### Action Recognition Model Comparison

| Model | Accuracy | FPS | Latency | Best For |
|-------|----------|-----|---------|----------|
| SlowFast-R101 | 79.8% | 30 | 15ms | General actions |
| TimeSformer | 81.0% | 15 | 30ms | High accuracy |
| Video Swin | 82.5% | 10 | 50ms | State-of-the-art |
| X3D | 77.4% | 80 | 5ms | Edge deployment |
| MobileNet-V2+LSTM | 73.2% | 100 | 2ms | Mobile/edge |

## Integration Guide

### FFmpeg Integration

```python
import subprocess
import cv2
import numpy as np

class VideoIO:
    def __init__(self):
        pass

    def extract_frames_ffmpeg(self, video_path, output_dir, fps=1):
        """Extract frames using FFmpeg for speed."""
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vf', f'fps={fps}',
            f'{output_dir}/frame_%06d.jpg',
            '-loglevel', 'quiet'
        ]
        subprocess.run(cmd, check=True)

    def get_video_info(self, video_path):
        """Get video metadata using FFprobe."""
        cmd = [
            'ffprobe', '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)

    def create_annotated_video(self, frames, output_path, fps=30):
        """Create video from annotated frames."""
        if not frames:
            return
        h, w = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
        for frame in frames:
            writer.write(frame)
        writer.release()
```

### ByteTrack Integration

```python
import numpy as np
from bytetracker import ByteTracker

class VideoTracker:
    def __init__(self, track_thresh=0.5, match_thresh=0.8, track_buffer=30):
        self.tracker = ByteTracker(
            track_thresh=track_thresh,
            match_thresh=match_thresh,
            track_buffer=track_buffer
        )

    def process_video(self, video_path, detector, fps=5):
        """Track objects across video frames."""
        cap = cv2.VideoCapture(video_path)
        frame_interval = int(cap.get(cv2.CAP_PROP_FPS) / fps)

        tracks = []
        frame_idx = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_interval == 0:
                detections = detector.detect(frame)
                online_targets = self.tracker.update(
                    detections.boxes, detections scores, detections.features
                )

                for t in online_targets:
                    tracks.append({
                        'frame': frame_idx,
                        'track_id': t.track_id,
                        'bbox': t.tlwh,
                        'class': t.class_name,
                        'score': t.score
                    })

            frame_idx += 1

        cap.release()
        return tracks
```

### SlowFast Action Recognition

```python
import torch
import torchvision.transforms as transforms

class ActionRecognizer:
    def __init__(self, model_name="slowfast_r101", num_classes=400):
        self.model = load_model(model_name, num_classes)
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.45, 0.45, 0.45],
                std=[0.225, 0.225, 0.225]
            )
        ])

    def recognize_actions(self, video_path, clip_length=32, stride=16):
        """Recognize actions in video using sliding window."""
        frames = load_video_frames(video_path)
        actions = []

        for start in range(0, len(frames) - clip_length, stride):
            clip = frames[start:start + clip_length]
            clip_tensor = self.prepare_clip(clip)

            with torch.no_grad():
                output = self.model(clip_tensor)
                probs = torch.softmax(output, dim=1)
                pred_class = torch.argmax(probs, dim=1).item()
                confidence = probs[0, pred_class].item()

            actions.append({
                'start_frame': start,
                'end_frame': start + clip_length,
                'action': self.class_names[pred_class],
                'confidence': confidence
            })

        return self.merge_actions(actions)

    def prepare_clip(self, frames):
        """Prepare clip tensor for model input."""
        processed = [self.transform(f) for f in frames]
        return torch.stack(processed).unsqueeze(0)
```

### Anomaly Detection Integration

```python
import torch
import torch.nn as nn

class VideoAnomalyDetector:
    def __init__(self, model="autoencoder", threshold=0.1):
        self.model = self.load_model(model)
        self.threshold = threshold
        self.memory_bank = None

    def train_normal(self, normal_videos, epochs=50):
        """Train on normal video patterns only."""
        for epoch in range(epochs):
            for video in normal_videos:
                frames = self.extract_features(video)
                reconstructed = self.model(frames)
                loss = nn.MSELoss()(reconstructed, frames)
                loss.backward()
                self.optimizer.step()

        # Build memory bank of normal features
        self.memory_bank = self.build_memory_bank(normal_videos)

    def detect_anomalies(self, video_path, window_size=32):
        """Detect anomalous frames in video."""
        frames = self.extract_features(video_path)
        anomalies = []

        for i in range(0, len(frames) - window_size):
            window = frames[i:i + window_size]

            # Reconstruction error
            reconstructed = self.model(window)
            error = torch.mean((window - reconstructed) ** 2).item()

            # Memory bank distance
            if self.memory_bank is not None:
                distance = self.compute_memory_distance(window)
                combined_score = 0.7 * error + 0.3 * distance
            else:
                combined_score = error

            if combined_score > self.threshold:
                anomalies.append({
                    'start_frame': i,
                    'end_frame': i + window_size,
                    'score': combined_score,
                    'type': self.classify_anomaly(window)
                })

        return anomalies
```

## Performance Optimization

### Frame Processing Optimization

| Technique | Description | Speedup |
|-----------|-------------|---------|
| Frame skipping | Process every Nth frame | Nx |
| ROI processing | Process only regions of interest | 2-5x |
| Batch inference | Process multiple frames together | 2-4x |
| TensorRT | Optimized GPU inference | 3-5x |
| Multi-threading | Parallel decode + inference | 1.5-2x |

### GPU Memory Management

```python
class GPUMemoryManager:
    def __init__(self, max_batch_size=16):
        self.max_batch_size = max_batch_size
        self.current_batch = []

    def process_frame(self, frame, detector):
        """Process frame with memory-aware batching."""
        self.current_batch.append(frame)

        if len(self.current_batch) >= self.max_batch_size:
            self.flush_batch(detector)

    def flush_batch(self, detector):
        """Process accumulated batch."""
        if not self.current_batch:
            return

        batch_tensor = torch.stack(self.current_batch)
        with torch.cuda.amp.autocast():
            results = detector.detect_batch(batch_tensor)

        self.current_batch.clear()
        torch.cuda.empty_cache()
        return results
```

### Real-Time Processing Pipeline

```python
import threading
import queue

class RealTimeProcessor:
    def __init__(self, target_fps=30, buffer_size=64):
        self.target_fps = target_fps
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.result_queue = queue.Queue()
        self.running = False

    def start(self, video_source, detector, tracker):
        """Start real-time processing pipeline."""
        self.running = True

        # Decoder thread
        decoder_thread = threading.Thread(
            target=self._decode_loop, args=(video_source,)
        )

        # Inference thread
        inference_thread = threading.Thread(
            target=self._inference_loop, args=(detector, tracker)
        )

        decoder_thread.start()
        inference_thread.start()

        return self.result_queue

    def _decode_loop(self, video_source):
        """Decode frames and add to queue."""
        cap = cv2.VideoCapture(video_source)
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if not self.frame_queue.full():
                self.frame_queue.put(frame)
        cap.release()

    def _inference_loop(self, detector, tracker):
        """Process frames from queue."""
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                detections = detector.detect(frame)
                tracks = tracker.update(detections)
                self.result_queue.put(tracks)
```

## Security Considerations

### Video Privacy

| Control | Description | Implementation |
|---------|-------------|----------------|
| Face Blurring | Anonymize faces | RetinaFace + Gaussian blur |
| License Plate Masking | Hide plate numbers | YOLO-Plate + crop |
| Region Redaction | Black out sensitive areas | Custom ROI masking |
| Access Control | Restrict video access | RBAC + encryption |
| Retention Policies | Auto-delete old footage | Lifecycle rules |

### Secure Video Storage

```
Security Layers:
├── Encryption at rest (AES-256)
├── Encryption in transit (TLS 1.3)
├── Access logging (CloudTrail/Audit)
├── Version control (immutable)
├── Backup replication (cross-region)
└── Retention automation (lifecycle)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Frame drops | Choppy output | Reduce target FPS, optimize decoder |
| Memory overflow | OOM during processing | Reduce batch size, process in chunks |
| Tracking ID switches | Inconsistent IDs | Increase track buffer, tune match thresh |
| High latency | Slow real-time | Use TensorRT, reduce model size |
| GPU utilization low | Underutilized GPU | Increase batch size, use multi-stream |
| Codec issues | Corrupt output | Use H.264 codec, check FFmpeg version |

### Debugging Commands

```bash
# Check video properties
ffprobe -v error -show_entries stream=width,height,r_frame_rate,codec_name video.mp4

# Monitor GPU usage
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 1

# Profile inference time
python -c "
import time
from video_analysis import VideoProcessor
vp = VideoProcessor()
start = time.time()
vp.process('video.mp4', fps=5)
print(f'Processing time: {time.time()-start:.2f}s')
"

# Check frame extraction
ffmpeg -i video.mp4 -vf fps=1 -f null - 2>&1 | grep "frame="
```

## API Reference

### VideoProcessor

```python
class VideoProcessor:
    def extract_frames(
        video_path: str,
        fps: float = 1.0,
        output_format: str = "jpg",
    ) -> list[np.ndarray]:
        """Extract frames from video at specified FPS."""

    def get_video_info(
        video_path: str,
    ) -> VideoInfo:
        """Get video metadata (duration, resolution, codec)."""

    def create_video(
        frames: list[np.ndarray],
        output_path: str,
        fps: int = 30,
        codec: str = "mp4v",
    ) -> str:
        """Create video from frames."""
```

### ObjectTracker

```python
class ObjectTracker:
    def track(
        video_path: str,
        model: str = "bytetrack",
        confidence: float = 0.5,
    ) -> list[Track]:
        """Track objects across video frames."""

    def track_realtime(
        video_source: str | int,
        model: str = "bytetrack",
    ) -> Generator[Track, None, None]:
        """Real-time tracking from camera stream."""
```

### ActionRecognizer

```python
class ActionRecognizer:
    def recognize(
        video_path: str,
        model: str = "slowfast_r101",
        clip_length: int = 32,
    ) -> list[Action]:
        """Recognize actions in video."""

    def recognize_stream(
        self,
        frame_generator: Generator,
        model: str = "slowfast_r101",
    ) -> Generator[Action, None, None]:
        """Real-time action recognition."""
```

### VideoSummarizer

```python
class VideoSummarizer:
    def summarize(
        video_path: str,
        target_duration_seconds: int = 30,
        method: str = "keyframe",
    ) -> VideoSummary:
        """Create video summary with keyframes and highlights."""

    def detect_highlights(
        video_path: str,
        sensitivity: float = 0.5,
    ) -> list[Highlight]:
        """Detect highlight moments in video."""
```

## Data Models

### VideoInfo

```
VideoInfo:
  path: str
  duration_seconds: float
  width: int
  height: int
  fps: float
  codec: str
  total_frames: int
  file_size_mb: float
```

### Track

```
Track:
  track_id: int
  class_name: str
  frames: list[FrameDetection]
  start_frame: int
  end_frame: int
  duration_frames: int
  avg_confidence: float
  bbox_trajectory: list[tuple]
```

### FrameDetection

```
FrameDetection:
  frame_idx: int
  timestamp: float
  detections: list[Detection]
  features: np.ndarray
```

### Action

```
Action:
  label: str
  confidence: float
  start_time: float
  end_time: float
  start_frame: int
  end_frame: int
  class_id: int
```

### VideoSummary

```
VideoSummary:
  keyframes: list[Keyframe]
  highlights: list[Highlight]
  duration_seconds: float
  summary_duration_seconds: float
  compression_ratio: float
  scene_changes: list[SceneChange]
```

## Deployment Guide

### Video Analytics Deployment

```
1. Prerequisites
   ├── GPU server (NVIDIA T4+)
   ├── FFmpeg installed
   ├── Python 3.10+
   └── CUDA toolkit

2. Deployment
   ├── Install dependencies
   ├── Download models
   ├── Configure GPU
   ├── Set up streaming
   └── Enable monitoring

3. Post-Deployment
   ├── Test with sample video
   ├── Verify tracking accuracy
   ├── Configure alerts
   └── Set up dashboards
```

### CI/CD Pipeline

```yaml
# .github/workflows/video-analytics.yml
name: Video Analytics CI/CD
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
      - name: Benchmark
        run: python benchmarks/run_benchmark.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to cloud
        run: |
          docker build -t video-analytics .
          docker push video-analytics:latest
```

## Monitoring & Observability

### Key Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Processing FPS | >15 | Frames processed per second |
| Tracking Accuracy | >80% MOTA | Multi-object tracking accuracy |
| Action Accuracy | >75% | Action recognition accuracy |
| Latency P99 | <100ms | 99th percentile latency |
| Memory Usage | <8GB | GPU memory usage |
| GPU Utilization | >70% | GPU usage percentage |

### Monitoring Dashboard

```
Video Analytics Dashboard:
├── Processing throughput (FPS)
├── Active tracks count
├── Detection accuracy
├── Tracking accuracy
├── Action recognition rate
├── Anomaly alerts
├── GPU utilization
├── Memory usage
├── Error rate
└── Pipeline latency
```

## Testing Strategy

### Video Analysis Tests

```
1. Unit Tests
   ├── Frame extraction
   ├── Detection functions
   ├── Tracking logic
   └── Action classification

2. Integration Tests
   ├── End-to-end pipeline
   ├── Multi-video processing
   ├── Real-time streaming
   └── API endpoints

3. Accuracy Tests
   ├── MOT17/MOT20 benchmark
   ├── ImageNet-1K action
   ├── Custom dataset
   └── Edge cases (occlusion, blur)

4. Performance Tests
   ├── Throughput benchmarks
   ├── Latency benchmarks
   ├── Memory profiling
   └── GPU utilization
```

## Versioning & Migration

### Versioning

```
Major: Architecture change
├── Example: New tracker algorithm
├── Requires: Full retraining
└── Risk: High

Minor: New features
├── Example: Add action recognition
├── Requires: Testing
└── Risk: Low

Patch: Bug fixes
├── Example: Fix tracking ID issue
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| ByteTrack | High-performance multi-object tracker |
| ByteTrack | Multi-object tracking algorithm |
| DeepSORT | Deep learning-based SORT tracker |
| FPS | Frames per second |
| IoU | Intersection over Union |
| MOTA | Multiple Object Tracking Accuracy |
| MOT | Multiple Object Tracking |
| ReID | Re-Identification |
| SlowFast | Two-pathway action recognition model |
| TimeSformer | Video Transformer for action recognition |
| YOLO | You Only Look Once detector |

## Changelog

### v2.0.0
- Added ByteTrack support
- Added action recognition
- Added anomaly detection
- Improved real-time processing

### v1.2.0
- Added DeepSORT tracking
- Added video summarization
- Improved GPU optimization

### v1.1.0
- Added frame extraction
- Added scene detection
- Improved tracking

### v1.0.0
- Initial release with basic tracking
- Simple frame processing
- Basic detection

---

## Contributing Guidelines

- Test with diverse video sources
- Document model performance
- Include benchmark results
- Handle edge cases (occlusion, blur)

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
