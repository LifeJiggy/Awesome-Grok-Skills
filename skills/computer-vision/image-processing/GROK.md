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
