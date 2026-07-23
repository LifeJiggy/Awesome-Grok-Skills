---
name: Vision and Multimodal Capabilities
category: multimodal
version: "1.0"
tags:
  - grok
  - xai
  - vision
  - multimodal
  - image-analysis
  - document-parsing
  - video
  - ocr
description: Grok Vision — comprehensive reference for image analysis, document parsing, video understanding, and multimodal capabilities.
---

# Grok Vision and Multimodal Capabilities

## Overview

Grok's vision capabilities enable models to process and understand visual information alongside text. This includes photographs, screenshots, diagrams, charts, handwritten text, documents, and video frames. Grok 4.5 and later models provide state-of-the-art vision understanding with particular strength in real-world imagery, technical diagrams, and complex document layouts.

This guide covers the full spectrum of visual tasks: from basic image description to advanced document parsing, chart extraction, video frame analysis, and OCR with structured output.

## Supported Input Formats

### Image Formats

| Format | Extension | Max Size | Notes |
|---|---|---|---|
| JPEG | `.jpg`, `.jpeg` | 20 MB | Recommended for photographs |
| PNG | `.png` | 20 MB | Recommended for screenshots, diagrams |
| GIF | `.gif` | 20 MB | First frame only (animated) |
| WebP | `.webp` | 20 MB | Good compression, wide support |
| BMP | `.bmp` | 20 MB | Uncompressed, large files |

### Document Formats (as images)

| Format | Method | Notes |
|---|---|---|
| PDF | Render pages to images | Use 300 DPI for text clarity |
| DOCX | Convert to PDF first, then render | Preserves layout |
| PPTX | Convert to images per slide | One image per slide |
| XLSX | Screenshot or render | Chart extraction |
| Handwritten | Direct image input | Moderate accuracy |

### Video (Frame-by-Frame)

| Approach | Description |
|---|---|
| Frame extraction | Extract key frames, analyze individually |
| Scene detection | Use scene boundaries for intelligent sampling |
| Uniform sampling | Extract frames at fixed intervals |
| Object tracking | Extract frames around detected objects |

## Token Cost for Images

Vision inputs consume tokens based on image resolution:

```
Image Resolution    Tokens per Tile    Total Tokens (typical)
────────────────────────────────────────────────────────────
Small (< 512px)    ~85 tokens         ~85-170
Medium (512-1024)  ~85 tokens         ~170-340
Large (1024-2048)  ~85 tokens         ~340-1700
Very Large (> 2048) ~85 tokens         ~1700+
```

**Optimization tip**: Resize images to the minimum resolution needed for your task. A 4K photo of a receipt doesn't need 4K resolution — 1024px is sufficient for OCR.

## API Configuration

### Basic Image Input

```python
import base64
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
)

def analyze_image(image_path: str, question: str) -> str:
    """Analyze an image with a natural language question."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # Determine media type
    ext = image_path.lower().split(".")[-1]
    media_type_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }
    media_type = media_type_map.get(ext, "image/png")

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        max_tokens=4096,
    )

    return response.choices[0].message.content
```

### Multiple Images

```python
def compare_images(image_paths: list[str], question: str) -> str:
    """Compare multiple images."""
    content = [{"type": "text", "text": question}]

    for path in image_paths:
        with open(path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image_data}"}
        })

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[{"role": "user", "content": content}],
        max_tokens=4096,
    )

    return response.choices[0].message.content
```

### Image URL Input

```python
def analyze_image_url(image_url: str, question: str) -> str:
    """Analyze an image from a URL."""
    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        max_tokens=4096,
    )

    return response.choices[0].message.content
```

## Use Cases

### 1. Document OCR and Extraction

