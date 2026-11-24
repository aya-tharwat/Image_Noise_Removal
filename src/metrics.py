"""
Image quality metrics (MSE & PSNR) and experiment summary helpers (Phase 5).

Uses pure NumPy so no extra heavy dependencies are required:
- MSE (Mean Squared Error): average squared pixel error vs. clean original (lower is better).
- PSNR (Peak Signal-to-Noise Ratio): logarithmic quality score in dB (higher is better).
"""

from typing import Any
import numpy as np


def calculate_mse(original: np.ndarray, processed: np.ndarray) -> float:
    """
    Compute Mean Squared Error (MSE) between two images of identical shape.

    Formula: MSE = mean((original - processed)^2)
    """
    if original.shape != processed.shape:
        raise ValueError(
            f"Image shapes must match for MSE: {original.shape} vs {processed.shape}"
        )

    diff = original.astype(np.float64) - processed.astype(np.float64)
    return float(np.mean(diff ** 2))


def calculate_psnr(
    original: np.ndarray,
    processed: np.ndarray,
    max_pixel: float = 255.0,
) -> float:
    """
    Compute Peak Signal-to-Noise Ratio (PSNR) in decibels (dB).

    Formula: PSNR = 20 * log10(MAX / sqrt(MSE))
    Returns float('inf') when the two images are identical (MSE == 0).
    """
    mse = calculate_mse(original, processed)
    if mse == 0.0:
        return float("inf")
    return float(20.0 * np.log10(max_pixel / np.sqrt(mse)))


def format_psnr(psnr_value: float) -> str:
    """Format a PSNR value cleanly for UI display."""
    if np.isinf(psnr_value):
        return "∞ dB"
    return f"{psnr_value:.2f} dB"


def evaluate_single_experiment(
    original: np.ndarray,
    noisy: np.ndarray,
    filtered: np.ndarray,
    noise_type: str,
    noise_intensity: str,
    noise_params: str,
    filter_name: str,
    filter_params: str,
) -> dict[str, Any]:
    """
    Compute MSE/PSNR before and after filtering and generate a student-friendly summary.
    """
    noisy_mse = calculate_mse(original, noisy)
    filtered_mse = calculate_mse(original, filtered)

    noisy_psnr = calculate_psnr(original, noisy)
    filtered_psnr = calculate_psnr(original, filtered)

    if np.isinf(filtered_psnr) and not np.isinf(noisy_psnr):
        psnr_gain = float("inf")
    elif np.isinf(noisy_psnr) and np.isinf(filtered_psnr):
        psnr_gain = 0.0
    else:
        psnr_gain = filtered_psnr - noisy_psnr

    mse_reduction_pct = (
        ((noisy_mse - filtered_mse) / noisy_mse) * 100.0
        if noisy_mse > 0.0
        else 0.0
    )

    if np.isinf(psnr_gain):
        verdict = (
            f"{filter_name} achieved near-perfect restoration on "
            f"{noise_type} ({noise_intensity}), reducing MSE to 0.00."
        )
    elif psnr_gain > 0.5:
        verdict = (
            f"{filter_name} improved image quality by +{psnr_gain:.2f} dB PSNR "
            f"(reducing MSE by {mse_reduction_pct:.1f}%) against "
            f"{noise_type} ({noise_intensity})."
        )
    elif psnr_gain >= -0.5:
        verdict = (
            f"{filter_name} produced minimal net PSNR change ({psnr_gain:+.2f} dB). "
            "Try adjusting the kernel size or testing another filter in Filter Comparison."
        )
    else:
        verdict = (
            f"{filter_name} lowered PSNR by {psnr_gain:.2f} dB—likely over-blurring "
            "fine image details. Try a smaller kernel size or a different spatial filter."
        )

    return {
        "noise_type": noise_type,
        "noise_intensity": noise_intensity,
        "noise_params": noise_params,
        "filter_name": filter_name,
        "filter_params": filter_params,
        "noisy_mse": noisy_mse,
        "filtered_mse": filtered_mse,
        "mse_delta": filtered_mse - noisy_mse,
        "mse_reduction_pct": mse_reduction_pct,
        "noisy_psnr": noisy_psnr,
        "filtered_psnr": filtered_psnr,
        "psnr_gain": psnr_gain,
        "verdict": verdict,
    }
