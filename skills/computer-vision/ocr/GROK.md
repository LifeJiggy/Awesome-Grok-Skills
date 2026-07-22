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
- Set appropriate confidence thresholds â€” reject low-confidence regions for review
- Use GPU acceleration for batch OCR processing to maximize throughput
- Process document layout first to determine reading order and structure
- Handle rotated text with rotation-invariant detection models
- Store OCR results with bounding boxes for downstream spatial queries

## Related Modules

- **image-processing**: Pre-processing for OCR quality improvement
- **object-detection**: General detection applicable to text regions
- **video-analysis**: Frame extraction for video OCR
- **face-recognition**: Document verification with face matching

## Architecture Patterns

### Detection-Recognition Pipeline

The most common OCR architecture separates text detection and recognition into two stages. A text detector (CRAFT, DBNet, or EAST) first localizes text regions in the image. Each detected region is then cropped, rectified (for curved text), and passed to a recognition model (TrOCR, CRNN, or PARSeq).

```
Input Image â†’ Text Detector â†’ Bounding Boxes â†’ Perspective Transform â†’ Crop/Rectify â†’ Recognition Model â†’ Text
```

This two-stage approach allows independent optimization of detection and recognition. The detector can focus on recall (finding all text) while the recognizer focuses on accuracy. CRAFT + TrOCR is the current state-of-the-art combination for document and scene text.

```python
class DetectionRecognitionOCR:
    def __init__(self):
        self.detector = CRAFTDetector()
        self.rectifier = TextRectifier()
        self.recognizer = TrOCRRecognizer()

    def process(self, image):
        # Detect text regions
        regions = self.detector.detect(image)

        results = []
        for region in regions:
            # Rectify and crop the region
            cropped = self.rectifier.rectify(image, region.bbox, region.angle)

            # Recognize text
            text_result = self.recognizer.recognize(cropped)

            results.append(TextResult(
                text=text_result.text,
                confidence=text_result.confidence,
                bbox=region.bbox,
                angle=region.angle
            ))

        return results
```

### End-to-End OCR

End-to-end models perform detection and recognition simultaneously in a single forward pass. PARSeq (Permuted Autoregressive Sequence) and MMOCR provide this capability with competitive accuracy. End-to-end models are simpler to deploy and often faster for short documents.

```python
class EndToEndOCR:
    def __init__(self, model="parseq_base"):
        self.model = load_model(model)

    def process(self, image):
        results = self.model.predict(image)
        return [
            TextResult(text=r.text, confidence=r.score, bbox=r.box)
            for r in results
        ]
```

### Document Layout Analysis Pipeline

For complex documents (invoices, forms, magazines), layout analysis determines the reading order and structure before OCR. The pipeline segments the page into regions (text blocks, tables, figures, headers) and processes each according to its type.

```
Document Image â†’ Layout Detector â†’ Region Classification â†’ Reading Order â†’ Per-Region OCR â†’ Structured Output
```

LayoutLMv3 and DiT (Document Image Transformer) provide strong layout understanding. The reading order module is critical for multi-column documents and mixed content pages.

```python
class DocumentLayoutOCR:
    def __init__(self):
        self.layout_detector = LayoutLMv3Detector()
        self.ocr_engine = TrOCRRecognizer()
        self.ordering = ReadingOrderEstimator()

    def process_document(self, page_image):
        # Detect layout regions
        regions = self.layout_detector.detect(page_image)

        # Determine reading order
        ordered_regions = self.ordering.order(regions)

        # OCR each region
        document = Document()
        for region in ordered_regions:
            if region.type == "text":
                text = self.ocr_engine.recognize(
                    crop_region(page_image, region.bbox)
                )
                document.add_text_block(text, region.bbox)
            elif region.type == "table":
                table = self.extract_table(page_image, region.bbox)
                document.add_table(table, region.bbox)

        return document
```

### Scene Text Recognition Architecture