```python
def extract_document_data(document_image: str, schema: dict) -> dict:
    """Extract structured data from a document image using a JSON schema."""
    schema_description = json.dumps(schema, indent=2)

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "system",
                "content": f"""Extract data from the document image into this JSON structure:
{schema_description}

Rules:
- Extract all visible text accurately
- For missing fields, use null
- Preserve original formatting for dates and numbers
- Output ONLY valid JSON, no explanations"""
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all data from this document:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(document_image)}"}}
                ]
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    return json.loads(response.choices[0].message.content)


# Usage: Invoice extraction
invoice_schema = {
    "invoice_number": "string",
    "date": "string (ISO format)",
    "due_date": "string (ISO format)",
    "vendor": {
        "name": "string",
        "address": "string",
        "tax_id": "string"
    },
    "customer": {
        "name": "string",
        "address": "string"
    },
    "line_items": [
        {
            "description": "string",
            "quantity": "number",
            "unit_price": "number",
            "total": "number"
        }
    ],
    "subtotal": "number",
    "tax": "number",
    "total": "number",
    "currency": "string"
}

result = extract_document_data("invoice.png", invoice_schema)
```

### 2. Chart and Graph Analysis

```python
def analyze_chart(chart_image: str, analysis_type: str = "comprehensive") -> dict:
    """Extract data and insights from charts and graphs."""
    prompt = f"""Analyze this chart/graph. Provide:

1. Chart type identification
2. Title and labels
3. Data extraction (as much numerical data as visible)
4. Trends and patterns
5. Key insights
6. Anomalies or notable features

Analysis type: {analysis_type}

Output as JSON with these keys: chart_type, title, axes, data_points, trends, insights, anomalies."""

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(chart_image)}"}}
                ]
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    return json.loads(response.choices[0].message.content)
```

### 3. UI/UX Review

```python
def review_ui(screenshot: str, guidelines: str = None) -> dict:
    """Review a UI screenshot against design guidelines."""
    prompt = """Review this UI screenshot. Evaluate:

1. Visual hierarchy and layout
2. Typography (readability, consistency)
3. Color usage and contrast
4. Spacing and alignment
5. Accessibility concerns (contrast ratios, text size)
6. Component consistency
7. Mobile responsiveness indicators
8. UX issues (confusing flows, unclear CTAs)

Rate each area: excellent, good, needs-improvement, poor.
Provide specific, actionable recommendations."""

    if guidelines:
        prompt += f"\n\nDesign guidelines to check against:\n{guidelines}"

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(screenshot)}"}}
                ]
            }
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    return response.choices[0].message.content
```

### 4. Code Screenshot to Code

```python
def image_to_code(
    code_image: str,
    target_language: str = "python",
    style_notes: str = "",
) -> str:
    """Convert a code screenshot to actual code."""
    prompt = f"""Convert this code screenshot into {target_language} code.

Requirements:
- Transcribe the code exactly as shown
- Preserve the logic and structure
- Use proper formatting and indentation
- Add type hints if the language supports them
- {style_notes}

Output ONLY the code, no explanations."""

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(code_image)}"}}
                ]
            }
        ],
        temperature=0.0,
        max_tokens=4096,
    )

    return response.choices[0].message.content
```

### 5. Handwritten Text Recognition

```python
def recognize_handwriting(
    image_path: str,
    language: str = "en",
    context: str = "",
) -> dict:
    """Recognize and transcribe handwritten text."""
    prompt = f"""Transcribe the handwritten text in this image.

Language: {language}
{f'Context: {context}' if context else ''}

Provide:
1. Full transcription
2. Confidence level per line (high/medium/low)
3. Words or characters that were uncertain
4. Any detected structure (lists, headers, paragraphs)

Output as JSON."""

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(image_path)}"}}
                ]
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    return json.loads(response.choices[0].message.content)
```

### 6. Medical/Scientific Image Analysis

```python
def analyze_scientific_image(
    image_path: str,
    domain: str,
    question: str,
) -> dict:
    """Analyze scientific or medical imagery with domain expertise."""
    prompt = f"""Analyze this image as a {domain} expert.

Question: {question}

Provide:
1. Image description and type
2. Key observations
3. Measurements or quantitative data if visible
4. Anomalies or notable features
5. Clinical/scientific significance
6. Confidence level in observations

Disclaimer: This analysis is for educational purposes and should not replace professional evaluation."""

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert in {domain}. Analyze images with precision and scientific rigor."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(image_path)}"}}
                ]
            }
        ],
        temperature=0.1,
        max_tokens=4096,
    )

    return response.choices[0].message.content
```

## Video Analysis

### Frame Extraction Pipeline

