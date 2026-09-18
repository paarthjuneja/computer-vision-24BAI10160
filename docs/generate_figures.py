import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath("."))

import cv2
import numpy as np
import matplotlib.pyplot as plt

from visionforge.common.io_utils import load_image
from visionforge.lowlevel.filters import apply_gaussian_blur, apply_laplacian
from visionforge.lowlevel.frequency import compute_fft_spectrum
from visionforge.lowlevel.histogram import apply_clahe
from visionforge.features.edges_corners import detect_canny_edges, detect_harris_corners
from visionforge.features.segmentation import segment_otsu, segment_kmeans
from visionforge.stereo_3d.depth_reconstruction import compute_disparity_map
from visionforge.motion_pattern.optical_flow import compute_dense_optical_flow
from visionforge.shape_from_x.photometric_stereo import compute_photometric_stereo, integrate_normals_to_depth

def generate_result_figures(data_dir="data", out_dir="docs/figures"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Low level figure
    sample = load_image(os.path.join(data_dir, "input_sample.png"))
    gauss = apply_gaussian_blur(sample, ksize=9)
    fft_spec = compute_fft_spectrum(sample)
    clahe_img = apply_clahe(sample)
    
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5), dpi=300)
    axes[0].imshow(cv2.cvtColor(sample, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original Input")
    axes[1].imshow(cv2.cvtColor(gauss, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Gaussian Blur")
    axes[2].imshow(fft_spec, cmap="gray")
    axes[2].set_title("2D FFT Spectrum")
    axes[3].imshow(cv2.cvtColor(clahe_img, cv2.COLOR_BGR2RGB))
    axes[3].set_title("CLAHE Enhanced")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "fig_lowlevel.png"), bbox_inches="tight")
    plt.close(fig)
    
    # 2. Features figure
    canny = detect_canny_edges(sample)
    harris = detect_harris_corners(sample)
    otsu = segment_otsu(sample)
    kmeans = segment_kmeans(sample, k=3)
    
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5), dpi=300)
    axes[0].imshow(canny, cmap="gray")
    axes[0].set_title("Canny Edges")
    axes[1].imshow(cv2.cvtColor(harris, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Harris Corners")
    axes[2].imshow(otsu, cmap="gray")
    axes[2].set_title("Otsu Segmentation")
    axes[3].imshow(cv2.cvtColor(kmeans, cv2.COLOR_BGR2RGB))
    axes[3].set_title("K-Means (k=3)")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "fig_features.png"), bbox_inches="tight")
    plt.close(fig)
    
    # 3. Stereo figure
    left = load_image(os.path.join(data_dir, "stereo_left.png"))
    right = load_image(os.path.join(data_dir, "stereo_right.png"))
    disp = compute_disparity_map(left, right, num_disparities=32, block_size=9)
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), dpi=300)
    axes[0].imshow(cv2.cvtColor(left, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Stereo Left")
    axes[1].imshow(cv2.cvtColor(right, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Stereo Right")
    axes[2].imshow(disp, cmap="plasma")
    axes[2].set_title("Disparity Map (SGBM)")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "fig_stereo.png"), bbox_inches="tight")
    plt.close(fig)
    
    # 4. Motion figure
    f1 = load_image(os.path.join(data_dir, "motion_frame1.png"))
    f2 = load_image(os.path.join(data_dir, "motion_frame2.png"))
    flow_vis, _ = compute_dense_optical_flow(f1, f2)
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), dpi=300)
    axes[0].imshow(cv2.cvtColor(f1, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Motion Frame 1")
    axes[1].imshow(cv2.cvtColor(f2, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Motion Frame 2")
    axes[2].imshow(cv2.cvtColor(flow_vis, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Dense Optical Flow (HSV)")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "fig_motion.png"), bbox_inches="tight")
    plt.close(fig)
    
    # 5. Photometric stereo figure
    lights = [
        [0.0, 0.577, 0.816],
        [0.577, 0.0, 0.816],
        [0.0, -0.577, 0.816],
        [-0.577, 0.0, 0.816]
    ]
    sphere_imgs = [load_image(os.path.join(data_dir, f"light{i+1}.png")) for i in range(4)]
    normals, albedo, vis_normals = compute_photometric_stereo(sphere_imgs, lights)
    _, vis_depth = integrate_normals_to_depth(normals)
    
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5), dpi=300)
    axes[0].imshow(cv2.cvtColor(sphere_imgs[0], cv2.COLOR_BGR2RGB))
    axes[0].set_title("Sample Light 1")
    axes[1].imshow(cv2.cvtColor(vis_normals, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Surface Normals (RGB)")
    axes[2].imshow(albedo, cmap="gray")
    axes[2].set_title("Estimated Albedo")
    axes[3].imshow(vis_depth, cmap="viridis")
    axes[3].set_title("3D Depth Reconstruction")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "fig_shape.png"), bbox_inches="tight")
    plt.close(fig)
    
    print("All result figures generated successfully.")

if __name__ == "__main__":
    generate_result_figures()
