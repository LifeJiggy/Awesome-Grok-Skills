"""
OCR Module
Document processing, text detection, recognition, handwriting, and post-processing.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TextRegion:
    """Detected text region."""
    bbox: Tuple[int, int, int, int]
    confidence: float = 0.0
    text: str = ""
    angle: float = 0.0


@dataclass
class TextLine:
    """Recognized text line."""
    text: str
    confidence: float = 0.0
    bbox: Tuple[int, int, int, int] = (0, 0, 0, 0)
    words: List["WordResult"] = field(default_factory=list)


@dataclass
class WordResult:
    """Recognized word."""
    text: str
    confidence: float = 0.0
    bbox: Tuple[int, int, int, int] = (0, 0, 0, 0)


@dataclass
class OCRResult:
    """Full OCR result."""
    text: str
    confidence: float = 0.0
    lines: List[TextLine] = field(default_factory=list)
    words: List[WordResult] = field(default_factory=list)
    language: str = "eng"
    processing_time_ms: float = 0.0
    num_regions: int = 0


@dataclass
class FormField:
    """Extracted form field."""
    name: str
    value: str
    confidence: float = 0.0
    bbox: Tuple[int, int, int, int] = (0, 0, 0, 0)


@dataclass
class FormExtraction:
    """Form extraction result."""
    fields: List[FormField] = field(default_factory=list)
    num_fields: int = 0


@dataclass
class DocumentLayout:
    """Document layout analysis result."""
    page_width: int = 0
    page_height: int = 0
    text_regions: List[TextRegion] = field(default_factory=list)
    tables: int = 0
    images: int = 0
    reading_order: List[int] = field(default_factory=list)


@dataclass
class HandwritingResult:
    """Handwriting recognition result."""
    text: str
    confidence: float = 0.0
    words: List[WordResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Document Processor
# ---------------------------------------------------------------------------

class DocumentProcessor:
    """Full OCR pipeline for documents."""

    def __init__(self, language: str = "eng", use_gpu: bool = False):
        self.language = language
        self.use_gpu = use_gpu
        self._detector = TextDetector()
        self._recognizer = TextRecognizer()
        self._post = PostProcessor()

    def process(self, image_path: str) -> OCRResult:
        regions = self._detector.detect(None)
        lines: List[TextLine] = []
        words: List[WordResult] = []
        for region in regions:
            recog = self._recognizer.recognize(None, region.bbox)
            word = WordResult(text=recog.text, confidence=recog.confidence, bbox=region.bbox)
            words.append(word)
            lines.append(TextLine(text=recog.text, confidence=recog.confidence, words=[word]))

        full_text = " ".join(w.text for w in words)
        corrected = self._post.correct(full_text, self.language)
        avg_conf = sum(w.confidence for w in words) / max(len(words), 1)
        return OCRResult(
            text=corrected,
            confidence=round(avg_conf, 3),
            lines=lines,
            words=words,
            language=self.language,
            num_regions=len(regions),
        )

    def process_batch(self, image_paths: List[str]) -> List[OCRResult]:
        return [self.process(p) for p in image_paths]

    def extract_form(self, image_path: str) -> FormExtraction:
        result = self.process(image_path)
        fields: List[FormField] = []
        for word in result.words:
            if ":" in word.text:
                parts = word.text.split(":", 1)
                fields.append(FormField(name=parts[0].strip(), value=parts[1].strip()))
        return FormExtraction(fields=fields, num_fields=len(fields))


# ---------------------------------------------------------------------------
# Text Detector
# ---------------------------------------------------------------------------

class TextDetector:
    """Detect text regions in images."""

    def __init__(self, model: str = "craft", min_confidence: float = 0.5):
        self.model = model
        self.min_confidence = min_confidence

    def detect(self, image: Any) -> List[TextRegion]:
        return [
            TextRegion(bbox=(50, 50, 300, 80), confidence=0.98, text=""),
            TextRegion(bbox=(50, 100, 350, 130), confidence=0.95, text=""),
            TextRegion(bbox=(50, 150, 280, 180), confidence=0.92, text=""),
            TextRegion(bbox=(50, 200, 320, 230), confidence=0.88, text=""),
        ]


# ---------------------------------------------------------------------------
# Text Recognizer
# ---------------------------------------------------------------------------

class TextRecognizer:
    """Recognize text from detected regions."""

    def __init__(self, model: str = "trocr"):
        self.model = model

    def recognize(self, image: Any, bbox: Tuple[int, int, int, int]) -> WordResult:
        sample_texts = ["Invoice", "Date:", "Amount:", "Total:"]
        idx = bbox[1] // 50 % len(sample_texts)
        text = sample_texts[idx]
        conf = 0.95 - (bbox[1] % 10) * 0.01
        return WordResult(text=text, confidence=round(conf, 3), bbox=bbox)


# ---------------------------------------------------------------------------
# Handwriting Recognizer
# ---------------------------------------------------------------------------

class HandwritingRecognizer:
    """Recognize handwritten text."""

    def __init__(self, model: str = "hw_trocr"):
        self.model = model

    def recognize(self, image: Any) -> HandwritingResult:
        return HandwritingResult(
            text="Handwritten text sample",
            confidence=0.82,
            words=[WordResult("Handwritten", 0.85), WordResult("text", 0.80), WordResult("sample", 0.81)],
        )


# ---------------------------------------------------------------------------
# Post Processor
# ---------------------------------------------------------------------------

class PostProcessor:
    """Post-process OCR results."""

    COMMON_CORRECTIONS = {
        "Helo": "Hello",
        "Wrold": "World",
        "recieved": "received",
        "occured": "occurred",
        "seperate": "separate",
    }

    def correct(self, text: str, language: str = "eng") -> str:
        corrected = text
        for wrong, right in self.COMMON_CORRECTIONS.items():
            corrected = corrected.replace(wrong, right)
        return corrected

    def extract_structured(self, text: str) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for line in text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
        return result

    def confidence_filter(
        self, words: List[WordResult], threshold: float = 0.5
    ) -> List[WordResult]:
        return [w for w in words if w.confidence >= threshold]


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  OCR Demo")
    print("=" * 60)

    print("\n[1] Document Processing")
    processor = DocumentProcessor("eng")
    result = processor.process("document.png")
    print(f"  Text: {result.text}")
    print(f"  Confidence: {result.confidence:.2f}")
    print(f"  Words: {len(result.words)}")

    print("\n[2] Text Detection")
    detector = TextDetector("craft")
    regions = detector.detect(None)
    print(f"  Detected: {len(regions)} regions")

    print("\n[3] Text Recognition")
    recognizer = TextRecognizer("trocr")
    for region in regions[:3]:
        recog = recognizer.recognize(None, region.bbox)
        print(f"  '{recog.text}' (conf: {recog.confidence:.2f})")

    print("\n[4] Handwriting")
    hw = HandwritingRecognizer()
    hw_result = hw.recognize(None)
    print(f"  Text: {hw_result.text}")
    print(f"  Confidence: {hw_result.confidence:.2f}")

    print("\n[5] Post-Processing")
    post = PostProcessor()
    corrected = post.correct("Helo Wrold")
    print(f"  Corrected: {corrected}")

    print("\n[6] Form Extraction")
    form = processor.extract_form("invoice.png")
    print(f"  Fields: {form.num_fields}")

    print("\n" + "=" * 60)
    print("  OCR demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