```python
import cv2
import numpy as np
from pathlib import Path

class VideoAnalyzer:
    """Extract and analyze key frames from video files."""

    def __init__(self, client):
        self.client = client

    def extract_frames(
        self,
        video_path: str,
        method: str = "uniform",
        max_frames: int = 10,
        interval_seconds: float = 1.0,
    ) -> list[tuple[float, np.ndarray]]:
        """Extract frames from video using specified method."""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps

        frames = []

        if method == "uniform":
            # Uniform sampling
            frame_interval = int(fps * interval_seconds)
            for i in range(0, total_frames, frame_interval):
                if len(frames) >= max_frames:
                    break
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret:
                    timestamp = i / fps
                    frames.append((timestamp, frame))

        elif method == "scene_change":
            # Scene change detection
            prev_frame = None
            scene_threshold = 30.0
            for i in range(0, total_frames, int(fps * 0.5)):
                if len(frames) >= max_frames:
                    break
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if not ret:
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if prev_frame is not None:
                    diff = cv2.absdiff(gray, prev_frame)
                    score = np.mean(diff)
                    if score > scene_threshold:
                        timestamp = i / fps
                        frames.append((timestamp, frame))
                else:
                    timestamp = i / fps
                    frames.append((timestamp, frame))
                prev_frame = gray

        elif method == "keyframe":
            # Keyframe extraction (simplified)
            step = max(1, total_frames // max_frames)
            for i in range(0, total_frames, step):
                if len(frames) >= max_frames:
                    break
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret:
                    timestamp = i / fps
                    frames.append((timestamp, frame))

        cap.release()
        return frames

    def analyze_video(
        self,
        video_path: str,
        question: str,
        extraction_method: str = "uniform",
        max_frames: int = 8,
    ) -> str:
        """Analyze a video by extracting and analyzing key frames."""
        frames = self.extract_frames(video_path, method=extraction_method, max_frames=max_frames)

        content = [{"type": "text", "text": f"Analyze these video frames to answer: {question}\n\nFrames are in chronological order."}]

        for timestamp, frame in frames:
            # Convert frame to base64
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = base64.b64encode(buffer).decode('utf-8')
            content.append({
                "type": "text",
                "text": f"Frame at {timestamp:.1f}s:"
            })
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
            })

        response = self.client.chat.completions.create(
            model="grok-4-5",
            messages=[{"role": "user", "content": content}],
            max_tokens=4096,
        )

        return response.choices[0].message.content

    def transcribe_video_content(self, video_path: str) -> dict:
        """Extract visual content and on-screen text from a video."""
        return self.analyze_video(
            video_path,
            """Transcribe all visible text and describe all visual content in these video frames.
            For each frame, provide:
            - Timestamp
            - On-screen text (if any)
            - Visual description
            - Key objects/elements visible
            Output as JSON array."""
        )
```

## Advanced Vision Patterns

### Chain-of-Thought Visual Analysis

```python
def chain_of_thought_analysis(image_path: str, task: str) -> str:
    """Use chain-of-thought reasoning for complex visual analysis."""
    response = client.chat.completions.create(
        model="grok-4-5-thinking",
        messages=[
            {
                "role": "system",
                "content": """Analyze images step by step:
1. First, describe what you see objectively
2. Identify key elements and their relationships
3. Apply domain knowledge to interpret findings
4. Draw conclusions with confidence levels
5. Note any uncertainties or limitations"""
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Analyze this image step by step: {task}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(image_path)}"}}
                ]
            }
        ],
        temperature=0.2,
        max_tokens=8192,
    )

    return response.choices[0].message.content
```

### Multi-Image Comparison

```python
def compare_product_images(
    image_paths: list[str],
    criteria: list[str],
) -> dict:
    """Compare multiple product images against specific criteria."""
    content = [{"type": "text", "text": f"Compare these {len(image_paths)} images based on: {', '.join(criteria)}"}]

    for i, path in enumerate(image_paths):
        content.append({"type": "text", "text": f"Image {i+1}:"})
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{read_image(path)}"}
        })

    content.append({"type": "text", "text": "Provide a structured comparison for each criterion. Rate each image and explain differences."})

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[{"role": "user", "content": content}],
        temperature=0.2,
        max_tokens=4096,
    )

    return response.choices[0].message.content
```

### Iterative Refinement