Scene text in natural images (signs, logos, product labels) requires specialized handling due to varied fonts, colors, backgrounds, and geometric distortions. The architecture includes text detection, perspective correction, and recognition with language model post-processing.

```python
class SceneTextOCR:
    def __init__(self):
        self.detector = DBNetDetector()
        selfçŸ«æ­£å™¨ = TextRectifier(output_size=(32, 100))
        self.recognizer = CRNNRecognizer()
        self.post_processor = LanguageModelPostProcessor()

    def process(self, image):
        regions = self.detector.detect(image, min_area=100)

        results = []
        for region in regions:
            # Perspective correction for skewed/curved text
            rectified = selfçŸ«æ­£å™¨.rectify(image, region.points)

            # Recognize
            raw_text = self.recognizer.recognize(rectified)

            # Language model correction
            corrected = self.post_processor.correct(raw_text)

            results.append(corrected)
        return results
```

### Handwriting Recognition Pipeline

Handwriting recognition (HWR) handles both online (pen-stroke sequences) and offline (static images) inputs. Offline HWR typically uses CRNN with attention mechanisms. The pipeline includes binarization, line segmentation, and per-line recognition.

```python
class HandwritingPipeline:
    def __init__(self):
        self.binarizer = AdaptiveBinarizer()
        self.line_segmenter = TextLineSegmenter()
        self.recognizer = HATRecognizer()  # Handwriting Attention Transformer

    def process(self, document_image):
        # Binarize
        binary = self.binarizer.process(document_image)

        # Segment into lines
        lines = self.line_segmenter.segment(binary)

        results = []
        for line in lines:
            text = self.recognizer.recognize(line)
            results.append(text)

        return "\n".join(results)
```

## Model Selection Guide

### Detection Model Comparison

| Model | Speed (FPS) | Precision | Recall | F-measure | Best For |
|-------|-------------|-----------|--------|-----------|----------|
| CRAFT | 8 | 0.88 | 0.87 | 0.875 | Balanced accuracy |
| DBNet | 30 | 0.84 | 0.82 | 0.830 | Real-time |
| EAST | 50 | 0.80 | 0.78 | 0.790 | Speed-critical |
| Mask R-CNN | 5 | 0.90 | 0.89 | 0.895 | Maximum accuracy |
| PSENet | 15 | 0.85 | 0.84 | 0.845 | Arbitrary shapes |

CRAFT remains the most widely used detector for its balance of accuracy and versatility. DBNet is preferred for real-time applications due to its significantly higher speed. Mask R-CNN provides the best accuracy but at the cost of speed.

### Recognition Model Comparison

| Model | Architecture | CER (IC15) | Speed (ms) | Best For |
|-------|-------------|------------|------------|----------|
| TrOCR-large | ViT-LM | 2.34% | 45 | Maximum accuracy |
| TrOCR-base | ViT-LM | 3.15% | 15 | Balanced |
| PARSeq | Transformer | 2.73% | 8 | Scene text |
| CRNN | CNN+RNN | 5.82% | 5 | Speed |
| MMOCR | Various | 2.50% | 20 | Research |

TrOCR provides the best accuracy for printed documents. PARSeq excels at scene text with its permutation-based attention. CRNN remains popular for applications where speed is paramount.

### Engine Comparison

| Engine | Language | GPU | Accuracy | Speed | Ease of Use |
|--------|----------|-----|----------|-------|-------------|
| Tesseract 5 | C++ | No | Good | Fast | Easy |
| PaddleOCR | Python | Optional | Very Good | Fast | Moderate |
| EasyOCR | Python | Optional | Good | Moderate | Very Easy |
| MMOCR | Python | Yes | Excellent | Moderate | Research |
| TrOCR | Python | Yes | Excellent | Slow | Moderate |

PaddleOCR offers the best balance of accuracy and ease of deployment. Tesseract is the simplest to integrate for legacy systems. TrOCR provides the best accuracy for document processing when GPU is available.

