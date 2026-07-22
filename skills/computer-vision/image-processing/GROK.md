---
name: "image-processing"
category: "computer-vision"
version: "2.0.0"
tags: ["computer-vision", "image-processing", "OpenCV", "filters", "transforms"]
---

# Image Processing

## Overview

The Image Processing module provides comprehensive tools for digital image manipulation, enhancement, analysis, and transformation. It covers spatial and frequency domain filtering, morphological operations, color space conversions, image segmentation, feature extraction, and image registration. The module integrates with OpenCV, scikit-image, and PIL/Pillow for production-ready implementations.

This skill is essential for computer vision engineers, image processing researchers, and developers building visual applications.

## Core Capabilities

- **Spatial Filtering**: Gaussian blur, median filter, bilateral filter, unsharp masking, and edge-preserving smoothing
- **Frequency Domain**: Fourier transforms, DFT filtering, Wiener deconvolution, and frequency-selective filtering
- **Morphological Operations**: Erosion, dilation, opening, closing, hit-or-miss, and skeleton extraction
- **Color Processing**: HSV/HLS conversions, color histogram equalization, white balance, and color transfer
- **Image Segmentation**: Thresholding (Otsu, adaptive), watershed, region growing, and superpixel segmentation
- **Feature Detection**: Harris corners, FAST, ORB, SIFT, SURF, and HOG descriptors
- **Geometric Transforms**: Rotation, affine, perspective, and image registration/stitching
- **Restoration**: Denoising (NLM, BM3D), deblurring, inpainting, and HDR tone mapping

## Usage Examples

```python
from image_processing import (
    SpatialFilter,
    FrequencyFilter,
    MorphologyProcessor,
    ColorProcessor,
    Segmenter,
    FeatureDetector,
)

# --- Spatial Filtering ---
spatial = SpatialFilter()
blurred = spatial.gaussian_blur(image, kernel_size=5, sigma=1.5)
sharpened = spatial.unsharp_mask(image, amount=1.5, radius=2)
denoised = spatial.bilateral_filter(image, d=9, sigma_color=75, sigma_space=75)
edges = spatial.canny_edge(image, low_threshold=50, high_threshold=150)

# --- Frequency Domain ---
freq = FrequencyFilter()
spectrum = freq.compute_dft(image)
filtered = freq.bandpass_filter(spectrum, low_cutoff=10, high_cutoff=100)
restored = freq.inverse_dft(filtered)

# --- Morphology ---
morph = MorphologyProcessor()
binary = morph.otsu_threshold(image)
cleaned = morph.opening(binary, kernel_size=3)
filled = morph.closing(cleaned, kernel_size=5)
skeleton = morph.skeletonize(binary)

# --- Color Processing ---
color = ColorProcessor()
hsv = color.rgb_to_hsv(image)
equalized = color.histogram_equalization(image, method="clahe")
wb = color.auto_white_balance(image)

# --- Segmentation ---
segmenter = Segmenter()
labels = segmenter.watershed_segment(image, markers=100)
superpixels = segmenter.slic_segment(image, n_segments=200)

# --- Feature Detection ---
detector = FeatureDetector()
corners = detector.detect_harris(image, threshold=0.01)
orb_features = detector.detect_orb(image, n_features=1000)
descriptors = detector.compute_descriptors(image, keypoints=orb_features)
```

## Best Practices

- Always convert to appropriate color space before processing (e.g., HSV for color-based segmentation)
- Apply Gaussian blur before edge detection to reduce noise sensitivity
- Use CLAHE (Contrast Limited Adaptive Histogram Equalization) for medical imaging
- Normalize image data to [0,1] or [-1,1] range before feeding to neural networks
- Preserve original images — never overwrite source files during processing pipelines
- Use kernel sizes that are odd numbers (3, 5, 7, ...) for symmetric filtering
- Consider bilateral filtering for edge-preserving smoothing in portrait enhancement
- For production pipelines, use OpenCV (C++ backend) over PIL for performance
- Validate image dimensions and formats at pipeline entry points
- Document all processing parameters for reproducibility

## Related Modules

- **object-detection**: Object detection and recognition
- **face-recognition**: Face detection and recognition systems
- **ocr**: Optical character recognition
- **video-analysis**: Video frame processing and analysis

## Advanced Configuration

### OpenCV Configuration

```python
import cv2

# Thread configuration
cv2.setNumThreads(4)
cv2.setUseOptimized(True)

# CUDA acceleration
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    print("CUDA available")
    cv2.cuda.setDevice(0)
```

### Image Processing Pipeline Config

```yaml
pipeline:
  input:
    format: ["jpg", "png", "tiff", "bmp"]
    max_size_mb: 50
    color_space: "bgr"
  preprocessing:
    resize: false
    max_dimension: 4096
    normalize: true
    target_range: [0, 1]
  processing:
    denoise: true
    denoise_strength: 10
    sharpen: false
    sharpen_amount: 1.5
  output:
    format: "png"
    quality: 95
    color_space: "bgr"
```

