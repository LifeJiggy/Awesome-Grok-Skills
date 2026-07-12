---
name: "face-recognition"
category: "computer-vision"
version: "2.0.0"
tags: ["computer-vision", "face-recognition", "facial-detection", "biometrics"]
---

# Face Recognition

## Overview

The Face Recognition module provides comprehensive tools for face detection, landmark localization, face alignment, face embedding generation, and face recognition/matching. It covers classical approaches (Haar cascades, dlib), deep learning methods (MTCNN, RetinaFace, ArcFace, FaceNet), and production deployment patterns including anti-spoofing and privacy considerations.

This skill is essential for security engineers, biometric system developers, and computer vision teams building identity verification, access control, or facial analysis systems.

## Core Capabilities

- **Face Detection**: MTCNN, RetinaFace, BlazeFace, and Haar cascade-based detection with confidence scoring
- **Landmark Localization**: 5-point, 68-point, and 300-point facial landmark detection
- **Face Alignment**: Affine transformation for pose normalization using landmark-based alignment
- **Face Embeddings**: ArcFace, FaceNet, CosFace embedding generation for identity representation
- **Face Recognition**: 1:1 verification and 1:N identification with configurable similarity thresholds
- **Anti-Spoofing**: Liveness detection using texture analysis, depth estimation, and challenge-response
- **Attribute Analysis**: Age estimation, gender classification, emotion recognition, and gaze tracking
- **Privacy**: Face anonymization, GDPR compliance, and consent management patterns

## Usage Examples

```python
from face_recognition import (
    FaceDetector,
    LandmarkDetector,
    FaceAligner,
    EmbeddingGenerator,
    FaceRecognizer,
    AntiSpoofDetector,
)

# --- Face Detection ---
detector = FaceDetector(model="retinaface")
faces = detector.detect(image)
for face in faces:
    print(f"  Face: conf={face.confidence:.2f}, bbox=[{face.x1},{face.y1},{face.x2},{face.y2}]")

# --- Landmark Detection ---
landmarks = LandmarkDetector(model="68_point")
points = landmarks.detect(image, face_bbox=faces[0].bbox)
print(f"  Landmarks: {len(points)} points")

# --- Face Alignment ---
aligner = FaceAligner(output_size=(112, 112))
aligned = aligner.align(image, landmarks=points)
print(f"  Aligned face shape: {aligned.shape}")

# --- Embedding Generation ---
embedder = EmbeddingGenerator(model="arcface_r100")
embedding = embedder.generate(aligned)
print(f"  Embedding dim: {len(embedding)}")
print(f"  Norm: {sum(x**2 for x in embedding)**0.5:.3f}")

# --- Face Recognition ---
recognizer = FaceRecognizer(threshold=0.4)
recognizer.register("user_001", embedding)
matches = recognizer.identify(query_embedding=embedding)
for match in matches:
    print(f"  Match: {match.identity} (similarity: {match.similarity:.3f})")

# --- Anti-Spoofing ---
spoof_detector = AntiSpoofDetector()
is_live = spoof_detector.check_liveness(image)
print(f"  Liveness: {'Live' if is_live.is_live else 'Spoof'}")
print(f"  Confidence: {is_live.confidence:.2f}")
```

## Best Practices

- Use ArcFace or CosFace for state-of-the-art face embedding quality
- Always align faces before generating embeddings — alignment significantly improves accuracy
- Set recognition threshold based on application: 0.4 for verification, 0.6 for identification
- Implement anti-spoofing for any security-critical face recognition deployment
- Store face embeddings, not face images, for privacy compliance (GDPR, BIPA)
- Use 112x112 input size as the standard for ArcFace and FaceNet models
- Apply quality checks (blur, illumination, pose angle) before processing faces
- Use batch processing for embedding generation to maximize GPU utilization
- Implement template aging — re-register embeddings periodically to handle appearance changes
- Document consent and data retention policies for face biometric systems

## Related Modules

- **image-processing**: Pre-processing for face detection
- **object-detection**: General face detection as part of object detection
- **ocr**: Document verification with face matching
- **video-analysis**: Real-time face tracking in video streams
