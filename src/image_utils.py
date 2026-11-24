"""
Image input, validation, and display utilities (Phase 2).

Uses Pillow (PIL) to safely open and validate uploaded or sample images,
and converts every image into a standard 3-channel RGB NumPy uint8 array
so all downstream noise and filtering functions receive consistent input.
"""

from io import BytesIO
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, UnidentifiedImageError


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
SAMPLE_IMAGES_DIR = Path(__file__).resolve().parent.parent / "sample_images"


def get_image_info(
    image: np.ndarray,
    filename: str,
    image_format: str = "Unknown",
    original_mode: str = "RGB",
) -> dict[str, Any]:
    """Return basic metadata about an RGB NumPy image for UI display."""
    height, width = image.shape[:2]
    channels = image.shape[2] if image.ndim == 3 else 1
    return {
        "filename": filename,
        "width": width,
        "height": height,
        "channels": channels,
        "format": image_format or "Unknown",
        "original_mode": original_mode,
        "dtype": str(image.dtype),
    }


def _decode_image_bytes(
    raw_bytes: bytes,
    filename: str,
) -> tuple[np.ndarray, dict[str, Any]]:
    """
    Validate raw image bytes with Pillow and convert to an RGB uint8 NumPy array.

    Raises:
        ValueError: If the file extension is unsupported, empty, or corrupted.
    """
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{suffix or 'unknown'}'. "
            "Please upload a JPG, JPEG, or PNG image."
        )

    if not raw_bytes:
        raise ValueError("The uploaded file is empty. Please choose a valid image.")

    # Step 1: Verify file integrity (catches renamed text files or truncated data)
    try:
        with Image.open(BytesIO(raw_bytes)) as check_img:
            image_format = check_img.format or suffix.lstrip(".").upper()
            check_img.verify()
    except (UnidentifiedImageError, OSError, SyntaxError) as exc:
        raise ValueError(
            f"'{filename}' is not a valid or readable image file."
        ) from exc

    # Step 2: Re-open and decode into a clean 3-channel RGB NumPy uint8 array
    try:
        with Image.open(BytesIO(raw_bytes)) as img:
            original_mode = img.mode
            rgb_img = img.convert("RGB")
            image_array = np.array(rgb_img, dtype=np.uint8)
    except Exception as exc:
        raise ValueError(
            f"Could not decode '{filename}'. Please try another JPG or PNG file."
        ) from exc

    if image_array.size == 0 or image_array.ndim != 3:
        raise ValueError("Decoded image has invalid dimensions.")

    metadata = get_image_info(
        image=image_array,
        filename=filename,
        image_format=image_format,
        original_mode=original_mode,
    )
    return image_array, metadata


def load_and_validate_image(
    uploaded_file: Any,
) -> tuple[np.ndarray, dict[str, Any]]:
    """
    Load and validate a Streamlit UploadedFile object.

    Returns:
        (image_rgb, metadata_dict)
    """
    if uploaded_file is None:
        raise ValueError("No file was provided.")

    filename = getattr(uploaded_file, "name", "uploaded_image")
    raw_bytes = uploaded_file.getvalue()
    return _decode_image_bytes(raw_bytes, filename)


def list_sample_images(folder: Path = SAMPLE_IMAGES_DIR) -> list[Path]:
    """Return a sorted list of valid JPG/JPEG/PNG files inside sample_images/."""
    if not folder.exists() or not folder.is_dir():
        return []

    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS
    )


def load_sample_image(image_path: Path) -> tuple[np.ndarray, dict[str, Any]]:
    """Load and validate a clean reference image from disk."""
    if not image_path.exists():
        raise ValueError(f"Sample image not found: {image_path.name}")

    raw_bytes = image_path.read_bytes()
    return _decode_image_bytes(raw_bytes, image_path.name)


def resize_for_display(image: np.ndarray, max_width: int = 720) -> np.ndarray:
    """
    Proportionally downscale very wide images for fast, consistent UI previews
    without modifying the original array used for processing.
    """
    height, width = image.shape[:2]
    if width <= max_width:
        return image

    scale = max_width / float(width)
    new_height = max(1, int(round(height * scale)))
    pil_img = Image.fromarray(image)
    resized = pil_img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    return np.array(resized, dtype=np.uint8)
