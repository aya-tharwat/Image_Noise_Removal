"""
Dark-themed Matplotlib visualization helpers for filter comparison (Phase 6).

Provides a clean PSNR bar chart comparing all four classical spatial filters
against the noisy image baseline.
"""

from typing import Any
import matplotlib.pyplot as plt
import numpy as np


def plot_psnr_comparison(
    filter_results: list[dict[str, Any]],
    noisy_psnr: float,
    best_filter_name: str,
) -> plt.Figure:
    """
    Create a dark-themed bar chart comparing PSNR (dB) across all spatial filters.

    Handles infinite PSNR values gracefully by capping the bar visually and
    labeling it '∞ dB' so Matplotlib never fails on non-finite heights.
    """
    names = [item["filter_name"].replace(" Filter", "") for item in filter_results]
    raw_psnrs = [item["psnr"] for item in filter_results]

    finite_vals = [v for v in raw_psnrs if np.isfinite(v)]
    if np.isfinite(noisy_psnr):
        finite_vals.append(noisy_psnr)
    cap_height = (max(finite_vals) + 6.0) if finite_vals else 50.0

    plot_heights = [v if np.isfinite(v) else cap_height for v in raw_psnrs]
    colors = [
        "#10B981" if item["filter_name"] == best_filter_name else "#3B82F6"
        for item in filter_results
    ]

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=120)
    bg_color = "#131926"
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    bars = ax.bar(names, plot_heights, color=colors, width=0.52, zorder=3)

    # Dashed baseline for the unfiltered noisy image
    if np.isfinite(noisy_psnr):
        ax.axhline(
            y=noisy_psnr,
            color="#F59E0B",
            linestyle="--",
            linewidth=1.5,
            zorder=4,
            label=f"Noisy Baseline ({noisy_psnr:.2f} dB)",
        )

    # Value labels above each bar
    for bar, raw_val in zip(bars, raw_psnrs):
        label_text = "∞ dB" if np.isinf(raw_val) else f"{raw_val:.2f} dB"
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + (cap_height * 0.025),
            label_text,
            ha="center",
            va="bottom",
            color="#F3F4F6",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_title(
        "Filter Quality Comparison — PSNR (Higher is Better)",
        color="#F9FAFB",
        fontsize=11,
        fontweight="bold",
        pad=12,
    )
    ax.set_ylabel("PSNR (dB)", color="#CBD5E1", fontsize=9.5)
    ax.set_ylim(0, cap_height * 1.16)

    # Clean dark-theme grid & spines
    ax.grid(axis="y", color="#334155", linestyle=":", linewidth=0.8, alpha=0.6, zorder=0)
    ax.tick_params(colors="#CBD5E1", labelsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#334155")

    if np.isfinite(noisy_psnr):
        legend = ax.legend(
            loc="lower right",
            facecolor="#0B0F19",
            edgecolor="#334155",
            fontsize=8.5,
        )
        for text in legend.get_texts():
            text.set_color("#FDE68A")

    fig.tight_layout()
    return fig
