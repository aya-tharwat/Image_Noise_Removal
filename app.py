"""
Image Noise Removal Laboratory — Main Streamlit Application (Phase 4: Spatial Filtering)

Provides a modern dark-themed dashboard layout with sidebar navigation
across four core views:
1. Dashboard
2. Noise Laboratory
3. Filter Comparison
4. About Project
"""

from pathlib import Path
import streamlit as st

from src.filters import (
    BILATERAL_DIAMETERS,
    FILTER_DESCRIPTIONS,
    FILTER_TYPES,
    KERNEL_SIZES,
    apply_filter,
    format_filter_params,
)
from src.image_utils import (
    list_sample_images,
    load_and_validate_image,
    load_sample_image,
    resize_for_display,
)
from src.noise import (
    INTENSITY_LEVELS,
    NOISE_DESCRIPTIONS,
    NOISE_TYPES,
    apply_noise,
    get_noise_parameter_label,
)


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


def init_session_state() -> None:
    """Initialize shared Streamlit session state keys once per session."""
    defaults = {
        "original_image": None,
        "image_info": None,
        "active_image_id": None,
        "noisy_image": None,
        "noise_type": None,
        "noise_intensity": None,
        "noise_param_label": None,
        "filtered_image": None,
        "filter_name": None,
        "filter_param_label": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_active_image(image, info: dict, image_id: str) -> None:
    """Store a new active clean image and clear stale noisy/filtered outputs."""
    if st.session_state.active_image_id != image_id:
        st.session_state.original_image = image
        st.session_state.image_info = info
        st.session_state.active_image_id = image_id
        st.session_state.noisy_image = None
        st.session_state.noise_type = None
        st.session_state.noise_intensity = None
        st.session_state.noise_param_label = None
        st.session_state.filtered_image = None
        st.session_state.filter_name = None
        st.session_state.filter_param_label = None


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
    """Render the interactive Noise Laboratory (Phase 2: Image Input & Preview)."""
    st.markdown(
        """
        <div class="hero-card">
            <span class="badge">Interactive Workspace</span>
            <h1>Noise Laboratory</h1>
            <p>
                Upload a clean JPG/PNG image or choose a reference sample to inspect
                it before applying controlled noise and spatial filters.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # Step 1: Image Input (Upload or Sample Selection)
    # ------------------------------------------------------------------
    st.subheader("1. Image Input")

    input_col, preview_col = st.columns([1, 1.3], gap="large")

    with input_col:
        input_mode = st.radio(
            label="Image Source",
            options=["Upload Clean Image", "Select Sample Image"],
            horizontal=True,
        )

        if input_mode == "Upload Clean Image":
            uploaded_file = st.file_uploader(
                label="Upload a clean image (JPG, JPEG, or PNG)",
                type=["jpg", "jpeg", "png"],
                help="Choose a clean reference image to use in your denoising experiments.",
            )
            if uploaded_file is not None:
                try:
                    image_rgb, info = load_and_validate_image(uploaded_file)
                    image_id = f"upload:{uploaded_file.name}:{uploaded_file.size}"
                    set_active_image(image_rgb, info, image_id)
                    st.success(f"Loaded **{info['filename']}** successfully.")
                except ValueError as err:
                    st.error(str(err))
        else:
            sample_paths = list_sample_images()
            if not sample_paths:
                st.info(
                    "No sample images found in `sample_images/` yet. "
                    "Add 5–8 clean JPG/PNG images from the Kaggle dataset into "
                    "`sample_images/`, or switch to **Upload Clean Image**."
                )
            else:
                sample_names = [p.name for p in sample_paths]
                selected_name = st.selectbox(
                    label="Choose a clean reference image",
                    options=sample_names,
                )
                selected_path = next(p for p in sample_paths if p.name == selected_name)
                try:
                    image_rgb, info = load_sample_image(selected_path)
                    image_id = f"sample:{selected_path.name}"
                    set_active_image(image_rgb, info, image_id)
                    st.success(f"Selected sample **{info['filename']}**.")
                except ValueError as err:
                    st.error(str(err))

        # Show image metadata if an image is currently loaded
        if st.session_state.image_info is not None:
            info = st.session_state.image_info
            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("Resolution", f"{info['width']} × {info['height']}")
            m2.metric("Format", info["format"])
            m3.metric("Color Space", f"RGB ({info['channels']}ch)")

            if info["original_mode"] != "RGB":
                st.caption(
                    f"Converted automatically from `{info['original_mode']}` to `RGB` "
                    "for consistent noise and filter processing."
                )

    with preview_col:
        if st.session_state.original_image is not None:
            preview_img = resize_for_display(st.session_state.original_image)
            st.image(
                preview_img,
                caption=f"Original Image — {st.session_state.image_info['filename']}",
                width="stretch",
            )
        else:
            st.markdown(
                """
                <div class="lab-card">
                    <span class="badge">Preview Area</span>
                    <h3>No Image Loaded Yet</h3>
                    <p>
                        Upload a clean JPG, JPEG, or PNG file on the left (or select a
                        sample image) to preview it here.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ------------------------------------------------------------------
    # Step 2: Noise Generation (Gaussian, Salt-and-Pepper, Speckle)
    # ------------------------------------------------------------------
    st.subheader("2. Noise Generation")

    if st.session_state.original_image is None:
        st.info("Upload or select a clean image in **Step 1** first to generate noise.")
    else:
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.3, 1.3, 1], gap="medium")

        with ctrl_col1:
            selected_noise = st.selectbox(
                label="Noise Type",
                options=NOISE_TYPES,
                help="Choose which classical noise model to inject into the clean image.",
            )

        with ctrl_col2:
            selected_intensity = st.select_slider(
                label="Noise Intensity",
                options=INTENSITY_LEVELS,
                value="Medium",
                help="Select Low, Medium, or High noise strength.",
            )

        param_label = get_noise_parameter_label(selected_noise, selected_intensity)

        with ctrl_col3:
            st.markdown("<br>", unsafe_allow_html=True)
            apply_clicked = st.button(
                "Apply Noise",
                type="primary",
                width="stretch",
            )

        st.caption(
            f"**{selected_noise} ({selected_intensity} — {param_label}):** "
            f"{NOISE_DESCRIPTIONS[selected_noise]}"
        )

        if apply_clicked:
            noisy = apply_noise(
                st.session_state.original_image,
                noise_type=selected_noise,
                intensity=selected_intensity,
            )
            st.session_state.noisy_image = noisy
            st.session_state.noise_type = selected_noise
            st.session_state.noise_intensity = selected_intensity
            st.session_state.noise_param_label = param_label
            # Clear previous filtered output since the noisy image changed
            st.session_state.filtered_image = None
            st.session_state.filter_name = None
            st.session_state.filter_param_label = None

        if st.session_state.noisy_image is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            orig_col, noisy_col = st.columns(2, gap="medium")

            with orig_col:
                st.image(
                    resize_for_display(st.session_state.original_image),
                    caption="Original Clean Image",
                    width="stretch",
                )

            with noisy_col:
                st.image(
                    resize_for_display(st.session_state.noisy_image),
                    caption=(
                        f"Noisy Image — {st.session_state.noise_type} "
                        f"({st.session_state.noise_intensity}, "
                        f"{st.session_state.noise_param_label})"
                    ),
                    width="stretch",
                )

    st.divider()

    # ------------------------------------------------------------------
    # Step 3: Spatial Filtering (Average, Gaussian, Median, Bilateral)
    # ------------------------------------------------------------------
    st.subheader("3. Spatial Filtering")

    if st.session_state.noisy_image is None:
        st.info("Generate a noisy image in **Step 2** first to apply spatial filters.")
    else:
        f_col1, f_col2, f_col3 = st.columns([1.2, 1.5, 0.9], gap="medium")

        with f_col1:
            selected_filter = st.selectbox(
                label="Spatial Filter",
                options=FILTER_TYPES,
                help="Choose a classical OpenCV spatial filter to denoise the image.",
            )

        # Default parameter values (adjusted below based on selected filter)
        kernel_size = 5
        sigma = 0.0
        diameter = 9
        sigma_color = 75.0
        sigma_space = 75.0

        with f_col2:
            if selected_filter in ("Average Filter", "Median Filter"):
                kernel_size = st.select_slider(
                    label="Kernel Size (odd window)",
                    options=KERNEL_SIZES,
                    value=5,
                    help="Larger kernels smooth more strongly but can blur fine details.",
                )
            elif selected_filter == "Gaussian Filter":
                p1, p2 = st.columns(2)
                with p1:
                    kernel_size = st.select_slider(
                        label="Kernel Size",
                        options=KERNEL_SIZES,
                        value=5,
                    )
                with p2:
                    sigma = st.slider(
                        label="Sigma (0 = auto)",
                        min_value=0.0,
                        max_value=5.0,
                        value=0.0,
                        step=0.5,
                    )
            else:  # Bilateral Filter
                p1, p2 = st.columns(2)
                with p1:
                    diameter = st.select_slider(
                        label="Diameter (d)",
                        options=BILATERAL_DIAMETERS,
                        value=9,
                    )
                with p2:
                    sigma_val = st.slider(
                        label="Sigma Color & Space",
                        min_value=25,
                        max_value=150,
                        value=75,
                        step=25,
                    )
                    sigma_color = float(sigma_val)
                    sigma_space = float(sigma_val)

        filter_param_text = format_filter_params(
            filter_name=selected_filter,
            kernel_size=kernel_size,
            sigma=sigma,
            diameter=diameter,
            sigma_color=sigma_color,
            sigma_space=sigma_space,
        )

        with f_col3:
            st.markdown("<br>", unsafe_allow_html=True)
            apply_filter_clicked = st.button(
                "Apply Filter",
                type="primary",
                width="stretch",
            )

        st.caption(
            f"**{selected_filter} ({filter_param_text}):** "
            f"{FILTER_DESCRIPTIONS[selected_filter]}"
        )

        if apply_filter_clicked:
            filtered = apply_filter(
                st.session_state.noisy_image,
                filter_name=selected_filter,
                kernel_size=kernel_size,
                sigma=sigma,
                diameter=diameter,
                sigma_color=sigma_color,
                sigma_space=sigma_space,
            )
            st.session_state.filtered_image = filtered
            st.session_state.filter_name = selected_filter
            st.session_state.filter_param_label = filter_param_text

        if st.session_state.filtered_image is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            n_col, flt_col = st.columns(2, gap="medium")

            with n_col:
                st.image(
                    resize_for_display(st.session_state.noisy_image),
                    caption=(
                        f"Noisy Input — {st.session_state.noise_type} "
                        f"({st.session_state.noise_intensity})"
                    ),
                    width="stretch",
                )

            with flt_col:
                st.image(
                    resize_for_display(st.session_state.filtered_image),
                    caption=(
                        f"Filtered Output — {st.session_state.filter_name} "
                        f"({st.session_state.filter_param_label})"
                    ),
                    width="stretch",
                )

    st.divider()

    # Upcoming phase placeholder
    st.markdown(
        """
        <div class="lab-card">
            <span class="badge">Coming in Phase 5</span>
            <h3>4. 3-Way Visual Comparison &amp; MSE / PSNR Metrics</h3>
            <p>
                Side-by-side Original, Noisy, and Filtered comparison grid with
                quantitative MSE/PSNR scores and an automatic experiment summary.
            </p>
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
    init_session_state()

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
        st.caption("Phase 4 • Spatial Filtering")

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
