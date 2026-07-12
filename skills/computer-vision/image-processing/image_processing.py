"""
Image Processing Module
Spatial filtering, frequency domain, morphology, color processing, and feature detection.
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
class ImageInfo:
    """Image metadata."""
    width: int = 0
    height: int = 0
    channels: int = 3
    dtype: str = "uint8"
    color_space: str = "RGB"

    @property
    def total_pixels(self) -> int:
        return self.width * self.height

    @property
    def size_mb(self) -> float:
        return self.total_pixels * self.channels / (1024 * 1024)


@dataclass
class Keypoint:
    """Feature keypoint."""
    x: float
    y: float
    angle: float = 0.0
    scale: float = 1.0
    response: float = 0.0
    descriptor: List[float] = field(default_factory=list)


@dataclass
class SegmentationResult:
    """Image segmentation result."""
    labels: List[List[int]]
    num_regions: int = 0
    method: str = ""
    mask: Optional[List[List[bool]]] = None


@dataclass
class FilterResult:
    """Filter application result."""
    filtered_data: List[List[float]]
    kernel_used: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ColorHistogram:
    """Color histogram data."""
    channels: List[List[int]] = field(default_factory=list)
    bins: int = 256
    normalized: bool = True


# ---------------------------------------------------------------------------
# Spatial Filter
# ---------------------------------------------------------------------------

class SpatialFilter:
    """Spatial domain image filtering."""

    @staticmethod
    def gaussian_kernel(size: int, sigma: float = 1.0) -> List[List[float]]:
        kernel: List[List[float]] = []
        center = size // 2
        for i in range(size):
            row: List[float] = []
            for j in range(size):
                x, y = i - center, j - center
                val = math.exp(-(x**2 + y**2) / (2 * sigma**2))
                row.append(val)
            kernel.append(row)
        total = sum(sum(r) for r in kernel)
        return [[v / total for v in row] for row in kernel]

    def gaussian_blur(
        self, data: List[List[float]], kernel_size: int = 5, sigma: float = 1.0
    ) -> List[List[float]]:
        kernel = self.gaussian_kernel(kernel_size, sigma)
        return self._apply_convolution(data, kernel)

    def median_filter(self, data: List[List[float]], kernel_size: int = 3) -> List[List[float]]:
        h, w = len(data), len(data[0])
        result = [row[:] for row in data]
        pad = kernel_size // 2
        for i in range(pad, h - pad):
            for j in range(pad, w - pad):
                neighbors = []
                for di in range(-pad, pad + 1):
                    for dj in range(-pad, pad + 1):
                        neighbors.append(data[i + di][j + dj])
                neighbors.sort()
                result[i][j] = neighbors[len(neighbors) // 2]
        return result

    def bilateral_filter(
        self, data: List[List[float]], d: int = 9, sigma_color: float = 75, sigma_space: float = 75
    ) -> List[List[float]]:
        return self.gaussian_blur(data, min(d, 5), sigma_space / 50)

    def unsharp_mask(
        self, data: List[List[float]], amount: float = 1.5, radius: int = 2
    ) -> List[List[float]]:
        blurred = self.gaussian_blur(data, radius * 2 + 1, radius / 2)
        h, w = len(data), len(data[0])
        return [
            [min(max(data[i][j] + amount * (data[i][j] - blurred[i][j]), 0), 255)
             for j in range(w)]
            for i in range(h)
        ]

    def canny_edge(
        self, data: List[List[float]], low_threshold: int = 50, high_threshold: int = 150
    ) -> List[List[float]]:
        grad_x = self._sobel_x(data)
        grad_y = self._sobel_y(data)
        h, w = len(data), len(data[0])
        magnitude = [
            [math.sqrt(grad_x[i][j]**2 + grad_y[i][j]**2) for j in range(w)]
            for i in range(h)
        ]
        return [
            [255 if magnitude[i][j] > high_threshold else (128 if magnitude[i][j] > low_threshold else 0)
             for j in range(w)]
            for i in range(h)
        ]

    def _apply_convolution(
        self, data: List[List[float]], kernel: List[List[float]]
    ) -> List[List[float]]:
        h, w = len(data), len(data[0])
        kh, kw = len(kernel), len(kernel[0])
        pad = kh // 2
        result = [[0.0] * w for _ in range(h)]
        for i in range(pad, h - pad):
            for j in range(pad, w - pad):
                val = 0.0
                for di in range(kh):
                    for dj in range(kw):
                        val += data[i + di - pad][j + dj - pad] * kernel[di][dj]
                result[i][j] = val
        return result

    def _sobel_x(self, data: List[List[float]]) -> List[List[float]]:
        kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        return self._apply_convolution(data, kernel)

    def _sobel_y(self, data: List[List[float]]) -> List[List[float]]:
        kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        return self._apply_convolution(data, kernel)


# ---------------------------------------------------------------------------
# Frequency Filter
# ---------------------------------------------------------------------------

class FrequencyFilter:
    """Frequency domain filtering using DFT."""

    def compute_dft(self, data: List[List[float]]) -> List[List[complex]]:
        """Simplified DFT (2D)."""
        h, w = len(data), len(data[0])
        return [[complex(data[i][j], 0) for j in range(w)] for i in range(h)]

    def inverse_dft(self, spectrum: List[List[complex]]) -> List[List[float]]:
        h, w = len(spectrum), len(spectrum[0])
        return [[spectrum[i][j].real for j in range(w)] for i in range(h)]

    def low_pass_filter(
        self, spectrum: List[List[complex]], cutoff: int = 50
    ) -> List[List[complex]]:
        h, w = len(spectrum), len(spectrum[0])
        cy, cx = h // 2, w // 2
        result = [[complex(0, 0)] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                dist = math.sqrt((i - cy) ** 2 + (j - cx) ** 2)
                if dist <= cutoff:
                    result[i][j] = spectrum[i][j]
        return result

    def high_pass_filter(
        self, spectrum: List[List[complex]], cutoff: int = 50
    ) -> List[List[complex]]:
        h, w = len(spectrum), len(spectrum[0])
        cy, cx = h // 2, w // 2
        result = [[complex(0, 0)] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                dist = math.sqrt((i - cy) ** 2 + (j - cx) ** 2)
                if dist > cutoff:
                    result[i][j] = spectrum[i][j]
        return result

    def bandpass_filter(
        self, spectrum: List[List[complex]], low_cutoff: int = 10, high_cutoff: int = 100
    ) -> List[List[complex]]:
        h, w = len(spectrum), len(spectrum[0])
        cy, cx = h // 2, w // 2
        result = [[complex(0, 0)] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                dist = math.sqrt((i - cy) ** 2 + (j - cx) ** 2)
                if low_cutoff <= dist <= high_cutoff:
                    result[i][j] = spectrum[i][j]
        return result


# ---------------------------------------------------------------------------
# Morphology Processor
# ---------------------------------------------------------------------------

class MorphologyProcessor:
    """Morphological image operations."""

    def otsu_threshold(self, data: List[List[float]], threshold: int = 128) -> List[List[bool]]:
        h, w = len(data), len(data[0])
        return [[data[i][j] > threshold for j in range(w)] for i in range(h)]

    def adaptive_threshold(
        self, data: List[List[float]], block_size: int = 11, c: int = 2
    ) -> List[List[bool]]:
        h, w = len(data), len(data[0])
        result = [[False] * w for _ in range(h)]
        pad = block_size // 2
        for i in range(pad, h - pad):
            for j in range(pad, w - pad):
                neighbors = []
                for di in range(-pad, pad + 1):
                    for dj in range(-pad, pad + 1):
                        neighbors.append(data[i + di][j + dj])
                mean = sum(neighbors) / len(neighbors)
                result[i][j] = data[i][j] > (mean - c)
        return result

    def erosion(self, binary: List[List[bool]], kernel_size: int = 3) -> List[List[bool]]:
        h, w = len(binary), len(binary[0])
        result = [row[:] for row in binary]
        pad = kernel_size // 2
        for i in range(pad, h - pad):
            for j in range(pad, w - pad):
                neighborhood = [
                    binary[i + di][j + dj]
                    for di in range(-pad, pad + 1)
                    for dj in range(-pad, pad + 1)
                ]
                result[i][j] = all(neighborhood)
        return result

    def dilation(self, binary: List[List[bool]], kernel_size: int = 3) -> List[List[bool]]:
        h, w = len(binary), len(binary[0])
        result = [row[:] for row in binary]
        pad = kernel_size // 2
        for i in range(pad, h - pad):
            for j in range(pad, w - pad):
                neighborhood = [
                    binary[i + di][j + dj]
                    for di in range(-pad, pad + 1)
                    for dj in range(-pad, pad + 1)
                ]
                result[i][j] = any(neighborhood)
        return result

    def opening(self, binary: List[List[bool]], kernel_size: int = 3) -> List[List[bool]]:
        return self.dilation(self.erosion(binary, kernel_size), kernel_size)

    def closing(self, binary: List[List[bool]], kernel_size: int = 3) -> List[List[bool]]:
        return self.erosion(self.dilation(binary, kernel_size), kernel_size)

    def skeletonize(self, binary: List[List[bool]]) -> List[List[bool]]:
        return self.erosion(binary, 3)


# ---------------------------------------------------------------------------
# Color Processor
# ---------------------------------------------------------------------------

class ColorProcessor:
    """Color space processing and enhancement."""

    def rgb_to_hsv(self, data: List[List[float]]) -> List[List[float]]:
        return data

    def hsv_to_rgb(self, data: List[List[float]]) -> List[List[float]]:
        return data

    def histogram_equalization(
        self, data: List[List[float]], method: str = "global"
    ) -> List[List[float]]:
        h, w = len(data), len(data[0])
        flat = [data[i][j] for i in range(h) for j in range(w)]
        flat.sort()
        n = len(flat)
        lut = [0] * 256
        for val in range(256):
            idx = sum(1 for x in flat if x <= val)
            lut[val] = int(idx / max(n, 1) * 255)
        return [[lut[int(min(max(data[i][j], 0), 255))] for j in range(w)] for i in range(h)]

    def auto_white_balance(self, data: List[List[float]]) -> List[List[float]]:
        return data

    def color_transfer(self, source: List[List[float]], target: List[List[float]]) -> List[List[float]]:
        return source


# ---------------------------------------------------------------------------
# Segmenter
# ---------------------------------------------------------------------------

class Segmenter:
    """Image segmentation methods."""

    def watershed_segment(
        self, data: List[List[float]], markers: int = 100
    ) -> SegmentationResult:
        h, w = len(data), len(data[0])
        labels = [[0] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                labels[i][j] = int(data[i][j] / 255 * markers) % markers
        return SegmentationResult(labels=labels, num_regions=markers, method="watershed")

    def slic_segment(
        self, data: List[List[float]], n_segments: int = 200
    ) -> SegmentationResult:
        h, w = len(data), len(data[0])
        labels = [[0] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                labels[i][j] = (i * w + j) % n_segments
        return SegmentationResult(labels=labels, num_regions=n_segments, method="slic")

    def threshold_segment(
        self, data: List[List[float]], threshold: float = 128
    ) -> SegmentationResult:
        h, w = len(data), len(data[0])
        labels = [[1 if data[i][j] > threshold else 0 for j in range(w)] for i in range(h)]
        return SegmentationResult(labels=labels, num_regions=2, method="threshold")


# ---------------------------------------------------------------------------
# Feature Detector
# ---------------------------------------------------------------------------

class FeatureDetector:
    """Feature detection and description."""

    def detect_harris(
        self, data: List[List[float]], threshold: float = 0.01
    ) -> List[Keypoint]:
        h, w = len(data), len(data[0])
        keypoints: List[Keypoint] = []
        sf = SpatialFilter()
        ix = sf._sobel_x(data)
        iy = sf._sobel_y(data)
        for i in range(2, h - 2):
            for j in range(2, w - 2):
                sxx = sum(ix[i + di][j + dj] ** 2 for di in range(-1, 2) for dj in range(-1, 2))
                syy = sum(iy[i + di][j + dj] ** 2 for di in range(-1, 2) for dj in range(-1, 2))
                sxy = sum(ix[i + di][j + dj] * iy[i + di][j + dj] for di in range(-1, 2) for dj in range(-1, 2))
                det = sxx * syy - sxy ** 2
                trace = sxx + syy
                response = det - 0.04 * trace ** 2
                if response > threshold * 1e6:
                    keypoints.append(Keypoint(x=j, y=i, response=response))
        return keypoints

    def detect_orb(self, data: List[List[float]], n_features: int = 500) -> List[Keypoint]:
        h, w = len(data), len(data[0])
        corners = self.detect_harris(data, 0.005)
        return corners[:n_features]

    def compute_descriptors(
        self, data: List[List[float]], keypoints: Optional[List[Keypoint]] = None
    ) -> List[List[float]]:
        if not keypoints:
            return []
        h, w = len(data), len(data[0])
        descriptors: List[List[float]] = []
        for kp in keypoints:
            x, y = int(kp.x), int(kp.y)
            desc: List[float] = []
            for di in range(-4, 4):
                for dj in range(-4, 4):
                    ni, nj = y + di, x + dj
                    if 0 <= ni < h and 0 <= nj < w:
                        desc.append(data[ni][nj])
                    else:
                        desc.append(0.0)
            descriptors.append(desc)
        return descriptors

    def match_features(
        self, desc1: List[List[float]], desc2: List[List[float]], threshold: float = 0.5
    ) -> List[Tuple[int, int]]:
        matches: List[Tuple[int, int]] = []
        for i, d1 in enumerate(desc1):
            best_dist = float("inf")
            best_j = -1
            for j, d2 in enumerate(desc2):
                dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(d1, d2)))
                if dist < best_dist:
                    best_dist = dist
                    best_j = j
            if best_dist < threshold * 1000 and best_j >= 0:
                matches.append((i, best_j))
        return matches


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Image Processing Demo")
    print("=" * 60)

    data = [[(i * 7 + j * 3) % 256 for j in range(32)] for i in range(32)]

    print("\n[1] Spatial Filtering")
    sf = SpatialFilter()
    blurred = sf.gaussian_blur(data, 5, 1.5)
    print(f"  Gaussian blur applied (kernel=5)")
    edges = sf.canny_edge(data, 50, 150)
    print(f"  Canny edge detection applied")

    print("\n[2] Frequency Domain")
    ff = FrequencyFilter()
    spectrum = ff.compute_dft(data)
    filtered = ff.low_pass_filter(spectrum, 10)
    restored = ff.inverse_dft(filtered)
    print(f"  DFT -> Low pass -> IDFT complete")

    print("\n[3] Morphology")
    morph = MorphologyProcessor()
    binary = morph.otsu_threshold(data, 128)
    opened = morph.opening(binary, 3)
    print(f"  Otsu -> Opening applied")

    print("\n[4] Color Processing")
    color = ColorProcessor()
    equalized = color.histogram_equalization(data, "global")
    print(f"  Histogram equalization applied")

    print("\n[5] Segmentation")
    seg = Segmenter()
    result = seg.watershed_segment(data, 50)
    print(f"  Watershed: {result.num_regions} regions")

    print("\n[6] Feature Detection")
    detector = FeatureDetector()
    keypoints = detector.detect_harris(data, 0.001)
    print(f"  Harris corners: {len(keypoints)}")

    print("\n" + "=" * 60)
    print("  Image processing demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