```python
def iterative_visual_analysis(
    image_path: str,
    initial_question: str,
    refinement_rounds: int = 3,
) -> str:
    """Iteratively refine visual analysis through follow-up questions."""
    history = []

    # Initial analysis
    content = [
        {"type": "text", "text": initial_question},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(image_path)}"}}
    ]

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[{"role": "user", "content": content}],
        temperature=0.3,
        max_tokens=4096,
    )
    analysis = response.choices[0].message.content
    history.append({"role": "assistant", "content": analysis})

    # Refinement rounds
    for round_num in range(refinement_rounds):
        refinement_prompt = f"""Review your previous analysis and provide deeper insights:

Previous analysis:
{analysis}

Look for:
1. Things you may have missed
2. Subtler patterns or details
3. Alternative interpretations
4. Higher-confidence conclusions

Provide a refined, more detailed analysis."""

        history.append({"role": "user", "content": refinement_prompt})

        response = client.chat.completions.create(
            model="grok-4-5",
            messages=[{"role": "user", "content": content}] + history,
            temperature=0.3,
            max_tokens=4096,
        )
        analysis = response.choices[0].message.content
        history.append({"role": "assistant", "content": analysis})

    return analysis
```

## Performance Optimization

### Image Preprocessing

```python
from PIL import Image
import io

def optimize_image_for_vision(
    image_path: str,
    max_dimension: int = 1024,
    quality: int = 85,
) -> bytes:
    """Optimize image for API consumption while preserving details."""
    img = Image.open(image_path)

    # Resize if too large
    if max(img.size) > max_dimension:
        ratio = max_dimension / max(img.size)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Compress
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    return buffer.getvalue()


def batch_optimize_images(
    image_paths: list[str],
    max_dimension: int = 1024,
) -> list[str]:
    """Optimize multiple images for batch analysis."""
    optimized = []
    for path in image_paths:
        optimized_data = optimize_image_for_vision(path, max_dimension)
        encoded = base64.b64encode(optimized_data).decode('utf-8')
        optimized.append(encoded)
    return optimized
```

### Caching Visual Analysis

```python
import hashlib
from functools import lru_cache

def cached_vision_analysis(image_path: str, question: str) -> str:
    """Cache visual analysis results based on image hash + question."""
    # Generate cache key from image content + question
    with open(image_path, "rb") as f:
        image_hash = hashlib.sha256(f.read()).hexdigest()[:16]
    question_hash = hashlib.sha256(question.encode()).hexdigest()[:8]
    cache_key = f"{image_hash}_{question_hash}"

    # Check cache
    cached = get_from_cache(cache_key)
    if cached:
        return cached

    # Perform analysis
    result = analyze_image(image_path, question)

    # Store in cache
    set_cache(cache_key, result, ttl=3600)

    return result
```

## Common Pitfalls and Solutions

### Pitfall 1: Low-Resolution Images

**Problem**: Sending tiny or blurry images produces poor results.

**Solution**: Ensure images are at least 512px on the shortest side. For text-heavy documents, use 1024px+ or 300 DPI.

```python
def ensure_minimum_resolution(image_path: str, min_px: int = 512) -> str:
    """Ensure image meets minimum resolution for accurate analysis."""
    img = Image.open(image_path)
    if min(img.size) < min_px:
        ratio = min_px / min(img.size)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        optimized_path = image_path.replace(".", "_optimized.")
        img.save(optimized_path)
        return optimized_path
    return image_path
```

### Pitfall 2: Excessive Token Usage

**Problem**: Sending very large images consumes excessive tokens.

**Solution**: Resize images based on the task:
- Simple description: 512px
- OCR/text extraction: 1024px
- Detailed analysis: 1024-2048px
- Artistic/stylistic review: Full resolution

### Pitfall 3: Vague Questions

**Problem**: "What is this?" produces generic, unhelpful responses.

**Solution**: Be specific about what you need:
```python
# Bad
"Describe this image"

# Good
"Extract all text visible in this screenshot, organized by UI element (header, sidebar, main content, footer)"
```

### Pitfall 4: Ignoring Image Orientation

**Problem**: Rotated or sideways images produce incorrect text extraction.

