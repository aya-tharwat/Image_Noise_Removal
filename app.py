"""
Image Noise Removal Laboratory — Main Streamlit Application (Phase 1: UI Shell)

Provides a modern dark-themed dashboard layout with sidebar navigation
across four core views:
1. Dashboard
2. Noise Laboratory
3. Filter Comparison
4. About Project
"""

from pathlib import Path
import streamlit as st


# ---------------------------------------------------------------------------
# Page Configuration & Custom CSS
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Image Noise Removal Laboratory",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_custom_css() -> None:
    """Load subtle dark-UI styling from assets/styles.css if present."""
    css_path = Path(__file__).parent / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Page Renderers
# ---------------------------------------------------------------------------
def render_dashboard() -> None:
    """Render the main Dashboard welcome page and tool overview."""
    st.markdown(
        """
        <div class="hero-card">
            <span class="badge">Classical Image Processing Lab</span>
            <h1>Image Noise Removal Laboratory</h1>
            <p>
                An interactive workspace for exploring how classical spatial filters
                remove different types of digital image noise. Upload a clean image,
                inject controlled noise, apply spatial filters, and compare results
                both visually and quantitatively.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick-start workflow steps
    st.subheader("How to Run an Experiment")
    s1, s2, s3, s4 = st.columns(4, gap="medium")

    with s1:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">Step 1</div>
                <h4>Load Clean Image</h4>
                <p>Upload a JPG/PNG image or choose a clean reference image from the sample library.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">Step 2</div>
                <h4>Generate Noise</h4>
                <p>Select Gaussian, Salt-and-Pepper, or Speckle noise at Low, Medium, or High intensity.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">Step 3</div>
                <h4>Apply Spatial Filter</h4>
                <p>Denoise with Average, Gaussian, Median, or Bilateral filtering and tune kernel size.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s4:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-number">Step 4</div>
                <h4>Compare &amp; Analyze</h4>
                <p>Inspect Original, Noisy, and Filtered images side by side with MSE/PSNR analysis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Overview of available noise models and spatial filters
    st.subheader("Available Laboratory Tools")
    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.markdown(
            """
            <div class="lab-card">
                <span class="badge">Noise Models (NumPy)</span>
                <h3>3 Classical Noise Generators</h3>
                <p>
                    <strong>• Gaussian Noise:</strong> Additive random sensor noise following a normal distribution.<br>
                    <strong>• Salt-and-Pepper Noise:</strong> Impulse noise producing sharp white and black pixels.<br>
                    <strong>• Speckle Noise:</strong> Multiplicative granular distortion proportional to pixel intensity.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
            <div class="lab-card">
                <span class="badge">Spatial Filters (OpenCV)</span>
                <h3>4 Classical Denoising Filters</h3>
                <p>
                    <strong>• Average Filter:</strong> Simple neighborhood mean smoothing.<br>
                    <strong>• Gaussian Filter:</strong> Weighted bell-curve smoothing for softer blurring.<br>
                    <strong>• Median Filter:</strong> Non-linear median replacement—ideal for impulse noise.<br>
                    <strong>• Bilateral Filter:</strong> Edge-preserving smoothing using spatial &amp; intensity weights.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_noise_laboratory() -> None:
    """Placeholder for the interactive Noise Laboratory (Phases 2–5)."""
    st.markdown(
        """
        <div class="hero-card">
            <span class="badge">Interactive Workspace</span>
            <h1>Noise Laboratory</h1>
            <p>
                Upload a clean image, add controlled noise, apply spatial filters,
                and inspect side-by-side results in one streamlined workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(
            """
            <div class="lab-card">
                <span class="badge">Coming in Phase 2</span>
                <h3>1. Image Input</h3>
                <p>Upload JPG/PNG files or pick a clean sample image with automatic validation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="lab-card">
                <span class="badge">Coming in Phase 3</span>
                <h3>2. Noise Generation</h3>
                <p>Apply Gaussian, Salt-and-Pepper, or Speckle noise at Low, Medium, or High intensity.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="lab-card">
                <span class="badge">Coming in Phases 4–5</span>
                <h3>3. Filtering &amp; Comparison</h3>
                <p>Apply spatial filters and compare Original, Noisy, and Filtered images with PSNR.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_filter_comparison() -> None:
    """Placeholder for the all-filters comparison workspace (Phase 6)."""
    st.markdown(
        """
        <div class="hero-card">
            <span class="badge">Benchmarking Workspace</span>
            <h1>Filter Comparison</h1>
            <p>
                Evaluate Average, Gaussian, Median, and Bilateral filters side by side
                on the same noisy image to see which method performs best.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="lab-card">
            <span class="badge">Coming in Phase 6</span>
            <h3>All-Filter Comparison Grid &amp; PSNR Chart</h3>
            <p>
                This workspace will run all four classical spatial filters simultaneously,
                display a visual comparison grid, plot a PSNR bar chart, and highlight the
                most effective filter for the selected noise type.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_about_project() -> None:
    """Render concise academic documentation for the project."""
    st.markdown(
        """
        <div class="hero-card">
            <span class="badge">Academic Reference</span>
            <h1>About This Project</h1>
            <p>
                <strong>Image Noise Removal Laboratory</strong> demonstrates classical
                spatial-domain image denoising without Machine Learning or Deep Learning,
                built with Python, NumPy, OpenCV, Pillow, Matplotlib, and Streamlit.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown(
            """
            <div class="lab-card">
                <h3>Why Different Filters Suit Different Noise</h3>
                <p>
                    • <strong>Gaussian Noise</strong> spreads smoothly around pixel values,
                    so <strong>Gaussian</strong> and <strong>Bilateral</strong> filters
                    average out random fluctuations effectively.<br><br>
                    • <strong>Salt-and-Pepper Noise</strong> creates extreme 0 or 255
                    outliers. Linear averages smear those extremes, while the
                    <strong>Median Filter</strong> replaces each pixel with the middle
                    neighbor value, cleanly removing impulse dots.<br><br>
                    • <strong>Speckle Noise</strong> scales with brightness; combining
                    smooth spatial averaging or edge-preserving filtering helps suppress
                    grain while preserving structure.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="lab-card">
                <h3>Evaluation Metric &amp; Dataset Strategy</h3>
                <p>
                    • <strong>MSE (Mean Squared Error):</strong> Average squared pixel
                    difference between a processed image and the clean original
                    (lower is better).<br><br>
                    • <strong>PSNR (Peak Signal-to-Noise Ratio):</strong> Logarithmic
                    quality score in decibels (dB) derived from MSE
                    (higher means closer to the clean original).<br><br>
                    • <strong>Dataset Usage:</strong> Clean reference images are taken
                    from a lightweight subset of the Kaggle <em>Image Denoising with
                    GANs</em> dataset so noise can be generated dynamically with exact
                    ground-truth references.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Sidebar Navigation & Entrypoint
# ---------------------------------------------------------------------------
def main() -> None:
    """Initialize styling, render sidebar navigation, and route active page."""
    load_custom_css()

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <h2>🔬 Noise Removal Lab</h2>
                <p>Classical Spatial Filtering</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            label="Navigation",
            options=[
                "Dashboard",
                "Noise Laboratory",
                "Filter Comparison",
                "About Project",
            ],
            label_visibility="collapsed",
        )

        st.divider()
        st.caption("Phase 1 • UI Shell & Navigation")

    if page == "Dashboard":
        render_dashboard()
    elif page == "Noise Laboratory":
        render_noise_laboratory()
    elif page == "Filter Comparison":
        render_filter_comparison()
    elif page == "About Project":
        render_about_project()


if __name__ == "__main__":
    main()