### Accuracy vs Speed Tradeoffs

**Maximum accuracy:** TrOCR-large + CRAFT achieves CER < 2.5% but requires 60+ ms per document page.

**Balanced:** TrOCR-base + DBNet provides CER ~ 3% with 20-30 ms latency, suitable for most production document processing.

**Speed-critical:** CRNN + EAST achieves CER ~ 6% at 5-10 ms, ideal for real-time scene text extraction.

**Edge deployment:** Quantized CRNN on ONNX Runtime can achieve 15+ FPS on mobile CPUs for lightweight OCR tasks.

### Hardware Requirements

**GPU (NVIDIA T4):** TrOCR processes 20-30 pages/second. Sufficient for batch document processing.

**GPU (NVIDIA A100):** 100+ pages/second with TrOCR. Required for high-volume document processing pipelines.

**CPU Only:** Tesseract processes 5-10 pages/second. PaddleOCR with CPU achieves 3-5 pages/second with good accuracy.

**Mobile:** EasyOCR with CRNN runs at 2-5 FPS on modern smartphones for on-device OCR.

## Preprocessing Pipeline

### Binarization

Binarization converts grayscale images to black and white, separating text from background. Otsu's method works well for uniform illumination. Adaptive thresholding (Gaussian, Niblack, Sauvola) handles varying lighting across the document.

```python
import cv2

class DocumentBinarizer:
    def otsu(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def adaptive_gaussian(self, image, block_size=11, c=2):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, block_size, c
        )

    def sauvola(self, image, window_size=25, k=0.2, r=128):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
        mean = cv2.blur(gray, (window_size, window_size))
        sq_mean = cv2.blur(gray ** 2, (window_size, window_size))
        std = np.sqrt(sq_mean - mean ** 2)
        threshold = mean * (1 + k * (std / r - 1))
        return (gray > threshold).astype(np.uint8) * 255
```

### Deskewing and Rotation Correction

Skewed documents cause OCR errors by misaligning text lines. Deskewing detects the dominant text angle using Hough transform or projection profile analysis and rotates the image to correct it.

```python
class Deskewer:
    def detect_angle(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100)

        if lines is None:
            return 0

        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if abs(angle) < 30:  # Only horizontal-ish lines
                angles.append(angle)

        return np.median(angles) if angles else 0

    def deskew(self, image):
        angle = self.detect_angle(image)
        if abs(angle) > 0.5:
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            return cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_CUBIC)
        return image
```

### Noise Removal and Denoising

Noise in scanned or photographed documents degrades OCR quality. Common noise types include salt-and-pepper noise, Gaussian noise, and JPEG compression artifacts.

```python
class NoiseRemover:
    def median_filter(self, image, kernel_size=3):
        return cv2.medianBlur(image, kernel_size)

    def gaussian_filter(self, image, kernel_size=5, sigma=1.0):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

    def non_local_means(self, image, h=10):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, h=h)
        return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)

    def morphological_clean(self, image):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        return closing
```

### Contrast Enhancement (CLAHE)

Contrast Limited Adaptive Histogram Equalization (CLAHE) improves text visibility in documents with uneven illumination or low contrast. It localizes the histogram equalization to prevent over-amplification in uniform regions.

```python
class ContrastEnhancer:
    def clahe(self, image, clip_limit=2.0, grid_size=8):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]

        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
        lab[:, :, 0] = clahe.apply(l_channel)

        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def auto_contrast(self, image, cutoff=1):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        p_low = np.percentile(gray, cutoff)
        p_high = np.percentile(gray, 100 - cutoff)
        stretched = np.clip((gray - p_low) / (p_high - p_low) * 255, 0, 255)
        return stretched.astype(np.uint8)
```

### Border Removal

Scanned documents often have dark borders from the scanner lid or document edges. Border removal eliminates these artifacts before OCR to improve accuracy and reduce processing time.