**Solution**: Pre-process images to correct orientation:
```python
from PIL import ImageOps

def correct_orientation(image_path: str) -> str:
    """Auto-correct image orientation using EXIF data."""
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img)
    corrected_path = image_path.replace(".", "_corrected.")
    img.save(corrected_path)
    return corrected_path
```

### Pitfall 5: Over-Reliance on Single Analysis

**Problem**: Trusting one analysis pass for critical decisions.

**Solution**: Use multi-pass verification:
```python
def verified_analysis(image_path: str, task: str) -> dict:
    """Perform analysis and verification in separate passes."""
    # Pass 1: Initial analysis
    initial = analyze_image(image_path, task)

    # Pass 2: Independent verification
    verification = analyze_image(
        image_path,
        f"Verify this previous analysis for accuracy:\n{initial}\n\nList any errors or missing information."
    )

    return {
        "analysis": initial,
        "verification": verification,
        "confidence": "high" if "accurate" in verification.lower() else "medium"
    }
```

## Integration Patterns

### Document Processing Pipeline

```python
class DocumentProcessor:
    """End-to-end document processing pipeline."""

    def __init__(self, client):
        self.client = client

    async def process(self, file_path: str, output_format: str = "markdown") -> dict:
        """Process a document through the full pipeline."""
        # Step 1: Convert to images if needed
        if file_path.endswith(".pdf"):
            images = self.pdf_to_images(file_path)
        else:
            images = [file_path]

        # Step 2: Analyze each page
        pages = []
        for i, image_path in enumerate(images):
            page_content = await self.analyze_page(image_path, page_num=i + 1)
            pages.append(page_content)

        # Step 3: Combine and format
        if output_format == "markdown":
            return self.to_markdown(pages)
        elif output_format == "json":
            return {"pages": pages}
        elif output_format == "text":
            return "\n\n".join(p["text"] for p in pages)

    async def analyze_page(self, image_path: str, page_num: int) -> dict:
        """Analyze a single document page."""
        response = self.client.chat.completions.create(
            model="grok-4-5",
            messages=[
                {
                    "role": "system",
                    "content": """Extract content from this document page.
                    Output as JSON with:
                    - text: full text content
                    - headings: list of headings
                    - tables: any tables as arrays
                    - images: description of any embedded images
                    - page_type: (letter, form, report, receipt, etc.)"""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Analyze page {page_num}:"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{read_image(image_path)}"}}
                    ]
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
        )

        return json.loads(response.choices[0].message.content)

    def pdf_to_images(self, pdf_path: str) -> list[str]:
        """Convert PDF pages to images."""
        # Using pdf2image or similar library
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=200)
        paths = []
        for i, img in enumerate(images):
            path = f"{pdf_path}_page_{i+1}.png"
            img.save(path)
            paths.append(path)
        return paths

    def to_markdown(self, pages: list[dict]) -> str:
        """Convert extracted pages to Markdown format."""
        md_parts = []
        for page in pages:
            if page.get("headings"):
                for heading in page["headings"]:
                    md_parts.append(f"## {heading}")
            md_parts.append(page["text"])
            if page.get("tables"):
                for table in page["tables"]:
                    md_parts.append(self.table_to_markdown(table))
        return "\n\n".join(md_parts)
```

### Real-Time Image Processing API

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/analyze")
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    question: str = "Describe this image in detail",
    model: str = "grok-4-5",
):
    """Analyze an uploaded image."""
    contents = await file.read()
    image_data = base64.b64encode(contents).decode("utf-8")
    media_type = file.content_type or "image/png"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_data}"}}
                ]
            }
        ],
        max_tokens=4096,
    )

    return JSONResponse({
        "analysis": response.choices[0].message.content,
        "model": response.model,
        "tokens": response.usage.total_tokens,
    })
```

## Rate Limits for Vision

| Tier | Images/Minute | Images/Day |
|---|---|---|
| Free | 5 | 50 |
| Standard | 30 | 5,000 |
| Premium | 150 | 50,000 |
| Enterprise | Custom | Custom |

## Related Documentation

- [Grok 4.5](./grok-4-5.md) — Model specification
- [Best Practices](./grok-best-practices.md) — Optimization guide
- [Build Configuration](./grok-build.md) — Deployment guide
- [Grok Code Fast 1](./grok-code-fast-1.md) — Code model
