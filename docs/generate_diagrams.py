import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_diagrams(out_dir="docs/diagrams"):
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. System Architecture Diagram
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    
    # Title
    ax.text(5, 5.7, "VisionForge: System Architecture", ha="center", va="center", fontsize=15, fontweight="bold", color="#1E293B")
    
    # CLI Layer
    rect_cli = patches.FancyBboxPatch((1, 4.6), 8, 0.7, boxstyle="round,pad=0.1", ec="#2563EB", fc="#DBEAFE", lw=2)
    ax.add_patch(rect_cli)
    ax.text(5, 4.95, "CLI Interface Layer (visionforge.cli - Argparse Dispatcher)", ha="center", va="center", fontsize=11, fontweight="bold", color="#1E40AF")
    
    # 5 Functional Modules
    colors = ["#FEE2E2", "#FEF3C7", "#D1FAE5", "#E0E7FF", "#FCE7F3"]
    edge_colors = ["#DC2626", "#D97706", "#059669", "#4F46E5", "#DB2777"]
    modules = [
        ("Module 1\nLow-Level\n(Filters, FFT,\nTransforms)", 1.0, 2.5),
        ("Module 2\nStereo 3D\n(Epipolar, SGBM,\nPoint Cloud)", 2.6, 2.5),
        ("Module 3\nFeatures\n(Canny, Harris,\nSegmentation)", 4.2, 2.5),
        ("Module 4\nMotion/Pattern\n(MOG2, Flow,\nPCA)", 5.8, 2.5),
        ("Module 5\nShape from X\n(Photometric\nStereo, Depth)", 7.4, 2.5)
    ]
    
    for i, (name, x, y) in enumerate(modules):
        patch = patches.FancyBboxPatch((x, y), 1.6, 1.4, boxstyle="round,pad=0.08", ec=edge_colors[i], fc=colors[i], lw=1.5)
        ax.add_patch(patch)
        ax.text(x + 0.8, y + 0.7, name, ha="center", va="center", fontsize=9, fontweight="bold", color="#1F2937")
        # Arrow down from CLI
        ax.annotate('', xy=(x + 0.8, y + 1.4), xytext=(x + 0.8, 4.6),
                    arrowprops=dict(arrowstyle="->", color="#4B5563", lw=1.5))
                    
    # Common Layer
    rect_common = patches.FancyBboxPatch((1, 0.8), 8, 1.0, boxstyle="round,pad=0.1", ec="#4B5563", fc="#F3F4F6", lw=2)
    ax.add_patch(rect_common)
    ax.text(5, 1.5, "Common Core Utilities & Storage (visionforge.common)", ha="center", va="center", fontsize=11, fontweight="bold", color="#111827")
    ax.text(5, 1.1, "Image I/O  •  ASCII PLY Point Cloud Writer  •  Metrics (MSE, PSNR, Entropy)", ha="center", va="center", fontsize=9, color="#4B5563")
    
    for _, x, y in modules:
        ax.annotate('', xy=(x + 0.8, 1.8), xytext=(x + 0.8, y),
                    arrowprops=dict(arrowstyle="->", color="#4B5563", lw=1.5))
                    
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "architecture_diagram.png"), bbox_inches="tight")
    plt.close(fig)

    # 2. Workflow Diagram
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    
    ax.text(5, 4.7, "VisionForge: End-to-End Processing Workflow", ha="center", va="center", fontsize=14, fontweight="bold", color="#1E293B")
    
    steps = [
        ("User Input\nCLI Command &\nImage Files", 0.5, "#EFF6FF", "#3B82F6"),
        ("Validation &\nImage Loading\n(io_utils)", 2.4, "#F0FDF4", "#22C55E"),
        ("Computer Vision\nPipeline\nExecution", 4.3, "#FEF3C7", "#F59E0B"),
        ("Diagnostic &\nQuality Metrics\n(PSNR, Entropy)", 6.2, "#F3E8FF", "#A855F7"),
        ("Output Storage\n(Images, Masks,\nPLY Point Cloud)", 8.1, "#FEE2E2", "#EF4444")
    ]
    
    for i, (text, x, fc, ec) in enumerate(steps):
        p = patches.FancyBboxPatch((x, 1.8), 1.4, 1.6, boxstyle="round,pad=0.08", ec=ec, fc=fc, lw=1.8)
        ax.add_patch(p)
        ax.text(x + 0.7, 2.6, text, ha="center", va="center", fontsize=9, fontweight="bold", color="#1F2937")
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + 1.4 + 0.5, 2.6), xytext=(x + 1.4, 2.6),
                        arrowprops=dict(arrowstyle="->", color="#374151", lw=2.0))
                        
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "workflow_diagram.png"), bbox_inches="tight")
    plt.close(fig)

    # 3. Use Case Diagram
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 6)
    ax.axis("off")
    
    ax.text(4.5, 5.7, "VisionForge: Use Case Diagram", ha="center", va="center", fontsize=14, fontweight="bold", color="#1E293B")
    
    # Actor: User
    ax.plot([1.2], [3.2], "o", markersize=14, color="#1E293B")
    ax.plot([1.2, 1.2], [3.0, 2.3], "-", color="#1E293B", lw=2)
    ax.plot([0.8, 1.6], [2.7, 2.7], "-", color="#1E293B", lw=2)
    ax.plot([1.2, 0.9], [2.3, 1.7], "-", color="#1E293B", lw=2)
    ax.plot([1.2, 1.5], [2.3, 1.7], "-", color="#1E293B", lw=2)
    ax.text(1.2, 1.4, "Student / User", ha="center", va="center", fontsize=10, fontweight="bold")
    
    # Boundary box
    box = patches.FancyBboxPatch((2.8, 0.5), 5.8, 4.8, boxstyle="round,pad=0.1", ec="#9CA3AF", fc="#F9FAFB", lw=1.5, ls="--")
    ax.add_patch(box)
    ax.text(5.7, 5.0, "VisionForge System", ha="center", va="center", fontsize=11, fontweight="bold", color="#4B5563")
    
    usecases = [
        ("Filter & Transform Images", 4.3),
        ("Compute Stereo Disparity & Export PLY", 3.5),
        ("Detect Edges, Corners & Keypoints", 2.7),
        ("Analyze Motion & Optical Flow", 1.9),
        ("Reconstruct 3D Surface via Photometric Stereo", 1.1)
    ]
    
    for text, y in usecases:
        ellipse = patches.Ellipse((5.7, y), 4.6, 0.55, ec="#2563EB", fc="#EFF6FF", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(5.7, y, text, ha="center", va="center", fontsize=9, fontweight="bold", color="#1E40AF")
        ax.plot([1.5, 3.4], [2.6, y], color="#6B7280", lw=1.2)
        
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "usecase_diagram.png"), bbox_inches="tight")
    plt.close(fig)

    # 4. Class / Component Diagram
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    
    ax.text(5, 5.7, "VisionForge: Component & Class Architecture", ha="center", va="center", fontsize=14, fontweight="bold", color="#1E293B")
    
    components = [
        ("visionforge.lowlevel", ["+ apply_box_blur()", "+ apply_gaussian_blur()", "+ compute_fft_spectrum()", "+ rotate_image()", "+ equalize_histogram()"], 0.6, 2.7, 2.7, 2.4),
        ("visionforge.stereo_3d", ["+ compute_disparity_map()", "+ disparity_to_point_cloud()", "+ compute_fundamental_matrix()", "+ stitch_images_homography()"], 3.65, 2.7, 2.7, 2.4),
        ("visionforge.features", ["+ detect_canny_edges()", "+ detect_harris_corners()", "+ extract_and_match_features()", "+ segment_otsu()", "+ segment_kmeans()"], 6.7, 2.7, 2.7, 2.4),
        ("visionforge.motion_pattern", ["+ compute_frame_difference()", "+ BackgroundModel", "+ compute_dense_optical_flow()", "+ compress_image_pca()"], 1.5, 0.4, 3.2, 1.8),
        ("visionforge.shape_from_x", ["+ compute_photometric_stereo()", "+ integrate_normals_to_depth()"], 5.3, 0.4, 3.2, 1.8)
    ]
    
    for title, methods, x, y, w, h in components:
        p = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", ec="#3B82F6", fc="#FFFFFF", lw=1.5)
        ax.add_patch(p)
        header = patches.Rectangle((x, y + h - 0.4), w, 0.4, ec="#3B82F6", fc="#DBEAFE", lw=1.5)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.2, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1E40AF")
        for idx, m in enumerate(methods):
            ax.text(x + 0.1, y + h - 0.65 - (idx * 0.3), m, ha="left", va="center", fontsize=7.5, color="#1F2937")
            
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "class_diagram.png"), bbox_inches="tight")
    plt.close(fig)

    # 5. Sequence Diagram
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    
    ax.text(5, 5.7, "VisionForge: Disparity & 3D Reconstruction Sequence", ha="center", va="center", fontsize=14, fontweight="bold", color="#1E293B")
    
    participants = [
        ("User / CLI", 1.5),
        ("io_utils", 3.8),
        ("StereoSGBM Engine", 6.2),
        ("3D Exporter", 8.5)
    ]
    
    for name, x in participants:
        p = patches.FancyBboxPatch((x - 1.0, 4.8), 2.0, 0.5, boxstyle="round,pad=0.05", ec="#2563EB", fc="#EFF6FF", lw=1.5)
        ax.add_patch(p)
        ax.text(x, 5.05, name, ha="center", va="center", fontsize=9, fontweight="bold", color="#1E40AF")
        ax.plot([x, x], [4.8, 0.8], "--", color="#9CA3AF", lw=1.2)
        
    calls = [
        (1.5, 3.8, 4.3, "load_image(left, right)"),
        (3.8, 1.5, 3.8, "left_img, right_img"),
        (1.5, 6.2, 3.2, "compute_disparity_map(left, right)"),
        (6.2, 1.5, 2.7, "disparity_matrix"),
        (1.5, 8.5, 2.1, "disparity_to_point_cloud(disp, focal, baseline)"),
        (8.5, 8.5, 1.6, "save_point_cloud_ply(path, points)"),
        (8.5, 1.5, 1.1, "return success & points count")
    ]
    
    for x1, x2, y, label in calls:
        if x1 == x2:
            ax.annotate('', xy=(x1, y - 0.2), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5))
            ax.text(x1 - 0.1, y - 0.1, label, ha="right", va="center", fontsize=7.5, color="#DC2626", fontweight="bold")
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
            ax.text((x1 + x2) / 2, y + 0.15, label, ha="center", va="center", fontsize=8, color="#1F2937")
            
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "sequence_diagram.png"), bbox_inches="tight")
    plt.close(fig)
    print("All diagrams generated successfully.")

if __name__ == "__main__":
    generate_diagrams()