```python
class BorderRemover:
    def remove_borders(self, image, threshold=200):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            return image[y:y+h, x:x+w]

        return image
```

## Post-Processing

### Spell Checking and Language Models

OCR post-processing uses spell checking and language models to correct recognition errors. Character-level n-gram models and transformer-based language models significantly reduce final character error rate.

```python
class SpellChecker:
    def __init__(self, language="en"):
        self.spellchecker = SymSpell(max_dictionary_edit_distance=2)
        self.lm = LanguageModel("en_small")

    def correct(self, ocr_text):
        words = ocr_text.split()
        corrected = []
        for word in words:
            suggestions = self.spellchecker.lookup(word, max_edit_distance=2)
            if suggestions:
                corrected.append(suggestions[0].term)
            else:
                corrected.append(word)
        return " ".join(corrected)

    def lm_correct(self, ocr_text, beam_width=5):
        return self.lm.decode(ocr_text, beam_width=beam_width)
```

### Dictionary-Based Correction

For domain-specific OCR (medical, legal, technical), dictionary-based correction replaces common OCR errors with domain-correct terms. This is especially effective for specialized vocabulary that spell checkers might flag incorrectly.

```python
class DomainDictionaryCorrector:
    def __init__(self, domain_terms):
        self.term_trie = Trie(domain_terms)
        selfçº é”™_map = {}

    def add_corrections(self, error_pattern, correct_term):
        selfçº é”™_map[error_pattern] = correct_term

    def correct(self, text):
        for error, correction in selfçº é”™_map.items():
            text = text.replace(error, correction)

        words = text.split()
        corrected = []
        for word in words:
            if self.term_trie.search(word.lower()):
                corrected.append(word)
            else:
                closest = self.term_trie.find_closest(word.lower(), max_distance=2)
                corrected.append(closest if closest else word)
        return " ".join(corrected)
```

### Confidence-Based Filtering

Low-confidence OCR results can be flagged for human review. Setting appropriate confidence thresholds reduces error rates at the cost of requiring manual verification for uncertain regions.

```python
class ConfidenceFilter:
    def __init__(self, word_threshold=0.7, line_threshold=0.8):
        self.word_threshold = word_threshold
        self.line_threshold = line_threshold

    def filter(self, ocr_results):
        filtered = []
        for result in ocr_results:
            if result.confidence < self.line_threshold:
                result.flagged_for_review = True

            for word in result.words:
                if word.confidence < self.word_threshold:
                    word.uncertain = True

            filtered.append(result)
        return filtered

    def get_review_queue(self, results):
        return [r for r in results if r.flagged_for_review]
```

### Structured Output Generation

OCR results can be structured into JSON, XML, or other formats for downstream processing. This includes converting detected tables into CSV/Excel, extracting key-value pairs from forms, and generating structured document representations.

```python
class StructuredOutputGenerator:
    def to_json(self, ocr_results):
        return json.dumps({
            "text": "\n".join([r.text for r in ocr_results]),
            "words": [{"text": w.text, "bbox": w.bbox, "confidence": w.confidence}
                      for r in ocr_results for w in r.words],
            "lines": [{"text": r.text, "bbox": r.bbox, "confidence": r.confidence}
                      for r in ocr_results],
            "metadata": {
                "engine": "trocr",
                "processing_time_ms": r.processing_time
            }
        }, indent=2)

    def to_alto(self, ocr_results):
        # ALTO XML format for archival
        pass

    def to_hOCR(self, ocr_results):
        # hOCR format for web integration
        pass
```

### Table Extraction and Parsing

Table extraction from documents involves detecting table structure (rows, columns, cells), extracting cell content via OCR, and converting to structured data formats.

