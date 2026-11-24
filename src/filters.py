"""
Classical spatial image filtering algorithms using OpenCV (Phase 4).

Implements four built-in OpenCV spatial filters:
1. Average Filter   (cv2.blur)            — simple uniform neighborhood mean
2. Gaussian Filter  (cv2.GaussianBlur)    — distance-weighted bell-curve smoothing
3. Median Filter    (cv2.medianBlur)      — non-linear median replacement (best for S&P)
4. Bilateral Filter (cv2.bilateralFilter) — edge-preserving spatial + intensity smoothing

Note: All four OpenCV spatial filters treat RGB channels symmetrically (Euclidean
channel distance is order-independent), so RGB uint8 arrays can be filtered directly
without RGB/BGR color channel swapping.
"""

import cv2
import numpy as np


FILTER_TYPES = [
    "Average Filter",
    "Gaussian Filter",
    "Median Filter",
    "Bilateral Filter",
]

KERNEL_SIZES = [3, 5, 7, 9]
BILATERAL_DIAMETERS = [5, 7, 9, 11]

FILTER_DESCRIPTIONS: dict[str, str] = {
    "Average Filter": (
        "Replaces each pixel with the simple average of its neighborhood. "
        "Fast and smooth, but blurs sharp edges."
    ),
    "Gaussian Filter": (
        "Uses a bell-curve weighted average that gives more importance to closer "
        "neighbors. Reduces Gaussian noise more naturally than the Average Filter."
    ),
    "Median Filter": (
        "Replaces each pixel with the middle (median) value in its neighborhood. "
        "Non-linear filter that excels at removing extreme Salt-and-Pepper dots."
    ),
    "Bilateral Filter": (
        "Smooths flat noisy regions while weighting neighbors by both spatial "
        "distance and color similarity—preserving sharp edges."
    ),
}


def _validate_odd_kernel(kernel_size: int) -> int:
    """Ensure kernel_size is an odd integer >= 3 as required by OpenCV."""
    k = int(kernel_size)
    if k < 3 or k % 2 == 0:
        raise ValueError(f"Kernel size must be an odd integer >= 3, got {kernel_size}.")
    return k


def apply_average_filter(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Apply a box / mean filter using cv2.blur."""
    k = _validate_odd_kernel(kernel_size)
    return cv2.blur(image, (k, k))


def apply_gaussian_filter(
    image: np.ndarray,
    kernel_size: int = 5,
    sigma: float = 0.0,
) -> np.ndarray:
    """Apply a Gaussian smoothing filter using cv2.GaussianBlur (sigma=0 lets OpenCV auto-compute)."""
    k = _validate_odd_kernel(kernel_size)
    return cv2.GaussianBlur(image, (k, k), sigmaX=float(sigma))


def apply_median_filter(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Apply a non-linear median filter using cv2.medianBlur."""
    k = _validate_odd_kernel(kernel_size)
    return cv2.medianBlur(image, k)


def apply_bilateral_filter(
    image: np.ndarray,
    diameter: int = 9,
    sigma_color: float = 75.0,
    sigma_space: float = 75.0,
) -> np.ndarray:
    """Apply an edge-preserving bilateral filter using cv2.bilateralFilter."""
    d = max(1, int(diameter))
    return cv2.bilateralFilter(
        image,
        d=d,
        sigmaColor=float(sigma_color),
        sigmaSpace=float(sigma_space),
    )


def format_filter_params(
    filter_name: str,
    kernel_size: int = 5,
    sigma: float = 0.0,
    diameter: int = 9,
    sigma_color: float = 75.0,
    sigma_space: float = 75.0,
) -> str:
    """Return a clean human-readable summary of the active filter parameters."""
    if filter_name == "Average Filter":
        return f"kernel = {kernel_size}×{kernel_size}"
    if filter_name == "Gaussian Filter":
        sigma_text = "auto" if sigma == 0 else f"{sigma:.1f}"
        return f"kernel = {kernel_size}×{kernel_size}, σ = {sigma_text}"
    if filter_name == "Median Filter":
        return f"kernel = {kernel_size}×{kernel_size}"
    if filter_name == "Bilateral Filter":
        return f"d = {diameter}, σ_color = {int(sigma_color)}, σ_space = {int(sigma_space)}"
    return ""


def apply_filter(
    image: np.ndarray,
    filter_name: str,
    kernel_size: int = 5,
    sigma: float = 0.0,
    diameter: int = 9,
    sigma_color: float = 75.0,
    sigma_space: float = 75.0,
) -> np.ndarray:
    """Dispatch helper that applies the requested spatial filter."""
    if filter_name == "Average Filter":
        return apply_average_filter(image, kernel_size=kernel_size)
    if filter_name == "Gaussian Filter":
        return apply_gaussian_filter(image, kernel_size=kernel_size, sigma=sigma)
    if filter_name == "Median Filter":
        return apply_median_filter(image, kernel_size=kernel_size)
    if filter_name == "Bilateral Filter":
        return apply_bilateral_filter(
            image,
            diameter=diameter,
            sigma_color=sigma_color,
            sigma_space=sigma_space,
        )
    raise ValueError(f"Unsupported filter type: {filter_name}")
