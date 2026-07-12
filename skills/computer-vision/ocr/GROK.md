---
name: "ocr"
category: "computer-vision"
version: "2.0.0"
tags: ["computer-vision", "OCR", "text-recognition", "document-processing"]
---

# OCR (Optical Character Recognition)

## Overview

The OCR module provides comprehensive tools for extracting text from images, scanned documents, and video frames. It covers document layout analysis, text detection, text recognition, handwriting recognition, and post-processing with language models. The module supports both traditional OCR engines (Tesseract) and deep learning approaches (CRNN, TrOCR, PaddleOCR).

This skill is essential for document processing engineers, automation developers, and teams building intelligent document processing systems.

## Core Capabilities

- **Document Layout Analysis**: Page segmentation, region detection, table extraction, and reading order determination
- **Text Detection**: EAST, CRAFT, DBNet, and Mask R-CNN based text detection in natural scenes and documents
- **Text Recognition**: CRNN, TrOCR, and attention-based recognition for detected text regions
- **Handwriting Recognition**: Online and offline handwriting recognition with style adaptation
- **Language Support**: Multi-language OCR with script detection and language identification
- **Post-Processing**: Spell checking, language model correction, and structured output generation
- **Document Understanding**: Form extraction, key-value pair identification, and document classification
- **Quality Enhancement**: Image preprocessing for degraded documents, binarization, and deskewing

## Usage Examples

```python
from ocr import (
    DocumentProcessor,
    TextDetector,
    TextRecognizer,
    HandwritingRecognizer,
    PostProcessor,
)

# --- Full OCR Pipeline ---
processor = DocumentProcessor(language="eng")
result = processor.process("scanned_document.png")
print(f"Text: {result.text}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Words: {len(result.words)}")
print(f"Lines: {len(result.lines)}")

# --- Text Detection ---
detector = TextDetector(model="craft")
regions = detector.detect(image)
print(f"Detected {len(regions)} text regions")
for region in regions:
    print(f"  BBox: {region.bbox}, Confidence: {region.confidence:.2f}")

# --- Text Recognition ---
recognizer = TextRecognizer(model="trocr")
for region in regions:
    text = recognizer.recognize(image, region.bbox)
    print(f"  Recognized: '{text.text}' (conf: {text.confidence:.2f})")

# --- Handwriting ---
hw_recognizer = HandwritingRecognizer()
hw_result = hw_recognizer.recognize(handwriting_image)
print(f"Handwriting: {hw_result.text}")

# --- Post-Processing ---
post = PostProcessor()
corrected = post.correct("Helo Wrold", language="eng")
print(f"Corrected: {corrected}")

# --- Form Extraction ---
form = processor.extract_form("invoice.png")
for field in form.fields:
    print(f"  {field.name}: {field.value}")
```

## Best Practices

- Preprocess images before OCR: deskew, binarize, denoise, and remove borders
- Use CRAFT or DBNet for text detection in natural scene images
- Use TrOCR for highest accuracy on printed text; CRNN for speed
- Apply language model post-processing to correct recognition errors
- Handle multi-language documents with script detection before recognition
- Set appropriate confidence thresholds — reject low-confidence regions for review
- Use GPU acceleration for batch OCR processing to maximize throughput
- Process document layout first to determine reading order and structure
- Handle rotated text with rotation-invariant detection models
- Store OCR results with bounding boxes for downstream spatial queries

## Related Modules

- **image-processing**: Pre-processing for OCR quality improvement
- **object-detection**: General detection applicable to text regions
- **video-analysis**: Frame extraction for video OCR
- **face-recognition**: Document verification with face matching
