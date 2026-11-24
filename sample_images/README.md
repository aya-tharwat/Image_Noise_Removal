# Sample Clean Reference Images

Place **5 to 8 clean reference images** (`.jpg`, `.jpeg`, or `.png`) in this folder for quick testing and academic demonstrations.

## Recommended Source
Download a small subset of clean ground-truth images from the academic reference dataset:
- https://www.kaggle.com/competitions/image-denoising-with-ga-ns/data

## What Images to Pick (5–8 images is enough)
Choose a diverse mix so filter behavior is easy to demonstrate:
1. **Sharp edges / geometric structures** — highlights edge-preserving filtering (Bilateral vs. Average/Gaussian).
2. **Fine textures / small details** — shows how larger kernel sizes blur fine details.
3. **Smooth gradients / plain backgrounds** — makes Gaussian and Speckle noise clearly visible.
4. **High-contrast scenes** — clearly demonstrates Salt-and-Pepper noise removal with the Median filter.