```python
class TableExtractor:
    def __init__(self):
        self.table_detector = TableStructureDetector()
        self.cell_ocr = TrOCRRecognizer()

    def extract(self, document_image):
        tables = self.table_detector.detect(document_image)

        results = []
        for table in tables:
            cells = table.cells
            cell_texts = {}
            for cell in cells:
                cropped = crop_region(document_image, cell.bbox)
                text = self.cell_ocr.recognize(cropped)
                cell_texts[(cell.row, cell.col)] = text.text

            # Build structured table
            df = pd.DataFrame(
                [[cell_texts.get((r, c), "") for c in range(table.num_cols)]
                 for r in range(table.num_rows)]
            )
            results.append(df)

        return results
```

## Advanced Topics

### Multi-Language OCR

Multi-language OCR handles documents containing text in multiple scripts and languages. The system must detect the script/language of each text region and apply the appropriate recognition model.

```python
class MultiLanguageOCR:
    def __init__(self):
        self.detector = CRAFTDetector()
        self.script_classifier = ScriptClassifier()
        self.recognizers = {
            "latin": TrOCRRecognizer(model="trocr_latin"),
            "chinese": TrOCRRecognizer(model="trocr_chinese"),
            "arabic": TrOCRRecognizer(model="trocr_arabic"),
            "devanagari": TrOCRRecognizer(model="trocr_devanagari"),
        }

    def process(self, image):
        regions = self.detector.detect(image)

        results = []
        for region in regions:
            cropped = crop_region(image, region.bbox)
            script = self.script_classifier.classify(cropped)

            recognizer = self.recognizers.get(script, self.recognizers["latin"])
            text = recognizer.recognize(cropped)
            results.append(text)
        return results
```

### Mathematical Expression Recognition

Mathematical expression recognition (MER) extracts LaTeX from images of mathematical formulas. The challenge includes 2D structural relationships (superscripts, subscripts, fractions, integrals) that linear text OCR cannot handle.

Models like UniMERNet and LaTeX-OCR use encoder-decoder architectures with attention to capture spatial relationships. The output is valid LaTeX that can be rendered or evaluated.

```python
class MathExpressionRecognizer:
    def __init__(self):
        self.detector = FormulaDetector()
        self.recognizer = UniMERNet()

    def process(self, document_image):
        formulas = self.detector.detect(document_image)

        results = []
        for formula in formulas:
            cropped = crop_region(document_image, formula.bbox)
            latex = self.recognizer.recognize(cropped)
            results.append(MathResult(
                latex=latex.text,
                confidence=latex.confidence,
                bbox=formula.bbox
            ))
        return results
```

### License Plate Recognition

License plate recognition (LPR/ANPR) is a specialized OCR application that detects vehicle license plates and reads the alphanumeric characters. The pipeline includes plate detection, character segmentation, and character recognition.

```python
class LicensePlateRecognizer:
    def __init__(self):
        self.plate_detector = YOLOPlateDetector()
        self.char_segmenter = CharSegmenter()
        self.char_recognizer = CRNNCharRecognizer()

    def recognize(self, image):
        plates = self.plate_detector.detect(image)

        results = []
        for plate in plates:
            cropped = crop_region(image, plate.bbox)

            # Segment characters
            chars = self.char_segmenter.segment(cropped)

            # Recognize each character
            plate_text = ""
            for char_img in chars:
                char = self.char_recognizer.recognize(char_img)
                plate_text += char.text

            results.append(PlateResult(
                text=plate_text,
                bbox=plate.bbox,
                confidence=plate.confidence
            ))
        return results
```

### Receipt and Invoice Processing

Receipt/invoice OCR combines document layout analysis with text recognition to extract structured data (vendor, date, line items, totals). This is the core of accounts payable automation.

```python
class ReceiptProcessor:
    def __init__(self):
        self.layout_analyzer = LayoutLMv3Detector()
        self.ocr_engine = TrOCRRecognizer()
        self.entity_extractor = LayoutLMv3ForTokenClassification()

    def process(self, receipt_image):
        # OCR the entire document
        ocr_results = self.ocr_engine.process_document(receipt_image)

        # Extract key entities
        entities = self.entity_extractor.extract(ocr_results)

        return ReceiptData(
            vendor=entities.get("vendor"),
            date=entities.get("date"),
            total=entities.get("total"),
            tax=entities.get("tax"),
            items=entities.get("line_items"),
            currency=entities.get("currency")
        )
```

