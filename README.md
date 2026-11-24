# Image Noise Removal Laboratory

An interactive Python & Streamlit application demonstrating how classical spatial filters remove different types of digital image noise — built strictly with classical image processing (**NumPy** and **OpenCV**), with no Machine Learning or Deep Learning.

---

## Features

- **Clean Image Input (FR1):** Upload `.jpg`, `.jpeg`, or `.png` images or select from `sample_images/`, with Pillow integrity validation and automatic conversion of grayscale/RGBA images to 3-channel RGB.
- **3 Classical Noise Generators (FR2):** Inject **Gaussian**, **Salt-and-Pepper**, or **Speckle** noise using pure NumPy at **Low**, **Medium**, and **High** intensities.
- **4 Spatial Filters (FR3):** Denoise images using OpenCV built-in filters — **Average** (`cv2.blur`), **Gaussian** (`cv2.GaussianBlur`), **Median** (`cv2.medianBlur`), and **Bilateral** (`cv2.bilateralFilter`) — with beginner-friendly parameter controls.
- **3-Way Visual Comparison (FR4):** Inspect **Original**, **Noisy**, and **Filtered** images side by side with consistent dimensions.
- **Quantitative Analysis & Chart (FR5 & FR6):** Pure-NumPy **MSE** and **PSNR (dB)** metrics, an all-filters **Filter Comparison** workspace, a dark-themed **Matplotlib PSNR bar chart**, and automatic academic insights.
- **Modern Dark UI:** Clean 4-page dashboard (**Dashboard**, **Noise Laboratory**, **Filter Comparison**, **About Project**).

---

## Project Structure

```text
Image_Noise_Removal/
├── .streamlit/
│   └── config.toml          # Modern dark theme settings
├── assets/
│   └── styles.css           # Subtle dark-UI card & button styling
├── docs/
│   └── EXECUTION_PLAN.md    # Phase-by-phase execution plan
├── sample_images/           # Clean reference images (5–8 from Kaggle subset)
├── src/
│   ├── __init__.py
│   ├── image_utils.py       # Upload validation, RGB normalization, display resizing
│   ├── noise.py             # Gaussian, Salt-and-Pepper, and Speckle noise (NumPy)
│   ├── filters.py           # Average, Gaussian, Median, and Bilateral filters (OpenCV)
│   ├── metrics.py           # MSE, PSNR, all-filter benchmarking & insights
│   └── visualization.py     # Dark-themed Matplotlib PSNR bar chart
├── app.py                   # Main Streamlit application
├── requirements.txt         # Minimal Python dependencies
└── README.md                # Setup and usage instructions
```

---

## Installation & Setup

### 1. Prerequisites
- Python **3.10+** installed locally.

### 2. Create & Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Add Sample Reference Images
Download **5 to 8 clean ground-truth images** (`.jpg` or `.png`) from the reference dataset and place them inside `sample_images/`:
- https://www.kaggle.com/competitions/image-denoising-with-ga-ns/data

*(You can also upload any clean `.jpg`, `.jpeg`, or `.png` image directly inside the app.)*

---

## Running the Application

From the project root:

```powershell
# Windows (with .venv activated, or directly via .\.venv\Scripts\streamlit.exe)
streamlit run app.py
```

Then open the local URL printed in your terminal (default: `http://localhost:8501`).

---

## Quick Academic Reference: Noise vs. Spatial Filters

| Noise Type | How It Corrupts Pixels | Best Spatial Filter | Why |
| :--- | :--- | :--- | :--- |
| **Gaussian Noise** | Adds zero-mean normal random values to every pixel | **Gaussian** or **Bilateral Filter** | Weighted averaging cancels random fluctuations; Bilateral also preserves sharp edges. |
| **Salt-and-Pepper Noise** | Replaces random pixels with pure `255` (white) or `0` (black) | **Median Filter** | Non-linear median discards extreme `0`/`255` outliers instead of smearing them. |
| **Speckle Noise** | Multiplicative grain (`img + img * N(0, σ)`), stronger in bright regions | **Gaussian**, **Median**, or **Bilateral Filter** | Smooths granular variance while balancing noise reduction and edge detail. |

### Quality Metrics Used
- **MSE (Mean Squared Error):** Average squared pixel difference from the clean original (**lower is better**).
- **PSNR (Peak Signal-to-Noise Ratio, dB):** Logarithmic fidelity score derived from MSE (**higher is better**; `∞ dB` means identical to the original).