### GPU Acceleration Config

```yaml
gpu:
  enabled: true
  device_id: 0
  memory_limit_gb: 4
  batch_size: 32
  use_cuda: true
  use_opencv_cuda: true
```

## Architecture Patterns

### Image Processing Pipeline

```
Input → Preprocessing → Processing → Analysis → Output

Preprocessing:
├── Read image
├── Color space conversion
├── Resize/scale
├── Normalize pixel values
└── Apply padding

Processing:
├── Denoising
├── Sharpening
├── Filtering
├── Morphology
└── Color manipulation

Analysis:
├── Feature detection
├── Segmentation
├── Histogram analysis
├── Statistical analysis
└── Pattern recognition

Output:
├── Save processed image
├── Generate report
├── Return metrics
└── Visualize results
```

### Filter Types

```
Spatial Filters:
├── Low-pass
│   ├── Gaussian blur
│   ├── Box filter
│   └── Median filter
├── High-pass
│   ├── Laplacian
│   ├── Sobel
│   └── Canny edge
├── Band-pass
│   └── Band-reject filter
└── Custom
    └── Convolution kernel

Frequency Domain:
├── Fourier Transform
├── DCT
├── Wavelet Transform
└── Frequency filtering
```

## Integration Guide

### OpenCV Integration

```python
import cv2
import numpy as np

# Read image
image = cv2.imread('input.jpg')

# Apply Gaussian blur
blurred = cv2.GaussianBlur(image, (5, 5), 1.5)

# Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Save result
cv2.imwrite('output.jpg', edges)
```

### scikit-image Integration

```python
from skimage import io, filters, morphology
import numpy as np

# Read image
image = io.imread('input.jpg', as_gray=True)

# Apply Sobel filter
edges = filters.sobel(image)

# Morphological cleaning
cleaned = morphology.opening(edges, morphology.disk(3))
```

### PIL/Pillow Integration

```python
from PIL import Image, ImageFilter, ImageEnhance

# Open image
image = Image.open('input.jpg')

# Apply filter
filtered = image.filter(ImageFilter.SHARPEN)

# Enhance contrast
enhancer = ImageEnhance.Contrast(filtered)
enhanced = enhancer.enhance(1.5)

# Save result
enhanced.save('output.jpg', quality=95)
```

## Performance Optimization

### Processing Speed

| Technique | Description | Speedup |
|-----------|-------------|---------|
| CUDA acceleration | GPU processing | 10-50x |
| Multi-threading | Parallel processing | 2-4x |
| Vectorization | NumPy operations | 5-10x |
| Cache processing | Reuse computations | 2-5x |
| Downsampling | Reduce resolution | Nx |

### Memory Optimization

```python
# Process in chunks for large images
def process_large_image(image_path, chunk_size=1024):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    result = np.zeros_like(image)
    
    for y in range(0, h, chunk_size):
        for x in range(0, w, chunk_size):
            chunk = image[y:y+chunk_size, x:x+chunk_size]
            processed = process_chunk(chunk)
            result[y:y+chunk_size, x:x+chunk_size] = processed
    
    return result
```

### Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor
import os

def process_image_batch(image_paths, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(process_single_image, image_paths))
    return results
```

## Security Considerations

### Image Security

| Control | Description | Implementation |
|---------|-------------|----------------|
| Input Validation | Check image format | Format detection |
| Size Limits | Prevent memory exhaustion | Maximum dimensions |
| Sanitization | Remove metadata | Strip EXIF data |
| Access Control | Restrict processing | File permissions |
| Audit Logging | Track processing | Log operations |

### EXIF Data Risks

```
Sensitive EXIF Data:
├── GPS coordinates (location)
├── Camera serial number
├── Date/time of capture
├── Software version
└── Thumbnail images
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Memory Error | Out of memory | Process in chunks |
| Format Error | Cannot read image | Check file format |
| Color Mismatch | Wrong colors | Check color space |
| Slow Processing | Long execution time | Use GPU, optimize |
| Distortion | Warped output | Check transform params |

### Debugging Tips

```python
# Check image properties
image = cv2.imread('input.jpg')
print(f"Shape: {image.shape}")
print(f"Dtype: {image.dtype}")
print(f"Size: {image.nbytes / 1024:.1f} KB")

# Debug histogram
hist = cv2.calcHist([image], [0], None, [256], [0, 256])
print(f"Min: {image.min()}, Max: {image.max()}")
```

## API Reference

### SpatialFilter

```python
class SpatialFilter:
    def gaussian_blur(
        image: np.ndarray,
        kernel_size: int,
        sigma: float,
    ) -> np.ndarray:
        """Apply Gaussian blur."""
    
    def median_filter(
        image: np.ndarray,
        kernel_size: int,
    ) -> np.ndarray:
        """Apply median filter."""
    
    def bilateral_filter(
        image: np.ndarray,
        d: int,
        sigma_color: float,
        sigma_space: float,
    ) -> np.ndarray:
        """Apply bilateral filter."""
    
    def canny_edge(
        image: np.ndarray,
        low_threshold: int,
        high_threshold: int,
    ) -> np.ndarray:
        """Apply Canny edge detection."""
```

