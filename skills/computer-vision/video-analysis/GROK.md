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