## Production Deployment

### Batch Processing Architecture

Batch OCR systems process large volumes of documents asynchronously using task queues and worker pools. The architecture uses message queues (RabbitMQ, Kafka) to distribute work across GPU workers.

```
Document Store â†’ Task Queue â†’ Worker Pool (GPU) â†’ Result Store â†’ Search Index
                              â†“
                         Progress Tracker
```

```python
class BatchOCRSystem:
    def __init__(self, num_workers=4):
        self.queue = TaskQueue("ocr_tasks")
        self.workers = [OCRWorker() for _ in range(num_workers)]
        self.result_store = ResultStore()

    def submit_batch(self, document_paths):
        for path in document_paths:
            self.queue.enqueue({"document": path, "priority": "normal"})

    def process_worker(self, worker):
        while True:
            task = self.queue.dequeue()
            if task is None:
                break

            result = worker.process(task["document"])
            self.result_store.save(task["document"], result)
```

### Real-Time OCR Pipelines

Real-time OCR processes documents as they arrive, suitable for live document scanning, camera-based OCR, and streaming document processing. The pipeline must maintain low latency while handling variable input rates.

```python
class RealTimeOCRPipeline:
    def __init__(self, target_latency_ms=200):
        self.detector = DBNetDetector()  # Fast detector
        self.recognizer = CRNNRecognizer()  # Fast recognizer
        self.target_latency = target_latency_ms

    async def process_stream(self, frame_generator):
        async for frame in frame_generator:
            start = time.time()

            regions = self.detector.detect(frame)
            results = []
            for region in regions:
                cropped = crop_region(frame, region.bbox)
                text = self.recognizer.recognize(cropped)
                results.append(text)

            latency_ms = (time.time() - start) * 1000
            if latency_ms > self.target_latency:
                logger.warning(f"Latency {latency_ms:.0f}ms exceeds target")

            yield results
```

### GPU Acceleration

GPU acceleration is essential for production OCR throughput. Key optimizations include CUDA graph capture for repeated inference patterns, mixed-precision (FP16) inference, and batch processing to maximize GPU utilization.

```python
class GPUOCREngine:
    def __init__(self, model_path, precision="fp16"):
        self.session = ort.InferenceSession(
            model_path,
            providers=["CUDAExecutionProvider"],
            sess_options=self._create_options(precision)
        )

    def _create_options(self, precision):
        opts = ort.SessionOptions()
        if precision == "fp16":
            opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        return opts

    def batch_process(self, images):
        preprocessed = [preprocess(img) for img in images]
        batch = np.stack(preprocessed)

        outputs = self.session.run(None, {"input": batch})
        return outputs
```

### Quality Assurance

Production OCR systems need quality assurance to catch and correct errors. QA workflows include automated confidence-based filtering, human review for low-confidence results, and periodic accuracy audits.

```python
class OCRAssurance:
    def __init__(self, confidence_threshold=0.8):
        self.threshold = confidence_threshold
        self.review_queue = ReviewQueue()

    def assess_quality(self, ocr_result):
        # Flag low-confidence words
        uncertain_words = [w for w in ocr_result.words if w.confidence < self.threshold]

        # Calculate quality metrics
        avg_confidence = np.mean([w.confidence for w in ocr_result.words])
        line_count = len(ocr_result.lines)

        quality_score = avg_confidence * (1 - len(uncertain_words) / max(len(ocr_result.words), 1))

        return QualityReport(
            quality_score=quality_score,
            avg_confidence=avg_confidence,
            uncertain_words=uncertain_words,
            needs_review=quality_score < 0.7
        )
```

## Integration Patterns

### Document Management Systems