### MorphologyProcessor

```python
class MorphologyProcessor:
    def otsu_threshold(
        image: np.ndarray,
    ) -> np.ndarray:
        """Apply Otsu thresholding."""
    
    def opening(
        image: np.ndarray,
        kernel_size: int,
    ) -> np.ndarray:
        """Apply morphological opening."""
    
    def closing(
        image: np.ndarray,
        kernel_size: int,
    ) -> np.ndarray:
        """Apply morphological closing."""
    
    def skeletonize(
        image: np.ndarray,
    ) -> np.ndarray:
        """Extract skeleton."""
```

### FeatureDetector

```python
class FeatureDetector:
    def detect_harris(
        image: np.ndarray,
        threshold: float,
    ) -> list[tuple]:
        """Detect Harris corners."""
    
    def detect_orb(
        image: np.ndarray,
        n_features: int,
    ) -> list[cv2.KeyPoint]:
        """Detect ORB features."""
    
    def compute_descriptors(
        image: np.ndarray,
        keypoints: list,
    ) -> np.ndarray:
        """Compute feature descriptors."""
```

## Data Models

### ImageInfo

```
ImageInfo:
  width: int
  height: int
  channels: int
  dtype: str
  format: str
  file_size: int
  color_space: str
  bit_depth: int
```

### ProcessingResult

```
ProcessingResult:
  input_shape: tuple
  output_shape: tuple
  processing_time_ms: float
  operations_applied: list[str]
  output_path: str
  quality_metrics: dict
```

### FilterKernel

```
FilterKernel:
  name: str
  size: tuple
  kernel: np.ndarray
  normalized: bool
  separable: bool
  description: str
```

## Deployment Guide

### Image Processing Environment

```
1. Prerequisites
   ├── Python 3.10+
   ├── OpenCV installed
   ├── NumPy installed
   └── GPU drivers (optional)

2. Installation
   pip install opencv-python-headless numpy scikit-image Pillow

3. Configuration
   ├── Set thread count
   ├── Configure GPU
   └── Set memory limits

4. Deployment
   ├── Package application
   ├── Set environment variables
   ├── Configure logging
   └── Monitor performance
```

## Monitoring & Observability

### Processing Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Processing Time | <100ms/image | Average processing time |
| Memory Usage | <4GB | Peak memory usage |
| GPU Utilization | >70% | GPU usage percentage |
| Throughput | >100 images/sec | Batch processing rate |
| Error Rate | <0.1% | Processing failures |

### Monitoring Dashboard

```
Image Processing Dashboard:
├── Processing throughput
├── Average processing time
├── Memory utilization
├── GPU utilization
├── Error rate
├── Queue depth
└── Resource alerts
```

## Testing Strategy

### Image Processing Tests

```
1. Unit Tests
   ├── Filter functions
   ├── Color conversions
   ├── Transform operations
   └── Morphology operations

2. Integration Tests
   ├── Pipeline end-to-end
   ├── Batch processing
   ├── GPU vs CPU comparison
   └── Output validation

3. Visual Tests
   ├── Reference image comparison
   ├── Perceptual hash
   ├── Structural similarity
   └── Edge preservation
```

## Versioning & Migration

### Image Processing Versioning

```
Major: Algorithm change
├── Example: New filter implementation
├── Requires: Re-validation
└── Risk: Medium

Minor: New operations
├── Example: Add new filter type
├── Requires: Testing
└── Risk: Low

Patch: Bug fixes
├── Example: Fix kernel normalization
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| Bilateral Filter | Edge-preserving smoothing filter |
| CLAHE | Contrast Limited Adaptive Histogram Equalization |
| Convolution | Mathematical operation on image |
| DCT | Discrete Cosine Transform |
| FFT | Fast Fourier Transform |
| Gaussian Blur | Smoothing filter using Gaussian kernel |
| Harris Corner | Corner detection algorithm |
| Kernel | Filter matrix |
| Morphology | Shape-based image operations |
| ORB | Oriented FAST and Rotated BRIEF |
| Sobel | Edge detection operator |
| Thresholding | Binarization of grayscale image |

## Changelog

### 2.0.0 (2024-12-01)
- Added GPU acceleration
- Added frequency domain processing
- Improved batch processing
- Added morphological skeletonization

### 1.2.0 (2024-08-15)
- Added bilateral filtering
- Added CLAHE
- Improved feature detection

### 1.1.0 (2024-05-20)
- Added spatial filtering
- Added color processing
- Improved segmentation

### 1.0.0 (2024-02-01)
- Initial release with basic filtering
- Simple color conversions
- Basic thresholding

## Contributing Guidelines

### Adding New Filters

1. Implement the filter
2. Add unit tests
3. Include performance benchmarks
4. Document parameters
5. Submit PR with examples

## License

MIT License

Copyright (c) 2024 Image Processing Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
