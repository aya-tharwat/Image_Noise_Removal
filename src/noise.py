"""
Classical image noise generation algorithms using NumPy (Phase 3).

Supports three classical noise models at Low, Medium, and High intensities:
1. Gaussian Noise       — additive normal random fluctuations
2. Salt-and-Pepper Noise — impulse noise setting pixels to pure white (255) or black (0)
3. Speckle Noise        — multiplicative noise scaled by pixel intensity
"""

from typing import Optional
import numpy as np


NOISE_TYPES = [
    "Gaussian Noise",
    "Salt-and-Pepper Noise",
    "Speckle Noise",
]

INTENSITY_LEVELS = ["Low", "Medium", "High"]

# Well-calibrated numeric presets for each noise type and intensity level
NOISE_PRESETS: dict[str, dict[str, float]] = {
    "Gaussian Noise": {
        "Low": 15.0,     # standard deviation sigma (pixel scale 0..255)
        "Medium": 35.0,
        "High": 60.0,
    },
    "Salt-and-Pepper Noise": {
        "Low": 0.02,     # 2% of pixels corrupted (1% salt + 1% pepper)
        "Medium": 0.06,  # 6% of pixels corrupted
        "High": 0.15,    # 15% of pixels corrupted
    },
    "Speckle Noise": {
        "Low": 0.15,     # standard deviation of multiplicative Gaussian factor
        "Medium": 0.35,
        "High": 0.60,
    },
}

NOISE_DESCRIPTIONS: dict[str, str] = {
    "Gaussian Noise": (
        "Adds zero-mean random values from a normal (bell-curve) distribution "
        "to every pixel, simulating electronic camera sensor noise."
    ),
    "Salt-and-Pepper Noise": (
        "Randomly replaces pixels with pure white (255, 'salt') or pure black "
        "(0, 'pepper'), simulating transmission bit errors or dead sensor pixels."
    ),
    "Speckle Noise": (
        "Multiplies pixel intensities by random Gaussian variations, creating "
        "granular noise that is stronger in brighter areas (common in radar/ultrasound)."
    ),
}


def get_noise_parameter_label(noise_type: str, intensity: str) -> str:
    """Return a readable parameter summary for the selected noise and intensity."""
    value = NOISE_PRESETS[noise_type][intensity]
    if noise_type == "Gaussian Noise":
        return f"σ = {int(value)}"
    if noise_type == "Salt-and-Pepper Noise":
        return f"{int(round(value * 100))}% corrupted pixels"
    if noise_type == "Speckle Noise":
        return f"σ = {value:.2f} (multiplicative)"
    return str(value)


def add_gaussian_noise(
    image: np.ndarray,
    intensity: str = "Medium",
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Add zero-mean Gaussian noise to an RGB uint8 image.

    Formula: noisy = clip(image + N(0, sigma), 0, 255)
    """
    sigma = NOISE_PRESETS["Gaussian Noise"][intensity]
    rng = np.random.default_rng(seed)

    img_float = image.astype(np.float32)
    noise = rng.normal(loc=0.0, scale=sigma, size=image.shape)
    noisy = np.clip(img_float + noise, 0, 255)
    return noisy.astype(np.uint8)


def add_salt_and_pepper_noise(
    image: np.ndarray,
    intensity: str = "Medium",
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Add Salt-and-Pepper (impulse) noise to an RGB uint8 image.

    Half of the corrupted pixels become pure white (255) and half become pure black (0).
    """
    amount = NOISE_PRESETS["Salt-and-Pepper Noise"][intensity]
    rng = np.random.default_rng(seed)

    noisy = image.copy()
    height, width = image.shape[:2]

    # One random number per (row, col) pixel so all RGB channels turn white or black together
    random_map = rng.random((height, width))
    salt_mask = random_map < (amount / 2.0)
    pepper_mask = (random_map >= (amount / 2.0)) & (random_map < amount)

    noisy[salt_mask] = 255
    noisy[pepper_mask] = 0
    return noisy


def add_speckle_noise(
    image: np.ndarray,
    intensity: str = "Medium",
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Add multiplicative Speckle noise to an RGB uint8 image.

    Formula: noisy = clip(image + image * N(0, sigma), 0, 255)
    """
    sigma = NOISE_PRESETS["Speckle Noise"][intensity]
    rng = np.random.default_rng(seed)

    img_float = image.astype(np.float32)
    gauss = rng.normal(loc=0.0, scale=sigma, size=image.shape)
    noisy = np.clip(img_float + img_float * gauss, 0, 255)
    return noisy.astype(np.uint8)


def apply_noise(
    image: np.ndarray,
    noise_type: str,
    intensity: str = "Medium",
    seed: Optional[int] = None,
) -> np.ndarray:
    """Dispatch helper that applies the requested noise model and intensity."""
    if intensity not in INTENSITY_LEVELS:
        raise ValueError(f"Unsupported intensity level: {intensity}")

    if noise_type == "Gaussian Noise":
        return add_gaussian_noise(image, intensity=intensity, seed=seed)
    if noise_type == "Salt-and-Pepper Noise":
        return add_salt_and_pepper_noise(image, intensity=intensity, seed=seed)
    if noise_type == "Speckle Noise":
        return add_speckle_noise(image, intensity=intensity, seed=seed)

    raise ValueError(f"Unsupported noise type: {noise_type}")