OCR integrates with document management systems (DMS) to make scanned documents searchable. The OCR pipeline generates full-text indexes that enable keyword search across archived documents.

### Email Processing

Email attachments (invoices, contracts, receipts) can be automatically OCR'd and classified. The pipeline extracts text, classifies the document type, and routes it to the appropriate business process.

### Form Processing (AP Automation)

Accounts payable automation uses OCR to extract invoice fields (vendor, date, line items, totals) and match them against purchase orders. Template-based extraction handles structured forms while key-value extraction handles unstructured invoices.

### Search Indexing

OCR enables full-text search over image-based documents. The extracted text is indexed in Elasticsearch or similar search engines, allowing users to search document collections by content.

### Content Moderation

OCR detects text in user-uploaded images for content moderation. The pipeline identifies offensive text, policy violations, or sensitive information in images shared on social media or messaging platforms.

## Performance Metrics

### Character Error Rate (CER)

CER measures the edit distance (insertions + deletions + substitutions) between recognized text and ground truth, normalized by the total number of characters. Lower is better.

```
CER = (S + D + I) / N
```

Where S = substitutions, D = deletions, I = insertions, N = total characters.

State-of-art CER on ICDAR 2015 (scene text): ~2.3% (TrOCR-large).
State-of-art CER on printed documents: < 1% (TrOCR with language model).

### Word Error Rate (WER)

WER measures word-level accuracy, which is more relevant for document processing:

```
WER = (S + D + I) / N_words
```

WER is typically 2-3x higher than CER because word-level errors require fewer character changes.

### Throughput Metrics

| Configuration | Pages/Hour | Cost/Page |
|--------------|------------|-----------|
| Tesseract (CPU, single) | 1,800 | $0.0001 |
| PaddleOCR (GPU, T4) | 12,000 | $0.00005 |
| TrOCR (GPU, A100) | 36,000 | $0.00003 |
| Cloud API (AWS Textract) | Unlimited | $0.015 |

### Benchmark Datasets

- **ICDAR 2015/2019:** Scene text detection and recognition
- **SROIE:** Receipt OCR
- **FUNSD:** Form understanding
- **CORD:** Receipt understanding
- **DocVQA:** Document visual question answering

## Testing and Validation

### Test Dataset Selection

Choose test datasets that match your production data characteristics. For document processing, SROIE and CORD cover receipts. For scene text, ICDAR 2015 provides the standard benchmark. For forms, FUNSD is the standard.

### Cross-Dataset Evaluation

Evaluate OCR models across multiple datasets to assess generalization. A model trained on printed documents may fail on handwritten text, and vice versa.

### Edge Case Testing

Test OCR with challenging inputs: rotated text, curved text, overlapping text, low-contrast text, degraded documents, multi-language mixed documents, and unusual fonts.

### Language-Specific Testing

Each language has unique OCR challenges: Arabic (right-to-left, connected script), Chinese (thousands of characters), Japanese (mixed scripts), and Hindi (complex conjuncts). Test language-specific accuracy separately.

## Troubleshooting

### Common OCR Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Poor accuracy on scanned docs | Low DPI | Resample to 300 DPI minimum |
| Garbled text | Wrong language model | Set correct language parameter |
| Missed text regions | Low contrast | Apply CLAHE preprocessing |
| Incorrect reading order | Multi-column layout | Use layout analysis before OCR |
| Tables not extracted | Missing table detection | Enable table detection module |
| Slow processing | CPU-only inference | Enable GPU acceleration |

### Quality Degradation Patterns

Monitor for quality degradation caused by: camera focus issues in mobile OCR, scanner calibration drift, JPEG compression artifacts, and document aging (yellowing, fading). Implement quality gates that reject images below minimum quality thresholds.

### Performance Debugging

Profile OCR pipelines to identify bottlenecks: image loading, preprocessing, detection, recognition, and post-processing. Use GPU profiling tools (nvprof, Nsight) to identify CUDA kernel inefficiencies.


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills
