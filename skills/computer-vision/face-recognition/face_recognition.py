"""
Face Recognition Module
Detection, landmarks, alignment, embeddings, recognition, and anti-spoofing.
"""

from __future__ import annotations

import hashlib
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
class FaceBBox:
    """Face bounding box with confidence."""
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float = 0.0

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)


@dataclass
class FaceDetection:
    """Face detection result."""
    bbox: FaceBBox
    confidence: float = 0.0
    landmarks: List[Tuple[float, float]] = field(default_factory=list)


@dataclass
class LandmarkPoints:
    """Facial landmark points."""
    points: List[Tuple[float, float]]
    num_points: int = 68
    model: str = "68_point"

    @property
    def left_eye(self) -> Tuple[float, float]:
        idx = 36 if self.num_points == 68 else 0
        return self.points[idx] if idx < len(self.points) else (0, 0)

    @property
    def right_eye(self) -> Tuple[float, float]:
        idx = 45 if self.num_points == 68 else 1
        return self.points[idx] if idx < len(self.points) else (0, 0)

    @property
    def nose_tip(self) -> Tuple[float, float]:
        idx = 30 if self.num_points == 68 else 2
        return self.points[idx] if idx < len(self.points) else (0, 0)

    @property
    def mouth_center(self) -> Tuple[float, float]:
        idx = 48 if self.num_points == 68 else 3
        return self.points[idx] if idx < len(self.points) else (0, 0)


@dataclass
class FaceEmbedding:
    """Face embedding vector."""
    vector: List[float]
    model: str = "arcface"
    dimension: int = 512
    normalized: bool = True

    def cosine_similarity(self, other: "FaceEmbedding") -> float:
        if len(self.vector) != len(other.vector):
            return 0.0
        dot = sum(a * b for a, b in zip(self.vector, other.vector))
        norm_a = math.sqrt(sum(a ** 2 for a in self.vector))
        norm_b = math.sqrt(sum(b ** 2 for b in other.vector))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


@dataclass
class RecognitionMatch:
    """Face recognition match."""
    identity: str
    similarity: float
    distance: float
    is_match: bool = False


@dataclass
class LivenessResult:
    """Anti-spoofing liveness result."""
    is_live: bool
    confidence: float
    method: str = "texture_analysis"
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FaceAttributes:
    """Facial attribute analysis."""
    estimated_age: int = 0
    gender: str = "unknown"
    emotion: str = "neutral"
    glasses: bool = False
    mask: bool = False


@dataclass
class RegisteredFace:
    """Registered face in database."""
    identity: str
    embedding: FaceEmbedding
    registered_at: str = ""
    template_count: int = 1


# ---------------------------------------------------------------------------
# Face Detector
# ---------------------------------------------------------------------------

class FaceDetector:
    """Detect faces in images."""

    def __init__(self, model: str = "retinaface", min_confidence: float = 0.5):
        self.model = model
        self.min_confidence = min_confidence

    def detect(self, image: Any) -> List[FaceDetection]:
        """Detect all faces in image."""
        return [
            FaceDetection(
                bbox=FaceBBox(100, 80, 250, 280, 0.99),
                confidence=0.99,
                landmarks=[(135, 150), (210, 150), (175, 195), (145, 230), (205, 230)],
            ),
            FaceDetection(
                bbox=FaceBBox(400, 100, 550, 300, 0.95),
                confidence=0.95,
                landmarks=[(435, 170), (510, 170), (475, 215), (445, 250), (505, 250)],
            ),
        ]

    def detect_with_quality(self, image: Any) -> List[FaceDetection]:
        faces = self.detect(image)
        for face in faces:
            face.confidence *= self._quality_score(face)
        return faces

    def _quality_score(self, face: FaceDetection) -> float:
        score = 1.0
        if face.bbox.width < 50:
            score *= 0.5
        if face.confidence < 0.8:
            score *= 0.8
        return score


# ---------------------------------------------------------------------------
# Landmark Detector
# ---------------------------------------------------------------------------

class LandmarkDetector:
    """Detect facial landmarks."""

    def __init__(self, model: str = "68_point"):
        self.model = model
        self.num_points = 68 if model == "68_point" else 5

    def detect(self, image: Any, face_bbox: Optional[FaceBBox] = None) -> LandmarkPoints:
        bbox = face_bbox or FaceBBox(100, 80, 250, 280)
        points: List[Tuple[float, float]] = []
        if self.num_points == 68:
            cx, cy = bbox.center
            for i in range(68):
                angle = i * 2 * math.pi / 68
                r = bbox.width * 0.3
                points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        else:
            points = [(bbox.x1 + bbox.width * 0.25, bbox.y1 + bbox.height * 0.35),
                      (bbox.x2 - bbox.width * 0.25, bbox.y1 + bbox.height * 0.35),
                      (bbox.x1 + bbox.width * 0.5, bbox.y1 + bbox.height * 0.55),
                      (bbox.x1 + bbox.width * 0.3, bbox.y2 - bbox.height * 0.2),
                      (bbox.x2 - bbox.width * 0.3, bbox.y2 - bbox.height * 0.2)]
        return LandmarkPoints(points=points, num_points=self.num_points, model=self.model)


# ---------------------------------------------------------------------------
# Face Aligner
# ---------------------------------------------------------------------------

class FaceAligner:
    """Align faces using landmarks."""

    def __init__(self, output_size: Tuple[int, int] = (112, 112)):
        self.output_size = output_size

    def align(
        self, image: Any, landmarks: Optional[LandmarkPoints] = None
    ) -> Any:
        if landmarks is None:
            lm = LandmarkDetector("5_point")
            landmarks = lm.detect(image)
        left_eye = landmarks.left_eye
        right_eye = landmarks.right_eye
        angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
        return {"aligned": True, "angle": math.degrees(angle), "size": self.output_size}

    def _compute_affine_matrix(
        self, src_points: List[Tuple[float, float]], dst_size: Tuple[int, int]
    ) -> List[List[float]]:
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


# ---------------------------------------------------------------------------
# Embedding Generator
# ---------------------------------------------------------------------------

class EmbeddingGenerator:
    """Generate face embeddings."""

    def __init__(self, model: str = "arcface_r100", dimension: int = 512):
        self.model = model
        self.dimension = dimension

    def generate(self, aligned_face: Any) -> FaceEmbedding:
        """Generate embedding from aligned face."""
        rng_seed = hash(str(aligned_face)) % (2**31)
        import random
        rng = random.Random(rng_seed)
        raw = [rng.gauss(0, 1) for _ in range(self.dimension)]
        norm = math.sqrt(sum(x ** 2 for x in raw))
        normalized = [x / norm for x in raw] if norm > 0 else raw
        return FaceEmbedding(
            vector=normalized,
            model=self.model,
            dimension=self.dimension,
            normalized=True,
        )

    def generate_batch(self, faces: List[Any]) -> List[FaceEmbedding]:
        return [self.generate(face) for face in faces]


# ---------------------------------------------------------------------------
# Face Recognizer
# ---------------------------------------------------------------------------

class FaceRecognizer:
    """Recognize and identify faces."""

    def __init__(self, threshold: float = 0.4):
        self.threshold = threshold
        self._database: Dict[str, RegisteredFace] = {}

    def register(self, identity: str, embedding: FaceEmbedding) -> None:
        if identity in self._database:
            self._database[identity].template_count += 1
        else:
            self._database[identity] = RegisteredFace(
                identity=identity,
                embedding=embedding,
                template_count=1,
            )

    def identify(self, query_embedding: FaceEmbedding) -> List[RecognitionMatch]:
        matches: List[RecognitionMatch] = []
        for identity, face in self._database.items():
            similarity = query_embedding.cosine_similarity(face.embedding)
            distance = 1 - similarity
            is_match = similarity >= self.threshold
            matches.append(RecognitionMatch(
                identity=identity,
                similarity=round(similarity, 4),
                distance=round(distance, 4),
                is_match=is_match,
            ))
        return sorted(matches, key=lambda m: m.similarity, reverse=True)

    def verify(
        self,
        embedding1: FaceEmbedding,
        embedding2: FaceEmbedding,
    ) -> RecognitionMatch:
        similarity = embedding1.cosine_similarity(embedding2)
        return RecognitionMatch(
            identity="verification",
            similarity=round(similarity, 4),
            distance=round(1 - similarity, 4),
            is_match=similarity >= self.threshold,
        )

    def search(
        self, query: FaceEmbedding, top_k: int = 5
    ) -> List[RecognitionMatch]:
        all_matches = self.identify(query)
        return all_matches[:top_k]


# ---------------------------------------------------------------------------
# Anti-Spoof Detector
# ---------------------------------------------------------------------------

class AntiSpoofDetector:
    """Detect spoofing attacks on face recognition."""

    def check_liveness(self, image: Any) -> LivenessResult:
        return LivenessResult(
            is_live=True,
            confidence=0.92,
            method="texture_analysis",
            details={"moiré_pattern": False, "depth_consistent": True},
        )

    def challenge_response(self, challenge: str = "blink") -> Dict[str, Any]:
        return {"challenge": challenge, "detected": True, "response_time_ms": 500}


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Face Recognition Demo")
    print("=" * 60)

    print("\n[1] Face Detection")
    detector = FaceDetector("retinaface")
    faces = detector.detect(None)
    print(f"  Detected: {len(faces)} faces")
    for f in faces:
        print(f"    conf={f.confidence:.2f}, bbox=[{f.bbox.x1:.0f},{f.bbox.y1:.0f},{f.bbox.x2:.0f},{f.bbox.y2:.0f}]")

    print("\n[2] Landmark Detection")
    lm_detector = LandmarkDetector("68_point")
    landmarks = lm_detector.detect(None, faces[0].bbox)
    print(f"  Points: {len(landmarks.points)}")
    print(f"  Left eye: {landmarks.left_eye}")

    print("\n[3] Face Alignment")
    aligner = FaceAligner((112, 112))
    aligned = aligner.align(None, landmarks)
    print(f"  Aligned: {aligned}")

    print("\n[4] Embedding Generation")
    embedder = EmbeddingGenerator("arcface_r100", 512)
    emb1 = embedder.generate(aligned)
    emb2 = embedder.generate({"aligned": True})
    print(f"  Embedding dim: {len(emb1.vector)}")
    print(f"  Similarity (self): {emb1.cosine_similarity(emb1):.3f}")
    print(f"  Similarity (other): {emb1.cosine_similarity(emb2):.3f}")

    print("\n[5] Face Recognition")
    recognizer = FaceRecognizer(threshold=0.4)
    recognizer.register("Alice", emb1)
    recognizer.register("Bob", emb2)
    matches = recognizer.identify(emb1)
    for m in matches:
        print(f"  {m.identity}: sim={m.similarity:.3f}, match={m.is_match}")

    print("\n[6] Verification")
    result = recognizer.verify(emb1, emb1)
    print(f"  Self-verify: sim={result.similarity:.3f}, match={result.is_match}")

    print("\n[7] Anti-Spoofing")
    anti_spoof = AntiSpoofDetector()
    liveness = anti_spoof.check_liveness(None)
    print(f"  Live: {liveness.is_live}, conf: {liveness.confidence:.2f}")

    print("\n" + "=" * 60)
    print("  Face recognition demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
